"""FastAPI application factory for the ActeOS API (discovery slice).

Adds a request-id middleware and maps DiscoveryError + validation errors to the
ErrorResponse contract shape. Health endpoints are unauthenticated.
"""
from __future__ import annotations

import uuid

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from .discovery import DiscoveryError, router as discovery_router
from .schemas import MessageResponse

REQUEST_ID_HEADER = "X-Request-ID"


def _error_payload(code: str, message: str, request_id: str, retryable: bool, details: dict | None = None) -> dict:
    body: dict = {"code": code, "message": message, "request_id": request_id, "retryable": retryable}
    if details:
        body["details"] = details
    return {"error": body}


def create_app() -> FastAPI:
    app = FastAPI(
        title="ActeOS API",
        version="1.1.0",
        description="ActeOS / LifeOS România v2.1 — discovery slice (intent-first).",
    )

    @app.middleware("http")
    async def add_request_id(request: Request, call_next):  # type: ignore[no-untyped-def]
        request_id = request.headers.get(REQUEST_ID_HEADER) or str(uuid.uuid4())
        request.state.request_id = request_id
        response = await call_next(request)
        response.headers[REQUEST_ID_HEADER] = request_id
        return response

    @app.exception_handler(DiscoveryError)
    async def _discovery_error_handler(request: Request, exc: DiscoveryError) -> JSONResponse:
        request_id = getattr(request.state, "request_id", "")
        return JSONResponse(
            status_code=exc.status_code,
            content=_error_payload(exc.code, exc.message, request_id, exc.retryable),
        )

    @app.exception_handler(RequestValidationError)
    async def _validation_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
        request_id = getattr(request.state, "request_id", "")
        return JSONResponse(
            status_code=422,
            content=_error_payload(
                "VALIDATION_ERROR",
                "Cerere invalidă.",
                request_id,
                False,
                details={"errors": exc.errors()},
            ),
        )

    app.include_router(discovery_router)

    @app.get("/health/live", response_model=MessageResponse, tags=["Health"])
    def health_live() -> MessageResponse:
        return MessageResponse(message="alive")

    @app.get("/health/ready", response_model=MessageResponse, tags=["Health"])
    def health_ready() -> MessageResponse:
        return MessageResponse(message="ready")

    return app


app = create_app()
