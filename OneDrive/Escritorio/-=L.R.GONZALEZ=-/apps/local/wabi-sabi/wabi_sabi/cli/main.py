from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict
from pathlib import Path
from typing import Any

from wabi_sabi.agents.base_agent import AgentInput, AgentResult
from wabi_sabi.cli.parser import parse_command
from wabi_sabi.cli.router import AgentRegistry
from wabi_sabi.core.config import RuntimeConfig, build_config
from wabi_sabi.core.gate import ActionGate
from wabi_sabi.core.memory import LocalMemory
from wabi_sabi.core.observation import ObservationEnvelope


def execute_prompt(
    prompt: str,
    *,
    workspace: str | Path | None = None,
    runtime_root: str | Path | None = None,
    agent_name: str | None = None,
    json_mode: bool = False,
) -> dict[str, Any]:
    config = build_config(workspace=workspace, runtime_root=runtime_root)
    registry = AgentRegistry(config.registry_path)
    parsed = parse_command(prompt)
    gate = ActionGate().evaluate_text(prompt)
    selected = registry.select_agent_name(parsed, explicit=agent_name)
    memory = LocalMemory(config.runtime_root)

    if gate.gate == "BLOCK":
        result = AgentResult(
            agent_name=selected,
            ok=False,
            action="blocked_by_action_gate",
            output="La accion fue bloqueada por ActionGate local.",
            evidence=gate.reasons,
            certainty=["El pedido cruza una frontera bloqueada."],
            inference=[],
            unknown=["Se requiere autorizacion/gate especifico para continuar."],
            error=";".join(gate.reasons),
        )
    else:
        agent = registry.build_agent(selected, config)
        result = agent.run(AgentInput(prompt=prompt, parsed=parsed))

    envelope = ObservationEnvelope(
        prompt=prompt,
        intent=parsed.intent,
        agent=result.agent_name,
        action_gate=gate.gate,
        certainty=result.certainty,
        inference=result.inference,
        unknown=result.unknown,
        artifacts=result.artifacts,
        evidence=result.evidence,
    ).finalize()

    event = {
        "prompt": prompt,
        "parsed": asdict(parsed),
        "agent": result.agent_name,
        "gate": gate.gate,
        "gate_reasons": gate.reasons,
        "ok": result.ok,
        "action": result.action,
        "artifacts": result.artifacts,
        "fingerprint": envelope.fingerprint,
    }
    log_path = memory.append_event(event)
    memory.append_memory({"prompt": prompt, "intent": parsed.intent, "agent": result.agent_name})

    payload = {
        "ok": result.ok,
        "prompt": prompt,
        "intent": parsed.intent,
        "confidence": parsed.confidence,
        "agent": result.agent_name,
        "gate": gate.gate,
        "gate_reasons": gate.reasons,
        "action": result.action,
        "output": result.output,
        "artifacts": result.artifacts,
        "evidence": result.evidence,
        "certainty": result.certainty,
        "inference": result.inference,
        "unknown": result.unknown,
        "error": result.error,
        "log": str(log_path),
        "fingerprint": envelope.fingerprint,
        "observation": envelope.to_dict(),
    }
    if not json_mode:
        print(_format_payload(payload))
    return payload


def _format_payload(payload: dict[str, Any]) -> str:
    lines = [
        "WABI SABI LOCAL",
        f"Intento: {payload['intent']}  Agente: {payload['agent']}  Gate: {payload['gate']}",
        f"Resultado: {'OK' if payload['ok'] else 'BLOCK'}",
        "",
        "CERTEZA:",
    ]
    lines.extend(f"- {item}" for item in payload["certainty"])
    lines.append("")
    lines.append("INFERENCIA:")
    lines.extend(f"- {item}" for item in payload["inference"])
    lines.append("")
    lines.append("INCOGNITA:")
    lines.extend(f"- {item}" for item in payload["unknown"])
    lines.append("")
    lines.append("ACCION:")
    lines.append(f"- {payload['action']}: {payload['output']}")
    lines.append("")
    lines.append("ARTEFACTOS:")
    if payload["artifacts"]:
        lines.extend(f"- {artifact}" for artifact in payload["artifacts"])
    else:
        lines.append("- Sin artefactos nuevos.")
    lines.append(f"- Log: {payload['log']}")
    lines.append(f"- Fingerprint: {payload['fingerprint']}")
    return "\n".join(lines)


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="wabi", description="Wabi Sabi local agent CLI")
    parser.add_argument("items", nargs="*", help="Prompt or subcommand")
    parser.add_argument("--workspace", default=None, help="Workspace to inspect")
    parser.add_argument("--runtime", default=None, help="Runtime/log directory")
    parser.add_argument("--agent", default=None, help="Force a specific agent")
    parser.add_argument("--json", action="store_true", help="Emit JSON")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_arg_parser().parse_args(argv)
    items = args.items
    config = build_config(workspace=args.workspace, runtime_root=args.runtime)
    registry = AgentRegistry(config.registry_path)
    if not items:
        return _interactive(config)
    command = items[0].lower()
    if command == "agents":
        payload = registry.as_dict()
        print(json.dumps(payload, indent=2, ensure_ascii=False) if args.json else _format_agents(payload))
        return 0
    if command in {"diagnose", "diagnostico", "diagnóstico"}:
        payload = execute_prompt(
            "ejecuta diagnostico",
            workspace=args.workspace,
            runtime_root=args.runtime,
            agent_name=args.agent,
            json_mode=args.json,
        )
        if args.json:
            print(json.dumps(payload, indent=2, ensure_ascii=False))
        return 0 if payload["ok"] else 2
    if command == "logs":
        memory = LocalMemory(config.runtime_root)
        print(json.dumps(memory.tail_events(), indent=2, ensure_ascii=False))
        return 0
    if command == "e2e-smoke":
        payload = execute_prompt(
            "crea una funcion que lea un archivo y resuma sus lineas",
            workspace=args.workspace,
            runtime_root=args.runtime,
            json_mode=args.json,
        )
        if args.json:
            print(json.dumps(payload, indent=2, ensure_ascii=False))
        return 0 if payload["ok"] else 2

    prompt = " ".join(items)
    payload = execute_prompt(
        prompt,
        workspace=args.workspace,
        runtime_root=args.runtime,
        agent_name=args.agent,
        json_mode=args.json,
    )
    if args.json:
        print(json.dumps(payload, indent=2, ensure_ascii=False))
    return 0 if payload["ok"] else 2


def _interactive(config: RuntimeConfig) -> int:
    print("Wabi Sabi Local. Escribe /exit para salir.")
    while True:
        try:
            prompt = input("Wabi> ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            return 0
        if not prompt:
            continue
        if prompt in {"/exit", "exit", "salir"}:
            return 0
        execute_prompt(prompt, workspace=config.workspace, runtime_root=config.runtime_root)


def _format_agents(payload: dict[str, Any]) -> str:
    lines = ["WABI SABI AGENTS"]
    for name, spec in payload.get("agents", {}).items():
        lines.append(f"- {name}: {spec.get('description', '')}")
        lines.append(f"  capacidades: {', '.join(spec.get('capabilities', []))}")
        lines.append(f"  limites: {', '.join(spec.get('limits', []))}")
    return "\n".join(lines)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
