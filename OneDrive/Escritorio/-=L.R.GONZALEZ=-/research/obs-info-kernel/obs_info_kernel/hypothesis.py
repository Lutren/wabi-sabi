from __future__ import annotations

import hashlib
from dataclasses import asdict, dataclass
from typing import Any, Dict, Iterable, List

from .epistemic_guard import EpistemicGuard
from .operator_profile import OperatorProfile


@dataclass(frozen=True)
class Hypothesis:
    id: str
    text: str
    linked_domains: List[str]
    delta_r: float
    transfer_span: float
    testability: float
    orphanhood: float
    overclaim_risk: float
    priority: float
    falsifier: str
    status: str

    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        for key in ["delta_r", "transfer_span", "testability", "orphanhood", "overclaim_risk", "priority"]:
            data[key] = round(float(data[key]), 4)
        return data


class HypothesisScorer:
    """Scores hypotheses by residue reduction, transfer, testability and risk."""

    def __init__(self):
        self.guard = EpistemicGuard()

    def priority(
        self,
        *,
        delta_r: float,
        transfer_span: float,
        testability: float,
        orphanhood: float,
        overclaim_risk: float,
    ) -> float:
        score = (
            _clamp(delta_r)
            * _clamp(transfer_span)
            * _clamp(testability)
            * _clamp(orphanhood)
            * (1.0 - _clamp(overclaim_risk))
        )
        return _clamp(score)

    def from_finding(self, finding: Dict[str, Any], profiles: Iterable[OperatorProfile]) -> Hypothesis:
        profiles = list(profiles)
        title = str(finding.get("title") or "Untitled hypothesis")
        payload = finding.get("payload") or {}
        linked_source_ids = set(finding.get("sources") or [])
        linked_profiles = [profile for profile in profiles if profile.source_id in linked_source_ids] or profiles
        domains = sorted({profile.domain for profile in linked_profiles})
        delta_r = _clamp(float(finding.get("score", 0.0)) * 0.50)
        transfer_span = _clamp(len(domains) / max(1, len({profile.domain for profile in profiles}) or 1))
        testability = _infer_testability(finding)
        orphanhood = _infer_orphanhood(finding, payload)
        claim = self.guard.classify(title, domains[0] if domains else "unknown")
        overclaim = max(float(getattr(claim, "risk", 0.0)), _overclaim_from_text(title))
        priority = self.priority(
            delta_r=delta_r,
            transfer_span=transfer_span,
            testability=testability,
            orphanhood=orphanhood,
            overclaim_risk=overclaim,
        )
        hid = hashlib.sha256(f"{title}|{domains}".encode("utf-8", errors="ignore")).hexdigest()[:12]
        return Hypothesis(
            id=f"hyp-{hid}",
            text=title,
            linked_domains=domains,
            delta_r=delta_r,
            transfer_span=transfer_span,
            testability=testability,
            orphanhood=orphanhood,
            overclaim_risk=overclaim,
            priority=priority,
            falsifier="Define a small corpus test: if adding this hypothesis does not reduce R_graph or produce a transferable prediction, reject it.",
            status=claim.status.value,
        )

    def from_findings(self, findings: List[Dict[str, Any]], profiles: Iterable[OperatorProfile], limit: int = 20) -> List[Hypothesis]:
        hypotheses = [self.from_finding(finding, profiles) for finding in findings[:limit]]
        hypotheses.sort(key=lambda item: item.priority, reverse=True)
        return hypotheses


def _infer_testability(finding: Dict[str, Any]) -> float:
    payload = finding.get("payload") or {}
    if "testability" in payload:
        try:
            return _clamp(float(payload["testability"]))
        except Exception:
            pass
    text = " ".join([str(finding.get("title", "")), " ".join(str(e) for e in finding.get("evidence", [])[:3])]).lower()
    markers = ["test", "prueba", "experiment", "experimento", "prediction", "prediccion", "benchmark", "dataset", "fals"]
    hits = sum(1 for marker in markers if marker in text)
    return max(0.20, min(1.0, hits / 4.0))


def _infer_orphanhood(finding: Dict[str, Any], payload: Dict[str, Any]) -> float:
    if "orphanhood" in payload:
        try:
            return _clamp(float(payload["orphanhood"]))
        except Exception:
            pass
    if finding.get("kind") == "dark_information":
        return 0.70
    if finding.get("kind") == "calibration_gap":
        return 0.55
    return 0.40


def _overclaim_from_text(text: str) -> float:
    lower = text.lower()
    risky = ["proves", "prueba", "demuestra", "resuelve", "redefine", "garantiza", "controls reality", "controlar la realidad"]
    return min(1.0, sum(1 for marker in risky if marker in lower) / 3.0)


def _clamp(value: float) -> float:
    return max(0.0, min(1.0, float(value)))
