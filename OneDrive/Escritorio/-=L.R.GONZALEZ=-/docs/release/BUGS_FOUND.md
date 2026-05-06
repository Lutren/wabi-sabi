# BUGS_FOUND

No runtime bugs were fixed in this pass.

Audit-level bugs/risks:

- root workspace lacks enforced package boundaries;
- secret files can be accidentally included in ZIPs;
- private game/TCG paths can be accidentally included without denylist;
- `mini_office` has placeholder test script;
- website source of truth is ambiguous;
- blueprint has multiple copies;
- large files appear in Git object history.

Fixed in this pass:

- `claudio\apps\argus_desktop\package-lock.json` was corrupted and blocked `npm ci` with invalid package names and integrity mismatches. The corrupt lockfile was archived and a clean lockfile was regenerated from `package.json`.

Additional fixed/contained in this pass:

- final public/commercial package roots did not exist as enforced physical boundaries; created `packages\open-dev`, `apps\commercial`, `books\editorial`, `game-private` and release lanes;
- Argus generated artifacts (`node_modules`, `dist`) are now controlled by an explicit archive script and denied by release tooling;
- Argus `npm ci` can produce partial installs in OneDrive (`ENOTEMPTY`, missing `.bin`); release QA now uses a temp cache plus `npm rebuild` through `tools\release\argus_release_check.py`;
- Hormiguero Mission Control first screen was still dashboard-shaped; replaced with a live GEODIA/Hormiguero city surface backed by real endpoints and offline fallback;
- Gemma + Observacionismo had no public-safe packaging boundary; created isolated MIT toolkit with synthetic fixtures only.
