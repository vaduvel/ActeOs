===
# Event Card — ro.life.medical_certificate_school (life.medical_certificate_school)

- batch_id: `B06_MEDICAL_CERTIFICATE_SCHOOL`
- status: `research_inbox`
- publication_gate: `blocked_pending_human_review`
- pilot: `ro.tm.timisoara`
- accessed_at: `2026-06-25`
- title_ro: Am nevoie de o adeverință medicală pentru școală

## Declanșator

Părintele, elevul sau studentul trebuie să obțină un document medical pentru intrarea în colectivitate, un dosar de orientare, revenire după boală ori alt scop școlar.

## Fapte cerute

| fact | tip | valori / observații |
|---|---|---|
| `certificate_purpose` | `enum` | entry_collectivity \| special_education_file \| return_after_illness \| sports_exemption \| school_transfer \| generic_school_request |
| `education_level` | `enum` | early_education \| primary \| secondary \| vocational \| higher_education |
| `school_year` | `string` | anul pentru care se solicită documentul |
| `service_provider` | `enum\|null` | family_doctor \| school_medical_office \| specialist_doctor \| private_clinic |
| `a5_provider_dsp_authorized` | `boolean\|null` | necesar pentru dosarul de orientare |
| `county` | `string\|null` | TM pentru pilot |
| `epi_within_verified_5_day_window` | `boolean\|null` | calculat pentru educația timpurie 2025–2026 |

## Reguli verificate

- Pentru educația timpurie 2025–2026 sunt verificate două documente: adeverința clinică în prima zi și avizul/dovada de vaccinare emis(ă) cu maximum 5 zile înainte.
- Pentru orientarea școlară/profesională, dosarul medical include A5 de la o unitate abilitată de DSP și fișa medicală sintetică gratuită de la medicul de familie.
- Gratuitatea legală privește serviciile cabinetului medical/stomatologic școlar; nu se extinde automat la orice adeverință a medicului de familie.

## Conflicte și limitări

- Nu există conflict oficial identificat; ghidul de intrare în colectivitate este limitat temporal la anul școlar 2025–2026.

## Canal pilot Timiș/Timișoara

- Medicul de familie pentru documentele verificate de intrare în colectivitate și fișa sintetică.
- Unitate abilitată de DSP pentru certificatul A5.
- DSP Timiș — canal de confirmare pentru unitățile abilitate și cerințele sanitare locale.

## Control de publicare

- source_claims: `6`
- rules: `16`
- golden_fixtures: `22`
- output_status: `draft_not_for_automatic_publication`
===
