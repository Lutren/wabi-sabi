from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

SOURCE_CARD_SCHEMA = "wabi.engine.source_card.v1"
ENGINE_MANIFEST_SCHEMA = "wabi.engine.manifest.v1"
ENGINE_PLAN_SCHEMA = "wabi.engine.plan.v1"
TASK_SPEC_SCHEMA = "wabi.task_spec.v1"

DEFAULT_BLOCKED_USE = [
    "copying source code from the reference project",
    "vendoring external repositories into this workspace",
    "using private game/TCG/RPG folders as engine input",
    "publishing or deploying generated output without review",
    "bypassing ActionGate, ObservationEnvelope, or WitnessLog",
]

DEFAULT_ALLOWED_USE = [
    "clean-room extraction of public architecture patterns",
    "local-first module planning",
    "task-spec generation for reviewed local implementation",
    "testable abstractions with explicit provenance",
]


@dataclass(frozen=True)
class SourceCard:
    source_name: str
    source_type: str
    repository: str
    extraction_style: str = "clean_room"
    license_note: str = "verify upstream license before redistribution"
    allowed_use: list[str] = field(default_factory=lambda: list(DEFAULT_ALLOWED_USE))
    blocked_use: list[str] = field(default_factory=lambda: list(DEFAULT_BLOCKED_USE))
    patterns: list[dict[str, str]] = field(default_factory=list)
    modules: list[str] = field(default_factory=list)
    evidence: list[str] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema": SOURCE_CARD_SCHEMA,
            "source_name": self.source_name,
            "source_type": self.source_type,
            "repository": self.repository,
            "extraction_style": self.extraction_style,
            "license_note": self.license_note,
            "allowed_use": list(self.allowed_use),
            "blocked_use": list(self.blocked_use),
            "patterns": [dict(pattern) for pattern in self.patterns],
            "modules": list(self.modules),
            "evidence": list(self.evidence),
            "notes": list(self.notes),
        }


SOURCE_CATALOG: dict[str, SourceCard] = {
    "gdevelop": SourceCard(
        source_name="GDevelop",
        source_type="public_open_source_reference",
        repository="https://github.com/4ian/GDevelop",
        license_note="public repository; verify LICENSE.md before redistribution",
        patterns=[
            {
                "name": "event_sheet_runtime",
                "invariant": "represent behavior as declarative conditions and actions instead of ad hoc code strings",
            },
            {
                "name": "scene_graph",
                "invariant": "separate project, scene, object, behavior, asset, and runtime state",
            },
            {
                "name": "extension_system",
                "invariant": "ship capabilities as discoverable modules with declared inputs, outputs, and tests",
            },
            {
                "name": "export_pipeline",
                "invariant": "compile project state into runnable targets without exposing private authoring state",
            },
        ],
        modules=[
            "event_runtime",
            "scene_graph",
            "asset_catalog",
            "behavior_modules",
            "export_pipeline",
        ],
        evidence=[
            "repo README describes editor, game engine, extensions, and online services",
            "repo tree exposes Core, GDJS, GDevelop.js, newIDE, and Extensions boundaries",
        ],
        notes=[
            "Use as game-engine architecture signal only; do not copy Core/GDJS/newIDE code.",
        ],
    ),
    "dyad": SourceCard(
        source_name="Dyad",
        source_type="public_open_source_reference",
        repository="https://github.com/dyad-sh/dyad",
        license_note="mixed licensing; repo README separates open-source code from src/pro fair-source code",
        patterns=[
            {
                "name": "local_app_builder",
                "invariant": "keep app generation local, private, and provider-optional",
            },
            {
                "name": "bring_your_own_keys",
                "invariant": "treat providers as replaceable adapters and never store secrets in generated specs",
            },
            {
                "name": "project_preview_loop",
                "invariant": "turn a user goal into files, checks, and previewable artifacts through small iterations",
            },
        ],
        modules=[
            "app_scaffold",
            "provider_adapter",
            "preview_loop",
            "project_state",
        ],
        evidence=[
            "repo README describes Dyad as a local AI app builder",
            "repo README highlights local/private/no lock-in posture",
        ],
        notes=[
            "Avoid src/pro and any fair-source implementation details; use only high-level local-builder invariants.",
        ],
    ),
    "openhands": SourceCard(
        source_name="OpenHands",
        source_type="public_open_source_reference",
        repository="https://github.com/OpenHands/OpenHands",
        license_note="public repository; verify upstream license before redistribution",
        patterns=[
            {
                "name": "agent_workspace_loop",
                "invariant": "agent work should pass through explicit actions, observations, and verifiable artifacts",
            },
            {
                "name": "tool_boundary",
                "invariant": "tools need declared read/write scope, risk class, and result capture",
            },
            {
                "name": "sandboxed_execution",
                "invariant": "execution belongs behind a gate, with rollback/evidence rather than raw shell freedom",
            },
        ],
        modules=[
            "agent_loop",
            "tool_boundary",
            "execution_gate",
            "artifact_trace",
        ],
        evidence=[
            "repo title presents OpenHands as AI-driven development",
        ],
        notes=[
            "Use as agent-runtime posture signal only; do not mirror internal implementation.",
        ],
    ),
    "lovable": SourceCard(
        source_name="Lovable-like app builder",
        source_type="product_pattern_reference",
        repository="external_product_pattern",
        license_note="not a source dependency; treat only as a UX/workflow category",
        patterns=[
            {
                "name": "goal_to_app_loop",
                "invariant": "convert user intent into a project graph, file plan, preview, and iteration log",
            },
            {
                "name": "human_visible_preview",
                "invariant": "generated apps need inspectable output and tight feedback loops",
            },
        ],
        modules=[
            "intent_parser",
            "project_graph",
            "preview_contract",
        ],
        evidence=[
            "user-requested comparison category",
        ],
        notes=[
            "Category card only; not an upstream code source.",
        ],
    ),
}


ENGINE_MODULES: dict[str, dict[str, Any]] = {
    "observation_kernel": {
        "family": "observacionismo_core",
        "capabilities": ["ObservationEnvelope", "Residue/R gate", "Phi_eff evidence loop"],
        "inputs": ["intent", "source_cards", "workspace_state"],
        "outputs": ["observation", "risk_flags", "evidence"],
        "gates": ["ActionGate", "WitnessLog"],
        "tests": ["unit: observation envelope hash is stable", "unit: blocked actions stay blocked"],
    },
    "project_graph": {
        "family": "app_core",
        "capabilities": ["project nodes", "module edges", "file/task mapping"],
        "inputs": ["goal", "selected_modules"],
        "outputs": ["graph", "task_spec_candidates"],
        "gates": ["workspace boundary", "no private layer"],
        "tests": ["unit: graph nodes have ids", "unit: edges reference existing nodes"],
    },
    "app_core": {
        "family": "app_core",
        "capabilities": ["routes", "state", "components", "preview contract"],
        "inputs": ["project_graph", "user_goal"],
        "outputs": ["app shell plan", "component contracts"],
        "gates": ["local preview only", "no deploy"],
        "tests": ["smoke: generated task spec validates"],
    },
    "game_core": {
        "family": "game_core",
        "capabilities": ["scene graph", "event sheet", "asset catalog", "runtime systems"],
        "inputs": ["scene definitions", "event rules", "asset references"],
        "outputs": ["game module plan", "simulation contracts"],
        "gates": ["no private RPG/TCG path", "clean-room only"],
        "tests": ["unit: event rules serialize", "unit: scene graph validates"],
    },
    "programmer_core": {
        "family": "programmer_core",
        "capabilities": ["task specs", "patch plans", "safe executor", "rollback"],
        "inputs": ["engine_plan", "workspace_state"],
        "outputs": ["wabi.task_spec.v1", "patch plan", "witness event"],
        "gates": ["ActionGate", "SafeExecutor", "RollbackStore"],
        "tests": ["unit: task spec never writes sensitive paths", "integration: task-spec-plan"],
    },
    "extension_registry": {
        "family": "modular_core",
        "capabilities": ["module discovery", "capability cards", "compatibility gates"],
        "inputs": ["module cards"],
        "outputs": ["registry manifest", "activation plan"],
        "gates": ["explicit module ownership", "no implicit dependency install"],
        "tests": ["unit: module names are unique"],
    },
}


def default_engine_manifest() -> dict[str, Any]:
    return {
        "schema": ENGINE_MANIFEST_SCHEMA,
        "engine_name": "wabi_modular_engine",
        "posture": "local_first_clean_room",
        "default_sources": ["gdevelop", "dyad", "openhands"],
        "modules": {name: dict(module) for name, module in ENGINE_MODULES.items()},
        "hard_boundaries": list(DEFAULT_BLOCKED_USE),
        "allowed_use": list(DEFAULT_ALLOWED_USE),
        "task_spec_schema": TASK_SPEC_SCHEMA,
    }


def build_source_card(source: str, evidence: list[str] | None = None) -> dict[str, Any]:
    key = _source_key(source)
    if key in SOURCE_CATALOG:
        card = SOURCE_CATALOG[key].to_dict()
    else:
        label = source.strip() or "Unknown source"
        card = SourceCard(
            source_name=label,
            source_type="user_declared_reference",
            repository=label if label.startswith(("http://", "https://")) else "user_declared",
            patterns=[
                {
                    "name": "user_declared_pattern",
                    "invariant": "extract only stable behavior and module boundaries after review",
                }
            ],
            modules=["review_required"],
            evidence=["user declared source; no upstream inspection claimed"],
            notes=["Unknown source cards are REVIEW for implementation until manually curated."],
        ).to_dict()
        card["action_gate"] = "REVIEW"
    if evidence:
        card["evidence"].extend(str(item) for item in evidence if str(item).strip())
    card.setdefault("action_gate", "APPROVE")
    return card


def build_engine_plan(
    goal: str,
    *,
    sources: list[str] | None = None,
    project_name: str | None = None,
) -> dict[str, Any]:
    clean_goal = " ".join(goal.split())
    if not clean_goal:
        raise ValueError("missing_engine_goal")
    selected_sources = sources or _sources_for_goal(clean_goal)
    source_cards = [build_source_card(source) for source in selected_sources]
    module_names = _modules_for_goal(clean_goal, source_cards)
    graph_nodes = [
        {
            "id": name,
            "type": ENGINE_MODULES[name]["family"],
            "capabilities": list(ENGINE_MODULES[name]["capabilities"]),
        }
        for name in module_names
    ]
    graph_edges = _graph_edges(module_names)
    action_gate = _plan_gate(clean_goal, source_cards)
    slug = _slugify(project_name or clean_goal)
    return {
        "schema": ENGINE_PLAN_SCHEMA,
        "engine_name": "wabi_modular_engine",
        "project_name": project_name or slug.replace("-", "_"),
        "goal": clean_goal,
        "posture": "clean_room_local_first",
        "action_gate": action_gate,
        "source_cards": source_cards,
        "modules": [
            {"name": name, **dict(ENGINE_MODULES[name])}
            for name in module_names
        ],
        "project_graph": {
            "nodes": graph_nodes,
            "edges": graph_edges,
        },
        "implementation_strategy": [
            "record source cards and invariants before code generation",
            "generate a wabi.task_spec.v1 plan before any source write",
            "apply changes only through task-spec-plan/task-spec-apply and SafeExecutor",
            "keep providers optional and secrets out of specs",
        ],
        "assumptions": [
            "external repositories are references for architecture only",
            "v1 writes documentation/task specs before executable engine code",
            "private RPG/TCG/game_bridge paths remain outside scope",
        ],
        "unknown": [
            "exact product target and UI stack are not fixed by this plan",
            "upstream licenses must be rechecked before redistribution",
        ],
        "test_commands": [
            "python -m pytest tests/test_engine.py -q",
            "python -m pytest tests/test_task_spec_planner.py -q",
        ],
    }


def load_engine_plan(workspace: str | Path, plan_ref: str | Path) -> dict[str, Any]:
    workspace_path = Path(workspace).resolve()
    plan_path = Path(plan_ref)
    if not plan_path.is_absolute():
        plan_path = workspace_path / plan_path
    plan_path = plan_path.resolve()
    try:
        plan_path.relative_to(workspace_path)
    except ValueError as exc:
        raise ValueError("engine_plan_must_be_inside_workspace") from exc
    data = json.loads(plan_path.read_text(encoding="utf-8"))
    _validate_engine_plan(data)
    return data


def engine_plan_to_task_spec(
    plan: dict[str, Any],
    *,
    target: str | None = None,
) -> dict[str, Any]:
    _validate_engine_plan(plan)
    target_path = target or f"docs/engine/{_slugify(plan['project_name'])}_ENGINE_PLAN.md"
    normalized_target = target_path.replace("\\", "/").lstrip("/")
    if not normalized_target.endswith(".md"):
        raise ValueError("engine_task_spec_target_must_be_markdown")
    _reject_sensitive_target(normalized_target)
    return {
        "schema": TASK_SPEC_SCHEMA,
        "summary": f"Document clean-room modular engine plan for {plan['project_name']}",
        "changes": [
            {
                "op": "write_text",
                "target": normalized_target,
                "content": _render_engine_plan_markdown(plan),
            }
        ],
        "test_commands": [],
        "metadata": {
            "origin_schema": ENGINE_PLAN_SCHEMA,
            "engine_name": plan["engine_name"],
            "action_gate": plan["action_gate"],
            "clean_room": True,
        },
    }


def _render_engine_plan_markdown(plan: dict[str, Any]) -> str:
    lines = [
        f"# {plan['project_name']} Engine Plan",
        "",
        "## Posture",
        f"- Schema: {plan['schema']}",
        f"- Engine: {plan['engine_name']}",
        f"- ActionGate: {plan['action_gate']}",
        "- Extraction: clean-room; no source-code copying; no vendoring.",
        "",
        "## Visibility",
        "- LOCAL_ONLY / NO_PUBLICAR.",
        "- No push, no deploy, no Gumroad, no social posting, no public release.",
        "- Private RPG/TCG/game_bridge paths stay out of scope.",
        "",
        "## Goal",
        plan["goal"],
        "",
        "## Source Cards",
    ]
    for card in plan.get("source_cards", []):
        lines.extend(
            [
                f"- {card['source_name']} ({card['source_type']})",
                f"  - Repository: {card['repository']}",
                f"  - Style: {card['extraction_style']}",
                f"  - Gate: {card.get('action_gate', 'APPROVE')}",
            ]
        )
        for pattern in card.get("patterns", [])[:4]:
            lines.append(f"  - Pattern: {pattern['name']} -> {pattern['invariant']}")
    lines.extend(["", "## Modules"])
    for module in plan.get("modules", []):
        lines.append(f"- {module['name']} [{module['family']}]")
        for capability in module.get("capabilities", []):
            lines.append(f"  - {capability}")
    lines.extend(["", "## Project Graph"])
    for node in plan.get("project_graph", {}).get("nodes", []):
        lines.append(f"- Node: {node['id']} ({node['type']})")
    for edge in plan.get("project_graph", {}).get("edges", []):
        lines.append(f"- Edge: {edge['from']} -> {edge['to']} ({edge['reason']})")
    lines.extend(["", "## Implementation Strategy"])
    lines.extend(f"- {item}" for item in plan.get("implementation_strategy", []))
    lines.extend(["", "## Boundaries"])
    lines.extend(f"- BLOCK: {item}" for item in DEFAULT_BLOCKED_USE)
    lines.extend(["", "## Tests"])
    lines.extend(f"- {item}" for item in plan.get("test_commands", []))
    if not plan.get("test_commands"):
        lines.append("- Not declared.")
    lines.append("")
    return "\n".join(lines)


def _source_key(source: str) -> str:
    source_lower = source.strip().lower()
    for key in SOURCE_CATALOG:
        if key in source_lower:
            return key
    if "4ian/gdevelop" in source_lower:
        return "gdevelop"
    if "all-hands-ai/openhands" in source_lower or "openhands/openhands" in source_lower:
        return "openhands"
    if "dyad-sh/dyad" in source_lower:
        return "dyad"
    return source_lower


def _sources_for_goal(goal: str) -> list[str]:
    goal_lower = goal.lower()
    sources = ["dyad", "openhands"]
    if any(term in goal_lower for term in ["game", "juego", "scene", "escena", "engine", "motor"]):
        sources.insert(0, "gdevelop")
    if any(term in goal_lower for term in ["lovable", "bolt", "v0", "app builder"]):
        sources.append("lovable")
    return list(dict.fromkeys(sources))


def _modules_for_goal(goal: str, source_cards: list[dict[str, Any]]) -> list[str]:
    goal_lower = goal.lower()
    modules = ["observation_kernel", "project_graph", "programmer_core", "extension_registry"]
    source_modules = {module for card in source_cards for module in card.get("modules", [])}
    if any(term in goal_lower for term in ["app", "web", "dashboard", "lovable", "bolt", "v0"]):
        modules.insert(2, "app_core")
    if any(term in goal_lower for term in ["game", "juego", "scene", "escena", "2d", "3d", "motor"]):
        modules.insert(2, "game_core")
    if "event_runtime" in source_modules or "scene_graph" in source_modules:
        modules.insert(2, "game_core")
    if "app_scaffold" in source_modules or "preview_loop" in source_modules:
        modules.insert(2, "app_core")
    return [name for name in dict.fromkeys(modules) if name in ENGINE_MODULES]


def _graph_edges(module_names: list[str]) -> list[dict[str, str]]:
    edges: list[dict[str, str]] = []
    if "observation_kernel" in module_names and "project_graph" in module_names:
        edges.append({"from": "observation_kernel", "to": "project_graph", "reason": "bounded intent becomes graph"})
    if "project_graph" in module_names and "app_core" in module_names:
        edges.append({"from": "project_graph", "to": "app_core", "reason": "graph drives app contracts"})
    if "project_graph" in module_names and "game_core" in module_names:
        edges.append({"from": "project_graph", "to": "game_core", "reason": "graph drives scenes and events"})
    if "programmer_core" in module_names:
        for candidate in ["app_core", "game_core", "project_graph"]:
            if candidate in module_names:
                edges.append({"from": candidate, "to": "programmer_core", "reason": "module plan becomes task spec"})
    if "extension_registry" in module_names:
        edges.append({"from": "extension_registry", "to": "project_graph", "reason": "capabilities constrain graph"})
    return edges


def _plan_gate(goal: str, source_cards: list[dict[str, Any]]) -> str:
    goal_lower = goal.lower()
    if any(term in goal_lower for term in ["delete", "deploy", "publish", "api key", "secret", "token"]):
        return "BLOCK"
    if any(card.get("action_gate") == "REVIEW" for card in source_cards):
        return "REVIEW"
    return "APPROVE"


def _validate_engine_plan(plan: dict[str, Any]) -> None:
    if plan.get("schema") != ENGINE_PLAN_SCHEMA:
        raise ValueError("unsupported_engine_plan_schema")
    for key in ["engine_name", "project_name", "goal", "action_gate", "modules", "source_cards", "project_graph"]:
        if key not in plan:
            raise ValueError(f"missing_engine_plan_field:{key}")
    if plan["action_gate"] == "BLOCK":
        raise ValueError("blocked_engine_plan_cannot_be_converted_to_task_spec")


def _reject_sensitive_target(target: str) -> None:
    lowered = target.lower()
    blocked = [
        ".git/",
        ".env",
        "runtime/",
        "releases/",
        "dist/",
        "build/",
        "game-private/",
        "metaevo-tcg/",
        "tcg/",
        "game_bridge/",
        "private/",
    ]
    if target.startswith("../") or "/../" in target:
        raise ValueError("engine_task_spec_target_outside_workspace")
    for part in blocked:
        if lowered.startswith(part) or f"/{part}" in lowered or lowered.endswith(part.rstrip("/")):
            raise ValueError(f"engine_task_spec_sensitive_target:{part.rstrip('/')}")


def _slugify(value: str, *, max_length: int = 64) -> str:
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", value.strip().lower()).strip("-")
    if not slug:
        slug = "engine-plan"
    return slug[:max_length].strip("-") or "engine-plan"
