from __future__ import annotations

from typing import Any

from .metrics import balance_lg, clamp01, phi_eff_power, theta_score


DEFAULT_GATE_CONFIG: dict[str, Any] = {
    "theta_approve": 0.22,
    "theta_review": 0.10,
    "residue_review": 0.30,
    "residue_block": 0.60,
    "high_risk": 0.80,
    "low_reversibility": 0.30,
    "balance_min": 0.12,
    "balance_max": 0.90,
    "jamming_threshold": 1.0,
    "demo_only_thresholds": True,
}

CONSEQUENTIAL_ACTIONS = {"send_email", "delete", "edit_file", "run_code", "approve_invoice", "publish"}


def _list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def _action_type(action: dict[str, Any]) -> str:
    return str(action.get("action_type") or action.get("actionType") or "").lower()


def _sources(action: dict[str, Any]) -> list[dict[str, Any]]:
    return [source for source in _list(action.get("sources")) if isinstance(source, dict)]


def _tools(action: dict[str, Any]) -> list[dict[str, Any]]:
    tools = action.get("tool_calls") or action.get("toolCalls")
    return [tool for tool in _list(tools) if isinstance(tool, dict)]


def _self_check(action: dict[str, Any]) -> dict[str, Any]:
    value = action.get("self_check") or action.get("selfCheck") or {}
    return value if isinstance(value, dict) else {}


def score_sources(action: dict[str, Any]) -> float:
    sources = _sources(action)
    if not sources:
        return 0.0
    total = 0.0
    for source in sources:
        confidence = clamp01(source.get("confidence", 0.5))
        verified = 1.0 if source.get("verified") else 0.45
        total += confidence * verified
    return clamp01(total / len(sources))


def dim_obs(action: dict[str, Any]) -> int:
    modes: set[str] = set()
    if str(action.get("input") or "").strip():
        modes.add("input")
    if str(action.get("output") or "").strip():
        modes.add("output")
    sources = _sources(action)
    if sources:
        modes.add("sources")
    if any(source.get("verified") for source in sources):
        modes.add("verified_sources")
    tools = _tools(action)
    if tools:
        modes.add("tool_calls")
    if any(tool.get("status") == "ok" for tool in tools):
        modes.add("successful_tools")
    if _self_check(action):
        modes.add("self_check")
    if _list(action.get("human_reviewers") or action.get("humanReviewers")):
        modes.add("human_review")
    if _list(action.get("policy_tags") or action.get("policyTags")):
        modes.add("policy_tags")
    return len(modes)


def self_reference(action: dict[str, Any]) -> float:
    self_check = _self_check(action)
    if isinstance(self_check.get("score"), (int, float)):
        return clamp01(self_check["score"])
    points = 0
    if str(self_check.get("summary") or "").strip():
        points += 1
    if isinstance(self_check.get("confidence"), (int, float)):
        points += 1
    if isinstance(self_check.get("assumptions"), list):
        points += 1
    if isinstance(self_check.get("uncertainties"), list):
        points += 1
    if isinstance(self_check.get("falsifiers"), list) and self_check["falsifiers"]:
        points += 1
    return clamp01(points / 5.0)


def broadcast(action: dict[str, Any]) -> float:
    points = 0
    if _sources(action):
        points += 1
    if _tools(action):
        points += 1
    if _self_check(action):
        points += 1
    if _list(action.get("human_reviewers") or action.get("humanReviewers")):
        points += 1
    if _list(action.get("policy_tags") or action.get("policyTags")):
        points += 1
    return clamp01(points / 5.0)


def useful_complexity(action: dict[str, Any]) -> float:
    text = f"{action.get('input') or ''} {action.get('output') or ''}"
    length = len(text.strip())
    if length <= 20:
        return 0.10
    if length < 160:
        return 0.45
    if length < 1200:
        return 0.75
    return 0.60


def compute_residue(action: dict[str, Any]) -> dict[str, Any]:
    missing_evidence: list[str] = []
    contradictions: list[str] = []
    assumptions: list[str] = []
    unresolved: list[str] = []
    policy_violations: list[str] = []

    sources = _sources(action)
    tools = _tools(action)
    check = _self_check(action)

    if not sources:
        missing_evidence.append("no_sources")
    elif not any(source.get("verified") for source in sources):
        missing_evidence.append("no_verified_source")

    if _action_type(action) in CONSEQUENTIAL_ACTIONS and not tools:
        missing_evidence.append("consequential_action_without_tool_check")

    if not check:
        assumptions.append("no_self_check")
    else:
        assumptions.extend(str(item) for item in _list(check.get("assumptions")))
        unresolved.extend(str(item) for item in _list(check.get("uncertainties")))
        contradictions.extend(str(item) for item in _list(check.get("contradictions")))

    risk = clamp01(action.get("risk", 0.5))
    reversibility = clamp01(action.get("reversibility", 0.5))
    if risk > 0.8 and reversibility < 0.3:
        policy_violations.append("high_risk_low_reversibility")

    policy_tags = _list(action.get("policy_tags") or action.get("policyTags"))
    human_reviewers = _list(action.get("human_reviewers") or action.get("humanReviewers"))
    if "requires_human_approval" in policy_tags and not human_reviewers:
        policy_violations.append("human_approval_required")

    residue = (
        0.10 * len(missing_evidence)
        + 0.14 * len(contradictions)
        + 0.05 * len(assumptions)
        + 0.07 * len(unresolved)
        + 0.18 * len(policy_violations)
    )

    return {
        "missing_evidence": missing_evidence,
        "contradictions": contradictions,
        "assumptions": assumptions,
        "unresolved": unresolved,
        "policy_violations": policy_violations,
        "R": clamp01(residue),
    }


def evaluate_action(action: dict[str, Any], config: dict[str, Any] | None = None) -> dict[str, Any]:
    cfg = {**DEFAULT_GATE_CONFIG, **(config or {})}
    residue = compute_residue(action)
    d_value = score_sources(action)
    dim_value = dim_obs(action)
    complexity = useful_complexity(action)
    broadcast_value = broadcast(action)
    self_ref = self_reference(action)
    restriction = 0.55 * clamp01(action.get("risk", 0.5)) + 0.45 * (1.0 - clamp01(action.get("reversibility", 0.5)))
    balance = balance_lg(d_value, restriction)
    phi = phi_eff_power(residue["R"], jamming_threshold=cfg["jamming_threshold"])
    theta = theta_score(
        distinguishability=d_value,
        dim_obs=dim_value,
        complexity=complexity,
        broadcast=broadcast_value,
        self_reference=self_ref,
        phi_eff_value=phi,
        balance=balance,
        balance_min=cfg["balance_min"],
        balance_max=cfg["balance_max"],
    )

    status = "APPROVE"
    reasons: list[str] = []
    risk = clamp01(action.get("risk", 0.5))
    reversibility = clamp01(action.get("reversibility", 0.5))

    if risk >= cfg["high_risk"] and reversibility <= cfg["low_reversibility"]:
        status = "BLOCK"
        reasons.append("high_risk_low_reversibility")

    if residue["R"] >= cfg["residue_block"]:
        status = "BLOCK"
        reasons.append("critical_residue")

    if status != "BLOCK":
        if theta < cfg["theta_review"]:
            status = "REVIEW"
            reasons.append("theta_below_review_threshold")
        elif theta < cfg["theta_approve"] or residue["R"] >= cfg["residue_review"]:
            status = "REVIEW"
            reasons.append("needs_review_due_to_theta_or_residue")
        else:
            reasons.append("sufficient_operational_threshold")

    if residue["policy_violations"] and status != "BLOCK":
        status = "REVIEW"
        reasons.append("policy_violation_requires_review")

    return {
        "schemaVersion": "obsai.action_gate.v1",
        "status": status,
        "theta": theta,
        "scores": {
            "R": residue["R"],
            "phi_eff": phi,
            "distinguishability": d_value,
            "dim_obs": dim_value,
            "complexity": complexity,
            "broadcast": broadcast_value,
            "self_reference": self_ref,
            "restriction": restriction,
            "balance_lg": balance,
        },
        "residue": residue,
        "reasons": reasons,
        "config": cfg,
        "claims": {
            "thresholdCalibration": "DEMO_ONLY",
            "weights": "DEMO_ONLY",
            "researchClaims": "NO_PRODUCT_CLAIMS",
        },
    }
