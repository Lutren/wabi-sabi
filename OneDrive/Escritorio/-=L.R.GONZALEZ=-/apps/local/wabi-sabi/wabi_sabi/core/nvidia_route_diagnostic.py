from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping

from wabi_sabi.core.cloud_adapters import CLOUD_ENABLE_ENV, build_cloud_adapters
from wabi_sabi.core.provider_status_contract import (
    FALLBACK_MODEL,
    FALLBACK_PROVIDER,
    LATEST_STATUS_NAME,
    PRIMARY_MODEL,
    PRIMARY_PROVIDER,
    PUBLICATION_GATE,
)
from wabi_sabi.core.redaction import is_sensitive_key, redact_mapping, redact_text
from wabi_sabi.core.tools import write_artifact


DIAGNOSTIC_SCHEMA = "wabi.nvidia_route_diagnostic.v0_5"
STATE_FINGERPRINT = "WABI-CLOUD-PROVIDER-v0-5-20260518"
PROVIDER_OR_MODEL_NOT_FOUND = "PROVIDER_OR_MODEL_NOT_FOUND_REDACTED"

ALIAS_CANDIDATES = (
    "nvidia/nemotron-3-super-120b-a12b",
    "nvidia/nemotron-super-120b-a12b",
    "nemotron-3-super-120b-a12b",
    "nemotron-super-120b-a12b",
)


def build_nvidia_route_diagnostic(
    *,
    runtime_root: str | Path,
    env: Mapping[str, str] | None = None,
    allow_model_list: bool = False,
    latest_status: Mapping[str, Any] | None = None,
    qa_status_path: str | Path | None = None,
) -> dict[str, Any]:
    """Build a route diagnostic without calling NVIDIA or listing remote models."""

    values = dict(os.environ if env is None else env)
    runtime = Path(runtime_root)
    status = dict(latest_status or _read_latest_status(runtime) or _read_qa_status(qa_status_path))
    adapter_status = build_cloud_adapters(runtime_root=runtime, env=values)["nvidia-nim"].status()
    credential_present = bool(_active_nvidia_credential_env(values))
    endpoint_base = str(adapter_status.get("base_url") or values.get("NVIDIA_NIM_BASE_URL") or "https://integrate.api.nvidia.com/v1/chat/completions")
    endpoint_mode = _endpoint_mode(endpoint_base)
    last_smoke_status = str(status.get("live_smoke_status") or "REVIEW_SMOKE_NOT_RUN")
    last_error_class = _last_error_class(status)
    route_status = _route_diagnostic_status(
        credential_present=credential_present,
        endpoint_mode=endpoint_mode,
        last_smoke_status=last_smoke_status,
        last_error_class=last_error_class,
    )
    recommended_next_smoke = "ALLOW" if route_status == "PASS" else "DO_NOT_CALL"
    model_list_status = "REVIEW_MODEL_LIST_API"
    if allow_model_list:
        model_list_status = "REVIEW_NOT_IMPLEMENTED_NO_REMOTE_CALL"

    payload: dict[str, Any] = {
        "schema": DIAGNOSTIC_SCHEMA,
        "state_fingerprint": STATE_FINGERPRINT,
        "provider": PRIMARY_PROVIDER,
        "primary_model_configured": PRIMARY_MODEL,
        "fallback_provider": FALLBACK_PROVIDER,
        "fallback_model": FALLBACK_MODEL,
        "alias_candidates": _alias_candidates(),
        "endpoint_mode": endpoint_mode,
        "endpoint_base_redacted": redact_text(endpoint_base, env=values),
        "request_shape": {
            "api": "OpenAI ChatCompletionRequest",
            "method": "POST",
            "path": "/v1/chat/completions",
            "body_keys": ["model", "messages", "temperature", "max_tokens"],
            "model_field": "required",
            "workspace_sent": False,
            "private_paths_sent": False,
            "code_sent": False,
        },
        "credential_present_redacted": credential_present,
        "cloud_allowed_by_flag": values.get(CLOUD_ENABLE_ENV, "0") == "1",
        "cloud_provider_called": False,
        "workspace_sent": False,
        "private_paths_sent": False,
        "code_sent": False,
        "last_smoke_status": last_smoke_status,
        "last_smoke_timestamp": str(status.get("last_smoke_timestamp") or ""),
        "last_error_class": last_error_class,
        "route_diagnostic_status": route_status,
        "recommended_next_smoke": recommended_next_smoke,
        "recommended_next_action": _recommended_next_action(route_status, last_error_class),
        "model_list_api_status": model_list_status,
        "allow_model_list_requested": bool(allow_model_list),
        "official_references": [
            {
                "label": "NVIDIA API Reference",
                "url": "https://docs.api.nvidia.com/nim/reference/nvidia-llama-3_1-nemotron-ultra-253b-v1",
                "model_id": PRIMARY_MODEL,
            },
            {
                "label": "NVIDIA NIM LLM API Reference",
                "url": "https://docs.nvidia.com/nim/large-language-models/latest/reference/api-reference.html",
                "endpoint": "/v1/chat/completions",
            },
        ],
        "secret_values_printed": False,
        "publication_gate": PUBLICATION_GATE,
        "created_at": _now_iso(),
    }
    payload["secret_values_printed"] = _secret_values_printed(payload, values)
    return redact_mapping(payload, env=values)


def write_nvidia_route_diagnostic_artifact(runtime_root: str | Path, payload: dict[str, Any]) -> Path:
    runtime = Path(runtime_root)
    text = json.dumps(redact_mapping(payload), indent=2, ensure_ascii=False) + "\n"
    path = write_artifact(runtime / "outputs", "wabi_nvidia_route_diagnostic_v0_5", ".json", text)
    (runtime / "outputs" / "wabi_nvidia_route_diagnostic_latest.json").write_text(text, encoding="utf-8")
    return path


def _alias_candidates() -> list[dict[str, str]]:
    reasons = (
        "configured_primary_model_id",
        "api_reference_slug_variant",
        "provider_prefix_removed_variant",
        "provider_prefix_removed_slug_variant",
    )
    return [
        {
            "alias": alias,
            "status": "LOCAL_REVIEW_ONLY",
            "reason": reason,
        }
        for alias, reason in zip(ALIAS_CANDIDATES, reasons)
    ]


def _endpoint_mode(endpoint_base: str) -> str:
    normalized = endpoint_base.lower().strip()
    if not normalized:
        return "misconfigured"
    if "integrate.api.nvidia.com" in normalized and "/v1/chat/completions" in normalized:
        return "openai_compatible"
    if "/v1/chat/completions" in normalized or "/v1/responses" in normalized:
        return "openai_compatible"
    if "/v1/models" in normalized:
        return "nim"
    if normalized.startswith("sdk:"):
        return "sdk"
    return "unknown"


def _route_diagnostic_status(
    *,
    credential_present: bool,
    endpoint_mode: str,
    last_smoke_status: str,
    last_error_class: str,
) -> str:
    if not credential_present or endpoint_mode == "misconfigured":
        return "FAIL"
    if last_smoke_status == "SMOKE_PASS":
        return "PASS"
    if last_error_class == PROVIDER_OR_MODEL_NOT_FOUND:
        return "REVIEW"
    return "REVIEW"


def _recommended_next_action(route_status: str, last_error_class: str) -> str:
    if route_status == "PASS":
        return "ALLOW_SINGLE_ALIAS_SMOKE_RETRY_IF_OPERATOR_APPROVES"
    if last_error_class == PROVIDER_OR_MODEL_NOT_FOUND:
        return "NVIDIA_DASHBOARD_ROUTE_REVIEW_REDACTED"
    return "VERIFY_ENDPOINT_MODEL_ALIAS_ENTITLEMENT_REDACTED"


def _last_error_class(status: Mapping[str, Any]) -> str:
    text = json.dumps(status, ensure_ascii=False, default=str).lower()
    if "provider 404" in text or "not-found" in text or "not found" in text or "cloud_http_404" in text:
        return PROVIDER_OR_MODEL_NOT_FOUND
    if str(status.get("live_smoke_status") or "") == "SMOKE_FAIL_REDACTED":
        return PROVIDER_OR_MODEL_NOT_FOUND
    if str(status.get("live_smoke_status") or "") == "AUTH_REQUIRED_REDACTED":
        return "AUTH_REQUIRED_REDACTED"
    if str(status.get("live_smoke_status") or "") == "QUOTA_OR_BILLING_REVIEW":
        return "QUOTA_OR_BILLING_REVIEW"
    if str(status.get("live_smoke_status") or "") == "TIMEOUT_REVIEW":
        return "TIMEOUT_REVIEW"
    return "UNKNOWN_REDACTED"


def _read_latest_status(runtime_root: Path) -> dict[str, Any]:
    path = runtime_root / "outputs" / LATEST_STATUS_NAME
    if not path.exists():
        return _read_qa_status(None)
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return _read_qa_status(None)
    return payload if isinstance(payload, dict) else _read_qa_status(None)


def _read_qa_status(path: str | Path | None) -> dict[str, Any]:
    candidate = Path(path) if path else Path(__file__).resolve().parents[2] / "qa_artifacts" / "WABI_CLOUD_PROVIDER_v0_4_PROVIDER_STATUS.json"
    if not candidate.exists():
        return {}
    try:
        payload = json.loads(candidate.read_text(encoding="utf-8"))
    except Exception:
        return {}
    return payload if isinstance(payload, dict) else {}


def _active_nvidia_credential_env(env: Mapping[str, str]) -> str:
    for key in ("NVIDIA_NIM_API_KEY", "NVIDIA_API_KEY"):
        if env.get(key):
            return key
    return ""


def _secret_values_printed(payload: Any, env: Mapping[str, str]) -> bool:
    text = json.dumps(payload, ensure_ascii=False, default=str)
    for key, value in env.items():
        if value and len(value) >= 8 and is_sensitive_key(key) and value in text:
            return True
    return False


def _now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
