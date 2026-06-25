# Research gaps — R1_ID_CARD_EXPIRED

| # | Gap | Status | De confirmat | Sursa tinta |
|---|---|---|---|---|
| GE1 | Cuantum sanctiune act expirat | conflicting | 40-80 lei vs 500-1000 lei intre SPCLEP-uri | textul consolidat OUG 97/2005, regim contraventional |
| GE2 | Locator exact art. 20 alin (1) CI provizorie + lista completa documente | partial | numar articol + lista oficiala | legislatie.just.ro 63354; HG 295/2021 |
| GE3 | Termen de eliberare a actului (zile lucratoare) la DEP Timisoara | not_started | termen oficial de procesare | primariatm.ro / DEP Timisoara |
| GE4 | Termen 2031 inlocuire buletine si gratuitate CEI pana in 2029 | needs_confirmation | confirmarea din Legea CEI / regulament UE | Monitorul Oficial, legislatie.just.ro |
| GE5 | Daca CEI cu valabilitate expirata are vreo regula distincta de CI simpla | not_started | regula specifica CEI la expirare | carteadeidentitate.gov.ro |

## Politica de conflict aplicata

`claim.exp.sanction_40_80` si `claim.exp.sanction_500_1000` sunt ambele `conflicting` cu `contradiction_claim_ids` reciproc. `rule.exp.sanction_conflict` blocheaza afisarea unui cuantum unic (efect critic) si emite avertisment, conform doctrinei D6. Nu se promoveaza in productie pana la rezolvarea GE1 cu sursa normativa.
