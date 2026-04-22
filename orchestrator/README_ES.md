# Orquestador Multi-IA para Escritura Creativa

**Delega tareas editoriales y de marketing a múltiples modelos con un solo comando.**

Diseñado para autores que usan IA como herramienta de producción y quieren resultados consistentes entre modelos.

---

## Problema que resuelve

Cada modelo de IA tiene fortalezas distintas para tareas de escritura. GPT-4o es mejor para sinopsis largas. DeepSeek y Claude son mejores para revisión de prosa en español. Gemini es rápido para keywords.

Sin este orquestador, cambiar de modelo implica reformatear el prompt cada vez, perder consistencia, y no tener historial comparable entre modelos.

Con el orquestador: **un comando, múltiples modelos, resultados en archivos comparables**.

---

## Tareas disponibles

| Tarea | Descripción |
|---|---|
| `revision` | Revisión editorial con diagnóstico cuantitativo |
| `synopsis-short` | Sinopsis ≤400 caracteres para KDP |
| `synopsis-long` | Sinopsis ≤4,000 caracteres para KDP |
| `keywords` | 10 keywords para Amazon |
| `back-cover` | Texto de contraportada |
| `dialogue-check` | Verificación de voces en diálogo |
| `continuity` | Detección de contradicciones |
| `custom` | Prompt personalizado |

---

## Instalación

```bash
pip install openai anthropic google-generativeai
```

Configura las API keys de los modelos que quieras usar:

```bash
export OPENAI_API_KEY=sk-...
export ANTHROPIC_API_KEY=sk-ant-...
export GOOGLE_API_KEY=...
export DEEPSEEK_API_KEY=...
export XAI_API_KEY=...
```

Solo necesitas las keys de los modelos que vayas a usar. El orquestador funciona con uno solo.

---

## Uso

### Un modelo, selección automática
```bash
python orchestrator.py --task revision --input capitulo.md --model auto
```
`auto` selecciona el mejor modelo disponible para la tarea.

### Modelo específico
```bash
python orchestrator.py --task revision --input capitulo.md --model deepseek
```

### Múltiples modelos en paralelo
```bash
python orchestrator.py --task synopsis-short --input libro.md --models gpt gemini claude
```
Genera un archivo por modelo + un archivo de comparación.

### Tarea personalizada
```bash
python orchestrator.py --task custom --input capitulo.md --model claude \
  --prompt "Analiza el ritmo de las frases. ¿Hay monotonía de longitud?"
```

### Con contexto de saga
```bash
python orchestrator.py --task continuity --input libro_03.md --model gpt \
  --saga "Mi Saga" --book 3 --total-books 10
```

---

## Fortalezas por modelo (basado en pruebas)

| Modelo | Mejor para |
|---|---|
| GPT-4o | Continuidad de saga, sinopsis larga, contraportada |
| Claude | Revisión editorial, continuidad, diálogo |
| Gemini | Keywords, sinopsis corta |
| DeepSeek | Revisión de prosa en español, diálogo |
| Grok | Tono, sinopsis corta |

---

## Formato de salida

Los resultados se guardan en `orchestrator_output/` por defecto:
```
orchestrator_output/
├── revision_deepseek.md
├── revision_claude.md
└── revision_comparacion.md  # Si usaste múltiples modelos
```

---

## Añadir modelos propios

En `orchestrator.py`, añade tu modelo al diccionario `MODELS`:

```python
MODELS["mi_modelo"] = {
    "name": "Mi Modelo",
    "env_key": "MI_MODELO_API_KEY",
    "model_id": "mi-modelo-v1",
    "provider": "openai",  # Si usa la misma API que OpenAI
    "strengths": ["revision", "synopsis-short"],
}
```

Si el proveedor no usa la API de OpenAI, añade un caller en `CALLERS`.

---

*Licencia MIT.*
