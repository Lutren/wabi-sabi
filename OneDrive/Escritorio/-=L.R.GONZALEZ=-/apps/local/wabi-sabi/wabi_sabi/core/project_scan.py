from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from wabi_sabi.core.subprocess_utils import run_hidden


PROJECT_SCAN_SCHEMA = "wabi.project_scan.v1"
DENY_DIRS = {
    ".git",
    ".claw",
    ".claude",
    ".wrangler",
    ".venv",
    "node_modules",
    "__pycache__",
    "runtime",
    "dist",
    "build",
    "target",
    "releases",
    "game-private",
    "metaevo-tcg",
    "tcg",
    "game_bridge",
}


def scan_project(*, workspace: str | Path, max_depth: int = 3, max_files: int = 3000) -> dict[str, Any]:
    root = Path(workspace).resolve()
    files = _walk_files(root, max_depth=max_depth, max_files=max_files)
    rel_names = {path.relative_to(root).as_posix() for path in files}
    root_names = {path.name for path in files if path.parent == root}
    package_json = _package_json_summary(root / "package.json") if "package.json" in root_names else None
    languages = _detect_languages(rel_names)
    managers = _detect_package_managers(root_names)
    test_commands = _detect_test_commands(root_names, rel_names, package_json)
    boundaries = _repo_boundaries(root, max_depth=max_depth)
    return {
        "schema": PROJECT_SCAN_SCHEMA,
        "ok": True,
        "workspace": str(root),
        "files_sampled": len(files),
        "max_depth": max_depth,
        "package_managers": managers,
        "languages": languages,
        "test_commands": test_commands,
        "repo_boundaries": boundaries,
        "entry_files": _entry_files(rel_names),
        "config_files": _config_files(rel_names),
        "limits": {
            "content_included": False,
            "package_json_scripts_read": bool(package_json),
            "deny_dirs": sorted(DENY_DIRS),
            "max_files": max_files,
        },
    }


def _walk_files(root: Path, *, max_depth: int, max_files: int) -> list[Path]:
    result: list[Path] = []
    stack: list[tuple[Path, int]] = [(root, 0)]
    while stack and len(result) < max_files:
        directory, depth = stack.pop()
        try:
            entries = sorted(directory.iterdir(), key=lambda item: item.name.lower())
        except OSError:
            continue
        for entry in entries:
            if len(result) >= max_files:
                break
            if entry.is_dir():
                if entry.name.lower() in DENY_DIRS:
                    continue
                if depth < max_depth:
                    stack.append((entry, depth + 1))
            elif entry.is_file():
                result.append(entry)
    return result


def _detect_package_managers(root_names: set[str]) -> list[str]:
    managers: list[str] = []
    if "pyproject.toml" in root_names:
        managers.append("python:pyproject")
    if "requirements.txt" in root_names:
        managers.append("python:pip")
    if "uv.lock" in root_names:
        managers.append("python:uv")
    if "poetry.lock" in root_names:
        managers.append("python:poetry")
    if "package.json" in root_names:
        managers.append("node:package-json")
    if "pnpm-lock.yaml" in root_names:
        managers.append("node:pnpm")
    if "package-lock.json" in root_names:
        managers.append("node:npm")
    if "yarn.lock" in root_names:
        managers.append("node:yarn")
    if "bun.lockb" in root_names:
        managers.append("node:bun")
    if "Cargo.toml" in root_names:
        managers.append("rust:cargo")
    if "go.mod" in root_names:
        managers.append("go:modules")
    return managers


def _detect_languages(rel_names: set[str]) -> list[str]:
    suffixes = {Path(name).suffix.lower() for name in rel_names}
    languages: list[str] = []
    if ".py" in suffixes:
        languages.append("python")
    if suffixes.intersection({".js", ".jsx", ".ts", ".tsx"}):
        languages.append("javascript/typescript")
    if ".rs" in suffixes:
        languages.append("rust")
    if ".go" in suffixes:
        languages.append("go")
    if ".md" in suffixes:
        languages.append("markdown")
    return languages


def _detect_test_commands(
    root_names: set[str],
    rel_names: set[str],
    package_json: dict[str, Any] | None,
) -> list[dict[str, str]]:
    commands: list[dict[str, str]] = []
    if "pyproject.toml" in root_names or "requirements.txt" in root_names or any(name.startswith("tests/") for name in rel_names):
        commands.append({"command": "python -m pytest -q", "source": "python_tests_detected"})
    if package_json:
        scripts = package_json.get("scripts", {})
        for script in ["test", "typecheck", "lint", "build"]:
            if script in scripts:
                commands.append({"command": f"npm run {script}", "source": f"package_json:{script}"})
    if "Cargo.toml" in root_names:
        commands.append({"command": "cargo test", "source": "cargo_manifest"})
    if "go.mod" in root_names:
        commands.append({"command": "go test ./...", "source": "go_mod"})
    return commands


def _repo_boundaries(root: Path, *, max_depth: int) -> dict[str, Any]:
    current = _git_root(root)
    nested: list[str] = []
    for directory in _walk_dirs(root, max_depth=max_depth):
        if (directory / ".git").exists() and directory != root:
            nested.append(directory.relative_to(root).as_posix())
    return {
        "current_git_root": current,
        "nested_git_roots": sorted(nested),
    }


def _git_root(root: Path) -> str:
    try:
        proc = run_hidden(
            ["git", "rev-parse", "--show-toplevel"],
            cwd=str(root),
            capture_output=True,
            text=True,
            timeout=5,
        )
    except Exception:
        return ""
    if proc.returncode != 0:
        return ""
    return proc.stdout.strip()


def _walk_dirs(root: Path, *, max_depth: int) -> list[Path]:
    result: list[Path] = []
    stack: list[tuple[Path, int]] = [(root, 0)]
    while stack:
        directory, depth = stack.pop()
        result.append(directory)
        if depth >= max_depth:
            continue
        try:
            entries = sorted(directory.iterdir(), key=lambda item: item.name.lower())
        except OSError:
            continue
        for entry in entries:
            if entry.is_dir() and entry.name.lower() not in DENY_DIRS:
                stack.append((entry, depth + 1))
    return result


def _package_json_summary(path: Path) -> dict[str, Any] | None:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None
    scripts = payload.get("scripts", {})
    if not isinstance(scripts, dict):
        scripts = {}
    return {
        "name": payload.get("name", ""),
        "scripts": {key: str(value) for key, value in scripts.items()},
    }


def _entry_files(rel_names: set[str]) -> list[str]:
    candidates = [
        "pyproject.toml",
        "package.json",
        "Cargo.toml",
        "go.mod",
        "README.md",
        "src/main.py",
        "main.py",
        "app.py",
        "index.js",
        "src/index.ts",
    ]
    return [item for item in candidates if item in rel_names]


def _config_files(rel_names: set[str]) -> list[str]:
    names = [
        "pyproject.toml",
        "pytest.ini",
        "package.json",
        "tsconfig.json",
        "vite.config.ts",
        "Cargo.toml",
        "go.mod",
        "ruff.toml",
    ]
    return [item for item in names if item in rel_names]
