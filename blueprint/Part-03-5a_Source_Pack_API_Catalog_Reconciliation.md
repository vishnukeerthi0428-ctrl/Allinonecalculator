# AI Growth Engine: Employee Sales & Marketing Automation
## Application Blueprint: PART 3 (Batch 3.5a), Source Pack API Catalog Reconciliation: Document 07 Review, Coverage Register and Operation Mapping

| Field | Value |
|---|---|
| Document | Part 3, Batch 3.5 (file a of 2): source-pack review of document 07 "REST API & External Integration Catalog" against Parts 3.1 and 3.2 |
| Version | 1.0 · 27 Nov 2026 |
| Baseline | BRD, FRD, Parts 0, 0A (DEC-001…065), 1, 2.1–2.5, 3.1 (architecture), 3.2 (555 DERIVED operations, AD-01…20, event catalogue, CT-01…14), 3.3 (ENT-001…199), 4.2 (NFR), 6.x; source pack document 07 (835,872 bytes of extracted text, 8,432 lines) and document 38 (authoritative counts) |
| Roles applied | API Architect (lead), Integration Architect, Principal Engineer, Security Reviewer; supporting views: QA Lead, FinOps Lead, Data Architect |
| Section numbering | `3.5.x` (batch-scoped). File a holds §3.5.1–§3.5.4; file b (`Part-03-5b_Source_Pack_API_Catalog_Reconciliation.md`) holds §3.5.5–§3.5.9 |
| Machine-readable outputs | `final/coverage/D_api_mapping.csv` (one row per source operation and candidate: 321 rows) · `final/coverage/D_coverage.csv` (every atomic aspect) · scripts in `assembly/source_pack/D_*.py` |
| Tags issued (both files) | ASSUMPTION-360…366 · GAP-360…367 · CONFLICT-360…372 · RECOMMENDATION-360…371 (register in file b §3.5.8) |

**Acronyms used in this batch.** API application programming interface · AD adapter (Part 3.2 catalogue ID) · BFF Backend-for-Frontend · CI continuous integration · CT contract-test layer (Part 3.2 §3.2.5) · DTO data transfer object · ENH enhancement · NS ingress namespace · OIDC OpenID Connect · OPT optimization control (source) · PDP Policy Decision Point · RL rate-limit class · SE side-effect class · SIT system integration test · SM-OP source-pack operation (document 07 sequence number) · SRC07-DEC source-local contract decision of document 07 · WABA WhatsApp Business Account.

**Reading guide.** Document 07 is the catalogue that Part 3.2 could not see: Part 3.2 §3.2.2.1 records "the 302-operation catalogue itself was not supplied (GAP-103)" and promises "a mapping table (original ID → API-###) … and any original operation without a match becomes a candidate addition (DEC-015)". This batch delivers that promise. File a reviews the document, registers every aspect and maps all 302 retained operations, the 17 adapters inside them and the 19 candidate operations to Part 3.2. File b writes the missing content at full depth: 24 new operations, normalized field contracts for 247 operations, 38 contract decisions, adapter envelope and three new adapters, a 74-entry provider register, error codes, contract approval lifecycle, requirements, stories and 345 test cases.

**Time-sensitive facts.** Every provider quota, price, free tier, API entitlement and signature scheme quoted from document 07 is the source author's statement "checked 2026-11-24" or "not verified"; all are **to verify at time of implementation (as of 27 Nov 2026)**. No price in this batch is presented as fact.

---

## 3.5.1 Documents reviewed

### 3.5.1.1 Document 07: identity, size and structure

| Item | Value |
|---|---|
| Title | AI Growth Engine · Employee Sales & Marketing Automation · REST API & External Integration Catalog · Product and Engineering Specification / 07 |
| Size | 835,872 bytes extracted text (≈ 836 KB), 8,432 lines; 302 numbered operation sections; 4 tables in the controls section (one of 302 rows); 38 decision sections; 19 candidate sections |
| Method of review | (1) Every prose section read line by line. (2) Every operation block parsed by `assembly/source_pack/D_parse_07.py` (23 field keys per block, the "Implementation contract" sentence split into request fields, result fields, synthetic request, proposed status and SIT assertion). (3) The 302-row SIT table, the 38 DEC sections, the 19 candidate sections (JSON Schemas) and the 20 OPT controls parsed separately. (4) Part 3.2 catalogue rows (API-001…555) and adapters (AD-01…20) parsed from the blueprint Markdown. (5) Mapping by `D_map_07.py`: automatic exact match on method + path, then a hand-reviewed semantic mapping for every remaining operation (documented per row) |
| Parser cross-checks (all pass) | 302 operation headings = 302 SIT rows (SM-SIT-A001…A302, method/path identical row by row) · 285 HTTP (111 GET, 163 POST, 11 PATCH) + 17 ADAPTER · contract maturity 164 explicit DTO + 1 public allowlist = **165** (source: "165 explicit proposed operation contracts") · 82 cursor lists (source: 82) · 38 review-required (source: "Exact API definitions outstanding: 38") · 17 adapters (source: 17) · 38 DEC sections · 19 candidates · 20 OPT controls · 74 distinct integration/tool names |

| Section (source heading) | Lines | Content | Pattern |
|---|---|---|---|
| Front matter | 1–6 | Title; "Current design scope: 147 interfaces (34 Website, 113 Admin)"; candidates pending approval | Common core |
| Product purpose and operating boundary; Initial startup configurations; Technology and execution principles | 7–36 | Scope, independent deployment, two frontends, tenancy; four startup profiles; stack and autonomy principles | **Common core: see document 01/02 coverage** |
| Engineering contracts | 37–39 | REST/JSON contract rules; database contract rules | API-specific (14 aspects) |
| Commercial REST and external adapter register | 40–5983 | Operations 001…288, each with up to 23 fields (see §3.5.1.3) | Catalogue |
| Website publishing and external-portal additions | 5984–6111 | Operations 289…302 (14 website/portal operations) with entities and interfaces | Catalogue |
| Website and confidential Admin operating contract | 6112–6138 | Surfaces table, routing decision, configuration, operational separation | API-specific + common core |
| Adapter contract and API-level regression | 6139–6141 | Adapter request/response context; contract-test list | API-specific |
| Contract verification and API lifecycle | 6142–6145 | Schema/approval rules, counts, delivery evidence | API-specific |
| Implementation, verification and delivery controls | 6146–8013 | 285/17 split; contract-decision table (6 rows); **302-row operation → SIT table**; acceptance and evidence record | API-specific + catalogue |
| Field-level contract approval and negative testing | 8014–8018 | Counts of proposal maturity; common error candidate; offline verification counts | API-specific |
| Optimization engineering and acceptance | 8019–8076 | OPT-01-01, OPT-02-01…07, OPT-08-01…06, OPT-09-01…05, OPT-19-01; Optimization Intelligence reuse of Admin operations | Common core (document 36) + API-specific OPT-09 |
| Implementation acceptance and verification; … final decision controls | 8077–8329 | Eight acceptance procedures (twice); outstanding approval gates; candidate field notation; DEC-001…038 | API-specific |
| Current multi-startup, omnichannel and automation scope | 8330–8432 | SM-UX-API-01…19 with JSON Schemas; applicant draft boundary; reuse-first comparison | Catalogue (candidates) |

### 3.5.1.2 What the document is trying to tell

Document 07 is the **operation-level contract book** of the product. Its message has five layers:

1. **Inventory.** The product has exactly 302 retained operations (285 HTTP routes and 17 server-side adapters) plus 19 candidate HTTP operations for the nine new interfaces (W31–W34, A109–A113). Each has a stable number and a SIT test ID (SM-SIT-A###) so engineering can track it.
2. **Boundary per operation.** Every operation carries an *access boundary* (Public, Portal, Portal + Admin, Admin, Authentication, Internal worker, Internal adapter, Provider callback) that decides the ingress, the serializer and the audience. This classification overrides older role wording.
3. **Contract maturity is uneven and honest.** 165 operations have a proposed explicit DTO, 82 list reads have only cursor controls, 38 have descriptive payloads that still need a decision (DEC-001…038), and 17 adapters must never be exposed to browsers. Nothing is "approved"; the document repeatedly says proposals are not production contracts.
4. **Integration economics.** Every operation names the libraries, providers and Claude developer plugins it touches, with licence, free quota, paid rate, budget allocation (B01…B10), source URL and verification status. Developer plugins are explicitly "not runtime entitlements".
5. **Acceptance discipline.** Contract tests per method/path, webhook replay tests, negative fixtures, a catalogue-integrity check and an evidence record are required before a route is enabled.

### 3.5.1.3 Per-operation field semantics (columns of the source register)

| Source field | Present on | Meaning | Blueprint home before this batch |
|---|---|---|---|
| Implementation contract | 302 | Maturity class, request fields (`name:type [enum] required|optional/review`), synthetic request, result fields, proposed status, SIT assertion and expected source result | None (Part 3.2 has no field-level DTOs) → §3.5.5.3 |
| Access boundary | 302 | Audience class and the controls that apply | Part 3.2 *NS* + *Auth / roles* |
| Website interface associations / Interfaces | 23 / 14 | W-screen served | Part 3.2 *FR / screen* |
| Interface type | 288 | App REST · External adapter · Provider webhook · Existing — reuse · Internal/probe | Part 3.2 *NS* and §3.2.4 |
| Purpose | 302 | One-line business purpose | Part 3.2 *Purpose* |
| Data effect | 288 | Read · validated transactional action with audit/outbox · provider I/O + normalized persistence · verify → dedupe → persist → enqueue | Part 3.2 *SE* class |
| Request / Response contract | 302 | Descriptive request and result | Part 3.2 *Purpose* (descriptive) → §3.5.5.3 |
| Authorization | 288 | Policy wording (RBAC, object permission, provider signature) | Part 3.2 *Auth / roles* |
| Acceptance | 302 | Acceptance statement | Part 5 stories (by FR), CT-05 |
| Implementation | 288 | Reuse / proposed serializer / adapter note | Part 3.1 module map |
| Module, Screens | 288 / 285 | Owning module and Admin screen names | Part 2.1 modules M01…M66; Part 2.5 screens |
| Tables / PostgreSQL entities | 302 | Physical table names (`growth_*`, `sales_*`, `existing user table`) | Part 3.3 ENT-001…199 (logical/physical) |
| Integration, Licence, Free quota, Paid rate, Allocation, Source, Verification | 288 / 246 | Provider and tool economics per operation | Part 3.2 §3.2.4.2 (per adapter) → §3.5.5.6.4 |

### 3.5.1.4 Atomic aspect count

| Aspect family | Count | Basis |
|---|---|---|
| Common core (listed once) | 6 | Purpose/boundary, startup configurations, technology principles (not re-assessed per document) |
| Prose, contract and control aspects | 80 | Engineering contracts, operating contract, adapter contract, lifecycle, implementation controls, field-level approval, acceptance procedures, current scope, security readings |
| Operation endpoints (302 retained, incl. 17 adapters) | 302 | One aspect per operation (method/path or adapter, boundary, purpose) |
| Field contracts (HTTP operations) | 285 | One aspect per HTTP operation's request/response contract |
| Operation SIT tests | 302 | One aspect per SM-SIT-A### row |
| Adapter command/result context | 17 | One aspect per adapter's context and result envelope |
| Candidate operations (endpoint + schema) | 19 | SM-UX-API-01…19 |
| Contract decisions SRC07-DEC | 38 | DEC-001…038 sections |
| Providers and tools | 74 | Distinct names in Integration columns |
| Optimization controls | 20 | OPT-01-01 … OPT-19-01 |
| **Total atomic aspects** | **1143** | |

---

## 3.5.2 Coverage register summary

| Aspect family | Aspects | Covered | Partially covered | Not covered | Conflict | Not applicable |
|---|---|---|---|---|---|---|
| Common core (listed once) | 6 | 0 | 0 | 0 | 0 | 6 |
| Prose, contract and control aspects | 80 | 46 | 16 | 10 | 6 | 2 |
| Operation endpoints (302 retained, incl. 17 adapters) | 302 | 281 | 15 | 6 | 0 | 0 |
| Field contracts (HTTP operations) | 285 | 0 | 0 | 285 | 0 | 0 |
| Operation SIT tests | 302 | 0 | 302 | 0 | 0 | 0 |
| Adapter command/result context | 17 | 0 | 17 | 0 | 0 | 0 |
| Candidate operations (endpoint + schema) | 19 | 16 | 3 | 0 | 0 | 0 |
| Contract decisions SRC07-DEC | 38 | 0 | 0 | 38 | 0 | 0 |
| Providers and tools | 74 | 36 | 2 | 1 | 5 | 30 |
| Optimization controls | 20 | 15 | 5 | 0 | 0 | 0 |
| **Document 07 total** | **1143** | **394** | **360** | **340** | **11** | **38** |

**Interpretation.** At the *endpoint* level Part 3.2 already covers 297 of 321 source operations (92.5%), because its 555-operation catalogue was derived from all 147 screens and is a superset. The real deficit is one level down: **no source operation had a field-level request/response contract, per-operation status/error set or per-operation SIT test in the blueprint**. That deficit, plus 24 missing operations, 3 missing adapter ports, the adapter envelope, the contract-approval lifecycle and 13 conflicts, is what file b closes.

---

## 3.5.3 Detailed coverage register

### 3.5.3.1 Non-catalogue aspects (prose, controls, decisions, providers)

Every Partially covered, Not covered and Conflict item is listed individually. Common-core aspects are listed once and marked "Common core: see document 01/02 coverage".

| Aspect | Source section | Aspect | Status | Blueprint location | Action | New IDs / tags |
|---|---|---|---|---|---|---|
| 07-CC-01 | Product purpose and operating boundary | Employee-operated commercial growth scope; no fundraising/investor functions | Not applicable | Part 0/1 (BRD §1, DEC-002) | Common core: see document 01/02 coverage |  |
| 07-CC-02 | Product purpose and operating boundary | Independent deployment: own origin, API audience, DB, storage, vectors, queues, credentials, budget, billing, audit, backup | Not applicable | NFR-031; Part 3.1 | Common core: see document 01/02 coverage |  |
| 07-CC-03 | Product purpose and operating boundary | Two React frontends with separate origins, sessions, OAuth clients, allowlists, builds | Not applicable | NFR-001; DEC-019 | Common core: see document 01/02 coverage |  |
| 07-CC-04 | Product purpose and operating boundary | 25+ owned startups, external tenants, tenant = security/billing boundary, owner group view read-only | Not applicable | DEC-055, DEC-065 | Common core: see document 01/02 coverage |  |
| 07-CC-05 | Initial startup configurations | Four startup profiles (AppNAI, MedMaarg, EduVerse, OrganicSpec) and template-based onboarding of new startups | Not applicable | Part 1; CFG-03/04 | Common core: see document 01/02 coverage |  |
| 07-CC-06 | Technology and execution principles | Stack, open-source first, autonomy policies, simulation zero effect, execution-time recheck, one consolidated plan | Not applicable | Part 3.1; DEC-064; NFR-038 | Common core: see document 01/02 coverage |  |
| 07-EC-01 | Engineering contracts | REST JSON over HTTPS with separate product audience | Covered | Part 3.2 §3.2.1.1–2; NFR-015 | None |  |
| 07-EC-02 | Engineering contracts | Verify the actual reused authentication route before coding | Covered | DEC-019 spike; TS-01-01 | None |  |
| 07-EC-03 | Engineering contracts | Typed input/output per operation | Partially covered | Part 3.2 §3.2.1.2 conventions only | Per-operation field contracts written | §3.5.5.3; GAP-360 |
| 07-EC-04 | Engineering contracts | Allowlisted filters and cursor pagination | Covered | Part 3.2 §3.2.1.6 | Source page_size reconciled to limit | CONFLICT-362 |
| 07-EC-05 | Engineering contracts | Request ID, version/revision, idempotency key and body hash | Covered | Part 3.2 §3.2.1.4–5, §3.2.1.8 | Body-field variants mapped to headers | CONFLICT-361 |
| 07-EC-06 | Engineering contracts | Status set 200/201/202/400/401/403-or-uniform-404/409/429/503 | Covered | Part 3.2 §3.2.1.9–10 | 24 per-operation status disagreements resolved | §3.5.4.6; CONFLICT-370 |
| 07-EC-07 | Engineering contracts | No live external effect before approvals and cost reservation | Covered | Part 3.2 IP-06, PDP P+D; NFR-014 | None |  |
| 07-EC-08 | Engineering contracts | transaction.atomic + row lock; state and outbox written together | Covered | NFR-006; Part 3.1 outbox | None |  |
| 07-EC-09 | Engineering contracts | Verified callbacks persist a minimal event and acknowledge quickly; dedupe by provider account + event ID | Covered | Part 3.2 §3.2.1.13; NFR-051 | None |  |
| 07-EC-10 | Engineering contracts | Reconcile uncertain results before retry; exponential back-off with jitter; capped retries; exception queue | Covered | Part 3.2 IP-04, §3.2.7; NFR-016, NFR-026 | None |  |
| 07-EC-11 | Engineering contracts | Independent DB/role per product; FK creation order; deferred cyclic constraints; indexes/views last | Covered | Part 3.3 (migration order) | Data detail owned by document 08 group |  |
| 07-EC-12 | Engineering contracts | UUID PK, UTC, tenant/startup composite FKs, RLS, revision; immutable approval/financial/audit rows; decimal + ISO currency | Covered | NFR-017, NFR-018; Part 3.3 | None |  |
| 07-EC-13 | Engineering contracts | Provider IDs unique within connection; separate object-storage/vector ACLs; no DB access for browser, Copilot or provider | Covered | Part 3.2 §3.2.1.13 step 5; Part 3.3; BRL-AI-05 | None |  |
| 07-EC-14 | Engineering contracts | Validate physical naming against existing schema; no executable migration asserted | Covered | Part 3.3 logical/physical names | Physical-name deltas (growth_*, sales_*) recorded | ASSUMPTION-366 |
| 07-RG-01 | Commercial REST and external adapter register | 288 proposed baseline items + 14 website additions = 302; 285 HTTP + 17 adapters | Conflict | Part 3.2 §3.2.2.1 (GAP-103: catalogue not supplied) | Full mapping produced; counts reconciled | §3.5.4; CONFLICT-365 |
| 07-RG-02 | Commercial REST and external adapter register | Preserve source identities for engineering tracking | Not covered | Part 3.2 has no source IDs | SM-OP-### and SM-SIT-A### carried as x-source-op / x-sit-id | ASSUMPTION-360; RECOMMENDATION-360 |
| 07-RG-03 | Commercial REST and external adapter register | Per-operation fields: Interface type, Purpose, Data effect, Request, Response, Authorization, Acceptance, Implementation, Module, Screens, Tables | Partially covered | Part 3.2 catalogue columns (purpose, roles, idempotency, SE, PDP, RL) | Missing columns supplied in mapping CSV and field register | §3.5.5.3; D_api_mapping.csv |
| 07-RG-04 | Commercial REST and external adapter register | Per-operation Integration, Licence, Free quota, Paid rate, Allocation, Source, Verification | Partially covered | Part 3.2 §3.2.4.2 per adapter only | 74-entry provider register classified | §3.5.5.6.4; RECOMMENDATION-365 |
| 07-RG-05 | Commercial REST and external adapter register | Existing-reuse auth items are logical aliases, not a mandate to rebuild | Covered | DEC-019; API-001…012 | SRC07-DEC-001…005 resolved to BFF | ASSUMPTION-361 |
| 07-WA-01 | Website and confidential Admin operating contract | 34 Website + 113 Admin = 147 interfaces; 138 retained + 9 added | Covered | Part 2.5 §2.43 | None |  |
| 07-WA-02 | Website and confidential Admin operating contract | Four surfaces: Website public, Website portal, Admin, Internal/callback with exposure controls | Covered | Part 3.2 §3.2.1.1 namespaces | None |  |
| 07-WA-03 | Website and confidential Admin operating contract | Retain canonical legacy method/path contracts | Conflict | Part 3.2 retains only 104 FRD-named paths | Resolution proposed | CONFLICT-360 |
| 07-WA-04 | Website and confidential Admin operating contract | Explicit access classification and external serializer rules override older role wording | Partially covered | Part 3.2 NS column | Classification precedence rule stated; 10 boundary differences resolved | §3.5.4.5; CONFLICT-366 |
| 07-WA-05 | Website and confidential Admin operating contract | New website endpoints under /api/v1/commercial/public\|portal\|admin/ | Covered | Part 3.2 §3.2.1.1 | None |  |
| 07-WA-06 | Website and confidential Admin operating contract | Legacy token routes under /public/ are restricted portal endpoints | Conflict | API-083 classified public | Reclassify to portal | CONFLICT-367 |
| 07-WA-07 | Website and confidential Admin operating contract | Route not admitted to website denied by default; CORS is not authorization | Covered | Part 3.2 §3.2.1.1 rule 4; CT-07 | Allowlist generated from catalogue | §3.5.5.7; RECOMMENDATION-366 |
| 07-WA-08 | Website and confidential Admin operating contract | Verified domain maps to one tenant/startup; unknown host 404 | Covered | NFR-020; UNKNOWN_HOST | Domain disable operation added | API-ENH-D-012 |
| 07-WA-09 | Website and confidential Admin operating contract | Immutable publication snapshot (content, locale, slug, revision); expiring noindex previews; atomic pointer swap; tenant-keyed cache invalidation | Covered | API-490…495; ENT-113/114; BRL-PUB-02/03 | None |  |
| 07-WA-10 | Website and confidential Admin operating contract | Public assets separately approved and scanned; portal content never in public snapshot or CDN | Covered | BRL-PUB-04; NFR-020, NFR-021 | None |  |
| 07-WA-11 | Website and confidential Admin operating contract | Public intake creates scoped durable event + outbox, not a business approval; workers recheck | Covered | API-212; CA-INTAKE; PDP D | None |  |
| 07-AD-01 | Adapter contract and API-level regression | External provider calls are server-side adapters, never public REST routes | Covered | Part 3.2 §3.2.4; CT-07 | None |  |
| 07-AD-02 | Adapter contract and API-level regression | Adapter request context: product, tenant, startup, approved action, idempotency/correlation key, deadline, budget reservation | Partially covered | Part 3.1 ADR AdapterResult; IP-01 | AdapterCommand envelope defined | §3.5.5.6.1; RECOMMENDATION-363 |
| 07-AD-03 | Adapter contract and API-level regression | Adapter response: normalized data/evidence, provider status, metered units, safe error code, external reference | Partially covered | AdapterResult(status, provider_ref, normalized, cost, failure_class) | metered_units, safe_error_code, evidence_refs added | §3.5.5.6.1 |
| 07-AD-04 | Adapter contract and API-level regression | Use existing integration registry, job and audit services | Covered | IP-01 registry; JobRun; audit | None |  |
| 07-AD-05 | Adapter contract and API-level regression | Contract tests per method/path/adapter: success, invalid input, foreign tenant/audience, stale/idempotency, pagination, callbacks/replay, no paid call without approval | Partially covered | CT-01…CT-14 (generic) | Per-operation tests TC-ENH-D-001…302 | §3.5.5.12; GAP-362 |
| 07-AD-06 | Adapter contract and API-level regression | Mock providers in unit/SIT, authorized sandboxes for compatibility, never expose credentials or internal exceptions | Covered | CT-08/09; IP-08; NFR-004 | None |  |
| 07-LC-01 | Contract verification and API lifecycle | Every method/path needs exact approved request/response schema, access guard, bounded filter, error contract, idempotency, positive/negative test | Partially covered | Part 3.2 standards | Field register + contract approval workflow + tests | §3.5.5.3, §3.5.5.9, §3.5.5.12; FR-ENH-D-001 |
| 07-LC-02 | Contract verification and API lifecycle | Freeze contracts by immutable build; deprecate only after compatibility review | Covered | Part 3.2 §3.2.1.3; CT-01 | None |  |
| 07-LC-03 | Contract verification and API lifecycle | Counts: 147 UI, 302 ops, 149 entities, 624 tests; 19 candidate ops, 6 candidate entities, 175 extra tests | Conflict | Part 3.2 555 ops; Part 3.3 199 ENT | Counts reconciled | §3.5.4.1; CONFLICT-365 |
| 07-LC-04 | Contract verification and API lifecycle | Delivery evidence against build, environment, scope, reviewer, approval; open critical defects block activation | Partially covered | Part 8.2 go-live gates; A090 | Contract evidence record defined | §3.5.5.9.2; FR-ENH-D-002 |
| 07-IC-01 | Implementation, verification and delivery controls | Do not expose adapters as browser APIs | Covered | Part 3.2 §3.2.4; CT-07 | Catalogue integrity check added | FR-ENH-D-003 |
| 07-IC-02 | Implementation, verification and delivery controls | Catalogue-complete OpenAPI draft supplied as engineering aid | Not covered | Not in the 38-document package (text only) | Recorded as gap; OpenAPI generated from §3.5.5.3 | GAP-366 |
| 07-IC-03 | Implementation, verification and delivery controls | Unknown payload types are not silently invented | Covered | Blueprint tagging rule | Defaults tagged | ASSUMPTION-363 |
| 07-IC-04 | Implementation, verification and delivery controls | Contract decision: authorization resolved server-side; public output allowlisted; provider-specific callback signatures | Covered | Part 3.2 §3.2.1.12–13 | None |  |
| 07-IC-05 | Implementation, verification and delivery controls | Contract decision: exact required fields, enums, numeric precision, range, unknown-field policy, path/query/body separation | Partially covered | additionalProperties false (§3.2.1.2) | Field register with types, enums, optionality | §3.5.5.3 |
| 07-IC-06 | Implementation, verification and delivery controls | Contract decision: confirm actual status codes per operation; safe errors with correlation IDs | Partially covered | §3.2.1.9–10 rules | Per-op status and error profile | §3.5.4.6, §3.5.5.3 |
| 07-IC-07 | Implementation, verification and delivery controls | Contract decision: idempotency scoped to tenant/startup, operation and key; changed payload conflicts; audit effect and replay | Partially covered | §3.2.1.5 (no audit of replays) | Replay audit event added | FR-ENH-D-004 |
| 07-IC-08 | Implementation, verification and delivery controls | Contract decision: stable sort + ID tie-breaker, bounded page, opaque cursor scoped to query and authorization | Covered | §3.2.1.6 | None |  |
| 07-IC-09 | Implementation, verification and delivery controls | Contract decision: run exact examples in SIT; typed contract must pass review before the route is enabled | Not covered | No route-activation gate | Contract approval state machine + route flag | §3.5.5.9; FR-ENH-D-001 |
| 07-IC-10 | Implementation, verification and delivery controls | Acceptance and evidence record: responsible/reviewer, artifact/test evidence, decision, remediation, business acceptance | Partially covered | Part 8.2 release evidence | Contract evidence record schema | §3.5.5.9.2 |
| 07-FL-01 | Field-level contract approval and negative testing | 165 explicit proposals, 0 source-typed, 82 cursor reads, 38 outstanding definitions, 17 adapters | Covered | §3.5.4.2 counts | Verified by parser (164 + 1, 82, 38, 17) |  |
| 07-FL-02 | Field-level contract approval and negative testing | Common error candidate: code, safe message, request_id; 400/401/403-404/409/429 | Covered | §3.2.1.9 problem+json (superset) | Mapping stated | §3.5.5.1 |
| 07-FL-03 | Field-level contract approval and negative testing | Provider callbacks and reused auth keep provider/identity-specific responses | Covered | §3.2.6.1; DEC-019 | None |  |
| 07-FL-04 | Field-level contract approval and negative testing | Offline verification: 164 request, 164 invalid, 165 response examples (schema only, not endpoint tests) | Not applicable | Informational; examples not supplied | Examples regenerated from §3.5.5.3 as CT-04 fixtures | GAP-366 |
| 07-FL-05 | Field-level contract approval and negative testing | Final field limits and projections accepted by backend, security and QA leads | Not covered | No named contract approvers | Three-lead review step in contract workflow | §3.5.5.9; FR-ENH-D-001 |
| 07-OP-01 | Optimization engineering and acceptance | Profile operation-level latency, payload bytes and query count; no silent endpoint renames | Partially covered | NFR-039/040 (aggregate) | Per-operation budget and N+1 gate | §3.5.5.10; FR-ENH-D-005 |
| 07-OP-02 | Optimization engineering and acceptance | Optimization Intelligence reuses existing Admin operations (7 groups) with persistence sources | Covered | API-115/124/116, 136/137/144, 119/128–130, 147–151, 537/265/266, 388, 538–540 | Physical table names noted | §3.5.5.10 |
| 07-OP-03 | Optimization engineering and acceptance | Acceptance protocol: baseline, candidate, dataset, digest, cost, outcome, reviewer; missing evidence = Pending | Covered | Common core (document 36 group) | Common core: see document 01/02 coverage |  |
| 07-AP-01 | Implementation acceptance and verification | Async acknowledgement: p95 ACK ≤ 2 s separate from completion | Covered | NFR-040 (≤ 800 ms, stricter) | None |  |
| 07-AP-02 | Implementation acceptance and verification | Catalogue integrity: 138 baseline UI IDs, 302 ops, 149 entities unique and preserved; 147 current reconcile | Not covered | No catalogue integrity gate | CI gate defined | FR-ENH-D-003; TC-ENH-D-N18 |
| 07-AP-03 | Implementation acceptance and verification | Typed request/response completeness: every mandatory endpoint has approved schema | Partially covered | CT-03 schemas | Field register + approval gate | §3.5.5.3 |
| 07-AP-04 | Implementation acceptance and verification | HTTP vs adapter classification: all ops represented exactly once in OpenAPI; path params resolved | Not covered | No such check | Integrity gate | FR-ENH-D-003 |
| 07-AP-05 | Implementation acceptance and verification | Authorization and error contract: wrong role, scope, malformed, conflict, rate limit; no confidential fields in errors/logs | Covered | CT-05, CT-06; NFR-078 | Negative families N01…N08 | §3.5.5.12.1 |
| 07-AP-06 | Implementation acceptance and verification | Webhook reliability: valid/invalid signature, stale timestamp, duplicate, quota | Covered | CT-10; §3.2.6 | Per-webhook table | §3.5.5.8 |
| 07-AP-07 | Implementation acceptance and verification | Unresolved contract decision management: every blocker in a decision queue | Partially covered | Part 9.1 decisions (not API-level) | SRC07-DEC queue | §3.5.5.4, §3.5.5.9 |
| 07-AP-08 | Implementation acceptance and verification | Operation-specific negative fixtures for read, mutation, callback and adapter cases | Not covered | Generic CT only | N01…N18 families mapped to every operation | §3.5.5.12 |
| 07-AP-09 | Implementation acceptance and verification | Outstanding approval gates: 38 API definitions, 0 partial, 4 DB field confirmations, 138 UI semantic mappings | Not covered | Not in blueprint | Gate register; 4 DB confirmations unidentified | §3.5.5.9.3; GAP-365 |
| 07-AP-10 | Implementation acceptance and final decision controls | Candidate field notation (u, s, i, b, m, c, cc, t, h, k, url, p, pct, ids, ss, items, slots, lines, fields, contact, map, ?, -) | Not covered | — | Notation → OpenAPI mapping | §3.5.5.1; ASSUMPTION-362 |
| 07-AP-11 | Implementation acceptance and final decision controls | Source-local DEC-001…038 contract decisions | Conflict | Blueprint DEC-001…065 namespace | Renamed SRC07-DEC-### | CONFLICT-364 |
| 07-CS-01 | Current multi-startup scope: API design | Product namespace; distinct applicant/client audience; server-side scope; revision, scope and idempotency on mutations | Covered | §3.2.1.1; API-503…518 | None |  |
| 07-CS-02 | Applicant draft boundary | Isolated expiring opaque draft before provisioning; no mutation of active startup; provision after verified authority; transactional idempotent hand-off | Covered | API-503…511; FRD §16.3 approval type client_application | Draft read added | API-ENH-D-019 |
| 07-CS-03 | Reuse-first comparison | Each candidate operation compared to an existing operation before adding | Covered | Part 3.2 derived operations | 19 reuse decisions recorded | §3.5.5.5 |
| 07-CS-04 | Current multi-startup scope | Release condition: approved screen/contract/entity decisions, product tests, QC, acceptance evidence | Covered | Part 8.2 gates | Contract gate added | FR-ENH-D-001 |
| 07-SE-01 | Per-operation access boundary (portal) | Portal: external audience + identity-bound grant + object/action authorization + allowlisted serializer; URL token alone insufficient | Covered | ABAC-09; ENT-009; CA-PORTAL | Grant revoke/rotate/list added | API-ENH-D-017, -022, -023 |
| 07-SE-02 | Per-operation access boundary (internal adapter) | Service identity only; scoped secret reference; policy, budget and audit checks | Covered | ABAC-12; AD-12 | None |  |
| 07-SE-03 | Operation 280 (bids control) | Bid 'submit' action | Covered | DEC-053: human submits on portal; API-367 records evidence | 'submit' bound to evidence recording only | §3.5.6 CONFLICT-370 note |
| 07-SE-04 | Operations 076/080 (enrichment) | Apollo/Hunter optional licensed pilot with credit caps | Covered | AD-19 OFF by default; B08/B18 | Verification port split | AD-D02 |
| 07-SE-05 | Provider register (Leadfeeder, PostHog) | Reverse-IP visitor identification and third-party analytics on public pages | Not applicable | First-party beacon API-291; DPDP lawful basis | Excluded with reason | RECOMMENDATION-369 |
| 07-SE-06 | Provider register (OpenAI) | 'claude/openai api' integration on AI ops | Conflict | DEC-007 tiers: Anthropic Tier 1; Tier 2 free fallbacks only | OpenAI not approved as runtime provider | CONFLICT-372 |
| 07-SE-07 | Provider register (PubMed) | Public literature lookup for MedMaarg claim substantiation | Not covered | Not in Part 3.2 | Optional evidence source behind SearchPort, off by default | GAP-367; RECOMMENDATION-368 |

### 3.5.3.2 Catalogue aspects (grouped; every non-Covered row is listed in §3.5.4.3 and the CSV)

| Aspect family | Count | Covered | Partially covered | Not covered | Conflict | Where listed |
|---|---|---|---|---|---|---|
| Operation endpoints (302 retained, incl. 17 adapters) | 302 | 281 | 15 | 6 | 0 | §3.5.4.3 |
| Field contracts (HTTP operations) | 285 | 0 | 0 | 285 | 0 | File b §3.5.5.3–4 |
| Operation SIT tests | 302 | 0 | 302 | 0 | 0 | File b §3.5.5.12.2 |
| Adapter command/result context | 17 | 0 | 17 | 0 | 0 | File b §3.5.5.6 |
| Candidate operations (endpoint + schema) | 19 | 16 | 3 | 0 | 0 | §3.5.4.4; file b §3.5.5.5 |
| Contract decisions SRC07-DEC | 38 | 0 | 0 | 38 | 0 | File b §3.5.5.4 |
| Providers and tools | 74 | 36 | 2 | 1 | 5 | File b §3.5.5.6.4 |
| Optimization controls | 20 | 15 | 5 | 0 | 0 | File b §3.5.5.10 |

---

## 3.5.4 Catalogue reconciliation

### 3.5.4.1 Count reconciliation (source counts vs blueprint counts)

| Quantity | Document 07 | Document 38 | Blueprint before this batch | Reconciled view (this batch) |
|---|---|---|---|---|
| Retained operations | 302 = 288 register + 14 website additions | 321 total = 304 HTTP incl. candidates + 17 adapters | "302 retained + 19 candidate" quoted from BRD §9; catalogue not supplied (GAP-103) | 302 parsed; 285 HTTP + 17 adapters; all mapped (§3.5.4.3) |
| HTTP operations | 285 | 304 incl. 19 candidates | 555 (104 FRD-named ★ + 451 DERIVED) | 285 + 19 = 304 map onto **343 distinct** Part 3.2 operations; 212 Part 3.2 operations are blueprint-only (§3.5.4.4) |
| Adapters | 17 non-HTTP | 17 | 20 (AD-01…20) | 17 map to 19 of the 20 AD entries (AD-12 Secrets Manager has no source adapter row; it is used by every adapter); 3 new ports AD-D01…D03 |
| Candidate operations | 19 (SM-UX-API-01…19) | 19 | Represented as DERIVED ops (API-459…518 range) | 19 mapped (16 Covered, 3 Partial) |
| FRD-named operations | — | — | 104 ★ (DEC-015 says 105: CONFLICT-103) | All 104 ★ are referenced by at least one source operation; 106 exact method+path matches (104 ★ + `GET /api/v1/webhooks/whatsapp` + `POST /api/v1/admin/products/{id}/launch` same path) |
| Logical entities | 149 baseline + 6 candidates | 155 | ENT-001…199 | Out of scope here (document 08 group); physical names in this document recorded per operation in `D_api_mapping.csv` [ASSUMPTION-366] |
| Product tests | 624 baseline + 175 expansion; 302 operation SIT rows | 799 (Unit 75, SIT 422, UAT 302) | Part 6 TCs per story; **0 TCs reference an API-### ID** | 302 + 19 + 24 operation tests TC-ENH-D-… (file b §3.5.5.12) |
| Contract maturity | 165 explicit, 82 cursor, 38 outstanding, 17 adapters | — | No per-operation DTO | §3.5.4.2 |

**CONFLICT-365 (counts).** Document 07 states "288 proposed items" at the top of the register, "302 proposed operations" at its end, and "Catalog integrity: All 138 baseline UI IDs, 302 baseline operations and 149 baseline entities". These are consistent once the 14 website additions (289–302) are added to the 288, and once "138 baseline UI IDs" is read as the retained subset of the current 147. Document 38's "304 HTTP operations including candidates" = 285 + 19. Part 0A DEC-015's "105 named operations" remains CONFLICT-103 (already reported). **Proposed resolution:** adopt "302 retained (285 HTTP + 17 adapters) + 19 candidates = 321" as the source inventory, "555 + 24 enhancement operations" as the blueprint inventory, and the mapping CSV as the authoritative bridge; Part 9 registers should quote both figures with this sentence.

### 3.5.4.2 Mapping summary by relation, boundary and contract maturity

| Relation | Meaning | HTTP (285) | Adapters (17) | Retained total (302) | Candidates (19) | All (321) |
|---|---|---|---|---|---|---|
| Exact | Same method and path; legacy contract retained in Part 3.2 (104 FRD-named ★ plus 2 same-path) | 106 | 0 | 106 | 0 | 106 |
| Alias | Same semantics; Part 3.2 uses the derived `~/` path (or AD-## for adapters) | 120 | 10 | 130 | 9 | 139 |
| Split | One source operation (often an `action` enum) maps to several Part 3.2 action sub-resources | 33 | 4 | 37 | 7 | 44 |
| Approval | Source per-object approve/review route consolidated into the Approval resource (API-541 submit, API-539 decide) | 8 | 0 | 8 | 0 | 8 |
| Partial | Part of the semantics exists; the missing part is added in §3.5.5.2 / §3.5.5.6 | 12 | 3 | 15 | 3 | 18 |
| New | No Part 3.2 equivalent; new operation added in §3.5.5.2 | 6 | 0 | 6 | 0 | 6 |
| **Total** | | **285** | **17** | **302** | **19** | **321** |

| Source access boundary | Operations | Covered | Partially covered | Not covered | Part 3.2 namespace(s) used |
|---|---|---|---|---|---|
| Admin | 242 | 225 | 11 | 6 | admin (233), admin+internal (1), admin+portal (1), portal (1) |
| Internal adapter | 17 | 14 | 3 | 0 | AD-## adapters |
| Portal | 14 | 13 | 1 | 0 | portal (12), public (1), public+portal (1) |
| Public | 10 | 10 | 0 | 0 | public (9), portal (1) |
| Provider callback | 8 | 8 | 0 | 0 | hooks (8) |
| Portal + Admin (separate policy/DTO) | 5 | 5 | 0 | 0 | admin (3), admin+internal (1), public+portal (1) |
| Internal worker | 3 | 3 | 0 | 0 | internal (3) |
| Authentication (separate audience) | 3 | 3 | 0 | 0 | bff (1), admin+portal (1), bff-admin (1) |

| Source contract maturity | Count | Part 3.2 before this batch | Part 3.5 action |
|---|---|---|---|
| Proposed explicit DTO (request + result fields, status, SIT assertion) | 164 | Purpose, roles, idempotency, side-effect class, PDP and rate-limit class only; no field-level DTO | Field contract normalized to blueprint conventions (§3.5.5.3) |
| Proposed public response allowlist | 1 | Purpose, roles, idempotency, side-effect class, PDP and rate-limit class only; no field-level DTO | Public allowlist adopted (§3.5.5.3) |
| Proposed cursor/page-size list (result DTO blocked) | 82 | Purpose, roles, idempotency, side-effect class, PDP and rate-limit class only; no field-level DTO | Query/response envelope defined (§3.5.5.3) |
| Review required (descriptive payload; SRC07-DEC-001…038) | 38 | Purpose, roles, idempotency, side-effect class, PDP and rate-limit class only; no field-level DTO | Proposed DTO per SRC07-DEC (§3.5.5.4) |
| Adapter contract review (no browser endpoint) | 17 | Purpose, roles, idempotency, side-effect class, PDP and rate-limit class only; no field-level DTO | Adapter command/result envelope (§3.5.5.6) |
| **Total** | **302** | | |

### 3.5.4.3 Full operation mapping: source operation → blueprint operation (302 retained operations, including 17 adapters)

`~/` = `/api/v1/commercial/`. "Approval" = API-541 (submit object revision for approval) + API-539 (decide). An enhancement ID means the missing part is specified in file b §3.5.5.2 (operations) or §3.5.5.6.3 (adapters). The same table with 25 columns (purpose, module, tables, integration, allocation, request/response fields, SIT assertion) is `final/coverage/D_api_mapping.csv`.

| Source op | SIT | Method | Source path / adapter | Source boundary | Blueprint operation(s) | Relation | Status | Enhancement |
|---|---|---|---|---|---|---|---|---|
| SM-OP-001 | SM-SIT-A001 | POST | `/auth/login` | Authentication (separate audience) | API-001 | Exact | Covered | — |
| SM-OP-002 | SM-SIT-A002 | GET | `/me` | Authentication (separate audience) | API-002 | Exact | Covered | — |
| SM-OP-003 | SM-SIT-A003 | GET | `/admin/users` | Admin | API-019 | Alias | Covered | — |
| SM-OP-004 | SM-SIT-A004 | POST | `/admin/users/{id}/roles` | Admin | API-021, API-020 | Alias | Covered | — |
| SM-OP-005 | SM-SIT-A005 | POST | `/auth/logout` | Authentication (separate audience) | API-007, API-012 | Split | Covered | — |
| SM-OP-006 | SM-SIT-A006 | GET | `/api/v1/products` | Admin | API-048 | Exact | Covered | — |
| SM-OP-007 | SM-SIT-A007 | GET | `/api/v1/products/{id}` | Admin | API-054 | Alias | Covered | — |
| SM-OP-008 | SM-SIT-A008 | POST | `/api/v1/admin/products` | Admin | API-053 | Alias | Covered | — |
| SM-OP-009 | SM-SIT-A009 | PATCH | `/api/v1/admin/products/{id}` | Admin | API-055, API-056 | Split | Covered | — |
| SM-OP-010 | SM-SIT-A010 | POST | `/api/v1/admin/claims/approve` | Admin | API-049 | Exact | Covered | — |
| SM-OP-011 | SM-SIT-A011 | POST | `/api/v1/admin/products/{id}/prices` | Admin | API-057 | Alias | Covered | — |
| SM-OP-012 | SM-SIT-A012 | POST | `/api/v1/knowledge/uploads` | Admin | API-051 | Exact | Covered | — |
| SM-OP-013 | SM-SIT-A013 | GET | `/api/v1/knowledge/documents` | Admin | API-061 | Alias | Covered | — |
| SM-OP-014 | SM-SIT-A014 | POST | `/api/v1/knowledge/documents/{id}/review` | Admin | API-541, API-539 | Approval | Covered | — |
| SM-OP-015 | SM-SIT-A015 | GET | `/api/v1/knowledge/search` | Admin | API-052 | Exact | Covered | — |
| SM-OP-016 | SM-SIT-A016 | ADAPTER | `Object storage / document extraction` | Internal adapter | AD-20 | Partial | Partially covered | AD-D01 |
| SM-OP-017 | SM-SIT-A017 | GET | `/api/v1/public/preferences/{token}` | Portal | API-083 | Alias | Covered | — |
| SM-OP-018 | SM-SIT-A018 | POST | `/api/v1/consents` | Portal + Admin (separate policy/DTO) | API-066 | Exact | Covered | — |
| SM-OP-019 | SM-SIT-A019 | POST | `/api/v1/opt-out` | Public | API-067 | Exact | Covered | — |
| SM-OP-020 | SM-SIT-A020 | GET | `/api/v1/admin/policies` | Admin | API-071 | Alias | Covered | — |
| SM-OP-021 | SM-SIT-A021 | POST | `/api/v1/admin/policies` | Admin | API-072, API-073 | Split | Covered | — |
| SM-OP-022 | SM-SIT-A022 | GET | `/api/v1/admin/suppressions` | Admin | API-074, API-076 | Split | Covered | — |
| SM-OP-023 | SM-SIT-A023 | GET | `/api/v1/integrations` | Admin | API-095 | Exact | Covered | — |
| SM-OP-024 | SM-SIT-A024 | POST | `/api/v1/admin/integrations` | Admin | API-097 | Alias | Covered | — |
| SM-OP-025 | SM-SIT-A025 | POST | `/api/v1/admin/integrations/test` | Admin | API-096 | Exact | Covered | — |
| SM-OP-026 | SM-SIT-A026 | POST | `/api/v1/admin/integrations/{id}/disable` | Admin | API-099 | Alias | Covered | — |
| SM-OP-027 | SM-SIT-A027 | GET | `/api/v1/events` | Admin | API-115 | Exact | Covered | — |
| SM-OP-028 | SM-SIT-A028 | GET | `/api/v1/admin/jobs` | Admin | API-124 | Alias | Covered | — |
| SM-OP-029 | SM-SIT-A029 | POST | `/api/v1/admin/jobs/{id}/retry` | Admin | API-116 | Exact | Covered | — |
| SM-OP-030 | SM-SIT-A030 | GET | `/api/v1/sources` | Admin | API-158 | Exact | Covered | — |
| SM-OP-031 | SM-SIT-A031 | POST | `/api/v1/admin/sources` | Admin | API-159 | Exact | Covered | — |
| SM-OP-032 | SM-SIT-A032 | PATCH | `/api/v1/admin/sources/{id}` | Admin | API-179 | Partial | Partially covered | API-ENH-D-001 |
| SM-OP-033 | SM-SIT-A033 | POST | `/api/v1/internal/ai/run` | Internal worker | API-134 | Exact | Covered | — |
| SM-OP-034 | SM-SIT-A034 | GET | `/api/v1/admin/ai/runs` | Admin | API-135 | Exact | Covered | — |
| SM-OP-035 | SM-SIT-A035 | POST | `/api/v1/admin/ai/prompts` | Admin | API-142 | Alias | Covered | — |
| SM-OP-036 | SM-SIT-A036 | GET | `/api/v1/admin/ai/eval-cases` | Admin |  | New | Not covered | API-ENH-D-002 |
| SM-OP-037 | SM-SIT-A037 | ADAPTER | `AI inference / embeddings` | Internal adapter | AD-13, AD-14 | Split | Covered | — |
| SM-OP-038 | SM-SIT-A038 | GET | `/api/v1/admin/costs` | Admin | API-136 | Exact | Covered | — |
| SM-OP-039 | SM-SIT-A039 | POST | `/api/v1/admin/budgets` | Admin | API-137 | Exact | Covered | — |
| SM-OP-040 | SM-SIT-A040 | POST | `/api/v1/admin/budgets/{id}/pause` | Admin | API-144 | Alias | Covered | — |
| SM-OP-041 | SM-SIT-A041 | POST | `/api/v1/privacy/requests` | Portal + Admin (separate policy/DTO) | API-069 | Exact | Covered | — |
| SM-OP-042 | SM-SIT-A042 | GET | `/api/v1/admin/privacy/requests` | Admin | API-084 | Alias | Covered | — |
| SM-OP-043 | SM-SIT-A043 | POST | `/api/v1/admin/privacy/requests/{id}/resolve` | Admin | API-085, API-086, API-087 | Split | Covered | — |
| SM-OP-044 | SM-SIT-A044 | POST | `/api/v1/admin/retention-policies` | Admin | API-091 | Alias | Covered | — |
| SM-OP-045 | SM-SIT-A045 | GET | `/api/v1/health` | Internal worker | API-117 | Exact | Covered | — |
| SM-OP-046 | SM-SIT-A046 | GET | `/api/v1/ready` | Internal worker | API-118 | Exact | Covered | — |
| SM-OP-047 | SM-SIT-A047 | GET | `/api/v1/admin/health` | Admin | API-119 | Exact | Covered | — |
| SM-OP-048 | SM-SIT-A048 | POST | `/api/v1/admin/incidents/{id}/resolve` | Admin | API-129, API-130 | Split | Covered | — |
| SM-OP-049 | SM-SIT-A049 | GET | `/api/v1/research/plans` | Admin | API-180 | Alias | Covered | — |
| SM-OP-050 | SM-SIT-A050 | POST | `/api/v1/research/plans` | Admin | API-160 | Exact | Covered | — |
| SM-OP-051 | SM-SIT-A051 | POST | `/api/v1/research/run` | Admin | API-161 | Exact | Covered | — |
| SM-OP-052 | SM-SIT-A052 | PATCH | `/api/v1/research/plans/{id}` | Admin | API-181 | Alias | Covered | — |
| SM-OP-053 | SM-SIT-A053 | GET | `/api/v1/research/results` | Admin | API-162 | Exact | Covered | — |
| SM-OP-054 | SM-SIT-A054 | GET | `/api/v1/research/runs/{id}` | Admin | API-183 | Alias | Covered | — |
| SM-OP-055 | SM-SIT-A055 | ADAPTER | `Public web search` | Internal adapter | AD-05, AD-06 | Split | Covered | — |
| SM-OP-056 | SM-SIT-A056 | GET | `/api/v1/evidence/{id}` | Admin | API-163 | Exact | Covered | — |
| SM-OP-057 | SM-SIT-A057 | GET | `/api/v1/evidence` | Admin | API-186 | Alias | Covered | — |
| SM-OP-058 | SM-SIT-A058 | ADAPTER | `Permitted website fetch / extraction` | Internal adapter | AD-07 | Alias | Covered | — |
| SM-OP-059 | SM-SIT-A059 | GET | `/api/v1/organizations` | Admin | API-164 | Exact | Covered | — |
| SM-OP-060 | SM-SIT-A060 | POST | `/api/v1/organizations` | Admin | API-165 | Exact | Covered | — |
| SM-OP-061 | SM-SIT-A061 | GET | `/api/v1/organizations/{id}` | Admin | API-189 | Alias | Covered | — |
| SM-OP-062 | SM-SIT-A062 | POST | `/api/v1/organizations/{id}/merge` | Admin | API-190, API-191 | Split | Covered | — |
| SM-OP-063 | SM-SIT-A063 | GET | `/api/v1/signals` | Admin | API-166 | Exact | Covered | — |
| SM-OP-064 | SM-SIT-A064 | POST | `/api/v1/signals/{id}/review` | Admin | API-167 | Exact | Covered | — |
| SM-OP-065 | SM-SIT-A065 | POST | `/api/v1/admin/signal-types` | Admin | API-047 | Partial | Partially covered | API-ENH-D-003 |
| SM-OP-066 | SM-SIT-A066 | GET | `/api/v1/needs` | Admin | API-168 | Exact | Covered | — |
| SM-OP-067 | SM-SIT-A067 | POST | `/api/v1/needs/{id}/verify` | Admin | API-169 | Exact | Covered | — |
| SM-OP-068 | SM-SIT-A068 | GET | `/api/v1/matches` | Admin | API-192 | Alias | Covered | — |
| SM-OP-069 | SM-SIT-A069 | POST | `/api/v1/matches/recompute` | Admin | API-170 | Exact | Covered | — |
| SM-OP-070 | SM-SIT-A070 | GET | `/api/v1/opportunities` | Admin | API-171 | Exact | Covered | — |
| SM-OP-071 | SM-SIT-A071 | POST | `/api/v1/opportunities/{id}/score` | Admin | API-172 | Exact | Covered | — |
| SM-OP-072 | SM-SIT-A072 | POST | `/api/v1/admin/scoring-rules` | Admin | API-194, API-195 | Split | Covered | — |
| SM-OP-073 | SM-SIT-A073 | GET | `/api/v1/organizations/{id}/contacts` | Admin | API-173 | Exact | Covered | — |
| SM-OP-074 | SM-SIT-A074 | POST | `/api/v1/organizations/{id}/contacts/discover` | Admin | API-196 | Alias | Covered | — |
| SM-OP-075 | SM-SIT-A075 | POST | `/api/v1/admin/role-mappings` | Admin | API-199 | Partial | Partially covered | API-ENH-D-004 |
| SM-OP-076 | SM-SIT-A076 | ADAPTER | `Apollo.io account / person enrichment` | Internal adapter | AD-19 | Alias | Covered | — |
| SM-OP-077 | SM-SIT-A077 | GET | `/api/v1/contacts/verification-queue` | Admin | API-200 | Alias | Covered | — |
| SM-OP-078 | SM-SIT-A078 | POST | `/api/v1/contacts/{id}/verify` | Admin | API-174 | Exact | Covered | — |
| SM-OP-079 | SM-SIT-A079 | PATCH | `/api/v1/contacts/{id}` | Admin | API-197 | Alias | Covered | — |
| SM-OP-080 | SM-SIT-A080 | ADAPTER | `Business contact verification provider` | Internal adapter | AD-19 | Partial | Partially covered | AD-D02 |
| SM-OP-081 | SM-SIT-A081 | POST | `/api/v1/opportunities/{id}/review` | Admin | API-175 | Exact | Covered | — |
| SM-OP-082 | SM-SIT-A082 | GET | `/api/v1/alerts` | Admin | API-176 | Exact | Covered | — |
| SM-OP-083 | SM-SIT-A083 | POST | `/api/v1/admin/research-review-rules` | Admin | API-202 | Alias | Covered | — |
| SM-OP-084 | SM-SIT-A084 | POST | `/api/v1/alerts/{id}/read` | Admin |  | New | Not covered | API-ENH-D-005 |
| SM-OP-085 | SM-SIT-A085 | GET | `/api/v1/deals` | Admin | API-209 | Exact | Covered | — |
| SM-OP-086 | SM-SIT-A086 | POST | `/api/v1/deals` | Admin | API-210 | Exact | Covered | — |
| SM-OP-087 | SM-SIT-A087 | GET | `/api/v1/deals/{id}` | Admin | API-214, API-217 | Split | Covered | — |
| SM-OP-088 | SM-SIT-A088 | POST | `/api/v1/deals/{id}/transition` | Admin | API-211 | Exact | Covered | — |
| SM-OP-089 | SM-SIT-A089 | GET | `/api/v1/admin/pipeline-stages` | Admin | API-218 | Alias | Covered | — |
| SM-OP-090 | SM-SIT-A090 | POST | `/api/v1/admin/pipeline-stages` | Admin | API-219, API-220 | Split | Covered | — |
| SM-OP-091 | SM-SIT-A091 | POST | `/api/v1/deals/{id}/assign` | Admin | API-216 | Alias | Covered | — |
| SM-OP-092 | SM-SIT-A092 | GET | `/api/v1/public/forms/{slug}` | Public | API-228 | Alias | Covered | — |
| SM-OP-093 | SM-SIT-A093 | POST | `/api/v1/public/leads` | Public | API-212 | Exact | Covered | — |
| SM-OP-094 | SM-SIT-A094 | GET | `/api/v1/admin/forms` | Admin | API-221 | Alias | Covered | — |
| SM-OP-095 | SM-SIT-A095 | POST | `/api/v1/admin/forms` | Admin | API-222, API-223 | Split | Covered | — |
| SM-OP-096 | SM-SIT-A096 | GET | `/api/v1/organizations/{id}/360` | Admin | API-213 | Exact | Covered | — |
| SM-OP-097 | SM-SIT-A097 | POST | `/api/v1/engagement/check` | Admin | API-068 | Exact | Covered | — |
| SM-OP-098 | SM-SIT-A098 | GET | `/api/v1/workflows` | Admin | API-444 | Exact | Covered | — |
| SM-OP-099 | SM-SIT-A099 | POST | `/api/v1/admin/workflows` | Admin | API-446, API-448 | Split | Covered | — |
| SM-OP-100 | SM-SIT-A100 | POST | `/api/v1/admin/workflows/pause` | Admin | API-445 | Exact | Covered | — |
| SM-OP-101 | SM-SIT-A101 | POST | `/api/v1/admin/workflows/{id}/resume` | Admin | API-469, API-450 | Partial | Partially covered | API-ENH-D-006 |
| SM-OP-102 | SM-SIT-A102 | GET | `/api/v1/workflows/{id}/executions` | Admin | API-466 | Alias | Covered | — |
| SM-OP-103 | SM-SIT-A103 | POST | `/api/v1/messages/draft` | Admin | API-237 | Exact | Covered | — |
| SM-OP-104 | SM-SIT-A104 | GET | `/api/v1/admin/message-templates` | Admin | API-255 | Alias | Covered | — |
| SM-OP-105 | SM-SIT-A105 | POST | `/api/v1/admin/message-templates` | Admin | API-256 | Alias | Covered | — |
| SM-OP-106 | SM-SIT-A106 | POST | `/api/v1/messages/drafts/{id}/review` | Admin | API-541, API-539 | Approval | Covered | — |
| SM-OP-107 | SM-SIT-A107 | GET | `/api/v1/admin/approvals` | Admin | API-540 | Alias | Covered | — |
| SM-OP-108 | SM-SIT-A108 | POST | `/api/v1/messages/send` | Admin | API-238 | Exact | Covered | — |
| SM-OP-109 | SM-SIT-A109 | POST | `/api/v1/webhooks/email` | Provider callback | API-239 | Exact | Covered | — |
| SM-OP-110 | SM-SIT-A110 | GET | `/api/v1/messages/{id}` | Admin | API-252, API-257 | Partial | Partially covered | API-ENH-D-007 |
| SM-OP-111 | SM-SIT-A111 | ADAPTER | `Email delivery / inbound provider` | Internal adapter | AD-01 | Alias | Covered | — |
| SM-OP-112 | SM-SIT-A112 | POST | `/api/v1/webhooks/inbound` | Provider callback | API-240 | Exact | Covered | — |
| SM-OP-113 | SM-SIT-A113 | GET | `/api/v1/threads` | Admin | API-241 | Exact | Covered | — |
| SM-OP-114 | SM-SIT-A114 | GET | `/api/v1/threads/{id}/messages` | Admin | API-257 | Alias | Covered | — |
| SM-OP-115 | SM-SIT-A115 | POST | `/api/v1/threads/{id}/handoff` | Admin | API-259 | Alias | Covered | — |
| SM-OP-116 | SM-SIT-A116 | GET | `/api/v1/sequences` | Admin | API-261 | Alias | Covered | — |
| SM-OP-117 | SM-SIT-A117 | POST | `/api/v1/admin/sequences` | Admin | API-262 | Alias | Covered | — |
| SM-OP-118 | SM-SIT-A118 | POST | `/api/v1/sequences/{id}/enroll` | Admin | API-242 | Exact | Covered | — |
| SM-OP-119 | SM-SIT-A119 | POST | `/api/v1/enrollments/{id}/stop` | Admin | API-264 | Alias | Covered | — |
| SM-OP-120 | SM-SIT-A120 | GET | `/api/v1/enrollments` | Admin | API-263 | Alias | Covered | — |
| SM-OP-121 | SM-SIT-A121 | GET | `/api/v1/meetings` | Admin | API-268 | Alias | Covered | — |
| SM-OP-122 | SM-SIT-A122 | GET | `/api/v1/public/meeting-slots/{token}` | Portal | API-272 | Alias | Covered | — |
| SM-OP-123 | SM-SIT-A123 | POST | `/api/v1/meetings/book` | Portal + Admin (separate policy/DTO) | API-243 | Exact | Covered | — |
| SM-OP-124 | SM-SIT-A124 | POST | `/api/v1/webhooks/calendar` | Provider callback | API-244 | Exact | Covered | — |
| SM-OP-125 | SM-SIT-A125 | POST | `/api/v1/admin/calendar-links` | Admin | API-110 | Alias | Covered | — |
| SM-OP-126 | SM-SIT-A126 | ADAPTER | `Calendar availability / booking` | Internal adapter | AD-03, AD-04 | Split | Covered | — |
| SM-OP-127 | SM-SIT-A127 | GET | `/api/v1/metrics/funnel` | Admin | API-537 | Exact | Covered | — |
| SM-OP-128 | SM-SIT-A128 | GET | `/api/v1/tasks` | Admin | API-265 | Alias | Covered | — |
| SM-OP-129 | SM-SIT-A129 | PATCH | `/api/v1/tasks/{id}` | Admin | API-266 | Alias | Covered | — |
| SM-OP-130 | SM-SIT-A130 | GET | `/api/v1/admin/whatsapp/accounts` | Admin | API-109, API-102 | Partial | Partially covered | API-ENH-D-008 |
| SM-OP-131 | SM-SIT-A131 | POST | `/api/v1/admin/whatsapp/accounts` | Admin | API-107 | Alias | Covered | — |
| SM-OP-132 | SM-SIT-A132 | POST | `/api/v1/admin/whatsapp/templates` | Admin | API-108 | Alias | Covered | — |
| SM-OP-133 | SM-SIT-A133 | GET | `/api/v1/webhooks/whatsapp` | Provider callback | API-249 | Exact | Covered | — |
| SM-OP-134 | SM-SIT-A134 | POST | `/api/v1/webhooks/whatsapp` | Provider callback | API-245 | Exact | Covered | — |
| SM-OP-135 | SM-SIT-A135 | GET | `/api/v1/whatsapp/conversations` | Admin | API-241 | Alias | Covered | — |
| SM-OP-136 | SM-SIT-A136 | ADAPTER | `Meta WhatsApp Business API` | Internal adapter | AD-02 | Alias | Covered | — |
| SM-OP-137 | SM-SIT-A137 | POST | `/api/v1/public/chat` | Public | API-246 | Exact | Covered | — |
| SM-OP-138 | SM-SIT-A138 | POST | `/api/v1/admin/chat/settings` | Admin | API-280 | Partial | Partially covered | API-ENH-D-009 |
| SM-OP-139 | SM-SIT-A139 | GET | `/api/v1/inbox` | Admin | API-247 | Exact | Covered | — |
| SM-OP-140 | SM-SIT-A140 | POST | `/api/v1/threads/{id}/assign` | Admin | API-248 | Exact | Covered | — |
| SM-OP-141 | SM-SIT-A141 | POST | `/api/v1/admin/routing-rules` | Admin | API-283 | Alias | Covered | — |
| SM-OP-142 | SM-SIT-A142 | GET | `/api/v1/admin/compliance` | Admin | API-070 | Exact | Covered | — |
| SM-OP-143 | SM-SIT-A143 | POST | `/api/v1/admin/compliance/{id}/resolve` | Admin | API-094 | Alias | Covered | — |
| SM-OP-144 | SM-SIT-A144 | GET | `/api/v1/social/signals` | Admin | API-177 | Exact | Covered | — |
| SM-OP-145 | SM-SIT-A145 | POST | `/api/v1/admin/social/sources` | Admin | API-206 | Alias | Covered | — |
| SM-OP-146 | SM-SIT-A146 | ADAPTER | `Authorized social listening API` | Internal adapter | AD-08 | Alias | Covered | — |
| SM-OP-147 | SM-SIT-A147 | GET | `/api/v1/content` | Admin | API-299 | Alias | Covered | — |
| SM-OP-148 | SM-SIT-A148 | POST | `/api/v1/content/draft` | Admin | API-284 | Exact | Covered | — |
| SM-OP-149 | SM-SIT-A149 | PATCH | `/api/v1/content/{id}` | Admin | API-301 | Alias | Covered | — |
| SM-OP-150 | SM-SIT-A150 | POST | `/api/v1/content/{id}/approve` | Admin | API-285 | Exact | Covered | — |
| SM-OP-151 | SM-SIT-A151 | GET | `/api/v1/social/posts` | Admin | API-302 | Alias | Covered | — |
| SM-OP-152 | SM-SIT-A152 | POST | `/api/v1/social/posts` | Admin | API-286 | Exact | Covered | — |
| SM-OP-153 | SM-SIT-A153 | GET | `/api/v1/social/status` | Admin | API-287 | Exact | Covered | — |
| SM-OP-154 | SM-SIT-A154 | POST | `/api/v1/admin/social/accounts` | Admin | API-113 | Alias | Covered | — |
| SM-OP-155 | SM-SIT-A155 | POST | `/api/v1/social/posts/{id}/cancel` | Admin | API-303 | Alias | Covered | — |
| SM-OP-156 | SM-SIT-A156 | ADAPTER | `Official social publishing API` | Internal adapter | AD-08 | Alias | Covered | — |
| SM-OP-157 | SM-SIT-A157 | GET | `/api/v1/seo/audit` | Admin | API-288 | Exact | Covered | — |
| SM-OP-158 | SM-SIT-A158 | POST | `/api/v1/seo/tasks` | Admin | API-289 | Exact | Covered | — |
| SM-OP-159 | SM-SIT-A159 | POST | `/api/v1/seo/audit/run` | Admin | API-289 | Alias | Covered | — |
| SM-OP-160 | SM-SIT-A160 | ADAPTER | `Search Console / site audit` | Internal adapter | AD-17 | Partial | Partially covered | AD-D03 |
| SM-OP-161 | SM-SIT-A161 | GET | `/api/v1/landing-pages` | Admin | API-308 | Alias | Covered | — |
| SM-OP-162 | SM-SIT-A162 | POST | `/api/v1/landing-pages` | Admin | API-309 | Alias | Covered | — |
| SM-OP-163 | SM-SIT-A163 | POST | `/api/v1/landing-pages/{id}/publish` | Admin | API-492 | Alias | Covered | — |
| SM-OP-164 | SM-SIT-A164 | GET | `/api/v1/public/pages/{slug}` | Public | API-290 | Exact | Covered | — |
| SM-OP-165 | SM-SIT-A165 | POST | `/api/v1/public/events` | Public | API-291 | Exact | Covered | — |
| SM-OP-166 | SM-SIT-A166 | GET | `/api/v1/campaigns` | Admin | API-311 | Alias | Covered | — |
| SM-OP-167 | SM-SIT-A167 | POST | `/api/v1/campaigns` | Admin | API-292 | Exact | Covered | — |
| SM-OP-168 | SM-SIT-A168 | POST | `/api/v1/campaigns/{id}/approve` | Admin | API-293 | Exact | Covered | — |
| SM-OP-169 | SM-SIT-A169 | POST | `/api/v1/campaigns/{id}/pause` | Admin | API-316 | Alias | Covered | — |
| SM-OP-170 | SM-SIT-A170 | POST | `/api/v1/ads/drafts` | Admin | API-294 | Exact | Covered | — |
| SM-OP-171 | SM-SIT-A171 | GET | `/api/v1/ads/metrics` | Admin | API-295 | Exact | Covered | — |
| SM-OP-172 | SM-SIT-A172 | POST | `/api/v1/ads/{id}/launch` | Admin | API-318 | Alias | Covered | — |
| SM-OP-173 | SM-SIT-A173 | POST | `/api/v1/ads/{id}/pause` | Admin | API-319 | Alias | Covered | — |
| SM-OP-174 | SM-SIT-A174 | ADAPTER | `Advertising provider API` | Internal adapter | AD-09 | Alias | Covered | — |
| SM-OP-175 | SM-SIT-A175 | GET | `/api/v1/events/business` | Admin | API-322 | Alias | Covered | — |
| SM-OP-176 | SM-SIT-A176 | POST | `/api/v1/events/business` | Admin | API-323 | Alias | Covered | — |
| SM-OP-177 | SM-SIT-A177 | GET | `/api/v1/public/events/{id}` | Public | API-326 | Alias | Covered | — |
| SM-OP-178 | SM-SIT-A178 | POST | `/api/v1/events/register` | Public | API-296 | Exact | Covered | — |
| SM-OP-179 | SM-SIT-A179 | POST | `/api/v1/webhooks/events` | Provider callback | API-297 | Exact | Covered | — |
| SM-OP-180 | SM-SIT-A180 | POST | `/api/v1/admin/events/{id}/settings` | Admin | API-325 | Alias | Covered | — |
| SM-OP-181 | SM-SIT-A181 | ADAPTER | `Webinar provider API` | Internal adapter | AD-18 | Alias | Covered | — |
| SM-OP-182 | SM-SIT-A182 | POST | `/api/v1/public/referrals` | Public | API-298 | Exact | Covered | — |
| SM-OP-183 | SM-SIT-A183 | GET | `/api/v1/admin/referrals` | Admin | API-327 | Alias | Covered | — |
| SM-OP-184 | SM-SIT-A184 | POST | `/api/v1/admin/referrals/{id}/review` | Admin | API-541, API-539 | Approval | Covered | — |
| SM-OP-185 | SM-SIT-A185 | GET | `/api/v1/deals/{id}/proposals` | Admin | API-334, API-335 | Split | Covered | — |
| SM-OP-186 | SM-SIT-A186 | POST | `/api/v1/deals/{id}/proposals` | Admin | API-328 | Exact | Covered | — |
| SM-OP-187 | SM-SIT-A187 | POST | `/api/v1/proposals/{id}/review` | Admin | API-541, API-539 | Approval | Covered | — |
| SM-OP-188 | SM-SIT-A188 | GET | `/api/v1/quotes` | Admin | API-338 | Alias | Covered | — |
| SM-OP-189 | SM-SIT-A189 | POST | `/api/v1/quotes` | Admin | API-329 | Exact | Covered | — |
| SM-OP-190 | SM-SIT-A190 | POST | `/api/v1/quotes/{id}/approve` | Admin | API-330 | Exact | Covered | — |
| SM-OP-191 | SM-SIT-A191 | GET | `/api/v1/deals/{id}/objections` | Admin | API-343 | Alias | Covered | — |
| SM-OP-192 | SM-SIT-A192 | POST | `/api/v1/deals/{id}/objections` | Admin | API-331 | Exact | Covered | — |
| SM-OP-193 | SM-SIT-A193 | POST | `/api/v1/negotiations/{id}/review` | Admin | API-347 | Alias | Covered | — |
| SM-OP-194 | SM-SIT-A194 | GET | `/api/v1/contracts` | Admin | API-348 | Alias | Covered | — |
| SM-OP-195 | SM-SIT-A195 | POST | `/api/v1/contracts` | Admin | API-332 | Exact | Covered | — |
| SM-OP-196 | SM-SIT-A196 | GET | `/api/v1/public/agreements/{token}` | Portal | API-358 | Alias | Covered | — |
| SM-OP-197 | SM-SIT-A197 | POST | `/api/v1/public/agreements/{token}/sign` | Portal | API-359 | Alias | Covered | — |
| SM-OP-198 | SM-SIT-A198 | POST | `/api/v1/contracts/{id}/approve` | Admin | API-541, API-539 | Approval | Covered | — |
| SM-OP-199 | SM-SIT-A199 | POST | `/api/v1/webhooks/esign` | Provider callback | API-333 | Exact | Covered | — |
| SM-OP-200 | SM-SIT-A200 | ADAPTER | `E-sign provider API` | Internal adapter | AD-10 | Alias | Covered | — |
| SM-OP-201 | SM-SIT-A201 | GET | `/api/v1/deals/{id}/payments` | Admin | API-393 | Alias | Covered | — |
| SM-OP-202 | SM-SIT-A202 | POST | `/api/v1/deals/{id}/invoices` | Admin | API-390 | Alias | Covered | — |
| SM-OP-203 | SM-SIT-A203 | GET | `/api/v1/public/payment-status/{token}` | Portal | API-409 | Alias | Covered | — |
| SM-OP-204 | SM-SIT-A204 | POST | `/api/v1/webhooks/payment` | Provider callback | API-385 | Exact | Covered | — |
| SM-OP-205 | SM-SIT-A205 | POST | `/api/v1/deals/{id}/close` | Admin | API-386 | Exact | Covered | — |
| SM-OP-206 | SM-SIT-A206 | POST | `/api/v1/payments/{id}/reconcile` | Admin | API-394, API-395, API-396 | Split | Covered | — |
| SM-OP-207 | SM-SIT-A207 | POST | `/api/v1/invoices/{id}/payment-link` | Portal + Admin (separate policy/DTO) | API-398 | Alias | Covered | — |
| SM-OP-208 | SM-SIT-A208 | ADAPTER | `Payment gateway API` | Internal adapter | AD-11 | Alias | Covered | — |
| SM-OP-209 | SM-SIT-A209 | GET | `/api/v1/onboarding` | Admin | API-412 | Exact | Covered | — |
| SM-OP-210 | SM-SIT-A210 | GET | `/api/v1/public/onboarding/{token}` | Portal | API-437 | Alias | Covered | — |
| SM-OP-211 | SM-SIT-A211 | POST | `/api/v1/onboarding/{id}/complete` | Portal + Admin (separate policy/DTO) | API-413 | Exact | Covered | — |
| SM-OP-212 | SM-SIT-A212 | POST | `/api/v1/onboarding/{id}/assign` | Admin | API-425 | Alias | Covered | — |
| SM-OP-213 | SM-SIT-A213 | GET | `/api/v1/partners` | Admin | API-427 | Alias | Covered | — |
| SM-OP-214 | SM-SIT-A214 | POST | `/api/v1/partners` | Admin | API-414 | Exact | Covered | — |
| SM-OP-215 | SM-SIT-A215 | POST | `/api/v1/pilots/{id}/status` | Admin | API-415 | Exact | Covered | — |
| SM-OP-216 | SM-SIT-A216 | POST | `/api/v1/partner-pilots` | Admin | API-419 | Alias | Covered | — |
| SM-OP-217 | SM-SIT-A217 | GET | `/api/v1/renewals` | Admin | API-416 | Exact | Covered | — |
| SM-OP-218 | SM-SIT-A218 | POST | `/api/v1/renewals/{id}/review` | Admin | API-417 | Exact | Covered | — |
| SM-OP-219 | SM-SIT-A219 | POST | `/api/v1/admin/renewal-policies` | Admin | API-429 | Alias | Covered | — |
| SM-OP-220 | SM-SIT-A220 | POST | `/api/v1/deals/{id}/lost` | Admin | API-387 | Exact | Covered | — |
| SM-OP-221 | SM-SIT-A221 | POST | `/api/v1/feedback` | Admin | API-418 | Exact | Covered | — |
| SM-OP-222 | SM-SIT-A222 | GET | `/api/v1/feedback` | Admin | API-431 | Alias | Covered | — |
| SM-OP-223 | SM-SIT-A223 | GET | `/api/v1/metrics/revenue` | Admin | API-388 | Exact | Covered | — |
| SM-OP-224 | SM-SIT-A224 | POST | `/api/v1/admin/kpi-definitions` | Admin | API-405 | Alias | Covered | — |
| SM-OP-225 | SM-SIT-A225 | POST | `/api/v1/admin/evals/run` | Admin | API-138 | Exact | Covered | — |
| SM-OP-226 | SM-SIT-A226 | GET | `/api/v1/admin/evals/results` | Admin | API-147, API-148 | Split | Covered | — |
| SM-OP-227 | SM-SIT-A227 | GET | `/api/v1/market/competitors` | Admin | API-178 | Exact | Covered | — |
| SM-OP-228 | SM-SIT-A228 | POST | `/api/v1/admin/competitor-sources` | Admin | API-208 | Alias | Covered | — |
| SM-OP-229 | SM-SIT-A229 | GET | `/api/v1/metrics/forecast` | Admin | API-389 | Exact | Covered | — |
| SM-OP-230 | SM-SIT-A230 | POST | `/api/v1/admin/forecast-settings` | Admin | API-407 | Partial | Partially covered | API-ENH-D-010 |
| SM-OP-231 | SM-SIT-A231 | GET | `/api/v1/admin/dashboard` | Admin | API-538 | Exact | Covered | — |
| SM-OP-232 | SM-SIT-A232 | POST | `/api/v1/admin/approvals/{id}/decide` | Admin | API-539 | Exact | Covered | — |
| SM-OP-233 | SM-SIT-A233 | GET | `/api/v1/admin/releases` | Admin | API-120 | Exact | Covered | — |
| SM-OP-234 | SM-SIT-A234 | POST | `/api/v1/admin/releases/{id}/approve` | Admin | API-132 | Alias | Covered | — |
| SM-OP-235 | SM-SIT-A235 | ADAPTER | `CI/CD and health monitoring` | Internal adapter | AD-15, AD-16, API-133 | Split | Covered | — |
| SM-OP-236 | SM-SIT-A236 | GET | `/api/v1/insurance/pilots` | Admin |  | New | Not covered | API-ENH-D-011 |
| SM-OP-237 | SM-SIT-A237 | POST | `/api/v1/pilots` | Admin | API-419 | Exact | Covered | — |
| SM-OP-238 | SM-SIT-A238 | POST | `/api/v1/insurance/pilots/{id}/approve` | Admin | API-541, API-539 | Approval | Covered | — |
| SM-OP-239 | SM-SIT-A239 | GET | `/api/v1/integration-enquiries` | Admin | API-433 | Alias | Covered | — |
| SM-OP-240 | SM-SIT-A240 | POST | `/api/v1/integration-enquiries` | Admin | API-420 | Exact | Covered | — |
| SM-OP-241 | SM-SIT-A241 | POST | `/api/v1/integration-enquiries/{id}/approve` | Admin | API-541, API-539 | Approval | Covered | — |
| SM-OP-242 | SM-SIT-A242 | GET | `/api/v1/deployments` | Admin | API-421 | Exact | Covered | — |
| SM-OP-243 | SM-SIT-A243 | POST | `/api/v1/deployments/{id}/approve` | Admin | API-541, API-539 | Approval | Covered | — |
| SM-OP-244 | SM-SIT-A244 | PATCH | `/api/v1/deployments/{id}` | Admin | API-435 | Alias | Covered | — |
| SM-OP-245 | SM-SIT-A245 | GET | `/api/v1/admin/products/planned` | Admin | API-064 | Alias | Covered | — |
| SM-OP-246 | SM-SIT-A246 | POST | `/api/v1/admin/products/{id}/launch` | Admin | API-050 | Exact | Covered | — |
| SM-OP-247 | SM-SIT-A247 | GET | `/api/v1/sales/tenants` | Admin | API-026 | Alias | Covered | — |
| SM-OP-248 | SM-SIT-A248 | POST | `/api/v1/sales/tenants` | Admin | API-027 | Alias | Covered | — |
| SM-OP-249 | SM-SIT-A249 | POST | `/api/v1/sales/tenants/{id}/control` | Admin | API-028 | Alias | Covered | — |
| SM-OP-250 | SM-SIT-A250 | GET | `/api/v1/sales/startups` | Admin | API-029 | Alias | Covered | — |
| SM-OP-251 | SM-SIT-A251 | POST | `/api/v1/sales/startups` | Admin | API-030 | Alias | Covered | — |
| SM-OP-252 | SM-SIT-A252 | PATCH | `/api/v1/sales/startups/{id}` | Admin | API-031, API-039 | Split | Covered | — |
| SM-OP-253 | SM-SIT-A253 | POST | `/api/v1/sales/memberships` | Admin | API-020, API-022 | Split | Covered | — |
| SM-OP-254 | SM-SIT-A254 | POST | `/api/v1/sales/support-grants` | Admin | API-024, API-025 | Split | Covered | — |
| SM-OP-255 | SM-SIT-A255 | GET | `/api/v1/sales/templates` | Admin | API-033 | Alias | Covered | — |
| SM-OP-256 | SM-SIT-A256 | POST | `/api/v1/sales/templates` | Admin | API-034 | Alias | Covered | — |
| SM-OP-257 | SM-SIT-A257 | POST | `/api/v1/sales/templates/{id}/control` | Admin | API-035, API-036, API-037, API-541, API-539 | Split | Covered | — |
| SM-OP-258 | SM-SIT-A258 | GET | `/api/v1/sales/domains` | Admin | API-044 | Alias | Covered | — |
| SM-OP-259 | SM-SIT-A259 | POST | `/api/v1/sales/domains` | Admin | API-045 | Alias | Covered | — |
| SM-OP-260 | SM-SIT-A260 | POST | `/api/v1/sales/domains/{id}/control` | Admin | API-046 | Partial | Partially covered | API-ENH-D-012 |
| SM-OP-261 | SM-SIT-A261 | GET | `/api/v1/sales/service-plans` | Admin | API-519 | Alias | Covered | — |
| SM-OP-262 | SM-SIT-A262 | POST | `/api/v1/sales/service-plans` | Admin | API-520, API-541, API-539 | Split | Covered | — |
| SM-OP-263 | SM-SIT-A263 | GET | `/api/v1/sales/service-subscriptions` | Admin | API-521 | Alias | Covered | — |
| SM-OP-264 | SM-SIT-A264 | POST | `/api/v1/sales/service-subscriptions/{id}/control` | Admin | API-522, API-523, API-524, API-525 | Split | Covered | — |
| SM-OP-265 | SM-SIT-A265 | GET | `/api/v1/sales/service-invoices` | Admin | API-526 | Alias | Covered | — |
| SM-OP-266 | SM-SIT-A266 | POST | `/api/v1/sales/service-invoices/{id}/reconcile` | Admin |  | New | Not covered | API-ENH-D-013 |
| SM-OP-267 | SM-SIT-A267 | GET | `/api/v1/sales/usage-charges` | Admin | API-528 | Partial | Partially covered | API-ENH-D-014 |
| SM-OP-268 | SM-SIT-A268 | POST | `/api/v1/sales/usage-charges/{id}/adjust` | Admin |  | New | Not covered | API-ENH-D-015 |
| SM-OP-269 | SM-SIT-A269 | GET | `/api/v1/sales/action-plans` | Admin | API-453 | Alias | Covered | — |
| SM-OP-270 | SM-SIT-A270 | POST | `/api/v1/sales/action-plans` | Admin | API-454, API-455 | Split | Covered | — |
| SM-OP-271 | SM-SIT-A271 | POST | `/api/v1/sales/action-plans/{id}/control` | Admin | API-456, API-457, API-458, API-541, API-539 | Split | Covered | — |
| SM-OP-272 | SM-SIT-A272 | GET | `/api/v1/sales/data-transfers` | Admin | API-530 | Alias | Covered | — |
| SM-OP-273 | SM-SIT-A273 | POST | `/api/v1/sales/data-transfers` | Admin | API-531, API-534 | Split | Covered | — |
| SM-OP-274 | SM-SIT-A274 | POST | `/api/v1/sales/data-transfers/{id}/complete` | Admin | API-532 | Alias | Covered | — |
| SM-OP-275 | SM-SIT-A275 | POST | `/api/v1/sales/data-transfers/{id}/control` | Admin | API-536, API-541, API-539 | Split | Covered | — |
| SM-OP-276 | SM-SIT-A276 | GET | `/api/v1/sales/data-transfers/{id}/download` | Admin | API-535 | Alias | Covered | — |
| SM-OP-277 | SM-SIT-A277 | GET | `/api/v1/sales/bids` | Admin | API-362 | Alias | Covered | — |
| SM-OP-278 | SM-SIT-A278 | POST | `/api/v1/sales/bids` | Admin | API-363 | Alias | Covered | — |
| SM-OP-279 | SM-SIT-A279 | PATCH | `/api/v1/sales/bids/{id}` | Admin | API-365 | Alias | Covered | — |
| SM-OP-280 | SM-SIT-A280 | POST | `/api/v1/sales/bids/{id}/control` | Admin | API-366, API-367, API-368, API-369, API-541, API-539 | Split | Covered | — |
| SM-OP-281 | SM-SIT-A281 | GET | `/api/v1/sales/orders` | Admin | API-370 | Alias | Covered | — |
| SM-OP-282 | SM-SIT-A282 | POST | `/api/v1/sales/orders` | Admin | API-371 | Alias | Covered | — |
| SM-OP-283 | SM-SIT-A283 | PATCH | `/api/v1/sales/orders/{id}` | Admin | API-373 | Alias | Covered | — |
| SM-OP-284 | SM-SIT-A284 | POST | `/api/v1/sales/orders/{id}/control` | Admin | API-374, API-375, API-376, API-378 | Split | Covered | — |
| SM-OP-285 | SM-SIT-A285 | POST | `/api/v1/sales/orders/{id}/milestones` | Admin | API-377 | Alias | Covered | — |
| SM-OP-286 | SM-SIT-A286 | POST | `/api/v1/sales/milestones/{id}/accept` | Admin | API-383, API-384 | Partial | Partially covered | API-ENH-D-016 |
| SM-OP-287 | SM-SIT-A287 | GET | `/api/v1/sales/notifications` | Admin | API-549 | Alias | Covered | — |
| SM-OP-288 | SM-SIT-A288 | PATCH | `/api/v1/sales/notifications/{id}` | Admin | API-550, API-552 | Split | Covered | — |
| SM-OP-289 | SM-SIT-A289 | GET | `/api/v1/commercial/public/site/pages/{slug}` | Public | API-290 | Alias | Covered | — |
| SM-OP-290 | SM-SIT-A290 | GET | `/api/v1/commercial/admin/website/pages` | Admin | API-486 | Alias | Covered | — |
| SM-OP-291 | SM-SIT-A291 | POST | `/api/v1/commercial/admin/website/pages` | Admin | API-487, API-488 | Split | Covered | — |
| SM-OP-292 | SM-SIT-A292 | POST | `/api/v1/commercial/admin/website/pages/{id}/control` | Admin | API-489, API-490, API-492, API-494, API-495, API-541, API-539 | Split | Covered | — |
| SM-OP-293 | SM-SIT-A293 | POST | `/api/v1/commercial/admin/external-grants` | Admin | API-227 | Alias | Covered | — |
| SM-OP-294 | SM-SIT-A294 | POST | `/api/v1/commercial/admin/external-grants/{id}/control` | Admin |  | New | Not covered | API-ENH-D-017 |
| SM-OP-295 | SM-SIT-A295 | POST | `/api/v1/commercial/portal/external-grants/accept` | Portal | API-013 | Alias | Covered | — |
| SM-OP-296 | SM-SIT-A296 | POST | `/api/v1/commercial/portal/documents` | Portal | API-235 | Alias | Covered | — |
| SM-OP-297 | SM-SIT-A297 | POST | `/api/v1/commercial/portal/documents/{id}/complete` | Portal | API-236 | Partial | Partially covered | API-ENH-D-018 |
| SM-OP-298 | SM-SIT-A298 | GET | `/api/v1/commercial/portal/overview` | Portal | API-436 | Alias | Covered | — |
| SM-OP-299 | SM-SIT-A299 | GET | `/api/v1/commercial/portal/quotations/{id}` | Portal | API-354, API-355 | Split | Covered | — |
| SM-OP-300 | SM-SIT-A300 | POST | `/api/v1/commercial/portal/quotations/{id}/respond` | Portal | API-356, API-357 | Split | Covered | — |
| SM-OP-301 | SM-SIT-A301 | GET | `/api/v1/commercial/portal/orders/{id}` | Portal | API-382 | Exact | Covered | — |
| SM-OP-302 | SM-SIT-A302 | POST | `/api/v1/commercial/portal/requests` | Portal | API-440, API-069 | Split | Covered | — |

### 3.5.4.4 Candidate operations (SM-UX-API-01…19) → blueprint

| Candidate | Method | Path | Screen | Audience | Blueprint operation(s) | Relation | Status | Enhancement |
|---|---|---|---|---|---|---|---|---|
| SM-UX-API-01 | GET | `/api/v1/commercial/workspace/public/plans` | W31 | Public | API-501 | Alias | Covered | — |
| SM-UX-API-02 | POST | `/api/v1/commercial/workspace/public/applications` | W32 | Public intake | API-503, API-505, API-506 | Split | Covered | — |
| SM-UX-API-03 | GET | `/api/v1/commercial/workspace/onboarding/{id}` | W33 | Onboarding applicant | API-507 | Partial | Partially covered | API-ENH-D-019 |
| SM-UX-API-04 | PATCH | `/api/v1/commercial/workspace/onboarding/{id}` | W33 | Onboarding applicant | API-504, API-509 | Split | Covered | — |
| SM-UX-API-05 | POST | `/api/v1/commercial/workspace/onboarding/{id}/submit` | W33 | Onboarding applicant | API-511 | Alias | Covered | — |
| SM-UX-API-06 | GET | `/api/v1/commercial/workspace/client/service` | W34 | SaaS client | API-513, API-514, API-515 | Split | Covered | — |
| SM-UX-API-07 | POST | `/api/v1/commercial/workspace/client/service-requests` | W34 | SaaS client | API-516, API-517, API-440 | Partial | Partially covered | API-ENH-D-020 |
| SM-UX-API-08 | GET | `/api/v1/commercial/workspace/admin/triggers` | A109 | Admin | API-459 | Alias | Covered | — |
| SM-UX-API-09 | POST | `/api/v1/commercial/workspace/admin/triggers` | A109 | Admin | API-460 | Alias | Covered | — |
| SM-UX-API-10 | POST | `/api/v1/commercial/workspace/admin/triggers/{id}/control` | A109 | Admin | API-464, API-465, API-541, API-539 | Split | Covered | — |
| SM-UX-API-11 | GET | `/api/v1/commercial/workspace/admin/executions` | A110 | Admin | API-466 | Alias | Covered | — |
| SM-UX-API-12 | GET | `/api/v1/commercial/workspace/admin/conflicts` | A111 | Admin | API-473 | Alias | Covered | — |
| SM-UX-API-13 | POST | `/api/v1/commercial/workspace/admin/conflicts/{id}/resolve` | A111 | Admin | API-475, API-476 | Split | Covered | — |
| SM-UX-API-14 | GET | `/api/v1/commercial/workspace/admin/configurations` | A112 | Admin | API-038 | Alias | Covered | — |
| SM-UX-API-15 | POST | `/api/v1/commercial/workspace/admin/configurations` | A112 | Admin | API-039 | Alias | Covered | — |
| SM-UX-API-16 | POST | `/api/v1/commercial/workspace/admin/configurations/{id}/control` | A112 | Admin | API-041, API-042, API-043, API-541, API-539 | Split | Covered | — |
| SM-UX-API-17 | GET | `/api/v1/commercial/workspace/admin/automation-templates` | A113 | Admin | API-477 | Alias | Covered | — |
| SM-UX-API-18 | POST | `/api/v1/commercial/workspace/admin/automation-templates` | A113 | Admin | API-479, API-480 | Partial | Partially covered | API-ENH-D-021 |
| SM-UX-API-19 | POST | `/api/v1/commercial/workspace/admin/automation-templates/{id}/control` | A113 | Admin | API-481, API-482, API-541, API-539 | Split | Covered | — |

### 3.5.4.5 Reverse mapping: Part 3.2 operations with no source counterpart

These 212 operations are **retained**: they are DERIVED operations that Part 3.2 added from screen actions, BFF/session needs, portal self-service, approvals, reconciliation, Copilot, inventory, ledgers and support (§3.2.2.1 steps 3–4). None contradicts document 07; document 07 simply does not enumerate them. They receive source-style tracking IDs only through the OpenAPI `x-source-op: none` marker [RECOMMENDATION-360].

| Part 3.2 domain | Ops | Referenced by a source operation | Blueprint-only (DERIVED beyond the source) | Blueprint-only operation IDs |
|---|---|---|---|---|
| Identity, session and BFF | 25 | 11 | 14 | 003, 004, 005, 006, 008, 009, 010, 011, 014, 015, 016, 017, 018, 023 |
| Tenancy, configuration and business templates | 22 | 20 | 2 | 032, 040 |
| Catalogue and knowledge | 18 | 12 | 6 | 058, 059, 060, 062, 063, 065 |
| Governance: consent, eligibility, privacy, compliance | 29 | 17 | 12 | 075, 077, 078, 079, 080, 081, 082, 088, 089, 090, 092, 093 |
| Integrations and channel configuration | 20 | 10 | 10 | 098, 100, 101, 103, 104, 105, 106, 111, 112, 114 |
| Events, audit, jobs, health and release | 19 | 11 | 8 | 121, 122, 123, 125, 126, 127, 128, 131 |
| AI gateway, cost, quality and Copilot | 24 | 9 | 15 | 139, 140, 141, 143, 145, 146, 149, 150, 151, 152, 153, 154, 155, 156, 157 |
| Intelligence: sources, research, evidence, organizations, signals, matching, qualification | 51 | 39 | 12 | 182, 184, 185, 187, 188, 193, 198, 201, 203, 204, 205, 207 |
| CRM, leads and Customer 360 | 28 | 18 | 10 | 215, 224, 225, 226, 229, 230, 231, 232, 233, 234 |
| Engagement: drafting, messaging, inbox, sequences, meetings, chat | 47 | 28 | 19 | 250, 251, 253, 254, 258, 260, 267, 269, 270, 271, 273, 274, 275, 276, 277, 278, 279, 281, 282 |
| Marketing: content, social, SEO, landing pages, campaigns, ads, events, referrals | 44 | 30 | 14 | 300, 304, 305, 306, 307, 310, 312, 313, 314, 315, 317, 320, 321, 324 |
| Commerce: proposals, quotes, negotiation, contracts | 34 | 18 | 16 | 336, 337, 339, 340, 341, 342, 344, 345, 346, 349, 350, 351, 352, 353, 360, 361 |
| Vertical desks: bids, orders, fulfilment, inventory | 23 | 18 | 5 | 364, 372, 379, 380, 381 |
| Finance: invoices, payments, ledgers, closure, revenue, forecast | 27 | 14 | 13 | 391, 392, 397, 399, 400, 401, 402, 403, 404, 406, 408, 410, 411 |
| Lifecycle: onboarding, partners, renewals, feedback, pilots, licensing, expansion, support | 32 | 19 | 13 | 422, 423, 424, 426, 428, 430, 432, 434, 438, 439, 441, 442, 443 |
| Automation: workflows, plans, triggers, runs, conflicts, templates | 40 | 25 | 15 | 447, 449, 451, 452, 461, 462, 463, 467, 468, 470, 471, 472, 474, 478, 483 |
| Website publishing | 17 | 8 | 9 | 484, 485, 491, 493, 496, 497, 498, 499, 500 |
| SaaS service lifecycle and portability | 36 | 28 | 8 | 502, 508, 510, 512, 518, 527, 529, 533 |
| Command Centre, approvals, notifications, search, reports | 19 | 8 | 11 | 542, 543, 544, 545, 546, 547, 548, 551, 553, 554, 555 |
| **Total** | **555** | **343** | **212** | IDs shown without the `API-` prefix |

### 3.5.4.6 Access-boundary differences (10 operations)

| Source op | Method and path | Source boundary | Part 3.2 op and namespace | Assessment | Resolution |
|---|---|---|---|---|---|
| SM-OP-017 | GET `/api/v1/public/preferences/{token}` | Portal | API-083 (public) | Conflict (CONFLICT-367) | Classify API-083 as `portal` (signed token route) per Part 3.2 rule (3); serve on api-web; RL-PUB-W |
| SM-OP-018 | POST `/api/v1/consents` | Portal + Admin (separate policy/DTO) | API-066 (admin+internal) | Compatible split | Admin/internal consent capture stays API-066; portal consent changes use API-082 (own preferences) with a portal serializer |
| SM-OP-019 | POST `/api/v1/opt-out` | Public | API-067 (portal) | Compatible | Part 3.2 already treats opt-out as a token-bound portal route on the website ingress; no change |
| SM-OP-041 | POST `/api/v1/privacy/requests` | Portal + Admin (separate policy/DTO) | API-069 (public+portal) | Partial (CONFLICT-366) | Keep API-069 for subjects; add API-ENH-D-024 for staff recording an offline request |
| SM-OP-097 | POST `/api/v1/engagement/check` | Admin | API-068 (admin+internal) | Compatible superset | Internal mount is for PDP pre-checks by workers; Admin behaviour identical |
| SM-OP-123 | POST `/api/v1/meetings/book` | Portal + Admin (separate policy/DTO) | API-243 (admin) | Compatible split (CONFLICT-366) | Admin booking API-243; portal/public booking through API-273/274 (hold then confirm) |
| SM-OP-207 | POST `/api/v1/invoices/{id}/payment-link` | Portal + Admin (separate policy/DTO) | API-398 (admin) | Conflict (CONFLICT-366) | Payment-link creation stays Admin (R08) because it starts an external effect; portal users read the issued link through API-410 |
| SM-OP-211 | POST `/api/v1/onboarding/{id}/complete` | Portal + Admin (separate policy/DTO) | API-413 (admin) | Compatible split | Admin completion API-413; customer completes own steps via API-438 |
| SM-OP-221 | POST `/api/v1/feedback` | Admin | API-418 (admin+portal) | Compatible superset | No change |
| SM-OP-286 | POST `/api/v1/sales/milestones/{id}/accept` | Admin | API-383, API-384 (portal) | Partial | Portal acceptance (sell direction) API-383/384; Admin acceptance for buy direction API-ENH-D-016 |

### 3.5.4.7 Status-code reconciliation (24 operations where the source proposal differs from the Part 3.2 side-effect rule)

Only operations with relation Exact or Alias are listed; split operations take the status of each target (file b §3.5.5.3). **Rule applied (CONFLICT-370):** Part 3.2 §3.2.1.10 is normative: work that is queued or starts an external effect returns 202 with a run reference; the source's 201/200 proposals for such operations are superseded. Public intake returns 202 because processing is asynchronous and a duplicate returns the same reference (CA-INTAKE).

| Source op | Method and source path | Source proposed | Part 3.2 op (SE class) | Normative status (Part 3.5) | Reason |
|---|---|---|---|---|---|
| SM-OP-012 | POST `/api/v1/knowledge/uploads` | 201 | API-051 (Q) | **202** | Asynchronous work or external effect (SE Q/X): 202 + run reference (§3.2.1.10/11) |
| SM-OP-025 | POST `/api/v1/admin/integrations/test` | 200 | API-096 (Q) | **202** | Asynchronous work or external effect (SE Q/X): 202 + run reference (§3.2.1.10/11) |
| SM-OP-041 | POST `/api/v1/privacy/requests` | 201 | API-069 (Q) | **202** | Asynchronous work or external effect (SE Q/X): 202 + run reference (§3.2.1.10/11) |
| SM-OP-078 | POST `/api/v1/contacts/{id}/verify` | 200 | API-174 (Q) | **202** | Asynchronous work or external effect (SE Q/X): 202 + run reference (§3.2.1.10/11) |
| SM-OP-093 | POST `/api/v1/public/leads` | 201 | API-212 (I) | **202** | Public intake: durable acknowledgement, processing asynchronous; duplicate returns the same reference |
| SM-OP-103 | POST `/api/v1/messages/draft` | 201 | API-237 (Q) | **202** | Asynchronous work or external effect (SE Q/X): 202 + run reference (§3.2.1.10/11) |
| SM-OP-118 | POST `/api/v1/sequences/{id}/enroll` | 201 | API-242 (X) | **202** | Asynchronous work or external effect (SE Q/X): 202 + run reference (§3.2.1.10/11) |
| SM-OP-123 | POST `/api/v1/meetings/book` | 201 | API-243 (X) | **202** | Asynchronous work or external effect (SE Q/X): 202 + run reference (§3.2.1.10/11) |
| SM-OP-125 | POST `/api/v1/admin/calendar-links` | 201 | API-110 (Q) | **202** | Asynchronous work or external effect (SE Q/X): 202 + run reference (§3.2.1.10/11) |
| SM-OP-131 | POST `/api/v1/admin/whatsapp/accounts` | 201 | API-107 (Q) | **202** | Asynchronous work or external effect (SE Q/X): 202 + run reference (§3.2.1.10/11) |
| SM-OP-137 | POST `/api/v1/public/chat` | 200 | API-246 (Q) | **202** | Asynchronous work or external effect (SE Q/X): 202 + run reference (§3.2.1.10/11) |
| SM-OP-149 | PATCH `/api/v1/content/{id}` | 201 | API-301 (W) | **200** | Synchronous state change/decision on an existing resource |
| SM-OP-154 | POST `/api/v1/admin/social/accounts` | 201 | API-113 (Q) | **202** | Asynchronous work or external effect (SE Q/X): 202 + run reference (§3.2.1.10/11) |
| SM-OP-158 | POST `/api/v1/seo/tasks` | 201 | API-289 (Q) | **202** | Asynchronous work or external effect (SE Q/X): 202 + run reference (§3.2.1.10/11) |
| SM-OP-163 | POST `/api/v1/landing-pages/{id}/publish` | 200 | API-492 (X) | **202** | Asynchronous work or external effect (SE Q/X): 202 + run reference (§3.2.1.10/11) |
| SM-OP-178 | POST `/api/v1/events/register` | 201 | API-296 (I) | **200** | Synchronous state change/decision on an existing resource |
| SM-OP-182 | POST `/api/v1/public/referrals` | 201 | API-298 (I) | **202** | Public intake: durable acknowledgement, processing asynchronous; duplicate returns the same reference |
| SM-OP-186 | POST `/api/v1/deals/{id}/proposals` | 201 | API-328 (Q) | **202** | Asynchronous work or external effect (SE Q/X): 202 + run reference (§3.2.1.10/11) |
| SM-OP-195 | POST `/api/v1/contracts` | 201 | API-332 (Q) | **202** | Asynchronous work or external effect (SE Q/X): 202 + run reference (§3.2.1.10/11) |
| SM-OP-248 | POST `/api/v1/sales/tenants` | 201 | API-027 (Q) | **202** | Asynchronous work or external effect (SE Q/X): 202 + run reference (§3.2.1.10/11) |
| SM-OP-249 | POST `/api/v1/sales/tenants/{id}/control` | 202 | API-028 (A) | **200** | Synchronous state change/decision on an existing resource |
| SM-OP-251 | POST `/api/v1/sales/startups` | 201 | API-030 (Q) | **202** | Asynchronous work or external effect (SE Q/X): 202 + run reference (§3.2.1.10/11) |
| SM-OP-293 | POST `/api/v1/commercial/admin/external-grants` | 201 | API-227 (X) | **202** | Asynchronous work or external effect (SE Q/X): 202 + run reference (§3.2.1.10/11) |
| SM-OP-296 | POST `/api/v1/commercial/portal/documents` | 201 | API-235 (Q) | **202** | Asynchronous work or external effect (SE Q/X): 202 + run reference (§3.2.1.10/11) |

### 3.5.4.8 Mapping quality checks

| Check | Result |
|---|---|
| Every source operation mapped to ≥ 1 blueprint operation, adapter or enhancement | 321 / 321 |
| Every FRD-named (★) Part 3.2 operation referenced by a source operation | 104 / 104 |
| Source operations needing a new operation | 6 Not covered + 18 Partial → 24 enhancement operations (API-ENH-D-001…024) and 3 adapters (AD-D01…D03) |
| Semantic mappings reviewed by hand | 215 (all non-exact rows: 139 alias, 44 split, 8 approval, 18 partial, 6 new; note column in CSV) |
| Mapping of approve/review routes into the Approval resource | 8 direct + 9 inside split actions; each approval type exists in Part 3.2 §3.2.2.3 |
| Bid `submit` action (SM-OP-280) | Mapped to API-367 *record human submission evidence* only; no automated submission (DEC-053) |
| Access-boundary differences | 10 found; 6 compatible as is, 4 resolved (§3.5.4.6) |
| Status-code differences | 24 resolved by rule (§3.5.4.7) |

---

## 3.5.4.9 Quality gate: Batch 3.5a

| # | Check | Result | Notes and fixes applied |
|---|---|---|---|
| 1 | Every requirement traced to a source | Pass | Every aspect row cites the document 07 section; every mapping row names SM-OP/SM-SIT and the Part 3.2 API/AD ID |
| 2 | Assumptions/gaps/conflicts tagged and logged | Pass | Tags from the allocated ranges only; register in file b §3.5.8 |
| 3 | IDs unique and consistent with earlier parts | Pass | Source IDs kept (SM-OP-###, SM-SIT-A###, SM-UX-API-##, OPT-##-##); source DEC-### renamed SRC07-DEC-### to avoid collision with DEC-001…065 (CONFLICT-364); new IDs API-ENH-D-###, AD-D##, FR-ENH-D-###, TC-ENH-D-### |
| 4 | No story lacks AC; no requirement lacks a test | Pass | File b: every FR-ENH-D has a story with Gherkin AC and TC-ENH-D tests; every source operation has a test row |
| 5 | Negative, edge, security and accessibility cases covered | Pass | Boundary, status, token-route and provider conflicts listed; negative families in file b; accessibility N/A for API contracts (UI covered in Part 2.5) |
| 6 | Agents: guardrail, fallback, KPI, cost | N/A | No agent defined here; AI operations map to Part 3.2/Part 7 |
| 7 | Time-sensitive facts flagged "verify" with as-of date | Pass | Provider facts quoted from the source carry "verify at implementation (as of 27 Nov 2026)" |
| 8 | No restricted data routed to free-tier models | Pass | No routing change; OpenAI listing rejected (CONFLICT-372) |
| 9 | Consistent with earlier parts | Pass with notes | Inconsistencies reported in file b §3.5.7.5, not fixed in other parts |

**Status: Part 3 Batch 3.5a complete. Document 07 reviewed line by line and parsed programmatically; 302 retained operations, 17 adapters and 19 candidates mapped to Part 3.2 (297 Covered, 18 Partial, 6 Not covered); non-catalogue aspects registered; enhancements continue in Batch 3.5b.**
