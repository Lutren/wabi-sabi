# Ficha Curador SETO - Untitled.txt

| campo | valor |
|---|---|
| Ruta original | `C:\Users\L-Tyr\Downloads\New folder\Untitled.txt` |
| SHA256 | `A9184A8D7D91FA97762D35C166CA5A5027793B175F8115CD2A9706D94D017636` |
| Bytes | `52379` |
| Tipo | `file` |
| Estado PSI | `CERTEZA` |
| Status | `REGISTRADO` |
| Clasificacion | `TEXT_SOURCE_REVIEW` |
| Lane | `cleanup` |
| Decision | `HOLD_WITH_TECHNICAL_CARD_BEFORE_USE` |
| ActionGate | `REVIEW` |
| Canonico | `C:\Users\L-Tyr\Downloads\New folder\Untitled.txt` |

## Resumen

Text source; register before deciding canon, archive or deletion.

## Sinapsis

- Destino: `Curador review queue`.
- Evidencia: SHA256 `A9184A8D7D91FA97762D35C166CA5A5027793B175F8115CD2A9706D94D017636`.
- Uso permitido: local, curado, sin publicacion externa directa.

## Falsadores

- secret/private marker, hash mismatch, unique content loss, strong claim without validation.
- Si aparece secreto, ruta privada o claim fuerte no validado, el estado cambia a `BLOQUEADO`.
