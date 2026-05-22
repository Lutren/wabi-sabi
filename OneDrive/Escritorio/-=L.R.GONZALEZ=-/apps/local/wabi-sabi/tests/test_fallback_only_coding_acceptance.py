from __future__ import annotations

import json
from pathlib import Path

from wabi_sabi.core.cloud_debug_loop import run_cloud_debug_loop


REPO_ROOT = Path(__file__).resolve().parents[4]
WABI_ROOT = Path(__file__).resolve().parents[1]
BRAIN_OS_ROOT = REPO_ROOT.parent / "-= BRAIN_OS =-"
RUN_DIR = REPO_ROOT / "qa_artifacts" / "release_validation" / "RUN_WABI_FALLBACK_ONLY_CODING_ACCEPTANCE_v0_2_20260518"
RUNTIME_SANDBOX = Path.home() / ".medioevo" / "wabi" / "runtime" / "coding_acceptance_v0_2"
PROVIDER_STATE = WABI_ROOT / "qa_artifacts" / "FALLBACK_ONLY_PROVIDER_STATE_v0_2.json"
ACCEPTANCE_STATE = RUN_DIR / "FALLBACK_ONLY_CODING_ACCEPTANCE_v0_2.json"
PATCHPLAN = RUN_DIR / "FALLBACK_ONLY_ACCEPTANCE_PATCHPLAN_v0_2.json"
APPLY_RESULT = RUN_DIR / "FALLBACK_ONLY_ACCEPTANCE_APPLY_RESULT_v0_2.json"
TEST_RESULT = RUN_DIR / "FALLBACK_ONLY_ACCEPTANCE_TEST_RESULT_v0_2.json"
WITNESS = RUN_DIR / "FALLBACK_ONLY_ACCEPTANCE_WITNESS_v0_2.jsonl"
UI_INDEX = BRAIN_OS_ROOT / "apps" / "local" / "wabi_ui" / "index.html"


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def test_fallback_only_provider_never_calls_cloud():
    state = load_json(PROVIDER_STATE)
    encoded = json.dumps(state, ensure_ascii=False)

    assert state["cloud_live_gate"] == "BLOCK_THIS_RUN"
    assert state["nvidia_smoke_gate"] == "DO_NOT_CALL"
    assert state["provider_state_preserved"] == "SMOKE_FAIL_REDACTED"
    assert state["cloud_called"] is False
    assert state["workspace_sent_external"] is False
    assert state["secret_values_printed"] is False
    assert "sk-" not in encoded.lower()
    assert "nvapi-" not in encoded.lower()


def test_fallback_only_acceptance_uses_runtime_sandbox():
    state = load_json(ACCEPTANCE_STATE)
    patch_plan = load_json(PATCHPLAN)

    assert state["sandbox"]["path_redacted"] == "<WABI_RUNTIME>/coding_acceptance_v0_2"
    assert state["sandbox"]["scope"] == "runtime"
    assert all(item.startswith("coding_acceptance_v0_2/") for item in state["sandbox"]["written"])
    assert all(
        operation["relative_path"].startswith("coding_acceptance_v0_2/")
        for operation in patch_plan["operations"]
    )


def test_acceptance_patchplan_blocks_out_of_scope_targets(tmp_path):
    runtime = tmp_path / "runtime"
    spec = tmp_path / "task.json"
    spec.write_text(
        json.dumps(
            {
                "schema": "wabi.task_spec.v1",
                "summary": "blocked out of scope acceptance target",
                "target_root": "runtime",
                "changes": [
                    {
                        "operation": "write_text",
                        "target": "../escape.py",
                        "suffix": ".py",
                        "content": "VALUE = 1\n",
                    }
                ],
                "test_commands": [],
            }
        ),
        encoding="utf-8",
    )

    payload = run_cloud_debug_loop(
        workspace=tmp_path / "workspace",
        runtime_root=runtime,
        task_spec_path=spec,
    )

    assert payload["ok"] is False
    assert payload["apply_status"] == "BLOCKED"
    assert payload["error"] == "BLOCK_PATCH_OUT_OF_SCOPE"
    assert payload["cloud_provider_called"] is False


def test_acceptance_dry_run_before_apply():
    state = load_json(ACCEPTANCE_STATE)

    assert state["loop"]["dry_run_before_apply"] is True
    assert state["loop"]["proposal_valid"] is True
    assert state["loop"]["task_spec_valid"] is True
    assert state["loop"]["patch_plan_valid"] is True


def test_acceptance_creates_rollback_before_apply():
    apply_result = load_json(APPLY_RESULT)

    assert apply_result["apply_status"] == "APPLIED"
    assert apply_result["rollback_available"] is True
    assert Path(apply_result["rollback_artifact"]).exists()
    assert apply_result["secret_values_printed"] is False


def test_acceptance_runs_sandbox_tests():
    test_result = load_json(TEST_RESULT)

    assert test_result["ok"] is True
    assert test_result["tests"]["ran"] is True
    assert test_result["tests"]["passed"] is True
    assert test_result["tests"]["results"][0]["returncode"] == 0
    assert "3 passed" in test_result["tests"]["results"][0]["stdout"]


def test_acceptance_rolls_back_on_failure(tmp_path):
    runtime = tmp_path / "runtime"
    runtime.mkdir()
    spec = runtime / "task.json"
    spec.write_text(
        json.dumps(
            {
                "schema": "wabi.task_spec.v1",
                "summary": "acceptance rollback on failed sandbox test",
                "target_root": "runtime",
                "changes": [
                    {
                        "operation": "write_text",
                        "target": "coding_acceptance_failure/temp.py",
                        "suffix": ".py",
                        "content": "VALUE = 1\n",
                    }
                ],
                "test_commands": ["python -m py_compile missing_after_apply.py"],
            }
        ),
        encoding="utf-8",
    )

    payload = run_cloud_debug_loop(
        workspace=tmp_path / "workspace",
        runtime_root=runtime,
        task_spec_path=spec,
        apply_patch=True,
    )

    assert payload["ok"] is False
    assert payload["apply_status"] == "ROLLED_BACK"
    assert payload["rollback_available"] is True
    assert not (runtime / "coding_acceptance_failure" / "temp.py").exists()


def test_acceptance_witness_written():
    line = WITNESS.read_text(encoding="utf-8-sig").strip()
    payload = json.loads(line)

    assert payload["event_id"] == 20
    assert payload["witness_verified"] is True
    assert payload["apply_status"] == "APPLIED"
    assert payload["tests_passed"] is True
    assert payload["cloud_provider_called"] is False


def test_acceptance_panel_data_schema():
    state = load_json(ACCEPTANCE_STATE)

    assert state["schema"] == "wabi.fallback_only_acceptance.result.v0_2"
    assert state["state_fingerprint"] == "WABI-FALLBACK-ONLY-CODING-ACCEPTANCE-v0-2-20260518"
    assert state["provider"]["nvidia_smoke_gate"] == "DO_NOT_CALL"
    assert state["provider"]["cloud_status"] == "SMOKE_FAIL_REDACTED"
    assert state["security"]["publication_gate"] == "BLOCK"


def test_acceptance_panel_no_external_urls():
    text = UI_INDEX.read_text(encoding="utf-8")

    assert "codingAcceptancePanel" in text
    assert "/api/coding-acceptance" in text
    assert "http://" not in text
    assert "https://" not in text
    assert "cdn" not in text.lower()


def test_acceptance_panel_no_secrets():
    text = "\n".join(
        [
            UI_INDEX.read_text(encoding="utf-8"),
            json.dumps(load_json(ACCEPTANCE_STATE), ensure_ascii=False),
            json.dumps(load_json(PROVIDER_STATE), ensure_ascii=False),
        ]
    )

    assert "sk-" not in text.lower()
    assert "nvapi-" not in text.lower()
    assert "-----begin" not in text.lower()
    assert "nvidia_api_key=" not in text.lower()


def test_provider_state_still_do_not_call():
    state = load_json(ACCEPTANCE_STATE)

    assert state["provider"]["next_smoke"] == "DO_NOT_CALL"
    assert state["provider"]["route_status"] == "REVIEW"
    assert state["security"]["cloud_called"] is False
