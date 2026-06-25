# Event Card — ro.life.civil_status_duplicate (life.civil_status_duplicate)

**Batch:** B01_CIVIL_STATUS_DUPLICATE  
**Status:** research_inbox (neaprobat)  
**Pilot:** `ro.tm.timisoara`  
**Accessed_at:** 2026-06-25

## Declanșator

„Am pierdut / mi s-a deteriorat certificatul de naștere, căsătorie sau deces și am nevoie de alt exemplar.”

## Limita evenimentului

Acoperă eliberarea la cerere a unui certificat/extras existent. Nu acoperă înregistrarea tardivă, reconstituirea actului inexistent sau rectificarea fondului actului.

## Fapte cerute

| fact | tip | valori / semnificație | obligatoriu |
|---|---|---|---|
| `certificate_type` | `enum` | `birth`, `marriage`, `death` | da |
| `requester_role` | `enum` | `holder`, `legal_representative`, `family`, `entitled`, `other`, `proxy`, `lawyer` | da |
| `legitimate_interest` | `boolean` | interes legitim | condițional |
| `mayor_approval` | `boolean` | aprobarea primarului | condițional |
| `request_channel` | `enum` | `counter`, `electronic`, `email`, `post`, `consulate` | da |
| `in_romania` | `boolean` | locul solicitantului | da |
| `valid_identity` | `boolean` | act de identitate valabil | da |
| `old_certificate_exchange` | `boolean` | preschimbare | da |
| `status_changed` | `boolean` | modificare a statutului civil | da |
| `record_location` | `enum` | `timisoara`, `other_ro`, `unknown` | da |

## Pași determinați

| step_id | rezultat | gate principal |
|---|---|---|
| `request_civil_status_certificate` | certificat/extras eliberat | calitate, identitate, canal, dosar |

## Reguli-cheie verificate

- Naștere/căsătorie: titular sau reprezentant legal; deces: familie ori persoană îndreptățită.
- Pentru o altă persoană care cere certificatul de deces sunt necesare interesul legitim și aprobarea primarului competent.
- Procura specială și împuternicirea avocațială sunt admise de lege.
- Există un conflict operațional real între posibilitatea legală de emitere electronică și pagina HUB care spune că serviciul nu gestionează documente electronice.

## Canal pilot Timișoara / Timiș

Pagina locală disponibilă redirecționează către arhiva Primăriei Timișoara; toate cerințele locale din aceasta rămân `needs_confirmation` până la o pagină curentă.

## Guvernanță

Motorul nu transformă pagina arhivată într-o obligație verde. Conflictul electronic și conflictul privind taxa rămân vizibile și blochează certitudinea operațională.
