from __future__ import annotations

from pathlib import Path
from typing import Any


def transcribe_local(media_path: Path, language: str = "es") -> dict[str, Any]:
    """Best-effort local STT. Never uploads media."""
    try:
        import whisper  # type: ignore

        model = whisper.load_model("base")
        result = model.transcribe(str(media_path), language=language)
        return {
            "ok": True,
            "source": "openai-whisper-local",
            "text": str(result.get("text", "")).strip(),
            "segments": result.get("segments", []),
        }
    except Exception as whisper_exc:
        try:
            from faster_whisper import WhisperModel  # type: ignore

            model = WhisperModel("base", device="cpu", compute_type="int8")
            segments, info = model.transcribe(str(media_path), language=language)
            rows = []
            text_parts = []
            for segment in segments:
                rows.append({"start": segment.start, "end": segment.end, "text": segment.text})
                text_parts.append(segment.text)
            return {
                "ok": True,
                "source": "faster-whisper-local",
                "language": getattr(info, "language", language),
                "text": " ".join(text_parts).strip(),
                "segments": rows,
            }
        except Exception as faster_exc:
            return {
                "ok": False,
                "source": "prompt-caption-fallback",
                "error": f"local_stt_unavailable: whisper={whisper_exc}; faster_whisper={faster_exc}",
                "text": "",
                "segments": [],
            }
