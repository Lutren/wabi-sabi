# Asistente Negocio Release Evidence - 2026-05-02

Status: `FOUNDER_ACCESS_WINDOWS_QA / DO_NOT_PUBLISH_CHECKOUT`

Asistente Negocio now has a verified Windows current-user installer path and an
E2E renderer smoke for the installed executable. It is still not `BUY_NOW`
because clean-machine QA, code-signing/unsigned decision and final legal/support
review remain gated.

## Fixes

- `scripts/package-final-release.cjs` now generates the standalone preview if it
  is missing.
- The same package script no longer fails when an optional platform icon is
  missing; it writes explicit `ICONO_PENDIENTE.txt` notes instead.
- `electron\main.cjs` now supports opt-in E2E-only `ASISTENTE_E2E_PORT` and
  `ASISTENTE_USER_DATA_DIR`, without changing normal customer launch behavior.
- `scripts\e2e-render-smoke.cjs` validates the packaged/installed app through
  Chromium DevTools Protocol: save business profile, draft response, approve
  response and confirm email/WhatsApp handoff links are enabled only after human
  approval.
- `packaging\icon.ico` and `packaging\icon.png` exist and are used by the Windows build/source package.
- `package:final` was tested with `MEDIOEVO_FINAL_RELEASE_DIR` pointing to a QA
  folder, not the real Desktop final product folder.

## Validation

```txt
npm run check
public_safe check passed

npm audit --omit=dev --audit-level=high
found 0 vulnerabilities

npm run build:win
public_safe check passed
electron-builder generated NSIS EXE, portable ZIP and win-unpacked app

npm run smoke:e2e-render
E2E render smoke passed
```

Installer QA:

- QA folder: `apps\commercial\asistente-negocio\qa_artifacts\asistente_negocio_windows_install_2026-05-02-r4`
- Silent install exit code: `0`.
- Installed exe existed at `%LOCALAPPDATA%\Programs\asistente-negocio-medioevo\Asistente de Negocio MEDIOEVO.exe`.
- Desktop shortcut: present.
- Start Menu shortcut: present.
- Registry display name/version: `Asistente de Negocio MEDIOEVO 1.0.0` / `1.0.0`.
- Installed executable E2E: `status=passed`.
- E2E verified: `Negocio listo`, `Respuesta aprobada`, email handoff enabled and WhatsApp handoff enabled.
- Silent uninstall exit code: `0`.
- Post-uninstall: install dir false, Desktop shortcut false, Start Menu shortcut false, registry false, process count `0`.

Secret scans:

- Product scan: `count_reported=0`.
- Source ZIP artifact scan: `count_reported=0`.
- Installer artifact scan: `count_reported=0`.
- Portable ZIP artifact scan: `count_reported=0`.

## Artifacts

Source/commercial ZIP:

- Path: `releases\paid-apps\asistente-negocio.zip`
- Bytes: `19050739`
- SHA256: `C2A73E1B82DB8B1174164398A4CE27C3BBBE42B817EF2B5A887BF95B1B10F423`
- Members: `37`
- Includes standalone preview and packaging icons; excludes `node_modules`, `dist`, `release`, `build` and `qa_artifacts`.

Windows installer:

- Path: `apps\commercial\asistente-negocio\release\Asistente-Negocio-MEDIOEVO-1.0.0-win-x64.exe`
- Bytes: `103243135`
- SHA256: `5B01373668EA2990F976963CB245A4C4F98B4420995A65CA1E438409F085654D`
- Signature: `NotSigned`

Windows portable ZIP:

- Path: `apps\commercial\asistente-negocio\release\Asistente-Negocio-MEDIOEVO-1.0.0-win-x64.zip`
- Bytes: `140109120`
- SHA256: `8E5B04DFFCF4DF97402DA0542D8BCF2B207CF23816ED9D50A2139755F4C3BF48`

Windows unpacked executable:

- Path: `apps\commercial\asistente-negocio\release\win-unpacked\Asistente de Negocio MEDIOEVO.exe`
- Bytes: `213915136`
- SHA256: `D4DAE8723AA1F8C591F91A9C8C629CAF47C08663DAFC46D65EB6C921EFE8029A`
- Signature: `NotSigned`

Final package QA output:

- Root: `qa_artifacts\asistente_negocio_final_package_2026-05-02\Asistente_Negocio_MEDIOEVO_v1.0.0`
- Files: `16`
- Includes:
  - `ABRE_AQUI_DEMO_MEDIOEVO.html`
  - `Preview_HTML_multiplataforma\app\index.html`
  - `README_PRIMERO.md`
  - `VERSION.txt`
  - `CHECKSUMS_SHA256.txt`
  - `Documentos\README_PRODUCTO.md`
  - `Documentos\POLITICA_PUBLIC_SAFE.md`
  - `Documentos\LICENCIA_EULA.md`
  - `Documentos\NOTAS_INSTALACION_CLIENTE.md`
  - `Documentos\SOPORTE_PRIVACIDAD_REEMBOLSO_DRAFT.md`
  - `Windows\Asistente-Negocio-MEDIOEVO-1.0.0-win-x64.exe`
  - `Windows\Asistente-Negocio-MEDIOEVO-1.0.0-win-x64.zip`
  - `Windows\Asistente-Negocio-MEDIOEVO-1.0.0-win-x64.exe.blockmap`
  - `Windows\icon.ico`
  - `Mac\ICONO_PENDIENTE.txt`
  - `Mac\COMO_COMPILAR_MAC.md`

Visual QA:

- Screenshot: `apps\commercial\asistente-negocio\qa_artifacts\asistente_negocio_windows_install_2026-05-02-r4\asistente-e2e-render.png`
- SHA256: `659E7ACF62D83AD5CBE8F8227105526C8E80975C9314D72BED0CC21AE750B528`
- Result: installed Electron app rendered and completed a human-approved reply workflow.

## Decision

Keep status as `FOUNDER_ACCESS`.

Allowed now:

- contact-based founder access;
- HTML preview demonstration;
- Windows installer pilot delivery after manual review;
- manual setup conversation.

Blocked before checkout:

- support/refund/privacy/terms final wording;
- clean Windows VM install smoke;
- code-signing certificate or explicit unsigned-installer customer warning;
- final human legal review;
- public Gumroad product URL verification after upload.
