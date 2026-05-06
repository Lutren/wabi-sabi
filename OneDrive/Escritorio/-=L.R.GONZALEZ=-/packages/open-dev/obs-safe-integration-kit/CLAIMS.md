# Claims Boundary

Status: package-level boundary for `obs-safe-integration-kit`.

## Allowed Claims

- Provides local-first data structures for `ObservationEnvelope`, `EstadoPSI`, `ActionGate`, `EvidenceStore` and adapter wrappers.
- Runs in dry-run/human-review mode by default; the package does not execute shell, browser, network or production actions.
- Blocks obvious destructive commands and secret-shaped strings in proposed actions.
- Stores observations, claims, actions and sessions in SQLite with hash-chain fields.
- Helps agent projects reduce drift between intent, evidence and proposed action when integrated by a developer.

## Demo-Only Claims

- Any threshold, risk score, residue value, `R`, `Phi_eff`, `J_c` or epsilon value is `DEMO_ONLY` until calibrated on a real dataset.
- Wrapper examples are integration patterns, not audited production integrations.
- Synthetic fixtures prove expected code paths, not real-world safety performance.

## Blocked Claims

- No guaranteed safety.
- No autonomous public execution without human review.
- No proof of consciousness, new physics, cosmology, medical diagnosis or cognitive diagnosis.
- No guarantee that a downstream project is secure just because it imports this package.
- No access to private MEDIOEVO runtime, RPG, TCG, books, assets, prompts, accounts or local sessions.

## Publication Rule

Public copy may describe this as an operational safety/evidence kernel for AI-agent workflows. Public copy must not present it as a scientific proof, legal compliance tool, autonomous hacking agent, medical tool or production browser-control system.
