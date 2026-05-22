from __future__ import annotations

import datetime as dt
import json
from collections import Counter
from pathlib import Path
from typing import Any

from wabi_sabi.core.bridge import WitnessLog
from wabi_sabi.core.observation import ObservationEnvelope
from wabi_sabi.core.project_scan import scan_project
from wabi_sabi.core.tools import stamp
from wabi_sabi.core.worktree import git_worktree_summary


CURATOR_ASSISTANT_SCHEMA = "wabi.curator_assistant_report.v1"


def run_curator_assistant(
    *,
    workspace: str | Path,
    runtime_root: str | Path,
    max_items: int = 120,
) -> dict[str, Any]:
    workspace_path = Path(workspace).resolve()
    runtime_path = Path(runtime_root).resolve()
    report = build_curator_assistant_report(workspace=workspace_path, max_items=max_items)

    output_dir = runtime_path / "outputs"
    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / f"curator_assistant_report_{stamp()}.json"
    markdown_path = output_dir / f"curator_assistant_report_{stamp()}.md"

    observation = ObservationEnvelope(
        prompt="curator-assistant",
        intent="workspace_order_dry_run",
        agent="curador_orden_assistant",
        action_gate=report["gate"],
        certainty=[
            "Generated a dry-run order report from git metadata and project scan metadata.",
            "No files were deleted, moved, staged, committed or reverted.",
        ],
        inference=[
            "Unknown or untracked files are treated as active or review-required while other agents are working.",
        ],
        unknown=[
            "File contents, exact duplicate hashes and canonical targets were not inspected in this lightweight pass.",
        ],
        artifacts=[str(json_path), str(markdown_path)],
        evidence=[
            f"status_count={report['workspace_state'].get('status_count', 'unknown')}",
            f"candidate_count={report['summary']['candidate_count']}",
            "mode=dry_run_only",
        ],
    ).finalize()

    witness = WitnessLog(runtime_path / "witness" / "wabi_patch_witness.sqlite")
    event_id = witness.append(
        "wabi_curator_assistant_report",
        {
            "workspace": str(workspace_path),
            "json_artifact": str(json_path),
            "markdown_artifact": str(markdown_path),
            "candidate_count": report["summary"]["candidate_count"],
            "observation_fingerprint": observation.fingerprint,
            "action_gate": report["gate"],
        },
    )
    witness_ok, witness_reason = witness.verify_chain()

    report.update(
        {
            "artifact": str(json_path),
            "markdown_artifact": str(markdown_path),
            "witness_event_id": event_id,
            "witness_verified": witness_ok,
            "witness_verify_reason": witness_reason,
            "witness_db": str(witness.db_path),
            "observation": observation.to_dict(),
        }
    )
    json_path.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    markdown_path.write_text(format_curator_assistant_markdown(report), encoding="utf-8")
    return report


def build_curator_assistant_report(*, workspace: str | Path, max_items: int = 120) -> dict[str, Any]:
    workspace_path = Path(workspace).resolve()
    worktree = git_worktree_summary(workspace_path, max_files=max_items)
    project = scan_project(workspace=workspace_path, max_files=3000)
    candidates = _candidate_items(worktree, max_items=max_items)
    category_counts = Counter(item["category"] for item in candidates)
    decision_counts = Counter(item["decision"] for item in candidates)
    gate_counts = Counter(item["action_gate"] for item in candidates)
    return {
        "schema": CURATOR_ASSISTANT_SCHEMA,
        "ok": True,
        "action": "curator_assistant_report",
        "gate": "APPROVE",
        "generated_at_utc": _utc_now(),
        "workspace": str(workspace_path),
        "mode": "dry_run_only",
        "policy": {
            "source_writes": False,
            "delete_files": False,
            "move_files": False,
            "git_stage": False,
            "git_commit": False,
            "read_file_contents": False,
            "metadata_only": True,
        },
        "assistant_contract": _assistant_contract(),
        "workspace_state": _workspace_state(worktree, project),
        "summary": {
            "candidate_count": len(candidates),
            "category_counts": dict(sorted(category_counts.items())),
            "decision_counts": dict(sorted(decision_counts.items())),
            "gate_counts": dict(sorted(gate_counts.items())),
            "concurrent_worktree": bool(worktree.get("dirty")),
            "safe_cleanup_performed": False,
        },
        "cleanup_plan": _cleanup_plan(candidates),
        "candidates": candidates,
        "teaching": _teaching_contract(),
        "next_safe_actions": [
            "Share this report path with agents before broad cleanup work.",
            "Convert high-value unknown files into fichas before any archive or delete decision.",
            "Run project-scan, claim-contract and run-safe-tests before claiming implementation closure.",
            "Keep concurrent tracked changes untouched until their owning agent writes a handoff.",
        ],
        "artifact": "",
        "markdown_artifact": "",
        "witness_event_id": 0,
        "witness_verified": False,
        "witness_verify_reason": "not_recorded",
        "witness_db": "",
        "observation": {},
    }


def format_curator_assistant_markdown(report: dict[str, Any]) -> str:
    summary = report["summary"]
    state = report["workspace_state"]
    lines = [
        "# Curador Orden Assistant Report",
        "",
        f"Schema: `{report['schema']}`",
        f"Workspace: `{report['workspace']}`",
        f"Mode: `{report['mode']}`",
        f"Gate: `{report['gate']}`",
        "",
        "## Estado seco",
        "",
        f"- Worktree dirty: `{state.get('dirty')}`",
        f"- Status count: `{state.get('status_count')}`",
        f"- Candidate count: `{summary['candidate_count']}`",
        f"- Safe cleanup performed: `{summary['safe_cleanup_performed']}`",
        "",
        "## Categorias",
        "",
    ]
    for category, count in summary["category_counts"].items():
        lines.append(f"- `{category}`: {count}")
    if not summary["category_counts"]:
        lines.append("- Sin candidatos en la muestra.")
    lines.extend(["", "## Reglas para quien trabaje en esta computadora", ""])
    for rule in report["teaching"]["rules"]:
        lines.append(f"- {rule['title']}: {rule['rule']}")
    lines.extend(["", "## Primeros candidatos", ""])
    for item in report["candidates"][:25]:
        lines.append(
            f"- `{item['path']}` -> `{item['category']}` / `{item['decision']}` / `{item['action_gate']}`"
        )
    if not report["candidates"]:
        lines.append("- Sin candidatos en la muestra.")
    lines.extend(["", "## Acciones bloqueadas", ""])
    for item in report["cleanup_plan"]["forbidden_now"]:
        lines.append(f"- {item}")
    lines.extend(["", "## Proxima accion segura", ""])
    lines.append("- Crear fichas para los `UNKNOWN_REVIEW_REQUIRED` de mayor valor antes de archivar o borrar.")
    return "\n".join(lines) + "\n"


def _candidate_items(worktree: dict[str, Any], *, max_items: int) -> list[dict[str, Any]]:
    if not worktree.get("ok"):
        return [
            {
                "path": worktree.get("workspace", ""),
                "source_status": "git_unavailable",
                "category": "WORKTREE_UNKNOWN",
                "psi_state": "INCOGNITA",
                "claim_level": "operational",
                "decision": "UNKNOWN_REVIEW_REQUIRED",
                "action_gate": "REVIEW",
                "risk_flags": ["git_metadata_unavailable"],
                "teaching_hint": "Do not clean or move files until git metadata is available or a manifest exists.",
            }
        ]
    seen: set[str] = set()
    candidates: list[dict[str, Any]] = []
    for raw in worktree.get("status_sample", [])[:max_items]:
        status, path = _parse_status(raw)
        if not path or path in seen:
            continue
        seen.add(path)
        candidates.append(_classify_status_path(status, path))
    return candidates


def _parse_status(raw: str) -> tuple[str, str]:
    if len(raw) >= 4 and raw[2] == " ":
        return raw[:2].strip() or "changed", raw[3:].strip()
    if raw.startswith("??"):
        return "??", raw[2:].strip()
    return "changed", raw.strip()


def _classify_status_path(status: str, path: str) -> dict[str, Any]:
    normalized = path.replace("\\", "/")
    lower = normalized.lower()
    if _is_private_or_secret_like(lower):
        return _item(
            status,
            normalized,
            category="BOUNDARY_BLOCKED",
            psi_state="BLOQUEADO",
            decision="KEEP",
            action_gate="BLOCK",
            risk_flags=["private_or_secret_like_path"],
            hint="Do not copy, publish, move or inspect content without the specific gate for this lane.",
        )
    if _is_cache_or_build(lower):
        return _item(
            status,
            normalized,
            category="CACHE_OR_BUILD_REVIEW",
            psi_state="INFERENCIA",
            decision="CANDIDATE_DELETE",
            action_gate="REVIEW",
            risk_flags=["generated_or_regenerable_inferred"],
            hint="Only delete in a later cleanup pass after regenerability, exact path and rollback evidence are recorded.",
        )
    if lower.startswith("runtime/") or "/runtime/" in lower:
        return _item(
            status,
            normalized,
            category="RUNTIME_EVIDENCE",
            psi_state="CERTEZA",
            decision="KEEP",
            action_gate="APPROVE",
            risk_flags=["generated_evidence"],
            hint="Keep runtime evidence unless a dedicated retention policy marks it as regenerable.",
        )
    if lower.endswith(("session_fingerprint.json", "next_session_brief.md", "test_report.md")):
        return _item(
            status,
            normalized,
            category="HANDOFF_EVIDENCE",
            psi_state="CERTEZA",
            decision="KEEP",
            action_gate="APPROVE",
            risk_flags=["handoff_state"],
            hint="Preserve handoff files; update them only when this task owns the closure.",
        )
    if status == "??":
        category = "ROOT_LOOSE_REVIEW" if "/" not in normalized else "UNTRACKED_REVIEW"
        return _item(
            status,
            normalized,
            category=category,
            psi_state="INCOGNITA",
            decision="UNKNOWN_REVIEW_REQUIRED",
            action_gate="REVIEW",
            risk_flags=["untracked", "concurrent_agent_possible"],
            hint="Create a ficha or assign an owner before moving, staging or deleting.",
        )
    return _item(
        status,
        normalized,
        category="CONCURRENT_TRACKED_CHANGE",
        psi_state="INCOGNITA",
        decision="KEEP",
        action_gate="REVIEW",
        risk_flags=["tracked_change", "concurrent_agent_possible"],
        hint="Do not revert or overwrite; wait for the owning agent handoff or inspect only the files this task owns.",
    )


def _item(
    status: str,
    path: str,
    *,
    category: str,
    psi_state: str,
    decision: str,
    action_gate: str,
    risk_flags: list[str],
    hint: str,
) -> dict[str, Any]:
    return {
        "path": path,
        "source_status": status,
        "category": category,
        "psi_state": psi_state,
        "claim_level": "operational",
        "decision": decision,
        "action_gate": action_gate,
        "risk_flags": risk_flags,
        "teaching_hint": hint,
    }


def _is_cache_or_build(path: str) -> bool:
    parts = set(path.split("/"))
    if parts.intersection(
        {
            "__pycache__",
            ".pytest_cache",
            "node_modules",
            "target",
            "dist",
            "build",
            "coverage",
        }
    ):
        return True
    return path.endswith((".pyc", ".pyo", ".log", ".tmp"))


def _is_private_or_secret_like(path: str) -> bool:
    private_markers = ["metaevo-tcg", "/tcg/", "game_bridge", "game-private"]
    secret_markers = [".env", "secret", "token", "credential", "password", "gumroad", "stripe"]
    return any(marker in path for marker in private_markers + secret_markers)


def _workspace_state(worktree: dict[str, Any], project: dict[str, Any]) -> dict[str, Any]:
    return {
        "workspace": worktree.get("workspace") or project.get("workspace"),
        "repo_root": worktree.get("repo_root", ""),
        "branch": worktree.get("branch", "unknown"),
        "base_commit": worktree.get("base_commit", "unknown"),
        "dirty": worktree.get("dirty"),
        "status_count": worktree.get("status_count"),
        "project_scan_schema": project.get("schema"),
        "files_sampled": project.get("files_sampled"),
        "package_managers": project.get("package_managers", []),
        "languages": project.get("languages", []),
        "test_commands": project.get("test_commands", []),
        "content_included": False,
        "limits": {
            "git_status_sample": worktree.get("limits", {}).get("max_files"),
            "project_scan_max_files": project.get("limits", {}).get("max_files"),
        },
    }


def _cleanup_plan(candidates: list[dict[str, Any]]) -> dict[str, Any]:
    review_count = sum(1 for item in candidates if item["action_gate"] == "REVIEW")
    blocked_count = sum(1 for item in candidates if item["action_gate"] == "BLOCK")
    return {
        "plan_gate": "REVIEW" if review_count or blocked_count else "APPROVE",
        "cleanup_performed": False,
        "allowed_now": [
            "write dry-run reports under runtime/outputs",
            "teach operators and agents the order protocol",
            "create fichas or manifests for owned files",
            "run safe tests through run-safe-tests",
        ],
        "forbidden_now": [
            "delete files",
            "move files",
            "git add .",
            "git reset, checkout or broad revert",
            "publish, push, deploy or upload",
            "inspect or print secret values",
            "touch private game, TCG or game bridge lanes",
        ],
        "review_required_count": review_count,
        "blocked_count": blocked_count,
        "candidate_delete_count": sum(1 for item in candidates if item["decision"] == "CANDIDATE_DELETE"),
        "delete_approved_count": 0,
    }


def _assistant_contract() -> dict[str, Any]:
    return {
        "name": "curador_orden_assistant",
        "display_name": "Curador Orden Assistant",
        "role": "assistant to the curator that keeps order, creates dry-run cleanup evidence and teaches workspace hygiene",
        "operating_mode": "READ_ONLY_PLUS_REPORTS",
        "reads": [
            "git metadata",
            "workspace filenames",
            "project scan metadata",
            "existing reports and handoffs by path reference",
        ],
        "may_write": [
            "runtime/outputs/curator_assistant_report_*.json",
            "runtime/outputs/curator_assistant_report_*.md",
            "runtime/logs/wabi_events.jsonl",
            "runtime/witness/wabi_patch_witness.sqlite",
            "curator assistant docs when explicitly maintaining the contract",
        ],
        "never_does": [
            "delete files",
            "move or rename files",
            "stage or commit git changes",
            "revert another agent's work",
            "publish or upload material",
            "read or print secret values",
            "touch private game or TCG lanes",
        ],
        "handoff_contract": [
            "CERTEZA: metadata observed directly",
            "INFERENCIA: likely category from path/status only",
            "INCOGNITA: untracked or ambiguous material awaiting ficha",
            "BLOQUEADO: secret/private/publication/destructive risk",
        ],
    }


def _teaching_contract() -> dict[str, Any]:
    return {
        "rules": [
            {
                "title": "Start with status",
                "rule": "Run worktree-status or curator-assistant before changing broad folders.",
            },
            {
                "title": "No broad staging",
                "rule": "Never use git add . in this workspace; stage only files owned by the current task.",
            },
            {
                "title": "No physical cleanup during concurrency",
                "rule": "When other agents are active, do not delete, move, revert or rename their files.",
            },
            {
                "title": "Use evidence folders",
                "rule": "Generated outputs go to runtime/outputs, logs to runtime/logs and handoffs to NEXT_SESSION_BRIEF/SESSION_FINGERPRINT.",
            },
            {
                "title": "Ficha before archive",
                "rule": "Unknown material needs a ficha, hash or manifest before archive/delete candidates are trusted.",
            },
            {
                "title": "Keep private lanes blocked",
                "rule": "Game, TCG, secrets, paid content and publication actions stay BLOCK unless a specific gate authorizes them.",
            },
            {
                "title": "Close with verification",
                "rule": "Use claim-contract, project-scan, test-plan and run-safe-tests before claiming a feature is done.",
            },
        ],
        "operator_checklist": [
            "1. Read AGENTS.md and the current handoff.",
            "2. Run curator-assistant --json for a dry report.",
            "3. Work only in owned files.",
            "4. Write artifacts to runtime/outputs.",
            "5. Add evidence before changing task status.",
            "6. Leave a handoff if the work remains open.",
        ],
        "anti_clutter_defaults": [
            "Prefer docs/intake or runtime/outputs over loose root files.",
            "Prefer manifests and fichas over copying raw source trees.",
            "Prefer REVIEW over cleanup when lineage is unclear.",
            "Prefer small reversible patches over broad reorganizations.",
        ],
    }


def _utc_now() -> str:
    return dt.datetime.now(dt.UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")
