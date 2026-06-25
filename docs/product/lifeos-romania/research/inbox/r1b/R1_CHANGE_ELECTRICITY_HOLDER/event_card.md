# Event Card — ro.life.change_electricity_holder (life.change_electricity_holder)

**Batch:** R1B-4  
**Status:** research_inbox (neaprobat)  
**Pilot:** `ro.tm.timisoara`  
**Accessed_at:** 2026-06-25

## Declanșator

„Vreau să trec contractul de curent pe numele meu".

## Fapte cerute

| fact | tip | valori |
|---|---|---|
| `reason` | enum | `purchase` / `rent` / `inheritance_death` |
| `has_active_supply` | boolean | există consum activ la locul de consum |
| `is_owner` | boolean | solicitantul e proprietar |

## Reguli cheie

- **Documente de bază** (aceleași ca la contract nou): act de identitate (copie+original), act care atestă dreptul locativ (proprietate/închiriere), **indexul contorului la zi**.
- **Deces titular**: contractul de furnizare **încetează** prin deces; pentru preluare se depun copie act identitate solicitant + copie act de deces al titularului.
- **Schimbarea furnizorului este gratuită** (ANRE) — interzisă perceperea de taxe pentru acest proces.
- Termen orientativ de intrare în vigoare a noului contract: ~21 zile (de confirmat).

## Canale (Timișoara / Banat)

- Furnizor: piață liberă (clientul alege furnizorul).
- Distribuție (Banat): **DEER — Distribuție Energie Electrică România, Sucursala Banat**.
