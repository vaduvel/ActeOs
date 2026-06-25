# 02 — Product Doctrine

Doctrina este constituția produsului. Backlogul, designul, tehnologia și monetizarea se schimbă; aceste reguli se schimbă numai prin decizie explicită și versiune majoră.

## D1. Intrarea este evenimentul de viață

Interfața principală întreabă „Ce s-a întâmplat?” sau „Ce vrei să rezolvi?”. Instituția, formularul și actul sunt rezultate ale rezolvării, nu condiții pentru a începe. Căutarea după procedură rămâne utilă ca funcție secundară pentru utilizatorii avansați.

## D2. Traseul este o concluzie executabilă

Un traseu conține pași ordonați, prerechizite, termene, acte, costuri unde sunt confirmate, canale, dovezi de finalizare și căi de recuperare. O listă de linkuri nu este un traseu.

## D3. Runtime-ul critic este determinist

Eligibilitatea, includerea unui act, calculul termenului, blocarea unui pas și starea de pregătire sunt produse de reguli tipate. Un LLM poate propune candidatul de eveniment, poate extrage câmpuri din text și poate explica rezultatul, dar nu poate modifica rezultatul motorului.

## D4. Adevărul este temporal și teritorial

Orice rezolvare are cel puțin:

- `reference_date`;
- `timezone`;
- `jurisdiction_path`;
- `ruleset_version`;
- `facts_snapshot_hash`.

Afirmația „același input produce același traseu” este adevărată numai pentru aceeași dată, aceeași jurisdicție și aceeași versiune de reguli.

## D5. Specific nu înseamnă automat superior

O instrucțiune locală se aplică numai dacă emitentul este competent și nu contrazice o normă superioară obligatorie. Resolverul nu folosește simpla regulă „instituția concretă bate legea”. Rangul juridic, competența, teritoriul, perioada și caracterul special sunt evaluate separat.

## D6. Conflictul nu se ascunde

Dacă două claim-uri active produc obligații incompatibile și conflictul nu poate fi rezolvat determinist, starea este `conflicting`. Pentru o regulă critică, traseul devine `needs_confirmation` sau este blocat la pasul afectat. UI explică exact ce trebuie confirmat și pe ce canal.

## D7. Fără claim, fără regulă critică

Eligibilitatea, termenul, taxa, actul obligatoriu, forma acceptată și criteriul de departajare nu pot fi publicate fără dovadă atomică. Claim-ul include URL, emitent, locator, citat, perioadă, teritoriu, dată de acces, hash de snapshot și reviewer.

## D8. Cache-ul nu produce verde fals

Cache-ul poate menține disponibilă o adresă sau o explicație. Nu poate prelungi tacit valabilitatea unui termen, act obligatoriu sau criteriu critic peste `hard_expiry_at`. Când sursa este indisponibilă, politica de prospețime decide `warn`, `needs_confirmation` sau `block`.

## D9. Utilizatorul păstrează controlul datelor

Experiența de bază poate funcționa fără cont. Profilul, familia, activele și sincronizarea sunt opționale. Document Vault este local implicit; încărcarea cloud necesită alegere separată, scop clar și retenție configurabilă.

## D10. OCR nu înseamnă autenticitate

Readiness poate verifica tip, lizibilitate, câmpuri, coerență, expirare, pagini și semnături vizibile. Nu afirmă că documentul este autentic decât dacă există un registru sau un mecanism oficial autorizat care confirmă aceasta.

## D11. Nicio plată nu cumpără o rută falsă

Partenerii pot oferi ajutor. Nu pot schimba cerințele, ascunde autoservirea, cumpăra primul loc în pașii legali sau transforma complexitatea în mod artificial. Comisionul este separat de logica rutei și auditat.

## D12. Fricțiunea este justificată numai de risc

Nu cerem cont, CNP, adresă completă sau fotografie de act înainte de momentul în care acestea schimbă rezolvarea. Fiecare întrebare explică de ce este necesară. Faptele sensibile pot fi marcate „prefer să nu răspund”, iar traseul coboară în încredere în loc să forțeze colectarea.

## D13. Limbajul este operațional

Copy-ul începe cu verb și spune ce urmează. Termenii juridici sunt păstrați unde contează, apoi explicați. Evităm formulări precum „în vederea efectuării demersurilor necesare”. Utilizatorul trebuie să poată acționa după prima propoziție.

## D14. Produsul trebuie să funcționeze și când statul nu funcționează

Sursele externe sunt tratate ca dependințe instabile. Traseele publicate se bazează pe snapshot-uri aprobate. Conectorii au timeout, circuit breaker, cache și fallback controlat. Indisponibilitatea portalului nu corupe ruleset-ul și nu șterge progresul local.

## D15. Operațiunile de conținut au gate-uri de producție

Un release de aplicație nu este complet dacă dashboardul de rule rot este roșu. Researcherul, curatorul și reviewerul au roluri și SLA-uri. Publicarea unei reguli este o operațiune privilegiată, separată de editare.

## D16. Construim modular, nu teatral

R1 este un modular monolith cu limite clare. Nu împărțim motorul în microservicii pentru prestigiu. Separăm procese numai când există nevoie de scalare, securitate sau ciclu de viață distinct.

## D17. Contractele sunt sursa de adevăr tehnică

OpenAPI, JSON Schema, SQL migrations și ADR-urile acceptate sunt normative pentru cod. Exemplele prose ajută înțelegerea, dar nu pot contrazice contractul.

## D18. Fiecare rezultat trebuie explicat și reprodus

Pentru orice traseu istoric trebuie să putem reconstrui:

- faptele folosite;
- regulile evaluate;
- claim-urile invocate;
- pașii incluși/excluși și motivul;
- versiunea motorului;
- data și jurisdicția.

## D19. Accesibilitatea este criteriu de acceptare

Nu folosim culoarea ca unic semnal. Textul se mărește fără tăiere. Ordinea focusului este corectă. Erorile sunt asociate câmpului. Acțiunile critice nu depind de gesturi ascunse. Copy-ul este testat inclusiv cu utilizatori cu alfabetizare digitală redusă.

## D20. Măsurăm rezultatul, nu dependența

North Star nu este timpul în aplicație. Este rezultatul administrativ obținut fără drum evitabil, împreună cu acoperirea și prospețimea regulilor. Un utilizator care închide aplicația după 90 de secunde cu următorul pas clar este succes.

## Test rapid pentru o decizie nouă

O propunere este respinsă sau revizuită dacă răspunsul „da” apare la oricare dintre întrebări:

- mută o decizie critică din engine într-un LLM?
- publică obligații fără claim?
- necesită cloud pentru documente implicit?
- ascunde ruta oficială gratuită?
- rezolvă conflictul fără să îl poată explica?
- colectează PII fără să schimbe traseul?
- crește timpul în aplicație fără să crească șansa de finalizare?
