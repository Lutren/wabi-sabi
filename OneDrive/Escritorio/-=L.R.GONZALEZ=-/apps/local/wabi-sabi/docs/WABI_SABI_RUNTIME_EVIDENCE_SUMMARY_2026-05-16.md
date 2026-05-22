# WABI_SABI_RUNTIME_EVIDENCE_SUMMARY 2026-05-16

## Decision

`runtime/` es evidencia local ignorada, no basura directa. Se mantiene fuera de
Git y no se borra sin ActionGate especifico.

## Inventario

Ruta: `apps/local/wabi-sabi/runtime`

Total inventariado: 194 archivos, 913448 bytes.

| bucket | files | bytes | accion |
|---|---:|---:|---|
| `debug` | 8 | 17072 | KEEP_LOCAL_EVIDENCE |
| `decision_log` | 3 | 17552 | KEEP_LOCAL_EVIDENCE |
| `executions` | 2 | 5308 | KEEP_LOCAL_EVIDENCE |
| `jobs` | 51 | 72887 | KEEP_LOCAL_EVIDENCE |
| `logs` | 1 | 83359 | KEEP_LOCAL_EVIDENCE |
| `memory` | 1 | 41190 | KEEP_LOCAL_EVIDENCE |
| `outputs` | 124 | 629884 | KEEP_LOCAL_EVIDENCE |
| `rollback` | 2 | 5236 | KEEP_LOCAL_EVIDENCE |
| `wabi_osit_bridge.sqlite` | 1 | 12288 | KEEP_LOCAL_DB |
| `witness` | 1 | 28672 | KEEP_LOCAL_DB |

## Tipos

| extension | files | bytes | lectura |
|---|---:|---:|---|
| `.json` | 93 | 632263 | outputs, plans, workpacks, snapshots |
| `.md` | 38 | 79705 | reports/responses local-only |
| `.log` | 34 | 0 | job stdout/stderr empty; review-only |
| `.py` | 12 | 6652 | generated/test snippets; review before use |
| `.diff` | 11 | 13622 | patch evidence |
| `.jsonl` | 3 | 127958 | event/memory/decision streams |
| `.sqlite` | 3 | 53248 | witness/bridge/decision local DBs |

## SQLite Hashes

| path | bytes | sha256 |
|---|---:|---|
| `runtime/wabi_osit_bridge.sqlite` | 12288 | `4D69C56A1C8A74D5C34E8E31F2093E6575BE3FB13B268198907461C8B82CFA5D` |
| `runtime/decision_log/wabi_decision_witness.sqlite` | 12288 | `7F63078FE94731407971E26546FAC4977554CA9E9D3A39B96D50E9759CAAF4B0` |
| `runtime/witness/wabi_patch_witness.sqlite` | 28672 | `CA5BE3758DBFDA862DCC4598493922A684A7744C6B1510CA1105B732209D74C6` |

## Sensitive-Name Triage

No se imprimio contenido. La busqueda por nombre/ruta sensible encontro solo:

- `runtime/outputs/wabi_environment_snapshot_20260506-104839.json`
- `runtime/outputs/wabi_environment_snapshot_20260506-104933.json`
- `runtime/outputs/wabi_environment_snapshot_20260506-122649.json`

Lectura: `REVIEW_LOCAL_ONLY`. Pueden contener nombres/estado de entorno; no se
incluyen en releases ni se imprimen.

## Evidencia Reciente

Ultimos outputs relevantes:

- `runtime/outputs/safe_test_run_20260516-160054.json`
- `runtime/outputs/safe_test_run_20260516-155314.json`
- `runtime/outputs/engine_plans/local_only_no_publicar_crear_wabi_sabi_observatorio_sandbox_app_ENGINE_PLAN.json`
- `runtime/outputs/engine_task_specs/local_only_no_publicar_crear_wabi_sabi_observatorio_sandbox_app_TASK_SPEC.json`
- patch plans/diffs `20260516-*`

## No Tocar Sin Gate

- SQLite witness/decision/bridge DBs.
- JSONL memory/log streams.
- Environment snapshots.
- Patch plans/diffs y rollback files.
- Job JSON files.

## Review Candidates

- `runtime/jobs/*.stdout.log` y `runtime/jobs/*.stderr.log`: 34 archivos,
  0 bytes. Se conservan por ahora porque estan acoplados a jobs; una limpieza
  futura puede moverlos a manifest `APPROVE_DELETE_ZERO_BYTE_JOB_LOG` si se
  valida que el job JSON conserva toda la evidencia necesaria.

## Manifest De Logs De Job

Se genero `docs/WABI_SABI_ZERO_BYTE_JOB_LOG_MANIFEST_2026-05-16.md`.

Resultado: 34/34 logs pesan 0 bytes, 17/17 JSON asociados existen y 17/17
parsean como JSON. No se imprimio contenido de jobs y no se borro ningun
archivo. La decision queda `REVIEW_READY_DELETE_ZERO_BYTE_LOGS`.

## Resultado

`runtime/` queda resumido y preservado. La limpieza visible ya se logro con
`.gitignore`; el contenido sigue disponible localmente para auditoria y
witness.
