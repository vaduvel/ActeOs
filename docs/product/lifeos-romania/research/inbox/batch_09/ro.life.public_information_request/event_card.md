# Event Card — ro.life.public_information_request (life.public_information_request)

**Titlu:** Vreau să cer informații de interes public  
**Batch:** B09_PUBLIC_INFORMATION_REQUEST  
**Status:** `research_inbox` — neaprobat; nu se publică în producție înainte de review independent  
**Pilot jurisdicție:** `ro.tm.timisoara`  
**Accessed_at:** `2026-06-25`

## Declanșator

Utilizatorul cere unei autorități informații care privesc activitatea sau rezultă din activitatea acesteia, în regimul Legii 544/2001.

## Fapte cerute (typed facts)

| fact | tip | valori / sens |
|---|---|---|
| `target_authority` | string | autoritatea destinatară |
| `request_is_public_information` | boolean | clasificare 544 |
| `submission_mode` | enum | written/electronic/verbal |
| `identifiable_information_description` | string | descriere suficientă |
| `requester_name` | string | nume și prenume |
| `requester_signature_present` | boolean | cerință scrisă |
| `response_address` | string | adresă răspuns |
| `request_registered` | boolean | ancoră termen |
| `registration_date` | date | data înregistrării |
| `extension_notice_received_within_10_days` | boolean | ramura 30 zile |
| `authority_refuses` | boolean | ramura refuz |
| `requests_document_copies` | boolean | cost copiere |
| `may_contain_exempt_information` | boolean | art. 12 |
| `wants_administrative_complaint` | boolean | contestație internă |
| `wants_court_complaint` | boolean | contencios |

## Obligații și ramuri

| step_id | condiție | efect determinist | dovezi |
|---|---|---|---|
| `classify_request_as_public_information` | întotdeauna | separă 544 de petiții/servicii | `claim.info.not_petition_or_service` |
| `prepare_written_information_request` | cerere scrisă | completează elementele legale | `claim.info.written_fields` |
| `receive_standard_response` | cerere înregistrată | urmărește termenul 10/30 zile | `claim.info.deadline_10_30` |
| `submit_administrative_complaint_to_authority_head` | refuz | reclamație în 30 zile | `claim.info.admin_complaint` |
| `submit_court_complaint` | vătămare și termen expirat | plângere la tribunal | `claim.info.court_complaint` |

## Canale oficiale

| arie | canal | stare |
|---|---|---|
| național | compartiment/persoană desemnată de autoritate | `verified` |
| Timișoara | Pagina PMT Legea 544 și modele | `verified_with_local_gap` |

## Note de guvernanță

- Regimul 544 nu este folosit pentru aprobări, autorizații sau servicii.
- Termenul de 30 zile cere notificarea în primele 10 zile.
- Costul modelat privește copierea, nu o taxă generică de depunere.

===
