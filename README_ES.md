# MEDIOEVO Tools

**Herramientas open source para autores indie de ficción larga.**

Desarrolladas durante la producción de [MEDIOEVO](https://medioevo.space), una saga de ciencia ficción en español, inglés y náhuatl publicada en Amazon KDP.

Tres módulos independientes. Puedes usar cualquiera por separado.

---

## Módulos

### 📋 [`/editorial`](./editorial/) — Sistema de 13 Capas Editoriales
Un framework de control de calidad para manuscritos largos (novelas, sagas).
Incluye umbrales cuantitativos, orden de ejecución probado y un prompt listo para revisión con IA.

**Para quién:** Autores que escriben ficción larga y quieren un proceso de revisión reproducible.

---

### 📦 [`/kdp`](./kdp/) — Pipeline de Publicación KDP
Scripts de Python para generar EPUB, PDF Paperback, PDF Hardcover y DOCX desde Markdown.
Con soporte nativo para lenguas indígenas, integración con DeepL y soluciones para errores comunes de validación KDP.

**Para quién:** Autores indie que publican en Amazon KDP, especialmente en lenguas minorizadas.

---

### 🤖 [`/orchestrator`](./orchestrator/) — Orquestador Multi-IA para Tareas Creativas
CLI para delegar tareas de escritura a múltiples modelos con prompts estructurados por tipo de tarea.

**Para quién:** Autores que usan IA como herramienta de producción y quieren resultados consistentes entre modelos.

---

## Instalación rápida

```bash
git clone https://github.com/Lutren/medioevo-tools
cd medioevo-tools
pip install -r requirements.txt
```

Cada módulo tiene sus propias dependencias documentadas en su `README.md`.

---

## Requisitos generales

- Python 3.10+
- Pandoc
- Ghostscript

---

## Licencia

MIT.

---

## Contribuciones

PRs e issues son bienvenidos.
