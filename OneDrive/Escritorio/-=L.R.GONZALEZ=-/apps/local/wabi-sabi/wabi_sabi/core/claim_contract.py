from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from wabi_sabi.core.patch_planner import resolve_workspace_text_target, sha256_text


CLAIM_CONTRACT_SCHEMA = "wabi.claim_contract.v1"
CLAIM_EVALUATION_SCHEMA = "wabi.claim_contract_evaluation.v1"

BLOCK_FLAGS = {
    "secret",
    "credential",
    "private_game",
    "tcg",
    "stealth",
    "offensive",
    "external_publication",
    "model_weights",
    "destructive",
}

STRONG_LEVELS = {
    "public",
    "commercial",
    "scientific",
    "public_scientific",
}

BLOCK_TERMS = {
    "token",
    "api key",
    "private key",
    "stealth",
    "evasion",
    "publish now",
    "deploy now",
}


@dataclass(frozen=True)
class ClaimContract:
    path: Path
    claim: str
    claim_level: str
    evidence: list[str]
    falsifiers: list[str]
    risk_flags: list[str]
    raw: dict[str, Any]

    def fingerprint(self) -> str:
        return sha256_text(
            json.dumps(
                {
                    "claim": self.claim,
                    "claim_level": self.claim_level,
                    "evidence": self.evidence,
                    "falsifiers": self.falsifiers,
                    "risk_flags": self.risk_flags,
                },
                sort_keys=True,
                ensure_ascii=False,
            )
        )


def load_claim_contract(*, workspace: str | Path, spec_path: str | Path) -> ClaimContract:
    workspace_path = Path(workspace).resolve()
    path = resolve_workspace_text_target(workspace_path, spec_path, suffix=".json")
    raw = json.loads(path.read_text(encoding="utf-8"))
    return _claim_contract_from_raw(raw, path=path)


def evaluate_claim_contract_payload(raw: dict[str, Any], *, contract_path: str | Path = "<embedded>") -> dict[str, Any]:
    contract = _claim_contract_from_raw(raw, path=Path(contract_path))
    return _evaluate_claim_contract(contract)


def evaluate_claim_contract(*, workspace: str | Path, spec_path: str | Path) -> dict[str, Any]:
    contract = load_claim_contract(workspace=workspace, spec_path=spec_path)
    return _evaluate_claim_contract(contract)


def _claim_contract_from_raw(raw: dict[str, Any], *, path: Path) -> ClaimContract:
    if not isinstance(raw, dict):
        raise ValueError("claim_contract_must_be_json_object")
    schema = raw.get("schema")
    if schema not in {CLAIM_CONTRACT_SCHEMA, None}:
        raise ValueError(f"unsupported_claim_contract_schema:{schema}")
    claim = str(raw.get("claim") or "").strip()
    if not claim:
        raise ValueError("claim_required")
    claim_level = str(raw.get("claim_level") or raw.get("level") or "operational").strip().lower()
    evidence = _string_list(raw.get("evidence", []), field="evidence")
    falsifiers = _string_list(raw.get("falsifiers", []), field="falsifiers")
    risk_flags = sorted({item.lower() for item in _string_list(raw.get("risk_flags", []), field="risk_flags")})
    return ClaimContract(
        path=path,
        claim=claim,
        claim_level=claim_level,
        evidence=evidence,
        falsifiers=falsifiers,
        risk_flags=risk_flags,
        raw=raw,
    )


def _evaluate_claim_contract(contract: ClaimContract) -> dict[str, Any]:
    reasons: list[str] = []
    required_actions: list[str] = []
    lowered_claim = contract.claim.lower()
    blocked_flags = sorted(BLOCK_FLAGS.intersection(contract.risk_flags))

    if blocked_flags:
        reasons.append("blocked_risk_flags:" + ",".join(blocked_flags))
    if any(term in lowered_claim for term in BLOCK_TERMS):
        reasons.append("blocked_claim_terms")

    if reasons:
        gate = "BLOCK"
        status = "blocked"
        required_actions.extend(["remove_blocked_material", "create_safe_public_boundary"])
    else:
        if not contract.evidence:
            reasons.append("evidence_required")
            required_actions.append("add_local_evidence")
        if not contract.falsifiers:
            reasons.append("falsifiers_required")
            required_actions.append("add_falsifiers")
        if contract.claim_level in STRONG_LEVELS and len(contract.evidence) < 2:
            reasons.append("strong_claim_needs_two_or_more_evidence_refs")
            required_actions.append("downgrade_claim_or_add_evidence")
        if contract.claim_level in {"scientific", "public_scientific"}:
            reasons.append("scientific_claim_requires_human_review")
            required_actions.append("keep_research_only_until_reviewed")
        gate = "APPROVE" if not reasons else "REVIEW"
        status = "ready" if gate == "APPROVE" else "needs_review"

    return {
        "schema": CLAIM_EVALUATION_SCHEMA,
        "ok": gate != "BLOCK",
        "action": "claim_contract_evaluation",
        "gate": gate,
        "status": status,
        "contract_path": str(contract.path),
        "claim": contract.claim,
        "claim_level": contract.claim_level,
        "fingerprint": contract.fingerprint(),
        "evidence_count": len(contract.evidence),
        "falsifier_count": len(contract.falsifiers),
        "risk_flags": contract.risk_flags,
        "reasons": reasons or ["evidence_and_falsifiers_present"],
        "required_actions": sorted(set(required_actions)),
    }


def _string_list(value: Any, *, field: str) -> list[str]:
    if not isinstance(value, list):
        raise ValueError(f"{field}_must_be_list")
    result: list[str] = []
    for index, item in enumerate(value):
        if not isinstance(item, str):
            raise ValueError(f"{field}_item_must_be_string:{index}")
        text = item.strip()
        if text:
            result.append(text)
    return result
