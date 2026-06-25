# UX Flows

## Home
Input principal: `Ce s-a intamplat?`

Chips initiale:
- M-am mutat
- Mi-am cumparat o masina
- Mi-am pierdut actele
- Mi s-a nascut copilul
- Vreau certificat fiscal
- Ma casatoresc
- Imi deschid un SRL

## Flow: M-am mutat
1. User introduce text.
2. App propune `life.moved` si cere facts minime.
3. App arata Event Map: CI, auto, taxe locale, utilitati, firma, scoala/medic optional.
4. User selecteaza obligatia `identity.change_domicile`.
5. App arata traseu + dosar + canal oficial.
6. User incarca documente pentru readiness.
7. App marcheaza `READY_TO_SUBMIT` sau probleme concrete.

## Flow: Am cumparat masina
Event map: local taxes, fiscal documents, insurance, vehicle registration/transcription, optional plates.

## Flow: Mi-am pierdut actele
Event map prioritizat: identity first, then travel/driver/vehicle/health. UI calm, urgent, fara jargon.
