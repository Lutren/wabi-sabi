from dataclasses import replace

import pytest

from wabi_sabi.core.eml import safe_eml
from wabi_sabi.core.gate import ActionGate, GateDecision
from wabi_sabi.core.geodia_math_core import compute_phi_eff
from wabi_sabi.core.observation import ObservationEnvelope
from wabi_sabi.core.patch_planner import build_file_patch_plan
from wabi_sabi.core.safe_executor import SafeExecutor, run_allowlisted_test_command


def test_formal_gate_decision_shape_is_covered_by_wabi_gate():
    decision = GateDecision("APPROVE", ["safe_local_deterministic_action"])

    assert decision.gate == "APPROVE"
    assert decision.reasons == ["safe_local_deterministic_action"]
    assert decision.allowed is True

    blocked = ActionGate().evaluate_text("publicar token en github release")

    assert blocked.gate == "BLOCK"
    assert blocked.allowed is False
    assert "external_publication_or_network_action" in blocked.reasons
    assert "secret_or_credential_boundary" in blocked.reasons


def test_formal_agent_output_shape_maps_to_observation_envelope():
    envelope = ObservationEnvelope(
        prompt="evaluacion observacionista formal",
        intent="contract_check",
        agent="wabi_contract_test",
        action_gate="REVIEW",
        certainty=["ActionGate exists as a local contract."],
        inference=["Formal AgentOutput maps to ObservationEnvelope fields."],
        unknown=["No Formal runtime import was performed."],
        artifacts=["docs/intake/FORMAL_WABI_CONTRACT_COMPARISON_2026-05-13.md"],
        evidence=["source=static_contract_comparison"],
    ).finalize()

    payload = envelope.to_dict()

    assert payload["envelope_version"] == "wabi-observation-v1"
    assert payload["action_gate"] == "REVIEW"
    assert payload["certainty"]
    assert payload["inference"]
    assert payload["unknown"]
    assert len(payload["fingerprint"]) == 64


def test_safe_executor_rejects_non_approved_formal_style_plan_before_write(tmp_path):
    plan = build_file_patch_plan(
        workspace=tmp_path,
        target="formal_contract_probe.py",
        content="VALUE = 1\n",
        summary="formal contract probe",
        suffix=".py",
    )
    review_plan = replace(plan, gate="REVIEW", reasons=["formal_import_not_allowed"])

    with pytest.raises(ValueError, match="patch_plan_not_approved:REVIEW"):
        SafeExecutor(workspace=tmp_path, runtime_root=tmp_path / "runtime").execute(review_plan)

    assert not (tmp_path / "formal_contract_probe.py").exists()


def test_pr11_fixture_cases_map_to_gate_ghost_and_handoff_contracts():
    gate = ActionGate()

    local_repair = gate.evaluate_text("repair local task and persist handoff")
    public_secret = gate.evaluate_text("publicar token en github release")

    assert local_repair.gate == "REVIEW"
    assert "local_write_or_repair_requires_scoped_artifact" in local_repair.reasons
    assert public_secret.gate == "BLOCK"
    assert "external_publication_or_network_action" in public_secret.reasons
    assert "secret_or_credential_boundary" in public_secret.reasons

    ghostgate_fixture = {
        "source": "Formal/PR11.txt",
        "ghost_check": "simulate_before_execute",
        "expected_gate": "REVIEW",
        "allowed_effects": ["local_artifact_only"],
        "blocked_effects": ["publish", "secret_print", "unbounded_process"],
    }

    assert ghostgate_fixture["expected_gate"] == local_repair.gate
    assert "publish" in ghostgate_fixture["blocked_effects"]

    handoff = ObservationEnvelope(
        prompt="PR11 ActionGate/GhostGate/Handoff fixture",
        intent="formal_pr11_fixture",
        agent="wabi_contract_test",
        action_gate=local_repair.gate,
        certainty=["PR11 fixture was mapped to local contracts."],
        inference=["GhostGate remains a simulation requirement, not runtime import."],
        unknown=["Formal PR11 runtime text was not executed."],
        artifacts=["docs/intake/FORMAL_CODE_RESCAN_CLAUDIO_WABI_2026-05-08.md"],
        evidence=["source=Formal/PR11.txt static fixture"],
    ).finalize()

    payload = handoff.to_dict()

    assert payload["action_gate"] == "REVIEW"
    assert payload["intent"] == "formal_pr11_fixture"
    assert payload["artifacts"]
    assert len(payload["fingerprint"]) == 64


def test_blocked_formal_execution_sources_stay_negative_cases(tmp_path):
    gate = ActionGate()

    uno = gate.evaluate_text("uno.py remove process and memory pressure shell control")
    deploy_overlord = gate.evaluate_text("deploy_overlord publish payload with token and API key")

    assert uno.gate == "BLOCK"
    assert "destructive_or_delete_request" in uno.reasons
    assert deploy_overlord.gate == "BLOCK"
    assert "external_publication_or_network_action" in deploy_overlord.reasons
    assert "secret_or_credential_boundary" in deploy_overlord.reasons

    with pytest.raises(ValueError, match="test_command_not_allowlisted"):
        run_allowlisted_test_command("python -m pytest -q; echo deploy", workspace=tmp_path)

    with pytest.raises(ValueError, match="target_path_blocked:runtime"):
        build_file_patch_plan(
            workspace=tmp_path,
            target="runtime/deploy_overlord_probe.py",
            content="VALUE = 1\n",
            summary="blocked formal negative case",
            suffix=".py",
        )


def test_phi_eff_and_eml_remain_bounded_research_helpers():
    assert compute_phi_eff(0.0) == 1.0
    assert 0.0 < compute_phi_eff(0.25, Jc=1.0) < 1.0
    assert compute_phi_eff(1.0, Jc=1.0) == 0.0

    with pytest.raises(ValueError, match="Jc_must_be_gt_zero"):
        compute_phi_eff(0.1, Jc=0.0)

    eml = safe_eml(signal_log=0.0, residue_norm=0.1)
    invalid = safe_eml(signal_log=0.0, residue_norm=-0.1)

    assert eml.epistemic_status == "RESEARCH_ONLY"
    assert eml.domain_ok is True
    assert invalid.domain_ok is False
    assert invalid.value is None
