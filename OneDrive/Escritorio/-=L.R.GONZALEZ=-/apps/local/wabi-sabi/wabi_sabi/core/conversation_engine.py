from __future__ import annotations

import json
import os
import sys
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, TextIO

from wabi_sabi.core.build_assist_cloud import build_assist_default_model_alias, build_build_assist_cloud_status
from wabi_sabi.core.cloud_budget import CloudBudgetGate
from wabi_sabi.core.conversational import ConversationOptions, ConversationSession, format_conversation_payload
from wabi_sabi.core.gate import ActionGate
from wabi_sabi.core.graphics_bridge import GraphicsBridge
from wabi_sabi.core.hypothesis_packet import run_conjecture_counterexample
from wabi_sabi.core.local_apply_readiness import build_safe_json_helper_changes, safe_json_helper_test_commands
from wabi_sabi.core.llm_proposal import llm_cloud_default_enabled, request_llm_proposal
from wabi_sabi.core.memory import LocalMemory
from wabi_sabi.core.redaction import redact_mapping, redact_text
from wabi_sabi.core.tools import write_artifact


CONVERSATION_TURN_SCHEMA = "wabi.conversation_turn.v0_1"
WORK_INTENT_SCHEMA = "wabi.work_intent.v0_1"
TASK_SPEC_SCHEMA = "wabi.conversation_task_spec.v0_1"

INTENT_NAMES = {
    "chat_general",
    "status_query",
    "plan_request",
    "code_request",
    "debug_request",
    "file_task_request",
    "graphics_scene_request",
    "graphics_asset_request",
    "build_assist_request",
    "hypothesis_request",
    "handoff_request",
    "unsafe_or_external_request",
}

HELP_TEXT = """Comandos:
/help                 muestra esta ayuda
/status               estado local de Wabi
/providers            matriz de proveedores, sin secretos
/graphics             capacidades graficas locales plan-only
/tasks                resumen de tareas conversacionales locales
/plan <texto>         crea plan sin aplicar cambios
/work <texto>         convierte pedido en TaskSpec local
/create <texto>       prepara creacion como propuesta gated
/code <texto>         prepara tarea de programacion, no aplica patch
/debug <texto>        prepara diagnostico local
/hypothesis <texto>   formaliza claim + contraejemplo/falsadores
/exit, /quit          cerrar sesion

Lenguaje natural tambien funciona: programa, debuggea, crea escena, genera assets,
usa nvidia para planear, abre tarea, crea handoff, busca contraejemplos."""


@dataclass(frozen=True)
class ConversationEngineOptions:
    codex_provider: str = "auto"
    codex_timeout: int = 35
    allow_cloud: bool = False
    target: str | None = None
    test_commands: tuple[str, ...] = ()
    persist_turns: bool = True
    include_prompt_in_turn: bool = True
    write_artifacts: bool = True


@dataclass
class ConversationSessionState:
    workspace: Path
    runtime_root: Path
    session_id: str = field(default_factory=lambda: time.strftime("wabi-cli-%Y%m%d-%H%M%S"))
    turn_index: int = 0


@dataclass(frozen=True)
class WorkIntent:
    intent_name: str
    confidence: float
    action_gate: str
    needs_cloud: bool
    needs_graphics: bool
    needs_file_write: bool
    proposal_only: bool
    reason: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema": WORK_INTENT_SCHEMA,
            "intent_name": self.intent_name,
            "confidence": self.confidence,
            "action_gate": self.action_gate,
            "needs_cloud": self.needs_cloud,
            "needs_graphics": self.needs_graphics,
            "needs_file_write": self.needs_file_write,
            "proposal_only": self.proposal_only,
            "reason": self.reason,
        }


class ConversationEngine:
    """Shared conversational core for terminal/UI adapters.

    It wraps the existing ConversationSession so chat/status/provider behavior
    stays shared while adding a stable WorkIntent/TaskSpec layer for CLI v0.1.
    """

    def __init__(
        self,
        *,
        workspace: str | Path,
        runtime_root: str | Path,
        options: ConversationEngineOptions | None = None,
    ):
        self.workspace = Path(workspace).resolve()
        self.runtime_root = Path(runtime_root).resolve()
        self.options = options or ConversationEngineOptions()
        self.state = ConversationSessionState(workspace=self.workspace, runtime_root=self.runtime_root)
        self.memory = LocalMemory(self.runtime_root)
        session_options = ConversationOptions(
            codex_provider=self.options.codex_provider,
            codex_timeout=self.options.codex_timeout,
            allow_cloud=self.options.allow_cloud,
            target=self.options.target,
            test_commands=self.options.test_commands,
        )
        self.session = ConversationSession(workspace=self.workspace, runtime_root=self.runtime_root, options=session_options)
        self.graphics = GraphicsBridge(workspace=self.workspace, runtime_root=self.runtime_root)

    def classify_intent(self, user_text: str) -> WorkIntent:
        return classify_intent(user_text)

    def handle_turn(
        self,
        user_text: str,
        session_state: ConversationSessionState | None = None,
    ) -> dict[str, Any]:
        state = session_state or self.state
        state.turn_index += 1
        prompt = user_text.strip()
        if not prompt:
            return self._turn_payload(
                prompt=prompt,
                route="empty",
                ok=True,
                output="",
                intent=WorkIntent("chat_general", 1.0, "APPROVE", False, False, False, True, "empty_prompt"),
                state=state,
            )
        forced, text = _split_command(prompt)
        if forced in {"exit", "quit"} or prompt.lower() in {"exit", "quit", "salir"}:
            intent = WorkIntent("chat_general", 1.0, "APPROVE", False, False, False, True, "operator_exit")
            return self._turn_payload(
                prompt=prompt,
                route="exit",
                ok=True,
                output="Sesion cerrada.",
                intent=intent,
                state=state,
                payload={"should_exit": True},
            )
        if forced == "help":
            intent = WorkIntent("chat_general", 1.0, "APPROVE", False, False, False, True, "operator_help")
            return self._turn_payload(prompt=prompt, route="help", ok=True, output=HELP_TEXT, intent=intent, state=state)
        if forced == "status":
            intent = WorkIntent("status_query", 1.0, "APPROVE", False, False, False, True, "operator_status")
            delegated = self.session.handle("/status")
            return self._from_delegated(prompt=prompt, delegated=delegated, intent=intent, state=state)
        if forced == "providers":
            intent = WorkIntent("status_query", 1.0, "APPROVE", False, False, False, True, "operator_provider_status")
            delegated = self.session.handle("/providers")
            return self._from_delegated(prompt=prompt, delegated=delegated, intent=intent, state=state)
        if forced == "graphics":
            intent = WorkIntent("graphics_scene_request", 0.9, "REVIEW", False, True, False, True, "operator_graphics_status")
            return self.request_graphics_engine_if_needed(intent, text or "status", state=state)
        if forced == "tasks":
            intent = WorkIntent("status_query", 0.8, "APPROVE", False, False, False, True, "operator_tasks_status")
            return self._tasks_payload(prompt=prompt, intent=intent, state=state)
        if forced in {"plan", "work", "create", "code", "debug", "hypothesis"}:
            intent = self._forced_intent(forced, text)
            return self.route_intent(intent, text or prompt, state=state)

        intent = self.classify_intent(prompt)
        return self.route_intent(intent, prompt, state=state)

    def route_intent(self, intent: WorkIntent, user_text: str, *, state: ConversationSessionState | None = None) -> dict[str, Any]:
        state = state or self.state
        if intent.intent_name == "unsafe_or_external_request":
            task = self.create_task_spec(intent, user_text)
            decision = self.apply_only_after_gate(task)
            return self._turn_payload(
                prompt=user_text,
                route="blocked",
                ok=False,
                output="ActionGate bloqueo o dejo en REVIEW: no deploy, no push, no publicacion, no secretos, no borrado.",
                intent=intent,
                state=state,
                payload={"task_spec": task, "apply_decision": decision},
            )
        if intent.needs_graphics:
            return self.request_graphics_engine_if_needed(intent, user_text, state=state)
        if intent.needs_cloud:
            return self.request_build_assist_if_needed(intent, user_text, state=state)
        if intent.intent_name == "hypothesis_request":
            result = run_conjecture_counterexample(
                user_text,
                workspace=self.workspace,
                runtime_root=self.runtime_root,
                persist=self.options.write_artifacts,
            )
            return self._turn_payload(
                prompt=user_text,
                route="hypothesis_plan",
                ok=bool(result.get("ok")),
                output=(
                    "Conjecture/Counterexample packet prepared. No source apply, "
                    "cloud call, publication, or strong claim approval was triggered."
                ),
                intent=intent,
                state=state,
                payload=result,
                artifacts=[str(result["artifact"])] if result.get("artifact") else [],
            )
        if intent.intent_name == "status_query":
            delegated = self.session.handle("/status")
            return self._from_delegated(prompt=user_text, delegated=delegated, intent=intent, state=state)
        if intent.intent_name == "debug_request":
            task = self.create_task_spec(intent, user_text)
            return self._task_response(
                prompt=user_text,
                route="debug_request",
                output="Prepare diagnostico local: revisar logs, reproducir fallo, sugerir tests y no aplicar cambios sin gate.",
                intent=intent,
                task=task,
                state=state,
            )
        if intent.intent_name in {"plan_request", "code_request", "file_task_request", "handoff_request"}:
            task = self.create_task_spec(intent, user_text)
            output = _task_output_for_intent(intent.intent_name)
            return self._task_response(prompt=user_text, route=intent.intent_name, output=output, intent=intent, task=task, state=state)
        delegated = self.session.handle(user_text)
        return self._from_delegated(prompt=user_text, delegated=delegated, intent=intent, state=state)

    def produce_response(self, turn_result: dict[str, Any]) -> str:
        return format_turn_response(turn_result)

    def create_task_spec(self, intent: WorkIntent, user_text: str) -> dict[str, Any]:
        action_gate = intent.action_gate
        implementation = _implementation_contract_for_intent(
            intent_name=intent.intent_name,
            user_text=user_text,
            explicit_target=self.options.target,
            explicit_tests=list(self.options.test_commands),
        )
        return {
            "schema": TASK_SPEC_SCHEMA,
            "intent_name": intent.intent_name,
            "title": _title_for_intent(intent.intent_name),
            "description": redact_text(user_text),
            "action_gate": action_gate,
            "proposal_only": True,
            "needs_cloud": intent.needs_cloud,
            "needs_graphics": intent.needs_graphics,
            "needs_file_write": intent.needs_file_write,
            "cloud_authority": "proposal_only",
            "applied_to_sources": False,
            "publication_gate": "BLOCK",
            "rollback_required": True,
            "rollback_strategy": "RollbackStore snapshot before local mutation.",
            "tests_required": True,
            "affected_paths": implementation["affected_paths"],
            "changes": implementation["changes"],
            "suggested_tests": implementation["suggested_tests"]
            or [
                "python -B -m pytest -q -p no:cacheprovider",
                "python -B -m py_compile wabi_sabi\\cli\\main.py",
            ],
            "safe_next_steps": _safe_steps_for_intent(intent.intent_name),
            "next_action": implementation["next_action"],
            "apply_mode": "local_allowlisted" if intent.needs_file_write else "review_only",
        }

    def request_build_assist_if_needed(
        self,
        intent: WorkIntent,
        user_text: str,
        *,
        state: ConversationSessionState | None = None,
    ) -> dict[str, Any]:
        state = state or self.state
        status = build_build_assist_cloud_status(workspace=self.workspace, runtime_root=self.runtime_root)
        model_alias = build_assist_default_model_alias()
        cloud_budget = CloudBudgetGate(runtime_root=self.runtime_root, session_id=state.session_id).render_status(
            provider="nvidia",
            model_alias=model_alias,
            intent=intent.intent_name,
        )
        task = self.create_task_spec(intent, user_text)
        task["provider"] = "nvidia"
        task["model_alias"] = model_alias
        task["cloud_budget"] = cloud_budget
        llm_proposal = self._maybe_llm_proposal(user_text, intent=intent, task=task, state=state)
        provider_called = bool(llm_proposal.get("cloud_provider_called")) if llm_proposal else False
        budget_gate = cloud_budget.get("budget_gate")
        if provider_called:
            output = (
                "LLM cloud proposal recibido como proposal_only. "
                "Wabi local conserva Gate Preview, Apply Local Preview, rollback y tests."
            )
        elif budget_gate == "CLOUD_BUDGET_EXCEEDED":
            output = (
                "CLOUD_BUDGET_EXCEEDED. No llame cloud. "
                "Prepare plan local/dry-run y conserva NVIDIA proposal_only."
            )
        elif budget_gate == "CLOUD_BUDGET_DRY_RUN":
            output = (
                "CLOUD_BUDGET_DRY_RUN. Falta doble opt-in; respondo con plan local proposal_only "
                "y no llamo provider."
            )
        else:
            output = (
                "CLOUD_BUDGET_READY. Build Assist queda en proposal_only; "
                "el turno conversacional no llama provider ni aplica fuentes."
            )
        payload = {
            "task_spec": task,
            "build_assist": status,
            "cloud_budget": cloud_budget,
            "llm_proposal": llm_proposal,
            "cloud_provider_called": provider_called,
            "applied_to_sources": False,
        }
        return self._turn_payload(
            prompt=user_text,
            route="build_assist_request",
            ok=True,
            output=output,
            intent=intent,
            state=state,
            payload=payload,
            artifacts=[],
        )

    def request_graphics_engine_if_needed(
        self,
        intent: WorkIntent,
        user_text: str,
        *,
        state: ConversationSessionState | None = None,
    ) -> dict[str, Any]:
        state = state or self.state
        if intent.intent_name == "graphics_asset_request":
            plan = self.graphics.create_asset_plan(user_text)
        else:
            plan = self.graphics.create_scene_plan(user_text)
        artifact = self.graphics.write_plan_artifact(plan) if self.options.write_artifacts else None
        status = self.graphics.status()
        llm_proposal = self._maybe_llm_proposal(
            user_text,
            intent=intent,
            task=plan.get("task_spec", {}),
            state=state,
        )
        output = (
            "GraphicsBridge preparado en modo plan-only. "
            f"graphics_live={status['graphics_live']} graphics_plan_ready={status['graphics_plan_ready']}. "
            "No publique, no llame red y no modifique fuentes."
        )
        if llm_proposal and llm_proposal.get("cloud_provider_called"):
            output += " LLM cloud agrego propuesta proposal_only; GraphicsBridge sigue plan-only."
        return self._turn_payload(
            prompt=user_text,
            route=intent.intent_name,
            ok=True,
            output=output,
            intent=intent,
            state=state,
            payload={
                "graphics_status": status,
                "graphics_plan": plan,
                "task_spec": plan.get("task_spec", {}),
                "llm_proposal": llm_proposal,
                "cloud_provider_called": bool(llm_proposal.get("cloud_provider_called")) if llm_proposal else False,
            },
            artifacts=[str(artifact)] if artifact else [],
        )

    def apply_only_after_gate(self, task_spec: dict[str, Any]) -> dict[str, Any]:
        gate = str(task_spec.get("action_gate") or "REVIEW")
        if gate == "BLOCK":
            return {"ok": False, "gate": "BLOCK", "applied_to_sources": False, "reason": "blocked_by_action_gate"}
        return {
            "ok": False,
            "gate": gate,
            "applied_to_sources": False,
            "reason": "proposal_only_requires_explicit_local_apply_path",
        }

    def _forced_intent(self, command: str, text: str) -> WorkIntent:
        if command == "debug":
            base = classify_intent(text or "debug")
            return WorkIntent("debug_request", max(base.confidence, 0.95), base.action_gate, False, False, False, True, "forced_debug_command")
        if command == "code":
            base = classify_intent(text or "code")
            return WorkIntent("code_request", max(base.confidence, 0.95), base.action_gate, False, False, True, True, "forced_code_command")
        if command == "hypothesis":
            base = classify_intent(text or "hypothesis")
            return WorkIntent("hypothesis_request", max(base.confidence, 0.95), base.action_gate, False, False, False, True, "forced_hypothesis_command")
        if command == "create":
            base = classify_intent(text or "create")
            if base.needs_graphics:
                return base
            return WorkIntent("code_request", 0.85, base.action_gate, False, False, True, True, "forced_create_command")
        if command == "work":
            base = classify_intent(text or "work")
            return WorkIntent(base.intent_name, max(base.confidence, 0.85), base.action_gate, base.needs_cloud, base.needs_graphics, base.needs_file_write, True, "forced_work_command")
        return WorkIntent("plan_request", 0.95, ActionGate().evaluate_text(text).gate, False, False, False, True, "forced_plan_command")

    def _task_response(
        self,
        *,
        prompt: str,
        route: str,
        output: str,
        intent: WorkIntent,
        task: dict[str, Any],
        state: ConversationSessionState,
    ) -> dict[str, Any]:
        artifacts: list[str] = []
        if self.options.write_artifacts:
            artifact = write_artifact(
                self.runtime_root / "outputs" / "conversation_tasks",
                "wabi_conversation_task",
                ".json",
                json.dumps(task, indent=2, ensure_ascii=False) + "\n",
            )
            artifacts.append(str(artifact))
        llm_proposal = self._maybe_llm_proposal(prompt, intent=intent, task=task, state=state)
        return self._turn_payload(
            prompt=prompt,
            route=route,
            ok=True,
            output=output,
            intent=intent,
            state=state,
            payload={
                "task_spec": task,
                "llm_proposal": llm_proposal,
                "cloud_provider_called": bool(llm_proposal.get("cloud_provider_called")) if llm_proposal else False,
            },
            artifacts=artifacts,
        )

    def _tasks_payload(self, *, prompt: str, intent: WorkIntent, state: ConversationSessionState) -> dict[str, Any]:
        events = self.memory.tail_events(limit=8)
        task_events = [item for item in events if str(item.get("channel", "")).startswith("wabi_conversation")]
        output = f"Tareas conversacionales recientes: {len(task_events)}. No hay executor automatico activo en v0.1."
        return self._turn_payload(
            prompt=prompt,
            route="tasks",
            ok=True,
            output=output,
            intent=intent,
            state=state,
            payload={"recent_task_events": task_events[-5:]},
        )

    def _from_delegated(
        self,
        *,
        prompt: str,
        delegated: dict[str, Any],
        intent: WorkIntent,
        state: ConversationSessionState,
    ) -> dict[str, Any]:
        output = str(delegated.get("output") or "")
        extra_payload: dict[str, Any] = {"delegated": delegated}
        if str(delegated.get("route") or "") in {"status", "providers"}:
            cloud_budget = self._cloud_budget_status(state)
            output = f"{output}\n\n{_format_cloud_budget_for_chat(cloud_budget)}"
            extra_payload["cloud_budget"] = cloud_budget
        return self._turn_payload(
            prompt=prompt,
            route=str(delegated.get("route") or intent.intent_name),
            ok=bool(delegated.get("ok")),
            output=output,
            intent=intent,
            state=state,
            gate=str(delegated.get("gate") or intent.action_gate),
            payload=extra_payload,
            artifacts=[str(item) for item in delegated.get("artifacts", [])],
            provider_status=delegated.get("provider_status", {}),
        )

    def _cloud_budget_status(self, state: ConversationSessionState) -> dict[str, Any]:
        return CloudBudgetGate(runtime_root=self.runtime_root, session_id=state.session_id).render_status(
            provider="nvidia",
            model_alias=build_assist_default_model_alias(),
            intent="conversation_status",
        )

    def _maybe_llm_proposal(
        self,
        prompt: str,
        *,
        intent: WorkIntent,
        task: dict[str, Any],
        state: ConversationSessionState,
    ) -> dict[str, Any]:
        if not llm_cloud_default_enabled():
            return {}
        if intent.intent_name not in {
            "plan_request",
            "code_request",
            "debug_request",
            "file_task_request",
            "graphics_scene_request",
            "graphics_asset_request",
            "build_assist_request",
        }:
            return {}
        return request_llm_proposal(
            workspace=self.workspace,
            runtime_root=self.runtime_root,
            user_text=prompt,
            intent_name=intent.intent_name,
            task_spec=task,
            session_id=state.session_id,
        )

    def _turn_payload(
        self,
        *,
        prompt: str,
        route: str,
        ok: bool,
        output: str,
        intent: WorkIntent,
        state: ConversationSessionState,
        gate: str | None = None,
        payload: dict[str, Any] | None = None,
        artifacts: list[str] | None = None,
        provider_status: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        payload_data = payload or {}
        raw_result: dict[str, Any] = {
            "schema": CONVERSATION_TURN_SCHEMA,
            "ok": ok,
            "route": route,
            "intent_name": intent.intent_name,
            "intent": intent.to_dict(),
            "gate": gate or intent.action_gate,
            "output": output,
            "proposal_only": True,
            "cloud_provider_called": bool(payload_data.get("cloud_provider_called", False)),
            "applied_to_sources": bool(payload_data.get("applied_to_sources", False)),
            "secrets_printed": False,
            "publication_gate": "BLOCK",
            "session_id": state.session_id,
            "turn_index": state.turn_index,
            "artifacts": artifacts or [],
            "provider_status": provider_status or {},
            "payload": payload_data,
        }
        if self.options.include_prompt_in_turn:
            raw_result["prompt"] = prompt
        result = redact_mapping(raw_result)
        self._log_turn(result)
        return result

    def _log_turn(self, result: dict[str, Any]) -> None:
        if not self.options.persist_turns:
            return
        if result.get("route") == "empty":
            return
        self.memory.append_event(
            {
                "channel": "wabi_conversation_cli",
                "route": result.get("route"),
                "intent_name": result.get("intent_name"),
                "gate": result.get("gate"),
                "ok": result.get("ok"),
                "cloud_provider_called": result.get("cloud_provider_called", False),
                "applied_to_sources": result.get("applied_to_sources", False),
                "artifacts": result.get("artifacts", [])[:5],
            }
        )
        self.memory.append_memory(
            {
                "channel": "wabi_conversation_cli",
                "prompt": result.get("prompt", ""),
                "route": result.get("route"),
                "intent_name": result.get("intent_name"),
                "gate": result.get("gate"),
                "ok": result.get("ok"),
                "output": str(result.get("output") or "")[:900],
                "artifacts": result.get("artifacts", [])[:3],
            }
        )


def classify_intent(user_text: str) -> WorkIntent:
    text = _normalize(user_text)
    gate_decision = ActionGate().evaluate_text(user_text)
    unsafe_terms = {
        "deploy",
        "push",
        "publica",
        "publicar",
        "borra",
        "borrar",
        "delete",
        "token",
        "secret",
        "secreto",
        ".env",
        "api key",
        "browserbridge live",
        "browser bridge live",
    }
    if gate_decision.gate == "BLOCK" or any(term in text for term in unsafe_terms):
        return WorkIntent("unsafe_or_external_request", 0.95, "BLOCK", False, False, False, True, "unsafe_or_external_boundary")
    if any(term in text for term in {"asset", "assets", "sprite", "sprites", "icono", "iconos", "tile", "tiles", "atlas"}):
        return WorkIntent("graphics_asset_request", 0.88, gate_decision.gate, False, True, False, True, "graphics_asset_intent")
    if any(term in text for term in {"escena", "scene", "duat city", "motor grafico", "motor gráfico", "renderer", "canvas", "nodos de agentes"}):
        return WorkIntent("graphics_scene_request", 0.9, gate_decision.gate, False, True, False, True, "graphics_scene_intent")
    if any(term in text for term in {"debug", "debuggea", "debuguea", "diagnostica", "falla", "fallo", "error", "arregla"}):
        return WorkIntent("debug_request", 0.86, gate_decision.gate, False, False, False, True, "debug_intent")
    if any(term in text for term in {"usa nvidia", "nvidia", "cloud", "build assist", "build-assist", "modelo cloud"}):
        return WorkIntent("build_assist_request", 0.9, gate_decision.gate, True, False, False, True, "cloud_build_assist_intent")
    if any(
        term in text
        for term in {
            "hipotesis",
            "hipótesis",
            "hypothesis",
            "conjetura",
            "conjecture",
            "contraejemplo",
            "counterexample",
            "falsador",
            "falsifier",
            "unit distance",
        }
    ):
        return WorkIntent("hypothesis_request", 0.9, gate_decision.gate, False, False, False, True, "hypothesis_counterexample_intent")
    if any(term in text for term in {"programa", "codigo", "código", "helper", "funcion", "función", "componente", "implementa", "refactor"}):
        return WorkIntent("code_request", 0.88, gate_decision.gate, False, False, True, True, "code_intent")
    if any(term in text for term in {"abre una tarea", "archivo", "file", "workpack", "task"}):
        return WorkIntent("file_task_request", 0.78, gate_decision.gate, False, False, True, True, "file_task_intent")
    if any(term in text for term in {"handoff", "brief", "fingerprint", "continuidad", "next session"}):
        return WorkIntent("handoff_request", 0.84, gate_decision.gate, False, False, False, True, "handoff_intent")
    if any(term in text for term in {"plan", "planea", "haz un plan", "planear"}):
        return WorkIntent("plan_request", 0.8, gate_decision.gate, False, False, False, True, "plan_intent")
    if any(term in text for term in {"status", "estado", "providers", "proveedores", "como va"}):
        return WorkIntent("status_query", 0.82, gate_decision.gate, False, False, False, True, "status_intent")
    return WorkIntent("chat_general", 0.7, gate_decision.gate, False, False, False, True, "general_chat")


def create_task_spec(intent: WorkIntent, user_text: str) -> dict[str, Any]:
    return ConversationEngine(workspace=Path.cwd(), runtime_root=Path.cwd() / "runtime").create_task_spec(intent, user_text)


def request_build_assist_if_needed(intent: WorkIntent, user_text: str, engine: ConversationEngine) -> dict[str, Any]:
    return engine.request_build_assist_if_needed(intent, user_text)


def request_graphics_engine_if_needed(intent: WorkIntent, user_text: str, engine: ConversationEngine) -> dict[str, Any]:
    return engine.request_graphics_engine_if_needed(intent, user_text)


def apply_only_after_gate(task_spec: dict[str, Any]) -> dict[str, Any]:
    gate = str(task_spec.get("action_gate") or "REVIEW")
    if gate == "BLOCK":
        return {"ok": False, "gate": "BLOCK", "applied_to_sources": False, "reason": "blocked_by_action_gate"}
    return {"ok": False, "gate": gate, "applied_to_sources": False, "reason": "proposal_only_requires_explicit_local_apply_path"}


def handle_turn(user_text: str, session_state: ConversationSessionState | None = None) -> dict[str, Any]:
    state = session_state or ConversationSessionState(workspace=Path.cwd(), runtime_root=Path.cwd() / "runtime")
    engine = ConversationEngine(workspace=state.workspace, runtime_root=state.runtime_root)
    return engine.handle_turn(user_text, state)


def route_intent(intent: WorkIntent, engine: ConversationEngine, user_text: str) -> dict[str, Any]:
    return engine.route_intent(intent, user_text)


def produce_response(turn_result: dict[str, Any]) -> str:
    return format_turn_response(turn_result)


def start_interactive_session(
    engine: ConversationEngine,
    *,
    input_stream: TextIO | None = None,
    output_stream: TextIO | None = None,
) -> int:
    input_stream = input_stream or sys.stdin
    output_stream = output_stream or sys.stdout
    status = engine.graphics.status()
    cloud_mode = "proposal_only"
    graphics_line = "available" if status.get("available") else "unavailable_plan_stub"
    print("Wabi-Sabi Conversational CLI", file=output_stream)
    print("mode: local-first", file=output_stream)
    print(f"cloud: {cloud_mode}", file=output_stream)
    print(f"graphics: {graphics_line}", file=output_stream)
    print("type /help for commands", file=output_stream)
    while True:
        print("wabi> ", end="", file=output_stream, flush=True)
        line = input_stream.readline()
        if line == "":
            print("", file=output_stream)
            return 0
        payload = engine.handle_turn(line.strip())
        text = engine.produce_response(payload)
        if text:
            print(text, file=output_stream)
        if payload.get("route") == "exit" or payload.get("payload", {}).get("should_exit"):
            return 0


def format_turn_response(payload: dict[str, Any]) -> str:
    if payload.get("route") == "empty":
        return ""
    if payload.get("route") == "help":
        return str(payload.get("output") or "")
    delegated = payload.get("payload", {}).get("delegated")
    if isinstance(delegated, dict) and delegated.get("route") in {"local_chat", "diff"}:
        return format_conversation_payload(delegated)
    output = str(payload.get("output") or "")
    if payload.get("route") == "exit":
        return f"Wabi-Sabi: {output}"
    suffix = f"[intent={payload.get('intent_name')} gate={payload.get('gate')} proposal_only=YES]"
    return f"Wabi-Sabi: {output}\n{suffix}"


def _split_command(prompt: str) -> tuple[str | None, str]:
    if not prompt.startswith("/"):
        return None, prompt
    parts = prompt[1:].split(maxsplit=1)
    command = parts[0].strip().lower() if parts else ""
    text = parts[1].strip() if len(parts) > 1 else ""
    aliases = {
        "salir": "exit",
        "ayuda": "help",
        "estado": "status",
        "proveedores": "providers",
        "grafica": "graphics",
        "graficas": "graphics",
        "tareas": "tasks",
        "crear": "create",
        "codigo": "code",
        "depurar": "debug",
        "hipotesis": "hypothesis",
        "conjetura": "hypothesis",
        "contraejemplo": "hypothesis",
        "falsador": "hypothesis",
    }
    return aliases.get(command, command), text


def _normalize(text: str) -> str:
    return str(text or "").strip().lower()


def _title_for_intent(intent_name: str) -> str:
    titles = {
        "plan_request": "Prepare local plan",
        "code_request": "Prepare code proposal",
        "debug_request": "Prepare debug plan",
        "file_task_request": "Prepare file task",
        "handoff_request": "Prepare handoff",
        "build_assist_request": "Prepare NVIDIA proposal-only assist",
        "graphics_scene_request": "Prepare graphics scene plan",
        "graphics_asset_request": "Prepare graphics asset plan",
        "hypothesis_request": "Prepare hypothesis/counterexample packet",
    }
    return titles.get(intent_name, "Prepare conversational task")


def _task_output_for_intent(intent_name: str) -> str:
    outputs = {
        "plan_request": "Plan local preparado como TaskSpec proposal_only. No aplique cambios.",
        "code_request": "Tarea de programacion preparada. Patch/apply queda separado por ActionGate y rollback.",
        "file_task_request": "Tarea de archivo preparada. Escritura real requiere gate local y ruta allowlisted.",
        "handoff_request": "Tarea de handoff preparada. Se puede convertir en artefacto local verificable.",
        "hypothesis_request": "Conjetura formalizada como HypothesisPacket. Ejecuta falsadores antes de canon/producto/publicacion.",
    }
    return outputs.get(intent_name, "TaskSpec local preparado como propuesta.")


def _implementation_contract_for_intent(
    *,
    intent_name: str,
    user_text: str,
    explicit_target: str | None,
    explicit_tests: list[str],
) -> dict[str, Any]:
    if intent_name != "code_request":
        return {
            "affected_paths": [],
            "changes": [],
            "suggested_tests": explicit_tests,
            "next_action": "Review TaskSpec. No source apply is available for this intent.",
        }
    if _looks_like_json_helper(user_text):
        changes = build_safe_json_helper_changes()
        return {
            "affected_paths": [str(change["target"]) for change in changes],
            "changes": changes,
            "suggested_tests": explicit_tests or safe_json_helper_test_commands(),
            "next_action": "Run Apply Local Preview, review diff/routes/tests, then Apply Local if readiness is PASS.",
        }
    if explicit_target:
        return {
            "affected_paths": [explicit_target],
            "changes": [],
            "suggested_tests": explicit_tests,
            "next_action": "Add explicit patch content or use a supported local patch candidate before apply.",
        }
    return {
        "affected_paths": [],
        "changes": [],
        "suggested_tests": explicit_tests,
        "next_action": "Review requested change and add explicit affected paths before local apply.",
    }


def _looks_like_json_helper(text: str) -> bool:
    normalized = _normalize(text)
    return "json" in normalized and any(marker in normalized for marker in ["helper", "valid", "seguro", "safe"])


def _format_cloud_budget_for_chat(cloud_budget: dict[str, Any]) -> str:
    return "\n".join(
        [
            "cloud_budget:",
            f"  mode: {cloud_budget.get('mode')}",
            f"  provider: {cloud_budget.get('provider')}",
            f"  model: {cloud_budget.get('model')}",
            f"  session_calls_used: {cloud_budget.get('session_calls_used')}",
            f"  session_calls_limit: {cloud_budget.get('session_calls_limit')}",
            f"  daily_calls_used: {cloud_budget.get('daily_calls_used')}",
            f"  daily_calls_limit: {cloud_budget.get('daily_calls_limit')}",
            f"  remaining_session_calls: {cloud_budget.get('remaining_session_calls')}",
            f"  remaining_daily_calls: {cloud_budget.get('remaining_daily_calls')}",
            f"  cloud_live_ready: {cloud_budget.get('cloud_live_ready')}",
            f"  double_opt_in: {cloud_budget.get('double_opt_in')}",
            f"  budget_gate: {cloud_budget.get('budget_gate')}",
            f"  next_cloud_call_allowed: {cloud_budget.get('next_cloud_call_allowed')}",
        ]
    )


def _safe_steps_for_intent(intent_name: str) -> list[str]:
    common = [
        "Mantener proposal_only hasta que exista ruta exacta y evidencia.",
        "No imprimir secretos ni leer .env.",
        "No publicar, deployar, pushear ni ejecutar BrowserBridge live.",
    ]
    if intent_name == "code_request":
        return [
            "Identificar archivo destino dentro del workspace.",
            "Crear patch candidate con rollback.",
            "Ejecutar tests focales antes de aplicar.",
            *common,
        ]
    if intent_name == "debug_request":
        return [
            "Reproducir fallo con comando local minimo.",
            "Capturar salida sanitizada.",
            "Proponer fix y test antes de aplicar.",
            *common,
        ]
    if intent_name == "handoff_request":
        return ["Crear fingerprint/brief local.", "Citar evidencia de comandos.", *common]
    if intent_name == "hypothesis_request":
        return [
            "Formalizar claim, contraafirmacion y falsadores.",
            "Ejecutar un falsador local con evidencia.",
            "Registrar WitnessLog antes de reutilizar en canon/producto.",
            *common,
        ]
    return ["Convertir pedido en pasos verificables.", "Registrar artefacto local.", *common]
