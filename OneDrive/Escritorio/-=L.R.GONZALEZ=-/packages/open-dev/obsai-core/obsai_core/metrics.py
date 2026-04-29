from __future__ import annotations

import math
from enum import Enum
from typing import Any, Sequence


class Regime(str, Enum):
    OPTIMO = "OPTIMO"
    FUNCIONAL = "FUNCIONAL"
    PRE_JAMMING = "PRE_JAMMING"
    JAMMING_TEMPRANO = "JAMMING_TEMPRANO"
    JAMMING = "JAMMING"


JAMMING_SIGNALS = {
    "circularity",
    "corrections",
    "goal_shift",
    "tokens_without_clarity",
    "redecision",
    "explicit_frustration",
    "latency",
    "unresolved_tasks",
    "contradiction",
    "overload",
}


def safe_float(value: Any, fallback: float = 0.0) -> float:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return fallback
    return number if math.isfinite(number) else fallback


def clamp01(value: Any) -> float:
    return max(0.0, min(1.0, safe_float(value)))


def estimate_residue_from_signals(signals: Sequence[str]) -> float:
    unique = {str(signal) for signal in signals}
    count = len(unique & JAMMING_SIGNALS)
    if count <= 0:
        return 0.10
    if count == 1:
        return 0.20
    if count == 2:
        return 0.32
    if count == 3:
        return 0.45
    if count == 4:
        return 0.58
    return 0.70


def estimate_regime(residue: Any) -> Regime:
    r_value = clamp01(residue)
    if r_value < 0.15:
        return Regime.OPTIMO
    if r_value < 0.30:
        return Regime.FUNCIONAL
    if r_value < 0.45:
        return Regime.PRE_JAMMING
    if r_value < 0.60:
        return Regime.JAMMING_TEMPRANO
    return Regime.JAMMING


def phi_eff_power(residue: Any, jamming_threshold: float = 1.0, phi0: float = 1.0, nu: float = 1.0) -> float:
    threshold = max(safe_float(jamming_threshold, 1.0), 1e-12)
    x_value = clamp01(safe_float(residue) / threshold)
    return clamp01(safe_float(phi0, 1.0) * ((1.0 - x_value) ** safe_float(nu, 1.0)))


def epsilon_distortion(
    residue: Any,
    jamming_threshold: float = 1.0,
    phi0: float = 1.0,
    nu: float = 1.0,
    kappa: float = 1.0,
) -> float:
    r_value = max(0.0, safe_float(residue))
    phi = phi_eff_power(r_value, jamming_threshold=jamming_threshold, phi0=phi0, nu=nu)
    return math.sqrt(max(0.0, safe_float(kappa, 1.0) * r_value * phi * phi))


def distortion_peak_residue(jamming_threshold: float = 1.0, nu: float = 1.0) -> float:
    return safe_float(jamming_threshold, 1.0) / (1.0 + 2.0 * safe_float(nu, 1.0))


def balance_lg(distinguishability: Any, restriction: Any, eps: float = 1e-12) -> float:
    d_value = max(0.0, safe_float(distinguishability))
    r_value = max(0.0, safe_float(restriction))
    return clamp01(d_value / (d_value + r_value + eps))


def dim_obs_score(dim_obs: Any, dim_scale: float = 6.0) -> float:
    dim = max(0.0, safe_float(dim_obs))
    return clamp01(1.0 - math.exp(-dim / max(dim_scale, 1e-12)))


def theta_score(
    *,
    distinguishability: Any,
    dim_obs: Any,
    complexity: Any,
    broadcast: Any,
    self_reference: Any,
    phi_eff_value: Any,
    balance: Any,
    balance_min: float = 0.12,
    balance_max: float = 0.90,
    weights: tuple[float, float, float, float, float, float] = (1, 1, 1, 1, 1, 1),
) -> float:
    if len(weights) != 6:
        raise ValueError("weights must contain six exponents")
    gate = 1.0 if balance_min < clamp01(balance) < balance_max else 0.0
    a, b, c, d, e, f = [safe_float(value, 1.0) for value in weights]
    return clamp01(
        (clamp01(distinguishability) ** a)
        * (dim_obs_score(dim_obs) ** b)
        * (clamp01(complexity) ** c)
        * (clamp01(broadcast) ** d)
        * (clamp01(self_reference) ** e)
        * (clamp01(phi_eff_value) ** f)
        * gate
    )
