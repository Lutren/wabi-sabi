from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools" / "release"))

import global_curador_audit as audit  # noqa: E402


def test_incremental_scan_limits_and_resumes_from_marker(tmp_path: Path) -> None:
    root = tmp_path / "root"
    root.mkdir()
    for name in ["a.txt", "b.txt", "c.txt"]:
        (root / name).write_text(name, encoding="utf-8")

    root_defs = [{"label": "fixture", "path": root, "exclude": []}]
    first = audit.scan_roots(
        hash_max_bytes=1024 * 1024,
        registry_blob="",
        root_labels={"fixture"},
        max_files=2,
        root_defs=root_defs,
    )

    assert [Path(str(row["path"])).name for row in first["rows"]] == ["a.txt", "b.txt"]
    assert first["resume"]["truncated"] is True
    assert first["resume"]["processed_files"] == 2
    marker = str(first["resume"]["next_start_after"])

    second = audit.scan_roots(
        hash_max_bytes=1024 * 1024,
        registry_blob="",
        root_labels={"fixture"},
        max_files=2,
        start_after=marker,
        root_defs=root_defs,
    )

    assert [Path(str(row["path"])).name for row in second["rows"]] == ["c.txt"]
    assert second["resume"]["truncated"] is False
    assert second["resume"]["processed_files"] == 1


def test_unknown_root_label_fails_closed(tmp_path: Path) -> None:
    root_defs = [{"label": "fixture", "path": tmp_path, "exclude": []}]

    try:
        audit.selected_root_defs({"missing"}, root_defs)
    except ValueError as exc:
        assert "unknown root label" in str(exc)
        assert "fixture" in str(exc)
    else:
        raise AssertionError("unknown root label should fail closed")
