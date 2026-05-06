# MIGRATION_PLAN

Status: planning document. No file moves are authorized by this file alone.

## Migration Strategy

1. Freeze the public release target as allowlists, not broad folder moves.
2. Create product manifests from current paths.
3. Generate clean packages into `releases/` using dry-run scripts.
4. Only after verification, create a clean repo or clean subtrees.
5. Archive residue with dated folders and `MIGRATION_MAP.md`.

## Phases

### Phase A: Boundaries

- Approve `VISIBILITY_MATRIX.md`.
- Approve `PRIVATE_GAME_BOUNDARY.md`.
- Approve denylist.

### Phase B: Canonical Sources

- Choose canonical ClaudioOS blueprint source.
- Choose website source of truth.
- Choose open-source packages.
- Choose commercial app release roots.

### Phase C: Dry-Run Packages

- Run product manifest generation.
- Run secret scan.
- Run free-dev package dry-run.
- Run paid-app package dry-run.

### Phase D: Archive

Only after approval:

- Move caches/build outputs to `_archive/legacy/YYYY-MM-DD/` or delete if explicitly approved.
- Move duplicate blueprint copies after canonical source is chosen.
- Move old prompts and logs to archive indexes.

### Phase E: Clean Repo

Create clean public/commercial repos from manifests. Do not publish the dirty workspace.

## Human Review Required

- Licenses.
- Book/sample publication decisions.
- Game boundary.
- Gumroad product pricing and refund/legal policies.
- Any history rewrite for large Git objects.
