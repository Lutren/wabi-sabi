# Workpack de Cierre Local - 2026-05-06

Estado: `ACTIVO / LOCAL_ONLY / SIN_ACCIONES_EXTERNAS`

Fuente principal: `REPORTE_AVANCES_PROXIMOS_PASOS_MEDIOEVO_2026-05-06.md` y
carpeta `Escritorio\promts`.

## Regla central

Reducir R operativo sin crear capas nuevas. Cada agente debe leer fuentes
reales, tocar solo su carril, dejar evidencia y no pisar trabajo concurrente.

## Carriles y archivos permitidos

| carril | permiso | no tocar |
|---|---|---|
| Curador SETO | `docs/intake`, `runtime/curador_seto`, `qa_artifacts/witness_log` | borrado fisico sin manifest |
| CEREBRO | `_MANIFIESTOS`, fichas, canon limpio | libros completos, ZIPs, DOCX/PDF sin ficha |
| Matrix/Biblioteca | `docs/matrix`, `library/index.json`, `library/modules` | CEREBRO completo en contexto |
| DUAT read-only | `docs/duat`, adapter read-only, tests sinteticos | DUAT/GEODIA real, RPG privado |
| AI Browser | `docs/ai_browser`, fixtures sinteticas | login, credenciales, scraping masivo |
| Lenguaje Observacionista | `docs/language`, `research/observacionismo-lab` | reemplazar Python/Godot/TypeScript |
| Programador Seguro | specs/stubs/tests de rollback | autonomia amplia, modelos pesados |
| Mission Control | reportes/UI read-only | daemons, acciones remotas |
| Release/Public-safe | allowlist/denylist/checklists | push, publish, Gumroad, LinkedIn |
| RPG Tooling | docs privadas/read-only | assets, legal/IP, publicacion |

## Cola P0

1. Mantener `pending_review.py --write --quiet` como snapshot de entrada.
2. Cerrar integracion de `promts` con fichas y hashes.
3. Convertir `OSIT Resource Optimizer` en policy spec antes de tocar runtime.
4. Generar manifest de limpieza CEREBRO antes de mover/renombrar.
5. Consolidar cambios concurrentes por agente, no con staging amplio.

## Cola P1

1. UI read-only de Matrix/COMMS en Mission Control.
2. Adapter OSIT Resource Optimizer para Wabi-Sabi/Sentido Comun.
3. AI Browser seguro como CLI/prototipo sin login.
4. Programador seguro con PatchPlanner/RollbackStore/SafeExecutor.
5. Release public-safe scan para paquetes allowlist.

## ActionGate

| accion | gate |
|---|---|
| leer, fichar, documentar, test local | `APPROVE` |
| mover/renombrar fuentes unicas | `REVIEW` |
| borrar duplicado exacto con hash/copia canonica | `REVIEW -> APPROVE path-specific` |
| publicar, push, Gumroad, LinkedIn, web externa | `BLOCK` hasta gate especifico |
| tocar secretos, RPG/TCG, claims fisicos fuertes | `BLOCK` |
| modelos pesados, alias Ollama, training | `BLOCK` |

## Handoff

Fingerprint: `WORKPACK_CIERRE_LOCAL_2026-05-06_F3EB20AC`

Brief:

- Prompts de Escritorio ya tienen registro y decision.
- CEREBRO reciente tiene manifest de limpieza reversible.
- El proximo cierre tecnico de alto valor es OSIT Resource Optimizer como
  policy-only adapter.
- No hay autorizacion de publicacion ni borrado global.
