# Event Card — ro.life.identity_card_first (life.identity_card_first)

**Batch:** B01_IDENTITY_CARD_FIRST  
**Status:** research_inbox (neaprobat)  
**Pilot:** `ro.tm.timisoara`  
**Accessed_at:** 2026-06-25

## Declanșator

„Am împlinit 14 ani / vreau primul act de identitate pentru copil.”

## Limita evenimentului

Acoperă prima emitere a CEI/CIS. Nu acoperă expirarea, pierderea, furtul, deteriorarea ori schimbarea datelor unui act deja emis.

## Fapte cerute

| fact | tip | valori / semnificație | obligatoriu |
|---|---|---|---|
| `age_years` | `integer` | vârsta la data cererii | da |
| `turned_14_at` | `date` | data împlinirii a 14 ani | condițional |
| `request_date` | `date` | data depunerii | da |
| `requested_document` | `enum` | `cei`, `cis` | da |
| `is_first_cei` | `boolean` | prima CEI sau emitere ulterioară | condițional |
| `applicant_present` | `boolean` | titular prezent la ghișeu | da |
| `parent_situation` | `enum` | `both_parents`, `one_parent_present`, `one_with_authenticated_consent`, `one_without_consent`, `legal_representative` | condițional |
| `parents_status` | `enum` | `married`, `divorced`, `other` | condițional |

## Pași determinați

| step_id | rezultat | gate principal |
|---|---|---|
| `request_first_identity_card` | depunere prim act | vârstă, termen, prezență, acte |
| `request_optional_cei_for_child` | CEI opțională sub 14 ani | persoană autorizată + acord/hotărâre |

## Reguli-cheie verificate

- Primul act devine obligatoriu de la 14 ani și cererea are termen legal de 15 zile.
- CIS este blocată sub 14 ani; CEI este opțională.
- Depunerea CEI/CIS necesită prezența titularului.
- Regula de gratuitate a primei CEI este limitată temporal la 30 iunie 2026.

## Canal pilot Timișoara / Timiș

DEP Timișoara: Bulevardul Mihai Eminescu nr. 15. Pentru CEI se folosește programarea HUB; disponibilitatea sloturilor este dinamică și nu este codificată.

## Guvernanță

Taxa după 30.06.2026 este intenționat `needs_confirmation`; motorul nu extrapolează gratuitatea după expirarea ferestrei oficiale.
