from __future__ import annotations

import json
from pathlib import Path

from wabi_sabi.core.taskspec_review import (
    build_gate_preview,
    block_apply_attempt,
    block_apply_with_preview,
    evaluate_apply_readiness,
    list_required_gates,
    normalize_taskspec_for_review,
    redact_taskspec,
    save_taskspec_draft,
)


def test_normalize_taskspec_for_review_core_fields():
    review = normalize_taskspec_for_review(
        {
            "schema": "wabi.conversation_task_spec.v0_1",
            "intent_name": "code_request",
            "title": "Prepare code proposal",
            "description": "programa un helper seguro para validar json",
            "action_gate": "APPROVE",
            "proposal_only": True,
            "needs_file_write": True,
            "suggested_tests": ["python -B -m pytest -q"],
            "safe_next_steps": ["Review patch plan", "Run tests"],
        },
        intent={"intent_name": "code_request", "action_gate": "APPROVE"},
        route="code_plan",
    )

    assert review["schema"] == "wabi.taskspec_review.v0_1"
    assert review["task_id"].startswith("taskspec-")
    assert review["intent_name"] == "code_request"
    assert review["route"] == "code_plan"
    assert review["action_gate"] == "APPROVE"
    assert review["proposal_only"] is True
    assert review["needs_file_write"] is True
    assert review["applied_to_sources"] is False
    assert review["cloud_provider_called"] is False
    assert review["suggested_tests"] == ["python -B -m pytest -q"]
    assert review["rollback_required"] is True


def test_normalize_taskspec_for_review_summarizes_multi_file_changes():
    review = normalize_taskspec_for_review(
        {
            "intent_name": "code_request",
            "action_gate": "APPROVE",
            "proposal_only": True,
            "needs_file_write": True,
            "changes": [
                {"target": "wabi_sabi/core/example.py", "content": "VALUE = 1\n"},
                {"target": "tests/test_example.py", "content": "def test_value():\n    assert True\n"},
            ],
            "suggested_tests": ["python -B -m pytest tests/test_example.py -q"],
            "rollback_required": True,
            "next_action": "Run Apply Local Preview.",
        }
    )
    encoded = json.dumps(review, ensure_ascii=False)

    assert review["changes_count"] == 2
    assert review["affected_paths"] == ["wabi_sabi/core/example.py", "tests/test_example.py"]
    assert review["suggested_tests"] == ["python -B -m pytest tests/test_example.py -q"]
    assert review["rollback_required"] is True
    assert review["next_action"] == "Run Apply Local Preview."
    assert "VALUE = 1" not in encoded


def test_redact_taskspec_removes_prompt_like_fields(monkeypatch):
    monkeypatch.setenv("NVIDIA_API_KEY", "nvapi-test-secret-1234567890")
    redacted = redact_taskspec(
        {
            "prompt": "usa este secreto nvapi-test-secret-1234567890 para programar",
            "description": "programa un helper seguro para validar json",
            "content": "source completo no debe guardarse",
            "target_files": ["src/helper.py"],
        }
    )
    encoded = json.dumps(redacted, ensure_ascii=False)

    assert "usa este secreto" not in encoded
    assert "programa un helper seguro" not in encoded
    assert "source completo" not in encoded
    assert "nvapi-test-secret" not in encoded
    assert "prompt_sha256" in redacted
    assert redacted["target_files"] == ["src/helper.py"]


def test_save_taskspec_draft_is_redacted(tmp_path, monkeypatch):
    monkeypatch.setenv("NVIDIA_API_KEY", "nvapi-test-secret-1234567890")
    result = save_taskspec_draft(
        {
            "intent_name": "build_assist_request",
            "title": "Prepare NVIDIA proposal-only assist",
            "description": "usa nvidia para planear este cambio con nvapi-test-secret-1234567890",
            "action_gate": "REVIEW",
            "proposal_only": True,
            "needs_cloud": True,
        },
        runtime_root=tmp_path / "runtime",
    )
    path = Path(result["draft_path"])
    text = path.read_text(encoding="utf-8")

    assert result["status"] == "SAVED"
    assert result["applied_to_sources"] is False
    assert result["saved_prompt_complete"] is False
    assert "usa nvidia para planear" not in text
    assert "nvapi-test-secret" not in text


def test_block_apply_attempt_is_always_blocked():
    result = block_apply_attempt({"intent_name": "code_request", "action_gate": "APPROVE"})

    assert result["status"] == "BLOCKED"
    assert result["reason"] == "APPLY_BLOCKED_REVIEW_ONLY_V0_1"
    assert result["applied_to_sources"] is False
    assert result["cloud_provider_called"] is False
    assert result["publication_gate"] == "BLOCK"
    assert result["gate_preview"]["reason"] == "APPLY_NOT_AVAILABLE_REVIEW_ONLY_V0_1"


def test_gate_preview_lists_required_future_gates():
    preview = build_gate_preview(
        {
            "intent_name": "code_request",
            "action_gate": "APPROVE",
            "proposal_only": True,
            "needs_file_write": True,
            "target_files": ["src/helper.py"],
            "suggested_tests": ["python -B -m pytest tests/test_helper.py -q"],
        }
    )
    gate_names = {item["name"] for item in preview["required_gates"]}

    assert preview["apply_status"] == "BLOCKED"
    assert preview["reason"] == "APPLY_NOT_AVAILABLE_REVIEW_ONLY_V0_1"
    assert {"ActionGate", "GhostGate", "RollbackStore", "TestRunner"} <= gate_names
    assert preview["applied_to_sources"] is False
    assert preview["cloud_provider_called"] is False
    assert preview["graphics_live"] is False
    assert preview["rollback_required"] is True


def test_gate_preview_cloud_and_graphics_remain_proposal_plan_only():
    preview = build_gate_preview(
        {
            "intent_name": "build_assist_request",
            "needs_cloud": True,
            "needs_graphics": True,
            "proposal_only": True,
            "action_gate": "REVIEW",
        }
    )

    assert preview["cloud"]["proposal_only"] is True
    assert preview["cloud"]["provider_called"] is False
    assert preview["graphics"]["plan_only"] is True
    assert preview["graphics"]["graphics_live"] is False
    assert "CloudBudgetGate" in {item["name"] for item in preview["required_gates"]}
    assert "GraphicsPlanGate" in {item["name"] for item in preview["required_gates"]}


def test_evaluate_apply_readiness_is_never_ready_in_v0_1():
    readiness = evaluate_apply_readiness({"intent_name": "code_request", "action_gate": "APPROVE"})

    assert readiness["apply_ready"] is False
    assert readiness["reason"] == "APPLY_NOT_AVAILABLE_REVIEW_ONLY_V0_1"
    assert "explicit_human_apply_gate" in readiness["missing"]


def test_block_apply_with_preview_uses_not_available_reason():
    result = block_apply_with_preview({"intent_name": "code_request", "action_gate": "APPROVE"})

    assert result["status"] == "BLOCKED"
    assert result["reason"] == "APPLY_NOT_AVAILABLE_REVIEW_ONLY_V0_1"
    assert result["applied_to_sources"] is False
    assert result["gate_preview"]["apply_status"] == "BLOCKED"


def test_list_required_gates_is_stable_minimum():
    names = {item["name"] for item in list_required_gates({"intent_name": "code_request"})}

    assert {"ActionGate", "GhostGate", "RollbackStore", "TestRunner"} <= names
