# Mission Control COMMS State - 2026-05-06

## Estado

- Prompt cubierto: `7. Claudio Mission Control / COMMS`.
- Resultado: cierre local de evidencia; no se edito codigo.
- Gate actual: `JAMMING/BLOCK` por host observacionista.
- Decision: mantener Mission Control como lector local de COMMS; no arrancar daemon ni navegador.

## Evidencia de implementacion existente

| superficie | evidencia | estado |
|---|---|---|
| API estado COMMS | `-=MEDIOEVO=-/-=LIBROS/claudio/apps/hormiguero_mission_control/app.py:726` | existe |
| API streams COMMS | `-=MEDIOEVO=-/-=LIBROS/claudio/apps/hormiguero_mission_control/app.py:737` | existe |
| lector COMMS | `-=MEDIOEVO=-/-=LIBROS/claudio/core/agent_comms.py:408` | existe |
| UI local | `-=MEDIOEVO=-/-=LIBROS/claudio/apps/hormiguero_mission_control/index.html:2502` | existe |
| tests API | `-=MEDIOEVO=-/-=LIBROS/claudio/tests/test_hormiguero_mission_control_api.py:469` | existe |

## Snapshot COMMS

| stream | archivos | filas |
|---|---:|---:|
| inbox | 2 | 3 |
| outbox | 2 | 43 |
| topics | 2 | 9 |
| handoffs | 3 | 3 |

## Agentes

| agente | departamento | estado | gate | riesgo |
|---|---|---|---|---|
| `claudio-local-agent` | `ayuntamiento` | `ACTIVE_LOCAL_BRIDGE` | `REVIEW` | lectura/escritura local con handoff |
| `claudio-local-autonomy` | `wabi_sabi` | `A0_LOCAL_REVIEW_ONLY` | `BLOCK` | no ejecutar rutas pesadas ni externas |
| `curador-seto` | `curador` | `ACTIVE_LOCAL_CONTRACT` | `REVIEW` | mantener fichas/manifiestos/COMMS append-only |
| `hormiguero-mission-control` | `logi` | `LOCAL_READ_SURFACE` | `REVIEW` | vista local, sin daemon bajo BLOCK |
| `publicacion-perfiles-observatorio` | `plaza-mercado` | `ACTIVE_LOCAL_STRATEGY_AGENT` | `REVIEW` | preparar paquetes, no publicar |
| `wabi-sabi-sentido-comun` | `patterns` | `POLICY_ONLY_LEARNING_SOURCE` | `REVIEW` | policy-only, sin pesos/adapters/aliases |

## Snapshot pending

- `active_markdown.raw_open`: 394.
- `active_markdown.dedup_open`: 389.
- `claudio_master.raw_open`: 69.
- `claudio_master.dedup_open`: 69.
- Bloqueadores dominantes: acciones externas, host/heavy, legal/humano y limite privado.

## Host

- Fuente: `-=MEDIOEVO=-/-=LIBROS/claudio/runtime/host_observacionista/latest_report.json`.
- Timestamp: `2026-05-06T07:54:48Z`.
- Gate: `JAMMING/BLOCK`.
- Accion recomendada por host: `reset_handoff`.
- Razones: `proceso_dominante_cpu`, `residuo_alto`.
- Nota operativa: el proceso dominante es Codex/codex; no se mata automaticamente porque no hay instruccion explicita y el cierre actual sigue en modo lectura/documentacion.

## Decision

Mission Control ya tiene el puente local suficiente para leer COMMS. Bajo host `BLOCK`, la accion correcta es registrar el estado y evitar nuevas capas. La proxima edicion de UI/API solo debe hacerse si el host baja de `BLOCK` y si el requerimiento no queda cubierto por las rutas actuales.
