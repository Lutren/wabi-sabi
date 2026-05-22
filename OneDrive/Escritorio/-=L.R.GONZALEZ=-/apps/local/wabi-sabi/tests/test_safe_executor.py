import json
from pathlib import Path

from wabi_sabi.core.patch_planner import build_file_patch_plan, build_multi_file_patch_plan
from wabi_sabi.core.rollback_store import RollbackStore
from wabi_sabi.core.safe_executor import SafeExecutor
from wabi_sabi.core.tool_registry import tool_registry_payload


def test_safe_executor_applies_plan_and_rolls_back_created_file(tmp_path):
    runtime = tmp_path / "runtime"
    plan = build_file_patch_plan(
        workspace=tmp_path,
        target="helpers.py",
        content="def answer() -> int:\n    return 42\n",
        summary="create helper",
        suffix=".py",
    )

    execution = SafeExecutor(workspace=tmp_path, runtime_root=runtime).execute(plan)

    assert execution.ok is True
    assert (tmp_path / "helpers.py").read_text(encoding="utf-8").strip().endswith("return 42")
    assert execution.diff_path.exists()
    assert execution.rollback_path.exists()
    assert execution.execution_path.exists()
    assert execution.witness_verified is True
    assert Path(execution.witness_db).exists()
    assert execution.observation["fingerprint"]

    rollback = RollbackStore(workspace=tmp_path, runtime_root=runtime).restore(execution.plan_id)

    assert rollback["ok"] is True
    assert rollback["witness_verified"] is True
    assert "helpers.py" in rollback["removed"]
    assert not (tmp_path / "helpers.py").exists()


def test_safe_executor_rolls_back_existing_file_content(tmp_path):
    runtime = tmp_path / "runtime"
    target = tmp_path / "helpers.py"
    target.write_text("def answer() -> int:\n    return 1\n", encoding="utf-8")
    plan = build_file_patch_plan(
        workspace=tmp_path,
        target="helpers.py",
        content="def answer() -> int:\n    return 2\n",
        summary="change helper",
        suffix=".py",
    )

    execution = SafeExecutor(workspace=tmp_path, runtime_root=runtime).execute(plan)
    rollback = RollbackStore(workspace=tmp_path, runtime_root=runtime).restore(execution.rollback_path)

    assert rollback["restored"] == ["helpers.py"]
    assert "return 1" in target.read_text(encoding="utf-8")


def test_safe_executor_rejects_sensitive_target(tmp_path):
    blocked = tmp_path / ".env" / "helpers.py"
    blocked.parent.mkdir()

    try:
        build_file_patch_plan(
            workspace=tmp_path,
            target=blocked,
            content="def answer():\n    return 1\n",
            summary="blocked",
            suffix=".py",
        )
    except ValueError as exc:
        assert "target_path_blocked" in str(exc)
    else:
        raise AssertionError("sensitive path was not rejected")


def test_tool_registry_exposes_safe_patch_and_rollback_tools():
    payload = tool_registry_payload()
    names = {tool["name"] for tool in payload["tools"]}

    assert {"patch_plan", "safe_execute_patch", "rollback", "pytest"}.issubset(names)
    assert "rm_rf" not in names
    assert "large destructive delete" in payload["blocked_patterns"]


def test_execution_record_is_json(tmp_path):
    runtime = tmp_path / "runtime"
    plan = build_file_patch_plan(
        workspace=tmp_path,
        target="helpers.py",
        content="def answer() -> int:\n    return 7\n",
        summary="create helper",
        suffix=".py",
    )

    execution = SafeExecutor(workspace=tmp_path, runtime_root=runtime).execute(plan)
    data = json.loads(Path(execution.execution_path).read_text(encoding="utf-8"))

    assert data["schema"] == "wabi.safe_execution_result.v1"
    assert data["verification"] == "py_compile_passed"
    assert data["witness_verified"] is True
    assert data["observation"]["intent"] == "patch_apply"


def test_safe_executor_applies_multi_file_plan_and_runs_allowlisted_tests(tmp_path):
    runtime = tmp_path / "runtime"
    plan = build_multi_file_patch_plan(
        workspace=tmp_path,
        summary="create helper and test",
        changes=[
            {
                "target": "helpers.py",
                "content": "def answer() -> int:\n    return 42\n",
                "suffix": ".py",
            },
            {
                "target": "test_helpers.py",
                "content": "from helpers import answer\n\n\ndef test_answer():\n    assert answer() == 42\n",
                "suffix": ".py",
            },
        ],
        test_commands=["python -m pytest test_helpers.py -q"],
    )

    execution = SafeExecutor(workspace=tmp_path, runtime_root=runtime).execute(plan)

    assert execution.ok is True
    assert execution.verification == "py_compile_and_tests_passed"
    assert execution.witness_verified is True
    assert execution.test_results[0]["returncode"] == 0
    assert sorted(execution.written) == ["helpers.py", "test_helpers.py"]

    rollback = RollbackStore(workspace=tmp_path, runtime_root=runtime).restore(execution.plan_id)
    assert sorted(rollback["removed"]) == ["helpers.py", "test_helpers.py"]


def test_safe_executor_rolls_back_when_test_command_fails(tmp_path):
    runtime = tmp_path / "runtime"
    plan = build_file_patch_plan(
        workspace=tmp_path,
        target="helpers.py",
        content="def answer() -> int:\n    return 42\n",
        summary="create helper with failing verification",
        suffix=".py",
        test_commands=["python -m pytest missing_test_file.py -q"],
    )

    execution = SafeExecutor(workspace=tmp_path, runtime_root=runtime).execute(plan)

    assert execution.ok is False
    assert execution.verification == "rollback_after_failed_execution"
    assert execution.witness_verified is True
    assert "test_command_failed" in execution.error
    assert not (tmp_path / "helpers.py").exists()


def test_safe_executor_rejects_shell_composition_in_test_command(tmp_path):
    runtime = tmp_path / "runtime"
    plan = build_file_patch_plan(
        workspace=tmp_path,
        target="helpers.py",
        content="def answer() -> int:\n    return 42\n",
        summary="unsafe command",
        suffix=".py",
        test_commands=["python -m pytest -q; echo bad"],
    )

    execution = SafeExecutor(workspace=tmp_path, runtime_root=runtime).execute(plan)

    assert execution.ok is False
    assert "test_command_not_allowlisted" in execution.error
    assert execution.witness_verified is True
    assert not (tmp_path / "helpers.py").exists()
