"""Local source intake registry for the user's Downloads files."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .contracts import LOCAL_SOURCE_INTAKE_SCHEMA
from .snapshot import file_sha256


DOWNLOADS = Path.home() / "Downloads"


@dataclass(frozen=True)
class LocalSourceSpec:
    filename: str
    lane: str
    functional_extracts: tuple[str, ...]
    lab_extracts: tuple[str, ...]
    blocked_or_deferred: tuple[str, ...]

    @property
    def path(self) -> Path:
        return DOWNLOADS / self.filename


LOCAL_SOURCES: tuple[LocalSourceSpec, ...] = (
    LocalSourceSpec(
        "deep-research-report (2).md",
        "FUNCTIONAL_AND_LAB",
        ("event store", "artifact graph", "router", "HITL", "metrics", "API sketch"),
        ("vLLM/Gemma serving", "cluster deployment", "ontology lab roadmap"),
        ("external citations are not imported as proof",),
    ),
    LocalSourceSpec(
        "observ.md",
        "FUNCTIONAL_AND_LAB",
        ("DUAT metrics", "router cache/small/strong/sim/human", "artifact lineage", "governance"),
        ("world model planner", "simulator suite", "model serving stack"),
        ("full model tuning",),
    ),
    LocalSourceSpec(
        "firma_conductual_observacionismo.html",
        "FUNCTIONAL",
        ("8-dimension behavioral signature", "chi phase", "signature hash", "drift risk"),
        ("radar UI",),
        ("standalone identity proof",),
    ),
    LocalSourceSpec(
        "duat_observacionismo_conway.html",
        "FUNCTIONAL",
        ("deterministic DUAT/Conway grid", "phase percentages", "seeded simulation"),
        ("interactive canvas UI",),
        ("social prediction claims",),
    ),
    LocalSourceSpec(
        "iceberg_code.py",
        "LAB_WITH_FUNCTIONAL_EXTRACTS",
        ("observer event metaphor", "artifact creation", "calibration network"),
        ("conversational universes", "education/game metaphors", "ontology experiments"),
        ("scientific cosmology claims",),
    ),
    LocalSourceSpec(
        "El Observacionismo no es solo una f.md",
        "LAB_WITH_FUNCTIONAL_EXTRACTS",
        ("DUAT/Conway rules", "jamming thresholds", "uncertainty separation"),
        ("paper drafts", "public positioning", "large conceptual synthesis"),
        ("prediction/validation claims",),
    ),
    LocalSourceSpec(
        "observacionismo_tech_stack_2026.html",
        "LAB",
        ("technique inventory for future evaluation",),
        ("ADEPT", "CLaSp", "AdaDecode", "MoR", "SWIFT", "MTP"),
        ("runtime model surgery", "weight edits", "unverified Gemma modifications"),
    ),
    LocalSourceSpec(
        "Sí, Luis René. Los Modelos de Mundo.txt",
        "LAB_WITH_FUNCTIONAL_EXTRACTS",
        ("world-model planner pattern", "Action Gate pattern", "route escalation"),
        ("Gemma LoRA/fine-tuning", "JEPA/DyMo experiments", "Dockerized model stack"),
        ("heavy model route until host gate approves",),
    ),
    LocalSourceSpec(
        "Luis René, tienes razón en tu intui.txt",
        "LAB",
        ("router signal ideas", "noise cleanup heuristics"),
        ("MoE expert reorganization", "training workshop", "pruning"),
        ("touching weights/adapters before evidence",),
    ),
    LocalSourceSpec(
        "Estimado Luis René,.txt",
        "EDITORIAL_CANON_WITH_EXTRACTS",
        ("session/artifact/calibration concepts",),
        ("observational cosmology narrative", "Gemma prompt simulations", "canon language"),
        ("direct code import without distillation",),
    ),
    LocalSourceSpec(
        "deep-research-report (4).md",
        "FUNCTIONAL_AND_LAB",
        (
            "ontology adequacy boundary",
            "phenomenon/observation/action separation",
            "artifact graph edge contract",
            "policy gateway",
        ),
        ("ontology lab roadmap", "private canon architecture", "multi-agent colony framing"),
        ("external publication", "private canon exposure", "heavy model serving"),
    ),
    LocalSourceSpec(
        "Esto es material extraordinariament.txt",
        "LAB_WITH_FUNCTIONAL_EXTRACTS",
        (
            "epoch configuration fixture ideas",
            "seeded Conway social cells",
            "phase thresholds",
            "CLI shape for offline simulation",
        ),
        ("EEG bridge", "conformational memory", "future predictor", "world map visualization"),
        ("guaranteed prediction claims", "real EEG anchoring", "scientific validation claims"),
    ),
    LocalSourceSpec(
        "duat_v2.html",
        "LAB_WITH_FUNCTIONAL_EXTRACTS",
        ("phase vocabulary", "canvas dashboard signals", "Chi/Phi readouts"),
        ("fractal UI", "EEG canvas", "microtubule/fractal metaphor surface"),
        ("public scientific product claim", "browser UI as core evidence"),
    ),
    LocalSourceSpec(
        "deep-research-report (5).md",
        "FUNCTIONAL_AND_LAB",
        (
            "three-lane DUAT roadmap",
            "event machine architecture",
            "minimal agent role set",
            "continuous identity scoring boundary",
            "blocker sequencing",
        ),
        (
            "Mesa/PettingZoo experiments",
            "FAISS/Qdrant vector memory evaluation",
            "Gemma/vLLM/Ray Serve stack review",
            "ontology and microtubule research lane",
        ),
        (
            "treating ontology as product prerequisite",
            "heavy model serving before host gate",
            "LoRA/adapters before evidence",
        ),
    ),
)


def build_source_record(spec: LocalSourceSpec) -> dict[str, Any]:
    path = spec.path
    record: dict[str, Any] = {
        "path": str(path),
        "filename": spec.filename,
        "exists": path.exists(),
        "lane": spec.lane,
        "functional_extracts": list(spec.functional_extracts),
        "lab_extracts": list(spec.lab_extracts),
        "blocked_or_deferred": list(spec.blocked_or_deferred),
        "copy_policy": "do_not_copy_raw; distill into contracts/tests/docs only",
    }
    if path.exists() and path.is_file():
        stat = path.stat()
        record["bytes"] = stat.st_size
        record["last_write_time_utc"] = datetime.fromtimestamp(stat.st_mtime, timezone.utc).isoformat()
        record["sha256"] = file_sha256(path)
    return record


def build_local_source_intake() -> dict[str, Any]:
    records = [build_source_record(spec) for spec in LOCAL_SOURCES]
    return {
        "schema": LOCAL_SOURCE_INTAKE_SCHEMA,
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "source_count": len(records),
        "missing_count": sum(1 for row in records if not row["exists"]),
        "sources": records,
        "boundary": {
            "functional_destination": "research/geodia-social-observatory",
            "lab_destination": "local private laboratory notes only",
            "publication_gate": "BLOCK",
            "heavy_model_gate": "BLOCK",
        },
    }
