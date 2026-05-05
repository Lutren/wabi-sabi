from __future__ import annotations

import argparse
import json
import os
import shutil
from datetime import datetime, timezone
from pathlib import Path

from _common import ROOT, print_json


TODAY = "2026-05-05"
ALLOWED_CACHE_DIRS = {"__pycache__", ".pytest_cache", ".ruff_cache", ".mypy_cache"}
EXCLUDE_PARTS = {
    ".git",
    "node_modules",
    ".venv",
    "venv",
    "env",
    "_archive",
    "_ARCHIVAR",
    ".skills",
    "tools\\vendor",
    "tools/vendor",
    "github-modules",
    "releases",
    "release",
}
PRIVATE_MARKERS = {
    "metaevo-tcg",
    "\\tcg\\",
    "/tcg/",
    "runtime\\game_bridge",
    "runtime/game_bridge",
    "game-private",
    "04_AUDIOVISUAL_Y_TCG",
}


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def norm(path: Path) -> str:
    return str(path.resolve()).replace("\\", "/")


def rel(path: Path) -> str:
    try:
        return str(path.resolve().relative_to(ROOT.resolve())).replace("\\", "/")
    except ValueError:
        return norm(path)


def ensure_safe_target(path: Path) -> Path:
    resolved = path.resolve()
    root = ROOT.resolve()
    if resolved == root or root not in resolved.parents:
        raise ValueError(f"path escapes workspace root: {resolved}")
    if resolved.name not in ALLOWED_CACHE_DIRS:
        raise ValueError(f"not an approved cache dir: {resolved}")
    lowered = str(resolved).lower().replace("\\", "/")
    if any(marker.lower().replace("\\", "/") in lowered for marker in PRIVATE_MARKERS):
        raise ValueError(f"private boundary target blocked: {resolved}")
    return resolved


def should_skip_dir(path: Path) -> bool:
    lowered = str(path).lower().replace("\\", "/")
    if "/tools/release" in lowered:
        return any(marker.lower().replace("\\", "/") in lowered for marker in PRIVATE_MARKERS)
    if any(part.lower().replace("\\", "/") in lowered for part in EXCLUDE_PARTS):
        return True
    return any(marker.lower().replace("\\", "/") in lowered for marker in PRIVATE_MARKERS)


def dir_size(path: Path) -> tuple[int, int]:
    files = 0
    bytes_total = 0
    for item in path.rglob("*"):
        if not item.is_file():
            continue
        try:
            files += 1
            bytes_total += item.stat().st_size
        except OSError:
            continue
    return files, bytes_total


def discover() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for base_text, dirs, _files in os.walk(ROOT, topdown=True):
        base = Path(base_text)
        kept_dirs: list[str] = []
        for name in dirs:
            path = base / name
            if name in ALLOWED_CACHE_DIRS:
                if should_skip_dir(path):
                    rows.append(
                        {
                            "path": rel(path),
                            "absolute_path": norm(path),
                            "cache_type": name,
                            "action_gate": "BLOCK",
                            "decision": "KEEP_BLOCKED_BOUNDARY",
                            "reason": "excluded boundary",
                            "file_count": 0,
                            "bytes": 0,
                        }
                    )
                else:
                    files, bytes_total = dir_size(path)
                    rows.append(
                        {
                            "path": rel(path),
                            "absolute_path": norm(path),
                            "cache_type": name,
                            "action_gate": "APPROVE",
                            "decision": "DELETE_APPROVED_REGENERABLE_CACHE",
                            "reason": "approved cache dir name under workspace root",
                            "file_count": files,
                            "bytes": bytes_total,
                        }
                    )
                continue
            if should_skip_dir(path):
                continue
            kept_dirs.append(name)
        dirs[:] = kept_dirs
    return sorted(rows, key=lambda row: str(row["path"]).lower())


def write_json(path: Path, data: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Dry-run or delete approved regenerable cache directories.")
    parser.add_argument("--execute", action="store_true")
    parser.add_argument("--json-out", default="")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    rows = discover()
    approved = [row for row in rows if row["action_gate"] == "APPROVE"]
    blocked = [row for row in rows if row["action_gate"] == "BLOCK"]
    deleted: list[dict[str, object]] = []
    errors: list[dict[str, object]] = []

    if args.execute:
        for row in approved:
            target = Path(str(row["absolute_path"]))
            try:
                safe = ensure_safe_target(target)
                shutil.rmtree(safe)
                deleted.append(row)
            except Exception as exc:  # noqa: BLE001 - cleanup report must record every failure.
                errors.append({"path": row["path"], "error": f"{exc.__class__.__name__}: {exc}"})

    data = {
        "generated_at_utc": utc_now(),
        "status": "EXECUTED" if args.execute else "DRY_RUN",
        "workspace_root": str(ROOT),
        "allowed_cache_dirs": sorted(ALLOWED_CACHE_DIRS),
        "excluded_boundaries": sorted(EXCLUDE_PARTS | PRIVATE_MARKERS),
        "summary": {
            "total_candidates": len(rows),
            "approved_count": len(approved),
            "blocked_count": len(blocked),
            "approved_bytes": sum(int(row["bytes"]) for row in approved),
            "approved_files": sum(int(row["file_count"]) for row in approved),
            "deleted_count": len(deleted),
            "deleted_bytes": sum(int(row["bytes"]) for row in deleted),
            "deleted_files": sum(int(row["file_count"]) for row in deleted),
            "errors": len(errors),
        },
        "approved": approved,
        "blocked": blocked,
        "deleted": deleted,
        "errors": errors,
        "rules": [
            "Only approved cache directory names are eligible.",
            "Private, archive, vendor, release, env, node_modules and git paths are excluded.",
            "No files outside the workspace root can be deleted.",
        ],
    }

    default_name = "seto-cache-cleanup-result" if args.execute else "seto-cache-cleanup-dry-run"
    output = Path(args.json_out) if args.json_out else ROOT / "qa_artifacts" / "release_validation" / f"{default_name}-{TODAY}.json"
    write_json(output, data)

    if args.json:
        print_json(data)
    else:
        print(f"status={data['status']}")
        print(f"approved={data['summary']['approved_count']} blocked={data['summary']['blocked_count']} bytes={data['summary']['approved_bytes']}")
        print(f"deleted={data['summary']['deleted_count']} errors={data['summary']['errors']}")
        print(f"json={output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
