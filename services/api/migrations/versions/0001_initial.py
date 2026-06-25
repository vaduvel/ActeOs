"""initial schema: journeys, route snapshots, append-only audit, idempotency

Revision ID: 0001
Revises:
Create Date: 2026-06-25
"""
from __future__ import annotations

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = "0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "journeys",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("intent_id", sa.String(length=200), nullable=False),
        sa.Column("jurisdiction_id", sa.String(length=200), nullable=False),
        sa.Column("reference_date", sa.String(length=10), nullable=False),
        sa.Column("encrypted_facts", sa.Text(), nullable=False),
        sa.Column("facts_hash", sa.String(length=80), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_index("ix_journeys_intent_id", "journeys", ["intent_id"])
    op.create_index("ix_journeys_jurisdiction_id", "journeys", ["jurisdiction_id"])
    op.create_index("ix_journeys_facts_hash", "journeys", ["facts_hash"])

    op.create_table(
        "route_snapshots",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("journey_id", sa.String(length=36), sa.ForeignKey("journeys.id"), nullable=False),
        sa.Column("route_hash", sa.String(length=80), nullable=False),
        sa.Column("rule_bundle_version", sa.String(length=80), nullable=True),
        sa.Column("rule_bundle_hash", sa.String(length=80), nullable=False),
        sa.Column("confidence", sa.String(length=40), nullable=False),
        sa.Column("route", postgresql.JSONB(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_index("ix_route_snapshots_journey_id", "route_snapshots", ["journey_id"])
    op.create_index("ix_route_snapshots_route_hash", "route_snapshots", ["route_hash"])

    op.create_table(
        "audit_events",
        sa.Column("seq", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("prev_hash", sa.String(length=80), nullable=False),
        sa.Column("entry_hash", sa.String(length=80), nullable=False, unique=True),
        sa.Column("actor", sa.String(length=200), nullable=False),
        sa.Column("action", sa.String(length=120), nullable=False),
        sa.Column("payload", postgresql.JSONB(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_index("ix_audit_events_action", "audit_events", ["action"])

    # Defence in depth: the audit log is append-only at the database level.
    op.execute(
        """
        CREATE OR REPLACE FUNCTION wb_audit_block_mutations()
        RETURNS trigger AS $$
        BEGIN
            RAISE EXCEPTION 'audit_events is append-only; % is not permitted', TG_OP;
        END;
        $$ LANGUAGE plpgsql;
        """
    )
    op.execute(
        """
        CREATE TRIGGER audit_events_no_mutation
        BEFORE UPDATE OR DELETE ON audit_events
        FOR EACH ROW EXECUTE FUNCTION wb_audit_block_mutations();
        """
    )

    op.create_table(
        "idempotency_keys",
        sa.Column("key", sa.String(length=200), primary_key=True),
        sa.Column("request_hash", sa.String(length=80), nullable=False),
        sa.Column("status", sa.String(length=20), nullable=False),
        sa.Column("response", postgresql.JSONB(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )


def downgrade() -> None:
    op.drop_table("idempotency_keys")
    op.execute("DROP TRIGGER IF EXISTS audit_events_no_mutation ON audit_events;")
    op.execute("DROP FUNCTION IF EXISTS wb_audit_block_mutations();")
    op.drop_table("audit_events")
    op.drop_table("route_snapshots")
    op.drop_table("journeys")
