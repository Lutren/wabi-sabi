import math

import pytest

from obs_info_kernel.eml import (
    EMLDomainError,
    EXPERIMENTAL_OPERATOR_STATUS,
    eml,
    gap_eml,
    operator_contract,
    residue_eml,
)


def test_eml_returns_finite_for_normal_inputs():
    value = eml(0.25, 1.5)

    assert math.isfinite(value)
    assert value == pytest.approx(math.exp(0.25) - math.log(1.5))


def test_eml_rejects_y_less_or_equal_zero():
    with pytest.raises(EMLDomainError):
        eml(0.0, 0.0)

    with pytest.raises(EMLDomainError):
        eml(0.0, -1.0)


def test_eml_identity_log_exp():
    x = 3.25
    y = 1.75

    assert eml(math.log(x), math.exp(y)) == pytest.approx(x - y)


def test_eml_monotonicity_x_up_y_down():
    assert eml(0.4, 1.25) > eml(0.2, 1.25)
    assert eml(0.4, 1.25) > eml(0.4, 1.75)


def test_residue_and_gap_proxies_keep_domain_guarded():
    assert residue_eml(0.5, -10) == pytest.approx(eml(0.5, 1.0))
    assert gap_eml(0.5, 0.25) == pytest.approx(abs(eml(0.5, 1.25)))


def test_adversarial_inputs_do_not_promote_claims():
    contract = operator_contract()

    assert EXPERIMENTAL_OPERATOR_STATUS == "EXPERIMENTAL_OPERATOR_NOT_PROOF"
    assert contract["public_claim_allowed"] is False
    assert "not_physics_proof" in contract["claim_boundary"]
    with pytest.raises(EMLDomainError):
        eml(float("nan"), 1.0)
    with pytest.raises(OverflowError):
        eml(1000.0, 1.0)
