# Event Card — ro.life.driving_licence_lost_stolen (life.driving_licence_lost_stolen)

**Batch:** B01_DRIVING_LICENCE_LOST_STOLEN  
**Status:** research_inbox (neaprobat)  
**Pilot:** `ro.tm.timisoara`  
**Accessed_at:** 2026-06-25

## Declanșator

„Mi-am pierdut permisul / mi-a fost furat / este deteriorat.”

## Limita evenimentului

Acoperă duplicatul cu valabilitatea existentă. Dacă permisul este expirat sau utilizatorul cere o valabilitate nouă, declanșează traseul separat de reînnoire.

## Fapte cerute

| fact | tip | valori / semnificație | obligatoriu |
|---|---|---|---|
| `incident_type` | `enum` | `lost`, `stolen`, `damaged` | da |
| `current_licence_expired` | `boolean` | valabilitatea permisului anterior | da |
| `wants_new_validity` | `boolean` | se dorește extinderea valabilității | da |
| `medical_document_present` | `boolean` | document medical | da |
| `request_channel` | `enum` | `counter`, `email` | da |
| `pickup_in_person` | `boolean` | ridicare la ghișeu | condițional |
| `selected_spcrpciv_email_known` | `boolean` | e-mail oficial verificat | condițional |
| `payment_status` | `enum` | `paid_online`, `unpaid` | da |
| `applicant_has_cei` | `boolean` | titular CEI | da |
| `has_damaged_licence` | `boolean` | permis deteriorat prezent | condițional |

## Pași determinați

| step_id | rezultat | gate principal |
|---|---|---|
| `request_driving_licence_duplicate` | duplicat permis | incident eligibil, taxă, dosar |
| `send_duplicate_documents_to_selected_spcrpciv` | dosar transmis | e-mail oficial |
| `collect_duplicate_in_person` | duplicat ridicat | finalizare fizică |

## Reguli-cheie verificate

- Duplicatul este disponibil pentru pierdere, furt sau deteriorare la orice SPCRPCIV.
- Fluxul prin e-mail este parțial: ridicarea rămâne la ghișeu.
- Tariful publicat este 89 lei.
- Nu este introdusă obligația unui proces-verbal de furt fără sursă oficială explicită în dosarul curent.

## Canal pilot Timișoara / Timiș

SPCRPCIV Timiș, Str. Demetriade nr. 1; e-mailul publicat al serviciului poate fi folosit numai după verificarea actualității lui.

## Guvernanță

Motorul nu confundă duplicatul cu reînnoirea. Cerința unui raport de poliție pentru furt rămâne în gaps, nu este inventată.
