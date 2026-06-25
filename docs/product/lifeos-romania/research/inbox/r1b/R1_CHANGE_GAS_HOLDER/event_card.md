# Event Card — ro.life.change_gas_holder (life.change_gas_holder)

**Batch:** R1B-5  
**Status:** research_inbox (neaprobat)  
**Pilot:** `ro.tm.timisoara`  
**Accessed_at:** 2026-06-25

## Declanșator

„Vreau să trec contractul de gaze pe numele meu".

## Fapte cerute

| fact | tip | valori |
|---|---|---|
| `reason` | enum | `purchase` / `rent` / `inheritance_death` |
| `is_owner` | boolean | solicitantul e proprietar |

## Reguli cheie (sursă Premier Energy Furnizare)

- **Documente** (aceleași ca la contract nou): copia actului de identitate; **declarație pe propria răspundere** privind calitatea în care folosești imobilul (sau actul de proprietate); **poza contorului de gaz** cu seria și indexul; **codul locului de consum** (de pe factură).
- **Deces titular**: contractul de furnizare gaze naturale încetează prin deces (la fel ca la energie electrică); se reia/încheie contract nou.

## Canale (Timișoara)

- Furnizor: piață liberă (ex. Premier Energy Furnizare).
- Distribuție gaz: operatorul de distribuție din zona Timiș (de confirmat).
