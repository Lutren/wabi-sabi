# RELEASE_CHECKLIST

Use this checklist for every release. No product is ready until all required items pass or are explicitly marked blocked.

## Global Gates

- [x] Product is classified in `VISIBILITY_MATRIX.md`.
- [x] Product has a manifest.
- [x] Product has README.
- [ ] Product has install instructions.
- [ ] Product has license decision or `LEGAL_REVIEW_REQUIRED`.
- [ ] Secret scan passes.
- [x] Private game paths are excluded.
- [x] Vendor and archive paths are excluded unless explicitly reviewed.
- [ ] Build command is documented.
- [x] Test or smoke command is documented.
- [x] Changelog entry exists.
- [x] Release notes generated.

## Open / Free Developer Release

- [ ] Contains only source/docs/templates intended for developers.
- [ ] Contains no books, paid PDFs, commercial installers, private lore, game assets, or secrets.
- [ ] License is explicit and copied from `LICENSES/MIT.txt` unless a package-specific review chooses otherwise.
- [x] Minimal tests run.
- [ ] Examples are sanitized.
- [ ] `THIRD_PARTY_NOTICES.md` exists, even if it says no bundled third-party code.

### Free-dev Batch 2026-05-01

- [x] `residueos`, `obsai-core`, `observacionismo-gate`, `claudio-os-blueprint` and `gemma-observacionismo-cleanup` have ZIPs under `releases/free-dev`.
- [x] Product allowlist secret scan passed with `count_reported=0`.
- [x] ZIP artifact secret scan passed with `count_reported=0`.
- [x] ZIP members match product manifests.
- [x] Python packages install from temporary extraction and pass import smoke.
- [x] `claudio-os-blueprint` has required docs in the extracted artifact.
- [x] Clean local Git staging repos exist under `publish_staging/open-dev`.
- [x] Staging repos have no remote configured.
- [x] Staging smoke passed from temporary copies.
- [x] Gated GitHub publisher dry-run passed with `external_actions_performed=false`.
- [ ] External publication target reviewed and approved by ActionGate.

### Free-dev Batch 2026-05-03

- [x] `residueos`, `obsai-core`, `observacionismo-gate`,
  `claudio-os-blueprint`, `gemma-observacionismo-cleanup`,
  `obs-safe-integration-kit` and `duat-genesis` have regenerated ZIPs under
  `releases/free-dev`.
- [x] Product allowlist secret scans passed with `count_reported=0`.
- [x] ZIP artifact secret scans passed with `count_reported=0`.
- [x] ZIP members match product manifests.
- [x] Python packages install from temporary extraction and pass import smoke.
- [x] Clean local Git staging repos already exist under `publish_staging/open-dev`.
- [x] Staging repos are clean; existing GitHub remotes are present only for
  already published targets.
- [x] Staging smoke passed from temporary copies.
- [x] Staging secret scan passed with `count_reported=0`.
- [x] GEODIA local intake tests tolerate cleaned `Downloads` sources without
  copying raw files.
- [x] External publication target reviewed and approved by ActionGate for the
  seven `open-dev` targets in this batch.
- [x] Host gate returned `APPROVE` during the 2026-05-03 execution window.
- [x] Gated GitHub publisher executed with
  `external_actions_performed=true`; all seven repos verified public by
  `gh repo view`.
- [ ] Workspace-wide publication remains blocked until the global legacy secret
  scan is remediated.

## GitHub Public Sanitized Release

- [x] Source came from curador ficha tecnica or allowlisted package.
- [x] `Downloads\r.txt` is classified as `USER_ASSERTED_SAFE_NON_BLOCKING`; it remains excluded from staging and public artifacts.
- [x] Repo has `README.md`, `LICENSE`, `CLAIMS.md`, `PRIVATE_EXCLUSIONS.md` and `SECURITY.md`.
- [x] Secret scan passes on staging repo.
- [x] Path scrub passes: no `C:\Users\L-Tyr`, OneDrive personal paths or `E:\` roots in public files unless intentionally redacted in docs.
- [x] Claims scan passes: no antigravity, proof of consciousness, solved physics/cosmology, medical claims or autonomous safety guarantees.
- [x] Examples use synthetic data only.
- [x] RPG, books, assets, prompts, sessions, tokens, vendors and zips are excluded.
- [x] ActionGate explicitly approves external push for the 2026-05-03 batch.
- [x] Public URL is verified after publication before claiming success.

### GitHub Public Sanitized Batch 2026-05-03

- [x] Eight staging repos exist under `publish_staging\github-public-sanitized`.
- [x] MIT license blockers were replaced with explicit MIT license text.
- [x] Focused staging secret scan passed with `count_reported=0`.
- [x] Gated dry-run passed with `external_actions_performed=false`.
- [x] Gated execute passed with `external_actions_performed=true`.
- [x] Public repos verified: `data-curation-observatory`, `residueos-core`,
  `ai-web-gateway-observacionista`, `obs-info-kernel-lite`,
  `observational-calibration-toolkit`, `duat-lab`, `neurostate-ui` and
  `la-biblioteca-de-alejandria`.
- [x] Existing remote divergence on `data-curation-observatory` was resolved
  by `git pull --rebase origin main`; no force-push was used.

## Commercial Release

- [ ] Product package contains only intended paid deliverables.
- [ ] App build tested on target platform.
- [ ] Source package excludes `node_modules`, `dist`, `build`, `release`, screenshots, logs and local caches.
- [x] EULA or `COMMERCIAL_LICENSE.md` exists.
- [x] `THIRD_PARTY_NOTICES.md` exists for npm/Python dependencies.
- [x] Support process draft exists in `CUSTOMER_SUPPORT_PLAN.md`; pilot/MVP intake is `medioevo.saga@gmail.com`, final branded alias optional.
- [x] Refund policy draft exists in `REFUND_POLICY_DRAFT.md`.
- [x] Privacy policy draft exists in `PRIVACY_POLICY_DRAFT.md`.
- [x] Terms draft exists in `TERMS_DRAFT.md`.
- [ ] Gumroad or website listing copy reviewed.
- [ ] Pricing and bundle included in catalog.
- [x] Legal docs are marked `LEGAL_REVIEW_REQUIRED`; final legal review remains blocked.
- [x] Commercial legal matrix exists at `docs\legal\COMMERCIAL_RELEASE_LEGAL_MATRIX_2026-05-01.md`.
- [x] Paid app deliverable boundary exists at `docs\product\paid-app-deliverable-boundary-2026-05-01.md`.
- [ ] Source ZIPs are not customer deliverables unless a reviewed source-access license/tier exists.

### FlujoCRM Local Source Package 2026-05-01

- [x] `package-lock.json` exists.
- [x] `npm run check` passes with main/preload smoke.
- [x] `npm audit --json` reports `total=0`.
- [x] Product secret scan passed with `count_reported=0`.
- [x] `release_manifests\flujocrm.json` has `blocked_count=0`.
- [x] Source ZIP exists at `releases\paid-apps\flujocrm.zip`.
- [x] ZIP artifact secret scan passed with `count_reported=0`.
- [x] Windows x64 QA installer exists at `apps\commercial\flujocrm\dist\FlujoCRM-Setup-1.0.0.exe`.
- [x] Windows installer artifact secret scan passed with `count_reported=0`.
- [x] Listing draft exists at `docs\product\flujocrm-listing-draft-2026-05-01.md`.
- [x] Clean install checklist exists at `docs\product\flujocrm-clean-install-checklist-2026-05-01.md`.
- [x] Standalone-first and Windows-first decision documented; `Pack Empresarial` and macOS can reopen later.
- [ ] Installer tested on clean Windows machine.
- [x] macOS `.dmg` excluded from the initial Windows-first release.
- [x] Code signing or explicit unsigned-install warning reviewed locally; `CUSTOMER_INSTALL_NOTES.md` and `installer\BUILD.md` document the unsigned pilot path, while legal/final checkout review remains blocked.
- [ ] Support/privacy/refund/terms finalized.

### Paid Apps Source ZIP Batch 2026-05-01

- [x] `argus-desktop.zip` generated under `releases\paid-apps`.
- [x] `asistente-negocio.zip` generated under `releases\paid-apps`.
- [x] `flujocrm.zip` generated under `releases\paid-apps`.
- [x] `mini-office.zip` generated under `releases\paid-apps`.
- [x] Each paid-app ZIP artifact secret scan passed with `count_reported=0`.
- [x] These ZIPs are documented as internal QA artifacts, not default customer deliverables.
- [ ] Customer-facing installers/apps are generated and tested before public sale.

### Wave FC Local Evidence Pack 2026-05-01

- [x] Evidence pack exists under `-=MEDIOEVO=-\-=LIBROS\claudio\runtime\wave_fc_client_demos\wave_fc_evidence_pack_2026-05-01`.
- [x] Demo inputs include synthetic `.md`, `.docx` and CSV only.
- [x] Focused Wave/Wabi suite passed with `61 passed`.
- [x] Release gate exists under `-=MEDIOEVO=-\-=LIBROS\claudio\runtime\wave_wabi_release_gates\wave_wabi_gate_2026-05-01`.
- [x] Release gate reports `local_demo_ready=true` and `public_publication_ready=false`.
- [x] Evidence pack and release gate secret scans passed with `count_reported=0`.
- [ ] DOCX visual render QA completed. Current host lacks `@oai/artifact-tool` and `soffice/libreoffice`.
- [x] Desktop/mobile captures generated under `qa_artifacts\2026-05-01-wave-fc-captures`; video remains optional.
- [ ] License/EULA, installation docs, landing copy and ActionGate approval completed before sale or publication.

## Books / Editorial Release

- [ ] Publication decision is explicit.
- [ ] Full book vs sample boundary is clear.
- [ ] Final manuscript validated.
- [ ] Cover and metadata present.
- [ ] Companion material separated.
- [ ] No private game lore leak.

## Private Game

- [ ] Not included in open packages.
- [ ] Not included in free dev releases.
- [ ] Not moved into public folders.
- [ ] Private builds are separate from public releases.
- [ ] Any commercial future release has its own review.
