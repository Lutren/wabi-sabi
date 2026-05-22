from __future__ import annotations

import json
import py_compile
import shlex
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from wabi_sabi.core.bridge import WitnessLog
from wabi_sabi.core.observation import ObservationEnvelope
from wabi_sabi.core.patch_planner import PatchPlan, resolve_workspace_text_target, write_patch_diff, write_patch_plan
from wabi_sabi.core.redaction import redact_text
from wabi_sabi.core.rollback_store import RollbackStore


@dataclass(frozen=True)
class ExecutionResult:
    ok: bool
    plan_id: str
    changed: bool
    plan_path: Path
    diff_path: Path
    rollback_path: Path
    execution_path: Path
    written: list[str]
    test_results: list[dict[str, Any]]
    witness_event_id: int
    witness_verified: bool
    witness_verify_reason: str
    witness_db: str
    observation: dict[str, Any]
    verification: str
    error: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema": "wabi.safe_execution_result.v1",
            "ok": self.ok,
            "plan_id": self.plan_id,
            "changed": self.changed,
            "plan_path": str(self.plan_path),
            "diff_path": str(self.diff_path),
            "rollback_path": str(self.rollback_path),
            "execution_path": str(self.execution_path),
            "written": self.written,
            "test_results": self.test_results,
            "witness_event_id": self.witness_event_id,
            "witness_verified": self.witness_verified,
            "witness_verify_reason": self.witness_verify_reason,
            "witness_db": self.witness_db,
            "observation": self.observation,
            "verification": self.verification,
            "error": self.error,
        }


class SafeExecutor:
    def __init__(self, *, workspace: Path, runtime_root: Path) -> None:
        self.workspace = workspace.resolve()
        self.runtime_root = runtime_root.resolve()
        self.output_dir = self.runtime_root / "outputs"
        self.execution_dir = self.runtime_root / "executions"
        self.execution_dir.mkdir(parents=True, exist_ok=True)

    def execute(self, plan: PatchPlan) -> ExecutionResult:
        if plan.gate != "APPROVE":
            raise ValueError(f"patch_plan_not_approved:{plan.gate}")
        plan_path = write_patch_plan(self.output_dir, plan)
        diff_path = write_patch_diff(self.output_dir, plan)
        rollback = RollbackStore(workspace=self.workspace, runtime_root=self.runtime_root).capture(plan)
        written: list[str] = []
        test_results: list[dict[str, Any]] = []
        try:
            for operation in plan.operations:
                target = resolve_workspace_text_target(self.workspace, operation.relative_path)
                if operation.changed:
                    target.parent.mkdir(parents=True, exist_ok=True)
                    target.write_text(operation.content, encoding="utf-8")
                    written.append(operation.relative_path)
                if target.suffix.lower() == ".py":
                    py_compile.compile(str(target), doraise=True)
            test_results = [
                run_allowlisted_test_command(command, workspace=self.workspace) for command in plan.test_commands
            ]
            failed_tests = [result for result in test_results if result["returncode"] != 0]
            if failed_tests:
                raise ValueError("test_command_failed:" + failed_tests[0]["command"])
            result = ExecutionResult(
                ok=True,
                plan_id=plan.plan_id,
                changed=plan.changed,
                plan_path=plan_path,
                diff_path=diff_path,
                rollback_path=rollback.path,
                execution_path=self.execution_dir / f"{plan.plan_id}.json",
                written=written,
                test_results=test_results,
                witness_event_id=0,
                witness_verified=False,
                witness_verify_reason="not_recorded",
                witness_db="",
                observation={},
                verification="py_compile_and_tests_passed" if test_results else "py_compile_passed",
            )
        except Exception as exc:
            RollbackStore(workspace=self.workspace, runtime_root=self.runtime_root).restore(rollback.rollback_id)
            result = ExecutionResult(
                ok=False,
                plan_id=plan.plan_id,
                changed=False,
                plan_path=plan_path,
                diff_path=diff_path,
                rollback_path=rollback.path,
                execution_path=self.execution_dir / f"{plan.plan_id}.json",
                written=written,
                test_results=test_results,
                witness_event_id=0,
                witness_verified=False,
                witness_verify_reason="not_recorded",
                witness_db="",
                observation={},
                verification="rollback_after_failed_execution",
                error=str(exc),
            )
        result = self._with_witness(plan, result)
        result.execution_path.write_text(json.dumps(result.to_dict(), indent=2, ensure_ascii=False), encoding="utf-8")
        return result

    def _run_allowlisted_test_command(self, command: str) -> dict[str, Any]:
        return run_allowlisted_test_command(command, workspace=self.workspace)

    def _with_witness(self, plan: PatchPlan, result: ExecutionResult) -> ExecutionResult:
        artifacts = [
            str(result.plan_path),
            str(result.diff_path),
            str(result.rollback_path),
            str(result.execution_path),
        ]
        evidence = [
            f"plan_id={plan.plan_id}",
            f"changed={result.changed}",
            f"written={','.join(result.written) or 'none'}",
            f"verification={result.verification}",
        ]
        if result.error:
            evidence.append(f"error={result.error}")
        observation = ObservationEnvelope(
            prompt=plan.summary,
            intent="patch_apply",
            agent="safe_executor",
            action_gate=plan.gate,
            certainty=["Patch execution was recorded with local artifacts."],
            inference=[],
            unknown=[] if result.ok else ["Patch execution failed and rollback was attempted."],
            artifacts=artifacts,
            evidence=evidence,
        ).finalize()
        witness = WitnessLog(self.runtime_root / "witness" / "wabi_patch_witness.sqlite")
        event_id = witness.append(
            "wabi_patch_execution",
            {
                "plan_id": plan.plan_id,
                "ok": result.ok,
                "changed": result.changed,
                "written": result.written,
                "verification": result.verification,
                "error": result.error,
                "observation_fingerprint": observation.fingerprint,
            },
        )
        witness_ok, witness_reason = witness.verify_chain()
        return ExecutionResult(
            ok=result.ok,
            plan_id=result.plan_id,
            changed=result.changed,
            plan_path=result.plan_path,
            diff_path=result.diff_path,
            rollback_path=result.rollback_path,
            execution_path=result.execution_path,
            written=result.written,
            test_results=result.test_results,
            witness_event_id=event_id,
            witness_verified=witness_ok,
            witness_verify_reason=witness_reason,
            witness_db=str(witness.db_path),
            observation=observation.to_dict(),
            verification=result.verification,
            error=result.error,
        )


def run_allowlisted_test_command(command: str, *, workspace: str | Path, timeout: int = 120) -> dict[str, Any]:
    if any(token in command for token in [";", "&&", "||", "|", ">", "<"]):
        raise ValueError(f"test_command_not_allowlisted:{command}")
    args = shlex.split(command)
    if not args:
        raise ValueError("empty_test_command")
    normalized = list(args)
    executable = Path(normalized[0]).name.lower()
    if executable in {"python", "python.exe", "py", "py.exe"}:
        normalized[0] = sys.executable
    module_args = normalized[1:]
    if module_args[:1] == ["-B"]:
        module_args = module_args[1:]
    allowed = (
        len(normalized) >= 3
        and Path(normalized[0]).name.lower().startswith("python")
        and module_args[:2] in (["-m", "pytest"], ["-m", "py_compile"])
    )
    if not allowed and executable not in {"pytest", "pytest.exe"}:
        raise ValueError(f"test_command_not_allowlisted:{command}")
    proc = subprocess.run(
        normalized,
        cwd=str(Path(workspace).resolve()),
        capture_output=True,
        text=True,
        timeout=timeout,
    )
    return {
        "command": command,
        "args": normalized,
        "returncode": proc.returncode,
        "stdout": redact_text(proc.stdout[-4000:]),
        "stderr": redact_text(proc.stderr[-4000:]),
    }
