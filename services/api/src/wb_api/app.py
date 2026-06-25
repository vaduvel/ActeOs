"""Application factory.

Builds the FastAPI app with structured logging, a per-request correlation id,
Problem+JSON exception handling, CORS, and all routers. Importing this module
has no side effects beyond defining ``create_app``; the ASGI instance lives in
``main``.
"""
from __future__ import annotations

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware

from .config import Settings, get_settings
from .errors import install_exception_handlers
from .logging import configure_logging, get_request_id, log_event, new_request_id, set_request_id
from .routers import api_router

REQUEST_ID_HEADER = "X-Request-Id"


class RequestContextMiddleware(BaseHTTPMiddleware):
    """Assign/propagate a correlation id and emit one structured access log."""

    async def dispatch(self, request: Request, call_next):
        incoming = request.headers.get(REQUEST_ID_HEADER)
        request_id = incoming or new_request_id()
        set_request_id(request_id)
        try:
            response = await call_next(request)
        except Exception:
            log_event("request.error", method=request.method, path=request.url.path)
            raise
        response.headers[REQUEST_ID_HEADER] = request_id
        log_event(
            "request.access", method=request.method, path=request.url.path,
            status=response.status_code,
        )
        return response


def _custom_openapi(app: FastAPI, settings: Settings):
    from fastapi.openapi.utils import get_openapi

    def openapi():
        if app.openapi_schema:
            return app.openapi_schema
        schema = get_openapi(
            title="Waze pentru Birocratie API",
            version=settings.service_version,
            description="Citizen-facing API for resolving bureaucratic routes from verified sources.",
            routes=app.routes,
            servers=[{"url": settings.public_base_url}],
        )
        schema.setdefault("components", {}).setdefault("securitySchemes", {})["curatorBearer"] = {
            "type": "oauth2",
            "flows": {"clientCredentials": {"tokenUrl": settings.oidc_token_url or "", "scopes": {}}},
        }
        app.openapi_schema = schema
        return schema

    return openapi


def create_app(settings: Settings | None = None) -> FastAPI:
    settings = settings or get_settings()
    configure_logging(level=settings.log_level, json_output=settings.json_logs)
    app = FastAPI(
        title="Waze pentru Birocratie API",
        version=settings.service_version,
        docs_url=None if settings.is_production else "/docs",
        redoc_url=None if settings.is_production else "/redoc",
        openapi_url="/openapi.json" if not settings.is_production else None,
    )
    app.add_middleware(RequestContextMiddleware)
    if settings.cors_origins:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=settings.cors_origins,
            allow_credentials=False,
            allow_methods=["GET", "POST", "PATCH", "DELETE", "OPTIONS"],
            allow_headers=["*"],
            expose_headers=[REQUEST_ID_HEADER],
        )
    install_exception_handlers(app)
    app.include_router(api_router)
    app.openapi = _custom_openapi(app, settings)
    return app
