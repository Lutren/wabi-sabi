# FlujoCRM

Classification: `COMMERCIAL`

Current path: `apps\commercial\flujocrm`

Legacy/source-of-history path: `-=MEDIOEVO=-\-=LIBROS\claudio\products\crm`

Status 2026-05-06: `FOUNDER_ACCESS_SQLITE_QA_PASS / CLEAN_MACHINE_QA_PENDING / PUBLICACION_BLOCK`

Commercial positioning: standalone first, bundle later. The local source ZIP is
an internal QA artifact, not a default customer deliverable.

Release decision: FlujoCRM ships Windows x64 first. No `.dmg` is part of the
initial release unless the commercial target changes to macOS.

Closed locally:

- lockfile created;
- `npm run check` passes with main/preload/renderer smoke;
- `npm run smoke:e2e-storage` passes after `npm run pack-win-qa`;
- production and full npm audit report `0` vulnerabilities;
- product secret scan `count_reported=0`;
- source package generated at `releases\paid-apps\flujocrm.zip`;
- artifact secret scan `count_reported=0`.
- Windows x64 QA installer generated at `apps\commercial\flujocrm\dist\FlujoCRM-Setup-1.0.0.exe`;
- installer artifact secret scan `count_reported=0`;
- installer and unpacked app are `NotSigned`.
- installed Electron builds use SQLite through IPC;
- standalone HTML preview uses browser storage only as fallback.

Detected scripts:

- `npm run start`
- `npm run check`
- `npm run build-win`
- `npm run build-win-qa`
- `npm run build-mac`
- `npm run pack`
- `npm run pack-win-qa`
- `npm run smoke:e2e-storage`

Before release:

- test real Electron install on clean Windows;
- verify data storage/privacy;
- create final icons/code signing plan;
- finalize support/privacy/refund/terms from the gated legal drafts;
- keep source ZIP private unless a separate reviewed license/tier explicitly sells it;
- do not publish until commercial checklist and ActionGate pass.

Current evidence:

- `docs\product\flujocrm-lane-unification-2026-05-06.md`
- `docs\product\flujocrm-release-evidence-2026-05-02.md`
- `docs\product\flujocrm-sqlite-storage-evidence-2026-05-02.md`
- `docs\product\flujocrm-current-user-install-qa-2026-05-02.md`

Historical evidence:

- `docs\product\legacy\FLUJOCRM_RELEASE_LOCAL_EVIDENCE_2026-05-01.md`
- `docs\product\legacy\FLUJOCRM_WINDOWS_INSTALLER_QA_2026-05-01.md`
- `docs\product\paid-app-deliverable-boundary-2026-05-01.md`
- `docs\product\flujocrm-windows-first-release-decision-2026-05-01.md`
- `docs\product\flujocrm-listing-draft-2026-05-01.md`
- `docs\product\flujocrm-clean-install-checklist-2026-05-01.md`
- `release_manifests\flujocrm.json`
