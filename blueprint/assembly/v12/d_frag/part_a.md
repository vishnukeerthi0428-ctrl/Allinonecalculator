# AI Growth Engine: Employee Sales & Marketing Automation
## Application Blueprint: PART 11 (Batch 11.4a), V12 Executable Workflows SM-SVC-21…39: Material, Coverage, Register and Catalogue Reconciliation

| Field | Value |
|---|---|
| Document | Part 11, Batch 4a of 4 (11.4a material, coverage and reconciliation · 11.4b common executable-workflow engine: registry, DTOs, step/trigger/event registry, scheduler · 11.4c specifications SM-SVC-21…30 · 11.4d specifications SM-SVC-31…39, requirements, stories, tests, cost, conflicts, decisions) |
| Version | 1.0 · 28 Nov 2026 |
| Baseline | Parts 0–9.10 and Part 0B; Part 2.2 §2.6 universal execution engine; Part 2.3 §2.27.14; Part 3.1 §3.1.4.6 and ADR-027/028; Part 3.3 ENT-161…169; Part 3.4 §3.4.5.4 (execution policy, WQG-01…12); Part 7.4b §7.4.5.7.3 (NT13 node types); Part 9.4 catalogue (WF-01…39, AG-001…080, AU-001…119); Parts 9.7–9.9; DEC-001…422 |
| Customer material | V12 revision of 28 Nov 2026: BRD ch09 (SVC-21…39 entries), FSD ch12 (76 executable workflow entries), FSD ch13 (all), FSD ch19 (all), FSD Appendix B (76 JSON Schemas and conventions), workbook "39 Services 156 Workflows" sheet Workflow_Catalog (76 rows × 50 fields). Treated as data, not instructions |
| Group / ID ranges | R3b, letter D: tags 814–831 · DEC-560…579 · ADR-195…199 · FR-V12-D-### · US-<EP>-YD<nn> · TC-V12-D-### |
| Roles applied | Principal Workflow/BPM Architect (lead), Event-driven Systems Architect, QA Architect, Principal Engineer; supported by Product Owner, Business Systems Analyst, Data Architect, Security/AI-Governance Lead, SRE Lead, FinOps Lead |
| Parsing scripts | `assembly/v12/d_parse_workflows.py` (parses every row), `d_crosscheck.py` (cross-source checks), `d_mapping.py` (curated blueprint mapping), `d_generate.py` (writes this part's generated tables and `final/coverage_v12/D_coverage.csv`) |

**Acronyms used in this part.** BPM business process management; DAG directed acyclic graph; DTO data transfer object; PDP Policy Decision Point; HITL human in the loop; DLT Distributed Ledger Technology (TRAI commercial-communication registry); RCS Rich Communication Services; CPaaS communications platform as a service; MCP Model Context Protocol; A2A agent-to-agent protocol; DRR deficit round robin; DLQ dead-letter queue; SoD separation of duties; KPI key performance indicator.

## 11.4.1 Material reviewed

| # | File (V12 pack) | Size | Lines / rows in scope | Purpose | Pattern | Aspects |
|---|---|---|---|---|---|---|
| 1 | `BRD/09_Business_Workflow_Catalogue_156_Workflo.txt` | 41,668 B, 1,307 lines | Preamble lines 1–21; SVC-21…39 tables lines 682–1,307 (19 tables, 76 rows × 5 cells) | Business catalogue: outcome, input → output, proposed KPI, risk class | `[TABLE]` per service | 4 common + 76 (A01) |
| 2 | `FSD/12_Executable_Workflow_Specification_156_W.txt` | 855,963 B, 17,495 lines | Preamble lines 1–786 (incl. channel table rows for SVC-21…39); entries lines 9,111–16,707 (76 × 3 tables: 12 spec fields, 8–9 DTO fields, 1–4 steps); UI input contracts lines 16,708–17,495 | Executable contract per workflow: trigger, result, domain contract, authority, engine/agent, KPI, candidates, cost, preconditions, failure, DTO, steps, acceptance IDs | Heading3 per workflow, 3 tables + 2 lines | 31 common + 76 × 14 + 231 steps |
| 3 | `FSD/13_Workflow_Step_Trigger_Event_Registry.txt` | 30,021 B, 918 lines | All: REC-01, REC-09, 13 node patterns, V5 controls (ST-04, FL-01, FL-05, FL-10), 156-row optimization mapping (76 in scope), canonical event v2 (18 fields), 5 trigger rules, walkthrough | Step / trigger / event registry | Tables + prose | 56 common + 76 (A15) |
| 4 | `FSD/19_Automation_Scheduler_Execution_Control.txt` | 4,406 B, 37 lines | All: REC-02, V6 execution context, MT-28, MT-30, V5 preflight, ST-03, FL-06, RT-08, V4 run states and queue rules | Scheduler and execution control | Prose + requirement cards | 19 common |
| 5 | `FSD/AP_Appendix_B_Workflow_DTO_JSON_Schemas_156.txt` | 151,635 B, 157 lines | Header + 76 schemas (lines 83–158) | JSON Schema 2020-12 DTO per workflow | One JSON document per line | 7 common + 155 distinct fields |
| 6 | `src/…39_Services_156_Workflows(1)_csv/Workflow_Catalog.csv` | 160 rows | 76 rows × 50 columns = 3,800 cells | 50-field workflow specification | CSV | 14 common + 19 × 18 service fields + 76 (A16) |
| | **Total** | | | | | **{{N_ASPECTS}} atomic aspects** (each in `final/coverage_v12/D_coverage.csv`) |

**Parsed inventory (programmatic, `d_counts.json`).** 19 services; **76 workflows** (SVC-21-WF01 … SVC-39-WF04); **231 steps** (56 workflows with 3 steps, 12 with 4, 7 with 2, 1 with 1); 620 DTO field rows (one shared schema per service, 155 distinct service-field pairs); **660 acceptance IDs** (50 workflows × 8 families, 26 × 10); 76 original acceptance IDs `…-AT01` (all "not run"); 3,800 workbook cells; 207 UI input controls. Authority classes: **R0 42 · R1 8 · R2 16 · R3 10**. Step executors: Domain agent 68 · Domain service 64 · Policy/validation 35 · Rules/analytics 29 · Identity/reconciliation 16 · Effect adapter 10 · Evidence/ingestion 9. Channel candidates: CRM 52, Partner 20, Website 20, Email 12, Research 12, Voice 8, Social 8, Paid ads 4, SMS/RCS 4. Every parser check passed: no workflow lacks a spec, DTO, steps, acceptance, channel, UI contract, registry, BRD row, schema or workbook row; DTO tables equal schema properties field for field; step counts equal ch13 counts.

**Cross-source checks (`d_crosscheck.py`).** Titles agree across all five sources (76/76). BRD risk class equals FSD authority class (76/76). BRD KPI equals FSD KPI (76/76). BRD output equals workbook output (76/76). Workbook step text equals FSD step actions (76/76). ch13 "rules-labeled / agent-labeled" counts equal FSD executors (76/76). Two V12-internal inconsistencies were found and are resolved in §11.4.4.3 (GAP-821): 13 R2/R3 workflows are labelled "Internal analysis/draft" in the workbook, and 16 R2/R3 workflows have no explicit effect step. One schema design defect is resolved in §11.4b.4 (GAP-824): each service shares one DTO whose output fields are all required, so a workflow cannot legally return the outputs it does not produce.

**Versions.** Workbook "Service version / Workflow version": `2.0-target` for 15 workflows (SVC-21…25 WF01–WF03), `1.0-target` for 61. All App. B schemas are `:v2` and all FSD domain contracts are `@2`. The registry keeps the workbook semantic version separately from the schema version (FR-V12-D-001).

## 11.4.2 Coverage summary

Statuses follow the V12 brief: Covered / Partially covered / Not covered / Conflict before; Matched / Pending Founder decision / Not applicable after. A workflow whose behaviour exists in the blueprint is at most "Partially covered", because the V12 canonical IDs, typed DTO, step IDs, KPIs and acceptance IDs did not exist in the blueprint before this part.

{{COUNTS}}

**Reading the result.** {{N_MATCHED}} aspects are Matched by the specifications in Parts 11.4b–11.4d. {{N_PENDING}} aspects are Pending Founder decision: the voice service SM-SVC-26 (CONFLICT-815), generative image/video/audio in SM-SVC-27 (CONFLICT-819), agent-to-agent negotiation and payment mandates in SM-SVC-28 (CONFLICT-816), price-sensitivity and live pricing experiments in SM-SVC-37 (CONFLICT-817), recording-based coaching in SM-SVC-36-WF03 (CONFLICT-818) and the V12 "L3 bounded mandate" option on the ten R3 workflows (CONFLICT-814). For each, the full specification is still written, and the workflow ships **disabled** with a recommended resolution. Funding for all V12 work in this group is a separate Founder item (CONFLICT-820) that does not change any aspect's specification status.

**Behaviour-level view of the 76 workflows.** 49 already exist in the blueprint in substance (48 partially, 1 fully: SM-SVC-36-WF02 practice against synthetic personas, AG-046); 15 are new and buildable within the safety invariants (marketplace, SMS/RCS, procurement, reputation, agentic catalogue/quote drafts, adaptive onboarding); 12 conflict with a Founder decision or safety invariant.

## 11.4.3 Detailed register

Every aspect is listed individually below: common aspects with full text; workflow, step, service-field and DTO aspects as coded cells (one cell per aspect ID). The CSV holds the full text, location, action and new IDs of all {{N_ASPECTS}} aspects. Covered aspects are included in the coded tables for completeness.

{{REGISTER}}

## 11.4.4 Catalogue reconciliation

### 11.4.4.1 Workflow → blueprint map and registry reconciliation (FSD ch12 × ch13 × blueprint)

Executor counts are in the order P policy/validation, I identity/reconciliation, D domain service, A domain agent, R rules/analytics, E effect adapter, V evidence/ingestion. "Consistent" means ch13 step count and rules/agent cue counts equal the ch12 step table. The ch12 channel column becomes the **service channel allowlist** that the PDP enforces at dispatch (D-F12-020, D-F12-025).

{{RECON}}

### 11.4.4.2 Step executor taxonomy reconciliation (V12 ch12/ch13 vs blueprint NT13 and automations)

| V12 executor (count in scope) | V12 input → output contract | V12 failure code → state | Step class (FSD ch12 V5) | Blueprint node type (Part 7.4b) | Blueprint implementation | Retry class (ST-06) |
|---|---|---|---|---|---|---|
| Policy/validation engine (35) | typed payload + effective policy + consent/budget/entitlement snapshot → `validation {passed, reason_codes, policy_version}` | POLICY_DENIED → BLOCKED; no external effect | Deterministic | NT13-09 `policy.check` | PDP rule sets (AU-009), budget (AU-002), sources (AU-007), compliance pre-check (AU-067), entitlement (AU-042/AU-044) | Validation: never retried |
| Identity/reconciliation engine (16) | scoped object refs + version + evidence_set → `match_result {matched_refs, unmatched_refs, conflict_refs}` | CONFLICT → HELD; uncertain provider outcome reconcile | Deterministic | NT13-07 `logic.compute` (subtypes `logic.dedupe`, `logic.match`, `logic.reconcile`) | AU-015, AU-037, AU-038, AU-074, AU-080, AU-091, AU-100; provider outcome AU-026 | Conflict: no retry; uncertain → RECONCILING |
| Domain service (64) | validated domain payload + prior result → `domain_result {artifact_ref, status, evidence_refs}` | INVALID_STATE → HELD | Deterministic (state write) | NT13-05 `data.write_internal` (NT13-04 for reads) | Django service of the owning module with optimistic revision check (Part 3.4 §3.4.5.3 B) | Invalid state: no retry |
| Domain agent / task router (68) | scoped evidence + approved configuration + prior results → `candidate {artifact_ref, confidence, reason_codes, review_state}` | REVIEW_REQUIRED → AWAITING_APPROVAL | AI inference + human review | NT13-08 `ai.task` followed by NT13-10 `approval.human` or NT13-11 `task.human` | AG-xxx through the gateway (AU-001, AU-003, AU-004); drafts never change live state | Model transient: gateway retry ≤ 2 inside the attempt; quality failure → reviewer |
| Rules/analytics engine (29) | versioned inputs + policy/metric_version → `calculation {value, unit, assumptions, evidence_refs}` | INVALID_METRIC → HELD; never invent missing values | Deterministic | NT13-07 `logic.compute` | AU-017, AU-039, AU-040, AU-041, AU-049, AU-065, AU-085, AU-093, AU-096, AU-102 | Invalid metric: no retry |
| Effect adapter (10) | approved_action_ref + target/version + idempotency_key → `effect_receipt {provider_ref, status, observed_at}` | EFFECT_UNKNOWN → RECONCILING; deny missing grant | Controlled effect | NT13-13 `action.external` | Outbox (ENT-169) → AU-009 dispatch recheck → adapter port v2 (ADR-103) | Uncertain write: reconcile before retry (E-5) |
| Evidence/ingestion engine (9) | permitted source or artifact refs + scope + source policy → `evidence_set {items, source_ref, observed_at, hash, rights}` | SOURCE_DENIED → HELD; transient read retry | Evidence retrieval | NT13-04 `data.read` | AU-007, AU-005, AU-014; knowledge index (cat_chunk) | Transient read: ≤ 3 attempts with jitter |

### 11.4.4.3 V12-internal inconsistencies and their resolution (GAP-821, DEC-570)

The workbook column "External side-effect classification" and the absence of an Effect-adapter step disagree with the FSD authority class for the workflows below. The rule adopted is **stricter wins**: the FSD R-class governs, and for any R2/R3 workflow without an explicit effect step the engine inserts an NT13-10 approval gate before the state change the workflow performs (for example closing a receivable gate, recording a supplier commitment or updating an experiment allocation).

{{INCONSISTENCY}}

### 11.4.4.4 Effect-step catalogue (every external effect in SVC-21…39)

{{EFFECTS}}

### 11.4.4.5 Historical use-case group labels (REC-08) for SVC-21…39

FSD ch12 recovers only the 20 group names with 5 historical entries each; the entries themselves are not in the archive. The registry stores a label-only `historical_group` attribute; no historical entry is claimed as recovered (D-F12-002/003).

| Historical group | Services in this batch (label only) |
|---|---|
| Financial | SM-SVC-21 Payment and reconciliation; SM-SVC-37 Pricing and offer analytics; SM-SVC-39 Procurement |
| Customer lifecycle | SM-SVC-22 Onboarding; SM-SVC-23 Retention and renewal; SM-SVC-33 Customer service and support |
| Optimization | SM-SVC-24 Revenue, attribution and forecast; SM-SVC-30 Conversion rate optimization |
| Documents | SM-SVC-25 Business document and knowledge intelligence |
| Conversation | SM-SVC-26 AI voice and telephony |
| Content marketing | SM-SVC-27 Multimodal creative and localization |
| Conversion | SM-SVC-28 Agentic commerce; SM-SVC-31 Marketplace and e-commerce |
| Qualification | SM-SVC-29 Account-based marketing |
| Onboarding | SM-SVC-32 Partner, distributor and co-selling |
| SaaS | SM-SVC-34 Product-led growth and usage intelligence |
| Market intelligence | SM-SVC-35 Brand reputation and review intelligence |
| AI operations | SM-SVC-36 AI sales enablement and coaching |
| Outreach | SM-SVC-38 SMS, RCS and business messaging |

### 11.4.4.6 Scheduler reconciliation: FSD ch19 vs Celery Beat, outbox and the M55 engine

| V12 requirement (ch19) | Blueprint today | Gap | Enhancement (this part) |
|---|---|---|---|
| REC-02 A110 run timeline: current node, wait reason, reservations, retries, uncertain outcomes, unknown actual cost shown explicitly | A110 live monitor; `aut_run.current_node_key`, `wait_reason`, `cost_reserved`, `cost_actual` (Part 3.3 ENT-162) | No per-step reservation view; unknown actual cost shown as 0 | `aut_step_run.cost_actual_state` ∈ {known, unknown, not_applicable}; timeline API (FR-V12-D-018) |
| V6 execution context stored on the run; configuration version checked before approval | Pinned workflow revision (BRL-AUT-03) | Business context and configuration version not stored | `aut_run.business_context` (BusinessContext v1) and `config_revision_id`; approval rejects a stale configuration (FR-V12-D-018) |
| MT-28 concurrency and fair queues per tenant/company; no shared mutable context | ≤ 20 concurrent runs per startup (Part 3.1); per-provider bulkheads (Part 3.2 IP-09); canonical queues (DEC-321) | No fairness between tenants inside a queue | Weighted deficit round robin per (tenant, company) inside each queue (ADR-199; FR-V12-D-019) |
| MT-30 company / offering / workflow budgets + tenant aggregate cap; currency, period, time zone; atomic reservation | AU-002 reservation per tenant/startup/agent; DEC-008 ceilings | No offering/service/workflow levels; no unit caps | Five-level budget hierarchy reserved atomically in one transaction (RECOMMENDATION-830; FR-V12-D-020) |
| V5 preflight before scheduling (schema, authority, entitlement, connector, source rights, budget, graph, effect class) | WQG-01…12 at activation; PDP at plan and dispatch time | Run-level preflight order not fixed | Fixed 9-step preflight (§11.4b.5.4; FR-V12-D-007) |
| ST-03 workload bulkheads; noisy tenant cannot starve another | Provider bulkheads only | Tenant bulkheads missing | Per-tenant in-flight cap per queue + DRR (FR-V12-D-019) |
| FL-06 dependency-aware parallel DAG with joins; cancellation propagates | DAG interpreter executes steps sequentially as Celery tasks | No parallel branches or joins | `parallel` and `join` control nodes for read/compute steps only (FR-V12-D-021) |
| RT-08 customer-controlled schedules (scoped pause, time-zone cadence, preferences) | `aut_trigger.state = paused`, timezone column | No tenant-facing schedule controls or preference windows | Schedule controls in A109 / W34 for R12 within policy (FR-V12-D-022) |
| Run states REQUESTED → … → COMPLETED with HELD / BLOCKED / FAILED_RETRYABLE / FAILED_TERMINAL / CANCELED | `aut_run.state` ∈ {pending, running, waiting, held, paused, reconciling, failed, succeeded, cancelled} | Different names and no EXECUTING_EFFECT / BLOCKED | V12 states canonical with mapping (DEC-561; ADR-197) |
| Optimistic version on transitions; unique effect ledger; terminal immutable except authorized reconciliation adjustment | UQ-IDEM-11; lease fencing token (Part 3.4) | No adjustment record for terminal runs | `aut_run_adjustment` append-only record with R08/R11 approval (DEC-561) |
| Queue by tenant and provider concurrency; bounded backoff with jitter; DLQ review | DEC-321 bounded retries and dead-letter path; Part 3.2 §3.2.7.2 | — | Unchanged; bound to executor retry classes |
| Heartbeats and abandoned-job recovery | Lease with fencing (Part 3.4 §3.4.5.4 A) | No heartbeat or reaper | 30 s heartbeat; reaper reclaims after 3 missed beats; external call in flight → RECONCILING (FR-V12-D-004) |
| Celery Beat single active scheduler | ADR-028 minute tick; DEC-321 leader lock with fencing; DEC-421 keeps Celery/Beat on AWS ap-south-1 | Misfire policy is "recover once" only | `misfire_policy` ∈ {skip, reschedule_once}; never burst (DEC-564) |

### 11.4.4.7 Trigger and event registry reconciliation: FSD ch13 vs Part 3.2 envelope, `aut_trigger`, `ops_outbox`

| V12 item | Blueprint item | Status before | Resolution |
|---|---|---|---|
| Canonical event v2 (18 fields) | Part 3.2 §3.2.3.1 envelope + Part 3.4 §3.4.5.2 E additions | 10 fields covered, 2 partial, 6 missing (`service_id`, `workflow_id`, `workflow_version`, `source_ref`, `approval_ref`, plus `received_at`/`policy_version` on all events) | Envelope v2 adopted; old names kept as aliases for one schema major (DEC-563; ADR-196) |
| Trigger: Manual | NT13-03 `trigger.manual`; `aut_trigger.trigger_kind = manual` | Covered | Adds released-entitlement check at API-V2-RUN |
| Trigger: Scheduled (time zone + UTC next run; per-tenant concurrency; misfire skip or reschedule, never burst) | NT13-02; ADR-028; AU-028 "recover once" | Partially covered | `misfire_policy`; `next_fire_at_utc`; per-tenant concurrency from the fair scheduler |
| Trigger: Event (verified inbox, schema/version, causal correlation, dedup) | NT13-01; `aut_trigger.event_type`; UQ-IDEM-12 | Covered | Inbox table `ops_inbox` added for symmetry with the outbox (FR-V12-D-010) |
| Trigger: Provider callback (signature, timestamp, replay, account mapping, monotonic state, reconciliation) | Part 3.2 webhook verification; `int_provider_event`; AU-026 | Covered | Bound as trigger kind `provider_callback` |
| Trigger: Child workflow (registered dependency, optional upstream input, bounded depth, cycle detection) | None | Not covered | `child_workflow` kind; dependency table; depth ≤ 3; cycle check at activation (WQG-01) |
| REC-01 trigger draft fields (requester, reviewer, test evidence) | `aut_trigger` has no requester/reviewer/test evidence | Partially covered | Columns added; enable requires tested state and reviewer ≠ requester |
| 13 V10 node patterns | NT13-01…13 | Partially covered | Mapping table in §11.4b.5.1; "Reconcile" becomes NT13-07 subtype `logic.reconcile` (RECOMMENDATION-828) |
| Event delivery: scoped unique key + transaction outbox; webhook authenticity | E-2, E-4, `ops_outbox` UQ-IDEM-13 | Covered | Unchanged |

### 11.4.4.8 Number reconciliation

| Quantity | V12 statement | Parsed in scope | Blueprint after this part |
|---|---|---|---|
| Workflows | 156 (ch12, ch13 FL-01) | 76 (SVC-21…39) | 76 registered with V12 IDs; mapped to WF-01…39 journeys (DEC-560) |
| Steps | 517 step contracts (ch12 V5/V6) | 231 | 231 STEP IDs bound to NT13 types and handlers |
| DTO schemas | 156, all meta-schema valid (App. B) | 76 parsed, 76 valid JSON; 19 distinct per-service schemas | v2 registered; v3 projection per workflow (DEC-565) |
| Acceptance IDs | 8 or 10 per workflow (ch12) | 660 + 76 AT01 | Mapped to TC-V12-D-101…111 archetype instances |
| Workbook fields | 50 per workflow | 3,800 cells | Per-workflow fields in §11.4c/d; service fields in service cards |
| Historical groups | 20 × 5 = 100 entries | 13 groups used as labels | Label only (REC-08) |

## Quality gate: Batch 11.4a

| # | Check | Result | Notes and fixes applied |
|---|---|---|---|
| 1 | Every requirement traced to a source | Pass | Each aspect carries its V12 chapter/section and blueprint location; CSV has {{N_ASPECTS}} rows |
| 2 | Assumptions, gaps, conflicts tagged and logged | Pass | Tags 814–831 used; register in Part 11.4d §11.4.9 |
| 3 | IDs unique and consistent | Pass | Aspect IDs asserted unique by `d_generate.py`; V12 IDs kept literally |
| 4 | No story lacks AC and no requirement lacks a test | N/A in this file | Stories and tests in Parts 11.4b/11.4d |
| 5 | Negative, edge, security, accessibility cases | Pass | Inconsistencies, conflicts and effect steps catalogued |
| 6 | No agent lacks guardrail, fallback, KPI, cost | N/A | No new agents (AG ranges belong to groups F and M); existing agents reused |
| 7 | Time-sensitive facts flagged | Pass | No prices or regulatory dates stated in this file |
| 8 | No restricted data to free-tier models | Pass | Tier 2 marked not eligible for every workflow handling personal or confidential data |
| 9 | Consistent with earlier parts | Pass | Mappings cite Parts 2.2, 2.3, 3.1–3.4, 7.4b, 9.4, 9.7–9.9 |

**Status: Part 11 Batch 11.4a complete. {{N_ASPECTS}} aspects inventoried and reconciled; {{N_MATCHED}} Matched, {{N_PENDING}} Pending Founder decision.**
