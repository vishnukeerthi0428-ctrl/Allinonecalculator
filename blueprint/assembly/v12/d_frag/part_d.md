# AI Growth Engine: Employee Sales & Marketing Automation
## Application Blueprint: PART 11 (Batch 11.4d), V12 Executable Workflows: Specifications SM-SVC-31…39, Requirements, Stories, Tests, Cost, Conflicts and Decisions

| Field | Value |
|---|---|
| Document | Part 11, Batch 4d of 4: executable specifications of the 36 workflows of SM-SVC-31…39 (103 steps); new domain entities; FR-V12-D register; stories; tests; effort and cost; ADR-196…199; conflicts; decisions; persona review; tags; quality gate |
| Version | 1.0 · 28 Nov 2026 |
| Baseline | Parts 11.4a–c; Parts 0–9.10; DEC-001…422 |
| V12 sources | BRD ch09; FSD ch12 entries lines 13,153–16,707; FSD ch13; App. B; workbook |
| Roles applied | Principal Workflow/BPM Architect, Event-driven Systems Architect, QA Architect, Principal Engineer, Product Owner, Security/AI-Governance Lead, FinOps Lead |

## 11.4.5 Enhancements (part 3 of 3)

Workflow cards follow the reading guide of Part 11.4c. Common rules (preconditions, failure handling, idempotency, timeouts, retries, outbox, simulation, Tier 2 ineligibility) are in Part 11.4b and are not repeated.

{{SERVICES_2}}

### 11.4.5.29 New domain entities for the new services (ASSUMPTION-827)

FSD-POL-V6-ARTIFACT requires fields with relational constraints, ledgers, uniqueness or retention to be normalized before production. The workflows that are new to the blueprint therefore get these proposed tables (all with STD-S, STD-W and RLS; final DDL owned by the data group):

| Table | Purpose (service) | Key columns and constraints | Retention class |
|---|---|---|---|
| `prc_requirement` | Approved procurement requirement (SVC-39) | id, tenant_id, startup_id, need_text_ref, quantity, unit, required_by, budget_line_id, state ∈ {draft, approved, sourcing, closed}, approved_by | Commercial record (Part 3.3 COM) |
| `prc_supplier_quote` | Supplier quotation (SVC-39) | id, requirement_id FK, supplier_org_id FK intel_organization, currency, total numeric(18,4), valid_until, document_id, normalized_terms jsonb (validated); UNIQUE (requirement_id, supplier_org_id, revision) | COM |
| `prc_purchase_order` / `prc_po_line` | Human-approved purchase commitment (SVC-39-WF03) | id, requirement_id, quote_id, po_number UNIQUE per startup per FY, currency, total, state ∈ {draft, awaiting_approval, approved, sent, acknowledged, received_partial, received, closed, cancelled}, mandate_id FK aut_mandate; lines: offering/SKU, unit, qty numeric(18,3), price numeric(18,4); over-receipt rejected (AU-038 rule) | Financial (8 years, DEC-028 analogue; verify) |
| `mkt_marketplace_listing` | Listing on an authorized marketplace (SVC-31) | id, integration_id, offering_version_id, price_version_id FK cat_price_version, external_listing_id UNIQUE per integration, state ∈ {draft, approved, published, suppressed, error}, content_hash | Marketing (Part 3.3 MKT) |
| `com_marketplace_order_event` | Idempotent marketplace order/cancel/return event (SVC-31-WF03) | id, integration_id, provider_event_id UNIQUE per integration, order_ref, event_kind ∈ {order, cancel, return, refund_notice}, occurred_at, payload_ref | OPS 13 months, then summarised |
| `com_marketplace_settlement` | Settlement and fee lines for reconciliation (SVC-31-WF04) | id, integration_id, settlement_ref UNIQUE, gross, fees, tax, net (numeric(18,4)), currency, period | Financial |
| `sup_case` / `sup_sla_policy` | Customer support case and SLA policy (SVC-33) | case: id, account_id, thread_id, severity ∈ {S1…S4}, queue_id, state ∈ {new, triaged, in_progress, waiting_customer, resolved, closed}, sla_due_at, breached_at; policy: per severity response/resolve minutes, business calendar | Service (24 months) |
| `mkt_brand_review` | Public review item from an authorized source (SVC-35) | id, source_id FK intel_source, external_review_id UNIQUE per source, rating, text_ref, observed_at, language, classification, response_draft_id | Research (source licence governs) |
| `eng_sms_sender` / `eng_sms_template` | DLT header and registered template (SVC-38) | sender: header, entity_id, dlt_status ∈ {pending, approved, suspended}; template: dlt_template_id, category ∈ {transactional, service, promotional}, body_hash, variables, approved_at | Config |
| `int_external_agent` | Verified external AI agent identity (SVC-28) | id, tenant_id, protocol ∈ {mcp, a2a, other}, client_id, public_key_ref, scopes text[] (read_catalog, request_quote only), verified_by, state ∈ {pending, active, suspended, revoked}, expires_at | Security (Part 4.1) |
| `com_agent_request` | Requirement/quote request received from an external agent (SVC-28-WF02) | id, external_agent_id, request_hash UNIQUE, requirement jsonb (validated), quote_id (draft) FK com_quote, state ∈ {received, validated, drafted, approved_for_release, released, rejected} | COM |
| `mkt_asset_rights` | Rights evidence for every creative asset (SVC-27-WF04) | id, asset_id, rights_type ∈ {owned, licensed, stock, generated}, licence_ref, territories, expires_at, model_release_ref, state ∈ {unknown, cleared, restricted, rejected} | Marketing |
| `eng_call` | Voice call record (SVC-26; **created only if the Founder approves CONFLICT-815**) | id, contact_id, direction, consent_id, disclosure_played boolean, disposition, started_at, ended_at, minutes, transcript_ref NULL by policy | Disabled |

### 11.4.5.30 Functional requirement register (FR-V12-D)

| FR | Requirement | V12 source | Priority | Package | Test |
|---|---|---|---|---|---|
| FR-V12-D-001 | The platform shall register every V12 workflow under its literal ID with service, authority class, semantic version, implementation status, historical group, DTO schema, handler manifest, control links, KPI IDs and channel allowlist; reject runs of unapproved or unregistered revisions; keep active-run snapshots immutable | ch13 FL-01; workbook versions/status/migration; REC-08 | P0 | CR-V12-D-1 | TC-V12-D-001 |
| FR-V12-D-002 | Validate run input and result against the registered App. B schema (v2) and the per-workflow v3 output projection; return field errors with JSON pointers; CI re-validates all schemas | ch12 FL-02; App. B; GAP-824 | P0 | CR-V12-D-1 | TC-V12-D-002 |
| FR-V12-D-003 | Bind every STEP ID to an executor, NT13 node type, handler, contracts, timeout, retry class, side-effect class, confidence floor, context budget and tests; a workflow with an unbound step cannot be activated | ch12 FL-03; ch13 AI-06 | P0 | CR-V12-D-1 | TC-V12-D-003 |
| FR-V12-D-004 | Checkpoint step state, version, artifact refs and effect status before acknowledgement; 30 s heartbeats; reaper reclaims after 3 missed beats; in-flight effects go to RECONCILING | ch13 ST-04; ch19 heartbeats | P0 | CR-V12-D-1 | TC-V12-D-004 |
| FR-V12-D-005 | Compute the step idempotency key as tenant/company/run/version/step/target digest; finalize in one transaction (result, provenance, receipts, actuals, release, audit) | FSD-POL-V6-PRECHECK; ST-05 | P0 | CR-V12-D-1 | TC-V12-D-005 |
| FR-V12-D-006 | Apply retry classes validation (never), transient read (≤ 3, jitter), throttle (Retry-After), uncertain write (reconcile first), model transient (gateway ≤ 2) | ch13 ST-06 | P0 | CR-V12-D-1 | TC-V12-D-006 |
| FR-V12-D-007 | Run the nine-check preflight in fixed order; `dry_run` returns plan, estimate and would-be holds with zero provider calls and no reservation | ch12 FL-07; ch19 V5 preflight | P0 | CR-V12-D-1 | TC-V12-D-007 |
| FR-V12-D-008 | Route any AI step below its confidence floor or failing schema/claims checks to human review; never to an effect | ch12 FL-08 | P0 | CR-V12-D-1 | TC-V12-D-008 |
| FR-V12-D-009 | Bind approvals as mandates (actor, role, resource, action, digest, amount, policy version, expiry, revocation); any change, expiry, revocation or stricter policy blocks the effect | ch13 FL-09; ch12 V4 approval | P0 | CR-V12-D-1 | TC-V12-D-009 |
| FR-V12-D-010 | Receive events through `ops_inbox` with verification, scoped uniqueness and dedupe; one eligible run per committed event | ch13 FL-05; trigger rules Event / Provider callback | P0 | CR-V12-D-1 | TC-V12-D-010 |
| FR-V12-D-011 | Start child workflows only through registered dependencies with depth ≤ 3, cycle check, and target entitlement or equivalent authorized input | ch13 FL-10; trigger rule Child workflow | P1 | CR-V12-D-1 | TC-V12-D-011 |
| FR-V12-D-012 | Cancel runs with release of unused reservations; compensate only reversible effects through approved compensation actions; hold uncertain effects for reconciliation | ch12 FL-11 | P0 | CR-V12-D-1 | TC-V12-D-012 |
| FR-V12-D-013 | Treat industry/business templates as versioned parameter sets over a registered workflow; never clone definitions; publish only entitled and tested templates with reviewer ≠ author | ch12 FL-12, MT-29, REC-05; BRD ch09 MT-34 | P1 | CR-V12-D-1 | TC-V12-D-013 |
| FR-V12-D-014 | Store an acceptance record for every accepted AI output (schema, evidence, confidence, policy, evaluator version) | ch12 FL-13 | P0 | CR-V12-D-1 | TC-V12-D-014 |
| FR-V12-D-015 | Rank expensive, slow and failure-prone workflows from the run ledger and propose evaluated changes with baseline, expected impact and rollback; never auto-apply | ch12 FL-14 | P2 | CR-V12-D-2 | TC-V12-D-015 |
| FR-V12-D-016 | Schedule triggers in IANA time zones with UTC next-fire, per-tenant concurrency and misfire policy skip or reschedule_once; never burst | ch13 trigger rule Scheduled | P0 | CR-V12-D-1 | TC-V12-D-016 |
| FR-V12-D-017 | Maintain triggers of five kinds with requester, reviewer, test evidence, revision and dedupe; enable only after a zero-effect test and reviewer approval | ch13 REC-01; trigger draft fields | P0 | CR-V12-D-1 | TC-V12-D-017 |
| FR-V12-D-018 | Use run state model v2 with optimistic transitions, immutable terminal states, adjustment records, BusinessContext and configuration-version checks; show the A110 timeline with reservations, actuals (known/unknown) and uncertain outcomes | ch19 run states, REC-02, V6 context | P0 | CR-V12-D-1 | TC-V12-D-018 |
| FR-V12-D-019 | Share each queue fairly across (tenant, company) by weighted deficit round robin with per-tenant in-flight caps and per-(provider, tenant) caps | ch19 MT-28, ST-03 | P0 | CR-V12-D-1 | TC-V12-D-019 |
| FR-V12-D-020 | Reserve money and units atomically across tenant, company, offering, service and workflow budget levels with currency, period and time zone | ch19 MT-30; ch12 V4 budget | P0 | CR-V12-D-1 | TC-V12-D-020 |
| FR-V12-D-021 | Execute declared parallel branches of no-effect steps with join conditions; propagate cancellation; keep effects sequential | ch19 FL-06 | P1 | CR-V12-D-2 | TC-V12-D-021 |
| FR-V12-D-022 | Let tenant administrators pause, resume and re-cadence schedules within template bounds and preference windows; consent and safety gates stay enforced | ch19 RT-08 | P1 | CR-V12-D-2 | TC-V12-D-022 |
| FR-V12-D-023 | Generate run request forms from the DTO input schema and common fields; provide next/previous/restart walkthrough and the state-derived trace in simulation | ch12 V4 input contract, UI input contracts; ch13 walkthrough | P1 | CR-V12-D-1 | TC-V12-D-023 |
| FR-V12-D-024 | Document V10 node patterns as NT13 semantics; add `logic.reconcile`; validate schema and effect policy before any handler runs | ch13 REC-09, node patterns | P1 | CR-V12-D-1 | TC-V12-D-024 |
| FR-V12-D-025 | Store the historical group label per workflow; claim no recovered historical entries | ch12/BRD ch09 REC-08 | P2 | CR-V12-D-1 | TC-V12-D-025 |
| FR-V12-D-026 | Map V12 authority (L0–L4, R0–R3) to blueprint autonomy with stricter-wins; deny any run whose requested autonomy exceeds the cap | BRD ch18 table; ch12 authority rows | P0 | CR-V12-D-1 | TC-V12-D-026 |
| FR-V12-D-027 | Register each workflow KPI with formula, numerator, denominator, source table, baseline status ("approved in pilot") and threshold owner | ch12 workflow KPI rows; BRD ch09 KPI column | P1 | CR-V12-D-1 | TC-V12-D-027 |
| FR-V12-D-028 | Meter usage per workflow unit and actual cost into the usage ledger; enforce the per-service pilot unit cap as a hard cap | App. "DB-V2-USAGE"; workbook usage limits and cost | P0 | CR-V12-D-1 | TC-V12-D-028 |
| FR-V12-D-121 | Provide SM-SVC-21 WF01–WF04 as specified in §11.4.5.10: import, partial allocation, discrepancy reporting, receivable risk; record and verify only, never move money; finance maker-checker | BRD/FSD SVC-21 | P0 | D-1 (WF01–03), D-1 (WF04 R2) | TC-V12-D-121 |
| FR-V12-D-122 | Provide SM-SVC-22 WF01–WF04 (§11.4.5.11); no health data in pilot readiness; reminders through approved templates | SVC-22 | P1 | D-1, D-2 (WF04) | TC-V12-D-122 |
| FR-V12-D-123 | Provide SM-SVC-23 WF01–WF04 (§11.4.5.12); duplicate-notice guard; churn advisory only (DEC-383) | SVC-23 | P1 | D-1, D-2 (WF04) | TC-V12-D-123 |
| FR-V12-D-124 | Provide SM-SVC-24 WF01–WF04 (§11.4.5.13); forecasts labelled estimates; default attribution last non-direct | SVC-24 | P1 | D-1, D-2 (WF04) | TC-V12-D-124 |
| FR-V12-D-125 | Provide SM-SVC-25 WF01–WF04 (§11.4.5.14); contradiction holds; no cross-client retrieval | SVC-25 | P0 | D-1, D-2 (WF04) | TC-V12-D-125 |
| FR-V12-D-126 | Specify SM-SVC-26 WF01–WF04 (§11.4.5.15) and keep them disabled until the Founder decides CONFLICT-815 | SVC-26 | Pending Founder | D-4 | TC-V12-D-126 |
| FR-V12-D-127 | Provide SM-SVC-27-WF04 and the text part of WF03; keep WF01, WF02 and synthetic audio disabled pending CONFLICT-819 | SVC-27 | P1 / Pending Founder | D-1 (WF04), D-3, D-4 | TC-V12-D-127 |
| FR-V12-D-128 | Provide SM-SVC-28-WF01 (machine-readable catalogue) and WF02 (quote drafts for verified external agents, released only after human approval); keep WF03–WF04 disabled pending CONFLICT-816 | SVC-28 | P2 / Pending Founder | D-3, D-4 | TC-V12-D-128 |
| FR-V12-D-129 | Provide SM-SVC-29 WF01–WF04 (§11.4.5.18) on WF-25/WF-27 with DEC-392 channel rules | SVC-29 | P1 | D-2 | TC-V12-D-129 |
| FR-V12-D-130 | Provide SM-SVC-30 WF01–WF04 (§11.4.5.19); offer arms only from approved price-book revisions; no sensitive inference | SVC-30 | P1 | D-3 | TC-V12-D-130 |
| FR-V12-D-131 | Provide SM-SVC-31 WF01–WF04 (§11.4.5.20); listing prices only from approved price-book revisions; idempotent marketplace events; settlement reconciliation | SVC-31 | P2 | D-3 | TC-V12-D-131 |
| FR-V12-D-132 | Provide SM-SVC-32 WF01–WF04 (§11.4.5.21); partners see only their own records; commission record-only | SVC-32 | P1 | D-2 | TC-V12-D-132 |
| FR-V12-D-133 | Provide SM-SVC-33 WF01–WF04 (§11.4.5.22); self-service only from an allowlisted reversible catalogue | SVC-33 | P1 | D-1, D-2 | TC-V12-D-133 |
| FR-V12-D-134 | Provide SM-SVC-34 WF01–WF04 (§11.4.5.23); product events only via ADR-105; no automatic plan change or charge | SVC-34 | P2 | D-3 | TC-V12-D-134 |
| FR-V12-D-135 | Provide SM-SVC-35 WF01–WF04 (§11.4.5.24); no review generation or incentives; humans post responses | SVC-35 | P2 | D-3 | TC-V12-D-135 |
| FR-V12-D-136 | Provide SM-SVC-36 WF01, WF02, WF04 and the written-notes path of WF03 (§11.4.5.25); outputs private to the learner; recordings disabled pending CONFLICT-818 | SVC-36 | P1 / Pending Founder | D-2, D-4 | TC-V12-D-136 |
| FR-V12-D-137 | Provide SM-SVC-37 WF01 and WF04 as deterministic analytics (§11.4.5.26); keep WF02–WF03 disabled pending CONFLICT-817 | SVC-37 | P2 / Pending Founder | D-3, D-4 | TC-V12-D-137 |
| FR-V12-D-138 | Provide SM-SVC-38 WF01–WF04 (§11.4.5.27) after Release 2 with DLT header/template registration and NCPR/DND scrub as activation gates | SVC-38 | P2 | D-3 | TC-V12-D-138 |
| FR-V12-D-139 | Provide SM-SVC-39 WF01–WF04 (§11.4.5.28); purchase orders only after human approval within DEC-038 thresholds; payables separate from receivables | SVC-39 | P2 | D-3 | TC-V12-D-139 |

### 11.4.5.31 User stories and acceptance criteria

Stories use the epics of Part 0 §0.10.2; services in new domains are temporarily homed to the nearest epic (ASSUMPTION-826) until group R2 confirms EP-22+.

| Story | As a … I want … so that … | FR | Points (range) |
|---|---|---|---|
| US-18-YD01 | As an Automation Lead (R11), I want every V12 workflow registered under its literal ID with its schema and handler manifest, so that only complete, approved revisions can run | FR-V12-D-001, 003 | 5–8 |
| US-18-YD02 | As a Requester, I want my run input validated against the workflow DTO with field-level errors, so that invalid requests never reach a model or provider | FR-V12-D-002, 023 | 3–5 |
| US-18-YD03 | As a Reviewer, I want approvals bound to the exact payload, amount, policy version and expiry, so that what I approved is exactly what executes | FR-V12-D-009, 026 | 5–8 |
| US-18-YD04 | As an SRE, I want checkpoints, heartbeats and a reaper, so that a crashed worker never repeats a completed effect | FR-V12-D-004, 005, 006 | 5–8 |
| US-18-YD05 | As an Automation Lead, I want five trigger kinds with misfire policy and reviewer approval, so that schedules and events start exactly one eligible run | FR-V12-D-010, 011, 016, 017 | 8–13 |
| US-18-YD06 | As an operator in A110, I want the V12 run states and a timeline with reservations, actuals and uncertain outcomes, so that I can see why any run is waiting | FR-V12-D-018 | 5–8 |
| US-18-YD07 | As a tenant, I want fair scheduling and a budget hierarchy, so that another tenant's load or my own runaway workflow cannot exhaust shared capacity or money | FR-V12-D-019, 020, 028 | 8–13 |
| US-18-YD08 | As an Automation Lead, I want parallel read branches with joins, so that independent evidence steps finish sooner without parallel effects | FR-V12-D-021 | 3–5 |
| US-18-YD09 | As a Tenant Administrator (R12), I want to pause and re-cadence my schedules within policy, so that automation fits my business hours | FR-V12-D-022 | 3–5 |
| US-18-YD10 | As a Product Owner, I want templates as parameter sets and KPIs registered per workflow, so that 25 customers can be configured without cloning definitions and outcomes are measurable | FR-V12-D-013, 014, 015, 024, 025, 027 | 5–8 |
| US-15-YD01 | As a Finance Maker (R08), I want payment evidence imported, allocated and reconciled by SVC-21, so that closure rests on verified money without the platform moving any | FR-V12-D-121 | 8–13 |
| US-16-YD01 | As a Startup Head (R02), I want onboarding plans, pilot readiness and adaptive due dates from SVC-22, so that handover is on time without health data | FR-V12-D-122 | 5–8 |
| US-16-YD02 | As a Growth Manager (R03), I want renewal reminders, feedback analysis and retention actions from SVC-23, so that renewals are timely and never duplicated | FR-V12-D-123 | 5–8 |
| US-17-YD01 | As Finance (R08), I want attribution, forecast scenarios and calibration from SVC-24, so that revenue reporting is reconciled and forecasts are honest estimates | FR-V12-D-124 | 5–8 |
| US-02-YD01 | As Compliance (R10), I want document intake, grounding, expiry tracking and contradiction holds from SVC-25, so that no output relies on stale or conflicting knowledge | FR-V12-D-125 | 5–8 |
| US-08-YD01 | As the Founder (R01), I want SVC-26 fully specified but disabled, so that I can decide on voice with a complete design in front of me | FR-V12-D-126 | 1–2 |
| US-11-YD01 | As a Marketing Lead (R05L), I want every creative checked for rights, brand and claims by SVC-27-WF04, so that nothing unverified is published | FR-V12-D-127 | 3–5 |
| US-13-YD01 | As a Sales Lead (R03L), I want verified external AI agents to read our approved catalogue and receive quote drafts I approve, so that agent-driven buyers can be served safely | FR-V12-D-128 | 8–13 |
| US-06-YD01 | As a Growth Manager, I want account selection, buying-group maps and coordinated plays from SVC-29, so that enterprise accounts are pursued with consent-safe journeys | FR-V12-D-129 | 5–8 |
| US-12-YD01 | As a Marketing Lead, I want funnel analysis and pre-registered experiments from SVC-30, so that conversion changes are proven before rollout | FR-V12-D-130 | 5–8 |
| US-14-YD01 | As an Order Coordinator (R07), I want marketplace listings, inventory, orders and settlements synchronised by SVC-31, so that marketplace sales reconcile to our ledger | FR-V12-D-131 | 13–21 |
| US-16-YD03 | As a Startup Head, I want partner recruitment, enablement, deal registration and performance evidence from SVC-32, so that partner selling is fair and auditable | FR-V12-D-132 | 5–8 |
| US-20-YD01 | As a support lead, I want cases created, triaged, resolved and SLA-monitored by SVC-33, so that customers get grounded answers on time | FR-V12-D-133 | 8–13 |
| US-20-YD02 | As a Growth Manager, I want usage, activation and expansion signals from SVC-34, so that I recommend upgrades without automatic charges | FR-V12-D-134 | 5–8 |
| US-11-YD02 | As a Marketing Lead, I want authorized reviews monitored, classified and answered with human-posted drafts by SVC-35, so that reputation issues are handled honestly | FR-V12-D-135 | 8–13 |
| US-21-YD01 | As a salesperson, I want playbooks, practice and private coaching from SVC-36, so that I improve without being evaluated by an AI | FR-V12-D-136 | 5–8 |
| US-13-YD02 | As Finance, I want margin and pricing-policy monitoring from SVC-37 using deterministic analytics only, so that pricing stays a human decision | FR-V12-D-137 | 3–5 |
| US-08-YD02 | As a Marketing Lead, I want DLT-compliant SMS/RCS campaigns with STOP handling from SVC-38 after Release 2, so that a mobile channel is available lawfully | FR-V12-D-138 | 8–13 |
| US-14-YD02 | As an Order Coordinator, I want supplier qualification, RFQ comparison, approved POs and supplier performance from SVC-39, so that buying is controlled end to end | FR-V12-D-139 | 8–13 |

```gherkin
Feature: V12 executable workflow engine (US-18-YD01 … US-18-YD10)

  Scenario: US-18-YD01 an unbound step blocks activation
    Given workflow "SM-SVC-21-WF02" revision 3 lacks a handler for "SM-SVC-21-WF02-STEP-03"
    When R11 requests activation
    Then activation is refused with "HANDLER_MISSING" naming the step
    And the revision stays "validated"

  Scenario: US-18-YD02 invalid input returns field pointers
    Given workflow "SM-SVC-21-WF01" is active and entitled
    When a run is requested with "currency" = "inr" and an extra property "note"
    Then the response is 422 with pointers "/input/currency" and "/input/note"
    And no reservation, outbox row or model call exists for the request

  Scenario: US-18-YD03 a changed payload voids the mandate
    Given reviewer "R09" approved digest D1 for "SM-SVC-39-WF03-STEP-03"
    When the purchase order total changes before dispatch
    Then the effect is not dispatched and the run returns to "AWAITING_APPROVAL" with "MANDATE_DIGEST_MISMATCH"

  Scenario: US-18-YD04 crash after checkpoint does not repeat an effect
    Given step "SM-SVC-38-WF02-STEP-02" committed its receipt checkpoint
    When the worker dies before acknowledging the task
    Then the reaper reclaims the step after 90 seconds
    And the provider receives no second send for the same idempotency key

  Scenario: US-18-YD05 misfire never bursts
    Given a daily trigger with misfire_policy "reschedule_once" missed 3 fire times during an outage
    When Celery Beat resumes
    Then exactly one catch-up run starts and "MISFIRE_RECOVERED" is recorded once

  Scenario: US-18-YD06 unknown actual cost is shown as unknown
    Given a run whose provider returned no cost for an effect step
    When the operator opens the A110 timeline
    Then the step shows actual cost "unknown" not "0" and the run total is labelled "incomplete"

  Scenario: US-18-YD07 a noisy tenant cannot starve another
    Given tenant A queues 5,000 runs and tenant B queues 10 runs on queue "ai" with equal weights
    When the scheduler drains for 10 minutes
    Then tenant B's 10 runs start before tenant A's 100th run

  Scenario: US-18-YD07 budget exhaustion at any level holds the run
    Given the workflow-level unit cap for "SM-SVC-38-WF02" is reached but the tenant cap is not
    When a new run is requested
    Then the run is "HELD" with "BUDGET_EXHAUSTED" at level "workflow" and no partial reservation remains

  Scenario: US-18-YD08 cancel propagates to parallel branches
    Given a run with two parallel evidence branches in progress
    When the run is cancelled
    Then both branches stop, the join never fires and unused reservations are released

  Scenario: US-18-YD09 tenant pause stops new runs only
    Given R12 pauses the schedule of "SM-SVC-23-WF01"
    When the next fire time passes
    Then no run starts and runs already in "AWAITING_APPROVAL" keep their state

  Scenario: US-18-YD10 templates do not clone definitions
    Given 25 customer configurations are created from template "renewal-standard"
    When the registry is listed
    Then the definition count for SM-SVC-23 remains 4 and each configuration references the same revision
```

```gherkin
Feature: V12 services SM-SVC-21 … SM-SVC-39 (service stories)

  Scenario: US-15-YD01 over-allocation is rejected and money never moves
    Given invoice I1 has an outstanding balance of 50000 minor units
    When SM-SVC-21-WF02 allocates a verified payment of 60000 minor units
    Then STEP-02 returns "POLICY_DENIED" with "OVER_ALLOCATION" and the run is "BLOCKED"
    And no adapter call to any bank or payment provider exists for the run

  Scenario: US-16-YD01 pilot readiness rejects health data
    Given a MedMaarg pilot readiness input that contains a field classified "health"
    When SM-SVC-22-WF02 runs
    Then STEP-01 blocks with "RESTRICTED_DATA_CLASS" and no model call is made

  Scenario: US-16-YD02 duplicate renewal notice is suppressed
    Given a renewal reminder for R1 was dispatched in the current window
    When SM-SVC-23-WF01 runs again for R1
    Then STEP-04 marks the notice duplicate and no second message is queued

  Scenario: US-17-YD01 forecast carries the estimate label
    When SM-SVC-24-WF02 completes
    Then the report is labelled "estimate" and is never summed with verified revenue

  Scenario: US-02-YD01 contradiction holds affected outputs
    Given claim C1 conflicts with an approved document revision
    When SM-SVC-25-WF04 runs
    Then drafts that cite C1 move to "HELD" until R10 resolves the correction

  Scenario: US-08-YD01 voice stays disabled
    When any SM-SVC-26 workflow is requested in live or simulation mode
    Then the run is "BLOCKED" with "FOUNDER_DECISION_PENDING" and no telephony adapter is loaded

  Scenario: US-11-YD01 unknown rights block publication
    Given a creative whose rights_state is "unknown"
    When SM-SVC-27-WF04 STEP-03 evaluates it
    Then the asset is held and cannot be referenced by any publication

  Scenario: US-13-YD01 external agent receives only an approved quote
    Given verified external agent X with scope "request_quote"
    When X submits a requirement for an approved offering
    Then SM-SVC-28-WF02 creates a quote draft priced by AU-089 from the active price book
    And nothing is returned to X until R03L approves the exact quote digest

  Scenario: US-06-YD01 ineligible committee member is excluded from journeys
    Given buying-group member M has only a role hypothesis and no eligible channel
    When SM-SVC-29-WF03 builds the journey
    Then M appears only as a human research task, never as an automated recipient

  Scenario: US-12-YD01 offer arm with unapproved price is rejected
    When an experiment arm references a price revision that is not approved
    Then SM-SVC-30-WF02 STEP-02 blocks with "PRICE_NOT_APPROVED"

  Scenario: US-14-YD01 marketplace event duplicates have one effect
    Given marketplace event E7 was processed
    When E7 is delivered again
    Then SM-SVC-31-WF03 STEP-01 returns the existing order_event_ref and changes no order state

  Scenario: US-16-YD03 partner sees only own registrations
    When partner P requests deal registrations
    Then only registrations created by P are returned and commission figures are read-only records

  Scenario: US-20-YD01 non-allowlisted self-service escalates
    Given a proposed fix "change billing plan" that is not in the self-service catalogue
    When SM-SVC-33-WF02 STEP-03 runs
    Then the case is escalated to a human and no account change is made

  Scenario: US-20-YD02 upgrade recommendation never charges
    When SM-SVC-34-WF04 recommends an upgrade
    Then no subscription change or invoice is created and the recommendation is a draft for R03L

  Scenario: US-11-YD02 no generated reviews
    When any SM-SVC-35 step is asked to create a customer review
    Then the request is refused with "PROHIBITED_CONTENT" and logged

  Scenario: US-21-YD01 coaching stays private
    Given a manager requests learner L's practice report
    Then access is denied and the report remains visible only to L

  Scenario: US-13-YD02 pricing analytics proposes no price
    When SM-SVC-37-WF01 completes
    Then the output contains margins and flags but no recommended price field

  Scenario: US-08-YD02 SMS needs a registered DLT template
    Given template T has dlt_status "pending"
    When SM-SVC-38-WF02 tries to dispatch with T
    Then STEP-01 blocks with "DLT_TEMPLATE_NOT_APPROVED"

  Scenario: US-14-YD02 PO above authority is held
    Given approver R08 has a DEC-038 threshold of 200000 INR
    When a purchase order of 250000 INR is submitted for approval by R08
    Then SM-SVC-39-WF03 holds the order for the next approver tier and records no commitment
```

### 11.4.5.32 Test cases (TC-V12-D)

**Engine tests (one per engine FR).**

| TC | Title | FR | Level | Preconditions → steps → expected | Priority |
|---|---|---|---|---|---|
| TC-V12-D-001 | Registry validates 76 IDs and rejects unapproved revision | 001 | Integration | Load registry fixture; start run on draft revision → 409 `WORKFLOW_NOT_ACTIVE`; 76/76 IDs match `^SM-SVC-\d{2}-WF0[1-4]$` | P0 |
| TC-V12-D-002 | DTO v2/v3 validation and CI meta-schema check | 002 | Unit + CI | 76 schemas valid 2020-12; invalid fixtures → 422 with pointers; non-produced output null accepted; produced output null rejected | P0 |
| TC-V12-D-003 | Handler manifest completeness gate | 003 | Integration | Remove one STEP binding → activation refused `HANDLER_MISSING` | P0 |
| TC-V12-D-004 | Checkpoint, heartbeat, reaper | 004 | Chaos (staging) | Kill worker after checkpoint → resume next step; kill during effect → RECONCILING; no duplicate provider call | P0 |
| TC-V12-D-005 | Idempotency key and finalize atomicity | 005 | Integration | Same key twice → same result; fault inject at finalize → no partial artifact, reservation intact | P0 |
| TC-V12-D-006 | Retry classes | 006 | Unit | Validation error never retried; 503 read retried ≤ 3 with jitter; 429 honours Retry-After; timeout on write → RECONCILING | P0 |
| TC-V12-D-007 | Preflight order and dry run | 007 | Integration | Each of the 9 checks failing in turn yields its state and reason; dry run → plan with zero egress and zero reservations | P0 |
| TC-V12-D-008 | Confidence routing | 008 | Integration | Classifier output 0.62 < floor 0.80 → AWAITING_APPROVAL `LOW_CONFIDENCE`; no effect step reached | P0 |
| TC-V12-D-009 | Mandate binding | 009 | Integration + security | Self-approval refused; digest change, expiry, revocation and stricter policy each block dispatch | P0 |
| TC-V12-D-010 | Inbox dedupe and provider callback | 010 | Integration + security | Duplicate webhook → one run; bad signature → rejected; replay beyond 300 s → rejected; scope mismatch → rejected | P0 |
| TC-V12-D-011 | Child workflow dependency | 011 | Integration | Unentitled child → HELD `DEPENDENCY_UNMET`, parent continues; cycle at activation refused; depth 4 refused | P1 |
| TC-V12-D-012 | Cancellation and compensation | 012 | Integration | Cancel releases reservation; reversible grant compensated after approval; irreversible effect → RECONCILING + owner task | P0 |
| TC-V12-D-013 | Template parameter sets | 013 | Integration | 2 businesses and 25 configurations → definition count unchanged (MT-TC-MT-29, MT-TC-MT-34); untested template cannot publish | P1 |
| TC-V12-D-014 | Acceptance record for AI outputs | 014 | Integration | Accepted output has schema, evidence, confidence, policy and evaluator version; low-quality fixture held (OPT-TC-FL-13) | P0 |
| TC-V12-D-015 | Optimization recommendations | 015 | Integration | Ranking uses run ledger; recommendation has baseline, test result, expected impact; nothing auto-applied (OPT-TC-FL-14) | P2 |
| TC-V12-D-016 | Misfire policy | 016 | Integration (virtual clock) | skip → no run; reschedule_once → exactly one; DST transition in Asia/Kolkata and Europe/London fixtures | P0 |
| TC-V12-D-017 | Trigger lifecycle | 017 | Integration | Enable without test evidence refused; reviewer = requester refused; invalid cron refused (REC-01) | P0 |
| TC-V12-D-018 | State model v2 and timeline | 018 | Integration | Concurrent transitions → one wins, other 409; terminal update refused; adjustment record created; legacy view returns old names | P0 |
| TC-V12-D-019 | Fair scheduler | 019 | Load (staging) | Noisy-tenant fixture: tenant B p95 queue wait ≤ 2× its solo baseline (OPT-TC-ST-03, MT-TC-MT-28) | P0 |
| TC-V12-D-020 | Budget hierarchy | 020 | Integration | Exhaust workflow, then service, then tenant level → HELD at the right level; invalid currency/schedule held (MT-TC-MT-30) | P0 |
| TC-V12-D-021 | Parallel DAG | 021 | Integration | Two read branches join; dependent step waits; cancel propagates; effect node inside a parallel block rejected at validation (OPT-TC-FL-06) | P1 |
| TC-V12-D-022 | Customer schedule controls | 022 | Integration + UI | Pause prevents new runs; consent gates still enforced; cadence outside template set refused (OPT-TC-RT-08) | P1 |
| TC-V12-D-023 | Run form and walkthrough | 023 | UI (WCAG 2.2 AA) | Form generated from schema with labels and errors announced; walkthrough next/previous/restart works by keyboard | P1 |
| TC-V12-D-024 | Node contracts | 024 | Unit | Handler not run when its input schema or effect policy fails; `logic.reconcile` writes only W1 state | P1 |
| TC-V12-D-025 | Historical labels | 025 | Unit | Label stored; no historical entry objects exist | P2 |
| TC-V12-D-026 | Authority mapping | 026 | Unit + integration | R3 run requesting L3 mandate → BLOCKED `AUTHORITY_DENIED`; R2 routine reminder under approved template allowed | P0 |
| TC-V12-D-027 | KPI registry | 027 | Integration | Each of the 76 workflows has ≥ 1 KPI with numerator, denominator and source; KPI marked "baseline pending pilot" | P1 |
| TC-V12-D-028 | Usage metering and unit caps | 028 | Integration | Completed run writes usage units and actual cost; 501st SMS attempt in a 500-unit pilot month → HELD | P0 |

**V12 acceptance archetypes (applied to every workflow; 660 V12 IDs + 76 AT01 = 736 instances).**

| TC | V12 family | Applies to | Expected result (pass criteria) |
|---|---|---|---|
| TC-V12-D-101 | `-TC-POS` | All 76 | Valid fixture, entitled, within budget → COMPLETED; result validates the v3 projection; KPI sample recorded; in simulation zero external calls |
| TC-V12-D-102 | `-TC-INPUT` | All 76 | Missing required field, extra property, wrong pattern → BLOCKED `INPUT_INVALID` with pointers; no reservation |
| TC-V12-D-103 | `-TC-SCOPE` | All 76 | Reference from another tenant or company → BLOCKED `SCOPE_DENIED`; response reveals nothing about the foreign object; audit row |
| TC-V12-D-104 | `-TC-ENT` | All 76 | Service not entitled → HELD `ENTITLEMENT_MISSING`; unentitled child → `DEPENDENCY_UNMET` |
| TC-V12-D-105 | `-TC-DUP` | All 76 | Same idempotency key → same run; duplicate event → one run; duplicate effect → one provider call |
| TC-V12-D-106 | `-TC-QUALITY` | All 76 | Low-confidence or claim-failing fixture → AWAITING_APPROVAL; for deterministic-only workflows, malformed metric input → HELD `INVALID_METRIC` |
| TC-V12-D-107 | `-TC-BUDGET` | All 76 | Exhausted level → HELD `BUDGET_EXHAUSTED`; no partial reservation |
| TC-V12-D-108 | `-TC-RECOVERY` | All 76 | Crash after checkpoint resumes; emergency stop → HELD within 60 s (E-7); retry cap respected |
| TC-V12-D-109 | `-TC-APPROVAL` | 26 R2/R3 | Self-approval refused; changed digest, expiry, revocation and stricter policy block the effect or state change |
| TC-V12-D-110 | `-TC-EFFECT` | 26 R2/R3 | Provider timeout → RECONCILING, no retry before reconciliation; dispatch recheck denies revoked consent; simulation egress = 0 |
| TC-V12-D-111 | `-AT01` (source acceptance, "not run") | All 76 | Executed as TC-V12-D-101 on the source fixture; result recorded as the first evidence for the V12 acceptance ID |

**Service safety tests.**

| TC | Service | Test | Expected |
|---|---|---|---|
| TC-V12-D-121 | SVC-21 | Over-allocation; closure without R09 check; any adapter call | Blocked; no closure; zero money-movement calls |
| TC-V12-D-122 | SVC-22 | Health-class field in pilot input; reminder with unapproved template | Blocked `RESTRICTED_DATA_CLASS`; reminder held |
| TC-V12-D-123 | SVC-23 | Duplicate notice; suppressed contact; churn score used in eligibility | Suppressed; held; churn never reaches PDP inputs (DEC-383) |
| TC-V12-D-124 | SVC-24 | Missing currency; forecast summed with actuals | `INVALID_METRIC` hold; summation refused |
| TC-V12-D-125 | SVC-25 | Contradiction; cross-client retrieval attempt | Outputs held; retrieval returns only own startup chunks |
| TC-V12-D-126 | SVC-26 | Any run in any mode | BLOCKED `FOUNDER_DECISION_PENDING`; adapter not loaded |
| TC-V12-D-127 | SVC-27 | Unknown rights; WF01/WF02 run | Held; blocked pending Founder |
| TC-V12-D-128 | SVC-28 | Unverified agent; quote release before approval; WF03/WF04 run | 401/403; nothing released; blocked pending Founder |
| TC-V12-D-129 | SVC-29 | Committee member without eligible channel; LinkedIn automated step | Human task only; automated step rejected (DEC-392) |
| TC-V12-D-130 | SVC-30 | Unapproved price arm; segment using sensitive attribute | `PRICE_NOT_APPROVED`; `SENSITIVE_INFERENCE` block |
| TC-V12-D-131 | SVC-31 | Listing price ≠ approved revision; duplicate order event; settlement mismatch | Blocked; one effect; exception report |
| TC-V12-D-132 | SVC-32 | Partner reads another partner's registration; commission edited | 404; edit refused (record-only) |
| TC-V12-D-133 | SVC-33 | Non-allowlisted self-service; SLA breach | Escalated; breach escalation within 1 scheduler tick |
| TC-V12-D-134 | SVC-34 | Non-allowlisted product event; recommendation creates charge | Rejected at ingress; no charge object |
| TC-V12-D-135 | SVC-35 | Request to generate a review; auto-post response | Refused; human post required |
| TC-V12-D-136 | SVC-36 | Manager reads learner report; recording as input | Denied; recording rejected (DEC-386) |
| TC-V12-D-137 | SVC-37 | Output containing a recommended price; WF02/WF03 run | Schema rejects field; blocked pending Founder |
| TC-V12-D-138 | SVC-38 | Pending DLT template; STOP received; quiet hours | Blocked; queued sends cancelled (AU-008); deferred |
| TC-V12-D-139 | SVC-39 | PO above approver threshold; duplicate PO; over-receipt | Held for next tier; one PO; over-receipt rejected |

### 11.4.5.33 Effort and cost (separately approvable; outside DEC-230, DEC-231 and DEC-422)

**Basis.** Part 8.4 rate ₹4,545–6,818 per person-day (22 working days, BRD §6). Per-workflow effort: already-built behaviour (P/C) 1.5–3 pd for handler binding, DTO v3 projection, KPI registration and the archetype fixtures; new workflow (N) 4–8 pd; conflict workflow if approved 6–12 pd. Adapters: marketplace 8–15 pd, SMS/RCS 6–12 pd, ERP/PO export 4–8 pd, external-agent gateway (catalogue publication and quote intake, read/draft scopes only) 10–18 pd. Common engine (FR-V12-D-001…028): registry 5–8, DTO registry 6–10, executor contracts and preflight and mandates 8–13, envelope/inbox/triggers 6–10, state model v2 and timeline 6–10, fair scheduler and budget hierarchy and heartbeats and parallel DAG 10–16, archetype test harness 8–14 = **49–81 pd**. All figures are estimates.

**Development (one-time).**

| Package | Content | Person-days | ₹ (lakh) | Timing proposal |
|---|---|---|---|---|
| CR-V12-D-1 | Common engine (49–81 pd) + alignment of the 19 workflows already in Release 1/2 scope (19 × 1.5–3 pd) | 77.5–138 | 3.52–9.41 | Before the Release 2 build gate (Day 208), using contract-engineer days as in DEC-416 |
| CR-V12-D-2 | Advanced A1: 16 workflows with existing behaviour (1.5–3 pd) + SVC-22-WF04 (4–8 pd) | 28–56 | 1.27–3.82 | With release A1 (DEC-417) |
| CR-V12-D-3 | A2/A3: 14 existing-behaviour workflows (21–42), 14 new workflows (56–112), SVC-27-WF03 text part (2–4), adapters marketplace + SMS/RCS + ERP + agent gateway (28–53) | 107–211 | 4.86–14.39 | Gate G-A1 / G-A2 (DEC-411) |
| **Subtotal D-1…D-3** | | **212.5–405** | **9.66–27.61** | |
| CR-V12-D-4 | Only if the Founder approves CONFLICT-815…819: 11 conflict workflows (6–12 pd) + voice and generative-media adapters (20–40) | 86–172 | 3.91–11.73 | Not before A3 |

**Running (recurring, pilot month), estimates; provider prices verify at time of implementation (as of 27 Nov 2026).**

{{AICOST}}

| Line | Basis | ₹ / month |
|---|---|---|
| AI model calls for SVC-21…39 (blueprint estimate above) | Pilot units ÷ 4 workflows × per-run model estimate; includes the disabled conflict workflows, so an upper bound | ≈ 1,476 (V12 illustrative ≈ 2,593) |
| SMS/RCS (SVC-38) | 500 attempts × ₹0.15–0.30 per SMS + DLT/header fees amortised ₹0–500 (verify) | 75–650 |
| External-agent gateway (SVC-28-WF01/02) | Small container on existing AWS compute | 300–900 |
| Worker, database and storage growth (registry, inbox, artifacts, timeline) | Incremental share of DEC-421 hosting lines | 400–1,200 |
| Marketplace and ERP connectors | Seller APIs and CSV/SFTP export; marketplace fees are the tenant's business cost (verify) | 0 |
| **Subtotal** | | **2,251–4,226** |
| 15% contingency | | 338–634 |
| **Total recurring proposal** | | **2,589–4,860** |
| CR-V12-D-4 only (if approved) | Voice 100 min: telephony ₹0.6–1.5/min + speech ₹1–3/min + number rental ₹300–800; media 50 assets × ₹4–20 (verify) | 660–2,250 |

**Fit with AI ceilings.** The baseline catalogue costs ≈ ₹1,150/month at base against the DEC-008 pilot ceiling of ₹3,000 (Part 7.3). Adding ≈ ₹1,476 brings AI to ≈ ₹2,626 (88%); the recommendation is a separate hard-capped sub-line (B25 "V12 workflows", ₹1,500 pilot) degrading to Tier 3 before any baseline agent is throttled, mirroring DEC-409. This is part of the Founder funding decision (CONFLICT-820).

### 11.4.5.34 Architecture decision records ADR-196…199

| ADR | Title | Decision | Alternatives rejected | Consequences | Status |
|---|---|---|---|---|---|
| ADR-196 | Canonical event envelope v2 and an inbox table | Adopt V12 envelope v2 for all domain, trigger and run events with Part 3.2 aliases for one major; add `ops_inbox` symmetric to `ops_outbox` | Keep Part 3.2 envelope and map at the edge (loses workflow/service identity); streaming broker now (DEC-401 sets the volume trigger) | + workflow-level correlation and approval refs on every event; − one migration of consumers | Proposed (Customer revision V12) |
| ADR-197 | Run and step state model v2 | V12 states canonical; legacy view for old names; terminal immutability with adjustment records | Keep blueprint names and translate in the UI (two vocabularies in logs and APIs) | + one vocabulary with the customer; − RP-22/KPI views regenerated | Proposed (Customer revision V12) |
| ADR-198 | DTO schema registry with per-workflow projections | App. B v2 schemas registered immutable; v3 adds per-workflow `x-produces`, typed arrays and numeric companions | Free-form JSON payloads (FL-02 forbids); one schema per workflow written by hand (breaks the V12 literal schema) | + valid results for every workflow; − schema-generation tooling needed | Proposed (Customer revision V12) |
| ADR-199 | Fair scheduling and hierarchical budget reservation | DRR per (tenant, company) inside DEC-321 queues; five-level budget reservation in one transaction with fixed lock order | Separate queue per tenant (queue explosion); Kubernetes-style quotas (no Kubernetes in DEC-421 stack) | + isolation of noisy tenants and runaway workflows; − more scheduler state in Valkey/PostgreSQL | Proposed (Customer revision V12) |

## 11.4.6 Conflicts and proposed resolutions

| Tag | V12 says | Baseline says | Why it conflicts | Options | Recommended resolution | Status |
|---|---|---|---|---|---|---|
| CONFLICT-814 | R3 workflows: "L2 mandatory approved effect; **L3 only with separately approved bounded mandate where lawful**" (10 workflows: SVC-21-WF01/02, 28-WF03/04, 30-WF02, 31-WF02/03, 32-WF04, 37-WF03, 39-WF03) | DEC-064: money movement not supported; contracts, quotes, discounts, bids, legal terms L1 maximum; V11 invariant "consequential actions capped at L1" | A standing mandate lets future financial or commitment actions execute without a per-item human approval | (a) adopt L3 mandates; (b) keep L1 per item; (c) allow L3 only for record-keeping steps with no external commitment | **(b) with (c):** V12 L2 = blueprint L1 per item; record-only internal steps may run at L3 when deterministic. V12 R3 default (L2) is fully honoured | Pending Founder decision (DEC-577) |
| CONFLICT-815 | SVC-26 AI voice: inbound AI answering, outbound AI calls, multilingual voice booking, permitted transcription | DEC-387 voice deferred (Won't this horizon, A3 re-evaluation via PG gates); DEC-218/DEC-386 recordings and transcripts excluded; DEC-392 calls human-dialled only; TR-R1 no voice outreach W0–W5 | Founder decisions and privacy controls | (a) adopt now; (b) defer to A3 with gates; (c) never | **(b):** keep the full specification; disabled; A3 evaluation via PG-01…PG-10 with self-hosted vs paid speech benchmark, TRAI/DND and recording-consent design, DPIA; outbound stays human-dialled; no transcripts until legal review | Pending Founder decision (DEC-572) |
| CONFLICT-816 | SVC-28 agent-assisted negotiation mandates (WF03) and authorized transaction/payment mandates (WF04) | Invariant: AI never signs, pays, submits or sets prices; DEC-064 money movement not supported; DEC-395 no AI price values | Machine-negotiated terms and payment mandates are consequential actions without a per-item human | (a) adopt; (b) WF01–WF02 only (catalogue, quote drafts released by a human); (c) defer all | **(b):** catalogue publication and approved quote drafts only; negotiation and payment stay human; transaction outcomes recorded and reconciled (record-only) | Pending Founder decision (DEC-573) |
| CONFLICT-817 | SVC-37 price-sensitivity scenarios (WF02) and live pricing/promotion experiments (WF03) | CI-071 excluded price recommendation; DEC-388 AI never proposes or computes a price; DEC-395 approved price books only | Scenario outputs become price recommendations; experiments change prices customers see | (a) adopt; (b) deterministic analytics only (WF01, WF04); (c) allow experiments only between two human-approved price-book revisions with Finance sign-off | **(b) now, (c) as a later Founder option**; no AI-generated price value in any case | Pending Founder decision (DEC-574) |
| CONFLICT-818 | SVC-36-WF03 coaching from permitted sales meetings and conversations; channel includes Voice; "review recordings and training outputs" | DEC-218 recordings/transcripts excluded; DEC-386 written notes only, no employee evaluation | Recordings are excluded data | (a) adopt; (b) written notes only | **(b):** coach on staff-written notes and in-product threads; learner-private outputs | Pending Founder decision (DEC-575) |
| CONFLICT-819 | SVC-27 image, video and synthetic audio generation (WF01, WF02, WF03 audio) | CI-061 excluded image generation (cost, likeness, claims); DEC-418 model strategy is Claude text models; budgets DEC-422 | Needs a new paid multimodal provider, likeness/consent policy and budget | (a) adopt with a provider; (b) brand-asset composition only; (c) defer | **(b) now; (a) at A2 gate** after PG-01…PG-10, matched benchmark, likeness and rights policy, budget line | Pending Founder decision (DEC-576) |
| CONFLICT-820 | 76 workflows with typed contracts, a common engine upgrade and new adapters | Approved budgets DEC-230/231/422 and staffing DEC-228 do not include V12 work | Development ₹9.66–27.61 L (+ ₹3.91–11.73 L if D-4) and ₹2,589–4,860/month recurring are outside the approved figures | (a) fund D-1…D-3 as proposed; (b) fund D-1 only now; (c) defer | **(b) now** (engine + Release 1/2 alignment, protects the Release 2 build), D-2 with A1, D-3 at G-A1/G-A2 | Pending Founder decision (DEC-578) |

## 11.4.7 Decisions

| DEC | Decision | Authority | Effect |
|---|---|---|---|
| DEC-560 | V12 IDs `SM-SVC-21…39-WF01…04` and their 231 STEP IDs are canonical; blueprint WF-01…39 remain end-to-end journeys mapped in §11.4.4.1 | Customer revision V12 (28 Nov 2026) | Amends Part 9.4 catalogue keys; no WF renumbering |
| DEC-561 | Run/step state model v2 (V12 names) with optimistic transitions, terminal immutability, adjustment records and a legacy view; API-V2-RUN/RESULT/APPROVAL/CANCEL over `aut_run` | Customer revision V12 (28 Nov 2026) | Amends Part 2.3 §2.27.14 and Part 3.3 ENT-162/163 state CHECKs |
| DEC-562 | Seven V12 executor kinds bound to NT13 node types and failure codes to run states; handler manifest mandatory per STEP ID; `logic.reconcile` subtype added | Customer revision V12 (28 Nov 2026) | Extends Part 7.4b NT13 and `aut_step_run.error_class` (adds `reason_code`) |
| DEC-563 | Canonical event envelope v2 for all events; `ops_inbox` added | Customer revision V12 (28 Nov 2026) | Amends Part 3.2 §3.2.3.1 and Part 3.4 §3.4.5.2 E |
| DEC-564 | Five trigger kinds; misfire `skip` or `reschedule_once`, never burst; REC-01 draft fields; child depth ≤ 3 | Customer revision V12 (28 Nov 2026) | Amends ADR-028 wording, AU-028 and Part 3.3 ENT-161 |
| DEC-565 | App. B schemas registered as v2; v3 per-workflow projection, typed arrays and numeric companions; money as minor units at the workflow DTO boundary only | Customer revision V12 (28 Nov 2026) | Narrows ADR-030 to REST resources; adds `aut_dto_schema` |
| DEC-566 | V12 L0–L4 / R0–R3 mapped to blueprint L0–L3 with stricter-wins (§11.4.5.9) | Customer revision V12 (28 Nov 2026) | DEC-064 unchanged; V12 tightenings (e.g. SVC-23-WF01) adopted |
| DEC-567 | Fair scheduler (DRR per tenant/company), tenant bulkheads, five-level budget hierarchy, parallel read branches, heartbeats/reaper, tenant schedule controls | Customer revision V12 (28 Nov 2026) | Extends DEC-321 and AU-002 |
| DEC-568 | The 8/10 V12 acceptance families per workflow are mandatory release evidence (TC-V12-D-101…111); a workflow cannot be activated with a failing family | Customer revision V12 (28 Nov 2026) | Adds 736 test instances to the Part 6 suite |
| DEC-569 | One definition per workflow revision; templates are parameter sets; BusinessContext v1 stored on every run | Customer revision V12 (28 Nov 2026) | Amends A113 template semantics (FR-A113) |
| DEC-570 | Where V12 sources disagree on side effects, the FSD R-class governs and an approval gate is inserted before the state change (GAP-821) | Customer revision V12 (28 Nov 2026) | 13 workbook labels corrected; 16 workflows gain an approval gate |
| DEC-571 | SMS/RCS (SVC-38) adopted for activation after Release 2 only, with DLT header/template registration, NCPR/DND scrub and AU-008 STOP as activation gates; "no SMS or voice outreach in W0–W5" unchanged | Customer revision V12 (28 Nov 2026) | Extends TR-R1 control; funding under DEC-578 |
| DEC-572 | Resolution of CONFLICT-815 (voice): specify, keep disabled, A3 evaluation through PG gates | Pending Founder decision | Until decided, SVC-26 is `disabled_pending_founder` |
| DEC-573 | Resolution of CONFLICT-816 (agentic commerce): WF01–WF02 only; negotiation and payment human | Pending Founder decision | WF03–WF04 disabled |
| DEC-574 | Resolution of CONFLICT-817 (pricing): deterministic analytics only; experiments only between approved revisions if later approved | Pending Founder decision | WF02–WF03 disabled |
| DEC-575 | Resolution of CONFLICT-818 (coaching): written notes only | Pending Founder decision | Recording input rejected |
| DEC-576 | Resolution of CONFLICT-819 (generative media): brand-asset composition now; generation at A2 gate | Pending Founder decision | WF01, WF02, WF03 audio disabled |
| DEC-577 | Resolution of CONFLICT-814 (R3 mandates): L1 per item; L3 only for deterministic record-keeping | Pending Founder decision | `aut_mandate.scope` = single step |
| DEC-578 | Funding of CR-V12-D-1…3 (and D-4 if approved) outside DEC-230/231/422; recommended: D-1 now | Pending Founder decision | No V12-D spend before approval |
| DEC-579 | Marketplace (SVC-31) and procurement (SVC-39) adopted: listing prices only from approved price-book revisions; purchase orders are human-approved commitments within DEC-038 thresholds; payables separate from receivables | Customer revision V12 (28 Nov 2026) | Extends WF-10 and the OrganicSpec route (BR-S004) |

## 11.4.8 Expert persona review

| Persona | Question asked | Findings | Changes made |
|---|---|---|---|
| Principal Workflow/BPM Architect | Can every V12 workflow execute on one engine without per-workflow code? | Seven executor kinds map cleanly to NT13; "Reconcile" had no node type; 16 R2/R3 workflows lacked an approval point | `logic.reconcile` added; approval gate inserted (DEC-570); handler manifest mandatory |
| Event-driven Systems Architect | Is every start and every effect exactly-once in effect? | No inbox table; child workflows undefined; misfire could burst | `ops_inbox`, envelope v2, child kind with depth and cycle checks, misfire enum |
| QA Architect | Is every V12 acceptance ID executable? | 660 IDs with no definitions beyond family names; AT01 never run | Eleven archetypes with pass criteria; 736 instances; 28 engine and 19 service safety tests |
| Principal Engineer | Are contracts implementable and safe under concurrency? | Shared output schemas unusable; state names diverge; no fairness or budget hierarchy | DTO v3 projection; state model v2 with optimistic guard; DRR and fixed-order budget locks |
| Security / AI-Governance Lead | Does V12 weaken any invariant? | R3 L3 mandates, AI voice, payment mandates, price scenarios, recordings, generative media | Six CONFLICTs with disabled-by-default specs; Tier 2 never eligible |
| FinOps Lead | What does V12 cost and where does it sit? | No provider/retry/labour in V12 costs | Model estimate per workflow; separate one-time and recurring tables; B25 sub-line proposal |
| Product Owner | Do customers get value without waiting for Founder items? | 64 of 76 workflows are buildable within invariants | Packages D-1…D-3 sequenced to releases; conflicts isolated in D-4 |

## 11.4.9 Tags register

| Tag | Type | Section | Statement | Status |
|---|---|---|---|---|
| CONFLICT-814 | Conflict | 11.4.6 | V12 R3 "L3 bounded mandate" vs DEC-064 L1 cap | Pending Founder decision (DEC-577) |
| CONFLICT-815 | Conflict | 11.4.6 | SVC-26 AI voice vs DEC-387, DEC-218, DEC-386, DEC-392, TR-R1 | Pending Founder decision (DEC-572) |
| CONFLICT-816 | Conflict | 11.4.6 | SVC-28 negotiation and payment mandates vs "AI never pays, signs or sets prices" | Pending Founder decision (DEC-573) |
| CONFLICT-817 | Conflict | 11.4.6 | SVC-37 price sensitivity and pricing experiments vs CI-071, DEC-388, DEC-395 | Pending Founder decision (DEC-574) |
| CONFLICT-818 | Conflict | 11.4.6 | SVC-36-WF03 recordings vs DEC-218, DEC-386 | Pending Founder decision (DEC-575) |
| CONFLICT-819 | Conflict | 11.4.6 | SVC-27 generative media vs CI-061, DEC-418 model strategy, DEC-422 budget | Pending Founder decision (DEC-576) |
| CONFLICT-820 | Conflict | 11.4.6, 11.4.5.33 | V12 work outside approved budgets and staffing (DEC-228/230/231/422) | Pending Founder decision (DEC-578) |
| GAP-821 | Gap | 11.4.4.3 | 13 R2/R3 workflows labelled "internal" in the workbook; 16 R2/R3 without an effect step | Resolved by DEC-570 |
| GAP-822 | Gap | 11.4b.6.3 | No event-type catalogue for "validated upstream business event" triggers | Resolved: event types defined |
| GAP-823 | Gap | 11.4b.6.4 | No default cadence for scheduled triggers | Resolved: defaults defined, tenant-editable |
| GAP-824 | Gap | 11.4b.4 | Shared per-service DTO with all outputs required; untyped arrays; band-only metrics; open `interval`; no catalogue output | Resolved by DTO v3 (DEC-565) |
| ASSUMPTION-825 | Assumption | 11.4b.4, envelope | V12 "company" = blueprint "startup" (`company_id` ↔ `startup_id`) | Open; confirm with group E (platform) |
| ASSUMPTION-826 | Assumption | 11.4c/d service cards; 11.4.5.31 | New-domain services homed to existing epics until R2 confirms EP-22+ | Open; group B owns new epics |
| ASSUMPTION-827 | Assumption | 11.4b.3; 11.4.5.29 | Proposed tables for new domains; final DDL owned by the data group (R8) | Open |
| RECOMMENDATION-828 | Recommendation | 11.4b.5.1 | NT13 stays canonical; V10 patterns are its semantics; add `logic.reconcile` | Adopted in DEC-562 |
| RECOMMENDATION-829 | Recommendation | 11.4b.4 | Minor units at workflow DTO boundary; ADR-030 decimals for REST; exact conversion | Adopted in DEC-565 |
| RECOMMENDATION-830 | Recommendation | 11.4b.8; 11.4b.3; 11.4b.6.4 | DRR weights 1/2/4, budget hierarchy, default cadences, 30-day deprecation notice | Adopted in DEC-567 (parameters tunable) |
| GAP-831 | Gap | 11.4c/d cards; 11.4.5.33 | V12 illustrative cost excludes provider, retry and labour; margin target TBD | Mitigated: blueprint estimates added; margin owner = service owner |

**Inconsistencies observed in earlier parts (reported, not fixed).** (1) Part 9.4 §9.4.2 is titled "WF-01…WF-39" and the summary counts 38 workflows; WF-24 is absent from the table. (2) Part 9.4 §9.4.5 diagram still reads "Business workflow WF-01 to WF-14". (3) Part 7.4b NT13 uses side-effect classes R0/W1/X2 while Part 3.3 `aut_step_run.side_effect_class` uses {none, internal, external}; the handler manifest here uses the Part 3.3 vocabulary and a mapping (R0→none, W1→internal, X2→external) should be stated in both parts.

## 11.4.10 Quality gate: Part 11.4 (all batches)

| # | Check | Result | Notes and fixes applied |
|---|---|---|---|
| 1 | Every requirement traced to a source | Pass | {{N_ASPECTS}} aspects with V12 chapter/section and blueprint location; FR register cites V12 controls |
| 2 | Assumptions, gaps, conflicts tagged and logged | Pass | Tags 814–831 all used and registered (§11.4.9) |
| 3 | IDs unique and consistent with earlier parts | Pass | DEC-560…579, ADR-195…199, FR-V12-D-001…028 and 121…139, US-##-YD##, TC-V12-D-001…139 within allocation; aspect IDs asserted unique |
| 4 | No story lacks AC and no requirement lacks a test | Pass | 29 stories with Gherkin; every FR has a TC; every workflow has archetype instances |
| 5 | Negative, edge, security, accessibility cases covered | Pass | Preflight denials, replay, misfire, mandate tampering, noisy tenant, cross-tenant scope, DLT, minors/health data, WCAG form test |
| 6 | No agent lacks guardrail, fallback, KPI, cost | Pass / N/A | No new agents; reused agents keep their cards; per-workflow model cost given |
| 7 | Time-sensitive facts flagged with as-of date | Pass | Model, SMS, telephony and media prices marked "verify (as of 27 Nov 2026)"; TRAI rules via TR-R1 "verify" |
| 8 | No restricted data to free-tier models | Pass | `tier2_eligible = false` for all 231 steps |
| 9 | Consistent with earlier parts | Pass | DEC-064, DEC-218, DEC-383, DEC-386…388, DEC-392, DEC-395, DEC-418, DEC-421 respected; three earlier-part inconsistencies reported |

**Status: Part 11 Batch 11.4 complete. 76 V12 workflows (231 steps) of SM-SVC-21…39 captured and specified; {{N_ASPECTS}} aspects: {{N_MATCHED}} Matched, {{N_PENDING}} Pending Founder decision (CONFLICT-814…820), 0 unresolved.**
