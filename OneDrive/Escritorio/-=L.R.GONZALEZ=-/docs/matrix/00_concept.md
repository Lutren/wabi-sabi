# Matrix / Biblioteca De Alejandria

Estado: `CONTRATO_LOCAL / MODULAR / NO_CANON_GIGANTE`.

Matrix es una biblioteca curada para agentes. No es una memoria total, no es un
modelo, no es una base de conocimiento infinita y no reemplaza al usuario. Su
trabajo es guardar modulos pequenos, verificables y combinables para que
Wabi-Sabi cargue solo lo necesario.

## Piezas existentes encontradas

| pieza | ruta | uso |
|---|---|---|
| Wabi-Sabi local | `apps/local/wabi-sabi` | CLI, agentes, gate, memoria y observacion local |
| COMMS | `COMMS` | bus local: inbox, outbox, topics, agents_state, handoffs |
| ObservationEnvelope | `COMMS/schemas/observation-envelope.schema.json` | evidencia y fingerprint |
| ActionGate | `COMMS/schemas/action-gate.schema.json` | aprobar, revisar o bloquear |
| WitnessLog | `COMMS/schemas/witness-log-event.schema.json` | trazabilidad append-only |
| Claudio/Wabi canon | `docs/canon/atlas/claudio-wabisabi.md` | vista atlas |
| Skills harness | `tools/harness/skills` | skills operativas por carril |
| DUAT adapter | `claudio/adapters/duat_readonly_adapter.py` | ejemplo reciente de frontera read-only |
| Observacionismo bridge | `docs/observacionismo/COMMS_L1_ACTIONGATE_BRIDGE_V0_1.md` | DO/IOI a COMMS/ActionGate |

No se encontro una carpeta previa `docs/matrix`, `library` o `tools/matrix`.
Esta entrega crea esa capa minima.

## Principio

La biblioteca guarda herramientas como martillo o rueda: primitivas claras,
estables y recombinables. Cada modulo debe decir para que sirve, que no puede
hacer, que evidencia lo sostiene, como se valida y como se entrega a otro agente.

## Wabi-Sabi

Wabi-Sabi es un `ControlNode / SensoryCognitiveOrchestrator /
TranslationCompiler`. Reduce R, deconstruye el estimulo, recupera modulos,
traduce tareas y compila salidas. No carga todo el canon ni actua sin gates.
