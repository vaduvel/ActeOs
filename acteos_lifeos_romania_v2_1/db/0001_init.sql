-- ActeOS baseline schema. PostgreSQL 18.x.
-- Supabase deployments use auth.users as identity source; local deployments may substitute.

create extension if not exists pgcrypto;
create extension if not exists citext;

create schema if not exists app;
create schema if not exists content;
create schema if not exists audit;

create type app.case_status as enum ('draft','needs_facts','resolved','needs_confirmation','conflicting','blocked','completed','cancelled');
create type app.journey_status as enum ('active','needs_review','completed','cancelled','archived','blocked');
create type app.step_status as enum ('locked','available','in_progress','ready_to_submit','submitted','completed','blocked','needs_confirmation','failed','skipped_not_applicable');
create type app.requirement_status as enum ('missing','provided','needs_review','ready','expired','rejected','not_applicable');
create type app.storage_mode as enum ('local_only','encrypted_backup','cloud_processing_consented','human_review_consented');
create type content.review_status as enum ('draft','in_review','approved','active','stale','hard_expired','withdrawn','superseded','conflicting');
create type content.ruleset_status as enum ('draft','validating','approved','active','superseded','withdrawn');
create type content.freshness_class as enum ('critical','operational','explanatory');
create type content.channel_status as enum ('active','stale','unavailable','withdrawn');
create type content.integration_status as enum ('SOURCE_ONLY','DEEP_LINK','ENROLMENT_REQUIRED','NOT_CONFIGURED','SANDBOX','ACTIVE','SUSPENDED');
create type app.job_status as enum ('queued','running','retry_wait','succeeded','dead_letter','cancelled');

create table app.profiles (
    user_id uuid primary key,
    locale text not null default 'ro-RO',
    timezone text not null default 'Europe/Bucharest',
    display_name text,
    created_at timestamptz not null default now(),
    updated_at timestamptz not null default now(),
    deleted_at timestamptz,
    constraint profile_locale_ck check (locale = 'ro-RO'),
    constraint profile_timezone_ck check (timezone = 'Europe/Bucharest')
);

create table app.installations (
    id uuid primary key default gen_random_uuid(),
    user_id uuid,
    anonymous_subject_hash text,
    platform text not null check (platform in ('android','ios','web')),
    app_version text,
    push_token_ciphertext bytea,
    created_at timestamptz not null default now(),
    last_seen_at timestamptz not null default now(),
    revoked_at timestamptz,
    constraint installation_identity_ck check (user_id is not null or anonymous_subject_hash is not null)
);

create table app.households (
    id uuid primary key default gen_random_uuid(),
    owner_user_id uuid not null,
    name text not null,
    created_at timestamptz not null default now(),
    updated_at timestamptz not null default now(),
    deleted_at timestamptz
);

create table app.household_members (
    id uuid primary key default gen_random_uuid(),
    household_id uuid not null references app.households(id) on delete cascade,
    linked_user_id uuid,
    display_name_ciphertext bytea,
    relationship text not null,
    birth_date_ciphertext bytea,
    created_at timestamptz not null default now(),
    deleted_at timestamptz
);

create table app.assets (
    id uuid primary key default gen_random_uuid(),
    household_id uuid references app.households(id) on delete cascade,
    owner_user_id uuid not null,
    asset_type text not null check (asset_type in ('vehicle','property','company')),
    label_ciphertext bytea,
    attributes_ciphertext bytea,
    created_at timestamptz not null default now(),
    updated_at timestamptz not null default now(),
    deleted_at timestamptz
);

create table content.jurisdictions (
    id text primary key,
    parent_id text references content.jurisdictions(id),
    type text not null,
    name_ro text not null,
    siruta bigint,
    iso_code text,
    nuts text,
    valid_from date,
    valid_to date,
    source_claim_id uuid,
    metadata jsonb not null default '{}'::jsonb,
    unique(type, siruta)
);

create table content.life_event_types (
    id text primary key,
    category_id text not null,
    title_ro text not null,
    description_ro text,
    trigger_phrases_ro jsonb not null default '[]'::jsonb,
    parent_event_id text references content.life_event_types(id),
    release_wave text not null,
    research_status text not null,
    production_status text not null,
    schema_version text not null,
    created_at timestamptz not null default now(),
    updated_at timestamptz not null default now()
);

create table content.fact_definitions (
    id text primary key,
    event_type_id text not null references content.life_event_types(id),
    type text not null,
    label_ro text not null,
    reason_ro text not null,
    sensitive boolean not null default false,
    required_for_resolution boolean not null default false,
    options jsonb,
    validation_schema jsonb not null default '{}'::jsonb,
    version integer not null default 1,
    status text not null default 'draft'
);

create table content.sources (
    id uuid primary key default gen_random_uuid(),
    canonical_url text not null unique,
    publisher text not null,
    authority_level text not null,
    legal_rank text,
    territory_ids text[] not null default '{}',
    competence_scope text[] not null default '{}',
    fetch_mode text not null check (fetch_mode in ('manual','scheduled','api')),
    allowed_to_fetch boolean not null default false,
    status text not null default 'active',
    last_checked_at timestamptz,
    next_check_at timestamptz,
    created_by uuid,
    created_at timestamptz not null default now(),
    updated_at timestamptz not null default now()
);

create table content.source_snapshots (
    id uuid primary key default gen_random_uuid(),
    source_id uuid not null references content.sources(id),
    captured_at timestamptz not null default now(),
    http_status integer,
    content_type text,
    storage_object_key text,
    normalized_text_object_key text,
    sha256 char(64) not null,
    etag text,
    last_modified text,
    previous_snapshot_id uuid references content.source_snapshots(id),
    change_detected boolean not null default false,
    change_summary jsonb,
    status text not null default 'captured',
    unique(source_id, sha256)
);

create table content.source_claims (
    id uuid primary key default gen_random_uuid(),
    stable_key text not null,
    source_id uuid not null references content.sources(id),
    snapshot_id uuid not null references content.source_snapshots(id),
    statement text not null,
    evidence_excerpt text not null,
    locator text not null,
    authority_level text not null,
    legal_rank text,
    territory_ids text[] not null default '{}',
    competence_scope text[] not null default '{}',
    published_at date,
    accessed_at date not null,
    effective_from date,
    effective_to date,
    confidence text not null,
    freshness_class content.freshness_class not null,
    review_due_at date,
    hard_expiry_at date,
    status content.review_status not null default 'draft',
    created_by uuid,
    reviewed_by uuid,
    approved_at timestamptz,
    supersedes_claim_id uuid references content.source_claims(id),
    created_at timestamptz not null default now(),
    updated_at timestamptz not null default now(),
    unique(stable_key, snapshot_id)
);

create table content.claim_conflicts (
    id uuid primary key default gen_random_uuid(),
    claim_a_id uuid not null references content.source_claims(id),
    claim_b_id uuid not null references content.source_claims(id),
    field_or_effect text not null,
    impact text not null check (impact in ('informational','operational','critical')),
    status text not null default 'open',
    resolution_note text,
    resolved_by uuid,
    resolved_at timestamptz,
    created_at timestamptz not null default now(),
    constraint conflict_order_ck check (claim_a_id <> claim_b_id)
);

create table content.step_templates (
    id text primary key,
    semantic_key text not null,
    title_ro text not null,
    instruction_ro text not null,
    sequence_hint integer not null default 100,
    completion_evidence_ro jsonb not null default '[]'::jsonb,
    recovery_actions_ro jsonb not null default '[]'::jsonb,
    status text not null default 'draft'
);

create table content.requirement_templates (
    id text primary key,
    title_ro text not null,
    description_ro text,
    obligation text not null check (obligation in ('mandatory','conditional','optional')),
    timing text not null check (timing in ('now','later')),
    accepted_forms text[] not null default '{}',
    validity jsonb not null default '{}'::jsonb,
    readiness_checks text[] not null default '{}',
    status text not null default 'draft'
);

create table content.official_channels (
    id text primary key,
    type text not null check (type in ('web','physical','phone','email','deep_link')),
    label_ro text not null,
    url text,
    address jsonb,
    phone text,
    email citext,
    integration_status content.integration_status not null,
    official_domain citext,
    jurisdiction_ids text[] not null default '{}',
    source_claim_ids uuid[] not null default '{}',
    valid_from date,
    valid_to date,
    status content.channel_status not null default 'active',
    last_verified_at date
);

create table content.rule_revisions (
    id uuid primary key default gen_random_uuid(),
    canonical_rule_id text not null,
    revision integer not null,
    event_type_id text not null references content.life_event_types(id),
    jurisdiction_ids text[] not null,
    authority_level text not null,
    competence_scope text[] not null default '{}',
    legal_rank text,
    severity content.freshness_class not null,
    effective_from date not null,
    effective_to date,
    predicate jsonb not null,
    effects jsonb not null,
    source_claim_ids uuid[] not null,
    override_rule_ids uuid[] not null default '{}',
    status content.review_status not null default 'draft',
    created_by uuid,
    reviewed_by uuid,
    approved_at timestamptz,
    created_at timestamptz not null default now(),
    unique(canonical_rule_id, revision),
    constraint rule_effective_ck check (effective_to is null or effective_to > effective_from),
    constraint critical_claim_ck check (severity <> 'critical' or cardinality(source_claim_ids) > 0)
);

create table content.rule_sets (
    id uuid primary key default gen_random_uuid(),
    version text not null unique,
    scope text[] not null,
    schema_version text not null,
    engine_compatibility text not null,
    manifest_sha256 char(64) not null unique,
    status content.ruleset_status not null default 'draft',
    approved_by uuid[] not null default '{}',
    published_by uuid,
    published_at timestamptz,
    supersedes_ruleset_id uuid references content.rule_sets(id),
    created_at timestamptz not null default now()
);

create table content.rule_set_members (
    rule_set_id uuid not null references content.rule_sets(id) on delete cascade,
    rule_revision_id uuid not null references content.rule_revisions(id),
    primary key(rule_set_id, rule_revision_id)
);

create table content.research_gaps (
    id uuid primary key default gen_random_uuid(),
    event_type_id text references content.life_event_types(id),
    jurisdiction_id text references content.jurisdictions(id),
    question text not null,
    impact text not null,
    expected_publisher text,
    expected_location text,
    status text not null default 'open',
    fallback_user_message_ro text not null,
    owner_id uuid,
    next_review_at date,
    created_at timestamptz not null default now(),
    resolved_at timestamptz
);

create table app.cases (
    id uuid primary key default gen_random_uuid(),
    user_id uuid,
    installation_id uuid references app.installations(id),
    event_type_id text not null references content.life_event_types(id),
    subject_ref text,
    reference_date date not null,
    timezone text not null default 'Europe/Bucharest',
    jurisdiction_path text[] not null,
    status app.case_status not null default 'draft',
    version integer not null default 1,
    source_text_ciphertext bytea,
    created_at timestamptz not null default now(),
    updated_at timestamptz not null default now(),
    deleted_at timestamptz,
    constraint case_identity_ck check (user_id is not null or installation_id is not null)
);

create table app.fact_values (
    case_id uuid not null references app.cases(id) on delete cascade,
    fact_definition_id text not null references content.fact_definitions(id),
    value_json jsonb not null,
    provenance text not null check (provenance in ('user_entered','derived','document_extracted','registry_verified')),
    sensitive boolean not null default false,
    version integer not null default 1,
    updated_at timestamptz not null default now(),
    primary key(case_id, fact_definition_id)
);

create table app.journeys (
    id uuid primary key default gen_random_uuid(),
    case_id uuid not null references app.cases(id),
    revision integer not null,
    previous_journey_id uuid references app.journeys(id),
    rule_set_id uuid not null references content.rule_sets(id),
    ruleset_version text not null,
    reference_date date not null,
    facts_hash char(64) not null,
    engine_version text not null,
    status app.journey_status not null default 'active',
    trust_state text not null,
    resolution_trace jsonb not null,
    created_at timestamptz not null default now(),
    archived_at timestamptz,
    unique(case_id, revision)
);

create table app.journey_steps (
    id uuid primary key default gen_random_uuid(),
    journey_id uuid not null references app.journeys(id) on delete cascade,
    template_id text,
    semantic_key text not null,
    title_ro text not null,
    instruction_ro text not null,
    sequence integer not null,
    status app.step_status not null,
    deadline jsonb,
    completion_evidence_ro jsonb not null default '[]'::jsonb,
    recovery_actions_ro jsonb not null default '[]'::jsonb,
    source_claim_ids uuid[] not null default '{}',
    user_note_ciphertext bytea,
    version integer not null default 1,
    created_at timestamptz not null default now(),
    updated_at timestamptz not null default now(),
    unique(journey_id, semantic_key)
);

create table app.journey_step_dependencies (
    journey_id uuid not null references app.journeys(id) on delete cascade,
    step_id uuid not null references app.journey_steps(id) on delete cascade,
    depends_on_step_id uuid not null references app.journey_steps(id) on delete cascade,
    primary key(step_id, depends_on_step_id),
    constraint dependency_self_ck check (step_id <> depends_on_step_id)
);

create table app.journey_requirements (
    id uuid primary key default gen_random_uuid(),
    journey_step_id uuid not null references app.journey_steps(id) on delete cascade,
    template_id text,
    semantic_key text not null,
    title_ro text not null,
    description_ro text,
    obligation text not null,
    timing text not null,
    accepted_forms text[] not null default '{}',
    validity jsonb not null default '{}'::jsonb,
    readiness_checks text[] not null default '{}',
    source_claim_ids uuid[] not null default '{}',
    status app.requirement_status not null default 'missing',
    version integer not null default 1,
    created_at timestamptz not null default now(),
    updated_at timestamptz not null default now(),
    unique(journey_step_id, semantic_key)
);

create table app.documents (
    id uuid primary key default gen_random_uuid(),
    user_id uuid,
    installation_id uuid references app.installations(id),
    owner_subject_ref text not null,
    document_type_id text not null,
    storage_mode app.storage_mode not null default 'local_only',
    local_ref_hash text,
    storage_object_key text,
    encryption_key_ref text,
    expires_on date,
    status text not null default 'active',
    retention_delete_at timestamptz,
    created_at timestamptz not null default now(),
    deleted_at timestamptz,
    constraint document_identity_ck check (user_id is not null or installation_id is not null),
    constraint cloud_object_ck check (storage_mode = 'local_only' or storage_object_key is not null)
);

create table app.document_readiness_runs (
    id uuid primary key default gen_random_uuid(),
    document_id uuid not null references app.documents(id) on delete cascade,
    requirement_id uuid references app.journey_requirements(id) on delete set null,
    processing_mode text not null,
    engine_version text not null,
    status text not null,
    checks jsonb not null,
    limitations jsonb not null default '[]'::jsonb,
    extracted_fields_ciphertext bytea,
    authenticity_verified boolean not null default false check (authenticity_verified = false),
    created_at timestamptz not null default now()
);

create table app.notification_preferences (
    user_id uuid primary key,
    deadline_reminders boolean not null default true,
    document_expiry boolean not null default true,
    rule_changes boolean not null default true,
    push_enabled boolean not null default false,
    email_enabled boolean not null default false,
    updated_at timestamptz not null default now()
);

create table app.notifications (
    id uuid primary key default gen_random_uuid(),
    user_id uuid,
    installation_id uuid references app.installations(id),
    type text not null,
    due_at timestamptz not null,
    payload jsonb not null,
    status text not null default 'scheduled',
    attempts integer not null default 0,
    provider_message_id text,
    sent_at timestamptz,
    created_at timestamptz not null default now()
);

create table app.feedback_reports (
    id uuid primary key default gen_random_uuid(),
    user_id uuid,
    installation_id uuid references app.installations(id),
    journey_id uuid references app.journeys(id),
    step_id uuid references app.journey_steps(id),
    occurred_on date not null,
    institution_label_ciphertext bytea,
    category text not null,
    description_ciphertext bytea,
    evidence_document_id uuid references app.documents(id),
    status text not null default 'open',
    severity text,
    assigned_to uuid,
    created_at timestamptz not null default now(),
    resolved_at timestamptz
);

create table app.jobs (
    id uuid primary key default gen_random_uuid(),
    type text not null,
    payload jsonb not null,
    status app.job_status not null default 'queued',
    priority integer not null default 100,
    run_at timestamptz not null default now(),
    attempts integer not null default 0,
    max_attempts integer not null default 5,
    locked_by text,
    locked_at timestamptz,
    last_error_code text,
    last_error_redacted text,
    created_at timestamptz not null default now(),
    updated_at timestamptz not null default now()
);

create table audit.events (
    id bigint generated always as identity primary key,
    occurred_at timestamptz not null default now(),
    actor_type text not null,
    actor_id text,
    action text not null,
    entity_type text not null,
    entity_id text,
    request_id text,
    ip_hash text,
    user_agent_hash text,
    metadata jsonb not null default '{}'::jsonb
);

comment on table audit.events is 'Append-only security and administrative audit; must not contain raw PII or document content.';
