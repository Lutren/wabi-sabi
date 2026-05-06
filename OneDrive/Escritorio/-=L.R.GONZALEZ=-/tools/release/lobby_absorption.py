from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import sys
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_LOBBY = Path.home() / "OneDrive" / "Escritorio" / "Lobby de Alejandria"
TODAY = datetime.now().date().isoformat()

TEXT_SUFFIXES = {".txt", ".md", ".json", ".csv", ".py", ".js", ".ts", ".html", ".css", ".yml", ".yaml"}
README_NAMES = {"readme_lobby_de_alejandria.md"}


@dataclass
class LobbyRecord:
    original_path: str
    archived_path: str | None
    filename: str
    sha256: str
    size_bytes: int
    line_count: int
    character_count: int
    lane: str
    psi_state: str
    action_gate: str
    status: str
    decision: str
    target_artifacts: list[str]
    evidence_markers: list[str]
    extracted_patterns: list[str]
    falsifiers: list[str]
    risk_flags: list[str] = field(default_factory=list)


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest().upper()


def slugify(value: str, limit: int = 96) -> str:
    text = value.encode("ascii", "ignore").decode("ascii").lower()
    text = re.sub(r"[^a-z0-9._-]+", "-", text).strip("-._")
    return (text or "source")[:limit]


def iter_lobby_files(root: Path) -> Iterable[Path]:
    for path in sorted(root.iterdir(), key=lambda p: p.name.lower()):
        if path.is_file() and path.suffix.lower() in TEXT_SUFFIXES:
            yield path


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def classify(path: Path, text: str) -> tuple[str, str, str, str, list[str], list[str]]:
    haystack = f"{path.name}\n{text}".lower()
    name_lower = path.name.lower()
    target_artifacts: list[str] = []
    risk_flags: set[str] = set()

    if any(marker in haystack for marker in ["rpg", "tcg", "private", "privado"]):
        risk_flags.add("private_boundary")
    if any(marker in haystack for marker in ["publica", "publish", "linkedin", "gumroad", "github sponsor"]):
        risk_flags.add("publication_boundary")
    if any(marker in haystack for marker in ["fine-tune", "finetune", "lora", "alias ollama", "descarga modelo"]):
        risk_flags.add("model_mutation_boundary")
    if any(marker in haystack for marker in ["diagnostico medico", "prediccion social", "nueva fisica probada"]):
        risk_flags.add("strong_claim_boundary")
    if any(marker in haystack for marker in ["antigravedad", "raychaudhuri", "gauss-bonnet", "gw170817"]):
        risk_flags.add("strong_physics_claim_boundary")

    if any(marker in name_lower for marker in ["rpg", "tcg", "medioevo-rpg", "medioevo rpg"]):
        lane = "Privado RPG/TCG"
        target_artifacts = ["docs/canon/atlas/privado-bloqueado.md", "game-private"]
    elif "prompt maestro" in name_lower or "orquestador" in name_lower:
        lane = "Prompt Master/Orquestador"
        target_artifacts = ["docs/ops/PROMPT_MASTER_EXECUTION_CONTROLLER_2026-05-06.md", "runtime/prompt_master"]
    elif "ai browser" in name_lower or "browser seguro" in name_lower:
        lane = "AI Browser Security"
        target_artifacts = ["docs/ai_browser", "tools/ai_browser"]
    elif "mission control" in name_lower or "comms" in name_lower or "hormiguero" in name_lower:
        lane = "Mission Control/COMMS"
        target_artifacts = ["docs/ops/MISSION_CONTROL_COMMS_STATE_2026-05-06.md", "COMMS/topics/agent-city-coordination.jsonl"]
    elif "release" in name_lower or "public-s" in name_lower or "perfil" in name_lower:
        lane = "Publicacion/Release"
        target_artifacts = ["docs/publication", "PRODUCT_MAP.md", "VISIBILITY_MATRIX.md"]
    elif "programador segur" in name_lower or "seguridad" in name_lower:
        lane = "Seguridad/Programador Local"
        target_artifacts = ["apps/local/wabi-sabi", "docs/canon/atlas/seguridad.md", "tools/security_geolocation_guard.py"]
    elif "duat read-only" in haystack or "readonly adapter" in haystack or "duat read-only" in name_lower:
        lane = "DUAT read-only adapter"
        target_artifacts = ["docs/duat", "claudio/adapters/duat_readonly_adapter.py", "tests/test_duat_readonly_adapter.py"]
    elif "duat" in name_lower or "geodia" in name_lower:
        lane = "DUAT/GEODIA private research"
        target_artifacts = ["docs/duat", "research/geodia-social-observatory", "docs/canon/atlas/privado-bloqueado.md"]
    elif "canon observacion" in name_lower or "observacionismo" in name_lower:
        lane = "PSI/Observacionismo"
        target_artifacts = ["docs/canon/atlas/psi-observacionismo.md", "schemas/observacionismo_concepts.schema.json"]
    elif "lenguaje observac" in name_lower or "lenguaje" in name_lower:
        lane = "Lenguaje Observacionista"
        target_artifacts = ["docs/canon/atlas/psi-observacionismo.md", "docs/matrix", "library/modules/observacionismo_core.json"]
    elif "matrix" in name_lower or "bibliotec" in name_lower or "alejandria" in name_lower:
        lane = "Matrix/Biblioteca"
        target_artifacts = ["docs/matrix", "library/index.json", "library/modules"]
    elif "osit" in haystack or "qg" in haystack or "wabi" in haystack or "qwen" in haystack or "bridge propio" in haystack:
        if "strong_physics_claim_boundary" in risk_flags:
            lane = "OSIT-QG research boundary"
            target_artifacts = ["docs/canon/atlas/psi-observacionismo.md", "docs/ops/OSIT_RESOURCE_OPTIMIZER_RUNTIME_SPEC_2026-05-06.md"]
        else:
            lane = "Wabi-Sabi/OSIT"
            target_artifacts = ["docs/ops/WABI_OSIT_BRIDGE_FROM_ESTADO_2026-05-06.md", "apps/local/wabi-sabi"]
    elif "duat" in haystack or "geodia" in haystack:
        lane = "DUAT/GEODIA private research"
        target_artifacts = ["docs/duat", "research/geodia-social-observatory", "docs/canon/atlas/privado-bloqueado.md"]
    else:
        lane = "Curaduria SETO"
        target_artifacts = ["docs/intake", "runtime/curador_seto"]

    if "strong_claim_boundary" in risk_flags or "strong_physics_claim_boundary" in risk_flags:
        psi_state = "BLOQUEADO"
        action_gate = "BLOCK"
    elif risk_flags:
        psi_state = "INFERENCIA"
        action_gate = "REVIEW"
    else:
        psi_state = "INFERENCIA"
        action_gate = "REVIEW"

    if path.name.lower() in README_NAMES:
        decision = "KEEP_LOBBY_OPERATING_README"
        status = "CANONICO_EN_LOBBY"
    elif action_gate == "BLOCK":
        decision = "ABSORB_METADATA_AND_ARCHIVE_BLOCKED_SOURCE"
        status = "BLOQUEADO_ARCHIVO_FRIO"
    else:
        decision = "ABSORB_TO_ATLAS_AND_ARCHIVE_SOURCE"
        status = "ABSORBIDO_ARCHIVO_FRIO"

    return lane, psi_state, action_gate, status, target_artifacts, sorted(risk_flags)


def extract_patterns(text: str, limit: int = 10) -> list[str]:
    lines = [line.strip() for line in text.splitlines()]
    candidates: list[str] = []
    markers = (
        "#",
        "MISION",
        "MISIÓN",
        "REGLA",
        "TAREAS",
        "VALIDACION",
        "VALIDACIÓN",
        "INTERFAZ",
        "ARCHIVOS",
        "RESTRICCIONES",
        "Wabi-Sabi",
        "ActionGate",
        "WitnessLog",
        "ObservationEnvelope",
        "RuntimeAdapter",
        "ResidueMeter",
        "Falsadores",
    )
    for line in lines:
        if not line:
            continue
        if len(line) > 260:
            line = line[:257] + "..."
        if line.startswith(markers) or any(marker.lower() in line.lower() for marker in markers[9:]):
            candidates.append(line)
        if len(candidates) >= limit:
            break
    return candidates


def evidence_markers_for(path: Path, text: str) -> list[str]:
    markers = []
    lowered = text.lower()
    for term in [
        "actiongate",
        "witnesslog",
        "observationenvelope",
        "wabi-sabi",
        "duat",
        "geodia",
        "matrix",
        "biblioteca",
        "ai browser",
        "mission control",
        "public-safe",
        "rpg",
        "osit",
        "qwen",
        "falsadores",
    ]:
        if term in lowered or term in path.name.lower():
            markers.append(term)
    return markers


def build_records(lobby_root: Path) -> list[LobbyRecord]:
    records: list[LobbyRecord] = []
    for path in iter_lobby_files(lobby_root):
        text = read_text(path)
        lane, psi_state, action_gate, status, target_artifacts, risk_flags = classify(path, text)
        line_count = len(text.splitlines())
        record = LobbyRecord(
            original_path=str(path),
            archived_path=None,
            filename=path.name,
            sha256=sha256_file(path),
            size_bytes=path.stat().st_size,
            line_count=line_count,
            character_count=len(text),
            lane=lane,
            psi_state=psi_state,
            action_gate=action_gate,
            status=status,
            decision="KEEP_LOBBY_OPERATING_README" if path.name.lower() in README_NAMES else "ABSORB_TO_ATLAS_AND_ARCHIVE_SOURCE",
            target_artifacts=target_artifacts,
            evidence_markers=evidence_markers_for(path, text),
            extracted_patterns=extract_patterns(text),
            falsifiers=[
                "sha256_mismatch",
                "target_artifact_missing",
                "private_boundary_leaks_to_public",
                "source_left_in_lobby_after_archive",
            ],
            risk_flags=risk_flags,
        )
        if action_gate == "BLOCK":
            record.decision = "ABSORB_METADATA_AND_ARCHIVE_BLOCKED_SOURCE"
        records.append(record)
    return records


def archive_records(records: list[LobbyRecord], archive_root: Path) -> None:
    archive_root.mkdir(parents=True, exist_ok=True)
    used_names: set[str] = set()
    for record in records:
        source = Path(record.original_path)
        if record.decision == "KEEP_LOBBY_OPERATING_README":
            continue
        safe_name = f"{record.sha256[:16]}_{slugify(source.name)}"
        while safe_name in used_names or (archive_root / safe_name).exists():
            safe_name = f"{record.sha256[:16]}_{len(used_names):02d}_{slugify(source.name)}"
        used_names.add(safe_name)
        destination = archive_root / safe_name
        shutil.move(str(source), str(destination))
        if sha256_file(destination) != record.sha256:
            raise RuntimeError(f"archive_hash_mismatch: {source} -> {destination}")
        record.archived_path = str(destination)


def write_outputs(records: list[LobbyRecord], output_prefix: Path) -> dict[str, str]:
    output_prefix.parent.mkdir(parents=True, exist_ok=True)
    manifest_path = output_prefix.with_name(output_prefix.name + "_MANIFEST.json")
    report_path = output_prefix.with_name(output_prefix.name + "_REPORT.md")
    retirements_path = output_prefix.with_name(output_prefix.name + "_RETIREMENTS.md")

    payload = {
        "schema": "medioevo.lobby_alejandria.absorption.v1",
        "generated_at_utc": utc_now(),
        "records": [asdict(record) for record in records],
        "summary": summarize(records),
    }
    manifest_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    report_path.write_text(render_report(payload), encoding="utf-8")
    retirements_path.write_text(render_retirements(records), encoding="utf-8")
    return {
        "manifest": str(manifest_path),
        "report": str(report_path),
        "retirements": str(retirements_path),
    }


def summarize(records: list[LobbyRecord]) -> dict[str, object]:
    archived = sum(1 for record in records if record.archived_path)
    kept = sum(1 for record in records if record.decision == "KEEP_LOBBY_OPERATING_README")
    total_lines = sum(record.line_count for record in records)
    lanes: dict[str, int] = {}
    gates: dict[str, int] = {}
    for record in records:
        lanes[record.lane] = lanes.get(record.lane, 0) + 1
        gates[record.action_gate] = gates.get(record.action_gate, 0) + 1
    return {
        "files": len(records),
        "archived": archived,
        "kept_in_lobby": kept,
        "total_lines_read": total_lines,
        "lanes": lanes,
        "gates": gates,
    }


def render_report(payload: dict[str, object]) -> str:
    summary = payload["summary"]
    records = [LobbyRecord(**record) for record in payload["records"]]  # type: ignore[arg-type]
    lines = [
        "# Lobby de Alejandria Full Absorption",
        "",
        f"Generated UTC: `{payload['generated_at_utc']}`",
        "",
        "## Summary",
        "",
        f"- Files read: `{summary['files']}`",
        f"- Total lines read: `{summary['total_lines_read']}`",
        f"- Archived to Archivo Frio: `{summary['archived']}`",
        f"- Kept in Lobby: `{summary['kept_in_lobby']}`",
        "",
        "## Lane Counts",
        "",
        "| lane | files |",
        "|---|---:|",
    ]
    for lane, count in sorted(summary["lanes"].items()):  # type: ignore[index,union-attr]
        lines.append(f"| `{lane}` | {count} |")
    lines.extend(["", "## Records", "", "| file | lane | gate | status | sha256 | lines | target |", "|---|---|---|---|---|---:|---|"])
    for record in records:
        targets = "<br>".join(f"`{target}`" for target in record.target_artifacts) or "`n/a`"
        lines.append(
            f"| `{record.filename}` | `{record.lane}` | `{record.action_gate}` | `{record.status}` | "
            f"`{record.sha256[:16]}` | {record.line_count} | {targets} |"
        )
    lines.extend(["", "## Extracted Patterns", ""])
    for record in records:
        lines.append(f"### {record.filename}")
        lines.append("")
        lines.append(f"- Original: `{record.original_path}`")
        if record.archived_path:
            lines.append(f"- Archivo Frio: `{record.archived_path}`")
        lines.append(f"- Decision: `{record.decision}`")
        lines.append(f"- Evidence markers: `{', '.join(record.evidence_markers) or 'none'}`")
        lines.append("- Patterns:")
        if record.extracted_patterns:
            lines.extend(f"  - {pattern}" for pattern in record.extracted_patterns)
        else:
            lines.append("  - no structural markers detected")
        lines.append("")
    return "\n".join(lines) + "\n"


def render_retirements(records: list[LobbyRecord]) -> str:
    lines = [
        "# Lobby de Alejandria Retirements",
        "",
        "Unique sources were absorbed into a manifest/report and moved to Archivo Frio. Nothing was deleted.",
        "",
        "| status | original path | sha256 | archive/canonical path | reason |",
        "|---|---|---|---|---|",
    ]
    for record in records:
        if not record.archived_path:
            continue
        lines.append(
            f"| `{record.status}` | `{record.original_path}` | `{record.sha256}` | "
            f"`{record.archived_path}` | `{record.decision}` |"
        )
    return "\n".join(lines) + "\n"


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Absorb Lobby de Alejandria text sources into Curador SETO artifacts.")
    parser.add_argument("--root", default=str(DEFAULT_LOBBY), help="Lobby path to scan.")
    parser.add_argument("--name", default=f"lobby_alejandria_full_absorption_{TODAY}", help="Output artifact prefix.")
    parser.add_argument("--archive-absorbed", action="store_true", help="Move absorbed sources to Archivo Frio.")
    parser.add_argument("--json", action="store_true", help="Print JSON summary.")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    args = parse_args(argv)
    lobby_root = Path(args.root).resolve()
    records = build_records(lobby_root)
    if args.archive_absorbed:
        archive_records(records, ROOT / "runtime" / "curador_seto" / "source_archive" / "lobby_alejandria" / TODAY)
    paths = write_outputs(records, ROOT / "docs" / "intake" / args.name)
    summary = {"paths": paths, "summary": summarize(records)}
    if args.json:
        print(json.dumps(summary, indent=2, ensure_ascii=False))
    else:
        print(f"report: {paths['report']}")
        print(f"manifest: {paths['manifest']}")
        print(f"retirements: {paths['retirements']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
