# MASTER_PLAN_STATUS_2026-05-01

Fecha: 2026-05-01

Raiz: `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-`

Decision ejecutiva: cierre local por evidencia en estado **GO** para open-dev
allowlist y GEODIA como investigacion interna. Publicacion externa general sigue
**BLOCK**: no Gumroad, no redes, no deploy, no modelos pesados y no Symphony
wide sin ActionGate y aprobacion humana explicita. Excepcion ejecutada con
override humano: perfil GitHub `Lutren/Lutren` y repo hackathon public-safe
`Lutren/rapid-agent-guardian`; dashboard GitHub Sponsors completado y verificado
publicamente. 2FA, hackathon/cloud/video y rotacion de secretos historicos
quedaron cerrados por responsabilidad del usuario; este documento no afirma
verificacion tecnica local de esos valores ni factores.

Actualizacion 2026-05-02: `duat-genesis` se integro al carril `free-dev` y se
publico en `https://github.com/Lutren/duat-genesis`. `duat-templates` se preparo
y publico como pack pagable de plantillas sinteticas en
`https://lrgonzalez.gumroad.com/l/duat-templates`. La web `medioevo-site` fue
desplegada en Cloudflare Pages y verificada en `https://medioevo.space/`.

Actualizacion 2026-05-03: tras limpieza agresiva y host gate `APPROVE`, se
publicaron y verificaron 7 repos `open-dev` y 8 repos
`github-public-sanitized`. La publicacion fue por targets allowlist, con scans
focalizados limpios y ActionGate; el workspace completo sigue `BLOCK` por el
scan global legacy.

## Gate Actual

| gate | resultado | evidencia |
|---|---|---|
| Host gate no destructivo | `APPROVE` | `python tools\host_observacionista.py --no-write`: `gate=APPROVE`, `status=LIMPIO`, `disk_pct=84.9`, `memory_pct=62.4` |
| ActionGate/publicacion | `BLOCK_GENERAL / TARGETS_PUBLICADOS_CON_EVIDENCIA` | se ejecutaron perfil GitHub, repos public-safe seleccionados, dashboard Sponsors, `duat-genesis`, `duat-templates`, deploy `medioevo-site`, 7 repos `open-dev` y 8 repos `github-public-sanitized`; redes, productos adicionales y workspace completo siguen bloqueados |
| Tareas user-owned | `CLOSED_BY_OWNER` | 2FA, tax/payout/bank, hackathon cloud/video y rotacion de secretos historicos quedan fuera del loop de Codex salvo nueva instruccion |
| Private game boundary | `BLOCK` para open/commercial | no se tocaron rutas `metaevo-tcg`, `tcg`, `runtime/game_bridge` ni RPG |
| Heavy models | `BLOCK` | no se ejecuto Gemma, vLLM, Ray, LoRA ni rutas pesadas |

## Evidencia Ejecutada

| comando | resultado |
|---|---|
| `python tools\release\product_manifest.py --hash --write` | 10 manifests regenerados en `release_manifests\`; todos con `blocked_count=0` |
| `python tools\release\scan_secrets.py --product ... --json --fail-on-findings` | productos open-dev, GEODIA y comerciales: `count_reported=0` |
| `python tools\release\run_tests.py --execute --json` | todos los checks publicos ejecutados pasaron; `private-metaevo-lint` omitido por frontera privada |
| `python tools\release\package_free_dev.py --execute` | 5 ZIPs free-dev regenerados por allowlist |
| `python tools\release\verify_free_dev_release.py --write --json` | `qa_artifacts\release_validation\free-dev-smoke.json`, `ok=true` |
| `python tools\release\scan_secrets.py --artifact releases/free-dev/*.zip --json --fail-on-findings` | ZIPs free-dev: `count_reported=0` |
| `python tools\release\package_free_dev.py --product duat-genesis --execute` | `releases\free-dev\duat-genesis.zip`, SHA256 `f672d974d88c3190699ea16caad04b8a6de9839f20aa9513cfd7fdf51c0cbb44` |
| `python tools\release\verify_free_dev_staging.py --product duat-genesis --write --json` | staging limpio `publish_staging\open-dev\duat-genesis`, commit `3488b49`, tests `3 passed` |
| `python tools\release\publish_free_dev_github.py --product duat-genesis --execute --owner-override-with-evidence --write --json` | repo publico `https://github.com/Lutren/duat-genesis`, HTTP 200 |
| `python tools\release\package_paid_templates.py --product duat-templates --execute` | `releases\paid\duat-templates.zip`, SHA256 `03c926b549307ef6106d80117183bb22121354671a10e0f2527473c06f6ca518` |
| `python tools\release\publish_gumroad_listing.py --listing packages\paid\duat-templates\commerce\gumroad_listing.json --create-draft --with-file --publish --owner-override-with-evidence --write --json` | Gumroad `DUAT Templates` publicado, `published=true`, URL `https://lrgonzalez.gumroad.com/l/duat-templates`, HTTP 200 |
| `wrangler pages deploy . --project-name medioevo-site --branch main --commit-dirty=true --commit-message "Add DUAT Genesis and Templates to landing"` | Cloudflare Pages deployment `fa4f39aa-93d4-4c38-a3fb-bdda712d6224`, `https://medioevo.space/` HTTP 200 con links DUAT Genesis y DUAT Templates |
| `python -m geodia_social_observatory.cli duat-v2-intake --pretty` | schema `motor.duat_v2_intake.v1`, `source_count=4`, `publication_gate=BLOCK` |
| `python -m geodia_social_observatory.cli run --offline --fixture fixtures\social_epoch_fixture.json --pretty` | reporte local con `publication_gate.status=BLOCK` |
| `python -m geodia_social_observatory.cli backtest --offline --fixture fixtures\social_epoch_fixture.json --pretty` | `status=evaluated`, `direction_match=true`, clasificacion `INFERENCIA` |
| `python -m geodia_social_observatory.cli validate-source --source-id random_blog --source-url https://example.com --pretty` | fallo esperado: `SourcePolicyError: source is not allowlisted: random_blog` |
| Obs Info Kernel intake/extract | `PASS`: seis fuentes nuevas de Downloads clasificadas; `research\obs-info-kernel` extraido limpio como `INTERNAL_RESEARCH / DO_NOT_PUBLISH`; EOR/AIA guardado; tests `10 passed` |
| Argus temp copy: `npm ci`, `npm run typecheck`, `npm run build` | paso en copia temporal; no se recreo `node_modules` en workspace |
| `npm audit --omit=dev --audit-level=high` en Argus y Asistente | `found 0 vulnerabilities` |
| `npm audit --json` en FlujoCRM | `PASS`: lockfile creado; `total=0`, `high=0`, `critical=0` |
| `npm run build-win-qa` en FlujoCRM | `PASS`: genero instalador Windows x64 QA `FlujoCRM-Setup-1.0.0.exe` |
| GitHub public-safe hackathon repo | `PASS`: `https://github.com/Lutren/rapid-agent-guardian`, commits `511333d576aa9f0273d1134390786b8cb8255e02` y `9de50f23502ada7934c1e61bde54699da20c553d` |
| GitHub open-dev batch 2026-05-03 | `PASS`: `publish_free_dev_github.py --execute --owner-override-with-evidence --write --json` publico/verifico 7 repos; evidencia `qa_artifacts\release_validation\free-dev-github-publish.json` |
| GitHub public-sanitized batch 2026-05-03 | `PASS`: `publish_public_sanitized_github.py --execute --owner-override-with-evidence --write --json` publico/verifico 8 repos; evidencia `qa_artifacts\release_validation\github-public-sanitized-publish.json` |
| GitHub profile Sponsors README | `PASS`: `Lutren/Lutren` commit `0b145602500228abc73cdfcf2f406d03caf58962`; API verifica Sponsor link, goal `25 monthly sponsors`, tiers `$5/$19/$50/$100/$500`, frontera paga y URLs sin hard-wrap roto |
| GitHub Sponsors dashboard | `PASS`: profile details actualizado, goal `25 monthly sponsors` creado y tiers `$5/$19/$50/$100/$500` publicados; verificacion publica no-cache confirma cards reales |
| GitHub Sponsors tier API | `BLOCK_API_ONLY`: `createSponsorsTier` fallo con `Resource not accessible by personal access token`; resuelto por dashboard UI autenticado |
| FlujoCRM Windows-first decision | `PASS`: `docs\product\flujocrm-windows-first-release-decision-2026-05-01.md`; standalone primero, bundle despues, sin `.dmg` inicial |
| Wave FC public-safe closure | `PASS`: `docs\product\wave-fc-public-safe-release-closure-2026-05-01.md`; demo privada/local OK, publicacion amplia BLOCK |
| Product continuation report | `PASS`: `docs\PRODUCT_CONTINUATION_FLUJOCRM_WAVE_2026-05-01.md` resume cierres user-owned y proximos proyectos reales |

## Resultados De Tests

| check | resultado |
|---|---|
| `obsai-core-pytest` | `9 passed in 0.31s` |
| `residueos-pytest` | `6 passed in 0.87s` |
| `gemma-cleanup-pytest` | `3 passed in 0.04s` |
| `geodia-social-observatory-pytest` | `15 passed in 0.17s` |
| `observacionismo-gate-import` | import OK: `observacionismo_gate` |
| `mini-office-pytest` | `22 passed in 0.15s` |
| `claudio-pytest` | `834 passed in 84.29s` |
| `argus-npm-ci-dry-run` | OK, `added 805 packages in 1s` dry-run |
| `asistente-negocio-check` | `public_safe check passed` |
| `flujocrm-check` | `flujocrm main smoke passed`; `flujocrm preload smoke passed` |
| `hormiguero-flask-smoke` | endpoints `/api/buildings`, `/api/agents`, `/api/city-registry` OK |
| `obs-info-kernel-pytest` | `10 passed in 0.09s` |

## Manifests Vigentes

| producto | clasificacion | lane | files | blocked | excluded | bytes | decision |
|---|---|---:|---:|---:|---:|---:|---|
| `residueos` | OPEN | free-dev | 13 | 0 | 12 | 42199 | GO local |
| `obsai-core` | OPEN | free-dev | 16 | 0 | 15 | 42782 | GO local |
| `observacionismo-gate` | OPEN | free-dev | 9 | 0 | 1 | 15319 | GO local |
| `claudio-os-blueprint` | OPEN | free-dev | 35 | 0 | 0 | 41465 | PUBLICADO GitHub como blueprint; no ISO |
| `gemma-observacionismo-cleanup` | OPEN | free-dev | 12 | 0 | 7 | 12527 | PUBLICADO GitHub; no pesos/modelos |
| `duat-genesis` | OPEN | free-dev | 11 | 0 | 8 | 15711 | PUBLICADO GitHub; no DUAT Geodia/RPG/claims cientificos |
| `geodia-social-observatory` | INTERNAL_RESEARCH | internal-research | 21 | 0 | 20 | 91370 | GO interno; publicacion BLOCK |
| `argus-desktop` | COMMERCIAL_OR_INTERNAL | paid-apps | 52 | 0 | 11 | 7484644 | REVIEW comercial |
| `asistente-negocio` | COMMERCIAL | paid-apps | 31 | 0 | 0 | 6950992 | REVIEW comercial |
| `flujocrm` | COMMERCIAL | paid-apps | 17 | 0 | 246 | 308906 | REVIEW comercial local; lock/audit/ZIP fuente, README corregido, listing draft e instalador Windows QA OK |
| `mini-office` | COMMERCIAL | paid-apps | 52 | 0 | 12 | 195943 | REVIEW comercial |
| `duat-templates` | COMMERCIAL | paid-templates | 8 | 0 | 0 | 6062 | PUBLICADO Gumroad; no DUAT Geodia/RPG/claims cientificos |

## ZIPs Free-Dev Regenerados

| ZIP | bytes | members | sha256 | smoke |
|---|---:|---:|---|---|
| `releases\free-dev\residueos.zip` | 15954 | 13 | `972b0c1a2bc4ac2eba9f69ba00fb7474c52e32bb527d04e3cf898a680d95d167` | OK |
| `releases\free-dev\obsai-core.zip` | 22856 | 18 | `7bea92af104f17bdc8c548e175c1ddd9371a5f18b7bdaef3f1aaf73e557326b6` | OK |
| `releases\free-dev\observacionismo-gate.zip` | 8004 | 9 | `0004aac74730cfdef1208b9a6b6ba0f1ba68908b01089855081e32098c47013c` | OK |
| `releases\free-dev\claudio-os-blueprint.zip` | 26725 | 35 | `c73e6cbd340f1084063317ac99813a58bf7e42dcdcc9bd7f3bbbb1d30ce2c570` | OK |
| `releases\free-dev\gemma-observacionismo-cleanup.zip` | 7847 | 12 | `9f8ba45409d157ebadbdbf4c25435a6c549b7410cd74a5bac5918af19276d0a7` | OK |
| `releases\free-dev\duat-genesis.zip` | 8505 | 11 | `f672d974d88c3190699ea16caad04b8a6de9839f20aa9513cfd7fdf51c0cbb44` | OK |

## Open-Dev

Decision: **PUBLICADO GitHub por allowlist**.

Los siete paquetes open-dev tienen allowlist, manifiesto hash, ZIP, artifact
secret scan `0`, smoke desde extraccion temporal y repos GitHub publicos
verificados. Esto no autoriza publicar el workspace completo ni targets nuevos:
el siguiente paso externo vuelve a requerir scans focalizados y ActionGate.

## GEODIA

Decision: **GO interno / BLOCK publicacion**.

GEODIA Social Observatory queda como `INTERNAL_RESEARCH`. DUAT v2 fue absorbido
como contratos, tests, hashing y documentos de laboratorio, no como dataset
publicable ni claim cientifico. El CLI offline reproduce intake, scenario report
y backtest. La fuente fuera de allowlist falla correctamente.

Bloqueos que siguen:

- datos historicos reales con licencia y atribucion;
- backtests historicos no sinteticos;
- claims con incertidumbre visible por cada salida;
- publicacion externa;
- EEG/neurociencia real;
- Gemma/vLLM/Ray/LoRA/model surgery.

## Obs Info Kernel

Decision: **GO interno / BLOCK publicacion**.

Se absorbio de forma controlada `obs_info_kernel_package.zip` como laboratorio
interno en `research\obs-info-kernel`, sin `__pycache__`, `.pyc`, `_out`,
corpus runs ni reportes generados del ZIP original. El README local queda
marcado `INTERNAL_RESEARCH / DO_NOT_PUBLISH`.

Las fuentes nuevas de Downloads quedaron registradas en intake con hashes,
lineas, decisiones y riesgos. La revision tecnica esta en
`docs\OBS_INFO_KERNEL_REVIEW_2026-05-01.md`. La utilidad aprobada es
anti-informacion, informacion oscura, brechas de calibracion y continuidad por
`SESSION_FINGERPRINT`; no es claim de verdad, consciencia, fisica ni novedad
validada.

Actualizacion EOR/AIA: la fuente
`C:\Users\L-Tyr\Downloads\Sí, Luis René. Radicalmente. Has pu.txt` quedo
registrada como `EXTERNAL_EOR_AIA_TOPOLOGY_SYNTHESIS`, decision
`keep_gated/eor_aia_entropy_topology_synthesis`. Se implementaron en el kernel
interno `EORCalculator`, `EpistemicGuard`, `EquivalenceTester`,
`OperatorProfiler`, `HypothesisScorer` y estados
`dark_candidate/dark_testable/dark_validated/dark_rejected`. La revision sanitizada esta en
`docs\OBS_EOR_AIA_TOPOLOGY_REVIEW_2026-05-01.md`.

Actualizacion Atlas: la direccion se fija como `AIA = Atlas de Operadores
Perdidos / Operator Discovery Engine`. La unidad de analisis pasa de documento
a perfil `K_source`: conceptos, claims, bordes, omisiones, metaforas,
ecuaciones, tipo de evidencia, `R_source`, `Phi_source` y estatus epistémico.
El reporte del kernel ahora incluye `operator_profiles`, `operator_atlas` e
`hypotheses` con falsador.

Regla añadida: `R_info` puede ser entropia condicional normalizada solo con
distribucion definida; `R_operativo`, `R_cognitivo` y `R_fisico` son capas
distintas. No publicar frases como `R es entropia`, `controlar R es controlar
la realidad`, prueba de conciencia, nueva fisica o sustituto de termodinamica.

Bloqueos que siguen:

- validar hallazgos externos con fuentes primarias;
- decidir licencia antes de cualquier publicacion;
- mantener claims publicos low-claim;
- agregar cache/rate limits/fixtures antes de loops con APIs academicas;
- validar EOR_graph_proxy con corpus real antes de cualquier claim;
- validar `K_source` y `OperatorAtlas` con corpus real antes de convertirlo en producto;
- dejar topologia `C_ij` como extra opcional con pruebas y frontera de claims;
- no mover a `packages\open-dev` ni publicar en GitHub hasta release gate propio.

## Comercial

Decision: **REVIEW local**.

Se limpiaron los dos hallazgos de secret scan:

- `apps\commercial\asistente-negocio\scripts\check-public-safe.cjs`
- `apps\commercial\flujocrm\installer\BUILD.md`

Asistente y FlujoCRM ahora dan `count_reported=0` en secret scan. Asistente
pasa `npm run check` y `npm audit --omit=dev --audit-level=high`. FlujoCRM ya
tiene `package-lock.json`, `npm run check` con smoke de main/preload, `npm audit
--json` con `total=0`, y ZIP fuente local privado en
`releases\paid-apps\flujocrm.zip` con artifact scan `count_reported=0`. Argus
pasa build/typecheck en copia temporal y auditoria con cero vulnerabilidades.
Mini Office pasa pytest.

Se genero instalador Windows x64 QA para FlujoCRM, pero no se instalo en maquina
limpia ni se publico nada. No hay `.dmg`. Ya existe matriz legal/comercial draft
en `docs\legal\COMMERCIAL_RELEASE_LEGAL_MATRIX_2026-05-01.md`, pero sigue
marcada `LEGAL_REVIEW_REQUIRED`. Quedan pendientes soporte final,
privacy/refund/terms finales por plataforma, code signing o aviso unsigned y
revision humana.

Decision comercial cerrada: FlujoCRM sale standalone primero como producto
Windows x64; `Pack Empresarial` queda como bundle posterior. No se prepara
`.dmg` para el primer release salvo que el objetivo comercial cambie.

Paquetes fuente locales comerciales generados y escaneados:

| ZIP | bytes | sha256 | scan |
|---|---:|---|---|
| `releases\paid-apps\argus-desktop.zip` | 7006395 | `b8b8bf292e4d72267a6c3a6683cf759e5b60f514e4c710f5880e5770f0c9bbfb` | 0 findings |
| `releases\paid-apps\asistente-negocio.zip` | 6780591 | `ce6a77299363ff66c7b33ef6542a0f1f3eeb1fea9955f00b0f91eacdfc41d4af` | 0 findings |
| `releases\paid-apps\flujocrm.zip` | 99795 | `f4c4be4aadfee141993047ad383fb263c6ead7b5fbb9dde7b6dca753e628e3c4` | 0 findings |
| `releases\paid-apps\mini-office.zip` | 81438 | `fe05d7997b7a4b8a8237a876fff6e4cdc970acddede750f1e7677dbb67d54ad8` | 0 findings |

Frontera comercial adoptada: `docs\product\paid-app-deliverable-boundary-2026-05-01.md`
define estos ZIPs como artefactos internos de QA, no como descargas publicas por
defecto. FlujoCRM queda recomendado como standalone primero y bundle despues.

Instalador FlujoCRM QA:

| Artefacto | bytes | sha256 | scan | firma |
|---|---:|---|---|---|
| `apps\commercial\flujocrm\dist\FlujoCRM-Setup-1.0.0.exe` | 103730060 | `b7ba740ad82e976dd84fcfc959e78f9a9c9db50117cfcdf419fed106f664723f` | 0 findings | NotSigned |

## Wave FC Local Pilot

Decision: **LOCAL_DEMO_READY / BLOCK publicacion**.

La direccion de producto existe en:

- `docs\product\wave-collapse.md`
- `docs\product\wave-fc-client-operating-model.md`

El carril correcto es piloto local/privado de bajo claim: hashes, copia de
trabajo, diff/redline, decision log, evidence manifest y rollback pack. Ya existe
evidence pack local con documentos sinteticos `.md`/`.docx` y CSV, y el release
gate marco `local_demo_ready=true` con `public_publication_ready=false`.

No se declara paquete vendible ni publicable: ya hay capturas desktop/mobile,
pero faltan EULA/legal, docs de instalacion/listing public-safe y QA visual DOCX.
El render visual quedo
bloqueado porque no hay `@oai/artifact-tool` ni `soffice/libreoffice` disponible
en este host. El video queda opcional; no es requisito del cierre actual.

## Readiness Actual

| dimension | score | decision |
|---|---:|---|
| Open-dev local packages | 95/100 | GO local |
| Secret safety por producto/ZIP | 95/100 | GO local en allowlists |
| GEODIA interno reproducible | 85/100 | GO interno |
| Obs Info Kernel | 84/100 interno | GO interno / BLOCK publicacion |
| Comercial local | 74/100 | REVIEW |
| Wave FC pilot | 68/100 | LOCAL_DEMO_READY / BLOCK publicacion |
| Publicacion externa | 0/100 | BLOCK |

Score operativo vigente: **78/100 para cierre local por carriles**.

Score de publicacion externa: **BLOCK**, sin porcentaje de salida, porque exige
ActionGate, revision legal, aprobacion humana y canal concreto.

## Cambios Hechos En Esta Sesion

- Regenerados: `release_manifests\*.json`.
- Regenerados: `releases\free-dev\*.zip`.
- Actualizado por script: `qa_artifacts\release_validation\free-dev-smoke.json`.
- Editado: `apps\commercial\asistente-negocio\scripts\check-public-safe.cjs`.
- Editado: `apps\commercial\flujocrm\installer\BUILD.md`.
- Creado: `MASTER_PLAN_STATUS_2026-05-01.md`.

## Siguiente Cierre De Menor Tiempo

1. Comercial: preparar instaladores y cerrar revision legal final sin publicar.
2. FlujoCRM: probar instalador Windows QA en maquina limpia y cerrar icono, legal, code signing/skip-signing documentado; `.dmg` fuera del primer release.
3. Wave FC: cerrar QA visual DOCX, legal e instalacion/listing antes de vender o publicar; video queda opcional.
4. Open-dev: si el usuario autoriza accion externa, pasar por ActionGate antes
   de push/publicacion.
