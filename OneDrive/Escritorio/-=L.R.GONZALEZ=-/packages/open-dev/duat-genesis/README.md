# DUAT Genesis

DUAT Genesis is a public, dependency-free synthetic sandbox for observable
simulation experiments.

It is not DUAT Geodia. DUAT Geodia remains a private MEDIOEVO research/runtime
lane. This package exposes only generic simulation contracts, synthetic state
updates, falsifier scaffolds and reports that can be modified for safe research
experiments.

## What It Does

- creates deterministic synthetic worlds from a seed;
- applies generic observation and rule pressure to bounded numeric state;
- emits reproducible `SimulationRun` reports;
- runs basic falsifiers for determinism, bounded values and claim safety;
- provides a small CLI for `run`, `report` and `falsify`.

## What It Does Not Do

- it does not predict real social, biological, neurological or physical systems;
- it does not include private DUAT Geodia engineering;
- it does not include MEDIOEVO RPG/TCG assets, lore, scenes or game runtime;
- it does not provide medical, scientific or safety guarantees.

## CLI

```powershell
python -m duat_genesis.cli run --seed demo --size 8 --ticks 5
python -m duat_genesis.cli report --seed demo --ticks 5
python -m duat_genesis.cli falsify --seed demo --ticks 5
```

## Public Claim

Allowed: "synthetic sandbox for observable simulation and falsifier examples."

Do not claim validated science, real-world prediction, diagnosis, private DUAT
Geodia engineering, or RPG living-world runtime.
