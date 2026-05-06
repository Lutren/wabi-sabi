# GitHub Sponsors High Tier Publication Report - 2026-05-06

Status: `LIVE_PUBLISHED_VERIFIED`

Public page: `https://github.com/sponsors/Lutren`

Dashboard target: `https://github.com/sponsors/Lutren/dashboard/tiers`

Publication time recorded: `2026-05-06T09:14:45Z`

## Scope

Executed only the prepared GitHub Sponsors high-tier target after the owner
authorized browser control and publication in chat.

No GitHub push, social post, Gumroad edit, LinkedIn edit or website deploy was
executed in this pass.

## Published Monthly Tiers

| price | name | status |
|---|---|---|
| `US$1,000/month` | `Founder Research Patron` | `PUBLISHED_VERIFIED` |
| `US$5,000/month` | `Strategic Lab Patron` | `PUBLISHED_VERIFIED` |
| `US$10,000/month` | `Institutional Research Partner` | `PUBLISHED_VERIFIED` |

The dashboard returned `You've published a tier.` after each publication. The
monthly tier count visible in the dashboard increased to `8`.

## Custom Amount Correction

The public page initially showed a custom amount of `US$12,000/month`, inherited
from existing dashboard settings. That conflicted with the intended high-tier
ladder. The dashboard custom amount settings were aligned to:

| field | value | evidence |
|---|---:|---|
| recommended sponsorship amount | `10000` | dashboard green check |
| minimum custom amount | `1000` | dashboard green check |

Post-correction public verification found `US$10,000` and did not find
`US$12,000`.

## Public Verification

Command:

```powershell
Invoke-WebRequest -UseBasicParsing -Uri https://github.com/sponsors/Lutren
```

Result:

```text
status=200
Founder Research Patron=True
Strategic Lab Patron=True
Institutional Research Partner=True
$1,000=True
$5,000=True
$10,000=True
$12,000=False after custom amount correction
```

## Screenshot Evidence

Stored under
`qa_artifacts/github_sponsors_dashboard_2026-05-06/`:

- `tier_1000_after_publish_click.png`
- `tier_5000_after_publish_click.png`
- `tier_10000_after_publish_click.png`
- `dashboard_custom_amount_after_retype_recommend.png`
- `public_sponsors_page_top_after_publish.png`
- `public_sponsors_page_top_after_custom_fix.png`

## Boundary Check

The published tiers are sponsorship access to curated public-safe research
packets, demos, roadmap notes and briefings. They do not offer raw workspace
research dumps, private runtime prompts, secrets, account access, unpublished
books, RPG/TCG material, real private datasets or guaranteed outcomes.
