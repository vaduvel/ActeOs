---
event_id: ro.life.account_recovery_gov
title_ro: "Recuperarea accesului la conturi guvernamentale"
reference_date: 2026-06-25
timezone: Europe/Bucharest
status: research_candidate_not_production_published
jurisdiction:
  - eu
  - ro
  - ro.tm
  - ro.tm.timisoara
---

# Recuperarea accesului la conturi guvernamentale

## Outcome

Utilizatorul este direcționat către fluxul oficial corect pentru ROeID, Ghișeul.ro, SPV ANAF sau Hub MAI.

## Scope and truth guard

Este un bundle multi-platformă, nu o procedură unică. ActeOS nu colectează parole, coduri de resetare sau răspunsuri de securitate.

> Acest card este candidat de research. Nicio regulă nu devine activă în producție înainte de captură imutabilă a sursei, review uman și aprobare explicită.

### Note de domeniu

- Aplicația nu solicită și nu stochează parole, coduri OTP, coduri de resetare sau răspunsuri la întrebări de securitate.

## Facts

| id | type | întrebare | motiv | sensibil | obligatoriu |
|---|---|---|---|---:|---:|
| `platform_id` | `enum` | Pentru ce cont ai nevoie de recuperare? | Fiecare platformă are alt flux. | false | true |
| `issue_type` | `enum` | Ce problemă ai? | Determină dacă se resetează parola sau se reface înrolarea. | false | true |
| `current_password_known` | `boolean` | Mai știi parola actuală? | ROeID și ANAF au fluxuri diferite când parola este cunoscută. | true | false |
| `registered_email_access` | `boolean` | Mai ai acces la e-mailul asociat? | Ghișeul.ro și ANAF trimit recuperarea la adresa înregistrată. | true | false |
| `registered_phone_access` | `boolean` | Mai ai acces la telefonul validat? | Hub MAI poate trimite codul prin SMS. | true | false |
| `cnp_available` | `boolean` | Ai CNP-ul la îndemână? | Este folosit în fluxurile Ghișeul.ro și SPV. | true | false |
| `username_known` | `boolean` | Mai știi numele de utilizator? | Este necesar în anumite operațiuni ANAF. | true | false |
| `security_answer_known` | `boolean` | Știi răspunsul la întrebarea de siguranță? | Este cerut de pagina ANAF pentru schimbarea e-mailului. | true | false |
| `new_email_available` | `boolean` | Ai o adresă nouă de e-mail accesibilă? | Este necesară schimbării adresei. | true | false |
| `roeid_old_phone_available` | `boolean` | Mai ai vechiul telefon ROeID? | Schimbarea telefonului presupune o nouă înregistrare, indiferent de disponibilitatea vechiului telefon. | true | false |
| `reset_message_received` | `boolean` | Ai primit e-mailul/SMS-ul de resetare? | Dacă nu, se trece la suportul oficial. | false | false |

## Gates

| prioritate | id | când | efect | cod | mesaj | claims |
|---:|---|---|---|---|---|---|
| 100 | `gate.platform_unknown` | platform_id in [unknown,other] | `needs_confirmation` | `PLATFORM_RECOVERY_UNMAPPED` | Nu există un flux universal de recuperare pentru toate conturile guvernamentale. | `claim.account_recovery_gov.roeid_password_forgotten`, `claim.account_recovery_gov.ghiseul_credentials_recovery`, `claim.account_recovery_gov.anaf_recovery_inputs`, `claim.account_recovery_gov.hub_mai_reset_channels` |
| 95 | `gate.roeid_reenrol` | platform_id == roeid and issue_type in [forgot_password,change_email,changed_phone] | `warn` | `ROEID_REENROLMENT_REQUIRED` | Pentru această situație ROeID cere reluarea înrolării/validării. | `claim.account_recovery_gov.roeid_password_forgotten`, `claim.account_recovery_gov.roeid_email_change`, `claim.account_recovery_gov.roeid_phone_change` |
| 90 | `gate.ghiseul_no_email` | platform_id == ghiseul and registered_email_access == false | `needs_confirmation` | `GHISEUL_REGISTERED_EMAIL_UNAVAILABLE` | Fluxul automat trimite credențialele pe e-mailul asociat; fără acces este necesar suportul oficial. | `claim.account_recovery_gov.ghiseul_credentials_by_email`, `claim.account_recovery_gov.ghiseul_support_after_failure` |
| 85 | `gate.anaf_missing_inputs` | platform_id == anaf_spv and issue_type in [forgot_password,forgot_username] and (cnp_available == false or registered_email_access == false) | `needs_confirmation` | `ANAF_RECOVERY_INPUTS_MISSING` | Recuperarea automată SPV cere CNP și acces la e-mailul folosit la înregistrare. | `claim.account_recovery_gov.anaf_recovery_inputs` |
| 80 | `gate.anaf_change_email_missing` | platform_id == anaf_spv and issue_type == change_email and (username_known == false or current_password_known == false or security_answer_known == false or new_email_available == false) | `block` | `ANAF_EMAIL_CHANGE_INPUTS_MISSING` | Pagina de schimbare e-mail nu poate fi completată fără toate credențialele și răspunsul de siguranță. | `claim.account_recovery_gov.anaf_change_email_inputs` |
| 75 | `gate.hub_no_contact` | platform_id == hub_mai and registered_email_access == false and registered_phone_access == false | `needs_confirmation` | `HUB_MAI_VALIDATED_CONTACT_UNAVAILABLE` | Resetarea automată cere acces la e-mailul utilizat sau telefonul validat. | `claim.account_recovery_gov.hub_mai_validated_contact` |
| 70 | `gate.reset_not_received` | reset_message_received == false | `warn` | `RESET_MESSAGE_NOT_RECEIVED` | Verifică spamul și datele introduse; apoi folosește suportul oficial al platformei. | `claim.account_recovery_gov.ghiseul_support_after_failure`, `claim.account_recovery_gov.anaf_recovery_email_link`, `claim.account_recovery_gov.hub_mai_reset_channels` |

## Steps

### 1. Identifică platforma și problema

- **Ce faci:** Alege ROeID, Ghișeul.ro, SPV ANAF sau Hub MAI și descrie problema exactă.
- **Până când:** `none`
- **Cum știi că e gata:** Platforma și tipul problemei sunt selectate.
- **Dacă eșuează:** Verifică domeniul oficial înainte să introduci CNP sau credențiale.
- **Canale:** `channel.roeid_recovery`, `channel.ghiseul_recovery`, `channel.anaf_recovery`, `channel.hub_mai_reset`
- **Claims:** `claim.account_recovery_gov.roeid_password_forgotten`, `claim.account_recovery_gov.ghiseul_credentials_recovery`, `claim.account_recovery_gov.anaf_recovery_inputs`, `claim.account_recovery_gov.hub_mai_reset_channels`

### 2. Pregătește datele cerute de platformă

- **Ce faci:** Folosește numai datele asociate contului și canalul oficial.
- **Până când:** `none`
- **Cum știi că e gata:** Ai datele necesare fluxului ales, fără a le transmite aplicației ActeOS.
- **Dacă eșuează:** Dacă nu mai ai acces la e-mail/telefon, treci la suportul instituției.
- **Canale:** `channel.roeid_recovery`, `channel.ghiseul_recovery`, `channel.anaf_recovery`, `channel.hub_mai_reset`
- **Claims:** `claim.account_recovery_gov.ghiseul_credentials_recovery`, `claim.account_recovery_gov.anaf_recovery_inputs`, `claim.account_recovery_gov.anaf_change_email_inputs`, `claim.account_recovery_gov.hub_mai_validated_contact`

### 3. Rulează recuperarea pe pagina oficială

- **Ce faci:** Solicită resetarea, reînrolarea sau schimbarea e-mailului prin fluxul platformei.
- **Până când:** `none`
- **Cum știi că e gata:** Platforma confirmă trimiterea mesajului sau începerea reînrolării.
- **Dacă eșuează:** Dacă nu primești mesajul, verifică spam și apelează suportul oficial.
- **Canale:** `channel.roeid_recovery`, `channel.ghiseul_recovery`, `channel.anaf_recovery`, `channel.anaf_change_email`, `channel.hub_mai_reset`
- **Claims:** `claim.account_recovery_gov.roeid_password_known`, `claim.account_recovery_gov.roeid_password_forgotten`, `claim.account_recovery_gov.roeid_email_change`, `claim.account_recovery_gov.roeid_phone_change`, `claim.account_recovery_gov.ghiseul_credentials_by_email`, `claim.account_recovery_gov.anaf_recovery_email_link`, `claim.account_recovery_gov.hub_mai_reset_channels`

### 4. Setează credențialele noi

- **Ce faci:** Deschide mesajul numai dacă domeniul este oficial și setează o parolă nouă, unică.
- **Până când:** `none`
- **Cum știi că e gata:** Te poți autentifica din nou pe domeniul oficial.
- **Dacă eșuează:** Dacă linkul este expirat sau suspect, pornește din nou din pagina oficială.
- **Canale:** `channel.ghiseul_recovery`, `channel.anaf_recovery`, `channel.hub_mai_reset`
- **Claims:** `claim.account_recovery_gov.ghiseul_credentials_by_email`, `claim.account_recovery_gov.anaf_recovery_email_link`, `claim.account_recovery_gov.hub_mai_reset_channels`

### 5. Securizează contul recuperat

- **Ce faci:** Verifică e-mailul și telefonul asociat, deconectează sesiunile necunoscute unde platforma permite și păstrează parola în siguranță.
- **Până când:** `none`
- **Cum știi că e gata:** Datele asociate sunt corecte și autentificarea funcționează.
- **Dacă eșuează:** Raportează imediat accesul neautorizat instituției.
- **Canale:** `channel.roeid_recovery`, `channel.ghiseul_support`, `channel.hub_mai_reset`
- **Claims:** `claim.account_recovery_gov.roeid_email_change`, `claim.account_recovery_gov.roeid_phone_change`, `claim.account_recovery_gov.ghiseul_support_after_failure`

## Requirements

| id | titlu | obligație | timing | forme | verificări | claims |
|---|---|---|---|---|---|---|
| `req.registered_email` | Acces la e-mailul asociat | `conditional` | `now` | electronic | user_confirmed | `claim.account_recovery_gov.ghiseul_credentials_recovery`, `claim.account_recovery_gov.anaf_recovery_inputs` |
| `req.cnp` | CNP | `conditional` | `now` | electronic | field_present, user_confirmed | `claim.account_recovery_gov.ghiseul_credentials_recovery`, `claim.account_recovery_gov.anaf_recovery_inputs` |
| `req.anaf_current_credentials` | Credențiale și răspuns de siguranță ANAF | `conditional` | `now` | electronic | field_present, user_confirmed | `claim.account_recovery_gov.anaf_change_email_inputs` |
| `req.hub_validated_contact` | E-mail sau telefon validat în Hub MAI | `conditional` | `now` | electronic | field_present, user_confirmed | `claim.account_recovery_gov.hub_mai_validated_contact` |
| `req.roeid_reenrolment_kit` | Kit pentru reînrolare ROeID | `conditional` | `now` | original, electronic | exists, not_expired, user_confirmed | `claim.account_recovery_gov.roeid_password_forgotten`, `claim.account_recovery_gov.roeid_email_change`, `claim.account_recovery_gov.roeid_phone_change` |

## Official channels

| id | tip | etichetă | URL | integrare | teritoriu |
|---|---|---|---|---|---|
| `channel.roeid_recovery` | `web` | ROeID — întrebări frecvente | https://www.roeid.ro/%C3%AEntreb%C4%83ri-frecvente | `DEEP_LINK` | ro |
| `channel.ghiseul_recovery` | `web` | Ghișeul.ro — recuperare date de acces | https://www.ghiseul.ro/ghiseul/public/informatii/intrebari-frecvente | `DEEP_LINK` | ro |
| `channel.ghiseul_support` | `web` | Ghișeul.ro — contact | https://www.ghiseul.ro/ghiseul/public/informatii/contact | `DEEP_LINK` | ro |
| `channel.anaf_recovery` | `web` | ANAF SPV — recuperare credențiale | https://www.anaf.ro/InregPersFizicePublic/recuperarecredentiale.jsp | `DEEP_LINK` | ro |
| `channel.anaf_change_email` | `web` | ANAF SPV — schimbare e-mail | https://www.anaf.ro/InregPersFizicePublic/schimbareEmail.jsp | `DEEP_LINK` | ro |
| `channel.hub_mai_reset` | `web` | Hub MAI — resetare parolă | https://hub.mai.gov.ro/site/forgot-password | `DEEP_LINK` | ro |

## Source claims

| claim_id | afirmație | sursă | confidence | locator |
|---|---|---|---|---|
| `claim.account_recovery_gov.roeid_password_known` | Dacă parola ROeID curentă este cunoscută, aceasta poate fi schimbată din Setări > Modificare parolă. | `roeid_faq` | `verified` | FAQ ROeID, întrebarea «Cum îmi pot schimba parola?» |
| `claim.account_recovery_gov.roeid_password_forgotten` | Dacă parola ROeID nu mai este cunoscută, este necesară reluarea procesului de înrolare. | `roeid_faq` | `verified` | FAQ ROeID, întrebarea «Cum îmi pot schimba parola?» |
| `claim.account_recovery_gov.roeid_email_change` | Schimbarea adresei de e-mail ROeID necesită o nouă validare a identității și reinstalarea aplicației. | `roeid_faq` | `verified` | FAQ ROeID, întrebarea «Cum pot să schimb adresa de email a contului?» |
| `claim.account_recovery_gov.roeid_phone_change` | Schimbarea telefonului ROeID necesită reluarea înregistrării; aplicația de pe vechiul telefon se dezactivează după aprobare. | `roeid_faq` | `verified` | FAQ ROeID, întrebarea «Pot instala și folosi aplicația pe un alt telefon?» |
| `claim.account_recovery_gov.ghiseul_credentials_recovery` | Ghișeul.ro regenerează datele de acces prin CNP/CUI și adresa de e-mail asociată contului. | `ghiseul_faq` | `verified` | FAQ Ghișeul.ro, întrebarea 6 |
| `claim.account_recovery_gov.ghiseul_credentials_by_email` | Noile date de acces Ghișeul.ro sunt transmise automat la adresa de e-mail asociată. | `ghiseul_faq` | `verified` | FAQ Ghișeul.ro, întrebarea 6 |
| `claim.account_recovery_gov.ghiseul_support_after_failure` | Ghișeul.ro recomandă contactarea suportului numai dacă datele regenerate nu ajung pe e-mail. | `ghiseul_faq` | `verified` | FAQ Ghișeul.ro, întrebarea 6 |
| `claim.account_recovery_gov.anaf_recovery_inputs` | Recuperarea credențialelor SPV pentru persoană fizică cere CNP-ul și e-mailul folosit la înregistrare. | `anaf_recovery` | `verified` | Pagina «Recuperare credențiale» |
| `claim.account_recovery_gov.anaf_recovery_email_link` | ANAF trimite pe e-mail datele necesare recuperării; utilizatorul accesează linkul primit și schimbă parola. | `anaf_recovery_success` | `verified` | Pagina de confirmare «Recuperare credențiale» |
| `claim.account_recovery_gov.anaf_change_email_inputs` | Schimbarea e-mailului SPV cere nume de utilizator, parolă, răspuns la întrebarea de siguranță și noua adresă. | `anaf_change_email` | `verified` | Pagina «Schimbare email» |
| `claim.account_recovery_gov.hub_mai_reset_channels` | Hub MAI permite generarea codului de resetare prin e-mail sau SMS, folosind e-mailul ori telefonul validat. | `hub_mai_reset` | `verified` | Pagina «Resetare parolă» |
| `claim.account_recovery_gov.hub_mai_validated_contact` | Pentru resetarea Hub MAI se introduce adresa utilizată sau numărul de telefon validat în portal. | `hub_mai_reset` | `verified` | Pagina «Resetare parolă» |

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
