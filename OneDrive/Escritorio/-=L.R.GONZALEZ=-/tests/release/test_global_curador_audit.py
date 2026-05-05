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


def test_resume_uses_traversal_marker_not_lexicographic_path(tmp_path: Path) -> None:
    root = tmp_path / "root"
    nested = root / "a_dir"
    nested.mkdir(parents=True)
    (root / "z_root.txt").write_text("already seen before nested marker", encoding="utf-8")
    marker = nested / "m_marker.txt"
    marker.write_text("marker", encoding="utf-8")
    (nested / "n_after.txt").write_text("after marker", encoding="utf-8")

    result = audit.scan_roots(
        hash_max_bytes=1024 * 1024,
        registry_blob="",
        root_labels={"fixture"},
        max_files=10,
        start_after=str(marker),
        root_defs=[{"label": "fixture", "path": root, "exclude": []}],
    )

    assert result["resume"]["start_after_found"] is True
    assert [Path(str(row["path"])).name for row in result["rows"]] == ["n_after.txt"]


def test_unknown_root_label_fails_closed(tmp_path: Path) -> None:
    root_defs = [{"label": "fixture", "path": tmp_path, "exclude": []}]

    try:
        audit.selected_root_defs({"missing"}, root_defs)
    except ValueError as exc:
        assert "unknown root label" in str(exc)
        assert "fixture" in str(exc)
    else:
        raise AssertionError("unknown root label should fail closed")


def test_resume_output_paths_include_marker_fingerprint() -> None:
    first = audit.default_output_paths({"workspace_lrgonzalez"}, 500, "C:/first/path.txt")
    second = audit.default_output_paths({"workspace_lrgonzalez"}, 500, "C:/second/path.txt")

    assert first != second
    assert "resume" in first[0].name
    assert "resume" in second[0].name
