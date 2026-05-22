from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from wabi_sabi.core.patch_planner import (
    SENSITIVE_PATH_PARTS,
    PatchPlan,
    build_multi_file_patch_plan,
    resolve_workspace_text_target,
)


TASK_SPEC_SCHEMA = "wabi.task_spec.v1"
MAX_CHANGES = 20
MAX_CONTENT_CHARS = 250_000
TASK_SPEC_INPUT_BLOCKED_PARTS = SENSITIVE_PATH_PARTS - {"runtime"}


@dataclass(frozen=True)
class TaskSpec:
    path: Path
    summary: str
    changes: list[dict[str, Any]]
    test_commands: list[str]
    raw: dict[str, Any]

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema": TASK_SPEC_SCHEMA,
            "path": str(self.path),
            "summary": self.summary,
            "changes": [
                {
                    "target": change["target"],
                    "suffix": change.get("suffix"),
                    "content_sha256": change.get("content_sha256"),
                }
                for change in self.changes
            ],
            "test_commands": list(self.test_commands),
        }


def load_task_spec(
    *,
    workspace: Path,
    spec_path: str | Path,
    input_roots: list[str | Path] | None = None,
) -> TaskSpec:
    workspace = workspace.resolve()
    path = _resolve_task_spec_input(workspace, spec_path, input_roots=input_roots)
    raw = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        raise ValueError("task_spec_must_be_json_object")
    schema = raw.get("schema")
    if schema not in {TASK_SPEC_SCHEMA, None}:
        raise ValueError(f"unsupported_task_spec_schema:{schema}")
    summary = str(raw.get("summary") or raw.get("title") or path.stem).strip()
    if not summary:
        raise ValueError("task_spec_summary_required")
    raw_changes = raw.get("changes")
    if not isinstance(raw_changes, list) or not raw_changes:
        raise ValueError("task_spec_changes_required")
    if len(raw_changes) > MAX_CHANGES:
        raise ValueError(f"task_spec_too_many_changes:{len(raw_changes)}")

    changes: list[dict[str, Any]] = []
    for index, item in enumerate(raw_changes):
        if not isinstance(item, dict):
            raise ValueError(f"task_spec_change_must_be_object:{index}")
        if item.get("operation", "write_text") != "write_text":
            raise ValueError(f"unsupported_task_spec_operation:{item.get('operation')}")
        target = item.get("target")
        if not isinstance(target, str) or not target.strip():
            raise ValueError(f"task_spec_target_required:{index}")
        content = _resolve_change_content(workspace=workspace, spec_dir=path.parent, item=item, index=index)
        if len(content) > MAX_CONTENT_CHARS:
            raise ValueError(f"task_spec_content_too_large:{index}")
        changes.append(
            {
                "target": target,
                "content": content,
                "suffix": item.get("suffix"),
                "content_sha256": item.get("content_sha256"),
            }
        )
    test_commands = raw.get("test_commands", [])
    if not isinstance(test_commands, list):
        raise ValueError("task_spec_test_commands_must_be_list")
    commands = [str(command) for command in test_commands]
    return TaskSpec(path=path, summary=summary, changes=changes, test_commands=commands, raw=raw)


def build_patch_plan_from_task_spec(
    *,
    workspace: Path,
    spec_path: str | Path,
    input_roots: list[str | Path] | None = None,
) -> tuple[TaskSpec, PatchPlan]:
    spec = load_task_spec(workspace=workspace, spec_path=spec_path, input_roots=input_roots)
    plan = build_multi_file_patch_plan(
        workspace=workspace,
        changes=spec.changes,
        summary=spec.summary,
        test_commands=spec.test_commands,
    )
    return spec, plan


def _resolve_change_content(*, workspace: Path, spec_dir: Path, item: dict[str, Any], index: int) -> str:
    has_content = "content" in item
    has_content_file = "content_file" in item
    if has_content == has_content_file:
        raise ValueError(f"task_spec_exactly_one_content_source_required:{index}")
    if has_content:
        content = item["content"]
        if not isinstance(content, str):
            raise ValueError(f"task_spec_content_must_be_string:{index}")
        return content
    raw_path = Path(str(item["content_file"]))
    candidate = raw_path.resolve() if raw_path.is_absolute() else (spec_dir / raw_path).resolve()
    workspace = workspace.resolve()
    if candidate != workspace and workspace not in candidate.parents:
        raise ValueError(f"task_spec_content_file_outside_workspace:{candidate}")
    return candidate.read_text(encoding="utf-8")


def _resolve_task_spec_input(
    workspace: Path,
    spec_path: str | Path,
    *,
    input_roots: list[str | Path] | None = None,
) -> Path:
    workspace = workspace.resolve()
    raw = Path(spec_path)
    candidate = raw.resolve() if raw.is_absolute() else (workspace / raw).resolve()
    allowed_roots = [workspace]
    allowed_roots.extend(Path(root).resolve() for root in (input_roots or []))
    if not any(candidate == root or root in candidate.parents for root in allowed_roots):
        raise ValueError(f"target_outside_workspace:{candidate}")
    lowered_parts = {part.lower() for part in candidate.parts}
    blocked = sorted(TASK_SPEC_INPUT_BLOCKED_PARTS.intersection(lowered_parts))
    if blocked:
        raise ValueError("task_spec_path_blocked:" + ",".join(blocked))
    if candidate.suffix.lower() != ".json":
        raise ValueError("only_json_task_specs_supported")
    return candidate
