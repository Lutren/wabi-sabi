from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from wabi_sabi.core.claim_contract import CLAIM_CONTRACT_SCHEMA, evaluate_claim_contract_payload
from wabi_sabi.core.geodia_synthetic_surface import build_geodia_synthetic_surface


GEODIA_SYNTHETIC_FALSIFIER_SCHEMA = "wabi.geodia_synthetic_falsifier.v1"


def build_geodia_synthetic_falsifier() -> dict[str, Any]:
    first = build_geodia_synthetic_surface()
    second = build_geodia_synthetic_surface()
    tests = [
        _test_result(
            "BOUNDED_DOMAIN",
            first["bounded"] is True,
            "All PSI values stay in [0, 1] and EML stays in [0, 10].",
            "Fails if any output leaves the declared numeric domain.",
        ),
        _test_result(
            "DETERMINISTIC_FIXTURE",
            first["metrics"] == second["metrics"] and first["cells"]["after"] == second["cells"]["after"],
            "Two consecutive deterministic fixture runs return identical metrics and updated cells.",
            "Fails if repeated local runs diverge without input change.",
        ),
        _test_result(
            "LOW_CLAIM_GATE",
            first["status"] == "SYNTHETIC_ONLY" and first["claim_gate"].startswith("NO_PUBLIC_STRONG_CLAIM"),
            "The surface marks itself synthetic-only and low-claim.",
            "Fails if the surface claims scientific, production, or public validation.",
        ),
        _test_result(
            "NO_EXTERNAL_IO",
            first["source"]["external_io"] is False and first["source"]["runtime_writes"] is False,
            "The surface performs no external I/O and no runtime writes.",
            "Fails if network, browser, archive import, publication, or source writes are introduced.",
        ),
    ]
    passed = all(test["passed"] for test in tests)
    contract = {
        "schema": CLAIM_CONTRACT_SCHEMA,
        "claim": "geodia_synthetic_surface is a deterministic local smoke surface with bounded synthetic metrics only.",
        "claim_level": "operational",
        "evidence": [
            "python -m wabi_sabi.cli.main geodia-synthetic --json",
            "python -m pytest tests\\test_geodia_synthetic_surface.py -q",
        ],
        "falsifiers": [test["falsifier"] for test in tests],
        "risk_flags": [],
    }
    return {
        "schema": GEODIA_SYNTHETIC_FALSIFIER_SCHEMA,
        "generated_at_utc": _utc_now(),
        "ok": passed,
        "status": "RESEARCH_ONLY_SYNTHETIC_FALSIFIER",
        "result": "PASS" if passed else "FAIL",
        "action_gate": "APPROVE_LOCAL_SYNTHETIC",
        "claim_gate": "OPERATIONAL_ONLY_NO_PUBLIC_STRONG_CLAIM",
        "surface": {
            "schema": first["schema"],
            "status": first["status"],
            "claim_gate": first["claim_gate"],
            "bounded": first["bounded"],
            "after_metrics": first["metrics"]["after"],
        },
        "falsifiers": tests,
        "claim_contract": contract,
        "claim_evaluation": None,
        "artifacts": [],
        "certainty": [
            "The falsifier only tests the local synthetic contract.",
            "Passing this falsifier does not validate real physics, economics, or city behavior.",
        ],
        "inference": [
            "The module is safe as a pre-dashboard gate for RESEARCH_ONLY visualizations.",
        ],
        "unknown": [
            "Real dataset calibration is still absent.",
            "Scientific/public claims still require independent numeric validation and review.",
        ],
    }


def write_geodia_synthetic_falsifier(payload: dict[str, Any], *, workspace: str | Path, output_dir: str | Path) -> dict[str, Any]:
    output_path = Path(output_dir).resolve()
    output_path.mkdir(parents=True, exist_ok=True)
    contract_path = output_path / "GEODIA_SYNTHETIC_SURFACE_CLAIM_CONTRACT.json"
    report_path = output_path / "GEODIA_SYNTHETIC_FALSIFIER.json"
    contract_path.write_text(
        json.dumps(payload["claim_contract"], indent=2, ensure_ascii=False, sort_keys=True),
        encoding="utf-8",
    )
    evaluation = evaluate_claim_contract_payload(payload["claim_contract"], contract_path=contract_path)
    enriched = {
        **payload,
        "claim_evaluation": evaluation,
        "artifacts": [str(contract_path), str(report_path)],
    }
    report_path.write_text(json.dumps(enriched, indent=2, ensure_ascii=False, sort_keys=True), encoding="utf-8")
    return enriched


def _test_result(test_id: str, passed: bool, evidence: str, falsifier: str) -> dict[str, Any]:
    return {
        "id": test_id,
        "passed": bool(passed),
        "status": "pass" if passed else "fail",
        "evidence": evidence,
        "falsifier": falsifier,
    }


def _utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()
