---
name: argus-ops
description: Local Argus operations skill for OneDrive-safe install/build verification, Electron/Vite/PWA dependency checks, UX/public-safe audits, and commercial/internal release evidence for Argus desktop.
---

# Argus Ops

Argus is a commercial/internal app lane. Verify the installed runtime shape; do not trust nominal install success.

## Reads

- Argus app root, usually `apps/commercial/argus-desktop` or legacy `-=MEDIOEVO=-\-=LIBROS\claudio\apps\argus_desktop`.
- `PRODUCT_MAP.md`, `VISIBILITY_MATRIX.md`, `RISK_REGISTER.md`, `QA_RESULTS.md`, `RELEASE_EVIDENCE.md`.
- Package files and release runner scripts in the selected Argus root.

## May Touch

- Argus source/config/tests/docs inside the selected Argus root and matching QA evidence docs.
- Do not touch unrelated Claudio runtime, private game source, or generated `dist`/`node_modules` except through product-owned install/build commands.
- No usar git add .; stage only explicit Argus-owned paths.

## Required Evidence

- Verify binaries after install: `node_modules/.bin/tsc`, `node_modules/.bin/vite`.
- Verify PWA/PostCSS dependencies: `workbox-build` and `caniuse-lite/dist/unpacker/agents`.
- Run `npm run typecheck`, `npm run build`, and `npm audit --omit=dev --audit-level=high` where applicable.

## ActionGate Blocks

Require ActionGate plus `host_observacionista` for signing, uploading, publishing installers, opening authenticated services, changing telemetry, or broad dependency installs outside the selected root.
Block if host state is `JAMMING` or `BLOCK`.
