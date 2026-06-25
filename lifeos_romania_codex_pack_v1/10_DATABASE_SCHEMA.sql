-- LifeOS Romania schema v1
CREATE TABLE IF NOT EXISTS users (
  id UUID PRIMARY KEY,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  locale TEXT NOT NULL DEFAULT 'ro-RO'
);

CREATE TABLE IF NOT EXISTS life_event_types (
  id TEXT PRIMARY KEY,
  category_id TEXT NOT NULL,
  label TEXT NOT NULL,
  frequency_tier TEXT NOT NULL CHECK (frequency_tier IN ('A','B','C')),
  r1_scope BOOLEAN NOT NULL DEFAULT false,
  definition JSONB NOT NULL,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS event_sessions (
  id UUID PRIMARY KEY,
  user_id UUID REFERENCES users(id),
  event_type_id TEXT REFERENCES life_event_types(id),
  status TEXT NOT NULL,
  jurisdiction JSONB NOT NULL DEFAULT '{}'::jsonb,
  reference_date DATE NOT NULL DEFAULT CURRENT_DATE,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS session_facts (
  session_id UUID REFERENCES event_sessions(id) ON DELETE CASCADE,
  fact_id TEXT NOT NULL,
  fact_value JSONB NOT NULL,
  sensitive BOOLEAN NOT NULL DEFAULT false,
  source TEXT NOT NULL DEFAULT 'user',
  updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  PRIMARY KEY (session_id, fact_id)
);

CREATE TABLE IF NOT EXISTS sources (
  id TEXT PRIMARY KEY,
  title TEXT NOT NULL,
  publisher TEXT NOT NULL,
  authority_level TEXT NOT NULL,
  canonical_url TEXT NOT NULL,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS source_snapshots (
  id UUID PRIMARY KEY,
  source_id TEXT REFERENCES sources(id),
  fetched_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  sha256 TEXT NOT NULL,
  storage_uri TEXT NOT NULL,
  status TEXT NOT NULL DEFAULT 'fetched'
);

CREATE TABLE IF NOT EXISTS source_claims (
  id TEXT PRIMARY KEY,
  source_id TEXT REFERENCES sources(id),
  snapshot_id UUID REFERENCES source_snapshots(id),
  claim_type TEXT NOT NULL,
  evidence_summary TEXT NOT NULL,
  quote TEXT NOT NULL,
  locator TEXT NOT NULL,
  effective_from DATE,
  effective_to DATE,
  confidence TEXT NOT NULL CHECK (confidence IN ('verified','verified_with_local_gap','needs_confirmation','conflicting','expired')),
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS rule_bundles (
  id TEXT PRIMARY KEY,
  version TEXT NOT NULL,
  jurisdiction JSONB NOT NULL,
  reference_year TEXT,
  status TEXT NOT NULL CHECK (status IN ('draft','review','published','retracted')),
  demo_mode BOOLEAN NOT NULL DEFAULT true,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  published_at TIMESTAMPTZ
);

CREATE TABLE IF NOT EXISTS rules (
  id TEXT PRIMARY KEY,
  bundle_id TEXT REFERENCES rule_bundles(id) ON DELETE CASCADE,
  rule_type TEXT NOT NULL,
  payload JSONB NOT NULL,
  source_claim_ids TEXT[] NOT NULL DEFAULT '{}',
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS route_runs (
  id UUID PRIMARY KEY,
  session_id UUID REFERENCES event_sessions(id) ON DELETE CASCADE,
  bundle_id TEXT REFERENCES rule_bundles(id),
  facts_hash TEXT NOT NULL,
  route_hash TEXT NOT NULL,
  status TEXT NOT NULL,
  output JSONB NOT NULL,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS document_assets (
  id UUID PRIMARY KEY,
  user_id UUID REFERENCES users(id),
  session_id UUID REFERENCES event_sessions(id),
  document_type TEXT,
  storage_uri TEXT,
  local_only BOOLEAN NOT NULL DEFAULT false,
  retention_policy TEXT NOT NULL DEFAULT 'delete_after_30_days',
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS document_checks (
  id UUID PRIMARY KEY,
  document_asset_id UUID REFERENCES document_assets(id) ON DELETE CASCADE,
  requirement_id TEXT NOT NULL,
  status TEXT NOT NULL,
  checks JSONB NOT NULL,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS freshness_incidents (
  id UUID PRIMARY KEY,
  source_id TEXT REFERENCES sources(id),
  severity TEXT NOT NULL,
  description TEXT NOT NULL,
  status TEXT NOT NULL DEFAULT 'open',
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS partner_offers (
  id UUID PRIMARY KEY,
  partner_type TEXT NOT NULL,
  label TEXT NOT NULL,
  disclosure TEXT NOT NULL,
  active BOOLEAN NOT NULL DEFAULT false,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
