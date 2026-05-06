# RELEASE_READINESS_SCORE

Fecha: 2026-05-01

Estado global: **CIERRE LOCAL POR CARRILES VALIDADO / PRIMERA PUBLICACION EXTERNA EJECUTADA CON EVIDENCIA**

Actualizacion 2026-05-02: la estrategia `open core + UI paga` quedo
documentada y se ejecuto una publicacion externa limitada con override de Luis
Rene Gonzalez solo para host-gate `REVIEW`. Secret scan, path scrub, claims,
licencia y frontera privada siguieron como bloqueos duros.

Actualizacion 2026-05-03: el host gate directo retorno `APPROVE` durante la
ventana de ejecucion GitHub. Se publicaron y verificaron 7 repos `open-dev` y
8 repos `github-public-sanitized` con scans focalizados limpios. El workspace
completo sigue en `BLOCK` por el scan global legacy con 200 hallazgos.

Score operativo vigente: **78 / 100 para cierre local por carriles**

Score de publicacion externa: **GO LIMITADO para los 15 repos GitHub y 2 productos Gumroad ya publicados/verificados / BLOCK para targets nuevos sin gate**.

Host gate actualizado 2026-05-02 durante la publicacion DUAT: `REVIEW`, no
`APPROVE` (`lambda_sat=0.878`, `disk_pct=87.8`). El override humano se aplico
solo a esta corrida y solo cuando el motivo era host `REVIEW`; no autoriza
redes, Gumroad adicionales, repos nuevos ni deploys futuros sin repetir gate y
evidencia.

Nota: este score reemplaza el estimado `45 / 100` del 2026-04-29. No autoriza
Gumroad, redes, push, deploy, modelos pesados ni Symphony wide. La evidencia
maestra vigente esta en `MASTER_PLAN_STATUS_2026-05-01.md`.

Este score mide cierre local por allowlists, tests, secret scans y artefactos
verificados. La publicacion externa mantiene gate separado.

## Score por dimension

| dimension | score | evidencia | bloqueo |
|---|---:|---|---|
| Separacion open/commercial/private | 85/100 | `VISIBILITY_MATRIX.md`, `PRODUCT_MAP.md`, `PRIVATE_GAME_BOUNDARY.md`, manifests por producto | publicacion externa requiere aprobacion humana |
| Secret safety por producto | 95/100 | scan de productos open-dev, GEODIA y comerciales con `count_reported=0` | el workspace completo sigue NO APTO por secretos fuera de allowlists |
| Artifact safety free-dev | 95/100 | 7 ZIPs regenerados, artifact scan `0`, smoke `ok=true`; 7 repos `open-dev` publicados/verificados en GitHub el 2026-05-03 | workspace completo bloqueado por scan global legacy |
| Build/test readiness | 93/100 | `run_tests.py --execute --json`: open-dev, GEODIA, Mini Office, Claudio 834 tests, Asistente, FlujoCRM y Hormiguero pasaron; FlujoCRM tiene SQLite E2E; Asistente tiene installed-app E2E; ambos con audit 0 | clean-VM comercial sigue pendiente |
| Open source readiness | 95/100 publicado por allowlist | 7 paquetes `free-dev` y 8 repos `github-public-sanitized` con scans focalizados limpios y GitHub publico verificado | nuevos targets requieren ActionGate antes de GitHub/publicacion |
| GEODIA interno | 85/100 | DUAT v2 intake, offline run, backtest y rechazo de fuente no allowlist | datos reales/backtests licenciados pendientes |
| Producto comercial | 82/100 | Argus build/typecheck temporal, auditorias Argus/Asistente, FlujoCRM lock/audit/check + Windows installer QA, Asistente Windows installer QA, decision standalone Windows-first, Mini Office runtime smoke/test y limpieza de copy/licencia/installers/generators, 4 ZIPs fuente paid-apps con artifact scan 0, matriz legal draft y frontera de entregable | revision legal final, firma/unsigned documentado, QA en maquina limpia y paquetes finales |
| Wave FC pilot | 70/100 | evidence pack local con `.md`, `.docx` y CSV sinteticos, release gate `local_demo_ready=true`, 61 tests, runtime secret scans 0 y capturas desktop/mobile; video no requerido para el cierre actual | falta QA visual DOCX, EULA/legal e instalacion/listing public-safe |
| Private game boundary | 90/100 | rutas privadas no tocadas ni incluidas en manifests/ZIPs | no sustituye validacion privada del RPG |
| Publicacion externa | 82/100 para targets ejecutados | 15 repos GitHub publicos verificados, 2 productos Gumroad publicados y `medioevo-site` desplegado; evidencia en `qa_artifacts\release_validation\free-dev-github-publish.json`, `qa_artifacts\release_validation\github-public-sanitized-publish.json`, `qa_artifacts\release_validation\publication-live-verification-2026-05-02.json` y `qa_artifacts\release_validation\duat-publication-live-verification-2026-05-02.json` | BLOCK para cualquier target nuevo hasta gate especifico |
| Agent City / open-core split | 80/100 documental | fichas de producto/agente, UI system, dependency gate, claim register y runbook creados | falta implementacion visual en apps y QA por producto |

## Producto por producto

| producto/ruta | readiness | estado |
|---|---:|---|
| `packages\open-dev\residueos` | 95/100 local + GitHub publicado | ZIP `ff9fb162...`, pytest/smoke OK, scan ZIP 0; repo `https://github.com/Lutren/residueos` |
| `packages\open-dev\obsai-core` | 95/100 local + GitHub publicado | ZIP `979fa8ce...`, pytest/smoke OK, scan ZIP 0; repo `https://github.com/Lutren/obsai-core` |
| `packages\open-dev\observacionismo-gate` | 95/100 local + GitHub publicado | ZIP `0004aac7...`, import OK, smoke OK, scan ZIP 0; repo `https://github.com/Lutren/observacionismo-gate` |
| `packages\open-dev\claudio-os-blueprint` | 90/100 local + GitHub publicado | ZIP `c73e6cbd...`, blueprint smoke OK, repo `https://github.com/Lutren/claudio-os-blueprint`; no ISO terminado |
| `packages\open-dev\gemma-observacionismo-cleanup` | 90/100 local + GitHub publicado | ZIP `9f8ba454...`, pytest 3, smoke OK, repo `https://github.com/Lutren/gemma-observacionismo-cleanup`; no pesos/modelos |
| `packages\open-dev\obs-safe-integration-kit` | 95/100 local + GitHub publicado | ZIP `e6b5225c...`, manifest 20 files/0 blocked, ZIP smoke OK, source/ZIP/staging secret scans 0; repo `https://github.com/Lutren/obs-safe-integration-kit` |
| `packages\open-dev\duat-genesis` | 95/100 local + GitHub publicado | ZIP `f672d974...`, manifest 11 files/0 blocked, tests 3 passed, ZIP smoke OK, source/ZIP/staging secret scans 0, path/claims/license checks OK; repo `https://github.com/Lutren/duat-genesis` |
| `packages\paid\medioevo-agent-ops-pack` | 90/100 Gumroad publicado | ZIP `7cf8fdf5...`, source/artifact secret scans 0, claims/path scrub OK, Gumroad `published=true`, URL HTTP 200 |
| `packages\paid\duat-templates` | 90/100 Gumroad publicado | ZIP `03c926b5...`, manifest 8 files/0 blocked, source/artifact secret scans 0, path/claims scan OK, listing JSON OK, Gumroad `published=true`, URL HTTP 200 |
| `research\geodia-social-observatory` | 85/100 interno | pytest 15, DUAT intake, run/backtest offline y allowlist rejection OK; publicacion BLOCK |
| `apps\commercial\argus-desktop` | 80/100 local | temp `npm ci`, typecheck, build y audit 0; paquete final no generado |
| `apps\commercial\asistente-negocio` | 84/100 local | check, audit 0, product/source/installer/portable artifact scans 0, Windows current-user install/E2E/uninstall QA, package-final con instalador/ZIP/demo/install notes/support draft/checksums; falta clean VM, firma/unsigned decision y legal final |
| `apps\commercial\flujocrm` | 86/100 local | lockfile, main/preload/renderer smoke, audit completo 0, product/ZIP/installer secret scan 0, ZIP fuente interno, Windows installer historico, current-user install/launch/uninstall QA con UI completa, SQLite storage E2E y customer pilot copy; standalone Windows-first; aviso unsigned documentado localmente el 2026-05-05; falta clean VM, rebuild/hash final del instalador activo y legal final |
| `apps\commercial\mini-office` | 82/100 local | `python -m pytest -q` 22 passed, `mini_office.py --status` OK, pyproject/package JSON OK, copy/licencia/installers/generators limpiados, manifest `file_count=53`/`blocked_count=0`, ZIP `43150036...`, source/artifact secret scans 0; bloqueado por legal final, clean-machine install, support/privacy/refund y checkout |
| `docs\product\wave-collapse.md` | 70/100 local demo | producto de bajo claim con evidence pack local, release gate, capturas y cierre public-safe local; falta QA visual DOCX, legal e instalacion/listing |
| `metaevo-tcg` | 0/100 para publicacion open | privado/no publicar; no tocado |

## Gates obligatorios antes de cualquier release publico

- [x] `PRIVATE_GAME_BOUNDARY.md` creado.
- [x] `AGENTS.md` raiz creado.
- [x] `README.md` raiz creado.
- [x] `LICENSE` raiz marcado `LEGAL_REVIEW_REQUIRED`.
- [x] Allowlist por producto inicial con manifests hash.
- [x] Denylist de secretos, juego, vendors, caches, builds locales.
- [x] Secret scan por producto sin hallazgos en carriles seleccionados.
- [x] Tests/build/smoke por producto ejecutados con evidencia local.
- [x] Artifact scan para ZIPs free-dev sin hallazgos.
- [x] `VISIBILITY_MATRIX.md` aprobada por humano para gobierno local por
  autorizacion del operador el 2026-05-05; no autoriza publicacion nueva.
- [x] `MIGRATION_MAP.md` existe como mapa obligatorio para cualquier movimiento
  futuro; todo movimiento sigue requiriendo registro antes/despues y gate.
- [x] `RELEASE_CHECKLIST.md` existe con secciones por capa antes de publicacion
  externa; cada target nuevo sigue necesitando checklist especifico y ActionGate.
- [ ] Legal docs comerciales finales con `LEGAL_REVIEW_REQUIRED` resuelto; matriz draft ya existe.
- [x] ActionGate explicito + override humano con evidencia para los targets publicados el 2026-05-02.
- [x] ActionGate explicito + host `APPROVE` para las tandas GitHub publicadas el 2026-05-03.
- [ ] ActionGate explicito para cualquier push, Gumroad, redes o deploy futuro que no sea parte de los targets ya cerrados en esta evidencia.

## Comandos vigentes

La lista completa de comandos, hashes y resultados esta en
`MASTER_PLAN_STATUS_2026-05-01.md`.

Resumen:

- `python tools\release\run_tests.py --execute --json`: paso; `claudio-pytest`
  reporto `834 passed in 84.29s`.
- `python tools\release\package_free_dev.py --execute`: genero 6 ZIPs incluyendo `obs-safe-integration-kit`.
- `python tools\release\verify_free_dev_release.py --write --json`: `ok=true`.
- Secret scan por productos y ZIPs: `count_reported=0`.
- GEODIA offline: intake DUAT v2, scenario report, backtest y rechazo de fuente
  no allowlist verificados.
- Comercial: Argus build/typecheck en copia temporal; Asistente y Argus audit 0;
  Asistente Windows installer QA current-user paso con E2E render; Mini Office
  runtime/test/server smoke paso y copy/licencia/installers quedaron limpiados; FlujoCRM
  audit completo 0 tras lockfile y actualizacion de devDependencies;
  legal/support/privacy/refund/terms tienen matriz draft, no final.

## Decision

Cierre local por carriles completado. La ruta corta queda: `open-dev`
principal en `PUBLICADO_GITHUB` para los siete repos verificados,
`github-public-sanitized` en `PUBLICADO_GITHUB` para ocho repos sanitizados,
GEODIA en `GO` interno, comercial en `REVIEW` salvo `MEDIOEVO Agent Ops Pack`
y `DUAT Templates` en `PUBLICADO_GUMROAD`, Wave FC en
`LOCAL_DEMO_READY / PUBLICACION_BLOCK`, y cualquier target nuevo en `BLOCK`
hasta gate especifico.
