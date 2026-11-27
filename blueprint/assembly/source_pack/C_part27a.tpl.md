# AI Growth Engine: Employee Sales & Marketing Automation
## Application Blueprint: PART 2 (Batch 2.7a), Source Pack UI Catalog and UX Enhancements

| Field | Value |
|---|---|
| Document | Application Blueprint · Part 2.7 (Batch 2.7a of 2; per-screen contract cards in Batch 2.7b) |
| Version | 1.0 · 27 Nov 2026 |
| Baseline | Source pack documents **06** "UI Screen, Filter, API and Table Catalog" and **17** "Unified Sales and Marketing Command Centre UI/UX and Interaction Design"; compared against Part 2.1 (FR register, field specs), Part 2.4, Part 2.5 (147 screens), Part 3.2 (API catalogue), Part 3.3 (entities), Part 6.1 (alias test mapping); binding decisions DEC-001…DEC-065 |
| Roles applied | Lead UX/UI Designer (lead), Frontend Lead, Accessibility Specialist, Business Systems Analyst (BSA); reviewed from Security and Solution Architect perspectives |
| Tag ranges used | ASSUMPTION-340…345, GAP-340…349, CONFLICT-340…351, RECOMMENDATION-340…349 |

**Acronyms used in this part.** BSA Business Systems Analyst · DTO data transfer object · ENT blueprint entity ID (Part 3.3) · IP interaction pattern · LCP/INP/CLS Largest Contentful Paint / Interaction to Next Paint / Cumulative Layout Shift · OI Optimization Intelligence · OKPI pack optimization KPI (renamed from the pack's KPI-01…35, see Source Pack brief) · PDP Policy Decision Point · RUM real-user monitoring · SR screen reader · SoD separation of duties · TC test case · UAT user acceptance test · WCAG Web Content Accessibility Guidelines.

---

## 2.7.1 Documents reviewed

### 2.7.1.1 Document 06: UI Screen, Filter, API and Table Catalog

| Attribute | Value |
|---|---|
| Size | 458,074 bytes of extracted text; 3,514 lines; 10 tables; 147 screen-decision blocks; 138 implementation-register blocks; 10 retained website capability blocks |
| What it is trying to tell | It is the **screen-to-contract register**: for every one of the 147 interfaces it names the access class, behaviour, build/reuse class, business modules, the exact legacy REST/adapter operations, the PostgreSQL tables, the plugin/provider associations with licence, quota, rate, budget line and verification status, the SM-FR / SM-UT / SM-UAT test associations, interaction checks, and the field-level "current / add / remove" decisions with automation, acceptance and related screens |
| Pattern | Common core (purpose and boundary, startups, technology principles, operating contract, implementation controls, optimization, final decision controls) + domain catalogue (Part A Website W01–W30, retained website capabilities, Part B Admin A001–A108, nine new interfaces, screen-specific decisions for all 147) |
| Atomic aspects found | {{N06}} (field decisions {{N06_FLD}}, screen operations {{N06_OP}}, tables {{N06_TAB}}, test associations {{N06_IMP}}, integration associations {{N06_PLG}}, related-screen sets 147, automation statements 147, retained capabilities 10, global and optimization aspects {{N06_G}}) |

| # | Section (heading 1/2) | Lines | Aspect family | Shared core? |
|---|---|---|---|---|
| 1 | Product purpose and operating boundary; initial startup configurations; technology and execution principles | 7–36 | Boundary, 4 startups, stack | Yes: common core, see document 01/02 coverage |
| 2 | Global filter hierarchy and contextual filters | 37–76 | 11 filter families + rules | Partly (also FRD §2) |
| 3 | Unified Command Centre: seven primary views | 77–104 | 7 views + persistent controls | Partly (also BRD §3) |
| 4 | Interface implementation register; Part A Website W01–W30; retained website capabilities 008…085 | 105–439 | 30 screen blocks, 10 capability blocks | No |
| 5 | Part B Confidential Admin A001–A108 | 440–2103 | 108 screen blocks with plugin/licence/budget rows | No |
| 6 | Website and confidential Admin operating contract; replacement options; interface acceptance and mapping | 2104–2137 | Surfaces, routing, configuration, separation | Partly |
| 7 | Implementation, verification and delivery controls (138-row table), global interaction contract, acceptance and evidence record | 2138–2743 | SM-FR / SM-UT / SM-UAT per screen | No |
| 8 | Frontend acceptance and contract gating (four-state UI matrix, engineering mapping) | 2744–2775 | UI gating | No |
| 9 | Optimization engineering and acceptance (OPT-02, OPT-09, OPT-15, OI integration points) | 2776–2823 | 16 optimization items + 7 OI integration points | Partly (doc 36 owns OPT catalogue) |
| 10 | Implementation acceptance and verification; final decision controls | 2824–2878 | 7 procedures (each stated twice) | Yes (duplicated, DEC-014 pattern) |
| 11 | Current multi-startup scope: UI catalog (9 new interfaces) and screen-specific field and automation decisions (147) | 2879–3514 | 1,733 field rows, 147 automation, 147 related, 444 screen-operation rows | No |

### 2.7.1.2 Document 17: Unified Sales and Marketing Command Centre UI/UX and Interaction Design

| Attribute | Value |
|---|---|
| Size | 186,090 bytes of extracted text; 1,621 lines; 13 tables; 147 screen-decision blocks; 138 interaction blocks |
| What it is trying to tell | It is the **interaction-design layer** of the same catalogue: the reusable shell (nine persistent regions), the website/portal/Admin layout compositions, breakpoints, interaction-state and accessibility specification, interaction rules, design handoff and release evidence, design-side optimization items (OPT-02, OPT-06-01, OPT-14-01, OPT-15, OPT-19-01) and acceptance procedures (adds public responsiveness, inbound/outbound journeys, accessibility, user productivity); per screen it adds an *Intent* line and one of three interaction patterns |
| Pattern | Same common core as document 06; per-screen field decisions are byte-identical to document 06 and document 02 (parser diff = 0, [ASSUMPTION-342]) |
| Atomic aspects found | {{N17}} (screen intents/interaction 147, field-decision sets 147 [common with 06], global design aspects {{N17_G}}) |

| # | Section | Lines | Aspect family | Shared core? |
|---|---|---|---|---|
| 1 | Purpose, startups, technology; seven views; filters | 7–104 | as doc 06 | Yes: common core / common with doc 06 |
| 2 | Interaction design and reusable shell | 105–138 | 9 persistent regions + interaction list | No |
| 3 | Screen-specific interaction index (W01–W30, capabilities, A001–A108) | 139–822 | Intent + interaction pattern per screen | No |
| 4 | Operating contract; website layout and interaction wireframe; layout compositions (public homepage, portal, Command Centre) | 823–928 | Layout regions, breakpoints, indexing | Partly |
| 5 | Replacement controls; design quality and release evidence | 929–934 | Adapter display, evidence | No |
| 6 | Interaction state and accessibility specification; design handoff; acceptance and evidence record; UI interaction rules | 935–1017 | 7 + 5 rules, handoff list | No |
| 7 | Optimization engineering (Performance, Scalability, Reusability, UI/UX, Privacy) and OI | 1018–1063 | 13 OPT items + 7 OI points | Partly |
| 8 | Acceptance procedures and final decision controls (9, duplicated) | 1064–1132 | Procedures | Yes (duplicated) |
| 9 | Current scope: UI interaction; nine new interfaces; screen-specific decisions (147) | 1133–1621 | Identical to doc 06 §11 | Common with doc 06 |

---

## 2.7.2 Coverage register summary

Statuses follow the Source Pack brief. "Not applicable" is used for shared-core text, layout-only placeholders and development-time plugins that have no runtime meaning.

{{STATUS_TABLE}}

**Headline findings.**

1. **Screens:** all 147 IDs exist in Part 2.1 and Part 2.5 with identical names (parser check 147/147). Document 06/17 field decisions equal FRD §16.2 word for word, so Part 2.1's traces remain valid.
2. **Fields:** of {{FLD_TOTAL}} field rows, {{FLD_C}} are named in the blueprint, **{{FLD_P}} retained-baseline fields were never specified** (Part 2.5 delegates field lists to Part 2.1; Part 2.1 lists only standardized/added fields). Largest gaps: {{FIELD_P_BY_VIEW}}. Closed by the 147 contract cards in Batch 2.7b [GAP-340].
3. **Operations:** document 06 names **{{OPS_DIST}} distinct legacy operations** ({{OPS_ROWS}} screen-operation rows). Only {{OPS_DC}} match a blueprint operation exactly, {{OPS_DP}} have an equivalent DERIVED operation under another path, and **{{OPS_DN}} have no equivalent** [GAP-342]. This is the first time the "retained 302" catalogue is visible at screen level (Part 3.2 GAP-103).
4. **Tables:** {{TAB_TOTAL}} source tables (152 named + 3 "existing" identity tables = the pack's 149 + 6 entities): {{TAB_C}} map by name, {{TAB_P}} by judged synonym, **{{TAB_N}} have no blueprint entity** (`sales_business_template`, `sales_ui_service_request`) [GAP-349].
5. **Tests:** the SM-UAT-S numbering rule of Part 6.1 §6.1.12.5 is confirmed mechanically (S001–S030 = W01–W30, S031–S138 = A001–A108), and the FR-count of every SM-UT alias equals Part 6.1's cluster table (001/002 = 138, 003 = 26, 004 = 22, 015 = 69, …).
6. **Integrations:** 86 distinct plugin/provider names on screens: 37 runtime adapters, 16 open-source dependencies, 8 unverified commercial services, **23 development-time plugins that doc 06 attaches to runtime screens** [CONFLICT-346], 2 internal.
7. **Navigation:** document 06 defines **435 related-screen links**; Part 2.5 shows 3 [GAP-343].
8. **Design layer (doc 17):** the shell, states and accessibility are covered; breakpoints conflict [CONFLICT-342]; status footer, focus restoration, design handoff, design evidence, Optimization Intelligence view and productivity measurement are missing or partial.

---

## 2.7.3 Detailed coverage register

The full atomic register ({{CSV_ROWS}} rows) is `final/coverage/C_coverage.csv`. This section lists every global aspect individually and groups per-screen rows; every Partial, Not covered and Conflict per-screen item is listed individually in §2.7.4 (operations, tables, integrations) or in its Batch 2.7b card (fields, related screens).

### 2.7.3.1 Global aspects: document 06

{{G06_TABLE}}

### 2.7.3.2 Global aspects: document 17

{{G17_TABLE}}

### 2.7.3.3 Per-screen aspect groups

| Aspect group | Rows | Covered | Partial | Not covered | N/A | Where the items are listed |
|---|---|---|---|---|---|---|
{{GROUP_ROWS}}

---

## 2.7.4 Catalogue reconciliation

```mermaid
flowchart TD
  A["Doc 06 and 17 text<br/>heading and table markers"] --> B["C_parse_ui_catalog.py"]
  B --> C["147 screen decisions<br/>138 screen blocks<br/>10 retained capabilities"]
  B --> D["138-row implementation<br/>table SM-FR SM-UT SM-UAT"]
  C --> E["Fields vs Part 2.1 and 2.5"]
  C --> F["Operations vs Part 3.2<br/>555 API rows"]
  C --> G["Tables vs Part 3.3<br/>199 ENT rows"]
  D --> H["Aliases vs Part 6.1<br/>cluster table"]
  C --> I["Integrations vs Part 3.1 and 3.2"]
  E --> J["C_generate_part27.py"]
  F --> J
  G --> J
  H --> J
  I --> J
  J --> K["Part 2.7b cards"]
  J --> L["C_coverage.csv"]
  J --> M["Part 2.7a tables"]
```

Scripts: `assembly/source_pack/C_parse_ui_catalog.py` (parse and reconcile) and `assembly/source_pack/C_generate_part27.py` (cards, fragments, coverage). Matching rules: fields match when ≥ 50% of the field's normalized tokens occur in the screen's Part 2.1 FR row or Part 2.5 row; operations match exactly on method + normalized path (legacy paths without `/api/v1` are prefixed), else on the same screen with the same final resource noun, else anywhere in the catalogue with the same method and resource; tables match on the name suffix after the `growth_`/`sales_` prefix, else on a judged synonym list in the script.

### 2.7.4.1 Screen identity reconciliation and legacy screen IDs

All 147 IDs and names agree between documents 02, 06, 17 and Parts 2.1/2.5. Document 06 preserves the **original 116-item numbering** ("existing NNN"): A001–A106 carry 106 of them and the ten retained website capabilities carry the other ten [ASSUMPTION-344]. A107/A108 and W01–W30 have no legacy number; W31–W34 and A109–A113 are the nine additions. The crosswalk is now part of the blueprint (FR-ENH-C-001):

{{CROSSWALK}}

**Retained website capabilities (doc 06 "Existing capability NNN") mapped to W-screens:**

{{CAPS}}

### 2.7.4.2 Operation reconciliation summary

| Measure | Count |
|---|---|
| Screen-operation rows in doc 06 (incl. retained capabilities and OI integration points) | {{OPS_ROWS}} |
| Distinct method + path pairs | {{OPS_DIST}} |
| Exact match to a blueprint operation (Covered) | {{OPS_DC}} |
| Equivalent DERIVED operation exists (Partial: alias route needed) | {{OPS_DP}} |
| No equivalent (Not covered: alias or new DERIVED operation needed) | {{OPS_DN}} |
| Of which generic `…/{id}/control` endpoints | {{OPS_CONTROL}} |
| Of which per-object `approve`/`review` endpoints | {{OPS_APPROVE}} |
| Of which `/api/v1/sales/…` or `/api/v1/commercial/workspace/…` namespace | {{OPS_NS}} |

Exactly matched operations: {{OPS_C_LIST}}.

### 2.7.4.3 Operations with no blueprint equivalent (Not covered, listed individually)

{{OPS_N}}

### 2.7.4.4 Operations with an equivalent under another path (Partial, listed individually)

{{OPS_P}}

### 2.7.4.5 Table reconciliation (155 source tables)

{{TABLES}}

### 2.7.4.6 Test-association reconciliation

| Check | Source (doc 06 implementation table) | Blueprint | Result |
|---|---|---|---|
| Rows | 138 (W01–W30, A001–A108) | Part 6.1: SM-UAT-S001…S138 one per SM-FR row | Equal |
| SM-UAT numbering | Parsed per row | S001–S030 = FR-W01…W30; S031–S138 = FR-A001…A108 | Rule holds for 138/138 rows |
| SM-UT distinct IDs | 63 (037, 049, 050 absent) | 63 (GAP-167) | Equal |
| SM-UT FR-counts | 001/002 = 138; 003 = 26; 004 = 22; 005/006 = 10; 007 = 17; 008/009 = 19; 010–012 = 26; 013 = 44; 014 = 19; 015 = 69; 016–019, 047 = 15; 020–022 = 14; 023 = 23; 024 = 41 … | Part 6.1 cluster table | Equal for every listed cluster |
| SM-UX-UAT-<screen> | 147 | Part 2.1 / Part 6.1, 147 | Equal |
| SM-UX-FR-<screen> | 147 | Aliased by scheme in Part 2.1 §2.4 ("SM-UX-FR-… for field specs") | Covered by scheme; each card now names its alias |
| Interaction checks column | 138 texts (5 check templates by surface/domain) | CA-PUB, CA-PORTAL, CA-ADMIN, CA-FIN, CA-DISPATCH | Covered |

### 2.7.4.7 Integration associations on screens

Classes: **INT** internal; **OSS** open-source runtime or test dependency (B01 shared); **ADP** provider adapter behind a feature flag (Part 3.2 §3.2.4); **CMU** commercial, unverified, ₹0 committed until procurement approval; **DEV** development-time plugin, no runtime entitlement. Every price, quota and licence statement in document 06 (for example per-million-token model rates, per-credit search rates and hosted-plan fees) is time-sensitive: **verify at time of implementation (as of 27 Nov 2026)** [CONFLICT-347]. Counts by class: {{PLUG_COUNTS}}.

{{PLUGINS}}

### 2.7.4.8 Related-screen graph

Document 06 lists 435 directed "Related" links across 147 screens (mean 3.0 per screen). Most-referenced targets: {{REL_TOP}}. Every link is reproduced in its Batch 2.7b card and becomes an in-context navigation requirement (FR-ENH-C-012).

### 2.7.4.9 Location class versus navigation home

Document 06 tags Admin screens "Admin", "Workspace" or "Existing". Cross-tabulated with Part 2.5 navigation homes: {{LOC_VIEW}}. The tag does not align with the seven views (for example "Admin" screens sit in all seven), so it is read as a **permission/workspace class** (configuration and approval screens restricted to administrative roles) and not as a navigation instruction; Part 2.5 navigation stands [ASSUMPTION-340].

---

## 2.7.5 Enhancements

Organized by blueprint part. Every item is additive; no earlier part is edited.

### 2.7.5.1 Part 2.1 additions: functional requirements

| FR | Requirement | Source | Profiles | Wave · Epic | Tests |
|---|---|---|---|---|---|
| FR-ENH-C-001 | **Legacy screen identity.** Every screen record (route manifest, telemetry, test evidence, RTM) carries its legacy number from §2.7.4.1 where one exists; the ten retained website capabilities are tracked as sub-features of their W-screens. Legacy numbers are labels, never routes | Doc 06 Part A/B headings; §"Interface implementation register" | CA-ALL | W0 · EP-01 | TC-ENH-C-001 |
| FR-ENH-C-002 | **Per-screen field contracts are binding.** Each screen implements exactly the fields of its Batch 2.7b card: label, origin, type, control, validation, editability. Computed, lifecycle-derived and read-only fields are rejected on write by the serializer (400 `FIELD_READ_ONLY`). Replace rules ("Status: controlled transition", "Password and MFA code: never persist", "Email: derive verified identity where possible") are enforced server-side | Doc 06/17 "Screen-specific field and automation decisions"; FRD §16.2 | CA-ALL, CA-CONFIG | Per screen wave | TC-ENH-C-002, TC-ENH-C-101…247 |
| FR-ENH-C-003 | **Legacy operation aliases.** Every operation in §2.7.4.3/§2.7.4.4 is reachable at its legacy method/path as an alias of the canonical blueprint operation (same view, serializer, permission class, rate-limit class and audit), so that retained integrations keep working (BRD §9 "retain canonical legacy method/path contracts"). Aliases return `Deprecation` and `Link: <canonical>; rel="successor-version"` headers. Generic `/control` aliases accept `{"action": …}` and dispatch only to actions valid for the current state (CONFLICT-344). Per-object `approve`/`review` aliases create and decide the same Approval record (CONFLICT-345) | Doc 06 operating contract "Routing decision"; Part 3.2 §3.2.2 | CA-ALL, CA-ADMIN | W0 framework; per module wave | TC-ENH-C-003, TC-ENH-C-004 |
| FR-ENH-C-004 | **Optimization Intelligence (OI) contextual panel** in A089, A009, A012, A014, A084, A042 and A082 (no new route, no new table count): filters tenant, startup, time window, workflow and provider (only when authorized); shows measured value, target, measurement period, denominator and evidence link; shows **Unassessed** when no denominator or evidence exists; labels stale metrics; displays measured vs proposed targets, never a fictitious score; no public/portal access; no secrets, private payloads or other tenants | Doc 06 "Optimization Intelligence"; doc 17 "Optimization view is Admin-only" | CA-ALL, CA-ADMIN | W2 (panel) · EP-17 | TC-ENH-C-005, TC-ENH-C-006 |
| FR-ENH-C-005 | **Responsive and viewport test matrix.** Every screen is verified at 360, 768, 1280 and 1440 CSS px (plus 320 px reflow for public/portal); breakpoint tiers of Part 2.5 §2.48 remain, with doc 17's mobile/tablet/desktop vocabulary mapped as in CONFLICT-342 | Doc 17 "Responsive shell", "Accessibility" | CA-ALL | W0 · EP-17 | TC-ENH-C-007 |
| FR-ENH-C-006 | **Interaction patterns.** Every screen implements one of three interaction patterns (§2.7.5.2): IP-PUB, IP-PORTAL or IP-ADMIN; the pattern's checklist is part of the screen's definition of done | Doc 17 screen interaction index | CA-ALL | W0 · EP-17 | TC-ENH-C-008 |
| FR-ENH-C-007 | **Status footer.** The Admin status bar (Part 2.5 §2.41) additionally shows last refresh time, degraded-provider indicator (per adapter in scope), pending job count with link to A009, and support entry; public/portal footers show contact, privacy, accessibility and support | Doc 17 "Footer/status"; Website layout wireframe | CA-ADMIN, CA-PUB | W2 · EP-17 | TC-ENH-C-009 |
| FR-ENH-C-008 | **Filter toolbar and focus behaviour.** Filter toolbar shows result count and as_of next to Apply; after a drawer, dialog or route return closes, focus returns to the invoking control (focus restoration); after scope switch, focus moves to the page heading and an SR announcement states the new scope | Doc 17 shell table and interaction list | CA-ADMIN | W0 · EP-17 | TC-ENH-C-010 |
| FR-ENH-C-009 | **Adapter and plugin display.** A008, A011, A012, workflow simulation (A033/A102), approval and exception panels show for each capability: selected adapter, licence status, entitlement, free/self-host capacity, residual external cost (estimate), capability limits, benchmark result, fallback approval state, disabled state, retry and exception details. A "free" or "verified" badge appears only when evidence exists; incomplete free coverage shows a human-readable warning. DEV-class plugins never appear as runtime options. Public and portal pages never show provider keys, internal budgets or debug logs | Doc 06 "Interface behavior for replacement options"; doc 17 "Replacement controls" | CA-ADMIN, CA-CONFIG | W0 · EP-04 | TC-ENH-C-011 |
| FR-ENH-C-010 | **Design handoff record** per screen: component names, breakpoint behaviour, loading/empty/error/denied/success states, filter types, accessible labels, role and mutation permission, exact API operations and visible fields (all available from the Batch 2.7b card). HTML prototypes and browser simulations are labelled "simulation" and never authenticate production users | Doc 17 "Design handoff"; "UI interaction" | CA-ALL | W0 · EP-17 | TC-ENH-C-012 |
| FR-ENH-C-011 | **Design and delivery evidence pack.** For each wave, role-based screenshots per screen (one per permitted role and one denied), recorded user walkthroughs for top journeys, network-payload evidence that the Website bundle calls no Admin API, build digest and reviewer; stored as EVR evidence (Part 6.1). Missing evidence = Pending | Doc 06 "Engineering mapping"; doc 17 "Design quality and release evidence" | CA-ALL | Every wave · EP-21 | TC-ENH-C-013 |
| FR-ENH-C-012 | **Related-screen navigation.** Each card's related screens are reachable from a "Related" menu or contextual link that carries the current tenant/startup scope and the selected record ID where the target accepts it; the target re-authorizes and shows a denied state if the record is outside the user's grant | Doc 06 "Related" lists | CA-ADMIN, CA-PORTAL | W2 · EP-17 | TC-ENH-C-014 |
| FR-ENH-C-013 | **Browser-callable allowlist for the Website.** The Website bundle may call only operations classified public or portal in §2.7.4 and Part 3.2; legacy token routes under `/api/v1/public/…/{token}` are restricted portal endpoints (signed, expiring, single-object); provider callbacks and adapters are server-only; Admin operations listed against retained capabilities (for example `POST /api/v1/invoices/{id}/payment-link`) are Admin-only (CONFLICT-350) | Doc 06 retained capabilities; operating contract | CA-PUB, CA-PORTAL | W2 · EP-19 | TC-ENH-C-015 |
| FR-ENH-C-014 | **Build class.** Each screen carries doc 06's build class (Reuse 2, New shell 1, New 72, New growth-specific view 1, Extension 22, Contextual panel 8, template-configured Website 34 + new Admin 7) for estimation and test depth: Reuse/Extension screens require regression of the reused component plus contract tests; New screens require full component, contract, E2E and accessibility tests | Doc 06 Build/reuse rows | — | W0 planning · EP-21 | TC-ENH-C-016 |
| FR-ENH-C-015 | **Filter performance behaviours.** Debounce free-text search (250–300 ms); cancel stale requests with AbortController; latest filter wins; virtualize lists above 200 rows; query cache keyed by product, tenant, startup, permission revision and filters; no scope flash on startup switch | OPT-02-02, OPT-02-04 | CA-ADMIN | W0 · EP-17 | TC-ENH-C-017 |
| FR-ENH-C-016 | **Productivity measurement.** For each core scenario (Part 4.2 NFR-090) record baseline and candidate task time, click count and error rate with a named representative user; approval safeguards may not be reduced to improve time | Doc 17 "User productivity" | — | W2, W5 · EP-17 | TC-ENH-C-018 |
| FR-ENH-C-017 | **Dashboard latency acceptance.** Identical scoped workload at 50 and 250 concurrent staff over 100,000 and 1,000,000 opportunities: dashboard first render p95 ≤ 2.0 s (initial scale) and ≤ 2.5 s (growth scale) with correct results and zero isolation failures; per-call targets of NFR-039/NFR-044 continue to apply | Doc 06/17 "Dashboard latency" | CA-ADMIN | W2, W5 · EP-21 | TC-ENH-C-019 |

### 2.7.5.2 Part 2.5 additions: interaction patterns, shell and states

**Interaction patterns** (one per screen, from doc 17; assignment in each Batch 2.7b card):

| Pattern | Screens | Mandatory behaviour checklist (each item is a test step in TC-ENH-C-008) |
|---|---|---|
| **IP-PUB** Public content and intake | W01–W20, W30 and W31–W33 public/applicant steps | Responsive public header and breadcrumb; one clear primary action; mobile stacked form; visible labels; error summary at top linked to fields (focus moves to summary on submit); published content only; consent notice visible before submit; safe enquiry confirmation with opaque reference |
| **IP-PORTAL** Identity-bound portal | W21–W29, W34 | Responsive header and breadcrumb; identity-bound navigation (own records only); status chips with text; secure document actions (view, download, sign, upload with scan state); expired/revoked grant shows recovery invitation path |
| **IP-ADMIN** Scoped Command Centre | A001–A113 | Current permitted scope visible; relevant typed filters; exact result status; scoped detail drawer; preview and confirm consequential actions (affected records, excluded count, business effect, cost, approval); approval, pending, failed and actual outcome states; no success shown on mere queue acceptance |

**Shell additions** (doc 17 "Interaction design and reusable shell" compared with Part 2.5 §2.41):

| Region | Doc 17 | Part 2.5 | Addition |
|---|---|---|---|
| Header | Product identity, tenant, startup, role, scope indicator, user, notification | Scope selector, search, bell, Copilot, avatar | Show **role** chip next to scope (FR-ENH-C-007) |
| Filter toolbar | Global hierarchy, typed filters, clear/apply/save, **result count**, as_of | Saved view, chips, add filter, reset | Result count + as_of (FR-ENH-C-008) |
| Action centre | Mark read only affects own notification | A106 own notifications | Covered (FR-A106) |
| Copilot | Read/draft/propose; exact scope, evidence, confirmation before live effect | Drafts only (DEC-035) | Consistent: "propose" = draft only; no live effect from Copilot |
| Footer/status | Last refresh, degraded provider, pending job, support | Automation status, budget, STOP | FR-ENH-C-007 |

**New UI state** (adds to Part 2.5 §2.47) [RECOMMENDATION-344]:

| State | Trigger | Visual | Copy pattern | Actions |
|---|---|---|---|---|
| Unassessed | Metric has no denominator or no evidence for the period | Grey outline, "UNASSESSED" label, no number | "Not assessed: no measured data for 1–30 Nov." | View measurement plan |

### 2.7.5.3 Part 3.2 additions: legacy operation alias layer

```mermaid
sequenceDiagram
  participant C as "Client or integration"
  participant R as "Alias router"
  participant V as "Canonical view (API-###)"
  participant P as "Permission and PDP"
  participant A as "Audit"
  C->>R: "Legacy method and path"
  R->>R: "Resolve alias table entry"
  R->>V: "Forward with canonical operation ID"
  V->>P: "Scope, role, state and policy checks"
  P-->>V: "Allow or deny with rule ID"
  V->>A: "Audit with canonical and legacy IDs"
  V-->>C: "Response plus Deprecation and Link headers"
```

| Rule | Specification [RECOMMENDATION-340] |
|---|---|
| Alias table | One row per legacy operation: legacy method, legacy path, canonical API-###, surface (public/portal/admin/internal), action discriminator (for `/control`), sunset date (none until the retained integrations are inventoried) |
| Handler | Aliases never have their own code path; they resolve to the canonical view and serializer so authorization and validation cannot diverge |
| `/control` mapping | Body `{"action": "approve" | "issue" | "cancel" | "suspend" | "activate" | "pause" | "resume" | "stop" | "retire" | "publish" | "rollback" …}`; allowed set per resource state from Part 2.3; any other value → 409 `INVALID_TRANSITION` |
| `approve`/`review` mapping | Creates the Approval (if absent) for the current object revision and decides it through `POST /api/v1/admin/approvals/{id}/decide`; SoD and hash binding apply (CA-APPROVE) |
| Namespaces | `/api/v1/sales/*` and `/api/v1/commercial/workspace/*` are admitted to the Admin ingress only; `/api/v1/commercial/workspace/public/*` and `/client/*` to the Website ingress with public or portal serializers respectively |
| Website ingress | Only aliases whose canonical operation is public or portal; everything else denied by default (doc 06 routing decision) |
| Contract tests | Each alias has a contract test proving identical status codes and response schema to its canonical operation (TC-ENH-C-003) |
| Ownership | Group D (document 07) owns the final operation IDs; this batch supplies screen-level evidence; any conflict is resolved in favour of document 07's operation catalogue mapping |

### 2.7.5.4 Part 3.3 additions: entity gaps

| Source table | Screen(s) | Proposal | Tag |
|---|---|---|---|
| `sales_business_template` | A100 | Add **BusinessTemplate** (versioned, scope X: platform default or tenant): `template_id`, `name`, `industry_taxonomy_ref`, `capability_set`, `field_schema` (JSON Schema), `objective_templates`, `workflow_bindings`, `locale`, `fallback_locale`, `theme_revision_ref`, `status` (draft, validated, approved, retired), `approved_hash`, `revision`. Until added, A100 stores templates as `aut_config_revision` rows with `config_kind = 'business_template'` | GAP-349 |
| `sales_ui_service_request` | W34 (and W28 support cases) | Add **ServiceRequest** (scope T): `request_type` (plan_change, support, export, renewal), `subject`, `body`, `severity`, `sla_due_at`, `status`, `requester_user_id`, `assigned_to`, `linked_object` (polymorphic), `revision`. Part 3.2 already exposes support cases (API-440, API-442) without an entity: inconsistency reported | GAP-349 |
| `sales_data_transfer` | A103 | Keep the blueprint split `saas_import_job` / `saas_export_job`; expose a read-only union view `v_data_transfer` for the legacy list alias | CONFLICT-351 |
| `sales_ui_trigger_revision`, `sales_ui_template_revision` | A109, A113 | Map to `aut_trigger` and `aut_workflow_template`, both versioned (Imm. V); the source "revision" tables are the version rows of these entities | CONFLICT-351 |

### 2.7.5.5 Part 4.2 additions: performance and responsiveness acceptance

| Item | Specification | Basis |
|---|---|---|
| Dashboard latency scenario LT-ENH-C-01 | Workload: identical scoped dashboard mix (A089, A042, A043, A082, A087) at 50 then 250 concurrent staff; data 100,000 then 1,000,000 opportunities across 2 tenants; report p95, throughput, errors, isolation failures | FR-ENH-C-017; CONFLICT-349 (250 staff is a stress level above the DEC-031 Year 2 design point) |
| Public responsiveness | RUM p75 LCP ≤ 2.5 s, INP ≤ 200 ms, CLS ≤ 0.1 (NFR-042); lab results labelled "lab proxy" with device, network and cache condition | Doc 17 procedure |
| Projection freshness tiers [RECOMMENDATION-348] | Tier O (operational, p95 ≤ 60 s): A032 Customer 360, A029 board, A106 action centre, A110 live monitor, A089 exception tiles. Tier A (analytical, ≤ 15 min, NFR-047): A042, A043, A082, A087 and reports | CONFLICT-348 |

### 2.7.5.6 Part 6 additions: test cases

| TC | Title | Type | Priority | Steps and expected result | Links |
|---|---|---|---|---|---|
| TC-ENH-C-001 | Legacy screen ID present in route manifest and evidence | Unit/static | P2 | Generate route manifest; every screen with a legacy number in §2.7.4.1 carries it; no legacy number is a route | FR-ENH-C-001 |
| TC-ENH-C-002 | Read-only field rejection | API | P0 | For each card field marked computed/read-only/lifecycle-derived, PATCH with a changed value → 400 `FIELD_READ_ONLY`; record unchanged; audit shows rejected attempt | FR-ENH-C-002 |
| TC-ENH-C-003 | Alias parity | Contract | P0 | For every alias row, call legacy and canonical paths with identical inputs under 4 roles × 2 tenants; status codes and response schemas identical; `Deprecation` header present on alias | FR-ENH-C-003 |
| TC-ENH-C-004 | `/control` invalid action | API negative | P1 | POST `/api/v1/sales/orders/{id}/control` `{"action":"complete"}` on a Draft order → 409 `INVALID_TRANSITION`; no state change | FR-ENH-C-003; CONFLICT-344 |
| TC-ENH-C-005 | OI panel Unassessed | E2E | P1 | Metric with zero denominator in period → "Unassessed" state, no number; stale metric shows amber as-of | FR-ENH-C-004 |
| TC-ENH-C-006 | OI panel isolation | Security | P0 | User in tenant T1 filters provider X; panel never shows T2 data, payloads or secrets; portal user receives 404 for panel endpoints | FR-ENH-C-004 |
| TC-ENH-C-007 | Viewport matrix | Visual/a11y | P1 | Each screen at 360/768/1280/1440 (+320 reflow public/portal): no horizontal page scroll except data tables in their container; no clipped action; drawer preserves filters | FR-ENH-C-005 |
| TC-ENH-C-008 | Interaction pattern checklist | E2E | P1 | Run IP checklist for the screen's pattern; every item passes | FR-ENH-C-006 |
| TC-ENH-C-009 | Status footer | E2E | P2 | Simulate adapter degradation → degraded indicator within 60 s; pending jobs count links to A009 | FR-ENH-C-007 |
| TC-ENH-C-010 | Focus restoration | A11y | P1 | Open drawer from row 7, close → focus on row 7 action; switch scope → focus on H1 and live-region announcement | FR-ENH-C-008 |
| TC-ENH-C-011 | No misleading "free" badge | E2E | P1 | Adapter with partial free coverage → warning text; no "free" badge; DEV-class plugin absent from adapter selectors | FR-ENH-C-009; CONFLICT-346 |
| TC-ENH-C-012 | Handoff record completeness | Static | P2 | Every screen's handoff record contains all ten fields; prototype pages carry "simulation" banner | FR-ENH-C-010 |
| TC-ENH-C-013 | Evidence pack per wave | Process | P1 | For the wave's screens, screenshots per role + denied, walkthrough recordings, network evidence, build digest present; missing → Pending | FR-ENH-C-011 |
| TC-ENH-C-014 | Related link scope carry | E2E | P1 | From A029 deal open related A065 → same startup scope; record outside grant → denied state, no data | FR-ENH-C-012 |
| TC-ENH-C-015 | Website allowlist | Security | P0 | Website bundle and runtime calls compared with allowlist; zero Admin operations; token routes reject expired/altered tokens | FR-ENH-C-013 |
| TC-ENH-C-016 | Build-class test depth | Process | P2 | Test plan for each screen matches its build class | FR-ENH-C-014 |
| TC-ENH-C-017 | Latest filter wins | Component | P1 | Type three filter changes within 500 ms with delayed responses; only last result rendered; no prior-scope flash | FR-ENH-C-015 |
| TC-ENH-C-018 | Productivity record | UAT | P2 | Task time, clicks and errors recorded for baseline and candidate; approval steps unchanged | FR-ENH-C-016 |
| TC-ENH-C-019 | Dashboard latency | Performance | P1 | LT-ENH-C-01 meets p95 ≤ 2.0 s / ≤ 2.5 s; 0 isolation failures | FR-ENH-C-017 |
| TC-ENH-C-020 | Residual investor wording | Static/negative | P0 | Scan UI strings, routes, filters, help text: no "investor", "issuer", "fundraising", "capital" term (extends DEC-002 regression test) | CONFLICT-340; FR-NEG-01 |

### 2.7.5.7 Part 5 additions: user stories

```gherkin
Feature: US-17-EC01 Optimization Intelligence panel
  As a Platform Owner (P01, R01) I want measured optimization metrics inside existing Admin screens
  so that I can see real effect versus target without a new screen.

  Scenario: Metric shown with evidence
    Given startup MedMaarg is in scope and metric OKPI-07 has 240 measured events in November
    When I open the OI panel in A089
    Then the panel shows the measured value, target, period 1-30 Nov, denominator 240 and an evidence link

  Scenario: No denominator
    Given metric OKPI-12 has no events in the period
    When I open the OI panel
    Then it shows "Unassessed" and no number

  Scenario: Portfolio scope is read-only
    Given scope is "All startups"
    Then the OI panel shows aggregates with the Portfolio read-only badge and no edit controls
```

```gherkin
Feature: US-01-EC01 Legacy operation aliases
  As the service identity of a retained integration (P16, R19) I want legacy paths to keep working so that retained integrations do not break.

  Scenario: Alias behaves like the canonical operation
    Given a tenant admin token for tenant T1
    When I call GET /api/v1/sales/orders
    Then the response equals GET /api/v1/commercial/admin/orders for the same scope
    And the response carries a Deprecation header and a successor link

  Scenario: Control action not valid for state
    Given order O-1 is Draft
    When I POST /api/v1/sales/orders/O-1/control with action "complete"
    Then I receive 409 INVALID_TRANSITION and O-1 stays Draft
```

```gherkin
Feature: US-17-EC02 Related screens keep scope
  As a growth manager (P03, R03) I want to jump from a deal to its proposal and payment screens
  so that I do not re-select scope and filters.

  Scenario: Navigate to related screen
    Given I am on A029 in scope AppNAI with deal D-9 selected
    When I choose Related > Proposal builder
    Then A065 opens in scope AppNAI with deal D-9 preselected

  Scenario: Related record outside grant
    Given deal D-10 belongs to startup EduVerse where I have no role
    When I follow a related link for D-10
    Then I see the denied state and no EduVerse data
```

```gherkin
Feature: US-17-EC03 Status footer and focus
  As a growth manager (P03, R03) I want to see data freshness, provider health and pending jobs
  so that I know whether what I see is current.

  Scenario: Degraded provider
    Given the email adapter for OrganicSpec is degraded
    When I view any Admin page in scope OrganicSpec
    Then the footer shows "Email provider degraded" with a link to A014 within 60 seconds

  Scenario: Focus returns after drawer
    Given I opened the detail drawer from row 7 of A016
    When I close the drawer with Escape
    Then keyboard focus returns to the row 7 "Open" control
```

```gherkin
Feature: US-04-EC01 Honest adapter display
  As an automation lead (P10, R11) I want each adapter's licence, capacity and residual cost shown truthfully
  so that nobody assumes a paid service is free.

  Scenario: Partial free coverage
    Given the search adapter has a free quota that covers 60 percent of the planned volume
    When I open A008
    Then the adapter card shows "Free quota covers about 60% of planned volume; residual cost estimated" and no "Free" badge

  Scenario: Development-only plugin
    Given "Skill Creator" is a development-time plugin
    Then it is absent from every runtime adapter selector
```

```gherkin
Feature: US-19-EC01 Website calls only allowlisted operations
  As legal/compliance (P09, R10) I want the Website to call only public and portal operations.

  Scenario: Admin operation blocked at the Website ingress
    Given the Website origin
    When a browser request is made to POST /api/v1/invoices/I-1/payment-link
    Then the Website ingress returns 404 and no handler runs

  Scenario: Expired token route
    Given an onboarding token expired yesterday
    When the portal page calls GET /api/v1/public/onboarding/{token}
    Then the expired-grant state is shown with a request-new-link action
```

```gherkin
Feature: US-21-EC01 Design evidence per wave
  As the founder approving releases (P01, R01) I want screenshots, walkthroughs and network evidence per screen
  so that release acceptance is evidence-based.

  Scenario: Missing evidence keeps the gate pending
    Given screen A105 lacks the denied-role screenshot
    When the wave gate is evaluated in A090
    Then the A105 evidence item shows Pending and the gate cannot pass
```

```gherkin
Feature: US-17-EC04 Responsive and accessible shell
  As a startup head (P02, R02) using a tablet I want approval screens usable at 768 px.

  Scenario: Approval at 768 px
    Given I open A068 at 768 px width
    Then the queue and item panes stack, all actions are reachable by keyboard and touch targets are at least 24 by 24 px
```

### 2.7.5.8 Part 8 / Part 9 notes

| Item | Note |
|---|---|
| Estimation (Part 8.1) | Build classes (FR-ENH-C-014) allow screen-level effort weighting: Reuse ≈ 0.25×, Extension ≈ 0.5×, Contextual panel ≈ 0.6×, New ≈ 1.0×, New shell ≈ 1.5× of a standard screen; to be calibrated in W0 [RECOMMENDATION-349]. Does not change the 287–483 person-day range (DEC-012) |
| Glossary (Part 9.2) | Add: Legacy screen ID; Alias route; Interaction pattern (IP-PUB/IP-PORTAL/IP-ADMIN); Unassessed; Build class; Field origin (B/A/R) |

---

## 2.7.6 Conflicts and proposed resolutions

| Tag | Conflict | Sources | Proposed resolution (for coordinator decision) |
|---|---|---|---|
| CONFLICT-340 | Residual investor wording not in DEC-002's replacement list: "separate from investor/customer journey" (W31), "not a marketplace investor or customer" (W32), "separately from investor/customer portal", "no … investor/customer records" (W34), "Authorized investor/customer completes synthetic enquiry" (OPT-15-03), "create scoped lead/investor record" (doc 17 inbound journeys), "no stale previous issuer/company data" (doc 17 startup switch) | Doc 06 §UI catalog, OPT-15-03; doc 17 §UI interaction rules, acceptance procedures | Extend DEC-002: "investor/customer journey/portal" → "customer journey/portal"; "marketplace investor or customer" → "marketplace customer"; "investor/customer records" → "customer records"; "investor/customer" (OPT-15-03) → "customer"; "lead/investor record" → "lead record"; "issuer/company" → "company". Add these strings to the DEC-002 negative regression test (TC-ENH-C-020) |
| CONFLICT-341 | "Inspect … two products, four frontends" vs DEC-009 "two frontends only" | Doc 06/17 "Independent products and frontends" | The sentence counts the two-product estate (this product + the separate investor application, DEC-058), each with two frontends. For this product the acceptance check is: two frontends, separate credentials and data; the investor application's two frontends are out of scope and must share no confidential runtime dependency |
| CONFLICT-342 | Breakpoints: doc 17 desktop ≥ 1200, tablet 768–1199, mobile < 768, tests at 360/768/1440; Part 2.5 §2.48 five tiers (360–599, 600–899, 900–1279, 1280–1679, ≥ 1680); DEC-043 Admin desktop-first 1280 px, usable to 768 px for review/approval | Doc 17 §Website layout and interaction wireframe; Part 2.5 §2.48; DEC-043 | Keep Part 2.5 tiers (finer control). Map doc 17 terms: mobile = XS+SM (< 768 effective for Admin), tablet = 768–1279 (Admin "review and approval usable", DEC-043), desktop = ≥ 1280. Adopt the test matrix 360/768/1280/1440 (+320 reflow) [RECOMMENDATION-342]. Admin below 768 px stays "not targeted" except DEC-043's approval, notification, inbox reply and meeting outcome screens |
| CONFLICT-343 | API namespaces: doc 06 uses `/api/v1/sales/*` (A099–A106) and `/api/v1/commercial/workspace/{public,client,onboarding,admin}/*` (W31–W34, A109–A113); Part 3.2 uses `~/admin/*`, `~/portal/*`, `~/public/*` | Doc 06 Part B, §Current scope; Part 3.2 §3.2.2 | Blueprint namespaces stay canonical (one ingress model, NFR-001); source paths become aliases (FR-ENH-C-003). Final IDs per Group D (document 07) |
| CONFLICT-344 | Generic `POST …/{id}/control` (12 resources) vs per-action endpoints in Part 3.2 (approve, issue, cancel, suspend, pause, resume, publish, rollback …) | Doc 06 A099–A113 | Per-action endpoints canonical (clear authorization per action); `/control` alias with validated `action` discriminator (§2.7.5.3) |
| CONFLICT-345 | Legacy per-object approve/review routes (e.g. `/contracts/{id}/approve`, `/proposals/{id}/review`, `/messages/drafts/{id}/review`, `/insurance/pilots/{id}/approve`) vs Part 3.2's single Approval resource with only four retained aliases | Doc 06 A006, A034–A035, A066, A070, A072, A092, A094, A096; Part 3.2 §3.2.2.3 | Keep the single Approval resource; add the remaining legacy approve/review routes as aliases that create/decide the Approval for the current revision |
| CONFLICT-346 | Development-time Claude plugins (for example CLAUDE.md Management, Claude Code Setup, Plugin Developer Toolkit, Skill Creator, Figma, Postman, document skills) are listed as integrations of runtime screens (A006, A008, A011, A014, A017, A029–A039, A047, A050–A059, A065–A066, A084, A090), while the same document states "developer plugins are not runtime entitlements" | Doc 06 Part B integration rows; doc 06 §Technology and execution principles | Treat DEV-class associations as development aids for building that screen only. No runtime adapter, entitlement, budget line or UI control is created for them; budget B09 (developer seats) only |
| CONFLICT-347 | Doc 06 states provider prices as facts (for example a per-million-token rate for a named Claude model, per-credit search pricing, hosted plan fees) | Doc 06 Part B "Production rate" rows; DEC-042 | DEC-042 applies: all such rates are unverified; verify at time of implementation (as of 27 Nov 2026). The UI shows cost as "estimate (rate card revision N)" and never as a confirmed price |
| CONFLICT-348 | OPT-02-04 "read projections refresh ≤ 60 s" vs NFR-047 dashboards ≤ 15 min (A110 monitor ≤ 5 min) | Doc 06/17 OPT-02-04; Part 4.2 NFR-047, NFR-008 | Two tiers [RECOMMENDATION-348]: operational projections (A032, A029, A106, A110, A089 exception tiles) p95 ≤ 60 s; analytical dashboards stay ≤ 15 min with as-of label. Cost impact: event-driven projection updates for tier O only |
| CONFLICT-349 | Scale figures: OPT-06-01 "25 owned + 10 external initial; 50+ owned + 100 external growth"; dashboard procedure "50/250 concurrent staff, 100k/1m opportunities" vs DEC-031 (Year 1: 25–40 workspaces, 2–10 tenants, 15–60 users; Year 2: 100 workspaces, 30 tenants, 200 internal users) | Doc 17 OPT-06-01; doc 06/17 dashboard latency; DEC-031 | DEC-031 remains the capacity design point. 100 external tenants and 250 concurrent staff are **stress-validation levels** for load tests (LT-ENH-C-01), not sizing commitments; infrastructure cost estimates are not changed |
| CONFLICT-350 | Retained capability 082 (website) lists `POST /api/v1/invoices/{id}/payment-link`, an Admin operation, among its operations | Doc 06 retained capability 082 | Website calls only `GET /api/v1/public/payment-status/{token}`; payment-link creation is Admin-only (A073) under CA-FIN and DEC-022 (FR-ENH-C-013) |
| CONFLICT-351 | Source single table `sales_data_transfer` vs blueprint `saas_import_job` + `saas_export_job`; source `sales_ui_trigger_revision` / `sales_ui_template_revision` vs blueprint versioned `aut_trigger` / `aut_workflow_template` | Doc 06 A103, A109, A113; Part 3.3 | Keep blueprint entities; legacy names become read views/aliases (§2.7.5.4) |

---

## 2.7.7 Expert persona review

| Persona | How the perspective was applied | What the persona would still flag |
|---|---|---|
| Lead UX/UI Designer | Reconciled all 147 screens; turned doc 06 field decisions into typed field contracts; mapped doc 17 interaction text to three testable patterns; added status footer, result count, Unassessed state and related-screen navigation | Field types are inferred from names (ASSUMPTION-341); a design review per epic must confirm control choices, especially multi-value fields (for example "Offerings", "Business units") and conditional fields on W15–W17 |
| Frontend Lead | Specified alias-independent frontend (canonical operations only), filter performance (debounce, abort, latest-wins, virtualization), viewport matrix, build classes for planning | Alias layer must not leak into the frontend; generate typed clients from canonical OpenAPI only. 435 related links need a route-parameter convention agreed in W0 |
| Accessibility Specialist | Added focus restoration, scope-switch announcement, error-summary focus, 320 px reflow, touch target checks at 768 px, Unassessed state with text (not colour) | Data-dense Admin tables at 768 px need a manual SR audit per wave; charts in the OI panel need table alternatives (DV-1) |
| Business Systems Analyst | Parsed every row programmatically; produced crosswalks (legacy IDs, capabilities, operations, tables, tests); logged 278 unspecified baseline fields, 83 unmapped operations and 2 missing entities | Final operation IDs depend on Group D; entity additions depend on Group E (document 08). The 83 Not-covered operations need an owner decision whether each becomes an alias or a new DERIVED operation |
| Security (review) | Website allowlist and token-route classification; DEV plugins excluded from runtime; alias layer shares canonical permission classes | Alias routes increase attack surface; contract tests and route inventory must be part of every BOLA/BFLA suite (NFR-002) |
| Solution Architect (review) | Namespaces kept canonical; `/control` mapped to state-validated actions; projection freshness tiers | Tier O projections add event-driven load; confirm against NFR-045 dispatch budget |

---

## 2.7.8 Tags register

| Tag | Type | Statement | Section |
|---|---|---|---|
| ASSUMPTION-340 | Assumption | Doc 06 "Admin role / location" (Admin, Workspace, Existing) is a permission/workspace class, not a navigation home; Part 2.5 navigation stands | §2.7.4.9 |
| ASSUMPTION-341 | Assumption | Field type, control and validation in Batch 2.7b are inferred by rule set R-FLD from field names; the Part 3.3 data dictionary prevails on conflict | 2.7b §2.7.10 |
| ASSUMPTION-342 | Assumption | Doc 06 and doc 17 field decisions are identical to FRD §16.2 (parser diff = 0), so Part 2.1 traces apply to all three documents | §2.7.1 |
| ASSUMPTION-343 | Assumption | Filter-family applicability per screen follows the screen's Command Centre view; vertical families appear only when enabled by the capability profile | 2.7b cards |
| ASSUMPTION-344 | Assumption | "Existing NNN" is the original 116-item numbering: A001–A106 hold 106 numbers and the ten retained website capabilities hold the other ten | §2.7.4.1 |
| ASSUMPTION-345 | Assumption | Doc 06 SM-FR/SM-UT/SM-UAT associations are those of FRD §11 (counts identical), so Part 6.1 §6.1.12.5 alias mapping holds without change | §2.7.4.6 |
| GAP-340 | Gap | {{FLD_P}} retained-baseline fields had no field-level specification in the blueprint | Closed by Batch 2.7b |
| GAP-341 | Gap | No legacy screen ID crosswalk or retained website capability mapping | Closed §2.7.4.1, FR-ENH-C-001 |
| GAP-342 | Gap | {{OPS_DN}} distinct legacy operations have no blueprint equivalent; {{OPS_DP}} only an equivalent under another path | §2.7.4.3–4; FR-ENH-C-003 |
| GAP-343 | Gap | 435 related-screen links not represented in navigation | FR-ENH-C-012 |
| GAP-344 | Gap | Per-screen integration associations, licence and capacity display not specified | FR-ENH-C-009; §2.7.4.7 |
| GAP-345 | Gap | Optimization Intelligence panel not specified | FR-ENH-C-004 |
| GAP-346 | Gap | Dashboard latency load scenario (50/250 staff, 100k/1m opportunities) missing | FR-ENH-C-017; LT-ENH-C-01 |
| GAP-347 | Gap | Design handoff record and design evidence pack missing | FR-ENH-C-010, FR-ENH-C-011 |
| GAP-348 | Gap | Status footer items, filter result count and focus restoration missing | FR-ENH-C-007, FR-ENH-C-008 |
| GAP-349 | Gap | No entity for `sales_business_template` or `sales_ui_service_request`; Part 3.2 support-case operations (API-440, API-442) have no entity | §2.7.5.4 |
| CONFLICT-340…351 | Conflict | See §2.7.6 | §2.7.6 |
| RECOMMENDATION-340 | Recommendation | Legacy alias routing layer (single canonical handler, Deprecation/Link headers, alias table) | §2.7.5.3 |
| RECOMMENDATION-341 | Recommendation | Generate a machine-readable field-contract registry (YAML per screen) from Batch 2.7b to drive FormSchemaRenderer, serializers and tests | §2.7.5.1 |
| RECOMMENDATION-342 | Recommendation | Viewport test matrix 360/768/1280/1440 plus 320 reflow | CONFLICT-342 |
| RECOMMENDATION-343 | Recommendation | AdapterCard component (licence, capacity, residual cost, benchmark, fallback approval) reused in A008, A011, A012, A033, A102 | FR-ENH-C-009 |
| RECOMMENDATION-344 | Recommendation | Add the Unassessed UI state | §2.7.5.2 |
| RECOMMENDATION-345 | Recommendation | "Related" menu component carrying scope and record ID | FR-ENH-C-012 |
| RECOMMENDATION-346 | Recommendation | Design evidence pack per wave stored as EVR evidence | FR-ENH-C-011 |
| RECOMMENDATION-347 | Recommendation | Productivity benchmark protocol (baseline vs candidate, named user, no safeguard reduction) | FR-ENH-C-016 |
| RECOMMENDATION-348 | Recommendation | Projection freshness tiers O (≤ 60 s) and A (≤ 15 min) | CONFLICT-348 |
| RECOMMENDATION-349 | Recommendation | Build-class weighting for screen-level estimation | §2.7.5.8 |

**Inconsistencies found in earlier parts (reported, not fixed):** (1) Part 2.5 §2.43 says "Field lists are in FR rows (Part 2.1)" while Part 2.1 §2.4 says "full field-level specs appear in Batch 2.5"; neither holds the full lists (GAP-340). (2) Part 3.2 API-440/API-442 expose support cases with no Part 3.3 entity (GAP-349). (3) Part 2.5 §2.48 breakpoints differ from DEC-043 wording "Admin desktop-first (1280 px+, usable down to 768 px)" only in the 768–899 px band, where Part 2.5 tier SM says "read-only dashboards" (CONFLICT-342 resolution applies).

---

## 2.7.9 Quality gate

| # | Check | Result | Notes and fixes applied |
|---|---|---|---|
| 1 | Every requirement traced to a source | Pass | Every FR-ENH-C, TC, conflict and gap cites doc 06/17 sections and blueprint IDs; CSV carries section per row |
| 2 | Assumptions, gaps, conflicts tagged and logged | Pass | 6 assumptions, 10 gaps, 12 conflicts, 10 recommendations, all within 340–359; register §2.7.8 |
| 3 | IDs unique and consistent | Pass | FR-ENH-C-001…017, TC-ENH-C-001…020 and 101…247, US-xx-EC01…04, LT-ENH-C-01; OKPI naming used for pack KPIs |
| 4 | No story lacks AC; no requirement lacks a test | Pass | Each FR-ENH-C has a TC; each story has Gherkin scenarios |
| 5 | Negative, edge, security, accessibility cases | Pass | TC-ENH-C-002/004/006/015/020 negative and security; 007/010 accessibility |
| 6 | Agents: guardrail, fallback, KPI, cost | N/A | No agent added; Copilot reading consistent with DEC-035 |
| 7 | Time-sensitive facts flagged | Pass | Provider prices in doc 06 not restated as fact; CONFLICT-347; "verify at time of implementation (as of 27 Nov 2026)" |
| 8 | No restricted data routed to free-tier models | Pass | No routing change; DEV plugins excluded from runtime |
| 9 | Consistent with earlier parts | Pass | Additive only; conflicts carry proposed resolutions; earlier-part inconsistencies reported in §2.7.8 |

**Status: Part 2 Batch 2.7a complete. Documents 06 and 17 reviewed line by line and parsed programmatically: {{CSV_ROWS}} atomic aspects; 147/147 screens reconciled; {{OPS_DIST}} operations, 155 tables and 138 test associations mapped; 17 enhanced FRs, 20 global test cases plus 147 per-screen conformance tests, 8 user stories; 12 conflicts with proposed resolutions. Per-screen contract cards: Batch 2.7b.**
