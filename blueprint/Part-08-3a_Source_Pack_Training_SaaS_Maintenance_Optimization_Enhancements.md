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

All five documents were read line by line. Every table row was also parsed by `J_build_data.py` (138 navigation entries, 138 practice rows, 6 journeys, 4 recovery cards, 7 exercise rows in document 33; 20 dimensions, 104 controls, 35 OKPIs, 24 scenarios, 5 benchmark rows, 10 UX-QC rows, 17 acceptance procedures and 7 panel rows in document 36; 21 tables in document 38). The coverage CSV has one row per atomic aspect (786 rows).

| Doc | Title | Bytes (text extraction) | Lines | Atomic aspects |
|---|---|---|---|---|
| 33 | End User, Administrator & Operational Training Manual | 199,484 | 1349 | 323 |
| 34 | SaaS Client Onboarding, Service Delivery, SLA & Commercial Operations | 32,181 | 380 | 52 |
| 35 | Product Maintenance, Continuous Improvement & Lifecycle Management | 22,197 | 274 | 49 |
| 36 | Comprehensive Product Optimization Engineering | 63,866 | 749 | 237 |
| 38 | Sales & Marketing Automation — All Numbers | 18,600 | 1100 | 125 |

### 8.3.1.1 Shared core (counted once)

Each document repeats the same core: product purpose and boundary ("employee-operated commercial growth; confidential investor records and fundraising are not functions of this application"), the 147-interface scope (34 Website + 113 Admin), retained and expansion counts (302 + 19 operations, 149 + 6 entities, 624 + 175 tests), the four product-specific business controls (AppNAI bids, MedMaarg non-clinical, EduVerse safeguarding, OrganicSpec separate ledgers, plus commercial campaigns), the completion/approval table and the five-field evidence record. These are recorded once per document as **"Common core: see document 01/02 coverage"** and map to Part 0 §0.2, Part 1, Part 2.2 vertical routes and the EVR (Part 6.1 §6.1.5.4).

### 8.3.1.2 Document 33: End User, Administrator & Operational Training Manual

| Item | Content |
|---|---|
| Sections | Purpose and boundary · Before using the application · Role-based learning journeys (6) · Screen navigation guide: Website W01–W30 (30 entries) · Screen navigation guide: Admin A001–A108 (108 entries) · Common troubleshooting / Safe recovery (4) · Completion and approval · Implementation, verification and delivery controls (138-row practice table with SM-UAT-S001…S138) · Acceptance and evidence record · Practical training and acceptance exercise (4 exercises + 3 operating-training rows) · Optimization engineering and acceptance (OPT-03-01, 04-01, 15-01…04) · Implementation acceptance and verification (5 procedures, twice) · Boundary and acceptance conditions · Current multi-startup scope: Training for the nine new interfaces |
| What it is trying to tell | Every person who touches the product (internal employee, administrator, support operator, external customer/supplier, SaaS client) must learn the product **by role and by screen**, using only synthetic data, demonstrating one denied action and one error recovery, and the trainer must record evidence. Each of the 138 original screens has an access class, a purpose line, a standard operating pattern and a practice procedure tied to a UAT ID |
| Pattern | Templated: one standard 4-step operating procedure is reused for every screen; 106 of the 108 Admin entries carry the same generic purpose line ("Open the named function within the assigned workspace…"), so the registers and task cards show the Part 2.1 FR text for those screens; the practice table uses 2 procedure templates (public 30, Admin 108) and 23 domain-specific success/troubleshooting families (publication, campaign, evidence, dispatch, order, payment, MedMaarg, EduVerse, renewal, tenant isolation and others), see §8.3.4.2 |
| Atomic aspects | 323 (38 non-screen aspects + 138 navigation entries + 138 practice/UAT rows + 9 new-interface training aspects) |

### 8.3.1.3 Document 34: SaaS Client Onboarding, Service Delivery, SLA & Commercial Operations

| Item | Content |
|---|---|
| Sections | Purpose and boundary · Service definition and contracting (plans, eligibility, managed service, commercial terms) · Client onboarding (provision, configure, website, integrations, train and activate) · Service delivery and SLA (availability, response, reliability, reporting, billing, profitability) · Renewal and offboarding (renewal, suspend, export, offboard) · Business controls · Completion · Service stage table (8 stages) and billing formula · Client service lifecycle and unit economics (5 rows) · Optimization (per-tenant measures; OPT-01-01, 03-01…08, 06-01, 14-01, 19-01, 20-01…04) · Implementation acceptance (13 procedures, twice) · SaaS service lifecycle and applicant draft boundary |
| What it is trying to tell | The SaaS line is a separately contracted, separately billed service: plans and fees must be approved before any price appears; clients are provisioned only after verified authority; SLA figures are **proposals** that become contractual only after measurement; every tenant's contribution margin is measured; offboarding leaves no live access |
| Pattern | Proposal-with-evidence: each item ends with an acceptance-evidence statement; the expansion section restates W31–W34 and the applicant-draft boundary |
| Atomic aspects | 52 |

### 8.3.1.4 Document 35: Product Maintenance, Continuous Improvement & Lifecycle Management

| Item | Content |
|---|---|
| Sections | Purpose and boundary · Maintenance operating model (ownership, intake, prioritize, change management, emergency fix) · Recurring maintenance (daily, weekly, monthly, quarterly, annual) · Lifecycle changes (AI model/prompt, knowledge, provider, database, frontend, retire feature) · Improvement measurement (business, engineering, service economics, learning loop) · Business controls · Completion · Cadence table (6 rows) and versioning rules · Maintenance schedule (5 rows) · Optimization cycle (OPT-03-01, 05-01, 10-01, 13-01…04, 14-01, 17-01, 18-01, 20-01) · Implementation acceptance (6 procedures, twice) · Resource and deployment approval · Maintenance for the expanded scope |
| What it is trying to tell | After go-live the product is run by a named roster on a fixed calendar; every change (including AI, provider and knowledge changes) goes through impact assessment, regression and approval; features are retired through notice, export and clean removal; improvement is measured as trends, not punitive metrics |
| Pattern | Two overlapping cadence tables plus lifecycle procedures; the blueprint had the pieces scattered across Part 4.3 and Part 8.2 |
| Atomic aspects | 49 |

### 8.3.1.5 Document 36: Comprehensive Product Optimization Engineering

| Item | Content |
|---|---|
| Sections | 1 Operating architecture and priority · 2 Weighted scorecard and gates (20 dimensions, weights, accountable roles, formula) · 3 Engineering implementation controls (104 controls OPT-01-01…OPT-20-04 in 20 dimension groups) · 4 KPI acceptance matrix (35 KPIs, renamed OKPI) · 5 Admin optimization panel (7 card groups with endpoints and sources) · 6 Benchmarking and trade-off control (5 candidates) · 7 Continuous optimization and acceptance · 8 Executable acceptance planning (OPT-TEST-01…24) · Implementation acceptance and verification (13 + 4 procedures) · Final decision controls (evidence integrity, approval effort, combined preflight) · Expansion scope (nine interfaces, UX-QC-01…10) |
| What it is trying to tell | Optimization is a governed engineering discipline: each dimension has a weight and an accountable role; each control has a measurable acceptance; a score may only be given with evidence; mandatory failures block irrespective of score; optimizers never deploy or move money by themselves |
| Pattern | Register-style; heavy reuse of the same targets as the blueprint NFRs, plus a few targets that differ (see §8.3.6) |
| Atomic aspects | 237 |
| **Note on dimension count** | The source lists **20** weighted dimensions (Σ = 100%) in both document 36 ("20 optimization dimensions") and document 38. The assignment brief says 21. Part 8.3c adopts the 20 source dimensions and adds one non-weighted blocking gate **G0** so that the model has 21 rows, of which 20 carry weight [CONFLICT-486] |

### 8.3.1.6 Document 38: Sales & Marketing Automation — All Numbers

| Item | Content |
|---|---|
| Sections | Reading guide (Inventory / Candidate / Target / Verified / Historical / Illustrative) · 01 Scope and deliverables · 02 UI coverage, API and data inventory · 03 Engineering candidate additions (19 operations, 6 entities) · 04 Testing, quality and evidence (tests by level, nine acceptance groups, verification counts) · 05 Effort and resource planning · 06 Optimization dimensions and scale · 07–08 KPI thresholds (35) · 09 Automation, configuration and prototype inventory (20 templates, 20 × 5 use cases, 13 node types) · 10 Documentation, historical evidence and limits · 11–12 Historical page references |
| What it is trying to tell | The authoritative count of everything in the package, with an explicit warning that inventory counts, candidate counts and historical runs are **not** evidence of a working product |
| Pattern | Counts only; every number is reconciled against the blueprint in §8.3.4.1 |
| Atomic aspects | 125 |

---

## 8.3.2 Coverage register summary

Status definitions follow the Source Pack brief: **Covered** (the blueprint already specifies it at equal or stricter level), **Partially covered** (present but missing a field, threshold, procedure or evidence rule), **Not covered**, **Conflict** (the blueprint states something different; proposed resolution in §8.3.6 of Part 8.3c), **Not applicable** (reason given).

| Document | Aspects | Covered | Partially covered | Not covered | Conflict | Not applicable |
|---|---|---|---|---|---|---|
| 33 End User, Administrator & Operational Training Manual | 323 | 150 | 157 | 16 | 0 | 0 |
| 34 SaaS Client Onboarding, Service Delivery, SLA & Commercial Operations | 52 | 29 | 19 | 2 | 2 | 0 |
| 35 Product Maintenance, Continuous Improvement & Lifecycle Management | 49 | 18 | 26 | 5 | 0 | 0 |
| 36 Comprehensive Product Optimization Engineering | 237 | 119 | 49 | 57 | 9 | 3 |
| 38 Sales & Marketing Automation — All Numbers | 125 | 68 | 36 | 5 | 7 | 9 |
| **Total** | 786 | 384 | 287 | 85 | 18 | 12 |

**Reading the numbers.** Document 33 is mostly "Partially covered" because the blueprint has all 147 screens, their FRs, stories, tests and UAT aliases, but no operating procedure, task card or practice record for users. Part 8.3b adds one task card per screen. Document 36 is mostly "Covered" at control level (78 of 104 controls already have an equal or stricter blueprint NFR, BRL or DEC), but the optimization model itself (dimensions, weights, scorecard, scenarios, OKPI registry, panel, evidence gate) did not exist. Part 8.3c adds it.

---

## 8.3.3 Detailed coverage register

Every Partially covered, Not covered and Conflict item is listed individually below. Screen-level items are listed in one consolidated table per document (one row per screen). The CSV `final/coverage/J_coverage.csv` holds the same rows plus every Covered row.

### 8.3.3.1 Document 33: non-screen aspects

| Aspect | Section | Summary | Status | Blueprint location | Action | New IDs |
|---|---|---|---|---|---|---|
| 33-01 | Purpose and operating boundary | Common core (purpose, boundary, counts) | Covered | Part 0/1 | Common core: see document 01/02 coverage |  |
| 33-02 | Before using the application | Use authorized environment and assigned identity | Covered | Part 8.2 §8.2.2.2 (staging, GSE-SYN) | — | §8.3.5.1 |
| 33-03 | Before using the application | Select correct tenant/startup before changing data | Covered | NFR-027; Part 2.5 §2.41 scope selector | Training step SOP-STD-01 | §8.3.5.3 |
| 33-04 | Before using the application | Synthetic fixtures only; never send, publish, submit bids/offers or process funds in training | Partially covered | Part 8.2 (GSE-SYN) | Training tenant with simulated adapters | FR-ENH-J-003 |
| 33-05 | Before using the application | Procedures describe proposed screens, not screenshots; replace with actual screenshots after development | Not covered | — | Screenshot replacement step in training content lifecycle | §8.3.5.9 |
| 33-06 | Role-based learning journeys | Marketing employee journey | Partially covered | Part 8.2 P05 modules | LJ-01 | §8.3.5.1 |
| 33-07 | Role-based learning journeys | Sales employee journey | Partially covered | Part 8.2 P03 modules | LJ-02 | §8.3.5.1 |
| 33-08 | Role-based learning journeys | Bid/procurement specialist journey | Partially covered | Part 8.2 P06/P07 | LJ-03 | §8.3.5.1 |
| 33-09 | Role-based learning journeys | External customer/supplier journey | Partially covered | Part 8.2 P14 (SP) | LJ-04 | §8.3.5.1 |
| 33-10 | Role-based learning journeys | Administrator journey | Partially covered | Part 8.2 P11 | LJ-05 | §8.3.5.1 |
| 33-11 | Role-based learning journeys | Support operator journey (temporary grant, escalate, revoke after resolution) | Partially covered | Part 8.2 P12; DEC-056 | LJ-06; revoke-on-resolution step | §8.3.5.1 |
| 33-12 | Role-based learning journeys | Practice rule: complete journey in UAT, show one denied action and one error recovery; trainer records completion and remediation | Not covered | — | Assessment rule TRN-AS-01 | §8.3.5.8 |
| 33-13 | Screen navigation guide | Standard operating steps (select permitted context → inspect → act only when eligible → review confirmation) | Not covered | — | SOP-STD-01…06 | §8.3.5.3 |
| 33-14 | Screen navigation guide | Denied: never change scope to bypass; contact administrator | Covered | BRL-TEN-01/04; Part 2.5 §2.47 denied state | Included in SOP-STD-05 |  |
| 33-15 | Screen navigation guide | Uncertain provider outcome: escalate before retry | Covered | BRL-AUT-07; RB-003 | Included in SOP-STD-06 |  |
| 33-16 | Safe recovery | No records: check startup, role, filters; never request another tenant's records | Partially covered | Part 2.5 §2.47 empty state | TS-01 troubleshooting card | §8.3.5.7 |
| 33-17 | Safe recovery | Pending approval: review approver and scope; wait | Partially covered | BRL-APR-10 | TS-02 | §8.3.5.7 |
| 33-18 | Safe recovery | Failed action: read safe error and correlation ID; report; avoid repeated submission | Partially covered | NFR-079; Part 2.5 microcopy | TS-03 | §8.3.5.7 |
| 33-19 | Safe recovery | Wrong public content: report and request authorized unpublish; never edit published data directly | Partially covered | BRL-PUB-02; A108 rollback | TS-04 | §8.3.5.7 |
| 33-20 | Completion and approval | Sign-off roles | Covered | EVR | Common core |  |
| 33-21 | Implementation controls | Use actual proposed screen names; synthetic tenant/startup and role account; never real investor/customer records, credentials or live providers | Partially covered | Part 8.2 | Training tenant | FR-ENH-J-003 |
| 33-22 | Evidence record | Five evidence fields | Covered | EVR | Common core |  |
| 33-23 | Practical exercise | Quotation calculation 2 × INR 150.00, 10% discount → INR 270.00; server recomputes; reject invalid discount/price | Partially covered | BRL-QTE-01/02; TC-13-* | TRN-EX-01 | TC-ENH-J-052 |
| 33-24 | Practical exercise | Bid expiry 2030-06-01 09:00 UTC: reject at/after deadline; exception; no false award or call | Partially covered | BRL-BID-01 | TRN-EX-02 | TC-ENH-J-021 |
| 33-25 | Practical exercise | Order fulfilment 2 kg; 1 kg twice same key; +2 kg rejected | Partially covered | BRL-ORD-02/03 | TRN-EX-03 | TC-ENH-J-053 |
| 33-26 | Practical exercise | EduVerse routing: external AI dev → AppNAI; school AI education → EduVerse; client templates independent | Partially covered | BRL-BID-06 | TRN-EX-04 | TC-ENH-J-023 |
| 33-27 | Operating training | Admin scope: select tenant/startup, filters, simulate workflow, inspect blocked actions, pause | Partially covered | Part 8.2 P10/P11 modules | TRN-EX-05 | §8.3.5.6 |
| 33-28 | Operating training | External portal: own invited object; revoked/expired invitation → safe denial | Partially covered | BRL-TEN-04 | TRN-EX-06 | §8.3.5.6 |
| 33-29 | Operating training | Evidence: trainer records screenshot, role, outcome, corrective action | Not covered | — | TrainingRecord | FR-ENH-J-004 |
| 33-30 | Optimization | Teach staff to interpret measured vs proposed metrics, simulate, pause optional jobs, escalate legal/financial exceptions | Not covered | — | TM-29 | §8.3.5.2 |
| 33-31 | Optimization | OPT-03-01, OPT-04-01, OPT-15-01…04 cited | Covered | doc 36 rows | Mapped | §8.3.5.15.3 |
| 33-32 | Acceptance procedures | Independent client tenant lifecycle | Covered | US-2012 | — |  |
| 33-33 | Acceptance procedures | Operational knowledge and handover | Not covered | — | TRN-EX-12 | TC-ENH-J-051 |
| 33-34 | Acceptance procedures | Accessibility review (keyboard, focus, labels, contrast, screen reader) | Covered | NFR-088/089 | — |  |
| 33-35 | Acceptance procedures | User productivity: time representative task, errors and handoff; baseline vs candidate; no reduced approval safeguards | Partially covered | NFR-090 | Training-time baseline capture | §8.3.5.9 |
| 33-36 | Acceptance procedures | Offboarding and client independence | Covered | US-2009/2012 | — |  |
| 33-37 | Boundary and acceptance | Independent scope per action; revalidate permission, eligibility, budget, approved content at execution; two-tenant fixture | Covered | BRL-ELG-18; NFR-032 | — |  |
| 33-38 | Expansion training | Practice registration, configuration, startup selector, template, trigger, execution, conflict, service portal; roles, denied state, simulation, recovery without real credentials | Not covered | — | TM-24, TM-32; TRN-EX-07…11 | §8.3.5.10 |

### 8.3.3.2 Document 33: screen-level aspects (147 screens; 138 navigation entries and 138 practice rows plus 9 new interfaces)

Navigation-procedure status is **Partially covered** for all 138 original screens: the screen, FR, stories and tests exist; the user-facing procedure does not. The UAT alias status is **Covered**: all 138 SM-UAT-S IDs resolve in the Part 6.6 RTM to FR-W01…FR-A108 and their test cases (DEC-017). The nine new interfaces have no navigation entry in document 33, only the expansion-training paragraph, so their procedure status is **Not covered**.

| Screen | Access (doc 33) | Purpose (doc 33, or FR text where doc 33 is generic) | Navigation-procedure status | UAT alias status | Blueprint location | New IDs |
|---|---|---|---|---|---|---|
| W01 | Public | Approved business introductions, contact and enquiry paths. | Partially covered | Covered | FR-W01; Website: public | TRN-SCR-W01 |
| W02 | Public | Published businesses filtered by sector and geography. | Partially covered | Covered | FR-W02; Website: public | TRN-SCR-W02 |
| W03 | Public | Approved brand, capabilities, locations and contact. | Partially covered | Covered | FR-W03; Website: public | TRN-SCR-W03 |
| W04 | Public | Published offerings and facets by startup and business line. | Partially covered | Covered | FR-W04; Website: public | TRN-SCR-W04 |
| W05 | Public | Approved specifications, delivery model and availability claims. | Partially covered | Covered | FR-W05; Website: public | TRN-SCR-W05 |
| W06 | Public / Portal | Publish approved price only; private negotiated pricing requires identity. | Partially covered | Covered | FR-W06; Website: public | TRN-SCR-W06 |
| W07 | Public | Approved need-to-solution explanations and enquiry calls to action. | Partially covered | Covered | FR-W07; Website: public | TRN-SCR-W07 |
| W08 | Public | Published content and search; no internal research evidence. | Partially covered | Covered | FR-W08; Website: public | TRN-SCR-W08 |
| W09 | Public | Only approved and consented claims/media. | Partially covered | Covered | FR-W09; Website: public | TRN-SCR-W09 |
| W10 | Public | Published content, approved forms and attribution. | Partially covered | Covered | FR-W10; Website: public | TRN-SCR-W10 |
| W11 | Public | Public approved FAQ retrieval, rate limits, lead capture with permission. | Partially covered | Covered | FR-W11; Website: public | TRN-SCR-W11 |
| W12 | Public | Validate contact and requirement; enqueue scoped lead. | Partially covered | Covered | FR-W12; Website: intake forms | TRN-SCR-W12 |
| W13 | Public | Capture demo and partnership interest with consent. | Partially covered | Covered | FR-W13; Website: intake forms | TRN-SCR-W13 |
| W14 | Public / Portal | Submit line items, quantity, unit, delivery region and requirements; no automatic quote approval. | Partially covered | Covered | FR-W14; Website: intake forms | TRN-SCR-W14 |
| W15 | Public / Portal | AppNAI project intake; file uploads only after scoped authentication and scan. | Partially covered | Covered | FR-W15; Website: intake forms | TRN-SCR-W15 |
| W16 | Public / Portal | OrganicSpec supplier requirements, categories, units and verification initiation. | Partially covered | Covered | FR-W16; Website: intake forms | TRN-SCR-W16 |
| W17 | Public / Portal | EduVerse programme, age/grade, institution and cohort; guardian/authorized contact where required. | Partially covered | Covered | FR-W17; Website: intake forms | TRN-SCR-W17 |
| W18 | Public / Portal | Public request or token-bound booking; no private calendar exposure. | Partially covered | Covered | FR-W18; Website: intake forms | TRN-SCR-W18 |
| W19 | Public | Approved event information and eligible registration. | Partially covered | Covered | FR-W19; Website: intake forms | TRN-SCR-W19 |
| W20 | Public | Authorized referral submission with source and consent. | Partially covered | Covered | FR-W20; Website: intake forms | TRN-SCR-W20 |
| W21 | Authentication | Reuse existing identity; separate external audience and recovery. | Partially covered | Covered | FR-W21; Portal | TRN-SCR-W21 |
| W22 | Portal | Own commercial requests, orders and permitted documents only. | Partially covered | Covered | FR-W22; Portal | TRN-SCR-W22 |
| W23 | Portal | Read approved recipient-specific proposal or quotation; accept or request changes without modifying terms. | Partially covered | Covered | FR-W23; Portal | TRN-SCR-W23 |
| W24 | Portal | Identity-bound signing; token is not authorization by itself. | Partially covered | Covered | FR-W24; Portal | TRN-SCR-W24 |
| W25 | Portal | Own orders, milestones, delivery and status. | Partially covered | Covered | FR-W25; Portal | TRN-SCR-W25 |
| W26 | Portal | Own invoices, verified payment instructions and payment status. | Partially covered | Covered | FR-W26; Portal | TRN-SCR-W26 |
| W27 | Portal | Own onboarding tasks, requested files, scan and status. | Partially covered | Covered | FR-W27; Portal | TRN-SCR-W27 |
| W28 | Portal | Own support request, feedback and renewal interest; no automatic contract alteration. | Partially covered | Covered | FR-W28; Portal | TRN-SCR-W28 |
| W29 | Public / Portal | Signed opt-out token or own authenticated preferences; no contact lookup. | Partially covered | Covered | FR-W29; Portal | TRN-SCR-W29 |
| W30 | Public / Portal | Published contact/legal pages and scoped privacy/support intake. | Partially covered | Covered | FR-W30; Website: public | TRN-SCR-W30 |
| W31 | new | SaaS service entry separate from the customer journey; approved service terms only; no fundraising offers or implied outcomes (FR-W31) | Not covered | Covered (SM-UX-UAT) | FR-W31; Website: public | TRN-SCR-W31 |
| W32 | new | Independent client application; prove administrator authority; no provisioning before verified identity and approval; isolated expiring draft (FRD §16.3) (FR-W32) | Not covered | Covered (SM-UX-UAT) | FR-W32; Website: intake forms | TRN-SCR-W32 |
| W33 | new | Configure business without core code; AI proposals unverified; no dispatch or spend during onboarding; activation only when authorized (FR-W33) | Not covered | Covered (SM-UX-UAT) | FR-W33; Portal | TRN-SCR-W33 |
| W34 | new | Subscription and service lifecycle; client-only scoped billing; no cross-tenant records (FR-W34) | Not covered | Covered (SM-UX-UAT) | FR-W34; Portal | TRN-SCR-W34 |
| A001 | Admin | Reuse authentication; current user and permitted navigation; session revocation (FR-A001; doc 33 line generic) | Partially covered | Covered | FR-A001; Admin: global and identity | TRN-SCR-A001 |
| A002 | Admin | Invite, assign role/team/startup grants, revoke, MFA requirement, membership expiry (FR-A002; doc 33 line generic) | Partially covered | Covered | FR-A002; Admin: Automation | TRN-SCR-A002 |
| A003 | Admin | Scope selector (tenant → startup → business line → offering/objective), seven views, saved views (FR-A003; doc 33 line generic) | Partially covered | Covered | FR-A003; Admin: global and identity | TRN-SCR-A003 |
| A004 | Admin | List catalogue and readiness; product detail; create product, draft capabilities; version changes; approval (FR-A004; doc 33 line generic) | Partially covered | Covered | FR-A004; Admin: Automation | TRN-SCR-A004 |
| A005 | Admin | List approved catalogue and readiness; search approved knowledge only (FR-A005; doc 33 line generic) | Partially covered | Covered | FR-A005; Admin: Automation | TRN-SCR-A005 |
| A006 | Admin | Validate upload and enqueue indexing; list documents and ingestion state; approve/reject version; search approved knowledge (FR-A006; doc 33 line generic) | Partially covered | Covered | FR-A006; Admin: Automation | TRN-SCR-A006 |
| A007 | Admin | Record consent evidence; list policy versions and suppression; publish approved policy version; read scoped suppression (FR-A007; doc 33 line generic) | Partially covered | Covered | FR-A007; Admin: Automation | TRN-SCR-A007 |
| A008 | Admin | List safe connector metadata; configure via secret reference; test; disable (FR-A008; doc 33 line generic) | Partially covered | Covered | FR-A008; Admin: Automation | TRN-SCR-A008 |
| A009 | Admin | Read redacted audit/event state; list job status; idempotent retry (FR-A009; doc 33 line generic) | Partially covered | Covered | FR-A009; Admin: Automation | TRN-SCR-A009 |
| A010 | Admin | List eligible sources; register and approve scope; revise/expire approval (FR-A010; doc 33 line generic) | Partially covered | Covered | FR-A010; Admin: Automation | TRN-SCR-A010 |
| A011 | Admin | Inspect redacted runs; version prompts and fixtures; model adapter with structured output and bounded token budget (FR-A011; doc 33 line generic) | Partially covered | Covered | FR-A011; Admin: Automation | TRN-SCR-A011 |
| A012 | Admin | Read actual and reserved cost; set daily/monthly caps; emergency pause of controlled spend (FR-A012; doc 33 line generic) | Partially covered | Covered | FR-A012; Admin: Automation | TRN-SCR-A012 |
| A013 | Admin | Submit scoped request; list verified requests and deadlines; resolve after identity verification; versioned retention (FR-A013; doc 33 line generic) | Partially covered | Covered | FR-A013; Admin: Automation | TRN-SCR-A013 |
| A014 | Admin | Job status; operational health and failures; acknowledge/resolve incident (FR-A014; doc 33 line generic) | Partially covered | Covered | FR-A014; Admin: Automation | TRN-SCR-A014 |
| A015 | Admin | List sources and plans; create scoped plan; enqueue run; update schedule and approved query scope; no personal-health targeting (FR-A015; doc 33 line generic) | Partially covered | Covered | FR-A015; Admin: Discovery | TRN-SCR-A015 |
| A016 | Admin | List permitted discovered records; research progress; single authorized search API; cache and source checks (FR-A016; doc 33 line generic) | Partially covered | Covered | FR-A016; Admin: Discovery | TRN-SCR-A016 |
| A017 | Admin | Inspect provenance and excerpt; filter evidence; redacted run records (FR-A017; doc 33 line generic) | Partially covered | Covered | FR-A017; Admin: Discovery | TRN-SCR-A017 |
| A018 | Admin | List/filter; create or upsert canonical account; profile; controlled merge with referential checks (FR-A018; doc 33 line generic) | Partially covered | Covered | FR-A018; Admin: Overview | TRN-SCR-A018 |
| A019 | Admin | Read signals; review observed signal (FR-A019; doc 33 line generic) | Partially covered | Covered | FR-A019; Admin: Discovery | TRN-SCR-A019 |
| A020 | Admin | List needs and verification state; confirm/reject need with evidence (FR-A020; doc 33 line generic) | Partially covered | Covered | FR-A020; Admin: Discovery | TRN-SCR-A020 |
| A021 | Admin | Read matches with limitations; recompute readiness-gated matching (FR-A021; doc 33 line generic) | Partially covered | Covered | FR-A021; Admin: Discovery | TRN-SCR-A021 |
| A022 | Admin | Read prioritized opportunities; recalculate score (FR-A022; doc 33 line generic) | Partially covered | Covered | FR-A022; Admin: Discovery | TRN-SCR-A022 |
| A023 | Admin | Plans, schedule, scope, progress, evidence filters, scoring versions, simulation before activation (FR-A023; doc 33 line generic) | Partially covered | Covered | FR-A023; Admin: Discovery | TRN-SCR-A023 |
| A024 | Admin | List professional contacts and sources; queue permitted discovery; optional licensed API pilot (off by default) (FR-A024; doc 33 line generic) | Partially covered | Covered | FR-A024; Admin: Discovery | TRN-SCR-A024 |
| A025 | Admin | List verification work; verify provenance and channel; correct contact record (FR-A025; doc 33 line generic) | Partially covered | Covered | FR-A025; Admin: Discovery | TRN-SCR-A025 |
| A026 | Admin | Controlled merge; update role hypotheses and mappings (FR-A026; doc 33 line generic) | Partially covered | Covered | FR-A026; Admin: Discovery | TRN-SCR-A026 |
| A027 | Admin | Read prioritized opportunities; accept/reject with evidence; alerts (FR-A027; doc 33 line generic) | Partially covered | Covered | FR-A027; Admin: Discovery | TRN-SCR-A027 |
| A028 | Admin | Read alerts; set approval thresholds (FR-A028; doc 33 line generic) | Partially covered | Covered | FR-A028; Admin: Discovery | TRN-SCR-A028 |
| A029 | Admin | List pipeline; create qualified deal; deal timeline; controlled stage transitions; verified closure; assign owner (FR-A029; doc 33 line generic) | Partially covered | Covered | FR-A029; Admin: Overview | TRN-SCR-A029 |
| A030 | Admin | Stage configuration; versioned stage/assignment policies; audited assignment (FR-A030; doc 33 line generic) | Partially covered | Covered | FR-A030; Admin: Overview | TRN-SCR-A030 |
| A031 | Admin | List form versions; publish forms and routing rules (FR-A031; doc 33 line generic) | Partially covered | Covered | FR-A031; Admin: Overview | TRN-SCR-A031 |
| A032 | Admin | Deal and account timeline; eligibility check (no send); scoped external invitation for verified contacts (FR-A032; doc 33 line generic) | Partially covered | Covered | FR-A032; Admin: Overview | TRN-SCR-A032 |
| A033 | Admin | Emergency pause; list workflows and executions; version definitions; pause executions and pending actions (FR-A033; doc 33 line generic) | Partially covered | Covered | FR-A033; Admin: Automation | TRN-SCR-A033 |
| A034 | Admin | Eligibility check; evidence-based draft; approve/reject; queue approved message with recheck at execution (FR-A034; doc 33 line generic) | Partially covered | Covered | FR-A034; Admin: Outreach & Marketing | TRN-SCR-A034 |
| A035 | Admin | Approved template inventory; versioned templates; approval queue (FR-A035; doc 33 line generic) | Partially covered | Covered | FR-A035; Admin: Outreach & Marketing | TRN-SCR-A035 |
| A036 | Admin | Configure via secret reference; test; SES or approved equivalent (FR-A036; doc 33 line generic) | Partially covered | Covered | FR-A036; Admin: Outreach & Marketing | TRN-SCR-A036 |
| A037 | Admin | Queue approved message (recheck at execution); verify and dedupe provider receipts; unified threads (email, later WhatsApp, chat) (FR-A037; doc 33 line generic) | Partially covered | Covered | FR-A037; Admin: Outreach & Marketing | TRN-SCR-A037 |
| A038 | Admin | List sequences/enrolments; enrol eligible contact; stop; pending actions; outstanding tasks (FR-A038; doc 33 line generic) | Partially covered | Covered | FR-A038; Admin: Follow-ups | TRN-SCR-A038 |
| A039 | Admin | Versioned allowed sequences; stop (FR-A039; doc 33 line generic) | Partially covered | Covered | FR-A039; Admin: Follow-ups | TRN-SCR-A039 |
| A040 | Admin | List appointments; book approved slot with conflict prevention; verify calendar updates (FR-A040; doc 33 line generic) | Partially covered | Covered | FR-A040; Admin: Follow-ups | TRN-SCR-A040 |
| A041 | Admin | Configure authorized calendar; free/busy and conflicts (FR-A041; doc 33 line generic) | Partially covered | Covered | FR-A041; Admin: Follow-ups | TRN-SCR-A041 |
| A042 | Admin | Funnel KPIs; outstanding tasks; update task outcome (FR-A042; doc 33 line generic) | Partially covered | Covered | FR-A042; Admin: Overview | TRN-SCR-A042 |
| A043 | Admin | Funnel KPIs and tasks for teams (FR-A043; doc 33 line generic) | Partially covered | Covered | FR-A043; Admin: Overview | TRN-SCR-A043 |
| A044 | Admin | List WABA/template metadata; connect WABA; sync approved templates; opt-in and template rules (FR-A044; doc 33 line generic) | Partially covered | Covered | FR-A044; Admin: Outreach & Marketing | TRN-SCR-A044 |
| A045 | Admin | Queue approved message on the same route as A037; provider verification challenge; dedupe receipts (FR-A045; doc 33 line generic) | Partially covered | Covered | FR-A045; Admin: Outreach & Marketing | TRN-SCR-A045 |
| A046 | Admin | Approved FAQ and retention; unified inbox; assign thread; versioned routing rules (FR-A046; doc 33 line generic) | Partially covered | Covered | FR-A046; Admin: Objections | TRN-SCR-A046 |
| A047 | Admin | Read incidents; resolve after review (FR-A047; doc 33 line generic) | Partially covered | Covered | FR-A047; Admin: Automation | TRN-SCR-A047 |
| A048 | Admin | Permitted organizational social signals; licensed public data only (FR-A048; doc 33 line generic) | Partially covered | Covered | FR-A048; Admin: Discovery | TRN-SCR-A048 |
| A049 | Admin | Configure permitted social sources (FR-A049; doc 33 line generic) | Partially covered | Covered | FR-A049; Admin: Discovery | TRN-SCR-A049 |
| A050 | Admin | List content and versions; approved-knowledge draft; revised version (FR-A050; doc 33 line generic) | Partially covered | Covered | FR-A050; Admin: Outreach & Marketing | TRN-SCR-A050 |
| A051 | Admin | Approval queue; approve a specific content version (FR-A051; doc 33 line generic) | Partially covered | Covered | FR-A051; Admin: Outreach & Marketing | TRN-SCR-A051 |
| A052 | Admin | Scheduled publications; schedule approved; provider status; cancel pending (FR-A052; doc 33 line generic) | Partially covered | Covered | FR-A052; Admin: Outreach & Marketing | TRN-SCR-A052 |
| A053 | Admin | Configure social account; cancel pending; publish status (FR-A053; doc 33 line generic) | Partially covered | Covered | FR-A053; Admin: Outreach & Marketing | TRN-SCR-A053 |
| A054 | Admin | SEO issues and metrics; queue permitted audit; authorized metrics only (FR-A054; doc 33 line generic) | Partially covered | Covered | FR-A054; Admin: Outreach & Marketing | TRN-SCR-A054 |
| A055 | Admin | Assign approved SEO action (FR-A055; doc 33 line generic) | Partially covered | Covered | FR-A055; Admin: Outreach & Marketing | TRN-SCR-A055 |
| A056 | Admin | Read pages; create draft page (FR-A056; doc 33 line generic) | Partially covered | Covered | FR-A056; Admin: Outreach & Marketing | TRN-SCR-A056 |
| A057 | Admin | Publish approved page (FR-A057; doc 33 line generic) | Partially covered | Covered | FR-A057; Admin: Outreach & Marketing | TRN-SCR-A057 |
| A058 | Admin | List campaigns; create draft (FR-A058; doc 33 line generic) | Partially covered | Covered | FR-A058; Admin: Outreach & Marketing | TRN-SCR-A058 |
| A059 | Admin | Approval queue; approve campaign version and spending; suspend (FR-A059; doc 33 line generic) | Partially covered | Covered | FR-A059; Admin: Outreach & Marketing | TRN-SCR-A059 |
| A060 | Admin | Ad drafts; spend and performance; explicit launch/pause (FR-A060; doc 33 line generic) | Partially covered | Covered | FR-A060; Admin: Outreach & Marketing | TRN-SCR-A060 |
| A061 | Admin | Launch within cap; pause via authorized provider (FR-A061; doc 33 line generic) | Partially covered | Covered | FR-A061; Admin: Outreach & Marketing | TRN-SCR-A061 |
| A062 | Admin | List events; create; verify attendance (FR-A062; doc 33 line generic) | Partially covered | Covered | FR-A062; Admin: Outreach & Marketing | TRN-SCR-A062 |
| A063 | Admin | Reminder policy (FR-A063; doc 33 line generic) | Partially covered | Covered | FR-A063; Admin: Outreach & Marketing | TRN-SCR-A063 |
| A064 | Admin | Review; approve or reject referral (FR-A064; doc 33 line generic) | Partially covered | Covered | FR-A064; Admin: Outreach & Marketing | TRN-SCR-A064 |
| A065 | Admin | Read versions; generate draft (FR-A065; doc 33 line generic) | Partially covered | Covered | FR-A065; Admin: Closure | TRN-SCR-A065 |
| A066 | Admin | Approve exact version (FR-A066; doc 33 line generic) | Partially covered | Covered | FR-A066; Admin: Closure | TRN-SCR-A066 |
| A067 | Admin | Read quotes; create price snapshot (FR-A067; doc 33 line generic) | Partially covered | Covered | FR-A067; Admin: Closure | TRN-SCR-A067 |
| A068 | Admin | Approve quote and discount (FR-A068; doc 33 line generic) | Partially covered | Covered | FR-A068; Admin: Closure | TRN-SCR-A068 |
| A069 | Admin | Negotiation state; record objection or proposed terms (FR-A069; doc 33 line generic) | Partially covered | Covered | FR-A069; Admin: Objections | TRN-SCR-A069 |
| A070 | Admin | Review non-standard terms (FR-A070; doc 33 line generic) | Partially covered | Covered | FR-A070; Admin: Objections | TRN-SCR-A070 |
| A071 | Admin | List contracts/signatures; generate draft; verify signature receipt (FR-A071; doc 33 line generic) | Partially covered | Covered | FR-A071; Admin: Closure | TRN-SCR-A071 |
| A072 | Admin | Approve legal version (FR-A072; doc 33 line generic) | Partially covered | Covered | FR-A072; Admin: Closure | TRN-SCR-A072 |
| A073 | Admin | Payment reconciliation; create approved invoice; verify receipt and amount; close only on verified evidence (FR-A073; doc 33 line generic) | Partially covered | Covered | FR-A073; Admin: Closure | TRN-SCR-A073 |
| A074 | Admin | Verify receipt; reconcile events; prevent double allocation (FR-A074; doc 33 line generic) | Partially covered | Covered | FR-A074; Admin: Closure | TRN-SCR-A074 |
| A075 | Admin | List onboarding; complete authorized step (FR-A075; doc 33 line generic) | Partially covered | Covered | FR-A075; Admin: Follow-ups | TRN-SCR-A075 |
| A076 | Admin | Assign handoff owner and SLA (FR-A076; doc 33 line generic) | Partially covered | Covered | FR-A076; Admin: Follow-ups | TRN-SCR-A076 |
| A077 | Admin | Partner pipeline; create partner; pilot record; approved stage transitions (FR-A077; doc 33 line generic) | Partially covered | Covered | FR-A077; Admin: Follow-ups | TRN-SCR-A077 |
| A078 | Admin | Approved pilot stage transition (FR-A078; doc 33 line generic) | Partially covered | Covered | FR-A078; Admin: Follow-ups | TRN-SCR-A078 |
| A079 | Admin | Renewal calendar; review renewal opportunity (FR-A079; doc 33 line generic) | Partially covered | Covered | FR-A079; Admin: Follow-ups | TRN-SCR-A079 |
| A080 | Admin | Approved renewal reminder policy (FR-A080; doc 33 line generic) | Partially covered | Covered | FR-A080; Admin: Follow-ups | TRN-SCR-A080 |
| A081 | Admin | Record loss and stop follow-ups; authorized correction; feedback history (FR-A081; doc 33 line generic) | Partially covered | Covered | FR-A081; Admin: Follow-ups | TRN-SCR-A081 |
| A082 | Admin | Realized revenue and attribution (FR-A082; doc 33 line generic) | Partially covered | Covered | FR-A082; Admin: Overview | TRN-SCR-A082 |
| A083 | Admin | Versioned KPI definitions (FR-A083; doc 33 line generic) | Partially covered | Covered | FR-A083; Admin: Overview | TRN-SCR-A083 |
| A084 | Admin | Capture correction; feedback history; queue evaluation; results (FR-A084; doc 33 line generic) | Partially covered | Covered | FR-A084; Admin: Automation | TRN-SCR-A084 |
| A085 | Admin | Read competitor events (FR-A085; doc 33 line generic) | Partially covered | Covered | FR-A085; Admin: Discovery | TRN-SCR-A085 |
| A086 | Admin | Register approved monitor (FR-A086; doc 33 line generic) | Partially covered | Covered | FR-A086; Admin: Discovery | TRN-SCR-A086 |
| A087 | Admin | Forecast and assumptions (labelled estimate) (FR-A087; doc 33 line generic) | Partially covered | Covered | FR-A087; Admin: Overview | TRN-SCR-A087 |
| A088 | Admin | Versioned assumptions (FR-A088; doc 33 line generic) | Partially covered | Covered | FR-A088; Admin: Overview | TRN-SCR-A088 |
| A089 | Admin | Scoped approval queue; aggregate administration view; record scoped approval decisions (FR-A089; doc 33 line generic) | Partially covered | Covered | FR-A089; Admin: Overview | TRN-SCR-A089 |
| A090 | Admin | Release readiness; approve only after gates (FR-A090; doc 33 line generic) | Partially covered | Covered | FR-A090; Admin: Automation | TRN-SCR-A090 |
| A091 | Admin | Organization-level insurance pilots; create (FR-A091; doc 33 line generic) | Partially covered | Covered | FR-A091; Admin: Follow-ups | TRN-SCR-A091 |
| A092 | Admin | Approve lawful institutional pilot (FR-A092; doc 33 line generic) | Partially covered | Covered | FR-A092; Admin: Follow-ups | TRN-SCR-A092 |
| A093 | Admin | Read opportunities; record request (FR-A093; doc 33 line generic) | Partially covered | Covered | FR-A093; Admin: Follow-ups | TRN-SCR-A093 |
| A094 | Admin | Approve integration scope (FR-A094; doc 33 line generic) | Partially covered | Covered | FR-A094; Admin: Follow-ups | TRN-SCR-A094 |
| A095 | Admin | Read rollout; update deployment progress (FR-A095; doc 33 line generic) | Partially covered | Covered | FR-A095; Admin: Follow-ups | TRN-SCR-A095 |
| A096 | Admin | Approve readiness for expansion (FR-A096; doc 33 line generic) | Partially covered | Covered | FR-A096; Admin: Follow-ups | TRN-SCR-A096 |
| A097 | Admin | Read planned offerings internally (FR-A097; doc 33 line generic) | Partially covered | Covered | FR-A097; Admin: Overview | TRN-SCR-A097 |
| A098 | Admin | Approve launch after readiness validation (FR-A098; doc 33 line generic) | Partially covered | Covered | FR-A098; Admin: Overview | TRN-SCR-A098 |
| A099 | Admin | List authorized tenants; provision tenant; activate/suspend/offboard; list and provision startups (FR-A099; doc 33 line generic) | Partially covered | Covered | FR-A099; Admin: Automation | TRN-SCR-A099 |
| A100 | Admin | List templates; create draft; validate, approve, apply, retire; domain status; request verified brand domain (FR-A100; doc 33 line generic) | Partially covered | Covered | FR-A100; Admin: Automation | TRN-SCR-A100 |
| A101 | Admin | List plans; approve rate revision; list subscriptions; start/change/suspend/cancel; list service invoices (FR-A101; doc 33 line generic) | Partially covered | Covered | FR-A101; Admin: Automation | TRN-SCR-A101 |
| A102 | Admin | List plans; generate or dry-run; approve/start/pause/stop (FR-A102; doc 33 line generic) | Partially covered | Covered | FR-A102; Admin: Automation | TRN-SCR-A102 |
| A103 | Admin | List jobs; create intent; validate artefact; approve/cancel/expire; export link (FR-A103; doc 33 line generic) | Partially covered | Covered | FR-A103; Admin: Automation | TRN-SCR-A103 |
| A104 | Admin | List bids; create bid; update checklist; approve, record human submission, withdraw, record award (FR-A104; doc 33 line generic) | Partially covered | Covered | FR-A104; Admin: Closure | TRN-SCR-A104 |
| A105 | Admin | List orders; create; edit draft; approve/issue/cancel/complete; record actual fulfilment (FR-A105; doc 33 line generic) | Partially covered | Covered | FR-A105; Admin: Closure | TRN-SCR-A105 |
| A106 | Admin | List own notifications; mark read/archive (FR-A106; doc 33 line generic) | Partially covered | Covered | FR-A106; Admin: global and identity | TRN-SCR-A106 |
| A107 | Admin | Configure tenant/startup website template, verified domain, locales, page blocks, claims, forms and draft revisions. | Partially covered | Covered | FR-A107; Admin: Outreach & Marketing | TRN-SCR-A107 |
| A108 | Admin | Private preview, separation of duties, approve immutable hash, atomic publication pointer, rollback and scoped aggregate analytics; existing campaign/event dashboards supply analytics. | Partially covered | Covered | FR-A108; Admin: Outreach & Marketing | TRN-SCR-A108 |
| A109 | new | Define events, timers, webhooks independently of workflow design; test synthetic event; sandbox replay; enable/pause (FR-A109) | Not covered | Covered (SM-UX-UAT) | FR-A109; Admin: Automation | TRN-SCR-A109 |
| A110 | new | Inspect concurrent runs and step history; pause/resume (revalidate policy); request retry only after reconciliation; cancel; export evidence (FR-A110) | Not covered | Covered (SM-UX-UAT) | FR-A110; Admin: Automation | TRN-SCR-A110 |
| A111 | new | Resolve conflicting actions across workflows on the same relationship; hold, merge, choose, escalate (FR-A111) | Not covered | Covered (SM-UX-UAT) | FR-A111; Admin: Automation | TRN-SCR-A111 |
| A112 | new | Govern post-onboarding changes: compare, simulate, approve, publish, revert future config (FR-A112) | Not covered | Covered (SM-UX-UAT) | FR-A112; Admin: Automation | TRN-SCR-A112 |
| A113 | new | Govern reusable templates and node schemas: search, clone, configure, test, approve, publish, deprecate (FR-A113) | Not covered | Covered (SM-UX-UAT) | FR-A113; Admin: Automation | TRN-SCR-A113 |

### 8.3.3.3 Document 34

| Aspect | Section | Summary | Status | Blueprint location | Action | New IDs |
|---|---|---|---|---|---|---|
| 34-01 | Purpose and operating boundary | Common core (purpose, boundary, 147 interfaces, retained/expansion counts) | Covered | Part 0 §0.2; Part 1 §1.1 | Common core: see document 01/02 coverage |  |
| 34-02 | Service definition | Service plans configurable per product: self-service, managed, enterprise; startup/user limits, research/AI/communication quota, support coverage | Conflict | DEC-047 (Starter/Growth/Scale); US-2001/2005 | CONFLICT-485; service model × archetype matrix | §8.3.5.13.1 |
| 34-03 | Service definition | Eligibility: verify legal identity, authorized admin, intended purpose, permitted jurisdiction; reject prohibited use | Partially covered | BRL-SVC-01; US-2002 | Purpose and jurisdiction due-diligence checklist added | CSO-02; FR-ENH-J-008 |
| 34-04 | Service definition | Managed service: authorized tasks, approvals, data handling, excluded regulated actions; scoped, audited staff support; signed responsibility matrix | Not covered | DEC-056 (support grant only) | Managed-service scope and RACI added | FR-ENH-J-007; GAP-489 |
| 34-05 | Service definition | Commercial terms: separate subscription, onboarding, usage, managed fees; disclose taxes and pass-through costs; investment compensation → legal review | Partially covered | BRL-SVC-07; DEC-047; US-2006 | Fee-type structure and disclosure rules added; investment clause N/A (CONFLICT-489) | §8.3.5.13.2 |
| 34-06 | Client onboarding | Provision: independent tenant, client admin, plan, trial; startup legal entities and memberships | Covered | A099; US-2002; BRL-SVC-01/05 | — |  |
| 34-07 | Client onboarding | Configure: template, offerings, approved knowledge, filters, workflows, language, time zone, budget; validation + dry run | Covered | W33, A100, A112; US-2003/2004/2010 | 'Investment thesis' option dropped (CONFLICT-489) |  |
| 34-08 | Client onboarding | Website: domain ownership/TLS, approved brand and publication; public/portal separation | Covered | BRL-TEN-10; CFG-05; RB-010 | — |  |
| 34-09 | Client onboarding | Integrations: client-owned or platform-managed authorized accounts; vault references, quotas, sender identity; sandbox tests and consent policy | Partially covered | CFG-24; A008 | Client-owned vs platform-managed credential decision added to onboarding stage CSO-05 | CSO-05 |
| 34-10 | Client onboarding | Train and activate: train client admins, UAT and quality checks, approval, supervised automation; trial expiry prevents dispatch | Partially covered | Part 8.2 (P13 1 h SP); BRL-SVC-05 | Client admin learning journey LJ-13 and activation checklist | LJ-13; CSO-06 |
| 34-11 | Service delivery and SLA | Availability: proposed 99.5% monthly for agreed core service, eligible successful requests; contract exclusions and maintenance windows; no guarantee until measured | Partially covered | NFR-053/054; SLO-01/02; DEC-044 | SLA schedule template SLA-01…12 added | FR-ENH-J-005 |
| 34-12 | Service delivery and SLA | Response: P1 ack 15 min, P2 1 h during coverage, P3 next business day; timezone, holidays, escalation | Conflict | DEC-044 (S1 2 h, S2 8 bh, S3 3 bd, internal) | CONFLICT-484 | SLA-05 |
| 34-13 | Service delivery and SLA | Reliability: initial/growth workload and recovery targets; client-specific capacity/region separate | Partially covered | NFR-056/057; DEC-031 | Client-specific capacity/region as change request with estimate | SLA-08 |
| 34-14 | Service delivery and SLA | Reporting: monthly usage, workflow outcomes, incidents, cost, credits, service health; separate business outcomes from service revenue; tenant-scoped, reconciles ledger | Partially covered | RP-28; KPI-24 | Monthly service report spec | FR-ENH-J-006 |
| 34-15 | Service delivery and SLA | Billing: reserve before consumption; record charge, unit, rate, currency, provider evidence, reversal; invoice once per period | Covered | BRL-SVC-03/04/07; US-2005/2006; DEC-086 | — |  |
| 34-16 | Service delivery and SLA | Profitability: revenue less allocated infra, external usage, labour/support; estimated vs actual | Partially covered | KPI-23; Part 4.46.3 | Worked example + labour/support allocation | §8.3.5.13.7; FR-ENH-J-010 |
| 34-17 | Renewal and offboarding | Renewal: notify admin before expiry; explain usage/charges/options; no automatic upgrade | Partially covered | US-2006 (renewal date shown) | Renewal notice schedule and no-auto-upgrade rule | FR-ENH-J-009 |
| 34-18 | Renewal and offboarding | Suspend: pause paid actions and live workflows at expiry/breach; retain export/read access | Covered | BRL-SVC-05/06 | — |  |
| 34-19 | Renewal and offboarding | Export: verify requester, scope, retention; encrypted export with expiring link; manifest and delivery; client acknowledges | Covered | BRL-PRV-07; US-2009 | Client acknowledgement recorded (CSO-10) |  |
| 34-20 | Renewal and offboarding | Offboard: revoke tokens/grants/senders, stop scheduler jobs, remove domain and public snapshots, retention/legal hold, deletion; checklist | Partially covered | US-2009; BRL-SVC-06 | Offboarding verification checklist (no residual live access) | CSO-11; FR-ENH-J-009 |
| 34-21 | Business controls | AppNAI / MedMaarg / EduVerse / OrganicSpec / campaigns | Covered | Part 2.2 vertical routes; BRL-BID/ORD/ELG/MKT | Common core: see document 01/02 coverage |  |
| 34-22 | Completion and approval | Responsible lead / independent reviewer / product owner sign-off | Covered | EVR (Part 6.1 §6.1.5.4) | Common core |  |
| 34-23 | Service stage table | Contract/trial: tenant, legal entity, plan, product, users, data, support, regulatory boundaries; approved agreement and price card | Partially covered | US-2001/2002 | Stage gate CSO-01 | CSO-01 |
| 34-24 | Service stage table | Provision: tenant/startups, roles, domain, data region, budget, credentials; isolation tests | Covered | A099; US-2012 | — | CSO-03 |
| 34-25 | Service stage table | Configure/import: template, knowledge, dry-run import, ownership/duplicates; approved profile hash and reconciliation | Covered | US-2008; A103 | — | CSO-04 |
| 34-26 | Service stage table | Activation: simulation, role training, source/channel permissions, paid services disabled by default; client sign-off | Partially covered | BRL-AUT-04; NFR-037 | Client sign-off record | CSO-06 |
| 34-27 | Service stage table | Billing: meter with unique event key, rate-card charge, separate tax, reconcile invoice and receipt | Covered | BRL-SVC-04; US-2005/2006 | — |  |
| 34-28 | Service stage table | SLA: availability, support hours, response/recovery terms, exclusions, measurement formula based on tested capacity | Not covered | DEC-044 | SLA schedule | FR-ENH-J-005 |
| 34-29 | Service stage table | Support: time-limited approved grants, redacted diagnostics, escalation, incident status | Covered | DEC-056; Part 4.45 | — |  |
| 34-30 | Service stage table | Renew/offboard: usage review, stop workflows, revoke, export, retention; no post-offboard actions | Partially covered | US-2009 | Verification step | CSO-11 |
| 34-31 | Billing formula | Invoice = subscription + Σ eligible metered units × approved rate + authorized adjustments + tax; rate-card revision and original currency stored; idempotent usage key and invoice period | Covered | BRL-SVC-04/07; US-2005/2006 | Worked example added | §8.3.5.13.3 |
| 34-32 | Billing formula | Platform service revenue never counted as investor capital or commercial proceeds; investment success fees need legal approval | Covered | BRL-FIN-08; BRL-TEN-12 | Investment clause N/A |  |
| 34-33 | Service operation table | Trial/provision, activation, billing, profitability, support/offboarding (5 rows) | Covered | EP-20 stories | Consolidated in §8.3.5.13 |  |
| 34-34 | Optimization | Measure per tenant: usage, cost to serve, contribution margin, renewal | Partially covered | KPI-23/24 | Cohort report | FR-ENH-J-010 |
| 34-35 | Optimization | OPT-01-01, OPT-03-01…08, OPT-06-01, OPT-14-01, OPT-19-01, OPT-20-01…04 cited | Partially covered | see doc 36 rows | Mapped in §8.3.5.15.3 |  |
| 34-36 | Acceptance procedures | Task and operating cost estimates (low/base/high per task, predecessor chain, incremental optimization effort) | Partially covered | Part 8.1 §8.1.6 | Incremental optimization effort rule | §8.3.5.14.8 |
| 34-37 | Acceptance procedures | Cost metering and anomaly response (duplicates, missing attribution, exhausted quota) | Covered | NFR-014/093; BRL-SVC-04 | — | TC-ENH-J-038 |
| 34-38 | Acceptance procedures | Configurable owned startups: 26th startup via template | Covered | BRL-TEN-11 | 'funding goals' removed (CONFLICT-489) | TC-ENH-J-014 |
| 34-39 | Acceptance procedures | Independent client tenant lifecycle: provision → grant → activate → offboard → access after revoke | Covered | US-2012 | — |  |
| 34-40 | Acceptance procedures | Outcome economics: cost per qualified opportunity and verified closure | Covered | KPI-22 | — | TC-ENH-J-012 |
| 34-41 | Acceptance procedures | Reusable business templates: two profiles | Covered | US-2004 | — |  |
| 34-42 | Acceptance procedures | Cross-border and regional decision sign-off | Covered | BRL-ELG-05; BRL-APR-06 | — |  |
| 34-43 | Acceptance procedures | Retention, portability and deletion of tenant data and derivatives | Covered | US-2009; BRL-PRV-04/05 | — |  |
| 34-44 | Acceptance procedures | Entitlement and trial controls | Covered | US-2011 (AP-09) | — |  |
| 34-45 | Acceptance procedures | Usage ledger and invoice reconciliation (replay, adjustment) | Covered | US-2005/2006; KPI-24 | — |  |
| 34-46 | Acceptance procedures | Service profitability and TCO | Partially covered | KPI-23 | Worked example | TC-ENH-J-020 |
| 34-47 | Acceptance procedures | SLA and support commitments: simulate incident support and customer notification; no claim before measured validation | Partially covered | DEC-044; Part 4.43.4 | SLA validation procedure | TC-ENH-J-040 |
| 34-48 | Acceptance procedures | Offboarding and client independence | Covered | US-2009/2012 | — | TC-ENH-J-042 |
| 34-49 | Acceptance procedures | Resource and deployment approval (estimate increments before promising SLA) | Partially covered | Part 8.1 | Rule added | §8.3.5.14.8 |
| 34-50 | Expansion scope | SaaS service lifecycle: separate applicant/service identity; verify company/admin authority; entitlement and budget; plan changes; controlled offboarding | Covered | EP-20; BRL-SVC-01…07 | — |  |
| 34-51 | Expansion scope | Applicant draft boundary: opaque expiring reference; isolated intake storage; no mutation of active startup; transactional idempotent handoff | Covered | BRL-SVC-02; US-2002 | — |  |
| 34-52 | Expansion scope | Nine new interfaces W31–W34, A109–A113 | Covered | Part 2.1/2.5 | Common core |  |

### 8.3.3.4 Document 35

| Aspect | Section | Summary | Status | Blueprint location | Action | New IDs |
|---|---|---|---|---|---|---|
| 35-01 | Purpose and operating boundary | Common core | Covered | Part 0/1 | Common core: see document 01/02 coverage |  |
| 35-02 | Maintenance operating model | Ownership: product owner, engineering lead, QA, security, DevOps, AI, support owners; primary/backup; named roster and escalation | Partially covered | Part 8.1 §8.1.5 RACI; Part 4.43.2 on-call | BAU maintenance roster added | MNT-R01 |
| 35-03 | Maintenance operating model | Intake: defect, feedback, security finding, provider change with impact/scope/evidence/priority; no uncontrolled production fix | Partially covered | Part 8.2 §8.2.2.4 CR process; Part 4.43 | Unified intake classes | §8.3.5.14.1 |
| 35-04 | Maintenance operating model | Prioritize: critical confidentiality/financial immediately; high blockers next; enhancements by impact/effort/risk | Partially covered | Severity matrix (Part 4.43.1) | Priority matrix | §8.3.5.14.1 |
| 35-05 | Maintenance operating model | Change management: affected UI/API/table/workflow/test, compatibility, cost; traceability updated before deployment | Covered | Part 8.2 §8.2.2.4 (BR-S134) | — | FR-ENH-J-022 |
| 35-06 | Maintenance operating model | Emergency fix: contain first, reviewed hotfix artefact, critical smoke, deviation recorded, follow-up review | Partially covered | Part 4.3 §4.38 rollback; incident lifecycle | Hotfix procedure | §8.3.5.14.1 |
| 35-07 | Recurring maintenance | Daily review: alerts, failed workflows, budgets, approvals, financial exceptions, public content incidents | Partially covered | Part 4.46.6, 4.47 (automated) | Daily operations review MNT-D01…D06 | §8.3.5.14.2 |
| 35-08 | Recurring maintenance | Weekly: defects, queue latency, AI samples, source failures, security alerts, support backlog | Partially covered | Part 4.46.6 weekly FinOps slot | MNT-W01…W07 | §8.3.5.14.2 |
| 35-09 | Recurring maintenance | Monthly: provider entitlements/cost, dependency vulnerabilities, access grants, tenant profitability, capacity | Partially covered | Part 4.46.6 monthly FinOps; NFR-067 | MNT-M01…M10 | §8.3.5.14.2 |
| 35-10 | Recurring maintenance | Quarterly: restore drill, security scenario review, AI regression benchmark, template review, client feedback analysis | Partially covered | Part 4.47 quarterly drills | MNT-Q01…Q07 | §8.3.5.14.2 |
| 35-11 | Recurring maintenance | Annual/material change: threat model, retention, service terms, DR, architecture vs demand | Partially covered | Part 4.47 annual | MNT-A01…A05 | §8.3.5.14.2 |
| 35-12 | Lifecycle changes | AI model/prompt: benchmark old/new, cost/latency; approve revision and canary; rollback; no self-modification | Covered | NFR-033; BRL-AI-09; Part 7.3 version pinning | — | LC-01 |
| 35-13 | Lifecycle changes | Knowledge: freshness, claim approval, revoke outdated claims, rebuild scoped index; revoked content not retrievable | Covered | BRL-MKT-01; Part 3.3 vector lifecycle | — | LC-02 |
| 35-14 | Lifecycle changes | Provider: deprecation/pricing monitoring; replacement adapter, licence, entitlement; migrate with fallback and reconciliation | Partially covered | RSK-039/080; Part 7.4 procurement gates | Provider change procedure | LC-03 |
| 35-15 | Lifecycle changes | Database: query plans, vacuum, indexes, storage; expand/backfill/validate/switch/contract | Covered | Part 4.3 §4.37.2 | — | LC-04 |
| 35-16 | Lifecycle changes | Frontend: browser/accessibility, mobile performance, stale cache; public and private UI independently | Covered | NFR-088/098; NFR-001 | — | LC-05 |
| 35-17 | Lifecycle changes | Retire feature: usage, dependency, contract, retention; notify clients, export, disable, remove after window; no orphan jobs/endpoints/credentials | Not covered | — | Feature lifecycle | FR-ENH-J-012; LC-06 |
| 35-18 | Improvement measurement | Business outcomes: qualified rate, response, conversion, verified outcomes, cost per outcome; AI score ≠ conversion | Covered | KPI-01…31; OKR (Part 1) | — |  |
| 35-19 | Improvement measurement | Engineering outcomes: lead time, change failure, recovery, critical defects, coverage; trends not punitive | Covered | NFR-083 (DORA); NFR-082 | Non-punitive rule added | §8.3.5.14.6 |
| 35-20 | Improvement measurement | Service economics per tenant/plan: revenue, cost, margin, churn, support burden; finance approves pricing | Partially covered | KPI-23/24 | Churn and support burden | FR-ENH-J-010 |
| 35-21 | Improvement measurement | Learning loop: hypothesis, metric, safe cohort, simulate, approve, compare, retain or roll back | Partially covered | BRL-MKT-10 (experiments) | Improvement record | §8.3.5.14.6 |
| 35-22 | Business controls | AppNAI / MedMaarg / EduVerse / OrganicSpec / campaigns | Covered | Vertical routes | Common core |  |
| 35-23 | Completion and approval | Sign-off roles | Covered | EVR | Common core |  |
| 35-24 | Cadence table | Daily: alerts, queue backlog, failed/uncertain actions, cost cap, provider availability, unauthorized access signals | Partially covered | Part 4.41 alerts | MNT-D01…D06 |  |
| 35-25 | Cadence table | Weekly: source coverage, stale contacts/claims, failed conversions, data quality, workflow effectiveness | Partially covered | KPI-27 | MNT-W |  |
| 35-26 | Cadence table | Monthly: dependencies/CVEs, AI regression, quotas and unit economics, DB indexes, backup restore evidence | Partially covered | Part 4.46.6/4.47 | MNT-M |  |
| 35-27 | Cadence table | Quarterly: restore/rollback rehearsal, capacity, access recertification, client contract/SLA and retention review | Partially covered | Part 4.47; Part 4.1 access reviews | MNT-Q |  |
| 35-28 | Cadence table | Before any update: impact, compatibility, tests, migration/rollback, approval | Covered | Part 8.2 §8.2.2.4; Part 4.3 | — |  |
| 35-29 | Cadence table | After incident: RCA, fix, regression test, control gaps, stakeholder notice | Covered | Part 4.43.5 postmortems | — |  |
| 35-30 | Versioning rules | Version profiles, prompts, knowledge snapshots, workflows independently of document publication; AI/provider update never changes policy automatically | Covered | BRL-AUT-03; NFR-033; DEC-061 | — |  |
| 35-31 | Versioning rules | Deprecate via notice, compatibility plan, export, rollback; retain audit and legal hold | Not covered | — | Feature lifecycle | FR-ENH-J-012 |
| 35-32 | Versioning rules | Prioritize fixes by business impact, security, financial integrity — not feature count | Partially covered | Part 4.43.1 | Priority matrix | §8.3.5.14.1 |
| 35-33 | Evidence record | Responsible/reviewer, artefact, decision, remediation, business acceptance | Covered | EVR | Common core |  |
| 35-34 | Maintenance schedule | Daily: workflow failures, uncertain results, budget, sender health; reconcile before retry | Covered | RB-003; RB-006 | — |  |
| 35-35 | Maintenance schedule | Weekly: source freshness, AI evidence quality, opt-outs, defect backlog, cost per qualified outcome, client support | Partially covered | Part 4.45 metrics | MNT-W |  |
| 35-36 | Maintenance schedule | Monthly: subscription/usage ledger, dependency updates, backups/restore sample, performance trends, approved business claims | Partially covered | Part 4.47 monthly | MNT-M |  |
| 35-37 | Maintenance schedule | Before any change: entitlement, migration compatibility, prompt regression, scope isolation, feature flags, rollback; mapped tests and QC | Covered | Part 4.3 pipeline; Part 4.36 | — |  |
| 35-38 | Maintenance schedule | Lifecycle: deprecate via approved migration and client communication; preserve financial/audit; no cross-client disclosure | Not covered | — | Feature lifecycle | FR-ENH-J-012 |
| 35-39 | Optimization | Cycle measure → diagnose → simulate → approve → implement → verify → standardize; retain before/after; reverse unsafe | Not covered | — | Continuous optimization cycle | §8.3.5.15.8 |
| 35-40 | Optimization | OPT-03-01, 05-01, 10-01, 13-01…04, 14-01, 17-01, 18-01, 20-01 cited | Partially covered | doc 36 rows | Mapped | §8.3.5.15.3 |
| 35-41 | Acceptance protocol | Baseline, candidate, scope, dataset, digest, cost, outcome, reviewer; missing = Pending; reject mandatory regressions; reversible rollback; reconcile before resume | Partially covered | EVR rules | Benchmark record | FR-ENH-J-020 |
| 35-42 | Acceptance procedures | Provider entitlement and schema change | Partially covered | Part 7.4 procurement gates PG-01…10 | LC-03 procedure | TC-ENH-J-047 |
| 35-43 | Acceptance procedures | Prompt/model version regression | Covered | NFR-033; Part 6.4 | — |  |
| 35-44 | Acceptance procedures | Dependency and technical debt inventory | Partially covered | NFR-084 | Tech-debt register | TC-ENH-J-048 |
| 35-45 | Acceptance procedures | Change impact assessment before merge | Covered | Part 8.2 §8.2.2.4 | Impact record automation | TC-ENH-J-049 |
| 35-46 | Acceptance procedures | Operational knowledge and handover: operator follows synthetic troubleshooting without developer | Not covered | — | TRN-EX-12 | TC-ENH-J-051 |
| 35-47 | Acceptance procedures | Artifact and version consistency: manifests and catalogue hashes; no stale artefact as evidence | Partially covered | EVR digest rule | Manifest validator | FR-ENH-J-015 |
| 35-48 | Resource and deployment approval | Keep PD baseline; estimate increments per discipline; approval before promising cost/SLA; staging load/security/migration/rollback/recovery tests | Partially covered | Part 8.1; Part 8.2 go-live | Rule added | §8.3.5.14.8 |
| 35-49 | Expansion scope | Maintenance: version templates/config; deprecate without changing active executions; update catalogues, routes, fixtures, release inventory together | Partially covered | BRL-AUT-03 | Inventory co-update rule | §8.3.5.14.4 |

### 8.3.3.5 Document 36: non-control aspects

Controls (104), OKPIs (35), scenarios (24) and UX-QC (10) are listed in full in Part 8.3c §8.3.5.15 with their status, because their mapping tables are the enhancement itself.

| Aspect | Section | Summary | Status | Blueprint location | Action | New IDs |
|---|---|---|---|---|---|---|
| 36-DIM-01 | Weighted scorecard | OPT-01 Security weight 14%; accountable Security lead | Not covered | — | Dimension added with weight and blueprint owner | OPT-01 |
| 36-DIM-02 | Weighted scorecard | OPT-02 Performance weight 8%; accountable Frontend and backend leads | Not covered | — | Dimension added with weight and blueprint owner | OPT-02 |
| 36-DIM-03 | Weighted scorecard | OPT-03 Cost weight 12%; accountable FinOps lead | Not covered | — | Dimension added with weight and blueprint owner | OPT-03 |
| 36-DIM-04 | Weighted scorecard | OPT-04 Automation weight 12%; accountable Automation lead | Not covered | — | Dimension added with weight and blueprint owner | OPT-04 |
| 36-DIM-05 | Weighted scorecard | OPT-05 Stability weight 10%; accountable Reliability lead | Not covered | — | Dimension added with weight and blueprint owner | OPT-05 |
| 36-DIM-06 | Weighted scorecard | OPT-06 Scalability weight 5%; accountable Architect | Not covered | — | Dimension added with weight and blueprint owner | OPT-06 |
| 36-DIM-07 | Weighted scorecard | OPT-07 Architecture weight 4%; accountable Solution architect | Not covered | — | Dimension added with weight and blueprint owner | OPT-07 |
| 36-DIM-08 | Weighted scorecard | OPT-08 Database weight 3%; accountable Database lead | Not covered | — | Dimension added with weight and blueprint owner | OPT-08 |
| 36-DIM-09 | Weighted scorecard | OPT-09 API & Integration weight 3%; accountable Integration lead | Not covered | — | Dimension added with weight and blueprint owner | OPT-09 |
| 36-DIM-10 | Weighted scorecard | OPT-10 AI Intelligence weight 5%; accountable AI lead | Not covered | — | Dimension added with weight and blueprint owner | OPT-10 |
| 36-DIM-11 | Weighted scorecard | OPT-11 Data Quality weight 3%; accountable Data steward | Not covered | — | Dimension added with weight and blueprint owner | OPT-11 |
| 36-DIM-12 | Weighted scorecard | OPT-12 Business Conversion weight 5%; accountable Product owner | Not covered | — | Dimension added with weight and blueprint owner | OPT-12 |
| 36-DIM-13 | Weighted scorecard | OPT-13 Maintainability weight 2%; accountable Engineering lead | Not covered | — | Dimension added with weight and blueprint owner | OPT-13 |
| 36-DIM-14 | Weighted scorecard | OPT-14 Reusability weight 2%; accountable Architect | Not covered | — | Dimension added with weight and blueprint owner | OPT-14 |
| 36-DIM-15 | Weighted scorecard | OPT-15 UI/UX weight 2%; accountable Design lead | Not covered | — | Dimension added with weight and blueprint owner | OPT-15 |
| 36-DIM-16 | Weighted scorecard | OPT-16 Development Productivity weight 2%; accountable CTO | Not covered | — | Dimension added with weight and blueprint owner | OPT-16 |
| 36-DIM-17 | Weighted scorecard | OPT-17 Testing & QC weight 3%; accountable QA lead | Not covered | — | Dimension added with weight and blueprint owner | OPT-17 |
| 36-DIM-18 | Weighted scorecard | OPT-18 Deployment & Recovery weight 2%; accountable DevOps lead | Not covered | — | Dimension added with weight and blueprint owner | OPT-18 |
| 36-DIM-19 | Weighted scorecard | OPT-19 Privacy & Compliance weight 2%; accountable Privacy and legal lead | Not covered | — | Dimension added with weight and blueprint owner | OPT-19 |
| 36-DIM-20 | Weighted scorecard | OPT-20 SaaS Profitability weight 1%; accountable Service owner | Not covered | — | Dimension added with weight and blueprint owner | OPT-20 |
| 36-01 | Operating architecture | Two independent products (public Website, portal, Admin each); share code, never operational data/credentials/queues/budgets; reuse PostgreSQL/React/Django/Celery/Valkey first | Covered | NFR-031; Part 3.1 | — |  |
| 36-02 | Operating architecture | Commercial outcomes measured only for the authorized startup; no revenue guarantee | Covered | BRL-FIN-06; Part 1 OKRs | — |  |
| 36-03 | Weighted scorecard | Weighted score = Σ(weight × approved score ÷ 10) ÷ Σ assessed weight × 100 | Not covered | — | Scorecard | §8.3.5.15.2; FR-ENH-J-013 |
| 36-04 | Weighted scorecard | Assessment coverage = assessed weight ÷ total weight | Not covered | — | Scorecard | §8.3.5.15.2 |
| 36-05 | Weighted scorecard | No score without evidence; zero-denominator ratios unassessed, not 100% | Not covered | — | Numeric rules | §8.3.5.15.2 |
| 36-06 | Weighted scorecard | Critical security/privacy/financial/mandatory delivery failures block irrespective of score | Partially covered | Part 8.2 §8.2.4.1 hard stops | G0 blocking gate | §8.3.5.15.1 |
| 36-07 | KPI matrix rules | Count-based negative controls record attempted test population even when zero | Not covered | — | OKPI rules | §8.3.5.15.4 |
| 36-08 | KPI matrix rules | Ratios use approved numerator/denominator; no rounding to hide failure | Partially covered | RPT-R1 (numerator/denominator shown) | OKPI rules | §8.3.5.15.4 |
| 36-09 | KPI matrix rules | Percentile tests need representative observations and agreed window | Partially covered | Part 4.2 §4.21 | OKPI rules | §8.3.5.15.4 |
| 36-10 | KPI matrix rules | Performance compares p95 and p99, error rate, throughput, resource cost | Covered | NFR-039/040 (p95+p99) | — |  |
| 36-11 | Admin optimization panel | Use existing Admin screens; cards security, latency, queue, cost, AI quality, freshness, conversion, service margin; filters tenant/startup/time/workflow/provider; scope and freshness visible; recommendations read-only until approved | Not covered | A089/A090 exist; no optimization cards | Optimization tab and cards | FR-ENH-J-013 |
| 36-12 | Admin optimization panel | Panel data sources: command centre, audit/jobs, cost/budget, health/incidents, AI quality, growth dashboard, revenue/attribution (7 groups of endpoints and growth_* sources) | Covered | A089, A009, A012, A014, A084, A042, A082 and their Part 3.2/3.3 contracts | growth_* names mapped to ENT names | §8.3.5.15.7 |
| 36-13 | Benchmarking | Smaller model / rules-first comparison | Covered | NFR-030 | Benchmark record | FR-ENH-J-020 |
| 36-14 | Benchmarking | Native vs paid research comparison | Covered | NFR-037; Part 7.4 | Benchmark record | FR-ENH-J-020 |
| 36-15 | Benchmarking | Caching and database indexing comparison | Partially covered | Part 3.3 index policy | Benchmark record | FR-ENH-J-020 |
| 36-16 | Benchmarking | Worker scaling / batch size comparison | Partially covered | Part 4.2 §4.27 | Benchmark record | FR-ENH-J-020 |
| 36-17 | Benchmarking | Reduced infrastructure comparison | Partially covered | Part 4.46.6 quarterly review | Benchmark record | FR-ENH-J-020 |
| 36-18 | Benchmarking | Synthetic first, then staging; same dataset/scope; warm-up, sample size, duration, environment documented | Not covered | — | Benchmark protocol | §8.3.5.15.8 |
| 36-19 | Continuous optimization | Measure → identify → diagnose → propose → simulate → approve → implement → verify → standardize/reverse; no automatic production deployment or financial action by the optimizer | Not covered | — | Cycle | §8.3.5.15.8 |
| 36-20 | Continuous optimization | Verification examples: scoped fixtures, parallel reservations, retry/replay, stale revisions, deterministic vs AI routing | Covered | Part 6 test families | — |  |
| 36-21 | Executable acceptance | Offline reference command and 100-task synthetic routing example (INR 100 vs INR 17.20; 82.8% illustrative) | Not applicable | Part 7.3 TCO | Illustrative only; reproduced as arithmetic check in TC-ENH-J-010 notes |  |
| 36-22 | Implementation acceptance | Evidence gate fail-closed (delete QC row, duplicate ID, mandatory N/A) | Partially covered | EVR; A090 | Validator | FR-ENH-J-015 |
| 36-23 | Implementation acceptance | Hierarchical budget controls (platform, tenant, startup, workflow) | Covered | BRL-AI-08; CFG-23 | — | TC-ENH-J-003 |
| 36-24 | Implementation acceptance | AI routing cost reproducible arithmetic | Covered | Part 7.3 | — |  |
| 36-25 | Implementation acceptance | Simulation side effects: no network, outbox send, charge or financial write | Covered | NFR-038; BRL-AUT-04 | — |  |
| 36-26 | Implementation acceptance | Availability and error budget: eligible minutes, exclusions, dependency failures | Covered | Part 4.40.2; §4.21 | — |  |
| 36-27 | Implementation acceptance | Numeric guardrail validation (NaN, infinity, negative counts/weights, invalid retries) | Not covered | — | Numeric rules | TC-ENH-J-055 |
| 36-28 | Implementation acceptance | Noisy neighbour protection | Covered | NFR-062 | — |  |
| 36-29 | Implementation acceptance | Model selection and token efficiency | Covered | NFR-030; Part 6.4 | — |  |
| 36-30 | Implementation acceptance | Classification quality with sample size; no claim from five synthetic documents | Covered | NFR-011 | — |  |
| 36-31 | Implementation acceptance | Outcome economics | Covered | KPI-22 | — |  |
| 36-32 | Implementation acceptance | Complete document inventory (36 Word files open) | Not applicable | Package QA | Done by the source-pack review |  |
| 36-33 | Implementation acceptance | Workbook source and formulas (24 original tabs) | Not applicable | Pack workbook not supplied | — |  |
| 36-34 | Implementation acceptance | Reference test integrity (skipped/failed separately; not product coverage) | Covered | Part 6.1 §6.1.5.5 | — |  |
| 36-35 | Implementation acceptance | Service profitability and TCO | Partially covered | KPI-23 | Worked example | TC-ENH-J-020 |
| 36-36 | Implementation acceptance | Authorization-safe cache key composition; public caches use public projection | Partially covered | NFR-020; Part 3.1 caching | Cache key standard | FR-ENH-J-016 |
| 36-37 | Implementation acceptance | Reject invalid weights, non-finite inputs, negative counts, out-of-range ratios; signed improvement metrics separate | Not covered | — | Numeric rules | §8.3.5.15.2 |
| 36-38 | Implementation acceptance | Fail-closed evidence inventory from reviewed immutable baseline; reject missing/extra/duplicate/mandatory N/A; edited register cannot define its own scope | Partially covered | EVR | Validator | FR-ENH-J-015 |
| 36-39 | Implementation acceptance | Optimization estimate reconciliation (385 PD / 149 items; 104 controls against existing tasks; no unverified savings) | Partially covered | Part 8.1 | Rule | §8.3.5.14.8 |
| 36-40 | Final decision controls | Evidence integrity: blank/whitespace evidence, executor = reviewer after trim/casefold, nonblank approval identity, artifact hashes; signed approvals via authenticated change management | Partially covered | EVR rule responsible ≠ reviewer | Normalized identity check | FR-ENH-J-015 |
| 36-41 | Final decision controls | Approval review effort 32.55 / 62.85 / 123.70 PD; subtract overlap | Partially covered | — | Rule | §8.3.5.14.8 |
| 36-42 | Final decision controls | Combined preflight: 1,188 records across 6 groups; CTO and product owner sign in release system | Conflict | A090 gate | CONFLICT-491 (1,188 vs 1,545) | §8.3.5.15.10 |
| 36-43 | Expansion | Apply 20 dimensions and 104 controls to expanded scope | Partially covered | — | Applied | §8.3.5.15 |
| 36-44 | Expansion | Nine new interfaces with purpose/acceptance | Covered | Part 2.1/2.5 | Common core |  |

### 8.3.3.6 Document 38

Listed in §8.3.4.1 (the reconciliation table is the register for document 38).

---

## 8.3.4 Catalogue reconciliation

### 8.3.4.1 Document 38 "All Numbers" against the blueprint (every number)

Rule applied: a difference is acceptable only when it is explained by (a) a different counting unit, (b) a documented DERIVED superset decision, (c) historical or package-only metrics that are not software scope, or (d) a recorded conflict with a proposed resolution.

| Aspect | Section | Inventory item (source value) | Status | Blueprint value | Explanation |
|---|---|---|---|---|---|
| 38-01 | §01 | Word documents (existing package): 36 | Covered | 2 used (BRD, FRD) + 36 reviewed in the source-pack review | Blueprint was built from documents 01/02 (byte-identical to the pack); the source-pack groups A…J review the rest |
| 38-02 | §01 | Companion Word documents: 2 (docs 37, 38) | Covered | Reviewed (doc 38 by this group) | Doc 37 worked example reviewed by its group |
| 38-03 | §01 | Documentation total with companions: 38 | Covered | 38 | — |
| 38-04 | §01 | Master management worksheets: 28 + 2 = 30 | Not applicable | 1 workbook (final/…Workbook_v1.0.xlsx) with its own sheet set | Pack worksheets are not supplied; the blueprint workbook is generated from Parts 0–9 (Part 10 assembly) |
| 38-05 | §01 | Website screen layouts: 30 + 4 = 34 | Covered | 34 (W01–W34) | Part 2.5 §2.43 |
| 38-06 | §01 | Admin screen layouts: 108 + 5 = 113 | Covered | 113 (A001–A113) | Part 2.5 §2.43 |
| 38-07 | §01 | Total UI layouts: 147 | Covered | 147 | Part 9.3 §9.3.4 |
| 38-08 | §01 | Frontend applications: 2 | Covered | 2 (`commercial-website-react`, `commercial-admin-react`) | NFR-001; Part 2.5 §2.40 |
| 38-09 | §01 | Independent backend / database: 1 / 1 | Covered | 1 Django modular monolith / 1 PostgreSQL | Part 3.1 |
| 38-10 | §01 | Business requirements: 71 + 5 = 76 | Conflict | 71 primary (66 BR-M + 5 cross-cutting BR-TENANT/WEB/AUTO/SVC/QA) + 140 BR-S | CONFLICT-487: the pack's 5 'added' BRs are the five cross-cutting B-* requirements, which the blueprint already counts inside 71; the pack's retained 71 cannot be decomposed into 66 + 5 other IDs |
| 38-11 | §01 | Functional requirements: 141 + 147 = 288 | Covered | 150 FR (147 screens + 3 OP) + 31 cross-cutting FR-XC + 147 FR-UX field specs | 141 = 138 SM-FR + 3 OP; 147 = SM-UX-FR (one per screen). Blueprint adds FR-W31…W34, FR-A109…A113 (GAP-019/DEC-033) and 31 cross-cutting FRs, so the blueprint superset is 328 IDs |
| 38-12 | §01 | API & adapter operations: 302 + 19 = 321 | Covered | 555 API operations + 20 adapters + 159 domain events (Part 3.2) | DEC-104: DERIVED superset; source catalogue not attached to BRD/FRD (GAP-001). The 19 SM-UX-API candidates map to Part 3.2 operations for W31–W34, A109–A113 (API group reconciles row by row) |
| 38-13 | §01 | Logical data entities: 149 + 6 = 155 | Covered | 199 logical entities (ENT-001…ENT-199) | DEC-087: DERIVED superset; the 6 sales_ui_* candidates map to ApplicationDraft, ConfigurationRevision, TriggerRevision, ConflictCase, TemplateRevision, ServiceRequest-equivalents in Part 3.3 §3.3.4.14/16 |
| 38-14 | §01 | Development work items: 149 + 13 = 162 | Covered | 21 epics, 230 user stories (Part 5); sprint plan (Part 8.1) | Different granularity: pack work items are engineering tasks; blueprint plans at story level |
| 38-15 | §01 | Product test specifications: 624 + 175 = 799 | Covered | 2,912 test cases (2,138 + 774 AI) + 48 VER; SM-UT/SM-UAT/SM-UX-UAT aliases | DEC-017 alias rule; Part 6.6 RTM |
| 38-16 | §01 | Quality controls: 235 + 10 = 245 | Partially covered | No QC-### register; quality-gate thresholds (Part 4.3 §4.33.4), DoD, go-live checklist GL-* | GAP-488: QC register reconciled by the QC/RTM group; OKPI-17 gate rule defined here |
| 38-17 | §01 | Engineering review decisions: 180 + 172 = 352 | Partially covered | 156 DEC + 70 ADR | Pack decisions are per-row approval decisions; the blueprint records binding decisions only. Approval records are evidence (EVR), not DEC rows |
| 38-18 | §02 | UI classification: Admin — Admin: 108 | Covered | 108 (A001–A108) | — |
| 38-19 | §02 | UI classification: Admin — Authorized Admin: 5 | Covered | 5 (A109–A113) | — |
| 38-20 | §02 | Website — Authenticated SaaS applicant: 1 (W33) | Covered | W33 applicant/client admin (R17) | Part 2.3 external surfaces |
| 38-21 | §02 | Website — Authenticated SaaS client: 1 (W34) | Covered | W34 (R17 own tenant) | — |
| 38-22 | §02 | Website — Authentication: 1 (W21) | Covered | W21 classified 'Portal' in Part 2.1 | Naming difference only; W21 is the portal sign-in |
| 38-23 | §02 | Website — Portal: 7 (W22–W28) | Covered | 7 | — |
| 38-24 | §02 | Website — Public: 15 | Covered | 15 (W01–W05, W07–W13, W19, W20, W31) | Doc 33 lists W17 and W30 as Public / Portal; Part 2.1 lists them Public: both pages are reachable from the portal shell, no rule changes |
| 38-25 | §02 | Website — Public / Portal: 8 | Covered | 8 (W06, W14–W18, W29, W32 per pack) | — |
| 38-26 | §02 | Website — Public / identity verification: 1 (W32) | Covered | W32 application with administrator verification (BRL-SVC-01) | — |
| 38-27 | §02 | Nine additional screens: W31–W34, A109–A113 | Covered | Same IDs | FR-W31…FR-A113 |
| 38-28 | §02 | HTTP operations including candidates: 304 | Covered | 555 (Part 3.2) | See row 'API & adapter operations' |
| 38-29 | §02 | Non-HTTP adapter operations: 17 | Covered | 20 adapters (Part 3.2) | Adapter count is per provider class, not per operation |
| 38-30 | §02 | Integration/plugin candidate review rows: 538 | Not applicable | F_integration_candidates.csv (group F) | Reconciled by group F (docs 16/21) |
| 38-31 | §02 | Retained operation-specific test variant records: 302 | Covered | Contract tests per Part 3.2 operation (Part 6.1) | One CT per operation (TC families per epic) |
| 38-32 | §03 | Candidate operations SM-UX-API-01…19: 19 | Covered | Part 3.2 operations for W31–W34, A109–A113 | Row-level mapping by the API group |
| 38-33 | §03 | Candidate entities sales_ui_*: 6 | Covered | ApplicationDraft, ConfigurationRevision, TriggerDefinition/Revision, ConflictCase, WorkflowTemplate revision, SupportRequest | DEC-087 |
| 38-34 | §04 | Unit tests: 66 + 9 = 75 | Covered | Unit tests inside 1,981 functional TCs (UT technique) | SM-UT-001…066 + SM-UX-UNIT-W31…A113 kept as aliases |
| 38-35 | §04 | SIT tests: 403 + 19 = 422 | Covered | IT/CT/SYS cases (Part 6) | SM-UX-SIT-W31…A113 + X01…X10 aliases |
| 38-36 | §04 | UAT tests: 155 + 147 = 302 | Covered | UAT packs AP-01…AP-10; SM-UAT-S001…S138 + SM-UX-UAT (147) aliases | Pack 155 retained UAT vs 138 SM-UAT-S IDs named in the FRD: the other 17 retained UAT records are not identifiable in BRD/FRD; the blueprint's AP-01…AP-10 vertical acceptance packs cover the same journeys (reported, no tag) |
| 38-37 | §04 | Acceptance groups (9) / required records: 1,545 | Partially covered | EVR + A090 gate; mapped in §8.3.5.15.10 | Gate groups mapped; counts recomputed by FR-ENH-J-015 at build time |
| 38-38 | §04 | Decision approvals / Product test execution / QC / Opt. controls / Opt. scenarios / Mandatory KPI / Expansion decisions / tests / QC: 180 / 624 / 235 / 104 / 24 / 21 / 172 / 175 / 10 | Partially covered | EVR groups G1…G9 (§8.3.5.15.10) | Blueprint previously had no optimization-control, scenario or mandatory-KPI groups |
| 38-39 | §04 | Prior offline test passes / skipped: 799 / 1 | Not applicable | Not used as evidence | Historical, synthetic; the blueprint certification ladder forbids production sign-off from synthetic runs (Part 6.1 §6.1.5.5) |
| 38-40 | §04 | New offline schema/catalog checks passed: 64 | Not applicable | — | Historical structural checks |
| 38-41 | §04 | UI routes rendered / link elements / JS errors: 147 / 435 / 0 | Covered | UX-QC-10 → TC-ENH-J-034; NFR-088 | Route-render smoke re-specified for the real build |
| 38-42 | §04 | Cached formula errors: 0 | Not applicable | — | Pack workbook not supplied |
| 38-43 | §05 | Effort scenario Low (baseline + expansion = gross): 287 + 62 = 349 PD | Conflict | Planning low 314 pd (Part 8.1 §8.1.6.4) | CONFLICT-488 |
| 38-44 | §05 | Effort scenario Base: 385 + 114 = 499 PD | Conflict | Planning central 416 pd; P80 445 | CONFLICT-488: implied overlap fraction f = 1 − (416 − 385) ÷ 114 = 0.728 |
| 38-45 | §05 | Effort scenario High: 483 + 196 = 679 PD | Conflict | Planning high 518 pd | CONFLICT-488 |
| 38-46 | §05 | Base PD by discipline (FE 90.68, BE 111.55, DB 52.85, AI 36.23, QA 65.64, DevOps/Sec 28.05): Σ 385.00 | Covered | Story-point based plan by epic and wave (Part 8.1 §8.1.6.2) | Discipline split recomputed from stories; the pack's split is a cross-check |
| 38-47 | §05 | Additional engineering work (5 items): 62 / 114 / 196 | Covered | Included in EP-01, EP-17, EP-18, EP-20, EP-21 stories | Nine screens planned in W5 (Part 8.1) |
| 38-48 | §05 | Baseline longest path: 113.5 PD | Covered | Critical path chain (Part 8.1 §8.1.7.1) | Different method (calendar critical path) |
| 38-49 | §05 | Approval review effort: 32.55 / 62.85 / 123.70 PD | Partially covered | Not separately estimated | Added to §8.3.5.14.8 resource approval: subtract overlap before approval |
| 38-50 | §05 | Illustrative cost formula (22 working days/month): 385 + 114 × (1 − f) | Covered | pd × rate; rate = ₹1.0–1.5 L ÷ 22 (Part 8.1) | Same 22-day basis |
| 38-51 | §06 | Optimization dimensions with weights: 20 (Σ 100%) | Not covered | None before this part | Added §8.3.5.15.1 (CONFLICT-486 on 20 vs 21) |
| 38-52 | §06 | Owned startup design capacity: 25+ | Covered | DEC-031 Y1 25–40 workspaces | — |
| 38-53 | §06 | Owned profiles demonstrated: 26 | Covered | TC-ENH-J-014 (27th startup) | Synthetic demonstration only |
| 38-54 | §06 | External tenants in recorded test / startups per tenant: 10 / 2 | Covered | TC-ENH-J-006; DEC-031 Y1 ≤ 10 tenants | — |
| 38-55 | §06 | Simulated concurrent runs tested: 20 | Covered | UX-QC-03 → TC-ENH-J-027; LT-06 | — |
| 38-56 | §06 | Optimization controls: 104 | Partially covered | 22 referenced before this part; 104 mapped now | §8.3.5.15.3 |
| 38-57 | §06 | Optimization acceptance scenarios: 24 | Not covered | 0 before; TC-ENH-J-001…024 now | §8.3.5.15.5 |
| 38-58 | §06 | KPI targets / mandatory: 35 / 21 | Partially covered | 0 OKPI before; NFR equivalents for 27 | OKPI-01…35 §8.3.5.15.4 |
| 38-59 | §07–08 | OKPI-01…35 thresholds: 35 rows | Partially covered | See OKPI table | Per-row status in §8.3.5.15.4 |
| 38-60 | §09 | Industry/business templates: 20 | Partially covered | Business templates CFG-04; A100 (count not fixed) | GAP-490: catalogue content reconciled by the automation-library group |
| 38-61 | §09 | Automation use-case groups × entries: 20 × 5 = 100 | Partially covered | Part 9.4 catalogue (36 AG + 43 AU, 14 WF) | GAP-490 |
| 38-62 | §09 | Workflow node types: 13 | Partially covered | Approved node types (DEC-051, A113); count not fixed | GAP-490 |
| 38-63 | §09 | Seeded owned startups: 4 | Covered | 4 (AppNAI, MedMaarg, EduVerse, OrganicSpec) | — |
| 38-64 | §09 | Website/Admin applications; new screens per platform: 2; 9 | Covered | 2; 9 | — |
| 38-65 | §09 | Archive entries in existing package: 237 | Not applicable | — | Package archive content, not software scope |
| 38-66 | §10 | Prior rendered page total / revised docs opened: 1,597 / 36 | Not applicable | — | Documentation metrics |
| 38-67 | §10 | Historical 100-parameter closure completeness: 74.5% | Not applicable | Not used | Historical; release conditions forbid using it as a readiness certificate |
| 38-68 | §10 | Production evidence gate: Blocked | Covered | A090 fail-closed gate (FR-A090) | Same principle |
| 38-69 | §10 | Release conditions (freeze candidates after code/schema review; run tests/QC; verify providers, security, load, DR, outcomes; budget review): — | Covered | Part 6.1 certification ladder; Part 8.1 gates; go-live checklist (Part 8.2 §8.2.4) | — |
| 38-70 | §11–12 | Historical page counts (36 documents): 982 + 615 = 1,597 | Not applicable | — | Historical documentation metric |

**Acceptance groups (document 38 §04) reconciled.** 180 decision approvals + 624 product tests + 235 QC + 104 optimization controls + 24 optimization scenarios + 21 mandatory KPIs = **1,188** (the "combined preflight" of document 36). Adding 172 expansion decisions + 175 expansion tests + 10 expansion QC gives **1,545** (document 38). Both totals are arithmetically correct; they describe different scopes [CONFLICT-491]. Part 8.3c §8.3.5.15.10 maps the nine groups to blueprint EVR gate groups G1…G9.

**Effort (document 38 §05) reconciled.** Document 38: gross base = 385 + 114 = 499 PD before reuse and overlap. Blueprint Part 8.1 §8.1.6.4: central 416 pd with the nine new screens already inside the story plan. Using the source's own formula, adjusted effort = 385 + 114 × (1 − f). Setting this equal to 416 gives f = 1 − 31 ÷ 114 = **0.728**: the blueprint plan implies that 72.8% of the expansion effort overlaps work already in the baseline stories. The same check for the low and high bands: low 314 = 287 + 62 × (1 − f) → f = 0.565; high 518 = 483 + 196 × (1 − f) → f = 0.821. The blueprint plan remains binding (DEC-124); the pack figures are a pre-reuse ceiling [CONFLICT-488].

### 8.3.4.2 Training manual catalogue (document 33) against the screen inventory

| Check (programmatic) | Result |
|---|---|
| Navigation entries vs Part 2.5 screens | 138 of 147 (W01–W30, A001–A108). The nine new screens W31–W34, A109–A113 appear only in the expansion training paragraph and the UX-QC table; Part 8.3b adds their task cards |
| Practice rows vs navigation entries | 138 = 138; same order; SM-UAT-S001…S138 contiguous |
| SM-UAT-S IDs resolving in Part 6.6 RTM | 138 of 138 (S001–S030 → FR-W01…W30; S031–S138 → FR-A001…A108) |
| Access classes in document 33 | Public 14, Public / Portal 8, Authentication 1, Portal 7, Admin 108 |
| Access-class differences with Part 2.1 | 3: W17 and W30 are "Public / Portal" in document 33 and "Public" in Part 2.1; W21 is "Authentication" in document 33 and "Portal" in Part 2.1. No rule changes: both pages are reachable from the public site and the portal shell; W21 is the portal sign-in. Recorded as Covered with note |
| Title wording differences | 17 (table below). All are abbreviations or catalog/catalogue spelling; IDs and meaning agree. Training material uses the Part 2.5 title and shows the document 33 title as an alias |
| Practice families | 23 families cover all 138 practice rows (none unclassified); Part 8.3b §8.3.5.5 turns each family into a reusable practice script |

| Screen | Doc 33 title | Part 2.1 FR title | Part 2.5 screen title |
|---|---|---|---|
| W02 | Company and startup business directory | Company and startup directory | Company and startup directory |
| W04 | Product, service and programme catalog | Product/service/programme catalogue | Offering catalogue |
| W05 | Product, service or programme details | Offering details | Offering details |
| W06 | Approved pricing and commercial packages | Approved pricing and packages | Approved pricing and packages |
| W07 | Industry and business solution pages | Industry and solution pages | Industry and solution pages |
| W08 | Blog, articles and knowledge centre | Blog, articles, knowledge centre | Blog and knowledge centre |
| W09 | Case studies, testimonials and business evidence | Case studies and testimonials | Case studies and testimonials |
| W13 | Product demo and partnership enquiry | Demo and partnership enquiry | Demo and partnership enquiry |
| W16 | Supplier registration and product supply enquiry | Supplier registration and supply enquiry | Supplier registration |
| W21 | Customer registration, login and recovery | Customer registration, login, recovery | Registration, login, recovery |
| W27 | Customer onboarding and document exchange | Onboarding and document exchange | Onboarding and document exchange |
| W30 | Contact, privacy, terms and help centre | Contact, privacy, terms, help centre | Contact, privacy, terms, help centre |
| A001 | Login, MFA and account recovery | Login, MFA, recovery | Login, MFA, recovery |
| A005 | Product knowledge catalog | Product knowledge catalogue | Product knowledge catalogue |
| A030 | Sales pipeline and assignment rules | Pipeline and assignment rules | Pipeline and assignment rules |
| A097 | Future product catalog view | Future product catalogue view | Future product catalogue |
| A108 | Website preview, approval, publishing and analytics | Website preview, approval, publishing, analytics | Website preview, approval, publishing, analytics |

### 8.3.4.3 Optimization controls (document 36) against the blueprint

Before this part, the blueprint cited **22** of the 104 controls (the 22 OPT IDs that also appear in the BRD/FRD: OPT-01-01, 03-01, 04-01…08, 07-01, 10-01, 11-01, 12-01…04, 15-01, 20-01…04). Part 8.3c maps all 104. Status after mapping: Covered 78, Partially covered 20, Conflict 5, Not covered 1.

| Dim | Dimension | Controls | Cited in blueprint before | Covered | Partially covered | Not covered | Conflict |
|---|---|---|---|---|---|---|---|
| OPT-01 | Security | 8 | 1 | 7 | 1 | 0 | 0 |
| OPT-02 | Performance | 7 | 0 | 4 | 2 | 0 | 1 |
| OPT-03 | Cost | 8 | 1 | 4 | 3 | 0 | 1 |
| OPT-04 | Automation | 8 | 8 | 8 | 0 | 0 | 0 |
| OPT-05 | Stability | 7 | 0 | 5 | 1 | 0 | 1 |
| OPT-06 | Scalability | 5 | 0 | 2 | 2 | 0 | 1 |
| OPT-07 | Architecture | 5 | 1 | 4 | 1 | 0 | 0 |
| OPT-08 | Database | 6 | 0 | 4 | 2 | 0 | 0 |
| OPT-09 | API & Integration | 5 | 0 | 5 | 0 | 0 | 0 |
| OPT-10 | AI Intelligence | 6 | 1 | 4 | 1 | 0 | 1 |
| OPT-11 | Data Quality | 5 | 1 | 5 | 0 | 0 | 0 |
| OPT-12 | Business Conversion | 4 | 4 | 4 | 0 | 0 | 0 |
| OPT-13 | Maintainability | 4 | 0 | 2 | 1 | 1 | 0 |
| OPT-14 | Reusability | 3 | 0 | 3 | 0 | 0 | 0 |
| OPT-15 | UI/UX | 4 | 1 | 4 | 0 | 0 | 0 |
| OPT-16 | Development Productivity | 3 | 0 | 2 | 1 | 0 | 0 |
| OPT-17 | Testing & QC | 4 | 0 | 3 | 1 | 0 | 0 |
| OPT-18 | Deployment & Recovery | 4 | 0 | 3 | 1 | 0 | 0 |
| OPT-19 | Privacy & Compliance | 4 | 0 | 4 | 0 | 0 | 0 |
| OPT-20 | SaaS Profitability | 4 | 4 | 1 | 3 | 0 | 0 |
|  | **Total** | 104 | 22 | 78 | 20 | 1 | 5 |

### 8.3.4.4 Optimization KPIs (OKPI-01…35)

21 OKPIs are mandatory (blocking): OKPI-01, OKPI-02, OKPI-03, OKPI-04, OKPI-05, OKPI-07, OKPI-08, OKPI-11, OKPI-12, OKPI-16, OKPI-17, OKPI-18, OKPI-19, OKPI-20, OKPI-22, OKPI-23, OKPI-26, OKPI-27, OKPI-28, OKPI-32, OKPI-35. Status after mapping to blueprint NFR, KPI and SLO IDs: Covered 24, Partially covered 5, Conflict 3, Not covered 3. Full table: Part 8.3c §8.3.5.15.4.

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

**Status: Part 8 Batch 8.3a complete. Five source documents reviewed line by line; 786 atomic aspects registered; every number in document 38 reconciled.**
