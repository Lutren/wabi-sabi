from __future__ import annotations

import json
import os
import shutil
import subprocess
from pathlib import Path
from typing import Any


def no_window_kwargs() -> dict[str, Any]:
    if os.name != "nt":
        return {}
    kwargs: dict[str, Any] = {"creationflags": int(getattr(subprocess, "CREATE_NO_WINDOW", 0))}
    if hasattr(subprocess, "STARTUPINFO"):
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= getattr(subprocess, "STARTF_USESHOWWINDOW", 0)
        startupinfo.wShowWindow = 0
        kwargs["startupinfo"] = startupinfo
    return kwargs


def find_executable(name: str) -> str:
    env_name = name.upper().replace("-", "_")
    candidate = os.getenv(env_name)
    if candidate and Path(candidate).exists():
        return candidate
    resolved = shutil.which(name)
    if resolved:
        return resolved
    raise FileNotFoundError(f"{name} not found in PATH")


def run_process(args: list[str], log_path: Path, timeout: int = 600, cwd: Path | None = None) -> subprocess.CompletedProcess:
    log_path.parent.mkdir(parents=True, exist_ok=True)
    with log_path.open("a", encoding="utf-8", errors="ignore") as log:
        log.write("$ " + " ".join(args) + "\n")
        result = subprocess.run(
            args,
            cwd=str(cwd) if cwd else None,
            capture_output=True,
            text=True,
            timeout=timeout,
            **no_window_kwargs(),
        )
        if result.stdout:
            log.write(result.stdout + "\n")
        if result.stderr:
            log.write(result.stderr + "\n")
        log.write(f"returncode={result.returncode}\n")
    return result


def run_ffmpeg(args: list[str], log_path: Path, timeout: int = 600, cwd: Path | None = None) -> subprocess.CompletedProcess:
    return run_process([find_executable("ffmpeg"), *args], log_path=log_path, timeout=timeout, cwd=cwd)


def probe_media(path: Path, log_path: Path | None = None) -> dict[str, Any]:
    args = [
        find_executable("ffprobe"),
        "-v",
        "error",
        "-print_format",
        "json",
        "-show_format",
        "-show_streams",
        str(path),
    ]
    result = subprocess.run(args, capture_output=True, text=True, timeout=60, **no_window_kwargs())
    if log_path:
        log_path.parent.mkdir(parents=True, exist_ok=True)
        log_path.write_text((result.stdout or "") + "\n" + (result.stderr or ""), encoding="utf-8")
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or "ffprobe failed")
    data = json.loads(result.stdout or "{}")
    data["path"] = str(path)
    return data


def scale_crop_filter(width: int, height: int) -> str:
    return (
        f"scale={width}:{height}:force_original_aspect_ratio=increase,"
        f"crop={width}:{height},setsar=1,format=yuv420p"
    )


def subtitles_filter(relative_srt: str) -> str:
    safe = relative_srt.replace("\\", "/").replace("'", r"\'")
    return (
        f"subtitles='{safe}':force_style="
        "'FontName=Arial,FontSize=44,Outline=2,Shadow=1,Alignment=2,MarginV=110'"
    )


def render_image_clip(
    image: Path,
    output: Path,
    width: int,
    height: int,
    duration: float,
    fps: int,
    log_path: Path,
    job_dir: Path,
    srt_relative: str | None = None,
    music: Path | None = None,
) -> tuple[Path, list[str]]:
    warnings: list[str] = []
    filters = scale_crop_filter(width, height)
    if srt_relative:
        filters = filters + "," + subtitles_filter(srt_relative)
    args = ["-y", "-loop", "1", "-t", f"{duration:.3f}", "-i", str(image)]
    audio_map = ["-f", "lavfi", "-t", f"{duration:.3f}", "-i", "anullsrc=channel_layout=stereo:sample_rate=44100"]
    if music:
        audio_map = ["-stream_loop", "-1", "-i", str(music)]
    args.extend(audio_map)
    args.extend([
        "-vf",
        filters,
        "-r",
        str(fps),
        "-map",
        "0:v:0",
        "-map",
        "1:a:0",
        "-c:v",
        "libx264",
        "-preset",
        "veryfast",
        "-pix_fmt",
        "yuv420p",
        "-c:a",
        "aac",
        "-shortest",
        str(output),
    ])
    result = run_ffmpeg(args, log_path=log_path, timeout=600, cwd=job_dir)
    if result.returncode != 0 and srt_relative:
        warnings.append("subtitle_burn_failed_retrying_without_subtitles")
        fallback_args = [arg for arg in args]
        vf_index = fallback_args.index("-vf") + 1
        fallback_args[vf_index] = scale_crop_filter(width, height)
        result = run_ffmpeg(fallback_args, log_path=log_path, timeout=600, cwd=job_dir)
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip()[-1200:] or "ffmpeg image render failed")
    return output, warnings


def render_video_source(
    video: Path,
    output: Path,
    width: int,
    height: int,
    duration: float,
    fps: int,
    log_path: Path,
    job_dir: Path,
    start: float = 0.0,
    cut_silence: bool = False,
    srt_relative: str | None = None,
) -> tuple[Path, list[str]]:
    warnings: list[str] = []
    filters = scale_crop_filter(width, height)
    if cut_silence:
        filters += ",setpts=N/FRAME_RATE/TB"
    if srt_relative:
        filters += "," + subtitles_filter(srt_relative)
    args = [
        "-y",
        "-ss",
        f"{max(0.0, start):.3f}",
        "-t",
        f"{duration:.3f}",
        "-i",
        str(video),
        "-vf",
        filters,
        "-r",
        str(fps),
        "-c:v",
        "libx264",
        "-preset",
        "veryfast",
        "-pix_fmt",
        "yuv420p",
        "-c:a",
        "aac",
        "-af",
        "silenceremove=start_periods=1:start_duration=0.2:start_threshold=-45dB" if cut_silence else "anull",
        "-shortest",
        str(output),
    ]
    result = run_ffmpeg(args, log_path=log_path, timeout=600, cwd=job_dir)
    if result.returncode != 0 and srt_relative:
        warnings.append("subtitle_burn_failed_retrying_without_subtitles")
        fallback_args = [arg for arg in args]
        vf_index = fallback_args.index("-vf") + 1
        fallback_args[vf_index] = scale_crop_filter(width, height)
        result = run_ffmpeg(fallback_args, log_path=log_path, timeout=600, cwd=job_dir)
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip()[-1200:] or "ffmpeg video render failed")
    return output, warnings


def create_thumbnail(video: Path, output: Path, log_path: Path) -> Path:
    args = ["-y", "-ss", "00:00:01", "-i", str(video), "-frames:v", "1", str(output)]
    result = run_ffmpeg(args, log_path=log_path, timeout=120)
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip()[-1200:] or "ffmpeg thumbnail failed")
    return output


def create_preview(video: Path, output: Path, duration: float, log_path: Path) -> Path:
    args = ["-y", "-t", f"{min(max(duration, 1.0), 4.0):.3f}", "-i", str(video), "-c", "copy", str(output)]
    result = run_ffmpeg(args, log_path=log_path, timeout=120)
    if result.returncode != 0:
        args = ["-y", "-t", f"{min(max(duration, 1.0), 4.0):.3f}", "-i", str(video), "-c:v", "libx264", "-c:a", "aac", str(output)]
        result = run_ffmpeg(args, log_path=log_path, timeout=120)
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip()[-1200:] or "ffmpeg preview failed")
    return output


def concat_videos(parts: list[Path], output: Path, list_file: Path, log_path: Path) -> Path:
    lines = []
    for part in parts:
        safe = part.resolve().as_posix().replace("'", r"'\''")
        lines.append(f"file '{safe}'")
    list_file.write_text("\n".join(lines), encoding="utf-8")
    args = ["-y", "-f", "concat", "-safe", "0", "-i", str(list_file), "-c", "copy", str(output)]
    result = run_ffmpeg(args, log_path=log_path, timeout=600)
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip()[-1200:] or "ffmpeg concat failed")
    return output
