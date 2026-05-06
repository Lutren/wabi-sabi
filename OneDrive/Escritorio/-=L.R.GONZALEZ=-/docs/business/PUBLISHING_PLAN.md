# PUBLISHING_PLAN

Status: GitHub/Gumroad publication runs executed with evidence through 2026-05-03.

## 2026-05-02 Decision

The publication direction is `OPEN_SOURCE_MAX / PATRIMONY_GUARD`:

- publish public-safe tools, docs, templates, schemas and synthetic fixtures;
- keep family patrimony in books, RPG, assets, commercial packs, support, hosted services and brand;
- never publish raw workspace folders, raw Downloads texts or E: roots;
- never push externally until secret scan, path scrub, claims scan and ActionGate pass.
- use `open core + UI paga`: GitHub receives public-safe cores and whitepapers;
  Gumroad/website sell app wrappers, agent UIs, premium templates, support and
  installers.
- publish agents one by one, never the full workspace.

## Sequence

1. Freeze private game boundary.
2. Clean first open developer package.
3. Clean first commercial app package.
4. Publish website landing updates only after content-token checks.
5. Publish Gumroad products only after package manifest and upload verification.
6. Add Buy Me a Coffee support tiers after public page copy is reviewed.

## Free Developer Lane

First clean local batch, generated 2026-05-01:

1. `residueos` -> `releases\free-dev\residueos.zip`
2. `obsai-core` -> `releases\free-dev\obsai-core.zip`
3. `observacionismo-gate` -> `releases\free-dev\observacionismo-gate.zip`
4. `claudio-os-blueprint` -> `releases\free-dev\claudio-os-blueprint.zip`
5. `gemma-observacionismo-cleanup` -> `releases\free-dev\gemma-observacionismo-cleanup.zip`
6. `obs-safe-integration-kit` -> `releases\free-dev\obs-safe-integration-kit.zip`
7. `duat-genesis` -> `releases\free-dev\duat-genesis.zip`

Evidence:

- product manifests in `release_manifests\`;
- `qa_artifacts\release_validation\free-dev-smoke.json`;
- `qa_artifacts\release_validation\free-dev-github-dry-run.json`;
- source and ZIP secret scans passed with `count_reported=0`;
- install/extraction smoke passed.
- `obs-safe-integration-kit`: source smoke passed, ZIP hash `e6b5225cd0337789f1ed95c5ec569267b1b1179a3301c53ae496380b79c5f64d`, ZIP smoke OK, source/ZIP/staging secret scans `count_reported=0`, and local staging repo `publish_staging\open-dev\obs-safe-integration-kit` is clean with no remote.
- `duat-genesis`: tests `3 passed`; manifest `release_manifests\duat-genesis.json` has `11` files and `0` blocked; ZIP hash `f672d974d88c3190699ea16caad04b8a6de9839f20aa9513cfd7fdf51c0cbb44`; ZIP smoke OK; source/ZIP/staging secret scans `count_reported=0`; staging repo `publish_staging\open-dev\duat-genesis` is clean at commit `3488b49`; published and verified public at `https://github.com/Lutren/duat-genesis`.

Required docs:

- README.
- LICENSE.
- install/test/build commands.
- examples.
- security notes.

External publication next gate:

- choose destination per product, for example GitHub repo, release attachment or package index;
- review README/claims one final time;
- verify no account token is used from this workspace without ActionGate;
- upload manually or through a gated script;
- verify public URL after upload before claiming published.

Current external gate result:

- Owner override with evidence was applied only to host-gate `REVIEW`; secret, path, claim, license and private-boundary gates remained hard blockers.
- Published and verified public on GitHub:
  - `https://github.com/Lutren/obs-safe-integration-kit`
  - `https://github.com/Lutren/obsai-core`
  - `https://github.com/Lutren/residueos`
  - `https://github.com/Lutren/observacionismo-gate`
  - `https://github.com/Lutren/claudio-os-blueprint`
  - `https://github.com/Lutren/gemma-observacionismo-cleanup`
  - `https://github.com/Lutren/duat-genesis`
- 2026-05-03 evidence:
  - `qa_artifacts\release_validation\free-dev-smoke.json`
  - `qa_artifacts\release_validation\free-dev-staging-smoke.json`
  - `qa_artifacts\release_validation\free-dev-github-publish.json`
  - `qa_artifacts\release_validation\github-publication-live-verification-2026-05-03.json`
- Live verification evidence: `qa_artifacts\release_validation\publication-live-verification-2026-05-02.json`.
- DUAT publication evidence: `qa_artifacts\release_validation\duat-publication-live-verification-2026-05-02.json`.
- Host disk offload moved selected large/generated artifacts to `E:\MEDIOEVO_OFFLOAD\2026-05-01-host-gate`; evidence is `qa_artifacts\release_validation\host-gate-offload-2026-05-01.json`.
- Current direct host gate after offload remains `REVIEW`: `disk_pct=84.9`, `disk_free_mb=34031.32`, `lambda_sat=0.849`.
- Current direct host gate on 2026-05-02 no-write check is `REVIEW`: `memory_pct=82.5`, `disk_pct=83.3`, `lambda_sat=0.833`; no external publication until host gate is `APPROVE`.
- Current direct host gate during the 2026-05-03 GitHub execution window returned
  `APPROVE` (`disk_pct=82.6`, `lambda_sat=0.826`), and ActionGate approved the
  target-specific GitHub actions. This does not override the global workspace
  secret-scan block.
- Future external publication still requires the same package-specific evidence and cannot rely on this override as a blanket approval.

## New Public Sanitized Lane

Queue status:

1. `obs-safe-integration-kit` -> published in the `open-dev` lane.
2. `data-curation-observatory` -> `https://github.com/Lutren/data-curation-observatory`
3. `residueos-core` -> `https://github.com/Lutren/residueos-core`
4. `ai-web-gateway-observacionista` -> `https://github.com/Lutren/ai-web-gateway-observacionista`
5. `obs-info-kernel-lite` -> `https://github.com/Lutren/obs-info-kernel-lite`
6. `observational-calibration-toolkit` -> `https://github.com/Lutren/observational-calibration-toolkit`
7. `duat-genesis` -> published in the `open-dev` lane.
8. `duat-lab` -> `https://github.com/Lutren/duat-lab`
9. `neurostate-ui` -> `https://github.com/Lutren/neurostate-ui`
10. `la-biblioteca-de-alejandria` -> `https://github.com/Lutren/la-biblioteca-de-alejandria`

Each repo must ship with:

- `README.md`;
- `LICENSE`;
- `CLAIMS.md`;
- `PRIVATE_EXCLUSIONS.md`;
- `SECURITY.md`;
- tests or reproducible demo;
- synthetic fixtures only.

Current published evidence:

- eight local repos exist under `publish_staging\github-public-sanitized`;
- MIT license blockers were removed from sanitized skeletons;
- `duat-genesis` is a real free-dev package in `publish_staging\open-dev\duat-genesis`; older lab-skeleton language should not be used for the public repo;
- `duat-lab` and `neurostate-ui` remain sanitized skeletons;
- focused staging secret scan reports `count_reported=0`;
- evidence: `qa_artifacts\release_validation\github-public-sanitized-staging.json`.
- execution evidence: `qa_artifacts\release_validation\github-public-sanitized-publish.json`.
- live verification evidence: `qa_artifacts\release_validation\github-publication-live-verification-2026-05-03.json`.
- Published and verified public on GitHub:
  - `https://github.com/Lutren/data-curation-observatory`
  - `https://github.com/Lutren/residueos-core`
  - `https://github.com/Lutren/ai-web-gateway-observacionista`
  - `https://github.com/Lutren/obs-info-kernel-lite`
  - `https://github.com/Lutren/observational-calibration-toolkit`
  - `https://github.com/Lutren/duat-lab`
  - `https://github.com/Lutren/neurostate-ui`
  - `https://github.com/Lutren/la-biblioteca-de-alejandria`

External publication for this batch is complete. New repos or updates still
require repo-specific secret scan, path scrub, claims scan and ActionGate.
`Downloads\r.txt` is `USER_ASSERTED_SAFE_NON_BLOCKING`, but remains excluded
from staging.

## Commercial Lane

Canonical runbook: `docs\publishing\OPEN_CORE_UI_PAID_PUBLICATION_RUNBOOK_2026-05-02.md`.

Published paid products:

- `MEDIOEVO Agent Ops Pack`: `https://lrgonzalez.gumroad.com/l/medioevo-agent-ops-pack`
- Price: USD 29.00.
- Artifact: `releases\paid\medioevo-agent-ops-pack.zip`.
- SHA256: `7cf8fdf5c8da49d691947becebdd3feae5f93b7e062212af38e3063404fab948`.
- Gumroad API verified `published=true`; public URL returned HTTP `200`.
- Evidence: `qa_artifacts\release_validation\gumroad-medioevo-agent-ops-pack.json` and `qa_artifacts\release_validation\publication-live-verification-2026-05-02.json`.
- `DUAT Templates`: `https://lrgonzalez.gumroad.com/l/duat-templates`
- Price: USD 19.00.
- Artifact: `releases\paid\duat-templates.zip`.
- SHA256: `03c926b549307ef6106d80117183bb22121354671a10e0f2527473c06f6ca518`.
- Gumroad API verified `published=true`; public URL returned HTTP `200`.
- Evidence: `qa_artifacts\release_validation\gumroad-duat-templates.json` and `qa_artifacts\release_validation\duat-publication-live-verification-2026-05-02.json`.

Commercial app-agent matrix:

- Canonical status file: `docs\product\COMMERCIAL_AGENT_PUBLICATION_MATRIX_2026-05-02.md`.
- Only `MEDIOEVO Agent Ops Pack` is `BUY_NOW`.
- FlujoCRM, Asistente Negocio and Writer Workbench are `FOUNDER_ACCESS`
  until package-specific QA/legal/support/installer evidence exists. FlujoCRM
  now has current-user install/launch/uninstall QA and SQLite storage E2E, but
  still needs clean-VM QA and final legal/support wording before checkout.
  Asistente Negocio now has Windows current-user install/E2E/uninstall QA, but
  still needs clean-VM QA, final legal review and signing/unsigned decision
  before checkout. Its install notes and support/privacy/refund text are draft
  artifacts, not legal approval.
- Mini Office is `FOUNDER_ACCESS_REVIEW`: runtime/test evidence exists and
  copy/claims/license/install scripts were cleaned on 2026-05-02, but it still
  needs legal, clean-machine, final package and checkout evidence.
- Wave, DUAT, OMNIS and NEUROSTATE remain lab/pilot surfaces with low-claim copy.

First candidates:

1. FlujoCRM + Asistente clean-VM, unsigned/signing and legal/support closure.
2. Mini Office legal/clean-machine/final package cleanup.
3. Writer Workbench.
4. Companion PDFs.

Required docs:

- Product catalog.
- Gumroad listing.
- customer support.
- refund draft.
- privacy draft.
- terms draft.
- release checklist.

## Website Lane

Use the website as the official hub:

- one products page;
- one free dev tools page;
- one books/samples page;
- one support page;
- one private game teaser only if approved, with no source/assets.

2026-05-02 website update:

- added `-=MEDIOEVO=-\-=LIBROS\claudio\website\agent-ops-pack.html`;
- linked the Gumroad product from `pricing.html`;
- added `agent-ops-pack.html` to `sitemap.xml`;
- verified sitemap XML parses and referenced local visual asset exists.
- published DUAT Genesis listing in `software.html`, `apps.html` and the home.
- published DUAT Templates link in `apps.html` and the home.
- deployed to Cloudflare Pages project `medioevo-site`, production branch `main`.
- Live URLs verified HTTP `200`: `https://medioevo.space/`,
  `https://medioevo.space/software.html`, `https://medioevo.space/apps.html`.
- Evidence: `qa_artifacts\release_validation\duat-publication-live-verification-2026-05-02.json`.

## Do Not Publish

- `metaevo-tcg`.
- TCG source/assets.
- private game bridge.
- full books unless explicitly approved.
- secrets.
- vendors and pentest repos.
