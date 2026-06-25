# Batch 10 — Work & Employment
# Evenimente: started_job, changed_job, lost_job, unemployment_benefit, medical_leave, employment_history_proof, hire_first_employee, work_abroad, return_to_ro_work, home_care_support

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
- ro.life.started_job
- ro.life.changed_job
- ro.life.lost_job
- ro.life.unemployment_benefit
- ro.life.medical_leave
- ro.life.employment_history_proof
- ro.life.hire_first_employee
- ro.life.work_abroad
- ro.life.return_to_ro_work
- ro.life.home_care_support

TOTAL: 50 fisiere pentru acest batch.

IMPORTANT: Nu sari peste niciun eveniment. Toate 10 trebuie livrate cu cate 20+ fixtures fiecare. Respecta schemele si enum-urile din documentatia de referinta.