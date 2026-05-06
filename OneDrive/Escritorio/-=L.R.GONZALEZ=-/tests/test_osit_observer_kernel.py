from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "tools" / "observacionismo" / "osit_observer_kernel.py"


def load_kernel():
    spec = importlib.util.spec_from_file_location("osit_observer_kernel", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_runtime_state_separates_r_ia_and_updates_discretely() -> None:
    kernel = load_kernel()
    state = kernel.RuntimeState(R_IA=0.15)

    state.update(tokens_in=1200, tokens_out=500, num_ctx=8192, closes=1, risk=0.1)

    assert 0.0 <= state.R_IA <= 1.0
    assert state.regime() in {"optimo", "funcional", "pre_jamming", "jamming_temprano", "jamming"}
    assert "R_IA" in state.to_dict()
    assert "phi_eff_formal_runtime" in state.to_dict()


def test_safe_answer_approves_without_tool_execution() -> None:
    kernel = load_kernel()
    result = kernel.audit_action({"action": "answer", "reason": "local answer", "value": "ok"})

    assert result["action_gate"] == "APPROVE"
    assert result["risk"] == 0.0
    assert "record WitnessLog" in result["allowed_next_actions"]


def test_browser_goto_allowed_domain_requires_review() -> None:
    kernel = load_kernel()
    result = kernel.audit_action(
        {"action": "browser.goto", "target": "https://wikipedia.org/wiki/Observability", "reason": "read source"}
    )

    assert result["action_gate"] == "REVIEW"
    assert "review_action:browser.goto" in result["reasons"]


def test_credential_or_privilege_action_blocks() -> None:
    kernel = load_kernel()
    result = kernel.audit_action(
        {
            "action": "privilege.escalate",
            "target": "Windows UAC bypass",
            "value": "token password",
        }
    )

    assert result["action_gate"] == "BLOCK"
    assert any(reason.startswith("blocked_action:privilege.escalate") for reason in result["reasons"])
    assert any(reason.startswith("sensitive_terms:") for reason in result["reasons"])


def test_disallowed_domain_blocks() -> None:
    kernel = load_kernel()
    result = kernel.audit_action(
        {"action": "browser.goto", "target": "https://unknown.invalid/private", "reason": "read"}
    )

    assert result["action_gate"] == "BLOCK"
    assert any(reason.startswith("domain_not_allowed:") for reason in result["reasons"])


def test_observation_envelope_carries_gate_and_no_execution() -> None:
    kernel = load_kernel()
    result = kernel.audit_action({"action": "network.scan", "target": "192.168.1.1/24"})
    envelope = kernel.observation_envelope(result, source="unit-test")

    assert envelope["action_gate"] == "BLOCK"
    assert envelope["decision"] == "OSIT_OBSERVER_BLOCK"
    assert any("no tool execution occurred" in item for item in envelope["evidence"])


def test_cli_block_returns_two_and_json(tmp_path: Path) -> None:
    trace = tmp_path / "trace.jsonl"
    result = subprocess.run(
        [
            sys.executable,
            str(SCRIPT),
            "audit",
            "--action-json",
            json.dumps({"action": "payment.submit", "target": "checkout", "value": "card"}),
            "--trace",
            str(trace),
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )

    assert result.returncode == 2
    payload = json.loads(result.stdout)
    assert payload["audit"]["action_gate"] == "BLOCK"
    assert payload["tool_executed"] is False
    assert trace.exists()
