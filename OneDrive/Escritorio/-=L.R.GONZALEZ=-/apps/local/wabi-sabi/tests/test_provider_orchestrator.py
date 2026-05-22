from types import SimpleNamespace

from wabi_sabi.core.provider_orchestrator import ProviderOrchestrator


def test_provider_orchestrator_default_uses_base_model_when_available(tmp_path, monkeypatch):
    monkeypatch.delenv("WABI_PROVIDER_ORDER", raising=False)
    monkeypatch.delenv("WABI_ENABLE_OLLAMA", raising=False)
    monkeypatch.delenv("WABI_DISABLE_BASE_MODEL", raising=False)
    monkeypatch.delenv("WABI_ALLOW_CLOUD_PROVIDERS", raising=False)  # ensure cloud-first logic is off
    orchestrator = ProviderOrchestrator(workspace=tmp_path, runtime_root=tmp_path / "runtime")
    calls = {"codex": 0, "ollama": 0}

    def fake_codex(prompt, **kwargs):
        calls["codex"] += 1
        return SimpleNamespace(
            to_dict=lambda: {
                "ok": False,
                "action": "codex_failed",
                "output": "sin creditos",
                "error": "credits_exhausted",
                "artifacts": [],
            }
        )

    orchestrator.codex.ask = fake_codex
    orchestrator.ollama.status = lambda: {
        "available": True,
        "base_model": "qwen2.5-coder:3b",
        "models": ["qwen2.5-coder:3b"],
        "running": [],
        "base_model_available": True,
    }
    orchestrator.ollama.generate = lambda *args, **kwargs: (
        calls.__setitem__("ollama", calls["ollama"] + 1)
        or SimpleNamespace(
            to_dict=lambda: {
                "ok": True,
                "action": "ollama_generate",
                "output": "respuesta base",
                "error": "",
                "artifacts": ["base.md"],
            }
        )
    )

    result = orchestrator.ask("hola")

    assert result.ok is True
    assert result.provider == "ollama"
    assert result.output == "respuesta base"
    assert calls == {"codex": 0, "ollama": 1}
    assert [attempt["provider"] for attempt in result.attempts] == ["ollama"]


def test_provider_orchestrator_can_disable_base_model_and_use_dry_run(tmp_path, monkeypatch):
    monkeypatch.delenv("WABI_PROVIDER_ORDER", raising=False)
    monkeypatch.delenv("WABI_ENABLE_OLLAMA", raising=False)
    monkeypatch.setenv("WABI_DISABLE_BASE_MODEL", "1")
    monkeypatch.delenv("WABI_ALLOW_CLOUD_PROVIDERS", raising=False)  # ensure cloud-first logic is off
    orchestrator = ProviderOrchestrator(workspace=tmp_path, runtime_root=tmp_path / "runtime")
    calls = {"codex": 0, "ollama": 0}

    def fake_codex(prompt, **kwargs):
        calls["codex"] += 1
        ok = kwargs.get("dry_run", False) or kwargs.get("provider") == "dry-run"
        return SimpleNamespace(
            to_dict=lambda: {
                "ok": ok,
                "action": "dry_run" if ok else "codex_failed",
                "output": "workpack" if ok else "sin creditos",
                "error": "" if ok else "credits_exhausted",
                "artifacts": ["workpack.json"] if ok else [],
            }
        )

    orchestrator.codex.ask = fake_codex
    orchestrator.ollama.generate = lambda *args, **kwargs: calls.__setitem__("ollama", calls["ollama"] + 1)

    result = orchestrator.ask("hola")

    assert result.ok is True
    assert result.provider == "dry-run"
    assert result.output == "workpack"
    assert calls == {"codex": 2, "ollama": 0}
    assert [attempt["provider"] for attempt in result.attempts] == ["codex", "dry-run"]


def test_provider_orchestrator_no_model_mode_uses_only_dry_run(tmp_path, monkeypatch):
    monkeypatch.setenv("MEDIOEVO_NO_MODEL_MODE", "1")
    monkeypatch.setenv("WABI_PROVIDER_ORDER", "ollama,codex,dry-run")
    monkeypatch.setenv("WABI_ENABLE_OLLAMA", "1")
    orchestrator = ProviderOrchestrator(workspace=tmp_path, runtime_root=tmp_path / "runtime")
    calls = {"codex": 0, "ollama": 0}

    def fake_codex(prompt, **kwargs):
        calls["codex"] += 1
        return SimpleNamespace(
            to_dict=lambda: {
                "ok": True,
                "action": "dry_run",
                "output": "workpack",
                "error": "",
                "artifacts": ["workpack.json"],
            }
        )

    orchestrator.codex.ask = fake_codex
    orchestrator.ollama.generate = lambda *args, **kwargs: calls.__setitem__("ollama", calls["ollama"] + 1)

    result = orchestrator.ask("hola", provider="ollama")

    assert result.ok is True
    assert result.provider == "dry-run"
    assert orchestrator.provider_order() == ["dry-run"]
    assert orchestrator.status()["ollama"]["model_status"] == "UNAVAILABLE"
    assert calls == {"codex": 1, "ollama": 0}


def test_provider_orchestrator_falls_back_to_ollama_when_explicitly_enabled(tmp_path, monkeypatch):
    monkeypatch.setenv("WABI_PROVIDER_ORDER", "codex,ollama,dry-run")
    monkeypatch.setenv("WABI_ENABLE_OLLAMA", "1")
    orchestrator = ProviderOrchestrator(workspace=tmp_path, runtime_root=tmp_path / "runtime")
    orchestrator.codex.ask = lambda *args, **kwargs: SimpleNamespace(
        to_dict=lambda: {
            "ok": False,
            "action": "codex_failed",
            "output": "sin creditos",
            "error": "credits_exhausted",
            "artifacts": [],
        }
    )
    orchestrator.ollama.generate = lambda *args, **kwargs: SimpleNamespace(
        to_dict=lambda: {
            "ok": True,
            "action": "ollama_generate",
            "output": "respuesta local",
            "error": "",
            "artifacts": ["local.md"],
        }
    )
    orchestrator.ollama.status = lambda: {"available": True, "models": ["qwen2.5:0.5b"], "running": []}

    result = orchestrator.ask("hola")

    assert result.ok is True
    assert result.provider == "ollama"
    assert result.output == "respuesta local"
    assert result.attempts[0]["provider"] == "codex"
    assert result.attempts[1]["provider"] == "ollama"


def test_provider_orchestrator_ends_with_dry_run(tmp_path, monkeypatch):
    monkeypatch.setenv("WABI_PROVIDER_ORDER", "codex,ollama,dry-run")
    monkeypatch.setenv("WABI_ENABLE_OLLAMA", "1")
    orchestrator = ProviderOrchestrator(workspace=tmp_path, runtime_root=tmp_path / "runtime")
    calls = {"codex": 0}

    def fake_codex(prompt, **kwargs):
        calls["codex"] += 1
        ok = kwargs.get("dry_run", False) or kwargs.get("provider") == "dry-run"
        return SimpleNamespace(
            to_dict=lambda: {
                "ok": ok,
                "action": "dry_run" if ok else "codex_failed",
                "output": "workpack" if ok else "fallo",
                "error": "" if ok else "failed",
                "artifacts": ["workpack.json"] if ok else [],
            }
        )

    orchestrator.codex.ask = fake_codex
    orchestrator.ollama.generate = lambda *args, **kwargs: SimpleNamespace(
        to_dict=lambda: {
            "ok": False,
            "action": "ollama_failed",
            "output": "fallo local",
            "error": "timeout",
            "artifacts": [],
        }
    )
    orchestrator.ollama.status = lambda: {"available": False, "models": [], "running": []}

    result = orchestrator.ask("hola")

    assert result.ok is True
    assert result.provider == "dry-run"
    assert result.output == "workpack"
    assert calls["codex"] == 2


def test_provider_orchestrator_reports_cloud_adapters_redacted(tmp_path, monkeypatch):
    monkeypatch.setenv("NVIDIA_API_KEY", "nvapi-test-secret-1234567890")
    orchestrator = ProviderOrchestrator(workspace=tmp_path, runtime_root=tmp_path / "runtime")

    status = orchestrator.status()

    assert "cloud" in status
    assert status["cloud"]["nvidia-nim"]["configured"] is True
    assert "nvapi-test-secret" not in str(status)


def test_provider_orchestrator_cloud_provider_falls_back_when_disabled(tmp_path, monkeypatch):
    monkeypatch.setenv("NVIDIA_API_KEY", "nvapi-test-secret-1234567890")
    monkeypatch.delenv("WABI_ALLOW_CLOUD_PROVIDERS", raising=False)
    orchestrator = ProviderOrchestrator(workspace=tmp_path, runtime_root=tmp_path / "runtime")
    orchestrator.codex.ask = lambda *args, **kwargs: SimpleNamespace(
        to_dict=lambda: {
            "ok": True,
            "action": "dry_run",
            "output": "workpack",
            "error": "",
            "artifacts": ["workpack.json"],
        }
    )

    result = orchestrator.ask("hola", provider="nvidia-nim")

    assert result.ok is True
    assert result.provider == "dry-run"
    assert [attempt["provider"] for attempt in result.attempts] == ["nvidia-nim", "dry-run"]


def test_provider_orchestrator_public_model_alias_falls_back_when_disabled(tmp_path, monkeypatch):
    monkeypatch.setenv("NVIDIA_API_KEY", "nvapi-test-secret-1234567890")
    monkeypatch.delenv("WABI_ALLOW_CLOUD_PROVIDERS", raising=False)
    orchestrator = ProviderOrchestrator(workspace=tmp_path, runtime_root=tmp_path / "runtime")
    orchestrator.codex.ask = lambda *args, **kwargs: SimpleNamespace(
        to_dict=lambda: {
            "ok": True,
            "action": "dry_run",
            "output": "workpack",
            "error": "",
            "artifacts": ["workpack.json"],
        }
    )

    result = orchestrator.ask("hola", provider="kimi")

    assert result.ok is True
    assert result.provider == "dry-run"
    assert [attempt["provider"] for attempt in result.attempts] == ["nvidia-nim:kimi", "dry-run"]
