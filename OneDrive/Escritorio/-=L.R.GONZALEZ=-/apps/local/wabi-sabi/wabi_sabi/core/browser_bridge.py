from __future__ import annotations

import hashlib
import http.client
import json
import os
import re
import shutil
import urllib.error
import urllib.request
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Callable
from urllib.parse import urlparse

from wabi_sabi.core.browser_gate import evaluate_browser_request
from wabi_sabi.core.cloud_code_proposal import (
    extract_cloud_code_proposal_payload,
    validate_cloud_code_proposal,
    write_cloud_proposal_artifact,
)
from wabi_sabi.core.browser_bridge_selector_pack import (
    BROWSER_BRIDGE_ENABLE_ENV as SELECTOR_BROWSER_BRIDGE_ENABLE_ENV,
    BROWSER_SEND_ENABLE_ENV as SELECTOR_BROWSER_SEND_ENABLE_ENV,
    KIMI_WEBBRIDGE_URL_ENV as SELECTOR_KIMI_WEBBRIDGE_URL_ENV,
    PUBLIC_PROMPT,
    SNAPSHOT_READONLY,
    build_selector_pack_status,
    is_safe_local_url,
    rank_browser_council_services,
    select_browser_bridge_backend,
)
from wabi_sabi.core.redaction import redact_mapping, redact_text
from wabi_sabi.core.tools import write_artifact


BROWSER_ACTION_SCHEMA = "wabi.browser_action.v0_1"
BROWSER_OBSERVATION_SCHEMA = "wabi.browser_observation.v0_1"
BROWSER_BRIDGE_STATUS_SCHEMA = "wabi.browser_bridge_status.v0_1"
BROWSER_AI_CONSULTATION_SCHEMA = "wabi.browser_ai_consultation.v0_1"
BROWSER_COUNCIL_SCHEMA = "wabi.browser_council.v0_1"
BROWSER_KIMI_SMOKE_SCHEMA = "wabi.browser_bridge_kimi_smoke.v0_2"
BROWSER_DEVTOOLS_READONLY_SCHEMA = "wabi.browser_bridge_devtools_readonly.v0_2"
BROWSER_RESPONSE_PROPOSAL_SCHEMA = "wabi.browser_response_to_proposal.v0_2"
BROWSER_BRIDGE_ENABLE_ENV = "WABI_ALLOW_BROWSER_BRIDGE"
BROWSER_SEND_ENABLE_ENV = "WABI_ALLOW_BROWSER_SEND"
KIMI_WEBBRIDGE_URL_ENV = "WABI_KIMI_WEBBRIDGE_URL"
KIMI_SMOKE_PROMPT = 'Return exactly this JSON:\n{"ok":true,"service":"kimi","bridge":"smoke"}'

READ_ONLY_ACTIONS = {"navigate", "open", "read", "inspect", "snapshot", "screenshot", "extract", "view"}
SUPPORTED_ACTIONS = READ_ONLY_ACTIONS | {"click", "type"}
SUPPORTED_BACKENDS = ("dry-run", "chrome-devtools-mcp", "kimi-webbridge", "hermes")


@dataclass(frozen=True)
class BrowserAIService:
    key: str
    label: str
    url: str
    family: str
    live_backend: str = ""
    council_candidate: bool = True
    notes: str = "prepare-only until adapter selector is proven"

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


AI_SERVICE_CATALOG: tuple[BrowserAIService, ...] = (
    BrowserAIService("kimi", "Kimi", "https://www.kimi.com/", "moonshot", live_backend="kimi-webbridge", notes="first live benchmark candidate"),
    BrowserAIService("chatgpt", "ChatGPT", "https://chatgpt.com/", "openai"),
    BrowserAIService("claude", "Claude", "https://claude.ai/", "anthropic"),
    BrowserAIService("gemini", "Gemini", "https://gemini.google.com/", "google"),
    BrowserAIService("gemini-pro", "Gemini Pro", "https://gemini.google.com/", "google"),
    BrowserAIService("gemini-thinking", "Gemini Thinking", "https://gemini.google.com/", "google"),
    BrowserAIService("perplexity", "Perplexity", "https://www.perplexity.ai/", "perplexity"),
    BrowserAIService("deepsearch", "DeepSearch", "https://www.perplexity.ai/", "perplexity"),
    BrowserAIService("grok", "Grok", "https://grok.com/", "xai"),
    BrowserAIService("copilot", "Copilot", "https://copilot.microsoft.com/", "microsoft"),
    BrowserAIService("copilot-smart", "Copilot Smart", "https://copilot.microsoft.com/", "microsoft"),
    BrowserAIService("qwen-max", "Qwen Max", "https://chat.qwen.ai/", "alibaba"),
    BrowserAIService("qwen-agents", "Qwen Agents", "https://chat.qwen.ai/", "alibaba"),
    BrowserAIService("deepseek-4-pro", "DeepSeek 4 Pro", "https://chat.deepseek.com/", "deepseek"),
    BrowserAIService("deepseek-4-vision", "DeepSeek 4 Vision", "https://chat.deepseek.com/", "deepseek"),
    BrowserAIService("deepseek4", "DeepSeek4", "https://chat.deepseek.com/", "deepseek"),
)

AI_SERVICE_URLS = {service.key: service.url for service in AI_SERVICE_CATALOG}
AI_SERVICE_BY_HOST = {
    (urlparse(service.url).hostname or "").lower(): service.key for service in AI_SERVICE_CATALOG
}

AI_SERVICE_ALIASES = {
    "gemini_pro": "gemini-pro",
    "gemini-thinking": "gemini-thinking",
    "gemini_thinking": "gemini-thinking",
    "copilot_smart": "copilot-smart",
    "qwen": "qwen-max",
    "qwen_max": "qwen-max",
    "qwen-agents": "qwen-agents",
    "qwen_agents": "qwen-agents",
    "deepseek": "deepseek4",
    "deepseek-4": "deepseek4",
    "deepseek_4": "deepseek4",
    "deepseek_4_pro": "deepseek-4-pro",
    "deepseek4pro": "deepseek-4-pro",
    "deepseek_4_vision": "deepseek-4-vision",
    "deepseek4vision": "deepseek-4-vision",
}

LIVE_SEND_BACKENDS = {
    "kimi-webbridge": {"kimi"},
}

BrowserConsultationSender = Callable[[dict[str, Any]], dict[str, Any]]


@dataclass(frozen=True)
class BrowserBackendStatus:
    backend: str
    configured: bool
    enabled: bool
    available: bool
    command: str = ""
    reason: str = ""
    network_policy: str = "no_external_call_by_default"
    role: str = "optional"
    send_capable_services: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class BrowserAction:
    schema: str
    backend: str
    url: str
    action: str
    selector: str = ""
    text: str = ""
    intent: str = ""
    gate: str = "REVIEW"
    reasons: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return redact_mapping(asdict(self))


def build_browser_bridge_status(
    *,
    env: dict[str, str] | None = None,
    command_finder: Callable[[str], str | None] | None = None,
) -> dict[str, Any]:
    values = os.environ if env is None else env
    finder = command_finder or shutil.which
    bridge_enabled = values.get(BROWSER_BRIDGE_ENABLE_ENV, "0") == "1"
    send_enabled = values.get(BROWSER_SEND_ENABLE_ENV, "0") == "1"

    npx = finder("npx") or ""
    hermes = finder("hermes") or ""
    kimi_url = values.get(KIMI_WEBBRIDGE_URL_ENV, "")

    backends = [
        BrowserBackendStatus(
            backend="dry-run",
            configured=True,
            enabled=True,
            available=True,
            reason="deterministic local fixture; no browser or network call",
            network_policy="local_artifact_only",
            role="fallback",
        ),
        BrowserBackendStatus(
            backend="chrome-devtools-mcp",
            configured=bool(npx),
            enabled=bridge_enabled,
            available=bool(npx and bridge_enabled),
            command="npx chrome-devtools-mcp@latest --autoConnect",
            reason="primary real backend candidate; Wabi detects npx but does not install or launch it automatically",
            role="primary_read_only",
        ),
        BrowserBackendStatus(
            backend="kimi-webbridge",
            configured=bool(kimi_url),
            enabled=bridge_enabled,
            available=bool(kimi_url and bridge_enabled),
            command="operator-installed Kimi WebBridge local service",
            reason="external installation remains manual REVIEW; Wabi only detects declared local endpoint",
            role="optional_ai_send",
            send_capable_services=sorted(LIVE_SEND_BACKENDS["kimi-webbridge"]),
        ),
        BrowserBackendStatus(
            backend="hermes",
            configured=bool(hermes),
            enabled=bridge_enabled,
            available=bool(hermes and bridge_enabled),
            command=hermes or "hermes",
            reason="optional adapter only; Wabi never runs hermes --yolo",
            role="optional_read_only",
        ),
    ]
    return redact_mapping(
        {
            "schema": BROWSER_BRIDGE_STATUS_SCHEMA,
            "bridge_enabled": bridge_enabled,
            "send_enabled": send_enabled,
            "enable_env": BROWSER_BRIDGE_ENABLE_ENV,
            "send_enable_env": BROWSER_SEND_ENABLE_ENV,
            "kimi_webbridge_url_env": KIMI_WEBBRIDGE_URL_ENV,
            "default_backend": "dry-run",
            "primary_backend": "chrome-devtools-mcp",
            "authority": "local_observation_only",
            "install_policy": "no_auto_install_no_curl_pipe_no_global_config",
            "execution_policy": "read_snapshot_extract_screenshot_only_unless_explicit_gate",
            "backends": [backend.to_dict() for backend in backends],
            "selector_pack": build_selector_pack_status(env=values, command_finder=finder),
            "ai_service_allowlist": sorted(AI_SERVICE_URLS),
            "ai_service_catalog": browser_ai_service_catalog(),
            "live_send_backends": {key: sorted(value) for key, value in LIVE_SEND_BACKENDS.items()},
        },
        env=values,
    )


def browser_ai_service_catalog() -> list[dict[str, Any]]:
    return [service.to_dict() for service in AI_SERVICE_CATALOG]


def build_browser_action(
    *,
    url: str,
    action: str = "navigate",
    backend: str = "dry-run",
    selector: str = "",
    text: str = "",
    intent: str = "",
) -> BrowserAction:
    normalized_action = _normalize_action(action)
    gate_eval = evaluate_browser_request(url, normalized_action)
    return BrowserAction(
        schema=BROWSER_ACTION_SCHEMA,
        backend=backend,
        url=url,
        action=normalized_action,
        selector=selector,
        text=redact_text(text),
        intent=redact_text(intent),
        gate=gate_eval["gate"],
        reasons=list(gate_eval["reasons"]),
    )


def observe_browser_url(
    *,
    workspace: str | Path,
    runtime_root: str | Path,
    url: str,
    action: str = "navigate",
    backend: str = "dry-run",
    selector: str = "",
    text: str = "",
    intent: str = "",
    env: dict[str, str] | None = None,
) -> dict[str, Any]:
    values = os.environ if env is None else env
    workspace_path = Path(workspace).resolve()
    runtime_path = Path(runtime_root).resolve()
    browser_action = build_browser_action(
        url=url,
        action=action,
        backend=backend,
        selector=selector,
        text=text,
        intent=intent,
    )
    action_payload = browser_action.to_dict()
    backend_status = build_browser_bridge_status(env=values)
    backend_info = _select_backend(backend_status, backend)

    if browser_action.gate == "BLOCK":
        return {
            "ok": False,
            "schema": BROWSER_OBSERVATION_SCHEMA,
            "action": "browser_observation_blocked",
            "browser_action": action_payload,
            "gate": "BLOCK",
            "reasons": browser_action.reasons,
            "browser_backend_called": False,
            "online_ai_called": False,
            "error": "browser_action_blocked",
        }
    if browser_action.gate != "APPROVE":
        return {
            "ok": False,
            "schema": BROWSER_OBSERVATION_SCHEMA,
            "action": "browser_observation_review_required",
            "browser_action": action_payload,
            "gate": browser_action.gate,
            "reasons": browser_action.reasons,
            "browser_backend_called": False,
            "online_ai_called": False,
            "error": "browser_action_review_required",
        }
    if backend != "dry-run" and not backend_info.get("available"):
        return {
            "ok": False,
            "schema": BROWSER_OBSERVATION_SCHEMA,
            "action": "browser_backend_unavailable",
            "browser_action": action_payload,
            "backend_status": backend_info,
            "gate": "REVIEW",
            "reasons": ["browser_backend_not_enabled_or_not_configured"],
            "browser_backend_called": False,
            "online_ai_called": False,
            "error": "browser_backend_unavailable",
        }

    observation = _dry_run_observation(
        workspace=workspace_path,
        url=url,
        action=browser_action.action,
        backend=backend,
        intent=intent,
    )
    artifact = write_artifact(
        runtime_path / "outputs" / "browser_bridge",
        "wabi_browser_observation",
        ".json",
        json.dumps(observation, indent=2, ensure_ascii=False) + "\n",
    )
    return {
        "ok": True,
        "schema": BROWSER_OBSERVATION_SCHEMA,
        "action": "browser_observation",
        "browser_action": action_payload,
        "backend_status": backend_info,
        "observation": observation,
        "artifact": str(artifact),
        "gate": "APPROVE",
        "reasons": browser_action.reasons,
        "browser_backend_called": False,
        "online_ai_called": False,
        "cloud_authority": "observation_only",
    }


def prepare_browser_ai_consultation(
    *,
    workspace: str | Path,
    runtime_root: str | Path,
    service: str,
    prompt: str,
    backend: str = "dry-run",
    env: dict[str, str] | None = None,
    send_requested: bool = False,
    sender: BrowserConsultationSender | None = None,
) -> dict[str, Any]:
    values = os.environ if env is None else env
    workspace_path = Path(workspace).resolve()
    runtime_path = Path(runtime_root).resolve()
    normalized = _normalize_ai_service(service)
    if normalized is None:
        return {
            "ok": False,
            "schema": BROWSER_AI_CONSULTATION_SCHEMA,
            "action": "browser_ai_consultation_blocked",
            "service": service,
            "url": service,
            "gate": "BLOCK",
            "reasons": ["ai_service_not_allowlisted"],
            "browser_backend_called": False,
            "online_ai_called": False,
            "secret_values_printed": False,
            "error": "ai_service_not_allowlisted",
        }
    service_info = normalized
    service_key = service_info.key
    url = service_info.url
    backend_status = build_browser_bridge_status(env=values)
    backend_info = _select_backend(backend_status, backend)

    sanitized_prompt = redact_text(prompt)
    send_enabled = values.get(BROWSER_SEND_ENABLE_ENV, "0") == "1"
    live_supported = _backend_supports_ai_service(backend, service_key)
    gate, reasons = _evaluate_ai_send_gate(
        send_requested=send_requested,
        send_enabled=send_enabled,
        backend_info=backend_info,
        backend=backend,
        service_key=service_key,
        live_supported=live_supported,
    )
    request = {
        "schema": BROWSER_AI_CONSULTATION_SCHEMA,
        "service": service_key,
        "service_label": service_info.label,
        "url": url,
        "backend": backend,
        "prompt": sanitized_prompt,
        "expected_return_contract": "wabi.cloud_code_proposal.v0_1 when code is requested",
        "authority": "online_ai_response_is_proposal_only",
        "local_revalidation_required": True,
        "send_requested": send_requested,
        "send_enabled": send_enabled,
        "backend_available": bool(backend_info.get("available")),
        "live_supported": live_supported,
        "gate": gate,
        "reasons": reasons,
        "redacted": sanitized_prompt != prompt,
    }
    artifact = write_artifact(
        runtime_path / "outputs" / "browser_bridge",
        f"wabi_browser_ai_consultation_{service_key}",
        ".json",
        json.dumps(request, indent=2, ensure_ascii=False) + "\n",
    )
    payload = {
        "ok": True,
        "schema": BROWSER_AI_CONSULTATION_SCHEMA,
        "action": "browser_ai_consultation_request",
        "service": service_key,
        "service_label": service_info.label,
        "url": url,
        "gate": gate,
        "reasons": reasons,
        "request": request,
        "artifact": str(artifact),
        "backend_status": backend_info,
        "browser_backend_called": False,
        "online_ai_called": False,
        "secret_values_printed": False,
        "next_step": "review request artifact, then use cloud proposal validation on any returned JSON",
        "workspace": str(workspace_path),
    }
    if gate == "APPROVE":
        send_result = _send_ai_consultation(
            request=request,
            service_info=service_info,
            runtime_path=runtime_path,
            env=values,
            sender=sender,
        )
        payload.update(send_result)
        response_text = send_result.get("response_text", "")
        if response_text:
            payload["proposal_extraction"] = _extract_and_validate_response_proposal(
                workspace=workspace_path,
                runtime_root=runtime_path,
                response_text=response_text,
                source=f"browser_{service_key}",
            )
    return redact_mapping(payload, env=values)


def prepare_browser_council(
    *,
    workspace: str | Path,
    runtime_root: str | Path,
    prompt: str,
    backend: str = "dry-run",
    env: dict[str, str] | None = None,
    send_requested: bool = False,
    services: list[str] | None = None,
    sender: BrowserConsultationSender | None = None,
) -> dict[str, Any]:
    values = os.environ if env is None else env
    runtime_path = Path(runtime_root).resolve()
    selected_services = services or [service.key for service in AI_SERVICE_CATALOG if service.council_candidate]
    ranking = rank_browser_council_services(
        payload_class=PUBLIC_PROMPT,
        send_requested=send_requested,
        env=dict(values),
        services=selected_services,
    )
    ranking_by_service = {item["service_id"]: item for item in ranking.get("services", [])}
    consultations: list[dict[str, Any]] = []
    artifacts: list[str] = []
    live_attempts = 0
    for service_name in selected_services:
        service_info = _normalize_ai_service(service_name)
        selected_backend = backend
        if send_requested and service_info and service_info.live_backend:
            selected_backend = service_info.live_backend
        consultation = prepare_browser_ai_consultation(
            workspace=workspace,
            runtime_root=runtime_path,
            service=service_name,
            prompt=prompt,
            backend=selected_backend,
            env=dict(values),
            send_requested=send_requested,
            sender=sender,
        )
        if service_info:
            consultation["selector"] = ranking_by_service.get(service_info.key, {})
        consultations.append(consultation)
        if consultation.get("artifact"):
            artifacts.append(str(consultation["artifact"]))
        if consultation.get("online_ai_called"):
            live_attempts += 1
    payload = {
        "ok": True,
        "schema": BROWSER_COUNCIL_SCHEMA,
        "action": "browser_council_prepare",
        "prompt": redact_text(prompt),
        "backend": backend,
        "send_requested": send_requested,
        "service_count": len(consultations),
        "prepared_count": sum(1 for item in consultations if item.get("ok")),
        "live_attempts": live_attempts,
        "ranking": ranking,
        "classifications": {
            "READY_READONLY": ranking.get("ready_readonly_count", 0),
            "READY_SEND_REVIEW": ranking.get("ready_send_review_count", 0),
            "PREPARE_ONLY": ranking.get("prepare_only_count", 0),
            "BLOCKED": ranking.get("blocked_count", 0),
        },
        "recommended_service": ranking.get("recommended_service", ""),
        "recommended_mode": ranking.get("recommended_mode", "DRY_RUN"),
        "next_action": ranking.get("next_action", "keep_dry_run_default"),
        "gate": "APPROVE" if live_attempts else "REVIEW",
        "reasons": (
            ["live_adapter_responses_are_proposals_only", "local_revalidation_required"]
            if live_attempts
            else ["council_prepare_only", "use --send plus send env plus proven adapter for live call"]
        ),
        "consultations": consultations,
        "artifacts": artifacts,
        "online_ai_called": live_attempts > 0,
        "browser_backend_called": any(item.get("browser_backend_called") for item in consultations),
        "cloud_authority": "proposals_only_never_execution_permission",
    }
    artifact = write_artifact(
        runtime_path / "outputs" / "browser_bridge",
        "wabi_browser_council",
        ".json",
        json.dumps(redact_mapping(payload, env=values), indent=2, ensure_ascii=False) + "\n",
    )
    payload["artifact"] = str(artifact)
    return redact_mapping(payload, env=values)


def run_kimi_smoke(
    *,
    runtime_root: str | Path,
    env: dict[str, str] | None = None,
    send_requested: bool = False,
    sender: BrowserConsultationSender | None = None,
) -> dict[str, Any]:
    values = os.environ if env is None else env
    runtime_path = Path(runtime_root).resolve()
    decision = select_browser_bridge_backend(
        service_id="kimi",
        payload_class=PUBLIC_PROMPT,
        requested_backend="kimi-webbridge",
        send_requested=send_requested,
        env=dict(values),
    )
    kimi_url = str(values.get(KIMI_WEBBRIDGE_URL_ENV, "")).strip()
    status = _kimi_smoke_not_run_status(send_requested=send_requested, env=values, kimi_url=kimi_url)
    base = {
        "ok": status == "KIMI_SMOKE_PASS",
        "schema": BROWSER_KIMI_SMOKE_SCHEMA,
        "action": "browser_bridge_kimi_smoke",
        "gate": "APPROVE" if status == "KIMI_SMOKE_PASS" else "REVIEW",
        "status": status,
        "service": "kimi",
        "backend": "kimi-webbridge",
        "prompt_class": PUBLIC_PROMPT,
        "prompt_sha256": hashlib.sha256(KIMI_SMOKE_PROMPT.encode("utf-8")).hexdigest(),
        "selector": decision,
        "workspace_sent": False,
        "private_paths_sent": False,
        "internal_code_sent": False,
        "credentials_sent": False,
        "secret_values_printed": False,
        "online_ai_called": False,
        "browser_backend_called": False,
        "live_attempts": 0,
        "publication_gate": "BLOCK",
        "reasons": [],
    }
    if status != "KIMI_SMOKE_PASS" and not decision.get("safe_to_send"):
        base["reasons"] = decision.get("reason", "").split(";") if decision.get("reason") else ["kimi_smoke_gates_missing"]
        artifact = write_artifact(
            runtime_path / "outputs" / "browser_bridge",
            "wabi_browser_kimi_smoke",
            ".json",
            json.dumps(redact_mapping(base, env=values), indent=2, ensure_ascii=False) + "\n",
        )
        base["artifact"] = str(artifact)
        return redact_mapping(base, env=values)

    request = {
        "schema": BROWSER_KIMI_SMOKE_SCHEMA,
        "service": "kimi",
        "backend": "kimi-webbridge",
        "prompt": KIMI_SMOKE_PROMPT,
        "expected": {"ok": True, "service": "kimi", "bridge": "smoke"},
        "authority": "public_synthetic_smoke_only",
    }
    if sender is not None:
        result = sender(request)
    else:
        result = _post_kimi_webbridge(request=request, env=values)
    response_text = _response_text(result)
    parsed = _parse_kimi_smoke_response(response_text)
    final_status = _classify_kimi_smoke_result(result, parsed)
    base.update(
        {
            "ok": final_status == "KIMI_SMOKE_PASS",
            "gate": "APPROVE" if final_status == "KIMI_SMOKE_PASS" else "REVIEW",
            "status": final_status,
            "send_result": redact_mapping(result, env=values),
            "response": parsed if isinstance(parsed, dict) else {},
            "online_ai_called": True,
            "browser_backend_called": True,
            "live_attempts": 1,
            "reasons": [] if final_status == "KIMI_SMOKE_PASS" else ["kimi_smoke_response_not_exact_public_contract"],
        }
    )
    artifact = write_artifact(
        runtime_path / "outputs" / "browser_bridge",
        "wabi_browser_kimi_smoke",
        ".json",
        json.dumps(redact_mapping(base, env=values), indent=2, ensure_ascii=False) + "\n",
    )
    base["artifact"] = str(artifact)
    return redact_mapping(base, env=values)


def run_devtools_readonly_snapshot(
    *,
    runtime_root: str | Path,
    url: str = "http://127.0.0.1:8787/",
    env: dict[str, str] | None = None,
    command_finder: Callable[[str], str | None] | None = None,
    fetcher: Callable[[str, int], str] | None = None,
) -> dict[str, Any]:
    values = os.environ if env is None else env
    runtime_path = Path(runtime_root).resolve()
    if not _is_local_http_url(url):
        payload = _devtools_snapshot_payload(
            status="DEVTOOLS_MCP_FAIL_REDACTED",
            url=url,
            reasons=["snapshot_url_must_be_localhost"],
            browser_backend_called=False,
        )
    else:
        selector = select_browser_bridge_backend(
            service_id="chrome-devtools-mcp",
            payload_class=SNAPSHOT_READONLY,
            requested_backend="chrome-devtools-mcp",
            env=dict(values),
            command_finder=command_finder,
        )
        if selector["mode"] != "READ_ONLY":
            payload = _devtools_snapshot_payload(
                status="DEVTOOLS_MCP_NOT_AVAILABLE",
                url=url,
                selector=selector,
                reasons=["chrome_devtools_mcp_not_enabled_or_not_configured"],
                browser_backend_called=False,
            )
        else:
            try:
                body = fetcher(url, _timeout_seconds(values)) if fetcher else _fetch_local_text(url, _timeout_seconds(values))
                payload = _devtools_snapshot_payload(
                    status="DEVTOOLS_MCP_READONLY_PASS",
                    url=url,
                    selector=selector,
                    reasons=["local_readonly_snapshot_collected", "no_external_service_called"],
                    browser_backend_called=True,
                    snapshot={
                        "title": _extract_html_title(body),
                        "body_chars": len(body),
                        "structure": _html_structure_summary(body),
                        "screenshot_artifact": "",
                    },
                )
            except TimeoutError:
                payload = _devtools_snapshot_payload(
                    status="DEVTOOLS_MCP_TIMEOUT_REVIEW",
                    url=url,
                    selector=selector,
                    reasons=["local_snapshot_timeout"],
                    browser_backend_called=False,
                )
            except Exception as exc:
                payload = _devtools_snapshot_payload(
                    status="DEVTOOLS_MCP_FAIL_REDACTED",
                    url=url,
                    selector=selector,
                    reasons=[f"local_snapshot_failed:{type(exc).__name__}"],
                    browser_backend_called=False,
                )
    artifact = write_artifact(
        runtime_path / "outputs" / "browser_bridge",
        "wabi_browser_devtools_readonly",
        ".json",
        json.dumps(redact_mapping(payload, env=values), indent=2, ensure_ascii=False) + "\n",
    )
    payload["artifact"] = str(artifact)
    return redact_mapping(payload, env=values)


def convert_browser_response_to_proposal(
    *,
    workspace: str | Path,
    runtime_root: str | Path,
    response_text: str | None = None,
    input_path: str | Path | None = None,
    source: str = "browser_response",
) -> dict[str, Any]:
    workspace_path = Path(workspace).resolve()
    runtime_path = Path(runtime_root).resolve()
    if input_path is not None:
        try:
            response_text = _read_response_input(workspace_path, runtime_path, input_path)
        except ValueError as exc:
            return {
                "ok": False,
                "schema": BROWSER_RESPONSE_PROPOSAL_SCHEMA,
                "action": "browser_response_to_proposal",
                "proposal_status": "REJECTED_OUT_OF_SCOPE",
                "error": str(exc),
                "auto_apply": False,
                "task_spec_created": False,
                "patch_plan_created": False,
                "secret_values_printed": False,
                "publication_gate": "BLOCK",
            }
    text = response_text or ""
    response_artifact = write_artifact(
        runtime_path / "outputs" / "browser_bridge",
        "wabi_browser_response_text",
        ".txt",
        redact_text(text) + "\n",
    )
    extraction = _extract_and_validate_response_proposal(
        workspace=workspace_path,
        runtime_root=runtime_path,
        response_text=text,
        source=source,
    )
    validation = extraction.get("validation", {}) if isinstance(extraction.get("validation"), dict) else {}
    errors = validation.get("errors", []) if isinstance(validation.get("errors"), list) else []
    status = _proposal_status_from_validation(extraction, errors)
    payload = {
        "ok": status == "VALIDATED",
        "schema": BROWSER_RESPONSE_PROPOSAL_SCHEMA,
        "action": "browser_response_to_proposal",
        "proposal_status": status,
        "response_artifact": str(response_artifact),
        "proposal_extraction": extraction,
        "auto_apply": False,
        "task_spec_created": False,
        "patch_plan_created": False,
        "task_spec_candidate": status == "VALIDATED",
        "patch_plan_candidate": status == "VALIDATED",
        "secret_values_printed": False,
        "publication_gate": "BLOCK",
    }
    artifact = write_artifact(
        runtime_path / "outputs" / "browser_bridge",
        "wabi_browser_response_to_proposal",
        ".json",
        json.dumps(redact_mapping(payload), indent=2, ensure_ascii=False) + "\n",
    )
    payload["artifact"] = str(artifact)
    return redact_mapping(payload)


def _normalize_action(action: str) -> str:
    normalized = action.strip().lower() or "navigate"
    aliases = {
        "observe": "navigate",
        "observa": "navigate",
        "open": "navigate",
        "read": "read",
        "extract": "extract",
        "snapshot": "snapshot",
        "screenshot": "screenshot",
    }
    normalized = aliases.get(normalized, normalized)
    return normalized if normalized in SUPPORTED_ACTIONS else normalized


def _select_backend(status: dict[str, Any], backend: str) -> dict[str, Any]:
    for item in status.get("backends", []):
        if item.get("backend") == backend:
            return item
    return {
        "backend": backend,
        "configured": False,
        "enabled": False,
        "available": False,
        "reason": "unknown_browser_backend",
    }


def _normalize_ai_service(service: str) -> BrowserAIService | None:
    raw = service.strip().lower() or "kimi"
    key = AI_SERVICE_ALIASES.get(raw, raw.replace(" ", "-"))
    if key in AI_SERVICE_URLS:
        return next(item for item in AI_SERVICE_CATALOG if item.key == key)
    parsed = urlparse(service)
    host = (parsed.hostname or "").lower()
    known_key = AI_SERVICE_BY_HOST.get(host)
    if known_key:
        return next(item for item in AI_SERVICE_CATALOG if item.key == known_key)
    return None


def _backend_supports_ai_service(backend: str, service_key: str) -> bool:
    return service_key in LIVE_SEND_BACKENDS.get(backend, set())


def _evaluate_ai_send_gate(
    *,
    send_requested: bool,
    send_enabled: bool,
    backend_info: dict[str, Any],
    backend: str,
    service_key: str,
    live_supported: bool,
) -> tuple[str, list[str]]:
    if not send_requested:
        return "REVIEW", ["send_flag_required", f"set {BROWSER_SEND_ENABLE_ENV}=1 for reviewed send"]
    if not send_enabled:
        return "REVIEW", [f"set {BROWSER_SEND_ENABLE_ENV}=1 for reviewed send"]
    if not backend_info.get("available"):
        return "REVIEW_SKIPPED", ["browser_backend_not_enabled_or_not_configured"]
    if not live_supported:
        return "REVIEW_SKIPPED", [f"service_prepare_only_until_selector_pack_proven:{service_key}:{backend}"]
    return "APPROVE", ["operator_requested_send", "operator_enabled_browser_send", "adapter_live_supported"]


def _send_ai_consultation(
    *,
    request: dict[str, Any],
    service_info: BrowserAIService,
    runtime_path: Path,
    env: dict[str, str] | os._Environ[str],
    sender: BrowserConsultationSender | None,
) -> dict[str, Any]:
    if sender is not None:
        result = sender(request)
    elif request["backend"] == "kimi-webbridge" and service_info.key == "kimi":
        result = _post_kimi_webbridge(request=request, env=env)
    else:
        return {
            "ok": False,
            "action": "browser_ai_consultation_send_skipped",
            "gate": "REVIEW_SKIPPED",
            "browser_backend_called": False,
            "online_ai_called": False,
            "error": "adapter_protocol_not_verified",
        }
    response_text = _response_text(result)
    response_artifact = write_artifact(
        runtime_path / "outputs" / "browser_bridge",
        f"wabi_browser_ai_response_{request['service']}",
        ".json",
        json.dumps(redact_mapping(result, env=env), indent=2, ensure_ascii=False) + "\n",
    )
    return {
        "action": "browser_ai_consultation_sent",
        "send_result": redact_mapping(result, env=env),
        "response_artifact": str(response_artifact),
        "response_text": redact_text(response_text, env=env),
        "browser_backend_called": True,
        "online_ai_called": True,
        "cloud_authority": "proposal_only",
    }


def _post_kimi_webbridge(*, request: dict[str, Any], env: dict[str, str] | os._Environ[str]) -> dict[str, Any]:
    endpoint = str(env.get(KIMI_WEBBRIDGE_URL_ENV, "")).strip()
    if not endpoint:
        return {"ok": False, "error": "missing_kimi_webbridge_url"}
    if not is_safe_local_url(endpoint):
        return {"ok": False, "error": "kimi_webbridge_url_must_be_localhost"}
    timeout = _timeout_seconds(env)
    body = json.dumps(
        {
            "service": request["service"],
            "prompt": request["prompt"],
            "expected_return_contract": request.get("expected_return_contract") or request.get("expected") or "public_synthetic_smoke_json",
            "authority": request["authority"],
        },
        ensure_ascii=False,
    ).encode("utf-8")
    http_request = urllib.request.Request(
        endpoint,
        data=body,
        headers={"Content-Type": "application/json", "User-Agent": "wabi-browser-bridge/0.1"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(http_request, timeout=timeout) as response:
            response_body = response.read(512_000).decode("utf-8", errors="replace")
            return {
                "ok": 200 <= response.status < 300,
                "status": response.status,
                "reason": getattr(response, "reason", ""),
                "output": response_body,
            }
    except urllib.error.HTTPError as exc:
        response_body = exc.read(64_000).decode("utf-8", errors="replace")
        return {"ok": False, "status": exc.code, "reason": exc.reason, "output": response_body}
    except (urllib.error.URLError, TimeoutError, http.client.HTTPException, OSError) as exc:
        return {"ok": False, "error": f"kimi_webbridge_request_failed:{exc}"}


def _timeout_seconds(env: dict[str, str] | os._Environ[str]) -> int:
    raw = str(env.get("WABI_BROWSER_BRIDGE_TIMEOUT_SECONDS", "20"))
    try:
        value = int(raw)
    except ValueError:
        return 20
    return min(max(value, 1), 120)


def _response_text(result: dict[str, Any]) -> str:
    for key in ("output", "text", "response", "content"):
        value = result.get(key)
        if isinstance(value, str):
            return value
    return json.dumps(result, ensure_ascii=False)


def _extract_and_validate_response_proposal(
    *,
    workspace: Path,
    runtime_root: Path,
    response_text: str,
    source: str,
) -> dict[str, Any]:
    try:
        proposal = extract_cloud_code_proposal_payload(response_text)
        proposal_artifact = write_cloud_proposal_artifact(runtime_root / "outputs", proposal, source=source)
        validation = validate_cloud_code_proposal(
            workspace=workspace,
            proposal_path=proposal_artifact,
            input_roots=[runtime_root],
        )
        return {
            "ok": validation.ok,
            "proposal_artifact": str(proposal_artifact),
            "validation": validation.to_dict(),
            "next_step": "operator may review proposal; no TaskSpec or PatchPlan was auto-applied",
        }
    except Exception as exc:
        return {
            "ok": False,
            "error": str(exc),
            "next_step": "no structured cloud proposal found; keep response as advisory text only",
        }


def _dry_run_observation(*, workspace: Path, url: str, action: str, backend: str, intent: str) -> dict[str, Any]:
    visible_text = "\n".join(
        [
            "Dry-run browser observation.",
            "No browser backend, extension, online service, cookie, login session, or network target was called.",
            f"Requested action: {action}",
            f"Requested URL: {url}",
            f"Workspace: {workspace}",
        ]
    )
    text_hash = hashlib.sha256(visible_text.encode("utf-8")).hexdigest()
    return {
        "schema": BROWSER_OBSERVATION_SCHEMA,
        "backend": backend,
        "url": url,
        "title": "Wabi BrowserBridge dry-run",
        "visible_text": visible_text,
        "visible_text_sha256": text_hash,
        "interactive_refs": [
            {"ref": "@e1", "role": "link", "label": "dry-run target"},
            {"ref": "@e2", "role": "button", "label": "no-op local evidence"},
        ],
        "screenshot_artifact": "",
        "intent": redact_text(intent),
        "cloud_authority": "observation_only",
        "local_sessions_read": False,
        "cookies_extracted": False,
        "secrets_printed": False,
    }


def _kimi_smoke_not_run_status(
    *,
    send_requested: bool,
    env: dict[str, str] | os._Environ[str],
    kimi_url: str,
) -> str:
    if not send_requested or env.get(BROWSER_SEND_ENABLE_ENV, "0") != "1" or env.get(BROWSER_BRIDGE_ENABLE_ENV, "0") != "1":
        return "KIMI_SEND_FLAGS_MISSING"
    if not kimi_url:
        return "KIMI_BRIDGE_URL_MISSING"
    if not is_safe_local_url(kimi_url):
        return "KIMI_SMOKE_FAIL_REDACTED"
    return "KIMI_SMOKE_PASS"


def _parse_kimi_smoke_response(response_text: str) -> dict[str, Any] | None:
    try:
        parsed = json.loads(response_text.strip())
    except json.JSONDecodeError:
        return None
    return parsed if isinstance(parsed, dict) else None


def _classify_kimi_smoke_result(result: dict[str, Any], parsed: dict[str, Any] | None) -> str:
    status = int(result.get("status") or 0)
    output = _response_text(result).lower()
    if status in {401, 403} or any(marker in output for marker in ["login", "2fa", "authentication", "upgrade", "payment"]):
        return "KIMI_AUTH_REQUIRED_REDACTED"
    if "timed out" in output or "timeout" in output:
        return "KIMI_TIMEOUT_REVIEW"
    if parsed == {"ok": True, "service": "kimi", "bridge": "smoke"}:
        return "KIMI_SMOKE_PASS"
    return "KIMI_SMOKE_FAIL_REDACTED"


def _is_local_http_url(url: str) -> bool:
    parsed = urlparse(str(url or "").strip())
    host = (parsed.hostname or "").lower()
    return parsed.scheme in {"http", "https"} and host in {"127.0.0.1", "localhost", "::1"}


def _fetch_local_text(url: str, timeout: int) -> str:
    request = urllib.request.Request(url, headers={"User-Agent": "wabi-browser-bridge-readonly/0.2"}, method="GET")
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return response.read(512_000).decode("utf-8", errors="replace")


def _extract_html_title(body: str) -> str:
    match = re.search(r"<title[^>]*>(.*?)</title>", body, flags=re.IGNORECASE | re.DOTALL)
    if not match:
        return ""
    return re.sub(r"\s+", " ", match.group(1)).strip()[:160]


def _html_structure_summary(body: str) -> dict[str, int]:
    lowered = body.lower()
    return {
        "h1": lowered.count("<h1"),
        "h2": lowered.count("<h2"),
        "button": lowered.count("<button"),
        "section": lowered.count("<section"),
        "panel_id_mentions": lowered.count("panel"),
    }


def _devtools_snapshot_payload(
    *,
    status: str,
    url: str,
    reasons: list[str],
    browser_backend_called: bool,
    selector: dict[str, Any] | None = None,
    snapshot: dict[str, Any] | None = None,
) -> dict[str, Any]:
    return {
        "ok": status == "DEVTOOLS_MCP_READONLY_PASS",
        "schema": BROWSER_DEVTOOLS_READONLY_SCHEMA,
        "action": "browser_bridge_devtools_readonly_snapshot",
        "gate": "APPROVE" if status == "DEVTOOLS_MCP_READONLY_PASS" else "REVIEW",
        "status": status,
        "backend": "chrome-devtools-mcp",
        "url": url,
        "selector": selector or {},
        "snapshot": snapshot or {},
        "browser_backend_called": browser_backend_called,
        "online_ai_called": False,
        "external_service_called": False,
        "credentials_sent": False,
        "secret_values_printed": False,
        "publication_gate": "BLOCK",
        "reasons": reasons,
    }


def _read_response_input(workspace: Path, runtime_root: Path, input_path: str | Path) -> str:
    raw = Path(input_path)
    candidate = raw.resolve() if raw.is_absolute() else (workspace / raw).resolve()
    allowed_roots = [workspace.resolve(), runtime_root.resolve()]
    if not any(candidate == root or root in candidate.parents for root in allowed_roots):
        raise ValueError(f"browser_response_input_outside_allowlist:{candidate.name}")
    if candidate.suffix.lower() not in {".txt", ".json", ".md"}:
        raise ValueError("browser_response_input_extension_blocked")
    return candidate.read_text(encoding="utf-8", errors="replace")


def _proposal_status_from_validation(extraction: dict[str, Any], errors: list[str]) -> str:
    if extraction.get("ok") is True:
        return "VALIDATED"
    joined = ";".join(str(item) for item in errors)
    if any(marker in joined for marker in ["target_blocked", "unsupported_cloud_proposal_operation", "target_outside_workspace", "path_blocked"]):
        return "REJECTED_OUT_OF_SCOPE"
    if extraction.get("error"):
        return "PROPOSAL_ONLY"
    return "REQUIRES_HUMAN_REVIEW"


def _allowed_ai_hosts() -> set[str]:
    return {urlparse(url).hostname or "" for url in AI_SERVICE_URLS.values()}
