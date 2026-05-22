from __future__ import annotations

import getpass
import os
from dataclasses import asdict, dataclass
from typing import Callable


SECRET_ENV_KEYS = {
    "NVIDIA_API_KEY",
    "NVIDIA_NIM_API_KEY",
    "DASHSCOPE_API_KEY",
    "QWEN_API_KEY",
    "ALIBABA_CLOUD_API_KEY",
    "DEEPSEEK_API_KEY",
    "OPENROUTER_API_KEY",
    "OPENAI_COMPATIBLE_API_KEY",
    "GEMINI_API_KEY",
    "GOOGLE_API_KEY",
    "HF_TOKEN",
    "HUGGINGFACE_API_KEY",
    "HUGGING_FACE_HUB_TOKEN",
    "CLOUDFLARE_API_TOKEN",
    "CLOUDFLARE_WORKERS_AI_TOKEN",
}

SAFE_CONFIG_ENV_KEYS = {
    "DEEPSEEK_BASE_URL",
    "OPENAI_COMPATIBLE_BASE_URL",
    "OPENAI_COMPATIBLE_MODEL",
    "CLOUDFLARE_ACCOUNT_ID",
}


PROVIDERS: dict[str, dict[str, object]] = {
    "nvidia": {
        "display": "NVIDIA",
        "env_keys": ("NVIDIA_API_KEY", "NVIDIA_NIM_API_KEY"),
        "base_url": "https://integrate.api.nvidia.com/v1",
        "default_model": "nvidia/nemotron-3-super-120b-a12b",
        "notes": "Ya es el proveedor cloud gratis funcional si el smoke esta PASS.",
    },
    "qwen": {
        "display": "Qwen / DashScope",
        "env_keys": ("DASHSCOPE_API_KEY", "QWEN_API_KEY", "ALIBABA_CLOUD_API_KEY"),
        "base_url": "https://dashscope.aliyuncs.com/compatible-mode/v1",
        "default_model": "qwen-plus",
        "notes": "Usa modo OpenAI-compatible de DashScope.",
    },
    "deepseek": {
        "display": "DeepSeek",
        "env_keys": ("DEEPSEEK_API_KEY",),
        "base_url": "https://api.deepseek.com/v1",
        "default_model": "deepseek-chat",
        "notes": "Usa API OpenAI-compatible /chat/completions.",
    },
    "openrouter": {
        "display": "OpenRouter",
        "env_keys": ("OPENROUTER_API_KEY",),
        "base_url": "https://openrouter.ai/api/v1",
        "default_model": "deepseek/deepseek-chat",
        "notes": "Fallback OpenAI-compatible con catalogo externo.",
    },
    "openai_compatible": {
        "display": "OpenAI-compatible custom",
        "env_keys": ("OPENAI_COMPATIBLE_API_KEY",),
        "base_url": "set OPENAI_COMPATIBLE_BASE_URL",
        "default_model": "set OPENAI_COMPATIBLE_MODEL",
        "notes": "Para cualquier proveedor gratis compatible con /chat/completions.",
    },
    "gemini": {
        "display": "Google Gemini",
        "env_keys": ("GEMINI_API_KEY", "GOOGLE_API_KEY"),
        "base_url": "https://generativelanguage.googleapis.com/v1beta/openai/chat/completions",
        "default_model": "gemini-2.0-flash",
        "notes": "OpenAI-compatible via Google AI Studio. Tier gratuito generoso. Modelos: flash, flash-lite, pro.",
    },
    "huggingface": {
        "display": "Hugging Face Router",
        "env_keys": ("HF_TOKEN", "HUGGINGFACE_API_KEY", "HUGGING_FACE_HUB_TOKEN"),
        "base_url": "https://router.huggingface.co/v1/chat/completions",
        "default_model": "Qwen/Qwen2.5-Coder-32B-Instruct",
        "notes": "Router OpenAI-compatible. Tier gratuito. Modelos: qwen-coder, llama-70b, llama-8b.",
    },
    "cloudflare": {
        "display": "Cloudflare Workers AI",
        "env_keys": ("CLOUDFLARE_API_TOKEN", "CLOUDFLARE_WORKERS_AI_TOKEN"),
        "base_url": "https://api.cloudflare.com/client/v4/accounts/<CLOUDFLARE_ACCOUNT_ID>/ai/v1",
        "default_model": "@cf/meta/llama-3.3-70b-instruct-fp8-fast",
        "notes": "OpenAI-compatible. Requiere CLOUDFLARE_ACCOUNT_ID ademas del token. Tier gratuito diario.",
    },
}


@dataclass(frozen=True)
class ProviderSetupStatus:
    provider: str
    display: str
    env_keys: tuple[str, ...]
    presence: dict[str, str]
    configured: bool
    base_url: str
    default_model: str
    next_action: str
    notes: str

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


def provider_setup_status(provider: str) -> ProviderSetupStatus:
    normalized = normalize_provider(provider)
    spec = PROVIDERS[normalized]
    env_keys = tuple(str(key) for key in spec["env_keys"])
    presence = {key: env_presence(key) for key in env_keys}
    configured = any(state == "PRESENTE" for state in presence.values())
    if configured:
        next_action = "Ejecuta /providers o revisa smoke; no se necesita pegar clave."
    else:
        first_key = env_keys[0]
        next_action = f"Para captura oculta en REPL usa /secret {first_key}; no pegues la clave como mensaje normal."
    return ProviderSetupStatus(
        provider=normalized,
        display=str(spec["display"]),
        env_keys=env_keys,
        presence=presence,
        configured=configured,
        base_url=str(spec["base_url"]),
        default_model=str(spec["default_model"]),
        next_action=next_action,
        notes=str(spec["notes"]),
    )


def provider_onboarding_report(provider: str | None = None) -> dict[str, object]:
    names = (
        [normalize_provider(provider)]
        if provider
        else ["nvidia", "gemini", "huggingface", "cloudflare", "qwen", "deepseek", "openrouter", "openai_compatible"]
    )
    statuses = [provider_setup_status(name).to_dict() for name in names]
    return {
        "schema": "wabi.provider_onboarding.v1",
        "secret_values_printed": False,
        "providers": statuses,
        "capture_rule": "Use hidden terminal prompt via /secret ENV_KEY; never paste key as a normal chat message.",
    }


def format_provider_onboarding(payload: dict[str, object]) -> str:
    lines = [
        "Provider setup seguro.",
        "No imprimo ni guardo claves en logs, WitnessLog ni handoff.",
        "Si falta una clave, usa captura oculta: /secret ENV_KEY.",
        "",
    ]
    for row in payload.get("providers", []):
        if not isinstance(row, dict):
            continue
        lines.append(f"{row['display']} ({row['provider']})")
        lines.append(f"- configured: {'YES' if row['configured'] else 'NO'}")
        lines.append(f"- base_url: {row['base_url']}")
        lines.append(f"- default_model: {row['default_model']}")
        presence = row.get("presence", {})
        if isinstance(presence, dict):
            for key, state in presence.items():
                lines.append(f"- {key}: {state}")
        lines.append(f"- next: {row['next_action']}")
        lines.append("")
    return "\n".join(lines).rstrip()


def normalize_provider(provider: str | None) -> str:
    raw = (provider or "").strip().lower().replace("-", "_")
    aliases = {
        "apis": "nvidia",
        "api": "nvidia",
        "gratis": "nvidia",
        "dashscope": "qwen",
        "dashscope_qwen": "qwen",
        "qwen_cloud": "qwen",
        "open_router": "openrouter",
        "compatible": "openai_compatible",
        "custom": "openai_compatible",
        "google": "gemini",
        "google_gemini": "gemini",
        "gem": "gemini",
        "flash": "gemini",
        "hf": "huggingface",
        "hugging_face": "huggingface",
        "hf_router": "huggingface",
        "cf": "cloudflare",
        "workers_ai": "cloudflare",
        "cloudflare_workers_ai": "cloudflare",
    }
    normalized = aliases.get(raw, raw)
    if normalized in PROVIDERS:
        return normalized
    return "nvidia"


def env_presence(key: str) -> str:
    if key not in os.environ:
        return "AUSENTE"
    if os.environ.get(key, "") == "":
        return "VACIA"
    return "PRESENTE"


def capture_secret_to_user_env(
    key: str,
    *,
    secret_getter: Callable[[str], str] | None = None,
    set_user_env: Callable[[str, str], None] | None = None,
) -> dict[str, object]:
    normalized = key.strip().upper()
    if normalized not in SECRET_ENV_KEYS and normalized not in SAFE_CONFIG_ENV_KEYS:
        return {
            "ok": False,
            "key": normalized,
            "status": "BLOCK",
            "reason": "ENV_KEY_NOT_ALLOWLISTED",
            "message": "Variable fuera del allowlist.",
            "secret_values_printed": False,
        }
    prompt = f"Valor para {normalized} (entrada oculta): "
    getter = secret_getter or getpass.getpass
    value = getter(prompt)
    if not value:
        return {
            "ok": False,
            "key": normalized,
            "status": "REVIEW",
            "reason": "EMPTY_INPUT",
            "message": "Entrada vacia; no se guardo nada.",
            "secret_values_printed": False,
        }
    setter = set_user_env or _set_user_env_var
    setter(normalized, value)
    os.environ[normalized] = value
    return {
        "ok": True,
        "key": normalized,
        "status": "PRESENTE",
        "reason": "SAVED_TO_USER_ENV",
        "message": "Guardada como User env var de Windows.",
        "secret_values_printed": False,
        "terminal_restart_may_be_required": True,
    }


def _set_user_env_var(key: str, value: str) -> None:
    if os.name != "nt":
        raise RuntimeError("user_env_write_only_supported_on_windows")
    import winreg

    with winreg.CreateKeyEx(winreg.HKEY_CURRENT_USER, "Environment", 0, winreg.KEY_SET_VALUE) as env_key:
        winreg.SetValueEx(env_key, key, 0, winreg.REG_EXPAND_SZ, value)
