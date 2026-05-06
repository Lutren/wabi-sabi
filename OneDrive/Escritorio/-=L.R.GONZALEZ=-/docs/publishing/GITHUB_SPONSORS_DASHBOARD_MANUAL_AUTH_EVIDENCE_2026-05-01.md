# GitHub Sponsors Dashboard Evidence - 2026-05-01

Scope: verify and complete the live GitHub Sponsors dashboard for `Lutren` without exposing credentials or private technology.

## Current Public State

Public page:

`https://github.com/sponsors/Lutren`

Latest no-cache public check:

```json
{
  "timestamp": "2026-05-01T15:55:52",
  "url": "https://github.com/sponsors/Lutren",
  "contains_goal": true,
  "contains_short_bio": true,
  "contains_observer": true,
  "contains_builder": true,
  "contains_lab": true,
  "contains_patron": true,
  "contains_integration": true,
  "contains_tier_ladder": true,
  "contains_500": true,
  "contains_custom_amount": true,
  "length": 163209
}
```

Interpretation: the public Sponsors page now exposes the goal, profile copy, custom amount flow and five named monthly tier cards.

## Dashboard Route Used

The public Sponsors preview page exposes an owner-only link labeled `Edit your profile`.

Clicking that link navigates to:

`https://github.com/sponsors/Lutren/dashboard`

That route is the active dashboard entry point for this account.

## Completed Dashboard Updates

Profile details were submitted through the dashboard:

- Short bio: local-first safety gates for AI agents.
- Introduction: public-safe open core, ActionGate, ResidueOS Lite, ObservationEnvelope, evidence/provenance/audit trails, and paid/private boundaries.
- Feature opt-in checkbox: enabled.

Goal created:

- Goal type: number of monthly sponsors.
- Target: `25`.
- Public goal copy: public-safe local-first agent safety gate, documentation, tests, release checklists, sanitized examples and lightweight demos.

Monthly tiers created and published:

- `Observer` - USD 5/month.
- `Builder` - USD 19/month.
- `Lab` - USD 50/month.
- `Patron` - USD 100/month.
- `Integration Sponsor` - USD 500/month.

All tier descriptions keep the commercial boundary clear. They do not offer private repositories, private prompts, unreleased canon/books, RPG/TCG material, family data, credentials, machine access, secret access, guaranteed safety, hallucination-removal guarantees, or medical/legal/financial promises.

## Evidence Files

Screenshots:

- `qa_artifacts/github_sponsors_dashboard_2026-05-01/profile_details_after_update_click.png`
- `qa_artifacts/github_sponsors_dashboard_2026-05-01/goal_after_publish_click.png`
- `qa_artifacts/github_sponsors_dashboard_2026-05-01/tier_5_after_publish_click.png`
- `qa_artifacts/github_sponsors_dashboard_2026-05-01/tier_19_after_publish_click.png`
- `qa_artifacts/github_sponsors_dashboard_2026-05-01/tier_50_after_publish_click.png`
- `qa_artifacts/github_sponsors_dashboard_2026-05-01/tier_100_after_publish_click.png`
- `qa_artifacts/github_sponsors_dashboard_2026-05-01/tier_500_after_publish_click.png`
- `qa_artifacts/github_sponsors_dashboard_2026-05-01/public_sponsors_page_after_updates_top.png`
- `qa_artifacts/github_sponsors_dashboard_2026-05-01/public_sponsors_page_after_updates_tiers_mid.png`

Public verification artifact:

- `qa_artifacts/github_sponsors_dashboard_2026-05-01/public_sponsors_verification_after_dashboard_updates.json`

Focused secret scan artifact:

- `qa_artifacts/github_sponsors_dashboard_2026-05-01/focused_docs_secret_scan_after_dashboard_updates.json` (`count_reported=0`)

## Residual Account Hygiene

GitHub still shows the account banner requiring two-factor authentication before June 14, 2026. This was not changed in this pass because 2FA setup requires account-owner security choices and devices.

Follow-up user report: tax, payout and bank information were edited/completed by the account owner. No fiscal, bank or payout values were copied, stored or reproduced here.

No PIN, passkey, OTP, backup code, password, tax data, bank data or payout data was entered, stored or reproduced in this document.

## Boundary

Do not offer or paste private prompts, private repositories, unreleased books/canon, RPG/TCG material, family data, credentials, machine access, secret access, guaranteed safety, hallucination-removal guarantees, or medical/legal/financial promises.
