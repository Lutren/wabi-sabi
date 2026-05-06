# Argus Desktop

Argus Desktop is the MEDIOEVO desktop companion shell. It is a commercial or internal application, not an open-source package.

## Status

- Classification: `COMMERCIAL_OR_INTERNAL`
- License: proprietary commercial, pending legal review before external sale
- Version: `0.1.0`
- Runtime stack: React, Vite, Electron
- Source lane: `apps/commercial/argus-desktop`

## Commands

```powershell
npm ci --dry-run --ignore-scripts --no-audit --no-fund
npm run typecheck
npm run build
npm run electron:build:win
```

## Release Boundaries

- Do not include `node_modules/`, `dist/`, build outputs, local logs or caches in source packages.
- Do not publish this app as open source from this folder.
- Do not claim public release readiness until typecheck, build, secret scan, license review and manual QA pass.
- Keep private game, TCG, secrets and local runtime state out of Argus packages.

## Evidence Files

- `COMMERCIAL_LICENSE.md`
- `THIRD_PARTY_NOTICES.md`
- `STATUS.md`
- `package.json`
- `electron-builder.json`
