from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any, Mapping

from wabi_sabi.core.patch_planner import (
    PatchPlan,
    build_multi_file_patch_plan,
    load_patch_plan,
    write_patch_diff,
    write_patch_plan,
)
from wabi_sabi.core.redaction import redact_mapping, redact_text
from wabi_sabi.core.safe_executor import SafeExecutor
from wabi_sabi.core.tools import write_artifact


LOCAL_APPLY_NOT_READY = "LOCAL_APPLY_NOT_READY"
LOCAL_APPLY_READY = "LOCAL_APPLY_READY"
LOCAL_APPLY_BLOCKED_PATH = "LOCAL_APPLY_BLOCKED_PATH"
LOCAL_APPLY_BLOCKED_SECRET = "LOCAL_APPLY_BLOCKED_SECRET"
LOCAL_APPLY_BLOCKED_BOUNDARY = "LOCAL_APPLY_BLOCKED_BOUNDARY"
LOCAL_APPLY_PATCH_READY = "LOCAL_APPLY_PATCH_READY"
LOCAL_APPLY_APPLIED = "LOCAL_APPLY_APPLIED"
LOCAL_APPLY_TESTS_PASS = "LOCAL_APPLY_TESTS_PASS"
LOCAL_APPLY_TESTS_FAIL_ROLLED_BACK = "LOCAL_APPLY_TESTS_FAIL_ROLLED_BACK"
LOCAL_APPLY_REVIEW_REQUIRED = "LOCAL_APPLY_REVIEW_REQUIRED"

LOCAL_APPLY_SCHEMA = "wabi.local_apply_readiness.v0_1"
PATCH_CANDIDATE_SCHEMA = "wabi.local_apply.patch_candidate.v0_1"

TEXT_SUFFIXES = {
    ".py",
    ".md",
    ".txt",
    ".json",
    ".yaml",
    ".yml",
    ".html",
    ".css",
    ".js",
    ".ts",
    ".tsx",
}

BLOCKED_PATH_PARTS = {
    ".git",
    ".env",
    ".venv",
    "venv",
    "node_modules",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    "dist",
    "build",
    "releases",
    "release",
    "secrets",
    "secret",
    "credentials",
    "tokens",
    "vault",
    "source_vault",
    "datasets",
    "private",
    "books",
    "lore",
    "game-private",
}

SECRET_PATTERNS = [
    re.compile(r"sk-[A-Za-z0-9_\-]{16,}"),
    re.compile(r"(?i)\b(api[_-]?key|token|secret|password|credential)\b\s*[:=]\s*['\"]?[^'\"\s]{8,}"),
    re.compile(r"(?i)\b(nvapi|nvidia)[A-Za-z0-9_\-]{20,}"),
]

PRIVATE_BOUNDARY_PATTERNS = [
    re.compile(r"(?i)c:\\users\\"),
    re.compile(r"(?i)onedrive"),
    re.compile(r"(?i)-= brain_os =-"),
    re.compile(r"(?i)-=l\.rgonzalez=-"),
]


def evaluate_local_apply_readiness(
    task_spec: Mapping[str, Any] | None,
    *,
    workspace: str | Path | None = None,
    runtime_root: str | Path | None = None,
) -> dict[str, Any]:
    candidate = build_patch_candidate(task_spec or {}, workspace=workspace, runtime_root=runtime_root)
    ready = candidate.get("readiness") == LOCAL_APPLY_READY
    return redact_mapping(
        {
            "schema": LOCAL_APPLY_SCHEMA,
            "status": LOCAL_APPLY_READY if ready else candidate.get("readiness", LOCAL_APPLY_NOT_READY),
            "ready": ready,
            "task_id": candidate.get("task_id", ""),
            "summary": candidate.get("summary", ""),
            "affected_paths": candidate.get("affected_paths", []),
            "tests_to_run": candidate.get("tests_to_run", []),
            "rollback_snapshot_required": True,
            "apply_mode": "local_allowlisted",
            "proposal_only": False if ready else True,
            "applied_to_sources": False,
            "cloud_provider_called": False,
            "graphics_live": False,
            "secret_scan": candidate.get("secret_scan", {}),
            "boundary_scan": candidate.get("boundary_scan", {}),
            "path_allowlist": candidate.get("path_allowlist", {}),
            "blockers": candidate.get("blockers", []),
            "next_safe_action": (
                "Run apply-local after reviewing patch candidate."
                if ready
                else "Review TaskSpec and add explicit, allowlisted implementation details."
            ),
        }
    )


def validate_path_allowlist(
    task_spec: Mapping[str, Any] | None,
    *,
    workspace: str | Path | None = None,
    runtime_root: str | Path | None = None,
) -> dict[str, Any]:
    candidate = build_patch_candidate(task_spec or {}, workspace=workspace, runtime_root=runtime_root)
    return redact_mapping(candidate.get("path_allowlist", {}))


def build_patch_candidate(
    task_spec: Mapping[str, Any] | None,
    *,
    workspace: str | Path | None = None,
    runtime_root: str | Path | None = None,
) -> dict[str, Any]:
    root = _workspace_root(workspace)
    runtime = _runtime_root(runtime_root)
    spec = dict(task_spec or {})
    task_id = str(spec.get("task_id") or spec.get("fingerprint") or "taskspec-local-apply")
    intent_name = str(spec.get("intent_name") or "chat_general")
    blockers: list[str] = []

    if bool(spec.get("needs_cloud")):
        blockers.append("Cloud-involved TaskSpecs remain proposal_only and cannot be applied directly.")
    if bool(spec.get("needs_graphics")):
        blockers.append("Graphics TaskSpecs remain plan-only; graphics_live=false.")
    if bool(spec.get("cloud_provider_called")):
        blockers.append("Cloud provider output cannot be applied by Local Apply.")

    changes, tests_to_run, summary = _changes_from_task_spec(spec, intent_name)
    if not changes:
        blockers.append("TaskSpec does not contain enough implementation detail for local apply.")
    if blockers:
        return _blocked_candidate(
            status=LOCAL_APPLY_REVIEW_REQUIRED,
            task_id=task_id,
            summary=summary,
            blockers=blockers,
            root=root,
            tests_to_run=tests_to_run,
        )

    try:
        plan = build_multi_file_patch_plan(
            workspace=root,
            changes=changes,
            summary=summary,
            test_commands=tests_to_run,
        )
    except Exception as exc:
        return _blocked_candidate(
            status=LOCAL_APPLY_BLOCKED_PATH,
            task_id=task_id,
            summary=summary,
            blockers=[redact_text(str(exc))],
            root=root,
            tests_to_run=tests_to_run,
        )

    path_scan = _scan_plan_paths(plan, root)
    if not path_scan["allowed"]:
        return _candidate_from_plan(
            plan=plan,
            task_id=task_id,
            runtime=runtime,
            readiness=LOCAL_APPLY_BLOCKED_PATH,
            blockers=path_scan["blockers"],
            path_scan=path_scan,
        )

    secret_scan = _scan_plan_secrets(plan)
    if secret_scan["status"] != "PASS":
        return _candidate_from_plan(
            plan=plan,
            task_id=task_id,
            runtime=runtime,
            readiness=LOCAL_APPLY_BLOCKED_SECRET,
            blockers=["Secret-like content detected in patch candidate."],
            path_scan=path_scan,
            secret_scan=secret_scan,
        )

    boundary_scan = _scan_plan_boundary(plan)
    if boundary_scan["status"] != "PASS":
        return _candidate_from_plan(
            plan=plan,
            task_id=task_id,
            runtime=runtime,
            readiness=LOCAL_APPLY_BLOCKED_BOUNDARY,
            blockers=["Private boundary marker detected in patch candidate."],
            path_scan=path_scan,
            secret_scan=secret_scan,
            boundary_scan=boundary_scan,
        )

    return _candidate_from_plan(
        plan=plan,
        task_id=task_id,
        runtime=runtime,
        readiness=LOCAL_APPLY_READY,
        blockers=[],
        path_scan=path_scan,
        secret_scan=secret_scan,
        boundary_scan=boundary_scan,
    )


def create_rollback_snapshot(
    affected_paths: list[str] | tuple[str, ...],
    *,
    workspace: str | Path | None = None,
    runtime_root: str | Path | None = None,
) -> dict[str, Any]:
    # The actual source snapshot is captured by SafeExecutor immediately before
    # writing. This function provides a read-only readiness contract for UI/CLI.
    root = _workspace_root(workspace)
    runtime = _runtime_root(runtime_root)
    payload = {
        "schema": "wabi.local_apply.rollback_snapshot_preview.v0_1",
        "status": "SNAPSHOT_REQUIRED_BEFORE_WRITE",
        "workspace": str(root),
        "runtime_root": str(runtime),
        "affected_paths": [str(path) for path in affected_paths],
        "rollback_snapshot_required": True,
        "applied_to_sources": False,
    }
    path = write_artifact(
        runtime / "outputs" / "local_apply",
        "rollback_snapshot_preview",
        ".json",
        json.dumps(redact_mapping(payload), indent=2, ensure_ascii=False) + "\n",
    )
    payload["artifact_path"] = str(path)
    return redact_mapping(payload)


def apply_patch_candidate(
    patch_candidate: Mapping[str, Any] | str | Path,
    *,
    workspace: str | Path | None = None,
    runtime_root: str | Path | None = None,
) -> dict[str, Any]:
    root = _workspace_root(workspace)
    runtime = _runtime_root(runtime_root)
    candidate = _load_candidate(patch_candidate)
    if candidate.get("readiness") != LOCAL_APPLY_READY:
        return produce_apply_report(
            {
                "status": candidate.get("readiness", LOCAL_APPLY_NOT_READY),
                "ok": False,
                "reason": "PATCH_CANDIDATE_NOT_READY",
                "patch_candidate": candidate,
                "applied_to_sources": False,
                "cloud_provider_called": False,
                "graphics_live": False,
            }
        )
    plan_path = candidate.get("patch_plan_path")
    if not plan_path:
        return produce_apply_report(
            {
                "status": LOCAL_APPLY_NOT_READY,
                "ok": False,
                "reason": "MISSING_PATCH_PLAN_PATH",
                "patch_candidate": candidate,
                "applied_to_sources": False,
            }
        )
    plan = load_patch_plan(str(plan_path))
    path_scan = _scan_plan_paths(plan, root)
    secret_scan = _scan_plan_secrets(plan)
    boundary_scan = _scan_plan_boundary(plan)
    if not path_scan["allowed"]:
        return produce_apply_report(
            {
                "status": LOCAL_APPLY_BLOCKED_PATH,
                "ok": False,
                "path_allowlist": path_scan,
                "secret_scan": secret_scan,
                "boundary_scan": boundary_scan,
                "applied_to_sources": False,
            }
        )
    if secret_scan["status"] != "PASS":
        return produce_apply_report(
            {
                "status": LOCAL_APPLY_BLOCKED_SECRET,
                "ok": False,
                "path_allowlist": path_scan,
                "secret_scan": secret_scan,
                "boundary_scan": boundary_scan,
                "applied_to_sources": False,
            }
        )
    if boundary_scan["status"] != "PASS":
        return produce_apply_report(
            {
                "status": LOCAL_APPLY_BLOCKED_BOUNDARY,
                "ok": False,
                "path_allowlist": path_scan,
                "secret_scan": secret_scan,
                "boundary_scan": boundary_scan,
                "applied_to_sources": False,
            }
        )

    execution = SafeExecutor(workspace=root, runtime_root=runtime).execute(plan)
    post_secret_scan = _scan_files_for_secrets(root, execution.written)
    post_boundary_scan = _scan_files_for_boundary(root, execution.written)
    ok = bool(execution.ok) and post_secret_scan["status"] == "PASS" and post_boundary_scan["status"] == "PASS"
    status = LOCAL_APPLY_TESTS_PASS if ok else LOCAL_APPLY_TESTS_FAIL_ROLLED_BACK
    result = {
        "schema": "wabi.local_apply.result.v0_1",
        "ok": ok,
        "status": status,
        "apply_status": LOCAL_APPLY_APPLIED if execution.ok else status,
        "task_id": candidate.get("task_id", ""),
        "patch_candidate": candidate,
        "execution": execution.to_dict(),
        "rollback_snapshot": str(execution.rollback_path),
        "tests": execution.test_results,
        "test_status": "PASS" if execution.ok else "FAIL_ROLLED_BACK",
        "secret_scan": post_secret_scan,
        "boundary_scan": post_boundary_scan,
        "applied_to_sources": bool(execution.ok),
        "cloud_provider_called": False,
        "graphics_live": False,
        "publication_gate": "BLOCK",
    }
    return produce_apply_report(result)


def run_required_tests(
    task_spec: Mapping[str, Any] | None,
    *,
    workspace: str | Path | None = None,
    runtime_root: str | Path | None = None,
) -> dict[str, Any]:
    candidate = build_patch_candidate(task_spec or {}, workspace=workspace, runtime_root=runtime_root)
    return {
        "schema": "wabi.local_apply.required_tests.v0_1",
        "status": "READY" if candidate.get("tests_to_run") else "REVIEW",
        "tests_to_run": candidate.get("tests_to_run", []),
        "applied_to_sources": False,
        "cloud_provider_called": False,
    }


def rollback_on_failure(
    snapshot: Mapping[str, Any] | str,
    *,
    workspace: str | Path | None = None,
    runtime_root: str | Path | None = None,
) -> dict[str, Any]:
    return {
        "schema": "wabi.local_apply.rollback_on_failure.v0_1",
        "status": "DELEGATED_TO_SAFE_EXECUTOR",
        "reason": "SafeExecutor restores rollback snapshots automatically when tests fail.",
        "snapshot_ref": redact_text(str(snapshot)),
        "workspace": str(_workspace_root(workspace)),
        "runtime_root": str(_runtime_root(runtime_root)),
        "applied_to_sources": False,
    }


def produce_apply_report(result: Mapping[str, Any]) -> dict[str, Any]:
    payload = {
        "schema": "wabi.local_apply.report.v0_1",
        "status": result.get("status", LOCAL_APPLY_REVIEW_REQUIRED),
        "ok": bool(result.get("ok", False)),
        "reason": result.get("reason", ""),
        "applied_to_sources": bool(result.get("applied_to_sources", False)),
        "cloud_provider_called": False,
        "graphics_live": False,
        "publication_gate": "BLOCK",
        "result": redact_mapping(dict(result)),
    }
    return redact_mapping(payload)


def preview_local_apply(
    task_spec: Mapping[str, Any] | None,
    *,
    workspace: str | Path | None = None,
    runtime_root: str | Path | None = None,
) -> dict[str, Any]:
    candidate = build_patch_candidate(task_spec or {}, workspace=workspace, runtime_root=runtime_root)
    return redact_mapping(
        {
            "schema": "wabi.local_apply.preview.v0_1",
            "ok": candidate.get("readiness") == LOCAL_APPLY_READY,
            "status": LOCAL_APPLY_PATCH_READY if candidate.get("readiness") == LOCAL_APPLY_READY else candidate.get("readiness"),
            "patch_candidate": candidate,
            "readiness": evaluate_local_apply_readiness(task_spec or {}, workspace=workspace, runtime_root=runtime_root),
            "rollback_preview": create_rollback_snapshot(candidate.get("affected_paths", []), workspace=workspace, runtime_root=runtime_root),
            "applied_to_sources": False,
            "cloud_provider_called": False,
            "graphics_live": False,
            "publication_gate": "BLOCK",
        }
    )


def apply_local_task_spec(
    task_spec: Mapping[str, Any] | None,
    *,
    workspace: str | Path | None = None,
    runtime_root: str | Path | None = None,
) -> dict[str, Any]:
    candidate = build_patch_candidate(task_spec or {}, workspace=workspace, runtime_root=runtime_root)
    if candidate.get("readiness") != LOCAL_APPLY_READY:
        return produce_apply_report(
            {
                "status": candidate.get("readiness", LOCAL_APPLY_NOT_READY),
                "ok": False,
                "reason": "LOCAL_APPLY_NOT_READY",
                "patch_candidate": candidate,
                "applied_to_sources": False,
                "cloud_provider_called": False,
                "graphics_live": False,
            }
        )
    return apply_patch_candidate(candidate, workspace=workspace, runtime_root=runtime_root)


def load_latest_taskspec(*, runtime_root: str | Path | None = None) -> dict[str, Any]:
    runtime = _runtime_root(runtime_root)
    candidates: list[Path] = []
    for folder in [
        runtime / "outputs" / "taskspec_review",
        runtime / "outputs" / "conversation_tasks",
    ]:
        if folder.exists():
            candidates.extend(folder.glob("*.json"))
    if not candidates:
        raise FileNotFoundError("no_latest_taskspec_found")
    latest = max(candidates, key=lambda path: path.stat().st_mtime)
    payload = json.loads(latest.read_text(encoding="utf-8"))
    if isinstance(payload.get("taskspec_review"), dict):
        return dict(payload["taskspec_review"])
    if isinstance(payload.get("task_spec"), dict):
        return dict(payload["task_spec"])
    return dict(payload)


def _changes_from_task_spec(spec: Mapping[str, Any], intent_name: str) -> tuple[list[dict[str, Any]], list[str], str]:
    summary = str(spec.get("summary") or spec.get("title") or "Local apply patch candidate")[:180]
    raw_changes = spec.get("changes")
    changes: list[dict[str, Any]] = []
    if isinstance(raw_changes, list):
        for item in raw_changes:
            if not isinstance(item, Mapping):
                continue
            target = item.get("target") or item.get("relative_path") or item.get("path")
            content = item.get("content") or item.get("new_text")
            if target and content is not None:
                changes.append({"target": str(target), "content": str(content), "suffix": item.get("suffix")})
    if changes:
        return changes, _tests_for_changes(spec, changes), summary
    if intent_name == "code_request" and _looks_like_json_helper_request(spec):
        return _json_helper_changes(), _json_helper_tests(), "Add safe JSON validation helper"
    return [], _tests_for_changes(spec, []), summary


def _looks_like_json_helper_request(spec: Mapping[str, Any]) -> bool:
    blob = json.dumps(spec, ensure_ascii=False, sort_keys=True).lower()
    return "json" in blob and ("helper" in blob or "valid" in blob or "validate" in blob or "seguro" in blob)


def _json_helper_changes() -> list[dict[str, Any]]:
    return build_safe_json_helper_changes()


def build_safe_json_helper_changes() -> list[dict[str, Any]]:
    helper = '''from __future__ import annotations

import json
from typing import Any, Iterable


def parse_json_object(text: str) -> tuple[bool, dict[str, Any], str]:
    """Parse a JSON object without hooks or side effects."""
    if not isinstance(text, str):
        return False, {}, "input_must_be_text"
    try:
        value = json.loads(text)
    except json.JSONDecodeError as exc:
        return False, {}, f"invalid_json:{exc.msg}"
    if not isinstance(value, dict):
        return False, {}, "json_root_must_be_object"
    return True, value, "ok"


def validate_json_object(text: str, required_keys: Iterable[str] = ()) -> dict[str, Any]:
    """Return a parsed object or raise ValueError with a stable reason."""
    ok, value, reason = parse_json_object(text)
    if not ok:
        raise ValueError(reason)
    missing = [key for key in required_keys if key not in value]
    if missing:
        raise ValueError("missing_required_keys:" + ",".join(sorted(missing)))
    return value
'''
    tests = '''from __future__ import annotations

import pytest

from wabi_sabi.core.json_safety import parse_json_object, validate_json_object


def test_parse_json_object_accepts_object() -> None:
    ok, value, reason = parse_json_object('{"status":"ok","count":1}')
    assert ok is True
    assert value == {"status": "ok", "count": 1}
    assert reason == "ok"


def test_parse_json_object_rejects_invalid_json() -> None:
    ok, value, reason = parse_json_object("{")
    assert ok is False
    assert value == {}
    assert reason.startswith("invalid_json:")


def test_parse_json_object_rejects_non_object_root() -> None:
    ok, value, reason = parse_json_object("[1, 2, 3]")
    assert ok is False
    assert value == {}
    assert reason == "json_root_must_be_object"


def test_validate_json_object_requires_keys() -> None:
    with pytest.raises(ValueError, match="missing_required_keys:mode"):
        validate_json_object('{"status":"ok"}', required_keys=["mode", "status"])


def test_validate_json_object_returns_object() -> None:
    assert validate_json_object('{"status":"ok"}', required_keys=["status"]) == {"status": "ok"}
'''
    return [
        {"target": "wabi_sabi/core/json_safety.py", "content": helper, "suffix": ".py"},
        {"target": "tests/test_json_safety.py", "content": tests, "suffix": ".py"},
    ]


def _json_helper_tests() -> list[str]:
    return safe_json_helper_test_commands()


def safe_json_helper_test_commands() -> list[str]:
    return [
        "python -B -m pytest tests/test_json_safety.py -q -p no:cacheprovider",
        "python -B -m py_compile wabi_sabi/core/json_safety.py",
    ]


def _tests_for_changes(spec: Mapping[str, Any], changes: list[dict[str, Any]]) -> list[str]:
    explicit = spec.get("tests_to_run") or spec.get("suggested_tests") or spec.get("test_commands")
    if isinstance(explicit, list):
        tests = [str(item) for item in explicit if str(item).strip() and "Define focused tests" not in str(item)]
        if tests:
            return tests
    paths = [str(change.get("target") or "") for change in changes]
    if paths and all(path.startswith("docs/") for path in paths):
        return []
    if any(path.startswith("tests/") for path in paths):
        return ["python -B -m pytest tests -q -p no:cacheprovider"]
    if any(path.startswith("wabi_sabi/") for path in paths):
        return ["python -B -m pytest -q -p no:cacheprovider"]
    return ["python -B -m pytest -q -p no:cacheprovider"] if paths else []


def _candidate_from_plan(
    *,
    plan: PatchPlan,
    task_id: str,
    runtime: Path,
    readiness: str,
    blockers: list[str],
    path_scan: dict[str, Any],
    secret_scan: dict[str, Any] | None = None,
    boundary_scan: dict[str, Any] | None = None,
) -> dict[str, Any]:
    plan_path = write_patch_plan(runtime / "outputs" / "local_apply", plan)
    diff_path = write_patch_diff(runtime / "outputs" / "local_apply", plan)
    diff_preview = "\n".join(operation.diff for operation in plan.operations)
    payload = {
        "schema": PATCH_CANDIDATE_SCHEMA,
        "readiness": readiness,
        "task_id": task_id,
        "summary": plan.summary,
        "apply_mode": "local_allowlisted",
        "affected_paths": [operation.relative_path for operation in plan.operations],
        "diff_preview": diff_preview[:12_000],
        "tests_to_run": list(plan.test_commands),
        "rollback_snapshot_required": True,
        "patch_plan_path": str(plan_path),
        "diff_path": str(diff_path),
        "path_allowlist": path_scan,
        "secret_scan": secret_scan or {"status": "PASS", "matches": 0},
        "boundary_scan": boundary_scan or {"status": "PASS", "matches": 0},
        "blockers": blockers,
        "proposal_only": readiness != LOCAL_APPLY_READY,
        "cloud_provider_called": False,
        "graphics_live": False,
        "applied_to_sources": False,
    }
    artifact = write_artifact(
        runtime / "outputs" / "local_apply",
        "patch_candidate",
        ".json",
        json.dumps(redact_mapping(payload), indent=2, ensure_ascii=False) + "\n",
    )
    payload["artifact_path"] = str(artifact)
    return redact_mapping(payload)


def _blocked_candidate(
    *,
    status: str,
    task_id: str,
    summary: str,
    blockers: list[str],
    root: Path,
    tests_to_run: list[str],
) -> dict[str, Any]:
    return redact_mapping(
        {
            "schema": PATCH_CANDIDATE_SCHEMA,
            "readiness": status,
            "task_id": task_id,
            "summary": summary,
            "apply_mode": "local_allowlisted",
            "affected_paths": [],
            "diff_preview": "",
            "tests_to_run": tests_to_run,
            "rollback_snapshot_required": True,
            "path_allowlist": {
                "status": "REVIEW",
                "allowed": False,
                "workspace": str(root),
                "blocked": [],
                "blockers": blockers,
            },
            "secret_scan": {"status": "PASS", "matches": 0},
            "boundary_scan": {"status": "PASS", "matches": 0},
            "blockers": blockers,
            "proposal_only": True,
            "cloud_provider_called": False,
            "graphics_live": False,
            "applied_to_sources": False,
        }
    )


def _scan_plan_paths(plan: PatchPlan, workspace: Path) -> dict[str, Any]:
    blocked: list[dict[str, str]] = []
    for operation in plan.operations:
        path = Path(operation.relative_path)
        parts = {part.lower() for part in path.parts}
        suffix = path.suffix.lower()
        if BLOCKED_PATH_PARTS.intersection(parts):
            blocked.append({"path": operation.relative_path, "reason": "blocked_path_part"})
        if suffix and suffix not in TEXT_SUFFIXES:
            blocked.append({"path": operation.relative_path, "reason": "unsupported_text_suffix"})
        if not _is_allowlisted_relative_path(operation.relative_path, workspace):
            blocked.append({"path": operation.relative_path, "reason": "outside_local_apply_allowlist"})
    return {
        "status": "PASS" if not blocked else "BLOCK",
        "allowed": not blocked,
        "workspace": str(workspace),
        "allowed_roots": _allowed_roots_for_workspace(workspace),
        "blocked": blocked,
        "blockers": [f"{item['path']}:{item['reason']}" for item in blocked],
    }


def _is_allowlisted_relative_path(relative_path: str, workspace: Path) -> bool:
    rel = relative_path.replace("\\", "/").lstrip("/")
    root_name = workspace.name.lower()
    if root_name == "wabi-sabi":
        return rel.startswith(("wabi_sabi/", "tests/", "docs/"))
    if root_name == "-= brain_os =-":
        return (
            rel == "02_CLAUDIO/server/wabi_local_server.py"
            or rel.startswith("02_CLAUDIO/tests/")
            or rel.startswith("apps/local/wabi_ui/")
        )
    return rel.startswith(("wabi_sabi/", "tests/", "docs/"))


def _allowed_roots_for_workspace(workspace: Path) -> list[str]:
    if workspace.name.lower() == "-= brain_os =-":
        return ["02_CLAUDIO/server/wabi_local_server.py", "02_CLAUDIO/tests/**", "apps/local/wabi_ui/**"]
    return ["wabi_sabi/**", "tests/**", "docs/**"]


def _scan_plan_secrets(plan: PatchPlan) -> dict[str, Any]:
    matches = 0
    for operation in plan.operations:
        for pattern in SECRET_PATTERNS:
            matches += len(pattern.findall(operation.content))
            matches += len(pattern.findall(operation.diff))
    return {"status": "PASS" if matches == 0 else "REVIEW", "matches": matches, "values_printed": False}


def _scan_plan_boundary(plan: PatchPlan) -> dict[str, Any]:
    matches = 0
    for operation in plan.operations:
        for pattern in PRIVATE_BOUNDARY_PATTERNS:
            matches += len(pattern.findall(operation.content))
            matches += len(pattern.findall(operation.diff))
    return {"status": "PASS" if matches == 0 else "REVIEW", "matches": matches}


def _scan_files_for_secrets(workspace: Path, relative_paths: list[str]) -> dict[str, Any]:
    matches = 0
    for rel in relative_paths:
        path = (workspace / rel).resolve()
        if not path.exists() or path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        for pattern in SECRET_PATTERNS:
            matches += len(pattern.findall(text))
    return {"status": "PASS" if matches == 0 else "REVIEW", "matches": matches, "values_printed": False}


def _scan_files_for_boundary(workspace: Path, relative_paths: list[str]) -> dict[str, Any]:
    matches = 0
    for rel in relative_paths:
        path = (workspace / rel).resolve()
        if not path.exists() or path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        for pattern in PRIVATE_BOUNDARY_PATTERNS:
            matches += len(pattern.findall(text))
    return {"status": "PASS" if matches == 0 else "REVIEW", "matches": matches}


def _load_candidate(candidate: Mapping[str, Any] | str | Path) -> dict[str, Any]:
    if isinstance(candidate, Mapping):
        return dict(candidate)
    path = Path(candidate)
    payload = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(payload.get("patch_candidate"), dict):
        return dict(payload["patch_candidate"])
    return dict(payload)


def _workspace_root(workspace: str | Path | None) -> Path:
    if workspace is not None:
        return Path(workspace).resolve()
    return Path(__file__).resolve().parents[2]


def _runtime_root(runtime_root: str | Path | None) -> Path:
    if runtime_root is not None:
        return Path(runtime_root).resolve()
    return Path.home() / ".medioevo" / "wabi" / "runtime"
