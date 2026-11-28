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
| | **Total** | | | | | **2075 atomic aspects** (each in `final/coverage_v12/D_coverage.csv`) |

**Parsed inventory (programmatic, `d_counts.json`).** 19 services; **76 workflows** (SVC-21-WF01 … SVC-39-WF04); **231 steps** (56 workflows with 3 steps, 12 with 4, 7 with 2, 1 with 1); 620 DTO field rows (one shared schema per service, 155 distinct service-field pairs); **660 acceptance IDs** (50 workflows × 8 families, 26 × 10); 76 original acceptance IDs `…-AT01` (all "not run"); 3,800 workbook cells; 207 UI input controls. Authority classes: **R0 42 · R1 8 · R2 16 · R3 10**. Step executors: Domain agent 68 · Domain service 64 · Policy/validation 35 · Rules/analytics 29 · Identity/reconciliation 16 · Effect adapter 10 · Evidence/ingestion 9. Channel candidates: CRM 52, Partner 20, Website 20, Email 12, Research 12, Voice 8, Social 8, Paid ads 4, SMS/RCS 4. Every parser check passed: no workflow lacks a spec, DTO, steps, acceptance, channel, UI contract, registry, BRD row, schema or workbook row; DTO tables equal schema properties field for field; step counts equal ch13 counts.

**Cross-source checks (`d_crosscheck.py`).** Titles agree across all five sources (76/76). BRD risk class equals FSD authority class (76/76). BRD KPI equals FSD KPI (76/76). BRD output equals workbook output (76/76). Workbook step text equals FSD step actions (76/76). ch13 "rules-labeled / agent-labeled" counts equal FSD executors (76/76). Two V12-internal inconsistencies were found and are resolved in §11.4.4.3 (GAP-821): 13 R2/R3 workflows are labelled "Internal analysis/draft" in the workbook, and 16 R2/R3 workflows have no explicit effect step. One schema design defect is resolved in §11.4b.4 (GAP-824): each service shares one DTO whose output fields are all required, so a workflow cannot legally return the outputs it does not produce.

**Versions.** Workbook "Service version / Workflow version": `2.0-target` for 15 workflows (SVC-21…25 WF01–WF03), `1.0-target` for 61. All App. B schemas are `:v2` and all FSD domain contracts are `@2`. The registry keeps the workbook semantic version separately from the schema version (FR-V12-D-001).

## 11.4.2 Coverage summary

Statuses follow the V12 brief: Covered / Partially covered / Not covered / Conflict before; Matched / Pending Founder decision / Not applicable after. A workflow whose behaviour exists in the blueprint is at most "Partially covered", because the V12 canonical IDs, typed DTO, step IDs, KPIs and acceptance IDs did not exist in the blueprint before this part. *(v1.2: every item counted here as "Pending Founder decision" was adopted by DEC-770…791 — Part 11.14; read as Adopted. Part 11.25.)*

| Status | Before | After |
|---|---|---|
| Covered | 59 | 0 |
| Partially covered | 1175 | 0 |
| Not covered | 742 | 0 |
| Conflict | 99 | 0 |
| Matched | 0 | 1976 |
| Pending Founder decision | 0 | 99 |
| Not applicable | 0 | 0 |
| **Total** | **2075** | **2075** |

| Source chapter | Aspects | Before: Covered / Partial / Not / Conflict | After: Matched / Pending Founder |
|---|---|---|---|
| 09 Business Workflow Catalogue | 80 | 0 / 51 / 17 / 12 | 68 / 12 |
| 12 Executable Workflow Specification | 1250 | 26 / 667 / 473 / 84 | 1166 / 84 |
| 13 Workflow Step, Trigger & Event Registry | 132 | 23 / 25 / 84 / 0 | 132 / 0 |
| 19 Automation Scheduler & Execution Control | 19 | 5 / 13 / 1 / 0 | 19 / 0 |
| Appendix B Workflow DTO JSON Schemas | 162 | 0 / 0 / 162 / 0 | 162 / 0 |
| Workflow_Catalog (50-field) | 432 | 5 / 419 / 5 / 3 | 429 / 3 |

| Service | Workflows | Steps | Behaviour before (C/P/N/X) | Aspects | Pending Founder after |
|---|---|---|---|---|---|
| SM-SVC-21 Payment, Invoice & Reconciliation Automation | 4 | 14 | 0 / 4 / 0 / 0 | 104 | 2 |
| SM-SVC-22 Customer, Partner & Institutional Onboarding Automation | 4 | 14 | 0 / 3 / 1 / 0 | 104 | 0 |
| SM-SVC-23 Customer Retention, Renewal & Feedback Automation | 4 | 13 | 0 / 4 / 0 / 0 | 103 | 0 |
| SM-SVC-24 Revenue, Attribution & Sales Forecast Automation | 4 | 14 | 0 / 4 / 0 / 0 | 105 | 0 |
| SM-SVC-25 Business Document & Knowledge Intelligence Automation | 4 | 16 | 0 / 4 / 0 / 0 | 106 | 0 |
| SM-SVC-26 AI Voice & Intelligent Telephony Automation | 4 | 12 | 0 / 0 / 0 / 4 | 102 | 38 |
| SM-SVC-27 Multimodal Creative & Localization Automation | 4 | 12 | 0 / 1 / 0 / 3 | 102 | 19 |
| SM-SVC-28 Agentic Commerce & AI-to-AI Business Transaction Automation | 4 | 12 | 0 / 0 / 2 / 2 | 102 | 14 |
| SM-SVC-29 Account-Based Marketing & Enterprise Buying Group Automation | 4 | 10 | 0 / 4 / 0 / 0 | 100 | 0 |
| SM-SVC-30 Conversion Rate Optimization & Intelligent Experimentation Automation | 4 | 11 | 0 / 4 / 0 / 0 | 102 | 1 |
| SM-SVC-31 Marketplace & E-commerce Channel Operations Automation | 4 | 11 | 0 / 1 / 3 / 0 | 101 | 2 |
| SM-SVC-32 Partner, Distributor & Co-Selling Automation | 4 | 12 | 0 / 4 / 0 / 0 | 102 | 1 |
| SM-SVC-33 Customer Service & Support Operations Automation | 4 | 12 | 0 / 4 / 0 / 0 | 103 | 0 |
| SM-SVC-34 Product-Led Growth & Usage Intelligence Automation | 4 | 10 | 0 / 4 / 0 / 0 | 100 | 0 |
| SM-SVC-35 Brand Reputation & Review Intelligence Automation | 4 | 12 | 0 / 1 / 3 / 0 | 102 | 0 |
| SM-SVC-36 AI Sales Enablement & Coaching Automation | 4 | 12 | 1 / 2 / 0 / 1 | 102 | 6 |
| SM-SVC-37 Pricing, Offer & Revenue Optimization Automation | 4 | 10 | 0 / 2 / 0 / 2 | 100 | 15 |
| SM-SVC-38 SMS, RCS & Business Messaging Automation | 4 | 11 | 0 / 0 / 4 / 0 | 101 | 0 |
| SM-SVC-39 Procurement & Supplier Management Automation | 4 | 13 | 0 / 2 / 2 / 0 | 103 | 1 |

**Reading the result.** 1976 aspects are Matched by the specifications in Parts 11.4b–11.4d. 99 aspects are Pending Founder decision: the voice service SM-SVC-26 (CONFLICT-815), generative image/video/audio in SM-SVC-27 (CONFLICT-819), agent-to-agent negotiation and payment mandates in SM-SVC-28 (CONFLICT-816), price-sensitivity and live pricing experiments in SM-SVC-37 (CONFLICT-817), recording-based coaching in SM-SVC-36-WF03 (CONFLICT-818) and the V12 "L3 bounded mandate" option on the ten R3 workflows (CONFLICT-814). For each, the full specification is still written, and the workflow ships **disabled** with a recommended resolution. Funding for all V12 work in this group is a separate Founder item (CONFLICT-820) that does not change any aspect's specification status. *(v1.2: every item counted here as "Pending Founder decision" was adopted by DEC-770…791 — Part 11.14; read as Adopted. Part 11.25.)*

**Behaviour-level view of the 76 workflows.** 49 already exist in the blueprint in substance (48 partially, 1 fully: SM-SVC-36-WF02 practice against synthetic personas, AG-046); 15 are new and buildable within the safety invariants (marketplace, SMS/RCS, procurement, reputation, agentic catalogue/quote drafts, adaptive onboarding); 12 conflict with a Founder decision or safety invariant.

## 11.4.3 Detailed register

Every aspect is listed individually below: common aspects with full text; workflow, step, service-field and DTO aspects as coded cells (one cell per aspect ID). The CSV holds the full text, location, action and new IDs of all 2075 aspects. Covered aspects are included in the coded tables for completeness.

#### 11.4.3.1 Common aspects (FSD ch12 preamble, ch13, ch19, BRD ch09 preamble, Appendix B conventions, workbook common fields)

| Aspect ID | Summary | Before | Blueprint location | Action | New IDs | After |
|---|---|---|---|---|---|---|
| D-F12-001 | REC-05 A113 canonical workflow-derived template: draft/validate/test/reviewer publish/retire; unentitled or untested draft cannot be published; no extra service SKU | Partially covered | Part 3.1 §3.1.4.6 A113; Part 3.4 §3.4.5.4 B WQG-01…12 | Template = parameter set over a registered workflow; publish gated by entitlement + WQG-09/10 evidence | FR-V12-D-013; DEC-569 | Matched |
| D-F12-002 | REC-08 map historical use-case group labels to the current registry; no duplicated workflow or fabricated library | Not covered | None | Group-label mapping table for SVC-21…39 (§11.4a.4.5); no recovered entries claimed | FR-V12-D-025 | Matched |
| D-F12-003 | 20 historical groups × 5 entries (100) and 20 industry templates not enumerated; current definitions canonical | Not covered | None | Recorded as label-only taxonomy attribute `historical_group` on registry rows | FR-V12-D-025 | Matched |
| D-F12-004 | One versioned definition per canonical workflow; BusinessContext DTO (tenant; organization; company; division; brand; offering; market; account; campaign/config; SKU/workflow/version; actor; policy sn | Partially covered | Part 2.3 BRL-AUT-03 pinned revision; Part 3.3 aut_run | BusinessContext envelope defined (§11.4b.4) and stored as run snapshot | FR-V12-D-013; DEC-569 | Matched |
| D-F12-005 | Reuse 517 step references; never duplicate definitions for a new customer (231 of the 517 are in SVC-21…39) | Not covered | None | 231 STEP IDs registered once; tenants get parameter sets only | DEC-560; FR-V12-D-001 | Matched |
| D-F12-006 | Industry templates are versioned approved parameter sets not copied code; validate rights/claims/outputs in context (FSD-POL-V6-PRECHECK / ARTIFACT) | Partially covered | Part 3.1 A113 templates | Adopted (DEC-569) | FR-V12-D-013 | Matched |
| D-F12-007 | MT-29 industry/business workflow templates; MT-TC-MT-29 apply template to two businesses and definition count stays 156 | Not covered | None | Test TC-V12-D-013 | TC-V12-D-013 | Matched |
| D-F12-008 | Classify each step deterministic / evidence retrieval / AI inference / human review / controlled effect; only inference uses a model; persist estimate; actual; accepted result; retry state; evidence | Partially covered | Part 7.1 principle 1; AU-001 | Seven V12 executor kinds mapped to the five step classes and NT13 (DEC-562) | DEC-562; FR-V12-D-003 | Matched |
| D-F12-009 | FL-02 canonical typed input contracts; OPT-TC-FL-02 invalid schema blocked with field errors | Not covered | None | App. B schemas registered and enforced (DEC-565) | FR-V12-D-002; TC-V12-D-002 | Matched |
| D-F12-010 | FL-03 map every step ID to executor/inputs/outputs/transition/timeout/recovery/tests; incomplete handler blocks release | Partially covered | Part 3.4 WQG-01 | Handler manifest per STEP ID; release gate | FR-V12-D-003; TC-V12-D-003 | Matched |
| D-F12-011 | FL-07 pre-execution simulation; dry run returns hold or plan; zero external effects | Covered | Part 2.2 E-6; Part 3.4 WQG-09 | Bound to API-V2-RUN mode=dry_run | FR-V12-D-007 | Matched |
| D-F12-012 | FL-08 confidence-based routing; uncertain output to reviewer | Partially covered | Part 7.2 agent thresholds | Per-step confidence floor in handler manifest | FR-V12-D-008; TC-V12-D-008 | Matched |
| D-F12-013 | FL-11 cancellation and compensation; unstarted / reversible / irreversible effects | Partially covered | Part 2.2 E-5; AU-026 | Effect reversibility class on every effect step; API-V2-CANCEL | FR-V12-D-012; TC-V12-D-012 | Matched |
| D-F12-014 | FL-12 industry workflow templates with explicit review; no automatic entitlement or policy override | Partially covered | A113 | Adopted | FR-V12-D-013 | Matched |
| D-F12-015 | FL-13 step-level AI evaluation before accepting outputs or effects | Partially covered | AU-003; AG-002 | Step acceptance record (schema; evidence; confidence; policy) | FR-V12-D-014; TC-V12-D-014 | Matched |
| D-F12-016 | FL-14 workflow optimization recommendations with baseline; test result; rollback | Partially covered | AU-068; AG-080 | Extended to workflow level using run ledger | FR-V12-D-015 | Matched |
| D-F12-017 | Role separation requester / reviewer / auditor; separation of duties server-side | Covered | Part 2.3 CA-APPROVE; R15 | Bound to API-V2-APPROVAL | DEC-561 | Matched |
| D-F12-018 | Budget and allowance: monthly units and monetary reservation; production atomic period ledger | Partially covered | AU-002; AU-042 | Hierarchical budget ledger (FR-V12-D-020) | FR-V12-D-020 | Matched |
| D-F12-019 | Scope: company entitlement and pause; portfolio aggregates only; external AI bid purpose denied for non-AppNAI tenants | Covered | DEC-055; BR-S001 | Unchanged | — | Matched |
| D-F12-020 | Channel: proposed service allowlist (e.g. SM-SVC-14 paid ads only); adapter/consent/source rights/provider approval before live action | Partially covered | Part 3.2 adapter registry | Service channel allowlist = ch12 channel candidates (§11.4a.4.1) | FR-V12-D-1xx | Matched |
| D-F12-021 | Duplicate / failures: duplicate held; missing rights / budget / consent / entitlement held; transient failed; uncertain held in reconciliation | Covered | Part 2.2 E-4; E-5 | Mapped to V12 states (DEC-561) | DEC-561 | Matched |
| D-F12-022 | Approval: distinct roles; 15-minute sample expiry; recheck budget at review; production exact digest and revocation | Partially covered | Part 2.2 E-8 | Approval mandate record with expiry (FR-V12-D-009); default expiry configurable | FR-V12-D-009 | Matched |
| D-F12-023 | Recovery: pause moves active runs to Held; cancel / retry / reconcile; production rechecks policy | Partially covered | Part 2.3 §2.27.14 | Adopted in run state model v2 (DEC-561) | DEC-561 | Matched |
| D-F12-024 | Input contract generated from required-input descriptions; physical DTO validators pending approval | Not covered | None | Replaced by App. B schemas; UI form generated from schema | FR-V12-D-002; FR-V12-D-023 | Matched |
| D-F12-025 | Channel candidates and execution contracts for 156 workflows (76 in scope; all "FSD chapter 12; simulation only") | Not covered | None | Channel allowlist table §11.4a.4.1 | FR-V12-D-1xx | Matched |
| D-F12-026 | Common UI fields: reference; trigger; channel; business purpose; integer units; mode L0–L4; sample cost/unit; cap; optional scheduled date; scenario; synthetic-data acknowledgement; no L0–L4 selection | Partially covered | A110; A033 | Run request form spec (FR-V12-D-023) | FR-V12-D-023 | Matched |
| D-F12-027 | Common contract on every workflow: precheck (schema; scope; source; version; policy; quota; reserve) and finalize; idempotency = tenant/company/run/version/step/target digest; read/AI timeouts 30 s/90 | Partially covered | Part 3.4 execution_policy; BRL-AUT-06 | Adopted as engine defaults (§11.4b.5) | FR-V12-D-005; FR-V12-D-006 | Matched |
| D-F12-028 | Per workflow 8 TC families (R0/R1) or 10 (R2/R3) plus original AT01 not run (chapter 33) | Not covered | None | Archetypes TC-V12-D-101…111 (DEC-568) | DEC-568 | Matched |
| D-F12-029 | API-V2-RUN / RESULT / APPROVAL and DB-V2-RUN / STEP / ARTIFACT / EVIDENCE / EFFECT per domain; not a deployed endpoint | Partially covered | Part 3.2 runs API; Part 3.3 aut_run | Mapped to blueprint tables (ADR-195) | DEC-561; ADR-195 | Matched |
| D-F12-030 | Active (SKU) entitlement; correct tenant/startup; validated inputs; approved policy; stub/synthetic fixtures; live entitlement / consent / source rights / policy / budget / scoped refs | Covered | Part 2.2 E-1…E-3; Part 3.4 WQG | Unchanged | — | Matched |
| D-F12-031 | Bounded retry for safe failures; reconcile uncertain outcome before retry; pause; route reviewer; log; emergency stop; no effect without authorization; ambiguous effect RECONCILING | Covered | Part 2.2 E-5; E-7; AU-025; AU-026 | Unchanged | — | Matched |
| D-F13-001 | REC-01 A109 versioned trigger (manual / scheduled / webhook event); timezone; condition; dedupe window; tested before reviewer approval; invalid schedule / duplicate / unapproved cannot start a real e | Partially covered | Part 3.3 aut_trigger (draft/tested/enabled); dedup_window_s | Trigger registry v2 (FR-V12-D-017) | FR-V12-D-017; TC-V12-D-017 | Matched |
| D-F13-002 | REC-09 candidate reusable node contracts: typed inputs/outputs; side-effect classification; failure routes; validate schema and effect policy before handler execution | Partially covered | Part 7.4b NT13-01…13 | V10 patterns mapped to NT13 (RECOMMENDATION-828) | FR-V12-D-024 | Matched |
| D-F13-003 | Trigger: event envelope → validated event; no effect | Partially covered | NT13-01/02/03 | Mapped | FR-V12-D-024 | Matched |
| D-F13-004 | Filter: typed record + predicate → eligible or held; no effect | Partially covered | NT13-06 | Mapped | FR-V12-D-024 | Matched |
| D-F13-005 | Research: permitted query + source rights → evidence references; read only | Partially covered | NT13-04 + AU-007 | Mapped | FR-V12-D-024 | Matched |
| D-F13-006 | Extract: evidence reference + schema → typed candidate; no effect | Partially covered | NT13-08 | Mapped | FR-V12-D-024 | Matched |
| D-F13-007 | Deduplicate: scoped identity + key → canonical reference; no effect | Partially covered | NT13-07 | Mapped | FR-V12-D-024 | Matched |
| D-F13-008 | Score: rubric + evidence → score and explanation; no effect | Partially covered | NT13-07 (+ NT13-08 explanation) | Mapped | FR-V12-D-024 | Matched |
| D-F13-009 | Route: scope + decision → next step; no effect | Partially covered | NT13-06 | Mapped | FR-V12-D-024 | Matched |
| D-F13-010 | Draft: approved context + prompt → versioned draft; no effect | Partially covered | NT13-08 | Mapped | FR-V12-D-024 | Matched |
| D-F13-011 | Validate: candidate + policy → validation evidence; no effect | Partially covered | NT13-09 | Mapped | FR-V12-D-024 | Matched |
| D-F13-012 | Approve: exact digest + mandate → reviewer decision; no effect | Partially covered | NT13-10 | Mapped | FR-V12-D-024 | Matched |
| D-F13-013 | Dispatch: authorized intent + key → uncertain or receipt reference; external effect via gateway | Partially covered | NT13-13 | Mapped | FR-V12-D-024 | Matched |
| D-F13-014 | Reconcile: intent + receipt → matched or exception; controlled state update | Partially covered | AU-026 (no NT13 type) | New subtype `logic.compute:reconcile` under NT13-07 with W1 write | FR-V12-D-024 | Matched |
| D-F13-015 | Wait / stop: checkpoint + stop condition → held or resumed; no effect | Partially covered | NT13-12 | Mapped | FR-V12-D-024 | Matched |
| D-F13-016 | Trigger draft fields: scope; workflow; event type; IANA zone; schedule; predicate; dedupe duration; revision; requester; test evidence; reviewer | Partially covered | aut_trigger (no requester / reviewer / test evidence) | Columns added (§11.4b.6) | FR-V12-D-017 | Matched |
| D-F13-017 | Event delivery uses a scoped unique key and transaction outbox; webhook authenticity mandatory in production | Covered | Part 2.2 E-2; E-4; ops_outbox | Unchanged | — | Matched |
| D-F13-018 | ST-04 durable checkpoints: persist step state / version / artifact refs / effect status before acknowledgement; resume safe step; OPT-TC-ST-04 | Partially covered | aut_step_run; lease fencing (Part 3.4) | Checkpoint contract (§11.4b.5) | FR-V12-D-004; TC-V12-D-004 | Matched |
| D-F13-019 | FL-01 machine-readable registry: version 156 definitions; immutable run snapshots; stable SKU and workflow IDs; OPT-TC-FL-01 | Partially covered | aut_workflow / aut_workflow_revision | Registry with V12 IDs (§11.4b.3) | FR-V12-D-001; TC-V12-D-001 | Matched |
| D-F13-020 | FL-05 event-driven orchestration with verified inbox/outbox and schedules; polling only if required; duplicate webhook deduped | Partially covered | ops_outbox; int_provider_event | Inbox table + trigger router (§11.4b.6) | FR-V12-D-010; TC-V12-D-010 | Matched |
| D-F13-021 | FL-10 tenant-scoped cross-workflow events with version and correlation; target entitlement or equivalent input required | Not covered | None | Child-workflow trigger + entitlement check (DEC-564) | FR-V12-D-011; TC-V12-D-011 | Matched |
| D-F13-022 | Per-workflow rows: steps; executor cues; V5 control links (76 in scope) | Not covered | None | Reconciled 76/76 with ch12 (§11.4a.4.2) | FR-V12-D-001 | Matched |
| D-F13-023 | AI-01 deterministic-first execution; golden fixtures zero model calls | Covered | Part 7.1 principle 1; AU-001 Tier 0 | Unchanged | — | Matched |
| D-F13-024 | AI-02 multi-tier router: cheapest eligible evaluated model | Covered | AU-001; DEC-418 | Unchanged (Claude primary per DEC-418) | — | Matched |
| D-F13-025 | AI-06 dynamic context budgeting: reserve output and safety margin; trim irrelevant evidence | Partially covered | Part 7.3 prompt-size rules | Per-step context budget in handler manifest | FR-V12-D-003 | Matched |
| D-F13-026 | AI-12 agent-loop termination: max steps / tool calls / time / tokens; repeated action detection | Covered | DEC-384; AU-053 | Unchanged | — | Matched |
| D-F13-027 | AI-15 quality-adjusted provider benchmarking | Covered | AU-045; FR-ENH-A-006 | Unchanged | — | Matched |
| D-F13-028 | FL-09 persistent approval mandates: actor; resource; payload digest; action; amount; policy; expiry; revocation | Partially covered | Part 2.2 E-8 approval hash | Mandate record (§11.4b.5) | FR-V12-D-009; TC-V12-D-009 | Matched |
| D-F13-029 | ST-05 authoritative idempotency and reconciliation | Covered | Part 3.3 UQ-IDEM-11/12/13 | Unchanged | — | Matched |
| D-F13-030 | ST-06 intelligent retry policy: validation / transient read / throttle / uncertain write | Covered | Part 3.2 §3.2.7.2 | Bound to executor retry classes | FR-V12-D-006 | Matched |
| D-F13-031 | event_id UUID | Covered | Part 3.2 §3.2.3.1 id | Renamed alias | DEC-563 | Matched |
| D-F13-032 | event_type enum | Covered | type | Alias | DEC-563 | Matched |
| D-F13-033 | schema_version | Covered | schema_version | Unchanged | DEC-563 | Matched |
| D-F13-034 | tenant_id | Covered | tenant_id | Unchanged | DEC-563 | Matched |
| D-F13-035 | company_id | Covered | startup_id (ASSUMPTION-825) | Alias | DEC-563 | Matched |
| D-F13-036 | service_id | Not covered | None | Added | DEC-563 | Matched |
| D-F13-037 | workflow_id | Not covered | run_id only | Added | DEC-563 | Matched |
| D-F13-038 | workflow_version | Not covered | None | Added | DEC-563 | Matched |
| D-F13-039 | actor_ref | Covered | actor {type; id} | Alias | DEC-563 | Matched |
| D-F13-040 | source_ref | Not covered | None | Added (connector/source reference) | DEC-563 | Matched |
| D-F13-041 | occurred_at UTC | Covered | occurred_at | Unchanged | DEC-563 | Matched |
| D-F13-042 | received_at UTC | Partially covered | inbound events only | Added to all events | DEC-563 | Matched |
| D-F13-043 | correlation_id | Covered | correlation_id | Unchanged | DEC-563 | Matched |
| D-F13-044 | causation_id | Covered | causation_id | Unchanged | DEC-563 | Matched |
| D-F13-045 | idempotency_key | Covered | Part 3.4 §3.4.5.2 E header | Unchanged | DEC-563 | Matched |
| D-F13-046 | policy_version | Partially covered | outbound intents only (Part 3.4 D) | Added to all events | DEC-563 | Matched |
| D-F13-047 | approval_ref nullable | Not covered | approval on intent only | Added | DEC-563 | Matched |
| D-F13-048 | payload_ref | Covered | data (references and digests) | Alias | DEC-563 | Matched |
| D-F13-049 | Tenant derived from trusted auth or verified connector mapping; never raw event | Covered | Part 2.2 E-1 | Unchanged | — | Matched |
| D-F13-050 | Unique scoped event ID and provider event; reject mismatched version/scope | Covered | UQ-IDEM; Part 3.2 webhook dedupe | Unchanged | — | Matched |
| D-F13-051 | Manual: authenticated user; released entitlement; typed inputs | Covered | NT13-03; PDP | Entitlement check added to API-V2-RUN | DEC-564 | Matched |
| D-F13-052 | Scheduled: time zone + UTC next execution; per-tenant concurrency; misfire skip or reschedule; never burst | Partially covered | ADR-028; AU-028 recover once | Misfire policy enum (DEC-564) | DEC-564; TC-V12-D-016 | Matched |
| D-F13-053 | Event: verified inbox; schema/version; causal correlation; dedup | Covered | FR-A109; UQ-IDEM-12 | Unchanged | DEC-564 | Matched |
| D-F13-054 | Provider callback: signature; timestamp; replay check; account mapping; monotonic state; reconciliation | Covered | Part 3.2 webhook verification; AU-026 | Unchanged | DEC-564 | Matched |
| D-F13-055 | Child workflow: explicit registered dependency; optional upstream input; bounded depth and cycle detection | Not covered | None | Added (depth ≤ 3) | DEC-564; FR-V12-D-011 | Matched |
| D-F13-056 | Workflow detail next/previous/restart walkthrough; run inspection shows input snapshot / role / period / budget / expiry; production uses persisted per-step state | Partially covered | A110; simulation report | Walkthrough view spec (FR-V12-D-023) | FR-V12-D-023 | Matched |
| D-F19-001 | REC-02 A110 scoped run timeline; current node; wait reason; reservations; retry and uncertain outcomes; unknown actual cost explicit; two runs isolated; unknown outcome not blindly retried | Partially covered | A110; aut_run current_node_key / wait_reason | Timeline fields added (FR-V12-D-018) | FR-V12-D-018; TC-V12-D-018 | Matched |
| D-F19-002 | Simulation requires selected offering / market / channel account in active company; store context and graph version on run; check configuration version before approval | Partially covered | aut_run pinned revision | BusinessContext snapshot + config_version check | FR-V12-D-018 | Matched |
| D-F19-003 | Atomic hierarchical reservations; consent; schedules; DAG execution; version checks; reconciliation; queue fairness; concurrency remain release gates | Partially covered | Part 3.4 WQG; AU-002 | Each gate mapped to an FR and test | FR-V12-D-019…022 | Matched |
| D-F19-004 | MT-28 concurrency and fair queues per tenant/company; stable config/effect IDs; no shared mutable context; MT-TC-MT-28 | Partially covered | Part 3.1 ≤ 20 runs per startup; IP-09 bulkheads | Fair scheduler (ADR-199) | FR-V12-D-019; TC-V12-D-019 | Matched |
| D-F19-005 | MT-30 company/offering/workflow budgets plus tenant aggregate cap; currency; period; timezone; atomic reservation; MT-TC-MT-30 | Partially covered | AU-002 tenant/startup/agent budgets | Budget hierarchy (RECOMMENDATION-830) | FR-V12-D-020; TC-V12-D-020 | Matched |
| D-F19-006 | Validate schema; authority; entitlement; connector; source rights; budget; dependency graph; effect class before scheduling | Partially covered | Part 3.4 WQG; PDP | Preflight order fixed (§11.4b.5) | FR-V12-D-007 | Matched |
| D-F19-007 | Dry run cannot reserve live money / dispatch / publish | Covered | Part 2.2 E-6 | Unchanged | — | Matched |
| D-F19-008 | Outbox creates one scoped run; durable steps checkpoint after committed artifact | Partially covered | ops_outbox; aut_step_run | Checkpoint contract | FR-V12-D-004 | Matched |
| D-F19-009 | Concurrency bounded per tenant/provider; revoked consent and emergency stop rechecked at effect | Covered | Part 2.2 E-3; E-7; IP-09 | Unchanged | — | Matched |
| D-F19-010 | Hold uncertain writes for reconciliation | Covered | Part 2.2 E-5 | Unchanged | — | Matched |
| D-F19-011 | Backpressure and retry with approved timeouts / rate limits / deadlines | Covered | Part 3.2 §3.2.7 | Unchanged | — | Matched |
| D-F19-012 | ST-03 workload bulkheads; noisy tenant cannot starve another; OPT-TC-ST-03 | Partially covered | IP-09 per-provider bulkheads | Per-tenant weighted fair share (ADR-199) | FR-V12-D-019; TC-V12-D-019 | Matched |
| D-F19-013 | FL-06 dependency-aware parallel DAG; join conditions; dependent waits; cancellation propagates | Not covered | Part 3.1 DAG interpreter (sequential) | Parallel read branches + join node | FR-V12-D-021; TC-V12-D-021 | Matched |
| D-F19-014 | RT-08 customer-controlled schedules: scoped pause; timezone cadence; preferences; consent gates stay | Partially covered | aut_trigger state paused | Tenant schedule controls (FR-V12-D-022) | FR-V12-D-022; TC-V12-D-022 | Matched |
| D-F19-015 | REQUESTED→VALIDATING→QUEUED→RUNNING→AWAITING_APPROVAL→EXECUTING_EFFECT→RECONCILING→COMPLETED; HELD / BLOCKED / FAILED_RETRYABLE / FAILED_TERMINAL / CANCELED | Partially covered | Part 2.3 §2.27.14; aut_run.state | V12 states canonical; old states mapped (DEC-561) | DEC-561; ADR-197 | Matched |
| D-F19-016 | Optimistic version on transition; unique effect ledger; terminal state immutable except authorized reconciliation adjustment | Partially covered | aut_step_run UQ-IDEM-11 | Transition guard + adjustment record | DEC-561; TC-V12-D-018 | Matched |
| D-F19-017 | Queue by tenant and provider concurrency | Partially covered | DEC-321 queues; IP-09 | Fair scheduler | FR-V12-D-019 | Matched |
| D-F19-018 | Bounded exponential backoff with jitter; dead-letter review | Covered | DEC-321; NFR-016 | Unchanged | — | Matched |
| D-F19-019 | Heartbeats and abandoned-job recovery | Partially covered | Part 3.4 lease fencing | Heartbeat + reaper (§11.4b.7) | FR-V12-D-004; TC-V12-D-004 | Matched |
| D-B09-001 | REC-05 (repeated from FSD ch12) | Partially covered | A113 | As D-F12-001 | FR-V12-D-013 | Matched |
| D-B09-002 | REC-08 (repeated from FSD ch12) | Not covered | None | As D-F12-002 | FR-V12-D-025 | Matched |
| D-B09-003 | MT-34 one definition per stable workflow/version; child step reuse via contracts; per-customer configuration only; MT-TC-MT-34 add 25 customer configurations with no cloning | Partially covered | BRL-AUT-03; A113 | Adopted (DEC-569) | FR-V12-D-013; TC-V12-D-013 | Matched |
| D-B09-004 | Per service table: workflow; business outcome; input → output; proposed KPI; risk (19 tables for SVC-21…39) | Not covered | None | Each row carried into §11.4c | DEC-560 | Matched |
| D-APB-001 | One JSON Schema 2020-12 document per workflow; \$id urn:sm:dto:<workflow>:v2; \$defs.input and \$defs.output | Not covered | None | Schema registry (DEC-565; ADR-198) | DEC-565; ADR-198 | Matched |
| D-APB-002 | Types reflect corrected DTO tables (D2); "all 156 pass meta-schema validation" | Not covered | None | CI gate re-validates every schema (TC-V12-D-002); 76/76 parsed here | TC-V12-D-002 | Matched |
| D-APB-003 | additionalProperties false; every input and output property required; one shared schema per service (4 workflows) | Not covered | None | v3 fix: per-workflow produced-output projection; non-produced outputs nullable (GAP-824) | DEC-565; GAP-824 | Matched |
| D-APB-004 | Configured enums as string maxLength 64 with values from a versioned registry | Not covered | None | Enum registry table (§11.4b.4) | DEC-565 | Matched |
| D-APB-005 | Arrays of string/object with maxItems 500 | Not covered | None | Typed item schemas in v3 (GAP-824) | DEC-565; GAP-824 | Matched |
| D-APB-006 | Free text minLength 1 maxLength 4000 | Not covered | None | Adopted; text treated as untrusted (AU-005) | DEC-565 | Matched |
| D-APB-007 | Refs uuid format; currency ^[A-Z]{3}\$; integers minimum 0 or 1; money as integer minor units | Not covered | ADR-030 decimal strings | Minor units at workflow DTO boundary only (RECOMMENDATION-829) | DEC-565; RECOMMENDATION-829 | Matched |
| D-CSV-001 | 50-field workflow specification; four named workflows per service; stable existing IDs and new WF04; approved service entitlement required per action | Partially covered | Part 9.4 | All 50 fields parsed (3800 cells for SVC-21…39) | DEC-560 | Matched |
| D-CSV-002 | Scoped service principal or authorized delegated user; deny privilege escalation; short-lived grants; no shared credentials | Covered | R19; R20; Part 7.2 tool registry | Unchanged | — | Matched |
| D-CSV-003 | Provider-neutral model adapter; rules-first; quality/cost gate; no vendor lock-in assumed | Covered | Part 3.1 §3.1.4.7 gateway; DEC-418 | Unchanged | — | Matched |
| D-CSV-004 | Proposed envelope event_id; tenant_id; startup_id; service_id; workflow_revision; input_ref; occurred_at; correlation_id | Partially covered | Part 3.2 §3.2.3.1 | Superseded by canonical event v2 (DEC-563) | DEC-563 | Matched |
| D-CSV-005 | Key = scoped event + workflow revision + action target; check duplicate effects / conflicts / active reply / suppression / reservation | Covered | UQ-IDEM-11/12; AU-030 | Unchanged | — | Matched |
| D-CSV-006 | Bounded retry; reconcile before retry; pause; route reviewer; log; emergency stop | Covered | Part 2.2 E-5; E-7 | Unchanged | — | Matched |
| D-CSV-007 | Source ID; owner; scope; observed_at; evidence hash/version; permitted use; freshness; hold stale/conflicting evidence | Covered | intel_evidence; AU-007 | Unchanged | — | Matched |
| D-CSV-008 | Pending actual provider / labour / retry costs; margin target TBD by owner | Partially covered | AU-049; RP-27 | Blueprint estimate added; margin owner = service owner (GAP-831) | GAP-831 | Matched |
| D-CSV-009 | Stable IDs; version and review material changes; immutable active-run snapshot; no silent downgrade; notify subscribers; map entitlements before migration | Partially covered | BRL-AUT-03 | Registry lifecycle (FR-V12-D-001) | FR-V12-D-001 | Matched |
| D-CSV-010 | Proposed; test Not run; live execution and pricing pending (all 76) | Partially covered | Part 9.4 release columns | Registry field implementation_status | FR-V12-D-001 | Matched |
| D-CSV-011 | 2.0-target for 15 workflows (SVC-21…25 WF01–03); 1.0-target for 61 | Not covered | None | Registry semantic version fields | FR-V12-D-001 | Matched |
| D-CSV-012 | AI-assisted / supervised; controlled autonomous only for preapproved eligible routine steps; simulation zero effects (2 wordings) | Partially covered | DEC-064 | Mapped (DEC-566) | DEC-566 | Matched |
| D-CSV-013 | 3 labels (internal analysis/draft; external communication; financial/commitment) — 13 conflict with FSD R-class | Partially covered | Part 7.2 §7.2.4 side-effect classes | Stricter R-class governs (DEC-570; GAP-821) | DEC-570; GAP-821 | Matched |
| D-CSV-014 | Text; structured records; audio/image/video where authorized; documents (4 combinations) | Partially covered | Part 7.3 text models | Modality bound per workflow; audio/video only where Founder approves (CONFLICT-815/819) | DEC-576 | Matched |

#### 11.4.3.2 Workflow aspects A01–A16 and every step (code before→after)

Legend: C Covered, P Partially covered, N Not covered, X Conflict → M Matched, F Pending Founder decision. A01 identity/outcome, A02 trigger, A03 result, A04 DTO, A05 authority, A06 engine/agent, A07 KPI, A08 UI/API/DB candidates, A09 API-V2/DB-V2 contract, A10 cost, A11 acceptance IDs, A12 source AT01, A13 channel, A14 UI input contract, A15 ch13 registry row, A16 workbook row. Full text of every cell: `final/coverage_v12/D_coverage.csv`.

| Workflow | A01 | A02 | A03 | A04 | A05 | A06 | A07 | A08 | A09 | A10 | A11 | A12 | A13 | A14 | A15 | A16 | Steps (STEP-nn code) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| SM-SVC-21-WF01 | P→M | P→M | P→M | N→M | X→F | P→M | N→M | C→M | N→M | P→M | N→M | N→M | P→M | P→M | N→M | P→M | 01 P→M 02 P→M 03 P→M |
| SM-SVC-21-WF02 | P→M | P→M | P→M | N→M | X→F | P→M | N→M | C→M | N→M | P→M | N→M | N→M | P→M | P→M | N→M | P→M | 01 P→M 02 P→M 03 P→M 04 P→M |
| SM-SVC-21-WF03 | P→M | P→M | P→M | N→M | P→M | P→M | N→M | C→M | N→M | P→M | N→M | N→M | P→M | P→M | N→M | P→M | 01 P→M 02 P→M 03 P→M |
| SM-SVC-21-WF04 | P→M | P→M | P→M | N→M | P→M | P→M | N→M | C→M | N→M | P→M | N→M | N→M | P→M | P→M | N→M | P→M | 01 P→M 02 P→M 03 P→M 04 P→M |
| SM-SVC-22-WF01 | P→M | P→M | P→M | N→M | P→M | P→M | N→M | C→M | N→M | P→M | N→M | N→M | P→M | P→M | N→M | P→M | 01 P→M 02 P→M 03 P→M |
| SM-SVC-22-WF02 | P→M | P→M | P→M | N→M | P→M | P→M | N→M | C→M | N→M | P→M | N→M | N→M | P→M | P→M | N→M | P→M | 01 P→M 02 P→M 03 P→M |
| SM-SVC-22-WF03 | P→M | P→M | P→M | N→M | P→M | P→M | N→M | C→M | N→M | P→M | N→M | N→M | P→M | P→M | N→M | P→M | 01 P→M 02 P→M 03 P→M 04 P→M |
| SM-SVC-22-WF04 | N→M | N→M | N→M | N→M | P→M | P→M | N→M | C→M | N→M | P→M | N→M | N→M | P→M | P→M | N→M | P→M | 01 N→M 02 N→M 03 N→M 04 N→M |
| SM-SVC-23-WF01 | P→M | P→M | P→M | N→M | P→M | P→M | N→M | C→M | N→M | P→M | N→M | N→M | P→M | P→M | N→M | P→M | 01 P→M 02 P→M 03 P→M 04 P→M |
| SM-SVC-23-WF02 | P→M | P→M | P→M | N→M | P→M | P→M | N→M | C→M | N→M | P→M | N→M | N→M | P→M | P→M | N→M | P→M | 01 P→M 02 P→M 03 P→M |
| SM-SVC-23-WF03 | P→M | P→M | P→M | N→M | P→M | P→M | N→M | C→M | N→M | P→M | N→M | N→M | P→M | P→M | N→M | P→M | 01 P→M 02 P→M 03 P→M |
| SM-SVC-23-WF04 | P→M | P→M | P→M | N→M | P→M | P→M | N→M | C→M | N→M | P→M | N→M | N→M | P→M | P→M | N→M | P→M | 01 P→M 02 P→M 03 P→M |
| SM-SVC-24-WF01 | P→M | P→M | P→M | N→M | P→M | P→M | N→M | C→M | N→M | P→M | N→M | N→M | P→M | P→M | N→M | P→M | 01 P→M 02 P→M 03 P→M |
| SM-SVC-24-WF02 | P→M | P→M | P→M | N→M | P→M | P→M | N→M | C→M | N→M | P→M | N→M | N→M | P→M | P→M | N→M | P→M | 01 P→M 02 P→M 03 P→M |
| SM-SVC-24-WF03 | P→M | P→M | P→M | N→M | P→M | P→M | N→M | C→M | N→M | P→M | N→M | N→M | P→M | P→M | N→M | P→M | 01 P→M 02 P→M 03 P→M 04 P→M |
| SM-SVC-24-WF04 | P→M | P→M | P→M | N→M | P→M | P→M | N→M | C→M | N→M | P→M | N→M | N→M | P→M | P→M | N→M | P→M | 01 P→M 02 P→M 03 P→M 04 P→M |
| SM-SVC-25-WF01 | P→M | P→M | P→M | N→M | P→M | P→M | N→M | C→M | N→M | P→M | N→M | N→M | P→M | P→M | N→M | P→M | 01 P→M 02 P→M 03 P→M 04 P→M |
| SM-SVC-25-WF02 | P→M | P→M | P→M | N→M | P→M | P→M | N→M | C→M | N→M | P→M | N→M | N→M | P→M | P→M | N→M | P→M | 01 P→M 02 P→M 03 P→M 04 P→M |
| SM-SVC-25-WF03 | P→M | P→M | P→M | N→M | P→M | P→M | N→M | C→M | N→M | P→M | N→M | N→M | P→M | P→M | N→M | P→M | 01 P→M 02 P→M 03 P→M 04 P→M |
| SM-SVC-25-WF04 | P→M | P→M | P→M | N→M | P→M | P→M | N→M | C→M | N→M | P→M | N→M | N→M | P→M | P→M | N→M | P→M | 01 P→M 02 P→M 03 P→M 04 P→M |
| SM-SVC-26-WF01 | X→F | X→F | X→F | N→M | X→F | X→F | N→M | P→M | N→M | P→M | N→M | N→M | X→F | P→M | N→M | P→M | 01 X→F 02 X→F 03 X→F |
| SM-SVC-26-WF02 | X→F | X→F | X→F | N→M | X→F | X→F | N→M | P→M | N→M | P→M | N→M | N→M | X→F | P→M | N→M | P→M | 01 X→F 02 X→F 03 X→F |
| SM-SVC-26-WF03 | X→F | X→F | X→F | N→M | X→F | X→F | N→M | P→M | N→M | P→M | N→M | N→M | X→F | P→M | N→M | P→M | 01 X→F 02 X→F 03 X→F |
| SM-SVC-26-WF04 | X→F | X→F | X→F | N→M | X→F | X→F | N→M | P→M | N→M | P→M | N→M | N→M | X→F | P→M | N→M | P→M | 01 X→F 02 X→F 03 X→F |
| SM-SVC-27-WF01 | X→F | X→F | X→F | N→M | X→F | X→F | N→M | P→M | N→M | P→M | N→M | N→M | P→M | P→M | N→M | P→M | 01 X→F 02 N→M 03 N→M |
| SM-SVC-27-WF02 | X→F | X→F | X→F | N→M | X→F | X→F | N→M | P→M | N→M | P→M | N→M | N→M | P→M | P→M | N→M | P→M | 01 X→F 02 N→M 03 N→M |
| SM-SVC-27-WF03 | X→F | X→F | X→F | N→M | X→F | X→F | N→M | P→M | N→M | P→M | N→M | N→M | P→M | P→M | N→M | P→M | 01 N→M 02 X→F 03 N→M |
| SM-SVC-27-WF04 | P→M | P→M | P→M | N→M | P→M | P→M | N→M | P→M | N→M | P→M | N→M | N→M | P→M | P→M | N→M | P→M | 01 P→M 02 P→M 03 P→M |
| SM-SVC-28-WF01 | N→M | N→M | N→M | N→M | P→M | P→M | N→M | P→M | N→M | P→M | N→M | N→M | P→M | P→M | N→M | P→M | 01 N→M 02 N→M 03 N→M |
| SM-SVC-28-WF02 | N→M | N→M | N→M | N→M | P→M | P→M | N→M | P→M | N→M | P→M | N→M | N→M | P→M | P→M | N→M | P→M | 01 N→M 02 N→M 03 N→M |
| SM-SVC-28-WF03 | X→F | X→F | X→F | N→M | X→F | X→F | N→M | P→M | N→M | P→M | N→M | N→M | P→M | P→M | N→M | P→M | 01 N→M 02 X→F 03 X→F |
| SM-SVC-28-WF04 | X→F | X→F | X→F | N→M | X→F | X→F | N→M | P→M | N→M | P→M | N→M | N→M | P→M | P→M | N→M | P→M | 01 N→M 02 X→F 03 X→F |
| SM-SVC-29-WF01 | P→M | P→M | P→M | N→M | P→M | P→M | N→M | P→M | N→M | P→M | N→M | N→M | P→M | P→M | N→M | P→M | 01 P→M 02 P→M 03 P→M |
| SM-SVC-29-WF02 | P→M | P→M | P→M | N→M | P→M | P→M | N→M | P→M | N→M | P→M | N→M | N→M | P→M | P→M | N→M | P→M | 01 P→M 02 P→M |
| SM-SVC-29-WF03 | P→M | P→M | P→M | N→M | P→M | P→M | N→M | P→M | N→M | P→M | N→M | N→M | P→M | P→M | N→M | P→M | 01 P→M 02 P→M |
| SM-SVC-29-WF04 | P→M | P→M | P→M | N→M | P→M | P→M | N→M | P→M | N→M | P→M | N→M | N→M | P→M | P→M | N→M | P→M | 01 P→M 02 P→M 03 P→M |
| SM-SVC-30-WF01 | P→M | P→M | P→M | N→M | P→M | P→M | N→M | P→M | N→M | P→M | N→M | N→M | P→M | P→M | N→M | P→M | 01 P→M 02 P→M 03 P→M |
| SM-SVC-30-WF02 | P→M | P→M | P→M | N→M | X→F | P→M | N→M | P→M | N→M | P→M | N→M | N→M | P→M | P→M | N→M | P→M | 01 P→M 02 P→M 03 P→M |
| SM-SVC-30-WF03 | P→M | P→M | P→M | N→M | P→M | P→M | N→M | P→M | N→M | P→M | N→M | N→M | P→M | P→M | N→M | P→M | 01 P→M 02 P→M 03 P→M |
| SM-SVC-30-WF04 | P→M | P→M | P→M | N→M | P→M | P→M | N→M | P→M | N→M | P→M | N→M | N→M | P→M | P→M | N→M | P→M | 01 P→M 02 P→M |
| SM-SVC-31-WF01 | N→M | N→M | N→M | N→M | P→M | P→M | N→M | P→M | N→M | P→M | N→M | N→M | P→M | P→M | N→M | P→M | 01 N→M 02 N→M 03 N→M |
| SM-SVC-31-WF02 | N→M | N→M | N→M | N→M | X→F | P→M | N→M | P→M | N→M | P→M | N→M | N→M | P→M | P→M | N→M | P→M | 01 N→M 02 N→M 03 N→M |
| SM-SVC-31-WF03 | P→M | P→M | P→M | N→M | X→F | P→M | N→M | P→M | N→M | P→M | N→M | N→M | P→M | P→M | N→M | P→M | 01 P→M 02 P→M 03 P→M |
| SM-SVC-31-WF04 | N→M | N→M | N→M | N→M | P→M | P→M | N→M | P→M | N→M | P→M | N→M | N→M | P→M | P→M | N→M | P→M | 01 N→M 02 N→M |
| SM-SVC-32-WF01 | P→M | P→M | P→M | N→M | P→M | P→M | N→M | P→M | N→M | P→M | N→M | N→M | P→M | P→M | N→M | P→M | 01 P→M 02 P→M 03 P→M |
| SM-SVC-32-WF02 | P→M | P→M | P→M | N→M | P→M | P→M | N→M | P→M | N→M | P→M | N→M | N→M | P→M | P→M | N→M | P→M | 01 P→M 02 P→M 03 P→M |
| SM-SVC-32-WF03 | P→M | P→M | P→M | N→M | P→M | P→M | N→M | P→M | N→M | P→M | N→M | N→M | P→M | P→M | N→M | P→M | 01 P→M 02 P→M 03 P→M |
| SM-SVC-32-WF04 | P→M | P→M | P→M | N→M | X→F | P→M | N→M | P→M | N→M | P→M | N→M | N→M | P→M | P→M | N→M | P→M | 01 P→M 02 P→M 03 P→M |
| SM-SVC-33-WF01 | P→M | P→M | P→M | N→M | P→M | P→M | N→M | P→M | N→M | P→M | N→M | N→M | P→M | P→M | N→M | P→M | 01 P→M 02 P→M 03 P→M |
| SM-SVC-33-WF02 | P→M | P→M | P→M | N→M | P→M | P→M | N→M | P→M | N→M | P→M | N→M | N→M | P→M | P→M | N→M | P→M | 01 P→M 02 P→M 03 P→M |
| SM-SVC-33-WF03 | P→M | P→M | P→M | N→M | P→M | P→M | N→M | P→M | N→M | P→M | N→M | N→M | P→M | P→M | N→M | P→M | 01 P→M 02 P→M 03 P→M |
| SM-SVC-33-WF04 | P→M | P→M | P→M | N→M | P→M | P→M | N→M | P→M | N→M | P→M | N→M | N→M | P→M | P→M | N→M | P→M | 01 P→M 02 P→M 03 P→M |
| SM-SVC-34-WF01 | P→M | P→M | P→M | N→M | P→M | P→M | N→M | P→M | N→M | P→M | N→M | N→M | P→M | P→M | N→M | P→M | 01 P→M 02 P→M 03 P→M |
| SM-SVC-34-WF02 | P→M | P→M | P→M | N→M | P→M | P→M | N→M | P→M | N→M | P→M | N→M | N→M | P→M | P→M | N→M | P→M | 01 P→M 02 P→M 03 P→M |
| SM-SVC-34-WF03 | P→M | P→M | P→M | N→M | P→M | P→M | N→M | P→M | N→M | P→M | N→M | N→M | P→M | P→M | N→M | P→M | 01 P→M |
| SM-SVC-34-WF04 | P→M | P→M | P→M | N→M | P→M | P→M | N→M | P→M | N→M | P→M | N→M | N→M | P→M | P→M | N→M | P→M | 01 P→M 02 P→M 03 P→M |
| SM-SVC-35-WF01 | N→M | N→M | N→M | N→M | P→M | P→M | N→M | P→M | N→M | P→M | N→M | N→M | P→M | P→M | N→M | P→M | 01 N→M 02 N→M 03 N→M |
| SM-SVC-35-WF02 | N→M | N→M | N→M | N→M | P→M | P→M | N→M | P→M | N→M | P→M | N→M | N→M | P→M | P→M | N→M | P→M | 01 N→M 02 N→M 03 N→M |
| SM-SVC-35-WF03 | N→M | N→M | N→M | N→M | P→M | P→M | N→M | P→M | N→M | P→M | N→M | N→M | P→M | P→M | N→M | P→M | 01 N→M 02 N→M 03 N→M |
| SM-SVC-35-WF04 | P→M | P→M | P→M | N→M | P→M | P→M | N→M | P→M | N→M | P→M | N→M | N→M | P→M | P→M | N→M | P→M | 01 P→M 02 P→M 03 P→M |
| SM-SVC-36-WF01 | P→M | P→M | P→M | N→M | P→M | P→M | N→M | P→M | N→M | P→M | N→M | N→M | P→M | P→M | N→M | P→M | 01 P→M 02 P→M 03 P→M |
| SM-SVC-36-WF02 | P→M | P→M | P→M | N→M | P→M | P→M | N→M | P→M | N→M | P→M | N→M | N→M | P→M | P→M | N→M | P→M | 01 P→M 02 P→M 03 P→M |
| SM-SVC-36-WF03 | X→F | X→F | X→F | N→M | X→F | X→F | N→M | P→M | N→M | P→M | N→M | N→M | P→M | P→M | N→M | P→M | 01 X→F 02 N→M 03 N→M |
| SM-SVC-36-WF04 | P→M | P→M | P→M | N→M | P→M | P→M | N→M | P→M | N→M | P→M | N→M | N→M | P→M | P→M | N→M | P→M | 01 P→M 02 P→M 03 P→M |
| SM-SVC-37-WF01 | P→M | P→M | P→M | N→M | P→M | P→M | N→M | P→M | N→M | P→M | N→M | N→M | P→M | P→M | N→M | P→M | 01 P→M 02 P→M 03 P→M |
| SM-SVC-37-WF02 | X→F | X→F | X→F | N→M | X→F | X→F | N→M | P→M | N→M | P→M | N→M | N→M | P→M | P→M | N→M | P→M | 01 X→F 02 X→F |
| SM-SVC-37-WF03 | X→F | X→F | X→F | N→M | X→F | X→F | N→M | P→M | N→M | P→M | N→M | N→M | P→M | P→M | N→M | P→M | 01 X→F 02 X→F 03 X→F |
| SM-SVC-37-WF04 | P→M | P→M | P→M | N→M | P→M | P→M | N→M | P→M | N→M | P→M | N→M | N→M | P→M | P→M | N→M | P→M | 01 P→M 02 P→M |
| SM-SVC-38-WF01 | N→M | N→M | N→M | N→M | P→M | P→M | N→M | P→M | N→M | P→M | N→M | N→M | P→M | P→M | N→M | P→M | 01 N→M 02 N→M |
| SM-SVC-38-WF02 | N→M | N→M | N→M | N→M | P→M | P→M | N→M | P→M | N→M | P→M | N→M | N→M | P→M | P→M | N→M | P→M | 01 N→M 02 N→M 03 N→M |
| SM-SVC-38-WF03 | N→M | N→M | N→M | N→M | P→M | P→M | N→M | P→M | N→M | P→M | N→M | N→M | P→M | P→M | N→M | P→M | 01 N→M 02 N→M 03 N→M |
| SM-SVC-38-WF04 | N→M | N→M | N→M | N→M | P→M | P→M | N→M | P→M | N→M | P→M | N→M | N→M | P→M | P→M | N→M | P→M | 01 N→M 02 N→M 03 N→M |
| SM-SVC-39-WF01 | N→M | N→M | N→M | N→M | P→M | P→M | N→M | P→M | N→M | P→M | N→M | N→M | P→M | P→M | N→M | P→M | 01 N→M 02 N→M 03 N→M 04 N→M |
| SM-SVC-39-WF02 | P→M | P→M | P→M | N→M | P→M | P→M | N→M | P→M | N→M | P→M | N→M | N→M | P→M | P→M | N→M | P→M | 01 P→M 02 P→M 03 P→M |
| SM-SVC-39-WF03 | N→M | N→M | N→M | N→M | X→F | P→M | N→M | P→M | N→M | P→M | N→M | N→M | P→M | P→M | N→M | P→M | 01 N→M 02 N→M 03 N→M |
| SM-SVC-39-WF04 | P→M | P→M | P→M | N→M | P→M | P→M | N→M | P→M | N→M | P→M | N→M | N→M | P→M | P→M | N→M | P→M | 01 P→M 02 P→M 03 P→M |

#### 11.4.3.3 Service-level workbook fields (code before→after)

| Service | objective | channels | prereq | agents | mode | provider | limits | kpi | availability | security | engine | complementary | interop | readiness | pricing | oss | industries | entitlements |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| SM-SVC-21 | P→M | P→M | P→M | P→M | P→M | P→M | P→M | P→M | P→M | P→M | P→M | P→M | P→M | P→M | P→M | P→M | P→M | P→M |
| SM-SVC-22 | P→M | P→M | P→M | P→M | P→M | P→M | P→M | P→M | P→M | P→M | P→M | P→M | P→M | P→M | P→M | P→M | P→M | P→M |
| SM-SVC-23 | P→M | P→M | P→M | P→M | P→M | P→M | P→M | P→M | P→M | P→M | P→M | P→M | P→M | P→M | P→M | P→M | P→M | P→M |
| SM-SVC-24 | P→M | P→M | P→M | P→M | P→M | P→M | P→M | P→M | P→M | P→M | P→M | P→M | P→M | P→M | P→M | P→M | P→M | P→M |
| SM-SVC-25 | P→M | P→M | P→M | P→M | P→M | P→M | P→M | P→M | P→M | P→M | P→M | P→M | P→M | P→M | P→M | P→M | P→M | P→M |
| SM-SVC-26 | P→M | X→F | P→M | P→M | P→M | X→F | P→M | P→M | P→M | P→M | P→M | P→M | P→M | P→M | P→M | P→M | P→M | P→M |
| SM-SVC-27 | P→M | P→M | P→M | P→M | P→M | X→F | P→M | P→M | P→M | P→M | P→M | P→M | P→M | P→M | P→M | P→M | P→M | P→M |
| SM-SVC-28 | P→M | P→M | P→M | P→M | P→M | N→M | P→M | P→M | P→M | P→M | P→M | P→M | P→M | P→M | P→M | P→M | P→M | P→M |
| SM-SVC-29 | P→M | P→M | P→M | P→M | P→M | P→M | P→M | P→M | P→M | P→M | P→M | P→M | P→M | P→M | P→M | P→M | P→M | P→M |
| SM-SVC-30 | P→M | P→M | P→M | P→M | P→M | P→M | P→M | P→M | P→M | P→M | P→M | P→M | P→M | P→M | P→M | P→M | P→M | P→M |
| SM-SVC-31 | P→M | P→M | P→M | P→M | P→M | N→M | P→M | P→M | P→M | P→M | P→M | P→M | P→M | P→M | P→M | P→M | P→M | P→M |
| SM-SVC-32 | P→M | P→M | P→M | P→M | P→M | P→M | P→M | P→M | P→M | P→M | P→M | P→M | P→M | P→M | P→M | P→M | P→M | P→M |
| SM-SVC-33 | P→M | P→M | P→M | P→M | P→M | P→M | P→M | P→M | P→M | P→M | P→M | P→M | P→M | P→M | P→M | P→M | P→M | P→M |
| SM-SVC-34 | P→M | P→M | P→M | P→M | P→M | P→M | P→M | P→M | P→M | P→M | P→M | P→M | P→M | P→M | P→M | P→M | P→M | P→M |
| SM-SVC-35 | P→M | P→M | P→M | P→M | P→M | P→M | P→M | P→M | P→M | P→M | P→M | P→M | P→M | P→M | P→M | P→M | P→M | P→M |
| SM-SVC-36 | P→M | P→M | P→M | P→M | P→M | P→M | P→M | P→M | P→M | P→M | P→M | P→M | P→M | P→M | P→M | P→M | P→M | P→M |
| SM-SVC-37 | P→M | P→M | P→M | P→M | P→M | P→M | P→M | P→M | P→M | P→M | P→M | P→M | P→M | P→M | P→M | P→M | P→M | P→M |
| SM-SVC-38 | P→M | P→M | P→M | P→M | P→M | N→M | P→M | P→M | P→M | P→M | P→M | P→M | P→M | P→M | P→M | P→M | P→M | P→M |
| SM-SVC-39 | P→M | P→M | P→M | P→M | P→M | N→M | P→M | P→M | P→M | P→M | P→M | P→M | P→M | P→M | P→M | P→M | P→M | P→M |

#### 11.4.3.4 DTO fields (Appendix B), all N→M

| Service | Input fields | Output fields |
|---|---|---|
| SM-SVC-21 | `invoice_ref`, `payment_ref`, `amount_minor`, `currency` | `allocation_ref`, `balance_minor`, `discrepancy_refs`, `reconciliation_state` |
| SM-SVC-22 | `customer_ref`, `agreement_ref`, `template_ref`, `milestone_refs` | `plan_ref`, `readiness_state`, `task_refs`, `handover_ref` |
| SM-SVC-23 | `customer_ref`, `renewal_ref`, `feedback_refs`, `consent_ref` | `renewal_task_ref`, `risk_score`, `reason_codes`, `recommendation_ref` |
| SM-SVC-24 | `outcome_refs`, `attribution_model_ref`, `period`, `assumption_refs` | `report_ref`, `attributed_minor`, `forecast_minor`, `error_metric`, `confidence` |
| SM-SVC-25 | `document_ref`, `taxonomy_ref`, `claim_refs`, `revision` | `document_version`, `claim_version_refs`, `review_state`, `correction_refs` |
| SM-SVC-26 | `call_ref`, `contact_ref`, `script_ref`, `recording_permission_ref` | `disposition`, `transcript_ref`, `booking_ref`, `call_event_ref` |
| SM-SVC-27 | `brief_ref`, `brand_ref`, `asset_rights_refs`, `target_language` | `asset_ref`, `revision`, `rights_state`, `qa_state` |
| SM-SVC-28 | `agent_ref`, `mandate_ref`, `offering_ref`, `order_ref` | `quote_ref`, `mandate_state`, `transaction_ref`, `reconciliation_state` |
| SM-SVC-29 | `account_ref`, `icp_ref`, `role_evidence_refs`, `engagement_refs` | `plan_ref`, `buying_group_ref`, `journey_ref`, `progress_report_ref` |
| SM-SVC-30 | `hypothesis_ref`, `variant_refs`, `allocation_policy_ref`, `event_refs` | `experiment_ref`, `allocation_ref`, `lift`, `interval`, `decision_state` |
| SM-SVC-31 | `marketplace_ref`, `sku_ref`, `inventory_ref`, `event_refs` | `listing_ref`, `inventory_version`, `order_event_ref`, `net_minor` |
| SM-SVC-32 | `partner_ref`, `territory_ref`, `material_refs`, `deal_ref` | `shortlist_ref`, `access_grant_ref`, `registration_ref`, `performance_ref` |
| SM-SVC-33 | `customer_ref`, `enquiry_ref`, `sla_policy_ref`, `knowledge_refs` | `case_ref`, `severity`, `queue_ref`, `resolution_ref`, `sla_state` |
| SM-SVC-34 | `account_ref`, `event_refs`, `feature_refs`, `plan_ref` | `activation_state`, `usage_report_ref`, `expansion_ref`, `recommendation_ref` |
| SM-SVC-35 | `brand_ref`, `review_refs`, `source_ids`, `threshold_ref` | `review_queue_ref`, `response_ref`, `incident_ref`, `improvement_ref` |
| SM-SVC-36 | `learner_ref`, `playbook_ref`, `scenario_ref`, `authorized_session_ref` | `playbook_revision`, `practice_report_ref`, `feedback_ref`, `training_plan_ref` |
| SM-SVC-37 | `offer_ref`, `cost_revision_ref`, `price_bounds_ref`, `history_refs` | `margin_minor`, `scenario_ref`, `experiment_ref`, `exception_ref` |
| SM-SVC-38 | `sender_ref`, `template_ref`, `recipient_refs`, `consent_refs` | `eligibility_state`, `dispatch_ref`, `delivery_state`, `suppression_state` |
| SM-SVC-39 | `requirement_ref`, `supplier_refs`, `quote_refs`, `budget_ref` | `shortlist_ref`, `comparison_ref`, `purchase_order_ref`, `exception_refs` |

#### 11.4.3.5 Every Conflict aspect individually (all ended Pending Founder decision; adopted by DEC-779…791 in Part 11.14)

| Aspect ID | Summary | Conflict | Proposed resolution |
|---|---|---|---|
| D-S26-channels | SM-SVC-26 Supported channels: Private Admin; approved client data and connectors; voice/telephony | CONFLICT-815 | Specify fully, ship disabled; inbound AI voice only after A3 PG gate and legal review; outbound stays human-dialled; no transcripts (DEC-572) |
| D-S26-provider | SM-SVC-26 External provider requirements: Authorized telephony, speech recognition and synthesis; calling/recording permission | CONFLICT-815 | Specify fully, ship disabled; inbound AI voice only after A3 PG gate and legal review; outbound stays human-dialled; no transcripts (DEC-572) |
| D-S27-provider | SM-SVC-27 External provider requirements: Authorized image/video/audio generation and asset rights | CONFLICT-819 | Brand-asset composition first; generative media behind a new provider, budget and likeness policy (DEC-576) |
| SM-SVC-21-WF01-A05 | Authority R3 financial/legal/commitment; L2 mandatory approved effect; L3 only with separately approved bounded mandate where lawful; Finance approves | CONFLICT-814 | Cap R3 at V12 L2 = blueprint L1 with exact-hash approval; disable "L3 bounded mandate" (DEC-577) |
| SM-SVC-21-WF02-A05 | Authority R3 financial/legal/commitment; L2 mandatory approved effect; L3 only with separately approved bounded mandate where lawful; Finance approves | CONFLICT-814 | Cap R3 at V12 L2 = blueprint L1 with exact-hash approval; disable "L3 bounded mandate" (DEC-577) |
| SM-SVC-26-WF01-A01 | Identity and business outcome: Inbound AI voice enquiry and call routing; Inbound call, approved knowledge, routing rules → Call disposition | CONFLICT-815 | Specify fully, ship disabled; inbound AI voice only after A3 PG gate and legal review; outbound stays human-dialled; no transcripts (DEC-572) |
| SM-SVC-26-WF01-A02 | Trigger / supplied input: Manual; scheduled monitoring; validated business event; authorized provider webhook when available; Inbound call, approved k | CONFLICT-815 | Specify fully, ship disabled; inbound AI voice only after A3 PG gate and legal review; outbound stays human-dialled; no transcripts (DEC-572) |
| SM-SVC-26-WF01-A03 | Result / acceptance artifact: Call disposition; Call disposition; no unapproved external side effects | CONFLICT-815 | Specify fully, ship disabled; inbound AI voice only after A3 PG gate and legal review; outbound stays human-dialled; no transcripts (DEC-572) |
| SM-SVC-26-WF01-A05 | Authority R2 external communication/provider/access write; L2 mandatory approved effect; L3 only with separately approved bounded mandate where lawful | CONFLICT-815 | Specify fully, ship disabled; inbound AI voice only after A3 PG gate and legal review; outbound stays human-dialled; no transcripts (DEC-572) |
| SM-SVC-26-WF01-A06 | Engine / agent: Multimodal AI; Workflow orchestration; Governance; Domain evidence review; Multimodal AI; policy review; orchestration; human speciali | CONFLICT-815 | Specify fully, ship disabled; inbound AI voice only after A3 PG gate and legal review; outbound stays human-dialled; no transcripts (DEC-572) |
| SM-SVC-26-WF01-A13 | Channel candidates: Voice; 3 steps; FSD chapter 12; simulation only | CONFLICT-815 | Specify fully, ship disabled; inbound AI voice only after A3 PG gate and legal review; outbound stays human-dialled; no transcripts (DEC-572) |
| SM-SVC-26-WF01-STEP-01 | Disclose AI as required [Domain service; INVALID_STATE → HELD] | CONFLICT-815 | Specify fully, ship disabled; inbound AI voice only after A3 PG gate and legal review; outbound stays human-dialled; no transcripts (DEC-572) |
| SM-SVC-26-WF01-STEP-02 | classify intent [Domain agent / task router; REVIEW_REQUIRED → AWAITING_APPROVAL] | CONFLICT-815 | Specify fully, ship disabled; inbound AI voice only after A3 PG gate and legal review; outbound stays human-dialled; no transcripts (DEC-572) |
| SM-SVC-26-WF01-STEP-03 | route or answer with evidence [Domain agent / task router; REVIEW_REQUIRED → AWAITING_APPROVAL] | CONFLICT-815 | Specify fully, ship disabled; inbound AI voice only after A3 PG gate and legal review; outbound stays human-dialled; no transcripts (DEC-572) |
| SM-SVC-26-WF02-A01 | Identity and business outcome: Authorized outbound voice engagement; Eligible contacts, call permission, approved script → Call event or hold | CONFLICT-815 | Specify fully, ship disabled; inbound AI voice only after A3 PG gate and legal review; outbound stays human-dialled; no transcripts (DEC-572) |
| SM-SVC-26-WF02-A02 | Trigger / supplied input: Manual; scheduled monitoring; validated business event; authorized provider webhook when available; Eligible contacts, call  | CONFLICT-815 | Specify fully, ship disabled; inbound AI voice only after A3 PG gate and legal review; outbound stays human-dialled; no transcripts (DEC-572) |
| SM-SVC-26-WF02-A03 | Result / acceptance artifact: Call event or hold; Call event or hold; no unapproved external side effects | CONFLICT-815 | Specify fully, ship disabled; inbound AI voice only after A3 PG gate and legal review; outbound stays human-dialled; no transcripts (DEC-572) |
| SM-SVC-26-WF02-A05 | Authority R2 external communication/provider/access write; L2 mandatory approved effect; L3 only with separately approved bounded mandate where lawful | CONFLICT-815 | Specify fully, ship disabled; inbound AI voice only after A3 PG gate and legal review; outbound stays human-dialled; no transcripts (DEC-572) |
| SM-SVC-26-WF02-A06 | Engine / agent: Multimodal AI; Workflow orchestration; Governance; Domain evidence review; Multimodal AI; policy review; orchestration; human speciali | CONFLICT-815 | Specify fully, ship disabled; inbound AI voice only after A3 PG gate and legal review; outbound stays human-dialled; no transcripts (DEC-572) |
| SM-SVC-26-WF02-A13 | Channel candidates: Voice; 3 steps; FSD chapter 12; simulation only | CONFLICT-815 | Specify fully, ship disabled; inbound AI voice only after A3 PG gate and legal review; outbound stays human-dialled; no transcripts (DEC-572) |
| SM-SVC-26-WF02-STEP-01 | Check consent, quiet hours and caps [Policy/validation engine; POLICY_DENIED → BLOCKED] | CONFLICT-815 | Specify fully, ship disabled; inbound AI voice only after A3 PG gate and legal review; outbound stays human-dialled; no transcripts (DEC-572) |
| SM-SVC-26-WF02-STEP-02 | initiate authorized call [Effect adapter; EFFECT_UNKNOWN → RECONCILING] | CONFLICT-815 | Specify fully, ship disabled; inbound AI voice only after A3 PG gate and legal review; outbound stays human-dialled; no transcripts (DEC-572) |
| SM-SVC-26-WF02-STEP-03 | record outcome [Domain service; INVALID_STATE → HELD] | CONFLICT-815 | Specify fully, ship disabled; inbound AI voice only after A3 PG gate and legal review; outbound stays human-dialled; no transcripts (DEC-572) |
| SM-SVC-26-WF03-A01 | Identity and business outcome: Multilingual voice conversation and appointment coordination; Call session, language, calendar availability → Booking o | CONFLICT-815 | Specify fully, ship disabled; inbound AI voice only after A3 PG gate and legal review; outbound stays human-dialled; no transcripts (DEC-572) |
| SM-SVC-26-WF03-A02 | Trigger / supplied input: Manual; scheduled monitoring; validated business event; authorized provider webhook when available; Call session, language,  | CONFLICT-815 | Specify fully, ship disabled; inbound AI voice only after A3 PG gate and legal review; outbound stays human-dialled; no transcripts (DEC-572) |
| SM-SVC-26-WF03-A03 | Result / acceptance artifact: Booking or handoff; Booking or handoff; no unapproved external side effects | CONFLICT-815 | Specify fully, ship disabled; inbound AI voice only after A3 PG gate and legal review; outbound stays human-dialled; no transcripts (DEC-572) |
| SM-SVC-26-WF03-A05 | Authority R2 external communication/provider/access write; L2 mandatory approved effect; L3 only with separately approved bounded mandate where lawful | CONFLICT-815 | Specify fully, ship disabled; inbound AI voice only after A3 PG gate and legal review; outbound stays human-dialled; no transcripts (DEC-572) |
| SM-SVC-26-WF03-A06 | Engine / agent: Multimodal AI; Workflow orchestration; Governance; Domain evidence review; Multimodal AI; policy review; orchestration; human speciali | CONFLICT-815 | Specify fully, ship disabled; inbound AI voice only after A3 PG gate and legal review; outbound stays human-dialled; no transcripts (DEC-572) |
| SM-SVC-26-WF03-A13 | Channel candidates: Voice; 3 steps; FSD chapter 12; simulation only | CONFLICT-815 | Specify fully, ship disabled; inbound AI voice only after A3 PG gate and legal review; outbound stays human-dialled; no transcripts (DEC-572) |
| SM-SVC-26-WF03-STEP-01 | Recognize language [Evidence/ingestion engine; SOURCE_DENIED → HELD] | CONFLICT-815 | Specify fully, ship disabled; inbound AI voice only after A3 PG gate and legal review; outbound stays human-dialled; no transcripts (DEC-572) |
| SM-SVC-26-WF03-STEP-02 | ground answers [Domain service; INVALID_STATE → HELD] | CONFLICT-815 | Specify fully, ship disabled; inbound AI voice only after A3 PG gate and legal review; outbound stays human-dialled; no transcripts (DEC-572) |
| SM-SVC-26-WF03-STEP-03 | confirm time with caller [Domain service; INVALID_STATE → HELD] | CONFLICT-815 | Specify fully, ship disabled; inbound AI voice only after A3 PG gate and legal review; outbound stays human-dialled; no transcripts (DEC-572) |
| SM-SVC-26-WF04-A01 | Identity and business outcome: Call intelligence, permitted transcription and CRM synchronization; Authorized recording or transcript, relationship ID | CONFLICT-815 | Specify fully, ship disabled; inbound AI voice only after A3 PG gate and legal review; outbound stays human-dialled; no transcripts (DEC-572) |
| SM-SVC-26-WF04-A02 | Trigger / supplied input: Manual; scheduled monitoring; validated business event; authorized provider webhook when available; Authorized recording or  | CONFLICT-815 | Specify fully, ship disabled; inbound AI voice only after A3 PG gate and legal review; outbound stays human-dialled; no transcripts (DEC-572) |
| SM-SVC-26-WF04-A03 | Result / acceptance artifact: Call summary and CRM event; Call summary and CRM event; no unapproved external side effects | CONFLICT-815 | Specify fully, ship disabled; inbound AI voice only after A3 PG gate and legal review; outbound stays human-dialled; no transcripts (DEC-572) |
| SM-SVC-26-WF04-A05 | Authority R1 scoped state write or safety control; L1/L2 review; L3 only for approved deterministic internal actions; Approve source/data rights and a | CONFLICT-815 | Specify fully, ship disabled; inbound AI voice only after A3 PG gate and legal review; outbound stays human-dialled; no transcripts (DEC-572) |
| SM-SVC-26-WF04-A06 | Engine / agent: Multimodal AI; Workflow orchestration; Governance; Domain evidence review; Multimodal AI; policy review; orchestration; human speciali | CONFLICT-815 | Specify fully, ship disabled; inbound AI voice only after A3 PG gate and legal review; outbound stays human-dialled; no transcripts (DEC-572) |
| SM-SVC-26-WF04-A13 | Channel candidates: Voice; 3 steps; FSD chapter 12; simulation only | CONFLICT-815 | Specify fully, ship disabled; inbound AI voice only after A3 PG gate and legal review; outbound stays human-dialled; no transcripts (DEC-572) |
| SM-SVC-26-WF04-STEP-01 | Extract actions [Evidence/ingestion engine; SOURCE_DENIED → HELD] | CONFLICT-815 | Specify fully, ship disabled; inbound AI voice only after A3 PG gate and legal review; outbound stays human-dialled; no transcripts (DEC-572) |
| SM-SVC-26-WF04-STEP-02 | redact restricted data [Domain service; INVALID_STATE → HELD] | CONFLICT-815 | Specify fully, ship disabled; inbound AI voice only after A3 PG gate and legal review; outbound stays human-dialled; no transcripts (DEC-572) |
| SM-SVC-26-WF04-STEP-03 | synchronize approved notes [Identity/reconciliation engine; CONFLICT → HELD] | CONFLICT-815 | Specify fully, ship disabled; inbound AI voice only after A3 PG gate and legal review; outbound stays human-dialled; no transcripts (DEC-572) |
| SM-SVC-27-WF01-A01 | Identity and business outcome: Marketing image and advertising creative generation; Brand brief, asset rights, approved claims → Image drafts | CONFLICT-819 | Brand-asset composition first; generative media behind a new provider, budget and likeness policy (DEC-576) |
| SM-SVC-27-WF01-A02 | Trigger / supplied input: Manual; scheduled monitoring; validated business event; authorized provider webhook when available; Brand brief, asset right | CONFLICT-819 | Brand-asset composition first; generative media behind a new provider, budget and likeness policy (DEC-576) |
| SM-SVC-27-WF01-A03 | Result / acceptance artifact: Image drafts; Image drafts; no unapproved external side effects | CONFLICT-819 | Brand-asset composition first; generative media behind a new provider, budget and likeness policy (DEC-576) |
| SM-SVC-27-WF01-A05 | Authority R0 internal analysis/draft; L1 assisted; L3 approved read/draft; Approve source/data rights and applicable external actions; review rights,  | CONFLICT-819 | Brand-asset composition first; generative media behind a new provider, budget and likeness policy (DEC-576) |
| SM-SVC-27-WF01-A06 | Engine / agent: Multimodal AI; Workflow orchestration; Governance; Domain evidence review; Multimodal AI; policy review; orchestration; human speciali | CONFLICT-819 | Brand-asset composition first; generative media behind a new provider, budget and likeness policy (DEC-576) |
| SM-SVC-27-WF01-STEP-01 | Generate variants [Domain agent / task router; REVIEW_REQUIRED → AWAITING_APPROVAL] | CONFLICT-819 | Brand-asset composition first; generative media behind a new provider, budget and likeness policy (DEC-576) |
| SM-SVC-27-WF02-A01 | Identity and business outcome: Product demonstration and promotional video generation; Product facts, approved storyboard, rights → Video draft | CONFLICT-819 | Brand-asset composition first; generative media behind a new provider, budget and likeness policy (DEC-576) |
| SM-SVC-27-WF02-A02 | Trigger / supplied input: Manual; scheduled monitoring; validated business event; authorized provider webhook when available; Product facts, approved  | CONFLICT-819 | Brand-asset composition first; generative media behind a new provider, budget and likeness policy (DEC-576) |
| SM-SVC-27-WF02-A03 | Result / acceptance artifact: Video draft; Video draft; no unapproved external side effects | CONFLICT-819 | Brand-asset composition first; generative media behind a new provider, budget and likeness policy (DEC-576) |
| SM-SVC-27-WF02-A05 | Authority R0 internal analysis/draft; L1 assisted; L3 approved read/draft; Approve source/data rights and applicable external actions; review rights,  | CONFLICT-819 | Brand-asset composition first; generative media behind a new provider, budget and likeness policy (DEC-576) |
| SM-SVC-27-WF02-A06 | Engine / agent: Multimodal AI; Workflow orchestration; Governance; Domain evidence review; Multimodal AI; policy review; orchestration; human speciali | CONFLICT-819 | Brand-asset composition first; generative media behind a new provider, budget and likeness policy (DEC-576) |
| SM-SVC-27-WF02-STEP-01 | Create storyboard and clips [Domain service; INVALID_STATE → HELD] | CONFLICT-819 | Brand-asset composition first; generative media behind a new provider, budget and likeness policy (DEC-576) |
| SM-SVC-27-WF03-A01 | Identity and business outcome: Multilingual audio, subtitle and creative localization; Approved asset, target language, voice rights → Localized asset | CONFLICT-819 | Brand-asset composition first; generative media behind a new provider, budget and likeness policy (DEC-576) |
| SM-SVC-27-WF03-A02 | Trigger / supplied input: Manual; scheduled monitoring; validated business event; authorized provider webhook when available; Approved asset, target l | CONFLICT-819 | Brand-asset composition first; generative media behind a new provider, budget and likeness policy (DEC-576) |
| SM-SVC-27-WF03-A03 | Result / acceptance artifact: Localized asset; Localized asset; no unapproved external side effects | CONFLICT-819 | Brand-asset composition first; generative media behind a new provider, budget and likeness policy (DEC-576) |
| SM-SVC-27-WF03-A05 | Authority R0 internal analysis/draft; L1 assisted; L3 approved read/draft; Approve source/data rights and applicable external actions; review rights,  | CONFLICT-819 | Brand-asset composition first; generative media behind a new provider, budget and likeness policy (DEC-576) |
| SM-SVC-27-WF03-A06 | Engine / agent: Multimodal AI; Workflow orchestration; Governance; Domain evidence review; Multimodal AI; policy review; orchestration; human speciali | CONFLICT-819 | Brand-asset composition first; generative media behind a new provider, budget and likeness policy (DEC-576) |
| SM-SVC-27-WF03-STEP-02 | generate captions/audio [Domain agent / task router; REVIEW_REQUIRED → AWAITING_APPROVAL] | CONFLICT-819 | Brand-asset composition first; generative media behind a new provider, budget and likeness policy (DEC-576) |
| SM-SVC-28-WF03-A01 | Identity and business outcome: Agent-assisted purchasing and negotiation mandate coordination; Mandate, price limits, negotiation policy → Mandate-lin | CONFLICT-816 | Catalogue and quote drafts allowed; negotiation and payment mandates stay human; record-only reconciliation (DEC-573) |
| SM-SVC-28-WF03-A02 | Trigger / supplied input: Manual; scheduled monitoring; validated business event; authorized provider webhook when available; Mandate, price limits, n | CONFLICT-816 | Catalogue and quote drafts allowed; negotiation and payment mandates stay human; record-only reconciliation (DEC-573) |
| SM-SVC-28-WF03-A03 | Result / acceptance artifact: Mandate-linked decision; Mandate-linked decision; no unapproved external side effects | CONFLICT-816 | Catalogue and quote drafts allowed; negotiation and payment mandates stay human; record-only reconciliation (DEC-573) |
| SM-SVC-28-WF03-A05 | Authority R3 financial/legal/commitment; L2 mandatory approved effect; L3 only with separately approved bounded mandate where lawful; Approve source/d | CONFLICT-814 | Cap R3 at V12 L2 = blueprint L1 with exact-hash approval; disable "L3 bounded mandate" (DEC-577) |
| SM-SVC-28-WF03-A06 | Engine / agent: Identity and permission; Workflow orchestration; Governance; Domain evidence review; Identity and permission; policy review; orchestra | CONFLICT-816 | Catalogue and quote drafts allowed; negotiation and payment mandates stay human; record-only reconciliation (DEC-573) |
| SM-SVC-28-WF03-STEP-02 | compare offers [Rules/analytics engine; INVALID_METRIC → HELD] | CONFLICT-816 | Catalogue and quote drafts allowed; negotiation and payment mandates stay human; record-only reconciliation (DEC-573) |
| SM-SVC-28-WF03-STEP-03 | route consequential decisions [Domain agent / task router; REVIEW_REQUIRED → AWAITING_APPROVAL] | CONFLICT-816 | Catalogue and quote drafts allowed; negotiation and payment mandates stay human; record-only reconciliation (DEC-573) |
| SM-SVC-28-WF04-A01 | Identity and business outcome: Authorized transaction, payment mandate and outcome reconciliation; Approved order, verified payment mandate, provider  | CONFLICT-816 | Catalogue and quote drafts allowed; negotiation and payment mandates stay human; record-only reconciliation (DEC-573) |
| SM-SVC-28-WF04-A02 | Trigger / supplied input: Manual; scheduled monitoring; validated business event; authorized provider webhook when available; Approved order, verified | CONFLICT-816 | Catalogue and quote drafts allowed; negotiation and payment mandates stay human; record-only reconciliation (DEC-573) |
| SM-SVC-28-WF04-A03 | Result / acceptance artifact: Auditable transaction record; Auditable transaction record; no unapproved external side effects | CONFLICT-816 | Catalogue and quote drafts allowed; negotiation and payment mandates stay human; record-only reconciliation (DEC-573) |
| SM-SVC-28-WF04-A05 | Authority R3 financial/legal/commitment; L2 mandatory approved effect; L3 only with separately approved bounded mandate where lawful; Approve source/d | CONFLICT-814 | Cap R3 at V12 L2 = blueprint L1 with exact-hash approval; disable "L3 bounded mandate" (DEC-577) |
| SM-SVC-28-WF04-A06 | Engine / agent: Identity and permission; Workflow orchestration; Governance; Domain evidence review; Identity and permission; policy review; orchestra | CONFLICT-816 | Catalogue and quote drafts allowed; negotiation and payment mandates stay human; record-only reconciliation (DEC-573) |
| SM-SVC-28-WF04-STEP-02 | execute only via approved provider [Effect adapter; EFFECT_UNKNOWN → RECONCILING] | CONFLICT-816 | Catalogue and quote drafts allowed; negotiation and payment mandates stay human; record-only reconciliation (DEC-573) |
| SM-SVC-28-WF04-STEP-03 | reconcile uncertain outcome [Identity/reconciliation engine; CONFLICT → HELD] | CONFLICT-816 | Catalogue and quote drafts allowed; negotiation and payment mandates stay human; record-only reconciliation (DEC-573) |
| SM-SVC-30-WF02-A05 | Authority R3 financial/legal/commitment; L2 mandatory approved effect; L3 only with separately approved bounded mandate where lawful; Approve source/d | CONFLICT-814 | Cap R3 at V12 L2 = blueprint L1 with exact-hash approval; disable "L3 bounded mandate" (DEC-577) |
| SM-SVC-31-WF02-A05 | Authority R3 financial/legal/commitment; L2 mandatory approved effect; L3 only with separately approved bounded mandate where lawful; Approve source/d | CONFLICT-814 | Cap R3 at V12 L2 = blueprint L1 with exact-hash approval; disable "L3 bounded mandate" (DEC-577) |
| SM-SVC-31-WF03-A05 | Authority R3 financial/legal/commitment; L2 mandatory approved effect; L3 only with separately approved bounded mandate where lawful; Approve source/d | CONFLICT-814 | Cap R3 at V12 L2 = blueprint L1 with exact-hash approval; disable "L3 bounded mandate" (DEC-577) |
| SM-SVC-32-WF04-A05 | Authority R3 financial/legal/commitment; L2 mandatory approved effect; L3 only with separately approved bounded mandate where lawful; Approve source/d | CONFLICT-814 | Cap R3 at V12 L2 = blueprint L1 with exact-hash approval; disable "L3 bounded mandate" (DEC-577) |
| SM-SVC-36-WF03-A01 | Identity and business outcome: Permitted sales meeting and conversation coaching; Authorized recording/notes, coaching rubric → Coaching feedback | CONFLICT-818 | Coach on staff-written notes only; recordings stay excluded (DEC-575) |
| SM-SVC-36-WF03-A02 | Trigger / supplied input: Manual; scheduled monitoring; validated business event; authorized provider webhook when available; Authorized recording/not | CONFLICT-818 | Coach on staff-written notes only; recordings stay excluded (DEC-575) |
| SM-SVC-36-WF03-A03 | Result / acceptance artifact: Coaching feedback; Coaching feedback; no unapproved external side effects | CONFLICT-818 | Coach on staff-written notes only; recordings stay excluded (DEC-575) |
| SM-SVC-36-WF03-A05 | Authority R0 internal analysis/draft; L1 assisted; L3 approved read/draft; Approve source/data rights and applicable external actions; review recordin | CONFLICT-818 | Coach on staff-written notes only; recordings stay excluded (DEC-575) |
| SM-SVC-36-WF03-A06 | Engine / agent: Multimodal AI; Workflow orchestration; Governance; Domain evidence review; Multimodal AI; policy review; orchestration; human speciali | CONFLICT-818 | Coach on staff-written notes only; recordings stay excluded (DEC-575) |
| SM-SVC-36-WF03-STEP-01 | Extract observable behaviors [Evidence/ingestion engine; SOURCE_DENIED → HELD] | CONFLICT-818 | Coach on staff-written notes only; recordings stay excluded (DEC-575) |
| SM-SVC-37-WF02-A01 | Identity and business outcome: Demand, margin and price sensitivity scenario modelling; Demand history, price assumptions, costs → Scenario report | CONFLICT-817 | Deterministic margin analytics only; sensitivity scenarios and live price tests need a Founder decision (DEC-574) |
| SM-SVC-37-WF02-A02 | Trigger / supplied input: Manual; scheduled monitoring; validated business event; authorized provider webhook when available; Demand history, price as | CONFLICT-817 | Deterministic margin analytics only; sensitivity scenarios and live price tests need a Founder decision (DEC-574) |
| SM-SVC-37-WF02-A03 | Result / acceptance artifact: Scenario report; Scenario report; no unapproved external side effects | CONFLICT-817 | Deterministic margin analytics only; sensitivity scenarios and live price tests need a Founder decision (DEC-574) |
| SM-SVC-37-WF02-A05 | Authority R0 internal analysis/draft; L1 assisted; L3 approved read/draft; Approve source/data rights and applicable external actions; approve experim | CONFLICT-817 | Deterministic margin analytics only; sensitivity scenarios and live price tests need a Founder decision (DEC-574) |
| SM-SVC-37-WF02-A06 | Engine / agent: Financial calculation; Workflow orchestration; Governance; Domain evidence review; Financial calculation; policy review; orchestration | CONFLICT-817 | Deterministic margin analytics only; sensitivity scenarios and live price tests need a Founder decision (DEC-574) |
| SM-SVC-37-WF02-STEP-01 | Estimate sensitivity with uncertainty [Rules/analytics engine; INVALID_METRIC → HELD] | CONFLICT-817 | Deterministic margin analytics only; sensitivity scenarios and live price tests need a Founder decision (DEC-574) |
| SM-SVC-37-WF02-STEP-02 | compare scenarios [Rules/analytics engine; INVALID_METRIC → HELD] | CONFLICT-817 | Deterministic margin analytics only; sensitivity scenarios and live price tests need a Founder decision (DEC-574) |
| SM-SVC-37-WF03-A01 | Identity and business outcome: Approved pricing and promotion experimentation; Approved price bounds, eligible variants and sample plan → Pricing expe | CONFLICT-817 | Deterministic margin analytics only; sensitivity scenarios and live price tests need a Founder decision (DEC-574) |
| SM-SVC-37-WF03-A02 | Trigger / supplied input: Manual; scheduled monitoring; validated business event; authorized provider webhook when available; Approved price bounds, e | CONFLICT-817 | Deterministic margin analytics only; sensitivity scenarios and live price tests need a Founder decision (DEC-574) |
| SM-SVC-37-WF03-A03 | Result / acceptance artifact: Pricing experiment result; Pricing experiment result; no unapproved external side effects | CONFLICT-817 | Deterministic margin analytics only; sensitivity scenarios and live price tests need a Founder decision (DEC-574) |
| SM-SVC-37-WF03-A05 | Authority R3 financial/legal/commitment; L2 mandatory approved effect; L3 only with separately approved bounded mandate where lawful; Approve source/d | CONFLICT-814 | Cap R3 at V12 L2 = blueprint L1 with exact-hash approval; disable "L3 bounded mandate" (DEC-577) |
| SM-SVC-37-WF03-A06 | Engine / agent: Financial calculation; Workflow orchestration; Governance; Domain evidence review; Financial calculation; policy review; orchestration | CONFLICT-817 | Deterministic margin analytics only; sensitivity scenarios and live price tests need a Founder decision (DEC-574) |
| SM-SVC-37-WF03-STEP-01 | Simulate or run approved experiment [Domain service; INVALID_STATE → HELD] | CONFLICT-817 | Deterministic margin analytics only; sensitivity scenarios and live price tests need a Founder decision (DEC-574) |
| SM-SVC-37-WF03-STEP-02 | enforce limits [Policy/validation engine; POLICY_DENIED → BLOCKED] | CONFLICT-817 | Deterministic margin analytics only; sensitivity scenarios and live price tests need a Founder decision (DEC-574) |
| SM-SVC-37-WF03-STEP-03 | measure outcomes [Rules/analytics engine; INVALID_METRIC → HELD] | CONFLICT-817 | Deterministic margin analytics only; sensitivity scenarios and live price tests need a Founder decision (DEC-574) |
| SM-SVC-39-WF03-A05 | Authority R3 financial/legal/commitment; L2 mandatory approved effect; L3 only with separately approved bounded mandate where lawful; Approve source/d | CONFLICT-814 | Cap R3 at V12 L2 = blueprint L1 with exact-hash approval; disable "L3 bounded mandate" (DEC-577) |

## 11.4.4 Catalogue reconciliation

### 11.4.4.1 Workflow → blueprint map and registry reconciliation (FSD ch12 × ch13 × blueprint)

Executor counts are in the order P policy/validation, I identity/reconciliation, D domain service, A domain agent, R rules/analytics, E effect adapter, V evidence/ingestion. "Consistent" means ch13 step count and rules/agent cue counts equal the ch12 step table. The ch12 channel column becomes the **service channel allowlist** that the PDP enforces at dispatch (D-F12-020, D-F12-025).

| Workflow | Title | Ch13 steps | Ch13 cues (rules / agent) | Ch12 executors (P I D A R E V) | Effect steps | Ch12 channel | Blueprint flow | Behaviour | Consistent |
|---|---|---|---|---|---|---|---|---|---|
| SM-SVC-21-WF01 | Invoice and payment evidence import | 3 | 0 / 0 | 1 1 1 0 0 0 0 | — | CRM | WF-11 (Part 2.2 §2.17) | Partially covered | Yes |
| SM-SVC-21-WF02 | Partial payment reconciliation | 4 | 0 / 1 | 2 0 1 1 0 0 0 | — | CRM | WF-11 partial payments | Partially covered | Yes |
| SM-SVC-21-WF03 | Discrepancy and financial reporting | 3 | 0 / 1 | 0 0 2 1 0 0 0 | — | CRM | WF-11 | Partially covered | Yes |
| SM-SVC-21-WF04 | Receivable anomaly and overdue payment-risk monitoring | 4 | 1 / 2 | 0 1 0 2 1 0 0 | — | CRM | WF-11 | Partially covered | Yes |
| SM-SVC-22-WF01 | Customer or partner onboarding plan | 3 | 0 / 2 | 1 0 0 2 0 0 0 | — | CRM, Partner | WF-12 (Part 2.2 §2.18) | Partially covered | Yes |
| SM-SVC-22-WF02 | Institutional pilot and deployment readiness | 3 | 0 / 1 | 1 0 1 1 0 0 0 | — | CRM, Partner | §2.21.1 MedMaarg institutional partnership | Partially covered | Yes |
| SM-SVC-22-WF03 | Milestone monitoring and handover | 4 | 0 / 0 | 1 0 2 0 0 1 0 | STEP-02 | CRM, Partner | WF-12 milestones and handover | Partially covered | Yes |
| SM-SVC-22-WF04 | Adaptive onboarding plans and readiness monitoring | 4 | 0 / 1 | 0 0 3 1 0 0 0 | — | CRM, Partner | WF-12 | Not covered | Yes |
| SM-SVC-23-WF01 | Renewal and obligation reminders | 4 | 1 / 1 | 1 0 1 1 1 0 0 | — | CRM, Email | WF-12 renewal calendar | Partially covered | Yes |
| SM-SVC-23-WF02 | Feedback and lost-deal analysis | 3 | 0 / 3 | 0 0 0 3 0 0 0 | — | CRM, Email | WF-12 lost-deal learning | Partially covered | Yes |
| SM-SVC-23-WF03 | Retention and re-engagement plan | 3 | 0 / 2 | 1 0 0 2 0 0 0 | — | CRM, Email | WF-31 | Partially covered | Yes |
| SM-SVC-23-WF04 | Churn and customer expansion opportunity prediction | 3 | 0 / 1 | 0 0 2 1 0 0 0 | — | CRM, Email | WF-17 (Part 9.7b) | Partially covered | Yes |
| SM-SVC-24-WF01 | Revenue and attribution calculation | 3 | 1 / 0 | 0 2 0 0 1 0 0 | — | CRM | AU-040 / AU-096 attribution (Part 9.8b) | Partially covered | Yes |
| SM-SVC-24-WF02 | Sales pipeline forecast | 3 | 1 / 0 | 1 0 1 0 1 0 0 | — | CRM | WF-29 forecast call (Part 9.8b) | Partially covered | Yes |
| SM-SVC-24-WF03 | Performance and optimization review | 4 | 1 / 2 | 0 0 1 2 1 0 0 | — | CRM | Part 2.4 RP-02, RP-16, RP-17 reviews | Partially covered | Yes |
| SM-SVC-24-WF04 | Revenue scenario simulation and forecast calibration | 4 | 2 / 1 | 0 0 1 1 2 0 0 | — | CRM | AU-041 backtest (KPI-29 MAPE) | Partially covered | Yes |
| SM-SVC-25-WF01 | Document intake and classification | 4 | 0 / 1 | 0 0 1 1 0 0 2 | — | Research, CRM | WF-01 knowledge ingestion (§2.7) | Partially covered | Yes |
| SM-SVC-25-WF02 | Knowledge grounding and revision | 4 | 1 / 0 | 0 1 1 0 1 0 1 | — | Research, CRM | WF-22 knowledge freshness (Part 9.7b) | Partially covered | Yes |
| SM-SVC-25-WF03 | Draft business document and expiry tracking | 4 | 0 / 2 | 1 0 0 2 0 0 1 | — | Research, CRM | WF-09 templates | Partially covered | Yes |
| SM-SVC-25-WF04 | Continuous business knowledge validation and contradiction detection | 4 | 0 / 1 | 1 0 2 1 0 0 0 | — | Research, CRM | WF-22 | Partially covered | Yes |
| SM-SVC-26-WF01 | Inbound AI voice enquiry and call routing | 3 | 0 / 2 | 0 0 1 2 0 0 0 | — | Voice | none (DEC-387) | Conflict | Yes |
| SM-SVC-26-WF02 | Authorized outbound voice engagement | 3 | 0 / 0 | 1 0 1 0 0 1 0 | STEP-02 | Voice | WF-27 human call tasks (DEC-392) | Conflict | Yes |
| SM-SVC-26-WF03 | Multilingual voice conversation and appointment coordination | 3 | 0 / 0 | 0 0 2 0 0 0 1 | — | Voice | WF-07 meetings | Conflict | Yes |
| SM-SVC-26-WF04 | Call intelligence, permitted transcription and CRM synchronization | 3 | 0 / 0 | 0 1 1 0 0 0 1 | — | Voice | AG-037 staff-written notes (DEC-218) | Conflict | Yes |
| SM-SVC-27-WF01 | Marketing image and advertising creative generation | 3 | 0 / 2 | 1 0 0 2 0 0 0 | — | Social, Website | WF-05 content (§2.11) | Conflict | Yes |
| SM-SVC-27-WF02 | Product demonstration and promotional video generation | 3 | 0 / 0 | 1 0 2 0 0 0 0 | — | Social, Website | WF-05 | Conflict | Yes |
| SM-SVC-27-WF03 | Multilingual audio, subtitle and creative localization | 3 | 0 / 1 | 0 0 2 1 0 0 0 | — | Social, Website | WF-19 localization (Part 9.7b) | Conflict | Yes |
| SM-SVC-27-WF04 | Brand, copyright, factual claim and creative quality validation | 3 | 0 / 1 | 1 0 1 1 0 0 0 | — | Social, Website | WF-05 claim approval | Partially covered | Yes |
| SM-SVC-28-WF01 | Machine-readable product and service catalog publication | 3 | 0 / 0 | 1 0 1 0 0 1 0 | STEP-02 | CRM, Partner | WF-01 product truth | Not covered | Yes |
| SM-SVC-28-WF02 | Authorized AI-agent requirement discovery and quotation exchange | 3 | 0 / 1 | 1 1 0 1 0 0 0 | — | CRM, Partner | WF-09 quote (§2.15) | Not covered | Yes |
| SM-SVC-28-WF03 | Agent-assisted purchasing and negotiation mandate coordination | 3 | 1 / 1 | 1 0 0 1 1 0 0 | — | CRM, Partner | WF-09 negotiation | Conflict | Yes |
| SM-SVC-28-WF04 | Authorized transaction, payment mandate and outcome reconciliation | 3 | 0 / 0 | 1 1 0 0 0 1 0 | STEP-02 | CRM, Partner | WF-11 closure | Conflict | Yes |
| SM-SVC-29-WF01 | Strategic account selection and account growth planning | 3 | 1 / 1 | 0 0 1 1 1 0 0 | — | CRM, Email, Research | WF-25 account-based engagement (Part 9.8b) | Partially covered | Yes |
| SM-SVC-29-WF02 | Buying committee and organizational relationship mapping | 2 | 0 / 1 | 0 0 1 1 0 0 0 | — | CRM, Email, Research | WF-25 | Partially covered | Yes |
| SM-SVC-29-WF03 | Account-specific multichannel campaign coordination | 2 | 0 / 0 | 1 0 1 0 0 0 0 | — | CRM, Email, Research | WF-25 | Partially covered | Yes |
| SM-SVC-29-WF04 | Account engagement, opportunity progression and expansion intelligence | 3 | 1 / 2 | 0 0 0 2 1 0 0 | — | CRM, Email, Research | WF-25 | Partially covered | Yes |
| SM-SVC-30-WF01 | Conversion funnel and abandonment analysis | 3 | 1 / 0 | 1 0 1 0 1 0 0 | — | Website, Paid ads | RP-02 funnel, RP-09 website analytics (Part 2.4) | Partially covered | Yes |
| SM-SVC-30-WF02 | Controlled landing page and offer experimentation | 3 | 1 / 0 | 1 0 1 0 1 0 0 | — | Website, Paid ads | WF-20 experiment lifecycle (Part 9.7b) | Partially covered | Yes |
| SM-SVC-30-WF03 | Privacy-respecting journey personalization | 3 | 0 / 0 | 1 0 2 0 0 0 0 | — | Website, Paid ads | WF-19 personalization (Part 9.7b) | Partially covered | Yes |
| SM-SVC-30-WF04 | Experiment effectiveness and incremental conversion evaluation | 2 | 1 / 1 | 0 0 0 1 1 0 0 | — | Website, Paid ads | WF-20 readout | Partially covered | Yes |
| SM-SVC-31-WF01 | Authorized marketplace product listing synchronization | 3 | 0 / 0 | 1 0 1 0 0 1 0 | STEP-03 | Website, Partner | WF-01 offering catalogue | Not covered | Yes |
| SM-SVC-31-WF02 | Marketplace pricing, availability and inventory synchronization | 3 | 0 / 0 | 1 1 0 0 0 1 0 | STEP-03 | Website, Partner | WF-10 stock reservation | Not covered | Yes |
| SM-SVC-31-WF03 | Order, cancellation and return-event coordination | 3 | 0 / 1 | 0 1 1 1 0 0 0 | — | Website, Partner | WF-10 order and fulfilment (§2.16) | Partially covered | Yes |
| SM-SVC-31-WF04 | Marketplace performance and reconciliation reporting | 2 | 0 / 0 | 0 1 1 0 0 0 0 | — | Website, Partner | AU-040 revenue reconciliation | Not covered | Yes |
| SM-SVC-32-WF01 | Partner recruitment and territory opportunity identification | 3 | 1 / 2 | 0 0 0 2 1 0 0 | — | Partner, CRM | WF-30 partner co-sell (Part 9.8b) | Partially covered | Yes |
| SM-SVC-32-WF02 | Partner product enablement and sales material distribution | 3 | 0 / 1 | 0 0 1 1 0 1 0 | STEP-02 | Partner, CRM | WF-30 | Partially covered | Yes |
| SM-SVC-32-WF03 | Deal registration, lead sharing and co-selling coordination | 3 | 0 / 1 | 1 1 0 1 0 0 0 | — | Partner, CRM | WF-30 deal registration | Partially covered | Yes |
| SM-SVC-32-WF04 | Partner performance, commission evidence and expansion monitoring | 3 | 1 / 1 | 0 0 1 1 1 0 0 | — | Partner, CRM | WF-30 commission records | Partially covered | Yes |
| SM-SVC-33-WF01 | Customer support ticket creation, classification and routing | 3 | 0 / 2 | 0 1 0 2 0 0 0 | — | CRM, Email, Website | Portal support W28/W34 | Partially covered | Yes |
| SM-SVC-33-WF02 | Evidence-grounded resolution and authorized self-service | 3 | 0 / 1 | 0 0 0 1 0 1 1 | STEP-03 | CRM, Email, Website | AG-031 / AG-014 grounded replies | Partially covered | Yes |
| SM-SVC-33-WF03 | SLA monitoring, escalation and service recovery | 3 | 1 / 1 | 0 0 1 1 1 0 0 | — | CRM, Email, Website | AU-027 SLA escalation | Partially covered | Yes |
| SM-SVC-33-WF04 | Support quality, recurring issue and resolution intelligence | 3 | 0 / 2 | 0 0 1 2 0 0 0 | — | CRM, Email, Website | WF-32 VoC themes | Partially covered | Yes |
| SM-SVC-34-WF01 | Authorized product usage and activation event analysis | 3 | 1 / 1 | 1 0 0 1 1 0 0 | — | Website, CRM | ADR-105 product-event ingress (Part 3.4) | Partially covered | Yes |
| SM-SVC-34-WF02 | Trial conversion and customer activation journeys | 3 | 0 / 2 | 0 0 1 2 0 0 0 | — | Website, CRM | §2.22.4 SaaS onboarding | Partially covered | Yes |
| SM-SVC-34-WF03 | Feature adoption and expansion opportunity detection | 1 | 0 / 1 | 0 0 0 1 0 0 0 | — | Website, CRM | WF-31 expansion | Partially covered | Yes |
| SM-SVC-34-WF04 | Usage-based upgrade and customer engagement recommendations | 3 | 1 / 1 | 0 0 1 1 1 0 0 | — | Website, CRM | WF-31 expansion via CPQ | Partially covered | Yes |
| SM-SVC-35-WF01 | Authorized review and brand reputation monitoring | 3 | 0 / 1 | 0 1 0 1 0 0 1 | — | Social, Research | AG-027 permitted public sources | Not covered | Yes |
| SM-SVC-35-WF02 | Review classification and evidence-grounded response drafting | 3 | 0 / 3 | 0 0 0 3 0 0 0 | — | Social, Research | AG-014 reply pattern | Not covered | Yes |
| SM-SVC-35-WF03 | Reputation incident detection and escalation | 3 | 0 / 1 | 1 0 1 1 0 0 0 | — | Social, Research | AU-031 compliance auto-pause | Not covered | Yes |
| SM-SVC-35-WF04 | Verified feedback trend and reputation improvement planning | 3 | 1 / 0 | 0 0 2 0 1 0 0 | — | Social, Research | WF-32 VoC loop | Partially covered | Yes |
| SM-SVC-36-WF01 | Sales knowledge and product playbook generation | 3 | 0 / 1 | 1 0 1 1 0 0 0 | — | CRM, Voice | AG-070 enablement coach (Part 9.8b) | Partially covered | Yes |
| SM-SVC-36-WF02 | Simulated customer objection and negotiation training | 3 | 0 / 0 | 0 0 3 0 0 0 0 | — | CRM, Voice | AG-046 objection-handling coach (Part 9.7b) | Partially covered | Yes |
| SM-SVC-36-WF03 | Permitted sales meeting and conversation coaching | 3 | 0 / 0 | 0 0 2 0 0 0 1 | — | CRM, Voice | AG-045 conversation intelligence, written only (DEC-386) | Conflict | Yes |
| SM-SVC-36-WF04 | Sales capability-gap and training recommendation generation | 3 | 0 / 2 | 0 0 1 2 0 0 0 | — | CRM, Voice | AG-070 | Partially covered | Yes |
| SM-SVC-37-WF01 | Pricing and product bundle profitability analysis | 3 | 2 / 1 | 0 0 0 1 2 0 0 | — | CRM | AU-049 contribution margin | Partially covered | Yes |
| SM-SVC-37-WF02 | Demand, margin and price sensitivity scenario modelling | 2 | 2 / 0 | 0 0 0 0 2 0 0 | — | CRM | none (CI-071) | Conflict | Yes |
| SM-SVC-37-WF03 | Approved pricing and promotion experimentation | 3 | 1 / 0 | 1 0 1 0 1 0 0 | — | CRM | WF-20 experiments | Conflict | Yes |
| SM-SVC-37-WF04 | Margin anomaly and commercial pricing-policy monitoring | 2 | 0 / 2 | 0 0 0 2 0 0 0 | — | CRM | AU-089 CPQ guardrails | Partially covered | Yes |
| SM-SVC-38-WF01 | Sender registration, template and communication eligibility validation | 2 | 0 / 0 | 2 0 0 0 0 0 0 | — | SMS/RCS | TR-R1 activation gates (Part 4.1) | Not covered | Yes |
| SM-SVC-38-WF02 | Authorized SMS and rich-message campaign coordination | 3 | 0 / 0 | 1 0 1 0 0 1 0 | STEP-02 | SMS/RCS | WF-06 outreach pattern | Not covered | Yes |
| SM-SVC-38-WF03 | Delivery, inbound response and approved channel fallback | 3 | 0 / 1 | 0 1 1 1 0 0 0 | — | SMS/RCS | WF-06 callbacks | Not covered | Yes |
| SM-SVC-38-WF04 | Messaging performance, usage and suppression monitoring | 3 | 1 / 1 | 1 0 0 1 1 0 0 | — | SMS/RCS | AU-024 suppression | Not covered | Yes |
| SM-SVC-39-WF01 | Supplier qualification and procurement requirement preparation | 4 | 1 / 2 | 1 0 0 2 1 0 0 | — | Partner, CRM | WF-10 OrganicSpec buy orders | Not covered | Yes |
| SM-SVC-39-WF02 | RFQ generation and supplier quotation comparison | 3 | 1 / 1 | 0 0 1 1 1 0 0 | — | Partner, CRM | WF-10 RFQ extraction (AG-023) | Partially covered | Yes |
| SM-SVC-39-WF03 | Approved purchase order and supplier commitment coordination | 3 | 1 / 0 | 0 0 1 0 1 1 0 | STEP-03 | Partner, CRM | WF-10 payables | Not covered | Yes |
| SM-SVC-39-WF04 | Supplier performance, delivery and procurement exception monitoring | 3 | 0 / 0 | 0 1 2 0 0 0 0 | — | Partner, CRM | WF-10 fulfilment ledger | Partially covered | Yes |

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

| Workflow | FSD ch12 R-class | Workbook side-effect label | Explicit effect step in ch12 | Resolution (DEC-570) |
|---|---|---|---|---|
| SM-SVC-21-WF01 | R3 | Internal analysis/draft | No | R-class governs; engine inserts NT13-10 approval before any state change or effect |
| SM-SVC-21-WF02 | R3 | Internal analysis/draft | No | R-class governs; engine inserts NT13-10 approval before any state change or effect |
| SM-SVC-22-WF03 | R2 | Internal analysis/draft | Yes | R-class governs; workbook label corrected |
| SM-SVC-23-WF01 | R2 | Internal analysis/draft | No | R-class governs; engine inserts NT13-10 approval before any state change or effect |
| SM-SVC-26-WF01 | R2 | Potential external write/communication; controlled | No | R-class governs; engine inserts NT13-10 approval before any state change or effect |
| SM-SVC-26-WF03 | R2 | Potential external write/communication; controlled | No | R-class governs; engine inserts NT13-10 approval before any state change or effect |
| SM-SVC-28-WF02 | R2 | Potential external write/communication; controlled | No | R-class governs; engine inserts NT13-10 approval before any state change or effect |
| SM-SVC-28-WF03 | R3 | Internal analysis/draft | No | R-class governs; engine inserts NT13-10 approval before any state change or effect |
| SM-SVC-29-WF03 | R2 | Potential external write/communication; controlled | No | R-class governs; engine inserts NT13-10 approval before any state change or effect |
| SM-SVC-30-WF02 | R3 | Internal analysis/draft | No | R-class governs; engine inserts NT13-10 approval before any state change or effect |
| SM-SVC-30-WF03 | R2 | Internal analysis/draft | No | R-class governs; engine inserts NT13-10 approval before any state change or effect |
| SM-SVC-31-WF03 | R3 | Internal analysis/draft | No | R-class governs; engine inserts NT13-10 approval before any state change or effect |
| SM-SVC-32-WF02 | R2 | Internal analysis/draft | Yes | R-class governs; workbook label corrected |
| SM-SVC-32-WF03 | R2 | Internal analysis/draft | No | R-class governs; engine inserts NT13-10 approval before any state change or effect |
| SM-SVC-32-WF04 | R3 | Internal analysis/draft | No | R-class governs; engine inserts NT13-10 approval before any state change or effect |
| SM-SVC-33-WF02 | R2 | Internal analysis/draft | Yes | R-class governs; workbook label corrected |
| SM-SVC-34-WF02 | R2 | Internal analysis/draft | No | R-class governs; engine inserts NT13-10 approval before any state change or effect |
| SM-SVC-37-WF03 | R3 | Consequential financial/legal or authority-bearing | No | R-class governs; engine inserts NT13-10 approval before any state change or effect |
| SM-SVC-38-WF03 | R2 | Potential external write/communication; controlled | No | R-class governs; engine inserts NT13-10 approval before any state change or effect |

### 11.4.4.4 Effect-step catalogue (every external effect in SVC-21…39)

| Step ID | Action | Workflow R-class | Adapter (port) | Approval binding | Status |
|---|---|---|---|---|---|
| SM-SVC-22-WF03-STEP-02 | send eligible reminders | R2 | ADP-EMAIL (SES) via outbox | Exact payload digest approved by R02 | Matched |
| SM-SVC-26-WF02-STEP-02 | initiate authorized call | R2 | ADP-VOICE (telephony/CPaaS, not procured) | Exact payload digest approved by R10, R01 | Adopted (DEC-782) |
| SM-SVC-28-WF01-STEP-02 | publish to authorized client endpoint | R2 | ADP-AGENT (MCP/A2A gateway, not procured) | Exact payload digest approved by R02, R10 | Matched |
| SM-SVC-28-WF04-STEP-02 | execute only via approved provider | R3 | ADP-AGENT (MCP/A2A gateway, not procured) | Exact payload digest approved by R08, R09, R01 | Adopted (DEC-780) |
| SM-SVC-31-WF01-STEP-03 | publish eligible updates | R2 | ADP-MKT (marketplace seller API, not procured) | Exact payload digest approved by R02, R10 | Matched |
| SM-SVC-31-WF02-STEP-03 | update authorized listings | R3 | ADP-MKT (marketplace seller API, not procured) | Exact payload digest approved by R02, R08 | Matched |
| SM-SVC-32-WF02-STEP-02 | grant scoped access | R2 | Portal grant (AU-090 pattern, R16P) | Exact payload digest approved by R02, R10 | Matched |
| SM-SVC-33-WF02-STEP-03 | execute eligible self-service or escalate | R2 | ADP-EMAIL reply via outbox; portal (W28/W34) | Exact payload digest approved by Tenant support lead | Matched |
| SM-SVC-38-WF02-STEP-02 | dispatch approved messages | R2 | ADP-SMS (DLT-registered SMS/RCS aggregator, not procured) | Exact payload digest approved by R05L, R10 | Matched |
| SM-SVC-39-WF03-STEP-03 | record supplier commitment | R3 | ADP-ERP (purchase order record/export, not procured) | Exact payload digest approved by R07, R08, R09 | Matched |

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
| 1 | Every requirement traced to a source | Pass | Each aspect carries its V12 chapter/section and blueprint location; CSV has 2075 rows |
| 2 | Assumptions, gaps, conflicts tagged and logged | Pass | Tags 814–831 used; register in Part 11.4d §11.4.9 |
| 3 | IDs unique and consistent | Pass | Aspect IDs asserted unique by `d_generate.py`; V12 IDs kept literally |
| 4 | No story lacks AC and no requirement lacks a test | N/A in this file | Stories and tests in Parts 11.4b/11.4d |
| 5 | Negative, edge, security, accessibility cases | Pass | Inconsistencies, conflicts and effect steps catalogued |
| 6 | No agent lacks guardrail, fallback, KPI, cost | N/A | No new agents (AG ranges belong to groups F and M); existing agents reused |
| 7 | Time-sensitive facts flagged | Pass | No prices or regulatory dates stated in this file |
| 8 | No restricted data to free-tier models | Pass | Tier 2 marked not eligible for every workflow handling personal or confidential data |
| 9 | Consistent with earlier parts | Pass | Mappings cite Parts 2.2, 2.3, 3.1–3.4, 7.4b, 9.4, 9.7–9.9 |

**Status: Part 11 Batch 11.4a complete. 2075 aspects inventoried and reconciled; 1976 Matched, 99 Pending Founder decision.** *(v1.2: every item counted here as "Pending Founder decision" was adopted by DEC-770…791 — Part 11.14; read as Adopted. Part 11.25.)*
