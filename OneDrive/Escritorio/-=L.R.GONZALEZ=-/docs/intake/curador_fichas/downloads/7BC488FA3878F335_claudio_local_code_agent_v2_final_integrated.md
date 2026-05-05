# Ficha Curador SETO - claudio_local_code_agent_v2_final_integrated.py

| campo | valor |
|---|---|
| Ruta original | `C:\Users\L-Tyr\Downloads\claudio_local_code_agent_v2_final_integrated.py` |
| SHA256 | `7BC488FA3878F33597E2444BE24A4EA1A20780992DF8DD1AD8F7CF8FFF4484F2` |
| Bytes | `143266` |
| Tipo | `file` |
| Estado PSI | `CERTEZA` |
| Status | `REGISTRADO` |
| Clasificacion | `CODE_PROTOTYPE_REVIEW` |
| Lane | `local-agent` |
| Decision | `READ_REVIEW_TEST_BEFORE_IMPORT` |
| ActionGate | `REVIEW` |
| Canonico | `C:\Users\L-Tyr\Downloads\claudio_local_code_agent_v2_final_integrated.py` |

## Resumen

Code prototype; no execution or import until dependencies and side effects are reviewed.

## Sinapsis

- Destino: `Claudio local-agent backlog and COMMS contracts`.
- Evidencia: SHA256 `7BC488FA3878F33597E2444BE24A4EA1A20780992DF8DD1AD8F7CF8FFF4484F2`.
- Uso permitido: local, curado, sin publicacion externa directa.

## Falsadores

- secret/private marker, hash mismatch, unique content loss, strong claim without validation.
- Si aparece secreto, ruta privada o claim fuerte no validado, el estado cambia a `BLOQUEADO`.
