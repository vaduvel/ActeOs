"""RFC 9457 problem details and exception handling.

Every error leaving the API is a ``application/problem+json`` document matching
`contracts/problem.schema.json`: it always carries ``type``, ``title``,
``status``, ``code`` and ``trace_id``. Internal detail and stack traces are
never exposed in production (10_SECURITY_PRIVACY §8).
"""
from __future__ import annotations

import logging
from typing import Any

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from starlette.exceptions import HTTPException as StarletteHTTPException

from .config import get_settings
from .logging import get_request_id, log_event

log = logging.getLogger("wb_api.errors")

PROBLEM_BASE = "https://schemas.example.invalid/waze-birocratie/problems"
PROBLEM_MEDIA_TYPE = "application/problem+json"


class FieldError(BaseModel):
    path: str
    code: str
    message: str


class Problem(BaseModel):
    type: str
    title: str
    status: int
    code: str
    detail: str | None = None
    instance: str | None = None
    trace_id: str
    field_errors: list[FieldError] | None = None


class AppError(Exception):
    """Base for errors that map deterministically to a problem response."""

    status: int = 500
    code: str = "internal_error"
    title: str = "Internal Server Error"

    def __init__(self, detail: str | None = None, *, field_errors: list[FieldError] | None = None, code: str | None = None, title: str | None = None):
        super().__init__(detail or self.title)
        self.detail = detail
        self.field_errors = field_errors
        if code:
            self.code = code
        if title:
            self.title = title


class ValidationProblem(AppError):
    status = 422
    code = "validation_error"
    title = "Unprocessable Entity"


class NotFoundError(AppError):
    status = 404
    code = "not_found"
    title = "Not Found"


class ConflictProblem(AppError):
    status = 409
    code = "conflict"
    title = "Conflict"


class UnauthorizedError(AppError):
    status = 401
    code = "unauthorized"
    title = "Unauthorized"


class ForbiddenError(AppError):
    status = 403
    code = "forbidden"
    title = "Forbidden"


class ServiceUnavailableError(AppError):
    status = 503
    code = "service_unavailable"
    title = "Service Unavailable"


def _problem_response(
    *, status: int, code: str, title: str, detail: str | None, instance: str | None, field_errors: list[FieldError] | None
) -> JSONResponse:
    problem = Problem(
        type=f"{PROBLEM_BASE}/{code}",
        title=title,
        status=status,
        code=code,
        detail=detail,
        instance=instance,
        trace_id=get_request_id(),
        field_errors=field_errors,
    )
    return JSONResponse(
        status_code=status,
        media_type=PROBLEM_MEDIA_TYPE,
        content=problem.model_dump(exclude_none=True),
    )


def _engine_problem(exc: Exception) -> tuple[int, str, str]:
    """Map deterministic rule-engine errors to status/code/title."""
    name = type(exc).__name__
    mapping = {
        "InvalidRequest": (422, "invalid_request", "Unprocessable Entity"),
        "NoApplicableRule": (409, "no_applicable_rule", "Conflict"),
        "RuleConflict": (409, "rule_conflict", "Conflict"),
        "DependencyCycle": (409, "dependency_cycle", "Conflict"),
    }
    return mapping.get(name, (500, "engine_error", "Internal Server Error"))


def install_exception_handlers(app: FastAPI) -> None:
    settings = get_settings()

    @app.exception_handler(AppError)
    async def _app_error(request: Request, exc: AppError):  # noqa: ANN202
        if exc.status >= 500:
            log_event(log, logging.ERROR, "app_error", code=exc.code, path=request.url.path)
        return _problem_response(
            status=exc.status, code=exc.code, title=exc.title,
            detail=exc.detail, instance=request.url.path, field_errors=exc.field_errors,
        )

    @app.exception_handler(RequestValidationError)
    async def _validation(request: Request, exc: RequestValidationError):  # noqa: ANN202
        field_errors = [
            FieldError(
                path=".".join(str(p) for p in err.get("loc", []) if p not in ("body",)),
                code=str(err.get("type", "invalid")).replace(".", "_"),
                message=err.get("msg", "invalid"),
            )
            for err in exc.errors()
        ]
        return _problem_response(
            status=422, code="validation_error", title="Unprocessable Entity",
            detail="Request body failed validation.", instance=request.url.path, field_errors=field_errors,
        )

    @app.exception_handler(StarletteHTTPException)
    async def _http(request: Request, exc: StarletteHTTPException):  # noqa: ANN202
        code = {401: "unauthorized", 403: "forbidden", 404: "not_found", 405: "method_not_allowed"}.get(exc.status_code, "http_error")
        return _problem_response(
            status=exc.status_code, code=code, title=str(exc.detail or "Error"),
            detail=str(exc.detail) if exc.detail else None, instance=request.url.path, field_errors=None,
        )

    @app.exception_handler(Exception)
    async def _unhandled(request: Request, exc: Exception):  # noqa: ANN202
        # Deterministic engine errors carry domain meaning even though they are
        # not AppError subclasses; map them explicitly.
        module = type(exc).__module__
        if module.startswith("wb_rule_engine"):
            status, code, title = _engine_problem(exc)
            detail = str(exc) if not settings.is_production or status < 500 else None
            if status >= 500:
                log_event(log, logging.ERROR, "engine_error", code=code, path=request.url.path)
            return _problem_response(status=status, code=code, title=title, detail=detail, instance=request.url.path, field_errors=None)
        log_event(log, logging.ERROR, "unhandled_exception", error_type=type(exc).__name__, path=request.url.path)
        detail = None if settings.is_production else f"{type(exc).__name__}: {exc}"
        return _problem_response(
            status=500, code="internal_error", title="Internal Server Error",
            detail=detail, instance=request.url.path, field_errors=None,
        )
