# Puente Observacionismo COMMS L1 ActionGate v0.1

Fecha: 2026-05-06

Estado: `CANON_OPERATIVO_INTERNO / LOCAL_ONLY / NO_PUBLIC_CLAIMS`

Este puente convierte cada concepto validado de
`data/observacionismo/concepts_seed.jsonl` en tres objetos operativos:

- `ObservationEnvelope` compatible con COMMS.
- Plan L1 de cinco verbos.
- Payload ActionGate conservador.

No publica claims. No ejecuta acciones externas. No borra ni mueve archivos. No
convierte hipotesis en verdad tecnica.

## 1. Fuente Canonica

La fuente de verdad sigue siendo:

- schema: `schemas/observacionismo_concepts.schema.json`
- dataset: `data/observacionismo/concepts_seed.jsonl`
- validador: `tools/observacionismo/validate_concepts.py`

El puente usa esos artefactos como entrada y falla si el dataset no valida.

## 2. COMMS

Cada concepto produce un `ObservationEnvelope` con:

- `source_kind=generated_artifact`
- `source_path=data/observacionismo/concepts_seed.jsonl`
- evidencia derivada de `source_paths`, `tests` y `evidence_required`
- `falsifiers` copiados del concepto
- `risk_flags` que preservan `local_only`, `no_public_claim` y fronteras privadas
- `action_gate` derivado del estado epistemico

Regla: el envelope transporta evidencia y estado local. No autoriza publicacion.

## 3. L1

Cada concepto baja a un plan L1 seguro:

```text
OBSERVAR bit 0
DOCUMENTAR bit 0
VERIFICAR halted == true
ACTUAR nop
HANDOFF
```

El mapeo semantico es:

| Verbo | Campo canonico |
|---|---|
| `OBSERVAR` | `inputs` + `source_paths` |
| `DOCUMENTAR` | `outputs` + `evidence_required` |
| `VERIFICAR` | `falsifiers` + `tests` |
| `ACTUAR` | `gates` por ActionGate |
| `HANDOFF` | `ObservationEnvelope` + WitnessLog |

`ACTUAR` queda como `nop` hasta que exista una accion concreta y ActionGate la
apruebe. Hipotesis y metaforas quedan en `review_only`.

## 4. ActionGate

El payload ActionGate conserva estas restricciones:

- `no_external_action=true`
- `no_delete=true`
- `no_move=true`
- `no_write_to_concurrent_lane=true`
- `requires_hash_refresh_before_future_action=true`

Reglas de decision:

- `verificado_por_prueba` con tests puede ser `APPROVE` solo para puente local.
- `proxy_operacional` queda en `REVIEW` salvo contrato ya verificado.
- `hipotesis` y `metafora_canon` quedan en `REVIEW`.
- claim publico sin evidencia verificada queda en `BLOCK`.
- rutas privadas con claim publico quedan en `BLOCK`.

## 5. Reportes

El puente genera:

- JSON: `qa_artifacts/observacionismo/bridge_concepts_report.json`
- Markdown: `qa_artifacts/observacionismo/bridge_concepts_report.md`

Opcionalmente puede emitir eventos append-only:

- COMMS topic: `COMMS/topics/seto-observacionismo-decisions.jsonl`
- WitnessLog: `qa_artifacts/witness_log/curador_seto_witnesslog.jsonl`

El evento WitnessLog no corrige historia mediante edicion. Solo agrega una cola
valida con `action_gate=REVIEW` o `BLOCK`.

## 6. Uso

Validar canon base:

```powershell
python tools/observacionismo/validate_concepts.py
```

Generar puente y reportes:

```powershell
python tools/observacionismo/bridge_concepts.py
```

Generar reportes y registrar evidencia local append-only:

```powershell
python tools/observacionismo/bridge_concepts.py --write-comms-topic --append-witness-event
```

Validar pruebas del puente:

```powershell
python -m pytest tests/test_observacionismo_bridge.py -q
```

## 7. Frontera De Claim

Este puente permite uso tecnico local verificable. No permite decir que los
conceptos matematicos sean ciencia validada, ley fisica, diagnostico, prediccion
o prueba publica.

Toda salida publica futura requiere:

- `public_claim_allowed=true`
- `status=verificado_por_prueba`
- dos fuentes minimo
- al menos un test
- sin rutas privadas
- ActionGate especifico
- copy publico de bajo claim
