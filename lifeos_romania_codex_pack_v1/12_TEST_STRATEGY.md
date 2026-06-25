# Test Strategy

## Required suites
- Schema validation.
- Predicate evaluator unit tests.
- Route determinism golden tests.
- Source governance tests.
- Freshness expiry tests.
- Document readiness fixture tests.
- Mobile E2E happy paths.
- Partner neutrality tests.

## Golden flows
1. `life.moved` with owns_vehicle=true and is_company_admin=true.
2. `life.bought_vehicle` person physical, RO vehicle, no import.
3. `life.lost_documents` with CI + driver license + vehicle certificate.
4. `life.local_taxes_certificate` for demo UAT.
