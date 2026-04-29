from __future__ import annotations

import math
from collections import Counter
from typing import Any


def safe_number(value: Any, fallback: float = 0.0) -> float:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return fallback
    return number if math.isfinite(number) else fallback


def clamp01(value: Any) -> float:
    number = safe_number(value)
    return max(0.0, min(1.0, number))


def entropy(text: str) -> float:
    text = str(text or "")
    if not text:
        return 0.0
    counts = Counter(text)
    total = len(text)
    value = 0.0
    for count in counts.values():
        probability = count / total
        value -= probability * math.log2(probability)
    max_entropy = math.log2(max(2, len(counts)))
    return clamp01(value / max_entropy)


def logistic01(value: Any, center: float = 0.0, sharpness: float = 1.0) -> float:
    x = safe_number(value)
    try:
        return clamp01(1.0 / (1.0 + math.exp(-sharpness * (x - center))))
    except OverflowError:
        return 0.0 if x < center else 1.0


def phi_eff(residue_score: Any, jamming_threshold: float = 50.0, phi0: float = 1.0) -> float:
    residue = max(0.0, safe_number(residue_score))
    threshold = max(1e-9, safe_number(jamming_threshold, 50.0))
    return clamp01(phi0 * math.exp(-residue / threshold))


def evidence_score(action: dict[str, Any]) -> float:
    sources = action.get("sources")
    if not isinstance(sources, list) or not sources:
        return 0.0
    score = 0.0
    for source in sources:
        if not isinstance(source, dict):
            continue
        confidence = clamp01(source.get("confidence", 0.5))
        verified_boost = 1.0 if source.get("verified") else 0.45
        score += confidence * verified_boost
    return clamp01(score / len(sources))


def observed_modes(action: dict[str, Any]) -> int:
    modes: set[str] = set()
    if str(action.get("input") or "").strip():
        modes.add("input")
    if str(action.get("output") or "").strip():
        modes.add("output")

    sources = action.get("sources") if isinstance(action.get("sources"), list) else []
    if sources:
        modes.add("sources")
    if any(isinstance(source, dict) and source.get("verified") for source in sources):
        modes.add("verified_sources")

    tools = action.get("toolCalls") if isinstance(action.get("toolCalls"), list) else []
    if tools:
        modes.add("tool_calls")
    if any(isinstance(tool, dict) and tool.get("status") == "ok" for tool in tools):
        modes.add("successful_tools")

    if isinstance(action.get("selfCheck"), dict):
        modes.add("self_check")
    if isinstance(action.get("policyTags"), list) and action["policyTags"]:
        modes.add("policy_tags")
    if isinstance(action.get("humanReviewers"), list) and action["humanReviewers"]:
        modes.add("human_review")
    return len(modes)


def dim_obs_score(dim_obs: Any, dim_scale: float = 6.0) -> float:
    dim = max(0.0, safe_number(dim_obs))
    return clamp01(1.0 - math.exp(-dim / max(dim_scale, 1e-9)))


def useful_complexity_score(action: dict[str, Any]) -> float:
    text = f"{action.get('input') or ''}\n{action.get('output') or ''}"
    entropy_score = entropy(text)
    length_score = logistic01(len(text), center=200.0, sharpness=0.01)
    return clamp01(0.55 * entropy_score + 0.45 * length_score)


def broadcast_score(action: dict[str, Any]) -> float:
    channels = 0
    if isinstance(action.get("sources"), list) and action["sources"]:
        channels += 1
    if isinstance(action.get("toolCalls"), list) and action["toolCalls"]:
        channels += 1
    if isinstance(action.get("selfCheck"), dict):
        channels += 1
    if isinstance(action.get("humanReviewers"), list) and action["humanReviewers"]:
        channels += 1
    if isinstance(action.get("policyTags"), list) and action["policyTags"]:
        channels += 1
    return clamp01(channels / 5.0)


def self_reference_score(action: dict[str, Any]) -> float:
    self_check = action.get("selfCheck")
    if not isinstance(self_check, dict):
        return 0.0
    if isinstance(self_check.get("score"), (int, float)):
        return clamp01(self_check["score"])

    points = 0
    if isinstance(self_check.get("assumptions"), list):
        points += 1
    if isinstance(self_check.get("uncertainties"), list):
        points += 1
    if isinstance(self_check.get("falsifiers"), list) and self_check["falsifiers"]:
        points += 1
    if str(self_check.get("summary") or "").strip():
        points += 1
    if isinstance(self_check.get("confidence"), (int, float)):
        points += 1
    return clamp01(points / 5.0)


def restriction_score(action: dict[str, Any]) -> float:
    risk = clamp01(action.get("risk", 0.5))
    reversibility = clamp01(action.get("reversibility", 0.5))
    irreversibility = 1.0 - reversibility
    policy_count = len(action.get("policyTags")) if isinstance(action.get("policyTags"), list) else 0
    policy_penalty = clamp01(policy_count / 8.0)
    return clamp01(0.55 * risk + 0.35 * irreversibility + 0.10 * policy_penalty)


def balance_lg(distinguishability: Any, restriction: Any, eps: float = 1e-12) -> float:
    d_value = max(0.0, safe_number(distinguishability))
    r_value = max(0.0, safe_number(restriction))
    return clamp01(d_value / (d_value + r_value + eps))


def theta_score(
    *,
    distinguishability: Any,
    dim_obs: Any,
    complexity: Any,
    broadcast: Any,
    self_reference: Any,
    phi_eff_value: Any,
    balance: Any,
    balance_min: float = 0.12,
    balance_max: float = 0.90,
    weights: tuple[float, float, float, float, float, float] = (1, 1, 1, 1, 1, 1),
) -> float:
    d_value = clamp01(distinguishability)
    dim_value = dim_obs_score(dim_obs)
    c_value = clamp01(complexity)
    b_value = clamp01(broadcast)
    sr_value = clamp01(self_reference)
    phi_value = clamp01(phi_eff_value)
    gate = 1.0 if balance_min < clamp01(balance) < balance_max else 0.0
    a, b, c, d, e, f = [safe_number(item, 1.0) for item in weights]
    return clamp01(
        (d_value**a)
        * (dim_value**b)
        * (c_value**c)
        * (b_value**d)
        * (sr_value**e)
        * (phi_value**f)
        * gate
    )
