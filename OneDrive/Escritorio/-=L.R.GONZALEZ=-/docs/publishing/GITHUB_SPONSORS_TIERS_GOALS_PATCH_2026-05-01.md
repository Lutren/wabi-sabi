# GitHub Sponsors Tiers And Goals Patch - 2026-05-01

Status: `DASHBOARD_PUBLISHED_PUBLIC_VERIFIED`

## Public Problem

The public Sponsors page at `https://github.com/sponsors/Lutren` now shows the
intended tier/goal structure.

Public no-cache check:

- `Observer`, `Builder`, `Lab`, `Patron`, `Integration Sponsor`: visible.
- Sponsor goal `25 monthly sponsors`: visible.
- Profile README and repos do expose the Sponsor link.

## API Attempt

GraphQL schema exposes `createSponsorsTier`, and GitHub Docs describe the
`CreateSponsorsTierInput` fields. The mutation was attempted with:

- `sponsorableLogin=Lutren`
- `publish=true`
- monthly tiers at USD `5`, `19`, `50`, `100`, `500`

GitHub returned:

```text
Resource not accessible by personal access token
```

The same token can update normal profile/repository metadata, but it cannot
manage Sponsors tiers/goals through the Sponsors GraphQL surface.

Follow-up verification:

- The keyring credential was forced by clearing `GH_TOKEN` for the command.
- `viewer.login` resolved to `Lutren`.
- `viewer.sponsorsListing` and `createSponsorsTier` still returned
  `Resource not accessible by personal access token`.
- The mutation did not create a partial draft or live tier.
- The GraphQL schema exposes tier creation/publish/retire mutations, but no
  Sponsors goal mutation was found; goals remain dashboard-only in this run.

## Dashboard Values Published

### Goal

Goal type: `Number of monthly sponsors`

Target: `25`

Description:

Help fund a public-safe local-first agent safety gate: documentation, tests,
release checklists, sanitized examples and lightweight demos for builders who
want AI agents to leave evidence before action.

### Monthly Tiers

USD 5:

Observer: monthly public-safe build notes on agent safety gates, evidence
trails, shipped work, failed tests and next priorities.

USD 19:

Builder: early access to public-safe local demos, examples and short
implementation notes for agent safety gates.

USD 50:

Lab: public-safe benchmark notes, release-risk reports and priority voting for
open examples and documentation.

USD 100:

Patron: optional mention plus one short monthly office-hours consult on
public-safe local-first agent workflows, boundaries or release planning.

USD 500:

Integration Sponsor: one monthly implementation review or architecture note for
public-safe/local-first agent workflows. No private IP transfer, secret access
or guaranteed outcomes.

## Public Boundary

Do not offer:

- private prompts;
- internal orchestration;
- private repositories;
- unreleased canon, books, RPG/TCG material or family data;
- credentials, machine access or secrets;
- guaranteed safety, guaranteed hallucination removal or medical/legal/financial
  promises.

## Dashboard Route Used

- Dashboard entry: `https://github.com/sponsors/Lutren/dashboard`
- Evidence: `docs/GITHUB_SPONSORS_DASHBOARD_MANUAL_AUTH_EVIDENCE_2026-05-01.md`

## Verification Criteria

Complete. Public page shows:

- a tier around USD 5 with Observer/updates language;
- a tier around USD 19 with Builder/demo language;
- a tier around USD 50 with Lab/benchmark language;
- a tier around USD 100 with Patron/consult language;
- optionally USD 500 Integration Sponsor;
- a visible sponsor-count goal for 25 monthly sponsors.
