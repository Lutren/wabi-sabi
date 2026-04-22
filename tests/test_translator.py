from pathlib import Path

from kdp import translator


def test_split_into_segments_preserves_code_blocks():
    text = "# Header\n\n```py\nprint('hi')\n```\n\nParagraph"
    segments = translator.split_into_segments(text)

    code_lines = [segment["text"] for segment in segments if not segment.get("translate")]
    assert "```py" in code_lines
    assert "print('hi')" in code_lines


def test_prepare_indigenous_translation_creates_template(tmp_path):
    input_path = tmp_path / "book.md"
    output_path = tmp_path / "book_nah.md"
    input_path.write_text("Line one\n\n# Heading", encoding="utf-8")

    translator.prepare_indigenous_translation(str(input_path), str(output_path), "nah")

    output = output_path.read_text(encoding="utf-8")
    assert "[TRANSLATE: náhuatl]" in output
    assert "<!-- ORIGINAL: Line one -->" in output
