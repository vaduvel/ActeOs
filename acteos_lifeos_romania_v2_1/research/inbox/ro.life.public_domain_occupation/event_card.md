# Event Card — ro.life.public_domain_occupation (life.public_domain_occupation)

**Titlu:** Vreau acord pentru ocuparea temporară a domeniului public  
**Batch:** B09_PUBLIC_DOMAIN_OCCUPATION  
**Status:** `research_inbox` — neaprobat; nu se publică în producție înainte de review independent  
**Pilot jurisdicție:** `ro.tm.timisoara`  
**Accessed_at:** `2026-06-25`

## Declanșator

Utilizatorul dorește să ocupe temporar domeniul public și să obțină acordul înainte de utilizare.

## Fapte cerute (typed facts)

| fact | tip | valori / sens |
|---|---|---|
| `jurisdiction_id` | jurisdiction id | UAT competent |
| `applicant_type` | enum | natural_person/legal_person |
| `occupation_type` | enum | scaffold/construction_site/scaffold_and_construction_site/other |
| `has_building_authorisation` | boolean | fact de selecție caz |
| `is_historic_or_protected_area` | boolean | fact de selecție caz |
| `payment_requested_after_review` | boolean | taxa a fost calculată |
| `payment_completed` | boolean | plata realizată |

## Obligații și ramuri

| step_id | condiție | efect determinist | dovezi |
|---|---|---|---|
| `classify_public_domain_occupation` | întotdeauna | stabilește cazul local | `claim.tm.domain.case_facts` |
| `submit_occupation_request` | caz Timișoara suportat | trimite dosarul | `claim.tm.domain.online_steps` |
| `pay_assessed_occupation_charge` | plată solicitată | achită suma calculată | `claim.tm.domain.payment_after_check` |
| `download_public_domain_agreement` | plată finalizată | descarcă acordul | `claim.tm.domain.payment_after_check` |

## Canale oficiale

| arie | canal | stare |
|---|---|---|
| Timișoara | Portal servicii PMT — ocupare domeniu public | `verified_with_local_gap` |
| alte UAT | autoritatea locală competentă | `verified_with_local_gap` |

## Note de guvernanță

- Acordul este condiționat de plata solicitată după verificarea dosarului.
- Tipurile din portalul pilot nu sunt extinse artificial la alte utilizări.
- Nu se publică o taxă generică fără anexă/caz confirmat.

===
