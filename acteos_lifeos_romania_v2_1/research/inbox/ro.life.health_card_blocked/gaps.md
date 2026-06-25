# Research gaps — B06_HEALTH_CARD_BLOCKED

| id | subiect | status | de confirmat | sursă țintă | comportament motor |
|---|---|---|---|---|---|
| HCB-G1 | PIN uitat | needs_confirmation | procedura curentă de resetare/deblocare și documentele cerute | CNAS / CAS competentă | Nu oferi PIN implicit și nu invita la încercări repetate. |
| HCB-G2 | Adresa e-mail de helpdesk | needs_confirmation | adresa oficială neobfuscată și câmpurile mesajului | CNAS | Afișează telefonul verificat; e-mailul se confirmă din canal oficial. |
| HCB-G3 | Eroare cititor/PIAS | needs_confirmation | procedura furnizorului și codurile tehnice relevante | CNAS SIUI/PIAS | Nu eticheta automat cardul ca blocat. |
| HCB-G4 | Timp de rezolvare tichet | needs_confirmation | SLA și dovada finalizării | CNAS | Nu promite termen. |

## Politică aplicată

- Nicio taxă, listă de documente, adresă sau durată neconfirmată nu este transformată în efect automat.
- `needs_confirmation` blochează doar afirmația critică nesusținută; pașii naționali verificați pot rămâne vizibili.
- `verified_with_local_gap` păstrează regula națională și cere verificarea canalului local din afara pilotului.
