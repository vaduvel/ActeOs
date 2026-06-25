# 13 — Content Operations

## 1. De ce există o echipă de conținut

În ActeOS, conținutul nu este marketing copy. Este o reprezentare operabilă a regulilor administrative. Echipa de conținut gestionează aceeași clasă de risc pe care o echipă financiară o gestionează în rate sau limite: orice schimbare trebuie observată, verificată, simulată și publicată controlat.

## 2. Roluri

### Researcher

Găsește surse, salvează snapshot-uri, creează claims draft și documentează gaps. Nu publică.

### Curator

Normalizează claims, construiește reguli și steps, adaugă fixtures. Nu aprobă singur propria regulă critical.

### Reviewer

Verifică sursa, competența, perioada, schema și impactul. Aprobă sau respinge cu motiv.

### Publisher

Publică ruleset-ul după ce gate-urile automate și umane sunt verzi. Poate retrage în incident.

### Content designer

Scrie instruction/recovery/copy în limbaj clar fără să modifice sensul normativ.

### Security/Privacy reviewer

Intervine la surse noi, procesare documente, integrări și date sensibile.

## 3. Queue-uri operaționale

- source changes detected;
- claims due for review;
- hard expiry approaching;
- unresolved conflicts;
- open gaps critical;
- user rejection reports;
- broken official channels;
- new publication/calendar;
- rule simulation failures;
- journeys impacted by upcoming ruleset.

## 4. Prioritate

P0: regulă critical greșită/compromisă sau leak.  
P1: deadline/eligibility/doc mandatory posibil greșit.  
P2: program/canal nefuncțional sau conflict local.  
P3: explicație/copy/metadata.

## 5. Daily operating loop

1. triage alerte și feedback;
2. verificare P0/P1;
3. research și snapshot;
4. claim/rule edit;
5. simulation;
6. independent review;
7. publish sau gap message;
8. monitor journeys affected;
9. close with evidence.

## 6. Publish checklist

- source canonical și snapshot hash;
- excerpt/locator verificabil;
- authority și competence scope;
- effective interval;
- claim atomic;
- rule AST valid;
- no orphan references/cycles;
- fixtures green;
- copy review;
- freshness dates;
- conflict review;
- impact diff;
- rollback target;
- reviewer/publisher distinct pentru critical.

## 7. Rule rot dashboard

Dashboardul minim arată:

- coverage critical by intent;
- claims stale/hard-expired;
- sources unavailable;
- average time change-detected → published;
- feedback rate per 1.000 journeys;
- rules with repeated rejection reports;
- unreviewed local gaps;
- calendars pending publication.

## 8. Deprecation

Când o procedură dispare:

- rule revision devine superseded/withdrawn;
- event type poate rămâne discoverable cu redirect spre noul event;
- journeys active primesc recalculation;
- istoricul rămâne reproductibil;
- copy-ul explică schimbarea și data, nu afișează generic „nu mai este disponibil”.

## 9. Localisation

Limba canonică este româna. Traducerea în alte limbi se face numai după stabilizarea sensului și cu review administrativ. Claim excerpt rămâne în limba sursei, iar explicația poate fi tradusă.

## 10. Quality sampling

Lunar, se selectează eșantion pe:

- events cu volum mare;
- rules critical;
- local overrides;
- rules cu feedback;
- channels recent changed;
- journeys completed fără outcome report.

Sampling-ul nu înlocuiește hard expiry și monitoring.
