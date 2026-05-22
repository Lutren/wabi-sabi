from __future__ import annotations

import json
from pathlib import Path

from wabi_sabi.core.local_apply_readiness import (
    LOCAL_APPLY_BLOCKED_PATH,
    LOCAL_APPLY_BLOCKED_SECRET,
    LOCAL_APPLY_PATCH_READY,
    LOCAL_APPLY_READY,
    LOCAL_APPLY_TESTS_PASS,
    apply_local_task_spec,
    build_patch_candidate,
    preview_local_apply,
)


def make_workspace(root: Path) -> Path:
    (root / "wabi_sabi" / "core").mkdir(parents=True)
    (root / "tests").mkdir(parents=True)
    (root / "wabi_sabi" / "__init__.py").write_text("", encoding="utf-8")
    (root / "wabi_sabi" / "core" / "__init__.py").write_text("", encoding="utf-8")
    return root


def json_helper_task() -> dict[str, object]:
    return {
        "task_id": "taskspec-json-helper",
        "intent_name": "code_request",
        "summary": "programa un helper seguro para validar json",
        "action_gate": "APPROVE",
        "proposal_only": True,
        "needs_file_write": True,
        "needs_cloud": False,
        "needs_graphics": False,
    }


def test_build_patch_candidate_for_json_helper_is_ready(tmp_path):
    workspace = make_workspace(tmp_path / "workspace")
    candidate = build_patch_candidate(json_helper_task(), workspace=workspace, runtime_root=tmp_path / "runtime")

    assert candidate["readiness"] == LOCAL_APPLY_READY
    assert candidate["affected_paths"] == ["wabi_sabi/core/json_safety.py", "tests/test_json_safety.py"]
    assert candidate["path_allowlist"]["allowed"] is True
    assert candidate["secret_scan"]["status"] == "PASS"
    assert candidate["boundary_scan"]["status"] == "PASS"
    assert candidate["applied_to_sources"] is False
    assert (workspace / "wabi_sabi" / "core" / "json_safety.py").exists() is False


def test_preview_local_apply_does_not_write_sources(tmp_path):
    workspace = make_workspace(tmp_path / "workspace")
    preview = preview_local_apply(json_helper_task(), workspace=workspace, runtime_root=tmp_path / "runtime")

    assert preview["status"] == LOCAL_APPLY_PATCH_READY
    assert preview["applied_to_sources"] is False
    assert preview["cloud_provider_called"] is False
    assert (workspace / "wabi_sabi" / "core" / "json_safety.py").exists() is False


def test_apply_local_task_spec_writes_allowlisted_patch_and_runs_tests(tmp_path):
    workspace = make_workspace(tmp_path / "workspace")
    result = apply_local_task_spec(json_helper_task(), workspace=workspace, runtime_root=tmp_path / "runtime")
    payload = result["result"]

    assert result["ok"] is True
    assert result["status"] == LOCAL_APPLY_TESTS_PASS
    assert payload["applied_to_sources"] is True
    assert payload["execution"]["written"] == ["wabi_sabi/core/json_safety.py", "tests/test_json_safety.py"]
    assert Path(payload["rollback_snapshot"]).exists()
    assert (workspace / "wabi_sabi" / "core" / "json_safety.py").exists()
    assert (workspace / "tests" / "test_json_safety.py").exists()


def test_apply_local_task_spec_accepts_explicit_multi_file_changes(tmp_path):
    workspace = make_workspace(tmp_path / "workspace")
    result = apply_local_task_spec(
        {
            "task_id": "explicit-multi",
            "intent_name": "code_request",
            "changes": [
                {"target": "wabi_sabi/core/example_multi.py", "content": "def value() -> int:\n    return 7\n", "suffix": ".py"},
                {
                    "target": "tests/test_example_multi.py",
                    "content": "from wabi_sabi.core.example_multi import value\n\n\ndef test_value():\n    assert value() == 7\n",
                    "suffix": ".py",
                },
            ],
            "tests_to_run": ["python -B -m pytest tests/test_example_multi.py -q -p no:cacheprovider"],
        },
        workspace=workspace,
        runtime_root=tmp_path / "runtime",
    )

    assert result["ok"] is True
    assert result["status"] == LOCAL_APPLY_TESTS_PASS
    assert (workspace / "wabi_sabi" / "core" / "example_multi.py").exists()
    assert (workspace / "tests" / "test_example_multi.py").exists()


def test_local_apply_blocks_outside_allowlist(tmp_path):
    workspace = make_workspace(tmp_path / "workspace")
    candidate = build_patch_candidate(
        {
            "task_id": "outside",
            "intent_name": "code_request",
            "changes": [{"target": "../outside.py", "content": "print('no')\n"}],
        },
        workspace=workspace,
        runtime_root=tmp_path / "runtime",
    )

    assert candidate["readiness"] == LOCAL_APPLY_BLOCKED_PATH
    assert candidate["applied_to_sources"] is False


def test_local_apply_blocks_secret_like_patch_content(tmp_path):
    workspace = make_workspace(tmp_path / "workspace")
    candidate = build_patch_candidate(
        {
            "task_id": "secret",
            "intent_name": "code_request",
            "changes": [{"target": "wabi_sabi/core/unsafe.py", "content": "API_KEY = 'sk-testsecret1234567890'\n"}],
        },
        workspace=workspace,
        runtime_root=tmp_path / "runtime",
    )
    encoded = json.dumps(candidate, ensure_ascii=False)

    assert candidate["readiness"] == LOCAL_APPLY_BLOCKED_SECRET
    assert "sk-testsecret" not in encoded


def test_failed_required_tests_roll_back_changes(tmp_path):
    workspace = make_workspace(tmp_path / "workspace")
    result = apply_local_task_spec(
        {
            "task_id": "failing-tests",
            "intent_name": "code_request",
            "changes": [{"target": "wabi_sabi/core/temp_patch.py", "content": "VALUE = 1\n"}],
            "tests_to_run": ["python -B -m pytest tests/test_missing.py -q -p no:cacheprovider"],
        },
        workspace=workspace,
        runtime_root=tmp_path / "runtime",
    )

    assert result["ok"] is False
    assert result["status"] == "LOCAL_APPLY_TESTS_FAIL_ROLLED_BACK"
    assert (workspace / "wabi_sabi" / "core" / "temp_patch.py").exists() is False
