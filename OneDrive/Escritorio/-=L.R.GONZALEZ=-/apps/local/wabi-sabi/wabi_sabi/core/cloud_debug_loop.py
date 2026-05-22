from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any, Mapping

from wabi_sabi.core.patch_planner import write_patch_diff, write_patch_plan
from wabi_sabi.core.provider_status_contract import build_provider_status_contract
from wabi_sabi.core.redaction import is_sensitive_key, redact_mapping, redact_text
from wabi_sabi.core.rollback_store import RollbackStore
from wabi_sabi.core.safe_executor import SafeExecutor
from wabi_sabi.core.task_spec_planner import build_patch_plan_from_task_spec
from wabi_sabi.core.tools import stamp


def run_cloud_debug_loop(
    *,
    workspace: str | Path,
    runtime_root: str | Path,
    task_spec_path: str | Path,
    apply_patch: bool = False,
    max_retries: int = 2,
    env: Mapping[str, str] | None = None,
) -> dict[str, Any]:
    values = env or os.environ
    workspace_path = Path(workspace).resolve()
    runtime = Path(runtime_root).resolve()
    target_workspace, workspace_scope = _select_target_workspace(
        workspace=workspace_path,
        runtime=runtime,
        task_spec_path=task_spec_path,
    )
    mode = "apply" if apply_patch else "dry_run"
    payload: dict[str, Any] = {
        "schema": "wabi.cloud_debug_loop.v0_4",
        "ok": False,
        "mode": mode,
        "workspace_scope": workspace_scope,
        "provider_status": build_provider_status_contract(runtime_root=runtime, env=values),
        "proposal_valid": True,
        "patch_plan_valid": False,
        "apply_status": "NOT_APPLIED" if not apply_patch else "BLOCKED",
        "tests": {"ran": False, "passed": False, "results": []},
        "secret_values_printed": False,
        "rollback_available": False,
        "rollback_artifact": "",
        "witness_path": "",
        "retries_max": max_retries,
        "retries_used": 0,
        "cloud_authority": "proposal_only",
        "cloud_provider_called": False,
    }
    try:
        spec, plan = build_patch_plan_from_task_spec(
            workspace=target_workspace,
            spec_path=task_spec_path,
            input_roots=[workspace_path, runtime],
        )
        plan_artifact = write_patch_plan(runtime / "outputs", plan)
        diff_artifact = write_patch_diff(runtime / "outputs", plan)
        payload.update(
            {
                "ok": True,
                "spec": spec.to_dict(),
                "plan_id": plan.plan_id,
                "patch_plan_valid": True,
                "changed": plan.changed,
                "operations": [operation.relative_path for operation in plan.operations],
                "plan_artifact": str(plan_artifact),
                "diff_artifact": str(diff_artifact),
                "test_commands": list(plan.test_commands),
            }
        )
        rollback = RollbackStore(workspace=target_workspace, runtime_root=runtime).capture(plan)
        payload["rollback_available"] = True
        payload["rollback_artifact"] = str(rollback.path)
        if not apply_patch:
            payload["apply_status"] = "NOT_APPLIED"
            return _finalize(payload, runtime, values)

        execution = SafeExecutor(workspace=target_workspace, runtime_root=runtime).execute(plan)
        execution_payload = redact_mapping(execution.to_dict(), env=values)
        test_results = execution_payload.get("test_results", [])
        tests_ran = bool(plan.test_commands)
        tests_passed = bool(execution.ok and all(int(result.get("returncode", 1)) == 0 for result in test_results))
        payload.update(
            {
                "ok": execution.ok,
                "apply_status": "APPLIED" if execution.ok else "ROLLED_BACK",
                "tests": {"ran": tests_ran, "passed": tests_passed, "results": test_results},
                "execution": execution_payload,
                "execution_artifact": str(execution.execution_path),
                "rollback_artifact": str(execution.rollback_path),
                "rollback_available": Path(execution.rollback_path).exists(),
                "witness_db": execution.witness_db,
                "witness_verified": execution.witness_verified,
                "error": redact_text(execution.error, env=values),
            }
        )
        return _finalize(payload, runtime, values)
    except Exception as exc:
        error = str(exc)
        payload["ok"] = False
        payload["apply_status"] = "BLOCKED"
        payload["error"] = _normalize_loop_error(error)
        payload["detail"] = redact_text(error, env=values)
        return _finalize(payload, runtime, values)


def _finalize(payload: dict[str, Any], runtime_root: Path, env: Mapping[str, str]) -> dict[str, Any]:
    payload["secret_values_printed"] = _secret_values_printed(payload, env)
    payload = redact_mapping(payload, env=env)
    output_dir = runtime_root / "outputs" / "cloud_debug_loop"
    output_dir.mkdir(parents=True, exist_ok=True)
    path = output_dir / f"wabi_cloud_debug_loop_{stamp()}.json"
    payload["witness_path"] = str(path)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return payload


def _select_target_workspace(*, workspace: Path, runtime: Path, task_spec_path: str | Path) -> tuple[Path, str]:
    try:
        raw = json.loads(Path(task_spec_path).read_text(encoding="utf-8"))
    except Exception:
        return workspace, "workspace"
    if not isinstance(raw, dict):
        return workspace, "workspace"
    target_root = str(raw.get("target_root") or raw.get("workspace_scope") or "").strip().lower()
    if target_root == "runtime":
        return runtime, "runtime"
    return workspace, "workspace"


def _normalize_loop_error(error: str) -> str:
    lowered = error.lower()
    if any(token in lowered for token in ("outside_workspace", "target_path_blocked", "path_blocked")):
        return "BLOCK_PATCH_OUT_OF_SCOPE"
    return "CLOUD_DEBUG_LOOP_FAILED"


def _secret_values_printed(payload: Any, env: Mapping[str, str]) -> bool:
    text = json.dumps(payload, ensure_ascii=False, default=str)
    for key, value in env.items():
        if value and len(value) >= 8 and is_sensitive_key(key) and value in text:
            return True
    return False
