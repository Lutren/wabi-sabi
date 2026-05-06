# FlujoCRM SQLite Storage Evidence - 2026-05-02

Status: `SQLITE_STORAGE_QA_PASS / CLEAN_MACHINE_QA_PENDING / CHECKOUT_BLOCKED`

This closes the previous UI/storage contract blocker for FlujoCRM. The installed
Electron app now uses SQLite through the preload IPC bridge. The standalone HTML
preview keeps `localStorage` only as a non-installed preview fallback.

## Implementation

- `main.js` supports isolated QA data directories through
  `FLUJOCRM_USER_DATA_DIR`.
- `main.js` supports an E2E-only debug port through `FLUJOCRM_E2E_PORT`.
- `contacts` SQLite schema now includes:
  - `stage`
  - `value`
  - `last_activity`
- Existing DBs are migrated with `ALTER TABLE` when those columns are missing.
- `mockup.html` detects `window.api.contacts` and uses IPC for:
  - create contact
  - update contact
  - delete contact
  - drag/drop stage updates
  - demo-data loading
- `mockup.html` uses bundled Chart.js:
  `./node_modules/chart.js/dist/chart.umd.js`.
- Browser fallback remains available only when `window.api` is absent.

## Tests

```txt
npm run check
flujocrm main smoke passed
flujocrm preload smoke passed
flujocrm renderer smoke passed

npm audit --omit=dev --audit-level=high
found 0 vulnerabilities

npm run smoke:e2e-storage
flujocrm e2e storage smoke passed
```

The E2E smoke launches the built app with a temporary user-data directory,
connects through the Electron debug port, runs `loadDemo()` in the renderer and
then inspects the generated SQLite DB.

Verified SQLite result:

- Contacts persisted: `15`.
- Total value persisted: `958000`.
- Required columns present: `stage`, `value`, `last_activity`.

The same E2E smoke also passed against the installed executable:

- `C:\Users\L-Tyr\AppData\Local\Programs\FlujoCRM\FlujoCRM.exe`

## Final Installer Evidence

Evidence folder:

- `qa_artifacts/flujocrm_sqlite_install_2026-05-02/`

Installer:

- Path: `apps\commercial\flujocrm\dist\FlujoCRM-Setup-1.0.0.exe`
- Bytes: `103743584`
- SHA256: `f7ffa5a513207b15f81778a1e524eff110ff0ea638b893d15e44cd8d88e513c1`
- Signature: `NotSigned`

Unpacked executable:

- Path: `apps\commercial\flujocrm\dist\win-unpacked\FlujoCRM.exe`
- Bytes: `223117824`
- SHA256: `7f26d6af4808c7c2fea90e0a3625f99582875c3c7bf32e181868fab3d255a320`
- Signature: `NotSigned`

Source ZIP:

- Path: `releases\paid-apps\flujocrm.zip`
- Bytes: `101781`
- SHA256: `39b40abbedef13e6561beadf0a95ba4f1f546f9bed4a7c9808ecd2be40029a76`

Secret scans:

- Product scan: `count_reported=0`.
- Source ZIP scan: `count_reported=0`.
- Installer scan: `count_reported=0`.

Customer pilot copy:

- `apps\commercial\flujocrm\CUSTOMER_INSTALL_NOTES.md`
- `docs\product\flujocrm-legal-support-copy-2026-05-02.md`

## Install QA

Current-user install pass:

- Silent install exit code: `0`.
- Installed executable launched and responded.
- Main window title: `FlujoCRM - Tu negocio, organizado`.
- DB initialized at:
  `C:\Users\L-Tyr\AppData\Roaming\FlujoCRM\data\flujocrm.db`.
- DB columns include `stage`, `value`, `last_activity`.
- Screenshot:
  `qa_artifacts/flujocrm_sqlite_install_2026-05-02/flujocrm-installed-launch-desktop.png`.
- Installed-exe E2E storage smoke passed with an isolated profile.
- Silent uninstall exit code: `0`.
- Install directory, shortcuts and uninstall registry entry were removed.
- `%APPDATA%\FlujoCRM` remained as user data.

## Decision

The UI/storage contract is closed for the Windows QA build.

FlujoCRM remains `FOUNDER_ACCESS`, not `BUY_NOW`, until:

- clean Windows machine QA passes;
- unsigned-installer warning or code signing is resolved;
- support/refund/privacy/terms copy is final;
- public checkout is verified after the final artifact hash is frozen.
