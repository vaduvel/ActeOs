# 05 — Intent Context & Deterministic Rule Engine

## 1. Scop

Motorul transformă un `Case` asociat unui `intent_type_id` confirmat și un set de fapte într-un `Journey`. El nu caută pe web în timpul rezolvării și nu apelează LLM-uri. Primește un ruleset publicat și produce un rezultat reproductibil.

## 1A. Separarea resolverelor

`Intent Resolver` selectează un ID canonic din catalog și se oprește la confirmarea utilizatorului. `Rule Engine` primește acel ID, faptele, data, jurisdicția și ruleset-ul. Primul rezolvă limbajul; al doilea rezolvă adevărul administrativ.

## 2. Contractul de intrare

```json
{
  "intent_type_id": "ro.identity.change_address",
  "reference_date": "2026-06-25",
  "timezone": "Europe/Bucharest",
  "jurisdiction_path": ["eu", "ro", "ro.tm", "ro.tm.timisoara"],
  "subject": {"role": "self", "subject_id": "optional"},
  "facts": {
    "new_address_occupancy": "owner",
    "owns_vehicle": true,
    "is_company_administrator": false
  },
  "ruleset_version": "ro.tm.timisoara@2026.06.25.1"
}
```

Câmpurile lipsă necesare nu sunt ghicite. Motorul returnează `missing_facts` și nu materializează o concluzie care depinde de ele.

## 3. Contractul de ieșire

```json
{
  "resolution_id": "uuid",
  "status": "resolved",
  "journey": {"...": "..."},
  "missing_facts": [],
  "warnings": [],
  "conflicts": [],
  "explanation": {
    "included_rule_ids": [],
    "excluded_rule_ids": [],
    "facts_hash": "sha256",
    "engine_version": "2.1.0"
  }
}
```

Statusuri: `resolved`, `needs_facts`, `needs_confirmation`, `conflicting`, `blocked`, `no_active_ruleset`.

## 4. Tipuri canonice

- `IntentType`: obiectiv administrativ canonic publicat;
- `Case`: instanța utilizatorului pentru un intent confirmat;
- `LifeEventType`: context opțional pentru bundle-uri și recomandări;
- `FactDefinition`: întrebare tipată;
- `FactValue`: răspuns validat;
- `Rule`: condiție + efect;
- `StepTemplate`: pas reutilizabil;
- `RequirementTemplate`: act/informație necesară;
- `OfficialChannel`: destinație oficială;
- `SourceClaim`: dovadă atomică;
- `RuleSet`: colecție publicată și imutabilă;
- `Journey`: rezultat materializat;
- `ResolutionTrace`: explicația evaluării.

## 5. Predicate DSL

Condițiile sunt un AST JSON restricționat. Nu se acceptă cod arbitrar sau text liber executabil.

### Operatori logici

- `all`: toate expresiile sunt adevărate;
- `any`: minimum una;
- `not`: negație;
- `const`: boolean literal.

### Operatori de comparație

- `eq`, `neq`;
- `in`, `not_in`;
- `lt`, `lte`, `gt`, `gte`;
- `exists`, `missing`;
- `contains`, doar pentru liste normalizate;
- `matches_enum`, nu regex liber din conținut.

### Operatori temporali

- `date_before`, `date_after`, `date_between`;
- `age_on_date_gte`, `age_on_date_lt`;
- `days_between_lte`;
- `within_window`;
- `deadline_relative_to` pentru pași, nu pentru eligibilitate nedefinită.

### Operatori de jurisdicție

- `jurisdiction_is`;
- `jurisdiction_descends_from`;
- `institution_is`;
- `authority_scope_contains`.

### Exemplu

```yaml
when:
  all:
    - op: eq
      field: facts.owns_vehicle
      value: true
    - op: jurisdiction_descends_from
      field: context.jurisdiction_path
      value: ro.tm.timisoara
```

## 6. Efectele unei reguli

- `include_step`;
- `exclude_step`;
- `include_requirement`;
- `set_requirement_obligation`;
- `set_deadline`;
- `attach_channel`;
- `emit_warning`;
- `block`;
- `require_confirmation`;
- `trigger_child_event`;
- `set_freshness_state`.

Efectele sunt declarative. O regulă nu poate executa I/O.

## 7. Pipeline de rezolvare

1. validează schema inputului;
2. normalizează datele și enumurile;
3. selectează ruleset-ul activ pentru intent, dată și jurisdicție;
4. verifică integritatea claim-urilor și freshness;
5. calculează facts required de condițiile candidate;
6. returnează `needs_facts` dacă lipsesc date obligatorii;
7. evaluează gate-urile în ordine de prioritate;
8. aplică regulile de includere/excludere;
9. construiește graful pașilor;
10. detectează cicluri și referințe inexistente;
11. sortează topologic, cu tie-breaker stabil;
12. atașează cerințe, canale, termene și claims;
13. aplică politica de conflict și prospețime;
14. materializează journey-ul și trace-ul;
15. calculează hash-ul rezultatului.

## 8. Jurisdiction Resolver

Arborele de bază: `EU → RO → județ → UAT → instituție`. O regulă are `authority_level`, `competence_scope`, `territory`, `effective_from/to` și `specificity`.

Ordinea de selecție:

1. elimină regulile inactive temporal;
2. elimină regulile din afara teritoriului;
3. verifică dacă emitentul are competență declarată;
4. aplică normele obligatorii de rang superior;
5. aplică norma specială/locală numai în spațiul permis;
6. dacă două efecte incompatibile rămân active, creează conflict.

Resolverul nu pretinde interpretare juridică autonomă. Relațiile de override trebuie declarate și aprobate în rule metadata.

## 9. Temporal Engine

Toate intervalele sunt half-open `[effective_from, effective_to)` dacă nu există motiv normativ explicit. Datele fără oră sunt evaluate în `Europe/Bucharest`. Deadline-urile păstrează tipul:

- `fixed_instant`;
- `fixed_window`;
- `relative_business_days`;
- `relative_calendar_days`;
- `institution_schedule`;
- `unknown_pending_publication`.

Nu convertim „în termen de X zile lucrătoare” în zile calendaristice. Calendarul sărbătorilor este versionat separat.

## 10. Conflict model

Conflictul conține:

- regulile și claim-urile implicate;
- câmpul sau efectul incompatibil;
- rangul și competența fiecărei surse;
- perioada comună;
- impactul: informational/operational/critical;
- acțiunea: warn/needs_confirmation/block;
- textul exact pentru utilizator și întrebarea de confirmare.

Un conflict nu poate fi „rezolvat” de scorul de încredere dacă ambele surse sunt oficiale și active.

## 11. Freshness

Înainte de aplicare, fiecare claim este evaluat:

- `fresh`: înainte de review_due;
- `stale`: după review_due, înainte de hard_expiry;
- `hard_expired`: după hard_expiry;
- `source_unavailable`: verificarea curentă a eșuat;
- `withdrawn` sau `superseded`.

Politica depinde de clasă. Pentru `critical`, hard expiry blochează efectul. Pentru `operational`, poate fi afișat cu warning. Pentru `explanatory`, cache-ul poate rămâne disponibil mai mult.

## 12. Journey composition

Pașii au `semantic_key` stabil, de exemplu `identity.update_address`. La recalculare:

- dacă semantic key și subiectul rămân aceleași, progresul poate fi păstrat;
- dacă cerințele obligatorii s-au schimbat, pasul revine la `needs_review`;
- dacă pasul dispare, este arhivat cu motiv;
- dacă apare un pas nou înaintea unuia finalizat, journey-ul semnalează ruta schimbată.

## 13. Stări

### Journey

`draft → active → needs_review → completed | cancelled | archived`

### Step

`locked → available → in_progress → ready_to_submit → submitted → completed`

Stări auxiliare: `blocked`, `needs_confirmation`, `failed`, `skipped_not_applicable`.

### Requirement

`missing`, `provided`, `needs_review`, `ready`, `expired`, `rejected`, `not_applicable`.

## 14. Determinism

Pentru același input canonic și aceleași artefacte versionate, outputul serializat canonic trebuie să aibă același hash. Surse de nondeterminism interzise:

- ordinea DB fără `ORDER BY`;
- timp curent citit intern în loc de `reference_date`;
- UUID random incluse în hash-ul semantic;
- seturi neordonate;
- LLM sau rețea;
- locale/timezone implicită a serverului.

## 15. Proprietăți testabile

- **Idempotence:** rezolvarea repetată nu schimbă rezultatul semantic.
- **Monotonic missing facts:** adăugarea unui fapt cerut reduce sau păstrează lista de lipsuri, nu o crește arbitrar.
- **No orphan step:** fiecare dependency există.
- **Acyclic journey:** graful publicabil nu conține cicluri.
- **Critical evidence:** orice efect critical are claim activ.
- **Temporal boundary:** exact la effective_to regula nu mai este activă.
- **Conflict visibility:** efecte incompatibile nu produc silently winner.
- **No test leakage:** ruleset production nu referă surse synthetic.

## 16. Pseudocod

```python
def resolve(request, ruleset):
    canonical = validate_and_normalize(request)
    candidates = ruleset.select(canonical.intent_type_id,
                                canonical.reference_date,
                                canonical.jurisdiction_path)
    evidence_state = validate_evidence(candidates, canonical.reference_date)
    required = collect_required_facts(candidates)
    if missing := required - canonical.facts.keys():
        return needs_facts(missing)
    gates = evaluate_gates(candidates, canonical)
    if gates.blocking:
        return blocked(gates)
    effects = evaluate_rules(candidates, canonical)
    graph = compose_graph(effects)
    validate_graph(graph)
    conflicts = detect_conflicts(effects, evidence_state)
    journey = materialize(graph, conflicts, canonical)
    return with_trace(journey, candidates, canonical)
```

## 17. Coduri de eroare relevante

- `RULESET_NOT_FOUND`
- `RULESET_INTEGRITY_FAILED`
- `MISSING_REQUIRED_FACTS`
- `RULE_CONDITION_INVALID`
- `RULE_EFFECT_INVALID`
- `RULE_CLAIM_MISSING`
- `CLAIM_HARD_EXPIRED`
- `RULE_CONFLICT_CRITICAL`
- `JOURNEY_GRAPH_CYCLE`
- `JOURNEY_REFERENCE_MISSING`
- `JURISDICTION_UNRESOLVED`
- `TEMPORAL_WINDOW_INVALID`

Lista completă este în `contracts/error_codes.yaml`.
