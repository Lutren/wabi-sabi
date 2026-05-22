from __future__ import annotations

import json
import os
import threading
import urllib.error
import urllib.request
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

from wabi_sabi.core.tools import write_artifact


DEFAULT_OLLAMA_HOST = "http://127.0.0.1:11434"
DEFAULT_FAST_MODEL = "qwen2.5:0.5b"
DEFAULT_CODER_MODEL = "qwen2.5-coder:3b"
DEFAULT_BASE_MODEL = DEFAULT_CODER_MODEL


@dataclass
class OllamaResult:
    ok: bool
    provider: str
    model: str
    action: str
    output: str
    artifacts: list[str] = field(default_factory=list)
    evidence: list[str] = field(default_factory=list)
    error: str = ""
    status: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


class OllamaBridge:
    def __init__(self, *, runtime_root: str | Path, host: str | None = None) -> None:
        self.runtime_root = Path(runtime_root)
        self.model_provider = os.environ.get("MODEL_PROVIDER", "ollama").strip().lower() or "ollama"
        model_endpoint = os.environ.get("MODEL_ENDPOINT")
        endpoint_host = model_endpoint if self.model_provider in {"ollama", "local", "installed_base_model"} else None
        raw_host = (host or endpoint_host or os.environ.get("OLLAMA_HOST") or DEFAULT_OLLAMA_HOST).rstrip("/")
        if not raw_host.startswith(("http://", "https://")):
            raw_host = "http://" + raw_host
        self.host = raw_host
        self.base_model = (
            os.environ.get("BASE_MODEL")
            or os.environ.get("WABI_BASE_MODEL")
            or os.environ.get("WABI_OLLAMA_BASE_MODEL")
            or DEFAULT_BASE_MODEL
        )
        self.base_model_explicit = bool(
            os.environ.get("BASE_MODEL")
            or os.environ.get("WABI_BASE_MODEL")
            or os.environ.get("WABI_OLLAMA_BASE_MODEL")
        )
        self.context_limit = os.environ.get("MODEL_CONTEXT_LIMIT") or os.environ.get("WABI_MODEL_CONTEXT_LIMIT") or ""
        self.fast_model = os.environ.get("WABI_OLLAMA_FAST_MODEL") or DEFAULT_FAST_MODEL
        self.coder_model = os.environ.get("WABI_OLLAMA_CODER_MODEL") or DEFAULT_CODER_MODEL

    def status(self) -> dict[str, Any]:
        tags = self._get("/api/tags", timeout=2)
        ps = self._get("/api/ps", timeout=2)
        raw_models = [item.get("name", "") for item in tags.get("models", []) if item.get("name")]
        running = [item.get("name", "") for item in ps.get("models", []) if item.get("name")]
        models = self._usable_models(raw_models)
        available = bool(models)
        return {
            "available": available,
            "host": self.host,
            "model_provider": self.model_provider,
            "model_endpoint": self.host,
            "context_limit": self.context_limit,
            "base_model": self.base_model,
            "models": models,
            "raw_models": raw_models,
            "cloud_models_filtered": [model for model in raw_models if model not in models],
            "running": running,
            "fast_model": self.fast_model,
            "coder_model": self.coder_model,
            "base_model_available": self.base_model in models,
            "fast_model_available": self.fast_model in models,
            "coder_model_available": self.coder_model in models,
        }

    def select_model(self, prompt: str, *, prefer_coder: bool = False) -> str | None:
        status = self.status()
        models = set(status["models"])
        if self.base_model_explicit and self.base_model in models:
            return self.base_model
        lowered = prompt.lower()
        code_like = any(word in lowered for word in ["codigo", "code", "python", "test", "refactor"])
        if prefer_coder or code_like:
            if self.coder_model in models:
                return self.coder_model
            if self.base_model in models:
                return self.base_model
        if self.fast_model in models:
            return self.fast_model
        if self.base_model in models:
            return self.base_model
        return status["models"][0] if status["models"] else None

    def generate(
        self,
        prompt: str,
        *,
        model: str | None = None,
        timeout: int = 60,
        num_predict: int = 64,
    ) -> OllamaResult:
        selected = model or self.select_model(prompt)
        status = self.status()
        if not selected:
            return OllamaResult(
                ok=False,
                provider="ollama",
                model="",
                action="ollama_model_missing",
                output="No hay modelo Ollama local disponible.",
                error="no_ollama_model_available",
                status=status,
            )
        body = {
            "model": selected,
            "prompt": build_ollama_prompt(prompt),
            "stream": False,
            "keep_alive": os.environ.get("WABI_OLLAMA_KEEP_ALIVE", "30m"),
            "options": {
                "num_ctx": int(os.environ.get("WABI_OLLAMA_NUM_CTX", "512")),
                "num_predict": num_predict,
                "temperature": float(os.environ.get("WABI_OLLAMA_TEMPERATURE", "0.2")),
            },
        }
        try:
            response = self._post("/api/generate", body, timeout=timeout)
        except Exception as exc:
            return OllamaResult(
                ok=False,
                provider="ollama",
                model=selected,
                action="ollama_generate_error",
                output="Ollama local fallo o tardo demasiado.",
                error=str(exc),
                status=status,
            )
        text = str(response.get("response", "")).strip()
        artifact = write_artifact(self.runtime_root / "outputs", "ollama_response", ".md", text + "\n")
        return OllamaResult(
            ok=bool(text),
            provider="ollama",
            model=selected,
            action="ollama_generate",
            output=text or "Ollama no devolvio texto.",
            artifacts=[str(artifact)],
            evidence=[
                f"model={selected}",
                f"base_model={self.base_model}",
                f"fallback_used={str(selected != self.base_model).lower()}",
                f"artifact_written={artifact}",
            ],
            status=self.status(),
        )

    def warm_async(self, *, model: str | None = None) -> None:
        if os.environ.get("WABI_OLLAMA_PREWARM", "0") != "1":
            return
        selected = model or self.select_model("estado rapido")
        if not selected:
            return
        thread = threading.Thread(target=self._warm, args=(selected,), daemon=True)
        thread.start()

    def _warm(self, model: str) -> None:
        try:
            self.generate("Responde OK.", model=model, timeout=90, num_predict=2)
        except Exception:
            return

    def _get(self, path: str, *, timeout: int) -> dict[str, Any]:
        try:
            with urllib.request.urlopen(self.host + path, timeout=timeout) as response:
                return json.loads(response.read().decode("utf-8"))
        except Exception:
            return {}

    def _usable_models(self, models: list[str]) -> list[str]:
        if os.environ.get("WABI_ALLOW_CLOUD_MODELS", "0") == "1":
            return models
        return [model for model in models if not (model.endswith(":cloud") or model.endswith("-cloud"))]

    def _post(self, path: str, body: dict[str, Any], *, timeout: int) -> dict[str, Any]:
        data = json.dumps(body).encode("utf-8")
        request = urllib.request.Request(
            self.host + path,
            data=data,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        try:
            with urllib.request.urlopen(request, timeout=timeout) as response:
                return json.loads(response.read().decode("utf-8"))
        except urllib.error.HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="replace")[-2000:]
            raise RuntimeError(f"ollama_http_{exc.code}: {detail}") from exc


def build_ollama_prompt(prompt: str) -> str:
    return (
        "Eres Wabi-Sabi local. Responde breve, operativo y en espanol. "
        "Maximo tres frases. "
        "No hagas acciones externas, no pidas secretos, no prometas cambios aplicados.\n\n"
        f"Pedido: {prompt}\n"
    )
