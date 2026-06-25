# packages/rule-engine

Pure deterministic rule engine. **No network, database, clock or LLM at evaluation
time** — `now` is injected, the bundle is passed in.

- `resolve(request, bundle, *, now)` returns a reproducible route with
  `rule_bundle_hash`, `facts_hash` and `route_hash`. The route hash excludes
  `route_id` and `evaluated_at`, and includes `engine_version`.
- Three-valued logic (`true`/`false`/`unknown`); a missing fact is never coerced to
  false. Unknown on a critical gate/step becomes an `unresolved_question`.
- Stable topological ordering of steps by (dependencies, sequence_hint, id).

Status: P2 core engine + unit/property tests. Full lawful-precedence merge and the
broad route fixture suite are follow-up P2 stories.

```bash
cd packages/rule-engine && python -m pip install -e '.[dev]' && python -m pytest -q
```
