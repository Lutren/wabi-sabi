import json
import os
import subprocess
import sys
from pathlib import Path


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


def build_fake_portfolio(root: Path) -> None:
    (root / "docs" / "ops").mkdir(parents=True)
    (root / "COMMS" / "agents_state").mkdir(parents=True)
    (root / "COMMS" / "tools").mkdir(parents=True)
    (root / "qa_artifacts" / "pending").mkdir(parents=True)
    (
        root / "-=MEDIOEVO=-" / "-=LIBROS" / "claudio" / "runtime" / "host_observacionista"
    ).mkdir(parents=True)

    (root / "COMMS" / "agents_state" / "claudio-local-autonomy.json").write_text(
        json.dumps(
            {
                "agent_id": "claudio-local-autonomy",
                "status": "A0_LOCAL_REVIEW_ONLY",
                "department": {"id": "wabi_sabi"},
                "action_gate": "BLOCK",
                "handoff_required": True,
                "allowed_actions": ["pending_review", "host_no_write"],
                "blocked_actions": ["external_target_execute", "destructive_file_moves"],
            }
        ),
        encoding="utf-8",
    )
    (root / "COMMS" / "tools" / "validate_seto_comms.py").write_text(
        "import json\nprint(json.dumps({'ok': True, 'status': 'PASS', 'errors': [], 'warnings': []}))\n",
        encoding="utf-8",
    )
    (root / "qa_artifacts" / "pending" / "pending_review_latest.json").write_text(
        json.dumps(
            {
                "active_markdown": {
                    "raw_open": 15,
                    "dedup_open": 15,
                    "by_blocker": {"external_or_gated": 2},
                }
            }
        ),
        encoding="utf-8",
    )
    (
        root
        / "-=MEDIOEVO=-"
        / "-=LIBROS"
        / "claudio"
        / "runtime"
        / "host_observacionista"
        / "latest_report.json"
    ).write_text(
        json.dumps(
            {
                "timestamp": "2026-05-06T16:49:19Z",
                "gate": {
                    "status": "JAMMING",
                    "gate": "BLOCK",
                    "action": "reset_handoff",
                    "lambda_sat": 0.975,
                    "reasons": ["proceso_dominante_cpu"],
                },
                "metrics": {"cpu_pct": 24.8},
            }
        ),
        encoding="utf-8",
    )


def test_decide_records_witness_task_manager_and_artifact(tmp_path):
    portfolio = tmp_path / "-=L.R.GONZALEZ=-"
    runtime = tmp_path / "runtime"
    build_fake_portfolio(portfolio)

    proc = run_cli("decide", "continuar pendientes locales", "--json", workspace=portfolio, runtime=runtime)

    assert proc.returncode == 0, proc.stderr
    payload = json.loads(proc.stdout)
    record = payload["record"]
    assert payload["action"] == "wabi_decision_recorded"
    assert record["schema"] == "wabi.decision_record.v0_2"
    assert record["status"] == "BLOCKED"
    assert record["recommended_mode"] == "A0_LOCAL_REVIEW_ONLY"
    assert record["witness_verified"] is True
    assert len(record["environment_snapshot_hash"]) == 64
    assert Path(payload["artifact"]).exists()
    assert Path(payload["snapshot_artifact"]).exists()

    manager = json.loads(Path(payload["task_manager"]).read_text(encoding="utf-8"))
    assert manager["schemaVersion"] == "obsai.task_manager.v1"
    assert manager["tasks"][0]["id"] == record["task_record"]["id"]
    assert manager["tasks"][0]["status"] == "BLOCKED"


def test_decision_log_lists_recorded_decisions(tmp_path):
    portfolio = tmp_path / "-=L.R.GONZALEZ=-"
    runtime = tmp_path / "runtime"
    build_fake_portfolio(portfolio)
    first = run_cli("decide", "estado local", "--json", workspace=portfolio, runtime=runtime)
    assert first.returncode == 0, first.stderr

    proc = run_cli("decision-log", "--json", workspace=portfolio, runtime=runtime)

    assert proc.returncode == 0, proc.stderr
    payload = json.loads(proc.stdout)
    assert payload["action"] == "wabi_decision_log"
    assert len(payload["records"]) == 1
    assert payload["records"][0]["witness_verified"] is True
    assert payload["tasks"]["schemaVersion"] == "obsai.task_manager.v1"


def test_comms_append_plan_uses_latest_decision_and_blocks_under_host_block(tmp_path):
    portfolio = tmp_path / "-=L.R.GONZALEZ=-"
    runtime = tmp_path / "runtime"
    build_fake_portfolio(portfolio)
    first = run_cli("decide", "estado local", "--json", workspace=portfolio, runtime=runtime)
    assert first.returncode == 0, first.stderr

    proc = run_cli("comms-append-plan", "--json", workspace=portfolio, runtime=runtime)

    assert proc.returncode == 0, proc.stderr
    payload = json.loads(proc.stdout)
    plan = payload["plan"]
    assert payload["action"] == "comms_append_plan"
    assert plan["append_allowed"] is False
    assert plan["append_performed"] is False
    assert plan["message"]["action_gate"] == "BLOCK"
    assert plan["message"]["observation_envelope"]["envelope_version"] == "seto-observation-v1"
    assert plan["validation"]["ok"] is True
    assert Path(payload["artifact"]).exists()
    assert not Path(plan["target_outbox"]).exists()


def test_programmer_workpack_is_plan_only_under_host_block(tmp_path):
    portfolio = tmp_path / "-=L.R.GONZALEZ=-"
    runtime = tmp_path / "runtime"
    build_fake_portfolio(portfolio)

    proc = run_cli(
        "programmer-workpack",
        "preparar cambio multiarchivo",
        "--json",
        workspace=portfolio,
        runtime=runtime,
    )

    assert proc.returncode == 0, proc.stderr
    payload = json.loads(proc.stdout)
    workpack = payload["workpack"]
    assert payload["action"] == "programmer_workpack"
    assert workpack["mode"] == "PLAN_ONLY"
    assert workpack["workpack_gate"] == "REVIEW"
    assert workpack["application_gate"] == "BLOCK"
    assert workpack["patches"] == []
    assert "apply_multi_file_patch" in workpack["blocked_now"]
    assert len(workpack["workpack_hash"]) == 64
    assert Path(payload["artifact"]).exists()
