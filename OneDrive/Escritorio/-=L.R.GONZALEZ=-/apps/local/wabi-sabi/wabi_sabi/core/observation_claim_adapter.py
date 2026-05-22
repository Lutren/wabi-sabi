from __future__ import annotations

import datetime as dt
import json
import sys
from pathlib import Path
from typing import Any, Mapping

from wabi_sabi.core.bridge import WitnessLog
from wabi_sabi.core.memory import LocalMemory
from wabi_sabi.core.observation import ObservationEnvelope as WabiObservationEnvelope
from wabi_sabi.core.redaction import redact_mapping, redact_text
from wabi_sabi.core.tools import write_artifact


ADAPTER_SCHEMA = "wabi.claim_observation_adapter.v0_1"
FIXTURE_REVIEW_SCHEMA = "wabi.claim_observation_fixture_review.v0_1"


def run_claim_observation_adapter(
    claim: str,
    *,
    workspace: str | Path,
    runtime_root: str | Path,
    persist: bool = True,
) -> dict[str, Any]:
    safe_claim = redact_text(str(claim or "").strip())
    if not safe_claim:
        raise ValueError("claim_required")
    classifier = _claim_classifier(workspace)
    obsai_envelope = classifier.classify(safe_claim, task="wabi_claim_observation_adapter")
    obsai_payload = redact_mapping(obsai_envelope.to_dict())
    claims = obsai_payload.get("claims") if isinstance(obsai_payload.get("claims"), list) else []
    primary_claim = claims[0] if claims and isinstance(claims[0], Mapping) else {}
    wabi_observation = WabiObservationEnvelope(
        prompt=safe_claim,
        intent="claim_observation_adapter",
        agent="ClaimClassifier",
        action_gate=_wabi_action_gate(str(obsai_payload.get("gate", "REVIEW"))),
        certainty=_certainty(obsai_payload),
        inference=_inference(obsai_payload),
        unknown=_unknown(obsai_payload),
        artifacts=[],
        evidence=list(obsai_payload.get("evidence", [])) if isinstance(obsai_payload.get("evidence"), list) else [],
    ).finalize()
    payload: dict[str, Any] = {
        "schema": ADAPTER_SCHEMA,
        "ok": True,
        "action": "claim_observation_adapter",
        "mode": "proposal_only",
        "workspace": str(Path(workspace).resolve()),
        "claim": safe_claim,
        "classification": {
            "label": primary_claim.get("label", "INCOGNITA"),
            "gate": obsai_payload.get("gate", "REVIEW"),
            "R_or": obsai_payload.get("R_or"),
            "phi_moi": obsai_payload.get("phi_moi"),
            "regime": obsai_payload.get("regime", "HOLD"),
        },
        "obsai_envelope": obsai_payload,
        "wabi_observation": wabi_observation.to_dict(),
        "proposal": _proposal(obsai_payload),
        "proposal_only": True,
        "cloud_provider_called": False,
        "applied_to_sources": False,
        "publication_gate": "BLOCK",
        "next_safe_action": "Review the ObservationEnvelope and only create a separate TaskSpec if the claim gate and evidence justify local work.",
    }
    if persist:
        payload["persistence"] = _persist("claim_observation_adapter", payload, runtime_root)
    return redact_mapping(payload)


def run_claim_fixture_review(
    fixture_path: str | Path,
    *,
    workspace: str | Path,
    runtime_root: str | Path,
    persist: bool = True,
) -> dict[str, Any]:
    fixture = _load_fixture(fixture_path)
    cases = fixture.get("cases") if isinstance(fixture.get("cases"), list) else []
    if not cases:
        raise ValueError("claim_fixture_cases_required")
    classifier = _claim_classifier(workspace)
    results: list[dict[str, Any]] = []
    for case in cases:
        if not isinstance(case, Mapping):
            continue
        case_id = str(case.get("id", f"case-{len(results) + 1}"))
        claim = redact_text(str(case.get("claim", "")).strip())
        if not claim:
            continue
        classified = classifier.classify_atom(claim)
        primary = redact_mapping(classified.to_dict())
        envelope_payload = {
            "gate": primary.get("gate", "REVIEW"),
            "R_or": primary.get("R_or", 0.0),
            "phi_moi": primary.get("phi_moi", 0.0),
        }
        expected_label = str(case.get("expected_label", ""))
        expected_gate = str(case.get("expected_gate", ""))
        expected_wabi_gate = _expected_gate_to_obsai(expected_gate)
        r_range = _number_pair(case.get("r_range"))
        phi_range = _number_pair(case.get("phi_moi_range"))
        label_match = primary.get("label") == expected_label if expected_label else True
        gate_match = envelope_payload.get("gate") == expected_wabi_gate if expected_wabi_gate else True
        r_match = _in_range(float(envelope_payload.get("R_or", 0.0)), r_range)
        phi_match = _in_range(float(envelope_payload.get("phi_moi", 0.0)), phi_range)
        status = "PASS" if label_match and gate_match and r_match and phi_match else "REVIEW"
        results.append(
            {
                "id": case_id,
                "claim": claim,
                "expected_label": expected_label,
                "actual_label": primary.get("label", "INCOGNITA"),
                "expected_gate": expected_gate,
                "actual_gate": envelope_payload.get("gate", "REVIEW"),
                "R_or": envelope_payload.get("R_or"),
                "phi_moi": envelope_payload.get("phi_moi"),
                "status": status,
                "checks": {
                    "label_match": label_match,
                    "gate_match": gate_match,
                    "r_range_match": r_match,
                    "phi_range_match": phi_match,
                },
                "rewrite_hint": primary.get("rewrite_hint") or case.get("rewrite"),
                "falsifier_hint": primary.get("falsifier_hint") or case.get("falsifier_hint"),
            }
        )
    review_count = sum(1 for item in results if item["status"] == "REVIEW")
    next_safe_action = (
        "Fixture review passed; no calibration patch is required. Use output as local evidence only."
        if review_count == 0
        else "Use REVIEW cases to calibrate ClaimClassifier rules or rewrite fixtures in a separate local patch."
    )
    payload: dict[str, Any] = {
        "schema": FIXTURE_REVIEW_SCHEMA,
        "ok": True,
        "action": "claim_observation_fixture_review",
        "mode": "proposal_only",
        "fixture_path": str(Path(fixture_path).resolve()),
        "fixture_schema": fixture.get("schema_version", ""),
        "case_count": len(results),
        "pass_count": len(results) - review_count,
        "review_count": review_count,
        "status": "PASS" if review_count == 0 else "REVIEW",
        "results": results,
        "proposal_only": True,
        "cloud_provider_called": False,
        "applied_to_sources": False,
        "publication_gate": "BLOCK",
        "next_safe_action": next_safe_action,
    }
    if persist:
        payload["persistence"] = _persist("claim_observation_fixture_review", payload, runtime_root)
    return redact_mapping(payload)


def _claim_classifier(workspace: str | Path):
    _ensure_obsai_core_path(Path(workspace).resolve())
    from obsai_core.claim_classifier import ClaimClassifier

    return ClaimClassifier(agent_name="WabiClaimClassifier")


def _ensure_obsai_core_path(workspace: Path) -> None:
    for root in _candidate_roots(workspace):
        package_root = root / "packages" / "open-dev" / "obsai-core"
        if (package_root / "obsai_core" / "claim_classifier.py").exists():
            package_text = str(package_root)
            if package_text not in sys.path:
                sys.path.insert(0, package_text)
            return
    raise RuntimeError("obsai_core_claim_classifier_not_found")


def _candidate_roots(workspace: Path) -> list[Path]:
    roots: list[Path] = []
    for item in [workspace, *workspace.parents, Path(__file__).resolve(), *Path(__file__).resolve().parents]:
        if item not in roots:
            roots.append(item)
    return roots


def _proposal(obsai_payload: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "schema": "wabi.claim_observation_proposal.v0_1",
        "proposal_only": True,
        "apply_allowed": False,
        "cloud_authority": "not_used",
        "source_authority": "local_obsai_core_claim_classifier",
        "claim_gate": obsai_payload.get("gate", "REVIEW"),
        "regime": obsai_payload.get("regime", "HOLD"),
        "recommended_action": obsai_payload.get("next_action", "Review claim before any local work."),
        "required_gates": ["ActionGate", "ScienceClaimGate", "EvidenceGate", "TaskSpecGate"],
    }


def _certainty(obsai_payload: Mapping[str, Any]) -> list[str]:
    claims = [item for item in obsai_payload.get("claims", []) if isinstance(item, Mapping)]
    values = [str(item["text"]) for item in claims if item.get("label") == "CERTEZA"]
    return values or [f"Claim gate: {obsai_payload.get('gate', 'REVIEW')}"]


def _inference(obsai_payload: Mapping[str, Any]) -> list[str]:
    claims = [item for item in obsai_payload.get("claims", []) if isinstance(item, Mapping)]
    values = [str(item["text"]) for item in claims if item.get("label") == "INFERENCIA"]
    return values or [f"Regime: {obsai_payload.get('regime', 'HOLD')}"]


def _unknown(obsai_payload: Mapping[str, Any]) -> list[str]:
    claims = [item for item in obsai_payload.get("claims", []) if isinstance(item, Mapping)]
    values = [str(item["text"]) for item in claims if item.get("label") in {"INCOGNITA", "BLOQUEO"}]
    if obsai_payload.get("gate") != "APPROVE":
        values.append(str(obsai_payload.get("next_action", "review_required")))
    return values or ["No unresolved claim reported by classifier."]


def _primary_claim(envelope: Mapping[str, Any]) -> Mapping[str, Any]:
    claims = envelope.get("claims")
    if isinstance(claims, list) and claims and isinstance(claims[0], Mapping):
        return claims[0]
    return {}


def _wabi_action_gate(gate: str) -> str:
    if gate == "APPROVE":
        return "APPROVE"
    if gate == "BLOCK":
        return "BLOCK"
    return "REVIEW"


def _expected_gate_to_obsai(expected_gate: str) -> str:
    if expected_gate.startswith("APPROVE"):
        return "APPROVE"
    if expected_gate.startswith("BLOCK"):
        return "BLOCK"
    if expected_gate.startswith("REVIEW"):
        return "REVIEW"
    return ""


def _number_pair(value: Any) -> tuple[float, float] | None:
    if not isinstance(value, list) or len(value) != 2:
        return None
    try:
        return float(value[0]), float(value[1])
    except (TypeError, ValueError):
        return None


def _in_range(value: float, bounds: tuple[float, float] | None) -> bool:
    if bounds is None:
        return True
    return bounds[0] <= value <= bounds[1]


def _load_fixture(path: str | Path) -> dict[str, Any]:
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("claim_fixture_must_be_json_object")
    return payload


def _persist(channel: str, payload: Mapping[str, Any], runtime_root: str | Path) -> dict[str, Any]:
    runtime = Path(runtime_root).resolve()
    artifact = write_artifact(
        runtime / "outputs" / "claim_observation_adapter",
        channel,
        ".json",
        json.dumps(redact_mapping(dict(payload)), indent=2, ensure_ascii=False) + "\n",
    )
    witness = WitnessLog(runtime / "witness" / "wabi_claim_observation_witness.sqlite")
    event_id = witness.append(
        channel,
        {
            "artifact": str(artifact),
            "schema": payload.get("schema"),
            "status": payload.get("status", payload.get("classification", {}).get("gate", "")),
            "cloud_provider_called": False,
            "applied_to_sources": False,
            "publication_gate": "BLOCK",
            "created_at_utc": dt.datetime.now(dt.UTC).isoformat(),
        },
    )
    verified, reason = witness.verify_chain()
    LocalMemory(runtime).append_event(
        {
            "channel": channel,
            "artifact": str(artifact),
            "witness_event_id": event_id,
            "witness_verified": verified,
            "witness_reason": reason,
            "cloud_provider_called": False,
            "applied_to_sources": False,
        }
    )
    return {
        "artifact": str(artifact),
        "witness_event_id": event_id,
        "witness_verified": verified,
        "witness_reason": reason,
        "witness_db": str(witness.db_path),
    }
