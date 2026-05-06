# QA_RESULTS

Fecha: 2026-04-29

## Actualizacion 2026-05-03

Estado: `FREE_DEV_AND_PUBLIC_SANITIZED_GITHUB_PUBLISHED_WITH_WORKSPACE_BLOCK`

Despues de la limpieza de `Downloads` y caches, se ajusto la prueba de intake
GEODIA para aceptar que los crudos de `Downloads` pueden haber sido fichados y
eliminados. La frontera sigue igual: `do_not_copy_raw` y `publication_gate=BLOCK`.

| check | resultado |
|---|---|
| `python -m pytest tests -q` en `packages\open-dev\obsai-core` | `12 passed` |
| `python -m pytest tests -q` en `packages\open-dev\residueos` | `7 passed` |
| `python -m pytest tests -q` en `packages\open-dev\gemma-observacionismo-cleanup` | `3 passed` |
| `python -m pytest tests -q` en `packages\open-dev\duat-genesis` | `3 passed` |
| `python -m pytest tests -q` en `research\geodia-social-observatory` | `15 passed in 0.09s` |
| `python -m pytest tests -q` en `apps\commercial\mini-office` | `22 passed` |
| `python -c "import observacionismo_gate; ..."` | import OK |
| `python tools\release\product_manifest.py --hash --write` | 14 manifests regenerados |
| `python tools\release\scan_secrets.py --product ... --json --fail-on-findings` | `count_reported=0` para `obsai-core`, `residueos`, `observacionismo-gate`, `claudio-os-blueprint`, `gemma-observacionismo-cleanup`, `obs-safe-integration-kit`, `duat-genesis` y `geodia-social-observatory` |
| `python tools\release\package_free_dev.py --execute` | 7 ZIPs escritos en `releases\free-dev` |
| `python tools\release\verify_free_dev_release.py --write --json` | `ok=true`; `qa_artifacts\release_validation\free-dev-smoke.json` |
| `python tools\release\stage_free_dev_repos.py --skip-existing --write --json` | `ok=true`; staging existente limpio en `publish_staging\open-dev` |
| `python tools\release\verify_free_dev_staging.py --write --json` | `ok=true`; `qa_artifacts\release_validation\free-dev-staging-smoke.json` |
| `python tools\release\scan_secrets.py --path publish_staging\open-dev --json --fail-on-findings` | `count_reported=0` |
| `python tools\release\scan_secrets.py --artifact releases\free-dev\*.zip --json --fail-on-findings` | `count_reported=0` para los 7 ZIPs |
| `python tools\release\publish_free_dev_github.py --execute --owner-override-with-evidence --write --json` | `ok=true`, `external_actions_performed=true`; 7 repos GitHub verificados |
| `python tools\release\scan_secrets.py --path publish_staging\github-public-sanitized --json --fail-on-findings` | `count_reported=0` |
| `python tools\release\publish_public_sanitized_github.py --execute --owner-override-with-evidence --write --json` | `ok=true`, `external_actions_performed=true`; 8 repos GitHub verificados |
| `python tools\release\scan_secrets.py` | `reported findings: 200` global, bloquea workspace completo |
| `python tools\host_observacionista.py --no-write` | `gate=APPROVE` en la ventana de publicacion, `disk_pct=82.6`, `lambda_sat=0.826` |

Decision: los 7 repos `open-dev` y los 8 repos `github-public-sanitized`
fueron publicados y verificados en GitHub con evidence JSON. No se hizo deploy
web, Gumroad adicional ni redes. El workspace completo sigue bloqueado por el
scan global legacy; cualquier target nuevo sigue requiriendo ActionGate/host
gate especifico y scans de path/claims/secrets.

Evidencia de verificacion viva: `qa_artifacts\release_validation\github-publication-live-verification-2026-05-03.json`
reporta `ok=true`, `public_count=15`, `count=15`.

Repos GitHub verificados el 2026-05-03:

- `https://github.com/Lutren/residueos`
- `https://github.com/Lutren/obsai-core`
- `https://github.com/Lutren/observacionismo-gate`
- `https://github.com/Lutren/claudio-os-blueprint`
- `https://github.com/Lutren/gemma-observacionismo-cleanup`
- `https://github.com/Lutren/obs-safe-integration-kit`
- `https://github.com/Lutren/duat-genesis`
- `https://github.com/Lutren/data-curation-observatory`
- `https://github.com/Lutren/residueos-core`
- `https://github.com/Lutren/ai-web-gateway-observacionista`
- `https://github.com/Lutren/obs-info-kernel-lite`
- `https://github.com/Lutren/observational-calibration-toolkit`
- `https://github.com/Lutren/duat-lab`
- `https://github.com/Lutren/neurostate-ui`
- `https://github.com/Lutren/la-biblioteca-de-alejandria`

Nota operacional: `data-curation-observatory` rechazo el primer push por
`fetch first`; se integro `origin/main` con `git pull --rebase origin main` y
la segunda corrida publico sin force-push. `gemma-observacionismo-cleanup`
recibio scrub de ruta local en README, tests `3 passed`, manifest y ZIP
regenerados; ZIP SHA256
`9f8ba45409d157ebadbdbf4c25435a6c549b7410cd74a5bac5918af19276d0a7`.

## Actualizacion 2026-05-01

Estado: `PRODUCT_TESTS_PASS_WITH_SECRET_SCAN_BLOCKER`

Comando:

```powershell
python tools\release\run_tests.py --execute --json
```

Resultado:

| check | resultado |
|---|---|
| `obsai-core-pytest` | `9 passed in 0.45s` |
| `residueos-pytest` | `6 passed in 0.96s` |
| `gemma-cleanup-pytest` | `3 passed in 0.02s` |
| `observacionismo-gate-import` | import OK |
| `mini-office-pytest` | `22 passed in 0.19s` |
| `claudio-pytest` | `834 passed in 90.27s` |
| `argus-npm-ci-dry-run` | OK |
| `asistente-negocio-check` | `public_safe check passed` |
| `flujocrm-check` | `flujocrm main smoke passed`; `flujocrm preload smoke passed` |
| `hormiguero-flask-smoke` | endpoints principales OK |

Privado: `private-metaevo-lint` omitido porque no se uso `--include-private`.

Nota: `python tools\release\scan_secrets.py` sigue reportando `200` hallazgos, por lo que no hay autorizacion de release publico amplio.

Actualizacion puntual GEODIA: `python tools\release\scan_secrets.py --product geodia-social-observatory --json --fail-on-findings` paso con `count_reported=0`. Esto solo limpia el artefacto allowlist, no el workspace completo.

Actualizacion free-dev 2026-05-01: los ZIPs locales de `residueos`, `obsai-core`, `observacionismo-gate`, `claudio-os-blueprint` y `gemma-observacionismo-cleanup` pasaron allowlist, secret scan de producto, secret scan interno de ZIP y smoke de instalacion/extraccion.

Actualizacion DUAT Genesis 2026-05-02: `packages\open-dev\duat-genesis` paso `python -m pytest tests -q` con `3 passed`; `product_manifest.py --product duat-genesis --hash --write` genero `release_manifests\duat-genesis.json` con `11` archivos y `0` bloqueados; `package_free_dev.py --product duat-genesis --execute` genero `releases\free-dev\duat-genesis.zip` SHA256 `f672d974d88c3190699ea16caad04b8a6de9839f20aa9513cfd7fdf51c0cbb44`; `verify_free_dev_release.py --product duat-genesis --write --json` dio `ok=true`; fuente, ZIP y staging tuvieron secret scan `count_reported=0`; `verify_free_dev_staging.py --product duat-genesis --write --json` dio `ok=true`; `publish_free_dev_github.py --product duat-genesis --execute --owner-override-with-evidence --write --json` publico el repo con evidencia; `https://github.com/Lutren/duat-genesis` devolvio HTTP `200`. Copias fechadas: `free-dev-smoke-duat-genesis-2026-05-02.json`, `free-dev-staging-smoke-duat-genesis-2026-05-02.json`, `free-dev-github-dry-run-duat-genesis-2026-05-02.json`, `free-dev-github-publish.json` y `duat-publication-live-verification-2026-05-02.json`.

Actualizacion DUAT Templates 2026-05-02: se creo `packages\paid\duat-templates` como pack comercial de plantillas sinteticas; `product_manifest.py --product duat-templates --hash --write` genero `release_manifests\duat-templates.json` con `8` archivos y `0` bloqueados; `package_paid_templates.py --product duat-templates --execute` genero `releases\paid\duat-templates.zip` SHA256 `03c926b549307ef6106d80117183bb22121354671a10e0f2527473c06f6ca518`; listing JSON OK; source/artifact secret scans `count_reported=0`; path/claims scan OK; `publish_gumroad_listing.py --listing packages\paid\duat-templates\commerce\gumroad_listing.json --create-draft --with-file --publish --owner-override-with-evidence --write --json` publico el producto; Gumroad verifico `published=true`; `https://lrgonzalez.gumroad.com/l/duat-templates` devolvio HTTP `200`.

Actualizacion website DUAT 2026-05-02: Cloudflare Pages `medioevo-site` desplego `https://fa4f39aa.medioevo-site.pages.dev` en produccion rama `main`; `https://medioevo.space/`, `https://medioevo.space/software.html` y `https://medioevo.space/apps.html` devolvieron HTTP `200`. La home contiene enlaces directos a `https://github.com/Lutren/duat-genesis` y `https://lrgonzalez.gumroad.com/l/duat-templates`; `software.html` contiene DUAT Genesis; `apps.html` contiene DUAT Genesis y DUAT Templates.

Actualizacion FlujoCRM 2026-05-01: se creo `package-lock.json`, se actualizo Electron/electron-builder para que `npm audit --json` quede en `total=0`, se agrego smoke de `main.js`, y se genero `releases\paid-apps\flujocrm.zip` con artifact secret scan `count_reported=0`. Esto no cierra instalador final ni publicacion.

Actualizacion FlujoCRM installer 2026-05-01: se actualizo `better-sqlite3` a `^12.9.0`, se agrego icono placeholder QA, y `npm run build-win-qa` genero `apps\commercial\flujocrm\dist\FlujoCRM-Setup-1.0.0.exe` (SHA256 `b7ba740ad82e976dd84fcfc959e78f9a9c9db50117cfcdf419fed106f664723f`, `NotSigned`, artifact secret scan `count_reported=0`). No se probo en maquina limpia ni se publico.

Actualizacion FlujoCRM listing 2026-05-01: `apps\commercial\flujocrm\README.md` fue corregido para remover texto corrupto y `docs\product\flujocrm-listing-draft-2026-05-01.md` fue creado como draft `DO_NOT_PUBLISH`; `npm run check` sigue pasando, manifest `flujocrm` queda en `17/0/246`, ZIP interno QA SHA256 `f4c4be4aadfee141993047ad383fb263c6ead7b5fbb9dde7b6dca753e628e3c4`, scans focalizados `count_reported=0`.

Actualizacion paid-apps 2026-05-01: `python tools\release\package_paid_apps.py --execute` genero ZIPs fuente locales para Argus, Asistente Negocio, FlujoCRM y Mini Office. Los cuatro ZIPs pasaron `scan_secrets.py --artifact ... --fail-on-findings` con `count_reported=0`.

Actualizacion Wave FC 2026-05-01: se genero evidence pack local con entradas sinteticas `.md`, `.docx` y CSV; `python -m pytest tests\test_wave_fc_client_demo_package.py tests\test_wave_wabi_release_gate.py tests\test_wave_collapse_report.py tests\test_wave_fc_local_server.py -q` en `-=MEDIOEVO=-\-=LIBROS\claudio` paso con `61 passed`. El release gate quedo en `local_demo_ready=true` y `public_publication_ready=false`; los secret scans focalizados del pack y del gate reportaron `count_reported=0`.

Actualizacion legal comercial 2026-05-01: se creo `docs\legal\COMMERCIAL_RELEASE_LEGAL_MATRIX_2026-05-01.md` para ordenar terms/refund/privacy/support por producto. Todo queda `DRAFT_GATED / LEGAL_REVIEW_REQUIRED`; no autoriza venta ni publicacion.

Actualizacion frontera paid-apps 2026-05-01: `docs\product\paid-app-deliverable-boundary-2026-05-01.md` define los ZIPs fuente comerciales como QA interno, no entregable cliente por defecto. FlujoCRM queda recomendado como standalone primero y bundle despues.

Actualizacion capturas Wave FC 2026-05-01: se generaron capturas locales desde `website\wave-collapse.html` en `qa_artifacts\2026-05-01-wave-fc-captures`; desktop SHA256 `718f82de95cf089ecbef2ce95b7c016660c15b32c54985ba4f45cfa90cb6e056`, mobile SHA256 `1ebc0fe854dbbda1e72fbb24a232e5274c19d49ea19d0367f5ff771cf24806c4`. Pixel/extrema check confirma que no estan vacias.

Actualizacion hackathon 2026-05-01: `hackathons\google-rapid-agent-2026` ahora incluye gate `rapid_agent_guardian.readiness` y exportador `scripts\export_public_repo.py`; `python -m rapid_agent_guardian.readiness --out runtime\submission_readiness.json` devuelve `LOCAL_PUBLIC_SAFE` y `cloudDemoReady=false`; `python scripts\export_public_repo.py` genero `publish_staging\hackathons\google-rapid-agent-2026-public-safe`; `python -m unittest discover -s tests` -> `4 tests OK`; secret scans del source y staging -> `count_reported=0`.

Actualizacion GitHub/Sponsors 2026-05-01: `https://github.com/Lutren/rapid-agent-guardian` fue creado desde el staging publico limpio; commits `511333d576aa9f0273d1134390786b8cb8255e02` y `9de50f23502ada7934c1e61bde54699da20c553d`, repo `PUBLIC`, rama `main`, `.github/FUNDING.yml` presente, homepage a Sponsors y topics de descubrimiento configurados. El README de perfil `Lutren/Lutren` fue actualizado con `rapid-agent-guardian` y niveles sugeridos de Sponsors en commit `f89578af7c6cfe67c67633dca3750eddbc4f49b6`. Intento API de crear tiers Sponsors quedo bloqueado por `Resource not accessible by personal access token`; `tiers.totalCount=0`.

| check | resultado |
|---|---|
| `python tools\release\scan_secrets.py --product ... --json --fail-on-findings` | `count_reported=0` |
| `python tools\release\package_free_dev.py --execute` | 5 ZIPs escritos en `releases\free-dev` |
| `python tools\release\scan_secrets.py --artifact ... --json --fail-on-findings` | `count_reported=0` |
| `python tools\release\verify_free_dev_release.py --write --json` | `ok=true`; reporte en `qa_artifacts\release_validation\free-dev-smoke.json` |
| `python tools\release\stage_free_dev_repos.py --skip-existing --write --json` | `ok=true`; 5 repos staging locales, sin remotos |
| `python tools\release\verify_free_dev_staging.py --write --json` | `ok=true`; install/import/tests desde copia temporal |
| `python tools\release\publish_free_dev_github.py --write --json` | `ok=true`, `external_actions_performed=false`; reporte en `qa_artifacts\release_validation\free-dev-github-dry-run.json` |
| `python tools\release\publish_free_dev_github.py --product observacionismo-gate --execute --write --json` | blocked before external action; `allowed=false`, `external_actions_performed=false`; reporte en `qa_artifacts\release_validation\free-dev-github-publish.json` |
| `python tools\release\scan_secrets.py --path publish_staging\open-dev --json --fail-on-findings` | `count_reported=0` |
| `python tools\release\scan_secrets.py --path qa_artifacts\release_validation\host-gate-offload-2026-05-01.json --json --fail-on-findings` | `count_reported=0` |
| `python -m pytest tests\test_wave_fc_client_demo_package.py tests\test_wave_wabi_release_gate.py tests\test_wave_collapse_report.py tests\test_wave_fc_local_server.py -q` | `61 passed` |
| `python tools\wave_fc_client_demo_package.py --name wave_fc_evidence_pack_2026-05-01` | evidence pack local generado |
| `python tools\wave_wabi_release_gate.py --name wave_wabi_gate_2026-05-01` | `local_demo_ready=true`; `public_publication_ready=false` |

Nota de publicacion: el dry-run de GitHub paso para los cinco paquetes. El intento real de un producto quedo bloqueado porque el host gate sigue en `REVIEW`; no hubo remotos, `gh`, `git push` ni URL publica.

Verificacion GEODIA ejecutada fuera del runner global:

| check | resultado |
|---|---|
| `python -m pytest tests -q` en `research\geodia-social-observatory` | `14 passed in 0.10s` |
| `python -m geodia_social_observatory.cli intake --pretty` | `source_count=10` |
| `python -m geodia_social_observatory.cli simulate-duat --seed 7 --size 12 --steps 5 --pretty` | contrato `motor.duat_conway_simulation.v1` |
| `python tools\release\product_manifest.py --product geodia-social-observatory --hash --write` | `file_count=19`, `blocked_count=0` |
| `python tools\release\scan_secrets.py --product geodia-social-observatory --json --fail-on-findings` | `count_reported=0` |
| `python tools\release\scan_secrets.py --path release_manifests\geodia-social-observatory.json --json --fail-on-findings` | `count_reported=0` |

## Resultado general

Estado: `PUBLIC_QA_PASS_WITH_RELEASE_BLOCKERS_IN_LEGACY_SECRET_SCAN`

La suite publica ejecutable paso. El release completo del workspace raiz sigue bloqueado por marcadores de secretos en rutas legacy detectadas por `scan_secrets.py`; los paquetes allowlist no quedaron bloqueados por manifests.

## Comandos ejecutados

| comando | resultado | evidencia |
|---|---|---|
| `python -m py_compile tools/release/_common.py tools/release/product_manifest.py tools/release/package_free_dev.py tools/release/package_paid_apps.py tools/release/run_tests.py tools/release/run_builds.py tools/release/clean_generated_artifacts.py tools/release/hormiguero_smoke.py` | pass | scripts de release compilan |
| `node -e "...new Function(script)..."` sobre `apps/hormiguero_mission_control/index.html` | pass | `inline scripts ok: 1` |
| `python tools/release/hormiguero_smoke.py` | pass | `/api/health`, `/api/state`, `/api/buildings`, `/api/agents`, `/api/city-registry` devolvieron 200 JSON |
| `python -m pytest packages/open-dev/gemma-observacionismo-cleanup/tests -q` | pass | `3 passed` |
| `python -m pytest packages/open-dev/obsai-core/tests -q` | pass | `5 passed` |
| `python -m pytest packages/open-dev/residueos/tests -q` | pass | `5 passed` |
| `python tools/release/run_tests.py --execute --json` | pass | paquetes open-dev, Mini Office, Claudio, Argus dry-run install, Asistente, FlujoCRM y Hormiguero pasaron; MetaEvo privado omitido |
| `python tools/release/run_builds.py --execute --json` | pass | manifests, packages dry-run, Argus release check, Asistente audit/check y FlujoCRM check pasaron; MetaEvo privado omitido |
| `python tools/release/clean_generated_artifacts.py --execute --json` | pass | `node_modules` y `dist` de Argus archivados al final |
| Playwright desktop/mobile contra `http://127.0.0.1:5050/` | pass | ciudad online, 9 edificios, 6 agentes, fallback offline oculto, screenshots no vacios, sin solape stage/panel |

## Detalle de suites

- `claudio`: `612 passed in 290.52s`.
- `mini-office`: `22 passed`.
- `obsai-core`: `5 passed`.
- `residueos`: `5 passed`.
- `gemma-observacionismo-cleanup`: `3 passed`.
- `observacionismo-gate`: import smoke paso.
- `argus-desktop`: `npm ci` con cache temporal, `npm rebuild`, `npm run typecheck`, `npm run build`, `npm audit --omit=dev --audit-level=high` pasaron.
- `asistente-negocio`: `npm run check` y `npm audit --omit=dev --audit-level=high` pasaron.
- `flujocrm`: `npm run check` paso.
- `hormiguero_mission_control`: smoke Flask paso.
- `hormiguero_mission_control` visual: screenshots en `qa_artifacts\2026-04-29-hormiguero-city\desktop.png` y `qa_artifacts\2026-04-29-hormiguero-city\mobile.png`.

## Bloqueos reales

- `scan_secrets.py` sigue encontrando marcadores de secretos en rutas legacy (`claudio/_archivo_sesiones`, `claudio/_legacy`, `llm-wiki`). Esto no bloquea los paquetes allowlist, pero si bloquea publicar el workspace completo.
- MetaEvo/TCG no se ejecuto por defecto. Requiere `--include-private` y coordinacion con el agente del videojuego.

## Incidente resuelto durante QA

Argus tuvo una instalacion parcial de `node_modules` en OneDrive: `npm ci` reporto `ENOTEMPTY`, y luego faltaban binarios como `tsc`/`vite`. Se archivo la instalacion parcial y se agrego `tools/release/argus_release_check.py`, que usa cache temporal y `npm rebuild` antes de typecheck/build/audit. El runner canonico paso despues de ese cambio.
