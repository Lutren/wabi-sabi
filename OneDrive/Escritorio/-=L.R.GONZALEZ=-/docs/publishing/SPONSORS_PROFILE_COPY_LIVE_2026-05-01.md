# Sponsors Profile Copy Live - 2026-05-01

Status: `PASTE_READY_DASHBOARD`

Purpose: improve the live GitHub Sponsors profile without giving away private technology, paid implementation work, private canon, RPG/TCG material, prompts, secrets or family data.

## Current Live Diagnosis

- Public URL: `https://github.com/sponsors/Lutren`
- Current visible copy is generic and does not explain the problem being solved.
- Public page shows a custom monthly amount field and no visible published tiers.
- Best positioning: local-first safety gates for AI agents, with evidence before action and human review before risky automation.

## Short Bio

Building local-first safety gates for AI agents: evidence before action, audit trails, and human review before risky automation.

## Introduction

AI agents can move faster than teams can audit. I build local-first tools that make agents leave evidence, provenance, residue logs, and review points before sensitive actions.

The public work focuses on the safe open core: ActionGate, ResidueOS Lite, ObservationEnvelope, reproducible examples, documentation, and small local utilities that help builders test agent behavior before trusting it.

Sponsorship funds maintenance, tests, security review, documentation, sanitized demos, and lightweight releases. It does not buy private prompts, the full internal orchestration layer, family data, unreleased books, RPG/TCG material, secrets, or absolute outcome claims.

Sponsor this work if you want AI agents that are slower to overreach and better at proving what they did, why they did it, and what still needs human review.

## Monthly Tiers

### Observer - USD 5/month

Monthly public-safe build notes: what shipped, what failed, and what is being tested next.

Welcome message:

Thanks for supporting the public layer. You will receive monthly public-safe build notes with shipped work, test evidence, and next priorities.

### Builder - USD 19/month

Early access to public-safe demos, examples and short implementation notes for local agent safety gates.

Welcome message:

Thanks for helping fund practical examples. You will receive early public-safe demos, implementation notes, and sanitized patterns that do not expose private orchestration.

### Lab - USD 50/month

Public-safe benchmark notes, release-risk reports and priority voting for open examples and docs.

Welcome message:

Thanks for funding deeper validation. You will receive public-safe benchmark notes, release-risk reports, and priority voting on open examples and documentation.

### Patron - USD 100/month

Optional mention plus one short monthly office-hours consult about public-safe usage, integration boundaries or release planning.

Welcome message:

Thanks for backing the work at a serious level. You may request an optional mention and one short monthly office-hours consult focused on public-safe/local-first usage.

### Integration Sponsor - USD 500/month

One monthly implementation review or architecture note for public-safe/local-first agent workflows. No private IP transfer, no secret access, no guaranteed outcomes.

Welcome message:

Thanks for sponsoring implementation-focused work. This tier covers one monthly architecture review or implementation note within public-safe boundaries. It does not include private repositories, secrets, internal prompts, family data, unreleased canon, RPG/TCG assets, or absolute outcome claims.

## Sponsor Goal

Use a sponsor-count goal instead of a money goal so the page does not publicly
center current revenue.

Goal type: `Number of monthly sponsors`

Target: `25`

Description:

Help fund a public-safe local-first agent safety gate: documentation, tests,
release checklists, sanitized examples and lightweight demos for builders who
want AI agents to leave evidence before action.

Short version:

25 monthly sponsors to fund public-safe docs, tests and demos for local-first
AI agent safety gates.

## Featured Repositories

Recommended order:

1. `safe-exec`
2. `medioevo-tools`
3. `data-double-slit`
4. Future public `residueos` repository only after package scan and release gate pass.
5. Future public `obsai-core` repository only after package scan and release gate pass.

Do not feature private, experimental, patent-adjacent, family, RPG/TCG, unreleased book, or broad-orchestration repositories.

## Do Not Offer

- Full private orchestration layer.
- Private prompts or method internals.
- Family data, legal or financial strategy.
- RPG/TCG access, lore, mechanics, assets or bridge data.
- Full books or paid companion PDFs.
- Secrets, local sessions, credentials or machine access.
- Medical, legal, financial or security guarantees.
- Claims that promise total hallucination removal, absolute safety or solved alignment.

## Dashboard Status

Dashboard completed on 2026-05-01 through `https://github.com/sponsors/Lutren/dashboard`.

Published items:

- Profile details: short bio and introduction.
- Goal: `25 monthly sponsors`.
- Tiers: `$5 Observer`, `$19 Builder`, `$50 Lab`, `$100 Patron`, `$500 Integration Sponsor`.
- Public verification: `qa_artifacts/github_sponsors_dashboard_2026-05-01/public_sponsors_verification_after_dashboard_updates.json`.

Residual manual account items:

- Complete GitHub 2FA before June 14, 2026.
- Tax/payout/bank was reported by the account owner as edited/completed; no sensitive values are stored here.

## API Attempt Result

GraphQL `createSponsorsTier` exists, but the authenticated GitHub CLI token was
blocked with `Resource not accessible by personal access token` when trying to
publish the tiers. The live dashboard UI remains the required path for final
tiers/goals publication.

Follow-up 2026-05-01:

- Retried with the keyring credential by clearing `GH_TOKEN`.
- Confirmed the authenticated viewer is `Lutren`.
- GitHub still blocked `viewer.sponsorsListing` and `createSponsorsTier`.
- A `USD 5 Observer` tier was attempted with `publish=true`; no tier was
  created because the mutation was rejected before writing.
- Goals do not expose a visible GraphQL mutation in the current schema; publish
  the sponsor-count goal through the dashboard.
- Dashboard UI was then used successfully; API limitation is no longer blocking
  the public Sponsors page.
