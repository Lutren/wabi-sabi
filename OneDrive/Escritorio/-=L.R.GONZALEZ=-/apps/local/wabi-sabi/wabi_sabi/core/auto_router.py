from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from wabi_sabi.cli.parser import ParsedCommand
from wabi_sabi.core.gate import ActionGate


LOCAL_INTENTS = {"debug_diagnostics", "file_operations"}

CONVERSATION_HINTS = {
    "buen dia",
    "buenas",
    "buenos dias",
    "como estas",
    "cómo estas",
    "como te llamas",
    "cuál es tu nombre",
    "cual es tu nombre",
    "dime tu nombre",
    "estoy probando",
    "hola",
    "probando las funciones",
    "quien eres",
    "quién eres",
    "saludos",
    "tu nombre",
}

CODEX_HINTS = {
    "analiza",
    "decide",
    "decidir",
    "elige",
    "mejor",
    "organiza",
    "plan",
    "siguiente",
    "autonomia",
    "autonomía",
    "implementa",
    "refactor",
    "integra",
    "explica",
    "investiga",
    "prioriza",
    "codex",
}

BLUEPRINT_BRIEF_HINTS = {
    "liberar",
    "redes",
    "post",
    "publicar en redes",
    "sacar algo",
    "sacame algo",
    "sácame algo",
    "solucion a algun problema",
    "solución a algún problema",
    "problema actual",
    "tech que pueda",
}

LOCAL_CODE_HINTS = {
    "crea una funcion",
    "crea una función",
    "genera una funcion",
    "genera una función",
    "helper",
}


@dataclass(frozen=True)
class AutoRouteDecision:
    route: str
    prompt: str
    gate: str
    reasons: list[str] = field(default_factory=list)
    forced: bool = False

    @property
    def ok_to_run(self) -> bool:
        return self.route != "blocked"


def decide_auto_route(
    prompt: str,
    parsed: ParsedCommand,
    provider_status: dict[str, Any],
    *,
    dry_run: bool = False,
) -> AutoRouteDecision:
    directive, clean_prompt = _strip_directive(prompt)
    if directive == "status":
        return AutoRouteDecision("status", clean_prompt, "APPROVE", ["operator_requested_status"], True)
    if not clean_prompt:
        return AutoRouteDecision("blocked", clean_prompt, "BLOCK", ["empty_prompt"], directive is not None)
    gate = ActionGate().evaluate_text(clean_prompt)
    if gate.gate == "BLOCK":
        return AutoRouteDecision("blocked", clean_prompt, gate.gate, gate.reasons, directive is not None)
    if dry_run or directive == "dry":
        return AutoRouteDecision("codex_dry_run", clean_prompt, gate.gate, ["dry_run_requested"], directive is not None)
    if directive == "codex":
        return AutoRouteDecision("codex", clean_prompt, gate.gate, ["operator_forced_codex"], True)
    if directive == "local":
        return AutoRouteDecision("local_agent", clean_prompt, gate.gate, ["operator_forced_local"], True)

    lowered = clean_prompt.lower()
    if _is_conversation(lowered):
        return AutoRouteDecision("local_chat", clean_prompt, gate.gate, ["local_conversation"])
    if _needs_blueprint_brief(lowered):
        return AutoRouteDecision(
            "hybrid_codex",
            clean_prompt,
            gate.gate,
            ["local_blueprint_brief", "codex_background_deepening"],
        )
    if parsed.intent in LOCAL_INTENTS:
        return AutoRouteDecision("local_agent", clean_prompt, gate.gate, [f"local_intent:{parsed.intent}"])
    if parsed.intent == "code_generation" and any(hint in lowered for hint in LOCAL_CODE_HINTS):
        return AutoRouteDecision("local_agent", clean_prompt, gate.gate, ["local_code_artifact_is_enough"])
    if _has_codex_hint(lowered):
        return _codex_or_dry(clean_prompt, gate.gate, provider_status, "codex_hint")
    if parsed.intent in {"local_research", "general"}:
        return _codex_or_dry(clean_prompt, gate.gate, provider_status, f"broad_intent:{parsed.intent}")
    return AutoRouteDecision("local_agent", clean_prompt, gate.gate, [f"default_local:{parsed.intent}"])


def _codex_or_dry(
    prompt: str,
    gate: str,
    provider_status: dict[str, Any],
    reason: str,
) -> AutoRouteDecision:
    provider = provider_status.get("auto_provider", "dry-run")
    if provider == "dry-run":
        return AutoRouteDecision("codex_dry_run", prompt, gate, [reason, "no_model_provider_available"])
    return AutoRouteDecision("codex", prompt, gate, [reason, f"provider:{provider}"])


def _strip_directive(prompt: str) -> tuple[str | None, str]:
    stripped = prompt.strip()
    lowered = stripped.lower()
    exact_directives = {
        "/codex": "codex",
        "codex": "codex",
        "/local": "local",
        "local": "local",
        "/dry": "dry",
        "dry": "dry",
    }
    if lowered in exact_directives:
        return exact_directives[lowered], ""
    directives = {
        "/codex ": "codex",
        "codex:": "codex",
        "/local ": "local",
        "local:": "local",
        "/dry ": "dry",
        "dry:": "dry",
    }
    for prefix, directive in directives.items():
        if lowered.startswith(prefix):
            return directive, stripped[len(prefix) :].strip()
    if lowered in {"/status", "status", "estado"}:
        return "status", stripped
    return None, stripped


def _has_codex_hint(text: str) -> bool:
    return any(hint in text for hint in CODEX_HINTS)


def _is_conversation(text: str) -> bool:
    normalized = (
        text.replace("á", "a")
        .replace("é", "e")
        .replace("í", "i")
        .replace("ó", "o")
        .replace("ú", "u")
        .replace("ü", "u")
    )
    return any(hint in normalized for hint in CONVERSATION_HINTS)


def _needs_blueprint_brief(text: str) -> bool:
    normalized = (
        text.replace("á", "a")
        .replace("é", "e")
        .replace("í", "i")
        .replace("ó", "o")
        .replace("ú", "u")
        .replace("ü", "u")
    )
    return any(hint in normalized for hint in BLUEPRINT_BRIEF_HINTS)
