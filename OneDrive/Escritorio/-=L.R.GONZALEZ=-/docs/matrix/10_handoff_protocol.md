# Matrix Handoff Protocol

Estado: `HANDOFF_PROTOCOL / COMMS_READY`.

## Handoff minimo

```json
{
  "fingerprint": "MATRIX_ALEJANDRIA_WABISABI_2026-05-06_<hash>",
  "sender": "wabisabi",
  "receiver": "department_head",
  "modules": ["observacionismo_core"],
  "goal": "reducir R y producir artefacto verificable",
  "evidence": ["library/index.json", "COMMS/schemas/action-gate.schema.json"],
  "gate": "REVIEW",
  "blocked_actions": ["publish", "delete", "train_weights"],
  "expected_return": ["artifacts", "tests", "residual_R", "handoff"]
}
```

## Campos obligatorios

- fingerprint;
- sender;
- receiver;
- task;
- selected modules;
- evidence;
- gate;
- blocked actions;
- tests;
- residual R;
- next safe action.

## WitnessLog

El handoff no reescribe decisiones anteriores. Se agrega como evento append-only
cuando exista integracion COMMS activa. Si no hay integracion, el handoff queda
como documento local.

## Fingerprint de esta entrega

`MATRIX_ALEJANDRIA_WABISABI_2026-05-06_317BE610`
