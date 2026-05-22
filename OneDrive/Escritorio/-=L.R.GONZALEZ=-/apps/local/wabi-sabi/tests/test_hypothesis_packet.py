import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

from wabi_sabi.core.hypothesis_packet import (
    build_hypothesis_packet,
    evaluate_hypothesis_packet_payload,
    run_conjecture_counterexample,
)


APP_ROOT = Path(__file__).resolve().parents[1]


def run_cli(*args, workspace: Path, runtime: Path):
    env = os.environ.copy()
    env["PYTHONPATH"] = str(APP_ROOT)
    env["MEDIOEVO_NO_MODEL_MODE"] = "1"
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


def test_build_hypothesis_packet_has_counterexample_contract():
    packet = build_hypothesis_packet("The motor reduces R only when evidence closes a task.")

    assert packet["schema_version"] == "medioevo.hypothesis_packet.v0.1"
    assert packet["hypothesis_id"].startswith("hypothesis-")
    assert packet["claim_level"] == "operational"
    assert packet["counterclaim"]
    assert packet["falsifiers"]
    assert packet["evidence_required"]
    assert packet["boundary"]["publication_gate"] == "BLOCK"
    assert packet["metadata"]["cloud_provider_called"] is False
    assert packet["metadata"]["applied_to_sources"] is False


def test_evaluate_hypothesis_keeps_scientific_claim_in_review():
    packet = build_hypothesis_packet("This proves a new physics claim for Observacionismo.")

    evaluation = evaluate_hypothesis_packet_payload(packet)

    assert evaluation["gate"] == "REVIEW"
    assert evaluation["status"] == "REVIEW"
    assert "strong_claim_requires_human_review" in evaluation["reasons"]
    assert evaluation["Phi_eff_est"] < 0.8
    assert evaluation["publication_gate"] == "BLOCK"


def test_hypothesis_packet_requires_falsifiers():
    packet = build_hypothesis_packet("A local status report is non-mutating.")
    packet["falsifiers"] = []

    with pytest.raises(ValueError, match="falsifiers_required"):
        evaluate_hypothesis_packet_payload(packet)


def test_run_conjecture_counterexample_persists_artifact_and_witness(tmp_path):
    workspace = tmp_path / "workspace"
    runtime = tmp_path / "runtime"
    workspace.mkdir()

    payload = run_conjecture_counterexample(
        "Use the unit distance lesson to test whether Wabi should support claims with falsifiers.",
        workspace=workspace,
        runtime_root=runtime,
    )

    assert payload["schema"] == "wabi.conjecture_counterexample.v0_1"
    assert payload["ok"] is True
    assert payload["proposal_only"] is True
    assert payload["cloud_provider_called"] is False
    assert payload["applied_to_sources"] is False
    assert payload["evaluation"]["gate"] == "REVIEW"
    assert payload["task_spec"]["intent_name"] == "hypothesis_request"
    assert payload["witness"]["verified"] is True
    assert Path(payload["artifact"]).exists()
    assert not list(workspace.rglob("*.py"))


def test_hypothesis_cli_outputs_json_contract(tmp_path):
    proc = run_cli(
        "hypothesis",
        "The motor should treat strong claims as hypotheses until falsified or supported.",
        "--json",
        workspace=tmp_path,
        runtime=tmp_path / "runtime",
    )

    assert proc.returncode == 0, proc.stderr
    payload = json.loads(proc.stdout)
    assert payload["schema"] == "wabi.conjecture_counterexample.v0_1"
    assert payload["hypothesis_packet"]["falsifiers"]
    assert payload["evaluation"]["gate"] == "REVIEW"
    assert payload["cloud_provider_called"] is False
    assert payload["applied_to_sources"] is False
