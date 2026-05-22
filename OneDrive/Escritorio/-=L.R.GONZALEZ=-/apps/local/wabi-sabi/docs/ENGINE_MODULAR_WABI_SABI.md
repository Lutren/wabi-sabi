# Wabi-Sabi Modular Engine

## Objetivo

Wabi-Sabi ahora tiene un carril inicial para convertir referencias publicas como
GDevelop, Dyad/OpenHands y patrones tipo Lovable en ingenieria propia, sin copiar
codigo ni venderizar repos externos.

El motor no instala dependencias ni escribe fuentes por si solo. Primero produce:

- `wabi.engine.source_card.v1`: tarjeta clean-room de una fuente.
- `wabi.engine.plan.v1`: plan modular app/juego/programacion.
- `wabi.task_spec.v1`: spec revisable que luego pasa por `task-spec-plan` y
  `task-spec-apply`.

## Comandos

```powershell
python -m wabi_sabi.cli.main engine-status --json
python -m wabi_sabi.cli.main engine-intake GDevelop --json
python -m wabi_sabi.cli.main engine-plan "crear app local con escena de juego" --json
python -m wabi_sabi.cli.main engine-task-spec .\engine_plan.json --target docs/engine/demo_ENGINE_PLAN.md --json
python -m wabi_sabi.cli.main engine-sandbox --json
python -m wabi_sabi.cli.main engine-project-validate docs\engine\local_only\wabi_sabi_observatorio_sandbox_PROJECT_SPEC.json --json
python -m wabi_sabi.cli.main engine-simulate docs\engine\local_only\wabi_sabi_observatorio_sandbox_PROJECT_SPEC.json 3 --json
```

Para planes privados/locales:

```powershell
python -m wabi_sabi.cli.main engine-plan "LOCAL_ONLY NO_PUBLICAR crear app local con escena" --write-docs --json
python -m wabi_sabi.cli.main engine-task-spec runtime\outputs\engine_plans\<plan>.json --target docs/engine/local_only/demo_ENGINE_PLAN.md --write-docs --json
python -m wabi_sabi.cli.main task-spec-plan docs\engine\local_only\<task_spec>.json --json
python -m wabi_sabi.cli.main task-spec-apply docs\engine\local_only\<task_spec>.json --json
python -m wabi_sabi.cli.main engine-sandbox --write-docs --json
python -m wabi_sabi.cli.main engine-project-validate docs\engine\local_only\wabi_sabi_observatorio_sandbox_PROJECT_SPEC.json --json
python -m wabi_sabi.cli.main engine-simulate docs\engine\local_only\wabi_sabi_observatorio_sandbox_PROJECT_SPEC.json 3 --json
```

`docs/engine/local_only/` esta ignorado por Git para reducir el riesgo de
publicacion accidental. Sigue siendo un artefacto local y revisable.

## Project Runtime v1

`engine-sandbox` genera un `wabi.engine.project_spec.v1` local-only con:

- `project_graph`: nodos y edges de app shell, escena, event sheet,
  programmer core y registry.
- `event_sheet`: reglas declarativas ordenadas por prioridad.
- `visibility`: `LOCAL_ONLY`, `NO_PUBLICAR`, `publish_allowed=false`.
- `fingerprint`: SHA-256 canonico para validar continuidad.

`engine-project-validate` verifica:

- edges apuntan a nodos existentes;
- reglas tienen condiciones y acciones;
- `visibility` sigue local-only;
- el fingerprint coincide;
- campos de ruta no apuntan a marcadores privados como RPG/TCG/game_bridge.

`engine-simulate` ejecuta eventos locales contra el event sheet. Para el
Observatorio Sandbox, tres clicks en `observe_button` deben producir:

- `scene.observation_count=3`;
- `pattern_marker.visible=true`;
- `residue_meter.value=0.12`;
- `sandbox.action_gate=APPROVE`.

## Modulos v1

- `observation_kernel`: ActionGate, ObservationEnvelope, evidencia y residuo.
- `project_graph`: grafo de proyecto, nodos, edges y contrato de archivos.
- `app_core`: rutas, estado, componentes y preview local.
- `game_core`: scene graph, event sheet, asset catalog y runtime systems.
- `programmer_core`: task specs, patch plans, SafeExecutor y rollback.
- `extension_registry`: discovery de capacidades modulares.

## Fronteras

- No copiar codigo de repos externos.
- No venderizar GDevelop/Dyad/OpenHands.
- No tocar rutas privadas RPG/TCG/game_bridge.
- No publicar, desplegar ni cambiar licencias desde este carril.
- No saltarse ActionGate, SafeExecutor, ObservationEnvelope o WitnessLog.

## Ruta segura

1. `engine-intake` crea la tarjeta de fuente.
2. `engine-plan` arma el plan modular clean-room.
3. Guardar el JSON del plan si se quiere materializar.
4. `engine-task-spec` lo convierte en `wabi.task_spec.v1`.
5. `task-spec-plan` valida el diff sin escribir fuente.
6. `task-spec-apply` aplica solo con SafeExecutor, rollback y evidencia.
