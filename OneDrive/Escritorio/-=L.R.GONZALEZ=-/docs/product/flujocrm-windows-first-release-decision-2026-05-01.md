# FlujoCRM Windows-First Release Decision - 2026-05-01

Status: `WINDOWS_FIRST_QA_PREP / DO_NOT_PUBLISH`

Decision: FlujoCRM sale primero como producto Windows x64. No se prepara `.dmg`
para el lanzamiento inicial. macOS queda fuera del primer release hasta que haya
tiempo de QA especifico, firma/notarizacion y soporte.

## Artifact

- Installer: `apps\commercial\flujocrm\dist\FlujoCRM-Setup-1.0.0.exe`
- Bytes: `103730060`
- SHA256: `c3007ddaaa4fa23f97f63c5e6d00450e5fcb630aa81bc2e9fdcee4d583818fc4`
- Signature: `NotSigned`
- Current deliverable mode: QA installer, not final public sale.

2026-05-02 update: installer was rebuilt after source/demo cleanup. Evidence:
`docs/product/flujocrm-release-evidence-2026-05-02.md`.

## Verification This Pass

```text
npm run check
flujocrm main smoke passed
flujocrm preload smoke passed
```

Installer metadata was rechecked with PowerShell:

```text
exists=true
signature_status=NotSigned
sha256=c3007ddaaa4fa23f97f63c5e6d00450e5fcb630aa81bc2e9fdcee4d583818fc4
```

## Customer-Facing Position

Use this framing for the first listing:

```text
Windows-first local CRM for contacts, follow-ups and simple sales pipelines.
No hosted account, no cloud sync and no subscription in the base app.
```

The first public page must state that the installer may show an
unknown-publisher warning if code signing is not ready. Do not hide that warning.

## Release Boundary

Do not mark FlujoCRM as final sale-ready until:

- clean Windows machine or VM install test passes;
- normal-user install and launch pass;
- create/edit/persist data smoke passes after app restart;
- uninstall behavior is documented;
- final icon/branding decision is made;
- unsigned warning copy or code signing decision is published;
- support/privacy/refund/terms are final.

## Current Decision

`WINDOWS_FIRST` is closed. `CLEAN_INSTALL_QA` remains open.
