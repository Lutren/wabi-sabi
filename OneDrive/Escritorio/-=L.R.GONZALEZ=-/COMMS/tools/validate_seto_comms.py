from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
ALLOWED_PSI = {"CERTEZA", "INFERENCIA", "INCOGNITA", "BLOQUEADO"}
ALLOWED_GATES = {"APPROVE", "REVIEW", "BLOCK"}
HASH_RE = re.compile(r"^[A-Fa-f0-9]{64}$")

SCHEMA_PATHS = [
    ROOT / "COMMS" / "schemas" / "observation-envelope.schema.json",
    ROOT / "COMMS" / "schemas" / "action-gate.schema.json",
    ROOT / "COMMS" / "schemas" / "witness-log-event.schema.json",
]
INBOX_PATH = ROOT / "COMMS" / "inbox" / "claudio-local-agent.jsonl"
OUTBOX_PATH = ROOT / "COMMS" / "outbox" / "claudio-local-agent.jsonl"
TOPIC_PATH = ROOT / "COMMS" / "topics" / "seto-observacionismo-decisions.jsonl"
DECISION_EXAMPLES = (
    ROOT
    / "qa_artifacts"
    / "release_validation"
    / "seto-observacionismo-decision-examples-2026-05-05.jsonl"
)
WITNESS_LOG = ROOT / "qa_artifacts" / "witness_log" / "curador_seto_witnesslog.jsonl"


def rel(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT.resolve()).as_posix()
    except ValueError:
        return path.resolve().as_posix()


def sha256_file(path: Path, chunk_size: int = 1024 * 1024) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(chunk_size), b""):
            digest.update(chunk)
    return digest.hexdigest()


def print_json(data: object) -> None:
    print(json.dumps(data, indent=2, ensure_ascii=False))


def read_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as fh:
        value = json.load(fh)
    if not isinstance(value, dict):
        raise ValueError(f"{rel(path)} must be a JSON object")
    return value


def iter_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as fh:
        for line_no, line in enumerate(fh, 1):
            text = line.strip()
            if not text:
                continue
            value = json.loads(text)
            if not isinstance(value, dict):
                raise ValueError(f"{rel(path)}:{line_no} must be a JSON object")
            rows.append(value)
    return rows


def require(condition: bool, errors: list[str], message: str) -> None:
    if not condition:
        errors.append(message)


def validate_envelope(envelope: dict[str, Any], label: str, errors: list[str]) -> None:
    required = {
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
    missing = sorted(required - set(envelope))
    require(not missing, errors, f"{label} missing keys: {missing}")
    require(envelope.get("envelope_version") == "seto-observation-v1", errors, f"{label} bad envelope_version")
    require(envelope.get("psi_state") in ALLOWED_PSI, errors, f"{label} bad psi_state: {envelope.get('psi_state')}")
    require(envelope.get("action_gate") in ALLOWED_GATES, errors, f"{label} bad action_gate: {envelope.get('action_gate')}")
    sha = envelope.get("sha256")
    if sha is not None:
        require(isinstance(sha, str) and HASH_RE.match(sha) is not None, errors, f"{label} bad sha256")
    require(isinstance(envelope.get("evidence"), list) and len(envelope.get("evidence", [])) > 0, errors, f"{label} missing evidence")


def validate_decision_example(row: dict[str, Any], label: str, errors: list[str]) -> None:
    require(row.get("psi_state") in ALLOWED_PSI, errors, f"{label} bad psi_state: {row.get('psi_state')}")
    require(row.get("action_gate") in ALLOWED_GATES, errors, f"{label} bad action_gate: {row.get('action_gate')}")
    require(bool(row.get("case_id")), errors, f"{label} missing case_id")
    require(isinstance(row.get("falsifiers"), list), errors, f"{label} falsifiers must be list")


def validate_witness_tail(errors: list[str]) -> dict[str, Any]:
    lines = [line.strip() for line in WITNESS_LOG.read_text(encoding="utf-8").splitlines() if line.strip()]
    require(bool(lines), errors, "WitnessLog is empty")
    if not lines:
        return {"checked": False}
    event = json.loads(lines[-1])
    require(isinstance(event, dict), errors, "WitnessLog tail is not object")
    expected = event.get("event_hash")
    require(isinstance(expected, str) and HASH_RE.match(expected) is not None, errors, "WitnessLog tail bad event_hash")
    event_without_hash = dict(event)
    event_without_hash.pop("event_hash", None)
    encoded = json.dumps(event_without_hash, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    actual = hashlib.sha256(encoded).hexdigest()
    require(expected == actual, errors, f"WitnessLog tail hash mismatch: expected {expected} actual {actual}")
    require(event.get("action_gate") in ALLOWED_GATES, errors, f"WitnessLog tail bad action_gate: {event.get('action_gate')}")
    return {"checked": True, "event_type": event.get("event_type"), "event_hash": expected, "hash_match": expected == actual}


def validate() -> dict[str, Any]:
    errors: list[str] = []
    warnings: list[str] = []
    schema_hashes: dict[str, str] = {}
    for path in SCHEMA_PATHS:
        schema = read_json(path)
        require(schema.get("$schema") == "https://json-schema.org/draft/2020-12/schema", errors, f"{rel(path)} wrong draft")
        require(bool(schema.get("required")), errors, f"{rel(path)} missing required list")
        schema_hashes[rel(path)] = sha256_file(path)

    inbox_rows = iter_jsonl(INBOX_PATH)
    for idx, row in enumerate(inbox_rows, 1):
        envelope = row.get("observation_envelope")
        require(isinstance(envelope, dict), errors, f"{rel(INBOX_PATH)}:{idx} missing observation_envelope")
        if isinstance(envelope, dict):
            validate_envelope(envelope, f"{rel(INBOX_PATH)}:{idx}", errors)

    outbox_rows = iter_jsonl(OUTBOX_PATH)
    for idx, row in enumerate(outbox_rows, 1):
        envelope = row.get("observation_envelope")
        require(isinstance(envelope, dict), errors, f"{rel(OUTBOX_PATH)}:{idx} missing observation_envelope")
        if isinstance(envelope, dict):
            validate_envelope(envelope, f"{rel(OUTBOX_PATH)}:{idx}", errors)

    topic_rows = iter_jsonl(TOPIC_PATH)
    topic_has_envelope = False
    legacy_topic_rows: list[str] = []
    for idx, row in enumerate(topic_rows, 1):
        gate = row.get("action_gate")
        if gate is not None:
            require(gate in ALLOWED_GATES, errors, f"{rel(TOPIC_PATH)}:{idx} bad action_gate: {gate}")
        require(bool(row.get("decision")), errors, f"{rel(TOPIC_PATH)}:{idx} missing decision")
        envelope = row.get("observation_envelope")
        if isinstance(envelope, dict):
            topic_has_envelope = True
            validate_envelope(envelope, f"{rel(TOPIC_PATH)}:{idx}", errors)
        else:
            legacy_topic_rows.append(f"{rel(TOPIC_PATH)}:{idx}")
    if legacy_topic_rows and not topic_has_envelope:
        warnings.append(f"{rel(TOPIC_PATH)} has legacy topics without observation_envelope")

    example_rows = iter_jsonl(DECISION_EXAMPLES)
    for idx, row in enumerate(example_rows, 1):
        validate_decision_example(row, f"{rel(DECISION_EXAMPLES)}:{idx}", errors)

    witness_tail = validate_witness_tail(errors)

    return {
        "schema": "medioevo.seto_comms_validator_result.v1",
        "status": "PASS" if not errors else "FAIL",
        "errors": errors,
        "warnings": warnings,
        "counts": {
            "schemas": len(SCHEMA_PATHS),
            "inbox_messages": len(inbox_rows),
            "outbox_messages": len(outbox_rows),
            "topic_events": len(topic_rows),
            "decision_examples": len(example_rows),
        },
        "schema_hashes": schema_hashes,
        "witness_tail": witness_tail,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate SETO COMMS contract artifacts.")
    parser.add_argument("--json", action="store_true", help="Print JSON output.")
    parser.add_argument("--fail-on-errors", action="store_true", help="Exit non-zero if validation fails.")
    args = parser.parse_args()
    result = validate()
    if args.json:
        print_json(result)
    else:
        print(f"status={result['status']} errors={len(result['errors'])}")
    if args.fail_on_errors and result["errors"]:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
