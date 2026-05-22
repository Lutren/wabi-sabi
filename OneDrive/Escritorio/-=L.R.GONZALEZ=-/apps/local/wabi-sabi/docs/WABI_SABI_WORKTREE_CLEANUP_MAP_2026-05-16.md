# WABI_SABI_WORKTREE_CLEANUP_MAP 2026-05-16

## Decision

El carril `apps/local/wabi-sabi` no debe limpiarse por borrado amplio. El
estado sucio actual representa trabajo funcional validado: runtime local,
motor modular, curador, proveedores, test runner, ActionGate, rollback,
worktree scan, safe executor y documentos de continuidad.

La limpieza correcta es clasificar y cerrar por modulo.

## Estado Verificado

- Ruta: `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\apps\local\wabi-sabi`
- Cambios modificados visibles: 16 archivos tracked.
- Archivos nuevos visibles despues de ignorar `runtime/`: 96 antes de crear
  este mapa; 98 despues de crear los dos mapas de cierre.
- `runtime/` y `docs/engine/local_only/` quedan ignorados como evidencia local.
- Caches regenerables: 0 candidatos despues del postcheck global.
- Suite final sin bytecode/cache de pytest: `209 passed in 72.40s`.
- Prueba focal del modulo `engine`: `18 passed in 2.97s`.
- Prueba focal del modulo `safe execution`: `21 passed in 19.76s`.
- Prueba focal del modulo `operator`: `10 passed in 10.67s`.
- Prueba focal del modulo `providers`: `35 passed in 2.17s`.
- Prueba focal del modulo `curador`: `28 passed in 8.23s`.
- Suite completa final: `209 passed in 102.70s`.
- Postcheck regenerable final: `approved=0`, `blocked=0`, `bytes=0`.
- Runtime evidence: 194 archivos, 913448 bytes, resumido sin borrar.

## Clasificacion

| carril | accion | razon |
|---|---|---|
| `wabi_sabi/engine/*` | KEEP_SOURCE | Motor modular clean-room; no es vendor ni fork. |
| `wabi_sabi/core/*` nuevos | KEEP_SOURCE | Capacidades operativas Wabi-Sabi ya cubiertas por tests. |
| `wabi_sabi/cli/*` nuevos | KEEP_SOURCE | Entrypoints locales para operador y automatizacion. |
| `tests/test_*.py` nuevos | KEEP_TESTS | Evidencia primaria; no limpiar. |
| `docs/*.md` nuevos | KEEP_DOCS | Handoff y contratos de uso. |
| `NEXT_SESSION_BRIEF.md`, `TEST_REPORT.md`, `SESSION_FINGERPRINT*.json` | KEEP_HANDOFF | Continuidad de sesion y evidencia. |
| `wabi-window.cmd`, `wabi-window.ps1` | KEEP_LAUNCHER_REVIEW | Entrypoints locales; revisar por launcher pero no borrar. |
| `runtime/` | KEEP_LOCAL_IGNORED | Evidencia local, logs, SQLite y outputs; no versionar. |
| `docs/engine/local_only/` | KEEP_LOCAL_IGNORED | Planes/proyectos no publicables. |

## No Borrar

- Codigo nuevo con tests.
- Docs de continuidad.
- `runtime/` aunque este ignorado: contiene evidencia y witness local.
- Launchers `wabi-window.*` sin revision de startup.

## Accion Ejecutada

- `.gitignore` actualizado para ignorar `runtime/`.
- Se conserva `docs/engine/local_only/`.
- Se genera este mapa para que la siguiente accion pueda cerrar por modulo.
- Se cierra el primer modulo interno, `engine`, con
  `SESSION_FINGERPRINT_WABI_ENGINE_MODULE_20260516.json`.
- Se cierra el segundo modulo interno, `safe execution`, con
  `SESSION_FINGERPRINT_WABI_SAFE_EXECUTION_MODULE_20260516.json`.
- Se cierra el tercer modulo interno, `operator`, con
  `SESSION_FINGERPRINT_WABI_OPERATOR_MODULE_20260516.json`.
- Se cierra el cuarto modulo interno, `providers`, con
  `SESSION_FINGERPRINT_WABI_PROVIDERS_MODULE_20260516.json`.
- Se cierra el quinto modulo interno, `curador`, con
  `SESSION_FINGERPRINT_WABI_CURADOR_MODULE_20260516.json`.
- Se ejecuta suite completa final y limpieza post-suite de caches generados.
- Se resume `runtime/` en
  `docs/WABI_SABI_RUNTIME_EVIDENCE_SUMMARY_2026-05-16.md`.

## Proximo Cierre Por Modulo

Orden recomendado:

1. `engine`: cerrado con prueba focal y fingerprint.
2. `safe execution`: cerrado con prueba focal y fingerprint.
3. `operator`: cerrado con prueba focal y fingerprint.
4. `providers`: cerrado con prueba focal y fingerprint.
5. `curador`: cerrado con prueba focal y fingerprint.
6. `runtime evidence`: resumido y preservado; zero-byte job logs quedan como
   `REVIEW_CANDIDATE`, no borrados.

## ActionGate

`APPROVE`: actualizar ignore/docs/briefs/tests y clasificar el arbol.

`REVIEW`: archivar o mover launchers, runtime logs, SQLite, docs historicos o
grandes grupos de tests.

`BLOCK`: borrar fuente, publicar, exponer secretos, tocar rutas privadas,
reescribir historia Git o mezclar con RPG/TCG.
