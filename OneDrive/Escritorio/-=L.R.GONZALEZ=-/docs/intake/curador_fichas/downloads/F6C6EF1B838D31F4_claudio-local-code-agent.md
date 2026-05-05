# Ficha Curador SETO - # CLAUDIO — LOCAL CODE AGENT.txt

| campo | valor |
|---|---|
| Ruta original | `C:\Users\L-Tyr\Downloads\# CLAUDIO — LOCAL CODE AGENT.txt` |
| SHA256 | `F6C6EF1B838D31F4E01C1DFB2A805849DF479D29B6E5200F01A15A74544A3F3D` |
| Bytes | `25753` |
| Tipo | `file` |
| Estado PSI | `INFERENCIA` |
| Status | `ARCHIVO_FRIO` |
| Clasificacion | `CODE_PROTOTYPE_REVIEW` |
| Lane | `local-agent` |
| Decision | `ABSORBIDO_CANONIZADO_ARCHIVO_FRIO` |
| ActionGate | `REVIEW` |
| Canonico | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\runtime\curador_seto\source_archive\downloads\2026-05-05\F6C6EF1B838D31F4_claudio-local-code-agent.txt` |
| Atlas | `Claudio / Wabi-Sabi` |

## Resumen

Code prototype; no execution or import until dependencies and side effects are reviewed.

## Sinapsis

- Destino: `Claudio local-agent backlog and COMMS contracts`.
- Evidencia: SHA256 `F6C6EF1B838D31F4E01C1DFB2A805849DF479D29B6E5200F01A15A74544A3F3D`.
- Uso permitido: local, curado, sin publicacion externa directa.

## Falsadores

- secret/private marker, hash mismatch, unique content loss, strong claim without validation.
- Si aparece secreto, ruta privada o claim fuerte no validado, el estado cambia a `BLOQUEADO`.
