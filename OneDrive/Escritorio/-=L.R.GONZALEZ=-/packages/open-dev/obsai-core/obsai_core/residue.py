from __future__ import annotations

from dataclasses import dataclass, field
from time import time
from typing import Literal

from .metrics import phi_eff_power


ResidueKind = Literal[
    "uncertainty",
    "contradiction",
    "missing_evidence",
    "failed_test",
    "overload",
    "calibration_gap",
    "unresolved_task",
    "operator_loss",
    "unknown",
]


@dataclass
class ResidueItem:
    message: str
    kind: ResidueKind = "unknown"
    weight: float = 0.05
    evidence: list[str] = field(default_factory=list)
    tags: list[str] = field(default_factory=list)
    created_at: float = field(default_factory=time)
    resolved: bool = False

    def to_dict(self) -> dict:
        return {
            "message": self.message,
            "kind": self.kind,
            "weight": self.weight,
            "evidence": self.evidence,
            "tags": self.tags,
            "createdAt": self.created_at,
            "resolved": self.resolved,
        }


class ResidueTracker:
    def __init__(self, jamming_threshold: float = 1.0):
        if jamming_threshold <= 0:
            raise ValueError("jamming_threshold must be positive")
        self.jamming_threshold = float(jamming_threshold)
        self.items: list[ResidueItem] = []

    def add(
        self,
        message: str,
        kind: ResidueKind = "unknown",
        weight: float = 0.05,
        evidence: list[str] | None = None,
        tags: list[str] | None = None,
    ) -> ResidueItem:
        item = ResidueItem(
            message=message,
            kind=kind,
            weight=max(0.0, float(weight)),
            evidence=evidence or [],
            tags=tags or [],
        )
        self.items.append(item)
        return item

    def resolve(self, index: int) -> None:
        self.items[index].resolved = True

    def unresolved(self) -> list[ResidueItem]:
        return [item for item in self.items if not item.resolved]

    @property
    def residue(self) -> float:
        return min(self.jamming_threshold, sum(item.weight for item in self.unresolved()))

    @property
    def phi_eff(self) -> float:
        return phi_eff_power(self.residue, jamming_threshold=self.jamming_threshold)

    def by_kind(self) -> dict[str, float]:
        output: dict[str, float] = {}
        for item in self.unresolved():
            output[item.kind] = output.get(item.kind, 0.0) + item.weight
        return output

    def report(self) -> dict:
        return {
            "R": self.residue,
            "J_c": self.jamming_threshold,
            "phi_eff": self.phi_eff,
            "unresolvedCount": len(self.unresolved()),
            "byKind": self.by_kind(),
            "items": [item.to_dict() for item in self.unresolved()],
        }
