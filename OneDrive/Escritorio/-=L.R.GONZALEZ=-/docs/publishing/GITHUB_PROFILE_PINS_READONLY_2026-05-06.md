# GitHub Profile Pins Read-Only Check - 2026-05-06

Status: `READ_ONLY_VERIFIED / NO_CHANGE_NEEDED_NOW`

## Scope

Verify the current public pinned repositories for `Lutren` before deciding
whether a profile mutation is justified.

No pin, unpin, profile edit, README change, funding change, repo setting change
or GitHub push was executed.

## Auth Context

`gh auth status` reports an active `Lutren` GitHub CLI session. The token values
were not recorded in this artifact.

## Current Pins

Read through GitHub GraphQL `user(login:"Lutren").pinnedItems(first: 6,
types: REPOSITORY)`.

| order | repo | visibility | archived | pushed |
|---|---|---|---|---|
| 1 | `data-curation-observatory` | public | false | `2026-05-03T03:59:21Z` |
| 2 | `residueos` | public | false | `2026-05-02T11:07:17Z` |
| 3 | `Lutren` | public | false | `2026-05-05T12:46:21Z` |
| 4 | `medioevo-tools` | public | false | `2026-04-22T02:23:11Z` |
| 5 | `rapid-agent-guardian` | public | false | `2026-05-01T18:42:45Z` |
| 6 | `safe-exec` | public | false | `2026-04-22T02:23:09Z` |

## Decision

Current pins are public, non-archived and relevant to the public profile:
curation, ActionGate, profile hub, author tooling, hackathon safety gate and
safe execution.

Do not mutate pins in this run. The marginal benefit of reordering is lower
than the risk of changing a live profile surface without a dedicated visual
review.

## Optional Future Pin Review

If a future pass intentionally reorders pins, review these candidates against
the public README and Sponsors funnel:

- keep `data-curation-observatory`, `residueos`, `Lutren` and
  `rapid-agent-guardian`;
- compare `medioevo-tools` and `safe-exec` against `obsai-core`,
  `observacionismo-gate`, `obs-safe-integration-kit`, `claudio-os-blueprint`
  and `duat-genesis`;
- execute only after ActionGate, focused public-surface scan and post-action
  public verification.
