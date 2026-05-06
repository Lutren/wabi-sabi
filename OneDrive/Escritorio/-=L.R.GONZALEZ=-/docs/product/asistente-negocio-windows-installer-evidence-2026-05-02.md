# Asistente Negocio Windows Installer Evidence - 2026-05-02

Status: `CURRENT_USER_INSTALL_QA_PASS / CHECKOUT_BLOCKED`

This evidence closes the previous "installer or HTML-only decision" blocker for
Asistente Negocio. The product now has a Windows one-click current-user
installer that installs, runs, passes E2E interaction and uninstalls locally.

## Commands

```txt
npm run check
public_safe check passed

npm audit --omit=dev --audit-level=high
found 0 vulnerabilities

npm run build:win
public_safe check passed

npm run smoke:e2e-render
E2E render smoke passed
```

## Installer Cycle

QA folder:

```txt
apps\commercial\asistente-negocio\qa_artifacts\asistente_negocio_windows_install_2026-05-02-r4
```

Install result:

- Installer: `apps\commercial\asistente-negocio\release\Asistente-Negocio-MEDIOEVO-1.0.0-win-x64.exe`
- Silent install args: `/currentuser /S`
- Exit code: `0`
- Installed exe: `%LOCALAPPDATA%\Programs\asistente-negocio-medioevo\Asistente de Negocio MEDIOEVO.exe`
- Desktop shortcut: `true`
- Start Menu shortcut: `true`
- Registry display: `Asistente de Negocio MEDIOEVO 1.0.0`

Installed E2E result:

- Evidence JSON: `e2e-render-smoke.json`
- Status: `passed`
- Page URL: `file:///C:/Users/L-Tyr/AppData/Local/Programs/asistente-negocio-medioevo/resources/app.asar/app/index.html`
- Ready state: `interactive`
- Verified UI state: `Negocio listo`, `Mensaje cargado`, `Respuesta aprobada`
- Verified handoff: email enabled `true`, WhatsApp enabled `true`
- Verified draft markers: business name, prices, hours and appointment offer
- Screenshot: `asistente-e2e-render.png`
- Screenshot SHA256: `659E7ACF62D83AD5CBE8F8227105526C8E80975C9314D72BED0CC21AE750B528`

Uninstall result:

- Quiet uninstall: `%LOCALAPPDATA%\Programs\asistente-negocio-medioevo\Uninstall Asistente de Negocio MEDIOEVO.exe /currentuser /S`
- Exit code: `0`
- Install dir exists after uninstall: `false`
- Desktop shortcut exists after uninstall: `false`
- Start Menu shortcut exists after uninstall: `false`
- Registry exists after uninstall: `false`
- Process count after uninstall: `0`

## Artifact Hashes

| artifact | bytes | SHA256 | signature |
|---|---:|---|---|
| `releases\paid-apps\asistente-negocio.zip` | 19050739 | `C2A73E1B82DB8B1174164398A4CE27C3BBBE42B817EF2B5A887BF95B1B10F423` | n/a |
| `apps\commercial\asistente-negocio\release\Asistente-Negocio-MEDIOEVO-1.0.0-win-x64.exe` | 103243135 | `5B01373668EA2990F976963CB245A4C4F98B4420995A65CA1E438409F085654D` | NotSigned |
| `apps\commercial\asistente-negocio\release\Asistente-Negocio-MEDIOEVO-1.0.0-win-x64.zip` | 140109120 | `8E5B04DFFCF4DF97402DA0542D8BCF2B207CF23816ED9D50A2139755F4C3BF48` | n/a |
| `apps\commercial\asistente-negocio\release\win-unpacked\Asistente de Negocio MEDIOEVO.exe` | 213915136 | `D4DAE8723AA1F8C591F91A9C8C629CAF47C08663DAFC46D65EB6C921EFE8029A` | NotSigned |

## Secret Scan

All scans below used the correct `--artifact` mode for ZIP/EXE outputs.

- Product path scan: `count_reported=0`
- Source ZIP artifact scan: `count_reported=0`
- Installer artifact scan: `count_reported=0`
- Portable ZIP artifact scan: `count_reported=0`

## Remaining Blockers

- Clean Windows VM install smoke.
- Code-signing certificate or explicit unsigned-installer customer warning.
- Final support/refund/privacy/terms legal review.
- Public Gumroad URL verification after upload.
