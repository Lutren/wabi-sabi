from __future__ import annotations

import hashlib
import json
import re
import zipfile
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable
from xml.etree import ElementTree


CEREBRO_LINE_AUDIT_SCHEMA = "wabi.cerebro_line_audit.v2"
CEREBRO_REL = Path("-=MEDIOEVO=-") / "-=LIBROS" / "-=CEREBRO=-"
DEFAULT_OUTPUT_REL = Path("runtime") / "cerebro_master_index"

TEXT_EXTENSIONS = {
    ".bat",
    ".cmd",
    ".conf",
    ".cjs",
    ".css",
    ".csv",
    ".html",
    ".ini",
    ".js",
    ".json",
    ".jsx",
    ".log",
    ".md",
    ".mjs",
    ".obs",
    ".ps1",
    ".py",
    ".rs",
    ".sample",
    ".sh",
    ".toml",
    ".ts",
    ".tsx",
    ".txt",
    ".svg",
    ".xml",
    ".yaml",
    ".yml",
}
DOCUMENT_TEXT_EXTENSIONS = {
    ".docx",
    ".pdf",
}
BINARY_EXTENSIONS = {
    ".7z",
    ".db",
    ".dll",
    ".doc",
    ".exe",
    ".gz",
    ".ico",
    ".jpeg",
    ".jpg",
    ".lnk",
    ".mp3",
    ".mp4",
    ".png",
    ".rar",
    ".sqlite",
    ".tar",
    ".webp",
    ".xls",
    ".xlsx",
    ".zip",
}
SKIP_DIRS = {
    ".git",
    ".hg",
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
    ".venv",
    "__pycache__",
    "build",
    "dist",
    "node_modules",
    "target",
}

SIGNAL_PATTERNS: list[tuple[str, re.Pattern[str]]] = [
    ("R", re.compile(r"(?<![A-Za-z0-9_])R(?![A-Za-z0-9_])|R\s*[<>=:]")),
    ("Phi_eff", re.compile(r"Phi_eff|\u03a6_eff|phi[_ -]?eff", re.IGNORECASE)),
    ("J_c", re.compile(r"J_c|jamming|jammed", re.IGNORECASE)),
    ("Sigma", re.compile(r"Sigma|\u03a3|sigma", re.IGNORECASE)),
    ("epsilon", re.compile(r"epsilon|\u03b5", re.IGNORECASE)),
    ("lambda", re.compile(r"lambda|\u03bb", re.IGNORECASE)),
    ("nu", re.compile(r"\bnu\b|\u03bd", re.IGNORECASE)),
    ("OSIT", re.compile(r"\bOSIT\b", re.IGNORECASE)),
    ("TUIP", re.compile(r"\bTUIP\b", re.IGNORECASE)),
    ("ActionGate", re.compile(r"ActionGate|action gate|compuerta", re.IGNORECASE)),
    ("WitnessLog", re.compile(r"WitnessLog|witness log|witness", re.IGNORECASE)),
    ("OSO", re.compile(r"\bOSO\b|observer state", re.IGNORECASE)),
    ("EML", re.compile(r"\bEML\b", re.IGNORECASE)),
    ("Conway", re.compile(r"Conway|game of life", re.IGNORECASE)),
    ("GhostGate", re.compile(r"GhostGate|ghost gate", re.IGNORECASE)),
    ("POVM", re.compile(r"\bPOVM\b", re.IGNORECASE)),
    ("NEC", re.compile(r"\bNEC\b|null energy", re.IGNORECASE)),
    ("Gauss-Bonnet", re.compile(r"Gauss[- ]Bonnet|Bonnet", re.IGNORECASE)),
    ("QNM", re.compile(r"\bQNM\b|quasinormal", re.IGNORECASE)),
    ("H_eff", re.compile(r"H_eff|effective hamiltonian", re.IGNORECASE)),
    ("anti-information", re.compile(r"anti[- ]informaci[oó]n|anti[- ]information", re.IGNORECASE)),
    ("dark information", re.compile(r"dark information|informaci[oó]n oscura", re.IGNORECASE)),
    ("DUAT", re.compile(r"\bDUAT\b", re.IGNORECASE)),
    ("GEODIA", re.compile(r"\bGEODIA\b", re.IGNORECASE)),
    ("Claudio", re.compile(r"\bClaudio\b", re.IGNORECASE)),
    ("Wabi-Sabi", re.compile(r"Wabi[-/ ]?Sabi|\bWabi\b", re.IGNORECASE)),
    ("browser", re.compile(r"browser|navegador|playwright|selenium", re.IGNORECASE)),
    ("agent_programming", re.compile(r"programador|programming|patch|codex|claude code|cursor|copilot", re.IGNORECASE)),
]

CODE_PATTERNS = [
    re.compile(r"^\s*class\s+\w+"),
    re.compile(r"^\s*def\s+\w+"),
    re.compile(r"^\s*async\s+def\s+\w+"),
    re.compile(r"^\s*function\s+\w+"),
    re.compile(r"^\s*(const|let|var)\s+\w+\s*="),
    re.compile(r"^\s*from\s+[\w.]+\s+import\s+"),
    re.compile(r"^\s*import\s+[\w.]+"),
    re.compile(r"^\s*@dataclass"),
    re.compile(r'"\$schema"\s*:'),
    re.compile(r"^\s*interface\s+\w+"),
    re.compile(r"^\s*type\s+\w+\s*="),
]


def build_cerebro_line_audit(
    workspace: str | Path,
    *,
    max_signal_records: int = 5000,
) -> dict[str, Any]:
    workspace_path = Path(workspace).resolve()
    cerebro_path = workspace_path / CEREBRO_REL
    generated_at = _utc_now()
    manifest_records: list[dict[str, Any]] = []
    line_signals: list[dict[str, Any]] = []
    signal_counter: Counter[str] = Counter()
    classification_counter: Counter[str] = Counter()
    total_lines = 0
    signal_line_count = 0
    code_block_count = 0
    code_candidate_count = 0
    skipped_count = 0

    if not cerebro_path.exists():
        return {
            "schema": CEREBRO_LINE_AUDIT_SCHEMA,
            "ok": False,
            "generated_at_utc": generated_at,
            "workspace": str(workspace_path),
            "cerebro_path": str(cerebro_path),
            "error": "cerebro_path_not_found",
            "summary": {},
            "manifest_records": [],
            "line_signals": [],
            "technology_atoms": [],
            "variant_records": [],
            "project_graph": _project_graph(workspace_path),
            "unknown_registry": _unknown_registry(),
            "action_gate_register": _action_gate_register(),
        }

    for path in _iter_cerebro_files(cerebro_path):
        rel = _rel(path, workspace_path)
        try:
            size = path.stat().st_size
        except OSError as exc:
            skipped_count += 1
            manifest_records.append(
                {
                    "path": rel,
                    "classification": "SKIPPED_ERROR",
                    "read_error": f"{type(exc).__name__}: {exc}",
                }
            )
            continue

        classification = _classify_path(path, size)
        file_record: dict[str, Any] = {
            "path": rel,
            "name": path.name,
            "suffix": path.suffix.lower(),
            "size_bytes": size,
            "sha256": _sha256(path),
            "classification": classification,
            "source_kind": "filesystem_text" if classification == "TEXT" else classification.lower(),
            "line_count": 0,
            "signal_count": 0,
            "code_candidate_count": 0,
            "code_fence_count": 0,
            "document_part_count": 0,
            "signals": {},
            "read_error": "",
        }
        if classification not in {"TEXT", "DOCUMENT_TEXT"}:
            classification_counter[classification] += 1
            manifest_records.append(file_record)
            continue

        file_signal_counter: Counter[str] = Counter()
        in_fence = False
        if classification == "DOCUMENT_TEXT":
            try:
                lines, document_meta = _read_document_lines(path)
            except Exception as exc:  # document parsers have varied exception types
                skipped_count += 1
                classification_counter["DOCUMENT_REVIEW"] += 1
                file_record["classification"] = "DOCUMENT_REVIEW"
                file_record["source_kind"] = "document_text_extraction_failed"
                file_record["read_error"] = f"{type(exc).__name__}: {exc}"
                manifest_records.append(file_record)
                continue
            file_record["source_kind"] = document_meta["source_kind"]
            file_record["document_part_count"] = document_meta["part_count"]
            classification_counter["DOCUMENT_TEXT"] += 1
        else:
            try:
                lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
            except OSError as exc:
                skipped_count += 1
                classification_counter["SKIPPED_ERROR"] += 1
                file_record["classification"] = "SKIPPED_ERROR"
                file_record["read_error"] = f"{type(exc).__name__}: {exc}"
                manifest_records.append(file_record)
                continue
            classification_counter["TEXT"] += 1

        for idx, line in enumerate(lines, start=1):
            stripped = line.strip()
            if stripped.startswith("```"):
                in_fence = not in_fence
                code_block_count += 1
                file_record["code_fence_count"] += 1
            signals = _line_signals(line)
            code_kind = _code_kind(line, in_fence)
            if code_kind:
                code_candidate_count += 1
                file_record["code_candidate_count"] += 1
            if signals:
                signal_line_count += 1
                file_record["signal_count"] += len(signals)
                file_signal_counter.update(signals)
                signal_counter.update(signals)
            if (signals or code_kind) and len(line_signals) < max_signal_records:
                line_signals.append(
                    {
                        "path": rel,
                        "line_no": idx,
                        "signals": signals,
                        "block_type": code_kind or "TEXT",
                        "excerpt": _excerpt(line),
                    }
                )
        file_record["line_count"] = len(lines)
        file_record["signals"] = dict(sorted(file_signal_counter.items()))
        total_lines += len(lines)
        manifest_records.append(file_record)

    variants = _build_variant_records(manifest_records)
    technology_atoms = _build_technology_atoms(signal_counter, line_signals, code_candidate_count)
    summary = {
        "file_count_total": len(manifest_records),
        "text_file_count": classification_counter.get("TEXT", 0),
        "document_text_file_count": classification_counter.get("DOCUMENT_TEXT", 0),
        "document_review_file_count": classification_counter.get("DOCUMENT_REVIEW", 0),
        "binary_file_count": classification_counter.get("BINARY_REVIEW", 0),
        "skipped_count": skipped_count + classification_counter.get("SKIP_REVIEW", 0),
        "total_lines": total_lines,
        "signal_line_count": signal_line_count,
        "signal_total": sum(signal_counter.values()),
        "code_block_marker_count": code_block_count,
        "code_candidate_count": code_candidate_count,
        "variant_group_count": len(variants),
        "signal_record_cap": max_signal_records,
        "signal_records_written_in_payload": len(line_signals),
        "by_classification": dict(sorted(classification_counter.items())),
        "top_signals": dict(signal_counter.most_common(20)),
    }
    return {
        "schema": CEREBRO_LINE_AUDIT_SCHEMA,
        "ok": True,
        "generated_at_utc": generated_at,
        "workspace": str(workspace_path),
        "cerebro_path": str(cerebro_path),
        "decision_context": {
            "no_operational_assumptions": True,
            "source_strategy": "INDICE_VIVO",
            "first_closure": "NUCLEO_LOCAL_FUNCIONAL",
            "browser": "COMPLETO_GATEADO",
            "agent_programming": "AUTONOMIA_AMPLIA_WITH_SAFE_EXECUTOR",
            "os_proof": "BOOT_COMPLETO_REQUIRES_CURRENT_EVIDENCE",
        },
        "summary": summary,
        "manifest_records": manifest_records,
        "line_signals": line_signals,
        "technology_atoms": technology_atoms,
        "variant_records": variants,
        "project_graph": _project_graph(workspace_path),
        "unknown_registry": _unknown_registry(),
        "action_gate_register": _action_gate_register(),
        "certainty": [
            "CEREBRO was scanned as files and text lines where decoding was possible.",
            "DOCX/PDF files are text-extracted when local parsers can read them; failed documents are indexed as REVIEW.",
            "Archives and unsupported binaries are indexed as REVIEW items, not silently treated as absorbed text.",
            "Variant groups are registered for review; different hashes are not merged automatically.",
        ],
        "inference": [
            "Repeated signals identify implementation candidates, but each candidate still needs a module contract and test.",
            "The safe unification layer is a live index plus project graph before any physical tree migration.",
        ],
        "unknown": [item["unknown"] for item in _unknown_registry()],
    }


def write_cerebro_audit_outputs(payload: dict[str, Any], output_root: str | Path | None = None) -> list[str]:
    workspace = Path(str(payload["workspace"])).resolve()
    output_dir = Path(output_root).resolve() if output_root else workspace / DEFAULT_OUTPUT_REL
    output_dir.mkdir(parents=True, exist_ok=True)

    artifacts: list[Path] = []
    manifest_path = output_dir / "LINE_AUDIT_MANIFEST.jsonl"
    signal_path = output_dir / "LINE_SIGNAL_INDEX.jsonl"
    technology_path = output_dir / "TECHNOLOGY_ATOMS.json"
    variants_path = output_dir / "VARIANT_DIFF_REGISTER.md"
    graph_json_path = output_dir / "MASTER_PROJECT_GRAPH.json"
    graph_md_path = output_dir / "MASTER_PROJECT_GRAPH.md"
    unknown_path = output_dir / "UNKNOWN_REGISTRY.md"
    gate_path = output_dir / "ACTION_GATE_REGISTER.md"
    status_path = output_dir / "FUNCTIONAL_STATUS.json"
    document_path = output_dir / "DOCUMENT_EXTRACTION_REGISTER.md"
    human_index_path = output_dir / "HUMAN_NAVIGATION_INDEX.md"
    report_path = output_dir / "CEREBRO_READ_COMPLETE_REPORT.md"

    manifest_path.write_text(
        "\n".join(json.dumps(item, ensure_ascii=False, sort_keys=True) for item in payload.get("manifest_records", [])) + "\n",
        encoding="utf-8",
    )
    signal_path.write_text(
        "\n".join(json.dumps(item, ensure_ascii=False, sort_keys=True) for item in payload.get("line_signals", [])) + "\n",
        encoding="utf-8",
    )
    technology_path.write_text(
        json.dumps(payload.get("technology_atoms", []), indent=2, ensure_ascii=False, sort_keys=True),
        encoding="utf-8",
    )
    variants_path.write_text(_variants_markdown(payload), encoding="utf-8")
    graph_json_path.write_text(
        json.dumps(payload.get("project_graph", {}), indent=2, ensure_ascii=False, sort_keys=True),
        encoding="utf-8",
    )
    graph_md_path.write_text(_graph_markdown(payload), encoding="utf-8")
    unknown_path.write_text(_unknown_markdown(payload), encoding="utf-8")
    gate_path.write_text(_gate_markdown(payload), encoding="utf-8")
    status_path.write_text(
        json.dumps(_functional_status(payload, output_dir), indent=2, ensure_ascii=False, sort_keys=True),
        encoding="utf-8",
    )
    document_path.write_text(_document_extraction_markdown(payload), encoding="utf-8")
    human_index_path.write_text(_human_navigation_markdown(payload, output_dir), encoding="utf-8")
    report_path.write_text(_read_complete_report(payload, output_dir), encoding="utf-8")

    artifacts.extend(
        [
            manifest_path,
            signal_path,
            technology_path,
            variants_path,
            graph_json_path,
            graph_md_path,
            unknown_path,
            gate_path,
            status_path,
            document_path,
            human_index_path,
            report_path,
        ]
    )
    payload["artifacts"] = [str(path) for path in artifacts]
    return payload["artifacts"]


def compact_cerebro_audit_payload(payload: dict[str, Any], *, max_files: int = 20, max_signals: int = 40) -> dict[str, Any]:
    compact = dict(payload)
    records = payload.get("manifest_records", [])
    signals = payload.get("line_signals", [])
    compact["manifest_sample"] = records[:max_files]
    compact["line_signal_sample"] = signals[:max_signals]
    compact.pop("manifest_records", None)
    compact.pop("line_signals", None)
    return compact


def _iter_cerebro_files(cerebro: Path) -> Iterable[Path]:
    for path in sorted(cerebro.rglob("*"), key=lambda item: str(item).lower()):
        if not path.is_file():
            continue
        rel_parts = path.relative_to(cerebro).parts
        if any(part in SKIP_DIRS for part in rel_parts[:-1]):
            continue
        yield path


def _classify_path(path: Path, size: int) -> str:
    suffix = path.suffix.lower()
    if suffix in DOCUMENT_TEXT_EXTENSIONS and size <= 25_000_000:
        return "DOCUMENT_TEXT"
    if suffix in BINARY_EXTENSIONS:
        return "BINARY_REVIEW"
    if suffix in TEXT_EXTENSIONS:
        return "TEXT"
    if not suffix and size <= 1_000_000:
        return "TEXT"
    if size > 5_000_000:
        return "SKIP_REVIEW"
    return "TEXT"


def _read_document_lines(path: Path) -> tuple[list[str], dict[str, Any]]:
    suffix = path.suffix.lower()
    if suffix == ".docx":
        return _read_docx_lines(path)
    if suffix == ".pdf":
        return _read_pdf_lines(path)
    raise ValueError(f"unsupported_document_extension:{suffix}")


def _read_docx_lines(path: Path) -> tuple[list[str], dict[str, Any]]:
    xml_names: list[str] = []
    lines: list[str] = []
    with zipfile.ZipFile(path) as archive:
        for name in sorted(archive.namelist()):
            if not name.startswith("word/") or not name.endswith(".xml"):
                continue
            base = Path(name).name
            if not (
                base == "document.xml"
                or base.startswith("header")
                or base.startswith("footer")
                or base in {"footnotes.xml", "endnotes.xml", "comments.xml"}
            ):
                continue
            xml_names.append(name)
            xml_text = archive.read(name)
            lines.extend(_docx_xml_lines(xml_text))
    return lines, {"source_kind": "docx_extracted_text", "part_count": len(xml_names)}


def _docx_xml_lines(xml_text: bytes) -> list[str]:
    root = ElementTree.fromstring(xml_text)
    namespace = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
    paragraph_tag = namespace + "p"
    text_tag = namespace + "t"
    tab_tag = namespace + "tab"
    break_tag = namespace + "br"
    lines: list[str] = []
    for paragraph in root.iter(paragraph_tag):
        chunks: list[str] = []
        for node in paragraph.iter():
            if node.tag == text_tag and node.text:
                chunks.append(node.text)
            elif node.tag == tab_tag:
                chunks.append("\t")
            elif node.tag == break_tag:
                chunks.append("\n")
        text = "".join(chunks)
        for line in text.splitlines() or [text]:
            stripped = line.strip()
            if stripped:
                lines.append(stripped)
    return lines


def _read_pdf_lines(path: Path) -> tuple[list[str], dict[str, Any]]:
    try:
        from pypdf import PdfReader
    except ImportError:
        from PyPDF2 import PdfReader  # type: ignore[no-redef]

    reader = PdfReader(str(path))
    lines: list[str] = []
    for index, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""
        for line in text.splitlines():
            stripped = line.strip()
            if stripped:
                lines.append(f"[page {index}] {stripped}")
    return lines, {"source_kind": "pdf_extracted_text", "part_count": len(reader.pages)}


def _line_signals(line: str) -> list[str]:
    return [name for name, pattern in SIGNAL_PATTERNS if pattern.search(line)]


def _code_kind(line: str, in_fence: bool) -> str:
    if in_fence:
        return "CODE_FENCE"
    for pattern in CODE_PATTERNS:
        if pattern.search(line):
            return "CODE_CANDIDATE"
    return ""


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    try:
        with path.open("rb") as handle:
            for chunk in iter(lambda: handle.read(1024 * 1024), b""):
                digest.update(chunk)
    except OSError:
        return ""
    return digest.hexdigest()


def _build_variant_records(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    variants: list[dict[str, Any]] = []
    by_hash: dict[str, list[dict[str, Any]]] = defaultdict(list)
    by_name: dict[str, list[dict[str, Any]]] = defaultdict(list)
    by_stem: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for record in records:
        sha = str(record.get("sha256") or "")
        if sha:
            by_hash[sha].append(record)
        name = str(record.get("name") or "").lower()
        stem = _normal_stem(Path(name).stem)
        by_name[name].append(record)
        by_stem[stem].append(record)

    seen: set[tuple[str, str]] = set()
    for sha, group in by_hash.items():
        if len(group) > 1:
            key = ("hash", sha)
            seen.add(key)
            variants.append(
                {
                    "variant_id": f"exact_sha256_{sha[:12]}",
                    "kind": "EXACT_DUPLICATE",
                    "keep_separate": False,
                    "merge_gate": "REVIEW_ARCHIVE_ONLY",
                    "files": [item["path"] for item in group],
                    "evidence": "same_sha256",
                }
            )
    for name, group in by_name.items():
        hashes = {str(item.get("sha256") or "") for item in group}
        if len(group) > 1 and len(hashes) > 1:
            variants.append(
                {
                    "variant_id": f"same_name_{_slug(name)}",
                    "kind": "SAME_NAME_DIFFERENT_HASH",
                    "keep_separate": True,
                    "merge_gate": "REVIEW_REQUIRED",
                    "files": [item["path"] for item in group],
                    "evidence": "same_filename_different_hash",
                }
            )
    for stem, group in by_stem.items():
        hashes = {str(item.get("sha256") or "") for item in group}
        if len(group) > 1 and len(hashes) > 1:
            files = [item["path"] for item in group]
            exact_key = ("stem", "|".join(files))
            if exact_key in seen:
                continue
            variants.append(
                {
                    "variant_id": f"same_stem_{_slug(stem)}",
                    "kind": "POSSIBLE_CONCEPT_VARIANT",
                    "keep_separate": True,
                    "merge_gate": "REVIEW_REQUIRED",
                    "files": files,
                    "evidence": "normalized_stem_match_different_hash",
                }
            )
    return variants


def _build_technology_atoms(
    signal_counter: Counter[str],
    line_signals: list[dict[str, Any]],
    code_candidate_count: int,
) -> list[dict[str, Any]]:
    atoms: list[dict[str, Any]] = []
    for signal, count in signal_counter.most_common():
        refs = [
            f"{item['path']}:{item['line_no']}"
            for item in line_signals
            if signal in item.get("signals", [])
        ][:5]
        atoms.append(
            {
                "atom_id": _slug(signal),
                "source_signal": signal,
                "count": count,
                "target": _target_for_signal(signal),
                "gate": _gate_for_signal(signal),
                "first_refs": refs,
                "module_contract_minimum": _module_contract_for_signal(signal),
                "test_minimum": _test_for_signal(signal),
            }
        )
    if code_candidate_count:
        atoms.append(
            {
                "atom_id": "code_candidates",
                "source_signal": "CODE_CANDIDATE",
                "count": code_candidate_count,
                "target": "WABI_SABI_REVIEW",
                "gate": "REVIEW_REQUIRED_BEFORE_IMPORT",
                "first_refs": [
                    f"{item['path']}:{item['line_no']}"
                    for item in line_signals
                    if item.get("block_type") in {"CODE_FENCE", "CODE_CANDIDATE"}
                ][:10],
                "module_contract_minimum": "extract purpose, inputs, outputs, dependencies, risks before implementation",
                "test_minimum": "static parse or isolated unit test before moving into runtime",
            }
        )
    return atoms


def _target_for_signal(signal: str) -> str:
    if signal in {"ActionGate", "WitnessLog", "EML", "OSO", "GhostGate", "Wabi-Sabi", "agent_programming"}:
        return "apps/local/wabi-sabi"
    if signal in {"DUAT", "GEODIA"}:
        return "DUAT_GEODIA_OS"
    if signal in {"OSIT", "TUIP", "Sigma", "POVM", "NEC", "Gauss-Bonnet", "QNM", "H_eff"}:
        return "CEREBRO_PSI_RESEARCH"
    if signal == "browser":
        return "BROWSER_GATE"
    if signal == "Claudio":
        return "CLAUDIO_RUNTIME"
    return "MEDIOEVO_OBSERVACIONISMO_MASTER"


def _gate_for_signal(signal: str) -> str:
    if signal in {"POVM", "NEC", "Gauss-Bonnet", "QNM", "H_eff", "Sigma", "OSIT", "TUIP"}:
        return "RESEARCH_REVIEW_REQUIRED"
    if signal in {"browser"}:
        return "COMPLETO_GATEADO"
    if signal in {"agent_programming"}:
        return "APPROVE_WITH_SAFE_EXECUTOR_AND_TESTS"
    return "APPROVE_LOCAL_DOC_OR_MODULE_SPEC"


def _module_contract_for_signal(signal: str) -> str:
    contracts = {
        "ActionGate": "evaluate action text or typed request -> APPROVE/REVIEW/BLOCK with reasons",
        "WitnessLog": "append event -> verify hash chain -> return evidence id",
        "EML": "measure context/load/jamming indicators -> regime recommendation",
        "browser": "evaluate URL/action -> gate and evidence requirements",
        "agent_programming": "convert task spec -> patch plan -> safe executor -> tests -> witness",
        "DUAT": "boot/build/test report -> OS status and missing host toolchain evidence",
        "GEODIA": "city/runtime module -> local proof artifact -> no public claim without gate",
    }
    return contracts.get(signal, "extract definition -> inputs -> outputs -> evidence -> falsifier or unit test")


def _test_for_signal(signal: str) -> str:
    tests = {
        "ActionGate": "table-driven APPROVE/REVIEW/BLOCK cases",
        "WitnessLog": "append two events and verify chain",
        "browser": "local URL approve, external read approve, login/publish review/block",
        "agent_programming": "patch plan against temp workspace plus rollback/test evidence",
        "DUAT": "kernel/ISO/QEMU command exits 0 or reports missing toolchain explicitly",
        "GEODIA": "current route/surface/OS artifact exists and is referenced by status",
    }
    return tests.get(signal, "minimum parser/classifier test with fixture source lines")


def _project_graph(workspace: Path) -> dict[str, Any]:
    return {
        "schema": "wabi.master_project_graph.v1",
        "workspace": str(workspace),
        "nodes": [
            {"id": "CEREBRO", "kind": "source_canon", "path": str(workspace / CEREBRO_REL)},
            {"id": "MEDIOEVO_OBSERVACIONISMO_MASTER", "kind": "compiled_canon", "path": str(workspace / "MEDIOEVO_OBSERVACIONISMO_MASTER")},
            {"id": "WABI_SABI", "kind": "local_agent_runtime", "path": str(workspace / "apps" / "local" / "wabi-sabi")},
            {"id": "OBSAI_CORE", "kind": "open_dev_toolkit", "path": str(workspace / "packages" / "open-dev" / "obsai-core")},
            {"id": "CLAUDIO_RUNTIME", "kind": "local_runtime", "path": str(workspace / "-=MEDIOEVO=-" / "-=LIBROS" / "claudio")},
            {"id": "DUAT_GEODIA_OS", "kind": "os_kernel_city_system", "path": str(workspace / "-=MEDIOEVO=-" / "-=LIBROS" / "claudio" / "os" / "duat_geodia_kernel")},
            {"id": "PRODUCTOS_MEDIOEVO", "kind": "product_lane", "path": str(workspace / "PRODUCTOS_MEDIOEVO")},
            {"id": "BROWSER_GATE", "kind": "capability_gate", "path": str(workspace / "apps" / "local" / "wabi-sabi" / "wabi_sabi" / "core" / "browser_gate.py")},
            {"id": "UNKNOWN_REGISTRY", "kind": "review_queue", "path": str(workspace / DEFAULT_OUTPUT_REL / "UNKNOWN_REGISTRY.md")},
        ],
        "edges": [
            {"from": "CEREBRO", "to": "MEDIOEVO_OBSERVACIONISMO_MASTER", "relation": "curated_into"},
            {"from": "CEREBRO", "to": "WABI_SABI", "relation": "runtime_requirements"},
            {"from": "WABI_SABI", "to": "OBSAI_CORE", "relation": "implements_or_mirrors_core_patterns"},
            {"from": "WABI_SABI", "to": "BROWSER_GATE", "relation": "gates_browser_capability"},
            {"from": "CLAUDIO_RUNTIME", "to": "DUAT_GEODIA_OS", "relation": "contains_os_lane"},
            {"from": "MEDIOEVO_OBSERVACIONISMO_MASTER", "to": "PRODUCTOS_MEDIOEVO", "relation": "eligible_after_review"},
            {"from": "CEREBRO", "to": "UNKNOWN_REGISTRY", "relation": "unresolved_evidence_queue"},
        ],
        "graph_gate": "APPROVE_LOCAL_INDEX",
    }


def _unknown_registry() -> list[dict[str, str]]:
    return [
        {
            "unknown": "Archives and failed/unsupported document files are indexed but not fully line-extracted by this pass.",
            "gate": "REVIEW_EXTRACTION_REQUIRED",
            "next_evidence": "extract archive contents in a quarantined review lane and attach provenance, hash and line/page references",
        },
        {
            "unknown": "Similar concepts with different hashes may contain small variables that change meaning.",
            "gate": "REVIEW_REQUIRED",
            "next_evidence": "compare variant excerpts before merging",
        },
        {
            "unknown": "Physical claims remain research hypotheses until formalism, numeric simulation, or falsifier exists.",
            "gate": "RESEARCH_REVIEW_REQUIRED",
            "next_evidence": "claim contract plus falsifier output",
        },
        {
            "unknown": "DUAT/GEODIA boot completeness requires current host toolchain and command evidence.",
            "gate": "BOOT_EVIDENCE_REQUIRED",
            "next_evidence": "brain_os_cli/kernel/ISO/QEMU report from this session",
        },
    ]


def _action_gate_register() -> list[dict[str, str]]:
    return [
        {"action": "CEREBRO_LINE_AUDIT", "gate": "APPROVE", "rule": "read-only source scan plus runtime artifacts"},
        {"action": "WRITE_MASTER_INDEX", "gate": "APPROVE", "rule": "writes only under runtime/cerebro_master_index"},
        {"action": "MERGE_VARIANTS", "gate": "REVIEW", "rule": "different hashes are not merged automatically"},
        {"action": "MOVE_SOURCE_TREE", "gate": "REVIEW", "rule": "physical reorganization requires migration log and backup"},
        {"action": "BROWSER_LOCAL_OR_READONLY", "gate": "APPROVE_LOGGED", "rule": "no login, no form submit, no publication"},
        {"action": "BROWSER_AUTH_PUBLISH_OR_PAYMENT", "gate": "REVIEW_OR_BLOCK", "rule": "requires explicit target-specific gate"},
        {"action": "AGENT_WRITE_CODE", "gate": "APPROVE_WITH_SAFE_EXECUTOR", "rule": "patch plan, rollback, py_compile/tests, witness"},
        {"action": "PUBLIC_STRONG_PHYSICS_CLAIM", "gate": "BLOCK_UNTIL_NUMERIC", "rule": "needs formalism and falsifier"},
    ]


def _functional_status(payload: dict[str, Any], output_dir: Path) -> dict[str, Any]:
    summary = payload.get("summary", {})
    return {
        "schema": "wabi.cerebro_functional_status.v1",
        "generated_at_utc": payload.get("generated_at_utc"),
        "workspace": payload.get("workspace"),
        "status": "PARTIAL_LOCAL_FUNCTIONAL" if payload.get("ok") else "BLOCKED",
        "evidence": {
            "line_audit_manifest": str(output_dir / "LINE_AUDIT_MANIFEST.jsonl"),
            "line_signal_index": str(output_dir / "LINE_SIGNAL_INDEX.jsonl"),
            "technology_atoms": str(output_dir / "TECHNOLOGY_ATOMS.json"),
            "project_graph": str(output_dir / "MASTER_PROJECT_GRAPH.json"),
        },
        "counts": {
            "files": summary.get("file_count_total", 0),
            "text_files": summary.get("text_file_count", 0),
            "document_text_files": summary.get("document_text_file_count", 0),
            "document_review_files": summary.get("document_review_file_count", 0),
            "lines": summary.get("total_lines", 0),
            "signal_lines": summary.get("signal_line_count", 0),
            "technology_atoms": len(payload.get("technology_atoms", [])),
            "variant_groups": summary.get("variant_group_count", 0),
        },
        "not_claimed": [
            "No physical source tree migration was performed.",
            "No public publication/deploy/push was performed.",
            "No ZIP/archive or unsupported binary was treated as fully absorbed text by this pass.",
            "No DUAT/GEODIA boot success is claimed by the audit alone.",
        ],
    }


def _variants_markdown(payload: dict[str, Any]) -> str:
    lines = [
        "# Variant Diff Register",
        "",
        "CERTEZA:",
        "- This register is generated from paths, filenames and hashes.",
        "",
        "ACCION:",
        "- Exact hash duplicates may be archived only after review.",
        "- Different hashes stay separate until a human/agent compares the semantic delta.",
        "",
        "| Variant | Kind | Gate | Keep separate | Files |",
        "|---|---|---|---|---|",
    ]
    for variant in payload.get("variant_records", []):
        files = "<br>".join(f"`{item}`" for item in variant.get("files", []))
        lines.append(
            f"| `{variant['variant_id']}` | {variant['kind']} | {variant['merge_gate']} | {variant['keep_separate']} | {files} |"
        )
    if not payload.get("variant_records"):
        lines.append("| none | none | APPROVE | false | none |")
    return "\n".join(lines) + "\n"


def _graph_markdown(payload: dict[str, Any]) -> str:
    graph = payload.get("project_graph", {})
    lines = [
        "# Master Project Graph",
        "",
        "CERTEZA:",
        "- The graph is an index; it does not move folders.",
        "",
        "## Nodes",
    ]
    for node in graph.get("nodes", []):
        lines.append(f"- `{node['id']}` ({node['kind']}): `{node['path']}`")
    lines.append("")
    lines.append("## Edges")
    for edge in graph.get("edges", []):
        lines.append(f"- `{edge['from']}` -> `{edge['to']}`: {edge['relation']}")
    return "\n".join(lines) + "\n"


def _unknown_markdown(payload: dict[str, Any]) -> str:
    lines = [
        "# Unknown Registry",
        "",
        "CERTEZA:",
        "- These items are not resolved by the audit.",
        "",
        "| Unknown | Gate | Next evidence |",
        "|---|---|---|",
    ]
    for item in payload.get("unknown_registry", []):
        lines.append(f"| {item['unknown']} | {item['gate']} | {item['next_evidence']} |")
    return "\n".join(lines) + "\n"


def _gate_markdown(payload: dict[str, Any]) -> str:
    lines = [
        "# Action Gate Register",
        "",
        "| Action | Gate | Rule |",
        "|---|---|---|",
    ]
    for item in payload.get("action_gate_register", []):
        lines.append(f"| {item['action']} | {item['gate']} | {item['rule']} |")
    return "\n".join(lines) + "\n"


def _document_extraction_markdown(payload: dict[str, Any]) -> str:
    records = payload.get("manifest_records", [])
    document_records = [item for item in records if str(item.get("classification", "")).startswith("DOCUMENT")]
    binary_records = [item for item in records if item.get("classification") in {"BINARY_REVIEW", "SKIP_REVIEW"}]
    lines = [
        "# Document Extraction Register",
        "",
        "CERTEZA:",
        "- DOCX/PDF files listed as `DOCUMENT_TEXT` were parsed locally into derived text lines for signal indexing.",
        "- `BINARY_REVIEW` and `SKIP_REVIEW` entries were not unpacked or treated as absorbed text.",
        "",
        "INFERENCIA:",
        "- Extracted text is enough for semantic and signal indexing, but not for layout, figures, equations rendered as images or visual QA.",
        "",
        "INCOGNITA:",
        "- ZIP/archive contents need a separate quarantined extraction pass before import or cleanup decisions.",
        "",
        "## DOCX/PDF",
        "",
        "| Path | Classification | Source | Lines | Parts/pages | Signals | Error |",
        "|---|---|---|---:|---:|---:|---|",
    ]
    if not document_records:
        lines.append("| none | none | none | 0 | 0 | 0 | none |")
    for item in document_records:
        signals = sum(int(value) for value in dict(item.get("signals", {})).values())
        lines.append(
            "| "
            f"`{item.get('path')}` | {item.get('classification')} | {item.get('source_kind')} | "
            f"{item.get('line_count', 0)} | {item.get('document_part_count', 0)} | {signals} | "
            f"{item.get('read_error') or ''} |"
        )
    lines.extend(
        [
            "",
            "## Unsupported / Archive Review",
            "",
            "| Path | Classification | Size bytes | SHA256 |",
            "|---|---|---:|---|",
        ]
    )
    if not binary_records:
        lines.append("| none | none | 0 | none |")
    for item in binary_records:
        lines.append(
            f"| `{item.get('path')}` | {item.get('classification')} | {item.get('size_bytes', 0)} | `{item.get('sha256', '')}` |"
        )
    return "\n".join(lines) + "\n"


def _human_navigation_markdown(payload: dict[str, Any], output_dir: Path) -> str:
    summary = payload.get("summary", {})
    top = summary.get("top_signals", {})
    top_lines = "\n".join(f"- `{name}`: {count}" for name, count in top.items()) or "- none"
    return f"""# Human Navigation Index

CERTEZA:
- CEREBRO was indexed without moving, deleting or rewriting source files.
- Text files and DOCX/PDF extracted text now feed the same line-signal index.
- The master index for agents is `{output_dir}`.

INFERENCIA:
- Use `MEDIOEVO_OBSERVACIONISMO_MASTER` for human reading and this runtime index for traceability.
- High-count signals indicate where implementation work should start, not where claims are already scientifically validated.

INCOGNITA:
- Archives and unsupported binaries require a separate extraction pass.
- Similar files with different hashes remain variants until compared semantically.

ACCION:
1. Read `MEDIOEVO_OBSERVACIONISMO_MASTER/00_README_MASTER.md` for the curated human overview.
2. Use `DOCUMENT_EXTRACTION_REGISTER.md` to see which DOCX/PDF files were absorbed as text.
3. Use `TECHNOLOGY_ATOMS.json` to turn repeated ideas into modules/tests.
4. Use `VARIANT_DIFF_REGISTER.md` before merging apparently similar files.
5. Keep source movement, publication and strong physics claims behind ActionGate.

ARTEFACTO:
- `LINE_AUDIT_MANIFEST.jsonl`
- `LINE_SIGNAL_INDEX.jsonl`
- `DOCUMENT_EXTRACTION_REGISTER.md`
- `TECHNOLOGY_ATOMS.json`
- `VARIANT_DIFF_REGISTER.md`
- `MASTER_PROJECT_GRAPH.md`

COUNTS:
- Files indexed: `{summary.get('file_count_total', 0)}`
- Filesystem text files: `{summary.get('text_file_count', 0)}`
- DOCX/PDF extracted: `{summary.get('document_text_file_count', 0)}`
- DOCX/PDF review: `{summary.get('document_review_file_count', 0)}`
- Lines indexed: `{summary.get('total_lines', 0)}`
- Signal lines: `{summary.get('signal_line_count', 0)}`
- Code candidates: `{summary.get('code_candidate_count', 0)}`
- Variants: `{summary.get('variant_group_count', 0)}`

TOP_SIGNALS:
{top_lines}
"""


def _read_complete_report(payload: dict[str, Any], output_dir: Path) -> str:
    summary = payload.get("summary", {})
    artifacts = [
        "LINE_AUDIT_MANIFEST.jsonl",
        "LINE_SIGNAL_INDEX.jsonl",
        "TECHNOLOGY_ATOMS.json",
        "VARIANT_DIFF_REGISTER.md",
        "MASTER_PROJECT_GRAPH.json",
        "MASTER_PROJECT_GRAPH.md",
        "UNKNOWN_REGISTRY.md",
        "ACTION_GATE_REGISTER.md",
        "FUNCTIONAL_STATUS.json",
    ]
    top = "\n".join(f"- {name}: {count}" for name, count in summary.get("top_signals", {}).items())
    return f"""# CEREBRO Read Complete Report

CERTEZA:
- Workspace: `{payload.get('workspace')}`
- CEREBRO path: `{payload.get('cerebro_path')}`
- Files indexed: `{summary.get('file_count_total', 0)}`
- Text files read line by line: `{summary.get('text_file_count', 0)}`
- DOCX/PDF files extracted as text: `{summary.get('document_text_file_count', 0)}`
- DOCX/PDF files needing review: `{summary.get('document_review_file_count', 0)}`
- Total text lines scanned: `{summary.get('total_lines', 0)}`
- Signal lines detected: `{summary.get('signal_line_count', 0)}`
- Code candidates detected: `{summary.get('code_candidate_count', 0)}`
- Variant groups registered: `{summary.get('variant_group_count', 0)}`

INFERENCIA:
- Signals and code candidates are implementation candidates, not proof of implementation.
- The correct unification shape for this pass is a live index and graph before source migration.

INCOGNITA:
- ZIP/archive and unsupported binary files need dedicated extraction before being marked absorbed.
- DOCX/PDF extraction is text-only and does not claim visual layout review.
- DUAT/GEODIA boot completeness needs separate command evidence.

ACCION:
- Use `TECHNOLOGY_ATOMS.json` to convert repeated ideas into module contracts/tests.
- Use `VARIANT_DIFF_REGISTER.md` before merging similar files.
- Use `ACTION_GATE_REGISTER.md` for browser, agent-write, publication and physics-claim boundaries.

ARTEFACTO:
- Output directory: `{output_dir}`
{chr(10).join(f"- `{item}`" for item in artifacts)}

TOP_SIGNALS:
{top or "- none"}
"""


def _normal_stem(stem: str) -> str:
    lowered = stem.lower()
    lowered = re.sub(r"\b(copy|copia|final|nuevo|new|version|v\d+)\b", "", lowered)
    lowered = re.sub(r"[\W_]+", "", lowered)
    return lowered or stem.lower()


def _slug(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", value.lower()).strip("_") or "item"


def _excerpt(line: str, limit: int = 260) -> str:
    stripped = line.strip()
    if len(stripped) <= limit:
        return stripped
    return stripped[: limit - 3] + "..."


def _rel(path: Path, base: Path) -> str:
    try:
        return str(path.resolve().relative_to(base))
    except ValueError:
        return str(path.resolve())


def _utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()
