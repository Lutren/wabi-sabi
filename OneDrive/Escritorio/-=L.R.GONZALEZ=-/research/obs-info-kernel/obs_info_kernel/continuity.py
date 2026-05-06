from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List

from .core import EstadoPSI, Finding, save_json


class ContinuityManager:
    """Mitiga segunda perdida con artefactos transferibles.

    No pretende preservar K_i^alpha completo; genera un proxy auditable.
    """

    def __init__(self, out_dir: str | Path = "obs_out"):
        self.out_dir = Path(out_dir)
        self.out_dir.mkdir(parents=True, exist_ok=True)

    def patterns_from_findings(self, findings: List[Finding | Dict[str, Any]], max_items: int = 12) -> List[str]:
        pats: List[str] = []
        for f in findings[:max_items]:
            if isinstance(f, Finding):
                kind, title, score = f.kind, f.title, f.score
            else:
                kind, title, score = f.get("kind", "finding"), f.get("title", ""), f.get("score", 0)
            pats.append(f"[{kind}] {title} (score={float(score):.3f})")
        return pats

    def write_fingerprint(self, estado: EstadoPSI, findings: List[Finding | Dict[str, Any]]) -> Path:
        fp = estado.fingerprint(patterns=self.patterns_from_findings(findings))
        path = self.out_dir / "SESSION_FINGERPRINT.json"
        save_json(path, fp)
        return path

    def write_next_session_brief(self, estado: EstadoPSI, findings: List[Finding | Dict[str, Any]]) -> Path:
        pats = self.patterns_from_findings(findings, max_items=8)
        brief = self.next_session_brief(estado, pats)
        path = self.out_dir / "NEXT_SESSION_BRIEF.md"
        path.write_text(brief, encoding="utf-8")
        return path

    def next_session_brief(self, estado: EstadoPSI, patterns: List[str]) -> str:
        decisiones = estado.decisiones or ["Plantear anti-informacion como divergencia/omision entre marcos, no como contenido falso.",
                                           "Plantear informacion oscura como baja visibilidad + rareza + relevancia, no como verdad marginal garantizada."]
        pendientes = estado.pendientes or ["Validar hallazgos externos con fuentes primarias antes de afirmar novedad.",
                                           "Separar modulo experimental de canon operativo."]
        return f"""# NEXT_SESSION_BRIEF — Anti-información / Información Oscura

Tema: {estado.tema}
R_cierre: {estado.R:.3f} ({estado.regimen})
Phi_eff: {estado.Phi_eff:.3f}

## Decisiones tomadas
{chr(10).join(f'- {d}' for d in decisiones)}

## Pendientes reales con evidencia
{chr(10).join(f'- {p}' for p in pendientes)}

## K_i^α proxy / patrones externalizados
{chr(10).join(f'- {p}' for p in patterns) if patterns else '- Sin patrones suficientes.'}

## Segunda pérdida
Los datos persisten. El operador no. Este brief no preserva la ventana; solo reduce la pérdida al reiniciar.

## Próxima acción verificable
Correr el kernel sobre un corpus de 20-50 fuentes por dominio y exportar hallazgos con evidencia local + verificación externa.
""".strip()
