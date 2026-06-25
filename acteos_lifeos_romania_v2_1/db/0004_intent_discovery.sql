-- ActeOS v2.1 — Intent-first discovery additive migration

create table content.intent_categories (
    id text primary key,
    title_ro text not null,
    description_ro text,
    icon_key text,
    display_order integer not null default 100,
    status text not null default 'active',
    catalog_version text not null,
    created_at timestamptz not null default now(),
    updated_at timestamptz not null default now()
);

create table content.intent_types (
    id text primary key,
    category_id text not null references content.intent_categories(id),
    kind text not null check (kind in ('direct_goal','bundle_goal')),
    title_ro text not null,
    outcome_ro text not null,
    journey_template_id text,
    jurisdiction_scope text not null,
    release_wave text not null,
    research_status text not null,
    production_status text not null,
    availability_policy text not null,
    search_boost numeric(5,3) not null default 1.000 check (search_boost >= 0 and search_boost <= 3),
    catalog_version text not null,
    created_at timestamptz not null default now(),
    updated_at timestamptz not null default now()
);

create table content.intent_aliases (
    id uuid primary key default gen_random_uuid(),
    intent_type_id text not null references content.intent_types(id) on delete cascade,
    locale text not null default 'ro-RO',
    alias_text text not null,
    normalized_alias text not null,
    alias_kind text not null check (alias_kind in ('positive','negative','abbreviation','common_misspelling')),
    weight numeric(5,3) not null default 1.000,
    status text not null default 'active',
    created_at timestamptz not null default now(),
    unique(locale, normalized_alias, intent_type_id, alias_kind)
);

create table content.intent_event_links (
    intent_type_id text not null references content.intent_types(id) on delete cascade,
    event_type_id text not null references content.life_event_types(id) on delete cascade,
    relation text not null check (relation in ('may_be_triggered_by','bundle_contains','related_context')),
    created_at timestamptz not null default now(),
    primary key(intent_type_id, event_type_id, relation)
);

alter table app.cases add column intent_type_id text references content.intent_types(id);
alter table app.cases add column event_context_ids text[] not null default '{}';
alter table app.cases add column discovery_source text;
alter table app.cases alter column event_type_id drop not null;
alter table app.cases add constraint case_intent_or_legacy_event_ck
    check (intent_type_id is not null or event_type_id is not null);

create table app.intent_query_feedback (
    id uuid primary key default gen_random_uuid(),
    user_id uuid,
    installation_id uuid references app.installations(id),
    query_fingerprint text,
    result_bucket text not null check (result_bucket in ('high','ambiguous','low','no_result')),
    selected_intent_id text references content.intent_types(id),
    category_hint text,
    resolver_version text not null,
    catalog_version text not null,
    feedback_kind text check (feedback_kind in ('selected','none_match','missing_intent','abandoned')),
    created_at timestamptz not null default now(),
    constraint intent_feedback_identity_ck check (user_id is not null or installation_id is not null)
);

create index intent_alias_normalized_idx on content.intent_aliases(locale, normalized_alias) where status = 'active';
create index intent_types_category_idx on content.intent_types(category_id, production_status, release_wave);
create index intent_event_event_idx on content.intent_event_links(event_type_id);
create index cases_intent_idx on app.cases(intent_type_id, created_at desc);
create index intent_feedback_created_idx on app.intent_query_feedback(created_at desc);

alter table app.intent_query_feedback enable row level security;

create policy intent_query_feedback_owner_select on app.intent_query_feedback
    for select using (
        user_id = nullif(current_setting('app.current_user_id', true), '')::uuid
        or installation_id = nullif(current_setting('app.current_installation_id', true), '')::uuid
    );

create policy intent_query_feedback_owner_insert on app.intent_query_feedback
    for insert with check (
        user_id = nullif(current_setting('app.current_user_id', true), '')::uuid
        or installation_id = nullif(current_setting('app.current_installation_id', true), '')::uuid
    );
