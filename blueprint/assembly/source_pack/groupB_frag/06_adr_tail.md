
### 3.4.5.9 Architecture decision records (ADR-100…ADR-109)

Format as Part 3.1 §3.1.9. All are **Proposed** until the coordinator accepts them.

#### ADR-100 Container compute: ECS on EC2 retained; Fargate for on-demand tasks

| Field | Content |
|---|---|
| Status | Proposed (resolves CONFLICT-320 with ADR-013) |
| Context | Docs 04/09 name ALB + ECS Fargate; doc 09 also says deployment mode needs workload validation. ADR-013 chose ECS on EC2 for pilot cost within B01 |
| Decision | Keep ECS on EC2 for long-running services and workers. Use Fargate for on-demand short tasks (C10 renderer, migration and backfill one-offs, restore-validation jobs) where per-second billing beats a warm instance. Re-evaluate worker-batch on Fargate Spot at the scale gate |
| Alternatives | All-Fargate (≈ 3–4× pilot compute, verify); EKS (control-plane fee) |
| Consequences | + Pack's isolation intent kept (task roles, private subnets). − Two launch types to operate (mitigated by IaC modules) |
| Review trigger | Pilot instance CPU > 70% sustained for 7 days, or scale-gate decision |

#### ADR-101 Valkey as broker and cache engine

| Field | Content |
|---|---|
| Status | Proposed (confirms CN-01, ADR-003; resolves CONFLICT-320 wording) |
| Decision | Celery broker, result backend, caches, locks and rate-limit buckets use Valkey (container at pilot, ElastiCache for Valkey at scale). Any "Redis" in source documents means the Redis protocol. Client libraries use the Redis protocol and must pass the Valkey compatibility test in CI |
| Consequences | + Open-source licence certainty. − Managed-service feature parity to verify at scale gate |

#### ADR-102 Data recovery classes RC-1…RC-3

| Field | Content |
|---|---|
| Status | Proposed (FR-ENH-B-002; resolves CONFLICT-322 and GAP-321) |
| Context | Pack: critical RPO ≤ 15 min, RTO ≤ 4 h initial / ≤ 2 h growth; regenerable research RPO ≤ 24 h / RTO ≤ 8 h. Blueprint: one class, DEC-018, CONFLICT-101 |
| Decision | Every Part 3.3 table carries a `recovery_class` attribute (RC-1, RC-2, RC-3). Restore runbooks restore in class order. RTO ≤ 2 h applies to RC-1 for non-regional failures after the scale gate. Trigger: RC-1 restore drill > 75 min → move RC-2 bulk tables to a separate research database instance |
| Alternatives | Warm standby in a second region (cost, deferred to Year 2 per ADR-019) |
| Consequences | + Restore time bounded by critical data size. − One more attribute to maintain per table |

#### ADR-103 Adapter port contract v2

| Field | Content |
|---|---|
| Status | Proposed (FR-ENH-B-004; extends ADR-009) |
| Decision | Every port implements `estimate`, `execute`, `reconcile`, `health`; results carry the normalized outcome (accepted, retryable, permanent, uncertain, denied) in addition to the ADR-009 failure class |
| Consequences | + Budget reservation, breakers and reconciliation are uniform. − Adapters without a provider status query must implement `reconcile` by correlation events (documented per adapter in §3.2.6.3) |

#### ADR-104 Agent envelope v1.1

| Field | Content |
|---|---|
| Status | Proposed (FR-ENH-B-009; extends Part 7.2 §7.2.7) |
| Decision | Add `purpose`, `schema_revision`, `missing_fields`, `policy_flags`, `proposed_action`, `requires_approval`, `cost_estimate`. The engine may only raise `requires_approval`; `proposed_action` is mapped to an allowlisted node or dropped |
| Consequences | + Policy enforced on structure, not on model prose. − Eval sets updated for every agent (AU-006) |

#### ADR-105 Product-event ingress through an allowlisted internal adapter

| Field | Content |
|---|---|
| Status | Proposed (FR-ENH-B-010; resolves CONFLICT-330) |
| Decision | Startups' own delivered products may send organization-level commercial lifecycle events only through `ProductEventPort`, closed schema, DLP scan, founder-and-DPO-approved source registration, flag OFF by default. Events are informational and never close deals or create payments |
| Alternatives | No ingestion (manual entry only); shared database views (rejected: violates independence) |
| Consequences | + Renewal and onboarding signals without clinical data. − Mapping table maintenance |

#### ADR-106 Commercial journey as a projection, not a state machine

| Field | Content |
|---|---|
| Status | Proposed (FR-ENH-B-011) |
| Decision | The end-to-end lifecycle in docs 04/09 is implemented as a read model derived from authoritative events. Guards and the PDP never read it |
| Consequences | + Funnel analytics without a second source of truth. − Projection lag (≤ 60 s) |

#### ADR-107 Declared execution policy per workflow revision

| Field | Content |
|---|---|
| Status | Proposed (FR-ENH-B-012, FR-ENH-B-013) |
| Decision | `execution_policy` JSON schema 1.0 is mandatory on every workflow revision; validated at save and at activation (WQG-07); mandatory stops auto-inserted; loosening only by R01; lease fencing tokens on StepRun |
| Consequences | + Uniform, auditable retry and stop behaviour. − Template migration for existing drafts |

#### ADR-108 Growth-scale validation profiles

| Field | Content |
|---|---|
| Status | Proposed (FR-ENH-B-001; resolves CONFLICT-321) |
| Decision | DEC-031 stays the sizing basis; the pack's capacity matrix is the validation basis (initial before Release 1, growth at the scale gate) using LT-ENH-B-01…04 |
| Consequences | + No premature spend. − Growth tests need Topology B in `perf` for the test window (≈ 1–2 days of Topology B cost, ≈ ₹1,400 per day at ₹21,000/month, estimate, verify) |

#### ADR-109 Four permission base classes per ingress namespace

| Field | Content |
|---|---|
| Status | Proposed (FR-ENH-B-005) |
| Decision | `PublicPublishedRead` (and `PublicIntakeWrite`), `ExternalGrantPermission`, `StaffRolePermission`, `ServiceIdentityPermission`; default `DenyAll`; exactly one base class per view, enforced by CI |
| Consequences | + Audience errors become structural failures at build time. − Dual-mounted operations need two view classes |

---

## 3.4.6 Conflicts and proposed resolutions

| ID | Conflict | Source (pack) | Blueprint position | Proposed resolution | Decision owner |
|---|---|---|---|---|---|
| CONFLICT-320 | Deployment technology: ECS Fargate + ALB + ElastiCache Redis + "Redis broker" | Docs 04/09 component rows | ADR-013 ECS on EC2, no ALB at pilot; Valkey (CN-01, ADR-003) | Blueprint governs; ADR-100 allows Fargate for on-demand tasks; ADR-101 reads "Redis" as protocol; ALB is the scale-gate state | Solutions Architect, FinOps |
| CONFLICT-321 | Capacity design points: initial 25 owned / 10 external; growth 50+ / 100 | Docs 04/09/10 capacity matrix; OPT-06-01 | DEC-031 Year 1 25–40 / 2–10; Year 2 100 / 30 | DEC-031 remains the sizing basis; the pack matrix is the validation basis (ADR-108, LT-ENH-B-01…04). 100 external tenants is a post-Year-2 validation target, priced at the scale gate | Founder, Architect |
| CONFLICT-322 | Growth RTO ≤ 2 h | Docs 04/09 | DEC-018 ≤ 4 h; CONFLICT-101/112 region ≤ 24 h pilot | Adopt ≤ 2 h for RC-1 non-regional failures after the scale gate (ADR-102); regional values unchanged; pilot stays ≤ 4 h | Founder, DevOps/SRE |
| CONFLICT-323 | Availability "99.9% critical availability over rolling 30 days" | OPT-05-07 (docs 05/10) | DEC-018 99.5% pilot → 99.9% public at scale gate; SLO-01 measured on a 28-day rolling window | 99.9% applies to website/portal after the scale gate (SLO-01); Admin stays 99.5%; window remains 28-day rolling for error budgets and calendar month for reporting (DEC-018) | DevOps/SRE |
| CONFLICT-324 | Budget alert thresholds 70/90% | OPT-03-08 | BRL-AI-08 / NT-025 80% alert, 100% stop; AWS Budgets 50/80/100% | Ladder 70 (info) / 80 (High) / 90 (Critical, optional jobs deprioritized) / 100 (stop) (FR-ENH-B-022); BRL-AI-08 unchanged | FinOps |
| CONFLICT-325 | "No cross-region replication before approval" | Doc 09 regional strategy | ADR-019 cross-Region automated backups to ap-south-2 from day one | DEC-040 is the approval for **backup copies** inside India; no live replication of application data outside ap-south-1 without a new decision; record DEC-040 as the approval evidence in the IaC change record | Legal/Security, Architect |
| CONFLICT-326 | Investor-product wording: "lead/investor record", "investor/customer tokens", "investment/commercial Django domains", event `product = investment_or_commercial` | Docs 05/09/10 | Investor functions are out of scope; separate investor product (DEC-009, ADR-033) | This product never creates investor records; the inbound journey test creates a lead only; investor tokens are used only as negative test inputs (TC-ENH-B-020); envelope `product` is the constant `commercial` | Product Owner |
| CONFLICT-327 | Agent decomposition: "six runtime responsibilities" vs 18 responsibilities vs blueprint catalogue | Doc 10 | Part 7.1: 36 agents (32 product-scope) + 43 automations | Six = families; Part 7.1 governs; family mapping in §3.4.5.5 B | AI lead |
| CONFLICT-328 | Effort and critical path: 385 PD base for 149 work items; dependency-only path 113.5 days | Doc 04 | Part 8.1 central 416 pd; re-baselined calendar (CONFLICT-142) | Part 8.1 governs scope and calendar; pack figures kept as a top-down cross-check; discipline shares used for capacity check (§3.4.5.7 B) | Product Owner, Delivery lead |
| CONFLICT-329 | Names: Django apps (accounts, catalog, …, reporting) and monorepo paths (apps/growth-ui, …) | Docs 04/09 | Part 3.1 §3.1.4 module names; ADR-006/ADR-060 repository layout | Blueprint names govern; mapping tables in §3.4.5.1 C | Principal Engineer |
| CONFLICT-330 | Product webhook into the marketing database vs "no live cross-product join or automatic handoff" | Docs 04/09 security boundary; common core | DEC-009 independence | The independence rule concerns the separate investor product; startups' own delivered products are external systems behind an allowlisted adapter, off by default (ADR-105) | DPO, Architect |

---

## 3.4.7 Expert persona review

| Persona | How the perspective was applied | What the persona would still flag |
|---|---|---|
| **Solutions Architect** | Reconciled every component row and deployment decision of docs 04/09 with ADR-001…043; kept the blueprint's cost-driven choices and wrote the pack's intent (independence, growth validation, recovery classes) as ADR-100…108 rather than re-opening settled decisions | The growth column (100 external tenants) needs a pricing decision for per-tenant KMS keys and Topology B; the scale gate should not be passed without LT-ENH-B-01…03 evidence |
| **Technical Architect** | Specified contracts the pack named but the blueprint left implicit: adapter port v2, permission base classes, route map with cache key, inbound/outbound contracts, envelope mapping | The 38 outstanding exact API definitions are the largest residual design risk; DTO completion must precede each consuming story (FR-ENH-B-024) |
| **Principal Engineer** | Wrote the service contract card, atomic transaction reference, fail-fast configuration, lease fencing, critical-branch coverage and the documentation-sync check, each enforceable in CI | Lease fencing and branch-inventory annotations add discipline cost; they should land in W0-B with the engine skeleton, or retrofitting will be expensive |
| **Automation Architect** | Turned doc 05's fixture, quality gates and regression list into a validated `execution_policy` schema, 12 activation gates and a 90-cell regression matrix; aligned the reply taxonomy and channel rules | The 90-cell matrix is large for a 1.0 FTE QA; prioritize S2, S3, S5 and S7 across all flows first (they carry the zero-tolerance KPIs) |
| DevOps/SRE Lead (consulted) | Added three runbooks, the class-ordered restore and growth load profiles | Growth profiles need a `perf` Topology B window; budget it in the scale-gate plan |
| Data Architect/DBA (consulted) | Recovery classes per table; opportunity and projection sizing; connection-pool arithmetic | RDS Proxy vs PgBouncer choice at the growth column needs a measured decision |
| FinOps Lead (consulted) | Threshold ladder, cost per 1,000 tasks, provider benchmark gate, per-tenant KMS cost | Unit-cost metric needs AI cost attribution per tenant to be complete (AU-012) |
| Security/Compliance/AI Governance Lead (consulted) | Product-event DLP allowlist, purpose field in the envelope, recording prohibition, investor-token negative tests | DPDP purpose-limitation and breach-notification timings must be verified with counsel (as of 27 Nov 2026) |
| QA Lead (consulted) | 40 test cases with techniques; matrix pairwise reduction; boundary tests for thresholds | Eval data for the two new intent classes needs bilingual labelling (errata 56) |

---

## 3.4.8 Tags register

| Tag | Type | Statement | Section |
|---|---|---|---|
| ASSUMPTION-320 | Assumption | Growth-column staff sessions are all active at r = 20 requests/min (ASSUMPTION-102 rate applied to every concurrent session) | §3.4.5.1 A |
| ASSUMPTION-321 | Assumption | Opportunity storage ≈ 2.6 KB per row including indexes and evidence links | §3.4.5.1 A |
| ASSUMPTION-322 | Assumption | RC-1 PITR restore of a growth-size database completes within 75 minutes; to be measured in the quarterly drill (verify RDS restore throughput) | §3.4.5.1 B |
| ASSUMPTION-323 | Assumption | Discipline-to-role mapping (React/UX → FE + UX; Django + PostgreSQL → BE + FS remainder; AI → FS; QA → QA; DevOps → DevOps) and focus factor 0.686 derived from Part 8 capacity (398 pd ÷ 580 FTE-days) | §3.4.5.7 B |
| ASSUMPTION-324 | Assumption | "Redis" in the source pack means the Redis protocol, satisfied by Valkey | §3.4.5.1 C |
| ASSUMPTION-325 | Assumption | Pack predecessors H02/H03 of BR-M01 are pre-existing identity hardening items of the reused service; treated as inputs to the identity spike US-0101 (not defined anywhere in the 38 documents) | §3.4.4.1 |
| GAP-320 | Gap | No load profile for the pack's growth column (250 sessions, 1 M opportunities, 100 k actions/day, 100 tenants) | §3.4.5.1 A |
| GAP-321 | Gap | No recovery class for regenerable research data | §3.4.5.1 B |
| GAP-322 | Gap | Adapter ports lack `estimate`/`health` and a `denied` outcome | §3.4.5.2 A |
| GAP-323 | Gap | Agent envelope lacks 7 of the 11 fields in doc 10 | §3.4.5.5 A |
| GAP-324 | Gap | No contract for product events from startups' own delivered products | §3.4.5.1 D |
| GAP-325 | Gap | Workflow definitions have no declared execution-policy block | §3.4.5.4 A |
| GAP-326 | Gap | Reply taxonomy lacks decline and meeting-request classes | §3.4.5.4 D |
| GAP-327 | Gap | No daily-operations runbook; client offboard and data-incident runbooks incomplete | §3.4.5.6 A |
| GAP-328 | Gap | No branch-coverage metric for critical decision code | §3.4.5.6 B |
| GAP-329 | Gap | No technical-debt register | §3.4.5.6 D |
| GAP-330 | Gap | Approval-gate items (38 API definitions, 4 DB confirmations, 138 UI mappings) not tracked | §3.4.5.7 D |
| GAP-331 | Gap | Pack integration candidates (PandaDoc, Crossbeam Skills, Socialinsider, PostHog) not evaluated | §3.4.5.2 F |
| GAP-332 | Gap | No website/portal/Admin URL route map | §3.4.5.2 C |
| GAP-333 | Gap | No composite dashboard load target | §3.4.5.1 A |
| GAP-334 | Gap | No fail-fast rule for mandatory configuration | §3.4.5.3 C |
| GAP-335 | Gap | No lawful meeting-notes summarization path (GAP-143 excludes recordings) | §3.4.5.4 E |
| CONFLICT-320…330 | Conflict | See §3.4.6 | §3.4.6 |
| RECOMMENDATION-320 | Recommendation | Validate the pack's capacity matrix with LT-ENH-B-01…04; buy no capacity before a §3.1.6.4 trigger | §3.4.5.1 A |
| RECOMMENDATION-321 | Recommendation | Adopt recovery classes RC-1…RC-3 with class-ordered restore | §3.4.5.1 B |
| RECOMMENDATION-322 | Recommendation | Adopt agent envelope v1.1 | §3.4.5.5 A |
| RECOMMENDATION-323 | Recommendation | Adopt the product-event ingress allowlist, off by default | §3.4.5.1 D |
| RECOMMENDATION-324 | Recommendation | Build the commercial journey projection as a read model | §3.4.5.1 E |
| RECOMMENDATION-325 | Recommendation | Run the 90-cell workflow regression matrix in SIT from W2 | §3.4.5.4 F |
| RECOMMENDATION-326 | Recommendation | Keep a technical-debt register with monthly review and a 10% capacity reservation for S1/S2 debt | §3.4.5.6 D |
| RECOMMENDATION-327 | Recommendation | Enforce a benchmark record before any paid provider activation | §3.4.5.2 F |
| RECOMMENDATION-328 | Recommendation | Use the pack's discipline shares as a capacity cross-check; skew any Option E hire to backend; schedule the dynamic-field framework before the nine expansion screens | §3.4.5.7 B, C |
| RECOMMENDATION-329 | Recommendation | Adopt four DRF permission base classes with CI enforcement | §3.4.5.2 B |
| RECOMMENDATION-330 | Recommendation | Price per-tenant KMS keys into plans or use per-tenant data keys under a shared CMK for tenants without a contractual need | §3.4.5.1 A |
| RECOMMENDATION-331 | Recommendation | Cite OPT IDs in the "Source" column of implementing artefacts | §3.4.4.4 |
| ADR-100…ADR-109 | ADR | See §3.4.5.9 | §3.4.5.9 |

**Inconsistencies found in earlier parts (reported, not changed).**

| # | Finding | Parts | Suggested fix |
|---|---|---|---|
| 1 | Part 4.2 NFR-082 measures line coverage only, while Part 4.3 §4.33.4 calls it "Coverage" without stating line vs branch | 4.2, 4.3 | State "line coverage" explicitly; add NFR-ENH-B-08 for branch coverage |
| 2 | Part 2.3 BRL-SEQ-02 stops a sequence on any "reply", while Part 7.2 AG-013 has a separate out-of-office class; the rules do not say whether an auto-reply stops or pauses the sequence | 2.3, 7.2 | Clarify in BRL-SEQ-02 that out-of-office auto-replies pause and reschedule (as in §3.4.5.4 D) |
| 3 | Part 3.1 §3.1.12 sizes on DEC-031 users while Part 4.2 LT-11 validates "10× pilot volume": neither covers 250 concurrent sessions | 3.1, 4.2, 6.1 | Add LT-ENH-B profiles (renumbered by Part 6.1) |

---

## 3.4.9 Quality gate

| # | Item | Result | Notes and fixes applied |
|---|---|---|---|
| 1 | Every requirement traced to a source | **Pass** | Every FR-ENH-B, NFR-ENH-B, ADR and story cites its source aspect IDs (doc + section) and the blueprint artefact it extends; the 394 aspects in `B_coverage.csv` each carry a blueprint location |
| 2 | Assumptions, gaps and conflicts tagged and logged | **Pass** | ASSUMPTION-320…325, GAP-320…335, CONFLICT-320…330, RECOMMENDATION-320…331 in §3.4.8; conflicts with proposed resolutions in §3.4.6 |
| 3 | IDs unique and consistent with earlier parts | **Pass** | New IDs use group-B namespaces (FR-ENH-B, US-xx-EBnn, TC-ENH-B, NFR-ENH-B, LT-ENH-B, RB-ENH-B, WQG) and ADR-100…109 (unused before); OPT IDs kept as in the source; no pack KPI IDs used (OKPI naming reserved); grep confirmed none of the new IDs exist in Parts 0–9 |
| 4 | No story lacks AC and no requirement lacks a test | **Pass** | 23 stories: 10 with Gherkin blocks in §3.4.5.8 A, the remaining 13 take their criteria from the referenced pass-criteria tables; 40 test cases cover all 27 FR-ENH-B (FR-ENH-B-025/026 are planning controls verified by TC-ENH-B-040 and the Part 8 gate review) |
| 5 | Negative, edge, security and accessibility cases covered | **Pass** | Negative: TC-ENH-B-019, -020, -022, -027, -035, -038; edge/boundary: -017, -021, -029; security: ingress DLP, token substitution, permission scan; accessibility: no new UI surface beyond routes (route map keeps Part 2.5 WCAG 2.2 AA obligations; dashboards' load target does not change accessible states) — N/A for new UI components |
| 6 | No agent lacks guardrail, fallback, KPI and cost estimate | **Pass** | No new agent is created; the notes-only summary is an AG-015 skill with guardrail (AG-012 block), fallback (L0 draft only), KPI (summary acceptance by author) and cost (< ₹1 per summary, estimate) in §3.4.5.4 E; envelope v1.1 strengthens existing guardrails |
| 7 | Time-sensitive facts flagged "verify" with an as-of date | **Pass** | Model prices, Fargate/EC2 ratio, KMS key price, RDS limits and restore throughput, provider quotas, DPDP/CERT-In timings all flagged "verify … as of 27 Nov 2026" |
| 8 | No restricted data routed to free-tier models | **Pass** | No new Tier 2 routing; notes-only summaries are Tier 1a; product events carry no personal or health data and do not reach a model |
| 9 | Consistent with earlier parts | **Pass** | No earlier part edited; every divergence from the pack is resolved in favour of binding DECs and ADRs, or raised as CONFLICT-320…330 with a proposed resolution; three earlier-part inconsistencies reported in §3.4.8 |

**Status: Part 3 Batch 3.4 complete. Documents 04, 05, 09 and 10 reviewed line by line (394 atomic aspects: 319 covered, 45 partially covered, 15 not covered, 15 in conflict); 27 enhanced FRs, 8 NFRs, 4 load profiles, 3 runbooks, 12 workflow quality gates, 10 ADRs, 23 stories and 40 test cases written; 11 conflicts proposed for coordinator decision.**
