# MEDIOEVO Tools

**Open-source tools for indie fiction authors**

These tools were developed during the production of [MEDIOEVO](https://medioevo.space), a science-fiction saga published in Spanish, English and Nahuatl. The repository groups three independent modules that can be used separately.

## Modules

### 📋 [`/editorial`](./editorial/) - 13-Layer Editorial System
A quality-control framework for long manuscripts (novels and sagas). It provides quantitative thresholds, a tested execution order, and a ready-made prompt for AI-assisted revision. Ideal for authors who want a reproducible editing process.

### 📦 [`/kdp`](./kdp/) - KDP Publishing Pipeline
Python scripts to generate EPUB, PDF (paperback and hardcover) and DOCX from Markdown. With native support for indigenous languages (including Nahuatl), integration with DeepL, and fixes for common Amazon KDP validation errors. Useful for indie authors publishing on KDP, especially in minority languages.

### 🤖 [`/orchestrator`](./orchestrator/) - Multi-AI Orchestrator for Creative Tasks
A command-line interface for delegating writing tasks to multiple models (GPT-4o, Gemini, DeepSeek, Grok, Claude) with structured prompts per task. Designed for writers who use AI and want consistent results across models.

## Quick installation

```bash
git clone https://github.com/Lutren/medioevo-tools
cd medioevo-tools
pip install -r requirements.txt
```

Each module documents its own dependencies in its README.

The Spanish guides are kept as `README_ES.md` files next to the English ones.

## General requirements

- Python 3.10+
- Pandoc (for format conversions)
- Ghostscript (for KDP-friendly PDFs)

## License

MIT - use it, modify it, distribute it.

## Project status

| Module | Status |
|---|---|
| 13-Layer Editorial System | Stable |
| KDP Pipeline | Stable |
| Multi-AI Orchestrator | Beta |

## Contributing

Pull requests and issues are welcome.
