# Curador SETO Next Actions

Pending source: `qa_artifacts/pending/pending_review_latest.json`

Estado operativo para decidir el siguiente loop sin reescanear todo el sistema.

## Downloads

| metric | value |
|---|---:|
| archivos vivos actuales | 0 |
| duplicados exactos activos | 0 |
| witness_event_hash | `1d8e2806f209fb51abf8ad8da094fd050c1a20726454086306c1244131bc54d7` |

## SQLite

| table | rows |
|---|---:|
| `atlas_synapses` | 1 |
| `canon_nodes` | 9 |
| `decisions` | 509 |
| `duplicate_groups` | 0 |
| `duplicates` | 18 |
| `extractions` | 1 |
| `fichas` | 186 |
| `files` | 186 |
| `retirements` | 1 |
| `synapses` | 1 |
| `witness_events` | 10 |

## Status historico

| status | rows |
|---|---:|
| `ARCHIVO_FRIO` | 167 |
| `BASURA_REGENERABLE_BORRADA` | 1 |
| `BORRADO_DUPLICADO` | 18 |

## Pendientes

| blocker | dedup_count |
|---|---:|
| `external_or_gated` | 263 |
| `host_or_heavy` | 52 |
| `legal_or_human` | 64 |
| `private_boundary` | 10 |

## Cola recomendada

| priority | lane | gate | title | next step |
|---|---|---|---|---|
| `P0` | `curador_seto` | `APPROVE_LOCAL` | Mantener CuradorSETO-Downloads-Intake activo | Usar el SQLite y CURADOR_MASTER_INDEX como verdad operativa de Downloads. |
| `P1` | `pending_review` | `REVIEW` | No forzar pendientes gated como locales | Convertir pendientes gated en subtareas locales solo cuando haya evidencia y frontera clara. |
| `P1` | `global_curador` | `REVIEW` | Reemplazar escaneo global largo por auditoria incremental por root | Agregar modo por root/resumible antes de repetir E:, Desktop y workspace completo. |
| `P1` | `cleanup_migration` | `REVIEW` | Consolidar duplicados grandes solo con hash, ficha y canon | Procesar por lote: Asistente/FlujoCRM releases, vendors/cache, luego E: offload; borrar solo si ActionGate aprueba. |
| `P2` | `claudio_wabisabi` | `REVIEW` | Conectar Curador SETO con Claudio/Wabi-Sabi como memoria operativa | Exponer lectura local del SQLite y del reporte de next-actions sin ejecutar mutaciones externas. |

## Bloqueos

- No publicar, hacer push, deploy, Gumroad, LinkedIn o Sponsors desde esta cola.
- No borrar o mover material unico, privado, RPG/TCG, sesiones, secretos o claims fuertes.
- No repetir el escaneo global completo si puede sustituirse por modo incremental por root.
