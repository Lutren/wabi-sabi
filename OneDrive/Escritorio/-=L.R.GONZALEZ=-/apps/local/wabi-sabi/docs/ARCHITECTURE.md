# Arquitectura Wabi Sabi Local

## Responsabilidades

```text
wabi_sabi/
  cli/
    main.py      # entrypoint, salida humana/json, modo interactivo
    parser.py    # intencion por reglas locales
    router.py    # registro y seleccion de agentes
  agents/
    base_agent.py
    programmer_agent.py
    debug_agent.py
    research_agent.py
    file_agent.py
  core/
    config.py
    gate.py
    memory.py
    observation.py
    tools.py
  config/
    agents.json
```

## Flujo

1. El CLI recibe texto en lenguaje natural.
2. `parser.py` clasifica intencion.
3. `gate.py` evalua riesgo local.
4. `router.py` selecciona agente desde `config/agents.json`.
5. El agente ejecuta una accion segura.
6. `memory.py` registra JSONL append-only.
7. La respuesta sale con CERTEZA / INFERENCIA / INCOGNITA.

## Contrato de agente

Cada agente declara:

- nombre
- descripcion
- capacidades
- limites
- entrypoint
- `safe_mode`

Entrada: `AgentInput(prompt, parsed, options)`.

Salida: `AgentResult` con `ok`, `action`, `output`, `artifacts`, `evidence`,
`certainty`, `inference`, `unknown` y `error`.

## Extension

1. Crear un nuevo archivo en `wabi_sabi/agents`.
2. Heredar de `BaseAgent`.
3. Agregar entrypoint y capacidades en `wabi_sabi/config/agents.json`.
4. Agregar ruta de intencion si corresponde.
5. Crear test focal en `tests/`.
