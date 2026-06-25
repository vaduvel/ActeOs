# 18 — Partner Neutrality Policy

## Principiu

Partenerii pot reduce munca utilizatorului, dar nu pot defini adevărul administrativ. Resolverul și ruta oficială sunt independente de contractele comerciale.

## Obligații

- ruta DIY oficială este afișată complet;
- costul și natura serviciului partenerului sunt clare;
- partenerul apare numai la cerere sau când complexitatea obiectivă justifică ajutorul;
- ranking-ul folosește criterii publice, nu comision;
- sponsorul nu poate modifica copy-ul legal sau readiness;
- clickurile comerciale sunt separate în analytics;
- partenerii au due diligence, reclamații și mecanism de suspendare;
- utilizatorul poate continua fără partener.

## Interzis

- „Pas obligatoriu: contactează partenerul” când nu este normativ;
- ascunderea adresei/linkului oficial;
- taxă de „urgentare” prezentată ca oficială;
- garantarea acceptării;
- colectarea documentelor de către partener fără disclosure și control;
- revânzarea leadurilor;
- modificarea statusului `ready` pe baza achiziției.

## UI

Cardul comercial are eticheta „Serviciu opțional oferit de un partener”, prețul sau mecanismul de ofertă, ce face și ce nu face, plus butonul „Continuă singur pe canalul oficial”.

## Audit

Orice integrare păstrează partner_id, disclosure_version, reason shown și event/step. Nu păstrăm PII în tracking. O creștere a recomandărilor fără creșterea complexității declanșează review.
