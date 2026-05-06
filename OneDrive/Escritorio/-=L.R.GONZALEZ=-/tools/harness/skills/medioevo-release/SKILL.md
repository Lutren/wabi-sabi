---
name: medioevo-release
description: Local MEDIOEVO release-governance skill for public/private separation, secret scans, license posture, QA evidence, release manifests, packaging allowlists, and safe commits across the multi-root workspace.
---

# MEDIOEVO Release

Treat release as blocked until evidence proves otherwise. Never package by broad glob.

## Reads

- `AGENTS.md`, `COMMIT_PROTOCOL.md`, `RELEASE_CHECKLIST.md`, `RELEASE_READINESS_SCORE.md`, `VISIBILITY_MATRIX.md`, `PRIVATE_GAME_BOUNDARY.md`.
- `SECRET_SCAN_REPORT.md`, `RISK_REGISTER.md`, `PRODUCT_MAP.md`, `QA_RESULTS.md`, `RELEASE_EVIDENCE.md`.
- Product-specific manifests and package scripts only inside the selected lane.

## May Touch

- Root release docs, allowlists, denylist policy, QA reports, product manifests, release evidence docs, and non-destructive audit scripts under `tools/release`.
- Do not touch private game source, vendor trees, archive folders, build outputs, or unrelated product code.
- No usar git add .; use `git add -- <owned paths>` only from the correct repo, never from `C:\Users\L-Tyr`.

## Required Evidence

- `python tools/release/scan_secrets.py` before any release claim.
- Product tests/builds from the intended product root, for example Argus `npm run typecheck` and `npm run build`.
- Package manifest with allowlist, denylist, hashes, and private-game exclusion proof.

## ActionGate Blocks

Block and require ActionGate plus `host_observacionista` for publication, external distribution, upload, payment platform actions, release ZIP creation, license decision changes, or moving files between layers.
Block if host state is `JAMMING` or `BLOCK`.
