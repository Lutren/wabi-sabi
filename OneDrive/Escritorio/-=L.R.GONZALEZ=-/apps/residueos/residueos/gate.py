from __future__ import annotations

from typing import Any

from .metrics import (
    balance_lg,
    broadcast_score,
    clamp01,
    evidence_score,
    observed_modes,
    phi_eff,
    restriction_score,
    self_reference_score,
    theta_score,
    useful_complexity_score,
)


DEFAULT_CONFIG: dict[str, float | bool] = {
    "theta_approve": 0.22,
    "theta_review": 0.10,
    "residue_review": 20.0,
    "residue_block": 45.0,
    "high_risk": 0.80,
    "low_reversibility": 0.30,
    "jamming_threshold": 50.0,
    "balance_min": 0.12,
    "balance_max": 0.90,
    "selectivity_review": 0.35,
    "calibration_review": 0.35,
    "demo_only_thresholds": True,
}

CONSEQUENTIAL_ACTIONS = {"approve_invoice", "edit_file", "delete", "run_code", "send_email", "publish"}


def _list_from(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def _field(action: dict[str, Any], *names: str, default: Any = None) -> Any:
    for name in names:
        if name in action:
            return action[name]
    return default


def _policy_tags(action: dict[str, Any]) -> list[str]:
    return [str(item) for item in _list_from(action.get("policyTags") or action.get("policy_tags"))]


def _receptor_state(action: dict[str, Any]) -> dict[str, Any]:
    action_type = str(action.get("actionType") or action.get("action_type") or "").lower()
    tags = _policy_tags(action)
    receptor_id = str(_field(action, "receptorId", "receptor_id", default="") or "")
    required = bool(
        _field(action, "requiresReceptor", "requires_receptor", default=action_type in CONSEQUENTIAL_ACTIONS)
        or "requires_authorized_receptor" in tags
    )
    authorized_value = _field(action, "receptorAuthorized", "receptor_authorized", default=None)
    authorized = bool(receptor_id) if authorized_value is None else bool(authorized_value)
    return {
        "id": receptor_id,
        "required": required,
        "authorized": authorized,
        "selectivity": _field(action, "selectivity", "receptorSelectivity", "receptor_selectivity", default=None),
        "calibration": _field(action, "calibration", "receptorCalibration", "receptor_calibration", default=None),
        "authorityScore": _field(action, "authorityScore", "authority_score", default=None),
    }


def compute_residue(action: dict[str, Any]) -> dict[str, Any]:
    missing_evidence: list[str] = []
    contradictions: list[str] = []
    assumptions: list[str] = []
    unresolved_questions: list[str] = []
    policy_violations: list[str] = []

    sources = _list_from(action.get("sources"))
    tools = _list_from(action.get("toolCalls"))
    receptor = _receptor_state(action)

    if not sources:
        missing_evidence.append("No sources were provided.")
    elif not any(isinstance(source, dict) and source.get("verified") for source in sources):
        missing_evidence.append("No verified source was provided.")

    action_type = str(action.get("actionType") or "").lower()
    if action_type in CONSEQUENTIAL_ACTIONS and not tools:
        missing_evidence.append("No tool call or external check was recorded for a consequential action.")

    self_check = action.get("selfCheck")
    if not isinstance(self_check, dict):
        assumptions.append("No self-check object was provided.")
    else:
        assumptions.extend(str(item) for item in _list_from(self_check.get("assumptions")))
        unresolved_questions.extend(str(item) for item in _list_from(self_check.get("uncertainties")))
        contradictions.extend(str(item) for item in _list_from(self_check.get("contradictions")))

    risk = clamp01(action.get("risk", 0.5))
    reversibility = clamp01(action.get("reversibility", 0.5))
    if risk > 0.8 and reversibility < 0.3:
        policy_violations.append("High-risk action with low reversibility.")

    if len(str(action.get("output") or "").strip()) < 20:
        unresolved_questions.append("Output is too short to audit meaningfully.")
    if len(str(action.get("input") or "").strip()) < 10:
        unresolved_questions.append("Input/context is too short.")

    policy_tags = _policy_tags(action)
    human_reviewers = _list_from(action.get("humanReviewers"))
    if "requires_human_approval" in policy_tags and not human_reviewers:
        policy_violations.append("Policy requires human approval but no human reviewer is attached.")

    if receptor["required"] and not receptor["id"]:
        policy_violations.append("missing_authorized_receptor")
    elif receptor["id"] and not receptor["authorized"]:
        policy_violations.append("receptor_not_authorized")

    if receptor["selectivity"] is not None and clamp01(receptor["selectivity"]) < float(DEFAULT_CONFIG["selectivity_review"]):
        unresolved_questions.append("low_receptor_selectivity")
    if receptor["calibration"] is not None and clamp01(receptor["calibration"]) < float(DEFAULT_CONFIG["calibration_review"]):
        unresolved_questions.append("low_receptor_calibration")

    residue_score = (
        len(missing_evidence) * 8
        + len(contradictions) * 10
        + len(assumptions) * 3
        + len(unresolved_questions) * 4
        + len(policy_violations) * 12
    )

    return {
        "missingEvidence": missing_evidence,
        "contradictions": contradictions,
        "assumptions": assumptions,
        "unresolvedQuestions": unresolved_questions,
        "policyViolations": policy_violations,
        "residueScore": residue_score,
    }


def evaluate_action(action: dict[str, Any], config: dict[str, Any] | None = None) -> dict[str, Any]:
    cfg = {**DEFAULT_CONFIG, **(config or {})}

    residue = compute_residue(action)
    distinguishability = evidence_score(action)
    dim_obs = observed_modes(action)
    complexity = useful_complexity_score(action)
    broadcast = broadcast_score(action)
    self_reference = self_reference_score(action)
    restriction = restriction_score(action)
    balance = balance_lg(distinguishability, restriction)
    phi = phi_eff(residue["residueScore"], float(cfg["jamming_threshold"]))
    receptor = _receptor_state(action)

    theta = theta_score(
        distinguishability=distinguishability,
        dim_obs=dim_obs,
        complexity=complexity,
        broadcast=broadcast,
        self_reference=self_reference,
        phi_eff_value=phi,
        balance=balance,
        balance_min=float(cfg["balance_min"]),
        balance_max=float(cfg["balance_max"]),
    )

    reasons: list[str] = []
    status = "APPROVE"

    risk = clamp01(action.get("risk", 0.5))
    reversibility = clamp01(action.get("reversibility", 0.5))
    if risk >= float(cfg["high_risk"]) and reversibility <= float(cfg["low_reversibility"]):
        status = "BLOCK"
        reasons.append("high-risk low-reversibility action")

    if residue["residueScore"] >= float(cfg["residue_block"]):
        status = "BLOCK"
        reasons.append("critical residue score")

    if any(item in residue["policyViolations"] for item in {"missing_authorized_receptor", "receptor_not_authorized"}):
        status = "BLOCK"
        reasons.append("authorized receptor required")

    if status != "BLOCK":
        if theta < float(cfg["theta_review"]) or residue["residueScore"] >= float(cfg["residue_review"]):
            status = "REVIEW"
            reasons.append("low operational threshold or significant residue")
        elif theta < float(cfg["theta_approve"]):
            status = "REVIEW"
            reasons.append("theta below approval threshold")

    if residue["policyViolations"] and status != "BLOCK":
        status = "REVIEW"
        reasons.append("policy violation requires review")

    if status == "APPROVE":
        reasons.append("sufficient evidence, acceptable residue and operational threshold")

    return {
        "schemaVersion": "residueos.decision.v1",
        "status": status,
        "theta": theta,
        "reasons": reasons,
        "residue": residue,
        "scores": {
            "distinguishability": distinguishability,
            "dimObs": dim_obs,
            "complexity": complexity,
            "broadcast": broadcast,
            "selfReference": self_reference,
            "restriction": restriction,
            "balanceLG": balance,
            "phiEff": phi,
            "receptorSelectivity": clamp01(receptor["selectivity"]) if receptor["selectivity"] is not None else None,
            "receptorCalibration": clamp01(receptor["calibration"]) if receptor["calibration"] is not None else None,
            "authorityScore": clamp01(receptor["authorityScore"]) if receptor["authorityScore"] is not None else None,
        },
        "receptor": receptor,
        "config": cfg,
        "claims": {
            "thresholdCalibration": "DEMO_ONLY",
            "confusionMatrix": "DEMO_ONLY_UNTIL_REAL_DATASET",
            "patentPatternUse": "ABSTRACT_SOFTWARE_PATTERN_ONLY",
            "legalStatus": "LEGAL_REVIEW_REQUIRED",
        },
    }
