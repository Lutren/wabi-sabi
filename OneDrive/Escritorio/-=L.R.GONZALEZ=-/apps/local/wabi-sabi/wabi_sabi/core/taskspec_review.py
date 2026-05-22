from __future__ import annotations

import hashlib
import json
import time
from pathlib import Path
from typing import Any, Mapping

from wabi_sabi.core.redaction import redact_mapping, redact_text
from wabi_sabi.core.tools import write_artifact


TASKSPEC_REVIEW_SCHEMA = "wabi.taskspec_review.v0_1"
TASKSPEC_APPLY_BLOCK_SCHEMA = "wabi.taskspec_review.apply_block.v0_1"
TASKSPEC_GATE_PREVIEW_SCHEMA = "wabi.taskspec_gate_preview.v0_1"
PRIVATE_TEXT_KEYS = {
    "prompt",
    "message",
    "user_text",
    "input",
    "raw_input",
    "description",
    "injected_prompt",
    "content",
    "proposedContent",
    "old",
    "new",
}


def normalize_taskspec_for_review(
    task_spec: Mapping[str, Any] | None,
    *,
    intent: Mapping[str, Any] | None = None,
    route: str | None = None,
    cloud_budget: Mapping[str, Any] | None = None,
    graphics: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    source = redact_taskspec(task_spec or {})
    intent_data = dict(intent or {})
    graphics_data = dict(graphics or {})
    budget_data = dict(cloud_budget or {})
    intent_name = str(source.get("intent_name") or intent_data.get("intent_name") or "chat_general")
    action_gate = str(source.get("action_gate") or intent_data.get("action_gate") or "REVIEW")
    review = {
        "schema": TASKSPEC_REVIEW_SCHEMA,
        "task_id": "",
        "fingerprint": "",
        "intent_name": intent_name,
        "route": route or _route_for_intent(intent_name),
        "action_gate": action_gate,
        "proposal_only": _bool(source.get("proposal_only"), True),
        "needs_cloud": _bool(source.get("needs_cloud") or intent_data.get("needs_cloud"), False),
        "needs_graphics": _bool(source.get("needs_graphics") or intent_data.get("needs_graphics"), False),
        "needs_file_write": _bool(source.get("needs_file_write") or intent_data.get("needs_file_write"), False),
        "applied_to_sources": False,
        "cloud_provider_called": False,
        "graphics_live": _bool(graphics_data.get("graphics_live"), False),
        "summary": _summary(source, intent_name),
        "plan_steps": _list_field(source, ("safe_next_steps", "steps", "planned_changes")),
        "risks": _risks_for(source, intent_name),
        "assumptions": _assumptions_for(source, budget_data, graphics_data),
        "suggested_tests": _list_field(source, ("suggested_tests", "test_plan", "test_commands")),
        "affected_paths": _affected_paths(source),
        "changes_count": _changes_count(source),
        "rollback_required": _bool(source.get("rollback_required"), True),
        "next_action": _next_action_for(source, action_gate),
        "gate_status": _gate_status(action_gate),
        "budget_gate": str(budget_data.get("budget_gate") or "CLOUD_BUDGET_DRY_RUN"),
        "raw_schema": str(source.get("schema") or ""),
    }
    fingerprint = _fingerprint(review)
    review["fingerprint"] = fingerprint
    review["task_id"] = f"taskspec-{fingerprint[:12]}"
    return redact_mapping(review)


def redact_taskspec(task_spec: Mapping[str, Any] | None) -> dict[str, Any]:
    return _strip_private_text(redact_mapping(dict(task_spec or {})))


def save_taskspec_draft(
    task_spec: Mapping[str, Any] | None,
    *,
    runtime_root: str | Path | None = None,
) -> dict[str, Any]:
    review = normalize_taskspec_for_review(task_spec)
    root = Path(runtime_root) if runtime_root is not None else Path.home() / ".medioevo" / "wabi" / "runtime"
    path = write_artifact(
        root / "outputs" / "taskspec_review",
        "wabi_taskspec_review",
        ".json",
        json.dumps(review, indent=2, ensure_ascii=False) + "\n",
    )
    return {
        "status": "SAVED",
        "schema": "wabi.taskspec_review.save_draft.v0_1",
        "task_id": review["task_id"],
        "draft_path": str(path),
        "applied_to_sources": False,
        "cloud_provider_called": False,
        "secrets_printed": False,
        "saved_prompt_complete": False,
        "taskspec_review": review,
    }


def block_apply_attempt(task_spec: Mapping[str, Any] | None = None) -> dict[str, Any]:
    review = normalize_taskspec_for_review(task_spec or {})
    preview = build_gate_preview(review)
    return {
        "schema": TASKSPEC_APPLY_BLOCK_SCHEMA,
        "status": "BLOCKED",
        "reason": "APPLY_BLOCKED_REVIEW_ONLY_V0_1",
        "task_id": review["task_id"],
        "action_gate": "BLOCK",
        "applied_to_sources": False,
        "cloud_provider_called": False,
        "graphics_live": False,
        "publication_gate": "BLOCK",
        "taskspec_review": review,
        "gate_preview": preview,
    }


def build_gate_preview(task_spec: Mapping[str, Any] | None) -> dict[str, Any]:
    review = normalize_taskspec_for_review(task_spec or {})
    readiness = evaluate_apply_readiness(review)
    local_apply = _local_apply_readiness(review)
    local_ready = bool(local_apply.get("ready"))
    preview = {
        "schema": TASKSPEC_GATE_PREVIEW_SCHEMA,
        "status": "OK",
        "task_id": review["task_id"],
        "fingerprint": review["fingerprint"],
        "intent_name": review["intent_name"],
        "route": review["route"],
        "apply_status": "BLOCKED",
        "reason": "APPLY_NOT_AVAILABLE_REVIEW_ONLY_V0_1",
        "proposal_only": True,
        "applied_to_sources": False,
        "cloud_provider_called": False,
        "graphics_live": False,
        "required_gates": list_required_gates(review),
        "required_tests": list_required_tests(review),
        "affected_paths_preview": list(review.get("affected_paths") or []),
        "rollback": list_required_rollback(review),
        "rollback_required": True,
        "risks": list(review.get("risks") or []),
        "blockers": readiness["blockers"],
        "next_safe_action": (
            "Run Apply Local Preview; legacy Apply remains blocked."
            if local_ready
            else "Review and save redacted TaskSpec draft."
        ),
        "readiness": readiness,
        "local_apply": local_apply,
        "cloud": {
            "involved": bool(review.get("needs_cloud")),
            "proposal_only": True,
            "provider_called": False,
            "budget_gate": review.get("budget_gate", "CLOUD_BUDGET_DRY_RUN"),
        },
        "graphics": {
            "involved": bool(review.get("needs_graphics")),
            "plan_only": True,
            "graphics_live": False,
        },
    }
    return redact_mapping(preview)


def _local_apply_readiness(task_spec: Mapping[str, Any]) -> dict[str, Any]:
    try:
        from wabi_sabi.core.local_apply_readiness import evaluate_local_apply_readiness

        return evaluate_local_apply_readiness(task_spec)
    except Exception as exc:  # pragma: no cover - defensive fallback only.
        return {
            "status": "LOCAL_APPLY_REVIEW_REQUIRED",
            "ready": False,
            "reason": redact_text(str(exc)),
            "applied_to_sources": False,
            "cloud_provider_called": False,
            "graphics_live": False,
        }


def evaluate_apply_readiness(task_spec: Mapping[str, Any] | None) -> dict[str, Any]:
    review = normalize_taskspec_for_review(task_spec or {})
    blockers = [
        "UI apply is intentionally disabled in v0.1.",
        "No future apply path is allowed until ActionGate, GhostGate, RollbackStore and TestRunner are implemented for this TaskSpec.",
        "No source mutation is allowed from UI in this phase.",
    ]
    if review.get("needs_cloud"):
        blockers.append("Cloud involvement remains proposal_only; provider output cannot be applied directly.")
    if review.get("needs_graphics"):
        blockers.append("GraphicsBridge remains plan-only; graphics_live=false.")
    if not review.get("affected_paths"):
        blockers.append("Affected paths must be explicit before any future local apply.")
    if not review.get("suggested_tests"):
        blockers.append("Required tests must be defined before any future local apply.")
    return {
        "apply_ready": False,
        "apply_status": "BLOCKED",
        "reason": "APPLY_NOT_AVAILABLE_REVIEW_ONLY_V0_1",
        "blockers": blockers,
        "missing": [
            "explicit_human_apply_gate",
            "ghostgate_simulation",
            "rollback_snapshot",
            "test_plan_lock",
            "path_allowlist",
        ],
        "applied_to_sources": False,
        "cloud_provider_called": False,
        "graphics_live": False,
    }


def list_required_gates(task_spec: Mapping[str, Any] | None) -> list[dict[str, str]]:
    review = normalize_taskspec_for_review(task_spec or {})
    gates = [
        {
            "name": "ActionGate",
            "status": "REQUIRED_FUTURE",
            "reason": "Local write/apply requires explicit gate.",
        },
        {
            "name": "GhostGate",
            "status": "REQUIRED_FUTURE",
            "reason": "Rollback and failure simulation required before apply.",
        },
        {
            "name": "RollbackStore",
            "status": "REQUIRED_FUTURE",
            "reason": "Must snapshot affected paths before mutation.",
        },
        {
            "name": "TestRunner",
            "status": "REQUIRED_FUTURE",
            "reason": "Must define tests before mutation.",
        },
        {
            "name": "PathAllowlist",
            "status": "REQUIRED_FUTURE",
            "reason": "Affected paths must be inside the allowed workspace and explicitly listed.",
        },
    ]
    if review.get("needs_cloud"):
        gates.append(
            {
                "name": "CloudBudgetGate",
                "status": "REQUIRED_CURRENT",
                "reason": "Cloud remains proposal_only and cannot authorize source apply.",
            }
        )
    if review.get("needs_graphics"):
        gates.append(
            {
                "name": "GraphicsPlanGate",
                "status": "REQUIRED_CURRENT",
                "reason": "Graphics work remains plan-only; graphics_live=false.",
            }
        )
    return gates


def list_required_tests(task_spec: Mapping[str, Any] | None) -> list[str]:
    review = normalize_taskspec_for_review(task_spec or {})
    tests = [str(item) for item in review.get("suggested_tests", []) if str(item).strip()]
    if tests:
        return tests
    return [
        "Define focused tests for the affected module before any future apply.",
        "Run regression suite only from local CLI, not from UI.",
    ]


def list_required_rollback(task_spec: Mapping[str, Any] | None) -> dict[str, Any]:
    review = normalize_taskspec_for_review(task_spec or {})
    return {
        "required": True,
        "status": "REQUIRED_FUTURE",
        "snapshot_required": True,
        "affected_paths": list(review.get("affected_paths") or []),
        "reason": "Must snapshot affected paths before mutation and provide rollback evidence.",
    }


def block_apply_with_preview(task_spec: Mapping[str, Any] | None = None) -> dict[str, Any]:
    preview = build_gate_preview(task_spec or {})
    return {
        "schema": TASKSPEC_APPLY_BLOCK_SCHEMA,
        "status": "BLOCKED",
        "reason": "APPLY_NOT_AVAILABLE_REVIEW_ONLY_V0_1",
        "task_id": preview["task_id"],
        "applied_to_sources": False,
        "cloud_provider_called": False,
        "graphics_live": False,
        "publication_gate": "BLOCK",
        "gate_preview": preview,
    }


def _strip_private_text(value: Any) -> Any:
    if isinstance(value, Mapping):
        output: dict[str, Any] = {}
        for key, item in value.items():
            key_text = str(key)
            if key_text in PRIVATE_TEXT_KEYS:
                output[f"{key_text}_sha256"] = _hash_text(str(item))
                output[f"{key_text}_redacted"] = "<redacted:no_full_prompt>"
                continue
            output[key_text] = _strip_private_text(item)
        return output
    if isinstance(value, list):
        return [_strip_private_text(item) for item in value]
    if isinstance(value, str):
        return redact_text(value)
    return value


def _fingerprint(value: Mapping[str, Any]) -> str:
    payload = json.dumps(value, sort_keys=True, ensure_ascii=False, default=str)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def _hash_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def _bool(value: Any, default: bool) -> bool:
    if value is None:
        return default
    return bool(value)


def _route_for_intent(intent_name: str) -> str:
    if intent_name == "code_request":
        return "code_plan"
    if intent_name == "debug_request":
        return "debug_plan"
    if intent_name in {"graphics_scene_request", "graphics_asset_request"}:
        return "graphics_plan"
    if intent_name == "build_assist_request":
        return "build_assist_plan"
    if intent_name in {"plan_request", "file_task_request", "handoff_request"}:
        return "work_plan"
    return "local_chat"


def _summary(source: Mapping[str, Any], intent_name: str) -> str:
    title = str(source.get("title") or source.get("summary") or "").strip()
    if title:
        return title[:180]
    labels = {
        "code_request": "Review code proposal TaskSpec",
        "debug_request": "Review debug TaskSpec",
        "graphics_scene_request": "Review graphics scene TaskSpec",
        "graphics_asset_request": "Review graphics asset TaskSpec",
        "build_assist_request": "Review build-assist proposal-only TaskSpec",
        "file_task_request": "Review file task proposal",
        "handoff_request": "Review handoff proposal",
        "plan_request": "Review local plan proposal",
    }
    return labels.get(intent_name, "Review conversational TaskSpec")


def _list_field(source: Mapping[str, Any], keys: tuple[str, ...]) -> list[str]:
    for key in keys:
        value = source.get(key)
        if isinstance(value, list):
            return [redact_text(str(item))[:240] for item in value[:12]]
        if isinstance(value, tuple):
            return [redact_text(str(item))[:240] for item in list(value)[:12]]
    return []


def _affected_paths(source: Mapping[str, Any]) -> list[str]:
    paths: list[str] = []
    for key in ("affected_paths", "target_files", "target_files_review", "target"):
        value = source.get(key)
        if isinstance(value, str) and value:
            paths.append(value)
        elif isinstance(value, list):
            paths.extend(str(item) for item in value if isinstance(item, str))
    changes = source.get("changes")
    if isinstance(changes, list):
        for item in changes:
            if isinstance(item, Mapping) and item.get("target"):
                paths.append(str(item.get("target")))
    return [redact_text(path)[:260] for path in paths[:20]]


def _changes_count(source: Mapping[str, Any]) -> int:
    changes = source.get("changes")
    return len(changes) if isinstance(changes, list) else 0


def _risks_for(source: Mapping[str, Any], intent_name: str) -> list[str]:
    risks = _list_field(source, ("risks", "risk", "known_risks"))
    if risks:
        return risks
    defaults = ["No aplicar cambios sin ActionGate, rollback y tests."]
    if intent_name == "build_assist_request":
        defaults.append("Cloud output is proposal-only and cannot apply sources.")
    if intent_name.startswith("graphics_"):
        defaults.append("GraphicsBridge remains plan-only; graphics_live=false.")
    if _bool(source.get("needs_file_write"), False):
        defaults.append("File writes require a future explicit local apply path.")
    return defaults


def _assumptions_for(
    source: Mapping[str, Any],
    cloud_budget: Mapping[str, Any],
    graphics: Mapping[str, Any],
) -> list[str]:
    assumptions = _list_field(source, ("assumptions", "assumption"))
    if assumptions:
        return assumptions
    output = ["TaskSpec review is local and redacted."]
    if cloud_budget:
        output.append(f"CloudBudgetGate={cloud_budget.get('budget_gate', 'CLOUD_BUDGET_DRY_RUN')}.")
    if graphics:
        output.append(f"graphics_live={bool(graphics.get('graphics_live'))}.")
    return output


def _next_action_for(source: Mapping[str, Any], action_gate: str) -> str:
    value = str(source.get("next_action") or "").strip()
    if value:
        return value[:240]
    if action_gate == "BLOCK":
        return "Do not apply. Revise gate and task scope."
    if action_gate == "REVIEW":
        return "Review TaskSpec details before any future local apply gate."
    return "Ready for human review; apply remains blocked in v0.1."


def _gate_status(action_gate: str) -> str:
    if action_gate == "BLOCK":
        return "BLOCKED_REVIEW_REQUIRED"
    if action_gate == "APPROVE":
        return "REVIEW_ONLY_APPROVED_SCOPE"
    return "REVIEW_REQUIRED"
