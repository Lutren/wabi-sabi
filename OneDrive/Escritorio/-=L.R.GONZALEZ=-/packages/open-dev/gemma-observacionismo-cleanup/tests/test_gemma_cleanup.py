from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from gemma_observacionismo_cleanup.core import (
    fingerprint_payload,
    noise_report,
    observe_payload,
)


def test_observe_payload_counts_text_fields() -> None:
    report = observe_payload({"response": "Texto limpio.", "nested": {"answer": "Otro texto."}})
    assert report["ok"] is True
    assert report["text_fields"] == 2
    assert report["metrics"]["word_count"] == 4


def test_noise_report_detects_improvement() -> None:
    before = {"response": "As an AI language model, TODO ajustar esto!!!"}
    after = {"response": "Ajuste listo con limite declarado."}
    report = noise_report(before, after)
    assert report["improved"] is True
    assert report["delta"]["residue_score"] < 0


def test_fingerprint_is_stable_for_key_order() -> None:
    first = fingerprint_payload({"b": 2, "a": 1})
    second = fingerprint_payload({"a": 1, "b": 2})
    assert first["fingerprint"] == second["fingerprint"]
