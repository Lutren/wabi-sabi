# Public Profile Pending Sweep - 2026-05-06

Status: `LOCAL_SWEEP_COMPLETE / WEBSITE_DEPLOY_DONE / GUMROAD_COPY_DONE / EXTERNALS_GATED`

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

Latest update: after the copy-only Gumroad publication pass, COMMS validated
with `status=PASS`, `errors=0`; focused secret scans over touched docs/listings
reported `count_reported=0`; the evidence artifact scan reported
`count_reported=0` with `--artifact`; public Gumroad recheck returned HTTP
`200` for both product URLs with the new copy markers visible; final host
no-write check at `2026-05-06T13:12:39Z` returned `LIMPIO / APPROVE`.

Latest final sequential host no-write check at `2026-05-06T13:46:30Z` returned
`LIMPIO / APPROVE`. A parallel check at `13:46:15Z` briefly reported
`JAMMING / BLOCK` because it was run alongside other Python validations; the
sequential recheck is the durable final host evidence.

## Current Target Truth

| target | status | evidence | next action |
|---|---|---|---|
| GitHub Sponsors high tiers | `DONE_PUBLISHED_VERIFIED` | public page HTTP `200`; found `Founder Research Patron`, `Strategic Lab Patron`, `Institutional Research Partner`, `$1,000`, `$5,000`, `$10,000`; did not find `$12,000` | none unless copy changes |
| GitHub profile README | `NO_CHANGE_NEEDED_NOW` | raw README HTTP `200`; found `Publication Lanes`, `Three Public Paths`, sponsor link, Gumroad and MEDIOEVO | no patch now |
| GitHub funding metadata | `READ_ONLY_VERIFIED / NO_CHANGE_NEEDED_NOW` | `Lutren/Lutren/.github/FUNDING.yml` raw and API checks returned HTTP `200` and contain `Lutren`; earlier `Lutren/.github` route returned `404` | none unless funding links change |
| GitHub pinned repos | `READ_ONLY_VERIFIED / NO_CHANGE_NEEDED_NOW` | GraphQL returned six public, non-archived pinned repos: `data-curation-observatory`, `residueos`, `Lutren`, `medioevo-tools`, `rapid-agent-guardian`, `safe-exec` | optional future visual review only |
| Website live home | `DONE_DEPLOYED_VERIFIED` | live `https://medioevo.space/` HTTP `200`; found `GitHub Sponsors`, `https://github.com/sponsors/Lutren` and JSON-LD `sameAs` after deploy | none unless copy changes |
| Gumroad Agent Ops Pack | `DONE_UPDATED_VERIFIED` | public page HTTP `200`; now contains `What you get`, `ActionGate checklist`, `What this does not include` and buyer-safe boundary text | none unless copy/media changes |
| Gumroad DUAT Templates | `DONE_UPDATED_VERIFIED` | public page HTTP `200`; now contains `What you get`, `Synthetic scenario brief`, `What this does not include` and `not a prediction engine` boundary | none unless copy/media changes |
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
- Future Gumroad listing edits or media uploads after this copy-only update.
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

## Update - Gumroad Listing Copy

After the website deploy, both live Gumroad products were updated as copy-only
targets:

- `docs/publishing/GUMROAD_LISTING_COPY_UPDATE_2026-05-06.md`;
- `qa_artifacts/release_validation/gumroad-listing-copy-update-2026-05-06.json`;
- no delivery ZIP upload or price change;
- both public product pages returned HTTP `200` with the new includes/excludes
  copy visible;
- post-update validation kept `pending_review` at `active_dedup=0`,
  `claudio_open=0` and COMMS at `PASS`.

## Update - GitHub Funding Metadata

Read-only recheck resolved the stale `REVIEW` item for funding metadata:

- `docs/publishing/GITHUB_FUNDING_METADATA_RECHECK_2026-05-06.md`;
- `qa_artifacts/release_validation/github-funding-metadata-recheck-2026-05-06.json`;
- remote `https://raw.githubusercontent.com/Lutren/Lutren/main/.github/FUNDING.yml`
  returned HTTP `200` and contains `Lutren`;
- no GitHub push, profile edit, pin change or Sponsors dashboard edit was
  executed.

## Update - GitHub Profile Pins

Read-only GraphQL check verified the current public pins:

- `docs/publishing/GITHUB_PROFILE_PINS_READONLY_2026-05-06.md`;
- `qa_artifacts/release_validation/github-profile-pins-readonly-2026-05-06.json`;
- all six pins are public and not archived;
- no pin/unpin, profile edit, README change, funding change or GitHub push was
  executed.

## Update - Remaining Gated Workpack

The remaining public-profile, commercial, legal, dependency and model gates were
converted into a target-specific reopen workpack:

- `docs/pending/REMAINING_GATED_WORKPACK_2026-05-06.md`;
- `qa_artifacts/release_validation/remaining-gated-workpack-2026-05-06.json`;
- ActionGate dry-runs passed for LinkedIn owner-view confirmation, social post,
  Gumroad media upload, future public publish and future website deploy paths;
- no LinkedIn edit, social post, Gumroad media upload, GitHub push, DNS change,
  legal/payment action, commercial sale approval, model promotion, ISO/QEMU
  build or destructive cleanup was executed.

## Update - Public Content Ready Packet

Social and optional Gumroad media preparation was completed locally:

- `docs/publishing/PUBLIC_CONTENT_READY_PACKET_2026-05-06.md`;
- `docs/publishing/assets/social/2026-05-06/`;
- `qa_artifacts/release_validation/public-content-ready-packet-2026-05-06.json`;
- SVG assets parse as XML and focused secret scans returned
  `count_reported=0`;
- no social post, scheduling, account edit, Gumroad media upload, listing
  change or delivery file upload was executed.
