import json
import os
import subprocess
import sys
from pathlib import Path

from wabi_sabi.core.bridge import WitnessLog
from wabi_sabi.core.operator_panel import build_operator_panel


APP_ROOT = Path(__file__).resolve().parents[1]


def run_cli(*args, workspace: Path, runtime: Path):
    env = os.environ.copy()
    env["PYTHONPATH"] = str(APP_ROOT)
    env["WABI_PROVIDER_ORDER"] = "codex,dry-run"
    env["WABI_DISABLE_BASE_MODEL"] = "1"
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


def write_spec(workspace: Path) -> Path:
    spec = {
        "schema": "wabi.task_spec.v1",
        "summary": "operator panel smoke spec",
        "changes": [
            {
                "operation": "write_text",
                "target": "examples/operator_answer.py",
                "suffix": ".py",
                "content": "def answer() -> int:\n    return 42\n",
            }
        ],
        "test_commands": ["python -m py_compile examples/operator_answer.py"],
    }
    path = workspace / "operator_spec.json"
    path.write_text(json.dumps(spec), encoding="utf-8")
    return path


def test_operator_panel_aggregates_safe_surfaces(tmp_path, monkeypatch):
    monkeypatch.setenv("WABI_PROVIDER_ORDER", "codex,dry-run")
    monkeypatch.setenv("WABI_DISABLE_BASE_MODEL", "1")
    subprocess.run(["git", "init"], cwd=str(tmp_path), check=True, capture_output=True, text=True)
    spec = write_spec(tmp_path)
    runtime = tmp_path / "runtime"
    witness = WitnessLog(runtime / "witness" / "wabi_patch_witness.sqlite")
    witness.append("test_event", {"ok": True})
    output_dir = runtime / "outputs"
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "safe_test_run_20260506-000000.json").write_text(
        json.dumps(
            {
                "schema": "wabi.safe_test_run.v1",
                "ok": True,
                "summary": {
                    "command_count": 1,
                    "passed": 1,
                    "failed": 0,
                    "errors": [],
                },
                "witness_event_id": 44,
                "witness_verified": True,
                "observation": {"observed_at_utc": "2026-05-06T00:00:00Z"},
            }
        ),
        encoding="utf-8",
    )

    payload = build_operator_panel(workspace=tmp_path, runtime_root=runtime, task_spec=spec)

    assert payload["ok"] is True
    assert payload["gate"] == "APPROVE"
    assert payload["provider"]["auto_provider"] == "codex"
    assert payload["worktree"]["ok"] is True
    assert payload["tools"]["names"]
    assert "operator_panel" in payload["tools"]["names"]
    assert payload["task_spec"]["ok"] is True
    assert payload["task_spec"]["operations"] == ["examples/operator_answer.py"]
    assert payload["witness"]["verified"] is True
    assert payload["witness"]["event_count"] == 1
    assert payload["latest_safe_tests"]["exists"] is True
    assert payload["latest_safe_tests"]["status"] == "passed"
    assert payload["latest_safe_tests"]["summary"]["passed"] == 1
    assert payload["latest_safe_tests"]["witness_verified"] is True
    assert payload["geodia_research"]["epistemic_status"] == "RESEARCH_ONLY"
    assert payload["geodia_research"]["surface"]["bounded"] is True
    assert payload["geodia_research"]["falsifier"]["result"] == "PASS"


def test_operator_status_cli_returns_json_without_writing_source(tmp_path):
    subprocess.run(["git", "init"], cwd=str(tmp_path), check=True, capture_output=True, text=True)
    spec = write_spec(tmp_path)
    proc = run_cli("operator-status", str(spec), "--json", workspace=tmp_path, runtime=tmp_path / "runtime")

    assert proc.returncode == 0, proc.stderr
    payload = json.loads(proc.stdout)
    assert payload["schema"] == "wabi.operator_panel.v1"
    assert payload["ok"] is True
    assert payload["task_spec"]["ok"] is True
    assert payload["geodia_research"]["epistemic_status"] == "RESEARCH_ONLY"
    assert "wabi task-spec-plan" in "\n".join(payload["commands"])
    assert not (tmp_path / "examples" / "operator_answer.py").exists()
