# GitHub Profile Bio Patch - 2026-05-01

Status: `APPLIED_WITH_STORED_GH_TOKEN`

Target: `https://github.com/Lutren`

Goal: make the public GitHub profile sharper for Sponsors traffic without exposing private technology.

## Current Verified State

- Login: `Lutren`
- Name: `Tyr`
- Blog: `medioevo.space`
- Current bio starts with: `Autistic writer building persistent-context systems, local-first tools, and operator frameworks for AI continuity across sessions.`

## Attempted API Update

Command class: `PATCH /user`

Initial result: blocked by token scope.

GitHub CLI returned that this operation needs the `user` scope and suggested:

```powershell
gh auth refresh -h github.com -s user
```

Later result: user supplied `C:\Users\L-Tyr\Downloads\r.txt`; a GitHub token was extracted without printing it, stored in the `gh` keyring, and the profile update succeeded.

## Proposed Bio

```text
Writer + local-first AI systems builder. I build agent safety gates, audit trails, and continuity tools. Sponsor: github.com/sponsors/Lutren
```

## Proposed Blog

```text
https://medioevo.space
```

## Applied Command Shape

```powershell
$bio = 'Writer + local-first AI systems builder. I build agent safety gates, audit trails, and continuity tools. Sponsor: github.com/sponsors/Lutren'
$body = @{ bio = $bio; blog = 'https://medioevo.space' } | ConvertTo-Json -Compress
$body | gh api -X PATCH user --input -
```

## Verified Remote State

- Login: `Lutren`
- Name: `Tyr`
- Bio: `Writer + local-first AI systems builder. I build agent safety gates, audit trails, and continuity tools. Sponsor: github.com/sponsors/Lutren`
- Blog: `https://medioevo.space`

## Boundary

Do not add private prompts, internal orchestration claims, RPG/TCG material, family data, secrets or absolute outcome claims to the public profile bio.
