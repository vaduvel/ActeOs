---
event_id: ro.life.digital_identity_ro
title_ro: "Crearea identității digitale ROeID"
reference_date: 2026-06-25
timezone: Europe/Bucharest
status: research_candidate_not_production_published
jurisdiction:
  - eu
  - ro
  - ro.tm
  - ro.tm.timisoara
---

# Crearea identității digitale ROeID

## Outcome

Utilizatorul finalizează înrolarea în aplicația oficială și poate autentifica accesul la serviciile publice compatibile.

## Scope and truth guard

ROeID este un serviciu național; sursele oficiale publică însă două durate incompatibile pentru validare, păstrate explicit ca conflict.

> Acest card este candidat de research. Nicio regulă nu devine activă în producție înainte de captură imutabilă a sursei, review uman și aprobare explicită.

## Facts

| id | type | întrebare | motiv | sensibil | obligatoriu |
|---|---|---|---|---:|---:|
| `romanian_citizen` | `boolean` | Ești cetățean român? | Termenii ROeID definesc utilizatorul persoană fizică prin cetățenia română. | true | true |
| `smartphone_os` | `enum` | Ce telefon folosești? | Aplicația este publicată pentru Android și iPhone. | false | true |
| `internet_available` | `boolean` | Ai conexiune la internet? | Este necesară înrolării și autentificării. | false | true |
| `identity_document_available` | `boolean` | Ai cartea de identitate la îndemână? | Este fotografiată și prezentată în proces. | false | true |
| `identity_document_valid` | `boolean` | Cartea de identitate este valabilă și lizibilă? | Un document neclar sau nevalabil poate bloca validarea. | false | true |
| `camera_available` | `boolean` | Camera telefonului funcționează? | Sunt necesare selfie și filmări. | false | true |
| `microphone_available` | `boolean` | Microfonul telefonului funcționează? | Fluxul include înregistrare audio-video. | false | true |
| `email_available` | `boolean` | Ai acces la o adresă de e-mail? | Confirmarea validării este transmisă pe e-mail. | false | true |
| `enrollment_submitted` | `boolean` | Ai trimis deja solicitarea? | Determină dacă urmează capturile sau așteptarea validării. | false | false |
| `enrollment_rejected` | `boolean` | Solicitarea a fost respinsă? | Activează instrucțiunile de refacere a capturilor. | false | false |
| `needs_exact_completion_deadline` | `boolean` | Ai nevoie de o dată garantată de activare? | Sursele oficiale publică termene incompatibile. | false | false |

## Gates

| prioritate | id | când | efect | cod | mesaj | claims |
|---:|---|---|---|---|---|---|
| 100 | `gate.not_romanian` | romanian_citizen == false | `needs_confirmation` | `ROEID_CITIZENSHIP_SCOPE` | Termenii cercetați definesc utilizatorul persoană fizică drept cetățean român. | `claim.digital_identity_ro.roeid_romanian_user` |
| 95 | `gate.no_supported_phone` | smartphone_os in [other,none] | `block` | `SUPPORTED_SMARTPHONE_REQUIRED` | Înrolarea ROeID necesită aplicația pe Android sau iPhone. | `claim.digital_identity_ro.roeid_phone_and_id`, `claim.digital_identity_ro.roeid_smartphone_internet` |
| 90 | `gate.no_id` | identity_document_available == false or identity_document_valid == false | `block` | `IDENTITY_DOCUMENT_REQUIRED` | Nu poți finaliza înrolarea fără cartea de identitate disponibilă și lizibilă. | `claim.digital_identity_ro.roeid_phone_and_id`, `claim.digital_identity_ro.roeid_rejected_capture_recovery` |
| 85 | `gate.no_capture_tools` | camera_available == false or microphone_available == false or internet_available == false | `block` | `ROEID_CAPTURE_NOT_READY` | Camera, microfonul și internetul sunt necesare capturilor ROeID. | `claim.digital_identity_ro.roeid_capture_requirements`, `claim.digital_identity_ro.roeid_smartphone_internet` |
| 80 | `gate.timeline_conflict` | enrollment_submitted == true | `warn` | `ROEID_APPROVAL_TIME_CONFLICT` | Sursele oficiale ROeID indică atât maximum 24 de ore, cât și 24–72 de ore lucrătoare. | `claim.digital_identity_ro.roeid_duration_24_72`, `claim.digital_identity_ro.roeid_duration_max_24` |
| 70 | `gate.rejected` | enrollment_rejected == true | `warn` | `ROEID_CAPTURE_REJECTED` | Refă imaginile și filmarea cu lumină bună, fără reflexii și cu actul original. | `claim.digital_identity_ro.roeid_rejected_capture_recovery` |

## Steps

### 1. Verifică dispozitivul și actul

- **Ce faci:** Pregătește un smartphone Android/iPhone, internet și cartea de identitate.
- **Până când:** `none`
- **Cum știi că e gata:** Telefonul, conexiunea, camera, microfonul și actul sunt disponibile.
- **Dacă eșuează:** Schimbă dispozitivul sau reînnoiește actul înainte de înrolare.
- **Canale:** `channel.roeid_citizens`
- **Claims:** `claim.digital_identity_ro.roeid_phone_and_id`, `claim.digital_identity_ro.roeid_smartphone_internet`

### 2. Instalează aplicația oficială ROeID

- **Ce faci:** Accesează magazinele oficiale prin pagina ROeID și deschide procesul de creare a contului.
- **Până când:** `none`
- **Cum știi că e gata:** Aplicația oficială este instalată și procesul de înrolare este deschis.
- **Dacă eșuează:** Nu instala aplicații din linkuri neoficiale.
- **Canale:** `channel.roeid_citizens`
- **Claims:** `claim.digital_identity_ro.roeid_purpose`, `claim.digital_identity_ro.roeid_smartphone_internet`

### 3. Parcurge cele cinci etape de captură

- **Ce faci:** Introdu datele, fotografiază actul, fă selfie-ul și înregistrările video/audio cerute.
- **Până când:** `none`
- **Cum știi că e gata:** Aplicația confirmă trimiterea solicitării de validare.
- **Dacă eșuează:** Refă capturile în lumină bună, cu actul original și fără reflexii.
- **Canale:** `channel.roeid_citizens`
- **Claims:** `claim.digital_identity_ro.roeid_five_steps`, `claim.digital_identity_ro.roeid_capture_requirements`, `claim.digital_identity_ro.roeid_rejected_capture_recovery`

### 4. Urmărește validarea

- **Ce faci:** Așteaptă e-mailul și notificarea din aplicație; nu trata intervalul publicat ca termen garantat.
- **Până când:** `none`
- **Cum știi că e gata:** Ai primit aprobarea sau un motiv de respingere.
- **Dacă eșuează:** Dacă nu primești rezultat, folosește suportul oficial ROeID.
- **Canale:** `channel.roeid_terms`, `channel.roeid_support`
- **Claims:** `claim.digital_identity_ro.roeid_duration_24_72`, `claim.digital_identity_ro.roeid_duration_max_24`

### 5. Folosește autentificarea ROeID

- **Ce faci:** Pe serviciile compatibile, selectează butonul «Autentifică-te cu ROeID» și aprobă cererea în aplicație.
- **Până când:** `none`
- **Cum știi că e gata:** Serviciul public confirmă autentificarea.
- **Dacă eșuează:** Verifică permisiunea de notificări și disponibilitatea ROeID pe platforma țintă.
- **Canale:** `channel.roeid_citizens`
- **Claims:** `claim.digital_identity_ro.roeid_purpose`

## Requirements

| id | titlu | obligație | timing | forme | verificări | claims |
|---|---|---|---|---|---|---|
| `req.smartphone` | Smartphone compatibil | `mandatory` | `now` | electronic | user_confirmed | `claim.digital_identity_ro.roeid_phone_and_id`, `claim.digital_identity_ro.roeid_smartphone_internet` |
| `req.identity_card` | Cartea de identitate | `mandatory` | `now` | original | exists, readable, correct_document_type, not_expired, names_consistent | `claim.digital_identity_ro.roeid_phone_and_id`, `claim.digital_identity_ro.roeid_rejected_capture_recovery` |
| `req.camera_microphone_internet` | Cameră, microfon și internet | `mandatory` | `now` | electronic | user_confirmed | `claim.digital_identity_ro.roeid_capture_requirements`, `claim.digital_identity_ro.roeid_smartphone_internet` |
| `req.email` | Adresă de e-mail accesibilă | `mandatory` | `now` | electronic | exists, user_confirmed | `claim.digital_identity_ro.roeid_duration_max_24` |

## Official channels

| id | tip | etichetă | URL | integrare | teritoriu |
|---|---|---|---|---|---|
| `channel.roeid_citizens` | `web` | ROeID — cetățeni | https://www.roeid.ro/cetateni | `DEEP_LINK` | ro |
| `channel.roeid_terms` | `web` | ROeID — termeni | https://www.roeid.ro/termeni | `SOURCE_ONLY` | ro |
| `channel.roeid_support` | `web` | ROeID — ajutor și contact | https://www.roeid.ro/contact | `DEEP_LINK` | ro |

## Source claims

| claim_id | afirmație | sursă | confidence | locator |
|---|---|---|---|---|
| `claim.digital_identity_ro.roeid_purpose` | ROeID permite accesarea serviciilor digitale ale instituțiilor publice unde este disponibil butonul de autentificare ROeID. | `roeid_citizens` | `verified` | Pagina «Cetățeni», introducere |
| `claim.digital_identity_ro.roeid_five_steps` | Activarea ROeID este prezentată în cinci pași de captură și validare. | `roeid_citizens` | `verified` | Pagina «Cetățeni», secțiunea de activare |
| `claim.digital_identity_ro.roeid_phone_and_id` | Pentru activare sunt necesare un smartphone Android/iPhone și cartea de identitate. | `roeid_citizens` | `verified` | Pagina «Cetățeni», FAQ «Ce este necesar» |
| `claim.digital_identity_ro.roeid_capture_requirements` | Fluxul cere fotografia cărții de identitate, selfie și înregistrări video/audio conform instrucțiunilor aplicației. | `roeid_citizens` | `verified` | Pagina «Cetățeni», FAQ și pașii 1-5 |
| `claim.digital_identity_ro.roeid_duration_24_72` | Pagina pentru cetățeni indică o durată obișnuită de aprobare între 24 și 72 de ore lucrătoare, cu posibile decalări. | `roeid_citizens` | `conflicting` | Pagina «Cetățeni», FAQ «Cât durează tot procesul?» |
| `claim.digital_identity_ro.roeid_duration_max_24` | Termenii ROeID indică o durată maximă de 24 de ore pentru validarea solicitării. | `roeid_terms` | `conflicting` | Termeni, secțiunea 5 «Validarea utilizatorului» |
| `claim.digital_identity_ro.roeid_smartphone_internet` | ROeID este accesibil prin smartphone iOS/Android cu conexiune la internet. | `roeid_terms` | `verified` | Termeni, secțiunea 3 «Cum accesezi ROeID?» |
| `claim.digital_identity_ro.roeid_romanian_user` | Termenii definesc utilizatorul persoană fizică drept cetățean român a cărui identitate a fost verificată și validată. | `roeid_terms` | `verified_with_local_gap` | Termeni, definiția «Utilizator» |
| `claim.digital_identity_ro.roeid_rejected_capture_recovery` | În cazul refuzului capturii, ROeID recomandă lumină bună, imagini clare, actul original și respectarea instrucțiunilor. | `roeid_citizens` | `verified` | Pagina «Cetățeni», FAQ «Nu reușesc, tot primesc mesaj de refuz» |

## Conflicts

| id | claim A | claim B | status | handling |
|---|---|---|---|---|
| `conflict.roeid.validation_duration` | `claim.digital_identity_ro.roeid_duration_24_72` | `claim.digital_identity_ro.roeid_duration_max_24` | `unresolved` | Nu se afișează termen garantat; utilizatorul urmărește notificarea oficială. |

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
