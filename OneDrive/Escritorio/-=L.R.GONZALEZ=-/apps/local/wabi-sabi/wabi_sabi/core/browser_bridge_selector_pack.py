from __future__ import annotations

import os
import shutil
from dataclasses import asdict, dataclass
from typing import Any, Callable
from urllib.parse import urlparse


SELECTOR_PACK_SCHEMA = "wabi.browser_bridge_selector_pack.v0_2"
SELECTOR_DECISION_SCHEMA = "wabi.browser_bridge_selector_decision.v0_2"
COUNCIL_RANKING_SCHEMA = "wabi.browser_bridge_council_ranking.v0_2"

BROWSER_BRIDGE_ENABLE_ENV = "WABI_ALLOW_BROWSER_BRIDGE"
BROWSER_SEND_ENABLE_ENV = "WABI_ALLOW_BROWSER_SEND"
KIMI_WEBBRIDGE_URL_ENV = "WABI_KIMI_WEBBRIDGE_URL"

PUBLICATION_GATE = "BLOCK"
SAFE_LOCAL_HOSTS = {"localhost", "127.0.0.1", "::1"}

PUBLIC_PROMPT = "PUBLIC_PROMPT"
SANITIZED_TASK = "SANITIZED_TASK"
SNAPSHOT_READONLY = "SNAPSHOT_READONLY"
CODE_PROPOSAL = "CODE_PROPOSAL"
PRIVATE_WORKSPACE_BLOCKED = "PRIVATE_WORKSPACE_BLOCKED"
CREDENTIAL_BLOCKED = "CREDENTIAL_BLOCKED"
PROTECTED_MATERIAL_BLOCKED = "PROTECTED_MATERIAL_BLOCKED"

PAYLOAD_CLASSES = (
    PUBLIC_PROMPT,
    SANITIZED_TASK,
    SNAPSHOT_READONLY,
    CODE_PROPOSAL,
    PRIVATE_WORKSPACE_BLOCKED,
    CREDENTIAL_BLOCKED,
    PROTECTED_MATERIAL_BLOCKED,
)

BLOCKED_PAYLOAD_CLASSES = {
    PRIVATE_WORKSPACE_BLOCKED,
    CREDENTIAL_BLOCKED,
    PROTECTED_MATERIAL_BLOCKED,
}


@dataclass(frozen=True)
class ServiceCapability:
    service_id: str
    display_name: str
    adapter: str
    mode: str
    supports_read: bool
    supports_send: bool
    supports_code_response: bool
    requires_url: bool
    requires_auth: bool
    default_gate: str
    risk_level: str
    allowed_payload_classes: tuple[str, ...]
    blocked_payload_classes: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


SERVICE_CAPABILITIES: tuple[ServiceCapability, ...] = (
    ServiceCapability(
        service_id="dry-run",
        display_name="Dry-run",
        adapter="dry-run",
        mode="DRY_RUN",
        supports_read=True,
        supports_send=False,
        supports_code_response=True,
        requires_url=False,
        requires_auth=False,
        default_gate="APPROVE",
        risk_level="LOW",
        allowed_payload_classes=(PUBLIC_PROMPT, SANITIZED_TASK, SNAPSHOT_READONLY, CODE_PROPOSAL),
        blocked_payload_classes=tuple(sorted(BLOCKED_PAYLOAD_CLASSES)),
    ),
    ServiceCapability(
        service_id="chrome-devtools-mcp",
        display_name="Chrome DevTools MCP",
        adapter="chrome-devtools-mcp",
        mode="READ_ONLY_SNAPSHOT",
        supports_read=True,
        supports_send=False,
        supports_code_response=False,
        requires_url=False,
        requires_auth=False,
        default_gate="REVIEW",
        risk_level="MEDIUM",
        allowed_payload_classes=(SNAPSHOT_READONLY,),
        blocked_payload_classes=tuple(sorted(BLOCKED_PAYLOAD_CLASSES | {PUBLIC_PROMPT, SANITIZED_TASK, CODE_PROPOSAL})),
    ),
    ServiceCapability(
        service_id="kimi",
        display_name="Kimi",
        adapter="kimi-webbridge",
        mode="SEND_REVIEW_DOUBLE_OPT_IN",
        supports_read=False,
        supports_send=True,
        supports_code_response=True,
        requires_url=True,
        requires_auth=True,
        default_gate="REVIEW",
        risk_level="HIGH",
        allowed_payload_classes=(PUBLIC_PROMPT, SANITIZED_TASK, CODE_PROPOSAL),
        blocked_payload_classes=tuple(sorted(BLOCKED_PAYLOAD_CLASSES | {SNAPSHOT_READONLY})),
    ),
    ServiceCapability(
        service_id="hermes",
        display_name="Hermes",
        adapter="hermes",
        mode="REVIEW_ADAPTER_NOT_LIVE",
        supports_read=True,
        supports_send=False,
        supports_code_response=True,
        requires_url=False,
        requires_auth=False,
        default_gate="REVIEW",
        risk_level="MEDIUM",
        allowed_payload_classes=(PUBLIC_PROMPT, SANITIZED_TASK, SNAPSHOT_READONLY, CODE_PROPOSAL),
        blocked_payload_classes=tuple(sorted(BLOCKED_PAYLOAD_CLASSES)),
    ),
    ServiceCapability("chatgpt", "ChatGPT", "prepare-only", "PREPARE_ONLY", False, False, True, False, True, "REVIEW", "MEDIUM", (PUBLIC_PROMPT, SANITIZED_TASK, CODE_PROPOSAL), tuple(sorted(BLOCKED_PAYLOAD_CLASSES | {SNAPSHOT_READONLY}))),
    ServiceCapability("claude", "Claude", "prepare-only", "PREPARE_ONLY", False, False, True, False, True, "REVIEW", "MEDIUM", (PUBLIC_PROMPT, SANITIZED_TASK, CODE_PROPOSAL), tuple(sorted(BLOCKED_PAYLOAD_CLASSES | {SNAPSHOT_READONLY}))),
    ServiceCapability("gemini", "Gemini", "prepare-only", "PREPARE_ONLY", False, False, True, False, True, "REVIEW", "MEDIUM", (PUBLIC_PROMPT, SANITIZED_TASK, CODE_PROPOSAL), tuple(sorted(BLOCKED_PAYLOAD_CLASSES | {SNAPSHOT_READONLY}))),
    ServiceCapability("gemini-pro", "Gemini Pro", "prepare-only", "PREPARE_ONLY", False, False, True, False, True, "REVIEW", "MEDIUM", (PUBLIC_PROMPT, SANITIZED_TASK, CODE_PROPOSAL), tuple(sorted(BLOCKED_PAYLOAD_CLASSES | {SNAPSHOT_READONLY}))),
    ServiceCapability("gemini-thinking", "Gemini Thinking", "prepare-only", "PREPARE_ONLY", False, False, True, False, True, "REVIEW", "MEDIUM", (PUBLIC_PROMPT, SANITIZED_TASK, CODE_PROPOSAL), tuple(sorted(BLOCKED_PAYLOAD_CLASSES | {SNAPSHOT_READONLY}))),
    ServiceCapability("perplexity", "Perplexity", "prepare-only", "PREPARE_ONLY", False, False, True, False, True, "REVIEW", "MEDIUM", (PUBLIC_PROMPT, SANITIZED_TASK, CODE_PROPOSAL), tuple(sorted(BLOCKED_PAYLOAD_CLASSES | {SNAPSHOT_READONLY}))),
    ServiceCapability("deepsearch", "DeepSearch", "prepare-only", "PREPARE_ONLY", False, False, True, False, True, "REVIEW", "MEDIUM", (PUBLIC_PROMPT, SANITIZED_TASK, CODE_PROPOSAL), tuple(sorted(BLOCKED_PAYLOAD_CLASSES | {SNAPSHOT_READONLY}))),
    ServiceCapability("grok", "Grok", "prepare-only", "PREPARE_ONLY", False, False, True, False, True, "REVIEW", "MEDIUM", (PUBLIC_PROMPT, SANITIZED_TASK, CODE_PROPOSAL), tuple(sorted(BLOCKED_PAYLOAD_CLASSES | {SNAPSHOT_READONLY}))),
    ServiceCapability("copilot", "Copilot", "prepare-only", "PREPARE_ONLY", False, False, True, False, True, "REVIEW", "MEDIUM", (PUBLIC_PROMPT, SANITIZED_TASK, CODE_PROPOSAL), tuple(sorted(BLOCKED_PAYLOAD_CLASSES | {SNAPSHOT_READONLY}))),
    ServiceCapability("copilot-smart", "Copilot Smart", "prepare-only", "PREPARE_ONLY", False, False, True, False, True, "REVIEW", "MEDIUM", (PUBLIC_PROMPT, SANITIZED_TASK, CODE_PROPOSAL), tuple(sorted(BLOCKED_PAYLOAD_CLASSES | {SNAPSHOT_READONLY}))),
    ServiceCapability("qwen-max", "Qwen Max", "prepare-only", "PREPARE_ONLY", False, False, True, False, True, "REVIEW", "MEDIUM", (PUBLIC_PROMPT, SANITIZED_TASK, CODE_PROPOSAL), tuple(sorted(BLOCKED_PAYLOAD_CLASSES | {SNAPSHOT_READONLY}))),
    ServiceCapability("qwen-agents", "Qwen Agents", "prepare-only", "PREPARE_ONLY", False, False, True, False, True, "REVIEW", "MEDIUM", (PUBLIC_PROMPT, SANITIZED_TASK, CODE_PROPOSAL), tuple(sorted(BLOCKED_PAYLOAD_CLASSES | {SNAPSHOT_READONLY}))),
    ServiceCapability("deepseek-4-pro", "DeepSeek 4 Pro", "prepare-only", "PREPARE_ONLY", False, False, True, False, True, "REVIEW", "HIGH", (PUBLIC_PROMPT, SANITIZED_TASK, CODE_PROPOSAL), tuple(sorted(BLOCKED_PAYLOAD_CLASSES | {SNAPSHOT_READONLY}))),
    ServiceCapability("deepseek-4-vision", "DeepSeek 4 Vision", "prepare-only", "PREPARE_ONLY", False, False, True, False, True, "REVIEW", "HIGH", (PUBLIC_PROMPT, SANITIZED_TASK, CODE_PROPOSAL), tuple(sorted(BLOCKED_PAYLOAD_CLASSES | {SNAPSHOT_READONLY}))),
    ServiceCapability("deepseek4", "DeepSeek4", "prepare-only", "PREPARE_ONLY", False, False, True, False, True, "REVIEW", "HIGH", (PUBLIC_PROMPT, SANITIZED_TASK, CODE_PROPOSAL), tuple(sorted(BLOCKED_PAYLOAD_CLASSES | {SNAPSHOT_READONLY}))),
)

AI_COUNCIL_SERVICE_IDS = tuple(
    capability.service_id
    for capability in SERVICE_CAPABILITIES
    if capability.service_id not in {"dry-run", "chrome-devtools-mcp", "hermes"}
)


def build_selector_pack_status(
    *,
    env: dict[str, str] | None = None,
    command_finder: Callable[[str], str | None] | None = None,
) -> dict[str, Any]:
    values = os.environ if env is None else env
    finder = command_finder or shutil.which
    backend_state = _backend_state(values, finder)
    return {
        "schema": SELECTOR_PACK_SCHEMA,
        "version": "v0.2",
        "default_backend": "dry-run",
        "publication_gate": PUBLICATION_GATE,
        "payload_classes": list(PAYLOAD_CLASSES),
        "dry_run_available": True,
        "backends": backend_state,
        "service_count": len(SERVICE_CAPABILITIES),
        "council_service_count": len(AI_COUNCIL_SERVICE_IDS),
        "capabilities": [capability.to_dict() for capability in SERVICE_CAPABILITIES],
        "gates": {
            "BrowserSendGate": "REVIEW_SEND_ONLY_WITH_DOUBLE_OPT_IN",
            "ExternalServiceGate": "REVIEW_PER_SERVICE_ADAPTER",
            "CloudLLMGate": "BLOCK_PRIVATE_WORKSPACE",
            "PublicationGate": PUBLICATION_GATE,
        },
    }


def select_browser_bridge_backend(
    *,
    service_id: str = "dry-run",
    payload_class: str = PUBLIC_PROMPT,
    requested_backend: str = "",
    send_requested: bool = False,
    env: dict[str, str] | None = None,
    command_finder: Callable[[str], str | None] | None = None,
) -> dict[str, Any]:
    values = os.environ if env is None else env
    finder = command_finder or shutil.which
    normalized_payload = normalize_payload_class(payload_class)
    capability = service_capability(service_id)
    backend = requested_backend or capability.adapter
    state = _backend_state(values, finder)
    backend_info = state.get(backend, {"available": False, "configured": False, "enabled": False})
    blocked_reason = blocked_payload_reason(normalized_payload, capability)

    if blocked_reason:
        return _decision(
            capability=capability,
            backend=backend,
            payload_class=normalized_payload,
            mode="BLOCK",
            reason="payload_class_blocked",
            requires_double_opt_in=capability.supports_send,
            safe_to_send=False,
            blocked_payload_reason=blocked_reason,
            backend_info=backend_info,
        )

    if capability.service_id == "dry-run":
        return _decision(
            capability=capability,
            backend="dry-run",
            payload_class=normalized_payload,
            mode="DRY_RUN",
            reason="dry_run_always_available",
            requires_double_opt_in=False,
            safe_to_send=False,
            blocked_payload_reason="",
            backend_info=state["dry-run"],
        )

    if capability.service_id == "chrome-devtools-mcp":
        mode = "READ_ONLY" if backend_info.get("available") else "DRY_RUN"
        return _decision(
            capability=capability,
            backend="chrome-devtools-mcp",
            payload_class=normalized_payload,
            mode=mode,
            reason="read_only_snapshot_available" if mode == "READ_ONLY" else "devtools_mcp_not_available_dry_run_fallback",
            requires_double_opt_in=False,
            safe_to_send=False,
            blocked_payload_reason="",
            backend_info=backend_info,
        )

    if capability.service_id == "kimi":
        send_flags_ready = (
            send_requested
            and values.get(BROWSER_SEND_ENABLE_ENV, "0") == "1"
            and values.get(BROWSER_BRIDGE_ENABLE_ENV, "0") == "1"
            and backend_info.get("available")
            and backend_info.get("safe_url")
        )
        reason = "kimi_send_ready_for_reviewed_public_payload" if send_flags_ready else "kimi_requires_double_opt_in_safe_local_url_and_public_payload"
        return _decision(
            capability=capability,
            backend="kimi-webbridge",
            payload_class=normalized_payload,
            mode="SEND_REVIEW",
            reason=reason,
            requires_double_opt_in=True,
            safe_to_send=bool(send_flags_ready),
            blocked_payload_reason="",
            backend_info=backend_info,
        )

    if capability.adapter == "hermes":
        return _decision(
            capability=capability,
            backend="hermes",
            payload_class=normalized_payload,
            mode="PREPARE_ONLY",
            reason="hermes_adapter_not_live",
            requires_double_opt_in=False,
            safe_to_send=False,
            blocked_payload_reason="",
            backend_info=backend_info,
        )

    return _decision(
        capability=capability,
        backend="dry-run",
        payload_class=normalized_payload,
        mode="PREPARE_ONLY",
        reason="service_without_proven_adapter_prepare_only",
        requires_double_opt_in=False,
        safe_to_send=False,
        blocked_payload_reason="",
        backend_info=state["dry-run"],
    )


def rank_browser_council_services(
    *,
    payload_class: str = PUBLIC_PROMPT,
    send_requested: bool = False,
    env: dict[str, str] | None = None,
    command_finder: Callable[[str], str | None] | None = None,
    services: list[str] | None = None,
) -> dict[str, Any]:
    service_ids = services or list(AI_COUNCIL_SERVICE_IDS)
    rows: list[dict[str, Any]] = []
    for service_id in service_ids:
        decision = select_browser_bridge_backend(
            service_id=service_id,
            payload_class=payload_class,
            send_requested=send_requested,
            env=env,
            command_finder=command_finder,
        )
        row = {
            "service_id": decision["selected_service"],
            "display_name": decision["display_name"],
            "adapter": decision["selected_backend"],
            "classification": council_classification(decision),
            "mode": decision["mode"],
            "scores": score_decision(decision),
            "safe_to_send": decision["safe_to_send"],
            "reason": decision["reason"],
            "blocked_payload_reason": decision["blocked_payload_reason"],
            "publication_gate": PUBLICATION_GATE,
        }
        row["total_score"] = round(
            row["scores"]["adapter_ready"]
            + row["scores"]["payload_safe"]
            + row["scores"]["expected_utility"]
            + row["scores"]["evidence_available"]
            - row["scores"]["risk"],
            3,
        )
        rows.append(row)
    rows.sort(key=lambda item: item["total_score"], reverse=True)
    recommended = rows[0] if rows else {}
    return {
        "schema": COUNCIL_RANKING_SCHEMA,
        "version": "v0.2",
        "payload_class": normalize_payload_class(payload_class),
        "send_requested": send_requested,
        "service_count": len(rows),
        "services": rows,
        "ready_readonly_count": sum(1 for row in rows if row["classification"] == "READY_READONLY"),
        "ready_send_review_count": sum(1 for row in rows if row["classification"] == "READY_SEND_REVIEW"),
        "prepare_only_count": sum(1 for row in rows if row["classification"] == "PREPARE_ONLY"),
        "blocked_count": sum(1 for row in rows if row["classification"] == "BLOCKED"),
        "recommended_service": recommended.get("service_id", ""),
        "recommended_mode": recommended.get("mode", "DRY_RUN"),
        "next_action": _next_action(recommended),
        "online_ai_called": False,
        "browser_backend_called": False,
        "publication_gate": PUBLICATION_GATE,
    }


def normalize_payload_class(payload_class: str) -> str:
    normalized = str(payload_class or PUBLIC_PROMPT).strip().upper().replace("-", "_")
    return normalized if normalized in PAYLOAD_CLASSES else PRIVATE_WORKSPACE_BLOCKED


def service_capability(service_id: str) -> ServiceCapability:
    normalized = str(service_id or "dry-run").strip().lower().replace("_", "-")
    aliases = {
        "deepseek": "deepseek4",
        "deepseek-4": "deepseek4",
        "qwen": "qwen-max",
        "gemini-pro": "gemini-pro",
        "gemini-thinking": "gemini-thinking",
        "copilot-smart": "copilot-smart",
    }
    key = aliases.get(normalized, normalized)
    for capability in SERVICE_CAPABILITIES:
        if capability.service_id == key:
            return capability
    return ServiceCapability(
        service_id=key,
        display_name=key,
        adapter="prepare-only",
        mode="PREPARE_ONLY",
        supports_read=False,
        supports_send=False,
        supports_code_response=True,
        requires_url=False,
        requires_auth=True,
        default_gate="REVIEW",
        risk_level="MEDIUM",
        allowed_payload_classes=(PUBLIC_PROMPT, SANITIZED_TASK, CODE_PROPOSAL),
        blocked_payload_classes=tuple(sorted(BLOCKED_PAYLOAD_CLASSES | {SNAPSHOT_READONLY})),
    )


def blocked_payload_reason(payload_class: str, capability: ServiceCapability) -> str:
    if payload_class in BLOCKED_PAYLOAD_CLASSES:
        return f"{payload_class}:cloud_private_or_protected_payload_blocked"
    if payload_class in capability.blocked_payload_classes:
        return f"{payload_class}:not_allowed_for_{capability.service_id}"
    if payload_class not in capability.allowed_payload_classes:
        return f"{payload_class}:not_allowlisted_for_{capability.service_id}"
    return ""


def council_classification(decision: dict[str, Any]) -> str:
    mode = str(decision.get("mode", "DRY_RUN"))
    if mode == "BLOCK":
        return "BLOCKED"
    if mode == "READ_ONLY":
        return "READY_READONLY"
    if mode == "SEND_REVIEW":
        return "READY_SEND_REVIEW"
    return "PREPARE_ONLY"


def score_decision(decision: dict[str, Any]) -> dict[str, float]:
    classification = council_classification(decision)
    backend_info = decision.get("backend_status", {}) if isinstance(decision.get("backend_status"), dict) else {}
    adapter_ready = 0.2 if classification == "PREPARE_ONLY" else (1.0 if backend_info.get("available") else (0.6 if classification == "READY_SEND_REVIEW" else 0.2))
    payload_safe = 0.0 if decision.get("blocked_payload_reason") else 1.0
    expected_utility = {
        "READY_READONLY": 0.7,
        "READY_SEND_REVIEW": 0.9,
        "PREPARE_ONLY": 0.45,
        "BLOCKED": 0.0,
    }.get(classification, 0.3)
    risk = {
        "LOW": 0.1,
        "MEDIUM": 0.35,
        "HIGH": 0.65,
    }.get(str(decision.get("risk_level", "MEDIUM")), 0.35)
    evidence_available = 1.0 if decision.get("safe_to_send") or classification == "READY_READONLY" else 0.35
    return {
        "adapter_ready": round(adapter_ready, 3),
        "payload_safe": round(payload_safe, 3),
        "expected_utility": round(expected_utility, 3),
        "risk": round(risk, 3),
        "evidence_available": round(evidence_available, 3),
    }


def is_safe_local_url(url: str) -> bool:
    parsed = urlparse(str(url or "").strip())
    if parsed.scheme not in {"http", "https"}:
        return False
    if parsed.username or parsed.password:
        return False
    host = (parsed.hostname or "").lower()
    return host in SAFE_LOCAL_HOSTS


def _backend_state(values: dict[str, str] | os._Environ[str], finder: Callable[[str], str | None]) -> dict[str, dict[str, Any]]:
    bridge_enabled = values.get(BROWSER_BRIDGE_ENABLE_ENV, "0") == "1"
    send_enabled = values.get(BROWSER_SEND_ENABLE_ENV, "0") == "1"
    kimi_url = str(values.get(KIMI_WEBBRIDGE_URL_ENV, "")).strip()
    npx = finder("npx") or ""
    hermes = finder("hermes") or ""
    return {
        "dry-run": {
            "configured": True,
            "enabled": True,
            "available": True,
            "safe_url": True,
            "send_enabled": False,
            "reason": "deterministic local fallback",
        },
        "chrome-devtools-mcp": {
            "configured": bool(npx),
            "enabled": bridge_enabled,
            "available": bool(npx and bridge_enabled),
            "safe_url": True,
            "send_enabled": False,
            "reason": "read-only local snapshot candidate; no auto-install",
        },
        "kimi-webbridge": {
            "configured": bool(kimi_url),
            "enabled": bridge_enabled,
            "available": bool(kimi_url and bridge_enabled and is_safe_local_url(kimi_url)),
            "safe_url": bool(kimi_url and is_safe_local_url(kimi_url)),
            "send_enabled": send_enabled,
            "reason": "send candidate only for safe local WebBridge URL and double opt-in",
        },
        "hermes": {
            "configured": bool(hermes),
            "enabled": bridge_enabled,
            "available": bool(hermes and bridge_enabled),
            "safe_url": True,
            "send_enabled": False,
            "reason": "optional read adapter, not live for council send",
        },
    }


def _decision(
    *,
    capability: ServiceCapability,
    backend: str,
    payload_class: str,
    mode: str,
    reason: str,
    requires_double_opt_in: bool,
    safe_to_send: bool,
    blocked_payload_reason: str,
    backend_info: dict[str, Any],
) -> dict[str, Any]:
    return {
        "schema": SELECTOR_DECISION_SCHEMA,
        "selected_service": capability.service_id,
        "display_name": capability.display_name,
        "selected_backend": backend,
        "adapter": capability.adapter,
        "mode": mode,
        "reason": reason,
        "requires_double_opt_in": requires_double_opt_in,
        "safe_to_send": safe_to_send,
        "blocked_payload_reason": blocked_payload_reason,
        "payload_class": payload_class,
        "supports_read": capability.supports_read,
        "supports_send": capability.supports_send,
        "supports_code_response": capability.supports_code_response,
        "requires_url": capability.requires_url,
        "requires_auth": capability.requires_auth,
        "default_gate": capability.default_gate,
        "risk_level": capability.risk_level,
        "backend_status": backend_info,
        "publication_gate": PUBLICATION_GATE,
        "online_ai_called": False,
        "browser_backend_called": False,
    }


def _next_action(recommended: dict[str, Any]) -> str:
    classification = recommended.get("classification", "")
    if classification == "READY_SEND_REVIEW":
        return "run_kimi_smoke_only_with_double_opt_in_and_public_payload"
    if classification == "READY_READONLY":
        return "run_readonly_local_snapshot"
    if classification == "PREPARE_ONLY":
        return "prepare_review_artifact_no_send"
    if classification == "BLOCKED":
        return "revise_payload_class_before_any_send"
    return "keep_dry_run_default"
