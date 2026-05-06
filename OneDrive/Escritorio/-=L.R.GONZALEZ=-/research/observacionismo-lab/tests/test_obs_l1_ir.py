from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from obs_l1_ir import parse_l1, run_l1


def test_l1_compiles_five_verbs_to_l0_bytecode():
    script = """
    OBSERVAR bit 0
    ACTUAR xor 0 1
    DOCUMENTAR bit 0
    VERIFICAR output == [1]
    HANDOFF
    """

    program = parse_l1(script)

    assert [step.verb for step in program.steps] == [
        "OBSERVAR",
        "ACTUAR",
        "DOCUMENTAR",
        "VERIFICAR",
        "HANDOFF",
    ]
    assert program.assembly() == ["OBS 0 0", "XOR 0 1", "OUT 0 0", "HALT 0 0"]


def test_l1_run_returns_observation_envelope_and_passed_checks():
    script = """
    OBSERVAR bit 0
    ACTUAR xor 0 1
    DOCUMENTAR bit 0
    VERIFICAR output == [0]
    VERIFICAR halted == true
    VERIFICAR residue <= 0
    HANDOFF
    """

    result = run_l1(script, inputs=[1, 1])

    assert result["ok"] is True
    assert result["output"] == [0]
    assert result["observation_envelope"]["action_gate"] == "APPROVE"
    assert all(check["passed"] for check in result["checks"])


def test_l1_failed_verification_stays_review_not_success():
    script = """
    OBSERVAR bit 0
    ACTUAR xor 0 1
    DOCUMENTAR bit 0
    VERIFICAR output == [1]
    HANDOFF
    """

    result = run_l1(script, inputs=[1, 1])

    assert result["ok"] is False
    assert result["observation_envelope"]["action_gate"] == "REVIEW"
    assert result["checks"][0]["passed"] is False


def test_l1_rejects_steps_after_handoff():
    script = """
    HANDOFF
    DOCUMENTAR bit 0
    """

    try:
        parse_l1(script)
    except ValueError as exc:
        assert "after HANDOFF" in str(exc)
    else:
        raise AssertionError("expected parser rejection")
