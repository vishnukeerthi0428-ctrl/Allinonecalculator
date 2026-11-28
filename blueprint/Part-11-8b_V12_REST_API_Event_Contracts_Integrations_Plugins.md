# AI Growth Engine: Employee Sales & Marketing Automation
## Application Blueprint: PART 11 (Batch 11.8b), V12 REST API, Event Contracts, External Integrations and Plugin Optimization: Enhancements, Conflicts and Decisions

| Field | Value |
|---|---|
| Document | Part 11.8b: enhancements that bring the blueprint to a 100% match with FSD V12 ch. 25, 27, 28 and Appendices A/A2: adopted requirements, contract conventions, developer platform, 76 new operations with field-level contracts, error codes, idempotency and authorization, event contracts and outbound webhooks, connector framework, new adapters, plugin and FinOps decisions, API hosting under DEC-421, stories, tests, effort and cost; conflicts, decisions, persona review, tags and quality gate |
| Version | 1.0 · 28 Nov 2026 |
| Baseline | Part 11.8a (material and reconciliation); Part 3.2 standards §3.2.1, catalogue §3.2.2, events §3.2.3, adapters §3.2.4; Parts 3.5a/3.5b; Parts 7.4a/7.4b; Part 9.9a; Part 9.10 (DEC-417, DEC-418, DEC-420, DEC-421, DEC-422) |
| Roles applied | Principal API Architect · Integration Architect · Open-source/plugin FinOps strategist · API security lead · Business Systems Analyst · QA Lead · Security/Compliance Lead · FinOps Lead |

---

## 11.8.5 Enhancements

### 11.8.5.1 Requirements adopted and release mapping

**V12 phase mapping [ASSUMPTION-893].** FSD V12 ch. 39 defines R0 Foundations, R1 Private beta India (owned companies), R2 General availability India, R3 EU launch, R4 UK/Middle East/APAC, R5 Americas, and states that durations are not estimated. The blueprint maps them as follows until the Founder decides CONFLICT-886…888:

| V12 phase | Blueprint release | Window of record | Rationale |
|---|---|---|---|
| R0 Foundations | Release 1, W0–W1 | Day 1–45 | Core platform, CI/CD, SBOM |
| R1 Private beta India (owned companies) | Release 1, W2–W3 | to Release 1 go/no-go Fri 4 Jun 2027 (Day 180) | Owned startups are the Release 1 users (DEC-006) |
| R2 GA India | Release 2, W4–W5 | build Fri 2 Jul 2027 (Day 208); W5 exit Fri 23 Jul 2027 (Day 229) | External SaaS tenants arrive in Release 2 |
| R3 EU launch | W6 (Phase 2, separate approval) | Day ≈ 237–365 | Phase-2 budget ₹25.8–38.7 L not yet approved |
| R4, R5 | Year 2 and later | Not planned | Outside the approved horizon |

**Requirement register (V12 wording adopted literally).**

| FR | Requirement | Source | V12 acceptance | V12 phase → release | Realised by |
|---|---|---|---|---|---|
| FR-V12-H-001 | Scoped, expiring API keys; stored as hash, shown once; optional IPv4/IPv6 allowlist; rotation and revocation | ENT-API-01 (P0) | Plaintext never persisted (C2 hash only); revoked key returns 401 | R1 → Release 1 (CONFLICT-886) | API-V12-H-001…004; §11.8.5.4 |
| FR-V12-H-002 | OAuth 2.0 client-credentials for server integrations | ENT-API-02 (P1) | Token audience and scope verified; expired token rejected | R2 → Release 2 | API-V12-H-005…008 |
| FR-V12-H-003 | Rate limits per key and tenant with 429 and Retry-After | ENT-API-03 (P0) | Load test shows fair limits; noisy tenant isolated (AIX-16) | R1 → Release 1 (CONFLICT-886) | RL-KEY, RL-SCIM (§11.8.5.4) |
| FR-V12-H-004 | URL versioning and at least 12 months' deprecation notice for breaking changes | ENT-API-04 (P1) | Deprecation headers present; changelog published (W39) | R2 → Release 2 | DEC-646 |
| FR-V12-H-005 | Signed webhooks (HMAC-SHA256 + timestamp), replay protection, exponential retries for 24 h, delivery log | ENT-API-05 (P0) | Tampered or > 5-minute-old signature rejected by reference verifier | R1 → Release 1 (CONFLICT-886) | API-V12-H-009…014; §11.8.5.6; ADR-206 |
| FR-V12-H-006 | SDKs for TypeScript, Python and Java generated from the OpenAPI contract | ENT-API-06 (P2) | SDK contract tests pass against sandbox | R3 → W6 | RECOMMENDATION-903 |
| FR-V12-H-007 | Developer portal with API reference, guides and sandbox access | ENT-API-07 (P1) | Portal built from Appendix A/A2; examples executable in sandbox | R2 → Release 2 | §11.8.5.4 |
| FR-V12-H-008 | Enterprise operations of Appendix A2 (48, OpenAPI 3.1) are part of the contract | FSD 25 V12 note | Validated contract | R1–R3 | §11.8.4.3; API-V12-H-001…048 |
| FR-V12-H-009 | Appendix A component conventions (Error, Page, Record, Command, RunRequest, BusinessContext, PreflightRequest/Result; cursor/limit; Idempotency-Key) | Appendix A | Validated contract | R0 | DEC-641, DEC-642 |
| FR-V12-H-010 | One authoritative registry with alias and migration map; row-level source disposition index; no unreviewed historical endpoint auto-deployed | MT-36 (P0), REC-18 (P0) | Conflicting path/entity names detected; contract tests against versioned schemas | R0 | §11.8.5.2; DEC-640 |
| FR-V12-H-011 | Common run gateway with BusinessContext DTO, entitlement/config/approval/budget checks; run ID or hold reason; no duplicate effect | API-V2-*, MT-API-08, V4 runs, OPT-API-01 | 202 run; 400/403/409/422/429 | R1 → Release 1 | API-V12-H-068…073; ADR-208 |
| FR-V12-H-012 | AI governance routes: model registry, promotion requests with passing suites, prompt versions, eval suites and runs with denominators, red-team results, content screening (flags only), usage and cost per accepted result, budgets, kill switch | FSD 25 V8 (AIX-02/04/05/06/08/12/13/14/20) | Suite pass required; stop effective | R1 → Release 1 | API-V12-H-049…056 + existing |
| FR-V12-H-013 | Compliance routes: jurisdiction packs and rules, send preflight, consent ledger search, record and withdraw, suppressions, public DSAR intake, DSAR queue/verify/complete with legal-hold check, incident register with clocks and notifications, cookie consent with notice version | FSD 25 V8 (CJ-R01/02/04/05/07/08/12) | Rule-cited verdicts; clocks recorded | R1 → Release 1 | API-V12-H-057…062 + existing |
| FR-V12-H-014 | Tenant/company configuration contracts: applications (202 pending, no entitlement), company creation, scoped configuration graph, drafts with 409 stale, independent review, rollback as new draft with re-review, context options | MT-API-01…07 | Per row | R1 | Existing operations; API-043 semantics (§11.8.5.3) |
| FR-V12-H-015 | Business metrics with scoped dimensions, period, currency and approved rate version; native and converted totals; missing rates listed | MT-API-09 | Never sum currencies without rate | R1 | API-V12-H-064 |
| FR-V12-H-016 | Portfolio grants require owner authority and explicit aggregate scope; independent clients excluded by default | MT-API-10 | Grant/revoke versioned and audited | R1 | API-V12-H-063 |
| FR-V12-H-017 | Optimization routes: preflight, cost summary, health, feedback, customer value, private application drafts, model evaluations, operator conversion metrics | OPT-API-01…08 | Per row | R1–R2 | API-V12-H-065…068 + existing |
| FR-V12-H-018 | Connector framework with one adapter contract: auth, scopes, data mapping, events, limits, failure handling | ENT-INT-01 (P0) | Every connector passes contract tests in sandbox | R1 → Release 1 (CONFLICT-886) | CF-01…12 (§11.8.5.7) |
| FR-V12-H-019 | OAuth tokens and API secrets only in a vault, rotated, never in database rows or logs; short-lived scoped credentials | ENT-INT-02 (P0), SEC-04 (P0) | Secret scan and DB inspection find no credentials | R1 | AD-12; CF-03; TC-V12-H-085 |
| FR-V12-H-020 | Per-connector rate limits, backoff and circuit breaker; uncertain writes reconcile before retry | ENT-INT-03 (P1) | Provider outage test loses no events (M58) | R2 | Part 3.2 §3.2.7; CF-07 |
| FR-V12-H-021 | Connector health, sync lag and error dashboards with alerts | ENT-INT-04 (P1) | Health check and alert fire in staging | R2 | API-V12-H-074 |
| FR-V12-H-022 | Activation gate: security review, DPA, transfer basis (CJ-R15) and channel registration (DLT, WhatsApp templates); contact-data connectors blocked until DEC-V9-04 closes | ENT-INT-05 (P0) | Blocked state enforced | R1 → Release 1 (CONFLICT-886) | API-V12-H-038; CF-11; DEC-649 |
| FR-V12-H-023 | Connector catalogue INT-01…11 with category, examples, auth and scope rule | FSD 27 | — | R1–R3 | API-V12-H-037; AD-V12-H-01…11 |
| FR-V12-H-024 | A company may have multiple independent channel accounts; offering-market mapping and independent eligibility | MT-22 (P0) | Email and WhatsApp accounts for two markets preserved in handoff | R1 | CF-05; API-097/API-104 fields |
| FR-V12-H-025 | Scoped provider identity, credential reference and sender aliases; no secrets in HTML or public artifacts | MT-23 (P0) | Two senders under one channel; wrong-company account denied | R1 | API-104/105; CF-03 |
| FR-V12-H-026 | Incremental provider sync with webhooks, cursors, ETags and change windows; reconcile gaps and provider reset | GC-08 (P1) | Unchanged source incurs no full fetch; missed event repaired without duplicates | R2 | CF-08 |
| FR-V12-H-027 | Provider shortlist rationalization: capabilities, licence, privacy, support, TCO and fallback; evidence retained | GC-09 (P0) | Each release connector has an approved shortlist decision and owner; redundant candidates archived | R1 | §11.8.5.9 |
| FR-V12-H-028 | Bring-your-own-provider accounts with isolated credential references and clearly allocated fees, permissions, support and revocation | GC-10 (P1) | BYO tenant charges separate from platform charges; revocation blocks calls | R2 | API-V12-H-038 `ownership` |
| FR-V12-H-029 | Provider volume and tier planning; compare tiers, commitments and overages | GC-11 (P2) | Scenarios include unused commitments; purchasing approval required | R3 → W6 | API-V12-H-076 |
| FR-V12-H-030 | Self-service operations: setup checklist, connector diagnostics, knowledge-based troubleshooting with human escalation | GC-13 (P1) | Representative setup succeeds without staff; unresolved cases route to support | R2 | API-V12-H-075 |
| FR-V12-H-031 | Idle resource detection with safe cleanup and ownership review | GC-15 (P1) | Idle fixture flagged; active or retained resource never deleted automatically | R2 | API-V12-H-074 + CAP-X3-21 finding type |
| FR-V12-H-032 | Paid plugin replacement register VND-01…97 with decisions Replace / Retain OSS / Conditional external service / Defer-exclude | FSD 28 V9 | Every candidate disabled until benchmark, licence, legal and budget evidence | R0 | §11.8.4.6, §11.8.5.9 |
| FR-V12-H-033 | Contact-data vendors need a transfer-register entry (CJ-R15), a DPA and CJ-GL-01 compliance before activation (DEC-V9-04) | FSD 28 V9 | Activation blocked otherwise | R1 | CF-11; DEC-649 |
| FR-V12-H-034 | Cross-device application handoff preserves identity, hierarchy, services and revision; production uses an authenticated server-owned request with replay protection and idempotent revisions | MOB-16 | MOB-16-AT01 | R1 | DEC-658 |
| FR-V12-H-035 | Outbound event catalogue for webhook subscriptions, references and digests only | ENT-API-05; C2 `webhook_endpoint.events` | Subscribed types only | R1 | §11.8.5.6 |
| FR-V12-H-036 | Enterprise identity APIs: SSO (SAML 2.0, OIDC) per tenant, verified domains, MFA/session policy, break-glass, SCIM 2.0 users and groups | A2 Identity/SCIM; ENT-IDN-01…06 | Per ENT-IDN rows | R1 (SSO) / R2 (SCIM) (CONFLICT-887) | API-V12-H-015…028; ADR-207 |
| FR-V12-H-037 | Custom roles from resource × action permissions with SoD at build and run time | A2 Access; ENT-ACC-01/02 | Request+approve role cannot be saved | R2 (CONFLICT-887) | API-V12-H-029…032 |
| FR-V12-H-038 | SIEM streaming to HTTPS, syslog over TLS or object storage with retention 1/3/7 years | A2 Audit; ENT-ACC-04 | Test event delivered; non-TLS rejected | R2 | API-V12-H-033/034; AD-V12-H-07 |
| FR-V12-H-039 | Billing invoice preview with tax; tax determination per line from approved rules | A2 Billing; ENT-BIZ-01, ENT-GLB-05 | Invoice tax lines match approved rule table | R2 | API-V12-H-035/036 |
| FR-V12-H-040 | Customer-managed keys; synthetic-data sandboxes; reviewed configuration promotion | A2 Data; ENT-DAT-02/04/05 | Invalid key rejected; sandbox has no personal fields; self-approval rejected | R2 (sandbox) / R3 (keys) | API-V12-H-039…043 |
| FR-V12-H-041 | Locales list, operational incident declaration, public status summary, vulnerability findings | A2 Global/Operations/Security; ENT-GLB-01/02, ENT-OPS-02/03, ENT-SEC-03 | Status hosted independently; overdue critical blocks release | R1–R2 | API-V12-H-044…048 |

### 11.8.5.2 Contract authority, registry and route aliases (DEC-640)

| Rule | Specification | V12 source |
|---|---|---|
| R-1 Single registry | The Part 3.2 catalogue (+ Part 3.5b, Part 9.7b, this part) is the one registry. Each operation carries `operationId` = V12 operationId where V12 names one (e.g. `post_admin_ai_prompts`), `x-blueprint-op` = API-###, `x-v12-path`, `x-v12-tag` (SM-SVC-## or screen), `x-source-op` (SM-OP-### / SM-UX-API-## / V8 / MT-API / OPT-API / API-V2 / V4 / A2) | MT-36, REC-18, FSD 25 V5 "map operation IDs at contract review" |
| R-2 No duplicate mounting | A V12 path that is an alias of an approved blueprint path is **not** mounted a second time; the alias is recorded in the registry and the developer portal shows the approved path | FSD 25 V6 "avoid duplicate endpoints"; V5 "reuse approved paths if equivalent" |
| R-3 New namespaces only where V12 creates them | `/api/v2/workflow-runs…` (run gateway), `/scim/v2/…` (RFC 7644 fixed paths), `/oauth/token` and the developer host | API-V2-*, A2 SCIM, ENT-API-02 |
| R-4 Route aliases (served) | Only two V12 spellings are served as thin aliases because external clients will call them: **RA-V12-H-01** `GET /api/v2/public/services` → API-501 projection; **RA-V12-H-02** `POST /api/v2/public/enquiries` → API-212 (one lead per duplicate) | API-V2-CATALOG, API-V2-INTAKE |
| R-5 Disposition index | `final/coverage_v12/H_coverage.csv` column *action* holds the relation (Exact, Alias, Alias (prefix), Split, Approval, Partial, New, New (Part 3.5b)); exact matches are separated from semantic review exactly as REC-18 asks | REC-18 |
| R-6 Historical retention | Operations of the historical registry absent from Appendix A (30) stay implemented; Appendix A is not read as a deletion list | FSD 25 V5 "exact source operations retained" |
| R-7 CI gates | (a) duplicate method + path across namespaces → fail; (b) every alias target exists; (c) every Appendix A/A2 operationId appears exactly once as `operationId` or alias; (d) oasdiff breaking-change check per published namespace (DEC-646); (e) Schemathesis property tests per operation against the V12 component schemas (RECOMMENDATION-901) | MT-TC-MT-36 |

### 11.8.5.3 Wire convention amendments (DEC-641, DEC-642) and field amendments to existing operations

| Topic | Part 3.2 before | V12 (Appendix A) | Rule adopted | Effect on existing clients |
|---|---|---|---|---|
| List envelope | `{data[], page{next_cursor, prev_cursor, limit}, meta}` | `Page {items[], next_cursor: string|null}` | **`{items[], next_cursor, prev_cursor?, meta?}`** — `items` and `next_cursor` required; `meta.as_of`, `meta.total_estimate` optional | Generated TypeScript clients regenerated in Sprint 0; no external client exists yet |
| Page size | default 25, max 100 | `limit` 1…200, default 50 | **default 50, max 200**; exports stay async | RL-ADM unchanged; payload cap 1 MB still applies |
| Revision field | `revision` + `ETag: "r<revision>"` | `Record.version ≥ 1` | Wire name **`version`** (= database `revision`); ETag `"r<version>"` | Field rename in serializers |
| Concurrency on commands | `If-Match` mandatory | `Command.expected_version ≥ 0` in body | Both accepted; if both present they must be equal (else 400 `VERSION_PRECONDITION_MISMATCH`); stale → 409 `STALE_REVISION` | Additive |
| Command body | Operation-specific DTO | `Command {expected_version, payload, reason ≤ 2000}` | Operation-specific DTO **inside** `payload`; `reason` top-level where the operation records a reason | Additive wrapper for V12 clients; blueprint DTOs unchanged inside |
| Error envelope | RFC 9457 problem+json with `code`, `detail`, `errors[]`, `rule_ids`, `correlation_id` | `Error {code, message, correlation_id, field_errors{}}` | **Superset:** `code`, `message` (= `detail`), `correlation_id`, `field_errors` (map field → message key) always present; RFC 9457 members and `rule_ids`, `reasons`, `required_approval`, `retryable` retained | Additive |
| Response codes | 200/201/202/204/304/400/401/403/404/409/413/415/429/503 | Reads 200/304/400/403/404/409; commands 200/202/400/403/404/409 | Superset retained and declared on every operation; **422 `SCHEMA_INVALID`** added for DTOs validated against Appendix B JSON Schemas (run inputs) and SCIM schema errors; 400 stays for envelope/format errors | Additive |
| Security schemes | BFF cookie only for browsers; no bearer from browsers | `bearerAuth` JWT, global | Two schemes: `bffSession` (browser namespaces) and `bearerAuth` (developer host, SCIM, `/api/v2` token callers). Bearer tokens presented on browser ingress → 401 `WRONG_AUDIENCE` (DEC-643) | No browser change |
| Idempotency | `Idempotency-Key` + body hash | `x-idempotency: Idempotency-Key header required` | Unchanged; also required for API-key callers | — |
| Servers | Per namespace | `https://api.example.invalid` | Real hosts per §11.8.5.10 | — |

**Preflight DTO adopted for API-068 (`POST /api/v1/engagement/check`, V12 `POST /api/v1/compliance/preflight`).**

```json
{
  "request": {"market": "IN", "channel": "WhatsApp", "purpose": "Promotional",
              "contact_id": "0193…", "send_at_local": "2027-03-04T10:30:00+05:30",
              "template_id": "tpl_…", "ai_generated": true, "ai_disclosed": true},
  "result":  {"verdict": "HOLD",
              "reasons": [{"rule_id": "CJ-IN-08", "effect": "hold", "message": "eligibility.whatsapp_optin_missing"}],
              "pack_versions": {"IN": 7}}
}
```

`verdict ∈ {ALLOW, HOLD, REVIEW}`; HOLD and REVIEW never dispatch; the dispatch-time PDP recheck still runs (safety invariant). `market` enum IN/EU/UK/US is extended only when a pack is counsel-approved (ENT-CMP-08).

**Field and semantic amendments to existing operations (no new route).**

| Operation | Amendment | V12 source |
|---|---|---|
| API-043 `POST ~/admin/config-revisions/{id}/rollback` | Creates a **new draft revision** copying the referenced approved revision; requires review (API-541/539) before activation; no automatic restore | MT-API-06 |
| API-030 `POST ~/admin/startups` | Response adds `company_version`; 201 `state: "pending"`; scoped member grants stay separate (API-020/021) | MT-API-02 |
| API-097 / API-104 | Add `market_ids[]`, `offering_ids[]`, `ownership ∈ {platform, tenant_byo}`, `sender_aliases[]` (≤ 10); eligibility evaluated per channel account | MT-22, MT-23, GC-10 |
| API-102 `GET ~/admin/integrations/{id}/health` | Add `sync_lag_s`, `error_rate_1h`, `breaker_state`, `alert_state` | ENT-INT-04 |
| API-122 audit export | `format ∈ {jsonl, csv}`; count of exported rows equals filtered count; hash-chain segment proof included | ENT-ACC-03 |
| API-534 / API-535 exports | `format ∈ {jsonl, csv, parquet}`; `manifest_hash`; second approver ≠ requester (approval type `export`); link valid **7 days** | ENT-DAT-01 |
| API-137 / API-146 AI budgets | `soft_limit` (alert) and `hard_limit` (stop) per scope; V12 `PUT /api/v1/ai/budgets/{id}` is an alias of the revision update | AIX-13 |
| API-148 eval run detail | Add `denominator` per metric and `suite_id` | V8 eval-runs |
| API-077 jurisdiction packs | Add `status ∈ {draft, counsel_approved, retired}` and `legal_source` per pack | CJ-R01 |
| API-526 / API-515 invoices | Add `tax_lines[]`, `net_minor`, `tax_minor`, `total_minor` (= net + tax) | A2 billing; C2 `invoice` |
| API-128 incidents | Add `severity ∈ {SEV1…SEV4}`, `status ∈ {Investigating, Identified, Monitoring, Resolved}`, `status_message` | C2 `ops_incident` |
| API-503/504/507 applications | Accept the SM-APPLICATION-6 envelope as the application DTO; `revision` + `digest`; 409 on stale or provisioned change | MT-API-01, V4, MOB-16 |

### 11.8.5.4 Developer platform (ENT-API-01…07; ADR-205)

**Surfaces and authentication.**

| Surface | Host (DEC-421, §11.8.5.10) | Callers | Credential | Accepted on |
|---|---|---|---|---|
| Browser namespaces `public`, `portal`, `admin`, `bff-*` | Same origin as each SPA | Browsers | `__Host-` session cookie + CSRF (DEC-019) | Browser ingress only |
| Developer API (`/api/v1/…` published subset, `/api/v2/workflow-runs…`) | `api.<platform-domain>` | Tenant servers | API key `Authorization: Bearer gek_…` or OAuth JWT | Developer host only |
| OAuth token endpoint `/oauth/token` | `api.<platform-domain>` | Registered clients | `private_key_jwt` (preferred) or `client_secret_basic` | Developer host |
| SCIM `/scim/v2/…` | `api.<platform-domain>` | Tenant IdP | SCIM bearer token (hash stored) | Developer host |
| Provider hooks | `hooks.<platform-domain>` | Providers | Provider signatures | Hooks host |

**API key specification [ASSUMPTION-894].** Format `gek_<env>_<prefix8>_<secret43>` (secret = 32 random bytes, base62). Storage: `prefix`, `last4`, `key_hash = HMAC-SHA-256(pepper, secret)` (pepper in Secrets Manager, rotated yearly with dual-pepper verification); plaintext returned once with `Cache-Control: no-store`. Lookup by prefix, constant-time compare. Expiry ≤ 365 days (default 90); optional IPv4/IPv6 allowlist (CIDR); scopes required. Revocation effective ≤ 60 s. Keys are tenant-scoped and attributed to the creating user for audit; deprovisioning the user (SCIM) revokes keys they created unless re-assigned by R12 within 24 h.

**Scope registry (draft-only by design).**

| Scope | Grants | Never grants |
|---|---|---|
| `<resource>:read` for leads, organizations, deals, quotes, orders, invoices, meetings, runs, metrics, catalogue | Reads with the same field masks as the creator's least-privileged role | Restricted fields (contact data is masked unless the scope `contacts:read_unmasked` is approved by R10) |
| `leads:write`, `organizations:write`, `deals:write` | Create or update **records and drafts** | Sends, publishes, launches |
| `runs:create` | `POST /api/v2/workflow-runs` with `mode=draft`; `mode=execute` only for workflows whose consequential steps all stop at a human approval | Approval of any kind |
| `webhooks:read` | Delivery log of own endpoints | Endpoint creation (Admin only) |
| — (no scope exists) | — | Approve, send, publish, launch ads, sign, pay, submit bids, set prices, change roles, change policies: **consequential actions stay capped at L1 and require a human in the Admin UI** |

**Rate-limit classes added to Part 3.2 §3.2.1.7 [ASSUMPTION-896].**

| Class | Applies to | Default | Key | On exceed |
|---|---|---|---|---|
| RL-KEY | Developer API reads and writes | 300/min per key; 1,500/min per tenant (all keys and clients); burst 2× for 10 s; payload ≤ 1 MB | key, tenant | 429 `RATE_LIMITED` + `Retry-After` + `RateLimit-Policy`/`RateLimit` |
| RL-KEY-H | `/api/v2/workflow-runs` creation, exports | 10/min per key; 60/min per tenant; ≤ 3 concurrent runs per key | key, tenant | 429, or 202 queued |
| RL-SCIM | `/scim/v2/*` | 60/min per tenant token; bulk ≤ 100 operations | token | 429 (RFC 7644 `tooMany`) |
| Noisy-tenant isolation | All token callers | Per-tenant worker concurrency (BRL-AUT-06) and separate Valkey bucket namespace | tenant | Other tenants unaffected (AIX-16 acceptance, TC-V12-H-079) |

**Versioning (DEC-646).** Breaking changes to any **published** contract (developer API, public, portal, outbound webhook payloads, SCIM) need at least **12 months'** notice: `Deprecation` and `Sunset` headers, `Link rel="deprecation"`, changelog entry on the developer portal (W39) and an email to the owners of keys that called the operation in the last 90 days. Admin-only operations not published in the portal keep the release-coupled rule of Part 3.2 §3.2.1.3.

**SDKs and portal.** TypeScript and Python SDKs generated with openapi-generator (Apache-2.0, verify) from the published namespaces at R2; Java at R3 (RECOMMENDATION-903). The developer portal is a static site generated from the OpenAPI documents (Appendix A/A2 + this part) hosted as a separate Vercel project (no personal data), with "Try it" bound only to the **sandbox tenant** (API-V12-H-042, synthetic data, sandbox adapters). Contract tests of each SDK run against the sandbox in CI (ENT-API-06 acceptance).

```mermaid
sequenceDiagram
  participant T as Tenant server
  participant W as WAF on developer host
  participant G as Django developer API
  participant K as Key cache in Valkey
  participant P as Policy Decision Point
  T->>W: HTTPS request with Bearer API key
  W->>G: Forward if IP allowlist and size rules pass
  G->>K: Lookup by key prefix
  K-->>G: Hash, scopes, tenant, expiry, state
  G->>G: Constant-time HMAC compare and expiry check
  G->>G: Rate limit RL-KEY per key and tenant
  G->>P: Scope to RBAC mapping and object check
  P-->>G: Allow or deny with rule IDs
  G-->>T: 200, 202, 401 API_KEY_REVOKED, 403 or 429 with Retry-After
```

### 11.8.5.5 New operations (76) with field-level contracts

Columns follow Part 3.2 §3.2.2.2. New namespaces: `dev` (developer host token endpoint), `scim` (`/scim/v2`), `v2` (run gateway; Admin session or token), `status` (independent status host). New rate-limit classes RL-KEY, RL-KEY-H and RL-SCIM are defined in §11.8.5.4. Every mutating operation takes `Idempotency-Key` (and `If-Match` or `expected_version` where marked) per Part 3.2 §3.2.1.4–5; every response carries `X-Correlation-Id`; errors use the DEC-641 envelope and the Part 3.2 code catalogue plus the codes below.

**New error codes.** `API_KEY_REVOKED` (401), `API_KEY_EXPIRED` (401), `TOKEN_EXPIRED` (401), `INSUFFICIENT_SCOPE` (403), `IP_NOT_ALLOWED` (403), `SCHEMA_INVALID` (422), `VERSION_PRECONDITION_MISMATCH` (400), `GATE_INCOMPLETE` (403, activation gate), `CHECK_PENDING` (409, SSO or domain not yet verified).

| Op ID | Method | Path | NS | Purpose | V12 source | FR / screen | Auth / roles | Idempotent | SE | PDP | RL class | V12 phase |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| API-V12-H-001 | GET | `~/admin/developer/api-keys` | admin | List API keys of the tenant (prefix, last4, scopes, expiry, last used); never the secret | A2 GET /api/v1/api-keys; ENT-API-01 | FR-V12-H-001; A125 | R12, R11, R01 | Safe | R | — | RL-ADM | R1 |
| API-V12-H-002 | POST | `~/admin/developer/api-keys` | admin | Create scoped, expiring API key; plaintext returned exactly once | A2 POST /api/v1/api-keys; ENT-API-01 | FR-V12-H-001; A125 | R12 (≠ approver for write scopes); write scopes need R01 approval | Key | A | P | RL-ADM | R1 |
| API-V12-H-003 | POST | `~/admin/developer/api-keys/{id}/revoke` | admin | Revoke API key immediately | A2 POST /api/v1/api-keys/{id}/revoke; ENT-API-01 | FR-V12-H-001; A125 | R12, R01, creator | Key + If-Match | W | — | RL-ADM | R1 |
| API-V12-H-004 | POST | `~/admin/developer/api-keys/{id}/rotate` | admin | Rotate key: issue successor with the same scopes; old key valid for an overlap window | ENT-API-01 (rotation) | FR-V12-H-001; A125 | R12, creator | Key + If-Match | A | P | RL-ADM | R1 |
| API-V12-H-005 | POST | `/oauth/token` | dev | OAuth 2.0 client-credentials token for server integrations | ENT-API-02 | FR-V12-H-002 | Registered OAuth client (R19-type integration identity) | Yes | R | — | RL-AUTH | R2 |
| API-V12-H-006 | GET | `~/admin/developer/oauth-clients` | admin | List OAuth clients (client ID, scopes, key thumbprints, state) | ENT-API-02 | FR-V12-H-002; A125 | R12, R01 | Safe | R | — | RL-ADM | R2 |
| API-V12-H-007 | POST | `~/admin/developer/oauth-clients` | admin | Register OAuth client (JWKS URL or uploaded public key, scopes) | ENT-API-02 | FR-V12-H-002; A125 | R12; write scopes need R01 approval | Key | A | P | RL-ADM | R2 |
| API-V12-H-008 | POST | `~/admin/developer/oauth-clients/{id}/revoke` | admin | Revoke OAuth client and its issued tokens | ENT-API-02 | FR-V12-H-002; A125 | R12, R01 | Key + If-Match | W | — | RL-ADM | R2 |
| API-V12-H-009 | GET | `~/admin/developer/webhooks` | admin | List outbound webhook endpoints of the tenant | A2 GET /api/v1/webhooks; ENT-API-05 | FR-V12-H-005; A125 | R12, R11, R01 | Safe | R | — | RL-ADM | R1 |
| API-V12-H-010 | POST | `~/admin/developer/webhooks` | admin | Add outbound webhook endpoint (HTTPS URL, subscribed event types) | A2 POST /api/v1/webhooks; ENT-API-05 | FR-V12-H-005; A125 | R12, R11 | Key | W | P | RL-ADM | R1 |
| API-V12-H-011 | PATCH | `~/admin/developer/webhooks/{id}` | admin | Change events, disable/enable, or rotate signing secret with overlap | ENT-API-05 (rotation, disable) | FR-V12-H-005; A125 | R12, R11 | If-Match | W | P | RL-ADM | R1 |
| API-V12-H-012 | POST | `~/admin/developer/webhooks/{id}/test` | admin | Send signed test event to the endpoint | A2 POST /api/v1/webhooks/{id}/test | FR-V12-H-005; A125 | R12, R11 | Key | X | P+D | RL-ADM | R1 |
| API-V12-H-013 | GET | `~/admin/developer/webhook-deliveries` | admin | Delivery log: attempts, status codes, latency, next retry | A2 GET /api/v1/webhook-deliveries; ENT-API-05 | FR-V12-H-005; A125 | R12, R11, R15 | Safe | R | — | RL-ADM | R1 |
| API-V12-H-014 | POST | `~/admin/developer/webhook-deliveries/{id}/replay` | admin | Re-send an earlier event payload (same event_id, new delivery) | ENT-API-05 (delivery log, replay) | FR-V12-H-005; A125 | R12, R11 | Key | X | P+D | RL-ADM | R1 |
| API-V12-H-015 | GET | `~/admin/identity/sso` | admin | Read tenant SSO configuration | A2 GET /api/v1/identity/sso; ENT-IDN-01 | FR-V12-H-036; A122 | R12, R01, R15 | Safe | R | — | RL-ADM | R1 |
| API-V12-H-016 | PUT | `~/admin/identity/sso` | admin | Update SSO configuration (draft until tested; enforcement guarded) | A2 PUT /api/v1/identity/sso; ENT-IDN-01/02/06 | FR-V12-H-036; A122 | R12 (step-up MFA) | If-Match | W | P | RL-ADM | R1 |
| API-V12-H-017 | POST | `~/admin/identity/sso/test` | admin | Test IdP connection with a real login round-trip of the administrator | A2 POST /api/v1/identity/sso/test | FR-V12-H-036; A122 | R12 | Key | Q | — | RL-AUTH | R1 |
| API-V12-H-018 | POST | `~/admin/identity/domains` | admin | Add email domain for SSO verification (DNS TXT challenge) | A2 POST /api/v1/identity/domains; ENT-IDN-02 | FR-V12-H-036; A122 | R12 | Key | W | — | RL-ADM | R1 |
| API-V12-H-019 | POST | `~/admin/identity/domains/{id}/verify` | admin | Verify domain DNS TXT record | A2 POST /api/v1/identity/domains/{id}/verify | FR-V12-H-036; A122 | R12 | Key | Q | — | RL-ADM | R1 |
| API-V12-H-020 | PUT | `~/admin/identity/policies` | admin | Set tenant MFA and session policy | A2 PUT /api/v1/identity/policies; ENT-IDN-04/05 | FR-V12-H-036; A122 | R12 (step-up); loosening needs R01 approval | If-Match | A | P | RL-ADM | R1 |
| API-V12-H-021 | GET | `/scim/v2/Users` | scim | SCIM list/filter users (RFC 7644 filter `userName eq`) | A2 GET /api/scim/v2/Users; ENT-IDN-03 | FR-V12-H-036 | SCIM token of the tenant | Safe | R | — | RL-SCIM | R2 |
| API-V12-H-022 | POST | `/scim/v2/Users` | scim | SCIM create user (membership without business grants) | A2 POST /api/scim/v2/Users | FR-V12-H-036 | SCIM token | Yes (externalId) | W | — | RL-SCIM | R2 |
| API-V12-H-023 | GET | `/scim/v2/Users/{id}` | scim | SCIM read user | A2 GET /api/scim/v2/Users/{id} | FR-V12-H-036 | SCIM token | Safe | R | — | RL-SCIM | R2 |
| API-V12-H-024 | PATCH | `/scim/v2/Users/{id}` | scim | SCIM update user (PatchOp), including active=false | A2 PATCH /api/scim/v2/Users/{id} | FR-V12-H-036 | SCIM token | If-Match (meta.version) | W | — | RL-SCIM | R2 |
| API-V12-H-025 | DELETE | `/scim/v2/Users/{id}` | scim | SCIM de-provision user | A2 DELETE /api/scim/v2/Users/{id} | FR-V12-H-036 | SCIM token | Yes | W | — | RL-SCIM | R2 |
| API-V12-H-026 | GET | `/scim/v2/Groups` | scim | SCIM list groups | A2 GET /api/scim/v2/Groups | FR-V12-H-036 | SCIM token | Safe | R | — | RL-SCIM | R2 |
| API-V12-H-027 | POST | `/scim/v2/Groups` | scim | SCIM create group | A2 POST /api/scim/v2/Groups | FR-V12-H-036 | SCIM token | Yes (externalId) | W | — | RL-SCIM | R2 |
| API-V12-H-028 | POST | `~/admin/identity/scim-tokens` | admin | Issue or revoke the tenant SCIM bearer token | C2 `scim_token`; ENT-IDN-03 | FR-V12-H-036; A122 | R12 (step-up) | Key | W | — | RL-ADM | R2 |
| API-V12-H-029 | GET | `~/admin/roles` | admin | List built-in (R01–R20) and custom roles with permissions | A2 GET /api/v1/roles; ENT-ACC-01 | FR-V12-H-037; A123 | R12, R01, R15 | Safe | R | — | RL-ADM | R2 |
| API-V12-H-030 | POST | `~/admin/roles` | admin | Create custom role (resource × action permissions); SoD checked | A2 POST /api/v1/roles; ENT-ACC-01/02 | FR-V12-H-037; A123 | R12; approval type `custom_role` by R01 | Key | A | P | RL-ADM | R2 |
| API-V12-H-031 | PATCH | `~/admin/roles/{id}` | admin | Update custom role (new revision; re-approval) | A2 PATCH /api/v1/roles/{id} | FR-V12-H-037; A123 | R12; R01 approves | If-Match | A | P | RL-ADM | R2 |
| API-V12-H-032 | DELETE | `~/admin/roles/{id}` | admin | Retire custom role | A2 DELETE /api/v1/roles/{id} | FR-V12-H-037; A123 | R12 | If-Match | W | — | RL-ADM | R2 |
| API-V12-H-033 | GET | `~/admin/siem-sinks` | admin | List SIEM destinations with delivery health | A2 GET /api/v1/siem-sinks; ENT-ACC-04 | FR-V12-H-038; A124 | R12, R10, R15 | Safe | R | — | RL-ADM | R2 |
| API-V12-H-034 | POST | `~/admin/siem-sinks` | admin | Add SIEM destination (HTTPS, syslog over TLS, object storage) | A2 POST /api/v1/siem-sinks | FR-V12-H-038; A124 | R12 + R10 approval | Key | A | P | RL-ADM | R2 |
| API-V12-H-035 | POST | `~/admin/billing/invoices/preview` | admin | Preview next service invoice with usage, credits and tax lines | A2 POST /api/v1/billing/invoices/preview | FR-V12-H-039; A131 | R14, R12 (own tenant), R08 | Key | R | — | RL-ADM | R2 |
| API-V12-H-036 | POST | `~/admin/tax/quote` | admin+internal | Tax determination for a line (rule table; provider for US sales tax later) | A2 POST /api/v1/tax/quote; ENT-GLB-05 | FR-V12-H-039; A131 | R08, R14, R19 (service) | Key | R | — | RL-ADM | R2 |
| API-V12-H-037 | GET | `~/admin/connectors` | admin | Connector catalogue (INT-01…11 kinds) with activation-gate status per tenant | A2 GET /api/v1/connectors; ENT-INT-01/05; INT-01…11 | FR-V12-H-023; A128 | R11, R12, R10 | Safe | R | — | RL-ADM | R1 |
| API-V12-H-038 | POST | `~/admin/connectors/{id}/installations` | admin | Install connector in sandbox or production behind the activation gate | A2 POST /api/v1/connectors/{id}/installations; ENT-INT-05 | FR-V12-H-022; A128 | R11 (sandbox); production: R11 + R10 approval | Key | A | P | RL-ADM | R1 |
| API-V12-H-039 | GET | `~/admin/encryption-keys` | admin | Read tenant key configuration (platform or customer-managed) | A2 GET /api/v1/encryption-keys; ENT-DAT-02 | FR-V12-H-040; A126 | R12, R10, R15 | Safe | R | — | RL-ADM | R3 |
| API-V12-H-040 | PUT | `~/admin/encryption-keys` | admin | Set platform or customer-managed key (AWS KMS, Azure Key Vault, GCP KMS) | A2 PUT /api/v1/encryption-keys; ENT-DAT-02 | FR-V12-H-040; A126 | R12 + R01 approval (step-up) | If-Match | A | P | RL-ADM | R3 |
| API-V12-H-041 | GET | `~/admin/sandboxes` | admin | List tenant sandbox environments | A2 GET /api/v1/sandboxes; ENT-DAT-04 | FR-V12-H-040; A127 | R12, R11 | Safe | R | — | RL-ADM | R2 |
| API-V12-H-042 | POST | `~/admin/sandboxes` | admin | Create sandbox with synthetic data only | A2 POST /api/v1/sandboxes; ENT-DAT-04 | FR-V12-H-040; A127 | R12 | Key | Q | — | RL-ADM-H | R2 |
| API-V12-H-043 | POST | `~/admin/sandboxes/{id}/promotions` | admin | Request configuration promotion sandbox → production as a reviewed revision | A2 POST /api/v1/sandboxes/{id}/promotions; ENT-DAT-05 | FR-V12-H-040; A127 | R12 or R11 (requester); different reviewer approves | Key | A | P | RL-ADM | R2 |
| API-V12-H-044 | GET | `~/public/locales` | public | Supported locales with coverage and direction | A2 GET /api/v1/locales; ENT-GLB-01/02/03 | FR-V12-H-041 | R18 and all | Safe | R | — | RL-PUB-R | R1 |
| API-V12-H-045 | POST | `~/admin/ops/incidents` | admin | Declare operational incident (SEV1–SEV4) with commander | A2 POST /api/v1/ops/incidents; ENT-OPS-03 | FR-V12-H-041; A130 | R13, R11, R01 | Key | W | — | RL-ADM | R1 |
| API-V12-H-046 | GET | `/status/v1/summary` | status | Public status summary (components, incidents, maintenance) | A2 GET /api/v1/public/status; ENT-OPS-02 | FR-V12-H-041; W40 | Anonymous | Safe | R | — | RL-PUB-R | R2 |
| API-V12-H-047 | GET | `~/admin/security/findings` | admin | Vulnerability findings with SLA due dates (operator) | A2 GET /api/v1/security/findings; ENT-SEC-03 | FR-V12-H-041; A129 | R13, R01, R10, R15 | Safe | R | — | RL-ADM | R1 |
| API-V12-H-048 | POST | `~/admin/security/findings` | admin | Log finding (pen test, scanner, bug report) | A2 POST /api/v1/security/findings | FR-V12-H-041; A129 | R13, R01 | Key | W | — | RL-ADM | R1 |
| API-V12-H-049 | GET | `~/admin/ai/models` | admin | Model registry entries (provider, model ID, tier, data-class ceiling, status, eval evidence) | V8 GET /api/v1/ai/models (AIX-02) | FR-V12-H-012; A011 | R11, R01, R10, R15 | Safe | R | — | RL-ADM | R1 |
| API-V12-H-050 | POST | `~/admin/ai/models/{id}/promotion-requests` | admin | Request model promotion; requires passing eval suites | V8 POST /api/v1/ai/models/{id}/promotion-requests (AIX-05) | FR-V12-H-012; A011 | R11 (request); R01 or AI lead approves (≠ requester) | Key | A | P | RL-ADM | R1 |
| API-V12-H-051 | GET | `~/admin/ai/prompts` | admin | List prompt versions with status and eval evidence | V8 GET /api/v1/ai/prompts (AIX-04) | FR-V12-H-012; A011 | R11, R01, R10 | Safe | R | — | RL-ADM | R1 |
| API-V12-H-052 | GET | `~/admin/ai/eval-suites` | admin | List evaluation suites (cases, metrics, thresholds) | V8 GET /api/v1/ai/eval-suites (AIX-05) | FR-V12-H-012; A084 | R11, R01, R10 | Safe | R | — | RL-ADM | R1 |
| API-V12-H-053 | GET | `~/admin/ai/red-team/results` | admin | AI-INJ prompt-injection suite results | V8 GET /api/v1/ai/red-team/results (AIX-08) | FR-V12-H-012; A084 | R11, R10, R01 | Safe | R | — | RL-ADM | R1 |
| API-V12-H-054 | POST | `~/internal/ai/content-screen` | internal | Screen untrusted content (evidence, inbound, uploads) and return flags only | V8 POST /api/v1/ai/content-screen | FR-V12-H-012 | R19 service identities | Key | R | — | RL-INT | R1 |
| API-V12-H-055 | GET | `~/admin/ai/usage` | admin | Token usage and cost per accepted result | V8 GET /api/v1/ai/usage (AIX-12, AIX-14) | FR-V12-H-012; A012 | R01, R11, R14 | Safe | R | — | RL-ADM | R1 |
| API-V12-H-056 | POST | `~/admin/ai/kill-switch` | admin | Stop a model, prompt, agent or workflow immediately | V8 POST /api/v1/ai/kill-switch (AIX-20) | FR-V12-H-012; A003 | R01, R11, R10 | Key | W | — | RL-ADM | R1 |
| API-V12-H-057 | GET | `~/admin/jurisdiction-rules/{id}/rules` | admin | Rules of a jurisdiction pack with legal source and approval status | V8 GET /api/v1/compliance/packs/{id}/rules | FR-V12-H-013; A118 | R10, R01, R11, R15 | Safe | R | — | RL-ADM | R1 |
| API-V12-H-058 | GET | `~/admin/consents` | admin | Search consent ledger (hashed identifier, channel, purpose, notice version) | V8 GET /api/v1/consents (CJ-R04) | FR-V12-H-013; A007 | R10, R03 (scope), R15 | Safe | R | — | RL-ADM | R1 |
| API-V12-H-059 | POST | `~/admin/consents/{id}/withdraw` | admin | Record a withdrawal received by staff; suppress and cancel queued sends | V8 POST /api/v1/consents/{id}/withdraw (CJ-R05) | FR-V12-H-013; A007 | R10, R03 (assigned) | Key | W | — | RL-ADM | R1 |
| API-V12-H-060 | POST | `~/admin/compliance/incidents` | admin | Open privacy/compliance incident; regulatory clocks start | V8 POST /api/v1/incidents (CJ-R08) | FR-V12-H-013; A121 | R10, R01, R13 | Key | W | — | RL-ADM | R1 |
| API-V12-H-061 | POST | `~/admin/compliance/incidents/{id}/notifications` | admin | Record authority or data-principal notification | V8 POST /api/v1/incidents/{id}/notifications | FR-V12-H-013; A121 | R10 (DPO) | Key | F | — | RL-ADM | R1 |
| API-V12-H-062 | POST | `~/public/cookie-consents` | public | Record cookie choice with notice version | V8 POST /api/v1/public/cookie-consent (CJ-R12) | FR-V12-H-013; W01 | R18 | Key | W | — | RL-PUB-W | R1 |
| API-V12-H-063 | POST | `~/admin/portfolio/grants` | admin | Grant or revoke explicit aggregate (portfolio) read scope | MT-API-10 | FR-V12-H-016; A089 | R01 (owner) only | Key | A | P | RL-ADM | R1 |
| API-V12-H-064 | GET | `~/admin/metrics/business` | admin | Attributed counts, native totals, converted totals with approved rate version and missing-rate list | MT-API-09 | FR-V12-H-015; A042 | Any admin (scope) | Safe | R | — | RL-ADM | R1 |
| API-V12-H-065 | GET | `~/admin/optimization/cost-summary` | admin | Meter categories, allocated and unallocated cost, accepted-output denominator | OPT-API-02 | FR-V12-H-017; A012 | R01, R14, R11 | Safe | R | — | RL-ADM | R2 |
| API-V12-H-066 | GET | `~/portal/service/value` | portal | Customer value view: accepted output, usage, value assumption, renewal state | OPT-API-05 | FR-V12-H-017; W34 | R17 client admin (own tenant) | Safe | R | — | RL-PORTAL | R2 |
| API-V12-H-067 | GET | `~/admin/operator/conversion-metrics` | admin | Platform-operator SaaS funnel, attribution quality and acquisition cost (aggregate only) | OPT-API-08 | FR-V12-H-017; A101 | Platform R01, R14 | Safe | R | — | RL-ADM | R2 |
| API-V12-H-068 | POST | `/api/v2/workflow-runs` | v2 | Common run gateway: start (or dry-run) any SM-SVC-##-WF# workflow with a validated DTO | API-V2-RUN; MT-API-08; V4 POST /commercial/workflow-runs; OPT-API-01; Appendix A RunRequest | FR-V12-H-011; A110 | Role allowed by the workflow definition; API key/OAuth scope `runs:create` (drafts only) | Key | Q | P | RL-ADM | R1 |
| API-V12-H-069 | GET | `/api/v2/workflow-runs/{id}` | v2 | Run result: state, step states, result reference, error, usage | API-V2-RESULT | FR-V12-H-011; A110 | Run owner, scope viewers | Safe | R | — | RL-ADM | R1 |
| API-V12-H-070 | POST | `/api/v2/workflow-runs/{id}/approvals` | v2 | Approve or reject the exact action digest of a held run | API-V2-APPROVAL; V4 /commercial/workflow-runs/{id}/decisions | FR-V12-H-011; A089 | Reviewer with authority (≠ requester); never an API key or R20 | Key + expected_version | A | P | RL-ADM | R1 |
| API-V12-H-071 | POST | `/api/v2/workflow-runs/{id}/cancel` | v2 | Cancel run and reconcile pending effects | API-V2-CANCEL | FR-V12-H-011; A110 | Owner or authorized | Key + expected_version | W | — | RL-ADM | R1 |
| API-V12-H-072 | GET | `/api/v2/workflow-runs/{id}/steps` | v2 | Step trace with artifact references and redacted failure evidence | V4 GET /commercial/workflow-runs/{id}/steps | FR-V12-H-011; A110 | Run owner, scope viewers | Safe | R | — | RL-ADM | R1 |
| API-V12-H-073 | POST | `/api/v2/connectors/{kind}/events` | hooks | Generic signed provider event intake for new connector kinds (CRM, SMS-DLT, voice, warehouse) | API-V2-WEBHOOK | FR-V12-H-018 | Verified provider account | Event ID | I | — | RL-HOOK | R1 |
| API-V12-H-074 | GET | `~/admin/connectors/health-summary` | admin | Connector health, sync lag and error-rate dashboard data with alert state | ENT-INT-04 | FR-V12-H-021; A128 | R11, R12, R13 | Safe | R | — | RL-ADM | R2 |
| API-V12-H-075 | POST | `~/admin/integrations/{id}/diagnostics` | admin | Self-service setup checklist and diagnostics with escalation to support | GC-13 | FR-V12-H-030; A128 | R11, R12 | Key | Q | — | RL-ADM-H | R2 |
| API-V12-H-076 | POST | `~/admin/finops/provider-tier-scenarios` | admin | Compare provider contractual tiers, commitments and overages from forecast usage | GC-11 | FR-V12-H-029; A089 | R01, R14 | Key | Q | — | RL-ADM-H | R3 |


**Operation detail.**

| Op ID | Request | Response | Business rules and authorization | Specific errors | Event emitted |
|---|---|---|---|---|---|
| API-V12-H-001 | query `state?∈{active,expired,revoked}`, `limit`, `cursor` | 200 Page of `{id, name, prefix, last4, scopes[], ip_allowlist[], expires_at, last_used_at, created_by, state, version}` | Secret never stored or returned (C2 `api_key.key_hash` only); R11 sees keys it created; R12/R01 see all keys of the tenant | — | — |
| API-V12-H-002 | `name: s(3..80)`, `scopes: ss` (from scope registry, ≥ 1), `expires_at: t` (≤ 365 days; default 90), `ip_allowlist: cidr[]?` (IPv4/IPv6), `environment ∈ {sandbox, production}` | 201 `{id, prefix, last4, secret (shown once), scopes, expires_at}`; header `Cache-Control: no-store` | Secret = `gek_<env>_<prefix>_<32 random bytes base62>`; stored as HMAC-SHA-256(pepper, secret) [ASSUMPTION-894]; write scopes create drafts or requests only, never dispatch (AI and API keys share the L1 cap on consequential actions); production write scopes require approval type `api_key_scope` (R01); scopes cannot exceed the creator's own permissions | `VALIDATION_FAILED` (scope unknown, expiry > 365 d), `APPROVAL_REQUIRED`, `FORBIDDEN` (scope above creator) | `developer.api_key.created` |
| API-V12-H-003 | `reason: s` | 200 `{id, state: "revoked", revoked_at}` | Effective ≤ 60 s across all API nodes (key cache TTL ≤ 30 s plus revocation broadcast); later calls with the key return 401 `API_KEY_REVOKED` | `INVALID_TRANSITION` (already revoked) | `developer.api_key.revoked` |
| API-V12-H-004 | `overlap_hours: i (0..168, default 24)`, `expires_at: t?` | 201 `{id (new), prefix, last4, secret (once), predecessor_id, predecessor_expires_at}` | Successor inherits scopes and allowlist; widening scopes is not possible through rotation | `INVALID_TRANSITION` (revoked key) | `developer.api_key.rotated` |
| API-V12-H-005 | form `grant_type=client_credentials`, `scope`, `audience=growth-engine-api`; client auth `private_key_jwt` (preferred) or `client_secret_basic` | 200 `{access_token (JWT, ≤ 15 min), token_type: "Bearer", expires_in, scope}` | Audience and scope verified on every call; scopes ⊆ client grant; no refresh tokens; tokens bound to tenant; expired token → 401 `TOKEN_EXPIRED` (ENT-API-02 acceptance) | `invalid_client`, `invalid_scope` (RFC 6749 error body) | — |
| API-V12-H-006 | `limit`, `cursor` | 200 Page of `{id, client_id, name, scopes[], auth_method, jwks_thumbprints[], state, version}` | Secrets never returned | — | — |
| API-V12-H-007 | `name`, `scopes: ss`, `auth_method ∈ {private_key_jwt, client_secret_basic}`, `jwks_uri: https-url?`, `public_jwk: map?`, `ip_allowlist: cidr[]?` | 201 `{id, client_id, client_secret? (once, basic only)}` | `jwks_uri` fetched only through the SSRF-guarded fetcher (Part 3.2 §3.2.1.12) | `VALIDATION_FAILED`, `APPROVAL_REQUIRED` | `developer.oauth_client.created` |
| API-V12-H-008 | `reason: s` | 200 `{id, state: "revoked"}` | Token introspection deny-list until the longest token expiry passes | `INVALID_TRANSITION` | `developer.oauth_client.revoked` |
| API-V12-H-009 | `limit`, `cursor` | 200 Page of `{id, url_masked, events[], active, secret_versions: [{version, created_at, expires_at}], failure_streak, version}` | Secret values never returned | — | — |
| API-V12-H-010 | `url: https-url` (C2 check `^https://`), `events: ss` (⊆ outbound catalogue §11.8.5.6, ≥ 1), `description: s?` | 201 `{id, signing_secret (shown once), events, active: true}` | URL resolved and blocked if private, link-local, loopback or metadata range (SSRF guard); ownership verified by a signed `ping` that must return 2xx within 10 s; event types limited to the caller's data permissions; no Restricted values in payloads (references and digests only) | `VALIDATION_FAILED` (non-HTTPS, private address), `FORBIDDEN` (event outside permission) | `developer.webhook_endpoint.created` |
| API-V12-H-011 | `events: ss?`, `active: b?`, `rotate_secret: b?`, `overlap_hours: i?(≤ 72)` | 200 `{id, version, active, new_signing_secret? (once)}` | During overlap both secrets sign (`v1=` repeated); auto-disable after 24 h of continuous failure (all retries exhausted) with notification | `STALE_REVISION` | `developer.webhook_endpoint.updated` |
| API-V12-H-012 | `event_type: s?` (default `developer.ping`) | 202 `{delivery_id, status_url}` | Synthetic payload only (`simulated: true`); counts toward per-endpoint rate limit | `INVALID_TRANSITION` (endpoint disabled) | `developer.webhook_delivery.succeeded` / `.failed` |
| API-V12-H-013 | query `endpoint_id?`, `event?`, `status?∈{pending,succeeded,failed,exhausted}`, `from?`, `to?`, `limit`, `cursor` | 200 Page of `{delivery_id, endpoint_id, event, event_id, attempt (1..6), status_code, signed_at, delivered_at, next_attempt_at, response_ms}` | Response bodies from tenant endpoints are not stored (first 256 bytes of status line only) | — | — |
| API-V12-H-014 | `reason: s` | 202 `{delivery_id}` | Payload re-signed with a fresh timestamp; receivers dedupe on `event_id`; only events ≤ 30 days old | `INVALID_TRANSITION` (older than 30 days) | `developer.webhook_delivery.replayed` |
| API-V12-H-015 | — | 200 `{protocol ∈ {SAML 2.0, OpenID Connect}, sso_url, issuer, domain, domain_verified, enforced, breakglass_email_masked, mfa_policy, max_session_hours, idle_minutes, version}` | C2 `identity_provider` row; certificates shown as thumbprint and expiry only | — | — |
| API-V12-H-016 | `protocol`, `sso_url: https-url`, `issuer: s`, `metadata_url: https-url?`, `signing_certificates: pem[]?`, `domain: s`, `enforced: b`, `breakglass_email: email?` | 200 `{version, state ∈ {draft, tested, active}}` | `enforced=true` requires `domain_verified` and a break-glass account (C2 CHECK; ENT-IDN-06); config activates only after a passing test (H-017); wrong audience/issuer rejected; metadata must be HTTPS | `VALIDATION_FAILED`, `INVALID_TRANSITION` (enforce before verify/test), `STEP_UP_REQUIRED` | `identity.sso_config.updated` |
| API-V12-H-017 | `return_to: s (allowlisted Admin route)` | 202 `{test_id, login_url (expires 10 min)}`; result via `GET ~/admin/runs/{id}` | Checks issuer, audience, signature, clock skew ≤ 2 min, NameID/sub mapping, MFA claim (amr/acr) | `PROVIDER_UNAVAILABLE` | `identity.sso_config.tested` |
| API-V12-H-018 | `domain: fqdn` | 201 `{id, domain, txt_name, txt_value, state: "pending"}` | A domain can be verified by one tenant only; public email providers (gmail.com etc.) rejected by list | `DUPLICATE` (claimed by another tenant) | — |
| API-V12-H-019 | — | 202 `{id, state ∈ {verified, pending, failed}, checked_at}` | Daily re-check; record removal raises an alert and suspends enforcement (ENT-IDN-02 acceptance) | — | `identity.email_domain.verified` / `.verification_lost` |
| API-V12-H-020 | `mfa_policy ∈ {totp_or_passkey, passkey_privileged, passkey_all}`, `max_session_hours: i (1..24)`, `idle_minutes: i (5..120)` | 200 `{version}` | Out-of-range values rejected (C2 CHECKs); cannot go below DEC-077 (passkeys for R01, R02, R08–R12 and approvers); revocation is immediate for sessions exceeding the new limits | `VALIDATION_FAILED`, `POLICY_DENIED` (below DEC-077) | `identity.mfa_policy.updated` |
| API-V12-H-021 | `filter`, `startIndex`, `count` (≤ 200) | 200 `ListResponse` (RFC 7643 User schema + enterprise extension) | Only the token's tenant; attributes limited to userName, name, emails[primary], active, groups, externalId | SCIM error schema (`invalidFilter`, `tooMany`) | — |
| API-V12-H-022 | RFC 7643 User | 201 User with `id`, `meta.version` | Email domain must be verified for the tenant; roles come only from group mapping to built-in or custom roles; approver roles still need DEC-077 passkey enrolment before use | 409 `uniqueness` | `identity.scim.user_provisioned` |
| API-V12-H-023 | — | 200 User | ETag = meta.version | 404 | — |
| API-V12-H-024 | RFC 7644 PatchOp | 200 User | `active=false` revokes sessions, API keys created by the user and pending approvals within 15 minutes (ENT-IDN-03); last tenant administrator cannot be deactivated without break-glass | 400 `mutability`, 412 precondition | `identity.scim.user_updated` / `.user_deprovisioned` |
| API-V12-H-025 | — | 204 | Soft delete: membership ended, audit and authored records retained (DEC-028); same revocation as active=false | 404 | `identity.scim.user_deprovisioned` |
| API-V12-H-026 | `filter`, `startIndex`, `count` | 200 ListResponse of Group | Groups map 1:1 to a role-mapping record (group → role, startup scope) | — | — |
| API-V12-H-027 | RFC 7643 Group (`displayName`, `members[]`) | 201 Group | A new group has no role until R12 maps it in A122 (no privilege from the IdP alone); SoD checked on mapping (ENT-ACC-02) | 409 `uniqueness` | `identity.scim.group_changed` |
| API-V12-H-028 | `action ∈ {issue, revoke}`, `token_id: u?` | 201 `{token_id, prefix, token (once)}` or 200 `{token_id, revoked_at}` | Hash only (C2 `token_hash`); one active token plus one in overlap | `INVALID_TRANSITION` | `identity.scim.token_changed` |
| API-V12-H-029 | `limit`, `cursor` | 200 Page of `{id, name, kind ∈ {builtin, custom}, permissions[] (resource:action), assigned_users, version}` | Built-in roles are read-only | — | — |
| API-V12-H-030 | `name: s`, `permissions: ss` (registry `resource:action`), `base_role: s?` | 201 `{id, version, state: "pending_approval"}` | Unknown permission rejected; request+approve pairs in runs, configuration and billing rejected (C2 `sod_conflict`, DB trigger); custom roles cannot exceed the union of built-in R01–R15 permissions; the AI identity R20 and API keys never receive custom roles | `SEPARATION_OF_DUTIES`, `VALIDATION_FAILED` | `access.role.created` |
| API-V12-H-031 | `permissions: ss`, `name?` | 200 `{version, state}` | Applies at API, worker and UI after approval; permission caches invalidated (API-021 pattern) | `SEPARATION_OF_DUTIES`, `STALE_REVISION` | `access.role.updated` |
| API-V12-H-032 | — | 204 | Refused while users are assigned (reassign first); record retained for audit | `INVALID_TRANSITION` (role in use) | `access.role.retired` |
| API-V12-H-033 | — | 200 Page of `{id, kind, endpoint_masked, format, retention_years, last_delivery_at, lag_seconds, state}` | Credentials as secret references only | — | — |
| API-V12-H-034 | `kind ∈ {https, syslog-tls, object-storage}`, `endpoint` (C2 regex), `format ∈ {JSON, CEF}`, `retention_years ∈ {1,3,7}`, `credential_ref: s` | 201 `{id, state: "pending_test"}` | Non-TLS endpoints rejected; test event must arrive before activation (ENT-ACC-04 acceptance); stream carries audit events only (redacted per §2.34.2) | `VALIDATION_FAILED` | `audit.siem_sink.added` |
| API-V12-H-035 | `tenant_id?` (platform roles), `period: yyyy-mm`, `include_pending_usage: b` | 200 `{lines[{description, quantity, unit_price: Money, net: Money}], tax_lines[{rule_id, rate_percent, amount: Money}], net_minor, tax_minor, total_minor, currency, fx_evidence?}` | Pure computation, no ledger entry; `total = net + tax` (C2 CHECK); mixed currencies never summed without an approved rate (ENT-GLB-06) | `VALIDATION_FAILED` (rate needs input) | — |
| API-V12-H-036 | `seller_jurisdiction`, `buyer_jurisdiction`, `buyer_tax_id?`, `hsn_sac?`, `amount: Money`, `supply_type ∈ {goods, services, digital}` | 200 `{rule_id, rate_percent, tax_amount: Money, reverse_charge: b, needs_rate_input: b, explanation_key}` | Uses approved `tax_rule` rows only (C2, approved_by not null); India GST per DEC-027; unknown jurisdiction → `needs_rate_input=true`, never a guessed rate | `VALIDATION_FAILED` | — |
| API-V12-H-037 | `category?`, `limit`, `cursor` | 200 Page of `{connector_id, category, providers[], auth, scopes, gate: {security_review, dpa, transfer_basis, channel_registration}, state ∈ {available, blocked_legal, installed, disabled}}` | Contact-data connectors show `blocked_legal` until DEC-V9-04 closes (ENT-INT-05) | — | — |
| API-V12-H-038 | `environment ∈ {sandbox, production}`, `credential_ref: s`, `scopes: ss`, `ownership ∈ {platform, tenant_byo}`, `legal_review_ref?`, `security_review_ref?`, `market_ids: ids`, `offering_ids: ids?` | 201 `{installation_id, state ∈ {sandbox_active, pending_gate, active}}` | Production requires legal and security review references (C2 CHECK); channel registration (DLT entity/header/template IDs, WhatsApp templates) verified; BYO charges kept separate from platform charges (GC-10) | `APPROVAL_REQUIRED`, `POLICY_DENIED` (gate incomplete) | `connector.installation.requested` / `.activated` / `.blocked` |
| API-V12-H-039 | — | 200 `{mode ∈ {platform, customer}, kms_key_ref_masked, rotation_days ∈ {90,180,365}, last_rotated_at, health}` | C2 `tenant_key_config` | — | — |
| API-V12-H-040 | `mode`, `kms_key_ref: s?`, `rotation_days` | 202 `{run_id}` (re-wrap job) | Key reference validated by a wrap/unwrap test before activation; revocation by the customer crypto-shreds data (drill evidence); reuses ADR-137 | `VALIDATION_FAILED` (invalid key ref) | `data.encryption_key.changed` |
| API-V12-H-041 | — | 200 Page of `{sandbox_id, name, copies_configuration, contains_personal_data: false, created_at}` | — | — | — |
| API-V12-H-042 | `name`, `copies_configuration: b` | 202 `{sandbox_id, run_id}` | Personal data never copied (C2 CHECK `contains_personal_data=false`); sandbox uses sandbox adapters only (IP-08); separate tenant scope | `ENTITLEMENT_EXCEEDED` | `data.sandbox.created` |
| API-V12-H-043 | `config_revision_ids: ids`, `reason` | 201 `{promotion_id, approval_id, state: "pending_review"}` | Creates a ConfigRevision candidate (API-039) in production; self-approval rejected (C2 CHECK); promoted revision immutable | `SEPARATION_OF_DUTIES` | `data.promotion.requested` |
| API-V12-H-044 | — | 200 `{items[{locale, direction ∈ {ltr, rtl}, coverage_percent, reviewed}]}` | Locales below 100% reviewed coverage are not offered in the switcher (fallback English) | — | — |
| API-V12-H-045 | `severity ∈ {SEV1..SEV4}`, `title`, `components: ss`, `commander_user_id`, `status_message?` | 201 `{incident_id, status: "Investigating"}` | SEV1/2 page on-call; communication timeline timers start; privacy impact flag routes to compliance incident (H-060) | — | `ops.incident.opened` |
| API-V12-H-046 | — | 200 `{components[{name, status}], incidents[{id, severity, status, status_message, updated_at}], maintenance[]}` | Served from the independent status host (RECOMMENDATION-900), published from approved notices only (CAP-X3-12); no tenant names | — | — |
| API-V12-H-047 | `severity?`, `state?`, `overdue?` | 200 Page of `{finding_id, title, severity, found_at, due_at, closed_at, evidence_ref, overdue}` | Platform-level (no tenant data); overdue Critical blocks release (KPI-03) | — | — |
| API-V12-H-048 | `title`, `severity ∈ {Critical, High, Medium, Low}`, `found_at: date`, `source`, `evidence_ref?` | 201 `{finding_id, due_at}` | due_at computed 7/30/90/180 days (C2 CHECK); closing requires evidence_ref | `VALIDATION_FAILED` | `security.finding.logged` |
| API-V12-H-049 | `tier?`, `status?` | 200 Page of `{id, provider, model_id, tier ∈ {0,1a,1b,2,3}, max_data_class, status ∈ {candidate, shadow, active, retired}, last_eval_run_id, version}` | Tier 2 entries carry `max_data_class ∈ {Public, Internal-non-personal}` and default off (safety invariant) | — | — |
| API-V12-H-050 | `target_status ∈ {shadow, active}`, `eval_run_ids: ids`, `routes: ids` | 201 `{approval_id, state: "pending"}` | Every required suite passed on the candidate with stated denominators; red-team (AI-INJ) suite pass mandatory; DEC-418 routing order preserved (Claude Sonnet primary) | `POLICY_DENIED` (suite missing/failing) | `ai.model.promotion_requested` |
| API-V12-H-051 | `task_key?`, `status?` | 200 Page of `{id, task_key, version, status, author, approved_by, eval_run_id, content_hash}` | Prompt text shown to R11/R01 only | — | — |
| API-V12-H-052 | — | 200 Page of `{id, name, task_keys[], case_count, metrics[{name, threshold}], dataset_revision}` | — | — | — |
| API-V12-H-053 | `model_id?`, `prompt_id?` | 200 Page of `{run_id, suite: "AI-INJ", passed, failed, denominator, findings[{case_id, category}], run_at}` | Attack strings shown redacted | — | — |
| API-V12-H-054 | `content_ref: u` or `text: s(≤ 32 KB)`, `source_kind`, `data_class` | 200 `{flags[{kind ∈ {prompt_injection, pii, secret, malware_link, policy}, severity, span}], verdict ∈ {pass, quarantine}}` | Returns flags only, never rewritten content; Tier 0 rules first, classifier per routing; Restricted text never to Tier 2 | `PAYLOAD_TOO_LARGE` | `ai.content.flagged` (when quarantined) |
| API-V12-H-055 | `period`, `group_by ∈ {agent, task, model, startup}` | 200 `{rows[{key, calls, input_tokens, output_tokens, cost: Money, accepted_results, cost_per_accepted: Money}], as_of}` | Denominator = human-accepted outputs; estimates labelled | — | — |
| API-V12-H-056 | `target_kind ∈ {model, prompt, agent, workflow}`, `target_id`, `scope ∈ {tenant, startup, platform}`, `reason` | 200 `{kill_id, effective_at}` | Protective, fail-closed (allowed at L2 by DEC-407 pattern); effective ≤ 60 s; release needs a second person (API-452 pattern) | — | `ai.kill_switch.activated` |
| API-V12-H-057 | `version?` | 200 Page of `{rule_id, channel, purpose, effect, legal_source, status ∈ {draft, counsel_approved, retired}}` | Pack status must be Approved before any send in that market (ENT-CMP-08) | — | — |
| API-V12-H-058 | `identifier_hash?`, `channel?`, `purpose?`, `state?`, `limit`, `cursor` | 200 Page of `{consent_id, subject_ref, channel, purpose, notice_version, state, captured_at, withdrawn_at}` | Search by hash only; Restricted field rules (§2.26.5) | `FILTER_NOT_ALLOWED` | — |
| API-V12-H-059 | `channel_received ∈ {email, phone, letter, in_person}`, `evidence_ref?`, `reason?` | 200 `{consent_id, state: "withdrawn", suppressions_added, cancelled_messages}` | Same effect as API-067 within one transaction (append-only consent record + suppression + outbox cancellation) | `INVALID_TRANSITION` (already withdrawn) | `governance.consent.withdrawn` |
| API-V12-H-060 | `kind ∈ {breach, misuse, complaint, policy}`, `detected_at: t`, `markets: ss`, `data_classes: ss`, `description` | 201 `{incident_id, clocks[{authority, deadline_at}]}` | Clock per jurisdiction pack (e.g. DPDP, GDPR 72 h; verify at time of implementation as of 27 Nov 2026); containment via API-093 | — | `governance.compliance_incident.opened` |
| API-V12-H-061 | `recipient_kind ∈ {authority, principals}`, `authority?`, `sent_at`, `channel`, `evidence_ref`, `principal_count?` | 201 `{notification_id, clock_state ∈ {met, late}}` | Human sends the notice; the platform records evidence only (no automated regulator submission) | — | `governance.compliance_incident.notification_recorded` |
| API-V12-H-062 | `notice_version`, `choices: {necessary: true, analytics: b, marketing: b}`, `consent_token?` | 201 `{consent_token, expires_at}` | No IP stored raw (hash); non-necessary trackers off until choice; first-party only (no third-party cookies, Part 2.4) | `RATE_LIMITED` | `governance.cookie_consent.recorded` |
| API-V12-H-063 | `action ∈ {grant, revoke}`, `user_id`, `startup_ids: ids`, `expires_at?` | 200 `{grant_id, version}` | Aggregate grants are read-only (DEC-055); independent SaaS clients excluded by default; audit | `FORBIDDEN` | `governance.portfolio_grant.changed` |
| API-V12-H-064 | `period`, `dimensions: ss`, `currency`, `rate_version?` | 200 `{rows[{dims, counts, native_totals[{currency, amount}], converted_total: Money?}], rate_version, missing_rates[]}` | Mixed currencies never summed without an approved rate (MT-21) | `FILTER_OUT_OF_SCOPE` | — |
| API-V12-H-065 | `period`, `sku?`, `cursor` | 200 Page of `{category, allocated: Money, unallocated: Money, accepted_outputs, unit_cost: Money}` | Estimates labelled | — | — |
| API-V12-H-066 | `period`, `sku?` | 200 `{accepted_outputs, usage, value_assumption{basis, stated_by}, renewal_state}` | Value assumptions labelled as assumptions, never as realised revenue | — | — |
| API-V12-H-067 | `cohort`, `period`, `dimension` | 200 `{stages[{name, count}], attribution_quality, acquisition_cost: Money}` | Aggregate only; k-anonymity ≥ 5 per cell; no tenant business content | — | — |
| API-V12-H-068 | `RunRequest {workflow_id ^SM-SVC-\d{2}-WF0[1-4]$, workflow_version, business_context: BusinessContext, input (urn:sm:dto:<workflow_id>:v2#/$defs/input), dry_run}` + `mode ∈ {draft, execute}` | 202 `{run_id, state, hold_reason?, reservation{amount: Money}, correlation_id}`; dry_run → 200 `{plan, gate_reasons[], cost_estimate}` | Entitlement, schema, quota, configuration, approval and budget checks; no duplicate effect (idempotency); external effects still go outbox → PDP dispatch recheck; API callers limited to `mode=draft` for consequential workflows (L1 cap) | 400, 403 `ENTITLEMENT_EXCEEDED`, 409, 422 `SCHEMA_INVALID`, 429 | `automation.run.started` |
| API-V12-H-069 | — | 200 `{state, step_states[], result_ref, error?, usage{tokens, cost: Money}}` | Projection of API-467; uniform 404 outside scope | 404, 403 | — |
| API-V12-H-070 | `action_digest: sha256`, `decision ∈ {approve, reject}`, `expiry: t`, `expected_version: i` | 200 `{approval_ref, state}` | Delegates to API-539; digest must equal current run hold digest; browser session with step-up only | 403, 409 `APPROVAL_VOIDED` | `approval.decided` |
| API-V12-H-071 | `expected_version`, `reason` | 200 `{state}` | Uncertain effects reconciled, never re-sent (BRL-AUT-07) | 409 `OUTCOME_UNCERTAIN` | `automation.run.cancelled` |
| API-V12-H-072 | `cursor`, `limit` | 200 Page of `{step_id (STEP-…), state, started_at, ended_at, artifact_refs[], failure{code, message}?}` | No provider secrets or raw payloads | 404 | — |
| API-V12-H-073 | Provider-signed payload | 200 `{receipt_id}` (duplicate → 200, no effect) | Signature/time/account mapping per §3.2.1.13; persist-then-ack ≤ 2 s | 401 (bad signature) | `ops.webhook.received` |
| API-V12-H-074 | `period` | 200 `{rows[{installation_id, kind, state, sync_lag_s, error_rate, breaker_state, last_success_at, alert_state}]}` | Thresholds per connector kind; alerts fire in staging test (ENT-INT-04 acceptance) | — | `connector.health.degraded` / `.recovered` |
| API-V12-H-075 | `checks: ss?` | 202 `{run_id}` → `{checks[{id, result, remedy_key}], escalation_case_id?}` | Read-only probes (no business side effect); unresolved → support case (API-440 pattern) | — | — |
| API-V12-H-076 | `provider`, `horizon_months`, `forecast_basis` | 202 → `{scenarios[{tier, commitment: Money, expected_overage: Money, unused_commitment: Money}]}` | Recommendation only; purchasing approval required outside the platform | — | — |


### 11.8.5.6 Event contracts and outbound webhooks (ADR-206)

**New domain event types (add to Part 3.2 §3.2.3.3; envelope of §3.2.3.1; schema v1).**

| Event type (v1) | Producer | Consumers | Payload keys (`data`) | Source |
|---|---|---|---|---|
| `developer.api_key.created` / `.rotated` / `.revoked` / `.expired` | core.developer | Key cache invalidation, Notify (R12), Audit, SIEM | key_id, prefix, scopes, expires_at, actor | API-V12-H-002…004 |
| `developer.oauth_client.created` / `.revoked` | core.developer | Token deny-list, Notify | client_id, scopes | API-V12-H-007/008 |
| `developer.webhook_endpoint.created` / `.updated` / `.disabled` | core.developer | Delivery worker, Notify | endpoint_id, events, active, secret_version | API-V12-H-010/011 |
| `developer.webhook_delivery.succeeded` / `.failed` / `.exhausted` / `.replayed` | delivery worker | A125 delivery log projection, Notify (exhausted), health | delivery_id, endpoint_id, event_id, attempt, status_code | API-V12-H-012…014 |
| `identity.sso_config.updated` / `.tested` / `.enforced` | core.identity | Session policy cache, Notify, SIEM | version, protocol, enforced | API-V12-H-016/017 |
| `identity.email_domain.verified` / `.verification_lost` | core.identity | SSO enforcement guard, Notify (High) | domain_id, domain | API-V12-H-019 |
| `identity.mfa_policy.updated` | core.identity | Session revocation job | version, mfa_policy, limits | API-V12-H-020 |
| `identity.scim.user_provisioned` / `.user_updated` / `.user_deprovisioned` / `.group_changed` / `.token_changed` | core.identity | Membership, key revocation, approvals re-check | user_id, external_id, change | API-V12-H-022…028 |
| `identity.breakglass.used` | core.identity | SEV3 security event, Notify (R01, R10), SIEM | user_id, reason | ENT-IDN-06 |
| `access.role.created` / `.updated` / `.retired` | core.access | Permission cache, Audit | role_id, permissions_hash | API-V12-H-030…032 |
| `audit.siem_sink.added` / `.delivery_failed` | audit | Notify (R12, R10) | sink_id, kind, lag_seconds | API-V12-H-034 |
| `connector.installation.requested` / `.activated` / `.blocked` | integrations | Approval, Notify, PDP capability cache | installation_id, connector_id, environment, gate | API-V12-H-038 |
| `connector.health.degraded` / `.recovered` | integrations | Notify (R11), status page component | installation_id, metric, value | API-V12-H-074 |
| `data.encryption_key.changed` | data | Re-wrap job, Notify | mode, key_ref_masked | API-V12-H-040 |
| `data.sandbox.created`, `data.promotion.requested` | data | Notify | sandbox_id / promotion_id | API-V12-H-042/043 |
| `ops.status.published` | ops | Status host publisher | notice_id, components | API-V12-H-046 |
| `security.finding.logged` / `.overdue` | security | Release gate (blocks on overdue Critical), Notify | finding_id, severity, due_at | API-V12-H-048 |
| `ai.model.promotion_requested` | ai.quality | Approval, Notify | model_id, target_status, eval_run_ids | API-V12-H-050 |
| `ai.kill_switch.activated` / `.released` | ai.gateway | Gateway route cache (≤ 60 s), automation (hold), Notify (Critical) | target_kind, target_id, scope | API-V12-H-056 |
| `ai.content.flagged` | ai.gateway | Quarantine handler, Audit | content_ref, flags | API-V12-H-054 |
| `governance.consent.withdrawn` | governance | Suppression, outbox cancellation, outbound projection | consent_id, channel, purpose | API-V12-H-059 |
| `governance.compliance_incident.notification_recorded` | governance | Clock tracker, Notify | incident_id, recipient_kind, clock_state | API-V12-H-061 |
| `governance.cookie_consent.recorded` | governance | Analytics gate | consent_token, choices | API-V12-H-062 |
| `governance.portfolio_grant.changed` | governance | Permission cache, Audit | grant_id, user_id, startup_ids, action | API-V12-H-063 |

That is 24 catalogue rows and **49 concrete event types** (`/` variants counted). Restricted values are never in payloads (references and digests only).

**Outbound webhook projection v1 (subscribable event types).** Tenants subscribe to these types only; each is a **projection** of a domain event with an allowlisted payload of references (`id`, `type`, `schema_version`, `occurred_at`, `tenant_id`, `startup_id`, `subject {type, id, version}`, `data {…}`, `links.self`). Receivers fetch details through the API with their own scopes, so the payload never widens access.

| # | Outbound type | Domain event | `data` keys | Minimum scope to subscribe |
|---|---|---|---|---|
| 1 | `lead.submitted` | `crm.lead.submitted` | lead_id, source, startup_id | `leads:read` |
| 2 | `lead.qualified` | `crm.lead.qualified` | lead_id, deal_id? | `leads:read` |
| 3 | `deal.created` | `crm.deal.created` | deal_id, stage | `deals:read` |
| 4 | `deal.stage_changed` | `crm.deal.transitioned` | deal_id, from_stage, to_stage | `deals:read` |
| 5 | `deal.won` | `crm.deal.won` | deal_id, amount_ref | `deals:read` |
| 6 | `deal.lost` | `crm.deal.lost` | deal_id, reason_code | `deals:read` |
| 7 | `quote.approved` | `commerce.quote.approved` | quote_id, version | `quotes:read` |
| 8 | `quote.accepted` | `commerce.quote.accepted` | quote_id, version | `quotes:read` |
| 9 | `contract.signed` | `commerce.contract.signed` | contract_id, version, content_hash | `contracts:read` |
| 10 | `order.issued` | `commerce.order.issued` | order_id, direction | `orders:read` |
| 11 | `order.completed` | `commerce.order.completed` | order_id | `orders:read` |
| 12 | `fulfilment.recorded` | `commerce.fulfilment.recorded` | order_id, event_key | `orders:read` |
| 13 | `invoice.issued` | `finance.invoice.issued` | invoice_id, total_ref | `invoices:read` |
| 14 | `payment.verified` | `finance.payment.verified` | payment_id, invoice_id | `invoices:read` |
| 15 | `meeting.booked` | `engagement.meeting.booked` | meeting_id, starts_at | `meetings:read` |
| 16 | `message.delivered` | `engagement.message.delivered` | message_id, channel | `messages:read` |
| 17 | `contact.opted_out` | `engagement.optout.received` / `governance.consent.withdrawn` | subject_ref (hash), channel, purpose | `contacts:read` (needed by CRM sync to suppress) |
| 18 | `run.completed` | `automation.run.completed` | run_id, workflow_id, result_ref | `runs:read` |
| 19 | `run.failed` | `automation.run.failed` | run_id, error_code | `runs:read` |
| 20 | `approval.decided` | `approval.decided` | approval_id, object_type, decision | `approvals:read` |
| 21 | `subscription.changed` | `saas.subscription.changed` | subscription_id, plan_version_id | `billing:read` |
| 22 | `usage.threshold_reached` | `saas.usage.threshold_reached` | dimension, percent | `billing:read` |
| 23 | `onboarding.completed` | `lifecycle.onboarding.completed` | onboarding_id | `onboarding:read` |
| 24 | `developer.ping` | (synthetic) | endpoint_id | — |

**Signature and delivery specification (ENT-API-05).**

| Item | Specification |
|---|---|
| Headers | `GE-Webhook-Id` (delivery UUID), `GE-Event-Id` (event UUID, receiver dedupe key), `GE-Event-Type`, `GE-Timestamp` (Unix seconds), `GE-Signature: v1=<hex>` (two `v1=` values during secret rotation overlap) |
| Signed string | `<GE-Timestamp>.<GE-Event-Id>.<raw body bytes>`; HMAC-SHA-256 with the endpoint secret (≥ 32 bytes, Secrets Manager reference in `webhook_endpoint.secret_ref`) |
| Freshness | Receivers reject `|now − GE-Timestamp| > 300 s` (V12: "> 5-minute-old signature rejected") |
| Replay protection | Receivers store `GE-Event-Id` for ≥ 24 h; the platform never reuses an event ID; manual replay (API-V12-H-014) re-signs with a new timestamp and the same event ID |
| Success | HTTP 2xx within 10 s; redirects not followed; 410 Gone disables the endpoint |
| Retries [ASSUMPTION-895] | 6 attempts within 24 h (C2 `attempt BETWEEN 1 AND 6`): immediately, +1 min, +10 min, +1 h, +5 h, +16 h (± 10% jitter; cumulative ≈ 22 h 11 min); then `exhausted`; endpoint auto-disabled after 24 h of continuous failure |
| Ordering | Not guaranteed; `subject.version` lets receivers discard stale events |
| Egress | Delivery workers on AWS ap-south-1 send from published static egress IPs (NAT) so tenants can allowlist; SSRF guard re-resolves DNS per attempt |
| Data | References and digests only; no Restricted values; `simulated: true` events are never delivered except to sandbox endpoints |

Reference verifier (published in the developer portal and used by TC-V12-H-082):

```python
import hmac, hashlib, time

def verify(secret: bytes, headers: dict, body: bytes, seen_event_ids: set) -> bool:
    ts = int(headers["GE-Timestamp"])
    if abs(time.time() - ts) > 300:
        return False                                   # older than 5 minutes
    event_id = headers["GE-Event-Id"]
    if event_id in seen_event_ids:
        return False                                   # replay
    signed = f"{ts}.{event_id}.".encode() + body
    expected = hmac.new(secret, signed, hashlib.sha256).hexdigest()
    candidates = [p.split("=", 1)[1] for p in headers["GE-Signature"].split(",") if p.strip().startswith("v1=")]
    if not any(hmac.compare_digest(expected, c.strip()) for c in candidates):
        return False                                   # tampered
    seen_event_ids.add(event_id)
    return True
```

```mermaid
flowchart TD
  A["Domain event committed with outbox row"] --> B["Projection worker maps to outbound type"]
  B --> C{"Any active endpoint subscribed in tenant"}
  C -- "No" --> Z["Stop"]
  C -- "Yes" --> D["Create webhook_delivery attempt 1"]
  D --> E["Sign timestamp, event id and body with endpoint secret"]
  E --> F["POST to tenant HTTPS endpoint<br/>SSRF guard, 10 s timeout"]
  F --> G{"2xx received"}
  G -- "Yes" --> H["Mark succeeded, emit delivery event"]
  G -- "410 Gone" --> I["Disable endpoint, notify R12"]
  G -- "Other or timeout" --> J{"Attempt below 6"}
  J -- "Yes" --> K["Schedule next attempt with backoff and jitter"]
  K --> E
  J -- "No" --> L["Mark exhausted, notify, count toward auto-disable"]
```

### 11.8.5.7 Connector framework and activation gate (ENT-INT-01…05; CF-01…12)

| Clause | Contract element (every connector) | Detail | V12 source |
|---|---|---|---|
| CF-01 | Port and manifest | Connector = adapter implementing a typed port (Part 3.2 IP-01) plus a manifest: `connector_id`, category, providers, auth method, scopes, data classes sent and received, events, limits, failure classes, sandbox availability, owner | ENT-INT-01 |
| CF-02 | Authentication | OAuth 2.0 (authorization code with PKCE for user grants; client credentials for service grants), API key or service account; tokens refreshed by the worker, never by browsers | ENT-INT-01, INT-01…11 |
| CF-03 | Secrets | Only `credential_ref` (Secrets Manager ARN) stored; rotation and revocation hooks; never in rows, logs, prompts or HTML (TC-V12-H-085) | ENT-INT-02, SEC-04, MT-23 |
| CF-04 | Data mapping | Anti-corruption mapping (IP-10); field mapping versioned; unknown provider fields ignored; data minimization per Part 3.2 §3.2.4.4 | ENT-INT-01 |
| CF-05 | Channel accounts | Multiple accounts per company with `market_ids`, `offering_ids`, sender aliases; eligibility per account; wrong-company account denied | MT-22, MT-23 |
| CF-06 | Events | Inbound via provider webhooks (§3.2.1.13) or `/api/v2/connectors/{kind}/events`; persist-then-ack; dedupe by provider event ID | ENT-INT-01, API-V2-WEBHOOK |
| CF-07 | Limits and resilience | Per-connector rate limits, timeouts, retries with backoff and jitter, circuit breaker and bulkhead (Part 3.2 §3.2.7); uncertain writes reconcile before retry | ENT-INT-03 |
| CF-08 | Incremental sync | Webhooks first; otherwise cursors, ETags and change windows; gap detection and repair; provider reset handling without duplicates | GC-08 |
| CF-09 | Reconciliation | Scheduled state reconciliation (IP-05) for money, delivery and sync; discrepancies to the exception queue | ENT-INT-03, adapter family "Payments / marketplace" |
| CF-10 | Health | Health probe, sync lag, error rate, breaker state, alert thresholds (API-V12-H-074) | ENT-INT-04 |
| CF-11 | Activation gate | Production activation needs: security review reference; DPA; transfer basis entry (CJ-R15); channel registration (DLT entity/header/template IDs for SMS; approved WhatsApp templates); licence and budget line approved (Part 7.4b PG-01…PG-10); contact-data connectors additionally blocked until DEC-V9-04 closes and CJ-GL-01 is met | ENT-INT-05, FSD 28 V9 |
| CF-12 | Selection evidence | Matched benchmark (coverage, accuracy, p95, reliability, licence, hosting/maintenance, fees), rights, jurisdiction, quota, evidence freshness; owner and release recorded | FSD 27 adapter families; GC-09; FSD 28 closing statement |

```mermaid
stateDiagram-v2
  [*] --> Available
  Available --> SandboxActive: Install in sandbox
  Available --> BlockedLegal: Contact-data connector before DEC-V9-04
  SandboxActive --> PendingGate: Request production
  PendingGate --> PendingGate: Evidence added
  PendingGate --> Active: Security review, DPA, CJ-R15, registration and approval complete
  PendingGate --> Rejected: Reviewer rejects
  Active --> Degraded: Health threshold breached
  Degraded --> Active: Recovered
  Active --> Disabled: Owner disables or credential revoked
  Disabled --> PendingGate: Re-enable request
  BlockedLegal --> Available: DEC-V9-04 closed
  Rejected --> [*]
```

### 11.8.5.8 New adapters (AD-V12-H-01…11)

**Part A: purpose, protocol, authentication, quotas, budget.** All quotas, fees and API versions are to **verify at time of implementation (as of 27 Nov 2026)**.

| AD | Port (provider candidates) | Purpose | Protocol | Authentication | Quotas / fees (verify) | V12 phase → release | Budget line |
|---|---|---|---|---|---|---|---|
| AD-V12-H-01 | `CrmSyncPort` (Zoho CRM, HubSpot, Salesforce) | Bi-directional sync of contacts, accounts, opportunities for tenants that keep an external CRM; platform stays system of record for consent and approvals | REST + provider webhooks / CDC | OAuth 2.0 per tenant (BYO) | Provider API call quotas per edition; ₹0 platform fee (tenant's own licence) | R1 → Release 1 (CONFLICT-888) | None (BYO) |
| AD-V12-H-02 | `SmsPort` (DLT-registered aggregator in India; RCS business messaging where the aggregator supports it) | Service and promotional SMS with DLT entity, header and template IDs; delivery receipts; STOP keyword handling | REST + delivery-report webhooks | API key in vault | Per-SMS fee and DLT registration fees per operator (verify); promotional sends only in permitted hours (CJ-IN-06) | R1 → Release 1 (CONFLICT-888) | New line B25 (proposal) |
| AD-V12-H-03 | `VoicePort` (CPaaS with 140-series promotional and 160-series service numbers) | Click-to-call and approved voice notifications with disclosure and recording consent | REST + call-status webhooks | API key in vault | Per-minute and number rental fees (verify) | R3+ → W6 or later | B26 (proposal) |
| AD-V12-H-04 | `WarehouseExportPort` (BigQuery, Snowflake, Postgres) | Scoped scheduled export of analytics tables to a tenant-owned warehouse | Provider bulk-load APIs or COPY over TLS | Tenant service account (vault) | Tenant-side cost; egress from AWS per GB (verify) | R2 → Release 2 | B01c egress |
| AD-V12-H-05 | `IdentityFederationPort` (Okta, Entra ID, Google Workspace via SAML 2.0 / OIDC; SCIM 2.0 server) | Per-tenant SSO and provisioning (ADR-207) | SAML/OIDC brokered through the existing IdP (DEC-019) where it supports per-tenant brokering; otherwise in-product SAML SP | IdP metadata + certificates; SCIM bearer token | ₹0 platform fee if the existing IdP supports brokering (Sprint 0 check 13, §11.8.5.11) | R1 SSO / R2 SCIM | B01 |
| AD-V12-H-06 | `WebhookDeliveryPort` (in-house on Celery) | Outbound signed webhooks (§11.8.5.6) | HTTPS POST | HMAC secret per endpoint | Compute within existing workers | R1 → Release 1 | B01c |
| AD-V12-H-07 | `SiemSinkPort` (HTTPS collector, syslog over TLS, S3/GCS/Azure Blob) | Stream audit events | HTTPS / RFC 5425 syslog-TLS / object put | Tenant credential reference | Tenant-side | R2 → Release 2 | B01c egress |
| AD-V12-H-08 | `TaxPort` (rule table; US sales-tax provider later) | Tax determination per line | In-process rule engine; provider REST at R5 | API key (R5) | Provider per-transaction fee (R5, verify) | R2 (rules) / R5 (provider) | — |
| AD-V12-H-09 | `TenantKmsPort` (AWS KMS cross-account; Azure Key Vault; GCP KMS) | Customer-managed key wrap/unwrap (ADR-137) | Provider KMS APIs | Cross-account role / workload identity federation | Per-request KMS fees (verify) | R3 → W6 | B01c |
| AD-V12-H-10 | `StatusPublishPort` (independent static host) | Publish approved status notices off-platform (ENT-OPS-02) | Static JSON + HTML upload | Deploy token | ₹0–1,800/month (verify) | R2 → Release 2 | B27 (proposal) |
| AD-V12-H-11 | `EmailPort` alternates (SendGrid, Postmark) | Equivalent ESPs behind the same port as AD-01, activated only through the gate | REST + signed webhooks | API key in vault | Per-email plans (verify) | Conditional | B05 |

**Part B: failure classes, idempotency, sandbox, data sent, fallback.**

| AD | Failure classes | Idempotency | Sandbox (verify) | Data class sent | Fallback (never silent) |
|---|---|---|---|---|---|
| AD-V12-H-01 CRM | 5xx/429 transient; 401 auth (disable after threshold); validation permanent; timeout on write uncertain | External ID field = platform record ID; upsert by external ID | Provider developer orgs/sandboxes | Confidential business records; Restricted contact fields only with consent basis | Sync paused, discrepancy queue; platform data unaffected |
| AD-V12-H-02 SMS | Throttling transient; DLT template mismatch permanent; timeout uncertain (reconcile by delivery report) | Client message reference = message ID | Aggregator test accounts | Restricted: phone (E.164) + approved template variables | Email if consented; else human task |
| AD-V12-H-03 Voice | As SMS; call failed permanent | Call reference = action ID | Provider test numbers | Restricted: phone; recordings only with consent | Human callback task |
| AD-V12-H-04 Warehouse | Load errors permanent per batch; transient retried | Batch ID + manifest hash | Tenant test dataset | Internal/Confidential aggregates per allowlist; no Restricted columns unless R10 approves | Batch held; manifest retained |
| AD-V12-H-05 Identity | IdP metadata invalid permanent; signature failure security event | Assertion ID replay cache | Test IdP tenants | Identity attributes only | Break-glass account (ENT-IDN-06) |
| AD-V12-H-06 Webhooks | Non-2xx/timeout retry per schedule; 410 disable | Event ID (receiver dedupe) | Sandbox endpoints | References and digests only | Delivery log + replay |
| AD-V12-H-07 SIEM | Sink unreachable retry with buffer ≤ 24 h | Sequence number per sink | Test collector | Audit events (redacted) | Buffer then alert R12/R10 |
| AD-V12-H-08 Tax | Unknown jurisdiction → `needs_rate_input` (never guessed) | Deterministic per input | — | Amounts, jurisdictions | Manual rate entry with approval |
| AD-V12-H-09 KMS | Key disabled → fail closed (data unreadable by design) | Key version | Test keys | Data keys only | None by design (crypto-shred semantics) |
| AD-V12-H-10 Status | Upload failure retry | Notice version | Staging site | Public notices only | Manual update by SRE |
| AD-V12-H-11 ESP alternates | As AD-01 | Message ID header | Provider sandboxes | As AD-01 | AD-01 |

### 11.8.5.9 Plugin decisions and FinOps controls (open-source first, paid by exception)

**Decisions for the components this part introduces.**

| Need | Decision | Component (licence, verify) | Why | Paid exception trigger |
|---|---|---|---|---|
| OpenAPI generation | Retain OSS | drf-spectacular (BSD-3-Clause) | Already in Part 3.2 | — |
| Breaking-change detection | Retain OSS | oasdiff (Apache-2.0) | CI gate for DEC-646 | — |
| Property-based contract tests | Retain OSS | Schemathesis (MIT) | 76 new + 330 V12 operations | — |
| SDK generation | Retain OSS | openapi-generator (Apache-2.0) | ENT-API-06 | — |
| Developer portal | Retain OSS | Static site from OpenAPI (e.g. Redoc, MIT) on the existing Vercel plan | No per-seat portal fees | — |
| Outbound webhooks | Replace (native) | Celery + outbox (no new service) | One-person operations; Svix OSS (MIT) considered and rejected for extra service to run | — |
| SCIM server | Retain OSS if justified | django-scim2 (MIT) or a thin in-house implementation after the RFC 7644 conformance suite | Small surface | — |
| SAML SP (only if the IdP cannot broker) | Retain OSS | pysaml2 (Apache-2.0) / python3-saml (MIT) | Avoid paid federation brokers | Paid IdP broker only if the existing IdP fails Sprint 0 check 13 and OSS is insufficient |
| Status page | Replace | Static page generated from approved notices on an independent host | ENT-OPS-02 independence | Hosted status SaaS only if the free static host is unsuitable (B27 ≤ ₹1,800/month, verify) |
| SMS / RCS | Conditional external service | DLT-registered aggregator | Carrier access cannot be self-hosted | Required for INT-04; B25 |
| Voice | Conditional external service | CPaaS | Telephony numbers | R3+; B26 |
| CRM sync | Conditional external service (tenant BYO) | Tenant's own CRM licence | Platform pays nothing | — |
| Tax for US | Conditional external service | Sales-tax provider | R5 only | Per-transaction fee |
| Contact data (INT-11, VND-02/04/14/23/31/33/35/85) | Replace core; licensed data only | — | Official contact paths first | Only after DEC-V9-04, CJ-R15 entry, DPA, CJ-GL-01, benchmark uplift and budget (B08/B18) |

**FinOps controls adopted (FSD 28 V5).**

| Control | Procedure | Owner | Evidence | Cadence |
|---|---|---|---|---|
| GC-09 shortlist rationalization | For every connector in a release: shortlist decision, owner, licence, privacy, support, TCO and fallback recorded on the IC/VND row; redundant candidates archived (state `archived`, no credential) | FinOps lead + Integration lead | IC/VND row + benchmark record | Each release gate |
| GC-10 BYO accounts | Installation `ownership = tenant_byo`; provider fees billed to the tenant by the provider; platform usage ledger excludes BYO provider costs; revocation of the credential blocks calls immediately | Integration lead | Usage ledger split; TC-V12-H-093 | Continuous |
| GC-11 volume and tier planning | API-V12-H-076 scenarios from 3-month usage forecast; include unused commitments; purchase decision outside the platform | FinOps lead | Scenario report | Quarterly from R3 |
| GC-13 self-service | Setup checklist and diagnostics per connector (API-V12-H-075); unresolved → support case | Support lead | Case links | Continuous |
| GC-15 idle resources | Weekly job flags connectors with no successful call in 30 days, idle infrastructure and orphaned artifacts as FinOps findings; owner review; **never auto-delete** | FinOps lead | Finding records; TC-V12-H-094 | Weekly |
| Paid-plugin activation | Part 7.4b PG-01…PG-10 plus CF-11; default **disabled** | FinOps lead + R10 | PG checklist | Per activation |

**Investor and market search (CONFLICT-890).** VND-54 Tavily and VND-73 Exa are labelled "Public market / investor search" in V12. The blueprint keeps them for **commercial market research only** (AD-05/AD-06); investor discovery and fundraising stay excluded by DEC-002 and the negative test TC-V12-H-095. VND-86 Bio Research and VND-95 Equity Research remain deferred ("No investment or confidential fundraising use in commercial product", V12).

### 11.8.5.10 API hosting under DEC-421 (ADR-209)

DEC-421 places the React frontends on Vercel (separate projects and origins), PostgreSQL on Supabase Pro (Mumbai) and the Django API, Celery, Valkey, SES and S3 on AWS ap-south-1. Part 3.2 assumed one CloudFront distribution per surface with same-origin path behaviours and **CORS disabled**. The API surfaces are therefore placed as follows.

| Surface | Public host | Platform | Path to the API | Authentication | Personal data in transit through |
|---|---|---|---|---|---|
| Website SPA (W01–W34), on startup domains and the platform site | Startup domains; `www.<platform-domain>` | Vercel project `web` | Vercel external rewrites `/api/*`, `/bff/web/*` → `web-origin.<platform-domain>` (AWS CloudFront + WAF → ALB, ap-south-1) | None / signed tokens / `__Host-` portal cookie | Vercel edge (TLS proxy) and AWS |
| Admin SPA (A001–A113 + V12 screens) | `admin.<platform-domain>` | Vercel project `admin` | Rewrites `/api/*`, `/bff/admin/*` → `admin-origin.<platform-domain>` (AWS) | `__Host-` BFF cookie + CSRF | Vercel edge and AWS |
| Provider webhooks | `hooks.<platform-domain>` | AWS only | Direct | Provider signatures | AWS only |
| Developer API, `/oauth/token`, `/scim/v2`, token callers of `/api/v2` | `api.<platform-domain>` | AWS only | Direct (CloudFront + WAF → ALB) | Bearer | AWS only |
| Developer portal (docs) | `developers.<platform-domain>` | Vercel static project | — | Public | None |
| Status page | `status.<independent-domain>` | Independent static host (RECOMMENDATION-900) | Static JSON published by AD-V12-H-10 | Public | None |
| Database | Private | Supabase Pro (Mumbai) | Django only, service key server-side; RLS enforced | — | AWS ↔ Supabase (TLS) |

**Controls.** Origin hosts accept requests only with a rotating `X-Origin-Verify` secret header injected by the Vercel rewrite (AWS WAF rule) or from the hooks/developer distributions; Vercel request logging is limited to metadata (no bodies) and its log drain excludes query strings with tokens; `__Host-` cookies remain host-only on the SPA origin, so CORS stays disabled for browsers; the developer host has CORS disabled (server-to-server). Supabase is never called from browsers and Supabase Auth is not used (DEC-421 unchanged).

**CONFLICT-889.** DEC-421 states that Vercel functions process no personal data. External rewrites are not functions, but they make Vercel's edge a TLS-terminating proxy for website and Admin API traffic, including personal data (leads, portal records). Options: **A (recommended)** keep same-origin through Vercel rewrites, add Vercel to the sub-processor list for transit only, configure metadata-only logging, and verify that Indian traffic is served from an Indian edge (verify, as of 27 Nov 2026); **B** serve each SPA's API from an AWS sibling host (`api-web.<startup-domain>`), which needs a certificate and DNS record per startup domain and credentialed CORS, and breaks `__Host-` cookie isolation for custom domains; **C** move the website SPA back to AWS CloudFront and keep only Admin on Vercel. Recommendation A; Founder decision required because it changes the data-flow statement of DEC-421 (DEC-652).

```mermaid
flowchart TD
  subgraph V["Vercel"]
    W["Website SPA project<br/>startup domains"]
    AD["Admin SPA project<br/>admin host"]
    DP["Developer portal<br/>static docs"]
  end
  subgraph A["AWS ap-south-1"]
    CF["CloudFront and WAF<br/>origin-verify rule"]
    WEB["api-web<br/>public, portal, bff-web"]
    ADM["api-admin<br/>admin, bff-admin, v2 session"]
    DEV["Developer host<br/>keys, OAuth, SCIM, v2 tokens"]
    HK["api-hooks<br/>provider webhooks"]
    WK["Celery workers<br/>dispatch, webhooks, sync"]
  end
  subgraph S["Supabase Mumbai"]
    DB["PostgreSQL with RLS"]
  end
  ST["Independent status host"]
  W -->|"rewrite /api and /bff"| CF
  AD -->|"rewrite /api and /bff"| CF
  CF --> WEB
  CF --> ADM
  CF --> DEV
  CF --> HK
  WEB --> DB
  ADM --> DB
  DEV --> DB
  HK --> DB
  WK --> DB
  WK -->|"signed outbound webhooks"| T["Tenant endpoints"]
  WK -->|"publish notices"| ST
```

### 11.8.5.11 Run gateway, SSO and SCIM design notes (ADR-207, ADR-208)

| Topic | Design |
|---|---|
| Run gateway resolution | `workflow_id` + `workflow_version` → pinned WorkflowRevision (BRL-AUT-03); `input` validated against `urn:sm:dto:<workflow_id>:v2#/$defs/input` (Appendix B, owned by Groups C/D) → 422 `SCHEMA_INVALID` with JSON-pointer `field_errors`; `business_context` must equal or narrow the caller's session or key scope (never widens; mismatch → 403) |
| Gate order | Authentication → scope → entitlement (ABAC-10) → quota → configuration revision active → approval requirement → budget reservation (IP-06) → enqueue; any failure returns `hold_reason` with rule IDs instead of a silent drop |
| Dry run | `dry_run=true` returns plan, gate reasons and cost estimate with zero external effects (OPT-API-01) |
| Consequential steps | Always end at an approval held for a human (API-V12-H-070 from a browser session with step-up); API keys and R20 cannot approve |
| SSO | Sprint 0 identity spike (DEC-019) gains **check 13**: per-tenant SAML 2.0/OIDC identity brokering with issuer/audience binding and `amr`/`acr` passthrough. Pass → AD-V12-H-05 configures the broker per tenant; fail → in-product SAML SP (pysaml2) behind the BFF |
| SSO enforcement | Only after domain verification (API-V12-H-019) and a break-glass account; break-glass use raises a SEV3 security event and notifies R01 and R10 |
| SCIM | Users map to memberships; groups map to role-mapping records reviewed by R12; deactivation revokes sessions, API keys and pending approvals within 15 minutes; conformance suite in CI |
| MFA policy floor | DEC-077 passkey requirement for R01, R02, R08–R12 and approvers cannot be lowered by tenant policy |

### 11.8.5.12 Security review of the new surfaces (API security lead)

| Threat (STRIDE) | Surface | Control | Test |
|---|---|---|---|
| S: stolen API key | Developer host | Hash-only storage, expiry ≤ 365 d, IP allowlist, prefix-based leak scanning (GitHub secret-scanning partner pattern, verify), anomaly alert on new ASN | TC-V12-H-077 |
| S: forged webhook to tenant | Outbound | HMAC + timestamp + event-ID dedupe; secret rotation overlap | TC-V12-H-082 |
| T: SCIM group grants admin | SCIM | Groups carry no privilege until R12 maps them; SoD check; audit | TC-V12-H-022…027 |
| R: denial of key actions | All | Audit events for key, client, endpoint, role, SSO changes; SIEM stream | TC-V12-H-033/034 |
| I: data leakage through webhook payloads | Outbound | Reference-only projection; scope check at subscription and at delivery | TC-V12-H-010 |
| I: SSRF via webhook URL, JWKS URL or SIEM endpoint | Admin | Private/link-local/metadata ranges blocked; DNS re-resolution per attempt; egress via NAT only | TC-V12-H-010, TC-V12-H-007 |
| D: noisy tenant through API keys | Developer host | RL-KEY per key and tenant; per-tenant worker concurrency | TC-V12-H-079 |
| E: API key performs consequential action | Developer host | No scope exists for approve/send/publish/launch/sign/pay/bid/price | TC-V12-H-068 |
| E: custom role combines request and approve | Admin | DB trigger `enforce_sod` + API check | TC-V12-H-030 |
| E: bearer token replayed on browser ingress | Browser ingress | Bearer rejected (401 `WRONG_AUDIENCE`) | TC-V12-H-096 |
| I: personal data through Vercel proxy logs | Website/Admin | Metadata-only logging; DPA; CONFLICT-889 | TC-V12-H-097 |
| T: tampered status page | Status host | Publish only approved notices; deploy token scoped to status bucket | TC-V12-H-046 |

### 11.8.5.13 Stories and acceptance criteria

| Story | Epic | As a … I want … so that … | FR | Release |
|---|---|---|---|---|
| US-01-YH01 | EP-01 | As a tenant administrator I want scoped, expiring API keys shown once so that our servers integrate without sharing passwords | FR-V12-H-001, 003 | Release 1 (pending CONFLICT-886) |
| US-01-YH02 | EP-01 | As an integration developer I want OAuth client credentials so that server tokens are short-lived and audience-bound | FR-V12-H-002 | Release 2 |
| US-01-YH03 | EP-01 | As a tenant administrator I want signed outbound webhooks with a delivery log and replay so that our systems react to deals and invoices reliably | FR-V12-H-005, 035 | Release 1 (pending CONFLICT-886) |
| US-01-YH04 | EP-01 | As a developer I want a portal with reference, guides and a sandbox so that I can build without production data | FR-V12-H-006, 007 | Release 2 |
| US-01-YH05 | EP-01 | As a tenant administrator I want SAML/OIDC SSO with verified domains and break-glass so that staff sign in with our IdP safely | FR-V12-H-036 | Release 1 (pending CONFLICT-887) |
| US-01-YH06 | EP-01 | As an IT administrator I want SCIM provisioning so that leavers lose access within 15 minutes | FR-V12-H-036 | Release 2 |
| US-01-YH07 | EP-01 | As a tenant administrator I want custom roles that cannot combine request and approve so that SoD holds | FR-V12-H-037 | Release 2 |
| US-01-YH08 | EP-01 | As an automation lead I want to install connectors behind an activation gate so that no channel goes live without review, DPA and registration | FR-V12-H-018, 022, 023 | Release 1 (pending CONFLICT-886) |
| US-03-YH01 | EP-03 | As a DPO I want to record withdrawals, open incidents with clocks and record notifications so that obligations are evidenced | FR-V12-H-013 | Release 1 |
| US-04-YH01 | EP-04 | As an AI lead I want model promotion to require passing suites and a kill switch effective in 60 s so that unsafe changes stop fast | FR-V12-H-012 | Release 1 |
| US-18-YH01 | EP-18 | As an integrator I want one run gateway with typed DTOs and dry-run so that I can start any approved workflow without bespoke endpoints | FR-V12-H-011 | Release 1 |
| US-20-YH01 | EP-20 | As a billing administrator I want invoice previews with tax lines so that customers see correct totals before issue | FR-V12-H-039 | Release 2 |
| US-21-YH01 | EP-21 | As an SRE I want to declare incidents and publish status on an independent host so that customers are informed during outages | FR-V12-H-041 | Release 2 |

**Acceptance criteria added in release v1.2** (Part 11.25 §11.25.3.6; these stories had a statement only). Format as the Part 5.1a template: one feature per story, a happy-path and a negative or edge scenario, IDs `AC-<epic><story>-nn`.

```gherkin
Feature: US-01-YH02 OAuth client credentials with short-lived, audience-bound tokens (FR-V12-H-002)
  @happy
  Scenario: AC-01YH02-01 Token issued for one audience and scope
    Given client "erp-connector" registered with scope "leads:read"
    When it requests a token with the client-credentials grant
    Then the token carries audience "api" and scope "leads:read" and expires within the configured lifetime
  @neg
  Scenario: AC-01YH02-02 Expired or wrong-audience token
    When an expired token or a token for another audience is presented
    Then the API returns 401 and no data is returned

Feature: US-01-YH04 Developer portal and sandbox without production data (FR-V12-H-006, FR-V12-H-007)
  @happy
  Scenario: AC-01YH04-01 Executable examples in the sandbox
    Given a developer signed in to the portal
    When she runs an example from the API reference
    Then it executes against the sandbox and the SDK contract tests pass against the sandbox
  @neg
  Scenario: AC-01YH04-02 No production data in the sandbox
    When the sandbox is queried for a production tenant's records
    Then nothing is returned and sandbox keys are rejected by production endpoints

Feature: US-03-YH01 Withdrawals, incidents with clocks and notifications (FR-V12-H-013)
  @happy
  Scenario: AC-03YH01-01 Incident clock
    Given the DPO opens a personal-data incident for an EU tenant
    Then the incident register starts the 72-hour notification clock and records each notification with timestamp
  @neg
  Scenario: AC-03YH01-02 Withdrawal stops processing
    When a data principal withdraws consent for marketing
    Then the consent ledger records the withdrawal and the next marketing send is blocked with CONSENT_WITHDRAWN

Feature: US-20-YH01 Invoice preview with tax lines (FR-V12-H-039)
  @happy
  Scenario: AC-20YH01-01 Tax per line from approved rules
    Given an invoice for an Indian customer in Karnataka billed from Karnataka
    When the billing administrator previews it
    Then each line shows CGST and SGST from the approved tax rule table and the total equals the sum in minor units
  @neg
  Scenario: AC-20YH01-02 No approved rule
    Given a market whose tax rules are not approved
    Then the preview is blocked with TAX_RULE_NOT_APPROVED and no invoice is issued

Feature: US-21-YH01 Incident declaration and independent status page (FR-V12-H-041)
  @happy
  Scenario: AC-21YH01-01 SEV1 published on the independent host
    Given the SRE declares a SEV1 incident
    Then an approved notice is published on the status host within 1 hour and updated every 2 hours
  @neg
  Scenario: AC-21YH01-02 Platform outage does not take the status page down
    Given the primary platform is unavailable
    Then the status page still serves from its independent host and an overdue critical vulnerability blocks the next release
```

```gherkin
Feature: API keys (US-01-YH01)
  Scenario: Key shown once and stored as hash
    Given tenant administrator "ta1" creates key "erp-sync" with scopes "leads:read"
    Then the response contains the secret once with "Cache-Control: no-store"
    And the api_key row holds prefix, last4 and key_hash but no plaintext
    And listing keys never returns the secret
  Scenario: Revoked key returns 401
    Given key "erp-sync" is revoked
    When a request presents the key 61 seconds later
    Then the response is 401 with code "API_KEY_REVOKED"
  Scenario: No consequential scope exists
    When "ta1" requests scope "messages:send"
    Then the response is 400 "VALIDATION_FAILED" with field_errors.scopes "unknown_scope"

Feature: Signed outbound webhooks (US-01-YH03)
  Scenario: Reference verifier rejects tampering and stale signatures
    Given an endpoint subscribed to "deal.stage_changed"
    When a delivery body is modified after signing
    Then the reference verifier returns false
    When a correctly signed delivery is received 301 seconds after GE-Timestamp
    Then the reference verifier returns false
  Scenario: Retries for 24 hours then exhausted
    Given the endpoint returns 500 to every attempt
    Then exactly 6 attempts are made within 24 hours
    And the delivery is marked "exhausted" and R12 is notified
  Scenario: Private address refused
    When "ta1" registers "https://10.0.0.5/hook"
    Then the response is 400 "VALIDATION_FAILED"

Feature: SSO enforcement guard (US-01-YH05)
  Scenario: Enforcement blocked without verified domain and break-glass
    Given SSO is configured but domain "acme.in" is pending
    When "ta1" sets enforced to true
    Then the response is 409 "INVALID_TRANSITION"
  Scenario: Break-glass use is a security event
    When the break-glass account signs in
    Then a SEV3 security event is raised and R01 and R10 are notified

Feature: SCIM de-provisioning (US-01-YH06)
  Scenario: Leaver loses access within 15 minutes
    Given user "u7" has an active session, an API key and a pending approval
    When the IdP sends PATCH active=false for "u7"
    Then within 15 minutes the session is revoked, the key is revoked and the approval is re-assigned

Feature: Custom role SoD (US-01-YH07)
  Scenario: Request and approve cannot coexist
    When "ta1" creates a role with "Runs:create" and "Runs:approve"
    Then the response is 403 "SEPARATION_OF_DUTIES"

Feature: Connector activation gate (US-01-YH08)
  Scenario: Production install needs reviews
    When "al1" installs "sms-dlt" in production without security_review_ref
    Then the response is 403 "GATE_INCOMPLETE"
  Scenario: Contact-data connector blocked
    Given DEC-V9-04 is open
    Then connector "contact-data" shows state "blocked_legal" and cannot be installed in production

Feature: Run gateway (US-18-YH01)
  Scenario: Invalid DTO rejected
    When a client posts a RunRequest whose input violates the Appendix B schema
    Then the response is 422 "SCHEMA_INVALID" with JSON-pointer field_errors
  Scenario: Duplicate request has no duplicate effect
    Given a run was accepted with Idempotency-Key "k1"
    When the same body is posted again with "k1"
    Then the stored 202 response is replayed with "Idempotent-Replayed: true"
  Scenario: API key cannot approve
    When an API-key caller posts an approval to a held run
    Then the response is 403 "FORBIDDEN"

Feature: AI kill switch (US-04-YH01)
  Scenario: Prompt stopped within 60 seconds
    When R11 activates the kill switch for prompt "draft-email-v12"
    Then within 60 seconds no model call uses that prompt and affected runs hold with reason "kill_switch"

Feature: Investor search stays excluded (DEC-002)
  Scenario: Market search cannot target investors
    When a research plan requests sources of category "investor discovery"
    Then the plan is rejected with rule "DEC-002"
```

### 11.8.5.14 Tests

**Operation contract tests (one per new operation).**

| Test | Operation | Route | Positive assertion | Negative / security assertions | Level | Priority |
|---|---|---|---|---|---|---|
| TC-V12-H-001 | API-V12-H-001 | GET ~/admin/developer/api-keys | Authorized role succeeds with documented status (200 Page of `{id, name, prefix, last4, scopes[], ip_allowlist[], expir…); audit row written | out-of-scope object → 404; unknown filter → 400 FILTER_NOT_ALLOWED; API key without read scope → 403 | Contract (Schemathesis/OpenAPI) + API SIT | P0 |
| TC-V12-H-002 | API-V12-H-002 | POST ~/admin/developer/api-keys | Authorized role succeeds with documented status (201 `{id, prefix, last4, secret (shown once), scopes, expires_at}`; he…); audit row written | requester approves own request → 403 SEPARATION_OF_DUTIES; changed payload after approval → 409 APPROVAL_VOIDED | Contract (Schemathesis/OpenAPI) + API SIT | P0 |
| TC-V12-H-003 | API-V12-H-003 | POST ~/admin/developer/api-keys/{id}/revoke | Authorized role succeeds with documented status (200 `{id, state: "revoked", revoked_at}`…); audit row written | missing Idempotency-Key → 400; stale If-Match/expected_version → 409 STALE_REVISION; role without permission → 403 | Contract (Schemathesis/OpenAPI) + API SIT | P0 |
| TC-V12-H-004 | API-V12-H-004 | POST ~/admin/developer/api-keys/{id}/rotate | Authorized role succeeds with documented status (201 `{id (new), prefix, last4, secret (once), predecessor_id, predeces…); audit row written | requester approves own request → 403 SEPARATION_OF_DUTIES; changed payload after approval → 409 APPROVAL_VOIDED | Contract (Schemathesis/OpenAPI) + API SIT | P0 |
| TC-V12-H-005 | API-V12-H-005 | POST /oauth/token | Authorized role succeeds with documented status (200 `{access_token (JWT, ≤ 15 min), token_type: "Bearer", expires_in, …); audit row written | out-of-scope object → 404; unknown filter → 400 FILTER_NOT_ALLOWED; API key without read scope → 403 | Contract (Schemathesis/OpenAPI) + API SIT | P1 |
| TC-V12-H-006 | API-V12-H-006 | GET ~/admin/developer/oauth-clients | Authorized role succeeds with documented status (200 Page of `{id, client_id, name, scopes[], auth_method, jwks_thumbpr…); audit row written | out-of-scope object → 404; unknown filter → 400 FILTER_NOT_ALLOWED; API key without read scope → 403 | Contract (Schemathesis/OpenAPI) + API SIT | P1 |
| TC-V12-H-007 | API-V12-H-007 | POST ~/admin/developer/oauth-clients | Authorized role succeeds with documented status (201 `{id, client_id, client_secret? (once, basic only)}`…); audit row written | requester approves own request → 403 SEPARATION_OF_DUTIES; changed payload after approval → 409 APPROVAL_VOIDED | Contract (Schemathesis/OpenAPI) + API SIT | P1 |
| TC-V12-H-008 | API-V12-H-008 | POST ~/admin/developer/oauth-clients/{id}/revoke | Authorized role succeeds with documented status (200 `{id, state: "revoked"}`…); audit row written | missing Idempotency-Key → 400; stale If-Match/expected_version → 409 STALE_REVISION; role without permission → 403 | Contract (Schemathesis/OpenAPI) + API SIT | P1 |
| TC-V12-H-009 | API-V12-H-009 | GET ~/admin/developer/webhooks | Authorized role succeeds with documented status (200 Page of `{id, url_masked, events[], active, secret_versions: [{ver…); audit row written | out-of-scope object → 404; unknown filter → 400 FILTER_NOT_ALLOWED; API key without read scope → 403 | Contract (Schemathesis/OpenAPI) + API SIT | P0 |
| TC-V12-H-010 | API-V12-H-010 | POST ~/admin/developer/webhooks | Authorized role succeeds with documented status (201 `{id, signing_secret (shown once), events, active: true}`…); audit row written | missing Idempotency-Key → 400; stale If-Match/expected_version → 409 STALE_REVISION; role without permission → 403 | Contract (Schemathesis/OpenAPI) + API SIT | P0 |
| TC-V12-H-011 | API-V12-H-011 | PATCH ~/admin/developer/webhooks/{id} | Authorized role succeeds with documented status (200 `{id, version, active, new_signing_secret? (once)}`…); audit row written | missing Idempotency-Key → 400; stale If-Match/expected_version → 409 STALE_REVISION; role without permission → 403 | Contract (Schemathesis/OpenAPI) + API SIT | P0 |
| TC-V12-H-012 | API-V12-H-012 | POST ~/admin/developer/webhooks/{id}/test | Authorized role succeeds with documented status (202 `{delivery_id, status_url}`…); audit row written | PDP deny at dispatch (emergency stop) → no external call; uncertain outcome blocks retry | Contract (Schemathesis/OpenAPI) + API SIT | P0 |
| TC-V12-H-013 | API-V12-H-013 | GET ~/admin/developer/webhook-deliveries | Authorized role succeeds with documented status (200 Page of `{delivery_id, endpoint_id, event, event_id, attempt (1..6…); audit row written | out-of-scope object → 404; unknown filter → 400 FILTER_NOT_ALLOWED; API key without read scope → 403 | Contract (Schemathesis/OpenAPI) + API SIT | P0 |
| TC-V12-H-014 | API-V12-H-014 | POST ~/admin/developer/webhook-deliveries/{id}/replay | Authorized role succeeds with documented status (202 `{delivery_id}`…); audit row written | PDP deny at dispatch (emergency stop) → no external call; uncertain outcome blocks retry | Contract (Schemathesis/OpenAPI) + API SIT | P0 |
| TC-V12-H-015 | API-V12-H-015 | GET ~/admin/identity/sso | Authorized role succeeds with documented status (200 `{protocol ∈ {SAML 2.0, OpenID Connect}, sso_url, issuer, domain, …); audit row written | out-of-scope object → 404; unknown filter → 400 FILTER_NOT_ALLOWED; API key without read scope → 403 | Contract (Schemathesis/OpenAPI) + API SIT | P0 |
| TC-V12-H-016 | API-V12-H-016 | PUT ~/admin/identity/sso | Authorized role succeeds with documented status (200 `{version, state ∈ {draft, tested, active}}`…); audit row written | missing Idempotency-Key → 400; stale If-Match/expected_version → 409 STALE_REVISION; role without permission → 403 | Contract (Schemathesis/OpenAPI) + API SIT | P0 |
| TC-V12-H-017 | API-V12-H-017 | POST ~/admin/identity/sso/test | Authorized role succeeds with documented status (202 `{test_id, login_url (expires 10 min)}`; result via `GET ~/admin/r…); audit row written | duplicate key, same body → replayed 202; same key, different body → 409 IDEMPOTENCY_KEY_REUSED | Contract (Schemathesis/OpenAPI) + API SIT | P0 |
| TC-V12-H-018 | API-V12-H-018 | POST ~/admin/identity/domains | Authorized role succeeds with documented status (201 `{id, domain, txt_name, txt_value, state: "pending"}`…); audit row written | missing Idempotency-Key → 400; stale If-Match/expected_version → 409 STALE_REVISION; role without permission → 403 | Contract (Schemathesis/OpenAPI) + API SIT | P0 |
| TC-V12-H-019 | API-V12-H-019 | POST ~/admin/identity/domains/{id}/verify | Authorized role succeeds with documented status (202 `{id, state ∈ {verified, pending, failed}, checked_at}`…); audit row written | duplicate key, same body → replayed 202; same key, different body → 409 IDEMPOTENCY_KEY_REUSED | Contract (Schemathesis/OpenAPI) + API SIT | P0 |
| TC-V12-H-020 | API-V12-H-020 | PUT ~/admin/identity/policies | Authorized role succeeds with documented status (200 `{version}`…); audit row written | requester approves own request → 403 SEPARATION_OF_DUTIES; changed payload after approval → 409 APPROVAL_VOIDED | Contract (Schemathesis/OpenAPI) + API SIT | P0 |
| TC-V12-H-021 | API-V12-H-021 | GET /scim/v2/Users | Authorized role succeeds with documented status (200 `ListResponse` (RFC 7643 User schema + enterprise extension)…); audit row written | out-of-scope object → 404; unknown filter → 400 FILTER_NOT_ALLOWED; API key without read scope → 403 | Contract (Schemathesis/OpenAPI) + API SIT | P1 |
| TC-V12-H-022 | API-V12-H-022 | POST /scim/v2/Users | Authorized role succeeds with documented status (201 User with `id`, `meta.version`…); audit row written | missing Idempotency-Key → 400; stale If-Match/expected_version → 409 STALE_REVISION; role without permission → 403 | Contract (Schemathesis/OpenAPI) + API SIT | P1 |
| TC-V12-H-023 | API-V12-H-023 | GET /scim/v2/Users/{id} | Authorized role succeeds with documented status (200 User…); audit row written | out-of-scope object → 404; unknown filter → 400 FILTER_NOT_ALLOWED; API key without read scope → 403 | Contract (Schemathesis/OpenAPI) + API SIT | P1 |
| TC-V12-H-024 | API-V12-H-024 | PATCH /scim/v2/Users/{id} | Authorized role succeeds with documented status (200 User…); audit row written | missing Idempotency-Key → 400; stale If-Match/expected_version → 409 STALE_REVISION; role without permission → 403 | Contract (Schemathesis/OpenAPI) + API SIT | P1 |
| TC-V12-H-025 | API-V12-H-025 | DELETE /scim/v2/Users/{id} | Authorized role succeeds with documented status (204…); audit row written | missing Idempotency-Key → 400; stale If-Match/expected_version → 409 STALE_REVISION; role without permission → 403 | Contract (Schemathesis/OpenAPI) + API SIT | P1 |
| TC-V12-H-026 | API-V12-H-026 | GET /scim/v2/Groups | Authorized role succeeds with documented status (200 ListResponse of Group…); audit row written | out-of-scope object → 404; unknown filter → 400 FILTER_NOT_ALLOWED; API key without read scope → 403 | Contract (Schemathesis/OpenAPI) + API SIT | P1 |
| TC-V12-H-027 | API-V12-H-027 | POST /scim/v2/Groups | Authorized role succeeds with documented status (201 Group…); audit row written | missing Idempotency-Key → 400; stale If-Match/expected_version → 409 STALE_REVISION; role without permission → 403 | Contract (Schemathesis/OpenAPI) + API SIT | P1 |
| TC-V12-H-028 | API-V12-H-028 | POST ~/admin/identity/scim-tokens | Authorized role succeeds with documented status (201 `{token_id, prefix, token (once)}` or 200 `{token_id, revoked_at}`…); audit row written | missing Idempotency-Key → 400; stale If-Match/expected_version → 409 STALE_REVISION; role without permission → 403 | Contract (Schemathesis/OpenAPI) + API SIT | P1 |
| TC-V12-H-029 | API-V12-H-029 | GET ~/admin/roles | Authorized role succeeds with documented status (200 Page of `{id, name, kind ∈ {builtin, custom}, permissions[] (resou…); audit row written | out-of-scope object → 404; unknown filter → 400 FILTER_NOT_ALLOWED; API key without read scope → 403 | Contract (Schemathesis/OpenAPI) + API SIT | P1 |
| TC-V12-H-030 | API-V12-H-030 | POST ~/admin/roles | Authorized role succeeds with documented status (201 `{id, version, state: "pending_approval"}`…); audit row written | requester approves own request → 403 SEPARATION_OF_DUTIES; changed payload after approval → 409 APPROVAL_VOIDED | Contract (Schemathesis/OpenAPI) + API SIT | P1 |
| TC-V12-H-031 | API-V12-H-031 | PATCH ~/admin/roles/{id} | Authorized role succeeds with documented status (200 `{version, state}`…); audit row written | requester approves own request → 403 SEPARATION_OF_DUTIES; changed payload after approval → 409 APPROVAL_VOIDED | Contract (Schemathesis/OpenAPI) + API SIT | P1 |
| TC-V12-H-032 | API-V12-H-032 | DELETE ~/admin/roles/{id} | Authorized role succeeds with documented status (204…); audit row written | missing Idempotency-Key → 400; stale If-Match/expected_version → 409 STALE_REVISION; role without permission → 403 | Contract (Schemathesis/OpenAPI) + API SIT | P1 |
| TC-V12-H-033 | API-V12-H-033 | GET ~/admin/siem-sinks | Authorized role succeeds with documented status (200 Page of `{id, kind, endpoint_masked, format, retention_years, last…); audit row written | out-of-scope object → 404; unknown filter → 400 FILTER_NOT_ALLOWED; API key without read scope → 403 | Contract (Schemathesis/OpenAPI) + API SIT | P1 |
| TC-V12-H-034 | API-V12-H-034 | POST ~/admin/siem-sinks | Authorized role succeeds with documented status (201 `{id, state: "pending_test"}`…); audit row written | requester approves own request → 403 SEPARATION_OF_DUTIES; changed payload after approval → 409 APPROVAL_VOIDED | Contract (Schemathesis/OpenAPI) + API SIT | P1 |
| TC-V12-H-035 | API-V12-H-035 | POST ~/admin/billing/invoices/preview | Authorized role succeeds with documented status (200 `{lines[{description, quantity, unit_price: Money, net: Money}], t…); audit row written | out-of-scope object → 404; unknown filter → 400 FILTER_NOT_ALLOWED; API key without read scope → 403 | Contract (Schemathesis/OpenAPI) + API SIT | P1 |
| TC-V12-H-036 | API-V12-H-036 | POST ~/admin/tax/quote | Authorized role succeeds with documented status (200 `{rule_id, rate_percent, tax_amount: Money, reverse_charge: b, nee…); audit row written | out-of-scope object → 404; unknown filter → 400 FILTER_NOT_ALLOWED; API key without read scope → 403 | Contract (Schemathesis/OpenAPI) + API SIT | P1 |
| TC-V12-H-037 | API-V12-H-037 | GET ~/admin/connectors | Authorized role succeeds with documented status (200 Page of `{connector_id, category, providers[], auth, scopes, gate:…); audit row written | out-of-scope object → 404; unknown filter → 400 FILTER_NOT_ALLOWED; API key without read scope → 403 | Contract (Schemathesis/OpenAPI) + API SIT | P0 |
| TC-V12-H-038 | API-V12-H-038 | POST ~/admin/connectors/{id}/installations | Authorized role succeeds with documented status (201 `{installation_id, state ∈ {sandbox_active, pending_gate, active}}…); audit row written | requester approves own request → 403 SEPARATION_OF_DUTIES; changed payload after approval → 409 APPROVAL_VOIDED | Contract (Schemathesis/OpenAPI) + API SIT | P0 |
| TC-V12-H-039 | API-V12-H-039 | GET ~/admin/encryption-keys | Authorized role succeeds with documented status (200 `{mode ∈ {platform, customer}, kms_key_ref_masked, rotation_days ∈…); audit row written | out-of-scope object → 404; unknown filter → 400 FILTER_NOT_ALLOWED; API key without read scope → 403 | Contract (Schemathesis/OpenAPI) + API SIT | P1 |
| TC-V12-H-040 | API-V12-H-040 | PUT ~/admin/encryption-keys | Authorized role succeeds with documented status (202 `{run_id}` (re-wrap job)…); audit row written | requester approves own request → 403 SEPARATION_OF_DUTIES; changed payload after approval → 409 APPROVAL_VOIDED | Contract (Schemathesis/OpenAPI) + API SIT | P1 |
| TC-V12-H-041 | API-V12-H-041 | GET ~/admin/sandboxes | Authorized role succeeds with documented status (200 Page of `{sandbox_id, name, copies_configuration, contains_persona…); audit row written | out-of-scope object → 404; unknown filter → 400 FILTER_NOT_ALLOWED; API key without read scope → 403 | Contract (Schemathesis/OpenAPI) + API SIT | P1 |
| TC-V12-H-042 | API-V12-H-042 | POST ~/admin/sandboxes | Authorized role succeeds with documented status (202 `{sandbox_id, run_id}`…); audit row written | duplicate key, same body → replayed 202; same key, different body → 409 IDEMPOTENCY_KEY_REUSED | Contract (Schemathesis/OpenAPI) + API SIT | P1 |
| TC-V12-H-043 | API-V12-H-043 | POST ~/admin/sandboxes/{id}/promotions | Authorized role succeeds with documented status (201 `{promotion_id, approval_id, state: "pending_review"}`…); audit row written | requester approves own request → 403 SEPARATION_OF_DUTIES; changed payload after approval → 409 APPROVAL_VOIDED | Contract (Schemathesis/OpenAPI) + API SIT | P1 |
| TC-V12-H-044 | API-V12-H-044 | GET ~/public/locales | Authorized role succeeds with documented status (200 `{items[{locale, direction ∈ {ltr, rtl}, coverage_percent, reviewe…); audit row written | out-of-scope object → 404; unknown filter → 400 FILTER_NOT_ALLOWED; API key without read scope → 403 | Contract (Schemathesis/OpenAPI) + API SIT | P0 |
| TC-V12-H-045 | API-V12-H-045 | POST ~/admin/ops/incidents | Authorized role succeeds with documented status (201 `{incident_id, status: "Investigating"}`…); audit row written | missing Idempotency-Key → 400; stale If-Match/expected_version → 409 STALE_REVISION; role without permission → 403 | Contract (Schemathesis/OpenAPI) + API SIT | P0 |
| TC-V12-H-046 | API-V12-H-046 | GET /status/v1/summary | Authorized role succeeds with documented status (200 `{components[{name, status}], incidents[{id, severity, status, sta…); audit row written | out-of-scope object → 404; unknown filter → 400 FILTER_NOT_ALLOWED; API key without read scope → 403 | Contract (Schemathesis/OpenAPI) + API SIT | P1 |
| TC-V12-H-047 | API-V12-H-047 | GET ~/admin/security/findings | Authorized role succeeds with documented status (200 Page of `{finding_id, title, severity, found_at, due_at, closed_at…); audit row written | out-of-scope object → 404; unknown filter → 400 FILTER_NOT_ALLOWED; API key without read scope → 403 | Contract (Schemathesis/OpenAPI) + API SIT | P0 |
| TC-V12-H-048 | API-V12-H-048 | POST ~/admin/security/findings | Authorized role succeeds with documented status (201 `{finding_id, due_at}`…); audit row written | missing Idempotency-Key → 400; stale If-Match/expected_version → 409 STALE_REVISION; role without permission → 403 | Contract (Schemathesis/OpenAPI) + API SIT | P0 |
| TC-V12-H-049 | API-V12-H-049 | GET ~/admin/ai/models | Authorized role succeeds with documented status (200 Page of `{id, provider, model_id, tier ∈ {0,1a,1b,2,3}, max_data_c…); audit row written | out-of-scope object → 404; unknown filter → 400 FILTER_NOT_ALLOWED; API key without read scope → 403 | Contract (Schemathesis/OpenAPI) + API SIT | P0 |
| TC-V12-H-050 | API-V12-H-050 | POST ~/admin/ai/models/{id}/promotion-requests | Authorized role succeeds with documented status (201 `{approval_id, state: "pending"}`…); audit row written | requester approves own request → 403 SEPARATION_OF_DUTIES; changed payload after approval → 409 APPROVAL_VOIDED | Contract (Schemathesis/OpenAPI) + API SIT | P0 |
| TC-V12-H-051 | API-V12-H-051 | GET ~/admin/ai/prompts | Authorized role succeeds with documented status (200 Page of `{id, task_key, version, status, author, approved_by, eval…); audit row written | out-of-scope object → 404; unknown filter → 400 FILTER_NOT_ALLOWED; API key without read scope → 403 | Contract (Schemathesis/OpenAPI) + API SIT | P0 |
| TC-V12-H-052 | API-V12-H-052 | GET ~/admin/ai/eval-suites | Authorized role succeeds with documented status (200 Page of `{id, name, task_keys[], case_count, metrics[{name, thresh…); audit row written | out-of-scope object → 404; unknown filter → 400 FILTER_NOT_ALLOWED; API key without read scope → 403 | Contract (Schemathesis/OpenAPI) + API SIT | P0 |
| TC-V12-H-053 | API-V12-H-053 | GET ~/admin/ai/red-team/results | Authorized role succeeds with documented status (200 Page of `{run_id, suite: "AI-INJ", passed, failed, denominator, fi…); audit row written | out-of-scope object → 404; unknown filter → 400 FILTER_NOT_ALLOWED; API key without read scope → 403 | Contract (Schemathesis/OpenAPI) + API SIT | P0 |
| TC-V12-H-054 | API-V12-H-054 | POST ~/internal/ai/content-screen | Authorized role succeeds with documented status (200 `{flags[{kind ∈ {prompt_injection, pii, secret, malware_link, poli…); audit row written | out-of-scope object → 404; unknown filter → 400 FILTER_NOT_ALLOWED; API key without read scope → 403 | Contract (Schemathesis/OpenAPI) + API SIT | P0 |
| TC-V12-H-055 | API-V12-H-055 | GET ~/admin/ai/usage | Authorized role succeeds with documented status (200 `{rows[{key, calls, input_tokens, output_tokens, cost: Money, acce…); audit row written | out-of-scope object → 404; unknown filter → 400 FILTER_NOT_ALLOWED; API key without read scope → 403 | Contract (Schemathesis/OpenAPI) + API SIT | P0 |
| TC-V12-H-056 | API-V12-H-056 | POST ~/admin/ai/kill-switch | Authorized role succeeds with documented status (200 `{kill_id, effective_at}`…); audit row written | missing Idempotency-Key → 400; stale If-Match/expected_version → 409 STALE_REVISION; role without permission → 403 | Contract (Schemathesis/OpenAPI) + API SIT | P0 |
| TC-V12-H-057 | API-V12-H-057 | GET ~/admin/jurisdiction-rules/{id}/rules | Authorized role succeeds with documented status (200 Page of `{rule_id, channel, purpose, effect, legal_source, status …); audit row written | out-of-scope object → 404; unknown filter → 400 FILTER_NOT_ALLOWED; API key without read scope → 403 | Contract (Schemathesis/OpenAPI) + API SIT | P0 |
| TC-V12-H-058 | API-V12-H-058 | GET ~/admin/consents | Authorized role succeeds with documented status (200 Page of `{consent_id, subject_ref, channel, purpose, notice_versio…); audit row written | out-of-scope object → 404; unknown filter → 400 FILTER_NOT_ALLOWED; API key without read scope → 403 | Contract (Schemathesis/OpenAPI) + API SIT | P0 |
| TC-V12-H-059 | API-V12-H-059 | POST ~/admin/consents/{id}/withdraw | Authorized role succeeds with documented status (200 `{consent_id, state: "withdrawn", suppressions_added, cancelled_me…); audit row written | missing Idempotency-Key → 400; stale If-Match/expected_version → 409 STALE_REVISION; role without permission → 403 | Contract (Schemathesis/OpenAPI) + API SIT | P0 |
| TC-V12-H-060 | API-V12-H-060 | POST ~/admin/compliance/incidents | Authorized role succeeds with documented status (201 `{incident_id, clocks[{authority, deadline_at}]}`…); audit row written | missing Idempotency-Key → 400; stale If-Match/expected_version → 409 STALE_REVISION; role without permission → 403 | Contract (Schemathesis/OpenAPI) + API SIT | P0 |
| TC-V12-H-061 | API-V12-H-061 | POST ~/admin/compliance/incidents/{id}/notifications | Authorized role succeeds with documented status (201 `{notification_id, clock_state ∈ {met, late}}`…); audit row written | maker = checker → 403; missing evidence → 400 | Contract (Schemathesis/OpenAPI) + API SIT | P0 |
| TC-V12-H-062 | API-V12-H-062 | POST ~/public/cookie-consents | Authorized role succeeds with documented status (201 `{consent_token, expires_at}`…); audit row written | missing Idempotency-Key → 400; stale If-Match/expected_version → 409 STALE_REVISION; role without permission → 403 | Contract (Schemathesis/OpenAPI) + API SIT | P0 |
| TC-V12-H-063 | API-V12-H-063 | POST ~/admin/portfolio/grants | Authorized role succeeds with documented status (200 `{grant_id, version}`…); audit row written | requester approves own request → 403 SEPARATION_OF_DUTIES; changed payload after approval → 409 APPROVAL_VOIDED | Contract (Schemathesis/OpenAPI) + API SIT | P0 |
| TC-V12-H-064 | API-V12-H-064 | GET ~/admin/metrics/business | Authorized role succeeds with documented status (200 `{rows[{dims, counts, native_totals[{currency, amount}], converted…); audit row written | out-of-scope object → 404; unknown filter → 400 FILTER_NOT_ALLOWED; API key without read scope → 403 | Contract (Schemathesis/OpenAPI) + API SIT | P0 |
| TC-V12-H-065 | API-V12-H-065 | GET ~/admin/optimization/cost-summary | Authorized role succeeds with documented status (200 Page of `{category, allocated: Money, unallocated: Money, accepted…); audit row written | out-of-scope object → 404; unknown filter → 400 FILTER_NOT_ALLOWED; API key without read scope → 403 | Contract (Schemathesis/OpenAPI) + API SIT | P1 |
| TC-V12-H-066 | API-V12-H-066 | GET ~/portal/service/value | Authorized role succeeds with documented status (200 `{accepted_outputs, usage, value_assumption{basis, stated_by}, ren…); audit row written | out-of-scope object → 404; unknown filter → 400 FILTER_NOT_ALLOWED; API key without read scope → 403 | Contract (Schemathesis/OpenAPI) + API SIT | P1 |
| TC-V12-H-067 | API-V12-H-067 | GET ~/admin/operator/conversion-metrics | Authorized role succeeds with documented status (200 `{stages[{name, count}], attribution_quality, acquisition_cost: Mo…); audit row written | out-of-scope object → 404; unknown filter → 400 FILTER_NOT_ALLOWED; API key without read scope → 403 | Contract (Schemathesis/OpenAPI) + API SIT | P1 |
| TC-V12-H-068 | API-V12-H-068 | POST /api/v2/workflow-runs | Authorized role succeeds with documented status (202 `{run_id, state, hold_reason?, reservation{amount: Money}, correla…); audit row written | duplicate key, same body → replayed 202; same key, different body → 409 IDEMPOTENCY_KEY_REUSED | Contract (Schemathesis/OpenAPI) + API SIT | P0 |
| TC-V12-H-069 | API-V12-H-069 | GET /api/v2/workflow-runs/{id} | Authorized role succeeds with documented status (200 `{state, step_states[], result_ref, error?, usage{tokens, cost: Mo…); audit row written | out-of-scope object → 404; unknown filter → 400 FILTER_NOT_ALLOWED; API key without read scope → 403 | Contract (Schemathesis/OpenAPI) + API SIT | P0 |
| TC-V12-H-070 | API-V12-H-070 | POST /api/v2/workflow-runs/{id}/approvals | Authorized role succeeds with documented status (200 `{approval_ref, state}`…); audit row written | requester approves own request → 403 SEPARATION_OF_DUTIES; changed payload after approval → 409 APPROVAL_VOIDED | Contract (Schemathesis/OpenAPI) + API SIT | P0 |
| TC-V12-H-071 | API-V12-H-071 | POST /api/v2/workflow-runs/{id}/cancel | Authorized role succeeds with documented status (200 `{state}`…); audit row written | missing Idempotency-Key → 400; stale If-Match/expected_version → 409 STALE_REVISION; role without permission → 403 | Contract (Schemathesis/OpenAPI) + API SIT | P0 |
| TC-V12-H-072 | API-V12-H-072 | GET /api/v2/workflow-runs/{id}/steps | Authorized role succeeds with documented status (200 Page of `{step_id (STEP-…), state, started_at, ended_at, artifact_…); audit row written | out-of-scope object → 404; unknown filter → 400 FILTER_NOT_ALLOWED; API key without read scope → 403 | Contract (Schemathesis/OpenAPI) + API SIT | P0 |
| TC-V12-H-073 | API-V12-H-073 | POST /api/v2/connectors/{kind}/events | Authorized role succeeds with documented status (200 `{receipt_id}` (duplicate → 200, no effect)…); audit row written | bad signature → 401 and payload discarded; duplicate event ID → 200 no effect | Contract (Schemathesis/OpenAPI) + API SIT | P0 |
| TC-V12-H-074 | API-V12-H-074 | GET ~/admin/connectors/health-summary | Authorized role succeeds with documented status (200 `{rows[{installation_id, kind, state, sync_lag_s, error_rate, brea…); audit row written | out-of-scope object → 404; unknown filter → 400 FILTER_NOT_ALLOWED; API key without read scope → 403 | Contract (Schemathesis/OpenAPI) + API SIT | P1 |
| TC-V12-H-075 | API-V12-H-075 | POST ~/admin/integrations/{id}/diagnostics | Authorized role succeeds with documented status (202 `{run_id}` → `{checks[{id, result, remedy_key}], escalation_case_i…); audit row written | duplicate key, same body → replayed 202; same key, different body → 409 IDEMPOTENCY_KEY_REUSED | Contract (Schemathesis/OpenAPI) + API SIT | P1 |
| TC-V12-H-076 | API-V12-H-076 | POST ~/admin/finops/provider-tier-scenarios | Authorized role succeeds with documented status (202 → `{scenarios[{tier, commitment: Money, expected_overage: Money, u…); audit row written | duplicate key, same body → replayed 202; same key, different body → 409 IDEMPOTENCY_KEY_REUSED | Contract (Schemathesis/OpenAPI) + API SIT | P1 |


**Requirement-level tests.**

| Test | Requirement | Assertion | Level | Priority |
|---|---|---|---|---|
| TC-V12-H-077 | FR-V12-H-001 | Database inspection finds no plaintext key; revoked key → 401 within 60 s; leaked-prefix scanner pattern matches | Security SIT | P0 |
| TC-V12-H-078 | FR-V12-H-002 | Wrong audience, missing scope and expired token rejected | Security SIT | P1 |
| TC-V12-H-079 | FR-V12-H-003 | k6 load: key A at 5× limit gets 429 with Retry-After; tenant B p95 unchanged ± 10% (noisy-tenant isolation) | Performance | P0 |
| TC-V12-H-080 | FR-V12-H-004 | Deprecated operation returns `Deprecation` and `Sunset` ≥ 12 months ahead; changelog entry exists; oasdiff gate blocks unannounced breaking change | CI | P1 |
| TC-V12-H-081 | FR-V12-H-010 | Registry check fails on a duplicate method+path or an unmapped Appendix A/A2 operationId | CI | P0 |
| TC-V12-H-082 | FR-V12-H-005 | Reference verifier: tampered body, wrong secret, timestamp skew > 300 s and replayed event ID all rejected; valid delivery accepted | Unit + SIT | P0 |
| TC-V12-H-083 | FR-V12-H-006 | Generated TypeScript and Python SDK contract tests pass against the sandbox | CI | P2 |
| TC-V12-H-084 | FR-V12-H-007 | Every portal example executes in the sandbox tenant and never reaches a live adapter | E2E | P1 |
| TC-V12-H-085 | FR-V12-H-019 | Secret scan of repository, logs and a database dump with seeded secrets: zero findings | Security | P0 |
| TC-V12-H-086 | FR-V12-H-024 | Email and WhatsApp accounts for two markets survive the MOB-16 handoff and keep independent eligibility | SIT | P0 |
| TC-V12-H-087 | FR-V12-H-025 | Two senders under one channel; using another company's account → 404 | SIT | P0 |
| TC-V12-H-088 | FR-V12-H-026 | Unchanged source: ETag 304, no full fetch; injected missed event repaired once, no duplicate | SIT | P1 |
| TC-V12-H-089 | FR-V12-H-020 | Provider outage simulation: breaker opens, no event lost, uncertain writes reconciled before retry | Resilience | P1 |
| TC-V12-H-090 | FR-V12-H-034 | MOB-16-AT01: both directions, two markets, two accounts, 39 SKUs, duplicate rejection, no subscription activation on import | E2E | P1 |
| TC-V12-H-091 | FR-V12-H-022, 033 | Production installation without reviews → 403 `GATE_INCOMPLETE`; contact-data connector `blocked_legal` | SIT | P0 |
| TC-V12-H-092 | FR-V12-H-021 | Staging connector failure fires health alert within threshold | SIT | P1 |
| TC-V12-H-093 | FR-V12-H-028 | BYO installation: provider cost absent from platform ledger; credential revocation blocks the next call | SIT | P1 |
| TC-V12-H-094 | FR-V12-H-031 | Idle connector fixture flagged; active and retained resources not deleted | SIT | P1 |
| TC-V12-H-095 | DEC-002, DEC-656 | No route, scope, source category or connector enables investor discovery or fundraising | Negative | P0 |
| TC-V12-H-096 | DEC-641, DEC-643 | All 282 + 48 + 76 operations: list responses carry `items`/`next_cursor`; errors carry `code`, `message`, `correlation_id`; bearer token on browser ingress → 401 | Contract | P0 |
| TC-V12-H-097 | DEC-652 | Website and Admin API calls through the Vercel rewrite keep `__Host-` cookies; origin rejects requests without origin-verify header; Vercel logs contain no bodies | Security E2E | P0 |

### 11.8.5.15 Effort and cost (separately approvable proposal CR-V12-H-01)

This proposal does **not** change Ledger A (DEC-230), the running budget (DEC-422), CR-ALN-01 (DEC-416) or the A1 approval (DEC-417). Development (one-time) and running (recurring) costs are in separate tables. Rates: ₹4,545–6,818 per person-day (Part 8.4 §8.4.2.1); central uses ₹5,682. AI-built delivery (DEC-420) may reduce effort after the Sprint 2 gate; not assumed here.

**Development (one-time).**

| Work package | Scope | pd low / central / high | ₹ low / central / high |
|---|---|---|---|
| H1 Developer platform | API keys, OAuth CC, RL-KEY, webhook engine, delivery log and replay, portal from OpenAPI, sandbox wiring (API-V12-H-001…014) | 18 / 26 / 36 | 0.82 / 1.48 / 2.45 L |
| H2 Identity APIs | SSO config/test, domains, policies, break-glass, SCIM 7 + tokens (API-V12-H-015…028); engine work counted by the identity owner group, not here | 14 / 21 / 30 | 0.64 / 1.19 / 2.05 L |
| H3 Access, audit, ops, security | Custom roles + SoD, SIEM sinks, incident declare, public status, locales, findings | 9 / 13 / 18 | 0.41 / 0.74 / 1.23 L |
| H4 Billing, tax, data | Invoice preview, tax quote, sandboxes, promotion, key configuration (platform mode) | 8 / 12 / 17 | 0.36 / 0.68 / 1.16 L |
| H5 AI governance and compliance routes | API-V12-H-049…062 | 9 / 13 / 18 | 0.41 / 0.74 / 1.23 L |
| H6 Run gateway and metrics | API-V12-H-063…073 | 8 / 12 / 17 | 0.36 / 0.68 / 1.16 L |
| H7 Connector framework | Catalogue, installation gate, health summary, diagnostics, CF-01…12 base classes | 8 / 12 / 17 | 0.36 / 0.68 / 1.16 L |
| H8 Adapters R1–R2 | CRM (one provider) 8/12/16; SMS-DLT 6/9/12; warehouse export 4/6/9; SIEM sink 3/4/6 | 21 / 31 / 43 | 0.95 / 1.76 / 2.93 L |
| H9 Convention migration | Page/Error/version/Command, x-v12 registry fields, CI gates, regenerated clients | 5 / 8 / 11 | 0.23 / 0.45 / 0.75 L |
| H10 Tests and evidence | 97 TC-V12-H tests, SCIM conformance, k6 per-key load, webhook verifier | 10 / 15 / 21 | 0.45 / 0.85 / 1.43 L |
| **Subtotal R1–R2** | | **110 / 163 / 228** | **₹5.00 / 9.26 / 15.55 L** |
| Later (R3+, W6 or Year 2) | Voice CPaaS 8/12/16; BYOK KMS 6/9/13; Java SDK and SDK publishing 3/5/7; US tax provider 3/5/8 | 20 / 31 / 44 | ₹0.91 / 1.76 / 3.00 L |
| External one-time | Developer-API scope added to the R1 penetration test (verify quote) | — | ₹0.5–1.5 L |

**Overlap.** If Part 9.9 A3 (CAP-X3-23 developer platform, CAP-X3-15 BYOK, CAP-X3-12 status page) is later approved, its estimate must be reduced by H1, the BYOK line and the status work here; they are the same capabilities pulled forward by V12.

**Running (recurring, per month, pilot; verify).**

| Line | Item | ₹ / month | Basis |
|---|---|---|---|
| B01c (existing AWS) | Webhook and sync workers, developer host on the existing ALB/CloudFront | 0–900 | Incremental compute within current instances; +1 small worker at peak |
| B25 (new, proposal) | SMS-DLT: ≈ 2,000 SMS × ₹0.15–0.30 (verify) + registration amortized | 300–1,000 | Pilot volume equal to the BRD §6 email pilot assumption |
| B27 (new, proposal) | Independent status host | 0–1,800 | Free static tier to paid status SaaS (verify) |
| — | CRM, warehouse, SIEM, KMS | 0 | Tenant-owned (BYO) |
| — | Developer portal on Vercel | 0 | Existing Pro plan (DEC-421) |
| **Total** | | **₹300–3,700** | Within the 15% contingency (B11) first; remainder by change control on DEC-422 |

---

## 11.8.6 Conflicts and proposed resolutions

| Tag | Conflict | V12 position | Blueprint / Founder position | Proposed resolution | Status |
|---|---|---|---|---|---|
| CONFLICT-886 | Developer platform and connector framework in R1 | ENT-API-01/03/05 and ENT-INT-01/05 are P0 in R1 (private beta) | Part 9.9a CAP-X3-23 in A3 (Year 2), not approved (DEC-417 approves A1 only); Release 1 budget/team/dates fixed (DEC-228, DEC-230, DEC-422) | Adopt V12 requirements. Fund CR-V12-H-01 H1, H7 and the R1 part of H10 (≈ 36 / 53 / 74 pd) as a change request; if the Founder declines, deliver them in Release 2 and keep Release 1 private beta on browser-only access | **Adopted (DEC-785)** (DEC-644, DEC-657) |
| CONFLICT-887 | Enterprise identity in R1/R2 | SSO, domains, MFA policy, break-glass R1; SCIM, custom roles R2 | DEC-019 shared IdP; no per-tenant SSO/SCIM/custom roles; budgets as above | Adopt; SSO in Release 1 only if the IdP passes Sprint 0 check 13 (brokering) at no licence cost; SCIM and custom roles in Release 2 | **Adopted (DEC-784)** (DEC-648, DEC-657) |
| CONFLICT-888 | New connector kinds | CRM and SMS-DLT connectors in R1; voice SVC-26; warehouse | Native CRM only; "no SMS in W0–W5" (Part 3.2 AD-02 fallback); no voice | Adopt as adapters AD-V12-H-01…04; CRM as tenant BYO (no platform licence); SMS-DLT funded via B25; voice R3+ | **Adopted (DEC-785)** (DEC-650, DEC-657) |
| CONFLICT-889 | API ingress under DEC-421 | — (V12 is host-neutral) | DEC-421: Vercel functions process no personal data; Part 3.2 same-origin, CORS disabled | Option A Vercel rewrites with transit-only DPA and metadata logging (§11.8.5.10) | **Adopted (DEC-786)** (DEC-652) |
| CONFLICT-890 | "Investor search" label on VND-54/73 | Category "Public market / investor search" | DEC-002 excludes investor discovery and fundraising | Use for commercial market research only; investor use excluded; negative test TC-V12-H-095 | Resolved (DEC-656; consistent with DEC-002, no change to a Founder decision) |
| CONFLICT-891 | Bearer JWT as the global security scheme | Appendix A/A2 `bearerAuth` JWT | DEC-019: no bearer tokens from browsers | Two schemes; bearer only on the developer host, SCIM and token callers of `/api/v2` | Resolved (DEC-643) |
| CONFLICT-892 | Pagination, version field, deprecation period, outbound webhooks | Page {items, next_cursor}, limit ≤ 200; Record.version; ≥ 12 months; signed webhooks | Part 3.2 {data, page}, ≤ 100; revision; ≥ 6 months; webhooks not offered | Adopt V12 (blueprint text, not a Founder decision) | Resolved (DEC-641, DEC-645, DEC-646) |

## 11.8.7 Decisions

| DEC | Decision | Authority | Effect |
|---|---|---|---|
| DEC-640 | **Contract authority and registry:** Appendix A/A2 and the FSD 25 candidates are mapped onto the Part 3.2 registry by operationId (`operationId` = V12 name, `x-blueprint-op`, `x-v12-path`, `x-v12-tag`, `x-source-op`); no duplicate mounting; new namespaces only for `/api/v2` run gateway, `/scim/v2`, `/oauth/token`; two served route aliases RA-V12-H-01/02; historical operations absent from Appendix A retained | Customer revision V12 (28 Nov 2026) | Registry rules R-1…R-7; CI gates; amends Part 3.2 §3.2.1.14 operationId rule |
| DEC-641 | **Wire conventions:** list `{items, next_cursor}`, `limit` default 50 max 200; wire field `version`; `expected_version` accepted; error envelope superset `{code, message, correlation_id, field_errors}` + RFC 9457 members | Customer revision V12 (28 Nov 2026) | Amends Part 3.2 §3.2.1.6, §3.2.1.8, §3.2.1.9 |
| DEC-642 | **Status codes:** blueprint superset declared on every operation; `422 SCHEMA_INVALID` added; new codes `API_KEY_REVOKED`, `API_KEY_EXPIRED`, `TOKEN_EXPIRED`, `INSUFFICIENT_SCOPE`, `IP_NOT_ALLOWED`, `VERSION_PRECONDITION_MISMATCH`, `GATE_INCOMPLETE`, `CHECK_PENDING` | Customer revision V12 (28 Nov 2026) | Amends Part 3.2 §3.2.1.9–10 |
| DEC-643 | **Security schemes:** `bffSession` for browser namespaces (DEC-019 unchanged); `bearerAuth` (API keys, OAuth JWT, SCIM tokens) only on the developer host and token callers of `/api/v2`; bearer on browser ingress → 401 | Customer revision V12 (28 Nov 2026) | Resolves CONFLICT-891; ADR-205 |
| DEC-644 | **Developer platform phase:** ENT-API-01/03/05 in Release 1, ENT-API-02/04/07 in Release 2, ENT-API-06 in W6 | **Adopted (DEC-785)** | CONFLICT-886; supersedes the A3 placement of CAP-X3-23 if approved |
| DEC-645 | **Outbound webhooks offered:** HMAC-SHA-256 over timestamp + event ID + body, ± 300 s freshness, 6 attempts in 24 h, delivery log and replay, reference-only projection of 24 event types | Customer revision V12 (28 Nov 2026) | Amends Part 3.2 §3.2.1.13 ("not offered"); ADR-206; delivery timing follows DEC-644 |
| DEC-646 | **Deprecation:** ≥ 12 months' notice for breaking changes to published contracts; headers, changelog, notice to key owners; Admin-only operations keep the release-coupled rule | Customer revision V12 (28 Nov 2026) | Amends Part 3.2 §3.2.1.3 |
| DEC-647 | **Run gateway** `/api/v2/workflow-runs` (create, read, approvals, cancel, steps) with RunRequest/BusinessContext DTOs, Appendix B validation, dry run, gate order of §11.8.5.11 | Customer revision V12 (28 Nov 2026) | ADR-208; v2 namespace introduced without retiring v1 |
| DEC-648 | **Enterprise identity and access APIs:** SSO per tenant, domain verification, MFA/session policy with DEC-077 floor, break-glass, SCIM 2.0, custom roles with SoD | **Adopted (DEC-784)** (release and funding) | CONFLICT-887; ADR-207; Sprint 0 identity check 13 |
| DEC-649 | **Connector framework and activation gate** CF-01…12; contact-data connectors blocked until DEC-V9-04 closes (stricter than the AD-19 W1 pilot) | Customer revision V12 (28 Nov 2026) | Amends Part 3.2 AD-19 wave; adds CF-11 to Part 7.4b PG gate |
| DEC-650 | **New adapters** AD-V12-H-01…11 (CRM BYO, SMS-DLT/RCS, voice, warehouse, identity federation, webhook delivery, SIEM, tax, tenant KMS, status publisher, ESP alternates) | **Adopted (DEC-785)** for CRM and SMS-DLT in Release 1; others Customer revision V12 | CONFLICT-888 |
| DEC-651 | **Plugin register:** VND-01…97 adopted as canonical IDs on the matching IC rows; decisions unchanged; GC-09/10/11/13/15 procedures adopted; OSS components of §11.8.5.9 | Customer revision V12 (28 Nov 2026) | Part 7.4a register keyed by VND; F_integration_candidates unchanged |
| DEC-652 | **API hosting under DEC-421:** API ingress on AWS; SPAs on Vercel reach the API through external rewrites (Option A) with origin-verify and metadata-only logging; webhooks, developer API and SCIM direct to AWS | **Adopted (DEC-786)** | CONFLICT-889; ADR-209 |
| DEC-653 | **Status page** on an independent static host fed by approved notices | Customer revision V12 (28 Nov 2026) | ENT-OPS-02; RECOMMENDATION-900; B27 proposal |
| DEC-654 | **Event catalogue additions:** 24 rows / 49 event types and the outbound projection v1 | Customer revision V12 (28 Nov 2026) | Adds to Part 3.2 §3.2.3.3 |
| DEC-655 | **V12 phase mapping** R0/R1 → Release 1, R2 → Release 2, R3 → W6, R4/R5 → Year 2+ for API and integration scope | Customer revision V12 (28 Nov 2026), subject to DEC-644/648/650 | ASSUMPTION-893 |
| DEC-656 | **Market search providers** (VND-54/73) limited to commercial market research; investor discovery stays excluded | Customer revision V12 (28 Nov 2026), consistent with DEC-002 | CONFLICT-890 resolved |
| DEC-657 | **CR-V12-H-01** development ₹5.00 / 9.26 / 15.55 L (R1–R2) + ₹0.91–3.00 L later + ₹0.5–1.5 L pen-test scope; running ₹300–3,700/month | **Adopted (DEC-790)** | Outside Ledger A and DEC-422 |
| DEC-658 | **MOB-16 handoff in production** uses the authenticated server-owned application draft (API-504 revision, API-ENH-D-019 read); the JSON fingerprint is demo-only | Customer revision V12 (28 Nov 2026) | FR-V12-H-034 |
| DEC-659 | **V8 AI-governance and compliance routes** adopted (API-V12-H-049…062 plus aliases) | Customer revision V12 (28 Nov 2026) | FR-V12-H-012/013 |

**ADRs.**

| ADR | Title | Decision | Alternatives rejected |
|---|---|---|---|
| ADR-205 | Developer API as a separate host and audience | `api.<platform-domain>` on AWS; API keys (HMAC-hashed) and OAuth client-credentials JWT; scopes map to RBAC and are draft-only for consequential domains | Bearer tokens on browser ingress (breaks DEC-019); third-party API gateway SaaS (cost, data path) |
| ADR-206 | Outbound webhook engine on outbox + Celery | Projection worker, HMAC v1 signature, 6-attempt schedule, delivery log, replay | Svix OSS (extra service), hosted webhook SaaS (paid, data transfer) |
| ADR-207 | Enterprise SSO and SCIM | Broker per-tenant SSO through the existing IdP if check 13 passes, else pysaml2 SP; SCIM server in Django mapped to memberships | Paid federation broker; IdP-assigned roles without review |
| ADR-208 | Run gateway as a thin facade | Delegates to the workflow engine; Appendix B validation; no bypass of PDP, approvals or budgets | One endpoint per workflow (156 routes); generic RPC without DTO validation |
| ADR-209 | API ingress under DEC-421 | Vercel external rewrites to AWS origins with origin-verify; direct AWS hosts for hooks, developer API and SCIM | Per-domain API hosts with credentialed CORS; moving SPAs back to AWS |

## 11.8.8 Expert persona review

### 11.8.8.1 Principal API Architect

| Finding | Action taken |
|---|---|
| Appendix A bodies are untyped (`payload: object`), so it cannot drive client generation alone | Blueprint DTOs kept inside `Command.payload`; GAP-897 asks the customer to approve per-operation DTOs; Schemathesis tests use blueprint schemas |
| Three spellings of the run gateway (`/api/v1/workflow-runs`, `/api/v1/commercial/workflow-runs`, `/api/v2/workflow-runs`) | One operation family under `/api/v2` (DEC-647); other spellings recorded as aliases, not mounted |
| 30 historical public/callback routes missing from Appendix A | Retained (registry rule R-6); reported to the customer as an Appendix A completeness gap |
| Page size and envelope differ from Part 3.2 | V12 adopted before any external client exists (cheapest moment) |

### 11.8.8.2 Integration Architect

| Finding | Action taken |
|---|---|
| Connector catalogue names categories without contracts | CF-01…12 give every connector one contract; AD-V12-H Part A/B tables |
| CRM sync risks two systems of record | Platform remains system of record for consent, suppression, approvals and money; CRM sync is BYO and bi-directional only for allowlisted fields |
| SMS-DLT requires entity, header and template registration before any send | CF-11 gate; DLT IDs stored on the channel account; PreflightRequest channel `SMS` |
| Uncertain writes on new connectors | Inherit IP-04 reconciliation; per-connector idempotency strategy in Part B |

### 11.8.8.3 Open-source / plugin FinOps strategist

| Finding | Action taken |
|---|---|
| V12's 97 decisions are identical to the blueprint's | No re-decision; VND IDs adopted as keys (DEC-651) |
| New capabilities could quietly add SaaS (webhook services, status pages, API portals, SCIM brokers) | OSS or native choices in §11.8.5.9; paid only by exception with a budget line |
| BYO provider fees could leak into platform cost | GC-10 ledger split and test TC-V12-H-093 |
| Running cost of this part | ₹300–3,700/month, mostly the SMS pilot and the status host |

### 11.8.8.4 API security lead

| Finding | Action taken |
|---|---|
| API keys and SCIM tokens are new long-lived credentials | Hash-only, expiry, allowlists, revocation ≤ 60 s, leak scanning, audit + SIEM |
| Outbound webhooks are a new data-exfiltration path | Reference-only payloads; scope check at subscription and delivery; SSRF guard |
| A key with write scopes could trigger consequential effects | No scope exists for consequential actions; L1 cap untouched; API keys and R20 cannot approve |
| Vercel rewrites put personal data in transit through a new processor | CONFLICT-889 raised with controls; Founder decision |

### 11.8.8.5 Inconsistencies found in earlier parts (reported, not edited)

| # | Location | Inconsistency | Suggested fix (owner of that part) |
|---|---|---|---|
| 1 | Part 9.3 "API operations 579 (555 + 24)" vs Part 9.7b | API-ADV-X1-01…40 (40 IDs, three rows combining `GET / POST`) are not counted; Parts 9.8a and 9.9a list further inline routes without operation IDs | State "579 core + 40 advanced (A1) + proposal routes" and assign IDs to approved X2/X3 routes |
| 2 | Part 3.2 §3.2.1.13 vs Part 9.9a ADR-138 | Part 3.2 says outbound webhooks are not offered in W0–W6; Part 9.9a specifies them for A3 | Superseded by DEC-645 |
| 3 | Part 3.2 §3.2.1.1/§3.2.1.12 vs DEC-421 | Ingress text still describes CloudFront path behaviours for the SPAs | Update with DEC-652 once decided |
| 4 | Part 3.2 AD-19 "W1 pilot only if approved" vs Part 7.4b PG gate | V12 requires DEC-V9-04 closure and CJ-R15 before any contact-data activation | Superseded by DEC-649 |
| 5 | Part 3.2 §3.2.3.3 count line | "91 catalogue rows covering 159 concrete event types" should be recomputed after DEC-654 (+24 rows, +49 types) | Registers update (Part 9.2) |

## 11.8.9 Tags register (allocated range 886–903)

| Tag | Statement | Where |
|---|---|---|
| CONFLICT-886 | Developer platform and connector framework in V12 R1 vs approved Release 1 budget/team/dates and the unapproved A3 placement | §11.8.6 |
| CONFLICT-887 | Enterprise identity (SSO, SCIM, custom roles) in R1/R2 vs DEC-019 scope and budgets | §11.8.6 |
| CONFLICT-888 | CRM, SMS-DLT, voice and warehouse connectors vs native-only CRM and "no SMS in W0–W5" | §11.8.6 |
| CONFLICT-889 | Vercel rewrites carry personal data vs the DEC-421 data-flow statement | §11.8.5.10, §11.8.6 |
| CONFLICT-890 | "Investor search" label on VND-54/73 vs DEC-002 | §11.8.5.9 |
| CONFLICT-891 | Global bearer JWT vs DEC-019 browser cookie model | §11.8.5.3 |
| CONFLICT-892 | Pagination, version field, deprecation and outbound-webhook conventions | §11.8.5.3 |
| ASSUMPTION-893 | V12 phases R0–R5 map to Release 1 / Release 2 / W6 / Year 2+ | §11.8.5.1 |
| ASSUMPTION-894 | API key format and HMAC-SHA-256 hashing with a server pepper | §11.8.5.4 |
| ASSUMPTION-895 | Webhook retry schedule (6 attempts in ≈ 22 h) within the V12 24-hour window | §11.8.5.6 |
| ASSUMPTION-896 | RL-KEY / RL-KEY-H / RL-SCIM default limits | §11.8.5.4 |
| GAP-897 | Appendix A/A2 lack per-operation request/response DTOs (generic Command/Record payloads) | §11.8.4.2.1 |
| GAP-898 | DEC-V9-04, CJ-R15 and CJ-GL-01 legal closures are outside the blueprint baseline; the blueprint only gates on them | CF-11 |
| GAP-899 | AIX-##, CJ-R##, CJ-IN-## and ENT-IDN/ACC/DAT IDs are defined in other V12 chapters (Groups E, F, I); this part cross-references them | §11.8.5.1 |
| RECOMMENDATION-900 | Host the status page on an independent provider so it survives an AWS or Vercel outage | §11.8.5.10 |
| RECOMMENDATION-901 | CI contract gates with oasdiff and Schemathesis on every published namespace | §11.8.5.2 |
| RECOMMENDATION-902 | Start CRM sync with one provider chosen by owned-company demand, BYO credentials | §11.8.4.7 |
| RECOMMENDATION-903 | Generate TypeScript and Python SDKs at R2; Java at R3 | §11.8.5.4 |

## 11.8.10 Quality gate: Batch 11.8 (a and b)

| # | Item | Result | Notes and fixes applied |
|---|---|---|---|
| 1 | Every requirement traced to a source | Pass | FR-V12-H-001…041 cite ENT-/MT-/OPT-/API-V2/GC-/INT-/VND IDs; every new operation cites its V12 row; CSV row per aspect |
| 2 | Assumptions/gaps/conflicts tagged and logged | Pass | 18 tags, all within 886–903 (§11.8.9) |
| 3 | IDs unique and consistent with earlier parts | Pass | Build script asserts referenced operation IDs exist and aspect IDs are unique; DEC-640…659 and ADR-205…209 within allocation |
| 4 | No story lacks AC and no requirement lacks a test | Pass | 13 stories with Gherkin; 76 operation tests + 21 requirement tests (TC-V12-H-001…097) |
| 5 | Negative, edge, security and accessibility cases | Pass | Negative assertions per operation; threat table §11.8.5.12; accessibility N/A for APIs (screens A122–A131, W38–W41 are Group G) |
| 6 | No agent lacks guardrail, fallback, KPI and cost | N/A | No new AI agent; AI routes govern existing agents |
| 7 | Time-sensitive facts flagged "verify" with as-of date | Pass | Provider fees, quotas, licences, regulatory clocks and edge regions flagged (as of 27 Nov 2026) |
| 8 | No restricted data routed to free-tier models | Pass | Content screening keeps Restricted text off Tier 2; DEC-418 routing unchanged |
| 9 | Consistent with earlier parts | Pass with findings | Five inconsistencies reported (§11.8.8.5); safety invariants unchanged: no scope or route lets AI or API keys sign, pay, submit bids, set prices or send consequential actions without a human; L1 cap, PDP dispatch recheck, RLS isolation and Website/Admin separation retained |

**Status: Part 11 Batch 11.8 complete. 1176 V12 aspects reconciled: 1168 Matched, 7 Pending Founder decision (CONFLICT-886/887/888), 1 Not applicable; 76 new operations (blueprint 579 → 655), 49 new event types and a 24-type outbound webhook projection, 11 adapters, 12 connector-framework clauses, 97 VND decisions confirmed; DEC-640…659 (five pending the Founder), ADR-205…209; CR-V12-H-01 ₹5.00–15.55 L one-time (R1–R2) and ₹300–3,700/month proposed outside the approved budgets.** *(v1.2: every item counted here as "Pending Founder decision" was adopted by DEC-770…791 — Part 11.14; read as Adopted. Part 11.25.)*
