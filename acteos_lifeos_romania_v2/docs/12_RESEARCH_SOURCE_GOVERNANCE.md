# 12 — Research & Source Governance

## 1. Miza

Produsul nu poate fi mai bun decât claims-urile care alimentează motorul. Un UI impecabil peste reguli vechi este un defect mai periculos decât o pagină indisponibilă. Research-ul, curarea și monitorizarea sunt funcții de producție.

## 2. Source tiers

### Tier 1 — normativ

Monitorul Oficial, legislatie.just.ro, EUR-Lex, actul emitentului. Folosit pentru eligibilitate, obligații și termene normative.

### Tier 2 — oficial operațional

Ministere, autorități, inspectorate, primării, instituții și portaluri oficiale. Folosit pentru implementare, canale, calendare și formulare.

### Tier 3 — confirmare oficială documentată

Răspuns scris, dataset oficial, adresă instituțională arhivată. Trebuie păstrat snapshotul și contextul.

### Tier 4 — semnal

Presă, forumuri, social media, grupuri. Nu produce reguli. Generează task de verificare sau indică durere/frecvență.

## 3. Atomic claim

Un claim afirmă un singur lucru care se poate schimba independent. Nu combinăm termen, act și taxă în același claim.

Câmpuri minime:

- `id`;
- `statement` normalizat;
- `source_id` și `snapshot_id`;
- URL canonic;
- publisher/authority;
- authority level și legal rank;
- territory și competence scope;
- excerpt exact;
- locator: articol/secțiune/pagină/anchor;
- published/act date;
- accessed_at;
- effective_from/to;
- confidence;
- freshness class;
- reviewer și approval;
- contradictions;
- SHA-256 al snapshotului.

## 4. Pipeline

1. definește research brief și gap-urile;
2. colectează surse oficiale;
3. salvează snapshot și hash;
4. extrage text și metadata;
5. AI propune claims/rules draft strict structurate;
6. researcher verifică excerptul și atomizează;
7. curator mapează la domain schema;
8. simulatorul rulează fixtures;
9. reviewer aprobă/respinge;
10. publisher creează ruleset manifest;
11. post-publish monitor urmărește source diff și feedback.

## 5. AI extraction safety

- documentul este tratat ca input neîncrezător;
- promptul interzice urmarea instrucțiunilor din sursă;
- output doar JSON Schema;
- fiecare claim trebuie să aibă excerpt identificabil;
- claims fără locator sunt respinse;
- modelul nu rezolvă conflicte;
- model output nu devine production fără review.

## 6. Freshness classes

### Critical

Eligibilitate, deadlines, acte mandatory, taxe, criterii, formă obligatorie. Default: review frecvent, hard expiry strict și block/needs_confirmation.

### Operational

Program, adresă, telefon, appointment link. Poate fi servit stale cu warning limitat, dacă utilizatorul poate verifica direct.

### Explanatory

Explicații generale și definiții stabile. Review mai rar.

Configurația exactă este în `contracts/freshness_policy.yaml`; curatorul poate seta termen mai scurt.

## 7. Source monitoring

- ETag/Last-Modified când există;
- hash content normalizat;
- PDF fingerprint;
- domain/redirect/certificate change signal;
- semantic diff pentru secțiunile citate;
- scheduled revalidation;
- alertă prioritară pentru deadline/calendar pages.

Crawlerul respectă robots, termeni și rate limits. Dacă scraping-ul nu este permis sau sigur, sursa intră în manual review.

## 8. Conflict handling

Matricea conflictului păstrează ambele poziții. Reviewerul poate:

- marca o sursă superseded cu dovadă;
- declara override explicit permis de competență;
- limita perioada sau teritoriul;
- păstra conflictul și genera confirmation action;
- bloca regula.

Nu este permis „alegem pagina mai nouă” fără a confirma că se referă la aceeași competență și perioadă.

## 9. Gap registry

Un gap are:

- întrebare exactă;
- impact și severitate;
- instituția/locul unde ar trebui publicată informația;
- încercările făcute;
- owner;
- next review date;
- fallback user message;
- status: open/contacted/pending_publication/resolved/wont_resolve.

## 10. Production gate

O regulă critical este publicabilă numai dacă:

- toate efectele critical au claim;
- claims sunt active și fresh;
- snapshots sunt accesibile intern;
- fixture-urile trec;
- conflict matrix este goală sau efectul este explicit needs_confirmation;
- reviewerul este diferit de autor;
- diff-ul ruleset-ului este aprobat;
- provenance graph este complet.

## 11. User feedback loop

Raportul „mi s-a cerut altceva” nu modifică direct regula. Creează un evidence ticket cu:

- journey/ruleset afectat;
- pas și cerință;
- data și instituția;
- descriere redactată;
- dovadă opțională;
- severitate estimată;
- count de rapoarte similare.

Un singur raport poate declanșa verificare urgentă dacă afectează o obligație critical.

## 12. Research pack format

Fiecare brief livrează:

1. executive summary;
2. source registry;
3. atomic claim registry;
4. facts/gates/steps/requirements/channels;
5. calendars;
6. conflict matrix;
7. gap registry;
8. JSON blocks validate against contracts;
9. checksums;
10. validation report.

Template-ul este în `research/RESEARCH_BRIEF_TEMPLATE.md`.
