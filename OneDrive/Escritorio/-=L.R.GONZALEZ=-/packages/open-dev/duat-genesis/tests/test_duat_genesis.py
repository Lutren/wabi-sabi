from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from duat_genesis import falsify_run, report_run, run_simulation


class DuatGenesisTests(unittest.TestCase):
    def test_simulation_is_deterministic_and_synthetic(self) -> None:
        first = run_simulation(seed="demo", size=8, ticks=5)
        second = run_simulation(seed="demo", size=8, ticks=5)
        self.assertEqual(first.fingerprint, second.fingerprint)
        self.assertEqual(first.claims["data"], "SYNTHETIC_ONLY")
        self.assertEqual(first.claims["private_engineering"], "EXCLUDED")

    def test_report_and_falsifiers_have_stable_shape(self) -> None:
        run = run_simulation(seed="demo", size=6, ticks=3)
        report = report_run(run)
        falsifiers = falsify_run(run)
        self.assertEqual(report["schemaVersion"], "duat.genesis.report.v1")
        self.assertEqual(report["claims"]["calibration"], "DEMO_ONLY")
        self.assertTrue(all(item.passed for item in falsifiers))

    def test_cli_outputs_json(self) -> None:
        root = Path(__file__).resolve().parents[1]
        result = subprocess.run(
            [sys.executable, "-m", "duat_genesis.cli", "falsify", "--seed", "demo", "--ticks", "2"],
            cwd=root,
            text=True,
            capture_output=True,
            check=True,
        )
        payload = json.loads(result.stdout)
        self.assertEqual(payload[0]["schemaVersion"], "duat.genesis.falsifier_result.v1")
        self.assertTrue(payload[0]["passed"])


if __name__ == "__main__":
    unittest.main()
