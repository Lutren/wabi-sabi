---
name: modelo-router
description: Local model-router skill for Claudio/local model gating, Gemma/Open WebUI/Ollama route evaluation, latency truth checks, residue thresholds, and daemon launch prevention until preflight says ready_to_launch=true.
---

# Modelo Router

Installed is not usable. Compiled is not daemon-ready. Route models through evidence and gate heavy launches.

## Reads

- Local model evaluation docs, `PORTFOLIO_EXECUTION_LEDGER.md`, `CLAIMS_BOUNDARY.md`, and model-router or Observacionismo threshold artifacts.
- `packages/obsai-core`, `apps/residueos`, or `packages/open-dev/observacionismo-gate` only as selected references.
- `tools/harness/candidate_routes.json` before considering Open WebUI, n8n, or Dagger.

## May Touch

- Local routing manifests, benchmark reports, threshold configs, and harness docs.
- Do not start heavy model daemons, download models, use credentials, or launch Open WebUI/n8n/Dagger routes without gate.
- No usar git add .; stage only model-router-owned reports/configs.

## Required Evidence

- Real local latency/response test against a small baseline before routing claims.
- Action decision from local gate (`APPROVE`, `REVIEW`, or `BLOCK`) for any route with cost, daemon, or credential risk.
- Preflight artifact must include `ready_to_launch=true` before any preview/daemon launch.

## ActionGate Blocks

Always require ActionGate plus `host_observacionista` for model downloads, daemon start, `-AcknowledgePreviewRisk`, Open WebUI launch, n8n activation, Dagger engine/container execution, external APIs, credentials, or expensive inference.
Block if host state is `JAMMING` or `BLOCK`, or if preflight lacks `ready_to_launch=true`.
