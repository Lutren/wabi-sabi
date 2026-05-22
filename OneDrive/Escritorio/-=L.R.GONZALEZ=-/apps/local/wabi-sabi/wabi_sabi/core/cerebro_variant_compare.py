from __future__ import annotations

import json
import re
import unicodedata
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CEREBRO_VARIANT_COMPARISON_SCHEMA = "wabi.cerebro_variant_semantic_comparison.v1"

TEXT_SUFFIXES = {
    ".cfg",
    ".csv",
    ".css",
    ".html",
    ".ini",
    ".js",
    ".json",
    ".jsx",
    ".md",
    ".py",
    ".toml",
    ".ts",
    ".tsx",
    ".txt",
    ".yaml",
    ".yml",
}
CODE_SUFFIXES = {".js", ".jsx", ".py", ".ts", ".tsx", ".html", ".css", ".toml", ".yaml", ".yml", ".json"}
CRITICAL_SIGNALS = {
    "ActionGate",
    "Claudio",
    "DUAT",
    "EML",
    "GEODIA",
    "H_eff",
    "J_c",
    "OSIT",
    "Phi_eff",
    "POVM",
    "R",
    "Sigma",
    "TUIP",
    "WitnessLog",
    "agent_programming",
    "browser",
    "epsilon",
    "lambda",
}
STOPWORDS = {
    "con",
    "del",
    "desde",
    "donde",
    "este",
    "esta",
    "esto",
    "para",
    "por",
    "que",
    "the",
    "and",
    "una",
    "uno",
    "los",
    "las",
    "como",
    "sin",
    "not",
    "this",
    "that",
    "from",
    "true",
    "false",
}


def build_cerebro_variant_comparison(
    workspace: str | Path,
    *,
    index_dir: str | Path | None = None,
) -> dict[str, Any]:
    workspace_path = Path(workspace).resolve()
    index_path = Path(index_dir).resolve() if index_dir else workspace_path / "runtime" / "cerebro_master_index"
    manifest_path = index_path / "LINE_AUDIT_MANIFEST.jsonl"
    signal_path = index_path / "LINE_SIGNAL_INDEX.jsonl"
    manifest = _read_jsonl(manifest_path)
    signals_by_path = _signals_by_path(_read_jsonl(signal_path))
    variant_records = _build_variant_records(manifest)
    record_by_path = {str(record.get("path")): record for record in manifest}
    comparisons = [
        _compare_variant_group(variant, record_by_path=record_by_path, signals_by_path=signals_by_path, workspace=workspace_path)
        for variant in variant_records
    ]
    summary = _summary(comparisons)
    return {
        "schema": CEREBRO_VARIANT_COMPARISON_SCHEMA,
        "generated_at_utc": _utc_now(),
        "ok": True,
        "workspace": str(workspace_path),
        "index_dir": str(index_path),
        "source_artifacts": {
            "manifest": str(manifest_path),
            "line_signal_index": str(signal_path),
        },
        "summary": summary,
        "comparisons": comparisons,
        "certainty": [
            "Comparison uses hashes, paths, manifest metrics, signal excerpts and text-token signatures where safe text is readable.",
            "No source file is moved, deleted, merged or rewritten by this comparison.",
        ],
        "inference": [
            "High similarity with no critical-signal delta is a review candidate, not an automatic merge.",
        ],
        "unknown": [
            "DOCX/PDF/binary semantic equality is limited to extracted manifest signals unless a dedicated visual/document diff is run.",
            "Archive/license ownership is not resolved by semantic similarity.",
        ],
        "not_claimed": [
            "No canon merge completed.",
            "No duplicate archive action completed.",
            "No public release or publication claim.",
        ],
    }


def write_cerebro_variant_comparison(payload: dict[str, Any], output_dir: str | Path) -> list[str]:
    output_path = Path(output_dir).resolve()
    output_path.mkdir(parents=True, exist_ok=True)
    json_path = output_path / "VARIANT_SEMANTIC_COMPARISON.json"
    md_path = output_path / "VARIANT_SEMANTIC_COMPARISON.md"
    actions_path = output_path / "VARIANT_ACTION_QUEUE.jsonl"
    json_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=True), encoding="utf-8")
    md_path.write_text(_comparison_markdown(payload), encoding="utf-8")
    with actions_path.open("w", encoding="utf-8") as handle:
        for item in payload.get("comparisons", []):
            handle.write(json.dumps(_action_record(item), ensure_ascii=False, sort_keys=True) + "\n")
    return [str(json_path), str(md_path), str(actions_path)]


def compact_cerebro_variant_comparison(payload: dict[str, Any]) -> dict[str, Any]:
    return {
        "schema": payload["schema"],
        "ok": payload["ok"],
        "workspace": payload["workspace"],
        "summary": payload["summary"],
        "artifacts": payload.get("artifacts", []),
        "top_review": payload.get("comparisons", [])[:12],
        "not_claimed": payload["not_claimed"],
    }


def _compare_variant_group(
    variant: dict[str, Any],
    *,
    record_by_path: dict[str, dict[str, Any]],
    signals_by_path: dict[str, list[dict[str, Any]]],
    workspace: Path,
) -> dict[str, Any]:
    files = [str(path) for path in variant.get("files", [])]
    records = [record_by_path.get(path, {"path": path}) for path in files]
    signatures = [_signature(record, signals_by_path.get(str(record.get("path")), []), workspace) for record in records]
    pairwise = _pairwise(signatures)
    signals = [set(item["signals"].keys()) for item in signatures]
    common_signals = sorted(set.intersection(*signals)) if signals else []
    union_signals = sorted(set.union(*signals)) if signals else []
    critical_delta = sorted(CRITICAL_SIGNALS.intersection(union_signals).difference(common_signals))
    status, recommendation, gate = _classify(variant, signatures, pairwise, critical_delta)
    canonical = _canonical_candidate(signatures)
    return {
        "variant_id": variant["variant_id"],
        "kind": variant["kind"],
        "source_gate": variant.get("merge_gate", "REVIEW_REQUIRED"),
        "semantic_status": status,
        "recommendation": recommendation,
        "merge_gate": gate,
        "group_size": len(files),
        "canonical_candidate": canonical,
        "keep_separate": gate != "REVIEW_ARCHIVE_ONLY",
        "min_token_similarity": _round(_min(pairwise, "token_similarity")),
        "avg_token_similarity": _round(_avg(pairwise, "token_similarity")),
        "min_signal_similarity": _round(_min(pairwise, "signal_similarity")),
        "critical_signal_delta": critical_delta,
        "common_signals": common_signals,
        "union_signals": union_signals,
        "files": [_file_summary(item) for item in signatures],
        "pairwise": pairwise[:40],
        "evidence": {
            "source": variant.get("evidence", ""),
            "basis": [
                "sha256",
                "filename/stem",
                "manifest line/code/signal counts",
                "token signatures for readable text",
                "line signal excerpts",
            ],
        },
        "next_action": _next_action(status),
    }


def _signature(record: dict[str, Any], signal_entries: list[dict[str, Any]], workspace: Path) -> dict[str, Any]:
    rel_path = str(record.get("path") or "")
    suffix = str(record.get("suffix") or Path(rel_path).suffix).lower()
    text = _safe_read_text(workspace, rel_path, suffix)
    excerpts = " ".join(str(entry.get("excerpt", "")) for entry in signal_entries[:16])
    semantic_text = " ".join([Path(rel_path).stem, text, excerpts, " ".join(record.get("signals", {}).keys())])
    tokens = _tokens(semantic_text)
    heading_tokens = _heading_tokens(text)
    return {
        "path": rel_path,
        "sha256": str(record.get("sha256") or ""),
        "suffix": suffix,
        "source_kind": str(record.get("source_kind") or ""),
        "classification": str(record.get("classification") or ""),
        "line_count": int(record.get("line_count") or 0),
        "size_bytes": int(record.get("size_bytes") or 0),
        "signal_count": int(record.get("signal_count") or 0),
        "code_candidate_count": int(record.get("code_candidate_count") or 0),
        "code_fence_count": int(record.get("code_fence_count") or 0),
        "signals": dict(record.get("signals") or {}),
        "readable_text": bool(text),
        "token_count": len(tokens),
        "tokens": tokens,
        "heading_tokens": heading_tokens,
        "sample_excerpts": [str(entry.get("excerpt", "")) for entry in signal_entries[:3]],
    }


def _safe_read_text(workspace: Path, rel_path: str, suffix: str) -> str:
    if suffix not in TEXT_SUFFIXES:
        return ""
    candidate = (workspace / rel_path).resolve()
    if candidate != workspace and workspace not in candidate.parents:
        return ""
    try:
        raw = candidate.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""
    return raw[:500_000]


def _tokens(text: str) -> set[str]:
    normalized = unicodedata.normalize("NFKD", text)
    lowered = "".join(ch.lower() if ch.isalnum() else " " for ch in normalized)
    return {token for token in lowered.split() if len(token) > 2 and token not in STOPWORDS}


def _heading_tokens(text: str) -> list[str]:
    headings = []
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("#") or stripped[:3].isdigit():
            headings.extend(sorted(_tokens(stripped))[:8])
        if len(headings) >= 20:
            break
    return headings[:20]


def _pairwise(signatures: list[dict[str, Any]]) -> list[dict[str, Any]]:
    pairs = []
    for left_index, left in enumerate(signatures):
        for right in signatures[left_index + 1 :]:
            left_tokens = left["tokens"]
            right_tokens = right["tokens"]
            left_signals = set(left["signals"])
            right_signals = set(right["signals"])
            pairs.append(
                {
                    "left": left["path"],
                    "right": right["path"],
                    "token_similarity": _round(_jaccard(left_tokens, right_tokens)),
                    "signal_similarity": _round(_jaccard(left_signals, right_signals)),
                    "line_delta_ratio": _round(_delta_ratio(left["line_count"], right["line_count"])),
                    "code_delta_ratio": _round(_delta_ratio(left["code_candidate_count"], right["code_candidate_count"])),
                }
            )
    return pairs


def _classify(
    variant: dict[str, Any],
    signatures: list[dict[str, Any]],
    pairwise: list[dict[str, Any]],
    critical_delta: list[str],
) -> tuple[str, str, str]:
    kind = variant.get("kind")
    suffixes = {item["suffix"] for item in signatures}
    has_code = bool(CODE_SUFFIXES.intersection(suffixes)) or any(item["code_candidate_count"] for item in signatures)
    min_token = _min(pairwise, "token_similarity")
    min_signal = _min(pairwise, "signal_similarity")
    max_line_delta = max((item["line_delta_ratio"] for item in pairwise), default=0.0)
    if kind == "EXACT_DUPLICATE":
        return "EXACT_DUPLICATE", "ARCHIVE_DUPLICATE_AFTER_REVIEW", "REVIEW_ARCHIVE_ONLY"
    if any(suffix in {".docx", ".pdf", ".zip", ".gz"} for suffix in suffixes):
        return "FORMAT_OR_ARCHIVE_VARIANT", "KEEP_SEPARATE_UNTIL_DOCUMENT_OR_ARCHIVE_DIFF", "REVIEW_REQUIRED_NO_MERGE"
    if has_code and min_token < 0.98:
        return "CODE_OR_CONFIG_MATERIAL_DELTA", "KEEP_SEPARATE_AND_REVIEW_CODE_DIFF", "REVIEW_REQUIRED_NO_MERGE"
    if critical_delta and (min_signal < 0.90 or min_token < 0.92):
        return "MATERIAL_SIGNAL_DELTA", "KEEP_SEPARATE_AND_COMPARE_CLAIMS", "REVIEW_REQUIRED_NO_MERGE"
    if min_token >= 0.92 and min_signal >= 0.90 and max_line_delta <= 0.10:
        return "NEAR_EQUIVALENT", "CANON_MERGE_CANDIDATE_AFTER_REVIEW", "REVIEW_CANON_MERGE_CANDIDATE"
    if min_token >= 0.65 and min_signal >= 0.60:
        return "RELATED_VARIANT", "COMPARE_EXCERPTS_BEFORE_CANON_MERGE", "REVIEW_REQUIRED_NO_MERGE"
    return "LOW_SIMILARITY_VARIANT", "KEEP_SEPARATE", "REVIEW_REQUIRED_NO_MERGE"


def _canonical_candidate(signatures: list[dict[str, Any]]) -> str:
    def score(item: dict[str, Any]) -> tuple[int, int, int, str]:
        path = item["path"].lower()
        penalty = 0
        for marker in ["archive", "new folder", "_archive", "_archivar", "duplicados", "copy"]:
            if marker in path:
                penalty += 10
        if item["suffix"] in {".zip", ".gz", ".pdf", ".docx"}:
            penalty += 5
        return (penalty, -item["signal_count"], item["line_count"], item["path"])

    return sorted(signatures, key=score)[0]["path"] if signatures else ""


def _file_summary(item: dict[str, Any]) -> dict[str, Any]:
    return {
        "path": item["path"],
        "sha256_prefix": item["sha256"][:12],
        "suffix": item["suffix"],
        "source_kind": item["source_kind"],
        "line_count": item["line_count"],
        "signal_count": item["signal_count"],
        "code_candidate_count": item["code_candidate_count"],
        "readable_text": item["readable_text"],
        "signals": item["signals"],
        "sample_excerpts": item["sample_excerpts"],
    }


def _build_variant_records(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    variants: list[dict[str, Any]] = []
    by_hash: dict[str, list[dict[str, Any]]] = defaultdict(list)
    by_name: dict[str, list[dict[str, Any]]] = defaultdict(list)
    by_stem: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for record in records:
        sha = str(record.get("sha256") or "")
        if sha:
            by_hash[sha].append(record)
        name = str(record.get("name") or "").lower()
        stem = _normal_stem(Path(name).stem)
        by_name[name].append(record)
        by_stem[stem].append(record)
    for sha, group in by_hash.items():
        if len(group) > 1:
            variants.append(
                {
                    "variant_id": f"exact_sha256_{sha[:12]}",
                    "kind": "EXACT_DUPLICATE",
                    "merge_gate": "REVIEW_ARCHIVE_ONLY",
                    "files": [item["path"] for item in group],
                    "evidence": "same_sha256",
                }
            )
    for name, group in by_name.items():
        hashes = {str(item.get("sha256") or "") for item in group}
        if len(group) > 1 and len(hashes) > 1:
            variants.append(
                {
                    "variant_id": f"same_name_{_slug(name)}",
                    "kind": "SAME_NAME_DIFFERENT_HASH",
                    "merge_gate": "REVIEW_REQUIRED",
                    "files": [item["path"] for item in group],
                    "evidence": "same_filename_different_hash",
                }
            )
    for stem, group in by_stem.items():
        hashes = {str(item.get("sha256") or "") for item in group}
        if len(group) > 1 and len(hashes) > 1:
            variants.append(
                {
                    "variant_id": f"same_stem_{_slug(stem)}",
                    "kind": "POSSIBLE_CONCEPT_VARIANT",
                    "merge_gate": "REVIEW_REQUIRED",
                    "files": [item["path"] for item in group],
                    "evidence": "normalized_stem_match_different_hash",
                }
            )
    return variants


def _summary(comparisons: list[dict[str, Any]]) -> dict[str, Any]:
    status_counts = Counter(item["semantic_status"] for item in comparisons)
    gate_counts = Counter(item["merge_gate"] for item in comparisons)
    recommendation_counts = Counter(item["recommendation"] for item in comparisons)
    return {
        "variant_group_count": len(comparisons),
        "status_counts": dict(sorted(status_counts.items())),
        "gate_counts": dict(sorted(gate_counts.items())),
        "recommendation_counts": dict(sorted(recommendation_counts.items())),
        "archive_review_candidates": gate_counts.get("REVIEW_ARCHIVE_ONLY", 0),
        "canon_merge_review_candidates": gate_counts.get("REVIEW_CANON_MERGE_CANDIDATE", 0),
        "must_keep_separate_count": gate_counts.get("REVIEW_REQUIRED_NO_MERGE", 0),
    }


def _comparison_markdown(payload: dict[str, Any]) -> str:
    summary = payload["summary"]
    lines = [
        "# VARIANT SEMANTIC COMPARISON",
        "",
        "CERTEZA:",
        "- Generated from manifest records, line-signal excerpts and safe readable text signatures.",
        "- No source file was moved, deleted, merged or rewritten.",
        "",
        "INFERENCIA:",
        "- Similarity is a triage signal, not a canon decision.",
        "",
        "INCOGNITA:",
        "- Binary/DOCX/PDF/archive equality still needs dedicated diff when content matters.",
        "",
        "SUMMARY:",
        f"- Variant groups: `{summary['variant_group_count']}`",
        f"- Archive review candidates: `{summary['archive_review_candidates']}`",
        f"- Canon merge review candidates: `{summary['canon_merge_review_candidates']}`",
        f"- Keep separate / no merge: `{summary['must_keep_separate_count']}`",
        "",
        "| Variant | Semantic status | Gate | Recommendation | Min token | Min signal | Files |",
        "|---|---|---|---|---:|---:|---|",
    ]
    for item in payload.get("comparisons", []):
        files = "<br>".join(f"`{file['path']}`" for file in item.get("files", [])[:6])
        if len(item.get("files", [])) > 6:
            files += f"<br>`... {len(item['files']) - 6} more`"
        lines.append(
            "| `{}` | {} | {} | {} | {:.3f} | {:.3f} | {} |".format(
                item["variant_id"],
                item["semantic_status"],
                item["merge_gate"],
                item["recommendation"],
                item["min_token_similarity"],
                item["min_signal_similarity"],
                files,
            )
        )
    return "\n".join(lines) + "\n"


def _action_record(item: dict[str, Any]) -> dict[str, Any]:
    return {
        "variant_id": item["variant_id"],
        "semantic_status": item["semantic_status"],
        "recommendation": item["recommendation"],
        "merge_gate": item["merge_gate"],
        "canonical_candidate": item["canonical_candidate"],
        "files": [file["path"] for file in item.get("files", [])],
        "next_action": item["next_action"],
    }


def _next_action(status: str) -> str:
    if status == "EXACT_DUPLICATE":
        return "review canonical_candidate, then archive duplicate only with migration log"
    if status == "NEAR_EQUIVALENT":
        return "review excerpts and choose one canon target before merge"
    if status == "FORMAT_OR_ARCHIVE_VARIANT":
        return "run dedicated document/archive diff before any merge"
    if status == "CODE_OR_CONFIG_MATERIAL_DELTA":
        return "run code/config diff and tests before import"
    return "keep separate until semantic delta is manually reviewed"


def _signals_by_path(entries: list[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for entry in entries:
        grouped[str(entry.get("path") or "")].append(entry)
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


def _jaccard(left: set[str], right: set[str]) -> float:
    if not left and not right:
        return 1.0
    union = left | right
    return len(left & right) / len(union) if union else 1.0


def _delta_ratio(left: int, right: int) -> float:
    high = max(left, right)
    if high <= 0:
        return 0.0
    return abs(left - right) / high


def _min(items: list[dict[str, Any]], key: str) -> float:
    if not items:
        return 1.0
    return min(float(item.get(key, 0.0)) for item in items)


def _avg(items: list[dict[str, Any]], key: str) -> float:
    if not items:
        return 1.0
    return sum(float(item.get(key, 0.0)) for item in items) / len(items)


def _round(value: float) -> float:
    return round(float(value), 6)


def _slug(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", value.lower()).strip("_") or "item"


def _normal_stem(stem: str) -> str:
    lowered = stem.lower()
    lowered = re.sub(r"\b(copy|copia|final|nuevo|new|version|v\d+)\b", "", lowered)
    lowered = re.sub(r"[\W_]+", "", lowered)
    return lowered or stem.lower()


def _utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()
