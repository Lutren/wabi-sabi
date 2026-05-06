# DEBUG_REPORT

Status: Fase 5 debug/release-readiness pass complete.

## Findings

- Workspace is not one clean repo; it is a multi-root product workspace.
- Secret candidates remain present locally. Public release is blocked.
- Private game/TCG paths were identified and denied from public package scripts.
- Build outputs and archives remain mixed with source in legacy product folders.
- `argus_desktop/package-lock.json` was corrupted and blocked `npm ci`.
- `_archive` initially slowed full scans after generated artifacts were moved
  there; release tools now exclude `_archive` and `_ARCHIVAR` by default.

## Fixes Applied

- Archived corrupt Argus lockfile before regeneration.
- Regenerated clean Argus lockfile from `package.json`.
- Verified Argus install dry-run, typecheck, build and npm audit.
- Archived generated Argus `node_modules` and `dist` outputs.
- Added `_archive` and `_ARCHIVAR` to release-tool denylist.
- Updated `audit_repo.py` to respect the common denylist unless
  `--include-denied` is passed.

## Remaining Blockers

- Secrets require review/rotation/exclusion.
- Commercial apps need manual QA, screenshots, support/legal docs approved.
- Open-source candidates need final license review.
- Private MetaEvo/TCG must remain excluded from public release jobs.
