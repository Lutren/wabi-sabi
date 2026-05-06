from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from obsai_core.fingerprint import stable_fingerprint
from obsai_core.gate import evaluate_action
from obsai_core.metrics import Regime, estimate_regime, estimate_residue_from_signals
from obsai_core.transduction import (
    CapabilityReceptor,
    RAGCalibrationRouter,
    ResidueAwareAttentionGate,
    RetrievalCandidate,
    SignalPacket,
    page_rank,
    transduce_signal,
)
from obsai_core.world import simulate_world


GOOD_ACTION = {
    "actor": "agent",
    "action_type": "send_email",
    "input": "Send a follow-up email using verified CRM notes and the confirmed invoice state.",
    "output": "Draft email references verified invoice status, avoids legal claims, and asks for scheduling confirmation.",
    "risk": 0.20,
    "reversibility": 0.85,
    "sources": [
        {"label": "CRM note", "confidence": 0.95, "verified": True},
        {"label": "Invoice record", "confidence": 0.90, "verified": True},
    ],
    "tool_calls": [{"name": "crm.lookup", "status": "ok"}],
    "self_check": {
        "summary": "Checked evidence and reversible impact.",
        "confidence": 0.85,
        "assumptions": [],
        "uncertainties": [],
        "falsifiers": ["invoice record mismatch"],
    },
}

BAD_ACTION = {
    "actor": "agent",
    "action_type": "delete",
    "input": "delete",
    "output": "done",
    "risk": 0.95,
    "reversibility": 0.05,
    "sources": [],
    "tool_calls": [],
    "policy_tags": ["requires_human_approval"],
}


class MetricsTests(unittest.TestCase):
    def test_residue_and_regime_are_stable(self) -> None:
        residue = estimate_residue_from_signals(["circularity", "corrections", "unresolved_tasks"])
        self.assertEqual(residue, 0.45)
        self.assertEqual(estimate_regime(residue), Regime.JAMMING_TEMPRANO)


class GateTests(unittest.TestCase):
    def test_gate_returns_stable_status_and_demo_claims(self) -> None:
        good = evaluate_action(GOOD_ACTION)
        bad = evaluate_action(BAD_ACTION)
        self.assertEqual(good["schemaVersion"], "obsai.action_gate.v1")
        self.assertEqual(good["status"], "APPROVE")
        self.assertEqual(bad["status"], "BLOCK")
        self.assertEqual(good["claims"]["thresholdCalibration"], "DEMO_ONLY")

    def test_gate_blocks_missing_required_receptor(self) -> None:
        action = {
            **GOOD_ACTION,
            "requires_receptor": True,
            "receptor_id": "",
        }
        decision = evaluate_action(action)
        self.assertEqual(decision["status"], "BLOCK")
        self.assertIn("authorized_receptor_required", decision["reasons"])


class TransductionTests(unittest.TestCase):
    def test_signal_only_activates_authorized_matching_receptor(self) -> None:
        packet = SignalPacket("publish", intensity=0.8)
        receptors = [
            CapabilityReceptor("repo_cleanup", accepts=("cleanup",), lane="cleanup"),
            CapabilityReceptor("publish", accepts=("publish",), lane="publishing", selectivity=0.9, calibration=0.8),
        ]
        result = transduce_signal(packet, receptors)
        self.assertTrue(result["accepted"])
        self.assertEqual(result["active_receptors"][0]["receptor_id"], "publish")

    def test_attention_gate_closes_on_high_residue(self) -> None:
        gate = ResidueAwareAttentionGate(threshold=0.35)
        clean = gate.admit({"relevance": 0.9, "authority": 0.8, "freshness": 0.7, "residue": 0.05})
        noisy = gate.admit({"relevance": 0.9, "authority": 0.8, "freshness": 0.7, "residue": 0.95})
        self.assertTrue(clean["admitted"])
        self.assertFalse(noisy["admitted"])

    def test_page_rank_and_rag_router_rank_authority(self) -> None:
        ranks = page_rank({"source_a": ["source_b"], "source_b": ["source_a"], "source_c": ["source_b"]})
        self.assertAlmostEqual(sum(ranks.values()), 1.0, places=6)
        router = RAGCalibrationRouter()
        ranked = router.rank(
            [
                RetrievalCandidate("low_authority", similarity=0.9, authority=0.1, freshness=0.5, residue=0.0),
                RetrievalCandidate("high_authority", similarity=0.8, authority=0.9, freshness=0.6, residue=0.0),
            ]
        )
        self.assertEqual(ranked[0]["candidate_id"], "high_authority")


class FingerprintTests(unittest.TestCase):
    def test_stable_fingerprint_ignores_dict_order(self) -> None:
        self.assertEqual(stable_fingerprint({"a": 1, "b": 2}), stable_fingerprint({"b": 2, "a": 1}))


class WorldTests(unittest.TestCase):
    def test_world_simulation_is_deterministic(self) -> None:
        first = simulate_world(ticks=8, seed="demo")
        second = simulate_world(ticks=8, seed="demo")
        self.assertEqual(first["fingerprint"], second["fingerprint"])
        self.assertEqual(first["claims"]["simulation"], "DEMO_ONLY")


class CliTests(unittest.TestCase):
    def test_cli_outputs_json_for_action_and_world(self) -> None:
        root = Path(__file__).resolve().parents[1]
        action = root / "examples" / "action_review.json"

        action_result = subprocess.run(
            [sys.executable, "-m", "obsai_core.cli", "evaluate-action", str(action)],
            cwd=root,
            text=True,
            capture_output=True,
            check=True,
        )
        action_payload = json.loads(action_result.stdout)
        self.assertIn(action_payload["status"], {"APPROVE", "REVIEW", "BLOCK"})
        self.assertEqual(action_payload["schemaVersion"], "obsai.action_gate.v1")

        world_result = subprocess.run(
            [sys.executable, "-m", "obsai_core.cli", "simulate-world", "--ticks", "4", "--seed", "demo"],
            cwd=root,
            text=True,
            capture_output=True,
            check=True,
        )
        world_payload = json.loads(world_result.stdout)
        self.assertEqual(world_payload["schemaVersion"], "obsai.world_simulation.v1")
        self.assertEqual(world_payload["ticks"], 4)


if __name__ == "__main__":
    unittest.main()
