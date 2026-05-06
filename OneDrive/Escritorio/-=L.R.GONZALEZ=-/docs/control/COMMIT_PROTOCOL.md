# COMMIT_PROTOCOL

Status: active protocol.

This workspace is not one public repo. Do not use the global Git repo at
`C:\Users\L-Tyr` for portfolio commits.

## Loop

Every closure cycle must follow:

1. OBSERVE: read live state, Git status, continuity docs, affected source and existing tests.
2. SELECT: choose one lane only.
3. IMPLEMENT: touch only files owned by that lane.
4. VERIFY: run concrete tests, smokes or manifests.
5. DOCUMENT: update ledger or handoff only when evidence exists.
6. COMMIT: commit only owned paths, from the correct repo.
7. RESIDUE: record blocked work with cause, failed check and next action.

## Lanes

| lane | owns | cannot touch |
|---|---|---|
| cleanup | root control docs, manifests, non-destructive audits | product code, private game source |
| residueos | `apps/residueos` and its tests/docs | `obsai-core`, game, publishing surfaces |
| obsai | `packages/obsai-core` and action-gate tests | ResidueOS app UI/store, game |
| claudio | `-=MEDIOEVO=-\-=LIBROS\claudio` runtime/docs after reading its continuity files | root cleanup docs unless recording evidence |
| lore | lore compiler schemas, fixtures and evidence maps | full books, private game code |
| rpg-private | private game repo/manifests only after explicit authorization | open-source packages, public release folders |
| publishing | Gumroad/site/product manifests and commercial docs | research claims, private game source |
| research-boundary | `research/` material marked `RESEARCH_ONLY` | product marketing claims |

## Git Rules

- Never run `git add .`.
- Use `git add -- <owned paths>`.
- One commit per verified closure.
- Do not commit from `C:\Users\L-Tyr` for portfolio work.
- In `-=LIBROS`, expect branch `imagenes` and unrelated dirty state.
- In `claudio`, expect branch `fix/claudio-cli-latency` and unrelated dirty state.
- In `tools\claw-code`, touch only when the selected lane requires it.
- `E:\Medioevo_RPG` needs a private local repo and strict `.gitignore` before source edits.
- `E:\-=Medioevo=-` stays archive/editorial/commercial state controlled by manifests and checksums, not a new Git repo.

## Add Policy

Allowed example:

```powershell
git add -- COMMIT_PROTOCOL.md PORTFOLIO_EXECUTION_LEDGER.md
```

Blocked examples:

```powershell
git add .
git add -- .
git commit -am "cleanup"
```

## Closure Evidence

A commit is allowed only after the ledger records:

- selected lane;
- files changed;
- verification command and result;
- residue or blocker if incomplete;
- any claim boundary that applies.
