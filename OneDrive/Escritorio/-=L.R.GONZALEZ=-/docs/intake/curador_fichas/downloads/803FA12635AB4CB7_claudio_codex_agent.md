# Ficha Curador SETO - claudio_codex_agent.py

| campo | valor |
|---|---|
| Ruta original | `C:\Users\L-Tyr\Downloads\claudio_codex_agent.py` |
| SHA256 | `803FA12635AB4CB747A638E4AB9D553539C450ADDF2AE78C7C3835B3E580B065` |
| Bytes | `12944` |
| Tipo | `file` |
| Estado PSI | `CERTEZA` |
| Status | `REGISTRADO` |
| Clasificacion | `CODE_PROTOTYPE_REVIEW` |
| Lane | `local-agent` |
| Decision | `READ_REVIEW_TEST_BEFORE_IMPORT` |
| ActionGate | `REVIEW` |
| Canonico | `C:\Users\L-Tyr\Downloads\claudio_codex_agent.py` |

## Resumen

Code prototype; no execution or import until dependencies and side effects are reviewed.

## Sinapsis

- Destino: `Claudio local-agent backlog and COMMS contracts`.
- Evidencia: SHA256 `803FA12635AB4CB747A638E4AB9D553539C450ADDF2AE78C7C3835B3E580B065`.
- Uso permitido: local, curado, sin publicacion externa directa.

## Falsadores

- secret/private marker, hash mismatch, unique content loss, strong claim without validation.
- Si aparece secreto, ruta privada o claim fuerte no validado, el estado cambia a `BLOQUEADO`.
