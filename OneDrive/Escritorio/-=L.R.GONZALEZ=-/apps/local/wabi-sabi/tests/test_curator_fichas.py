import json
import os
import subprocess
import sys
from pathlib import Path

from wabi_sabi.core.curator_assistant import run_curator_assistant
from wabi_sabi.core.curator_fichas import (
    build_curation_record,
    build_fichas_from_report,
    build_owner_assignment,
    curation_processing_status,
    run_curator_fichas,
)


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


def make_workspace(workspace: Path) -> None:
    subprocess.run(["git", "init"], cwd=str(workspace), check=True, capture_output=True, text=True)
    (workspace / "pyproject.toml").write_text("[project]\nname='demo'\n", encoding="utf-8")
    (workspace / "docs" / "intake").mkdir(parents=True)
    (workspace / "loose-note.md").write_text("# note\n", encoding="utf-8")
    (workspace / "notes").mkdir()
    (workspace / "notes" / "idea.md").write_text("# idea\n", encoding="utf-8")
    (workspace / "secret_token.txt").write_text("do-not-read", encoding="utf-8")


def test_curator_fichas_generate_review_cards_without_cleanup(tmp_path):
    runtime = tmp_path / "runtime"
    make_workspace(tmp_path)
    report = run_curator_assistant(workspace=tmp_path, runtime_root=runtime)

    payload = run_curator_fichas(workspace=tmp_path, runtime_root=runtime, report_path=report["artifact"], max_fichas=5)

    assert payload["schema"] == "wabi.curator_fichas.v1"
    assert payload["ok"] is True
    assert payload["policy"]["delete_files"] is False
    assert payload["policy"]["move_files"] is False
    assert payload["policy"]["print_file_contents"] is False
    assert payload["policy"]["hash_existing_files"] is True
    assert payload["summary"]["delete_approved_count"] == 0
    assert payload["summary"]["cleanup_performed"] is False
    assert payload["summary"]["agent_processed_count"] == payload["summary"]["ficha_count"]
    assert payload["summary"]["needs_agent_processing_count"] == 0
    assert payload["summary"]["owner_assigned_count"] == payload["summary"]["ficha_count"]
    assert payload["summary"]["unassigned_count"] == 0
    assert payload["fichas"]
    assert all("delete" in ficha["blocked_actions"] for ficha in payload["fichas"])
    assert all("secret_token.txt" not in ficha["source_path"] for ficha in payload["fichas"])
    assert any(ficha["file_evidence"]["exists"] is True and ficha["file_evidence"]["sha256"] for ficha in payload["fichas"])
    assert all(ficha["owner"].startswith("agent:") for ficha in payload["fichas"])
    assert all(ficha["owner"] != "UNASSIGNED_CONCURRENT_SAFE" for ficha in payload["fichas"])
    assert all(ficha["owner_assignment"]["assigned_by_actor_type"] == "agent" for ficha in payload["fichas"])
    assert all(ficha["owner_assignment"]["status"] == "AGENT_ASSIGNED" for ficha in payload["fichas"])
    assert all(ficha["curation"]["status"] == "AGENT_PROCESSED" for ficha in payload["fichas"])
    assert all(ficha["curation"]["last_record"]["actor_type"] == "agent" for ficha in payload["fichas"])
    assert Path(payload["artifact"]).exists()
    assert Path(payload["markdown_artifact"]).exists()
    assert Path(payload["workspace_doc"]).exists()
    assert payload["witness_verified"] is True


def test_build_fichas_skips_blocked_candidates():
    report = {
        "schema": "wabi.curator_assistant_report.v1",
        "artifact": "report.json",
        "summary": {"candidate_count": 2},
        "candidates": [
            {
                "path": "safe-note.md",
                "source_status": "??",
                "category": "ROOT_LOOSE_REVIEW",
                "psi_state": "INCOGNITA",
                "decision": "UNKNOWN_REVIEW_REQUIRED",
                "action_gate": "REVIEW",
                "risk_flags": ["untracked"],
            },
            {
                "path": ".env",
                "source_status": "??",
                "category": "BOUNDARY_BLOCKED",
                "psi_state": "BLOQUEADO",
                "decision": "KEEP",
                "action_gate": "BLOCK",
                "risk_flags": ["secret_like"],
            },
        ],
    }

    fichas = build_fichas_from_report(report, max_fichas=10)

    assert len(fichas) == 1
    assert fichas[0]["source_path"] == "safe-note.md"
    assert fichas[0]["action_gate"] == "REVIEW"
    assert fichas[0]["owner"] == "agent:workspace_governance_curator"
    assert fichas[0]["owner_assignment"]["assigned_by_actor_type"] == "agent"
    assert fichas[0]["owner_assignment"]["status"] == "AGENT_ASSIGNED"
    assert fichas[0]["curation"]["last_record"]["actor_type"] == "agent"
    assert fichas[0]["curation"]["status"] == "AGENT_PROCESSED"


def test_curation_status_requires_agent_as_last_record():
    human_record = build_curation_record(
        actor_type="human",
        actor="manual_owner_assignment",
        event="owner_changed",
    )
    agent_record = build_curation_record(
        actor_type="agent",
        actor="curador_orden_assistant",
        event="curator_fichas_generated",
    )

    assert human_record["status"] == "NEEDS_AGENT_PROCESSING"
    assert human_record["human_last_record_means"] == "NEEDS_AGENT_PROCESSING"
    assert agent_record["status"] == "AGENT_PROCESSED"
    assert curation_processing_status({"actor_type": "human"}) == "NEEDS_AGENT_PROCESSING"
    assert curation_processing_status({"actor_type": "agent"}) == "AGENT_PROCESSED"


def test_owner_assignment_is_agent_recorded_by_lane():
    app_assignment = build_owner_assignment("apps/local/wabi-sabi/docs/USAGE.md", {})
    docs_assignment = build_owner_assignment("docs/developer/CURADOR.md", {})
    intake_assignment = build_owner_assignment("docs/intake/CURADOR.md", {})
    runtime_assignment = build_owner_assignment(
        "runtime/outputs/report.json",
        {"category": "RUNTIME_EVIDENCE"},
    )

    assert app_assignment["owner"] == "agent:wabi_sabi_maintenance_curator"
    assert docs_assignment["owner"] == "agent:developer_docs_curator"
    assert intake_assignment["owner"] == "agent:intake_curator"
    assert runtime_assignment["owner"] == "agent:runtime_evidence_curator"
    assert app_assignment["assigned_by_actor_type"] == "agent"
    assert app_assignment["status"] == "AGENT_ASSIGNED"


def test_curator_fichas_cli_uses_latest_report(tmp_path):
    runtime = tmp_path / "runtime"
    make_workspace(tmp_path)
    run_curator_assistant(workspace=tmp_path, runtime_root=runtime)

    proc = run_cli("curator-fichas", "--json", workspace=tmp_path, runtime=runtime)

    assert proc.returncode == 0, proc.stderr
    payload = json.loads(proc.stdout)
    assert payload["schema"] == "wabi.curator_fichas.v1"
    assert payload["ok"] is True
    assert payload["summary"]["delete_approved_count"] == 0
    assert payload["fichas"]
    assert payload["summary"]["agent_processed_count"] == payload["summary"]["ficha_count"]
    assert payload["summary"]["owner_assigned_count"] == payload["summary"]["ficha_count"]
    assert payload["summary"]["unassigned_count"] == 0
