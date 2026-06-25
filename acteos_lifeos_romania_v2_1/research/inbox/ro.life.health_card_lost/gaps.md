# Research gaps — B06_HEALTH_CARD_LOST

| id | subiect | status | de confirmat | sursă țintă | comportament motor |
|---|---|---|---|---|---|
| HCL-G1 | Contul exact de plată CAS Timiș | needs_confirmation | IBAN, beneficiar, explicație și metode curente | site-ul oficial CAS Timiș | Afișează suma națională, nu inventa contul. |
| HCL-G2 | Adresa e-mail și limitele tehnice CAS Timiș | needs_confirmation | e-mail funcțional, format și mărime fișiere | CAS Timiș | Permite selectarea e-mail numai cu confirmare locală. |
| HCL-G3 | Termenul de emitere/livrare a duplicatului | needs_confirmation | durata procedurală curentă | CNAS / CAS Timiș | Nu promite o dată de primire. |
| HCL-G4 | Documente schimbare nume | needs_confirmation | actul de stare civilă și forma cerută | CAS competentă / Ordinul 98/2015 consolidat | Păstrează cererea, CI, plata și returnarea cardului; cere confirmarea documentului suport. |
| HCL-G5 | Valabilitatea cardului 5 vs 7 ani | conflicting | textul normativ consolidat și actualizarea paginilor CNAS | HG 900/2012 consolidată / CNAS | Blochează durata unică. |

## Politică aplicată

- Nicio taxă, listă de documente, adresă sau durată neconfirmată nu este transformată în efect automat.
- `needs_confirmation` blochează doar afirmația critică nesusținută; pașii naționali verificați pot rămâne vizibili.
- `verified_with_local_gap` păstrează regula națională și cere verificarea canalului local din afara pilotului.
