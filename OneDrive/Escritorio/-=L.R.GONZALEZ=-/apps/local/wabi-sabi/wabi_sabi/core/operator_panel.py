from __future__ import annotations

import json
import sqlite3
from pathlib import Path
from typing import Any

from wabi_sabi.core.bridge import WitnessLog
from wabi_sabi.core.geodia_synthetic_falsifier import build_geodia_synthetic_falsifier
from wabi_sabi.core.geodia_synthetic_surface import build_geodia_synthetic_surface
from wabi_sabi.core.provider_orchestrator import ProviderOrchestrator
from wabi_sabi.core.task_spec_planner import build_patch_plan_from_task_spec
from wabi_sabi.core.tool_registry import tool_registry_payload
from wabi_sabi.core.worktree import git_worktree_summary


def build_operator_panel(
    *,
    workspace: str | Path,
    runtime_root: str | Path,
    task_spec: str | Path | None = None,
    max_files: int = 12,
) -> dict[str, Any]:
    workspace_path = Path(workspace).resolve()
    runtime_path = Path(runtime_root).resolve()
    provider_status = ProviderOrchestrator(workspace=workspace_path, runtime_root=runtime_path).status()
    worktree = git_worktree_summary(workspace_path, max_files=max_files)
    tools = tool_registry_payload()
    task_spec_status = _task_spec_status(workspace_path, task_spec)
    witness = witness_summary(runtime_path)
    latest_safe_tests = latest_safe_test_summary(runtime_path)
    geodia_research = geodia_research_summary(runtime_path)
    provider = _provider_summary(provider_status)
    checks = {
        "provider_visible": bool(provider.get("auto_provider")),
        "worktree_readable": bool(worktree.get("ok")),
        "tools_visible": bool(tools.get("tools")),
        "task_spec_plan_ready": bool(task_spec_status.get("ok")),
        "witness_chain_ok": bool(witness.get("verified") or not witness.get("exists")),
        "latest_safe_tests_readable": bool(latest_safe_tests.get("ok")),
        "geodia_research_only_readable": bool(geodia_research.get("ok")),
    }
    return {
        "schema": "wabi.operator_panel.v1",
        "ok": all(checks.values()),
        "action": "operator_status",
        "workspace": str(workspace_path),
        "runtime_root": str(runtime_path),
        "gate": "APPROVE" if all(checks.values()) else "REVIEW",
        "checks": checks,
        "provider": provider,
        "worktree": {
            "ok": worktree.get("ok"),
            "repo_root": worktree.get("repo_root"),
            "branch": worktree.get("branch"),
            "base_commit": worktree.get("base_commit"),
            "dirty": worktree.get("dirty"),
            "status_count": worktree.get("status_count"),
            "status_sample": worktree.get("status_sample", []),
            "content_included": worktree.get("limits", {}).get("content_included", False),
            "error": worktree.get("error", ""),
        },
        "tools": {
            "names": [tool["name"] for tool in tools.get("tools", [])],
            "blocked_patterns": tools.get("blocked_patterns", []),
        },
        "task_spec": task_spec_status,
        "witness": witness,
        "latest_safe_tests": latest_safe_tests,
        "geodia_research": geodia_research,
        "commands": _operator_commands(task_spec_status),
        "next_actions": [
            "Use task-spec-plan before task-spec-apply.",
            "Use worktree-status before touching files in a dirty workspace.",
            "Use rollback with a plan_id if a Wabi/Sabi patch must be reverted.",
            "Use run-safe-tests only when fresh verification is needed; operator-status reads the latest artifact.",
            "Use geodia-falsifier before showing GEODIA metrics beyond RESEARCH_ONLY.",
        ],
    }


def witness_summary(runtime_root: str | Path) -> dict[str, Any]:
    db_path = Path(runtime_root).resolve() / "witness" / "wabi_patch_witness.sqlite"
    if not db_path.exists():
        return {
            "ok": True,
            "exists": False,
            "path": str(db_path),
            "verified": True,
            "verify_reason": "witness_db_not_created_yet",
            "event_count": 0,
            "last_hash": "GENESIS",
        }
    try:
        verified, reason = WitnessLog(db_path).verify_chain()
        with sqlite3.connect(db_path) as conn:
            row = conn.execute(
                "SELECT COUNT(*), COALESCE(MAX(id), 0) FROM witness_events"
            ).fetchone()
            count = int(row[0]) if row else 0
            last = conn.execute(
                "SELECT event_hash FROM witness_events ORDER BY id DESC LIMIT 1"
            ).fetchone()
        return {
            "ok": verified,
            "exists": True,
            "path": str(db_path),
            "verified": verified,
            "verify_reason": reason,
            "event_count": count,
            "last_hash": str(last[0]) if last else "GENESIS",
        }
    except Exception as exc:
        return {
            "ok": False,
            "exists": True,
            "path": str(db_path),
            "verified": False,
            "verify_reason": str(exc),
            "event_count": 0,
            "last_hash": "",
        }


def latest_safe_test_summary(runtime_root: str | Path) -> dict[str, Any]:
    output_dir = Path(runtime_root).resolve() / "outputs"
    if not output_dir.exists():
        return {
            "ok": True,
            "exists": False,
            "artifact": "",
            "schema": "wabi.safe_test_run.v1",
            "status": "not_run",
            "summary": {},
            "witness_event_id": 0,
            "witness_verified": False,
            "observed_at_utc": "",
        }
    reports = sorted(output_dir.glob("safe_test_run_*.json"), key=lambda path: path.stat().st_mtime, reverse=True)
    if not reports:
        return {
            "ok": True,
            "exists": False,
            "artifact": "",
            "schema": "wabi.safe_test_run.v1",
            "status": "not_run",
            "summary": {},
            "witness_event_id": 0,
            "witness_verified": False,
            "observed_at_utc": "",
        }
    latest = reports[0]
    try:
        payload = json.loads(latest.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return {
            "ok": False,
            "exists": True,
            "artifact": str(latest),
            "schema": "wabi.safe_test_run.v1",
            "status": "invalid",
            "summary": {},
            "witness_event_id": 0,
            "witness_verified": False,
            "observed_at_utc": "",
            "error": str(exc),
        }
    observation = payload.get("observation", {}) if isinstance(payload.get("observation"), dict) else {}
    summary = payload.get("summary", {}) if isinstance(payload.get("summary"), dict) else {}
    return {
        "ok": bool(payload.get("ok")),
        "exists": True,
        "artifact": str(latest),
        "schema": payload.get("schema", "wabi.safe_test_run.v1"),
        "status": "passed" if payload.get("ok") else "failed_or_review",
        "summary": {
            "command_count": summary.get("command_count", 0),
            "passed": summary.get("passed", 0),
            "failed": summary.get("failed", 0),
            "errors": summary.get("errors", []),
        },
        "witness_event_id": payload.get("witness_event_id", 0),
        "witness_verified": bool(payload.get("witness_verified")),
        "observed_at_utc": observation.get("observed_at_utc", ""),
    }


def geodia_research_summary(runtime_root: str | Path) -> dict[str, Any]:
    output_dir = Path(runtime_root).resolve() / "outputs"
    falsifier_artifact = output_dir / "GEODIA_SYNTHETIC_FALSIFIER.json"
    artifact_payload = _safe_json(falsifier_artifact) if falsifier_artifact.exists() else {}
    surface = build_geodia_synthetic_surface()
    falsifier = build_geodia_synthetic_falsifier()
    evaluation = artifact_payload.get("claim_evaluation", {}) if isinstance(artifact_payload.get("claim_evaluation"), dict) else {}
    return {
        "ok": bool(surface.get("ok")) and bool(falsifier.get("ok")),
        "epistemic_status": "RESEARCH_ONLY",
        "source": "deterministic_synthetic_fixture",
        "surface": {
            "schema": surface.get("schema"),
            "status": surface.get("status"),
            "claim_gate": surface.get("claim_gate"),
            "bounded": surface.get("bounded"),
            "regime": surface.get("metrics", {}).get("after", {}).get("regime"),
            "R": surface.get("metrics", {}).get("after", {}).get("R"),
            "phi_eff": surface.get("metrics", {}).get("after", {}).get("phi_eff"),
            "I_obs": surface.get("metrics", {}).get("after", {}).get("I_obs"),
        },
        "falsifier": {
            "schema": falsifier.get("schema"),
            "status": falsifier.get("status"),
            "result": falsifier.get("result"),
            "claim_gate": falsifier.get("claim_gate"),
            "claim_evaluation_gate": evaluation.get("gate", "not_written"),
            "claim_level": evaluation.get("claim_level", "operational"),
        },
        "artifact": str(falsifier_artifact) if falsifier_artifact.exists() else "",
        "not_claimed": [
            "No scientific validation.",
            "No production city simulation.",
            "No public claim beyond operational local smoke surface.",
        ],
    }


def _provider_summary(provider_status: dict[str, Any]) -> dict[str, Any]:
    codex = provider_status.get("codex", {})
    ollama = provider_status.get("ollama", {})
    return {
        "auto_provider": provider_status.get("auto_provider"),
        "provider_order": provider_status.get("provider_order", []),
        "base_model": ollama.get("base_model", ""),
        "base_model_available": bool(ollama.get("base_model_available")),
        "endpoint": ollama.get("model_endpoint") or ollama.get("host") or "",
        "ollama_enabled": bool(ollama.get("enabled")),
        "ollama_available": bool(ollama.get("available")),
        "ollama_running": ollama.get("running", []),
        "cloud_models_filtered": len(ollama.get("cloud_models_filtered", [])),
        "codex_cli_available": bool(codex.get("codex_cli", {}).get("available")),
        "openai_responses_available": bool(codex.get("openai_responses", {}).get("available")),
    }


def _safe_json(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}
    return data if isinstance(data, dict) else {}


def _task_spec_status(workspace: Path, task_spec: str | Path | None) -> dict[str, Any]:
    spec_ref = task_spec or _default_task_spec(workspace)
    spec_path = Path(spec_ref)
    candidate = spec_path if spec_path.is_absolute() else workspace / spec_path
    if not candidate.exists():
        return {
            "ok": False,
            "path": str(candidate),
            "error": "task_spec_not_found",
            "gate": "REVIEW",
            "operations": [],
            "test_commands": [],
        }
    try:
        spec, plan = build_patch_plan_from_task_spec(workspace=workspace, spec_path=spec_ref)
        return {
            "ok": True,
            "path": str(spec.path),
            "summary": spec.summary,
            "gate": plan.gate,
            "changed": plan.changed,
            "operations": [operation.relative_path for operation in plan.operations],
            "test_commands": plan.test_commands,
            "reasons": plan.reasons,
        }
    except Exception as exc:
        return {
            "ok": False,
            "path": str(candidate),
            "error": str(exc),
            "gate": "REVIEW",
            "operations": [],
            "test_commands": [],
        }


def _default_task_spec(workspace: Path) -> Path:
    candidates = [
        workspace / "docs" / "wabi_task_spec.example.json",
        Path(__file__).resolve().parents[2] / "docs" / "wabi_task_spec.example.json",
    ]
    for candidate in candidates:
        resolved = candidate.resolve()
        if resolved.exists() and (resolved == workspace or workspace in resolved.parents):
            return resolved
    return candidates[0]


def _operator_commands(task_spec_status: dict[str, Any]) -> list[str]:
    spec_path = task_spec_status.get("path") or "docs/wabi_task_spec.example.json"
    commands = [
        "wabi auto /status --json",
        "wabi worktree-status --json",
        "wabi tools --json",
    ]
    if task_spec_status.get("ok"):
        commands.append(f"wabi task-spec-plan {spec_path} --json")
    else:
        commands.append("wabi task-spec-plan docs/wabi_task_spec.example.json --json")
    return commands
