# Product Requirements Document

## 1. Obiectivul produsului

Reducerea drumurilor administrative inutile și creșterea ratei dosarelor acceptate din prima, prin transformarea regulilor publice într-un traseu personalizat, temporal, teritorial și explicabil.

## 2. Jobs to be done

### Cetățean

- Când am un obiectiv administrativ, vreau să aflu traseul exact pentru situația mea, ca să nu pierd timp interpretând site-uri.
- Când pregătesc dosarul, vreau să știu ce îmi lipsește și ce este doar condițional, ca să nu adun acte inutil.
- Când o informație este incertă, vreau să văd ce trebuie confirmat și întrebarea exactă, nu o presupunere.
- Când mă apropii de termen, vreau să fiu avertizat și să văd alternativa dacă l-am ratat.
- Când ajung la instituție, vreau să știu ce originale prezint și ce dovadă trebuie să primesc.

### Curator

- Când o sursă se schimbă, vreau să văd diff-ul și impactul asupra traseelor înainte de publicare.
- Când extrag reguli, vreau fiecare afirmație legată de dovadă și marcată după risc.
- Când public o schimbare, vreau să pot reproduce, audita și reveni la versiunea anterioară.

### Operator produs

- Vreau să văd ce reguli se apropie de expirare, ce conflicte sunt deschise și ce feedback-uri indică respingeri reale.
- Vreau să măsor acceptarea din prima, nu timpul petrecut în aplicație.

## 3. Personaje de referință

### Ana — părinte ocupat

Are nevoie de grădiniță sau școală, nu cunoaște diferența dintre reînscriere, etapa I și ajustări. Are documentele împrăștiate și se teme să nu piardă termenul.

### Mihai — adult care rezolvă o schimbare de viață

Schimbă domiciliul sau numele. Procedura atinge mai multe instituții și nu știe ordinea corectă.

### Elena — utilizator cu competențe digitale reduse

Are nevoie de propoziții simple, acțiuni mari, explicații audio opționale și posibilitatea de a exporta checklistul pentru un membru al familiei.

### Radu — curator juridic/operațional

Nu scrie cod. Trebuie să poată compara surse, aproba reguli, vedea impactul și bloca publicarea dacă dovada este slabă.

## 4. Capabilități funcționale

### FR-01 Descoperirea intenției

- Căutare semantică dintr-un catalog controlat de intenții.
- Sugestii și întrebări de dezambiguizare.
- Niciun text liber nu este transformat direct în obligație.

### FR-02 Context și jurisdicție

- Județ, UAT, instituție, dată de referință și anul procedural.
- Fapte personale tipate: dată naștere, statut, program dorit, reprezentare, situații speciale.
- Fiecare întrebare declară de ce este necesară și durata de păstrare.

### FR-03 Rezolvarea traseului

- Selectarea bundle-ului publicat pentru intenție, jurisdicție și timp.
- Evaluare de predicate tipate.
- Sortare topologică a pașilor și detectarea ciclurilor.
- Output cu hash reproductibil, surse și stări de încredere.

### FR-04 Checklist și timeline

- Statusuri: `not_started`, `ready`, `blocked`, `in_progress`, `submitted`, `completed`, `not_applicable`.
- Separare: necesar acum / condițional / mai târziu.
- Termene absolute și relative, timezone `Europe/Bucharest`.
- Remediere și rută alternativă.

### FR-05 Dosar și document readiness

- Import local foto/PDF.
- Clasificare document, OCR, câmpuri extrase și verificări formale.
- Findings: blocking, warning, info, unknown.
- Utilizatorul confirmă/correctează câmpurile extrase.
- Autenticitatea rămâne `not_verified` dacă nu există verificare oficială.

### FR-06 Surse și explicabilitate

- Fiecare cerință afișează sursa, publisherul, aplicabilitatea, data verificării și fragmentul relevant.
- Confidence: `verified`, `verified_with_local_gap`, `needs_confirmation`, `conflicting`, `expired`.
- Nu se folosește un procent decorativ de încredere.

### FR-07 Depunere și canal oficial

- Adresă, program, programare, originale, taxă și expected receipt.
- Deep-link allowlisted către domeniul oficial.
- Integrările sunt feature-gated și au status explicit.

### FR-08 Recalculare

Trigger-uri:

- schimbarea unui fapt;
- schimbarea jurisdicției;
- publicarea unui bundle nou;
- termen ratat;
- respingere/loc indisponibil;
- document expirat.

Aplicația arată diferența dintre ruta veche și cea nouă înainte de acceptare.

### FR-09 Feedback de teren

- „Mi s-a cerut un document suplimentar.”
- „Programul sau adresa sunt greșite.”
- „Linkul oficial nu funcționează.”
- „Dosarul a fost acceptat din prima.”

Feedback-ul nu schimbă direct regula; creează un incident de verificare.

### FR-10 Portal curator

- Registry surse și jurisdicții.
- Fetch manual/automat, snapshot, diff semantic și raw.
- Draft AI cu citate; schema validation.
- Review pe claim, regulă și impact.
- Publish canary, publish general, rollback.
- Dashboard de staleness, conflicte și feedback.

## 5. Cerințe non-funcționale

- API p95 sub 400 ms pentru route resolve cu bundle în cache; sub 1.5 s cold path.
- Route resolve este pur determinist și nu efectuează call extern.
- Aplicația rămâne utilă offline pentru traseele și documentele deja descărcate.
- Zero secrete în client sau repository.
- Disponibilitate țintă API R1: 99.5%; portal curator: 99.0%.
- RPO 24h și RTO 4h pentru date operaționale; rule bundles publicate sunt versionate și replicabile.
- WCAG 2.2 AA pentru portal; Android accessibility checks și font scaling 200%.
- Localizare română completă; toate stringurile UI externalizate.
- Telemetria nu conține CNP, nume, adrese, OCR raw sau imagini.

## 6. North Star și metrici

**North Star:** rata dosarelor marcate `ready` care sunt acceptate fără drum suplimentar și fără document omis de produs.

Metrici secundare:

- drumuri inutile evitate;
- timp de la intenție la dosar gata;
- false-block rate;
- reguli critice expirate expuse — ținta zero;
- vârsta medie și p95 a verificării surselor;
- route resolution errors;
- feedback confirmat per 1.000 trasee;
- procent de pași cu provenance complet;
- rata de finalizare a traseului;
- procent de documente procesate exclusiv local.

## 7. Evenimente analytics fără PII

- `intent_selected`
- `journey_started`
- `question_answered` cu `question_id`, nu valoarea sensibilă
- `route_resolved`
- `step_opened`
- `requirement_marked_ready`
- `document_analysis_started` cu tip generic
- `finding_created` cu cod, nu conținut
- `official_channel_opened`
- `route_recalculated`
- `feedback_submitted`
- `journey_completed`

Toate evenimentele au consent și pot fi dezactivate.
