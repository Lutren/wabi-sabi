import json
import os
import subprocess
import sys
from pathlib import Path

from wabi_sabi.core.project_scan import scan_project


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


def test_project_scan_detects_stack_and_tests_without_secret_content(tmp_path):
    subprocess.run(["git", "init"], cwd=str(tmp_path), check=True, capture_output=True, text=True)
    (tmp_path / "pyproject.toml").write_text("[project]\nname='demo'\n", encoding="utf-8")
    (tmp_path / "package.json").write_text(
        json.dumps({"name": "demo", "scripts": {"test": "vitest", "build": "vite build"}}),
        encoding="utf-8",
    )
    (tmp_path / "tests").mkdir()
    (tmp_path / "tests" / "test_demo.py").write_text("SECRET_SHOULD_NOT_APPEAR = 'hidden'\n", encoding="utf-8")

    payload = scan_project(workspace=tmp_path)
    as_text = json.dumps(payload)

    assert payload["schema"] == "wabi.project_scan.v1"
    assert "python:pyproject" in payload["package_managers"]
    assert "node:package-json" in payload["package_managers"]
    assert {"command": "python -m pytest -q", "source": "python_tests_detected"} in payload["test_commands"]
    assert {"command": "npm run test", "source": "package_json:test"} in payload["test_commands"]
    assert payload["repo_boundaries"]["current_git_root"]
    assert payload["limits"]["content_included"] is False
    assert "SECRET_SHOULD_NOT_APPEAR" not in as_text


def test_project_scan_cli(tmp_path):
    (tmp_path / "requirements.txt").write_text("pytest\n", encoding="utf-8")
    (tmp_path / "tests").mkdir()
    proc = run_cli("project-scan", "--json", workspace=tmp_path, runtime=tmp_path / "runtime")

    assert proc.returncode == 0, proc.stderr
    payload = json.loads(proc.stdout)
    assert payload["ok"] is True
    assert "python:pip" in payload["package_managers"]
    assert payload["test_commands"]
