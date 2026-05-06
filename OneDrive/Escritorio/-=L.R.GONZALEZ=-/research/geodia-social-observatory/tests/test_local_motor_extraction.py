from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from geodia_social_observatory.artifacts import create_artifact_record, project_artifact_graph
from geodia_social_observatory.behavior import analyze_behavior_signature
from geodia_social_observatory.cli import main as cli_main
from geodia_social_observatory.contracts import (
    ARTIFACT_RECORD_SCHEMA,
    BEHAVIOR_SIGNATURE_SCHEMA,
    DUAT_CONWAY_SIMULATION_SCHEMA,
    DUAT_HEALTH_WINDOW_SCHEMA,
    DUAT_V2_INTAKE_SCHEMA,
    LOCAL_SOURCE_INTAKE_SCHEMA,
    OBSERVATION_EVENT_SCHEMA,
    ROUTE_DECISION_SCHEMA,
)
from geodia_social_observatory.duat_sim import run_duat_conway_simulation
from geodia_social_observatory.duat_v2_intake import build_duat_v2_intake
from geodia_social_observatory.events import JsonlEventStore, build_event
from geodia_social_observatory.health import duat_health_window
from geodia_social_observatory.router import RequestFeatures, decide_route
from geodia_social_observatory.source_registry import build_local_source_intake


class LocalMotorExtractionTests(unittest.TestCase):
    def test_local_source_intake_classifies_downloads_without_copying(self) -> None:
        registry = build_local_source_intake()
        self.assertEqual(registry["schema"], LOCAL_SOURCE_INTAKE_SCHEMA)
        self.assertEqual(registry["source_count"], 14)
        self.assertEqual(registry["boundary"]["publication_gate"], "BLOCK")
        self.assertTrue(all(row["copy_policy"].startswith("do_not_copy_raw") for row in registry["sources"]))
        existing = [row for row in registry["sources"] if row["exists"]]
        self.assertEqual(registry["missing_count"], registry["source_count"] - len(existing))
        self.assertTrue(all("sha256" in row for row in existing))
        if not existing:
            self.assertEqual(registry["missing_count"], registry["source_count"])
        self.assertTrue(any(row["lane"] == "FUNCTIONAL" for row in registry["sources"]))
        self.assertTrue(any("LAB" in row["lane"] for row in registry["sources"]))
        self.assertTrue(any(row["filename"] == "duat_v2.html" for row in registry["sources"]))
        self.assertTrue(any(row["filename"] == "deep-research-report (5).md" for row in registry["sources"]))

    def test_duat_v2_intake_separates_functional_lab_and_blocked(self) -> None:
        intake = build_duat_v2_intake()
        self.assertEqual(intake["schema"], DUAT_V2_INTAKE_SCHEMA)
        self.assertEqual(intake["source_count"], 4)
        self.assertEqual(intake["integration_decision"]["raw_copy_policy"], "do_not_copy_raw")
        self.assertEqual(intake["integration_decision"]["publication_gate"], "BLOCK")
        filenames = {row["filename"] for row in intake["sources"]}
        self.assertEqual(
            filenames,
            {
                "deep-research-report (4).md",
                "Esto es material extraordinariament.txt",
                "duat_v2.html",
                "deep-research-report (5).md",
            },
        )
        self.assertIn("artifact_graph_edges", intake["integration_decision"]["functional_now"])
        self.assertIn("three_lane_duat_roadmap", intake["integration_decision"]["functional_now"])
        self.assertIn("eeg_bridge", intake["integration_decision"]["lab_private"])
        self.assertIn("guaranteed_social_prediction", intake["integration_decision"]["blocked"])
        self.assertIn("layer_mixing", intake["integration_decision"]["resolved_local_blockers"])
        self.assertIn("heavy_model_path", intake["integration_decision"]["blocked_by_gate"])
        self.assertIn("supports", intake["artifact_graph_contract"]["edge_types"])
        self.assertIn("contradicts", intake["artifact_graph_contract"]["edge_types"])
        self.assertIn("verified_by", intake["artifact_graph_contract"]["edge_types"])

    def test_behavior_signature_is_stable_risk_signal(self) -> None:
        text = (
            "Observo el sistema y creo que debemos revisar la evidencia, "
            "porque una conclusion sin pruebas aumenta el residuo. "
            "Tal vez conviene pedir otra observacion antes de actuar?"
        )
        first = analyze_behavior_signature(text, subject_id="agent_demo")
        second = analyze_behavior_signature(text, subject_id="agent_demo")
        self.assertEqual(first["schema"], BEHAVIOR_SIGNATURE_SCHEMA)
        self.assertEqual(first["signature_hash"], second["signature_hash"])
        self.assertEqual(len(first["dimensions"]), 8)
        self.assertIn(first["phase"], ("ordered", "griffiths", "chaotic"))
        self.assertIn("not a standalone identity proof", first["claim_boundary"])

    def test_router_decides_cache_sim_strong_and_human(self) -> None:
        cache = decide_route(RequestFeatures(cache_hit_prob=0.99, impact=0.1, policy_risk=0.1))
        sim = decide_route(RequestFeatures(simulator_needed=0.9, uncertainty=0.4))
        strong = decide_route(RequestFeatures(impact=0.8, uncertainty=0.7))
        human = decide_route(RequestFeatures(policy_risk=0.9, auth_drift=0.2))
        self.assertEqual(cache["schema"], ROUTE_DECISION_SCHEMA)
        self.assertEqual(cache["route"], "cache")
        self.assertEqual(sim["route"], "sim")
        self.assertEqual(strong["route"], "strong")
        self.assertEqual(human["route"], "human")
        self.assertTrue(human["requires_approval"])

    def test_event_store_replay_and_artifact_graph_are_deterministic(self) -> None:
        artifact = create_artifact_record(
            "claim",
            "Router keeps heavy models gated",
            {"route": "human", "reason": "policy risk"},
            evidence=[{"type": "test", "sha256": "abc123"}],
        )
        self.assertEqual(artifact["schema"], ARTIFACT_RECORD_SCHEMA)
        graph = project_artifact_graph([artifact])
        self.assertEqual(graph["node_count"], 1)
        with tempfile.TemporaryDirectory() as tmp:
            store = JsonlEventStore(Path(tmp) / "events.jsonl")
            event = build_event(
                "artifact_created",
                "agt_verifier",
                {"artifact_id": artifact["artifact_id"], "route": "human"},
                approval_state="required",
            )
            store.append(event)
            first = store.replay_state()
            second = store.replay_state()
        self.assertEqual(event["schema"], OBSERVATION_EVENT_SCHEMA)
        self.assertEqual(first["event_count"], 1)
        self.assertEqual(first["approvals_required"], 1)
        self.assertEqual(first["replay_sha256"], second["replay_sha256"])

    def test_duat_health_window_computes_engineering_metrics(self) -> None:
        result = duat_health_window(
            [
                {
                    "verify_fail": 0,
                    "residue": 0.2,
                    "queue_pressure": 0.1,
                    "auth_drift": 0.1,
                    "accepted_utility": 0.8,
                    "latency_ms": 100,
                    "gpu_seconds": 0.2,
                    "cooperation": 0.8,
                    "contradiction": 0.1,
                    "novelty_kept": 0.7,
                }
            ]
        )
        self.assertEqual(result["schema"], DUAT_HEALTH_WINDOW_SCHEMA)
        self.assertEqual(result["status"], "evaluated")
        self.assertGreater(result["Phi_Duat"], 0)

    def test_duat_conway_simulation_is_seed_deterministic(self) -> None:
        first = run_duat_conway_simulation(seed=7, size=10, steps=5)
        second = run_duat_conway_simulation(seed=7, size=10, steps=5)
        self.assertEqual(first["schema"], DUAT_CONWAY_SIMULATION_SCHEMA)
        self.assertEqual(first["state_sha256"], second["state_sha256"])
        self.assertAlmostEqual(sum(first["phase_percentages"].values()), 1.0, places=4)

    def test_cli_new_commands_emit_contracts(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "signature.json"
            rc = cli_main(
                [
                    "signature",
                    "--text",
                    "Observo evidencia porque quizas el sistema necesita otra prueba?",
                    "--out",
                    str(out),
                ]
            )
            signature = json.loads(out.read_text(encoding="utf-8"))
            sim_out = Path(tmp) / "sim.json"
            rc2 = cli_main(["simulate-duat", "--seed", "3", "--size", "8", "--steps", "2", "--out", str(sim_out)])
            sim = json.loads(sim_out.read_text(encoding="utf-8"))
            duat_v2_out = Path(tmp) / "duat_v2.json"
            rc3 = cli_main(["duat-v2-intake", "--out", str(duat_v2_out)])
            duat_v2 = json.loads(duat_v2_out.read_text(encoding="utf-8"))
        self.assertEqual(rc, 0)
        self.assertEqual(rc2, 0)
        self.assertEqual(rc3, 0)
        self.assertEqual(signature["schema"], BEHAVIOR_SIGNATURE_SCHEMA)
        self.assertEqual(sim["schema"], DUAT_CONWAY_SIMULATION_SCHEMA)
        self.assertEqual(duat_v2["schema"], DUAT_V2_INTAKE_SCHEMA)


if __name__ == "__main__":
    unittest.main()
