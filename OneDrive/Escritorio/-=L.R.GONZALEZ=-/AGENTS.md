# AGENTS.md

Project root: `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-`

This workspace contains MEDIOEVO, Claudio, Observacionismo / PSI-IA, Brain OS tooling, commercial apps, editorial assets, websites, product bundles, vendors, local sessions, and a private game/TCG. Treat it as a multi-layer workspace, not as one public repo.

## Central Rule

Do not maximize changes. Maximize verified closure.

Los datos persisten. El operador no. Preserve intent through docs, tests, fingerprints and migration maps.

## Curador Always-On

Every agent in this workspace is also a curator. When encountering a broad,
dirty, duplicated or unknown repo/source/download/folder, do not leave it as
chat-only context and do not create orphan residue.

Before using, copying, extracting, publishing, archiving or discarding it:

1. Run or mentally apply the curator preflight:
   `python tools/release/curador_preflight.py --path <path>`.
2. Check whether it already has a ficha in `SOURCE_INTAKE_REGISTER.md`,
   `PRODUCT_MAP.md`, `VISIBILITY_MATRIX.md`, `RISK_REGISTER.md`,
   `DUPLICATES_AND_DEAD_CODE.md`, `DELETE_CANDIDATES.md`, Claudio
   `PENDIENTES_MASTER.md`, Claudio `NEXT_SESSION_BRIEF.md` or
   `docs/memoria_viva/fichas`.
3. If it has useful tech, extract the idea or minimal public-safe code into the
   proper lane with provenance, hash/test evidence and claim boundaries. Never
   copy a dirty repo wholesale into public/commercial packages.
4. If it is private, secret-like, paid-source, RPG/TCG, session state or raw
   personal context, mark the boundary and do not copy it into open lanes.
5. If it is not useful, document it in `DELETE_CANDIDATES.md` or the relevant
   archive/migration map. Actual deletion or movement still requires the
   cleanup gate and evidence.

The default state for undocumented material is `UNKNOWN_REVIEW_REQUIRED`, not
"safe", not "trash", and not "publishable".

Current global cleanup contract:
`docs/developer/CURADOR_SETO_GLOBAL_OPERATING_CONTRACT_2026-05-05.md`.
Use it for SETO folder vocabulary, `ObservationEnvelope`, `ActionGate`,
`WitnessLog`, agent COMMS and dry-run cleanup decisions.

## Pending Review Every Run

At the start of every session/day, refresh the pending-work snapshot before
choosing backlog-driven work:

```powershell
python tools\release\pending_review.py --write --quiet
```

This snapshot is evidence for triage, not permission to publish, push, deploy,
delete or mark tasks closed. Use it to answer "cuantos quedan" with current
counts, pick the shortest verified local closure first, and keep gated external
actions separated from local candidates. If the task is inside Claudio, the
equivalent wrapper is:

```powershell
python tools\pending_review.py --write --quiet
```

## Autonomy Continuation Law

Default behavior is continuous local execution, not repeated confirmation.

Agents must continue without asking "yes, continue" for local, reversible,
evidence-backed work: reading, tests, docs, adapters, local runtime artifacts,
workpack generation and append-only COMMS messages with `ObservationEnvelope`.

Stop, gate or ask only for high-blast-radius boundaries: external sending,
publication, push, deploy, Gumroad/social actions, secrets/credentials, private
game/TCG material, destructive delete/move/cleanup, model weights/aliases/training,
strong claims, or a genuinely human preference that cannot be discovered from
the repo.

For Claudio, the living policy is `core/local_autonomy.py` and the law id is
`LEY_CONTINUIDAD_AUTONOMA_LOCAL`.

## Required First Read

At the start of every session:

1. Inspect this root: `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-`.
2. Read this file.
3. Read the current audit docs:
   - `AUDIT_REPO_TREE.md`
   - `PRODUCT_MAP.md`
   - `VISIBILITY_MATRIX.md`
   - `RISK_REGISTER.md`
   - `SECRET_SCAN_REPORT.md`
   - `DUPLICATES_AND_DEAD_CODE.md`
   - `RELEASE_READINESS_SCORE.md`
4. If working inside `-=MEDIOEVO=-\-=LIBROS\claudio`, also read:
   - `CLAUDE.md`
   - `PENDIENTES_MASTER.md`
   - `NEXT_SESSION_BRIEF.md`

## Layers

### OPEN / Free Developer Tools

Candidates only after secret and license review:

- Claudio core pieces that are public-safe.
- Observacionismo / PSI-IA developer toolkit.
- Brain OS tooling and blueprints.
- Agent templates and Codex helper tools.
- Dev utilities that do not contain private assets or paid content.

### COMMERCIAL / Sellable Products

- MEDIOEVO apps.
- Productivity apps.
- Premium bundles.
- Companion PDFs.
- Gumroad and website products.
- Paid installers and release packages.

### BOOKS / CANON / EDITORIAL

- MEDIOEVO books.
- El Observador and Observacionismo essays.
- Narrative material.
- Companion docs.
- Editorial assets.

Do not publish full books or canon vaults unless explicitly instructed.

### PRIVATE / Game

The game and TCG source are private. This includes:

- `-=MEDIOEVO=-\-=LIBROS\metaevo-tcg\**`
- `-=MEDIOEVO=-\-=LIBROS\claudio\tcg\**`
- `-=MEDIOEVO=-\-=LIBROS\claudio\runtime\game_bridge\**`
- TCG/game builds, lore, private assets, bridge code, and internal release scripts.

Never move these paths into public folders. Never include them in open-source packages. Never include them in free developer releases.

### ARCHIVE / LEGACY / VENDOR

- `_archive`, `_ARCHIVAR`, `_legacy`, `archive`, `_trash_revisar`, `_SNAPSHOTS`.
- `.skills`, `github-modules`, `tools/vendor`, `tools/pentest_repos`.
- `.git`, `.claw`, `.claude`, `.wrangler`, `.test_*`, caches, logs.
- Build outputs: `dist`, `build`, `release`, `releases`, `target`, `node_modules`, `.venv*`, `__pycache__`.

Do not publish archive/vendor material by default.

## Safety Rules

- Do not delete files directly.
- If something looks disposable, list it in `DELETE_CANDIDATES.md` or move it to `_archive/` only with a migration map.
- Do not move or rename critical folders without updating `MIGRATION_MAP.md`.
- Do not touch private game paths unless explicitly authorized for private-boundary work.
- Do not include secrets, `.env`, tokens, API keys, sessions, local configs, or debug JSON in releases.
- Do not invent completion. A task is done only with evidence.
- Do not mark backlog items done from inference.
- Do not claim a product is ready to publish unless the release checklist passes.
- Do not change active repos while another agent may be working unless the file is clearly owned by this task.

## Secrets Policy

Public packages must exclude:

- `**/.env`
- `**/.env.*`
- `**/*secret*`
- `**/*token*`
- `**/*credential*`
- `**/settings.local.json`
- `**/.claw/**`
- `**/.claude/**`
- `**/.wrangler/**`
- `**/*gumroad*` unless explicitly selected and scrubbed
- `**/*stripe*` unless explicitly selected and scrubbed

Run `python tools/release/scan_secrets.py` before any release.

## License Policy

There is no global license decision for the entire workspace. Root `LICENSE` is intentionally marked `LEGAL_REVIEW_REQUIRED`.

Use per-layer decisions:

- OPEN packages may use MIT/Apache-2.0/other only after explicit review.
- COMMERCIAL products are proprietary unless stated otherwise.
- BOOKS/editorial material is all rights reserved unless explicit samples are approved.
- PRIVATE game is proprietary and not publishable.
- VENDOR material keeps its upstream license and must not be rebranded as MEDIOEVO-owned.

## Install Commands

Use commands from the specific product folder. Common candidates:

```powershell
cd "C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-"
python tools/release/audit_repo.py
python tools/release/scan_secrets.py
python tools/release/product_manifest.py
```

For Claudio runtime:

```powershell
cd "C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\claudio"
python -m pytest tests/ -x --quiet
```

For Argus desktop:

```powershell
cd "C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\claudio\apps\argus_desktop"
npm run typecheck
npm run build
```

## Test Commands

Run only in the intended product root:

- Python: `python -m pytest`
- Vite/TS: `npm run typecheck`, `npm run lint`, `npm run build`
- Rust: `cargo test`

If tests do not exist, report `NO_TEST_BASELINE` and add a minimal smoke test only if the task owns that product.

## Build Commands

Use product-specific build scripts. Do not run packaging scripts that create public bundles unless secret scan and visibility matrix are clean.

## Folder Conventions

Target structure:

```txt
apps/
packages/
books/
game-private/
docs/
tools/
website/
releases/
_archive/
```

This workspace has not yet been migrated to that structure. Follow `TREE_PLAN.md` and `MIGRATION_PLAN.md`.

## Naming Conventions

- Use lowercase kebab-case for new public package folders.
- Use `README.md`, `CHANGELOG.md`, `ROADMAP.md`, `RELEASE_CHECKLIST.md`.
- Use dated archive paths: `_archive/legacy/YYYY-MM-DD/<reason>/`.
- Use `PRIVATE`, `COMMERCIAL`, `OPEN`, `BOOKS_EDITORIAL`, `ARCHIVE`, `UNKNOWN_REVIEW_REQUIRED` classifications.

## PR / Change Policy

Before PR or push:

1. Check working tree.
2. List files changed by this task.
3. Run relevant tests or explain why not.
4. Verify secrets.
5. Verify private game is excluded.
6. Update migration maps if files moved.
7. Do not include unrelated user changes.

## Residue Reporting

Use:

- `RISK_REGISTER.md` for risks.
- `DUPLICATES_AND_DEAD_CODE.md` for duplication/dead-code observations.
- `DELETE_CANDIDATES.md` for things that may be removed later.
- `MIGRATION_MAP.md` for moves/renames.
- `DELETED_OR_ARCHIVED.md` for actual archival actions.

## Release Closure

A release is closed only when:

- product manifest exists;
- license is decided or marked `LEGAL_REVIEW_REQUIRED`;
- secret scan passes;
- private game boundary passes;
- tests/build/smoke checks pass or are explicitly blocked;
- package contents are generated from allowlist, not broad globs;
- final report lists files, commands, test results, risks, residue, and next tasks.
