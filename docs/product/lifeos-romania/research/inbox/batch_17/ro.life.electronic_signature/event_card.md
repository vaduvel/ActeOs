---
event_id: ro.life.electronic_signature
title_ro: "Obținerea unei semnături electronice"
reference_date: 2026-06-25
timezone: Europe/Bucharest
status: research_candidate_not_production_published
jurisdiction:
  - eu
  - ro
  - ro.tm
  - ro.tm.timisoara
---

# Obținerea unei semnături electronice

## Outcome

Utilizatorul confirmă tipul necesar, alege un prestator calificat și finalizează emiterea/activarea certificatului.

## Scope and truth guard

Baza juridică este națională, dar prețul, identificarea, livrarea și înrolarea sunt proceduri ale prestatorului și ale platformei țintă.

> Acest card este candidat de research. Nicio regulă nu devine activă în producție înainte de captură imutabilă a sursei, review uman și aprobare explicită.

### Note de domeniu

- Semnătura calificată nu înlocuiește forma autentică atunci când aceasta este impusă de lege.
- Datele de emitere sunt candidate de research și necesită captură imutabilă înainte de producție.

## Facts

| id | type | întrebare | motiv | sensibil | obligatoriu |
|---|---|---|---|---:|---:|
| `signature_goal` | `enum` | Pentru ce ai nevoie de semnătură? | Forma cerută de act sau platformă determină tipul potrivit. | false | true |
| `requested_signature_type` | `enum` | Știi ce tip de semnătură ți se cere? | Nu toate semnăturile au automat efectul semnăturii olografe. | false | true |
| `provider_id` | `enum` | Ce prestator ai ales? | Documentele, tariful și livrarea sunt stabilite de prestator. | false | true |
| `delivery_mode` | `enum` | Vrei semnătură în cloud sau pe token? | Modul de livrare schimbă pașii și timpul orientativ. | false | true |
| `age_years` | `integer` | Ce vârstă ai? | Unii prestatori publică limite proprii pentru fluxul video. | true | true |
| `valid_identity_document` | `boolean` | Ai un act de identitate valabil? | Este necesar identificării titularului. | false | true |
| `payment_card_available` | `boolean` | Ai un card pentru plata online? | Este cerut în fluxurile online cercetate. | false | true |
| `camera_microphone_available` | `boolean` | Ai cameră și microfon funcționale? | Sunt necesare identificării video. | false | true |
| `internet_available` | `boolean` | Ai o conexiune stabilă la internet? | Este necesară identificării și activării. | false | true |
| `target_requires_authentic_form` | `boolean` | Actul trebuie autentificat de notar sau altă autoritate? | Semnătura calificată nu înlocuiește autentificarea impusă de lege. | false | false |
| `target_platform_known` | `boolean` | Știi platforma în care vei folosi certificatul? | Unele platforme cer o înrolare separată după emitere. | false | false |

## Gates

| prioritate | id | când | efect | cod | mesaj | claims |
|---:|---|---|---|---|---|---|
| 100 | `gate.authentic_form` | target_requires_authentic_form == true | `warn` | `AUTHENTIC_FORM_NOT_REPLACED` | Semnătura electronică nu înlocuiește autentificarea cerută expres de lege. | `claim.electronic_signature.authentic_form_exception` |
| 95 | `gate.signature_type_unknown` | requested_signature_type == unknown | `needs_confirmation` | `SIGNATURE_TYPE_UNCONFIRMED` | Nu cumpăra un certificat până nu confirmi tipul acceptat de destinatar. | `claim.electronic_signature.all_signatures_have_legal_effect`, `claim.electronic_signature.qualified_equals_handwritten` |
| 90 | `gate.invalid_id` | valid_identity_document == false | `block` | `VALID_ID_REQUIRED` | Fluxurile de emitere cercetate necesită un document de identitate valabil. | `claim.electronic_signature.certsign_video_requirements`, `claim.electronic_signature.digisign_identity_prerequisites` |
| 80 | `gate.video_tools_missing` | camera_microphone_available == false or internet_available == false | `block` | `VIDEO_IDENTIFICATION_NOT_READY` | Identificarea video nu poate fi finalizată fără cameră, microfon și internet. | `claim.electronic_signature.certsign_video_requirements`, `claim.electronic_signature.digisign_identity_prerequisites` |
| 75 | `gate.digisign_under_18` | provider_id == digisign and age_years < 18 | `needs_confirmation` | `DIGISIGN_VIDEO_AGE_LIMIT` | Fluxul DigiSign cercetat indică vârsta minimă de 18 ani. | `claim.electronic_signature.digisign_identity_prerequisites` |
| 70 | `gate.provider_unknown` | provider_id == unknown | `needs_confirmation` | `TRUSTED_PROVIDER_REQUIRED` | Prestatorul și statutul calificat trebuie verificate înainte de achiziție. | `claim.electronic_signature.eu_qualified_trusted_list` |

## Steps

### 1. Confirmă tipul de semnătură acceptat

- **Ce faci:** Verifică dacă destinatarul cere semnătură calificată, avansată sau acceptă alt tip.
- **Până când:** `none`
- **Cum știi că e gata:** Ai o cerință oficială sau contractuală clară privind tipul acceptat.
- **Dacă eșuează:** Solicită confirmare scrisă destinatarului.
- **Canale:** `channel.adr_trusted_list`
- **Claims:** `claim.electronic_signature.all_signatures_have_legal_effect`, `claim.electronic_signature.qualified_equals_handwritten`, `claim.electronic_signature.authentic_form_exception`

### 2. Alege un prestator calificat

- **Ce faci:** Verifică prestatorul și serviciul în Trusted List înainte de plată.
- **Până când:** `none`
- **Cum știi că e gata:** Prestatorul și serviciul ales apar ca fiind calificate în lista oficială.
- **Dacă eșuează:** Nu continua pe un site neconfirmat; revino la Trusted List.
- **Canale:** `channel.adr_trusted_list`, `channel.certsign`, `channel.digisign`
- **Claims:** `claim.electronic_signature.eu_qualified_trusted_list`

### 3. Completează comanda și identificarea

- **Ce faci:** Furnizează datele cerute, plătește prin canalul oficial și finalizează identificarea video.
- **Până când:** `none`
- **Cum știi că e gata:** Ai confirmarea trimiterii și rezultatul validării identității.
- **Dacă eșuează:** Refă identificarea în condiții bune de lumină sau contactează suportul prestatorului.
- **Canale:** `channel.certsign`, `channel.digisign`
- **Claims:** `claim.electronic_signature.certsign_video_requirements`, `claim.electronic_signature.certsign_validation_24h`, `claim.electronic_signature.digisign_identity_prerequisites`

### 4. Primește și activează certificatul

- **Ce faci:** Urmează instrucțiunile pentru cloud sau token și păstrează în siguranță credențialele/PIN-ul.
- **Până când:** `none`
- **Cum știi că e gata:** Poți aplica și valida o semnătură de test.
- **Dacă eșuează:** Folosește suportul oficial al prestatorului pentru activare.
- **Canale:** `channel.certsign`, `channel.digisign`
- **Claims:** `claim.electronic_signature.certsign_delivery_estimates`, `claim.electronic_signature.digisign_issue_window`

### 5. Înrolează certificatul unde este necesar

- **Ce faci:** Dacă platforma țintă cere înrolare separată, urmează procedura ei oficială.
- **Până când:** `none`
- **Cum știi că e gata:** Platforma țintă confirmă certificatul sau acceptă documentul semnat.
- **Dacă eșuează:** Verifică ghidul oficial al platformei țintă.
- **Canale:** `channel.adr_trusted_list`
- **Claims:** `claim.electronic_signature.qualified_equals_handwritten`

## Requirements

| id | titlu | obligație | timing | forme | verificări | claims |
|---|---|---|---|---|---|---|
| `req.valid_id` | Document de identitate valabil | `mandatory` | `now` | original | exists, readable, correct_document_type, not_expired, names_consistent | `claim.electronic_signature.certsign_video_requirements`, `claim.electronic_signature.digisign_identity_prerequisites` |
| `req.payment_method` | Metodă de plată online | `mandatory` | `now` | electronic | user_confirmed | `claim.electronic_signature.certsign_video_requirements`, `claim.electronic_signature.digisign_identity_prerequisites` |
| `req.video_device` | Dispozitiv pentru identificare video | `mandatory` | `now` | electronic | user_confirmed | `claim.electronic_signature.certsign_video_requirements`, `claim.electronic_signature.digisign_identity_prerequisites` |
| `req.recipient_requirement` | Cerința destinatarului | `mandatory` | `now` | electronic, copy, declaration | exists, readable, field_present, user_confirmed | `claim.electronic_signature.all_signatures_have_legal_effect`, `claim.electronic_signature.qualified_equals_handwritten`, `claim.electronic_signature.authentic_form_exception` |

## Official channels

| id | tip | etichetă | URL | integrare | teritoriu |
|---|---|---|---|---|---|
| `channel.adr_trusted_list` | `web` | ADR — Trusted List | https://www.adr.gov.ro/semnatura-electronica-trusted-list | `DEEP_LINK` | ro |
| `channel.certsign` | `web` | certSIGN — achiziție și identificare | https://www.certsign.ro/ro/intrebari-despre-semnatura-electronica-calificata/ | `DEEP_LINK` | ro |
| `channel.digisign` | `web` | DigiSign — identificare video | https://digisign.ro/video/portal-identificare-video-fara-operator/ | `DEEP_LINK` | ro |

## Source claims

| claim_id | afirmație | sursă | confidence | locator |
|---|---|---|---|---|
| `claim.electronic_signature.all_signatures_have_legal_effect` | Toate tipurile de semnătură electronică produc efecte juridice și pot fi folosite ca mijloace de probă. | `law_214_2024` | `verified` | Art. 3 alin. (1); forma consolidată accesată la 25.06.2026 |
| `claim.electronic_signature.qualified_equals_handwritten` | Semnătura electronică calificată produce aceleași efecte juridice ca semnătura olografă. | `law_214_2024` | `verified` | Art. 4 alin. (1); forma consolidată accesată la 25.06.2026 |
| `claim.electronic_signature.authentic_form_exception` | Dacă legea cere înscris autentic, semnătura electronică nu înlocuiește autentificarea prevăzută de lege. | `law_214_2024` | `verified` | Art. 4 alin. (11); forma consolidată accesată la 25.06.2026 |
| `claim.electronic_signature.eu_qualified_trusted_list` | Certificatele calificate emise de prestatori calificați înscriși în Trusted List UE sunt valabile în toate statele membre, inclusiv România. | `adr_trusted_list` | `verified` | Secțiunea Trusted List; paragraful privind recunoașterea în UE |
| `claim.electronic_signature.certsign_video_requirements` | Pentru identificarea video certSIGN sunt necesare un act valabil, card pentru plată, dispozitiv cu cameră și internet. | `certsign_qes` | `verified` | FAQ, întrebarea 2 «Ce elemente sunt necesare» |
| `claim.electronic_signature.certsign_validation_24h` | certSIGN indică validarea sau respingerea identificării video în 24 de ore. | `certsign_qes` | `verified` | FAQ, întrebarea 4 |
| `claim.electronic_signature.certsign_delivery_estimates` | certSIGN publică termene orientative diferite pentru token și cloud după validarea identificării. | `certsign_qes` | `verified_with_local_gap` | FAQ, întrebarea 5 |
| `claim.electronic_signature.digisign_identity_prerequisites` | Fluxul DigiSign de identificare video publică cerințe proprii de identitate, vârstă, dispozitiv și plată. | `digisign_qes` | `verified_with_local_gap` | Pagina oficială «Identificare Video»; condiții de utilizare |
| `claim.electronic_signature.digisign_issue_window` | DigiSign indică un termen maxim operațional după identificarea video pentru emiterea certificatului. | `digisign_qes` | `verified_with_local_gap` | Pagina oficială «Identificare Video»; secțiunea privind emiterea |

## Freshness

critical:
  review_due_at: '2026-07-25'
  hard_expiry_at: '2026-09-23'
  on_expiry: needs_confirmation
operational:
  review_due_at: '2026-08-24'
  hard_expiry_at: '2026-12-22'
  on_expiry: warn
normative:
  review_due_at: '2026-12-22'
  hard_expiry_at: '2027-06-25'
  on_expiry: needs_confirmation
