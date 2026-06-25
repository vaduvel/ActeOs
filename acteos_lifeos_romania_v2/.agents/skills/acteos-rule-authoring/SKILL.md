---
name: acteos-rule-authoring
description: Use when creating, changing, importing, reviewing or publishing ActeOS administrative source claims, rules, rulesets, predicates, deadlines, requirements or official channels.
---

# ActeOS Rule Authoring

## Goal

Transformă dovezi oficiale în reguli atomice, tipate, versionate și publicabile fără a inventa obligații administrative.

## Required inputs

- sursa oficială/snapshotul și hash-ul;
- jurisdicția, autoritatea, rangul și perioada aplicabilă;
- claim-uri atomice cu citat și locator;
- schema din `contracts/jsonschema/`;
- politica de prospețime și conflict;
- story/requirement IDs.

## Procedure

1. Confirmă că materialul este în `research/inbox` sau în registrul surselor, nu direct în producție.
2. Verifică publisherul, competența, data, teritoriul și dacă sursa este superseded.
3. Creează câte un claim pentru fiecare obligație care se poate schimba independent.
4. Leagă fiecare claim de citatul exact și locator; nu extinde sensul dovezii.
5. Modelează condiția în predicate AST tipat; nu folosi text liber executabil.
6. Modelează intervalul temporal și timezone explicit.
7. Aplică ierarhia juridică prin authority/competence/specificity, nu prin simpla proximitate locală.
8. Marchează conflictele fără a alege arbitrar un câștigător.
9. Configurează review_due, hard_expiry și on_expiry conform riscului.
10. Rulează schema validation, static rule validation, cycle/conflict checks și golden simulations.
11. Obține review independent pentru orice claim critic.
12. Publică numai într-un ruleset imutabil cu manifest, hash, approvers și rollback pointer.

## Never do

- Nu inventa act, taxă, deadline, canal, adresă sau eligibilitate.
- Nu publica rezultatul LLM direct.
- Nu combina două obligații independente într-un claim.
- Nu permite unui claim expirat/conflictual să producă verde.
- Nu confunda OCR/coerența formală cu autenticitatea.

## Completion evidence

- schemele trec;
- toate referințele există;
- diff-ul de ruleset este revizuit;
- golden cases și impact simulation sunt verzi;
- four-eyes approval este în audit;
- `codex/EXECUTION_PLAN.md` și implementation status sunt actualizate.
