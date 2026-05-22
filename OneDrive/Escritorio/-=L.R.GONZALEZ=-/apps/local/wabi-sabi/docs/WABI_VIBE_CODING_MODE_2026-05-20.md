# WABI VIBE CODING MODE 2026-05-20

Fingerprint: `WABI_VIBE_CODING_MODE_20260520`

## Estado

Wabi-Sabi queda cableado como interfaz de programacion y planeacion estilo
Vibe Coding, sin convertir el cloud en ejecutor. La ruta operativa es:

```txt
Chat/UI/CLI
ConversationEngine
LLM proposal only
TaskSpec multiarchivo
Gate Preview
Apply Local Preview
Apply Local explicito
Rollback/tests/scans
WitnessLog/runtime JSON
```

## Contrato JSON

Todo turno de trabajo normalizado debe exponer:

```json
{
  "status": "OK|REVIEW",
  "intent_name": "...",
  "route": "...",
  "proposal": "...",
  "task_spec": {},
  "patch_candidate": {},
  "graphics_plan": {},
  "cloud_provider_called": false,
  "applied_to_sources": false,
  "rollback_snapshot_required": true,
  "next_safe_action": "Review TaskSpec / Preview Apply Local",
  "warnings": ["Proposal-only; Apply Local blocked until explicit local readiness"],
  "tags": ["LLM_proposal", "proposal_only", "vibe_coding"]
}
```

## UI

La UI local en `http://127.0.0.1:8787/` ahora muestra:

- Panel `Vibe Coding`.
- Pipeline visible: Chat, Proposal, TaskSpec, Gate, Preview, Apply.
- Botones seguros: `Programar + tests`, `Debug plan`, `DUAT graphics plan`,
  `Preview Apply Local`.
- Paneles existentes: `Wabi Conversation`, `Review TaskSpec`, `Gate Preview`,
  `LLM Proposal`, `Local Apply Readiness`.

La UI no agrega boton para llamada cloud directa ni para aplicar output cloud.

## CLI

Uso proposal-only local:

```powershell
$env:WABI_LLM_PROVIDER_CLOUD_DEFAULT='1'
wabi --once "programa un helper seguro para validar JSON y genera tests asociados" --json
```

Uso con cloud real controlado, aun proposal-only:

```powershell
$env:WABI_BUILD_ASSIST_CLOUD='1'
$env:WABI_ALLOW_CLOUD_PROVIDERS='1'
wabi --once "programa un helper seguro para validar JSON y genera tests asociados" --json
```

La llamada cloud real requiere tambien que `CloudBudgetGate` permita la llamada.

## Gates

- Cloud live: requiere doble opt-in y presupuesto.
- Apply Local: separado, sandboxed, allowlisted, con rollback y tests.
- DUAT graphics: plan-only, `graphics_live=false`.
- BrowserBridge live: apagado.
- Push/deploy/publicacion: bloqueados.

## Evidencia 2026-05-20

- Wabi focal CLI/core: `30 passed`.
- BRAIN_OS API/UI focal: `25 passed`.
- `py_compile`: PASS.
- CLI code smoke: `cloud_provider_called=false`, `applied_to_sources=false`,
  `graphics_live=false`, tags incluyen `vibe_coding`.
- CLI DUAT graphics smoke: `graphics_plan_ready=true`, `graphics_live=false`,
  tags incluyen `duat_graphics_plan` y `vibe_coding`.
- HTTP UI smoke: `200`, con `Vibe Coding`, `Wabi Conversation`,
  `Review TaskSpec`, `Gate Preview`, `Apply Local Preview` y sin boton
  `Call NVIDIA now` ni `Apply cloud output`.
- Secret scan focal: `FOCAL_SECRET_PATTERN_COUNT=0`.

## Limites

- No se ejecuto live cloud en este ciclo.
- No se ejecuto Apply Local desde UI en este ciclo.
- Browser plugin no estuvo expuesto para screenshot en este turno; el smoke UI
  fue HTTP/HTML.
- Publicacion externa sigue bloqueada por repo/worktree/AssetGate.
