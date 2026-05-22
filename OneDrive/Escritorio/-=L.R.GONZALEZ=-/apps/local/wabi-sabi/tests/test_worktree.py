import json
import os
import subprocess
import sys
from pathlib import Path

from wabi_sabi.core.worktree import git_worktree_summary
from wabi_sabi.cli.main import execute_auto_prompt


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


def test_git_worktree_summary_reports_untracked_without_file_content(tmp_path):
    subprocess.run(["git", "init"], cwd=str(tmp_path), check=True, capture_output=True, text=True)
    (tmp_path / "notes.txt").write_text("secret-looking-value-not-to-print", encoding="utf-8")

    payload = git_worktree_summary(tmp_path)

    assert payload["ok"] is True
    assert payload["dirty"] is True
    assert "notes.txt" in payload["untracked"]
    assert "secret-looking-value-not-to-print" not in json.dumps(payload)
    assert payload["limits"]["content_included"] is False


def test_worktree_status_cli_is_read_only(tmp_path):
    subprocess.run(["git", "init"], cwd=str(tmp_path), check=True, capture_output=True, text=True)
    (tmp_path / "notes.txt").write_text("hello", encoding="utf-8")

    proc = run_cli("worktree-status", "--json", workspace=tmp_path, runtime=tmp_path / "runtime")

    assert proc.returncode == 0, proc.stderr
    payload = json.loads(proc.stdout)
    assert payload["ok"] is True
    assert payload["status_count"] >= 1
    assert "notes.txt" in payload["untracked"]


def test_auto_status_includes_worktree_summary(tmp_path):
    subprocess.run(["git", "init"], cwd=str(tmp_path), check=True, capture_output=True, text=True)
    (tmp_path / "notes.txt").write_text("hello", encoding="utf-8")

    payload = execute_auto_prompt("/status", workspace=tmp_path, runtime_root=tmp_path / "runtime")

    assert payload["ok"] is True
    assert payload["payload"]["worktree"]["ok"] is True
    assert "Worktree:" in payload["output"]
