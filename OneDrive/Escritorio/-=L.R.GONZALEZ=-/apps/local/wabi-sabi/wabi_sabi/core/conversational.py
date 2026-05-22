from __future__ import annotations

import os
import re
import shutil
import time
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from wabi_sabi.core.conversation import local_chat_response
from wabi_sabi.core.gate import ActionGate
from wabi_sabi.core.live_context import load_live_context
from wabi_sabi.core.memory import LocalMemory
from wabi_sabi.core.patch_planner import (
    PatchPlan,
    build_file_patch_plan,
    load_patch_plan,
    resolve_workspace_text_target,
    write_patch_diff,
    write_patch_plan,
)
from wabi_sabi.core.programming import build_new_python_text, code_for_prompt
from wabi_sabi.core.provider_onboarding import format_provider_onboarding, normalize_provider, provider_onboarding_report
from wabi_sabi.core.provider_orchestrator import ProviderOrchestrator
from wabi_sabi.core.redaction import redact_text
from wabi_sabi.core.rollback_store import RollbackStore
from wabi_sabi.core.runtime_diagnostics import (
    build_doctor_report,
    build_provider_report,
    debug_deepseek_provider,
    format_deepseek_debug,
    format_doctor_report,
    format_provider_report,
)
from wabi_sabi.core.safe_executor import SafeExecutor
from wabi_sabi.core.config import RuntimeConfig
from wabi_sabi.engine import default_engine_manifest


PROTECTED_CLOUD_HINTS = {
    ".env",
    "api key",
    "apikey",
    "credential",
    "credencial",
    "dataset privado",
    "datasets privados",
    "duat completo",
    "duat/geodia privado",
    "geodia completo",
    "libro completo",
    "libros",
    "manuscrito",
    "password",
    "private key",
    "raw prompt",
    "raw prompts",
    "rpg",
    "secreto",
    "secret",
    "source vault",
    "source_zips",
    "tcg",
    "token",
    "wabi-sabi internals",
}

PROGRAMMING_HINTS = {
    "agrega",
    "anade",
    "añade",
    "arregla",
    "codifica",
    "crea",
    "edita",
    "funcion",
    "función",
    "implementa",
    "modifica",
    "programa",
    "refactor",
    "revisa el repo",
    "revisa este repo",
    "revisa este proyecto",
    "corre tests",
    "ejecuta tests",
    "haz un diff",
    "muestra diff",
    "diff",
}

DIFF_HINTS = {"diff", "haz un diff", "muestra diff", "muestrame diff", "muéstrame diff"}
APPLY_HINTS = {"aplica", "aplicar", "si aplica", "sí aplica", "confirmo", "aplica el cambio"}
ROLLBACK_HINTS = {"rollback", "revierte", "revertir", "haz rollback", "deshacer", "deshaz"}
PROVIDER_SETUP_HINTS = {
    "activa openrouter",
    "activa qwen",
    "agrega mis modelos gratis",
    "agrega openrouter",
    "agrega qwen",
    "configura deepseek",
    "configura mis apis",
    "configura mis apis gratis",
    "configura openrouter",
    "configura qwen",
    "revisa deepseek",
    "usa mis apis gratis",
    "usa mis apis gratis para programar",
}


@dataclass(frozen=True)
class ConversationOptions:
    codex_provider: str = "auto"
    codex_timeout: int = 60
    allow_cloud: bool = True
    provider_order: str = "ollama,nvidia,qwen,deepseek,openrouter,codex,dry-run"
    target: str | None = None
    test_commands: tuple[str, ...] = ()


class ConversationSession:
    def __init__(self, *, workspace: str | Path, runtime_root: str | Path, options: ConversationOptions | None = None):
        self.workspace = Path(workspace).resolve()
        self.runtime_root = Path(runtime_root).resolve()
        self.options = options or ConversationOptions()
        self.memory = LocalMemory(self.runtime_root)
        self.pending_plan: PatchPlan | None = None
        self.pending_plan_path: Path | None = None
        self.pending_diff_path: Path | None = None
        self.mode = "chat"
        self.selected_provider = options.codex_provider if options and options.codex_provider != "auto" else "auto"
        self.last_applied_plan_id: str | None = None
        self.session_dir = self._create_session_dir()
        self._configure_provider_env()
        self.orchestrator = ProviderOrchestrator(workspace=self.workspace, runtime_root=self.runtime_root)

    def _create_session_dir(self) -> Path:
        stamp = time.strftime("%Y%m%d_%H%M%S")
        sessions_root = self.runtime_root / "sessions"
        session_dir = sessions_root / f"session_{stamp}_{os.getpid()}"
        for child in ("plans", "diffs", "rollbacks"):
            (session_dir / child).mkdir(parents=True, exist_ok=True)
        session_data = {
            "schema": "wabi.conversation_session.v1",
            "created_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
            "workspace": str(self.workspace),
            "runtime_root": str(self.runtime_root),
            "mode": self.mode,
            "selected_provider": self.selected_provider,
            "cloud_allowed": self.options.allow_cloud,
        }
        (session_dir / "session.json").write_text(json.dumps(session_data, indent=2, ensure_ascii=False), encoding="utf-8")
        (session_dir / "workspace.json").write_text(
            json.dumps({"workspace": str(self.workspace), "policy": "current_directory_with_confirmation"}, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )
        (session_dir / "handoff.md").write_text(
            "# Wabi-Sabi Session Handoff\n\nEstado: sesion abierta.\n\nDo not: publicar, push, deploy, imprimir secretos o aplicar sin confirmacion.\n",
            encoding="utf-8",
        )
        return session_dir

    def handle(self, text: str) -> dict[str, Any]:
        prompt = text.strip()
        if not prompt:
            return self._payload(route="empty", ok=True, output="", reasons=["empty_prompt"])
        normalized = _normalize(prompt)
        if prompt.lower() in {"/exit", "exit", "salir", "/salir", "/quit", "quit"}:
            return self._payload(route="exit", ok=True, output="Sesion cerrada.", reasons=["operator_exit"])
        if prompt.lower() in {"/help", "help", "ayuda", "/ayuda"}:
            return self._help_payload()
        if prompt.lower() in {"/status", "status", "estado"}:
            return self._status_payload()
        if prompt.lower() in {"/providers", "providers", "/proveedores", "proveedores"}:
            return self._providers_payload()
        if prompt.lower() in {"/setup", "/setup providers", "/setup proveedores"}:
            return self._provider_setup_payload(prompt)
        if prompt.lower().startswith("/setup "):
            return self._provider_setup_payload(prompt)
        if prompt.lower() in {"/doctor", "doctor", "diagnostico", "diagnóstico"}:
            return self._doctor_payload()
        if prompt.lower().startswith("/workspace") or prompt.lower().startswith("workspace"):
            return self._workspace_payload(prompt)
        if prompt.lower() == "/mode" or prompt.lower().startswith("/mode "):
            return self._mode_payload(prompt)
        if prompt.lower() == "/model" or prompt.lower().startswith("/model "):
            return self._model_select_payload(prompt)
        if prompt.lower() in {"/memory", "memory", "memoria"}:
            summary = self.memory.conversation_summary()
            return self._payload(
                route="memory",
                ok=True,
                output=summary or "No hay memoria conversacional local todavia.",
                reasons=["operator_memory"],
            )
        if prompt.lower() in {"/diff", "diff"} or any(hint in normalized for hint in DIFF_HINTS):
            return self._diff_payload()
        if prompt.lower().startswith("/rollback") or prompt.lower().startswith("rollback") or any(hint in normalized for hint in ROLLBACK_HINTS):
            return self._rollback_payload(prompt)
        if prompt.lower() in {"/apply", "apply", "aplica", "/aplica", "aplicar", "/aplicar", "si aplica", "sí aplica", "confirmo"} or any(hint in normalized for hint in APPLY_HINTS):
            return self._apply_payload()
        if prompt.lower().startswith("/plan "):
            return self._plan_payload(prompt[6:].strip())

        if _looks_like_provider_setup(prompt):
            return self._provider_setup_payload(prompt)

        gate = ActionGate().evaluate_text(prompt)
        if _looks_like_live_context_request(prompt):
            return self._live_context_payload(prompt, gate="APPROVE")
        if gate.gate == "BLOCK":
            return self._payload(
                route="blocked",
                ok=False,
                gate=gate.gate,
                output="ActionGate bloqueo el pedido: no publico, no borro, no leo secretos y no cruzo frontera privada.",
                reasons=gate.reasons,
                prompt=prompt,
            )
        if _looks_like_repo_review(prompt):
            return self._coding_intent_payload(prompt, gate=gate.gate)
        if _looks_like_programming(prompt):
            return self._plan_payload(prompt, gate=gate.gate)
        if _looks_like_casual(prompt):
            status = self.orchestrator.status()
            if self._should_try_model_for_casual(prompt, status) and not _cloud_boundary_blocked(prompt):
                model_payload = self._model_payload(prompt, gate=gate.gate)
                if model_payload.get("ok") and _is_substantive_model_output(str(model_payload.get("output") or "")):
                    model_payload["reasons"] = ["model_conversation_preferred", *model_payload.get("reasons", [])]
                    return model_payload
            return self._payload(
                route="local_chat",
                ok=True,
                gate=gate.gate,
                output=local_chat_response(prompt, status, self.memory.tail_memory(limit=12)),
                reasons=["local_conversation"],
                prompt=prompt,
                provider_status=status,
            )
        return self._model_payload(prompt, gate=gate.gate)

    def _should_try_model_for_casual(self, prompt: str, status: dict[str, Any]) -> bool:
        normalized = _normalize(prompt)
        if any(item in normalized for item in {"hola", "estas ahi", "como estas", "quien eres", "que eres"}):
            return False
        if os.environ.get("MEDIOEVO_NO_MODEL_MODE", "0") == "1":
            return False
        auto_provider = str(status.get("auto_provider") or "").lower()
        if auto_provider in {"", "dry-run"}:
            return False
        if auto_provider == "codex" and not status.get("codex", {}).get("codex_cli", {}).get("available"):
            return False
        return True

    def _configure_provider_env(self) -> None:
        if not self.options.allow_cloud:
            return
        os.environ.setdefault("WABI_ALLOW_CLOUD_PROVIDERS", "1")
        # When cloud is globally enabled, let ProviderOrchestrator.provider_order()
        # compute the cloud-first order dynamically based on configured adapters.
        # Only pin WABI_PROVIDER_ORDER when the operator has NOT enabled cloud globally,
        # so we don't override the dynamic cloud-first logic with a stale ollama-first list.
        if os.environ.get("WABI_ALLOW_CLOUD_PROVIDERS", "0") != "1":
            os.environ.setdefault("WABI_PROVIDER_ORDER", self.options.provider_order)

    def _status_payload(self) -> dict[str, Any]:
        status = self.orchestrator.status()
        ollama = status.get("ollama", {}) if isinstance(status.get("ollama"), dict) else {}
        base_model = str(ollama.get("base_model") or "")
        base_model_available = bool(ollama.get("base_model_available"))
        running = ollama.get("running", []) if isinstance(ollama.get("running"), list) else []
        cloud_line = (
            "Cloud: opt-in activo para esta sesion; los secretos siguen redactados."
            if self.options.allow_cloud
            else "Cloud: bloqueado por defecto en esta sesion local; usa --cloud solo para una revision explicita."
        )
        if base_model_available:
            if base_model in running:
                local_model_line = f"Modelo local: {base_model} disponible y cargado."
            elif running:
                local_model_line = f"Modelo local: {base_model} disponible; activo ahora: {', '.join(running)}."
            else:
                local_model_line = f"Modelo local: {base_model} disponible; se carga al primer prompt local."
        else:
            local_model_line = "Modelo local: no verificado en esta sesion; Codex/dry-run quedan como fallback seguro."
        engine_manifest = default_engine_manifest()
        output = [
            "Wabi-Sabi conversacional activo.",
            f"Proveedor auto: {status.get('auto_provider')}",
            f"Orden: {', '.join(status.get('provider_order', []))}",
            cloud_line,
            local_model_line,
            f"Motor modular: disponible ({len(engine_manifest.get('modules', {}))} modulos clean-room).",
            "Modo programador: plan primero, /apply despues.",
        ]
        return self._payload(
            route="status",
            ok=True,
            output="\n".join(output),
            reasons=["operator_status"],
            provider_status=status,
        )

    def _providers_payload(self) -> dict[str, Any]:
        report = build_provider_report(runtime_root=self.runtime_root, smoke=False)
        lines = [
            f"Modelo seleccionado: {self.selected_provider}",
            f"Orden runtime: {', '.join(self.orchestrator.provider_order())}",
            "",
            format_provider_report(report),
        ]
        return self._payload(
            route="providers",
            ok=True,
            output="\n".join(lines),
            reasons=["operator_provider_matrix"],
            provider_status=report,
        )

    def _provider_setup_payload(self, prompt: str) -> dict[str, Any]:
        provider = _provider_from_setup_prompt(prompt)
        setup = provider_onboarding_report(provider)
        lines = [
            format_provider_onboarding(setup),
            "",
            "Captura segura:",
            "- Si quieres guardar una clave desde esta terminal, usa /secret ENV_KEY.",
            "- Ejemplos: /secret DASHSCOPE_API_KEY, /secret QWEN_API_KEY, /secret DEEPSEEK_API_KEY, /secret OPENROUTER_API_KEY.",
            "- La captura usa entrada oculta cuando la terminal lo permite; el valor no se escribe en logs ni handoff.",
            "",
            "Router auto_free_first:",
            "- Chat: local -> nvidia -> qwen -> deepseek -> openrouter.",
            "- Programacion: nvidia -> deepseek -> qwen -> local.",
            "- Privado/sensible: local o confirmacion antes de cloud.",
        ]
        if provider == "deepseek":
            debug = debug_deepseek_provider(timeout=12)
            lines.extend(["", "DeepSeek debug sanitizado:", format_deepseek_debug(debug)])
        return self._payload(
            route="provider_setup",
            ok=True,
            output="\n".join(lines),
            reasons=["natural_provider_setup_intent", "no_secret_values_logged"],
            prompt=prompt,
            payload={"provider": provider or "all", "setup": setup},
        )

    def _doctor_payload(self) -> dict[str, Any]:
        config = RuntimeConfig(workspace=self.workspace, runtime_root=self.runtime_root, registry_path=self.runtime_root / "_session_registry_unused.json")
        report = build_doctor_report(config)
        return self._payload(
            route="doctor",
            ok=report.get("result") in {"PASS", "REVIEW"},
            gate="APPROVE" if report.get("result") != "BLOCK" else "BLOCK",
            output=format_doctor_report(report),
            reasons=["operator_doctor"],
            payload=report,
        )

    def _help_payload(self) -> dict[str, Any]:
        return self._payload(
            route="help",
            ok=True,
            output=(
                "Escribe normal. Para codigo: pide crear, arreglar, revisar, diff, aplica o rollback.\n"
                "Comandos utiles: /providers, /setup providers, /setup qwen, /setup deepseek, /secret ENV_KEY, "
                "/doctor, /workspace [path], /mode chat|code, /model auto|nvidia|qwen|deepseek|local, "
                "/diff, /apply, /rollback, /salir."
            ),
            reasons=["operator_help"],
        )

    def _workspace_payload(self, prompt: str) -> dict[str, Any]:
        parts = prompt.split(maxsplit=1)
        if len(parts) == 1:
            return self._payload(
                route="workspace",
                ok=True,
                output=f"Workspace actual: {self.workspace}",
                reasons=["workspace_status"],
            )
        candidate = Path(parts[1]).expanduser()
        if not candidate.is_absolute():
            candidate = (self.workspace / candidate).resolve()
        if not candidate.exists() or not candidate.is_dir():
            return self._payload(
                route="workspace",
                ok=False,
                gate="REVIEW",
                output=f"No encontre ese workspace: {candidate}",
                reasons=["workspace_not_found"],
            )
        self.workspace = candidate.resolve()
        self.orchestrator = ProviderOrchestrator(workspace=self.workspace, runtime_root=self.runtime_root)
        (self.session_dir / "workspace.json").write_text(
            json.dumps({"workspace": str(self.workspace), "policy": "operator_selected"}, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )
        return self._payload(
            route="workspace",
            ok=True,
            output=f"Workspace activo cambiado a: {self.workspace}",
            reasons=["workspace_selected"],
        )

    def _mode_payload(self, prompt: str) -> dict[str, Any]:
        parts = prompt.split(maxsplit=1)
        requested = parts[1].strip().lower() if len(parts) > 1 else self.mode
        if requested not in {"chat", "code"}:
            return self._payload(route="mode", ok=False, gate="REVIEW", output="Modo valido: chat o code.", reasons=["invalid_mode"])
        self.mode = requested
        return self._payload(route="mode", ok=True, output=f"Modo activo: {self.mode}", reasons=["mode_selected"])

    def _model_select_payload(self, prompt: str) -> dict[str, Any]:
        parts = prompt.split(maxsplit=1)
        requested = parts[1].strip().lower() if len(parts) > 1 else self.selected_provider
        aliases = {
            "auto": "auto",
            "nvidia": "nvidia",
            "qwen": "qwen",
            "dashscope": "qwen",
            "dashscope_qwen": "qwen",
            "deepseek": "deepseek",
            "local": "local",
            "ollama": "local",
            "openrouter": "openrouter",
        }
        if requested not in aliases:
            return self._payload(
                route="model",
                ok=False,
                gate="REVIEW",
                output="Modelo valido: auto, nvidia, qwen, deepseek, openrouter o local.",
                reasons=["invalid_model"],
            )
        self.selected_provider = aliases[requested]
        return self._payload(route="model", ok=True, output=f"Proveedor activo: {self.selected_provider}", reasons=["model_selected"])

    def _coding_intent_payload(self, prompt: str, *, gate: str) -> dict[str, Any]:
        return self._payload(
            route="coding_plan",
            ok=True,
            gate=gate,
            output=(
                "Entendido. Trato esto como trabajo de codigo local.\n"
                f"Workspace: {self.workspace}\n"
                "Plan seguro:\n"
                "1. revisar estructura y estado del proyecto;\n"
                "2. localizar errores o tests relevantes;\n"
                "3. preparar diff si hay cambio concreto;\n"
                "4. aplicar solo cuando digas aplica;\n"
                "5. guardar rollback y mini-handoff.\n"
                "No modifique archivos todavia."
            ),
            reasons=["natural_language_coding_intent", "plan_before_diff_apply"],
            prompt=prompt,
        )

    def _live_context_payload(self, prompt: str, *, gate: str) -> dict[str, Any]:
        brain_os = os.environ.get("BRAIN_OS") or "C:\\Users\\L-Tyr\\OneDrive\\Escritorio\\-= BRAIN_OS =-"
        result = load_live_context(brain_os)
        return self._payload(
            route="live_context",
            ok=result.ok,
            gate=gate,
            output=result.output,
            reasons=["live_state_allowlist_context", "no_source_vaults"],
            prompt=prompt,
            artifacts=result.files_used,
            payload={"files_used": result.files_used, "blocked": result.blocked},
        )

    def _model_payload(self, prompt: str, *, gate: str) -> dict[str, Any]:
        if self.options.allow_cloud and _cloud_boundary_blocked(prompt):
            provider = "local"
            reasons = ["protected_prompt_forces_local_only_fallback"]
        else:
            provider = self.selected_provider
            reasons = ["model_conversation"]
        result = self.orchestrator.ask(prompt, provider=provider, timeout=self.options.codex_timeout).to_dict()
        return self._payload(
            route="model_chat",
            ok=bool(result.get("ok")),
            gate=gate,
            output=str(result.get("output") or "No hubo respuesta del proveedor."),
            reasons=reasons,
            prompt=prompt,
            artifacts=[str(item) for item in result.get("artifacts", [])],
            provider_status=result.get("status", {}),
            payload=result,
        )

    def _plan_payload(self, prompt: str, *, gate: str = "APPROVE") -> dict[str, Any]:
        target = self.options.target or _target_from_prompt(prompt)
        if not target:
            return self._payload(
                route="programming_plan",
                ok=False,
                gate="REVIEW",
                output=(
                    "Puedo programarlo, pero necesito una ruta destino para crear el diff. "
                    "Ejemplo: /plan crea una funcion que lea archivos en helpers.py"
                ),
                reasons=["missing_target_for_programming_plan"],
                prompt=prompt,
            )
        try:
            target_path = resolve_workspace_text_target(self.workspace, target, suffix=".py")
            old_text = target_path.read_text(encoding="utf-8") if target_path.exists() else ""
            code, output, inference = code_for_prompt(prompt)
            new_text = build_new_python_text(old_text, code)
            plan = build_file_patch_plan(
                workspace=self.workspace,
                target=target,
                content=new_text,
                summary=prompt,
                suffix=".py",
                test_commands=list(self.options.test_commands),
            )
            plan_path = write_patch_plan(self.runtime_root / "outputs", plan)
            diff_path = write_patch_diff(self.runtime_root / "outputs", plan)
            session_plan = self.session_dir / "plans" / plan_path.name
            session_diff = self.session_dir / "diffs" / diff_path.name
            shutil.copy2(plan_path, session_plan)
            shutil.copy2(diff_path, session_diff)
        except Exception as exc:
            return self._payload(
                route="programming_plan",
                ok=False,
                gate="REVIEW",
                output=f"No pude crear el plan de parche: {exc}",
                reasons=["patch_plan_rejected"],
                prompt=prompt,
            )
        self.pending_plan = plan
        self.pending_plan_path = plan_path
        self.pending_diff_path = diff_path
        return self._payload(
            route="programming_plan",
            ok=True,
            gate=gate,
            output=(
                f"{output}\n\n"
                f"Plan listo para revisar: {plan.plan_id}\n"
                f"Target: {target_path}\n"
                f"Diff: {diff_path}\n\n"
                "No escribi en el codigo fuente. Si quieres aplicarlo, escribe /apply."
            ),
            reasons=["plan_then_apply_policy", *plan.reasons],
            prompt=prompt,
            artifacts=[str(plan_path), str(diff_path)],
            payload={
                "plan_id": plan.plan_id,
                "target": str(target_path),
                "inference": inference,
                "session_plan": str(session_plan),
                "session_diff": str(session_diff),
            },
        )

    def _apply_payload(self) -> dict[str, Any]:
        plan = self.pending_plan
        plan_path = self.pending_plan_path
        if plan is None:
            plan_path = _latest_patch_plan(self.runtime_root)
            if plan_path is not None:
                plan = load_patch_plan(plan_path)
        if plan is None or plan_path is None:
            return self._payload(
                route="apply",
                ok=False,
                gate="REVIEW",
                output="No hay plan pendiente para aplicar. Primero pide /plan ... en un archivo destino.",
                reasons=["missing_pending_plan"],
            )
        try:
            execution = SafeExecutor(workspace=self.workspace, runtime_root=self.runtime_root).execute(plan)
            if execution.ok:
                self.last_applied_plan_id = execution.plan_id
            if execution.rollback_path.exists():
                shutil.copy2(execution.rollback_path, self.session_dir / "rollbacks" / execution.rollback_path.name)
        except Exception as exc:
            return self._payload(
                route="apply",
                ok=False,
                gate="REVIEW",
                output=f"No se aplico el parche: {exc}",
                reasons=["safe_executor_rejected"],
                artifacts=[str(plan_path)],
            )
        return self._payload(
            route="apply",
            ok=execution.ok,
            gate=plan.gate,
            output=(
                f"Aplicacion {'OK' if execution.ok else 'REVIEW'} para {plan.plan_id}.\n"
                f"Archivos escritos: {', '.join(execution.written) or 'ninguno'}\n"
                f"Rollback: {execution.rollback_path}\n"
                f"Verificacion: {execution.verification}"
            ),
            reasons=["operator_apply_confirmed", execution.verification],
            artifacts=[
                str(execution.plan_path),
                str(execution.diff_path),
                str(execution.rollback_path),
                str(execution.execution_path),
            ],
            payload=execution.to_dict(),
        )

    def _diff_payload(self) -> dict[str, Any]:
        diff_path = self.pending_diff_path
        if diff_path is None:
            plan_path = _latest_patch_plan(self.runtime_root)
            if plan_path is not None:
                diff_path = plan_path.parent.parent / f"{plan_path.stem}.diff"
        if diff_path is None or not diff_path.exists():
            return self._payload(route="diff", ok=False, gate="REVIEW", output="No hay diff pendiente.", reasons=["missing_diff"])
        text = diff_path.read_text(encoding="utf-8", errors="replace")
        return self._payload(route="diff", ok=True, output=text[-5000:] or "Diff vacio.", reasons=["operator_diff"], artifacts=[str(diff_path)])

    def _rollback_payload(self, prompt: str) -> dict[str, Any]:
        parts = prompt.split(maxsplit=1)
        if len(parts) < 2:
            ref = self.last_applied_plan_id or _latest_rollback_ref(self.runtime_root)
            if not ref:
                return self._payload(route="rollback", ok=False, gate="REVIEW", output="No hay rollback reciente en esta sesion.", reasons=["missing_rollback_ref"])
        else:
            ref = parts[1].strip()
        try:
            result = RollbackStore(workspace=self.workspace, runtime_root=self.runtime_root).restore(ref)
        except Exception as exc:
            return self._payload(route="rollback", ok=False, gate="REVIEW", output=f"Rollback no ejecutado: {exc}", reasons=["rollback_failed"])
        return self._payload(
            route="rollback",
            ok=True,
            output=f"Rollback aplicado. Restaurados: {', '.join(result.get('restored', [])) or 'ninguno'}.",
            reasons=["operator_rollback"],
            payload=result,
        )

    def _payload(
        self,
        *,
        route: str,
        ok: bool,
        output: str,
        reasons: list[str],
        gate: str = "APPROVE",
        prompt: str = "",
        artifacts: list[str] | None = None,
        provider_status: dict[str, Any] | None = None,
        payload: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        result = {
            "ok": ok,
            "route": route,
            "gate": gate,
            "prompt": redact_text(prompt),
            "reasons": reasons,
            "output": redact_text(output),
            "artifacts": artifacts or [],
            "provider_status": provider_status or {},
            "payload": payload or {},
        }
        self.memory.append_event(
            {
                "channel": "wabi_hablar",
                "route": route,
                "gate": gate,
                "ok": ok,
                "reasons": reasons,
                "artifacts": result["artifacts"],
            }
        )
        if route not in {"empty", "diff"}:
            self.memory.append_memory(
                {
                    "channel": "wabi_hablar",
                    "prompt": redact_text(prompt),
                    "route": route,
                    "gate": gate,
                    "ok": ok,
                    "output": _excerpt(output, 700),
                    "artifacts": result["artifacts"][:3],
                }
            )
        self._append_session_message(result)
        return result

    def _append_session_message(self, result: dict[str, Any]) -> None:
        if result.get("route") == "empty":
            return
        record = {
            "time": time.strftime("%Y-%m-%dT%H:%M:%S"),
            "role": "wabi",
            "route": result.get("route"),
            "gate": result.get("gate"),
            "ok": result.get("ok"),
            "prompt": result.get("prompt", ""),
            "output": _excerpt(str(result.get("output") or ""), 1200),
            "artifacts": result.get("artifacts", [])[:10],
        }
        messages_path = self.session_dir / "messages.jsonl"
        with messages_path.open("a", encoding="utf-8", newline="\n") as handle:
            handle.write(json.dumps(record, ensure_ascii=False) + "\n")
        handoff = [
            "# Wabi-Sabi Session Handoff",
            "",
            f"Updated: {record['time']}",
            f"Workspace: {self.workspace}",
            f"Mode: {self.mode}",
            f"Provider: {self.selected_provider}",
            "",
            "Unknowns First:",
            "- Provider availability can drift; run /providers for current matrix.",
            "",
            "Last Turn:",
            f"- route: {record['route']}",
            f"- gate: {record['gate']}",
            f"- ok: {record['ok']}",
            "",
            "Do Not:",
            "- publicar, push, deploy, ZIP replacement, imprimir secretos, tocar privado o aplicar sin confirmacion.",
            "",
            "Next Contract:",
            "- Continue in the same REPL; ask normally, request /diff before apply, and use /rollback if a confirmed patch must be reverted.",
        ]
        (self.session_dir / "handoff.md").write_text("\n".join(handoff) + "\n", encoding="utf-8")


def format_conversation_payload(payload: dict[str, Any]) -> str:
    if payload.get("route") == "empty":
        return ""
    prefix = "Wabi-Sabi"
    output = str(payload.get("output") or "")
    if payload.get("route") in {"status", "diff"}:
        body = output
    else:
        body = f"{prefix}: {output}"
    if payload.get("gate") != "APPROVE" or payload.get("route") in {"blocked", "apply", "programming_plan"}:
        body += (
            "\n"
            f"[route={payload.get('route')} gate={payload.get('gate')} "
            f"ok={'YES' if payload.get('ok') else 'NO'}]"
        )
    return body


def _looks_like_programming(prompt: str) -> bool:
    normalized = _normalize(prompt)
    return any(hint in normalized for hint in {_normalize(item) for item in PROGRAMMING_HINTS})


def _looks_like_repo_review(prompt: str) -> bool:
    normalized = _normalize(prompt)
    return any(
        hint in normalized
        for hint in {
            "abre este proyecto",
            "revisa este proyecto",
            "revisa el proyecto",
            "revisa este repo",
            "revisa el repo",
            "revisa los errores",
            "corre tests",
            "ejecuta tests",
        }
    )


def _looks_like_casual(prompt: str) -> bool:
    normalized = _normalize(prompt)
    return any(
        hint in normalized
        for hint in {
            "estas ahi",
            "estoy probando",
            "hola",
            "quien eres",
            "que eres",
            "tu nombre",
            "como estas",
            "bajo riesgo",
            "que puedo hacer hoy",
            "no apliques",
        }
    )


def _looks_like_provider_setup(prompt: str) -> bool:
    normalized = _normalize(prompt)
    if any(_normalize(hint) in normalized for hint in PROVIDER_SETUP_HINTS):
        return True
    return ("api" in normalized or "apis" in normalized or "provider" in normalized or "proveedor" in normalized) and any(
        item in normalized for item in {"configura", "activar", "activa", "agrega", "setup", "revisa"}
    )


def _provider_from_setup_prompt(prompt: str) -> str | None:
    normalized = _normalize(prompt)
    if "deepseek" in normalized:
        return "deepseek"
    if "qwen" in normalized or "dashscope" in normalized:
        return "qwen"
    if "openrouter" in normalized:
        return "openrouter"
    if "nvidia" in normalized:
        return "nvidia"
    candidate = prompt.strip().split()[-1] if prompt.strip().startswith("/setup ") else ""
    return normalize_provider(candidate) if candidate else None


def _is_substantive_model_output(output: str) -> bool:
    normalized = _normalize(output)
    if not normalized.strip():
        return False
    menu_markers = ("usa /status", "puedes pedirme /status", "comandos:")
    return not any(marker in normalized for marker in menu_markers)


def _cloud_boundary_blocked(prompt: str) -> bool:
    normalized = _normalize(prompt)
    return any(_normalize(hint) in normalized for hint in PROTECTED_CLOUD_HINTS)


def _looks_like_live_context_request(prompt: str) -> bool:
    normalized = _normalize(prompt)
    return (
        ("live-state" in normalized or "live state" in normalized or "estado actual" in normalized)
        and ("no publiques" in normalized or "sin publicar" in normalized or "bloqueos" in normalized)
    )


def _target_from_prompt(prompt: str) -> str | None:
    matches = re.findall(r"(?:(?:en|a|archivo|target)\s+)([A-Za-z0-9_./\\-]+\.py)\b", prompt)
    return matches[-1] if matches else None


def _latest_patch_plan(runtime_root: Path) -> Path | None:
    directory = runtime_root / "outputs" / "patch_plans"
    if not directory.exists():
        return None
    plans = sorted(directory.glob("patch-*.json"), key=lambda path: path.stat().st_mtime, reverse=True)
    return plans[0] if plans else None


def _latest_rollback_ref(runtime_root: Path) -> str | None:
    directory = runtime_root / "rollback"
    if not directory.exists():
        return None
    rollbacks = sorted(directory.glob("*.json"), key=lambda path: path.stat().st_mtime, reverse=True)
    return rollbacks[0].stem if rollbacks else None


def _excerpt(text: str, limit: int) -> str:
    clean = " ".join(str(text or "").split())
    if len(clean) <= limit:
        return clean
    return clean[: max(0, limit - 3)] + "..."


def _normalize(text: str) -> str:
    return (
        text.lower()
        .replace("á", "a")
        .replace("é", "e")
        .replace("í", "i")
        .replace("ó", "o")
        .replace("ú", "u")
        .replace("ü", "u")
    )
