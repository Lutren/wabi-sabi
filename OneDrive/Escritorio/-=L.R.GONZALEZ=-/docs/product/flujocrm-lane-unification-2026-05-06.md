# FlujoCRM Lane Unification - 2026-05-06

Status: `COMMERCIAL / FOUNDER_ACCESS / PUBLICATION_BLOCK`

FlujoCRM queda como una sola lane comercial en `apps\commercial\flujocrm`.
La fuente histórica vive en `-=MEDIOEVO=-\-=LIBROS\claudio\products\crm`, pero
no debe usarse como verdad activa salvo para comparación o archivo.

## Funcion Fundamental

CRM local para contactos, pipeline simple, tareas y actividad comercial. La
promesa publica permitida es baja: app local-first para organizar clientes sin
suscripción. No hay promesa de ingresos, cumplimiento legal, seguridad absoluta,
sincronización de equipos ni reemplazo de CRM empresarial.

## Canon Activo

- App: `apps\commercial\flujocrm`.
- Ficha de producto: `docs\product\flujocrm.md`.
- Evidencia de release: `docs\product\flujocrm-release-evidence-2026-05-02.md`.
- Evidencia SQLite: `docs\product\flujocrm-sqlite-storage-evidence-2026-05-02.md`.
- QA install actual: `docs\product\flujocrm-current-user-install-qa-2026-05-02.md`.
- Cliente piloto: `apps\commercial\flujocrm\CUSTOMER_INSTALL_NOTES.md`.

## Validacion 2026-05-06

Comandos ejecutados:

```txt
npm ci
npm run check
npm run pack-win-qa
npm run smoke:e2e-storage
python tools\release\scan_secrets.py --path apps\commercial\flujocrm --json --fail-on-findings
```

Resultados:

- `npm ci`: `0 vulnerabilities`.
- `npm run check`: main, preload y renderer smoke pass.
- `npm run pack-win-qa`: genero `dist\win-unpacked\FlujoCRM.exe`.
- `npm run smoke:e2e-storage`: persisted 15 demo contacts to SQLite in an isolated temp profile.
- Secret scan focalizado: `count_reported=0`.

## Decision

- `KEEP`: app, lockfile, scripts de smoke, docs de cliente piloto y assets QA.
- `ARCHIVO`: evidencia 2026-05-01 queda historica.
- `REVIEW`: clean Windows machine QA, code signing/unsigned warning and legal copy.
- `BLOCK`: Gumroad checkout, website buy-now and public release until gates pass.

## Siguiente Cierre

2026-05-06 recheck: `docs\product\flujocrm-current-gate-recheck-2026-05-06.md`
confirma que source smoke, SQLite smoke, secret scan y manifest refresh pasan.
El setup installer final sigue ausente; solo existe `dist\win-unpacked`.

Ejecutar clean-machine QA con installer final y congelar hash. Solo despues se
puede pasar de `FOUNDER_ACCESS` a piloto pago limitado.
