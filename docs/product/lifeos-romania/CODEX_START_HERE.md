# CODEX START HERE — LifeOS România

## Misiune

Construiește **LifeOS România**: o platformă care pornește de la un **eveniment de viață** descris de utilizator în limbaj natural și produce graful complet, personalizat și verificat de obligații administrative (proceduri atomice cu pași, termene, dovezi și canale oficiale). Livrează cod funcțional, teste, migrații, documentație de operare și un istoric clar al deciziilor. Nu transforma produsul într-un chatbot care răspunde liber din internet.

## Modelul în trei straturi (obligatoriu de respectat)

1. **LifeEvent** — evenimentul de viață („m-am mutat", „am cumpărat o mașină"). Selectează și ordonează un set de proceduri.
2. **Intent / Procedură atomică** — unitatea rezolvată de motorul determinist (ex. `ro.identity.id_card.address_change`). Are surse, reguli, termene, cerințe.
3. **Orchestrator** — compune procedurile unui eveniment într-un graf cu dependențe și fapte (`facts`) partajate, fără a duplica logica motorului.

## Mod de lucru obligatoriu

1. Reutilizează monorepo-ul existent și `IMPLEMENTATION_STATUS.md`.
2. Execută fazele din `16_PHASE_PROMPTS.md` în ordine.
3. La fiecare fază: citește documentele relevante; scrie un plan scurt; implementează doar scope-ul fazei; rulează format, lint, type-check, unit, contract și integration tests; actualizează statusul, riscurile și comenzile de reproducere; nu marca faza completă dacă un gate este roșu.
4. Orice ambiguitate semnificativă produce un ADR; nu se rezolvă prin presupunere ascunsă.

## Garduri de adevăr

- Nu inventa instituții, documente, termene, taxe, coduri, adrese sau URL-uri.
- Nu transforma fixture-urile de test în seed de producție.
- Nu folosi text liber drept condiție executabilă.
- Nu folosi `eval`, `exec`, evaluare de expresii sau SQL prin concatenare.
- Nu publica automat output de LLM.
- Nu interpreta o fotografie ca dovadă de autenticitate.
- Nu compune un eveniment din proceduri neverificate marcându-l ca `verified`.
- Nu face upload de documente fără consimțământ explicit și scope de retenție.

## Reutilizare (nu porni de la zero)

Motorul de reguli, schemele, auditul, idempotența și criptarea existente se reutilizează. Stratul nou este `LifeEvent` + orchestratorul; restul se extinde, nu se rescrie.

## Rezultatul minim acceptat

- `make bootstrap`, `make up`, `make migrate`, `make seed-verified`, `make test-all` funcționează dintr-un mediu curat.
- API-ul pornește, expune OpenAPI și trece testele contractuale.
- Motorul rezolvă deterministic fixture-urile de rutare (același `route_hash` pentru aceleași intrări).
- Orchestratorul compune deterministic un eveniment din proceduri (același `event_plan_hash` pentru aceleași intrări).
- Utilizatorul poate parcurge end-to-end cel puțin un eveniment 🔥 din R1 fără date demo în producție.
- Documentele sunt analizate local implicit.
