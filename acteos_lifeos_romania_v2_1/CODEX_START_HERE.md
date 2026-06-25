# Codex — Start Here

Acesta nu este un prompt de tip „construiește-mi aplicația”. Este contractul de execuție al proiectului.

## Înainte de orice modificare

1. Citește `AGENTS.md` integral.
2. Citește `PLANS.md` și planul viu `codex/EXECUTION_PLAN.md`.
3. Citește documentele în ordinea din `README.md`, inclusiv `docs/03A_DISCOVERY_INTENT_ATLAS.md`.
4. Verifică skill-urile repo-scoped din `.agents/skills/` și folosește-l pe cel relevant lucrării.
5. Rulează `python infra/scripts/validate_pack.py`.
6. Creează `IMPLEMENTATION_STATUS.md` din template.
7. Nu scrie cod pentru o fază ulterioară până când gate-ul fazei curente nu este verde.
8. După fiecare batch semnificativ, actualizează `codex/EXECUTION_PLAN.md`: Progress, Surprises, Decision Log și Outcomes.

## Ce ai voie să inventezi

- structură internă de cod compatibilă cu documentele;
- nume de funcții private;
- teste suplimentare;
- implementări tehnice echivalente, dacă păstrează contractele.

## Ce nu ai voie să inventezi

- acte, taxe, termene, eligibilități, adrese, programe sau canale oficiale;
- integrare publică presupusă cu o instituție;
- autentificare/semnare prin ROeID fără acord și documentație confirmată;
- verdict de autenticitate al unui document numai din OCR;
- „verde” dacă o regulă critică este expirată, conflictuală sau fără dovadă.

## Mod de lucru

- un branch și un PR per fază;
- schimbări mici, testate și trasabile;
- OpenAPI și JSON Schema sunt contracte, nu sugestii;
- orice abatere arhitecturală cere ADR nou;
- după fiecare fază: teste, raport, fișiere schimbate, riscuri rămase;
- pentru intenturi/search folosește `acteos-intent-authoring`; pentru reguli, vertical slices, import de research și release, urmează skill-ul corespunzător din `.agents/skills/`.

Promptul complet se află în `codex/CODEX_MASTER_PROMPT.md`, iar planul viu în `codex/EXECUTION_PLAN.md`.
