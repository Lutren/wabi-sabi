from __future__ import annotations

import difflib
import hashlib
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from wabi_sabi.core.tools import stamp


SENSITIVE_PATH_PARTS = {
    ".git",
    ".claw",
    ".claude",
    ".wrangler",
    ".env",
    ".venv",
    ".venv_api",
    "node_modules",
    "runtime",
    "releases",
    "release",
    "dist",
    "build",
    "target",
    "game-private",
    "metaevo-tcg",
    "tcg",
    "game_bridge",
}


@dataclass(frozen=True)
class PatchOperation:
    relative_path: str
    operation: str
    existed: bool
    before_hash: str
    after_hash: str
    content: str
    diff: str
    changed: bool

    def to_dict(self) -> dict[str, Any]:
        return {
            "relative_path": self.relative_path,
            "operation": self.operation,
            "existed": self.existed,
            "before_hash": self.before_hash,
            "after_hash": self.after_hash,
            "content": self.content,
            "diff": self.diff,
            "changed": self.changed,
        }


@dataclass(frozen=True)
class PatchPlan:
    plan_id: str
    created_at: str
    workspace: str
    summary: str
    gate: str
    reasons: list[str]
    operations: list[PatchOperation]
    test_commands: list[str]

    @property
    def changed(self) -> bool:
        return any(operation.changed for operation in self.operations)

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema": "wabi.patch_plan.v1",
            "plan_id": self.plan_id,
            "created_at": self.created_at,
            "workspace": self.workspace,
            "summary": self.summary,
            "gate": self.gate,
            "reasons": list(self.reasons),
            "changed": self.changed,
            "test_commands": list(self.test_commands),
            "operations": [operation.to_dict() for operation in self.operations],
        }


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def resolve_workspace_text_target(workspace: Path, target: str | Path, *, suffix: str | None = None) -> Path:
    workspace = workspace.resolve()
    raw = Path(target)
    candidate = raw.resolve() if raw.is_absolute() else (workspace / raw).resolve()
    if candidate != workspace and workspace not in candidate.parents:
        raise ValueError(f"target_outside_workspace:{candidate}")
    relative_parts = candidate.relative_to(workspace).parts if candidate != workspace else ()
    lowered_parts = {part.lower() for part in relative_parts}
    blocked = sorted(SENSITIVE_PATH_PARTS.intersection(lowered_parts))
    if blocked:
        raise ValueError("target_path_blocked:" + ",".join(blocked))
    if suffix and candidate.suffix.lower() != suffix.lower():
        raise ValueError(f"only_{suffix.lstrip('.').lower()}_targets_supported")
    return candidate


def build_file_patch_plan(
    *,
    workspace: Path,
    target: str | Path,
    content: str,
    summary: str,
    suffix: str | None = None,
    test_commands: list[str] | None = None,
) -> PatchPlan:
    return build_multi_file_patch_plan(
        workspace=workspace,
        changes=[{"target": target, "content": content, "suffix": suffix}],
        summary=summary,
        test_commands=test_commands,
    )


def build_multi_file_patch_plan(
    *,
    workspace: Path,
    changes: list[dict[str, Any]],
    summary: str,
    test_commands: list[str] | None = None,
) -> PatchPlan:
    workspace = workspace.resolve()
    operations: list[PatchOperation] = []
    seen: set[str] = set()
    for change in changes:
        target_path = resolve_workspace_text_target(workspace, change["target"], suffix=change.get("suffix"))
        rel = target_path.relative_to(workspace).as_posix()
        if rel in seen:
            raise ValueError(f"duplicate_patch_target:{rel}")
        seen.add(rel)
        content = str(change["content"])
        old_text = target_path.read_text(encoding="utf-8") if target_path.exists() else ""
        before_hash = sha256_text(old_text)
        after_hash = sha256_text(content)
        diff_text = "".join(
            difflib.unified_diff(
                old_text.splitlines(keepends=True),
                content.splitlines(keepends=True),
                fromfile=f"a/{rel}",
                tofile=f"b/{rel}",
            )
        )
        operations.append(
            PatchOperation(
                relative_path=rel,
                operation="write_text",
                existed=target_path.exists(),
                before_hash=before_hash,
                after_hash=after_hash,
                content=content,
                diff=diff_text or f"# no textual change for {rel}\n",
                changed=old_text != content,
            )
        )
    if not operations:
        raise ValueError("empty_patch_plan")
    commands = list(test_commands or [])
    plan_hash = sha256_text(
        json.dumps(
            {
                "operations": [operation.to_dict() for operation in operations],
                "test_commands": commands,
            },
            sort_keys=True,
            ensure_ascii=False,
        )
    )
    created_at = stamp()
    plan_id = f"patch-{created_at}-{plan_hash[:12]}"
    return PatchPlan(
        plan_id=plan_id,
        created_at=created_at,
        workspace=str(workspace),
        summary=summary,
        gate="APPROVE",
        reasons=["text_patch_plan", "targets_inside_workspace", "sensitive_paths_blocked"],
        operations=operations,
        test_commands=commands,
    )


def write_patch_plan(output_dir: Path, plan: PatchPlan) -> Path:
    directory = output_dir / "patch_plans"
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / f"{plan.plan_id}.json"
    path.write_text(json.dumps(plan.to_dict(), indent=2, ensure_ascii=False), encoding="utf-8")
    return path


def write_patch_diff(output_dir: Path, plan: PatchPlan) -> Path:
    directory = output_dir
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / f"{plan.plan_id}.diff"
    diff_text = "\n".join(operation.diff.rstrip("\n") for operation in plan.operations)
    path.write_text(diff_text.rstrip() + "\n", encoding="utf-8")
    return path


def patch_plan_from_dict(payload: dict[str, Any]) -> PatchPlan:
    operations = [
        PatchOperation(
            relative_path=str(item["relative_path"]),
            operation=str(item["operation"]),
            existed=bool(item["existed"]),
            before_hash=str(item["before_hash"]),
            after_hash=str(item["after_hash"]),
            content=str(item["content"]),
            diff=str(item["diff"]),
            changed=bool(item["changed"]),
        )
        for item in payload.get("operations", [])
    ]
    return PatchPlan(
        plan_id=str(payload["plan_id"]),
        created_at=str(payload["created_at"]),
        workspace=str(payload["workspace"]),
        summary=str(payload["summary"]),
        gate=str(payload["gate"]),
        reasons=[str(item) for item in payload.get("reasons", [])],
        operations=operations,
        test_commands=[str(item) for item in payload.get("test_commands", [])],
    )


def load_patch_plan(path: str | Path) -> PatchPlan:
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    return patch_plan_from_dict(payload)
