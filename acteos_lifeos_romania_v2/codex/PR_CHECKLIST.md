# Pull Request Checklist

## Purpose
- [ ] Requirement/story IDs linked
- [ ] Scope and out-of-scope stated

## Contracts
- [ ] OpenAPI updated first where needed
- [ ] Generated clients refreshed
- [ ] JSON Schemas validated
- [ ] Migration added/reviewed

## Quality
- [ ] Unit/property/contract tests
- [ ] Error/offline/loading states
- [ ] Accessibility review
- [ ] Observability added

## Safety
- [ ] No PII in logs/analytics
- [ ] Authz/RLS verified
- [ ] No synthetic data in production bundle
- [ ] No LLM runtime decision for critical rules
- [ ] Official route remains visible

## Operations
- [ ] Rollback described
- [ ] Feature flag/kill switch considered
- [ ] Docs and implementation status updated
