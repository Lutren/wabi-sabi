#!/usr/bin/env python3
"""
ObsBitMachine: minimal bit-level VM for observational programming experiments.

This is a local research harness, not a general-purpose language. The point is
to test how far an Observacionismo-style control loop can be reduced while
keeping observation, action gating, traceability and inverse fitting explicit.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from itertools import product
from typing import Dict, Iterable, List, Mapping, Sequence, Tuple


OPCODES = {
    "NOP": 0,
    "OBS": 1,
    "ZERO": 2,
    "ONE": 3,
    "XOR": 4,
    "AND": 5,
    "OUT": 6,
    "HALT": 7,
}
NAMES = {value: key for key, value in OPCODES.items()}


@dataclass(frozen=True)
class Instruction:
    op: int
    x: int = 0
    y: int = 0

    def encode(self) -> int:
        """Pack one instruction as 3 opcode bits, 3 x bits and 2 y bits."""
        if not 0 <= self.op <= 7:
            raise ValueError(f"opcode out of range: {self.op}")
        if not 0 <= self.x <= 7:
            raise ValueError(f"x out of range: {self.x}")
        if not 0 <= self.y <= 3:
            raise ValueError(f"y out of range: {self.y}")
        return (self.op << 5) | (self.x << 2) | self.y

    @classmethod
    def decode(cls, byte: int) -> "Instruction":
        if not 0 <= byte <= 255:
            raise ValueError(f"byte out of range: {byte}")
        return cls(op=(byte >> 5) & 0b111, x=(byte >> 2) & 0b111, y=byte & 0b11)

    def text(self) -> str:
        return f"{NAMES.get(self.op, 'BAD')} {self.x} {self.y}".rstrip()


@dataclass
class RunResult:
    memory: List[int]
    output: List[int]
    trace: List[Dict[str, object]]
    halted: bool
    residue: float
    phi_eff: float


@dataclass
class ObsBitMachine:
    memory_size: int = 8
    max_steps: int = 64
    trace_limit: int = 256
    memory: List[int] = field(default_factory=list)

    def __post_init__(self) -> None:
        if not self.memory:
            self.memory = [0] * self.memory_size
        if len(self.memory) != self.memory_size:
            raise ValueError("memory length must match memory_size")
        self.memory = [1 if bit else 0 for bit in self.memory]

    def run(self, program: Sequence[int], inputs: Sequence[int] = ()) -> RunResult:
        mem = [0] * self.memory_size
        for idx, bit in enumerate(inputs[: self.memory_size]):
            mem[idx] = 1 if bit else 0

        pc = 0
        output: List[int] = []
        trace: List[Dict[str, object]] = []
        residue = 0.0
        halted = False

        for step in range(self.max_steps):
            if pc < 0 or pc >= len(program):
                residue += 1.0
                break
            ins = Instruction.decode(program[pc])
            before = list(mem)
            event: Dict[str, object] = {
                "step": step,
                "pc": pc,
                "instruction": ins.text(),
                "before": before,
            }

            if ins.x >= self.memory_size or ins.y >= self.memory_size:
                residue += 1.0
                event["error"] = "address_out_of_range"
                trace.append(event)
                break

            if ins.op == OPCODES["NOP"]:
                pass
            elif ins.op == OPCODES["OBS"]:
                event["observed_bit"] = mem[ins.x]
            elif ins.op == OPCODES["ZERO"]:
                mem[ins.x] = 0
            elif ins.op == OPCODES["ONE"]:
                mem[ins.x] = 1
            elif ins.op == OPCODES["XOR"]:
                mem[ins.x] ^= mem[ins.y]
            elif ins.op == OPCODES["AND"]:
                mem[ins.x] &= mem[ins.y]
            elif ins.op == OPCODES["OUT"]:
                output.append(mem[ins.x])
            elif ins.op == OPCODES["HALT"]:
                halted = True
                event["after"] = list(mem)
                trace.append(event)
                break
            else:
                residue += 1.0
                event["error"] = "unknown_opcode"
                trace.append(event)
                break

            event["after"] = list(mem)
            if len(trace) < self.trace_limit:
                trace.append(event)
            pc += 1
        else:
            residue += 1.0

        if not halted:
            residue += 0.25

        steps = max(1, len(trace))
        residue_norm = min(1.0, residue / max(1.0, steps))
        phi_eff = (len(output) / steps) * (1.0 - residue_norm)
        return RunResult(mem, output, trace, halted, residue, phi_eff)


def assemble(lines: Iterable[str]) -> List[int]:
    program: List[int] = []
    for raw in lines:
        line = raw.split("#", 1)[0].strip()
        if not line:
            continue
        parts = line.replace(",", " ").split()
        op_name = parts[0].upper()
        if op_name not in OPCODES:
            raise ValueError(f"unknown op: {op_name}")
        x = int(parts[1]) if len(parts) > 1 else 0
        y = int(parts[2]) if len(parts) > 2 else 0
        program.append(Instruction(OPCODES[op_name], x, y).encode())
    return program


def disassemble(program: Sequence[int]) -> List[str]:
    return [Instruction.decode(byte).text() for byte in program]


def hamming_residue(expected: Sequence[int], actual: Sequence[int]) -> float:
    max_len = max(len(expected), len(actual))
    residue = abs(len(expected) - len(actual))
    residue += sum(1 for a, b in zip(expected, actual) if int(a) != int(b))
    return residue / max(1, max_len)


def infer_binary_program(
    observations: Mapping[Tuple[int, int], Sequence[int]],
    *,
    max_program_len: int = 4,
) -> Dict[str, object]:
    """Infer a tiny program from IO observations by minimizing residue.

    The search is deliberately small and transparent. It is inverse
    observational engineering: observe IO, enumerate candidate mechanisms,
    measure residue, then choose the simplest zero-residue candidate.
    """

    atoms = [
        Instruction(OPCODES["OBS"], 0, 0).encode(),
        Instruction(OPCODES["OBS"], 1, 0).encode(),
        Instruction(OPCODES["ZERO"], 0, 0).encode(),
        Instruction(OPCODES["ONE"], 0, 0).encode(),
        Instruction(OPCODES["XOR"], 0, 1).encode(),
        Instruction(OPCODES["AND"], 0, 1).encode(),
        Instruction(OPCODES["OUT"], 0, 0).encode(),
        Instruction(OPCODES["OUT"], 1, 0).encode(),
    ]
    halt = Instruction(OPCODES["HALT"], 0, 0).encode()
    machine = ObsBitMachine(memory_size=8, max_steps=16)
    best: Dict[str, object] | None = None

    for length in range(1, max_program_len + 1):
        for prefix in product(atoms, repeat=length):
            program = list(prefix) + [halt]
            total_residue = 0.0
            outputs: Dict[str, List[int]] = {}
            halted_all = True
            for inputs, expected in observations.items():
                result = machine.run(program, inputs)
                halted_all = halted_all and result.halted
                total_residue += hamming_residue(expected, result.output)
                outputs[str(inputs)] = result.output
            total_residue /= max(1, len(observations))
            cost = total_residue + 0.01 * len(program)
            candidate = {
                "program": program,
                "assembly": disassemble(program),
                "residue": total_residue,
                "cost": cost,
                "halted_all": halted_all,
                "outputs": outputs,
            }
            if best is None or (candidate["cost"], len(program)) < (best["cost"], len(best["program"])):  # type: ignore[index]
                best = candidate
            if total_residue == 0.0 and halted_all:
                return candidate

    assert best is not None
    return best


def demo() -> Dict[str, object]:
    program = assemble(["OBS 0", "XOR 0 1", "OUT 0", "HALT"])
    machine = ObsBitMachine()
    return {
        "program_bytes": program,
        "assembly": disassemble(program),
        "runs": {
            "1,0": machine.run(program, [1, 0]).__dict__,
            "1,1": machine.run(program, [1, 1]).__dict__,
        },
    }


if __name__ == "__main__":
    import json

    print(json.dumps(demo(), indent=2, ensure_ascii=False))
