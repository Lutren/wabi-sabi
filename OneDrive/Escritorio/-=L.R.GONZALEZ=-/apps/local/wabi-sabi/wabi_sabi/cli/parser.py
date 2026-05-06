from __future__ import annotations

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
    scores = {
        "code_generation": _score(lowered, CODE_WORDS),
        "debug_diagnostics": _score(lowered, DEBUG_WORDS),
        "local_research": _score(lowered, RESEARCH_WORDS),
        "file_operations": _score(lowered, FILE_WORDS),
    }
    if "crea una funcion" in lowered or "crea una función" in lowered:
        scores["code_generation"] += 3
    if "ejecuta diagnostico" in lowered or "ejecuta diagnóstico" in lowered:
        scores["debug_diagnostics"] += 3
    if "crea un readme" in lowered:
        scores["file_operations"] += 3
    intent, score = max(scores.items(), key=lambda item: item[1])
    if score <= 0:
        return ParsedCommand(text=text, intent="general", confidence=0.2)
    total = sum(scores.values()) or score
    confidence = min(0.95, max(0.35, score / total))
    return ParsedCommand(text=text, intent=intent, confidence=confidence)


def _score(text: str, words: set[str]) -> int:
    return sum(1 for word in words if word in text)
