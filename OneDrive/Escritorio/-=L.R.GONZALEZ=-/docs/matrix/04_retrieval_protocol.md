# Matrix Retrieval Protocol

Estado: `RETRIEVAL_PROTOCOL / MINIMAL_CONTEXT`.

## Entrada

```json
{
  "user_goal": "crear landing page segura",
  "risk": "medium",
  "needed_domains": ["web", "security", "documentation"],
  "forbidden_domains": ["private_canon", "external_publish"]
}
```

## Proceso

1. Normalizar intencion.
2. Estimar R, regimen y Phi_eff.
3. Buscar modulos por `domain`, `primitives`, `inputs` y `outputs`.
4. Eliminar modulos con combinaciones prohibidas.
5. Ordenar por menor dependencia y mayor evidencia.
6. Cargar solo `minimal_summary`, invariantes, safety constraints y ejemplos.
7. Si falta evidencia, devolver `REVIEW` y pedir modulo o fuente.

## Resultado

```json
{
  "selected_modules": ["html_foundations", "web_ui_minimal", "security_actiongate"],
  "excluded_modules": ["game_metroidvania_design"],
  "gate": "REVIEW",
  "reason": "landing page can be planned locally; publish remains blocked"
}
```

## Regla

RAG/FTS5 puede ayudar a recuperar rutas, pero no decide verdad. La verdad
operativa viene de modulo validado, evidencia local, falsador y ActionGate.
