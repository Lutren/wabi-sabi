# GitHub Sponsors Live Audit 2026-05-01

Status: `LIVE_DASHBOARD_PUBLISHED_PUBLIC_VERIFIED`

## Evidence Checked

- Public Sponsors URL: `https://github.com/sponsors/Lutren`.
- Public page initial state observed: profile was live but only exposed a custom monthly amount selector; no named tiers were visible.
- Public page follow-up state: dashboard completed; public page now exposes goal `25 monthly sponsors`, custom amount and named tiers `$5/$19/$50/$100/$500`.
- Authenticated GitHub API state: user bio is already sponsor-focused:
  `Writer + local-first AI systems builder. I build agent safety gates, audit trails, and continuity tools. Sponsor: github.com/sponsors/Lutren`
- Profile README remote `Lutren/Lutren` contains a clear sponsor CTA and public boundary.
- Remote `.github/FUNDING.yml` contains `github: Lutren`.
- Profile README was updated again to include `rapid-agent-guardian`, suggested sponsor levels and the paid/private boundary; commit `f89578af7c6cfe67c67633dca3750eddbc4f49b6`.
- Public hackathon repo `https://github.com/Lutren/rapid-agent-guardian` is live, public, and contains `.github/FUNDING.yml`.
- Known public repos checked for funding metadata: `safe-exec`, `agent-handoff-protocol`, `agent-release-checklist`, `medioevo-tools`, `data-double-slit`, `rapid-agent-guardian`; all returned funding metadata present.
- GraphQL Sponsors listing query with the active `GH_TOKEN` showed `tiers.totalCount=0`.
- `createSponsorsTier` was attempted through the GitHub GraphQL API using the keyring credential; all four tier attempts failed with `Resource not accessible by personal access token`.

## Conversion Problem

Resolved for the Sponsors page: named monthly tiers and the sponsor-count goal are now visible publicly. The remaining account-hygiene issue is GitHub's 2FA requirement banner before June 14, 2026. Follow-up user report: payout/tax/bank was edited/completed by the account owner; no fiscal, bank or payout values are stored here.

The API credential could not create Sponsors tiers, so the live dashboard UI was used. GitHub's current docs describe tier/profile editing through the Sponsors dashboard UI, including `Profile details` and `Sponsor tiers`. The docs also state that tiers are optional, that up to 10 monthly and 10 one-time tiers can be published, and that published tier prices cannot be edited later.

Sources:

- `https://docs.github.com/en/sponsors/receiving-sponsorships-through-github-sponsors/setting-up-github-sponsors-for-your-personal-account`
- `https://docs.github.com/en/sponsors/receiving-sponsorships-through-github-sponsors/managing-your-sponsorship-tiers`

## Dashboard Copy

### Short Bio

Local-first AI agent safety gates, evidence trails, and handoff tools for builders who want agents to do real work without losing control.

### Introduction

I build public, local-first tools for AI agents that need to plan, act, leave evidence, and hand work back to a human before sensitive actions.

The open layer focuses on safety gates, audit trails, release checklists, handoff protocols, and public-safe examples. Sponsors help fund maintenance, tests, documentation, benchmark packs, and demos that other builders can inspect and reuse.

The public work stays open and verifiable. Private prompts, unreleased products, full orchestration, customer integrations, RPG/TCG material, family data, and paid implementation details stay private or commercial.

Sponsor this work if you want more practical infrastructure for agents that can do useful tasks without becoming opaque automation.

## Monthly Tiers

### $5 - Observer

Monthly public-safe update on agent safety gates, handoff patterns, and release discipline.

Welcome message:

Thanks for supporting the open layer. Your sponsorship helps keep the public tools maintained, tested, and documented.

### $19 - Builder

Observer benefits plus early notes on local demos, schemas, and implementation decisions that are safe to publish.

Welcome message:

You are funding practical examples for builders. Early notes stay public-safe and do not include private prompts, customer data, or unreleased proprietary systems.

### $50 - Lab

Builder benefits plus periodic benchmark notes, release-gate reports, and priority on public-safe examples.

Welcome message:

You are helping fund deeper tests and evidence packs. Reports remain honest: they show what passed, what failed, and what still needs review.

### $100 - Patron

Lab benefits plus optional public thanks in the profile README and one short monthly async review of a public-safe agent workflow.

Welcome message:

Thank you. This tier supports sustained maintenance. The monthly review is limited to public-safe workflows and does not include private IP transfer, guaranteed outcomes, medical/financial/security claims, or access to sensitive systems.

## Do Not Offer

- Private prompts or internal orchestration.
- Full product internals before paid release.
- RPG/TCG, family data, canon privado or unreleased books.
- Guaranteed safety, guaranteed anti-hallucination, medical, financial or legal claims.
- Access to secrets, customer data or local private runtimes.

## Next Manual Action

1. Complete GitHub 2FA before June 14, 2026 from the owner account/device.
2. Keep one-time custom amount enabled.
3. Do not attach private repositories to tiers unless a future paid contract explicitly requires it and passes review.

## Decision

`DASHBOARD_PUBLISHED / PUBLIC_PAGE_VERIFIED / API_TIERS_BLOCKED_BUT_NOT_BLOCKING`.

No public repo release, package upload, Gumroad listing or broad workspace publication is authorized by this audit.
