# ASSUMPTIONS WABI-SABI

## 2026-05-20 - Wabi LLM Safe JSON Contract

- Assumption: los consumidores UI/API pueden leer `llm_status` cuando necesiten el estado interno del provider o CloudBudgetGate.
- Assumption: el contrato top-level `status=OK|REVIEW` es mas estable para UI, CLI y consumidores futuros que exponer estados internos como status principal.
- Assumption: guardar runtime JSON y WitnessLog redacted por respuesta es aceptable como evidencia local y no implica publicacion.
- Assumption: `Apply Local` seguira requiriendo confirmacion/gate separado aunque exista `patch_candidate`.
- Assumption: `tags` debe ayudar a UI/CLI a presentar estado operativo, pero no reemplaza ActionGate ni LocalApplyGate.

## 2026-05-19 - Wabi LLM Cloud Work Mode

- Assumption: el provider por defecto para esta fase es `nvidia` con alias `nano-30b`, salvo override por entorno.
- Assumption: si solo `WABI_LLM_PROVIDER_CLOUD_DEFAULT=1` esta activo, el modo correcto es dry-run proposal con `cloud_provider_called=false`.
- Assumption: los artefactos LLM proposal son evidencia local, no autorizacion de apply ni publicacion.
- Assumption: GraphicsBridge debe seguir `graphics_live=false` aunque el LLM proponga escenas o assets.

## 2026-05-19 - Wabi Work Mode v1

- Assumption: el operador usara Wabi para tareas locales pequenas y medianas antes de intentar release externo.
- Assumption: `http://127.0.0.1:8787/` sigue siendo la URL UI local esperada cuando el servidor Wabi esta activo.
- Assumption: `wabi` o `.\wabi.cmd` son los entrypoints correctos segun el PATH/shell local.
- Assumption: assets Du WABI pueden permanecer como candidatos internos, pero no publicarse sin provenance/licencia.
- Assumption: no full regression era necesaria en este cierre porque no hubo cambio de codigo.

## 2026-05-19 - WABI Assets Du WABI Local Integration + Release Gate

- Assumption: el uso local interno de cuatro PNGs re-encodeados es aceptable como `INTERNAL_REVIEWED_ASSET_CANDIDATE`, pero no equivale a aprobacion publica.
- Assumption: la ausencia de EXIF, secret-like findings, private path leaks y hashes duplicados reduce riesgo tecnico, pero no resuelve ownership/licencia.
- Assumption: el destino actual correcto para validacion UI es `-= BRAIN_OS =-\apps\local\wabi_ui\assets\wabi_du_wabi_20260519\`.
- Assumption: GitHub/medioevo.space deben tratarse como fase separada despues de provenance, staging limpio y scans finales.

## 2026-05-19 - Wabi UI TaskSpec Gate Preview v0.1

- Assumption: el preview puede usar defaults seguros cuando el TaskSpec no declara todos los campos de paths, tests o rollback.
- Assumption: `PathAllowlist` debe aparecer como gate futuro junto con `ActionGate`, `GhostGate`, `RollbackStore` y `TestRunner`, aunque no estuviera en el prompt minimo, porque reduce riesgo antes de cualquier apply local.
- Assumption: evidencia API + screenshot interactiva es suficiente para confirmar que la UI muestra Gate Preview sin activar ejecucion.
- Assumption: los artefactos runtime de smoke guardan resumen redacted, no prompts completos.

## 2026-05-19 - CloudBudgetGate UI Visual QA

- Assumption: mantener el servidor local corriendo en `127.0.0.1:8787` es deseable porque la mision era reiniciar/abrir la UI real.
- Assumption: evidencia screenshot + endpoint redacted es suficiente para confirmar visibilidad UI sin activar BrowserBridge live.
- Assumption: `build-assist-plan --dry-run` puede crear artefactos runtime de propuesta sin aplicar fuentes y sin incrementar presupuesto cloud completado.
- Assumption: los nombres de variables/env mostrados por status no son secretos; los valores siguen sin imprimirse.

## 2026-05-18 - Wabi fallback-only coding acceptance v0.2

- `LOCAL_FALLBACK_OLLAMA_AVAILABLE` se basa en lista local; no se uso para generar la propuesta.
- `DETERMINISTIC_STUB_USED` es aceptable para v0.2 porque el objetivo era probar el pipeline completo sin cloud.
- El resultado de acceptance se considera publicacion-bloqueada aunque sea local y redactado.

- `apps/local/wabi-sabi` es la ruta que el usuario quiere preservar como
  proyecto unico.
- Los scripts host pueden permanecer fuera si son wrappers hacia la ruta
  canonica y no contienen la implementacion principal.
- Configuracion de modelos sin valores secretos puede vivir en el canon.
- Loaders de secretos y stores locales requieren revision separada y no deben
  copiarse por absorcion automatica.
- Source cards, atlas, staging y protected IP no son proyectos Wabi-Sabi; son
  referencias gobernadas.
- Para multimodal v0, "funciona" significa captura local + metadatos seguros +
  witness + pruebas, no vision semantica productiva ni transcripcion cloud.
- Los proveedores cloud multimodales quedan disponibles solo como superficie de
  gate/documentacion hasta que exista adaptador revisado; no se llama red por
  defecto.
- Para cloud proposal v0.1, "NVIDIA integrado" significa contrato offline
  validable y convertible a TaskSpec/PatchPlan; no significa llamada live.
- La salida cloud debe ser propuesta estructurada; el gate final y apply siguen
  siendo responsabilidad local de Wabi/Sabi.
- Permitir specs bajo `runtime/outputs` como entrada es aceptable porque los
  targets de escritura siguen pasando por validacion de rutas sensibles.
- Para provider-gated v0.2, "conectar NVIDIA" significa construir el prompt,
  capturar una respuesta provider como artefacto redactado, extraer solo JSON y
  revalidarlo localmente. No significa auto-apply ni control remoto de PC.
- El runtime externo `C:\Users\L-Tyr\.medioevo\wabi\runtime` es un input root
  confiable para artefactos generados por Wabi/Sabi, no para targets de
  escritura.
- En esta corrida, `provider-status` confirma API keys por nombre de variable
  pero `WABI_ALLOW_CLOUD_PROVIDERS=0`; por tanto no hubo llamada live cloud.
- Para cloud provider v0.3, `CLOUD_DISABLED_BY_FLAG` es un cierre correcto si
  el flag no esta activo, incluso cuando existe credencial en entorno.
- `credential_present_redacted=true` significa presencia booleana de variable,
  no exposicion de valor.
- `cloud-debug-loop` puede crear rollback snapshot en dry-run sin modificar
  fuentes; apply real requiere `--apply`.
# Wabi Cloud Provider v0.4 - 2026-05-18

- La credencial NVIDIA existe solo como presencia redactada; su valor no fue leido ni impreso.
- El error `SMOKE_FAIL_REDACTED` apunta a provider/model/account routing, no a una prueba de capacidad del modelo.

# Wabi Cloud Provider v0.5 - 2026-05-18

- La referencia oficial NVIDIA puede existir aunque la cuenta/ruta local devuelva provider/model not-found.
- `endpoint_mode=openai_compatible` describe el adapter/request shape local, no verifica entitlement ni quota.
- `alias_candidates` son candidatos de revision local; ninguno queda validado live en v0.5.

# 2026-05-18 - BrowserBridge multibackend v0.1

- Kimi WebBridge se considera instalado/configurado solo si existe
  `WABI_KIMI_WEBBRIDGE_URL`; Wabi no lo instala ni asume protocolo si falta.
- `chrome-devtools-mcp` puede aparecer como configurado cuando existe `npx`,
  pero Wabi no ejecuta `npx` durante `status`.
- El catalogo de servicios es allowlist de preparacion, no prueba de cuenta,
  login, cuota ni funcionamiento live.
- `REVIEW_SKIPPED` es resultado correcto para live smoke Kimi si falta
  `WABI_ALLOW_BROWSER_BRIDGE=1`, `WABI_ALLOW_BROWSER_SEND=1`,
  `WABI_KIMI_WEBBRIDGE_URL` o `--send`.
- El fix de `gitleaks` es degradacion segura: timeout de version no significa
  scan aprobado, solo evita romper el endpoint de estado.
- La proxima llamada real debe ser unica y solo despues de confirmar alias/ruta en dashboard/API reference.

# Tree/workbench/code cleanup - 2026-05-18

- Los caches Python/pytest son regenerables y pueden moverse a quarantine sin cambiar comportamiento.
- Los duplicados de runtime outputs son evidencia historica hasta que exista una politica de compactacion.
- Los tres archivos legacy de inventario Claudio no forman parte del runtime activo, pero deben compilar para que global compileall sea significativo.
- Las rutas public staging quedan fuera de cleanup porque PublicationGate esta en `BLOCK`.
- El panel QA local puede abrirse como archivo estatico y no requiere servidor ni CDN.

# 2026-05-18 - Wabi Fallback-only Coding Acceptance v0.3

- Assumption: deterministic local stub is the right proposal source for this reproducible acceptance run.
- Assumption: sandbox-only apply is enough for v0.3; repo-internal fixture should wait for v0.4.

# 2026-05-18 - BrowserBridge Selector Pack v0.2

- Assumption: missing Kimi flags/URL should produce `KIMI_SEND_FLAGS_MISSING`
  or related not-run status, not a false pass and not a live call.
- Assumption: `npx` or Chrome MCP availability can drift; selector status must
  be measured at runtime and dry-run remains the deterministic fallback.
- Assumption: a local temporary server on 8788 is valid HTTP evidence for the
  new BRAIN_OS server code when 8787 already has a live older process that
  should not be stopped during this run.
- Assumption: synthetic public payloads are the only acceptable Kimi smoke
  content until the user explicitly opts in with flags and safe URL.
- Assumption: proposal validation success is not execution approval; TaskSpec,
  PatchPlan and apply remain separate local gates.

## 2026-05-19 - Build Assist Cloud Temporal

- La capa cloud es andamio de construccion para 60-90 dias; el producto final sigue local-first.
- NVIDIA `nano-30b` es el default pragmatico para bajar coste/latencia; `super` y `ultra` se reservan para revision.
- Un smoke live debe usar prompt sintetico/no privado y no aplicar cambios fuente.

## 2026-05-19 - NVIDIA nano-30b Live Smoke

- La presencia de `LIVE_SMOKE_PASS` indica conectividad funcional para una llamada sintetica minima, no capacidad ilimitada.
- El costo real y rate limit no se infieren porque el adapter devolvio `usage=null` y `cost_estimate=null`.
- La ruta apta para construccion debe seguir usando tareas bounded y logs redacted.
## 2026-05-19 - Wabi Conversational CLI v0.1

- Assumption: la ruta canonica de Wabi sigue siendo `apps/local/wabi-sabi`.
- Assumption: DUAT graphics local disponible se descubre desde `artifacts/duat-city/src/graphics` en el workspace padre.
- Assumption: en v0.1 el puente grafico debe preparar planes/specs, no mutar el renderer ni copiar assets.
- Assumption: `wabi --once` debe conservar compatibilidad de salida conversacional (`route=local_chat` para saludo) aunque ahora incluya `ConversationTurn`.
- Assumption: cloud live no se llama desde el REPL conversacional; las llamadas live siguen aisladas en comandos build-assist con doble bandera.

## 2026-05-19 - CloudBudgetGate v0.1

- Assumption: el presupuesto seguro inicial debe contar llamadas, no coste, porque tokens/coste pueden venir `null`.
- Assumption: `runtime_root/cloud_budget` es la ubicacion local correcta para estado no publico de presupuesto.
- Assumption: cada proceso CLI puede ser una sesion si `WABI_SESSION_ID` no esta fijado.
- Assumption: `build-assist-plan --dry-run` no debe incrementar llamadas completadas.
- Assumption: consultar `/status`, `/providers` o `build-assist-status` puede crear el JSON local de presupuesto con contadores en cero.

## 2026-05-19 - CloudBudgetGate UI v0.1

- Assumption: la UI activa de Wabi vive en `-= BRAIN_OS =-\apps\local\wabi_ui`, mientras la fuente canonica de CloudBudgetGate vive en `apps/local/wabi-sabi`.
- Assumption: es aceptable que el endpoint de status cree/normalice el JSON de presupuesto con contadores en cero, igual que CLI status.
- Assumption: esta fase no debe agregar acciones live desde UI; la UI solo prepara visibilidad de gate.

## 2026-05-19 - Wabi UI ConversationEngine v0.1

- Assumption: `POST /api/conversation/turn` debe usar la misma capa Python que el CLI, aunque la UI mantenga historico visual efimero en memoria del navegador.
- Assumption: no guardar prompts completos significa no persistir turnos ni artefactos desde el endpoint UI; la respuesta HTTP puede contener el plan generado para render inmediato.
- Assumption: `build-assist_request` desde UI debe quedar dry-run mientras `double_opt_in=false`.
- Assumption: la siguiente mejora debe ser revisar TaskSpec en UI, no activar apply ni cloud live.

## 2026-05-19 - Wabi UI Review TaskSpec v0.1

- Assumption: el TaskSpec revisable es suficiente para que el humano entienda scope/gate sin exponer prompt completo.
- Assumption: drafts redacted con `task_id` y fingerprint son evidencia suficiente para retomar sin guardar el texto completo del usuario.
- Assumption: un endpoint apply bloqueado es util para probar UX futura sin abrir ejecucion real.
- Assumption: temporales bajo `AppData` no deben ser tratados como parte del repo host aunque `C:\Users\L-Tyr` tenga `.git`.

## 2026-05-21 - HypothesisPacket / Counterexample Mode v0.1

- Assumption: la aplicacion correcta del caso unit distance es metodologica, no un claim publico de que Wabi resuelve matematicas abiertas.
- Assumption: el primer cierre util es core/CLI/ConversationEngine dentro de `apps/local/wabi-sabi` y contrato compartido en `packages/shared-contracts`.
- Assumption: la UI/API activa mencionada en handoffs vive fuera de este workspace primario y debe tocarse solo con gate separado.
- Assumption: una hipotesis nueva nace en `REVIEW` hasta que existan evidencias locales y falsadores ejecutados.
