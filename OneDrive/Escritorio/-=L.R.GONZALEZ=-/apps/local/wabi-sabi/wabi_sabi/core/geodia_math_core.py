from __future__ import annotations

import math
from dataclasses import asdict, dataclass
from typing import Callable


REGIME_OPTIMO = "OPTIMO"
REGIME_FUNCIONAL = "FUNCIONAL"
REGIME_PRE_JAMMING = "PRE_JAMMING"
REGIME_JAMMING_TEMPRANO = "JAMMING_TEMPRANO"
REGIME_JAMMING = "JAMMING"

SigmaVector = tuple[float, float, float, float]


@dataclass(frozen=True)
class OSITParams:
    nu: float = 2.5
    j_c: float = 1.0
    epsilon_0: float = 0.15
    mu: float = 0.8
    gamma: float = 0.28


@dataclass(frozen=True)
class GeodiaCell:
    x: int
    y: int
    resources: float
    knowledge: float
    memory: float
    conflict: float
    signal_noise: float
    stability: float
    agent_density: float

    def to_dict(self) -> dict[str, float | int]:
        return asdict(self)


@dataclass(frozen=True)
class PSIMetrics:
    R: float
    phi_eff: float
    j_c: float
    epsilon: float
    fatigue: float
    regime: str
    sigma: SigmaVector
    I_obs: float

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


def clamp(value: float, low: float = 0.0, high: float = 1.0) -> float:
    if not math.isfinite(value):
        raise ValueError("value_must_be_finite")
    if low > high:
        raise ValueError("low_must_be_lte_high")
    return min(max(value, low), high)


def compute_phi_eff(R: float, Jc: float = 1.0, nu: float = 2.5) -> float:
    """Synthetic OSIT helper: phi_eff collapses as residue approaches Jc."""
    _require_finite({"R": R, "Jc": Jc, "nu": nu})
    if Jc <= 0:
        raise ValueError("Jc_must_be_gt_zero")
    if R <= 0:
        return 1.0
    if R >= Jc:
        return 0.0
    return math.exp(-nu * R / (Jc - R))


def compute_epsilon(R: float, Jc: float = 1.0, *, params: OSITParams | None = None) -> float:
    params = params or OSITParams(j_c=Jc)
    _require_finite({"R": R, "Jc": Jc, "epsilon_0": params.epsilon_0, "mu": params.mu})
    if Jc <= 0:
        raise ValueError("Jc_must_be_gt_zero")
    return clamp(params.epsilon_0 * (clamp(R / Jc) ** params.mu))


def observe_signal(signal: float, noise_kernel: float, epsilon: float) -> float:
    eps = clamp(epsilon)
    return clamp(math.sqrt(1 - eps * eps) * clamp(signal) + eps * clamp(noise_kernel))


def compute_regime(R: float, Jc: float = 1.0) -> str:
    _require_finite({"R": R, "Jc": Jc})
    if Jc <= 0:
        raise ValueError("Jc_must_be_gt_zero")
    ratio = clamp(R / Jc)
    if ratio < 0.30:
        return REGIME_OPTIMO
    if ratio < 0.50:
        return REGIME_FUNCIONAL
    if ratio < 0.70:
        return REGIME_PRE_JAMMING
    if ratio < 0.90:
        return REGIME_JAMMING_TEMPRANO
    return REGIME_JAMMING


def local_residue(cell: GeodiaCell) -> float:
    return clamp(cell.conflict * 0.5 + cell.signal_noise * 0.3 + (1 - cell.stability) * 0.2)


def update_cell(cell: GeodiaCell, random: Callable[[], float], *, params: OSITParams | None = None) -> GeodiaCell:
    params = params or OSITParams()
    local_R = local_residue(cell)
    local_eps = compute_epsilon(local_R, params.j_c, params=params)
    phi_cell = compute_phi_eff(local_R, params.j_c, params.nu)
    obs_resources = observe_signal(cell.resources, random() * 0.25, local_eps)
    obs_knowledge = observe_signal(cell.knowledge, random() * 0.15, local_eps)
    return GeodiaCell(
        x=cell.x,
        y=cell.y,
        resources=clamp(obs_resources + 0.022 * phi_cell * (1 - obs_resources) - 0.012 * cell.conflict),
        knowledge=clamp(obs_knowledge + 0.012 * phi_cell * (1 - obs_knowledge)),
        memory=clamp(0.9 * cell.memory + 0.1 * obs_knowledge * phi_cell),
        conflict=clamp(cell.conflict + 0.03 * (cell.signal_noise - 0.3) * (1 + local_eps) - 0.02 * phi_cell),
        signal_noise=clamp(0.78 * cell.signal_noise + 0.22 * (random() * (1 - phi_cell * 0.4) + local_eps * 0.25)),
        stability=clamp(phi_cell * (1 - cell.conflict * 0.5) - cell.signal_noise * 0.18 + 0.48),
        agent_density=clamp(cell.agent_density + (0.01 if obs_resources > 0.5 else -0.01) * phi_cell),
    )


def compute_psi(cells: list[GeodiaCell], ticks: int = 0, prev_fatigue: float = 0.0, *, params: OSITParams | None = None) -> PSIMetrics:
    params = params or OSITParams()
    _require_finite({"prev_fatigue": prev_fatigue})
    if ticks < 0:
        raise ValueError("ticks_must_be_gte_zero")
    if not cells:
        sigma: SigmaVector = (1.0, 1.0, 0.0, 0.0)
        return PSIMetrics(R=0.0, phi_eff=1.0, j_c=1.0, epsilon=0.0, fatigue=0.0, regime=REGIME_OPTIMO, sigma=sigma, I_obs=1.0)

    residues = [local_residue(cell) for cell in cells]
    n = len(residues)
    R_mean = sum(residues) / n
    R_var = sum((residue - R_mean) ** 2 for residue in residues) / n
    coupling = params.gamma * R_mean * (1 - math.sqrt(min(R_var, 1.0)))
    R = clamp(R_mean + coupling)
    phi_eff = compute_phi_eff(R, params.j_c, params.nu)
    j_c = clamp(1 - R / params.j_c)
    epsilon = compute_epsilon(R, params.j_c, params=params)
    fatigue = clamp(0.95 * prev_fatigue + 0.05 * R)
    regime = compute_regime(R, params.j_c)
    sigma_0 = clamp(1 - fatigue)
    sigma_1 = clamp(phi_eff * j_c)
    sigma_2 = epsilon
    sigma_3 = clamp(sum(cell.conflict * (1 - cell.resources) for cell in cells) / n)
    sigma: SigmaVector = (sigma_0, sigma_1, sigma_2, sigma_3)
    I_obs = clamp(phi_eff * (1 - sigma_2) * j_c * (1 - sigma_3))
    return PSIMetrics(R=R, phi_eff=phi_eff, j_c=j_c, epsilon=epsilon, fatigue=fatigue, regime=regime, sigma=sigma, I_obs=I_obs)


def compute_eml(load: float, saturation: float, noise: float, intrinsic_clarity: float, scale: float) -> float:
    _require_finite(
        {
            "load": load,
            "saturation": saturation,
            "noise": noise,
            "intrinsic_clarity": intrinsic_clarity,
            "scale": scale,
        }
    )
    Jc = max(saturation, load + 0.001)
    phi = compute_phi_eff(load, Jc)
    bandwidth = clamp(1 - noise)
    info = math.log1p(bandwidth * intrinsic_clarity)
    return clamp(phi * info * scale, 0.0, 10.0)


def _require_finite(values: dict[str, float]) -> None:
    for name, value in values.items():
        if not math.isfinite(value):
            raise ValueError(f"{name}_must_be_finite")
