import hashlib
import json
import subprocess
import sys
from pathlib import Path

from wabi_sabi.core.cerebro_variant_compare import (
    CEREBRO_VARIANT_COMPARISON_SCHEMA,
    build_cerebro_variant_comparison,
    write_cerebro_variant_comparison,
)
from wabi_sabi.core.tool_registry import tool_registry_payload


def _sha(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _write_manifest(index: Path, rows: list[dict]) -> None:
    index.mkdir(parents=True, exist_ok=True)
    with (index / "LINE_AUDIT_MANIFEST.jsonl").open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")


def _write_signals(index: Path, rows: list[dict]) -> None:
    with (index / "LINE_SIGNAL_INDEX.jsonl").open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")


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
        "code_candidate_count": 1 if Path(path).suffix == ".py" else 0,
        "code_fence_count": 0,
    }


def _fixture_workspace(tmp_path: Path) -> Path:
    workspace = tmp_path
    index = workspace / "runtime" / "cerebro_master_index"
    exact = "# Observacionismo\nR Phi_eff ActionGate\n"
    variant_a = "# PSI\nR Phi_eff ActionGate\n"
    variant_b = "# PSI\nR Sigma OSIT\n"
    code_a = "def run():\n    return 'safe'\n"
    code_b = "def run():\n    return 'changed'\n"
    files = {
        "CEREBRO/01.md": exact,
        "CEREBRO/copy/01.md": exact,
        "CEREBRO/02.md": variant_a,
        "CEREBRO/archive/02.md": variant_b,
        "CEREBRO/app.py": code_a,
        "CEREBRO/archive/app.py": code_b,
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
        _record("CEREBRO/app.py", code_a, signals={"agent_programming": 1}),
        _record("CEREBRO/archive/app.py", code_b, signals={"agent_programming": 1}),
    ]
    _write_manifest(index, rows)
    _write_signals(
        index,
        [
            {"path": "CEREBRO/02.md", "line_no": 2, "excerpt": "R Phi_eff ActionGate", "signals": ["R", "Phi_eff", "ActionGate"]},
            {"path": "CEREBRO/archive/02.md", "line_no": 2, "excerpt": "R Sigma OSIT", "signals": ["R", "Sigma", "OSIT"]},
        ],
    )
    return workspace


def test_cerebro_variant_comparison_classifies_groups(tmp_path):
    workspace = _fixture_workspace(tmp_path)
    payload = build_cerebro_variant_comparison(workspace)

    assert payload["schema"] == CEREBRO_VARIANT_COMPARISON_SCHEMA
    assert payload["summary"]["variant_group_count"] >= 3
    statuses = {item["semantic_status"] for item in payload["comparisons"]}
    assert "EXACT_DUPLICATE" in statuses
    assert "MATERIAL_SIGNAL_DELTA" in statuses
    assert "CODE_OR_CONFIG_MATERIAL_DELTA" in statuses
    assert payload["not_claimed"]


def test_write_cerebro_variant_comparison_outputs_json_md_and_actions(tmp_path):
    workspace = _fixture_workspace(tmp_path)
    payload = build_cerebro_variant_comparison(workspace)
    artifacts = write_cerebro_variant_comparison(payload, workspace / "runtime" / "cerebro_master_index")

    assert len(artifacts) == 3
    for artifact in artifacts:
        assert Path(artifact).exists()
    parsed = json.loads(Path(artifacts[0]).read_text(encoding="utf-8"))
    assert parsed["schema"] == CEREBRO_VARIANT_COMPARISON_SCHEMA


def test_cerebro_variant_compare_cli_json(tmp_path):
    workspace = _fixture_workspace(tmp_path)
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "wabi_sabi.cli.main",
            "variant-compare",
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
    assert payload["schema"] == CEREBRO_VARIANT_COMPARISON_SCHEMA
    assert payload["summary"]["variant_group_count"] >= 3
    assert payload["artifacts"]


def test_tool_registry_exposes_variant_compare():
    payload = tool_registry_payload()
    names = {tool["name"] for tool in payload["tools"]}

    assert "cerebro_variant_compare" in names
