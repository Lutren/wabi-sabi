from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


ROOT = Path(__file__).resolve().parents[2]

DENY_SUBSTRINGS = [
    "/.git/",
    "/node_modules/",
    "/.venv",
    "/__pycache__/",
    "/.pytest_cache/",
    "/.mypy_cache/",
    "/.ruff_cache/",
    "/target/",
    "/dist/",
    "/build/",
    "/release/",
    "/releases/",
    "/_archive",
    "/_archivar",
    "/apps/residueos/runtime/",
    "/packages/open-dev/residueos/runtime/",
    "/.claw/",
    "/.claude/",
    "/.wrangler/",
    "/.test_",
    "/tools/pentest_repos/",
    "/tools/vendor/",
    "/.skills/",
    "/github-modules/",
    "/core/sadtalker/",
    "/core/wav2lip/",
]

PRIVATE_GAME_SUBSTRINGS = [
    "/-=medioevo=-/-=libros/metaevo-tcg/",
    "/-=medioevo=-/-=libros/claudio/tcg/",
    "/-=medioevo=-/-=libros/claudio/runtime/game_bridge/",
    "/productos_medioevo/04_audiovisual_y_tcg/",
]

SECRET_NAME_MARKERS = [
    ".env",
    "secret",
    "token",
    "credential",
    "api_key",
    "apikey",
    "private_key",
    "gumroad_api",
    "stripe",
    "discord_token",
    "youtube_token",
    "settings.local.json",
]

BINARY_SUFFIXES = {
    ".zip",
    ".exe",
    ".apk",
    ".png",
    ".jpg",
    ".jpeg",
    ".webp",
    ".gif",
    ".mp3",
    ".wav",
    ".onnx",
    ".pyd",
    ".dll",
    ".so",
    ".dylib",
    ".pdb",
    ".pack",
    ".pyc",
    ".o",
    ".rlib",
}


def rel(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT.resolve()).as_posix()
    except ValueError:
        return path.resolve().as_posix()


def norm(path: Path) -> str:
    return "/" + rel(path).replace("\\", "/").lower().lstrip("/")


def is_denied(path: Path) -> bool:
    value = norm(path)
    return any(marker in value for marker in DENY_SUBSTRINGS)


def is_private_game(path: Path) -> bool:
    value = norm(path)
    return any(marker in value for marker in PRIVATE_GAME_SUBSTRINGS)


def is_secret_named(path: Path) -> bool:
    value = path.name.lower()
    full = norm(path)
    return any(marker in value or marker in full for marker in SECRET_NAME_MARKERS)


def iter_files(include_denied: bool = False) -> Iterable[Path]:
    for base, dirs, files in os.walk(ROOT):
        base_path = Path(base)
        kept_dirs = []
        for name in dirs:
            d = base_path / name
            if include_denied or not is_denied(d):
                kept_dirs.append(name)
        dirs[:] = kept_dirs
        for name in files:
            p = base_path / name
            if include_denied or not is_denied(p):
                yield p


def sha256_file(path: Path, chunk_size: int = 1024 * 1024) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(chunk_size), b""):
            h.update(chunk)
    return h.hexdigest()


def print_json(data: object) -> None:
    print(json.dumps(data, indent=2, ensure_ascii=True))


def ensure_under_root(path: Path) -> Path:
    resolved = path.resolve()
    root = ROOT.resolve()
    if root not in (resolved, *resolved.parents):
        raise ValueError(f"path escapes root: {resolved}")
    return resolved


def run_command(command: list[str], cwd: Path, execute: bool) -> dict[str, object]:
    if not execute:
        return {"cwd": rel(cwd), "command": command, "executed": False}
    resolved = list(command)
    executable = shutil.which(resolved[0])
    if executable:
        resolved[0] = executable
    try:
        result = subprocess.run(resolved, cwd=cwd, text=True, capture_output=True)
    except FileNotFoundError as exc:
        return {
            "cwd": rel(cwd),
            "command": command,
            "executed": False,
            "returncode": 127,
            "error": str(exc),
        }
    return {
        "cwd": rel(cwd),
        "command": command,
        "executed": True,
        "returncode": result.returncode,
        "stdout_tail": result.stdout.splitlines()[-20:],
        "stderr_tail": result.stderr.splitlines()[-20:],
    }


@dataclass(frozen=True)
class Product:
    name: str
    classification: str
    source: str
    lane: str
    include: tuple[str, ...]
    notes: str

    @property
    def source_path(self) -> Path:
        return ROOT / self.source


PRODUCTS = [
    Product(
        name="residueos",
        classification="OPEN",
        source="packages/open-dev/residueos",
        lane="free-dev",
        include=("packages/open-dev/residueos",),
        notes="MIT local AI action gate MVP; thresholds remain DEMO_ONLY until calibrated with real data.",
    ),
    Product(
        name="obsai-core",
        classification="OPEN",
        source="packages/open-dev/obsai-core",
        lane="free-dev",
        include=("packages/open-dev/obsai-core",),
        notes="MIT dependency-free operational core; no research or consciousness product claims.",
    ),
    Product(
        name="observacionismo-gate",
        classification="OPEN",
        source="packages/open-dev/observacionismo-gate",
        lane="free-dev",
        include=("packages/open-dev/observacionismo-gate",),
        notes="MIT SDK candidate extracted from Claudio without runtime state.",
    ),
    Product(
        name="claudio-os-blueprint",
        classification="OPEN",
        source="packages/open-dev/claudio-os-blueprint",
        lane="free-dev",
        include=("packages/open-dev/claudio-os-blueprint",),
        notes="Blueprint only; do not claim finished ISO.",
    ),
    Product(
        name="gemma-observacionismo-cleanup",
        classification="OPEN",
        source="packages/open-dev/gemma-observacionismo-cleanup",
        lane="free-dev",
        include=("packages/open-dev/gemma-observacionismo-cleanup",),
        notes="MIT cleanup/observation toolkit with synthetic fixtures only; no weights, prompts or Claudio runtime.",
    ),
    Product(
        name="argus-desktop",
        classification="COMMERCIAL_OR_INTERNAL",
        source="apps/commercial/argus-desktop",
        lane="paid-apps",
        include=("apps/commercial/argus-desktop",),
        notes="Commercial/internal desktop app; generated artifacts denied.",
    ),
    Product(
        name="asistente-negocio",
        classification="COMMERCIAL",
        source="apps/commercial/asistente-negocio",
        lane="paid-apps",
        include=("apps/commercial/asistente-negocio",),
        notes="Commercial app candidate.",
    ),
    Product(
        name="flujocrm",
        classification="COMMERCIAL",
        source="apps/commercial/flujocrm",
        lane="paid-apps",
        include=("apps/commercial/flujocrm",),
        notes="Commercial app candidate.",
    ),
    Product(
        name="mini-office",
        classification="COMMERCIAL",
        source="apps/commercial/mini-office",
        lane="paid-apps",
        include=("apps/commercial/mini-office",),
        notes="Needs real smoke tests before release.",
    ),
]


def collect_product_files(product: Product) -> tuple[list[Path], list[tuple[str, str]], list[tuple[str, str]]]:
    allowed: list[Path] = []
    blocked: list[tuple[str, str]] = []
    excluded: list[tuple[str, str]] = []
    for include in product.include:
        base = ROOT / include
        if not base.exists():
            blocked.append((include, "missing"))
            continue
        for root, dirs, files in os.walk(base):
            root_path = Path(root)
            kept_dirs = []
            for name in dirs:
                path = root_path / name
                if is_private_game(path):
                    blocked.append((rel(path), "private_game"))
                elif is_denied(path):
                    excluded.append((rel(path), "denylist"))
                elif is_secret_named(path):
                    blocked.append((rel(path), "secret_like_name"))
                else:
                    kept_dirs.append(name)
            dirs[:] = kept_dirs
            for name in files:
                path = root_path / name
                if is_private_game(path):
                    blocked.append((rel(path), "private_game"))
                elif is_denied(path):
                    excluded.append((rel(path), "denylist"))
                elif is_secret_named(path):
                    blocked.append((rel(path), "secret_like_name"))
                else:
                    allowed.append(path)
    return allowed, blocked, excluded


def product_by_name(name: str) -> Product:
    for product in PRODUCTS:
        if product.name == name:
            return product
    raise SystemExit(f"unknown product: {name}")


def add_common_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--root", default=str(ROOT), help="workspace root; scripts are designed for the current root")


def validate_root_arg(args: argparse.Namespace) -> None:
    if Path(args.root).resolve() != ROOT.resolve():
        raise SystemExit(f"this tool is pinned to {ROOT}; got {args.root}")
