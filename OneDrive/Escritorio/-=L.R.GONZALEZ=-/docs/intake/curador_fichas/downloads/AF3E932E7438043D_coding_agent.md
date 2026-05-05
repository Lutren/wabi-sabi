# Ficha Curador SETO - coding_agent.py

| campo | valor |
|---|---|
| Ruta original | `C:\Users\L-Tyr\Downloads\coding_agent.py` |
| SHA256 | `AF3E932E7438043D8F14680C0FF997E2AA407A7B350B0D59619A04C318123979` |
| Bytes | `42341` |
| Tipo | `file` |
| Estado PSI | `CERTEZA` |
| Status | `REGISTRADO` |
| Clasificacion | `CODE_PROTOTYPE_REVIEW` |
| Lane | `local-agent` |
| Decision | `READ_REVIEW_TEST_BEFORE_IMPORT` |
| ActionGate | `REVIEW` |
| Canonico | `C:\Users\L-Tyr\Downloads\coding_agent.py` |

## Resumen

Code prototype; no execution or import until dependencies and side effects are reviewed.

## Sinapsis

- Destino: `Claudio local-agent backlog and COMMS contracts`.
- Evidencia: SHA256 `AF3E932E7438043D8F14680C0FF997E2AA407A7B350B0D59619A04C318123979`.
- Uso permitido: local, curado, sin publicacion externa directa.

## Falsadores

- secret/private marker, hash mismatch, unique content loss, strong claim without validation.
- Si aparece secreto, ruta privada o claim fuerte no validado, el estado cambia a `BLOQUEADO`.
