from obs_safe_integration_kit import EvidenceStore, EstadoPSI, ObservationEnvelope, ActionGate, ActionProposal, GateStatus


def test_observation_and_store(tmp_path):
    store = EvidenceStore(tmp_path / "test.sqlite")
    psi = EstadoPSI(topic="test")
    obs = ObservationEnvelope(source="manual", text="This is useful evidence about a safe gate.").finalize()
    psi.absorb_observation(obs)
    oid = store.add_observation(obs)
    cid = store.add_claim(oid, "Safe gates should run before actions.", 0.8, evidence_ref=oid)
    status = store.latest_status()
    assert oid.startswith("obs_")
    assert cid.startswith("claim_")
    assert status["counts"]["observations"] == 1
    assert status["counts"]["claims"] == 1


def test_gate_blocks_secret():
    psi = EstadoPSI(topic="secret")
    gate = ActionGate()
    fixture_value = "github" + "_pat_" + "ABCDEF1234567890ABCDEF"
    prop = ActionProposal(tool="shell", args={"command": f"echo {fixture_value}"}, intent="print debug", shell=True)
    dec = gate.evaluate(prop, psi)
    assert dec.status == GateStatus.BLOCK


def test_gate_blocks_rm_rf():
    psi = EstadoPSI(topic="danger")
    gate = ActionGate()
    prop = ActionProposal(tool="shell", args={"command": "rm -rf ~/.ssh"}, intent="clean temp files", shell=True)
    dec = gate.evaluate(prop, psi)
    assert dec.status == GateStatus.BLOCK


def test_gate_dry_run_safe_command():
    psi = EstadoPSI(topic="safe")
    gate = ActionGate()
    prop = ActionProposal(tool="shell", args={"command": "pytest -q"}, intent="run local tests", shell=True)
    dec = gate.evaluate(prop, psi)
    assert dec.status in {GateStatus.DRY_RUN, GateStatus.HUMAN_REVIEW}
