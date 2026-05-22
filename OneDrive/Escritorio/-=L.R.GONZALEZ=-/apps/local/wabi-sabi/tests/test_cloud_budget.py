import json
from pathlib import Path

from wabi_sabi.core.cloud_budget import CloudBudgetGate


def enabled_env(tmp_path: Path, **extra: str) -> dict[str, str]:
    env = {
        "WABI_BUILD_ASSIST_CLOUD": "1",
        "WABI_ALLOW_CLOUD_PROVIDERS": "1",
        "WABI_CLOUD_USAGE_DIR": str(tmp_path / "runtime" / "cloud_budget"),
    }
    env.update(extra)
    return env


def test_default_max_calls_per_session_is_three(tmp_path):
    gate = CloudBudgetGate(runtime_root=tmp_path / "runtime", env=enabled_env(tmp_path))

    limits = gate.get_limits()

    assert limits["max_calls_per_session"] == 3
    assert limits["max_calls_per_day"] == 10
    assert limits["mode"] == "strict"


def test_can_call_true_before_limit(tmp_path):
    gate = CloudBudgetGate(runtime_root=tmp_path / "runtime", env=enabled_env(tmp_path))

    decision = gate.can_call("nvidia", "nano-30b", "build_assist_plan")

    assert decision["budget_gate"] == "CLOUD_BUDGET_READY"
    assert decision["next_cloud_call_allowed"] is True
    assert decision["cloud_provider_called"] is False


def test_can_call_false_at_session_limit(tmp_path):
    gate = CloudBudgetGate(
        runtime_root=tmp_path / "runtime",
        env=enabled_env(tmp_path, WABI_CLOUD_MAX_CALLS_PER_SESSION="1"),
    )
    gate.record_planned_call("nvidia", "nano-30b", "build_assist_plan")

    decision = gate.can_call("nvidia", "nano-30b", "build_assist_plan")

    assert decision["budget_gate"] == "CLOUD_BUDGET_EXCEEDED"
    assert decision["next_cloud_call_allowed"] is False


def test_record_completed_call_increments_counter(tmp_path):
    gate = CloudBudgetGate(runtime_root=tmp_path / "runtime", env=enabled_env(tmp_path))

    gate.record_completed_call("nvidia", "nano-30b", {"status": "LIVE_SMOKE_PASS", "usage": {"input_tokens": 3}})
    usage = gate.get_usage()

    assert usage["calls_completed"] == 1
    assert usage["session_calls_used"] == 1
    assert gate.load_state()["usage_known"] is True


def test_without_double_opt_in_is_dry_run_and_does_not_increment_completed(tmp_path):
    gate = CloudBudgetGate(
        runtime_root=tmp_path / "runtime",
        env={"WABI_CLOUD_USAGE_DIR": str(tmp_path / "runtime" / "cloud_budget")},
    )

    decision = gate.can_call("nvidia", "nano-30b", "build_assist_plan")
    usage = gate.get_usage()

    assert decision["budget_gate"] == "CLOUD_BUDGET_DRY_RUN"
    assert decision["next_cloud_call_allowed"] is False
    assert usage["calls_completed"] == 0


def test_no_full_prompt_is_persisted(tmp_path):
    secretish_prompt = "programa un helper con contenido privado muy largo que no debe quedar completo"
    gate = CloudBudgetGate(runtime_root=tmp_path / "runtime", env=enabled_env(tmp_path))

    gate.record_planned_call("nvidia", "nano-30b", secretish_prompt)
    state_path = Path(gate.get_usage()["state_path"])
    text = state_path.read_text(encoding="utf-8")
    payload = json.loads(text)

    assert secretish_prompt not in text
    assert payload["last_intent_label"] == "redacted_user_intent"
    assert "last_intent_hash" in payload


def test_error_provider_result_is_recorded_without_secret_value(tmp_path):
    gate = CloudBudgetGate(runtime_root=tmp_path / "runtime", env=enabled_env(tmp_path, NVIDIA_API_KEY="nvapi-test-secret-1234567890"))

    gate.record_completed_call(
        "nvidia",
        "nano-30b",
        {"ok": False, "status": "REVIEW_NVIDIA_LIVE_SMOKE_FAILED", "error": "nvapi-test-secret-1234567890"},
    )
    text = Path(gate.get_usage()["state_path"]).read_text(encoding="utf-8")

    assert "nvapi-test-secret" not in text
    assert gate.get_usage()["calls_failed"] == 1
