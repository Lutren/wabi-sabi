# FlujoCRM - Evidencia De Cierre Local

Fecha: 2026-05-01

Ruta canonica: `apps\commercial\flujocrm`

Decision: `WINDOWS_INSTALLER_QA_GENERATED / PUBLICACION_BLOCK`. El paquete fuente privado y el instalador Windows x64 QA estan generados y verificados. No equivale a Gumroad, website, release publico ni repo publicado.

Superseded: 2026-05-02 source cleanup rebuilt the source ZIP and installer. Use
`docs\product\flujocrm-release-evidence-2026-05-02.md` for current hashes:
source ZIP `483b129ea88a9e62f230182252f932bc20a3474edc8591c4148f8873d0d6eee6`
and installer `c3007ddaaa4fa23f97f63c5e6d00450e5fcb630aa81bc2e9fdcee4d583818fc4`.
The 2026-05-01 hashes below remain historical evidence only.

## Cambios Cerrados

- Creado `package-lock.json` para desbloquear `npm audit`.
- Actualizadas devDependencies de build:
  - `electron`: `^41.4.0`
- `electron-builder`: `^26.8.1`
- Actualizado `better-sqlite3` a `^12.9.0` para compatibilidad con Electron `41.4.0`.
- Agregados scripts `build-win-qa` y `pack-win-qa` para builds locales sin publish remoto.
- Agregados iconos placeholder QA en `assets\icon.png` y `assets\icon.ico`.
- Corregidos errores de runtime en `main.js`:
  - `app.whenready()` -> `app.whenReady()`
  - `.foreach(...)` -> `.forEach(...)`
  - `toIerestring()` -> `toISOString()`
- Agregado `scripts\smoke-main.cjs` para cubrir bootstrap de Electron e IPC handlers.
- `npm run check` ahora ejecuta smoke de main y preload.
- Regenerado `release_manifests\flujocrm.json`.
- Generado paquete local privado: `releases\paid-apps\flujocrm.zip`.
- README de producto corregido para remover texto corrupto y dejar estado QA/publicacion bloqueada.
- Listing draft creado en `docs\product\flujocrm-listing-draft-2026-05-01.md`.
- Generado instalador Windows x64 QA: `apps\commercial\flujocrm\dist\FlujoCRM-Setup-1.0.0.exe`.

## Verificaciones

| Comando | Resultado |
|---|---|
| `npm run check` en `apps\commercial\flujocrm` | paso: `flujocrm main smoke passed`, `flujocrm preload smoke passed` |
| `npm audit --omit=dev --json` | `total=0`, `high=0`, `critical=0` |
| `npm audit --json` | `total=0`, `high=0`, `critical=0` |
| `npm run build-win-qa` | `FlujoCRM-Setup-1.0.0.exe` generado |
| `python tools\release\scan_secrets.py --path apps\commercial\flujocrm --json --fail-on-findings` | `count_reported=0` |
| `python tools\release\product_manifest.py --product flujocrm --hash --write` | `release_manifests\flujocrm.json` escrito |
| `python tools\release\package_paid_apps.py --product flujocrm --execute` | `releases\paid-apps\flujocrm.zip` escrito |
| `python tools\release\scan_secrets.py --artifact releases\paid-apps\flujocrm.zip --json --fail-on-findings` | `count_reported=0` |
| `python tools\release\scan_secrets.py --artifact apps\commercial\flujocrm\dist\FlujoCRM-Setup-1.0.0.exe --json --fail-on-findings` | `count_reported=0` |

## Artefactos

- `release_manifests\flujocrm.json`: `file_count=17`, `blocked_count=0`, `excluded_count=246`, `total_bytes=308906`, SHA256 `9ef96ea57ee78f99dc62209bb4a46f982b1590258d839aff33f9ecd2868c22f5`.
- `releases\paid-apps\flujocrm.zip`: 99,795 bytes, SHA256 `f4c4be4aadfee141993047ad383fb263c6ead7b5fbb9dde7b6dca753e628e3c4`.
- `apps\commercial\flujocrm\README.md`: SHA256 `5865e12a228f85da169a81fb5c2a78f25a68444879533154874e377dd5f5c700`.
- `docs\product\flujocrm-listing-draft-2026-05-01.md`: SHA256 `1dce2a7c7cfec06a8e8687eef3501709fc43fbea96e15ca7e8a2dd78f2e90990`.
- `apps\commercial\flujocrm\dist\FlujoCRM-Setup-1.0.0.exe`: 103,730,060 bytes, SHA256 `b7ba740ad82e976dd84fcfc959e78f9a9c9db50117cfcdf419fed106f664723f`, Authenticode `NotSigned`.
- `apps\commercial\flujocrm\dist\win-unpacked\FlujoCRM.exe`: 223,117,824 bytes, SHA256 `6183d2e10a6475fac5ced4a4f546648d2938937100e8826057d51a35fe3696e2`, Authenticode `NotSigned`.

## No Cerrado

- No se probo el instalador en maquina limpia.
- No se genero `.dmg`.
- No hay code signing; el instalador y app estan `NotSigned`.
- Los iconos son placeholder QA, no marca final.
- Legal/support/privacy/refund/terms siguen en `LEGAL_REVIEW_REQUIRED`.
- No publicar en Gumroad ni website hasta cerrar checklist comercial.

Detalle extendido: `docs\product\legacy\FLUJOCRM_WINDOWS_INSTALLER_QA_2026-05-01.md`.
