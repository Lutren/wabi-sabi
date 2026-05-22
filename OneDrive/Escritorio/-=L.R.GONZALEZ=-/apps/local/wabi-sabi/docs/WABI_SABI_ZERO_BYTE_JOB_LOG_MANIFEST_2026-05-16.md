# WABI_SABI_ZERO_BYTE_JOB_LOG_MANIFEST 2026-05-16

## Decision

Los logs `runtime/jobs/*.stdout.log` y `runtime/jobs/*.stderr.log` pesan 0
bytes y cada par tiene un JSON de job valido. Aun asi no se borran en esta
pasada porque siguen siendo parte del runtime evidence ignorado y no recuperan
espacio en disco. Quedan como `REVIEW_READY_DELETE_ZERO_BYTE_LOGS`.

## Resultado

- Logs revisados: 34.
- Logs con 0 bytes: 34.
- Jobs JSON asociados: 17.
- Jobs JSON existentes: 17.
- Jobs JSON parseables: 17.
- Bytes recuperables si se borran: 0.
- Accion ejecutada: ninguna eliminacion.

## Manifest

| job_id | json_bytes | stdout_log | stderr_log | json_valid | action_gate |
|---|---:|---:|---:|---|---|
| `20260506-084323-8b830bc7` | 2754 | 0 | 0 | true | REVIEW_READY_DELETE_ZERO_BYTE_LOGS |
| `20260506-084355-1be93cf9` | 2775 | 0 | 0 | true | REVIEW_READY_DELETE_ZERO_BYTE_LOGS |
| `20260506-084532-9247fbef` | 2754 | 0 | 0 | true | REVIEW_READY_DELETE_ZERO_BYTE_LOGS |
| `20260506-084604-06ab4a2a` | 2775 | 0 | 0 | true | REVIEW_READY_DELETE_ZERO_BYTE_LOGS |
| `20260506-084924-a225d008` | 3204 | 0 | 0 | true | REVIEW_READY_DELETE_ZERO_BYTE_LOGS |
| `20260506-085610-f4c49386` | 1298 | 0 | 0 | true | REVIEW_READY_DELETE_ZERO_BYTE_LOGS |
| `20260506-085901-f483af81` | 3976 | 0 | 0 | true | REVIEW_READY_DELETE_ZERO_BYTE_LOGS |
| `20260506-090358-ebaf7369` | 1077 | 0 | 0 | true | REVIEW_READY_DELETE_ZERO_BYTE_LOGS |
| `20260506-090643-b913e766` | 3964 | 0 | 0 | true | REVIEW_READY_DELETE_ZERO_BYTE_LOGS |
| `20260506-090700-8816c774` | 4403 | 0 | 0 | true | REVIEW_READY_DELETE_ZERO_BYTE_LOGS |
| `20260506-091339-dc602c93` | 3778 | 0 | 0 | true | REVIEW_READY_DELETE_ZERO_BYTE_LOGS |
| `20260506-091613-38996216` | 3678 | 0 | 0 | true | REVIEW_READY_DELETE_ZERO_BYTE_LOGS |
| `20260506-092153-43d3619e` | 7030 | 0 | 0 | true | REVIEW_READY_DELETE_ZERO_BYTE_LOGS |
| `20260506-100445-e614fbee` | 6185 | 0 | 0 | true | REVIEW_READY_DELETE_ZERO_BYTE_LOGS |
| `20260506-102047-92448110` | 7099 | 0 | 0 | true | REVIEW_READY_DELETE_ZERO_BYTE_LOGS |
| `20260506-102424-10c06120` | 7100 | 0 | 0 | true | REVIEW_READY_DELETE_ZERO_BYTE_LOGS |
| `20260507-143702-a8666ee9` | 9037 | 0 | 0 | true | REVIEW_READY_DELETE_ZERO_BYTE_LOGS |

## Justificacion

Cada JSON asociado contiene metadatos estructurados del job. No se imprimio ni
copio contenido de prompts, outputs ni errores. La validacion fue de existencia,
tamanio y parseo JSON.

## Gate

`APPROVE`: crear manifest, validar pares y registrar evidencia.

`REVIEW`: borrar los 34 logs vacios. Aunque son cero bytes, siguen siendo
archivos de runtime. La eliminacion no mejora espacio y debe esperar decision
explicita de limpieza final por runtime.

`BLOCK`: borrar JSON de jobs, SQLite, JSONL, snapshots de entorno, patch plans,
rollback o outputs.
