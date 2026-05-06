from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from obsai_core.fingerprint import stable_fingerprint
from obsai_core.gate import evaluate_action
from obsai_core.metrics import Regime, estimate_regime, estimate_residue_from_signals
from obsai_core.ontology import ObservationEnvelope, ObservationEnvelopeStore, OntologyGraph, PACReasoner
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

    def test_gate_blocks_scientific_claim_without_verified_evidence(self) -> None:
        action = {
            **GOOD_ACTION,
            "action_type": "scientific_claim",
            "sources": [{"label": "draft hypothesis", "confidence": 0.7, "verified": False}],
            "self_check": {
                "summary": "Hypothesis only.",
                "confidence": 0.5,
                "assumptions": [],
                "uncertainties": ["no experiment yet"],
                "falsifiers": ["controlled observation fails"],
            },
            "method": "draft literature comparison",
        }
        decision = evaluate_action(action)
        self.assertEqual(decision["status"], "BLOCK")
        self.assertIn("scientific_claim_requires_verified_evidence", decision["reasons"])

    def test_gate_blocks_hard_boundaries_and_raw_download_import(self) -> None:
        action = {
            **GOOD_ACTION,
            "action_type": "raw_download_import",
            "policy_tags": ["raw_downloads"],
            "risk": 0.2,
            "reversibility": 0.9,
        }
        decision = evaluate_action(action)
        self.assertEqual(decision["status"], "BLOCK")
        self.assertIn("hard_boundary_requires_block", decision["reasons"])

    def test_gate_blocks_controlled_claim_without_verified_evidence(self) -> None:
        action = {
            **GOOD_ACTION,
            "claim_type": "social_prediction",
            "sources": [{"label": "synthetic lab", "confidence": 0.7, "verified": False}],
        }
        decision = evaluate_action(action)
        self.assertEqual(decision["status"], "BLOCK")
        self.assertIn("controlled_claim_requires_verified_evidence", decision["reasons"])


class OntologyTests(unittest.TestCase):
    def test_observation_envelope_prov_and_pac_reasoner(self) -> None:
        envelope = ObservationEnvelope(
            observer="debugtyr",
            subject="Agent Safety Gate",
            claim="Verified evidence should be required before publishing scientific claims.",
            kind="process",
            claim_type="scientific_claim",
            evidence=[{"label": "local test", "source": "tests", "verified": True, "confidence": 0.91}],
            confidence=0.82,
            provenance={"method": "unit test"},
            constraints={"falsifiers": ["gate approves unverified scientific claim"]},
        )
        graph = OntologyGraph()
        record = graph.add_envelope(envelope)
        reasoning = PACReasoner().evaluate(envelope)
        self.assertTrue(record["validation"]["conforms"])
        self.assertEqual(record["dolceType"], "dolce:perdurant")
        self.assertEqual(reasoning["status"], "APPROVE")
        self.assertEqual(record["provO"]["schemaVersion"], "obsai.prov_o_graph.v1")

    def test_observation_store_persists_envelope_in_sqlite(self) -> None:
        envelope = ObservationEnvelope(
            observer="debugtyr",
            subject="ResidueOS Lite",
            claim="Sponsors copy must avoid absolute safety claims.",
            kind="artifact",
            evidence=[{"label": "profile draft", "source": "docs", "verified": True, "confidence": 0.8}],
            confidence=0.75,
        )
        with tempfile.TemporaryDirectory() as tmp:
            db_path = Path(tmp) / "observations.sqlite"
            store = ObservationEnvelopeStore(db_path)
            stored = store.insert_envelope(envelope)
            fetched = store.get_envelope(envelope.envelope_id)
            self.assertEqual(stored["id"], envelope.envelope_id)
            self.assertIsNotNone(fetched)
            self.assertEqual(fetched["envelope"]["dolceType"], "dolce:endurant")
            self.assertEqual(len(store.list_envelopes()), 1)

    def test_observation_envelope_v2_round_trips_psi_gate_and_witness(self) -> None:
        payload = {
            "schemaVersion": "obsai.observation_envelope.v2",
            "observer": "claudio-nollm",
            "subject": "repo",
            "claim": {
                "text": "Dry-run patch plan is ready for review.",
                "claimType": "operational_claim",
                "epistemicState": "CERTEZA",
                "confidence": 0.88,
            },
            "kind": "process",
            "evidence": [{"label": "unit test", "source": "tests", "verified": True, "confidence": 0.9}],
            "psiState": {"R": 0.12, "Phi_eff": 0.84, "J_c": 0.75, "regime": "FUNCTIONAL"},
            "sigma": {"observer_profile": "code_agent", "dimensions": {"resolution": 0.8}},
            "falsifiers": [{"id": "dry_run_writes_file", "status": "passed"}],
            "gate": {"decision": "REVIEW", "reasons": ["dry-run only"]},
            "witness": {"previous_hash": "", "event_hash": "abc"},
            "familyStewardship": {
                "enabled": True,
                "localOnly": True,
                "storesSecretsPlaintext": False,
                "externalAction": False,
                "requiresHumanLegalAuthority": True,
            },
        }
        envelope = ObservationEnvelope.from_dict(payload)
        round_trip = envelope.to_dict()
        validation = PACReasoner().evaluate(envelope)

        self.assertEqual(round_trip["schemaVersion"], "obsai.observation_envelope.v2")
        self.assertEqual(round_trip["claimObject"]["epistemicState"], "CERTEZA")
        self.assertEqual(round_trip["psiState"]["regime"], "FUNCTIONAL")
        self.assertTrue(round_trip["familyStewardship"]["enabled"])
        self.assertEqual(validation["status"], "APPROVE")

    def test_observation_envelope_v2_blocks_jamming_state(self) -> None:
        envelope = ObservationEnvelope(
            observer="claudio-nollm",
            subject="host",
            claim="Host is jammed and must not approve writes.",
            kind="process",
            evidence=[{"label": "host report", "source": "runtime", "verified": True}],
            psi_state={"R": 0.91, "Phi_eff": 0.2, "J_c": 0.75, "regime": "JAMMING"},
            gate={"decision": "BLOCK"},
        )
        reasoning = PACReasoner().evaluate(envelope)
        self.assertEqual(reasoning["status"], "BLOCK")

    def test_observation_envelope_blocks_family_stewardship_plaintext_secrets(self) -> None:
        envelope = ObservationEnvelope(
            observer="wabi-sabi-local",
            subject="family continuity inventory",
            claim="Family stewardship inventory is local and redacted.",
            kind="artifact",
            evidence=[{"label": "unit test", "source": "tests", "verified": True}],
            family_stewardship={
                "enabled": True,
                "localOnly": True,
                "storesSecretsPlaintext": True,
                "externalAction": False,
            },
        )
        reasoning = PACReasoner().evaluate(envelope)
        self.assertEqual(reasoning["status"], "BLOCK")
        self.assertIn("family stewardship cannot store secrets in plaintext", reasoning["reasons"])


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

    def test_demo_agent_action_blocks_delete_and_allows_readme_summary(self) -> None:
        root = Path(__file__).resolve().parents[1]
        with tempfile.TemporaryDirectory() as tmp:
            delete_result = subprocess.run(
                [
                    sys.executable,
                    "demo_agent_action.py",
                    "--action",
                    "delete project folder",
                    "--witness-dir",
                    tmp,
                ],
                cwd=root,
                text=True,
                capture_output=True,
                check=True,
            )
            delete_payload = json.loads(delete_result.stdout)
            self.assertEqual(delete_payload["decision"], "BLOCK")
            self.assertIn("high_risk_low_reversibility", delete_payload["evidence"])
            self.assertTrue(Path(delete_payload["witness_log"]).exists())

            summary_result = subprocess.run(
                [
                    sys.executable,
                    "demo_agent_action.py",
                    "--action",
                    "summarize README",
                    "--witness-dir",
                    tmp,
                ],
                cwd=root,
                text=True,
                capture_output=True,
                check=True,
            )
            summary_payload = json.loads(summary_result.stdout)
            self.assertEqual(summary_payload["decision"], "APPROVE")

    def test_starter_benchmark_reports_action_gate_metrics(self) -> None:
        root = Path(__file__).resolve().parents[1]
        result = subprocess.run(
            [sys.executable, "benchmarks/run_agent_action_benchmark.py"],
            cwd=root,
            text=True,
            capture_output=True,
            check=True,
        )
        payload = json.loads(result.stdout)
        self.assertEqual(payload["schemaVersion"], "obsai.agent_action_benchmark.v1")
        self.assertEqual(payload["scenario_count"], 6)
        self.assertGreaterEqual(payload["accuracy"], 0.8)
        self.assertEqual(payload["false_blocks"], 0)


if __name__ == "__main__":
    unittest.main()
