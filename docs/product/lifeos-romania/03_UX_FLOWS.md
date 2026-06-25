# Fluxuri UX — LifeOS România

## 1. Principiu

Utilizatorul nu navighează un meniu de instituții sau proceduri. Pornește de la **„Ce s-a întâmplat?"** și primește un **graf de proceduri** pe care îl parcurge pas cu pas.

## 2. Fluxul principal: eveniment → graf

1. **Intrare.** Ecran cu un singur câmp: „Ce s-a întâmplat?" + exemple-cip (M-am mutat · Mi-am cumpărat o mașină · Mi s-a născut copilul · Mi-am pierdut actele).
2. **Interpretare.** Textul este mapat la un eveniment din catalogul controlat. Dacă e ambiguu, 1–3 întrebări scurte de dezambiguizare. Niciodată nu se inventează un eveniment inexistent în catalog.
3. **Context.** Județ/localitate, dată de referință și 3–6 fapte care ramifică graful (ai mașină? ai firmă? ai copii minori? ești PFA?).
4. **Planificare.** Orchestratorul produce graful de proceduri: ce se aplică, în ce ordine, ce depinde de ce.
5. **Harta evenimentului.** Ecran-hartă: pașii **deblocați acum**, cei **care urmează**, cei **condiționali**. Progres agregat.
6. **Procedură.** La intrarea într-un nod, se rulează traseul determinist al procedurii (checklist, termene, dovezi, canal oficial) — exact modelul anterior.
7. **Deblocare.** La finalizarea unui pas, dependenții se deblochează; harta se actualizează.
8. **Recalculare.** Schimbarea unui fapt, a jurisdicției sau publicarea unui bundle re-planifică graful; se arată diff-ul înainte de acceptare.

## 3. Standardul de ecran (nivel procedură)

Ce fac acum? · Până când? · Ce îmi trebuie? · Cum știu că am terminat? · Ce fac dacă nu merge? În zona extensibilă: de ce e necesar, sursă, data verificării, nivel de încredere, excepții.

## 4. Stări vizuale de încredere

- `verified` — verde, cu sursă și dată.
- `verified_with_local_gap` — verde cu notă: baza e verificată, lipsește o informație locală necritică.
- `needs_confirmation` — galben, cu întrebarea exactă.
- `conflicting` — portocaliu, fără verdict definitiv.
- `expired` — gri/roșu, blocat punctual (fail-closed pe clasa critică).

## 5. Accesibilitate

Acțiuni mari, propoziții simple, explicații audio opționale, export checklist pentru un membru al familiei, font scaling 200%.
