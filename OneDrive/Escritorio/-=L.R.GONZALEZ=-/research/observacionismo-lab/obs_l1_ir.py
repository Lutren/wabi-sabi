#!/usr/bin/env python3
"""
L1 observational IR for the ObsBitMachine.

The surface is deliberately small: OBSERVAR, DOCUMENTAR, VERIFICAR, ACTUAR and
HANDOFF. Parsing produces bytecode plus explicit checks. Verification stays out
of bytecode so the machine remains minimal and auditable.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from typing import Dict, Iterable, List, Sequence

from obs_bit_machine import ObsBitMachine, assemble, disassemble


VERB_ALIASES = {
    "OBSERVAR": "OBSERVAR",
    "OBSERVE": "OBSERVAR",
    "DOCUMENTAR": "DOCUMENTAR",
    "DOCUMENT": "DOCUMENTAR",
    "DOC": "DOCUMENTAR",
    "VERIFICAR": "VERIFICAR",
    "VERIFY": "VERIFICAR",
    "ACTUAR": "ACTUAR",
    "ACT": "ACTUAR",
    "HANDOFF": "HANDOFF",
    "ENTREGAR": "HANDOFF",
}

ACTION_TO_L0 = {
    "NOP": "NOP",
    "ZERO": "ZERO",
    "CERO": "ZERO",
    "ONE": "ONE",
    "UNO": "ONE",
    "XOR": "XOR",
    "AND": "AND",
}


@dataclass(frozen=True)
class L1Step:
    verb: str
    args: List[str]
    line_no: int
    source: str


@dataclass(frozen=True)
class L1Check:
    subject: str
    operator: str
    expected: str
    line_no: int


@dataclass
class L1Program:
    steps: List[L1Step] = field(default_factory=list)
    checks: List[L1Check] = field(default_factory=list)
    bytecode: List[int] = field(default_factory=list)

    def assembly(self) -> List[str]:
        return disassemble(self.bytecode)


def _tokens(line: str) -> List[str]:
    return line.replace(",", " ").split()


def _parse_address(value: str) -> int:
    try:
        return int(value)
    except ValueError as exc:
        raise ValueError(f"address must be an integer: {value}") from exc


def _compile_observar(args: Sequence[str]) -> str:
    if len(args) != 2 or args[0].upper() not in {"BIT", "MEM"}:
        raise ValueError("OBSERVAR expects: OBSERVAR bit <addr>")
    return f"OBS {_parse_address(args[1])}"


def _compile_documentar(args: Sequence[str]) -> str:
    if len(args) != 2 or args[0].upper() not in {"BIT", "MEM", "SALIDA", "OUTPUT"}:
        raise ValueError("DOCUMENTAR expects: DOCUMENTAR bit <addr>")
    return f"OUT {_parse_address(args[1])}"


def _compile_actuar(args: Sequence[str]) -> str:
    if not args:
        raise ValueError("ACTUAR expects an action")
    action = ACTION_TO_L0.get(args[0].upper())
    if action is None:
        raise ValueError(f"unknown ACTUAR action: {args[0]}")
    if action in {"NOP"}:
        if len(args) != 1:
            raise ValueError("ACTUAR nop takes no address")
        return "NOP"
    if action in {"ZERO", "ONE"}:
        if len(args) != 2:
            raise ValueError(f"ACTUAR {args[0]} expects one address")
        return f"{action} {_parse_address(args[1])}"
    if action in {"XOR", "AND"}:
        if len(args) != 3:
            raise ValueError(f"ACTUAR {args[0]} expects two addresses")
        return f"{action} {_parse_address(args[1])} {_parse_address(args[2])}"
    raise AssertionError(action)


def _parse_check(args: Sequence[str], line_no: int) -> L1Check:
    if len(args) != 3:
        raise ValueError("VERIFICAR expects: VERIFICAR <subject> <op> <expected>")
    subject = args[0].lower()
    operator = args[1]
    if subject not in {"output", "salida", "halted", "residue"}:
        raise ValueError(f"unknown check subject: {subject}")
    if operator not in {"==", "<=", ">="}:
        raise ValueError(f"unknown check operator: {operator}")
    return L1Check(subject=subject, operator=operator, expected=args[2], line_no=line_no)


def parse_l1(script: str) -> L1Program:
    steps: List[L1Step] = []
    checks: List[L1Check] = []
    assembly: List[str] = []
    seen_handoff = False

    for line_no, raw in enumerate(script.splitlines(), start=1):
        line = raw.split("#", 1)[0].strip()
        if not line:
            continue
        parts = _tokens(line)
        verb = VERB_ALIASES.get(parts[0].upper())
        if verb is None:
            raise ValueError(f"line {line_no}: unknown L1 verb: {parts[0]}")
        if seen_handoff:
            raise ValueError(f"line {line_no}: no steps allowed after HANDOFF")
        args = parts[1:]
        steps.append(L1Step(verb=verb, args=list(args), line_no=line_no, source=line))

        if verb == "OBSERVAR":
            assembly.append(_compile_observar(args))
        elif verb == "DOCUMENTAR":
            assembly.append(_compile_documentar(args))
        elif verb == "ACTUAR":
            assembly.append(_compile_actuar(args))
        elif verb == "VERIFICAR":
            checks.append(_parse_check(args, line_no))
        elif verb == "HANDOFF":
            assembly.append("HALT")
            seen_handoff = True

    if not seen_handoff:
        raise ValueError("L1 program must end with HANDOFF")
    return L1Program(steps=steps, checks=checks, bytecode=assemble(assembly))


def _parse_expected_bits(raw: str) -> List[int]:
    if raw in {"[]", "empty", "vacio"}:
        return []
    if raw.startswith("[") and raw.endswith("]"):
        raw = raw[1:-1]
    return [1 if part.strip() in {"1", "true", "TRUE"} else 0 for part in raw.replace(",", " ").split()]


def _eval_check(check: L1Check, result) -> Dict[str, object]:
    subject = check.subject
    actual: object
    expected: object
    if subject in {"output", "salida"}:
        actual = result.output
        expected = _parse_expected_bits(check.expected)
    elif subject == "halted":
        actual = result.halted
        expected = check.expected.lower() in {"1", "true", "yes", "si"}
    elif subject == "residue":
        actual = float(result.residue)
        expected = float(check.expected)
    else:
        raise AssertionError(subject)

    if check.operator == "==":
        passed = actual == expected
    elif check.operator == "<=":
        passed = float(actual) <= float(expected)  # type: ignore[arg-type]
    elif check.operator == ">=":
        passed = float(actual) >= float(expected)  # type: ignore[arg-type]
    else:
        raise AssertionError(check.operator)

    return {
        "line_no": check.line_no,
        "subject": check.subject,
        "operator": check.operator,
        "expected": expected,
        "actual": actual,
        "passed": passed,
    }


def fingerprint(payload: Dict[str, object], prefix: str = "OBS_L1") -> str:
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
    digest = hashlib.sha256(canonical.encode("utf-8")).hexdigest()[:16]
    return f"{prefix}_{digest}"


def run_l1(script: str, inputs: Sequence[int] = ()) -> Dict[str, object]:
    program = parse_l1(script)
    machine = ObsBitMachine()
    result = machine.run(program.bytecode, inputs)
    check_results = [_eval_check(check, result) for check in program.checks]
    ok = result.halted and all(item["passed"] for item in check_results)
    payload: Dict[str, object] = {
        "ok": ok,
        "inputs": list(inputs),
        "bytecode": program.bytecode,
        "assembly": program.assembly(),
        "output": result.output,
        "halted": result.halted,
        "residue": result.residue,
        "phi_eff": result.phi_eff,
        "checks": check_results,
    }
    payload["fingerprint"] = fingerprint(payload)
    payload["observation_envelope"] = {
        "envelope_version": "seto-observation-v1",
        "source_kind": "l1_script",
        "evidence": [
            "L1 parsed with five verbs",
            "compiled to ObsBitMachine bytecode",
            "checks evaluated after VM run",
        ],
        "psi_state": "CERTEZA" if ok else "INFERENCIA",
        "claim_level": "operational",
        "falsifiers": [
            "parser rejects program",
            "VM result does not satisfy checks",
            "program does not halt",
        ],
        "risk_flags": [],
        "action_gate": "APPROVE" if ok else "REVIEW",
        "decision": "KEEP" if ok else "REVIEW",
        "fingerprint": payload["fingerprint"],
    }
    return payload


def demo() -> Dict[str, object]:
    script = """
    OBSERVAR bit 0
    ACTUAR xor 0 1
    DOCUMENTAR bit 0
    VERIFICAR output == [1]
    VERIFICAR halted == true
    VERIFICAR residue <= 0
    HANDOFF
    """
    return run_l1(script, inputs=[1, 0])


if __name__ == "__main__":
    print(json.dumps(demo(), indent=2, ensure_ascii=False))
