# Event Card — ro.life.resume_business (life.resume_business)

**Batch:** B12_RESUME_BUSINESS  
**Status:** research_inbox (neaprobat)  
**Pilot:** `ro.tm.timisoara`  
**Accessed_at:** 2026-06-25

## Declanșator

„Vreau să reiau activitatea firmei sau PFA-ului.”

## Limita evenimentului

Acoperă mențiunea de reluare după o suspendare temporară valabilă. Nu presupune că sediul, codurile CAEN, avizele, obligațiile fiscale sau acordurile locale sunt încă valabile.

## Fapte cerute

| fact | tip | valori / semnificație | obligatoriu |
|---|---|---|---|
| `entity_type` | `enum` | pfa sau srl | da |
| `currently_suspended` | `boolean` | există mențiune de suspendare activă | da |
| `suspension_elapsed_months` | `integer` | luni de la înscrierea suspendării | da |
| `activities_still_registered_authorized` | `boolean` | activitățile rămân înregistrate și autorizate | da |
| `seat_use_right_still_valid` | `boolean` | dreptul de sediu este valabil | da |
| `resume_decision_date` | `date` | data deciziei SRL | condițional |
| `filing_actor` | `enum` | titular/reprezentant/mandatar/avocat | da |
| `local_commercial_activity` | `boolean` | activitate supusă acordului local | condițional |
| `local_agreement_current` | `boolean` | acordul local este valabil și actual | condițional |

## Pași determinați

| step_id | rezultat | gate principal |
|---|---|---|
| `file_pfa_resume_mention` | reluare PFA la ONRC | suspendare existentă și în termen |
| `approve_srl_resume` | hotărâre SRL | stare și durată |
| `file_srl_resume_mention` | mențiune SRL | termen și semnatar |
| `update_and_authorize_activities` | actualizare activități | coduri nevalide |
| `obtain_or_modify_timisoara_agreement` | acord local | activitate comercială locală |

## Reguli-cheie verificate

- Reluarea PFA se înregistrează la registrul comerțului.
- Perioada de suspendare nu poate depăși trei ani.
- ONRC are procedură distinctă pentru reluarea persoanelor juridice.
- Activitățile neînregistrate/neautorizate trebuie rezolvate înainte de operare.

## Canal pilot Timișoara / Timiș

Pentru Timișoara se verifică starea acordului comercial; reluarea ONRC nu îl reactivează automat.

## Guvernanță

Motorul verifică întâi starea curentă din registru. După trei ani sau când sediul și activitățile nu mai sunt valabile, traseul este blocat până la clarificare.
