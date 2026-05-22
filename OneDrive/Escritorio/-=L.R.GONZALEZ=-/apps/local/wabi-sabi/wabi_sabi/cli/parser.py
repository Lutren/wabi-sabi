from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass, field


@dataclass(frozen=True)
class ParsedCommand:
    text: str
    intent: str
    confidence: float
    entities: dict[str, str] = field(default_factory=dict)


CODE_WORDS = {
    "codigo",
    "code",
    "programa",
    "programar",
    "funcion",
    "función",
    "function",
    "clase",
    "script",
    "refactor",
}

DEBUG_WORDS = {
    "diagnostico",
    "diagnóstico",
    "debug",
    "depura",
    "depurar",
    "falla",
    "fallan",
    "tests",
    "pytest",
    "arregla",
    "repara",
    "optimiza",
}

RESEARCH_WORDS = {
    "investiga",
    "investigar",
    "busca",
    "buscar",
    "documentacion",
    "documentación",
    "repo",
    "proyecto",
    "analiza",
}

FILE_WORDS = {
    "readme",
    "archivo",
    "file",
    "lee",
    "leer",
    "resume",
    "resuma",
    "documenta",
    "crea un readme",
}


def parse_command(text: str) -> ParsedCommand:
    lowered = text.lower()
    normalized = _normalize(lowered)
    scores = {
        "code_generation": _score(normalized, CODE_WORDS),
        "debug_diagnostics": _score(normalized, DEBUG_WORDS),
        "local_research": _score(normalized, RESEARCH_WORDS),
        "file_operations": _score(normalized, FILE_WORDS),
    }
    if "crea una funcion" in normalized:
        scores["code_generation"] += 3
    if "ejecuta diagnostico" in normalized:
        scores["debug_diagnostics"] += 3
    if "crea un readme" in normalized:
        scores["file_operations"] += 3
    intent, score = max(scores.items(), key=lambda item: item[1])
    if score <= 0:
        return ParsedCommand(text=text, intent="general", confidence=0.2)
    total = sum(scores.values()) or score
    confidence = min(0.95, max(0.35, score / total))
    return ParsedCommand(text=text, intent=intent, confidence=confidence)


def _score(text: str, words: set[str]) -> int:
    return sum(1 for word in words if _contains_term(text, word))


def _normalize(text: str) -> str:
    decomposed = unicodedata.normalize("NFD", text)
    return "".join(ch for ch in decomposed if unicodedata.category(ch) != "Mn")


def _contains_term(text: str, term: str) -> bool:
    normalized_term = _normalize(term.lower())
    if " " in normalized_term:
        return normalized_term in text
    return re.search(rf"(?<!\w){re.escape(normalized_term)}(?!\w)", text) is not None
