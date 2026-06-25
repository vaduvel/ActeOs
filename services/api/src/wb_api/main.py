"""ASGI entrypoint. Run with: ``uvicorn wb_api.main:app``."""
from __future__ import annotations

from .app import create_app

app = create_app()
