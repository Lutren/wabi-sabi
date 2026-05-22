import json
import os
import subprocess
import sys
from pathlib import Path

from wabi_sabi.engine import (
    build_engine_plan,
    build_source_card,
    default_engine_manifest,
    engine_plan_to_task_spec,
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


def test_source_card_for_gdevelop_is_clean_room():
    card = build_source_card("https://github.com/4ian/GDevelop")

    assert card["schema"] == "wabi.engine.source_card.v1"
    assert card["source_name"] == "GDevelop"
    assert card["extraction_style"] == "clean_room"
    assert card["action_gate"] == "APPROVE"
    assert any("copying source code" in item for item in card["blocked_use"])
    assert "event_runtime" in card["modules"]


def test_default_engine_manifest_has_core_families():
    manifest = default_engine_manifest()
    modules = manifest["modules"]

    assert manifest["schema"] == "wabi.engine.manifest.v1"
    assert modules["app_core"]["family"] == "app_core"
    assert modules["game_core"]["family"] == "game_core"
    assert modules["programmer_core"]["family"] == "programmer_core"


def test_engine_plan_selects_app_and_game_modules():
    plan = build_engine_plan("crear app local con escena de juego y boton de prueba")
    module_names = {module["name"] for module in plan["modules"]}

    assert plan["schema"] == "wabi.engine.plan.v1"
    assert plan["action_gate"] == "APPROVE"
    assert "app_core" in module_names
    assert "game_core" in module_names
    assert "programmer_core" in module_names
    assert plan["project_graph"]["edges"]


def test_engine_plan_to_task_spec_is_task_spec_compatible():
    plan = build_engine_plan("crear motor app juego modular")
    task_spec = engine_plan_to_task_spec(plan, target="docs/engine/custom_ENGINE_PLAN.md")
    change = task_spec["changes"][0]

    assert task_spec["schema"] == "wabi.task_spec.v1"
    assert task_spec["metadata"]["clean_room"] is True
    assert change["op"] == "write_text"
    assert change["target"] == "docs/engine/custom_ENGINE_PLAN.md"
    assert "clean-room" in change["content"]
    assert "game_core" in change["content"]


def test_engine_plan_to_task_spec_rejects_sensitive_target():
    plan = build_engine_plan("crear motor app juego modular")

    try:
        engine_plan_to_task_spec(plan, target="private/ENGINE_PLAN.md")
    except ValueError as exc:
        assert "engine_task_spec_sensitive_target" in str(exc)
    else:
        raise AssertionError("sensitive engine task-spec target was not blocked")


def test_engine_cli_commands_are_read_only(tmp_path):
    runtime = tmp_path / "runtime"

    intake = run_cli("engine-intake", "GDevelop", "--json", workspace=tmp_path, runtime=runtime)
    assert intake.returncode == 0, intake.stderr
    intake_payload = json.loads(intake.stdout)
    assert intake_payload["source_card"]["source_name"] == "GDevelop"

    plan_proc = run_cli(
        "engine-plan",
        "crear app local con escena de juego",
        "--json",
        workspace=tmp_path,
        runtime=runtime,
    )
    assert plan_proc.returncode == 0, plan_proc.stderr
    plan_payload = json.loads(plan_proc.stdout)
    assert plan_payload["plan"]["action_gate"] == "APPROVE"

    plan_path = tmp_path / "engine_plan.json"
    plan_path.write_text(json.dumps(plan_payload["plan"], indent=2), encoding="utf-8")
    spec_proc = run_cli(
        "engine-task-spec",
        str(plan_path),
        "--target",
        "docs/engine/custom_ENGINE_PLAN.md",
        "--json",
        workspace=tmp_path,
        runtime=runtime,
    )
    assert spec_proc.returncode == 0, spec_proc.stderr
    spec_payload = json.loads(spec_proc.stdout)
    assert spec_payload["target"] == "docs/engine/custom_ENGINE_PLAN.md"
    assert spec_payload["task_spec"]["schema"] == "wabi.task_spec.v1"
    assert not (tmp_path / "docs" / "engine" / "custom_ENGINE_PLAN.md").exists()

    status = run_cli("engine-status", "--json", workspace=tmp_path, runtime=runtime)
    assert status.returncode == 0, status.stderr
    status_payload = json.loads(status.stdout)
    assert "game_core" in status_payload["manifest"]["modules"]


def test_engine_cli_write_docs_creates_runtime_artifacts(tmp_path):
    runtime = tmp_path / "runtime"
    plan_proc = run_cli(
        "engine-plan",
        "LOCAL_ONLY NO_PUBLICAR crear app local con escena",
        "--write-docs",
        "--json",
        workspace=tmp_path,
        runtime=runtime,
    )
    assert plan_proc.returncode == 0, plan_proc.stderr
    plan_payload = json.loads(plan_proc.stdout)
    plan_artifact = Path(plan_payload["artifact"])
    assert plan_artifact.exists()
    assert plan_artifact.read_text(encoding="utf-8").startswith("{")

    spec_proc = run_cli(
        "engine-task-spec",
        str(plan_artifact),
        "--target",
        "docs/engine/local_only/demo_ENGINE_PLAN.md",
        "--write-docs",
        "--json",
        workspace=tmp_path,
        runtime=runtime,
    )
    assert spec_proc.returncode == 0, spec_proc.stderr
    spec_payload = json.loads(spec_proc.stdout)
    spec_artifact = Path(spec_payload["artifact"])
    assert spec_artifact.exists()
    assert spec_payload["target"] == "docs/engine/local_only/demo_ENGINE_PLAN.md"
    assert not (tmp_path / "docs" / "engine" / "local_only" / "demo_ENGINE_PLAN.md").exists()
