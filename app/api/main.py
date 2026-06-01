from __future__ import annotations

import logging
import time
import uuid
from collections.abc import Awaitable, Callable

from fastapi import FastAPI, Request, Response

from app.api.routers import health, metadata
from app.core.config import get_settings
from app.core.logging import configure_logging
from app.core.request_context import reset_request_id, set_request_id


def create_app() -> FastAPI:
    settings = get_settings()
    configure_logging(settings.log_level)

    app = FastAPI(title=settings.app_name)
    app.include_router(health.router)
    app.include_router(metadata.router)

    @app.middleware("http")
    async def request_context_middleware(
        request: Request,
        call_next: Callable[[Request], Awaitable[Response]],
    ) -> Response:
        request_id = request.headers.get("x-request-id") or str(uuid.uuid4())
        token = set_request_id(request_id)
        started = time.perf_counter()
        try:
            response = await call_next(request)
        finally:
            elapsed_ms = round((time.perf_counter() - started) * 1000, 2)
            logging.getLogger("text2sql.request").info(
                "request finished",
                extra={
                    "method": request.method,
                    "path": request.url.path,
                    "elapsed_ms": elapsed_ms,
                },
            )
            reset_request_id(token)

        response.headers["x-request-id"] = request_id
        return response

    return app


app = create_app()
