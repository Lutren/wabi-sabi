from wabi_sabi.core.ollama_bridge import OllamaBridge


def test_ollama_bridge_selects_fast_model(tmp_path, monkeypatch):
    monkeypatch.delenv("BASE_MODEL", raising=False)
    monkeypatch.delenv("WABI_BASE_MODEL", raising=False)
    monkeypatch.delenv("WABI_OLLAMA_BASE_MODEL", raising=False)
    bridge = OllamaBridge(runtime_root=tmp_path / "runtime")

    monkeypatch.setattr(
        bridge,
        "_get",
        lambda path, timeout: {
            "models": [{"name": "qwen2.5:0.5b"}, {"name": "qwen2.5-coder:3b"}]
        }
        if path == "/api/tags"
        else {"models": []},
    )

    assert bridge.status()["fast_model_available"] is True
    assert bridge.status()["base_model_available"] is True
    assert bridge.select_model("hola") == "qwen2.5:0.5b"
    assert bridge.select_model("codigo python") == "qwen2.5-coder:3b"


def test_ollama_bridge_honors_base_model_env(tmp_path, monkeypatch):
    monkeypatch.setenv("BASE_MODEL", "qwen2.5:0.5b")
    bridge = OllamaBridge(runtime_root=tmp_path / "runtime")

    monkeypatch.setattr(
        bridge,
        "_get",
        lambda path, timeout: {"models": [{"name": "qwen2.5:0.5b"}, {"name": "qwen2.5-coder:3b"}]}
        if path == "/api/tags"
        else {"models": []},
    )

    assert bridge.status()["base_model"] == "qwen2.5:0.5b"
    assert bridge.select_model("codigo python") == "qwen2.5:0.5b"


def test_ollama_bridge_filters_cloud_models_by_default(tmp_path, monkeypatch):
    monkeypatch.delenv("WABI_ALLOW_CLOUD_MODELS", raising=False)
    bridge = OllamaBridge(runtime_root=tmp_path / "runtime")

    monkeypatch.setattr(
        bridge,
        "_get",
        lambda path, timeout: {"models": [{"name": "qwen3-coder:480b-cloud"}, {"name": "qwen2.5-coder:3b"}]}
        if path == "/api/tags"
        else {"models": []},
    )

    status = bridge.status()

    assert status["models"] == ["qwen2.5-coder:3b"]
    assert status["cloud_models_filtered"] == ["qwen3-coder:480b-cloud"]


def test_ollama_bridge_normalizes_host_without_scheme(tmp_path):
    bridge = OllamaBridge(runtime_root=tmp_path / "runtime", host="127.0.0.1:11434")

    assert bridge.host == "http://127.0.0.1:11434"


def test_ollama_bridge_generate_writes_artifact(tmp_path, monkeypatch):
    monkeypatch.delenv("BASE_MODEL", raising=False)
    bridge = OllamaBridge(runtime_root=tmp_path / "runtime")
    monkeypatch.setattr(
        bridge,
        "status",
        lambda: {
            "available": True,
            "models": ["qwen2.5:0.5b"],
            "running": [],
            "fast_model": "qwen2.5:0.5b",
            "coder_model": "qwen2.5-coder:3b",
            "fast_model_available": True,
            "coder_model_available": False,
        },
    )
    monkeypatch.setattr(bridge, "_post", lambda path, body, timeout: {"response": "respuesta local"})

    result = bridge.generate("hola")

    assert result.ok is True
    assert result.model == "qwen2.5:0.5b"
    assert result.output == "respuesta local"
    assert result.artifacts
