from __future__ import annotations

import math
import time
from collections import Counter
from typing import Dict, Iterable, List, Mapping, Optional

from .calibration import CalibrationGapDetector
from .core import Finding, Source
from .text import concept_counter, cosine, rarity_scores, surrounding_sentences, tfidf, tokens


class DarkInformationMiner:
    """Mina informacion oscura: conocimiento relegado, invisible o subintegrado.

    Separa tres cosas:
    1. baja visibilidad (pocas citas, archivo local marginal, fuente abandonada),
    2. alta rareza conceptual dentro del corpus,
    3. relevancia suficiente para el tema actual.

    Si no hay metadatos externos, usa proxies internos; por eso el score no debe
    venderse como verdad bibliometrica.
    """

    def __init__(self, equivalences: Mapping[str, List[str]] | None = None):
        self.calibration = CalibrationGapDetector(equivalences)

    def mine(self, query: str, sources: List[Source], top_k: int = 25) -> Dict:
        counters = [concept_counter(s.text, max_ngram=2) for s in sources]
        vectors = tfidf(counters)
        query_counter = concept_counter(query, max_ngram=2)
        query_vec = tfidf([query_counter] + counters)[0] if sources else dict(query_counter)
        rarity = rarity_scores(counters)

        findings: List[Finding] = []
        rows: List[Dict] = []
        for idx, s in enumerate(sources):
            c = counters[idx]
            v = vectors[idx] if idx < len(vectors) else {}
            relevance = cosine(query_vec, v) if query.strip() else 0.5
            if query.strip() and relevance == 0:
                # Fallback: overlap simple para queries cortas.
                qt = set(tokens(query))
                st = set(tokens(s.text))
                relevance = len(qt & st) / max(1, len(qt))

            rare_terms = sorted(c.keys(), key=lambda t: rarity.get(t, 0.0) * c[t], reverse=True)[:30]
            novelty = sum(rarity.get(t, 0.0) for t in list(c.keys())[:200]) / max(1, min(200, len(c)))
            visibility = self._visibility_score(s)
            orphanhood = self._orphanhood_score(s, c, rarity)
            age_gap = self._age_gap_score(s)
            testability = self._testability_score(s)
            darkness = self._combine(relevance, novelty, visibility, orphanhood, age_gap)
            dark_state = self._dark_state(s, darkness, testability)

            row = {
                "source_id": s.id,
                "title": s.title,
                "domain": s.domain,
                "relevance": round(relevance, 4),
                "novelty": round(novelty, 4),
                "low_visibility": round(visibility, 4),
                "orphanhood": round(orphanhood, 4),
                "age_gap": round(age_gap, 4),
                "testability": round(testability, 4),
                "dark_state": dark_state,
                "darkness_score": round(darkness, 4),
                "rare_terms": rare_terms[:15],
            }
            rows.append(row)
            if darkness >= 0.35:
                evidence = surrounding_sentences(s.text, rare_terms[:5], max_items=3) or [", ".join(rare_terms[:10])]
                findings.append(
                    Finding(
                        kind="dark_information",
                        title=f"Candidato a informacion oscura: {s.title}",
                        score=darkness,
                        evidence=evidence,
                        sources=[s.id],
                        payload=row,
                    )
                )
        rows.sort(key=lambda r: r["darkness_score"], reverse=True)
        findings.sort(key=lambda f: f.score, reverse=True)
        return {
            "summary": {"sources": len(sources), "dark_candidates": len(findings), "query": query},
            "ranked_sources": rows[:top_k],
            "findings": [f.to_dict() for f in findings[:top_k]],
            "absence_patterns": self.absence_patterns(sources),
        }

    def absence_patterns(self, sources: List[Source]) -> List[Dict]:
        """Busca operadores esperables del canon que faltan por dominio."""
        by_domain: Dict[str, Counter] = {}
        for s in sources:
            by_domain.setdefault(s.domain, Counter()).update(self.calibration.canonicalize_tokens(tokens(s.text)))
        all_concepts = set(self.calibration.equivalences)
        out: List[Dict] = []
        for domain, counter in by_domain.items():
            present = {c for c in all_concepts if counter.get(c, 0) > 0}
            missing = sorted(all_concepts - present)
            if missing:
                out.append({"domain": domain, "missing_operators": missing, "present_operators": sorted(present)})
        return out

    def _visibility_score(self, s: Source) -> float:
        """1 = baja visibilidad. Usa citas si existen; si no, metadata local."""
        meta = s.metadata or {}
        citations = meta.get("citations", meta.get("citas", meta.get("cited_by_count")))
        if citations is not None:
            try:
                c = max(0.0, float(citations))
                return 1.0 / (1.0 + math.log1p(c))
            except Exception:
                pass
        source_type = str(meta.get("source_type", meta.get("tipo", ""))).lower()
        if any(x in source_type for x in ["abandoned", "archive", "tesis", "patente", "nota", "local"]):
            return 0.80
        if s.url:
            return 0.45
        return 0.60

    def _orphanhood_score(self, s: Source, c: Counter, rarity: Dict[str, float]) -> float:
        if not c:
            return 0.0
        weighted = [rarity.get(t, 0.0) * min(1.0, c[t] / 3.0) for t in c]
        return max(0.0, min(1.0, sum(weighted) / max(1, len(weighted))))

    def _age_gap_score(self, s: Source) -> float:
        # Lo viejo o sin fecha puede ser relegado, pero no siempre. Peso moderado.
        if not s.year:
            return 0.35
        current_year = time.gmtime().tm_year
        age = max(0, current_year - int(s.year))
        return max(0.0, min(1.0, age / 60.0))

    def _testability_score(self, s: Source) -> float:
        meta = s.metadata or {}
        explicit = meta.get("testability", meta.get("testabilidad"))
        if explicit is not None:
            try:
                return max(0.0, min(1.0, float(explicit)))
            except Exception:
                pass

        text = " ".join([s.title or "", s.text or ""]).lower()
        markers = [
            "prediction",
            "prediccion",
            "predicción",
            "test",
            "prueba",
            "experiment",
            "experimento",
            "benchmark",
            "dataset",
            "replica",
            "replicacion",
            "replicación",
            "falsable",
        ]
        hits = sum(1 for marker in markers if marker in text)
        return max(0.10, min(1.0, hits / 5.0))

    def _dark_state(self, s: Source, darkness: float, testability: float) -> str:
        meta = s.metadata or {}
        explicit = meta.get("dark_state")
        if explicit in {"dark_candidate", "dark_validated", "dark_rejected"}:
            return str(explicit)
        if bool(meta.get("validated", False)):
            return "dark_validated"
        if bool(meta.get("rejected", False)) or bool(meta.get("noise", False)):
            return "dark_rejected"
        if darkness >= 0.60 and testability >= 0.50 and bool(meta.get("independent_check", False)):
            return "dark_validated"
        if darkness >= 0.35 and testability >= 0.50:
            return "dark_testable"
        return "dark_candidate"

    def _combine(self, relevance: float, novelty: float, visibility: float, orphanhood: float, age_gap: float) -> float:
        # La relevancia actua como compuerta: no basta ser raro.
        gate = 0.25 + 0.75 * max(0.0, min(1.0, relevance))
        raw = 0.30 * novelty + 0.30 * visibility + 0.25 * orphanhood + 0.15 * age_gap
        return max(0.0, min(1.0, gate * raw))
