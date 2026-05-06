from __future__ import annotations

import re
from collections import Counter
from dataclasses import asdict, dataclass, field
from typing import Any, Dict, Iterable, List, Mapping

from .calibration import DEFAULT_EQUIVALENCES, CalibrationGapDetector
from .core import Source
from .eor import EORCalculator
from .epistemic_guard import EpistemicGuard
from .text import sentences, tokens, top_terms


CLAIM_MARKERS = [
    "define",
    "definimos",
    "hipotesis",
    "hipótesis",
    "claim",
    "sugiere",
    "propone",
    "demuestra",
    "prueba",
    "is ",
    "es ",
]
METAPHOR_MARKERS = ["como", "as if", "analog", "analogia", "analogía", "metafora", "metáfora"]
EXPERIMENT_MARKERS = ["test", "prueba", "experimento", "experiment", "benchmark", "dataset", "replica", "falsable"]


@dataclass
class OperatorProfile:
    source_id: str
    title: str
    domain: str
    claims: List[str]
    concepts: List[str]
    edges: List[Dict[str, Any]]
    omissions: List[str]
    metaphors: List[str]
    equations: List[str]
    evidence_type: str
    k_vector: Dict[str, float]
    r_source: float
    phi_source: float
    epistemic_status: str
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        data["r_source"] = round(float(self.r_source), 4)
        data["phi_source"] = round(float(self.phi_source), 4)
        data["k_vector"] = {k: round(float(v), 4) for k, v in self.k_vector.items()}
        return data


class OperatorProfiler:
    """Builds K_source: how a source makes a phenomenon legible."""

    def __init__(self, expected_operators: Iterable[str] | None = None):
        self.calibration = CalibrationGapDetector()
        self.guard = EpistemicGuard()
        self.expected_operators = list(expected_operators or DEFAULT_EQUIVALENCES.keys())

    def build(self, source: Source) -> OperatorProfile:
        concepts = [term for term, _ in top_terms(source.text, k=40, max_ngram=2)]
        claims = self._extract_claims(source.text)
        metaphors = self._extract_metaphors(source.text)
        equations = self._extract_equations(source.text)
        evidence_type = self._evidence_type(source, equations)
        k_vector = self._k_vector(source)
        omissions = [op for op in self.expected_operators if k_vector.get(op, 0.0) <= 0.0]
        r_source = self._r_source(k_vector, omissions, evidence_type)
        phi_source = EORCalculator.phi_eff(r_source, j_c=1.0)
        claim_basis = claims[0] if claims else f"{source.title}: {source.domain}"
        status = self.guard.classify(claim_basis, source.domain).status.value
        return OperatorProfile(
            source_id=source.id,
            title=source.title,
            domain=source.domain,
            claims=claims,
            concepts=concepts,
            edges=self._edges(source.text, concepts),
            omissions=omissions,
            metaphors=metaphors,
            equations=equations,
            evidence_type=evidence_type,
            k_vector=k_vector,
            r_source=r_source,
            phi_source=phi_source,
            epistemic_status=status,
            metadata={"char_count": source.char_count, **(source.metadata or {})},
        )

    def build_many(self, sources: List[Source]) -> List[OperatorProfile]:
        return [self.build(source) for source in sources]

    def atlas_summary(self, profiles: List[OperatorProfile]) -> Dict[str, Any]:
        if not profiles:
            return {"profiles": 0, "shared_operators": [], "orphan_operators": [], "domains": []}
        operator_hits: Counter[str] = Counter()
        domains = sorted({profile.domain for profile in profiles})
        for profile in profiles:
            for op, value in profile.k_vector.items():
                if value > 0:
                    operator_hits[op] += 1
        shared = [op for op, count in operator_hits.items() if count >= 2]
        orphan = [op for op, count in operator_hits.items() if count == 1]
        mean_r = sum(profile.r_source for profile in profiles) / len(profiles)
        return {
            "profiles": len(profiles),
            "domains": domains,
            "shared_operators": sorted(shared),
            "orphan_operators": sorted(orphan),
            "mean_r_source": round(mean_r, 4),
            "mean_phi_source": round(1.0 - mean_r, 4),
        }

    def _k_vector(self, source: Source) -> Dict[str, float]:
        canonical = self.calibration.canonicalize_tokens(tokens(source.text))
        counts = Counter(canonical)
        total = max(1, sum(counts.get(op, 0) for op in self.expected_operators))
        return {op: counts.get(op, 0) / total for op in self.expected_operators}

    def _r_source(self, k_vector: Mapping[str, float], omissions: List[str], evidence_type: str) -> float:
        omission_pressure = len(omissions) / max(1, len(self.expected_operators))
        evidence_penalty = 0.0 if evidence_type in {"experiment", "code", "equation"} else 0.10
        weak_vector_penalty = 0.10 if sum(k_vector.values()) <= 0 else 0.0
        return max(0.0, min(1.0, omission_pressure + evidence_penalty + weak_vector_penalty))

    def _extract_claims(self, text: str, limit: int = 8) -> List[str]:
        out = []
        for sentence in sentences(text):
            lower = sentence.lower()
            if any(marker in lower for marker in CLAIM_MARKERS):
                out.append(sentence[:500])
            if len(out) >= limit:
                break
        return out

    def _extract_metaphors(self, text: str, limit: int = 8) -> List[str]:
        out = []
        for sentence in sentences(text):
            lower = sentence.lower()
            if any(marker in lower for marker in METAPHOR_MARKERS):
                out.append(sentence[:500])
            if len(out) >= limit:
                break
        return out

    def _extract_equations(self, text: str, limit: int = 10) -> List[str]:
        patterns = [
            r"\b[A-Za-z][A-Za-z0-9_{}^()|+\-*/ ]{0,40}=\s*[^.;\n]{1,120}",
            r"\bR[_A-Za-z0-9{}^()]*\s*=\s*[^.;\n]{1,120}",
        ]
        found: List[str] = []
        for pattern in patterns:
            for match in re.finditer(pattern, text):
                value = " ".join(match.group(0).split())
                if value not in found:
                    found.append(value[:220])
                if len(found) >= limit:
                    return found
        return found

    def _evidence_type(self, source: Source, equations: List[str]) -> str:
        meta = source.metadata or {}
        if meta.get("evidence_type"):
            return str(meta["evidence_type"])
        lower = source.text.lower()
        if "```" in lower or re.search(r"\bdef\s+\w+\(", lower):
            return "code"
        if any(marker in lower for marker in EXPERIMENT_MARKERS):
            return "experiment"
        if equations:
            return "equation"
        if source.url:
            return "external_text"
        return "essay"

    def _edges(self, text: str, concepts: List[str], limit: int = 80) -> List[Dict[str, Any]]:
        concept_set = {concept for concept in concepts if " " not in concept}
        counts: Counter[tuple[str, str]] = Counter()
        for sentence in sentences(text)[:80]:
            seen = [token for token in tokens(sentence) if token in concept_set]
            for left, right in zip(seen, seen[1:]):
                if left != right:
                    counts[(left, right)] += 1
        return [
            {"source": left, "target": right, "weight": weight}
            for (left, right), weight in counts.most_common(limit)
        ]
