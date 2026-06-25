# Event Card — ro.life.identity_theft_suspected (life.identity_theft_suspected)

**Batch:** B01_IDENTITY_THEFT_SUSPECTED  
**Status:** research_inbox (neaprobat)  
**Pilot:** `ro.tm.timisoara`  
**Accessed_at:** 2026-06-25

## Declanșator

„Cred că cineva mi-a folosit datele sau documentele pentru a se da drept mine.”

## Limita evenimentului

Este un router de protecție și raportare, nu un verdict penal și nu promite anularea automată a CNP-ului, a creditelor ori a contractelor.

## Fapte cerute

| fact | tip | valori / semnificație | obligatoriu |
|---|---|---|---|
| `urgent_danger` | `boolean` | pericol imediat/faptă în desfășurare | da |
| `physical_id_missing` | `boolean` | CI fizică lipsește | da |
| `passport_missing` | `boolean` | pașaportul lipsește | da |
| `unauthorized_transaction` | `boolean` | tranzacție neautorizată | da |
| `account_created_in_name` | `boolean` | cont/contract creat în numele persoanei | da |
| `document_used_by_other` | `boolean` | utilizare confirmată a documentului | da |
| `known_controller` | `boolean` | operatorul de date este cunoscut | da |
| `controller_contacted` | `boolean` | operator contactat | condițional |
| `controller_response` | `enum` | `pending_under_one_month`, `none_after_one_month`, `unsatisfactory`, `satisfactory` | condițional |
| `evidence_available` | `boolean` | există dovezi | da |
| `complaint_channel` | `enum` | `paper`, `electronic`, `oral`, `petition_portal` | da |
| `has_qualified_esignature` | `boolean` | semnătură electronică aplicabilă | condițional |
| `only_id_copy_leaked` | `boolean` | doar copia a fost expusă | da |

## Pași determinați

| step_id | rezultat | gate principal |
|---|---|---|
| `preserve_identity_theft_evidence` | dovezi păstrate | mesaje, extrase, contracte, loguri |
| `file_criminal_complaint` | sesizare penală formală | fapte indicând posibilă infracțiune |
| `contact_personal_data_controller` | cerere către operator | operator cunoscut |
| `file_anspdcp_complaint` | plângere ANSPDCP | contact prealabil + termen/răspuns |

## Reguli-cheie verificate

- Urgențele nu se trimit prin formularul de petiții; se apelează 112.
- Plângerea penală trebuie să descrie faptele și probele cunoscute; făptuitorul nu trebuie inventat.
- Plângerea electronică are cerință de semnătură; cea orală se consemnează.
- Pentru ANSPDCP se păstrează dovada contactării prealabile a operatorului.

## Canal pilot Timișoara / Timiș

Competența concretă a organului de cercetare nu este ghicită; aplicația conduce către Poliția Română/Parchet și către canalul ANSPDCP, după tipul faptei.

## Guvernanță

Aplicația nu afișează «schimbă-ți CNP-ul» și nu etichetează o persoană drept autor. Separă suspiciunea, incidentul de date și fapta penală confirmată.
