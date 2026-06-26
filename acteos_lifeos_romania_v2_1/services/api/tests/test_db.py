"""The DB engine factory must be inert unless ACTEOS_DATABASE_URL is set."""

from __future__ import annotations

from acteos_api.db import (
    DbSettings,
    get_content_repository,
    get_db_settings,
    get_engine,
)


def test_engine_is_none_without_url(monkeypatch):
    monkeypatch.delenv("ACTEOS_DATABASE_URL", raising=False)
    get_db_settings.cache_clear()
    get_engine.cache_clear()
    assert DbSettings().database_url is None
    assert get_engine() is None
    assert get_content_repository() is None
    get_db_settings.cache_clear()
    get_engine.cache_clear()


def test_settings_reads_url(monkeypatch):
    monkeypatch.setenv("ACTEOS_DATABASE_URL", "postgresql+psycopg://u:p@localhost:5432/acteos")
    get_db_settings.cache_clear()
    get_engine.cache_clear()
    settings = DbSettings()
    assert settings.database_url == "postgresql+psycopg://u:p@localhost:5432/acteos"
    get_db_settings.cache_clear()
    get_engine.cache_clear()
    monkeypatch.delenv("ACTEOS_DATABASE_URL", raising=False)
