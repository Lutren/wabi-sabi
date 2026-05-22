from __future__ import annotations

import hashlib
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CEREBRO_CANON_MERGE_REVIEW_SCHEMA = "wabi.cerebro_canon_merge_review.v1"
TEXT_SUFFIXES = {"", ".cfg", ".csv", ".css", ".html", ".ini", ".js", ".json", ".md", ".py", ".toml", ".txt", ".yaml", ".yml"}


def build_cerebro_canon_merge_review(
    workspace: str | Path,
    *,
    index_dir: str | Path | None = None,
) -> dict[str, Any]:
    workspace_path = Path(workspace).resolve()
    index_path = Path(index_dir).resolve() if index_dir else workspace_path / "runtime" / "cerebro_master_index"
    comparison_path = index_path / "VARIANT_SEMANTIC_COMPARISON.json"
    comparison = _safe_json(comparison_path)
    signal_entries = _signals_by_path(_read_jsonl(index_path / "LINE_SIGNAL_INDEX.jsonl"))
    candidates = [
        _review_candidate(item, workspace=workspace_path, signals_by_path=signal_entries)
        for item in comparison.get("comparisons", [])
        if item.get("merge_gate") == "REVIEW_CANON_MERGE_CANDIDATE"
    ]
    set_counts = Counter(candidate["candidate_set_id"] for candidate in candidates)
    for candidate in candidates:
        candidate["duplicate_candidate_set"] = set_counts[candidate["candidate_set_id"]] > 1
        candidate["review_decision"] = _review_decision(candidate)
    summary = {
        "review_candidate_groups": len(candidates),
        "unique_candidate_sets": len(set_counts),
        "duplicate_candidate_sets": sum(1 for count in set_counts.values() if count > 1),
        "license_boundary_candidates": sum(1 for candidate in candidates if candidate["boundary_type"] == "LICENSE_BOUNDARY"),
        "content_canonicalization_candidates": sum(
            1 for candidate in candidates if candidate["boundary_type"] == "CONTENT_CANONICALIZATION"
        ),
        "auto_merge_actions": 0,
        "source_mutations": 0,
        "comparison_source_exists": comparison_path.exists(),
    }
    return {
        "schema": CEREBRO_CANON_MERGE_REVIEW_SCHEMA,
        "generated_at_utc": _utc_now(),
        "ok": comparison_path.exists(),
        "workspace": str(workspace_path),
        "index_dir": str(index_path),
        "source_artifacts": {
            "variant_semantic_comparison": str(comparison_path),
            "line_signal_index": str(index_path / "LINE_SIGNAL_INDEX.jsonl"),
        },
        "summary": summary,
        "candidates": candidates,
        "certainty": [
            "Only groups already gated as REVIEW_CANON_MERGE_CANDIDATE are included.",
            "The review pack does not merge, move, delete or rewrite source files.",
        ],
        "inference": [
            "A repeated candidate_set_id means two comparison heuristics point to the same file set.",
            "License files require ownership/package-boundary review even when text-token similarity is high.",
        ],
        "unknown": [
            "Human/legal ownership of LICENSE variants is not resolved by text similarity.",
            "Canon merge decisions remain pending until excerpts are reviewed and a migration log exists.",
        ],
        "not_claimed": [
            "No canon merge was performed.",
            "No duplicate archive action was performed.",
            "No source tree cleanup was executed.",
        ],
    }


def write_cerebro_canon_merge_review(payload: dict[str, Any], output_dir: str | Path) -> list[str]:
    output_path = Path(output_dir).resolve()
    output_path.mkdir(parents=True, exist_ok=True)
    json_path = output_path / "VARIANT_CANON_MERGE_REVIEW_PACK.json"
    md_path = output_path / "VARIANT_CANON_MERGE_REVIEW_PACK.md"
    jsonl_path = output_path / "VARIANT_CANON_MERGE_REVIEW_QUEUE.jsonl"
    json_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=True), encoding="utf-8")
    md_path.write_text(_review_markdown(payload), encoding="utf-8")
    with jsonl_path.open("w", encoding="utf-8") as handle:
        for candidate in payload.get("candidates", []):
            handle.write(json.dumps(candidate, ensure_ascii=False, sort_keys=True) + "\n")
    return [str(json_path), str(md_path), str(jsonl_path)]


def compact_cerebro_canon_merge_review(payload: dict[str, Any]) -> dict[str, Any]:
    return {
        "schema": payload["schema"],
        "ok": payload["ok"],
        "workspace": payload["workspace"],
        "summary": payload["summary"],
        "artifacts": payload.get("artifacts", []),
        "candidates": payload.get("candidates", []),
        "not_claimed": payload["not_claimed"],
    }


def _review_candidate(item: dict[str, Any], *, workspace: Path, signals_by_path: dict[str, list[dict[str, Any]]]) -> dict[str, Any]:
    file_items = item.get("files", [])
    paths = [str(file_item.get("path") if isinstance(file_item, dict) else file_item) for file_item in file_items]
    suffixes = sorted({str(file_item.get("suffix") or Path(str(file_item.get("path", ""))).suffix).lower() for file_item in file_items if isinstance(file_item, dict)})
    sha_prefixes = sorted({str(file_item.get("sha256_prefix") or "") for file_item in file_items if isinstance(file_item, dict)})
    boundary_type = _boundary_type(paths, suffixes)
    files = [_file_review(file_item, workspace=workspace, signals_by_path=signals_by_path) for file_item in file_items]
    return {
        "variant_id": item.get("variant_id"),
        "candidate_set_id": _candidate_set_id(paths),
        "semantic_status": item.get("semantic_status"),
        "recommendation": item.get("recommendation"),
        "original_merge_gate": item.get("merge_gate"),
        "review_gate": "REVIEW_REQUIRED_NO_AUTO_MERGE",
        "boundary_type": boundary_type,
        "canonical_candidate": item.get("canonical_candidate"),
        "group_size": item.get("group_size"),
        "min_token_similarity": item.get("min_token_similarity"),
        "min_signal_similarity": item.get("min_signal_similarity"),
        "critical_signal_delta": item.get("critical_signal_delta", []),
        "common_signals": item.get("common_signals", []),
        "sha_prefixes": sha_prefixes,
        "suffixes": suffixes,
        "material_delta": _material_delta(sha_prefixes, suffixes),
        "files": files,
        "source_mutations": 0,
    }


def _file_review(file_item: dict[str, Any], *, workspace: Path, signals_by_path: dict[str, list[dict[str, Any]]]) -> dict[str, Any]:
    rel_path = str(file_item.get("path") or "")
    suffix = str(file_item.get("suffix") or Path(rel_path).suffix).lower()
    signal_excerpts = [
        {
            "line_no": entry.get("line_no"),
            "excerpt": entry.get("excerpt"),
            "signals": entry.get("signals", []),
        }
        for entry in signals_by_path.get(rel_path, [])[:5]
    ]
    text_excerpts = signal_excerpts or _plain_excerpts(workspace, rel_path, suffix)
    return {
        "path": rel_path,
        "suffix": suffix,
        "sha256_prefix": file_item.get("sha256_prefix", ""),
        "line_count": file_item.get("line_count", 0),
        "signal_count": file_item.get("signal_count", 0),
        "signals": file_item.get("signals", {}),
        "excerpt_basis": "line_signal_index" if signal_excerpts else "plain_text_head",
        "excerpts": text_excerpts,
    }


def _review_decision(candidate: dict[str, Any]) -> dict[str, Any]:
    if candidate["boundary_type"] == "LICENSE_BOUNDARY":
        action = "KEEP_LICENSE_FILES_SEPARATE_UNTIL_PACKAGE_OWNER_REVIEW"
        risk = "license_boundary"
    elif candidate["duplicate_candidate_set"]:
        action = "DEDUP_REVIEW_ENTRY_BEFORE_CANON_ACTION"
        risk = "duplicate_review_group"
    elif ".md" in candidate["suffixes"] and ".txt" in candidate["suffixes"]:
        action = "CANONICALIZE_MARKDOWN_AFTER_EXCERPT_REVIEW"
        risk = "format_variant"
    else:
        action = "COMPARE_EXCERPTS_BEFORE_CANON_MERGE"
        risk = "semantic_variant"
    return {
        "action": action,
        "risk": risk,
        "execution_allowed_now": False,
        "required_before_execution": [
            "review excerpts",
            "choose canonical target",
            "write migration log",
            "run relevant tests or document no-code impact",
        ],
    }


def _boundary_type(paths: list[str], suffixes: list[str]) -> str:
    names = {Path(path).name.lower() for path in paths}
    lowered = " ".join(paths).lower()
    if names == {"license"} or "license" in names:
        return "LICENSE_BOUNDARY"
    if ".md" in suffixes and ".txt" in suffixes:
        return "CONTENT_CANONICALIZATION"
    if "_github_staging" in lowered:
        return "PACKAGE_BOUNDARY"
    return "CANON_REVIEW"


def _material_delta(sha_prefixes: list[str], suffixes: list[str]) -> list[str]:
    delta = []
    if len(set(sha_prefixes)) > 1:
        delta.append("sha256_prefix_delta")
    if len(set(suffixes)) > 1:
        delta.append("format_suffix_delta")
    return delta


def _plain_excerpts(workspace: Path, rel_path: str, suffix: str) -> list[dict[str, Any]]:
    if suffix not in TEXT_SUFFIXES:
        return []
    target = (workspace / rel_path).resolve()
    try:
        target.relative_to(workspace)
    except ValueError:
        return []
    try:
        lines = target.read_text(encoding="utf-8", errors="replace").splitlines()
    except OSError:
        return []
    excerpts = []
    for number, line in enumerate(lines, start=1):
        clean = line.strip()
        if not clean:
            continue
        excerpts.append({"line_no": number, "excerpt": clean[:220], "signals": []})
        if len(excerpts) >= 5:
            break
    return excerpts


def _candidate_set_id(paths: list[str]) -> str:
    joined = "\n".join(sorted(paths))
    return hashlib.sha256(joined.encode("utf-8")).hexdigest()[:12]


def _review_markdown(payload: dict[str, Any]) -> str:
    summary = payload["summary"]
    lines = [
        "# VARIANT CANON MERGE REVIEW PACK",
        "",
        "CERTEZA:",
        "- Includes only groups gated as `REVIEW_CANON_MERGE_CANDIDATE`.",
        "- Source mutations: `0`.",
        "",
        "INFERENCIA:",
        "- High similarity is a review signal, not merge permission.",
        "- License files remain package-boundary material until ownership is reviewed.",
        "",
        "SUMMARY:",
        f"- Review candidate groups: `{summary['review_candidate_groups']}`",
        f"- Unique candidate sets: `{summary['unique_candidate_sets']}`",
        f"- Duplicate candidate sets: `{summary['duplicate_candidate_sets']}`",
        f"- License boundary candidates: `{summary['license_boundary_candidates']}`",
        f"- Content canonicalization candidates: `{summary['content_canonicalization_candidates']}`",
        f"- Auto-merge actions: `{summary['auto_merge_actions']}`",
        "",
    ]
    for candidate in payload.get("candidates", []):
        lines.extend(
            [
                f"## {candidate['variant_id']}",
                "",
                f"- Boundary: `{candidate['boundary_type']}`",
                f"- Candidate set: `{candidate['candidate_set_id']}` duplicate=`{candidate['duplicate_candidate_set']}`",
                f"- Canonical candidate: `{candidate['canonical_candidate']}`",
                f"- Review action: `{candidate['review_decision']['action']}`",
                f"- Material delta: `{', '.join(candidate['material_delta']) or 'none'}`",
                "",
            ]
        )
        for file_item in candidate.get("files", []):
            lines.append(f"### `{file_item['path']}`")
            for excerpt in file_item.get("excerpts", [])[:5]:
                lines.append(f"- L{excerpt.get('line_no')}: {excerpt.get('excerpt')}")
            lines.append("")
    return "\n".join(lines) + "\n"


def _signals_by_path(entries: list[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
    grouped: dict[str, list[dict[str, Any]]] = {}
    for entry in entries:
        grouped.setdefault(str(entry.get("path") or ""), []).append(entry)
    return grouped


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
