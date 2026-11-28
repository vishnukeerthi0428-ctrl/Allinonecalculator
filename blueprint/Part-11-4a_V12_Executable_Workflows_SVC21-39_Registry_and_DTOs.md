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
| D-APB-001 | One JSON Schema 2020-12 document per workflow; $id urn:sm:dto:<workflow>:v2; $defs.input and $defs.output | Not covered | None | Schema registry (DEC-565; ADR-198) | DEC-565; ADR-198 | Matched |
| D-APB-002 | Types reflect corrected DTO tables (D2); "all 156 pass meta-schema validation" | Not covered | None | CI gate re-validates every schema (TC-V12-D-002); 76/76 parsed here | TC-V12-D-002 | Matched |
| D-APB-003 | additionalProperties false; every input and output property required; one shared schema per service (4 workflows) | Not covered | None | v3 fix: per-workflow produced-output projection; non-produced outputs nullable (GAP-824) | DEC-565; GAP-824 | Matched |
| D-APB-004 | Configured enums as string maxLength 64 with values from a versioned registry | Not covered | None | Enum registry table (§11.4b.4) | DEC-565 | Matched |
| D-APB-005 | Arrays of string/object with maxItems 500 | Not covered | None | Typed item schemas in v3 (GAP-824) | DEC-565; GAP-824 | Matched |
| D-APB-006 | Free text minLength 1 maxLength 4000 | Not covered | None | Adopted; text treated as untrusted (AU-005) | DEC-565 | Matched |
| D-APB-007 | Refs uuid format; currency ^[A-Z]{3}$; integers minimum 0 or 1; money as integer minor units | Not covered | ADR-030 decimal strings | Minor units at workflow DTO boundary only (RECOMMENDATION-829) | DEC-565; RECOMMENDATION-829 | Matched |
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

#### 11.4.3.5 Every Conflict aspect individually (all end Pending Founder decision)

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
