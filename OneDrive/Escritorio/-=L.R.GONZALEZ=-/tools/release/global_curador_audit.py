from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import re
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

from _common import ROOT, print_json, sha256_file


TODAY = "2026-05-05"
DEFAULT_HASH_MAX_MB = 50
DEFAULT_DUPLICATE_LIMIT = 80
DEFAULT_LARGE_LIMIT = 80
DEFAULT_STATE_OUT = ROOT / "runtime" / "curador_seto" / "global_curador_audit_state.json"

GENERATED_DIR_NAMES = {
    ".git",
    ".hg",
    ".svn",
    "node_modules",
    ".venv",
    "venv",
    "env",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    ".cache",
    "target",
    "dist",
    "build",
    "release",
    "releases",
    ".next",
    ".nuxt",
    ".parcel-cache",
    ".gradle",
    ".godot",
    ".import",
    "bin",
    "obj",
    "DerivedData",
    "Library",
    "Temp",
}

GENERATED_FILE_SUFFIXES = {
    ".pyc",
    ".pyo",
    ".o",
    ".obj",
    ".log",
    ".tmp",
    ".temp",
    ".cache",
    ".tsbuildinfo",
}

PROJECT_MARKERS = {
    "package.json",
    "pyproject.toml",
    "setup.py",
    "requirements.txt",
    "Cargo.toml",
    "go.mod",
    "pytest.ini",
    "vite.config.js",
    "vite.config.ts",
}

TEXTUAL_SUFFIXES = {".md", ".txt", ".py", ".json", ".csv", ".html", ".js", ".ts", ".css", ".yml", ".yaml"}
ZIP_SUFFIXES = {".zip", ".7z", ".rar", ".tar", ".gz"}
SECRET_MARKERS = {
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
}
ROOT_ABS = os.path.abspath(str(ROOT)).lower().replace("\\", "/")


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def is_under(path: Path, parent: Path) -> bool:
    try:
        resolved = path.resolve()
        root = parent.resolve()
    except OSError:
        return False
    return resolved == root or root in resolved.parents


def safe_resolve(path: Path) -> str:
    return os.path.abspath(str(path))


def norm_abs(path: Path | str) -> str:
    return os.path.abspath(str(path)).lower().replace("\\", "/")


def is_under_norm(child_abs: str, parent_abs: str) -> bool:
    parent = parent_abs.rstrip("/")
    return child_abs == parent or child_abs.startswith(parent + "/")


def rel_to_root(path: Path) -> str:
    path_abs = os.path.abspath(str(path)).lower().replace("\\", "/")
    if is_under_norm(path_abs, ROOT_ABS):
        return os.path.relpath(os.path.abspath(str(path)), os.path.abspath(str(ROOT)))
    return safe_resolve(path)


def is_secret_like_name(path: Path) -> bool:
    name = path.name.lower()
    full = safe_resolve(path).lower().replace("\\", "/")
    return any(marker in name or marker in full for marker in SECRET_MARKERS)


def path_flags(path: Path, size: int | None = None) -> list[str]:
    flags: list[str] = []
    name = path.name.lower()
    suffix = path.suffix.lower()
    if is_secret_like_name(path):
        flags.append("secret_like_name")
    if is_private_boundary(path):
        flags.append("private_game_boundary")
    if suffix in ZIP_SUFFIXES:
        flags.append("package_or_archive")
    if suffix in GENERATED_FILE_SUFFIXES or name in {"tmp.json", "debug.log"}:
        flags.append("generated_or_log_candidate")
    if size is not None and size == 0:
        flags.append("empty_file")
    if size is not None and size >= 50 * 1024 * 1024:
        flags.append("large_file")
    return flags


def gate_for_flags(flags: Iterable[str], *, has_hash: bool = False) -> str:
    values = set(flags)
    if values & {"secret_like_name", "private_game_boundary"}:
        return "BLOCK"
    if "package_or_archive" in values:
        return "REVIEW"
    if "generated_or_log_candidate" in values and has_hash:
        return "REVIEW"
    return "REVIEW"


def decision_for_flags(flags: Iterable[str]) -> str:
    values = set(flags)
    if values & {"secret_like_name", "private_game_boundary"}:
        return "KEEP_BLOCKED_BOUNDARY"
    if "generated_or_log_candidate" in values:
        return "CANDIDATE_DELETE_REGENERABLE_REVIEW"
    if "package_or_archive" in values:
        return "CANDIDATE_ARCHIVE_OR_LINEAGE_REVIEW"
    if "empty_file" in values:
        return "CANDIDATE_DELETE_EMPTY_REVIEW"
    return "KEEP_OR_REVIEW"


def generated_dir_record(path: Path, root_label: str) -> dict[str, object]:
    name = path.name.lower()
    classification = classify_root(path)
    if name == ".git":
        decision = "KEEP_BLOCKED_GIT_HISTORY"
        gate = "BLOCK"
    elif name in {"env", "venv", ".venv"}:
        decision = "REVIEW_ENV_DIR_SECRET_AND_REGENERABILITY"
        gate = "REVIEW"
        classification = "ENVIRONMENT_DIR_REVIEW"
    elif name in {"release", "releases"}:
        decision = "CANDIDATE_ARCHIVE_OR_LINEAGE_REVIEW"
        gate = "REVIEW"
        classification = "RELEASE_EVIDENCE_REVIEW"
    elif name == "bin":
        decision = "REVIEW_BINARY_OR_TOOL_DIR"
        gate = "REVIEW"
        classification = "BINARY_TOOL_DIR_REVIEW"
    elif is_private_boundary(path):
        decision = "KEEP_BLOCKED_BOUNDARY"
        gate = "BLOCK"
    else:
        decision = "CANDIDATE_DELETE_REGENERABLE_REVIEW"
        gate = "REVIEW"
    return {
        "path": safe_resolve(path),
        "root": root_label,
        "classification": classification,
        "decision": decision,
        "action_gate": gate,
    }


def normalized_version_key(path: Path) -> str:
    stem = path.stem.lower()
    stem = re.sub(r"\s*\(\d+\)$", "", stem)
    stem = re.sub(r"\s*-\s*copy$", "", stem)
    stem = re.sub(r"\s+copy$", "", stem)
    stem = re.sub(r"\s+copia$", "", stem)
    stem = re.sub(r"[_\-\s]+", " ", stem).strip()
    return f"{stem}{path.suffix.lower()}"


def read_registry_texts() -> str:
    registry_names = [
        "SOURCE_INTAKE_REGISTER.md",
        "source_intake_register.json",
        "PRODUCT_MAP.md",
        "VISIBILITY_MATRIX.md",
        "RISK_REGISTER.md",
        "DUPLICATES_AND_DEAD_CODE.md",
        "DELETE_CANDIDATES.md",
        "MIGRATION_MAP.md",
        "DELETED_OR_ARCHIVED.md",
    ]
    chunks: list[str] = []
    for name in registry_names:
        path = ROOT / name
        if not path.exists():
            continue
        try:
            chunks.append(path.read_text(encoding="utf-8", errors="ignore").lower())
        except OSError:
            continue
    return "\n".join(chunks)


def is_registered(path: Path, registry_blob: str) -> bool:
    tokens = {path.name.lower(), safe_resolve(path).lower().replace("\\", "/"), rel_to_root(path).lower().replace("\\", "/")}
    return any(token and token in registry_blob for token in tokens)


def default_roots() -> list[dict[str, object]]:
    desktop = Path.home() / "OneDrive" / "Escritorio"
    downloads = Path.home() / "Downloads"
    return [
        {"label": "workspace_lrgonzalez", "path": ROOT, "exclude": []},
        {"label": "downloads", "path": downloads, "exclude": []},
        {"label": "desktop_other", "path": desktop, "exclude": [ROOT]},
        {"label": "e_drive", "path": Path("E:/"), "exclude": []},
    ]


def selected_root_defs(
    root_labels: set[str] | None = None,
    root_defs: list[dict[str, object]] | None = None,
) -> list[dict[str, object]]:
    roots = list(root_defs if root_defs is not None else default_roots())
    if not root_labels:
        return roots
    requested = {label.lower() for label in root_labels}
    selected = [item for item in roots if str(item["label"]).lower() in requested]
    found = {str(item["label"]).lower() for item in selected}
    missing = sorted(requested - found)
    if missing:
        available = ", ".join(str(item["label"]) for item in roots)
        raise ValueError(f"unknown root label(s): {', '.join(missing)}; available: {available}")
    return selected


def normalize_resume_marker(value: str | None) -> str:
    if not value:
        return ""
    path = Path(value)
    if not path.is_absolute():
        path = ROOT / path
    return norm_abs(path)


def should_skip_dir(path: Path) -> bool:
    return path.name in GENERATED_DIR_NAMES


def classify_root(path: Path) -> str:
    text = safe_resolve(path).lower().replace("\\", "/")
    if "/metaevo-tcg" in text or "medioevo_rpg" in text or "/tcg" in text:
        return "PRIVATE_BOUNDARY"
    if "downloads" in text:
        return "SOURCE_INTAKE_REVIEW"
    if "node_modules" in text or "target" in text or "__pycache__" in text:
        return "GENERATED_RESIDUE"
    if "website" in text:
        return "PUBLIC_SURFACE_REVIEW"
    if "packages/open-dev" in text:
        return "OPEN_DEV"
    if "apps/commercial" in text or "productos_medioevo" in text:
        return "COMMERCIAL_REVIEW"
    return "UNKNOWN_REVIEW_REQUIRED"


def is_private_boundary(path: Path) -> bool:
    text = safe_resolve(path).lower().replace("\\", "/")
    return (
        "e:/medioevo_rpg" in text
        or "e:/medioevo_assets" in text
        or "/-=medioevo=-/-=libros/metaevo-tcg/" in text
        or "/-=medioevo=-/-=libros/claudio/tcg/" in text
        or "/productos_medioevo/04_audiovisual_y_tcg/" in text
        or "/metaevo-tcg" in text
        or "/tcg" in text
        or "/runtime/game_bridge" in text
    )


def scan_roots(
    hash_max_bytes: int,
    registry_blob: str,
    *,
    root_labels: set[str] | None = None,
    max_files: int | None = None,
    start_after: str | None = None,
    root_defs: list[dict[str, object]] | None = None,
) -> dict[str, object]:
    rows: list[dict[str, object]] = []
    generated_dirs: list[dict[str, object]] = []
    project_roots: dict[str, dict[str, object]] = {}
    errors: list[dict[str, str]] = []
    root_stats: dict[str, dict[str, object]] = {}
    seen_files: set[str] = set()
    seen_dirs: set[str] = set()
    selected_roots = selected_root_defs(root_labels, root_defs)
    start_after_abs = normalize_resume_marker(start_after)
    resume_found = not bool(start_after_abs)
    processed_files = 0
    limit_reached = False
    resume = {
        "truncated": False,
        "max_files": max_files or 0,
        "start_after": start_after or "",
        "start_after_found": resume_found,
        "last_path": "",
        "next_start_after": "",
        "processed_files": 0,
        "root_labels": [str(item["label"]) for item in selected_roots],
    }

    focus_psi = ROOT / "-=MEDIOEVO=-" / "-=LIBROS" / "-=CEREBRO=-" / "-=PSI=-"
    focus_paths = {
        "psi": focus_psi,
        "downloads": Path.home() / "Downloads",
        "desktop": Path.home() / "OneDrive" / "Escritorio",
        "workspace": ROOT,
        "e_drive": Path("E:/"),
    }
    focus_abs = {name: norm_abs(path) for name, path in focus_paths.items()}
    focus_stats = {name: {"files": 0, "bytes": 0, "hashed": 0} for name in focus_paths}

    for root_def in selected_roots:
        label = str(root_def["label"])
        root = Path(root_def["path"])
        excludes = [Path(item) for item in root_def["exclude"]]  # type: ignore[arg-type]
        exclude_abs = [norm_abs(item) for item in excludes]
        root_stats[label] = {
            "path": safe_resolve(root),
            "exists": root.exists(),
            "files": 0,
            "dirs": 0,
            "bytes": 0,
            "hashed": 0,
            "hash_skipped": 0,
            "generated_dirs_skipped": 0,
            "errors": 0,
        }
        if not root.exists():
            continue

        for current, dir_names, file_names in os.walk(root, topdown=True, followlinks=False):
            if limit_reached:
                break
            current_path = Path(current)
            current_resolved = safe_resolve(current_path)
            if current_resolved in seen_dirs:
                dir_names[:] = []
                continue
            seen_dirs.add(current_resolved)

            current_abs = norm_abs(current_path)
            if any(is_under_norm(current_abs, excluded) for excluded in exclude_abs):
                dir_names[:] = []
                continue

            root_stats[label]["dirs"] = int(root_stats[label]["dirs"]) + 1

            kept_dirs: list[str] = []
            for dir_name in sorted(dir_names, key=str.lower):
                child = current_path / dir_name
                if should_skip_dir(child):
                    generated_dirs.append(generated_dir_record(child, label))
                    root_stats[label]["generated_dirs_skipped"] = int(root_stats[label]["generated_dirs_skipped"]) + 1
                    continue
                kept_dirs.append(dir_name)
            dir_names[:] = kept_dirs

            marker_hits = sorted(set(file_names) & PROJECT_MARKERS)
            if marker_hits:
                project_roots[safe_resolve(current_path)] = {
                    "path": safe_resolve(current_path),
                    "root": label,
                    "markers": marker_hits,
                    "classification": classify_root(current_path),
                    "registered": is_registered(current_path, registry_blob),
                }

            for file_name in sorted(file_names, key=str.lower):
                path = current_path / file_name
                resolved = safe_resolve(path)
                if resolved in seen_files:
                    continue
                seen_files.add(resolved)
                if not resume_found:
                    if norm_abs(resolved) == start_after_abs:
                        resume_found = True
                        resume["start_after_found"] = True
                    continue

                try:
                    stat = path.stat()
                    size = int(stat.st_size)
                except OSError as exc:
                    errors.append({"path": resolved, "error": str(exc)})
                    root_stats[label]["errors"] = int(root_stats[label]["errors"]) + 1
                    continue

                flags = path_flags(path, size)
                sha = ""
                if size <= hash_max_bytes and "secret_like_name" not in flags and "private_game_boundary" not in flags:
                    hash_status = "pending_candidate"
                else:
                    hash_status = "skipped_secret_or_private" if {"secret_like_name", "private_game_boundary"} & set(flags) else "skipped_large"
                    root_stats[label]["hash_skipped"] = int(root_stats[label]["hash_skipped"]) + 1

                registered = is_registered(path, registry_blob)
                row = {
                    "root": label,
                    "path": resolved,
                    "rel_to_workspace": rel_to_root(path),
                    "name": path.name,
                    "extension": path.suffix.lower(),
                    "size_bytes": size,
                    "sha256": sha,
                    "hash_status": hash_status,
                    "flags": "|".join(flags),
                    "registered": "yes" if registered else "no",
                    "psi_state": "BLOQUEADO" if {"secret_like_name", "private_game_boundary"} & set(flags) else "INFERENCIA",
                    "action_gate": gate_for_flags(flags, has_hash=bool(sha)),
                    "decision": decision_for_flags(flags),
                }
                rows.append(row)
                processed_files += 1
                resume["processed_files"] = processed_files
                resume["last_path"] = resolved
                root_stats[label]["files"] = int(root_stats[label]["files"]) + 1
                root_stats[label]["bytes"] = int(root_stats[label]["bytes"]) + size

                resolved_abs = norm_abs(resolved)
                for focus_name, focus_path_abs in focus_abs.items():
                    if is_under_norm(resolved_abs, focus_path_abs):
                        focus_stats[focus_name]["files"] += 1
                        focus_stats[focus_name]["bytes"] += size
                if max_files and processed_files >= max_files:
                    resume["truncated"] = True
                    resume["next_start_after"] = resolved
                    limit_reached = True
                    dir_names[:] = []
                    break

    hash_candidate_rows(rows, root_stats, focus_stats, focus_abs, hash_max_bytes, errors)

    return {
        "rows": rows,
        "generated_dirs": generated_dirs,
        "project_roots": sorted(project_roots.values(), key=lambda item: str(item["path"]).lower()),
        "errors": errors,
        "root_stats": root_stats,
        "focus_stats": focus_stats,
        "selected_roots": selected_roots,
        "resume": resume,
    }


def hash_candidate_rows(
    rows: list[dict[str, object]],
    root_stats: dict[str, dict[str, object]],
    focus_stats: dict[str, dict[str, int]],
    focus_abs: dict[str, str],
    hash_max_bytes: int,
    errors: list[dict[str, str]],
) -> None:
    by_size: dict[int, list[dict[str, object]]] = defaultdict(list)
    for row in rows:
        if row["hash_status"] != "pending_candidate":
            continue
        size = int(row["size_bytes"])
        if size <= 0 or size > hash_max_bytes:
            row["hash_status"] = "skipped_empty_or_large"
            continue
        by_size[size].append(row)

    for group in by_size.values():
        for row in group:
            path_text = str(row["path"])
            path_abs = norm_abs(path_text)
            priority = (
                len(group) > 1
                or row["root"] == "downloads"
                or str(row["extension"]) in ZIP_SUFFIXES
                or is_under_norm(path_abs, focus_abs["psi"])
            )
            if not priority:
                row["hash_status"] = "skipped_unique_size"
                continue
            try:
                row["sha256"] = sha256_file(Path(path_text))
                row["hash_status"] = "hashed"
                row["psi_state"] = "CERTEZA"
                root_label = str(row["root"])
                if root_label in root_stats:
                    root_stats[root_label]["hashed"] = int(root_stats[root_label]["hashed"]) + 1
                for focus_name, focus_path_abs in focus_abs.items():
                    if is_under_norm(path_abs, focus_path_abs):
                        focus_stats[focus_name]["hashed"] += 1
            except OSError as exc:
                row["hash_status"] = f"hash_error:{exc.__class__.__name__}"
                errors.append({"path": path_text, "error": str(exc)})


def summarize(rows: list[dict[str, object]], generated_dirs: list[dict[str, object]], project_roots: list[dict[str, object]], errors: list[dict[str, str]], duplicate_limit: int, large_limit: int) -> dict[str, object]:
    by_hash: dict[tuple[int, str], list[dict[str, object]]] = defaultdict(list)
    by_version: dict[str, list[dict[str, object]]] = defaultdict(list)
    ext_counts: Counter[str] = Counter()
    decision_counts: Counter[str] = Counter()
    gate_counts: Counter[str] = Counter()
    flag_counts: Counter[str] = Counter()
    unregistered_review: list[dict[str, object]] = []

    for row in rows:
        ext_counts[str(row["extension"]) or "[none]"] += 1
        decision_counts[str(row["decision"])] += 1
        gate_counts[str(row["action_gate"])] += 1
        for flag in str(row["flags"]).split("|"):
            if flag:
                flag_counts[flag] += 1
        sha = str(row["sha256"])
        if sha:
            by_hash[(int(row["size_bytes"]), sha)].append(row)
        key = normalized_version_key(Path(str(row["path"])))
        if key:
            by_version[key].append(row)
        if row["registered"] == "no" and (row["extension"] in ZIP_SUFFIXES or row["root"] == "downloads" or row["decision"] != "KEEP_OR_REVIEW"):
            unregistered_review.append(row)

    exact_duplicates = []
    for (size, sha), group in by_hash.items():
        if len(group) < 2:
            continue
        private_or_secret = any("private_game_boundary" in str(item["flags"]) or "secret_like_name" in str(item["flags"]) for item in group)
        exact_duplicates.append(
            {
                "sha256": sha,
                "size_bytes": size,
                "count": len(group),
                "total_duplicate_bytes_if_one_kept": size * (len(group) - 1),
                "action_gate": "BLOCK" if private_or_secret else "REVIEW",
                "decision": "CANDIDATE_DELETE_EXACT_DUPLICATE_REVIEW" if not private_or_secret else "KEEP_BLOCKED_BOUNDARY",
                "examples": [str(item["path"]) for item in group[:8]],
            }
        )
    exact_duplicates.sort(key=lambda item: (int(item["total_duplicate_bytes_if_one_kept"]), int(item["count"])), reverse=True)

    version_collisions = []
    for key, group in by_version.items():
        if len(group) < 2:
            continue
        unique_hashes = sorted({str(item["sha256"]) for item in group if str(item["sha256"])})
        if len(unique_hashes) <= 1 and unique_hashes:
            continue
        version_collisions.append(
            {
                "key": key,
                "count": len(group),
                "unique_hashes": len(unique_hashes),
                "action_gate": "REVIEW",
                "decision": "MERGE_OR_VERSION_REVIEW",
                "examples": [str(item["path"]) for item in group[:8]],
            }
        )
    version_collisions.sort(key=lambda item: int(item["count"]), reverse=True)

    large_files = sorted(rows, key=lambda row: int(row["size_bytes"]), reverse=True)[:large_limit]
    zip_files = [row for row in rows if str(row["extension"]) in ZIP_SUFFIXES]
    zip_files.sort(key=lambda row: int(row["size_bytes"]), reverse=True)

    delete_candidates = []
    for item in generated_dirs[:200]:
        delete_candidates.append(item)
    for row in rows:
        if row["decision"] in {"CANDIDATE_DELETE_REGENERABLE_REVIEW", "CANDIDATE_DELETE_EMPTY_REVIEW"}:
            delete_candidates.append(
                {
                    "path": row["path"],
                    "root": row["root"],
                    "classification": "GENERATED_OR_EMPTY_REVIEW",
                    "size_bytes": row["size_bytes"],
                    "sha256": row["sha256"],
                    "decision": row["decision"],
                    "action_gate": row["action_gate"],
                }
            )
        if len(delete_candidates) >= 300:
            break

    return {
        "counts": {
            "files": len(rows),
            "generated_dirs_recorded": len(generated_dirs),
            "project_roots_detected": len(project_roots),
            "errors": len(errors),
            "hashed_files": sum(1 for row in rows if row["sha256"]),
            "zip_or_archive_files": len(zip_files),
            "exact_duplicate_groups": len(exact_duplicates),
            "version_review_groups": len(version_collisions),
        },
        "extension_counts_top": ext_counts.most_common(25),
        "decision_counts": decision_counts.most_common(),
        "gate_counts": gate_counts.most_common(),
        "flag_counts": flag_counts.most_common(),
        "exact_duplicates": exact_duplicates[:duplicate_limit],
        "version_collisions": version_collisions[:duplicate_limit],
        "large_files": large_files,
        "zip_files": zip_files[:large_limit],
        "unregistered_review_sample": unregistered_review[:120],
        "delete_candidates_sample": delete_candidates,
    }


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    columns = [
        "root",
        "path",
        "rel_to_workspace",
        "name",
        "extension",
        "size_bytes",
        "sha256",
        "hash_status",
        "flags",
        "registered",
        "psi_state",
        "action_gate",
        "decision",
    ]
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=columns)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: row.get(key, "") for key in columns})


def write_json(path: Path, data: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")


def incremental_suffix(root_labels: set[str], max_files: int | None, start_after: str | None) -> str:
    if not root_labels and not max_files and not start_after:
        return ""
    label_text = "-".join(sorted(root_labels)) if root_labels else "selected"
    parts = [label_text]
    if max_files:
        parts.append(f"max{max_files}")
    if start_after:
        marker_hash = hashlib.sha256(start_after.encode("utf-8", errors="ignore")).hexdigest()[:10]
        parts.append(f"resume{marker_hash}")
    clean = re.sub(r"[^A-Za-z0-9_-]+", "_", "_".join(parts)).strip("_")
    return f"-{clean}" if clean else "-incremental"


def default_output_paths(root_labels: set[str], max_files: int | None, start_after: str | None) -> tuple[Path, Path, Path]:
    suffix = incremental_suffix(root_labels, max_files, start_after)
    json_path = ROOT / "qa_artifacts" / "release_validation" / f"global-curador-seto-audit-{TODAY}{suffix}.json"
    csv_path = ROOT / "qa_artifacts" / "release_validation" / f"global-curador-file-manifest-{TODAY}{suffix}.csv"
    report_suffix = suffix.replace("-", "_").upper()
    report_path = ROOT / "docs" / "intake" / f"GLOBAL_CURADOR_SETO_AUDIT_{TODAY}{report_suffix}.md"
    return json_path, csv_path, report_path


def write_resume_state(path: Path, data: dict[str, object], json_path: Path, csv_path: Path, report_path: Path) -> None:
    resume = data.get("resume", {})
    state = {
        "schema": "medioevo.global_curador_resume.v1",
        "updated_at_utc": utc_now(),
        "scan_mode": data.get("scan_mode"),
        "status": data.get("status"),
        "resume": resume,
        "outputs": {
            "json": str(json_path),
            "csv": str(csv_path),
            "report": str(report_path),
        },
        "next_command_hint": "",
    }
    if isinstance(resume, dict) and resume.get("truncated"):
        labels = " ".join(f"--only-root {label}" for label in resume.get("root_labels", []))
        state["next_command_hint"] = (
            "python tools\\release\\global_curador_audit.py "
            f"{labels} --max-files {resume.get('max_files')} --start-after \"{resume.get('next_start_after')}\""
        ).strip()
    write_json(path, state)


def artifact_hash(path: Path) -> str:
    return sha256_file(path) if path.exists() else ""


def write_report(path: Path, data: dict[str, object], csv_path: Path, json_path: Path, witness_path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    summary = data["summary"]  # type: ignore[index]
    counts = summary["counts"]  # type: ignore[index]
    root_stats = data["root_stats"]  # type: ignore[index]
    focus_stats = data["focus_stats"]  # type: ignore[index]
    resume = data.get("resume", {})
    lines = [
        "# Global Curador SETO Dry Audit 2026-05-05",
        "",
        "Status: `DRY_RUN_NO_DELETE_NO_MOVE`",
        f"Scan mode: `{data.get('scan_mode', 'full')}`",
        "",
        "This report implements a dry Curador pass over the selected roots. It records evidence for later cleanup gates; it does not approve deletion by itself.",
        "",
        "## Artifacts",
        "",
        f"- JSON summary: `{json_path}`",
        f"- CSV file manifest: `{csv_path}`",
        f"- WitnessLog: `{witness_path}`",
        "",
        "## Counts",
        "",
        "| metric | value |",
        "|---|---:|",
    ]
    for key, value in counts.items():  # type: ignore[union-attr]
        lines.append(f"| `{key}` | {value} |")
    if isinstance(resume, dict):
        lines.extend(
            [
                "",
                "## Resume",
                "",
                "| field | value |",
                "|---|---|",
                f"| `truncated` | `{resume.get('truncated')}` |",
                f"| `processed_files` | `{resume.get('processed_files')}` |",
                f"| `max_files` | `{resume.get('max_files')}` |",
                f"| `start_after_found` | `{resume.get('start_after_found')}` |",
                f"| `next_start_after` | `{resume.get('next_start_after') or ''}` |",
            ]
        )
    lines.extend(["", "## Root Stats", "", "| root | exists | files | dirs | MB | hashed | hash_skipped | generated_dirs_skipped |", "|---|---:|---:|---:|---:|---:|---:|---:|"])
    for label, stats in root_stats.items():  # type: ignore[union-attr]
        mb = int(stats["bytes"]) / 1024 / 1024
        lines.append(
            f"| `{label}` | {stats['exists']} | {stats['files']} | {stats['dirs']} | {mb:.2f} | {stats['hashed']} | {stats['hash_skipped']} | {stats['generated_dirs_skipped']} |"
        )
    lines.extend(["", "## Focus Stats", "", "| focus | files | MB | hashed |", "|---|---:|---:|---:|"])
    for label, stats in focus_stats.items():  # type: ignore[union-attr]
        mb = int(stats["bytes"]) / 1024 / 1024
        lines.append(f"| `{label}` | {stats['files']} | {mb:.2f} | {stats['hashed']} |")
    lines.extend(["", "## ActionGate Summary", "", "| gate | count |", "|---|---:|"])
    for gate, count in summary["gate_counts"]:  # type: ignore[index]
        lines.append(f"| `{gate}` | {count} |")
    lines.extend(["", "## Decision Summary", "", "| decision | count |", "|---|---:|"])
    for decision, count in summary["decision_counts"]:  # type: ignore[index]
        lines.append(f"| `{decision}` | {count} |")
    lines.extend(["", "## Exact Duplicate Groups", "", "| sha256 | count | duplicate MB if one kept | gate | examples |", "|---|---:|---:|---|---|"])
    for group in summary["exact_duplicates"][:20]:  # type: ignore[index]
        dup_mb = int(group["total_duplicate_bytes_if_one_kept"]) / 1024 / 1024
        examples = "<br>".join(f"`{example}`" for example in group["examples"][:3])
        lines.append(f"| `{str(group['sha256'])[:16]}...` | {group['count']} | {dup_mb:.2f} | `{group['action_gate']}` | {examples} |")
    lines.extend(["", "## Large Files", "", "| size MB | gate | decision | path |", "|---:|---|---|---|"])
    for row in summary["large_files"][:25]:  # type: ignore[index]
        mb = int(row["size_bytes"]) / 1024 / 1024
        lines.append(f"| {mb:.2f} | `{row['action_gate']}` | `{row['decision']}` | `{row['path']}` |")
    lines.extend(["", "## Delete Candidate Sample", "", "| gate | decision | path |", "|---|---|---|"])
    for item in summary["delete_candidates_sample"][:50]:  # type: ignore[index]
        lines.append(f"| `{item.get('action_gate', 'REVIEW')}` | `{item.get('decision', 'CANDIDATE_DELETE_REVIEW')}` | `{item.get('path')}` |")
    lines.extend(["", "## Boundaries", "", "- No deletion, movement, extraction or publication was executed.", "- `BLOCK` rows require private/secret/claim review and cannot be cleanup targets.", "- `REVIEW` rows require ficha, canonical copy or regenerability proof before a later cleanup pass.", "- The CSV manifest is the evidence base for follow-up exact-duplicate and generated-residue gates.", ""])
    path.write_text("\n".join(lines), encoding="utf-8")


def write_witness_log(path: Path, event: dict[str, object]) -> dict[str, object]:
    path.parent.mkdir(parents=True, exist_ok=True)
    previous_hash = "GENESIS"
    if path.exists():
        try:
            lines = [line for line in path.read_text(encoding="utf-8", errors="ignore").splitlines() if line.strip()]
            if lines:
                previous_hash = json.loads(lines[-1]).get("event_hash", "PARSE_MISSING")
        except (OSError, json.JSONDecodeError):
            previous_hash = "PARSE_ERROR_REVIEW"
    event = dict(event)
    event["previous_hash"] = previous_hash
    canonical = json.dumps(event, sort_keys=True, ensure_ascii=False, separators=(",", ":"))
    event["event_hash"] = hashlib.sha256(canonical.encode("utf-8")).hexdigest()
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(event, ensure_ascii=False, sort_keys=True) + "\n")
    return event


def normalize_existing_data(data: dict[str, object]) -> None:
    generated = []
    for item in data.get("generated_dirs_sample", []):  # type: ignore[union-attr]
        path = Path(str(item.get("path", "")))
        root_label = str(item.get("root", "unknown"))
        if str(path):
            generated.append(generated_dir_record(path, root_label))
    if generated:
        data["generated_dirs_sample"] = generated

    summary = data.get("summary")
    if not isinstance(summary, dict):
        return
    old_candidates = summary.get("delete_candidates_sample", [])
    file_candidates = []
    if isinstance(old_candidates, list):
        for item in old_candidates:
            if not isinstance(item, dict):
                continue
            if "size_bytes" in item and str(item.get("decision", "")).startswith("CANDIDATE_DELETE"):
                file_candidates.append(item)
    dir_candidates = [
        item
        for item in generated
        if str(item.get("decision", "")).startswith("CANDIDATE_DELETE")
    ]
    summary["delete_candidates_sample"] = (dir_candidates + file_candidates)[:300]


def main() -> int:
    parser = argparse.ArgumentParser(description="Global dry-run Curador SETO audit. Writes manifests only; never deletes or moves files.")
    parser.add_argument("--hash-max-mb", type=int, default=DEFAULT_HASH_MAX_MB)
    parser.add_argument("--duplicate-limit", type=int, default=DEFAULT_DUPLICATE_LIMIT)
    parser.add_argument("--large-limit", type=int, default=DEFAULT_LARGE_LIMIT)
    parser.add_argument("--only-root", action="append", default=[], help="scan only a default root label; repeatable")
    parser.add_argument("--max-files", type=int, default=0, help="stop after this many file rows and emit resume state")
    parser.add_argument("--start-after", default="", help="resume after this absolute or workspace-relative path")
    parser.add_argument("--json-out", default="")
    parser.add_argument("--csv-out", default="")
    parser.add_argument("--report-out", default="")
    parser.add_argument("--state-out", default=str(DEFAULT_STATE_OUT))
    parser.add_argument("--witness-log", default=str(ROOT / "qa_artifacts" / "witness_log" / "curador_seto_witnesslog.jsonl"))
    parser.add_argument("--finalize-existing", action="store_true", help="finish report and WitnessLog from an existing JSON/CSV audit output")
    parser.add_argument("--json", action="store_true", help="print the summary JSON to stdout")
    args = parser.parse_args()

    root_labels = {str(item) for item in args.only_root}
    max_files = args.max_files if args.max_files > 0 else None
    default_json, default_csv, default_report = default_output_paths(root_labels, max_files, args.start_after or None)
    csv_path = Path(args.csv_out or default_csv)
    json_path = Path(args.json_out or default_json)
    report_path = Path(args.report_out or default_report)
    state_path = Path(args.state_out)
    witness_path = Path(args.witness_log)

    if args.finalize_existing:
        data = json.loads(json_path.read_text(encoding="utf-8"))
        normalize_existing_data(data)
    else:
        hash_max_bytes = args.hash_max_mb * 1024 * 1024
        registry_blob = read_registry_texts()
        try:
            scan = scan_roots(
                hash_max_bytes=hash_max_bytes,
                registry_blob=registry_blob,
                root_labels=root_labels or None,
                max_files=max_files,
                start_after=args.start_after or None,
            )
        except ValueError as exc:
            parser.error(str(exc))
        rows = scan.pop("rows")
        summary = summarize(
            rows=rows,  # type: ignore[arg-type]
            generated_dirs=scan["generated_dirs"],  # type: ignore[arg-type]
            project_roots=scan["project_roots"],  # type: ignore[arg-type]
            errors=scan["errors"],  # type: ignore[arg-type]
            duplicate_limit=args.duplicate_limit,
            large_limit=args.large_limit,
        )

        data = {
            "generated_at_utc": utc_now(),
            "status": "DRY_RUN_NO_DELETE_NO_MOVE",
            "scan_mode": "incremental" if root_labels or max_files or args.start_after else "full",
            "workspace_root": str(ROOT),
            "hash_max_mb": args.hash_max_mb,
            "selected_roots": [str(item["label"]) for item in scan["selected_roots"]],  # type: ignore[index]
            "resume": scan["resume"],
            "root_stats": scan["root_stats"],
            "focus_stats": scan["focus_stats"],
            "summary": summary,
            "project_roots": scan["project_roots"],
            "generated_dirs_sample": scan["generated_dirs"][:300],
            "errors_sample": scan["errors"][:120],
            "manifest_csv": str(csv_path),
            "report_md": str(report_path),
            "witness_log": str(witness_path),
            "rules": [
                "No files were deleted, moved, extracted or published.",
                "Exact duplicates remain REVIEW until a canonical copy is chosen.",
                "Private game, TCG, secret-like and strong-claim material remains BLOCK.",
                "Generated caches/builds are candidates only after ActionGate and path containment checks.",
            ],
        }

        write_csv(csv_path, rows)  # type: ignore[arg-type]
        write_json(json_path, data)
    selected_roots_for_event = data.get("selected_roots")
    if not isinstance(selected_roots_for_event, list):
        selected_roots_for_event = [str(item["label"]) for item in selected_root_defs(root_labels or None)]
    event = write_witness_log(
        witness_path,
        {
            "timestamp_utc": utc_now(),
            "event_type": "global_curador_seto_dry_audit",
            "actor": "tools/release/global_curador_audit.py",
            "status": "DRY_RUN_NO_DELETE_NO_MOVE",
            "scan_mode": data.get("scan_mode", "full"),
            "input_roots": selected_roots_for_event,
            "outputs": {
                "json": str(json_path),
                "csv": str(csv_path),
                "report": str(report_path),
                "state": str(state_path),
            },
            "artifact_hashes": {
                "json": artifact_hash(json_path),
                "csv": artifact_hash(csv_path),
            },
            "action_gate": "REVIEW",
        },
    )
    data["witness_event_hash"] = event["event_hash"]
    write_json(json_path, data)
    write_resume_state(state_path, data, json_path, csv_path, report_path)
    write_report(report_path, data, csv_path, json_path, witness_path)

    if args.json:
        print_json(data)
    else:
        summary = data["summary"]
        print(f"status={data['status']}")
        print(f"files={summary['counts']['files']} hashed={summary['counts']['hashed_files']} duplicates={summary['counts']['exact_duplicate_groups']}")
        print(f"json={json_path}")
        print(f"csv={csv_path}")
        print(f"report={report_path}")
        print(f"witness_event_hash={event['event_hash']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
