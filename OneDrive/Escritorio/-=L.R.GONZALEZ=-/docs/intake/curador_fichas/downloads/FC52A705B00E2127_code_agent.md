# Ficha Curador SETO - CODE_AGENT.md

| campo | valor |
|---|---|
| Ruta original | `C:\Users\L-Tyr\Downloads\CODE_AGENT.md` |
| SHA256 | `FC52A705B00E2127D6978BE3C2DE50E87092C8A145D74B2366C6D5931478855C` |
| Bytes | `3544` |
| Tipo | `file` |
| Estado PSI | `INFERENCIA` |
| Status | `ARCHIVO_FRIO` |
| Clasificacion | `CODE_PROTOTYPE_REVIEW` |
| Lane | `local-agent` |
| Decision | `ABSORBIDO_CANONIZADO_ARCHIVO_FRIO` |
| ActionGate | `REVIEW` |
| Canonico | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\runtime\curador_seto\source_archive\downloads\2026-05-05\FC52A705B00E2127_code_agent.md` |
| Atlas | `Claudio / Wabi-Sabi` |

## Resumen

Code prototype; no execution or import until dependencies and side effects are reviewed.

## Sinapsis

- Destino: `Claudio local-agent backlog and COMMS contracts`.
- Evidencia: SHA256 `FC52A705B00E2127D6978BE3C2DE50E87092C8A145D74B2366C6D5931478855C`.
- Uso permitido: local, curado, sin publicacion externa directa.

## Falsadores

- secret/private marker, hash mismatch, unique content loss, strong claim without validation.
- Si aparece secreto, ruta privada o claim fuerte no validado, el estado cambia a `BLOQUEADO`.
