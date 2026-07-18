# packages/source-ingestion

Logică de ingestie surse partajată: fetch adapters, normalizare, diff, review, publish, rollback.

## Module

| Modul | Descriere |
|-------|-----------|
| `registry.py` | Source registry (CRUD, domain allowlist, fetch scheduling) |
| `fetcher.py` | Bounded fetcher cu SSRF protection (scheme, IP, domain, size, timeout) |
| `snapshot.py` | Immutable content-addressed snapshot store (SHA-256) |
| `normalize.py` | HTML → plain text normalization (stdlib only) |
| `diff.py` | Snapshot diff + severity classification (none/cosmetic/moderate/critical) |
| `impact.py` | Impact analysis (care claims/rules sunt afectate de o schimbare) |
| `ai_adapter.py` | Optional AI draft extraction (`AI_EXTRACTION_ENABLED` flag) |
| `review.py` | Human review workflow (2 reviewers for critical, no self-approval) |
| `publish.py` | Atomic publish + rollback (pointer-based, history never deleted) |
| `staleness.py` | Staleness scheduler (time-travel testable) |

## Exit gate P3

- [x] controlled HTML/PDF fixtures traverse fetch-to-draft
- [x] AI output cannot publish itself
- [x] critical changes require two distinct reviewers
- [x] staleness alerts are time-travel tested
- [x] rollback restores the production pointer without deleting history
- [x] SSRF/malformed document tests pass

## Tests

```bash
make bootstrap
cd packages/source-ingestion && ../../.venv/bin/python -m pytest tests/ -v
```
