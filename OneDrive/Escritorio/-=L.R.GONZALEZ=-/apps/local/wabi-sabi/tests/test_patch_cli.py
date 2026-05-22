import json
import os
import subprocess
import sys
from pathlib import Path


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


def test_patch_plan_cli_writes_plan_without_source_change(tmp_path):
    runtime = tmp_path / "runtime"
    proc = run_cli(
        "patch-plan",
        "crea una funcion que lea un archivo y resuma sus lineas",
        "--target",
        "helpers.py",
        "--json",
        workspace=tmp_path,
        runtime=runtime,
    )

    assert proc.returncode == 0, proc.stderr
    payload = json.loads(proc.stdout)
    assert payload["ok"] is True
    assert payload["action"] == "patch_plan"
    assert Path(payload["plan_artifact"]).exists()
    assert not (tmp_path / "helpers.py").exists()


def test_patch_apply_cli_writes_and_rollback_cli_restores(tmp_path):
    runtime = tmp_path / "runtime"
    apply_proc = run_cli(
        "patch-apply",
        "crea una funcion que lea un archivo y resuma sus lineas",
        "--target",
        "helpers.py",
        "--json",
        workspace=tmp_path,
        runtime=runtime,
    )

    assert apply_proc.returncode == 0, apply_proc.stderr
    payload = json.loads(apply_proc.stdout)
    assert payload["ok"] is True
    assert payload["verification"] == "py_compile_passed"
    assert payload["witness_verified"] is True
    assert (tmp_path / "helpers.py").exists()

    rollback_proc = run_cli(
        "rollback",
        payload["plan_id"],
        "--json",
        workspace=tmp_path,
        runtime=runtime,
    )

    assert rollback_proc.returncode == 0, rollback_proc.stderr
    rollback = json.loads(rollback_proc.stdout)
    assert rollback["ok"] is True
    assert rollback["result"]["witness_verified"] is True
    assert "helpers.py" in rollback["result"]["removed"]
    assert not (tmp_path / "helpers.py").exists()


def test_tools_cli_lists_patch_tools(tmp_path):
    proc = run_cli("tools", "--json", workspace=tmp_path, runtime=tmp_path / "runtime")

    assert proc.returncode == 0, proc.stderr
    payload = json.loads(proc.stdout)
    names = {tool["name"] for tool in payload["tools"]}
    assert "safe_execute_patch" in names
    assert "git_worktree_summary" in names
    assert "task_spec_plan" in names


def test_patch_apply_cli_accepts_allowlisted_test_command(tmp_path):
    runtime = tmp_path / "runtime"
    proc = run_cli(
        "patch-apply",
        "crea una funcion que lea un archivo y resuma sus lineas",
        "--target",
        "helpers.py",
        "--test-command",
        "python -m py_compile helpers.py",
        "--json",
        workspace=tmp_path,
        runtime=runtime,
    )

    assert proc.returncode == 0, proc.stderr
    payload = json.loads(proc.stdout)
    assert payload["ok"] is True
    assert payload["verification"] == "py_compile_and_tests_passed"
    assert payload["witness_verified"] is True
    assert payload["test_results"][0]["returncode"] == 0
