# Event Card — ro.life.suspend_business (life.suspend_business)

**Batch:** B12_SUSPEND_BUSINESS  
**Status:** research_inbox (neaprobat)  
**Pilot:** `ro.tm.timisoara`  
**Accessed_at:** 2026-06-25

## Declanșator

„Vreau să suspend temporar activitatea.”

## Limita evenimentului

Acoperă înscrierea întreruperii temporare pentru PFA sau SRL, maximum trei ani. Nu tratează suspendarea ONRC ca oprire automată a tuturor obligațiilor fiscale, contractuale sau de muncă.

## Fapte cerute

| fact | tip | valori / semnificație | obligatoriu |
|---|---|---|---|
| `entity_type` | `enum` | pfa sau srl | da |
| `requested_duration_months` | `integer` | durata suspendării, maximum 36 luni | da |
| `currently_suspended` | `boolean` | există deja o mențiune activă | da |
| `decision_date` | `date` | data deciziei pentru SRL | condițional |
| `filing_actor` | `enum` | titular/reprezentant/mandatar/avocat | da |
| `filing_channel` | `enum` | counter, post_courier, online | da |
| `has_employees` | `boolean` | există salariați | da |
| `tax_registrations_present` | `boolean` | există vector fiscal relevant | da |
| `local_commercial_agreement_exists` | `boolean` | există acord local | condițional |

## Pași determinați

| step_id | rezultat | gate principal |
|---|---|---|
| `approve_pfa_interruption` | decizie titular PFA | durata legală |
| `file_pfa_suspension_mention` | mențiune PFA | semnatar și canal |
| `approve_srl_temporary_inactivity` | hotărâre SRL | durata și competența |
| `file_srl_suspension_mention` | mențiune SRL | termen de depunere |
| `review_timisoara_agreement_during_suspension` | revizuire acord local | efectul suspendării asupra acordului |

## Reguli-cheie verificate

- Suspendarea temporară nu poate depăși trei ani.
- ONRC publică proceduri distincte pentru PFA și persoane juridice.
- Nereluarea societății după perioada maximă poate declanșa dizolvarea.
- Depunerea online cere semnătură electronică calificată.

## Canal pilot Timișoara / Timiș

Statutul acordului comercial Timișoara pe durata suspendării se confirmă în cazul concret; motorul nu presupune anularea automată.

## Guvernanță

Evenimentul este un bundle: mențiunea ONRC este nucleul, iar taxele, salariații, contractele și autorizațiile sunt verificări copil obligatorii când sunt aplicabile.
