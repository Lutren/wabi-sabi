from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from wabi_sabi.core.blueprint_policy import BlueprintPolicyLoader
from wabi_sabi.core.cloud_adapters import CLOUD_ENABLE_ENV, build_cloud_adapters
from wabi_sabi.core.codex_bridge import WabiCodexBridge
from wabi_sabi.core.ollama_bridge import OllamaBridge
from wabi_sabi.core.redaction import redact_mapping, redact_text


@dataclass
class OrchestratorResult:
    ok: bool
    provider: str
    action: str
    output: str
    artifacts: list[str] = field(default_factory=list)
    attempts: list[dict[str, Any]] = field(default_factory=list)
    error: str = ""
    status: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "ok": self.ok,
            "provider": self.provider,
            "action": self.action,
            "output": self.output,
            "artifacts": self.artifacts,
            "attempts": self.attempts,
            "error": self.error,
            "status": self.status,
        }


class ProviderOrchestrator:
    def __init__(self, *, workspace: str | Path, runtime_root: str | Path) -> None:
        self.workspace = Path(workspace).resolve()
        self.runtime_root = Path(runtime_root).resolve()
        self.codex = WabiCodexBridge(workspace=self.workspace, runtime_root=self.runtime_root)
        self.ollama = OllamaBridge(runtime_root=self.runtime_root)
        self.cloud_adapters = build_cloud_adapters(runtime_root=self.runtime_root)
        self.blueprint_policy = BlueprintPolicyLoader(
            workspace=self.workspace,
            runtime_root=self.runtime_root,
        ).load()

    def status(self) -> dict[str, Any]:
        codex = self.codex.status()
        ollama = self._ollama_status()
        order = self.provider_order()
        auto_provider = order[0] if order else codex.get("auto_provider", "dry-run")
        status = {
            "auto_provider": auto_provider,
            "provider_order": order,
            "codex": codex,
            "ollama": ollama,
            "cloud": {name: adapter.status() for name, adapter in self.cloud_adapters.items()},
            "blueprint_policy": self.blueprint_policy.to_dict(),
        }
        return redact_mapping(status)

    def provider_order(self) -> list[str]:
        if self._no_model_mode():
            return ["dry-run"]
        raw = os.environ.get("WABI_PROVIDER_ORDER")
        if raw is None:
            if os.environ.get(CLOUD_ENABLE_ENV, "0") == "1":
                # Cloud enabled: put configured cloud adapters first, local as fallback
                configured_cloud = [
                    name
                    for name, adapter in self.cloud_adapters.items()
                    if adapter.status().get("configured")
                ]
                local_part = ["ollama"] if self._base_model_ready() else []
                return configured_cloud + local_part + ["codex", "dry-run"]
            elif self._base_model_ready():
                raw = "ollama,codex,dry-run"
            else:
                raw = ",".join(self.blueprint_policy.provider_order)
        order = [item.strip().lower() for item in raw.split(",") if item.strip()]
        if not self._ollama_enabled():
            order = [item for item in order if item != "ollama"]
        return order or ["codex", "dry-run"]

    def warm_fast_models(self) -> None:
        if self._ollama_enabled():
            self.ollama.warm_async()

    def ask(self, prompt: str, *, provider: str = "auto", timeout: int = 180) -> OrchestratorResult:
        attempts: list[dict[str, Any]] = []
        order = self._resolve_order(provider)
        for candidate in order:
            alias_candidate = _nvidia_model_alias_candidate(candidate)
            if candidate in self.cloud_adapters:
                result = self.cloud_adapters[candidate].execute(prompt, timeout=timeout).to_dict()
                attempts.append(_attempt(candidate, result))
                if result["ok"]:
                    return self._success(candidate, result, attempts)
            elif alias_candidate:
                result = self.cloud_adapters["nvidia-nim"].execute(
                    prompt,
                    timeout=timeout,
                    model=alias_candidate,
                ).to_dict()
                attempts.append(_attempt(f"nvidia-nim:{alias_candidate}", result))
                if result["ok"]:
                    return self._success(f"nvidia-nim:{alias_candidate}", result, attempts)
            elif candidate == "codex":
                result = self.codex.ask(prompt, provider="auto", timeout=timeout).to_dict()
                attempts.append(_attempt("codex", result))
                if result["ok"]:
                    return self._success("codex", result, attempts)
            elif candidate == "codex-cli":
                result = self.codex.ask(prompt, provider="codex-cli", timeout=timeout).to_dict()
                attempts.append(_attempt("codex-cli", result))
                if result["ok"]:
                    return self._success("codex-cli", result, attempts)
            elif candidate == "openai-responses":
                result = self.codex.ask(prompt, provider="openai-responses", timeout=timeout).to_dict()
                attempts.append(_attempt("openai-responses", result))
                if result["ok"]:
                    return self._success("openai-responses", result, attempts)
            elif candidate == "ollama":
                ollama_timeout = int(os.environ.get("WABI_OLLAMA_TIMEOUT", "45"))
                result = self.ollama.generate(prompt, timeout=ollama_timeout).to_dict()
                attempts.append(_attempt("ollama", result))
                if result["ok"]:
                    return self._success("ollama", result, attempts)
            elif candidate == "nvidia":
                result = self.cloud_adapters["nvidia-nim"].execute(prompt, timeout=timeout).to_dict()
                attempts.append(_attempt("nvidia-nim", result))
                if result["ok"]:
                    return self._success("nvidia-nim", result, attempts)
            elif candidate == "qwen":
                result = self.cloud_adapters["qwen-cloud"].execute(prompt, timeout=timeout).to_dict()
                attempts.append(_attempt("qwen-cloud", result))
                if result["ok"]:
                    return self._success("qwen-cloud", result, attempts)
            elif candidate == "dry-run":
                result = self.codex.ask(prompt, provider="dry-run", dry_run=True, timeout=timeout).to_dict()
                attempts.append(_attempt("dry-run", result))
                if result["ok"]:
                    return self._success("dry-run", result, attempts)

        last_error = attempts[-1].get("error", "") if attempts else "no_provider_attempted"
        return OrchestratorResult(
            ok=False,
            provider="none",
            action="provider_orchestration_failed",
            output="Ningun proveedor pudo responder.",
            attempts=attempts,
            error=last_error,
            status=self.status(),
        )

    def _resolve_order(self, provider: str) -> list[str]:
        if self._no_model_mode():
            return ["dry-run"]
        if provider == "auto":
            return self.provider_order()
        if provider == "dry-run":
            return ["dry-run"]
        if provider == "ollama":
            if not self._ollama_enabled():
                return ["dry-run"]
            return ["ollama", "dry-run"]
        if provider == "nvidia":
            return ["nvidia-nim", "dry-run"]
        if provider == "qwen":
            return ["qwen-cloud", "dry-run"]
        if provider == "gemini":
            return ["gemini", "dry-run"]
        if provider in {"huggingface", "hf", "hugging-face"}:
            return ["huggingface", "dry-run"]
        if provider in {"cloudflare", "cf", "workers-ai", "cloudflare-workers-ai"}:
            return ["cloudflare", "dry-run"]
        if provider == "local":
            if not self._ollama_enabled():
                return ["dry-run"]
            return ["ollama", "dry-run"]
        if provider in self.cloud_adapters:
            return [provider, "dry-run"]
        provider_alias = _nvidia_model_alias_candidate(provider)
        if provider_alias:
            return [provider_alias, "dry-run"]
        return [provider, "dry-run"]

    def _ollama_status(self) -> dict[str, Any]:
        if not self._ollama_enabled():
            reason = "no_model_mode" if self._no_model_mode() else "base_model_unavailable_or_disabled"
            return {
                "enabled": False,
                "available": False,
                "reason": reason,
                "model_status": "UNAVAILABLE",
                "enable_env": "BASE_MODEL=qwen2.5-coder:3b or WABI_ENABLE_OLLAMA=1",
                "disable_env": "MEDIOEVO_NO_MODEL_MODE=1 or MEDIOEVO_DISABLE_OLLAMA=1 or MEDIOEVO_LIVE_LLM=0 or WABI_DISABLE_BASE_MODEL=1",
                "blueprint_reason": "base_model_primary_when_available",
            }
        status = self.ollama.status()
        status["enabled"] = True
        return status

    def _ollama_enabled(self) -> bool:
        if self._no_model_mode():
            return False
        if os.environ.get("MEDIOEVO_DISABLE_OLLAMA", "0") == "1":
            return False
        if os.environ.get("WABI_DISABLE_BASE_MODEL", "0") == "1":
            return False
        if os.environ.get("WABI_ENABLE_OLLAMA", "0") == "1":
            return True
        if os.environ.get("BASE_MODEL") or os.environ.get("MODEL_ENDPOINT"):
            return True
        return self._base_model_ready()

    def _base_model_ready(self) -> bool:
        status = self.ollama.status()
        return bool(status.get("base_model_available") or status.get("available"))

    def _no_model_mode(self) -> bool:
        return (
            os.environ.get("MEDIOEVO_NO_MODEL_MODE", "0") == "1"
            or os.environ.get("MEDIOEVO_LIVE_LLM", "1") == "0"
        )

    def _success(self, provider: str, result: dict[str, Any], attempts: list[dict[str, Any]]) -> OrchestratorResult:
        return OrchestratorResult(
            ok=True,
            provider=provider,
            action=f"{provider}_response",
            output=redact_text(result.get("output", "")),
            artifacts=list(result.get("artifacts", [])),
            attempts=attempts,
            status=self.status(),
        )


def _attempt(provider: str, result: dict[str, Any]) -> dict[str, Any]:
    return {
        "provider": provider,
        "ok": bool(result.get("ok")),
        "action": result.get("action", ""),
        "output": redact_text(str(result.get("output", ""))[:500]),
        "error": redact_text(str(result.get("error", ""))),
        "artifacts": result.get("artifacts", []),
    }


def _nvidia_model_alias_candidate(candidate: str) -> str:
    normalized = candidate.strip().lower()
    aliases = {
        "ultra": "ultra",
        "nemotron-ultra": "ultra",
        "llama-70b": "llama-70b",
        "super": "super",
        "nemotron-super": "super",
        "nano-30b": "nano-30b",
        "nemotron-nano-30b": "nano-30b",
        "nano-9b": "nano-9b",
        "nemotron-nano-9b": "nano-9b",
        "deepseek": "deepseek",
        "deepseek-v4": "deepseek",
        "deepseek-v4-pro": "deepseek",
        "kimi": "kimi",
        "kimi-k2.6": "kimi",
        "moonshot": "kimi",
        "minimax": "minimax",
        "minimax-m2.7": "minimax",
        "mistral": "mistral",
        "mistral-medium": "mistral",
        "mistral-medium-3.5": "mistral",
        "glm": "glm",
        "glm4.7": "glm",
        "z-ai": "glm",
    }
    return aliases.get(normalized, "")
