# Guvernanța surselor și operațiunile de conținut

## 1. Principiul central

Produsul este un sistem de operare al regulilor, nu o colecție de articole. Menținerea adevărului este o funcție de produs de prim rang.

## 2. Surse acceptate

### Tier 1 — normativ

- Portal Legislativ / Monitorul Oficial;
- EUR-Lex;
- acte publicate de autoritatea emitentă.

### Tier 2 — oficial operațional

- ministere, agenții, inspectorate, primării, servicii publice și unități;
- portaluri oficiale de depunere/plată;
- calendare și formulare oficiale.

### Tier 3 — confirmare instituțională documentată

- răspuns public oficial;
- comunicare semnată/înregistrată de instituție;
- dataset public furnizat formal.

### Tier 4 — semnal, nu adevăr

- feedback utilizator;
- presă;
- forumuri și social media.

Tier 4 poate declanșa verificarea, dar nu poate publica o obligație.

## 3. Registry-ul unei surse

Câmpuri obligatorii:

- `source_id`
- titlu și publisher;
- URL canonic și domeniu allowlisted;
- tip sursă;
- autoritate și jurisdicție;
- competență;
- access mode și termeni;
- frecvență de verificare;
- freshness class;
- parser strategy;
- owner;
- status;
- ultima verificare reușită;
- următoarea verificare;
- escalation policy.

## 4. Pipeline de ingestie

1. scheduler creează job;
2. fetcher folosește rate limits, conditional requests și user-agent identificabil;
3. snapshotul raw este stocat imutabil;
4. normalizer extrage text, structură, linkuri și metadata;
5. hash/diff compară cu snapshotul anterior;
6. classifier atribuie severitate;
7. extractor AI produce draft de claim și regulă, cu citate;
8. schema validator respinge output incomplet;
9. curatorul verifică;
10. impact analysis și teste;
11. publish/rollback.

## 5. Crawler policy

- Respectă robots.txt, termenii și limitele tehnice.
- Nu ocolește autentificări, CAPTCHA sau protecții.
- Nu colectează date personale din formulare sau pagini de rezultate individuale.
- Folosește `If-None-Match` și `If-Modified-Since` când sunt disponibile.
- Max 1 request/secundă/domeniu implicit, configurabil mai strict.
- Playwright este fallback pentru conținut public randat JS, nu instrument de bypass.
- PDF-urile text sunt parse; OCR numai pentru documente scanate și cu confidence marcat.

## 6. Severitatea schimbării

- `cosmetic` — whitespace, meniu, tracking; nu cere review procedural.
- `informational` — explicații fără impact asupra traseului.
- `operational` — program, adresă, link, contact.
- `procedural` — pași, documente, criterii, canal.
- `critical` — eligibilitate, deadline, taxă, obligație, derogare.

Schimbările `procedural` și `critical` nu se publică fără reviewer uman.

## 7. SLA de review

- critical activ: 4 ore lucrătoare;
- procedural în perioadă activă: 1 zi lucrătoare;
- operational: 2 zile;
- informational: 5 zile.

Dacă SLA-ul expiră, confidence scade automat; pentru clasa A se blochează afirmația afectată.

## 8. Review roles

- `researcher` — înregistrează surse și drafturi;
- `curator` — validează claim-uri și reguli;
- `senior_reviewer` — aprobă schimbări cu risc mare;
- `publisher` — publică bundle-ul;
- `auditor` — read-only, export și verificare.

Separation of duties: autorul unei schimbări critice nu o poate publica singur.

## 9. Conflict workflow

1. sistemul detectează suprapunerea;
2. blochează regula afectată;
3. curatorul evaluează rang, competență, teritoriu și timp;
4. cere clarificare oficială dacă este necesar;
5. documentează decizia și eventualul override;
6. rulează impact analysis;
7. publică sau păstrează `needs_confirmation`.

## 10. Feedback de teren

Feedback-ul primește:

- severitate;
- duplicat grouping;
- link către traseu și versiune;
- instituție și dată;
- status: received, triaged, verifying, confirmed, rejected, resolved.

Dacă este confirmat oficial, se creează un nou source claim; feedback-ul original rămâne provenance de incident, nu de regulă.

## 11. Politica anti-rule-rot

Fiecare source are `max_unverified_age`. Schedulerul generează:

- `fresh`;
- `review_due`;
- `stale`;
- `expired`;
- `unreachable`.

În perioade active de înscriere, frecvența crește automat. Calendarul și locurile nu folosesc aceeași politică de cache ca metodologia stabilă.

## 12. Backup și probatoriu

- snapshoturile publicate se păstrează cel puțin pe durata auditului și a versiunilor active;
- hashurile și metadata sunt imutabile;
- bloburile au object lock dacă providerul permite;
- exportul unui traseu include versiunea, sursele și timestamps, fără documentele utilizatorului implicit.
