# Public Profile Pending Sweep - 2026-05-06

Status: `LOCAL_SWEEP_COMPLETE / WEBSITE_DEPLOY_DONE / EXTERNALS_GATED`

Scope: continue the remaining public-profile, GitHub, Gumroad, LinkedIn,
website and social pending work after GitHub Sponsors high tiers were published.

## Gate

Earlier sweep host check:

```powershell
python tools\host_observacionista.py --no-write
```

Result at `2026-05-06T09:46:37Z`:

| field | value |
|---|---|
| status | `MIXTO` |
| gate | `REVIEW` |
| reason | `residuo_precaucion` |
| memory | `76.0%` |
| disk | `80.3%` |
| lambda_sat | `0.803` |

Interpretation: do not run broad publication, push, deploy, Gumroad saves,
LinkedIn edits or social posts from this host state. Continue local/evidence
work.

Later update: a fresh persisted host check returned `LIMPIO / APPROVE` at
`2026-05-06T12:44:55Z`, then the single prepared website deploy target passed
ActionGate and was executed. Final no-write host check at
`2026-05-06T12:48:17Z` remained `LIMPIO / APPROVE`.

## Current Target Truth

| target | status | evidence | next action |
|---|---|---|---|
| GitHub Sponsors high tiers | `DONE_PUBLISHED_VERIFIED` | public page HTTP `200`; found `Founder Research Patron`, `Strategic Lab Patron`, `Institutional Research Partner`, `$1,000`, `$5,000`, `$10,000`; did not find `$12,000` | none unless copy changes |
| GitHub profile README | `NO_CHANGE_NEEDED_NOW` | raw README HTTP `200`; found `Publication Lanes`, `Three Public Paths`, sponsor link, Gumroad and MEDIOEVO | no patch now |
| GitHub funding metadata | `REVIEW` | checked public raw `.github/FUNDING.yml`; got `404` at that path | inspect only in a GitHub target window |
| Website live home | `DONE_DEPLOYED_VERIFIED` | live `https://medioevo.space/` HTTP `200`; found `GitHub Sponsors`, `https://github.com/sponsors/Lutren` and JSON-LD `sameAs` after deploy | none unless copy changes |
| Gumroad Agent Ops Pack | `LIVE_SAFE_ENHANCEMENT_PENDING` | public page HTTP `200`; already has ActionGate/private-runtime exclusion language; missing stronger `What you get` section | update listing after Gumroad target gate |
| Gumroad DUAT Templates | `LIVE_SAFE_ENHANCEMENT_PENDING` | public page HTTP `200`; has synthetic and prediction-exclusion boundary | update listing/media after Gumroad target gate |
| LinkedIn | `AUTHENTICATED_CONFIRMATION_REQUIRED` | public HTTP checks returned LinkedIn `999` for both candidate URLs | confirm canonical owner view before edit |
| Social posts | `DRAFT_READY_AFTER_GATE` | calendar exists; Sponsors post now factually valid | publish only with account auth, asset rights and target gate |

Evidence JSON:

```text
qa_artifacts/release_validation/public-profile-pending-sweep-2026-05-06.json
```

## Done In This Sweep

- Refreshed `pending_review`: `active_dedup=389`, `claudio_open=69`.
- Rechecked Claudio host gate: `MIXTO / REVIEW`.
- Verified Sponsors high tiers remain publicly visible.
- Verified the live website still needs the local Sponsors route deployed.
- Verified Gumroad product pages are live and already use safe boundary wording.
- Confirmed LinkedIn still cannot be treated as canonical through public HTTP.

## Still Gated

- Future Cloudflare/website deploys after this Sponsors route patch.
- Gumroad listing edits or media upload.
- LinkedIn profile edits or posts.
- Instagram/TikTok/YouTube posts.
- GitHub push/profile/pin changes.

These are not blocked because the copy is unready; they are blocked because
each needs a clean target execution window and post-action verification.

## Update - Website Sponsors Route Deploy

After a later host refresh returned `LIMPIO / APPROVE`, the prepared website
Sponsors route patch was deployed as a single target. Evidence:

- `docs/publishing/WEBSITE_SPONSORS_ROUTE_DEPLOY_2026-05-06.md`;
- `qa_artifacts/release_validation/website-sponsors-route-deploy-2026-05-06.json`;
- production `https://medioevo.space/` returned HTTP `200` and contains
  `GitHub Sponsors`, the Sponsors URL and JSON-LD `sameAs`.

No Gumroad, LinkedIn, social, GitHub push, DNS or product artifact action was
executed with this deploy.
