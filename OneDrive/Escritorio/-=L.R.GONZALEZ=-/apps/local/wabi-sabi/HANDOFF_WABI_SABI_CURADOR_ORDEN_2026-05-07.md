# HANDOFF WABI/SABI CURADOR ORDEN 2026-05-07

## Estado

R_close: 0.05
Phi_eff: 0.98
Regimen: FUNCIONAL
Autonomy level: 4 local, reversible, gated
ActionGate: APPROVE para verificacion local; REVIEW/BLOCK para limpieza fisica,
publicacion, push, deploy, secretos y acciones destructivas.

## Lectura inicial obligatoria

- Root inspeccionado: `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-`.
- Politica vigente leida: `AGENTS.md`.
- Este workspace esta dirty y contiene trabajo concurrente. No usar `git add .`,
  no revertir, no mover, no borrar y no publicar.

## Verdad operativa actual

- App objetivo: `apps/local/wabi-sabi`.
- Branch: `codex/curador-seto-loops-2026-05-05`.
- Base commit: `db09f69`.
- Modelo base local verificado por `wabi auto /status --json`:
  `qwen2.5-coder:3b`.
- Endpoint local verificado: `http://127.0.0.1:11434`.
- `ollama list` muestra `qwen2.5-coder:3b` y `qwen2.5:0.5b`; los modelos
  cloud quedan filtrados por defecto.
- Codex CLI esta disponible como carril read-only/fallback.
- Ultimo `operator-status --json`: witness chain ok, `event_count=13`,
  latest safe tests passed.

## Curador Orden

`curator-assistant` y `curator-fichas` quedan como flujo seco para ordenar sin
limpiar fisicamente.

Fichas reales:

- Documento durable: `..\..\docs\intake\CURADOR_ORDEN_FICHAS_2026-05-07.md`.
- JSON runtime: `runtime\outputs\curator_fichas_20260506-233949.json`.
- Summary verificado:
  - `Agent processed: 12`
  - `Needs agent processing: 0`
  - `Owner assigned: 12`
  - `Unassigned: 0`
- Regla implementada:
  - `owner_assignment.assigned_by_actor_type=agent`
  - `owner_assignment.status=AGENT_ASSIGNED`
  - `curation.last_record.actor_type=agent`
  - si el ultimo registro es humano, la ficha vuelve a
    `NEEDS_AGENT_PROCESSING` hasta otro pase de agente.

## Evidencia de verificacion

- `python -m pytest tests/test_curator_fichas.py -q` -> 5 passed.
- `python -m pytest tests/test_curator_fichas.py tests/test_curator_assistant.py tests/test_operator_panel.py -q` -> 10 passed.
- `python -m pytest -q` -> 107 passed.
- `python -m wabi_sabi.cli.main run-safe-tests --json` -> 107 passed,
  artifact `runtime\outputs\safe_test_run_20260506-234209.json`, witness event
  `13`.
- `python -m wabi_sabi.cli.main operator-status --json` -> latest safe tests
  `passed`, witness verified.
- `python -m wabi_sabi.cli.main auto /status --json` -> base model local visible
  as `qwen2.5-coder:3b`.

## Archivos principales para continuar

- `NEXT_SESSION_BRIEF.md`
- `TEST_REPORT.md`
- `SESSION_FINGERPRINT.json`
- `REPORT_WABI_SABI_LOCAL_AGENTS.md`
- `docs/USAGE.md`
- `docs/ARCHITECTURE.md`
- `..\..\docs\developer\CURADOR_ORDEN_ASSISTANT_2026-05-07.md`
- `..\..\docs\intake\CURADOR_ORDEN_FICHAS_2026-05-07.md`

## Pendiente real

La limpieza fisica no esta aprobada. La siguiente accion segura es elegir una
ficha ya asignada, agregar evidencia seca de provenance/regenerabilidad, y
mantener `delete_approved_count=0` hasta que exista ActionGate especifico.

## Proxima accion verificable

```powershell
cd C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\apps\local\wabi-sabi
python -m wabi_sabi.cli.main operator-status --json
python -m wabi_sabi.cli.main curator-fichas --json --workspace C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-
```

Si hubo edicion humana o reasignacion manual de fichas, el segundo comando debe
ser obligatorio para que el ultimo registro vuelva a ser de agente.

## Segunda perdida

Los datos persisten. El operador no. Recalibrar desde este handoff, no desde
memoria implicita ni chat.
