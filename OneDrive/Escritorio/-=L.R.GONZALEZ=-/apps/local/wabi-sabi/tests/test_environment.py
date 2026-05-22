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

    (root / "COMMS" / "agents_state" / "wabi-sabi-sentido-comun.json").write_text(
        json.dumps(
            {
                "schema": "medioevo.comms.agent_state.v1",
                "agent_id": "wabi-sabi-sentido-comun",
                "status": "POLICY_ONLY_LEARNING_SOURCE",
                "department_slug": "patterns",
                "action_gate": "REVIEW",
                "owns": ["runtime/sentido_comun policy inputs"],
                "may_touch": ["runtime/sentido_comun/**"],
                "must_not_touch_without_handoff": ["external actions"],
                "last_observation_fingerprint": "TEST_FINGERPRINT",
            }
        ),
        encoding="utf-8",
    )
    (root / "COMMS" / "tools" / "validate_seto_comms.py").write_text(
        "import json\n"
        "print(json.dumps({'ok': True, 'status': 'PASS', 'errors': [], 'warnings': [], 'counts': {'agents': 1}}))\n",
        encoding="utf-8",
    )
    (root / "qa_artifacts" / "pending" / "pending_review_latest.json").write_text(
        json.dumps(
            {
                "schema": "medioevo.pending_review.v1",
                "generated_at": "2026-05-06T16:22:25+00:00",
                "date": "2026-05-06",
                "active_markdown": {
                    "raw_open": 15,
                    "dedup_open": 15,
                    "by_lane": {"general": 10},
                    "by_blocker": {"legal_or_human": 12},
                    "top_items": [{"item": "Test pending", "first_evidence": "TASKS.md:1"}],
                },
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
                "timestamp": "2026-05-06T14:36:46Z",
                "gate": {
                    "status": "JAMMING",
                    "gate": "BLOCK",
                    "action": "reset_handoff",
                    "lambda_sat": 1.0,
                    "reasons": ["proceso_dominante_cpu"],
                },
                "metrics": {"cpu_pct": 48.2, "memory_pct": 81.6, "top_cpu_pct": 121.9},
                "top_cpu": [{"name": "codex.exe", "cpu_pct": 121.9}],
            }
        ),
        encoding="utf-8",
    )


def test_env_status_reads_pending_host_comms_and_writes_artifact(tmp_path):
    portfolio = tmp_path / "-=L.R.GONZALEZ=-"
    runtime = tmp_path / "runtime"
    build_fake_portfolio(portfolio)

    proc = run_cli("env-status", "--json", workspace=portfolio, runtime=runtime)

    assert proc.returncode == 0, proc.stderr
    payload = json.loads(proc.stdout)
    snapshot = payload["snapshot"]
    assert payload["action"] == "environment_snapshot"
    assert snapshot["schema"] == "wabi.environment_snapshot.v0_2"
    assert snapshot["pending"]["active_dedup"] == 15
    assert snapshot["host"]["gate"] == "BLOCK"
    assert snapshot["comms"]["agent_count"] == 1
    assert snapshot["comms"]["validator"]["ok"] is True
    assert snapshot["decision"]["recommended_mode"] == "A0_LOCAL_REVIEW_ONLY"
    assert Path(payload["artifact"]).exists()


def test_comms_state_reads_agents_and_validator(tmp_path):
    portfolio = tmp_path / "-=L.R.GONZALEZ=-"
    runtime = tmp_path / "runtime"
    build_fake_portfolio(portfolio)

    proc = run_cli("comms-state", "--json", workspace=portfolio, runtime=runtime)

    assert proc.returncode == 0, proc.stderr
    payload = json.loads(proc.stdout)
    assert payload["action"] == "comms_state"
    assert payload["comms"]["agent_count"] == 1
    assert payload["comms"]["by_gate"] == {"REVIEW": 1}
    assert payload["comms"]["validator"]["ok"] is True
    assert Path(payload["artifact"]).exists()
