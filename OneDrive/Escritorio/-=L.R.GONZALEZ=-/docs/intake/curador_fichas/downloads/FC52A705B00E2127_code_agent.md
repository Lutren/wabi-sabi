# Ficha Curador SETO - CODE_AGENT.md

| campo | valor |
|---|---|
| Ruta original | `C:\Users\L-Tyr\Downloads\CODE_AGENT.md` |
| SHA256 | `FC52A705B00E2127D6978BE3C2DE50E87092C8A145D74B2366C6D5931478855C` |
| Bytes | `3544` |
| Tipo | `file` |
| Estado PSI | `CERTEZA` |
| Status | `REGISTRADO` |
| Clasificacion | `CODE_PROTOTYPE_REVIEW` |
| Lane | `local-agent` |
| Decision | `READ_REVIEW_TEST_BEFORE_IMPORT` |
| ActionGate | `REVIEW` |
| Canonico | `C:\Users\L-Tyr\Downloads\CODE_AGENT.md` |

## Resumen

Code prototype; no execution or import until dependencies and side effects are reviewed.

## Sinapsis

- Destino: `Claudio local-agent backlog and COMMS contracts`.
- Evidencia: SHA256 `FC52A705B00E2127D6978BE3C2DE50E87092C8A145D74B2366C6D5931478855C`.
- Uso permitido: local, curado, sin publicacion externa directa.

## Falsadores

- secret/private marker, hash mismatch, unique content loss, strong claim without validation.
- Si aparece secreto, ruta privada o claim fuerte no validado, el estado cambia a `BLOQUEADO`.
