"""Core contracts for a safe Observacionista integration kernel.

The package is intentionally dependency-light and local-first.
It does not execute shell/browser/network actions; it only scores,
logs, gates, and produces immutable receipts.
"""
from __future__ import annotations

from dataclasses import dataclass, field, asdict
from enum import Enum
from typing import Any, Dict, List, Literal, Optional
import hashlib
import json
import re
import time
import uuid

ObservationMode = Literal[
    "api",
    "reader",
    "browser_snapshot",
    "browser_action",
    "pdf",
    "manual",
    "code",
    "test",
]


class Regime(str, Enum):
    CLEAR = "CLEAR"
    WATCH = "WATCH"
    PRE_JAMMING = "PRE_JAMMING"
    JAMMING = "JAMMING"


@dataclass
class ObservationEnvelope:
    """Universal observation object.

    Every external result, browser state, code diff, test output or manual note
    should be normalized to this format before an agent uses it.
    """

    source: str
    url: str = ""
    mode: ObservationMode = "manual"
    title: str = ""
    text: str = ""
    raw: Dict[str, Any] = field(default_factory=dict)
    extracted: Dict[str, Any] = field(default_factory=dict)

    timestamp: float = field(default_factory=time.time)
    content_hash: str = ""
    source_confidence: float = 0.0
    calibration_epsilon: float = 0.0
    r_cost: float = 0.0
    phi_gain: float = 0.0
    token_estimate: int = 0

    evidence: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def finalize(self) -> "ObservationEnvelope":
        payload = json.dumps(
            {
                "source": self.source,
                "url": self.url,
                "mode": self.mode,
                "title": self.title,
                "text": self.text[:8000],
                "extracted": self.extracted,
                "raw_digest": stable_hash(self.raw) if self.raw else "",
            },
            ensure_ascii=False,
            sort_keys=True,
            default=str,
        )
        self.content_hash = hashlib.sha256(payload.encode("utf-8")).hexdigest()
        self.token_estimate = max(1, len(self.text) // 4)
        if not self.source_confidence:
            self.source_confidence = infer_source_confidence(self.source, self.url, self.mode)
        if not self.calibration_epsilon:
            self.calibration_epsilon = infer_calibration_epsilon(self)
        if not self.r_cost:
            self.r_cost = estimate_r_cost(self)
        if not self.phi_gain:
            self.phi_gain = estimate_phi_gain(self)
        return self

    @property
    def observation_id(self) -> str:
        if not self.content_hash:
            self.finalize()
        return f"obs_{self.content_hash[:16]}"

    def to_dict(self) -> Dict[str, Any]:
        if not self.content_hash:
            self.finalize()
        return asdict(self)


@dataclass
class EstadoPSI:
    """Operational state of an observer/agent/session.

    R: accumulated unresolved residue/risk/cost.
    Phi_eff: useful integration efficiency.
    J_c: jamming threshold.
    epsilon: intent-action/source-output divergence.
    """

    session_id: str = field(default_factory=lambda: f"sess_{uuid.uuid4().hex[:12]}")
    topic: str = ""
    R: float = 0.0
    Phi_eff: float = 1.0
    J_c: float = 0.60
    epsilon: float = 0.0
    pending_count: int = 0
    reopened_decisions: int = 0
    duplicate_ratio: float = 0.0
    failures: int = 0
    useful_events: int = 0
    total_events: int = 0
    signals: List[str] = field(default_factory=list)
    started_at: float = field(default_factory=time.time)

    def regime(self) -> Regime:
        if self.R >= self.J_c or len(self.signals) >= 5:
            return Regime.JAMMING
        if self.R >= 0.45 or self.epsilon >= 0.55 or len(self.signals) >= 3:
            return Regime.PRE_JAMMING
        if self.R >= 0.30 or self.Phi_eff <= 0.55:
            return Regime.WATCH
        return Regime.CLEAR

    def add_signal(self, signal: str) -> None:
        if signal not in self.signals:
            self.signals.append(signal)

    def absorb_observation(self, obs: ObservationEnvelope) -> None:
        obs.finalize()
        self.total_events += 1
        if obs.phi_gain > obs.r_cost:
            self.useful_events += 1
        else:
            self.failures += 1
            self.add_signal("low_phi_gain")

        # Controlled update: R rises with cost/epsilon/duplication and is relieved by Phi.
        residue_input = clamp(obs.r_cost + 0.5 * obs.calibration_epsilon + 0.25 * self.duplicate_ratio, 0.0, 1.0)
        relief = clamp(obs.phi_gain * 0.25, 0.0, 0.25)
        self.R = clamp(self.R + 0.18 * residue_input * (1.0 - self.R) - relief * self.R, 0.0, 1.0)
        self.Phi_eff = clamp(0.75 * self.Phi_eff + 0.25 * obs.phi_gain - 0.10 * obs.calibration_epsilon, 0.0, 1.0)

        if obs.token_estimate > 4000:
            self.add_signal("large_context")
        if obs.calibration_epsilon > 0.55:
            self.add_signal("high_calibration_epsilon")
        if obs.r_cost > 0.45:
            self.add_signal("high_r_cost")

    def update_epsilon(self, epsilon: float) -> None:
        self.epsilon = clamp(epsilon, 0.0, 1.0)
        if self.epsilon > 0.55:
            self.add_signal("intent_action_drift")
            self.R = clamp(self.R + 0.10 * self.epsilon, 0.0, 1.0)

    def should_compact(self) -> bool:
        return (
            self.R > 0.35
            or self.duplicate_ratio > 0.50
            or len(self.signals) >= 3
            or self.regime() in {Regime.PRE_JAMMING, Regime.JAMMING}
        )

    def fingerprint(self) -> str:
        payload = json.dumps(
            {
                "session_id": self.session_id,
                "topic": self.topic,
                "R": round(self.R, 4),
                "Phi_eff": round(self.Phi_eff, 4),
                "epsilon": round(self.epsilon, 4),
                "pending_count": self.pending_count,
                "reopened_decisions": self.reopened_decisions,
                "signals": sorted(self.signals),
                "regime": self.regime().value,
            },
            sort_keys=True,
            ensure_ascii=False,
        )
        return hashlib.sha256(payload.encode("utf-8")).hexdigest()

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d["regime"] = self.regime().value
        d["fingerprint"] = self.fingerprint()
        d["should_compact"] = self.should_compact()
        return d


def clamp(x: float, lo: float, hi: float) -> float:
    return max(lo, min(hi, x))


def stable_hash(value: Any) -> str:
    payload = json.dumps(value, sort_keys=True, ensure_ascii=False, default=str)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def infer_source_confidence(source: str, url: str, mode: str) -> float:
    s = f"{source} {url}".lower()
    if any(x in s for x in ["arxiv", "openalex", "semanticscholar", "pubmed", "doi.org", "github.com"]):
        base = 0.86
    elif mode == "api":
        base = 0.78
    elif mode == "reader":
        base = 0.68
    elif mode.startswith("browser"):
        base = 0.55
    else:
        base = 0.50
    return clamp(base, 0.0, 1.0)


def infer_calibration_epsilon(obs: ObservationEnvelope) -> float:
    text = obs.text or ""
    epsilon = 0.25
    if obs.mode == "api":
        epsilon -= 0.08
    if obs.mode == "browser_action":
        epsilon += 0.20
    if obs.mode == "browser_snapshot":
        epsilon += 0.12
    if len(text) < 200:
        epsilon += 0.12
    if len(text) > 12000:
        epsilon += 0.15
    if not obs.evidence and obs.mode not in {"manual", "code", "test"}:
        epsilon += 0.12
    # Penalize raw HTML/script-heavy captures.
    script_count = len(re.findall(r"<script|function\s*\(|window\.", text, flags=re.I))
    if script_count:
        epsilon += min(0.25, 0.03 * script_count)
    return clamp(epsilon, 0.0, 1.0)


def estimate_r_cost(obs: ObservationEnvelope) -> float:
    token_cost = min(0.35, obs.token_estimate / 24000)
    mode_cost = {
        "api": 0.06,
        "reader": 0.10,
        "pdf": 0.14,
        "browser_snapshot": 0.22,
        "browser_action": 0.40,
        "manual": 0.08,
        "code": 0.18,
        "test": 0.12,
    }.get(obs.mode, 0.16)
    weak_source = 0.12 * (1.0 - obs.source_confidence)
    return clamp(mode_cost + token_cost + weak_source + 0.25 * obs.calibration_epsilon, 0.0, 1.0)


def estimate_phi_gain(obs: ObservationEnvelope) -> float:
    text = obs.text or ""
    if not text and not obs.extracted:
        return 0.05
    density = min(0.30, len(set(re.findall(r"\w{5,}", text.lower()))) / 4000)
    evidence_bonus = min(0.25, 0.05 * len(obs.evidence))
    structured_bonus = 0.18 if obs.extracted else 0.0
    confidence_bonus = 0.25 * obs.source_confidence
    penalty = 0.30 * obs.calibration_epsilon
    return clamp(0.10 + density + evidence_bonus + structured_bonus + confidence_bonus - penalty, 0.0, 1.0)
