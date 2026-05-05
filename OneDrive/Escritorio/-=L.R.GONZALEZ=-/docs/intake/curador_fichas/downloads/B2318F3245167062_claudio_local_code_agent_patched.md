# Ficha Curador SETO - claudio_local_code_agent_patched.py

| campo | valor |
|---|---|
| Ruta original | `C:\Users\L-Tyr\Downloads\claudio_local_code_agent_patched.py` |
| SHA256 | `B2318F3245167062B9152AD9B46C241CF1281E614125487C213306A76B6606E2` |
| Bytes | `50899` |
| Tipo | `file` |
| Estado PSI | `CERTEZA` |
| Status | `REGISTRADO` |
| Clasificacion | `CODE_PROTOTYPE_REVIEW` |
| Lane | `local-agent` |
| Decision | `READ_REVIEW_TEST_BEFORE_IMPORT` |
| ActionGate | `REVIEW` |
| Canonico | `C:\Users\L-Tyr\Downloads\claudio_local_code_agent_patched.py` |

## Resumen

Code prototype; no execution or import until dependencies and side effects are reviewed.

## Sinapsis

- Destino: `Claudio local-agent backlog and COMMS contracts`.
- Evidencia: SHA256 `B2318F3245167062B9152AD9B46C241CF1281E614125487C213306A76B6606E2`.
- Uso permitido: local, curado, sin publicacion externa directa.

## Falsadores

- secret/private marker, hash mismatch, unique content loss, strong claim without validation.
- Si aparece secreto, ruta privada o claim fuerte no validado, el estado cambia a `BLOQUEADO`.
