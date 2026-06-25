"""SQLAlchemy 2.0 models for the persistence layer (PostgreSQL 17)."""
from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


def _new_uuid() -> str:
    return str(uuid.uuid4())


class Journey(Base):
    __tablename__ = "journeys"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_new_uuid)
    intent_id: Mapped[str] = mapped_column(String(200), index=True)
    jurisdiction_id: Mapped[str] = mapped_column(String(200), index=True)
    reference_date: Mapped[str] = mapped_column(String(10))
    # Ciphertext token from FieldCipher; raw citizen facts are never stored in clear.
    encrypted_facts: Mapped[str] = mapped_column(Text)
    facts_hash: Mapped[str] = mapped_column(String(80), index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    snapshots: Mapped[list["RouteSnapshot"]] = relationship(back_populates="journey")


class RouteSnapshot(Base):
    __tablename__ = "route_snapshots"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_new_uuid)
    journey_id: Mapped[str] = mapped_column(ForeignKey("journeys.id"), index=True)
    route_hash: Mapped[str] = mapped_column(String(80), index=True)
    rule_bundle_version: Mapped[str | None] = mapped_column(String(80), nullable=True)
    rule_bundle_hash: Mapped[str] = mapped_column(String(80))
    confidence: Mapped[str] = mapped_column(String(40))
    route: Mapped[dict] = mapped_column(JSONB)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    journey: Mapped[Journey] = relationship(back_populates="snapshots")


class AuditEvent(Base):
    __tablename__ = "audit_events"

    seq: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    prev_hash: Mapped[str] = mapped_column(String(80))
    entry_hash: Mapped[str] = mapped_column(String(80), unique=True)
    actor: Mapped[str] = mapped_column(String(200))
    action: Mapped[str] = mapped_column(String(120), index=True)
    payload: Mapped[dict] = mapped_column(JSONB)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class IdempotencyKey(Base):
    __tablename__ = "idempotency_keys"

    key: Mapped[str] = mapped_column(String(200), primary_key=True)
    request_hash: Mapped[str] = mapped_column(String(80))
    status: Mapped[str] = mapped_column(String(20))
    response: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
