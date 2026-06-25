# API and worker

Phase P1 creates a FastAPI modular monolith. Domain packages must not import adapters directly. The rule engine is a pure module and is tested independently. The worker imports the same application services but runs background jobs through a PostgreSQL-backed queue/outbox.

Expected modules: identity, catalog, cases, resolver, content, documents, channels, notifications, feedback, audit, operations.
