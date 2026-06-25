# Securitate și confidențialitate — LifeOS România

## Principii

- **Date minime.** Se colectează doar faptele care ramifică traseul; fiecare fapt are scop și sensibilitate (`public`/`personal`/`sensitive`/`special_category`).
- **Local-first pentru documente.** Documentele utilizatorului stau implicit local; vault cloud doar la opt-in explicit.
- **Retenție** conform `config/retention_policy.yaml` (documente șterse implicit după 30 de zile; metadate de rută 12 luni; loguri cu PII redactat).
- **EU-region, GDPR.** Drept de ștergere și export.
- **Cont opțional.** Aplicația funcționează și fără cont; sincronizarea cere cont.

## Acces și roluri

- Curatori prin OIDC + RBAC; promovarea conținutului la `verified` cere two-person rule.
- Audit pe orice publicare de bundle și pe orice modificare de surse/claim-uri.

## Runtime

- Fără LLM/internet/OCR în decizia de rutare. Extragerea AI se face offline, pe partea de curator, și produce doar `SourceClaim` propuse, revizuite de oameni.
- Fail-closed pe clase critice stale: o regulă critică expirată nu poate produce `READY_TO_SUBMIT`.
