from __future__ import annotations

import math
from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass(frozen=True)
class EMLResult:
    value: float | None
    domain_ok: bool
    warnings: list[str] = field(default_factory=list)
    epistemic_status: str = "RESEARCH_ONLY"

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def safe_eml(signal_log: float, residue_norm: float) -> EMLResult:
    """Research-only EML helper: exp(signal_log) - ln(1 + residue_norm).

    NOTA: Esta es la forma pre-canónica de EML. La forma canónica (07b §5) es sigmoidal:
      EML(s, c; alpha, beta, theta) = sigma(alpha * s - beta * log(1 + c) - theta)
    Ver Descubrimientos/eml_neural.py para la implementacion canonical.
    """
    warnings: list[str] = []
    if not math.isfinite(signal_log):
        warnings.append("signal_log_not_finite")
    if not math.isfinite(residue_norm):
        warnings.append("residue_norm_not_finite")
    if residue_norm < 0:
        warnings.append("residue_norm_must_be_gte_zero")
    if warnings:
        return EMLResult(value=None, domain_ok=False, warnings=warnings)
    try:
        value = math.exp(signal_log) - math.log1p(residue_norm)
    except (OverflowError, ValueError) as exc:
        return EMLResult(value=None, domain_ok=False, warnings=[f"domain_error:{exc.__class__.__name__}"])
    if not math.isfinite(value):
        return EMLResult(value=None, domain_ok=False, warnings=["eml_value_not_finite"])
    return EMLResult(value=value, domain_ok=True)


def window_load_eml(*, r_token: float, circularity: float, unresolved_tasks: float) -> EMLResult:
    warnings = _non_negative_inputs(
        {
            "r_token": r_token,
            "circularity": circularity,
            "unresolved_tasks": unresolved_tasks,
        }
    )
    if warnings:
        return EMLResult(value=None, domain_ok=False, warnings=warnings)
    value = math.log1p(r_token) + math.log1p(circularity) + math.log1p(unresolved_tasks)
    return EMLResult(value=value, domain_ok=math.isfinite(value), warnings=[] if math.isfinite(value) else ["value_not_finite"])


def jamming_margin_eml(*, residue_norm: float, phi_log: float) -> EMLResult:
    warnings = _non_negative_inputs({"residue_norm": residue_norm})
    if not math.isfinite(phi_log):
        warnings.append("phi_log_not_finite")
    if warnings:
        return EMLResult(value=None, domain_ok=False, warnings=warnings)
    try:
        value = math.log1p(residue_norm) - math.exp(phi_log)
    except OverflowError:
        return EMLResult(value=None, domain_ok=False, warnings=["phi_exp_overflow"])
    return EMLResult(value=value, domain_ok=math.isfinite(value), warnings=[] if math.isfinite(value) else ["value_not_finite"])


def _non_negative_inputs(values: dict[str, float]) -> list[str]:
    warnings: list[str] = []
    for name, value in values.items():
        if not math.isfinite(value):
            warnings.append(f"{name}_not_finite")
        elif value < 0:
            warnings.append(f"{name}_must_be_gte_zero")
    return warnings
