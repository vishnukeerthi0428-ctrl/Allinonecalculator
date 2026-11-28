| id | name | type | default | consumers | source |
|---|---|---|---|---|---|
| FE-01 | VITE_API_ORIGIN | HTTPS URL | https://api.{zone}.{domain} | website, admin | Part 11.5a |
| FE-02 | VITE_ZONE | IN\|EU | per Vercel project | website, admin | DEC-772 |
| FE-03 | VITE_APP_SURFACE | website\|admin | per project | website, admin | ADR-006 |
| FE-04 | VITE_SENTRY_DSN | public DSN | none | website, admin | ADR-025 |
| FE-05 | VITE_BUILD_SHA | string | CI | website, admin | Part 4.3 |
| FE-06 | VITE_DEFAULT_LOCALE | BCP-47 | en-IN (IN) / en-GB (EU) | website, admin | DEC-776 |
