from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Dict


@dataclass(frozen=True)
class EquivalenceCheck:
    same_variables: bool
    same_causal_direction: bool
    same_threshold_type: bool
    same_perturbation_response: bool
    comparable_prediction_or_intervention: bool

    @property
    def passed_count(self) -> int:
        return sum(
            [
                self.same_variables,
                self.same_causal_direction,
                self.same_threshold_type,
                self.same_perturbation_response,
                self.comparable_prediction_or_intervention,
            ]
        )

    @property
    def passes(self) -> bool:
        return self.passed_count == 5

    def to_dict(self) -> Dict[str, object]:
        data = asdict(self)
        data["passed_count"] = self.passed_count
        data["passes"] = self.passes
        return data


@dataclass(frozen=True)
class EquivalenceVerdict:
    verdict: str
    check: EquivalenceCheck
    note: str

    def to_dict(self) -> Dict[str, object]:
        return {"verdict": self.verdict, "note": self.note, "check": self.check.to_dict()}


class EquivalenceTester:
    """Operational equivalence test for cross-domain claims."""

    def evaluate(
        self,
        *,
        same_variables: bool,
        same_causal_direction: bool,
        same_threshold_type: bool,
        same_perturbation_response: bool,
        comparable_prediction_or_intervention: bool,
    ) -> EquivalenceVerdict:
        check = EquivalenceCheck(
            same_variables=same_variables,
            same_causal_direction=same_causal_direction,
            same_threshold_type=same_threshold_type,
            same_perturbation_response=same_perturbation_response,
            comparable_prediction_or_intervention=comparable_prediction_or_intervention,
        )
        if check.passes:
            return EquivalenceVerdict(
                verdict="equivalence",
                check=check,
                note="All five operational filters pass.",
            )
        if check.passed_count >= 4:
            return EquivalenceVerdict(
                verdict="partial_translation",
                check=check,
                note="Strong structural overlap, but not enough for equivalence.",
            )
        if check.passed_count >= 2:
            return EquivalenceVerdict(
                verdict="analogy",
                check=check,
                note="Useful analogy only; do not promote to identity.",
            )
        return EquivalenceVerdict(
            verdict="rejected_or_noise",
            check=check,
            note="Insufficient operational overlap.",
        )
