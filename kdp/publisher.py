#!/usr/bin/env python3
"""
MEDIOEVO Publisher
Generate EPUB, paperback PDF, hardcover PDF, and DOCX files from Markdown for Amazon KDP.

Usage:
    python publisher.py --input book.md --metadata metadata.yaml --all-formats
    python publisher.py --input book.md --format epub --lang nah
    python publisher.py --input libro.md --fix-mediabox

License: MIT
"""

import argparse
import subprocess
import shutil
import sys
import os
import re
from pathlib import Path
import yaml


# ──────────────────────────────────────────────────────────────────────────────
# CONFIGURACIÓN POR DEFECTO
# ──────────────────────────────────────────────────────────────────────────────

DEFAULT_CONFIG = {
    "font_size": 12,
    "font_family": "Noto Serif",   # Cobertura amplia incluyendo lenguas indígenas
    "line_height": 1.5,
    "margin_inner": 1.0,
    "margin_outer": 0.75,
    "margin_top": 1.0,
    "margin_bottom": 1.0,
    "paperback_width": "6in",
    "paperback_height": "9in",
    "hardcover_width": "6.14in",
    "hardcover_height": "9.21in",
    "output_dir": "output",
}

# Fuentes recomendadas por lengua para cobertura correcta de caracteres
LANGUAGE_FONTS = {
    "nah": "Noto Serif",        # Náhuatl — saltillo y vocales largas
    "mix": "Noto Serif",        # Mixteco
    "zap": "Noto Serif",        # Zapoteco
    "myn": "Noto Serif",        # Familia Maya
    "es":  "Noto Serif",
    "en":  "Noto Serif",
    "fr":  "Noto Serif",
}


# ──────────────────────────────────────────────────────────────────────────────
# UTILIDADES
# ──────────────────────────────────────────────────────────────────────────────

def check_dependency(name: str) -> bool:
    """Return True when an external tool is available on PATH."""
    return shutil.which(name) is not None


def ghostscript_binary() -> str:
    """Return the preferred Ghostscript executable for the current platform."""
    if sys.platform == "win32":
        return "gswin64c" if check_dependency("gswin64c") else "gswin32c"
    return "ghostscript" if check_dependency("ghostscript") else "gs"


def verify_dependencies(formats: list[str]) -> None:
    """Validate external dependencies required by the selected formats."""
    required = {"pandoc"}
    if any(f in formats for f in ["pdf", "paperback", "hardcover"]):
        required.add(ghostscript_binary())
        required.add("xelatex")

    missing = [dep for dep in required if not check_dependency(dep)]
    if missing:
        print(f"ERROR: Missing dependencies: {', '.join(missing)}")
        print("Install them with:")
        print("  Ubuntu/Debian: sudo apt install pandoc ghostscript texlive-xetex")
        print("  macOS: brew install pandoc ghostscript mactex")
        print("  Windows: install Pandoc, Ghostscript, and XeLaTeX / TeX Live")
        sys.exit(1)


def load_metadata(path: str | None) -> dict:
    """Carga metadata desde YAML o devuelve defaults vacíos."""
    if path is None or not Path(path).exists():
        return {}
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def load_config(path: str | None) -> dict:
    """Carga configuración con fallback a defaults."""
    config = DEFAULT_CONFIG.copy()
    if path and Path(path).exists():
        with open(path, "r", encoding="utf-8") as f:
            user_config = yaml.safe_load(f) or {}
        config.update(user_config)
    return config


def prepare_output_dir(base: str, title: str) -> Path:
    """Crea el directorio de salida."""
    safe_title = re.sub(r"[^\w\-]", "_", title.lower())[:40]
    out = Path(base) / safe_title
    out.mkdir(parents=True, exist_ok=True)
    return out


# ──────────────────────────────────────────────────────────────────────────────
# GENERACIÓN DE EPUB
# ──────────────────────────────────────────────────────────────────────────────

def generate_epub(input_path: str, output_path: str, metadata: dict, config: dict, lang: str) -> bool:
    """Genera EPUB con Pandoc."""
    font = LANGUAGE_FONTS.get(lang, "Noto Serif")
    title = metadata.get("title", Path(input_path).stem)
    author = metadata.get("author", "Unknown author")
    language = metadata.get("language", lang)

    cmd = [
        "pandoc", input_path,
        "-o", output_path,
        "--epub-chapter-level=1",
        f"--metadata=title:{title}",
        f"--metadata=author:{author}",
        f"--metadata=lang:{language}",
    ]

    if metadata.get("isbn"):
        cmd.append(f"--metadata=identifier:isbn:{metadata['isbn']}")

    # CSS inline para EPUB
    epub_css = generate_epub_css(config, font)
    css_path = Path(output_path).with_suffix(".css")
    css_path.write_text(epub_css, encoding="utf-8")
    cmd.extend(["--css", str(css_path)])

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        print(f"  OK EPUB generated: {output_path}")
        css_path.unlink(missing_ok=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"  ERROR generating EPUB:\n{e.stderr}")
        return False


def generate_epub_css(config: dict, font: str) -> str:
    """Generate KDP-friendly EPUB CSS."""
    return f"""
body {{
    font-family: "{font}", serif;
    font-size: {config['font_size']}pt;
    line-height: {config['line_height']};
    margin: 5%;
    text-align: justify;
    hyphens: auto;
}}
h1 {{ font-size: 1.6em; text-align: center; margin: 2em 0 1em; }}
h2 {{ font-size: 1.3em; margin: 1.5em 0 0.8em; }}
p {{ margin: 0; text-indent: 1.5em; }}
p:first-child, h1 + p, h2 + p {{ text-indent: 0; }}
blockquote {{ margin: 1em 2em; font-style: italic; }}
"""


# ──────────────────────────────────────────────────────────────────────────────
# GENERACIÓN DE PDF
# ──────────────────────────────────────────────────────────────────────────────

def generate_pdf(
    input_path: str,
    output_path: str,
    metadata: dict,
    config: dict,
    lang: str,
    size: str = "paperback",
    fix_mediabox: bool = False,
) -> bool:
    """Generate a PDF through Pandoc and XeLaTeX."""
    font = LANGUAGE_FONTS.get(lang, "Noto Serif")
    title = metadata.get("title", Path(input_path).stem)
    author = metadata.get("author", "")

    width = config["paperback_width"] if size == "paperback" else config["hardcover_width"]
    height = config["paperback_height"] if size == "paperback" else config["hardcover_height"]

    variables = [
        f"geometry:paperwidth={width},paperheight={height},"
        f"inner={config['margin_inner']}in,outer={config['margin_outer']}in,"
        f"top={config['margin_top']}in,bottom={config['margin_bottom']}in",
        f"mainfont:{font}",
        f"fontsize:{config['font_size']}pt",
        "documentclass:book",
    ]

    cmd = ["pandoc", input_path, "-o", output_path, "--pdf-engine=xelatex"]
    for var in variables:
        cmd.extend(["-V", var])
    cmd.extend([
        f"--metadata=title:{title}",
        f"--metadata=author:{author}",
    ])

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        print(f"  OK PDF ({size}) generated: {output_path}")

        if fix_mediabox:
            fixed = fix_pdf_mediabox(output_path)
            if fixed:
                print("  OK MediaBox normalized")

        return True
    except subprocess.CalledProcessError as e:
        print(f"  ERROR generating PDF ({size}):\n{e.stderr}")
        return False


def fix_pdf_mediabox(pdf_path: str) -> bool:
    """
    Fix the KDP error "PDF has a negative MediaBox origin".
    Uses Ghostscript to recompress and normalize the PDF.
    """
    tmp_path = pdf_path + ".tmp.pdf"
    gs_binary = ghostscript_binary()
    gs_cmd = [
        gs_binary,
        "-dBATCH", "-dNOPAUSE", "-dQUIET",
        "-sDEVICE=pdfwrite",
        "-dCompatibilityLevel=1.4",
        "-dPDFSETTINGS=/prepress",
        f"-sOutputFile={tmp_path}",
        pdf_path,
    ]
    try:
        subprocess.run(gs_cmd, capture_output=True, text=True, check=True)
        shutil.move(tmp_path, pdf_path)
        return True
    except subprocess.CalledProcessError as e:
        print(f"  ERROR running fix_mediabox:\n{e.stderr}")
        Path(tmp_path).unlink(missing_ok=True)
        return False


# ──────────────────────────────────────────────────────────────────────────────
# GENERACIÓN DE DOCX
# ──────────────────────────────────────────────────────────────────────────────

def generate_docx(input_path: str, output_path: str, metadata: dict) -> bool:
    """Generate a DOCX file with Pandoc."""
    title = metadata.get("title", Path(input_path).stem)
    author = metadata.get("author", "")

    cmd = [
        "pandoc", input_path,
        "-o", output_path,
        f"--metadata=title:{title}",
        f"--metadata=author:{author}",
    ]

    try:
        subprocess.run(cmd, capture_output=True, text=True, check=True)
        print(f"  OK DOCX generated: {output_path}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"  ERROR generating DOCX:\n{e.stderr}")
        return False


# ──────────────────────────────────────────────────────────────────────────────
# VALIDACIÓN EPUB
# ──────────────────────────────────────────────────────────────────────────────

def validate_epub(epub_path: str) -> bool:
    """Validate an EPUB with epubcheck if available."""
    if not check_dependency("epubcheck"):
        print("  INFO epubcheck not installed - skipping validation")
        print("    Install: https://github.com/w3c/epubcheck")
        return True

    try:
        result = subprocess.run(
            ["epubcheck", epub_path],
            capture_output=True, text=True
        )
        if result.returncode == 0:
            print("  OK valid EPUB (epubcheck)")
            return True
        else:
            print("  ERROR EPUB validation issues:")
            for line in result.stdout.splitlines():
                if "ERROR" in line or "WARNING" in line:
                    print(f"    {line}")
            return False
    except Exception as e:
        print(f"  ERROR running epubcheck: {e}")
        return False


# ──────────────────────────────────────────────────────────────────────────────
# CLI PRINCIPAL
# ──────────────────────────────────────────────────────────────────────────────

def parse_args():
    parser = argparse.ArgumentParser(
        description="MEDIOEVO Publisher - Generate KDP formats from Markdown",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python publisher.py --input book.md --all-formats
  python publisher.py --input book.md --format epub --lang nah
  python publisher.py --input book.md --fix-mediabox
  python publisher.py --input book.md --metadata meta.yaml --all-formats
        """
    )
    parser.add_argument("--input", required=True, help="Input Markdown file")
    parser.add_argument("--metadata", help="YAML file with book metadata")
    parser.add_argument("--config", help="YAML configuration file")
    parser.add_argument("--lang", default="es", help="BCP-47 language code (es, en, nah...)")
    parser.add_argument("--format", choices=["epub", "paperback", "hardcover", "docx"],
                        help="Generate only this format")
    parser.add_argument("--all-formats", action="store_true", help="Generate all formats")
    parser.add_argument("--fix-mediabox", action="store_true",
                        help="Normalize negative MediaBox values in PDFs (KDP error)")
    parser.add_argument("--validate-epub", action="store_true",
                        help="Validate EPUB with epubcheck after generation")
    parser.add_argument("--output-dir", default="output", help="Output directory")
    return parser.parse_args()


def main():
    args = parse_args()

    if not Path(args.input).exists():
        print(f"ERROR: File not found: {args.input}")
        sys.exit(1)

    config = load_config(args.config)
    config["output_dir"] = args.output_dir
    metadata = load_metadata(args.metadata)

    formats = []
    if args.all_formats:
        formats = ["epub", "paperback", "hardcover", "docx"]
    elif args.format:
        formats = [args.format]
    else:
        formats = ["epub"]

    verify_dependencies(formats)

    title = metadata.get("title", Path(args.input).stem)
    out_dir = prepare_output_dir(config["output_dir"], title)
    base_name = Path(args.input).stem

    print("\nMEDIOEVO Publisher")
    print(f"   Input:  {args.input}")
    print(f"   Language: {args.lang}")
    print(f"   Output: {out_dir}/")
    print(f"   Formats: {', '.join(formats)}\n")

    results = {}

    if "epub" in formats:
        epub_path = str(out_dir / f"{base_name}.epub")
        results["epub"] = generate_epub(args.input, epub_path, metadata, config, args.lang)
        if results["epub"] and args.validate_epub:
            validate_epub(epub_path)

    if "paperback" in formats:
        pdf_path = str(out_dir / f"{base_name}_paperback.pdf")
        results["paperback"] = generate_pdf(
            args.input, pdf_path, metadata, config, args.lang,
            size="paperback", fix_mediabox=args.fix_mediabox
        )

    if "hardcover" in formats:
        pdf_path = str(out_dir / f"{base_name}_hardcover.pdf")
        results["hardcover"] = generate_pdf(
            args.input, pdf_path, metadata, config, args.lang,
            size="hardcover", fix_mediabox=args.fix_mediabox
        )

    if "docx" in formats:
        docx_path = str(out_dir / f"{base_name}.docx")
        results["docx"] = generate_docx(args.input, docx_path, metadata)

    print()
    successes = sum(1 for v in results.values() if v)
    total = len(results)
    print(f"OK {successes}/{total} formats generated in: {out_dir}/")

    if successes < total:
        sys.exit(1)


if __name__ == "__main__":
    main()
