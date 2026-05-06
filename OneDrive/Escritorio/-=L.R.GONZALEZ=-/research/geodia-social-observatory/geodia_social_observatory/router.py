"""Observation router for local motor routes."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from enum import Enum
from typing import Any

from .contracts import ROUTE_DECISION_SCHEMA
from .snapshot import canonical_sha256


class Route(str, Enum):
    CACHE = "cache"
    SMALL = "small"
    STRONG = "strong"
    SIM = "sim"
    HUMAN = "human"


@dataclass(frozen=True)
class RequestFeatures:
    novelty: float = 0.0
    uncertainty: float = 0.0
    auth_drift: float = 0.0
    impact: float = 0.0
    cache_hit_prob: float = 0.0
    artifact_conf: float = 0.0
    simulator_needed: float = 0.0
    policy_risk: float = 0.0
    needs_tool: bool = False
    multimodal: bool = False


def decide_route(features: RequestFeatures) -> dict[str, Any]:
    reasons: list[str] = []
    route = Route.SMALL
    requires_approval = False
    if features.policy_risk >= 0.8 or features.auth_drift >= 0.7:
        route = Route.HUMAN
        requires_approval = True
        reasons.append("high policy risk or behavioral drift")
    elif features.simulator_needed >= 0.65:
        route = Route.SIM
        reasons.append("claim requires simulation before inference")
    elif features.cache_hit_prob >= 0.97 and features.impact < 0.5 and features.policy_risk < 0.4:
        route = Route.CACHE
        reasons.append("exact or high-confidence cache route")
    elif features.artifact_conf >= 0.88 and features.uncertainty < 0.45:
        route = Route.CACHE
        reasons.append("artifact memory confidence is high")
    elif features.impact >= 0.65 or features.uncertainty >= 0.65 or features.multimodal:
        route = Route.STRONG
        reasons.append("high impact, high uncertainty or multimodal request")
    else:
        route = Route.SMALL
        reasons.append("routine request with bounded uncertainty")

    payload = {
        "features": asdict(features),
        "route": route.value,
        "requires_approval": requires_approval,
        "reasons": reasons,
        "claim_boundary": "router is a local cost-risk gate; heavy models remain blocked unless host gate approves",
    }
    return {
        "schema": ROUTE_DECISION_SCHEMA,
        "decision_id": "rte_" + canonical_sha256(payload)[:16],
        **payload,
    }


def features_from_mapping(value: dict[str, Any]) -> RequestFeatures:
    allowed = {field.name for field in RequestFeatures.__dataclass_fields__.values()}
    return RequestFeatures(**{key: value[key] for key in value if key in allowed})
