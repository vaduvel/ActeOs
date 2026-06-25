# Motorul determinist + orchestratorul de evenimente

## Partea A — Motorul de procedură (neschimbat)

Motorul primește un bundle publicat, fapte tipate, jurisdicție și dată de referință și returnează un traseu reproductibil pentru **o procedură** (intent). Nu apelează internet, LLM, OCR sau baze externe la evaluare.

Contractele de intrare/ieșire, canonicalizarea, `route_hash`, logica tri-valued, freshness (clasele A/B/C), publicarea bundle-ului și invariantele rămân cele din implementarea curentă (`wb_rule_engine`). Acest workbook nu le modifică.

## Partea B — Orchestratorul de evenimente (nou)

### B.1 Scop

Dat fiind un `life_event_id`, fapte tipate, jurisdicție și dată de referință, orchestratorul produce un **plan de eveniment** reproductibil: ce proceduri se aplică, în ce ordine și cu ce dependențe. Nu evaluează internet/LLM. Reutilizează motorul de procedură pentru fiecare nod.

### B.2 Contract de intrare

```json
{
  "life_event_id": "ro.life.move_residence",
  "jurisdiction_id": "ro.tm.timisoara",
  "reference_date": "2026-06-25",
  "facts": {
    "person.owns_vehicle": true,
    "person.has_minor_children": false,
    "person.is_self_employed": false,
    "move.same_county": false
  }
}
```

### B.3 Contract de ieșire

```json
{
  "event_plan_id": "uuid",
  "life_event_id": "ro.life.move_residence",
  "jurisdiction_id": "ro.tm.timisoara",
  "reference_date": "2026-06-25",
  "evaluated_at": "2026-06-25T12:00:00Z",
  "facts_hash": "sha256:...",
  "event_plan_hash": "sha256:...",
  "confidence": "verified_with_local_gap",
  "nodes": [
    {
      "intent_id": "ro.identity.id_card.address_change",
      "obligation": "mandatory",
      "state": "actionable",
      "depends_on": [],
      "route_ref": "route_session_uuid"
    },
    {
      "intent_id": "ro.auto.registration_certificate.address_update",
      "obligation": "mandatory",
      "state": "upcoming",
      "depends_on": ["ro.identity.id_card.address_change"],
      "route_ref": null
    }
  ],
  "edges": [["ro.identity.id_card.address_change", "ro.auto.registration_certificate.address_update"]],
  "conflicts": [],
  "unresolved_questions": []
}
```

### B.4 Algoritm obligatoriu

```text
plan_event(request):
  validate request against contract
  load LifeEvent definition by life_event_id (published)
  canonicalize facts and compute facts_hash
  for each ProcedureRef:
    evaluate applies_when (tri-valued)
      TRUE  -> include node
      FALSE -> exclude node
      UNKNOWN -> include as needs_confirmation + emit unresolved_question
  build dependency graph from depends_on of included nodes
  drop edges pointing to excluded nodes; record as informational
  reject cycles (=> conflicting)
  topologically sort using stable secondary order (phase_order, intent_id)
  assign node.state: actionable (no unmet deps), upcoming (has unmet deps), conditional (obligation=conditional)
  aggregate confidence = weakest critical node confidence
  canonicalize output excluding event_plan_id and evaluated_at
  compute event_plan_hash (includes engine_version + orchestrator_version)
  persist EventPlanSession
  return output
```

### B.5 Determinism și hash

- JSON canonic, chei ordonate, seturi sortate lexical, ISO 8601, `Europe/Bucharest`.
- `event_plan_hash` exclude `event_plan_id` și `evaluated_at`.
- Materialul de hash include `engine_version` și `orchestrator_version`.
- Procedurile individuale își păstrează `route_hash`; planul nu îl recalculează, îl referă.

### B.6 Necunoscute

Un fapt de dezambiguizare lipsă nu înseamnă „procedura nu se aplică". Dacă `applies_when` este `unknown` pentru un nod critic, nodul apare ca `needs_confirmation` cu întrebarea exactă.

### B.7 Impact analysis

Înainte de publicarea unui eveniment sau a unei modificări de dependențe: rulează fixture-urile de plan curente și candidate; compară `event_plan_hash` și grafurile; blochează publicarea dacă apare ciclu, se pierde un claim de dependență, sau crește conflict count.

### B.8 Invariante

- Niciun eveniment publicat cu graf ciclic.
- Niciun nod critic fără claim aprobat pentru includere și pentru fiecare dependență.
- Nicio dependență către un intent inexistent sau nepublicat.
- Nicio compunere care marchează `verified` un eveniment cu noduri critice `needs_confirmation`.
- Niciun text liber drept condiție de aplicabilitate.
