# Research gaps — B06_MEDICAL_CERTIFICATE_SCHOOL

| id | subiect | status | de confirmat | sursă țintă | comportament motor |
|---|---|---|---|---|---|
| MED-G1 | Reguli 2026–2027 pentru intrarea în colectivitate | needs_confirmation | documente, format și fereastră de valabilitate | Ministerul Educației / Ministerul Sănătății | Nu reutiliza automat ghidul 2025–2026. |
| MED-G2 | Revenire după boală | needs_confirmation | emitent, formular și durată de absență relevantă | Ministerul Sănătății / metodologia de asistență medicală școlară | Nu genera o adeverință obligatorie generică. |
| MED-G3 | Scutire educație fizică | needs_confirmation | tip document, medic competent, perioadă și circuit | Ministerul Sănătății / Ministerul Educației | Solicită cerința oficială curentă. |
| MED-G4 | Lista unităților A5 din Timiș | needs_confirmation | unități DSP-abilitate și date de contact curente | DSP Timiș | Atașează DSP ca punct de confirmare, nu inventa furnizori. |
| MED-G5 | Tarife în afara cabinetului școlar | needs_confirmation | dacă documentul solicitat este serviciu decontat sau cu plată | CNAS / furnizorul competent | Nu afișa gratuitate sau taxă fără temei specific. |

## Politică aplicată

- Nicio taxă, listă de documente, adresă sau durată neconfirmată nu este transformată în efect automat.
- `needs_confirmation` blochează doar afirmația critică nesusținută; pașii naționali verificați pot rămâne vizibili.
- `verified_with_local_gap` păstrează regula națională și cere verificarea canalului local din afara pilotului.
