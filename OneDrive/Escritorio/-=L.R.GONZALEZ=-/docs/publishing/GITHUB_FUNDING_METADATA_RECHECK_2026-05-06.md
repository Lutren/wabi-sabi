# GitHub Funding Metadata Recheck - 2026-05-06

Status: `READ_ONLY_VERIFIED / NO_PUSH_EXECUTED`

## Scope

Resolve the stale `GitHub funding metadata` review item from the public-profile
queue. This pass performed read-only local and public checks only.

No GitHub push, profile edit, repo setting change, pin change, Sponsors
dashboard edit or branch mutation was executed.

## Evidence

| target | result |
|---|---|
| local `.github/FUNDING.yml` | present; contains `github: Lutren` |
| `https://raw.githubusercontent.com/Lutren/.github/main/FUNDING.yml` | HTTP `404` |
| `https://raw.githubusercontent.com/Lutren/.github/main/.github/FUNDING.yml` | HTTP `404` |
| `https://raw.githubusercontent.com/Lutren/Lutren/main/.github/FUNDING.yml` | HTTP `200`; contains `Lutren` |
| `https://api.github.com/repos/Lutren/Lutren/contents/.github/FUNDING.yml` | HTTP `200`; contains `FUNDING.yml` metadata and `Lutren` |

## Decision

The public funding metadata for the profile is verified in the `Lutren/Lutren`
profile repository path:

```text
https://raw.githubusercontent.com/Lutren/Lutren/main/.github/FUNDING.yml
```

The earlier 404 was route-specific, not evidence that funding metadata was
missing.

## Remaining GitHub Boundary

- GitHub profile README: no urgent change needed.
- GitHub funding metadata: no urgent change needed.
- GitHub pinned repos: still `REVIEW` because it needs visual/API-safe pin
  verification before any profile UI change.
- GitHub push remains gated by target-specific ActionGate and focused secret
  scan.
