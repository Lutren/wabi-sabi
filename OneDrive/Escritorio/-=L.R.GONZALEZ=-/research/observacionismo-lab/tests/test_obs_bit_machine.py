from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from obs_bit_machine import ObsBitMachine, assemble, disassemble, infer_binary_program


def test_assemble_round_trip_and_xor_run():
    program = assemble(["OBS 0", "XOR 0 1", "OUT 0", "HALT"])

    assert disassemble(program) == ["OBS 0 0", "XOR 0 1", "OUT 0 0", "HALT 0 0"]

    machine = ObsBitMachine()
    assert machine.run(program, [1, 0]).output == [1]
    assert machine.run(program, [1, 1]).output == [0]


def test_inverse_observational_engineering_finds_xor():
    observations = {
        (0, 0): [0],
        (0, 1): [1],
        (1, 0): [1],
        (1, 1): [0],
    }

    result = infer_binary_program(observations, max_program_len=3)

    assert result["residue"] == 0.0
    assert "XOR 0 1" in result["assembly"]
    assert result["assembly"][-1] == "HALT 0 0"


def test_gate_like_residue_when_program_does_not_halt():
    program = assemble(["OBS 0", "OUT 0"])
    result = ObsBitMachine(max_steps=4).run(program, [1])

    assert result.halted is False
    assert result.residue > 0
    assert result.phi_eff < 1
