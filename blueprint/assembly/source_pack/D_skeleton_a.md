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

**Reading guide.** Document 07 is the catalogue that Part 3.2 could not see: Part 3.2 §3.2.2.1 records "the 302-operation catalogue itself was not supplied (GAP-103)" and promises "a mapping table (original ID → API-###) … and any original operation without a match becomes a candidate addition (DEC-015)". This batch delivers that promise. File a reviews the document, registers every aspect and maps all 302 retained operations, the 17 adapters inside them and the 19 candidate operations to Part 3.2. File b writes the missing content at full depth: 24 new operations, normalized field contracts for 247 operations, 38 contract decisions, adapter envelope and three new adapters, a 74-entry provider register, error codes, contract approval lifecycle, requirements, stories and 367 test cases.

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

<<ASPECT_COUNT_TABLE>>

---

## 3.5.2 Coverage register summary

<<SUMMARY_TABLE>>

**Interpretation.** At the *endpoint* level Part 3.2 already covers 297 of 321 source operations (92.5%), because its 555-operation catalogue was derived from all 147 screens and is a superset. The real deficit is one level down: **no source operation had a field-level request/response contract, per-operation status/error set or per-operation SIT test in the blueprint**. That deficit, plus 24 missing operations, 3 missing adapter ports, the adapter envelope, the contract-approval lifecycle and 13 conflicts, is what file b closes.

---

## 3.5.3 Detailed coverage register

### 3.5.3.1 Non-catalogue aspects (prose, controls, decisions, providers)

Every Partially covered, Not covered and Conflict item is listed individually. Common-core aspects are listed once and marked "Common core: see document 01/02 coverage".

<<ASPECTS_TABLE>>

### 3.5.3.2 Catalogue aspects (grouped; every non-Covered row is listed in §3.5.4.3 and the CSV)

| Aspect family | Count | Covered | Partially covered | Not covered | Conflict | Where listed |
|---|---|---|---|---|---|---|
<<CATALOGUE_FAMILY_ROWS>>

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

<<COUNTS_REL>>

<<COUNTS_BOUNDARY>>

<<COUNTS_KIND>>

### 3.5.4.3 Full operation mapping: source operation → blueprint operation (302 retained operations, including 17 adapters)

`~/` = `/api/v1/commercial/`. "Approval" = API-541 (submit object revision for approval) + API-539 (decide). An enhancement ID means the missing part is specified in file b §3.5.5.2 (operations) or §3.5.5.6.3 (adapters). The same table with 25 columns (purpose, module, tables, integration, allocation, request/response fields, SIT assertion) is `final/coverage/D_api_mapping.csv`.

<<FRAG:map_ops.md>>

### 3.5.4.4 Candidate operations (SM-UX-API-01…19) → blueprint

<<FRAG:map_cands.md>>

### 3.5.4.5 Reverse mapping: Part 3.2 operations with no source counterpart

These 212 operations are **retained**: they are DERIVED operations that Part 3.2 added from screen actions, BFF/session needs, portal self-service, approvals, reconciliation, Copilot, inventory, ledgers and support (§3.2.2.1 steps 3–4). None contradicts document 07; document 07 simply does not enumerate them. They receive source-style tracking IDs only through the OpenAPI `x-source-op: none` marker [RECOMMENDATION-360].

<<FRAG:reverse.md>>

### 3.5.4.6 Access-boundary differences (10 operations)

<<FRAG:ns.md>>

### 3.5.4.7 Status-code reconciliation (24 operations where the source proposal differs from the Part 3.2 side-effect rule)

Only operations with relation Exact or Alias are listed; split operations take the status of each target (file b §3.5.5.3). **Rule applied (CONFLICT-370):** Part 3.2 §3.2.1.10 is normative: work that is queued or starts an external effect returns 202 with a run reference; the source's 201/200 proposals for such operations are superseded. Public intake returns 202 because processing is asynchronous and a duplicate returns the same reference (CA-INTAKE).

<<FRAG:status.md>>

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
