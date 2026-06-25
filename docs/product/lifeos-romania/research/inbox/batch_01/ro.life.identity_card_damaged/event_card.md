# Event Card — ro.life.identity_card_damaged (life.identity_card_damaged)

**Batch:** B01_IDENTITY_CARD_DAMAGED  
**Status:** research_inbox (neaprobat)  
**Pilot:** `ro.tm.timisoara`  
**Accessed_at:** 2026-06-25

## Declanșator

„Cartea mea de identitate este deteriorată și trebuie înlocuită.”

## Limita evenimentului

Acoperă deteriorarea fizică/funcțională. Dacă actul nu mai este în posesia titularului, cazul se recalcifică drept pierdere/furt, nu deteriorare.

## Fapte cerute

| fact | tip | valori / semnificație | obligatoriu |
|---|---|---|---|
| `incident_date` | `date` | data deteriorării | da |
| `request_date` | `date` | data cererii | da |
| `requested_document` | `enum` | `cei`, `cis` | da |
| `applicant_present` | `boolean` | titular prezent | da |
| `has_damaged_id` | `boolean` | actul deteriorat este prezent | da |
| `rnep_has_face_image` | `boolean` | imagine disponibilă în RNEP | da |
| `has_alt_photo_id` | `boolean` | pașaport/permis recent | condițional |
| `civil_status_changed` | `boolean` | date de stare civilă schimbate | da |
| `domicile_changed` | `boolean` | domiciliu schimbat | da |

## Pași determinați

| step_id | rezultat | gate principal |
|---|---|---|
| `replace_damaged_identity_card` | act nou | termen, prezență, identificare, dosar |
| `police_identity_verification` | identitate confirmată | fără imagine/document foto |

## Reguli-cheie verificate

- Cererea are termen de 15 zile de la deteriorare.
- Actul deteriorat se prezintă în dosar.
- Fără imagine în RNEP este necesar un document oficial recent cu fotografie; în lipsa lui se fac verificări.
- CEI și CIS au canale și taxe diferite.

## Canal pilot Timișoara / Timiș

DEP Timișoara, Bulevardul Mihai Eminescu nr. 15; disponibilitatea programărilor HUB este dinamică.

## Guvernanță

Motorul nu transformă automat lipsa actului deteriorat în pierdere; solicită clarificarea incidentului.
