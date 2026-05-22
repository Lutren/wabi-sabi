from __future__ import annotations

import argparse
import getpass
import json
import sys
from dataclasses import asdict
from pathlib import Path
from typing import Any

from wabi_sabi.agents.base_agent import AgentInput, AgentResult
from wabi_sabi.cli.parser import parse_command
from wabi_sabi.cli.router import AgentRegistry
from wabi_sabi.core.comms_append import build_comms_append_plan, execute_comms_append_plan, write_comms_append_plan
from wabi_sabi.core.config import RuntimeConfig, build_config
from wabi_sabi.core.auto_router import AutoRouteDecision, decide_auto_route
from wabi_sabi.core.bridge import BridgeExecutor
from wabi_sabi.core.claim_contract import evaluate_claim_contract
from wabi_sabi.core.cloud_code_proposal import (
    build_cloud_code_proposal_prompt,
    build_dry_run_cloud_code_proposal,
    cloud_proposal_to_task_spec,
    extract_cloud_code_proposal_payload,
    validate_cloud_code_proposal,
    write_cloud_proposal_artifact,
    write_cloud_task_spec_artifact,
)
from wabi_sabi.core.cloud_debug_loop import run_cloud_debug_loop
from wabi_sabi.core.codex_bridge import WabiCodexBridge
from wabi_sabi.core.cloud_budget import CloudBudgetGate
from wabi_sabi.core.conversational import ConversationOptions, ConversationSession, format_conversation_payload
from wabi_sabi.core.conversation_engine import (
    ConversationEngine,
    ConversationEngineOptions,
    format_turn_response,
    start_interactive_session,
)
from wabi_sabi.core.conversation import blueprint_release_brief, is_followup, local_chat_response
from wabi_sabi.core.cerebro_index import build_cerebro_navigation, write_cerebro_navigation_docs
from wabi_sabi.core.cerebro_line_audit import (
    build_cerebro_line_audit,
    compact_cerebro_audit_payload,
    write_cerebro_audit_outputs,
)
from wabi_sabi.core.cerebro_variant_compare import (
    build_cerebro_variant_comparison,
    compact_cerebro_variant_comparison,
    write_cerebro_variant_comparison,
)
from wabi_sabi.core.cerebro_duplicate_migration_plan import (
    build_cerebro_duplicate_migration_plan,
    compact_cerebro_duplicate_migration_plan,
    write_cerebro_duplicate_migration_plan,
)
from wabi_sabi.core.cerebro_canon_merge_review import (
    build_cerebro_canon_merge_review,
    compact_cerebro_canon_merge_review,
    write_cerebro_canon_merge_review,
)
from wabi_sabi.core.cerebro_archive_intake import compact_archive_intake_payload, run_archive_intake
from wabi_sabi.core.browser_bridge import (
    build_browser_bridge_status,
    convert_browser_response_to_proposal,
    observe_browser_url,
    prepare_browser_ai_consultation,
    prepare_browser_council,
    run_devtools_readonly_snapshot,
    run_kimi_smoke,
)
from wabi_sabi.core.browser_bridge_selector_pack import (
    PUBLIC_PROMPT,
    rank_browser_council_services,
    select_browser_bridge_backend,
)
from wabi_sabi.core.browser_gate import build_browser_gate_policy, evaluate_browser_request
from wabi_sabi.velo.runner import (
    velo_ask,
    velo_login,
    velo_reset_profile,
    velo_serve,
    velo_status,
)
from wabi_sabi.core.build_assist_cloud import (
    build_assist_budget_status,
    build_assist_default_model_alias,
    build_build_assist_cloud_status,
    record_build_assist_usage,
    run_build_assist_nvidia_smoke,
)
from wabi_sabi.core.curator_assistant import run_curator_assistant
from wabi_sabi.core.curator_fichas import run_curator_fichas
from wabi_sabi.core.decision_log import DecisionLogAdapter, write_decision_record
from wabi_sabi.core.eml import jamming_margin_eml, safe_eml, window_load_eml
from wabi_sabi.core.environment import (
    CommsBridge,
    build_environment_snapshot,
    find_portfolio_root,
    write_comms_state,
    write_environment_snapshot,
)
from wabi_sabi.core.functional_status import build_functional_status, write_functional_status
from wabi_sabi.core.gate import ActionGate
from wabi_sabi.core.geodia_synthetic_falsifier import build_geodia_synthetic_falsifier, write_geodia_synthetic_falsifier
from wabi_sabi.core.geodia_synthetic_surface import build_geodia_synthetic_surface
from wabi_sabi.core.job_queue import JobStore, format_job_result, submit_orchestrator_job, summarize_jobs
from wabi_sabi.core.hypothesis_packet import run_conjecture_counterexample
from wabi_sabi.core.local_apply_readiness import apply_local_task_spec, load_latest_taskspec, preview_local_apply
from wabi_sabi.core.llm_work_response import build_safe_llm_work_response
from wabi_sabi.core.memory import LocalMemory
from wabi_sabi.core.multimodal_intake import (
    CaptureOptions,
    build_multimodal_status,
    run_camera_smoke,
    run_mic_smoke,
    run_multimodal_observe,
)
from wabi_sabi.core.observation import ObservationEnvelope
from wabi_sabi.core.observation_claim_adapter import run_claim_fixture_review, run_claim_observation_adapter
from wabi_sabi.core.operator_panel import build_operator_panel
from wabi_sabi.core.patch_planner import build_file_patch_plan, write_patch_diff, write_patch_plan
from wabi_sabi.core.project_scan import scan_project
from wabi_sabi.core.programming import build_new_python_text, code_for_prompt, resolve_python_target
from wabi_sabi.core.programmer_workpack import build_programmer_workpack, write_programmer_workpack
from wabi_sabi.core.provider_orchestrator import ProviderOrchestrator
from wabi_sabi.core.provider_onboarding import SAFE_CONFIG_ENV_KEYS, SECRET_ENV_KEYS, capture_secret_to_user_env
from wabi_sabi.core.provider_status_contract import (
    build_provider_status_contract,
    run_nvidia_live_smoke,
    write_provider_status_artifact,
)
from wabi_sabi.core.nvidia_route_diagnostic import (
    build_nvidia_route_diagnostic,
    write_nvidia_route_diagnostic_artifact,
)
from wabi_sabi.core.redaction import redact_text
from wabi_sabi.core.rollback_store import RollbackStore
from wabi_sabi.core.runtime_diagnostics import (
    build_debug_bundle,
    build_doctor_report,
    build_provider_report,
    build_repair_report,
    format_debug_report,
    format_doctor_report,
    format_provider_report,
    format_repair_report,
)
from wabi_sabi.core.user_config import ensure_user_config
from wabi_sabi.core.safe_executor import SafeExecutor
from wabi_sabi.core.safe_test_runner import run_safe_tests
from wabi_sabi.core.task_spec_planner import build_patch_plan_from_task_spec
from wabi_sabi.core.test_plan import build_test_plan
from wabi_sabi.core.tool_registry import tool_registry_payload
from wabi_sabi.core.tools import write_artifact
from wabi_sabi.core.worktree import git_worktree_summary
from wabi_sabi.engine import (
    build_engine_plan,
    build_observatorio_sandbox_project,
    build_source_card,
    default_engine_manifest,
    engine_plan_to_task_spec,
    load_engine_project_spec,
    load_engine_plan,
    observatorio_click_events,
    simulate_engine_project,
    validate_engine_project_spec,
    write_engine_project_spec,
)


def execute_prompt(
    prompt: str,
    *,
    workspace: str | Path | None = None,
    runtime_root: str | Path | None = None,
    agent_name: str | None = None,
    json_mode: bool = False,
    apply: bool = False,
    target: str | None = None,
) -> dict[str, Any]:
    config = build_config(workspace=workspace, runtime_root=runtime_root)
    registry = AgentRegistry(config.registry_path)
    parsed = parse_command(prompt)
    gate = ActionGate().evaluate_text(prompt)
    selected = registry.select_agent_name(parsed, explicit=agent_name)
    memory = LocalMemory(config.runtime_root)

    if gate.gate == "BLOCK":
        result = AgentResult(
            agent_name=selected,
            ok=False,
            action="blocked_by_action_gate",
            output="La accion fue bloqueada por ActionGate local.",
            evidence=gate.reasons,
            certainty=["El pedido cruza una frontera bloqueada."],
            inference=[],
            unknown=["Se requiere autorizacion/gate especifico para continuar."],
            error=";".join(gate.reasons),
        )
    else:
        agent = registry.build_agent(selected, config)
        result = agent.run(AgentInput(prompt=prompt, parsed=parsed, options={"apply": apply, "target": target}))

    envelope = ObservationEnvelope(
        prompt=prompt,
        intent=parsed.intent,
        agent=result.agent_name,
        action_gate=gate.gate,
        certainty=result.certainty,
        inference=result.inference,
        unknown=result.unknown,
        artifacts=result.artifacts,
        evidence=result.evidence,
    ).finalize()

    event = {
        "prompt": redact_text(prompt),
        "parsed": asdict(parsed),
        "agent": result.agent_name,
        "gate": gate.gate,
        "gate_reasons": gate.reasons,
        "ok": result.ok,
        "action": result.action,
        "artifacts": result.artifacts,
        "fingerprint": envelope.fingerprint,
    }
    log_path = memory.append_event(event)
    memory.append_memory({"prompt": redact_text(prompt), "intent": parsed.intent, "agent": result.agent_name})

    payload = {
        "ok": result.ok,
        "prompt": prompt,
        "intent": parsed.intent,
        "confidence": parsed.confidence,
        "agent": result.agent_name,
        "gate": gate.gate,
        "gate_reasons": gate.reasons,
        "action": result.action,
        "output": result.output,
        "artifacts": result.artifacts,
        "evidence": result.evidence,
        "certainty": result.certainty,
        "inference": result.inference,
        "unknown": result.unknown,
        "error": result.error,
        "log": str(log_path),
        "fingerprint": envelope.fingerprint,
        "observation": envelope.to_dict(),
    }
    if not json_mode:
        print(_format_payload(payload))
    return payload


def _format_payload(payload: dict[str, Any]) -> str:
    lines = [
        "WABI SABI LOCAL",
        f"Intento: {payload['intent']}  Agente: {payload['agent']}  Gate: {payload['gate']}",
        f"Resultado: {'OK' if payload['ok'] else 'BLOCK'}",
        "",
        "CERTEZA:",
    ]
    lines.extend(f"- {item}" for item in payload["certainty"])
    lines.append("")
    lines.append("INFERENCIA:")
    lines.extend(f"- {item}" for item in payload["inference"])
    lines.append("")
    lines.append("INCOGNITA:")
    lines.extend(f"- {item}" for item in payload["unknown"])
    lines.append("")
    lines.append("ACCION:")
    lines.append(f"- {payload['action']}: {payload['output']}")
    lines.append("")
    lines.append("ARTEFACTOS:")
    if payload["artifacts"]:
        lines.extend(f"- {artifact}" for artifact in payload["artifacts"])
    else:
        lines.append("- Sin artefactos nuevos.")
    lines.append(f"- Log: {payload['log']}")
    lines.append(f"- Fingerprint: {payload['fingerprint']}")
    return "\n".join(lines)


def execute_auto_prompt(
    prompt: str,
    *,
    workspace: str | Path | None = None,
    runtime_root: str | Path | None = None,
    agent_name: str | None = None,
    apply: bool = False,
    target: str | None = None,
    codex_provider: str = "auto",
    codex_timeout: int = 35,
    dry_run: bool = False,
    background_codex: bool = False,
) -> dict[str, Any]:
    config = build_config(workspace=workspace, runtime_root=runtime_root)
    parsed = parse_command(prompt)
    orchestrator = ProviderOrchestrator(workspace=config.workspace, runtime_root=config.runtime_root)
    status = orchestrator.status()
    decision = decide_auto_route(prompt, parsed, status, dry_run=dry_run)
    if decision.route == "status":
        status = {**status, "worktree": git_worktree_summary(config.workspace, max_files=20)}
    memory = LocalMemory(config.runtime_root)
    recent_memory = memory.tail_memory(limit=10)
    if decision.route in {"codex", "codex_dry_run"} and is_followup(decision.prompt) and recent_memory:
        decision = AutoRouteDecision(
            "local_chat",
            decision.prompt,
            decision.gate,
            ["local_memory_followup"],
            decision.forced,
        )

    if decision.route == "status":
        result: dict[str, Any] = {
            "ok": True,
            "route": decision.route,
            "gate": decision.gate,
            "prompt": redact_text(decision.prompt),
            "reasons": decision.reasons,
            "output": _format_codex_status(status),
            "artifacts": [],
            "provider_status": status,
            "payload": status,
        }
    elif decision.route == "blocked":
        result = {
            "ok": False,
            "route": decision.route,
            "gate": decision.gate,
            "prompt": redact_text(decision.prompt),
            "reasons": decision.reasons,
            "output": "ActionGate bloqueo el pedido antes de elegir proveedor.",
            "artifacts": [],
            "provider_status": status,
            "payload": {"error": ";".join(decision.reasons)},
        }
    elif decision.route == "local_chat":
        result = {
            "ok": True,
            "route": decision.route,
            "gate": decision.gate,
            "prompt": redact_text(decision.prompt),
            "reasons": decision.reasons,
            "output": local_chat_response(decision.prompt, status, recent_memory),
            "artifacts": [],
            "provider_status": status,
            "payload": {"mode": "local_chat"},
        }
    elif decision.route == "local_agent":
        local_payload = execute_prompt(
            decision.prompt,
            workspace=config.workspace,
            runtime_root=config.runtime_root,
            agent_name=agent_name,
            json_mode=True,
            apply=apply,
            target=target,
        )
        result = {
            "ok": local_payload["ok"],
            "route": decision.route,
            "gate": decision.gate,
            "prompt": redact_text(decision.prompt),
            "reasons": decision.reasons,
            "output": local_payload["output"],
            "artifacts": local_payload["artifacts"],
            "provider_status": status,
            "payload": local_payload,
        }
    elif decision.route == "hybrid_codex":
        output = blueprint_release_brief(decision.prompt, status)
        artifacts: list[str] = []
        payload: dict[str, Any] = {"mode": "local_blueprint_brief"}
        route = decision.route
        reasons = list(decision.reasons)
        if background_codex:
            job = submit_orchestrator_job(
                prompt=decision.prompt,
                workspace=config.workspace,
                runtime_root=config.runtime_root,
                provider=codex_provider,
                timeout=codex_timeout,
            )
            route = "hybrid_codex_background"
            reasons.append("background_codex")
            artifacts = [job["job_file"]]
            payload = job
            output = (
                f"{output}\n\n"
                f"Codex profundo quedo trabajando en background.\n"
                f"Job: {job['job_id']}\n"
                "Usa /jobs o /result para ampliar y contrastar la propuesta."
            )
        result = {
            "ok": True,
            "route": route,
            "gate": decision.gate,
            "prompt": redact_text(decision.prompt),
            "reasons": reasons,
            "output": output,
            "artifacts": artifacts,
            "provider_status": status,
            "payload": payload,
        }
    elif background_codex and decision.route == "codex":
        job = submit_orchestrator_job(
            prompt=decision.prompt,
            workspace=config.workspace,
            runtime_root=config.runtime_root,
            provider=codex_provider,
            timeout=codex_timeout,
        )
        result = {
            "ok": True,
            "route": "codex_background",
            "gate": decision.gate,
            "prompt": redact_text(decision.prompt),
            "reasons": decision.reasons + ["background_codex"],
            "output": (
                f"Recibi el pedido y lo mande a Codex en segundo plano.\n"
                f"Job: {job['job_id']}\n"
                "Puedes seguir escribiendo. Usa /jobs o /result para ver el avance."
            ),
            "artifacts": [job["job_file"]],
            "provider_status": status,
            "payload": job,
        }
    else:
        deep_provider = "dry-run" if decision.route == "codex_dry_run" else codex_provider
        codex_result = orchestrator.ask(
            decision.prompt,
            provider=deep_provider,
            timeout=codex_timeout,
        ).to_dict()
        result = {
            "ok": codex_result["ok"],
            "route": decision.route,
            "gate": decision.gate,
            "prompt": redact_text(decision.prompt),
            "reasons": decision.reasons,
            "output": codex_result["output"],
            "artifacts": codex_result["artifacts"],
            "provider_status": status,
            "payload": codex_result,
        }

    memory.append_event(
        {
            "channel": "wabi_auto_router",
            "prompt": redact_text(prompt),
            "route": result["route"],
            "gate": result["gate"],
            "ok": result["ok"],
            "reasons": result["reasons"],
            "artifacts": result["artifacts"],
        }
    )
    memory.append_memory(
        {
            "channel": "wabi_auto_conversation",
            "prompt": redact_text(prompt),
            "route": result["route"],
            "gate": result["gate"],
            "ok": result["ok"],
            "reasons": result["reasons"],
            "output": _memory_excerpt(result["output"]),
            "artifacts": result["artifacts"][:3],
        }
    )
    return result


def execute_chat_prompt(
    prompt: str,
    *,
    workspace: str | Path | None = None,
    runtime_root: str | Path | None = None,
) -> dict[str, Any]:
    config = build_config(workspace=workspace, runtime_root=runtime_root)
    clean_prompt = prompt.strip()
    redacted_prompt = redact_text(clean_prompt)
    if clean_prompt.lower() in {"/status", "status", "estado"}:
        return execute_auto_prompt(
            clean_prompt,
            workspace=config.workspace,
            runtime_root=config.runtime_root,
        )
    gate = ActionGate().evaluate_text(clean_prompt)
    orchestrator = ProviderOrchestrator(workspace=config.workspace, runtime_root=config.runtime_root)
    status = orchestrator.status()
    memory = LocalMemory(config.runtime_root)
    recent_memory = memory.tail_memory(limit=10)
    if gate.gate == "BLOCK":
        payload = {
            "ok": False,
            "route": "local_chat",
            "gate": gate.gate,
            "prompt": redacted_prompt,
            "reasons": gate.reasons,
            "output": "ActionGate bloqueo la conversacion porque cruza una frontera de secretos, publicacion o accion destructiva.",
            "artifacts": [],
            "provider_status": status,
            "payload": {"mode": "local_chat_blocked"},
        }
    else:
        payload = {
            "ok": True,
            "route": "local_chat",
            "gate": gate.gate,
            "prompt": redacted_prompt,
            "reasons": ["explicit_chat_command", "local_conversation"],
            "output": local_chat_response(clean_prompt, status, recent_memory),
            "artifacts": [],
            "provider_status": status,
            "payload": {"mode": "local_chat"},
        }
    memory.append_event(
        {
            "channel": "wabi_chat",
            "route": payload["route"],
            "gate": payload["gate"],
            "ok": payload["ok"],
            "reasons": payload["reasons"],
            "artifacts": payload["artifacts"],
        }
    )
    memory.append_memory(
        {
            "channel": "wabi_chat",
            "prompt": redacted_prompt,
            "route": payload["route"],
            "gate": payload["gate"],
            "ok": payload["ok"],
            "output": _memory_excerpt(payload["output"]),
        }
    )
    return payload


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="wabi", description="Wabi Sabi local agent CLI")
    parser.add_argument("items", nargs="*", help="Prompt or subcommand")
    parser.add_argument("--workspace", default=None, help="Workspace to inspect")
    parser.add_argument("--runtime", default=None, help="Runtime/log directory")
    parser.add_argument("--agent", default=None, help="Force a specific agent")
    parser.add_argument("--json", action="store_true", help="Emit JSON")
    parser.add_argument("--apply", action="store_true", help="Apply a scoped local code patch")
    parser.add_argument("--target", default=None, help="Target file for --apply, relative to --workspace")
    parser.add_argument("--task", default=None, help="Task spec path for cloud-debug-loop")
    parser.add_argument("--latest", action="store_true", help="Use the latest redacted TaskSpec from the local Wabi runtime")
    parser.add_argument("--provider", default=None, help="Provider name for provider subcommands")
    parser.add_argument("--model", default=None, help="Model alias for build-assist-smoke")
    parser.add_argument("--live", action="store_true", help="Allow a live build-assist smoke when gates are enabled")
    parser.add_argument(
        "--browser-backend",
        "--backend",
        default="dry-run",
        choices=["dry-run", "chrome-devtools-mcp", "kimi-webbridge", "hermes"],
        help="BrowserBridge backend; real backends stay disabled unless locally configured and gated",
    )
    parser.add_argument("--service", default=None, help="BrowserBridge service id for selector/smoke")
    parser.add_argument("--payload-class", default=PUBLIC_PROMPT, help="BrowserBridge selector payload class")
    parser.add_argument("--input", default=None, help="Input file for BrowserBridge response conversion")
    parser.add_argument("--snapshot-url", default="http://127.0.0.1:8787/", help="Local URL for BrowserBridge read-only snapshot")
    parser.add_argument("--velo-host", default="127.0.0.1", help="Loopback host for the Velo browser bridge server")
    parser.add_argument("--velo-port", type=int, default=8777, help="Local port for the Velo browser bridge server")
    parser.add_argument("--headless", action="store_true", help="Run the Velo browser with no visible window")
    parser.add_argument(
        "--send",
        action="store_true",
        help="Request BrowserBridge AI send; still requires WABI_ALLOW_BROWSER_SEND=1 and an available proven adapter",
    )
    parser.add_argument(
        "--allow-model-list",
        action="store_true",
        help="Request provider model-list diagnostic review without making a cloud call by default",
    )
    parser.add_argument("--dry-run", action="store_true", help="Build a workpack without model/subprocess calls")
    parser.add_argument("--write-docs", action="store_true", help="Write generated documentation for supported commands")
    parser.add_argument(
        "--test-command",
        action="append",
        default=[],
        help="Allowlisted verification command for patch-apply, for example: python -m pytest -q",
    )
    parser.add_argument(
        "--codex-provider",
        default="auto",
        choices=[
            "auto",
            "codex-cli",
            "openai-responses",
            "ollama",
            "nvidia",
            "nvidia-nim",
            "nano-9b",
            "nano-30b",
            "super",
            "ultra",
            "llama-70b",
            "kimi",
            "deepseek",
            "mistral",
            "minimax",
            "glm",
            "qwen",
            "qwen-cloud",
            "openrouter",
            "local",
            "dry-run",
        ],
        help="Provider for the deep Wabi-Sabi route",
    )
    parser.add_argument("--codex-timeout", type=int, default=35, help="Codex bridge timeout in seconds")
    parser.add_argument(
        "--background-codex",
        action="store_true",
        help="Return immediately and run Codex jobs in the background",
    )
    parser.add_argument("--cloud", action="store_true", help="Allow cloud provider fallback for hablar mode")
    parser.add_argument("--no-cloud", action="store_true", help="Keep hablar mode local/Codex/Ollama only")
    parser.add_argument("--local-only", action="store_true", help="Force supported commands to stay local-only")
    parser.add_argument("--seconds", type=int, default=5, help="Capture duration for multimodal microphone/observe commands")
    parser.add_argument("--device-index", type=int, default=0, help="Camera device index for multimodal commands")
    parser.add_argument("--sample-rate", type=int, default=16000, help="Microphone sample rate for multimodal commands")
    parser.add_argument("--width", type=int, default=320, help="Camera capture width for multimodal commands")
    parser.add_argument("--height", type=int, default=180, help="Camera capture height for multimodal commands")
    parser.add_argument(
        "--transcribe",
        action="store_true",
        help="Request local transcription when WABI_ENABLE_LOCAL_TRANSCRIPTION=1",
    )
    parser.add_argument("--once", default=None, help="Run one conversational prompt and exit")
    return parser


def _load_local_apply_task_spec(config: RuntimeConfig, refs: list[str], *, latest: bool = False) -> dict[str, Any]:
    if latest:
        return load_latest_taskspec(runtime_root=config.runtime_root)
    ref = refs[0] if refs else ""
    if not ref:
        raise FileNotFoundError("missing_taskspec_ref_or_latest")
    path = Path(ref)
    if not path.is_absolute():
        path = (config.workspace / path).resolve()
    payload = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(payload.get("taskspec_review"), dict):
        return dict(payload["taskspec_review"])
    if isinstance(payload.get("task_spec"), dict):
        return dict(payload["task_spec"])
    return dict(payload)


def _format_local_apply_payload(payload: dict[str, Any]) -> str:
    candidate = payload.get("patch_candidate", {})
    result = payload.get("result", {})
    if not isinstance(candidate, dict):
        candidate = {}
    if isinstance(result, dict) and not candidate and isinstance(result.get("patch_candidate"), dict):
        candidate = result["patch_candidate"]
    paths = candidate.get("affected_paths") or []
    tests = candidate.get("tests_to_run") or []
    lines = [
        f"status: {payload.get('status', result.get('status', 'REVIEW'))}",
        f"ok: {bool(payload.get('ok', False))}",
        f"applied_to_sources: {bool(payload.get('applied_to_sources', result.get('applied_to_sources', False)))}",
        "cloud_provider_called: false",
        f"paths: {', '.join(str(item) for item in paths) or 'none'}",
        f"tests: {', '.join(str(item) for item in tests) or 'none'}",
    ]
    rollback = result.get("rollback_snapshot") if isinstance(result, dict) else None
    if rollback:
        lines.append(f"rollback: {rollback}")
    reason = payload.get("reason") or result.get("reason") if isinstance(result, dict) else ""
    if reason:
        lines.append(f"reason: {reason}")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    args = build_arg_parser().parse_args(argv)
    items = args.items
    ensure_user_config()
    config = build_config(workspace=args.workspace, runtime_root=args.runtime)
    registry = AgentRegistry(config.registry_path)
    if args.once:
        options = ConversationEngineOptions(
            codex_provider=args.codex_provider,
            codex_timeout=args.codex_timeout,
            allow_cloud=_conversation_cloud_allowed(args),
            target=args.target,
            test_commands=tuple(args.test_command),
        )
        engine = ConversationEngine(workspace=config.workspace, runtime_root=config.runtime_root, options=options)
        payload = engine.handle_turn(args.once)
        original_schema = payload.get("schema")
        payload.update(build_safe_llm_work_response(payload, runtime_root=config.runtime_root, source="cli_once"))
        if original_schema:
            payload["schema"] = original_schema
        print(json.dumps(payload, indent=2, ensure_ascii=False) if args.json else format_turn_response(payload))
        return 0 if payload["ok"] else 2
    if not items:
        options = ConversationEngineOptions(
            codex_provider=args.codex_provider,
            codex_timeout=args.codex_timeout,
            allow_cloud=_conversation_cloud_allowed(args),
            target=args.target,
            test_commands=tuple(args.test_command),
        )
        return start_interactive_session(ConversationEngine(workspace=config.workspace, runtime_root=config.runtime_root, options=options))
    command = items[0].lower()
    if command in {"doctor", "diagnostico", "diagnóstico"}:
        payload = build_doctor_report(config)
        print(json.dumps(payload, indent=2, ensure_ascii=False) if args.json else format_doctor_report(payload))
        return 0 if payload["result"] in {"PASS", "REVIEW"} else 2
    if command in {"providers", "proveedores"}:
        payload = build_provider_report(runtime_root=config.runtime_root, smoke=not args.dry_run)
        print(json.dumps(payload, indent=2, ensure_ascii=False) if args.json else format_provider_report(payload))
        return 0
    if command == "provider":
        subcommand = items[1].lower() if len(items) > 1 else "status"
        if subcommand in {"status", "estado", "model-status"}:
            payload = build_provider_status_contract(runtime_root=config.runtime_root)
            artifact = write_provider_status_artifact(config.runtime_root, payload)
            payload["provider_status_artifact"] = str(artifact)
            print(json.dumps(payload, indent=2, ensure_ascii=False) if args.json else _format_provider_contract_payload(payload))
            return 0
        if subcommand in {"live-smoke", "smoke"}:
            provider = (args.provider or "nvidia").lower()
            if provider != "nvidia":
                payload = {
                    "ok": False,
                    "action": "provider_live_smoke",
                    "provider": provider,
                    "live_smoke_status": "SMOKE_FAIL_REDACTED",
                    "error": "unsupported_provider_for_live_smoke",
                    "cloud_provider_called": False,
                    "secret_values_printed": False,
                    "publication_gate": "BLOCK",
                }
            else:
                payload = run_nvidia_live_smoke(runtime_root=config.runtime_root, timeout=args.codex_timeout)
            print(json.dumps(payload, indent=2, ensure_ascii=False) if args.json else _format_provider_contract_payload(payload))
            return 0 if payload.get("live_smoke_status") in {"SMOKE_PASS", "CLOUD_DISABLED_BY_FLAG", "NOT_CONFIGURED"} else 2
        if subcommand in {"diagnose", "diagnostic", "diagnostico", "diagnóstico"}:
            provider = (args.provider or "nvidia").lower()
            if provider != "nvidia":
                payload = {
                    "ok": False,
                    "action": "provider_diagnose",
                    "provider": provider,
                    "error": "unsupported_provider_for_route_diagnostic",
                    "cloud_provider_called": False,
                    "secret_values_printed": False,
                    "publication_gate": "BLOCK",
                }
                print(json.dumps(payload, indent=2, ensure_ascii=False) if args.json else payload["error"])
                return 2
            diagnostic = build_nvidia_route_diagnostic(
                runtime_root=config.runtime_root,
                allow_model_list=args.allow_model_list,
            )
            artifact = write_nvidia_route_diagnostic_artifact(config.runtime_root, diagnostic)
            payload = {
                "ok": diagnostic.get("route_diagnostic_status") in {"PASS", "REVIEW"},
                "action": "provider_diagnose",
                "provider": "nvidia",
                "provider_status": build_provider_status_contract(runtime_root=config.runtime_root),
                "last_smoke_status": diagnostic.get("last_smoke_status"),
                "route_diagnostic": diagnostic,
                "alias_candidates": diagnostic.get("alias_candidates", []),
                "recommended_next_action": diagnostic.get("recommended_next_action"),
                "credential_present_redacted": diagnostic.get("credential_present_redacted", False),
                "cloud_provider_called": False,
                "secret_values_printed": diagnostic.get("secret_values_printed", False),
                "publication_gate": diagnostic.get("publication_gate", "BLOCK"),
                "diagnostic_artifact": str(artifact),
            }
            print(json.dumps(payload, indent=2, ensure_ascii=False) if args.json else _format_nvidia_route_diagnostic_payload(payload))
            return 0 if payload["ok"] else 2
        payload = {"ok": False, "action": "provider", "error": f"unsupported_provider_subcommand:{subcommand}"}
        print(json.dumps(payload, indent=2, ensure_ascii=False) if args.json else payload["error"])
        return 2
    if command in {"repair", "reparar"}:
        payload = build_repair_report(config, dry_run=args.dry_run)
        print(json.dumps(payload, indent=2, ensure_ascii=False) if args.json else format_repair_report(payload))
        return 0
    if command in {"debug", "debug-bundle", "diagnostic-bundle"}:
        payload = build_debug_bundle(config, dry_run=args.dry_run)
        print(json.dumps(payload, indent=2, ensure_ascii=False) if args.json else format_debug_report(payload))
        return 0
    if command in {"auto", "operador", "operator"}:
        if len(items) == 1:
            return _auto_interactive(
                config,
                codex_provider=args.codex_provider,
                codex_timeout=args.codex_timeout,
            )
        prompt = " ".join(items[1:])
        payload = execute_auto_prompt(
            prompt,
            workspace=args.workspace,
            runtime_root=args.runtime,
            agent_name=args.agent,
            apply=args.apply,
            target=args.target,
            codex_provider=args.codex_provider,
            codex_timeout=args.codex_timeout,
            dry_run=args.dry_run,
            background_codex=args.background_codex,
        )
        print(json.dumps(payload, indent=2, ensure_ascii=False) if args.json else _format_auto_payload(payload))
        return 0 if payload["ok"] else 2
    if command in {"hablar"}:
        options = ConversationOptions(
            codex_provider=args.codex_provider,
            codex_timeout=args.codex_timeout,
            allow_cloud=_conversation_cloud_allowed(args),
            target=args.target,
            test_commands=tuple(args.test_command),
        )
        session = ConversationSession(workspace=config.workspace, runtime_root=config.runtime_root, options=options)
        if len(items) == 1:
            return _conversational_interactive(session)
        prompt = " ".join(items[1:])
        payload = session.handle(prompt)
        print(json.dumps(payload, indent=2, ensure_ascii=False) if args.json else format_conversation_payload(payload))
        return 0 if payload["ok"] else 2
    if command in {"chat", "talk"}:
        if len(items) == 1:
            return _interactive(config)
        prompt = " ".join(items[1:])
        payload = execute_chat_prompt(
            prompt,
            workspace=args.workspace,
            runtime_root=args.runtime,
        )
        print(json.dumps(payload, indent=2, ensure_ascii=False) if args.json else _format_auto_payload(payload))
        return 0 if payload["ok"] else 2
    if command in {"provider-status", "status-providers", "model-status"}:
        orchestrator = ProviderOrchestrator(workspace=config.workspace, runtime_root=config.runtime_root)
        payload = orchestrator.status()
        payload["build_assist"] = build_build_assist_cloud_status(
            workspace=config.workspace,
            runtime_root=config.runtime_root,
            provider_status=payload,
        )
        payload["provider_contract"] = build_provider_status_contract(runtime_root=config.runtime_root)
        payload["worktree"] = git_worktree_summary(config.workspace, max_files=20)
        print(json.dumps(payload, indent=2, ensure_ascii=False) if args.json else _format_codex_status(payload))
        return 0
    if command in {"build-assist-status", "survival-status", "cloud-build-status"}:
        orchestrator = ProviderOrchestrator(workspace=config.workspace, runtime_root=config.runtime_root)
        provider_status = orchestrator.status()
        payload = build_build_assist_cloud_status(
            workspace=config.workspace,
            runtime_root=config.runtime_root,
            provider_status=provider_status,
        )
        LocalMemory(config.runtime_root).append_event(
            {
                "channel": "wabi_build_assist_status",
                "ok": payload["ok"],
                "cloud_live_ready": payload.get("cloud_live_ready", False),
                "action_gate": payload.get("action_gate", ""),
            }
        )
        print(json.dumps(payload, indent=2, ensure_ascii=False) if args.json else _format_build_assist_payload(payload))
        return 0
    if command in {"build-assist-plan", "survival-plan", "cloud-build-plan"}:
        payload = _execute_build_assist_plan_command(
            config,
            items[1:],
            provider=args.codex_provider,
            timeout=args.codex_timeout,
            dry_run=args.dry_run,
        )
        LocalMemory(config.runtime_root).append_event(
            {
                "channel": "wabi_build_assist_plan",
                "ok": payload.get("ok", False),
                "provider": payload.get("provider", ""),
                "cloud_provider_called": payload.get("cloud_provider_called", False),
                "proposal": payload.get("proposal_artifact", ""),
            }
        )
        print(json.dumps(payload, indent=2, ensure_ascii=False) if args.json else _format_build_assist_payload(payload))
        return 0 if payload.get("ok") else 2
    if command in {"build-assist-smoke", "survival-smoke", "cloud-build-smoke"}:
        payload = run_build_assist_nvidia_smoke(
            workspace=config.workspace,
            runtime_root=config.runtime_root,
            provider=args.provider or "nvidia",
            model_alias=args.model or None,
            live=args.live,
            timeout=args.codex_timeout,
        )
        LocalMemory(config.runtime_root).append_event(
            {
                "channel": "wabi_build_assist_smoke",
                "status": payload.get("status"),
                "provider": payload.get("provider"),
                "model": payload.get("model"),
                "cloud_provider_called": payload.get("cloud_provider_called", False),
                "artifact": payload.get("artifact_path", ""),
            }
        )
        print(json.dumps(payload, indent=2, ensure_ascii=False) if args.json else _format_build_assist_payload(payload))
        return 0 if payload.get("status") == "LIVE_SMOKE_PASS" else 2
    if command in {"multimodal", "multimodal-status", "camera-smoke", "mic-smoke"}:
        subcommand = items[1].lower() if command == "multimodal" and len(items) > 1 else ""
        if command == "multimodal-status":
            subcommand = "status"
        elif command == "camera-smoke":
            subcommand = "smoke-camera"
        elif command == "mic-smoke":
            subcommand = "smoke-mic"
        if args.cloud and not args.local_only:
            payload = {
                "schema": "wabi.multimodal_intake.v1",
                "ok": False,
                "action": "multimodal_cloud_request",
                "gate": "REVIEW",
                "reason": "cloud_multimodal_requires_explicit_review_path",
                "cloud_provider_called": False,
                "secret_values_printed": False,
            }
        else:
            options = CaptureOptions(
                seconds=args.seconds,
                device_index=args.device_index,
                sample_rate=args.sample_rate,
                width=args.width,
                height=args.height,
                transcribe=args.transcribe,
            )
            if subcommand in {"", "status", "estado"}:
                payload = build_multimodal_status(workspace=config.workspace, runtime_root=config.runtime_root)
            elif subcommand in {"smoke-camera", "camera", "camara", "cámara"}:
                payload = run_camera_smoke(workspace=config.workspace, runtime_root=config.runtime_root, options=options)
            elif subcommand in {"smoke-mic", "microphone", "mic", "microfono", "micrófono"}:
                payload = run_mic_smoke(workspace=config.workspace, runtime_root=config.runtime_root, options=options)
            elif subcommand in {"observe", "observar", "stream", "loop"}:
                payload = run_multimodal_observe(workspace=config.workspace, runtime_root=config.runtime_root, options=options)
            else:
                payload = {
                    "schema": "wabi.multimodal_intake.v1",
                    "ok": False,
                    "action": "multimodal_unknown_subcommand",
                    "gate": "REVIEW",
                    "subcommand": subcommand,
                    "valid_subcommands": ["status", "smoke-camera", "smoke-mic", "observe"],
                    "cloud_provider_called": False,
                    "secret_values_printed": False,
                }
        LocalMemory(config.runtime_root).append_event(
            {
                "channel": "wabi_multimodal_cli",
                "action": payload.get("action"),
                "ok": payload.get("ok"),
                "gate": payload.get("gate"),
                "artifact": payload.get("artifact", ""),
                "cloud_provider_called": payload.get("cloud_provider_called", False),
            }
        )
        print(json.dumps(payload, indent=2, ensure_ascii=False) if args.json else _format_multimodal_payload(payload))
        return 0 if payload.get("gate") != "BLOCK" else 2
    if command in {"env-status", "environment", "entorno"}:
        orchestrator = ProviderOrchestrator(workspace=config.workspace, runtime_root=config.runtime_root)
        snapshot = build_environment_snapshot(
            workspace=config.workspace,
            runtime_root=config.runtime_root,
            provider_status=orchestrator.status(),
            run_comms_validator=True,
        )
        artifact = write_environment_snapshot(config.output_dir, snapshot)
        LocalMemory(config.runtime_root).append_event(
            {
                "channel": "wabi_environment_snapshot",
                "artifact": str(artifact),
                "recommended_mode": snapshot["decision"]["recommended_mode"],
                "host_gate": snapshot["host"].get("gate"),
                "comms_agents": snapshot["comms"].get("agent_count"),
            }
        )
        payload = {
            "ok": True,
            "action": "environment_snapshot",
            "artifact": str(artifact),
            "snapshot": snapshot,
        }
        print(json.dumps(payload, indent=2, ensure_ascii=False) if args.json else _format_environment_payload(payload))
        return 0
    if command in {"comms-state", "comms", "comunicacion"}:
        portfolio_root = find_portfolio_root(config.workspace, config.runtime_root)
        bridge = CommsBridge(portfolio_root)
        summary = bridge.summary()
        summary["validator"] = bridge.validate()
        payload = {
            "ok": bool(portfolio_root),
            "action": "comms_state",
            "portfolio_root": str(portfolio_root) if portfolio_root else "",
            "comms": summary,
        }
        artifact = write_comms_state(config.output_dir, payload)
        payload["artifact"] = str(artifact)
        LocalMemory(config.runtime_root).append_event(
            {
                "channel": "wabi_comms_state",
                "artifact": str(artifact),
                "ok": payload["ok"],
                "agent_count": summary.get("agent_count"),
                "validator_ok": summary.get("validator", {}).get("ok"),
            }
        )
        print(json.dumps(payload, indent=2, ensure_ascii=False) if args.json else _format_comms_payload(payload))
        return 0 if payload["ok"] else 2
    if command in {"decide", "decision", "decidir"}:
        decision_prompt = " ".join(items[1:]).strip() or "estado local"
        orchestrator = ProviderOrchestrator(workspace=config.workspace, runtime_root=config.runtime_root)
        snapshot = build_environment_snapshot(
            workspace=config.workspace,
            runtime_root=config.runtime_root,
            provider_status=orchestrator.status(),
            run_comms_validator=True,
        )
        snapshot_artifact = write_environment_snapshot(config.output_dir, snapshot)
        adapter = DecisionLogAdapter(runtime_root=config.runtime_root)
        record = adapter.record(
            prompt=decision_prompt,
            snapshot=snapshot,
            evidence_refs=[str(snapshot_artifact), "wabi_cli_decide"],
        )
        artifact = write_decision_record(config.output_dir, record)
        payload = {
            "ok": True,
            "action": "wabi_decision_recorded",
            "artifact": str(artifact),
            "snapshot_artifact": str(snapshot_artifact),
            "record": record,
            "task_manager": str(adapter.task_manager_path),
            "ledger": str(adapter.ledger_path),
            "witness_db": str(adapter.witness.db_path),
        }
        LocalMemory(config.runtime_root).append_event(
            {
                "channel": "wabi_decision_log",
                "artifact": str(artifact),
                "record_hash": record["record_hash"],
                "recommended_mode": record["recommended_mode"],
                "status": record["status"],
                "witness_verified": record["witness_verified"],
            }
        )
        print(json.dumps(payload, indent=2, ensure_ascii=False) if args.json else _format_decision_payload(payload))
        return 0
    if command in {"decision-log", "decisions", "decisiones"}:
        adapter = DecisionLogAdapter(runtime_root=config.runtime_root)
        payload = {
            "ok": True,
            "action": "wabi_decision_log",
            "ledger": str(adapter.ledger_path),
            "task_manager": str(adapter.task_manager_path),
            "witness_db": str(adapter.witness.db_path),
            "records": adapter.tail(),
            "tasks": adapter.task_manager(),
        }
        print(json.dumps(payload, indent=2, ensure_ascii=False) if args.json else _format_decision_log_payload(payload))
        return 0
    if command in {"comms-append-plan", "comms-plan", "plan-comms"}:
        portfolio_root = find_portfolio_root(config.workspace, config.runtime_root)
        adapter = DecisionLogAdapter(runtime_root=config.runtime_root)
        records = adapter.tail(limit=1)
        if portfolio_root is None or not records:
            payload = {
                "ok": False,
                "action": "comms_append_plan",
                "error": "portfolio_root_or_decision_record_not_found",
                "portfolio_root": str(portfolio_root) if portfolio_root else "",
                "ledger": str(adapter.ledger_path),
            }
            print(json.dumps(payload, indent=2, ensure_ascii=False) if args.json else payload["error"])
            return 2
        plan = build_comms_append_plan(portfolio_root=portfolio_root, decision_record=records[-1])
        plan = execute_comms_append_plan(plan, apply=args.apply)
        artifact = write_comms_append_plan(config.output_dir, plan)
        payload = {
            "ok": True,
            "action": "comms_append_plan",
            "artifact": str(artifact),
            "plan": plan,
        }
        LocalMemory(config.runtime_root).append_event(
            {
                "channel": "wabi_comms_append_plan",
                "artifact": str(artifact),
                "append_allowed": plan["append_allowed"],
                "append_performed": plan["append_performed"],
                "action_gate": plan["message"]["action_gate"],
            }
        )
        print(json.dumps(payload, indent=2, ensure_ascii=False) if args.json else _format_comms_append_plan_payload(payload))
        return 0 if not args.apply or plan["append_performed"] else 2
    if command in {"operator-status", "operator-panel", "ops-status", "panel"}:
        task_spec_ref = " ".join(items[1:]).strip() or None
        payload = build_operator_panel(
            workspace=config.workspace,
            runtime_root=config.runtime_root,
            task_spec=task_spec_ref,
        )
        LocalMemory(config.runtime_root).append_event(
            {
                "channel": "wabi_operator_panel",
                "ok": payload["ok"],
                "gate": payload["gate"],
                "auto_provider": payload["provider"].get("auto_provider"),
                "worktree_dirty": payload["worktree"].get("dirty"),
                "task_spec_ok": payload["task_spec"].get("ok"),
                "witness_verified": payload["witness"].get("verified"),
            }
        )
        print(json.dumps(payload, indent=2, ensure_ascii=False) if args.json else _format_operator_panel_payload(payload))
        return 0 if payload["ok"] else 2
    if command in {"claim-contract", "claim-check", "claim-gate", "contrato-claim"}:
        contract_ref = " ".join(items[1:]).strip()
        if not contract_ref:
            payload = {
                "ok": False,
                "action": "claim_contract_evaluation",
                "gate": "REVIEW",
                "error": "missing_claim_contract_path",
            }
        else:
            try:
                payload = evaluate_claim_contract(workspace=config.workspace, spec_path=contract_ref)
            except Exception as exc:
                payload = {
                    "ok": False,
                    "action": "claim_contract_evaluation",
                    "gate": "REVIEW",
                    "error": str(exc),
                }
        LocalMemory(config.runtime_root).append_event(
            {
                "channel": "wabi_claim_contract",
                "ok": payload.get("ok"),
                "gate": payload.get("gate"),
                "contract": payload.get("contract_path", contract_ref),
                "status": payload.get("status", ""),
            }
        )
        print(json.dumps(payload, indent=2, ensure_ascii=False) if args.json else _format_claim_contract_payload(payload))
        return 0 if payload.get("ok") else 2
    if command in {"claim-observation", "claim-adapter", "observation-claim", "claim-envelope"}:
        claim = " ".join(items[1:]).strip()
        if not claim:
            payload = {
                "ok": False,
                "action": "claim_observation_adapter",
                "gate": "REVIEW",
                "error": "missing_claim",
                "cloud_provider_called": False,
                "applied_to_sources": False,
                "publication_gate": "BLOCK",
            }
        else:
            try:
                payload = run_claim_observation_adapter(
                    claim,
                    workspace=config.workspace,
                    runtime_root=config.runtime_root,
                    persist=True,
                )
            except Exception as exc:
                payload = {
                    "ok": False,
                    "action": "claim_observation_adapter",
                    "gate": "REVIEW",
                    "error": redact_text(str(exc)),
                    "cloud_provider_called": False,
                    "applied_to_sources": False,
                    "publication_gate": "BLOCK",
                }
        LocalMemory(config.runtime_root).append_event(
            {
                "channel": "wabi_claim_observation_adapter_cli",
                "ok": payload.get("ok", False),
                "gate": payload.get("classification", {}).get("gate", payload.get("gate", "")),
                "mode": payload.get("mode", ""),
            }
        )
        print(json.dumps(payload, indent=2, ensure_ascii=False) if args.json else _format_claim_observation_payload(payload))
        return 0 if payload.get("ok") else 2
    if command in {"claim-fixtures", "claim-fixture-review", "claim-adapter-fixtures"}:
        fixture_ref = " ".join(items[1:]).strip()
        if not fixture_ref:
            payload = {
                "ok": False,
                "action": "claim_observation_fixture_review",
                "status": "REVIEW",
                "error": "missing_fixture_path",
                "cloud_provider_called": False,
                "applied_to_sources": False,
                "publication_gate": "BLOCK",
            }
        else:
            try:
                payload = run_claim_fixture_review(
                    fixture_ref,
                    workspace=config.workspace,
                    runtime_root=config.runtime_root,
                    persist=True,
                )
            except Exception as exc:
                payload = {
                    "ok": False,
                    "action": "claim_observation_fixture_review",
                    "status": "REVIEW",
                    "error": redact_text(str(exc)),
                    "cloud_provider_called": False,
                    "applied_to_sources": False,
                    "publication_gate": "BLOCK",
                }
        LocalMemory(config.runtime_root).append_event(
            {
                "channel": "wabi_claim_observation_fixtures_cli",
                "ok": payload.get("ok", False),
                "status": payload.get("status", ""),
                "case_count": payload.get("case_count", 0),
                "review_count": payload.get("review_count", 0),
            }
        )
        print(json.dumps(payload, indent=2, ensure_ascii=False) if args.json else _format_claim_fixture_review_payload(payload))
        return 0 if payload.get("ok") else 2
    if command in {"hypothesis", "hipotesis", "conjecture", "counterexample", "contraejemplo", "falsifier"}:
        claim = " ".join(items[1:]).strip()
        if not claim:
            payload = {
                "ok": False,
                "action": "conjecture_counterexample",
                "gate": "REVIEW",
                "error": "missing_hypothesis_claim",
                "cloud_provider_called": False,
                "applied_to_sources": False,
                "publication_gate": "BLOCK",
            }
        else:
            try:
                payload = run_conjecture_counterexample(
                    claim,
                    workspace=config.workspace,
                    runtime_root=config.runtime_root,
                    persist=True,
                )
            except Exception as exc:
                payload = {
                    "ok": False,
                    "action": "conjecture_counterexample",
                    "gate": "REVIEW",
                    "error": redact_text(str(exc)),
                    "cloud_provider_called": False,
                    "applied_to_sources": False,
                    "publication_gate": "BLOCK",
                }
        LocalMemory(config.runtime_root).append_event(
            {
                "channel": "wabi_conjecture_counterexample_cli",
                "ok": payload.get("ok", False),
                "gate": payload.get("evaluation", {}).get("gate", payload.get("gate", "")),
                "status": payload.get("evaluation", {}).get("status", ""),
                "hypothesis_id": payload.get("hypothesis_packet", {}).get("hypothesis_id", ""),
            }
        )
        print(json.dumps(payload, indent=2, ensure_ascii=False) if args.json else _format_hypothesis_payload(payload))
        return 0 if payload.get("ok") else 2
    if command in {"project-scan", "scan-project", "repo-scan", "scanner-proyecto"}:
        payload = scan_project(workspace=config.workspace)
        LocalMemory(config.runtime_root).append_event(
            {
                "channel": "wabi_project_scan",
                "ok": payload["ok"],
                "package_managers": payload["package_managers"],
                "test_command_count": len(payload["test_commands"]),
            }
        )
        print(json.dumps(payload, indent=2, ensure_ascii=False) if args.json else _format_project_scan_payload(payload))
        return 0
    if command in {"test-plan", "plan-tests", "verification-plan", "plan-pruebas"}:
        payload = build_test_plan(workspace=config.workspace)
        LocalMemory(config.runtime_root).append_event(
            {
                "channel": "wabi_test_plan",
                "ok": payload["ok"],
                "command_count": len(payload["commands"]),
                "auto_execute": payload["policy"]["auto_execute"],
            }
        )
        print(json.dumps(payload, indent=2, ensure_ascii=False) if args.json else _format_test_plan_payload(payload))
        return 0
    if command in {"run-safe-tests", "safe-tests", "run-tests-safe", "ejecutar-pruebas-seguras"}:
        payload = run_safe_tests(workspace=config.workspace, runtime_root=config.runtime_root)
        LocalMemory(config.runtime_root).append_event(
            {
                "channel": "wabi_run_safe_tests",
                "ok": payload["ok"],
                "artifact": payload["artifact"],
                "passed": payload["summary"]["passed"],
                "failed": payload["summary"]["failed"],
                "witness_verified": payload["witness_verified"],
            }
        )
        print(json.dumps(payload, indent=2, ensure_ascii=False) if args.json else _format_safe_test_run_payload(payload))
        return 0 if payload["ok"] else 2
    if command in {"curator-assistant", "curador-assistant", "orden-assistant", "curador-orden"}:
        payload = run_curator_assistant(workspace=config.workspace, runtime_root=config.runtime_root)
        LocalMemory(config.runtime_root).append_event(
            {
                "channel": "wabi_curator_assistant",
                "ok": payload["ok"],
                "artifact": payload["artifact"],
                "markdown_artifact": payload["markdown_artifact"],
                "candidate_count": payload["summary"]["candidate_count"],
                "safe_cleanup_performed": payload["summary"]["safe_cleanup_performed"],
                "witness_verified": payload["witness_verified"],
            }
        )
        print(json.dumps(payload, indent=2, ensure_ascii=False) if args.json else _format_curator_assistant_payload(payload))
        return 0 if payload["ok"] else 2
    if command in {"curator-fichas", "curador-fichas", "fichas-curador", "orden-fichas"}:
        report_ref = " ".join(items[1:]).strip() or None
        payload = run_curator_fichas(workspace=config.workspace, runtime_root=config.runtime_root, report_path=report_ref)
        LocalMemory(config.runtime_root).append_event(
            {
                "channel": "wabi_curator_fichas",
                "ok": payload["ok"],
                "artifact": payload["artifact"],
                "markdown_artifact": payload["markdown_artifact"],
                "workspace_doc": payload["workspace_doc"],
                "ficha_count": payload["summary"]["ficha_count"],
                "delete_approved_count": payload["summary"]["delete_approved_count"],
                "witness_verified": payload["witness_verified"],
            }
        )
        print(json.dumps(payload, indent=2, ensure_ascii=False) if args.json else _format_curator_fichas_payload(payload))
        return 0 if payload["ok"] else 2
    if command in {"cerebro-index", "cerebro", "cerebro-navigation", "indice-cerebro"}:
        payload = build_cerebro_navigation(config.workspace)
        if args.write_docs:
            payload["artifacts"] = write_cerebro_navigation_docs(payload)
            payload["action"] = "cerebro_index_docs_written"
        else:
            payload["artifacts"] = []
            payload["action"] = "cerebro_index_dry_run"
        LocalMemory(config.runtime_root).append_event(
            {
                "channel": "wabi_cerebro_index",
                "ok": payload["ok"],
                "action": payload["action"],
                "artifact_count": len(payload["artifacts"]),
                "source_count": payload["source_summary"]["source_count"],
            }
        )
        print(json.dumps(payload, indent=2, ensure_ascii=False) if args.json else _format_cerebro_index_payload(payload))
        return 0 if payload["ok"] else 2
    if command in {"cerebro-audit", "line-audit", "auditar-cerebro", "cerebro-lineas"}:
        payload = build_cerebro_line_audit(config.workspace)
        if args.write_docs:
            payload["artifacts"] = write_cerebro_audit_outputs(payload)
            payload["action"] = "cerebro_line_audit_docs_written"
        else:
            payload["artifacts"] = []
            payload["action"] = "cerebro_line_audit_dry_run"
        LocalMemory(config.runtime_root).append_event(
            {
                "channel": "wabi_cerebro_line_audit",
                "ok": payload["ok"],
                "action": payload["action"],
                "artifact_count": len(payload["artifacts"]),
                "file_count": payload.get("summary", {}).get("file_count_total", 0),
                "total_lines": payload.get("summary", {}).get("total_lines", 0),
                "variant_groups": payload.get("summary", {}).get("variant_group_count", 0),
            }
        )
        output_payload = compact_cerebro_audit_payload(payload) if args.json else payload
        print(json.dumps(output_payload, indent=2, ensure_ascii=False) if args.json else _format_cerebro_line_audit_payload(payload))
        return 0 if payload["ok"] else 2
    if command in {"project-graph", "tech-index", "technology-index", "grafo-maestro", "indice-tecnologia"}:
        payload = build_cerebro_line_audit(config.workspace)
        if args.write_docs:
            payload["artifacts"] = write_cerebro_audit_outputs(payload)
        else:
            payload["artifacts"] = []
        graph_payload = {
            "ok": payload["ok"],
            "action": "project_graph",
            "workspace": payload["workspace"],
            "summary": payload.get("summary", {}),
            "technology_atoms": payload.get("technology_atoms", []),
            "project_graph": payload.get("project_graph", {}),
            "artifacts": payload.get("artifacts", []),
        }
        LocalMemory(config.runtime_root).append_event(
            {
                "channel": "wabi_project_graph",
                "ok": graph_payload["ok"],
                "technology_atoms": len(graph_payload["technology_atoms"]),
                "nodes": len(graph_payload["project_graph"].get("nodes", [])),
            }
        )
        print(json.dumps(graph_payload, indent=2, ensure_ascii=False) if args.json else _format_project_graph_payload(graph_payload))
        return 0 if graph_payload["ok"] else 2
    if command in {"variant-compare", "cerebro-variant-compare", "comparar-variantes", "variant-semantic"}:
        payload = build_cerebro_variant_comparison(config.workspace)
        if args.write_docs:
            artifacts = write_cerebro_variant_comparison(payload, config.workspace / "runtime" / "cerebro_master_index")
            payload["artifacts"] = artifacts
            payload["action"] = "cerebro_variant_comparison_docs_written"
        else:
            payload["artifacts"] = []
            payload["action"] = "cerebro_variant_comparison_dry_run"
        LocalMemory(config.runtime_root).append_event(
            {
                "channel": "wabi_cerebro_variant_comparison",
                "ok": payload["ok"],
                "action": payload["action"],
                "variant_groups": payload["summary"]["variant_group_count"],
                "archive_review_candidates": payload["summary"]["archive_review_candidates"],
                "canon_merge_review_candidates": payload["summary"]["canon_merge_review_candidates"],
            }
        )
        output_payload = compact_cerebro_variant_comparison(payload) if args.json else payload
        print(json.dumps(output_payload, indent=2, ensure_ascii=False) if args.json else _format_variant_comparison_payload(payload))
        return 0 if payload["ok"] else 2
    if command in {
        "duplicate-migration-plan",
        "cerebro-duplicate-plan",
        "plan-duplicados",
        "variant-archive-plan",
    }:
        payload = build_cerebro_duplicate_migration_plan(config.workspace)
        if args.write_docs:
            artifacts = write_cerebro_duplicate_migration_plan(payload, config.workspace / "runtime" / "cerebro_master_index")
            payload["artifacts"] = artifacts
            payload["action"] = "cerebro_duplicate_migration_plan_docs_written"
        else:
            payload["artifacts"] = []
            payload["action"] = "cerebro_duplicate_migration_plan_dry_run"
        LocalMemory(config.runtime_root).append_event(
            {
                "channel": "wabi_cerebro_duplicate_migration_plan",
                "ok": payload["ok"],
                "action": payload["action"],
                "proposed_archive_moves": payload["summary"]["proposed_archive_moves"],
                "ready_for_review": payload["summary"]["ready_for_review"],
                "blocked_moves": payload["summary"]["blocked_moves"],
            }
        )
        output_payload = compact_cerebro_duplicate_migration_plan(payload) if args.json else payload
        print(json.dumps(output_payload, indent=2, ensure_ascii=False) if args.json else _format_duplicate_migration_plan_payload(payload))
        return 0 if payload["ok"] else 2
    if command in {
        "canon-merge-review",
        "cerebro-merge-review",
        "merge-review-pack",
        "review-merge-canonico",
    }:
        payload = build_cerebro_canon_merge_review(config.workspace)
        if args.write_docs:
            artifacts = write_cerebro_canon_merge_review(payload, config.workspace / "runtime" / "cerebro_master_index")
            payload["artifacts"] = artifacts
            payload["action"] = "cerebro_canon_merge_review_pack_written"
        else:
            payload["artifacts"] = []
            payload["action"] = "cerebro_canon_merge_review_dry_run"
        LocalMemory(config.runtime_root).append_event(
            {
                "channel": "wabi_cerebro_canon_merge_review",
                "ok": payload["ok"],
                "action": payload["action"],
                "review_candidate_groups": payload["summary"]["review_candidate_groups"],
                "unique_candidate_sets": payload["summary"]["unique_candidate_sets"],
                "auto_merge_actions": payload["summary"]["auto_merge_actions"],
            }
        )
        output_payload = compact_cerebro_canon_merge_review(payload) if args.json else payload
        print(json.dumps(output_payload, indent=2, ensure_ascii=False) if args.json else _format_canon_merge_review_payload(payload))
        return 0 if payload["ok"] else 2
    if command in {"archive-intake", "cerebro-archive-intake", "intake-archivo", "absorber-archivo"}:
        archive_ref = " ".join(items[1:]).strip() or None
        payload = run_archive_intake(config.workspace, archive_path=archive_ref)
        LocalMemory(config.runtime_root).append_event(
            {
                "channel": "wabi_cerebro_archive_intake",
                "ok": payload["ok"],
                "archive": payload["archive"],
                "text_indexed_count": payload["summary"]["text_indexed_count"],
                "member_count": payload["summary"]["member_count"],
            }
        )
        output_payload = compact_archive_intake_payload(payload) if args.json else payload
        print(json.dumps(output_payload, indent=2, ensure_ascii=False) if args.json else _format_archive_intake_payload(payload))
        return 0 if payload["ok"] else 2
    if command in {"geodia-synthetic", "geodia-math", "geodia-surface", "duat-geodia-synthetic"}:
        payload = build_geodia_synthetic_surface()
        LocalMemory(config.runtime_root).append_event(
            {
                "channel": "wabi_geodia_synthetic_surface",
                "ok": payload["ok"],
                "status": payload["status"],
                "claim_gate": payload["claim_gate"],
                "regime": payload["metrics"]["after"]["regime"],
                "bounded": payload["bounded"],
            }
        )
        print(json.dumps(payload, indent=2, ensure_ascii=False) if args.json else _format_geodia_synthetic_payload(payload))
        return 0 if payload["ok"] else 2
    if command in {"geodia-falsifier", "geodia-claim-falsifier", "duat-geodia-falsifier"}:
        payload = build_geodia_synthetic_falsifier()
        payload = write_geodia_synthetic_falsifier(payload, workspace=config.workspace, output_dir=config.output_dir)
        LocalMemory(config.runtime_root).append_event(
            {
                "channel": "wabi_geodia_synthetic_falsifier",
                "ok": payload["ok"],
                "result": payload["result"],
                "claim_gate": payload["claim_gate"],
                "claim_contract_gate": payload["claim_evaluation"]["gate"],
                "artifacts": payload["artifacts"],
            }
        )
        print(json.dumps(payload, indent=2, ensure_ascii=False) if args.json else _format_geodia_falsifier_payload(payload))
        return 0 if payload["ok"] else 2
    if command in {"browser-gate", "navegador-gate", "gate-browser"}:
        url = " ".join(items[1:]).strip()
        payload = {
            "ok": True,
            "action": "browser_gate",
            "policy": build_browser_gate_policy(config.workspace),
            "evaluation": evaluate_browser_request(url) if url else None,
        }
        LocalMemory(config.runtime_root).append_event(
            {
                "channel": "wabi_browser_gate",
                "ok": True,
                "evaluated": bool(url),
                "gate": payload["evaluation"].get("gate") if payload["evaluation"] else "POLICY",
            }
        )
        print(json.dumps(payload, indent=2, ensure_ascii=False) if args.json else _format_browser_gate_payload(payload))
        return 0
    if command in {"browser-bridge", "browserbridge", "navegador-bridge", "puente-navegador"}:
        payload = _execute_browser_bridge_command(
            config,
            items[1:],
            backend=args.browser_backend,
            send_requested=args.send,
            service=args.service,
            payload_class=args.payload_class,
            input_path=args.input,
            snapshot_url=args.snapshot_url,
        )
        LocalMemory(config.runtime_root).append_event(
            {
                "channel": "wabi_browser_bridge",
                "ok": payload.get("ok", False),
                "action": payload.get("action", ""),
                "gate": payload.get("gate", "APPROVE"),
                "browser_backend_called": payload.get("browser_backend_called", False),
                "online_ai_called": payload.get("online_ai_called", False),
                "artifact": payload.get("artifact", ""),
            }
        )
        print(json.dumps(payload, indent=2, ensure_ascii=False) if args.json else _format_browser_bridge_payload(payload))
        gate = str(payload.get("gate", ""))
        return 0 if payload.get("ok") or gate in {"REVIEW", "REVIEW_SKIPPED"} else 2
    if command in {"velo", "navegador-velo", "browser-velo", "puente-velo"}:
        payload = _execute_velo_command(
            config,
            items[1:],
            service=args.service,
            host=args.velo_host,
            port=args.velo_port,
            headless=args.headless,
            answer_timeout=float(args.codex_timeout * 3),
        )
        LocalMemory(config.runtime_root).append_event(
            {
                "channel": "wabi_velo",
                "ok": payload.get("ok", False),
                "action": payload.get("action", ""),
                "gate": payload.get("gate", "APPROVE"),
                "site": payload.get("site", ""),
                "online_ai_called": payload.get("online_ai_called", False),
                "artifact": payload.get("artifact", ""),
            }
        )
        print(json.dumps(payload, indent=2, ensure_ascii=False) if args.json else _format_velo_payload(payload))
        gate = str(payload.get("gate", ""))
        return 0 if payload.get("ok") or gate in {"REVIEW", "REVIEW_SKIPPED"} else 2
    if command in {"functional-status", "estado-funcional", "status-funcional", "boot-gate", "os-boot-gate"}:
        payload = build_functional_status(config.workspace, config.runtime_root)
        artifact = write_functional_status(payload, config.output_dir)
        payload["artifact"] = str(artifact)
        LocalMemory(config.runtime_root).append_event(
            {
                "channel": "wabi_functional_status",
                "status": payload["status"],
                "artifact": str(artifact),
                "cerebro": payload["cerebro_line_audit"]["status"],
                "agents": payload["agents_can_program"]["status"],
                "duat_geodia": payload["duat_geodia_os"]["status"],
            }
        )
        print(json.dumps(payload, indent=2, ensure_ascii=False) if args.json else _format_functional_status_payload(payload))
        return 0 if payload["status"] != "BLOCKED" else 2
    if command in {"tools", "tool-registry", "herramientas"}:
        payload = tool_registry_payload()
        print(json.dumps(payload, indent=2, ensure_ascii=False) if args.json else _format_tool_registry_payload(payload))
        return 0
    if command in {"engine-status", "motor-status", "engine-manifest", "motor-manifest"}:
        payload = _execute_engine_status_command()
        LocalMemory(config.runtime_root).append_event(
            {
                "channel": "wabi_engine_status",
                "ok": payload["ok"],
                "modules": len(payload["manifest"].get("modules", {})),
            }
        )
        print(json.dumps(payload, indent=2, ensure_ascii=False) if args.json else _format_engine_status_payload(payload))
        return 0
    if command in {"engine-intake", "motor-intake", "source-card", "fuente-motor"}:
        payload = _execute_engine_intake_command(items[1:])
        LocalMemory(config.runtime_root).append_event(
            {
                "channel": "wabi_engine_intake",
                "ok": payload["ok"],
                "source": payload.get("source_card", {}).get("source_name", ""),
                "gate": payload.get("source_card", {}).get("action_gate", ""),
            }
        )
        print(json.dumps(payload, indent=2, ensure_ascii=False) if args.json else _format_engine_intake_payload(payload))
        return 0 if payload["ok"] else 2
    if command in {"engine-plan", "motor-plan", "plan-motor"}:
        payload = _execute_engine_plan_command(config, items[1:], write_docs=args.write_docs)
        LocalMemory(config.runtime_root).append_event(
            {
                "channel": "wabi_engine_plan",
                "ok": payload["ok"],
                "gate": payload.get("plan", {}).get("action_gate", ""),
                "modules": len(payload.get("plan", {}).get("modules", [])),
            }
        )
        print(json.dumps(payload, indent=2, ensure_ascii=False) if args.json else _format_engine_plan_payload(payload))
        return 0 if payload["ok"] else 2
    if command in {"engine-task-spec", "motor-task-spec", "engine-spec", "motor-spec"}:
        payload = _execute_engine_task_spec_command(
            config,
            items[1:],
            target=args.target,
            write_docs=args.write_docs,
        )
        LocalMemory(config.runtime_root).append_event(
            {
                "channel": "wabi_engine_task_spec",
                "ok": payload["ok"],
                "target": payload.get("target", ""),
                "gate": payload.get("metadata", {}).get("action_gate", ""),
            }
        )
        print(json.dumps(payload, indent=2, ensure_ascii=False) if args.json else _format_engine_task_spec_payload(payload))
        return 0 if payload["ok"] else 2
    if command in {"engine-sandbox", "engine-observatorio", "motor-sandbox", "observatorio-sandbox"}:
        payload = _execute_engine_sandbox_command(config, items[1:], write_docs=args.write_docs)
        LocalMemory(config.runtime_root).append_event(
            {
                "channel": "wabi_engine_sandbox",
                "ok": payload["ok"],
                "artifact": payload.get("artifact", ""),
                "fingerprint": payload.get("validation", {}).get("fingerprint", ""),
            }
        )
        print(json.dumps(payload, indent=2, ensure_ascii=False) if args.json else _format_engine_sandbox_payload(payload))
        return 0 if payload["ok"] else 2
    if command in {"engine-project-validate", "engine-validate", "motor-validar"}:
        payload = _execute_engine_project_validate_command(config, items[1:])
        LocalMemory(config.runtime_root).append_event(
            {
                "channel": "wabi_engine_project_validate",
                "ok": payload["ok"],
                "spec": payload.get("spec_path", ""),
                "fingerprint": payload.get("validation", {}).get("fingerprint", ""),
            }
        )
        print(json.dumps(payload, indent=2, ensure_ascii=False) if args.json else _format_engine_project_validation_payload(payload))
        return 0 if payload["ok"] else 2
    if command in {"engine-simulate", "engine-run", "motor-simular"}:
        payload = _execute_engine_simulate_command(config, items[1:])
        LocalMemory(config.runtime_root).append_event(
            {
                "channel": "wabi_engine_simulate",
                "ok": payload["ok"],
                "spec": payload.get("spec_path", ""),
                "event_count": payload.get("simulation", {}).get("event_count", 0),
                "fired_rules": len(payload.get("simulation", {}).get("fired_rules", [])),
            }
        )
        print(json.dumps(payload, indent=2, ensure_ascii=False) if args.json else _format_engine_simulation_payload(payload))
        return 0 if payload["ok"] else 2
    if command in {"worktree-status", "git-status", "diff-summary", "estado-git"}:
        payload = git_worktree_summary(config.workspace)
        LocalMemory(config.runtime_root).append_event(
            {
                "channel": "wabi_git_worktree_summary",
                "ok": payload["ok"],
                "dirty": payload.get("dirty"),
                "status_count": payload.get("status_count"),
            }
        )
        print(json.dumps(payload, indent=2, ensure_ascii=False) if args.json else _format_worktree_payload(payload))
        return 0 if payload["ok"] else 2
    if command in {"patch-plan", "plan-patch", "plan-parche"}:
        payload = _execute_patch_plan_command(
            config,
            items[1:],
            target=args.target,
            apply_patch=False,
            test_commands=args.test_command,
        )
        LocalMemory(config.runtime_root).append_event(
            {
                "channel": "wabi_patch_plan",
                "ok": payload["ok"],
                "target": payload.get("target", ""),
                "plan": payload.get("plan_artifact", ""),
            }
        )
        print(json.dumps(payload, indent=2, ensure_ascii=False) if args.json else _format_patch_payload(payload))
        return 0 if payload["ok"] else 2
    if command in {"patch-apply", "apply-patch", "aplicar-parche"}:
        payload = _execute_patch_plan_command(
            config,
            items[1:],
            target=args.target,
            apply_patch=True,
            test_commands=args.test_command,
        )
        LocalMemory(config.runtime_root).append_event(
            {
                "channel": "wabi_patch_apply",
                "ok": payload["ok"],
                "target": payload.get("target", ""),
                "plan": payload.get("plan_artifact", ""),
                "rollback": payload.get("rollback_artifact", ""),
            }
        )
        print(json.dumps(payload, indent=2, ensure_ascii=False) if args.json else _format_patch_payload(payload))
        return 0 if payload["ok"] else 2
    if command in {"cloud-proposal-validate", "cloud-proposal-validar"}:
        payload = _execute_cloud_proposal_command(config, items[1:], mode="validate")
        LocalMemory(config.runtime_root).append_event(
            {
                "channel": "wabi_cloud_proposal_validate",
                "ok": payload["ok"],
                "proposal": payload.get("proposal_path", ""),
                "errors": payload.get("validation", {}).get("errors", []),
            }
        )
        print(json.dumps(payload, indent=2, ensure_ascii=False) if args.json else _format_cloud_proposal_payload(payload))
        return 0 if payload["ok"] else 2
    if command in {"cloud-proposal-task-spec", "cloud-proposal-spec"}:
        payload = _execute_cloud_proposal_command(config, items[1:], mode="task_spec")
        LocalMemory(config.runtime_root).append_event(
            {
                "channel": "wabi_cloud_proposal_task_spec",
                "ok": payload["ok"],
                "proposal": payload.get("proposal_path", ""),
                "task_spec": payload.get("task_spec_artifact", ""),
            }
        )
        print(json.dumps(payload, indent=2, ensure_ascii=False) if args.json else _format_cloud_proposal_payload(payload))
        return 0 if payload["ok"] else 2
    if command in {"cloud-proposal-plan", "cloud-proposal-patch-plan"}:
        payload = _execute_cloud_proposal_command(config, items[1:], mode="plan")
        LocalMemory(config.runtime_root).append_event(
            {
                "channel": "wabi_cloud_proposal_plan",
                "ok": payload["ok"],
                "proposal": payload.get("proposal_path", ""),
                "task_spec": payload.get("task_spec_artifact", ""),
                "plan": payload.get("plan_artifact", ""),
            }
        )
        print(json.dumps(payload, indent=2, ensure_ascii=False) if args.json else _format_cloud_proposal_payload(payload))
        return 0 if payload["ok"] else 2
    if command in {"cloud-proposal-from-provider", "cloud-proposal-generate", "cloud-proposal-provider"}:
        payload = _execute_cloud_proposal_from_provider_command(
            config,
            items[1:],
            mode="validate",
            provider=args.codex_provider,
            timeout=args.codex_timeout,
            dry_run=args.dry_run,
        )
        LocalMemory(config.runtime_root).append_event(
            {
                "channel": "wabi_cloud_proposal_from_provider",
                "ok": payload["ok"],
                "provider": payload.get("provider", ""),
                "proposal": payload.get("proposal_artifact", ""),
                "cloud_provider_called": payload.get("cloud_provider_called", False),
            }
        )
        print(json.dumps(payload, indent=2, ensure_ascii=False) if args.json else _format_cloud_proposal_payload(payload))
        return 0 if payload["ok"] else 2
    if command in {"cloud-proposal-from-provider-task-spec", "cloud-proposal-generate-task-spec"}:
        payload = _execute_cloud_proposal_from_provider_command(
            config,
            items[1:],
            mode="task_spec",
            provider=args.codex_provider,
            timeout=args.codex_timeout,
            dry_run=args.dry_run,
        )
        LocalMemory(config.runtime_root).append_event(
            {
                "channel": "wabi_cloud_proposal_from_provider_task_spec",
                "ok": payload["ok"],
                "provider": payload.get("provider", ""),
                "proposal": payload.get("proposal_artifact", ""),
                "task_spec": payload.get("task_spec_artifact", ""),
                "cloud_provider_called": payload.get("cloud_provider_called", False),
            }
        )
        print(json.dumps(payload, indent=2, ensure_ascii=False) if args.json else _format_cloud_proposal_payload(payload))
        return 0 if payload["ok"] else 2
    if command in {"cloud-proposal-from-provider-plan", "cloud-proposal-generate-plan"}:
        payload = _execute_cloud_proposal_from_provider_command(
            config,
            items[1:],
            mode="plan",
            provider=args.codex_provider,
            timeout=args.codex_timeout,
            dry_run=args.dry_run,
        )
        LocalMemory(config.runtime_root).append_event(
            {
                "channel": "wabi_cloud_proposal_from_provider_plan",
                "ok": payload["ok"],
                "provider": payload.get("provider", ""),
                "proposal": payload.get("proposal_artifact", ""),
                "task_spec": payload.get("task_spec_artifact", ""),
                "plan": payload.get("plan_artifact", ""),
                "cloud_provider_called": payload.get("cloud_provider_called", False),
            }
        )
        print(json.dumps(payload, indent=2, ensure_ascii=False) if args.json else _format_cloud_proposal_payload(payload))
        return 0 if payload["ok"] else 2
    if command in {"cloud-debug-loop", "cloud-debug"}:
        task_ref = args.task or " ".join(items[1:]).strip()
        if not task_ref:
            payload = {
                "ok": False,
                "mode": "apply" if args.apply else "dry_run",
                "error": "missing_task_spec_path",
                "apply_status": "BLOCKED",
                "secret_values_printed": False,
            }
        else:
            payload = run_cloud_debug_loop(
                workspace=config.workspace,
                runtime_root=config.runtime_root,
                task_spec_path=task_ref,
                apply_patch=bool(args.apply),
            )
        LocalMemory(config.runtime_root).append_event(
            {
                "channel": "wabi_cloud_debug_loop",
                "ok": payload.get("ok", False),
                "mode": payload.get("mode", ""),
                "apply_status": payload.get("apply_status", ""),
                "witness_path": payload.get("witness_path", ""),
            }
        )
        print(json.dumps(payload, indent=2, ensure_ascii=False) if args.json else _format_cloud_debug_loop_payload(payload))
        return 0 if payload.get("ok") else 2
    if command in {"apply-local-preview", "local-apply-preview", "task-spec-apply-local-preview"}:
        try:
            task_spec = _load_local_apply_task_spec(config, items[1:], latest=args.latest)
            payload = preview_local_apply(task_spec, workspace=config.workspace, runtime_root=config.runtime_root)
        except Exception as exc:
            payload = {
                "ok": False,
                "status": "LOCAL_APPLY_REVIEW_REQUIRED",
                "reason": redact_text(str(exc)),
                "applied_to_sources": False,
                "cloud_provider_called": False,
                "graphics_live": False,
                "publication_gate": "BLOCK",
            }
        LocalMemory(config.runtime_root).append_event(
            {
                "channel": "wabi_local_apply_preview",
                "ok": payload.get("ok", False),
                "status": payload.get("status", ""),
                "cloud_provider_called": False,
            }
        )
        print(json.dumps(payload, indent=2, ensure_ascii=False) if args.json else _format_local_apply_payload(payload))
        return 0 if payload.get("ok") or payload.get("status") in {"LOCAL_APPLY_PATCH_READY", "LOCAL_APPLY_READY"} else 2
    if command in {"apply-local", "local-apply", "task-spec-apply-local"}:
        try:
            task_spec = _load_local_apply_task_spec(config, items[1:], latest=args.latest)
            payload = apply_local_task_spec(task_spec, workspace=config.workspace, runtime_root=config.runtime_root)
        except Exception as exc:
            payload = {
                "ok": False,
                "status": "LOCAL_APPLY_REVIEW_REQUIRED",
                "reason": redact_text(str(exc)),
                "applied_to_sources": False,
                "cloud_provider_called": False,
                "graphics_live": False,
                "publication_gate": "BLOCK",
            }
        LocalMemory(config.runtime_root).append_event(
            {
                "channel": "wabi_local_apply",
                "ok": payload.get("ok", False),
                "status": payload.get("status", ""),
                "applied_to_sources": payload.get("applied_to_sources", False),
            }
        )
        print(json.dumps(payload, indent=2, ensure_ascii=False) if args.json else _format_local_apply_payload(payload))
        return 0 if payload.get("ok") else 2
    if command in {"task-spec-plan", "spec-plan", "plan-spec"}:
        payload = _execute_task_spec_command(config, items[1:], apply_patch=False)
        LocalMemory(config.runtime_root).append_event(
            {
                "channel": "wabi_task_spec_plan",
                "ok": payload["ok"],
                "spec": payload.get("spec_path", ""),
                "plan": payload.get("plan_artifact", ""),
            }
        )
        print(json.dumps(payload, indent=2, ensure_ascii=False) if args.json else _format_task_spec_payload(payload))
        return 0 if payload["ok"] else 2
    if command in {"task-spec-apply", "spec-apply", "aplicar-spec"}:
        payload = _execute_task_spec_command(config, items[1:], apply_patch=True)
        LocalMemory(config.runtime_root).append_event(
            {
                "channel": "wabi_task_spec_apply",
                "ok": payload["ok"],
                "spec": payload.get("spec_path", ""),
                "plan": payload.get("plan_artifact", ""),
                "rollback": payload.get("rollback_artifact", ""),
            }
        )
        print(json.dumps(payload, indent=2, ensure_ascii=False) if args.json else _format_task_spec_payload(payload))
        return 0 if payload["ok"] else 2
    if command in {"rollback", "revert", "revertir"}:
        rollback_ref = " ".join(items[1:]).strip()
        if not rollback_ref:
            payload = {"ok": False, "action": "rollback", "error": "missing_rollback_id_or_path"}
        else:
            try:
                result = RollbackStore(workspace=config.workspace, runtime_root=config.runtime_root).restore(rollback_ref)
                payload = {"ok": True, "action": "rollback", "result": result}
            except Exception as exc:
                payload = {"ok": False, "action": "rollback", "error": str(exc)}
        LocalMemory(config.runtime_root).append_event(
            {
                "channel": "wabi_rollback",
                "ok": payload["ok"],
                "ref": rollback_ref,
                "error": payload.get("error", ""),
            }
        )
        print(json.dumps(payload, indent=2, ensure_ascii=False) if args.json else _format_rollback_payload(payload))
        return 0 if payload["ok"] else 2
    if command in {"programmer-workpack", "programming-workpack", "workpack-programacion"}:
        workpack_prompt = " ".join(items[1:]).strip() or "preparar programacion multiarchivo como workpack REVIEW"
        orchestrator = ProviderOrchestrator(workspace=config.workspace, runtime_root=config.runtime_root)
        snapshot = build_environment_snapshot(
            workspace=config.workspace,
            runtime_root=config.runtime_root,
            provider_status=orchestrator.status(),
            run_comms_validator=True,
        )
        workpack = build_programmer_workpack(prompt=workpack_prompt, snapshot=snapshot)
        artifact = write_programmer_workpack(config.output_dir, workpack)
        payload = {
            "ok": True,
            "action": "programmer_workpack",
            "artifact": str(artifact),
            "workpack": workpack,
        }
        LocalMemory(config.runtime_root).append_event(
            {
                "channel": "wabi_programmer_workpack",
                "artifact": str(artifact),
                "application_gate": workpack["application_gate"],
                "workpack_hash": workpack["workpack_hash"],
            }
        )
        print(json.dumps(payload, indent=2, ensure_ascii=False) if args.json else _format_programmer_workpack_payload(payload))
        return 0
    if command == "eml":
        payload = _execute_eml_command(items[1:])
        print(json.dumps(payload, indent=2, ensure_ascii=False) if args.json else _format_eml_payload(payload))
        return 0 if payload["ok"] else 2
    if command == "agents":
        payload = registry.as_dict()
        print(json.dumps(payload, indent=2, ensure_ascii=False) if args.json else _format_agents(payload))
        return 0
    if command in {"codex-status", "status-codex"}:
        bridge = WabiCodexBridge(workspace=config.workspace, runtime_root=config.runtime_root)
        payload = bridge.status()
        print(json.dumps(payload, indent=2, ensure_ascii=False) if args.json else _format_codex_status(payload))
        return 0
    if command in {"codex", "ask-codex", "consulta-codex"}:
        prompt = " ".join(items[1:]).strip()
        if not prompt and not sys.stdin.isatty():
            prompt = sys.stdin.read().strip()
        if not prompt:
            print("Falta prompt para el puente Codex. Ejemplo: wabi codex \"resume este repo\"")
            return 2
        bridge = WabiCodexBridge(workspace=config.workspace, runtime_root=config.runtime_root)
        result = bridge.ask(
            prompt,
            provider=args.codex_provider,
            dry_run=args.dry_run,
            timeout=args.codex_timeout,
        )
        payload = result.to_dict()
        print(json.dumps(payload, indent=2, ensure_ascii=False) if args.json else _format_codex_payload(payload))
        return 0 if payload["ok"] else 2
    if command in {"diagnose", "diagnostico", "diagnóstico"}:
        payload = execute_prompt(
            "ejecuta diagnostico",
            workspace=args.workspace,
            runtime_root=args.runtime,
            agent_name=args.agent,
            json_mode=args.json,
            apply=args.apply,
            target=args.target,
        )
        if args.json:
            print(json.dumps(payload, indent=2, ensure_ascii=False))
        return 0 if payload["ok"] else 2
    if command == "logs":
        memory = LocalMemory(config.runtime_root)
        print(json.dumps(memory.tail_events(), indent=2, ensure_ascii=False))
        return 0
    if command in {"memory", "memoria"}:
        memory = LocalMemory(config.runtime_root)
        payload = {
            "summary": memory.conversation_summary(),
            "items": memory.tail_memory(),
        }
        print(json.dumps(payload, indent=2, ensure_ascii=False) if args.json else payload["summary"])
        return 0
    if command in {"bridge", "bridge-plan", "osit"}:
        bridge_prompt = " ".join(items[1:]).strip() or "estado local"
        executor = BridgeExecutor(config.runtime_root / "wabi_osit_bridge.sqlite")
        payload = executor.execute(
            bridge_prompt,
            intent=parse_command(bridge_prompt).intent,
            evidence_refs=["wabi_cli_bridge"],
            source="wabi_cli",
        ).to_dict()
        print(json.dumps(payload, indent=2, ensure_ascii=False) if args.json else _format_bridge_payload(payload))
        return 0 if payload["decision"]["gate"] != "BLOCK" else 2
    if command == "e2e-smoke":
        payload = execute_prompt(
            "crea una funcion que lea un archivo y resuma sus lineas",
            workspace=args.workspace,
            runtime_root=args.runtime,
            json_mode=args.json,
            apply=args.apply,
            target=args.target,
        )
        if args.json:
            print(json.dumps(payload, indent=2, ensure_ascii=False))
        return 0 if payload["ok"] else 2

    prompt = " ".join(items)
    payload = execute_prompt(
        prompt,
        workspace=args.workspace,
        runtime_root=args.runtime,
        agent_name=args.agent,
        json_mode=args.json,
        apply=args.apply,
        target=args.target,
    )
    if args.json:
        print(json.dumps(payload, indent=2, ensure_ascii=False))
    return 0 if payload["ok"] else 2


def _format_bridge_payload(payload: dict[str, Any]) -> str:
    decision = payload["decision"]
    envelope = payload["envelope"]
    lines = [
        "WABI SABI OSIT BRIDGE",
        f"Gate: {decision['gate']}  Ruta: {decision['route']}  Runtime: {decision['runtime']}",
        f"Modelo: {decision['model_id'] or 'none'}",
        f"R: {decision['r_estimate']}  Phi_eff: {decision['phi_eff']}",
        "",
        "RAZONES:",
    ]
    lines.extend(f"- {reason}" for reason in decision["reasons"])
    lines.append("")
    lines.append("EVIDENCIA:")
    if envelope["evidence_refs"]:
        lines.extend(f"- {item}" for item in envelope["evidence_refs"])
    else:
        lines.append("- Falta evidencia; queda en REVIEW/BLOCK segun riesgo.")
    lines.append("")
    lines.append("ACCION:")
    lines.append(f"- witness_event_id: {payload['witness_event_id']}")
    lines.append(f"- fingerprint: {envelope['fingerprint']}")
    if decision["blocked_actions"]:
        lines.append(f"- blocked_actions: {', '.join(decision['blocked_actions'])}")
    return "\n".join(lines)


def _format_environment_payload(payload: dict[str, Any]) -> str:
    snapshot = payload["snapshot"]
    decision = snapshot["decision"]
    host = snapshot["host"]
    pending = snapshot["pending"]
    comms = snapshot["comms"]
    lines = [
        "WABI SABI ENVIRONMENT",
        f"Modo: {decision['recommended_mode']}",
        f"Host: {host.get('status') or 'UNKNOWN'}/{host.get('gate') or 'UNKNOWN'}",
        f"Pending: {pending.get('active_dedup', 'UNKNOWN')} abiertos",
        f"COMMS: {comms.get('agent_count', 0)} agentes  Validator: {'OK' if comms.get('validator', {}).get('ok') else 'REVIEW'}",
        "",
        "ACCIONES PERMITIDAS:",
    ]
    lines.extend(f"- {item}" for item in decision.get("allowed_actions", []))
    lines.append("")
    lines.append("ACCIONES BLOQUEADAS:")
    lines.extend(f"- {item}" for item in decision.get("blocked_actions", []))
    lines.append("")
    lines.append(f"Artefacto: {payload['artifact']}")
    return "\n".join(lines)


def _format_comms_payload(payload: dict[str, Any]) -> str:
    comms = payload["comms"]
    validator = comms.get("validator", {})
    lines = [
        "WABI SABI COMMS",
        f"Root: {payload.get('portfolio_root') or 'NO_ENCONTRADO'}",
        f"Agentes: {comms.get('agent_count', 0)}  Invalidos: {comms.get('invalid_count', 0)}",
        f"Validator: {'OK' if validator.get('ok') else 'REVIEW'}",
        "",
        "GATES:",
    ]
    by_gate = comms.get("by_gate", {})
    if by_gate:
        lines.extend(f"- {gate}: {count}" for gate, count in sorted(by_gate.items()))
    else:
        lines.append("- Sin estados COMMS cargados.")
    lines.append("")
    lines.append(f"Artefacto: {payload['artifact']}")
    return "\n".join(lines)


def _format_decision_payload(payload: dict[str, Any]) -> str:
    record = payload["record"]
    lines = [
        "WABI SABI DECISION",
        f"Modo: {record['recommended_mode']}  Estado: {record['status']}",
        f"Host: {record['host_status']}/{record['host_gate']}",
        f"Witness: {'OK' if record['witness_verified'] else 'REVIEW'}",
        f"Hash: {record['record_hash']}",
        "",
        "SIGUIENTES ACCIONES:",
    ]
    lines.extend(f"- {item}" for item in record.get("next_actions", []))
    lines.append("")
    lines.append(f"Artefacto: {payload['artifact']}")
    lines.append(f"TaskManager: {payload['task_manager']}")
    lines.append(f"Ledger: {payload['ledger']}")
    return "\n".join(lines)


def _format_decision_log_payload(payload: dict[str, Any]) -> str:
    records = payload.get("records", [])
    lines = [
        "WABI SABI DECISION LOG",
        f"Registros: {len(records)}",
        f"TaskManager: {payload['task_manager']}",
        f"Ledger: {payload['ledger']}",
        "",
        "ULTIMOS:",
    ]
    for record in records[-5:]:
        lines.append(f"- {record.get('generated_at_utc')}: {record.get('recommended_mode')} {record.get('record_hash')}")
    if not records:
        lines.append("- Sin registros.")
    return "\n".join(lines)


def _format_comms_append_plan_payload(payload: dict[str, Any]) -> str:
    plan = payload["plan"]
    message = plan["message"]
    lines = [
        "WABI SABI COMMS APPEND PLAN",
        f"Gate: {message['action_gate']}  Append: {'OK' if plan['append_allowed'] else 'BLOCK'}",
        f"Target: {plan['target_outbox']}",
        f"Performed: {plan['append_performed']}",
        "",
        "EVIDENCIA:",
    ]
    lines.extend(f"- {item}" for item in message["observation_envelope"].get("evidence", []))
    lines.append("")
    lines.append(f"Artefacto: {payload['artifact']}")
    return "\n".join(lines)


def _format_programmer_workpack_payload(payload: dict[str, Any]) -> str:
    workpack = payload["workpack"]
    lines = [
        "WABI SABI PROGRAMMER WORKPACK",
        f"Modo: {workpack['mode']}  Workpack: {workpack['workpack_gate']}  Apply: {workpack['application_gate']}",
        f"Hash: {workpack['workpack_hash']}",
        "",
        "BLOQUEADO AHORA:",
    ]
    lines.extend(f"- {item}" for item in workpack.get("blocked_now", []))
    lines.append("")
    lines.append(f"Artefacto: {payload['artifact']}")
    return "\n".join(lines)


def _format_multimodal_payload(payload: dict[str, Any]) -> str:
    lines = [
        "WABI SABI MULTIMODAL",
        f"Accion: {payload.get('action')}  Gate: {payload.get('gate', 'REVIEW')}  OK: {payload.get('ok')}",
        f"Modo: {payload.get('mode', 'LOCAL_OPEN_SOURCE')}",
        "",
        "PRIVACIDAD:",
        f"- raw_image_included={payload.get('raw_image_included', False)}",
        f"- raw_audio_included={payload.get('raw_audio_included', False)}",
        f"- raw_media_saved={payload.get('raw_media_saved', False)}",
        f"- cloud_provider_called={payload.get('cloud_provider_called', False)}",
    ]
    if payload.get("reason"):
        lines.extend(["", "RAZON:", f"- {payload['reason']}"])
    if payload.get("devices"):
        devices = payload["devices"]
        lines.extend(
            [
                "",
                "DISPOSITIVOS:",
                f"- camera_present={devices.get('camera_present', False)}",
                f"- microphone_present={devices.get('microphone_present', False)}",
            ]
        )
    if payload.get("libraries"):
        available = [name for name, ok in payload["libraries"].items() if ok]
        missing = [name for name, ok in payload["libraries"].items() if not ok]
        lines.extend(["", "LIBRERIAS:", f"- disponibles: {', '.join(available) or 'ninguna'}"])
        if missing:
            lines.append(f"- faltantes: {', '.join(missing)}")
    if payload.get("decision"):
        decision = payload["decision"]
        lines.extend(
            [
                "",
                "WORLD MODEL:",
                f"- gate={decision.get('gate')} regime={decision.get('regime')}",
                f"- R={decision.get('r_world')} Phi_eff={decision.get('phi_eff_world')}",
            ]
        )
    if payload.get("fusion"):
        fusion = payload["fusion"]
        lines.extend(
            [
                "",
                "FUSION:",
                f"- gate={fusion.get('fusion_gate')} channels={fusion.get('channel_count')}",
                f"- R={fusion.get('fusion_R')} Phi_eff={fusion.get('fusion_Phi_eff')}",
            ]
        )
    if payload.get("evidence"):
        lines.extend(["", "EVIDENCIA:"])
        lines.extend(f"- {item}" for item in payload["evidence"])
    if payload.get("artifact"):
        lines.extend(["", f"Artefacto: {payload['artifact']}"])
    if payload.get("witness_db"):
        lines.append(f"Witness: {payload['witness_db']} ({payload.get('witness_verify_reason')})")
    if payload.get("commands"):
        lines.extend(["", "COMANDOS:"])
        lines.extend(f"- {command}" for command in payload["commands"])
    return "\n".join(lines)


def _format_operator_panel_payload(payload: dict[str, Any]) -> str:
    provider = payload.get("provider", {})
    worktree = payload.get("worktree", {})
    task_spec = payload.get("task_spec", {})
    witness = payload.get("witness", {})
    safe_tests = payload.get("latest_safe_tests", {})
    safe_summary = safe_tests.get("summary", {}) if isinstance(safe_tests.get("summary"), dict) else {}
    lines = [
        "WABI SABI OPERATOR STATUS",
        f"Gate: {payload.get('gate')}  Resultado: {'OK' if payload.get('ok') else 'REVIEW'}",
        f"Provider: {provider.get('auto_provider')}  Orden: {', '.join(provider.get('provider_order', []))}",
        f"Modelo base: {provider.get('base_model') or 'no expuesto'}  Disponible: {provider.get('base_model_available')}",
        f"Worktree: {'dirty' if worktree.get('dirty') else 'clean'} status={worktree.get('status_count')}",
        f"Task spec: {task_spec.get('gate')} {'OK' if task_spec.get('ok') else task_spec.get('error', 'REVIEW')}",
        f"Witness: {witness.get('event_count')} eventos, {witness.get('verify_reason')}",
        (
            f"Safe tests: {safe_tests.get('status', 'not_run')} "
            f"passed={safe_summary.get('passed', 0)} failed={safe_summary.get('failed', 0)} "
            f"witness={safe_tests.get('witness_event_id', 0)}"
        ),
        "",
        "COMANDOS:",
    ]
    lines.extend(f"- {command}" for command in payload.get("commands", []))
    lines.append("")
    lines.append("TOOLS:")
    lines.extend(f"- {name}" for name in payload.get("tools", {}).get("names", []))
    return "\n".join(lines)


def _format_claim_contract_payload(payload: dict[str, Any]) -> str:
    if payload.get("error"):
        return f"WABI SABI CLAIM CONTRACT\nGate: {payload.get('gate', 'REVIEW')}\nError: {payload['error']}"
    lines = [
        "WABI SABI CLAIM CONTRACT",
        f"Gate: {payload.get('gate')}  Status: {payload.get('status')}",
        f"Claim level: {payload.get('claim_level')}",
        f"Evidence: {payload.get('evidence_count')}  Falsifiers: {payload.get('falsifier_count')}",
        f"Fingerprint: {payload.get('fingerprint')}",
        "",
        "RAZONES:",
    ]
    lines.extend(f"- {item}" for item in payload.get("reasons", []))
    if payload.get("required_actions"):
        lines.append("")
        lines.append("ACCIONES REQUERIDAS:")
        lines.extend(f"- {item}" for item in payload.get("required_actions", []))
    return "\n".join(lines)


def _format_claim_observation_payload(payload: dict[str, Any]) -> str:
    if payload.get("error"):
        return f"WABI SABI CLAIM OBSERVATION\nGate: {payload.get('gate', 'REVIEW')}\nError: {payload['error']}"
    classification = payload.get("classification", {})
    lines = [
        "WABI SABI CLAIM OBSERVATION",
        f"Gate: {classification.get('gate')}  Label: {classification.get('label')}",
        f"R_or: {classification.get('R_or')}  Phi_moi: {classification.get('phi_moi')}",
        "mode: proposal_only",
        "cloud_provider_called: false",
        "applied_to_sources: false",
        "publication_gate: BLOCK",
        "",
        "NEXT:",
        f"- {payload.get('next_safe_action')}",
    ]
    return "\n".join(lines)


def _format_claim_fixture_review_payload(payload: dict[str, Any]) -> str:
    if payload.get("error"):
        return f"WABI SABI CLAIM FIXTURE REVIEW\nStatus: {payload.get('status', 'REVIEW')}\nError: {payload['error']}"
    lines = [
        "WABI SABI CLAIM FIXTURE REVIEW",
        f"Status: {payload.get('status')}  Cases: {payload.get('case_count')}  Review: {payload.get('review_count')}",
        "mode: proposal_only",
        "cloud_provider_called: false",
        "applied_to_sources: false",
        "publication_gate: BLOCK",
    ]
    review_cases = [item for item in payload.get("results", []) if item.get("status") == "REVIEW"]
    if review_cases:
        lines.extend(["", "REVIEW CASES:"])
        lines.extend(f"- {item.get('id')}: {item.get('actual_label')} / {item.get('actual_gate')}" for item in review_cases[:12])
    return "\n".join(lines)


def _format_hypothesis_payload(payload: dict[str, Any]) -> str:
    if payload.get("error"):
        return f"WABI SABI HYPOTHESIS PACKET\nGate: {payload.get('gate', 'REVIEW')}\nError: {payload['error']}"
    packet = payload.get("hypothesis_packet", {})
    evaluation = payload.get("evaluation", {})
    lines = [
        "WABI SABI HYPOTHESIS PACKET",
        f"Gate: {evaluation.get('gate')}  Status: {evaluation.get('status')}",
        f"Hypothesis: {packet.get('hypothesis_id')}",
        f"Claim level: {packet.get('claim_level')}",
        f"Evidence: {evaluation.get('evidence_count')}/{evaluation.get('evidence_required_count')}  Falsifiers: {evaluation.get('falsifier_count')}",
        f"R_est: {evaluation.get('R_est')}  Phi_eff_est: {evaluation.get('Phi_eff_est')}",
        "cloud_provider_called: false",
        "applied_to_sources: false",
        "publication_gate: BLOCK",
        "",
        "FALSIFIERS:",
    ]
    lines.extend(f"- {item}" for item in packet.get("falsifiers", []))
    lines.append("")
    lines.append("REASONS:")
    lines.extend(f"- {item}" for item in evaluation.get("reasons", []))
    artifact = payload.get("artifact")
    if artifact:
        lines.append("")
        lines.append(f"Artifact: {artifact}")
    return "\n".join(lines)


def _format_project_scan_payload(payload: dict[str, Any]) -> str:
    lines = [
        "WABI SABI PROJECT SCAN",
        f"Workspace: {payload.get('workspace')}",
        f"Files sampled: {payload.get('files_sampled')}",
        f"Managers: {', '.join(payload.get('package_managers', [])) or 'none'}",
        f"Languages: {', '.join(payload.get('languages', [])) or 'unknown'}",
        "",
        "TEST COMMANDS:",
    ]
    commands = payload.get("test_commands", [])
    if commands:
        lines.extend(f"- {item['command']} ({item['source']})" for item in commands)
    else:
        lines.append("- none detected")
    boundaries = payload.get("repo_boundaries", {})
    lines.append("")
    lines.append(f"Git root: {boundaries.get('current_git_root') or 'none'}")
    if boundaries.get("nested_git_roots"):
        lines.append("Nested repos:")
        lines.extend(f"- {item}" for item in boundaries["nested_git_roots"])
    lines.append("")
    lines.append("Contenido de archivos: NO incluido")
    return "\n".join(lines)


def _format_test_plan_payload(payload: dict[str, Any]) -> str:
    lines = [
        "WABI SABI TEST PLAN",
        f"Workspace: {payload.get('workspace')}",
        "Auto execute: NO",
        "Auto apply: NO",
        "",
        "COMMANDS:",
    ]
    for item in payload.get("commands", []):
        lines.append(f"- {item['command']} [{item['gate']}] ({item['source']})")
    scan = payload.get("scan", {})
    lines.append("")
    lines.append(f"Managers: {', '.join(scan.get('package_managers', [])) or 'none'}")
    lines.append(f"Languages: {', '.join(scan.get('languages', [])) or 'unknown'}")
    return "\n".join(lines)


def _format_safe_test_run_payload(payload: dict[str, Any]) -> str:
    summary = payload.get("summary", {})
    lines = [
        "WABI SABI RUN SAFE TESTS",
        f"Gate: {payload.get('gate')}  Resultado: {'OK' if payload.get('ok') else 'REVIEW'}",
        f"Commands: {summary.get('command_count')}  Passed: {summary.get('passed')}  Failed: {summary.get('failed')}",
        f"Artifact: {payload.get('artifact')}",
        f"Witness: {payload.get('witness_event_id')} {'OK' if payload.get('witness_verified') else 'REVIEW'}",
    ]
    if summary.get("errors"):
        lines.append("ERRORES:")
        lines.extend(f"- {item}" for item in summary["errors"])
    return "\n".join(lines)


def _format_curator_assistant_payload(payload: dict[str, Any]) -> str:
    summary = payload.get("summary", {})
    cleanup = payload.get("cleanup_plan", {})
    lines = [
        "WABI SABI CURADOR ORDEN ASSISTANT",
        f"Gate: {payload.get('gate')}  Modo: {payload.get('mode')}  Resultado: {'OK' if payload.get('ok') else 'REVIEW'}",
        f"Candidates: {summary.get('candidate_count')}  Cleanup performed: {summary.get('safe_cleanup_performed')}",
        f"Review: {cleanup.get('review_required_count')}  Blocked: {cleanup.get('blocked_count')}",
        f"Artifact: {payload.get('artifact')}",
        f"Markdown: {payload.get('markdown_artifact')}",
        f"Witness: {payload.get('witness_event_id')} {'OK' if payload.get('witness_verified') else 'REVIEW'}",
        "",
        "REGLAS:",
    ]
    for rule in payload.get("teaching", {}).get("rules", [])[:7]:
        lines.append(f"- {rule['title']}: {rule['rule']}")
    lines.append("")
    lines.append("ACCIONES BLOQUEADAS:")
    lines.extend(f"- {item}" for item in cleanup.get("forbidden_now", []))
    return "\n".join(lines)


def _format_cerebro_index_payload(payload: dict[str, Any]) -> str:
    status = payload.get("artifact_status", {})
    summary = payload.get("source_summary", {})
    lines = [
        "WABI SABI CEREBRO INDEX",
        f"Resultado: {'OK' if payload.get('ok') else 'REVIEW'}  Accion: {payload.get('action')}",
        f"Fuentes inventariadas: {summary.get('source_count', 0)}",
        f"Docs existentes: {len(status.get('existing_docs', []))}/{len(status.get('required_docs', []))}",
        "",
        "CERTEZA:",
    ]
    lines.extend(f"- {item}" for item in payload.get("certainty", []))
    lines.append("")
    lines.append("INFERENCIA:")
    lines.extend(f"- {item}" for item in payload.get("inference", []))
    lines.append("")
    lines.append("INCOGNITA:")
    lines.extend(f"- {item}" for item in payload.get("unknown", []))
    lines.append("")
    lines.append("ARTEFACTOS:")
    if payload.get("artifacts"):
        lines.extend(f"- {item}" for item in payload["artifacts"])
    else:
        lines.append("- Dry-run: no se escribieron documentos.")
    return "\n".join(lines)


def _format_cerebro_line_audit_payload(payload: dict[str, Any]) -> str:
    summary = payload.get("summary", {})
    lines = [
        "WABI SABI CEREBRO LINE AUDIT",
        f"Resultado: {'OK' if payload.get('ok') else 'REVIEW'}  Accion: {payload.get('action')}",
        f"Files: {summary.get('file_count_total', 0)}  Text: {summary.get('text_file_count', 0)}  Lines: {summary.get('total_lines', 0)}",
        f"Signal lines: {summary.get('signal_line_count', 0)}  Code candidates: {summary.get('code_candidate_count', 0)}",
        f"Variants: {summary.get('variant_group_count', 0)}  Signal records: {summary.get('signal_records_written_in_payload', 0)}",
        "",
        "TOP SIGNALS:",
    ]
    top = summary.get("top_signals", {})
    if top:
        lines.extend(f"- {name}: {count}" for name, count in top.items())
    else:
        lines.append("- none")
    lines.append("")
    lines.append("CERTEZA:")
    lines.extend(f"- {item}" for item in payload.get("certainty", []))
    lines.append("")
    lines.append("INCOGNITA:")
    lines.extend(f"- {item}" for item in payload.get("unknown", []))
    lines.append("")
    lines.append("ARTEFACTOS:")
    if payload.get("artifacts"):
        lines.extend(f"- {item}" for item in payload["artifacts"])
    else:
        lines.append("- Dry-run: no se escribieron documentos.")
    return "\n".join(lines)


def _format_project_graph_payload(payload: dict[str, Any]) -> str:
    graph = payload.get("project_graph", {})
    summary = payload.get("summary", {})
    lines = [
        "WABI SABI PROJECT GRAPH",
        f"Resultado: {'OK' if payload.get('ok') else 'REVIEW'}",
        f"Atoms: {len(payload.get('technology_atoms', []))}  Nodes: {len(graph.get('nodes', []))}  Edges: {len(graph.get('edges', []))}",
        f"Files: {summary.get('file_count_total', 0)}  Lines: {summary.get('total_lines', 0)}",
        "",
        "NODES:",
    ]
    lines.extend(f"- {node['id']}: {node['kind']}" for node in graph.get("nodes", []))
    lines.append("")
    lines.append("TOP ATOMS:")
    for atom in payload.get("technology_atoms", [])[:12]:
        lines.append(f"- {atom['source_signal']}: {atom['count']} -> {atom['target']} [{atom['gate']}]")
    if not payload.get("technology_atoms"):
        lines.append("- none")
    lines.append("")
    lines.append("ARTEFACTOS:")
    if payload.get("artifacts"):
        lines.extend(f"- {item}" for item in payload["artifacts"])
    else:
        lines.append("- Dry-run: no se escribieron documentos.")
    return "\n".join(lines)


def _format_browser_gate_payload(payload: dict[str, Any]) -> str:
    policy = payload["policy"]
    evaluation = payload.get("evaluation")
    lines = [
        "WABI SABI BROWSER GATE",
        f"Modo: {policy['decision_context']['mode']}",
        "",
        "ALLOW:",
    ]
    lines.extend(f"- {item['scope']}: {item['gate']} ({item['reason']})" for item in policy.get("allow", []))
    lines.append("")
    lines.append("REVIEW:")
    lines.extend(f"- {item}" for item in policy.get("review", []))
    lines.append("")
    lines.append("BLOCK:")
    lines.extend(f"- {item}" for item in policy.get("block", []))
    if evaluation:
        lines.append("")
        lines.append("EVALUATION:")
        lines.append(f"- URL: {evaluation['url']}")
        lines.append(f"- Gate: {evaluation['gate']}")
        lines.extend(f"- {reason}" for reason in evaluation.get("reasons", []))
    return "\n".join(lines)


def _format_browser_bridge_payload(payload: dict[str, Any]) -> str:
    lines = [
        "WABI SABI BROWSER BRIDGE",
        f"Accion: {payload.get('action')}",
        f"Resultado: {'OK' if payload.get('ok') else payload.get('gate', 'REVIEW')}",
    ]
    if payload.get("error"):
        lines.append(f"Error: {payload.get('error')}")
    if payload.get("schema") == "wabi.browser_bridge_status.v0_1":
        lines.extend(
            [
                f"Bridge enabled: {payload.get('bridge_enabled')}",
                f"Send enabled: {payload.get('send_enabled')}",
                "BACKENDS:",
            ]
        )
        for backend in payload.get("backends", []):
            lines.append(
                "- {backend}: configured={configured} enabled={enabled} available={available}".format(**backend)
            )
        return "\n".join(lines)
    if payload.get("url"):
        lines.append(f"URL: {payload.get('url')}")
    if payload.get("service"):
        lines.append(f"Servicio: {payload.get('service')}")
    if payload.get("gate"):
        lines.append(f"Gate: {payload.get('gate')}")
    if payload.get("reasons"):
        lines.append("RAZONES:")
        lines.extend(f"- {reason}" for reason in payload.get("reasons", []))
    observation = payload.get("observation") or {}
    if observation:
        lines.append("OBSERVACION:")
        lines.append(f"- Titulo: {observation.get('title')}")
        lines.append(f"- Hash texto: {observation.get('visible_text_sha256')}")
    if payload.get("artifact"):
        lines.append("ARTEFACTO:")
        lines.append(f"- {payload.get('artifact')}")
    lines.append("LLAMADAS:")
    lines.append(f"- browser_backend_called={payload.get('browser_backend_called', False)}")
    lines.append(f"- online_ai_called={payload.get('online_ai_called', False)}")
    return "\n".join(lines)


def _format_velo_payload(payload: dict[str, Any]) -> str:
    lines = [
        "WABI SABI VELO (puente de navegador)",
        f"Accion: {payload.get('action')}",
        f"Resultado: {'OK' if payload.get('ok') else payload.get('gate', 'REVIEW')}",
    ]
    if payload.get("action") == "velo_status":
        lines.extend(
            [
                f"Playwright: {'OK' if payload.get('playwright_importable') else 'NO'}",
                f"Chromium: {'OK' if payload.get('chromium_ready') else 'NO'} ({payload.get('chromium_detail')})",
                f"Perfil: {payload.get('profile_dir')} (existe={payload.get('profile_exists')})",
                f"Sitios: {', '.join(payload.get('sites', []))}",
            ]
        )
        if payload.get("next_step"):
            lines.append(f"Siguiente paso: {payload.get('next_step')}")
        return "\n".join(lines)
    if payload.get("site"):
        lines.append(f"Sitio: {payload.get('site')}")
    if payload.get("velo_status"):
        lines.append(f"Estado velo: {payload.get('velo_status')}")
    if payload.get("error"):
        lines.append(f"Error: {payload.get('error')}")
    if payload.get("reasons"):
        lines.append("RAZONES:")
        lines.extend(f"- {reason}" for reason in payload.get("reasons", []))
    if payload.get("url"):
        lines.append(f"URL del puente: {payload.get('url')}")
    if payload.get("elapsed_seconds") is not None and payload.get("action") == "velo_ask":
        lines.append(f"Tiempo: {payload.get('elapsed_seconds')}s")
    output = str(payload.get("output", "")).strip()
    if output:
        lines.append("RESPUESTA (propuesta, requiere revalidacion local):")
        preview = output if len(output) <= 1200 else output[:1200] + "\n[...]"
        lines.append(preview)
    if payload.get("next_step"):
        lines.append(f"Siguiente paso: {payload.get('next_step')}")
    if payload.get("artifact"):
        lines.append(f"Artefacto: {payload.get('artifact')}")
    return "\n".join(lines)


def _format_functional_status_payload(payload: dict[str, Any]) -> str:
    lines = [
        "WABI SABI FUNCTIONAL STATUS",
        f"Status: {payload.get('status')}",
        f"CEREBRO audit: {payload.get('cerebro_line_audit', {}).get('status')}",
        f"Agents can program: {payload.get('agents_can_program', {}).get('status')}",
        f"Local engine: {payload.get('local_engine', {}).get('status')} ({payload.get('local_engine', {}).get('module_count', 0)} modules)",
        f"Browser: {payload.get('browser', {}).get('status')}",
        f"DUAT/GEODIA OS: {payload.get('duat_geodia_os', {}).get('status')}",
        "",
        "BLOCKERS:",
    ]
    blockers = payload.get("blockers", [])
    lines.extend(f"- {item}" for item in blockers) if blockers else lines.append("- none")
    lines.append("")
    lines.append("NOT CLAIMED:")
    lines.extend(f"- {item}" for item in payload.get("not_claimed", []))
    if payload.get("artifact"):
        lines.append("")
        lines.append(f"Artefacto: {payload['artifact']}")
    return "\n".join(lines)


def _format_curator_fichas_payload(payload: dict[str, Any]) -> str:
    summary = payload.get("summary", {})
    lines = [
        "WABI SABI CURADOR FICHAS",
        f"Gate: {payload.get('gate')}  Modo: {payload.get('mode')}  Resultado: {'OK' if payload.get('ok') else 'REVIEW'}",
        f"Fichas: {summary.get('ficha_count')}  Delete approved: {summary.get('delete_approved_count')}",
        f"Artifact: {payload.get('artifact')}",
        f"Markdown: {payload.get('markdown_artifact')}",
        f"Workspace doc: {payload.get('workspace_doc') or 'none'}",
        f"Witness: {payload.get('witness_event_id')} {'OK' if payload.get('witness_verified') else 'REVIEW'}",
        "",
        "FICHAS:",
    ]
    for ficha in payload.get("fichas", [])[:12]:
        lines.append(f"- {ficha['ficha_id']}: {ficha['source_path']} [{ficha['decision']}/{ficha['action_gate']}]")
    if not payload.get("fichas"):
        lines.append("- Sin fichas nuevas.")
    lines.append("")
    lines.append("SIGUIENTES ACCIONES:")
    lines.extend(f"- {item}" for item in payload.get("next_safe_actions", []))
    return "\n".join(lines)


def _execute_patch_plan_command(
    config: RuntimeConfig,
    items: list[str],
    *,
    target: str | None,
    apply_patch: bool,
    test_commands: list[str] | None = None,
) -> dict[str, Any]:
    prompt = " ".join(items).strip() or "crea una funcion que lea un archivo y resuma sus lineas"
    if not target:
        return {
            "ok": False,
            "action": "patch_apply" if apply_patch else "patch_plan",
            "error": "missing_target",
            "unknown": ["Se requiere --target con una ruta .py dentro del workspace."],
        }
    try:
        target_path = resolve_python_target(config.workspace, target)
        old_text = target_path.read_text(encoding="utf-8") if target_path.exists() else ""
        code, output, inference = code_for_prompt(prompt)
        new_text = build_new_python_text(old_text, code)
        plan = build_file_patch_plan(
            workspace=config.workspace,
            target=target,
            content=new_text,
            summary=prompt,
            suffix=".py",
            test_commands=test_commands,
        )
        plan_artifact = write_patch_plan(config.output_dir, plan)
        diff_artifact = write_patch_diff(config.output_dir, plan)
        payload: dict[str, Any] = {
            "ok": True,
            "action": "patch_apply" if apply_patch else "patch_plan",
            "target": str(target_path),
            "changed": plan.changed,
            "plan_id": plan.plan_id,
            "plan_artifact": str(plan_artifact),
            "diff_artifact": str(diff_artifact),
            "output": output,
            "inference": inference,
            "gate": plan.gate,
            "reasons": plan.reasons,
            "test_commands": plan.test_commands,
        }
        if apply_patch:
            execution = SafeExecutor(workspace=config.workspace, runtime_root=config.runtime_root).execute(plan)
            payload.update(
                {
                    "ok": execution.ok,
                    "execution_artifact": str(execution.execution_path),
                    "rollback_artifact": str(execution.rollback_path),
                    "written": execution.written,
                    "test_results": execution.test_results,
                    "witness_event_id": execution.witness_event_id,
                    "witness_verified": execution.witness_verified,
                    "witness_db": execution.witness_db,
                    "observation": execution.observation,
                    "verification": execution.verification,
                    "error": execution.error,
                }
            )
        return payload
    except Exception as exc:
        return {
            "ok": False,
            "action": "patch_apply" if apply_patch else "patch_plan",
            "error": str(exc),
        }


def _execute_engine_status_command() -> dict[str, Any]:
    return {
        "ok": True,
        "action": "engine_status",
        "manifest": default_engine_manifest(),
    }


def _execute_engine_intake_command(items: list[str]) -> dict[str, Any]:
    source = " ".join(items).strip() or "GDevelop"
    try:
        source_card = build_source_card(source)
        return {
            "ok": source_card.get("action_gate") != "BLOCK",
            "action": "engine_intake",
            "clean_room": True,
            "source_card": source_card,
        }
    except Exception as exc:
        return {
            "ok": False,
            "action": "engine_intake",
            "error": str(exc),
        }


def _execute_engine_plan_command(
    config: RuntimeConfig,
    items: list[str],
    *,
    write_docs: bool = False,
) -> dict[str, Any]:
    goal = " ".join(items).strip()
    if not goal:
        return {
            "ok": False,
            "action": "engine_plan",
            "error": "missing_engine_goal",
        }
    try:
        plan = build_engine_plan(goal)
        payload = {
            "ok": plan["action_gate"] != "BLOCK",
            "action": "engine_plan",
            "plan": plan,
        }
        if write_docs and payload["ok"]:
            artifact = _write_engine_json_artifact(
                config.output_dir,
                "engine_plans",
                f"{plan['project_name']}_ENGINE_PLAN.json",
                plan,
            )
            payload["artifact"] = str(artifact)
        return payload
    except Exception as exc:
        return {
            "ok": False,
            "action": "engine_plan",
            "error": str(exc),
        }


def _execute_engine_task_spec_command(
    config: RuntimeConfig,
    items: list[str],
    *,
    target: str | None,
    write_docs: bool = False,
) -> dict[str, Any]:
    plan_ref = " ".join(items).strip()
    if not plan_ref:
        return {
            "ok": False,
            "action": "engine_task_spec",
            "error": "missing_engine_plan_path",
        }
    try:
        plan = load_engine_plan(config.workspace, plan_ref)
        task_spec = engine_plan_to_task_spec(plan, target=target)
        change = task_spec["changes"][0]
        payload = {
            "ok": True,
            "action": "engine_task_spec",
            "plan_project": plan["project_name"],
            "target": change["target"],
            "task_spec": task_spec,
            "metadata": task_spec.get("metadata", {}),
        }
        if write_docs:
            artifact = _write_engine_task_spec_artifact(
                config.workspace,
                change["target"],
                plan["project_name"],
                task_spec,
            )
            payload["artifact"] = str(artifact)
        return payload
    except Exception as exc:
        return {
            "ok": False,
            "action": "engine_task_spec",
            "error": str(exc),
        }


def _execute_engine_sandbox_command(
    config: RuntimeConfig,
    items: list[str],
    *,
    write_docs: bool = False,
) -> dict[str, Any]:
    project_name = "_".join(item.strip() for item in items if item.strip()) or "wabi_sabi_observatorio_sandbox"
    try:
        project = build_observatorio_sandbox_project(project_name=project_name)
        validation = validate_engine_project_spec(project)
        payload: dict[str, Any] = {
            "ok": validation["ok"],
            "action": "engine_sandbox",
            "project": project,
            "validation": validation,
        }
        if write_docs and validation["ok"]:
            artifact = write_engine_project_spec(config.workspace, project)
            payload["artifact"] = str(artifact)
        return payload
    except Exception as exc:
        return {
            "ok": False,
            "action": "engine_sandbox",
            "error": str(exc),
        }


def _execute_engine_project_validate_command(config: RuntimeConfig, items: list[str]) -> dict[str, Any]:
    spec_ref = " ".join(items).strip()
    if not spec_ref:
        return {
            "ok": False,
            "action": "engine_project_validate",
            "error": "missing_engine_project_spec_path",
        }
    try:
        project = load_engine_project_spec(config.workspace, spec_ref)
        validation = validate_engine_project_spec(project)
        return {
            "ok": validation["ok"],
            "action": "engine_project_validate",
            "spec_path": spec_ref,
            "validation": validation,
        }
    except Exception as exc:
        return {
            "ok": False,
            "action": "engine_project_validate",
            "error": str(exc),
        }


def _execute_engine_simulate_command(config: RuntimeConfig, items: list[str]) -> dict[str, Any]:
    if not items:
        return {
            "ok": False,
            "action": "engine_simulate",
            "error": "missing_engine_project_spec_path",
        }
    spec_ref = items[0]
    click_count = 3
    if len(items) > 1:
        try:
            click_count = int(items[1])
        except ValueError:
            return {
                "ok": False,
                "action": "engine_simulate",
                "error": "click_count_must_be_integer",
            }
    try:
        project = load_engine_project_spec(config.workspace, spec_ref)
        events = observatorio_click_events(click_count)
        simulation = simulate_engine_project(project, events)
        return {
            "ok": True,
            "action": "engine_simulate",
            "spec_path": spec_ref,
            "events": events,
            "simulation": simulation,
        }
    except Exception as exc:
        return {
            "ok": False,
            "action": "engine_simulate",
            "error": str(exc),
        }


def _write_engine_json_artifact(output_dir: Path, folder: str, filename: str, payload: dict[str, Any]) -> Path:
    safe_name = "".join(ch if ch.isalnum() or ch in {"-", "_", "."} else "_" for ch in filename)
    artifact_dir = output_dir / folder
    artifact_dir.mkdir(parents=True, exist_ok=True)
    artifact = artifact_dir / safe_name
    artifact.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    return artifact


def _write_engine_task_spec_artifact(
    workspace: Path,
    target: str,
    project_name: str,
    payload: dict[str, Any],
) -> Path:
    workspace = workspace.resolve()
    target_path = (workspace / target).resolve()
    try:
        target_path.relative_to(workspace)
    except ValueError as exc:
        raise ValueError("engine_task_spec_artifact_outside_workspace") from exc
    safe_project = "".join(ch if ch.isalnum() or ch in {"-", "_"} else "_" for ch in project_name)
    artifact_dir = target_path.parent
    artifact_dir.mkdir(parents=True, exist_ok=True)
    artifact = artifact_dir / f"{safe_project}_TASK_SPEC.json"
    artifact.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    return artifact


def _execute_task_spec_command(config: RuntimeConfig, items: list[str], *, apply_patch: bool) -> dict[str, Any]:
    spec_ref = " ".join(items).strip()
    if not spec_ref:
        return {
            "ok": False,
            "action": "task_spec_apply" if apply_patch else "task_spec_plan",
            "error": "missing_task_spec_path",
        }
    try:
        spec, plan = build_patch_plan_from_task_spec(
            workspace=config.workspace,
            spec_path=spec_ref,
            input_roots=[config.runtime_root],
        )
        plan_artifact = write_patch_plan(config.output_dir, plan)
        diff_artifact = write_patch_diff(config.output_dir, plan)
        payload: dict[str, Any] = {
            "ok": True,
            "action": "task_spec_apply" if apply_patch else "task_spec_plan",
            "spec_path": str(spec.path),
            "spec": spec.to_dict(),
            "plan_id": plan.plan_id,
            "changed": plan.changed,
            "operations": [operation.relative_path for operation in plan.operations],
            "plan_artifact": str(plan_artifact),
            "diff_artifact": str(diff_artifact),
            "gate": plan.gate,
            "reasons": plan.reasons,
            "test_commands": plan.test_commands,
        }
        if apply_patch:
            execution = SafeExecutor(workspace=config.workspace, runtime_root=config.runtime_root).execute(plan)
            payload.update(
                {
                    "ok": execution.ok,
                    "execution_artifact": str(execution.execution_path),
                    "rollback_artifact": str(execution.rollback_path),
                    "written": execution.written,
                    "test_results": execution.test_results,
                    "witness_event_id": execution.witness_event_id,
                    "witness_verified": execution.witness_verified,
                    "witness_db": execution.witness_db,
                    "observation": execution.observation,
                    "verification": execution.verification,
                    "error": execution.error,
                }
            )
        return payload
    except Exception as exc:
        return {
            "ok": False,
            "action": "task_spec_apply" if apply_patch else "task_spec_plan",
            "error": str(exc),
        }


def _conversation_cloud_allowed(args: argparse.Namespace) -> bool:
    return bool(getattr(args, "cloud", False) and not getattr(args, "no_cloud", False))


def _execute_browser_bridge_command(
    config: RuntimeConfig,
    items: list[str],
    *,
    backend: str,
    send_requested: bool = False,
    service: str | None = None,
    payload_class: str = PUBLIC_PROMPT,
    input_path: str | None = None,
    snapshot_url: str = "http://127.0.0.1:8787/",
) -> dict[str, Any]:
    subcommand = items[0].lower() if items else "status"
    if subcommand in {"status", "estado", "backends", "diagnostic", "diagnostico"}:
        return {
            "ok": True,
            "action": "browser_bridge_status",
            "gate": "APPROVE",
            **build_browser_bridge_status(),
        }
    if subcommand in {"select", "selector", "seleccionar"}:
        selected_service = service or (items[1] if len(items) > 1 else "dry-run")
        return {
            "ok": True,
            "action": "browser_bridge_select",
            "gate": "APPROVE",
            "selector_pack": rank_browser_council_services(payload_class=payload_class, send_requested=send_requested),
            "decision": select_browser_bridge_backend(
                service_id=selected_service,
                payload_class=payload_class,
                requested_backend=backend if backend != "dry-run" else "",
                send_requested=send_requested,
            ),
            "browser_backend_called": False,
            "online_ai_called": False,
            "publication_gate": "BLOCK",
        }
    if subcommand in {"smoke", "smoke-kimi", "kimi-smoke"}:
        selected_service = service or (items[1] if len(items) > 1 else "kimi")
        if selected_service.strip().lower() != "kimi":
            return {
                "ok": False,
                "action": "browser_bridge_smoke",
                "gate": "REVIEW",
                "status": "SMOKE_NOT_IMPLEMENTED_FOR_SERVICE",
                "service": selected_service,
                "browser_backend_called": False,
                "online_ai_called": False,
            }
        return run_kimi_smoke(
            runtime_root=config.runtime_root,
            send_requested=send_requested,
        )
    if subcommand in {"snapshot", "readonly-snapshot", "read-only-snapshot"}:
        return run_devtools_readonly_snapshot(
            runtime_root=config.runtime_root,
            url=snapshot_url,
        )
    if subcommand in {"proposal-from-response", "response-to-proposal", "proposal"}:
        source_input = input_path or (items[1] if len(items) > 1 else "")
        if not source_input:
            return {
                "ok": False,
                "action": "browser_response_to_proposal",
                "gate": "REVIEW",
                "error": "response_input_required",
                "browser_backend_called": False,
                "online_ai_called": False,
            }
        return convert_browser_response_to_proposal(
            workspace=config.workspace,
            runtime_root=config.runtime_root,
            input_path=source_input,
        )
    if subcommand in {"observe", "observa", "open", "navigate", "snapshot", "screenshot", "extract", "read"}:
        url = " ".join(items[1:]).strip()
        if not url:
            return {
                "ok": False,
                "action": "browser_bridge_observe",
                "gate": "REVIEW",
                "error": "browser_url_required",
                "browser_backend_called": False,
                "online_ai_called": False,
            }
        return observe_browser_url(
            workspace=config.workspace,
            runtime_root=config.runtime_root,
            url=url,
            action=subcommand,
            backend=backend,
            intent=f"browser bridge {subcommand}",
        )
    if subcommand in {"ai-consult", "consult-ai", "ia-consulta", "consultar-ia"}:
        service = items[1] if len(items) > 1 else "kimi"
        prompt = " ".join(items[2:]).strip()
        if not prompt:
            return {
                "ok": False,
                "action": "browser_ai_consultation_request",
                "service": service,
                "gate": "REVIEW",
                "error": "consultation_prompt_required",
                "browser_backend_called": False,
                "online_ai_called": False,
            }
        return prepare_browser_ai_consultation(
            workspace=config.workspace,
            runtime_root=config.runtime_root,
            service=service,
            prompt=prompt,
            backend=backend,
            send_requested=send_requested,
        )
    if subcommand in {"council", "concilio", "ai-council", "consejo"}:
        prompt = " ".join(items[1:]).strip() or "Rank BrowserBridge services for a public synthetic task."
        return prepare_browser_council(
            workspace=config.workspace,
            runtime_root=config.runtime_root,
            prompt=prompt,
            backend=backend,
            send_requested=send_requested,
        )
    return {
        "ok": False,
        "action": "browser_bridge_unknown_subcommand",
        "gate": "REVIEW",
        "error": f"unknown_browser_bridge_subcommand:{subcommand}",
        "supported": [
            "status",
            "select --service kimi",
            "observe <url>",
            "smoke --service kimi",
            "snapshot --backend chrome-devtools-mcp",
            "ai-consult <service> <prompt>",
            "council [prompt]",
            "proposal-from-response --input <file>",
        ],
        "browser_backend_called": False,
        "online_ai_called": False,
    }


def _execute_velo_command(
    config: RuntimeConfig,
    items: list[str],
    *,
    service: str | None = None,
    host: str = "127.0.0.1",
    port: int = 8777,
    headless: bool = False,
    answer_timeout: float = 120.0,
) -> dict[str, Any]:
    """Dispatch `wabi velo <subcommand>` for the browser-velo (Option C)."""

    subcommand = items[0].lower() if items else "status"
    headless_flag = True if headless else None
    if subcommand in {"status", "estado", "diagnostic", "diagnostico"}:
        return velo_status(config.runtime_root)
    if subcommand in {"login", "signin", "sign-in", "iniciar-sesion"}:
        target = service or (items[1] if len(items) > 1 else None)
        return velo_login(runtime_root=config.runtime_root, service=target)
    if subcommand in {"ask", "pregunta", "consulta", "consultar"}:
        target = service or (items[1] if len(items) > 1 else None)
        offset = 1 if (service or len(items) <= 1) else 2
        prompt = " ".join(items[offset:]).strip()
        if not prompt:
            return {
                "ok": False,
                "action": "velo_ask",
                "gate": "REVIEW",
                "error": "velo_prompt_required",
                "online_ai_called": False,
            }
        return velo_ask(
            runtime_root=config.runtime_root,
            service=target,
            prompt=prompt,
            headless=headless_flag,
            answer_timeout=answer_timeout,
        )
    if subcommand in {"serve", "server", "servir", "bridge", "puente"}:
        return velo_serve(
            runtime_root=config.runtime_root,
            host=host,
            port=port,
            default_site=service or "chatgpt",
            headless=headless_flag,
            answer_timeout=answer_timeout,
        )
    if subcommand in {"reset", "reset-profile", "limpiar", "olvidar"}:
        return velo_reset_profile(config.runtime_root)
    return {
        "ok": False,
        "action": "velo_unknown_subcommand",
        "gate": "REVIEW",
        "error": f"unknown_velo_subcommand:{subcommand}",
        "supported": [
            "status",
            "login <site>",
            "ask <site> <prompt>",
            "serve [--velo-port N] [--service <site>]",
            "reset",
        ],
        "online_ai_called": False,
    }


def _execute_cloud_proposal_from_provider_command(
    config: RuntimeConfig,
    items: list[str],
    *,
    mode: str,
    provider: str,
    timeout: int,
    dry_run: bool,
) -> dict[str, Any]:
    intent = " ".join(items).strip()
    action = f"cloud_proposal_from_provider_{mode}"
    if not intent:
        return {
            "ok": False,
            "action": action,
            "error": "missing_cloud_proposal_intent",
        }
    try:
        if dry_run:
            proposal = build_dry_run_cloud_code_proposal(intent=intent)
            proposal_artifact = write_cloud_proposal_artifact(config.output_dir, proposal, source="dry_run")
            generated = _execute_cloud_proposal_command(config, [str(proposal_artifact)], mode=mode)
            generated.update(
                {
                    "action": action,
                    "intent": redact_text(intent),
                    "provider": "dry-run",
                    "provider_requested": provider,
                    "proposal_artifact": str(proposal_artifact),
                    "cloud_provider_called": False,
                    "provider_prompt_artifact": "",
                    "provider_response_artifact": "",
                    "provider_result": {
                        "ok": True,
                        "provider": "dry-run",
                        "action": "local_fixture",
                    },
                }
            )
            return generated

        workspace_summary = scan_project(workspace=config.workspace, max_depth=2, max_files=200)
        prompt = build_cloud_code_proposal_prompt(intent=intent, workspace_summary=workspace_summary)
        prompt_artifact = write_artifact(config.output_dir / "cloud_prompts", "wabi_cloud_code_proposal_prompt", ".md", prompt)
        orchestrator = ProviderOrchestrator(workspace=config.workspace, runtime_root=config.runtime_root)
        result = orchestrator.ask(prompt, provider=provider, timeout=timeout)
        response_artifact = write_artifact(
            config.output_dir / "cloud_provider_outputs",
            "wabi_cloud_code_provider_response",
            ".md",
            redact_text(result.output) + "\n",
        )
        provider_called = _cloud_network_called(result.attempts)
        base_payload: dict[str, Any] = {
            "action": action,
            "intent": redact_text(intent),
            "provider": result.provider,
            "provider_requested": provider,
            "provider_prompt_artifact": str(prompt_artifact),
            "provider_response_artifact": str(response_artifact),
            "cloud_provider_called": provider_called,
            "provider_result": {
                "ok": result.ok,
                "provider": result.provider,
                "action": result.action,
                "error": result.error,
                "attempts": result.attempts,
            },
        }
        if not result.ok:
            base_payload.update(
                {
                    "ok": False,
                    "error": result.error or "provider_failed",
                    "cloud_authority": "proposal_only",
                }
            )
            return base_payload
        try:
            proposal = extract_cloud_code_proposal_payload(result.output)
        except Exception as exc:
            base_payload.update(
                {
                    "ok": False,
                    "error": str(exc),
                    "cloud_authority": "proposal_only",
                }
            )
            return base_payload
        proposal_artifact = write_cloud_proposal_artifact(config.output_dir, proposal, source=result.provider)
        generated = _execute_cloud_proposal_command(config, [str(proposal_artifact)], mode=mode)
        generated.update(base_payload)
        generated["proposal_artifact"] = str(proposal_artifact)
        return generated
    except Exception as exc:
        return {
            "ok": False,
            "action": action,
            "intent": redact_text(intent),
            "provider": provider,
            "cloud_provider_called": False,
            "error": str(exc),
        }


def _execute_build_assist_plan_command(
    config: RuntimeConfig,
    items: list[str],
    *,
    provider: str,
    timeout: int,
    dry_run: bool,
) -> dict[str, Any]:
    intent = " ".join(items).strip()
    if not intent:
        return {
            "schema": "wabi.build_assist_plan.v0_1",
            "ok": False,
            "action": "build_assist_plan",
            "error": "missing_build_assist_intent",
            "cloud_provider_called": False,
            "cloud_authority": "proposal_only",
        }
    status = build_build_assist_cloud_status(workspace=config.workspace, runtime_root=config.runtime_root)
    budget = build_assist_budget_status(runtime_root=config.runtime_root)
    live_ready = bool(status.get("cloud_live_ready"))
    forced_dry_run = bool(not dry_run and not live_ready)
    effective_dry_run = bool(dry_run or forced_dry_run)
    selected_provider = provider if provider != "auto" else build_assist_default_model_alias()
    cloud_budget_gate = CloudBudgetGate(runtime_root=config.runtime_root)
    cloud_budget_decision = cloud_budget_gate.can_call("nvidia", selected_provider, "build_assist_plan")

    if not dry_run and cloud_budget_decision.get("budget_gate") == "CLOUD_BUDGET_EXCEEDED":
        cloud_budget_gate.record_blocked_call("nvidia", selected_provider, "build_assist_plan", status="CLOUD_BUDGET_EXCEEDED")
        return {
            "schema": "wabi.build_assist_plan.v0_1",
            "ok": False,
            "action": "build_assist_plan",
            "error": "CLOUD_BUDGET_EXCEEDED",
            "provider": selected_provider,
            "cloud_provider_called": False,
            "cloud_authority": "proposal_only",
            "build_assist": status,
            "cloud_budget": cloud_budget_decision,
        }

    if not effective_dry_run and (budget["remaining_cloud_calls"] <= 0 or not cloud_budget_decision.get("next_cloud_call_allowed")):
        blocked_status = "CLOUD_BUDGET_EXCEEDED" if budget["remaining_cloud_calls"] > 0 else "BLOCK_BUDGET_EXHAUSTED"
        cloud_budget_gate.record_blocked_call("nvidia", selected_provider, "build_assist_plan", status=blocked_status)
        return {
            "schema": "wabi.build_assist_plan.v0_1",
            "ok": False,
            "action": "build_assist_plan",
            "error": blocked_status,
            "provider": selected_provider,
            "cloud_provider_called": False,
            "cloud_authority": "proposal_only",
            "build_assist": status,
            "cloud_budget": cloud_budget_decision,
        }

    if not effective_dry_run:
        cloud_budget_gate.record_planned_call("nvidia", selected_provider, "build_assist_plan")
    payload = _execute_cloud_proposal_from_provider_command(
        config,
        [intent],
        mode="plan",
        provider=selected_provider,
        timeout=timeout,
        dry_run=effective_dry_run,
    )
    if not effective_dry_run:
        cloud_budget_gate.record_completed_call(
            "nvidia",
            selected_provider,
            {
                "ok": payload.get("ok"),
                "status": "BUILD_ASSIST_PLAN_PROVIDER_CALLED" if payload.get("cloud_provider_called") else "BUILD_ASSIST_PLAN_PROVIDER_NOT_CALLED",
                "usage": payload.get("usage", {}),
                "cost_estimate": payload.get("cost_estimate"),
            },
        )
    if payload.get("cloud_provider_called") is True:
        usage_log = record_build_assist_usage(
            runtime_root=config.runtime_root,
            event={
                "action": "build_assist_plan",
                "provider": payload.get("provider", selected_provider),
                "provider_requested": selected_provider,
                "intent": redact_text(intent)[:500],
                "cloud_provider_called": True,
                "proposal_artifact": payload.get("proposal_artifact", ""),
            },
        )
        payload["build_assist_usage_log"] = str(usage_log)
    payload.update(
        {
            "schema": "wabi.build_assist_plan.v0_1",
            "action": "build_assist_plan",
            "build_assist_mode": "TEMPORARY_CLOUD_ASSIST_LOCAL_FIRST",
            "provider_requested": selected_provider,
            "dry_run_forced_by_gate": forced_dry_run,
            "cloud_authority": "proposal_only",
            "real_apply_allowed": False,
            "auto_apply_from_cloud": False,
            "build_assist": status,
            "cloud_budget": cloud_budget_gate.render_status("nvidia", selected_provider, "build_assist_plan"),
        }
    )
    return payload


def _execute_cloud_proposal_command(config: RuntimeConfig, items: list[str], *, mode: str) -> dict[str, Any]:
    proposal_ref = " ".join(items).strip()
    action = f"cloud_proposal_{mode}"
    if not proposal_ref:
        return {
            "ok": False,
            "action": action,
            "error": "missing_cloud_proposal_path",
        }
    try:
        validation = validate_cloud_code_proposal(
            workspace=config.workspace,
            proposal_path=proposal_ref,
            input_roots=[config.runtime_root],
        )
        payload: dict[str, Any] = {
            "ok": validation.ok,
            "action": action,
            "proposal_path": str(validation.path),
            "validation": validation.to_dict(),
            "cloud_provider_called": False,
            "cloud_authority": "proposal_only",
        }
        if mode == "validate" or not validation.ok:
            if not validation.ok:
                payload["error"] = ";".join(validation.errors)
            return payload
        task_spec = cloud_proposal_to_task_spec(validation)
        task_spec_artifact = write_cloud_task_spec_artifact(config.output_dir, task_spec)
        task_spec_summary = {
            "schema": task_spec.get("schema"),
            "summary": task_spec.get("summary"),
            "changes": [
                {
                    "target": change.get("target"),
                    "suffix": change.get("suffix"),
                }
                for change in task_spec.get("changes", [])
            ],
            "test_commands": task_spec.get("test_commands", []),
            "metadata": {
                "cloud_gate_recommendation": task_spec.get("metadata", {}).get("cloud_gate_recommendation"),
                "cloud_authority": task_spec.get("metadata", {}).get("cloud_authority"),
                "redacted_fields": task_spec.get("metadata", {}).get("redacted_fields", []),
            },
        }
        payload.update(
            {
                "task_spec": task_spec_summary,
                "task_spec_artifact": str(task_spec_artifact),
            }
        )
        if mode == "task_spec":
            return payload
        spec, plan = build_patch_plan_from_task_spec(
            workspace=config.workspace,
            spec_path=task_spec_artifact,
            input_roots=[config.runtime_root],
        )
        plan_artifact = write_patch_plan(config.output_dir, plan)
        diff_artifact = write_patch_diff(config.output_dir, plan)
        payload.update(
            {
                "spec": spec.to_dict(),
                "plan_id": plan.plan_id,
                "changed": plan.changed,
                "operations": [operation.relative_path for operation in plan.operations],
                "plan_artifact": str(plan_artifact),
                "diff_artifact": str(diff_artifact),
                "gate": plan.gate,
                "reasons": plan.reasons,
                "test_commands": plan.test_commands,
            }
        )
        return payload
    except Exception as exc:
        return {
            "ok": False,
            "action": action,
            "proposal_path": proposal_ref,
            "cloud_provider_called": False,
            "error": str(exc),
        }


def _cloud_network_called(attempts: list[dict[str, Any]]) -> bool:
    network_actions = {"cloud_chat_completion", "cloud_provider_error"}
    cloud_prefixes = ("nvidia", "qwen", "deepseek", "openrouter", "openai-compatible")
    for attempt in attempts:
        provider = str(attempt.get("provider", "")).lower()
        action = str(attempt.get("action", ""))
        if provider.startswith(cloud_prefixes) and action in network_actions:
            return True
    return False


def _format_engine_status_payload(payload: dict[str, Any]) -> str:
    manifest = payload.get("manifest", {})
    lines = [
        "WABI SABI MODULAR ENGINE",
        f"Resultado: {'OK' if payload.get('ok') else 'REVIEW'}",
        f"Schema: {manifest.get('schema')}",
        f"Postura: {manifest.get('posture')}",
        "MODULOS:",
    ]
    for name, module in manifest.get("modules", {}).items():
        lines.append(f"- {name}: {module.get('family')} ({', '.join(module.get('capabilities', [])[:2])})")
    lines.append("FRONTERAS:")
    lines.extend(f"- {item}" for item in manifest.get("hard_boundaries", []))
    return "\n".join(lines)


def _format_build_assist_payload(payload: dict[str, Any]) -> str:
    if payload.get("schema") == "wabi.build_assist_plan.v0_1":
        assist = payload.get("build_assist", {})
        cloud_budget = payload.get("cloud_budget") or assist.get("cloud_budget", {})
        lines = [
            "WABI BUILD ASSIST CLOUD",
            f"Resultado: {'OK' if payload.get('ok') else 'REVIEW'}",
            f"Provider: {payload.get('provider', payload.get('provider_requested', ''))}",
            f"Cloud called: {payload.get('cloud_provider_called', False)}",
            f"Dry-run forced: {payload.get('dry_run_forced_by_gate', False)}",
            f"Authority: {payload.get('cloud_authority', 'proposal_only')}",
            f"Gate: {assist.get('action_gate', 'REVIEW')}",
            f"CloudBudget: {cloud_budget.get('budget_gate', 'UNKNOWN')} "
            f"{cloud_budget.get('remaining_session_calls', '?')}/{cloud_budget.get('session_calls_limit', '?')} session, "
            f"{cloud_budget.get('remaining_daily_calls', '?')}/{cloud_budget.get('daily_calls_limit', '?')} day",
        ]
        if payload.get("proposal_artifact"):
            lines.append(f"Proposal: {payload['proposal_artifact']}")
        if payload.get("plan_artifact"):
            lines.append(f"Plan: {payload['plan_artifact']}")
        if payload.get("error"):
            lines.append(f"Error: {payload['error']}")
        return "\n".join(lines)

    nvidia = payload.get("nvidia", {})
    budget = payload.get("budget", {})
    cloud_budget = payload.get("cloud_budget", {})
    lines = [
        "WABI BUILD ASSIST CLOUD",
        f"Modo: {payload.get('mode')}",
        f"Enabled: {payload.get('enabled')}  Live ready: {payload.get('cloud_live_ready')}",
        f"Gate: {payload.get('action_gate')}",
        f"NVIDIA default: {nvidia.get('default_model_alias')} -> {nvidia.get('default_model')}",
        f"Budget: {budget.get('remaining_cloud_calls')}/{budget.get('max_cloud_calls')} cloud calls",
        f"CloudBudgetGate: {cloud_budget.get('budget_gate', 'UNKNOWN')} "
        f"{cloud_budget.get('remaining_session_calls', '?')}/{cloud_budget.get('session_calls_limit', '?')} session, "
        f"{cloud_budget.get('remaining_daily_calls', '?')}/{cloud_budget.get('daily_calls_limit', '?')} day",
        "Authority: cloud proposal-only; Wabi local validates/applies.",
        "",
        "COMANDOS:",
    ]
    lines.extend(f"- {command}" for command in payload.get("recommended_commands", []))
    return "\n".join(lines)


def _format_engine_intake_payload(payload: dict[str, Any]) -> str:
    lines = [
        "WABI SABI ENGINE INTAKE",
        f"Resultado: {'OK' if payload.get('ok') else 'REVIEW'}",
    ]
    if not payload.get("ok"):
        lines.append(f"Error: {payload.get('error', 'unknown')}")
        return "\n".join(lines)
    card = payload.get("source_card", {})
    lines.extend(
        [
            f"Fuente: {card.get('source_name')}",
            f"Tipo: {card.get('source_type')}",
            f"Repositorio: {card.get('repository')}",
            f"Extraccion: {card.get('extraction_style')}",
            f"Gate: {card.get('action_gate')}",
            "PATRONES:",
        ]
    )
    for pattern in card.get("patterns", [])[:6]:
        lines.append(f"- {pattern.get('name')}: {pattern.get('invariant')}")
    lines.append("BLOQUEADO:")
    lines.extend(f"- {item}" for item in card.get("blocked_use", [])[:6])
    return "\n".join(lines)


def _format_engine_plan_payload(payload: dict[str, Any]) -> str:
    lines = [
        "WABI SABI ENGINE PLAN",
        f"Resultado: {'OK' if payload.get('ok') else 'REVIEW'}",
    ]
    if not payload.get("ok"):
        lines.append(f"Error: {payload.get('error', 'unknown')}")
        return "\n".join(lines)
    plan = payload.get("plan", {})
    lines.extend(
        [
            f"Proyecto: {plan.get('project_name')}",
            f"Gate: {plan.get('action_gate')}",
            f"Postura: {plan.get('posture')}",
            f"Objetivo: {plan.get('goal')}",
            "MODULOS:",
        ]
    )
    for module in plan.get("modules", []):
        lines.append(f"- {module.get('name')}: {module.get('family')}")
    lines.append("FUENTES:")
    for card in plan.get("source_cards", []):
        lines.append(f"- {card.get('source_name')}: {card.get('extraction_style')} / {card.get('action_gate')}")
    if payload.get("artifact"):
        lines.append("ARTEFACTO:")
        lines.append(f"- {payload.get('artifact')}")
    lines.append("PROXIMO:")
    lines.append("- Guarda este JSON y usa engine-task-spec <plan.json> para convertirlo en wabi.task_spec.v1.")
    return "\n".join(lines)


def _format_engine_task_spec_payload(payload: dict[str, Any]) -> str:
    lines = [
        "WABI SABI ENGINE TASK SPEC",
        f"Resultado: {'OK' if payload.get('ok') else 'REVIEW'}",
    ]
    if not payload.get("ok"):
        lines.append(f"Error: {payload.get('error', 'unknown')}")
        return "\n".join(lines)
    task_spec = payload.get("task_spec", {})
    lines.extend(
        [
            f"Proyecto: {payload.get('plan_project')}",
            f"Target: {payload.get('target')}",
            f"Schema: {task_spec.get('schema')}",
            f"Gate: {payload.get('metadata', {}).get('action_gate')}",
            "CAMBIOS:",
        ]
    )
    for change in task_spec.get("changes", []):
        lines.append(f"- {change.get('op')}: {change.get('target')}")
    if payload.get("artifact"):
        lines.append("ARTEFACTO:")
        lines.append(f"- {payload.get('artifact')}")
    lines.append("PROXIMO:")
    lines.append("- Escribe este JSON como spec y pasalo por task-spec-plan/task-spec-apply.")
    return "\n".join(lines)


def _format_engine_sandbox_payload(payload: dict[str, Any]) -> str:
    lines = [
        "WABI SABI ENGINE SANDBOX",
        f"Resultado: {'OK' if payload.get('ok') else 'REVIEW'}",
    ]
    if not payload.get("ok"):
        lines.append(f"Error: {payload.get('error', 'unknown')}")
        validation = payload.get("validation", {})
        if validation.get("errors"):
            lines.append("ERRORES:")
            lines.extend(f"- {item}" for item in validation["errors"])
        return "\n".join(lines)
    project = payload.get("project", {})
    validation = payload.get("validation", {})
    lines.extend(
        [
            f"Proyecto: {project.get('project_name')}",
            f"Schema: {project.get('schema')}",
            f"Fingerprint: {validation.get('fingerprint')}",
            f"Nodos: {validation.get('node_count')}  Edges: {validation.get('edge_count')}  Escenas: {validation.get('scene_count')}",
            f"Visibility: {project.get('visibility', {}).get('classification')} / publish={project.get('visibility', {}).get('publish_allowed')}",
        ]
    )
    if payload.get("artifact"):
        lines.append("ARTEFACTO:")
        lines.append(f"- {payload.get('artifact')}")
    return "\n".join(lines)


def _format_engine_project_validation_payload(payload: dict[str, Any]) -> str:
    lines = [
        "WABI SABI ENGINE PROJECT VALIDATION",
        f"Resultado: {'OK' if payload.get('ok') else 'REVIEW'}",
    ]
    if not payload.get("ok") and payload.get("error"):
        lines.append(f"Error: {payload.get('error')}")
        return "\n".join(lines)
    validation = payload.get("validation", {})
    lines.extend(
        [
            f"Spec: {payload.get('spec_path')}",
            f"Fingerprint: {validation.get('fingerprint')}",
            f"Nodos: {validation.get('node_count')}  Edges: {validation.get('edge_count')}  Escenas: {validation.get('scene_count')}",
        ]
    )
    if validation.get("errors"):
        lines.append("ERRORES:")
        lines.extend(f"- {item}" for item in validation["errors"])
    return "\n".join(lines)


def _format_engine_simulation_payload(payload: dict[str, Any]) -> str:
    lines = [
        "WABI SABI ENGINE SIMULATION",
        f"Resultado: {'OK' if payload.get('ok') else 'REVIEW'}",
    ]
    if not payload.get("ok"):
        lines.append(f"Error: {payload.get('error', 'unknown')}")
        return "\n".join(lines)
    simulation = payload.get("simulation", {})
    state = simulation.get("state", {})
    lines.extend(
        [
            f"Spec: {payload.get('spec_path')}",
            f"Eventos: {simulation.get('event_count')}",
            f"Reglas disparadas: {len(simulation.get('fired_rules', []))}",
            f"Observation count: {state.get('scene.observation_count')}",
            f"Pattern visible: {state.get('pattern_marker.visible')}",
            f"Residue: {state.get('residue_meter.value')}",
            f"Gate: {state.get('sandbox.action_gate')}",
        ]
    )
    return "\n".join(lines)


def _format_task_spec_payload(payload: dict[str, Any]) -> str:
    lines = [
        "WABI SABI TASK SPEC",
        f"Accion: {payload.get('action')}  Resultado: {'OK' if payload.get('ok') else 'BLOCK'}",
    ]
    if not payload.get("ok"):
        lines.append(f"Error: {payload.get('error', 'unknown')}")
        return "\n".join(lines)
    lines.extend(
        [
            f"Spec: {payload.get('spec_path')}",
            f"Plan: {payload.get('plan_id')}",
            f"Changed: {payload.get('changed')}",
            "Operaciones:",
        ]
    )
    lines.extend(f"- {item}" for item in payload.get("operations", []))
    lines.append("ARTEFACTOS:")
    lines.append(f"- Plan: {payload.get('plan_artifact')}")
    lines.append(f"- Diff: {payload.get('diff_artifact')}")
    if payload.get("execution_artifact"):
        lines.append(f"- Execution: {payload.get('execution_artifact')}")
    if payload.get("rollback_artifact"):
        lines.append(f"- Rollback: {payload.get('rollback_artifact')}")
    if payload.get("verification"):
        lines.append(f"Verificacion: {payload.get('verification')}")
    if payload.get("witness_event_id"):
        lines.append(f"Witness: {payload.get('witness_event_id')} {'OK' if payload.get('witness_verified') else 'REVIEW'}")
    return "\n".join(lines)


def _format_cloud_proposal_payload(payload: dict[str, Any]) -> str:
    lines = [
        "WABI SABI CLOUD PROPOSAL",
        f"Accion: {payload.get('action')}  Resultado: {'OK' if payload.get('ok') else 'REVIEW'}",
        f"Cloud: proposal_only, provider_called={payload.get('cloud_provider_called', False)}",
    ]
    validation = payload.get("validation", {})
    if validation:
        lines.extend(
            [
                f"Schema: {validation.get('proposal_schema')}",
                f"Summary: {validation.get('summary')}",
                f"Gate sugerido por cloud: {validation.get('gate_recommendation')}",
                f"Cambios: {validation.get('changes_count')}",
            ]
        )
    if not payload.get("ok"):
        lines.append(f"Error: {payload.get('error', 'unknown')}")
        for error in validation.get("errors", []):
            lines.append(f"- {error}")
        return "\n".join(lines)
    if payload.get("task_spec_artifact"):
        lines.append(f"TaskSpec: {payload.get('task_spec_artifact')}")
    if payload.get("plan_artifact"):
        lines.append(f"PatchPlan: {payload.get('plan_artifact')}")
    if payload.get("diff_artifact"):
        lines.append(f"Diff: {payload.get('diff_artifact')}")
    warnings = validation.get("warnings", [])
    if warnings:
        lines.append("Warnings:")
        lines.extend(f"- {item}" for item in warnings)
    lines.append("Siguiente: task-spec-plan/task-spec-apply segun gate local.")
    return "\n".join(lines)


def _format_provider_contract_payload(payload: dict[str, Any]) -> str:
    status = payload.get("provider_status", payload)
    return "\n".join(
        [
            "WABI PROVIDER STATUS v0.4",
            f"Primary: {status.get('primary_provider', payload.get('provider'))}/{status.get('primary_model', payload.get('model'))}",
            f"State: {status.get('provider_state', payload.get('live_smoke_status'))}",
            f"Live smoke: {status.get('live_smoke_status', payload.get('live_smoke_status'))}",
            f"Fallback: {status.get('fallback_provider')}/{status.get('fallback_model')}",
            f"Cloud flag: {status.get('cloud_allowed_by_flag')}",
            f"Cloud mode: {status.get('cloud_allowed_mode')}",
            f"Credential present: {status.get('credential_present_redacted')}",
            f"PublicationGate: {status.get('publication_gate', payload.get('publication_gate', 'BLOCK'))}",
        ]
    )


def _format_nvidia_route_diagnostic_payload(payload: dict[str, Any]) -> str:
    diagnostic = payload.get("route_diagnostic", payload)
    aliases = ", ".join(item.get("alias", "") for item in diagnostic.get("alias_candidates", []) if isinstance(item, dict))
    return "\n".join(
        [
            "WABI NVIDIA ROUTE DIAGNOSTIC v0.5",
            f"Provider: {diagnostic.get('provider', payload.get('provider', 'nvidia'))}",
            f"Primary model: {diagnostic.get('primary_model_configured')}",
            f"Endpoint mode: {diagnostic.get('endpoint_mode')}",
            f"Last smoke: {diagnostic.get('last_smoke_status')}",
            f"Last error: {diagnostic.get('last_error_class')}",
            f"Route diagnostic: {diagnostic.get('route_diagnostic_status')}",
            f"Recommended smoke: {diagnostic.get('recommended_next_smoke')}",
            f"Next action: {payload.get('recommended_next_action')}",
            f"Credential present: {payload.get('credential_present_redacted')}",
            f"Cloud called: {payload.get('cloud_provider_called', False)}",
            f"Aliases: {aliases}",
            f"PublicationGate: {payload.get('publication_gate', 'BLOCK')}",
        ]
    )


def _format_cloud_debug_loop_payload(payload: dict[str, Any]) -> str:
    return "\n".join(
        [
            "WABI CLOUD DEBUG LOOP v0.4",
            f"Mode: {payload.get('mode')}",
            f"Scope: {payload.get('workspace_scope')}",
            f"Result: {'OK' if payload.get('ok') else 'BLOCK'}",
            f"PatchPlan: {payload.get('patch_plan_valid')}",
            f"Apply: {payload.get('apply_status')}",
            f"Tests: ran={payload.get('tests', {}).get('ran')} passed={payload.get('tests', {}).get('passed')}",
            f"Rollback: {payload.get('rollback_artifact') or 'none'}",
            f"Witness: {payload.get('witness_path') or 'none'}",
        ]
    )


def _format_patch_payload(payload: dict[str, Any]) -> str:
    lines = [
        "WABI SABI PATCH",
        f"Accion: {payload.get('action')}  Resultado: {'OK' if payload.get('ok') else 'BLOCK'}",
    ]
    if not payload.get("ok"):
        lines.append(f"Error: {payload.get('error', 'unknown')}")
        return "\n".join(lines)
    lines.extend(
        [
            f"Target: {payload.get('target')}",
            f"Plan: {payload.get('plan_id')}",
            f"Changed: {payload.get('changed')}",
            f"Gate: {payload.get('gate')}",
            "",
            "ARTEFACTOS:",
            f"- Plan: {payload.get('plan_artifact')}",
            f"- Diff: {payload.get('diff_artifact')}",
        ]
    )
    if payload.get("execution_artifact"):
        lines.append(f"- Execution: {payload.get('execution_artifact')}")
    if payload.get("rollback_artifact"):
        lines.append(f"- Rollback: {payload.get('rollback_artifact')}")
    if payload.get("verification"):
        lines.append(f"Verificacion: {payload.get('verification')}")
    if payload.get("witness_event_id"):
        lines.append(f"Witness: {payload.get('witness_event_id')} {'OK' if payload.get('witness_verified') else 'REVIEW'}")
    if payload.get("test_commands"):
        lines.append("Tests:")
        lines.extend(f"- {command}" for command in payload.get("test_commands", []))
    return "\n".join(lines)


def _format_rollback_payload(payload: dict[str, Any]) -> str:
    if not payload.get("ok"):
        return f"WABI SABI ROLLBACK\nResultado: BLOCK\nError: {payload.get('error', 'unknown')}"
    result = payload["result"]
    lines = [
        "WABI SABI ROLLBACK",
        "Resultado: OK",
        f"Snapshot: {result.get('snapshot')}",
        f"Witness: {result.get('witness_event_id')} {'OK' if result.get('witness_verified') else 'REVIEW'}",
        "Restored:",
    ]
    lines.extend(f"- {item}" for item in result.get("restored", []))
    if not result.get("restored"):
        lines.append("- ninguno")
    lines.append("Removed:")
    lines.extend(f"- {item}" for item in result.get("removed", []))
    if not result.get("removed"):
        lines.append("- ninguno")
    return "\n".join(lines)


def _format_tool_registry_payload(payload: dict[str, Any]) -> str:
    lines = ["WABI SABI TOOL REGISTRY"]
    for tool in payload.get("tools", []):
        lines.append(f"- {tool['name']}: {tool['gate']} - {tool['purpose']}")
    lines.append("BLOQUEADO:")
    lines.extend(f"- {item}" for item in payload.get("blocked_patterns", []))
    return "\n".join(lines)


def _format_archive_intake_payload(payload: dict[str, Any]) -> str:
    summary = payload.get("summary", {})
    lines = [
        "WABI SABI ARCHIVE INTAKE",
        f"Resultado: {'OK' if payload.get('ok') else 'REVIEW'}",
        f"Archive: {payload.get('archive')}",
        f"Members: {summary.get('member_count', 0)}  Text indexed: {summary.get('text_indexed_count', 0)}",
        "",
        "CLASIFICACION:",
    ]
    for name, count in summary.get("classification_counts", {}).items():
        lines.append(f"- {name}: {count}")
    lines.append("")
    lines.append("ARTEFACTOS:")
    for artifact in payload.get("artifacts", []):
        lines.append(f"- {artifact}")
    return "\n".join(lines)


def _format_variant_comparison_payload(payload: dict[str, Any]) -> str:
    summary = payload.get("summary", {})
    lines = [
        "WABI SABI CEREBRO VARIANT COMPARISON",
        f"Resultado: {'OK' if payload.get('ok') else 'REVIEW'}",
        f"Variant groups: {summary.get('variant_group_count', 0)}",
        f"Archive review: {summary.get('archive_review_candidates', 0)}",
        f"Canon merge review: {summary.get('canon_merge_review_candidates', 0)}",
        f"Keep separate/no merge: {summary.get('must_keep_separate_count', 0)}",
        "",
        "TOP REVIEW:",
    ]
    for item in payload.get("comparisons", [])[:12]:
        lines.append(
            f"- {item['variant_id']}: {item['semantic_status']} / {item['merge_gate']} / {item['recommendation']}"
        )
    if payload.get("artifacts"):
        lines.append("")
        lines.append("ARTEFACTOS:")
        lines.extend(f"- {artifact}" for artifact in payload["artifacts"])
    lines.append("")
    lines.append("NOT CLAIMED:")
    lines.extend(f"- {item}" for item in payload.get("not_claimed", []))
    return "\n".join(lines)


def _format_duplicate_migration_plan_payload(payload: dict[str, Any]) -> str:
    summary = payload.get("summary", {})
    lines = [
        "WABI SABI CEREBRO DUPLICATE MIGRATION PLAN",
        f"Resultado: {'OK' if payload.get('ok') else 'REVIEW'}",
        f"Exact duplicate groups: {summary.get('exact_duplicate_groups', 0)}",
        f"Proposed archive moves: {summary.get('proposed_archive_moves', 0)}",
        f"Ready for review: {summary.get('ready_for_review', 0)}",
        f"Blocked moves: {summary.get('blocked_moves', 0)}",
        f"Dry-run source mutations: {summary.get('source_mutations', 0)}",
        "",
        "TOP ACTIONS:",
    ]
    for action in payload.get("actions", [])[:12]:
        lines.append(
            "- {}: {} -> {}".format(
                action.get("status"),
                action.get("source"),
                action.get("proposed_archive_target"),
            )
        )
    if payload.get("artifacts"):
        lines.append("")
        lines.append("ARTEFACTOS:")
        lines.extend(f"- {artifact}" for artifact in payload["artifacts"])
    lines.append("")
    lines.append("NOT CLAIMED:")
    lines.extend(f"- {item}" for item in payload.get("not_claimed", []))
    return "\n".join(lines)


def _format_canon_merge_review_payload(payload: dict[str, Any]) -> str:
    summary = payload.get("summary", {})
    lines = [
        "WABI SABI CEREBRO CANON MERGE REVIEW",
        f"Resultado: {'OK' if payload.get('ok') else 'REVIEW'}",
        f"Review candidate groups: {summary.get('review_candidate_groups', 0)}",
        f"Unique candidate sets: {summary.get('unique_candidate_sets', 0)}",
        f"Duplicate candidate sets: {summary.get('duplicate_candidate_sets', 0)}",
        f"Auto-merge actions: {summary.get('auto_merge_actions', 0)}",
        f"Source mutations: {summary.get('source_mutations', 0)}",
        "",
        "CANDIDATES:",
    ]
    for candidate in payload.get("candidates", [])[:12]:
        lines.append(
            "- {}: {} / {} / {}".format(
                candidate.get("variant_id"),
                candidate.get("boundary_type"),
                candidate.get("review_gate"),
                candidate.get("review_decision", {}).get("action"),
            )
        )
    if payload.get("artifacts"):
        lines.append("")
        lines.append("ARTEFACTOS:")
        lines.extend(f"- {artifact}" for artifact in payload["artifacts"])
    lines.append("")
    lines.append("NOT CLAIMED:")
    lines.extend(f"- {item}" for item in payload.get("not_claimed", []))
    return "\n".join(lines)


def _format_geodia_synthetic_payload(payload: dict[str, Any]) -> str:
    after = payload["metrics"]["after"]
    lines = [
        "WABI SABI GEODIA SYNTHETIC SURFACE",
        f"Status: {payload['status']}  Gate: {payload['action_gate']}",
        f"Claim gate: {payload['claim_gate']}",
        f"Regimen: {after['regime']}",
        f"R: {after['R']:.4f}  Phi_eff: {after['phi_eff']:.4f}  I_obs: {after['I_obs']:.4f}",
        f"EML: {payload['metrics']['eml']:.4f}  Bounded: {payload['bounded']}",
        "",
        "CERTEZA:",
    ]
    lines.extend(f"- {item}" for item in payload.get("certainty", []))
    lines.append("")
    lines.append("INCOGNITA:")
    lines.extend(f"- {item}" for item in payload.get("unknown", []))
    lines.append("")
    lines.append("NOT CLAIMED:")
    lines.extend(f"- {item}" for item in payload.get("not_claimed", []))
    return "\n".join(lines)


def _format_geodia_falsifier_payload(payload: dict[str, Any]) -> str:
    lines = [
        "WABI SABI GEODIA SYNTHETIC FALSIFIER",
        f"Resultado: {payload['result']}  Gate: {payload['action_gate']}",
        f"Claim gate: {payload['claim_gate']}",
        f"Claim contract: {payload['claim_evaluation']['gate']} / {payload['claim_evaluation']['status']}",
        "",
        "FALSADORES:",
    ]
    lines.extend(f"- {item['id']}: {item['status']} - {item['falsifier']}" for item in payload.get("falsifiers", []))
    lines.append("")
    lines.append("ARTEFACTOS:")
    lines.extend(f"- {artifact}" for artifact in payload.get("artifacts", []))
    lines.append("")
    lines.append("INCOGNITA:")
    lines.extend(f"- {item}" for item in payload.get("unknown", []))
    return "\n".join(lines)


def _format_worktree_payload(payload: dict[str, Any]) -> str:
    if not payload.get("ok"):
        return f"WABI SABI WORKTREE\nResultado: REVIEW\nError: {payload.get('error', 'unknown')}"
    lines = [
        "WABI SABI WORKTREE",
        f"Repo: {payload.get('repo_root')}",
        f"Branch: {payload.get('branch')}  Commit: {payload.get('base_commit')}",
        f"Dirty: {payload.get('dirty')}  Status: {payload.get('status_count')}",
        "",
        "STATUS SAMPLE:",
    ]
    if payload.get("status_sample"):
        lines.extend(f"- {item}" for item in payload["status_sample"])
    else:
        lines.append("- limpio")
    if payload.get("diff_stat"):
        lines.append("")
        lines.append("DIFF STAT:")
        lines.append(payload["diff_stat"])
    lines.append("")
    lines.append("Contenido de archivos: NO incluido")
    return "\n".join(lines)


def _execute_eml_command(items: list[str]) -> dict[str, Any]:
    mode = items[0].lower() if items else "safe"
    numbers = items[1:] if mode in {"safe", "window-load", "jamming-margin"} else items
    try:
        if mode == "window-load":
            if len(numbers) != 3:
                raise ValueError("window-load requiere r_token circularity unresolved_tasks")
            result = window_load_eml(
                r_token=float(numbers[0]),
                circularity=float(numbers[1]),
                unresolved_tasks=float(numbers[2]),
            )
        elif mode == "jamming-margin":
            if len(numbers) != 2:
                raise ValueError("jamming-margin requiere residue_norm phi_log")
            result = jamming_margin_eml(residue_norm=float(numbers[0]), phi_log=float(numbers[1]))
        else:
            if len(numbers) != 2:
                raise ValueError("eml requiere signal_log residue_norm")
            result = safe_eml(signal_log=float(numbers[0]), residue_norm=float(numbers[1]))
    except ValueError as exc:
        return {
            "ok": False,
            "action": "eml_research_only",
            "error": str(exc),
            "result": {"domain_ok": False, "warnings": [str(exc)], "epistemic_status": "RESEARCH_ONLY"},
        }
    return {
        "ok": result.domain_ok,
        "action": "eml_research_only",
        "mode": mode if mode in {"safe", "window-load", "jamming-margin"} else "safe",
        "result": result.to_dict(),
    }


def _format_eml_payload(payload: dict[str, Any]) -> str:
    result = payload["result"]
    lines = [
        "WABI SABI EML",
        f"Modo: {payload.get('mode', 'safe')}  Estado: {result.get('epistemic_status', 'RESEARCH_ONLY')}",
        f"Dominio: {'OK' if result.get('domain_ok') else 'ERROR'}",
        f"Valor: {result.get('value') if result.get('value') is not None else 'none'}",
    ]
    if result.get("warnings"):
        lines.append("Warnings:")
        lines.extend(f"- {item}" for item in result["warnings"])
    return "\n".join(lines)


def _format_codex_status(payload: dict[str, Any]) -> str:
    if "codex" in payload or "ollama" in payload:
        codex = payload.get("codex", {})
        ollama = payload.get("ollama", {})
        lines = [
            "WABI SABI PROVIDERS",
            f"Auto provider: {payload.get('auto_provider')}",
            f"Orden: {', '.join(payload.get('provider_order', []))}",
            f"Codex CLI: {'OK' if codex.get('codex_cli', {}).get('available') else 'NO'}",
            f"OpenAI Responses: {'OK' if codex.get('openai_responses', {}).get('available') else 'NO'}",
            f"Modelo base: {ollama.get('base_model') or 'no expuesto'}",
            f"Endpoint modelo: {ollama.get('model_endpoint') or ollama.get('host') or 'no expuesto'}",
            f"Ollama/Base local: {'OK' if ollama.get('enabled') and ollama.get('available') else 'NO_DISPONIBLE'}",
        ]
        if ollama.get("enabled"):
            lines.append(f"Ollama modelos: {', '.join(ollama.get('models', [])) or 'ninguno'}")
            lines.append(f"Ollama activos: {', '.join(ollama.get('running', [])) or 'ninguno'}")
            if ollama.get("cloud_models_filtered"):
                lines.append(f"Modelos cloud filtrados: {len(ollama.get('cloud_models_filtered', []))}")
        else:
            lines.append(f"Activacion: {ollama.get('enable_env', 'BASE_MODEL=qwen2.5-coder:3b')}")
        cloud = payload.get("cloud", {})
        if cloud:
            lines.append("Cloud adapters:")
            for name, provider in cloud.items():
                configured = "configurado" if provider.get("configured") else "sin clave"
                enabled = "habilitado" if provider.get("enabled") else "bloqueado"
                lines.append(f"- {name}: {configured}, {enabled}, modelo={provider.get('model', 'no expuesto')}")
                catalog = provider.get("model_catalog", [])
                if catalog:
                    aliases = ", ".join(str(item.get("alias", "")) for item in catalog if item.get("alias"))
                    lines.append(f"  aliases: {aliases}")
        policy = payload.get("blueprint_policy", {})
        if policy:
            lines.append(f"Planos: {'OK' if policy.get('loaded') else 'NO'}")
            if policy.get("loaded"):
                lines.append(f"Planos fuentes: {len(policy.get('sources', []))}")
            if policy.get("reasons"):
                lines.append(f"Politica: {', '.join(policy.get('reasons', []))}")
        worktree = payload.get("worktree", {})
        if worktree:
            if worktree.get("ok"):
                lines.append(
                    f"Worktree: {'dirty' if worktree.get('dirty') else 'clean'} "
                    f"{worktree.get('branch')}@{worktree.get('base_commit')} "
                    f"status={worktree.get('status_count')}"
                )
            else:
                lines.append(f"Worktree: {worktree.get('error', 'unknown')}")
        return "\n".join(lines)
    lines = [
        "WABI SABI CODEX STATUS",
        f"Auto provider: {payload['auto_provider']}",
        f"Codex CLI: {'OK' if payload['codex_cli']['available'] else 'NO'}",
        f"OpenAI Responses: {'OK' if payload['openai_responses']['available'] else 'NO'}",
        f"Safe default: {payload['safe_default']}",
    ]
    if payload["codex_cli"].get("path"):
        lines.append(f"Codex path: {payload['codex_cli']['path']}")
    lines.append(f"OpenAI model: {payload['openai_responses']['model']}")
    return "\n".join(lines)


def _format_codex_payload(payload: dict[str, Any]) -> str:
    lines = [
        "WABI SABI CODEX BRIDGE",
        f"Proveedor: {payload['provider']}  Gate: {payload['gate']}  Resultado: {'OK' if payload['ok'] else 'BLOCK'}",
        f"Accion: {payload['action']}",
        "",
        "RESPUESTA:",
        payload["output"] or "- Sin salida.",
        "",
        "EVIDENCIA:",
    ]
    if payload["evidence"]:
        lines.extend(f"- {item}" for item in payload["evidence"])
    else:
        lines.append("- Sin evidencia adicional.")
    if payload["artifacts"]:
        lines.append("")
        lines.append("ARTEFACTOS:")
        lines.extend(f"- {artifact}" for artifact in payload["artifacts"])
    if payload["error"]:
        lines.append("")
        lines.append(f"ERROR: {payload['error']}")
    return "\n".join(lines)


def _format_auto_payload(payload: dict[str, Any]) -> str:
    lines = [
        "WABI SABI AUTO",
        f"Ruta: {payload['route']}  Gate: {payload['gate']}  Resultado: {'OK' if payload['ok'] else 'BLOCK'}",
        f"Razon: {', '.join(payload['reasons']) or 'sin razon registrada'}",
        "",
        "RESPUESTA:",
        payload["output"] or "- Sin salida.",
    ]
    if payload["artifacts"]:
        lines.append("")
        lines.append("ARTEFACTOS:")
        lines.extend(f"- {artifact}" for artifact in payload["artifacts"])
    return "\n".join(lines)


def _auto_interactive(
    config: RuntimeConfig,
    *,
    codex_provider: str = "auto",
    codex_timeout: int = 35,
) -> int:
    orchestrator = ProviderOrchestrator(workspace=config.workspace, runtime_root=config.runtime_root)
    orchestrator.warm_fast_models()
    print("Wabi Sabi Auto. Respuesta local inmediata; Codex profundo corre en background.")
    print("Comandos: /status, /jobs, /result [id], /memory, /local, /codex, /dry, /exit.")
    while True:
        try:
            prompt = input("Wabi-Auto> ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            return 0
        if not prompt:
            continue
        if prompt in {"/exit", "exit", "salir"}:
            return 0
        if prompt in {"/jobs", "jobs"}:
            print(summarize_jobs(JobStore(config.runtime_root).list_recent(limit=10)))
            continue
        if prompt in {"/memory", "memory", "memoria"}:
            summary = LocalMemory(config.runtime_root).conversation_summary()
            print(summary or "No hay memoria conversacional local todavia.")
            continue
        if prompt.startswith("/result") or prompt.startswith("result"):
            parts = prompt.split(maxsplit=1)
            store = JobStore(config.runtime_root)
            job_id = parts[1].strip() if len(parts) > 1 else store.latest_id()
            if not job_id:
                print("No hay jobs registrados.")
                continue
            try:
                print(format_job_result(store.read(job_id)))
            except FileNotFoundError:
                print(f"No encontre job: {job_id}")
            continue
        payload = execute_auto_prompt(
            prompt,
            workspace=config.workspace,
            runtime_root=config.runtime_root,
            codex_provider=codex_provider,
            codex_timeout=codex_timeout,
            background_codex=True,
        )
        print(_format_auto_payload(payload))


def _interactive(config: RuntimeConfig) -> int:
    print("Wabi Sabi Local Chat. Escribe /status para estado o /exit para salir.")
    while True:
        try:
            prompt = input("Wabi> ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            return 0
        if not prompt:
            continue
        if prompt in {"/exit", "exit", "salir"}:
            return 0
        payload = execute_chat_prompt(prompt, workspace=config.workspace, runtime_root=config.runtime_root)
        print(_format_auto_payload(payload))


def _conversational_interactive(session: ConversationSession) -> int:
    session.orchestrator.warm_fast_models()
    print("Wabi-Sabi")
    print("Modo: chat/code auto")
    print("Provider: auto")
    print(_startup_provider_summary(session))
    print(f"Workspace: {session.workspace}")
    print("Wabi-Sabi listo. Escribe normal. Usa /salir para cerrar. /help para comandos.")
    while True:
        try:
            prompt = input("Luis> ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            return 0
        if _is_secret_command(prompt):
            print(_handle_secret_command(prompt))
            continue
        payload = session.handle(prompt)
        if payload["route"] == "exit":
            print(format_conversation_payload(payload))
            return 0
        formatted = format_conversation_payload(payload)
        if formatted:
            print(formatted)


def _startup_provider_summary(session: ConversationSession) -> str:
    try:
        report = build_provider_report(runtime_root=session.runtime_root, smoke=False, timeout=5)
        statuses = {row["provider"]: row["status"] for row in report.get("providers", [])}
        nvidia = statuses.get("nvidia", "UNKNOWN")
        qwen = statuses.get("qwen") or statuses.get("dashscope_qwen", "UNKNOWN")
        deepseek = statuses.get("deepseek", "UNKNOWN")
        local = statuses.get("local/ollama", "UNKNOWN")
        return f"Cloud: NVIDIA {nvidia} | Qwen {qwen} | DeepSeek {deepseek} | Local {local}"
    except Exception:
        return "Cloud: provider summary unavailable; usa /providers."


def _is_secret_command(prompt: str) -> bool:
    return prompt.strip().lower().startswith(("/secret ", "/set-secret ", "/secreto "))


def _handle_secret_command(prompt: str) -> str:
    parts = prompt.strip().split()
    if len(parts) < 2:
        allowed = ", ".join(sorted(SECRET_ENV_KEYS))
        return f"Wabi-Sabi: indica una variable permitida. Ejemplo: /secret DASHSCOPE_API_KEY. Permitidas: {allowed}"
    key = parts[1].strip().upper()
    allowed_keys = SECRET_ENV_KEYS | SAFE_CONFIG_ENV_KEYS
    if key not in allowed_keys:
        allowed = ", ".join(sorted(allowed_keys))
        return f"Wabi-Sabi: variable no permitida para captura segura: {key}. Permitidas: {allowed}"

    def hidden_prompt(_prompt: str = "") -> str:
        return getpass.getpass(f"{key} (oculto, no se imprime): ")

    try:
        result = capture_secret_to_user_env(key, secret_getter=hidden_prompt)
    except Exception as exc:
        return f"Wabi-Sabi: no pude guardar {key}; estado REVIEW. Razon: {redact_text(str(exc))}"
    status = result.get("status", "REVIEW")
    message = result.get("message", "")
    restart = " Abre una terminal nueva si el provider no ve el cambio en esta sesion." if result.get("terminal_restart_may_be_required") else ""
    return f"Wabi-Sabi: {key} {status}. {message}.{restart}"


def _format_agents(payload: dict[str, Any]) -> str:
    lines = ["WABI SABI AGENTS"]
    for name, spec in payload.get("agents", {}).items():
        lines.append(f"- {name}: {spec.get('description', '')}")
        lines.append(f"  capacidades: {', '.join(spec.get('capabilities', []))}")
        lines.append(f"  limites: {', '.join(spec.get('limits', []))}")
    return "\n".join(lines)


def _memory_excerpt(text: str, limit: int = 700) -> str:
    clean = " ".join(str(text or "").split())
    if len(clean) <= limit:
        return clean
    return clean[: limit - 3] + "..."


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
