import json
import os
import subprocess
import sys
from pathlib import Path

from wabi_sabi.core.rollback_store import RollbackStore
from wabi_sabi.core.safe_executor import SafeExecutor
from wabi_sabi.core.task_spec_planner import build_patch_plan_from_task_spec, load_task_spec


APP_ROOT = Path(__file__).resolve().parents[1]


def run_cli(*args, workspace: Path, runtime: Path):
    env = os.environ.copy()
    env["PYTHONPATH"] = str(APP_ROOT)
    return subprocess.run(
        [
            sys.executable,
            "-m",
            "wabi_sabi.cli.main",
            *args,
            "--workspace",
            str(workspace),
            "--runtime",
            str(runtime),
        ],
        cwd=str(APP_ROOT),
        env=env,
        text=True,
        capture_output=True,
        timeout=30,
    )


def write_spec(path: Path, *, test_commands: list[str] | None = None) -> Path:
    spec = {
        "schema": "wabi.task_spec.v1",
        "summary": "create helper and tests from explicit spec",
        "changes": [
            {
                "target": "helpers.py",
                "suffix": ".py",
                "content": "def answer() -> int:\n    return 42\n",
            },
            {
                "target": "test_helpers.py",
                "suffix": ".py",
                "content": "from helpers import answer\n\n\ndef test_answer():\n    assert answer() == 42\n",
            },
        ],
        "test_commands": test_commands or ["python -m pytest test_helpers.py -q"],
    }
    path.write_text(json.dumps(spec, indent=2), encoding="utf-8")
    return path


def test_task_spec_planner_builds_multi_file_patch_plan(tmp_path):
    spec_path = write_spec(tmp_path / "wabi_task_spec.json")

    spec, plan = build_patch_plan_from_task_spec(workspace=tmp_path, spec_path=spec_path)

    assert spec.summary == "create helper and tests from explicit spec"
    assert [operation.relative_path for operation in plan.operations] == ["helpers.py", "test_helpers.py"]
    assert plan.test_commands == ["python -m pytest test_helpers.py -q"]


def test_task_spec_apply_executes_tests_and_rolls_back(tmp_path):
    spec_path = write_spec(tmp_path / "wabi_task_spec.json")
    _, plan = build_patch_plan_from_task_spec(workspace=tmp_path, spec_path=spec_path)

    execution = SafeExecutor(workspace=tmp_path, runtime_root=tmp_path / "runtime").execute(plan)

    assert execution.ok is True
    assert execution.verification == "py_compile_and_tests_passed"
    assert sorted(execution.written) == ["helpers.py", "test_helpers.py"]

    rollback = RollbackStore(workspace=tmp_path, runtime_root=tmp_path / "runtime").restore(execution.plan_id)
    assert sorted(rollback["removed"]) == ["helpers.py", "test_helpers.py"]


def test_task_spec_rejects_sensitive_target(tmp_path):
    spec = {
        "schema": "wabi.task_spec.v1",
        "summary": "bad target",
        "changes": [{"target": ".env/helpers.py", "suffix": ".py", "content": "x = 1\n"}],
    }
    spec_path = tmp_path / "bad.json"
    spec_path.write_text(json.dumps(spec), encoding="utf-8")

    try:
        build_patch_plan_from_task_spec(workspace=tmp_path, spec_path=spec_path)
    except ValueError as exc:
        assert "target_path_blocked" in str(exc)
    else:
        raise AssertionError("sensitive target was not blocked")


def test_task_spec_rejects_spec_outside_workspace(tmp_path):
    outside = tmp_path.parent / "outside_wabi_spec.json"
    outside.write_text(json.dumps({"summary": "outside", "changes": []}), encoding="utf-8")

    try:
        load_task_spec(workspace=tmp_path, spec_path=outside)
    except ValueError as exc:
        assert "target_outside_workspace" in str(exc)
    else:
        raise AssertionError("outside spec was not blocked")


def test_task_spec_plan_cli_does_not_touch_sources(tmp_path):
    spec_path = write_spec(tmp_path / "wabi_task_spec.json")
    proc = run_cli("task-spec-plan", str(spec_path), "--json", workspace=tmp_path, runtime=tmp_path / "runtime")

    assert proc.returncode == 0, proc.stderr
    payload = json.loads(proc.stdout)
    assert payload["ok"] is True
    assert payload["operations"] == ["helpers.py", "test_helpers.py"]
    assert Path(payload["plan_artifact"]).exists()
    assert not (tmp_path / "helpers.py").exists()


def test_task_spec_apply_cli_runs_tests_and_witness(tmp_path):
    spec_path = write_spec(
        tmp_path / "wabi_task_spec.json",
        test_commands=["python -m py_compile helpers.py test_helpers.py"],
    )
    proc = run_cli("task-spec-apply", str(spec_path), "--json", workspace=tmp_path, runtime=tmp_path / "runtime")

    assert proc.returncode == 0, proc.stderr
    payload = json.loads(proc.stdout)
    assert payload["ok"] is True
    assert payload["verification"] == "py_compile_and_tests_passed"
    assert payload["witness_verified"] is True
    assert sorted(payload["written"]) == ["helpers.py", "test_helpers.py"]
