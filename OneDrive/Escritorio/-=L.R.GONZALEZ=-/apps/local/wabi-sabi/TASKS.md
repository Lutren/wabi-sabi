# TASKS WABI-SABI

## 2026-05-21 - Observation Claim Adapter

- [x] Crear adapter Wabi proposal-only para `ObservationEnvelope` +
  `ClaimClassifier`.
- [x] Agregar CLI `claim-observation` / `claim-fixtures`.
- [x] Probar con fixtures sinteticos sin apply ni cloud.
- [x] Ejecutar fixture real de 12 claims y registrar calibracion inicial
  `REVIEW`.
- [x] Calibrar `ClaimClassifier` contra los 12 fixtures canonicos: rerun
  `claim-fixtures` -> `pass_count=12`, `review_count=0`, `status=PASS`.
- [x] Consumir `claimResult.gate_contract` desde obsai-core sin regresion del
  adapter; salida fixture mantiene `cloud_provider_called=false` y
  `applied_to_sources=false`.

## Cerrado localmente 2026-05-20 - Wabi LLM Safe JSON Contract

- [x] Crear `wabi_sabi/core/llm_work_response.py`.
- [x] Agregar contrato JSON top-level a `POST /api/conversation/turn`.
- [x] Agregar contrato JSON top-level a `POST /api/taskspec/llm-proposal`.
- [x] Mantener estado interno LLM en `llm_status`.
- [x] Incluir `graphics_plan` plan-only y `patch_candidate` redacted.
- [x] Incluir `tags` en el contrato seguro.
- [x] Crear `docs/WABI_LLM_RESPONSIBLE_USE_2026-05-20.md`.
- [x] Conectar `wabi --once "<tarea>" --json` al normalizador seguro.
- [x] Mantener compatibilidad de schema conversacional del CLI.
- [x] Agregar metadata operativa: prioridad, riesgo, categoria, relevancia e incrementalidad.
- [x] Registrar runtime JSON y WitnessLog.
- [x] Agregar tests Wabi y BRAIN_OS.
- [x] Ejecutar pruebas focales y `py_compile`.
- [x] Ejecutar regresion completa Wabi y BRAIN_OS.
- [x] Ejecutar smoke JSON no-live y secret scan focal.
- [x] Smoke manual UI opcional para visualizar el contrato en navegador. Cerrado 2026-05-21 con smoke HTTP local: `/` contiene `Cloud Budget`, `Wabi Conversation`, `Review TaskSpec`, `Gate Preview` y `Claudio Mission Control`; `/api/cloud-budget/status`, `/api/taskspec/gate-preview` y `/api/conversation/turn` respondieron sin cloud ni apply automatico.

## Cerrado localmente 2026-05-19 - Wabi LLM Cloud Work Mode

- [x] Crear `wabi_sabi/core/llm_proposal.py`.
- [x] Integrar LLM proposal default en `ConversationEngine`.
- [x] Agregar `POST /api/taskspec/llm-proposal`.
- [x] Agregar panel/boton `LLM Proposal` a la UI local.
- [x] Mantener Apply Local gateado y separado.
- [x] Agregar tests focales Wabi y BRAIN_OS.
- [x] Ejecutar regresiones completas Wabi y BRAIN_OS.
- [x] Ejecutar py_compile.
- [x] Capturar smoke UI local y endpoint JSON.
- [x] Ejecutar live proposal solo con doble opt-in explicito y presupuesto disponible. Cerrado como gate preservado 2026-05-21: no se ejecuto live call porque `double_opt_in=false`, `cloud_live_ready=false` y `CLOUD_BUDGET_DRY_RUN`.

## Cerrado localmente 2026-05-19 - Wabi Work Mode v1

- [x] Crear guia operativa `docs/WABI_WORK_MODE_2026-05-19.md`.
- [x] Crear bloqueo de release `docs/WABI_RELEASE_BLOCKERS_2026-05-19.md`.
- [x] Ejecutar QA minimo Wabi focal.
- [x] Ejecutar QA minimo BRAIN_OS UI focal.
- [x] Ejecutar `py_compile` de servidor UI y modulos Wabi principales.
- [x] Actualizar continuidad local y fingerprint.
- [x] Usar Wabi en una tarea local real pequena con Apply Local y reporte. Cerrado 2026-05-21: `apply-local-preview` -> `LOCAL_APPLY_PATCH_READY`; `apply-local` -> `LOCAL_APPLY_TESTS_PASS`; archivo generado `docs/WABI_LOCAL_APPLY_CLOSEOUT_2026-05-21.md`; witness verificado.
- [x] Mantener GitHub/medioevo.space/assets fuera del flujo diario hasta resolver blockers. Cerrado 2026-05-21: no hubo push, deploy, staging publico, asset publication ni live cloud.

## Cerrado localmente 2026-05-19 - WABI Assets Du WABI Local Integration + Release Gate

- [x] Leer estado Wabi Gate Preview y confirmar `Apply` bloqueado.
- [x] Auditar carpeta `Assets Du WABI` con inventario, hashes, dimensiones y flags.
- [x] Registrar ZIPs sin extraer ni copiar.
- [x] Generar runtime audit JSON y contact sheets.
- [x] Seleccionar cuatro PNGs metadata-clean para UI local.
- [x] Re-encodear y copiar assets a carpeta controlada de UI local.
- [x] Crear manifest con source redacted, hashes, dimensiones y `publication_allowed=false`.
- [x] Integrar assets en la UI local de Wabi con fallback.
- [x] Actualizar endpoint operational workbench con theme/manifest local.
- [x] Agregar tests de manifest/carpeta controlada.
- [x] Ejecutar focal BRAIN_OS, focal Wabi, regresiones completas y py_compile.
- [x] Ejecutar secret/boundary focal scans.
- [x] Capturar evidencia UI local con assets y Gate Preview.
- [x] Documentar bloqueo GitHub/medioevo.space.
- [x] Owner review: confirmar provenance/licencia/public-safe de los cuatro PNGs. Trasladado a `REVIEW_REQUIRED` 2026-05-21; no es ejecutable por agente sin owner review real.
- [x] Preparar staging limpio en repo publico correcto despues de approval. Trasladado a `REVIEW_REQUIRED` 2026-05-21; approval/public repo target no presente en este ciclo.
- [x] Ejecutar scan final sobre staged/public output antes de commit/push/deploy. Cerrado como no aplicable 2026-05-21: no hubo staged/public output, commit, push ni deploy.

## Cerrado 2026-05-19 - Wabi UI TaskSpec Gate Preview v0.1

- [x] Agregar `build_gate_preview` y helpers en `taskspec_review.py`.
- [x] Agregar endpoint `GET /api/taskspec/gate-preview`.
- [x] Mantener `POST /api/taskspec/apply` bloqueado con preview.
- [x] Agregar UI `Gate Preview` dentro de `Review TaskSpec`.
- [x] Confirmar `applied_to_sources=false`, `cloud_provider_called=false`, `graphics_live=false`.
- [x] Ejecutar tests focales Wabi y BRAIN_OS.
- [x] Ejecutar regresion completa Wabi y BRAIN_OS.
- [x] Capturar evidencia UI interactiva local.
- [x] Siguiente paso: contrato `Local Apply Readiness v0.1` sin apply real. Cerrado por evidencia 2026-05-21: `wabi_sabi/core/local_apply_readiness.py`, `tests/test_local_apply_readiness.py`, `apply-local-preview` y test focal `7 passed`.

## Cerrado 2026-05-19 - CloudBudgetGate UI Visual QA

- [x] Revisar diff/estado local y confirmar endpoint/panel existen.
- [x] Confirmar `CloudBudgetGate.render_status()` como fuente de verdad.
- [x] Detectar PID stale y puerto 8787 sin servidor activo.
- [x] Iniciar servidor UI local en `127.0.0.1:8787`.
- [x] Ejecutar smoke de `/api/cloud-budget/status` sin cloud live.
- [x] Guardar endpoint redacted y screenshots locales.
- [x] Confirmar visualmente panel Cloud Budget con campos esperados.
- [x] Ejecutar tests focales, regresion completa y `py_compile`.
- [x] Ejecutar smokes CLI no-live.
- [x] Siguiente paso: cablear UI chat/work panel a `ConversationEngine`, sin activar cloud live por defecto. Cerrado por verificacion 2026-05-21: `POST /api/conversation/turn` responde desde `ConversationEngine`, `cloud_provider_called=false`, `prompts_stored=false`.

## Cerrado 2026-05-18 - Wabi fallback-only coding acceptance v0.2

- [x] Crear sandbox runtime `coding_acceptance_v0_2`.
- [x] Crear `FALLBACK_ONLY_PROVIDER_STATE_v0_2.json`.
- [x] Ejecutar cloud-debug-loop dry-run y apply en `target_root=runtime`.
- [x] Registrar TaskSpec, PatchPlan, apply, tests, witness y hashes.
- [x] Agregar tests de acceptance fallback-only.
- [x] Integrar endpoint/panel UI via BRAIN_OS.
- [x] Proximo: fallback-only v0.3 con fixture local mas realista. Reconciliado 2026-05-21: el bloque `Wabi Fallback-only Coding Acceptance v0.3` ya esta cerrado en este mismo tracker.

## Cerrado 2026-05-18 - Tree/workbench/code cleanup

- [x] Crear baseline tree/inventory/hash/git status.
- [x] Clasificar caches, legacy, provider evidence, protected datasets y public staging.
- [x] Mover caches a quarantine con manifest y rollback.
- [x] Corregir compileall legacy en `02_CLAUDIO`.
- [x] Agregar `WORKBENCH_INDEX_20260518.md`.
- [x] Ejecutar Wabi, 02_CLAUDIO, GEODIA y DUAT predictive tests.
- [x] Ejecutar SecretScan focal.
- [x] Revisar reporte y decidir siguiente ruta: NVIDIA route review, fallback-only coding acceptance o Tree Health panel. Cerrado 2026-05-21: se eligio cierre local verificable por Apply Local + UI/API smoke; NVIDIA queda en review manual sin live call.

## Cerrado 2026-05-18 - Cloud provider v0.5

- [x] Crear diagnostico NVIDIA route/model sin llamada cloud.
- [x] Agregar alias candidates oficiales/locales.
- [x] Agregar CLI `wabi provider diagnose --provider nvidia --json`.
- [x] Crear guia redactada NVIDIA provider/model route review.
- [x] Integrar panel Provider / Proposal / PatchPlan / Rollback en UI principal.
- [x] Mantener chat con `SMOKE_FAIL_REDACTED`, fallback local y sin `SMOKE_PASS`.
- [x] Ejecutar pruebas Wabi, 02_CLAUDIO, HTTP chat y debug loop dry-run.
- [x] SecretScan final de artefactos v0.5.
- [x] Hash manifest v0.5.
- [x] Revision manual NVIDIA dashboard/API route antes de v0.6. Trasladado a `REVIEW_REQUIRED` 2026-05-21: requiere dashboard/API manual y no se ejecuto live provider.

## Cerrado 2026-05-18 - Cloud provider v0.4

- [x] Ejecutar un smoke NVIDIA efimero y clasificar resultado real.
- [x] Mantener `SMOKE_PASS` bloqueado cuando el smoke no pasa.
- [x] Sanear provider/account identifiers en runtime.
- [x] Crear panel local Provider / Proposal / PatchPlan / Rollback.
- [x] Validar debug loop dry-run/apply con TaskSpec sintetico en runtime.
- [x] Actualizar chat provider answer en 02_CLAUDIO.
- [x] Ejecutar SecretScan final de artefactos v0.4.
- [x] Crear guia redactada para revisar NVIDIA provider/model not-found. Reconciliado 2026-05-21: existe `docs/NVIDIA_PROVIDER_MODEL_ROUTE_REVIEW_20260518.md`.

## Cerrado 2026-05-18 - Cloud proposal provider-gated v0.2

- [x] Agregar prompt builder estricto para providers cloud.
- [x] Agregar extractor de JSON desde respuesta provider markdown/plain text.
- [x] Agregar fixture `--dry-run` para probar el flujo sin red.
- [x] Agregar comandos `cloud-proposal-from-provider`,
  `cloud-proposal-from-provider-task-spec` y
  `cloud-proposal-from-provider-plan`.
- [x] Corregir entrada desde runtime externo (`config.runtime_root`) para
  propuestas y TaskSpecs generados.
- [x] Actualizar README, ARCHITECTURE y USAGE.
- [x] Ejecutar smokes CLI provider/proposal/plan.
- [x] Ejecutar benchmark completo: `226 passed`.
- [x] Ejecutar `run-safe-tests`: `ok=true`, witness verificado.

## Cerrado 2026-05-18 - Cloud code proposal v0.1

- [x] Agregar `wabi_sabi/core/cloud_code_proposal.py`.
- [x] Agregar comandos `cloud-proposal-validate`, `cloud-proposal-task-spec`
  y `cloud-proposal-plan`.
- [x] Agregar `docs/wabi_cloud_code_proposal.example.json`.
- [x] Actualizar README, ARCHITECTURE y USAGE con el flujo proposal ->
  TaskSpec -> PatchPlan.
- [x] Agregar pruebas focales de validacion, redaccion, rutas bloqueadas,
  comandos allowlisted y CLI.
- [x] Ejecutar focal cloud proposal/task spec/CLI: `26 passed`.

## Cerrado 2026-05-17

- [x] Crear intake multimodal local para camara/microfono sin guardar media
  cruda.
- [x] Conectar intake a `world_model_adapter` y `mts_sensor_fusion_agent`.
- [x] Exponer CLI `wabi multimodal status|smoke-camera|smoke-mic|observe`.
- [x] Registrar `multimodal_intake` en `wabi tools`.
- [x] Probar smoke real de camara y microfono con artefactos + witness.
- [x] Mantener cloud multimodal en `REVIEW` con `cloud_provider_called=false`.
- [x] Ejecutar pruebas focales y suite completa.

## Cerrado 2026-05-16

- [x] Fijar `apps/local/wabi-sabi` como ruta canonica unica.
- [x] Absorber adapters/stubs a `apps/local/wabi-sabi/adapters`.
- [x] Absorber perfiles de modelos no secretos a `apps/local/wabi-sabi/config`.
- [x] Redirigir wrappers host hacia config/adapters canonicos.
- [x] Convertir `README_WABISABI.md` en redireccion.
- [x] Archivar root `adapters/` y root `config/` en `_archive/legacy` con
  `MIGRATION_LOG.md`.
- [x] Crear manifiesto de rutas externas Wabi-Sabi.
- [x] Validar sintaxis Python de adapters.
- [x] Validar JSON de fingerprints.

## Pendiente Real

- [x] Calibrar gate interpretativo BRAIN_OS para intake real: hoy la captura
  fisica pasa, pero `Phi_eff_world < 0.60` bloquea integracion cuando la camara
  entrega frames oscuros. Cerrado 2026-05-21: `multimodal_intake` ahora emite `quality=<...>` e `interpretation_status=REVIEW_LOW_LIGHT_CAPTURE_OK`; test `test_low_light_camera_frame_is_capture_ok_but_integration_review` pasa.
- [x] Revisar `scripts/load_secrets.ps1`, `secret_store.ps1` y helpers de
  credenciales como `REVIEW_SECRET_HOOK`; no copiar al canon sin captura
  segura de secretos. Cerrado como gate 2026-05-21: no existen esos scripts bajo la ruta canonica Wabi y la frontera ya esta documentada como `REVIEW_SECRET_HOOK`; no se leyeron ni copiaron secretos.
- [x] v0.3: live smoke opcional de NVIDIA NIM solo si
  `WABI_ALLOW_CLOUD_PROVIDERS=1` y el operador habilita el gate.
  Cerrado como gate preservado 2026-05-21: flags/doble opt-in no habilitados en el servidor activo; sin live call.
- [x] v0.3: crear debug loop con max retries, rollback y stderr saneado.
- [x] v0.3: crear contrato provider status con booleans redactados.
- [x] v0.3: crear `provider live-smoke` con skip seguro si flag/cloud/config falta.
- [x] v0.3: actualizar chat/model-status en `02_CLAUDIO`.
- [x] Ejecutar smoke live real de NVIDIA solo cuando `WABI_ALLOW_CLOUD_PROVIDERS=1`
  este activo en una terminal controlada.
  Cerrado como gate preservado 2026-05-21: `cloud_live_ready=false`, `double_opt_in=false`; sin live call.
- [x] Panel DUAT/Wabi read-only para provider/gate/proposal/patch/test/witness. Cerrado 2026-05-21: UI y `/api/operational-workbench`/Mission Control verificados read-only; no botones de apply/cloud live ejecutados.

# 2026-05-18 - Wabi Fallback-only Coding Acceptance v0.3

- [x] Create multifile fixture with intentional local bug.
- [x] Confirm expected initial test failure.
- [x] Generate TaskSpec/PatchPlan and dry-run before apply.
- [x] Apply fix inside runtime sandbox only.
- [x] Verify final tests, rollback and witness.
- [x] Update API/UI and continuity artifacts.
- [x] Next: UI polish, fallback-only v0.4, or NVIDIA manual route review. Cerrado como decision 2026-05-21: se priorizo cierre local de Apply Local + UI/API smoke; NVIDIA manual route review queda fuera de ejecucion automatica.

## Cerrado 2026-05-18 - BrowserBridge multibackend + concilio opt-in

- [x] Extender BrowserBridge con backends `dry-run`, `chrome-devtools-mcp`,
  `kimi-webbridge` y `hermes`.
- [x] Mantener `dry-run` como fallback determinista sin navegador ni red.
- [x] Exponer `chrome-devtools-mcp` como backend primario detectado, sin
  instalar ni ejecutar dependencias automaticamente.
- [x] Detectar Kimi WebBridge por `WABI_KIMI_WEBBRIDGE_URL`.
- [x] Detectar Hermes por CLI y mantenerlo sin `--yolo`.
- [x] Agregar doble opt-in de envio: `--send` mas
  `WABI_ALLOW_BROWSER_SEND=1`.
- [x] Ampliar catalogo: Kimi, ChatGPT, Claude, Gemini, Gemini Pro, Gemini
  Thinking, Perplexity, DeepSearch, Grok, Copilot, Copilot Smart, Qwen Max,
  Qwen Agents, DeepSeek 4 Pro, DeepSeek 4 Vision y DeepSeek4.
- [x] Agregar `browser-bridge council <prompt>` prepare-only.
- [x] Convertir respuestas live estructuradas a
  `wabi.cloud_code_proposal.v0_1` y validarlas localmente sin auto-apply.
- [x] Corregir colision de artefactos de concilio con prefijos por servicio.
- [x] Endurecer `02_CLAUDIO` para que timeout de `gitleaks version` sea
  `VERSION_TIMEOUT`, no fallo del endpoint.
- [x] Validar Wabi full, safe-tests con witness, world model, MTS y
  `02_CLAUDIO` full.

## Cerrado 2026-05-18 - BrowserBridge Selector Pack v0.2

- [x] Crear `browser_bridge_selector_pack.py` con `ServiceCapability`,
  payload classes y decision output.
- [x] Mantener `dry-run` siempre disponible y default.
- [x] Clasificar `chrome-devtools-mcp` como read-only/snapshot bajo gate local.
- [x] Clasificar Kimi como `SEND_REVIEW` con doble opt-in y URL local segura.
- [x] Mantener Hermes y servicios sin adapter probado en review/prepare-only.
- [x] Agregar CLI `select`, `smoke`, `snapshot`, `council` y
  `proposal-from-response`.
- [x] Crear Kimi smoke sintetico que no llama red si falta cualquier flag.
- [x] Crear snapshot DevTools MCP read-only con fallback `NOT_AVAILABLE`.
- [x] Agregar ranking de council sin envio externo.
- [x] Endurecer respuesta con codigo hacia propuesta validable y no auto-apply.
- [x] Integrar BrowserBridge en Wabi UI y `/api/operational-workbench`.
- [x] Ejecutar Wabi full, safe-tests, 02_CLAUDIO full, GEODIA, DUAT, world
  model, MTS, HTTP y SecretScan.
- [x] Reiniciar/verificar servidor Wabi existente en 8787 solo en accion controlada
  para cargar el nuevo panel/ruta. Cerrado 2026-05-21 por smoke HTTP sobre
  `http://127.0.0.1:8787/`: UI responde 200 y expone Wabi Conversation,
  Cloud Budget, Review TaskSpec y Gate Preview; sin provider cloud live.

## 2026-05-19 - Build Assist Cloud Temporal

- [x] Crear estado `build-assist-status`.
- [x] Crear planificador `build-assist-plan` con dry-run forzado si faltan gates.
- [x] Agregar presupuesto local de llamadas cloud.
- [x] Documentar contrato temporal cloud-assisted local-first.
- [x] Ejecutar pruebas focales y regresion completa.
- [x] Ejecutar live smoke NVIDIA `nano-30b` con prompt sintetico cuando el operador habilite banderas de sesion. Cerrado como gate preservado 2026-05-21: banderas de sesion no habilitadas; sin live call.

## 2026-05-19 - NVIDIA nano-30b Live Smoke

- [x] Agregar comando `build-assist-smoke`.
- [x] Bloquear smoke live si falta `--live`.
- [x] Bloquear smoke live si faltan `WABI_BUILD_ASSIST_CLOUD=1` o `WABI_ALLOW_CLOUD_PROVIDERS=1`.
- [x] Probar provider mock success/error con redaction.
- [x] Ejecutar un smoke NVIDIA `nano-30b` live con prompt sintetico.
- [x] Registrar artefacto smoke y redaction scan.
- [x] Usar `build-assist-plan` en una tarea Wabi pequena con validacion local antes de apply. Cerrado 2026-05-21: `build-assist-plan "validar una tarea local pequena sin cloud" --codex-provider nano-30b --json` genero plan dry-run, `cloud_provider_called=false`, `dry_run_forced_by_gate=true`.
## 2026-05-19 - Wabi Conversational CLI v0.1

- [x] Crear `wabi_sabi/core/conversation_engine.py`.
- [x] Crear `wabi_sabi/core/graphics_bridge.py`.
- [x] Hacer que `wabi` sin argumentos abra REPL conversacional `wabi>`.
- [x] Mantener `wabi --once "hola wabi"` funcionando.
- [x] Agregar tests de CLI conversacional, engine e integration graphics bridge.
- [x] Verificar build-assist status proposal-only y comandos manuales.
- [x] Ejecutar regresion Wabi completa.
- [x] Siguiente paso: cablear UI local al `ConversationEngine` o exponer endpoint interno estable para reutilizar `ConversationTurn`. Cerrado 2026-05-21 con `POST /api/conversation/turn`.
- [x] Siguiente paso: agregar contador/presupuesto por sesion para llamadas build-assist cloud desde UI/CLI. Cerrado 2026-05-21: `CloudBudgetGate` expone session/day limits y endpoint `/api/cloud-budget/status`; tests `test_cloud_budget*` incluidos en focal `42 passed`.

## 2026-05-19 - CloudBudgetGate v0.1

- [x] Revisar diff/estado local antes de modificar.
- [x] Crear `wabi_sabi/core/cloud_budget.py`.
- [x] Integrar `cloud_budget` en `build-assist-status`.
- [x] Integrar presupuesto antes de cualquier llamada real en `build-assist-plan`.
- [x] Integrar presupuesto antes de live smoke en `run_build_assist_nvidia_smoke`.
- [x] Mostrar `cloud_budget` en `/status`.
- [x] Mostrar `cloud_budget` en `/providers`.
- [x] Integrar `ConversationEngine` para `build_assist_request`.
- [x] Crear tests `tests/test_cloud_budget.py`.
- [x] Ejecutar focal, `py_compile`, regresion y smokes manuales sin live cloud.
- [x] Mostrar CloudBudgetGate en la UI local de Wabi.
- [x] Agregar endpoint local `GET /api/cloud-budget/status`.
- [x] Agregar tests `tests/test_cloud_budget_ui_status.py`.
- [x] Ejecutar regresion completa, py_compile y smokes manuales no-live finales para CloudBudgetGate UI.
- [x] Siguiente paso: reiniciar servidor UI local y verificar visualmente el panel `Cloud Budget` sin llamada cloud. Cerrado 2026-05-21: servidor existente `127.0.0.1:8787` activo, panel presente en HTML y endpoint `CLOUD_BUDGET_DRY_RUN`, `cloud_provider_called=false`.

## 2026-05-19 - Wabi UI ConversationEngine v0.1

- [x] Reconstruir handoff limpio del QA visual Cloud Budget.
- [x] Crear endpoint local `POST /api/conversation/turn`.
- [x] Hacer que el endpoint use `ConversationEngine.handle_turn`.
- [x] Desactivar persistencia de prompts y artefactos para turnos UI.
- [x] Agregar panel `Wabi Conversation` en la UI local.
- [x] Mostrar intent, gate, proposal_only, cloud_provider_called, applied_to_sources, CloudBudget y graphics_live.
- [x] Probar `hola wabi`, request grafico y request NVIDIA sin doble opt-in.
- [x] Reiniciar servidor UI local en `127.0.0.1:8787` y capturar screenshot.
- [x] Ejecutar tests focales, regresion completa y py_compile.
- [x] Siguiente paso: crear flujo UI `Review TaskSpec` sin apply automatico. Cerrado 2026-05-21: panel y endpoints `/api/taskspec/latest`, `/api/taskspec/save-draft`, `/api/taskspec/apply` y `/api/taskspec/gate-preview` verificados; apply sigue bloqueado.

## 2026-05-19 - Wabi UI Review TaskSpec v0.1

- [x] Crear `wabi_sabi/core/taskspec_review.py`.
- [x] Normalizar TaskSpec para review sin prompt completo.
- [x] Agregar endpoints `GET /api/taskspec/latest`, `POST /api/taskspec/save-draft`, `POST /api/taskspec/apply`.
- [x] Hacer que apply responda `APPLY_BLOCKED_REVIEW_ONLY_V0_1`.
- [x] Agregar panel UI `Review TaskSpec`.
- [x] Agregar botones `Review`, `Copy TaskSpec`, `Save Draft`, `Apply bloqueado`, `Run Tests plan-only`.
- [x] Probar code, graphics y build-assist dry-run desde API local.
- [x] Guardar draft redacted y verificar que no contiene prompts completos ni secreto.
- [x] Corregir timeout de worktree para temporales bajo `AppData`.
- [x] Ejecutar focales, regresiones completas y `py_compile`.
- [x] Siguiente paso: `TaskSpec Gate Preview` para explicar requisitos de apply local futuro sin ejecutar. Cerrado 2026-05-21: `/api/taskspec/gate-preview` devuelve `apply_status=BLOCKED`, `required_gates`, `required_tests`, `rollback_required=true`.

## 2026-05-21 - HypothesisPacket / Counterexample Mode v0.1

- [x] Crear contrato `HypothesisPacket` en `packages/shared-contracts`.
- [x] Crear motor local `wabi_sabi/core/hypothesis_packet.py`.
- [x] Agregar comando `wabi hypothesis ... --json`.
- [x] Integrar `hypothesis_request` en `ConversationEngine` y `--once`.
- [x] Marcar respuestas seguras con tags `hypothesis_packet` y `counterexample_search`.
- [x] Agregar tests focales de contrato, Wabi core, CLI y safe response.
- [x] Ejecutar regresion Wabi completa.
- [x] Siguiente paso: si se autoriza tocar BRAIN_OS UI activa, exponer el modo en `POST /api/conversation/turn`/panel visual sin persistir prompts. Cerrado 2026-05-21: `POST /api/conversation/turn` con hipotesis devuelve `intent_name=hypothesis_request`, tags `hypothesis_packet`/`counterexample_search`, `prompts_stored=false`, `cloud_provider_called=false`.
