from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any


TEXT_KEYS = {"text", "response", "answer", "output", "content", "message"}
PLACEHOLDER_RE = re.compile(r"\b(todo|tbd|fixme|placeholder|lorem ipsum)\b", re.IGNORECASE)
REPEATED_PUNCT_RE = re.compile(r"([!?.,;:])\1{2,}")
EXCESS_WHITESPACE_RE = re.compile(r"[ \t]{3,}|\n{4,}")
BOILERPLATE_RE = re.compile(
    r"\b(as an ai|as a language model|i cannot browse|i do not have access)\b",
    re.IGNORECASE,
)


@dataclass(frozen=True)
class TextMetrics:
    char_count: int
    word_count: int
    line_count: int
    placeholder_hits: int
    repeated_punctuation_hits: int
    whitespace_hits: int
    boilerplate_hits: int
    residue_score: float

    def to_dict(self) -> dict[str, int | float]:
        return {
            "char_count": self.char_count,
            "word_count": self.word_count,
            "line_count": self.line_count,
            "placeholder_hits": self.placeholder_hits,
            "repeated_punctuation_hits": self.repeated_punctuation_hits,
            "whitespace_hits": self.whitespace_hits,
            "boilerplate_hits": self.boilerplate_hits,
            "residue_score": self.residue_score,
        }


def load_json(path: str | Path) -> Any:
    with Path(path).open("r", encoding="utf-8") as fh:
        return json.load(fh)


def canonical_json(payload: Any) -> str:
    return json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def fingerprint_payload(payload: Any) -> dict[str, Any]:
    canonical = canonical_json(payload)
    return {
        "fingerprint": hashlib.sha256(canonical.encode("utf-8")).hexdigest(),
        "bytes": len(canonical.encode("utf-8")),
        "items": count_items(payload),
    }


def count_items(payload: Any) -> int:
    if isinstance(payload, dict):
        return 1 + sum(count_items(value) for value in payload.values())
    if isinstance(payload, list):
        return 1 + sum(count_items(value) for value in payload)
    return 1


def extract_text(payload: Any) -> list[str]:
    texts: list[str] = []
    if isinstance(payload, str):
        return [payload]
    if isinstance(payload, list):
        for item in payload:
            texts.extend(extract_text(item))
        return texts
    if isinstance(payload, dict):
        for key, value in payload.items():
            if key.lower() in TEXT_KEYS and isinstance(value, str):
                texts.append(value)
            elif isinstance(value, (dict, list)):
                texts.extend(extract_text(value))
        return texts
    return texts


def measure_text(text: str) -> TextMetrics:
    char_count = len(text)
    words = re.findall(r"\b[\w'-]+\b", text, flags=re.UNICODE)
    word_count = len(words)
    line_count = text.count("\n") + 1 if text else 0
    placeholder_hits = len(PLACEHOLDER_RE.findall(text))
    repeated_punctuation_hits = len(REPEATED_PUNCT_RE.findall(text))
    whitespace_hits = len(EXCESS_WHITESPACE_RE.findall(text))
    boilerplate_hits = len(BOILERPLATE_RE.findall(text))
    raw_score = (
        placeholder_hits * 0.35
        + repeated_punctuation_hits * 0.16
        + whitespace_hits * 0.14
        + boilerplate_hits * 0.35
    )
    residue_score = min(1.0, round(raw_score / max(1.0, word_count / 120), 4))
    return TextMetrics(
        char_count=char_count,
        word_count=word_count,
        line_count=line_count,
        placeholder_hits=placeholder_hits,
        repeated_punctuation_hits=repeated_punctuation_hits,
        whitespace_hits=whitespace_hits,
        boilerplate_hits=boilerplate_hits,
        residue_score=residue_score,
    )


def observe_payload(payload: Any) -> dict[str, Any]:
    texts = extract_text(payload)
    joined = "\n".join(texts)
    metrics = measure_text(joined)
    fingerprint = fingerprint_payload(payload)
    return {
        "ok": True,
        "text_fields": len(texts),
        "metrics": metrics.to_dict(),
        "fingerprint": fingerprint["fingerprint"],
        "items": fingerprint["items"],
        "limits": {
            "method": "heuristic_cleanup_observation",
            "claims": "engineering_signal_only",
        },
    }


def noise_report(before: Any, after: Any) -> dict[str, Any]:
    before_report = observe_payload(before)
    after_report = observe_payload(after)
    before_metrics = before_report["metrics"]
    after_metrics = after_report["metrics"]
    delta = {
        key: round(float(after_metrics[key]) - float(before_metrics[key]), 4)
        for key in before_metrics
    }
    return {
        "ok": True,
        "before": before_report,
        "after": after_report,
        "delta": delta,
        "improved": after_metrics["residue_score"] <= before_metrics["residue_score"],
    }
