# RISKS WABI-SABI

## 2026-05-20 - Wabi LLM Safe JSON Contract

- Risk: consumidores antiguos de `/api/taskspec/llm-proposal` pueden esperar `status=CLOUD_BUDGET_DRY_RUN`. Mitigacion: conservar `llm_status` y documentar `status=OK|REVIEW` como contrato externo.
- Risk: runtime JSON/WitnessLog se confundan con autorizacion de apply. Mitigacion: contrato fuerza `proposal_only=true`, `applied_to_sources=false` y `rollback_snapshot_required=true`.
- Risk: plan grafico DUAT se interprete como ejecucion grafica live. Mitigacion: `graphics_plan.graphics_live=false` y warning explicito.
- Risk: prompts completos se filtren por evidencia. Mitigacion: normalizador no incluye `prompt` y tests verifican que no se guarde contenido completo.
- Risk: `tags` se use como permiso de ejecucion. Mitigacion: los tags son clasificadores informativos; Apply Local sigue dependiendo de confirmacion explicita, PathAllowlist, rollback, tests y scans.

## 2026-05-19 - Wabi LLM Cloud Work Mode

- Risk: activar doble opt-in puede consumir cuota cloud. Mitigacion: CloudBudgetGate controla llamadas por sesion/dia y registra planned/completed/blocked.
- Risk: el provider devuelve JSON invalido o cambio demasiado amplio. Mitigacion: validar `wabi.cloud_code_proposal.v0_1`; invalido queda REVIEW.
- Risk: confundir proposal cloud con apply local. Mitigacion: `proposal_only=true`, `applied_to_sources=false`; Apply Local sigue con PathAllowlist, rollback y tests.
- Risk: prompts o secretos completos en artefactos runtime. Mitigacion: LLM proposal usa intent hash redacted y no guarda prompt completo en propuesta.

## 2026-05-19 - Wabi Work Mode v1

- Risk: seguir construyendo features sin uso diario aumenta R operacional. Mitigacion: usar Work Mode para tareas locales reales antes de abrir sistemas nuevos.
- Risk: confundir LOCAL WORK PASS con release externo aprobado. Mitigacion: `docs/WABI_RELEASE_BLOCKERS_2026-05-19.md` separa GitHub/deploy/assets como BLOCK/REVIEW.
- Risk: aplicar cambios demasiado amplios desde Wabi. Mitigacion: mantener tareas pequenas, PathAllowlist, Gate Preview, rollback snapshot y tests.
- Risk: cloud live se active por costumbre. Mitigacion: CloudGate sigue `PROPOSAL_ONLY_DOUBLE_OPT_IN`; Work Mode no requiere cloud live.

## 2026-05-19 - WABI Assets Du WABI Local Integration + Release Gate

- Riesgo: confundir candidato local metadata-clean con asset publicable. Mitigacion: manifest conserva `publication_allowed=false` y docs bloquean GitHub/medioevo.space hasta provenance.
- Riesgo: incorporar ZIPs o paquetes de codigo sin revision. Mitigacion: archivos `.zip` quedaron registrados solamente, sin extraccion ni copia.
- Riesgo: publicar desde repo incorrecto o con cambios no relacionados. Mitigacion: `GitGate=REVIEW_BLOCKED`; requiere staging path-scoped en repo confirmado.
- Riesgo: medioevo.space use pipeline distinto al asumido o contenga claves publishable que requieren revision. Mitigacion: deploy no ejecutado; revisar pipeline/domain y secret boundary antes de release.
- Riesgo: una linea 404 no critica de browser QA oculte recurso faltante. Mitigacion: `broken_images=0`, screenshot confirma render de assets y se debe revisar consola otra vez antes de public release.

## 2026-05-19 - Wabi UI TaskSpec Gate Preview v0.1

- Riesgo: interpretar `Gate Preview` como autorizacion para apply. Mitigacion: `apply_status=BLOCKED`, `reason=APPLY_NOT_AVAILABLE_REVIEW_ONLY_V0_1`, boton Apply bloqueado y tests del endpoint.
- Riesgo: duplicar logica de gates en UI. Mitigacion: UI consume `GET /api/taskspec/gate-preview` y solo renderiza.
- Riesgo: TaskSpec incompleto o schema variable. Mitigacion: normalizacion backend con defaults seguros y `affected_paths_preview=[]` si no hay rutas explicitas.
- Riesgo: cloud/graphics se confundan con ejecucion live. Mitigacion: preview conserva `proposal_only=true`, `cloud_provider_called=false` y `graphics_live=false`.

## 2026-05-19 - CloudBudgetGate UI Visual QA

- Riesgo: confundir panel visible con autorizacion para llamar NVIDIA. Mitigacion: panel sigue status-only, muestra `proposal_only=true`, `double_opt_in=false`, `cloud_provider_called=false`.
- Riesgo: QA visual con navegador headless pueda disparar red externa de navegador. Mitigacion: URL local `127.0.0.1`, Edge con `--disable-background-networking`, sin BrowserBridge live y sin flags cloud.
- Riesgo: servidor viejo o PID stale oculte version actual de UI. Mitigacion: PID muerto documentado, servidor local reiniciado y endpoint validado.
- Riesgo: usage/cost desconocidos. Mitigacion: contador local por llamadas sigue como gate primario.

## 2026-05-18 - Wabi fallback-only coding acceptance v0.2

- No usar el PASS local como evidencia de NVIDIA; cloud sigue bloqueado.
- El fixture clamp01 solo prueba el loop, no capacidades de edicion productiva compleja.
- Mantener `runtime` como frontera para acceptance hasta que exista fixture controlado mas realista.

| id | severidad | riesgo | mitigacion |
|---|---|---|---|
| WABI-R-001 | ALTA | Duplicar Wabi-Sabi en rutas externas | Canon unico en `apps/local/wabi-sabi`; externos quedan wrappers o referencias |
| WABI-R-002 | ALTA | Copiar secretos o secret loaders al canon | No se copiaron loaders; se dejan como `REVIEW_SECRET_HOOK` |
| WABI-R-003 | MEDIA | Romper autostart al mover implementation source | Se mantuvo wrapper host y solo se cambio destino de adapters/logs |
| WABI-R-004 | MEDIA | Confundir protected IP/assets con motor activo | Source cards y pet asset quedan como referencia, no runtime |
| WABI-R-005 | MEDIA | Borrar fuentes originales sin gate | No hubo borrado; root legacy quedo archivado con `MIGRATION_LOG.md` |
| WABI-R-006 | MEDIA | Confundir captura fisica exitosa con integracion cognitiva aprobada | Separar `gate` operativo de `world_model_gate`/`fusion_gate`; documentar `Phi_eff_world` |
| WABI-R-007 | ALTA | Enviar media cruda a cloud durante pruebas multimodales | Cloud queda `REVIEW`, `cloud_provider_called=false`, media cruda excluida de payloads/witness |
| WABI-R-008 | ALTA | Tratar una propuesta cloud como permiso de ejecucion | `cloud-proposal-*` no aplica; aplica solo `task-spec-apply` con gate local |
| WABI-R-009 | ALTA | Filtrar secretos por contenido generado, logs o comandos cloud | `cloud_code_proposal` redacts secret-like values y rechaza comandos con secretos |
| WABI-R-010 | MEDIA | Usar comandos no soportados por SafeExecutor desde propuesta cloud | `commands_requested` y `test_commands` deben pasar allowlist local |
| WABI-R-011 | MEDIA | Romper el flujo por runtime externo fuera del workspace | Propuestas/TaskSpecs generados pueden leerse desde `config.runtime_root`, pero targets siguen path-gated dentro del workspace |
| WABI-R-012 | ALTA | Aceptar respuesta provider no estructurada como codigo ejecutable | `cloud-proposal-from-provider` extrae solo JSON valido; si falla, queda `REVIEW` y no hay apply |
| WABI-R-013 | ALTA | Declarar `SMOKE_PASS` sin smoke live real | `provider_status_contract` separa `provider_state`, `live_smoke_status` y `cloud_provider_called`; con flag apagado queda `CLOUD_DISABLED_BY_FLAG` |
| WABI-R-014 | ALTA | Filtrar secretos por stderr/stdout de tests | `SafeExecutor` redacta stdout/stderr antes de persistir resultados |
| WABI-R-015 | ALTA | Repetir smoke ciego con alias incorrecto | v0.5 bloquea `recommended_next_smoke=DO_NOT_CALL` hasta route diagnostic/manual review |
| WABI-R-016 | MEDIA | Confundir alias registrado con alias validado live | Alias candidates quedan `LOCAL_REVIEW_ONLY`; no implican `SMOKE_PASS` |
| WABI-R-017 | MEDIA | Panel UI presentando estado aspiracional | Panel consume diagnostico real/local y muestra `SMOKE_FAIL_REDACTED` |
| WABI-R-018 | MEDIA | Quarantine de caches confundida con borrado | Move manifest y rollback script; `delete_direct=false` |
| WABI-R-019 | MEDIA | Mover evidencia runtime duplicada y perder trazabilidad | Runtime duplicates quedan `REVIEW_LEGACY`, no se mueven |
| WABI-R-020 | ALTA | Tocar datasets/canon por limpieza amplia | Datasets/canon/libros/RPG quedan `KEEP_PROTECTED` |
# Wabi Cloud Provider v0.4 - 2026-05-18

- Riesgo: NVIDIA devolvio provider not-found durante smoke real. Mitigacion: clasificar `SMOKE_FAIL_REDACTED`, no declarar PASS y preparar guia redactada.
- Riesgo: errores cloud pueden incluir identificadores internos. Mitigacion: redaccion extendida para function/account IDs y SecretScan focal.
- Riesgo: apply sobre workspace real desde TaskSpec de prueba. Mitigacion: `target_root=runtime` y rollback antes de write.

# 2026-05-18 - Wabi Fallback-only Coding Acceptance v0.3

- Risk: fallback-only PASS can be confused with NVIDIA PASS. Mitigation: provider state remains `SMOKE_FAIL_REDACTED` and `DO_NOT_CALL`.
- Risk: full-suite runtime can exceed old safe-test timeout. Mitigation: safe-test timeout updated to 600s and verified.

# 2026-05-18 - BrowserBridge multibackend v0.1

- Risk: AI web consultation could be mistaken for local execution approval. Mitigation: responses remain `proposal_only`; code must validate as `wabi.cloud_code_proposal.v0_1`.
- Risk: accidental online send. Mitigation: require `--send`, `WABI_ALLOW_BROWSER_SEND=1`, allowlisted service, available backend and proven live adapter.
- Risk: catalog services beyond Kimi are treated as working live adapters. Mitigation: non-Kimi services are `prepare-only` until selector pack is tested.
- Risk: external browser backend installs or global config changes. Mitigation: status detects only; no auto-install, no curl pipe, no global config, no Hermes `--yolo`.
- Risk: external security helper timeout breaks Wabi hub status. Mitigation: `gitleaks version` timeout returns `VERSION_TIMEOUT` and keeps status inspectable.

# 2026-05-18 - BrowserBridge Selector Pack v0.2

- Risk: `SEND_REVIEW` can be misread as permission to send. Mitigation:
  selector returns `safe_to_send=false` unless CLI flag, env flags, safe URL and
  public/sanitized payload all pass.
- Risk: council ranking can be misread as provider execution. Mitigation:
  `live_attempts=0`, `online_ai_called=false` and prepare-only classification
  are persisted in artifacts.
- Risk: Chrome DevTools MCP could become a broad browser control surface.
  Mitigation: v0.2 exposes read-only/snapshot only, no install, no external
  network, no publication.
- Risk: response-to-proposal could bypass local gate. Mitigation: conversion
  creates proposal-only artifacts and tests block delete patches and
  out-of-scope paths.
- Risk: old server on 8787 hides the new UI until restart. Mitigation: v0.2
  verified on temporary 8788 and restart is left as explicit operational next
  action.

## 2026-05-19 - Build Assist Cloud Temporal

- Risk: quemar creditos por retries o modelos grandes. Mitigacion: default `nano-30b`, presupuesto `WABI_BUILD_ASSIST_MAX_CLOUD_CALLS`, no auto-retry en quota/billing/rate-limit.
- Risk: confundir propuesta cloud con permiso de aplicar. Mitigacion: `cloud_authority=proposal_only`, `real_apply_allowed=false`, PatchPlan/TaskSpec local.
- Risk: fuga de contexto privado. Mitigacion: prompt saneado, no workspace completo, no secretos, no canon privado, no `.env`.

## 2026-05-19 - NVIDIA nano-30b Live Smoke

- Risk: usar el PASS del smoke como autorizacion general de cloud. Mitigacion: mantener `proposal_only`, prompts sinteticos o bounded y validacion local.
- Risk: cuota/costo no reportado por el adapter. Mitigacion: conservar presupuesto local por conteo de llamadas y no hacer retries agresivos.
- Risk: outputs del proveedor incluyan codigo no pedido. Mitigacion: smoke exige `Do not include code`; flujo real debe validar schema antes de PatchPlan.
## 2026-05-19 - Wabi Conversational CLI v0.1

- Riesgo: la UI local todavia no consume directamente `ConversationEngine`; el contrato existe para compartir capa, pero falta cablear componente UI si se quiere equivalencia total.
- Riesgo: `GraphicsBridge` descubre DUAT graphics local, pero no hay API live estable del renderer; por eso queda `graphics_live=false` y `graphics_plan_ready=true`.
- Riesgo: comandos conversacionales de codigo preparan `TaskSpec`; aplicar cambios sigue requiriendo ruta local separada con ActionGate, rollback y tests.
- Riesgo: costos/tokens de NVIDIA no se pueden estimar si el provider no devuelve uso.

## 2026-05-19 - CloudBudgetGate v0.1

- Riesgo: el control por llamadas no equivale a control exacto de coste; es el gate primario solo porque usage/cost puede venir ausente.
- Riesgo: si no se fija `WABI_SESSION_ID`, cada proceso CLI usa una sesion propia; el limite diario sigue protegiendo la jornada.
- Riesgo: `WABI_CLOUD_BUDGET_MODE=warn` permitiria continuar bajo REVIEW; mantener `strict` para seguridad operacional.
- Riesgo: UI aun no muestra el presupuesto; por ahora esta visible en CLI conversacional y build-assist JSON.

## 2026-05-19 - CloudBudgetGate UI v0.1

- Riesgo: un servidor UI ya abierto puede estar sirviendo codigo anterior hasta reinicio; mitigacion: endpoint/panel probados por test y reinicio queda accion operacional separada.
- Riesgo: el panel puede leerse como permiso para llamar cloud; mitigacion: texto visible `proposal-only`, `cloud_provider_called=false` y sin boton de llamada.
- Riesgo: `usage_known=false` y `cost_known=false` pueden ocultar coste real; mitigacion: mantener contador local como gate primario.

## 2026-05-19 - Wabi UI ConversationEngine v0.1

- Riesgo: el panel conversacional puede parecer capaz de aplicar cambios; mitigacion: respuesta muestra `applied_to_sources=false` y no hay apply automatico.
- Riesgo: prompts de usuario podrian quedar en logs si se usa el modo CLI normal; mitigacion: el endpoint UI instancia ConversationEngine con persistencia y artefactos desactivados.
- Riesgo: `GraphicsBridge` devuelve planes utiles pero no tiene renderer live; mitigacion: `graphics_live=false` visible y tests verifican plan-only.
- Riesgo: costos/tokens cloud siguen desconocidos si el proveedor no devuelve usage; mitigacion: UI mantiene `CLOUD_BUDGET_DRY_RUN` mientras no haya doble opt-in.

## 2026-05-19 - Wabi UI Review TaskSpec v0.1

- Riesgo: un usuario lea TaskSpec como permiso de ejecucion; mitigacion: `Apply bloqueado`, endpoint bloqueado y flags `applied_to_sources=false`.
- Riesgo: guardar drafts con prompts completos o secretos; mitigacion: `taskspec_review.py` elimina campos prompt-like y guarda hashes/redacciones.
- Riesgo: `Run Tests` desde UI ejecute comandos sin gate; mitigacion: boton deshabilitado y v0.1 plan-only.
- Riesgo: workspaces temporales hereden el repo host y ralenticen tests; mitigacion: `git_worktree_summary()` deja de subir al home para hijos sin `.git`.

## 2026-05-21 - HypothesisPacket / Counterexample Mode v0.1

- Riesgo: convertir un resultado matematico externo en claim fuerte de MEDIOEVO/CLAUDIO. Mitigacion: se absorbe solo como metodo; `publication_gate=BLOCK`.
- Riesgo: leer `SUPPORTED` como verdad cientifica. Mitigacion: claims cientificos/publicos/comerciales quedan `REVIEW` y requieren revision humana.
- Riesgo: usar falsadores como permiso de apply. Mitigacion: `hypothesis_request` no tiene escritura, `applied_to_sources=false` y no produce PatchPlan.
- Riesgo: tocar UI/API activa fuera del workspace primario. Mitigacion: esta fase implementa core/CLI/ConversationEngine; BRAIN_OS UI queda como siguiente accion con gate separado.
