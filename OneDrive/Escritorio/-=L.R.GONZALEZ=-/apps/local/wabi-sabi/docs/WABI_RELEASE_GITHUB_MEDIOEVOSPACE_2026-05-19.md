# WABI Release GitHub + medioevo.space Check - 2026-05-19

Fingerprint: `WABI_ASSETS_RELEASE_20260519`

## Owner Authorization

The owner authorized GitHub and medioevo.space update only after local work passes QA and release checks. This does not bypass gates.

## Current Release Decision

- GitGate: `REVIEW_BLOCKED`
- DeployGate: `REVIEW_BLOCKED`
- PublicationGate: `REVIEW_BLOCKED_UNTIL_PUBLIC_SAFE_PROVENANCE`

No commit, push or deploy was executed in this phase.

## Final QA Evidence

- Local UI URL verified: `http://127.0.0.1:8787/` -> HTTP `200`.
- UI server PID after restart: `2176`.
- Operational workbench reports `ui.theme=wabi_du_wabi_20260519`, manifest `assets/wabi_du_wabi_20260519/ASSET_MANIFEST_20260519.json`, `external_assets=false`.
- Visual evidence: `C:\Users\L-Tyr\.medioevo\wabi\runtime\outputs\ui_assets_du_wabi_20260519\wabi_ui_du_wabi_assets_gate_preview.png`.
- Browser report: `C:\Users\L-Tyr\.medioevo\wabi\runtime\outputs\ui_assets_du_wabi_20260519\wabi_ui_du_wabi_assets_browser_report.json`.
- Focal BRAIN_OS: `250 passed in 369.44s`.
- Focal Wabi: `52 passed in 57.49s`.
- Wabi regression: `362 passed in 461.37s`.
- BRAIN_OS regression: `760 passed in 392.89s`.
- Py compile: PASS.
- Focal secret-like scan on integrated assets/docs: `0` findings.
- Boundary scan on UI/asset manifest: PASS for private path patterns.
- Cloud live: not called.
- BrowserBridge live: not activated.
- graphics_live: false.
- Apply: still blocked by Gate Preview.

## Repo/Pipeline Check

- BRAIN_OS/Wabi UI changes are under the broad host repo root `C:\Users\L-Tyr`, which has unrelated dirty state. This blocks a safe commit from that root.
- Host git excludes `OneDrive/Escritorio/*` through `.git/info/exclude`, so the BRAIN_OS UI asset files are not a clean tracked release delta by default.
- `publish_staging/medioevo-site` is a separate clean repo with remote `https://github.com/Lutren/medioevo-site.git`; it contains `CNAME=medioevo.space`, `netlify.toml` and `wrangler.jsonc`.
- `publish_staging/medioevo-duat-public-release` is a separate clean repo with remote `https://github.com/Lutren/medioevo-duat-public-release.git`.
- No files were staged into either public repo in this phase.
- Public repo code includes publishable/anon key-like strings that require explicit review before deploy scans are considered release-ready. Values were not printed.

## Why External Release Is Blocked

1. The exact asset source path returned `NEEDS_FICHA_BEFORE_USE` from `curador_preflight.py`.
2. A prior related ficha for `POST\Assets Du WABI` states `RuntimeImportGate=BLOCK`, `PublicationGate=BLOCK`, `RawAdoption=BLOCK` until provenance review.
3. The selected assets are metadata-clean and visually suitable, but the release-ready provenance/license note is still missing.
4. The broader workspace and nested repos are dirty. GitGate requires path-scoped staging and exact remote/domain confirmation before any commit/push.
5. medioevo.space pipeline must be detected from the correct repo before deploy; no deploy command was run.

## Local Integration Completed

The local Wabi UI now uses a controlled, re-encoded subset:

- `duat-control-surface.png`
- `image-reactor-workstation.png`
- `tool-forge-gate.png`
- `causal-frame-orb-v2.png`

All are under:

`C:\Users\L-Tyr\OneDrive\Escritorio\-= BRAIN_OS =-\apps\local\wabi_ui\assets\wabi_du_wabi_20260519\`

No raw ZIPs, vaults, prompts, datasets or archives were copied.

## Required Before GitHub Push

1. Confirm target repo for Wabi UI and/or medioevo site.
2. Confirm remote URL and branch.
3. Confirm selected assets have public-safe provenance.
4. Stage only path-scoped files related to this release.
5. Run focal and regression tests.
6. Run secret/path scan on staged diff.
7. Confirm no unrelated worktree changes enter the commit.

## Required Before medioevo.space Deploy

1. Identify real deployment pipeline for medioevo.space.
2. Confirm domain is exactly `medioevo.space`.
3. Build local public output from the correct source.
4. Run public/private boundary scan on build output.
5. Verify HTTP routes after deploy.

## Current Next Safe Action

Owner review of the four selected asset candidates:

- confirm they are generated/owned/licensed for public use;
- confirm they can be used on GitHub and medioevo.space;
- confirm no image should be excluded.

Until then, publication remains blocked and local UI integration remains the safe stopping point.
