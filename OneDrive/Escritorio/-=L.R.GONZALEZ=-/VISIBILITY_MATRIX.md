# VISIBILITY_MATRIX

Fecha: 2026-05-01

Regla central: si hay duda, `UNKNOWN_REVIEW_REQUIRED`. El videojuego y TCG quedan fuera de releases publicos.

| path | classification | reason | risk | recommended_action |
|---|---|---|---|---|
| `packages\open-dev\obsai-core` | OPEN | paquete MIT extraido por allowlist | claims `DEMO_ONLY` si no hay calibracion real | publicar solo con claims boundary y tests |
| `packages\open-dev\residueos` | OPEN | paquete MIT extraido por allowlist | runtime local excluido; thresholds demo | publicar como tooling, no como ciencia validada |
| `packages\open-dev\observacionismo-gate` | OPEN | SDK MIT aislado | no debe absorber runtime Claudio | mantener dependencia cero y notices |
| `packages\open-dev\claudio-os-blueprint` | OPEN | blueprint MIT aislado | ISO/QEMU no verificados | publicarlo solo como blueprint/handoff |
| `packages\open-dev\gemma-observacionismo-cleanup` | OPEN | toolkit MIT nuevo con fixtures sinteticos | riesgo de claims exagerados si se vende como verdad absoluta | mantenerlo como metodo de limpieza/observacion |
| `packages\open-dev\obs-safe-integration-kit` | OPEN | kernel MIT local-first con ObservationEnvelope, EstadoPSI, ActionGate, EvidenceStore y wrappers dry-run | wrappers externos podrian sobreprometer seguridad o ejecutar acciones si se integran mal | publicar solo con `CLAIMS.md`, `PRIVATE_EXCLUSIONS.md`, tests, secret scan 0 y ActionGate por destino |
| `packages\open-dev\duat-genesis` | OPEN_PUBLIC_REPO_LIVE | sandbox sintetico MIT con `GenesisState`, `GenesisRule`, `Observation`, `SimulationRun`, reportes y falsadores; staging local limpio `3488b49`; repo publico `https://github.com/Lutren/duat-genesis` | riesgo de que terceros lo vendan como prediccion social, biologica, neurologica o nueva fisica | mantener `CLAIMS.md`, `PRIVATE_EXCLUSIONS.md`, tests, secret scan 0, path/claims scan 0 y copy `SYNTHETIC_ONLY` |
| `hackathons\google-rapid-agent-2026` | OPEN_PUBLIC_REPO_LIVE | scaffold MIT para Google Cloud Rapid Agent Hackathon; repo `https://github.com/Lutren/rapid-agent-guardian` | no debe absorber runtime privado, prompts, MEDIOEVO canon ni RPG/TCG; partner MCP real pendiente de detalles oficiales | mantener sincronizado solo desde staging limpio, con scan y sin `runtime/` |
| `research\geodia-social-observatory` | INTERNAL_RESEARCH | MVP local privado con contratos `claudio.social_*`, fixtures offline, hash y backtest | riesgo de claims si se presenta como prediccion o se usan fuentes sin licencia revisada | mantener `publication_gate=BLOCK`; no publicar sin ActionGate, legal y backtests reales |
| `research\obs-info-kernel` | INTERNAL_RESEARCH | kernel limpio para anti-informacion, informacion oscura, EOR_graph_proxy, perfiles `K_source`, Operator Atlas, guardas epistémicas, equivalencia operacional, HypothesisScorer y continuidad `SESSION_FINGERPRINT` | riesgo de claims fuertes si rareza, topologia, conciencia o entropia se presentan como verdad o novedad validada; licencia no cerrada | mantener interno; validar fuentes primarias/licencia/claims antes de cualquier open-dev o producto |
| `apps\commercial\argus-desktop` | COMMERCIAL_OR_INTERNAL | app escritorio separada | requiere UX/public-safe review antes de venta | mantener propietario; excluir `node_modules` y `dist` |
| `apps\commercial\asistente-negocio` | COMMERCIAL | app comercial separada | Windows current-user QA local; requiere clean VM/legal/soporte/signing | release solo con checklist comercial |
| `apps\commercial\flujocrm` | COMMERCIAL | app comercial separada con lockfile/audit/smoke, ZIP fuente, Windows installer, current-user install/launch/uninstall QA, SQLite storage E2E y customer pilot copy verificados | falta clean VM, revision legal y firma/unsigned decision | release solo con checklist comercial |
| `apps\commercial\mini-office` | COMMERCIAL | runtime local verificado; copy/licencia/installers limpiados | legal, clean-machine, paquete final y checkout | no vender hasta cierre comercial final |
| `packages\paid\duat-templates` | COMMERCIAL_PUBLISHED | pack comercial de plantillas sinteticas para DUAT Genesis; ZIP, manifest, listing, scans y path/claims scan limpios; Gumroad `https://lrgonzalez.gumroad.com/l/duat-templates` | puede confundirse con DUAT Geodia o con validacion cientifica si el copy se exagera | vender solo como plantillas sinteticas; no incluir DUAT Geodia, RPG/TCG, datasets reales ni claims de prediccion |
| `website\wave-collapse.html` | COMMERCIAL_DRAFT | landing local MVP 1 Document Collapse sin deploy | riesgo de claims si se publica sin revision; canal de interes por mailto | mantener noindex, no desplegar sin ActionGate y prueba con documentos sanitizados |
| `docs\product\wave-collapse.md` | COMMERCIAL_DRAFT | README de producto public-safe | no sustituye spec interna ni autoriza venta | usar como orientacion de producto Document Collapse |
| `books\editorial` | BOOKS_EDITORIAL | muestras/borradores public-safe | riesgo de incluir libros completos | mantener all rights reserved |
| `game-private` | PRIVATE_BOUNDARY | frontera/documentacion | no es destino de fuente activa sin coordinar al agente del juego | no mover MetaEvo/TCG aqui todavia |
| `docs\developer\OPEN_SOURCE_MAX_PATRIMONY_IMPLEMENTATION_2026-05-02.md` | GOVERNANCE_PUBLIC_SAFE | decision open-source-max con frontera patrimonial | no sustituye licencia ni publicacion real | usar para orientar staging GitHub |
| `docs\developer\TECHNOLOGY_IMPLEMENTATION_BACKLOG_2026-05-02.md` | GOVERNANCE_PUBLIC_SAFE | backlog tecnico derivado de curador | no prueba implementacion final | convertir en issues/tareas por repo |
| `docs\publishing\GITHUB_PUBLIC_SANITIZED_WHITEPAPERS_2026-05-02.md` | GOVERNANCE_PUBLIC_SAFE | cola de whitepapers low-claim | no publicar si hay rutas/secrets/claims fuertes | usar como plantilla de repo |
| `docs\business\PATRIMONIO_DIGITAL_PRIVATE_ACTIONS_2026-05-02.md` | PRIVATE_GOVERNANCE | checklist patrimonial redactado | no debe contener secretos ni sustituir abogado/contador | mantener privado y completar fuera de repos publicos |
| `docs\product\AGENT_PRODUCT_FICHAS_2026-05-02.md` | GOVERNANCE_PUBLIC_SAFE | fichas tecnica/comercial/agente sin secretos | puede quedar desactualizado si productos cambian | usar como mapa operativo para UI paga/open core |
| `docs\design\MEDIOEVO_AGENT_CITY_UI_SYSTEM_2026-05-02.md` | GOVERNANCE_PUBLIC_SAFE | sistema visual/UX sin assets privados copiados | riesgo de usar RPG assets sin permiso si se interpreta mal | usar solo como direccion; assets privados siguen excluidos |
| `docs\developer\DEPENDENCY_ADOPTION_GATE_2026-05-02.md` | GOVERNANCE_PUBLIC_SAFE | gate de dependencias por licencia/seguridad/claims | snapshots externos caducan | refrescar antes de instalar o publicar |
| `docs\developer\CLAIM_FALSIFICATION_REGISTER_2026-05-02.md` | GOVERNANCE_PUBLIC_SAFE | registro de claims y falsacion | no sustituye pruebas reales | mantener claims fuertes fuera de copy hasta `VERIFIED` |
| `docs\developer\CURADOR_ALWAYS_ON_PROTOCOL_2026-05-03.md` | GOVERNANCE_PUBLIC_SAFE | regla de curador obligatorio para rutas sucias, fuentes nuevas y residuos | no autoriza borrar, mover o publicar; solo obliga a registrar y verificar | usar `curador_preflight.py` antes de usar/copiar/descartar material no fichado |
| `docs\developer\CURADOR_SETO_GLOBAL_OPERATING_CONTRACT_2026-05-05.md` | GOVERNANCE_PUBLIC_SAFE | contrato operativo de carpetas SETO, envelopes, ActionGate, WitnessLog y comunicacion entre agentes | no autoriza creacion fisica de carpetas ni borrado directo | usarlo como contrato antes de limpieza o handoff |
| `docs\intake\GLOBAL_CURADOR_SETO_AUDIT_2026-05-05.md` | GOVERNANCE_EVIDENCE | reporte local de inventario global seco con hashes, duplicados, grandes y candidatos | contiene rutas locales y no es copy publico | usar solo como evidencia interna; no publicar |
| `docs\publishing\OPEN_CORE_UI_PAID_PUBLICATION_RUNBOOK_2026-05-02.md` | GOVERNANCE_PUBLIC_SAFE | runbook GitHub/website/Gumroad | no autoriza publicar por si solo | usar con ActionGate y scans |
| `-=MEDIOEVO=-\-=LIBROS\claudio\memory_vault` | GOVERNANCE_PRIVATE_INDEX | MemPalace limpio para Downloads, DUAT, NEUROSTATE, papers y split comercial/open-source | contiene rutas locales y decisiones internas; no es public copy | usar como indice operativo privado, extraer solo docs public-safe |
| `qa_artifacts\release_validation\external_repos_verification_2026-05-02.json` | GOVERNANCE_EVIDENCE | snapshot GitHub API para proyectos externos | licencias/status pueden cambiar; no autoriza vendoring | refrescar antes de dependencia real o publicacion |
| `apps\residueos` | OPEN_OR_COMMERCIAL_CANDIDATE | MVP local de action gate con SQLite, CLI, API HTTP y tests | thresholds/calibracion son `DEMO_ONLY`; falta dataset real y decision de licencia final | mantener allowlist, ejecutar tests, no vender metricas como ciencia validada |
| `packages\obsai-core` | OPEN_CANDIDATE | nucleo operacional sin dependencias con gate, residuo, fingerprint, simulacion deterministica y CLI | thresholds, pesos y simulacion son `DEMO_ONLY`; no debe absorber research/game/lore | mantener paquete public-safe, calibrar con dataset real antes de claims |
| `-=MEDIOEVO=-\-=LIBROS\claudio\sdk` | OPEN_CANDIDATE | SDK `observacionismo-gate`, MIT declarado | falta validar LICENSE/README/tests completos | auditar y extraer como package dev |
| `PRODUCTOS_MEDIOEVO\03_OPEN_SOURCE_GITHUB` | OPEN_CANDIDATE | carpeta de staging open source | puede contener mezclas no revisadas | escanear antes de publicar |
| `PRODUCTOS_MEDIOEVO\claudio_os_blueprint` | OPEN_CANDIDATE | blueprint pequeno y duplicado controlable | ISO/QEMU no verificados | publicar solo como blueprint/handoff, no como OS terminado |
| `tools\claw-code` | OPEN_CANDIDATE | herramienta dev separada | `target/` pesado y plugins no trackeados | limpiar build outputs antes de release |
| `-=MEDIOEVO=-\-=LIBROS\claudio\brain_os` | OPEN_CANDIDATE | tooling Brain OS | estado runtime puede depender de entorno local | separar CLI/docs de runtime privado |
| `-=MEDIOEVO=-\-=LIBROS\claudio\observacionismo` | OPEN_OR_BOOKS_REVIEW | nombre dev/canon | puede mezclar teoria/libro y toolkit | clasificar archivo por archivo |
| `-=MEDIOEVO=-\-=LIBROS\-=CEREBRO=-\-=PSI=-` | UNKNOWN_REVIEW_REQUIRED | PSI/Observacionismo canon + framework | riesgo de publicar libro/ensayo completo | extraer toolkit dev y samples; no abrir todo |
| `-=MEDIOEVO=-\-=LIBROS\claudio\products\asistente_negocio` | COMMERCIAL | app Electron vendible con release | necesita privacy/terms/support y verificar public-safe | preparar release comercial |
| `-=MEDIOEVO=-\-=LIBROS\claudio\products\crm` | COMMERCIAL | app Electron vendible | falta matriz QA/legal | preparar checklist comercial |
| `-=MEDIOEVO=-\-=LIBROS\claudio\apps\argus_desktop` | COMMERCIAL_OR_INTERNAL | desktop app con build/typecheck | puede contener telemetria interna o assets privados | auditar UX y limite publico |
| `-=MEDIOEVO=-\-=LIBROS\claudio\mini_office` | COMMERCIAL_OR_OPEN_CORE | app usuario/dev legacy | no es canon actual | no publicar; usar `apps\commercial\mini-office` como ruta operativa |
| `-=MEDIOEVO=-\-=LIBROS\claudio\website` | COMMERCIAL_SURFACE | landing/website activo | assets y productos mezclados | separar assets publicos y privados |
| `PRODUCTOS_MEDIOEVO\01_LIBROS_Y_BUNDLES` | COMMERCIAL_BOOKS | libros/bundles | no regalar libros completos | preparar Gumroad/website solo con decision explicita |
| `PRODUCTOS_MEDIOEVO\02_SOFTWARE_LOCAL` | COMMERCIAL | software local | faltan pruebas por producto | crear manifests y smoke tests |
| `PRODUCTOS_MEDIOEVO\content_forge` | COMMERCIAL_OR_OPEN_CANDIDATE | herramienta de contenido | licencia/alcance no claros | decidir capa antes de publicar |
| `-=MEDIOEVO=-\-=LIBROS\MEDIOEVO_BESTSELLER_OUTPUT` | BOOKS_EDITORIAL | salida editorial | puede contener libros completos | no publicar en open source |
| `-=MEDIOEVO=-\-=LIBROS\vault_medioevo` | BOOKS_EDITORIAL_PRIVATE_REVIEW | vault/canon | IP central | publicar solo samples aprobados |
| `-=MEDIOEVO=-\-=LIBROS\metaevo-tcg` | PRIVATE | juego/TCG con scripts build/lint/package | fuente de videojuego y assets | no mover a carpetas publicas, no incluir en packages |
| `-=MEDIOEVO=-\-=LIBROS\claudio\tcg` | PRIVATE_REVIEW | TCG dentro de Claudio | posible asset/lore de juego | excluir de releases publicos |
| `-=MEDIOEVO=-\-=LIBROS\claudio\runtime\game_bridge` | PRIVATE_REVIEW | puente runtime/game | riesgo de filtrar integracion del juego | excluir de open/free |
| `PRODUCTOS_MEDIOEVO\04_AUDIOVISUAL_Y_TCG` | PRIVATE_OR_COMMERCIAL_REVIEW | TCG/audiovisual | puede tocar videojuego o assets sensibles | revisar manualmente antes de vender/publicar |
| `-=MEDIOEVO=-\-=LIBROS\claudio\tools\pentest_repos` | PRIVATE_SECURITY_REVIEW | repos de pentest/ofensivos | riesgo legal/seguridad/licencia | no publicar ni empaquetar |
| `-=MEDIOEVO=-\-=LIBROS\claudio\tools\vendor` | VENDOR_REVIEW | terceros | licencias y dependencias ajenas | excluir de productos propios salvo permiso |
| `-=MEDIOEVO=-\-=LIBROS\.skills` | ARCHIVE_OR_VENDOR | skills/agentes de terceros | duplica `claudio\.skills` | no incluir en release |
| `-=MEDIOEVO=-\-=LIBROS\claudio\.skills` | ARCHIVE_OR_VENDOR | skills/agentes de terceros | mas de 10k archivos, vendors | no incluir en release |
| `-=MEDIOEVO=-\CLAUDIO - researchs` | ARCHIVE_OR_SOURCE_REVIEW | investigacion/historico/staging | contiene docs viejos y staging GitHub | no publicar directo |
| `_ARCHIVAR`, `_archive`, `archive`, `_legacy`, `_trash_revisar`, `_SNAPSHOTS` | ARCHIVE | residuo reconocido | puede contener secretos antiguos | fuera de releases |
| `.claw`, `.claude`, `.wrangler`, `.test_*`, `.pytest_cache` | LOCAL_STATE | estado local/herramientas | secretos/sesiones/caches | fuera de releases |

## Archivos/rutas que no deben entrar a releases publicos

- `-=MEDIOEVO=-\-=LIBROS\metaevo-tcg\**`
- `-=MEDIOEVO=-\-=LIBROS\claudio\tcg\**`
- `-=MEDIOEVO=-\-=LIBROS\claudio\runtime\game_bridge\**`
- `PRODUCTOS_MEDIOEVO\04_AUDIOVISUAL_Y_TCG\**` hasta revision manual
- `**\.env`, `**\.env.*` salvo ejemplos sin secreto
- `**\*secret*`, `**\*token*`, `**\*credential*`
- `**\*.zip`, `**\*.exe`, `**\*.apk` salvo release comercial explicitamente seleccionado
- `**\.git\**`, `**\node_modules\**`, `**\.venv*\**`, `**\target\**`, `**\__pycache__\**`
- `**\.skills\**` salvo que se cree paquete independiente revisado
- `claudio\tools\pentest_repos\**`
- `claudio\tools\vendor\**`

## Decision operativa

No hay todavia una frontera tecnica suficiente para empaquetar releases publicos. La matriz debe convertirse en:

1. allowlist por release (`free-dev`, `paid-apps`, `editorial-samples`);
2. denylist global (`private-game`, secretos, vendors, builds locales);
3. manifests con hashes para cada paquete generado.

Actualizacion 2026-05-02: el carril nuevo `GitHub publico saneado` permite abrir
herramientas y whitepapers solo desde staging limpio. No autoriza publicar el
workspace completo ni fuentes crudas de Downloads/E:.
