| Check | Result |
|---|---|
| Validator | openapi-spec-validator 0.9.0 (OpenAPI 3.1 schema + semantic checks) |
| Validator errors | 0 |
| Operations / paths | 1122 / 1002 |
| Duplicate operationId | 0 |
| Equivalent templated paths (OpenAPI 3.1 §4.8.8) | 0 |
| POST without Idempotency-Key, documented alternative (State/nonce, If-Match, Event ID, envelope) | 9 |
| POST without Idempotency-Key and no alternative | 1 (POST /api/v2/mandates/{id}/simulate: read-only simulation; accepted, GAP-1206) |
| PUT/PATCH/DELETE without If-Match | 0 |
| Undeclared path parameters | 0 |
| Operations without security requirement | 0 |
| Anonymous access outside public/BFF namespaces | 0 |
| Side-effect class X without PDP (P, D or P+D) | 0 |
| Version prefixes | v1: 988, bff: 10, oauth: 3, scim: 16, status: 1, v2: 93, hooks: 8, .well-known: 2, agent: 1 |
| WebSocket streams kept out of OpenAPI (x-websockets) | 1 |
