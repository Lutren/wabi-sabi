# Model Efficiency Lane

Research around pruning, lottery-ticket style subnetworks and quantization is
useful to Brain OS, but it is not accepted as a universal rule. Smaller can be
better only after task-specific measurement.

## Rule

No model variant replaces a baseline until it passes:

- Baseline evidence.
- Task accuracy.
- Latency.
- Memory.
- Energy.
- Safety.
- Regression tests.
- Human approval for replacement.

## PC2 Default

PC2 should prefer small local models:

- Quantized GGUF models first.
- Small coding and routing models before large APIs.
- Remote paid APIs only through Guardian approval.
- DeepSeek V4 remains API-only for now; local weights are not assumed.

## Evidence Contract

The first measurement helper is:

```text
../model_slimmer_evidence.py
```

It produces an evaluation plan with quantization and pruning candidates,
including a `prune_90` variant. That does not mean `prune_90` is accepted. It
means it is measurable.

Acceptance defaults:

```text
accuracy_drop <= 0.02
safety_drop <= 0.01
latency must not increase
memory must not increase
energy must not increase
regression suite required
replacement requires approval
```

## Observacionista Reading

The useful lesson is not "remove 90 percent and trust it." The useful lesson is:

```text
capacity can be hidden in smaller structures, but every claim must survive
measurement in the real task and real machine.
```

