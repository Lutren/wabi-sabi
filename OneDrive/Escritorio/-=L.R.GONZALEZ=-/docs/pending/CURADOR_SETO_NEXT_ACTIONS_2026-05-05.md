# Curador SETO Next Actions

Generated UTC: `2026-05-05T18:55:41.751068+00:00`

Estado operativo para decidir el siguiente loop sin reescanear todo el sistema.

## Downloads

| metric | value |
|---|---:|
| archivos vivos actuales | 160 |
| duplicados exactos activos | 0 |
| witness_event_hash | `07215e235ac0fe8c4c497f06feaee745287ad97ace0c2d493b3a4115a48f007e` |

## SQLite

| table | rows |
|---|---:|
| `decisions` | 337 |
| `duplicate_groups` | 0 |
| `duplicates` | 17 |
| `fichas` | 177 |
| `files` | 177 |
| `synapses` | 160 |
| `witness_events` | 2 |

## Status historico

| status | rows |
|---|---:|
| `BORRADO_DUPLICADO` | 17 |
| `REGISTRADO` | 160 |

## Pendientes

| blocker | dedup_count |
|---|---:|
| `external_or_gated` | 297 |
| `host_or_heavy` | 68 |
| `legal_or_human` | 135 |
| `local_candidate` | 182 |
| `private_boundary` | 103 |

## Cola recomendada

| priority | lane | gate | title | next step |
|---|---|---|---|---|
| `P0` | `curador_seto` | `APPROVE_LOCAL` | Mantener CuradorSETO-Downloads-Intake activo | Usar el SQLite y CURADOR_MASTER_INDEX como verdad operativa de Downloads. |
| `P1` | `pending_review` | `APPROVE_LOCAL` | Trabajar candidatos locales primero | Elegir cierres locales con prueba directa y actualizar trackers, sin publicar ni mover fuentes. |
| `P1` | `global_curador` | `REVIEW` | Reemplazar escaneo global largo por auditoria incremental por root | Agregar modo por root/resumible antes de repetir E:, Desktop y workspace completo. |
| `P1` | `cleanup_migration` | `REVIEW` | Consolidar duplicados grandes solo con hash, ficha y canon | Procesar por lote: Asistente/FlujoCRM releases, vendors/cache, luego E: offload; borrar solo si ActionGate aprueba. |
| `P2` | `claudio_wabisabi` | `REVIEW` | Conectar Curador SETO con Claudio/Wabi-Sabi como memoria operativa | Exponer lectura local del SQLite y del reporte de next-actions sin ejecutar mutaciones externas. |

## Bloqueos

- No publicar, hacer push, deploy, Gumroad, LinkedIn o Sponsors desde esta cola.
- No borrar o mover material unico, privado, RPG/TCG, sesiones, secretos o claims fuertes.
- No repetir el escaneo global completo si puede sustituirse por modo incremental por root.
