import json

from wabi_sabi.core.llm_work_response import build_safe_llm_work_response


def test_safe_llm_work_response_has_required_contract(tmp_path, monkeypatch):
    monkeypatch.setenv("NVIDIA_API_KEY", "nvapi-test-secret-value")
    payload = build_safe_llm_work_response(
        {
            "ok": True,
            "route": "code_plan",
            "intent_name": "code_request",
            "intent": {"intent_name": "code_request", "action_gate": "REVIEW"},
            "response": "Prepare a helper.",
            "task_spec": {
                "task_id": "task-safe-json",
                "intent_name": "code_request",
                "summary": "Create safe JSON helper.",
                "affected_paths": ["wabi_sabi/core/json_safety.py"],
                "suggested_tests": ["python -B -m pytest tests/test_json_safety.py -q"],
                "rollback_required": True,
                "next_action": "Review TaskSpec / Preview Apply Local",
            },
            "llm_proposal": {"status": "CLOUD_BUDGET_DRY_RUN", "cloud_provider_called": False},
            "cloud_provider_called": False,
            "applied_to_sources": False,
        },
        runtime_root=tmp_path / "runtime",
        source="test",
    )
    encoded = json.dumps(payload, ensure_ascii=False)

    assert payload["status"] == "OK"
    assert payload["intent_name"] == "code_request"
    assert payload["route"] == "code_plan"
    assert payload["proposal"]
    assert payload["task_spec"]["task_id"] == "task-safe-json"
    assert payload["cloud_provider_called"] is False
    assert payload["applied_to_sources"] is False
    assert payload["rollback_snapshot_required"] is True
    assert payload["next_safe_action"] == "Review TaskSpec / Preview Apply Local"
    assert "Proposal-only; Apply Local blocked" in payload["warnings"][0]
    assert "proposal_only" in payload["tags"]
    assert "vibe_coding" in payload["tags"]
    assert "double_opt_in_required" in payload["tags"]
    assert "LLM_proposal" in payload["tags"]
    assert payload["metadata"]["category"] == "code"
    assert payload["metadata"]["interface_mode"] == "vibe_coding"
    assert payload["metadata"]["incremental"] is True
    assert payload["metadata"]["workflow"] == [
        "chat",
        "llm_proposal",
        "taskspec_review",
        "gate_preview",
        "apply_local_preview",
        "explicit_apply_local",
    ]
    assert payload["metadata"]["fallback_mode"] == "local_rules_task_spec"
    assert payload["metadata"]["apply_simulation"]["available"] is True
    assert payload["runtime_json"]
    assert payload["witness"]["verified"] is True
    assert "nvapi-test-secret-value" not in encoded


def test_safe_llm_work_response_graphics_plan_stays_plan_only(tmp_path):
    payload = build_safe_llm_work_response(
        {
            "ok": True,
            "route": "graphics_plan",
            "intent_name": "graphics_scene_request",
            "intent": {"intent_name": "graphics_scene_request", "action_gate": "REVIEW"},
            "graphics": {
                "graphics_live": False,
                "graphics_plan_ready": True,
                "plan": {"summary": "DUAT city scene plan", "scene": "agents and handoff nodes"},
            },
            "task_spec": {"intent_name": "graphics_scene_request", "summary": "Create DUAT scene plan."},
            "cloud_provider_called": False,
        },
        runtime_root=tmp_path / "runtime",
        persist=False,
    )

    assert payload["graphics_plan"]["graphics_live"] is False
    assert payload["graphics_plan"]["graphics_plan_ready"] is True
    assert payload["graphics_plan"]["plan_mode"] is True
    assert payload["applied_to_sources"] is False
    assert "GraphicsBridge plan-only; graphics_live=false." in payload["warnings"]
    assert "duat_graphics_plan" in payload["tags"]
    assert "vibe_coding" in payload["tags"]
    assert "graphics_live_false" in payload["tags"]
    assert payload["metadata"]["category"] == "duat_graphics"
    assert payload["metadata"]["asset_audit_required"] is True
    assert payload["metadata"]["duat_graphics_plan_only"] is True


def test_safe_llm_work_response_artifact_does_not_store_prompt(tmp_path):
    payload = build_safe_llm_work_response(
        {
            "ok": True,
            "route": "code_plan",
            "intent_name": "code_request",
            "prompt": "programa un helper seguro para validar json con este prompt privado completo",
            "task_spec": {"summary": "Safe helper", "affected_paths": []},
            "cloud_provider_called": False,
        },
        runtime_root=tmp_path / "runtime",
    )

    artifact_text = open(payload["runtime_json"], encoding="utf-8").read()
    assert "prompt privado completo" not in artifact_text
    assert payload["prompts_stored"] is False


def test_safe_llm_work_response_marks_hypothesis_mode(tmp_path):
    payload = build_safe_llm_work_response(
        {
            "ok": True,
            "route": "hypothesis_plan",
            "intent_name": "hypothesis_request",
            "task_spec": {
                "intent_name": "hypothesis_request",
                "summary": "Run local counterexample search.",
                "falsifiers": ["Fails without local evidence."],
                "suggested_tests": ["python -B -m pytest tests/test_hypothesis_packet.py -q"],
            },
            "cloud_provider_called": False,
        },
        runtime_root=tmp_path / "runtime",
        persist=False,
    )

    assert payload["route"] == "hypothesis_plan"
    assert payload["metadata"]["category"] == "hypothesis"
    assert payload["metadata"]["hypothesis_packet"] is True
    assert payload["metadata"]["counterexample_search"] is True
    assert "hypothesis_packet" in payload["tags"]
    assert "counterexample_search" in payload["tags"]
