# Specificația motorului determinist de reguli

## 1. Scop

Motorul primește un bundle publicat, fapte tipate, jurisdicție și dată de referință și returnează un traseu reproductibil. Nu apelează internetul, LLM-ul, OCR-ul sau baze de date externe în timpul evaluării.

## 2. Contract de intrare

```json
{
  "intent_id": "ro.education.preschool.enrollment",
  "jurisdiction_id": "ro.tm.timisoara",
  "reference_date": "2026-06-25",
  "facts": {
    "child.birth_date": "2022-10-10",
    "current_enrolment.same_unit": false,
    "program_type": "extended",
    "parents.employment_status": "both_working",
    "submission_channel": "in_person"
  },
  "requested_rule_version": null
}
```

## 3. Contract de ieșire

```json
{
  "route_id": "uuid",
  "intent_id": "ro.education.preschool.enrollment",
  "rule_bundle_version": "2026.1.0",
  "rule_bundle_hash": "sha256:...",
  "facts_hash": "sha256:...",
  "evaluated_at": "2026-06-25T12:00:00Z",
  "reference_date": "2026-06-25",
  "route_hash": "sha256:...",
  "confidence": "verified",
  "steps": [],
  "requirements": [],
  "unresolved_questions": [],
  "conflicts": [],
  "warnings": []
}
```

## 4. Algoritmul obligatoriu

```text
resolve(request):
  validate request against contract
  locate one published bundle matching intent, jurisdiction and reference_date
  verify bundle signature/hash and engine compatibility
  canonicalize facts and compute facts_hash
  select applicable rule fragments by jurisdiction ancestry and time
  validate legal competence and explicit overrides
  detect unresolved conflicts; mark affected claims/requirements
  evaluate typed predicates without dynamic code execution
  instantiate applicable steps and requirements
  resolve relative deadlines
  construct dependency graph
  reject cycles and dangling dependencies
  topologically sort using stable secondary order
  compute step/requirement confidence from source claims and freshness
  attach provenance
  canonicalize output excluding route_id and evaluated_at
  compute route_hash
  persist RouteSession
  return output
```

## 5. Canonicalizare și hash

- JSON este serializat canonic, cu chei ordonate și format stabil.
- Datele sunt ISO 8601.
- Timezone-urile sunt păstrate; pentru România se folosește `Europe/Bucharest`.
- Seturile sunt sortate lexical după ID.
- `route_hash` exclude câmpurile nondeterministe.
- `engine_version` este inclus în materialul de hash.

## 6. Ordinea stabilă a pașilor

1. dependențe topologice;
2. `phase_order`;
3. `priority`;
4. `step_id` lexical.

Astfel, două execuții nu schimbă arbitrar ordinea.

## 7. Necunoscute

Faptele lipsă nu sunt echivalente cu `false`.

Predicatele au logică tri-valued:

- `true`
- `false`
- `unknown`

Dacă `unknown` afectează un pas critic, motorul emite `unresolved_question` și nu presupune ramura convenabilă.

## 8. Freshness și date stale

### Clasa A — critică

Eligibilitate, document obligatoriu, termen, taxă, canal de depunere, criteriu de departajare. Nu se servește tăcut peste prag. Rezultat: `needs_confirmation` sau blocare punctuală.

### Clasa B — operațională

Program, adresă, telefon, locuri disponibile. Poate fi afișată ultima valoare cu avertisment clar și timestamp dacă riscul este acceptat de politica sursei.

### Clasa C — explicativă

Ghiduri și context. Poate fi cache-uită mai mult dacă nu schimbă decizia.

Pragurile sunt configurate per source, nu hardcodate global.

## 9. Publicarea bundle-ului

Un bundle publicat conține:

- schema version;
- engine compatibility range;
- intent și acoperire;
- toate regulile și claim-urile necesare;
- source snapshot IDs;
- test manifest și rezultat;
- semnătura/hash;
- reviewer IDs și timestamps;
- changelog.

## 10. Impact analysis

Înainte de publicare:

- rulează fixture-urile versiunii curente și candidate;
- compară route hashes și rezultate;
- clasifică schimbările așteptate/neexplicate;
- blochează publicarea dacă un traseu pierde provenance, introduce ciclu, schimbă un document critic fără claim sau crește conflict count.

## 11. Pseudocod predicate

```python
class EvalResult(Enum):
    TRUE = "true"
    FALSE = "false"
    UNKNOWN = "unknown"


def eval_expr(expr, facts, context):
    op = expr["op"]
    if op == "all":
        return tri_all(eval_expr(x, facts, context) for x in expr["args"])
    if op == "any":
        return tri_any(eval_expr(x, facts, context) for x in expr["args"])
    if op == "eq":
        value = facts.get(expr["fact"], MISSING)
        return UNKNOWN if value is MISSING else bool_to_tri(value == expr["value"])
    if op == "age_on_date_between":
        birth = parse_date(facts.get(expr["fact"]))
        if birth is None:
            return UNKNOWN
        age = completed_years(birth, parse_date(expr["on_date"]))
        return bool_to_tri(expr["min"] <= age < expr["max_exclusive"])
    raise UnsupportedOperator(op)
```

Implementarea reală trebuie să fie exhaustivă, tipată și acoperită de property-based tests.

## 12. Invariante

- Nicio cerință critică fără claim aprobat.
- Niciun pas aplicabil fără jurisdicție și interval temporal.
- Niciun deadline în trecut prezentat ca acțiune activă fără rută de remediere.
- Niciun deep-link către domeniu neallowlisted.
- Niciun conflict critic ascuns.
- Nicio condiție text liberă.
- Nicio schimbare publicată fără test manifest.
