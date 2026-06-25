# Incident runbook

## Severități

- SEV-0: expunere confirmată de documente/PII sau reguli malițioase publicate;
- SEV-1: trasee critice greșite la scară, autentificare compromisă, indisponibilitate totală;
- SEV-2: funcție majoră degradată, surse critice expirate fără fallback sigur;
- SEV-3: defect limitat cu workaround.

## Primele acțiuni

1. desemnează incident commander și canal unic;
2. oprește funcția/rulesetul prin feature flag dacă reduce riscul;
3. păstrează dovezile și nu modifica auditul;
4. limitează accesul, rotește credențialele dacă este relevant;
5. cuantifică utilizatorii, datele, intervalul și rulesetul afectat;
6. comunică factual, fără presupuneri;
7. aplică obligațiile de notificare legală după evaluarea DPO/legal;
8. publică postmortem intern cu acțiuni, owner și termen.
