import json

from wabi_sabi.core.cloud_budget import CloudBudgetGate
from wabi_sabi.core.llm_proposal import build_llm_proposal_status, request_llm_proposal


def _valid_provider_response(*_args, **_kwargs):
    proposal = {
        "schema": "wabi.cloud_code_proposal.v0_1",
        "summary": "mock provider proposal",
        "intent": "mock-intent",
        "assumptions": ["mocked provider response"],
        "files_to_read": [],
        "changes": [
            {
                "operation": "write_text",
                "target": "examples/mock_llm_generated.py",
                "suffix": ".py",
                "content": "def status():\n    return 'ok'\n",
            }
        ],
        "commands_requested": ["python -m py_compile examples/mock_llm_generated.py"],
        "test_commands": ["python -m py_compile examples/mock_llm_generated.py"],
        "risks": ["proposal-only"],
        "rollback_notes": ["local rollback required before apply"],
        "debug_strategy": ["run py_compile"],
        "gate_recommendation": "REVIEW",
    }
    return {"choices": [{"message": {"content": json.dumps(proposal)}}]}


def test_llm_proposal_default_disabled_is_safe_dry_run(tmp_path, monkeypatch):
    monkeypatch.delenv("WABI_LLM_PROVIDER_CLOUD_DEFAULT", raising=False)
    monkeypatch.delenv("WABI_BUILD_ASSIST_CLOUD", raising=False)
    monkeypatch.delenv("WABI_ALLOW_CLOUD_PROVIDERS", raising=False)
    monkeypatch.setenv("WABI_CLOUD_USAGE_DIR", str(tmp_path / "runtime" / "cloud_budget"))

    payload = request_llm_proposal(
        workspace=tmp_path,
        runtime_root=tmp_path / "runtime",
        user_text="programa un helper seguro",
        intent_name="code_request",
    )

    assert payload["status"] == "LLM_PROPOSAL_DEFAULT_DISABLED"
    assert payload["proposal_only"] is True
    assert payload["cloud_provider_called"] is False
    assert payload["applied_to_sources"] is False
    assert payload["proposal_artifact"]


def test_llm_cloud_default_without_double_opt_in_does_not_call_provider(tmp_path, monkeypatch):
    monkeypatch.setenv("WABI_LLM_PROVIDER_CLOUD_DEFAULT", "1")
    monkeypatch.delenv("WABI_BUILD_ASSIST_CLOUD", raising=False)
    monkeypatch.delenv("WABI_ALLOW_CLOUD_PROVIDERS", raising=False)
    monkeypatch.setenv("NVIDIA_API_KEY", "nvapi-test-secret-value")
    monkeypatch.setenv("WABI_CLOUD_USAGE_DIR", str(tmp_path / "runtime" / "cloud_budget"))

    payload = request_llm_proposal(
        workspace=tmp_path,
        runtime_root=tmp_path / "runtime",
        user_text="programa un helper seguro",
        intent_name="code_request",
        http_post=_valid_provider_response,
    )
    encoded = json.dumps(payload, ensure_ascii=False)

    assert payload["status"] == "CLOUD_BUDGET_DRY_RUN"
    assert payload["cloud_provider_called"] is False
    assert payload["cloud_budget"]["budget_gate"] == "CLOUD_BUDGET_DRY_RUN"
    assert "nvapi-test-secret-value" not in encoded


def test_llm_cloud_default_with_mock_provider_creates_proposal_only_task(tmp_path, monkeypatch):
    monkeypatch.setenv("WABI_LLM_PROVIDER_CLOUD_DEFAULT", "1")
    monkeypatch.setenv("WABI_BUILD_ASSIST_CLOUD", "1")
    monkeypatch.setenv("WABI_ALLOW_CLOUD_PROVIDERS", "1")
    monkeypatch.setenv("NVIDIA_API_KEY", "nvapi-test-secret-value")
    monkeypatch.setenv("WABI_CLOUD_USAGE_DIR", str(tmp_path / "runtime" / "cloud_budget"))

    payload = request_llm_proposal(
        workspace=tmp_path,
        runtime_root=tmp_path / "runtime",
        user_text="programa un helper seguro para validar json",
        intent_name="code_request",
        session_id="mock-live",
        http_post=_valid_provider_response,
    )
    encoded = json.dumps(payload, ensure_ascii=False)

    assert payload["status"] == "LLM_PROPOSAL_READY"
    assert payload["cloud_provider_called"] is True
    assert payload["applied_to_sources"] is False
    assert payload["task_spec"]["metadata"]["cloud_authority"] == "proposal_only"
    assert payload["proposal_artifact"]
    assert payload["task_spec_artifact"]
    assert "nvapi-test-secret-value" not in encoded


def test_llm_budget_exceeded_blocks_provider_call(tmp_path, monkeypatch):
    monkeypatch.setenv("WABI_LLM_PROVIDER_CLOUD_DEFAULT", "1")
    monkeypatch.setenv("WABI_BUILD_ASSIST_CLOUD", "1")
    monkeypatch.setenv("WABI_ALLOW_CLOUD_PROVIDERS", "1")
    monkeypatch.setenv("WABI_CLOUD_MAX_CALLS_PER_SESSION", "1")
    monkeypatch.setenv("NVIDIA_API_KEY", "nvapi-test-secret-value")
    monkeypatch.setenv("WABI_CLOUD_USAGE_DIR", str(tmp_path / "runtime" / "cloud_budget"))
    CloudBudgetGate(runtime_root=tmp_path / "runtime", session_id="limited").record_planned_call(
        "nvidia",
        "nano-30b",
        "llm_proposal:code_request",
    )

    payload = request_llm_proposal(
        workspace=tmp_path,
        runtime_root=tmp_path / "runtime",
        user_text="programa otro helper",
        intent_name="code_request",
        session_id="limited",
        http_post=_valid_provider_response,
    )

    assert payload["status"] == "LLM_PROPOSAL_BUDGET_EXCEEDED"
    assert payload["cloud_provider_called"] is False
    assert payload["cloud_budget"]["budget_gate"] == "CLOUD_BUDGET_EXCEEDED"


def test_llm_status_reports_cloud_default_flag(tmp_path, monkeypatch):
    monkeypatch.setenv("WABI_LLM_PROVIDER_CLOUD_DEFAULT", "1")
    monkeypatch.setenv("WABI_CLOUD_USAGE_DIR", str(tmp_path / "runtime" / "cloud_budget"))

    status = build_llm_proposal_status(runtime_root=tmp_path / "runtime")

    assert status["llm_cloud_default_enabled"] is True
    assert status["proposal_only"] is True
    assert status["cloud_provider_called"] is False
