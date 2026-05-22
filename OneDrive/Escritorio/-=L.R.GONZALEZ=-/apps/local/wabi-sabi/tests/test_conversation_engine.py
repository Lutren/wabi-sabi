import json

from wabi_sabi.core.conversation_engine import ConversationEngine, ConversationEngineOptions, classify_intent
from wabi_sabi.core.cloud_budget import CloudBudgetGate


def test_classify_required_intents():
    assert classify_intent("hola wabi").intent_name == "chat_general"
    assert classify_intent("programa un helper seguro para validar json").intent_name == "code_request"
    assert classify_intent("crea una escena de DUAT city con nodos de agentes").intent_name == "graphics_scene_request"
    assert classify_intent("debuggea el build assist").intent_name == "debug_request"
    assert classify_intent("usa nvidia para planear este cambio").intent_name == "build_assist_request"
    assert classify_intent("formula una hipotesis con contraejemplo para el motor").intent_name == "hypothesis_request"


def test_code_request_creates_task_spec_but_does_not_apply(tmp_path):
    engine = ConversationEngine(workspace=tmp_path, runtime_root=tmp_path / "runtime")

    payload = engine.handle_turn("programa un helper seguro para validar json")

    assert payload["ok"] is True
    assert payload["intent_name"] == "code_request"
    assert payload["proposal_only"] is True
    assert payload["applied_to_sources"] is False
    task = payload["payload"]["task_spec"]
    assert task["needs_file_write"] is True
    assert task["applied_to_sources"] is False
    assert task["rollback_required"] is True
    assert task["affected_paths"] == ["wabi_sabi/core/json_safety.py", "tests/test_json_safety.py"]
    assert [change["target"] for change in task["changes"]] == ["wabi_sabi/core/json_safety.py", "tests/test_json_safety.py"]
    assert task["suggested_tests"] == [
        "python -B -m pytest tests/test_json_safety.py -q -p no:cacheprovider",
        "python -B -m py_compile wabi_sabi/core/json_safety.py",
    ]
    assert task["proposal_only"] is True
    assert payload["artifacts"]
    assert not list(tmp_path.glob("*.py"))


def test_graphics_scene_request_calls_bridge_in_plan_mode(tmp_path):
    engine = ConversationEngine(workspace=tmp_path, runtime_root=tmp_path / "runtime")

    payload = engine.handle_turn("crea una escena de DUAT city con agentes y handoff")

    assert payload["ok"] is True
    assert payload["intent_name"] == "graphics_scene_request"
    assert payload["payload"]["graphics_status"]["graphics_live"] is False
    assert payload["payload"]["graphics_status"]["graphics_plan_ready"] is True
    assert payload["payload"]["graphics_plan"]["publication_allowed"] is False
    assert payload["cloud_provider_called"] is False
    assert payload["artifacts"]


def test_cloud_request_without_flags_stays_dry_run_proposal_only(tmp_path, monkeypatch):
    monkeypatch.delenv("WABI_BUILD_ASSIST_CLOUD", raising=False)
    monkeypatch.delenv("WABI_ALLOW_CLOUD_PROVIDERS", raising=False)
    engine = ConversationEngine(workspace=tmp_path, runtime_root=tmp_path / "runtime")

    payload = engine.handle_turn("usa nvidia para planear este cambio")

    assert payload["ok"] is True
    assert payload["intent_name"] == "build_assist_request"
    assert payload["cloud_provider_called"] is False
    assert payload["applied_to_sources"] is False
    assert payload["payload"]["build_assist"]["cloud_live_ready"] is False
    assert payload["payload"]["build_assist"]["authority"]["cloud_authority"] == "proposal_only"
    assert payload["payload"]["cloud_budget"]["budget_gate"] == "CLOUD_BUDGET_DRY_RUN"


def test_cloud_request_with_flags_reports_ready_without_apply_or_provider_call(tmp_path, monkeypatch):
    monkeypatch.setenv("WABI_BUILD_ASSIST_CLOUD", "1")
    monkeypatch.setenv("WABI_ALLOW_CLOUD_PROVIDERS", "1")
    monkeypatch.setenv("NVIDIA_API_KEY", "nvapi-test-secret-1234567890")
    engine = ConversationEngine(workspace=tmp_path, runtime_root=tmp_path / "runtime")

    payload = engine.handle_turn("usa nvidia para planear este cambio")
    text = json.dumps(payload)

    assert payload["ok"] is True
    assert payload["payload"]["build_assist"]["cloud_live_ready"] is True
    assert payload["payload"]["task_spec"]["cloud_authority"] == "proposal_only"
    assert payload["payload"]["cloud_budget"]["budget_gate"] == "CLOUD_BUDGET_READY"
    assert payload["cloud_provider_called"] is False
    assert payload["applied_to_sources"] is False
    assert "nvapi-test-secret" not in text


def test_cloud_request_with_budget_exceeded_does_not_call_provider(tmp_path, monkeypatch):
    monkeypatch.setenv("WABI_BUILD_ASSIST_CLOUD", "1")
    monkeypatch.setenv("WABI_ALLOW_CLOUD_PROVIDERS", "1")
    monkeypatch.setenv("WABI_CLOUD_MAX_CALLS_PER_SESSION", "1")
    monkeypatch.setenv("WABI_CLOUD_USAGE_DIR", str(tmp_path / "runtime" / "cloud_budget"))
    engine = ConversationEngine(workspace=tmp_path, runtime_root=tmp_path / "runtime")
    engine.state.session_id = "budget-test"
    CloudBudgetGate(
        runtime_root=tmp_path / "runtime",
        session_id="budget-test",
    ).record_planned_call("nvidia", "nano-30b", "build_assist_plan")

    payload = engine.handle_turn("usa nvidia para planear otro cambio")

    assert payload["payload"]["cloud_budget"]["budget_gate"] == "CLOUD_BUDGET_EXCEEDED"
    assert payload["cloud_provider_called"] is False
    assert payload["applied_to_sources"] is False


def test_llm_cloud_default_attaches_dry_run_proposal_without_double_opt_in(tmp_path, monkeypatch):
    monkeypatch.setenv("WABI_LLM_PROVIDER_CLOUD_DEFAULT", "1")
    monkeypatch.delenv("WABI_BUILD_ASSIST_CLOUD", raising=False)
    monkeypatch.delenv("WABI_ALLOW_CLOUD_PROVIDERS", raising=False)
    monkeypatch.setenv("WABI_CLOUD_USAGE_DIR", str(tmp_path / "runtime" / "cloud_budget"))
    engine = ConversationEngine(workspace=tmp_path, runtime_root=tmp_path / "runtime")

    payload = engine.handle_turn("programa un helper seguro para validar json")
    proposal = payload["payload"]["llm_proposal"]

    assert payload["intent_name"] == "code_request"
    assert proposal["status"] == "CLOUD_BUDGET_DRY_RUN"
    assert proposal["proposal_only"] is True
    assert payload["cloud_provider_called"] is False
    assert payload["applied_to_sources"] is False


def test_status_and_providers_include_cloud_budget(tmp_path):
    engine = ConversationEngine(workspace=tmp_path, runtime_root=tmp_path / "runtime")

    status = engine.handle_turn("/status")
    providers = engine.handle_turn("/providers")

    assert "cloud_budget:" in status["output"]
    assert "budget_gate:" in status["output"]
    assert status["payload"]["cloud_budget"]["budget_gate"] == "CLOUD_BUDGET_DRY_RUN"
    assert "cloud_budget:" in providers["output"]


def test_unsafe_external_request_is_blocked(tmp_path):
    engine = ConversationEngine(workspace=tmp_path, runtime_root=tmp_path / "runtime")

    payload = engine.handle_turn("haz deploy y publica todo")

    assert payload["ok"] is False
    assert payload["intent_name"] == "unsafe_or_external_request"
    assert payload["gate"] == "BLOCK"
    assert payload["applied_to_sources"] is False


def test_hypothesis_request_creates_packet_without_apply_or_cloud(tmp_path):
    engine = ConversationEngine(workspace=tmp_path, runtime_root=tmp_path / "runtime")

    payload = engine.handle_turn("formula una hipotesis con contraejemplo para el motor")

    assert payload["ok"] is True
    assert payload["intent_name"] == "hypothesis_request"
    assert payload["route"] == "hypothesis_plan"
    assert payload["cloud_provider_called"] is False
    assert payload["applied_to_sources"] is False
    assert payload["payload"]["hypothesis_packet"]["falsifiers"]
    assert payload["payload"]["task_spec"]["intent_name"] == "hypothesis_request"
    assert payload["artifacts"]


def test_ui_style_options_do_not_persist_full_prompts_or_artifacts(tmp_path):
    runtime_root = tmp_path / "runtime"
    engine = ConversationEngine(
        workspace=tmp_path,
        runtime_root=runtime_root,
        options=ConversationEngineOptions(
            persist_turns=False,
            include_prompt_in_turn=False,
            write_artifacts=False,
        ),
    )

    payload = engine.handle_turn("programa un helper seguro para validar json")
    encoded_files = [path.read_text(encoding="utf-8", errors="ignore") for path in runtime_root.rglob("*") if path.is_file()]

    assert "prompt" not in payload
    assert payload["artifacts"] == []
    assert all("programa un helper seguro para validar json" not in text for text in encoded_files)
