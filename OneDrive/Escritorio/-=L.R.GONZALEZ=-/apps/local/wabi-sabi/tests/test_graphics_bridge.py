import json
from pathlib import Path

from wabi_sabi.core.graphics_bridge import GraphicsBridge


def test_graphics_bridge_discovers_duat_graphics_capabilities(tmp_path):
    graphics = tmp_path / "artifacts" / "duat-city" / "src" / "graphics"
    graphics.mkdir(parents=True)
    (graphics / "isoMath.ts").write_text("export const ok = true;\n", encoding="utf-8")
    (graphics / "tileRenderer.ts").write_text("export const ok = true;\n", encoding="utf-8")

    bridge = GraphicsBridge(workspace=tmp_path, runtime_root=tmp_path / "runtime")
    status = bridge.status()
    capabilities = bridge.list_capabilities()

    assert status["available"] is True
    assert status["graphics_live"] is False
    assert status["graphics_plan_ready"] is True
    assert status["external_calls_allowed"] is False
    assert {item["name"] for item in capabilities["capabilities"]} >= {"iso_math", "tile_renderer"}


def test_graphics_bridge_creates_scene_plan_without_publish_or_network(tmp_path):
    bridge = GraphicsBridge(workspace=tmp_path, runtime_root=tmp_path / "runtime")

    plan = bridge.create_scene_plan("crea una escena de DUAT city con nodos de agentes")
    task = bridge.export_task_spec(plan)
    artifact = bridge.write_plan_artifact(plan)

    assert plan["schema"] == "wabi.graphics_plan.v0_1"
    assert plan["kind"] == "scene"
    assert plan["external_calls_allowed"] is False
    assert plan["publication_allowed"] is False
    assert plan["applied_to_sources"] is False
    assert task["proposal_only"] is True
    assert task["applied_to_sources"] is False
    assert artifact.exists()
    assert json.loads(artifact.read_text(encoding="utf-8"))["kind"] == "scene"


def test_graphics_bridge_asset_plan_is_safe_stub_when_engine_missing(tmp_path):
    bridge = GraphicsBridge(workspace=tmp_path, runtime_root=tmp_path / "runtime")

    status = bridge.status()
    plan = bridge.create_asset_plan("genera assets para agentes")

    assert status["available"] is False
    assert status["graphics_live"] is False
    assert status["graphics_plan_ready"] is True
    assert plan["kind"] == "asset"
    assert "src/graphics/spriteResolver.ts" in plan["target_files"]
