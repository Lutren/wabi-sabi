# FlujoCRM - Windows Installer QA

Fecha: 2026-05-01

Decision: `WINDOWS_INSTALLER_QA_GENERATED / PUBLICACION_BLOCK`.

Superseded: 2026-05-02 source cleanup rebuilt the installer. Use
`docs\product\flujocrm-release-evidence-2026-05-02.md` and SHA256
`c3007ddaaa4fa23f97f63c5e6d00450e5fcb630aa81bc2e9fdcee4d583818fc4` for the
current QA installer. The hashes below are historical evidence for the
2026-05-01 build only.

No se publico nada. El instalador es un artefacto local de QA y requiere prueba
en maquina limpia, firma o aviso unsigned, y revision legal/comercial antes de
venta.

## Cambios

- `better-sqlite3` subio a `^12.9.0` para compilar contra Electron `41.4.0`.
- Se agregaron scripts QA:
  - `build-win-qa`: `electron-builder --win --config.win.signAndEditExecutable=false --publish never`
  - `pack-win-qa`: `electron-builder --dir --config.win.signAndEditExecutable=false`
- `build.publish` queda como `[]` para evitar metadata remota/update files.
- Windows queda en `x64` para el primer instalador QA.
- Se crearon `assets\icon.png` y `assets\icon.ico` como placeholder QA; no son marca final.

## Artefactos

| Artefacto | Tamano | SHA256 | Estado |
|---|---:|---|---|
| `apps\commercial\flujocrm\dist\FlujoCRM-Setup-1.0.0.exe` | 103730060 | `b7ba740ad82e976dd84fcfc959e78f9a9c9db50117cfcdf419fed106f664723f` | installer QA x64 |
| `apps\commercial\flujocrm\dist\FlujoCRM-Setup-1.0.0.exe.blockmap` | 108711 | `eee715e93e5266f70f8115b1207e534176f45542592fd54986c579e745281940` | build metadata local |
| `apps\commercial\flujocrm\dist\win-unpacked\FlujoCRM.exe` | 223117824 | `6183d2e10a6475fac5ced4a4f546648d2938937100e8826057d51a35fe3696e2` | unpacked app |
| `releases\paid-apps\flujocrm.zip` | 99795 | `f4c4be4aadfee141993047ad383fb263c6ead7b5fbb9dde7b6dca753e628e3c4` | source QA ZIP, not customer deliverable |
| `release_manifests\flujocrm.json` | n/a | `9ef96ea57ee78f99dc62209bb4a46f982b1590258d839aff33f9ecd2868c22f5` | 17 files, 0 blocked |

Authenticode:

- `FlujoCRM-Setup-1.0.0.exe`: `NotSigned`
- `dist\win-unpacked\FlujoCRM.exe`: `NotSigned`

## Validaciones

| Comando | Resultado |
|---|---|
| `npm ci` | 330 packages, `0 vulnerabilities` |
| `npm run check` | `flujocrm main smoke passed`; `flujocrm preload smoke passed` |
| `npm audit --json` | `total=0`, `high=0`, `critical=0` |
| `npm run build-win-qa` | genera `FlujoCRM-Setup-1.0.0.exe` |
| `python tools\release\product_manifest.py --product flujocrm --hash --write` | `file_count=17`, `blocked_count=0` |
| `python tools\release\package_paid_apps.py --product flujocrm --execute` | `17 files included`, ZIP regenerado |
| `scan_secrets.py --artifact releases\paid-apps\flujocrm.zip` | `count_reported=0` |
| `scan_secrets.py --artifact apps\commercial\flujocrm\dist\FlujoCRM-Setup-1.0.0.exe` | `count_reported=0` |
| `scan_secrets.py --path apps\commercial\flujocrm` | `count_reported=0` |
| `scan_secrets.py --path docs\product\flujocrm-listing-draft-2026-05-01.md` | `count_reported=0` |

## Bloqueos Pendientes

- No hay prueba en maquina limpia.
- No hay firma de codigo; usuarios veran publisher desconocido.
- Icono es placeholder QA, no marca final.
- No hay instalador macOS; falta `assets\icon.icns` y build en macOS.
- No se publico Gumroad/website/listing.
- Legal final sigue `LEGAL_REVIEW_REQUIRED`.
