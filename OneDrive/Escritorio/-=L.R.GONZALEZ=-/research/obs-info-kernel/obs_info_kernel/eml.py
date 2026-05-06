"""Experimental EML operator for local Observacionismo research.

EML is kept as a mathematical operator/proxy only:

    eml(x, y) = exp(x) - ln(y), y > 0

It is not evidence for physics, consciousness, history, social prediction or
any other strong claim.
"""

from __future__ import annotations

import math


EXPERIMENTAL_OPERATOR_STATUS = "EXPERIMENTAL_OPERATOR_NOT_PROOF"


class EMLDomainError(ValueError):
    """Raised when EML receives non-finite inputs or y <= 0."""


def _finite_number(value: float | int, name: str) -> float:
    number = float(value)
    if not math.isfinite(number):
        raise EMLDomainError(f"{name} must be finite")
    return number


def eml(x: float | int, y: float | int) -> float:
    """Return exp(x) - ln(y) with explicit domain and finitude checks."""

    x_value = _finite_number(x, "x")
    y_value = _finite_number(y, "y")
    if y_value <= 0.0:
        raise EMLDomainError("y must be > 0")

    result = math.exp(x_value) - math.log(y_value)
    if not math.isfinite(result):
        raise OverflowError("eml result is not finite")
    return result


def residue_eml(input_log: float | int, r_norm: float | int) -> float:
    """Operational residue proxy using EML(input_log, 1 + max(0, r_norm))."""

    residue = max(0.0, _finite_number(r_norm, "r_norm"))
    return eml(input_log, 1.0 + residue)


def gap_eml(signal_log: float | int, registry_norm: float | int) -> float:
    """Absolute EML gap proxy for local signal/registry comparison."""

    registry = max(0.0, _finite_number(registry_norm, "registry_norm"))
    return abs(eml(signal_log, 1.0 + registry))


def operator_contract() -> dict[str, object]:
    """Machine-readable claim boundary for EML integrations."""

    return {
        "schema": "obs_info_kernel.eml_operator_contract.v1",
        "status": EXPERIMENTAL_OPERATOR_STATUS,
        "formula": "eml(x, y) = exp(x) - ln(y)",
        "domain": {"x": "finite real", "y": "finite real > 0"},
        "public_claim_allowed": False,
        "claim_boundary": [
            "mathematical_proxy_only",
            "not_physics_proof",
            "not_consciousness_proof",
            "not_history_or_social_prediction",
        ],
        "falsifiers": [
            "x is not finite",
            "y is not finite",
            "y <= 0",
            "result overflows or is not finite",
            "monotonicity with x or y is broken",
            "operator is promoted as proof outside its mathematical domain",
        ],
    }
