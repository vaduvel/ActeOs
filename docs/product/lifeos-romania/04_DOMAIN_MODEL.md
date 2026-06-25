# Model de domeniu — LifeOS România

Acest model **extinde** modelul anterior. Entitățile de procedură (Intent, Jurisdiction, Source, RuleVersion, JourneyStep, Requirement, RouteSession, Dossier, DocumentAsset, FeedbackIncident etc.) rămân valabile. Se adaugă stratul de **eveniment de viață**.

## 1. Entități noi

### LifeEvent

Eveniment de viață controlat, ex. `ro.life.move_residence`. Câmpuri:

- `life_event_id` (StableId)
- `category` (ex. `housing`, `auto`, `children`, `identity`)
- `frequency_tier` (`high` 🔥 / `medium` ⭐ / `low` 🏔️)
- `nl_synonyms` — expresii în limbaj natural pentru clasificator (date de antrenare/matching, nu obligații)
- `disambiguation_facts` — fapte care decid ramurile
- `procedures` — listă de `ProcedureRef`
- `status` (`draft` / `production` / `hidden`)

### ProcedureRef

Legătura dintre un eveniment și o procedură (intent). Câmpuri:

- `intent_id` — procedura atomică
- `applies_when` — predicat tipat (același AST ca motorul); dacă `unknown`, nodul devine `needs_confirmation`, nu se omite tăcut
- `depends_on` — listă de `intent_id` care trebuie finalizate înainte
- `phase_order` — întreg pentru ordonare stabilă
- `obligation` — `mandatory` / `conditional` / `optional` / `later`
- `deadline_origin` — `fixed` / `calendar_rule` / `relative_to_step`
- `rationale_claim_ref` — dovada pentru includere și dependență (obligatorie pentru noduri critice)

### EventPlan (rezultat)

Rezultatul orchestrării pentru fapte concrete:

- `event_plan_id`, `life_event_id`, `jurisdiction_id`, `reference_date`, `evaluated_at`
- `bundle_set` — bundle-urile folosite per procedură
- `facts_hash`, `event_plan_hash`
- `nodes` — procedurile instanțiate cu stare și dependențe rezolvate
- `edges` — dependențele efective
- `confidence` — agregat din nodurile critice (cel mai slăbit nivel domină)
- `conflicts`, `unresolved_questions`

### EventPlanSession

Persistă planul evaluat, analog `RouteSession`, cu `event_plan_hash` reproductibil.

## 2. Relația cu procedura

Un nod din EventPlan referă o `RouteSession` (rezultatul motorului pentru acel intent). Orchestratorul **nu** reimplementează logica de rutare; doar selectează, ordonează și partajează faptele.

## 3. Fapte partajate

Faptele se definesc o singură dată (`FactDefinition`) și sunt partajate între procedurile aceluiași eveniment. Tipuri și sensibilitate ca în modelul anterior (`public`/`personal`/`sensitive`/`special_category`). Faptele lipsă nu sunt `false`; logica rămâne tri-valued.

## 4. Rezolvarea conflictelor

Neschimbată la nivel de procedură (rang juridic, competență, teritoriu, perioadă, special vs general, derogare, specificitate, prospețime). La nivel de eveniment se adaugă: dacă două proceduri au dependențe incompatibile (ciclu sau ordine contradictorie), planul marchează `conflicting` și nodurile afectate nu primesc verdict de ordine definitiv.

## 5. Temporalitate

Fiecare plan are `reference_date`, `evaluated_at`, bundle versions și timezone `Europe/Bucharest`. Termenele relative între proceduri (ex. „în 90 de zile de la dobândirea proprietății") se rezolvă din evenimentul-ancoră.

## 6. Stări de încredere și findings

Identice cu modelul anterior (`verified` … `withdrawn`; coduri `DOC_*`, `RULE_SOURCE_*`, `LOCAL_REQUIREMENT_MISSING`, `OFFICIAL_CHANNEL_UNAVAILABLE`). Se adaugă codul `EVENT_NODE_DEPENDENCY_UNVERIFIED` pentru dependențe fără claim aprobat.
