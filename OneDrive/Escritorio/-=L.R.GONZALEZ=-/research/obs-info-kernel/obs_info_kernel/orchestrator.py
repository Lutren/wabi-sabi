from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional

from .anti_information import AntiInformationMiner
from .continuity import ContinuityManager
from .core import EstadoPSI, Finding, Source, save_json
from .dark_information import DarkInformationMiner
from .hypothesis import HypothesisScorer
from .operator_profile import OperatorProfiler
from .text import normalize, top_terms
from .topology import OperatorTopology


class ObservacionismoResearchKernel:
    """Orquestador anti-informacion + informacion oscura.

    Modo correcto:
    - No afirma que un hallazgo sea verdadero.
    - Prioriza brechas, omisiones y candidatos verificables.
    - Exporta fingerprint para no perder calibracion.
    """

    def __init__(self, out_dir: str | Path = "obs_out"):
        self.out_dir = Path(out_dir)
        self.out_dir.mkdir(parents=True, exist_ok=True)
        self.anti = AntiInformationMiner()
        self.dark = DarkInformationMiner()
        self.operator_profiler = OperatorProfiler()
        self.operator_topology = OperatorTopology()
        self.hypothesis_scorer = HypothesisScorer()
        self.continuity = ContinuityManager(self.out_dir)

    def load_sources_from_dir(self, path: str | Path, recursive: bool = True) -> List[Source]:
        root = Path(path)
        patterns = ["**/*.md", "**/*.txt", "**/*.json"] if recursive else ["*.md", "*.txt", "*.json"]
        files: List[Path] = []
        for p in patterns:
            files.extend(root.glob(p))
        sources: List[Source] = []
        for file in sorted(set(files)):
            if file.name.startswith("."):
                continue
            try:
                text = file.read_text(encoding="utf-8", errors="ignore")
            except Exception:
                continue
            if not text.strip():
                continue
            domain = self._infer_domain(file.name, text)
            meta: Dict[str, Any] = {"path": str(file), "source_type": "local"}
            year = self._extract_year(text)
            src = Source.make(title=file.name, text=text, domain=domain, year=year, **meta)
            sources.append(src)
        return sources

    def analyze(self, query: str, sources: List[Source], min_coverage: float = 0.55) -> Dict[str, Any]:
        estado = EstadoPSI(tema=query)
        estado.registrar_query(useful=bool(sources), redundancy=0.0 if sources else 1.0)
        warnings: List[Dict[str, Any]] = []
        if not sources:
            warnings.append(
                {
                    "kind": "no_sources",
                    "title": "No sources available for analysis",
                    "severity": "BLOCK",
                    "action": "provide_corpus_or_fixture",
                    "detail": "The kernel produced continuity artifacts but did not infer claims without sources.",
                }
            )

        anti_report = self.anti.mine(sources, min_coverage=min_coverage) if sources else {}
        dark_report = self.dark.mine(query, sources) if sources else {}
        profiles = self.operator_profiler.build_many(sources) if sources else []
        atlas = self.operator_profiler.atlas_summary(profiles)
        topology = self.operator_topology.build(profiles) if profiles else self.operator_topology.build([])

        all_findings = []
        for block in (anti_report.get("findings", []), dark_report.get("findings", [])):
            all_findings.extend(block)
        for warning in warnings:
            all_findings.append(
                Finding(
                    kind="warning",
                    title=warning["title"],
                    score=1.0,
                    evidence=[warning["detail"]],
                    payload=warning,
                ).to_dict()
            )
        all_findings.sort(key=lambda f: f.get("score", 0.0), reverse=True)
        hypotheses = self.hypothesis_scorer.from_findings(all_findings, profiles)

        estado.divergencia_media = anti_report.get("summary", {}).get("divergence_mean", 0.0)
        # convertir dicts a Findings solo para registrar tipo/score
        estado.registrar_hallazgos([Finding(kind=f.get("kind", "finding"), title=f.get("title", ""), score=f.get("score", 0.0), payload=f.get("payload", {})) for f in all_findings])

        patterns = [f"{f.get('kind')}: {f.get('title')}" for f in all_findings[:10]]
        fp_path = self.continuity.write_fingerprint(estado, all_findings)
        brief_path = self.continuity.write_next_session_brief(estado, all_findings)

        report = {
            "run_status": {
                "status": "OK" if sources else "NO_SOURCES",
                "source_count": len(sources),
                "warnings": warnings,
                "claim_policy": "no_claims_without_sources",
            },
            "query": query,
            "estado_psi": estado.to_dict(),
            "sources": [s.to_dict() for s in sources],
            "operator_profiles": [profile.to_dict() for profile in profiles],
            "operator_atlas": atlas,
            "operator_topology": topology,
            "anti_information": anti_report,
            "dark_information": dark_report,
            "hypotheses": [hypothesis.to_dict() for hypothesis in hypotheses],
            "top_findings": all_findings[:50],
            "artifacts": {"fingerprint": str(fp_path), "next_session_brief": str(brief_path)},
        }
        json_path = self.out_dir / "observacionismo_research_report.json"
        md_path = self.out_dir / "observacionismo_research_report.md"
        save_json(json_path, report)
        md_path.write_text(self.to_markdown(report), encoding="utf-8")
        report["artifacts"]["json_report"] = str(json_path)
        report["artifacts"]["markdown_report"] = str(md_path)
        return report

    def to_markdown(self, report: Dict[str, Any]) -> str:
        estado = report.get("estado_psi", {})
        lines: List[str] = []
        lines.append("# Observacionismo Research Report")
        lines.append("")
        lines.append(f"**Query:** {report.get('query','')}")
        lines.append(f"**R:** {estado.get('R')} | **Phi_eff:** {estado.get('Phi_eff')} | **Regimen:** {estado.get('regimen')}")
        lines.append("")
        lines.append("## Lectura operacional")
        lines.append("Anti-información = divergencias, omisiones y brechas de calibración entre fuentes.")
        lines.append("Información oscura = candidatos con baja visibilidad, rareza conceptual y relevancia suficiente.")
        lines.append("Atlas de operadores = perfiles K_source: conceptos, omisiones, evidencia, R_source y Phi_source por fuente.")
        lines.append("El reporte prioriza hipótesis verificables; no convierte rareza en verdad.")
        lines.append("")

        run_status = report.get("run_status", {})
        if run_status:
            lines.append("## Estado de corrida")
            lines.append(f"Status: `{run_status.get('status')}` | sources={run_status.get('source_count')}")
            for warning in run_status.get("warnings", []):
                lines.append(f"- **{warning.get('severity')}** {warning.get('title')}: {warning.get('detail')}")
            lines.append("")

        atlas = report.get("operator_atlas", {})
        if atlas:
            lines.append("## Atlas de operadores")
            lines.append(f"Resumen: `{json.dumps(atlas, ensure_ascii=False)}`")
            lines.append("")

        topology = report.get("operator_topology", {})
        if topology:
            lines.append("## Topologia operacional C_ij")
            lines.append(f"Status: `{topology.get('status')}`")
            lines.append(str(topology.get("claim_boundary", "")))
            for edge in topology.get("edges", [])[:10]:
                lines.append(
                    f"- {edge.get('source_title')} ↔ {edge.get('target_title')}: "
                    f"C_ij={edge.get('c_ij')} shared={', '.join(edge.get('shared_operators', [])[:6])}"
                )
            lines.append("")

        hypotheses = report.get("hypotheses", [])[:10]
        if hypotheses:
            lines.append("## Hipótesis priorizadas")
            for h in hypotheses:
                lines.append(
                    f"- **{h.get('id')}** priority={h.get('priority')} delta_R={h.get('delta_r')} "
                    f"testability={h.get('testability')} status={h.get('status')}: {h.get('text')}"
                )
                lines.append(f"  - falsador: {h.get('falsifier')}")
            lines.append("")

        lines.append("## Top findings")
        for i, f in enumerate(report.get("top_findings", [])[:20], 1):
            lines.append(f"{i}. **[{f.get('kind')}] {f.get('title')}** — score={float(f.get('score', 0)):.3f}")
            ev = f.get("evidence") or []
            for e in ev[:3]:
                lines.append(f"   - {str(e)[:500]}")
        lines.append("")

        anti = report.get("anti_information", {})
        if anti:
            lines.append("## Anti-información")
            lines.append(f"Resumen: `{json.dumps(anti.get('summary', {}), ensure_ascii=False)}`")
            pairwise = anti.get("pairwise", [])[:10]
            if pairwise:
                lines.append("")
                lines.append("### Divergencias principales")
                for p in pairwise:
                    lines.append(
                        f"- {p.get('a_title')} ↔ {p.get('b_title')}: "
                        f"anti_score={p.get('anti_information_score')} divergence={p.get('divergence')} coverage={p.get('coverage')}"
                    )
            lines.append("")

        dark = report.get("dark_information", {})
        if dark:
            lines.append("## Información oscura")
            for r in dark.get("ranked_sources", [])[:15]:
                lines.append(f"- **{r.get('title')}** [{r.get('domain')}] dark={r.get('darkness_score')} relevance={r.get('relevance')} rare={', '.join(r.get('rare_terms', [])[:5])}")
            lines.append("")

        lines.append("## Artefactos de continuidad")
        for k, v in report.get("artifacts", {}).items():
            lines.append(f"- {k}: `{v}`")
        lines.append("")
        return "\n".join(lines)

    def _infer_domain(self, filename: str, text: str) -> str:
        fn = normalize(filename)
        tx = normalize(text[:4000])
        # Primero filename: casi todos los docs canon contienen la palabra Observacionismo,
        # asi que usar el texto primero colapsa dominios distintos.
        if "brain" in fn:
            return "brain_os"
        if "eml" in fn:
            return "eml"
        if "psi_teoria" in fn or "teoria_formal" in fn:
            return "psi_formal"
        if "psi_ai" in fn or "framework" in fn:
            return "psi_ia"
        if "segunda" in fn or "perdida" in fn:
            return "continuidad"
        if "agent" in fn or "spec" in fn:
            return "agente"
        if "posicionamiento" in fn or "observador" in fn:
            return "narrativa"
        if "observacionismo" in fn or "core" in fn:
            return "core"
        if "codigo" in fn or "code" in fn or "python" in tx[:1000]:
            return "codigo"
        if "antigravity" in fn:
            return "runtime"
        if "observacionismo" in tx:
            return "canon_observacionismo"
        return "local"

    def _extract_year(self, text: str) -> Optional[int]:
        m = re.search(r"\b(19\d{2}|20\d{2})\b", text[:5000])
        if m:
            try:
                return int(m.group(1))
            except Exception:
                return None
        return None
