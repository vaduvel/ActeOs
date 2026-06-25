# 26 — Modelul de execuție Codex

## 1. De ce există acest strat

Documentația produsului definește adevărul despre ce construim. Modelul de execuție definește cum transformă un agent acel adevăr în cod fără să sară gate-uri, să piardă context sau să inventeze reguli administrative.

## 2. Cele patru niveluri

1. **`AGENTS.md` — constituția repo-ului.** Invariante, stack, reguli și interdicții.
2. **`PLANS.md` — convenția planurilor.** Când este obligatoriu un ExecPlan și ce trebuie să conțină.
3. **`codex/EXECUTION_PLAN.md` — planul viu.** Milestones P0–P15, progres, decizii, surprize, rollout și rezultate.
4. **`.agents/skills/` — proceduri specializate.** Intent authoring, rule authoring, vertical slice, research import și release certification.

Backlogul și phase prompts transformă fiecare milestone în stories și acceptance criteria. `IMPLEMENTATION_STATUS.md` este snapshotul scurt; ExecPlan-ul rămâne jurnalul operațional complet.

## 3. Bucla obligatorie a agentului

1. Citește instrucțiunile și planul.
2. Alege phase/story și skill-ul relevant.
3. Rulează baseline validation.
4. Actualizează contractele înaintea implementărilor dependente.
5. Implementează schimbarea minimă end-to-end.
6. Adaugă dovezi automatizate în aceeași schimbare.
7. Rulează gate-ul complet, nu doar testul local.
8. Actualizează planul, statusul și decision log-ul.
9. Produce PR summary cu scope, fișiere, teste, riscuri și rollback.

## 4. Reguli anti-derapaj

- Agentul nu declară „done” pe baza existenței fișierelor.
- Nu avansează faza dacă gate-ul anterior este roșu.
- Nu ascunde gap-urile prin hardcode sau copy generic.
- Nu schimbă simultan contract, runtime și UI fără compatibilitate și test end-to-end.
- Nu transformă research inbox în adevăr de producție.
- Nu creează ADR retroactiv după implementarea unei deviații majore.

## 5. Skill selection

| Situație | Skill obligatoriu |
|---|---|
| claim/rule/ruleset/deadline/channel | `acteos-rule-authoring` |
| journey cap-coadă contract→mobile | `acteos-vertical-slice` |
| raport/PDF/dataset intră în pipeline | `acteos-research-import` |
| release/ruleset activation/migration | `acteos-release-certification` |

Dacă două skill-uri se aplică, se urmează ambele și se unifică dovezile în același ExecPlan.

## 6. Definition of execution-ready

O fază este execution-ready când are:

- outcome utilizator și non-scope;
- stories și dependențe;
- contracte/scheme suficiente;
- acceptance criteria testabile;
- fixtures permise;
- failure states și recovery;
- privacy/security/a11y constraints;
- rollout/rollback;
- comenzi de validare;
- owner și gate explicit.

Acest pachet îndeplinește aceste condiții ca baseline; implementarea trebuie să mențină documentele vii pe măsură ce realitatea tehnică este confirmată.

- Intent catalog/search changes: `.agents/skills/acteos-intent-authoring/SKILL.md`.
