# CODEX START HERE

## Misiune

Construiește platforma „Waze pentru birocrație” descrisă în acest pachet. Livrează cod funcțional, teste, migrații, documentație de operare și un istoric clar al deciziilor. Nu transforma produsul într-un chatbot de proceduri.

## Mod de lucru obligatoriu

1. Creează monorepo-ul și fișierul `IMPLEMENTATION_STATUS.md`.
2. Execută fazele din `16_PHASE_PROMPTS.md` în ordine.
3. La fiecare fază:
   - citește toate documentele relevante;
   - scrie un plan scurt în `IMPLEMENTATION_STATUS.md`;
   - implementează numai scope-ul fazei;
   - rulează format, lint, type-check, unit, contract și integration tests;
   - actualizează statusul, riscurile și comenzile de reproducere;
   - nu marchează faza completă dacă un gate este roșu.
4. Orice ambiguitate semnificativă produce un ADR în `docs/adr/`; nu este rezolvată prin presupunere ascunsă.
5. Orice deviație de la acest workbook trebuie justificată într-un ADR și nu poate încălca manifestul.

## Garduri de adevăr

- Nu inventa instituții, documente, termene, taxe, coduri de liceu, adrese sau URL-uri.
- Nu transforma fragmentele de test în seed de producție.
- Nu folosi text liber drept condiție executabilă.
- Nu folosi `eval`, `exec`, JavaScript expression evaluation sau SQL construit prin concatenare.
- Nu publica automat outputul LLM.
- Nu interpreta o fotografie ca dovadă de autenticitate.
- Nu face upload de documente fără consimțământ explicit și scope de retenție.

## Rezultatul minim acceptat la final

- `make bootstrap`, `make up`, `make migrate`, `make seed-verified`, `make test-all` funcționează dintr-un mediu curat.
- Android compilează în `debug` și `release` fără secrete hardcodate.
- API-ul pornește, expune OpenAPI și trece testele contractuale.
- Portalul curator compilează și poate parcurge fetch → diff → draft → review → publish → rollback.
- Motorul rezolvă deterministic fixture-urile de rutare și produce același `route_hash` pentru aceleași intrări.
- Regula publicată poate fi reconstituită prin `rule_bundle_hash`, `evaluated_at` și `facts_hash`.
- Utilizatorul poate parcurge end-to-end cele două trasee R1 fără date demo în producție.
- Documentele sunt analizate local implicit; serverul păstrează doar metadata dacă utilizatorul nu activează sincronizarea securizată.
- Auditul de securitate acoperă OWASP MASVS 2.1 și ASVS 5.0 la nivelul stabilit în workbook.
