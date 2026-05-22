# Wabi Sabi Conversational Blueprints - 2026-05-06

## Estado

Wabi Sabi Auto ya no debe comportarse como un router binario entre agente local
y Codex. El modo correcto es:

1. Respuesta local inmediata.
2. ActionGate antes de efectos externos.
3. Blueprints locales para contexto y limites.
4. Codex background solo como ampliacion, no como reemplazo de la respuesta.

## Blueprints Cargados

`BlueprintPolicyLoader` detecta 7 fuentes locales:

- `docs/ops/WABI_SABI_QWEN_BLUEPRINT_WORKPACK_2026-05-06.md`
- `docs/ops/QWEN_BLUEPRINT_LOCAL_INDEX_2026-05-06.md`
- `docs/ops/WABI_OSIT_BRIDGE_FROM_ESTADO_2026-05-06.md`
- `docs/ops/OSIT_RESOURCE_OPTIMIZER_RUNTIME_SPEC_2026-05-06.md`
- `runtime/prompt_master/prompt_master_execution_controller_2026-05-06.json`
- `COMMS/agents_state/wabi-sabi-sentido-comun.json`
- `COMMS/agents_state/claudio-local-autonomy.json`

Senales principales:

- `blueprints_loaded`
- `host_or_heavy_models_blocked`
- `ollama_alias_blocked`
- `ollama_optional_by_blueprint`
- `osit_policy_only`
- `workpack_fallback_available`

## Comportamiento Conversacional

Wabi Auto mantiene memoria conversacional local en:

- `runtime/memory/session_memory.jsonl`

La memoria guarda resumen acotado de cada turno auto, ruta, gate, salida y
artefactos. No reemplaza los blueprints ni autoriza acciones externas; solo
permite continuidad inmediata dentro de la sesion.

### Contacto directo

Prompt ejemplo:

```text
hola, estamos en contacto directo?
```

Ruta esperada:

```text
local_chat / APPROVE
```

Respuesta esperada:

```text
Si. Esta ventana es contacto directo con Wabi Sabi Auto local...
```

### Pedido amplio public-safe

Prompt ejemplo:

```text
same algo de tech que pueda liberar el dia de hoy por redes y que no revele tanto pero sea una solucion a algun problema actual
```

Ruta esperada:

```text
hybrid_codex_background / APPROVE
```

Respuesta esperada:

- brief local inmediato;
- propuesta public-safe basada en ActionGate Lite;
- lista de que mostrar y que retener privado;
- job Codex en background para ampliar.

### Follow-up corto con memoria

Secuencia ejemplo:

```text
sacame algo de tech que pueda liberar hoy por redes...
aplicalo
```

Ruta esperada del segundo turno:

```text
local_chat / APPROVE / local_memory_followup
```

Respuesta esperada:

- retoma ActionGate Lite;
- no publica ni envia fuera;
- entrega aplicacion local segura y copy public-safe;
- propone convertirlo en post o demo sintetica.

Comando para inspeccionar memoria:

```powershell
wabi auto
/memory
```

## Implementacion

- `wabi_sabi/core/conversation.py`
  - `local_chat_response`
  - `blueprint_release_brief`
  - `is_followup`
  - `recent_topic`
- `wabi_sabi/core/memory.py`
  - `tail_memory`
  - `conversation_summary`
- `wabi_sabi/core/auto_router.py`
  - `local_chat`
  - `hybrid_codex`
- `wabi_sabi/cli/main.py`
  - respuesta local para `local_chat`;
  - respuesta local + job para `hybrid_codex_background`.

## Validacion

Comando:

```powershell
python -m pytest -q
```

Resultado:

```text
51 passed in 1.64s
```

Reproduccion manual:

- contacto directo: `local_chat`, sin job;
- idea tech/redes: `hybrid_codex_background`, con brief local y job.
- follow-up `aplicalo`: `local_chat`, con continuidad desde memoria local.

## Bloqueos

- No publica en redes por si solo.
- No libera blueprints internos.
- No usa Ollama por defecto.
- No crea aliases/modelos/pesos.
- No toca privado, secretos, RPG/TCG ni runtime Claudio completo.
