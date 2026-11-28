| FR | Cap. | Requirement | Source | Story | Tests | Release | MoSCoW |
|---|---|---|---|---|---|---|---|
| FR-V12-R-001 | C1 | The system shall let R12 create up to 5 IdP connections (Okta, Entra ID, Google Workspace, generic SAML 2.0, generic OIDC) per tenant, each in state draft/testing/active/disabled | ENT-IDN-01; DEC-880 | US-01-ZR01 | TC-V12-R-001; M01 | Release 1 | Must |
| FR-V12-R-002 | C1 | The system shall reject metadata or SSO URLs that are not https and algorithms outside RS256/PS256/ES256 (SAML SHA-256+) | ENT-IDN-01 | US-01-ZR01 | TC-V12-R-002 | Release 1 | Must |
| FR-V12-R-003 | C1 | The system shall validate SAML signature, Audience, Destination, InResponseTo, NotOnOrAfter (60 s skew) and assertion-ID replay; OIDC iss, aud, azp, nonce, exp and PKCE | ENT-IDN-01; ADR-255 | US-01-ZR01 | TC-V12-R-003; M01 | Release 1 | Must |
| FR-V12-R-004 | C1 | The system shall require a successful test login before a connection becomes active | ENT-IDN-01 | US-01-ZR01 | TC-V12-R-004 | Release 1 | Must |
| FR-V12-R-005 | C1 | The system shall resolve the residency zone before processing personal data and issue sessions only from the tenant's zone | DEC-772; DEC-895 | US-01-ZR28 | TC-V12-R-005; M01 | Release 1 | Must |
| FR-V12-R-006 | C1 | The system shall verify email domains by DNS TXT, recheck daily and mark verification lost after 2 consecutive misses with a High alert, without locking users out | ENT-IDN-02 | US-01-ZR02 | TC-V12-R-006 | Release 1 | Must |
| FR-V12-R-007 | C1 | The system shall refuse SSO enforcement unless the connection has a verified domain and the tenant has a break-glass account (API and DB trigger) | ENT-IDN-02, 06 | US-01-ZR02 | TC-V12-R-007 | Release 1 | Must |
| FR-V12-R-008 | C1 | The system shall require 1–2 break-glass accounts with hardware keys and raise SEV3 with notification on every use | ENT-IDN-06 | US-01-ZR02 | TC-V12-R-008 | Release 1 | Must |
| FR-V12-R-009 | C1 | The system shall enforce tenant MFA policy that can only tighten the platform floor and require phishing-resistant factors for privileged roles, with WebAuthn step-up where the IdP amr does not prove it | ENT-IDN-04; SEC-03; DEC-077 | US-01-ZR02 | TC-V12-R-009; M01 | Release 1 | Must |
| FR-V12-R-010 | C1 | The system shall enforce session max 1–24 h and idle 5–120 min (privileged ≤ 12 h / ≤ 30 min) and revoke sessions within 60 s | ENT-IDN-05 | US-01-ZR02 | TC-V12-R-010 | Release 1 | Must |
| FR-V12-R-011 | C1 | The system shall expose a SCIM 2.0 service provider per zone (Users, Groups, Bulk ≤ 100, ServiceProviderConfig, Schemas, ResourceTypes) conforming to RFC 7643/7644 | ENT-IDN-03; DEC-881 | US-01-ZR03 | TC-V12-R-011; M02 | Release 1 | Must |
| FR-V12-R-012 | C1 | The system shall issue tenant SCIM tokens shown once, stored as hash, zone-bound, lifetime ≤ 397 days, revocable | ENT-IDN-03 | US-01-ZR03 | TC-V12-R-013 | Release 1 | Must |
| FR-V12-R-013 | C1 | The system shall grant no role for unmapped SCIM groups and require an approved group-to-role mapping (requester ≠ approver) | ENT-IDN-03; DEC-881 | US-01-ZR03 | TC-V12-R-012; M02 | Release 1 | Must |
| FR-V12-R-014 | C1 | The system shall on de-provisioning revoke sessions, API keys and OAuth clients of the user and re-queue approvals within 60 s of receipt | ENT-IDN-03 | US-01-ZR03 | TC-V12-R-015; M02 | Release 1 | Must |
| FR-V12-R-015 | C1 | The system shall measure end-to-end de-provisioning and alert when it exceeds 15 minutes (reconciliation sweep every 10 min) | ENT-IDN-03; DEC-881 | US-01-ZR03 | TC-V12-R-016 | Release 1 | Must |
| FR-V12-R-016 | C1 | The system shall apply RL-SCIM (60/min per token, Bulk ≤ 100, 1 MB) and return SCIM error types | ENT-IDN-03; ENT-API-03 | US-01-ZR03 | TC-V12-R-014 | Release 1 | Must |
| FR-V12-R-017 | C1 | The system shall offer a permission catalogue generated from the RBAC YAML with privileged and consequential flags | ENT-ACC-01 | US-01-ZR04 | TC-V12-R-017 | Release 1 | Must |
| FR-V12-R-018 | C1 | The system shall let R12 build tenant- or company-scoped custom roles only from permissions they hold | ENT-ACC-01 | US-01-ZR04 | TC-V12-R-018; M03 | Release 1 | Must |
| FR-V12-R-019 | C1 | The system shall reject any role or assignment that combines an SoD pair, at API, assignment trigger, SCIM mapping and run time | ENT-ACC-02; C2-T1; DEC-898 | US-01-ZR04 | M03 | Release 1 | Must |
| FR-V12-R-020 | C1 | The system shall maintain the SoD matrix of record (V12 four pairs plus eight DEC-898 pairs) as platform data | ENT-ACC-02; DEC-898 | US-01-ZR04 | TC-V12-R-019 | Release 1 | Must |
| FR-V12-R-021 | C1 | The system shall apply custom roles identically at API, worker and UI | ENT-ACC-01 acceptance | US-01-ZR04 | TC-V12-R-020 | Release 1 | Must |
| FR-V12-R-022 | C1 | The system shall require R10 co-approval for custom roles that hold any consequential permission | DEC-898; DEC-779 | US-01-ZR04 | M03 | Release 1 | Must |
| FR-V12-R-023 | C1 | The system shall run quarterly access recertification and suspend unconfirmed privileged permissions after 14 days | DEC-898; DEC-775 | US-01-ZR05 | TC-V12-R-020; AU-292 | Release 1 | Must |
| FR-V12-R-024 | C1 | The system shall stream audit and identity events to SIEM sinks (HTTPS, syslog-TLS, object storage; JSON/CEF; retention 1/3/7 years) and reject non-TLS endpoints | ENT-ACC-04 | US-01-ZR05 | TC-V12-R-019 | Release 1 | Must |
| FR-V12-R-025 | C1 | The system shall export the hash-chained audit as JSON Lines or CSV with a manifest and verify endpoint | ENT-ACC-03 | US-01-ZR05 | TC-V12-R-019 | Release 1 | Must |
| FR-V12-R-026 | C1 | The system shall require a ticket ID, tenant approval and expiry on every support access grant and show tenants every support session | ENT-ACC-05 | US-01-ZR05 | TC-V12-R-020 | Release 1 | Must |
| FR-V12-R-027 | C1 | The system shall monitor IdP certificates and metadata and alert at 30/14/7/1 days before expiry (AU-290) | ENT-IDN-01; DEC-880 | US-01-ZR29 | TC-V12-R-004; AU-290 | Release 1 | Must |
| FR-V12-R-028 | C1 | The system shall raise SEV3 security events for SSO replay and signature failures without storing assertion bodies | ENT-IDN-01 | US-01-ZR01 | M01 | Release 1 | Must |
| FR-V12-R-029 | C1 | The system shall keep the V12 C2 `identity_provider` shape as a compatibility view | Appendix C2 | US-01-ZR01 | TC-V12-R-001 | Release 1 | Must |
| FR-V12-R-030 | C1 | The system shall exclude break-glass accounts from SCIM changes and SSO enforcement | ENT-IDN-06 | US-01-ZR03 | M02 | Release 1 | Must |
| FR-V12-R-031 | C2 | The system shall issue scoped, expiring API keys `gek_<env>_<zone>_…`, shown once, stored as HMAC hash with prefix and last4, lifetime ≤ 365 days (DDL cap 397) | ENT-API-01 | US-20-ZR06 | TC-V12-R-021; M04 | Release 1 | Must |
| FR-V12-R-032 | C2 | The system shall support IPv4/IPv6 allowlists per key and per OAuth client | ENT-API-01 | US-20-ZR06 | M04 | Release 1 | Must |
| FR-V12-R-033 | C2 | The system shall rotate keys with ≤ 24 h overlap and revoke within 60 s | ENT-API-01 | US-20-ZR06 | TC-V12-R-022 | Release 1 | Must |
| FR-V12-R-034 | C2 | The system shall never create a scope for approve, send, publish, pay, sign, submit bids, set prices, roles or policies (DDL check) | DEC-883; DEC-779 | US-20-ZR06 | TC-V12-R-023; M04 | Release 1 | Must |
| FR-V12-R-035 | C2 | The system shall offer OAuth 2.0 client credentials with private_key_jwt (preferred) or client_secret_basic and 15-minute JWT access tokens bound to the zone | ENT-API-02; DEC-882 | US-20-ZR07 | TC-V12-R-024; M04 | Release 1 | Must |
| FR-V12-R-036 | C2 | The system shall reject replayed client assertions (jti) and assertions with exp > 60 s | ENT-API-02 | US-20-ZR07 | TC-V12-R-025 | Release 1 | Must |
| FR-V12-R-037 | C2 | The system shall support token revocation (RFC 7009) and client suspension | ENT-API-02 | US-20-ZR07 | TC-V12-R-026 | Release 1 | Must |
| FR-V12-R-038 | C2 | The system shall apply RL-KEY, RL-KEY-H and token-endpoint limits with 429, Retry-After and RateLimit headers and isolate noisy tenants | ENT-API-03 | US-20-ZR06 | M04 | Release 1 | Must |
| FR-V12-R-039 | C2 | The system shall accept bearer credentials only on the developer host of the credential's zone | DEC-882; DEC-772 | US-20-ZR06 | M04 | Release 1 | Must |
| FR-V12-R-040 | C2 | The system shall version the published API by URL major and give ≥ 12 months' notice with Deprecation/Sunset headers for breaking changes | ENT-API-04; DEC-646 | US-20-ZR09 | TC-V12-R-032 | Release 1 | Must |
| FR-V12-R-041 | C2 | The system shall sign webhooks with HMAC-SHA-256 over timestamp and raw body, ±300 s tolerance, with dual signatures during secret rotation | ENT-API-05 | US-20-ZR08 | TC-V12-R-027; M06 | Release 1 | Must |
| FR-V12-R-042 | C2 | The system shall deliver webhooks with 6 attempts within 24 h, disable on 410, and mark exhausted after attempt 6 | ENT-API-05 | US-20-ZR08 | TC-V12-R-028; M05 | Release 1 | Must |
| FR-V12-R-043 | C2 | The system shall require endpoint verification (challenge) before delivery | ENT-API-05; DEC-882 | US-20-ZR08 | M05 | Release 1 | Must |
| FR-V12-R-044 | C2 | The system shall keep a delivery log and allow replay for 30 days | ENT-API-05 | US-20-ZR08 | TC-V12-R-029 | Release 1 | Must |
| FR-V12-R-045 | C2 | The system shall block SSRF targets at registration and every delivery and never follow redirects | ENT-API-05; SEC | US-20-ZR08 | TC-V12-R-030 | Release 1 | Must |
| FR-V12-R-046 | C2 | The system shall send references and digests only in webhook payloads, never Restricted fields | ENT-API-05; DEC-883 | US-20-ZR08 | TC-V12-R-031 | Release 1 | Must |
| FR-V12-R-047 | C2 | The system shall publish the webhook event catalogue v1 with scope-based subscription | ENT-API-05 | US-20-ZR08 | TC-V12-R-031 | Release 1 | Must |
| FR-V12-R-048 | C2 | The system shall publish TypeScript, Python and Java SDKs generated from the OpenAPI with auth, pagination, retry, idempotency and webhook verify helpers | ENT-API-06; DEC-882 | US-20-ZR10 | TC-V12-R-033; M06 | Release 1 | Must |
| FR-V12-R-049 | C2 | The system shall run SDK contract tests against the sandbox in CI on every release | ENT-API-06 acceptance | US-20-ZR10 | TC-V12-R-033 | Release 1 | Must |
| FR-V12-R-050 | C2 | The system shall sign SDK releases with provenance | RECOMMENDATION-1097 | US-20-ZR10 | TC-V12-R-033 | Release 1 | Must |
| FR-V12-R-051 | C2 | The system shall host a developer portal with API reference, guides, changelog and sandbox Try-it, without personal data | ENT-API-07 | US-20-ZR09 | TC-V12-R-032 | Release 1 | Must |
| FR-V12-R-052 | C2 | The system shall revoke a key within 60 s of a leak report and notify R12 (AU-293) | DEC-882 | US-20-ZR06 | TC-V12-R-022; AU-293 | Release 1 | Must |
| FR-V12-R-053 | C2 | The system shall create sandbox tenants in the same zone with synthetic data only and simulator adapters only | ENT-DAT-04; DEC-899 | US-20-ZR09 | TC-V12-R-034 | Release 1 | Must |
| FR-V12-R-054 | C2 | The system shall promote configuration from sandbox to production as a reviewed revision (requester ≠ approver) | ENT-DAT-05 | US-20-ZR09 | TC-V12-R-035 | Release 1 | Must |
| FR-V12-R-055 | C2 | The system shall refuse promotions that contain sandbox credentials or personal data | ENT-DAT-04/05 | US-20-ZR09 | TC-V12-R-036 | Release 1 | Must |
| FR-V12-R-056 | C3 | The system shall implement every connector against the CF-01…12 contract with a manifest | ENT-INT-01 | US-18-ZR11 | TC-V12-R-037 | Release 1 | Must |
| FR-V12-R-057 | C3 | The system shall store OAuth tokens and API secrets only in the zone's vault and refresh them only in workers | ENT-INT-02 | US-18-ZR11 | TC-V12-R-038 | Release 1 | Must |
| FR-V12-R-058 | C3 | The system shall block production activation until security review, DPA, CJ-R15 transfer entry, channel registration and approval (requester ≠ approver) are present | ENT-INT-05 | US-18-ZR11 | TC-V12-R-039; M07 | Release 1 | Must |
| FR-V12-R-059 | C3 | The system shall block activation for any market whose jurisdiction rule pack is not counsel-approved | DEC-785; Part 11.15 | US-18-ZR11 | M07 | Release 1 | Must |
| FR-V12-R-060 | C3 | The system shall apply per-connector rate limits, backoff with jitter, circuit breaker and bulkheads | ENT-INT-03 | US-18-ZR11 | M07 | Release 1 | Must |
| FR-V12-R-061 | C3 | The system shall reconcile uncertain writes before any retry | ENT-INT-03 | US-18-ZR11 | M07 | Release 1 | Must |
| FR-V12-R-062 | C3 | The system shall show connector health, sync lag, error rate and breaker state with alerts | ENT-INT-04 | US-18-ZR11 | TC-V12-R-043 | Release 1 | Must |
| FR-V12-R-063 | C3 | The system shall sync contacts, accounts and opportunities bi-directionally with Salesforce, HubSpot and Zoho CRM in Release 1 | INT-01; DEC-884 | US-07-ZR12 | TC-V12-R-040; M07 | Release 1 | Must |
| FR-V12-R-064 | C3 | The system shall keep consent, suppression, approvals and mandates platform-owned; CRM opt-outs import as suppression | DEC-885 | US-07-ZR13 | TC-V12-R-040 | Release 1 | Must |
| FR-V12-R-065 | C3 | The system shall apply per-field policies platform_wins, crm_wins or newest_wins and queue conflicts | DEC-885 | US-07-ZR13 | TC-V12-R-041 | Release 1 | Must |
| FR-V12-R-066 | C3 | The system shall upsert by external ID and keep a link table per object | INT-01 | US-07-ZR12 | M07 | Release 1 | Must |
| FR-V12-R-067 | C3 | The system shall use change capture (CDC, webhooks, notifications) and fall back to cursor polling with gap repair | GC-08 | US-07-ZR12 | TC-V12-R-042; M07 | Release 1 | Must |
| FR-V12-R-068 | C3 | The system shall verify provider webhook authenticity and persist before acknowledging | CF-06 | US-07-ZR12 | TC-V12-R-041 | Release 1 | Must |
| FR-V12-R-069 | C3 | The system shall disable an installation after 3 consecutive 401 responses and create a reconnect task | CF-07 | US-07-ZR12 | M07 | Release 1 | Must |
| FR-V12-R-070 | C3 | The system shall send SMS in India only with registered DLT entity, header and template IDs and matching variables | INT-04; CJ-IN-06 | US-23-ZR14 | TC-V12-R-044; M07 | Release 1 | Must |
| FR-V12-R-071 | C3 | The system shall scrub promotional SMS and calls against the preference registry before dispatch | BRD 20; FSD 18 | US-23-ZR14 | M07 | Release 1 | Must |
| FR-V12-R-072 | C3 | The system shall send promotional SMS only within the stricter of the legal window and DEC-777 | DEC-777; CJ-IN-06 | US-23-ZR14 | TC-V12-R-045 | Release 1 | Must |
| FR-V12-R-073 | C3 | The system shall reconcile SMS delivery reports and handle STOP keywords deterministically | INT-04 | US-23-ZR14 | TC-V12-R-046 | Release 1 | Must |
| FR-V12-R-074 | C3 | The system shall store DLT registrations and templates per channel account with format checks | FSD 18 DLT and registry integration | US-23-ZR14 | TC-V12-R-044 | Release 1 | Must |
| FR-V12-R-075 | C3 | The system shall place calls only from numbers whose series matches the purpose (140 promotional, 160 service) | INT-05; CJ-IN-07 | US-22-ZR15 | TC-V12-R-048 | Release 1 | Must |
| FR-V12-R-076 | C3 | The system shall provide click-to-call and approved voice notifications through VoicePort with status reconciliation | INT-05; DEC-884 | US-22-ZR15 | TC-V12-R-049 | Release 1 | Must |
| FR-V12-R-077 | C3 | The system shall record calls only where the pack allows and consent is captured | DEC-782; Part 11.18 | US-22-ZR15 | TC-V12-R-050 | Release 1 | Must |
| FR-V12-R-078 | C3 | The system shall expose VoicePort to Part 11.18 AI voice workflows without bypassing its controls | DEC-782; GAP-1089 | US-22-ZR15 | TC-V12-R-050 | Release 1 | Must |
| FR-V12-R-079 | C3 | The system shall record a CJ-R15 transfer entry for providers processing outside the tenant's zone | DEC-772; CJ-R15 | US-18-ZR11 | TC-V12-R-047 | Release 1 | Must |
| FR-V12-R-080 | C3 | The system shall flag idle connectors (no successful call in 30 days) without auto-deleting them | GC-15 | US-18-ZR11 | AU-295 | Release 1 | Must |
| FR-V12-R-081 | C4 | The system shall deploy one Vercel project per surface per zone and attach each custom domain to its tenant's zone project only | DEC-786; DEC-886 | US-21-ZR16 | TC-V12-R-051; M08 | Release 1 | Must |
| FR-V12-R-082 | C4 | The system shall pin functions to bom1 (IN) or fra1 (EU) and block deployments that are not pinned | DEC-786 | US-21-ZR16 | TC-V12-R-052; M08 | Release 1 | Must |
| FR-V12-R-083 | C4 | The system shall restrict Edge Middleware to non-personal routing | DEC-786 | US-21-ZR16 | M08 | Release 1 | Must |
| FR-V12-R-084 | C4 | The system shall stream uploads to presigned in-zone storage without buffering bodies in functions | DEC-786 | US-21-ZR16 | M08 | Release 1 | Must |
| FR-V12-R-085 | C4 | The system shall never log request or response bodies, cookies, Authorization headers or token query strings in Vercel | DEC-786 | US-21-ZR17 | TC-V12-R-053; M08 | Release 1 | Must |
| FR-V12-R-086 | C4 | The system shall drain Vercel logs to the zone's collector with metadata fields only | DEC-786 | US-21-ZR17 | TC-V12-R-053 | Release 1 | Must |
| FR-V12-R-087 | C4 | The system shall forward only allowlisted headers to the origin | DEC-786 | US-21-ZR17 | TC-V12-R-055; M08 | Release 1 | Must |
| FR-V12-R-088 | C4 | The system shall enforce TLS on every hop and reject origin requests without X-Origin-Verify | DEC-786 | US-21-ZR17 | TC-V12-R-054; M08 | Release 1 | Must |
| FR-V12-R-089 | C4 | The system shall mark personal-data responses no-store and disable ISR/data cache on authenticated routes | DEC-786 | US-21-ZR17 | TC-V12-R-056 | Release 1 | Must |
| FR-V12-R-090 | C4 | The system shall keep database and provider secrets out of Vercel | DEC-786; SB-09 | US-21-ZR17 | AU-296 | Release 1 | Must |
| FR-V12-R-091 | C4 | The system shall list Vercel as a sub-processor under a DPA with 30-day change notice | DEC-786; ENT-CMP-04 | US-21-ZR17 | TC-V12-R-057 | Release 1 | Must |
| FR-V12-R-092 | C4 | The system shall disable Web Analytics/Speed Insights on authenticated surfaces | DEC-786 | US-21-ZR17 | AU-296 | Release 1 | Must |
| FR-V12-R-093 | C4 | The system shall check VD-01…12 daily and on every deployment (AU-296) | DEC-786 | US-21-ZR16 | AU-296 | Release 1 | Must |
| FR-V12-R-094 | C4 | The system shall keep a same-zone static fallback for Vercel outages | DR-04 | US-21-ZR16 | TC-V12-R-052 | Release 1 | Must |
| FR-V12-R-095 | C4 | The system shall document the edge-transit position in the IN and EU rule packs before EU onboarding | DEC-887; GAP-1088 | US-21-ZR17 | TC-V12-R-058 | Release 1 | Must |
| FR-V12-R-096 | C5 | The system shall run Supabase PITR at the longest retention offered in every zone | DEC-787 | US-21-ZR18 | TC-V12-R-059 | Release 1 gate | Must |
| FR-V12-R-097 | C5 | The system shall maintain an in-zone AWS standby by logical replication with WAL-G continuous archiving and daily base backups retained 35 days | DEC-787; FSD 38 V8 | US-21-ZR18 | TC-V12-R-060 | Release 1 gate | Must |
| FR-V12-R-098 | C5 | The system shall encrypt every backup with zone KMS keys and protect archives with Object Lock | FSD 38; ST-14 | US-21-ZR18 | TC-V12-R-061 | Release 1 gate | Must |
| FR-V12-R-099 | C5 | The system shall replicate archives only to the in-zone secondary region | DEC-772; CJ-R09 | US-21-ZR18 | M09 | Release 1 gate | Must |
| FR-V12-R-100 | C5 | The system shall sample replication lag and WAL archive age every 30 s and page at 10 min, SEV1 at 15 min (AU-297) | DEC-787 | US-21-ZR18 | TC-V12-R-062 | Release 1 gate | Must |
| FR-V12-R-101 | C5 | The system shall apply migrations to the standby in the same CI job as production | ADR-261 | US-21-ZR18 | TC-V12-R-060 | Release 1 gate | Must |
| FR-V12-R-102 | C5 | The system shall meet RPO ≤ 15 min for critical and growth data, proven by drills | DEC-V9-01; DEC-787 | US-21-ZR19 | M09 | Release 1 gate | Must |
| FR-V12-R-103 | C5 | The system shall meet growth RTO ≤ 120 min and critical RTO ≤ 4 h, measured | DEC-771; DEC-V9-01 | US-21-ZR19 | TC-V12-R-063; M09 | Release 1 gate | Must |
| FR-V12-R-104 | C5 | The system shall run restore drills at every release gate and quarterly per zone, alternating paths | DEC-787; OPT-TC-ST-14 | US-21-ZR19 | TC-V12-R-064 | Release 1 gate | Must |
| FR-V12-R-105 | C5 | The system shall run the PRV-01…08 verification pack after every restore | FSD 38 | US-21-ZR19 | TC-V12-R-065 | Release 1 gate | Must |
| FR-V12-R-106 | C5 | The system shall replay the erasure log after any restore | FSD 38 V8 | US-21-ZR19 | TC-V12-R-065 | Release 1 gate | Must |
| FR-V12-R-107 | C5 | The system shall pause external effects during failover until in-flight effects are reconciled | FSD 38 V8 | US-21-ZR19 | M09 | Release 1 gate | Must |
| FR-V12-R-108 | C5 | The system shall record drills with achieved RPO/RTO and evidence, and treat a miss as a release blocker | OPT-TC-ST-14 | US-21-ZR19 | TC-V12-R-066 | Release 1 gate | Must |
| FR-V12-R-109 | C5 | The system shall support tenant-level restore from logical dumps by reviewed script | DR-R4 | US-21-ZR19 | M09 | Release 1 gate | Must |
| FR-V12-R-110 | C5 | The system shall restrict restore credentials to two holders with audited break-glass | FSD 38 V8 keys | US-21-ZR18 | TC-V12-R-061 | Release 1 gate | Must |
| FR-V12-R-111 | C6 | The system shall route AI calls only to approved registry rows | AIX-02; DEC-788 | US-04-ZR22 | TC-V12-R-067; M10 | Release 1 | Must |
| FR-V12-R-112 | C6 | The system shall store per row provider, version, hosting, modality, zones, data classes, task classes, context limit, DPA/no-training/retention, EVAL status, red-team, security review, cost per accepted result, latency p95, licence, rollback and re-certification date | AIX-02; V12 16.2 | US-04-ZR20 | TC-V12-R-067 | Release 1 | Must |
| FR-V12-R-113 | C6 | The system shall refuse approval unless all seven V12 evidence items (and licence for open-weight) are present | V12 16.2; DEC-890 | US-04-ZR21 | TC-V12-R-068; M13 | Release 1 | Must |
| FR-V12-R-114 | C6 | The system shall require two distinct approvers (R10 and R01 or delegate) for each row and task class | DEC-890 | US-04-ZR20 | TC-V12-R-069; M13 | Release 1 | Must |
| FR-V12-R-115 | C6 | The system shall record the Founder approval of Claude Sonnet as the current primary (REG-002) | DEC-788 | US-04-ZR23 | TC-V12-R-070 | Release 1 | Must |
| FR-V12-R-116 | C6 | The system shall route EU tenants only to rows with EU processing and India tenants only to rows permitted for India | DEC-772; DEC-891 | US-04-ZR22 | M10 | Release 1 | Must |
| FR-V12-R-117 | C6 | The system shall allow masked personal data to self-hosted in-zone open-weight rows and never unmasked Personal or Restricted | DEC-788; MDL-S1 | US-04-ZR22 | M10 | Release 1 | Must |
| FR-V12-R-118 | C6 | The system shall restrict free third-party rows to Public and Internal-non-personal data, opt-in, default off | Invariant; DEC-890 | US-04-ZR22 | M10 | Release 1 | Must |
| FR-V12-R-119 | C6 | The system shall choose the cheapest row whose suite passes for workflow, language and data class | AIX-03 | US-04-ZR22 | M10 | Release 1 | Must |
| FR-V12-R-120 | C6 | The system shall escalate at most once within the remaining budget, else HOLD for a reviewer | AIX-03 | US-04-ZR22 | M10 | Release 1 | Must |
| FR-V12-R-121 | C6 | The system shall fall back only to a row with the same schema, zone and same-or-stricter class | V12 16.2 fallback | US-04-ZR22 | TC-V12-R-071; M10 | Release 1 | Must |
| FR-V12-R-122 | C6 | The system shall pin model and prompt per workflow, task, locale and zone with a rollback pointer | V12 16.2 rollback | US-04-ZR22 | TC-V12-R-071 | Release 1 | Must |
| FR-V12-R-123 | C6 | The system shall apply a kill switch per row, task or workflow within 60 s | AIX-20 | US-04-ZR22 | TC-V12-R-073 | Release 1 | Must |
| FR-V12-R-124 | C6 | The system shall re-certify rows every 12 months and suspend on DPA, region, price, regression or advisory triggers (AU-298) | DEC-890 | US-04-ZR21 | TC-V12-R-072 | Release 1 | Must |
| FR-V12-R-125 | C6 | The system shall register image, video and voice rows with modality and likeness/rights policy | DEC-788; DEC-892 | US-04-ZR21 | M13 | Release 1 | Must |
| FR-V12-R-126 | C6 | The system shall register an advanced tier MDL-L1 row and route complex synthesis to it only when approved | DEC-892; MDL-L1 | US-04-ZR23 | M10 | Release 1 | Should |
| FR-V12-R-127 | C6 | The system shall onboard new candidates through a 5% canary for 7 days per task class | DEC-890 | US-04-ZR23 | TC-V12-R-074 | Release 1 | Should |
| FR-V12-R-128 | C6 | The system shall explain each route decision (eligible rows, reasons) to R10 and auditors | AIX-03 | US-04-ZR22 | TC-V12-R-071 | Release 1 | Must |
| FR-V12-R-129 | C6 | The system shall fund and run the 111 EVAL suites as registry evidence | DEC-788; DEC-603 | US-04-ZR21 | AU-154 | Release 1 | Must |
| FR-V12-R-130 | C6 | The system shall expose the registry list API (V12 Appendix A AIX-02 operation) | AIX-02 | US-04-ZR20 | TC-V12-R-067 | Release 1 | Must |
| FR-V12-R-131 | C7 | The system shall enrol tenants in benchmarks only by explicit opt-in under contract clause BM-CL-1 | DEC-789; ASSUMPTION-1084 | US-17-ZR24 | TC-V12-R-075; M11 | Release 2 | Must |
| FR-V12-R-132 | C7 | The system shall apply withdrawal from the next period without recomputing published cells | DEC-789 | US-17-ZR24 | M11 | Release 2 | Must |
| FR-V12-R-133 | C7 | The system shall exclude Owner Portfolio startups unless R01 opts in per startup | DEC-893 | US-17-ZR24 | M11 | Release 2 | Must |
| FR-V12-R-134 | C7 | The system shall show benchmarks only to contributing tenants | DEC-893 BM-04 | US-17-ZR24 | M11 | Release 2 | Must |
| FR-V12-R-135 | C7 | The system shall compute per-tenant clipped contributions inside the tenant boundary under RLS | DEC-789 | US-17-ZR25 | TC-V12-R-076 | Release 2 | Must |
| FR-V12-R-136 | C7 | The system shall publish a cell only when k ≥ 10 contributing tenants | DEC-789 | US-17-ZR25 | TC-V12-R-077; M11 | Release 2 | Must |
| FR-V12-R-137 | C7 | The system shall suppress cells where one tenant exceeds 30% of events | DEC-893 | US-17-ZR25 | M11 | Release 2 | Must |
| FR-V12-R-138 | C7 | The system shall add Laplace noise at ε = 0.5 per metric per cell per month with a yearly cap of 6 and keep a privacy ledger | DEC-893 | US-17-ZR25 | TC-V12-R-078; M11 | Release 2 | Must |
| FR-V12-R-139 | C7 | The system shall compute benchmarks per zone and form global cells only from noised zone cells | DEC-772; DEC-893 | US-17-ZR25 | M11 | Release 2 | Must |
| FR-V12-R-140 | C7 | The system shall publish rates and durations only, rounded, with k bands | DEC-893 | US-17-ZR25 | TC-V12-R-079 | Release 2 | Must |
| FR-V12-R-141 | C7 | The system shall merge sparse cohorts up one level before suppression | DEC-893 BM-09 | US-17-ZR25 | TC-V12-R-080 | Release 2 | Must |
| FR-V12-R-142 | C7 | The system shall complete DPIA updates before the first publication in each zone | DEC-789 | US-17-ZR24 | TC-V12-R-080 | Release 2 | Must |
| FR-V12-R-143 | C8 | The system shall connect Django only as app_rw and Celery only as app_worker, both NOBYPASSRLS | DEC-778 | US-01-ZR26 | TC-V12-R-084; M12 | Sprint 0–1 | Must |
| FR-V12-R-144 | C8 | The system shall never place service_role or postgres credentials in API or worker runtime | DEC-778 | US-01-ZR27 | TC-V12-R-082; M12 | Sprint 0–1 | Must |
| FR-V12-R-145 | C8 | The system shall disable the Data API for application schemas and revoke anon/authenticated privileges | DEC-778 | US-01-ZR27 | TC-V12-R-081; M12 | Sprint 0–1 | Must |
| FR-V12-R-146 | C8 | The system shall use service_role only for CI migrations behind two-person, time-boxed break-glass with audit | DEC-778 | US-01-ZR27 | TC-V12-R-083; M12 | Sprint 0–1 | Must |
| FR-V12-R-147 | C8 | The system shall run normal migrations as app_migrator with SET ROLE app_owner | DEC-894 | US-01-ZR26 | M12 | Sprint 0–1 | Must |
| FR-V12-R-148 | C8 | The system shall set tenant, company, actor and zone context per transaction and fail closed when unset | DEC-778; SB-03 | US-01-ZR26 | TC-V12-R-084; M12 | Sprint 0–1 | Must |
| FR-V12-R-149 | C8 | The system shall force RLS on every tenant table and fail CI if any is missing | DEC-778 | US-01-ZR26 | TC-V12-R-085 | Sprint 0–1 | Must |
| FR-V12-R-150 | C8 | The system shall fail CI if any application role can bypass RLS | DEC-778 | US-01-ZR26 | TC-V12-R-085 | Sprint 0–1 | Must |
| FR-V12-R-151 | C8 | The system shall rename ge_* roles to canonical app_* names idempotently | DEC-894; CONFLICT-1092 | US-01-ZR26 | TC-V12-R-086 | Sprint 0–1 | Must |
| FR-V12-R-152 | C8 | The system shall restrict Supabase network access to zone NAT IPs and the CI runner | SB-05 | US-01-ZR27 | AU-292 | Sprint 0–1 | Must |
| FR-V12-R-153 | C8 | The system shall rotate database passwords every 90 days with dual logins | SB-09 | US-01-ZR26 | AU-293 | Sprint 0–1 | Must |
| FR-V12-R-154 | C8 | The system shall detect role, grant, policy and Data API drift nightly (AU-292) | DEC-778 | US-01-ZR27 | TC-V12-R-085 | Sprint 0–1 | Must |
| FR-V12-R-155 | C8 | The system shall alert SEV2 when a service_role or postgres session appears from an application subnet | DEC-778 | US-01-ZR27 | TC-V12-R-082 | Sprint 0–1 | Must |
