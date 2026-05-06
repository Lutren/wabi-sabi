from __future__ import annotations

from typing import Any

from ..core.engine import ContentForgeEngine

try:
    from fastapi import FastAPI, HTTPException
except Exception as exc:  # pragma: no cover
    FastAPI = None  # type: ignore
    HTTPException = None  # type: ignore
    FASTAPI_IMPORT_ERROR = exc
else:
    FASTAPI_IMPORT_ERROR = None


if FastAPI is not None:
    app = FastAPI(title="Content Forge Observacionista", version="1.0.0")
    engine = ContentForgeEngine()

    @app.get("/health")
    def health() -> dict[str, Any]:
        return engine.health()

    @app.post("/render")
    def render(payload: dict[str, Any]) -> dict[str, Any]:
        result = engine.render(payload)
        if not result.get("ok"):
            raise HTTPException(status_code=400, detail=result)
        return result

    @app.post("/carousel")
    def carousel(payload: dict[str, Any]) -> dict[str, Any]:
        result = engine.carousel(payload)
        if not result.get("ok"):
            raise HTTPException(status_code=400, detail=result)
        return result

    @app.get("/status/{job_id}")
    def status(job_id: str) -> dict[str, Any]:
        return engine.status(job_id)
else:  # pragma: no cover
    app = None
