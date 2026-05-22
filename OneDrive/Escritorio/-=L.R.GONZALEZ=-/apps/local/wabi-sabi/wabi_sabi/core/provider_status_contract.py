from __future__ import annotations

import json
import os
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Mapping

from wabi_sabi.core.cloud_adapters import CLOUD_ENABLE_ENV, build_cloud_adapters
from wabi_sabi.core.redaction import is_sensitive_key, redact_mapping, redact_text
from wabi_sabi.core.tools import stamp, write_artifact


PRIMARY_PROVIDER = "nvidia"
PRIMARY_MODEL = "nvidia/nemotron-3-super-120b-a12b"
FALLBACK_PROVIDER = "ollama"
FALLBACK_MODEL = "qwen2.5:0.5b"
PUBLICATION_GATE = "BLOCK"
NVIDIA_CREDENTIAL_ENV_KEYS = ("NVIDIA_NIM_API_KEY", "NVIDIA_API_KEY")
SMOKE_PROMPT = 'Return exactly this JSON and nothing else:\n{"ok":true,"provider":"nvidia","smoke":"pass"}'
LATEST_STATUS_NAME = "wabi_provider_status_latest.json"
CONTRACT_SCHEMA = "wabi.provider_status_contract.v0_4"
LIVE_SMOKE_SCHEMA = "wabi.provider_live_smoke.v0_4"

ALLOWED_PROVIDER_STATES = {
    "NOT_CONFIGURED",
    "CONFIGURED_NOT_SMOKED",
    "REVIEW_SMOKE_NOT_RUN",
    "SMOKE_PASS",
    "SMOKE_FAIL_REDACTED",
    "AUTH_REQUIRED_REDACTED",
    "QUOTA_OR_BILLING_REVIEW",
    "CLOUD_DISABLED_BY_FLAG",
    "DRY_RUN_ONLY",
    "FALLBACK_LOCAL_ACTIVE",
    "TIMEOUT_REVIEW",
}


def build_provider_status_contract(
    *,
    runtime_root: str | Path,
    env: Mapping[str, str] | None = None,
) -> dict[str, Any]:
    values = os.environ if env is None else env
    runtime = Path(runtime_root)
    previous = _read_latest_status(runtime)
    cloud_allowed = values.get(CLOUD_ENABLE_ENV, "0") == "1"
    credential_env = _active_nvidia_credential_env(values)
    credential_present = bool(credential_env)
    last_smoke_status = str(previous.get("live_smoke_status") or "REVIEW_SMOKE_NOT_RUN")
    if last_smoke_status not in ALLOWED_PROVIDER_STATES:
        last_smoke_status = "REVIEW_SMOKE_NOT_RUN"
    last_smoke_timestamp = str(previous.get("last_smoke_timestamp") or "")
    if last_smoke_status in {"CLOUD_DISABLED_BY_FLAG", "NOT_CONFIGURED"}:
        last_smoke_timestamp = ""
        last_smoke_status = "REVIEW_SMOKE_NOT_RUN"

    provider_state = _effective_provider_state(
        cloud_allowed=cloud_allowed,
        credential_present=credential_present,
        live_smoke_status=last_smoke_status,
    )
    payload = {
        "schema": CONTRACT_SCHEMA,
        "primary_provider": PRIMARY_PROVIDER,
        "primary_model": PRIMARY_MODEL,
        "fallback_provider": FALLBACK_PROVIDER,
        "fallback_model": FALLBACK_MODEL,
        "cloud_allowed_by_flag": cloud_allowed,
        "cloud_allowed_mode": _cloud_allowed_mode(
            cloud_allowed=cloud_allowed,
            previous_mode=str(previous.get("cloud_allowed_mode") or ""),
            live_smoke_status=last_smoke_status,
        ),
        "cloud_enable_env": CLOUD_ENABLE_ENV,
        "credential_present_redacted": credential_present,
        "active_credential_env": credential_env,
        "live_smoke_status": last_smoke_status,
        "provider_state": provider_state,
        "last_smoke_timestamp": last_smoke_timestamp,
        "workspace_sent": False,
        "private_paths_sent": False,
        "code_sent": False,
        "secret_values_printed": False,
        "publication_gate": PUBLICATION_GATE,
    }
    payload["secret_values_printed"] = _secret_values_printed(payload, values)
    return redact_mapping(payload, env=values)


def run_nvidia_live_smoke(
    *,
    runtime_root: str | Path,
    env: Mapping[str, str] | None = None,
    timeout: int = 20,
    http_post: Callable[[str, dict[str, str], dict[str, Any], int], dict[str, Any]] | None = None,
) -> dict[str, Any]:
    values = dict(os.environ if env is None else env)
    runtime = Path(runtime_root)
    started = time.perf_counter()
    base = build_provider_status_contract(runtime_root=runtime, env=values)
    payload: dict[str, Any] = {
        "schema": LIVE_SMOKE_SCHEMA,
        "ok": False,
        "action": "provider_live_smoke",
        "provider": PRIMARY_PROVIDER,
        "model": PRIMARY_MODEL,
        "cloud_allowed_mode": "EPHEMERAL_SINGLE_SMOKE",
        "cloud_provider_called": False,
        "workspace_sent": False,
        "private_paths_sent": False,
        "code_sent": False,
        "prompt_contract": "minimal_json_only",
        "latency_ms": 0,
        "live_smoke_status": "REVIEW_SMOKE_NOT_RUN",
        "provider_status": base,
        "error": "",
        "secret_values_printed": False,
        "publication_gate": PUBLICATION_GATE,
    }

    if values.get(CLOUD_ENABLE_ENV, "0") != "1":
        return _finish_smoke(
            payload,
            runtime,
            status="CLOUD_DISABLED_BY_FLAG",
            error=f"{CLOUD_ENABLE_ENV}_not_enabled",
            started=started,
            env=values,
        )

    if not _active_nvidia_credential_env(values):
        return _finish_smoke(
            payload,
            runtime,
            status="NOT_CONFIGURED",
            error="nvidia_credential_missing",
            started=started,
            env=values,
        )

    smoke_env = dict(values)
    smoke_env.setdefault("WABI_NVIDIA_NIM_MODEL", PRIMARY_MODEL)
    smoke_env.setdefault("WABI_CLOUD_MAX_TOKENS", "64")
    smoke_env.setdefault("WABI_CLOUD_TEMPERATURE", "0")
    adapter = build_cloud_adapters(runtime_root=runtime, env=smoke_env, http_post=http_post)["nvidia-nim"]
    payload["cloud_provider_called"] = True
    result = adapter.execute(SMOKE_PROMPT, timeout=timeout, model=PRIMARY_MODEL)
    result_payload = result.to_dict()
    payload["provider_result"] = {
        "ok": result_payload.get("ok", False),
        "provider": result_payload.get("provider", "nvidia-nim"),
        "action": result_payload.get("action", ""),
        "gate": result_payload.get("gate", ""),
        "error": redact_text(str(result_payload.get("error", "")), env=smoke_env),
        "artifacts": result_payload.get("artifacts", []),
    }
    if not result.ok:
        return _finish_smoke(
            payload,
            runtime,
            status=_classify_provider_error(result.error or result.action),
            error=result.error or result.action,
            started=started,
            env=smoke_env,
        )

    parsed = _parse_exact_smoke_json(result.output)
    if parsed.get("ok") is True and parsed.get("provider") == "nvidia" and parsed.get("smoke") == "pass":
        payload["ok"] = True
        payload["response_json"] = parsed
        return _finish_smoke(payload, runtime, status="SMOKE_PASS", error="", started=started, env=smoke_env)

    return _finish_smoke(
        payload,
        runtime,
        status="SMOKE_FAIL_REDACTED",
        error="provider_response_did_not_match_smoke_contract",
        started=started,
        env=smoke_env,
    )


def write_provider_status_artifact(runtime_root: str | Path, payload: dict[str, Any]) -> Path:
    runtime = Path(runtime_root)
    text = json.dumps(redact_mapping(payload), indent=2, ensure_ascii=False) + "\n"
    path = write_artifact(runtime / "outputs", "wabi_provider_status_v0_4", ".json", text)
    latest = runtime / "outputs" / LATEST_STATUS_NAME
    latest.write_text(text, encoding="utf-8")
    return path


def _finish_smoke(
    payload: dict[str, Any],
    runtime: Path,
    *,
    status: str,
    error: str,
    started: float,
    env: Mapping[str, str],
) -> dict[str, Any]:
    payload["live_smoke_status"] = status if status in ALLOWED_PROVIDER_STATES else "SMOKE_FAIL_REDACTED"
    payload["latency_ms"] = int((time.perf_counter() - started) * 1000)
    payload["last_smoke_timestamp"] = _now_iso() if status not in {"CLOUD_DISABLED_BY_FLAG", "NOT_CONFIGURED"} else ""
    payload["error"] = redact_text(error, env=env)
    provider_status = build_provider_status_contract(runtime_root=runtime, env=env)
    provider_status["cloud_allowed_mode"] = payload.get("cloud_allowed_mode", provider_status.get("cloud_allowed_mode", ""))
    provider_status["live_smoke_status"] = payload["live_smoke_status"]
    provider_status["provider_state"] = payload["live_smoke_status"]
    provider_status["last_smoke_timestamp"] = payload["last_smoke_timestamp"]
    payload["provider_status"] = provider_status
    payload["secret_values_printed"] = _secret_values_printed(payload, env)
    payload = redact_mapping(payload, env=env)
    artifact = write_provider_status_artifact(runtime, payload)
    payload["provider_status_artifact"] = str(artifact)
    return payload


def _effective_provider_state(
    *,
    cloud_allowed: bool,
    credential_present: bool,
    live_smoke_status: str,
) -> str:
    if not cloud_allowed:
        return "CLOUD_DISABLED_BY_FLAG"
    if not credential_present:
        return "NOT_CONFIGURED"
    if live_smoke_status == "SMOKE_PASS":
        return "SMOKE_PASS"
    if live_smoke_status in {"SMOKE_FAIL_REDACTED", "AUTH_REQUIRED_REDACTED", "QUOTA_OR_BILLING_REVIEW", "TIMEOUT_REVIEW"}:
        return live_smoke_status
    return "CONFIGURED_NOT_SMOKED"


def _cloud_allowed_mode(*, cloud_allowed: bool, previous_mode: str, live_smoke_status: str) -> str:
    if cloud_allowed:
        return "SESSION_FLAG_ENABLED"
    if previous_mode.startswith("EPHEMERAL_SINGLE_SMOKE") and live_smoke_status not in {
        "REVIEW_SMOKE_NOT_RUN",
        "CLOUD_DISABLED_BY_FLAG",
        "NOT_CONFIGURED",
    }:
        return "EPHEMERAL_SINGLE_SMOKE_RECORDED"
    return "CLOUD_DISABLED_BY_FLAG"


def _read_latest_status(runtime_root: Path) -> dict[str, Any]:
    path = runtime_root / "outputs" / LATEST_STATUS_NAME
    if not path.exists():
        return {}
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}
    return payload if isinstance(payload, dict) else {}


def _active_nvidia_credential_env(env: Mapping[str, str]) -> str:
    for key in NVIDIA_CREDENTIAL_ENV_KEYS:
        if env.get(key):
            return key
    return ""


def _parse_exact_smoke_json(text: str) -> dict[str, Any]:
    try:
        payload = json.loads(str(text).strip())
    except json.JSONDecodeError:
        return {}
    return payload if isinstance(payload, dict) else {}


def _classify_provider_error(error: str) -> str:
    lowered = str(error).lower()
    if any(token in lowered for token in ("timeout", "timed out")):
        return "TIMEOUT_REVIEW"
    if any(token in lowered for token in ("401", "403", "unauthorized", "forbidden", "auth", "api key")):
        return "AUTH_REQUIRED_REDACTED"
    if any(token in lowered for token in ("402", "429", "quota", "billing", "payment", "insufficient")):
        return "QUOTA_OR_BILLING_REVIEW"
    return "SMOKE_FAIL_REDACTED"


def _secret_values_printed(payload: Any, env: Mapping[str, str]) -> bool:
    text = json.dumps(payload, ensure_ascii=False, default=str)
    for key, value in env.items():
        if value and len(value) >= 8 and is_sensitive_key(key) and value in text:
            return True
    return False


def _now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
