from wabi_sabi.cli.parser import parse_command
from wabi_sabi.cli.router import AgentRegistry
from wabi_sabi.core.config import build_config


def test_programmer_intent_routes_to_programmer(tmp_path):
    config = build_config(workspace=tmp_path, runtime_root=tmp_path / "runtime")
    registry = AgentRegistry(config.registry_path)
    parsed = parse_command("crea una funcion que lea un archivo y resuma sus lineas")

    assert parsed.intent == "code_generation"
    assert registry.select_agent_name(parsed) == "programmer"


def test_diagnostic_intent_routes_to_debugger(tmp_path):
    config = build_config(workspace=tmp_path, runtime_root=tmp_path / "runtime")
    registry = AgentRegistry(config.registry_path)
    parsed = parse_command("ejecuta diagnostico")

    assert parsed.intent == "debug_diagnostics"
    assert registry.select_agent_name(parsed) == "debugger"
