# Batch 08 — Property & Construction
# Evenimente: declare_home_local_tax, declare_property_local_tax, property_cadastral_registration, land_split_merge, building_permit, demolition_permit, renovation_authorisation_check, house_extension, construction_reception, construction_start_notice

## PROMPT (copy-paste in GPT-5.5 Pro Deep Research)

ESTI cercetator juridic-administrativ pentru Romania. Livrezi date STRUCTURATE si VERIFICABILE pentru un motor determinist de reguli. NU scrii cod. NU scrii proza libera in afara campurilor cerute.

REGULA SUPREMA DE ADEVAR (truth-guard):
- NU inventa institutii, documente, termene, taxe, coduri, adrese sau URL-uri.
- Fiecare afirmatie critica (termen, taxa, document obligatoriu, temei legal) trebuie sa aiba o sursa OFICIALA (.gov.ro, institutie publica, legislatie.just.ro, ANRE, ANPIS, MAI, Politia Romana, primarie/UAT) cu citat textual scurt si URL.
- Daca nu gasesti sursa oficiala, marcheaza claim-ul `needs_confirmation` sau `conflicting` si adauga-l in gaps.md. Niciodata nu prezenta o presupunere ca fapt.
- Cand doua surse oficiale se contrazic, modeleaza CONFLICT explicit (nu alege arbitrar).

ACOPERIRE GEOGRAFICA:
- Pasii nationali = nivel national.
- Pasii locali (taxe locale, utilitati, programari, circumscriptii) = pilot Timisoara / judetul Timis. Pentru alt UAT marcheaza `verified_with_local_gap`, nu inventa.

DATA DE REFERINTA: foloseste anul curent; noteaza data accesarii fiecarei surse (accessed_at).

LIVRABIL: Pentru FIECARE din cele 10 evenimente de mai jos, intoarce exact 5 fisiere (event_card.md, source_claims.yaml, rules.yaml, fixtures/golden.yaml, gaps.md). Delimiteaza fiecare eveniment cu o linie `===`.

Evenimente de cercetat (toate 10 in aceeasi rulare):
- ro.life.declare_home_local_tax
- ro.life.declare_property_local_tax
- ro.life.property_cadastral_registration
- ro.life.land_split_merge
- ro.life.building_permit
- ro.life.demolition_permit
- ro.life.renovation_authorisation_check
- ro.life.house_extension
- ro.life.construction_reception
- ro.life.construction_start_notice

TOTAL: 60 fisiere pentru acest batch (10 evenimente × 6 fisiere: event_card, source_claims, rules, fixtures, gaps, intent_proposal).

## CERINTA V2.1 — Intent-first discovery
Pentru FIECARE din cele 10 evenimente de mai jos, in plus fata de cele 5 fisiere (event_card.md, source_claims.yaml, rules.yaml, fixtures/golden.yaml, gaps.md), vei intoarce si un fisier intent_proposal.yaml cu:
- id: ro.intent.<domeniu>.<actiune> (propus)
- title_ro: "Vreau să..." (orientat pe actiune)
- outcome_ro: rezultatul pe care il urmareste utilizatorul
- aliases_ro: [formulari si cautari tipice]
- negative_aliases_ro: [expresii care NU trebuie sa se potriveasca]
- linked_event_ids: [ro.life.<slug>]
- category_id: categoria din taxonomie (identity_documents, home_address_utilities, vehicles_mobility, family_civil_status, education, work_social, health_care, tax_money_penalties, business_self_employment, property_construction, international_citizenship, legal_emergency_civic)
- kind: direct_goal (daca e o singura procedura) / bundle_goal (daca coordoneaza mai multe)

Porneste de la principiul: omul nu spune "ce s-a intamplat" ci "ce vrei sa rezolvi?". Titlul incepe cu un verb sau exprima clar obiectivul.

IMPORTANT: Nu sari peste niciun eveniment. Toate 10 trebuie livrate cu cate 20+ fixtures fiecare. Respecta schemele si enum-urile din documentatia de referinta.