# obsai-core

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
- generates stable session fingerprints;
- runs a deterministic world simulation smoke;
- exposes a CLI with JSON output.

## Claims Boundary

- This is an engineering control layer, not proof of consciousness.
- `Theta`, `J_c`, weights and thresholds are `DEMO_ONLY` until calibrated.
- World simulation output is a deterministic test fixture, not a physical model.
- Research claims must remain under `research-boundary` with falsifiers or `PREDICTION_REQUIRED`.

## Commands

```powershell
cd "C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\packages\open-dev\obsai-core"
python -m obsai_core.cli triage --signals circularity corrections unresolved_tasks
python -m obsai_core.cli evaluate-action examples\action_review.json
python -m obsai_core.cli fingerprint --session-id demo-001
python -m obsai_core.cli simulate-world --ticks 12 --seed demo
python -m unittest discover -s tests
```

`pytest` can run the same tests if available:

```powershell
python -m pytest tests -q
```
