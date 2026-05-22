import json
import os
import subprocess
import sys
from pathlib import Path

from wabi_sabi.engine import (
    build_observatorio_sandbox_project,
    fingerprint_payload,
    observatorio_click_events,
    simulate_engine_project,
    validate_engine_project_spec,
    write_engine_project_spec,
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
        timeout=30,
    )


def test_observatorio_sandbox_project_is_valid_local_only():
    project = build_observatorio_sandbox_project()
    validation = validate_engine_project_spec(project)

    assert project["schema"] == "wabi.engine.project_spec.v1"
    assert project["visibility"]["classification"] == "LOCAL_ONLY"
    assert project["visibility"]["publish_allowed"] is False
    assert validation["ok"] is True
    assert validation["node_count"] == 5
    assert validation["edge_count"] == 4
    assert validation["scene_count"] == 1
    assert validation["fingerprint"] == project["fingerprint"]


def test_project_runtime_serialization_is_stable():
    first = build_observatorio_sandbox_project()
    second = build_observatorio_sandbox_project()

    assert first == second
    assert first["fingerprint"] == fingerprint_payload(first)
    rules = first["scenes"][0]["event_sheet"]["rules"]
    assert [rule["id"] for rule in rules] == [
        "observe_click_records_signal",
        "three_signals_reveal_pattern",
        "residue_floor_keeps_local_review",
    ]


def test_project_validation_rejects_missing_edge_target():
    project = build_observatorio_sandbox_project()
    project["project_graph"]["edges"].append({"from": "app_shell", "to": "missing", "relation": "bad"})
    project["fingerprint"] = fingerprint_payload(project)

    validation = validate_engine_project_spec(project)

    assert validation["ok"] is False
    assert any(error.startswith("edge_target_missing") for error in validation["errors"])


def test_project_validation_rejects_event_rule_without_actions():
    project = build_observatorio_sandbox_project()
    project["scenes"][0]["event_sheet"]["rules"][0]["actions"] = []
    project["fingerprint"] = fingerprint_payload(project)

    validation = validate_engine_project_spec(project)

    assert validation["ok"] is False
    assert "event_rule_requires_actions:observe_click_records_signal" in validation["errors"]


def test_project_validation_rejects_private_path_markers_in_path_fields():
    project = build_observatorio_sandbox_project()
    project["scenes"][0]["objects"][0]["asset_path"] = "E:/Medioevo_RPG/private.png"
    project["fingerprint"] = fingerprint_payload(project)

    validation = validate_engine_project_spec(project)

    assert validation["ok"] is False
    assert "private_path_marker_present:rpg" in validation["errors"]


def test_write_engine_project_spec_creates_local_only_artifact(tmp_path):
    project = build_observatorio_sandbox_project()
    artifact = write_engine_project_spec(tmp_path, project)

    assert artifact == tmp_path / "docs" / "engine" / "local_only" / "wabi_sabi_observatorio_sandbox_PROJECT_SPEC.json"
    data = json.loads(artifact.read_text(encoding="utf-8"))
    assert data["fingerprint"] == project["fingerprint"]


def test_engine_sandbox_cli_write_and_validate(tmp_path):
    runtime = tmp_path / "runtime"
    sandbox = run_cli("engine-sandbox", "--write-docs", "--json", workspace=tmp_path, runtime=runtime)

    assert sandbox.returncode == 0, sandbox.stderr
    sandbox_payload = json.loads(sandbox.stdout)
    artifact = Path(sandbox_payload["artifact"])
    assert artifact.exists()
    assert sandbox_payload["validation"]["ok"] is True
    assert sandbox_payload["project"]["visibility"]["publish_allowed"] is False

    validation = run_cli("engine-project-validate", str(artifact), "--json", workspace=tmp_path, runtime=runtime)
    assert validation.returncode == 0, validation.stderr
    validation_payload = json.loads(validation.stdout)
    assert validation_payload["ok"] is True
    assert validation_payload["validation"]["fingerprint"] == sandbox_payload["project"]["fingerprint"]


def test_observatorio_simulation_runs_three_clicks():
    project = build_observatorio_sandbox_project()
    simulation = simulate_engine_project(project, observatorio_click_events(3))

    assert simulation["ok"] is True
    assert simulation["event_count"] == 3
    assert simulation["state"]["scene.observation_count"] == 3
    assert simulation["state"]["pattern_marker.visible"] is True
    assert simulation["state"]["residue_meter.value"] == 0.12
    assert simulation["state"]["sandbox.action_gate"] == "APPROVE"
    assert "pattern_visible" in simulation["state"]["signal_log.entries"]
    assert [item["rule_id"] for item in simulation["fired_rules"]].count("three_signals_reveal_pattern") == 1


def test_observatorio_simulation_is_deterministic():
    project = build_observatorio_sandbox_project()
    events = observatorio_click_events(3)

    first = simulate_engine_project(project, events)
    second = simulate_engine_project(project, events)

    assert first == second


def test_simulation_rejects_invalid_project():
    project = build_observatorio_sandbox_project()
    project["project_graph"]["edges"].append({"from": "app_shell", "to": "missing", "relation": "bad"})
    project["fingerprint"] = fingerprint_payload(project)

    try:
        simulate_engine_project(project, observatorio_click_events(1))
    except ValueError as exc:
        assert "invalid_engine_project_spec" in str(exc)
    else:
        raise AssertionError("invalid project spec was simulated")


def test_engine_simulate_cli_runs_project_spec(tmp_path):
    runtime = tmp_path / "runtime"
    project = build_observatorio_sandbox_project()
    artifact = write_engine_project_spec(tmp_path, project)

    proc = run_cli("engine-simulate", str(artifact), "3", "--json", workspace=tmp_path, runtime=runtime)

    assert proc.returncode == 0, proc.stderr
    payload = json.loads(proc.stdout)
    assert payload["ok"] is True
    assert payload["simulation"]["state"]["scene.observation_count"] == 3
    assert payload["simulation"]["state"]["pattern_marker.visible"] is True
    assert payload["simulation"]["state"]["residue_meter.value"] == 0.12
