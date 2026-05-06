from __future__ import annotations

import math
from collections import Counter
from typing import Any, Mapping


DEFAULT_RUNTIME_WEIGHTS = {
    "failures": 0.25,
    "redundancy": 0.20,
    "contradictions": 0.25,
    "open_pending": 0.15,
    "blocked_actions": 0.15,
}


class EORCalculator:
    """Operational EOR utilities.

    EOR here means residual uncertainty for an observer/model over a corpus.
    It does not claim to measure physical entropy.
    """

    @staticmethod
    def shannon_entropy(counts: Mapping[Any, int | float]) -> float:
        total = sum(float(v) for v in counts.values() if float(v) > 0)
        if total <= 0:
            return 0.0
        entropy = 0.0
        for value in counts.values():
            count = float(value)
            if count <= 0:
                continue
            p = count / total
            entropy -= p * math.log2(p)
        return entropy

    @staticmethod
    def normalized_conditional_entropy(joint_counts: Mapping[tuple[Any, Any], int | float]) -> float:
        """Approximate R_info = H(M|X) / H(M).

        The keys are `(phenomenon_m, representation_x)` pairs. This is a graph
        or corpus proxy, not a physical entropy measurement.
        """

        joint = Counter()
        m_counts: Counter[Any] = Counter()
        x_counts: Counter[Any] = Counter()

        for key, value in joint_counts.items():
            if not isinstance(key, tuple) or len(key) != 2:
                raise ValueError("joint_counts keys must be (phenomenon, representation) tuples")
            count = float(value)
            if count <= 0:
                continue
            m, x = key
            joint[(m, x)] += count
            m_counts[m] += count
            x_counts[x] += count

        h_m = EORCalculator.shannon_entropy(m_counts)
        if h_m <= 0:
            return 0.0

        total = sum(joint.values())
        h_m_given_x = 0.0
        for x, x_count in x_counts.items():
            local_m = Counter()
            for (m, x2), count in joint.items():
                if x2 == x:
                    local_m[m] += count
            h_m_given_x += (x_count / total) * EORCalculator.shannon_entropy(local_m)

        return _clamp(h_m_given_x / h_m)

    @staticmethod
    def operational_residue(
        *,
        failures: float = 0.0,
        redundancy: float = 0.0,
        contradictions: float = 0.0,
        open_pending: float = 0.0,
        blocked_actions: float = 0.0,
        total_events: float | None = None,
        weights: Mapping[str, float] | None = None,
    ) -> float:
        """Compute a bounded R_operational proxy for agent runtime state."""

        components = {
            "failures": failures,
            "redundancy": redundancy,
            "contradictions": contradictions,
            "open_pending": open_pending,
            "blocked_actions": blocked_actions,
        }
        normalized = {
            key: _normalize_component(value, total_events)
            for key, value in components.items()
        }
        return EORCalculator.weighted_residue(normalized, weights or DEFAULT_RUNTIME_WEIGHTS)

    @staticmethod
    def weighted_residue(
        components: Mapping[str, float],
        weights: Mapping[str, float] | None = None,
    ) -> float:
        """Combine already normalized residue components into 0..1."""

        chosen = weights or {key: 1.0 for key in components}
        total_weight = sum(max(0.0, float(w)) for w in chosen.values())
        if total_weight <= 0:
            return 0.0
        score = 0.0
        for key, value in components.items():
            weight = max(0.0, float(chosen.get(key, 0.0)))
            score += weight * _clamp(value)
        return _clamp(score / total_weight)

    @staticmethod
    def total_residue(components: Mapping[str, float], weights: Mapping[str, float] | None = None) -> float:
        """Combine R_info, R_operational, R_dark, R_anti or similar layers."""

        return EORCalculator.weighted_residue(components, weights)

    @staticmethod
    def phi_eff(r_total: float, j_c: float = 0.60) -> float:
        if j_c <= 0:
            return 0.0
        return _clamp(1.0 - float(r_total) / float(j_c))


def _normalize_component(value: float, total_events: float | None) -> float:
    if total_events and total_events > 0:
        return _clamp(float(value) / float(total_events))
    return _clamp(value)


def _clamp(value: float, lo: float = 0.0, hi: float = 1.0) -> float:
    return max(lo, min(hi, float(value)))
