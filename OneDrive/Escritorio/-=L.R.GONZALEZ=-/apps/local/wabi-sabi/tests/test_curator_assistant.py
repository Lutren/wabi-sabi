import json
import os
import subprocess
import sys
from pathlib import Path

from wabi_sabi.core.curator_assistant import build_curator_assistant_report, run_curator_assistant


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
        timeout=45,
    )


def make_dirty_workspace(workspace: Path) -> None:
    subprocess.run(["git", "init"], cwd=str(workspace), check=True, capture_output=True, text=True)
    (workspace / "pyproject.toml").write_text("[project]\nname='demo'\n", encoding="utf-8")
    (workspace / "runtime" / "outputs").mkdir(parents=True)
    (workspace / "runtime" / "outputs" / "previous.json").write_text("{}", encoding="utf-8")
    (workspace / "__pycache__").mkdir()
    (workspace / "__pycache__" / "demo.pyc").write_bytes(b"cache")
    (workspace / "SESSION_FINGERPRINT.json").write_text("{}", encoding="utf-8")
    (workspace / "scratch.tmp").write_text("temporary", encoding="utf-8")
    (workspace / "notes").mkdir()
    (workspace / "notes" / "idea.md").write_text("# idea\n", encoding="utf-8")


def test_curator_assistant_report_is_dry_run_and_teaches_order(tmp_path):
    make_dirty_workspace(tmp_path)

    payload = run_curator_assistant(workspace=tmp_path, runtime_root=tmp_path / "runtime")

    assert payload["schema"] == "wabi.curator_assistant_report.v1"
    assert payload["ok"] is True
    assert payload["mode"] == "dry_run_only"
    assert payload["policy"]["delete_files"] is False
    assert payload["policy"]["move_files"] is False
    assert payload["policy"]["git_stage"] is False
    assert payload["policy"]["read_file_contents"] is False
    assert payload["cleanup_plan"]["cleanup_performed"] is False
    assert payload["cleanup_plan"]["delete_approved_count"] == 0
    assert payload["assistant_contract"]["name"] == "curador_orden_assistant"
    assert "delete files" in payload["assistant_contract"]["never_does"]
    assert payload["teaching"]["rules"]
    assert Path(payload["artifact"]).exists()
    assert Path(payload["markdown_artifact"]).exists()
    assert payload["witness_verified"] is True
    assert not any(item["decision"] == "DELETE_APPROVED_AFTER_HASH" for item in payload["candidates"])


def test_curator_assistant_classifies_cache_handoff_and_unknown(tmp_path):
    make_dirty_workspace(tmp_path)

    payload = build_curator_assistant_report(workspace=tmp_path, max_items=80)
    categories = {item["category"] for item in payload["candidates"]}

    assert "CACHE_OR_BUILD_REVIEW" in categories
    assert "HANDOFF_EVIDENCE" in categories
    assert "ROOT_LOOSE_REVIEW" in categories or "UNTRACKED_REVIEW" in categories
    assert payload["summary"]["safe_cleanup_performed"] is False
    assert payload["cleanup_plan"]["candidate_delete_count"] >= 1


def test_curator_assistant_cli(tmp_path):
    make_dirty_workspace(tmp_path)

    proc = run_cli("curator-assistant", "--json", workspace=tmp_path, runtime=tmp_path / "runtime")

    assert proc.returncode == 0, proc.stderr
    payload = json.loads(proc.stdout)
    assert payload["schema"] == "wabi.curator_assistant_report.v1"
    assert payload["ok"] is True
    assert payload["artifact"]
    assert payload["summary"]["safe_cleanup_performed"] is False
    assert payload["witness_verified"] is True
