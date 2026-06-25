-- Waze pentru birocrație — PostgreSQL 16+ canonical schema
-- Apply with a migration tool (Alembic). This file defines the target model, not a one-shot production migration.
BEGIN;

CREATE EXTENSION IF NOT EXISTS pgcrypto;
CREATE EXTENSION IF NOT EXISTS citext;

CREATE SCHEMA IF NOT EXISTS content;
CREATE SCHEMA IF NOT EXISTS app;
CREATE SCHEMA IF NOT EXISTS ops;
CREATE SCHEMA IF NOT EXISTS audit;

CREATE TYPE content.source_status AS ENUM ('active','paused','retired');
CREATE TYPE content.authority_level AS ENUM ('eu','national_normative','national_operational','county','uat','institution','signal_only');
CREATE TYPE content.freshness_class AS ENUM ('critical','operational','explanatory');
CREATE TYPE content.snapshot_status AS ENUM ('fetched','unchanged','changed','failed','blocked');
CREATE TYPE content.rule_status AS ENUM ('draft','in_review','changes_requested','approved','rejected','published','retired');
CREATE TYPE content.confidence_state AS ENUM ('verified','verified_with_local_gap','needs_confirmation','conflicting','expired');
CREATE TYPE content.release_status AS ENUM ('preview','production','retired');
CREATE TYPE app.journey_status AS ENUM ('active','completed','archived');
CREATE TYPE app.requirement_status AS ENUM ('not_started','ready','blocked','in_progress','submitted','completed','not_applicable');
CREATE TYPE app.finding_severity AS ENUM ('blocking','warning','info','unknown');
CREATE TYPE app.finding_status AS ENUM ('detected','not_detected','unable_to_check');
CREATE TYPE ops.job_status AS ENUM ('queued','running','succeeded','failed','cancelled');
CREATE TYPE ops.incident_status AS ENUM ('new','triaged','investigating','resolved','dismissed');

CREATE OR REPLACE FUNCTION app.set_updated_at() RETURNS trigger LANGUAGE plpgsql AS $$
BEGIN
  NEW.updated_at = timezone('utc', now());
  RETURN NEW;
END $$;

CREATE TABLE content.jurisdiction (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  parent_id uuid REFERENCES content.jurisdiction(id),
  code text NOT NULL UNIQUE CHECK (code ~ '^[a-z0-9][a-z0-9_.-]{2,127}$'),
  name text NOT NULL,
  kind text NOT NULL CHECK (kind IN ('country','county','uat','institution')),
  timezone text NOT NULL DEFAULT 'Europe/Bucharest' CHECK (timezone = 'Europe/Bucharest'),
  metadata jsonb NOT NULL DEFAULT '{}'::jsonb,
  is_active boolean NOT NULL DEFAULT true,
  created_at timestamptz NOT NULL DEFAULT timezone('utc', now()),
  updated_at timestamptz NOT NULL DEFAULT timezone('utc', now())
);
CREATE INDEX jurisdiction_parent_idx ON content.jurisdiction(parent_id);

CREATE TABLE content.authority (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  jurisdiction_id uuid REFERENCES content.jurisdiction(id),
  code text NOT NULL UNIQUE,
  official_name text NOT NULL,
  authority_level content.authority_level NOT NULL,
  official_domains text[] NOT NULL DEFAULT '{}',
  metadata jsonb NOT NULL DEFAULT '{}'::jsonb,
  created_at timestamptz NOT NULL DEFAULT timezone('utc', now()),
  updated_at timestamptz NOT NULL DEFAULT timezone('utc', now())
);

CREATE TABLE content.intent (
  id text PRIMARY KEY CHECK (id ~ '^[a-z0-9][a-z0-9_.-]{2,127}$'),
  category text NOT NULL,
  title_ro text NOT NULL,
  description_ro text NOT NULL,
  keywords_ro text[] NOT NULL DEFAULT '{}',
  release_status content.release_status NOT NULL DEFAULT 'preview',
  owner_team text NOT NULL,
  created_at timestamptz NOT NULL DEFAULT timezone('utc', now()),
  updated_at timestamptz NOT NULL DEFAULT timezone('utc', now())
);
CREATE INDEX intent_keywords_gin ON content.intent USING gin(keywords_ro);

CREATE TABLE content.source (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  authority_id uuid REFERENCES content.authority(id),
  jurisdiction_id uuid REFERENCES content.jurisdiction(id),
  canonical_url text NOT NULL UNIQUE CHECK (canonical_url ~ '^https://'),
  title text NOT NULL,
  publisher text NOT NULL,
  authority_level content.authority_level NOT NULL,
  status content.source_status NOT NULL DEFAULT 'active',
  freshness_class content.freshness_class NOT NULL,
  review_interval_days integer NOT NULL CHECK (review_interval_days BETWEEN 1 AND 730),
  robots_policy jsonb NOT NULL DEFAULT '{}'::jsonb,
  fetch_policy jsonb NOT NULL DEFAULT '{}'::jsonb,
  last_fetched_at timestamptz,
  last_verified_at timestamptz,
  next_review_at timestamptz,
  consecutive_failures integer NOT NULL DEFAULT 0 CHECK (consecutive_failures >= 0),
  created_by uuid,
  created_at timestamptz NOT NULL DEFAULT timezone('utc', now()),
  updated_at timestamptz NOT NULL DEFAULT timezone('utc', now())
);
CREATE INDEX source_review_idx ON content.source(status, next_review_at);
CREATE INDEX source_jurisdiction_idx ON content.source(jurisdiction_id);

CREATE TABLE content.source_snapshot (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  source_id uuid NOT NULL REFERENCES content.source(id) ON DELETE RESTRICT,
  fetched_at timestamptz NOT NULL,
  status content.snapshot_status NOT NULL,
  http_status integer,
  final_url text,
  content_type text,
  etag text,
  last_modified text,
  content_sha256 text CHECK (content_sha256 IS NULL OR content_sha256 ~ '^[a-f0-9]{64}$'),
  normalized_sha256 text CHECK (normalized_sha256 IS NULL OR normalized_sha256 ~ '^[a-f0-9]{64}$'),
  storage_key text,
  extraction_metadata jsonb NOT NULL DEFAULT '{}'::jsonb,
  error_code text,
  error_detail text,
  created_at timestamptz NOT NULL DEFAULT timezone('utc', now()),
  UNIQUE (source_id, normalized_sha256)
);
CREATE INDEX source_snapshot_source_time_idx ON content.source_snapshot(source_id, fetched_at DESC);

CREATE TABLE content.source_claim (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  source_snapshot_id uuid NOT NULL REFERENCES content.source_snapshot(id) ON DELETE RESTRICT,
  stable_key text NOT NULL CHECK (stable_key ~ '^[a-z0-9][a-z0-9_.-]{2,191}$'),
  claim_text text NOT NULL,
  evidence_excerpt text NOT NULL,
  locator jsonb NOT NULL,
  jurisdiction_id uuid REFERENCES content.jurisdiction(id),
  effective_from timestamptz,
  effective_to timestamptz,
  confidence content.confidence_state NOT NULL,
  extracted_by text NOT NULL CHECK (extracted_by IN ('human','ai_candidate','import')),
  verified_by uuid,
  verified_at timestamptz,
  created_at timestamptz NOT NULL DEFAULT timezone('utc', now()),
  UNIQUE(source_snapshot_id, stable_key),
  CHECK (effective_to IS NULL OR effective_from IS NULL OR effective_to > effective_from),
  CHECK ((confidence IN ('verified','verified_with_local_gap')) = (verified_at IS NOT NULL))
);
CREATE INDEX source_claim_effective_idx ON content.source_claim(jurisdiction_id, effective_from, effective_to);

CREATE TABLE content.rule_family (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  stable_id text NOT NULL UNIQUE CHECK (stable_id ~ '^[a-z0-9][a-z0-9_.-]{2,191}$'),
  intent_id text NOT NULL REFERENCES content.intent(id),
  jurisdiction_id uuid NOT NULL REFERENCES content.jurisdiction(id),
  title text NOT NULL,
  risk_class text NOT NULL CHECK (risk_class IN ('low','medium','high','critical')),
  owner_team text NOT NULL,
  created_at timestamptz NOT NULL DEFAULT timezone('utc', now()),
  updated_at timestamptz NOT NULL DEFAULT timezone('utc', now())
);
CREATE INDEX rule_family_lookup_idx ON content.rule_family(intent_id, jurisdiction_id);

CREATE TABLE content.rule_version (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  rule_family_id uuid NOT NULL REFERENCES content.rule_family(id) ON DELETE RESTRICT,
  revision integer NOT NULL CHECK (revision > 0),
  status content.rule_status NOT NULL DEFAULT 'draft',
  effective_from timestamptz NOT NULL,
  effective_to timestamptz,
  canonical_payload jsonb NOT NULL,
  canonical_sha256 text NOT NULL CHECK (canonical_sha256 ~ '^[a-f0-9]{64}$'),
  schema_version text NOT NULL,
  engine_min_version text NOT NULL,
  confidence content.confidence_state NOT NULL,
  supersedes_id uuid REFERENCES content.rule_version(id),
  change_summary text NOT NULL,
  created_by uuid NOT NULL,
  created_at timestamptz NOT NULL DEFAULT timezone('utc', now()),
  approved_at timestamptz,
  published_at timestamptz,
  UNIQUE(rule_family_id, revision),
  UNIQUE(canonical_sha256),
  CHECK (effective_to IS NULL OR effective_to > effective_from),
  CHECK (status <> 'published' OR (approved_at IS NOT NULL AND published_at IS NOT NULL))
);
CREATE INDEX rule_version_effective_idx ON content.rule_version(rule_family_id, status, effective_from, effective_to);
CREATE INDEX rule_payload_gin ON content.rule_version USING gin(canonical_payload jsonb_path_ops);

CREATE TABLE content.rule_claim_link (
  rule_version_id uuid NOT NULL REFERENCES content.rule_version(id) ON DELETE CASCADE,
  source_claim_id uuid NOT NULL REFERENCES content.source_claim(id) ON DELETE RESTRICT,
  rule_path text NOT NULL,
  is_critical boolean NOT NULL DEFAULT false,
  PRIMARY KEY(rule_version_id, source_claim_id, rule_path)
);

CREATE TABLE content.rule_review (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  rule_version_id uuid NOT NULL REFERENCES content.rule_version(id) ON DELETE CASCADE,
  reviewer_id uuid NOT NULL,
  reviewer_role text NOT NULL CHECK (reviewer_role IN ('content','legal','publisher','security')),
  decision text NOT NULL CHECK (decision IN ('approve','request_changes','reject')),
  rationale text NOT NULL CHECK (length(rationale) >= 10),
  checklist jsonb NOT NULL DEFAULT '{}'::jsonb,
  created_at timestamptz NOT NULL DEFAULT timezone('utc', now()),
  UNIQUE(rule_version_id, reviewer_id, reviewer_role)
);

CREATE TABLE content.rule_bundle (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  intent_id text NOT NULL REFERENCES content.intent(id),
  jurisdiction_id uuid NOT NULL REFERENCES content.jurisdiction(id),
  channel text NOT NULL CHECK (channel IN ('draft','canary','production','retired')),
  valid_from timestamptz NOT NULL,
  valid_to timestamptz,
  engine_version text NOT NULL,
  manifest jsonb NOT NULL,
  bundle_sha256 text NOT NULL UNIQUE CHECK (bundle_sha256 ~ '^[a-f0-9]{64}$'),
  created_by uuid NOT NULL,
  created_at timestamptz NOT NULL DEFAULT timezone('utc', now()),
  CHECK (valid_to IS NULL OR valid_to > valid_from)
);
CREATE INDEX bundle_lookup_idx ON content.rule_bundle(intent_id, jurisdiction_id, channel, valid_from, valid_to);

CREATE TABLE content.rule_bundle_member (
  bundle_id uuid NOT NULL REFERENCES content.rule_bundle(id) ON DELETE CASCADE,
  rule_version_id uuid NOT NULL REFERENCES content.rule_version(id) ON DELETE RESTRICT,
  priority integer NOT NULL DEFAULT 0,
  PRIMARY KEY(bundle_id, rule_version_id)
);

CREATE TABLE content.bundle_publication (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  bundle_id uuid NOT NULL REFERENCES content.rule_bundle(id) ON DELETE RESTRICT,
  channel text NOT NULL CHECK (channel IN ('canary','production')),
  jurisdiction_id uuid NOT NULL REFERENCES content.jurisdiction(id),
  intent_id text NOT NULL REFERENCES content.intent(id),
  previous_publication_id uuid REFERENCES content.bundle_publication(id),
  action text NOT NULL CHECK (action IN ('publish','rollback','retire')),
  reason text NOT NULL,
  published_by uuid NOT NULL,
  published_at timestamptz NOT NULL DEFAULT timezone('utc', now()),
  is_current boolean NOT NULL DEFAULT true
);
CREATE UNIQUE INDEX one_current_publication_idx
  ON content.bundle_publication(intent_id, jurisdiction_id, channel)
  WHERE is_current;

CREATE TABLE app.device_identity (
  id uuid PRIMARY KEY,
  pseudonymous_token_hash text NOT NULL UNIQUE,
  created_at timestamptz NOT NULL DEFAULT timezone('utc', now()),
  last_seen_at timestamptz NOT NULL DEFAULT timezone('utc', now()),
  deleted_at timestamptz
);

CREATE TABLE app.journey (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  device_id uuid NOT NULL REFERENCES app.device_identity(id) ON DELETE CASCADE,
  account_subject text,
  intent_id text NOT NULL REFERENCES content.intent(id),
  jurisdiction_id uuid NOT NULL REFERENCES content.jurisdiction(id),
  title text NOT NULL,
  status app.journey_status NOT NULL DEFAULT 'active',
  evaluated_at timestamptz NOT NULL,
  active_bundle_hash text CHECK (active_bundle_hash IS NULL OR active_bundle_hash ~ '^[a-f0-9]{64}$'),
  current_route_hash text CHECK (current_route_hash IS NULL OR current_route_hash ~ '^[a-f0-9]{64}$'),
  created_at timestamptz NOT NULL DEFAULT timezone('utc', now()),
  updated_at timestamptz NOT NULL DEFAULT timezone('utc', now()),
  deleted_at timestamptz
);
CREATE INDEX journey_device_idx ON app.journey(device_id, status, updated_at DESC) WHERE deleted_at IS NULL;

CREATE TABLE app.journey_fact (
  journey_id uuid NOT NULL REFERENCES app.journey(id) ON DELETE CASCADE,
  fact_id text NOT NULL,
  value_encrypted bytea NOT NULL,
  value_type text NOT NULL,
  source text NOT NULL CHECK (source IN ('user','derived','document_confirmed')),
  updated_at timestamptz NOT NULL DEFAULT timezone('utc', now()),
  PRIMARY KEY(journey_id, fact_id)
);
COMMENT ON COLUMN app.journey_fact.value_encrypted IS 'Envelope-encrypted. Do not log or index raw values.';

CREATE TABLE app.route_resolution (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  journey_id uuid NOT NULL REFERENCES app.journey(id) ON DELETE CASCADE,
  sequence integer NOT NULL,
  status text NOT NULL CHECK (status IN ('resolved','needs_facts','blocked')),
  evaluated_at timestamptz NOT NULL,
  engine_version text NOT NULL,
  bundle_hash text,
  facts_hash text NOT NULL CHECK (facts_hash ~ '^[a-f0-9]{64}$'),
  route_hash text,
  canonical_output jsonb NOT NULL,
  confidence content.confidence_state NOT NULL,
  created_at timestamptz NOT NULL DEFAULT timezone('utc', now()),
  UNIQUE(journey_id, sequence),
  UNIQUE(journey_id, route_hash)
);
CREATE INDEX route_resolution_latest_idx ON app.route_resolution(journey_id, sequence DESC);

CREATE TABLE app.requirement_state (
  journey_id uuid NOT NULL REFERENCES app.journey(id) ON DELETE CASCADE,
  requirement_id text NOT NULL,
  status app.requirement_status NOT NULL DEFAULT 'not_started',
  note_encrypted bytea,
  updated_at timestamptz NOT NULL DEFAULT timezone('utc', now()),
  PRIMARY KEY(journey_id, requirement_id)
);

CREATE TABLE app.document_analysis (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  journey_id uuid NOT NULL REFERENCES app.journey(id) ON DELETE CASCADE,
  local_document_id uuid NOT NULL,
  requirement_id text NOT NULL,
  document_type text NOT NULL,
  analyzer_version text NOT NULL,
  user_confirmed boolean NOT NULL CHECK (user_confirmed),
  minimized_fields_encrypted bytea,
  created_at timestamptz NOT NULL DEFAULT timezone('utc', now()),
  UNIQUE(journey_id, local_document_id, analyzer_version)
);
COMMENT ON TABLE app.document_analysis IS 'No image bytes and no raw OCR. Stores only minimized, user-confirmed metadata.';

CREATE TABLE app.document_finding (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  analysis_id uuid NOT NULL REFERENCES app.document_analysis(id) ON DELETE CASCADE,
  code text NOT NULL,
  severity app.finding_severity NOT NULL,
  status app.finding_status NOT NULL,
  message_code text NOT NULL,
  field_ref text,
  created_at timestamptz NOT NULL DEFAULT timezone('utc', now())
);

CREATE TABLE app.feedback_incident (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  device_id uuid REFERENCES app.device_identity(id) ON DELETE SET NULL,
  journey_id uuid REFERENCES app.journey(id) ON DELETE SET NULL,
  bundle_hash text,
  step_id text,
  requirement_id text,
  incident_type text NOT NULL,
  message_encrypted bytea NOT NULL,
  status ops.incident_status NOT NULL DEFAULT 'new',
  severity text NOT NULL DEFAULT 'untriaged' CHECK (severity IN ('untriaged','low','medium','high','critical')),
  assigned_to uuid,
  created_at timestamptz NOT NULL DEFAULT timezone('utc', now()),
  updated_at timestamptz NOT NULL DEFAULT timezone('utc', now()),
  resolved_at timestamptz
);
CREATE INDEX feedback_queue_idx ON app.feedback_incident(status, severity, created_at);

CREATE TABLE ops.fetch_job (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  source_id uuid NOT NULL REFERENCES content.source(id),
  status ops.job_status NOT NULL DEFAULT 'queued',
  scheduled_for timestamptz NOT NULL,
  started_at timestamptz,
  finished_at timestamptz,
  attempts integer NOT NULL DEFAULT 0,
  idempotency_key text NOT NULL UNIQUE,
  trace_id text,
  error_code text,
  error_detail text,
  created_at timestamptz NOT NULL DEFAULT timezone('utc', now())
);
CREATE INDEX fetch_job_queue_idx ON ops.fetch_job(status, scheduled_for);

CREATE TABLE ops.source_change_alert (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  source_id uuid NOT NULL REFERENCES content.source(id),
  previous_snapshot_id uuid REFERENCES content.source_snapshot(id),
  current_snapshot_id uuid NOT NULL REFERENCES content.source_snapshot(id),
  severity text NOT NULL CHECK (severity IN ('cosmetic','explanatory','operational','critical')),
  diff_summary jsonb NOT NULL,
  impacted_rule_versions uuid[] NOT NULL DEFAULT '{}',
  status ops.incident_status NOT NULL DEFAULT 'new',
  created_at timestamptz NOT NULL DEFAULT timezone('utc', now()),
  resolved_at timestamptz
);

CREATE TABLE ops.idempotency_record (
  scope text NOT NULL,
  idempotency_key text NOT NULL,
  request_hash text NOT NULL CHECK (request_hash ~ '^[a-f0-9]{64}$'),
  response_status integer NOT NULL,
  response_body jsonb,
  expires_at timestamptz NOT NULL,
  created_at timestamptz NOT NULL DEFAULT timezone('utc', now()),
  PRIMARY KEY(scope, idempotency_key)
);

CREATE TABLE audit.event_log (
  id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  occurred_at timestamptz NOT NULL DEFAULT timezone('utc', now()),
  actor_type text NOT NULL CHECK (actor_type IN ('user','curator','service','system')),
  actor_id text,
  action text NOT NULL,
  entity_type text NOT NULL,
  entity_id text NOT NULL,
  correlation_id text,
  ip_hash text,
  user_agent_hash text,
  payload jsonb NOT NULL DEFAULT '{}'::jsonb,
  previous_event_hash text,
  event_hash text NOT NULL UNIQUE
);
COMMENT ON TABLE audit.event_log IS 'Append-only. Payload must not contain raw PII or document content.';

CREATE OR REPLACE FUNCTION audit.reject_mutation() RETURNS trigger LANGUAGE plpgsql AS $$
BEGIN
  RAISE EXCEPTION 'audit.event_log is append-only';
END $$;
CREATE TRIGGER audit_no_update BEFORE UPDATE OR DELETE ON audit.event_log
FOR EACH ROW EXECUTE FUNCTION audit.reject_mutation();

CREATE TRIGGER jurisdiction_updated BEFORE UPDATE ON content.jurisdiction FOR EACH ROW EXECUTE FUNCTION app.set_updated_at();
CREATE TRIGGER authority_updated BEFORE UPDATE ON content.authority FOR EACH ROW EXECUTE FUNCTION app.set_updated_at();
CREATE TRIGGER intent_updated BEFORE UPDATE ON content.intent FOR EACH ROW EXECUTE FUNCTION app.set_updated_at();
CREATE TRIGGER source_updated BEFORE UPDATE ON content.source FOR EACH ROW EXECUTE FUNCTION app.set_updated_at();
CREATE TRIGGER rule_family_updated BEFORE UPDATE ON content.rule_family FOR EACH ROW EXECUTE FUNCTION app.set_updated_at();
CREATE TRIGGER journey_updated BEFORE UPDATE ON app.journey FOR EACH ROW EXECUTE FUNCTION app.set_updated_at();
CREATE TRIGGER feedback_updated BEFORE UPDATE ON app.feedback_incident FOR EACH ROW EXECUTE FUNCTION app.set_updated_at();

-- Row-level security must be enabled in deployment migrations after service roles are created.
-- Public API role: no direct table access. Curator role: views/functions scoped by RBAC.
-- All access occurs through application services and parameterized queries/ORM.

COMMIT;
