from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Iterable, Mapping

from .metrics import clamp01


@dataclass(frozen=True)
class SignalPacket:
    """Software-only signal packet for selective action routing."""

    signal_type: str
    intensity: float = 1.0
    payload: Mapping[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class CapabilityReceptor:
    receptor_id: str
    accepts: tuple[str, ...]
    lane: str = "general"
    threshold: float = 0.5
    required_capability: str = ""
    authorized: bool = True
    private_boundary: bool = False
    selectivity: float = 1.0
    calibration: float = 1.0

    def accepts_signal(self, packet: SignalPacket) -> bool:
        accepted = "*" in self.accepts or packet.signal_type in self.accepts
        return bool(self.authorized and accepted and clamp01(packet.intensity) >= clamp01(self.threshold))


def transduce_signal(packet: SignalPacket, receptors: Iterable[CapabilityReceptor]) -> dict[str, Any]:
    candidates: list[dict[str, Any]] = []
    for receptor in receptors:
        signal_match = "*" in receptor.accepts or packet.signal_type in receptor.accepts
        score = (
            clamp01(packet.intensity)
            * clamp01(receptor.selectivity)
            * clamp01(receptor.calibration)
        )
        candidates.append(
            {
                "receptor_id": receptor.receptor_id,
                "lane": receptor.lane,
                "signal_match": signal_match,
                "accepted": receptor.accepts_signal(packet),
                "authorized": receptor.authorized,
                "private_boundary": receptor.private_boundary,
                "score": score,
            }
        )

    accepted = [item for item in candidates if item["accepted"]]
    return {
        "schemaVersion": "obsai.transduction.v1",
        "signal_type": packet.signal_type,
        "accepted": bool(accepted),
        "active_receptors": accepted,
        "candidates": candidates,
        "claims": {
            "patentPatternUse": "ABSTRACT_SOFTWARE_PATTERN_ONLY",
            "legalStatus": "LEGAL_REVIEW_REQUIRED",
        },
    }


class ResidueAwareAttentionGate:
    def __init__(self, threshold: float = 0.35, residue_weight: float = 0.65) -> None:
        self.threshold = clamp01(threshold)
        self.residue_weight = clamp01(residue_weight)

    def score(self, item: Mapping[str, Any]) -> float:
        relevance = clamp01(item.get("relevance", item.get("similarity", 0.0)))
        authority = clamp01(item.get("authority", item.get("authority_score", 0.5)))
        freshness = clamp01(item.get("freshness", 0.5))
        residue = clamp01(item.get("residue", item.get("R", 0.0)))
        return clamp01((0.50 * relevance + 0.35 * authority + 0.15 * freshness) * (1.0 - residue * self.residue_weight))

    def admit(self, item: Mapping[str, Any]) -> dict[str, Any]:
        score = self.score(item)
        return {
            "admitted": score >= self.threshold,
            "attention_score": score,
            "threshold": self.threshold,
        }


def page_rank(graph: Mapping[str, Iterable[str]], damping: float = 0.85, iterations: int = 30) -> dict[str, float]:
    nodes = sorted({str(node) for node in graph} | {str(dest) for dests in graph.values() for dest in dests})
    if not nodes:
        return {}
    damping = clamp01(damping)
    scores = {node: 1.0 / len(nodes) for node in nodes}
    outgoing = {node: [str(dest) for dest in graph.get(node, [])] for node in nodes}

    for _ in range(max(1, int(iterations))):
        base = (1.0 - damping) / len(nodes)
        next_scores = {node: base for node in nodes}
        for node in nodes:
            links = outgoing[node]
            if not links:
                share = scores[node] / len(nodes)
                for dest in nodes:
                    next_scores[dest] += damping * share
                continue
            share = scores[node] / len(links)
            for dest in links:
                if dest in next_scores:
                    next_scores[dest] += damping * share
        scores = next_scores

    total = sum(scores.values()) or 1.0
    return {node: value / total for node, value in scores.items()}


@dataclass(frozen=True)
class RetrievalCandidate:
    candidate_id: str
    similarity: float
    authority: float = 0.5
    freshness: float = 0.5
    residue: float = 0.0
    metadata: Mapping[str, Any] = field(default_factory=dict)


class RAGCalibrationRouter:
    def __init__(self, residue_penalty: float = 0.45) -> None:
        self.residue_penalty = clamp01(residue_penalty)

    def score(self, candidate: RetrievalCandidate) -> float:
        return clamp01(
            0.50 * clamp01(candidate.similarity)
            + 0.30 * clamp01(candidate.authority)
            + 0.20 * clamp01(candidate.freshness)
            - self.residue_penalty * clamp01(candidate.residue)
        )

    def rank(self, candidates: Iterable[RetrievalCandidate]) -> list[dict[str, Any]]:
        ranked = [
            {
                "candidate_id": candidate.candidate_id,
                "score": self.score(candidate),
                "metadata": dict(candidate.metadata),
            }
            for candidate in candidates
        ]
        return sorted(ranked, key=lambda item: item["score"], reverse=True)
