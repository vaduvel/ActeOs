---
name: acteos-release-certification
description: Use before any ActeOS production release, ruleset activation, migration rollout or security-sensitive deployment.
---

# ActeOS Release Certification

## Goal

Demonstrează că release-ul poate fi lansat gradual, observat și retras fără a pierde trasabilitatea sau datele.

## Procedure

1. Îngheață scope-ul și leagă release-ul de stories, ADR-uri, migrations și ruleset IDs.
2. Rulează pack validation, lint, typecheck, unit, property, integration, contract și E2E.
3. Rulează a11y, privacy, SAST, dependency, secret, container și API security checks aplicabile.
4. Repetă migrations pe staging/copie și testează restore/rollback.
5. Verifică freshness/conflicts/four-eyes pentru fiecare claim critic activat.
6. Generează rule bundle manifest, checksums, signature metadata, SBOM și provenance.
7. Verifică feature flags, kill switches, dashboards, alerts și on-call owner.
8. Execută staged rollout cu cohortă mică și criterii explicite de abort.
9. Monitorizează SLO, resolver errors, wrong-route feedback și privacy signals.
10. Înregistrează verdictul: go, conditional_go sau no_go, cu dovezi.

## Automatic no-go conditions

- claim critic expirat/conflicting/unapproved;
- migration fără restore/forward recovery demonstrată;
- testdata în bundle-ul de producție;
- PII în log/analytics/crash payload;
- contract breaking necoordonat;
- lipsa kill switch-ului pentru o funcție/ruleset cu risc;
- autorul este singurul aprobator al conținutului critic.

## Completion evidence

- checklist semnat;
- validation outputs și artefacte identificate prin hash;
- rollout/rollback record;
- release notes și known risks;
- post-release verdict în ExecPlan și incident handoff dacă este cazul.
