import json
import os
import subprocess
import sys
from pathlib import Path

from wabi_sabi.core.safe_test_runner import run_safe_tests


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
        timeout=60,
    )


def make_pytest_project(workspace: Path) -> None:
    (workspace / "pyproject.toml").write_text("[project]\nname='demo'\n", encoding="utf-8")
    tests = workspace / "tests"
    tests.mkdir()
    (tests / "test_demo.py").write_text(
        "def test_demo() -> None:\n    assert 1 + 1 == 2\n",
        encoding="utf-8",
    )


def test_run_safe_tests_executes_allowlisted_plan_and_witnesses(tmp_path):
    runtime = tmp_path / "runtime"
    make_pytest_project(tmp_path)

    payload = run_safe_tests(workspace=tmp_path, runtime_root=runtime)

    assert payload["schema"] == "wabi.safe_test_run.v1"
    assert payload["ok"] is True
    assert payload["policy"]["auto_apply"] is False
    assert payload["policy"]["timeout_seconds"] == 600
    assert payload["summary"]["command_count"] == 1
    assert payload["summary"]["passed"] == 1
    assert payload["summary"]["failed"] == 0
    assert payload["results"][0]["returncode"] == 0
    assert Path(payload["artifact"]).exists()
    assert payload["witness_verified"] is True
    assert Path(payload["witness_db"]).exists()


def test_run_safe_tests_reviews_missing_baseline(tmp_path):
    payload = run_safe_tests(workspace=tmp_path, runtime_root=tmp_path / "runtime")

    assert payload["ok"] is False
    assert payload["gate"] == "REVIEW"
    assert payload["summary"]["command_count"] == 0
    assert payload["plan"]["commands"][0]["command"] == "NO_TEST_BASELINE"
    assert payload["witness_verified"] is True


def test_run_safe_tests_cli(tmp_path):
    make_pytest_project(tmp_path)

    proc = run_cli("run-safe-tests", "--json", workspace=tmp_path, runtime=tmp_path / "runtime")

    assert proc.returncode == 0, proc.stderr
    payload = json.loads(proc.stdout)
    assert payload["ok"] is True
    assert payload["schema"] == "wabi.safe_test_run.v1"
    assert payload["summary"]["passed"] == 1
    assert payload["witness_verified"] is True
