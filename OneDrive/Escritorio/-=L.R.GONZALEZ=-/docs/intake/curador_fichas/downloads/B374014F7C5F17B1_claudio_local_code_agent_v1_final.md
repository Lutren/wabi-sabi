# Ficha Curador SETO - claudio_local_code_agent_v1_final.txt

| campo | valor |
|---|---|
| Ruta original | `C:\Users\L-Tyr\Downloads\claudio_local_code_agent_v1_final.txt` |
| SHA256 | `B374014F7C5F17B187EDFBC585F27ACEC5888D8C95EA7D97D7E5687E03CAD6A1` |
| Bytes | `90859` |
| Tipo | `file` |
| Estado PSI | `INFERENCIA` |
| Status | `ARCHIVO_FRIO` |
| Clasificacion | `CODE_PROTOTYPE_REVIEW` |
| Lane | `local-agent` |
| Decision | `ABSORBIDO_CANONIZADO_ARCHIVO_FRIO` |
| ActionGate | `REVIEW` |
| Canonico | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\runtime\curador_seto\source_archive\downloads\2026-05-05\B374014F7C5F17B1_claudio_local_code_agent_v1_final.txt` |
| Atlas | `Claudio / Wabi-Sabi` |

## Resumen

Code prototype; no execution or import until dependencies and side effects are reviewed.

## Sinapsis

- Destino: `Claudio local-agent backlog and COMMS contracts`.
- Evidencia: SHA256 `B374014F7C5F17B187EDFBC585F27ACEC5888D8C95EA7D97D7E5687E03CAD6A1`.
- Uso permitido: local, curado, sin publicacion externa directa.

## Falsadores

- secret/private marker, hash mismatch, unique content loss, strong claim without validation.
- Si aparece secreto, ruta privada o claim fuerte no validado, el estado cambia a `BLOQUEADO`.
