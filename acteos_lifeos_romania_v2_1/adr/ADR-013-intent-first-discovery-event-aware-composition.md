# ADR-013 — Intent-first discovery, event-aware composition

- **Status:** Accepted
- **Date:** 2026-06-25
- **Owners:** Product + Architecture
- **Supersedes:** ADR-001 as the public navigation decision

## Context

Users usually approach the product with an action or desired outcome: replace an ID card, register a vehicle, obtain a certificate or enroll a child. A life event remains useful for coordinating related obligations, but it is not the clearest mandatory entry point.

## Decision

The public discovery model is intent-first. Search and category browsing resolve to a canonical `intent_type_id`. Life events remain internal context for bundles, related-intent recommendations and multi-journey composition.

A query may be interpreted by deterministic search and an optional semantic adapter, but every result must map to a published canonical intent and requires user confirmation before a case is created.

## Consequences

- Home asks `Ce vrei să rezolvi?` and keeps categories visible.
- Cases created by v2.1 require `intent_type_id`.
- `event_type_id` is optional context, not the public primary key.
- Analytics use intent IDs for discovery and event IDs only for bundle/context analysis.
- Event Atlas remains valuable and is not deleted.
- Search index and aliases become governed product content.

## Revisit triggers

- measured failure to resolve common Romanian queries;
- catalog maintenance cost exceeds demonstrated value;
- privacy review blocks query handling model;
- a public standard supplies a superior interoperable intent taxonomy.
