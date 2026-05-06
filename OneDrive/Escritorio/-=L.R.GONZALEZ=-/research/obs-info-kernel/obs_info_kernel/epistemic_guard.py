from __future__ import annotations

import re
from dataclasses import dataclass, field
from enum import Enum
from typing import Iterable, List, Optional


class ClaimStatus(str, Enum):
    DEFINITIONAL = "A_definicional"
    OPERATIONAL = "D_operativo"
    CONJECTURAL = "C_conjetural"
    PHYSICAL_HYPOTHESIS = "H_hipotesis_fisica"
    METAPHORICAL = "M_metaforico"
    BLOCKED = "X_bloqueado"


@dataclass
class Claim:
    text: str
    status: ClaimStatus
    domain: str
    evidence: List[str] = field(default_factory=list)
    test_required: Optional[str] = None
    risk: float = 0.0


class EpistemicGuard:
    """Classify claims so analogies do not become public proof claims."""

    DANGEROUS_PATTERNS = [
        "es identico a",
        "es idéntico a",
        "prueba que",
        "demuestra",
        "resuelve la fisica",
        "resuelve la física",
        "redefine la entropia",
        "redefine la entropía",
        "la entropia es",
        "la entropía es",
        "la mecanica cuantica es",
        "la mecánica cuántica es",
    ]
    BLOCKED_PATTERNS = [
        "controlar r es controlar la realidad",
        "el residuo r es la variable que une la fisica",
        "el residuo r es la variable que une la física",
        "la entropia ahora tiene dueno",
        "la entropía ahora tiene dueño",
    ]
    PHYSICAL_DOMAINS = {
        "fisica",
        "física",
        "cosmologia",
        "cosmología",
        "cuantica",
        "cuántica",
        "termodinamica",
        "termodinámica",
        "physics",
        "cosmology",
        "quantum",
        "thermodynamics",
    }

    def classify(self, claim_text: str, domain: str = "unknown", evidence: Iterable[str] | None = None) -> Claim:
        lower = claim_text.casefold()
        matched = [pattern for pattern in self.DANGEROUS_PATTERNS if pattern in lower]
        blocked = [pattern for pattern in self.BLOCKED_PATTERNS if pattern in lower]
        risk = min(1.0, (len(matched) / max(1, len(self.DANGEROUS_PATTERNS))) + (0.50 if blocked else 0.0))
        ev = list(evidence or [])
        normalized_domain = domain.casefold()

        if blocked:
            return Claim(
                text=claim_text,
                status=ClaimStatus.BLOCKED,
                domain=domain,
                evidence=ev,
                test_required="Rewrite before canon or public use; this overstates the framework.",
                risk=max(0.90, risk),
            )

        if matched and normalized_domain in self.PHYSICAL_DOMAINS:
            return Claim(
                text=claim_text,
                status=ClaimStatus.PHYSICAL_HYPOTHESIS,
                domain=domain,
                evidence=ev,
                test_required="Requires falsifiable prediction and comparison with standard domain models.",
                risk=max(0.60, risk),
            )

        if _contains_any(lower, ["proxy", "metrica operacional", "métrica operacional", "runtime", "corpus"]):
            return Claim(text=claim_text, status=ClaimStatus.OPERATIONAL, domain=domain, evidence=ev, risk=risk)

        if _contains_any(lower, ["definimos", "se define", "por definicion", "por definición"]):
            return Claim(text=claim_text, status=ClaimStatus.DEFINITIONAL, domain=domain, evidence=ev, risk=risk)

        if _contains_any(lower, ["analog", "analogia", "analogía", "metafora", "metáfora", "resonancia"]):
            return Claim(text=claim_text, status=ClaimStatus.METAPHORICAL, domain=domain, evidence=ev, risk=risk)

        return Claim(
            text=claim_text,
            status=ClaimStatus.CONJECTURAL,
            domain=domain,
            evidence=ev,
            test_required="Requires domain validation before runtime or public-copy promotion.",
            risk=risk,
        )

    def safe_rewrite(self, claim: Claim) -> str:
        text = claim.text
        replacements = {
            r"prueba que": "sugiere como hipotesis que",
            r"demuestra": "propone evaluar",
            r"es idéntico a": "puede modelarse parcialmente como",
            r"es identico a": "puede modelarse parcialmente como",
            r"redefine la entropía": "propone una metrica relacional compatible con teoria de informacion",
            r"redefine la entropia": "propone una metrica relacional compatible con teoria de informacion",
            r"la entropía es": "una capa informacional de R puede modelarse como",
            r"la entropia es": "una capa informacional de R puede modelarse como",
            r"controlar R es controlar la realidad observable": "reducir R mejora la calidad operacional de observacion",
            r"controlar r es controlar la realidad observable": "reducir R mejora la calidad operacional de observacion",
        }
        for pattern, replacement in replacements.items():
            text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)

        if claim.status == ClaimStatus.PHYSICAL_HYPOTHESIS:
            return "Hipotesis de investigacion: " + text
        if claim.status == ClaimStatus.BLOCKED:
            return "Version segura pendiente: " + text
        return text


def _contains_any(text: str, candidates: Iterable[str]) -> bool:
    return any(candidate in text for candidate in candidates)
