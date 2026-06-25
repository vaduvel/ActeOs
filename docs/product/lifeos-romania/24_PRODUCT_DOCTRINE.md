# 24 — Doctrina de produs (transplant din v2)

Doctrina este constituția produsului. Se schimbă doar prin decizie explicită și versiune majoră.

- **D1. Intrarea este evenimentul de viață.** „Ce s-a întâmplat?" Instituția/formularul/actul sunt rezultate, nu condiții de pornire.
- **D2. Traseul este o concluzie executabilă.** Pași ordonați, prerechizite, termene, acte, costuri confirmate, canale, dovezi de finalizare și căi de recuperare. O listă de linkuri nu e un traseu.
- **D3. Runtime-ul critic este determinist.** Eligibilitate, includere de act, termen, blocare, readiness = reguli tipate. LLM doar propune/explică, nu modifică rezultatul.
- **D4. Adevărul este temporal și teritorial.** Orice rezolvare are `reference_date`, `timezone`, `jurisdiction_path`, `ruleset_version`, `facts_snapshot_hash`.
- **D5. Specific nu înseamnă automat superior.** Rangul juridic, competența, teritoriul, perioada și caracterul special se evaluează separat.
- **D6. Conflictul nu se ascunde.** Două claim-uri active incompatibile ⇒ `conflicting`; pentru reguli critice, `needs_confirmation` sau blocare.
- **D7. Fără claim, fără regulă critică.** Claim-ul include URL, emitent, locator, citat, perioadă, teritoriu, dată de acces, hash de snapshot și reviewer.
- **D8. Cache-ul nu produce verde fals.** Nu prelungește tacit valabilitatea peste `hard_expiry_at`.
- **D9. Utilizatorul păstrează controlul datelor.** Cont opțional; Document Vault local implicit.
- **D10. OCR nu înseamnă autenticitate.** Readiness verifică formă/lizibilitate/câmpuri, nu autenticitate, decât cu mecanism oficial.
- **D11. Nicio plată nu cumpără o rută falsă.** Partenerii nu schimbă cerințele și nu ascund autoservirea.
- **D12. Fricțiunea e justificată doar de risc.** Nu cerem date înainte să schimbe rezolvarea; fiecare întrebare își explică rostul.
- **D13. Limbajul este operațional.** Copy cu verb, acționabil din prima propoziție.
- **D14. Produsul funcționează și când statul nu funcționează.** Snapshot-uri aprobate, timeout, circuit breaker, fallback.
- **D15. Operațiunile de conținut au gate-uri de producție.** Publicarea unei reguli e privilegiată, separată de editare.
- **D16. Construim modular, nu teatral.** Modular monolith; separare doar la nevoie reală.
- **D17. Contractele sunt sursa de adevăr tehnic.** OpenAPI, JSON Schema, SQL, ADR.
- **D18. Fiecare rezultat trebuie explicat și reprodus.**
- **D19. Accesibilitatea este criteriu de acceptare.** Țintă WCAG 2.2 AA pe web, principii echivalente nativ.
- **D20. Măsurăm rezultatul, nu dependența.** North Star = rezultat administrativ fără drum evitabil.

## Test rapid pentru o decizie nouă

Respinsă/revizuită dacă răspunsul e „da": mută o decizie critică într-un LLM? publică obligații fără claim? cere cloud pentru documente implicit? ascunde ruta oficială? rezolvă conflictul fără să-l explice? colectează PII fără să schimbe traseul? crește timpul în aplicație fără a crește șansa de finalizare?
