# obsai-core

Dependency-free evidence core for local-first AI agents.

Start here if you want the smallest public contract in the MEDIOEVO /
Observacionismo stack. Other repos can wrap it, visualize it, or package it,
but `obsai-core` is the canonical library for evidence envelopes, action gates,
residue scoring, and witnessable decisions.

`obsai-core` is the public-safe operational core extracted selectively from:

- `observacionismo_ai_os_fullstack.zip`
- `operational_ai_threshold.zip`

It does not copy either ZIP wholesale. Caches, Godot scripts, TypeScript files,
Codex task packets, lore/game files and research-only modules stay outside this
package.

## What It Does

- estimates residue `R` from operational signals;
- classifies regimes from `OPTIMO` through `JAMMING`;
- evaluates actions with an `APPROVE | REVIEW | BLOCK` gate;
- routes software signals through explicit capability receptors;
- ranks attention, evidence and RAG candidates with residue-aware controls;
- validates `ObservationEnvelope` records with PROV-O/SHACL-lite contracts;
- stores observation envelopes in SQLite for local audit trails;
- generates stable session fingerprints;
- runs a deterministic world simulation smoke;
- exposes a CLI with JSON output.

## One-Minute Demo

The demo never executes the requested action. It converts the action into a
review payload, evaluates it, and writes a witness log.

```powershell
python demo_agent_action.py --action "delete project folder"
```

Expected shape:

```json
{
  "decision": "BLOCK",
  "reason": "high_risk_low_reversibility",
  "evidence": [
    "no_sources",
    "consequential_action_without_tool_check",
    "high_risk_low_reversibility",
    "human_approval_required",
    "missing_authorized_receptor"
  ],
  "witness_log": "witness/..."
}
```

Read-only actions pass when they have evidence:

```powershell
python demo_agent_action.py --action "summarize README"
```

Expected shape:

```json
{
  "decision": "APPROVE",
  "reason": "sufficient_operational_threshold",
  "witness_log": "witness/..."
}
```

## Starter Benchmark

The benchmark is intentionally small and synthetic; it is a harness for public
comparison, not a production calibration claim.

```powershell
python benchmarks\run_agent_action_benchmark.py
```

It reports:

- `accuracy`
- `errors_prevented`
- `false_blocks`
- `correct_allows`
- `human_review_cost`

The next useful public contribution is a 100-500 scenario dataset comparing
agent actions with and without this gate.

## Where It Fits

- `obsai-core`: canonical primitives and tests.
- `safe-exec`: practical execution wrapper for tools and long-running agents.
- `agent-handoff-protocol`: workflow for session handoff and continuity.
- `residueos`: dashboard/API direction for review surfaces.
- `duat-genesis` and `duat-lab`: synthetic research labs and falsifier demos.

## Claims Boundary

- This is an engineering control layer, not proof of consciousness.
- `Theta`, `J_c`, weights and thresholds are `DEMO_ONLY` until calibrated.
- World simulation output is a deterministic test fixture, not a physical model.
- Research claims must remain under `research-boundary` with falsifiers or `PREDICTION_REQUIRED`.
- Patent-derived material is used only as an abstract software pattern and remains `LEGAL_REVIEW_REQUIRED`.

## Commands

```powershell
cd obsai-core
python -m obsai_core.cli triage --signals circularity corrections unresolved_tasks
python -m obsai_core.cli evaluate-action examples\action_review.json
python -m obsai_core.cli validate-envelope examples\observation_envelope.json --db runtime\observations.sqlite
python -m obsai_core.cli fingerprint --session-id demo-001
python -m obsai_core.cli simulate-world --ticks 12 --seed demo
python -m unittest discover -s tests
```

`pytest` can run the same tests if available:

```powershell
python -m pytest tests -q
```
