from pathlib import Path

from kdp import publisher


def test_ghostscript_binary_prefers_windows_64(monkeypatch):
    monkeypatch.setattr(publisher.sys, "platform", "win32")
    monkeypatch.setattr(
        publisher,
        "check_dependency",
        lambda name: name == "gswin64c",
    )

    assert publisher.ghostscript_binary() == "gswin64c"


def test_fix_pdf_mediabox_uses_selected_binary(monkeypatch, tmp_path):
    pdf_path = tmp_path / "book.pdf"
    pdf_path.write_text("pdf", encoding="utf-8")
    called = {}

    def fake_run(cmd, capture_output, text, check):
        called["cmd"] = cmd
        output_arg = next(part for part in cmd if part.startswith("-sOutputFile="))
        output_path = Path(output_arg.split("=", 1)[1])
        output_path.write_text("fixed", encoding="utf-8")
        return None

    monkeypatch.setattr(publisher, "ghostscript_binary", lambda: "gs-custom")
    monkeypatch.setattr(publisher.subprocess, "run", fake_run)

    assert publisher.fix_pdf_mediabox(str(pdf_path)) is True
    assert called["cmd"][0] == "gs-custom"


def test_prepare_output_dir_sanitizes_title(tmp_path):
    output_dir = publisher.prepare_output_dir(str(tmp_path), "My Book: Draft/01")
    assert output_dir.exists()
    assert output_dir.name.startswith("my_book__draft_01")
