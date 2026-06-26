"""Database settings + lazy engine factory.

The API serves from pure in-memory adapters by default; a PostgreSQL engine is
created only when ``ACTEOS_DATABASE_URL`` is configured. This keeps local dev
and the test suite free of a database dependency while making the production
adapter a one-env-var switch.
"""

from __future__ import annotations

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine

from .content_publish import SqlAlchemyContentRepository


class DbSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="ACTEOS_", extra="ignore")

    database_url: str | None = None
    db_echo: bool = False


@lru_cache(maxsize=1)
def get_db_settings() -> DbSettings:
    return DbSettings()


@lru_cache(maxsize=1)
def get_engine() -> Engine | None:
    settings = get_db_settings()
    if not settings.database_url:
        return None
    return create_engine(
        settings.database_url,
        echo=settings.db_echo,
        pool_pre_ping=True,
        future=True,
    )


def get_content_repository() -> SqlAlchemyContentRepository | None:
    engine = get_engine()
    if engine is None:
        return None
    return SqlAlchemyContentRepository(engine)
