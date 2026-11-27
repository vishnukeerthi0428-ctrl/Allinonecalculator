# AI Growth Engine: Employee Sales & Marketing Automation
## Application Blueprint: PART 3 (Batch 3.4), Source Pack Review: Architecture, Delivery and Workflow Enhancements (documents 04, 05, 09, 10)

| Field | Value |
|---|---|
| Document | Application Blueprint · Part 3.4: line-by-line coverage review of source-pack documents 04 *Solution Architecture & Delivery Plan*, 05 *Workflow Automation & Engagement Playbook*, 09 *High Level Design* and 10 *Detailed Level Design*, with enhancements at blueprint depth |
| Version | 1.0 · 27 Nov 2026 |
| Baseline | BRD, FRD, Parts 0, 0A (DEC-001…065), 1, 2.1–2.5, 3.1–3.3, 4.1–4.3, 5.x, 6.x, 7.1–7.3, 8.1–8.2, 9.1–9.4; errata log items 1–87 |
| Compared chiefly against | Part 2.2 (process flows), Part 2.3 (rules and state machines), Part 3.1 (architecture), Part 3.2 (API and integration), Part 7 (AI), Part 8 (delivery) |
| Roles applied | Solutions Architect (lead), Technical Architect, Principal Engineer, Automation Architect; consulted: DevOps/SRE Lead, Data Architect/DBA, FinOps Lead, QA Lead, Security/Compliance/AI Governance Lead |
| Group | **B** (Source Pack Brief). Enhanced IDs: FR-ENH-B-001…027, US-<EP>-EB<nn>, TC-ENH-B-001…036, NFR-ENH-B-01…08, LT-ENH-B-01…04, RB-ENH-B-01…03, WQG-01…12, ADR-100…109 |
| Tags issued | ASSUMPTION-320…325 · GAP-320…335 · CONFLICT-320…330 · RECOMMENDATION-320…331 (register in §3.4.8) |
| Coverage CSV | `final/coverage/B_coverage.csv` (394 atomic aspects) |
| Scripts | `assembly/source_pack/groupB_parse.py` (parses every table row of the four documents and reconciles catalogues), `assembly/source_pack/groupB_aspects.py` (aspect register, CSV and register tables) |

**Acronyms used in this part.** ACK acknowledgement · ADR architecture decision record · ALB Application Load Balancer · AZ Availability Zone · CMK customer-managed key · DAG directed acyclic graph · DLQ dead-letter queue · DLP data-loss prevention · DRF Django REST Framework · DTO data transfer object · ECS Elastic Container Service · EVR evidence record · FTE full-time equivalent · IaC infrastructure as code · KMS Key Management Service · LT load-test profile · OKPI optimization KPI of the source pack (the pack's KPI-01…35, renamed to avoid collision with Part 1 KPI-01…31) · OPT optimization control of the source pack · PD person-day · PDP Policy Decision Point · PITR point-in-time recovery · RC recovery class · RLS row-level security · RPO/RTO recovery point/time objective · RUM real-user monitoring · SLO service level objective · WQG workflow quality gate.

**Verification convention.** Every price, quota, model name, managed-service behaviour and timing quoted in this part is an **estimate to verify at time of implementation (as of 27 Nov 2026)**. Currency conversion uses ₹90 per USD (ASSUMPTION-101 of Part 3.1). Taxes excluded.

**How to read this part.** §3.4.1–§3.4.4 record what the four documents say and how much of it the blueprint already covers. §3.4.5 is the main body: it writes the missing content, organized by the blueprint part it extends. §3.4.6 lists conflicts with proposed resolutions for the coordinator to turn into binding decisions. Nothing in an earlier part is changed by this part; where this part adds to or refines an earlier design, the addition is tagged and the earlier part remains authoritative until the coordinator accepts the change.

---

## 3.4.1 Documents reviewed

All four documents were read completely, line by line. Every table row was also parsed programmatically by `groupB_parse.py` (48 tables, 402 table rows across the four documents), so that no row, ID or threshold was skipped.

**Pattern found.** Each document opens with the same common core as documents 01/02 (product purpose and boundary, the four initial startups, technology and execution principles). Documents 04, 09 and 10 then share three further sections that are **not** in 01/02 (Independent deployment topology, Capacity/reliability/recovery acceptance, Configuration and activation; lines 37–118 are byte-identical in 04, 09 and 10). Every document closes with the common Website/Admin operating contract, the implementation and acceptance controls, an optimization section and the nine-interface expansion table (W31–W34, A109–A113). The common core is registered once (aspects B-CC-01…16) and marked "Common core: see document 01/02 coverage".

| Doc | Title | Size (bytes / lines) | Sections (H1+H2) | Tables / rows | What it is trying to tell | Atomic aspects |
|---|---|---|---|---|---|---|
| 04 | Solution Architecture & Delivery Plan | 59,240 / 1,023 | 61 | 16 / 177 | The **delivery architecture**: independent deployment topology, capacity and recovery targets, configuration-to-activation sequence, a seven-package dependency order, the **66-module delivery backlog with dependencies and acceptance**, a production runbook, effort and pilot-cost assumptions (287–483 PD; ₹14,500 → ₹16,675 → ₹31,165), a **discipline-level task allocation (385 PD, 113.5-day dependency path)**, cost/scalability/architecture/reusability/productivity/SaaS-profitability optimization controls, and acceptance procedures including a 32.55–123.70 PD approval-review effort model. Expansion: UX-TASK DAG for nine new interfaces (62/114/196 PD) | 85 (+ shared rows) |
| 05 | Workflow Automation & Engagement Playbook | 65,364 / 862 | 73 | 13 / 88 | The **automation playbook**: the 14-workflow register, channel contracts (email, WhatsApp, web, calendar, referrals, social), inbound acquisition capabilities, **22 module cards** (UX, backend, governance, entities, API, trigger, tools, licence/quota, budget), vertical conversion sequences, a deterministic execution decision table, a **proposed workflow fixture** (max_attempts, stop_on, paid_fallback, uncertain_result), operational regression scenarios, business regression fixtures, automation and stability optimization controls and nine acceptance procedures | 81 |
| 09 | High Level Design | 37,451 / 442 | 56 | 9 / 59 | The **high-level design**: seven Command Centre views, component contracts (frontends, Django monolith, workers, data/RAG, adapters, AI runtime, deployment, state machine, security boundary, delivery engineering, auto-driven Admin), interface topology, provider independence, production boundary and AWS deployment decisions (separate accounts, RPO/RTO, regional strategy), security/stability/scalability/architecture/database/deployment controls and seven acceptance procedures (product/audience isolation, growth workload, shared-library boundaries, IaC completeness) | 35 |
| 10 | Detailed Level Design | 70,407 / 784 | 106 | 10 / 78 | The **detailed design**: the global filter hierarchy, **18 logical AI responsibilities with a typed prompt envelope**, RAG rules, **20 design contracts** (REST, canonical inbound event, outbound intent, locking, AI schema, retry, webhook security, reply routing, closure rule, admin authorization, clinical data isolation, budget, scoring, performance, agent decomposition, metrics, clinical escalation, development vs runtime), frontend **route map and DRF permission classes**, the **adapter interface estimate/execute/reconcile/health**, test harness and coverage targets, the canonical event envelope, service-level execution decisions, an atomic transaction pattern, 41 optimization controls and 15 acceptance procedures including **outstanding approval gates (38 API definitions, 4 DB confirmations, 138 UI mappings)** | 109 |
| — | Shared across documents | — | — | — | Common core (16), sections shared by 04/09/10 (28), component rows shared by 04/09 (12), optimization controls deduplicated across documents (64 distinct OPT IDs, registered once each) | 84 |
| | **Total** | 232,462 / 3,111 | 296 | 48 / 402 | | **394** |

**Distinct optimization controls in the four documents.** 64 OPT IDs across 19 dimensions (Security, Performance, Cost, Automation, Stability, Scalability, Architecture, Database, API & Integration, AI Intelligence, Data Quality, Maintainability, Reusability, Development Productivity, Testing & QC, Deployment & Recovery, SaaS Profitability). 12 of them also appear in the FRD; 17 are already cited by ID somewhere in the blueprint. The master optimization catalogue (104 controls, OKPI-01…35) belongs to the reviewer of document 36; this part maps the 64 controls found in documents 04/05/09/10 to blueprint locations (§3.4.4.4) and writes the missing ones.

---

## 3.4.2 Coverage register summary

Counts by status per document group (from `B_coverage.csv`). A "Conflict" is counted once per aspect even when the same conflict ID covers several aspects.

<!--STATUS_COUNTS-->

**Interpretation.** 81% of the atomic aspects are already covered by the blueprint, usually at greater depth than the source (the blueprint's Part 3 alone holds 43 ADRs, 555 catalogued operations and 199 entities against the pack's retained 302 operations and 149 entities). The 75 aspects that are partial, missing or in conflict cluster in six areas, each written up in §3.4.5:

| Cluster | Aspects | Where the enhancement is written |
|---|---|---|
| Growth-scale capacity, recovery classes, availability and budget thresholds | 14 | §3.4.5.1 (A, B), §3.4.5.6 (C) |
| Deployment technology and naming differences (Fargate, Redis, ALB, app and repository names) | 5 | §3.4.5.1 (C), ADR-100, ADR-101 |
| Integration contracts: adapter port operations, permission classes, route map, inbound/outbound contracts, product-event ingress | 10 | §3.4.5.1 (D), §3.4.5.2 |
| Workflow engine contracts: execution-policy block, activation gates, reply taxonomy, regression matrix, recording rule | 8 | §3.4.5.4 |
| AI contracts: typed envelope, responsibility mapping, need schema, agent decomposition | 5 | §3.4.5.5 |
| Delivery and operations: discipline effort, expansion DAG, approval-gate register, runbooks, coverage rule, technical debt, fail-fast configuration, provider candidates | 20 | §3.4.5.6, §3.4.5.7 |

---

## 3.4.3 Detailed coverage register

Every aspect is listed. Covered aspects cite the blueprint location that already satisfies them; every Partially covered, Not covered or Conflict aspect is listed individually with the action and the new IDs. The same table is in `final/coverage/B_coverage.csv`.

<!--REGISTER-->

---

## 3.4.4 Catalogue reconciliation

### 3.4.4.1 Document 04 commercial module delivery backlog (66 rows) vs Part 1 BR-M register

Method: `groupB_parse.py` parses the 66 backlog rows (sequence, module, dependency list, acceptance), resolves each dependency name to its backlog sequence, maps names to BR-M numbers by exact module name, and compares dependency sets and acceptance text with Part 1 §1.x BR-M01…M66.

| Check | Result | Note |
|---|---|---|
| Module names matched to BR-M | **66 / 66** | Exact name match |
| Dependency sets equal to Part 1 | **66 / 66** | After mapping the pack's dependency-ordered sequence numbers to BR-M numbers |
| Acceptance text identical | **52 / 66** | 13 differ only by British spelling or by the DEC suffix Part 1 added (e.g. "(DEC-023)"); 1 real difference (BR-M01) |
| BR-M01 acceptance | Pack: "Existing capability; validate growth/admin access before launch (not new build)"; predecessors **H02, H03** (pre-existing hardening items of the reused identity service) | Blueprint: "Cross-role access denied; session revoked" plus DEC-003/DEC-019 reuse. Both apply; TC-ENH-B-021 adds the reuse-validation acceptance. H02/H03 are not defined anywhere in the pack's 38 documents [GAP-320 note: treated as the identity spike US-0101 inputs] |
| Cycles in the dependency graph | **0** | Acyclic |
| Forward references (dependency on a later sequence) | **0** | The pack's sequence is a valid topological order |
| Dependency depth | **27 levels** | Level sizes 1,3,3,2,4,4,1,2,1,2,1,1,1,1,2,3,2,3,5,7,3,3,2,4,3,1,1 |

**Longest module chain (27 modules).** BR-M01 Identity → M04 Consent → M05 Integration registry → M07 Source permissions → M10 Search query planner → M11 Public web discovery → M12 Evidence extraction → M13 Account discovery → M14 Buying signal → M15 Business need → M16 Solution matching → M17 Opportunity scoring → M18 Decision-maker role discovery → M19 Contact verification → M24 Engagement eligibility → M25 Message drafting → M26 Email integration → M27 Unified inbound → M29 Meeting and calendar → M43 Proposal builder → M44 Quote engine → M46 Contract/MoU → M47 Payment and closure → M52 Revenue and attribution → M60 Forecast → M61 Admin command centre → M62 Production release.

**Consequence for Part 8.** The module chain confirms the order Part 8.1 §8.1.7.1 uses at story level (identity and RLS → PDP → gateway → discovery → engagement → closure). It also shows that **M60 Forecast (Could) sits on the path to M61/M62 (Must)**; errata item 10 already makes that dependency soft ("Forecast not enabled" slot). No change to Part 8 is needed.

### 3.4.4.2 Document 05 module cards (22) vs Part 3.2 API catalogue and Part 3.3 entities

The 12 inbound-acquisition cards carry objective, dependency, acceptance, owner, reuse and scope; the 10 conversion cards add UX, backend, governance, entities, API, trigger, tools, licence/quota and budget treatment.

| Module card | Operations named (method path) | Part 3.2 operation (★ legacy) | Entities named | In Part 3.3 |
|---|---|---|---|---|
| Proposal builder | POST /deals/{id}/proposals | API-328 ★ | Proposal, ProposalVersion | Yes |
| Quote and pricing engine | POST /quotes; POST /quotes/{id}/approve | API-329 ★, API-330 ★ | Quote, QuoteLine, PriceVersion | Yes |
| Negotiation and objection handling | POST /deals/{id}/objections | API-331 ★ | Objection, Negotiation, Approval | Yes |
| Contract and MoU workflow | POST /contracts; POST /webhooks/esign | API-332 ★, API-333 ★ | Contract, SignatureEvent | Yes |
| Payment and closure | POST /webhooks/payment; POST /deals/{id}/close | API-385 ★, API-386 ★ | Payment, Invoice, Deal | Yes |
| Onboarding and handoff | GET /onboarding; POST /onboarding/{id}/complete | API-412 ★, API-413 ★ | Onboarding, Task, Handoff | Yes |
| Partner deployment pipeline | POST /partners; POST /pilots/{id}/status | API-414 ★, API-415 ★ | Partner, Pilot, Deployment | Yes |
| Retention and renewal | GET /renewals; POST /renewals/{id}/review | API-416 ★, API-417 ★ | Renewal, Subscription, AccountMetric | Yes ("Subscription" = CustomerSubscription, errata 22) |
| Lost deal and feedback | POST /deals/{id}/lost; POST /feedback | API-387 ★, API-418 ★ | Outcome, Feedback | Yes |
| Revenue and attribution | GET /metrics/revenue | API-388 ★ | MetricSnapshot, AttributionEvent, Payment | Yes |
| **Totals** | **17 operations** | **17 / 17 found, all as retained legacy paths** | **27 entity mentions** | **27 / 27** |

**Integration candidates named on the cards and not in the blueprint:** PandaDoc (proposal, contract), Crossbeam Skills (partner pipeline), Socialinsider and PostHog (revenue and attribution). The cards themselves mark licence, quota and price as unverified. The blueprint made different, deliberate choices (ADR-032 server-side document rendering, ADR-038 manual e-sign evidence first, ADR-011 first-party analytics only). §3.4.5.2 (F) adds a provider candidate register so that these candidates are evaluated through the replacement-first gate rather than silently dropped [GAP-331].

### 3.4.4.3 Cost and estimate recomputation (document 04)

| Item | Source figure | Recomputed | Blueprint position |
|---|---|---|---|
| Pilot base (B01–B07) | ₹14,500 | 5,000 + 3,000 + 1,500 + 1,000 + 500 + 2,000 + 500 = **₹14,500** ✓ | DEC-020 |
| Base with 15% contingency | ₹16,675 | 14,500 × 1.15 = **₹16,675** ✓ | DEC-020; superseded by Part 8 band ₹19,665–22,885 (errata 68) |
| With Apollo reserve and developer seats | ₹31,165 | (14,500 + 9,000 + 3,600) × 1.15 = **₹31,165** ✓ | Part 8 band with optional items ₹34,155–37,375 (errata 68) |
| Developer seats | ₹3,600 | 2 × $20 × ₹90 = ₹3,600 ✓ (verify seat price) | B09 |
| Discipline allocation total | 385 PD | 90.68 + 111.55 + 52.85 + 36.23 + 65.64 + 28.05 = **385.00** ✓ | Part 8.1 central 416 pd (CONFLICT-328) |
| Discipline cost at ₹1 L / ₹1.5 L per month | e.g. React ₹412,182 / ₹618,273 | PD ÷ 22 × 100,000 (or 150,000): all six rows match to the rupee ✓ | — |
| Discipline total cost | — | ₹17.50 L at ₹1 L; ₹26.25 L at ₹1.5 L | Inside BRD §6 ₹13.05–32.93 L |
| Expansion UX-TASK sum | 62 / 114 / 196 PD | 13 tasks summed: **62 / 114 / 196** ✓ | §3.4.5.7 (C) |
| Expansion critical path | not stated | FOUNDATION → FIELDS → any screen → QA = **36 / 64 / 110 PD** (low/base/high) | §3.4.5.7 (C) |
| Approval review effort | 32.55 / 62.85 / 123.70 PD | Not decomposed in the source; taken as stated | §3.4.5.7 (D) |

### 3.4.4.4 Optimization controls (64 distinct OPT IDs) vs blueprint

| Dimension | OPT IDs in documents 04/05/09/10 | Covered | Partial | Not covered | Conflict |
|---|---|---|---|---|---|
| Security | OPT-01-01 | 1 | 0 | 0 | 0 |
| Performance | OPT-02-01 | 1 | 0 | 0 | 0 |
| Cost | OPT-03-01…08 | 6 | 1 (03-04) | 0 | 1 (03-08) |
| Automation | OPT-04-01…08 | 8 | 0 | 0 | 0 |
| Stability | OPT-05-01…07 | 4 | 2 (05-04, 05-06) | 0 | 1 (05-07) |
| Scalability | OPT-06-01…05 | 2 | 0 | 2 (06-02, 06-03) | 1 (06-01) |
| Architecture | OPT-07-01…05 | 5 | 0 | 0 | 0 |
| Database | OPT-08-01…06 | 6 | 0 | 0 | 0 |
| API & Integration | OPT-09-01…05 | 4 | 1 (09-01) | 0 | 0 |
| AI Intelligence, Data Quality | OPT-10-01, OPT-11-01 | 2 | 0 | 0 | 0 |
| Maintainability | OPT-13-01…04 | 2 | 1 (13-03) | 1 (13-02) | 0 |
| Reusability | OPT-14-01…03 | 3 | 0 | 0 | 0 |
| Development Productivity | OPT-16-01…03 | 2 | 1 (16-02) | 0 | 0 |
| Testing & QC, Deployment & Recovery | OPT-17-01, OPT-18-01 | 2 | 0 | 0 | 0 |
| SaaS Profitability | OPT-20-01…04 | 4 | 0 | 0 | 0 |
| **Total** | **64** | **51** | **6** | **3** | **4** (counted as Conflict in §3.4.2) |

**Cross-reference rule [RECOMMENDATION-331].** The blueprint already implements most controls without citing their OPT IDs. To make the source-pack acceptance protocol auditable, each implementing artefact cites the OPT ID in its "Source" column when next revised (for example ADR-003 → OPT-05-01; ADR-023 → OPT-05-02; NFR-042 → OPT-02-01; NFR-009 → OPT-04-07; Part 4.3 §4.46.5 → OPT-20-01). The full mapping is the "Blueprint location" column of the OPT rows in §3.4.3.

### 3.4.4.5 Inventory totals quoted in all four documents

| Source statement | Source count | Blueprint count | Status |
|---|---|---|---|
| Interfaces | 147 (34 W + 113 A; 138 retained + 9 added) | 147 (W01–W34, A001–A113) | Covered |
| API/adapter operations | 302 retained + 19 candidate | 555 catalogued (DERIVED superset, errata 42) | Covered (superset) |
| Logical entities | 149 retained + 6 candidate | 199 (DERIVED superset, errata 24) | Covered (superset) |
| Product tests | 624 retained + 175 candidate | Part 6 TC catalogue (epic-based IDs) | Covered; reconciled by the test-document reviewer |
| Outstanding approval gates (doc 10) | 38 exact API definitions, 0 partial, 4 DB confirmations, 138 UI semantic mappings | Not tracked | Not covered → §3.4.5.7 (D) |
