from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from wabi_sabi.core.provider_status_contract import (
    PRIMARY_MODEL,
    SMOKE_PROMPT,
    build_provider_status_contract,
    run_nvidia_live_smoke,
)


def run_cli(*args, workspace: Path, runtime: Path):
    return subprocess.run(
        [
            sys.executable,
            "-m",
            "wabi_sabi.cli.main",
            *args,
            "--workspace",
            str(workspace),
            "--runtime",
            str(runtime),
        ],
        cwd=workspace,
        text=True,
        capture_output=True,
        check=False,
    )


def test_provider_status_contract_redacts_credentials(tmp_path):
    secret = "provider-status-secret-value-1234567890"
    env = {"WABI_ALLOW_CLOUD_PROVIDERS": "1", "NVIDIA_API_KEY": secret}

    payload = build_provider_status_contract(runtime_root=tmp_path / "runtime", env=env)
    text = json.dumps(payload, ensure_ascii=False)

    assert payload["primary_provider"] == "nvidia"
    assert payload["primary_model"] == PRIMARY_MODEL
    assert payload["fallback_provider"] == "ollama"
    assert payload["fallback_model"] == "qwen2.5:0.5b"
    assert payload["cloud_allowed_mode"] == "SESSION_FLAG_ENABLED"
    assert payload["credential_present_redacted"] is True
    assert payload["active_credential_env"] == "NVIDIA_API_KEY"
    assert payload["workspace_sent"] is False
    assert payload["secret_values_printed"] is False
    assert secret not in text


def test_live_smoke_skips_when_flag_disabled(tmp_path):
    calls = []

    def http_post(url, headers, body, timeout):
        calls.append((url, headers, body, timeout))
        return {}

    payload = run_nvidia_live_smoke(
        runtime_root=tmp_path / "runtime",
        env={"WABI_ALLOW_CLOUD_PROVIDERS": "0", "NVIDIA_API_KEY": "disabled-secret-value-1234567890"},
        http_post=http_post,
    )

    assert payload["live_smoke_status"] == "CLOUD_DISABLED_BY_FLAG"
    assert payload["cloud_allowed_mode"] == "EPHEMERAL_SINGLE_SMOKE"
    assert payload["cloud_provider_called"] is False
    assert payload["secret_values_printed"] is False
    assert calls == []


def test_live_smoke_not_configured_without_credential(tmp_path):
    calls = []

    def http_post(url, headers, body, timeout):
        calls.append((url, headers, body, timeout))
        return {}

    payload = run_nvidia_live_smoke(
        runtime_root=tmp_path / "runtime",
        env={"WABI_ALLOW_CLOUD_PROVIDERS": "1"},
        http_post=http_post,
    )

    assert payload["live_smoke_status"] == "NOT_CONFIGURED"
    assert payload["cloud_provider_called"] is False
    assert payload["secret_values_printed"] is False
    assert calls == []


def test_live_smoke_parses_success_json_with_mock(tmp_path):
    secret = "live-smoke-secret-value-1234567890"
    calls = []

    def http_post(url, headers, body, timeout):
        calls.append((url, headers, body, timeout))
        assert headers["Authorization"] == f"Bearer {secret}"
        assert body["model"] == PRIMARY_MODEL
        assert any(message["content"] == SMOKE_PROMPT for message in body["messages"])
        assert "C:\\Users" not in json.dumps(body)
        assert "BRAIN_OS" not in json.dumps(body)
        return {
            "choices": [
                {
                    "message": {
                        "content": '{"ok":true,"provider":"nvidia","smoke":"pass"}',
                    }
                }
            ]
        }

    payload = run_nvidia_live_smoke(
        runtime_root=tmp_path / "runtime",
        env={"WABI_ALLOW_CLOUD_PROVIDERS": "1", "NVIDIA_API_KEY": secret},
        http_post=http_post,
    )
    text = json.dumps(payload, ensure_ascii=False)

    assert payload["ok"] is True
    assert payload["live_smoke_status"] == "SMOKE_PASS"
    assert payload["cloud_allowed_mode"] == "EPHEMERAL_SINGLE_SMOKE"
    assert payload["provider_status"]["cloud_allowed_mode"] == "EPHEMERAL_SINGLE_SMOKE"
    assert payload["workspace_sent"] is False
    assert payload["cloud_provider_called"] is True
    assert payload["secret_values_printed"] is False
    assert secret not in text
    assert len(calls) == 1


def test_live_smoke_redacts_auth_error(tmp_path):
    secret = "auth-error-secret-value-1234567890"

    def http_post(url, headers, body, timeout):
        raise RuntimeError(f"cloud_http_401: invalid key {secret}")

    payload = run_nvidia_live_smoke(
        runtime_root=tmp_path / "runtime",
        env={"WABI_ALLOW_CLOUD_PROVIDERS": "1", "NVIDIA_API_KEY": secret},
        http_post=http_post,
    )
    text = json.dumps(payload, ensure_ascii=False)

    assert payload["live_smoke_status"] == "AUTH_REQUIRED_REDACTED"
    assert payload["cloud_provider_called"] is True
    assert payload["secret_values_printed"] is False
    assert secret not in text
    assert "REDACTED" in text


def test_live_smoke_redacts_provider_internal_ids(tmp_path):
    function_id = "84bf12ff" + "-edbd-4435-baea-" + "0fa6a7453d2e"
    account_id = "provider-account" + "-id-1234567890"
    error = f"cloud_http_404: Function '{function_id}': Not found for account '{account_id}'"

    def http_post(url, headers, body, timeout):
        raise RuntimeError(error)

    payload = run_nvidia_live_smoke(
        runtime_root=tmp_path / "runtime",
        env={"WABI_ALLOW_CLOUD_PROVIDERS": "1", "NVIDIA_API_KEY": "internal-id-secret-value-1234567890"},
        http_post=http_post,
    )
    text = json.dumps(payload, ensure_ascii=False)

    assert payload["live_smoke_status"] == "SMOKE_FAIL_REDACTED"
    assert function_id not in text
    assert account_id not in text
    assert "provider_function_id" in text
    assert "provider_account_id" in text


def test_no_secret_values_printed_in_provider_status(tmp_path):
    secret = "cli-status-secret-value-1234567890"
    env = {"WABI_ALLOW_CLOUD_PROVIDERS": "1", "NVIDIA_API_KEY": secret}
    payload = build_provider_status_contract(runtime_root=tmp_path / "runtime", env=env)

    assert payload["secret_values_printed"] is False
    assert secret not in json.dumps(payload, ensure_ascii=False)


def test_live_smoke_cli_skips_when_flag_disabled(tmp_path, monkeypatch):
    monkeypatch.setenv("WABI_ALLOW_CLOUD_PROVIDERS", "0")
    monkeypatch.setenv("NVIDIA_API_KEY", "cli-disabled-secret-value-1234567890")

    proc = run_cli("provider", "live-smoke", "--provider", "nvidia", "--json", workspace=tmp_path, runtime=tmp_path / "runtime")
    payload = json.loads(proc.stdout)

    assert proc.returncode == 0
    assert payload["live_smoke_status"] == "CLOUD_DISABLED_BY_FLAG"
    assert payload["cloud_provider_called"] is False
    assert payload["secret_values_printed"] is False
