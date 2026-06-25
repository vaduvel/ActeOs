# packages/contracts

Canonical contracts, **canonical JSON hashing** (cross-language reference) and the
shared error vocabulary.

- `wb_contracts.canonical` — `canonical_json` / `sha256_hex`. These hashing rules MUST
  be matched byte-for-byte by the Kotlin and TypeScript implementations.
- `wb_contracts.errors` — problem+json error codes (`ProblemCode`, `WbError`).
- `wb_contracts.schema` — JSON Schema validation helper (schemas live in the pack).

Status: P1 core (hashing, errors, schema util). DB models/migrations, field
encryption, append-only audit and idempotency are the remaining P1 stories.

```bash
cd packages/contracts && python -m pip install -e '.[dev]' && python -m pytest -q
```
