# Batch 17 — Banking, Digital Life & Religion
# Evenimente: bank_account_open, bank_card_lost_stolen, bank_card_change, home_insurance_claim, life_insurance_claim, electronic_signature, digital_identity_ro, account_recovery_gov, religious_marriage, baptism

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
- ro.life.bank_account_open
- ro.life.bank_card_lost_stolen
- ro.life.bank_card_change
- ro.life.home_insurance_claim
- ro.life.life_insurance_claim
- ro.life.electronic_signature
- ro.life.digital_identity_ro
- ro.life.account_recovery_gov
- ro.life.religious_marriage
- ro.life.baptism

TOTAL: 60 fisiere pentru acest batch (10 evenimente × 6 fisiere).

## CERINTA V2.1 — Intent-first discovery
Pentru FIECARE din cele 10 evenimente de mai jos, in plus fata de cele 5 fisiere (event_card.md, source_claims.yaml, rules.yaml, fixtures/golden.yaml, gaps.md), vei intoarce si un fisier intent_proposal.yaml cu:
- id: ro.intent.<domeniu>.<actiune> (propus)
- title_ro: "Vreau să..." (orientat pe actiune)
- outcome_ro: rezultatul pe care il urmareste utilizatorul
- aliases_ro: [formulari si cautari tipice]
- negative_aliases_ro: [expresii care NU trebuie sa se potriveasca]
- linked_event_ids: [ro.life.<slug>]
- category_id: categoria din taxonomie (identity_documents, home_address_utilities, vehicles_mobility, family_civil_status, education, work_social, health_care, tax_money_penalties, business_self_employment, property_construction, international_citizenship, legal_emergency_civic, banking_insurance, digital_life, religion_cult)
- kind: direct_goal (daca e o singura procedura) / bundle_goal (daca coordoneaza mai multe)

Porneste de la principiul: omul nu spune "ce s-a intamplat" ci "ce vrei sa rezolvi?". Titlul incepe cu un verb sau exprima clar obiectivul.

IMPORTANT: Nu sari peste niciun eveniment. Toate 10 trebuie livrate cu cate 20+ fixtures fiecare. Respecta schemele si enum-urile din documentatia de referinta.
