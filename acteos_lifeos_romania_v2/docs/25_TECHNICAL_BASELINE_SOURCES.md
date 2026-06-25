# 25 — Technical Baseline Sources (verified 25 June 2026)

Aceste versiuni sunt baseline-ul de bootstrap, nu promisiunea de a rămâne permanent pe ele. Lockfiles sunt normative în repo.

| Componentă | Baseline | Sursă oficială |
|---|---|---|
| Expo | SDK 56, include React Native 0.85 și React 19.2 | https://expo.dev/changelog/sdk-56 |
| React Native | 0.86 este release-ul upstream curent; Expo 56 folosește 0.85 | https://reactnative.dev/blog/2026/06/11/react-native-0.86 |
| Next.js | 16.2 | https://nextjs.org/blog/next-16-2 |
| FastAPI | 0.138.x | https://fastapi.tiangolo.com/release-notes/ |
| PostgreSQL | 18.4 current supported release line | https://www.postgresql.org/docs/current/ |
| OpenAPI | 3.1.1 pentru compatibilitatea tooling-ului | https://spec.openapis.org/oas/v3.1.1.html |
| Accessibility | WCAG 2.2 | https://www.w3.org/TR/WCAG22/ |
| Mobile security | OWASP MASVS 2.1.0 | https://mas.owasp.org/MASVS/ |
| Web/API security | OWASP ASVS 5.0.0 | https://owasp.org/www-project-application-security-verification-standard/ |
| Privacy by design | EDPB Guidelines 4/2019 | https://www.edpb.europa.eu/our-work-tools/our-documents/guidelines/guidelines-42019-article-25-data-protection-design-and_en |
| SIRUTA | Registrul INS | https://insse.ro/cms/ro/siruta |

## Decizie Expo vs React Native upstream

R1 folosește Expo SDK 56/RN 0.85, nu migrează imediat la RN 0.86 bare. Motivul este stabilitatea toolchain-ului cross-platform și accesul la modulele Expo. Upgrade-ul la următorul SDK se face prin ADR/PR dedicat după compatibilitatea bibliotecilor.
