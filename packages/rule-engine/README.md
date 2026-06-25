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

## Authoring executor & golden runner (`wb_rule_engine.authoring`)

Governed research lives in the *authoring* contract language
(`docs/product/lifeos-romania/contracts/rule.schema.json` +
`predicate.schema.json`): rules use `op`/`field` predicates and a typed `effects`
vocabulary. This is the language the GPT deep-research batches under
`research/inbox/<EVENT>/` are written in — distinct from the compiled runtime
`bundle` language used by `resolve`.

The `authoring` subpackage evaluates that language directly:

- `authoring.evaluate(pred, facts, ctx)` — typed predicate AST evaluator
  (const/all/any/not, eq/neq/in/.../date_*/age_*/jurisdiction_*), trivalent.
- `authoring.evaluate_ruleset(ruleset, facts, *, jurisdiction_path, reference_date)`
  — applies effects and returns a `RouteResult` (included steps, requirements,
  channels, advice, warnings, confirmations, `missing_facts`, status).
- `authoring.run_fixtures(batch)` — runs a batch's `fixtures/golden.yaml` and
  reports pass/fail per fixture.

The pure pieces import with **no third-party dependency**. File loaders
(`authoring.loader`, `authoring.cli`) require PyYAML (`[authoring]` extra).

Run every governed batch's golden fixtures:

```bash
cd packages/rule-engine && python -m pip install -e '.[authoring]'
wb-golden                      # defaults to docs/product/lifeos-romania/research/inbox
# or: python -m wb_rule_engine.authoring <INBOX_DIR>
```

Exits non-zero if any fixture fails, so it can gate CI before a batch is
promoted out of `inbox`.
