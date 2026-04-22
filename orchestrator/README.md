# Multi-AI Orchestrator for Creative Writing

**Delegate editorial and marketing tasks to multiple models with a single command.**

Designed for authors who use AI as a production tool and want consistent results across models.

## The problem it solves

Each AI model has different strengths for writing tasks. GPT-4o is often better for long synopses, Claude is usually stronger on editorial review, and Gemini is fast for keyword generation. Without an orchestrator, switching models means reformatting prompts, losing consistency, and scattering outputs. With this tool: **one command, multiple models, comparable markdown results**.

## Available tasks

| Task | Description |
|---|---|
| `revision` | Editorial revision with quantitative diagnosis |
| `synopsis-short` | Synopsis <=400 characters for KDP |
| `synopsis-long` | Synopsis <=4,000 characters for KDP |
| `keywords` | Ten Amazon keywords |
| `back-cover` | Back-cover text |
| `dialogue-check` | Voice distinction check in dialogue |
| `continuity` | Detection of contradictions |
| `custom` | Custom prompt |

## Installation

Install the API clients for the models you plan to use:

```bash
pip install openai anthropic google-generativeai
```

Then set the relevant API keys:

```bash
export OPENAI_API_KEY=...
export ANTHROPIC_API_KEY=...
export GOOGLE_API_KEY=...
export DEEPSEEK_API_KEY=...
export XAI_API_KEY=...
```

## Usage

### One model, automatic selection

```bash
python orchestrator.py --task revision --input chapter.md --model auto
```

### Specific model

```bash
python orchestrator.py --task revision --input chapter.md --model deepseek
```

### Multiple models

```bash
python orchestrator.py --task synopsis-short --input book.md --models gpt gemini claude
```

### Custom task

```bash
python orchestrator.py --task custom --input chapter.md --model claude --prompt "Analyze the rhythm of the sentences."
```

## Output format

The orchestrator writes markdown files into `orchestrator_output/`, with one file per model and, when multiple models are used, an additional comparison file.

## License

Distributed under the MIT license.

The Spanish guide is available as `README_ES.md`.
