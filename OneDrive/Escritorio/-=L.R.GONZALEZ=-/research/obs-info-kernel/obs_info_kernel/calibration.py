from __future__ import annotations

from collections import Counter, defaultdict
from typing import Dict, Iterable, List, Mapping, Tuple

from .core import Finding, Source
from .text import concept_counter, cosine, normalize, tfidf, tokens


DEFAULT_EQUIVALENCES: Dict[str, List[str]] = {
    "observacion": ["observacion", "observation", "registro", "measurement", "medicion", "witness", "awareness"],
    "residuo": ["residuo", "residue", "carga", "load", "ruido", "noise", "resto", "pendiente"],
    "actualizacion": ["actualizacion", "update", "integracion", "integration", "aprendizaje", "learning"],
    "sesgo": ["sesgo", "bias", "filtro", "filter", "marco", "frame", "prediccion", "prediction"],
    "umbral": ["umbral", "threshold", "jamming", "bloqueo", "blockade", "gate", "compuerta", "restriccion"],
    "calibracion": ["calibracion", "calibration", "alineacion", "alignment", "sincronizacion", "phase", "fase"],
    "operador": ["operador", "operator", "ventana", "window", "agente", "agent", "sujeto", "observer"],
    "continuidad": ["continuidad", "continuity", "handoff", "fingerprint", "memoria", "memory", "persistencia"],
    "oscuridad": ["oscura", "dark", "relegado", "olvidado", "marginal", "abandoned", "orphan", "invisible"],
    "distorsion": ["distorsion", "epsilon", "divergencia", "drift", "amplificacion", "hallucination"],
    "distincion": ["distincion", "distinguibilidad", "distinguish", "separacion", "symmetry", "simetria", "collapse", "colapso"],
}


class CalibrationGapDetector:
    """Detecta brechas de calibracion sin depender de una narrativa humana.

    La capa no-humana aqui es operacional: convierte textos a grafos pobres de
    conceptos y busca invariantes/ausencias, no belleza retorica.
    """

    def __init__(self, equivalences: Mapping[str, List[str]] | None = None):
        self.equivalences: Dict[str, List[str]] = dict(DEFAULT_EQUIVALENCES)
        if equivalences:
            for k, vals in equivalences.items():
                self.equivalences[k] = list({*self.equivalences.get(k, []), *vals})
        self.reverse: Dict[str, str] = {}
        for canonical, variants in self.equivalences.items():
            self.reverse[normalize(canonical)] = canonical
            for v in variants:
                self.reverse[normalize(v)] = canonical

    def canonicalize_tokens(self, ts: Iterable[str]) -> List[str]:
        out = []
        for t in ts:
            nt = normalize(t)
            out.append(self.reverse.get(nt, nt))
        return out

    def concept_presence(self, source: Source) -> Dict[str, List[str]]:
        text = normalize(source.text)
        presence: Dict[str, List[str]] = defaultdict(list)
        for canonical, variants in self.equivalences.items():
            for v in variants + [canonical]:
                nv = normalize(v)
                if nv and nv in text:
                    presence[canonical].append(v)
        return dict(presence)

    def matrix(self, sources: List[Source]) -> List[List[float]]:
        counters = [concept_counter(s.text, max_ngram=1) for s in sources]
        vecs = tfidf(counters)
        return [[round(cosine(a, b), 4) for b in vecs] for a in vecs]

    def detect(self, sources: List[Source], min_sources: int = 2) -> List[Finding]:
        findings: List[Finding] = []
        presences = {s.id: self.concept_presence(s) for s in sources}
        by_concept: Dict[str, Dict[str, List[str]]] = defaultdict(dict)
        for s in sources:
            for c, variants in presences[s.id].items():
                by_concept[c][s.id] = variants

        for concept, per_source in by_concept.items():
            if len(per_source) < min_sources:
                continue
            variant_sets = {sid: sorted(set(vs))[:5] for sid, vs in per_source.items()}
            all_variants = {v for vs in variant_sets.values() for v in vs}
            if len(all_variants) <= 1:
                continue
            titles = [s.title for s in sources if s.id in per_source]
            score = min(1.0, 0.45 + 0.12 * len(per_source) + 0.05 * len(all_variants))
            findings.append(
                Finding(
                    kind="calibration_gap",
                    title=f"Mismo operador conceptual con vocabularios distintos: {concept}",
                    score=score,
                    evidence=[f"{sid}: {', '.join(vs)}" for sid, vs in variant_sets.items()],
                    sources=list(per_source.keys()),
                    payload={"concept": concept, "variants": variant_sets, "source_titles": titles},
                )
            )
        findings.sort(key=lambda f: f.score, reverse=True)
        return findings

    def structural_invariants(self, sources: List[Source]) -> List[Finding]:
        """Busca patrones ASRO transversales: umbral, residuo, actualizacion, operador."""
        by_domain: Dict[str, Counter] = defaultdict(Counter)
        for s in sources:
            c_tokens = self.canonicalize_tokens(tokens(s.text))
            by_domain[s.domain].update(c_tokens)

        findings: List[Finding] = []
        domains = list(by_domain)
        if len(domains) < 2:
            return findings

        for concept in self.equivalences:
            hit_domains = [d for d in domains if by_domain[d].get(concept, 0) > 0]
            if len(hit_domains) >= 2:
                score = min(1.0, len(hit_domains) / max(2, len(domains)))
                findings.append(
                    Finding(
                        kind="invariant",
                        title=f"Invariante transversal detectado: {concept}",
                        score=score,
                        evidence=[f"{d}: {by_domain[d].get(concept, 0)} ocurrencias" for d in hit_domains],
                        sources=[],
                        payload={"concept": concept, "domains": hit_domains},
                    )
                )
        findings.sort(key=lambda f: f.score, reverse=True)
        return findings
