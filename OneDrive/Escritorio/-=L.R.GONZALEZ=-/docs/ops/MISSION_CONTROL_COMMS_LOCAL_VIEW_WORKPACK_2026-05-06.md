# Mission Control / COMMS Local View Workpack - 2026-05-06

## ESTADO

- Prompt cubierto: `7. Claudio Mission Control / COMMS`.
- Gate: `REVIEW`.
- Host: `JAMMING/BLOCK`.
- Ejecucion permitida: documentacion, lectura local, JSON/COMMS append-only.
- Ejecucion bloqueada: daemon, browser externo, deploy, publicacion.

## OBJETIVO LOCAL

Crear una vista local clara de:

- agente;
- departamento;
- estado;
- gate;
- ultimo artefacto;
- pendientes;
- riesgo;
- solapamientos.

## FUENTES

- `COMMS/agents_state/*.json`
- `COMMS/topics/agent-city-coordination.jsonl`
- `docs/ops/AGENT_CITY_LIVE_MAP_2026-05-06.md`
- `qa_artifacts/pending/pending_review_latest.json`
- `COMMS/tools/validate_seto_comms.py`

## CONTRATO DE VISTA

| campo | origen | certeza |
|---|---|---|
| `agent_id` | `COMMS/agents_state/*.json` | `CERTEZA` |
| `department_slug` | `COMMS/agents_state/*.json` o `department.id` | `CERTEZA/INFERENCIA` |
| `status` | `COMMS/agents_state/*.json` | `CERTEZA` |
| `action_gate` | `COMMS/agents_state/*.json` | `CERTEZA` |
| `owns` | `COMMS/agents_state/*.json` | `CERTEZA` |
| `may_touch` | `COMMS/agents_state/*.json` | `CERTEZA` |
| `must_not_touch` | `COMMS/agents_state/*.json` | `CERTEZA` |
| `latest_artifact` | `current_handoff/current_outbox/last_observation_fingerprint` | `CERTEZA` |
| `risk` | gate + must_not_touch + host gate | `INFERENCIA` |

## ACCION SEGURA

1. No crear nueva capa si Mission Control ya puede leer COMMS.
2. Generar primero reporte local.
3. Solo despues, si se edita UI/API, hacerlo en archivos de `hormiguero-mission-control` y tests propios.
4. Cada extension debe mantener COMMS como fuente unica.

## NO EJECUTAR

- Servidor permanente.
- Navegacion externa.
- Publicacion.
- Escritura en streams de otros agentes.
- Acciones de cleanup.

## HANDOFF

Siguiente artefacto de codigo permitido cuando el host baje de `BLOCK`: un endpoint o vista que lea este workpack y `COMMS/agents_state` sin mutar nada.
