#!/usr/bin/env python3
"""Validate the Observacionismo operational canon seed dataset.

This validator intentionally avoids jsonschema as a hard dependency. It checks
the schema subset used by `schemas/observacionismo_concepts.schema.json`, then
adds project-specific evidence and claim-boundary rules.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_SCHEMA = ROOT / "schemas" / "observacionismo_concepts.schema.json"
DEFAULT_DATASET = ROOT / "data" / "observacionismo" / "concepts_seed.jsonl"
DEFAULT_REPORT_JSON = ROOT / "qa_artifacts" / "observacionismo" / "validate_concepts_report.json"
DEFAULT_REPORT_MD = ROOT / "qa_artifacts" / "observacionismo" / "validate_concepts_report.md"

STATUS_VALUES = {
    "verificado_por_prueba",
    "proxy_operacional",
    "hipotesis",
    "metafora_canon",
}
MATH_CLAIM_TYPES = {"mathematical"}
PRIVATE_PATH_MARKERS = {
    "game-private",
    "metaevo-tcg",
    "/tcg/",
    "\\tcg\\",
    "runtime/game_bridge",
    "runtime\\game_bridge",
}


@dataclass
class ValidationIssue:
    line: int
    concept_id: str
    path: str
    message: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "line": self.line,
            "concept_id": self.concept_id,
            "path": self.path,
            "message": self.message,
        }


@dataclass
class ValidationResult:
    records: list[dict[str, Any]] = field(default_factory=list)
    errors: list[ValidationIssue] = field(default_factory=list)
    warnings: list[ValidationIssue] = field(default_factory=list)
    missing_paths: list[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.errors


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def load_jsonl(path: Path) -> list[tuple[int, dict[str, Any]]]:
    rows: list[tuple[int, dict[str, Any]]] = []
    for line_no, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not raw.strip():
            continue
        try:
            value = json.loads(raw)
        except json.JSONDecodeError as exc:
            raise ValueError(f"{path}:{line_no}: invalid JSON: {exc}") from exc
        if not isinstance(value, dict):
            raise ValueError(f"{path}:{line_no}: JSONL row must be an object")
        rows.append((line_no, value))
    return rows


def _matches_type(value: Any, expected: str) -> bool:
    if expected == "object":
        return isinstance(value, dict)
    if expected == "array":
        return isinstance(value, list)
    if expected == "string":
        return isinstance(value, str)
    if expected == "boolean":
        return isinstance(value, bool)
    if expected == "integer":
        return isinstance(value, int) and not isinstance(value, bool)
    if expected == "number":
        return isinstance(value, (int, float)) and not isinstance(value, bool)
    return True


def validate_schema_node(
    value: Any,
    schema_node: dict[str, Any],
    path: str,
    errors: list[ValidationIssue],
    *,
    line: int,
    concept_id: str,
) -> None:
    expected_type = schema_node.get("type")
    if expected_type and not _matches_type(value, str(expected_type)):
        errors.append(ValidationIssue(line, concept_id, path, f"expected {expected_type}"))
        return

    if "enum" in schema_node and value not in schema_node["enum"]:
        errors.append(ValidationIssue(line, concept_id, path, f"value {value!r} not in enum"))

    if isinstance(value, str):
        min_length = schema_node.get("minLength")
        if isinstance(min_length, int) and len(value) < min_length:
            errors.append(ValidationIssue(line, concept_id, path, f"string shorter than {min_length}"))
        pattern = schema_node.get("pattern")
        if pattern and not re.search(str(pattern), value):
            errors.append(ValidationIssue(line, concept_id, path, f"value does not match pattern {pattern}"))

    if isinstance(value, list):
        min_items = schema_node.get("minItems")
        if isinstance(min_items, int) and len(value) < min_items:
            errors.append(ValidationIssue(line, concept_id, path, f"array shorter than {min_items}"))
        if schema_node.get("uniqueItems") and len(value) != len({json.dumps(item, sort_keys=True) for item in value}):
            errors.append(ValidationIssue(line, concept_id, path, "array items must be unique"))
        item_schema = schema_node.get("items")
        if isinstance(item_schema, dict):
            for index, item in enumerate(value):
                validate_schema_node(
                    item,
                    item_schema,
                    f"{path}[{index}]",
                    errors,
                    line=line,
                    concept_id=concept_id,
                )

    if isinstance(value, dict):
        required = schema_node.get("required") or []
        for key in required:
            if key not in value:
                errors.append(ValidationIssue(line, concept_id, f"{path}.{key}", "missing required field"))
        props = schema_node.get("properties") or {}
        if schema_node.get("additionalProperties") is False:
            for key in value:
                if key not in props:
                    errors.append(ValidationIssue(line, concept_id, f"{path}.{key}", "additional property not allowed"))
        for key, child_schema in props.items():
            if key in value and isinstance(child_schema, dict):
                validate_schema_node(
                    value[key],
                    child_schema,
                    f"{path}.{key}" if path else key,
                    errors,
                    line=line,
                    concept_id=concept_id,
                )


def resolve_path(path_value: str, root: Path) -> Path:
    candidate = Path(path_value)
    if candidate.is_absolute():
        return candidate
    return root / path_value


def has_private_marker(path_value: str) -> bool:
    normalized = path_value.replace("\\", "/").lower()
    return any(marker.replace("\\", "/").lower() in normalized for marker in PRIVATE_PATH_MARKERS)


def validate_concept_rules(record: dict[str, Any], line: int, root: Path, result: ValidationResult) -> None:
    concept_id = str(record.get("concept_id") or "<missing>")
    source_paths = record.get("source_paths") if isinstance(record.get("source_paths"), list) else []
    test_paths = record.get("tests") if isinstance(record.get("tests"), list) else []
    evidence_required = record.get("evidence_required") if isinstance(record.get("evidence_required"), list) else []
    falsifiers = record.get("falsifiers") if isinstance(record.get("falsifiers"), list) else []
    gates = record.get("gates") if isinstance(record.get("gates"), list) else []
    status = str(record.get("status") or "")
    claim_type = str(record.get("claim_type") or "")

    if not source_paths:
        result.errors.append(ValidationIssue(line, concept_id, "source_paths", "at least one source path is required"))
    for source in source_paths:
        if not isinstance(source, str):
            continue
        resolved = resolve_path(source, root)
        if not resolved.exists():
            result.errors.append(ValidationIssue(line, concept_id, "source_paths", f"source path not found: {source}"))
            result.missing_paths.append(source)

    for test_path in test_paths:
        if not isinstance(test_path, str):
            continue
        resolved = resolve_path(test_path, root)
        if not resolved.exists():
            result.errors.append(ValidationIssue(line, concept_id, "tests", f"test path not found: {test_path}"))
            result.missing_paths.append(test_path)

    if not evidence_required:
        result.errors.append(ValidationIssue(line, concept_id, "evidence_required", "evidence requirements are mandatory"))
    if not falsifiers:
        result.errors.append(ValidationIssue(line, concept_id, "falsifiers", "falsifiers are mandatory"))
    if not gates:
        result.errors.append(ValidationIssue(line, concept_id, "gates", "at least one gate is mandatory"))

    if status == "verificado_por_prueba" and not test_paths:
        result.errors.append(ValidationIssue(line, concept_id, "tests", "verified concepts require at least one test path"))

    if status in {"hipotesis", "metafora_canon"}:
        approved = [gate for gate in gates if isinstance(gate, dict) and gate.get("decision") == "APPROVE"]
        if approved:
            result.errors.append(
                ValidationIssue(line, concept_id, "gates", "hypothesis/metaphor concepts cannot have APPROVE gates")
            )

    if claim_type in MATH_CLAIM_TYPES:
        if status not in STATUS_VALUES:
            result.errors.append(ValidationIssue(line, concept_id, "status", "mathematical concept lacks classification"))
        if record.get("public_claim_allowed") and status != "verificado_por_prueba":
            result.errors.append(
                ValidationIssue(line, concept_id, "public_claim_allowed", "mathematical public claim requires verified status")
            )

    if record.get("public_claim_allowed") is True:
        if status != "verificado_por_prueba":
            result.errors.append(
                ValidationIssue(line, concept_id, "public_claim_allowed", "public claims require verificado_por_prueba")
            )
        if len(source_paths) < 2:
            result.errors.append(
                ValidationIssue(line, concept_id, "public_claim_allowed", "public claims require at least two source paths")
            )
        if not test_paths:
            result.errors.append(
                ValidationIssue(line, concept_id, "public_claim_allowed", "public claims require at least one test")
            )
        if any(isinstance(path, str) and has_private_marker(path) for path in source_paths):
            result.errors.append(
                ValidationIssue(line, concept_id, "public_claim_allowed", "public claims cannot cite private/game paths")
            )

    if any(isinstance(path, str) and has_private_marker(path) for path in source_paths):
        result.warnings.append(
            ValidationIssue(line, concept_id, "source_paths", "concept cites private-sensitive path; keep public_claim_allowed=false")
        )


def validate_dataset(schema_path: Path, dataset_path: Path, root: Path = ROOT) -> ValidationResult:
    schema = load_json(schema_path)
    rows = load_jsonl(dataset_path)
    result = ValidationResult()
    seen_ids: set[str] = set()

    for line, record in rows:
        concept_id = str(record.get("concept_id") or "<missing>")
        validate_schema_node(record, schema, "", result.errors, line=line, concept_id=concept_id)
        if concept_id in seen_ids:
            result.errors.append(ValidationIssue(line, concept_id, "concept_id", "duplicate concept_id"))
        seen_ids.add(concept_id)
        validate_concept_rules(record, line, root, result)
        result.records.append(record)

    if len(result.records) < 20:
        result.errors.append(ValidationIssue(0, "<dataset>", "records", "dataset must contain at least 20 concepts"))

    return result


def build_report(result: ValidationResult, schema_path: Path, dataset_path: Path, root: Path) -> dict[str, Any]:
    status_counts = Counter(str(row.get("status") or "<missing>") for row in result.records)
    layer_counts = Counter(str(row.get("layer") or "<missing>") for row in result.records)
    claim_counts = Counter(str(row.get("claim_type") or "<missing>") for row in result.records)
    return {
        "schema": "observacionismo.concepts.validation_report.v1",
        "generated_at_utc": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "ok": result.ok,
        "root": str(root),
        "schema_path": str(schema_path),
        "dataset_path": str(dataset_path),
        "concept_count": len(result.records),
        "public_claim_allowed_count": sum(1 for row in result.records if row.get("public_claim_allowed") is True),
        "status_counts": dict(sorted(status_counts.items())),
        "layer_counts": dict(sorted(layer_counts.items())),
        "claim_type_counts": dict(sorted(claim_counts.items())),
        "errors": [issue.to_dict() for issue in result.errors],
        "warnings": [issue.to_dict() for issue in result.warnings],
        "missing_paths": sorted(set(result.missing_paths)),
        "concept_ids": [str(row.get("concept_id")) for row in result.records],
    }


def write_markdown_report(report: dict[str, Any], path: Path) -> None:
    lines = [
        "# Observacionismo Concepts Validation Report",
        "",
        f"Generated UTC: `{report['generated_at_utc']}`",
        f"OK: `{str(report['ok']).lower()}`",
        f"Concepts: `{report['concept_count']}`",
        f"Public claims allowed: `{report['public_claim_allowed_count']}`",
        "",
        "## Status Counts",
        "",
    ]
    for key, value in report["status_counts"].items():
        lines.append(f"- `{key}`: {value}")
    lines.extend(["", "## Errors", ""])
    if report["errors"]:
        for issue in report["errors"]:
            lines.append(f"- line {issue['line']} `{issue['concept_id']}` `{issue['path']}`: {issue['message']}")
    else:
        lines.append("- none")
    lines.extend(["", "## Warnings", ""])
    if report["warnings"]:
        for issue in report["warnings"]:
            lines.append(f"- line {issue['line']} `{issue['concept_id']}` `{issue['path']}`: {issue['message']}")
    else:
        lines.append("- none")
    lines.extend(["", "## Concept IDs", ""])
    for concept_id in report["concept_ids"]:
        lines.append(f"- `{concept_id}`")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate Observacionismo operational concept records.")
    parser.add_argument("--schema", default=str(DEFAULT_SCHEMA))
    parser.add_argument("--dataset", default=str(DEFAULT_DATASET))
    parser.add_argument("--root", default=str(ROOT))
    parser.add_argument("--report-json", default=str(DEFAULT_REPORT_JSON))
    parser.add_argument("--report-md", default=str(DEFAULT_REPORT_MD))
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    schema_path = Path(args.schema)
    dataset_path = Path(args.dataset)
    root = Path(args.root)
    report_json_path = Path(args.report_json)
    report_md_path = Path(args.report_md)

    try:
        result = validate_dataset(schema_path, dataset_path, root=root)
    except Exception as exc:  # noqa: BLE001 - CLI needs a concise failure report.
        print(json.dumps({"ok": False, "error": str(exc)}, ensure_ascii=False, indent=2))
        return 1

    report = build_report(result, schema_path, dataset_path, root)
    report_json_path.parent.mkdir(parents=True, exist_ok=True)
    report_json_path.write_text(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    write_markdown_report(report, report_md_path)

    print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if result.ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
