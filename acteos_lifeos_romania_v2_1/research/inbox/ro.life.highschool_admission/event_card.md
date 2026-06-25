# Event Card — ro.life.highschool_admission (life.highschool_admission)

## Metadata

| field | value |
|---|---|
| batch_id | B05_EDUCATION_1 |
| title_ro | Copilul intră la liceu |
| trigger | copilul intră la liceu |
| reference_date | 2026-06-25 |
| reference_period | admitere 2026-2027 |
| timezone | Europe/Bucharest |
| jurisdiction_scope | RO national + pilot ro.tm / ro.tm.timisoara |
| research_status | verified_with_local_gap |
| production_status | not_published |
| conflict_policy | Nu a fost identificat conflict oficial nerezolvat; orice conflict ulterior blochează efectul critic. |

## Scope

Admiterea inițială în clasa a IX-a pentru anul școlar 2026-2027. Exclude candidații care trebuie să folosească transferul/reînmatricularea și nu substituie procedurile unităților cu probe.

## Required facts

| id | type | required | sensitive | question_ro | options |
|---|---|---|---|---|---|
| candidate.series | enum | true | false | Candidatul este din seria curentă sau anterioară? | current, previous |
| candidate.previously_enrolled | boolean | true | false | A fost deja înmatriculat în liceal/profesional? | — |
| candidate.age_on_school_start | integer | true | true | Ce vârstă are la începutul cursurilor? | — |
| evaluation_national_taken | boolean | true | false | A susținut Evaluarea Națională? | — |
| admission_route | enum | true | false | Ce rută urmărește? | general, aptitude, roma, ces, special_education, evening, reduced_frequency, second_stage |
| reference_date | date | true | false | La ce dată verificăm? | — |
| target_county | string | true | false | În ce județ participă la repartizarea computerizată? | — |
| options_verified | boolean | true | false | Codurile și ordinea opțiunilor sunt verificate? | — |
| allocated | boolean | false | false | Candidatul a fost repartizat? | — |
| local_offer_verified | boolean | true | false | Broșura/codurile Timiș sunt verificate? | — |
| multiple_counties_requested | boolean | false | false | Încerci să completezi opțiuni simultan în mai multe județe? | — |
| candidate.age_on_2026_08_31 | integer | false | true | Ce vârstă are candidatul la 31 august 2026? | — |

## Deterministic route

| step_id | title_ro | completion_evidence | source_claim_ids |
|---|---|---|---|
| step.hs.select_route | Selectează ruta de admitere | Ruta generală/specială/vocațională este confirmată. | claim.hs.scope.current_previous, claim.hs.special_routes |
| step.hs.verify_local_offer | Verifică broșura și codurile | Fiecare opțiune are cod, specializare, limbă, formă și sursă oficială curentă. | claim.hs.timis.local_offer |
| step.hs.complete_options | Completează și verifică opțiunile | Fișa listată este verificată și eventualele erori sunt corectate. | claim.hs.general_calendar |
| step.hs.check_allocation | Verifică repartizarea | Rezultatul din 22 iulie sau al rutei speciale este salvat. | claim.hs.general_calendar, claim.hs.special_routes |
| step.hs.prepare_dossier | Pregătește dosarul de înscriere | Cererea, actele și fișa medicală sunt complete. | claim.hs.dossier |
| step.hs.submit_dossier | Depune dosarul la liceul repartizat | Liceul confirmă înscrierea. | claim.hs.general_calendar, claim.hs.dossier |
| step.hs.second_stage | Intră în a doua etapă | Cererea este primită de comisia județeană și repartizarea este comunicată. | claim.hs.second_stage, claim.hs.en_requirement |

## Requirements

| requirement_id | title_ro | obligation | timing | source_claim_ids |
|---|---|---|---|---|
| req.hs.options_form | Fișa de înscriere cu opțiuni | mandatory | now | claim.hs.general_calendar |
| req.hs.application | Cerere de înscriere la liceul repartizat | mandatory | later | claim.hs.dossier |
| req.hs.identity | Carte de identitate, dacă este cazul | conditional | later | claim.hs.dossier |
| req.hs.birth_certificate | Certificat de naștere | mandatory | later | claim.hs.dossier |
| req.hs.medical_sheet | Fișă medicală | mandatory | later | claim.hs.dossier |
| req.hs.special_evidence | Recomandare/certificat pentru ruta specială | conditional | now | claim.hs.special_routes |

## Official channels

| channel_id | type | label | url | integration_status |
|---|---|---|---|---|
| ch.hs.order | web | Portal Legislativ — Ordinul nr. 6.060/2025 | https://legislatie.just.ro/Public/DetaliiDocument/301910 | SOURCE_ONLY |
| ch.hs.calendar | web | Portal Legislativ — calendar admitere 2026-2027 | https://legislatie.just.ro/Public/DetaliiDocumentAfis/302010 | DEEP_LINK |
| ch.hs.isjtm | web | ISJ Timiș — admitere | https://www.isj.tm.edu.ro/examene-nationale/admitere | SOURCE_ONLY |

## Evidence coverage

| claim_id | confidence | authority_level | locator |
|---|---|---|---|
| claim.hs.scope.current_previous | verified | national_normative | Art. 2 alin. (4) |
| claim.hs.previous_under18 | verified | national_normative | Art. 2 alin. (5) |
| claim.hs.reduced_frequency_age | verified | national_normative | Art. 2 alin. (6) |
| claim.hs.tie_break | verified | national_normative | Art. 2 alin. (9) |
| claim.hs.general_calendar | verified | national_normative | Anexa nr. 1, secțiunea G |
| claim.hs.second_stage | verified | national_normative | Anexa nr. 1, secțiunea H |
| claim.hs.special_routes | verified | national_normative | Anexa nr. 1, secțiunile E-F |
| claim.hs.dossier | verified | national_normative | Art. 2 alin. (23) |
| claim.hs.en_requirement | verified | national_normative | Art. 2 alin. (26)-(27) |
| claim.hs.timis.local_offer | verified_with_local_gap | county | Pagina oficială admitere |
| claim.hs.single_county | verified | national_normative | Art. 2 alin. (32) |

## Release guard

- National effects may be evaluated only from claims marked `verified` and still fresh.
- Institution/UAT-specific dates, places, fees, criteria, schedules or document variants remain `verified_with_local_gap` or `needs_confirmation` until independently reviewed.
- This pack is research input; `rules.yaml` remains `draft`/`in_review` and is not an active ruleset.
