import json
import os
import subprocess
import sys
import zipfile
from pathlib import Path

from wabi_sabi.core.cerebro_line_audit import (
    build_cerebro_line_audit,
    compact_cerebro_audit_payload,
    write_cerebro_audit_outputs,
)


APP_ROOT = Path(__file__).resolve().parents[1]


def make_workspace(root: Path) -> Path:
    cerebro = root / "-=MEDIOEVO=-" / "-=LIBROS" / "-=CEREBRO=-"
    (cerebro / "a").mkdir(parents=True)
    (cerebro / "b").mkdir(parents=True)
    (cerebro / "00_LEER.txt").write_text(
        "R < 0.30 and Phi_eff > 0.60\nActionGate controls browser and agent programming\n```python\ndef gate():\n    return 'APPROVE'\n```\n",
        encoding="utf-8",
    )
    (cerebro / "a" / "foo.txt").write_text("DUAT GEODIA boot evidence\n", encoding="utf-8")
    (cerebro / "b" / "foo.txt").write_text("DUAT GEODIA boot evidence changed\n", encoding="utf-8")
    _write_minimal_docx(cerebro / "osit.docx", "OSIT TUIP Sigma ActionGate from DOCX")
    (cerebro / "bundle.docx").write_bytes(b"not-a-real-docx")
    return cerebro


def _write_minimal_docx(path: Path, text: str) -> None:
    xml = f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:body>
    <w:p><w:r><w:t>{text}</w:t></w:r></w:p>
  </w:body>
</w:document>
"""
    with zipfile.ZipFile(path, "w") as archive:
        archive.writestr("word/document.xml", xml)


def run_cli(*args, workspace: Path, runtime: Path):
    env = os.environ.copy()
    env["PYTHONPATH"] = str(APP_ROOT)
    return subprocess.run(
        [
            sys.executable,
            "-m",
            "wabi_sabi.cli.main",
            *args,
            "--workspace",
            str(workspace),
            "--runtime",
            str(runtime),
        ],
        cwd=str(APP_ROOT),
        env=env,
        text=True,
        capture_output=True,
        timeout=45,
    )


def test_cerebro_line_audit_scans_text_lines_and_registers_variants(tmp_path):
    make_workspace(tmp_path)

    payload = build_cerebro_line_audit(tmp_path)

    assert payload["schema"] == "wabi.cerebro_line_audit.v2"
    assert payload["ok"] is True
    assert payload["summary"]["text_file_count"] == 3
    assert payload["summary"]["document_text_file_count"] == 1
    assert payload["summary"]["document_review_file_count"] == 1
    assert payload["summary"]["signal_line_count"] >= 2
    assert payload["summary"]["code_candidate_count"] >= 1
    assert any(atom["source_signal"] == "ActionGate" for atom in payload["technology_atoms"])
    assert any(variant["kind"] == "SAME_NAME_DIFFERENT_HASH" for variant in payload["variant_records"])

    compact = compact_cerebro_audit_payload(payload)
    assert "manifest_records" not in compact
    assert compact["manifest_sample"]


def test_write_cerebro_line_audit_outputs(tmp_path):
    make_workspace(tmp_path)
    payload = build_cerebro_line_audit(tmp_path)

    artifacts = write_cerebro_audit_outputs(payload, tmp_path / "runtime" / "cerebro_master_index")

    assert artifacts
    output = tmp_path / "runtime" / "cerebro_master_index"
    assert (output / "LINE_AUDIT_MANIFEST.jsonl").exists()
    assert (output / "LINE_SIGNAL_INDEX.jsonl").exists()
    assert (output / "TECHNOLOGY_ATOMS.json").exists()
    assert (output / "MASTER_PROJECT_GRAPH.json").exists()
    report = (output / "CEREBRO_READ_COMPLETE_REPORT.md").read_text(encoding="utf-8")
    assert "Text files read line by line" in report
    assert "DUAT/GEODIA boot completeness needs separate command evidence" in report


def test_cerebro_line_audit_cli_json_and_write_docs(tmp_path):
    make_workspace(tmp_path)

    dry = run_cli("cerebro-audit", "--json", workspace=tmp_path, runtime=tmp_path / "runtime")
    assert dry.returncode == 0, dry.stderr
    dry_payload = json.loads(dry.stdout)
    assert dry_payload["action"] == "cerebro_line_audit_dry_run"
    assert "manifest_records" not in dry_payload

    write = run_cli("cerebro-audit", "--write-docs", "--json", workspace=tmp_path, runtime=tmp_path / "runtime")
    assert write.returncode == 0, write.stderr
    write_payload = json.loads(write.stdout)
    assert write_payload["action"] == "cerebro_line_audit_docs_written"
    assert write_payload["artifacts"]
    assert (tmp_path / "runtime" / "cerebro_master_index" / "ACTION_GATE_REGISTER.md").exists()
