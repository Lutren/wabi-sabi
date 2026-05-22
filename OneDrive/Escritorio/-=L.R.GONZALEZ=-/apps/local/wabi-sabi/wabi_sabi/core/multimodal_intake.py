from __future__ import annotations

import importlib
import importlib.util
import json
import math
import os
import subprocess
import sys
import time
import wave
from dataclasses import dataclass
from pathlib import Path
from types import SimpleNamespace
from typing import Any

from wabi_sabi.core.bridge import WitnessLog
from wabi_sabi.core.observation import ObservationEnvelope
from wabi_sabi.core.tools import stamp


SCHEMA = "wabi.multimodal_intake.v1"
DEFAULT_CAMERA_WIDTH = 320
DEFAULT_CAMERA_HEIGHT = 180
DEFAULT_SAMPLE_RATE = 16_000
MAX_OBSERVE_SECONDS = 30
MAX_CAMERA_FRAMES = 5


@dataclass(frozen=True)
class CaptureOptions:
    seconds: int = 5
    device_index: int = 0
    sample_rate: int = DEFAULT_SAMPLE_RATE
    width: int = DEFAULT_CAMERA_WIDTH
    height: int = DEFAULT_CAMERA_HEIGHT
    transcribe: bool = False


def build_multimodal_status(*, workspace: str | Path, runtime_root: str | Path) -> dict[str, Any]:
    runtime = Path(runtime_root).resolve()
    libs = {
        name: _module_available(name)
        for name in (
            "cv2",
            "sounddevice",
            "pyaudio",
            "numpy",
            "faster_whisper",
            "whisper",
            "speech_recognition",
            "mediapipe",
        )
    }
    brain_os = _brain_os_status(Path(workspace).resolve())
    return {
        "schema": SCHEMA,
        "ok": True,
        "action": "multimodal_status",
        "gate": "APPROVE",
        "mode": "LOCAL_OPEN_SOURCE",
        "runtime_root": str(runtime),
        "workspace": str(Path(workspace).resolve()),
        "privacy": _privacy_policy(),
        "libraries": libs,
        "devices": _device_status(),
        "brain_os_bridge": brain_os,
        "cloud": {
            "enabled": _env_flag("WABI_ALLOW_CLOUD_PROVIDERS", "0"),
            "policy": "FREE_OR_CONFIGURED_REVIEW",
            "paid_required": False,
            "raw_media_to_cloud_allowed": False,
        },
        "commands": [
            "wabi multimodal status",
            "wabi multimodal smoke-camera",
            "wabi multimodal smoke-mic",
            "wabi multimodal observe --seconds 10 --local-only",
        ],
        "secret_values_printed": False,
    }


def run_camera_smoke(
    *,
    workspace: str | Path,
    runtime_root: str | Path,
    options: CaptureOptions | None = None,
) -> dict[str, Any]:
    opts = options or CaptureOptions()
    payload = _camera_capture_payload(workspace=Path(workspace), runtime_root=Path(runtime_root), options=opts)
    return _write_and_witness(
        runtime_root=Path(runtime_root),
        action="multimodal_smoke_camera",
        payload=payload,
        prompt="multimodal smoke-camera",
    )


def run_mic_smoke(
    *,
    workspace: str | Path,
    runtime_root: str | Path,
    options: CaptureOptions | None = None,
) -> dict[str, Any]:
    opts = options or CaptureOptions()
    payload = _mic_capture_payload(workspace=Path(workspace), runtime_root=Path(runtime_root), options=opts)
    return _write_and_witness(
        runtime_root=Path(runtime_root),
        action="multimodal_smoke_mic",
        payload=payload,
        prompt="multimodal smoke-mic",
    )


def run_multimodal_observe(
    *,
    workspace: str | Path,
    runtime_root: str | Path,
    options: CaptureOptions | None = None,
) -> dict[str, Any]:
    opts = _bounded_options(options or CaptureOptions())
    workspace_path = Path(workspace)
    runtime_path = Path(runtime_root)
    visual_payloads = []
    frame_count = max(1, min(MAX_CAMERA_FRAMES, opts.seconds))
    for _ in range(frame_count):
        visual_payloads.append(
            _camera_capture_payload(
                workspace=workspace_path,
                runtime_root=runtime_path,
                options=opts,
                observation_prefix="camera_stream",
            )
        )
        if frame_count > 1:
            time.sleep(min(1.0, max(0.05, opts.seconds / max(frame_count, 1) / 2.0)))
    mic_payload = _mic_capture_payload(workspace=workspace_path, runtime_root=runtime_path, options=opts)
    channels = [item for item in visual_payloads if item.get("ok")]
    if mic_payload.get("ok"):
        channels.append(mic_payload)

    fusion = _fuse_payloads(workspace_path, channels)
    combined_observation = _combined_observation(channels, opts.seconds)
    decision = _evaluate_world_model(workspace_path, combined_observation)
    payload = {
        "schema": SCHEMA,
        "ok": bool(channels),
        "action": "multimodal_observe",
        "gate": "APPROVE" if channels else "REVIEW",
        "world_model_gate": decision.get("gate", "REVIEW"),
        "fusion_gate": fusion.get("fusion_gate", "REVIEW"),
        "mode": "LOCAL_OPEN_SOURCE",
        "seconds": opts.seconds,
        "camera_samples": visual_payloads,
        "mic_sample": mic_payload,
        "combined_observation": combined_observation,
        "decision": decision,
        "fusion": fusion,
        "privacy": _privacy_policy(),
        "raw_image_included": False,
        "raw_audio_included": False,
        "raw_media_saved": False,
        "cloud_provider_called": False,
        "secret_values_printed": False,
    }
    return _write_and_witness(
        runtime_root=runtime_path,
        action="multimodal_observe",
        payload=payload,
        prompt=f"multimodal observe seconds={opts.seconds}",
    )


def visual_observation_from_frame(
    frame: Any,
    *,
    observation_id: str,
    latency_ms: float,
    source: str = "local_camera",
) -> dict[str, Any]:
    metrics = _frame_metrics(frame)
    evidence = 0.88 if metrics["usable"] else 0.25
    prediction_error = 0.08 if metrics["usable"] else 0.55
    surprise = 0.08 if metrics["std"] >= 8.0 else 0.35
    risk = 0.20 if metrics["usable"] else 0.40
    return _safe_world_observation(
        source=source,
        observation_id=observation_id,
        modality="visual",
        input_modality="camera",
        latent_dim=8,
        action="local_camera_frame_summary",
        prediction_error=prediction_error,
        surprise=surprise,
        predicted_goal_distance=0.12,
        calibration=0.78 if metrics["usable"] else 0.45,
        latency_ms=latency_ms,
        evidence=evidence,
        risk=risk,
        sensitive_residue=0.0,
        notes=(
            "frame_reduced_metadata_only",
            "capture_ok=true",
            f"quality={metrics['quality']}",
            f"width={metrics['width']}",
            f"height={metrics['height']}",
            f"mean={metrics['mean']:.2f}",
            f"std={metrics['std']:.2f}",
        ),
    )


def audio_observation_from_samples(
    samples: Any,
    *,
    sample_rate: int,
    observation_id: str,
    latency_ms: float,
    source: str = "local_microphone",
    transcript: str = "",
) -> dict[str, Any]:
    metrics = _audio_metrics(samples, sample_rate=sample_rate)
    has_signal = metrics["rms"] >= 0.0015
    evidence = 0.82 if has_signal else 0.35
    return _safe_world_observation(
        source=source,
        observation_id=observation_id,
        modality="multimodal",
        input_modality="audio",
        latent_dim=8,
        action="local_microphone_chunk_summary",
        prediction_error=0.12 if has_signal else 0.45,
        surprise=0.12 if has_signal else 0.32,
        predicted_goal_distance=0.18 if has_signal else 0.35,
        calibration=0.72 if has_signal else 0.42,
        latency_ms=latency_ms,
        evidence=evidence,
        risk=0.18,
        sensitive_residue=0.0,
        notes=(
            "audio_chunk_metadata_only",
            f"duration_sec={metrics['duration_sec']:.3f}",
            f"sample_rate={metrics['sample_rate']}",
            f"rms={metrics['rms']:.6f}",
            f"peak={metrics['peak']:.6f}",
            "transcript_present=" + str(bool(transcript)).lower(),
        ),
    )


def _camera_capture_payload(
    *,
    workspace: Path,
    runtime_root: Path,
    options: CaptureOptions,
    observation_prefix: str = "camera",
) -> dict[str, Any]:
    started = time.perf_counter()
    cv2 = _optional_module("cv2")
    if cv2 is None:
        return _capture_review_payload("camera", "cv2_not_available", workspace)
    cap = None
    try:
        cap = cv2.VideoCapture(int(options.device_index))
        if hasattr(cap, "set"):
            cap.set(3, float(options.width))
            cap.set(4, float(options.height))
        opened = bool(cap.isOpened()) if hasattr(cap, "isOpened") else True
        if not opened:
            return _capture_review_payload("camera", "camera_not_opened", workspace)
        ok, frame = cap.read()
        if not ok or frame is None:
            return _capture_review_payload("camera", "camera_frame_not_read", workspace)
        latency_ms = (time.perf_counter() - started) * 1000.0
        observation = visual_observation_from_frame(
            frame,
            observation_id=f"{observation_prefix}_{stamp()}",
            latency_ms=latency_ms,
        )
        decision = _evaluate_world_model(workspace, observation)
        interpretation_status = _interpret_visual_integration_status(observation, decision)
        return {
            "schema": SCHEMA,
            "ok": True,
            "action": "camera_capture",
            "gate": "APPROVE",
            "capture_gate": "APPROVE",
            "integration_gate": decision.get("gate", "REVIEW"),
            "interpretation_status": interpretation_status,
            "world_model_gate": decision.get("gate", "REVIEW"),
            "device_index": int(options.device_index),
            "observation": observation,
            "decision": decision,
            "privacy": _privacy_policy(),
            "raw_image_included": False,
            "raw_audio_included": False,
            "raw_media_saved": False,
            "cloud_provider_called": False,
            "secret_values_printed": False,
            "evidence": [
                "camera_frame_read=true",
                f"latency_ms={latency_ms:.2f}",
                "raw_image_included=false",
            ],
        }
    except Exception as exc:
        return _capture_review_payload("camera", f"camera_exception:{type(exc).__name__}", workspace)
    finally:
        if cap is not None and hasattr(cap, "release"):
            cap.release()


def _mic_capture_payload(*, workspace: Path, runtime_root: Path, options: CaptureOptions) -> dict[str, Any]:
    started = time.perf_counter()
    sd = _optional_module("sounddevice")
    if sd is None:
        return _capture_review_payload("microphone", "sounddevice_not_available", workspace)
    np = _optional_module("numpy")
    if np is None:
        return _capture_review_payload("microphone", "numpy_not_available", workspace)
    seconds = max(1, min(MAX_OBSERVE_SECONDS, int(options.seconds)))
    sample_rate = max(8_000, min(48_000, int(options.sample_rate)))
    try:
        samples = sd.rec(int(seconds * sample_rate), samplerate=sample_rate, channels=1, dtype="float32")
        sd.wait()
        latency_ms = (time.perf_counter() - started) * 1000.0
        transcript = ""
        transcription = {"enabled": bool(options.transcribe), "status": "disabled_by_default"}
        if options.transcribe:
            transcript, transcription = _try_transcribe_samples(samples, sample_rate=sample_rate, runtime_root=runtime_root)
        observation = audio_observation_from_samples(
            samples,
            sample_rate=sample_rate,
            observation_id=f"microphone_{stamp()}",
            latency_ms=latency_ms,
            transcript=transcript,
        )
        decision = _evaluate_world_model(workspace, observation)
        metrics = _audio_metrics(samples, sample_rate=sample_rate)
        return {
            "schema": SCHEMA,
            "ok": True,
            "action": "microphone_capture",
            "gate": "APPROVE",
            "world_model_gate": decision.get("gate", "REVIEW"),
            "seconds": seconds,
            "sample_rate": sample_rate,
            "audio_metrics": metrics,
            "transcription": transcription,
            "transcript_text_included": bool(transcript),
            "transcript_excerpt": transcript[:500],
            "observation": observation,
            "decision": decision,
            "privacy": _privacy_policy(),
            "raw_image_included": False,
            "raw_audio_included": False,
            "raw_media_saved": False,
            "cloud_provider_called": False,
            "secret_values_printed": False,
            "evidence": [
                "microphone_chunk_recorded=true",
                f"duration_sec={metrics['duration_sec']:.3f}",
                f"rms={metrics['rms']:.6f}",
                "raw_audio_included=false",
            ],
        }
    except Exception as exc:
        return _capture_review_payload("microphone", f"microphone_exception:{type(exc).__name__}", workspace)


def _try_transcribe_samples(samples: Any, *, sample_rate: int, runtime_root: Path) -> tuple[str, dict[str, Any]]:
    if not _env_flag("WABI_ENABLE_LOCAL_TRANSCRIPTION", "0"):
        return "", {"enabled": True, "status": "blocked_by_env", "reason": "set WABI_ENABLE_LOCAL_TRANSCRIPTION=1"}
    temp_dir = runtime_root / "tmp"
    temp_dir.mkdir(parents=True, exist_ok=True)
    wav_path = temp_dir / f"mic_chunk_{stamp()}.wav"
    try:
        _write_temp_wav(samples, sample_rate=sample_rate, path=wav_path)
        if _module_available("faster_whisper"):
            fw = importlib.import_module("faster_whisper")
            model_name = os.environ.get("WABI_WHISPER_MODEL", "tiny")
            model = fw.WhisperModel(model_name, device="cpu", compute_type="int8")
            segments, _info = model.transcribe(str(wav_path), beam_size=1)
            text = " ".join(segment.text.strip() for segment in segments if getattr(segment, "text", "").strip())
            return text, {"enabled": True, "status": "pass", "engine": "faster_whisper", "model": model_name}
        if _module_available("whisper"):
            whisper = importlib.import_module("whisper")
            model_name = os.environ.get("WABI_WHISPER_MODEL", "tiny")
            model = whisper.load_model(model_name)
            result = model.transcribe(str(wav_path), fp16=False)
            return str(result.get("text", "")).strip(), {"enabled": True, "status": "pass", "engine": "whisper", "model": model_name}
        return "", {"enabled": True, "status": "review", "reason": "no_local_whisper_engine"}
    except Exception as exc:
        return "", {"enabled": True, "status": "review", "reason": f"transcription_exception:{type(exc).__name__}"}
    finally:
        try:
            wav_path.unlink(missing_ok=True)
        except Exception:
            pass


def _write_temp_wav(samples: Any, *, sample_rate: int, path: Path) -> None:
    np = importlib.import_module("numpy")
    data = np.asarray(samples).reshape(-1)
    data = np.clip(data, -1.0, 1.0)
    pcm = (data * 32767.0).astype(np.int16)
    with wave.open(str(path), "wb") as wav:
        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(sample_rate)
        wav.writeframes(pcm.tobytes())


def _frame_metrics(frame: Any) -> dict[str, Any]:
    np = _optional_module("numpy")
    if np is None:
        shape = getattr(frame, "shape", (0, 0))
        height = int(shape[0]) if len(shape) > 0 else 0
        width = int(shape[1]) if len(shape) > 1 else 0
        usable = width > 0 and height > 0
        return {
            "width": width,
            "height": height,
            "channels": 0,
            "mean": 0.0,
            "std": 0.0,
            "usable": usable,
            "quality": "metadata_only" if usable else "empty",
        }
    arr = np.asarray(frame)
    shape = arr.shape
    height = int(shape[0]) if len(shape) > 0 else 0
    width = int(shape[1]) if len(shape) > 1 else 0
    channels = int(shape[2]) if len(shape) > 2 else 1
    mean = float(arr.mean()) if arr.size else 0.0
    std = float(arr.std()) if arr.size else 0.0
    usable = width > 0 and height > 0 and 5.0 <= mean <= 250.0
    if width <= 0 or height <= 0:
        quality = "empty"
    elif mean < 5.0:
        quality = "low_light"
    elif mean > 250.0:
        quality = "overexposed"
    elif std < 2.0:
        quality = "low_texture"
    else:
        quality = "usable"
    return {
        "width": width,
        "height": height,
        "channels": channels,
        "mean": mean,
        "std": std,
        "usable": usable,
        "quality": quality,
    }


def _interpret_visual_integration_status(observation: dict[str, Any], decision: dict[str, Any]) -> str:
    gate = str(decision.get("gate") or "REVIEW").upper()
    notes = {str(item) for item in observation.get("notes", [])}
    quality = next((item.split("=", 1)[1] for item in notes if item.startswith("quality=")), "unknown")
    if quality in {"low_light", "overexposed", "low_texture"} and gate != "APPROVE":
        return f"REVIEW_{quality.upper()}_CAPTURE_OK"
    if gate == "APPROVE":
        return "APPROVE_CAPTURE_AND_INTEGRATION"
    return "REVIEW_CAPTURE_OK_INTEGRATION_NOT_READY"


def _audio_metrics(samples: Any, *, sample_rate: int) -> dict[str, Any]:
    np = _optional_module("numpy")
    if np is None:
        return {"sample_rate": int(sample_rate), "sample_count": 0, "duration_sec": 0.0, "rms": 0.0, "peak": 0.0}
    arr = np.asarray(samples, dtype="float32").reshape(-1)
    sample_count = int(arr.size)
    duration = sample_count / float(sample_rate) if sample_rate else 0.0
    rms = float(math.sqrt(float(np.mean(arr * arr)))) if sample_count else 0.0
    peak = float(np.max(np.abs(arr))) if sample_count else 0.0
    return {
        "sample_rate": int(sample_rate),
        "sample_count": sample_count,
        "duration_sec": duration,
        "rms": rms,
        "peak": peak,
    }


def _safe_world_observation(**kwargs: Any) -> dict[str, Any]:
    observation = dict(kwargs)
    observation["prediction_error"] = _clamp01(observation["prediction_error"])
    observation["surprise"] = _clamp01(observation["surprise"])
    observation["predicted_goal_distance"] = _clamp01(observation["predicted_goal_distance"])
    observation["calibration"] = _clamp01(observation["calibration"])
    observation["latency_ms"] = max(0.0, float(observation["latency_ms"]))
    observation["evidence"] = _clamp01(observation["evidence"])
    observation["risk"] = _clamp01(observation["risk"])
    observation["sensitive_residue"] = _clamp01(observation["sensitive_residue"])
    observation["notes"] = [str(item) for item in observation.get("notes", ())]
    observation["raw_image_included"] = False
    observation["raw_audio_included"] = False
    observation["raw_private_data_included"] = False
    observation["secret_values_printed"] = False
    return observation


def _evaluate_world_model(workspace: Path, observation: dict[str, Any]) -> dict[str, Any]:
    module = _import_brain_core(workspace, "world_model_adapter")
    if module is not None:
        try:
            obs = module.WorldModelObservation(
                source=observation["source"],
                observation_id=observation["observation_id"],
                modality=observation["modality"],
                latent_dim=int(observation["latent_dim"]),
                action=observation["action"],
                prediction_error=float(observation["prediction_error"]),
                surprise=float(observation["surprise"]),
                predicted_goal_distance=float(observation["predicted_goal_distance"]),
                calibration=float(observation["calibration"]),
                latency_ms=float(observation["latency_ms"]),
                evidence=float(observation["evidence"]),
                risk=float(observation["risk"]),
                sensitive_residue=float(observation["sensitive_residue"]),
                notes=tuple(observation.get("notes", [])),
            )
            return module.evaluate_world_model(obs).to_dict()
        except Exception as exc:
            return {"gate": "REVIEW", "regime": "CARGADO", "reason": f"brain_os_world_model_exception:{type(exc).__name__}"}
    r_world = _clamp01(
        0.35 * observation["prediction_error"]
        + 0.25 * observation["surprise"]
        + 0.20 * observation["predicted_goal_distance"]
        + 0.10 * (1.0 - observation["calibration"])
        + 0.10 * observation["risk"]
    )
    phi_eff = _clamp01(observation["calibration"] * observation["evidence"] * math.exp(-2.0 * r_world))
    if observation["sensitive_residue"] >= 0.80:
        gate = "BLOCK"
    elif phi_eff < 0.50 or r_world >= 0.55:
        gate = "REVIEW"
    else:
        gate = "APPROVE"
    return {
        "r_world": r_world,
        "phi_eff_world": phi_eff,
        "gate": gate,
        "regime": "FUNCIONAL" if gate == "APPROVE" else "CARGADO",
        "recommended_action": "local_reversible_observation_only",
        "reasons": ["fallback_world_model_no_brain_os_import"],
        "witness_event": {
            "event_type": "world_model_observation_decision",
            "observation_id": observation["observation_id"],
            "raw_image_included": False,
            "raw_audio_included": False,
            "secret_values_printed": False,
            "gate": gate,
        },
    }


def _fuse_payloads(workspace: Path, payloads: list[dict[str, Any]]) -> dict[str, Any]:
    module = _import_brain_core(workspace, "mts_sensor_fusion_agent")
    channels = [_fusion_channel_from_payload(item) for item in payloads if item.get("observation")]
    if not channels:
        return {"fusion_gate": "REVIEW", "reason": "no_usable_channels", "channel_count": 0}
    if module is not None:
        try:
            module_channels = [_channel_for_fusion_module(module, channel) for channel in channels]
            result = module.fuse_channels(module_channels)
            return result.to_dict() if hasattr(result, "to_dict") else dict(result)
        except Exception as exc:
            return {"fusion_gate": "REVIEW", "reason": f"brain_os_fusion_exception:{type(exc).__name__}", "channel_count": len(channels)}
    blocked = [channel["channel_id"] for channel in channels if channel["gate_status"] == "BLOCK"]
    review = [channel["channel_id"] for channel in channels if channel["gate_status"] == "REVIEW"]
    gate = "BLOCK" if blocked else ("REVIEW" if review else "APPROVE")
    return {
        "fusion_gate": gate,
        "fusion_R": _clamp01(sum(channel["r_total"] for channel in channels) / len(channels)),
        "fusion_Phi_eff": _clamp01(sum(channel["phi_eff"] for channel in channels) / len(channels)),
        "confidence": _clamp01(sum(channel["calibration_K"] for channel in channels) / len(channels)),
        "channel_count": len(channels),
        "usable_channels": [channel["channel_id"] for channel in channels],
        "bad_channels": sorted(blocked + review),
        "fusion_explanation": "fallback_fusion_no_brain_os_import",
    }


def _fusion_channel_from_payload(payload: dict[str, Any]) -> dict[str, Any]:
    obs = payload["observation"]
    decision = payload.get("decision", {})
    gate = str(decision.get("gate") or payload.get("gate") or "REVIEW")
    r_world = float(decision.get("r_world", 0.40 if gate == "REVIEW" else 0.15))
    phi = float(decision.get("phi_eff_world", obs.get("evidence", 0.5)))
    return {
        "channel_id": str(obs["observation_id"]),
        "modality": str(obs.get("input_modality", obs.get("modality", "multimodal"))),
        "measured_domain": "local_multimodal_intake",
        "gate_status": gate,
        "r_total": _clamp01(r_world),
        "phi_eff": _clamp01(phi),
        "bandwidth_B": _clamp01(obs.get("evidence", 0.5)),
        "calibration_K": _clamp01(obs.get("calibration", 0.5)),
        "residue_noise": _clamp01(obs.get("prediction_error", 0.0)),
        "residue_latency": _clamp01(float(obs.get("latency_ms", 0.0)) / 1000.0),
        "residue_saturation": 0.0,
        "residue_calibration": _clamp01(1.0 - float(obs.get("calibration", 0.0))),
        "residue_missing": 0.0 if payload.get("ok") else 1.0,
        "residue_contradiction": 0.0,
        "residue_sensitive": _clamp01(obs.get("sensitive_residue", 0.0)),
    }


def _channel_for_fusion_module(module: Any, channel: dict[str, Any]) -> Any:
    channel_cls = getattr(module, "ChannelFusionInput", None)
    if channel_cls is not None:
        try:
            return channel_cls(**channel)
        except TypeError:
            pass
    return SimpleNamespace(**channel)


def _combined_observation(channels: list[dict[str, Any]], seconds: int) -> dict[str, Any]:
    observations = [channel["observation"] for channel in channels if channel.get("observation")]
    if not observations:
        return _safe_world_observation(
            source="local_multimodal_intake",
            observation_id=f"multimodal_empty_{stamp()}",
            modality="multimodal",
            input_modality="none",
            latent_dim=8,
            action="local_multimodal_empty",
            prediction_error=0.75,
            surprise=0.55,
            predicted_goal_distance=0.60,
            calibration=0.10,
            latency_ms=0.0,
            evidence=0.0,
            risk=0.35,
            sensitive_residue=0.0,
            notes=("no_usable_channels",),
        )
    avg = lambda key: sum(float(obs.get(key, 0.0)) for obs in observations) / len(observations)
    return _safe_world_observation(
        source="local_multimodal_intake",
        observation_id=f"multimodal_{stamp()}",
        modality="multimodal",
        input_modality="camera_microphone",
        latent_dim=16,
        action=f"local_micro_stream_summary_seconds_{seconds}",
        prediction_error=avg("prediction_error"),
        surprise=avg("surprise"),
        predicted_goal_distance=avg("predicted_goal_distance"),
        calibration=avg("calibration"),
        latency_ms=avg("latency_ms"),
        evidence=avg("evidence"),
        risk=max(float(obs.get("risk", 0.0)) for obs in observations),
        sensitive_residue=max(float(obs.get("sensitive_residue", 0.0)) for obs in observations),
        notes=(
            "combined_camera_microphone_metadata_only",
            f"channel_count={len(observations)}",
            "raw_media_included=false",
        ),
    )


def _write_and_witness(*, runtime_root: Path, action: str, payload: dict[str, Any], prompt: str) -> dict[str, Any]:
    runtime = runtime_root.resolve()
    output_dir = runtime / "outputs"
    output_dir.mkdir(parents=True, exist_ok=True)
    payload = dict(payload)
    payload.setdefault("schema", SCHEMA)
    payload["artifact"] = ""
    payload["witness_event_id"] = 0
    payload["witness_verified"] = False
    payload["witness_verify_reason"] = "not_recorded"
    payload["witness_db"] = ""
    payload["observation_envelope"] = {}
    artifact = output_dir / f"{action}_{stamp()}.json"
    payload["artifact"] = str(artifact)
    observation = ObservationEnvelope(
        prompt=prompt,
        intent="multimodal_intake",
        agent="multimodal_intake",
        action_gate=str(payload.get("gate", "REVIEW")),
        certainty=[
            "Local camera/microphone intake records sanitized metadata only.",
            "Raw image/audio bytes are not included in payloads or witness events.",
        ],
        inference=["Cloud provider fields stay gated and were not called."],
        unknown=[] if payload.get("ok") else ["One or more local media channels did not produce a usable observation."],
        artifacts=[str(artifact)],
        evidence=[
            f"action={action}",
            f"raw_image_included={payload.get('raw_image_included', False)}",
            f"raw_audio_included={payload.get('raw_audio_included', False)}",
            f"cloud_provider_called={payload.get('cloud_provider_called', False)}",
        ],
    ).finalize()
    witness_payload = _witness_safe_payload(payload)
    witness_payload["observation_fingerprint"] = observation.fingerprint
    witness = WitnessLog(runtime / "witness" / "wabi_patch_witness.sqlite")
    event_id = witness.append("wabi_multimodal_intake", witness_payload)
    witness_ok, witness_reason = witness.verify_chain()
    payload.update(
        {
            "witness_event_id": event_id,
            "witness_verified": witness_ok,
            "witness_verify_reason": witness_reason,
            "witness_db": str(witness.db_path),
            "observation_envelope": observation.to_dict(),
        }
    )
    artifact.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    return payload


def _witness_safe_payload(payload: dict[str, Any]) -> dict[str, Any]:
    return {
        "schema": payload.get("schema", SCHEMA),
        "action": payload.get("action"),
        "ok": bool(payload.get("ok")),
        "gate": payload.get("gate"),
        "mode": payload.get("mode", "LOCAL_OPEN_SOURCE"),
        "raw_image_included": False,
        "raw_audio_included": False,
        "raw_media_saved": False,
        "cloud_provider_called": False,
        "secret_values_printed": False,
        "artifact": payload.get("artifact", ""),
        "decision": _compact_decision(payload.get("decision", {})),
        "world_model_gate": payload.get("world_model_gate", payload.get("decision", {}).get("gate", "")),
        "fusion_gate": payload.get("fusion_gate", payload.get("fusion", {}).get("fusion_gate", "")),
    }


def _compact_decision(decision: dict[str, Any]) -> dict[str, Any]:
    return {
        "gate": decision.get("gate"),
        "regime": decision.get("regime"),
        "r_world": decision.get("r_world"),
        "phi_eff_world": decision.get("phi_eff_world"),
        "reasons": decision.get("reasons", []),
    }


def _capture_review_payload(channel: str, reason: str, workspace: Path) -> dict[str, Any]:
    observation = _safe_world_observation(
        source=f"local_{channel}",
        observation_id=f"{channel}_review_{stamp()}",
        modality="visual" if channel == "camera" else "multimodal",
        input_modality=channel,
        latent_dim=8,
        action=f"{channel}_capture_review",
        prediction_error=0.65,
        surprise=0.45,
        predicted_goal_distance=0.55,
        calibration=0.20,
        latency_ms=0.0,
        evidence=0.0,
        risk=0.25,
        sensitive_residue=0.0,
        notes=(reason, "raw_media_included=false"),
    )
    decision = _evaluate_world_model(workspace, observation)
    return {
        "schema": SCHEMA,
        "ok": False,
        "action": f"{channel}_capture",
        "gate": "REVIEW",
        "reason": reason,
        "observation": observation,
        "decision": decision,
        "privacy": _privacy_policy(),
        "raw_image_included": False,
        "raw_audio_included": False,
        "raw_media_saved": False,
        "cloud_provider_called": False,
        "secret_values_printed": False,
        "evidence": [reason, "raw_media_included=false"],
    }


def _privacy_policy() -> dict[str, Any]:
    return {
        "raw_image_included": False,
        "raw_audio_included": False,
        "raw_media_saved_by_default": False,
        "cloud_provider_called_by_default": False,
        "transcription_default": "disabled",
        "witness_contains": "metadata_and_decisions_only",
    }


def _bounded_options(options: CaptureOptions) -> CaptureOptions:
    return CaptureOptions(
        seconds=max(1, min(MAX_OBSERVE_SECONDS, int(options.seconds))),
        device_index=max(0, int(options.device_index)),
        sample_rate=max(8_000, min(48_000, int(options.sample_rate))),
        width=max(64, min(1280, int(options.width))),
        height=max(64, min(720, int(options.height))),
        transcribe=bool(options.transcribe),
    )


def _brain_os_status(workspace: Path) -> dict[str, Any]:
    available = {
        "world_model_adapter": _import_brain_core(workspace, "world_model_adapter") is not None,
        "mts_sensor_fusion_agent": _import_brain_core(workspace, "mts_sensor_fusion_agent") is not None,
    }
    return {
        "available": all(available.values()),
        "modules": available,
        "path": str(_find_brain_os_root(workspace) or ""),
    }


def _import_brain_core(workspace: Path, module_name: str) -> Any | None:
    brain_root = _find_brain_os_root(workspace)
    if brain_root is None:
        return None
    claudio_root = brain_root / "02_CLAUDIO"
    if not claudio_root.exists():
        return None
    claudio_str = str(claudio_root)
    if claudio_str not in sys.path:
        sys.path.insert(0, claudio_str)
    try:
        return importlib.import_module(f"core.{module_name}")
    except Exception:
        return None


def _find_brain_os_root(workspace: Path) -> Path | None:
    env = os.environ.get("WABI_BRAIN_OS_ROOT", "").strip()
    candidates: list[Path] = []
    if env:
        candidates.append(Path(env))
    current = workspace.resolve()
    candidates.extend([current, *current.parents])
    desktop = Path.home() / "OneDrive" / "Escritorio"
    candidates.append(desktop / "-= BRAIN_OS =-")
    for candidate in candidates:
        if (candidate / "02_CLAUDIO" / "core" / "world_model_adapter.py").exists():
            return candidate.resolve()
    return None


def _device_status() -> dict[str, Any]:
    if os.name != "nt":
        return {"platform": os.name, "windows_pnp_checked": False, "summary": []}
    command = [
        "powershell",
        "-NoProfile",
        "-Command",
        "Get-PnpDevice -Class Camera,Media,AudioEndpoint -PresentOnly | "
        "Select-Object Class,FriendlyName,Status | ConvertTo-Json -Compress",
    ]
    try:
        proc = subprocess.run(command, capture_output=True, text=True, timeout=10)
    except Exception as exc:
        return {"platform": "windows", "windows_pnp_checked": False, "error": type(exc).__name__, "summary": []}
    if proc.returncode != 0:
        return {"platform": "windows", "windows_pnp_checked": False, "error": proc.stderr[-500:], "summary": []}
    try:
        parsed = json.loads(proc.stdout or "[]")
    except json.JSONDecodeError:
        parsed = []
    if isinstance(parsed, dict):
        parsed = [parsed]
    summary = [
        {
            "class": str(row.get("Class", "")),
            "friendly_name": str(row.get("FriendlyName", "")),
            "status": str(row.get("Status", "")),
        }
        for row in parsed
        if isinstance(row, dict)
    ]
    return {
        "platform": "windows",
        "windows_pnp_checked": True,
        "camera_present": any(row["class"].lower() == "camera" and row["status"].upper() == "OK" for row in summary),
        "microphone_present": any("microphone" in row["friendly_name"].lower() and row["status"].upper() == "OK" for row in summary),
        "summary": summary[:20],
    }


def _module_available(name: str) -> bool:
    try:
        return importlib.util.find_spec(name) is not None
    except (ImportError, ValueError):
        return False


def _optional_module(name: str) -> Any | None:
    try:
        return importlib.import_module(name)
    except Exception:
        return None


def _env_flag(name: str, default: str = "0") -> bool:
    return os.environ.get(name, default).strip().lower() in {"1", "true", "yes", "on"}


def _clamp01(value: Any) -> float:
    try:
        return max(0.0, min(1.0, float(value)))
    except (TypeError, ValueError):
        return 0.0
