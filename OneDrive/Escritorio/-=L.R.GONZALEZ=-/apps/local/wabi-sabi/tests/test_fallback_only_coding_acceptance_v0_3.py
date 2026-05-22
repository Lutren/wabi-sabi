from __future__ import annotations

import json
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[4]
WABI_ROOT = Path(__file__).resolve().parents[1]
RUN_DIR = REPO_ROOT / "qa_artifacts" / "release_validation" / "RUN_WABI_FALLBACK_ONLY_CODING_ACCEPTANCE_v0_3_20260518"
RUNTIME_SANDBOX = Path.home() / ".medioevo" / "wabi" / "runtime" / "coding_acceptance_v0_3"
PROVIDER_STATE = WABI_ROOT / "qa_artifacts" / "FALLBACK_ONLY_PROVIDER_STATE_v0_3.json"
BASELINE = RUN_DIR / "FALLBACK_ONLY_ACCEPTANCE_BASELINE_v0_3.json"
INITIAL_FAILURE = RUN_DIR / "FALLBACK_ONLY_ACCEPTANCE_INITIAL_FAILURE_v0_3.json"
TASKSPEC = RUN_DIR / "FALLBACK_ONLY_ACCEPTANCE_TASKSPEC_v0_3.json"
PATCHPLAN = RUN_DIR / "FALLBACK_ONLY_ACCEPTANCE_PATCHPLAN_v0_3.json"
DRY_RUN = RUN_DIR / "FALLBACK_ONLY_ACCEPTANCE_DRY_RUN_v0_3.json"
APPLY_RESULT = RUN_DIR / "FALLBACK_ONLY_ACCEPTANCE_APPLY_RESULT_v0_3.json"
TEST_RESULT = RUN_DIR / "FALLBACK_ONLY_ACCEPTANCE_TEST_RESULT_v0_3.json"
STATE = RUN_DIR / "FALLBACK_ONLY_CODING_ACCEPTANCE_v0_3.json"
DIFF_SUMMARY = RUN_DIR / "FALLBACK_ONLY_ACCEPTANCE_DIFF_SUMMARY_v0_3.md"
WITNESS = RUN_DIR / "FALLBACK_ONLY_ACCEPTANCE_WITNESS_v0_3.jsonl"


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def test_acceptance_v03_creates_realistic_multifile_fixture():
    expected = [
        "src/metrics.py",
        "src/gates.py",
        "src/report.py",
        "tests/test_metrics.py",
        "tests/test_gates.py",
        "tests/test_report.py",
    ]

    assert RUNTIME_SANDBOX.exists()
    for relative in expected:
        assert (RUNTIME_SANDBOX / relative).exists(), relative

    baseline = load_json(BASELINE)
    assert baseline["intentional_bug"].startswith("weighted_average")
    assert baseline["provider_state"] == "SMOKE_FAIL_REDACTED"


def test_acceptance_v03_initial_tests_fail_expected():
    failure = load_json(INITIAL_FAILURE)

    assert failure["expected_failure"] is True
    assert failure["returncode"] == 1
    assert failure["tests"]["failed"] == 1
    assert failure["tests"]["passed"] == 6
    assert failure["tests"]["failure"] == "test_weighted_average_uses_sum_of_weights"


def test_acceptance_v03_patchplan_only_sandbox_targets():
    patch_plan = load_json(PATCHPLAN)
    task_spec = load_json(TASKSPEC)

    assert patch_plan["gate"] == "APPROVE"
    assert patch_plan["operations"]
    assert all(
        operation["relative_path"].startswith("coding_acceptance_v0_3/")
        for operation in patch_plan["operations"]
    )
    assert all(change["target"].startswith("coding_acceptance_v0_3/") for change in task_spec["changes"])


def test_acceptance_v03_dry_run_before_apply():
    dry_run = load_json(DRY_RUN)
    state = load_json(STATE)

    assert dry_run["mode"] == "dry_run"
    assert dry_run["apply_status"] == "NOT_APPLIED"
    assert dry_run["patch_plan_valid"] is True
    assert state["loop"]["dry_run_before_apply"] is True


def test_acceptance_v03_rollback_snapshot_before_apply():
    dry_run = load_json(DRY_RUN)
    apply_result = load_json(APPLY_RESULT)

    assert dry_run["rollback_available"] is True
    assert Path(dry_run["rollback_artifact"]).exists()
    assert apply_result["rollback_available"] is True
    assert Path(apply_result["rollback_artifact"]).exists()


def test_acceptance_v03_final_tests_pass():
    test_result = load_json(TEST_RESULT)
    state = load_json(STATE)

    assert test_result["ok"] is True
    assert test_result["final_tests"]["passed"] is True
    assert "7 passed" in test_result["final_tests"]["results"][0]["stdout"]
    assert state["loop"]["tests_passed"] is True


def test_acceptance_v03_witness_written():
    payload = json.loads(WITNESS.read_text(encoding="utf-8-sig").strip())
    state = load_json(STATE)

    assert payload["event_id"] == state["loop"]["witness_event_id"]
    assert payload["witness_verified"] is True
    assert payload["cloud_provider_called"] is False
    assert payload["nvidia_smoke_gate"] == "DO_NOT_CALL"


def test_acceptance_v03_diff_summary_exists():
    text = DIFF_SUMMARY.read_text(encoding="utf-8-sig")

    assert "weighted_average" in text
    assert "sum(weights)" in text
    assert "7 passed" in text
    assert "DO_NOT_CALL" in text


def test_acceptance_v03_no_cloud_call():
    provider_state = load_json(PROVIDER_STATE)
    dry_run = load_json(DRY_RUN)
    apply_result = load_json(APPLY_RESULT)
    state = load_json(STATE)

    assert provider_state["cloud_called"] is False
    assert dry_run["cloud_provider_called"] is False
    assert apply_result["cloud_provider_called"] is False
    assert state["security"]["cloud_called"] is False


def test_acceptance_v03_provider_state_do_not_call():
    provider_state = load_json(PROVIDER_STATE)
    state = load_json(STATE)

    assert provider_state["nvidia_smoke_gate"] == "DO_NOT_CALL"
    assert provider_state["provider_state"] == "SMOKE_FAIL_REDACTED"
    assert state["provider"]["nvidia_smoke_gate"] == "DO_NOT_CALL"
    assert state["provider"]["cloud_status"] == "SMOKE_FAIL_REDACTED"


def test_acceptance_outputs_no_secrets():
    paths = [
        PROVIDER_STATE,
        BASELINE,
        INITIAL_FAILURE,
        TASKSPEC,
        PATCHPLAN,
        DRY_RUN,
        APPLY_RESULT,
        TEST_RESULT,
        STATE,
        DIFF_SUMMARY,
        WITNESS,
    ]
    text = "\n".join(path.read_text(encoding="utf-8-sig") for path in paths)
    lowered = text.lower()

    assert "sk-" not in lowered
    assert "nvapi-" not in lowered
    assert "-----begin" not in lowered
    assert "nvidia_api_key=" not in lowered
    assert "smoke_pass" not in lowered

