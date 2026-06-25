# START HERE - LifeOS Romania

1. Citeste `15_CODEX_MASTER_PROMPT.md`.
2. Citeste `01_PRD.md`, `04_DOMAIN_MODEL.md`, `05_EVENT_RESOLVER_SPEC.md`, `06_RULE_ENGINE_SPEC.md`.
3. Implementeaza fazele din `16_PHASE_PROMPTS.md` in ordine P0-P12.
4. Nu sari peste contracte: `contracts/*.schema.json` si `09_API_SPEC.yaml` sunt sursa de adevar tehnica.
5. Nu inventa reguli administrative. Orice regula reala are nevoie de `source_claim_ids`. Datele R1 din seed sunt demo-safe daca nu sunt marcate altfel.
6. La finalul fiecarei faze actualizeaza `templates/IMPLEMENTATION_STATUS.template.md`.

Comanda conceptuala pentru Codex:

```text
Build LifeOS Romania exactly from this pack. Follow phases P0-P12. Keep AI out of runtime legal/admin decisions. Implement deterministic event and rule resolution. Use demo-mode seeds unless source claims are provided. Do not invent administrative requirements.
```
