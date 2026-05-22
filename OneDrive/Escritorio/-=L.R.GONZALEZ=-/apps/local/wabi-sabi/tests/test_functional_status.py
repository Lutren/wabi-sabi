import json
from pathlib import Path

from wabi_sabi.core.functional_status import build_functional_status, write_functional_status


def test_functional_status_reports_current_evidence_without_claiming_boot(tmp_path):
    wabi_core = tmp_path / "apps" / "local" / "wabi-sabi" / "wabi_sabi" / "core"
    wabi_core.mkdir(parents=True)
    for name in [
        "safe_executor.py",
        "patch_planner.py",
        "provider_orchestrator.py",
        "tool_registry.py",
        "browser_gate.py",
        "cerebro_line_audit.py",
        "cerebro_archive_intake.py",
        "cerebro_variant_compare.py",
        "cerebro_duplicate_migration_plan.py",
        "cerebro_canon_merge_review.py",
        "geodia_math_core.py",
        "geodia_synthetic_surface.py",
        "geodia_synthetic_falsifier.py",
    ]:
        (wabi_core / name).write_text("# module\n", encoding="utf-8")

    audit_dir = tmp_path / "runtime" / "cerebro_master_index"
    audit_dir.mkdir(parents=True)
    for name in [
        "LINE_AUDIT_MANIFEST.jsonl",
        "LINE_SIGNAL_INDEX.jsonl",
        "TECHNOLOGY_ATOMS.json",
        "MASTER_PROJECT_GRAPH.json",
        "CEREBRO_READ_COMPLETE_REPORT.md",
        "DOCUMENT_EXTRACTION_REGISTER.md",
        "HUMAN_NAVIGATION_INDEX.md",
        "VARIANT_SEMANTIC_COMPARISON.json",
        "VARIANT_EXACT_DUPLICATE_MIGRATION_PLAN.json",
        "VARIANT_CANON_MERGE_REVIEW_PACK.json",
    ]:
        (audit_dir / name).write_text("{}\n", encoding="utf-8")

    archive_dir = tmp_path / "runtime" / "cerebro_archive_intake" / "ReplitExport-lutren_tar_ccac616e3076"
    archive_dir.mkdir(parents=True)
    for name in ["ARCHIVE_MEMBER_MANIFEST.jsonl", "ARCHIVE_TEXT_INDEX.jsonl", "ARCHIVE_INTAKE_REPORT.md"]:
        (archive_dir / name).write_text("{}\n", encoding="utf-8")

    claudio = tmp_path / "-=MEDIOEVO=-" / "-=LIBROS" / "claudio"
    (claudio / "os" / "duat_geodia_kernel").mkdir(parents=True)
    (claudio / "tools").mkdir(parents=True)
    (claudio / "tests").mkdir(parents=True)
    for name in [
        "brain_os_cli.py",
        "duat_geodia_os_orchestrator.py",
        "duat_geodia_iso_builder.py",
        "duat_geodia_multistage_benchmark.py",
    ]:
        (claudio / "tools" / name).write_text("# tool\n", encoding="utf-8")

    payload = build_functional_status(tmp_path, tmp_path / "runtime")

    assert payload["schema"] == "wabi.functional_status.v1"
    assert payload["cerebro_line_audit"]["status"] == "READY"
    assert payload["agents_can_program"]["status"] == "READY_LOCAL_SAFE_EXECUTOR"
    assert payload["browser"]["status"] == "COMPLETO_GATEADO"
    assert payload["archive_intake"]["status"] == "READY_REVIEW_QUARANTINE"
    assert payload["duat_geodia_os"]["status"] == "REVIEW_NO_BOOT_EVIDENCE"
    assert "duat_geodia_boot_not_currently_verified" in payload["blockers"]


def test_write_functional_status(tmp_path):
    payload = build_functional_status(tmp_path, tmp_path / "runtime")
    artifact = write_functional_status(payload, tmp_path / "runtime" / "outputs")

    assert artifact.exists()
    parsed = json.loads(artifact.read_text(encoding="utf-8"))
    assert parsed["schema"] == "wabi.functional_status.v1"
