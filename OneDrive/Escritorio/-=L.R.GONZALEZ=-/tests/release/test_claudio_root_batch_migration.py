from __future__ import annotations

import json
from pathlib import Path

from tools.release import claudio_root_batch_migration


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def test_batch_migration_builds_root_document_entries(tmp_path):
    write(tmp_path / "note.md", "# note")
    write(tmp_path / "tool.py", "print('x')")

    entries = claudio_root_batch_migration.build_entries(
        tmp_path,
        "root_document",
        limit=None,
        include_tracked_clean=True,
    )

    assert len(entries) == 1
    assert entries[0].name == "note.md"
    assert "docs" in entries[0].destination
    assert "root_notes_review" in entries[0].destination
    assert entries[0].sha256
    assert entries[0].action == "MOVE"


def test_batch_migration_apply_moves_files_and_writes_manifest(tmp_path):
    target = tmp_path / "claudio"
    output = tmp_path / "out"
    target.mkdir()
    write(target / "note.md", "# note")

    entries = claudio_root_batch_migration.build_entries(
        target,
        "root_document",
        limit=None,
        include_tracked_clean=True,
    )
    claudio_root_batch_migration.apply_entries(entries, "root_document")

    assert not (target / "note.md").exists()
    assert (target / "docs" / "root_notes_review" / "note.md").exists()
    assert (target / "docs" / "root_notes_review" / "00_LEER_PRIMERO.md").exists()
    assert entries[0].applied is True

    payload = {
        "schema": "medioevo.claudio_root_batch_migration.v1",
        "generated_at_utc": "2026-05-06T00:00:00+00:00",
        "target_root": str(target),
        "category": "root_document",
        "destination_hint": "docs/root_notes_review",
        "apply": True,
        "summary": {"entries": 1, "move_count": 1, "applied_count": 1, "skipped_count": 0},
        "entries": [entry.__dict__ for entry in entries],
    }
    paths = claudio_root_batch_migration.write_outputs(payload, output, "batch")

    assert Path(paths["json"]).exists()
    assert Path(paths["markdown"]).exists()
    assert json.loads(Path(paths["json"]).read_text(encoding="utf-8"))["summary"]["applied_count"] == 1


def test_batch_migration_rejects_unsafe_category(tmp_path):
    try:
        claudio_root_batch_migration.build_entries(tmp_path, "secret_or_sensitive", None, False)
    except ValueError as exc:
        assert "unsupported or unsafe category" in str(exc)
    else:
        raise AssertionError("unsafe category should fail")
