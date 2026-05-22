import hashlib
import json
import subprocess
import sys
from pathlib import Path

from wabi_sabi.core.cerebro_canon_merge_review import (
    CEREBRO_CANON_MERGE_REVIEW_SCHEMA,
    build_cerebro_canon_merge_review,
    write_cerebro_canon_merge_review,
)
from wabi_sabi.core.cerebro_variant_compare import (
    build_cerebro_variant_comparison,
    write_cerebro_variant_comparison,
)
from wabi_sabi.core.tool_registry import tool_registry_payload


def _sha(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _record(path: str, text: str) -> dict:
    return {
        "path": path,
        "name": Path(path).name,
        "suffix": Path(path).suffix,
        "sha256": _sha(text),
        "classification": "TEXT",
        "source_kind": "filesystem_text",
        "line_count": len(text.splitlines()),
        "size_bytes": len(text.encode("utf-8")),
        "signal_count": 0,
        "signals": {},
        "code_candidate_count": 0,
        "code_fence_count": 0,
    }


def _fixture_workspace(tmp_path: Path) -> Path:
    workspace = tmp_path
    index = workspace / "runtime" / "cerebro_master_index"
    index.mkdir(parents=True, exist_ok=True)
    license_a = "\n".join(["MIT License", "Copyright Owner A", *["Permission paragraph"] * 19])
    license_b = "\n".join(["MIT License", "Copyright Owner B", *["Permission paragraph"] * 19])
    files = {
        "repo_a/LICENSE": license_a,
        "repo_b/LICENSE": license_b,
    }
    for rel, text in files.items():
        target = workspace / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text, encoding="utf-8")
    with (index / "LINE_AUDIT_MANIFEST.jsonl").open("w", encoding="utf-8") as handle:
        for rel, text in files.items():
            handle.write(json.dumps(_record(rel, text), ensure_ascii=False) + "\n")
    (index / "LINE_SIGNAL_INDEX.jsonl").write_text("", encoding="utf-8")
    comparison = build_cerebro_variant_comparison(workspace)
    write_cerebro_variant_comparison(comparison, index)
    return workspace


def test_canon_merge_review_marks_license_boundary_without_auto_merge(tmp_path):
    workspace = _fixture_workspace(tmp_path)
    payload = build_cerebro_canon_merge_review(workspace)

    assert payload["schema"] == CEREBRO_CANON_MERGE_REVIEW_SCHEMA
    assert payload["summary"]["review_candidate_groups"] >= 1
    assert payload["summary"]["auto_merge_actions"] == 0
    assert payload["summary"]["source_mutations"] == 0
    assert payload["candidates"][0]["boundary_type"] == "LICENSE_BOUNDARY"
    assert payload["candidates"][0]["review_decision"]["execution_allowed_now"] is False


def test_write_canon_merge_review_outputs_json_md_jsonl(tmp_path):
    workspace = _fixture_workspace(tmp_path)
    payload = build_cerebro_canon_merge_review(workspace)
    artifacts = write_cerebro_canon_merge_review(payload, workspace / "runtime" / "cerebro_master_index")

    assert len(artifacts) == 3
    for artifact in artifacts:
        assert Path(artifact).exists()
    parsed = json.loads(Path(artifacts[0]).read_text(encoding="utf-8"))
    assert parsed["schema"] == CEREBRO_CANON_MERGE_REVIEW_SCHEMA


def test_canon_merge_review_cli_json(tmp_path):
    workspace = _fixture_workspace(tmp_path)
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "wabi_sabi.cli.main",
            "merge-review-pack",
            "--workspace",
            str(workspace),
            "--runtime",
            str(workspace / "runtime"),
            "--write-docs",
            "--json",
        ],
        capture_output=True,
        text=True,
        check=True,
    )

    payload = json.loads(result.stdout)
    assert payload["schema"] == CEREBRO_CANON_MERGE_REVIEW_SCHEMA
    assert payload["summary"]["auto_merge_actions"] == 0
    assert payload["artifacts"]


def test_tool_registry_exposes_canon_merge_review():
    payload = tool_registry_payload()
    names = {tool["name"] for tool in payload["tools"]}

    assert "cerebro_canon_merge_review" in names
