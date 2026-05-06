# Matrix Examples

Estado: `EXAMPLES / PUBLIC_SAFE_SYNTHETIC`.

## Caso: usuario quiere crear landing page segura

### 1. Estimacion

- R inicial: `0.46`
- Regimen: `web_local_review`
- Phi_eff: `0.54`
- Gate: `REVIEW` porque puede terminar en publicacion externa.

### 2. Modulos minimos

- `html_foundations`
- `web_ui_minimal`
- `security_actiongate`
- `documentation_witnesslog`
- opcional: `ai_browser_security`

No cargar:

- `duat_world_state`
- `game_metroidvania_design`
- canon privado

### 3. Workpack

```json
{
  "task_id": "landing_safe_001",
  "goal": "crear landing local public-safe",
  "selected_modules": ["html_foundations", "web_ui_minimal", "security_actiongate"],
  "forbidden_actions": ["publish", "collect_secrets", "use_private_assets"],
  "tests": ["html renders locally", "secret scan clean", "copy low-claim"],
  "action_gate": "REVIEW"
}
```

### 4. Cierre

Auditor valida que no haya rutas privadas, claims fuertes o secretos. SecurityGate
bloquea publicacion hasta tener target, scan y aprobacion. Archivist guarda
WitnessLog. WabiSabi entrega archivos y handoff.
