# FlujoCRM

Status: `SQLITE_STORAGE_QA_PASS / CURRENT_USER_INSTALL_QA_PASS / PUBLICATION_BLOCKED`

FlujoCRM is a local-first desktop CRM for small businesses, freelancers and
operators who want a simple customer pipeline without a hosted SaaS account.

The current build is a QA artifact. It is not ready for public sale until the
installer is tested on a clean Windows machine, final branding is added, the
unsigned-install warning or code signing decision is reviewed, and the legal
drafts are finalized.

## What It Does

- Local contact management.
- Simple pipeline stages for opportunities.
- Follow-up tasks.
- Activity log.
- Local SQLite storage through the Electron IPC bridge.
- The installed UI writes contacts to `%APPDATA%\FlujoCRM\data\flujocrm.db`.
- The standalone HTML preview still falls back to browser `localStorage`.
- CSV import and local backup/export workflows where available in the app.
- Spanish-first defaults with English labels in parts of the interface.

## Current Deliverables

Customer-facing deliverable target:

- Windows x64 installer after clean-machine QA.
- Install/use notes: `CUSTOMER_INSTALL_NOTES.md`.
- Support and refund/privacy/terms links.

macOS is not part of the initial release target. See:
`docs/product/flujocrm-windows-first-release-decision-2026-05-01.md`.

Internal QA artifacts:

- `dist/FlujoCRM-Setup-1.0.0.exe`
- `dist/win-unpacked/`
- `releases/paid-apps/flujocrm.zip` from the workspace root

The source ZIP is not a default customer deliverable.

## Development

```powershell
npm ci
npm run check
npm run start
```

## QA Builds

```powershell
npm run pack-win-qa
npm run build-win-qa
```

`build-win-qa` writes a Windows x64 installer with publishing disabled.

## Release Blockers

- Current-user Windows install/launch/uninstall QA passes with evidence.
- SQLite storage E2E passes against the unpacked build and installed `.exe`.
- Clean Windows machine QA is still pending.
- The current QA icon is a placeholder.
- Artifacts are not code signed.
- macOS DMG is intentionally out of scope for the first release.
- Pilot customer copy exists, but final legal/support/privacy/refund/terms
  review is pending.
- Gumroad or website listing is draft-only.

## License

Proprietary. Copyright L.R. Gonzalez. All rights reserved.
