# 11 — Security, Privacy & Compliance Baseline

Acest document este baseline tehnic, nu opinie juridică finală. Înainte de lansare se execută DPIA/legitimate basis assessment și review juridic pentru fluxurile reale.

## 1. Threat model

Active principale:

- documente de identitate și date extrase;
- adrese, relații familiale și active;
- journeys care dezvăluie evenimente sensibile;
- rulesets și source claims;
- conturi curator/reviewer;
- canale oficiale și linkuri;
- tokenuri de autentificare;
- audit și feedback de respingere.

Adversari:

- atacator extern;
- aplicație compromisă/dispozitiv pierdut;
- partener rău-intenționat;
- insider cu acces excesiv;
- sursă oficială compromisă sau domeniu schimbat;
- prompt injection în pipeline-ul de extracție;
- dependency/supply-chain compromise.

## 2. Privacy by design

- contul este opțional pentru flow-ul de bază;
- faptele sunt cerute progresiv;
- scopul fiecărui câmp este explicat;
- local-only este default pentru documente;
- analytics nu primește text liber sau PII;
- retenția este selectabilă și vizibilă;
- exportul și ștergerea sunt funcții de produs;
- cloud processing și human review au consimțăminte distincte;
- dark patterns și bundle consent sunt interzise.

## 3. Mobile controls

Țintă: OWASP MASVS 2.1.0 ca baseline.

- tokenuri/chei în SecureStore/Keychain/Keystore;
- SQLite sensibil criptat sau câmpuri envelope-encrypted;
- screenshots blocate pe ecrane de document unde platforma permite și utilizatorul este avertizat;
- clipboard evitat pentru CNP/date sensibile;
- deep links allowlisted și validate;
- certificate pinning evaluat, nu introdus fără strategie de rotație;
- root/jailbreak detection doar semnal, nu blocare absolută;
- debug logs și dev menu eliminate în production;
- backup OS exclus pentru vault keys unde este necesar;
- auto-lock vault opțional;
- biometric unlock pentru vault, fără a transforma biometria în autentificare server.

## 4. Backend controls

Țintă: OWASP ASVS 5.0 nivel adecvat riscului.

- authn/authz la fiecare boundary;
- object-level authorization și RLS;
- input validation Pydantic + DB constraints;
- rate limits separate public/auth/admin;
- idempotency și replay protection;
- CSRF pentru admin browser flows;
- CORS strict;
- SSRF protection în source fetcher;
- allowlist schemes și private-network blocking;
- malware scan pentru uploaduri cloud;
- signed URLs scurte;
- secrets în secret manager;
- dependency scanning, SBOM și provenance;
- encryption in transit și at rest;
- backups criptate și restore tests.

## 5. Admin controls

- MFA obligatoriu;
- roluri: researcher, curator, reviewer, publisher, security_admin;
- separation of duties: autorul nu poate publica singur o regulă critical;
- session timeout și revocation;
- audit pentru read access la documente/feedback sensibile;
- exporturile sunt watermarkate și limitate;
- bulk actions cer re-auth;
- publish/withdraw au motiv obligatoriu.

## 6. Rule supply chain

- snapshot hash și URL canonic;
- extracted text este conținut neîncrezător;
- prompturile de extracție nu pot executa instrucțiuni din document;
- output strict schema-validated;
- reviewer vede excerptul original;
- rule package semnat/hash-uit;
- API încarcă numai manifest aprobat;
- rollback la ruleset anterior;
- alertă pentru modificări masive sau sursă/domain change.

## 7. Document processing

Readiness checks sunt clasificate:

- deterministic local: format, expiry, field presence;
- heuristic local: document type, signature region;
- cloud model: numai cu consimțământ și retenție;
- registry verification: numai adapter autorizat.

Rezultatul include `check_type`, `engine_version`, `confidence`, `limitations` și nu este transformat automat în autenticitate.

## 8. Incident response

Severități:

- SEV0: expunere documente/chei sau ruleset corupt la scară;
- SEV1: acces neautorizat, canal oficial compromis, critic rule wrong;
- SEV2: indisponibilitate majoră sau freshness failure;
- SEV3: bug limitat, fără impact critic.

Acțiuni minime:

1. contain / kill switch;
2. preserve audit;
3. assess affected users/journeys;
4. rotate/revoke;
5. notify conform obligațiilor;
6. correct ruleset/data;
7. postmortem fără culpabilizare;
8. add regression test.

## 9. Compliance work products înainte de production

- record of processing activities;
- DPIA pentru document vault și profiling administrativ;
- privacy notice pe scopuri;
- DPA-uri cu vendorii;
- retention schedule;
- data subject request runbook;
- international transfer assessment dacă există;
- AI system inventory și clasificare;
- accessibility statement;
- vulnerability disclosure policy;
- incident notification matrix;
- legal review pentru disclaimere și parteneri.

## 10. Standard references

- EDPB Guidelines 4/2019 — Data Protection by Design and by Default;
- OWASP MASVS 2.1.0 și MASTG;
- OWASP ASVS 5.0.0;
- WCAG 2.2 AA pentru interfețele web și principiile echivalente native.
