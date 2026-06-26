-- 0002: lossless resolution snapshot on app.journeys.
-- The engine resolution aggregate (events + advice/warnings/conflicts/deadlines/
-- blocks/missing_facts) is richer than the normalized journey_steps /
-- journey_requirements projection. Store it losslessly so a resolved case can be
-- served from the database before the normalization slice lands. The
-- resolution_trace column (0001) is kept as the verifiable provenance header
-- (facts_hash + engine_version + included/excluded rule ids).

alter table app.journeys
    add column if not exists resolution_snapshot jsonb not null default '{}'::jsonb;

comment on column app.journeys.resolution_snapshot is
    'Lossless engine resolution aggregate (events + resolution_trace + intent/event ids) exactly as returned by the API. Authoritative for serving; normalized journey_steps/journey_requirements are a derived projection added in a later slice.';
