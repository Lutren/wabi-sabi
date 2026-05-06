# Gumroad Listing Copy Update - 2026-05-06

Status: `LIVE_UPDATED_VERIFIED`

## Scope

Updated only the public listing copy for the two existing live Gumroad products:

- `MEDIOEVO Agent Ops Pack`
- `DUAT Templates`

No product price, file upload, product artifact, payout setting, dashboard
setting, deletion, new product creation, Gumroad media upload, website deploy,
LinkedIn edit, social post, DNS change or GitHub push was executed in this
pass.

## Preflight

| check | result |
|---|---|
| pending tracker | `active_dedup=0`, `claudio_open=0` |
| host gate after sequential recheck | `LIMPIO / APPROVE` at `2026-05-06T13:04:57Z` |
| listing JSON parse | OK for both listings |
| listing secret scans | `count_reported=0` for both listing JSON files |
| source/product secret scans | `count_reported=0` in Gumroad publisher preflight |
| artifact secret scans | `count_reported=0` for both ZIPs |
| path scrub | OK |
| claims scan | OK |
| API verify before update | both products found by existing `short_url` and `id` |

## Updates Executed

| product | operation | ActionGate | artifact hash |
|---|---|---|---|
| `MEDIOEVO Agent Ops Pack` | `update_product` | `pass`, decision `80de9c7f-f8df-4b64-b0a3-9245891240d1` | unchanged `7cf8fdf5c8da49d691947becebdd3feae5f93b7e062212af38e3063404fab948` |
| `DUAT Templates` | `update_product` | `pass`, decision `f1fb05d0-62f8-4f4c-bdb8-23428bccd4f3` | unchanged `03c926b549307ef6106d80117183bb22121354671a10e0f2527473c06f6ca518` |

Both update runs used `with_file_requested=false`, so no delivery ZIP was
uploaded or replaced.

## Public Verification

`https://lrgonzalez.gumroad.com/l/medioevo-agent-ops-pack`:

- HTTP `200`;
- contains `What you get`;
- contains `ActionGate checklist`;
- contains `What this does not include`;
- contains buyer-safe boundary text: `does not guarantee agent safety`.

`https://lrgonzalez.gumroad.com/l/duat-templates`:

- HTTP `200`;
- contains `What you get`;
- contains `Synthetic scenario brief`;
- contains `What this does not include`;
- contains buyer-safe boundary text: `not a prediction engine`.

## Post-Update Validation

| check | result |
|---|---|
| `pending_review.py --write --quiet` after docs/COMMS update | `active_dedup=0`, `claudio_open=0` |
| COMMS validator | `status=PASS`, `errors=0` |
| focused secret scans over touched docs/listings | `count_reported=0` |
| evidence artifact secret scan | `count_reported=0` with `--artifact` |
| public Gumroad recheck | both product URLs HTTP `200` with new copy markers visible |
| final host no-write check | `LIMPIO / APPROVE` at `2026-05-06T13:12:39Z` |

## Evidence

- `packages/paid/medioevo-agent-ops-pack/commerce/gumroad_listing.json`
- `packages/paid/duat-templates/commerce/gumroad_listing.json`
- `qa_artifacts/release_validation/gumroad-medioevo-agent-ops-pack.json`
- `qa_artifacts/release_validation/gumroad-duat-templates.json`
- `qa_artifacts/release_validation/gumroad-listing-copy-update-2026-05-06.json`

## Boundary

The copy reinforces what buyers get and what they do not get. It does not offer
private Claudio runtime access, private prompts, credentials, account access,
RPG/TCG source/assets/lore, unreleased books, real private datasets, prediction
claims, scientific validation, diagnosis, guaranteed safety or guaranteed
outcomes.
