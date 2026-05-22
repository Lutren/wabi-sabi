import os

from wabi_sabi.core.provider_onboarding import (
    capture_secret_to_user_env,
    format_provider_onboarding,
    provider_onboarding_report,
)
from wabi_sabi.core.runtime_diagnostics import build_provider_report, debug_deepseek_provider


def test_provider_onboarding_report_has_qwen_deepseek_without_secret_values(monkeypatch):
    monkeypatch.setenv("DASHSCOPE_API_KEY", "dashscope-unit-secret")

    payload = provider_onboarding_report()
    rendered = format_provider_onboarding(payload)

    assert payload["secret_values_printed"] is False
    assert "qwen" in rendered.lower()
    assert "deepseek" in rendered.lower()
    assert "dashscope-unit-secret" not in rendered


def test_capture_secret_to_user_env_uses_allowlist_and_no_value_in_result(monkeypatch):
    stored = {}
    monkeypatch.delenv("DEEPSEEK_API_KEY", raising=False)

    result = capture_secret_to_user_env(
        "DEEPSEEK_API_KEY",
        secret_getter=lambda _prompt: "deepseek-unit-secret",
        set_user_env=lambda key, value: stored.setdefault(key, value),
    )

    assert result["ok"] is True
    assert result["secret_values_printed"] is False
    assert stored["DEEPSEEK_API_KEY"] == "deepseek-unit-secret"
    assert "deepseek-unit-secret" not in str(result)
    assert os.environ["DEEPSEEK_API_KEY"] == "deepseek-unit-secret"
    monkeypatch.delenv("DEEPSEEK_API_KEY", raising=False)


def test_capture_secret_to_user_env_blocks_unknown_key():
    result = capture_secret_to_user_env("NOT_ALLOWED_KEY", secret_getter=lambda _prompt: "secret")

    assert result["ok"] is False
    assert result["status"] == "BLOCK"


def test_provider_matrix_includes_free_openai_compatible_routes(tmp_path, monkeypatch):
    monkeypatch.delenv("QWEN_API_KEY", raising=False)
    monkeypatch.delenv("DASHSCOPE_API_KEY", raising=False)
    monkeypatch.delenv("DEEPSEEK_API_KEY", raising=False)

    report = build_provider_report(runtime_root=tmp_path / "runtime", smoke=False)
    providers = {row["provider"]: row for row in report["providers"]}

    assert {"nvidia", "qwen", "dashscope_qwen", "deepseek", "openrouter", "openai_compatible"}.issubset(providers)
    assert providers["qwen"]["smoke_model"] == "qwen-plus"
    assert providers["deepseek"]["coding_model"] == "deepseek-chat"


def test_deepseek_debug_missing_env_is_concrete(monkeypatch):
    monkeypatch.delenv("DEEPSEEK_API_KEY", raising=False)

    payload = debug_deepseek_provider()

    assert payload["classification"] == "MISSING_ENV"
    assert payload["secret_values_printed"] is False
