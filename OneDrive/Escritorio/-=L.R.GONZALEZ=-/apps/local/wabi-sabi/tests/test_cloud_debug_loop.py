from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from wabi_sabi.core.cloud_debug_loop import run_cloud_debug_loop


def run_cli(*args, workspace: Path, runtime: Path):
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
        cwd=workspace,
        text=True,
        capture_output=True,
        check=False,
    )


def write_task_spec(
    path: Path,
    *,
    target: str = "generated/debug_loop.py",
    content: str = "VALUE = 1\n",
    test_commands=None,
    target_root: str | None = None,
) -> Path:
    payload = {
        "schema": "wabi.task_spec.v1",
        "summary": "debug loop test spec",
        "changes": [
            {
                "operation": "write_text",
                "target": target,
                "suffix": ".py",
                "content": content,
            }
        ],
        "test_commands": list(test_commands or []),
    }
    if target_root:
        payload["target_root"] = target_root
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return path


def test_cloud_debug_loop_dry_run_default(tmp_path):
    runtime = tmp_path / "runtime"
    spec = write_task_spec(tmp_path / "task.json")

    proc = run_cli("cloud-debug-loop", "--task", str(spec), "--json", workspace=tmp_path, runtime=runtime)
    payload = json.loads(proc.stdout)

    assert proc.returncode == 0
    assert payload["ok"] is True
    assert payload["mode"] == "dry_run"
    assert payload["workspace_scope"] == "workspace"
    assert payload["patch_plan_valid"] is True
    assert payload["apply_status"] == "NOT_APPLIED"
    assert payload["rollback_available"] is True
    assert Path(payload["witness_path"]).exists()
    assert not (tmp_path / "generated" / "debug_loop.py").exists()


def test_cloud_debug_loop_blocks_out_of_scope_patch(tmp_path):
    payload = run_cloud_debug_loop(
        workspace=tmp_path,
        runtime_root=tmp_path / "runtime",
        task_spec_path=write_task_spec(tmp_path / "task.json", target="../escape.py"),
    )

    assert payload["ok"] is False
    assert payload["apply_status"] == "BLOCKED"
    assert payload["error"] == "BLOCK_PATCH_OUT_OF_SCOPE"
    assert payload["secret_values_printed"] is False


def test_cloud_debug_loop_blocks_runtime_target_inside_workspace(tmp_path):
    payload = run_cloud_debug_loop(
        workspace=tmp_path,
        runtime_root=tmp_path / "external_runtime",
        task_spec_path=write_task_spec(tmp_path / "task.json", target="runtime/blocked.py"),
    )

    assert payload["ok"] is False
    assert payload["apply_status"] == "BLOCKED"
    assert payload["error"] == "BLOCK_PATCH_OUT_OF_SCOPE"
    assert secret_values_not_printed(payload)


def test_cloud_debug_loop_rolls_back_on_test_failure(tmp_path):
    target = tmp_path / "generated" / "rollback_me.py"
    spec = write_task_spec(
        tmp_path / "task.json",
        target="generated/rollback_me.py",
        content="VALUE = 2\n",
        test_commands=["python -m py_compile missing_after_apply.py"],
    )

    payload = run_cloud_debug_loop(
        workspace=tmp_path,
        runtime_root=tmp_path / "runtime",
        task_spec_path=spec,
        apply_patch=True,
    )

    assert payload["ok"] is False
    assert payload["apply_status"] == "ROLLED_BACK"
    assert payload["rollback_available"] is True
    assert payload["tests"]["ran"] is True
    assert payload["tests"]["passed"] is False
    assert not target.exists()


def test_cloud_debug_loop_stderr_redacted(tmp_path, monkeypatch):
    secret = "debug-loop-secret-value-1234567890"
    monkeypatch.setenv("NVIDIA_API_KEY", secret)
    tests_dir = tmp_path / "tests"
    tests_dir.mkdir()
    (tests_dir / "test_secret_output.py").write_text(
        "import os\n\n"
        "def test_secret_output():\n"
        "    assert False, os.environ['NVIDIA_API_KEY']\n",
        encoding="utf-8",
    )
    spec = write_task_spec(
        tmp_path / "task.json",
        target="generated/redacted.py",
        content="VALUE = 3\n",
        test_commands=["python -m pytest tests/test_secret_output.py -q"],
    )

    payload = run_cloud_debug_loop(
        workspace=tmp_path,
        runtime_root=tmp_path / "runtime",
        task_spec_path=spec,
        apply_patch=True,
    )
    text = json.dumps(payload, ensure_ascii=False)

    assert payload["ok"] is False
    assert payload["apply_status"] == "ROLLED_BACK"
    assert payload["secret_values_printed"] is False
    assert secret not in text
    assert "REDACTED" in text


def test_cloud_debug_loop_apply_runtime_scope(tmp_path):
    runtime = tmp_path / "runtime"
    spec = write_task_spec(
        runtime / "safe_cloud_debug_task_v0_4.json",
        target="debug_loop_v0_4/runtime_demo.py",
        content="VALUE = 4\n",
        test_commands=["python -m py_compile debug_loop_v0_4/runtime_demo.py"],
        target_root="runtime",
    )

    payload = run_cloud_debug_loop(
        workspace=tmp_path / "workspace",
        runtime_root=runtime,
        task_spec_path=spec,
        apply_patch=True,
    )

    assert payload["ok"] is True
    assert payload["workspace_scope"] == "runtime"
    assert payload["apply_status"] == "APPLIED"
    assert payload["rollback_available"] is True
    assert payload["tests"]["ran"] is True
    assert payload["tests"]["passed"] is True
    assert (runtime / "debug_loop_v0_4" / "runtime_demo.py").exists()
    assert not (tmp_path / "workspace" / "debug_loop_v0_4" / "runtime_demo.py").exists()


def secret_values_not_printed(payload: dict) -> bool:
    return payload["secret_values_printed"] is False
