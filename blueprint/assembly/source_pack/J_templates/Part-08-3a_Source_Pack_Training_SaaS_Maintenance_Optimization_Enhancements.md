# AI Growth Engine: Employee Sales & Marketing Automation
## Application Blueprint: PART 8 (Batch 8.3a), Source Pack Review: Training, SaaS Service Operations, Maintenance and Optimization (Documents 33–36, 38): Documents Reviewed, Coverage Register and Catalogue Reconciliation

| Field | Value |
|---|---|
| Document | Application Blueprint, Part 8, Batch 8.3 (file a of 3), source-pack group J |
| Version | 1.0 · 27 Nov 2026 |
| Baseline | Part 0 (inventory, NFR-001…038), Part 0A (DEC-001…065), Part 1 (BR, P01–P16, KPI-01…31), Part 2.1 (FR register), Part 2.3 (BRL, R01–R20, RBAC matrix), Part 2.4 (RP, CFG), Part 2.5 (147 screens), Part 4.2 (NFR-001…099), Part 4.3 (SLO-01…12, RB-001…015, support, FinOps), Part 6.1/6.6/6.7 (EVR, RTM, TC-NFR), Part 7.3, Part 8.1, Part 8.2, Part 9.1 (DEC-066…156), Part 9.3 (inventory) |
| Source documents reviewed | 33 End User, Administrator & Operational Training Manual · 34 SaaS Client Onboarding, Service Delivery, SLA & Commercial Operations · 35 Product Maintenance, Continuous Improvement & Lifecycle Management · 36 Comprehensive Product Optimization Engineering · 38 Sales & Marketing Automation — All Numbers |
| Roles applied | Training and Change Lead, SaaS Service Owner, Product Operations Lead, Optimization Engineer, FinOps Lead, with Product Owner, QA Lead, DevOps/SRE Lead and Security/Compliance Lead as reviewers |
| Companion files | Part 8.3b (operational training manual), Part 8.3c (SaaS service operations, maintenance lifecycle, optimization model, conflicts, tags, quality gate) |
| Scripts | `assembly/source_pack/J_build_data.py` (parses every table row of documents 33–36 and 38 plus the blueprint registers), `J_maps.py` (reviewed mappings), `J_build_docs.py` (generates the tables in this part and `final/coverage/J_coverage.csv`) |

**Acronyms used in this part.** AP acceptance procedure · CCB change control board · CSO client service operation (new ID family) · EVR evidence record (Part 6.1 §6.1.5.4) · FR-ENH enhanced functional requirement · G0 non-weighted blocking gate · LC lifecycle change procedure · LJ learning journey · MNT maintenance task · OKPI optimization key performance indicator (the source pack's KPI-01…35, renamed to avoid collision with Part 1 KPI-01…31) · OPT optimization dimension or control · PD person-day · PF practice family · QC quality control · RACI responsible, accountable, consulted, informed · RPO/RTO recovery point/time objective · SLA service level agreement · SLI/SLO service level indicator/objective · SOP standard operating procedure · TM training module · TRN training artefact (task card, exercise, assessment) · TS troubleshooting card · UAT user acceptance testing.

**ID rule used throughout Part 8.3.** The source pack numbers its optimization KPIs `KPI-01…KPI-35`. Inside the blueprint they are always **OKPI-01…OKPI-35**. Part 1 `KPI-01…31` keep their business meaning. Source IDs that do not collide (`OPT-01-01…OPT-20-04`, `OPT-TEST-01…24`, `UX-QC-01…10`, `SM-UAT-S001…S138`) are kept unchanged and mapped to blueprint IDs.

---

## 8.3.1 Documents reviewed

All five documents were read line by line. Every table row was also parsed by `J_build_data.py` (138 navigation entries, 138 practice rows, 6 journeys, 4 recovery cards, 7 exercise rows in document 33; 20 dimensions, 104 controls, 35 OKPIs, 24 scenarios, 5 benchmark rows, 10 UX-QC rows, 17 acceptance procedures and 7 panel rows in document 36; 21 tables in document 38). The coverage CSV has one row per atomic aspect ({{N_ASPECTS}} rows).

{{DOC_SIZES}}

### 8.3.1.1 Shared core (counted once)

Each document repeats the same core: product purpose and boundary ("employee-operated commercial growth; confidential investor records and fundraising are not functions of this application"), the 147-interface scope (34 Website + 113 Admin), retained and expansion counts (302 + 19 operations, 149 + 6 entities, 624 + 175 tests), the four product-specific business controls (AppNAI bids, MedMaarg non-clinical, EduVerse safeguarding, OrganicSpec separate ledgers, plus commercial campaigns), the completion/approval table and the five-field evidence record. These are recorded once per document as **"Common core: see document 01/02 coverage"** and map to Part 0 §0.2, Part 1, Part 2.2 vertical routes and the EVR (Part 6.1 §6.1.5.4).

### 8.3.1.2 Document 33: End User, Administrator & Operational Training Manual

| Item | Content |
|---|---|
| Sections | Purpose and boundary · Before using the application · Role-based learning journeys (6) · Screen navigation guide: Website W01–W30 (30 entries) · Screen navigation guide: Admin A001–A108 (108 entries) · Common troubleshooting / Safe recovery (4) · Completion and approval · Implementation, verification and delivery controls (138-row practice table with SM-UAT-S001…S138) · Acceptance and evidence record · Practical training and acceptance exercise (4 exercises + 3 operating-training rows) · Optimization engineering and acceptance (OPT-03-01, 04-01, 15-01…04) · Implementation acceptance and verification (5 procedures, twice) · Boundary and acceptance conditions · Current multi-startup scope: Training for the nine new interfaces |
| What it is trying to tell | Every person who touches the product (internal employee, administrator, support operator, external customer/supplier, SaaS client) must learn the product **by role and by screen**, using only synthetic data, demonstrating one denied action and one error recovery, and the trainer must record evidence. Each of the 138 original screens has an access class, a purpose line, a standard operating pattern and a practice procedure tied to a UAT ID |
| Pattern | Templated: one standard 4-step operating procedure is reused for every screen; {{N_GENERIC}} of the 108 Admin entries carry the same generic purpose line ("Open the named function within the assigned workspace…"), so the registers and task cards show the Part 2.1 FR text for those screens; the practice table uses 2 procedure templates (public 30, Admin 108) and 23 domain-specific success/troubleshooting families (publication, campaign, evidence, dispatch, order, payment, MedMaarg, EduVerse, renewal, tenant isolation and others), see §8.3.4.2 |
| Atomic aspects | {{N_D33}} (38 non-screen aspects + 138 navigation entries + 138 practice/UAT rows + 9 new-interface training aspects) |

### 8.3.1.3 Document 34: SaaS Client Onboarding, Service Delivery, SLA & Commercial Operations

| Item | Content |
|---|---|
| Sections | Purpose and boundary · Service definition and contracting (plans, eligibility, managed service, commercial terms) · Client onboarding (provision, configure, website, integrations, train and activate) · Service delivery and SLA (availability, response, reliability, reporting, billing, profitability) · Renewal and offboarding (renewal, suspend, export, offboard) · Business controls · Completion · Service stage table (8 stages) and billing formula · Client service lifecycle and unit economics (5 rows) · Optimization (per-tenant measures; OPT-01-01, 03-01…08, 06-01, 14-01, 19-01, 20-01…04) · Implementation acceptance (13 procedures, twice) · SaaS service lifecycle and applicant draft boundary |
| What it is trying to tell | The SaaS line is a separately contracted, separately billed service: plans and fees must be approved before any price appears; clients are provisioned only after verified authority; SLA figures are **proposals** that become contractual only after measurement; every tenant's contribution margin is measured; offboarding leaves no live access |
| Pattern | Proposal-with-evidence: each item ends with an acceptance-evidence statement; the expansion section restates W31–W34 and the applicant-draft boundary |
| Atomic aspects | {{N_D34}} |

### 8.3.1.4 Document 35: Product Maintenance, Continuous Improvement & Lifecycle Management

| Item | Content |
|---|---|
| Sections | Purpose and boundary · Maintenance operating model (ownership, intake, prioritize, change management, emergency fix) · Recurring maintenance (daily, weekly, monthly, quarterly, annual) · Lifecycle changes (AI model/prompt, knowledge, provider, database, frontend, retire feature) · Improvement measurement (business, engineering, service economics, learning loop) · Business controls · Completion · Cadence table (6 rows) and versioning rules · Maintenance schedule (5 rows) · Optimization cycle (OPT-03-01, 05-01, 10-01, 13-01…04, 14-01, 17-01, 18-01, 20-01) · Implementation acceptance (6 procedures, twice) · Resource and deployment approval · Maintenance for the expanded scope |
| What it is trying to tell | After go-live the product is run by a named roster on a fixed calendar; every change (including AI, provider and knowledge changes) goes through impact assessment, regression and approval; features are retired through notice, export and clean removal; improvement is measured as trends, not punitive metrics |
| Pattern | Two overlapping cadence tables plus lifecycle procedures; the blueprint had the pieces scattered across Part 4.3 and Part 8.2 |
| Atomic aspects | {{N_D35}} |

### 8.3.1.5 Document 36: Comprehensive Product Optimization Engineering

| Item | Content |
|---|---|
| Sections | 1 Operating architecture and priority · 2 Weighted scorecard and gates (20 dimensions, weights, accountable roles, formula) · 3 Engineering implementation controls (104 controls OPT-01-01…OPT-20-04 in 20 dimension groups) · 4 KPI acceptance matrix (35 KPIs, renamed OKPI) · 5 Admin optimization panel (7 card groups with endpoints and sources) · 6 Benchmarking and trade-off control (5 candidates) · 7 Continuous optimization and acceptance · 8 Executable acceptance planning (OPT-TEST-01…24) · Implementation acceptance and verification (13 + 4 procedures) · Final decision controls (evidence integrity, approval effort, combined preflight) · Expansion scope (nine interfaces, UX-QC-01…10) |
| What it is trying to tell | Optimization is a governed engineering discipline: each dimension has a weight and an accountable role; each control has a measurable acceptance; a score may only be given with evidence; mandatory failures block irrespective of score; optimizers never deploy or move money by themselves |
| Pattern | Register-style; heavy reuse of the same targets as the blueprint NFRs, plus a few targets that differ (see §8.3.6) |
| Atomic aspects | {{N_D36}} |
| **Note on dimension count** | The source lists **20** weighted dimensions (Σ = 100%) in both document 36 ("20 optimization dimensions") and document 38. The assignment brief says 21. Part 8.3c adopts the 20 source dimensions and adds one non-weighted blocking gate **G0** so that the model has 21 rows, of which 20 carry weight [CONFLICT-486] |

### 8.3.1.6 Document 38: Sales & Marketing Automation — All Numbers

| Item | Content |
|---|---|
| Sections | Reading guide (Inventory / Candidate / Target / Verified / Historical / Illustrative) · 01 Scope and deliverables · 02 UI coverage, API and data inventory · 03 Engineering candidate additions (19 operations, 6 entities) · 04 Testing, quality and evidence (tests by level, nine acceptance groups, verification counts) · 05 Effort and resource planning · 06 Optimization dimensions and scale · 07–08 KPI thresholds (35) · 09 Automation, configuration and prototype inventory (20 templates, 20 × 5 use cases, 13 node types) · 10 Documentation, historical evidence and limits · 11–12 Historical page references |
| What it is trying to tell | The authoritative count of everything in the package, with an explicit warning that inventory counts, candidate counts and historical runs are **not** evidence of a working product |
| Pattern | Counts only; every number is reconciled against the blueprint in §8.3.4.1 |
| Atomic aspects | {{N_D38}} |

---

## 8.3.2 Coverage register summary

Status definitions follow the Source Pack brief: **Covered** (the blueprint already specifies it at equal or stricter level), **Partially covered** (present but missing a field, threshold, procedure or evidence rule), **Not covered**, **Conflict** (the blueprint states something different; proposed resolution in §8.3.6 of Part 8.3c), **Not applicable** (reason given).

{{STATUS_SUMMARY}}

**Reading the numbers.** Document 33 is mostly "Partially covered" because the blueprint has all 147 screens, their FRs, stories, tests and UAT aliases, but no operating procedure, task card or practice record for users. Part 8.3b adds one task card per screen. Document 36 is mostly "Covered" at control level (78 of 104 controls already have an equal or stricter blueprint NFR, BRL or DEC), but the optimization model itself (dimensions, weights, scorecard, scenarios, OKPI registry, panel, evidence gate) did not exist. Part 8.3c adds it.

---

## 8.3.3 Detailed coverage register

Every Partially covered, Not covered and Conflict item is listed individually below. Screen-level items are listed in one consolidated table per document (one row per screen). The CSV `final/coverage/J_coverage.csv` holds the same rows plus every Covered row.

### 8.3.3.1 Document 33: non-screen aspects

{{REG_D33_EXTRA}}

### 8.3.3.2 Document 33: screen-level aspects (147 screens; 138 navigation entries and 138 practice rows plus 9 new interfaces)

Navigation-procedure status is **Partially covered** for all 138 original screens: the screen, FR, stories and tests exist; the user-facing procedure does not. The UAT alias status is **Covered**: all {{N_SMUAT_RESOLVED}} SM-UAT-S IDs resolve in the Part 6.6 RTM to FR-W01…FR-A108 and their test cases (DEC-017). The nine new interfaces have no navigation entry in document 33, only the expansion-training paragraph, so their procedure status is **Not covered**.

{{REG_D33_SCREENS}}

### 8.3.3.3 Document 34

{{REG_D34}}

### 8.3.3.4 Document 35

{{REG_D35}}

### 8.3.3.5 Document 36: non-control aspects

Controls (104), OKPIs (35), scenarios (24) and UX-QC (10) are listed in full in Part 8.3c §8.3.5.15 with their status, because their mapping tables are the enhancement itself.

{{REG_D36_EXTRA}}

### 8.3.3.6 Document 38

Listed in §8.3.4.1 (the reconciliation table is the register for document 38).

---

## 8.3.4 Catalogue reconciliation

### 8.3.4.1 Document 38 "All Numbers" against the blueprint (every number)

Rule applied: a difference is acceptable only when it is explained by (a) a different counting unit, (b) a documented DERIVED superset decision, (c) historical or package-only metrics that are not software scope, or (d) a recorded conflict with a proposed resolution.

{{RECON_D38}}

**Acceptance groups (document 38 §04) reconciled.** 180 decision approvals + 624 product tests + 235 QC + 104 optimization controls + 24 optimization scenarios + 21 mandatory KPIs = **1,188** (the "combined preflight" of document 36). Adding 172 expansion decisions + 175 expansion tests + 10 expansion QC gives **1,545** (document 38). Both totals are arithmetically correct; they describe different scopes [CONFLICT-491]. Part 8.3c §8.3.5.15.10 maps the nine groups to blueprint EVR gate groups G1…G9.

**Effort (document 38 §05) reconciled.** Document 38: gross base = 385 + 114 = 499 PD before reuse and overlap. Blueprint Part 8.1 §8.1.6.4: central 416 pd with the nine new screens already inside the story plan. Using the source's own formula, adjusted effort = 385 + 114 × (1 − f). Setting this equal to 416 gives f = 1 − 31 ÷ 114 = **0.728**: the blueprint plan implies that 72.8% of the expansion effort overlaps work already in the baseline stories. The same check for the low and high bands: low 314 = 287 + 62 × (1 − f) → f = 0.565; high 518 = 483 + 196 × (1 − f) → f = 0.821. The blueprint plan remains binding (DEC-124); the pack figures are a pre-reuse ceiling [CONFLICT-488].

### 8.3.4.2 Training manual catalogue (document 33) against the screen inventory

| Check (programmatic) | Result |
|---|---|
| Navigation entries vs Part 2.5 screens | 138 of 147 (W01–W30, A001–A108). The nine new screens W31–W34, A109–A113 appear only in the expansion training paragraph and the UX-QC table; Part 8.3b adds their task cards |
| Practice rows vs navigation entries | 138 = 138; same order; SM-UAT-S001…S138 contiguous |
| SM-UAT-S IDs resolving in Part 6.6 RTM | {{N_SMUAT_RESOLVED}} of 138 (S001–S030 → FR-W01…W30; S031–S138 → FR-A001…A108) |
| Access classes in document 33 | {{P_ACCESS}} |
| Access-class differences with Part 2.1 | 3: W17 and W30 are "Public / Portal" in document 33 and "Public" in Part 2.1; W21 is "Authentication" in document 33 and "Portal" in Part 2.1. No rule changes: both pages are reachable from the public site and the portal shell; W21 is the portal sign-in. Recorded as Covered with note |
| Title wording differences | {{N_TITLE_DIFF}} (table below). All are abbreviations or catalog/catalogue spelling; IDs and meaning agree. Training material uses the Part 2.5 title and shows the document 33 title as an alias |
| Practice families | 23 families cover all 138 practice rows (none unclassified); Part 8.3b §8.3.5.5 turns each family into a reusable practice script |

{{TITLE_DIFF}}

### 8.3.4.3 Optimization controls (document 36) against the blueprint

Before this part, the blueprint cited **{{N_OPT_PRE}}** of the 104 controls (the 22 OPT IDs that also appear in the BRD/FRD: OPT-01-01, 03-01, 04-01…08, 07-01, 10-01, 11-01, 12-01…04, 15-01, 20-01…04). Part 8.3c maps all 104. Status after mapping: {{CONTROL_COUNTS}}.

{{RECON_OPT_BY_DIM}}

### 8.3.4.4 Optimization KPIs (OKPI-01…35)

{{N_MAND}} OKPIs are mandatory (blocking): {{MAND_LIST}}. Status after mapping to blueprint NFR, KPI and SLO IDs: {{OKPI_COUNTS}}. Full table: Part 8.3c §8.3.5.15.4.

### 8.3.4.5 Scenarios, UX-QC and acceptance procedures

| Source set | Count | Blueprint before | After this part |
|---|---|---|---|
| OPT-TEST-01…24 | 24 | 0 | TC-ENH-J-001…024 (Part 8.3c §8.3.5.15.5) |
| UX-QC-01…10 | 10 | Behaviour covered by EP-18/EP-20 stories; no acceptance wrapper | TC-ENH-J-025…034 |
| Document 33 acceptance procedures | 5 (+1 boundary) | 3 covered (tenant lifecycle, accessibility, offboarding) | Handover → TC-ENH-J-051; productivity → §8.3.5.9 |
| Document 34 acceptance procedures | 13 | 9 covered | 4 added (TC-ENH-J-020, 038, 040, 042) |
| Document 35 acceptance procedures | 6 | 2 covered | 4 added (TC-ENH-J-047…051) |
| Document 36 acceptance procedures | 17 | 9 covered | Numeric guardrails, fail-closed evidence, cache key, preflight added (TC-ENH-J-055…057, FR-ENH-J-015/016) |

---

## 8.3.4.6 Quality gate: Batch 8.3a

| # | Check | Result | Notes and fixes applied |
|---|---|---|---|
| 1 | Every requirement traced to a source | Pass | Every row cites the source document and section and the blueprint location |
| 2 | Assumptions, gaps, conflicts tagged and logged | Pass | Tags in the 480–499 ranges; register in Part 8.3c §8.3.8 |
| 3 | IDs unique and consistent | Pass | OKPI rename applied everywhere; new families checked against all parts (no TM-, LJ-, TRN-, MNT-, CSO-, SLA-, LC-, OKPI- prior use) |
| 4 | No story lacks AC; no requirement lacks a test | N/A in 8.3a | Stories, AC and tests are in Part 8.3b/8.3c |
| 5 | Negative, edge, security, accessibility cases | N/A in 8.3a | See Part 8.3b/8.3c |
| 6 | No agent lacks guardrail, fallback, KPI, cost | N/A | No new agent |
| 7 | Time-sensitive facts flagged | Pass | No prices or provider terms stated in this file |
| 8 | No restricted data to free-tier models | Pass | Not affected |
| 9 | Consistent with earlier parts | Pass with conflicts recorded | 12 conflicts (CONFLICT-480…491) with proposed resolutions in Part 8.3c §8.3.6 |

**Status: Part 8 Batch 8.3a complete. Five source documents reviewed line by line; {{N_ASPECTS}} atomic aspects registered; every number in document 38 reconciled.**
