#!/usr/bin/env python3
"""
Small Observacionista DSL compiler.

The DSL is intentionally boring: one directive per line, compiled into a JSON
shape that can be validated, witnessed and translated into Guardian payloads.
It is a cognitive layer over JSON, not a replacement for JSON.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any
import argparse
import json
import shlex


SCHEMA = "observacionista.dsl/v0.1"
VALID_STATES = {
    "observando",
    "planificando",
    "ejecutando",
    "renderizando",
    "qa",
    "esperando",
    "atascado",
    "requiere_aprobacion",
    "listo",
    "fallido",
}
VALID_RISKS = {"low", "medium", "high", "critical"}


class DSLParseError(ValueError):
    """Raised when the DSL cannot compile into a safe JSON contract."""


def _strip_comment(line: str) -> str:
    in_quote = False
    quote_char = ""
    for index, char in enumerate(line):
        if char in {"'", '"'} and (index == 0 or line[index - 1] != "\\"):
            if not in_quote:
                in_quote = True
                quote_char = char
            elif quote_char == char:
                in_quote = False
                quote_char = ""
        if char == "#" and not in_quote:
            return line[:index].strip()
    return line.strip()


def _tokenize(line: str, line_number: int) -> list[str]:
    try:
        return shlex.split(line, comments=False, posix=True)
    except ValueError as exc:
        raise DSLParseError(f"line {line_number}: {exc}") from exc


def _parse_tags(tokens: list[str]) -> tuple[list[str], list[str]]:
    tags: list[str] = []
    remaining: list[str] = []
    for token in tokens:
        if token.startswith("tags="):
            raw = token.split("=", 1)[1]
            tags.extend([item.strip() for item in raw.split(",") if item.strip()])
        else:
            remaining.append(token)
    return tags, remaining


def parse_dsl(text: str) -> dict[str, Any]:
    program: dict[str, Any] = {
        "schema": SCHEMA,
        "intent": "",
        "beliefs": [],
        "goals": [],
        "evidence": [],
        "risks": [],
        "waits": [],
        "states": [],
        "actions": [],
        "requires_approval": [],
        "witness": {},
        "recovery": [],
    }

    for line_number, raw_line in enumerate(text.splitlines(), start=1):
        line = _strip_comment(raw_line)
        if not line:
            continue
        tokens = _tokenize(line, line_number)
        if not tokens:
            continue
        directive = tokens[0].lower()
        values = tokens[1:]

        if directive == "intent":
            if not values:
                raise DSLParseError(f"line {line_number}: intent requires a value")
            program["intent"] = " ".join(values)
        elif directive == "belief":
            if len(values) < 1:
                raise DSLParseError(f"line {line_number}: belief requires a name")
            program["beliefs"].append({"name": values[0], "value": " ".join(values[1:]) or True})
        elif directive == "goal":
            if not values:
                raise DSLParseError(f"line {line_number}: goal requires a value")
            program["goals"].append(" ".join(values))
        elif directive == "evidence":
            if not values:
                raise DSLParseError(f"line {line_number}: evidence requires a name")
            program["evidence"].append({"name": values[0], "ref": " ".join(values[1:])})
        elif directive == "risk":
            if not values or values[0] not in VALID_RISKS:
                raise DSLParseError(f"line {line_number}: risk must be one of {sorted(VALID_RISKS)}")
            program["risks"].append({"level": values[0], "scope": " ".join(values[1:])})
        elif directive == "wait":
            if not values:
                raise DSLParseError(f"line {line_number}: wait requires a condition")
            program["waits"].append(" ".join(values))
        elif directive == "state":
            if not values or values[0] not in VALID_STATES:
                raise DSLParseError(f"line {line_number}: state must be one of {sorted(VALID_STATES)}")
            program["states"].append(values[0])
        elif directive == "action":
            if not values:
                raise DSLParseError(f"line {line_number}: action requires a name")
            tags, rest = _parse_tags(values[1:])
            program["actions"].append({"name": values[0], "args": rest, "tags": tags})
        elif directive in {"approval", "approve", "require"}:
            if not values:
                raise DSLParseError(f"line {line_number}: {directive} requires a gate name")
            program["requires_approval"].append(values[0])
        elif directive == "witness":
            if not values:
                raise DSLParseError(f"line {line_number}: witness requires a path")
            program["witness"] = {"log": " ".join(values)}
        elif directive == "recovery":
            if len(values) < 2:
                raise DSLParseError(f"line {line_number}: recovery requires target and step")
            program["recovery"].append({"on": values[0], "step": " ".join(values[1:])})
        else:
            raise DSLParseError(f"line {line_number}: unknown directive {directive!r}")

    validate_program(program)
    return program


def validate_program(program: dict[str, Any]) -> None:
    if not program.get("intent"):
        raise DSLParseError("intent is required")
    if not program.get("actions"):
        raise DSLParseError("at least one action is required")
    if not program.get("states"):
        raise DSLParseError("at least one state is required")
    if not program.get("evidence"):
        raise DSLParseError("at least one evidence item is required")
    if not program.get("witness", {}).get("log"):
        raise DSLParseError("witness log is required")


def compile_file(path: str | Path) -> dict[str, Any]:
    return parse_dsl(Path(path).read_text(encoding="utf-8"))


def to_gate_payload(program: dict[str, Any]) -> dict[str, Any]:
    """Translate a compiled DSL program into the shared Guardian gate payload."""
    validate_program(program)
    action = program["actions"][0]["name"]
    tags = set(program.get("requires_approval", []))
    for item in program.get("actions", []):
        tags.update(item.get("tags", []))

    evidence_names = {item.get("name", "") for item in program.get("evidence", [])}
    risk_levels = {item.get("level", "low") for item in program.get("risks", [])}
    browser = "browser" in tags or action.startswith("browser_")
    manifest = "browser_manifest" in evidence_names
    paid_api = "paid_api" in tags or "spend_credits" in tags
    irreversible = "irreversible" in tags or "publish" in tags or "clone_voice" in tags

    return {
        "action": action,
        "tags": sorted(tags | ({"irreversible"} if irreversible else set())),
        "evidence": bool(program.get("evidence")),
        "R": 0.0,
        "J_c": 0.65,
        "epsilon": 0.75 if "critical" in risk_levels else 0.0,
        "browser": browser,
        "manifest": manifest,
        "paid_api": paid_api,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Compile Observacionista DSL to JSON")
    parser.add_argument("path", help="Path to .dsl file")
    parser.add_argument("--gate-payload", action="store_true", help="Print Guardian gate payload instead")
    args = parser.parse_args()

    program = compile_file(args.path)
    output = to_gate_payload(program) if args.gate_payload else program
    print(json.dumps(output, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
