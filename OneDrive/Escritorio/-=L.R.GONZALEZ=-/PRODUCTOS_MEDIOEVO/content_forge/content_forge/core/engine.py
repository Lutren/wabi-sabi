from __future__ import annotations

import json
import os
import time
from pathlib import Path
from typing import Any

from ..catalog.assets_catalog import build_asset_catalog
from ..history.trends import load_historical_context
from ..media.assets import create_placeholder_image, select_image_assets, select_music_asset
from ..media.captions import cues_from_text, write_srt, write_vtt
from ..media.ffmpeg import (
    concat_videos,
    create_preview,
    create_thumbnail,
    find_executable,
    probe_media,
    render_image_clip,
    render_video_source,
)
from ..media.transcribe import transcribe_local
from ..media.visual_qa import analyze_video_frame, write_visual_qa
from ..publish.queue import enqueue_publish_request
from .job_store import JobStore
from .metrics import StageMetricsStore
from .models import PRESETS, ForgePaths, as_path_list, normalize_preset
from .observacionismo_state import JobState, ObservacionismoMonitor


class ContentForgeEngine:
    def __init__(
        self,
        product_root: Path | None = None,
        output_root: Path | None = None,
        medioevo_root: Path | None = None,
    ) -> None:
        resolved_product = Path(product_root or Path(__file__).resolve().parents[2]).resolve()
        resolved_medioevo = discover_medioevo_root(resolved_product, medioevo_root)
        claudio_root = resolved_medioevo / "claudio" if resolved_medioevo and (resolved_medioevo / "claudio").exists() else None
        runtime_root = Path(output_root).resolve() if output_root else resolved_product / "runtime" / "content_forge"
        self.paths = ForgePaths(
            product_root=resolved_product,
            runtime_root=runtime_root,
            jobs_root=runtime_root / "jobs",
            medioevo_root=resolved_medioevo,
            claudio_root=claudio_root,
        )
        self.store = JobStore(self.paths.jobs_root)
        self.metrics = StageMetricsStore(self.paths.runtime_root / "stage_metrics.jsonl")

    def health(self) -> dict[str, Any]:
        ffmpeg_ok = True
        ffprobe_ok = True
        ffmpeg_error = ""
        try:
            ffmpeg_path = find_executable("ffmpeg")
        except Exception as exc:
            ffmpeg_ok = False
            ffmpeg_path = ""
            ffmpeg_error = str(exc)
        try:
            ffprobe_path = find_executable("ffprobe")
        except Exception as exc:
            ffprobe_ok = False
            ffprobe_path = ""
            ffmpeg_error = (ffmpeg_error + "; " + str(exc)).strip("; ")
        return {
            "ok": ffmpeg_ok and ffprobe_ok,
            "product_root": str(self.paths.product_root),
            "runtime_root": str(self.paths.runtime_root),
            "jobs_root": str(self.paths.jobs_root),
            "medioevo_root": str(self.paths.medioevo_root) if self.paths.medioevo_root else None,
            "claudio_root": str(self.paths.claudio_root) if self.paths.claudio_root else None,
            "ffmpeg": {"ok": ffmpeg_ok, "path": ffmpeg_path},
            "ffprobe": {"ok": ffprobe_ok, "path": ffprobe_path},
            "error": ffmpeg_error,
            "voice_clone": "disabled_by_default",
            "publication": "queue_requires_human_approval",
            "metrics": {
                "path": str(self.metrics.metrics_path),
                "learned_thresholds": self.metrics.learned_thresholds(),
            },
        }

    def asset_catalog(self, max_items: int = 500) -> dict[str, Any]:
        return build_asset_catalog(self.paths.medioevo_root, self.paths.product_root, max_items=max_items)

    def render(self, request: dict[str, Any]) -> dict[str, Any]:
        job_id, job_dir, manifest = self.store.create("render", request)
        monitor = ObservacionismoMonitor(job_dir, thresholds=self.metrics.learned_thresholds())
        try:
            monitor.transition(JobState.OBSERVANDO, "collecting local inputs")
            preset_name = normalize_preset(str(request.get("format") or request.get("preset") or "shorts"))
            preset = PRESETS[preset_name]
            duration = clamp_float(request.get("duration"), 5.0, 90.0, 8.0)
            prompt = str(request.get("prompt") or request.get("title") or "MEDIOEVO").strip()
            platforms = normalize_platforms(request.get("platforms"))
            assets = select_image_assets(self.paths.medioevo_root, as_path_list(request.get("assets")), limit=1)
            music = select_music_asset(self.paths.medioevo_root, Path(str(request["music"])) if request.get("music") else None)
            video_source = Path(str(request["video"])).expanduser() if request.get("video") else None
            manifest.update(
                {
                    "state": JobState.OBSERVANDO.value,
                    "preset": {"name": preset_name, **preset},
                    "duration": duration,
                    "voice_clone": "disabled_by_default",
                    "trends": load_historical_context(self.paths.medioevo_root, self.paths.claudio_root),
                }
            )
            self.store.save(job_dir, manifest)

            if video_source is None and not assets:
                placeholder = create_placeholder_image(job_dir / "inputs" / "medioevo_placeholder.ppm", prompt)
                assets = [placeholder]
                manifest["warnings"].append("no_public_image_asset_found_generated_placeholder")
            if video_source is not None and not video_source.exists():
                raise FileNotFoundError(f"Video source not found: {video_source}")

            monitor.transition(JobState.PLANIFICANDO, "building captions and render plan")
            text = str(request.get("transcript") or "")
            stt_result = {"ok": False, "source": "not_requested", "text": ""}
            if not text and video_source and bool(request.get("transcribe", False)):
                stt_result = transcribe_local(video_source, language=str(request.get("language", "es")))
                text = str(stt_result.get("text") or "")
            if not text:
                text = prompt
            cues = cues_from_text(text, duration)
            srt_path = write_srt(cues, job_dir / "captions" / "captions.srt")
            vtt_path = write_vtt(cues, job_dir / "captions" / "captions.vtt")
            manifest["artifacts"].update({"srt": str(srt_path), "vtt": str(vtt_path)})
            manifest["stt"] = stt_result
            self.store.save(job_dir, manifest)

            monitor.transition(JobState.RENDERIZANDO, "rendering mp4")
            final_path = job_dir / "final" / f"{job_id}.mp4"
            burn = bool(request.get("burn_subtitles", False) or request.get("burn", False))
            if video_source:
                _, warnings = render_video_source(
                    video=video_source,
                    output=final_path,
                    width=int(preset["width"]),
                    height=int(preset["height"]),
                    duration=duration,
                    fps=int(preset["fps"]),
                    log_path=job_dir / "logs" / "ffmpeg_render.log",
                    job_dir=job_dir,
                    start=clamp_float(request.get("start"), 0.0, 99999.0, 0.0),
                    cut_silence=bool(request.get("cut_silence", False)),
                    srt_relative="captions/captions.srt" if burn else None,
                )
            else:
                _, warnings = render_image_clip(
                    image=assets[0],
                    output=final_path,
                    width=int(preset["width"]),
                    height=int(preset["height"]),
                    duration=duration,
                    fps=int(preset["fps"]),
                    log_path=job_dir / "logs" / "ffmpeg_render.log",
                    job_dir=job_dir,
                    srt_relative="captions/captions.srt" if burn else None,
                    music=music,
                )
            manifest["warnings"].extend(warnings)
            manifest["artifacts"]["final_mp4"] = str(final_path)
            monitor.progress("render complete", final=str(final_path))

            self._finish_media_job(job_dir, manifest, final_path, duration, platforms, monitor)
            return manifest
        except Exception as exc:
            monitor.transition(JobState.FALLIDO, "job failed", error=str(exc))
            manifest["ok"] = False
            manifest["state"] = JobState.FALLIDO.value
            manifest["error"] = str(exc)
            manifest["metrics"] = self.metrics.record_job(job_dir, manifest)
            self.store.save(job_dir, manifest)
            return manifest

    def carousel(self, request: dict[str, Any]) -> dict[str, Any]:
        job_id, job_dir, manifest = self.store.create("carousel", request)
        monitor = ObservacionismoMonitor(job_dir, thresholds=self.metrics.learned_thresholds())
        try:
            monitor.transition(JobState.OBSERVANDO, "collecting carousel assets")
            preset_name = normalize_preset(str(request.get("format") or request.get("preset") or "reel"))
            preset = PRESETS[preset_name]
            duration_per_slide = clamp_float(request.get("duration_per_slide"), 1.0, 12.0, 2.0)
            prompt = str(request.get("prompt") or request.get("title") or "MEDIOEVO").strip()
            platforms = normalize_platforms(request.get("platforms"))
            assets = select_image_assets(self.paths.medioevo_root, as_path_list(request.get("assets")), limit=5)
            if len(assets) < 3:
                for index in range(len(assets), 3):
                    assets.append(create_placeholder_image(job_dir / "inputs" / f"medioevo_slide_{index + 1}.ppm", prompt, index=index))
                manifest["warnings"].append("not_enough_public_image_assets_generated_placeholders")
            assets = assets[:5]
            total_duration = duration_per_slide * len(assets)
            manifest.update(
                {
                    "state": JobState.OBSERVANDO.value,
                    "preset": {"name": preset_name, **preset},
                    "duration": total_duration,
                    "slide_count": len(assets),
                    "assets": [str(path) for path in assets],
                    "voice_clone": "disabled_by_default",
                    "trends": load_historical_context(self.paths.medioevo_root, self.paths.claudio_root),
                }
            )
            self.store.save(job_dir, manifest)

            monitor.transition(JobState.PLANIFICANDO, "building carousel captions")
            cues = cues_from_text(str(request.get("transcript") or prompt), total_duration)
            srt_path = write_srt(cues, job_dir / "captions" / "captions.srt")
            vtt_path = write_vtt(cues, job_dir / "captions" / "captions.vtt")
            manifest["artifacts"].update({"srt": str(srt_path), "vtt": str(vtt_path)})
            self.store.save(job_dir, manifest)

            monitor.transition(JobState.RENDERIZANDO, "rendering carousel slides")
            parts: list[Path] = []
            for index, asset in enumerate(assets, start=1):
                part = job_dir / "work" / f"slide_{index:02}.mp4"
                render_image_clip(
                    image=asset,
                    output=part,
                    width=int(preset["width"]),
                    height=int(preset["height"]),
                    duration=duration_per_slide,
                    fps=int(preset["fps"]),
                    log_path=job_dir / "logs" / f"ffmpeg_slide_{index:02}.log",
                    job_dir=job_dir,
                    srt_relative=None,
                    music=None,
                )
                parts.append(part)
                monitor.progress("slide rendered", index=index, total=len(assets))
            final_path = job_dir / "final" / f"{job_id}.mp4"
            concat_videos(parts, final_path, job_dir / "work" / "concat.txt", job_dir / "logs" / "ffmpeg_concat.log")
            manifest["artifacts"]["final_mp4"] = str(final_path)
            self._finish_media_job(job_dir, manifest, final_path, total_duration, platforms, monitor)
            return manifest
        except Exception as exc:
            monitor.transition(JobState.FALLIDO, "job failed", error=str(exc))
            manifest["ok"] = False
            manifest["state"] = JobState.FALLIDO.value
            manifest["error"] = str(exc)
            manifest["metrics"] = self.metrics.record_job(job_dir, manifest)
            self.store.save(job_dir, manifest)
            return manifest

    def status(self, job_id: str | None = None, limit: int = 20) -> dict[str, Any]:
        if job_id:
            try:
                return {"ok": True, "job": self.store.load(job_id)}
            except (FileNotFoundError, ValueError) as exc:
                return {"ok": False, "error": str(exc)}
        return {"ok": True, "jobs": self.store.latest(limit=limit)}

    def simulate_stall(self, job_id: str | None = None) -> dict[str, Any]:
        if job_id:
            job_dir = self.store.job_dir(job_id)
            manifest = self.store.load(job_id)
        else:
            job_id, job_dir, manifest = self.store.create("stall_simulation", {"prompt": "stall simulation"})
        monitor = ObservacionismoMonitor(job_dir, thresholds={JobState.RENDERIZANDO.value: 0.01})
        monitor.transition(JobState.RENDERIZANDO, "simulated long render")
        time.sleep(0.02)
        status = monitor.mark_stalled_if_needed()
        manifest["state"] = JobState.ATASCADO.value if status["stalled"] else monitor.state
        manifest["stall_check"] = status
        manifest["metrics"] = self.metrics.record_job(job_dir, manifest)
        self.store.save(job_dir, manifest)
        return manifest

    def _finish_media_job(
        self,
        job_dir: Path,
        manifest: dict[str, Any],
        final_path: Path,
        duration: float,
        platforms: list[str],
        monitor: ObservacionismoMonitor,
    ) -> None:
        monitor.transition(JobState.QA, "probing final media")
        thumb_path = create_thumbnail(final_path, job_dir / "thumbnails" / "thumbnail.jpg", job_dir / "logs" / "ffmpeg_thumbnail.log")
        preview_path = create_preview(final_path, job_dir / "preview" / "preview.mp4", duration, job_dir / "logs" / "ffmpeg_preview.log")
        qa = probe_media(final_path, log_path=job_dir / "logs" / "ffprobe_final.log")
        (job_dir / "qa.json").write_text(json.dumps(qa, indent=2, ensure_ascii=False), encoding="utf-8")
        visual_qa = analyze_video_frame(final_path, job_dir / "work" / "visual_qa_frame.ppm", job_dir / "logs" / "ffmpeg_visual_qa.log")
        visual_qa_path = write_visual_qa(job_dir / "visual_qa.json", visual_qa)
        manifest["artifacts"].update(
            {
                "thumbnail": str(thumb_path),
                "preview_mp4": str(preview_path),
                "qa": str(job_dir / "qa.json"),
                "visual_qa": str(visual_qa_path),
            }
        )
        manifest["qa_summary"] = summarize_probe(qa)
        manifest["visual_qa_summary"] = {
            "ok": bool(visual_qa.get("ok")),
            "nonblank": bool(visual_qa.get("nonblank")),
            "contrast_ok": bool(visual_qa.get("contrast_ok")),
            "sample_variance": visual_qa.get("sample_variance"),
        }
        if not visual_qa.get("ok"):
            manifest["warnings"].append("visual_qa_frame_needs_review")
        publish_entry = enqueue_publish_request(self.paths.runtime_root, manifest, platforms)
        manifest["publish_queue"] = publish_entry
        manifest["state"] = JobState.REQUIERE_APROBACION.value
        monitor.transition(JobState.REQUIERE_APROBACION, "package ready and waiting for publication approval")
        manifest["ok"] = True
        manifest["metrics"] = self.metrics.record_job(job_dir, manifest)
        self.store.save(job_dir, manifest)


def discover_medioevo_root(product_root: Path, explicit: Path | None = None) -> Path | None:
    candidates: list[Path] = []
    if explicit:
        candidates.append(explicit)
    env = os.getenv("MEDIOEVO_ROOT")
    if env:
        candidates.append(Path(env))
    candidates.extend(
        [
            product_root.parent.parent / "-=MEDIOEVO=-" / "-=LIBROS",
            Path.home() / "OneDrive" / "Escritorio" / "-=L.R.GONZALEZ=-" / "-=MEDIOEVO=-" / "-=LIBROS",
        ]
    )
    for candidate in candidates:
        if candidate.exists():
            return candidate.resolve()
    return None


def clamp_float(value: Any, minimum: float, maximum: float, default: float) -> float:
    try:
        number = float(value)
    except Exception:
        number = default
    return max(minimum, min(maximum, number))


def normalize_platforms(value: Any) -> list[str]:
    if not value:
        return []
    if isinstance(value, str):
        value = [part.strip() for part in value.split(",")]
    return [str(item).strip().lower() for item in value if str(item).strip()]


def summarize_probe(qa: dict[str, Any]) -> dict[str, Any]:
    video = next((stream for stream in qa.get("streams", []) if stream.get("codec_type") == "video"), {})
    audio = next((stream for stream in qa.get("streams", []) if stream.get("codec_type") == "audio"), {})
    fmt = qa.get("format", {})
    return {
        "duration": float(fmt.get("duration", 0.0) or 0.0),
        "size": int(fmt.get("size", 0) or 0),
        "width": int(video.get("width", 0) or 0),
        "height": int(video.get("height", 0) or 0),
        "video_codec": video.get("codec_name"),
        "audio_codec": audio.get("codec_name"),
    }
