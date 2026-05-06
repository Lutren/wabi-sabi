# CLAIMS_BOUNDARY

Status: active boundary.

This document separates product claims, research claims and private-world
material. It exists to prevent accidental overclaiming.

## Allowed Product Claims

Allowed only when implemented and verified:

- action gate returns stable `APPROVE`, `REVIEW` or `BLOCK` decisions;
- JSON output schema is stable and covered by tests;
- SQLite persistence exists and survives restart;
- human review queue exists and is auditable;
- public or commercial package was generated from an allowlist;
- Gumroad or website publication was verified with live evidence.

## Allowed Public GitHub Claims

Allowed for sanitized repos and whitepapers when the repo contains only clean,
synthetic, public-safe material:

- local-first data curation workflow;
- action gate for AI action review;
- pre-execution ActionGate wrappers that evaluate proposed shell/browser/research actions without executing them;
- evidence envelope for web/research observations;
- claim registry and evidence store;
- operational calibration templates;
- reproducible demos and falsifier scaffolds;
- project boundary map separating open, commercial, editorial and private lanes.

Every public repo must include `CLAIMS.md` and `PRIVATE_EXCLUSIONS.md`.

## Demo-Only Claims

Use `DEMO_ONLY` until real calibration data exists:

- `theta_approve`;
- `theta_review`;
- `Theta`;
- `J_c`;
- action-gate weights;
- confusion matrices generated from synthetic examples;
- threshold performance claims;
- world simulation or residue scores without supervised validation.

## Research-Only Claims

Use `RESEARCH_ONLY` and store under `research/` or equivalent research boundary:

- operational consciousness;
- Orch OR;
- Hameroff/Penrose;
- EML;
- cosmology;
- physics interpretations;
- claims that require falsifiers, predictions or peer review.
- patent-adjacent engineering patterns before legal review.

Strong claims must include one of:

- falsifier;
- `PREDICTION_REQUIRED`;
- explicit note that this is speculative research, not product behavior.

## Strong Claim Falsification Gate

Effective 2026-05-02, strong claims are not adopted as product copy unless they
are tested or explicitly downgraded. Use
`docs\developer\CLAIM_FALSIFICATION_REGISTER_2026-05-02.md` as the active
registry.

Every strong claim must be labelled:

- `OBSERVED`;
- `INFERENCE`;
- `HYPOTHESIS`;
- `UNKNOWN`;
- `VERIFIED`;
- `FALSIFIED`;
- `DEMO_ONLY`;
- `RESEARCH_ONLY`;
- `BLOCK`.

If a claim cannot be tested or falsified in the current release, it cannot be
used as a public or commercial product promise.

## Patent Pattern Boundary

Patent-adjacent files may inform abstract software patterns only. Every derived
module, spec or product note must preserve these labels:

- `ABSTRACT_SOFTWARE_PATTERN_ONLY`;
- `LEGAL_REVIEW_REQUIRED`;
- `RESEARCH_ONLY` unless the specific product claim was separately reviewed.

Allowed abstraction:

```text
global signal -> authorized receptor -> local threshold/gate -> evidence and residue ledger -> reversible action or human review
```

Blocked claims:

- patent clearance or freedom to operate;
- biomedical, therapeutic, device or genetic-engineering instructions;
- assertion that a patent validates Observacionismo scientifically;
- product copy implying proven consciousness, physics or medical capability.

## MEDIOEVO / Lore Claims

Lore Compiler outputs must distinguish:

- `evidence`: direct source fragment, file or canon reference;
- `inference`: structured interpretation from evidence;
- `contradiction`: conflict routed to `canon_residue`;
- `private`: data that cannot leave the private game/canon boundary.

Do not publish full books, private lore, TCG data, game balance or unreleased
assets through open tooling.

## Private Game Claims

The private game may be improved in the `rpg-private` lane only. Do not claim:

- open-source availability;
- free release;
- public package readiness;
- Gumroad/web publication;
- game build readiness without Godot headless validation.

## Product Copy Rule

Public copy may sell:

- continuity;
- operational control for AI actions;
- action-gate review;
- handoff discipline;
- lore-to-data tooling;
- local-first review workflows.

Public copy must not sell:

- proven consciousness;
- solved physics;
- solved cosmology;
- autonomous safety guarantees;
- private game access unless explicitly released as a paid private product.

## Public GitHub Prohibited Claims

Public GitHub copy must not claim:

- proof of consciousness;
- new validated physics;
- antigravity;
- solved cosmology;
- medical, therapeutic or biomedical capability;
- autonomous research without human supervision;
- autonomous shell/browser/research execution from `obs-safe-integration-kit`;
- guaranteed safety;
- access to Claudio private runtime, private agent prompts, RPG, full books or assets.
