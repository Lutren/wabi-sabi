from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
from typing import Any, Callable, Mapping

from wabi_sabi.core.cloud_adapters import build_cloud_adapters
from wabi_sabi.core.cloud_budget import CloudBudgetGate
from wabi_sabi.core.cloud_code_proposal import (
    build_dry_run_cloud_code_proposal,
    cloud_proposal_to_task_spec,
    extract_cloud_code_proposal_payload,
    validate_cloud_code_proposal,
    write_cloud_proposal_artifact,
    write_cloud_task_spec_artifact,
)
from wabi_sabi.core.redaction import redact_mapping, redact_text


LLM_PROPOSAL_SCHEMA = "wabi.llm_proposal.v0_1"
LLM_CLOUD_DEFAULT_ENV = "WABI_LLM_PROVIDER_CLOUD_DEFAULT"
LLM_PROVIDER_ENV = "WABI_LLM_PROVIDER"
LLM_MODEL_ALIAS_ENV = "WABI_LLM_MODEL_ALIAS"
DEFAULT_LLM_PROVIDER = "nvidia"
DEFAULT_LLM_MODEL_ALIAS = "nano-30b"


def llm_cloud_default_enabled(env: Mapping[str, str] | None = None) -> bool:
    values = os.environ if env is None else env
    return str(values.get(LLM_CLOUD_DEFAULT_ENV, "0")).strip() == "1"


def build_llm_proposal_status(
    *,
    runtime_root: str | Path,
    env: Mapping[str, str] | None = None,
    session_id: str | None = None,
    intent: str = "status",
    provider: str | None = None,
    model_alias: str | None = None,
    http_post: Callable[[str, dict[str, str], dict[str, Any], int], dict[str, Any]] | None = None,
) -> dict[str, Any]:
    values = os.environ if env is None else env
    runtime = Path(runtime_root)
    selected_provider = _provider_name(provider, values)
    selected_model = _model_alias(model_alias, selected_provider, values)
    adapters = build_cloud_adapters(runtime_root=runtime, env=dict(values), http_post=http_post)
    adapter_key = _adapter_key(selected_provider)
    adapter = adapters.get(adapter_key)
    adapter_status = adapter.status() if adapter is not None else {"configured": False, "available": False}
    budget_provider = _budget_provider_name(selected_provider)
    cloud_budget = CloudBudgetGate(runtime_root=runtime, env=values, session_id=session_id).render_status(
        provider=budget_provider,
        model_alias=selected_model,
        intent=f"llm_proposal:{intent}",
    )
    default_enabled = llm_cloud_default_enabled(values)
    provider_configured = bool(adapter_status.get("configured")) if adapter is not None else False
    cloud_live_ready = bool(default_enabled and provider_configured and cloud_budget.get("next_cloud_call_allowed"))
    return redact_mapping(
        {
            "schema": f"{LLM_PROPOSAL_SCHEMA}.status",
            "llm_cloud_default_enabled": default_enabled,
            "cloud_default_env": LLM_CLOUD_DEFAULT_ENV,
            "provider": selected_provider,
            "adapter": adapter_key,
            "model_alias": selected_model,
            "provider_configured": provider_configured,
            "provider_available": bool(adapter_status.get("available")) if adapter is not None else False,
            "cloud_budget": cloud_budget,
            "cloud_live_ready": cloud_live_ready,
            "proposal_only": True,
            "applied_to_sources": False,
            "cloud_provider_called": False,
            "graphics_live": False,
            "publication_gate": "BLOCK",
            "secret_values_printed": False,
        },
        env=values,
    )


def request_llm_proposal(
    *,
    workspace: str | Path,
    runtime_root: str | Path,
    user_text: str,
    intent_name: str,
    task_spec: dict[str, Any] | None = None,
    session_id: str | None = None,
    provider: str | None = None,
    model_alias: str | None = None,
    timeout: int = 45,
    env: Mapping[str, str] | None = None,
    http_post: Callable[[str, dict[str, str], dict[str, Any], int], dict[str, Any]] | None = None,
) -> dict[str, Any]:
    values = os.environ if env is None else env
    workspace_path = Path(workspace).resolve()
    runtime = Path(runtime_root).resolve()
    selected_provider = _provider_name(provider, values)
    selected_model = _model_alias(model_alias, selected_provider, values)
    adapter_key = _adapter_key(selected_provider)
    status = build_llm_proposal_status(
        runtime_root=runtime,
        env=values,
        session_id=session_id,
        intent=intent_name,
        provider=selected_provider,
        model_alias=selected_model,
        http_post=http_post,
    )
    base = {
        "schema": LLM_PROPOSAL_SCHEMA,
        "status": "LLM_PROPOSAL_REVIEW",
        "provider": selected_provider,
        "adapter": adapter_key,
        "model_alias": selected_model,
        "intent_name": intent_name,
        "intent_hash": _intent_hash(user_text),
        "proposal_only": True,
        "applied_to_sources": False,
        "cloud_provider_called": False,
        "graphics_live": False,
        "publication_gate": "BLOCK",
        "secrets_printed": False,
        "llm_status": status,
        "cloud_budget": status.get("cloud_budget", {}),
        "proposal_artifact": "",
        "task_spec_artifact": "",
        "task_spec": {},
        "validation": {},
        "error_class": None,
    }
    if not status.get("llm_cloud_default_enabled"):
        return _dry_run_payload(base, workspace_path, runtime, user_text, status="LLM_PROPOSAL_DEFAULT_DISABLED")
    budget = status.get("cloud_budget", {})
    if budget.get("budget_gate") == "CLOUD_BUDGET_EXCEEDED":
        CloudBudgetGate(runtime_root=runtime, env=values, session_id=session_id).record_blocked_call(
            _budget_provider_name(selected_provider),
            selected_model,
            f"llm_proposal:{intent_name}",
            status="CLOUD_BUDGET_EXCEEDED",
        )
        return _dry_run_payload(base, workspace_path, runtime, user_text, status="LLM_PROPOSAL_BUDGET_EXCEEDED")
    if not budget.get("next_cloud_call_allowed"):
        return _dry_run_payload(base, workspace_path, runtime, user_text, status=str(budget.get("budget_gate") or "LLM_PROPOSAL_DRY_RUN"))
    if not status.get("provider_configured"):
        return _dry_run_payload(base, workspace_path, runtime, user_text, status="LLM_PROPOSAL_PROVIDER_NOT_CONFIGURED")

    adapters = build_cloud_adapters(runtime_root=runtime, env=dict(values), http_post=http_post)
    adapter = adapters.get(adapter_key)
    if adapter is None:
        return _dry_run_payload(base, workspace_path, runtime, user_text, status="LLM_PROPOSAL_PROVIDER_UNSUPPORTED")

    gate = CloudBudgetGate(runtime_root=runtime, env=values, session_id=session_id)
    gate.record_planned_call(_budget_provider_name(selected_provider), selected_model, f"llm_proposal:{intent_name}")
    prompt = _build_llm_cloud_prompt(intent=_safe_intent_label(user_text), workspace_summary=_workspace_summary(task_spec))
    result = adapter.execute(prompt, timeout=timeout, model=selected_model).to_dict()
    gate.record_completed_call(
        _budget_provider_name(selected_provider),
        selected_model,
        {
            "status": result.get("action") or "provider_result",
            "provider_action": result.get("action"),
            "usage": {},
            "cost_estimate": None,
        },
    )
    called_payload = {
        **base,
        "status": "LLM_PROPOSAL_PROVIDER_CALLED",
        "cloud_provider_called": True,
        "provider_result": {
            "ok": bool(result.get("ok")),
            "provider": result.get("provider"),
            "action": result.get("action"),
            "error": redact_text(str(result.get("error", "")), env=values),
        },
    }
    if not result.get("ok"):
        called_payload["status"] = "LLM_PROPOSAL_PROVIDER_ERROR_REDACTED"
        called_payload["error_class"] = "PROVIDER_ERROR_REDACTED"
        return redact_mapping(called_payload, env=values)
    try:
        proposal = extract_cloud_code_proposal_payload(str(result.get("output") or ""))
        proposal["intent"] = _safe_intent_label(user_text)
        proposal_artifact = write_cloud_proposal_artifact(runtime / "outputs", proposal, source=f"{adapter_key}_{selected_model}")
        validation = validate_cloud_code_proposal(
            workspace=workspace_path,
            proposal_path=proposal_artifact,
            input_roots=[runtime / "outputs"],
        )
        called_payload["proposal_artifact"] = str(proposal_artifact)
        called_payload["validation"] = validation.to_dict()
        if not validation.ok:
            called_payload["status"] = "LLM_PROPOSAL_REVIEW_INVALID_CONTRACT"
            return redact_mapping(called_payload, env=values)
        generated_task = cloud_proposal_to_task_spec(validation)
        task_artifact = write_cloud_task_spec_artifact(runtime / "outputs", generated_task)
        called_payload["status"] = "LLM_PROPOSAL_READY"
        called_payload["task_spec"] = generated_task
        called_payload["task_spec_artifact"] = str(task_artifact)
        return redact_mapping(called_payload, env=values)
    except Exception as exc:  # noqa: BLE001 - provider output is untrusted.
        called_payload["status"] = "LLM_PROPOSAL_REVIEW_INVALID_JSON"
        called_payload["error_class"] = redact_text(type(exc).__name__, env=values)
        called_payload["error"] = redact_text(str(exc), env=values)
        return redact_mapping(called_payload, env=values)


def _dry_run_payload(base: dict[str, Any], workspace: Path, runtime: Path, user_text: str, *, status: str) -> dict[str, Any]:
    proposal = build_dry_run_cloud_code_proposal(intent=_safe_intent_label(user_text))
    artifact = write_cloud_proposal_artifact(runtime / "outputs", proposal, source="llm_default_dry_run")
    validation = validate_cloud_code_proposal(workspace=workspace, proposal_path=artifact, input_roots=[runtime / "outputs"])
    task_spec: dict[str, Any] = {}
    task_artifact = ""
    if validation.ok:
        task_spec = cloud_proposal_to_task_spec(validation)
        task_artifact = str(write_cloud_task_spec_artifact(runtime / "outputs", task_spec))
    return redact_mapping(
        {
            **base,
            "status": status,
            "proposal_artifact": str(artifact),
            "validation": validation.to_dict(),
            "task_spec": task_spec,
            "task_spec_artifact": task_artifact,
            "cloud_provider_called": False,
            "applied_to_sources": False,
        }
    )


def _provider_name(provider: str | None, env: Mapping[str, str]) -> str:
    raw = (provider or env.get(LLM_PROVIDER_ENV) or DEFAULT_LLM_PROVIDER).strip().lower()
    aliases = {"nvidia-nim": "nvidia", "nvidia_nim": "nvidia", "nv": "nvidia"}
    return aliases.get(raw, raw)


def _model_alias(model_alias: str | None, provider: str, env: Mapping[str, str]) -> str:
    if model_alias:
        return model_alias.strip()
    if env.get(LLM_MODEL_ALIAS_ENV):
        return str(env[LLM_MODEL_ALIAS_ENV]).strip()
    if provider == "nvidia":
        return str(env.get("WABI_BUILD_ASSIST_NVIDIA_MODEL_ALIAS") or DEFAULT_LLM_MODEL_ALIAS).strip()
    if provider == "deepseek":
        return str(env.get("WABI_DEEPSEEK_MODEL_ALIAS") or "deepseek-chat").strip()
    if provider == "qwen":
        return str(env.get("WABI_QWEN_MODEL_ALIAS") or "qwen-plus").strip()
    return "default"


def _adapter_key(provider: str) -> str:
    return {
        "nvidia": "nvidia-nim",
        "qwen": "qwen-cloud",
        "deepseek": "deepseek",
        "openrouter": "openrouter",
        "openai-compatible": "openai-compatible",
    }.get(provider, provider)


def _budget_provider_name(provider: str) -> str:
    return "nvidia" if provider == "nvidia" else provider


def _safe_intent_label(text: str) -> str:
    clean = redact_text(text).strip()
    digest = _intent_hash(clean)
    return f"redacted_intent:{digest}"


def _intent_hash(text: str) -> str:
    return hashlib.sha256(redact_text(text).encode("utf-8", errors="ignore")).hexdigest()[:16]


def _workspace_summary(task_spec: dict[str, Any] | None) -> dict[str, Any]:
    task = task_spec or {}
    return redact_mapping(
        {
            "task_schema": task.get("schema", ""),
            "intent_name": task.get("intent_name") or task.get("metadata", {}).get("intent", ""),
            "summary": task.get("summary") or task.get("title", ""),
            "affected_paths": task.get("affected_paths", []),
            "suggested_tests": task.get("suggested_tests") or task.get("test_commands", []),
            "cloud_authority": "proposal_only",
            "apply_local_requires": ["PathAllowlist", "RollbackStore", "TestRunner", "SensitiveValueScan", "BoundaryScan"],
        }
    )


def _build_llm_cloud_prompt(*, intent: str, workspace_summary: dict[str, Any]) -> str:
    schema = {
        "schema": "wabi.cloud_code_proposal.v0_1",
        "summary": "short human summary",
        "intent": "operator intent label",
        "assumptions": ["explicit assumption"],
        "files_to_read": ["relative/path.py"],
        "changes": [
            {
                "operation": "write_text",
                "target": "relative/path.py",
                "suffix": ".py",
                "content": "complete file text",
            }
        ],
        "commands_requested": ["python -m py_compile relative/path.py"],
        "test_commands": ["python -m py_compile relative/path.py"],
        "risks": ["risk or boundary"],
        "rollback_notes": ["how local Wabi can restore the prior file state"],
        "debug_strategy": ["sanitized debug step"],
        "gate_recommendation": "REVIEW",
    }
    return "\n".join(
        [
            "Act as a cloud planner only. You do not execute code and you do not control the PC.",
            "Return exactly one JSON object and no markdown.",
            "The JSON must match this contract:",
            json.dumps(schema, indent=2, ensure_ascii=False),
            "",
            "Hard rules:",
            "- Use only operation=write_text.",
            "- Use relative workspace paths only.",
            "- Avoid sensitive host values, external release actions, destructive shell actions, or full source dumps.",
            "- Commands must be SafeExecutor-compatible: python -m py_compile, python -m pytest, or pytest.",
            "- Prefer gate_recommendation=REVIEW unless the change is trivial and fully testable.",
            "- Include complete replacement file content for each change.",
            "",
            "Operator intent label:",
            intent,
            "",
            "Sanitized workspace summary:",
            json.dumps(workspace_summary, indent=2, ensure_ascii=False),
        ]
    )
