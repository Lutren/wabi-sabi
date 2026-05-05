# DUAT / GEODIA Integration Backlog - 2026-05-02

Estado: `BACKLOG_ACCIONABLE / CLAIMS_GATED`.

Este backlog aterriza el intake DUAT/GEODIA en tareas implementables. No autoriza
Gumroad, push ni deploy. DUAT Geodia queda privado; DUAT Genesis es el carril
publico sintetico.

## Cola por carril

| id | carril | accion | destino | validacion | estado |
|---|---|---|---|---|---|
| DG-001 | intake | registrar fuentes, hashes, lineas, ZIPs y pruebas temporales | `docs/intake/DUAT_GEODIA_DOWNLOADS_INTAKE_2026-05-02.md` | rutas, hashes y pytest temporal documentados | `DONE_LOCAL` |
| DG-002 | fichas | separar DUAT, GEODIA, FOR, EML, MCP, OMNIS, MCR y ciudad.matrix | `docs/product/DUAT_GEODIA_TECHNICAL_FICHAS_2026-05-02.md` | cada ficha tiene uso, bloqueo y siguiente accion | `DONE_LOCAL` |
| GEODIA-101 | research runtime | evaluar hand-port de falsadores, EML seguro y source registry desde `duat_geodia_v0_2` | `research/geodia-social-observatory` | tests existentes + nuevos tests sinteticos; sin `.pyc` | `NEXT` |
| GEODIA-102 | research runtime | agregar fixture OMNIS reproducible sin claims reales | `research/geodia-social-observatory/fixtures` | snapshot deterministico + hash | `NEXT` |
| GENESIS-101 | open-dev | crear sandbox publico DUAT Genesis sin ingenieria Geodia privada | `packages/open-dev/duat-genesis` | tests, claims, private exclusions y CLI JSON | `DONE_LOCAL` |
| GENESIS-102 | open-dev | preparar staging/publicacion futura de DUAT Genesis | GitHub sanitized lane | secret scan, path scrub, claims scan y ActionGate | `BLOCKED_BY_GATE` |
| FOR-101 | obs kernel | convertir metricas FOR utiles en modulo experimental | `research/obs-info-kernel` o modulo interno GEODIA | pruebas de finitud, sensibilidad y no-NaN | `REVIEW` |
| EML-101 | obs kernel | definir contrato EML unico: inputs, outputs, rangos, errores y limites | `research/obs-info-kernel` | unit tests + falsadores negativos | `NEXT` |
| MCP-101 | Claudio local | disenar tools DUAT read-only: `status`, `simulate`, `falsify`, `report` | Claudio runtime / MCP gated | ActionGate antes de red/shell/browser/escritura | `BLOCKED_BY_GATE` |
| DG-LC-001 | Claudio/GEODIA core | implementar `LClock` persistente como base causal antes de nuevos agentes | `docs/developer/DUAT_GEODIA_LCLOCK_WITNESSLOG_BACKLOG_2026-05-05.md` | `test_lclock_survives_restart()` | `NEXT_LOCAL` |
| DG-WL-001 | Claudio/GEODIA core | implementar `WitnessLog v2` append-only con hash-chain | `docs/developer/DUAT_GEODIA_LCLOCK_WITNESSLOG_BACKLOG_2026-05-05.md` | alterar entrada vieja debe romper verificacion | `NEXT_LOCAL` |
| DG-ENV-001 | Claudio/GEODIA core | definir `EnvelopeRecord` comun para Evidence, ActionGate y WitnessLog | `docs/developer/DUAT_GEODIA_LCLOCK_WITNESSLOG_BACKLOG_2026-05-05.md` | serializacion canonica + hash reproducible | `NEXT_LOCAL` |
| DG-CR-001 | Claudio/GEODIA research | investigar `Cerebro/Router` sin LLM y sin lookup rigido | `docs/developer/DUAT_GEODIA_LCLOCK_WITNESSLOG_BACKLOG_2026-05-05.md` | falsadores definidos antes de codigo | `BLOCKED_RESEARCH` |
| UI-101 | ciudad de agentes | agregar `Sociometro` y `Laboratorio` como edificios de lab | docs/design + website/app shell | copy sin prediccion ni diagnostico | `NEXT` |
| CLAIM-101 | governance | registrar claims Newton/MCR/EML/social/neuro con prueba minima | `docs/developer/CLAIM_FALSIFICATION_REGISTER_2026-05-02.md` | cada claim tiene estado publico | `DONE_LOCAL` |
| DATA-101 | provenance | crear matriz de fuentes externas sugeridas y licencia/provenance | GEODIA docs/backlog | no fetch de red sin aprobacion | `REVIEW` |
| SENSORIUM-101 | observer audit | extraer contrato `sensorium.audit.v1` para medir dependencia de canal, cobertura, acuerdo entre observadores e invariancia | Claudio local / GEODIA privado | tests sinteticos; no claims reales; bloquear falsos positivos de `hidden_candidate_fraction=1.0` | `NEXT_LOCAL` |
| SENSORIUM-102 | DUAT/GEODIA | mapear canales sociales sinteticos a perfiles de observador antes de colapsar conclusiones | `research/geodia-social-observatory` o ficha privada | replay deterministico + witness log + `label_agreement >= 0.55` antes de aceptar conclusion | `REVIEW` |
| PUB-101 | publicacion | mantener DUAT/GEODIA como lab/piloto hasta scans y legal | website/Gumroad/GitHub | secret scan, path scrub, claims scan y ActionGate | `BLOCK` |

## Reglas de implementacion

- Hand-port selectivo: copiar ideas o funciones revisadas, no carpetas completas.
- Excluir siempre `__pycache__`, `.pyc`, rutas locales, tokens, outputs y texto
  crudo conversacional.
- Si una claim no tiene prueba reproducible, queda `HYPOTHESIS`,
  `RESEARCH_ONLY`, `DEMO_ONLY` o `BLOCK`.
- GEODIA no publica ingenieria. Publicamente solo se describe como carril
  privado low-claim. El codigo publicable vive en DUAT Genesis.
- DUAT Genesis publica solo escenarios sinteticos o low-claim; datos reales
  requieren licencia, snapshot, hash y holdout.
- Claudio puede usar MCP DUAT solo local y con ActionGate visible.

## Primer bloque ejecutable siguiente

1. Crear rama o patch pequeno solo para `research/geodia-social-observatory`.
2. Hand-port un falsador y un operador EML desde los ZIPs, con tests nuevos.
3. Agregar fixture OMNIS sintetico y replay deterministico.
4. Ejecutar `python -m pytest tests -q` en el observatorio.
5. Actualizar las fichas con evidencia real o bajar estados a `REVIEW`.

## Carril publico DUAT Genesis

Ya existe `packages/open-dev/duat-genesis` con:

- `GenesisState`, `GenesisRule`, `Observation`, `Observer`, `SimulationRun`,
  `FalsifierResult`;
- CLI `run`, `report`, `falsify`;
- `CLAIMS.md`, `PRIVATE_EXCLUSIONS.md`, `SECURITY.md`;
- tests locales `3 passed`.

No publicar hasta ejecutar secret scan, path scrub, claims scan y ActionGate.
