# Event Card — ro.life.driving_licence_expired (life.driving_licence_expired)

**Batch:** B01_DRIVING_LICENCE_EXPIRED  
**Status:** research_inbox (neaprobat)  
**Pilot:** `ro.tm.timisoara`  
**Accessed_at:** 2026-06-25

## Declanșator

„Permisul meu a expirat sau vreau să îl preschimb cu o valabilitate nouă.”

## Limita evenimentului

Acoperă serviciul DGPCI de emitere cu valabilitate nouă. Pierderea/furtul cu păstrarea valabilității aparțin evenimentului de duplicat.

## Fapte cerute

| fact | tip | valori / semnificație | obligatoriu |
|---|---|---|---|
| `licence_expiry_date` | `date` | data expirării | da |
| `request_date` | `date` | data solicitării | da |
| `wants_new_validity` | `boolean` | se cere extinderea valabilității | da |
| `medical_document_present` | `boolean` | document medical aplicabil | da |
| `request_channel` | `enum` | `counter`, `email` | da |
| `applicant_route` | `enum` | `self`, `proxy` | condițional |
| `has_old_licence` | `boolean` | permisul anterior | da |
| `has_identity_document` | `boolean` | act de identitate valabil | da |
| `payment_status` | `enum` | `paid_online`, `unpaid` | da |
| `applicant_has_cei` | `boolean` | titular CEI | da |
| `address_certificate` | `boolean` | certificat adresă | condițional |

## Pași determinați

| step_id | rezultat | gate principal |
|---|---|---|
| `request_licence_new_validity` | permis cu valabilitate nouă | dosar, taxă, canal, condiții medicale |

## Reguli-cheie verificate

- Serviciul poate fi cerut în orice moment și la orice SPCRPCIV.
- Tariful publicat este 89 lei.
- Fluxul național pentru nouă valabilitate nu acceptă documente prin e-mail.
- Lista exactă a dosarului rămâne blocată până la un snapshot stabil DGPCI; nu este reconstituită din memorie.

## Canal pilot Timișoara / Timiș

SPCRPCIV Timiș, Str. Demetriade nr. 1, Iulius Mall. Programul publicat este conflictual (19:00 vs 19:30 L-J), deci se cere reverificare.

## Guvernanță

Regula medicală este promovată numai pentru pilotul Timiș ca `verified_with_local_gap`; extinderea națională cere confirmare din Ordinul MAI 82/2024 sau pagina DGPCI stabilă.
