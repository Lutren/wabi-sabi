"""Distilled DUAT v2 intake decisions for the local motor."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .contracts import DUAT_V2_INTAKE_SCHEMA
from .snapshot import canonical_sha256
from .source_registry import build_local_source_intake


DUAT_V2_SOURCE_FILENAMES = (
    "deep-research-report (4).md",
    "Esto es material extraordinariament.txt",
    "duat_v2.html",
    "deep-research-report (5).md",
)


def _select_sources(registry: dict[str, Any]) -> list[dict[str, Any]]:
    by_name = {Path(row["path"]).name: row for row in registry["sources"]}
    return [by_name[name] for name in DUAT_V2_SOURCE_FILENAMES if name in by_name]


def build_duat_v2_intake() -> dict[str, Any]:
    """Build the local decision artifact for the 2026-05-01 DUAT v2 files."""

    registry = build_local_source_intake()
    sources = _select_sources(registry)
    source_evidence = [
        {
            "filename": row["filename"],
            "path": row["path"],
            "exists": row["exists"],
            "sha256": row.get("sha256", "MISSING"),
            "lane": row["lane"],
            "copy_policy": row["copy_policy"],
        }
        for row in sources
    ]

    functional_candidates = [
        {
            "id": "ontology_operational_adequacy",
            "classification": "CERTEZA",
            "decision": "functional_now",
            "extract": "Separate last-truth claims from operational adequacy claims.",
            "destination": "claim boundary and scenario report language",
            "evidence_files": ["deep-research-report (4).md"],
        },
        {
            "id": "artifact_graph_edges",
            "classification": "CERTEZA",
            "decision": "functional_now",
            "extract": "Use explicit graph edges for supports, contradicts and verified_by evidence.",
            "destination": "artifact records and report evidence contracts",
            "evidence_files": ["deep-research-report (4).md"],
        },
        {
            "id": "phenomenon_observation_action_split",
            "classification": "CERTEZA",
            "decision": "functional_now",
            "extract": "Keep phenomenon, observation and action as separate layers.",
            "destination": "source snapshot, epoch model and scenario report flow",
            "evidence_files": ["deep-research-report (4).md"],
        },
        {
            "id": "seeded_epoch_simulation_shape",
            "classification": "INFERENCIA",
            "decision": "functional_now",
            "extract": "Distill epoch configs, social cells, Conway updates and phase thresholds into offline fixtures/tests.",
            "destination": "DUAT/Conway simulation and backtest fixtures",
            "evidence_files": ["Esto es material extraordinariament.txt", "duat_v2.html"],
        },
        {
            "id": "phase_vocabulary",
            "classification": "INFERENCIA",
            "decision": "functional_now",
            "extract": "Expose ordered, griffiths, disordered and chaotic as descriptive phases, not proof labels.",
            "destination": "DUAT health and simulation summaries",
            "evidence_files": ["duat_v2.html"],
        },
        {
            "id": "three_lane_duat_roadmap",
            "classification": "CERTEZA",
            "decision": "functional_now",
            "extract": "Separate DUAT into engineering/product, falsifiable metrics, and ontology research lanes.",
            "destination": "blocker policy and roadmap gating",
            "evidence_files": ["deep-research-report (5).md"],
        },
        {
            "id": "event_machine_architecture",
            "classification": "CERTEZA",
            "decision": "functional_now",
            "extract": "Represent observations, proposals, objections, verifications and human overrides as immutable events.",
            "destination": "event store and replay contract",
            "evidence_files": ["deep-research-report (5).md"],
        },
        {
            "id": "minimal_agent_society",
            "classification": "INFERENCIA",
            "decision": "functional_now",
            "extract": "Start with investigator, critic, verifier, memory, governance and optimizer roles before expanding.",
            "destination": "agent-roadmap contract",
            "evidence_files": ["deep-research-report (5).md"],
        },
        {
            "id": "continuous_identity_scoring",
            "classification": "INFERENCIA",
            "decision": "functional_now",
            "extract": "Use behavioral signature as a continuous drift/risk score, never as the root identity proof.",
            "destination": "behavior signature claim boundary",
            "evidence_files": ["deep-research-report (5).md"],
        },
    ]

    lab_candidates = [
        {
            "id": "visual_duat_v2_dashboard",
            "decision": "lab_private",
            "reason": "Useful as local visualization, but not engine evidence.",
            "evidence_files": ["duat_v2.html"],
        },
        {
            "id": "eeg_bridge",
            "decision": "lab_private",
            "reason": "Can remain as metaphor or future experiment until real data, consent, license and validation exist.",
            "evidence_files": ["Esto es material extraordinariament.txt", "duat_v2.html"],
        },
        {
            "id": "conformational_memory",
            "decision": "lab_private",
            "reason": "Keep as research metaphor until it maps to measurable state transitions.",
            "evidence_files": ["Esto es material extraordinariament.txt"],
        },
        {
            "id": "gemma_vllm_lora_world_model",
            "decision": "lab_private_blocked_by_host_gate",
            "reason": "Heavy model routes require host approval, latency evidence and QA before motor use.",
            "evidence_files": ["deep-research-report (4).md", "deep-research-report (5).md"],
        },
        {
            "id": "mesa_pettingzoo_simulators",
            "decision": "lab_private",
            "reason": "Promising for later ABM/RL experiments, but the MVP keeps the current deterministic simulation first.",
            "evidence_files": ["deep-research-report (5).md"],
        },
        {
            "id": "vector_memory_stack",
            "decision": "lab_private",
            "reason": "FAISS/Qdrant selection should wait until the event/artifact contracts prove useful.",
            "evidence_files": ["deep-research-report (5).md"],
        },
    ]

    blocked_claims = [
        {
            "id": "guaranteed_social_prediction",
            "decision": "blocked",
            "reason": "The motor may generate scenarios with uncertainty, not guaranteed predictions.",
        },
        {
            "id": "real_eeg_or_neuroscience_validation",
            "decision": "blocked",
            "reason": "No verified EEG dataset, consent chain, medical review or validation protocol is present.",
        },
        {
            "id": "external_publication",
            "decision": "blocked",
            "reason": "Publication remains behind ActionGate, clean packaging and secret scan.",
        },
        {
            "id": "private_canon_or_raw_download_copy",
            "decision": "blocked",
            "reason": "Raw Downloads and private canon stay outside public/open packages.",
        },
        {
            "id": "ontology_as_mvp_prerequisite",
            "decision": "blocked",
            "reason": "The ontology/microtubule lane may generate hypotheses, but it cannot gate the engineering MVP.",
        },
        {
            "id": "internal_model_surgery",
            "decision": "blocked",
            "reason": "Expert masking, early-exit, LoRA/adapters and weight work wait for observability and host approval.",
        },
    ]

    resolved_blockers = [
        {
            "id": "layer_mixing",
            "status": "resolved_local",
            "resolution": "DUAT is split into engineering/product, falsifiable metrics and ontology research lanes.",
            "evidence_files": ["deep-research-report (5).md"],
        },
        {
            "id": "raw_download_ingestion",
            "status": "resolved_local",
            "resolution": "Sources are hashed and registered with do_not_copy_raw policy.",
            "evidence_files": [row["filename"] for row in source_evidence],
        },
        {
            "id": "claim_confusion",
            "status": "resolved_local",
            "resolution": "Functional outputs are operational claims; prediction, EEG and ontology claims stay blocked.",
            "evidence_files": ["deep-research-report (4).md", "deep-research-report (5).md"],
        },
        {
            "id": "missing_core_contracts",
            "status": "resolved_local",
            "resolution": "Existing event store, artifact graph, router, behavior, health and simulation contracts remain the core.",
            "evidence_files": ["deep-research-report (5).md"],
        },
        {
            "id": "heavy_model_path",
            "status": "blocked_by_gate",
            "resolution": "Gemma/vLLM/Ray/LoRA remain laboratory-only until host gate, latency, memory and QA evidence pass.",
            "evidence_files": ["deep-research-report (5).md"],
        },
        {
            "id": "external_publication_path",
            "status": "blocked_by_gate",
            "resolution": "Publication remains blocked until ActionGate, clean package, legal posture and artifact secret scan pass.",
            "evidence_files": ["deep-research-report (5).md"],
        },
    ]

    artifact_graph_contract = {
        "edge_types": ["supports", "contradicts", "verified_by", "derived_from"],
        "required_node_fields": ["artifact_id", "kind", "status", "content_sha256"],
        "required_evidence_fields": ["filename", "sha256", "classification"],
        "claim_rule": "every scenario claim must cite evidence or remain INCOGNITA",
    }

    integration_decision = {
        "functional_now": [item["id"] for item in functional_candidates],
        "lab_private": [item["id"] for item in lab_candidates],
        "blocked": [item["id"] for item in blocked_claims],
        "resolved_local_blockers": [
            item["id"] for item in resolved_blockers if item["status"] == "resolved_local"
        ],
        "blocked_by_gate": [
            item["id"] for item in resolved_blockers if item["status"] == "blocked_by_gate"
        ],
        "raw_copy_policy": "do_not_copy_raw",
        "publication_gate": "BLOCK",
    }

    stable_body = {
        "sources": source_evidence,
        "functional_candidates": functional_candidates,
        "lab_candidates": lab_candidates,
        "blocked_claims": blocked_claims,
        "resolved_blockers": resolved_blockers,
        "artifact_graph_contract": artifact_graph_contract,
        "integration_decision": integration_decision,
    }
    return {
        "schema": DUAT_V2_INTAKE_SCHEMA,
        "source_count": len(sources),
        "sources": source_evidence,
        "functional_candidates": functional_candidates,
        "lab_candidates": lab_candidates,
        "blocked_claims": blocked_claims,
        "resolved_blockers": resolved_blockers,
        "artifact_graph_contract": artifact_graph_contract,
        "integration_decision": integration_decision,
        "decision_sha256": canonical_sha256(stable_body),
        "claim_boundary": (
            "DUAT v2 material is integrated as local contracts, tests and lab notes only; "
            "it is not a scientific validation, publication approval or prediction guarantee."
        ),
    }
