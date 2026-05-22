# DECISIONS WABI-SABI

## 2026-05-20 - Wabi LLM Safe JSON Contract

- Decision: `wabi_sabi/core/llm_work_response.py` es la fuente comun para respuestas JSON seguras de trabajo LLM.
- Decision: las respuestas UI/API exponen `status=OK|REVIEW`; estados internos de LLM quedan en `llm_status`.
- Decision: `rollback_snapshot_required=true` es obligatorio en el contrato, aunque Apply Local no corra automaticamente.
- Decision: `graphics_plan` top-level siempre conserva `graphics_live=false`.
- Decision: cada respuesta normalizada registra runtime JSON redacted y WitnessLog local, sin prompts completos.
- Decision: `tags` es parte del contrato seguro para que UI/CLI distingan proposal-only, double opt-in, DUAT graphics plan-only y publication block.
- Decision: `docs/WABI_LLM_RESPONSIBLE_USE_2026-05-20.md` es la referencia humana de uso responsable para LLM cloud proposal-only.
- Decision: `wabi --once "<tarea>" --json` preserva `schema=wabi.conversation_turn.v0_1` y agrega campos del contrato seguro en top-level.
- Decision: el tag literal `LLM_proposal` se conserva para compatibilidad con el contrato humano entregado por el owner.
- Decision: `metadata` es parte del contrato seguro para prioridad, riesgo, categoria, relevancia, incrementalidad, fallback local, simulacion de apply y presupuesto.

## 2026-05-19 - Wabi LLM Cloud Work Mode

- Decision: `WABI_LLM_PROVIDER_CLOUD_DEFAULT=1` habilita preferencia cloud proposal-only por defecto.
- Decision: una llamada live real requiere doble opt-in: `WABI_BUILD_ASSIST_CLOUD=1` y `WABI_ALLOW_CLOUD_PROVIDERS=1`.
- Decision: CloudBudgetGate decide si el provider puede ser llamado; si excede presupuesto, `cloud_provider_called=false`.
- Decision: output cloud debe validar contrato `wabi.cloud_code_proposal.v0_1` antes de convertirse en TaskSpec.
- Decision: Apply Local sigue separado y no acepta autoridad directa del provider cloud.

## 2026-05-19 - Wabi Work Mode v1

- Decision: Wabi queda en `WORK_MODE_READY` para uso diario local.
- Decision: el uso diario debe preferir tareas pequenas y medianas con TaskSpec, Review, Gate Preview, Apply Local Preview, Apply Local, tests y reporte.
- Decision: no se agregan mas features hasta que el usuario trabaje con el flujo actual y aparezca un bug real o una necesidad verificada.
- Decision: GitHub, medioevo.space y publicacion de assets quedan bloqueados fuera del Work Mode hasta que `docs/WABI_RELEASE_BLOCKERS_2026-05-19.md` sea resuelto con evidencia.
- Decision: cloud sigue `proposal_only` y no se activa live sin doble opt-in explicito.

## 2026-05-19 - WABI Assets Du WABI Local Integration + Release Gate

- Decision: `Assets Du WABI` puede integrarse solo como subconjunto local re-encodeado y manifestado mientras `AssetGate=REVIEW_PUBLIC_SAFE_ASSETS_REQUIRED`.
- Decision: ZIPs y archivos fuente de assets quedan `REVIEW_REQUIRED`; no se extraen, no se copian y no se publican.
- Decision: los cuatro PNGs seleccionados quedan `publication_allowed=false` hasta que el owner confirme provenance/licencia/public-safe.
- Decision: no se hace commit/push desde el repo host amplio `C:\Users\L-Tyr` con dirty state no relacionado.
- Decision: no se actualiza medioevo.space hasta que exista staging limpio, repo correcto, scan final y PublicationGate aprobado.

## 2026-05-19 - Wabi UI TaskSpec Gate Preview v0.1

- Decision: `Gate Preview` es explicativo y no ejecutable en v0.1.
- Decision: el preview debe venir del backend `taskspec_review.py`; JS solo renderiza.
- Decision: Apply mantiene `APPLY_BLOCKED_REVIEW_ONLY_V0_1`, pero puede adjuntar `gate_preview.reason=APPLY_NOT_AVAILABLE_REVIEW_ONLY_V0_1`.
- Decision: los gates futuros minimos son `ActionGate`, `GhostGate`, `RollbackStore`, `TestRunner` y `PathAllowlist`.
- Decision: no se habilita ningun boton UI para correr comandos, escribir fuentes o aplicar patches.

## 2026-05-19 - CloudBudgetGate UI Visual QA

- Decision: reiniciar el servidor UI local en `127.0.0.1:8787` es una accion operacional aprobada cuando el PID registrado esta muerto y no hay proceso escuchando.
- Decision: la QA visual confirma estado, no habilita ejecucion cloud ni botones live.
- Decision: Edge headless local es evidencia aceptable de UI cuando el navegador integrado no expone herramienta callable; se ejecuta con URL local y background networking deshabilitado.
- Decision: mantener `cloud_provider_called=false` como criterio central de cierre para esta fase.

## 2026-05-18 - Wabi fallback-only coding acceptance v0.2

- Acceptance de programacion asistida corre en runtime sandbox, no en codigo productivo.
- Proposal source determinista aprobado para evitar cloud/model nondeterminism.
- Provider state se preserva como `SMOKE_FAIL_REDACTED`; NVIDIA sigue `DO_NOT_CALL`.
- UI local expone `/api/coding-acceptance` como evidencia operativa.

## 2026-05-18 - Tree/workbench/code cleanup

- Decision: caches se mueven a quarantine con rollback, no se borran.
- Decision: evidencia provider v0.3/v0.4/v0.5 queda en rutas existentes y se agrega indice logico para no romper referencias.
- Decision: duplicados de runtime/datasets quedan en review/protected, no se mueven.
- Decision: fixes legacy compileall son sintacticos y no cambian provider/runtime activo.
- Decision: cloud smoke sigue bloqueado; provider state permanece `SMOKE_FAIL_REDACTED`.

## 2026-05-18 - Cloud provider v0.5

- Decision: no repetir smoke NVIDIA hasta que el diagnostico de ruta/modelo pase.
- Decision: conservar `SMOKE_FAIL_REDACTED` como estado real y no declararlo `SMOKE_PASS`.
- Decision: registrar alias candidates localmente sin llamar cloud por cada alias.
- Decision: `--allow-model-list` queda como `REVIEW_NOT_IMPLEMENTED_NO_REMOTE_CALL` hasta definir una API segura.
- Decision: integrar el panel provider/debug en UI principal como vista read-only de estado, no como ejecutor cloud.

## 2026-05-18 - Cloud provider v0.4

- Decision: NVIDIA/Nemotron no se considera PASS; el smoke real termino `SMOKE_FAIL_REDACTED`.
- Decision: el flag cloud se uso de forma efimera para una sola llamada y no queda persistente.
- Decision: identificadores internos de provider/account se tratan como sensibles y se redactan.
- Decision: el debug loop puede operar con `target_root=runtime` para tareas sinteticas que no tocan workspace real.
- Decision: el panel provider/debug queda en QA local antes de integrarse a la UI principal.

## 2026-05-18 - Cloud proposal provider-gated v0.2

- Decision: agregar `cloud-proposal-from-provider` como generador provider-gated
  de propuestas `wabi.cloud_code_proposal.v0_1`.
- Decision: `--dry-run` ejercita el pipeline completo sin llamar red; el modo
  live depende de `WABI_ALLOW_CLOUD_PROVIDERS`, credenciales en entorno/vault y
  ActionGate.
- Decision: guardar prompts/respuestas/propuestas en runtime externo es valido
  como entrada confiable solo si el path cae bajo `config.runtime_root`; los
  targets de escritura siguen limitados al workspace y denylist de rutas.
- Decision: si el provider no devuelve JSON valido, el flujo queda en `REVIEW`
  y no genera apply.

## 2026-05-18 - Cloud code proposal v0.1

- Decision: implementar `wabi.cloud_code_proposal.v0_1` como contrato offline
  cloud-proposes/local-executes, sin llamadas live a proveedores.
- Decision: permitir que TaskSpecs generados bajo `runtime/outputs` se usen
  como entrada, mientras los targets de escritura siguen bloqueando `runtime`,
  `.env`, vendors, builds, TCG/game y rutas externas.
- Decision: no agregar apply directo desde cloud proposal; la aplicacion queda
  separada en `task-spec-apply` bajo ActionGate local.
- Decision: comandos solicitados por la nube y test commands deben ser
  compatibles con el allowlist de SafeExecutor; shell chaining queda rechazado.

## 2026-05-17 - Multimodal intake local-first

- Decision: la primera version multimodal usa camara/microfono locales y solo
  persiste metadatos sanitizados.
- Motivo: permite cerrar evidencia real sin exponer imagen/audio crudo ni
  depender de proveedor cloud.
- Gate: `APPROVE` para captura local reversible con witness; `REVIEW` para
  cualquier ruta cloud multimodal.
- Resultado: `wabi multimodal` opera en CLI, escribe artefactos JSON, verifica
  `WitnessLog` y mantiene `cloud_provider_called=false`.
- Nota: el gate interpretativo de BRAIN_OS queda separado del gate operativo de
  captura. Si `Phi_eff_world < 0.60`, la captura puede pasar pero la integracion
  cognitiva queda bloqueada/revisable.

## 2026-05-16 - Ruta unica

- Decision: `apps/local/wabi-sabi` es la unica ruta de proyecto Wabi-Sabi.
- Motivo: habia codigo/config/adapters/docs dispersos que podian convertirse en
  segundos centros de verdad.
- Evidencia: inventario por `rg`, hash de fuentes externas, curador preflight y
  validaciones locales.
- Gate: `APPROVE` para absorcion local de adapters/config no secretos;
  `REVIEW` para secretos, protected IP, staging, assets y publicaciones.

## 2026-05-16 - No borrar fuentes alejadas

- Decision: no borrar ni mover fuentes originales en esta pasada.
- Motivo: limpieza destructiva requiere migration map y gate especifico.
- Resultado: wrappers y referencias se conservaron; root `adapters/` y root
  `config/` se archivaron de forma reversible bajo `_archive/legacy` despues
  de absorberlos en la ruta canonica.

## 2026-05-18 - Cloud provider v0.3

- Decision: el estado provider se expresa por contrato JSON verificable, no por
  texto inferido del chat.
- Decision: `SMOKE_PASS` solo puede declararse despues de un live smoke exitoso
  y parseado contra el contrato minimo.
- Decision: si `WABI_ALLOW_CLOUD_PROVIDERS` esta apagado, el estado final es
  `CLOUD_DISABLED_BY_FLAG` y no se llama cloud aunque exista credencial.
- Decision: cloud sigue `proposal_only`; apply local queda separado, gateado y
  con rollback.
- Decision: stdout/stderr de tests se redactan antes de persistirse.

# 2026-05-18 - WABI_FALLBACK_ONLY_CODING_ACCEPTANCE_v0_3

- Decision: no NVIDIA/cloud calls; keep `DO_NOT_CALL` until manual route review.
- Decision: deterministic stub is the local proposal source for reproducible acceptance.
- Decision: v0.3 becomes latest in `/api/coding-acceptance`; v0.2 remains preserved in `versions`.
- Decision: safe-tests timeout defaults to 600s to match current full-suite duration.

## 2026-05-18 - BrowserBridge multibackend v0.1

- Decision: BrowserBridge queda local-first; `dry-run` sigue como fallback
  determinista y ningun backend real se instala automaticamente.
- Decision: `chrome-devtools-mcp` es el backend primario de lectura/snapshot/
  extract/screenshot solo cuando el operador habilita
  `WABI_ALLOW_BROWSER_BRIDGE=1` y la herramienta local existe.
- Decision: `ai-consult --send` requiere doble permiso:
  flag CLI `--send` y `WABI_ALLOW_BROWSER_SEND=1`; sin ambos, solo hay
  artefacto revisable.
- Decision: Kimi WebBridge es el primer candidato live; el resto del catalogo
  queda prepare-only hasta selector pack probado.
- Decision: `council` prepara propuestas de todos los servicios allowlisted,
  pero las respuestas son consejo/propuesta y nunca permiso de ejecucion.
- Decision: codigo devuelto por un servicio live debe entrar como
  `wabi.cloud_code_proposal.v0_1` y validarse localmente; no hay auto-apply.
- Decision: timeouts de herramientas externas de seguridad en `02_CLAUDIO`
  degradan a status revisable (`VERSION_TIMEOUT`) y no rompen el hub.

## 2026-05-18 - BrowserBridge Selector Pack v0.2

- Decision: el selector pack es la autoridad local para clasificar servicio,
  backend, modo, payload seguro, doble opt-in y gate de publicacion.
- Decision: `dry-run` sigue siendo default incluso cuando hay backends reales
  configurables.
- Decision: `chrome-devtools-mcp` no es canal de envio; solo puede ser lectura
  local/snapshot cuando el gate y herramienta local existen.
- Decision: Kimi WebBridge es el primer candidato live, pero `SEND_REVIEW` no
  equivale a `safe_to_send=true`.
- Decision: council v0.2 rankea servicios y prepara artefactos; no llama ni
  aplica por defecto.
- Decision: respuesta externa con codigo solo puede producir propuesta
  `wabi.cloud_code_proposal.v0_1` validada; TaskSpec/PatchPlan/apply quedan
  separados y locales.
- Decision: Wabi UI muestra estado BrowserBridge, pero los botones de envio y
  apply externo quedan bloqueados visualmente por gate.

## 2026-05-19 - Build Assist Cloud Temporal

- Decision: Wabi puede usar cloud durante la construccion solo como capa de propuestas, no como ejecutor.
- Default: `build-assist-plan` usa NVIDIA `nano-30b` para supervivencia de credito.
- Escalada: `super`, `ultra` y aliases publicos grandes quedan en revision manual.
- Gate: live cloud requiere `WABI_BUILD_ASSIST_CLOUD=1` y `WABI_ALLOW_CLOUD_PROVIDERS=1`; sin ambas, dry-run.

## 2026-05-19 - NVIDIA nano-30b Live Smoke

- Decision: NVIDIA `nano-30b` queda validado como proveedor temporal para build-assist proposal-only.
- Decision: El smoke live no autoriza apply; solo valida ruta proveedor -> JSON seguro -> artefacto.
- Decision: Uso/costo quedan en `null` si la respuesta del adapter no expone tokens/coste.

## 2026-05-19 - Wabi Conversational CLI v0.1

- Decision: `wabi` sin argumentos abre el nuevo CLI conversacional local-first.
- Decision: `ConversationEngine` es la capa comun para CLI/UI adapters y envuelve `ConversationSession` para no duplicar memoria, status y proveedores.
- Decision: todo trabajo natural se normaliza a `WorkIntent` y `TaskSpec` proposal-only antes de cualquier escritura real.
- Decision: NVIDIA/build-assist sigue siendo propuesta solamente; el turno conversacional no llama provider live ni aplica output cloud.
- Decision: `GraphicsBridge` queda plan-only en v0.1: descubre DUAT graphics y emite scene/asset plans, pero no publica, no llama red y no modifica fuentes.

## 2026-05-19 - CloudBudgetGate v0.1

- Decision: controlar build-assist cloud por contador local de llamadas, no por tokens/coste.
- Decision: defaults: `WABI_CLOUD_MAX_CALLS_PER_SESSION=3`, `WABI_CLOUD_MAX_CALLS_PER_DAY=10`, `WABI_CLOUD_BUDGET_MODE=strict`.
- Decision: sin doble opt-in, el budget queda `CLOUD_BUDGET_DRY_RUN` y no incrementa llamadas completadas.
- Decision: si el presupuesto se excede en modo strict, `build-assist-plan` bloquea antes de provider con `CLOUD_BUDGET_EXCEEDED` y `cloud_provider_called=false`.
- Decision: no guardar prompts completos en el JSON de presupuesto; usar etiqueta segura y `intent_hash`.

## 2026-05-19 - CloudBudgetGate UI v0.1

- Decision: la UI local debe mostrar CloudBudgetGate desde `CloudBudgetGate.render_status()`, no desde calculos duplicados en JavaScript.
- Decision: `GET /api/cloud-budget/status` es solo lectura y siempre reporta `cloud_provider_called=false`.
- Decision: la tarjeta UI no incluye boton para llamar NVIDIA ni boton para aplicar output cloud.
- Decision: `operational_workbench_payload()` incluye `cloud_budget` para que la evidencia de UI y API sea reconstruible.

## 2026-05-19 - Wabi UI ConversationEngine v0.1

- Decision: `POST /api/conversation/turn` es el endpoint local para que la UI use `ConversationEngine`.
- Decision: JavaScript no clasifica intents; solo renderiza `intent`, `gate`, `cloud_budget` y `graphics` devueltos por Python.
- Decision: la llamada UI a ConversationEngine es efimera: `persist_turns=false`, `include_prompt_in_turn=false`, `write_artifacts=false`.
- Decision: `graphics_live=false` y `cloud_provider_called=false` son invariantes por defecto desde la UI.
- Decision: la UI puede preparar `TaskSpec`, pero no aplica output cloud ni patches.

## 2026-05-19 - Wabi UI Review TaskSpec v0.1

- Decision: el panel `Review TaskSpec` renderiza solo TaskSpecs normalizados por backend.
- Decision: `POST /api/taskspec/apply` existe solo para devolver `APPLY_BLOCKED_REVIEW_ONLY_V0_1`.
- Decision: `Save Draft` guarda exclusivamente version redacted/local sin prompt completo.
- Decision: `Run Tests` queda plan-only/deshabilitado en v0.1.
- Decision: `git_worktree_summary()` no debe subir hasta el home para workspaces temporales bajo `AppData`, evitando heredar el repo host y timeouts.

## 2026-05-21 - HypothesisPacket / Counterexample Mode v0.1

- Decision: el resultado del unit distance problem se absorbe como metodo operacional: claim, contraafirmacion, falsadores, evidencia, ActionGate, WitnessLog y decision antes de canon/producto/publicacion.
- Decision: `HypothesisPacket` vive en contratos compartidos para que Wabi, DUAT y otros carriles puedan validar la misma forma.
- Decision: Wabi solo prepara busqueda de contraejemplos en modo `proposal_only`; no llama cloud, no aplica fuentes y mantiene `publication_gate=BLOCK`.
- Decision: claims cientificos, publicos o comerciales quedan en `REVIEW` aunque tengan forma valida.
- Decision: el CLI canonico es `wabi hypothesis "<claim>" --json`; el lenguaje natural se enruta como `hypothesis_request`.
