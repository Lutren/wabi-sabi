from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Any

from wabi_sabi.core.redaction import redact_text
from wabi_sabi.core.tools import write_artifact


GRAPHICS_BRIDGE_SCHEMA = "wabi.graphics_bridge.v0_1"
GRAPHICS_PLAN_SCHEMA = "wabi.graphics_plan.v0_1"
GRAPHICS_TASK_SCHEMA = "wabi.graphics_task_spec.v0_1"

GRAPHICS_FILES = {
    "atlas": "atlas.ts",
    "asset_manifest_loader": "assetManifestLoader.ts",
    "agent_renderer": "agentRenderer.ts",
    "building_renderer": "buildingRenderer.ts",
    "fibmob_procedural": "fibmobProcedural.ts",
    "iso_math": "isoMath.ts",
    "light_engine": "lightEngine.ts",
    "particle_engine": "particleEngine.ts",
    "render_budget": "renderBudget.ts",
    "shadow_engine": "shadowEngine.ts",
    "sprite_resolver": "spriteResolver.ts",
    "tile_renderer": "tileRenderer.ts",
}


class GraphicsBridge:
    """Plan-only bridge from Wabi to the local DUAT graphics lane.

    v0.1 intentionally does not call external services, does not publish, and
    does not ingest private assets. It discovers local capabilities and emits
    task specs/artifacts that a human or local gated executor can review later.
    """

    def __init__(self, *, workspace: str | Path, runtime_root: str | Path):
        self.workspace = Path(workspace).resolve()
        self.runtime_root = Path(runtime_root).resolve()
        self.engine_root = self._discover_engine_root()

    def status(self) -> dict[str, Any]:
        capabilities = self.list_capabilities()
        available = bool(self.engine_root and capabilities.get("capabilities"))
        return {
            "schema": GRAPHICS_BRIDGE_SCHEMA,
            "ok": True,
            "available": available,
            "graphics_live": False,
            "graphics_plan_ready": True,
            "mode": "LOCAL_PLAN_ONLY",
            "safe_mode": "plan_only_no_external_calls",
            "engine_root": str(self.engine_root) if self.engine_root else "",
            "external_calls_allowed": False,
            "publication_allowed": False,
            "private_asset_access_allowed": False,
            "capability_count": len(capabilities.get("capabilities", [])),
        }

    def list_capabilities(self) -> dict[str, Any]:
        graphics_dir = self.engine_root / "src" / "graphics" if self.engine_root else None
        found: list[dict[str, str]] = []
        if graphics_dir and graphics_dir.exists():
            for name, filename in sorted(GRAPHICS_FILES.items()):
                path = graphics_dir / filename
                if path.exists():
                    found.append({"name": name, "path": str(path)})
        return {
            "schema": f"{GRAPHICS_BRIDGE_SCHEMA}.capabilities",
            "engine_root": str(self.engine_root) if self.engine_root else "",
            "graphics_live": False,
            "graphics_plan_ready": True,
            "capabilities": found,
            "fallback": "procedural_plan_only" if not found else "duat_graphics_files_discovered",
            "blocked_actions": [
                "publish",
                "deploy",
                "cloud_asset_generation",
                "private_asset_scan_outside_allowlist",
                "direct_renderer_mutation_without_gate",
            ],
        }

    def create_scene_plan(self, prompt: str) -> dict[str, Any]:
        return self._create_plan(kind="scene", prompt=prompt)

    def create_asset_plan(self, prompt: str) -> dict[str, Any]:
        return self._create_plan(kind="asset", prompt=prompt)

    def export_task_spec(self, plan: dict[str, Any]) -> dict[str, Any]:
        kind = str(plan.get("kind") or "graphics")
        prompt = str(plan.get("prompt") or "")
        return {
            "schema": GRAPHICS_TASK_SCHEMA,
            "task_type": f"graphics_{kind}",
            "title": f"Prepare DUAT {kind} plan",
            "description": redact_text(prompt),
            "proposal_only": True,
            "action_gate": "REVIEW",
            "graphics_bridge": {
                "graphics_live": False,
                "graphics_plan_ready": True,
                "external_calls_allowed": False,
                "publication_allowed": False,
            },
            "target_files": plan.get("target_files", []),
            "test_plan": plan.get("test_plan", []),
            "rollback": "No source files are modified by this task spec. Discard the generated artifact to roll back.",
            "applied_to_sources": False,
        }

    def write_plan_artifact(self, plan: dict[str, Any]) -> Path:
        text = json.dumps(plan, indent=2, ensure_ascii=False) + "\n"
        return write_artifact(self.runtime_root / "outputs" / "graphics_bridge", "wabi_graphics_plan", ".json", text)

    def _create_plan(self, *, kind: str, prompt: str) -> dict[str, Any]:
        capabilities = self.list_capabilities()
        if kind == "asset":
            steps = [
                "Revisar manifest de assets revisados antes de copiar o promover cualquier imagen.",
                "Mapear el asset solicitado a TileType, BuildingType, AgentRole o UI icon si aplica.",
                "Preparar task spec local con fallback procedural activo.",
                "Validar que no haya publicacion ni lectura de assets privados fuera de allowlist.",
            ]
            target_files = [
                "src/graphics/assetManifestLoader.ts",
                "src/graphics/spriteResolver.ts",
                "public/reviewed-assets/*/REVIEWED_ASSETS_MANIFEST.json",
            ]
        else:
            steps = [
                "Describir composicion 2.5D y entidades visibles de la escena.",
                "Mapear escena a renderers DUAT existentes sin reescribir el motor.",
                "Preparar cambios candidatos como plan, no como patch aplicado.",
                "Validar visualmente con screenshot local cuando exista browser QA disponible.",
            ]
            target_files = [
                "src/graphics/isoMath.ts",
                "src/graphics/tileRenderer.ts",
                "src/graphics/buildingRenderer.ts",
                "src/graphics/agentRenderer.ts",
                "src/components/MainCanvas.tsx",
            ]
        plan = {
            "schema": GRAPHICS_PLAN_SCHEMA,
            "created_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
            "kind": kind,
            "prompt": redact_text(prompt),
            "mode": "plan_only",
            "engine_status": self.status(),
            "capabilities": capabilities.get("capabilities", []),
            "steps": steps,
            "target_files": target_files,
            "test_plan": [
                "pnpm --filter @workspace/duat-city run test",
                "pnpm --filter @workspace/duat-city run typecheck",
                "pnpm --filter @workspace/duat-city run build",
            ],
            "external_calls_allowed": False,
            "publication_allowed": False,
            "applied_to_sources": False,
        }
        plan["task_spec"] = self.export_task_spec(plan)
        return plan

    def _discover_engine_root(self) -> Path | None:
        candidates: list[Path] = []
        for base in [self.workspace, *self.workspace.parents]:
            candidates.append(base / "artifacts" / "duat-city")
            candidates.append(base / "Duat-Fibmob-Lab")
        for candidate in candidates:
            if (candidate / "src" / "graphics").exists():
                return candidate.resolve()
        return None
