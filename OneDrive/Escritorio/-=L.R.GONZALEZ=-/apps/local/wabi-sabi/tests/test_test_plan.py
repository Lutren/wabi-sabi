import json
import os
import subprocess
import sys
from pathlib import Path

from wabi_sabi.core.test_plan import build_test_plan


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


def test_test_plan_uses_project_scan_without_execution(tmp_path):
    (tmp_path / "pyproject.toml").write_text("[project]\nname='demo'\n", encoding="utf-8")
    (tmp_path / "tests").mkdir()

    payload = build_test_plan(workspace=tmp_path)

    assert payload["schema"] == "wabi.test_plan.v1"
    assert payload["ok"] is True
    assert payload["policy"]["auto_execute"] is False
    assert payload["policy"]["auto_apply"] is False
    assert payload["commands"][0]["command"] == "python -m pytest -q"
    assert payload["commands"][0]["gate"] == "APPROVE"


def test_test_plan_reports_no_test_baseline(tmp_path):
    payload = build_test_plan(workspace=tmp_path)

    assert payload["commands"][0]["command"] == "NO_TEST_BASELINE"
    assert payload["commands"][0]["gate"] == "REVIEW"


def test_test_plan_cli(tmp_path):
    (tmp_path / "requirements.txt").write_text("pytest\n", encoding="utf-8")
    (tmp_path / "tests").mkdir()
    proc = run_cli("test-plan", "--json", workspace=tmp_path, runtime=tmp_path / "runtime")

    assert proc.returncode == 0, proc.stderr
    payload = json.loads(proc.stdout)
    assert payload["schema"] == "wabi.test_plan.v1"
    assert payload["commands"][0]["command"] == "python -m pytest -q"
