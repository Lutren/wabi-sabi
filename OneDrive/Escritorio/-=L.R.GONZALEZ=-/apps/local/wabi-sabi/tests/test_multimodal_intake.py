import json
from pathlib import Path
from types import SimpleNamespace

from wabi_sabi.core import multimodal_intake as mm


class FakeCamera:
    def isOpened(self):
        return True

    def set(self, *_args):
        return None

    def read(self):
        return True, object()

    def release(self):
        return None


class FakeCv2:
    def VideoCapture(self, _device_index):
        return FakeCamera()


class FakeSoundDevice:
    def rec(self, sample_count, *, samplerate, channels, dtype):
        return [0.01] * int(sample_count)

    def wait(self):
        return None


class FakeFusionModule:
    class ChannelFusionInput:
        def __init__(self, **kwargs):
            self.__dict__.update(kwargs)

    @staticmethod
    def fuse_channels(channels):
        assert channels
        assert hasattr(channels[0], "channel_id")
        return SimpleNamespace(
            to_dict=lambda: {
                "fusion_gate": "APPROVE",
                "fusion_R": 0.1,
                "fusion_Phi_eff": 0.7,
                "confidence": 0.8,
                "channel_count": len(channels),
            }
        )


def fake_observation(observation_id: str, input_modality: str) -> dict:
    return {
        "source": f"local_{input_modality}",
        "observation_id": observation_id,
        "modality": "multimodal",
        "input_modality": input_modality,
        "latent_dim": 8,
        "action": f"{input_modality}_summary",
        "prediction_error": 0.1,
        "surprise": 0.1,
        "predicted_goal_distance": 0.1,
        "calibration": 0.8,
        "latency_ms": 1.0,
        "evidence": 0.8,
        "risk": 0.1,
        "sensitive_residue": 0.0,
        "notes": ["test"],
        "raw_image_included": False,
        "raw_audio_included": False,
        "raw_private_data_included": False,
        "secret_values_printed": False,
    }


def approve_decision(_workspace: Path, _observation: dict) -> dict:
    return {
        "gate": "APPROVE",
        "regime": "FUNCIONAL",
        "r_world": 0.12,
        "phi_eff_world": 0.72,
        "reasons": ["unit_test"],
    }


def test_camera_smoke_writes_sanitized_artifact_and_witness(tmp_path, monkeypatch):
    monkeypatch.setattr(mm, "_optional_module", lambda name: FakeCv2() if name == "cv2" else None)
    monkeypatch.setattr(
        mm,
        "visual_observation_from_frame",
        lambda _frame, observation_id, latency_ms, source="local_camera": fake_observation(observation_id, "camera"),
    )
    monkeypatch.setattr(mm, "_evaluate_world_model", approve_decision)

    payload = mm.run_camera_smoke(workspace=tmp_path, runtime_root=tmp_path / "runtime")

    assert payload["ok"] is True
    assert payload["gate"] == "APPROVE"
    assert payload["raw_image_included"] is False
    assert payload["raw_audio_included"] is False
    assert payload["cloud_provider_called"] is False
    assert payload["witness_verified"] is True
    artifact = Path(payload["artifact"])
    assert artifact.exists()
    stored = json.loads(artifact.read_text(encoding="utf-8"))
    assert stored["raw_image_included"] is False
    assert stored["secret_values_printed"] is False


def test_fuse_payloads_uses_brain_os_channel_contract(tmp_path, monkeypatch):
    observation = fake_observation("camera-1", "camera")
    payload = {
        "ok": True,
        "observation": observation,
        "decision": {"gate": "APPROVE", "r_world": 0.1, "phi_eff_world": 0.7},
    }
    monkeypatch.setattr(
        mm,
        "_import_brain_core",
        lambda _workspace, name: FakeFusionModule if name == "mts_sensor_fusion_agent" else None,
    )

    result = mm._fuse_payloads(tmp_path, [payload])

    assert result["fusion_gate"] == "APPROVE"
    assert result["channel_count"] == 1


def test_mic_smoke_writes_metadata_only(tmp_path, monkeypatch):
    def optional(name: str):
        if name == "sounddevice":
            return FakeSoundDevice()
        if name == "numpy":
            return object()
        return None

    monkeypatch.setattr(mm, "_optional_module", optional)
    monkeypatch.setattr(
        mm,
        "audio_observation_from_samples",
        lambda _samples, sample_rate, observation_id, latency_ms, source="local_microphone", transcript="": fake_observation(
            observation_id, "audio"
        ),
    )
    monkeypatch.setattr(mm, "_audio_metrics", lambda _samples, sample_rate: {
        "sample_rate": sample_rate,
        "sample_count": sample_rate,
        "duration_sec": 1.0,
        "rms": 0.01,
        "peak": 0.01,
    })
    monkeypatch.setattr(mm, "_evaluate_world_model", approve_decision)

    payload = mm.run_mic_smoke(
        workspace=tmp_path,
        runtime_root=tmp_path / "runtime",
        options=mm.CaptureOptions(seconds=1),
    )

    assert payload["ok"] is True
    assert payload["audio_metrics"]["duration_sec"] == 1.0
    assert payload["raw_audio_included"] is False
    assert payload["raw_media_saved"] is False
    assert payload["cloud_provider_called"] is False
    assert Path(payload["artifact"]).exists()


def test_status_keeps_cloud_disabled_by_default(tmp_path, monkeypatch):
    monkeypatch.delenv("WABI_ALLOW_CLOUD_PROVIDERS", raising=False)
    monkeypatch.setattr(mm, "_device_status", lambda: {
        "platform": "windows",
        "windows_pnp_checked": True,
        "camera_present": True,
        "microphone_present": True,
        "summary": [],
    })

    payload = mm.build_multimodal_status(workspace=tmp_path, runtime_root=tmp_path / "runtime")

    assert payload["ok"] is True
    assert payload["mode"] == "LOCAL_OPEN_SOURCE"
    assert payload["cloud"]["enabled"] is False
    assert payload["cloud"]["raw_media_to_cloud_allowed"] is False
    assert payload["secret_values_printed"] is False


def test_low_light_camera_frame_is_capture_ok_but_integration_review(monkeypatch):
    monkeypatch.setattr(
        mm,
        "_frame_metrics",
        lambda _frame: {
            "width": 320,
            "height": 180,
            "channels": 3,
            "mean": 2.0,
            "std": 0.8,
            "usable": False,
            "quality": "low_light",
        },
    )

    observation = mm.visual_observation_from_frame(object(), observation_id="dark-frame", latency_ms=3.0)
    status = mm._interpret_visual_integration_status(observation, {"gate": "BLOCK", "phi_eff_world": 0.42})

    assert "capture_ok=true" in observation["notes"]
    assert "quality=low_light" in observation["notes"]
    assert observation["raw_image_included"] is False
    assert status == "REVIEW_LOW_LIGHT_CAPTURE_OK"
