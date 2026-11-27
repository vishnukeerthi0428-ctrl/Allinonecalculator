# AI Growth Engine: Employee Sales & Marketing Automation
## Application Blueprint: PART 7 (Batch 7.4a), Source Pack Review: AI Agents, Prompts and RAG; Plugins, APIs, Open Source and Cost; Paid-Plugin Replacement (Coverage and Reconciliation)

| Field | Value |
|---|---|
| Document | Part 7, Batch 7.4a of 7.4a–7.4b (Group F source-pack review: documents 15, 16, 21, plus the automation library of document 38 §09) |
| Version | 1.0 · 27 Nov 2026 |
| Baseline | BRD, FRD; Parts 0, 0A (DEC-001…065, in particular DEC-007, DEC-008, DEC-020, DEC-022, DEC-023, DEC-025, DEC-041, DEC-047, DEC-048, DEC-051, DEC-053, DEC-064); Part 3.1 (ADR-018); Part 3.2 §3.2.4 (AD-01…AD-20, IP-01…IP-10); Part 7.1 (AG-001…036, AU-001…043, CI-001…135); Part 7.2 (cards, TL-01…20, envelope §7.2.7); Part 7.3 (tiers, routing, costs, governance, ADR-070…085); Part 8.2 §8.2.7 (B01–B23, C03) |
| Sources reviewed | Document 15 *AI Agents, Prompts, RAG and Intelligence Engineering* (46 KB, 406 lines); Document 16 *Plugin, API, Open Source and Cost Management* (626 KB, 9,097 lines, 538 candidate records); Document 21 *Paid Plugin Replacement and Open-Source Automation Strategy* (85 KB, 1,175 lines); Document 38 §09 automation-library counts |
| Roles applied | AI/ML Lead (lead), Prompt and RAG Engineer, Security/Compliance/AI Governance Lead, FinOps Lead, Procurement and Vendor Manager, Integration Architect, QA Lead, Product Owner |
| Tag ranges used | ASSUMPTION-400…419 · GAP-400…419 · CONFLICT-400…419 · RECOMMENDATION-400…419 · AG-037+ · AU-044+ · FR-ENH-F-### · US-<EP>-EF<nn> · TC-ENH-F-### |
| Machine-readable outputs | `final/coverage/F_coverage.csv` (804 rows: 266 atomic aspects + 538 candidate rows) · `final/coverage/F_integration_candidates.csv` (538 rows × 26 columns) · scripts `assembly/source_pack/F_parse_doc16_21.py`, `F_build_coverage.py` |

**Acronyms used in Part 7.4.** AG (AI agent) · AU (deterministic automation) · AL (automation-library use case, defined here) · IC (integration candidate, the source's record number) · PC (prompt contract, defined here) · PG (procurement gate step, defined here) · TPL (industry template, defined here) · NT13 (canonical workflow node type, defined here) · OKPI (the source pack's optimization KPI; the pack's KPI-01…35 are always written OKPI-01…35 in this blueprint because KPI-01…31 are already the business KPIs of Part 1) · OPT (the pack's optimization control ID, e.g. OPT-10-02) · RAG (retrieval-augmented generation) · ACL (access-control list) · TCO (total cost of ownership) · SBOM (software bill of materials) · AGPL (GNU Affero General Public License, network copyleft) · ECE (expected calibration error) · P/R (precision/recall) · PAYG (pay as you go).

**Numbering note [CONFLICT-410].** Batch 7.3 already uses the headings §7.4 (cost optimization), §7.5 (subscriptions and TCO), §7.6 (governance), §7.7 and §7.8 inside its own file. This batch is "Part 7.4" by coordinator instruction and numbers its sections 7.4.1…7.4.9. To avoid ambiguity, references to Batch 7.3 are always written **"Part 7.3 §7.x.y"**; references without a file prefix point into this batch. The assembly step (Part 10) should renumber one of them (proposed resolution in §7.4.6).

---

## 7.4.1 Documents reviewed

### 7.4.1.1 Document 15: AI Agents, Prompts, RAG and Intelligence Engineering

| Item | Detail |
|---|---|
| Size and structure | 46,256 bytes, 406 extracted lines, 8 Heading-1 sections, 52 Heading-2 sections, 5 tables |
| Sections | Product purpose and operating boundary · Initial startup configurations · Technology and execution principles · **Logical AI responsibilities and typed prompt contracts (18 responsibilities)** · RAG and model-gateway rules · Engineering contracts · Website and confidential Admin operating contract · Public AI versus confidential Copilot · Local AI, model fallback and evaluation · AI evaluation and change governance · Implementation, verification and delivery controls (scoped AI task contract, evaluation table) · Acceptance and evidence record · AI evaluation rubric and autonomy constraints · Optimization engineering and acceptance (OPT-01, 03, 04, 05, 10, 11) · Implementation acceptance and verification (11 procedures, repeated as final decision controls) · Current multi-startup scope |
| What it is trying to tell | The AI layer is a **set of typed, narrow responsibilities**, each a prompt contract with fixed inputs, outputs and a common result envelope; retrieved content is data, never instructions; policy, identity, finance and approvals are deterministic services; every model or prompt change is benchmarked on frozen labelled data before activation; and no synthetic test is production certification |
| Pattern | Shared common core (purpose, startups, stack, Website/Admin contract, engineering contracts, current scope) + domain block (contracts, RAG, Copilot separation, evaluation, OPT-10/11) + acceptance procedures |
| Atomic aspects | **98** (7 common core, 18 prompt contracts, 73 rules/controls/procedures) |

### 7.4.1.2 Document 16: Plugin, API, Open Source and Cost Management

| Item | Detail |
|---|---|
| Size and structure | 626,068 bytes, 9,097 lines, 13 Heading-1 sections, **538 Heading-2 candidate records** (each with exactly 15 fields, verified by parser), 1 budget register (22 rows with live formulas and cached values), 2 effort/cost tables, procurement and acceptance tables |
| Sections | Product purpose · Integration selection and procurement gates · **Individual candidate register (538 records)** · **Source operating budget register** · Consolidated effort and operating cost assumptions · Website and Admin operating contract (+ website-specific integration and cost controls) · Paid-plugin substitution and procurement rule · Provider procurement and operating economics · Implementation, verification and delivery controls (integration procurement and runtime control) · Provider procurement and benchmark approval · Optimization engineering (OPT-03, 09, 10, 20) · Implementation acceptance and verification (10 procedures + benchmark execution) · Current scope |
| What it is trying to tell | Every plugin or API the founders' tool inventory contains is **retained for traceability but disabled**; nothing is bought because it is listed; free software still costs hosting and staff time; every activation needs a verified licence, entitlement, quota, rate, data-processing term, sandbox benchmark, approved budget and rollback; and the pilot runtime is ₹16,675 per month (₹31,165 with optional Apollo and developer seats) |
| Fields per candidate | Category · Source priority · Decision / cost treatment · Application · Commercial modules · Interface · Trigger · Acceptance · Procurement · Licence · Free tier · Paid API · Allocation · Official / evidence URL · Verification status |
| Atomic aspects | **85** rule/budget/procedure aspects + **538** candidate records (IC-001…IC-538) |

### 7.4.1.3 Document 21: Paid Plugin Replacement and Open-Source Automation Strategy

| Item | Detail |
|---|---|
| Size and structure | 85,450 bytes, 1,175 lines, 15 Heading-1 sections; 27-row capability replacement register; 97-row named-decision table; 26-category supporting inventory (441 names); 28-category benchmark plan |
| Sections | 1 Purpose, scope and procurement decision (4 decision classes) · 2 Preferred deployment architecture · 3 Capability replacement register (01…27) · 4 Adapter selection, activation and rollback (7 stages) · 5 Engineering contract and deployment checklist · 6 Cost model (subscription avoided is not total saving) · 7 Named integration decisions · 8 Supporting-candidate inventory · 9 Upstream verification references · Replacement procurement gate · Native replacement benchmark and fallback decision · Optimization (repeat) · Implementation acceptance (open-source economics, entitlement, shared adapter code) · Current scope |
| What it is trying to tell | **Build the automation in-house** on Django/Celery/PostgreSQL/Valkey, keep open-source upstreams where they fit, use paid external services only where proprietary data, regulated transactions or official channels make them unavoidable, and prove any replacement with the same labelled workload and a full-cost comparison per verified outcome, not per avoided subscription |
| Atomic aspects | **79** rule/benchmark/metric aspects (the 538 candidate decisions are counted once, under IC rows) |

### 7.4.1.4 Document 38 §09: automation library (assigned to Group F)

| Item | Detail |
|---|---|
| Content | Counts only: 20 industry/business templates, 20 use-case groups × 5 = 100 use cases, 13 workflow node types, 4 seeded startups; the 20 group names; a statement that the library is a catalogue of proposed use cases, not 100 live integrations |
| Finding | None of documents 15, 16 or 21 (nor any other pack document, checked with a full-text search of all 38 extractions) **names** the 100 use cases, the 20 templates or the 13 node types [GAP-401]. Group F therefore maps the 20 groups to the AG/AU catalogue and **proposes** the 100 use cases, 20 templates and 13 node types in Part 7.4b §7.4.5.7 [ASSUMPTION-400] |
| Atomic aspects | **4** |

### 7.4.1.5 Method

1. Each document was read in full from its plain-text extraction; all prose sections were read line by line, and the repeated common-core blocks were identified once and marked "common core: see document 01/02 coverage".
2. Document 16's 538 candidate records and its budget register, and document 21's named-decision table, supporting inventory and benchmark-category table were parsed programmatically (`F_parse_doc16_21.py`). The parser asserts that exactly 538 records exist, that every record has all 15 fields, and that every supporting-inventory category lists exactly the number of names its heading states. All 538 candidates were matched to a document-21 decision (97 named + 441 supporting, 0 unmatched).
3. Every aspect was checked against the blueprint with full-text search and by reading Parts 0A, 3.1, 3.2 §3.2.4, 7.1, 7.2, 7.3 and 8.2 §8.2.7. Status values: Covered, Partially covered, Not covered, Conflict, Not applicable (with reason).
4. Every Partially covered, Not covered and Conflict aspect has an enhancement in Part 7.4b or a conflict with a proposed resolution in §7.4.6.

---

## 7.4.2 Coverage register summary

| Document | Covered | Partially covered | Not covered | Conflict | Not applicable | Total |
|---|---|---|---|---|---|---|
| 15 AI Agents, Prompts, RAG | 59 | 21 | 4 | 7 | 7 | 98 |
| 16 Plugin, API, OSS and Cost (aspects) | 42 | 14 | 22 | 3 | 4 | 85 |
| 21 Paid Plugin Replacement (aspects) | 38 | 12 | 19 | 6 | 4 | 79 |
| 38 §09 Automation library (assigned) | 1 | 3 | 0 | 0 | 0 | 4 |
| Integration candidates IC-001…IC-538 (16 + 21) | 485 | 0 | 0 | 1 | 52 | 538 |
| **Total** | **625** | **50** | **45** | **17** | **67** | **804** |

**Reading the table.** The source pack is largely consistent with the blueprint's AI design: 625 of 804 rows are already covered (59 of 98 document-15 aspects, including 13 of the 18 prompt contracts). The 50 partial and 45 not-covered rows cluster in five places: (1) the **AI result envelope and prompt-contract minimum output**, (2) **RAG revocation and authorization-safe caching**, (3) **procurement records, licence/model-weight register, benchmark harness and adapter retirement**, (4) **replacement economics, invoice reconciliation and tenant margin**, and (5) **budget views** that Part 8.2 does not show. The 17 conflict rows (13 distinct conflicts, CONFLICT-400…412) are resolved in Part 7.4b §7.4.6. The 52 "Not applicable" candidate rows are investor, clinical, learner-assessment and HR tools that fall outside the commercial scope (DEC-002, DEC-030) or have no runtime need.

| Status | What it means for the build |
|---|---|
| Covered (625) | No change; the cited blueprint section is authoritative |
| Partially covered (50) | Enhancement in Part 7.4b adds the missing field, rule, automation or test |
| Not covered (45) | New requirement, automation, entity, metric or test in Part 7.4b |
| Conflict (17 rows) | Proposed resolution in Part 7.4b §7.4.6 for the coordinator to turn into a decision |
| Not applicable (67) | Common-core repeats and duplicate procedures (15 aspects); out-of-scope or no-runtime-need candidates (52) |

---

## 7.4.3 Detailed coverage register

All 266 atomic aspects are listed individually below. The 538 candidate rows are reconciled in §7.4.4.2 (all 97 named candidates individually; the 441 supporting candidates by category) and individually in `F_coverage.csv` and `F_integration_candidates.csv`.

**Document 15**

| Aspect | Section | Aspect summary | Status | Blueprint location | Action | New IDs |
|---|---|---|---|---|---|---|
| F15-001 | Product purpose and operating boundary | Commercial growth only; no investor/fundraising; independent deployment | Not applicable | Part 0 §0.2; DEC-002 | Common core: see document 01/02 coverage | — |
| F15-002 | Initial startup configurations | Four seeded startups and commercial focus | Not applicable | Part 1 §1.3 | Common core: see document 01/02 coverage | — |
| F15-003 | Technology and execution principles | Stack, open-source-first, autonomy modes, recheck at execution | Not applicable | Part 3.1; DEC-064 | Common core: see document 01/02 coverage | — |
| F15-010 | Logical AI responsibilities and typed prompt contracts | Prompt contract 'Knowledge': Approved claims, documents, offering -> approved facts, citations, unknowns | Covered | Part 7.2 §7.2.2 (AG-001; TL-09; AU-029) | Mapped in prompt contract registry | PC-01 |
| F15-011 | Logical AI responsibilities and typed prompt contracts | Prompt contract 'Research': Permitted sources, geography -> queries, evidence, source IDs, freshness | Covered | Part 7.2 §7.2.2 (AG-003, AG-004; AU-007, AU-014) | Mapped in prompt contract registry | PC-02 |
| F15-012 | Logical AI responsibilities and typed prompt contracts | Prompt contract 'Signal': Source records -> signal type, evidence, confidence | Covered | Part 7.2 §7.2.2 (AG-005) | Mapped in prompt contract registry | PC-03 |
| F15-013 | Logical AI responsibilities and typed prompt contracts | Prompt contract 'Matching': Verified evidence + approved scoring -> score factors, missing evidence, explanation | Partially covered | Part 7.2 §7.2.2 (AU-016, AU-017 (rules); AG-007) | Bound to prompt contract registry; envelope v2 | PC-04; FR-ENH-F-001 (missing_fields) |
| F15-014 | Logical AI responsibilities and typed prompt contracts | Prompt contract 'Contact': Org/person professional source -> role, channel, provenance, verification status | Covered | Part 7.2 §7.2.2 (AG-008; AU-018) | Mapped in prompt contract registry | PC-05 |
| F15-015 | Logical AI responsibilities and typed prompt contracts | Prompt contract 'Engagement': Eligible contact, approved facts, channel -> draft, claims, source IDs, escalation | Covered | Part 7.2 §7.2.2 (AG-011; AG-012; TL-10) | Mapped in prompt contract registry | PC-06 |
| F15-016 | Logical AI responsibilities and typed prompt contracts | Prompt contract 'Response': Inbound + thread -> intent, objection, next action, stop flag | Covered | Part 7.2 §7.2.2 (AG-013, AG-014; AU-008) | Mapped in prompt contract registry | PC-07 |
| F15-017 | Logical AI responsibilities and typed prompt contracts | Prompt contract 'Objection': Concern + approved evidence -> answer draft or specialist escalation | Covered | Part 7.2 §7.2.2 (AG-021) | Mapped in prompt contract registry | PC-08 |
| F15-018 | Logical AI responsibilities and typed prompt contracts | Prompt contract 'Planner': Objective, scope, budget, state, deadlines -> actions, cost, dependencies, approval | Partially covered | Part 7.2 §7.2.2 (AG-016; TL-18) | Bound to prompt contract registry; envelope v2 | PC-09; FR-ENH-F-001 (cost_estimate, requires_approval) |
| F15-019 | Logical AI responsibilities and typed prompt contracts | Prompt contract 'Meeting': Authorized transcript/notes -> summary, actions, confirmed vs unconfirmed | Not covered | Part 7.2 §7.2.2 (GAP-143 (excluded in Part 7.1)) | Bound to prompt contract registry; envelope v2 | PC-10; AG-037 (new); FR-ENH-F-026 |
| F15-020 | Logical AI responsibilities and typed prompt contracts | Prompt contract 'Forecast': Actual pipeline + evidence -> scenario, assumptions, uncertainty | Partially covered | Part 7.2 §7.2.2 (AU-041 (rules) + AG-029 narrative) | Bound to prompt contract registry; envelope v2 | PC-11; AG-029 forecast mode (FR-ENH-F-002) |
| F15-021 | Logical AI responsibilities and typed prompt contracts | Prompt contract 'Quality': Candidate output, gold case, policy -> pass/fail, reason, severity | Covered | Part 7.2 §7.2.2 (AG-002; AG-012; AU-006) | Mapped in prompt contract registry | PC-12 |
| F15-022 | Logical AI responsibilities and typed prompt contracts | Prompt contract 'Cost routing': Token estimate, models, caps -> selected model, reserve, fallback | Conflict | Part 7.2 §7.2.2 (AU-001, AU-002 (deterministic by design)) | Bound to prompt contract registry; envelope v2 | PC-13; CONFLICT-411 |
| F15-023 | Logical AI responsibilities and typed prompt contracts | Prompt contract 'Copilot': Authorized scoped request -> read/draft/action proposal, confirmation | Covered | Part 7.2 §7.2.2 (AG-015; DEC-035) | Mapped in prompt contract registry | PC-14 |
| F15-024 | Logical AI responsibilities and typed prompt contracts | Prompt contract 'Business need': Organization requirement + source -> need and offering match | Covered | Part 7.2 §7.2.2 (AG-006; AU-016) | Mapped in prompt contract registry | PC-15 |
| F15-025 | Logical AI responsibilities and typed prompt contracts | Prompt contract 'Content and SEO': Approved offering + audience -> draft content, claims, review | Covered | Part 7.2 §7.2.2 (AG-018; AG-012; AU-033) | Mapped in prompt contract registry | PC-16 |
| F15-026 | Logical AI responsibilities and typed prompt contracts | Prompt contract 'Proposal': Approved prices + bid/order requirements -> draft quote/proposal, assumptions | Covered | Part 7.2 §7.2.2 (AG-020; AU-035) | Mapped in prompt contract registry | PC-17 |
| F15-027 | Logical AI responsibilities and typed prompt contracts | Prompt contract 'Retention': Delivery, feedback, contract -> renewal opportunity and next action | Partially covered | Part 7.2 §7.2.2 (AU-039; AG-011 renewal mode; AG-026) | Bound to prompt contract registry; envelope v2 | PC-18; AG-038 (new); FR-ENH-F-027 |
| F15-030 | Prompt contracts | Common instruction: retrieved docs are untrusted data; authorized scope; JSON; unknown when unsupported; cite evidence IDs; no invented claims; no direct external execution | Covered | Part 7.3 §7.6.3, §7.6.5; BRL-AI-03/04; ADR-082 | None (already covered) | — |
| F15-031 | Prompt contracts | Required envelope: tenant_id, startup_id, purpose, schema_revision, evidence_ids, confidence, missing_fields, policy_flags, proposed_action, requires_approval, cost_estimate | Partially covered | Part 7.2 §7.2.7 (envelope lacks purpose, missing_fields, policy_flags, proposed_action, requires_approval, cost_estimate) | Envelope v2 specified | FR-ENH-F-001; GAP-405; RECOMMENDATION-400 |
| F15-032 | Prompt contracts | Evaluation per contract: schema, scope isolation, factual support, injection, unknown handling, deterministic policy gate, regression | Covered | Part 7.3 §7.6.9; Part 6.4 | None (already covered) | — |
| F15-033 | RAG | Tenant/product/startup ACL before retrieval AND after ranking | Partially covered | Part 7.2 TL-01 (namespace before retrieval only) | Post-ranking ACL recheck specified | FR-ENH-F-003; GAP-407 |
| F15-034 | RAG | Chunk carries document version, checksum, approval, effective time, expiry | Partially covered | Part 7.3 THR-057 (approved versions only) | Chunk metadata and window filter | FR-ENH-F-004 |
| F15-035 | RAG | Remove revoked chunks and cache entries | Partially covered | Part 7.2 §7.2.6 (invalidate on version change); AU-011 (privacy purge) | Revocation propagation automation | AU-046; FR-ENH-F-005 |
| F15-036 | RAG | Citations to approved evidence | Covered | BRL-AI-03; Part 7.3 §7.6.5 | None (already covered) | — |
| F15-037 | Model gateway | Gateway selects low-cost reliable model by task, reserves tokens, caps context, validates, bounded retry or approved fallback | Covered | Part 7.3 §7.3.4, §7.3.7; ADR-070 | None (already covered) | — |
| F15-038 | Model gateway | No autonomous approval of legal/financial terms, consent or payment | Covered | DEC-064; Part 7.3 §7.6.1 | None (already covered) | — |
| F15-039 | Model gateway | Dry run with stub adapters; validate exact plan hash before dispatch | Covered | IP-08; BRL-AUT-04; AG-016 | None (already covered) | — |
| F15-040 | Model gateway | Eval datasets synthetic/authorized; tenant evidence separate; no cross-client learning by default | Partially covered | RECOMMENDATION-017; Part 7.3 §7.6.9 (cross-client learning rule not explicit) | Explicit no-cross-tenant-learning rule | FR-ENH-F-006 |
| F15-041 | Engineering contracts | REST conventions, status codes, idempotency, outbox, callbacks | Not applicable | Part 3.2 §3.2.1 | Common core: see document 01/02 coverage | — |
| F15-042 | Engineering contracts | Independent PostgreSQL, UUID PK, RLS, revision, decimal currency | Not applicable | Part 3.3 | Common core: see document 01/02 coverage | — |
| F15-043 | Website and Admin contract | 147 interfaces, surfaces, routing namespaces, publication snapshots | Not applicable | Part 2.5; Part 3.2 §3.2.1.1 | Common core: see document 01/02 coverage | — |
| F15-044 | Public AI versus confidential Copilot | Public assistant: approved published snapshot only, host/startup/locale scoped; no staff tools | Covered | AG-017; TL-01 public namespace | None (already covered) | — |
| F15-045 | Public AI versus confidential Copilot | Portal AI: granted materials and own thread only | Covered | AG-031 (portal grant scope) | None (already covered) | — |
| F15-046 | Public AI versus confidential Copilot | Admin Copilot: staff scope and approved tool allowlist | Covered | AG-015; §7.2.4 | None (already covered) | — |
| F15-047 | Public AI versus confidential Copilot | Injection cannot widen retrieval or execute publication, money or outreach | Covered | ADR-082; Part 7.3 §7.6.3 | None (already covered) | — |
| F15-048 | Public AI versus confidential Copilot | Red-team cross-tenant AND cross-audience (public/portal/admin) leakage; default deny | Partially covered | Part 7.3 §7.7.2 (cross-tenant only) | Cross-audience red-team cases | TC-ENH-F-006 |
| F15-049 | Local AI, fallback, evaluation | Typed Python gateway; local embedding/retrieval in PostgreSQL/pgvector | Covered | ADR-070, ADR-077; Part 7.3 §7.5.1 | None (already covered) | — |
| F15-050 | Local AI, fallback, evaluation | Validate model-weight commercial rights separately from framework licence | Not covered | — | Licence register incl. model weights | AU-047; FR-ENH-F-017; GAP-403 |
| F15-051 | Local AI, fallback, evaluation | Benchmark CPU/GPU cost, latency and accuracy of local inference | Covered | RECOMMENDATION-067 (W6 spike) | None (already covered) | — |
| F15-052 | Local AI, fallback, evaluation | No paid AI subscription as prerequisite; paid model fallback needs per-tenant allowance, redacted prompts, budget reservation | Conflict | DEC-007 (paid Anthropic Tier 1 primary) | Resolution proposed | CONFLICT-400; FR-ENH-F-030 |
| F15-053 | Local AI, fallback, evaluation | Labelled examples for classification, extraction, relevance, response, objections, injection, unsupported facts | Covered | Part 6.4 datasets; GAP-142 | None (already covered) | — |
| F15-054 | Local AI, fallback, evaluation | Unit: schema/policy; SIT: scoped RAG, fallback, tool permissions; UAT: explanations and escalation | Covered | Part 6.1, 6.4 | None (already covered) | — |
| F15-055 | AI evaluation and change governance | Benchmark model/prompt change vs baseline (grounding, privacy, refusal, latency, cost); approve before activation; roll back | Covered | AU-006; ADR-084; Part 7.3 §7.6.9 | None (already covered) | — |
| F15-056 | AI evaluation and change governance | Delivery evidence against build/env/scope/reviewer; critical defects block activation | Covered | Part 8.2 §8.2.4.2 | None (already covered) | — |
| F15-057 | Scoped AI task contract | Example contract: return {answer, evidence_ids, escalate}; unknown -> escalate; policy/identity/finance deterministic | Partially covered | Part 7.2 card outputs (per-agent shapes, no common minimum) | Common minimum output in registry | FR-ENH-F-002 |
| F15-058 | Evaluation table | Output shape: 100% critical outputs parse or fail closed | Covered | AU-003; BRL-AI-02 | None (already covered) | — |
| F15-059 | Evaluation table | Grounding: zero private leakage; unsupported claim -> refusal/escalation | Covered | Part 7.3 §7.6.5 | None (already covered) | — |
| F15-060 | Evaluation table | Matching: precision/recall AND calibration; owner approves minimum | Partially covered | Part 6.4 (precision/recall; calibration not specified) | Calibration (ECE) metric | TC-ENH-F-009 |
| F15-061 | Evaluation table | Prompt injection: no unauthorized tool action or disclosure | Covered | Part 7.3 §7.6.3 | None (already covered) | — |
| F15-062 | Evaluation table | Fallback: timeout, quota, local model unavailable, paid fallback disabled -> safe retry, no unapproved charge | Covered | Part 7.3 §7.3.4 R9-R13; FB sets | None (already covered) | — |
| F15-063 | Evaluation table | Model change: record model, prompt hash and dataset hash | Partially covered | ADR-084 (eval run link; dataset hash not explicit) | Eval run record fields | FR-ENH-F-007 |
| F15-064 | Evaluation table | Seed JSONL is synthetic, not a benchmark; expand per startup/language/category; independent human or calibrated evaluator; no patient/child/investor data | Covered | GAP-142; Part 7.3 §7.6.6 judge calibration | None (already covered) | — |
| F15-065 | Acceptance and evidence record | Evidence fields: responsible/reviewer, artifact, decision, remediation, business acceptance | Covered | Part 8.2 §8.2.4.2 | None (already covered) | — |
| F15-066 | Evaluation cases | Evidence A allowed, B foreign -> only allowed IDs; unknown -> escalate | Covered | Part 6.4 cross-scope cases | None (already covered) | — |
| F15-067 | Evaluation cases | Malformed output -> bounded retry then hold/escalate; no action | Covered | AU-003 | None (already covered) | — |
| F15-068 | Evaluation cases | Simulation: nonfinite or negative costs rejected; zero external effects | Partially covered | TP simulation oracle (Part 6.1); numeric validation absent | Numeric validation rule | FR-ENH-F-008 |
| F15-069 | Evaluation cases | Critical isolation, unsupported claims, privacy, financial cases require 100% pass | Covered | Part 5.1a D-11; Part 7.3 §7.6.9 | None (already covered) | — |
| F15-070 | Optimization | Deterministic rules before AI; benchmark model and RAG on frozen samples; report error, cost, latency | Covered | Part 7.3 §7.4.2 technique 3; ADR-073 | None (already covered) | — |
| F15-071 | Optimization engineering | OPT-01-01: Authentication, privileged sessions, MFA, revoke | Covered | Part 4.1 | None (already covered) | — |
| F15-072 | Optimization engineering | OPT-03-01: Native vs paid plugins; benchmark before enabling; zero unapproved paid calls; full TCO | Partially covered | BRD §10 (paid off by default); no TCO procedure | Enhancement / resolution in Part 7.4b | AU-044, AU-045; FR-ENH-F-012, FR-ENH-F-018 |
| F15-073 | Optimization engineering | OPT-04-01: Daily planning/discovery: missed runs recover once; prohibited source never fetched | Covered | AG-003; AU-028; AU-007 | None (already covered) | — |
| F15-074 | Optimization engineering | OPT-04-02: Qualification: precision >= 90% on benchmark; uncertain to review | Conflict | DEC-001 (80% W1 exit; 90% before L2) | Enhancement / resolution in Part 7.4b | CONFLICT-405 |
| F15-075 | Optimization engineering | OPT-04-03: Outreach: zero sends to ineligible; reply cancels follow-up | Covered | AU-009, AU-022 | None (already covered) | — |
| F15-076 | Optimization engineering | OPT-04-04: Objection & meetings: no unsupported promises or double-booking | Covered | AG-021; AU-023 | None (already covered) | — |
| F15-077 | Optimization engineering | OPT-04-05: Documents/approvals: zero execution with stale/missing approval | Covered | CA-APPROVE; AU-036 | None (already covered) | — |
| F15-078 | Optimization engineering | OPT-04-06: Financial closure: zero duplicate side effects; 100% verified reconciled | Covered | AU-037, AU-040 | None (already covered) | — |
| F15-079 | Optimization engineering | OPT-04-07: Exception/learning: completion >= 99% of eligible due runs; no blind repeat | Partially covered | AU-026, AU-028 (target not stated) | Enhancement / resolution in Part 7.4b | OKPI-09 wired (FR-ENH-F-031) |
| F15-080 | Optimization engineering | OPT-04-08: Autonomy/stop: >= 90% eligible steps automated; stop prevents future calls | Partially covered | AU-025; DEC-064 (automation share not tracked) | Enhancement / resolution in Part 7.4b | OKPI-10 wired (FR-ENH-F-031) |
| F15-081 | Optimization engineering | OPT-05-01: Transactional outbox | Covered | IP-02; Part 3.1 | None (already covered) | — |
| F15-082 | Optimization engineering | OPT-10-01: Rules-first routing; compare quality/latency/INR per task | Covered | Part 7.3 §7.3.4; §7.4.1 | None (already covered) | — |
| F15-083 | Optimization engineering | OPT-10-02: >= 99.5% schema-valid outputs; report token p50/p95 | Conflict | Part 7.3 §7.6.9 (>= 99% first pass) | Enhancement / resolution in Part 7.4b | CONFLICT-404 |
| F15-084 | Optimization engineering | OPT-10-03: >= 95% evidence-grounded accuracy | Covered | Part 7.3 §7.6.9 groundedness >= 95% | None (already covered) | — |
| F15-085 | Optimization engineering | OPT-10-04: Caching by full scope/model/prompt/knowledge version; no cross-scope or stale hit | Partially covered | AU-001 key lacks principal/grant/permission/policy revision | Enhancement / resolution in Part 7.4b | FR-ENH-F-009; GAP-406 |
| F15-086 | Optimization engineering | OPT-10-05: Local inference benchmark; no silent paid fallback | Covered | RECOMMENDATION-067; DEC-007 | None (already covered) | — |
| F15-087 | Optimization engineering | OPT-10-06: Adversarial benchmark: zero forbidden actions; versioned datasets | Covered | Part 7.3 §7.6.3 | None (already covered) | — |
| F15-088 | Optimization engineering | OPT-11-01: Provenance and source rights; missing rights quarantined | Covered | AU-007; M07 | None (already covered) | — |
| F15-089 | Optimization engineering | OPT-11-02: Per-source freshness SLA; reverify before external action | Covered | AU-018; AU-007 | None (already covered) | — |
| F15-090 | Optimization engineering | OPT-11-03: Identity/dedupe: never merge by name alone | Covered | AU-015 | None (already covered) | — |
| F15-091 | Optimization engineering | OPT-11-04: Classification precision >= 90%; disclose recall and sample size | Conflict | DEC-001 | Enhancement / resolution in Part 7.4b | CONFLICT-405 |
| F15-092 | Optimization engineering | OPT-11-05: Corrections/deletion propagate to caches and embeddings; legal hold | Partially covered | AU-011 (privacy purge) | Enhancement / resolution in Part 7.4b | AU-046 |
| F15-093 | Implementation acceptance and verification (duplicated in final decision controls) | Acceptance procedure 'AI routing cost': 100-task synthetic routing fixture vs all-advanced baseline; arithmetic reproducible | Partially covered | Part 7.3 §7.4.1 waterfall (no fixture test) | Test added | TC-ENH-F-011 |
| F15-094 | Implementation acceptance and verification (duplicated in final decision controls) | Acceptance procedure 'Retention and scoped vector indexing': Delete/expire source; indexes, caches, embeddings updated; legal hold | Partially covered | AU-011 | Test added | AU-046; TC-ENH-F-004 |
| F15-095 | Implementation acceptance and verification (duplicated in final decision controls) | Acceptance procedure 'RAG scope and evidence': Tenant A material + tenant B distractor; no foreign evidence | Covered | Part 6.4 | None (already covered) | — |
| F15-096 | Implementation acceptance and verification (duplicated in final decision controls) | Acceptance procedure 'Structured output quality': Valid/malformed/unexpected fields; >= 99.5% valid; invalid never drives side effects | Conflict | CONFLICT-404 | Test added | TC-ENH-F-012 |
| F15-097 | Implementation acceptance and verification (duplicated in final decision controls) | Acceptance procedure 'Model selection and token efficiency': Small vs advanced on fixed corpus; tokens, latency, cost; >= 95% grounded | Covered | ADR-073; Part 6.4 | None (already covered) | — |
| F15-098 | Implementation acceptance and verification (duplicated in final decision controls) | Acceptance procedure 'Prompt injection and tool access': Hostile text requesting secrets/tool calls; no disclosure | Covered | Part 6.4 RT sets | None (already covered) | — |
| F15-099 | Implementation acceptance and verification (duplicated in final decision controls) | Acceptance procedure 'Prompt/model version regression': Freeze prompt/model/dataset/policy; rerun benchmark before promoting | Covered | AU-006 | None (already covered) | — |
| F15-100 | Implementation acceptance and verification (duplicated in final decision controls) | Acceptance procedure 'Classification quality': Precision >= 90%; recall measured; no claim from five synthetic documents | Conflict | CONFLICT-405 | Test added | TC-ENH-F-013 |
| F15-101 | Implementation acceptance and verification (duplicated in final decision controls) | Acceptance procedure 'Objection resolution': Supported vs unsupported; approved response or escalation | Covered | Part 6.4 AG-021 | None (already covered) | — |
| F15-102 | Implementation acceptance and verification (duplicated in final decision controls) | Acceptance procedure 'Sensitive data exclusions': Patient or school-minor fixture never enters acquisition workflow | Covered | DEC-030; AU-004; Part 6.4 | None (already covered) | — |
| F15-103 | Implementation acceptance and verification (duplicated in final decision controls) | Acceptance procedure 'Authorization-safe cache and numeric validation': Private cache key includes product, tenant, startup, principal/grant fingerprint, permission/policy/model/knowledge revision, normalized query; reject nonfinite/negative/out-of-range | Not covered | — | Test added | FR-ENH-F-008, FR-ENH-F-009; TC-ENH-F-001, TC-ENH-F-002, TC-ENH-F-003 |
| F15-104 | Implementation acceptance and verification (duplicated in final decision controls) | Acceptance procedure 'Provider and evidence benchmark': Matched samples by geography/purpose; precision, recall, verified contacts, p95, full cost, entitlement, conversion | Not covered | — | Test added | AU-045; TC-ENH-F-015 |
| F15-105 | Current multi-startup scope | 147 interfaces; 19 proposed HTTP operations; 6 candidate entities | Not applicable | Groups A-E reconciliation | Common core: see document 01/02 coverage | — |
| F15-106 | Current multi-startup scope | AI engineering release condition: rule-first, validated structured output, provenance, scoped retrieval, model budget | Covered | Part 7.3; Part 8.2 §8.2.4 | None (already covered) | — |

**Document 16**

| Aspect | Section | Aspect summary | Status | Blueprint location | Action | New IDs |
|---|---|---|---|---|---|---|
| F16-001 | Product purpose | Purpose, startups, technology principles (repeat) | Not applicable | Doc 15 F15-001..003 | Common core: see document 01/02 coverage | — |
| F16-002 | Integration selection and procurement gates | Open-source-first; separate development assistance from production API access; free licence != free usage | Covered | BRD §10; Part 7.3 §7.5.2 | None (already covered) | — |
| F16-003 | Integration selection and procurement gates | Before activation verify licence, entitlement, commercial use, rate, quota, region, data processing/deletion, security, support, failure handling, benchmark | Partially covered | Part 3.2 §3.2.4.2 (quotas to verify); no gate record | Procurement gate PG-01..PG-10 | AU-044; FR-ENH-F-012; GAP-402 |
| F16-004 | Integration selection and procurement gates | Record provider account, approved spending, fallback and expiry; no vendor blanket data access | Not covered | — | integration_candidate + provider_entitlement entities | FR-ENH-F-011 |
| F16-010 | Preferred implementation table | React/Django/PostgreSQL self-hosted; licence and dependency scan | Covered | Part 3.1; Part 4.3 SBOM | None (already covered) | — |
| F16-011 | Preferred implementation table | Celery, Beat, Valkey; shared code, separate queues | Covered | ADR-071; Part 3.1 | None (already covered) | — |
| F16-012 | Preferred implementation table | Search/extraction: approved public search API, self-hosted extraction; benchmark coverage and unit cost | Conflict | AD-05, AD-07; CONFLICT-401/402 | Resolution in §7.4.6 | CONFLICT-401; CONFLICT-402 |
| F16-013 | Preferred implementation table | Contact verification: official channels; Apollo pilot if eligible | Covered | AD-19 (OFF); AU-018 | None (already covered) | — |
| F16-014 | Preferred implementation table | Email/calendar/messaging: official account-bound APIs | Covered | AD-01..AD-04 | None (already covered) | — |
| F16-015 | Preferred implementation table | AI/embeddings: scoped gateway, structured outputs, token/budget caps | Covered | ADR-070, ADR-072, ADR-083 | None (already covered) | — |
| F16-016 | Preferred implementation table | Observability/backup: open-source where practical | Covered | DEC-041; ADR-078 | None (already covered) | — |
| F16-017 | Preferred implementation table | Signing/payment: approved provider; independent accounts; verify evidence | Covered | DEC-022, DEC-023; AD-10, AD-11 | None (already covered) | — |
| F16-020 | Individual candidate register | 538 candidate records with 15 fields each (category, priority, decision, application, modules, interface, trigger, acceptance, procurement, licence, free tier, paid API, allocation, URL, verification) | Partially covered | Part 3.2 AD-01..AD-20 (20 adapters only) | All 538 parsed; register entity specified | F_integration_candidates.csv; IC-001..IC-538; FR-ENH-F-011 |
| F16-021 | Individual candidate register | Source priority codes P0-P3, R, V, X undefined | Not covered | — | Interpretation stated | ASSUMPTION-401; GAP-400 |
| F16-022 | Individual candidate register | All 538 triggers = development environment (Claude Code, Cowork); developer plugins are not runtime entitlements | Covered | Part 7.3 §7.5.2; AG-033..AG-036 | None (already covered) | — |
| F16-030 | Source operating budget register | B01: AWS shared hosting ₹5,000 | Covered | DEC-020 B01; Part 8.2 (revised 5,000-7,000) | Reconciled (§7.4.4.4) | — |
| F16-031 | Source operating budget register | B02: Production AI inference ₹3,000 | Covered | DEC-008; DEC-020 B02 | Reconciled (§7.4.4.4) | — |
| F16-032 | Source operating budget register | B03: Public search API ₹1,500 (500 fetches; Tavily 1,000 free credits) | Covered | DEC-020 B03; AD-05 | Reconciled (§7.4.4.4) | — |
| F16-033 | Source operating budget register | B04: Extraction compute/overage ₹1,000 | Covered | DEC-020 B04 | Reconciled (§7.4.4.4) | — |
| F16-034 | Source operating budget register | B05: Email delivery ₹500 (2,000 sends) | Covered | DEC-020 B05; DEC-025 | Reconciled (§7.4.4.4) | — |
| F16-035 | Source operating budget register | B06: WhatsApp Business ₹2,000 (1,000 templates) | Covered | DEC-020 B06 | Reconciled (§7.4.4.4) | — |
| F16-036 | Source operating budget register | B07: Monitoring/security/CI ₹500 (reduced from ₹1,000) | Covered | DEC-020 B07 | Reconciled (§7.4.4.4) | — |
| F16-037 | Source operating budget register | B08: Apollo paid enrichment reserve ₹9,000 (not a quote) | Covered | DEC-020 B08 (OFF) | Reconciled (§7.4.4.4) | — |
| F16-038 | Source operating budget register | B09: Claude Code developer seats ₹3,600 (2 x $20 x ₹90) | Covered | DEC-020 B09 | Reconciled (§7.4.4.4) | — |
| F16-039 | Source operating budget register | B10: Optional integration reserve ₹1,000 | Covered | DEC-020 B10 | Reconciled (§7.4.4.4) | — |
| F16-040 | Source operating budget register | B11: Contingency 15% | Covered | DEC-020 B11 | Reconciled (§7.4.4.4) | — |
| F16-041 | Source operating budget register | SUM: Base runtime before contingency ₹14,500 = B01..B07 + B10 | Covered | Part 8.2 §8.2.7.2 (BRD figure) | Reconciled (§7.4.4.4) | — |
| F16-042 | Source operating budget register | SUM: Base runtime incl. contingency ₹16,675 | Conflict | Part 8.2 revised 19,665-22,885 | Reconciled in §7.4.4.4 / §7.4.5.10 | CONFLICT-412 |
| F16-043 | Source operating budget register | SUM: Base monthly incl. developer seats ₹20,815 | Not covered | — | Reconciled in §7.4.4.4 / §7.4.5.10 | Budget view table (§7.4.5.10) |
| F16-044 | Source operating budget register | SUM: Paid Apollo runtime incl. contingency ₹27,025 | Not covered | — | Reconciled in §7.4.4.4 / §7.4.5.10 | Budget view table |
| F16-045 | Source operating budget register | SUM: Paid Apollo + seats ₹31,165 | Covered | Part 8.2 (BRD 31,165; revised 34,155-37,375) | Reconciled (§7.4.4.4) | — |
| F16-046 | Source operating budget register | SUM: Base annual incl. seats ₹249,780 | Not covered | — | Reconciled in §7.4.4.4 / §7.4.5.10 | Budget view table; GAP-409 |
| F16-047 | Source operating budget register | SUM: Paid Apollo annual incl. seats ₹373,980 | Not covered | — | Reconciled in §7.4.4.4 / §7.4.5.10 | Budget view table |
| F16-048 | Source operating budget register | SUM: Base annual runtime only ₹200,100 | Not covered | — | Reconciled in §7.4.4.4 / §7.4.5.10 | Budget view table |
| F16-049 | Source operating budget register | SUM: Paid Apollo annual runtime only ₹324,300 | Not covered | — | Reconciled in §7.4.4.4 / §7.4.5.10 | Budget view table |
| F16-050 | Source operating budget register | SUM: Three-month base operating budget ₹62,445 | Not covered | — | Reconciled in §7.4.4.4 / §7.4.5.10 | Budget view table |
| F16-051 | Source operating budget register | SUM: Three-month paid Apollo budget ₹93,495 | Not covered | — | Reconciled in §7.4.4.4 / §7.4.5.10 | Budget view table |
| F16-052 | Consolidated effort | Effort packages 194-323 / 35-60 / 30-52 / 28-48 = 287-483 pd; ₹13.05-32.93 lakh; ₹1-1.5 lakh/resource-month, 22 days | Covered | Part 0; Part 8.2 §8.2.7.1; DEC-012 | None (already covered) | — |
| F16-053 | Consolidated effort | SaaS: plans, metered base + included usage + approved overage; append-only credits; suspension on entitlement expiry; export | Covered | DEC-047; AU-042 | None (already covered) | — |
| F16-054 | Consolidated effort | Margin = recognized service fee minus attributable provider and infrastructure cost | Not covered | NFR-035 (attributable cost stated, no calculation) | Contribution margin automation | AU-049; FR-ENH-F-020; GAP-411 |
| F16-055 | Consolidated effort | Third-party managed service activity and success fees require contractual and regulatory review | Not covered | — | Disabled-until-reviewed rule | FR-ENH-F-029 |
| F16-056 | Website-specific integration and cost controls | CDN, domain/TLS, CAPTCHA, email verification costs; budget per tenant/startup AND surface; separate public/portal from staff consumption; per-IP and per-tenant ceilings for public AI/chat/intake; no browser vendor secrets | Partially covered | NFR-022 (per-IP); B21; Part 3.2 RL classes (no per-surface budget) | Per-surface budget scopes | FR-ENH-F-021; RECOMMENDATION-414 |
| F16-057 | Paid-plugin substitution rule | Inventory is not a shopping list; paid wrappers disabled by default; no stacking competing plans; developer subscription != production API | Partially covered | BRD §10; DEC-020 (B08 OFF) | Rules PG-01..PG-10 | FR-ENH-F-012, FR-ENH-F-013 |
| F16-058 | Paid-plugin substitution rule | Approve paid service only after: function identified, compliant alternatives and measured gap, terms verified, sandbox benchmark, incremental cost and rollback, budget approval, metering and periodic re-evaluation | Not covered | — | Procurement gate state machine | AU-044; FR-ENH-F-015 |
| F16-059 | Provider procurement and operating economics | Inventory licences, entitlements, free quota, unit price, retention, DP terms; reserve atomically; reconcile usage and charge ledger; review monthly | Partially covered | IP-06 reservation; AU-012 attribution (no invoice reconciliation) | Invoice reconciliation | AU-048; FR-ENH-F-019; GAP-410 |
| F16-060 | Integration procurement and runtime control | Inventory: Retain every candidate; dev-only vs runtime; direct API vs wrapper | Partially covered | — | Enhanced | FR-ENH-F-011 |
| F16-061 | Integration procurement and runtime control | Licence: Verify licence version and commercial/network/SaaS obligations with legal | Partially covered | RSK-303 (Firecrawl only) | Enhanced | AU-047 |
| F16-062 | Integration procurement and runtime control | Rate and quota: Check entitlements, free quota, rates, taxes, regional terms before purchase | Partially covered | ASSUMPTION-108 (verify) | Enhanced | PG-04 |
| F16-063 | Integration procurement and runtime control | Adapter design: Canonical request/result, error classes, timeout, rate limit, scoped credentials; mock + sandbox | Covered | IP-01; Part 3.2 §3.2.4.3, §3.2.7 | None (already covered) | — |
| F16-064 | Integration procurement and runtime control | Budget: Reserve max cost; reconcile; release; stop paid fallback unless enabled | Covered | IP-06; AU-002 | None (already covered) | — |
| F16-065 | Integration procurement and runtime control | TCO benchmark: Same workload: coverage, accuracy, latency, failures, hosting/maintenance | Not covered | — | Enhanced | AU-045; FR-ENH-F-016 |
| F16-066 | Integration procurement and runtime control | 538 decision records retain source terms; benchmark columns pending, not measured | Covered | F_integration_candidates.csv (activation default disabled) | None (already covered) | — |
| F16-067 | Provider procurement and benchmark approval | Compare: Same fixture and volume across native and paid comparator | Not covered | — | Enhanced | AU-045 |
| F16-068 | Provider procurement and benchmark approval | Licence: Runtime entitlement, OSS licence, model-weight rights, SaaS use, retention, export | Not covered | — | Enhanced | AU-047 |
| F16-069 | Provider procurement and benchmark approval | TCO: Hosting + metered + engineering/maintenance + licences + support; cost per verified usable outcome | Not covered | — | Enhanced | FR-ENH-F-018 |
| F16-070 | Provider procurement and benchmark approval | Fallback: Disabled by default; approve per tenant, startup, channel, purpose, hard cap; audit paid invocation | Partially covered | Part 7.3 §7.3.6 (Tier 2 opt-in only) | Enhanced | FR-ENH-F-013 |
| F16-071 | Provider procurement and benchmark approval | Synthetic benchmark: Five local synthetic sources only; paid comparisons unverified | Covered | GAP-142 note | None (already covered) | — |
| F16-072 | Optimization engineering | OPT-03-02: Model and token costs: rules first, smaller models, minimal context, bounded tokens; INR/task | Covered | Part 7.3 §7.4.2 | None (already covered) | — |
| F16-073 | Optimization engineering | OPT-03-03: Research/contact cost per qualified verified opportunity improves without regression | Partially covered | KPI-21 AI cost/task only | Enhanced / resolved | FR-ENH-F-018 (verified outcome cost) |
| F16-074 | Optimization engineering | OPT-03-04: Cloud/worker right-sizing; cost/1000 tasks and queue age | Covered | Part 4.3 FinOps (§4.46) | None (already covered) | — |
| F16-075 | Optimization engineering | OPT-03-05: Storage/retention cost; GB-month; legal hold | Covered | Part 4.3; DEC-028 | None (already covered) | — |
| F16-076 | Optimization engineering | OPT-03-06: Communication/subscription costs; review unused seats and API entitlements | Partially covered | AU-024 (suppression); no seat review | Enhanced / resolved | AU-044 monthly entitlement review |
| F16-077 | Optimization engineering | OPT-03-07: Atomic budget reservation across tenant/startup/action; parallel test | Covered | IP-06; AU-002; ADR-083 | None (already covered) | — |
| F16-078 | Optimization engineering | OPT-03-08: Alerts at 70%/90% (proposed); pause optional jobs at cap | Conflict | ADR-083 80%/100%; ladder 80-100% | Enhanced / resolved | CONFLICT-403; FR-ENH-F-022 |
| F16-079 | Optimization engineering | OPT-09-01: Typed contracts 100% before activation | Covered | Part 3.2 §3.2.5 | None (already covered) | — |
| F16-080 | Optimization engineering | OPT-09-02: Consolidation and batching; minimal serializers | Covered | Part 3.2 §3.2.1 | None (already covered) | — |
| F16-081 | Optimization engineering | OPT-09-03: Adapter reliability: timeouts, rate limits, breakers, entitlement fallback | Covered | Part 3.2 §3.2.7 | None (already covered) | — |
| F16-082 | Optimization engineering | OPT-09-04: Webhook: signature, replay window, dedupe; p95 ACK <= 2 s | Covered | IP-03; Part 3.2 §3.2.6 | None (already covered) | — |
| F16-083 | Optimization engineering | OPT-09-05: Meter by provider, operation, tenant/startup; no unapproved paid calls | Covered | AU-012; IP-06 | None (already covered) | — |
| F16-084 | Optimization engineering | OPT-20-01: Unit economics: contribution margin per tenant | Not covered | — | Enhanced / resolved | AU-049 |
| F16-085 | Optimization engineering | OPT-20-02: Entitlements and usage: 100% attributable usage reconciled | Partially covered | AU-042 (metering) | Enhanced / resolved | AU-048 |
| F16-086 | Optimization engineering | OPT-20-03: Support and renewal: onboarding effort, tickets, churn by cohort | Covered | Part 8.2 §8.2.6; AG-031 | None (already covered) | — |
| F16-087 | Optimization engineering | OPT-20-04: Client scalability/portability: self-service onboarding; export and revoke on offboard | Covered | B-SVC; W31-W34 | None (already covered) | — |
| F16-088 | Implementation acceptance and verification | Acceptance procedure 'Hierarchical budget controls': Concurrent reservation at platform/tenant/startup/workflow; duplicate and insufficient balance | Covered | AU-002; Part 6 budget TCs | None (already covered) | — |
| F16-089 | Implementation acceptance and verification | Acceptance procedure 'AI routing cost': Duplicate of F15-093 | Not applicable | See F15-093 | — | — |
| F16-090 | Implementation acceptance and verification | Acceptance procedure 'Open-source replacement economics': Native vs paid on same corpus incl. CPU, labour, API | Not covered | — | Test added | TC-ENH-F-016 |
| F16-091 | Implementation acceptance and verification | Acceptance procedure 'Cost metering and anomaly response': Duplicates, missing attribution, exhausted quota; hard limit halts | Partially covered | AU-012 (anomaly); duplicate usage billing not tested | Test added | TC-ENH-F-017 |
| F16-092 | Implementation acceptance and verification | Acceptance procedure 'HTTP vs adapter classification': All HTTP and adapter operations represented exactly once | Not applicable | Group C (doc 07) reconciliation | — | — |
| F16-093 | Implementation acceptance and verification | Acceptance procedure 'Webhook and provider reliability': Valid/invalid signatures, stale timestamp, duplicate, quota | Covered | Part 3.2 §3.2.6; Part 6 | None (already covered) | — |
| F16-094 | Implementation acceptance and verification | Acceptance procedure 'Provider entitlement and schema change': Official rights, schema version, quota, timeout, compatibility test; no activation without | Not covered | — | Test added | AU-044; TC-ENH-F-018 |
| F16-095 | Implementation acceptance and verification | Acceptance procedure 'Source inventory completeness': Preserved 15-sheet commercial source inventory; coverage measured | Not applicable | Group B (doc 11) reconciliation | — | — |
| F16-096 | Implementation acceptance and verification | Acceptance procedure 'Usage ledger and invoice reconciliation': Replay usage and payment; approved adjustment; no double bill | Partially covered | AU-042 | Test added | AU-048; TC-ENH-F-019 |
| F16-097 | Implementation acceptance and verification | Acceptance procedure 'Service profitability and TCO': Contribution margin by tenant; allocation basis; zero denominator not assessed | Not covered | — | Test added | AU-049; TC-ENH-F-020 |
| F16-098 | Implementation acceptance and verification | Acceptance procedure 'Matched-sample discovery benchmark execution': Unique opaque IDs; micro P/R; nearest-rank p95; reject invalid inputs | Not covered | — | Test added | AU-045; TC-ENH-F-015 |
| F16-099 | Current scope: integration and cost | Connect only entitled providers; capability grants, revocation, health; budgets per tenant/startup/objective/run; reserve before charge | Covered | AD-08 capability grant; AU-010; AU-002; envelope budget_remaining_inr | None (already covered) | — |

**Document 21**

| Aspect | Section | Aspect summary | Status | Blueprint location | Action | New IDs |
|---|---|---|---|---|---|---|
| F21-001 | 1. Purpose, scope | Own automation; OSS/existing first; paid plugin not a dependency because it is in a dev inventory | Covered | BRD §10; ADR-071 | None (already covered) | — |
| F21-002 | 1. Purpose, scope | Distinguish developer assistance, OSS library, self-hosted app, hosted API, licensed/regulated service | Not covered | — | candidate_type enum | FR-ENH-F-011 |
| F21-003 | 1. Purpose, scope | Decision classes Replace / Retain OSS / Conditional external service / Defer-exclude with default actions | Not covered | — | decision_class enum and default action | FR-ENH-F-011 |
| F21-004 | 1. Purpose, scope | Commercial use only; no investor discovery or capital ledger | Not applicable | DEC-002 | Common core: see document 01/02 coverage | — |
| F21-005 | 2. Deployment architecture | Website -> APIs -> domain services -> outbox -> Celery -> adapter registry -> provider; Admin owns config, simulation, approvals, usage, provider health | Covered | Part 3.1; IP-01, IP-02 | None (already covered) | — |
| F21-006 | 2. Deployment architecture | Valkey is broker/cache, not authoritative financial storage | Covered | Part 3.1 (PostgreSQL system of record) | None (already covered) | — |
| F21-007 | 2. Deployment architecture | Layer/runtime/cost table (frontend, backend, durability, jobs, search, AI, external) | Covered | Part 3.1; Part 7.3 §7.5.1 | None (already covered) | — |
| F21-010 | 3. Capability replacement register | 01 Workflow orchestration and RPA | Covered | ADR-071; DEC-051; A033 editor | None (already covered) | — |
| F21-011 | 3. Capability replacement register | 02 Public market / investor search | Conflict | AD-05 Tavily primary | Enhancement / resolution | CONFLICT-401; CONFLICT-406 |
| F21-012 | 3. Capability replacement register | 03 Website extraction | Conflict | ADR-018 Firecrawl self-hosted primary | Enhancement / resolution | CONFLICT-402 |
| F21-013 | 3. Capability replacement register | 04 Professional contact discovery (no guessed addresses; MX != mailbox proof) | Partially covered | AU-018; AD-19 OFF (MX rule not explicit) | Enhancement / resolution | FR-ENH-F-023 |
| F21-014 | 3. Capability replacement register | 05 CRM / relationship pipeline | Covered | M21-M23; AU-020, AU-021 | None (already covered) | — |
| F21-015 | 3. Capability replacement register | 06 LLM / agent framework (local model gateway first) | Conflict | DEC-007 | Enhancement / resolution | CONFLICT-400 |
| F21-016 | 3. Capability replacement register | 07 Embeddings, knowledge, enterprise search (remove revoked content) | Partially covered | ADR-077; AU-001 | Enhancement / resolution | AU-046 |
| F21-017 | 3. Capability replacement register | 08 Email automation and inbox | Covered | DEC-025 SES; AD-01 | None (already covered) | — |
| F21-018 | 3. Capability replacement register | 09 WhatsApp, SMS, social messaging (no unofficial bots) | Covered | AD-02; DEC-026 | None (already covered) | — |
| F21-019 | 3. Capability replacement register | 10 Meeting scheduling and video (Jitsi; local transcription with notice) | Partially covered | AU-023; GAP-143 | Enhancement / resolution | AG-037; RECOMMENDATION-412 |
| F21-020 | 3. Capability replacement register | 11 Document generation / secure storage | Covered | AU-036; S3; AD-20 | None (already covered) | — |
| F21-021 | 3. Capability replacement register | 12 Electronic signing and identity verification (Documenso after review) | Partially covered | DEC-023; AD-10 (Documenso not on shortlist) | Enhancement / resolution | RECOMMENDATION-405 (shortlist note) |
| F21-022 | 3. Capability replacement register | 13 Banking, receipts and billing | Covered | DEC-022; AD-11; AU-037 | None (already covered) | — |
| F21-023 | 3. Capability replacement register | 14 Observability (avoid hosted Sentry/Datadog) | Conflict | DEC-041 Sentry free tier | Enhancement / resolution | CONFLICT-409 |
| F21-024 | 3. Capability replacement register | 15 Cloud infrastructure and storage | Covered | DEC-040; Part 4.3 IaC | None (already covered) | — |
| F21-025 | 3. Capability replacement register | 16 Developer tools, QA, coordination | Covered | Part 7.3 §7.5.2; Part 4.3 | None (already covered) | — |
| F21-026 | 3. Capability replacement register | 17 Analytics, reporting, forecasting | Covered | RP-01..30; AU-041 | None (already covered) | — |
| F21-027 | 3. Capability replacement register | 18 Customer support / collaboration | Covered | AG-031; NT | None (already covered) | — |
| F21-028 | 3. Capability replacement register | 19 Marketing content and localization | Covered | AG-018; AG-012 | None (already covered) | — |
| F21-029 | 3. Capability replacement register | 20 SEO and AI search visibility | Covered | AU-033; AD-17 | None (already covered) | — |
| F21-030 | 3. Capability replacement register | 21 Social listening and publishing (Postiz self-host after AGPL review) | Covered | AD-08; AU-029 | None (already covered) | — |
| F21-031 | 3. Capability replacement register | 22 Marketing campaigns and attribution (Matomo optional) | Covered | AU-040; Part 3.1 alternatives | None (already covered) | — |
| F21-032 | 3. Capability replacement register | 23 Advertising and paid acquisition | Covered | AD-09; AU-032; B12 | None (already covered) | — |
| F21-033 | 3. Capability replacement register | 24 Website and landing page builder | Covered | B-WEB; A107, A108 | None (already covered) | — |
| F21-034 | 3. Capability replacement register | 25 Project/tender discovery (amendments update evidence) | Partially covered | DEC-053; AU-034 (amendments not detected) | Enhancement / resolution | AU-052 |
| F21-035 | 3. Capability replacement register | 26 Supplier, order, procurement, retention | Covered | WF-10; AU-035, AU-038 | None (already covered) | — |
| F21-036 | 3. Capability replacement register | 27 Webinar and demo registration (capacity, dedupe, opt-out) | Partially covered | AD-18; M40 (no automation) | Enhancement / resolution | AU-051 |
| F21-037 | 4. Adapter selection, activation and rollback | Adapter lifecycle stage 'Configure' | Covered | A008; IP-01 registry | None (already covered) | — |
| F21-038 | 4. Adapter selection, activation and rollback | Adapter lifecycle stage 'Simulate' | Covered | IP-08; BRL-AUT-04 | None (already covered) | — |
| F21-039 | 4. Adapter selection, activation and rollback | Adapter lifecycle stage 'Benchmark' | Not covered | — | Lifecycle state machine | AU-045; FR-ENH-F-015 |
| F21-040 | 4. Adapter selection, activation and rollback | Adapter lifecycle stage 'Approve' | Partially covered | CFG-25 (Tier 2 only) | Lifecycle state machine | AU-044; FR-ENH-F-015 |
| F21-041 | 4. Adapter selection, activation and rollback | Adapter lifecycle stage 'Execute' | Covered | IP-02; PDP | None (already covered) | — |
| F21-042 | 4. Adapter selection, activation and rollback | Adapter lifecycle stage 'Recover' | Covered | IP-04; AU-026 | None (already covered) | — |
| F21-043 | 4. Adapter selection, activation and rollback | Adapter lifecycle stage 'Retire' | Not covered | — | Lifecycle state machine | AU-050; GAP-404 |
| F21-044 | 5. Engineering contract | Adapter interface estimate/execute/reconcile/health; context; error classes denied, invalid, quota, retryable, permanent, uncertain | Partially covered | IP-01 AdapterResult; failure classes transient/rate_limited/auth/permanent/uncertain/unsupported | Port contract and class mapping | FR-ENH-F-014; RECOMMENDATION-405 |
| F21-045 | 5. Engineering contract | Pinned deps, SBOM, source and model licences approved separately, isolated containers, egress allowlist, rotation; AGPL network-use review | Partially covered | Part 4.3 SBOM; RSK-303 | Licence register gate | AU-047 |
| F21-046 | 5. Deployment checklist | Control: No paid plugin by default | Covered | BRD §10; DEC-020 | None (already covered) | — |
| F21-047 | 5. Deployment checklist | Control: Quality equivalence (labelled fixture; uncovered data reported) | Not covered | — | Enhanced | AU-045 / AU-047 |
| F21-048 | 5. Deployment checklist | Control: Scope (cross-product and foreign tenant denied) | Covered | NFR-032 | None (already covered) | — |
| F21-049 | 5. Deployment checklist | Control: Recovery (429/timeout/unknown; no duplicate) | Covered | IP-04 | None (already covered) | — |
| F21-050 | 5. Deployment checklist | Control: Licence (dependency and model-weight register) | Not covered | — | Enhanced | AU-045 / AU-047 |
| F21-051 | 5. Deployment checklist | Control: Metering separated from investment or sales cash | Covered | DEC-008; ledgers | None (already covered) | — |
| F21-052 | 5. Deployment checklist | Control: Rollback (previous adapter only after policy/budget checks) | Partially covered | — | Enhanced | FR-ENH-F-015 |
| F21-053 | 6. Cost model | Cost per successful verified outcome; monthly total = infra + inference + data + comms + regulated fees + monitoring/storage + support + contingency | Partially covered | Part 7.3 §7.5.5 (AI layer only) | Full TCO formula | FR-ENH-F-018 |
| F21-054 | 6. Cost model | Break-even example ₹9,000 vs ₹2,000 + ₹3,000 = ₹4,000/month; ₹40,000 effort -> 10 months | Not covered | — | Worked example verified | §7.4.5.9 |
| F21-055 | 6. Cost model | Retained pilot envelope ₹16,675; Apollo ₹9,000 and seats ₹3,600 optional | Conflict | Part 8.2 revised | CONFLICT-412 | — |
| F21-056 | 6. Cost model metrics | Metric: Avoidable subscription | Not covered | — | Metric defined | FR-ENH-F-018; RECOMMENDATION-406 |
| F21-057 | 6. Cost model metrics | Metric: Incremental replacement cost | Not covered | — | Metric defined | FR-ENH-F-018; RECOMMENDATION-406 |
| F21-058 | 6. Cost model metrics | Metric: Net saving | Not covered | — | Metric defined | FR-ENH-F-018; RECOMMENDATION-406 |
| F21-059 | 6. Cost model metrics | Metric: Break-even | Not covered | — | Metric defined | FR-ENH-F-018; RECOMMENDATION-406 |
| F21-060 | 6. Cost model metrics | Metric: Verified outcome cost (zero outcomes undefined) | Not covered | — | Metric defined | FR-ENH-F-018; RECOMMENDATION-406 |
| F21-061 | 6. Cost model metrics | Metric: Approval (switch only when quality, compliance, latency, TCO pass) | Not covered | — | Metric defined | FR-ENH-F-018; RECOMMENDATION-406 |
| F21-062 | 7. Named integration decisions | 97 named candidates with decisions (53 primary + selected supporting) | Covered | F_integration_candidates.csv; §7.4.4.2 | Every row reconciled | — |
| F21-063 | 7. Named integration decisions | 'Apollo GraphQL' mapped to professional contact discovery | Conflict | — | Reclassify | CONFLICT-407 |
| F21-064 | 8. Supporting inventory | 441 supporting candidates in 26 categories; default Defer | Covered | F_integration_candidates.csv | None (already covered) | — |
| F21-065 | 9. Upstream references | Celery BSD, Valkey BSD-3, Scrapy BSD-3, Playwright Apache-2.0, scrapy-playwright, SearXNG AGPL, Matomo, WhatsApp pricing, Meta rate limits | Partially covered | Part 3.1 tech table (partial) | Seed licence register | AU-047 |
| F21-066 | 9. Final procurement gate | No substitution may remove a legally necessary verification, delivery, signature or payment service | Covered | DEC-022, DEC-023; PG-09 | None (already covered) | — |
| F21-067 | Replacement benchmark | Benchmark dimension: Licence and data rights | Not covered | — | Benchmark harness | AU-045 |
| F21-068 | Replacement benchmark | Benchmark dimension: Functional parity | Not covered | — | Benchmark harness | AU-045 |
| F21-069 | Replacement benchmark | Benchmark dimension: Accuracy / coverage | Not covered | — | Benchmark harness | AU-045 |
| F21-070 | Replacement benchmark | Benchmark dimension: Reliability / latency | Not covered | — | Benchmark harness | AU-045 |
| F21-071 | Replacement benchmark | Benchmark dimension: Total cost | Not covered | — | Benchmark harness | AU-045 |
| F21-072 | Replacement benchmark | Benchmark dimension: Fallback (paid disabled, outage, quota) | Covered | Part 7.3 §7.3.4 | None (already covered) | — |
| F21-073 | Replacement benchmark | Per-candidate benchmark scope; activation 'Disabled pending evidence' (35 rows) | Covered | F_integration_candidates.csv activation_default | None (already covered) | — |
| F21-074 | Benchmark method | Sample workload stratified by country/category/difficulty; success metrics; financial control | Not covered | — | — | AU-045 |
| F21-075 | Benchmark method | Local benchmark: guarded extraction 5 synthetic docs, 0 forbidden; unguarded baseline 2 false positives | Covered | Informational; no claim (GAP-142) | None (already covered) | — |
| F21-076 | Benchmark method | Benchmark plans for 28 categories (538 candidates), all pending | Covered | §7.4.4.2 category table | None (already covered) | — |
| F21-077 | Optimization (repeat) | OPT-03-01..08, OPT-09-01, OPT-10-01..06 repeated | Not applicable | See F15/F16 rows | Duplicate | — |
| F21-078 | Implementation acceptance | Open-source replacement economics (repeat of F16) | Not applicable | F16-090 | — | — |
| F21-079 | Implementation acceptance | Provider entitlement and schema change (repeat) | Not applicable | F16-094 | — | — |
| F21-080 | Implementation acceptance | Shared workflow and adapter code: reusable code without shared credentials or data; no duplicate side effects | Covered | Part 3.1 (independent deployment; shared libraries) | None (already covered) | — |
| F21-081 | Current scope | Provider replacement: native workflow code cannot replace official provider authorization | Covered | AD-02, AD-08 capability grants | None (already covered) | — |

**Document 38 (§09 automation library)**

| Aspect | Section | Aspect summary | Status | Blueprint location | Action | New IDs |
|---|---|---|---|---|---|---|
| F38-001 | 09 Automation library | 20 industry/business templates (names not given in pack) | Partially covered | CFG-04 business templates; A100 (no catalogue) | 20 templates proposed | TPL-01..TPL-20; ASSUMPTION-400; GAP-401 |
| F38-002 | 09 Automation library | 20 use-case groups x 5 = 100 use cases (group names only) | Partially covered | AG-001..036, AU-001..043 cover 89 of 100 | 100 use cases mapped; 11 gaps filled | AL-01.1..AL-20.5; AG-037, AG-038; AU-044..AU-052 |
| F38-003 | 09 Automation library | 13 workflow node types (names not given) | Partially covered | DEC-051; BRL-AUT-02; API-478 (no list) | 13 canonical node types proposed | NT13-01..NT13-13; ASSUMPTION-400 |
| F38-004 | 09 Automation library | Library is a catalogue of proposed use cases, not 100 live integrations; prototypes are simulations | Covered | BRL-AUT-04; Part 6.1 simulation oracle | None (already covered) | — |

---

## 7.4.4 Catalogue reconciliation

### 7.4.4.1 Prompt contracts (document 15) to the AG/AU catalogue

Document 15 defines 18 logical AI responsibilities. Each is bound below to a **prompt contract ID (PC-01…PC-18)**, the blueprint agents and automations that implement it, and the gap closed in Part 7.4b. All contracts share the source's common instruction (retrieved content is untrusted data; authorized scope only; structured JSON; `unknown` when unsupported; cite evidence IDs; never invent claims or external results; no direct external execution), which the blueprint already enforces through AU-005, ADR-082, BRL-AI-03 and BRL-AI-04 (Part 7.3 §7.6.3, §7.6.5).

| PC | Responsibility (doc 15) | Inputs → outputs (doc 15) | Blueprint implementation | Tier (DEC-007) | Status | Gap closed in 7.4b |
|---|---|---|---|---|---|---|
| PC-01 | Knowledge | Approved claims, documents, offering → approved facts, citations, unknowns | AG-001 (claim candidates), TL-09 `claims.lookup`, AU-029 | 1a | Covered | — |
| PC-02 | Research | Permitted sources, geography → queries, evidence, source IDs, freshness | AG-003 (plans), AG-004 (extraction), AU-007, AU-014 | 0 → 1a | Covered | — |
| PC-03 | Signal | Source records, published context → signal type, evidence, confidence | AG-005 | 1a | Covered | — |
| PC-04 | Matching | Verified evidence, approved scoring policy → score factors, missing evidence, explanation | AU-016 and AU-017 (deterministic), AG-007 (explanation) | 0 + 1a | Partial: `missing_fields` not a common output | Envelope v2 (FR-ENH-F-001) |
| PC-05 | Contact | Organization/person professional source → role, channel, provenance, verification status | AG-008, AU-018 | 1a | Covered | FR-ENH-F-023 tightens "verified" |
| PC-06 | Engagement | Eligible contact, approved facts, channel → draft, claims, source IDs, escalation | AG-011, AG-012, TL-10 | 1b | Covered | — |
| PC-07 | Response | Incoming message, thread → intent, objection, next action, stop flag | AG-013, AG-014, AU-008 | 0 → 1a | Covered | — |
| PC-08 | Objection | Concern, approved evidence → answer draft or specialist escalation | AG-021 | 1b | Covered | — |
| PC-09 | Planner | Objective, scope, budget, state, deadlines → proposed actions, cost, dependencies, approval requirement | AG-016, TL-18 | 1b | Partial: cost and approval requirement not in the common envelope | Envelope v2 |
| PC-10 | Meeting | Authorized transcript or notes → summary, actions, confirmed/unconfirmed distinction | None (GAP-143 excluded meeting summarization) | — | **Not covered** | **AG-037** (notes-based) |
| PC-11 | Forecast | Actual pipeline, evidence → scenario, assumptions, uncertainty | AU-041 (stage-weighted, backtested) + AG-029 narratives | 0 + 1a | Partial: no scenario/assumption output | AG-029 forecast mode (FR-ENH-F-002) |
| PC-12 | Quality | Candidate output, gold case, policy → pass/fail, reason, severity | AG-002, AG-012, AU-006 | 1b batch | Covered | — |
| PC-13 | Cost routing | Token estimate, approved models, caps → selected model, reserve, fallback | AU-001, AU-002 (deterministic) | 0 | **Conflict**: source treats it as an AI task | CONFLICT-411 (keep deterministic) |
| PC-14 | Copilot | Authorized scoped request → read/draft/action proposal, confirmation requirements | AG-015 (DEC-035) | 1a/1b | Covered | — |
| PC-15 | Business need | Organization requirement, source → need and offering match | AG-006, AU-016 | 1a | Covered | — |
| PC-16 | Content and SEO | Approved offering, audience → draft content, claims, review | AG-018, AG-012, AU-033 | 1b | Covered | — |
| PC-17 | Proposal | Approved prices, bid/order requirements → draft quote/proposal, assumptions | AG-020 (no amounts), AU-035 (prices) | 1b | Covered | — |
| PC-18 | Retention | Actual delivery, feedback, contract → renewal opportunity and next action | AU-039, AG-011 renewal mode, AG-026 | 0 + 1a | Partial: no next-best-action output | **AG-038** |

**Required envelope reconciliation.** Document 15 requires 11 fields on every AI result; the blueprint's inter-agent envelope (Part 7.2 §7.2.7) has 15 fields, 5 of which match.

| Doc 15 field | Blueprint envelope field (Part 7.2 §7.2.7) | Status |
|---|---|---|
| tenant_id, startup_id | `tenant_id`, `startup_id` | Covered |
| purpose | — (`intent` is the operation, not the business purpose) | **Missing** |
| schema_revision | `payload_schema` (schema name; no revision) | Partial |
| evidence_ids | `evidence_ids[]`, `citation_ids[]` | Covered |
| confidence | `confidence` | Covered |
| missing_fields | — | **Missing** |
| policy_flags | — (guard results live in the audit record only) | **Missing** |
| proposed_action | — | **Missing** |
| requires_approval | — (implied by autonomy level) | **Missing** |
| cost_estimate | `budget_remaining_inr` (remaining, not estimate) | **Missing** |

Envelope v2 (Part 7.4b §7.4.5.1, FR-ENH-F-001) adds the six missing fields and a schema revision.

### 7.4.4.2 Integration candidates (documents 16 and 21)

**Parse result.** 538 records; 15 of 15 fields present in every record; 538 matched to a document-21 decision (97 named in §7, 441 in the §8 supporting inventory); document 21's benchmark plan lists 28 categories totalling 538, which equals the parsed count.

**By source decision (document 21).**

| Document 21 decision | Candidates | Blueprint treatment |
|---|---|---|
| Defer; no runtime need established | 441 | Disabled; no credentials; capability (if any) delivered natively |
| Replace/defer paid wrapper | 73 | Native Django/Celery capability; wrapper never installed in runtime |
| Replace core; conditional licensed data only | 8 | Official contact paths first (AU-018); licensed enrichment only via AD-19, OFF, B08 |
| Replace workflow; external service conditional | 7 | Native workflow; official provider adapter only when required (e-sign, payments, ads, events, email alternative) |
| Retain open-source candidate if justified | 3 | Playwright, DeepEval, Pydantic AI: pinned, licence-registered (AU-047) |
| Self-host or replace after licence review | 2 | Firecrawl, Postiz: AGPL network-use review before any deployment |
| Replace first; conditional search fallback | 2 | Tavily, Exa: native source adapters first; PAYG search as capped fallback (CONFLICT-401) |
| Defer unless commercial evidence need approved | 2 | Equity Research (out of scope), Bio Research (no clinical data) |

**By licence class and fee class (document 16, verify at implementation, as of 27 Nov 2026).**

| Licence class | Count | | Fee class (paid API field) | Count |
|---|---|---|---|---|
| Unverified (not established) | 435 | | Not verified (no assumed price) | 498 |
| Commercial / hybrid (edition unverified) | 73 | | Developer seat usage (B09/B02) | 17 |
| Developer plugin (licence unverified) | 17 | | Plan/quote required | 15 |
| Proprietary service | 8 | | Published rate (verify) | 4 |
| Open source (permissive) | 3 | | ₹0 licence; hosting extra | 4 |
| Hybrid AGPL self-host / proprietary cloud | 2 | | | |

**By priority [ASSUMPTION-401].** P0 9 · P1 24 · P2 12 · P3 9 · R 22 · X 72 · V 390. The source does not define the codes [GAP-400]; this blueprint reads P0–P3 as adoption priority, R as "retained alternative", X as "excluded / not selected" and V as "verification-only inventory". Only P0/P1 rows carry any budget allocation. Every row's trigger is "Development environment: Claude Code, Cowork", confirming that **none is a runtime entitlement** (Part 7.3 §7.5.2).

**Budget references inside candidate rows.** B02 20 · B09 17 · B10 13 · B07 12 · B01 11 · B03 2 · B04 2 · B05 2 · B06 1 · B08 1. No candidate references B11–B23, so no candidate creates a new budget line. Only seven rows carry a dated source check (24 Nov 2026): Firecrawl, Apollo.io, Hunter, Tavily, Resend, Exa and Zapier; all are restated "verify at implementation (as of 27 Nov 2026)".

**By category.**

| Category (doc 16) | Candidates | Named in doc 21 §7 | Supporting (§8) | P0/P1 | Covered | Not applicable | Conflict | Default capability (doc 21 §8) |
|---|---|---|---|---|---|---|---|---|
| Data and Databases | 66 | 3 | 63 | 0 | 66 | 0 | 0 | Embeddings, knowledge and enterprise search |
| Developer Workflows | 50 | 3 | 47 | 2 | 49 | 0 | 1 | Developer tools, QA and project coordination |
| Observability and Monitoring | 37 | 4 | 33 | 3 | 37 | 0 | 0 | Observability, error tracking, metrics and security |
| Finance and Accounting | 36 | 3 | 33 | 0 | 17 | 19 | 0 | Banking, receipts and billing |
| Marketing and Web | 33 | 33 | 0 | 9 | 33 | 0 | 0 | — |
| AI Development and Agents | 30 | 6 | 24 | 4 | 30 | 0 | 0 | LLM / agent framework |
| Security | 30 | 2 | 28 | 1 | 30 | 0 | 0 | Observability, error tracking, metrics and security |
| Cloud and Infrastructure | 27 | 7 | 20 | 1 | 27 | 0 | 0 | Cloud infrastructure and storage |
| Design and Creative | 24 | 1 | 23 | 1 | 24 | 0 | 0 | Marketing content and localization |
| CRM and Sales | 20 | 20 | 0 | 4 | 18 | 2 | 0 | — |
| Code Quality and Review | 20 | 0 | 20 | 0 | 20 | 0 | 0 | Developer tools, QA and project coordination |
| Healthcare and Life Sciences | 19 | 1 | 18 | 0 | 1 | 18 | 0 | No runtime requirement established |
| Productivity and Documents | 16 | 3 | 13 | 0 | 16 | 0 | 0 | Document generation / secure storage |
| Legal | 16 | 1 | 15 | 0 | 16 | 0 | 0 | Electronic signing and identity verification |
| Platforms and SaaS | 15 | 2 | 13 | 1 | 15 | 0 | 0 | Workflow orchestration and RPA |
| Communication and Messaging | 15 | 3 | 12 | 2 | 15 | 0 | 0 | Email automation and inbox |
| Language Servers | 15 | 0 | 15 | 0 | 15 | 0 | 0 | Developer tools, QA and project coordination |
| Business Operations | 13 | 1 | 12 | 0 | 13 | 0 | 0 | Workflow orchestration and RPA |
| Payments and Billing | 9 | 1 | 8 | 0 | 9 | 0 | 0 | Banking, receipts and billing |
| Human Resources | 8 | 0 | 8 | 0 | 0 | 8 | 0 | No runtime requirement established |
| Documentation | 7 | 0 | 7 | 0 | 7 | 0 | 0 | Document generation / secure storage |
| Project Management | 6 | 2 | 4 | 1 | 6 | 0 | 0 | Developer tools, QA and project coordination |
| Skills Authoring | 6 | 0 | 6 | 3 | 6 | 0 | 0 | Developer tools, QA and project coordination |
| Engineering and Product | 6 | 0 | 6 | 0 | 6 | 0 | 0 | Developer tools, QA and project coordination |
| Education and Learning | 5 | 0 | 5 | 0 | 0 | 5 | 0 | No runtime requirement established |
| Browser Automation | 4 | 1 | 3 | 1 | 4 | 0 | 0 | Website extraction |
| Customer Support | 3 | 0 | 3 | 0 | 3 | 0 | 0 | Customer support / collaboration |
| Output Styles | 2 | 0 | 2 | 0 | 2 | 0 | 0 | Developer tools, QA and project coordination |
| **Total** | **538** | **97** | **441** | **33** | **485** | **52** | **1** | |

**All 97 named candidates (document 21 §7) with document-16 terms and the blueprint mapping.** Rates are the source's historical planning inputs; **verify at time of implementation (as of 27 Nov 2026)** [ASSUMPTION-402].

| IC | Candidate | Pri | Source capability (doc 21) | Doc 21 decision | Licence (doc 16) | Free tier / paid rate (doc 16, verify) | Allocation | Blueprint adapter / module | Blueprint replacement decision | Status |
|---|---|---|---|---|---|---|---|---|---|---|
| IC-001 | Firecrawl | P0 | Website extraction | Self-host or replace after licence review | Hybrid — AGPL-3.0 self-host / proprietary cloud | 1,000 cloud credits/month; self-host capacity only / Cloud Hobby $19/month, 5,000 credits; $16/month annual billing; self-host ₹0 licence | B04 ₹1,000/month reserve; cloud plan needs approval | AD-07 | Retain OSS / self-host | Covered |
| IC-002 | Apollo.io | P1 | Professional contact discovery | Replace core; conditional licensed data only | Proprietary data service | Free plan exists; 900 advertised credits; reset interval and API entitlement confirm in account / Plan + enrichment credits; no universal per-call price; paid API entitlement and quote required | B08 ₹9,000/month conditional reserve, not quote | AD-19 | Conditional external service (B08/B18) | Covered |
| IC-003 | customer-sales-automation | P1 | CRM / relationship pipeline | Replace/defer paid wrapper | Claude skill/plugin; licence unverified; development-first | Claude plan limits; no independent runtime quota assumed / No separate installation fee assumed only after verification; production model/API usage billed separately | B09 developer seats; B02 runtime if applicable | M21–M23 native CRM | Replace (native) | Covered |
| IC-004 | Hunter | P1 | Professional contact discovery | Replace core; conditional licensed data only | Proprietary data service | 50 credits/month; 30 AI Discover searches/month shared across interfaces / Paid data plans/credit bundles; exact API plan cost not verified | B10 shared ₹1,000 optional reserve; alternative to Apollo, not additive | AD-19 | Conditional external service (B08/B18) | Covered |
| IC-005 | Sales | P1 | CRM / relationship pipeline | Replace/defer paid wrapper | Claude skill/plugin; licence unverified; development-first | Claude plan limits; no independent runtime quota assumed / No separate installation fee assumed only after verification; production model/API usage billed separately | B09 developer seats; B02 runtime if applicable | M21–M23 native CRM | Replace (native) | Covered |
| IC-006 | Content Studio | P1 | Marketing content and localization | Replace/defer paid wrapper | Claude skill/plugin; licence unverified; development-first | Claude plan limits; no independent runtime quota assumed / No separate installation fee assumed only after verification; production model/API usage billed separately | B09 developer seats; B02 runtime if applicable | M34 content studio | Replace (native) | Covered |
| IC-007 | content-marketing | P1 | Marketing content and localization | Replace/defer paid wrapper | Claude skill/plugin; licence unverified; development-first | Claude plan limits; no independent runtime quota assumed / No separate installation fee assumed only after verification; production model/API usage billed separately | B09 developer seats; B02 runtime if applicable | M34 content studio | Replace (native) | Covered |
| IC-008 | Marketing | P1 | Marketing content and localization | Replace/defer paid wrapper | Claude skill/plugin; licence unverified; development-first | Claude plan limits; no independent runtime quota assumed / No separate installation fee assumed only after verification; production model/API usage billed separately | B09 developer seats; B02 runtime if applicable | M34 content studio | Replace (native) | Covered |
| IC-009 | Postiz | P1 | Social listening and publishing | Self-host or replace after licence review | Hybrid — AGPL-3.0 self-host / paid hosted | Self-host: no provider execution quota; social APIs separate / ₹0 self-host licence; hosted pricing not verified; social APIs may charge | B01/B10 shared; no hosted subscription approved | AD-08 SocialPort | Conditional external service (B16) | Covered |
| IC-010 | seo-analysis-monitoring | P1 | SEO and AI search visibility | Replace/defer paid wrapper | Claude skill/plugin; licence unverified; development-first | Claude plan limits; no independent runtime quota assumed / No separate installation fee assumed only after verification; production model/API usage billed separately | B09 developer seats; B02 runtime if applicable | AD-17 Search Console | Replace (native) + official API | Covered |
| IC-011 | seo-content-creation | P1 | Marketing content and localization | Replace/defer paid wrapper | Claude skill/plugin; licence unverified; development-first | Claude plan limits; no independent runtime quota assumed / No separate installation fee assumed only after verification; production model/API usage billed separately | B09 developer seats; B02 runtime if applicable | M34 content studio | Replace (native) | Covered |
| IC-012 | seo-technical-optimization | P1 | SEO and AI search visibility | Replace/defer paid wrapper | Claude skill/plugin; licence unverified; development-first | Claude plan limits; no independent runtime quota assumed / No separate installation fee assumed only after verification; production model/API usage billed separately | B09 developer seats; B02 runtime if applicable | AD-17 Search Console | Replace (native) + official API | Covered |
| IC-013 | social-publishing | P1 | Social listening and publishing | Replace/defer paid wrapper | Claude skill/plugin; licence unverified; development-first | Claude plan limits; no independent runtime quota assumed / No separate installation fee assumed only after verification; production model/API usage billed separately | B09 developer seats; B02 runtime if applicable | AD-08 SocialPort | Conditional external service (B16) | Covered |
| IC-014 | Clay | P2 | Professional contact discovery | Replace core; conditional licensed data only | Commercial service / hybrid; exact wrapper and upstream licence unverified | — / not verified | ₹0 committed; use only after approved procurement | AD-19 Apollo/Hunter (EnrichmentPort, OFF) | Conditional external service (B08/B18) | Covered |
| IC-015 | Common Room | P2 | Marketing campaigns and attribution | Replace/defer paid wrapper | Commercial service / hybrid; exact wrapper and upstream licence unverified | — / not verified | ₹0 committed; use only after approved procurement | M39 campaigns; AU-040 | Replace (native) | Covered |
| IC-016 | Crossbeam Skills | P2 | CRM / relationship pipeline | Replace/defer paid wrapper | Commercial service / hybrid; exact wrapper and upstream licence unverified | — / not verified | ₹0 committed; use only after approved procurement | M21–M23 native CRM | Replace (native) | Covered |
| IC-017 | Endgame | P2 | CRM / relationship pipeline | Replace/defer paid wrapper | Commercial service / hybrid; exact wrapper and upstream licence unverified | — / not verified | ₹0 committed; use only after approved procurement | M21–M23 native CRM | Replace (native) | Covered |
| IC-018 | Leadfeeder | P2 | Marketing campaigns and attribution | Replace/defer paid wrapper | Commercial service / hybrid; exact wrapper and upstream licence unverified | — / not verified | ₹0 committed; use only after approved procurement | M39 campaigns; AU-040 | Replace (native) | Covered |
| IC-019 | Adspirer | P2 | Advertising and paid acquisition | Replace/defer paid wrapper | Commercial service / hybrid; exact wrapper and upstream licence unverified | — / not verified | ₹0 committed; use only after approved procurement | AD-09 AdsPort | Conditional external service (B12/B16) | Covered |
| IC-020 | Socialinsider | P2 | Social listening and publishing | Replace/defer paid wrapper | Commercial service / hybrid; exact wrapper and upstream licence unverified | — / not verified | ₹0 committed; use only after approved procurement | AD-08 SocialPort | Conditional external service (B16) | Covered |
| IC-021 | Writesonic | P2 | Marketing content and localization | Replace/defer paid wrapper | Commercial service / hybrid; exact wrapper and upstream licence unverified | — / not verified | ₹0 committed; use only after approved procurement | M34 content studio | Replace (native) | Covered |
| IC-022 | EULER for Partner Managers | P3 | CRM / relationship pipeline | Replace/defer paid wrapper | Commercial service / hybrid; exact wrapper and upstream licence unverified | — / not verified | ₹0 committed; use only after approved procurement | M21–M23 native CRM | Replace (native) | Covered |
| IC-023 | Vibe Prospecting | P3 | Professional contact discovery | Replace core; conditional licensed data only | Commercial service / hybrid; exact wrapper and upstream licence unverified | — / not verified | ₹0 committed; use only after approved procurement | AD-19 Apollo/Hunter (EnrichmentPort, OFF) | Conditional external service (B08/B18) | Covered |
| IC-024 | AppFollow AI Toolkit | P3 | SEO and AI search visibility | Replace/defer paid wrapper | Commercial service / hybrid; exact wrapper and upstream licence unverified | — / not verified | ₹0 committed; use only after approved procurement | AD-17 Search Console | Replace (native) + official API | Covered |
| IC-025 | AppTweak API | P3 | SEO and AI search visibility | Replace/defer paid wrapper | Commercial service / hybrid; exact wrapper and upstream licence unverified | — / not verified | ₹0 committed; use only after approved procurement | AD-17 Search Console | Replace (native) + official API | Covered |
| IC-026 | Pendo Orchestrate | P3 | Marketing campaigns and attribution | Replace/defer paid wrapper | Commercial service / hybrid; exact wrapper and upstream licence unverified | — / not verified | ₹0 committed; use only after approved procurement | M39 campaigns; AU-040 | Replace (native) | Covered |
| IC-027 | Realize | P3 | Advertising and paid acquisition | Replace workflow; external service conditional | Commercial service / hybrid; exact wrapper and upstream licence unverified | — / not verified | ₹0 committed; use only after approved procurement | AD-09 AdsPort | Conditional external service (B12/B16) | Covered |
| IC-028 | Spotify Ads API | P3 | Advertising and paid acquisition | Replace workflow; external service conditional | Commercial service / hybrid; exact wrapper and upstream licence unverified | — / not verified | ₹0 committed; use only after approved procurement | AD-09 AdsPort | Conditional external service (B12/B16) | Covered |
| IC-029 | vidIQ | P3 | SEO and AI search visibility | Replace/defer paid wrapper | Commercial service / hybrid; exact wrapper and upstream licence unverified | — / not verified | ₹0 committed; use only after approved procurement | AD-17 Search Console | Replace (native) + official API | Covered |
| IC-030 | HubSpot Sales | R | CRM / relationship pipeline | Replace/defer paid wrapper | Commercial service / hybrid; exact wrapper and upstream licence unverified | — / not verified | ₹0 committed; use only after approved procurement | M21–M23 native CRM | Replace (native) | Covered |
| IC-031 | Lusha | R | Professional contact discovery | Replace core; conditional licensed data only | Commercial service / hybrid; exact wrapper and upstream licence unverified | — / not verified | ₹0 committed; use only after approved procurement | AD-19 Apollo/Hunter (EnrichmentPort, OFF) | Conditional external service (B08/B18) | Covered |
| IC-032 | monday CRM | R | CRM / relationship pipeline | Replace/defer paid wrapper | Commercial service / hybrid; exact wrapper and upstream licence unverified | — / not verified | ₹0 committed; use only after approved procurement | M21–M23 native CRM | Replace (native) | Covered |
| IC-033 | RocketReach | R | Professional contact discovery | Replace core; conditional licensed data only | Commercial service / hybrid; exact wrapper and upstream licence unverified | — / not verified | ₹0 committed; use only after approved procurement | AD-19 Apollo/Hunter (EnrichmentPort, OFF) | Conditional external service (B08/B18) | Covered |
| IC-034 | Sales Cloud | R | CRM / relationship pipeline | Replace/defer paid wrapper | Commercial service / hybrid; exact wrapper and upstream licence unverified | — / not verified | ₹0 committed; use only after approved procurement | M21–M23 native CRM | Replace (native) | Covered |
| IC-035 | ZoomInfo | R | Professional contact discovery | Replace core; conditional licensed data only | Commercial service / hybrid; exact wrapper and upstream licence unverified | — / not verified | ₹0 committed; use only after approved procurement | AD-19 Apollo/Hunter (EnrichmentPort, OFF) | Conditional external service (B08/B18) | Covered |
| IC-036 | ActiveCampaign | R | Marketing campaigns and attribution | Replace/defer paid wrapper | Commercial service / hybrid; exact wrapper and upstream licence unverified | — / not verified | ₹0 committed; use only after approved procurement | M39 campaigns; AU-040 | Replace (native) | Covered |
| IC-037 | Apify | R | Website extraction | Replace/defer paid wrapper | Commercial service / hybrid; exact wrapper and upstream licence unverified | — / not verified | ₹0 committed; use only after approved procurement | AD-07 Firecrawl self-hosted (ExtractionPort) | Retain OSS / self-host | Covered |
| IC-038 | Botify | R | SEO and AI search visibility | Replace/defer paid wrapper | Commercial service / hybrid; exact wrapper and upstream licence unverified | — / not verified | ₹0 committed; use only after approved procurement | AD-17 Search Console | Replace (native) + official API | Covered |
| IC-039 | Bright Data | R | Website extraction | Replace/defer paid wrapper | Commercial service / hybrid; exact wrapper and upstream licence unverified | — / not verified | ₹0 committed; use only after approved procurement | AD-07 Firecrawl self-hosted (ExtractionPort) | Retain OSS / self-host | Covered |
| IC-040 | Customer.io | R | Marketing campaigns and attribution | Replace/defer paid wrapper | Commercial service / hybrid; exact wrapper and upstream licence unverified | — / not verified | ₹0 committed; use only after approved procurement | M39 campaigns; AU-040 | Replace (native) | Covered |
| IC-041 | Nimble | R | CRM / relationship pipeline | Replace/defer paid wrapper | Commercial service / hybrid; exact wrapper and upstream licence unverified | — / not verified | ₹0 committed; use only after approved procurement | M21–M23 native CRM | Replace (native) | Covered |
| IC-042 | SearchAtlas Toolkit | R | SEO and AI search visibility | Replace/defer paid wrapper | Commercial service / hybrid; exact wrapper and upstream licence unverified | — / not verified | ₹0 committed; use only after approved procurement | AD-17 Search Console | Replace (native) + official API | Covered |
| IC-043 | SearchFit SEO | R | SEO and AI search visibility | Replace/defer paid wrapper | Commercial service / hybrid; exact wrapper and upstream licence unverified | — / not verified | ₹0 committed; use only after approved procurement | AD-17 Search Console | Replace (native) + official API | Covered |
| IC-044 | Supermetrics | R | Marketing campaigns and attribution | Replace/defer paid wrapper | Commercial service / hybrid; exact wrapper and upstream licence unverified | — / not verified | ₹0 committed; use only after approved procurement | M39 campaigns; AU-040 | Replace (native) | Covered |
| IC-045 | Unbounce Landing Page Builder | R | Website and landing page builder | Replace/defer paid wrapper | Commercial service / hybrid; exact wrapper and upstream licence unverified | — / not verified | ₹0 committed; use only after approved procurement | B-WEB publication service (A107, A108) | Replace (native) | Covered |
| IC-046 | Windsor.ai | R | Marketing campaigns and attribution | Replace/defer paid wrapper | Commercial service / hybrid; exact wrapper and upstream licence unverified | — / not verified | ₹0 committed; use only after approved procurement | M39 campaigns; AU-040 | Replace (native) | Covered |
| IC-047 | Zyte Web Data | R | Website extraction | Replace/defer paid wrapper | Commercial service / hybrid; exact wrapper and upstream licence unverified | — / not verified | ₹0 committed; use only after approved procurement | AD-07 Firecrawl self-hosted (ExtractionPort) | Retain OSS / self-host | Covered |
| IC-048 | Carta crm | X | CRM / relationship pipeline | Replace/defer paid wrapper | Commercial service / hybrid; exact wrapper and upstream licence unverified | — / not verified | ₹0 committed; use only after approved procurement | M21–M23 native CRM | Replace (native) | Not applicable |
| IC-049 | GovTribe | X | Project / tender discovery and bid preparation | Replace/defer paid wrapper | Commercial service / hybrid; exact wrapper and upstream licence unverified | — / not verified | ₹0 committed; use only after approved procurement | WF-08 bids; AU-034 (DEC-053) | Replace (native); no auto-submission | Covered |
| IC-050 | Wealthbox | X | CRM / relationship pipeline | Replace/defer paid wrapper | Commercial service / hybrid; exact wrapper and upstream licence unverified | — / not verified | ₹0 committed; use only after approved procurement | M21–M23 native CRM | Replace (native) | Not applicable |
| IC-051 | B12 | X | Website and landing page builder | Replace/defer paid wrapper | Commercial service / hybrid; exact wrapper and upstream licence unverified | — / not verified | ₹0 committed; use only after approved procurement | B-WEB publication service (A107, A108) | Replace (native) | Covered |
| IC-052 | Build with WordPress | X | Website and landing page builder | Replace/defer paid wrapper | Commercial service / hybrid; exact wrapper and upstream licence unverified | — / not verified | ₹0 committed; use only after approved procurement | B-WEB publication service (A107, A108) | Replace (native) | Covered |
| IC-053 | Replo | X | Website and landing page builder | Replace/defer paid wrapper | Commercial service / hybrid; exact wrapper and upstream licence unverified | — / not verified | ₹0 committed; use only after approved procurement | B-WEB publication service (A107, A108) | Replace (native) | Covered |
| IC-054 | Tavily | P0 | Public market / investor search | Replace first; conditional search fallback | Proprietary hosted API | 1,000 API credits/month / PAYG $0.008/credit; advanced operations may consume >1 credit | B03 ₹1,500/month shared reserve | AD-05 | Replace core; investor use excluded (DEC-002 scope) | Covered |
| IC-055 | Playwright | P0 | Website extraction | Retain open-source candidate if justified | Open source — Apache-2.0 | Self-host: no vendor execution quota; compute limits apply / ₹0 software licence; hosting/maintenance and connected API charges extra | B01 shared; no duplicate allocation | Part 6 tooling | Retain OSS / self-host | Covered |
| IC-056 | AWS Core | P0 | Cloud infrastructure and storage | Replace/defer paid wrapper | Proprietary managed cloud | Account/region/service-specific free credits and quotas; no blanket free tier / Metered region/service pricing; calculate from actual storage, requests, secrets, logs and compute | B01 ₹5,000/month; B07 ₹500/month monitoring shared | AWS ap-south-1 (DEC-040) | Retain existing (B01) | Covered |
| IC-057 | Claude Code Setup | P0 | Developer tools, QA and project coordination | Replace/defer paid wrapper | Claude skill/plugin; licence unverified; development-first | Claude plan limits; no independent runtime quota assumed / No separate installation fee assumed only after verification; production model/API usage billed separately | B09 developer seats; B02 runtime if applicable | Delivery tooling (Part 7.3 §7.5.2) | Defer (developer-only) | Covered |
| IC-058 | CLAUDE.md Management | P0 | Developer tools, QA and project coordination | Replace/defer paid wrapper | Claude skill/plugin; licence unverified; development-first | Claude plan limits; no independent runtime quota assumed / No separate installation fee assumed only after verification; production model/API usage billed separately | B09 developer seats; B02 runtime if applicable | Delivery tooling (Part 7.3 §7.5.2) | Defer (developer-only) | Covered |
| IC-059 | Postman | P0 | Developer tools, QA and project coordination | Replace/defer paid wrapper | Hybrid / commercial service; exact edition licence verify | Free plan; API and collaboration limits verify / Paid plan/API entitlement or provider quota; current rate not verified | B07/B10 shared optional; no new commitment | Part 3.2 §3.2.5 | Defer (developer-only) | Covered |
| IC-060 | GitHub | P0 | Developer tools, QA and project coordination | Replace/defer paid wrapper | Hybrid / commercial service; exact edition licence verify | Free plan; Actions minutes/storage depend on account / Paid plan/API entitlement or provider quota; current rate not verified | B07/B10 shared optional; no new commitment | Part 4.3 CI | Defer (developer-only) | Covered |
| IC-061 | Security Guidance | P0 | Observability, error tracking, metrics and security | Replace/defer paid wrapper | Claude skill/plugin; licence unverified; development-first | Claude plan limits; no independent runtime quota assumed / No separate installation fee assumed only after verification; production model/API usage billed separately | B09 developer seats; B02 runtime if applicable | AD-15 Sentry, AD-16 CloudWatch; ADR-078 | Retain OSS / existing | Covered |
| IC-062 | Agent SDK Dev | P1 | LLM / agent framework | Replace/defer paid wrapper | Claude skill/plugin; licence unverified; development-first | Claude plan limits; no independent runtime quota assumed / No separate installation fee assumed only after verification; production model/API usage billed separately | B09 developer seats; B02 runtime if applicable | AD-13 Anthropic via ai.gateway (ADR-070) | Replace (native gateway) | Covered |
| IC-063 | DeepEval | P1 | Developer tools, QA and project coordination | Retain open-source candidate if justified | Open source — Apache-2.0 | Self-host: no vendor execution quota; compute limits apply / ₹0 software licence; hosting/maintenance and connected API charges extra | B01 shared; no duplicate allocation | ADR-079 | Defer (developer-only) | Covered |
| IC-064 | Pydantic AI | P1 | LLM / agent framework | Retain open-source candidate if justified | Open source — MIT | Self-host: no vendor execution quota; compute limits apply / ₹0 software licence; hosting/maintenance and connected API charges extra | B01 shared; no duplicate allocation | Part 7.3 §7.5.3 | Replace (native gateway) | Covered |
| IC-065 | Resend | P1 | Email automation and inbox | Replace workflow; external service conditional | Proprietary hosted email service | Free plan exists; transactional/marketing limits separately verify / Paid plans + overage; published extra emails $0.90/1,000 on applicable plan | B05 alternative to SES; not additive | AD-01 alt (DEC-025) | Conditional external service (B05) | Covered |
| IC-066 | Zoom | P1 | Meeting scheduling and video | Replace workflow; external service conditional | Hybrid / commercial service; exact edition licence verify | Basic plan; meeting/API limits verify / Paid plan/API entitlement or provider quota; current rate not verified | B07/B10 shared optional; no new commitment | AD-18 | Conditional external service (B15) | Covered |
| IC-067 | Figma | P1 | Developer tools, QA and project coordination | Replace/defer paid wrapper | Hybrid / commercial service; exact edition licence verify | Free Starter plan; limits verify / Paid plan/API entitlement or provider quota; current rate not verified | B07/B10 shared optional; no new commitment | Delivery tooling (Part 7.3 §7.5.2) | Defer (developer-only) | Covered |
| IC-068 | Langfuse | P1 | Observability, error tracking, metrics and security | Replace/defer paid wrapper | Hybrid / commercial service; exact edition licence verify | Self-host option; cloud free limits verify / Paid plan/API entitlement or provider quota; current rate not verified | B07/B10 shared optional; no new commitment | ADR-078 / B22 | Retain OSS / existing | Covered |
| IC-069 | PostHog | P1 | Marketing campaigns and attribution | Replace/defer paid wrapper | Hybrid / commercial service; exact edition licence verify | Free quotas differ by feature / Paid plan/API entitlement or provider quota; current rate not verified | B07/B10 shared optional; no new commitment | M39 campaigns; AU-040 | Replace (native) | Covered |
| IC-070 | Sentry | P1 | Observability, error tracking, metrics and security | Replace/defer paid wrapper | Hybrid / commercial service; exact edition licence verify | Free tier; error/trace quotas verify / Paid plan/API entitlement or provider quota; current rate not verified | B07/B10 shared optional; no new commitment | AD-15 | Retain OSS / existing | Covered |
| IC-074 | AWS Serverless | P2 | Cloud infrastructure and storage | Replace/defer paid wrapper | Proprietary managed cloud | Account/region/service-specific free credits and quotas; no blanket free tier / Metered region/service pricing; calculate from actual storage, requests, secrets, logs and compute | B01 ₹5,000/month; B07 ₹500/month monitoring shared | AWS ap-south-1 (DEC-040) | Retain existing (B01) | Covered |
| IC-077 | PandaDoc | P2 | Document generation / secure storage | Replace workflow; external service conditional | Hybrid / commercial service; exact edition licence verify | Trial/free features; production API entitlement verify / Paid plan/API entitlement or provider quota; current rate not verified | B07/B10 shared optional; no new commitment | AU-036 document assembly; S3 | Replace (native) | Covered |
| IC-079 | Exa | R | Public market / investor search | Replace first; conditional search fallback | Proprietary hosted API | Advertised >$120 credits/year; account-specific allowance verify / Search pricing varies by mode: published from $4/1,000 requests; confirm selected tier | B03 alternative to Tavily; no extra allocation | AD-06 | Replace core; investor use excluded (DEC-002 scope) | Covered |
| IC-088 | AWS Agents | V | LLM / agent framework | Replace/defer paid wrapper | Unverified — plugin/upstream licence not established | — / not verified | ₹0 committed; no activation until verification | AD-13 Anthropic via ai.gateway (ADR-070) | Replace (native gateway) | Covered |
| IC-111 | Enterprise Search | V | Embeddings, knowledge and enterprise search | Replace/defer paid wrapper | Unverified — plugin/upstream licence not established | — / not verified | ₹0 committed; no activation until verification | AD-14 EmbeddingPort; pgvector (ADR-077) | Retain OSS | Covered |
| IC-122 | AWS Amplify | V | Cloud infrastructure and storage | Replace/defer paid wrapper | Unverified — plugin/upstream licence not established | — / not verified | ₹0 committed; no activation until verification | AWS ap-south-1 (DEC-040) | Retain existing (B01) | Covered |
| IC-123 | AWS Startup Advisor | V | Cloud infrastructure and storage | Replace/defer paid wrapper | Unverified — plugin/upstream licence not established | — / not verified | ₹0 committed; no activation until verification | AWS ap-south-1 (DEC-040) | Retain existing (B01) | Covered |
| IC-124 | AWS Transform | V | Cloud infrastructure and storage | Replace/defer paid wrapper | Unverified — plugin/upstream licence not established | — / not verified | ₹0 committed; no activation until verification | AWS ap-south-1 (DEC-040) | Retain existing (B01) | Covered |
| IC-130 | Deploy on AWS | V | Cloud infrastructure and storage | Replace/defer paid wrapper | Unverified — plugin/upstream licence not established | — / not verified | ₹0 committed; no activation until verification | AWS ap-south-1 (DEC-040) | Retain existing (B01) | Covered |
| IC-136 | Migration to AWS | V | Cloud infrastructure and storage | Replace/defer paid wrapper | Unverified — plugin/upstream licence not established | — / not verified | ₹0 committed; no activation until verification | AWS ap-south-1 (DEC-040) | Retain existing (B01) | Covered |
| IC-176 | Slack | V | Customer support / collaboration | Replace/defer paid wrapper | Commercial service / hybrid; exact wrapper and upstream licence unverified | — / not verified | ₹0 committed; use only after approved procurement | M63 support; NT notifications | Replace (native) | Covered |
| IC-190 | AWS Data Analytics | V | Analytics, reporting and forecasting | Replace/defer paid wrapper | Unverified — plugin/upstream licence not established | — / not verified | ₹0 committed; no activation until verification | RP-01…30; AU-040, AU-041 | Replace (native) | Covered |
| IC-199 | Cloud SQL for PostgreSQL | V | Embeddings, knowledge and enterprise search | Replace/defer paid wrapper | Unverified — plugin/upstream licence not established | — / not verified | ₹0 committed; no activation until verification | AD-14 EmbeddingPort; pgvector (ADR-077) | Retain OSS | Covered |
| IC-209 | Databases on AWS | V | Embeddings, knowledge and enterprise search | Replace/defer paid wrapper | Unverified — plugin/upstream licence not established | — / not verified | ₹0 committed; no activation until verification | AD-14 EmbeddingPort; pgvector (ADR-077) | Retain OSS | Covered |
| IC-270 | Apollo GraphQL | V | Professional contact discovery | Replace core; conditional licensed data only | Unverified — plugin/upstream licence not established | — / not verified | ₹0 committed; no activation until verification | AD-19 Apollo/Hunter (EnrichmentPort, OFF) | Conditional external service (B08/B18) | Conflict |
| IC-332 | Bio Research | V | Public market / investor search | Defer unless commercial evidence need approved | Unverified — plugin/upstream licence not established | — / not verified | ₹0 committed; no activation until verification | AD-05 Tavily / AD-06 Exa (SearchPort) | Replace core; investor use excluded (DEC-002 scope) | Covered |
| IC-360 | LegalZoom | V | Electronic signing and identity verification | Replace workflow; external service conditional | Unverified — plugin/upstream licence not established | — / not verified | ₹0 committed; no activation until verification | AD-10 ESignPort (manual first, DEC-023) | Conditional external service (B13) | Covered |
| IC-392 | Sentry CLI | V | Observability, error tracking, metrics and security | Replace/defer paid wrapper | Unverified — plugin/upstream licence not established | — / not verified | ₹0 committed; no activation until verification | AD-15 Sentry, AD-16 CloudWatch; ADR-078 | Retain OSS / existing | Covered |
| IC-405 | Stripe | V | Banking, receipts and billing | Replace workflow; external service conditional | Unverified — plugin/upstream licence not established | — / not verified | ₹0 committed; no activation until verification | AD-11 PaymentPort (manual first, DEC-022) | Conditional external service (B14) | Covered |
| IC-413 | Dropbox | V | Document generation / secure storage | Replace/defer paid wrapper | Unverified — plugin/upstream licence not established | — / not verified | ₹0 committed; no activation until verification | AU-036 document assembly; S3 | Replace (native) | Covered |
| IC-426 | Meeting Memory by Grain | V | Meeting scheduling and video | Replace/defer paid wrapper | Unverified — plugin/upstream licence not established | — / not verified | ₹0 committed; no activation until verification | AD-03/AD-04 Calendar; AD-18 Webinar | Conditional external service (B15) | Covered |
| IC-427 | Notion | V | Document generation / secure storage | Replace/defer paid wrapper | Unverified — plugin/upstream licence not established | — / not verified | ₹0 committed; no activation until verification | AU-036 document assembly; S3 | Replace (native) | Covered |
| IC-439 | Linear | V | Developer tools, QA and project coordination | Replace/defer paid wrapper | Unverified — plugin/upstream licence not established | — / not verified | ₹0 committed; no activation until verification | Delivery tooling (Part 7.3 §7.5.2) | Defer (developer-only) | Covered |
| IC-445 | AWS Agents for DevSecOps | V | Observability, error tracking, metrics and security | Replace/defer paid wrapper | Unverified — plugin/upstream licence not established | — / not verified | ₹0 committed; no activation until verification | AD-15 Sentry, AD-16 CloudWatch; ADR-078 | Retain OSS / existing | Covered |
| IC-486 | Equity Research | X | Public market / investor search | Defer unless commercial evidence need approved | Unverified — plugin/upstream licence not established | — / not verified | ₹0 committed; no activation until verification | AD-05 Tavily / AD-06 Exa (SearchPort) | Replace core; investor use excluded (DEC-002 scope) | Not applicable |
| IC-499 | Market Researcher | X | Public market / investor search | Replace/defer paid wrapper | Unverified — plugin/upstream licence not established | — / not verified | ₹0 committed; no activation until verification | AD-05 Tavily / AD-06 Exa (SearchPort) | Replace core; investor use excluded (DEC-002 scope) | Covered |
| IC-500 | Meeting Prep Agent | X | Meeting scheduling and video | Replace/defer paid wrapper | Unverified — plugin/upstream licence not established | — / not verified | ₹0 committed; no activation until verification | AD-03/AD-04 Calendar; AD-18 Webinar | Conditional external service (B15) | Covered |

**Not-applicable candidates (52).** IC-048 Carta crm, IC-050 Wealthbox, IC-076 PubMed, IC-331 AdisInsight, IC-333 BioRender, IC-334 bioRxiv, IC-335 Boltz, IC-336 ChEMBL, IC-337 Claude for Healthcare, IC-338 Clinical Trial Protocol, IC-339 Clinical Trials, IC-340 Consensus, IC-341 Cortellis, IC-342 Medidata, IC-343 Open Targets, IC-344 Owkin, IC-345 Scientific Problem Selection, IC-346 Synapse, IC-347 ToolUniverse, IC-348 Wiley Scholar Gateway, IC-473 Learn with Coursera, IC-474 Math Olympiad, IC-475 Math Proof, IC-476 Oak National Academy, IC-477 Scrimba Explain, IC-479 BlackRock Advisor Center, IC-480 Carta cap table, IC-481 Carta investors, IC-482 Chronograph GP, IC-483 Chronograph LP, IC-484 Claude for Financial Advisors, IC-485 Earnings Reviewer, IC-486 Equity Research, IC-491 Fund Admin, IC-495 Investment Banking, IC-496 Juniper Square, IC-498 LinqAlpha, IC-503 Morningstar, IC-505 Pitch Agent, IC-506 Private Equity, IC-507 PrivCo Data, IC-511 Valuation Reviewer, IC-512 Vanguard Advisor Tools, IC-513 Zocks Advisor, IC-514 Bonusly, IC-515 Greenhouse, IC-516 hr-legal-compliance, IC-517 Human Resources, IC-518 Lusha Talent Sourcing, IC-519 Remote.com, IC-520 Sana from Workday, IC-521 UKG Bryte. These are investor/fundraising, clinical/life-science, learner-assessment, HR or generic education tools. They stay in the register for traceability, are flagged `scope_excluded = true`, and AU-044 refuses any activation request for them (PG-02).

**Conflict candidate (1).** IC-270 *Apollo GraphQL* is a GraphQL developer toolkit (doc 16 category "Developer Workflows") but document 21 maps it to "professional contact discovery" with the decision "Replace core; conditional licensed data only", evidently by name similarity with Apollo.io [CONFLICT-407].

### 7.4.4.3 Capability replacement register (document 21 §3) to blueprint adapters

| # | Capability | Doc 21 avoid / replace | Doc 21 preferred implementation | Blueprint today | Status | Resolution / enhancement |
|---|---|---|---|---|---|---|
| 01 | Workflow orchestration and RPA | Zapier, Make, hosted n8n | Django services, outbox, Celery/Beat, Valkey; revisioned DAG; approval nodes | ADR-071; DEC-051; M55 engine; A033 | Covered | 13 node types (§7.4.5.7.3) |
| 02 | Public market search | Tavily, Exa, premium research agents | Source registry, RSS/sitemap/official adapters, conditional fetch, PostgreSQL full text; optional SearXNG | AD-05 Tavily primary, AD-06 Exa off | Conflict | CONFLICT-401, CONFLICT-406 |
| 03 | Website extraction | Firecrawl Cloud, Apify, Zyte, Bright Data | Scrapy + Trafilatura; Playwright only for permitted JS pages | ADR-018 Firecrawl self-hosted + trafilatura | Conflict | CONFLICT-402 (benchmark decides) |
| 04 | Professional contact discovery | Apollo, Hunter, ZoomInfo, Lusha, RocketReach, Clay | Official pages, consented referrals, inbound forms; syntax/MX checks; unknown stays unverified | AU-018; AD-19 OFF | Partial | FR-ENH-F-023 |
| 05 | CRM | HubSpot, Salesforce, monday CRM, Nimble | Native PostgreSQL records and state machines | M21–M23; AU-020, AU-021 | Covered | — |
| 06 | LLM / agent framework | Hosted agent builders, plugin runtime | Typed Python + Pydantic; local llama.cpp/vLLM gateway; paid fallback by budget | ADR-070…072; DEC-007 (Anthropic primary) | Conflict | CONFLICT-400 |
| 07 | Embeddings and search | Hosted vector DB, enterprise search | pgvector + full text; local embedding; ACL before retrieval; remove revoked | ADR-077; AU-001 | Partial | AU-046 |
| 08 | Email | Resend, SendGrid, ActiveCampaign | Django sequence worker + approved relay; SPF/DKIM/DMARC; suppression | DEC-025 (SES); AD-01 | Covered | — |
| 09 | WhatsApp, SMS, social messaging | Paid BSP plugins | First-party business API; no unofficial bots | AD-02 | Covered | — |
| 10 | Meetings and video | Calendly, Zoom extensions, meeting memory | Django availability, iCalendar, Jitsi or existing account; local transcription only with notice | AU-023; GAP-143 | Partial | AG-037 (notes only) |
| 11 | Documents and storage | PandaDoc templates, Dropbox, Notion | python-docx, Jinja2, LibreOffice headless; S3 prefixes; scan | AU-036; AD-20 | Covered | — |
| 12 | E-sign and identity | PandaDoc signing, LegalZoom | Signed-upload workflow; Documenso after review; regulated e-sign/KYC when required | DEC-023; AD-10 shortlist | Partial | Documenso added to evaluation shortlist (RECOMMENDATION-405) |
| 13 | Banking and billing | Stripe automation, aggregator plugins | Decimal ledger state machine; bank import; official gateway webhooks | DEC-022; AD-11 | Covered | — |
| 14 | Observability | Hosted Sentry, Datadog | OpenTelemetry, Prometheus + Grafana, local exception tracking, Trivy/OSV | DEC-041 Sentry free tier + CloudWatch | Conflict | CONFLICT-409 |
| 15 | Cloud infrastructure | AWS convenience plugins | Containers, backups/WAL, reverse proxy; OpenTofu/Ansible after review | DEC-040; Part 4.3 IaC | Covered | — |
| 16 | Developer tools | Paid skills, Postman paid tier, wrappers | Git, pytest, Vitest, Playwright, Bruno/curl | Part 7.3 §7.5.2; Part 4.3 | Covered | — |
| 17 | Analytics and forecasting | Paid BI | PostgreSQL aggregates, React charts, Python statistics | RP-01…30; AU-041 | Covered | — |
| 18 | Support and collaboration | Slack/Teams/Intercom wrappers | Built-in tasks, notifications, inbox | AG-031; NT | Covered | — |
| 19 | Content and localization | Writesonic, Content Studio | Claim store + LLM draft + human review; Jinja variants | AG-018; AG-012 | Covered | — |
| 20 | SEO | SearchAtlas, Botify, SearchFit, AppTweak, vidIQ | Lighthouse + Scrapy audits; Search Console API | AU-033; AD-17 | Covered | — |
| 21 | Social publishing | Postiz Cloud, Socialinsider | Celery publisher with official APIs; Postiz self-host after AGPL review | AD-08; AU-029 | Covered | — |
| 22 | Campaigns and attribution | Customer.io, Pendo, Common Room, Leadfeeder, Supermetrics, Windsor.ai | Native audience rules, consent, UTM attribution; Matomo optional | AU-040; Part 3.1 alternatives | Covered | — |
| 23 | Advertising | Adspirer, Realize, Spotify Ads wrappers | Direct ad APIs with budget cap and campaign hash | AD-09; AU-032; B12 | Covered | — |
| 24 | Website builder | Unbounce, B12, Replo, WordPress builders | React templates and publication snapshots | B-WEB; A107, A108 | Covered | — |
| 25 | Tender discovery and bids | GovTribe | Official portal feeds; deadline/eligibility extraction; manual submission | DEC-053; AU-034; AG-019 | Partial | AU-052 (amendments) |
| 26 | Supplier, order, retention | Commerce/ERP adapters | Django quote/order services, Decimal, ledgers | WF-10; AU-035, AU-038 | Covered | — |
| 27 | Webinar and demo registration | Paid event tools | Website forms, capacity, calendars, consented reminders | AD-18; M40 | Partial | AU-051 |

### 7.4.4.4 Budget lines (document 16 register) to DEC-020 and Part 8.2 §8.2.7

All amounts are monthly INR estimates unless stated; **verify all rates at time of implementation (as of 27 Nov 2026)**. "Source" = document 16 budget register (identical to BRD §6); "Revised" = Part 8.2 §8.2.7.2.

| Line | Source item and amount | DEC-020 | Part 8.2 revised | Candidate rows referencing it | Status | Note |
|---|---|---|---|---|---|---|
| B01 | AWS shared hosting 5,000 | B01 5,000 | 5,000–7,000 | 11 | Covered | Errata 44 revision governs |
| B02 | Production AI inference 3,000 | B02 3,000 (cap) | 3,000 cap; expected 512 / 1,150 / 2,992 | 20 | Covered | New agents AG-037/038 add ≈ ₹15 base / ₹43 high (§7.4.5.6) |
| B03 | Public search API 1,500 | B03 1,500 | 1,500 | 2 | Covered | CONFLICT-401 changes the primary, not the amount |
| B04 | Extraction compute/overage 1,000 | B04 1,000 | 1,000 | 2 | Covered | — |
| B05 | Email delivery 500 | B05 500 | 500 | 2 | Covered | Resend "alternative, not additive" |
| B06 | WhatsApp Business 2,000 | B06 2,000 | 2,000 | 1 | Covered | — |
| B07 | Monitoring/security/CI 500 | B07 500 | 500 | 12 | Covered | — |
| B08 | Apollo paid enrichment reserve 9,000 | B08 9,000 OFF | 0 until scale gate | 1 | Covered | — |
| B09 | Claude Code seats 3,600 | B09 3,600 | 3,600 | 17 | Covered | 17 developer plugins draw on seats only |
| B10 | Optional integration reserve 1,000 | B10 1,000 | 1,000 | 13 | Covered | Benchmark trial spend charged here (RECOMMENDATION-415) |
| B11 | Contingency 15% | B11 15% | 15% | — | Covered | — |
| B12–B22 | Not in source | Reserved ₹0 | Per Part 8.2 | 0 | Covered | No candidate requests a reserved line |
| B23 | Not in source | Not in DEC-020 text (errata 27) | ≈ 1,000 | 0 | Covered | Inconsistency reported (§7.4.6) |
| Σ | Base before contingency 14,500 | — | 17,100–19,900 | — | Covered | — |
| Σ | Base incl. contingency 16,675 | — | 19,665–22,885 | — | **Conflict** | CONFLICT-412 |
| Σ | Base incl. seats 20,815 | — | not shown | — | **Not covered** | Added: 23,805–27,025 |
| Σ | Paid Apollo runtime 27,025 | — | not shown | — | **Not covered** | Added: 30,015–33,235 |
| Σ | Paid Apollo + seats 31,165 | — | 34,155–37,375 | — | Covered | — |
| Σ | Base annual incl. seats 249,780 | — | not shown | — | **Not covered** | Added: 285,660–324,300 |
| Σ | Paid Apollo annual incl. seats 373,980 | — | not shown | — | **Not covered** | Added: 409,860–448,500 |
| Σ | Base annual runtime 200,100 | — | not shown | — | **Not covered** | Added: 235,980–274,620 |
| Σ | Paid Apollo annual runtime 324,300 | — | not shown | — | **Not covered** | Added: 360,180–398,820 |
| Σ | Three-month base 62,445 | — | not shown | — | **Not covered** | Added: 71,415–81,075 |
| Σ | Three-month paid Apollo 93,495 | — | not shown | — | **Not covered** | Added: 102,465–112,125 |

**Arithmetic check of the source register (all reproduced exactly).** 5,000 + 3,000 + 1,500 + 1,000 + 500 + 2,000 + 500 + 1,000 = 14,500; × 1.15 = 16,675; (14,500 + 3,600) × 1.15 = 20,815; (14,500 + 9,000) × 1.15 = 27,025; (14,500 + 9,000 + 3,600) × 1.15 = 31,165; × 12 = 200,100 / 249,780 / 324,300 / 373,980; × 3 = 62,445 / 93,495. The formulas and the revised equivalents are in Part 7.4b §7.4.5.10.

### 7.4.4.5 Optimization controls and OKPIs in Group F scope

| OPT control | Source target | Blueprint | Status | OKPI (pack ID → blueprint label) |
|---|---|---|---|---|
| OPT-03-01 | Zero unapproved paid calls; full TCO | BRD §10; AU-002 | Partial | OKPI-11 Unapproved paid provider calls ≤ 0 (mandatory) |
| OPT-03-07 | Zero unauthorized overspend under parallel reservation | IP-06; AU-002 | Covered | OKPI-12 Unauthorized budget overspend ≤ 0 (mandatory) |
| OPT-03-08 | Alerts 70%/90%; pause optional jobs at cap | ADR-083 80/100% | Conflict | — (CONFLICT-403) |
| OPT-04-07 | Completion ≥ 99% of eligible due runs | AU-026, AU-028 | Partial | OKPI-09 Eligible workflow completion ≥ 99% |
| OPT-04-08 | ≥ 90% eligible steps automated | AU-025 | Partial | OKPI-10 Eligible steps automated ≥ 90% |
| OPT-09-05 | All attributable consumption metered | AU-012 | Covered | OKPI-21 Attributable consumption assigned ≥ 100% |
| OPT-10-02 | ≥ 99.5% schema-valid | Part 7.3 §7.6.9 ≥ 99% | Conflict | OKPI-13 Schema-valid AI outputs ≥ 99.5% |
| OPT-10-03 | ≥ 95% evidence-grounded accuracy | Part 7.3 §7.6.9 | Covered | OKPI-14 Evidence-grounded accuracy ≥ 95% |
| OPT-04-02 / OPT-11-04 | Precision ≥ 90% | DEC-001 80% (W1) / 90% (L2) | Conflict | OKPI-15 Opportunity classification precision ≥ 90% |
| OPT-10-06 | Mandatory regression passes | AU-006 | Covered | OKPI-16 Mandatory regression pass rate = 100% (mandatory) |
| OPT-03-03 | Cost per qualified verified opportunity improves | KPI-21 (cost per AI task) | Partial | OKPI-24 Acquisition cost improvement ≥ 0% |
| OPT-04-03 | Zero sends to ineligible recipients | AU-009 | Covered | OKPI-35 Disallowed dispatch or formal offer ≤ 0 (mandatory); OKPI-08 Duplicate external message execution ≤ 0 |

### 7.4.4.6 Automation library (document 38 §09) to the AG/AU catalogue

| Library element | Source count | Named in pack? | Blueprint before 7.4 | After Part 7.4b |
|---|---|---|---|---|
| Use-case groups | 20 | Group names only | Implicit in AG/AU and WF-01…14 | 20 groups mapped (§7.4.5.7.1) |
| Use cases | 100 | No | 87 of 100 proposed use cases map to existing AG/AU | 100 mapped; 13 filled by AG-037, AG-038, AU-044…AU-052 |
| Industry templates | 20 | No | CFG-04 business templates, 4 seeded startups | TPL-01…TPL-20 proposed (§7.4.5.7.2) |
| Node types | 13 | No | DEC-051 "approved node types"; examples in Part 5.3/6.3a | NT13-01…NT13-13 canonical list (§7.4.5.7.3) |

---

## 7.4.4.7 Quality gate: Batch 7.4a

| # | Check | Result | Notes / fixes applied |
|---|---|---|---|
| 1 | Every requirement traced to a source | Pass | Every aspect row cites its document section and the blueprint location |
| 2 | Assumptions/gaps/conflicts tagged and logged | Pass | Tags issued here are registered in Part 7.4b §7.4.8 |
| 3 | IDs unique and consistent | Pass | Aspect IDs F15/F16/F21/F38-### unique (asserted by the build script); IC numbers keep the source numbering; OKPI prefix used for the pack's KPIs |
| 4 | No story lacks AC; no requirement lacks a test | N/A | Stories, ACs and tests are in Part 7.4b |
| 5 | Negative, edge, security and accessibility cases | N/A | Covered by the tests in Part 7.4b |
| 6 | No agent lacks guardrail, fallback, KPI and cost | N/A | New agents specified in Part 7.4b |
| 7 | Time-sensitive facts flagged "verify" with as-of date | Pass | All rates and free tiers marked historical and "verify at implementation (as of 27 Nov 2026)" |
| 8 | No restricted data routed to free-tier models | Pass | No change to DEC-007 routing proposed |
| 9 | Consistent with earlier parts | Pass with conflicts logged | 17 conflict rows (13 distinct conflicts) carried to Part 7.4b §7.4.6; numbering collision CONFLICT-410 |

**Fixes applied during drafting.** (1) The first parser pass classified 452 licences as "unverified" because it searched for keywords; it now classifies by the source's own licence phrases (six classes). (2) A first status pass marked the 19 investor and clinical candidates as "Covered (deferred)"; they are now "Not applicable" with an explicit never-activate rule. (3) IC-270 *Apollo GraphQL* was first accepted under its document-21 mapping; it is now a conflict.

**Status: Part 7 Batch 7.4a complete. 804 coverage rows (625 covered, 50 partial, 45 not covered, 17 conflict, 67 not applicable); all 538 integration candidates parsed and reconciled. Next: Batch 7.4b (enhancements).**
