# Event Card — ro.life.administrative_decision_contest (life.administrative_decision_contest)

**Batch:** BATCH_11_PENSIONS_HEALTH_ADMIN  
**Status:** research_inbox — neaprobat pentru producție  
**Pilot jurisdicție locală:** `ro.tm.timisoara`  
**Data de referință:** 2026-06-25  
**Accessed_at surse:** 2026-06-25

## Declanșator

„Vreau să contest o decizie administrativă”.

## Limită de domeniu

Acoperă traseul general al Legii nr. 554/2004 pentru actele administrative individuale sau normative: verificarea procedurii speciale, plângerea prealabilă, termenele acțiunii, competența, documentele, taxa și suspendarea. Procedurile speciale prevalează și sunt rutate separat.

## Fapte cerute (typed facts)

| fact | tip | valori / sens | obligatoriu |
|---|---|---|---|
| `act_type` | enum | individual / normative | da |
| `recipient_role` | enum | addressee / third_party | pentru act individual |
| `special_judicial_procedure_checked` | boolean | a fost verificată o lege organică specială | da |
| `special_judicial_procedure_exists` | boolean | există altă procedură judiciară | da |
| `prior_complaint_exception_confirmed` | boolean | excepție art. 7 alin. (5) confirmată | da |
| `communication_date` | date\|null | data comunicării destinatarului | după caz |
| `issue_date` | date\|null | data emiterii actului | pentru limita destinatarului |
| `knowledge_date` | date\|null | data luării la cunoștință de terț | pentru terț |
| `days_since_communication` | integer\|null | zile calendaristice calculate de serviciul temporal | după caz |
| `days_since_knowledge` | integer\|null | zile de la luarea la cunoștință | după caz |
| `within_6_months_of_issue` | boolean\|null | calcul calendaristic al limitei de 6 luni | pentru destinatar tardiv |
| `within_6_months_of_knowledge` | boolean\|null | calcul calendaristic al limitei de 6 luni | pentru terț tardiv |
| `justified_late_reasons` | boolean | motive temeinice pentru plângerea tardivă | după caz |
| `court_action_planned` | boolean | utilizatorul pregătește sesizarea instanței | da |
| `within_6_months_of_court_anchor` | boolean | calcul de la ancora art. 11 alin. (1) | pentru act individual |
| `within_1_year_of_court_anchor` | boolean | limita exterioară art. 11 alin. (2) | pentru act individual tardiv |
| `justified_court_delay_reasons` | boolean | motive temeinice pentru acțiune tardivă | după caz |
| `authority_level` | enum | local / county / central | pentru competență |
| `fiscal_case` | boolean | litigiu fiscal/vamal/contribuții | da |
| `fiscal_amount_lei` | number\|null | valoarea relevantă pentru pragul legal | pentru litigiu fiscal |
| `claimant_type` | enum | private / public | da |
| `claimant_jurisdiction_id` | jurisdiction_id | domiciliul sau sediul reclamantului privat | după caz |
| `requests_damages` | boolean | există capăt patrimonial | da |
| `claimed_damages_lei` | number\|null | valoarea pretinsă | pentru despăgubiri |
| `requests_suspension` | boolean | se solicită suspendarea | da |
| `well_justified_case` | boolean | caz bine justificat | pentru suspendare |
| `imminent_damage` | boolean | pagubă iminentă | pentru suspendare |
| `suspension_procedural_trigger_met` | boolean | sesizarea autorității sau ipoteza legală echivalentă | pentru suspendare |
| `suspension_mode` | enum | none / before_main_action / with_main_action / after_main_action | pentru suspendare |
| `days_since_main_action` | integer\|null | zile de la acțiunea principală | pentru cererea separată |
| `main_action_filed_within_60_days` | boolean | safeguard art. 14 | pentru suspendare înainte de fond |

## Traseu determinist

1. **verify_special_judicial_procedure** — verifică dacă o procedură judiciară specială exclude traseul general — `verified`.
2. **prepare_prior_complaint** — formulează plângerea prealabilă când este obligatorie — `verified`.
3. **calculate_court_action_window** — calculează termenul de 6 luni și limita exterioară de un an — `verified`.
4. **identify_competent_court** — stabilește competența materială și teritorială — `verified_with_local_gap`.
5. **prepare_and_file_court_action** — atașează actul/dovezile, timbrează și depune — `verified_with_local_gap`.
6. **evaluate_suspension** — evaluează separat suspendarea și ferestrele de 60 de zile — `verified`.

## Canale oficiale

- `ch.issuing_or_hierarchically_superior_authority` — autoritatea emitentă sau ierarhic superioară, după caz
- `ch.portal.just.ro.courts` — Portalul instanțelor pentru identificarea instanței și a datelor oficiale
- `ch.competent_administrative_fiscal_court` — registratura instanței competente; canalul concret se verifică la data depunerii

## Excluderi și hand-off

- Nu înlocuiește procedura specială pentru amenzi contravenționale, pensii, fiscalitate, achiziții, stare civilă sau alte materii cu cale proprie.
- Nu stabilește automat că actul este nelegal și nu promite anularea lui.
- Nu calculează termenele calendaristice prin conversia lunilor în 180/183 de zile; folosește date și ferestre calendaristice.
- Nu inventează instanța ori canalul local fără verificarea competenței și a paginii oficiale curente.

## Note de guvernanță

- Gate-ul de procedură specială este obligatoriu înaintea oricărei recomandări de fond.
- Pentru destinatar, limita tardivă a plângerii prealabile se raportează la emiterea actului; pentru terț, la luarea la cunoștință.
- Ancora celor 6 luni pentru acțiunea în instanță diferă după răspuns, refuz, expirarea termenului sau excepția de la plângerea prealabilă.
- Pilotul local Timișoara nu fixează automat Tribunalul Timiș ori Curtea de Apel Timișoara fără evaluarea tuturor faptelor de competență.
