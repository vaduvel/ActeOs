# Domain Model

## Core
- `LifeEventType`: tip stabil in taxonomie.
- `EventSession`: cazul utilizatorului.
- `Fact`: raspuns tipat care schimba traseul.
- `AdministrativeObligation`: obligatie generata de eveniment.
- `Journey`: procedura rezolvabila.
- `Step`: actiune in journey.
- `Requirement`: act/document/dovada.
- `SourceClaim`: dovada atomica.
- `Rule`: predicat executabil.
- `RuleBundle`: set versionat publicat.
- `RouteRun`: output determinist.
- `DocumentCheck`: verificare formala.
- `FreshnessIncident`: sursa expira/se schimba.

## State machine EventSession
`DRAFT -> NEEDS_FACTS -> ROUTE_READY -> IN_PROGRESS -> READY_TO_SUBMIT -> SUBMITTED -> COMPLETED | BLOCKED | CANCELLED`
