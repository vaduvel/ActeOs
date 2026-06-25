===
# Event Card — ro.life.vaccination_record (life.vaccination_record)

- batch_id: `B06_VACCINATION_RECORD`
- status: `research_inbox`
- publication_gate: `blocked_pending_human_review`
- pilot: `ro.tm.timisoara`
- accessed_at: `2026-06-25`
- title_ro: Am nevoie de dovada / copia evidenței vaccinărilor

## Declanșator

Titularul sau reprezentantul legal are nevoie de acces la datele de vaccinare ori de un document acceptat pentru școală, călătorie sau alt scop.

## Fapte cerute

| fact | tip | valori / observații |
|---|---|---|
| `purpose` | `enum` | personal_copy \| replace_physical_record \| early_education_entry \| school_entry \| international_travel \| employment |
| `record_holder_known` | `boolean` | dacă furnizorul medical care deține evidența este cunoscut |
| `subject_is_minor` | `boolean` | controlează reprezentarea |
| `school_year` | `string\|null` | regula de 5 zile este verificată doar pentru 2025–2026 |
| `record_discrepancy` | `boolean` | declanșează corectarea la furnizor |
| `county` | `string\|null` | TM pentru canalul pilot DSP |
| `document_within_verified_5_day_window` | `boolean\|null` | calculat pentru regula verificată a educației timpurii 2025–2026 |

## Reguli verificate

- Dreptul verificat este accesul la datele medicale personale; emitentul concret este furnizorul care păstrează evidența.
- Pentru educația timpurie 2025–2026, medicul de familie emite avizul/dovada cu maximum 5 zile înainte de frecventare.
- Nu există în sursele verificate o procedură națională publică unică de „duplicat carnet de vaccinări”; motorul cere confirmarea formatului.

## Conflicte și limitări

- Nu a fost identificat conflict oficial; limitarea esențială este că regula școlară exactă provine din ghidul 2025–2026.

## Canal pilot Timiș/Timișoara

- Furnizorul medical care deține datele, de regulă medicul de familie pentru documentul de intrare în colectivitate.
- DSP Timiș este canal de îndrumare/escaladare, nu emitent universal al dovezii.

## Control de publicare

- source_claims: `4`
- rules: `16`
- golden_fixtures: `22`
- output_status: `draft_not_for_automatic_publication`
===
