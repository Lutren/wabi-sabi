from obs_info_kernel import ClaimStatus, EORCalculator, EpistemicGuard, EquivalenceTester


def test_eor_zero_when_representation_identifies_phenomenon():
    joint = {("a", "x_a"): 3, ("b", "x_b"): 3}
    assert EORCalculator.normalized_conditional_entropy(joint) == 0.0


def test_eor_increases_for_ambiguous_representation():
    joint = {("a", "x"): 3, ("b", "x"): 3, ("b", "y"): 3}
    assert EORCalculator.normalized_conditional_entropy(joint) > 0.0


def test_operational_residue_and_phi_eff_are_bounded():
    r = EORCalculator.operational_residue(
        failures=3,
        redundancy=0.5,
        contradictions=2,
        open_pending=1,
        blocked_actions=1,
        total_events=4,
    )
    assert 0.0 <= r <= 1.0
    assert EORCalculator.phi_eff(0.0) == 1.0
    assert EORCalculator.phi_eff(9.0) == 0.0


def test_guard_blocks_control_reality_overclaim():
    claim = EpistemicGuard().classify("Controlar R es controlar la realidad observable.", "fisica")
    assert claim.status == ClaimStatus.BLOCKED
    assert claim.risk >= 0.9


def test_guard_marks_physical_identity_as_hypothesis():
    guard = EpistemicGuard()
    claim = guard.classify("La mecanica cuantica es jamming.", "fisica")
    assert claim.status == ClaimStatus.PHYSICAL_HYPOTHESIS
    assert guard.safe_rewrite(claim).startswith("Hipotesis de investigacion:")


def test_guard_accepts_proxy_as_operational():
    claim = EpistemicGuard().classify("R_operativo es un proxy de runtime.", "agentes")
    assert claim.status == ClaimStatus.OPERATIONAL


def test_equivalence_tester_requires_all_filters():
    tester = EquivalenceTester()
    assert tester.evaluate(
        same_variables=True,
        same_causal_direction=True,
        same_threshold_type=True,
        same_perturbation_response=True,
        comparable_prediction_or_intervention=True,
    ).verdict == "equivalence"
    assert tester.evaluate(
        same_variables=True,
        same_causal_direction=True,
        same_threshold_type=True,
        same_perturbation_response=True,
        comparable_prediction_or_intervention=False,
    ).verdict == "partial_translation"
