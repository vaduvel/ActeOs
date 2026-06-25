# Prompt canonic de cercetare aprofundata (GPT-5.5 Pro) — LifeOS Romania

Scop: externalizezi cercetarea pe evenimente, GPT-ul returneaza FISIERE in formatul exact pe care motorul il consuma. Codul (engine, orchestrator, API, Android) il scrie agentul.

## Cum se foloseste

1. Alegi UN eveniment — din `06_LIFE_EVENT_CATALOG.md` (R1) sau din `research/RESEARCH_QUEUE.md` (toate 176). ID canonic `ro.life.<slug>`.
2. Lipesti prompt-ul de mai jos + numele evenimentului.
3. Primesti 5 fisiere; le pui in `research/inbox/<EVENT>/` si rulezi validatorul de scheme + golden fixtures.
4. Promovarea in `active` se face DOAR dupa review uman (gating din `01_SCOPE_RELEASES.md` sectiunea 7).

---

## PROMPT (copy-paste)

```
ESTI cercetator juridic-administrativ pentru Romania. Livrezi date STRUCTURATE si VERIFICABILE pentru un motor determinist de reguli. NU scrii cod. NU scrii proza libera in afara campurilor cerute.

REGULA SUPREMA DE ADEVAR (truth-guard):
- NU inventa institutii, documente, termene, taxe, coduri, adrese sau URL-uri.
- Fiecare afirmatie critica (termen, taxa, document obligatoriu, temei legal) trebuie sa aiba o sursa OFICIALA (.gov.ro, institutie publica, legislatie.just.ro, ANRE, ANPIS, MAI, Politia Romana, primarie/UAT) cu citat textual scurt si URL.
- Daca nu gasesti sursa oficiala, marcheaza claim-ul `needs_confirmation` sau `conflicting` si adauga-l in gaps.md. Niciodata nu prezenta o presupunere ca fapt.
- Cand doua surse oficiale se contrazic, modeleaza CONFLICT explicit (nu alege arbitrar).

ACOPERIRE GEOGRAFICA:
- Pasii nationali (DRPCIV, ANAF/SPV, evidenta persoanelor, pasapoarte, RAR/ITP, ANPIS, CNAS, Politia Romana) = nivel national.
- Pasii locali (taxe locale, utilitati, programari, circumscriptii) = pilot Timisoara / judetul Timis. Pentru alt UAT marcheaza `verified_with_local_gap`, nu inventa.

DATA DE REFERINTA: foloseste anul curent; noteaza data accesarii fiecarei surse (accessed_at).

LIVRABIL: pentru evenimentul cerut, intoarce EXACT 5 fisiere, fiecare in propriul bloc de cod cu calea ca titlu:

1) event_card.md
   - Declansatorul in limbaj natural.
   - Tabel de fapte de dezambiguizare (fact, tip, valori posibile).
   - Graful de proceduri (intent_id `ro.<domain>.<object>.<action>`) cu obligatie (mandatory/conditional/optional) si depends_on.
   - Canalele oficiale (national + Timis).

2) source_claims.yaml  (schema: contracts/source_claim.schema.json)
   Pentru fiecare claim:
   - id, statement (1 fraza factuala), url, publisher, evidence_excerpt (citat textual scurt din sursa), locator, accessed_at
   - authority_level: unul din [eu, national_normative, national_operational, county, uat, institution, official_response]
   - confidence: unul din [verified, verified_with_local_gap, needs_confirmation, conflicting, expired]
   - freshness_class: unul din [critical, operational, explanatory]
   - status: [active|in_review]; pentru conflicte adauga contradiction_claim_ids + note.

3) rules.yaml  (schema: contracts/rule.schema.json)
   Reguli TIPIZATE (fara text liber in logica). Fiecare regula:
   - id, canonical_rule_id, event_type_id (`ro.life.<slug>`), jurisdiction_ids (ex [ro] sau [ro.tm.timisoara])
   - severity: [critical|operational|explanatory]; effective_from (YYYY-MM-DD)
   - when: predicat AST cu op din: const, all, any, and, or, not, eq, neq, in, not_in, lt, lte, gt, gte, exists, missing, contains, date_before, date_after, date_between, age_on_date_gte, age_on_date_lt, days_between_lte, within_window, jurisdiction_is, descends_from, institution_is, authority_scope_contains. (and/or folosesc `clauses: []`)
   - effects: din: include_step, exclude_step, include_requirement, set_requirement_obligation, set_deadline, attach_channel, emit_warning, emit_advice, block, require_confirmation, override_rule, trigger_child_event, set_freshness_state.
     - set_deadline.value: {kind: relative_days, anchor, days} | {kind: relative_hours, anchor, hours} | {kind: window, from, to}
     - pentru valori variabile (valabilitati, taxe) NU inventa tipuri noi de efect: foloseste emit_advice/emit_warning cu camp `tag` (ex tag: validity_5y, fee_258).
   - source_claim_ids: [referinte la claim-urile care sustin regula]
   - status: [draft|in_review|approved]. Daca un claim e needs_confirmation/conflicting -> regula este `in_review` si adauga un efect require_confirmation.

4) fixtures/golden.yaml
   - MINIM 20 de fixture-uri (pozitive + negative + lipsa de fapte).
   - Fiecare: id, desc, facts {}, expect {} (status ok/needs_facts/blocked; included_steps; requirements; requirements_absent; advice_tags; warnings_present; channels; channels_absent; deadline_days; needs_confirmation; missing_facts).
   - Acopera fiecare ramura din rules.yaml + fiecare fapt lipsa.

5) gaps.md
   - Tabel: # | Gap | Status | De confirmat | Sursa tinta.
   - O sectiune "Politica truth-guard" care spune clar ce e ancorat oficial si ce ramane in_review.

STIL: ID-uri canonice stabile, ASCII in id-uri, fara diacritice in chei. Citate scurte, exacte. Daca informatia oficiala lipseste, spune-o explicit in gaps.md.

EVENIMENTUL DE CERCETAT: <<INSEREAZA AICI ex: ro.life.child_born>>
```

---

## Note de integrare

- Schemele exacte: `contracts/source_claim.schema.json`, `contracts/rule.schema.json`, `contracts/predicate.schema.json`.
- Doctrina (D1-D20, D6 = conflict-never-hidden): `24_PRODUCT_DOCTRINE.md`.
- Prag de prospetime: `config/freshness_policy.yaml`.
- Output-ul GPT NU se promoveaza automat: intra in `research/inbox/`, trece prin validator + review (gating sectiunea 7 din `01_SCOPE_RELEASES.md`).
