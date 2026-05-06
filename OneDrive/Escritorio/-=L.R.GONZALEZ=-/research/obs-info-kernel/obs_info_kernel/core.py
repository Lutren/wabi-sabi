from __future__ import annotations

import hashlib
import json
import math
import time
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional


@dataclass
class Source:
    """Unidad minima de evidencia para el kernel.

    `domain` no debe significar verdad; solo ventana de calibracion.
    Ejemplos: ciencia, mito, patente, arte, historia, canon, codigo.
    """

    id: str
    title: str
    text: str
    domain: str = "unknown"
    author: str = ""
    year: Optional[int] = None
    url: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)

    @staticmethod
    def make(title: str, text: str, domain: str = "unknown", **metadata: Any) -> "Source":
        raw = f"{domain}\n{title}\n{text[:2000]}".encode("utf-8", errors="ignore")
        sid = hashlib.sha256(raw).hexdigest()[:16]
        return Source(id=sid, title=title, text=text, domain=domain, metadata=metadata)

    @property
    def char_count(self) -> int:
        return len(self.text or "")

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class Finding:
    """Hallazgo trazable.

    kind: anti_information | dark_information | calibration_gap | invariant | warning
    score: 0..1, no es probabilidad; es prioridad operacional.
    """

    kind: str
    title: str
    score: float
    evidence: List[str] = field(default_factory=list)
    sources: List[str] = field(default_factory=list)
    payload: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d["score"] = round(float(self.score), 4)
        return d


@dataclass
class EstadoPSI:
    """Estado PSI operacional para una sesion de investigacion.

    No modela la mente como metafora; instrumenta carga, redundancia,
    divergencia, omisiones y cierre como variables de trabajo.
    """

    tema: str = ""
    J_c: float = 0.60
    started_at: float = field(default_factory=time.time)
    queries_total: int = 0
    queries_utiles: int = 0
    queries_fallidas: int = 0
    redundancia: float = 0.0
    divergencia_media: float = 0.0
    omisiones_detectadas: int = 0
    dark_candidates: int = 0
    decisiones: List[str] = field(default_factory=list)
    pendientes: List[str] = field(default_factory=list)
    señales_jamming: List[str] = field(default_factory=list)

    def registrar_query(self, useful: bool, redundancy: float = 0.0) -> None:
        self.queries_total += 1
        if useful:
            self.queries_utiles += 1
        else:
            self.queries_fallidas += 1
            self.señales_jamming.append("query_fallida_o_vacia")
        self.redundancia = _clamp((self.redundancia + redundancy) / 2.0 if self.queries_total > 1 else redundancy)

    def registrar_hallazgos(self, findings: Iterable[Finding]) -> None:
        for f in findings:
            if f.kind == "dark_information":
                self.dark_candidates += 1
            if f.kind in {"anti_information", "calibration_gap"}:
                self.omisiones_detectadas += len(f.payload.get("omissions", []))
            if f.score >= 0.85:
                self.señales_jamming.append(f"alta_prioridad:{f.kind}")

    @property
    def R(self) -> float:
        if self.queries_total <= 0:
            base = 0.0
        else:
            fallo = self.queries_fallidas / max(self.queries_total, 1)
            base = 0.40 * fallo + 0.30 * self.redundancia + 0.30 * self.divergencia_media
        carga_omisiones = min(self.omisiones_detectadas / 30.0, 0.25)
        return round(_clamp(base + carga_omisiones), 4)

    @property
    def Phi_eff(self) -> float:
        return round(max(0.0, 1.0 - self.R / max(self.J_c, 1e-9)), 4)

    @property
    def regimen(self) -> str:
        r = self.R
        if r < 0.15:
            return "OPTIMO"
        if r < 0.30:
            return "FUNCIONAL"
        if r < 0.45:
            return "PRE-JAMMING"
        if r < 0.60:
            return "JAMMING_TEMPRANO"
        return "JAMMING"

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d["R"] = self.R
        d["Phi_eff"] = self.Phi_eff
        d["regimen"] = self.regimen
        d["elapsed_sec"] = round(time.time() - self.started_at, 3)
        return d

    def fingerprint(self, patterns: Optional[List[str]] = None) -> Dict[str, Any]:
        return {
            "schema_version": "observacionismo.research_fingerprint.v0.1",
            "session_id": time.strftime("OBS-%Y%m%d-%H%M%S", time.gmtime()),
            "timestamp_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "tema": self.tema,
            "R_close": self.R,
            "Phi_eff_close": self.Phi_eff,
            "regimen_close": self.regimen,
            "J_c": self.J_c,
            "queries_total": self.queries_total,
            "queries_utiles": self.queries_utiles,
            "queries_fallidas": self.queries_fallidas,
            "omisiones_detectadas": self.omisiones_detectadas,
            "dark_candidates": self.dark_candidates,
            "señales_jamming": self.señales_jamming[-20:],
            "K_i_alpha_proxy": patterns or [],
            "segunda_perdida": "Los datos persisten. El operador no. Este fingerprint solo conserva proxy transferible.",
        }


def _clamp(x: float, lo: float = 0.0, hi: float = 1.0) -> float:
    return max(lo, min(hi, float(x)))


def save_json(path: str | Path, data: Any) -> None:
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def stable_hash(obj: Any) -> str:
    raw = json.dumps(obj, sort_keys=True, ensure_ascii=False, default=str).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()[:16]


def safe_mean(values: List[float], default: float = 0.0) -> float:
    return sum(values) / len(values) if values else default


def entropy(values: Iterable[str]) -> float:
    counts: Dict[str, int] = {}
    n = 0
    for v in values:
        counts[v] = counts.get(v, 0) + 1
        n += 1
    if n == 0:
        return 0.0
    return -sum((c / n) * math.log(c / n + 1e-12, 2) for c in counts.values())
