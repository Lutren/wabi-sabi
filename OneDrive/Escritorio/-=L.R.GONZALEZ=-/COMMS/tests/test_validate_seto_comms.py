from __future__ import annotations

import importlib.util
from pathlib import Path
import sys
import unittest


ROOT = Path(__file__).resolve().parents[2]
VALIDATOR_PATH = ROOT / "COMMS" / "tools" / "validate_seto_comms.py"


def load_validator():
    spec = importlib.util.spec_from_file_location("validate_seto_comms", VALIDATOR_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load validate_seto_comms.py")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class ValidateSetoCommsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.validator = load_validator()

    def test_validator_includes_outbox_and_passes(self) -> None:
        result = self.validator.validate()

        self.assertEqual(result["schema"], "medioevo.seto_comms_validator_result.v1")
        self.assertEqual(result["status"], "PASS")
        self.assertGreaterEqual(result["counts"]["inbox_messages"], 1)
        self.assertGreaterEqual(result["counts"]["outbox_messages"], 1)
        self.assertEqual(result["errors"], [])


if __name__ == "__main__":
    unittest.main()
