from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Callable

from wabi_sabi.core.gate import ActionGate
from wabi_sabi.core.redaction import redact_mapping, redact_text
from wabi_sabi.core.tools import write_artifact


CLOUD_ENABLE_ENV = "WABI_ALLOW_CLOUD_PROVIDERS"


@dataclass
class CloudProviderResult:
    ok: bool
    provider: str
    gate: str
    action: str
    output: str
    artifacts: list[str] = field(default_factory=list)
    evidence: list[str] = field(default_factory=list)
    error: str = ""
    status: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return redact_mapping(asdict(self))


@dataclass(frozen=True)
class CloudModelProfile:
    alias: str
    model: str
    label: str
    use: str
    status: str
    source: str = ""

    def to_dict(self) -> dict[str, str]:
        return asdict(self)


class OpenAICompatibleChatAdapter:
    def __init__(
        self,
        *,
        name: str,
        runtime_root: str | Path,
        env_keys: list[str],
        base_url_env: str,
        default_base_url: str,
        model_env: str,
        default_model: str,
        model_alias_env: str,
        default_model_alias: str,
        model_profiles: list[CloudModelProfile],
        instructions: str,
        env: dict[str, str] | None = None,
        http_post: Callable[[str, dict[str, str], dict[str, Any], int], dict[str, Any]] | None = None,
    ) -> None:
        self.name = name
        self.runtime_root = Path(runtime_root)
        self.env = os.environ if env is None else env
        self.env_keys = env_keys
        self.base_url_env = base_url_env
        self.default_base_url = default_base_url
        self.model_env = model_env
        self.default_model = default_model
        self.model_alias_env = model_alias_env
        self.default_model_alias = default_model_alias
        self.model_profiles = model_profiles
        self.instructions = instructions
        self.http_post = http_post or _post_json

    def status(self) -> dict[str, Any]:
        api_key_name = self._api_key_name()
        enabled = self.env.get(CLOUD_ENABLE_ENV, "0") == "1"
        base_url = self.env.get(self.base_url_env, self.default_base_url)
        model = self.resolve_model()
        payload = {
            "provider": self.name,
            "configured": bool(api_key_name),
            "available": bool(api_key_name and enabled),
            "enabled": enabled,
            "enable_env": CLOUD_ENABLE_ENV,
            "env_keys": self.env_keys,
            "active_env_key": api_key_name or "",
            "base_url_env": self.base_url_env,
            "base_url_configured": bool(base_url),
            "model_env": self.model_env,
            "model_alias_env": self.model_alias_env,
            "default_model_alias": self.default_model_alias,
            "model": model,
            "requested_model": self._requested_model(),
            "model_catalog": self.model_catalog(),
            "configured_models_count": len(self.model_profiles),
            "network_policy": "blocked_by_default",
        }
        return redact_mapping(payload, env=self.env)

    def model_catalog(self) -> list[dict[str, str]]:
        return [profile.to_dict() for profile in self.model_profiles]

    def resolve_model(self, requested: str | None = None) -> str:
        candidate = (requested or self._requested_model()).strip()
        if not candidate:
            candidate = self.default_model_alias or self.default_model
        normalized = candidate.lower()
        for profile in self.model_profiles:
            if normalized in {profile.alias.lower(), profile.model.lower(), profile.label.lower()}:
                return profile.model
        return candidate

    def execute(self, prompt: str, *, timeout: int = 60, model: str | None = None) -> CloudProviderResult:
        gate = ActionGate().evaluate_text(prompt)
        status = self.status()
        if gate.gate == "BLOCK":
            return CloudProviderResult(
                ok=False,
                provider=self.name,
                gate=gate.gate,
                action="blocked_by_action_gate",
                output="ActionGate bloqueo el pedido antes de llamar a un proveedor cloud.",
                evidence=gate.reasons,
                error=";".join(gate.reasons),
                status=status,
            )
        if self.env.get(CLOUD_ENABLE_ENV, "0") != "1":
            return CloudProviderResult(
                ok=False,
                provider=self.name,
                gate="REVIEW",
                action="cloud_provider_disabled",
                output=f"{self.name} esta configurado como adapter, pero las llamadas cloud estan bloqueadas por defecto.",
                evidence=[f"set {CLOUD_ENABLE_ENV}=1 only after ActionGate approval"],
                error="cloud_provider_disabled",
                status=status,
            )
        api_key_name = self._api_key_name()
        api_key = self.env.get(api_key_name or "")
        if not api_key:
            return CloudProviderResult(
                ok=False,
                provider=self.name,
                gate="REVIEW",
                action="cloud_api_key_missing",
                output=f"{self.name} no tiene una clave configurada en el entorno.",
                error="cloud_api_key_missing",
                status=status,
            )
        url = self.env.get(self.base_url_env, self.default_base_url)
        model = self.resolve_model(model)
        body = {
            "model": model,
            "messages": [
                {"role": "system", "content": self.instructions},
                {"role": "user", "content": prompt},
            ],
            "temperature": float(self.env.get("WABI_CLOUD_TEMPERATURE", "0.2")),
            "max_tokens": int(self.env.get("WABI_CLOUD_MAX_TOKENS", "2048")),
        }
        headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
        try:
            response = self.http_post(url, headers, body, timeout)
        except Exception as exc:  # pragma: no cover - network failures vary by host
            return CloudProviderResult(
                ok=False,
                provider=self.name,
                gate=gate.gate,
                action="cloud_provider_error",
                output=f"La llamada a {self.name} fallo.",
                error=redact_text(str(exc), env=self.env),
                status=status,
            )
        output_text = extract_chat_text(response)
        artifact = write_artifact(
            self.runtime_root / "outputs",
            f"{self.name.replace('-', '_')}_response",
            ".md",
            redact_text(output_text, env=self.env) + "\n",
        )
        return CloudProviderResult(
            ok=bool(output_text),
            provider=self.name,
            gate=gate.gate,
            action="cloud_chat_completion",
            output=redact_text(output_text or "El proveedor cloud no devolvio texto extraible.", env=self.env),
            artifacts=[str(artifact)],
            evidence=[f"provider={self.name}", f"model={model}", f"artifact_written={artifact}"],
            status=status,
        )

    def _api_key_name(self) -> str | None:
        for key in self.env_keys:
            if self.env.get(key):
                return key
        return None

    def _requested_model(self) -> str:
        return (
            self.env.get(self.model_alias_env)
            or self.env.get("WABI_CLOUD_MODEL_ALIAS")
            or self.env.get(self.model_env)
            or self.default_model_alias
            or self.default_model
        )


def build_cloud_adapters(
    *,
    runtime_root: str | Path,
    env: dict[str, str] | None = None,
    http_post: Callable[[str, dict[str, str], dict[str, Any], int], dict[str, Any]] | None = None,
) -> dict[str, OpenAICompatibleChatAdapter]:
    values = os.environ if env is None else env
    shared_http_post = http_post or _post_json
    # Cloudflare Workers AI embeds the account id in the endpoint path. Without
    # an account id there is no usable URL, so the adapter is left unconfigured
    # (empty env_keys -> configured=False) instead of joining the order broken.
    cf_account = str(values.get("CLOUDFLARE_ACCOUNT_ID", "")).strip()
    cloudflare_base_url = (
        f"https://api.cloudflare.com/client/v4/accounts/{cf_account}/ai/v1/chat/completions"
        if cf_account
        else ""
    )
    cloudflare_env_keys = ["CLOUDFLARE_API_TOKEN", "CLOUDFLARE_WORKERS_AI_TOKEN"] if cf_account else []
    return {
        "nvidia-nim": OpenAICompatibleChatAdapter(
            name="nvidia-nim",
            runtime_root=runtime_root,
            env_keys=["NVIDIA_NIM_API_KEY", "NVIDIA_API_KEY"],
            base_url_env="NVIDIA_NIM_BASE_URL",
            default_base_url="https://integrate.api.nvidia.com/v1/chat/completions",
            model_env="WABI_NVIDIA_NIM_MODEL",
            default_model="nvidia/nemotron-3-super-120b-a12b",
            model_alias_env="WABI_NVIDIA_NIM_MODEL_ALIAS",
            default_model_alias="super",
            model_profiles=[
                CloudModelProfile(
                    alias="kimi",
                    model="moonshotai/kimi-k2.6",
                    label="Kimi K2.6",
                    use="long_context_reasoning_code",
                    status="provider_catalog_configured_network_blocked",
                    source="NVIDIA Integrate OpenAI-compatible route observed in authorized local provider notes",
                ),
                CloudModelProfile(
                    alias="deepseek",
                    model="deepseek-ai/deepseek-v4-pro",
                    label="DeepSeek V4 Pro",
                    use="reasoning_code_planning",
                    status="provider_catalog_configured_network_blocked",
                    source="NVIDIA Integrate OpenAI-compatible route observed in authorized local provider notes",
                ),
                CloudModelProfile(
                    alias="mistral",
                    model="mistralai/mistral-medium-3.5-128b",
                    label="Mistral Medium 3.5 128B",
                    use="reasoning_code_general_agent",
                    status="provider_catalog_configured_network_blocked",
                    source="NVIDIA Integrate OpenAI-compatible route observed in authorized local provider notes",
                ),
                CloudModelProfile(
                    alias="minimax",
                    model="minimaxai/minimax-m2.7",
                    label="MiniMax M2.7",
                    use="agent_reasoning_code",
                    status="provider_catalog_configured_network_blocked",
                    source="NVIDIA Integrate OpenAI-compatible route observed in authorized local provider notes",
                ),
                CloudModelProfile(
                    alias="glm",
                    model="z-ai/glm4.7",
                    label="GLM 4.7",
                    use="reasoning_code_general",
                    status="provider_catalog_configured_network_blocked",
                    source="NVIDIA Integrate OpenAI-compatible route observed in authorized local provider notes",
                ),
                CloudModelProfile(
                    alias="ultra",
                    model="nvidia/llama-3.1-nemotron-ultra-253b-v1",
                    label="Llama 3.1 Nemotron Ultra 253B",
                    use="max_reasoning_science_code",
                    status="provider_catalog_configured_network_blocked",
                    source="https://docs.api.nvidia.com/nim/reference/nvidia-llama-3_1-nemotron-ultra-253b-v1",
                ),
                CloudModelProfile(
                    alias="llama-70b",
                    model="nvidia/llama-3.1-nemotron-70b-instruct",
                    label="Llama 3.1 Nemotron 70B Instruct",
                    use="balanced_reasoning_instruction_following",
                    status="provider_catalog_configured_network_blocked",
                    source="https://build.nvidia.com/nvidia/llama-3_1-nemotron-70b-instruct",
                ),
                CloudModelProfile(
                    alias="super",
                    model="nvidia/nemotron-3-super-120b-a12b",
                    label="Nemotron 3 Super 120B A12B",
                    use="high_throughput_reasoning_code",
                    status="provider_catalog_configured_network_blocked",
                    source="https://docs.api.nvidia.com/nim/reference/nvidia-nemotron-3-super-120b-a12b",
                ),
                CloudModelProfile(
                    alias="nano-30b",
                    model="nvidia/nemotron-3-nano-30b-a3b",
                    label="Nemotron 3 Nano 30B A3B",
                    use="fast_agents_tools_low_latency",
                    status="provider_catalog_configured_network_blocked",
                    source="https://docs.api.nvidia.com/nim/reference/nvidia-nemotron-3-nano-30b-a3b",
                ),
                CloudModelProfile(
                    alias="nano-9b",
                    model="nvidia/nvidia-nemotron-nano-9b-v2",
                    label="NVIDIA Nemotron Nano 9B v2",
                    use="fast_triage_agents_low_latency",
                    status="provider_catalog_configured_network_blocked",
                    source="https://docs.api.nvidia.com/nim/reference/llm-apis",
                ),
            ],
            instructions=_cloud_instructions("NVIDIA NIM"),
            env=values,
            http_post=shared_http_post,
        ),
        "qwen-cloud": OpenAICompatibleChatAdapter(
            name="qwen-cloud",
            runtime_root=runtime_root,
            env_keys=["DASHSCOPE_API_KEY", "QWEN_API_KEY", "ALIBABA_CLOUD_API_KEY"],
            base_url_env="WABI_QWEN_BASE_URL",
            default_base_url="https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions",
            model_env="WABI_QWEN_MODEL",
            default_model="qwen-plus",
            model_alias_env="WABI_QWEN_MODEL_ALIAS",
            default_model_alias="qwen-plus",
            model_profiles=[
                CloudModelProfile(
                    alias="qwen-plus",
                    model="qwen-plus",
                    label="Qwen Plus",
                    use="agentic_coding_long_context_general",
                    status="provider_catalog_configured_network_blocked",
                    source="https://docs.qwencloud.com/developer-guides/getting-started/text-generation-models",
                ),
                CloudModelProfile(
                    alias="qwen3.6-plus",
                    model="qwen3.6-plus",
                    label="Qwen 3.6 Plus",
                    use="agentic_coding_long_context_general",
                    status="provider_catalog_configured_network_blocked",
                    source="https://docs.qwencloud.com/developer-guides/getting-started/text-generation-models",
                ),
                CloudModelProfile(
                    alias="qwen-235b",
                    model="qwen3-235b-a22b",
                    label="Qwen3 235B A22B",
                    use="hybrid_thinking_reasoning_code",
                    status="provider_catalog_configured_network_blocked",
                    source="https://docs.qwencloud.com/developer-guides/getting-started/text-generation-models",
                ),
            ],
            instructions=_cloud_instructions("Qwen cloud"),
            env=values,
            http_post=shared_http_post,
        ),
        "deepseek": OpenAICompatibleChatAdapter(
            name="deepseek",
            runtime_root=runtime_root,
            env_keys=["DEEPSEEK_API_KEY"],
            base_url_env="DEEPSEEK_BASE_URL",
            default_base_url="https://api.deepseek.com/v1/chat/completions",
            model_env="WABI_DEEPSEEK_MODEL",
            default_model="deepseek-chat",
            model_alias_env="WABI_DEEPSEEK_MODEL_ALIAS",
            default_model_alias="deepseek-chat",
            model_profiles=[
                CloudModelProfile(
                    alias="deepseek-chat",
                    model="deepseek-chat",
                    label="DeepSeek Chat",
                    use="coding_reasoning_chat",
                    status="provider_catalog_configured_network_blocked",
                    source="DeepSeek OpenAI-compatible API",
                ),
                CloudModelProfile(
                    alias="deepseek-reasoner",
                    model="deepseek-reasoner",
                    label="DeepSeek Reasoner",
                    use="complex_reasoning_code_planning",
                    status="provider_catalog_configured_network_blocked",
                    source="DeepSeek OpenAI-compatible API",
                ),
            ],
            instructions=_cloud_instructions("DeepSeek"),
            env=values,
            http_post=shared_http_post,
        ),
        "openrouter": OpenAICompatibleChatAdapter(
            name="openrouter",
            runtime_root=runtime_root,
            env_keys=["OPENROUTER_API_KEY"],
            base_url_env="OPENROUTER_BASE_URL",
            default_base_url="https://openrouter.ai/api/v1/chat/completions",
            model_env="WABI_OPENROUTER_MODEL",
            default_model="openai/gpt-5-mini",
            model_alias_env="WABI_OPENROUTER_MODEL_ALIAS",
            default_model_alias="openai/gpt-5-mini",
            model_profiles=[
                CloudModelProfile(
                    alias="default",
                    model="openai/gpt-5-mini",
                    label="OpenRouter configured default",
                    use="fallback_chat_code",
                    status="provider_catalog_configured_network_blocked",
                    source="OpenRouter OpenAI-compatible API",
                ),
            ],
            instructions=_cloud_instructions("OpenRouter"),
            env=values,
            http_post=shared_http_post,
        ),
        "openai-compatible": OpenAICompatibleChatAdapter(
            name="openai-compatible",
            runtime_root=runtime_root,
            env_keys=["OPENAI_COMPATIBLE_API_KEY"],
            base_url_env="OPENAI_COMPATIBLE_BASE_URL",
            default_base_url="",
            model_env="OPENAI_COMPATIBLE_MODEL",
            default_model="model-required",
            model_alias_env="OPENAI_COMPATIBLE_MODEL_ALIAS",
            default_model_alias="model-required",
            model_profiles=[
                CloudModelProfile(
                    alias="default",
                    model="model-required",
                    label="User configured OpenAI-compatible model",
                    use="custom_chat_code",
                    status="requires_operator_config",
                    source="OPENAI_COMPATIBLE_* user env",
                ),
            ],
            instructions=_cloud_instructions("OpenAI-compatible custom"),
            env=values,
            http_post=shared_http_post,
        ),
        "gemini": OpenAICompatibleChatAdapter(
            name="gemini",
            runtime_root=runtime_root,
            env_keys=["GEMINI_API_KEY", "GOOGLE_API_KEY"],
            base_url_env="GEMINI_BASE_URL",
            default_base_url="https://generativelanguage.googleapis.com/v1beta/openai/chat/completions",
            model_env="GEMINI_MODEL",
            default_model="gemini-2.0-flash",
            model_alias_env="WABI_GEMINI_MODEL_ALIAS",
            default_model_alias="flash",
            model_profiles=[
                CloudModelProfile(
                    alias="flash",
                    model="gemini-2.0-flash",
                    label="Gemini 2.0 Flash",
                    use="fast_chat_code_free_tier",
                    status="provider_catalog_configured_network_blocked",
                    source="https://generativelanguage.googleapis.com/v1beta/openai/",
                ),
                CloudModelProfile(
                    alias="flash-lite",
                    model="gemini-2.0-flash-lite",
                    label="Gemini 2.0 Flash-Lite",
                    use="fast_low_latency_free_tier",
                    status="provider_catalog_configured_network_blocked",
                    source="https://generativelanguage.googleapis.com/v1beta/openai/",
                ),
                CloudModelProfile(
                    alias="pro",
                    model="gemini-2.5-pro",
                    label="Gemini 2.5 Pro",
                    use="complex_reasoning_code",
                    status="provider_catalog_configured_network_blocked",
                    source="https://generativelanguage.googleapis.com/v1beta/openai/",
                ),
            ],
            instructions=_cloud_instructions("Gemini"),
            env=values,
            http_post=shared_http_post,
        ),
        "huggingface": OpenAICompatibleChatAdapter(
            name="huggingface",
            runtime_root=runtime_root,
            env_keys=["HF_TOKEN", "HUGGINGFACE_API_KEY", "HUGGING_FACE_HUB_TOKEN"],
            base_url_env="HF_BASE_URL",
            default_base_url="https://router.huggingface.co/v1/chat/completions",
            model_env="HF_MODEL",
            default_model="Qwen/Qwen2.5-Coder-32B-Instruct",
            model_alias_env="WABI_HF_MODEL_ALIAS",
            default_model_alias="qwen-coder",
            model_profiles=[
                CloudModelProfile(
                    alias="qwen-coder",
                    model="Qwen/Qwen2.5-Coder-32B-Instruct",
                    label="Qwen2.5 Coder 32B Instruct",
                    use="coding_reasoning_free_tier",
                    status="provider_catalog_configured_network_blocked",
                    source="https://router.huggingface.co/v1/",
                ),
                CloudModelProfile(
                    alias="llama-70b",
                    model="meta-llama/Llama-3.3-70B-Instruct",
                    label="Llama 3.3 70B Instruct",
                    use="general_reasoning_code",
                    status="provider_catalog_configured_network_blocked",
                    source="https://router.huggingface.co/v1/",
                ),
                CloudModelProfile(
                    alias="llama-8b",
                    model="meta-llama/Llama-3.1-8B-Instruct",
                    label="Llama 3.1 8B Instruct",
                    use="fast_chat_free_tier",
                    status="provider_catalog_configured_network_blocked",
                    source="https://router.huggingface.co/v1/",
                ),
            ],
            instructions=_cloud_instructions("HuggingFace"),
            env=values,
            http_post=shared_http_post,
        ),
        "cloudflare": OpenAICompatibleChatAdapter(
            name="cloudflare",
            runtime_root=runtime_root,
            env_keys=cloudflare_env_keys,
            base_url_env="CLOUDFLARE_AI_BASE_URL",
            default_base_url=cloudflare_base_url,
            model_env="CLOUDFLARE_AI_MODEL",
            default_model="@cf/meta/llama-3.3-70b-instruct-fp8-fast",
            model_alias_env="WABI_CLOUDFLARE_MODEL_ALIAS",
            default_model_alias="llama-70b",
            model_profiles=[
                CloudModelProfile(
                    alias="llama-70b",
                    model="@cf/meta/llama-3.3-70b-instruct-fp8-fast",
                    label="Llama 3.3 70B (Workers AI)",
                    use="general_reasoning_code_free_tier",
                    status="provider_catalog_configured_network_blocked",
                    source="https://developers.cloudflare.com/workers-ai/",
                ),
                CloudModelProfile(
                    alias="llama-8b",
                    model="@cf/meta/llama-3.1-8b-instruct",
                    label="Llama 3.1 8B (Workers AI)",
                    use="fast_chat_free_tier",
                    status="provider_catalog_configured_network_blocked",
                    source="https://developers.cloudflare.com/workers-ai/",
                ),
                CloudModelProfile(
                    alias="qwen-coder",
                    model="@cf/qwen/qwen2.5-coder-32b-instruct",
                    label="Qwen2.5 Coder 32B (Workers AI)",
                    use="coding_free_tier",
                    status="provider_catalog_configured_network_blocked",
                    source="https://developers.cloudflare.com/workers-ai/",
                ),
            ],
            instructions=_cloud_instructions("Cloudflare Workers AI"),
            env=values,
            http_post=shared_http_post,
        ),
    }


def extract_chat_text(response: dict[str, Any]) -> str:
    chunks: list[str] = []
    for choice in response.get("choices", []) or []:
        message = choice.get("message") or {}
        content = message.get("content")
        reasoning_content = message.get("reasoning_content")
        before_count = len(chunks)
        if isinstance(content, str):
            chunks.append(content)
        elif isinstance(content, list):
            for item in content:
                text = item.get("text") if isinstance(item, dict) else None
                if isinstance(text, str):
                    chunks.append(text)
        if len(chunks) == before_count and isinstance(reasoning_content, str) and reasoning_content.strip():
            chunks.append(reasoning_content)
        text = choice.get("text")
        if isinstance(text, str) and text.strip():
            chunks.append(text)
    return "\n".join(chunk.strip() for chunk in chunks if chunk.strip()).strip()


def _cloud_instructions(provider_label: str) -> str:
    return (
        f"Eres un proveedor {provider_label} conectado por Wabi-Sabi. "
        "Responde en espanol claro, no pidas secretos, no reveles credenciales, "
        "y no afirmes que ejecutaste cambios locales."
    )


def _post_json(url: str, headers: dict[str, str], body: dict[str, Any], timeout: int) -> dict[str, Any]:
    data = json.dumps(body).encode("utf-8")
    request = urllib.request.Request(url, data=data, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")[-2000:]
        raise RuntimeError(f"cloud_http_{exc.code}: {redact_text(detail)}") from exc
