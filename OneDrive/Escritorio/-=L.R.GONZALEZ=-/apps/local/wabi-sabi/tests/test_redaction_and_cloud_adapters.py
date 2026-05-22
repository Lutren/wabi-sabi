from wabi_sabi.core.cloud_adapters import build_cloud_adapters, extract_chat_text
from wabi_sabi.core.redaction import redact_mapping, redact_text


def test_redact_text_masks_env_secret_values():
    env = {"NVIDIA_API_KEY": "nvapi-test-secret-1234567890", "SAFE_VALUE": "visible"}

    text = redact_text("key=nvapi-test-secret-1234567890 safe=visible", env=env)

    assert "nvapi-test-secret" not in text
    assert "visible" in text
    assert "[REDACTED:NVIDIA_API_KEY" in text


def test_redact_mapping_masks_sensitive_fields():
    payload = {"api_key": "abc123456789", "nested": {"message": "Bearer abcdefghijklmnop"}}

    redacted = redact_mapping(payload, env={})

    assert redacted["api_key"].startswith("[REDACTED:api_key")
    assert "abcdefghijklmnop" not in redacted["nested"]["message"]


def test_redact_text_masks_aliyun_access_key_material():
    text = "AccessKey ID\nLTAI1234567890abcdef\nAccessKey Secret\nabcdefghijklmnopqrstuvwxyz123456"

    redacted = redact_text(text)

    assert "LTAI1234567890abcdef" not in redacted
    assert "abcdefghijklmnopqrstuvwxyz123456" not in redacted
    assert "AccessKey ID" in redacted


def test_cloud_adapters_are_blocked_by_default(tmp_path):
    adapters = build_cloud_adapters(
        runtime_root=tmp_path / "runtime",
        env={"NVIDIA_API_KEY": "nvapi-test-secret-1234567890"},
    )

    status = adapters["nvidia-nim"].status()
    result = adapters["nvidia-nim"].execute("hola")

    assert status["configured"] is True
    assert status["available"] is False
    assert result.ok is False
    assert result.action == "cloud_provider_disabled"


def test_cloud_adapter_status_exposes_model_profiles_without_secrets(tmp_path):
    adapters = build_cloud_adapters(
        runtime_root=tmp_path / "runtime",
        env={"NVIDIA_API_KEY": "nvapi-test-secret-1234567890", "WABI_NVIDIA_NIM_MODEL_ALIAS": "ultra"},
    )

    status = adapters["nvidia-nim"].status()
    aliases = {profile["alias"] for profile in status["model_catalog"]}

    assert status["model"] == "nvidia/llama-3.1-nemotron-ultra-253b-v1"
    assert {
        "ultra",
        "llama-70b",
        "super",
        "nano-30b",
        "nano-9b",
        "kimi",
        "deepseek",
        "mistral",
        "minimax",
        "glm",
    }.issubset(aliases)
    assert "nvapi-test-secret" not in str(status)


def test_cloud_adapter_uses_mocked_http_when_explicitly_enabled(tmp_path):
    calls = []

    def fake_post(url, headers, body, timeout):
        calls.append({"url": url, "headers": headers, "body": body, "timeout": timeout})
        return {"choices": [{"message": {"content": "respuesta segura"}}]}

    adapters = build_cloud_adapters(
        runtime_root=tmp_path / "runtime",
        env={"WABI_ALLOW_CLOUD_PROVIDERS": "1", "QWEN_API_KEY": "qwen-test-secret-1234567890"},
        http_post=fake_post,
    )

    result = adapters["qwen-cloud"].execute("responde breve", timeout=5)

    assert result.ok is True
    assert result.output == "respuesta segura"
    assert calls
    assert calls[0]["headers"]["Authorization"].startswith("Bearer ")


def test_cloud_adapter_resolves_nvidia_model_alias_for_mocked_http(tmp_path):
    calls = []

    def fake_post(url, headers, body, timeout):
        calls.append(body)
        return {"choices": [{"message": {"content": "ok"}}]}

    adapters = build_cloud_adapters(
        runtime_root=tmp_path / "runtime",
        env={
            "WABI_ALLOW_CLOUD_PROVIDERS": "1",
            "NVIDIA_API_KEY": "nvapi-test-secret-1234567890",
            "WABI_NVIDIA_NIM_MODEL_ALIAS": "nano-30b",
        },
        http_post=fake_post,
    )

    result = adapters["nvidia-nim"].execute("responde ok", timeout=5)

    assert result.ok is True
    assert calls[0]["model"] == "nvidia/nemotron-3-nano-30b-a3b"


def test_cloud_adapter_resolves_public_model_aliases_for_mocked_http(tmp_path):
    calls = []

    def fake_post(url, headers, body, timeout):
        calls.append(body)
        return {"choices": [{"message": {"content": "ok"}}]}

    adapters = build_cloud_adapters(
        runtime_root=tmp_path / "runtime",
        env={
            "WABI_ALLOW_CLOUD_PROVIDERS": "1",
            "NVIDIA_API_KEY": "nvapi-test-secret-1234567890",
            "WABI_NVIDIA_NIM_MODEL_ALIAS": "kimi",
        },
        http_post=fake_post,
    )

    result = adapters["nvidia-nim"].execute("responde ok", timeout=5)

    assert result.ok is True
    assert calls[0]["model"] == "moonshotai/kimi-k2.6"


def test_cloud_adapter_resolves_qwen_model_alias_for_mocked_http(tmp_path):
    calls = []

    def fake_post(url, headers, body, timeout):
        calls.append(body)
        return {"choices": [{"message": {"content": "ok"}}]}

    adapters = build_cloud_adapters(
        runtime_root=tmp_path / "runtime",
        env={
            "WABI_ALLOW_CLOUD_PROVIDERS": "1",
            "QWEN_API_KEY": "qwen-test-secret-1234567890",
            "WABI_QWEN_MODEL_ALIAS": "qwen-235b",
        },
        http_post=fake_post,
    )

    result = adapters["qwen-cloud"].execute("responde ok", timeout=5)

    assert result.ok is True
    assert calls[0]["model"] == "qwen3-235b-a22b"


def test_extract_chat_text_supports_choices():
    payload = {"choices": [{"message": {"content": "uno"}}, {"message": {"content": [{"text": "dos"}]}}]}

    assert extract_chat_text(payload) == "uno\ndos"


def test_extract_chat_text_supports_reasoning_only_responses():
    payload = {"choices": [{"message": {"role": "assistant", "reasoning_content": "razonamiento"}}]}

    assert extract_chat_text(payload) == "razonamiento"
