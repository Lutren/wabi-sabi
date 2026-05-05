# Ficha Curador SETO - claudio_local_code_agent (1).py

| campo | valor |
|---|---|
| Ruta original | `C:\Users\L-Tyr\Downloads\claudio_local_code_agent (1).py` |
| SHA256 | `B8236884F87A435082B7622D28DD0C7704919A5614C9CF3F0A54F76BE7034506` |
| Bytes | `47568` |
| Tipo | `file` |
| Estado PSI | `CERTEZA` |
| Status | `DUPLICADO_EXACTO` |
| Clasificacion | `CODE_PROTOTYPE_REVIEW` |
| Lane | `local-agent` |
| Decision | `CANDIDATE_DELETE_EXACT_DUPLICATE` |
| ActionGate | `REVIEW` |
| Canonico | `C:\Users\L-Tyr\Downloads\claudio_local_code_agent.py` |

## Resumen

Code prototype; no execution or import until dependencies and side effects are reviewed.

## Sinapsis

- Destino: `Claudio local-agent backlog and COMMS contracts`.
- Evidencia: SHA256 `B8236884F87A435082B7622D28DD0C7704919A5614C9CF3F0A54F76BE7034506`.
- Uso permitido: local, curado, sin publicacion externa directa.

## Falsadores

- secret/private marker, hash mismatch, unique content loss, strong claim without validation.
- Si aparece secreto, ruta privada o claim fuerte no validado, el estado cambia a `BLOQUEADO`.
