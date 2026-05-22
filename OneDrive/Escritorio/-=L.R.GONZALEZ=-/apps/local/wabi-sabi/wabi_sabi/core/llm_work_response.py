from __future__ import annotations

import datetime as dt
import hashlib
import json
from pathlib import Path
from typing import Any, Mapping

from wabi_sabi.core.bridge import WitnessLog
from wabi_sabi.core.redaction import redact_mapping, redact_text


LLM_WORK_RESPONSE_SCHEMA = "wabi.llm_work_response.v0_1"
DEFAULT_NEXT_SAFE_ACTION = "Review TaskSpec / Preview Apply Local"


def build_safe_llm_work_response(
    conversation_result: Mapping[str, Any],
    *,
    runtime_root: str | Path,
    source: str = "conversation",
    persist: bool = True,
) -> dict[str, Any]:
    """Normalize UI/CLI LLM work responses into the public safe contract.

    This is intentionally a proposal surface. It records redacted evidence but
    never applies source changes, never calls providers, and never executes tests.
    """

    runtime = Path(runtime_root)
    result = redact_mapping(dict(conversation_result))
    payload = _mapping(result.get("payload"))
    llm_proposal = _mapping(result.get("llm_proposal") or payload.get("llm_proposal"))
    intent = _mapping(result.get("intent"))
    task_spec = _first_mapping(
        result.get("task_spec"),
        result.get("taskspec_review"),
        payload.get("task_spec"),
        llm_proposal.get("task_spec"),
    )
    intent_name = _first_text(
        result.get("intent_name"),
        intent.get("intent_name"),
        task_spec.get("intent_name"),
        llm_proposal.get("intent_name"),
        "chat_general",
    )
    route = _normalize_route(_first_text(result.get("route"), _route_from_intent(intent_name)), intent_name)
    graphics_plan = _normalize_graphics_plan(result, payload)
    cloud_provider_called = bool(result.get("cloud_provider_called") or payload.get("cloud_provider_called") or llm_proposal.get("cloud_provider_called"))
    applied_to_sources = False
    status = _normalize_status(result, llm_proposal)
    proposal = _proposal_summary(result, llm_proposal, graphics_plan)
    patch_candidate = _patch_candidate(task_spec)
    next_safe_action = _first_text(
        task_spec.get("next_action"),
        task_spec.get("next_safe_action"),
        patch_candidate.get("next_safe_action"),
        DEFAULT_NEXT_SAFE_ACTION,
    )
    warnings = _warnings(
        intent_name=intent_name,
        cloud_provider_called=cloud_provider_called,
        graphics_plan=graphics_plan,
        llm_proposal=llm_proposal,
    )
    tags = _tags(
        intent_name=intent_name,
        cloud_provider_called=cloud_provider_called,
        graphics_plan=graphics_plan,
        llm_proposal=llm_proposal,
    )
    metadata = _metadata(
        intent_name=intent_name,
        task_spec=task_spec,
        graphics_plan=graphics_plan,
        cloud_provider_called=cloud_provider_called,
        llm_proposal=llm_proposal,
    )
    safe: dict[str, Any] = {
        "schema": LLM_WORK_RESPONSE_SCHEMA,
        "status": status,
        "intent_name": intent_name,
        "route": route,
        "proposal": proposal,
        "task_spec": task_spec,
        "graphics_plan": graphics_plan,
        "patch_candidate": patch_candidate,
        "cloud_provider_called": cloud_provider_called,
        "applied_to_sources": applied_to_sources,
        "rollback_snapshot_required": True,
        "next_safe_action": next_safe_action,
        "warnings": warnings,
        "tags": tags,
        "metadata": metadata,
        "proposal_only": True,
        "secrets_printed": False,
        "prompts_stored": False,
        "graphics_live": False,
        "publication_gate": "BLOCK",
        "source": source,
    }
    safe = redact_mapping(safe)
    if persist:
        artifact = write_llm_work_response_artifact(runtime, safe)
        witness = append_llm_work_witness(runtime, safe, artifact_path=artifact)
        safe["runtime_json"] = str(artifact)
        safe["witness"] = witness
    return redact_mapping(safe)


def write_llm_work_response_artifact(runtime_root: str | Path, payload: Mapping[str, Any]) -> Path:
    runtime = Path(runtime_root)
    output_dir = runtime / "outputs" / "llm_work_response"
    output_dir.mkdir(parents=True, exist_ok=True)
    stamp = dt.datetime.now(dt.UTC).strftime("%Y%m%d-%H%M%S")
    digest = hashlib.sha256(json.dumps(payload, sort_keys=True, ensure_ascii=True).encode("utf-8")).hexdigest()[:12]
    path = output_dir / f"wabi_llm_work_response_{stamp}_{digest}.json"
    path.write_text(json.dumps(redact_mapping(dict(payload)), indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return path


def append_llm_work_witness(runtime_root: str | Path, payload: Mapping[str, Any], *, artifact_path: str | Path) -> dict[str, Any]:
    runtime = Path(runtime_root)
    witness_db = runtime / "witness" / "wabi_patch_witness.sqlite"
    witness = WitnessLog(witness_db)
    event_payload = {
        "schema": f"{LLM_WORK_RESPONSE_SCHEMA}.witness",
        "intent_name": payload.get("intent_name"),
        "route": payload.get("route"),
        "status": payload.get("status"),
        "runtime_json": str(artifact_path),
        "cloud_provider_called": bool(payload.get("cloud_provider_called")),
        "applied_to_sources": False,
        "rollback_snapshot_required": True,
        "proposal_only": True,
        "graphics_live": False,
        "secrets_printed": False,
    }
    event_id = witness.append("llm_work_response", redact_mapping(event_payload))
    verified, reason = witness.verify_chain()
    return {
        "event_type": "llm_work_response",
        "event_id": event_id,
        "verified": verified,
        "reason": reason,
        "db_path": str(witness_db),
    }


def _normalize_status(result: Mapping[str, Any], llm_proposal: Mapping[str, Any]) -> str:
    raw_status = str(result.get("status") or llm_proposal.get("status") or "").upper()
    if raw_status in {"OK", "REVIEW"}:
        return raw_status
    if not bool(result.get("ok", True)):
        return "REVIEW"
    if "ERROR" in raw_status or "INVALID" in raw_status or "EXCEEDED" in raw_status or "BLOCK" in raw_status:
        return "REVIEW"
    return "OK"


def _proposal_summary(result: Mapping[str, Any], llm_proposal: Mapping[str, Any], graphics_plan: Mapping[str, Any]) -> str:
    if llm_proposal:
        llm_status = str(llm_proposal.get("status") or "LLM_PROPOSAL_REVIEW")
        if llm_proposal.get("cloud_provider_called"):
            return redact_text(f"LLM cloud proposal received as proposal-only ({llm_status}).")
        return redact_text(f"LLM proposal is proposal-only/dry-run ({llm_status}); no provider call was made.")
    if graphics_plan.get("graphics_plan_ready"):
        return "GraphicsBridge generated a plan-only DUAT graphics proposal; graphics_live=false."
    response = str(result.get("response") or result.get("output") or "").strip()
    if response:
        return redact_text(response[:700])
    return "Local proposal-only TaskSpec response."


def _normalize_graphics_plan(result: Mapping[str, Any], payload: Mapping[str, Any]) -> dict[str, Any]:
    direct = _mapping(result.get("graphics_plan"))
    graphics = _mapping(result.get("graphics") or payload.get("graphics"))
    payload_plan = _mapping(payload.get("graphics_plan"))
    plan = _mapping(direct.get("plan") or graphics.get("plan") or payload_plan)
    is_graphics = str(result.get("intent_name") or _mapping(result.get("intent")).get("intent_name") or "").startswith("graphics_")
    return redact_mapping(
        {
            "graphics_live": False,
            "graphics_plan_ready": bool(direct.get("graphics_plan_ready") or graphics.get("graphics_plan_ready") or plan or is_graphics),
            "external_calls_allowed": False,
            "publication_allowed": False,
            "plan_mode": True,
            "plan": plan,
        }
    )


def _patch_candidate(task_spec: Mapping[str, Any]) -> dict[str, Any]:
    affected_paths = _string_list(task_spec.get("affected_paths"))
    tests = _string_list(task_spec.get("suggested_tests") or task_spec.get("test_commands"))
    changes = task_spec.get("changes") if isinstance(task_spec.get("changes"), list) else []
    diff_preview: list[str] = []
    for change in changes[:5]:
        if not isinstance(change, Mapping):
            continue
        target = redact_text(str(change.get("target") or change.get("path") or ""))
        operation = redact_text(str(change.get("operation") or "proposed_change"))
        diff_preview.append(f"{operation}: {target}".strip())
    return redact_mapping(
        {
            "task_id": _first_text(task_spec.get("task_id"), task_spec.get("id"), _fingerprint(task_spec)),
            "summary": _first_text(task_spec.get("summary"), task_spec.get("title"), task_spec.get("description"), "TaskSpec proposal."),
            "affected_paths": affected_paths,
            "diff_preview": diff_preview,
            "tests_to_run": tests,
            "rollback_snapshot_required": True,
            "apply_mode": "local_allowlisted_preview",
            "cloud_provider_called": False,
            "proposal_only": True,
            "incremental": True,
            "simulation_supported": True,
            "source": "ConversationEngine/TaskSpec",
            "next_safe_action": DEFAULT_NEXT_SAFE_ACTION,
        }
    )


def _warnings(
    *,
    intent_name: str,
    cloud_provider_called: bool,
    graphics_plan: Mapping[str, Any],
    llm_proposal: Mapping[str, Any],
) -> list[str]:
    warnings = ["Proposal-only; Apply Local blocked until explicit local readiness."]
    if not cloud_provider_called:
        warnings.append("Cloud live requires double opt-in and CloudBudgetGate allowance.")
    if llm_proposal and str(llm_proposal.get("status") or "").upper().endswith("EXCEEDED"):
        warnings.append("CloudBudgetGate blocked the cloud call.")
    if graphics_plan.get("graphics_plan_ready") or intent_name.startswith("graphics_"):
        warnings.append("GraphicsBridge plan-only; graphics_live=false.")
    warnings.append("No push, deploy, publication, BrowserBridge live, or graphics_live was triggered.")
    return warnings


def _tags(
    *,
    intent_name: str,
    cloud_provider_called: bool,
    graphics_plan: Mapping[str, Any],
    llm_proposal: Mapping[str, Any],
) -> list[str]:
    tags = ["proposal_only", "vibe_coding", "apply_local_requires_confirmation", "rollback_required", "publication_blocked"]
    tags.append("cloud_provider_called" if cloud_provider_called else "cloud_provider_not_called")
    if not cloud_provider_called:
        tags.append("double_opt_in_required")
    if llm_proposal:
        tags.extend(["LLM_proposal", "llm_proposal_attached"])
    if graphics_plan.get("graphics_plan_ready") or intent_name.startswith("graphics_"):
        tags.extend(["duat_graphics_plan", "graphics_live_false"])
    if intent_name == "hypothesis_request":
        tags.extend(["hypothesis_packet", "counterexample_search", "claim_gate"])
    return sorted(set(tags))


def _metadata(
    *,
    intent_name: str,
    task_spec: Mapping[str, Any],
    graphics_plan: Mapping[str, Any],
    cloud_provider_called: bool,
    llm_proposal: Mapping[str, Any],
) -> dict[str, Any]:
    affected_paths = _string_list(task_spec.get("affected_paths"))
    tests = _string_list(task_spec.get("suggested_tests") or task_spec.get("test_commands"))
    category = _category_for_intent(intent_name)
    risk = _risk_level(task_spec=task_spec, cloud_provider_called=cloud_provider_called, affected_paths=affected_paths)
    priority = _priority_for_risk(risk)
    return redact_mapping(
        {
            "priority": priority,
            "risk": risk,
            "category": category,
            "relevance": "high" if intent_name in {"code_request", "debug_request", "graphics_scene_request", "graphics_asset_request"} else "medium",
            "incremental": True,
            "incremental_strategy": _incremental_strategy(intent_name, affected_paths),
            "fallback_mode": "local_rules_task_spec" if not cloud_provider_called else "cloud_proposal_validated_locally",
            "apply_simulation": {
                "available": True,
                "mode": "Apply Local Preview",
                "modifies_files": False,
            },
            "asset_audit_required": intent_name in {"graphics_scene_request", "graphics_asset_request"},
            "duat_graphics_plan_only": bool(graphics_plan.get("graphics_plan_ready")),
            "hypothesis_packet": intent_name == "hypothesis_request",
            "counterexample_search": intent_name == "hypothesis_request",
            "budget_control": "CloudBudgetGate",
            "interface_mode": "vibe_coding",
            "workflow": [
                "chat",
                "llm_proposal",
                "taskspec_review",
                "gate_preview",
                "apply_local_preview",
                "explicit_apply_local",
            ],
            "llm_status": str(llm_proposal.get("status") or "not_attached") if llm_proposal else "not_attached",
            "affected_path_count": len(affected_paths),
            "suggested_test_count": len(tests),
        }
    )


def _category_for_intent(intent_name: str) -> str:
    if intent_name == "code_request":
        return "code"
    if intent_name == "debug_request":
        return "debug"
    if intent_name in {"graphics_scene_request", "graphics_asset_request"}:
        return "duat_graphics"
    if intent_name == "build_assist_request":
        return "build_assist"
    if intent_name == "hypothesis_request":
        return "hypothesis"
    if intent_name == "handoff_request":
        return "handoff"
    if intent_name in {"plan_request", "file_task_request"}:
        return "planning"
    return "conversation"


def _risk_level(*, task_spec: Mapping[str, Any], cloud_provider_called: bool, affected_paths: list[str]) -> str:
    if cloud_provider_called:
        return "medium"
    if len(affected_paths) > 3:
        return "medium"
    if task_spec.get("needs_file_write") or task_spec.get("apply_mode") == "local_allowlisted":
        return "medium"
    return "low"


def _priority_for_risk(risk: str) -> str:
    return "P1" if risk == "medium" else "P2"


def _incremental_strategy(intent_name: str, affected_paths: list[str]) -> list[str]:
    if intent_name in {"graphics_scene_request", "graphics_asset_request"}:
        return ["split_scene_plan", "review_asset_provenance", "preview_graphics_plan", "keep_graphics_live_false"]
    if intent_name == "hypothesis_request":
        return ["formalize_claim", "run_counterexample_search", "attach_evidence", "record_decision_before_reuse"]
    if affected_paths:
        return ["split_by_file", "preview_patch_candidate", "run_targeted_tests", "apply_only_after_confirmation"]
    return ["review_taskspec", "generate_local_fallback_plan", "confirm_before_apply"]


def _mapping(value: Any) -> dict[str, Any]:
    return dict(value) if isinstance(value, Mapping) else {}


def _first_mapping(*values: Any) -> dict[str, Any]:
    for value in values:
        if isinstance(value, Mapping) and value:
            return redact_mapping(dict(value))
    return {}


def _first_text(*values: Any) -> str:
    for value in values:
        text = redact_text(str(value or "")).strip()
        if text:
            return text
    return ""


def _string_list(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    output: list[str] = []
    for item in value[:20]:
        if isinstance(item, str):
            output.append(redact_text(item))
        elif isinstance(item, Mapping):
            output.append(redact_text(str(item.get("target") or item.get("path") or item.get("command") or "")))
    return [item for item in output if item]


def _route_from_intent(intent_name: str) -> str:
    if intent_name == "code_request":
        return "code_plan"
    if intent_name == "debug_request":
        return "debug_plan"
    if intent_name.startswith("graphics_"):
        return "graphics_plan"
    if intent_name == "build_assist_request":
        return "build_assist_plan"
    if intent_name == "hypothesis_request":
        return "hypothesis_plan"
    return "work_plan" if intent_name else "local_chat"


def _normalize_route(route: str, intent_name: str) -> str:
    if route in {
        "code_request",
        "debug_request",
        "graphics_scene_request",
        "graphics_asset_request",
        "build_assist_request",
        "plan_request",
        "file_task_request",
        "handoff_request",
        "hypothesis_request",
    }:
        return _route_from_intent(intent_name or route)
    return route or _route_from_intent(intent_name)


def _fingerprint(task_spec: Mapping[str, Any]) -> str:
    payload = json.dumps(redact_mapping(dict(task_spec)), sort_keys=True, ensure_ascii=True)
    return f"taskspec-{hashlib.sha256(payload.encode('utf-8')).hexdigest()[:12]}"
