# Securitate, confidențialitate și conformitate

## 1. Date cu risc ridicat

- documente de identitate;
- certificate de naștere;
- adrese;
- date despre copii;
- situații familiale;
- documente medicale/CES;
- numere de înregistrare și documente administrative.

Prin urmare, securitatea nu este un addon. Baseline-ul este OWASP MASVS 2.1 pentru mobil și ASVS 5.0 pentru API/web.

## 2. Model de procesare implicit

- traseul poate exista anonim;
- documentele sunt importate și analizate local;
- OCR raw și imagini nu părăsesc dispozitivul;
- backendul primește numai statusuri și metadata strict necesare dacă sincronizarea nu este activată;
- uploadul este o acțiune distinctă, cu scop, retenție și consimțământ explicite.

## 3. Criptare

### Android

- chei master generate în Android Keystore;
- chei per dossier/document, envelope encryption;
- AES-GCM cu nonce unic;
- fișiere în internal app storage;
- backup Android dezactivat pentru assets sensibile sau controlat prin rules;
- clipboard și screenshot protection numai pe ecranele cu date sensibile, fără a bloca inutil accesibilitatea;
- no hardcoded secrets.

### Server

- TLS 1.2+;
- encryption at rest provider + application envelope encryption pentru uploaduri;
- KMS/secret manager;
- presigned URLs scurte și scope limitat;
- hashes pentru integritate;
- rotation și revocation.

## 4. Retenție

- fără cont: documentele locale până la ștergere/dezinstalare;
- cont fără sync: numai route metadata;
- sync activ: utilizatorul alege 7/30/90 zile sau până la finalizarea traseului;
- feedback attachments: 30 zile implicit, extensie justificată pentru incident;
- audit de reguli: păstrare lungă, fără PII de utilizator;
- logs: 30 zile operațional, fără PII;
- backupurile respectă expirarea prin crypto-shredding unde ștergerea imediată nu este posibilă.

## 5. Drepturile utilizatorului

- export route metadata și document findings;
- ștergere cont și sync assets;
- retragere analytics consent;
- ștergere dossier separat de cont;
- explicația scopului fiecărui câmp;
- contact DPO/operator;
- răspuns DSAR urmărit procedural.

## 6. Date despre minori

- contul aparține părintelui/reprezentantului;
- nu se creează profil de copil cu acces independent;
- se colectează numai datele necesare traseului;
- datele medicale/special-category rămân local implicit;
- niciun model generativ terț nu primește documente de copil.

## 7. Threat model sumar

| Amenințare | Control principal |
|---|---|
| Furtul documentelor de pe telefon | internal storage, Keystore, encryption, auth device |
| MITM/API spoofing | TLS, certificate validation, optional pinning with rotation plan |
| Deep-link phishing | allowlist domain + interstitial cu domeniul exact |
| Compromiterea contului curator | OIDC, MFA, RBAC, reauth publish, audit |
| Regulă malițioasă/greșită | human gate, schema, tests, two-person review, rollback |
| Source poisoning | official allowlist, snapshots, content hash, provenance |
| LLM hallucination | draft-only, no auto-publish, claim spans obligatorii |
| Log leakage | structured redaction, denylist keys, tests |
| Upload URL abuse | content type validation, size limits, AV scan, short presign |
| IDOR | ownership checks, RLS/authorization tests |
| SQL injection | parameterized ORM/queries, no string SQL from input |
| Supply chain | lockfiles, SBOM, dependency scanning, signed builds |

## 8. API security

- rate limits pe IP/session/user;
- idempotency keys pentru writes sensibile;
- CSRF pentru web sessions;
- CORS deny-by-default;
- JWT audience/issuer checks;
- object-level authorization;
- request size limits;
- upload MIME sniffing și decompression bomb protection;
- pagination hard limits;
- no stack traces în producție;
- security headers;
- audit pentru admin writes.

## 9. Mobile security gates

- exported components minimizate;
- app links verificate;
- network security config fără cleartext;
- root/debug detection doar ca semnal, nu blocaj universal;
- release build non-debuggable;
- obfuscation/minification;
- Play Integrity opțional pentru operațiuni server-side cu risc;
- biometric gate opțional pentru dossier, nu obligatoriu pentru accesibilitate.

## 10. DPIA și juridic

Înainte de producție:

- mapare activități și temeiuri;
- DPIA pentru documente și date despre copii;
- DPA cu furnizorii;
- registru procesare;
- procedură breach;
- termeni care clarifică rolul de ghid și limitele;
- review juridic al microcopy-ului de „pregătit” și „confirmat”.

Disclaimerul nu înlocuiește designul sigur. Produsul trebuie să prevină în mod tehnic afirmațiile pe care nu le poate susține.

## 11. Incident response

Se definesc:

- severity matrix;
- on-call;
- izolare/revocare credentials;
- invalidare bundle;
- notificare utilizatori afectați;
- conservarea probelor;
- postmortem fără culpabilizare;
- test tabletop trimestrial.
