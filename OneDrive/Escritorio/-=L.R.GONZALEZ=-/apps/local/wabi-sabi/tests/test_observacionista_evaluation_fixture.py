from types import SimpleNamespace

from wabi_sabi.core.provider_orchestrator import ProviderOrchestrator


PROMPT = "Evalua observacionista: separa CERTEZA, INFERENCIA e INCOGNITA sin secretos."


def _result(*, ok=True, action="dry_run", output="CERTEZA: fixture", error="", artifacts=None):
    return SimpleNamespace(
        to_dict=lambda: {
            "ok": ok,
            "action": action,
            "output": output,
            "error": error,
            "artifacts": list(artifacts or []),
        }
    )


class _FakeCloudAdapter:
    def status(self):
        return {"configured": True, "available": True, "model": "qwen-fixture", "secret": "[REDACTED]"}

    def execute(self, prompt, timeout=180, **kwargs):
        return _result(
            action="cloud_mock",
            output="CERTEZA: cloud mock ok\nINFERENCIA: sin red real\nINCOGNITA: none",
            artifacts=["cloud-mock.json"],
        )


def test_observacionista_fixture_compares_local_dry_run_and_cloud_mock(tmp_path, monkeypatch):
    monkeypatch.setenv("WABI_DISABLE_BASE_MODEL", "1")
    monkeypatch.delenv("WABI_PROVIDER_ORDER", raising=False)
    dry = ProviderOrchestrator(workspace=tmp_path, runtime_root=tmp_path / "runtime-dry")
    dry.ollama.status = lambda: {"available": False, "models": [], "running": []}
    dry.codex.ask = lambda *args, **kwargs: _result(
        ok=kwargs.get("dry_run", False) or kwargs.get("provider") == "dry-run",
        action="dry_run" if kwargs.get("dry_run", False) or kwargs.get("provider") == "dry-run" else "codex_failed",
        output="CERTEZA: dry-run ok",
        error="" if kwargs.get("dry_run", False) or kwargs.get("provider") == "dry-run" else "offline",
        artifacts=["dry-run.json"],
    )

    dry_result = dry.ask(PROMPT)

    assert dry_result.ok is True
    assert dry_result.provider == "dry-run"
    assert [attempt["provider"] for attempt in dry_result.attempts] == ["codex", "dry-run"]

    monkeypatch.delenv("WABI_DISABLE_BASE_MODEL", raising=False)
    monkeypatch.setenv("WABI_ENABLE_OLLAMA", "1")
    monkeypatch.setenv("WABI_PROVIDER_ORDER", "ollama,dry-run")
    local = ProviderOrchestrator(workspace=tmp_path, runtime_root=tmp_path / "runtime-local")
    local.ollama.status = lambda: {"available": True, "models": ["qwen2.5:0.5b"], "running": []}
    local.ollama.generate = lambda *args, **kwargs: _result(
        action="ollama_generate",
        output="CERTEZA: local mock ok\nINFERENCIA: modelo local simulado",
        artifacts=["local-mock.md"],
    )

    local_result = local.ask(PROMPT)

    assert local_result.ok is True
    assert local_result.provider == "ollama"
    assert "CERTEZA" in local_result.output

    monkeypatch.delenv("WABI_ENABLE_OLLAMA", raising=False)
    monkeypatch.delenv("WABI_PROVIDER_ORDER", raising=False)
    monkeypatch.setenv("WABI_ALLOW_CLOUD_PROVIDERS", "1")
    monkeypatch.setenv("QWEN_API_KEY", "qwen-test-secret-1234567890")
    cloud = ProviderOrchestrator(workspace=tmp_path, runtime_root=tmp_path / "runtime-cloud")
    cloud.ollama.status = lambda: {"available": False, "models": [], "running": []}
    cloud.cloud_adapters["qwen-cloud"] = _FakeCloudAdapter()

    cloud_result = cloud.ask(PROMPT, provider="qwen")

    assert cloud_result.ok is True
    assert cloud_result.provider == "qwen-cloud"
    assert cloud_result.attempts[0]["provider"] == "qwen-cloud"
    assert "qwen-test-secret" not in str(cloud_result.to_dict())

