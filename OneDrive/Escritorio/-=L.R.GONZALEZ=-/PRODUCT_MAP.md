# PRODUCT_MAP

Fecha: 2026-05-01

Raiz auditada: `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-`

Este mapa es inferido por rutas, manifests y nombres. No es autorizacion de publicacion.

## Criterio de capas

| capa | regla |
|---|---|
| OPEN | herramientas dev publicables solo si no contienen secretos, assets privados, builds, vendors con licencias incompatibles ni contenido editorial completo |
| COMMERCIAL | apps, bundles, PDFs, productos, instaladores y assets vendibles |
| BOOKS_EDITORIAL | libros, canon, ensayos, companions, materiales narrativos |
| PRIVATE | videojuego, TCG/game source, builds internos, lore privado y assets sensibles |
| ARCHIVE | duplicados, vendors, snapshots, experimentos viejos, logs, caches, builds locales |
| UNKNOWN_REVIEW_REQUIRED | rutas ambiguas o con capas mezcladas |

## Mapa activo final

| ruta | producto/capa | clasificacion | licencia | estado |
|---|---|---|---|---|
| `packages\open-dev\obsai-core` | Observacionismo / PSI-IA operational core | OPEN | MIT | extraido por allowlist; fuente legacy queda sin publicar completa |
| `packages\open-dev\residueos` | ResidueOS action gate | OPEN | MIT | extraido por allowlist; runtime state excluido |
| `packages\open-dev\observacionismo-gate` | SDK Observacionismo gate | OPEN | MIT | extraido desde `claudio\sdk`; sin runtime Claudio |
| `packages\open-dev\claudio-os-blueprint` | ClaudioOS blueprint | OPEN | MIT | blueprint/handoff; no ISO terminado |
| `packages\open-dev\gemma-observacionismo-cleanup` | limpieza/observacion de modelos | OPEN | MIT | nuevo toolkit publico-safe con fixtures sinteticos |
| `packages\open-dev\obs-safe-integration-kit` | OBS Safe Integration Kit / ActionGate adapter kernel | OPEN | MIT | ZIP/staging local verificados; manifest 20 files/0 blocked; secret scans fuente/ZIP/staging `0`; publicacion externa `BLOCK` |
| `packages\open-dev\duat-genesis` | DUAT Genesis synthetic simulation sandbox | OPEN_PUBLIC_REPO_LIVE | MIT | paquete publico sintetico creado; tests `3 passed`; ZIP `f672d974...`, staging Git limpio `3488b49`, repo publicado `https://github.com/Lutren/duat-genesis`; no contiene ingenieria privada DUAT Geodia, RPG/TCG ni claims cientificos |
| `hackathons\google-rapid-agent-2026` | Agent Safety Gate for Real Work / Google Rapid Agent Hackathon | OPEN_PUBLIC_REPO_LIVE | MIT | repo limpio publicado en `https://github.com/Lutren/rapid-agent-guardian`; cloud/partner MCP pendiente de reglas finales |
| `research\geodia-social-observatory` | GEODIA Social Observatory | INTERNAL_RESEARCH | propietario/research | MVP local privado; contratos sociales, fixtures offline, backtest y publication gate `BLOCK` |
| `research\obs-info-kernel` | Observacionismo anti-informacion / informacion oscura / EOR / Operator Atlas kernel | INTERNAL_RESEARCH | license review required | paquete limpio extraido desde Downloads; EOR/AIA, perfiles K_source, guardas epistémicas, HypothesisScorer y estados dark_* integrados; tests pasan; no publicar ni mover a open-dev sin validacion de claims/licencia |
| `apps\commercial\argus-desktop` | Argus desktop | COMMERCIAL_OR_INTERNAL | propietario comercial | extraido por allowlist; artifacts generados denegados |
| `apps\commercial\asistente-negocio` | Asistente Negocio | COMMERCIAL | propietario comercial | Windows current-user installer/E2E QA; clean VM/legal/signing pendientes |
| `apps\commercial\flujocrm` | FlujoCRM | COMMERCIAL | propietario comercial | lockfile/audit/smoke, ZIP fuente, Windows installer, current-user install/launch/uninstall QA, SQLite storage E2E y customer pilot copy verificados; clean VM y firma/legal pendientes |
| `apps\commercial\mini-office` | Mini Office | COMMERCIAL | propietario comercial | runtime/test local OK; copy/licencia/installers/generators limpiados; venta bloqueada por legal, clean-machine, paquete final y checkout |
| `packages\paid\duat-templates` | DUAT Templates paid pack | COMMERCIAL_PUBLISHED | propietario comercial | ZIP `03c926b5...`, manifest 8 files/0 blocked, source/artifact secret scans 0, path/claims scan OK, Gumroad publicado `https://lrgonzalez.gumroad.com/l/duat-templates` |
| `docs\product\wave-collapse.md` | Wave Function Collapse | COMMERCIAL_DRAFT | propietario comercial | MVP 1 Document Collapse local-only; landing local no desplegada |
| `books\editorial` | canon, muestras y borradores | BOOKS_EDITORIAL | all rights reserved | solo material editorial aprobado; no libros completos movidos |
| `game-private` | frontera del videojuego | PRIVATE_BOUNDARY | all rights reserved | documentacion/frontera solamente; fuente activa no movida |
| `docs\developer\OPEN_SOURCE_MAX_PATRIMONY_IMPLEMENTATION_2026-05-02.md` | Open Source Max + Patrimony Guard | GOVERNANCE | n/a | decision de carril: abrir herramientas, proteger patrimonio |
| `docs\developer\TECHNOLOGY_IMPLEMENTATION_BACKLOG_2026-05-02.md` | Technology implementation backlog | GOVERNANCE | n/a | cola accionable desde curador |
| `docs\publishing\GITHUB_PUBLIC_SANITIZED_WHITEPAPERS_2026-05-02.md` | GitHub sanitized whitepaper queue | GOVERNANCE | n/a | whitepapers publicos low-claim en cola |
| `docs\business\PATRIMONIO_DIGITAL_PRIVATE_ACTIONS_2026-05-02.md` | Patrimonio digital actions | PRIVATE_GOVERNANCE | private | checklist redactado, no contiene secretos |
| `docs\product\AGENT_PRODUCT_FICHAS_2026-05-02.md` | Agent product fichas | GOVERNANCE | n/a | fichas tecnica/comercial/agente para open core + UI paga |
| `docs\design\MEDIOEVO_AGENT_CITY_UI_SYSTEM_2026-05-02.md` | MEDIOEVO Agent City UI System | GOVERNANCE | n/a | direccion visual comun ciudad de agentes |
| `docs\developer\DEPENDENCY_ADOPTION_GATE_2026-05-02.md` | Dependency adoption gate | GOVERNANCE | n/a | ficha antes de instalar dependencias |
| `docs\developer\CLAIM_FALSIFICATION_REGISTER_2026-05-02.md` | Claim falsification register | GOVERNANCE | n/a | prueba/falsacion o downgrade de claims fuertes |
| `docs\developer\CURADOR_ALWAYS_ON_PROTOCOL_2026-05-03.md` | Curador Always-On protocol | GOVERNANCE | n/a | regla obligatoria: verificar ficha, extraer tecnologia util, registrar frontera o descarte antes de actuar |
| `docs\developer\CURADOR_SETO_GLOBAL_OPERATING_CONTRACT_2026-05-05.md` | Curador SETO global contract | GOVERNANCE | n/a | contrato activo para INBOX/CURADURIA/COMMS, ObservationEnvelope, ActionGate, WitnessLog y limpieza global seca |
| `docs\intake\GLOBAL_CURADOR_SETO_AUDIT_2026-05-05.md` | Global Curador SETO dry audit | GOVERNANCE_EVIDENCE | n/a | inventario seco de 81,107 archivos en workspace, Downloads, Desktop y E:; no autoriza borrado |
| `docs\publishing\OPEN_CORE_UI_PAID_PUBLICATION_RUNBOOK_2026-05-02.md` | Open core + paid UI publication runbook | GOVERNANCE | n/a | orden GitHub/website/Gumroad con gates |
| `-=MEDIOEVO=-\-=LIBROS\claudio\memory_vault` | MemPalace / Downloads curated index | GOVERNANCE_PRIVATE_INDEX | n/a | indice limpio de Downloads, DUAT, NEUROSTATE, papers, split comercial/open-source y verificacion GitHub; no copia fuentes crudas |
| `qa_artifacts\release_validation\external_repos_verification_2026-05-02.json` | External project verification evidence | GOVERNANCE_EVIDENCE | n/a | GitHub REST API snapshot para decidir dependencias; no autoriza vendoring |

## Mapa legacy/inicial por ruta

| ruta | producto/capa probable | clasificacion | razon | accion recomendada |
|---|---|---|---|---|
| `apps\residueos` | ResidueOS action gate | OPEN_OR_COMMERCIAL_CANDIDATE | MVP local con salida `APPROVE`/`REVIEW`/`BLOCK`, SQLite, CLI, API y tests | calibrar con dataset real antes de claims; decidir licencia/canal |
| `packages\obsai-core` | Observacionismo / PSI-IA operational core | OPEN_CANDIDATE | paquete sin dependencias con residuo, regimen, gate, fingerprint, simulacion y CLI | mantener sin research/game/lore; publicar solo con licencia y claims boundary |
| `-=MEDIOEVO=-\-=LIBROS\claudio` | Claudio runtime/ecosistema | UNKNOWN_REVIEW_REQUIRED | mezcla core, apps, editorial, comercial, website, vendors, secretos y builds | dividir por subproducto antes de publicar |
| `-=MEDIOEVO=-\-=LIBROS\claudio\sdk` | `observacionismo-gate` SDK | OPEN_CANDIDATE | `pyproject.toml` declara MIT y dependencia cero | verificar `LICENSE`, README, tests y secretos |
| `-=MEDIOEVO=-\-=LIBROS\claudio\brain_os` | Brain OS tooling | OPEN_CANDIDATE | herramienta dev/runtime | verificar estado build y limite ClaudioOS |
| `-=MEDIOEVO=-\-=LIBROS\claudio\claudio_os` | Claudio OS tooling | OPEN_OR_COMMERCIAL_REVIEW | OS tooling, build no cerrado | no vender ni publicar como ISO hasta QEMU/ISO verificado |
| `PRODUCTOS_MEDIOEVO\claudio_os_blueprint` | blueprint ClaudioOS | OPEN_CANDIDATE | staging limpio y pequeno | comparar con copias y elegir canon |
| `-=MEDIOEVO=-\-=LIBROS\claudio\_workspace\claudio_os_blueprint` | copia blueprint | ARCHIVE_OR_DUPLICATE_REVIEW | 33 archivos, similar a `PRODUCTOS_MEDIOEVO` | marcar fuente canon antes de borrar/mover |
| `-=MEDIOEVO=-\-=LIBROS\claudio\runtime\claudio_os_build\staging\claudio_os_blueprint` | staging build ClaudioOS | BUILD_STAGING | copia generada para build | excluir de releases publicos salvo paquete de build intencional |
| `-=MEDIOEVO=-\-=LIBROS\claudio\apps\argus_desktop` | Argus desktop | COMMERCIAL_OR_INTERNAL_APP | Vite/Electron, scripts reales | auditar UX, secretos, licencia y build |
| `-=MEDIOEVO=-\-=LIBROS\claudio\products\asistente_negocio` | Asistente negocio MEDIOEVO | COMMERCIAL | package final/release existentes | ruta legacy; canon actual en `apps\commercial\asistente-negocio` |
| `-=MEDIOEVO=-\-=LIBROS\claudio\products\crm` | FlujoCRM | COMMERCIAL | Electron app comercial | necesita docs, privacy, terms y smoke test |
| `-=MEDIOEVO=-\-=LIBROS\claudio\mini_office` | Mini Office legacy | COMMERCIAL_OR_OPEN_CORE | ruta legacy mezclada | no publicar; canon operativo actual esta en `apps\commercial\mini-office` |
| `-=MEDIOEVO=-\-=LIBROS\claudio\website` | sitio Claudio/MEDIOEVO | COMMERCIAL_SURFACE | 571 archivos, 231 MB | separar landing publica de assets privados |
| `-=MEDIOEVO=-\-=LIBROS\website` | sitio padre minimo | UNKNOWN_REVIEW_REQUIRED | solo 1 archivo detectado | comparar contra `claudio\website` |
| `-=MEDIOEVO=-\-=LIBROS\metaevo-tcg` | MetaEvo TCG / videojuego | PRIVATE | juego/TCG con build scripts y muchos cambios activos | no publicar, no mover a open, crear frontera privada |
| `-=MEDIOEVO=-\-=LIBROS\claudio\tcg` | TCG relacionado | PRIVATE_REVIEW | nombre TCG dentro de Claudio | excluir de paquetes publicos |
| `-=MEDIOEVO=-\-=LIBROS\claudio\runtime\game_bridge` | puente juego/runtime | PRIVATE_REVIEW | ruta game bridge | excluir de open/free |
| `PRODUCTOS_MEDIOEVO\04_AUDIOVISUAL_Y_TCG` | audiovisual/TCG | PRIVATE_OR_COMMERCIAL_REVIEW | TCG puede tocar videojuego/IP | no publicar hasta revisar contenido |
| `-=MEDIOEVO=-\-=LIBROS\MEDIOEVO_BESTSELLER_OUTPUT` | salida editorial/comercial | BOOKS_EDITORIAL | salida de libros/publicacion | separar samples publicos de libros completos |
| `-=MEDIOEVO=-\-=LIBROS\vault_medioevo` | canon/editorial | BOOKS_EDITORIAL_PRIVATE_REVIEW | vault de obra/canon | no publicar completo |
| `-=MEDIOEVO=-\-=LIBROS\-=CEREBRO=-\-=PSI=-` | Observacionismo / PSI-IA | BOOKS_EDITORIAL_AND_OPEN_REVIEW | contiene canon, libro, agente, framework y archivo | separar toolkit dev de ensayo/libro |
| `PRODUCTOS_MEDIOEVO\01_LIBROS_Y_BUNDLES` | libros/bundles | COMMERCIAL_BOOKS | staging de venta | revisar que no sea fuente publica |
| `PRODUCTOS_MEDIOEVO\02_SOFTWARE_LOCAL` | apps locales | COMMERCIAL | staging producto | preparar manifests y builds |
| `PRODUCTOS_MEDIOEVO\03_OPEN_SOURCE_GITHUB` | open source | OPEN_CANDIDATE | carpeta ya diseñada para GitHub | validar secretos/licencias |
| `PRODUCTOS_MEDIOEVO\05_BETAS_Y_PROXIMAMENTE` | betas | UNKNOWN_REVIEW_REQUIRED | preventa/betas | no publicar sin checklist |
| `PRODUCTOS_MEDIOEVO\content_forge` | herramienta contenido | COMMERCIAL_OR_OPEN_CANDIDATE | pyproject detectado y assets placeholder | decidir licencia y publico objetivo |
| `tools\claw-code` | herramienta dev | OPEN_CANDIDATE | repo separado Rust/Python | excluir `target/` y revisar no trackeados |
| `-=MEDIOEVO=-\CLAUDIO - researchs` | investigacion y staging | ARCHIVE_OR_SOURCE_REVIEW | research, staging GitHub, archivos historicos | no publicar directo |
| `-=MEDIOEVO=-\-=LIBROS\.skills` | vendor/herramientas agentes | VENDOR_ARCHIVE_REVIEW | 9148 archivos, 631 MB, varios repos | no mezclar con productos propios |
| `-=MEDIOEVO=-\-=LIBROS\claudio\.skills` | vendor/herramientas agentes | VENDOR_ARCHIVE_REVIEW | 10268 archivos, 192 MB | no mezclar con productos propios |
| `-=MEDIOEVO=-\-=LIBROS\claudio\tools\pentest_repos` | repos pentest/offensive | PRIVATE_SECURITY_REVIEW | herramientas de seguridad de terceros | no empaquetar ni publicar sin revision especifica |
| `-=MEDIOEVO=-\-=LIBROS\claudio\tools\vendor` | vendor externo | VENDOR_REVIEW | terceros, licencias diversas | mantener fuera de releases propios |

## Productos candidatos

### Gratis/dev

- ResidueOS (`apps\residueos`) como action gate local, con thresholds `DEMO_ONLY`
- obsai-core (`packages\obsai-core`) como nucleo operacional public-safe, con research claims bloqueados
- `observacionismo-gate` (`claudio\sdk`)
- Brain OS tooling (`claudio\brain_os`, `PRODUCTOS_MEDIOEVO\claudio_os_blueprint`)
- PSI-IA / Observacionismo toolkit extraido desde `-=CEREBRO=-\-=PSI=-`
- `tools\claw-code` si se limpia `target/` y plugins locales
- templates de agentes solo si son propios y con licencia clara
- `data-curation-observatory` como version publica generica del curador real, con demo sintetica
- `ai-web-gateway-observacionista` como gateway de observacion/evidence envelopes, sin credenciales ni browser action insegura
- `obs-info-kernel-lite` como claim registry/evidence store con corpus sintetico
- `obs-safe-integration-kit` como kernel local-first con `ObservationEnvelope`, `ActionGate`, `EvidenceStore`, wrappers dry-run y docs de frontera
- `observational-calibration-toolkit` como schemas/falsadores/calibracion operativa low-claim
- `duat-genesis` como laboratorio sintetico de simulacion observable/falsadores, sin RPG/canon privado ni claims de fisica validada
- `neurostate-ui` como prototipo local de observabilidad de estado, con privacidad y claims review antes de abrir
- `la-biblioteca-de-alejandria` como indice publico de repos saneados y fronteras

### Interno/research

- GEODIA Social Observatory (`research\geodia-social-observatory`): simulador local de epocas/cambios sociales con DUAT + Conway + Observacionismo. No publicable hasta snapshots licenciados, backtests historicos y ActionGate.
- Obs Info Kernel (`research\obs-info-kernel`): laboratorio interno para anti-informacion, informacion oscura, EOR_graph_proxy, perfiles `K_source`, Operator Atlas, guardas epistémicas, equivalencia operacional, scoring de hipotesis y continuidad por fingerprint. No publicable hasta validar fuentes primarias, licencia, claims y secret scan.

### Comerciales

- Asistente Negocio MEDIOEVO (`claudio\products\asistente_negocio`)
- FlujoCRM (`apps\commercial\flujocrm`)
- Mini Office (`apps\commercial\mini-office`)
- Argus desktop (`claudio\apps\argus_desktop`)
- Wave Function Collapse (`docs\product\wave-collapse.md`, `website\wave-collapse.html`) como MVP 1 Document Collapse local-only
- MEDIOEVO bundles y companion PDFs (`PRODUCTOS_MEDIOEVO\01_LIBROS_Y_BUNDLES`)
- website/landing propia (`claudio\website`)

### Libros/canon/editorial

- MEDIOEVO saga outputs
- `vault_medioevo`
- `-=CEREBRO=-\-=PSI=-\libro`
- El Observador / Observacionismo docs
- Companion docs y samples publicos por decidir

### Privado/no publicar

- `metaevo-tcg`
- `claudio\tcg`
- `claudio\runtime\game_bridge`
- todo asset/lore/build interno del juego
- `PRODUCTOS_MEDIOEVO\04_AUDIOVISUAL_Y_TCG` hasta revision manual

## Huecos de producto

- No existe catalogo unico de productos en la raiz.
- No existe frontera tecnica para excluir juego de paquetes publicos.
- No existe politica central de licencias por capa.
- No existe mapa canonico de que repo/subarbol es fuente de verdad.
- No existe release manifest que diga que entra y que no entra en cada ZIP.

## Siguiente paso recomendado

Crear en Fase 1:

- `TREE_PLAN.md`
- `MIGRATION_PLAN.md`
- `PRIVATE_GAME_BOUNDARY.md`
- `OPEN_SOURCE_STRATEGY.md`
- `COMMERCIAL_STRATEGY.md`
- `MIGRATION_MAP.md`
