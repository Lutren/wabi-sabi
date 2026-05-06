from __future__ import annotations

import math
from dataclasses import asdict, dataclass
from typing import Any, Dict, Iterable, List, Mapping, Sequence

from .operator_profile import OperatorProfile


@dataclass(frozen=True)
class CijEdge:
    source_id: str
    target_id: str
    source_title: str
    target_title: str
    c_ij: float
    vector_cosine: float
    concept_jaccard: float
    shared_operators: List[str]

    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        for key in ("c_ij", "vector_cosine", "concept_jaccard"):
            data[key] = round(float(data[key]), 4)
        return data


class OperatorTopology:
    """Computes a bounded operator-proximity graph.

    `C_ij` is an operational proxy over extracted `K_source` profiles. It is
    not proof of physical, cognitive or social equivalence.
    """

    schema = "obs_info_kernel.operator_topology.v1"
    claim_boundary = "C_ij is a local operator-proximity proxy, not evidence of isomorphism or new physics."

    def build(self, profiles: Sequence[OperatorProfile], threshold: float = 0.15) -> Dict[str, Any]:
        nodes = [self._node(profile) for profile in profiles]
        edges: List[CijEdge] = []
        for idx, left in enumerate(profiles):
            for right in profiles[idx + 1 :]:
                edge = self.compare(left, right)
                if edge.c_ij >= threshold:
                    edges.append(edge)
        edges.sort(key=lambda edge: edge.c_ij, reverse=True)
        return {
            "schema": self.schema,
            "status": "OPERATIONAL_PROXY_NOT_PROOF",
            "claim_boundary": self.claim_boundary,
            "nodes": nodes,
            "edges": [edge.to_dict() for edge in edges],
            "threshold": threshold,
        }

    def compare(self, left: OperatorProfile, right: OperatorProfile) -> CijEdge:
        vector_cosine = _cosine(left.k_vector, right.k_vector)
        concept_jaccard = _jaccard(left.concepts[:30], right.concepts[:30])
        shared_operators = sorted(
            op
            for op in set(left.k_vector).intersection(right.k_vector)
            if left.k_vector.get(op, 0.0) > 0.0 and right.k_vector.get(op, 0.0) > 0.0
        )
        shared_bonus = min(0.15, 0.03 * len(shared_operators))
        c_ij = _clamp((0.65 * vector_cosine) + (0.25 * concept_jaccard) + shared_bonus)
        return CijEdge(
            source_id=left.source_id,
            target_id=right.source_id,
            source_title=left.title,
            target_title=right.title,
            c_ij=c_ij,
            vector_cosine=vector_cosine,
            concept_jaccard=concept_jaccard,
            shared_operators=shared_operators,
        )

    def _node(self, profile: OperatorProfile) -> Dict[str, Any]:
        active_operators = sorted(op for op, value in profile.k_vector.items() if value > 0.0)
        return {
            "source_id": profile.source_id,
            "title": profile.title,
            "domain": profile.domain,
            "active_operators": active_operators,
            "r_source": round(float(profile.r_source), 4),
            "phi_source": round(float(profile.phi_source), 4),
            "epistemic_status": profile.epistemic_status,
        }


def _cosine(left: Mapping[str, float], right: Mapping[str, float]) -> float:
    keys = set(left).union(right)
    if not keys:
        return 0.0
    dot = sum(float(left.get(key, 0.0)) * float(right.get(key, 0.0)) for key in keys)
    left_norm = math.sqrt(sum(float(left.get(key, 0.0)) ** 2 for key in keys))
    right_norm = math.sqrt(sum(float(right.get(key, 0.0)) ** 2 for key in keys))
    if left_norm <= 0.0 or right_norm <= 0.0:
        return 0.0
    return _clamp(dot / (left_norm * right_norm))


def _jaccard(left: Iterable[str], right: Iterable[str]) -> float:
    a = {item for item in left if item}
    b = {item for item in right if item}
    if not a and not b:
        return 0.0
    return _clamp(len(a.intersection(b)) / max(1, len(a.union(b))))


def _clamp(value: float, lo: float = 0.0, hi: float = 1.0) -> float:
    return max(lo, min(hi, float(value)))
