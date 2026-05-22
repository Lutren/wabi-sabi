from __future__ import annotations

import json

from wabi_sabi.core.blueprint_policy import BlueprintPolicyLoader
from wabi_sabi.core.provider_orchestrator import ProviderOrchestrator


def test_blueprint_policy_loads_planos_from_portfolio_root(tmp_path):
    root = tmp_path / "-=L.R.GONZALEZ=-"
    app = root / "apps" / "local" / "wabi-sabi"
    runtime = app / "runtime"
    ops = root / "docs" / "ops"
    comms = root / "COMMS" / "agents_state"
    ops.mkdir(parents=True)
    comms.mkdir(parents=True)
    (ops / "WABI_OSIT_BRIDGE_FROM_ESTADO_2026-05-06.md").write_text(
        "Ollama queda como backend opcional, no como arquitectura.\n"
        "No llama modelos por defecto. Usa dry-run workpack.\n",
        encoding="utf-8",
    )
    (comms / "claudio-local-autonomy.json").write_text(
        json.dumps({"action_gate": "BLOCK", "blocked_actions": ["ollama_create_alias"]}),
        encoding="utf-8",
    )

    policy = BlueprintPolicyLoader(workspace=app, runtime_root=runtime).load()

    assert policy.loaded is True
    assert policy.root == str(root.resolve())
    assert policy.provider_order == ["codex", "dry-run"]
    assert policy.ollama_enabled_by_default is False
    assert "ollama_optional_by_blueprint" in policy.reasons
    assert "ollama_alias_blocked" in policy.reasons


def test_provider_order_filters_ollama_unless_opt_in(tmp_path, monkeypatch):
    monkeypatch.setenv("WABI_PROVIDER_ORDER", "codex,ollama,dry-run")
    monkeypatch.delenv("WABI_ENABLE_OLLAMA", raising=False)
    monkeypatch.setenv("WABI_DISABLE_BASE_MODEL", "1")

    orchestrator = ProviderOrchestrator(workspace=tmp_path, runtime_root=tmp_path / "runtime")

    assert orchestrator.provider_order() == ["codex", "dry-run"]
    assert orchestrator.status()["ollama"]["enabled"] is False


def test_explicit_ollama_provider_degrades_to_dry_run_when_disabled(tmp_path, monkeypatch):
    monkeypatch.delenv("WABI_ENABLE_OLLAMA", raising=False)
    monkeypatch.setenv("WABI_DISABLE_BASE_MODEL", "1")
    orchestrator = ProviderOrchestrator(workspace=tmp_path, runtime_root=tmp_path / "runtime")
    calls = {"ollama": 0}

    orchestrator.ollama.generate = lambda *args, **kwargs: calls.__setitem__("ollama", calls["ollama"] + 1)

    result = orchestrator.ask("hola", provider="ollama")

    assert result.ok is True
    assert result.provider == "dry-run"
    assert calls["ollama"] == 0
