import json
import os
import subprocess
import sys
from pathlib import Path

from wabi_sabi.core.build_assist_cloud import (
    build_assist_budget_status,
    build_assist_default_model_alias,
    build_build_assist_cloud_status,
    record_build_assist_usage,
    run_build_assist_nvidia_smoke,
)
from wabi_sabi.core.cloud_budget import CloudBudgetGate


APP_ROOT = Path(__file__).resolve().parents[1]


def run_cli(*args, workspace: Path, runtime: Path, env_overrides: dict[str, str] | None = None):
    env = os.environ.copy()
    env["PYTHONPATH"] = str(APP_ROOT)
    env.update(env_overrides or {})
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
        cwd=str(APP_ROOT),
        env=env,
        text=True,
        capture_output=True,
        timeout=30,
    )


def test_build_assist_status_is_local_first_and_secret_safe(tmp_path):
    status = build_build_assist_cloud_status(
        workspace=tmp_path,
        runtime_root=tmp_path / "runtime",
        env={"NVIDIA_API_KEY": "nvapi-test-secret-1234567890"},
    )
    text = json.dumps(status)

    assert status["schema"] == "wabi.build_assist_cloud.v0_1"
    assert status["enabled"] is False
    assert status["cloud_live_ready"] is False
    assert status["authority"]["cloud_authority"] == "proposal_only"
    assert status["authority"]["real_apply_allowed"] is False
    assert status["nvidia"]["default_model_alias"] == "nano-30b"
    assert status["nvidia"]["default_model"] == "nvidia/nemotron-3-nano-30b-a3b"
    assert status["cloud_budget"]["budget_gate"] == "CLOUD_BUDGET_DRY_RUN"
    assert "nvapi-test-secret" not in text


def test_build_assist_live_ready_requires_both_flags_and_key(tmp_path):
    status = build_build_assist_cloud_status(
        workspace=tmp_path,
        runtime_root=tmp_path / "runtime",
        env={
            "WABI_BUILD_ASSIST_CLOUD": "1",
            "WABI_ALLOW_CLOUD_PROVIDERS": "1",
            "NVIDIA_API_KEY": "nvapi-test-secret-1234567890",
        },
    )

    assert status["enabled"] is True
    assert status["cloud_flag_enabled"] is True
    assert status["cloud_live_ready"] is True
    assert status["action_gate"] == "REVIEW_CLOUD_LIVE_READY"
    assert status["cloud_budget"]["budget_gate"] == "CLOUD_BUDGET_READY"


def test_build_assist_default_model_alias_ignores_general_nvidia_alias(tmp_path):
    assert (
        build_assist_default_model_alias(
            {
                "WABI_NVIDIA_NIM_MODEL_ALIAS": "super",
            }
        )
        == "nano-30b"
    )
    assert (
        build_assist_default_model_alias(
            {
                "WABI_BUILD_ASSIST_NVIDIA_MODEL_ALIAS": "nano-9b",
                "WABI_NVIDIA_NIM_MODEL_ALIAS": "super",
            }
        )
        == "nano-9b"
    )


def test_build_assist_budget_counts_only_cloud_calls(tmp_path):
    runtime = tmp_path / "runtime"
    record_build_assist_usage(runtime_root=runtime, event={"cloud_provider_called": False, "provider": "dry-run"})
    record_build_assist_usage(runtime_root=runtime, event={"cloud_provider_called": True, "provider": "nvidia-nim:nano-30b"})

    budget = build_assist_budget_status(
        runtime_root=runtime,
        env={"WABI_BUILD_ASSIST_MAX_CLOUD_CALLS": "2"},
    )

    assert budget["max_cloud_calls"] == 2
    assert budget["recorded_cloud_calls"] == 1
    assert budget["remaining_cloud_calls"] == 1


def test_build_assist_status_cli(tmp_path):
    proc = run_cli("build-assist-status", "--json", workspace=tmp_path, runtime=tmp_path / "runtime")

    assert proc.returncode == 0, proc.stderr
    payload = json.loads(proc.stdout)
    assert payload["schema"] == "wabi.build_assist_cloud.v0_1"
    assert payload["cloud_live_ready"] is False
    assert payload["authority"]["auto_apply_from_cloud"] is False
    assert payload["nvidia"]["default_model_alias"] == "nano-30b"
    assert payload["cloud_budget"]["budget_gate"] == "CLOUD_BUDGET_DRY_RUN"


def test_build_assist_plan_defaults_to_dry_run_when_cloud_flags_are_absent(tmp_path):
    proc = run_cli(
        "build-assist-plan",
        "crear helper seguro",
        "--json",
        workspace=tmp_path,
        runtime=tmp_path / "runtime",
    )

    assert proc.returncode == 0, proc.stderr
    payload = json.loads(proc.stdout)
    assert payload["schema"] == "wabi.build_assist_plan.v0_1"
    assert payload["ok"] is True
    assert payload["provider"] == "dry-run"
    assert payload["provider_requested"] == "nano-30b"
    assert payload["cloud_provider_called"] is False
    assert payload["dry_run_forced_by_gate"] is True
    assert payload["cloud_budget"]["budget_gate"] == "CLOUD_BUDGET_DRY_RUN"
    assert not (tmp_path / "examples" / "wabi_cloud_proposal_generated.py").exists()


def test_build_assist_plan_accepts_nvidia_nano_alias_without_live_call(tmp_path):
    proc = run_cli(
        "build-assist-plan",
        "crear helper seguro",
        "--codex-provider",
        "nano-30b",
        "--json",
        workspace=tmp_path,
        runtime=tmp_path / "runtime",
    )

    assert proc.returncode == 0, proc.stderr
    payload = json.loads(proc.stdout)
    assert payload["ok"] is True
    assert payload["provider_requested"] == "nano-30b"
    assert payload["cloud_provider_called"] is False
    assert payload["dry_run_forced_by_gate"] is True


def test_build_assist_plan_blocks_when_cloud_budget_exceeded(tmp_path):
    runtime = tmp_path / "runtime"
    env = {
        "WABI_BUILD_ASSIST_CLOUD": "1",
        "WABI_ALLOW_CLOUD_PROVIDERS": "1",
        "WABI_CLOUD_MAX_CALLS_PER_SESSION": "1",
        "WABI_CLOUD_USAGE_DIR": str(runtime / "cloud_budget"),
        "WABI_SESSION_ID": "budget-test",
        "NVIDIA_API_KEY": "nvapi-test-secret-1234567890",
    }
    CloudBudgetGate(runtime_root=runtime, session_id="budget-test", env=env).record_planned_call(
        "nvidia",
        "nano-30b",
        "build_assist_plan",
    )

    proc = run_cli(
        "build-assist-plan",
        "crear helper seguro",
        "--codex-provider",
        "nano-30b",
        "--json",
        workspace=tmp_path,
        runtime=runtime,
        env_overrides=env,
    )

    assert proc.returncode == 2
    payload = json.loads(proc.stdout)
    assert payload["error"] == "CLOUD_BUDGET_EXCEEDED"
    assert payload["cloud_provider_called"] is False
    assert payload["cloud_budget"]["budget_gate"] == "CLOUD_BUDGET_EXCEEDED"


def test_build_assist_smoke_without_live_flag_does_not_call_provider(tmp_path):
    payload = run_build_assist_nvidia_smoke(
        workspace=tmp_path,
        runtime_root=tmp_path / "runtime",
        provider="nvidia",
        model_alias="nano-30b",
        live=False,
        env={"NVIDIA_API_KEY": "nvapi-test-secret-1234567890"},
    )

    assert payload["status"] == "REVIEW_LIVE_FLAG_REQUIRED"
    assert payload["cloud_provider_called"] is False
    assert payload["applied_to_sources"] is False
    assert payload["secrets_printed"] is False
    assert payload["redaction"] == "PASS"
    assert "nvapi-test-secret" not in json.dumps(payload)


def test_build_assist_smoke_with_one_flag_does_not_call_provider(tmp_path):
    payload = run_build_assist_nvidia_smoke(
        workspace=tmp_path,
        runtime_root=tmp_path / "runtime",
        provider="nvidia",
        model_alias="nano-30b",
        live=True,
        env={
            "WABI_BUILD_ASSIST_CLOUD": "1",
            "NVIDIA_API_KEY": "nvapi-test-secret-1234567890",
        },
    )

    assert payload["status"] == "REVIEW_CLOUD_PROVIDER_DISABLED"
    assert payload["cloud_provider_called"] is False
    assert payload["applied_to_sources"] is False
    assert payload["secrets_printed"] is False


def test_build_assist_smoke_with_mocked_provider_passes_proposal_only(tmp_path):
    calls = []

    def fake_post(url, headers, body, timeout):
        calls.append({"url": url, "headers": headers, "body": body, "timeout": timeout})
        return {
            "choices": [
                {
                    "message": {
                        "content": json.dumps(
                            {
                                "status": "WABI_PROVIDER_OK",
                                "provider": "nvidia",
                                "mode": "proposal_only",
                                "proposal": "Create a local helper plan and keep apply gated.",
                            }
                        )
                    }
                }
            ]
        }

    payload = run_build_assist_nvidia_smoke(
        workspace=tmp_path,
        runtime_root=tmp_path / "runtime",
        provider="nvidia",
        model_alias="nano-30b",
        live=True,
        env={
            "WABI_BUILD_ASSIST_CLOUD": "1",
            "WABI_ALLOW_CLOUD_PROVIDERS": "1",
            "NVIDIA_API_KEY": "nvapi-test-secret-1234567890",
        },
        http_post=fake_post,
    )

    assert payload["status"] == "LIVE_SMOKE_PASS"
    assert payload["provider"] == "nvidia"
    assert payload["model"] == "nvidia/nemotron-3-nano-30b-a3b"
    assert payload["mode"] == "proposal_only"
    assert payload["cloud_provider_called"] is True
    assert payload["applied_to_sources"] is False
    assert payload["secrets_printed"] is False
    assert payload["redaction"] == "PASS"
    assert payload["usage"] == {"input_tokens": None, "output_tokens": None}
    assert Path(payload["artifact_path"]).exists()
    assert calls[0]["body"]["model"] == "nvidia/nemotron-3-nano-30b-a3b"
    assert "nvapi-test-secret" not in json.dumps(payload)


def test_build_assist_smoke_provider_error_is_redacted(tmp_path):
    def fake_post(url, headers, body, timeout):
        raise RuntimeError("provider failed with nvapi-test-secret-1234567890")

    payload = run_build_assist_nvidia_smoke(
        workspace=tmp_path,
        runtime_root=tmp_path / "runtime",
        provider="nvidia",
        model_alias="nano-30b",
        live=True,
        env={
            "WABI_BUILD_ASSIST_CLOUD": "1",
            "WABI_ALLOW_CLOUD_PROVIDERS": "1",
            "NVIDIA_API_KEY": "nvapi-test-secret-1234567890",
        },
        http_post=fake_post,
    )

    assert payload["status"] == "REVIEW_NVIDIA_LIVE_SMOKE_FAILED"
    assert payload["cloud_provider_called"] is True
    assert payload["applied_to_sources"] is False
    assert payload["secrets_printed"] is False
    assert payload["redaction"] == "PASS"
    assert payload["error_class"] == "PROVIDER_ERROR_REDACTED"
    assert "nvapi-test-secret" not in json.dumps(payload)


def test_build_assist_smoke_cli_requires_live_flag(tmp_path):
    proc = run_cli(
        "build-assist-smoke",
        "--provider",
        "nvidia",
        "--model",
        "nano-30b",
        "--json",
        workspace=tmp_path,
        runtime=tmp_path / "runtime",
        env_overrides={"NVIDIA_API_KEY": "nvapi-test-secret-1234567890"},
    )

    assert proc.returncode == 2
    payload = json.loads(proc.stdout)
    assert payload["status"] == "REVIEW_LIVE_FLAG_REQUIRED"
    assert payload["cloud_provider_called"] is False
    assert payload["secrets_printed"] is False
