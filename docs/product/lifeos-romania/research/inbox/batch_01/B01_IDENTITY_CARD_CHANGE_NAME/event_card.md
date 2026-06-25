# Event Card — ro.life.identity_card_change_name (life.identity_card_change_name)

**Batch:** B01_IDENTITY_CARD_CHANGE_NAME  
**Status:** research_inbox (neaprobat)  
**Pilot:** `ro.tm.timisoara`  
**Accessed_at:** 2026-06-25

## Declanșator

„Mi-am schimbat numele după căsătorie, divorț, procedură administrativă sau hotărâre.”

## Limita evenimentului

Acoperă emiterea actului de identitate după ce schimbarea numelui este deja opozabilă și înscrisă în documentele de stare civilă aplicabile.

## Fapte cerute

| fact | tip | valori / semnificație | obligatoriu |
|---|---|---|---|
| `change_date` | `date` | data producerii/înscrierii schimbării | da |
| `request_date` | `date` | data cererii | da |
| `change_basis` | `enum` | `marriage`, `divorce`, `administrative`, `court`, `foreign` | da |
| `requested_document` | `enum` | `cei`, `cis` | da |
| `applicant_present` | `boolean` | titular prezent | da |
| `has_old_id` | `boolean` | actul anterior | da |
| `has_updated_civil_certificate` | `boolean` | certificat cu numele actual | da |
| `has_admin_or_court_act` | `boolean` | act definitiv | condițional |
| `foreign_change_registered_in_ro` | `boolean` | mențiune/transcriere română | condițional |
| `domicile_changed` | `boolean` | schimbare simultană de domiciliu | da |

## Pași determinați

| step_id | rezultat | gate principal |
|---|---|---|
| `replace_identity_card_after_name_change` | act cu numele actual | termen, document final, prezență |

## Reguli-cheie verificate

- Termenul legal este 15 zile de la modificarea numelui.
- Documentul care dovedește numele actual depinde de căsătorie, divorț, act administrativ sau hotărâre.
- Schimbările produse în străinătate trebuie întâi reflectate în registrele române.
- Actul anterior și dovada domiciliului fac parte din dosarul general.

## Canal pilot Timișoara / Timiș

DEP Timișoara, Bulevardul Mihai Eminescu nr. 15; programarea CEI se face prin canalul HUB.

## Guvernanță

Data `change_date` trebuie să fie data juridic relevantă din document, nu data la care utilizatorul a decis informal să folosească alt nume.
