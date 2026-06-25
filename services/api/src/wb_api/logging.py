"""Structured JSON logging with per-request correlation ids.

Logs are machine-parseable, carry a request id, and must never contain raw PII
or document content (10_SECURITY_PRIVACY §8). The correlation id doubles as the
``trace_id`` returned in problem responses so a user-reported error can be tied
to a server log line without exposing internals.
"""
from __future__ import annotations

import json
import logging
import sys
import uuid
from contextvars import ContextVar

_request_id: ContextVar[str] = ContextVar("wb_request_id", default="-")

# Keys that must never be logged in clear, even if present on a record's extra.
_DENYLIST = {"facts", "value", "message", "payload", "note", "email", "token", "authorization"}


def new_request_id() -> str:
    return uuid.uuid4().hex


def set_request_id(value: str) -> str:
    _request_id.set(value)
    return value


def get_request_id() -> str:
    return _request_id.get()


class JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        entry = {
            "ts": self.formatTime(record, "%Y-%m-%dT%H:%M:%S%z"),
            "level": record.levelname,
            "logger": record.name,
            "msg": record.getMessage(),
            "request_id": get_request_id(),
        }
        for key, value in getattr(record, "context", {}).items():
            if key not in _DENYLIST:
                entry[key] = value
        if record.exc_info:
            entry["exc"] = self.formatException(record.exc_info)
        return json.dumps(entry, ensure_ascii=False, separators=(",", ":"))


def configure_logging(level: str = "INFO") -> None:
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(JsonFormatter())
    root = logging.getLogger()
    root.handlers[:] = [handler]
    root.setLevel(level.upper())
    # Uvicorn access logs are redundant with our structured middleware logging.
    logging.getLogger("uvicorn.access").handlers[:] = []


def log_event(logger: logging.Logger, level: int, msg: str, **context) -> None:
    logger.log(level, msg, extra={"context": context})
