import math

import pytest

from wabi_sabi.core.geodia_math_core import (
    REGIME_FUNCIONAL,
    REGIME_JAMMING,
    REGIME_JAMMING_TEMPRANO,
    REGIME_OPTIMO,
    REGIME_PRE_JAMMING,
    GeodiaCell,
    compute_eml,
    compute_epsilon,
    compute_phi_eff,
    compute_psi,
    compute_regime,
    observe_signal,
    update_cell,
)


def sample_cell(**overrides):
    data = {
        "x": 0,
        "y": 0,
        "resources": 0.6,
        "knowledge": 0.4,
        "memory": 0.3,
        "conflict": 0.2,
        "signal_noise": 0.25,
        "stability": 0.7,
        "agent_density": 0.5,
    }
    data.update(overrides)
    return GeodiaCell(**data)


def test_phi_eff_monotonic_and_jamming_boundary():
    assert compute_phi_eff(0) == 1
    assert compute_phi_eff(1.0) == 0
    assert compute_phi_eff(0.1) > compute_phi_eff(0.3) > compute_phi_eff(0.6)


def test_epsilon_increases_with_residue_and_observation_is_clamped():
    assert compute_epsilon(0.1) < compute_epsilon(0.5)
    observed = observe_signal(signal=2.0, noise_kernel=-1.0, epsilon=0.5)
    assert 0 <= observed <= 1


@pytest.mark.parametrize(
    ("R", "expected"),
    [
        (0.0, REGIME_OPTIMO),
        (0.3, REGIME_FUNCIONAL),
        (0.5, REGIME_PRE_JAMMING),
        (0.7, REGIME_JAMMING_TEMPRANO),
        (0.9, REGIME_JAMMING),
    ],
)
def test_regime_thresholds(R, expected):
    assert compute_regime(R) == expected


def test_compute_psi_empty_cells_is_optimal():
    psi = compute_psi([])
    assert psi.R == 0
    assert psi.phi_eff == 1
    assert psi.regime == REGIME_OPTIMO
    assert psi.sigma == (1.0, 1.0, 0.0, 0.0)


def test_compute_psi_outputs_bounded_metrics():
    psi = compute_psi([sample_cell(), sample_cell(x=1, conflict=0.8, signal_noise=0.6, stability=0.2)])
    for value in [psi.R, psi.phi_eff, psi.j_c, psi.epsilon, psi.fatigue, psi.I_obs, *psi.sigma]:
        assert 0 <= value <= 1


def test_update_cell_is_deterministic_with_supplied_random():
    values = iter([0.2, 0.4, 0.6])
    cell = update_cell(sample_cell(), lambda: next(values))
    for value in cell.to_dict().values():
        if isinstance(value, float):
            assert 0 <= value <= 1


def test_compute_eml_returns_finite_clamped_value():
    value = compute_eml(load=0.2, saturation=1.0, noise=0.3, intrinsic_clarity=2.0, scale=5.0)
    assert math.isfinite(value)
    assert 0 <= value <= 10


def test_invalid_domains_raise():
    with pytest.raises(ValueError):
        compute_phi_eff(0.2, Jc=0)
    with pytest.raises(ValueError):
        compute_regime(float("nan"))
