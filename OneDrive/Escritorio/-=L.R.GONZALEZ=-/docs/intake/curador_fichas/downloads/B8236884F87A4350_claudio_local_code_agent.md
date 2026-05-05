# Ficha Curador SETO - claudio_local_code_agent.py

| campo | valor |
|---|---|
| Ruta original | `C:\Users\L-Tyr\Downloads\claudio_local_code_agent.py` |
| SHA256 | `B8236884F87A435082B7622D28DD0C7704919A5614C9CF3F0A54F76BE7034506` |
| Bytes | `47568` |
| Tipo | `file` |
| Estado PSI | `INFERENCIA` |
| Status | `ARCHIVO_FRIO` |
| Clasificacion | `CODE_PROTOTYPE_REVIEW` |
| Lane | `local-agent` |
| Decision | `ABSORBIDO_CANONIZADO_ARCHIVO_FRIO` |
| ActionGate | `REVIEW` |
| Canonico | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\runtime\curador_seto\source_archive\downloads\2026-05-05\B8236884F87A4350_claudio_local_code_agent.py` |
| Atlas | `Claudio / Wabi-Sabi` |

## Resumen

Code prototype; no execution or import until dependencies and side effects are reviewed.

## Sinapsis

- Destino: `Claudio local-agent backlog and COMMS contracts`.
- Evidencia: SHA256 `B8236884F87A435082B7622D28DD0C7704919A5614C9CF3F0A54F76BE7034506`.
- Uso permitido: local, curado, sin publicacion externa directa.

## Falsadores

- secret/private marker, hash mismatch, unique content loss, strong claim without validation.
- Si aparece secreto, ruta privada o claim fuerte no validado, el estado cambia a `BLOQUEADO`.
