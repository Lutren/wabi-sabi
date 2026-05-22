from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from wabi_sabi.core.browser_gate import build_browser_gate_policy
from wabi_sabi.engine import default_engine_manifest


FUNCTIONAL_STATUS_SCHEMA = "wabi.functional_status.v1"


def build_functional_status(workspace: str | Path, runtime_root: str | Path | None = None) -> dict[str, Any]:
    workspace_path = Path(workspace).resolve()
    runtime_path = Path(runtime_root).resolve() if runtime_root else workspace_path / "runtime"
    wabi_root = _resolve_wabi_root(workspace_path)
    portfolio_root = _resolve_portfolio_root(workspace_path, wabi_root)
    claudio_root = portfolio_root / "-=MEDIOEVO=-" / "-=LIBROS" / "claudio"
    cerebro_index = workspace_path / "runtime" / "cerebro_master_index"
    os_status = _duat_geodia_status(claudio_root)
    engine_manifest = default_engine_manifest()
    engine_modules = engine_manifest.get("modules", {})
    engine_ready = bool(engine_modules)
    modules = {
        "safe_executor": wabi_root / "wabi_sabi" / "core" / "safe_executor.py",
        "patch_planner": wabi_root / "wabi_sabi" / "core" / "patch_planner.py",
        "provider_orchestrator": wabi_root / "wabi_sabi" / "core" / "provider_orchestrator.py",
        "tool_registry": wabi_root / "wabi_sabi" / "core" / "tool_registry.py",
        "browser_gate": wabi_root / "wabi_sabi" / "core" / "browser_gate.py",
        "cerebro_line_audit": wabi_root / "wabi_sabi" / "core" / "cerebro_line_audit.py",
        "cerebro_archive_intake": wabi_root / "wabi_sabi" / "core" / "cerebro_archive_intake.py",
        "cerebro_variant_compare": wabi_root / "wabi_sabi" / "core" / "cerebro_variant_compare.py",
        "cerebro_duplicate_migration_plan": wabi_root / "wabi_sabi" / "core" / "cerebro_duplicate_migration_plan.py",
        "cerebro_canon_merge_review": wabi_root / "wabi_sabi" / "core" / "cerebro_canon_merge_review.py",
        "geodia_math_core": wabi_root / "wabi_sabi" / "core" / "geodia_math_core.py",
        "geodia_synthetic_surface": wabi_root / "wabi_sabi" / "core" / "geodia_synthetic_surface.py",
        "geodia_synthetic_falsifier": wabi_root / "wabi_sabi" / "core" / "geodia_synthetic_falsifier.py",
    }
    module_status = {name: path.exists() for name, path in modules.items()}
    agents_can_program = all(
        module_status.get(name)
        for name in ["safe_executor", "patch_planner", "provider_orchestrator", "tool_registry"]
    )
    cerebro_outputs = {
        "line_manifest": cerebro_index / "LINE_AUDIT_MANIFEST.jsonl",
        "line_signal_index": cerebro_index / "LINE_SIGNAL_INDEX.jsonl",
        "technology_atoms": cerebro_index / "TECHNOLOGY_ATOMS.json",
        "project_graph": cerebro_index / "MASTER_PROJECT_GRAPH.json",
        "read_report": cerebro_index / "CEREBRO_READ_COMPLETE_REPORT.md",
        "document_register": cerebro_index / "DOCUMENT_EXTRACTION_REGISTER.md",
        "human_navigation": cerebro_index / "HUMAN_NAVIGATION_INDEX.md",
        "variant_semantic_comparison": cerebro_index / "VARIANT_SEMANTIC_COMPARISON.json",
        "exact_duplicate_migration_plan": cerebro_index / "VARIANT_EXACT_DUPLICATE_MIGRATION_PLAN.json",
        "canon_merge_review_pack": cerebro_index / "VARIANT_CANON_MERGE_REVIEW_PACK.json",
    }
    archive_intake = workspace_path / "runtime" / "cerebro_archive_intake" / "ReplitExport-lutren_tar_ccac616e3076"
    archive_outputs = {
        "archive_manifest": archive_intake / "ARCHIVE_MEMBER_MANIFEST.jsonl",
        "archive_text_index": archive_intake / "ARCHIVE_TEXT_INDEX.jsonl",
        "archive_report": archive_intake / "ARCHIVE_INTAKE_REPORT.md",
    }
    archive_status = {name: path.exists() for name, path in archive_outputs.items()}
    cerebro_status = {name: path.exists() for name, path in cerebro_outputs.items()}
    policy = build_browser_gate_policy(workspace_path)
    blockers = []
    if not all(cerebro_status.values()):
        blockers.append("cerebro_line_audit_outputs_missing_or_stale")
    if not agents_can_program:
        blockers.append("programming_modules_missing")
    if os_status["status"] != "BOOT_VERIFIED_CURRENT_SESSION":
        blockers.append("duat_geodia_boot_not_currently_verified")

    return {
        "schema": FUNCTIONAL_STATUS_SCHEMA,
        "generated_at_utc": _utc_now(),
        "workspace": str(workspace_path),
        "runtime_root": str(runtime_path),
        "wabi_root": str(wabi_root),
        "status": "LOCAL_FUNCTIONAL_PARTIAL" if blockers else "LOCAL_FUNCTIONAL_VERIFIED",
        "decision_context": {
            "no_operational_assumptions": True,
            "required_truth": "claim only what has current evidence",
        },
        "cerebro_line_audit": {
            "status": "READY" if all(cerebro_status.values()) else "REVIEW",
            "outputs": {name: str(path) for name, path in cerebro_outputs.items()},
            "exists": cerebro_status,
        },
        "agents_can_program": {
            "status": "READY_LOCAL_SAFE_EXECUTOR" if agents_can_program else "REVIEW",
            "modules": {name: str(path) for name, path in modules.items()},
            "exists": module_status,
            "gate": "APPROVE_WITH_PATCH_PLAN_ROLLBACK_TESTS_WITNESS" if agents_can_program else "REVIEW_REQUIRED",
        },
        "local_engine": {
            "status": "READY_LOCAL_CLEAN_ROOM" if engine_ready else "REVIEW",
            "engine_manifest_ready": engine_ready,
            "engine_name": engine_manifest.get("engine_name", ""),
            "module_count": len(engine_modules) if isinstance(engine_modules, dict) else 0,
            "modules": sorted(engine_modules) if isinstance(engine_modules, dict) else [],
            "gate": "APPROVE_LOCAL_ONLY_NO_DEPLOY",
        },
        "archive_intake": {
            "status": "READY_REVIEW_QUARANTINE" if all(archive_status.values()) else "REVIEW",
            "outputs": {name: str(path) for name, path in archive_outputs.items()},
            "exists": archive_status,
            "gate": "REVIEW_BEFORE_IMPORT",
        },
        "browser": {
            "status": "COMPLETO_GATEADO",
            "policy": policy,
        },
        "duat_geodia_os": os_status,
        "blockers": blockers,
        "not_claimed": [
            "No deploy, push, public publication, billing action, or account action is claimed.",
            "No full CEREBRO absorption is claimed for binary/DOCX/PDF/archive files without dedicated extraction.",
            "No DUAT/GEODIA boot success is claimed unless a current command report proves it.",
        ],
    }


def _resolve_wabi_root(workspace_path: Path) -> Path:
    candidates = [
        workspace_path,
        workspace_path / "apps" / "local" / "wabi-sabi",
        Path(__file__).resolve().parents[2],
    ]
    for candidate in candidates:
        if (candidate / "wabi_sabi" / "core").exists():
            return candidate.resolve()
    return candidates[1].resolve()


def _resolve_portfolio_root(workspace_path: Path, wabi_root: Path) -> Path:
    if (workspace_path / "-=MEDIOEVO=-" / "-=LIBROS" / "claudio").exists():
        return workspace_path
    if wabi_root.name == "wabi-sabi" and wabi_root.parent.name == "local" and wabi_root.parent.parent.name == "apps":
        return wabi_root.parent.parent.parent.resolve()
    return workspace_path


def write_functional_status(payload: dict[str, Any], output_dir: str | Path) -> Path:
    output_path = Path(output_dir).resolve()
    output_path.mkdir(parents=True, exist_ok=True)
    target = output_path / "WABI_FUNCTIONAL_STATUS.json"
    target.write_text(json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=True), encoding="utf-8")
    return target


def _duat_geodia_status(claudio_root: Path) -> dict[str, Any]:
    kernel_root = claudio_root / "os" / "duat_geodia_kernel"
    tools = [
        claudio_root / "tools" / "brain_os_cli.py",
        claudio_root / "tools" / "duat_geodia_os_orchestrator.py",
        claudio_root / "tools" / "duat_geodia_iso_builder.py",
        claudio_root / "tools" / "duat_geodia_multistage_benchmark.py",
    ]
    tests = [
        claudio_root / "tests" / "test_brain_os_kernel.py",
        claudio_root / "tests" / "test_duat_geodia_os_orchestrator.py",
        claudio_root / "tests" / "test_duat_geodia_iso_builder.py",
        claudio_root / "tests" / "test_duat_geodia_multistage_benchmark.py",
    ]
    qa_dir = claudio_root / "qa_artifacts" / "os"
    qa_reports = sorted(qa_dir.glob("duat_geodia_os_*.json"), key=lambda path: path.stat().st_mtime if path.exists() else 0, reverse=True)[:8] if qa_dir.exists() else []
    runtime_reports = sorted(
        claudio_root.glob("runtime/**/*duat*geodia*.json"),
        key=lambda path: path.stat().st_mtime if path.exists() else 0,
        reverse=True,
    )[:8]
    latest_payloads = [_safe_json(path) for path in [*qa_reports[:3], *runtime_reports[:3]]]
    previous_verified = any(_looks_like_boot_pass(payload) for payload in latest_payloads)
    current_verification = _safe_json(claudio_root / "runtime" / "wabi_sabi" / "DUAT_GEODIA_CURRENT_VERIFICATION.json")
    current_verified = bool(current_verification.get("ok") is True and current_verification.get("session_verified") is True)
    evidence_present = bool(qa_reports or runtime_reports)
    if current_verified:
        status = "BOOT_VERIFIED_CURRENT_SESSION"
    elif previous_verified:
        status = "BOOT_EVIDENCE_PRESENT_REVERIFY_REQUIRED"
    elif evidence_present:
        status = "EVIDENCE_PRESENT_REVERIFY_REQUIRED"
    else:
        status = "REVIEW_NO_BOOT_EVIDENCE"

    return {
        "status": status,
        "claudio_root": str(claudio_root),
        "kernel_root": str(kernel_root),
        "kernel_exists": kernel_root.exists(),
        "tools": {path.name: str(path) for path in tools},
        "tool_exists": {path.name: path.exists() for path in tools},
        "tests": {path.name: str(path) for path in tests},
        "test_exists": {path.name: path.exists() for path in tests},
        "qa_reports": [str(path) for path in qa_reports],
        "runtime_reports": [str(path) for path in runtime_reports],
        "current_verification": str(claudio_root / "runtime" / "wabi_sabi" / "DUAT_GEODIA_CURRENT_VERIFICATION.json"),
        "current_verification_exists": bool(current_verification),
        "gate": "REVERIFY_WITH_LOCAL_COMMANDS",
    }


def _safe_json(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}
    return data if isinstance(data, dict) else {"payload": data}


def _looks_like_boot_pass(payload: dict[str, Any]) -> bool:
    text = json.dumps(payload, ensure_ascii=False).lower()
    if not text:
        return False
    required = ["duat", "geodia"]
    pass_words = ["pass", "passed", "ok", "bootable", "boot_verified", "success"]
    return all(word in text for word in required) and any(word in text for word in pass_words)


def _utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()
