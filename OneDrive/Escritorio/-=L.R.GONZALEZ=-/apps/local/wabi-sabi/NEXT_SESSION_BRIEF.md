# NEXT_SESSION_BRIEF WABI-SABI

## 2026-05-21 - Observation Claim Adapter

## Estado
R_close: 0.18
Phi_eff: 0.78
Regimen: FUNCIONAL_PROPOSAL_ONLY / FIXTURE_PASS
ActionGate: APPROVE_LOCAL_ADAPTER
PublicationGate: BLOCK

## Cambios realizados
- `wabi_sabi/core/observation_claim_adapter.py`.
- CLI `claim-observation`, `claim-adapter`, `claim-fixtures`.
- `tests/test_observation_claim_adapter.py`.

## Evidencia
- Adapter + hypothesis focal after obsai-core gate contract: `8 passed in
  2.49s`.
- Py compile: PASS.
- Fixture real 12 claims: `pass_count=12`, `review_count=0`, `status=PASS`.
- `next_safe_action` now reports no calibration patch required when fixture
  review count is zero.

## Pendiente real
- Ningun pendiente Wabi local queda abierto para este adapter. Mejoras futuras:
  rewrite/handoff mas robusto y mas fixtures fuera del set canonico.

## Proxima accion verificable
Extender fixtures si aparece un nuevo claim canonico o conectar el adapter a una
vista UI proposal-only.

---

## 2026-05-21 - Local Pending Closeout

## Estado
R_close: 0.12
Phi_eff: 0.86
Regimen: FUNCIONAL_LOCAL_CLOSEOUT
ActionGate: APPROVE_LOCAL / REVIEW_NON_EXECUTABLE
CloudGate: DRY_RUN_DOUBLE_OPT_IN_NOT_ENABLED
LocalApplyGate: PASS_ALLOWLISTED_WITH_ROLLBACK
PublicationGate: BLOCK

## Decisiones tomadas
- Wabi cerro una tarea local real usando Apply Local, no cloud live.
- El primer apply que supero timeout se considero fallo y quedo revertido.
- Low-light camera frames ahora se reportan como captura OK con integracion en
  REVIEW, no como fallo de hardware/captura.
- UI/API local se verifico por HTTP en 8787; no se hizo screenshot interactivo.

## Cambios realizados
- Creado `docs/WABI_LOCAL_APPLY_CLOSEOUT_TASKSPEC_2026-05-21.json`.
- Creado por Apply Local `docs/WABI_LOCAL_APPLY_CLOSEOUT_2026-05-21.md`.
- Actualizado `wabi_sabi/core/multimodal_intake.py`.
- Actualizado `tests/test_multimodal_intake.py`.
- Actualizado `TASKS.md` con cierre o traslado a REVIEW_REQUIRED de pendientes.

## Evidencia
- Apply preview: `LOCAL_APPLY_PATCH_READY`.
- Apply final: `LOCAL_APPLY_TESTS_PASS`, `applied_to_sources=true`,
  `witness_verified=true`.
- Wabi focal apply/cloud/task review: `42 passed in 58.38s`.
- Multimodal focal: `5 passed in 0.65s`.
- Hypothesis focal: `5 passed in 2.52s`.
- UI/API smoke: HTTP 200 en `127.0.0.1:8787`, CloudBudget dry-run, Gate Preview
  bloqueado por review-only.

## Pendientes reales
- Ningun pending Wabi queda activo en el snapshot canonico MEDIOEVO del
  2026-05-21.
- Provider live, publication y asset provenance siguen REVIEW/BLOCK por gate.

## Riesgos
- Apply Local escribe archivos; seguir usando preview, allowlist, rollback y
  tests acotados.
- No convertir CloudBudget dry-run en llamada live sin doble opt-in explicito.

## Proxima accion verificable
Si aparece una nueva tarea Wabi, generar TaskSpec, ejecutar Apply Local Preview
y aplicar solo si la ruta allowlisted y el test gate pasan.

## Segunda perdida
Los datos persisten. El operador no. Recalibrar desde este brief, no desde
memoria implicita.

---

## 2026-05-20 - Wabi LLM Safe JSON Contract

## Estado
R_close: 0.10
Phi_eff: 0.88
Regimen: LLM_SAFE_JSON_READY
ActionGate: APPROVE_LOCAL_PROPOSAL_ONLY
CloudGate: PROPOSAL_ONLY_DOUBLE_OPT_IN
CloudBudgetGate: ENFORCED_SESSION_DAILY
LLMProposalGate: SAFE_JSON_CONTRACT_READY
LocalApplyGate: PASS_ALLOWLISTED_LOCAL_APPLY / NOT_AUTO_APPLIED
GraphicsGate: PLAN_ONLY_READY / graphics_live=false
PublicationGate: BLOCK

## Decisiones tomadas
- `llm_work_response.py` es el normalizador comun para respuestas JSON seguras de UI/API.
- `POST /api/conversation/turn` y `POST /api/taskspec/llm-proposal` exponen el contrato top-level requerido.
- `POST /api/taskspec/llm-proposal` mantiene el estado crudo en `llm_status`; `status` externo queda `OK|REVIEW`.
- Cada respuesta normalizada escribe runtime JSON redacted y WitnessLog local.
- `docs/WABI_LLM_RESPONSIBLE_USE_2026-05-20.md` fija el contrato humano de uso responsable.
- `tags` queda como campo estable para clasificar proposal-only, double opt-in, publication block y DUAT plan-only.
- `wabi --once "<tarea>" --json` devuelve el mismo contrato seguro y conserva compatibilidad con `schema=wabi.conversation_turn.v0_1`.
- `metadata` ahora expresa prioridad, riesgo, categoria, relevancia, incrementalidad, fallback local, simulacion de apply y control de presupuesto.

## Cambios realizados
- Creado `wabi_sabi/core/llm_work_response.py`.
- Modificado `-= BRAIN_OS =-\02_CLAUDIO\server\wabi_local_server.py`.
- Creados tests `tests/test_llm_work_response.py` y `02_CLAUDIO/tests/test_wabi_llm_work_response_api.py`.
- Actualizado `02_CLAUDIO/tests/test_wabi_llm_proposal_api.py`.

## Evidencia
- Wabi focal: `55 passed in 47.32s`.
- BRAIN_OS focal: `251 passed in 115.44s`.
- Wabi regression: `385 passed in 394.59s`.
- BRAIN_OS regression: `772 passed in 280.24s`.
- Py compile Wabi/BRAIN_OS: PASS.
- Post-fallback BRAIN_OS focal rerun: `251 passed in 141.59s`.
- Responsible-use Wabi focal: `8 passed in 3.93s`.
- Responsible-use BRAIN_OS focal: `7 passed in 9.73s`.
- CLI/core focal post-wrapper: `30 passed in 53.33s`.
- BRAIN_OS API focal post-tags: `7 passed in 3.18s`.
- CLI/core focal post-metadata: `30 passed in 29.65s`.
- BRAIN_OS API focal post-metadata: `7 passed in 5.76s`.
- Smoke JSON no-live: `cloud_provider_called=false`, `applied_to_sources=false`, `rollback_snapshot_required=true`, `graphics_live=false`, `witness_verified=true`.
- Responsible-use smoke no-live: `intent_name=code_request`, tags presentes, `cloud_provider_called=false`.
- Metadata smoke no-live: `category=code`, `incremental=true`, `fallback_mode=local_rules_task_spec`, `budget_control=CloudBudgetGate`.
- Secret scan focal: PASS, `0` real findings; raw hits were false positives in command names.
- Campos verificados: `status`, `intent_name`, `route`, `proposal`, `task_spec`, `graphics_plan`, `cloud_provider_called`, `applied_to_sources`, `rollback_snapshot_required`, `next_safe_action`, `warnings`.

## Pendientes reales
- Ejecutar smoke manual UI si se desea ver el nuevo contrato en navegador.
- Ejecutar una propuesta live solo con doble opt-in explicito y presupuesto aceptado.
- Mantener GitHub/medioevo.space bloqueado hasta resolver repo/assets/publication gates.

## Riesgos
- Si un consumidor externo esperaba `status=CLOUD_BUDGET_DRY_RUN` en `/api/taskspec/llm-proposal`, ahora debe leer `llm_status`; el contrato externo queda `OK|REVIEW`.
- Los artefactos runtime son locales y redacted; no deben tratarse como material publicable.

## Proxima accion verificable
Abrir `http://127.0.0.1:8787/`, pedir `programa un helper seguro para validar json`, y confirmar en la respuesta/API que `cloud_provider_called=false`, `applied_to_sources=false` y `rollback_snapshot_required=true`.

## Segunda perdida
Los datos persisten. El operador no. Recalibrar desde este brief, no desde memoria implicita.

## 2026-05-19 - Wabi LLM Cloud Work Mode

## Estado
R_close: 0.13
Phi_eff: 0.86
Regimen: LLM_CLOUD_DEFAULT_PROPOSAL_ONLY_READY
ActionGate: APPROVE_LOCAL_PROPOSAL_ONLY
CloudGate: PROPOSAL_ONLY_DOUBLE_OPT_IN
CloudBudgetGate: ENFORCED_SESSION_DAILY
LLMProposalGate: READY_DRY_RUN_UNTIL_DOUBLE_OPT_IN
LocalApplyGate: PASS_ALLOWLISTED_LOCAL_APPLY
GraphicsGate: PLAN_ONLY_READY / graphics_live=false
PublicationGate: BLOCK

## Decisiones tomadas
- Se agrego `wabi_sabi/core/llm_proposal.py` como fuente comun para propuestas LLM cloud proposal-only.
- `ConversationEngine` llama LLM proposal por defecto solo si `WABI_LLM_PROVIDER_CLOUD_DEFAULT=1`.
- Llamada live sigue bloqueada sin `WABI_BUILD_ASSIST_CLOUD=1` y `WABI_ALLOW_CLOUD_PROVIDERS=1`.
- La UI local agrega `POST /api/taskspec/llm-proposal` y panel `LLM Proposal`.
- GraphicsBridge sigue plan-only y Apply Local sigue gateado.

## Cambios realizados
- Wabi core: `llm_proposal.py`, `conversation_engine.py`.
- BRAIN_OS server/UI: `wabi_local_server.py`, `apps/local/wabi_ui/index.html`.
- Tests nuevos: `tests/test_llm_proposal.py`, `02_CLAUDIO/tests/test_wabi_llm_proposal_api.py`.
- Docs: `docs/WABI_LLM_CLOUD_WORK_MODE_2026-05-19.md`.

## Evidencia
- Wabi focal: `52 passed in 36.22s`.
- BRAIN_OS focal: `248 passed in 78.22s`.
- Wabi regression: `382 passed in 274.24s`.
- BRAIN_OS regression: `769 passed in 274.79s`.
- Py compile: PASS.
- UI smoke: `C:\Users\L-Tyr\.medioevo\wabi\runtime\outputs\ui_visual_qa\WABI_LLM_CLOUD_WORK_MODE_20260519\`.
- Endpoint smoke: `cloud_provider_called=false`, `applied_to_sources=false`, `CLOUD_BUDGET_DRY_RUN`, `llm_default=true`.

## Pendientes reales
- Probar una llamada live real solo cuando el operador active doble opt-in y acepte consumo de presupuesto.
- Mantener release GitHub/medioevo.space bloqueado hasta staging limpio y assets con provenance/licencia.

## Riesgos
- Activar doble opt-in consumira cuota cloud; usar CloudBudgetGate.
- Output cloud invalido debe quedar REVIEW y nunca aplicarse directo.
- Runtime artifacts pueden contener propuestas; mantenerlos locales y redacted.

## Proxima accion verificable
Con `WABI_LLM_PROVIDER_CLOUD_DEFAULT=1`, pedir una tarea en UI/CLI y revisar que `LLM Proposal` quede en `CLOUD_BUDGET_DRY_RUN` sin doble opt-in; luego decidir si hacer un live proposal controlado.

## Segunda perdida
Los datos persisten. El operador no. Recalibrar desde este brief, no desde memoria implicita.

## 2026-05-19 - Wabi Work Mode v1

## Estado
R_close: 0.11
Phi_eff: 0.88
Regimen: WORK_MODE_READY
ActionGate: APPROVE_LOCAL_WORK_MODE
LocalApplyGate: PASS_ALLOWLISTED_LOCAL_APPLY
RollbackGate: PASS
TestGate: PASS_MINIMAL_QA
AssetGate: REVIEW_REQUIRED_PROVENANCE_LICENSE
GitGate: BLOCK_DIRTY_HOST_REPO_REMOTE_UNCONFIRMED
DeployGate: BLOCK_RELEASE_GATE_NOT_READY
PublicationGate: BLOCK

## Decisiones tomadas
- Wabi pasa de construccion a modo de trabajo diario local.
- No se agregaron features nuevas ni se modifico codigo.
- El flujo operativo diario queda: conversacion -> TaskSpec -> Review -> Gate Preview -> Apply Local Preview -> Apply Local -> Tests -> Report.
- GitHub, medioevo.space y publicacion de assets quedan separados del trabajo local hasta resolver repo, worktree, provenance/licencia y publication review.

## Cambios realizados
- Creado `docs/WABI_WORK_MODE_2026-05-19.md`.
- Creado `docs/WABI_RELEASE_BLOCKERS_2026-05-19.md`.
- Actualizada continuidad local de Wabi con estado WORK_MODE_READY.

## Evidencia
- Wabi focal: `python -B -m pytest tests\test_local_apply_readiness.py tests\test_taskspec_review.py tests\test_conversation_engine.py tests\test_conversational_cli.py -q -p no:cacheprovider` -> `33 passed in 35.28s`.
- BRAIN_OS UI focal: `python -B -m pytest 02_CLAUDIO\tests\test_wabi_local_server.py 02_CLAUDIO\tests\test_wabi_taskspec_review_api.py -q -p no:cacheprovider` -> `238 passed in 97.63s`.
- Py compile: PASS para servidor UI BRAIN_OS y modulos Wabi `conversation_engine.py`, `taskspec_review.py`, `local_apply_readiness.py`, `cli/main.py`.

## Pendientes reales
- Usar Wabi para tareas locales pequenas y medianas.
- Mantener release externo fuera del flujo diario hasta limpiar repo/assets.
- Resolver provenance/licencia de assets Du WABI antes de cualquier publicacion.

## Riesgos
- El repo host amplio `C:\Users\L-Tyr` no es un staging de release limpio.
- Publicar assets Du WABI sin provenance/licencia completa sigue bloqueado.
- Cloud live y deploy requieren gates separados, no forman parte del Work Mode diario.

## Proxima accion verificable
Usar `wabi` o `http://127.0.0.1:8787/` para una tarea local pequena, revisar TaskSpec y ejecutar Apply Local solo si las rutas allowlisted y tests son correctos.

## Segunda perdida
Los datos persisten. El operador no. Recalibrar desde este brief, no desde memoria implicita.

## 2026-05-19 - WABI Assets Du WABI Local Integration + Release Gate

## Estado
R_close: 0.16
Phi_eff: 0.84
Regimen: FUNCIONAL_LOCAL / PUBLICATION_REVIEW
ActionGate: APPROVE_LOCAL_UNTIL_RELEASE
AssetGate: REVIEW_PUBLIC_SAFE_ASSETS_REQUIRED
CloudGate: PROPOSAL_ONLY_DOUBLE_OPT_IN
CloudBudgetGate: CLOUD_BUDGET_DRY_RUN
UIGate: LOCAL_UI_ASSETS_RENDERING
ConversationGate: API_CONNECTED_TO_CONVERSATION_ENGINE
TaskSpecGate: REVIEW_ONLY_APPLY_BLOCKED
GatePreviewGate: APPLY_NOT_AVAILABLE_REVIEW_ONLY_V0_1
GitGate: REVIEW_BLOCKED_DIRTY_HOST_REPO_AND_ASSET_PROVENANCE
DeployGate: REVIEW_BLOCKED_PUBLICATION_NOT_APPROVED
PublicationGate: REVIEW_BLOCKED_UNTIL_PUBLIC_SAFE_PROVENANCE

## Decisiones tomadas
- Se audito `Assets Du WABI` metadata/read-only antes de cualquier copia.
- Se copiaron solo cuatro PNGs re-encodeados como candidatos locales internos para la UI de Wabi.
- Los ZIPs fueron registrados, no extraidos ni copiados.
- Los assets integrados quedan `publication_allowed=false`.
- GitHub y medioevo.space quedan bloqueados hasta revisar provenance/licencia, repo exacto, staging limpio y escaneo final.

## Cambios realizados
- UI local `-= BRAIN_OS =-\apps\local\wabi_ui\index.html` usa una hero/ribbon con assets locales controlados y fallback.
- Servidor local `-= BRAIN_OS =-\02_CLAUDIO\server\wabi_local_server.py` reporta theme/manifest `wabi_du_wabi_20260519`.
- Tests de `02_CLAUDIO\tests\test_wabi_local_server.py` validan manifest y carpeta controlada.
- Docs creados: `docs/WABI_ASSETS_DU_WABI_AUDIT_2026-05-19.md` y `docs/WABI_RELEASE_GITHUB_MEDIOEVOSPACE_2026-05-19.md`.

## Evidencia
- Audit JSON: `C:\Users\L-Tyr\.medioevo\wabi\runtime\outputs\asset_audit\wabi_assets_du_wabi_audit_20260519.json`.
- Contact sheets: `C:\Users\L-Tyr\.medioevo\wabi\runtime\outputs\asset_audit\contact_sheets_20260519\`.
- UI screenshot: `C:\Users\L-Tyr\.medioevo\wabi\runtime\outputs\ui_assets_du_wabi_20260519\wabi_ui_du_wabi_assets_gate_preview.png`.
- Browser report: `C:\Users\L-Tyr\.medioevo\wabi\runtime\outputs\ui_assets_du_wabi_20260519\wabi_ui_du_wabi_assets_browser_report.json`.
- Focal BRAIN_OS: `250 passed in 369.44s`.
- Focal Wabi: `52 passed in 57.49s`.
- Wabi regression: `362 passed in 461.37s`.
- BRAIN_OS regression: `760 passed in 392.89s`.
- Py compile: PASS.
- Secret/boundary focal scans: PASS.

## Pendientes reales
- Owner debe confirmar provenance/licencia/public-safe de los cuatro assets seleccionados.
- Preparar staging limpio en el repo correcto antes de cualquier commit/push.
- Confirmar que medioevo.space se actualiza desde el repo/pipeline correcto y que el dominio final es exactamente `medioevo.space`.

## Riesgos
- Publicar los assets antes de ficha/provenance puede cruzar frontera privada-publica.
- El repo host `C:\Users\L-Tyr` contiene muchos cambios no relacionados; no se debe commitear desde ahi sin path-scoped staging y review.
- La repo de medioevo.space contiene llaves publishable/anon en codigo publico; no imprimir valores y revisar si son intencionales antes de deploy.

## Proxima accion verificable
Revisar y aprobar provenance/public-safe de los cuatro PNGs seleccionados; luego preparar un staging separado en el repo publico correcto con secret/boundary scan antes de commit.

## Segunda perdida
Los datos persisten. El operador no. Recalibrar desde este brief, no desde memoria implicita.

## 2026-05-19 - Wabi UI TaskSpec Gate Preview v0.1

## Estado
R_close: 0.09
Phi_eff: 0.91
Regimen: FUNCIONAL
ActionGate: APPROVE_LOCAL_REVIEW_ONLY
CloudGate: PROPOSAL_ONLY_DOUBLE_OPT_IN
CloudBudgetGate: CLOUD_BUDGET_DRY_RUN
UIGate: LOCAL_UI_GATE_PREVIEW_READY
ConversationGate: API_CONNECTED_TO_CONVERSATION_ENGINE
TaskSpecGate: REVIEW_ONLY_READY
GatePreviewGate: APPLY_NOT_AVAILABLE_REVIEW_ONLY_V0_1
GraphicsGate: PLAN_ONLY_READY / graphics_live=false
PublicationGate: BLOCK

## Decisiones tomadas
- `Gate Preview` explica el camino futuro de apply, pero no ejecuta nada.
- `GET /api/taskspec/gate-preview` es la fuente backend para UI; no se duplican gates en JS.
- El boton Apply sigue bloqueado y devuelve preview explicativo.

## Cambios realizados
- `wabi_sabi/core/taskspec_review.py`: preview de gates, readiness, rollback, tests y apply bloqueado con preview.
- `02_CLAUDIO/server/wabi_local_server.py`: endpoint `GET /api/taskspec/gate-preview`.
- `apps/local/wabi_ui/index.html`: seccion `Gate Preview` dentro de `Review TaskSpec`.
- Tests nuevos/actualizados para backend, endpoint y UI.

## Evidencia
- Wabi focal: `52 passed in 14.33s`.
- BRAIN_OS focal: `248 passed in 270.38s`.
- Wabi regression: `362 passed in 156.89s`.
- BRAIN_OS regression: `758 passed in 153.48s`.
- `py_compile`: PASS.
- Screenshot: `C:\Users\L-Tyr\.medioevo\wabi\runtime\outputs\ui_taskspec_gate_preview_20260519\wabi_ui_taskspec_gate_preview_interactive.png`.
- Endpoint smoke: `C:\Users\L-Tyr\.medioevo\wabi\runtime\outputs\ui_taskspec_gate_preview_20260519\gate_preview_endpoint_smoke.json`.

## Pendientes reales
- Disenar contrato futuro de sandbox local apply con `ActionGate`, `GhostGate`, `RollbackStore`, `PathAllowlist` y `TestRunner`.
- Mantener UI apply bloqueado hasta que el contrato de rollback y tests exista por TaskSpec.

## Riesgos
- Un preview explicativo puede confundirse con permiso de ejecutar. Mitigacion: status final siempre `APPLY_NOT_AVAILABLE_REVIEW_ONLY_V0_1` y Apply sigue bloqueado.
- El schema TaskSpec puede variar; la normalizacion usa defaults seguros.

## Proxima accion verificable
Crear el contrato de `Local Apply Readiness v0.1` como documento + tests de no-ejecucion, sin activar apply real.

## Segunda perdida
Los datos persisten. El operador no. Recalibrar desde este brief, no desde memoria implicita.

## 2026-05-19 - CloudBudgetGate UI Visual QA

## Estado
R_close: 0.07
Phi_eff: 0.92
Regimen: FUNCIONAL_UI_VISUAL_QA
ActionGate: APPROVE_LOCAL_VISUAL_UI_QA
CloudGate: PROPOSAL_ONLY_DOUBLE_OPT_IN
CloudBudgetGate: UI_VISIBLE_DRY_RUN_CONFIRMED
UIGate: PASS_LOCAL_8787
GraphicsGate: PLAN_ONLY_READY / graphics_live=false
PublicationGate: BLOCK

## Decisiones tomadas
- El servidor UI real puede correr en `127.0.0.1:8787` con el panel Cloud Budget visible.
- La evidencia visual se guarda fuera del repo en runtime local `.medioevo`.
- QA visual no autoriza live cloud; solo confirma UI/API/status.

## Cambios realizados
- No se modifico logica de presupuesto ni UI.
- Se actualizaron reportes de cierre y fingerprint de esta QA visual.
- Se guardo evidencia runtime redacted y screenshots locales.

## Evidencia
- Endpoint `/api/cloud-budget/status`: PASS, `source_of_truth=CloudBudgetGate.render_status`.
- Estado confirmado: `CLOUD_BUDGET_DRY_RUN`, `double_opt_in=false`, `proposal_only=true`, `cloud_provider_called=false`.
- Screenshot panel: `C:\Users\L-Tyr\.medioevo\wabi\runtime\outputs\ui_visual_qa\WABI_CLOUD_BUDGET_UI_VISUAL_QA_20260519\wabi_cloud_budget_ui_tall_20260519.png`.
- BRAIN_OS server focal: `229 passed in 116.51s (0:01:56)`.
- Wabi focal: `39 passed in 23.23s`.
- Wabi regression: `352 passed in 214.62s (0:03:34)`.
- `py_compile`: PASS.
- Manual no-live CLI: `build-assist-status`, `--once`, `build-assist-plan --dry-run`, REPL `/status` y `/providers` PASS.

## Pendientes reales
- Cablear el panel chat/work de la UI a `ConversationEngine`, sin activar cloud live por defecto.
- Si se agrega llamada build-assist desde UI, debe mostrar presupuesto antes y exigir doble opt-in.

## Riesgos
- Edge headless se uso solo como fallback de screenshot local; BrowserBridge live no fue activado.
- Coste/tokens NVIDIA siguen desconocidos si el provider no devuelve usage.

## Proxima accion verificable
Cablear UI chat/work panel a `ConversationEngine` manteniendo `cloud_provider_called=false` por defecto y tests de no-live.

## Segunda perdida
Los datos persisten. El operador no. Recalibrar desde este brief, no desde memoria implicita.

## 2026-05-19 - Wabi UI ConversationEngine

R_close: 0.13
Phi_eff: 0.88
Regimen: FUNCIONAL
ActionGate: APPROVE_LOCAL
CloudGate: PROPOSAL_ONLY_DOUBLE_OPT_IN
CloudBudgetGate: CLOUD_BUDGET_DRY_RUN
UIGate: LOCAL_UI_CONVERSATION_READY
ConversationGate: API_CONNECTED_TO_CONVERSATION_ENGINE
GraphicsGate: PLAN_ONLY_READY / graphics_live=false
PublicationGate: BLOCK

- Handoff limpio del QA visual Cloud Budget reconstruido en `docs/WABI_UI_VISUAL_QA_CLOUD_BUDGET_2026-05-19.md`.
- Agregado endpoint local `POST /api/conversation/turn`.
- UI `Wabi Conversation` consume `ConversationEngine.handle_turn` desde el servidor local.
- El endpoint usa modo efimero para UI: no persiste prompts completos ni escribe artefactos de turno.
- CloudBudgetGate sigue visible y `cloud_provider_called=false`.
- Servidor UI reiniciado localmente en `http://127.0.0.1:8787/`, nuevo PID `10552`.
- Evidencia visual: `C:\Users\L-Tyr\.medioevo\wabi\runtime\outputs\ui_conversation_engine_20260519\wabi_ui_conversation_engine.png`.

Proxima accion verificable:
Agregar un flujo UI `Review TaskSpec` que muestre el plan generado por ConversationEngine y lo deje listo para un gate futuro de apply local, sin aplicar por defecto.

## 2026-05-19 - Wabi UI Review TaskSpec v0.1

R_close: 0.12
Phi_eff: 0.89
Regimen: FUNCIONAL
ActionGate: APPROVE_LOCAL
CloudGate: PROPOSAL_ONLY_DOUBLE_OPT_IN
CloudBudgetGate: CLOUD_BUDGET_DRY_RUN
UIGate: LOCAL_UI_TASKSPEC_REVIEW_READY
ConversationGate: API_CONNECTED_TO_CONVERSATION_ENGINE
TaskSpecGate: REVIEW_ONLY_APPLY_BLOCKED
GraphicsGate: PLAN_ONLY_READY / graphics_live=false
PublicationGate: BLOCK

- Agregado `wabi_sabi/core/taskspec_review.py`.
- Agregados endpoints `GET /api/taskspec/latest`, `POST /api/taskspec/save-draft` y `POST /api/taskspec/apply`.
- UI `Review TaskSpec` muestra TaskSpec normalizado/redacted desde backend.
- `Apply bloqueado` responde `APPLY_BLOCKED_REVIEW_ONLY_V0_1` y no modifica fuentes.
- `Save Draft` guarda JSON redacted en runtime local sin prompt completo ni secreto.
- Corregido timeout de `provider-status` en tests temporales con `wabi_sabi/core/worktree.py`.
- Evidencia visual: `C:\Users\L-Tyr\.medioevo\wabi\runtime\outputs\ui_taskspec_review_20260519\wabi_ui_taskspec_review.png`.

Proxima accion verificable:
Crear `TaskSpec Gate Preview` para explicar requisitos de un apply local futuro sin ejecutarlo.

---

## 2026-05-19 - CloudBudgetGate UI v0.1

## Estado
R_close: 0.09
Phi_eff: 0.90
Regimen: FUNCIONAL_CLOUD_BUDGET_UI
ActionGate: APPROVE_LOCAL
CloudGate: PROPOSAL_ONLY_DOUBLE_OPT_IN
CloudBudgetGate: visible en UI como CLOUD_BUDGET_DRY_RUN/READY/EXCEEDED
UIGate: APPROVE_LOCAL_STATUS_PANEL
GraphicsGate: PLAN_ONLY_READY / graphics_live=false
PublicationGate: BLOCK

## Decisiones tomadas
- La UI local lee `CloudBudgetGate.render_status()` via `GET /api/cloud-budget/status`.
- La tarjeta `Cloud Budget` vive en `-= BRAIN_OS =-\apps\local\wabi_ui\index.html`.
- La UI no agrega boton para llamar NVIDIA ni aplicar output cloud.
- `operational_workbench_payload()` incluye `cloud_budget` para evidencia centralizada.

## Cambios realizados
- Modificado `-= BRAIN_OS =-\02_CLAUDIO\server\wabi_local_server.py`.
- Modificado `-= BRAIN_OS =-\apps\local\wabi_ui\index.html`.
- Agregado `tests/test_cloud_budget_ui_status.py`.
- Documentado en `docs/WABI_CLOUD_BUDGET_UI_2026-05-19.md`.

## Evidencia
- Focal UI: `5 passed in 11.15s`.
- Focal requerido: `39 passed in 12.25s`.
- `py_compile`: PASS para Wabi core/CLI/test UI y servidor UI BRAIN_OS.
- Regresion Wabi completa: `352 passed in 372.11s (0:06:12)`.
- BRAIN_OS server/UI focal: `229 passed in 138.64s (0:02:18)`.
- Manual no-live: `build-assist-status --json`, `--once "hola wabi"`, `build-assist-plan --dry-run --json`, REPL `/status`, `/providers`, `/exit`.
- No hubo nueva llamada live cloud.
- BrowserBridge live y graphics_live siguen apagados.

## Pendientes reales
- Reiniciar/abrir el servidor UI local si se quiere ver el panel en una ventana ya abierta.
- Si se agrega build-assist desde UI, mostrar presupuesto y exigir doble opt-in antes de llamada real.

## Proxima accion verificable
Reiniciar el servidor UI local y verificar visualmente el panel `Cloud Budget` sin llamar cloud.

---

## 2026-05-19 - CloudBudgetGate v0.1

## Estado
R_close: 0.10
Phi_eff: 0.88
Regimen: FUNCIONAL_CLOUD_BUDGET_GATE
ActionGate: APPROVE_LOCAL
CloudGate: PROPOSAL_ONLY_DOUBLE_OPT_IN
CloudBudgetGate: CLOUD_BUDGET_DRY_RUN sin doble opt-in; READY solo con presupuesto y doble bandera
GraphicsGate: PLAN_ONLY_READY / graphics_live=false
PublicationGate: BLOCK

## Decisiones tomadas
- Presupuesto cloud se controla por contador de llamadas, no por tokens/coste.
- Defaults: 3 llamadas por sesion, 10 por dia local, modo `strict`.
- `build-assist-status`, `build-assist-plan`, `/status`, `/providers` y `ConversationEngine` muestran o respetan `cloud_budget`.
- Antes de provider real se valida doble opt-in y presupuesto; si excede, `cloud_provider_called=false`.
- No se guardan prompts completos en budget JSON; solo etiqueta segura e hash.

## Cambios realizados
- Agregado `wabi_sabi/core/cloud_budget.py`.
- Modificados `wabi_sabi/core/build_assist_cloud.py`, `wabi_sabi/core/conversation_engine.py`, `wabi_sabi/cli/main.py`.
- Agregado `tests/test_cloud_budget.py`.
- Actualizados tests de build-assist, CLI conversacional y conversation engine.
- Documentado en `docs/WABI_CLOUD_BUDGET_GATE_2026-05-19.md`.

## Evidencia
- Focal: `34 passed in 15.93s`.
- `py_compile`: PASS.
- Wabi full: `347 passed in 192.89s (0:03:12)`.
- Manual no-live: `--once`, `build-assist-status`, `build-assist-plan --dry-run`, REPL `/status`, `/providers`, `usa nvidia...`, `/exit`.
- Budget JSON: `C:\Users\L-Tyr\.medioevo\wabi\runtime\cloud_budget\cloud_budget_20260519.json`.
- Secret scan focal del budget JSON: `0` coincidencias.

## Pendientes reales
- Exponer `cloud_budget` en la UI local.
- Medir usage/cost solo si el provider lo devuelve, sin hacerlo gate primario.
- Revisar rate limits reales de NVIDIA fuera de esta fase.

## Riesgos
- Sin `WABI_SESSION_ID`, cada proceso CLI crea sesion propia; limite diario sigue activo.
- `mode=warn` debe tratarse como REVIEW, no como aprobacion operacional.

## Proxima accion verificable
Exponer CloudBudgetGate en la UI local de Wabi sin activar llamadas live cloud.

## Segunda perdida
Los datos persisten. El operador no. Recalibrar desde este brief, no desde memoria implicita.

---

## 2026-05-19 - Wabi Conversational CLI v0.1

## Estado
R_close: 0.12
Phi_eff: 0.86
Regimen: FUNCIONAL_CONVERSATIONAL_CLI
ActionGate: APPROVE_LOCAL
CloudGate: PROPOSAL_ONLY_DOUBLE_OPT_IN
GraphicsGate: PLAN_ONLY_READY
PublicationGate: BLOCK

## Decisiones tomadas
- `wabi` sin argumentos abre REPL conversacional local-first con prompt `wabi>`.
- `ConversationEngine` queda como capa comun para CLI/UI adapters y envuelve `ConversationSession`.
- Natural language se convierte en `WorkIntent` y `TaskSpec` proposal-only.
- `GraphicsBridge` descubre DUAT graphics y genera scene/asset plans sin red, sin publish y sin aplicar fuentes.
- Build Assist NVIDIA se conserva proposal-only; no hubo live cloud call en esta fase.

## Cambios realizados
- Agregado `wabi_sabi/core/conversation_engine.py`.
- Agregado `wabi_sabi/core/graphics_bridge.py`.
- Modificado `wabi_sabi/cli/main.py` para usar el nuevo engine en `wabi` y `--once`.
- Agregados tests `tests/test_conversational_cli.py`, `tests/test_conversation_engine.py`, `tests/test_graphics_bridge.py`.
- Documentado en `docs/WABI_CONVERSATIONAL_CLI_2026-05-19.md`.

## Evidencia
- Focal conversacional requerido: `14 passed in 3.69s`.
- Focal conversacional + redaccion: `25 passed in 15.26s`.
- `py_compile`: PASS.
- Wabi full: `336 passed in 495.58s (0:08:15)`.
- Manual: `.\wabi.cmd --help`, `.\wabi.cmd --once "hola wabi" --json`, `.\wabi.cmd build-assist-status --json`, y REPL con `/help`, `/status`, escena DUAT, helper JSON, `/exit`.

## Pendientes reales
- Conectar UI local a `ConversationEngine` si se quiere equivalencia total UI/terminal.
- Definir endpoint/adapter live estable de DUAT renderer antes de cambiar `graphics_live=false`.
- Agregar contador/presupuesto por sesion para llamadas cloud de build-assist.

## Riesgos
- UI y CLI comparten capa disponible, pero la UI aun no esta cableada directamente.
- GraphicsBridge es plan-only; no debe interpretarse como generador live de assets.
- Costos/tokens NVIDIA dependen del provider y pueden venir `null`.

## Proxima accion verificable
Integrar presupuesto local por sesion para build-assist cloud y mostrarlo en `/status`/`/providers`, sin activar nuevas llamadas live.

## Segunda perdida
Los datos persisten. El operador no. Recalibrar desde este brief, no desde memoria implicita.

---

## 2026-05-18 - Multi-step Workpacks v0.2 integrated status

## Estado
R_close: 0.04
Phi_eff: 0.95
Regimen: OPTIMO_MULTI_STEP_WORKPACKS_v0_2
CloudLiveGate: BLOCK_THIS_RUN
NvidiaSmokeGate: DO_NOT_CALL
DeepSeekGate: REVIEW_QUOTA_OR_BILLING
ProviderState: SMOKE_FAIL_REDACTED
PublicationGate: BLOCK

## Decisiones tomadas
- Multi-step Workpacks v0.2 queda local-only, manual tick y delegado a Local Execute / Workpack Bridge / Scheduler.
- Wabi UI muestra Multi-step Workpacks junto a Local Hub, Agent Hub, Agent Chat, Scheduler y Operational Workbench.
- Provider state se preserva: no SMOKE_PASS, NVIDIA DO_NOT_CALL y DeepSeek REVIEW_QUOTA_OR_BILLING.

## Evidencia
- Run: `qa_artifacts/release_validation/RUN_MULTI_STEP_WORKPACKS_v0_2_20260518/`.
- Wabi full: 293 passed.
- Wabi safe-tests: ok=true, 293 passed, witness_event_id=36.
- 02_CLAUDIO full: 687 passed.
- HTTP smoke local provider/chat/multi-step: PASS.
- SecretScan focal: PASS, finding_count=0.

## Proxima accion verificable
Choose Agent Chat persistence/search v0.3, Scheduler priorities/dependencies v0.2, public-safe docs update, or Claudio Mission Control dashboard v0.1.

---

## Estado
R_close: 0.04
Phi_eff: 0.94
Regimen: FUNCIONAL_PUBLIC_UPDATE_AND_LOCAL_EXECUTE_v0_2_READY
CloudLLMGate: BLOCK_PRIVATE_WORKSPACE
NvidiaSmokeGate: DO_NOT_CALL
ProviderState: SMOKE_FAIL_REDACTED

## Decisiones tomadas
- Public Hub follow-up cerrado en GitHub PR #4.
- LinkedIn queda MANUAL_POST_REQUIRED con copy public-safe listo.
- Siguiente run tecnico: Local Execute v0.2.

## Evidencia
- Public repo npm test: 44 passed; build PASS.
- medioevo.space rutas Hub: HTTP 200.
- SecretScan/BoundaryScan/ScienceClaimGate: PASS.

## Proxima accion verificable
Ejecutar Local Execute v0.2 con TaskSpec, GhostGate, rollback y WitnessLog.

---
# NEXT_SESSION_BRIEF WABI-SABI

## Estado
R_close: 0.05
Phi_eff: 0.93
Regimen: FUNCIONAL_PUBLIC_SAFE_HUB_AND_LOCAL_AGENT_HUB
Autonomy level: OWNER_ADMIN_DEVELOPER_PUBLIC_SAFE_NO_PAUSE
CloudLLMGate: NOT_USED
NvidiaSmokeGate: DO_NOT_CALL
ProviderState: SMOKE_FAIL_REDACTED

## Decisiones tomadas
- Local Operator Hub v0.1 agregado en Claudio/Wabi UI.
- Agent Hub v0.1 y MSN-style Agent Chat v0.1 quedan local-only.
- Execute local permanece BLOCK en v0.1; solo prepare, GhostGate y queue.
- Public-safe Hub publicado en medioevo.space sin bridge de ejecucion local.

## Cambios realizados
- /api/local-hub, /api/agent-hub y /api/agent-chat/* activos.
- Wabi UI muestra Local Hub, Agent Hub y chat local de agentes.
- Public Hub verificado en /hub, /agents, /theory, /roadmap y /updates/2026-05-18.

## Evidencia
- Wabi full: 279 passed.
- Wabi safe-tests: ok=true, witness event 28.
- 02_CLAUDIO focused: 88 passed; full: 597 passed.
- GEODIA: 74 passed.
- DUAT predictive: 117 passed.
- Public repo: npm test 44 passed; build PASS.
- medioevo.space routes: HTTP 200.

## Pendientes reales
- Wabi/Claudio execute local v0.2 con sandbox, rollback y WitnessLog.
- Agent Chat persistence/search.
- NVIDIA manual route review antes de cualquier retry.

## Riesgos
- Execute endpoint puede confundirse con apply activo; v0.1 devuelve BLOCK.
- Public Hub no debe conectar con ejecucion local.

## Proxima accion verificable
Implementar execute local v0.2 solo para tareas sandbox/documentacion con TaskSpec, GhostGate, rollback y WitnessLog.

---
# NEXT_SESSION_BRIEF WABI-SABI

## Estado
R_close: 0.04
Phi_eff: 0.94
Regimen: OPTIMO_WABI_UI_VISUAL_ASSET_POLISH_LOCAL
Autonomy level: OWNER_ADMIN_DEVELOPER_PUBLIC_SAFE_NO_PAUSE

## Decisiones tomadas
- UI visual polish cerrado con assets locales controlados.
- NVIDIA/cloud permanece bloqueado: DO_NOT_CALL.
- Provider state no cambia: SMOKE_FAIL_REDACTED / route REVIEW.

## Cambios realizados
- Inventario de assets Wabi: 42 PNG.
- Copia controlada de 3 assets a apps/local/wabi_ui/assets/wabi_visual_20260518/.
- Rediseno visual de apps/local/wabi_ui/index.html.
- /api/operational-workbench reporta theme wabi_visual_20260518.
- Export estatico y handoff creados en qa_artifacts/release_validation/RUN_WABI_UI_VISUAL_ASSET_POLISH_20260518/.

## Evidencia
- Wabi full: 279 passed.
- Wabi safe-tests: ok=true, witness event 26.
- 02_CLAUDIO full: 629 passed.
- GEODIA: 74 passed.
- DUAT predictive: 117 passed.
- SecretScan focal: PASS.

## Pendientes reales
- Wabi fallback-only v0.4 sobre fixture controlado.
- DUAT/Wabi unified dashboard bridge.
- NVIDIA manual route review antes de cualquier retry.

## Riesgos
- NVIDIA route diagnostic sigue REVIEW; no repetir smoke sin revision manual.

## Bloqueos
- CloudLiveGate BLOCK_THIS_RUN.
- NvidiaSmokeGate DO_NOT_CALL.
- PublicationGate BLOCK.

## Proxima accion verificable
Ejecutar Wabi fallback-only v0.4 sobre fixture interno controlado, sin cloud.

## Segunda perdida
Los datos persisten. El operador no. Recalibrar desde este brief, no desde memoria implicita.



## 2026-05-18 - Agent Chat Routing v0.2

- StateFingerprint: AGENT-CHAT-ROUTING-v0-2-20260518.
- Agent Chat now routes local MSN-style messages to agents, detects mentions, creates TaskSpec drafts, creates Workpack drafts, attaches messages to Workpacks, writes system status messages, and exposes inbox/outbox.
- Chat routing does not execute. Execution remains behind Workpack Bridge + Local Execute + TaskSpec + GhostGate APPROVE + rollback + WitnessLog.
- Provider preserved: SMOKE_FAIL_REDACTED; NVIDIA DO_NOT_CALL; PublicationGate BLOCK.
- Evidence: qa_artifacts/release_validation/RUN_AGENT_CHAT_ROUTING_v0_2_20260518/.
- Tests: 02_CLAUDIO 690 passed; Wabi 283 passed; safe-tests ok witness 32; GEODIA 74; DUAT predictive 117; compileall PASS; HTTP smoke PASS; SecretScan focal PASS.
- Next: Workpack Scheduler v0.1, Multi-step Workpacks v0.2, or Agent Chat persistence/search v0.3.

## Workpack Scheduler v0.1 - 2026-05-18

StateFingerprint: WORKPACK-SCHEDULER-v0-1-20260518

- Implemented local-only manual-tick Workpack Scheduler v0.1.
- Added `/api/workpack-scheduler` plus enqueue, approve, tick, retry, rollback and evidence endpoints.
- Integrated Scheduler into Local Hub, Agent Hub, Agent Chat and Wabi UI.
- Demo sequence passed: step-1, dependency-gated step-2, docs-note; CLOUD lane blocked.
- Provider remains SMOKE_FAIL_REDACTED / NVIDIA DO_NOT_CALL; DeepSeek remains REVIEW_QUOTA_OR_BILLING; PublicationGate BLOCK.
- Verification: Wabi 290 passed; safe-tests ok=true witness 33; 02_CLAUDIO 709 passed; GEODIA 74 passed; DUAT 117 passed; compileall PASS; SecretScan PASS.

## 2026-05-18 - BrowserBridge multibackend + concilio opt-in

R_close: 0.09
Phi_eff: 0.92
Regimen: FUNCIONAL_BROWSER_BRIDGE_GATEADO
Autonomy level: 4
PublicationGate: BLOCK
CloudLLMGate: REVIEW_DOUBLE_OPT_IN
BrowserSendGate: BLOCK_BY_DEFAULT

## Decisiones tomadas
- BrowserBridge conserva `dry-run` como fallback determinista.
- `chrome-devtools-mcp` queda como backend primario de lectura cuando existe
  herramienta local y `WABI_ALLOW_BROWSER_BRIDGE=1`; Wabi no instala ni lanza
  dependencias automaticamente.
- Envio AI requiere doble permiso: `--send` y `WABI_ALLOW_BROWSER_SEND=1`,
  mas servicio allowlisted y adapter probado disponible.
- Kimi WebBridge es primer candidato live; el resto del catalogo entra
  prepare-only via `council`.
- Respuestas con codigo solo avanzan como `wabi.cloud_code_proposal.v0_1`
  validado localmente. No hay auto-apply.
- `gitleaks version` timeout en `02_CLAUDIO` ahora degrada a
  `VERSION_TIMEOUT` para no romper el hub.

## Cambios realizados
- Actualizados `wabi_sabi/core/browser_bridge.py`, `wabi_sabi/cli/main.py` y
  `tests/test_browser_bridge.py`.
- Agregado `docs/BROWSER_BRIDGE_MULTIBACKEND_2026-05-18.md`.
- Actualizados README, USAGE, ARCHITECTURE y continuidad Wabi.
- Actualizados `02_CLAUDIO/core/external_secret_tools.py` y
  `02_CLAUDIO/tests/test_external_secret_tools.py`.

## Evidencia
- Wabi full: `293 passed`.
- Wabi safe-tests: `ok=true`, `293 passed`, `witness_verified=true`,
  `witness_event_id=35`.
- BrowserBridge focal: `10 passed`.
- CLI/cloud/browser gate focal: `37 passed`.
- BRAIN_OS world model: `gate_accuracy=1.0`, `false_approve_rate=0.0`.
- BRAIN_OS MTS v0.3: `success=True`, `mts_accuracy=0.98`.
- `02_CLAUDIO` full: `688 passed`.

## Pendientes reales
- Live Kimi smoke sigue `REVIEW_SKIPPED` hasta que existan `--send`,
  `WABI_ALLOW_BROWSER_SEND=1`, `WABI_ALLOW_BROWSER_BRIDGE=1` y
  `WABI_KIMI_WEBBRIDGE_URL`.
- Selector pack para ChatGPT/Claude/Gemini/etc. queda pendiente antes de
  cualquier live concilio multi-servicio.

## Proxima accion verificable
Preparar un selector pack de adapters de concilio con fixtures fake y una
prueba Kimi local opt-in que espere `REVIEW_SKIPPED` cuando falte cualquier
flag.

Next: Multi-step Workpacks v0.2 or Agent Chat persistence/search v0.3.

---

## 2026-05-18 - BrowserBridge Selector Pack v0.2

## Estado
R_close: 0.05
Phi_eff: 0.94
Regimen: OPTIMO_BROWSER_BRIDGE_SELECTOR_PACK_v0_2
Autonomy level: OWNER_ADMIN_DEVELOPER_PUBLIC_SAFE_NO_PAUSE
BrowserSendGate: REVIEW_SEND_ONLY_WITH_DOUBLE_OPT_IN
ExternalServiceGate: REVIEW_PER_SERVICE_ADAPTER
CloudLLMGate: BLOCK_PRIVATE_WORKSPACE
NvidiaSmokeGate: DO_NOT_CALL
DeepSeekGate: REVIEW_QUOTA_OR_BILLING
PublicationGate: BLOCK

## Decisiones tomadas
- Selector Pack v0.2 queda como matriz de capacidades y decision local para BrowserBridge.
- `dry-run` sigue default y fallback.
- Kimi es el unico candidato `READY_SEND_REVIEW`; sin doble opt-in queda sin envio.
- Servicios sin adapter probado quedan `PREPARE_ONLY`.
- DevTools MCP solo lectura queda detras de gate local y herramienta disponible.
- Respuestas con codigo se convierten a `wabi.cloud_code_proposal.v0_1` proposal-only, sin auto-apply.
- BrowserBridge queda visible en Wabi UI y Operational Workbench.

## Cambios realizados
- Agregado `wabi_sabi/core/browser_bridge_selector_pack.py`.
- Extendidos `wabi_sabi/core/browser_bridge.py`, `wabi_sabi/cli/main.py` y `tests/test_browser_bridge.py`.
- Agregada seccion BrowserBridge a `apps/local/wabi_ui/index.html`.
- Agregado `/api/browser-bridge` y payload BrowserBridge en `/api/operational-workbench`.
- Creado run de evidencia `qa_artifacts/release_validation/RUN_BROWSER_BRIDGE_SELECTOR_PACK_v0_2_20260518/`.

## Evidencia
- BrowserBridge focal: `21 passed`.
- Expanded Wabi/provider/CLI focal: `81 passed`.
- Wabi full: `304 passed`.
- Safe-tests: `ok=true`, witness `38`, verified.
- BRAIN_OS Wabi local server/UI: `180 passed`.
- `02_CLAUDIO` full: `690 passed`.
- GEODIA: `74 passed`.
- DUAT predictive: `117 passed`.
- HTTP 8788: endpoints requeridos PASS.
- SecretScan focal: PASS, `finding_count=0`.

## Pendientes reales
- Reiniciar el servidor existente en `127.0.0.1:8787` en una accion controlada para que cargue la nueva ruta/UI; la verificacion actual uso servidor temporal 8788.
- Kimi smoke real requiere `--send`, `WABI_ALLOW_BROWSER_SEND=1`, `WABI_ALLOW_BROWSER_BRIDGE=1`, `WABI_KIMI_WEBBRIDGE_URL` y payload publico.
- DevTools visual QA v0.3 requiere `WABI_ALLOW_BROWSER_BRIDGE=1` y herramienta local disponible.

## Riesgos
- Confundir ranking de council con permiso de envio o apply.
- Confundir `SEND_REVIEW` de Kimi con `safe_to_send=true`.
- Confundir propuesta validada con TaskSpec/PatchPlan/aplicacion.

## Bloqueos
- No envio de workspace privado, rutas privadas, codigo interno, canon/libros/RPG/TCG, credenciales, cookies ni raw prompts.
- No NVIDIA smoke, DeepSeek retry, push, deploy, commit ni publicacion.

## Proxima accion verificable
Si se configuran flags/URL seguros, ejecutar Kimi public synthetic smoke; si no, preparar Kimi WebBridge setup guide redactada.

## Segunda perdida
Los datos persisten. El operador no. Recalibrar desde este brief, no desde memoria implicita.


## 2026-05-19 - Wabi build-assist cloud temporal

R_close: 0.18
Phi_eff: 0.82
Regimen: FUNCIONAL
ActionGate: APPROVE_LOCAL para implementacion; REVIEW para live NVIDIA smoke.

- Implementado `build-assist-status` y `build-assist-plan`.
- Default de supervivencia: NVIDIA `nano-30b`; `super`/`ultra` quedan como revision manual.
- Sin `WABI_BUILD_ASSIST_CLOUD=1` y `WABI_ALLOW_CLOUD_PROVIDERS=1`, `build-assist-plan` fuerza dry-run y no llama red.
- Cloud sigue `proposal_only`: no auto-apply, `real_apply_allowed=false`, `publication_gate=BLOCK`.
- Evidencia: `37 passed in 5.69s`; regresion completa Wabi `317 passed in 114.72s`.
- Smoke CLI: `build-assist-status` reporto `cloud_live_ready=false`, NVIDIA configurado por env redacted y `remaining_cloud_calls=12`.

Proxima accion verificable:
Ejecutar un smoke NVIDIA `nano-30b` con prompt sintetico y banderas de sesion, sin aplicar fuentes, si el operador quiere probar consumo real.

## 2026-05-19 - NVIDIA nano-30b live smoke

R_close: 0.14
Phi_eff: 0.88
Regimen: FUNCIONAL
ActionGate: APPROVE_LOCAL
CloudGate: LIVE_SMOKE_PASS
PublicationGate: BLOCK

- Agregado `build-assist-smoke --provider nvidia --model nano-30b --live --json`.
- Smoke sin `--live`: `REVIEW_LIVE_FLAG_REQUIRED`, `cloud_provider_called=false`, `prompt_sent=false`.
- Smoke live con banderas de sesion: `LIVE_SMOKE_PASS`.
- Provider/model: `nvidia`, `nano-30b`, `nvidia/nemotron-3-nano-30b-a3b`.
- Modo conservado: `proposal_only`.
- `cloud_provider_called=true` solo con `WABI_BUILD_ASSIST_CLOUD=1` y `WABI_ALLOW_CLOUD_PROVIDERS=1`.
- `applied_to_sources=false`, `secrets_printed=false`, `redaction=PASS`.
- Artefacto smoke: `C:\Users\L-Tyr\.medioevo\wabi\runtime\outputs\build_assist_smoke\wabi_build_assist_nvidia_smoke_20260519-133139.json`.
- Redaction scan: `files_scanned=2`, `secret_value_hits=0`.
- Tests: focal recomendado `42 passed in 14.67s`; regresion Wabi `322 passed in 111.97s`; `py_compile` PASS.

Proxima accion verificable:
Usar `build-assist-plan` con `nano-30b` en una tarea Wabi pequena y bounded; validar propuesta local antes de cualquier apply.

## 2026-05-21 - HypothesisPacket / Counterexample Mode v0.1

R_close: 0.12
Phi_eff: 0.88
Regimen: FUNCIONAL
ActionGate: APPROVE_LOCAL_CORE / REVIEW_STRONG_CLAIMS
PublicationGate: BLOCK

- Implementado contrato `HypothesisPacket` en shared-contracts.
- Implementado `wabi_sabi/core/hypothesis_packet.py`.
- Agregado CLI `wabi hypothesis "<claim>" --json`.
- `ConversationEngine` clasifica `hypothesis_request` por hipotesis/conjetura/contraejemplo/unit distance.
- `--once` y safe LLM response exponen tags `hypothesis_packet`, `counterexample_search`, `claim_gate`.
- Claims cientificos/publicos/comerciales quedan `REVIEW`.
- El modo no aplica fuentes, no llama cloud, no publica y registra artefacto runtime + WitnessLog cuando persiste.
- Evidencia: shared contracts `11 tests OK`; Wabi focal `20 passed`; Wabi regression `393 passed`; py_compile PASS.

Proxima accion verificable:
Usar `.\wabi.cmd hypothesis "claim concreto del motor" --json`, ejecutar un falsador local y adjuntar evidencia antes de convertir el claim en canon/producto/publicacion.
