from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

PROJECT_SPEC_SCHEMA = "wabi.engine.project_spec.v1"
LOCAL_ONLY_VISIBILITY = {
    "classification": "LOCAL_ONLY",
    "publish_allowed": False,
    "public_release_allowed": False,
    "external_channels": "CLOSED",
    "notes": [
        "NO_PUBLICAR",
        "No push, no deploy, no Gumroad, no social posting.",
        "Private RPG/TCG/game_bridge paths stay out of scope.",
    ],
}
PRIVATE_PATH_MARKERS = ("rpg", "tcg", "game_bridge", "game-private", "metaevo-tcg")


@dataclass(frozen=True)
class GraphNode:
    node_id: str
    node_type: str
    label: str
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.node_id,
            "type": self.node_type,
            "label": self.label,
            "metadata": dict(self.metadata),
        }


@dataclass(frozen=True)
class GraphEdge:
    source: str
    target: str
    relation: str
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "from": self.source,
            "to": self.target,
            "relation": self.relation,
            "metadata": dict(self.metadata),
        }


@dataclass(frozen=True)
class ProjectGraph:
    nodes: list[GraphNode]
    edges: list[GraphEdge]

    def to_dict(self) -> dict[str, Any]:
        return {
            "nodes": [node.to_dict() for node in self.nodes],
            "edges": [edge.to_dict() for edge in self.edges],
        }


@dataclass(frozen=True)
class EventCondition:
    kind: str
    target: str
    operator: str
    value: Any

    def to_dict(self) -> dict[str, Any]:
        return {
            "kind": self.kind,
            "target": self.target,
            "operator": self.operator,
            "value": self.value,
        }


@dataclass(frozen=True)
class EventAction:
    kind: str
    target: str
    parameters: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "kind": self.kind,
            "target": self.target,
            "parameters": dict(self.parameters),
        }


@dataclass(frozen=True)
class EventRule:
    rule_id: str
    label: str
    conditions: list[EventCondition]
    actions: list[EventAction]
    priority: int = 100
    enabled: bool = True

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.rule_id,
            "label": self.label,
            "enabled": self.enabled,
            "priority": self.priority,
            "conditions": [condition.to_dict() for condition in self.conditions],
            "actions": [action.to_dict() for action in self.actions],
        }


@dataclass(frozen=True)
class EventSheet:
    scene_id: str
    rules: list[EventRule]

    def to_dict(self) -> dict[str, Any]:
        return {
            "scene_id": self.scene_id,
            "rules": [rule.to_dict() for rule in sorted(self.rules, key=lambda item: (item.priority, item.rule_id))],
        }


@dataclass(frozen=True)
class SceneSpec:
    scene_id: str
    label: str
    objects: list[dict[str, Any]]
    event_sheet: EventSheet

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.scene_id,
            "label": self.label,
            "objects": [dict(item) for item in self.objects],
            "event_sheet": self.event_sheet.to_dict(),
        }


@dataclass(frozen=True)
class EngineProjectSpec:
    project_name: str
    goal: str
    graph: ProjectGraph
    scenes: list[SceneSpec]
    modules: list[str]
    visibility: dict[str, Any] = field(default_factory=lambda: dict(LOCAL_ONLY_VISIBILITY))
    boundaries: list[str] = field(
        default_factory=lambda: [
            "LOCAL_ONLY",
            "NO_PUBLICAR",
            "no external channel actions",
            "no private RPG/TCG/game_bridge input",
            "no source-code copying from reference projects",
        ]
    )

    def to_dict(self) -> dict[str, Any]:
        payload = {
            "schema": PROJECT_SPEC_SCHEMA,
            "project_name": self.project_name,
            "goal": self.goal,
            "visibility": dict(self.visibility),
            "boundaries": list(self.boundaries),
            "modules": list(self.modules),
            "project_graph": self.graph.to_dict(),
            "scenes": [scene.to_dict() for scene in self.scenes],
        }
        payload["fingerprint"] = fingerprint_payload(payload)
        return payload


def build_observatorio_sandbox_project(
    *,
    project_name: str = "wabi_sabi_observatorio_sandbox",
) -> dict[str, Any]:
    graph = ProjectGraph(
        nodes=[
            GraphNode("app_shell", "app_core", "Local app shell", {"route": "/"}),
            GraphNode("scene_observatorio", "game_core.scene", "Observatorio scene", {"local_only": True}),
            GraphNode("event_sheet_observatorio", "game_core.event_sheet", "Declarative event sheet"),
            GraphNode("programmer_core", "programmer_core", "Task spec generator"),
            GraphNode("extension_registry", "modular_core", "Capability registry"),
        ],
        edges=[
            GraphEdge("app_shell", "scene_observatorio", "hosts"),
            GraphEdge("scene_observatorio", "event_sheet_observatorio", "uses"),
            GraphEdge("event_sheet_observatorio", "programmer_core", "generates_task_specs_for"),
            GraphEdge("extension_registry", "event_sheet_observatorio", "constrains_capabilities"),
        ],
    )
    scene = SceneSpec(
        scene_id="scene_observatorio",
        label="Observatorio Sandbox",
        objects=[
            {"id": "observe_button", "type": "button", "label": "Observe", "state": {"enabled": True}},
            {"id": "residue_meter", "type": "meter", "label": "R", "state": {"value": 0.15}},
            {"id": "signal_log", "type": "log", "label": "Signal Log", "state": {"entries": []}},
            {"id": "pattern_marker", "type": "marker", "label": "Pattern", "state": {"visible": False}},
        ],
        event_sheet=EventSheet(
            scene_id="scene_observatorio",
            rules=[
                EventRule(
                    rule_id="observe_click_records_signal",
                    label="Click observe records one signal",
                    priority=10,
                    conditions=[
                        EventCondition("input", "observe_button", "clicked", True),
                    ],
                    actions=[
                        EventAction("state.increment", "scene.observation_count", {"amount": 1}),
                        EventAction("log.append", "signal_log", {"message": "observation_recorded"}),
                        EventAction("state.add", "residue_meter.value", {"amount": -0.01, "min": 0.0}),
                    ],
                ),
                EventRule(
                    rule_id="three_signals_reveal_pattern",
                    label="Three observations reveal the pattern marker",
                    priority=20,
                    conditions=[
                        EventCondition("state", "scene.observation_count", ">=", 3),
                        EventCondition("state", "pattern_marker.visible", "==", False),
                    ],
                    actions=[
                        EventAction("state.set", "pattern_marker.visible", {"value": True}),
                        EventAction("log.append", "signal_log", {"message": "pattern_visible"}),
                    ],
                ),
                EventRule(
                    rule_id="residue_floor_keeps_local_review",
                    label="Residue floor keeps the sandbox in review mode",
                    priority=30,
                    conditions=[
                        EventCondition("state", "residue_meter.value", "<=", 0.05),
                    ],
                    actions=[
                        EventAction("gate.set", "sandbox.action_gate", {"value": "REVIEW"}),
                    ],
                ),
            ],
        ),
    )
    spec = EngineProjectSpec(
        project_name=project_name,
        goal=(
            "LOCAL_ONLY NO_PUBLICAR sandbox with declarative scene, event sheet, "
            "project graph, extension registry and programmer_core task-spec lane"
        ),
        graph=graph,
        scenes=[scene],
        modules=[
            "observation_kernel",
            "project_graph",
            "app_core",
            "game_core",
            "programmer_core",
            "extension_registry",
        ],
    )
    payload = spec.to_dict()
    validate_engine_project_spec(payload)
    return payload


def simulate_engine_project(
    spec: dict[str, Any],
    events: list[dict[str, Any]],
    *,
    initial_state: dict[str, Any] | None = None,
) -> dict[str, Any]:
    validation = validate_engine_project_spec(spec)
    if not validation["ok"]:
        raise ValueError("invalid_engine_project_spec:" + ";".join(validation["errors"]))
    state = _initial_state(spec)
    if initial_state:
        state.update(dict(initial_state))
    fired_rules: list[dict[str, Any]] = []
    logs: list[dict[str, Any]] = []
    for event_index, event in enumerate(events):
        context = {"event": dict(event), "event_index": event_index}
        for scene in spec["scenes"]:
            for rule in scene["event_sheet"]["rules"]:
                if not rule.get("enabled", True):
                    continue
                if _rule_matches(rule, state, context):
                    _apply_actions(rule["actions"], state, logs, context)
                    fired_rules.append(
                        {
                            "event_index": event_index,
                            "scene_id": scene["id"],
                            "rule_id": rule["id"],
                        }
                    )
    return {
        "schema": "wabi.engine.simulation_result.v1",
        "project_name": spec["project_name"],
        "project_fingerprint": spec["fingerprint"],
        "event_count": len(events),
        "fired_rules": fired_rules,
        "state": state,
        "logs": logs,
        "ok": True,
    }


def observatorio_click_events(count: int) -> list[dict[str, Any]]:
    if count < 0:
        raise ValueError("click_count_must_be_non_negative")
    return [
        {
            "kind": "input",
            "target": "observe_button",
            "event": "clicked",
            "value": True,
        }
        for _ in range(count)
    ]


def validate_engine_project_spec(spec: dict[str, Any]) -> dict[str, Any]:
    errors: list[str] = []
    if spec.get("schema") != PROJECT_SPEC_SCHEMA:
        errors.append("unsupported_project_spec_schema")
    visibility = spec.get("visibility", {})
    if visibility.get("classification") != "LOCAL_ONLY":
        errors.append("project_spec_visibility_must_be_local_only")
    if visibility.get("publish_allowed") is not False:
        errors.append("project_spec_publish_must_be_false")
    graph = spec.get("project_graph", {})
    errors.extend(_validate_graph(graph))
    raw_scenes = spec.get("scenes", [])
    if not isinstance(raw_scenes, list):
        raw_scenes = []
        errors.append("project_spec_scenes_must_be_list")
    scene_ids = set()
    for index, scene in enumerate(raw_scenes):
        if not isinstance(scene, dict):
            errors.append(f"scene_must_be_object:{index}")
            continue
        scene_id = str(scene.get("id", "")).strip()
        if not scene_id:
            errors.append(f"scene_id_required:{index}")
        if scene_id in scene_ids:
            errors.append(f"duplicate_scene_id:{scene_id}")
        scene_ids.add(scene_id)
        event_sheet = scene.get("event_sheet", {})
        errors.extend(_validate_event_sheet(event_sheet, scene_id=scene_id, index=index))
    if not raw_scenes:
        errors.append("project_spec_requires_scene")
    private_hits = _private_marker_hits(spec)
    if private_hits:
        errors.append("private_path_marker_present:" + ",".join(private_hits))
    expected = dict(spec)
    provided_fingerprint = expected.pop("fingerprint", None)
    computed = fingerprint_payload(expected)
    if provided_fingerprint and provided_fingerprint != computed:
        errors.append("project_spec_fingerprint_mismatch")
    return {
        "ok": not errors,
        "schema": "wabi.engine.project_validation.v1",
        "fingerprint": provided_fingerprint or computed,
        "errors": errors,
        "node_count": len(graph.get("nodes", [])) if isinstance(graph, dict) else 0,
        "edge_count": len(graph.get("edges", [])) if isinstance(graph, dict) else 0,
        "scene_count": len(raw_scenes),
    }


def load_engine_project_spec(workspace: str | Path, spec_ref: str | Path) -> dict[str, Any]:
    workspace_path = Path(workspace).resolve()
    spec_path = Path(spec_ref)
    if not spec_path.is_absolute():
        spec_path = workspace_path / spec_path
    spec_path = spec_path.resolve()
    try:
        spec_path.relative_to(workspace_path)
    except ValueError as exc:
        raise ValueError("engine_project_spec_must_be_inside_workspace") from exc
    data = json.loads(spec_path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("engine_project_spec_must_be_json_object")
    return data


def write_engine_project_spec(workspace: str | Path, spec: dict[str, Any]) -> Path:
    validation = validate_engine_project_spec(spec)
    if not validation["ok"]:
        raise ValueError("invalid_engine_project_spec:" + ";".join(validation["errors"]))
    workspace_path = Path(workspace).resolve()
    project_name = _slugify(str(spec.get("project_name", "engine_project")))
    target_dir = workspace_path / "docs" / "engine" / "local_only"
    target_dir.mkdir(parents=True, exist_ok=True)
    target = target_dir / f"{project_name}_PROJECT_SPEC.json"
    target.write_text(canonical_json(spec, indent=2), encoding="utf-8")
    return target


def canonical_json(payload: dict[str, Any], *, indent: int | None = None) -> str:
    return json.dumps(payload, ensure_ascii=False, sort_keys=True, indent=indent)


def fingerprint_payload(payload: dict[str, Any]) -> str:
    clean = dict(payload)
    clean.pop("fingerprint", None)
    encoded = json.dumps(clean, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _initial_state(spec: dict[str, Any]) -> dict[str, Any]:
    state: dict[str, Any] = {
        "scene.observation_count": 0,
        "sandbox.action_gate": "APPROVE",
    }
    for scene in spec.get("scenes", []):
        for item in scene.get("objects", []):
            object_id = item.get("id")
            if not object_id:
                continue
            for key, value in item.get("state", {}).items():
                state[f"{object_id}.{key}"] = value
    return state


def _rule_matches(rule: dict[str, Any], state: dict[str, Any], context: dict[str, Any]) -> bool:
    return all(_condition_matches(condition, state, context) for condition in rule.get("conditions", []))


def _condition_matches(condition: dict[str, Any], state: dict[str, Any], context: dict[str, Any]) -> bool:
    kind = condition.get("kind")
    target = condition.get("target")
    operator = condition.get("operator")
    expected = condition.get("value")
    if kind == "input":
        event = context["event"]
        actual = event.get("value")
        return event.get("kind") == "input" and event.get("target") == target and event.get("event") == operator and actual == expected
    if kind == "state":
        actual = state.get(target)
        return _compare(actual, operator, expected)
    return False


def _compare(actual: Any, operator: str, expected: Any) -> bool:
    if operator == "==":
        return actual == expected
    if operator == "!=":
        return actual != expected
    if operator in {">", ">=", "<", "<="}:
        try:
            left = float(actual)
            right = float(expected)
        except (TypeError, ValueError):
            return False
        if operator == ">":
            return left > right
        if operator == ">=":
            return left >= right
        if operator == "<":
            return left < right
        if operator == "<=":
            return left <= right
    return False


def _apply_actions(
    actions: list[dict[str, Any]],
    state: dict[str, Any],
    logs: list[dict[str, Any]],
    context: dict[str, Any],
) -> None:
    for action in actions:
        kind = action.get("kind")
        target = action.get("target")
        parameters = action.get("parameters", {})
        if kind == "state.increment":
            amount = parameters.get("amount", 1)
            state[target] = state.get(target, 0) + amount
        elif kind == "state.add":
            amount = parameters.get("amount", 0)
            value = state.get(target, 0) + amount
            if "min" in parameters:
                value = max(parameters["min"], value)
            if "max" in parameters:
                value = min(parameters["max"], value)
            state[target] = round(value, 10) if isinstance(value, float) else value
        elif kind == "state.set":
            state[target] = parameters.get("value")
        elif kind == "gate.set":
            state[target] = parameters.get("value")
        elif kind == "log.append":
            entry = {
                "event_index": context["event_index"],
                "target": target,
                "message": parameters.get("message", ""),
            }
            logs.append(entry)
            existing = state.get(f"{target}.entries", [])
            if isinstance(existing, list):
                state[f"{target}.entries"] = [*existing, entry["message"]]


def _validate_graph(graph: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(graph, dict):
        return ["project_graph_must_be_object"]
    nodes = graph.get("nodes", [])
    edges = graph.get("edges", [])
    if not isinstance(nodes, list) or not nodes:
        errors.append("project_graph_requires_nodes")
        nodes = []
    if not isinstance(edges, list):
        errors.append("project_graph_edges_must_be_list")
        edges = []
    ids: set[str] = set()
    for index, node in enumerate(nodes):
        node_id = str(node.get("id", "")).strip() if isinstance(node, dict) else ""
        if not node_id:
            errors.append(f"node_id_required:{index}")
            continue
        if node_id in ids:
            errors.append(f"duplicate_node_id:{node_id}")
        ids.add(node_id)
    for index, edge in enumerate(edges):
        source = str(edge.get("from", "")).strip() if isinstance(edge, dict) else ""
        target = str(edge.get("to", "")).strip() if isinstance(edge, dict) else ""
        if source not in ids:
            errors.append(f"edge_source_missing:{index}:{source}")
        if target not in ids:
            errors.append(f"edge_target_missing:{index}:{target}")
    return errors


def _validate_event_sheet(event_sheet: Any, *, scene_id: str, index: int) -> list[str]:
    errors: list[str] = []
    if not isinstance(event_sheet, dict):
        return [f"event_sheet_must_be_object:{index}"]
    if event_sheet.get("scene_id") != scene_id:
        errors.append(f"event_sheet_scene_mismatch:{index}")
    rules = event_sheet.get("rules", [])
    if not isinstance(rules, list) or not rules:
        return errors + [f"event_sheet_requires_rules:{index}"]
    rule_ids: set[str] = set()
    for rule_index, rule in enumerate(rules):
        rule_id = str(rule.get("id", "")).strip() if isinstance(rule, dict) else ""
        if not rule_id:
            errors.append(f"event_rule_id_required:{index}:{rule_index}")
            continue
        if rule_id in rule_ids:
            errors.append(f"duplicate_event_rule_id:{rule_id}")
        rule_ids.add(rule_id)
        conditions = rule.get("conditions", []) if isinstance(rule, dict) else []
        actions = rule.get("actions", []) if isinstance(rule, dict) else []
        if not isinstance(conditions, list) or not conditions:
            errors.append(f"event_rule_requires_conditions:{rule_id}")
        if not isinstance(actions, list) or not actions:
            errors.append(f"event_rule_requires_actions:{rule_id}")
    return errors


def _private_marker_hits(spec: dict[str, Any]) -> list[str]:
    hits: set[str] = set()

    def walk(value: Any, key: str = "") -> None:
        if isinstance(value, dict):
            for child_key, child in value.items():
                walk(child, str(child_key))
            return
        if isinstance(value, list):
            for child in value:
                walk(child, key)
            return
        if not isinstance(value, str):
            return
        lowered = value.lower()
        looks_like_path = key.lower().endswith(("path", "paths", "file", "dir"))
        if not looks_like_path:
            return
        for marker in PRIVATE_PATH_MARKERS:
            if marker in lowered:
                hits.add(marker)

    walk(spec)
    return sorted(hits)


def _slugify(value: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9]+", "_", value.strip().lower()).strip("_")
    return slug or "engine_project"
