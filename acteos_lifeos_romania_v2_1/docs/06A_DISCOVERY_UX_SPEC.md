# 06A — Discovery UX Specification

## 1. Obiectiv

Discovery trebuie să ducă un utilizator de la formularea lui naturală la un intent canonic în maximum trei interacțiuni, fără să îi ceară să cunoască instituția, formularul sau terminologia juridică.

## 2. Home — stări

### Fără cazuri active

- headline: `Ce vrei să rezolvi?`;
- search field persistent;
- 4–6 quick actions publicate;
- categorii;
- explicație scurtă: `Îți spunem pașii, actele și canalul oficial.`

### Cu cazuri active

- `Astăzi` / deadline alerts înaintea discovery;
- `Continuă de unde ai rămas`;
- apoi search și categorii.

### Offline

- search local și categorii disponibile;
- rezultate marcate cu versiunea catalogului local;
- pornirea traseului permisă numai dacă ruleset-ul necesar există local ori API-ul este disponibil;
- mesaj clar, fără spinner infinit.

## 3. Search interaction

- autofocus numai când utilizatorul apasă căutarea;
- minimum 2 caractere, cu excepția abrevierilor aprobate;
- debounce 150–250 ms pentru API, zero pentru index local;
- taste și voice input converg în același query model;
- rezultatele apar sub câmp, nu într-un chat obligatoriu;
- fiecare rezultat este accesibil cu screen reader și touch target minimum 44 px.

## 4. Result card

Conține:

1. title;
2. outcome scurt;
3. categorie;
4. disponibilitate teritorială, numai dacă relevantă;
5. `De ce apare` pentru debugging intern, nu obligatoriu public;
6. CTA `Alege`.

Nu afișează scor numeric, probabilitate de acceptare sau badge de „AI”.

## 5. Disambiguation sheet

Se folosește când rezultatele sunt apropiate. Titlu: `Care dintre acestea vrei să rezolvi?`. Maximum trei opțiuni și un buton `Niciuna dintre acestea`.

## 6. Category browse

- grid/list accesibil de pe Home;
- categorie → intenturi populare + toate intenturile;
- search scoped opțional;
- deep-link stabil către categorie și intent;
- ordinea nu poate fi cumpărată de parteneri.

## 7. Intent detail înainte de start

Afișează:

- ce rezultat urmărește;
- pentru cine este;
- ce informații inițiale vor fi cerute;
- dacă traseul este disponibil în localitatea selectată;
- stare de research/availability fără a expune jargon intern;
- CTA `Începe`.

## 8. Failure states

- query prea scurt;
- zero rezultate;
- catalog indisponibil;
- intent cunoscut, dar traseu nepublicat în jurisdicție;
- intent retras;
- semantic fallback indisponibil;
- incompatibilitate catalog local/API.

Fiecare stare are recovery concret: reformulează, explorează categoria, schimbă localitatea, verifică mai târziu sau trimite gap feedback.

## 9. Copy rules

Folosim: `Ce vrei să rezolvi?`, `Caută un act sau o procedură`, `Alege rezultatul potrivit`, `Nu găsesc ce caut`.

Evităm: `Descrie evenimentul de viață`, `Inițiază speța`, `Selectează nomenclatorul`, `Clasificare AI`.

## 10. E2E obligatoriu

1. `buletin expirat` → intent exact → start case;
2. `schimb buletin` → disambiguare expirare/adresă/pierdere;
3. `cazier` → disambiguare;
4. `pasaport copil` fără diacritice → intent minor passport;
5. navigare Home → Auto → înmatriculare;
6. zero result → categorie + feedback;
7. offline exact alias;
8. screen reader și font scaling;
9. query sensibil nu ajunge în telemetry;
10. intent nepublicat este exclus.
