from __future__ import annotations

from collections import Counter, defaultdict
from itertools import combinations
from typing import Dict, List, Mapping, Tuple

from .calibration import CalibrationGapDetector
from .core import Finding, Source, safe_mean
from .text import concept_counter, cosine, jaccard_distance, surrounding_sentences, tfidf, tokens, weighted_jaccard_distance


class AntiInformationMiner:
    """Mina anti-informacion: informacion perdida por diferencia de calibracion.

    Anti-informacion no es "lo falso". Es el residuo entre marcos:
    - A y B hablan del mismo fenomeno con vocabularios distintos.
    - A presupone algo que B omite.
    - El nucleo comun existe, pero cada fuente pierde bordes distintos.
    """

    def __init__(self, equivalences: Mapping[str, List[str]] | None = None):
        self.calibration = CalibrationGapDetector(equivalences)

    def source_counters(self, sources: List[Source]) -> Dict[str, Counter]:
        out: Dict[str, Counter] = {}
        for s in sources:
            raw = concept_counter(s.text, max_ngram=2)
            # canonicaliza solo unigramas presentes en mapa; preserva n-gramas para evidencia.
            c = Counter()
            for term, count in raw.items():
                parts = term.split()
                if len(parts) == 1:
                    term = self.calibration.reverse.get(term, term)
                c[term] += count
            out[s.id] = c
        return out

    def pairwise(self, sources: List[Source]) -> List[Dict]:
        counters = self.source_counters(sources)
        vecs = tfidf([counters[s.id] for s in sources])
        by_id_vec = {s.id: v for s, v in zip(sources, vecs)}
        rows: List[Dict] = []
        for a, b in combinations(sources, 2):
            keys_a = set(counters[a.id].keys())
            keys_b = set(counters[b.id].keys())
            shared = keys_a & keys_b
            union = keys_a | keys_b
            set_dist = jaccard_distance(keys_a, keys_b)
            weight_dist = weighted_jaccard_distance(counters[a.id], counters[b.id])
            semantic_dist = 1.0 - cosine(by_id_vec[a.id], by_id_vec[b.id])
            divergence = max(0.0, min(1.0, 0.25 * set_dist + 0.35 * weight_dist + 0.40 * semantic_dist))
            coverage = len(shared) / max(1, min(len(keys_a), len(keys_b)))
            omission_pressure = len(keys_a ^ keys_b) / max(1, len(union))
            anti_score = max(0.0, min(1.0, (0.65 * divergence + 0.35 * omission_pressure) * coverage))
            rows.append(
                {
                    "a": a.id,
                    "b": b.id,
                    "a_title": a.title,
                    "b_title": b.title,
                    "a_domain": a.domain,
                    "b_domain": b.domain,
                    "jaccard_distance": round(set_dist, 4),
                    "weighted_distance": round(weight_dist, 4),
                    "tfidf_semantic_distance": round(semantic_dist, 4),
                    "divergence": round(divergence, 4),
                    "coverage": round(coverage, 4),
                    "omission_pressure": round(omission_pressure, 4),
                    "anti_information_score": round(anti_score, 4),
                }
            )
        rows.sort(key=lambda r: r["anti_information_score"], reverse=True)
        return rows

    def nucleus_and_omissions(self, sources: List[Source], min_coverage: float = 0.55) -> Dict:
        counters = self.source_counters(sources)
        n = max(1, len(sources))
        df: Counter = Counter()
        for c in counters.values():
            for term in c:
                df[term] += 1
        nucleus = sorted([term for term, freq in df.items() if freq / n >= min_coverage])
        # Mantener nucleo manejable: prioriza terminos conceptuales, no ruido.
        nucleus = [t for t in nucleus if len(t) > 3][:120]

        omissions = {}
        exclusives = {}
        for s in sources:
            own = set(counters[s.id])
            omissions[s.id] = sorted([t for t in nucleus if t not in own])[:80]
            exclusive = [t for t in own if df[t] == 1]
            exclusives[s.id] = sorted(exclusive, key=lambda t: counters[s.id][t], reverse=True)[:80]
        return {
            "nucleus": nucleus,
            "nucleus_size": len(nucleus),
            "omissions_by_source": omissions,
            "exclusive_by_source": exclusives,
        }

    def mine(self, sources: List[Source], min_coverage: float = 0.55) -> Dict:
        pairwise = self.pairwise(sources)
        nucleus = self.nucleus_and_omissions(sources, min_coverage=min_coverage)
        calibration_findings = self.calibration.detect(sources)
        invariants = self.calibration.structural_invariants(sources)
        divergence_mean = safe_mean([p["divergence"] for p in pairwise])
        anti_score_mean = safe_mean([p["anti_information_score"] for p in pairwise])

        findings: List[Finding] = []
        if pairwise:
            high = pairwise[0]
            findings.append(
                Finding(
                    kind="anti_information",
                    title="Mayor divergencia de calibracion entre fuentes",
                    score=high["anti_information_score"],
                    evidence=[
                        f"{high['a_title']} ↔ {high['b_title']}",
                        f"anti_score={high['anti_information_score']}",
                        f"divergencia={high['divergence']}, coverage={high['coverage']}",
                    ],
                    sources=[high["a"], high["b"]],
                    payload=high,
                )
            )

        for sid, omissions in nucleus["omissions_by_source"].items():
            if not omissions:
                continue
            src = next((s for s in sources if s.id == sid), None)
            score = min(1.0, len(omissions) / max(10, nucleus["nucleus_size"] or 1))
            findings.append(
                Finding(
                    kind="anti_information",
                    title=f"Omisiones frente al nucleo calibrado: {src.title if src else sid}",
                    score=score,
                    evidence=omissions[:12],
                    sources=[sid],
                    payload={"omissions": omissions},
                )
            )

        findings.extend(calibration_findings[:20])
        findings.extend(invariants[:20])
        findings.sort(key=lambda f: f.score, reverse=True)
        return {
            "summary": {
                "sources": len(sources),
                "pairwise_pairs": len(pairwise),
                "divergence_mean": round(divergence_mean, 4),
                "anti_score_mean": round(anti_score_mean, 4),
                "nucleus_size": nucleus["nucleus_size"],
                "calibration_gaps": len(calibration_findings),
                "invariants": len(invariants),
            },
            "pairwise": pairwise,
            "nucleus": nucleus,
            "findings": [f.to_dict() for f in findings],
        }

    def evidence_for_terms(self, sources: List[Source], terms: List[str], max_per_source: int = 3) -> Dict[str, List[str]]:
        out: Dict[str, List[str]] = {}
        for s in sources:
            ev = surrounding_sentences(s.text, terms, max_items=max_per_source)
            if ev:
                out[s.id] = ev
        return out
