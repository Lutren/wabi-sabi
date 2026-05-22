from __future__ import annotations

import datetime as dt
import hashlib
import json
from pathlib import Path
from typing import Any

from wabi_sabi.core.bridge import WitnessLog
from wabi_sabi.core.curator_assistant import run_curator_assistant
from wabi_sabi.core.observation import ObservationEnvelope
from wabi_sabi.core.tools import stamp


CURATOR_FICHAS_SCHEMA = "wabi.curator_fichas.v1"
MAX_HASH_BYTES = 5_000_000
CURATOR_AGENT_NAME = "curador_orden_assistant"
CURATION_STATUS_AGENT_PROCESSED = "AGENT_PROCESSED"
CURATION_STATUS_NEEDS_AGENT_PROCESSING = "NEEDS_AGENT_PROCESSING"
OWNER_ASSIGNMENT_STATUS_AGENT_ASSIGNED = "AGENT_ASSIGNED"


def run_curator_fichas(
    *,
    workspace: str | Path,
    runtime_root: str | Path,
    report_path: str | Path | None = None,
    max_fichas: int = 12,
) -> dict[str, Any]:
    workspace_path = Path(workspace).resolve()
    runtime_path = Path(runtime_root).resolve()
    report = _load_or_create_report(workspace_path, runtime_path, report_path)
    fichas = build_fichas_from_report(report, max_fichas=max_fichas, workspace=workspace_path)
    payload: dict[str, Any] = {
        "schema": CURATOR_FICHAS_SCHEMA,
        "ok": True,
        "action": "curator_fichas",
        "gate": "APPROVE",
        "generated_at_utc": _utc_now(),
        "workspace": str(workspace_path),
        "source_report": report.get("artifact") or str(report_path or ""),
        "source_report_schema": report.get("schema"),
        "mode": "ficha_generation_only",
        "policy": {
            "source_writes": False,
            "delete_files": False,
            "move_files": False,
            "git_stage": False,
            "git_commit": False,
            "read_file_contents": False,
            "print_file_contents": False,
            "hash_existing_files": True,
            "max_hash_bytes": MAX_HASH_BYTES,
            "metadata_only": True,
            "candidate_limit": max_fichas,
        },
        "summary": {
            "ficha_count": len(fichas),
            "source_candidate_count": report.get("summary", {}).get("candidate_count", 0),
            "delete_approved_count": 0,
            "cleanup_performed": False,
            "review_required_count": sum(1 for item in fichas if item["action_gate"] == "REVIEW"),
            "blocked_count": sum(1 for item in fichas if item["action_gate"] == "BLOCK"),
            "agent_processed_count": sum(
                1 for item in fichas if item.get("curation", {}).get("status") == CURATION_STATUS_AGENT_PROCESSED
            ),
            "needs_agent_processing_count": sum(
                1 for item in fichas if item.get("curation", {}).get("status") == CURATION_STATUS_NEEDS_AGENT_PROCESSING
            ),
            "owner_assigned_count": sum(
                1
                for item in fichas
                if item.get("owner_assignment", {}).get("status") == OWNER_ASSIGNMENT_STATUS_AGENT_ASSIGNED
            ),
            "unassigned_count": sum(
                1 for item in fichas if not item.get("owner") or item.get("owner") == "UNASSIGNED_CONCURRENT_SAFE"
            ),
        },
        "fichas": fichas,
        "next_safe_actions": [
            "Route each ficha through its assigned agent owner before touching the path.",
            "If a human edits or reassigns a ficha, run an agent pass afterwards so owner assignment and curation last record are agent-owned.",
            "Add hash/provenance evidence for any path that may become archive or delete candidate.",
            "Keep physical cleanup blocked until the owning agent handoff and ActionGate evidence exist.",
        ],
        "artifact": "",
        "markdown_artifact": "",
        "workspace_doc": "",
        "witness_event_id": 0,
        "witness_verified": False,
        "witness_verify_reason": "not_recorded",
        "witness_db": "",
        "observation": {},
    }
    output_dir = runtime_path / "outputs"
    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / f"curator_fichas_{stamp()}.json"
    markdown_path = output_dir / f"curator_fichas_{stamp()}.md"
    payload["artifact"] = str(json_path)
    payload["markdown_artifact"] = str(markdown_path)
    workspace_doc = _write_workspace_doc(workspace_path, payload)
    payload["workspace_doc"] = str(workspace_doc) if workspace_doc else ""

    observation = ObservationEnvelope(
        prompt="curator-fichas",
        intent="workspace_order_fichas",
        agent="curador_orden_assistant",
        action_gate=payload["gate"],
        certainty=[
            "Generated fichas from the latest curator assistant metadata report.",
            "Assigned an agent owner to each ficha without touching source paths.",
            "No files were deleted, moved, staged, committed or reverted.",
        ],
        inference=[
            "Fichas prioritize REVIEW/UNKNOWN items so later cleanup has an owner and evidence path.",
        ],
        unknown=[
            "Fichas do not prove duplicate status or safe deletion; they only route review work.",
        ],
        artifacts=[str(json_path), str(markdown_path), payload["workspace_doc"]],
        evidence=[
            f"ficha_count={payload['summary']['ficha_count']}",
            f"owner_assigned_count={payload['summary']['owner_assigned_count']}",
            "delete_approved_count=0",
            "mode=ficha_generation_only",
        ],
    ).finalize()
    witness = WitnessLog(runtime_path / "witness" / "wabi_patch_witness.sqlite")
    event_id = witness.append(
        "wabi_curator_fichas",
        {
            "workspace": str(workspace_path),
            "json_artifact": str(json_path),
            "markdown_artifact": str(markdown_path),
            "workspace_doc": payload["workspace_doc"],
            "ficha_count": payload["summary"]["ficha_count"],
            "observation_fingerprint": observation.fingerprint,
            "action_gate": payload["gate"],
        },
    )
    witness_ok, witness_reason = witness.verify_chain()
    payload.update(
        {
            "witness_event_id": event_id,
            "witness_verified": witness_ok,
            "witness_verify_reason": witness_reason,
            "witness_db": str(witness.db_path),
            "observation": observation.to_dict(),
        }
    )
    json_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    markdown_path.write_text(format_curator_fichas_markdown(payload), encoding="utf-8")
    if workspace_doc:
        workspace_doc.write_text(format_curator_fichas_markdown(payload), encoding="utf-8")
    return payload


def build_fichas_from_report(
    report: dict[str, Any],
    *,
    max_fichas: int = 12,
    workspace: str | Path | None = None,
) -> list[dict[str, Any]]:
    candidates = list(report.get("candidates", []))
    selected = sorted(candidates, key=_candidate_rank)
    workspace_path = Path(workspace).resolve() if workspace else None
    fichas: list[dict[str, Any]] = []
    for item in selected:
        if len(fichas) >= max_fichas:
            break
        if item.get("action_gate") == "APPROVE" and item.get("decision") == "KEEP":
            continue
        if item.get("action_gate") == "BLOCK":
            continue
        fichas.append(_build_ficha(item, len(fichas) + 1, report, workspace_path))
    return fichas


def format_curator_fichas_markdown(payload: dict[str, Any]) -> str:
    lines = [
        "# Curador Orden Fichas",
        "",
        f"Schema: `{payload['schema']}`",
        f"Workspace: `{payload['workspace']}`",
        f"Source report: `{payload.get('source_report') or 'unknown'}`",
        f"Mode: `{payload['mode']}`",
        "",
        "## Summary",
        "",
        f"- Fichas: `{payload['summary']['ficha_count']}`",
        f"- Cleanup performed: `{payload['summary']['cleanup_performed']}`",
        f"- Delete approved: `{payload['summary']['delete_approved_count']}`",
        f"- Agent processed: `{payload['summary'].get('agent_processed_count', 0)}`",
        f"- Needs agent processing: `{payload['summary'].get('needs_agent_processing_count', 0)}`",
        f"- Owner assigned: `{payload['summary'].get('owner_assigned_count', 0)}`",
        f"- Unassigned: `{payload['summary'].get('unassigned_count', 0)}`",
        "",
        "## Fichas",
        "",
    ]
    if not payload.get("fichas"):
        lines.append("- Sin fichas nuevas desde el reporte fuente.")
    for ficha in payload.get("fichas", []):
        curation = ficha.get("curation", {})
        last_record = curation.get("last_record", {}) if isinstance(curation.get("last_record"), dict) else {}
        owner_assignment = ficha.get("owner_assignment", {})
        lines.extend(
            [
                f"### {ficha['ficha_id']}",
                "",
                f"- Path: `{ficha['source_path']}`",
                f"- Estado: `{ficha['psi_state']}`",
                f"- Decision: `{ficha['decision']}`",
                f"- Gate: `{ficha['action_gate']}`",
                f"- Riesgos: `{', '.join(ficha['risk_flags']) or 'none'}`",
                f"- Owner: `{ficha['owner']}`",
                f"- Owner asignado por: `{owner_assignment.get('assigned_by_actor_type', 'unknown')}:{owner_assignment.get('assigned_by', 'unknown')}`",
                f"- Owner reason: `{owner_assignment.get('reason', 'unknown')}`",
                f"- Curacion: `{curation.get('status', CURATION_STATUS_NEEDS_AGENT_PROCESSING)}`",
                f"- Ultimo registro: `{last_record.get('actor_type', 'unknown')}:{last_record.get('actor', 'unknown')}`",
                f"- Evidencia: `{'; '.join(ficha['evidence'])}`",
                f"- Archivo: `{_file_evidence_summary(ficha.get('file_evidence', {}))}`",
                f"- Siguiente accion: {ficha['next_action']}",
                f"- Bloqueado ahora: `{', '.join(ficha['blocked_actions'])}`",
                "",
            ]
        )
    lines.extend(["## Next Safe Actions", ""])
    for action in payload.get("next_safe_actions", []):
        lines.append(f"- {action}")
    return "\n".join(lines) + "\n"


def _load_or_create_report(workspace: Path, runtime_root: Path, report_path: str | Path | None) -> dict[str, Any]:
    if report_path:
        path = _resolve_report_path(workspace, runtime_root, report_path)
        return json.loads(path.read_text(encoding="utf-8"))
    latest = _latest_report(runtime_root)
    if latest:
        return json.loads(latest.read_text(encoding="utf-8"))
    return run_curator_assistant(workspace=workspace, runtime_root=runtime_root)


def _resolve_report_path(workspace: Path, runtime_root: Path, report_path: str | Path) -> Path:
    raw = Path(report_path)
    candidates = [raw]
    if not raw.is_absolute():
        candidates.append(workspace / raw)
        candidates.append(runtime_root / raw)
        candidates.append(runtime_root / "outputs" / raw)
    for candidate in candidates:
        path = candidate.resolve()
        if path.exists() and path.is_file():
            return path
    raise FileNotFoundError(f"curator report not found: {report_path}")


def _latest_report(runtime_root: Path) -> Path | None:
    output_dir = runtime_root / "outputs"
    if not output_dir.exists():
        return None
    reports = sorted(output_dir.glob("curator_assistant_report_*.json"), key=lambda path: path.stat().st_mtime, reverse=True)
    return reports[0] if reports else None


def _candidate_rank(item: dict[str, Any]) -> tuple[int, str]:
    gate = item.get("action_gate", "")
    decision = item.get("decision", "")
    category = item.get("category", "")
    path = item.get("path", "")
    if gate == "BLOCK":
        return (90, path)
    if decision == "UNKNOWN_REVIEW_REQUIRED":
        base = 0
    elif decision == "CANDIDATE_DELETE":
        base = 20
    else:
        base = 40
    if category == "ROOT_LOOSE_REVIEW":
        base -= 5
    if "docs/" in path.replace("\\", "/").lower():
        base -= 2
    return (base, path)


def _build_ficha(item: dict[str, Any], index: int, report: dict[str, Any], workspace: Path | None) -> dict[str, Any]:
    source_path = str(item.get("path", ""))
    file_evidence = _file_evidence(workspace, source_path)
    owner_assignment = build_owner_assignment(source_path, item)
    curation = build_curation_record(
        actor_type="agent",
        actor=CURATOR_AGENT_NAME,
        event="curator_fichas_generated",
    )
    fingerprint = hashlib.sha256(
        json.dumps(
            {
                "source_path": source_path,
                "decision": item.get("decision"),
                "gate": item.get("action_gate"),
                "source_report": report.get("artifact"),
                "file_evidence": file_evidence,
                "owner_assignment": owner_assignment,
                "curation": curation,
            },
            sort_keys=True,
            ensure_ascii=True,
        ).encode("utf-8")
    ).hexdigest()
    return {
        "ficha_id": f"CURADOR-ORDEN-{index:03d}",
        "fingerprint": fingerprint,
        "source_path": source_path,
        "source_status": item.get("source_status", ""),
        "category": item.get("category", "UNKNOWN_REVIEW_REQUIRED"),
        "psi_state": item.get("psi_state", "INCOGNITA"),
        "claim_level": item.get("claim_level", "operational"),
        "decision": item.get("decision", "UNKNOWN_REVIEW_REQUIRED"),
        "action_gate": item.get("action_gate", "REVIEW"),
        "risk_flags": list(item.get("risk_flags", [])),
        "owner": owner_assignment["owner"],
        "owner_assignment": owner_assignment,
        "curation": curation,
        "evidence": [
            "source=curator_assistant_report",
            "content_read=false",
            "content_printed=false",
            f"source_status={item.get('source_status', '')}",
            f"category={item.get('category', '')}",
            f"file_exists={file_evidence.get('exists')}",
            f"owner_assignment_status={owner_assignment['status']}",
            f"owner_assigned_by_actor_type={owner_assignment['assigned_by_actor_type']}",
            f"curation_status={curation['status']}",
            f"last_record_actor_type={curation['last_record']['actor_type']}",
        ],
        "file_evidence": file_evidence,
        "next_action": _next_action_for_item(item),
        "blocked_actions": [
            "delete",
            "move",
            "git_add_dot",
            "commit",
            "publish",
            "overwrite_without_owner",
        ],
        "teaching_hint": item.get("teaching_hint", ""),
    }


def build_owner_assignment(source_path: str, item: dict[str, Any] | None = None) -> dict[str, Any]:
    item = item or {}
    normalized = source_path.replace("\\", "/").lower()
    category = str(item.get("category", "")).upper()
    base_name = normalized.rsplit("/", 1)[-1]
    root_governance_names = {
        "agents.md",
        "assumptions.md",
        "audit_claudio.md",
        "blocked_actions.md",
        "decisions.md",
        "duplicates_and_dead_code.md",
        "implementation_plan.md",
        "migration_log.md",
        "next_session_brief.md",
        "product_map.md",
        "review_required.md",
        "risk_register.md",
        "secret_scan_report.md",
        "session_fingerprint.json",
        "tasks.md",
        "test_report.md",
        "visibility_matrix.md",
    }

    owner = "agent:curador_orden_assistant"
    reason = "default_curador_lane"
    if "apps/local/wabi-sabi/" in normalized:
        owner = "agent:wabi_sabi_maintenance_curator"
        reason = "wabi_sabi_local_lane"
    elif "docs/developer/" in normalized:
        owner = "agent:developer_docs_curator"
        reason = "developer_docs_lane"
    elif "docs/intake/" in normalized:
        owner = "agent:intake_curator"
        reason = "intake_lane"
    elif category == "HANDOFF_EVIDENCE":
        owner = "agent:handoff_curator"
        reason = "handoff_evidence_lane"
    elif category == "RUNTIME_EVIDENCE":
        owner = "agent:runtime_evidence_curator"
        reason = "runtime_evidence_lane"
    elif category == "CACHE_OR_BUILD_REVIEW":
        owner = "agent:cache_retention_curator"
        reason = "cache_or_build_review_lane"
    elif category == "ROOT_LOOSE_REVIEW" or base_name in root_governance_names:
        owner = "agent:workspace_governance_curator"
        reason = "workspace_governance_lane"

    return {
        "owner": owner,
        "assigned_by_actor_type": "agent",
        "assigned_by": CURATOR_AGENT_NAME,
        "assignment_event": "curator_owner_assignment",
        "status": OWNER_ASSIGNMENT_STATUS_AGENT_ASSIGNED,
        "reason": reason,
        "rule": "owner_assignment_must_be_agent_recorded_before_cleanup",
    }


def build_curation_record(*, actor_type: str, actor: str, event: str) -> dict[str, Any]:
    normalized_actor_type = (actor_type or "").strip().lower()
    last_record = {
        "actor_type": normalized_actor_type or "unknown",
        "actor": actor or "unknown",
        "event": event or "unknown",
        "source": "wabi_sabi.core.curator_fichas",
    }
    return {
        "required_last_actor_type": "agent",
        "status": curation_processing_status(last_record),
        "last_record": last_record,
        "rule": "data_curation_is_processed_only_when_the_last_record_actor_type_is_agent",
        "human_last_record_means": CURATION_STATUS_NEEDS_AGENT_PROCESSING,
    }


def curation_processing_status(last_record: dict[str, Any]) -> str:
    actor_type = str(last_record.get("actor_type", "")).strip().lower()
    if actor_type == "agent":
        return CURATION_STATUS_AGENT_PROCESSED
    return CURATION_STATUS_NEEDS_AGENT_PROCESSING


def _next_action_for_item(item: dict[str, Any]) -> str:
    category = item.get("category", "")
    if category == "CACHE_OR_BUILD_REVIEW":
        return "Document regenerability and canonical source before marking as delete candidate."
    if category == "CONCURRENT_TRACKED_CHANGE":
        return "Use the assigned owner handoff before editing."
    if category in {"UNTRACKED_REVIEW", "ROOT_LOOSE_REVIEW"}:
        return "Owner is assigned; add provenance/hash before moving, staging or archiving."
    return "Keep as REVIEW until the owning agent supplies evidence."


def _file_evidence(workspace: Path | None, source_path: str) -> dict[str, Any]:
    if workspace is None:
        return {"exists": None, "sha256": "", "size_bytes": None, "reason": "workspace_not_provided"}
    path = _resolve_source_path(workspace, source_path)
    if path is None or not path.exists() or not path.is_file():
        return {"exists": False, "sha256": "", "size_bytes": None, "reason": "file_not_found"}
    try:
        size = path.stat().st_size
    except OSError as exc:
        return {"exists": True, "sha256": "", "size_bytes": None, "reason": f"stat_error:{exc}"}
    if size > MAX_HASH_BYTES:
        return {"exists": True, "sha256": "", "size_bytes": size, "reason": "too_large_for_lightweight_hash"}
    try:
        sha256 = hashlib.sha256(path.read_bytes()).hexdigest()
    except OSError as exc:
        return {"exists": True, "sha256": "", "size_bytes": size, "reason": f"hash_error:{exc}"}
    return {"exists": True, "sha256": sha256, "size_bytes": size, "reason": "hash_recorded_content_not_printed"}


def _resolve_source_path(workspace: Path, source_path: str) -> Path | None:
    raw = Path(source_path)
    candidates: list[Path] = []
    if raw.is_absolute():
        candidates.append(raw)
    else:
        candidates.append(workspace / raw)
        normalized = source_path.replace("\\", "/")
        marker = workspace.name + "/"
        if marker in normalized:
            suffix = normalized.split(marker, 1)[1]
            candidates.append(workspace / suffix)
        parent_marker = "OneDrive/Escritorio/" + workspace.name + "/"
        if parent_marker in normalized:
            suffix = normalized.split(parent_marker, 1)[1]
            candidates.append(workspace / suffix)
    for candidate in candidates:
        try:
            resolved = candidate.resolve()
        except OSError:
            continue
        try:
            resolved.relative_to(workspace)
        except ValueError:
            continue
        if resolved.exists():
            return resolved
    for candidate in candidates:
        try:
            resolved = candidate.resolve()
        except OSError:
            continue
        try:
            resolved.relative_to(workspace)
        except ValueError:
            continue
        return resolved
    return None


def _file_evidence_summary(file_evidence: dict[str, Any]) -> str:
    if file_evidence.get("exists") is True and file_evidence.get("sha256"):
        return f"exists=true size={file_evidence.get('size_bytes')} sha256={file_evidence.get('sha256')}"
    return f"exists={file_evidence.get('exists')} reason={file_evidence.get('reason')}"


def _write_workspace_doc(workspace: Path, payload: dict[str, Any]) -> Path | None:
    intake_dir = workspace / "docs" / "intake"
    if not intake_dir.exists() or not intake_dir.is_dir():
        return None
    date = dt.datetime.now(dt.UTC).strftime("%Y-%m-%d")
    base = intake_dir / f"CURADOR_ORDEN_FICHAS_{date}.md"
    if not base.exists():
        return base
    try:
        first_line = base.read_text(encoding="utf-8", errors="replace").splitlines()[0]
    except (OSError, IndexError):
        first_line = ""
    if first_line.strip() == "# Curador Orden Fichas":
        return base
    suffix = stamp()
    return intake_dir / f"CURADOR_ORDEN_FICHAS_{date}_{suffix}.md"


def _utc_now() -> str:
    return dt.datetime.now(dt.UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")
