from __future__ import annotations

import json
import math
import urllib.request
from typing import List, Optional


class OllamaEmbedder:
    """Cliente opcional para embeddings locales de Ollama.

    El kernel no depende de esto. Si Ollama no responde, usar TF-IDF fallback.
    """

    def __init__(self, model: str = "nomic-embed-text", endpoint: str = "http://localhost:11434/api/embeddings"):
        self.model = model
        self.endpoint = endpoint

    def embed(self, text: str, timeout: int = 30) -> Optional[List[float]]:
        payload = json.dumps({"model": self.model, "prompt": text[:8000]}).encode("utf-8")
        req = urllib.request.Request(self.endpoint, data=payload, headers={"Content-Type": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                data = json.loads(resp.read().decode("utf-8"))
            emb = data.get("embedding")
            return [float(x) for x in emb] if emb else None
        except Exception:
            return None


def vector_cosine(a: List[float], b: List[float]) -> float:
    if not a or not b or len(a) != len(b):
        return 0.0
    dot = sum(x * y for x, y in zip(a, b))
    na = math.sqrt(sum(x * x for x in a))
    nb = math.sqrt(sum(y * y for y in b))
    if na <= 0 or nb <= 0:
        return 0.0
    return dot / (na * nb)
