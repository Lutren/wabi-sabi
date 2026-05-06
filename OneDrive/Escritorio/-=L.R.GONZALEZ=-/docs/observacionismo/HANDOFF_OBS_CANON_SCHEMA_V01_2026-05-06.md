# HANDOFF OBS Canon Schema v0.1

Fingerprint: `OBS_CANON_SCHEMA_V01_2026-05-06_139FDDC7`

Estado: `VALIDATED_LOCAL_CANON_SEED / NO_PUBLIC_CLAIMS`

## Brief

El canon operativo de Observacionismo v0.1 quedo materializado en schema,
dataset semilla, validador, tests y reporte de validacion. El objetivo de esta
fase fue convertir teoria/documentos en objetos verificables sin publicar claims
ni mezclar CEREBRO privado con open-dev publico.

## Evidencia

- Schema: `schemas/observacionismo_concepts.schema.json`
- Dataset: `data/observacionismo/concepts_seed.jsonl`
- Validador: `tools/observacionismo/validate_concepts.py`
- Documento humano: `docs/observacionismo/OPERATIONAL_CANON_V0_1.md`
- Tests: `tests/test_observacionismo_concepts.py`
- Reporte JSON: `qa_artifacts/observacionismo/validate_concepts_report.json`
- Reporte Markdown: `qa_artifacts/observacionismo/validate_concepts_report.md`

## Resultado Validado

- Conceptos validados: `21`
- Errores: `0`
- Warnings: `1`
- Claims publicos permitidos: `0`

Warning esperado:

- `worldpulse` cita frontera privada; debe mantenerse con
  `public_claim_allowed=false`.

## Conceptos Semilla

`R`, `Phi_eff`, `J_c`, `Sigma`, `ObservationEnvelope`, `ActionGate`,
`GhostGate`, `WitnessLog`, `COMMS`, `ObservaBit`, `L0`, `L1`, `L2`, `SleepGC`,
`RegimeAutomaton`, `HandoffSnapshot`, `DUAT`, `WorldPulse`, `source_registry`,
`falsifier`, `Wabi-Sabi Control Node`.

## Validacion Ejecutada

```powershell
python tools\observacionismo\validate_concepts.py
python -m pytest tests\test_observacionismo_concepts.py -q
python -m py_compile tools\observacionismo\validate_concepts.py
```

Resultados:

- `validate_concepts.py`: `ok=true`, `concept_count=21`, `errors=[]`.
- `pytest`: `4 passed`.
- `py_compile`: sin errores.

## Proximo Paso

Conectar schema con:

1. COMMS: emitir `ObservationEnvelope` desde conceptos canonicos.
2. Lenguaje L1: bajar conceptos a `observar/documentar/verificar/actuar/handoff`.
3. ActionGate: bloquear cualquier claim o accion que no tenga evidencia,
   falsador y gate compatible.

No avanzar a claims publicos hasta que exista gate especifico, tests y claim
scan limpio por target.
