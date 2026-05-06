# FlujoCRM - Build Instructions

Status: `SQLITE_STORAGE_QA_PASS / CURRENT_USER_INSTALL_QA_PASS / DO_NOT_PUBLISH_CHECKOUT`

These instructions are for internal QA and release packaging. Do not publish a
Gumroad checkout until clean-machine install, legal/support copy and unsigned
installer messaging are complete.

## Prerequisites

1. Node.js 18+.
2. npm.
3. Git, optional for version control.
4. Windows for final Windows install QA.

## Setup

```bash
cd apps/commercial/flujocrm
npm ci
```

## Development

```bash
npm start
```

This opens the Electron app in development mode. The current QA build loads
`mockup.html`, which is the complete CRM UI. In Electron, the UI uses
`window.api.contacts` through the preload bridge and persists contacts in
SQLite. When opened outside Electron, the same HTML falls back to browser
`localStorage` for preview/demo use.

## Checks

```bash
npm run check
npm audit --omit=dev --audit-level=high
```

`npm run check` validates `main.js`, `preload.js` and the local smoke scripts.

## Windows QA Build

```bash
npm run build-win-qa
```

Output:

- `dist/FlujoCRM-Setup-1.0.0.exe`
- `dist/FlujoCRM-Setup-1.0.0.exe.blockmap`
- `dist/win-unpacked/`

The QA installer:

- installs as a one-click NSIS installer;
- creates desktop and Start Menu shortcuts;
- installs under the normal Electron/electron-builder app location;
- stores the local database under the user's Electron app data path:
  `%APPDATA%\FlujoCRM\data\flujocrm.db`.

## Current-User Install QA

Evidence from 2026-05-02 is recorded in:

- `docs/product/flujocrm-current-user-install-qa-2026-05-02.md`
- `qa_artifacts/flujocrm_current_user_install_2026-05-02-r4-final/`

Result:

- install exit code `0`;
- desktop and Start Menu shortcuts were created;
- app launched with window title `FlujoCRM - Tu negocio, organizado`;
- screenshot shows the complete dashboard UI;
- the window is shown after `did-finish-load` to avoid the blank-window capture
  found during an intermediate QA pass;
- SQLite DB was initialized under `%APPDATA%`;
- SQLite storage E2E passed against the installed `.exe` with an isolated QA
  profile: `loadDemo()` wrote 15 contacts, `stage`, `value` and
  `last_activity` persisted, and the SQLite total was `958000`;
- silent uninstall exit code `0`;
- install directory, shortcuts and uninstall registry entry were gone after a
  follow-up wait;
- `%APPDATA%\FlujoCRM` remained as user data.

## macOS

macOS is intentionally out of scope for the first release. Do not build or list
a `.dmg` as part of the first public offer until a separate macOS QA pass is
approved.

## App Icons

Required files:

- `assets/icon.ico` for Windows.
- `assets/icon.png` as fallback.
- `assets/icon.icns` only when macOS returns to scope.

If icons are regenerated, record the source asset and rerun the build.

## Code Signing

### Windows

The current QA build is unsigned. That means Windows may show an unknown
publisher or SmartScreen warning. Before a public paid release, choose one of:

1. Obtain a code signing certificate and rebuild the installer.
2. Keep v1 unsigned, but make the warning explicit in the listing, install
   notes and support policy.

Never commit certificate files, passphrases or signing secrets.

### macOS

Requires Apple Developer ID signing and notarization. Out of scope for the first
release.

## Clean Install QA

Use `docs/product/flujocrm-clean-install-checklist-2026-05-01.md`.

Minimum evidence before checkout:

- SHA256 of the installer verified on the test machine.
- Normal-user install completes.
- App launches from Start Menu or desktop shortcut.
- Contact create/edit/delete works.
- Pipeline/task create/edit/delete works.
- Backup path works or the limitation is documented.
- Uninstall behavior is documented.
- Any Windows warning is captured and reflected in customer copy.

Current pilot customer copy:

- `CUSTOMER_INSTALL_NOTES.md`

This file includes unsigned-installer wording, local-data behavior, support
intake, refund draft and privacy draft. It remains
`LEGAL_REVIEW_REQUIRED`.

## Distribution Checklist

- [x] `npm run check` passes. Verificado local 2026-05-05: `node --check main.js`, `node --check preload.js`, `smoke-main.cjs`, `smoke-preload.cjs` y `smoke-renderer.cjs` pasaron.
- [ ] `npm audit --omit=dev --audit-level=high` passes.
- [ ] Source and artifact secret scans pass.
- [x] Current-user Windows install/launch/uninstall QA passes.
- [x] SQLite UI storage E2E passes.
- [ ] Clean Windows machine QA passes.
- [x] Code signing or unsigned-warning decision is documented for pilot/founder access; v1 may stay unsigned only with explicit customer warning, while final checkout remains blocked by clean-machine QA and legal review.
- [ ] Support, refund, privacy and terms copy is final.
- [ ] Gumroad product page is created only after the above evidence exists.
- [ ] Website CTA stays `Acceso fundador` until checkout is verified.
