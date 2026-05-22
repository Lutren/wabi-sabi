from __future__ import annotations

import datetime as dt
import hashlib
import json
from pathlib import Path
from typing import Any, Mapping

from wabi_sabi.core.bridge import WitnessLog
from wabi_sabi.core.gate import ActionGate
from wabi_sabi.core.memory import LocalMemory
from wabi_sabi.core.redaction import redact_mapping, redact_text
from wabi_sabi.core.tools import write_artifact


HYPOTHESIS_PACKET_SCHEMA = "medioevo.hypothesis_packet.v0.1"
HYPOTHESIS_EVALUATION_SCHEMA = "wabi.hypothesis_packet_evaluation.v0_1"
CONJECTURE_RUN_SCHEMA = "wabi.conjecture_counterexample.v0_1"

SYSTEMS = {
    "WABI_SABI_CONTROL_PLANE",
    "DUAT_SIMULATOR_WORLD",
    "MEDIOEVO_FORGE_APP_GAME_CREATOR",
    "MEDIOEVO_SPACE_PUBLIC_PORTAL",
    "SHARED_CONTRACTS",
}

STRONG_CLAIM_TERMS = {
    "agi",
    "consciousness",
    "consciencia",
    "diagnostico medico",
    "medical diagnosis",
    "medicina",
    "new physics",
    "nueva fisica",
    "predicts society",
    "prediccion social",
    "proves",
    "resuelve",
    "scientific",
    "teorema",
}

PUBLIC_TERMS = {"publica", "publicar", "deploy", "push", "gumroad", "linkedin", "x.com"}
COMMERCIAL_TERMS = {"vende", "venta", "commercial", "comercial", "gumroad", "stripe"}


def build_hypothesis_packet(
    claim: str,
    *,
    source_system: str = "WABI_SABI_CONTROL_PLANE",
    target_system: str = "WABI_SABI_CONTROL_PLANE",
    claim_level: str | None = None,
    counterclaim: str | None = None,
    falsifiers: list[str] | None = None,
    evidence_required: list[str] | None = None,
    evidence: list[str] | None = None,
) -> dict[str, Any]:
    safe_claim = redact_text(str(claim or "").strip())
    if not safe_claim:
        raise ValueError("claim_required")
    source = _system(source_system)
    target = _system(target_system)
    inferred_level = _claim_level(safe_claim, explicit=claim_level)
    packet = {
        "schema_version": HYPOTHESIS_PACKET_SCHEMA,
        "hypothesis_id": "",
        "source_system": source,
        "target_system": target,
        "claim": safe_claim,
        "counterclaim": redact_text(counterclaim or _default_counterclaim(safe_claim)),
        "claim_level": inferred_level,
        "status": "OPEN",
        "falsifiers": _string_list(falsifiers) or _default_falsifiers(safe_claim, inferred_level),
        "evidence_required": _string_list(evidence_required) or _default_required_evidence(inferred_level),
        "evidence": _string_list(evidence),
        "counterexample_search": {
            "mode": "local_dry_run",
            "proposal_only": True,
            "search_targets": ["focused_tests", "runtime_artifacts", "witness_log", "decision_log"],
            "cloud_provider_called": False,
            "applied_to_sources": False,
        },
        "grader": {
            "status_rule": "SUPPORTED only after required evidence is present and ActionGate is not BLOCK.",
            "counterexample_rule": "FALSIFIED if any falsifier is observed with evidence.",
            "r_phi_rule": "Missing evidence raises R; verified local closure raises Phi_eff.",
        },
        "action_gate": {
            "decision": "REVIEW",
            "reason": "hypothesis_requires_evidence_before_support",
        },
        "boundary": {
            "contains_private_data": False,
            "publication_gate": "BLOCK",
            "external_actions_allowed": False,
        },
        "metadata": {
            "origin": "unit_distance_method_transfer",
            "created_at_utc": _utc_now(),
            "cloud_provider_called": False,
            "applied_to_sources": False,
            "secrets_printed": False,
        },
    }
    packet["hypothesis_id"] = "hypothesis-" + _fingerprint(packet)[:16]
    return redact_mapping(packet)


def evaluate_hypothesis_packet_payload(raw: Mapping[str, Any]) -> dict[str, Any]:
    packet = _normalize_packet(raw)
    claim = str(packet["claim"])
    gate_decision = ActionGate().evaluate_text(" ".join([claim, str(packet.get("counterclaim", ""))]))
    gate = gate_decision.gate
    reasons = list(gate_decision.reasons)
    level = str(packet["claim_level"])
    boundary = packet.get("boundary") if isinstance(packet.get("boundary"), Mapping) else {}
    evidence = _string_list(packet.get("evidence"))
    evidence_required = _string_list(packet.get("evidence_required"))
    falsifiers = _string_list(packet.get("falsifiers"))
    missing_evidence = max(0, len(evidence_required) - len(evidence))

    if boundary.get("contains_private_data") is True:
        gate = "BLOCK"
        reasons.append("private_data_boundary")
    if boundary.get("publication_gate") != "BLOCK":
        gate = "REVIEW" if gate != "BLOCK" else "BLOCK"
        reasons.append("publication_gate_must_block")
    if _is_strong_claim(claim, level):
        gate = "REVIEW" if gate != "BLOCK" else "BLOCK"
        reasons.append("strong_claim_requires_human_review")
    if not falsifiers:
        gate = "REVIEW" if gate != "BLOCK" else "BLOCK"
        reasons.append("falsifiers_required")
    if missing_evidence:
        gate = "REVIEW" if gate != "BLOCK" else "BLOCK"
        reasons.append("evidence_required")

    status = _status_for(packet, gate=gate, missing_evidence=missing_evidence, strong_claim=_is_strong_claim(claim, level))
    r_est = _r_estimate(
        gate=gate,
        missing_evidence=missing_evidence,
        falsifier_count=len(falsifiers),
        strong_claim=_is_strong_claim(claim, level),
    )
    phi_eff = round(max(0.0, 1.0 - r_est), 3)
    return redact_mapping(
        {
            "schema": HYPOTHESIS_EVALUATION_SCHEMA,
            "ok": gate != "BLOCK",
            "gate": gate,
            "status": status,
            "hypothesis_id": packet["hypothesis_id"],
            "claim_level": level,
            "evidence_count": len(evidence),
            "evidence_required_count": len(evidence_required),
            "falsifier_count": len(falsifiers),
            "missing_evidence_count": missing_evidence,
            "R_est": r_est,
            "Phi_eff_est": phi_eff,
            "reasons": sorted(set(reasons or ["hypothesis_ready_for_local_counterexample_search"])),
            "required_actions": _required_actions(gate=gate, status=status, missing_evidence=missing_evidence, level=level),
            "cloud_provider_called": False,
            "applied_to_sources": False,
            "publication_gate": "BLOCK",
            "fingerprint": _fingerprint(packet),
        }
    )


def run_conjecture_counterexample(
    user_text: str,
    *,
    workspace: str | Path,
    runtime_root: str | Path,
    persist: bool = True,
) -> dict[str, Any]:
    workspace_path = Path(workspace).resolve()
    runtime = Path(runtime_root).resolve()
    packet = build_hypothesis_packet(user_text, target_system="WABI_SABI_CONTROL_PLANE")
    evaluation = evaluate_hypothesis_packet_payload(packet)
    task_spec = _task_spec_for(packet, evaluation)
    result: dict[str, Any] = {
        "schema": CONJECTURE_RUN_SCHEMA,
        "ok": bool(evaluation["ok"]),
        "action": "conjecture_counterexample",
        "workspace": str(workspace_path),
        "hypothesis_packet": packet,
        "evaluation": evaluation,
        "task_spec": task_spec,
        "proposal_only": True,
        "cloud_provider_called": False,
        "applied_to_sources": False,
        "graphics_live": False,
        "publication_gate": "BLOCK",
        "next_safe_action": "Run the listed falsifiers with local evidence, then re-evaluate the HypothesisPacket.",
    }
    if persist:
        artifact = write_artifact(
            runtime / "outputs" / "hypothesis_packets",
            "wabi_hypothesis_packet",
            ".json",
            json.dumps(redact_mapping(result), indent=2, ensure_ascii=False) + "\n",
        )
        witness = WitnessLog(runtime / "witness" / "wabi_hypothesis_witness.sqlite")
        event_id = witness.append(
            "hypothesis_packet",
            {
                "hypothesis_id": packet["hypothesis_id"],
                "gate": evaluation["gate"],
                "status": evaluation["status"],
                "fingerprint": evaluation["fingerprint"],
                "artifact": str(artifact),
                "cloud_provider_called": False,
                "applied_to_sources": False,
                "publication_gate": "BLOCK",
            },
        )
        verified, reason = witness.verify_chain()
        LocalMemory(runtime).append_event(
            {
                "channel": "wabi_hypothesis_packet",
                "ok": result["ok"],
                "gate": evaluation["gate"],
                "status": evaluation["status"],
                "hypothesis_id": packet["hypothesis_id"],
                "artifact": str(artifact),
                "witness_event_id": event_id,
            }
        )
        result["artifact"] = str(artifact)
        result["witness"] = {
            "event_type": "hypothesis_packet",
            "event_id": event_id,
            "verified": verified,
            "reason": reason,
            "db_path": str(witness.db_path),
        }
    return redact_mapping(result)


def _normalize_packet(raw: Mapping[str, Any]) -> dict[str, Any]:
    if not isinstance(raw, Mapping):
        raise ValueError("hypothesis_packet_must_be_object")
    packet = dict(raw)
    if packet.get("schema_version") != HYPOTHESIS_PACKET_SCHEMA:
        raise ValueError("unsupported_hypothesis_packet_schema")
    for field in [
        "hypothesis_id",
        "source_system",
        "target_system",
        "claim",
        "counterclaim",
        "claim_level",
        "status",
        "falsifiers",
        "evidence_required",
        "evidence",
        "action_gate",
        "boundary",
    ]:
        if field not in packet:
            raise ValueError(f"missing_required:{field}")
    if _system(str(packet["source_system"])) != packet["source_system"]:
        raise ValueError("invalid_source_system")
    if _system(str(packet["target_system"])) != packet["target_system"]:
        raise ValueError("invalid_target_system")
    if str(packet["status"]) not in {"OPEN", "FALSIFIED", "SUPPORTED", "REVIEW", "BLOCK"}:
        raise ValueError("invalid_hypothesis_status")
    if not _string_list(packet["falsifiers"]):
        raise ValueError("falsifiers_required")
    if not _string_list(packet["evidence_required"]):
        raise ValueError("evidence_required")
    return redact_mapping(packet)


def _task_spec_for(packet: Mapping[str, Any], evaluation: Mapping[str, Any]) -> dict[str, Any]:
    return redact_mapping(
        {
            "schema": "wabi.conversation_task_spec.v0_1",
            "task_id": f"hypothesis-task-{str(packet.get('hypothesis_id', 'unknown'))[-12:]}",
            "intent_name": "hypothesis_request",
            "title": "Run local counterexample search",
            "summary": "Formalize claim, run falsifiers, and record evidence before support/canon/product use.",
            "action_gate": str(evaluation.get("gate", "REVIEW")),
            "proposal_only": True,
            "needs_cloud": False,
            "needs_graphics": False,
            "needs_file_write": False,
            "cloud_authority": "proposal_only",
            "applied_to_sources": False,
            "publication_gate": "BLOCK",
            "rollback_required": False,
            "falsifiers": list(packet.get("falsifiers") or []),
            "evidence_required": list(packet.get("evidence_required") or []),
            "affected_paths": [],
            "changes": [],
            "suggested_tests": [
                "python -B -m pytest tests/test_hypothesis_packet.py -q -p no:cacheprovider",
                "python -m unittest discover packages\\shared-contracts\\tests -v",
            ],
            "safe_next_steps": [
                "Run one falsifier locally.",
                "Attach evidence to the HypothesisPacket.",
                "Re-evaluate before canon, product, or publication use.",
                "Keep publication_gate=BLOCK until separate review.",
            ],
            "next_action": "Collect evidence for the first falsifier.",
        }
    )


def _default_counterclaim(claim: str) -> str:
    return f"There exists local evidence or a counterexample that invalidates or narrows this claim: {claim}"


def _default_falsifiers(claim: str, level: str) -> list[str]:
    falsifiers = [
        "Fails if no focused local command, test, or artifact can support the claim.",
        "Fails if ActionGate returns BLOCK for the requested action.",
        "Fails if source files are mutated during proposal-only evaluation.",
    ]
    if _is_strong_claim(claim, level):
        falsifiers.append("Fails as public/scientific copy until human review and stronger evidence exist.")
    return falsifiers


def _default_required_evidence(level: str) -> list[str]:
    evidence = [
        "Focused local test or command output.",
        "Artifact fingerprint or WitnessLog event.",
    ]
    if level in {"scientific", "public", "commercial", "public_scientific"}:
        evidence.append("Human review of claims, license, and publication boundary.")
    return evidence


def _required_actions(*, gate: str, status: str, missing_evidence: int, level: str) -> list[str]:
    actions = ["run_counterexample_search", "record_witness_event"]
    if missing_evidence:
        actions.append("attach_required_evidence")
    if level in {"scientific", "public", "commercial", "public_scientific"}:
        actions.append("keep_claim_low_or_request_human_review")
    if gate == "BLOCK":
        actions.append("remove_blocked_boundary")
    if status == "SUPPORTED":
        actions.append("record_decision_before_reuse")
    return sorted(set(actions))


def _status_for(packet: Mapping[str, Any], *, gate: str, missing_evidence: int, strong_claim: bool) -> str:
    explicit = str(packet.get("status") or "OPEN")
    if gate == "BLOCK":
        return "BLOCK"
    if explicit == "FALSIFIED":
        return "FALSIFIED"
    if missing_evidence or strong_claim or gate == "REVIEW":
        return "REVIEW"
    return "SUPPORTED"


def _r_estimate(*, gate: str, missing_evidence: int, falsifier_count: int, strong_claim: bool) -> float:
    r = 0.10
    r += min(0.30, missing_evidence * 0.10)
    if falsifier_count == 0:
        r += 0.25
    if strong_claim:
        r += 0.18
    if gate == "BLOCK":
        r += 0.40
    elif gate == "REVIEW":
        r += 0.10
    return round(max(0.0, min(1.0, r)), 3)


def _claim_level(text: str, *, explicit: str | None) -> str:
    if explicit:
        level = explicit.strip().lower()
        if level in {"operational", "research", "scientific", "public", "commercial", "public_scientific"}:
            return level
    lowered = text.lower()
    if any(term in lowered for term in COMMERCIAL_TERMS):
        return "commercial"
    if any(term in lowered for term in PUBLIC_TERMS):
        return "public"
    if any(term in lowered for term in STRONG_CLAIM_TERMS):
        return "scientific"
    if any(term in lowered for term in {"observacionismo", "duat", "geodia", "psi", "osit"}):
        return "research"
    return "operational"


def _is_strong_claim(claim: str, level: str) -> bool:
    lowered = claim.lower()
    return level in {"scientific", "public", "commercial", "public_scientific"} or any(
        term in lowered for term in STRONG_CLAIM_TERMS
    )


def _system(value: str) -> str:
    if value not in SYSTEMS:
        raise ValueError(f"invalid_system:{value}")
    return value


def _string_list(value: Any) -> list[str]:
    if value is None:
        return []
    if not isinstance(value, list):
        raise ValueError("expected_string_list")
    output: list[str] = []
    for index, item in enumerate(value):
        if not isinstance(item, str):
            raise ValueError(f"list_item_must_be_string:{index}")
        text = redact_text(item.strip())
        if text:
            output.append(text)
    return output


def _fingerprint(payload: Mapping[str, Any]) -> str:
    encoded = json.dumps(redact_mapping(dict(payload)), sort_keys=True, ensure_ascii=True, default=str).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _utc_now() -> str:
    return dt.datetime.now(dt.UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")
