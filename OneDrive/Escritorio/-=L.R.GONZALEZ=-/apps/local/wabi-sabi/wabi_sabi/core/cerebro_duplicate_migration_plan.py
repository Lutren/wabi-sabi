from __future__ import annotations

import csv
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CEREBRO_DUPLICATE_MIGRATION_PLAN_SCHEMA = "wabi.cerebro_duplicate_migration_plan.v1"


def build_cerebro_duplicate_migration_plan(
    workspace: str | Path,
    *,
    index_dir: str | Path | None = None,
    archive_root: str | Path | None = None,
) -> dict[str, Any]:
    workspace_path = Path(workspace).resolve()
    index_path = Path(index_dir).resolve() if index_dir else workspace_path / "runtime" / "cerebro_master_index"
    comparison_path = index_path / "VARIANT_SEMANTIC_COMPARISON.json"
    comparison = _safe_json(comparison_path)
    manifest = _read_jsonl(index_path / "LINE_AUDIT_MANIFEST.jsonl")
    record_by_path = {str(record.get("path")): record for record in manifest}
    archive_root_rel = _normalize_rel_archive_root(archive_root)
    groups: list[dict[str, Any]] = []
    actions: list[dict[str, Any]] = []
    blocked = 0
    binary_or_archive = 0

    for item in comparison.get("comparisons", []):
        if item.get("semantic_status") != "EXACT_DUPLICATE" or item.get("merge_gate") != "REVIEW_ARCHIVE_ONLY":
            continue
        group_actions: list[dict[str, Any]] = []
        canonical = str(item.get("canonical_candidate") or "")
        canonical_record = record_by_path.get(canonical, {})
        canonical_exists = _inside_workspace(workspace_path, canonical).exists() if canonical else False
        for file_item in item.get("files", []):
            source = str(file_item.get("path") if isinstance(file_item, dict) else file_item)
            if not source or source == canonical:
                continue
            source_abs = _inside_workspace(workspace_path, source)
            source_record = record_by_path.get(source, {})
            suffix = str(source_record.get("suffix") or Path(source).suffix).lower()
            if suffix in {".zip", ".gz", ".tar", ".tgz", ".docx", ".pdf"}:
                binary_or_archive += 1
            status, reasons = _action_status(
                source=source,
                canonical=canonical,
                source_abs=source_abs,
                canonical_exists=canonical_exists,
                source_record=source_record,
                canonical_record=canonical_record,
            )
            if status != "READY_FOR_REVIEW":
                blocked += 1
            action = {
                "variant_id": item.get("variant_id"),
                "semantic_status": item.get("semantic_status"),
                "action": "DRY_RUN_ARCHIVE_DUPLICATE",
                "status": status,
                "review_gate": "REVIEW_ARCHIVE_ONLY_WITH_MIGRATION_LOG",
                "source": source,
                "canonical_preserved": canonical,
                "proposed_archive_target": _archive_target(archive_root_rel, source),
                "source_exists": source_abs.exists(),
                "canonical_exists": canonical_exists,
                "sha256": source_record.get("sha256") or canonical_record.get("sha256") or "",
                "suffix": suffix,
                "risk_flags": _risk_flags(source, suffix),
                "blocking_reasons": reasons,
                "not_executed": True,
            }
            group_actions.append(action)
            actions.append(action)
        groups.append(
            {
                "variant_id": item.get("variant_id"),
                "canonical_preserved": canonical,
                "group_size": int(item.get("group_size") or len(item.get("files", []))),
                "duplicate_action_count": len(group_actions),
                "review_gate": "REVIEW_ARCHIVE_ONLY_WITH_MIGRATION_LOG",
                "actions": group_actions,
            }
        )

    action_counter = Counter(action["status"] for action in actions)
    summary = {
        "exact_duplicate_groups": len(groups),
        "proposed_archive_moves": len(actions),
        "ready_for_review": int(action_counter.get("READY_FOR_REVIEW", 0)),
        "blocked_moves": blocked,
        "binary_or_archive_duplicates": binary_or_archive,
        "canonical_files_preserved": len({group["canonical_preserved"] for group in groups if group["canonical_preserved"]}),
        "comparison_source_exists": comparison_path.exists(),
        "dry_run_only": True,
        "source_mutations": 0,
    }
    return {
        "schema": CEREBRO_DUPLICATE_MIGRATION_PLAN_SCHEMA,
        "generated_at_utc": _utc_now(),
        "ok": comparison_path.exists(),
        "workspace": str(workspace_path),
        "index_dir": str(index_path),
        "source_artifacts": {
            "variant_semantic_comparison": str(comparison_path),
            "line_audit_manifest": str(index_path / "LINE_AUDIT_MANIFEST.jsonl"),
        },
        "archive_root_proposed": archive_root_rel,
        "summary": summary,
        "groups": groups,
        "actions": actions,
        "certainty": [
            "Only groups already classified as EXACT_DUPLICATE with REVIEW_ARCHIVE_ONLY are included.",
            "The plan does not move, delete, merge or rewrite source files.",
        ],
        "inference": [
            "The proposed archive target preserves the original relative path under a review archive root.",
        ],
        "unknown": [
            "Final archive execution still requires review and a migration log entry.",
            "External ownership or license implications are not resolved by hash equality.",
        ],
        "not_claimed": [
            "No duplicate was archived.",
            "No canon merge was performed.",
            "No source tree cleanup was executed.",
        ],
    }


def write_cerebro_duplicate_migration_plan(payload: dict[str, Any], output_dir: str | Path) -> list[str]:
    output_path = Path(output_dir).resolve()
    output_path.mkdir(parents=True, exist_ok=True)
    json_path = output_path / "VARIANT_EXACT_DUPLICATE_MIGRATION_PLAN.json"
    md_path = output_path / "VARIANT_EXACT_DUPLICATE_MIGRATION_PLAN.md"
    jsonl_path = output_path / "VARIANT_EXACT_DUPLICATE_MIGRATION_QUEUE.jsonl"
    csv_path = output_path / "VARIANT_EXACT_DUPLICATE_MIGRATION_PLAN.csv"
    json_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=True), encoding="utf-8")
    md_path.write_text(_plan_markdown(payload), encoding="utf-8")
    with jsonl_path.open("w", encoding="utf-8") as handle:
        for action in payload.get("actions", []):
            handle.write(json.dumps(action, ensure_ascii=False, sort_keys=True) + "\n")
    with csv_path.open("w", encoding="utf-8", newline="") as handle:
        fieldnames = [
            "variant_id",
            "status",
            "source",
            "canonical_preserved",
            "proposed_archive_target",
            "suffix",
            "sha256",
            "risk_flags",
        ]
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for action in payload.get("actions", []):
            writer.writerow(
                {
                    "variant_id": action.get("variant_id", ""),
                    "status": action.get("status", ""),
                    "source": action.get("source", ""),
                    "canonical_preserved": action.get("canonical_preserved", ""),
                    "proposed_archive_target": action.get("proposed_archive_target", ""),
                    "suffix": action.get("suffix", ""),
                    "sha256": action.get("sha256", ""),
                    "risk_flags": ";".join(action.get("risk_flags", [])),
                }
            )
    return [str(json_path), str(md_path), str(jsonl_path), str(csv_path)]


def compact_cerebro_duplicate_migration_plan(payload: dict[str, Any]) -> dict[str, Any]:
    return {
        "schema": payload["schema"],
        "ok": payload["ok"],
        "workspace": payload["workspace"],
        "summary": payload["summary"],
        "artifacts": payload.get("artifacts", []),
        "top_actions": payload.get("actions", [])[:12],
        "not_claimed": payload["not_claimed"],
    }


def _action_status(
    *,
    source: str,
    canonical: str,
    source_abs: Path,
    canonical_exists: bool,
    source_record: dict[str, Any],
    canonical_record: dict[str, Any],
) -> tuple[str, list[str]]:
    reasons: list[str] = []
    if not canonical:
        reasons.append("missing_canonical_candidate")
    if source == canonical:
        reasons.append("source_is_canonical")
    if not source_abs.exists():
        reasons.append("source_missing")
    if not canonical_exists:
        reasons.append("canonical_missing")
    source_sha = str(source_record.get("sha256") or "")
    canonical_sha = str(canonical_record.get("sha256") or "")
    if source_sha and canonical_sha and source_sha != canonical_sha:
        reasons.append("sha256_mismatch")
    return ("BLOCKED_REVIEW_INPUT", reasons) if reasons else ("READY_FOR_REVIEW", [])


def _risk_flags(source: str, suffix: str) -> list[str]:
    flags = []
    lowered = source.lower()
    if suffix in {".zip", ".gz", ".tar", ".tgz"}:
        flags.append("archive_binary")
    if suffix in {".docx", ".pdf"}:
        flags.append("document_binary")
    if "license" in lowered:
        flags.append("license_file")
    if "new folder" in lowered or "copy" in lowered or "copia" in lowered:
        flags.append("duplicate_folder_marker")
    return flags


def _archive_target(archive_root_rel: str, source: str) -> str:
    return str(Path(archive_root_rel) / _source_archive_tail(source)).replace("/", "\\")


def _source_archive_tail(source: str) -> Path:
    parts = [part for part in source.replace("/", "\\").split("\\") if part]
    for marker in ["-=CEREBRO=-", "CEREBRO"]:
        if marker in parts:
            index = parts.index(marker)
            tail = parts[index + 1 :]
            if tail:
                return Path(*tail)
    return Path(*parts) if parts else Path("unknown")


def _normalize_rel_archive_root(archive_root: str | Path | None) -> str:
    if archive_root is None:
        return str(
            Path("-=MEDIOEVO=-")
            / "-=LIBROS"
            / "-=CEREBRO=-"
            / "_archive"
            / "exact_duplicates"
            / datetime.now().strftime("%Y%m%d")
        )
    return str(Path(archive_root))


def _inside_workspace(workspace: Path, rel_path: str) -> Path:
    target = (workspace / rel_path).resolve()
    try:
        target.relative_to(workspace)
    except ValueError:
        return workspace / "__PATH_OUTSIDE_WORKSPACE_BLOCKED__"
    return target


def _plan_markdown(payload: dict[str, Any]) -> str:
    summary = payload["summary"]
    lines = [
        "# VARIANT EXACT DUPLICATE MIGRATION PLAN",
        "",
        "CERTEZA:",
        "- Includes only semantic status `EXACT_DUPLICATE` with gate `REVIEW_ARCHIVE_ONLY`.",
        "- This is a dry-run plan. Source mutations: `0`.",
        "",
        "INFERENCIA:",
        "- Proposed archive targets preserve source paths under the review archive root.",
        "",
        "INCOGNITA:",
        "- Review must still approve execution and write `MIGRATION_LOG.md` before moving files.",
        "",
        "SUMMARY:",
        f"- Exact duplicate groups: `{summary['exact_duplicate_groups']}`",
        f"- Proposed archive moves: `{summary['proposed_archive_moves']}`",
        f"- Ready for review: `{summary['ready_for_review']}`",
        f"- Blocked moves: `{summary['blocked_moves']}`",
        f"- Binary/archive duplicates: `{summary['binary_or_archive_duplicates']}`",
        "",
        "| Status | Source | Canonical preserved | Proposed archive target | Flags |",
        "|---|---|---|---|---|",
    ]
    for action in payload.get("actions", []):
        flags = ", ".join(action.get("risk_flags", [])) or "none"
        lines.append(
            "| {} | `{}` | `{}` | `{}` | {} |".format(
                action.get("status", ""),
                action.get("source", ""),
                action.get("canonical_preserved", ""),
                action.get("proposed_archive_target", ""),
                flags,
            )
        )
    return "\n".join(lines) + "\n"


def _read_jsonl(path: Path) -> list[dict[str, Any]]:
    rows = []
    if not path.exists():
        return rows
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if not line:
                continue
            try:
                data = json.loads(line)
            except json.JSONDecodeError:
                continue
            if isinstance(data, dict):
                rows.append(data)
    return rows


def _safe_json(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}
    return data if isinstance(data, dict) else {"payload": data}


def _utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()
