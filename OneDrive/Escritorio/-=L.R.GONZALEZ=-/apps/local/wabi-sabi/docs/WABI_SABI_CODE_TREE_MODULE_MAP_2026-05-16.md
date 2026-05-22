# WABI_SABI_CODE_TREE_MODULE_MAP 2026-05-16

## Proposito

Mapa operativo del arbol de codigo Wabi-Sabi despues de la integracion de motor
modular y curador. Sirve para que Wabi-Sabi programe por modulos sin depender
de memoria implicita ni mezclar capas.

## Modulos

| modulo | rutas | contrato |
|---|---|---|
| CLI local | `wabi_sabi/cli/main.py`, `wabi_sabi/cli/parser.py`, `wabi_sabi/cli/job_runner.py` | Exponer comandos locales; no publicar ni llamar red por defecto. |
| Motor modular | `wabi_sabi/engine/` | Extraer patrones clean-room y generar specs locales. |
| Programacion segura | `patch_planner.py`, `safe_executor.py`, `rollback_store.py`, `task_spec_planner.py`, `programming.py`, `programmer_workpack.py` | Planificar, aplicar y revertir cambios internos con tests. |
| Operador | `operator_panel.py`, `project_scan.py`, `test_plan.py`, `safe_test_runner.py`, `worktree.py`, `tool_registry.py` | Estado, tests allowlisted, resumen Git sin leer contenido sensible. |
| Proveedores | `provider_orchestrator.py`, `ollama_bridge.py`, `codex_bridge.py`, `cloud_adapters.py`, `provider_onboarding.py`, `user_config.py` | Base local primero; cloud solo opt-in. |
| Curador | `curator_assistant.py`, `curator_fichas.py`, `cerebro_*`, `redaction.py` | Clasificar, fichar, comparar y redactar sin borrar por defecto. |
| Observacionismo runtime | `claim_contract.py`, `decision_log.py`, `eml.py`, `functional_status.py`, `geodia_*`, `environment.py`, `runtime_diagnostics.py` | Medir, registrar decisiones y mantener claims con evidencia. |
| Conversacion/agentes | `conversation.py`, `conversational.py`, `auto_router.py`, `blueprint_policy.py`, `browser_gate.py`, `job_queue.py`, `live_context.py`, `comms_append.py` | Enrutamiento local, jobs y contexto operativo. |

## Tests Por Contrato

| contrato | tests |
|---|---|
| CLI y parser | `tests/test_cli.py`, `tests/test_patch_cli.py` |
| Motor modular | `tests/test_engine.py`, `tests/test_engine_project_runtime.py` |
| Ejecucion segura | `tests/test_safe_executor.py`, `tests/test_task_spec_planner.py`, `tests/test_worktree.py` |
| Operador y pruebas | `tests/test_operator_panel.py`, `tests/test_project_scan.py`, `tests/test_test_plan.py`, `tests/test_safe_test_runner.py` |
| Proveedores | `tests/test_provider_orchestrator.py`, `tests/test_ollama_bridge.py`, `tests/test_provider_onboarding.py`, `tests/test_codex_bridge.py` |
| Curador/Cerebro | `tests/test_curator_assistant.py`, `tests/test_curator_fichas.py`, `tests/test_cerebro_*.py`, `tests/test_redaction_and_cloud_adapters.py` |
| Observacionismo | `tests/test_claim_contract.py`, `tests/test_decision_log.py`, `tests/test_eml.py`, `tests/test_geodia_*.py`, `tests/test_formal_contract_intake.py` |

## Regla De Programacion

Wabi-Sabi puede programar sobre este motor en este orden:

1. `project-scan` para entender el repo.
2. `engine-intake` o `engine-plan` para convertir idea en plan.
3. `engine-task-spec` o `task-spec-plan` para convertirlo en cambios.
4. `patch-apply` con test allowlisted.
5. `run-safe-tests` para cerrar evidencia.
6. `SESSION_FINGERPRINT` y `NEXT_SESSION_BRIEF` para continuidad.

## Fronteras

- `runtime/` es evidencia local ignorada.
- `docs/engine/local_only/` es no publicable.
- Launchers Windows se revisan por carril startup antes de moverlos.
- No se toca juego/TCG, secretos, publicacion ni proveedores cloud sin gate.
