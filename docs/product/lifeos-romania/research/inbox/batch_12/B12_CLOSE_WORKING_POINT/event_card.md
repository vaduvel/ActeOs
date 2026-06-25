# Event Card — ro.life.close_working_point (life.close_working_point)

**Batch:** B12_CLOSE_WORKING_POINT  
**Status:** research_inbox (neaprobat)  
**Pilot:** `ro.tm.timisoara`  
**Accessed_at:** 2026-06-25

## Declanșator

„Vreau să închid un punct de lucru.”

## Limita evenimentului

Acoperă desființarea unui punct de lucru/sediu secundar pentru PFA sau SRL. Nu radiază întreaga afacere și nu confundă punctul de lucru cu o sucursală.

## Fapte cerute

| fact | tip | valori / semnificație | obligatoriu |
|---|---|---|---|
| `entity_type` | `enum` | pfa sau srl | da |
| `working_point_identifier` | `string` | locația exactă din registru | da |
| `location_type` | `enum` | working_point sau branch | da |
| `decision_date` | `date` | data deciziei SRL | condițional |
| `constitutive_act_is_modified` | `boolean` | operațiunea modifică actul constitutiv | condițional |
| `filing_actor` | `enum` | titular/reprezentant/mandatar/avocat | da |
| `filing_channel` | `enum` | counter, post_courier, online | da |
| `user_intends_whole_business_closure` | `boolean` | intenția reală este radierea afacerii | da |
| `local_commercial_agreement_exists` | `boolean` | există acord local pentru locație | condițional |

## Pași determinați

| step_id | rezultat | gate principal |
|---|---|---|
| `file_pfa_working_point_closure` | mențiune PFA | punct identificat |
| `approve_secondary_office_closure` | decizie internă SRL | competența și actul constitutiv |
| `file_secondary_office_closure` | mențiune ONRC | termen și semnatar |
| `cancel_local_agreement_for_point` | anulare acord local | autorizația locației |

## Reguli-cheie verificate

- ONRC are procedură distinctă pentru desființarea sediilor secundare.
- Când actul constitutiv este modificat, se depune și textul complet actualizat.
- Mențiunea se solicită în cel mult 15 zile de la act/fapt.
- Acordul comercial Timișoara se anulează separat.

## Canal pilot Timișoara / Timiș

Pentru Timișoara, motorul include anularea acordului numai dacă locația are efectiv un asemenea acord; documentele se confirmă în formularul local.

## Guvernanță

Clasificarea locației este gate critic. Dacă inputul descrie radierea firmei sau o sucursală, evenimentul se redirecționează și nu continuă cu traseul de punct de lucru.
