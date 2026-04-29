# gemma-observacionismo-cleanup

MIT toolkit for observing and reducing response residue in model outputs. It is
packaged as developer tooling and documentation, not as Claudio runtime, model
routing, private prompts, weights or logs.

## Scope

- measure noisy text patterns in JSON samples;
- compare before/after cleanup payloads;
- generate stable fingerprints for regression fixtures;
- produce reproducible JSON reports for QA.

## Not Included

- model weights;
- private prompts;
- Claudio runtime state;
- sensitive logs;
- claims that this proves consciousness or scientific truth.

## Commands

```powershell
cd "C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\packages\open-dev\gemma-observacionismo-cleanup"
python -m gemma_observacionismo_cleanup.cli observe fixtures\sample.json
python -m gemma_observacionismo_cleanup.cli noise-report fixtures\before.json fixtures\after.json
python -m gemma_observacionismo_cleanup.cli fingerprint fixtures\sample.json
python -m pytest tests -q
```

Console scripts after installation:

```powershell
gemma-observe fixtures\sample.json
gemma-noise-report fixtures\before.json fixtures\after.json
gemma-fingerprint fixtures\sample.json
```

## Method Boundary

The scores are operational heuristics. They are useful for regression checks
and cleanup review, but they are not scientific proof. Calibrate thresholds
with explicit datasets before using them as release gates.
