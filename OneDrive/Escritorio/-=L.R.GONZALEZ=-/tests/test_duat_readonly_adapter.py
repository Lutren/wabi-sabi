from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path

from claudio.adapters.duat_readonly_adapter import DuatReadonlyAdapter, ReadOnlyViolation


ROOT = Path(__file__).resolve().parents[1]


class DuatReadonlyAdapterTests(unittest.TestCase):
    def setUp(self) -> None:
        self.adapter = DuatReadonlyAdapter(ROOT)

    def test_status_is_readonly_and_boundary_aware(self) -> None:
        status = self.adapter.status()
        self.assertEqual(status["schema"], "claudio.duat_readonly.status.v1")
        self.assertEqual(status["mode"], "READ_ONLY")
        self.assertFalse(status["write_enabled"])
        self.assertEqual(status["external_actions"], "BLOCK")
        self.assertEqual(status["public_private_boundary"], "PRESERVED")

    def test_source_registry_lists_required_interfaces_with_hashes(self) -> None:
        registry = self.adapter.source_registry()
        source_ids = {source["source_id"] for source in registry["sources"]}
        self.assertIn("duat_genesis_public", source_ids)
        self.assertIn("duat_rpg_private_living_world", source_ids)
        self.assertIn("seto_comms_contracts", source_ids)
        available_without_hash = [
            source["source_id"]
            for source in registry["sources"]
            if source["available"] and not (source.get("sha256") or source.get("directory_sha256"))
        ]
        self.assertEqual(available_without_hash, [])

    def test_public_report_does_not_expose_private_sources(self) -> None:
        report = self.adapter.report("public")
        self.assertEqual(report["schema"], "claudio.duat_readonly.report.v1")
        self.assertTrue(report["sources"])
        self.assertTrue(all(source["lane"] == "public" for source in report["sources"]))
        self.assertFalse(any(source["privacy"].startswith("PRIVATE") for source in report["sources"]))
        self.assertIn("write_to_duat_internal", report["blocked_actions"])

    def test_falsifiers_cover_required_claims(self) -> None:
        for claim_id in (
            "duat_public_boundary",
            "readonly_adapter",
            "duat_claims_low",
            "living_world_fixture_contract",
            "source_registry_hashes",
            "comms_actiongate",
        ):
            result = self.adapter.falsify(claim_id)
            self.assertEqual(result["schema"], "claudio.duat_readonly.falsifier.v1")
            self.assertEqual(result["status"], "PASS", claim_id)

    def test_unknown_claim_is_blocked(self) -> None:
        result = self.adapter.falsify("unregistered_private_claim")
        self.assertEqual(result["status"], "BLOCK")
        self.assertIn("available_claims", result)

    def test_write_and_apply_are_blocked(self) -> None:
        with self.assertRaises(ReadOnlyViolation):
            self.adapter.write({"target": "duat"})
        with self.assertRaises(ReadOnlyViolation):
            self.adapter.apply({"target": "duat"})

    def test_public_fixture_has_private_rpg_shape_without_private_lore(self) -> None:
        fixture = json.loads((ROOT / "fixtures/duat/public_synthetic_fixture.json").read_text(encoding="utf-8"))
        living_world = fixture["living_world_fixture_spec"]
        self.assertEqual(living_world["expected_output"], "LivingWorldEvents")
        self.assertEqual(len(living_world["npcs"]), 10)
        self.assertEqual(len(living_world["zones"]), 3)
        self.assertEqual(len(living_world["events"]), 20)
        self.assertEqual({event["output"] for event in living_world["events"]}, {"LivingWorldEvents"})

    def test_cli_outputs_json(self) -> None:
        result = subprocess.run(
            [sys.executable, "-m", "claudio.adapters.duat_readonly_adapter", "falsify", "readonly_adapter"],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=True,
        )
        payload = json.loads(result.stdout)
        self.assertEqual(payload["status"], "PASS")


if __name__ == "__main__":
    unittest.main()
