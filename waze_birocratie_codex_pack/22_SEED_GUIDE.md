# Seed and content loading guide

`make seed-verified` must:

1. validate every file in `seed/rules/` against `contracts/rule.schema.json`;
2. reject any rule whose status is not approved/published for the configured channel;
3. verify every referenced claim ID exists;
4. verify each critical requirement/gate/step has source claims;
5. validate effective dates and freshness timestamps;
6. canonicalize and calculate rule hashes;
7. load sources, snapshots/claims, rule families and versions transactionally;
8. run fixture tests before creating a canary bundle;
9. never fetch the internet;
10. never load `content_gaps_timisoara.json` as a rule.

The national seeds are reference content. They still require the application's curator/publisher workflow before production. Local data is deliberately absent where it could not be verified without live institutional curation.
