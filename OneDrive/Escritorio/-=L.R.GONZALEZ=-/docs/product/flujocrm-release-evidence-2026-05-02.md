# FlujoCRM Release Evidence - 2026-05-02

Status: `FOUNDER_ACCESS_SQLITE_STORAGE_QA_PASS / DO_NOT_PUBLISH_CHECKOUT`

FlujoCRM improved from commercial review to a current-user Windows install QA
pass with verified SQLite storage from the installed UI, but it is still not
`BUY_NOW` because clean-machine QA, code-signing or unsigned-installer copy, and
legal/support final copy are not complete.

## Source cleanup

- Rewrote corrupted human docs:
  - `apps\commercial\flujocrm\BUSINESS.md`
  - `apps\commercial\flujocrm\installer\BUILD.md`
- Fixed demo/source corruption:
  - `index.html`: `.foreach(...)` -> `.forEach(...)`
  - `mockup.html`: checkbox/checked/delete tokens repaired
  - `main.js`: SQL keyword casing normalized without behavior change
- Fixed installed-app launch target after QA found a placeholder screen:
  - `main.js` now loads `mockup.html`, the complete standalone CRM UI.
  - `package.json` includes `mockup.html` in Electron build files.
  - `scripts/smoke-main.cjs` asserts the complete QA UI is loaded.
  - `index.html` now redirects to `mockup.html` instead of keeping a misleading
    placeholder page.
  - `main.js` shows the window after `did-finish-load` to avoid a blank
    first-paint window during install QA.
- Closed the UI/storage contract:
  - `mockup.html` now uses `window.api.contacts` in Electron.
  - Browser `localStorage` is retained only as standalone preview fallback.
  - Chart.js is bundled locally instead of loaded from CDN.
  - `main.js` migrates existing SQLite DBs with `stage`, `value` and
    `last_activity`.
  - `scripts/e2e-storage-smoke.cjs` verifies renderer-to-SQLite persistence.
- Remaining corruption scan for the product source only finds the smoke-test
  assertion string that checks `.foreach(` is absent.

## Validation

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

Secret scans:

- Product scan: `count_reported=0`.
- Source ZIP artifact scan: `count_reported=0`.
- Windows installer artifact scan: `count_reported=0`.

## Artifacts

Source ZIP:

- Path: `releases\paid-apps\flujocrm.zip`
- Bytes: `101781`
- SHA256: `39b40abbedef13e6561beadf0a95ba4f1f546f9bed4a7c9808ecd2be40029a76`
- Source package only; not the default customer deliverable.

Windows QA installer:

- Path: `apps\commercial\flujocrm\dist\FlujoCRM-Setup-1.0.0.exe`
- Bytes: `103743584`
- SHA256: `f7ffa5a513207b15f81778a1e524eff110ff0ea638b893d15e44cd8d88e513c1`
- Signature: `NotSigned`
- Rebuilt after installed-UI fix on 2026-05-02.

Unpacked executable:

- Path: `apps\commercial\flujocrm\dist\win-unpacked\FlujoCRM.exe`
- Bytes: `223117824`
- SHA256: `7f26d6af4808c7c2fea90e0a3625f99582875c3c7bf32e181868fab3d255a320`
- Signature: `NotSigned`

Release manifest:

- Path: `release_manifests\flujocrm.json`
- Regenerated with hashes after the installed-UI fix.

## Install QA

Detailed evidence:

- `docs/product/flujocrm-current-user-install-qa-2026-05-02.md`
- `docs/product/flujocrm-sqlite-storage-evidence-2026-05-02.md`
- `qa_artifacts/flujocrm_sqlite_install_2026-05-02/`

Result:

- first attempt installed but opened a placeholder UI, so it was blocked;
- after the fix, silent install exited `0`;
- desktop and Start Menu shortcuts were created;
- installed app launched with window title
  `FlujoCRM - Tu negocio, organizado`;
- screenshot shows the complete dashboard UI;
- intermediate blank-window capture was fixed by delaying `show()` until
  `did-finish-load`;
- SQLite DB was initialized under `%APPDATA%\FlujoCRM\data\flujocrm.db`;
- installed DB has `stage`, `value` and `last_activity` columns;
- E2E storage smoke passed against the installed `.exe` with an isolated QA
  profile and persisted 15 demo contacts to SQLite;
- pilot customer install/support/refund/privacy copy was drafted in
  `CUSTOMER_INSTALL_NOTES.md`;
- silent uninstall exited `0`;
- after a follow-up wait, install directory, shortcuts and uninstall registry
  entry were removed;
- `%APPDATA%\FlujoCRM` remained as user data.

Storage note: installed Electron builds use SQLite through IPC. Standalone HTML
preview fallback uses browser `localStorage`.

## Decision

`FOUNDER_ACCESS` remains correct.

FlujoCRM can be offered by contact to a small founder/pilot group only if the
operator manually explains:

- Windows-first scope;
- local-first data behavior;
- unsigned installer warning;
- support/refund limits;
- clean-install QA is still pending.

Do not create or publish a Gumroad checkout until:

- clean Windows machine install checklist passes;
- uninstall behavior is recorded;
- legal review approves privacy/refund/terms/support copy;
- public listing includes unsigned installer wording or the app is signed;
- the final customer artifact hash is verified after any rebuild.
