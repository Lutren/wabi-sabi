from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


ALLOWLIST_RELATIVE = (
    Path("00_START_HERE") / "LIVE_STATE" / "REPORT_STATUS_PROJECTS_PENDING.md",
    Path("00_START_HERE") / "LIVE_STATE" / "HANDOFF_CURRENT.md",
    Path("00_START_HERE") / "LIVE_STATE" / "NEXT_SESSION_BRIEF.md",
    Path("00_START_HERE") / "LIVE_STATE" / "PENDIENTES_MASTER.md",
    Path("README_START_HERE_HUMANO.md"),
)

BLOCKED_PARTS = {
    ".env",
    "tokens",
    "credentials",
    "source_zips",
    "99_source_vault",
    "books",
    "libros",
    "rpg",
    "tcg",
    "duat_private",
    "wabi-sabi internals public copy",
    "claudio private runtime public copy",
}


@dataclass(frozen=True)
class LiveContextResult:
    ok: bool
    output: str
    files_used: list[str]
    blocked: list[str]


def load_live_context(brain_os: str | Path, *, max_chars_per_file: int = 3500) -> LiveContextResult:
    root = Path(brain_os).resolve()
    files_used: list[str] = []
    blocked: list[str] = []
    sections: list[str] = []
    for rel in ALLOWLIST_RELATIVE:
        path = (root / rel).resolve()
        if _blocked(path):
            blocked.append(str(path))
            continue
        if not path.exists() or path.suffix.lower() != ".md":
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        excerpt = _tail_excerpt(text, max_chars_per_file)
        files_used.append(str(path))
        sections.append(f"## {rel.as_posix()}\n{excerpt}")
    if not sections:
        return LiveContextResult(False, "No encontre live-state allowlist legible.", files_used, blocked)
    output = _summarize_context("\n\n".join(sections), files_used)
    return LiveContextResult(True, output, files_used, blocked)


def _blocked(path: Path) -> bool:
    parts = {part.lower() for part in path.parts}
    joined = str(path).lower()
    return bool(parts.intersection(BLOCKED_PARTS)) or any(marker in joined for marker in BLOCKED_PARTS)


def _tail_excerpt(text: str, limit: int) -> str:
    clean = text.replace("\x00", "")
    if len(clean) <= limit:
        return clean
    return clean[-limit:]


def _summarize_context(text: str, files_used: list[str]) -> str:
    lower = text.lower()
    blockers: list[str] = []
    if "publication_gate: block" in lower or "publicacion" in lower or "publicación" in lower:
        blockers.append("publicacion/push/deploy siguen bloqueados")
    if "zip replacement" in lower or "zip replacement: block" in lower:
        blockers.append("ZIP replacement sigue bloqueado")
    if "secret" in lower or "secreto" in lower:
        blockers.append("secretos siguen bajo presence-only")
    if "wabi" in lower:
        status = "Wabi-Sabi conversacional local esta activo o fue actualizado recientemente."
    else:
        status = "BRAIN_OS live-state cargado desde allowlist."
    next_action = _find_next_action(text)
    if not next_action:
        next_action = "Siguiente accion segura: trabajo local reversible con ActionGate y WitnessLog."
    lines = [
        "Estado actual:",
        f"- {status}",
        "- Fuente: live-state allowlist, sin source vaults ni privados.",
        "",
        "Bloqueos:",
    ]
    lines.extend(f"- {item}" for item in (blockers or ["publicacion externa, secretos y acciones destructivas requieren gate"]))
    lines.extend(["", "Siguiente accion:", f"- {next_action}", "", "Archivos usados:"])
    lines.extend(f"- {path}" for path in files_used)
    return "\n".join(lines)


def _find_next_action(text: str) -> str:
    lines = [line.strip("- ").strip() for line in text.splitlines() if line.strip()]
    for line in reversed(lines):
        lower = line.lower()
        if lower.startswith("next:") or lower.startswith("next action") or lower.startswith("proxima accion") or lower.startswith("próxima acción"):
            return line
    for line in reversed(lines):
        if "siguiente accion" in line.lower() or "siguiente acción" in line.lower():
            return line
    return ""
