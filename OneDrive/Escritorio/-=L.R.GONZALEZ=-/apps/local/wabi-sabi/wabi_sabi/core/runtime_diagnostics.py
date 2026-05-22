from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import time
import urllib.error
import urllib.request
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

from wabi_sabi.core.config import APP_ROOT, DEFAULT_RUNTIME, RuntimeConfig
from wabi_sabi.core.user_config import CONFIG_PATH, ensure_user_config


SMOKE_PROMPT = "Reply exactly: WABI_PROVIDER_OK"
GLOBAL_BIN = Path.home() / ".medioevo" / "bin"
GLOBAL_SHIM = GLOBAL_BIN / "wabi.cmd"


@dataclass(frozen=True)
class ProviderDiagnostic:
    provider: str
    configured: bool
    auth_present: bool
    sdk_or_cli: str
    default_model: str
    smoke: str
    status: str
    reason: str
    repair_action: str
    active_env_key: str = ""
    base_url: str = ""
    smoke_model: str = ""
    coding_model: str = ""

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class CommandStatus:
    command: str
    available: bool
    path: str
    version: str = ""

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def build_provider_report(*, runtime_root: Path, smoke: bool = True, timeout: int = 20) -> dict[str, Any]:
    ensure_user_config()
    rows = [
        _ollama_diagnostic(smoke=smoke, timeout=timeout),
        _openai_compatible_diagnostic(
            provider="nvidia",
            env_keys=("NVIDIA_API_KEY", "NVIDIA_NIM_API_KEY", "NGC_API_KEY"),
            model=_env_first(("WABI_NVIDIA_NIM_MODEL", "NVIDIA_NIM_MODEL"), "nvidia/nemotron-3-super-120b-a12b"),
            base_url=_env_first(("NVIDIA_NIM_BASE_URL",), "https://integrate.api.nvidia.com/v1"),
            smoke=smoke,
            timeout=timeout,
        ),
        _anthropic_diagnostic(smoke=smoke, timeout=timeout),
        _gemini_diagnostic(smoke=smoke, timeout=timeout),
        _openai_compatible_diagnostic(
            provider="openai",
            env_keys=("OPENAI_API_KEY",),
            model=_env_first(("OPENAI_MODEL",), "gpt-5.4-mini"),
            base_url=_env_first(("OPENAI_BASE_URL",), "https://api.openai.com/v1"),
            smoke=smoke,
            timeout=timeout,
        ),
        _openai_compatible_diagnostic(
            provider="openrouter",
            env_keys=("OPENROUTER_API_KEY",),
            model=_env_first(("OPENROUTER_MODEL",), "openai/gpt-5-mini"),
            base_url=_env_first(("OPENROUTER_BASE_URL",), "https://openrouter.ai/api/v1"),
            smoke=smoke,
            timeout=timeout,
        ),
        _openai_compatible_diagnostic(
            provider="qwen",
            env_keys=("QWEN_API_KEY", "DASHSCOPE_API_KEY", "ALIBABA_CLOUD_API_KEY"),
            model=_env_first(("QWEN_MODEL", "WABI_QWEN_MODEL"), "qwen-plus"),
            base_url=_env_first(("QWEN_BASE_URL", "DASHSCOPE_BASE_URL", "WABI_QWEN_BASE_URL"), "https://dashscope.aliyuncs.com/compatible-mode/v1"),
            smoke=smoke,
            timeout=timeout,
        ),
        _openai_compatible_diagnostic(
            provider="dashscope_qwen",
            env_keys=("DASHSCOPE_API_KEY", "QWEN_API_KEY", "ALIBABA_CLOUD_API_KEY"),
            model=_env_first(("QWEN_MODEL", "WABI_QWEN_MODEL"), "qwen-plus"),
            base_url=_env_first(("DASHSCOPE_BASE_URL", "WABI_QWEN_BASE_URL"), "https://dashscope.aliyuncs.com/compatible-mode/v1"),
            smoke=smoke,
            timeout=timeout,
        ),
        _openai_compatible_diagnostic(
            provider="deepseek",
            env_keys=("DEEPSEEK_API_KEY",),
            model=_env_first(("DEEPSEEK_MODEL", "WABI_DEEPSEEK_MODEL"), "deepseek-chat"),
            base_url=_env_first(("DEEPSEEK_BASE_URL",), "https://api.deepseek.com/v1"),
            smoke=smoke,
            timeout=timeout,
        ),
        _openai_compatible_diagnostic(
            provider="openai_compatible",
            env_keys=("OPENAI_COMPATIBLE_API_KEY",),
            model=_env_first(("OPENAI_COMPATIBLE_MODEL",), "model-required"),
            base_url=_env_first(("OPENAI_COMPATIBLE_BASE_URL",), ""),
            smoke=smoke,
            timeout=timeout,
        ),
    ]
    runtime_root.mkdir(parents=True, exist_ok=True)
    return {
        "schema": "wabi.provider_matrix.v1",
        "smoke_prompt": SMOKE_PROMPT,
        "smoke_requested": smoke,
        "secret_values_printed": False,
        "providers": [row.to_dict() for row in rows],
        "runtime_root": str(runtime_root),
    }


def build_doctor_report(config: RuntimeConfig) -> dict[str, Any]:
    config_path = ensure_user_config()
    runtime_root = config.runtime_root
    runtime_root.mkdir(parents=True, exist_ok=True)
    output_dir = runtime_root / "outputs"
    log_dir = runtime_root / "logs"
    rollback_dir = runtime_root / "rollback"
    for path in (output_dir, log_dir, rollback_dir):
        path.mkdir(parents=True, exist_ok=True)

    providers = build_provider_report(runtime_root=runtime_root, smoke=False)
    bridges = {name: _command_status(name).to_dict() for name in ("codex", "claude", "claude-code", "opencode")}
    shim = _global_shim_status()
    where_wabi = _where("wabi")
    provider_statuses = [row["status"] for row in providers["providers"]]
    if any(status == "BLOCK" for status in provider_statuses):
        final = "BLOCK"
    elif any(status == "REVIEW" for status in provider_statuses):
        final = "REVIEW"
    else:
        final = "PASS"
    if not shim["path_in_user_path"] or not shim["exists"]:
        final = "REVIEW"

    return {
        "schema": "wabi.doctor.v1",
        "wabi_root": str(APP_ROOT),
        "python": {
            "executable": sys.executable,
            "version": sys.version.split()[0],
        },
        "version": _project_version(),
        "workspace": str(config.workspace),
        "runtime_root": str(runtime_root),
        "config_path": str(config_path),
        "repl": "READY",
        "coding_workflow": "plan_diff_apply_rollback",
        "runtime_writable": _can_write(runtime_root),
        "sandbox_status": "READY" if _can_write(config.workspace) else "REVIEW_NOT_WRITABLE",
        "rollback_dir": str(rollback_dir),
        "rollback_ready": _can_write(rollback_dir),
        "logs_dir": str(log_dir),
        "logs_ready": _can_write(log_dir),
        "global_shim": shim,
        "where_wabi": where_wabi,
        "providers": providers["providers"],
        "bridges": bridges,
        "latest_tests": _latest_test_hint(),
        "result": final,
        "secret_values_printed": False,
    }


def build_repair_report(config: RuntimeConfig, *, dry_run: bool = False) -> dict[str, Any]:
    config_path = ensure_user_config()
    actions: list[dict[str, Any]] = []
    real_cmd = APP_ROOT / "wabi.cmd"
    shim_text = _shim_text(real_cmd)
    path_before = _user_path()
    path_parts = _split_path(path_before)
    path_has_bin = _path_contains(path_parts, GLOBAL_BIN)

    actions.append({"action": "ensure_global_bin", "target": str(GLOBAL_BIN), "would_change": not GLOBAL_BIN.exists()})
    actions.append({"action": "write_shim", "target": str(GLOBAL_SHIM), "would_change": (not GLOBAL_SHIM.exists()) or GLOBAL_SHIM.read_text(encoding="utf-8", errors="replace") != shim_text if GLOBAL_SHIM.exists() else True})
    actions.append({"action": "prepend_user_path", "target": str(GLOBAL_BIN), "would_change": not path_has_bin})
    actions.append({"action": "ensure_user_config", "target": str(config_path), "would_change": False})
    for path in (config.runtime_root, config.output_dir, config.log_dir, config.memory_dir, config.runtime_root / "rollback"):
        actions.append({"action": "ensure_runtime_dir", "target": str(path), "would_change": not path.exists()})

    if not dry_run:
        GLOBAL_BIN.mkdir(parents=True, exist_ok=True)
        GLOBAL_SHIM.write_text(shim_text, encoding="utf-8", newline="\r\n")
        for path in (config.runtime_root, config.output_dir, config.log_dir, config.memory_dir, config.runtime_root / "rollback"):
            path.mkdir(parents=True, exist_ok=True)
        if not path_has_bin:
            _set_user_path(";".join([str(GLOBAL_BIN), *path_parts]))
        current_parts = _split_path(os.environ.get("PATH", ""))
        if not _path_contains(current_parts, GLOBAL_BIN):
            os.environ["PATH"] = str(GLOBAL_BIN) + os.pathsep + os.environ.get("PATH", "")

    return {
        "schema": "wabi.repair.v1",
        "dry_run": dry_run,
        "real_cmd": str(real_cmd),
        "shim": str(GLOBAL_SHIM),
        "config": str(config_path),
        "actions": actions,
        "path_updated": (not dry_run and not path_has_bin),
        "secret_values_printed": False,
        "result": "DRY_RUN" if dry_run else "PASS",
    }


def build_debug_bundle(config: RuntimeConfig, *, dry_run: bool = False) -> dict[str, Any]:
    bundle_dir = config.runtime_root / "debug" / time.strftime("wabi_debug_%Y%m%d_%H%M%S")
    if dry_run:
        return {
            "schema": "wabi.debug_bundle.v1",
            "dry_run": True,
            "bundle_dir": str(bundle_dir),
            "would_include": ["doctor.json", "providers.json", "bridges.json", "README.md"],
            "secret_values_printed": False,
            "result": "DRY_RUN",
        }
    bundle_dir.mkdir(parents=True, exist_ok=True)
    doctor = build_doctor_report(config)
    providers = build_provider_report(runtime_root=config.runtime_root, smoke=False)
    bridges = {name: _command_status(name).to_dict() for name in ("codex", "claude", "claude-code", "opencode")}
    (bundle_dir / "doctor.json").write_text(json.dumps(doctor, indent=2, ensure_ascii=False), encoding="utf-8")
    (bundle_dir / "providers.json").write_text(json.dumps(providers, indent=2, ensure_ascii=False), encoding="utf-8")
    (bundle_dir / "bridges.json").write_text(json.dumps(bridges, indent=2, ensure_ascii=False), encoding="utf-8")
    (bundle_dir / "README.md").write_text(
        "# Wabi Debug Bundle\n\nSanitized local diagnostics. No .env files, key values, private books, RPG/TCG, DUAT private material or source vaults are included.\n",
        encoding="utf-8",
    )
    return {
        "schema": "wabi.debug_bundle.v1",
        "dry_run": False,
        "bundle_dir": str(bundle_dir),
        "files": [str(path) for path in sorted(bundle_dir.iterdir())],
        "secret_values_printed": False,
        "result": "PASS",
    }


def format_provider_report(payload: dict[str, Any]) -> str:
    rows = payload.get("providers", [])
    lines = [
        "WABI PROVIDERS",
        "Secret values printed: NO",
        "",
        "provider | configured | auth_present | base_url | smoke_model | coding_model | smoke | status | reason | repair_action",
        "---|---:|---:|---|---|---|---|---|---|---",
    ]
    for row in rows:
        lines.append(
            "{provider} | {configured} | {auth_present} | {base_url} | {smoke_model} | {coding_model} | {smoke} | {status} | {reason} | {repair_action}".format(
                **row
            )
        )
    return "\n".join(lines)


def format_doctor_report(payload: dict[str, Any]) -> str:
    shim = payload["global_shim"]
    bridges = payload["bridges"]
    lines = [
        "WABI DOCTOR",
        f"Result: {payload['result']}",
        f"Wabi root: {payload['wabi_root']}",
        f"Python: {payload['python']['version']} ({payload['python']['executable']})",
        f"Version: {payload['version']}",
        f"Config: {payload['config_path']}",
        f"REPL: {payload['repl']}  Coding: {payload['coding_workflow']}",
        f"Runtime: {payload['runtime_root']} writable={payload['runtime_writable']}",
        f"Workspace: {payload['workspace']} status={payload['sandbox_status']}",
        f"Rollback: {payload['rollback_dir']} ready={payload['rollback_ready']}",
        f"Logs: {payload['logs_dir']} ready={payload['logs_ready']}",
        f"Shim: {shim['path']} exists={shim['exists']} user_path={shim['path_in_user_path']}",
        f"where wabi: {payload['where_wabi'] or 'NOT_FOUND'}",
        "",
        "Providers:",
    ]
    for row in payload["providers"]:
        lines.append(f"- {row['provider']}: {row['status']} smoke={row['smoke']} reason={row['reason']}")
    lines.append("")
    lines.append("Bridges:")
    for name, status in bridges.items():
        lines.append(f"- {name}: {'OK' if status['available'] else 'NO'} {status.get('version', '')}".rstrip())
    lines.append("")
    lines.append(f"Latest tests: {payload['latest_tests']}")
    lines.append("Secret values printed: NO")
    return "\n".join(lines)


def format_repair_report(payload: dict[str, Any]) -> str:
    lines = [
        "WABI REPAIR",
        f"Result: {payload['result']}",
        f"Dry run: {payload['dry_run']}",
        f"Shim: {payload['shim']}",
        f"Real cmd: {payload['real_cmd']}",
        "Actions:",
    ]
    for action in payload["actions"]:
        lines.append(f"- {action['action']}: {action['target']} would_change={action['would_change']}")
    lines.append("Secret values printed: NO")
    return "\n".join(lines)


def format_debug_report(payload: dict[str, Any]) -> str:
    lines = [
        "WABI DEBUG",
        f"Result: {payload['result']}",
        f"Dry run: {payload['dry_run']}",
        f"Bundle: {payload['bundle_dir']}",
        "Secret values printed: NO",
    ]
    if payload.get("files"):
        lines.append("Files:")
        lines.extend(f"- {item}" for item in payload["files"])
    return "\n".join(lines)


def _ollama_diagnostic(*, smoke: bool, timeout: int) -> ProviderDiagnostic:
    host = _env_first(("OLLAMA_HOST",), "http://127.0.0.1:11434").rstrip("/")
    if not host.startswith(("http://", "https://")):
        host = "http://" + host
    coding_model = _env_first(("WABI_OLLAMA_CODING_MODEL", "WABI_OLLAMA_MODEL", "BASE_MODEL", "WABI_BASE_MODEL", "WABI_OLLAMA_BASE_MODEL", "OLLAMA_MODEL"), "qwen2.5-coder:3b")
    configured_smoke_model = _env_first(("WABI_OLLAMA_SMOKE_MODEL",), "")
    cli = _command_status("ollama")
    tags: dict[str, Any] = {}
    try:
        tags = _get_json(host + "/api/tags", 5)
    except Exception:
        pass
    models = [item.get("name", "") for item in tags.get("models", []) if isinstance(item, dict)]
    available = bool(models)
    configured = True
    reason = "endpoint_healthy" if available else "OLLAMA_SERVICE_NOT_RUNNING_OR_NO_MODELS"
    smoke_status = "SKIPPED"
    status = "PASS" if available else "REVIEW"
    if smoke and available:
        selected = configured_smoke_model if configured_smoke_model in models else _choose_ollama_smoke_model(models, coding_model)
        try:
            output = _ollama_generate(host, selected, timeout)
            if output.strip() == "WABI_PROVIDER_OK":
                smoke_status = "PASS"
                status = "PASS"
                reason = f"smoke_model_ok:{selected}; coding_model={coding_model}"
            else:
                smoke_status = "FAIL"
                status = "REVIEW"
                reason = f"LOCAL_SMOKE_MODEL_NON_EXACT:{selected}; coding_model={coding_model}"
        except Exception as exc:
            smoke_status = "FAIL"
            status = "REVIEW"
            reason = _classify_error(exc)
            fast_candidate = _choose_ollama_smoke_model(models, coding_model)
            if selected != fast_candidate and fast_candidate in models:
                try:
                    fallback_output = _ollama_generate(host, fast_candidate, min(timeout, 30))
                    if fallback_output.strip() == "WABI_PROVIDER_OK":
                        smoke_status = "PASS"
                        status = "PASS"
                        reason = f"SMOKE_MODEL_FALLBACK_PASS:{fast_candidate}; coding_model={coding_model}; original={reason}"
                    else:
                        reason = f"SMOKE_MODEL_FALLBACK_NON_EXACT:{fast_candidate}; coding_model={coding_model}; original={reason}"
                except Exception as fallback_exc:
                    reason = f"SMOKE_MODEL_FALLBACK_FAILED:{_classify_error(fallback_exc)}; coding_model={coding_model}; original={reason}"
    smoke_model = configured_smoke_model if configured_smoke_model in models else (_choose_ollama_smoke_model(models, coding_model) if models else configured_smoke_model or coding_model)
    return ProviderDiagnostic(
        provider="local/ollama",
        configured=configured,
        auth_present=False,
        sdk_or_cli="YES" if cli.available or available else "NO",
        default_model=coding_model,
        smoke=smoke_status,
        status=status,
        reason=reason,
        repair_action=(
            "No repair needed."
            if status == "PASS"
            else "Start Ollama or run a small existing model; do not download large models automatically."
        ),
        active_env_key="OLLAMA_HOST" if os.environ.get("OLLAMA_HOST") else "",
        base_url=host,
        smoke_model=smoke_model,
        coding_model=coding_model,
    )


def _openai_compatible_diagnostic(
    *,
    provider: str,
    env_keys: tuple[str, ...],
    model: str,
    base_url: str,
    smoke: bool,
    timeout: int,
) -> ProviderDiagnostic:
    active = _active_env_key(env_keys)
    if not active:
        empty = _empty_env_key(env_keys)
        reason = "EMPTY_ENV" if empty else "MISSING_ENV"
        repair = f"Set a non-empty value for: {empty}" if empty else f"Set one of: {', '.join(env_keys)}"
        return ProviderDiagnostic(
            provider=provider,
            configured=False,
            auth_present=bool(empty),
            sdk_or_cli="YES",
            default_model=model,
            smoke="SKIPPED",
            status="NOT_CONFIGURED",
            reason=reason,
            repair_action=repair,
            base_url=base_url,
            smoke_model=model,
            coding_model=model,
        )
    smoke_status = "SKIPPED"
    status = "REVIEW"
    reason = "SMOKE_NOT_RUN"
    if smoke:
        try:
            output = _call_openai_compatible(base_url, os.environ[active], model, timeout)
            if output.strip() == "WABI_PROVIDER_OK":
                smoke_status = "PASS"
                status = "PASS"
                reason = "OK"
            else:
                smoke_status = "FAIL"
                status = "REVIEW"
                reason = "NON_EXACT_SMOKE_RESPONSE"
        except Exception as exc:
            smoke_status = "FAIL"
            status = "REVIEW"
            reason = _classify_error(exc)
            if provider == "deepseek" and reason == "UNKNOWN_DEGRADED":
                detail = debug_deepseek_provider(timeout=timeout)
                reason = str(detail.get("classification") or reason)
    return ProviderDiagnostic(
        provider=provider,
        configured=True,
        auth_present=True,
        sdk_or_cli="YES",
        default_model=model,
        smoke=smoke_status,
        status=status,
        reason=reason,
        repair_action=_repair_action_for_reason(reason, env_keys, model),
        active_env_key=active,
        base_url=base_url,
        smoke_model=model,
        coding_model=model,
    )


def _anthropic_diagnostic(*, smoke: bool, timeout: int) -> ProviderDiagnostic:
    active = _active_env_key(("ANTHROPIC_API_KEY",))
    model = _env_first(("ANTHROPIC_MODEL",), "claude-sonnet-4-5")
    if not active:
        return ProviderDiagnostic("anthropic", False, False, "YES", model, "SKIPPED", "NOT_CONFIGURED", "MISSING_ENV", "Set ANTHROPIC_API_KEY")
    smoke_status = "SKIPPED"
    status = "REVIEW"
    reason = "SMOKE_NOT_RUN"
    if smoke:
        try:
            output = _call_anthropic(os.environ[active], model, timeout)
            if output.strip() == "WABI_PROVIDER_OK":
                smoke_status = "PASS"
                status = "PASS"
                reason = "OK"
            else:
                smoke_status = "FAIL"
                status = "REVIEW"
                reason = "NON_EXACT_SMOKE_RESPONSE"
        except Exception as exc:
            smoke_status = "FAIL"
            status = "REVIEW"
            reason = _classify_error(exc)
    return ProviderDiagnostic("anthropic", True, True, "YES", model, smoke_status, status, reason, _repair_action_for_reason(reason, ("ANTHROPIC_API_KEY",), model), active)


def _gemini_diagnostic(*, smoke: bool, timeout: int) -> ProviderDiagnostic:
    active = _active_env_key(("GOOGLE_API_KEY", "GEMINI_API_KEY"))
    model = _env_first(("GEMINI_MODEL", "GOOGLE_MODEL"), "gemini-2.5-flash")
    if not active:
        return ProviderDiagnostic("gemini", False, False, "YES", model, "SKIPPED", "NOT_CONFIGURED", "MISSING_ENV", "Set GOOGLE_API_KEY or GEMINI_API_KEY")
    smoke_status = "SKIPPED"
    status = "REVIEW"
    reason = "SMOKE_NOT_RUN"
    if smoke:
        try:
            output = _call_gemini(os.environ[active], model, timeout)
            if output.strip() == "WABI_PROVIDER_OK":
                smoke_status = "PASS"
                status = "PASS"
                reason = "OK"
            else:
                smoke_status = "FAIL"
                status = "REVIEW"
                reason = "NON_EXACT_SMOKE_RESPONSE"
        except Exception as exc:
            smoke_status = "FAIL"
            status = "REVIEW"
            reason = _classify_error(exc)
    return ProviderDiagnostic("gemini", True, True, "YES", model, smoke_status, status, reason, _repair_action_for_reason(reason, ("GOOGLE_API_KEY", "GEMINI_API_KEY"), model), active)


def _call_openai_compatible(base_url: str, api_key: str, model: str, timeout: int) -> str:
    url = base_url.rstrip("/")
    if not url.endswith("/chat/completions"):
        url += "/chat/completions"
    response = _post_json(
        url,
        {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        {
            "model": model,
            "messages": [
                {
                    "role": "system",
                    "content": (
                        "Eres un proveedor conectado por Wabi-Sabi. Responde de forma breve, "
                        "no pidas secretos, no reveles credenciales, y no afirmes que ejecutaste cambios locales."
                    ),
                },
                {"role": "user", "content": SMOKE_PROMPT},
            ],
            "temperature": 0.2,
            "max_tokens": 512,
        },
        timeout,
    )
    return _extract_openai_text(response)


def _call_anthropic(api_key: str, model: str, timeout: int) -> str:
    response = _post_json(
        "https://api.anthropic.com/v1/messages",
        {
            "Content-Type": "application/json",
            "x-api-key": api_key,
            "anthropic-version": "2023-06-01",
        },
        {
            "model": model,
            "system": "Return exactly WABI_PROVIDER_OK and nothing else.",
            "messages": [{"role": "user", "content": SMOKE_PROMPT}],
            "max_tokens": 32,
            "temperature": 0,
        },
        timeout,
    )
    return "\n".join(item.get("text", "") for item in response.get("content", []) if isinstance(item, dict)).strip()


def _call_gemini(api_key: str, model: str, timeout: int) -> str:
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
    response = _post_json(
        url,
        {"Content-Type": "application/json"},
        {
            "systemInstruction": {"parts": [{"text": "Return exactly WABI_PROVIDER_OK and nothing else."}]},
            "contents": [{"parts": [{"text": SMOKE_PROMPT}]}],
            "generationConfig": {"temperature": 0, "maxOutputTokens": 32},
        },
        timeout,
    )
    chunks: list[str] = []
    for candidate in response.get("candidates", []):
        for part in candidate.get("content", {}).get("parts", []):
            if isinstance(part, dict) and isinstance(part.get("text"), str):
                chunks.append(part["text"])
    return "\n".join(chunks).strip()


def _ollama_generate(host: str, model: str, timeout: int) -> str:
    response = _post_json(
        host.rstrip("/") + "/api/generate",
        {"Content-Type": "application/json"},
        {
            "model": model,
            "prompt": "Return only WABI_PROVIDER_OK. Do not explain.",
            "stream": False,
            "options": {"temperature": 0, "num_predict": 12},
        },
        timeout,
    )
    return str(response.get("response") or "").strip()


def debug_deepseek_provider(*, timeout: int = 20) -> dict[str, Any]:
    env_key = "DEEPSEEK_API_KEY"
    base_url = _env_first(("DEEPSEEK_BASE_URL",), "https://api.deepseek.com/v1").rstrip("/")
    model = _env_first(("DEEPSEEK_MODEL", "WABI_DEEPSEEK_MODEL"), "deepseek-chat")
    if env_key not in os.environ:
        return _debug_payload("MISSING_ENV", base_url=base_url, model=model, auth_present=False)
    if not os.environ.get(env_key):
        return _debug_payload("EMPTY_ENV", base_url=base_url, model=model, auth_present=False)
    if not base_url.startswith(("http://", "https://")):
        return _debug_payload("BAD_BASE_URL", base_url=base_url, model=model, auth_present=True)

    api_key = os.environ[env_key]
    models_probe = _probe_json_endpoint(base_url + "/models", api_key=api_key, timeout=timeout, method="GET")
    chat_probe = _probe_json_endpoint(
        base_url + "/chat/completions",
        api_key=api_key,
        timeout=timeout,
        method="POST",
        body={
            "model": model,
            "messages": [{"role": "user", "content": SMOKE_PROMPT}],
            "temperature": 0,
            "max_tokens": 32,
        },
    )
    classification = _classify_probe(chat_probe)
    if chat_probe.get("ok") and _extract_openai_text(chat_probe.get("json", {})).strip() == "WABI_PROVIDER_OK":
        classification = "PASS"
    elif chat_probe.get("ok"):
        classification = "BAD_RESPONSE_FORMAT"
    return {
        "schema": "wabi.deepseek_debug.v1",
        "provider": "deepseek",
        "auth_present": True,
        "base_url": base_url,
        "model": model,
        "models_endpoint": _public_probe_summary(models_probe),
        "chat_endpoint": _public_probe_summary(chat_probe),
        "classification": classification,
        "secret_values_printed": False,
    }


def format_deepseek_debug(payload: dict[str, Any]) -> str:
    models = payload.get("models_endpoint", {})
    chat = payload.get("chat_endpoint", {})
    lines = [
        "# DeepSeek Debug",
        "",
        f"provider: {payload.get('provider', 'deepseek')}",
        f"auth_present: {'YES' if payload.get('auth_present') else 'NO'}",
        f"base_url: {payload.get('base_url')}",
        f"model: {payload.get('model')}",
        f"classification: {payload.get('classification')}",
        "secret_values_printed: NO",
        "",
        "## /models",
        f"- status_code: {models.get('status_code', 'N/A')}",
        f"- error_type: {models.get('error_type', '')}",
        f"- error_code: {models.get('error_code', '')}",
        "",
        "## /chat/completions",
        f"- status_code: {chat.get('status_code', 'N/A')}",
        f"- error_type: {chat.get('error_type', '')}",
        f"- error_code: {chat.get('error_code', '')}",
        f"- expected_format: {chat.get('expected_format', False)}",
    ]
    return "\n".join(lines)


def _post_json(url: str, headers: dict[str, str], body: dict[str, Any], timeout: int) -> dict[str, Any]:
    request = urllib.request.Request(url, data=json.dumps(body).encode("utf-8"), headers=headers, method="POST")
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")[-1000:]
        raise RuntimeError(f"http_{exc.code}:{_sanitize_error(detail)}") from exc


def _probe_json_endpoint(
    url: str,
    *,
    api_key: str,
    timeout: int,
    method: str,
    body: dict[str, Any] | None = None,
) -> dict[str, Any]:
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    data = json.dumps(body or {}).encode("utf-8") if method == "POST" else None
    request = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            text = response.read().decode("utf-8", errors="replace")
            parsed = json.loads(text) if text.strip() else {}
            return {"ok": True, "status_code": response.status, "json": parsed, "expected_format": isinstance(parsed, dict)}
    except urllib.error.HTTPError as exc:
        raw = exc.read().decode("utf-8", errors="replace")[-1500:]
        parsed_error = _extract_error_public_fields(raw)
        return {
            "ok": False,
            "status_code": exc.code,
            "error_type": _classify_error(RuntimeError(raw)),
            "error_code": parsed_error.get("code", ""),
            "message_hint": parsed_error.get("type", ""),
            "expected_format": False,
        }
    except Exception as exc:
        return {
            "ok": False,
            "status_code": "",
            "error_type": _classify_error(exc),
            "error_code": "",
            "expected_format": False,
        }


def _extract_error_public_fields(text: str) -> dict[str, str]:
    try:
        data = json.loads(text)
    except Exception:
        return {"code": "", "type": ""}
    error = data.get("error", data) if isinstance(data, dict) else {}
    if not isinstance(error, dict):
        return {"code": "", "type": ""}
    return {
        "code": str(error.get("code", ""))[:80],
        "type": str(error.get("type", ""))[:80],
    }


def _public_probe_summary(probe: dict[str, Any]) -> dict[str, Any]:
    return {
        "ok": bool(probe.get("ok")),
        "status_code": probe.get("status_code", ""),
        "error_type": probe.get("error_type", ""),
        "error_code": probe.get("error_code", ""),
        "expected_format": bool(probe.get("expected_format")),
    }


def _classify_probe(probe: dict[str, Any]) -> str:
    if probe.get("ok"):
        return "PASS"
    status_code = str(probe.get("status_code", ""))
    error_type = str(probe.get("error_type", ""))
    if error_type:
        return error_type
    if status_code in {"401", "403"}:
        return "AUTH_FAILED"
    if status_code == "404":
        return "MODEL_NOT_FOUND"
    if status_code == "429":
        return "QUOTA_OR_BILLING"
    if status_code in {"400", "422"}:
        return "BAD_RESPONSE_FORMAT"
    if status_code.startswith("5"):
        return "NETWORK_ERROR"
    return "UNKNOWN_DEGRADED"


def _debug_payload(classification: str, *, base_url: str, model: str, auth_present: bool) -> dict[str, Any]:
    return {
        "schema": "wabi.deepseek_debug.v1",
        "provider": "deepseek",
        "auth_present": auth_present,
        "base_url": base_url,
        "model": model,
        "models_endpoint": {},
        "chat_endpoint": {},
        "classification": classification,
        "secret_values_printed": False,
    }


def _get_json(url: str, timeout: int) -> dict[str, Any]:
    request = urllib.request.Request(url, method="GET")
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return json.loads(response.read().decode("utf-8"))


def _extract_openai_text(response: dict[str, Any]) -> str:
    chunks: list[str] = []
    for choice in response.get("choices", []) or []:
        message = choice.get("message") or {}
        content = message.get("content")
        if isinstance(content, str):
            chunks.append(content)
        elif isinstance(content, list):
            chunks.extend(str(item.get("text", "")) for item in content if isinstance(item, dict))
        if isinstance(choice.get("text"), str):
            chunks.append(choice["text"])
    return "\n".join(item.strip() for item in chunks if item.strip()).strip()


def _classify_error(exc: Exception) -> str:
    text = _sanitize_error(str(exc)).lower()
    if (
        "401" in text
        or "403" in text
        or "unauthorized" in text
        or "permission" in text
        or "api key" in text
        or "invalid_api_key" in text
        or "invalid api key" in text
        or "authentication" in text
    ):
        return "AUTH_FAILED"
    if "quota" in text or "billing" in text or "429" in text or "rate" in text or "balance" in text or "credit" in text:
        return "QUOTA_OR_BILLING"
    if "model" in text and ("not found" in text or "404" in text or "not_found" in text):
        return "MODEL_NOT_FOUND"
    if "404" in text or "not found" in text:
        return "BAD_BASE_URL"
    if "400" in text or "422" in text or "bad request" in text or "invalid_request" in text:
        return "BAD_RESPONSE_FORMAT"
    if "timed out" in text or "timeout" in text or "name resolution" in text or "connection" in text:
        return "NETWORK_ERROR"
    if "no module" in text or "import" in text:
        return "SDK_IMPORT_ERROR"
    return "UNKNOWN_DEGRADED"


def _choose_ollama_smoke_model(models: list[str], coding_model: str) -> str:
    if not models:
        return coding_model
    preferred = ["qwen2.5:0.5b", "gemma:2b", "llama3.2:1b", "phi3:mini"]
    for name in preferred:
        if name in models:
            return name
    small_markers = ("0.5b", "1b", "1.5b", "2b", "mini", "tiny")
    for name in models:
        if name != coding_model and any(marker in name.lower() for marker in small_markers):
            return name
    for name in models:
        if name != coding_model:
            return name
    return models[0]


def _repair_action_for_reason(reason: str, env_keys: tuple[str, ...], model: str) -> str:
    if reason == "OK":
        return "No repair needed."
    if reason == "MISSING_ENV":
        return f"Set one of: {', '.join(env_keys)}"
    if reason == "AUTH_FAILED":
        return "Review/rotate key outside logs; do not print value."
    if reason == "QUOTA_OR_BILLING":
        return "Check provider quota/billing in provider console."
    if reason == "MODEL_NOT_FOUND":
        return f"Set supported model env for provider; current default: {model}"
    if reason == "NETWORK_ERROR":
        return "Check network/provider endpoint and retry one smoke."
    if reason == "NON_EXACT_SMOKE_RESPONSE":
        return "Provider responded but not exact smoke; inspect parser/model behavior."
    return "No automatic repair; keep REVIEW with sanitized diagnostics."


def _sanitize_error(text: str) -> str:
    sanitized = text
    for key in ("sk-", "ghp_", "nvapi-", "Bearer ", "x-api-key", "key="):
        if key in sanitized:
            sanitized = sanitized.split(key)[0] + "[REDACTED]"
    return sanitized[-500:]


def _env_first(keys: tuple[str, ...], default: str) -> str:
    for key in keys:
        value = os.environ.get(key)
        if value:
            return value
    return default


def _active_env_key(keys: tuple[str, ...]) -> str:
    for key in keys:
        if os.environ.get(key):
            return key
    return ""


def _empty_env_key(keys: tuple[str, ...]) -> str:
    for key in keys:
        if key in os.environ and not os.environ.get(key):
            return key
    return ""


def _command_status(command: str) -> CommandStatus:
    path = shutil.which(command) or ""
    version = "not_checked" if path else ""
    if path and os.environ.get("WABI_DOCTOR_CHECK_VERSIONS", "").strip() == "1":
        try:
            if os.name == "nt" and path.lower().endswith((".cmd", ".bat")):
                proc = subprocess.run(f'"{path}" --version', capture_output=True, text=True, timeout=2, shell=True)
            else:
                proc = subprocess.run([path, "--version"], capture_output=True, text=True, timeout=2)
            version = (proc.stdout or proc.stderr).strip().splitlines()[0] if (proc.stdout or proc.stderr).strip() else ""
        except Exception:
            version = "version_check_failed"
    return CommandStatus(command=command, available=bool(path), path=path, version=version)


def _where(command: str) -> str:
    if os.name == "nt":
        try:
            proc = subprocess.run(["where.exe", command], capture_output=True, text=True, timeout=2)
            return "; ".join(line.strip() for line in proc.stdout.splitlines() if line.strip())
        except Exception:
            return shutil.which(command) or ""
    return shutil.which(command) or ""


def _project_version() -> str:
    pyproject = APP_ROOT / "pyproject.toml"
    if not pyproject.exists():
        return "unknown"
    for line in pyproject.read_text(encoding="utf-8", errors="replace").splitlines():
        if line.strip().startswith("version"):
            return line.split("=", 1)[1].strip().strip('"')
    return "unknown"


def _latest_test_hint() -> str:
    report = APP_ROOT / "TEST_REPORT.md"
    if report.exists():
        try:
            lines = [line.strip() for line in report.read_text(encoding="utf-8", errors="replace").splitlines() if "passed" in line.lower() or "PASS" in line]
            return lines[-1] if lines else str(report)
        except Exception:
            return str(report)
    return "not_found"


def _can_write(path: Path) -> bool:
    try:
        path.mkdir(parents=True, exist_ok=True)
        probe = path / ".wabi_write_probe"
        probe.write_text("ok", encoding="utf-8")
        probe.unlink(missing_ok=True)
        return True
    except Exception:
        return False


def _global_shim_status() -> dict[str, Any]:
    user_parts = _split_path(_user_path())
    return {
        "path": str(GLOBAL_SHIM),
        "exists": GLOBAL_SHIM.exists(),
        "bin": str(GLOBAL_BIN),
        "path_in_user_path": _path_contains(user_parts, GLOBAL_BIN),
        "current_which": shutil.which("wabi") or "",
    }


def _shim_text(real_cmd: Path) -> str:
    return f"""@echo off
setlocal
set "WABI_REAL={real_cmd}"
if exist "%WABI_REAL%" (
  call "%WABI_REAL%" %*
  exit /b %ERRORLEVEL%
)
set "WABI_ALT=%USERPROFILE%\\OneDrive\\Escritorio\\-=L.R.GONZALEZ=-\\apps\\local\\wabi-sabi\\wabi.cmd"
if exist "%WABI_ALT%" (
  call "%WABI_ALT%" %*
  exit /b %ERRORLEVEL%
)
echo Wabi-Sabi real CLI not found. Expected: %WABI_REAL%
exit /b 2
"""


def _user_path() -> str:
    if os.name != "nt":
        return os.environ.get("PATH", "")
    try:
        import winreg

        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Environment", 0, winreg.KEY_READ) as key:
            value, _ = winreg.QueryValueEx(key, "Path")
            return str(value)
    except Exception:
        return os.environ.get("PATH", "")


def _set_user_path(value: str) -> None:
    if os.name != "nt":
        return
    import winreg

    with winreg.CreateKeyEx(winreg.HKEY_CURRENT_USER, "Environment", 0, winreg.KEY_SET_VALUE) as key:
        winreg.SetValueEx(key, "Path", 0, winreg.REG_EXPAND_SZ, value)


def _split_path(value: str) -> list[str]:
    return [part for part in value.split(os.pathsep) if part.strip()]


def _path_contains(parts: list[str], target: Path) -> bool:
    target_text = str(target).rstrip("\\/").lower()
    return any(part.rstrip("\\/").lower() == target_text for part in parts)
