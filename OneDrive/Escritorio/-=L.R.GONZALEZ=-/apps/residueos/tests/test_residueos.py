from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import threading
import unittest
import urllib.request
from http.server import ThreadingHTTPServer
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from residueos.gate import evaluate_action
from residueos.server import make_handler
from residueos.store import ResidueStore


GOOD_ACTION = {
    "actor": "agent",
    "actionType": "send_email",
    "input": "Send a follow-up email using the verified CRM notes and invoice state.",
    "output": "Draft email that references the verified invoice status, avoids legal claims, and asks for meeting availability.",
    "risk": 0.2,
    "reversibility": 0.85,
    "receptorId": "crm_followup_receptor",
    "receptorAuthorized": True,
    "selectivity": 0.92,
    "calibration": 0.84,
    "sources": [
        {"label": "CRM note", "confidence": 0.95, "verified": True},
        {"label": "Invoice record", "confidence": 0.92, "verified": True},
    ],
    "toolCalls": [{"name": "crm.lookup", "status": "ok"}],
    "selfCheck": {
        "summary": "Checked evidence and risks.",
        "confidence": 0.87,
        "assumptions": [],
        "uncertainties": [],
        "falsifiers": ["invoice record mismatch"],
    },
}

REVIEW_ACTION = {
    "actor": "agent",
    "actionType": "publish",
    "input": "Publish the summary after reviewing only one unverified note.",
    "output": "A public summary with caveats and unresolved source quality.",
    "risk": 0.45,
    "reversibility": 0.6,
    "receptorId": "publish_review_receptor",
    "receptorAuthorized": True,
    "selectivity": 0.74,
    "calibration": 0.58,
    "sources": [{"label": "draft note", "confidence": 0.45, "verified": False}],
    "toolCalls": [],
    "selfCheck": {
        "summary": "Some checks remain incomplete.",
        "confidence": 0.4,
        "assumptions": ["draft note is current"],
        "uncertainties": ["publication approval missing"],
        "falsifiers": [],
    },
}

BAD_ACTION = {
    "actor": "agent",
    "actionType": "delete",
    "input": "delete",
    "output": "done",
    "risk": 0.95,
    "reversibility": 0.05,
    "sources": [],
    "toolCalls": [],
    "policyTags": ["requires_human_approval"],
}


class GateTests(unittest.TestCase):
    def test_gate_returns_all_three_stable_statuses(self) -> None:
        self.assertEqual(evaluate_action(GOOD_ACTION)["status"], "APPROVE")
        self.assertEqual(evaluate_action(REVIEW_ACTION)["status"], "REVIEW")
        self.assertEqual(evaluate_action(BAD_ACTION)["status"], "BLOCK")

    def test_threshold_claims_are_marked_demo_only(self) -> None:
        decision = evaluate_action(GOOD_ACTION)
        self.assertTrue(decision["config"]["demo_only_thresholds"])
        self.assertEqual(decision["claims"]["thresholdCalibration"], "DEMO_ONLY")

    def test_consequential_action_without_receptor_blocks(self) -> None:
        action = {
            **GOOD_ACTION,
            "receptorId": "",
            "receptorAuthorized": False,
        }
        decision = evaluate_action(action)
        self.assertEqual(decision["status"], "BLOCK")
        self.assertIn("authorized receptor required", decision["reasons"])


class StoreTests(unittest.TestCase):
    def test_sqlite_persistence_and_human_review_audit(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            db_path = Path(tmp) / "residueos.sqlite"
            store = ResidueStore(db_path)
            record = store.insert_action(REVIEW_ACTION, evaluate_action(REVIEW_ACTION))

            reopened = ResidueStore(db_path)
            fetched = reopened.get_action(record["id"])
            self.assertIsNotNone(fetched)
            self.assertEqual(fetched["decision"]["status"], "REVIEW")
            self.assertEqual(len(fetched["audit"]), 1)
            self.assertEqual(fetched["audit"][0]["payload"]["receptorId"], "publish_review_receptor")

            reviewed = reopened.update_human_decision(record["id"], "APPROVED", "human", "reviewed evidence")
            self.assertIsNotNone(reviewed)
            self.assertEqual(reviewed["humanDecision"]["status"], "APPROVED")
            self.assertEqual(len(reviewed["audit"]), 2)


class CliTests(unittest.TestCase):
    def test_cli_evaluate_json_output(self) -> None:
        app_root = Path(__file__).resolve().parents[1]
        sample = app_root / "examples" / "sample_action.json"
        with tempfile.TemporaryDirectory() as tmp:
            db_path = Path(tmp) / "residueos.sqlite"
            result = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "residueos.cli",
                    "evaluate",
                    str(sample),
                    "--db",
                    str(db_path),
                ],
                cwd=app_root,
                text=True,
                capture_output=True,
                check=True,
            )
            payload = json.loads(result.stdout)
            self.assertEqual(payload["decision"]["schemaVersion"], "residueos.decision.v1")
            self.assertIn(payload["decision"]["status"], {"APPROVE", "REVIEW", "BLOCK"})
            self.assertTrue(db_path.exists())


class ServerTests(unittest.TestCase):
    def test_http_health_and_evaluate_smoke(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            db_path = Path(tmp) / "residueos.sqlite"
            server = ThreadingHTTPServer(("127.0.0.1", 0), make_handler(db_path))
            thread = threading.Thread(target=server.serve_forever, daemon=True)
            thread.start()
            base = f"http://127.0.0.1:{server.server_address[1]}"
            try:
                with urllib.request.urlopen(f"{base}/api/health", timeout=5) as response:
                    health = json.loads(response.read().decode("utf-8"))
                self.assertTrue(health["ok"])

                body = json.dumps(GOOD_ACTION).encode("utf-8")
                request = urllib.request.Request(
                    f"{base}/api/evaluate",
                    data=body,
                    headers={"Content-Type": "application/json"},
                    method="POST",
                )
                with urllib.request.urlopen(request, timeout=5) as response:
                    payload = json.loads(response.read().decode("utf-8"))
                self.assertEqual(payload["decision"]["schemaVersion"], "residueos.decision.v1")
                self.assertEqual(payload["decision"]["status"], "APPROVE")
            finally:
                server.shutdown()
                server.server_close()
                thread.join(timeout=5)


if __name__ == "__main__":
    unittest.main()
