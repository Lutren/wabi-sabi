from __future__ import annotations

import datetime as dt
import os
import platform
import subprocess
import sys
from pathlib import Path


SKIP_DIRS = {
    ".git",
    ".venv",
    ".venv_api",
    "__pycache__",
    "node_modules",
    "target",
    "dist",
    "build",
    "release",
    "releases",
    "_archive",
    "_ARCHIVAR",
    "archive",
}


def stamp() -> str:
    return dt.datetime.now().strftime("%Y%m%d-%H%M%S")


def write_artifact(output_dir: Path, prefix: str, suffix: str, text: str) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    safe_prefix = "".join(ch if ch.isalnum() or ch in "-_" else "_" for ch in prefix).strip("_")
    path = output_dir / f"{safe_prefix}_{stamp()}{suffix}"
    path.write_text(text, encoding="utf-8")
    return path


def discover_project(workspace: Path, max_files: int = 300) -> dict:
    files: list[str] = []
    markers: list[str] = []
    marker_names = {
        "README.md",
        "AGENTS.md",
        "package.json",
        "pyproject.toml",
        "requirements.txt",
        "setup.py",
        "Cargo.toml",
        "Makefile",
    }
    for root, dirs, names in os.walk(workspace):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS and not d.startswith(".pytest_cache")]
        root_path = Path(root)
        for name in names:
            rel = str((root_path / name).relative_to(workspace))
            if name in marker_names:
                markers.append(rel)
            if len(files) < max_files:
                files.append(rel)
        if len(files) >= max_files and markers:
            break
    return {
        "workspace": str(workspace),
        "file_sample_count": len(files),
        "files_sample": files,
        "markers": sorted(markers),
    }


def safe_command_snapshot() -> dict:
    return {
        "python": sys.version.split()[0],
        "executable": sys.executable,
        "platform": platform.platform(),
    }


def run_short_command(args: list[str], cwd: Path, timeout: int = 20) -> dict:
    proc = subprocess.run(args, cwd=str(cwd), capture_output=True, text=True, timeout=timeout)
    return {
        "args": args,
        "returncode": proc.returncode,
        "stdout": proc.stdout[-4000:],
        "stderr": proc.stderr[-4000:],
    }


def read_text_sample(path: Path, max_chars: int = 8000) -> str:
    return path.read_text(encoding="utf-8", errors="replace")[:max_chars]
