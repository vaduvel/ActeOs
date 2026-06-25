# Source Governance

## Chain
Official source -> immutable snapshot -> source claim -> typed rule -> review -> tests -> bundle -> production.

## Authority levels
- national_normative
- national_operational
- county
- uat
- institution
- documented_confirmation
- signal_only

## Conflict policy
Do not resolve conflict by convenience. Store both claims and set route confidence `conflicting` when the conflict affects output.

## Freshness
See `config/freshness_policy.yaml`.
