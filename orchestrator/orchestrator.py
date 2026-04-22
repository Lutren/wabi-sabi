#!/usr/bin/env python3
"""
MEDIOEVO Orchestrator
Delegate creative writing tasks to multiple AI models through structured prompts.

Usage:
    python orchestrator.py --task revision --input chapter.md --model deepseek
    python orchestrator.py --task synopsis-short --input book.md --model gpt
    python orchestrator.py --task synopsis-long --input book.md --models gpt claude gemini

Environment variables required by the selected models:
    OPENAI_API_KEY
    ANTHROPIC_API_KEY
    GOOGLE_API_KEY
    DEEPSEEK_API_KEY
    XAI_API_KEY

License: MIT
"""

import argparse
import os
import sys
import json
from pathlib import Path
from dataclasses import dataclass
from typing import Callable


# ──────────────────────────────────────────────────────────────────────────────
# TIPOS DE TAREAS
# ──────────────────────────────────────────────────────────────────────────────

TASK_TYPES = {
    "revision": "Editorial manuscript review",
    "synopsis-short": "Short KDP synopsis (<=400 characters)",
    "synopsis-long": "Long KDP synopsis (<=4,000 characters)",
    "keywords": "10 Amazon KDP keywords",
    "back-cover": "Back-cover copy",
    "chapter-outline": "Chapter outline from notes",
    "dialogue-check": "Dialogue voice consistency check",
    "continuity": "Continuity and contradiction review",
    "custom": "Custom prompt",
}

# Available models and identifiers.
MODELS = {
    "gpt": {
        "name": "GPT-4o",
        "env_key": "OPENAI_API_KEY",
        "model_id": "gpt-4o",
        "provider": "openai",
        "strengths": ["continuity", "synopsis-long", "back-cover"],
    },
    "claude": {
        "name": "Claude Sonnet",
        "env_key": "ANTHROPIC_API_KEY",
        "model_id": "claude-sonnet-4-20250514",
        "provider": "anthropic",
        "strengths": ["revision", "continuity", "dialogue-check"],
    },
    "gemini": {
        "name": "Gemini 1.5 Pro",
        "env_key": "GOOGLE_API_KEY",
        "model_id": "gemini-1.5-pro",
        "provider": "google",
        "strengths": ["synopsis-short", "keywords"],
    },
    "deepseek": {
        "name": "DeepSeek Chat",
        "env_key": "DEEPSEEK_API_KEY",
        "model_id": "deepseek-chat",
        "provider": "deepseek",
        "strengths": ["revision", "dialogue-check"],
    },
    "grok": {
        "name": "Grok",
        "env_key": "XAI_API_KEY",
        "model_id": "grok-3",
        "provider": "xai",
        "strengths": ["synopsis-short", "back-cover"],
    },
}


# ──────────────────────────────────────────────────────────────────────────────
# PROMPTS POR TAREA
# ──────────────────────────────────────────────────────────────────────────────

def build_revision_prompt(text: str, context: dict) -> str:
    saga_name = context.get("saga", "the saga")
    book_num = context.get("book", "X")
    total_books = context.get("total_books", "N")

    return f"""You are a professional literary editor specialized in science fiction.
You are reviewing an excerpt from Book {book_num} of {total_books} in {saga_name}.

CRITICAL CONTEXT:
1. This is NOT a standalone book. Unresolved threads may be intentional.
2. The prose may fragment deliberately near the end of the book.
3. Do NOT suggest resolutions that belong in later books.

QUANTITATIVE DIAGNOSTIC - count and report:
• vague filler patterns
• simile-over-abstraction patterns
• decorative phrasing that weakens precision
• mechanical reversal constructions
• chains of 3 or more sentences with 4 words or fewer

STRUCTURAL DIAGNOSTIC:
• Is there an irreversible change in the scene?
• Does the protagonist act, or only react?
• Are the character voices distinguishable?
• Does the scene explain what it already showed?

FOR EACH PROBLEM:
1. Exact quote (<=20 words)
2. Specific diagnosis
3. Minimal concrete fix
4. Effort: LOW / MEDIUM / HIGH

Maximum 10 issues, ordered by impact.
At the end: 2 strengths that should NOT be touched.
Verdict: PUBLISH / MINOR REVISION / REWRITE

TEXT:
{text}"""


def build_synopsis_short_prompt(text: str, context: dict) -> str:
    lang = context.get("lang", "en")
    return f"""You are an editorial copywriter specialized in Amazon KDP.

Write a selling synopsis for Amazon KDP.
STRICT CONSTRAINTS:
- Maximum 400 characters
- Write in {lang}
- Open with the core tension or question, not the protagonist's name
- No spoilers for the main twist
- End with a hook that invites purchase
- Avoid generic phrases such as "a journey", "a story", or "will discover"

MANUSCRIPT:
{text[:3000]}..."""


def build_synopsis_long_prompt(text: str, context: dict) -> str:
    lang = context.get("lang", "en")
    return f"""You are an editorial copywriter specialized in Amazon KDP.

Write the long-form synopsis for an Amazon KDP product page.
CONSTRAINTS:
- Between 2,000 and 4,000 characters
- Write in {lang}
- Structure: hook (1 paragraph) + central conflict (2-3 paragraphs) + stakes (1 paragraph) + final hook
- Do not reveal the main twist
- Basic KDP-safe HTML is allowed: <b>, <i>, <br>, <ul>, <li>

MANUSCRIPT:
{text[:8000]}..."""


def build_keywords_prompt(text: str, context: dict) -> str:
    lang = context.get("lang", "en")
    return f"""You are an Amazon KDP SEO specialist.

Generate exactly 10 keywords for this book on Amazon KDP.
RULES:
- Write in {lang}
- Each keyword must contain 2-5 words
- Focus on real reader searches, not abstract themes
- Include genre, subgenre, thematic elements, and audience
- Do NOT include the title or author name
- Output one keyword per line with no numbering

BISAC reference:
{context.get('bisac', 'Science Fiction')}

MANUSCRIPT (first 2000 characters):
{text[:2000]}"""


def build_dialogue_check_prompt(text: str, context: dict) -> str:
    characters = context.get("characters", {})
    char_desc = "\n".join([f"- {name}: {desc}" for name, desc in characters.items()])

    return f"""You are an editor specialized in character voice.

CHARACTERS AND SPEECH PATTERNS:
{char_desc if char_desc else "Not provided - infer them from the text."}

TASK:
Identify dialogue fragments where the character voice feels inconsistent with the profile.
For each inconsistency:
1. Exact quote
2. Character speaking
3. Why it sounds off-profile
4. Suggested rewrite

If there are no inconsistencies, report the 2-3 clearest voice strengths in the text.

TEXT:
{text}"""


def build_continuity_prompt(text: str, context: dict) -> str:
    return f"""You are a continuity editor for long-form fiction.

Analyze the text for:
1. Internal contradictions
2. Characters who know things they should not know yet
3. World rules applied inconsistently
4. Internal chronology errors

For each problem:
1. Quote A (first mention)
2. Quote B (contradiction)
3. Exact diagnosis
4. Minimal fix

If there are no contradictions, confirm the 3 strongest continuity elements.

TEXT:
{text}"""


TASK_PROMPTS: dict[str, Callable] = {
    "revision": build_revision_prompt,
    "synopsis-short": build_synopsis_short_prompt,
    "synopsis-long": build_synopsis_long_prompt,
    "keywords": build_keywords_prompt,
    "dialogue-check": build_dialogue_check_prompt,
    "continuity": build_continuity_prompt,
}


# ──────────────────────────────────────────────────────────────────────────────
# ADAPTADORES POR PROVEEDOR
# ──────────────────────────────────────────────────────────────────────────────

def call_openai(prompt: str, model_id: str, api_key: str) -> str:
    try:
        from openai import OpenAI
        client = OpenAI(api_key=api_key)
        response = client.chat.completions.create(
            model=model_id,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=2000,
        )
        return response.choices[0].message.content
    except ImportError:
        return "ERROR: pip install openai"
    except Exception as e:
        return f"ERROR OpenAI: {e}"


def call_anthropic(prompt: str, model_id: str, api_key: str) -> str:
    try:
        import anthropic
        client = anthropic.Anthropic(api_key=api_key)
        response = client.messages.create(
            model=model_id,
            max_tokens=2000,
            messages=[{"role": "user", "content": prompt}],
        )
        return response.content[0].text
    except ImportError:
        return "ERROR: pip install anthropic"
    except Exception as e:
        return f"ERROR Anthropic: {e}"


def call_google(prompt: str, model_id: str, api_key: str) -> str:
    try:
        import google.generativeai as genai
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel(model_id)
        response = model.generate_content(prompt)
        return response.text
    except ImportError:
        return "ERROR: pip install google-generativeai"
    except Exception as e:
        return f"ERROR Google: {e}"


def call_deepseek(prompt: str, model_id: str, api_key: str) -> str:
    """DeepSeek uses an OpenAI-compatible API."""
    try:
        from openai import OpenAI
        client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")
        response = client.chat.completions.create(
            model=model_id,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=2000,
        )
        return response.choices[0].message.content
    except ImportError:
        return "ERROR: pip install openai"
    except Exception as e:
        return f"ERROR DeepSeek: {e}"


def call_xai(prompt: str, model_id: str, api_key: str) -> str:
    """Grok uses an OpenAI-compatible API."""
    try:
        from openai import OpenAI
        client = OpenAI(api_key=api_key, base_url="https://api.x.ai/v1")
        response = client.chat.completions.create(
            model=model_id,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=2000,
        )
        return response.choices[0].message.content
    except ImportError:
        return "ERROR: pip install openai"
    except Exception as e:
        return f"ERROR xAI: {e}"


CALLERS = {
    "openai": call_openai,
    "anthropic": call_anthropic,
    "google": call_google,
    "deepseek": call_deepseek,
    "xai": call_xai,
}


# ──────────────────────────────────────────────────────────────────────────────
# ORCHESTRATOR
# ──────────────────────────────────────────────────────────────────────────────

def run_task(
    task: str,
    text: str,
    model_key: str,
    context: dict,
    custom_prompt: str | None = None,
) -> dict:
    """Run a task on a specific model."""
    model = MODELS[model_key]
    api_key = os.environ.get(model["env_key"])

    if not api_key:
        return {
            "model": model["name"],
            "status": "error",
            "result": f"API key not found. Set {model['env_key']}",
        }

    if task == "custom" and custom_prompt:
        prompt = f"{custom_prompt}\n\nTEXT:\n{text}"
    elif task in TASK_PROMPTS:
        prompt = TASK_PROMPTS[task](text, context)
    else:
        return {"model": model["name"], "status": "error", "result": f"Unknown task: {task}"}

    print(f"  -> {model['name']}...", end=" ", flush=True)
    caller = CALLERS[model["provider"]]
    result = caller(prompt, model["model_id"], api_key)
    print("✓")

    return {
        "model": model["name"],
        "model_key": model_key,
        "task": task,
        "status": "ok" if not result.startswith("ERROR") else "error",
        "result": result,
    }


def recommend_model(task: str) -> str:
    """Recommend the best model for a given task when possible."""
    for key, model in MODELS.items():
        if task in model.get("strengths", []):
            if os.environ.get(model["env_key"]):
                return key
    # Fallback: first available model.
    for key, model in MODELS.items():
        if os.environ.get(model["env_key"]):
            return key
    return "claude"


# ──────────────────────────────────────────────────────────────────────────────
# CLI PRINCIPAL
# ──────────────────────────────────────────────────────────────────────────────

def parse_args():
    parser = argparse.ArgumentParser(
        description="MEDIOEVO Orchestrator - Delegate creative tasks to multiple AI models",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=f"""
Available tasks:
{chr(10).join(f'  {k:20s} {v}' for k, v in TASK_TYPES.items())}

Available models:
{chr(10).join(f'  {k:10s} {v["name"]}' for k, v in MODELS.items())}

Examples:
  python orchestrator.py --task revision --input cap01.md --model deepseek
  python orchestrator.py --task synopsis-short --input libro.md --models gpt gemini
  python orchestrator.py --task revision --input cap01.md --model auto
  python orchestrator.py --task custom --input cap01.md --prompt "Analyze the rhythm of the sentences"
        """
    )
    parser.add_argument("--task", required=True, choices=list(TASK_TYPES.keys()))
    parser.add_argument("--input", required=True, help="Input Markdown file")
    parser.add_argument("--model", default="auto",
                        help="Model to use (auto, gpt, claude, gemini, deepseek, grok)")
    parser.add_argument("--models", nargs="+",
                        help="Multiple models (results are written separately)")
    parser.add_argument("--output", help="Output directory for results")
    parser.add_argument("--prompt", help="Custom prompt (only with --task custom)")
    parser.add_argument("--lang", default="en", help="Language of the manuscript")
    parser.add_argument("--saga", default="", help="Saga name")
    parser.add_argument("--book", default="X", help="Book number in the saga")
    parser.add_argument("--total-books", default="N", help="Total number of books in the saga")
    parser.add_argument("--list-tasks", action="store_true", help="List available tasks")
    parser.add_argument("--list-models", action="store_true", help="List models and status")
    return parser.parse_args()


def main():
    args = parse_args()

    if args.list_tasks:
        print("\nAvailable tasks:")
        for k, v in TASK_TYPES.items():
            print(f"  {k:20s} {v}")
        return

    if args.list_models:
        print("\nModels and status:")
        for k, model in MODELS.items():
            key_present = "OK" if os.environ.get(model["env_key"]) else "MISSING API KEY"
            print(f"  {k:10s} {model['name']:20s} {key_present}")
            print(f"           Strengths: {', '.join(model.get('strengths', []))}")
        return

    if not Path(args.input).exists():
        print(f"ERROR: File not found: {args.input}")
        sys.exit(1)

    text = Path(args.input).read_text(encoding="utf-8")
    context = {
        "lang": args.lang,
        "saga": args.saga,
        "book": args.book,
        "total_books": args.total_books,
    }

    if args.models:
        model_keys = args.models
    elif args.model == "auto":
        model_keys = [recommend_model(args.task)]
        print(f"  Recommended model for '{args.task}': {MODELS[model_keys[0]]['name']}")
    else:
        model_keys = [args.model]

    print("\nMEDIOEVO Orchestrator")
    print(f"   Task:   {TASK_TYPES[args.task]}")
    print(f"   Input:  {args.input} ({len(text):,} characters)")
    print(f"   Models: {', '.join(MODELS[k]['name'] for k in model_keys)}\n")

    results = []
    for model_key in model_keys:
        if model_key not in MODELS:
            print(f"  ERROR unknown model: {model_key}")
            continue
        result = run_task(args.task, text, model_key, context, args.prompt)
        results.append(result)

    output_dir = Path(args.output) if args.output else Path("orchestrator_output")
    output_dir.mkdir(parents=True, exist_ok=True)

    print()
    for result in results:
        model_slug = result["model_key"]
        out_file = output_dir / f"{args.task}_{model_slug}.md"

        content = f"# {result['model']} — {TASK_TYPES[args.task]}\n\n"
        content += f"**Input:** {args.input}\n\n---\n\n"
        content += result["result"]

        out_file.write_text(content, encoding="utf-8")
        print(f"  OK {result['model']}: {out_file}")

    if len(results) > 1:
        comparison = output_dir / f"{args.task}_comparison.md"
        comp_content = f"# Comparison: {TASK_TYPES[args.task]}\n\n"
        for result in results:
            comp_content += f"## {result['model']}\n\n{result['result']}\n\n---\n\n"
        comparison.write_text(comp_content, encoding="utf-8")
        print(f"  OK Comparison: {comparison}")


if __name__ == "__main__":
    main()
