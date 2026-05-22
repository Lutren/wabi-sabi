import math

from wabi_sabi.core.eml import jamming_margin_eml, safe_eml, window_load_eml


def test_safe_eml_uses_shifted_residue_domain():
    result = safe_eml(signal_log=0.0, residue_norm=0.0)

    assert result.domain_ok is True
    assert result.epistemic_status == "RESEARCH_ONLY"
    assert result.value == 1.0


def test_safe_eml_rejects_negative_residue():
    result = safe_eml(signal_log=0.0, residue_norm=-0.1)

    assert result.domain_ok is False
    assert result.value is None
    assert "residue_norm_must_be_gte_zero" in result.warnings


def test_window_load_eml_is_finite_for_non_negative_inputs():
    result = window_load_eml(r_token=1.0, circularity=2.0, unresolved_tasks=3.0)

    assert result.domain_ok is True
    assert result.value == math.log1p(1.0) + math.log1p(2.0) + math.log1p(3.0)


def test_jamming_margin_eml_reports_auxiliary_margin():
    result = jamming_margin_eml(residue_norm=1.0, phi_log=0.0)

    assert result.domain_ok is True
    assert result.value == math.log1p(1.0) - 1.0
