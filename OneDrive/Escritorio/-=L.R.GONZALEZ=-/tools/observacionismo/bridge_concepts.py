#!/usr/bin/env python3
"""Build the Observacionismo canon bridge into COMMS, L1 and ActionGate.

This tool does not promote theory into public claims. It takes concept records
that already pass `validate_concepts.py` and emits local-only bridge artifacts:

- COMMS-compatible ObservationEnvelope objects;
- conservative L1 lowering plans using the five L1 verbs;
- ActionGate payloads that keep external/destructive/public actions blocked.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
TOOLS_DIR = Path(__file__).resolve().parent
if str(TOOLS_DIR) not in sys.path:
    sys.path.insert(0, str(TOOLS_DIR))

from validate_concepts import (  # noqa: E402
    DEFAULT_DATASET,
    DEFAULT_SCHEMA,
    has_private_marker,
    validate_dataset,
)


DEFAULT_REPORT_JSON = ROOT / "qa_artifacts" / "observacionismo" / "bridge_concepts_report.json"
DEFAULT_REPORT_MD = ROOT / "qa_artifacts" / "observacionismo" / "bridge_concepts_report.md"
DEFAULT_COMMS_TOPIC = ROOT / "COMMS" / "topics" / "seto-observacionismo-decisions.jsonl"
DEFAULT_WITNESS_LOG = ROOT / "qa_artifacts" / "witness_log" / "curador_seto_witnesslog.jsonl"

COMMS_ENVELOPE_VERSION = "seto-observation-v1"
L1_VERB_SEQUENCE = ["OBSERVAR", "DOCUMENTAR", "VERIFICAR", "ACTUAR", "HANDOFF"]
L1_SAFE_SCRIPT = [
    "OBSERVAR bit 0",
    "DOCUMENTAR bit 0",
    "VERIFICAR halted == true",
    "ACTUAR nop",
    "HANDOFF",
]

STATUS_TO_PSI = {
    "verificado_por_prueba": "CERTEZA",
    "proxy_operacional": "INFERENCIA",
    "hipotesis": "INCOGNITA",
    "metafora_canon": "INCOGNITA",
}
COMMS_REQUIRED = {
    "envelope_version",
    "source_path",
    "source_kind",
    "evidence",
    "psi_state",
    "claim_level",
    "falsifiers",
    "risk_flags",
    "action_gate",
    "decision",
    "fingerprint",
}
COMMS_ALLOWED_SOURCE_KINDS = {
    "file",
    "directory",
    "zip",
    "repo",
    "generated_artifact",
    "external_note",
    "coordination_contract",
    "handoff_contract",
    "topic_event",
}
COMMS_ALLOWED_CLAIM_LEVELS = {"operational", "research_only", "demo_only", "blocked_claim"}
COMMS_ALLOWED_GATES = {"APPROVE", "REVIEW", "BLOCK"}


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def canonical_json(payload: Any) -> str:
    return json.dumps(payload, ensure_ascii=True, sort_keys=True, separators=(",", ":"))


def fingerprint(prefix: str, payload: Any, length: int = 16) -> str:
    digest = hashlib.sha256(canonical_json(payload).encode("utf-8")).hexdigest()[:length].upper()
    return f"{prefix}_{digest}"


def sha256_file(path: Path, chunk_size: int = 1024 * 1024) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(chunk_size), b""):
            digest.update(chunk)
    return digest.hexdigest()


def rel(path: Path, root: Path = ROOT) -> str:
    try:
        return path.resolve().relative_to(root.resolve()).as_posix()
    except ValueError:
        return path.resolve().as_posix()


def concept_evidence(record: dict[str, Any]) -> list[str]:
    evidence: list[str] = []
    for path in record.get("source_paths") or []:
        if isinstance(path, str) and path.strip():
            evidence.append(f"source:{path}")
    for path in record.get("tests") or []:
        if isinstance(path, str) and path.strip():
            evidence.append(f"test:{path}")
    for item in record.get("evidence_required") or []:
        if isinstance(item, str) and item.strip():
            evidence.append(f"required:{item}")
    return evidence


def concept_has_private_source(record: dict[str, Any]) -> bool:
    return any(isinstance(path, str) and has_private_marker(path) for path in record.get("source_paths") or [])


def risk_flags(record: dict[str, Any]) -> list[str]:
    flags = ["no_public_claim", "local_only"]
    status = str(record.get("status") or "")
    claim_type = str(record.get("claim_type") or "")

    if status != "verificado_por_prueba":
        flags.append(f"status_{status}")
    if claim_type == "mathematical":
        flags.append("mathematical_proxy_claim")
    if status in {"hipotesis", "metafora_canon"}:
        flags.append("review_only_concept")
    if not record.get("tests"):
        flags.append("no_test_path")
    if concept_has_private_source(record):
        flags.append("private_boundary")
    if record.get("public_claim_allowed") is not True:
        flags.append("public_claim_blocked")

    return sorted(set(flags))


def claim_level(record: dict[str, Any]) -> str:
    status = str(record.get("status") or "")
    claim_type = str(record.get("claim_type") or "")

    if record.get("public_claim_allowed") is True and status != "verificado_por_prueba":
        return "blocked_claim"
    if claim_type == "gameplay":
        return "demo_only"
    if status in {"hipotesis", "metafora_canon"}:
        return "research_only"
    if claim_type == "mathematical":
        return "research_only"
    if claim_type in {"protocol", "evidence", "language", "runtime", "gate", "orchestration"}:
        return "operational"
    return "research_only"


def recommended_gate(record: dict[str, Any]) -> str:
    status = str(record.get("status") or "")
    claim_type = str(record.get("claim_type") or "")

    if record.get("public_claim_allowed") is True and status != "verificado_por_prueba":
        return "BLOCK"
    if concept_has_private_source(record) and record.get("public_claim_allowed") is True:
        return "BLOCK"
    if status in {"hipotesis", "metafora_canon"}:
        return "REVIEW"
    if claim_type == "mathematical":
        return "REVIEW"
    if status == "verificado_por_prueba" and record.get("tests"):
        return "APPROVE"
    return "REVIEW"


def bridge_decision(record: dict[str, Any]) -> str:
    gate = recommended_gate(record)
    if gate == "APPROVE":
        return "APPROVE_LOCAL_CANON_BRIDGE_NO_EXTERNAL_ACTION"
    if gate == "BLOCK":
        return "BLOCK_PUBLIC_OR_UNEVIDENCED_CLAIM"
    return "REVIEW_LOCAL_CANON_BRIDGE_NO_PUBLIC_CLAIM"


def build_observation_envelope(record: dict[str, Any], dataset_path: Path, root: Path) -> dict[str, Any]:
    gate = recommended_gate(record)
    envelope: dict[str, Any] = {
        "envelope_version": COMMS_ENVELOPE_VERSION,
        "source_path": rel(dataset_path, root),
        "source_kind": "generated_artifact",
        "sha256": sha256_file(dataset_path),
        "size_bytes": dataset_path.stat().st_size,
        "evidence": concept_evidence(record),
        "psi_state": STATUS_TO_PSI.get(str(record.get("status") or ""), "INCOGNITA"),
        "claim_level": claim_level(record),
        "falsifiers": [str(item) for item in record.get("falsifiers") or []],
        "risk_flags": risk_flags(record),
        "action_gate": gate,
        "decision": bridge_decision(record),
    }
    envelope["fingerprint"] = fingerprint(
        "OBS_CANON_ENV",
        {
            "concept_id": record.get("concept_id"),
            "source_path": envelope["source_path"],
            "sha256": envelope["sha256"],
            "status": record.get("status"),
            "claim_level": envelope["claim_level"],
            "action_gate": gate,
        },
    )
    return envelope


def build_l1_bridge(record: dict[str, Any]) -> dict[str, Any]:
    status = str(record.get("status") or "")
    lowering_status = "review_only"
    if status in {"verificado_por_prueba", "proxy_operacional"}:
        lowering_status = "safe_l1_plan"

    return {
        "schema": "observacionismo.l1_bridge_plan.v1",
        "concept_id": record.get("concept_id"),
        "verb_sequence": L1_VERB_SEQUENCE,
        "script": L1_SAFE_SCRIPT,
        "lowering_status": lowering_status,
        "field_mapping": {
            "OBSERVAR": "inputs + source_paths",
            "DOCUMENTAR": "outputs + evidence_required",
            "VERIFICAR": "falsifiers + tests",
            "ACTUAR": "gates through ActionGate only",
            "HANDOFF": "COMMS ObservationEnvelope + WitnessLog",
        },
        "notes": [
            "L1 plan is a local bridge contract, not publication permission.",
            "ACTUAR remains nop until ActionGate approves a concrete action.",
        ],
    }


def build_action_gate_payload(record: dict[str, Any]) -> dict[str, Any]:
    return {
        "decision": recommended_gate(record),
        "risk_flags": risk_flags(record),
        "required_evidence": concept_evidence(record),
        "no_delete": True,
        "no_move": True,
        "no_external_action": True,
        "no_write_to_concurrent_lane": True,
        "requires_hash_refresh_before_future_action": True,
        "requires_canonical_replacement_or_keep_decision": str(record.get("status") or "") != "verificado_por_prueba",
        "post_validation": [
            "python tools/observacionismo/validate_concepts.py",
            "python tools/observacionismo/bridge_concepts.py",
        ],
    }


def validate_comms_envelope(envelope: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    missing = sorted(COMMS_REQUIRED - set(envelope))
    if missing:
        errors.append(f"missing envelope keys: {missing}")
    if envelope.get("envelope_version") != COMMS_ENVELOPE_VERSION:
        errors.append("bad envelope_version")
    if envelope.get("source_kind") not in COMMS_ALLOWED_SOURCE_KINDS:
        errors.append(f"bad source_kind: {envelope.get('source_kind')}")
    if envelope.get("claim_level") not in COMMS_ALLOWED_CLAIM_LEVELS:
        errors.append(f"bad claim_level: {envelope.get('claim_level')}")
    if envelope.get("action_gate") not in COMMS_ALLOWED_GATES:
        errors.append(f"bad action_gate: {envelope.get('action_gate')}")
    if not isinstance(envelope.get("evidence"), list) or not envelope.get("evidence"):
        errors.append("missing evidence")
    if not isinstance(envelope.get("falsifiers"), list):
        errors.append("falsifiers must be list")
    return errors


def validate_l1_bridge(plan: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if plan.get("verb_sequence") != L1_VERB_SEQUENCE:
        errors.append("bad L1 verb sequence")
    script = plan.get("script")
    if not isinstance(script, list) or len(script) != len(L1_SAFE_SCRIPT):
        errors.append("bad L1 script")
    else:
        observed_verbs = [str(line).split()[0].upper() for line in script if str(line).strip()]
        if observed_verbs != L1_VERB_SEQUENCE:
            errors.append(f"L1 script verbs do not match bridge sequence: {observed_verbs}")
    return errors


def build_bridge_records(records: list[dict[str, Any]], dataset_path: Path, root: Path) -> tuple[list[dict[str, Any]], list[str]]:
    bridge_records: list[dict[str, Any]] = []
    errors: list[str] = []

    for record in records:
        concept_id = str(record.get("concept_id") or "<missing>")
        envelope = build_observation_envelope(record, dataset_path, root)
        l1_bridge = build_l1_bridge(record)
        action_gate_payload = build_action_gate_payload(record)

        for error in validate_comms_envelope(envelope):
            errors.append(f"{concept_id}: {error}")
        for error in validate_l1_bridge(l1_bridge):
            errors.append(f"{concept_id}: {error}")
        if action_gate_payload.get("decision") not in COMMS_ALLOWED_GATES:
            errors.append(f"{concept_id}: bad ActionGate decision")
        if record.get("public_claim_allowed") is True and action_gate_payload.get("decision") == "APPROVE":
            errors.append(f"{concept_id}: public claim cannot auto-approve from bridge")

        bridge_records.append(
            {
                "concept_id": concept_id,
                "name": record.get("name"),
                "status": record.get("status"),
                "claim_type": record.get("claim_type"),
                "public_claim_allowed": record.get("public_claim_allowed"),
                "observation_envelope": envelope,
                "l1_bridge": l1_bridge,
                "action_gate_payload": action_gate_payload,
            }
        )

    return bridge_records, errors


def build_bridge_fingerprint(schema_path: Path, dataset_path: Path, concept_ids: list[str]) -> str:
    return fingerprint(
        "OBS_CANON_BRIDGE",
        {
            "schema_sha256": sha256_file(schema_path),
            "dataset_sha256": sha256_file(dataset_path),
            "bridge_tool_sha256": sha256_file(Path(__file__).resolve()),
            "concept_ids": concept_ids,
        },
    )


def build_report(
    records: list[dict[str, Any]],
    bridge_records: list[dict[str, Any]],
    validation_errors: list[dict[str, Any]],
    validation_warnings: list[dict[str, Any]],
    bridge_errors: list[str],
    schema_path: Path,
    dataset_path: Path,
    root: Path,
    *,
    write_comms_topic: bool,
    append_witness_event: bool,
) -> dict[str, Any]:
    gates = Counter(row["observation_envelope"]["action_gate"] for row in bridge_records)
    psi = Counter(row["observation_envelope"]["psi_state"] for row in bridge_records)
    claim_levels = Counter(row["observation_envelope"]["claim_level"] for row in bridge_records)
    l1_status = Counter(row["l1_bridge"]["lowering_status"] for row in bridge_records)
    concept_ids = [str(row.get("concept_id")) for row in records]

    return {
        "schema": "observacionismo.canon_bridge_report.v1",
        "generated_at_utc": utc_now(),
        "ok": not validation_errors and not bridge_errors,
        "root": str(root),
        "schema_path": rel(schema_path, root),
        "dataset_path": rel(dataset_path, root),
        "bridge_fingerprint": build_bridge_fingerprint(schema_path, dataset_path, concept_ids),
        "concept_count": len(records),
        "public_claim_allowed_count": sum(1 for row in records if row.get("public_claim_allowed") is True),
        "counts": {
            "action_gate": dict(sorted(gates.items())),
            "psi_state": dict(sorted(psi.items())),
            "claim_level": dict(sorted(claim_levels.items())),
            "l1_lowering_status": dict(sorted(l1_status.items())),
        },
        "validation_errors": validation_errors,
        "validation_warnings": validation_warnings,
        "bridge_errors": bridge_errors,
        "write_comms_topic_requested": write_comms_topic,
        "append_witness_event_requested": append_witness_event,
        "bridge_records": bridge_records,
    }


def write_markdown_report(report: dict[str, Any], path: Path) -> None:
    lines = [
        "# Observacionismo Canon Bridge Report",
        "",
        f"Generated UTC: `{report['generated_at_utc']}`",
        f"OK: `{str(report['ok']).lower()}`",
        f"Fingerprint: `{report['bridge_fingerprint']}`",
        f"Concepts: `{report['concept_count']}`",
        f"Public claims allowed: `{report['public_claim_allowed_count']}`",
        "",
        "## Counts",
        "",
    ]
    for group, values in report["counts"].items():
        lines.append(f"### {group}")
        for key, value in values.items():
            lines.append(f"- `{key}`: {value}")
        lines.append("")

    lines.extend(["## Bridge Rules", ""])
    lines.extend(
        [
            "- COMMS uses `ObservationEnvelope` with `source_kind=generated_artifact`.",
            "- L1 uses the five-verb safe bridge plan and keeps `ACTUAR` as `nop`.",
            "- ActionGate keeps `no_external_action=true`, `no_delete=true` and `no_move=true`.",
            "- `public_claim_allowed=false` remains the default boundary.",
            "",
            "## Errors",
            "",
        ]
    )
    if report["validation_errors"] or report["bridge_errors"]:
        for issue in report["validation_errors"]:
            lines.append(f"- validation `{issue.get('concept_id')}` `{issue.get('path')}`: {issue.get('message')}")
        for issue in report["bridge_errors"]:
            lines.append(f"- bridge: {issue}")
    else:
        lines.append("- none")

    lines.extend(["", "## Warnings", ""])
    if report["validation_warnings"]:
        for issue in report["validation_warnings"]:
            lines.append(f"- `{issue.get('concept_id')}` `{issue.get('path')}`: {issue.get('message')}")
    else:
        lines.append("- none")

    lines.extend(["", "## Concept Bridge Table", ""])
    lines.append("| Concept | Status | Claim | PSI | Claim level | Gate | L1 |")
    lines.append("|---|---|---|---|---|---|---|")
    for row in report["bridge_records"]:
        envelope = row["observation_envelope"]
        l1_bridge = row["l1_bridge"]
        lines.append(
            "| `{}` | `{}` | `{}` | `{}` | `{}` | `{}` | `{}` |".format(
                row["concept_id"],
                row["status"],
                row["claim_type"],
                envelope["psi_state"],
                envelope["claim_level"],
                envelope["action_gate"],
                l1_bridge["lowering_status"],
            )
        )

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def build_topic_event(report: dict[str, Any], report_path: Path, root: Path) -> dict[str, Any]:
    bridge_fingerprint = str(report["bridge_fingerprint"])
    envelope_payload = {
        "bridge_fingerprint": bridge_fingerprint,
        "report_path": rel(report_path, root),
        "concept_count": report["concept_count"],
        "ok": report["ok"],
    }
    envelope = {
        "envelope_version": COMMS_ENVELOPE_VERSION,
        "source_path": rel(report_path, root),
        "source_kind": "generated_artifact",
        "evidence": [
            rel(DEFAULT_SCHEMA, root),
            rel(DEFAULT_DATASET, root),
            rel(Path(__file__).resolve(), root),
            rel(report_path, root),
        ],
        "psi_state": "CERTEZA" if report["ok"] else "BLOQUEADO",
        "claim_level": "operational" if report["ok"] else "blocked_claim",
        "falsifiers": [
            "concept validator fails",
            "bridge emits non-COMMS envelope",
            "public claim is enabled without verified evidence",
        ],
        "risk_flags": ["local_only", "no_public_claim", "no_external_action"],
        "action_gate": "REVIEW" if report["ok"] else "BLOCK",
        "decision": "CONNECT_OBS_CANON_TO_COMMS_L1_ACTIONGATE_LOCAL_ONLY",
        "fingerprint": fingerprint("OBS_CANON_TOPIC_ENV", envelope_payload),
    }
    return {
        "topic_event_id": fingerprint("OBS_CANON_TOPIC", envelope_payload),
        "timestamp_utc": utc_now(),
        "sender": "observacionismo-canon-bridge",
        "topic": "seto-observacionismo-decisions",
        "status": "PUBLISHED_LOCAL_TOPIC" if report["ok"] else "BLOCKED_BRIDGE_REPORT",
        "summary": {
            "bridge_fingerprint": bridge_fingerprint,
            "concept_count": report["concept_count"],
            "public_claim_allowed_count": report["public_claim_allowed_count"],
            "report_path": rel(report_path, root),
        },
        "action_gate": envelope["action_gate"],
        "decision": envelope["decision"],
        "observation_envelope": envelope,
    }


def append_jsonl_once(path: Path, row: dict[str, Any], token: str) -> bool:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and token in path.read_text(encoding="utf-8"):
        return False
    with path.open("a", encoding="utf-8", newline="\n") as fh:
        fh.write(json.dumps(row, ensure_ascii=False) + "\n")
    return True


def find_jsonl_row_with_token(path: Path, token: str) -> dict[str, Any] | None:
    if not path.exists():
        return None
    for raw in path.read_text(encoding="utf-8").splitlines():
        if token not in raw:
            continue
        try:
            value = json.loads(raw)
        except json.JSONDecodeError:
            continue
        if isinstance(value, dict):
            return value
    return None


def event_hash(event_without_hash: dict[str, Any]) -> str:
    encoded = json.dumps(event_without_hash, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def last_event_hash(path: Path) -> str:
    if not path.exists():
        return "0" * 64
    for raw in reversed(path.read_text(encoding="utf-8").splitlines()):
        if not raw.strip():
            continue
        try:
            value = json.loads(raw)
        except json.JSONDecodeError:
            break
        previous = value.get("event_hash")
        if isinstance(previous, str) and len(previous) == 64:
            return previous
        break
    return "0" * 64


def build_witness_event(report: dict[str, Any], report_json: Path, report_md: Path, witness_path: Path, root: Path) -> dict[str, Any]:
    event: dict[str, Any] = {
        "action_gate": "REVIEW" if report["ok"] else "BLOCK",
        "actor": "tools/observacionismo/bridge_concepts.py",
        "artifact_hashes": {
            "schema": sha256_file(DEFAULT_SCHEMA),
            "dataset": sha256_file(DEFAULT_DATASET),
            "bridge_tool": sha256_file(Path(__file__).resolve()),
        },
        "event_type": "observacionismo_canon_bridge_v0_1",
        "outputs": {
            "report_json": rel(report_json, root),
            "report_md": rel(report_md, root),
            "topic": rel(DEFAULT_COMMS_TOPIC, root),
        },
        "previous_hash": last_event_hash(witness_path),
        "rules": [
            "append-only witness event",
            "no public claims",
            "no external action",
            "no delete",
            "no move",
        ],
        "status": "LOCAL_BRIDGE_REVIEW_NO_EXTERNAL_ACTION" if report["ok"] else "BRIDGE_BLOCKED",
        "summary": {
            "bridge_fingerprint": report["bridge_fingerprint"],
            "concept_count": report["concept_count"],
            "public_claim_allowed_count": report["public_claim_allowed_count"],
            "bridge_errors": len(report["bridge_errors"]),
            "validation_errors": len(report["validation_errors"]),
        },
        "timestamp_utc": utc_now(),
    }
    event["event_hash"] = event_hash(event)
    return event


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Bridge Observacionismo concepts to COMMS, L1 and ActionGate.")
    parser.add_argument("--schema", default=str(DEFAULT_SCHEMA))
    parser.add_argument("--dataset", default=str(DEFAULT_DATASET))
    parser.add_argument("--root", default=str(ROOT))
    parser.add_argument("--report-json", default=str(DEFAULT_REPORT_JSON))
    parser.add_argument("--report-md", default=str(DEFAULT_REPORT_MD))
    parser.add_argument("--write-comms-topic", action="store_true")
    parser.add_argument("--append-witness-event", action="store_true")
    parser.add_argument("--comms-topic", default=str(DEFAULT_COMMS_TOPIC))
    parser.add_argument("--witness-log", default=str(DEFAULT_WITNESS_LOG))
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    root = Path(args.root)
    schema_path = Path(args.schema)
    dataset_path = Path(args.dataset)
    report_json_path = Path(args.report_json)
    report_md_path = Path(args.report_md)
    comms_topic_path = Path(args.comms_topic)
    witness_log_path = Path(args.witness_log)

    validation = validate_dataset(schema_path, dataset_path, root=root)
    bridge_records, bridge_errors = build_bridge_records(validation.records, dataset_path, root)
    report = build_report(
        validation.records,
        bridge_records,
        [issue.to_dict() for issue in validation.errors],
        [issue.to_dict() for issue in validation.warnings],
        bridge_errors,
        schema_path,
        dataset_path,
        root,
        write_comms_topic=args.write_comms_topic,
        append_witness_event=args.append_witness_event,
    )

    report_json_path.parent.mkdir(parents=True, exist_ok=True)
    report_json_path.write_text(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    write_markdown_report(report, report_md_path)

    if args.write_comms_topic:
        topic_event = build_topic_event(report, report_json_path, root)
        appended = append_jsonl_once(comms_topic_path, topic_event, topic_event["topic_event_id"])
        report["comms_topic_event"] = {
            "path": rel(comms_topic_path, root),
            "topic_event_id": topic_event["topic_event_id"],
            "appended": appended,
        }

    if args.append_witness_event:
        # Re-write report with COMMS topic metadata before hashing it into the witness event.
        report_json_path.write_text(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        write_markdown_report(report, report_md_path)
        witness_event = build_witness_event(report, report_json_path, report_md_path, witness_log_path, root)
        appended = append_jsonl_once(witness_log_path, witness_event, str(report["bridge_fingerprint"]))
        existing_witness_event = find_jsonl_row_with_token(witness_log_path, str(report["bridge_fingerprint"]))
        event_hash_value = witness_event["event_hash"]
        if isinstance(existing_witness_event, dict) and isinstance(existing_witness_event.get("event_hash"), str):
            event_hash_value = existing_witness_event["event_hash"]
        report["witness_event"] = {
            "path": rel(witness_log_path, root),
            "event_hash": event_hash_value,
            "appended": appended,
        }

    # Final write includes append metadata. The witness event hashes the previous
    # report version; the event itself is append-only evidence, not report input.
    report_json_path.write_text(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    write_markdown_report(report, report_md_path)

    print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
