# Claudio Root Human Migration Plan - 2026-05-06

Status: `DRY_RUN_NO_MOVES`

## Objective

Make Claudio navigable for humans without breaking the runtime or trampling concurrent agent work.

## Proposed Root Contract

Keep visible at root only:

- `00_LEER_PRIMERO.md` or equivalent root README.
- `apps/`, `core/`, `tests/`, `tools/`, `docs/`, `runtime/`, `reports/`.
- `website/`, `products/`, `data/`, `datasets/` when actively used.
- Required repo control files.

Everything else gets a category-specific move plan before any physical action.

## Batches

| order | batch | action | gate |
|---:|---|---|---|
| 1 | secrets and local config | move to private config lane or keep blocked | `BLOCK/REVIEW` |
| 2 | launchers | move to `tools/launchers` with README | `REVIEW` |
| 3 | root docs | move to `docs/root_notes_review` or canon docs | `REVIEW` |
| 4 | root python scripts | move to `tools/root_scripts_review` then classify owners | `REVIEW` |
| 5 | caches/generated | delete only if regenerable and logged | `APPROVE` |
| 6 | legacy/archive dirs | consolidate into one archivo frio lane | `REVIEW` |

## Current Counts

- Root items: `240`
- Root files: `88`
- Root directories: `152`
- Git pending lines: `913`

## No-Go

- Do not delete `.env`, tokens, databases, model files, private RPG/TCG or PSI sources.
- Do not broad-stage the nested repo.
- Do not move files touched by other agents without a rollback manifest.
- Do not publish or deploy from this cleanup pass.

## Next Safe Command

Create a move-manifest for one batch at a time, starting with launchers or root docs. Do not start with secrets or runtime code.
