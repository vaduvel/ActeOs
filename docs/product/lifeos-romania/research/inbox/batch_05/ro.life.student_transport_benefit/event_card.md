# Event Card — ro.life.student_transport_benefit (life.student_transport_benefit)

## Metadata

| field | value |
|---|---|
| batch_id | B05_EDUCATION_1 |
| title_ro | Solicit facilitate de transport ca elev/student |
| trigger | solicit facilitate de transport ca elev sau student |
| reference_date | 2026-06-25 |
| reference_period | regim 2026 verificat la 2026-06-25 |
| timezone | Europe/Bucharest |
| jurisdiction_scope | RO national + pilot ro.tm / ro.tm.timisoara |
| research_status | verified_with_local_gap |
| production_status | not_published |
| conflict_policy | Nu a fost identificat conflict oficial nerezolvat; orice conflict ulterior blochează efectul critic. |

## Scope

Două ramuri: gratuitatea elevilor și reducerea studenților. Pentru studenți, override-ul fiscal-bugetar din 2026 restrânge traseele eligibile și expiră la 31 decembrie 2026.

## Required facts

| id | type | required | sensitive | question_ro | options |
|---|---|---|---|---|---|
| beneficiary_type | enum | true | false | Beneficiarul este elev sau student universitar? | pupil, university_student |
| institution_authorized_or_accredited | boolean | true | false | Instituția este autorizată/acreditată? | — |
| study_mode | enum | true | false | Care este forma de studiu? | full_time, part_time, distance, preuniversity |
| beneficiary_age | integer | true | true | Ce vârstă are beneficiarul? | — |
| transport_mode | enum | true | false | Ce tip de transport folosește? | local, metro, road, rail, naval, school_route, lump_sum |
| reference_date | date | true | false | La ce dată se solicită facilitatea? | — |
| route_relation | enum | true | false | Ce relație are traseul cu domiciliul și instituția? | domicile_to_institution, institution_city_local, other_route |
| boarding_or_hosted | boolean | false | true | Elevul este cazat la internat/gazdă? | — |
| public_transport_service_available | boolean | false | false | Există serviciu public pe ruta necesară? | — |
| proof_of_status_available | boolean | true | false | Există carnet/document de elev/student? | — |
| local_process_verified | boolean | true | false | Procedura operatorului/instituției este verificată? | — |

## Deterministic route

| step_id | title_ro | completion_evidence | source_claim_ids |
|---|---|---|---|
| step.transport.select_regime | Selectează regimul elev/student și anul | Legea și derogarea temporală aplicabilă sunt identificate. | claim.transport.pupil.free, claim.transport.student.permanent, claim.transport.student.2026_road_rail |
| step.transport.verify_route | Verifică traseul eligibil | Originea, destinația și tipul de transport respectă regula aplicabilă. | claim.transport.student.2026_road_rail, claim.transport.student.2026_local, claim.transport.pupil.free |
| step.transport.prepare_proof | Pregătește dovada statutului | Documentul emis/vizat de instituție este valabil. | claim.transport.pupil.proof, claim.transport.student.methodology_2026 |
| step.transport.obtain_benefit | Solicită titlul/reducerea prin canalul oficial | Abonamentul, biletul redus sau confirmarea decontului este emisă. | claim.transport.student.methodology_2026, claim.transport.local_process |
| step.transport.lump_sum | Solicită suma forfetară pentru elev | Consiliul județean/unitatea confirmă eligibilitatea și cuantumul curent. | claim.transport.pupil.lump_sum |
| step.transport.boarding_trips | Folosește călătoriile elevului cazat | Documentele de transport și dovada cazării sunt păstrate. | claim.transport.pupil.boarding |

## Requirements

| requirement_id | title_ro | obligation | timing | source_claim_ids |
|---|---|---|---|---|
| req.transport.status_proof | Document de elev/student valabil | mandatory | now | claim.transport.pupil.proof, claim.transport.student.methodology_2026 |
| req.transport.route_proof | Dovada domiciliului și a localității instituției | conditional | now | claim.transport.student.2026_road_rail |
| req.transport.boarding_proof | Dovada cazării la internat/gazdă și documentele de călătorie | conditional | now | claim.transport.pupil.boarding |
| req.transport.lump_sum_file | Dosarul local pentru suma forfetară | conditional | now | claim.transport.pupil.lump_sum |
| req.transport.operator_documents | Documentele cerute de operator/instituție | conditional | now | claim.transport.local_process |

## Official channels

| channel_id | type | label | url | integration_status |
|---|---|---|---|---|
| ch.transport.law198 | web | Portal Legislativ — Legea învățământului preuniversitar | https://legislatie.just.ro/Public/DetaliiDocument/271896 | SOURCE_ONLY |
| ch.transport.law199 | web | Portal Legislativ — Legea învățământului superior | https://legislatie.just.ro/Public/DetaliiDocument/271898 | SOURCE_ONLY |
| ch.transport.methodology | web | Ministerul Educației — facilități studenți | https://www.edu.ro/facilitati-studenti | SOURCE_ONLY |

## Evidence coverage

| claim_id | confidence | authority_level | locator |
|---|---|---|---|
| claim.transport.pupil.free | verified | national_normative | Art. 83 alin. (1) |
| claim.transport.pupil.boarding | verified | national_normative | Art. 83 alin. (2) |
| claim.transport.pupil.proof | verified | national_normative | Art. 83 |
| claim.transport.pupil.lump_sum | verified | national_normative | Art. 83 |
| claim.transport.student.permanent | verified | national_normative | Art. 128 alin. (3) |
| claim.transport.student.2026_road_rail | verified | national_normative | Derogare aplicabilă în 2026, art. XXXV din Legea nr. 141/2025 |
| claim.transport.student.2026_local | verified | national_normative | Derogare aplicabilă în 2026, art. XXXV din Legea nr. 141/2025 |
| claim.transport.student.methodology_2026 | verified | national_operational | Cadru normativ — facilități studenți |
| claim.transport.local_process | verified_with_local_gap | national_operational | Cadru normativ |

## Release guard

- National effects may be evaluated only from claims marked `verified` and still fresh.
- Institution/UAT-specific dates, places, fees, criteria, schedules or document variants remain `verified_with_local_gap` or `needs_confirmation` until independently reviewed.
- This pack is research input; `rules.yaml` remains `draft`/`in_review` and is not an active ruleset.
