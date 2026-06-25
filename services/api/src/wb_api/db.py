from __future__ import annotations

import os

from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session, sessionmaker


def get_database_url() -> str:
    return os.environ.get(
        "DATABASE_URL", "postgresql+psycopg://wb:wb@localhost:5432/wb"
    )


def make_engine(url: str | None = None, **kwargs) -> Engine:
    return create_engine(url or get_database_url(), future=True, **kwargs)


def make_session_factory(engine: Engine | None = None) -> sessionmaker[Session]:
    return sessionmaker(bind=engine or make_engine(), expire_on_commit=False, future=True)
