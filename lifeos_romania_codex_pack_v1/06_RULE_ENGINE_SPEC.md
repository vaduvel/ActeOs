# Rule Engine Spec

## Determinism
`route = f(event_type, facts, jurisdiction, reference_date, bundle_version, engine_version)`.

## Predicate operators
- equals / not_equals
- is_true / is_false / is_unknown
- in / not_in
- all / any / not
- date_before / date_after / date_between
- jurisdiction_matches
- exists / missing

## Ternary logic
Unknown is not false. If unknown affects a critical branch, output `NEEDS_FACTS`.

## Invariants
- Same canonical input => same route_hash.
- Critical requirement without source_claim_ids is invalid unless `demo_mode=true`.
- Expired critical rule cannot produce READY_TO_SUBMIT.
