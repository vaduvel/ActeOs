# Event Card — ro.life.urbanism_certificate (life.urbanism_certificate)

**Titlu:** Vreau să obțin un certificat de urbanism  
**Batch:** B09_URBANISM_CERTIFICATE  
**Status:** `research_inbox` — neaprobat; nu se publică în producție înainte de review independent  
**Pilot jurisdicție:** `ro.tm.timisoara`  
**Accessed_at:** `2026-06-25`

## Declanșator

Utilizatorul urmărește emiterea unui certificat de urbanism pentru un imobil și un scop identificat.

## Fapte cerute (typed facts)

| fact | tip | valori / sens |
|---|---|---|
| `property_locality` | string | localitatea imobilului |
| `request_purpose` | string | scopul explicit |
| `cadastral_data_applicable` | boolean | dacă datele cadastrale sunt aplicabile |
| `cadastral_number` | string\|null | unde este cazul |
| `land_book_number` | string\|null | unde este cazul |
| `jurisdiction_id` | jurisdiction id | UAT competent |
| `purpose_class` | enum | construction/puz/pud/listed_notarial_operation/exit_coownership_partition/other |
| `construction_or_infrastructure_purpose` | boolean | pentru excepția de indiviziune |
| `request_submitted` | boolean | cerere înregistrată |
| `request_registered_at` | date\|null | ancoră termen |
| `consents_digital_delivery` | boolean | acord e-mail |

## Obligații și ramuri

| step_id | condiție | efect determinist | dovezi |
|---|---|---|---|
| `define_purpose_and_property` | întotdeauna | identifică scopul și imobilul | `claim.urbanism.requester_identification_purpose` |
| `select_timisoara_case` | Timișoara | alege cazul din portal | `claim.tm.urbanism.online_cases` |
| `submit_request` | dosar pregătit | înregistrează cererea | `claim.tm.urbanism.steps` |
| `receive_certificate` | cerere înregistrată | termen maxim 15 zile lucrătoare | `claim.urbanism.deadline_15wd` |
| `obtain_certificate_before_notarial_operation` | operațiune enumerată | nu încheia operațiunea fără certificat | `claim.urbanism.notarial_operations` |

## Canale oficiale

| arie | canal | stare |
|---|---|---|
| național | autoritatea competentă potrivit Legii 50/1991 | `verified` |
| Timișoara | Portal servicii PMT — certificat de urbanism | `verified_with_local_gap` |
| alte UAT | portal/registratură locală | `verified_with_local_gap` |

## Note de guvernanță

- Certificatul nu este autorizație de construire.
- Actele și taxa locală nu sunt extrapolate către alte UAT-uri.
- Datele cadastrale sunt cerute numai unde sunt aplicabile.

===
