#!/usr/bin/env python3
"""
MEDIOEVO Translator
Translate Markdown manuscripts with the DeepL API while preserving formatting.

Usage:
    python translator.py --input book_es.md --target en --output book_en.md
    python translator.py --input book_es.md --target nah  # manual template for indigenous languages

Environment variables:
    DEEPL_API_KEY - DeepL API key (https://www.deepl.com/api)

License: MIT
"""

import argparse
import os
import sys
import re
import time
from pathlib import Path


# ──────────────────────────────────────────────────────────────────────────────
# INSTALACIÓN CONDICIONAL DE DEEPL
# ──────────────────────────────────────────────────────────────────────────────

try:
    import deepl
    DEEPL_AVAILABLE = True
except ImportError:
    DEEPL_AVAILABLE = False


def ensure_deepl():
    if not DEEPL_AVAILABLE:
        print("ERROR: deepl is not installed.")
        print("  pip install deepl")
        sys.exit(1)


# ──────────────────────────────────────────────────────────────────────────────
# LENGUAS SOPORTADAS
# ──────────────────────────────────────────────────────────────────────────────

# Languages supported by DeepL.
DEEPL_LANGUAGES = {
    "en": "EN-US",
    "en-gb": "EN-GB",
    "es": "ES",
    "fr": "FR",
    "de": "DE",
    "it": "IT",
    "pt": "PT-BR",
    "pt-pt": "PT-PT",
    "ru": "RU",
    "ja": "JA",
    "zh": "ZH",
    "ko": "KO",
    "nl": "NL",
    "pl": "PL",
    "tr": "TR",
}

# Indigenous languages are not supported directly by DeepL.
# The script can still prepare a manual translation template.
INDIGENOUS_LANGUAGES = {
    "nah": "náhuatl",
    "mix": "mixteco",
    "zap": "zapoteco",
    "myn": "maya",
    "otm": "otomí",
    "tzh": "tzeltal",
    "tzo": "tzotzil",
}


# ──────────────────────────────────────────────────────────────────────────────
# PRESERVACIÓN DE FORMATO MARKDOWN
# ──────────────────────────────────────────────────────────────────────────────

# Markdown patterns that should not be translated.
PROTECTED_PATTERNS = [
    (r"^(#{1,6}\s)", "header"),           # Headers
    (r"`[^`]+`", "inline_code"),          # Código inline
    (r"```[\s\S]*?```", "code_block"),    # Bloques de código
    (r"\[([^\]]+)\]\([^\)]+\)", "link"),  # Links (preservar URL)
    (r"!\[([^\]]*)\]\([^\)]+\)", "img"),  # Imágenes
    (r"^\s*[-*+]\s", "list_item"),        # Listas
    (r"^\s*\d+\.\s", "ordered_list"),     # Listas numeradas
    (r"^>\s", "blockquote"),              # Blockquotes
    (r"\*\*([^*]+)\*\*", "bold"),         # Bold
    (r"\*([^*]+)\*", "italic"),           # Italic
    (r"^---$", "hr"),                     # Línea horizontal
]


def split_into_segments(text: str) -> list[dict]:
    """
    Split input into translatable and non-translatable segments.
    Preserve Markdown structure.
    """
    segments = []
    lines = text.split("\n")

    in_code_block = False

    for line in lines:
        if line.strip().startswith("```"):
            in_code_block = not in_code_block
            segments.append({"text": line, "translate": False})
            continue

        if in_code_block:
            segments.append({"text": line, "translate": False})
            continue

        if not line.strip():
            segments.append({"text": line, "translate": False})
            continue

        header_match = re.match(r"^(#{1,6}\s)(.*)", line)
        if header_match:
            segments.append({
                "text": header_match.group(1),
                "translate": False
            })
            segments.append({
                "text": header_match.group(2),
                "translate": True
            })
            segments.append({"text": "", "translate": False, "newline": True})
            continue

        if re.match(r"^(---|\*\*\*|___)$", line.strip()):
            segments.append({"text": line, "translate": False})
            continue

        segments.append({"text": line, "translate": True})

    return segments


def reassemble(segments: list[dict]) -> str:
    """Reassemble segments back into Markdown text."""
    lines = []
    i = 0
    while i < len(segments):
        seg = segments[i]
        if seg.get("newline"):
            i += 1
            continue
        lines.append(seg["text"])
        i += 1
    return "\n".join(lines)


# ──────────────────────────────────────────────────────────────────────────────
# TRADUCCIÓN CON DEEPL
# ──────────────────────────────────────────────────────────────────────────────

class MedioevoTranslator:
    def __init__(self, api_key: str, target_lang: str, source_lang: str = "ES"):
        ensure_deepl()
        self.translator = deepl.Translator(api_key)
        self.target_lang = DEEPL_LANGUAGES.get(target_lang.lower(), target_lang.upper())
        self.source_lang = DEEPL_LANGUAGES.get(source_lang.lower(), source_lang.upper())
        self.request_count = 0
        self.delay_between_requests = 0.1

    def translate_batch(self, texts: list[str]) -> list[str]:
        """Translate a batch of texts while preserving order."""
        if not texts:
            return []
        try:
            results = self.translator.translate_text(
                texts,
                source_lang=self.source_lang,
                target_lang=self.target_lang,
                preserve_formatting=True,
            )
            self.request_count += 1
            time.sleep(self.delay_between_requests)
            return [r.text for r in results]
        except Exception as e:
            print(f"\n  ERROR during translation: {e}")
            return texts

    def translate_markdown(self, text: str, batch_size: int = 50) -> str:
        """
        Translate a Markdown manuscript while preserving formatting.
        The work is processed in batches for efficiency.
        """
        segments = split_into_segments(text)

        translatable_indices = [
            i for i, seg in enumerate(segments)
            if seg.get("translate") and seg["text"].strip()
        ]

        total = len(translatable_indices)
        print(f"  Segments to translate: {total}")

        for batch_start in range(0, total, batch_size):
            batch_indices = translatable_indices[batch_start:batch_start + batch_size]
            batch_texts = [segments[i]["text"] for i in batch_indices]

            translated = self.translate_batch(batch_texts)

            for idx, translated_text in zip(batch_indices, translated):
                segments[idx]["text"] = translated_text

            progress = min(batch_start + batch_size, total)
            print(f"  Progress: {progress}/{total} segments", end="\r")

        print()
        return reassemble(segments)

    def check_usage(self):
        """Display the current DeepL API usage when available."""
        try:
            usage = self.translator.get_usage()
            print(f"\n  DeepL usage: {usage.character.count:,} / {usage.character.limit:,} characters")
        except Exception:
            pass


# ──────────────────────────────────────────────────────────────────────────────
# LENGUAS INDÍGENAS — MODO MANUAL
# ──────────────────────────────────────────────────────────────────────────────

def prepare_indigenous_translation(input_path: str, output_path: str, lang: str) -> None:
    """
    For languages not supported by DeepL (Nahuatl, etc.), generate
    an interleaved template with the original and space for manual translation.
    """
    lang_name = INDIGENOUS_LANGUAGES.get(lang, lang)
    text = Path(input_path).read_text(encoding="utf-8")
    lines = text.split("\n")

    output_lines = [
        f"<!-- TRADUCCIÓN A {lang_name.upper()} ({lang}) -->",
        f"<!-- File generated by MEDIOEVO Translator -->",
        f"<!-- Replace each [TRANSLATE] line with the correct translation -->",
        "",
    ]

    for line in lines:
        if line.strip() and not line.startswith("#") and not line.startswith("```"):
            output_lines.append(f"<!-- ORIGINAL: {line} -->")
            output_lines.append(f"[TRANSLATE: {lang_name}]")
        else:
            output_lines.append(line)

    Path(output_path).write_text("\n".join(output_lines), encoding="utf-8")
    print(f"  OK manual translation template generated: {output_path}")
    print(f"  INFO DeepL does not support {lang_name}. Use this template with a native speaker.")


# ──────────────────────────────────────────────────────────────────────────────
# CLI PRINCIPAL
# ──────────────────────────────────────────────────────────────────────────────

def parse_args():
    parser = argparse.ArgumentParser(
        description="MEDIOEVO Translator - Translate Markdown manuscripts with DeepL",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python translator.py --input book_es.md --target en
  python translator.py --input book_es.md --target en --output book_en.md
  python translator.py --input book_es.md --target nah  # generates a manual template
  python translator.py --input book_es.md --target fr --check-usage

Available DeepL languages:
  en, es, fr, de, it, pt, ru, ja, zh, ko, nl, pl, tr

Indigenous languages (manual template mode):
  nah (náhuatl), mix (mixteco), zap (zapoteco), myn (maya), otm (otomí)
        """
    )
    parser.add_argument("--input", required=True, help="Input Markdown file")
    parser.add_argument("--target", required=True, help="Target language (BCP-47 code)")
    parser.add_argument("--source", default="es", help="Source language (default: es)")
    parser.add_argument("--output", help="Output file (default: input_TARGET.md)")
    parser.add_argument("--api-key", help="DeepL API key (or use DEEPL_API_KEY)")
    parser.add_argument("--batch-size", type=int, default=50,
                        help="Batch size for translation (default: 50)")
    parser.add_argument("--check-usage", action="store_true",
                        help="Show current DeepL API usage")
    return parser.parse_args()


def main():
    args = parse_args()

    if not Path(args.input).exists():
        print(f"ERROR: File not found: {args.input}")
        sys.exit(1)

    target = args.target.lower()

    if args.output:
        output_path = args.output
    else:
        stem = Path(args.input).stem
        output_path = str(Path(args.input).parent / f"{stem}_{target}.md")

    print("\nMEDIOEVO Translator")
    print(f"   Input:  {args.input}")
    print(f"   Target: {target}")
    print(f"   Output: {output_path}\n")

    if target in INDIGENOUS_LANGUAGES:
        prepare_indigenous_translation(args.input, output_path, target)
        return

    if target not in DEEPL_LANGUAGES:
        print(f"ERROR: Language not supported by DeepL: {target}")
        print(f"Available languages: {', '.join(DEEPL_LANGUAGES.keys())}")
        print(f"Indigenous languages (manual template): {', '.join(INDIGENOUS_LANGUAGES.keys())}")
        sys.exit(1)

    api_key = args.api_key or os.environ.get("DEEPL_API_KEY")
    if not api_key:
        print("ERROR: DeepL API key not found.")
        print("  Option 1: --api-key YOUR_KEY")
        print("  Option 2: export DEEPL_API_KEY=YOUR_KEY")
        print("  Get a key: https://www.deepl.com/api")
        sys.exit(1)

    ensure_deepl()
    translator = MedioevoTranslator(api_key, target, args.source)

    if args.check_usage:
        translator.check_usage()

    text = Path(args.input).read_text(encoding="utf-8")
    print(f"  Source text: {len(text):,} characters")

    translated = translator.translate_markdown(text, batch_size=args.batch_size)

    Path(output_path).write_text(translated, encoding="utf-8")
    print(f"  OK translation saved: {output_path}")
    print(f"  DeepL requests: {translator.request_count}")

    if args.check_usage:
        translator.check_usage()


if __name__ == "__main__":
    main()
