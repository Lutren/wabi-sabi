import hashlib
import json
import subprocess
import sys
from pathlib import Path

from wabi_sabi.core.cerebro_duplicate_migration_plan import (
    CEREBRO_DUPLICATE_MIGRATION_PLAN_SCHEMA,
    build_cerebro_duplicate_migration_plan,
    write_cerebro_duplicate_migration_plan,
)
from wabi_sabi.core.cerebro_variant_compare import (
    build_cerebro_variant_comparison,
    write_cerebro_variant_comparison,
)
from wabi_sabi.core.tool_registry import tool_registry_payload


def _sha(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _record(path: str, text: str, *, signals: dict[str, int]) -> dict:
    return {
        "path": path,
        "name": Path(path).name,
        "suffix": Path(path).suffix,
        "sha256": _sha(text),
        "classification": "TEXT",
        "source_kind": "filesystem_text",
        "line_count": len(text.splitlines()),
        "size_bytes": len(text.encode("utf-8")),
        "signal_count": sum(signals.values()),
        "signals": signals,
        "code_candidate_count": 0,
        "code_fence_count": 0,
    }


def _fixture_workspace(tmp_path: Path) -> Path:
    workspace = tmp_path
    index = workspace / "runtime" / "cerebro_master_index"
    index.mkdir(parents=True, exist_ok=True)
    exact = "# Observacionismo\nR Phi_eff ActionGate\n"
    variant_a = "# PSI\nR Phi_eff ActionGate\n"
    variant_b = "# PSI\nR Sigma OSIT\n"
    files = {
        "CEREBRO/01.md": exact,
        "CEREBRO/copy/01.md": exact,
        "CEREBRO/02.md": variant_a,
        "CEREBRO/archive/02.md": variant_b,
    }
    for rel, text in files.items():
        target = workspace / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text, encoding="utf-8")
    rows = [
        _record("CEREBRO/01.md", exact, signals={"R": 1, "Phi_eff": 1, "ActionGate": 1}),
        _record("CEREBRO/copy/01.md", exact, signals={"R": 1, "Phi_eff": 1, "ActionGate": 1}),
        _record("CEREBRO/02.md", variant_a, signals={"R": 1, "Phi_eff": 1, "ActionGate": 1}),
        _record("CEREBRO/archive/02.md", variant_b, signals={"R": 1, "Sigma": 1, "OSIT": 1}),
    ]
    with (index / "LINE_AUDIT_MANIFEST.jsonl").open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")
    (index / "LINE_SIGNAL_INDEX.jsonl").write_text("", encoding="utf-8")
    comparison = build_cerebro_variant_comparison(workspace)
    write_cerebro_variant_comparison(comparison, index)
    return workspace


def test_duplicate_migration_plan_uses_only_exact_duplicates(tmp_path):
    workspace = _fixture_workspace(tmp_path)
    payload = build_cerebro_duplicate_migration_plan(workspace)

    assert payload["schema"] == CEREBRO_DUPLICATE_MIGRATION_PLAN_SCHEMA
    assert payload["summary"]["exact_duplicate_groups"] == 1
    assert payload["summary"]["proposed_archive_moves"] == 1
    assert payload["summary"]["source_mutations"] == 0
    assert payload["actions"][0]["status"] == "READY_FOR_REVIEW"
    assert payload["actions"][0]["source"] == "CEREBRO/copy/01.md"
    assert payload["actions"][0]["canonical_preserved"] == "CEREBRO/01.md"
    assert payload["not_claimed"]


def test_write_duplicate_migration_plan_outputs_json_md_jsonl_csv(tmp_path):
    workspace = _fixture_workspace(tmp_path)
    payload = build_cerebro_duplicate_migration_plan(workspace)
    artifacts = write_cerebro_duplicate_migration_plan(payload, workspace / "runtime" / "cerebro_master_index")

    assert len(artifacts) == 4
    for artifact in artifacts:
        assert Path(artifact).exists()
    parsed = json.loads(Path(artifacts[0]).read_text(encoding="utf-8"))
    assert parsed["schema"] == CEREBRO_DUPLICATE_MIGRATION_PLAN_SCHEMA


def test_duplicate_migration_plan_cli_json(tmp_path):
    workspace = _fixture_workspace(tmp_path)
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "wabi_sabi.cli.main",
            "plan-duplicados",
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
    assert payload["schema"] == CEREBRO_DUPLICATE_MIGRATION_PLAN_SCHEMA
    assert payload["summary"]["proposed_archive_moves"] == 1
    assert payload["artifacts"]


def test_tool_registry_exposes_duplicate_migration_plan():
    payload = tool_registry_payload()
    names = {tool["name"] for tool in payload["tools"]}

    assert "cerebro_duplicate_migration_plan" in names
