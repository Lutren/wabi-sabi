"""Behavioral signature extraction as a risk signal, not identity proof."""

from __future__ import annotations

import math
import re
from typing import Any

from .contracts import BEHAVIOR_SIGNATURE_SCHEMA


DIMS = (
    ("curiosity", "curiosidad"),
    ("lex_div", "diversidad lexica"),
    ("causality", "razonamiento"),
    ("humility", "humildad"),
    ("abstraction", "abstraccion"),
    ("meta", "meta-conciencia"),
    ("coupling", "acoplamiento"),
    ("coherence", "coherencia"),
)

CHI_STAR = 0.567
GRIFFITHS_LOW = 0.369
GRIFFITHS_HIGH = 0.879

WORD_RE = re.compile(r"\b[a-záéíóúüñ]+\b", re.I)
HEDGE_RE = re.compile(r"\b(quizas|quizá|quizás|tal vez|posiblemente|podria|podría|maybe|perhaps|might|probably|creo|pienso|parece)\b", re.I)
ASSERT_RE = re.compile(r"\b(siempre|nunca|es|son|debe|jamas|jamás|todo|nada|imposible|obvio|claro|always|never|must)\b", re.I)
CONNECTOR_RE = re.compile(r"\b(porque|aunque|sin embargo|por lo tanto|ademas|además|pero|pues|thus|because|however|therefore|although|since)\b", re.I)
META_RE = re.compile(r"\b(observ|pens|sient|creo|cree|noto|nota|percib|analiz|reflexion|consider|watch|think|feel|believe|notice|observe)\b", re.I)
SELF_RE = re.compile(r"\b(yo|me|mi|mis|mio|mío|i|my)\b", re.I)
OTHER_RE = re.compile(r"\b(ellos|nosotros|ustedes|tu|tú|el|él|ella|they|we|you|he|she)\b", re.I)


def tokenize(text: str) -> list[str]:
    return [match.group(0).lower() for match in WORD_RE.finditer(text)]


def sentences(text: str) -> list[str]:
    return [item.strip() for item in re.split(r"[.!?]+", text) if len(item.strip()) > 3]


def _bounded(value: float) -> float:
    return max(0.0, min(1.0, value))


def extract_dimensions(text: str) -> dict[str, float] | None:
    words = tokenize(text)
    if len(words) < 5:
        return None
    sent_count = max(len(sentences(text)), 1)
    unique = len(set(words))
    word_count = len(words)
    questions = text.count("?")
    avg_len = sum(len(word) for word in words) / word_count
    repetition = 1.0 - (unique / word_count)
    hedges = len(HEDGE_RE.findall(text))
    connectors = len(CONNECTOR_RE.findall(text))
    meta_words = len(META_RE.findall(text))
    self_ref = len(SELF_RE.findall(text))
    other_ref = len(OTHER_RE.findall(text))
    return {
        "curiosity": _bounded((questions / sent_count) * 2.5),
        "lex_div": _bounded(unique / word_count),
        "causality": _bounded((connectors / word_count) * 8.0),
        "humility": _bounded((hedges / word_count) * 15.0),
        "abstraction": _bounded((avg_len - 3.0) / 6.0),
        "meta": _bounded((meta_words / word_count) * 20.0),
        "coupling": _bounded(other_ref / (self_ref + other_ref + 0.1)),
        "coherence": _bounded(1.0 - repetition * 1.5),
    }


def phase_for_chi(chi: float) -> str:
    if chi < GRIFFITHS_LOW:
        return "ordered"
    if chi <= GRIFFITHS_HIGH:
        return "griffiths"
    return "chaotic"


def chi_vector(dimensions: dict[str, float]) -> dict[str, Any]:
    values = [float(dimensions[key]) for key, _label in DIMS]
    mean = sum(values) / len(values)
    entropy = -sum(value * math.log(value + 1e-9) for value in values if value > 0.0) / len(values)
    chi = 0.3 * mean + 0.4 * (entropy / math.log(len(values))) + 0.3 * (1.0 - sum(1 for value in values if value < 0.1) / len(values))
    chi = max(0.05, min(0.95, chi))
    return {"chi": round(chi, 6), "entropy": round(entropy, 6), "values": [round(value, 6) for value in values]}


def signature_hash(dimensions: dict[str, float]) -> str:
    digits = "".join(str(round(float(dimensions[key]) * 10)) for key, _label in DIMS)
    return "psi-" + digits[:8]


def analyze_behavior_signature(text: str, *, subject_id: str = "local_text") -> dict[str, Any]:
    dimensions = extract_dimensions(text)
    if dimensions is None:
        return {
            "schema": BEHAVIOR_SIGNATURE_SCHEMA,
            "subject_id": subject_id,
            "status": "insufficient_text",
            "minimum_words": 5,
        }
    chi = chi_vector(dimensions)
    phase = phase_for_chi(float(chi["chi"]))
    trust_color = "green" if phase == "griffiths" else "yellow"
    return {
        "schema": BEHAVIOR_SIGNATURE_SCHEMA,
        "subject_id": subject_id,
        "status": "evaluated",
        "dimensions": {key: round(float(dimensions[key]), 6) for key, _label in DIMS},
        "dimension_labels": {key: label for key, label in DIMS},
        "chi": chi["chi"],
        "entropy": chi["entropy"],
        "phase": phase,
        "signature_hash": signature_hash(dimensions),
        "trust_color": trust_color,
        "claim_boundary": "continuous drift/risk signal only; not a standalone identity proof",
    }
