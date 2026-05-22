from __future__ import annotations

import datetime as dt
import hashlib
import json
from pathlib import Path
from typing import Any

from wabi_sabi.core.tools import write_artifact


COMMS_APPEND_PLAN_SCHEMA = "wabi.comms_append_plan.v0_1"


def build_comms_append_plan(
    *,
    portfolio_root: str | Path,
    decision_record: dict[str, Any],
    sender: str = "wabi-sabi-sentido-comun",
    recipient: str = "curador-seto,hormiguero-mission-control,wabi-sabi-sentido-comun",
) -> dict[str, Any]:
    root = Path(portfolio_root).resolve()
    timestamp = _utc_now()
    action_gate = _action_gate(decision_record)
    record_hash = str(decision_record.get("record_hash") or "")
    source_path = str(decision_record.get("evidence_refs", ["wabi_decision_record"])[0])
    message_id = f"{sender}-decisionlog-{record_hash[:16].lower() or _short_hash(timestamp)}"
    envelope = {
        "envelope_version": "seto-observation-v1",
        "source_path": source_path,
        "source_kind": "generated_artifact",
        "evidence": _evidence(decision_record),
        "psi_state": "BLOQUEADO" if action_gate == "BLOCK" else "INFERENCIA",
        "claim_level": "operational",
        "falsifiers": [
            "COMMS validator fails after append",
            "message is appended while host gate is BLOCK",
            "message lacks seto-observation-v1 envelope",
            "append overwrites an existing COMMS stream",
        ],
        "risk_flags": _risk_flags(decision_record),
        "action_gate": action_gate,
        "decision": _decision_text(decision_record, action_gate),
        "fingerprint": "",
    }
    envelope["fingerprint"] = _hash_payload(envelope)
    message = {
        "message_id": message_id,
        "message_type": "WABI_DECISIONLOG_LOCAL_REVIEW",
        "timestamp_utc": timestamp,
        "sender": sender,
        "recipient": recipient,
        "status": "BLOCKED_BY_GATE" if action_gate == "BLOCK" else "READY_FOR_REVIEW",
        "action_gate": action_gate,
        "observation_envelope": envelope,
        "summary": {
            "record_hash": record_hash,
            "recommended_mode": decision_record.get("recommended_mode"),
            "host_gate": decision_record.get("host_gate"),
            "pending_active_dedup": decision_record.get("pending_active_dedup"),
            "witness_verified": decision_record.get("witness_verified"),
        },
    }
    target_outbox = root / "COMMS" / "outbox" / f"{sender}.jsonl"
    validation = validate_comms_message(message)
    append_allowed = validation["ok"] and action_gate != "BLOCK"
    return {
        "schema": COMMS_APPEND_PLAN_SCHEMA,
        "generated_at_utc": timestamp,
        "portfolio_root": str(root),
        "target_outbox": str(target_outbox),
        "append_allowed": append_allowed,
        "append_performed": False,
        "apply_requested": False,
        "blocked_reason": "" if append_allowed else "action_gate_block_or_invalid_message",
        "validation": validation,
        "message": message,
    }


def execute_comms_append_plan(plan: dict[str, Any], *, apply: bool = False) -> dict[str, Any]:
    result = dict(plan)
    result["apply_requested"] = bool(apply)
    result["append_performed"] = False
    if not apply:
        return result
    if not plan.get("append_allowed"):
        result["blocked_reason"] = plan.get("blocked_reason") or "append_not_allowed"
        return result

    target = Path(str(plan["target_outbox"]))
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(plan["message"], sort_keys=True, ensure_ascii=False) + "\n")
    result["append_performed"] = True
    result["appended_to"] = str(target)
    return result


def write_comms_append_plan(output_dir: Path, plan: dict[str, Any]) -> Path:
    text = json.dumps(plan, indent=2, sort_keys=True, ensure_ascii=False)
    return write_artifact(output_dir, "wabi_comms_append_plan", ".json", text)


def validate_comms_message(message: dict[str, Any]) -> dict[str, Any]:
    errors: list[str] = []
    for field in ["message_id", "message_type", "timestamp_utc", "sender", "recipient", "status", "action_gate"]:
        if not message.get(field):
            errors.append(f"missing:{field}")
    if message.get("action_gate") not in {"APPROVE", "REVIEW", "BLOCK"}:
        errors.append("bad_action_gate")
    envelope = message.get("observation_envelope")
    if not isinstance(envelope, dict):
        errors.append("missing_observation_envelope")
    else:
        required = [
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
        ]
        for field in required:
            if field not in envelope:
                errors.append(f"missing_envelope:{field}")
        if envelope.get("envelope_version") != "seto-observation-v1":
            errors.append("bad_envelope_version")
        if envelope.get("action_gate") not in {"APPROVE", "REVIEW", "BLOCK"}:
            errors.append("bad_envelope_action_gate")
        if envelope.get("psi_state") not in {"CERTEZA", "INFERENCIA", "INCOGNITA", "BLOQUEADO"}:
            errors.append("bad_psi_state")
        if not isinstance(envelope.get("evidence"), list) or not envelope.get("evidence"):
            errors.append("empty_evidence")
    return {"ok": not errors, "errors": errors}


def _action_gate(record: dict[str, Any]) -> str:
    if record.get("host_gate") == "BLOCK" or record.get("recommended_mode") == "A0_LOCAL_REVIEW_ONLY":
        return "BLOCK"
    if record.get("blocked_actions"):
        return "REVIEW"
    return "REVIEW"


def _evidence(record: dict[str, Any]) -> list[str]:
    refs = [str(item) for item in record.get("evidence_refs", []) if str(item)]
    refs.extend(
        [
            f"record_hash={record.get('record_hash', '')}",
            f"environment_snapshot_hash={record.get('environment_snapshot_hash', '')}",
            f"witness_verified={record.get('witness_verified', False)}",
        ]
    )
    return refs


def _risk_flags(record: dict[str, Any]) -> list[str]:
    flags = ["local_review_only", "no_publication", "no_external_action"]
    if record.get("host_gate") == "BLOCK":
        flags.append("host_block")
    for action in record.get("blocked_actions", []):
        flags.append(str(action))
    return sorted(set(flags))


def _decision_text(record: dict[str, Any], action_gate: str) -> str:
    if action_gate == "BLOCK":
        return (
            "DecisionLog recorded locally, but COMMS append is blocked while "
            f"host={record.get('host_status')}/{record.get('host_gate')}."
        )
    return "DecisionLog is ready for append-only COMMS review."


def _hash_payload(payload: dict[str, Any]) -> str:
    encoded = json.dumps(payload, sort_keys=True, ensure_ascii=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest().upper()


def _short_hash(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]


def _utc_now() -> str:
    return dt.datetime.now(dt.UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")
