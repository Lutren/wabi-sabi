# TESTING_DEBUG_BENCHMARKS_FINAL

Fecha local: 2026-04-29

Alcance congelado. No se crearon suites, benchmarks, rutas, skills, manifests ni capas nuevas. No se arrancaron daemons. No se uso `-AcknowledgePreviewRisk`. No se uso `git add .`. No se corrigieron bugs nuevos.

## 0. Evidencia base

Archivos/reports usados como evidencia:

- `PRODUCT_MAP.md`
- `FINAL_RELEASE_PREP_SUMMARY.md`
- `RELEASE_EVIDENCE.md`
- `QA_RESULTS.md`
- `PUBLISHING_PLAN.md`
- `PRIVATE_GAME_BOUNDARY.md`
- `-=MEDIOEVO=-\-=LIBROS\claudio\reports\SYSTEM_OBSERVACIONISMO_REPORT.md`
- `-=MEDIOEVO=-\-=LIBROS\claudio\runtime\symphony_claudio\latest_preflight.json`
- `-=MEDIOEVO=-\-=LIBROS\claudio\runtime\host_observacionista\latest_report.json`
- `-=MEDIOEVO=-\-=LIBROS\claudio\runtime\observacionista\benchmark_suite\benchmark_suite_latest.md`

Archivo tocado por esta consolidacion:

- `TESTING_DEBUG_BENCHMARKS_FINAL.md`

Runtime tocado por preflight existente durante la consolidacion:

- `-=MEDIOEVO=-\-=LIBROS\claudio\runtime\symphony_claudio\latest_preflight.json`

No se stageo nada.

## 1. Estado Git acotado

Comandos:

```powershell
git status --short --untracked-files=no
```

Resultados:

| repo / ruta | estado tracked observado |
|---|---|
| `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-` | sin cambios tracked visibles antes de crear este reporte |
| `...\-=MEDIOEVO=-\-=LIBROS` | cambios tracked en `claudio/CLAUDE.md`, `claudio/NEXT_SESSION_BRIEF.md`, `claudio/PENDIENTES_MASTER.md`, `claudio/catalog/catalog.json`, `claudio/claudio_api_server.py`, `claudio/config/hardware_profiles.py`, `claudio/core/embeddings.py`, `claudio/core/prompt_cache.py`, `claudio/core/provider_hub.py`, `claudio/website/js/store-integration.js`, `claudio/website/pricing.html` |
| `...\-=MEDIOEVO=-\-=LIBROS\claudio` | cambios tracked en `NEXT_SESSION_BRIEF.md`, `PENDIENTES_MASTER.md`, `claudio_tui.py`, `config/hardware_profiles.py` |
| `E:\Medioevo_RPG` | sin cambios tracked visibles |

Interpretacion: hay trabajo concurrente en `-=LIBROS` y `claudio`. No tocar, no revertir, no stagear globalmente.

## 2. Suites disponibles

### 2.1 Root release test runner

Comando de inventario:

```powershell
python tools\release\run_tests.py --json
```

Resultado: 11 suites disponibles, en modo dry-run por defecto.

| suite | comando declarado | nota |
|---|---|---|
| `obsai-core-pytest` | `python -m pytest tests -q` en `packages/open-dev/obsai-core` | open tooling MIT candidate |
| `residueos-pytest` | `python -m pytest tests -q` en `packages/open-dev/residueos` | open tooling MIT candidate |
| `gemma-cleanup-pytest` | `python -m pytest tests -q` en `packages/open-dev/gemma-observacionismo-cleanup` | no ejecuta modelo pesado |
| `observacionismo-gate-import` | `python -c "import observacionismo_gate; ..."` | import smoke |
| `mini-office-pytest` | `python -m pytest tests -q` en `apps/commercial/mini-office` | app comercial propietaria |
| `claudio-pytest` | `python -m pytest tests/ -x --quiet` en `-=MEDIOEVO=-/-=LIBROS/claudio` | suite grande |
| `argus-npm-ci-dry-run` | `npm ci --dry-run --ignore-scripts --no-audit --no-fund` | no basta como prueba final de Argus |
| `asistente-negocio-check` | `npm run check` | app comercial propietaria |
| `flujocrm-check` | `npm run check` | app comercial propietaria |
| `hormiguero-flask-smoke` | `python tools/release/hormiguero_smoke.py` | Flask smoke sin servidor externo |
| `private-metaevo-lint` | `npm run lint` en `-=MEDIOEVO=-/-=LIBROS/metaevo-tcg` | skipped salvo `--include-private` |

### 2.2 Root release build/QA runner

Comando de inventario:

```powershell
python tools\release\run_builds.py --json
```

Resultado: 10 suites disponibles, en modo dry-run por defecto.

| suite | comando declarado | nota |
|---|---|---|
| `secret-scan` | `python tools/release/scan_secrets.py` | bloqueo de publicacion si falla |
| `release-free-dev-dry-run` | `python tools/release/package_free_dev.py` | paquete open tooling |
| `release-paid-apps-dry-run` | `python tools/release/package_paid_apps.py` | paquete apps comerciales |
| `product-manifest` | `python tools/release/product_manifest.py` | manifest de release, no crear nuevo en esta pausa |
| `argus-clean-generated-before-build` | `python tools/release/clean_generated_artifacts.py --execute --json` | mueve/archiva artifacts; no ejecutar en pausa |
| `argus-release-check` | `python tools/release/argus_release_check.py --json` | check canonico de Argus |
| `asistente-public-safe-check` | `npm run check` | comercial |
| `asistente-audit-high` | `npm audit --omit=dev --audit-level=high` | comercial |
| `flujocrm-check` | `npm run check` | comercial |
| `private-metaevo-build` | `npm run build` en `metaevo-tcg` | skipped salvo `--include-private` |

### 2.3 Claudio local

Comando de inventario:

```powershell
Get-ChildItem tests -Filter 'test_*.py'
```

Resultado: 101 archivos `test_*.py` detectados en `-=MEDIOEVO=-\-=LIBROS\claudio\tests`.

Suites focales conocidas:

- `tests\test_system_observacionista.py`
- `tests\test_host_observacionista.py`
- `tests\test_observacion_action_gate.py`
- `tests\test_observacionismo_benchmark_suite.py`
- `tests\test_observacionismo_download_intake.py`
- `tests\test_observacionismo_promotion_matrix.py`
- `tests\test_gemma4_benchmark_guard.py`
- `tests\test_gemma4_model_lifecycle.py`
- `tests\test_gemma4_observacion_benchmark_suite.py`
- `tests\test_gemma4_observacion_contract.py`
- `tests\test_gemma4_observacion_gate_report.py`
- `tests\test_gemma4_observacion_optimizer.py`
- `tests\test_model_router.py`

### 2.4 Observacionismo benchmark runner

Comando de inventario:

```powershell
python tools\run_observacionismo_benchmark_suite.py --help
```

Opciones existentes:

- `--quick`
- `--skip-duat-audit`
- `--skip-download-intake`
- `--skip-promotion-matrix`
- `--output-dir`

No se creo ningun benchmark nuevo.

### 2.5 Symphony preflight

Comando existente:

```powershell
python tools\setup_claudio_symphony.py --json --require-ready
```

Launcher bloqueado por diseno:

```powershell
powershell -ExecutionPolicy Bypass -File tools\run_claudio_symphony.ps1
```

Regla activa: no usar `-AcknowledgePreviewRisk` hasta que `ready_to_launch=true`.

### 2.6 Juego privado

Comando de inventario:

```powershell
rg --files E:\Medioevo_RPG -g 'Validate*.tscn' -g 'validate*.gd' -g 'test_*.gd'
```

Resultado: 46 archivos de validacion/test detectados. Relevantes antes de declarar integracion RPG:

- `E:\Medioevo_RPG\tools\campaign\ValidateWorldPulseBridge.tscn`
- `E:\Medioevo_RPG\tools\campaign\ValidateEcosystemObservationalSlice.tscn`
- `E:\Medioevo_RPG\tools\campaign\ValidateObservacionismoGameplay.tscn`
- `E:\Medioevo_RPG\tools\campaign\ValidateMainPlaytestLayout.tscn`
- `E:\Medioevo_RPG\tools\campaign\ValidateGameFactory.tscn`

No se ejecutaron por frontera privada y pausa de expansion.

## 3. Suites ejecutadas realmente

Ejecuciones reales observadas en esta sesion antes de la pausa final:

| comando exacto | resultado | tiempo observado |
|---|---|---:|
| `python -m py_compile tools\system_observacionista.py tests\test_system_observacionista.py` | pass | 1.3s |
| `python tools\system_observacionista.py --no-write` | pass; inventario no destructivo | 9.1s |
| `python tools\system_observacionista.py --write-host` | pass; escribio evidencia runtime/reporte | 22.1s |
| `python -m pytest tests\test_system_observacionista.py -q` | `5 passed` | 17.0s wall; 1.42s pytest |
| `python -m pytest tests\test_host_observacionista.py tests\test_observacion_action_gate.py tests\test_observacionismo_benchmark_suite.py tests\test_observacionismo_download_intake.py tests\test_observacionismo_promotion_matrix.py tests\test_system_observacionista.py -q` | `28 passed` | 15.2s wall; 5.79s pytest |
| `python tools\run_observacionismo_benchmark_suite.py --quick` | `ok=True`; 6 checks PASS | 35.2s |
| `python -m py_compile tools\system_observacionista.py tests\test_system_observacionista.py` | pass segunda ronda | 1.5s |
| `python -m pytest tests\test_system_observacionista.py tests\test_host_observacionista.py tests\test_observacion_action_gate.py tests\test_observacionismo_benchmark_suite.py tests\test_observacionismo_download_intake.py tests\test_observacionismo_promotion_matrix.py -q` | `28 passed` segunda ronda | 20.4s wall; 8.16s pytest |
| `python tools\run_observacionismo_benchmark_suite.py` | `ok=True`; 6 checks PASS | 44.4s |

Ejecuciones reales de preflight/debug existentes:

| comando exacto | resultado | tiempo observado |
|---|---|---:|
| `python tools\host_observacionista.py --no-write` | `CONTAMINADO/REVIEW`; CPU 47.5%, RAM 74.0%, disco 96.8%, 223 procesos | 1.027s |
| `python tools\setup_claudio_symphony.py --json --require-ready` | exit code 2; `ready_to_launch=false`; razon actual: `missing_linear_or_repo_environment` | 1.845s |
| `python tools\release\run_tests.py --json` | inventario dry-run; no ejecuta suites | 0.179s |
| `python tools\release\run_builds.py --json` | inventario dry-run; no ejecuta suites | 0.179s |
| `Get-ChildItem tests -Filter 'test_*.py'` | 101 tests detectados | 0.128s |
| `python tools\run_observacionismo_benchmark_suite.py --help` | ayuda disponible | 0.198s |
| `rg --files E:\Medioevo_RPG -g 'Validate*.tscn' -g 'validate*.gd' -g 'test_*.gd'` | 46 validadores/tests privados detectados | 0.077s |

Tiempo total medido de comandos de validacion realmente ejecutados en la sesion: aproximadamente 168.7s.

Tiempo total medido de la consolidacion final de inventario/preflight: 3.633s, sin contar cuatro `git status` acotados.

## 4. Suites skipped y razon

| suite / comando | razon |
|---|---|
| `private-metaevo-lint` | requiere `--include-private`; juego/TCG es frontera privada |
| `private-metaevo-build` | requiere `--include-private`; juego/TCG es frontera privada |
| Validadores Godot de `E:\Medioevo_RPG` | no ejecutados por pausa de expansion y frontera privada |
| `python tools\release\run_tests.py --execute --json` | no re-ejecutado en consolidacion por pausa, host/disco y riesgo OneDrive |
| `python tools\release\run_builds.py --execute --json` | no re-ejecutado en consolidacion por pausa; contiene acciones como archivar artifacts de Argus |
| `python tools\release\argus_release_check.py --json` | no re-ejecutado en consolidacion por riesgo OneDrive/dependencias y porque puede reinstalar `node_modules` |
| `tools\run_claudio_symphony.ps1 -AcknowledgePreviewRisk` | prohibido; `ready_to_launch=false` |
| Gemma pesado / daemon / ruta interactiva | no ejecutar hasta host apto y suites minimas verdes |
| Acciones Gumroad/redes/publicacion/mouse | fuera de alcance; requieren ActionGate/host y aprobacion especifica |

## 5. Fallos reales

No hubo fallos reales en las suites pytest/benchmark ejecutadas.

Bloqueos o errores observados:

| comando | resultado | clasificacion |
|---|---|---|
| `python -m pytest tests\test_host_observacionista.py tests\test_host_process_admin.py tests\test_observacion_action_gate.py -q` | error: `tests\test_host_process_admin.py` no existe; `no tests ran` | seleccion invalida de ruta, no fallo de codigo |
| `python tools\setup_claudio_symphony.py --json --require-ready` | exit code 2; `ready_to_launch=false` | bloqueo correcto de preflight |
| busquedas amplias `Get-ChildItem` / `rg` sobre arboles con vendor/pentest | timeouts/truncado | fallo de discovery amplio, no fallo de suite |

Estado Symphony actual: instalado/compilado, pero no operativo en daemon. La activacion sigue congelada hasta que el preflight devuelva `ready_to_launch=true`.

## 6. Riesgos

| riesgo | evidencia | efecto |
|---|---|---|
| Host saturado o cercano a saturacion | `host_observacionista --no-write`: `CONTAMINADO/REVIEW`, disco 96.8%, 223 procesos. Reporte previo `SYSTEM_OBSERVACIONISMO_REPORT.md` registro `JAMMING/BLOCK` durante carga alta. | No activar daemons/modelos pesados. Repetir host gate antes de ejecutar suites largas. |
| Disco C: casi lleno | disco 96.8% | npm/Godot/build caches pueden fallar o dejar installs parciales. |
| OneDrive | Argus y workspace viven bajo OneDrive | `npm ci` puede fallar parcialmente o dejar `node_modules/.bin` incompleto. Verificar `tsc`, `vite`, `workbox-build`, `caniuse-lite`. |
| Dependencias npm | Argus requiere install real y binarios dev | No confiar solo en dry-run. Usar `argus_release_check.py` cuando se permita ejecucion. |
| Multi-root y otros agentes | cambios tracked en `-=LIBROS` y `claudio` no atribuibles a esta consolidacion | No broad-stage, no revert, no commits monoliticos. |
| Private game boundary | `E:\Medioevo_RPG` y TCG privados | No mezclar con MIT/open tooling ni runners publicos. |
| Symphony preview | falta entorno Linear/repo; preflight actual `ready_to_launch=false` | No arrancar con `-AcknowledgePreviewRisk`. |

## 7. Suite minima antes de activar Symphony o Gemma

### 7.1 Antes de activar Symphony

Minimo obligatorio:

```powershell
cd C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\claudio
python tools\host_observacionista.py --no-write
python tools\setup_claudio_symphony.py --json --require-ready
```

Condicion de salida:

- `ready_to_launch=true`
- sin `missing_linear_or_repo_environment`
- host no debe estar `JAMMING/BLOCK`
- no usar `-AcknowledgePreviewRisk` antes de esa condicion

Smoke recomendado sin daemon:

```powershell
python -m pytest tests\test_host_observacionista.py tests\test_observacion_action_gate.py -q
```

### 7.2 Antes de activar Gemma pesado

Minimo obligatorio:

```powershell
cd C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\claudio
python tools\host_observacionista.py --no-write
python -m pytest tests\test_gemma4_benchmark_guard.py tests\test_gemma4_model_lifecycle.py tests\test_gemma4_observacion_contract.py tests\test_gemma4_observacion_gate_report.py tests\test_model_router.py -q
```

Condicion de salida:

- host no debe estar `JAMMING/BLOCK`
- contrato/gate/model-router verde
- no usar Gemma como ruta interactiva permanente si la latencia/host no pasan gate observado

## 8. Cierre

Estado de testing: las suites observacionistas ejecutadas pasaron en dos rondas. No hay fallo real de test pendiente en esta consolidacion. Los bloqueos actuales son operativos: credenciales/entorno para Symphony, host/disco, OneDrive/dependencias y fronteras privadas.

## 9. Cierre operativo Wave Collapse primero

Actualizacion local: 2026-04-29.

Se localizo este reporte final en dos ubicaciones activas:

- `TESTING_DEBUG_BENCHMARKS_FINAL.md`
- `-=MEDIOEVO=-\-=LIBROS\claudio\TESTING_DEBUG_BENCHMARKS_FINAL.md`

Verificaciones no destructivas ejecutadas para cerrar la evidencia faltante del
lockfile:

| comando | resultado | lectura |
|---|---|---|
| `python tools\release\run_tests.py --json` | 11 suites inventariadas; `private-metaevo-lint` skipped por frontera privada | inventario dry-run, sin ejecutar suites largas |
| `python tools\release\run_builds.py --json` | 10 suites/builds inventariados; `private-metaevo-build` skipped por frontera privada | inventario dry-run, sin archivar ni empaquetar |
| `python -m pytest tests\test_claudio_harness_skills.py tests\test_observacion_action_gate.py tests\test_host_observacionista.py -q` | `16 passed in 0.58s` | suite minima local verde |
| `python tools\setup_claudio_symphony.py --json --require-ready` | exit code `1`; `ok=true`, `ready_to_launch=false`, bloqueo `missing_linear_or_repo_environment`, host `CONTAMINADO/REVIEW` | bloqueo correcto; no autoriza daemon |

Decision: el testing minimo queda cerrado para avanzar a MVP 0 manual/read-only
de Wave Collapse. No queda autorizado ejecutar Gemma pesado, Symphony daemon,
`wide`, publicacion, Gumroad, redes, mouse, movimientos amplios ni acciones
externas automaticas.
