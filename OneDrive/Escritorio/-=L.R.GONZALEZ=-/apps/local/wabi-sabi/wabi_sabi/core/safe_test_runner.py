from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from wabi_sabi.core.bridge import WitnessLog
from wabi_sabi.core.observation import ObservationEnvelope
from wabi_sabi.core.safe_executor import run_allowlisted_test_command
from wabi_sabi.core.test_plan import build_test_plan
from wabi_sabi.core.tools import stamp


SAFE_TEST_RUN_SCHEMA = "wabi.safe_test_run.v1"
DEFAULT_SAFE_TEST_TIMEOUT = 600


def run_safe_tests(*, workspace: str | Path, runtime_root: str | Path, timeout: int = DEFAULT_SAFE_TEST_TIMEOUT) -> dict[str, Any]:
    workspace_path = Path(workspace).resolve()
    runtime_path = Path(runtime_root).resolve()
    plan = build_test_plan(workspace=workspace_path)
    runnable = [
        item
        for item in plan.get("commands", [])
        if item.get("gate") == "APPROVE" and item.get("command") != "NO_TEST_BASELINE"
    ]
    results: list[dict[str, Any]] = []
    errors: list[str] = []
    for item in runnable:
        command = item["command"]
        try:
            result = run_allowlisted_test_command(command, workspace=workspace_path, timeout=timeout)
        except Exception as exc:
            result = {
                "command": command,
                "args": [],
                "returncode": -1,
                "stdout": "",
                "stderr": "",
                "error": str(exc),
            }
        if result.get("returncode") != 0:
            errors.append(f"{command}:returncode={result.get('returncode')}")
        results.append(result)

    gate = "APPROVE" if runnable else "REVIEW"
    ok = bool(runnable) and not errors
    payload: dict[str, Any] = {
        "schema": SAFE_TEST_RUN_SCHEMA,
        "ok": ok,
        "action": "run_safe_tests",
        "gate": gate if ok else "REVIEW",
        "workspace": str(workspace_path),
        "policy": {
            "auto_apply": False,
            "source_writes": False,
            "allowlist": "python -m pytest, python -m py_compile, pytest",
            "timeout_seconds": timeout,
        },
        "plan": plan,
        "results": results,
        "summary": {
            "command_count": len(runnable),
            "passed": sum(1 for result in results if result.get("returncode") == 0),
            "failed": sum(1 for result in results if result.get("returncode") != 0),
            "errors": errors,
        },
        "artifact": "",
        "witness_event_id": 0,
        "witness_verified": False,
        "witness_verify_reason": "not_recorded",
        "witness_db": "",
        "observation": {},
    }
    artifact = _write_run_artifact(runtime_path, payload)
    payload["artifact"] = str(artifact)
    observation = ObservationEnvelope(
        prompt="run-safe-tests",
        intent="test_verification",
        agent="safe_test_runner",
        action_gate=payload["gate"],
        certainty=["Allowlisted test commands were evaluated from test-plan."],
        inference=[],
        unknown=[] if ok else ["One or more tests failed or no test baseline was detected."],
        artifacts=[str(artifact)],
        evidence=[
            f"command_count={payload['summary']['command_count']}",
            f"passed={payload['summary']['passed']}",
            f"failed={payload['summary']['failed']}",
        ],
    ).finalize()
    witness = WitnessLog(runtime_path / "witness" / "wabi_patch_witness.sqlite")
    event_id = witness.append(
        "wabi_safe_test_run",
        {
            "ok": ok,
            "artifact": str(artifact),
            "command_count": payload["summary"]["command_count"],
            "passed": payload["summary"]["passed"],
            "failed": payload["summary"]["failed"],
            "observation_fingerprint": observation.fingerprint,
        },
    )
    witness_ok, witness_reason = witness.verify_chain()
    payload.update(
        {
            "witness_event_id": event_id,
            "witness_verified": witness_ok,
            "witness_verify_reason": witness_reason,
            "witness_db": str(witness.db_path),
            "observation": observation.to_dict(),
        }
    )
    artifact.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    return payload


def _write_run_artifact(runtime_root: Path, payload: dict[str, Any]) -> Path:
    output_dir = runtime_root / "outputs"
    output_dir.mkdir(parents=True, exist_ok=True)
    path = output_dir / f"safe_test_run_{stamp()}.json"
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    return path
