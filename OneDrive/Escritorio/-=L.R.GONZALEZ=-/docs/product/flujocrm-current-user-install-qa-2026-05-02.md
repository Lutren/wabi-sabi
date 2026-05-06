# FlujoCRM Current-User Install QA - 2026-05-02

Status: `SUPERSEDED_BY_SQLITE_STORAGE_QA / CLEAN_MACHINE_QA_PENDING / CHECKOUT_BLOCKED`

This is a current-user Windows QA pass on the operator machine. It is not a
clean VM pass and does not authorize a public Gumroad checkout.

## First Attempt

The first rebuilt installer installed and launched, but opened `index.html`,
which was only a placeholder message. That attempt was marked
`BLOCK_UI_PLACEHOLDER`.

Evidence:

- `qa_artifacts/flujocrm_current_user_install_2026-05-02/install-result.json`
- `qa_artifacts/flujocrm_current_user_install_2026-05-02/launch-result.json`
- `qa_artifacts/flujocrm_current_user_install_2026-05-02/flujocrm-installed-launch-desktop.png`

## Fix Applied

- `main.js` now loads `mockup.html`, the complete standalone CRM UI.
- `package.json` includes `mockup.html` in the Electron build files.
- `scripts/smoke-main.cjs` asserts that the complete QA UI is loaded.
- `index.html` now redirects to `mockup.html`, removing the misleading
  placeholder page from the package.
- `main.js` shows the window after `did-finish-load`; this fixes an
  intermediate QA capture where the window title appeared but the first paint was
  blank.

Storage note: this document captured the intermediate installed-UI pass. It is
superseded by `docs/product/flujocrm-sqlite-storage-evidence-2026-05-02.md`,
where the installed UI is verified writing to SQLite through IPC.

## Validation After Fix

```txt
npm run check
flujocrm main smoke passed
flujocrm preload smoke passed

npm audit --omit=dev --audit-level=high
found 0 vulnerabilities
```

Secret scans:

- Product scan: `count_reported=0`.
- Source ZIP scan: `count_reported=0`.
- Windows installer scan: `count_reported=0`.

## Rebuilt Artifacts

This section is superseded. Current final artifact hashes are recorded in:

- `docs/product/flujocrm-sqlite-storage-evidence-2026-05-02.md`

## Current-User Install Result

Evidence folder:

- `qa_artifacts/flujocrm_current_user_install_2026-05-02-r4-final/`

Preflight:

- Installer existed.
- Install directory did not exist.
- Start Menu shortcut did not exist.
- Desktop shortcut did not exist.
- `%APPDATA%\FlujoCRM` already existed from the earlier QA attempt.

Install:

- Installer silent exit code: `0`.
- Install directory created:
  `C:\Users\L-Tyr\AppData\Local\Programs\FlujoCRM`.
- Start Menu shortcut created.
- Desktop shortcut created.
- Uninstall registry entry created: `FlujoCRM 1.0.0`.

Launch:

- Installed app started from:
  `C:\Users\L-Tyr\AppData\Local\Programs\FlujoCRM\FlujoCRM.exe`.
- Main window title: `FlujoCRM - Tu negocio, organizado`.
- Process count observed: `4`.
- App responding: `true`.
- DB path existed:
  `C:\Users\L-Tyr\AppData\Roaming\FlujoCRM\data\flujocrm.db`.
- Wait before capture: `8` seconds.
- DB bytes after launch: `32768`.
- Screenshot:
  `qa_artifacts/flujocrm_current_user_install_2026-05-02-r4-final/flujocrm-installed-launch-desktop.png`.

Uninstall:

- Silent uninstall exit code: `0`.
- After a follow-up wait, install directory was removed.
- Start Menu shortcut was removed.
- Desktop shortcut was removed.
- Uninstall registry entry was removed.
- `%APPDATA%\FlujoCRM` and its DB remained as user data.
- No `FlujoCRM` process remained.

## Decision

FlujoCRM can stay as `FOUNDER_ACCESS` with contact-based delivery discussion.
It must not become `BUY_NOW` until:

- clean Windows machine QA passes;
- unsigned installer wording or code signing is resolved;
- support/refund/privacy/terms copy is final;
- final customer artifact hash is re-verified after any rebuild.
