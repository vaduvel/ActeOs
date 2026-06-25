# Model de domeniu

## 1. Entități principale

### Intent

Obiectiv controlat, de exemplu `ro.education.preschool.enrollment`. Conține sinonime de căutare, categoria de viață și cerințele minime de jurisdicție.

### Jurisdiction

Arbore explicit:

`EU → RO → județ → UAT → instituție → unitate/punct de lucru`

Câmpuri:

- `jurisdiction_id`
- `type`
- `parent_id`
- `name`
- `siruta_code` unde este disponibil și verificat
- `valid_from` / `valid_to`

### Authority

Emitentul unei surse: Parlament, Guvern, minister, inspectorat, UAT, instituție sau unitate.

### Source

URL canonic și metadata persistentă. O sursă are multiple snapshots.

### SourceSnapshot

Conținutul capturat la un moment, hash, headers, status HTTP, parser version, text normalizat și locația blobului.

### SourceClaim

Afirmație atomică extrasă din sursă, cu fragment exact, locator și semantică. O regulă critică nu poate exista fără cel puțin un claim aprobat.

### RuleSet / RuleVersion

Specificație imutabilă a unei călătorii pentru o perioadă și acoperire. `RuleVersion` conține AST-ul executabil și hash canonic.

### FactDefinition / FactValue

Fapte tipate cerute utilizatorului sau derivate determinist. Exemple: `child.birth_date`, `program_type`, `submission_channel`.

### JourneyStep

Acțiune ordonabilă în graf, cu predicate, dependențe, termene, cerințe și dovadă de finalizare.

### Requirement

Document, dată, taxă, original, copie, programare sau condiție ce trebuie satisfăcută.

### RouteSession

Rezultatul evaluării unei versiuni de reguli pentru faptele utilizatorului. Păstrează `rule_bundle_hash`, `facts_hash`, `evaluated_at`, `route_hash`.

### Dossier

Colecția locală/sincronizată de requirements și document metadata pentru un traseu.

### DocumentAsset / DocumentFinding

Asset criptat sau referință locală, plus constatări formale. `authenticity_status` este separat de `readiness_status`.

### Integration

Canal oficial cu capabilități: `deep_link`, `oauth`, `submit`, `status_sync`, `payment`. Fiecare capabilitate are status și dovadă contractuală.

### FeedbackIncident

Raport de teren care intră în review; nu este sursă oficială și nu override-uiește o regulă.

## 2. Tipuri de fapte

- `string`
- `enum`
- `boolean`
- `integer`
- `decimal`
- `date`
- `datetime`
- `country_code`
- `jurisdiction_id`
- `document_reference`
- `set<enum|string>`

Faptele sensibile au `sensitivity`: `public`, `personal`, `sensitive`, `special_category`.

## 3. Predicate executabile

Nu se acceptă expresii text libere. AST-ul suportă:

- `all`, `any`, `not`
- `eq`, `neq`, `in`, `not_in`
- `exists`, `missing`
- `gt`, `gte`, `lt`, `lte`
- `date_before`, `date_on_or_before`, `date_after`, `date_between`
- `age_on_date_gte`, `age_on_date_lt`, `age_on_date_between`
- `jurisdiction_is_descendant_of`
- `has_document_type`
- `document_field_eq`
- `deadline_state_is`

Orice operator nou necesită:

- contract JSON Schema;
- implementare server;
- fixture pozitivă și negativă;
- documentație;
- versiune de engine.

## 4. Ierarhia și rezolvarea conflictelor

Formula greșită „unitatea bate regula națională” este interzisă. Resolverul evaluează:

1. **rang juridic**;
2. **competența emitentului** pentru subiect;
3. **teritoriul**;
4. **perioada de valabilitate**;
5. **normă specială versus generală**;
6. **derogare explicită**;
7. **specificitatea situației**;
8. **starea și prospețimea sursei**.

O regulă locală/unitate poate completa sau particulariza numai în limita competenței și a delegării. Dacă două reguli aplicabile rămân incompatibile, rezultatul este `conflicting` și pasul afectat nu primește verdict definitiv.

### Model de prioritate

- `legal_rank`: 0–100, configurat pe tipul actului, nu pe preferință.
- `competence_scope`: domenii și operațiuni autorizate.
- `specificity_score`: număr de dimensiuni concrete potrivite.
- `explicit_override_of`: lista regulilor suprascrise legitim.
- `effective_from/to`.

Prioritatea numerică nu poate rezolva singură un conflict; explicația și competența sunt obligatorii.

## 5. Temporalitate

Orice evaluare are:

- `reference_date` — data pentru care utilizatorul cere traseul;
- `evaluated_at` — momentul tehnic;
- `rule_bundle_version` și hash;
- timezone explicit.

Un termen poate fi:

- absolut;
- interval;
- relativ la alt pas;
- relativ la un eveniment extern;
- recurent;
- nedefinit încă (`pending_official_publication`).

Datele nedeterminate nu sunt completate cu estimări în producție.

## 6. Stări de încredere

- `verified` — claim oficial și review valid.
- `verified_with_local_gap` — baza este verificată, însă lipsește informația locală necritică.
- `needs_confirmation` — informația critică nu este suficient confirmată.
- `conflicting` — surse aplicabile divergente.
- `expired` — sursa sau regula a depășit pragul de valabilitate.
- `withdrawn` — emitentul a retras-o.

## 7. Separarea readiness de autenticitate

`readiness_status`:

- `unknown`
- `missing`
- `incomplete`
- `invalid_format`
- `expired`
- `needs_user_confirmation`
- `ready_formally`

`authenticity_status`:

- `not_checked`
- `not_verifiable`
- `verified_via_official_registry`
- `registry_mismatch`

UI nu combină cele două într-un singur „valid”.

## 8. Coduri canonice pentru findings

- `DOC_MISSING`
- `DOC_WRONG_TYPE`
- `DOC_UNREADABLE`
- `DOC_PAGE_MISSING`
- `DOC_EXPIRED`
- `DOC_EXPIRES_BEFORE_DEADLINE`
- `DOC_NAME_MISMATCH`
- `DOC_ADDRESS_MISMATCH`
- `DOC_DATE_MISSING`
- `DOC_SIGNATURE_UNCONFIRMED`
- `DOC_FIELD_MISSING`
- `DOC_AUTHENTICITY_NOT_VERIFIED`
- `RULE_SOURCE_STALE`
- `RULE_SOURCE_CONFLICT`
- `LOCAL_REQUIREMENT_MISSING`
- `OFFICIAL_CHANNEL_UNAVAILABLE`
