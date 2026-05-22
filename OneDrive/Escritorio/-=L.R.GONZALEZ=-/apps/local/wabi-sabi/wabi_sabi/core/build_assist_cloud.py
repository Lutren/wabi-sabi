from __future__ import annotations

import json
import os
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Mapping

from wabi_sabi.core.browser_bridge import build_browser_bridge_status
from wabi_sabi.core.cloud_adapters import CLOUD_ENABLE_ENV, build_cloud_adapters
from wabi_sabi.core.cloud_budget import CloudBudgetGate
from wabi_sabi.core.redaction import is_sensitive_key, redact_mapping, redact_text
from wabi_sabi.core.tools import write_artifact


BUILD_ASSIST_SCHEMA = "wabi.build_assist_cloud.v0_1"
BUILD_ASSIST_SMOKE_SCHEMA = "wabi.build_assist_nvidia_smoke.v0_1"
BUILD_ASSIST_ENABLE_ENV = "WABI_BUILD_ASSIST_CLOUD"
BUILD_ASSIST_MODEL_ALIAS_ENV = "WABI_BUILD_ASSIST_NVIDIA_MODEL_ALIAS"
BUILD_ASSIST_MAX_REQUESTS_ENV = "WABI_BUILD_ASSIST_MAX_CLOUD_CALLS"
DEFAULT_BUILD_ASSIST_MODEL_ALIAS = "nano-30b"
DEFAULT_BUILD_ASSIST_MAX_CLOUD_CALLS = 12
USAGE_LOG_NAME = "build_assist_cloud_usage.jsonl"
SMOKE_PROMPT = (
    "Return only valid JSON with keys status, provider, mode, proposal. "
    "status must be WABI_PROVIDER_OK. provider must be nvidia. mode must be proposal_only. "
    "proposal must be a short safe plan for creating a local helper function. Do not include code."
)


def build_assist_default_model_alias(env: Mapping[str, str] | None = None) -> str:
    values = os.environ if env is None else env
    return (values.get(BUILD_ASSIST_MODEL_ALIAS_ENV) or DEFAULT_BUILD_ASSIST_MODEL_ALIAS).strip()


def build_build_assist_cloud_status(
    *,
    workspace: str | Path,
    runtime_root: str | Path,
    env: Mapping[str, str] | None = None,
    provider_status: dict[str, Any] | None = None,
) -> dict[str, Any]:
    values = os.environ if env is None else env
    runtime = Path(runtime_root)
    adapters = build_cloud_adapters(runtime_root=runtime, env=dict(values))
    nvidia = adapters["nvidia-nim"]
    nvidia_status = nvidia.status()
    model_alias = build_assist_default_model_alias(values)
    model = nvidia.resolve_model(model_alias)
    enabled = values.get(BUILD_ASSIST_ENABLE_ENV, "0") == "1"
    cloud_flag = values.get(CLOUD_ENABLE_ENV, "0") == "1"
    nvidia_configured = bool(nvidia_status.get("configured"))
    cloud_live_ready = bool(enabled and cloud_flag and nvidia_configured)
    budget = build_assist_budget_status(runtime_root=runtime, env=values)
    cloud_budget = CloudBudgetGate(runtime_root=runtime, env=values).render_status(
        provider="nvidia",
        model_alias=model_alias,
        intent="status",
    )
    browser = build_browser_bridge_status(env=dict(values))
    action_gate = "REVIEW_CLOUD_LIVE_READY" if cloud_live_ready else "APPROVE_LOCAL_DRY_RUN"
    if enabled and not cloud_flag:
        action_gate = "REVIEW_SET_WABI_ALLOW_CLOUD_PROVIDERS"
    elif enabled and cloud_flag and not nvidia_configured:
        action_gate = "REVIEW_CONFIGURE_NVIDIA_KEY"
    if cloud_live_ready and budget["remaining_cloud_calls"] <= 0:
        action_gate = "BLOCK_BUDGET_EXHAUSTED"
        cloud_live_ready = False
    if cloud_live_ready and cloud_budget["budget_gate"] == "CLOUD_BUDGET_EXCEEDED":
        action_gate = "BLOCK_CLOUD_BUDGET_EXCEEDED"
        cloud_live_ready = False

    payload = {
        "schema": BUILD_ASSIST_SCHEMA,
        "ok": True,
        "action": "build_assist_cloud_status",
        "workspace": str(Path(workspace)),
        "runtime_root": str(runtime),
        "mode": "TEMPORARY_CLOUD_ASSIST_LOCAL_FIRST",
        "enabled": enabled,
        "enable_env": BUILD_ASSIST_ENABLE_ENV,
        "cloud_enable_env": CLOUD_ENABLE_ENV,
        "cloud_flag_enabled": cloud_flag,
        "cloud_live_ready": cloud_live_ready,
        "action_gate": action_gate,
        "authority": {
            "cloud_authority": "proposal_only",
            "local_wabi_decides": True,
            "real_apply_allowed": False,
            "auto_apply_from_cloud": False,
            "publication_gate": "BLOCK",
        },
        "default_route": [
            "local_ollama_or_codex_dry_run",
            "nvidia_nim_proposal_nano",
            "nvidia_nim_super_manual_review",
            "browserbridge_manual_double_opt_in",
            "dry_run",
        ],
        "nvidia": {
            "configured": nvidia_configured,
            "enabled": bool(nvidia_status.get("enabled")),
            "available": bool(nvidia_status.get("available")),
            "default_model_alias": model_alias,
            "default_model": model,
            "normal_aliases": ["nano-9b", "nano-30b"],
            "manual_review_aliases": ["super", "ultra", "llama-70b", "kimi", "deepseek", "mistral", "minimax", "glm"],
            "active_env_key": nvidia_status.get("active_env_key", ""),
        },
        "budget": budget,
        "cloud_budget": cloud_budget,
        "browserbridge": {
            "default_backend": browser.get("default_backend"),
            "bridge_enabled": browser.get("bridge_enabled"),
            "send_enabled": browser.get("send_enabled"),
            "authority": browser.get("authority"),
            "send_enable_env": browser.get("send_enable_env"),
        },
        "provider_order": list((provider_status or {}).get("provider_order", [])),
        "recommended_commands": [
            ".\\wabi.cmd build-assist-status --json",
            ".\\wabi.cmd build-assist-plan \"crear helper seguro\" --dry-run --json",
            "$env:WABI_BUILD_ASSIST_CLOUD='1'; $env:WABI_ALLOW_CLOUD_PROVIDERS='1'; .\\wabi.cmd build-assist-plan \"crear helper seguro\" --codex-provider nano-30b --json",
        ],
        "hard_boundaries": [
            "No secrets in prompts, logs, docs, or provider responses.",
            "No full workspace upload.",
            "No private canon, game, browser cookies, or .env material.",
            "Provider output must validate as wabi.cloud_code_proposal.v0_1 before any local plan.",
            "Patch/apply remains local, rollback-backed, and separately gated.",
        ],
    }
    return redact_mapping(payload, env=values)


def build_assist_budget_status(
    *,
    runtime_root: str | Path,
    env: Mapping[str, str] | None = None,
) -> dict[str, Any]:
    values = os.environ if env is None else env
    max_calls = _positive_int(values.get(BUILD_ASSIST_MAX_REQUESTS_ENV), DEFAULT_BUILD_ASSIST_MAX_CLOUD_CALLS)
    used = _count_recorded_cloud_calls(Path(runtime_root))
    return {
        "max_cloud_calls": max_calls,
        "recorded_cloud_calls": used,
        "remaining_cloud_calls": max(0, max_calls - used),
        "budget_env": BUILD_ASSIST_MAX_REQUESTS_ENV,
        "usage_log": str(_usage_log_path(Path(runtime_root))),
        "retry_policy": "no_auto_retry_on_quota_billing_or_rate_limit",
    }


def run_build_assist_nvidia_smoke(
    *,
    workspace: str | Path,
    runtime_root: str | Path,
    provider: str = "nvidia",
    model_alias: str | None = None,
    live: bool = False,
    timeout: int = 35,
    env: Mapping[str, str] | None = None,
    http_post: Callable[[str, dict[str, str], dict[str, Any], int], dict[str, Any]] | None = None,
) -> dict[str, Any]:
    values = os.environ if env is None else env
    runtime = Path(runtime_root)
    provider_id = _normalize_provider(provider)
    model_alias = (model_alias or build_assist_default_model_alias(values)).strip()
    adapters = build_cloud_adapters(runtime_root=runtime, env=dict(values), http_post=http_post)
    adapter = adapters["nvidia-nim"]
    model = adapter.resolve_model(model_alias)
    status = build_build_assist_cloud_status(workspace=workspace, runtime_root=runtime, env=values)
    budget = build_assist_budget_status(runtime_root=runtime, env=values)
    cloud_budget_gate = CloudBudgetGate(runtime_root=runtime, env=values)
    started = time.perf_counter()
    base_payload: dict[str, Any] = {
        "schema": BUILD_ASSIST_SMOKE_SCHEMA,
        "status": "REVIEW_NOT_RUN",
        "provider": "nvidia",
        "provider_requested": provider,
        "model_alias": model_alias,
        "model": model,
        "mode": "proposal_only",
        "cloud_live_ready": bool(status.get("cloud_live_ready")),
        "cloud_provider_called": False,
        "applied_to_sources": False,
        "secrets_printed": False,
        "latency_ms": None,
        "usage": {"input_tokens": None, "output_tokens": None},
        "cost_estimate": None,
        "redaction": "PASS",
        "error_class": None,
        "artifact_path": "",
        "build_assist": status,
        "prompt_class": "synthetic_non_sensitive",
        "prompt_sent": False,
        "response": {},
    }
    if provider_id != "nvidia":
        return _finalize_smoke_payload(
            runtime,
            values,
            {
                **base_payload,
                "status": "REVIEW_UNSUPPORTED_PROVIDER",
                "error_class": "UNSUPPORTED_PROVIDER_REDACTED",
            },
        )
    if not live:
        return _finalize_smoke_payload(
            runtime,
            values,
            {
                **base_payload,
                "status": "REVIEW_LIVE_FLAG_REQUIRED",
                "error_class": "LIVE_FLAG_REQUIRED",
            },
        )
    if values.get(BUILD_ASSIST_ENABLE_ENV, "0") != "1":
        return _finalize_smoke_payload(
            runtime,
            values,
            {
                **base_payload,
                "status": "REVIEW_BUILD_ASSIST_DISABLED",
                "error_class": "BUILD_ASSIST_FLAG_MISSING",
            },
        )
    if values.get(CLOUD_ENABLE_ENV, "0") != "1":
        return _finalize_smoke_payload(
            runtime,
            values,
            {
                **base_payload,
                "status": "REVIEW_CLOUD_PROVIDER_DISABLED",
                "error_class": "CLOUD_PROVIDER_FLAG_MISSING",
            },
        )
    if not adapter.status().get("configured"):
        return _finalize_smoke_payload(
            runtime,
            values,
            {
                **base_payload,
                "status": "REVIEW_NVIDIA_KEY_MISSING",
                "error_class": "NVIDIA_KEY_MISSING",
            },
        )
    if budget["remaining_cloud_calls"] <= 0:
        return _finalize_smoke_payload(
            runtime,
            values,
            {
                **base_payload,
                "status": "BLOCK_BUDGET_EXHAUSTED",
                "error_class": "BUDGET_EXHAUSTED",
            },
        )
    budget_decision = cloud_budget_gate.can_call("nvidia", model_alias, "build_assist_smoke")
    if not budget_decision.get("next_cloud_call_allowed"):
        cloud_budget_gate.record_blocked_call("nvidia", model_alias, "build_assist_smoke", status=str(budget_decision.get("budget_gate")))
        return _finalize_smoke_payload(
            runtime,
            values,
            {
                **base_payload,
                "status": str(budget_decision.get("budget_gate") or "CLOUD_BUDGET_REVIEW"),
                "error_class": str(budget_decision.get("budget_gate") or "CLOUD_BUDGET_REVIEW"),
                "cloud_budget": budget_decision,
            },
        )

    cloud_budget_gate.record_planned_call("nvidia", model_alias, "build_assist_smoke")
    try:
        result = adapter.execute(SMOKE_PROMPT, timeout=timeout, model=model_alias)
        latency_ms = int((time.perf_counter() - started) * 1000)
    except Exception:
        latency_ms = int((time.perf_counter() - started) * 1000)
        failed_payload = {
            **base_payload,
            "status": "REVIEW_NVIDIA_LIVE_SMOKE_FAILED",
            "cloud_provider_called": True,
            "prompt_sent": True,
            "latency_ms": latency_ms,
            "error_class": "PROVIDER_EXCEPTION_REDACTED",
        }
        cloud_budget_gate.record_completed_call("nvidia", model_alias, failed_payload)
        return _finalize_smoke_payload(
            runtime,
            values,
            failed_payload,
            record_usage=True,
        )

    parsed, parse_ok = _safe_parse_json_response(result.output)
    pass_conditions = (
        result.ok
        and parse_ok
        and parsed.get("status") == "WABI_PROVIDER_OK"
        and str(parsed.get("provider", "")).lower() == "nvidia"
        and parsed.get("mode") == "proposal_only"
    )
    payload = {
        **base_payload,
        "status": "LIVE_SMOKE_PASS" if pass_conditions else "REVIEW_NVIDIA_LIVE_SMOKE_FAILED",
        "cloud_provider_called": result.action in {"cloud_chat_completion", "cloud_provider_error"} or result.ok,
        "prompt_sent": True,
        "latency_ms": latency_ms,
        "error_class": None if pass_conditions else _smoke_error_class(result, parse_ok),
        "response": parsed,
        "provider_action": result.action,
        "provider_gate": result.gate,
        "provider_artifacts": result.artifacts,
    }
    cloud_budget_gate.record_completed_call("nvidia", model_alias, payload)
    return _finalize_smoke_payload(runtime, values, payload, record_usage=payload["cloud_provider_called"])


def record_build_assist_usage(*, runtime_root: str | Path, event: dict[str, Any]) -> Path:
    runtime = Path(runtime_root)
    path = _usage_log_path(runtime)
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = redact_mapping(
        {
            "schema": "wabi.build_assist_cloud_usage.v0_1",
            "timestamp_utc": datetime.now(timezone.utc).isoformat(),
            **event,
        }
    )
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(payload, ensure_ascii=False) + "\n")
    return path


def _finalize_smoke_payload(
    runtime_root: Path,
    env: Mapping[str, str],
    payload: dict[str, Any],
    *,
    record_usage: bool = False,
) -> dict[str, Any]:
    clean = redact_mapping(payload, env=env)
    text_without_artifact = json.dumps(clean, ensure_ascii=False, sort_keys=True)
    redaction = "PASS" if not _contains_sensitive_env_value(text_without_artifact, env) else "REVIEW"
    clean["redaction"] = redaction
    clean["secrets_printed"] = redaction != "PASS"
    artifact = write_artifact(
        runtime_root / "outputs" / "build_assist_smoke",
        "wabi_build_assist_nvidia_smoke",
        ".json",
        json.dumps(clean, indent=2, ensure_ascii=False) + "\n",
    )
    clean["artifact_path"] = str(artifact)
    if record_usage:
        record_build_assist_usage(
            runtime_root=runtime_root,
            event={
                "action": "build_assist_smoke",
                "provider": clean.get("provider"),
                "model": clean.get("model"),
                "model_alias": clean.get("model_alias"),
                "status": clean.get("status"),
                "cloud_provider_called": clean.get("cloud_provider_called"),
                "artifact_path": str(artifact),
            },
        )
    final_text = json.dumps(clean, ensure_ascii=False, sort_keys=True)
    if _contains_sensitive_env_value(final_text, env):
        clean["redaction"] = "REVIEW"
        clean["secrets_printed"] = True
    return clean


def _safe_parse_json_response(text: str) -> tuple[dict[str, Any], bool]:
    redacted = redact_text(text)
    try:
        payload = json.loads(redacted)
    except json.JSONDecodeError:
        return {"raw_text": redacted, "parse_error": "json_decode_failed"}, False
    if not isinstance(payload, dict):
        return {"raw_text": redacted, "parse_error": "json_not_object"}, False
    return redact_mapping(payload), True


def _smoke_error_class(result: Any, parse_ok: bool) -> str:
    if not result.ok:
        return "PROVIDER_ERROR_REDACTED"
    if not parse_ok:
        return "JSON_PARSE_REVIEW"
    return "CONTRACT_REVIEW"


def _normalize_provider(provider: str) -> str:
    normalized = str(provider or "").strip().lower()
    return "nvidia" if normalized in {"nvidia", "nvidia-nim"} else normalized


def _contains_sensitive_env_value(text: str, env: Mapping[str, str]) -> bool:
    for key, value in env.items():
        if not value or len(value) < 8 or not is_sensitive_key(key):
            continue
        if value in text:
            return True
    return False


def _usage_log_path(runtime_root: Path) -> Path:
    return runtime_root / "logs" / USAGE_LOG_NAME


def _count_recorded_cloud_calls(runtime_root: Path) -> int:
    path = _usage_log_path(runtime_root)
    if not path.exists():
        return 0
    count = 0
    try:
        for line in path.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            try:
                payload = json.loads(line)
            except json.JSONDecodeError:
                continue
            if payload.get("cloud_provider_called") is True:
                count += 1
    except OSError:
        return 0
    return count


def _positive_int(value: str | None, default: int) -> int:
    try:
        parsed = int(str(value or "").strip())
    except ValueError:
        return default
    return parsed if parsed > 0 else default
