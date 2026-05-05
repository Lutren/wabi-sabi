# Ficha Curador SETO - claudio_local_code_agent_patched.py

| campo | valor |
|---|---|
| Ruta original | `C:\Users\L-Tyr\Downloads\claudio_local_code_agent_patched.py` |
| SHA256 | `B2318F3245167062B9152AD9B46C241CF1281E614125487C213306A76B6606E2` |
| Bytes | `50899` |
| Tipo | `file` |
| Estado PSI | `INFERENCIA` |
| Status | `ARCHIVO_FRIO` |
| Clasificacion | `CODE_PROTOTYPE_REVIEW` |
| Lane | `local-agent` |
| Decision | `ABSORBIDO_CANONIZADO_ARCHIVO_FRIO` |
| ActionGate | `REVIEW` |
| Canonico | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\runtime\curador_seto\source_archive\downloads\2026-05-05\B2318F3245167062_claudio_local_code_agent_patched.py` |
| Atlas | `Claudio / Wabi-Sabi` |

## Resumen

Code prototype; no execution or import until dependencies and side effects are reviewed.

## Sinapsis

- Destino: `Claudio local-agent backlog and COMMS contracts`.
- Evidencia: SHA256 `B2318F3245167062B9152AD9B46C241CF1281E614125487C213306A76B6606E2`.
- Uso permitido: local, curado, sin publicacion externa directa.

## Falsadores

- secret/private marker, hash mismatch, unique content loss, strong claim without validation.
- Si aparece secreto, ruta privada o claim fuerte no validado, el estado cambia a `BLOQUEADO`.
