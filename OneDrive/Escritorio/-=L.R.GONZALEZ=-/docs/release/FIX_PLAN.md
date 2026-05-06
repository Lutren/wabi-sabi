# FIX_PLAN

## P0 Fixes

- [x] Enforce private game denylist in release scripts.
- [x] Enforce secrets denylist in release scripts.
- [x] Generate manifests before packages.
- [x] Avoid whole-workspace ZIPs.
- [x] Repair Argus lockfile enough for reproducible dry-run install and build checks.
- [x] Create final physical roots for open-dev, commercial apps, editorial and private game boundary.
- [x] Isolate Gemma + Observacionismo as public-safe MIT toolkit without Claudio runtime.

## P1 Fixes

- [x] Choose canonical blueprint copy for release lane: `packages\open-dev\claudio-os-blueprint`.
- [x] Choose website source of truth: `claudio\website` is canonical for `medioevo-site`; `claudio\apps\editorial_web` is legacy/experimental.
- [x] Create product READMEs.
- [x] Create smoke tests where missing for Hormiguero Mission Control public endpoints.
- [x] Convert Hormiguero Mission Control first screen into city viva/flipbook UI.

## P2 Fixes

- [x] Run product-specific tests.
- [x] Archive caches/build outputs with migration map through explicit script.
- [x] Split clean public packages into new roots.
- [x] Harden Argus QA against partial npm installs in OneDrive.
