# KDP Publishing Pipeline

**Automatic generation of EPUB, PDF and DOCX from Markdown for Amazon KDP.**

This pipeline supports indigenous languages (including Nahuatl), has been tested with manuscripts up to 180 pages and fixes the most common KDP validation errors.

## Features

- **Input:** Standard Markdown (one file per book or one file per chapter).
- **Output:** EPUB, PDF (Paperback 6x9 in, Hardcover 6.14x9.21 in) and DOCX.
- **Translation:** Optional integration with the DeepL API for translation.
- **Languages:** Support for special characters from Nahuatl and other indigenous languages.
- **Auto-fix:** Corrects negative MediaBox origin in PDFs, a common KDP validation error.
- **Metadata:** Generates complete metadata including title, author, ISBN, language and BISAC codes.

## Requirements

Install the dependencies:

```bash
pip install -r requirements.txt
```

You will also need:

- Python 3.10 or newer.
- Pandoc.
- Ghostscript.
- A DeepL API account for translation.

## Quick usage

### Generate all formats

```bash
python publisher.py --input book.md --all-formats --lang en
```

### Only EPUB

```bash
python publisher.py --input book.md --format epub --lang nah
```

### Translate and generate

```bash
python translator.py --input book_es.md --target en --output book_en.md
python publisher.py --input book_en.md --lang en
```

### Fix PDFs with negative MediaBox

```bash
python publisher.py --input book.md --fix-mediabox
```

## Metadata configuration

Create a `metadata.yaml` file next to your manuscript:

```yaml
title: "Book Title"
author: "Author Name"
language: "en"
isbn: "978-XXXXXXXXXX"
publisher: "Publisher Name"
description: |
  Synopsis up to 4,000 characters for KDP.
bisac:
  - "FIC028000"
  - "FIC028010"
keywords:
  - "science fiction novel"
  - "indie sci-fi saga"
```

## License

Distributed under the MIT license.

The Spanish guide is available as `README_ES.md`.
