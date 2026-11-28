### 11.4.5.10 SM-SVC-21 Payment, Invoice & Reconciliation Automation

| Field | Specification |
|---|---|
| Family / objective | Financial controls; Match verified payments and invoices and report commercial closure readiness |
| Channels / providers | Private financial workspace; Authorized accounting/bank/payment connection or statement import; no autonomous money transfer |
| Optional producers / complementary | Included foundation; no mandatory upstream paid service; optional input producers: SM-SVC-20; authorized equivalent input accepted. |
| Service KPI | Duplicate allocations = 0; reconciled payment or exception 100% |
| Availability / bundle | Full suite / Sales Conversion & Operations bundle / selective (1 SKU); entitlement and usage approval required. |
| Interoperability / readiness | Optional authorized connector; external agent access disabled unless explicitly granted; Proposed; test and validate customer demand, provider access and economics |
| Open-source stack | Python; Django REST Framework; PostgreSQL; Celery / Beat; Valkey; decimal arithmetic and atomic PostgreSQL transactions |
| Blueprint epic / module | EP-15 (ASSUMPTION-826) / `commerce.payments` |
| Effect adapter | none (record/verify only, DEC-064) |
| Service guardrail | Money movement stays unsupported (DEC-064): the service records and verifies; it never transfers, refunds or settles. |
| Functional requirement | FR-V12-D-121 (§11.4.5.29 register) |

**DTO `urn:sm:dto:SM-SVC-21-WF0n:v2` (one schema shared by the four workflows; v3 projection per workflow below):**

| Dir | Field | JSON Schema (App. B v2) | V12 validation | Blueprint storage target |
|---|---|---|---|---|
| in | `invoice_ref` | string format=uuid | UUID / scoped external reference; input, validate authorized scope | com_invoice.id (ENT-140) |
| in | `payment_ref` | string format=uuid | UUID / scoped external reference; input, validate authorized scope | com_payment.id (ENT-142) |
| in | `amount_minor` | integer minimum=0 | int64, nonnegative except signed ledger deltas; input, validate author | com_payment.amount numeric(18,4) ↔ int64 minor (RECOMMENDATION-829) |
| in | `currency` | string pattern=^[A-Z]{3}$ | ISO 4217 code; input, validate authorized scope | char(3) ISO 4217 (DEC-027) |
| out | `allocation_ref` | string format=uuid | UUID / scoped external reference; output, validate schema and evidence | com_payment_allocation.id (Part 3.3 allocation rows) |
| out | `balance_minor` | integer minimum=0 | int64, nonnegative except signed ledger deltas; output, validate schem | derived: invoice total − Σ allocations |
| out | `discrepancy_refs` | array maxItems=500 | array (typed references or structured items); output, validate schema  | aut_artifact items (domain receivable) |
| out | `reconciliation_state` | string maxLength=64 | string / configured enum; length and allowed values in versioned schem | enum {staged, matched, partial, mismatch, exception, reconciled} |

#### SM-SVC-21-WF01 Invoice and payment evidence import

| Field | Specification |
|---|---|
| V12 sources | BRD ch09 row; FSD ch12 lines 9112–9210; FSD ch13 registry row; App. B `urn:sm:dto:SM-SVC-21-WF01:v2`; workbook row "SM-SVC-21-WF01 — Invoice and payment evidence import" |
| Business outcome | Invoice and payment evidence import. Input → output: Invoice and authorized receipt source → Invoice/payment evidence |
| Detailed functionality (workbook) | Validate reference, currency and amount; deduplicate; stage verified records |
| Blueprint mapping | WF-11 (Part 2.2 §2.17); WF-10 payables (§2.16); agents AG-024; automations AU-037, AU-026, AU-004 |
| What V12 adds | Adds V12 IDs, typed DTO and the staging step; behaviour exists in WF-11 payment verification. |
| Behaviour status | Partially covered → Matched |
| Trigger (V12) | Authorized business event or manual import; signed webhook if applicable; Invoice and authorized receipt source |
| Trigger kinds (registry, DEC-564) | `manual` (NT13-03); `event` (NT13-01; `sm.svc21.wf01.requested` or upstream domain event, §11.4b.6); `provider_callback` (signed, replay-checked) |
| Authority (V12) | R3 financial/legal/commitment; L2 mandatory approved effect; L3 only with separately approved bounded mandate where lawful; Finance approves mismatches, refunds and corrections; no unverified closure |
| Blueprint autonomy (DEC-566) | V12 L2 default → blueprint **L1 maximum** (human approval bound to the exact hash; money movement not supported, DEC-064). V12 "L3 bounded mandate" **not adopted** (CONFLICT-814, Pending Founder decision). Approver: R08 maker, R09 checker |
| Human approval (workbook) | Finance approves mismatches, refunds and corrections; no unverified closure |
| Effect boundary | No external effect; approval gate inserted before state change (DEC-570) |
| Outputs produced (v3 projection) | `discrepancy_refs`, `reconciliation_state` |
| Workflow KPI | reference match precision; duplicate receipt count; baseline and threshold approved in pilot; source service KPI Duplicate allocations = 0; reconciled payment or exception 100% |
| Preconditions / failure handling | Common contract (D-F12-030 variant 1, D-F12-031): §11.4b.5 |
| Cost | V12 illustrative ₹0.15/invocation (excludes provider, retry, labour). Blueprint model estimate ₹0.00/run for 0 agent step(s) at Tier 1a (Part 7.3 prices, FX ₹90/USD, verify at time of implementation, as of 27 Nov 2026); Tier 2 not eligible (Confidential/personal data) |
| Usage limit (pilot, not approved) | Illustrative pilot: 500 invoice or receipt record(s)/month; 1 concurrent run; configurable hard budget, provider quota and frequency limits. Not approved. |
| Data modalities / version | Text; structured records; audio/image/video where applicable and authorized; documents; service 2.0-target, workflow 2.0-target |
| Acceptance (V12 → blueprint) | SM-SVC-21-WF01-TC-{POS,INPUT,SCOPE,ENT,DUP,QUALITY,BUDGET,RECOVERY,APPROVAL,EFFECT} → TC-V12-D-101…110; SM-SVC-21-WF01-AT01 → TC-V12-D-111 |
| Release proposal | R1 (W4) alignment |

| Step ID | Action (V12) | V12 executor → node type | Blueprint handler | Output contract | Failure → run state | Model tier | Status |
|---|---|---|---|---|---|---|---|
| SM-SVC-21-WF01-STEP-01 | Validate reference, currency and amount | Policy/validation engine → NT13-09 `policy.check` | PDP (AU-009) rule set | validation {passed,reason_codes,policy_version} | POLICY_DENIED → BLOCKED | Tier 0 / none | Matched |
| SM-SVC-21-WF01-STEP-02 | deduplicate | Identity/reconciliation engine → NT13-07 `logic.compute` | AU-037 registered function | match_result {matched_refs,unmatched_refs,conflict_refs} | CONFLICT → HELD | Tier 0 / none | Matched |
| SM-SVC-21-WF01-STEP-03 | stage verified records | Domain service → NT13-05 `data.write_internal` | `commerce.payments` service (revision check) | domain_result {artifact_ref,status,evidence_refs} | INVALID_STATE → HELD | Tier 0 / none | Matched |

#### SM-SVC-21-WF02 Partial payment reconciliation

| Field | Specification |
|---|---|
| V12 sources | BRD ch09 row; FSD ch12 lines 9211–9315; FSD ch13 registry row; App. B `urn:sm:dto:SM-SVC-21-WF02:v2`; workbook row "SM-SVC-21-WF02 — Partial payment reconciliation" |
| Business outcome | Partial payment reconciliation. Input → output: Verified payment and invoice balance → Allocation and outstanding balance |
| Detailed functionality (workbook) | Apply atomic allocation; check outstanding balance; flag mismatch; update eligible closure gate |
| Blueprint mapping | WF-11 partial payments; agents AG-024; automations AU-037, AU-035 |
| What V12 adds | Atomic allocation and closure gate exist (DEC-054); V12 R3 L3 mandate path is not adopted. |
| Behaviour status | Partially covered → Matched (CONFLICT-814) |
| Trigger (V12) | Manual request or validated upstream business event; Verified payment and invoice balance |
| Trigger kinds (registry, DEC-564) | `manual` (NT13-03); `event` (NT13-01; `sm.svc21.wf02.requested` or upstream domain event, §11.4b.6); `child_workflow` (registered dependency, depth ≤ 3) |
| Authority (V12) | R3 financial/legal/commitment; L2 mandatory approved effect; L3 only with separately approved bounded mandate where lawful; Finance approves mismatches, refunds and corrections; no unverified closure |
| Blueprint autonomy (DEC-566) | V12 L2 default → blueprint **L1 maximum** (human approval bound to the exact hash; money movement not supported, DEC-064). V12 "L3 bounded mandate" **not adopted** (CONFLICT-814, Pending Founder decision). Approver: R08 maker, R09 checker |
| Human approval (workbook) | Finance approves mismatches, refunds and corrections; no unverified closure |
| Effect boundary | No external effect; approval gate inserted before state change (DEC-570) |
| Outputs produced (v3 projection) | `allocation_ref`, `balance_minor`, `reconciliation_state` |
| Workflow KPI | allocation balance accuracy; over-allocation rejection; baseline and threshold approved in pilot; source service KPI Duplicate allocations = 0; reconciled payment or exception 100% |
| Preconditions / failure handling | Common contract (D-F12-030 variant 1, D-F12-031): §11.4b.5 |
| Cost | V12 illustrative ₹0.15/invocation (excludes provider, retry, labour). Blueprint model estimate ₹0.03/run for 1 agent step(s) at Tier 1a (Part 7.3 prices, FX ₹90/USD, verify at time of implementation, as of 27 Nov 2026); Tier 2 not eligible (Confidential/personal data) |
| Usage limit (pilot, not approved) | Illustrative pilot: 500 invoice or receipt record(s)/month; 1 concurrent run; configurable hard budget, provider quota and frequency limits. Not approved. |
| Data modalities / version | Text; structured records; service 2.0-target, workflow 2.0-target |
| Acceptance (V12 → blueprint) | SM-SVC-21-WF02-TC-{POS,INPUT,SCOPE,ENT,DUP,QUALITY,BUDGET,RECOVERY,APPROVAL,EFFECT} → TC-V12-D-101…110; SM-SVC-21-WF02-AT01 → TC-V12-D-111 |
| Release proposal | R1 (W4) alignment |

| Step ID | Action (V12) | V12 executor → node type | Blueprint handler | Output contract | Failure → run state | Model tier | Status |
|---|---|---|---|---|---|---|---|
| SM-SVC-21-WF02-STEP-01 | Apply atomic allocation | Policy/validation engine → NT13-09 `policy.check` | PDP (AU-009) rule set | validation {passed,reason_codes,policy_version} | POLICY_DENIED → BLOCKED | Tier 0 / none | Matched |
| SM-SVC-21-WF02-STEP-02 | check outstanding balance | Policy/validation engine → NT13-09 `policy.check` | PDP (AU-009) rule set | validation {passed,reason_codes,policy_version} | POLICY_DENIED → BLOCKED | Tier 0 / none | Matched |
| SM-SVC-21-WF02-STEP-03 | flag mismatch | Domain agent → NT13-08 `ai.task` + NT13-10 `approval.human` | AG-024 via gateway; routed to R08 maker | candidate {artifact_ref,confidence,reason_codes,review_state} | REVIEW_REQUIRED → AWAITING_APPROVAL | Tier 1a | Matched |
| SM-SVC-21-WF02-STEP-04 | update eligible closure gate | Domain service → NT13-05 `data.write_internal` | `commerce.payments` service (revision check) | domain_result {artifact_ref,status,evidence_refs} | INVALID_STATE → HELD | Tier 0 / none | Matched |

#### SM-SVC-21-WF03 Discrepancy and financial reporting

| Field | Specification |
|---|---|
| V12 sources | BRD ch09 row; FSD ch12 lines 9316–9414; FSD ch13 registry row; App. B `urn:sm:dto:SM-SVC-21-WF03:v2`; workbook row "SM-SVC-21-WF03 — Discrepancy and financial reporting" |
| Business outcome | Discrepancy and financial reporting. Input → output: Unmatched payments and verified ledger → Reconciliation report |
| Detailed functionality (workbook) | Summarize exceptions; route finance review; report verified receivables and receipts |
| Blueprint mapping | WF-11; RP-15 receipts and reconciliation; agents AG-029; automations AU-037, AU-040 |
| What V12 adds | Exception summary and finance review exist; V12 adds a typed reconciliation report artifact. |
| Behaviour status | Partially covered → Matched |
| Trigger (V12) | Manual request or validated upstream business event; Unmatched payments and verified ledger |
| Trigger kinds (registry, DEC-564) | `manual` (NT13-03); `event` (NT13-01; `sm.svc21.wf03.requested` or upstream domain event, §11.4b.6); `child_workflow` (registered dependency, depth ≤ 3) |
| Authority (V12) | R0 internal analysis/draft; L1 assisted; L3 approved read/draft; Finance approves mismatches, refunds and corrections; no unverified closure |
| Blueprint autonomy (DEC-566) | V12 L1 assisted / L3 approved read-draft → blueprint **L0–L1** (drafts and analysis only; no external effect). Approver: R08, R09 |
| Human approval (workbook) | Finance approves mismatches, refunds and corrections; no unverified closure |
| Effect boundary | No external effect; internal artifacts only |
| Outputs produced (v3 projection) | `discrepancy_refs`, `reconciliation_state` |
| Workflow KPI | exception completeness; verified ledger coverage; baseline and threshold approved in pilot; source service KPI Duplicate allocations = 0; reconciled payment or exception 100% |
| Preconditions / failure handling | Common contract (D-F12-030 variant 1, D-F12-031): §11.4b.5 |
| Cost | V12 illustrative ₹0.55/invocation (excludes provider, retry, labour). Blueprint model estimate ₹0.03/run for 1 agent step(s) at Tier 1a (Part 7.3 prices, FX ₹90/USD, verify at time of implementation, as of 27 Nov 2026); Tier 2 not eligible (Confidential/personal data) |
| Usage limit (pilot, not approved) | Illustrative pilot: 500 invoice or receipt record(s)/month; 1 concurrent run; configurable hard budget, provider quota and frequency limits. Not approved. |
| Data modalities / version | Text; structured records; service 2.0-target, workflow 2.0-target |
| Acceptance (V12 → blueprint) | SM-SVC-21-WF03-TC-{POS,INPUT,SCOPE,ENT,DUP,QUALITY,BUDGET,RECOVERY} → TC-V12-D-101…108; SM-SVC-21-WF03-AT01 → TC-V12-D-111 |
| Release proposal | R1 (W4) alignment |

| Step ID | Action (V12) | V12 executor → node type | Blueprint handler | Output contract | Failure → run state | Model tier | Status |
|---|---|---|---|---|---|---|---|
| SM-SVC-21-WF03-STEP-01 | Summarize exceptions | Domain service → NT13-05 `data.write_internal` | `commerce.payments` service (revision check) | domain_result {artifact_ref,status,evidence_refs} | INVALID_STATE → HELD | Tier 0 / none | Matched |
| SM-SVC-21-WF03-STEP-02 | route finance review | Domain agent → NT13-08 `ai.task` + NT13-10 `approval.human` | AG-029 via gateway; routed to R08 | candidate {artifact_ref,confidence,reason_codes,review_state} | REVIEW_REQUIRED → AWAITING_APPROVAL | Tier 1a | Matched |
| SM-SVC-21-WF03-STEP-03 | report verified receivables and receipts | Domain service → NT13-05 `data.write_internal` | `commerce.payments` service (revision check) | domain_result {artifact_ref,status,evidence_refs} | INVALID_STATE → HELD | Tier 0 / none | Matched |

#### SM-SVC-21-WF04 Receivable anomaly and overdue payment-risk monitoring

| Field | Specification |
|---|---|
| V12 sources | BRD ch09 row; FSD ch12 lines 9415–9519; FSD ch13 registry row; App. B `urn:sm:dto:SM-SVC-21-WF04:v2`; workbook row "SM-SVC-21-WF04 — Receivable anomaly and overdue payment-risk monitoring" |
| Business outcome | Receivable anomaly and overdue payment-risk monitoring. Input → output: Invoices, verified payments, due dates and currency → Receivable risk report |
| Detailed functionality (workbook) | Reconcile amounts; flag anomalies; calculate overdue exposure; route review |
| Blueprint mapping | WF-11; WF-17 early warning pattern; agents AG-079; automations AU-116, AU-037 |
| What V12 adds | New: overdue exposure ageing calculation and receivable anomaly flags (AU-116 rules extended). |
| Behaviour status | Partially covered → Matched |
| Trigger (V12) | Manual; scheduled or relevant validated business event; provider webhook only where authorized; Invoices, verified payments, due dates and currency |
| Trigger kinds (registry, DEC-564) | `manual` (NT13-03); `scheduled` (NT13-02; default cadence per §11.4b, misfire `reschedule_once`); `event` (NT13-01; `sm.svc21.wf04.requested` or upstream domain event, §11.4b.6); `provider_callback` (signed, replay-checked) |
| Authority (V12) | R0 internal analysis/draft; L1 assisted; L3 approved read/draft; Approve source/data rights and applicable external actions; approve consequential communications, commitments and changes; routine steps only within preapproved policies. |
| Blueprint autonomy (DEC-566) | V12 L1 assisted / L3 approved read-draft → blueprint **L0–L1** (drafts and analysis only; no external effect). Approver: R08 |
| Human approval (workbook) | Approve source/data rights and applicable external actions; approve consequential communications, commitments and changes; routine steps only within preapproved policies. |
| Effect boundary | No external effect; internal artifacts only |
| Outputs produced (v3 projection) | `balance_minor`, `discrepancy_refs`, `reconciliation_state` |
| Workflow KPI | overdue exposure accuracy; anomaly precision; baseline and threshold approved in pilot; source service KPI Duplicate allocations = 0; reconciled payment or exception 100% |
| Preconditions / failure handling | Common contract (D-F12-030 variant 2, D-F12-031): §11.4b.5 |
| Cost | V12 illustrative ₹0.55/invocation (excludes provider, retry, labour). Blueprint model estimate ₹0.06/run for 2 agent step(s) at Tier 1a (Part 7.3 prices, FX ₹90/USD, verify at time of implementation, as of 27 Nov 2026); Tier 2 not eligible (Confidential/personal data) |
| Usage limit (pilot, not approved) | Illustrative pilot: 500 invoice or receipt record(s)/month; 1 concurrent run; configurable hard budget, provider quota and frequency limits. Not approved. |
| Data modalities / version | Text; structured records; service 1.0-target, workflow 1.0-target |
| Acceptance (V12 → blueprint) | SM-SVC-21-WF04-TC-{POS,INPUT,SCOPE,ENT,DUP,QUALITY,BUDGET,RECOVERY} → TC-V12-D-101…108; SM-SVC-21-WF04-AT01 → TC-V12-D-111 |
| Release proposal | R2 (W5) |

| Step ID | Action (V12) | V12 executor → node type | Blueprint handler | Output contract | Failure → run state | Model tier | Status |
|---|---|---|---|---|---|---|---|
| SM-SVC-21-WF04-STEP-01 | Reconcile amounts | Identity/reconciliation engine → NT13-07 `logic.compute` | AU-037 registered function | match_result {matched_refs,unmatched_refs,conflict_refs} | CONFLICT → HELD | Tier 0 / none | Matched |
| SM-SVC-21-WF04-STEP-02 | flag anomalies | Domain agent → NT13-08 `ai.task` + NT13-10 `approval.human` | AG-079 via gateway; routed to R08 | candidate {artifact_ref,confidence,reason_codes,review_state} | REVIEW_REQUIRED → AWAITING_APPROVAL | Tier 1a | Matched |
| SM-SVC-21-WF04-STEP-03 | calculate overdue exposure | Rules/analytics engine → NT13-07 `logic.compute` | AU-116 registered function | calculation {value,unit,assumptions,evidence_refs} | INVALID_METRIC → HELD | Tier 0 / none | Matched |
| SM-SVC-21-WF04-STEP-04 | route review | Domain agent → NT13-08 `ai.task` + NT13-10 `approval.human` | AG-079 via gateway; routed to R08 | candidate {artifact_ref,confidence,reason_codes,review_state} | REVIEW_REQUIRED → AWAITING_APPROVAL | Tier 1a | Matched |

### 11.4.5.11 SM-SVC-22 Customer, Partner & Institutional Onboarding Automation

| Field | Specification |
|---|---|
| Family / objective | Customer lifecycle; Configure onboarding, partner deployment, institutional pilots and eligible service milestones |
| Channels / providers | Private workspace, eligible client notifications; Client systems or manual milestone evidence; no sensitive health data by default |
| Optional producers / complementary | Included foundation; no mandatory upstream paid service; optional input producers: SM-SVC-18; SM-SVC-20; authorized equivalent input accepted. |
| Service KPI | Required readiness gates 100%; overdue escalation ≥99% |
| Availability / bundle | Full suite / Lifecycle & Business Intelligence bundle / selective (1 SKU); entitlement and usage approval required. |
| Interoperability / readiness | Optional authorized connector; external agent access disabled unless explicitly granted; Proposed; test and validate customer demand, provider access and economics |
| Open-source stack | Python; Django REST Framework; PostgreSQL; Celery / Beat; Valkey |
| Blueprint epic / module | EP-16 (ASSUMPTION-826) / `lifecycle.onboarding` |
| Effect adapter | ADP-EMAIL (SES) via outbox |
| Service guardrail | MedMaarg institutional pilots carry no patient data (BR-S002, DEC-030 analogue for health). |
| Functional requirement | FR-V12-D-122 (§11.4.5.29 register) |

**DTO `urn:sm:dto:SM-SVC-22-WF0n:v2` (one schema shared by the four workflows; v3 projection per workflow below):**

| Dir | Field | JSON Schema (App. B v2) | V12 validation | Blueprint storage target |
|---|---|---|---|---|
| in | `customer_ref` | string format=uuid | UUID / scoped external reference; input, validate authorized scope | crm_account / lcy customer (ENT-086 deal owner account) |
| in | `agreement_ref` | string format=uuid | UUID / scoped external reference; input, validate authorized scope | com_contract.id (ENT-131) |
| in | `template_ref` | string format=uuid | UUID / scoped external reference; input, validate authorized scope | aut_workflow_template / eng_message_template by service |
| in | `milestone_refs` | array maxItems=500 | array (typed references or structured items); input, validate authoriz | lcy_task milestones (ENT-148) |
| out | `plan_ref` | string format=uuid | UUID / scoped external reference; output, validate schema and evidence | aut_artifact (domain plan) or lcy_onboarding (ENT-147) |
| out | `readiness_state` | string maxLength=64 | string / configured enum; length and allowed values in versioned schem | enum {not_ready, ready_with_risks, ready, blocked} |
| out | `task_refs` | array maxItems=500 | array (typed references or structured items); output, validate schema  | lcy_task.id[] (ENT-148) |
| out | `handover_ref` | string format=uuid | UUID / scoped external reference; output, validate schema and evidence | lcy_handoff.id (ENT-149) |

#### SM-SVC-22-WF01 Customer or partner onboarding plan

| Field | Specification |
|---|---|
| V12 sources | BRD ch09 row; FSD ch12 lines 9521–9619; FSD ch13 registry row; App. B `urn:sm:dto:SM-SVC-22-WF01:v2`; workbook row "SM-SVC-22-WF01 — Customer or partner onboarding plan" |
| Business outcome | Customer or partner onboarding plan. Input → output: Approved agreement or existing customer and template → Onboarding plan |
| Detailed functionality (workbook) | Generate scoped task dependencies; assign owners; check required documents |
| Blueprint mapping | WF-12 (Part 2.2 §2.18); agents AG-025; automations AU-036, AU-027 |
| What V12 adds | Onboarding checklist and handoff exist; V12 adds dependency graph and owner assignment as typed outputs. |
| Behaviour status | Partially covered → Matched |
| Trigger (V12) | Manual request or validated upstream business event; Approved agreement or existing customer and template |
| Trigger kinds (registry, DEC-564) | `manual` (NT13-03); `event` (NT13-01; `sm.svc22.wf01.requested` or upstream domain event, §11.4b.6); `child_workflow` (registered dependency, depth ≤ 3) |
| Authority (V12) | R0 internal analysis/draft; L1 assisted; L3 approved read/draft; Approve deployment readiness, pilot scope and regulated operations; consent for notifications |
| Blueprint autonomy (DEC-566) | V12 L1 assisted / L3 approved read-draft → blueprint **L0–L1** (drafts and analysis only; no external effect). Approver: R02 |
| Human approval (workbook) | Approve deployment readiness, pilot scope and regulated operations; consent for notifications |
| Effect boundary | No external effect; internal artifacts only |
| Outputs produced (v3 projection) | `plan_ref`, `task_refs` |
| Workflow KPI | dependency coverage; task owner completeness; baseline and threshold approved in pilot; source service KPI Required readiness gates 100%; overdue escalation ≥99% |
| Preconditions / failure handling | Common contract (D-F12-030 variant 1, D-F12-031): §11.4b.5 |
| Cost | V12 illustrative ₹0.75/invocation (excludes provider, retry, labour). Blueprint model estimate ₹1.29/run for 2 agent step(s) at Tier 1a (Part 7.3 prices, FX ₹90/USD, verify at time of implementation, as of 27 Nov 2026); Tier 2 not eligible (Confidential/personal data) |
| Usage limit (pilot, not approved) | Illustrative pilot: 100 onboarding case(s)/month; 1 concurrent run; configurable hard budget, provider quota and frequency limits. Not approved. |
| Data modalities / version | Text; structured records; service 2.0-target, workflow 2.0-target |
| Acceptance (V12 → blueprint) | SM-SVC-22-WF01-TC-{POS,INPUT,SCOPE,ENT,DUP,QUALITY,BUDGET,RECOVERY} → TC-V12-D-101…108; SM-SVC-22-WF01-AT01 → TC-V12-D-111 |
| Release proposal | R2 (W5) alignment |

| Step ID | Action (V12) | V12 executor → node type | Blueprint handler | Output contract | Failure → run state | Model tier | Status |
|---|---|---|---|---|---|---|---|
| SM-SVC-22-WF01-STEP-01 | Generate scoped task dependencies | Domain agent → NT13-08 `ai.task` + NT13-10 `approval.human` | AG-025 via gateway; routed to R02 | candidate {artifact_ref,confidence,reason_codes,review_state} | REVIEW_REQUIRED → AWAITING_APPROVAL | Tier 1b | Matched |
| SM-SVC-22-WF01-STEP-02 | assign owners | Domain agent → NT13-08 `ai.task` + NT13-10 `approval.human` | AG-025 via gateway; routed to R02 | candidate {artifact_ref,confidence,reason_codes,review_state} | REVIEW_REQUIRED → AWAITING_APPROVAL | Tier 1a | Matched |
| SM-SVC-22-WF01-STEP-03 | check required documents | Policy/validation engine → NT13-09 `policy.check` | PDP (AU-009) rule set | validation {passed,reason_codes,policy_version} | POLICY_DENIED → BLOCKED | Tier 0 / none | Matched |

#### SM-SVC-22-WF02 Institutional pilot and deployment readiness

| Field | Specification |
|---|---|
| V12 sources | BRD ch09 row; FSD ch12 lines 9620–9718; FSD ch13 registry row; App. B `urn:sm:dto:SM-SVC-22-WF02:v2`; workbook row "SM-SVC-22-WF02 — Institutional pilot and deployment readiness" |
| Business outcome | Institutional pilot and deployment readiness. Input → output: Pilot scope and milestone evidence → Readiness decision and milestone plan |
| Detailed functionality (workbook) | Validate capability and readiness; track risks; route review before activation |
| Blueprint mapping | §2.21.1 MedMaarg institutional partnership; agents AG-032; automations AU-043, AU-009 |
| What V12 adds | Pilot readiness gates exist (AU-043); V12 adds risk tracking and review-before-activation step IDs. |
| Behaviour status | Partially covered → Matched |
| Trigger (V12) | Manual request or validated upstream business event; Pilot scope and milestone evidence |
| Trigger kinds (registry, DEC-564) | `manual` (NT13-03); `event` (NT13-01; `sm.svc22.wf02.requested` or upstream domain event, §11.4b.6); `child_workflow` (registered dependency, depth ≤ 3) |
| Authority (V12) | R0 internal analysis/draft; L1 assisted; L3 approved read/draft; Approve deployment readiness, pilot scope and regulated operations; consent for notifications |
| Blueprint autonomy (DEC-566) | V12 L1 assisted / L3 approved read-draft → blueprint **L0–L1** (drafts and analysis only; no external effect). Approver: R02, R10 |
| Human approval (workbook) | Approve deployment readiness, pilot scope and regulated operations; consent for notifications |
| Effect boundary | No external effect; internal artifacts only |
| Outputs produced (v3 projection) | `plan_ref`, `readiness_state` |
| Workflow KPI | readiness evidence coverage; unsafe activation count; baseline and threshold approved in pilot; source service KPI Required readiness gates 100%; overdue escalation ≥99% |
| Preconditions / failure handling | Common contract (D-F12-030 variant 1, D-F12-031): §11.4b.5 |
| Cost | V12 illustrative ₹0.97/invocation (excludes provider, retry, labour). Blueprint model estimate ₹0.03/run for 1 agent step(s) at Tier 1a (Part 7.3 prices, FX ₹90/USD, verify at time of implementation, as of 27 Nov 2026); Tier 2 not eligible (Confidential/personal data) |
| Usage limit (pilot, not approved) | Illustrative pilot: 100 onboarding case(s)/month; 1 concurrent run; configurable hard budget, provider quota and frequency limits. Not approved. |
| Data modalities / version | Text; structured records; service 2.0-target, workflow 2.0-target |
| Acceptance (V12 → blueprint) | SM-SVC-22-WF02-TC-{POS,INPUT,SCOPE,ENT,DUP,QUALITY,BUDGET,RECOVERY} → TC-V12-D-101…108; SM-SVC-22-WF02-AT01 → TC-V12-D-111 |
| Release proposal | R2 (W5) alignment |

| Step ID | Action (V12) | V12 executor → node type | Blueprint handler | Output contract | Failure → run state | Model tier | Status |
|---|---|---|---|---|---|---|---|
| SM-SVC-22-WF02-STEP-01 | Validate capability and readiness | Policy/validation engine → NT13-09 `policy.check` | PDP (AU-009) rule set | validation {passed,reason_codes,policy_version} | POLICY_DENIED → BLOCKED | Tier 0 / none | Matched |
| SM-SVC-22-WF02-STEP-02 | track risks | Domain service → NT13-05 `data.write_internal` | `lifecycle.onboarding` service (revision check) | domain_result {artifact_ref,status,evidence_refs} | INVALID_STATE → HELD | Tier 0 / none | Matched |
| SM-SVC-22-WF02-STEP-03 | route review before activation | Domain agent → NT13-08 `ai.task` + NT13-10 `approval.human` | AG-032 via gateway; routed to R02 | candidate {artifact_ref,confidence,reason_codes,review_state} | REVIEW_REQUIRED → AWAITING_APPROVAL | Tier 1a | Matched |

#### SM-SVC-22-WF03 Milestone monitoring and handover

| Field | Specification |
|---|---|
| V12 sources | BRD ch09 row; FSD ch12 lines 9719–9823; FSD ch13 registry row; App. B `urn:sm:dto:SM-SVC-22-WF03:v2`; workbook row "SM-SVC-22-WF03 — Milestone monitoring and handover" |
| Business outcome | Milestone monitoring and handover. Input → output: Deployment status and acceptance evidence → Deployment status and handover |
| Detailed functionality (workbook) | Check dependencies; send eligible reminders; escalate overdue tasks; record acceptance |
| Blueprint mapping | WF-12 milestones and handover; agents AG-025; automations AU-027, AU-009, AU-022 |
| What V12 adds | Eligible reminders already dispatch via outbox; V12 R2 requires exact approved effect (template-level approval). |
| Behaviour status | Partially covered → Matched |
| Trigger (V12) | Authorized business event or manual import; signed webhook if applicable; Deployment status and acceptance evidence |
| Trigger kinds (registry, DEC-564) | `manual` (NT13-03); `event` (NT13-01; `sm.svc22.wf03.requested` or upstream domain event, §11.4b.6); `provider_callback` (signed, replay-checked) |
| Authority (V12) | R2 external communication/provider/access write; L2 mandatory approved effect; L3 only with separately approved bounded mandate where lawful; Approve deployment readiness, pilot scope and regulated operations; consent for notifications |
| Blueprint autonomy (DEC-566) | V12 L2 exact approved effect → blueprint **L1 approval of the exact payload hash, then L2 dispatch** of that item through the outbox (DEC-064 publishing pattern); V12 L3 mandate only for routine replies/reminders within caps. Approver: R02 |
| Human approval (workbook) | Approve deployment readiness, pilot scope and regulated operations; consent for notifications |
| Effect boundary | Effect steps: STEP-02 via ADP-EMAIL (SES) via outbox |
| Outputs produced (v3 projection) | `task_refs`, `handover_ref` |
| Workflow KPI | milestone acceptance accuracy; escalation latency; baseline and threshold approved in pilot; source service KPI Required readiness gates 100%; overdue escalation ≥99% |
| Preconditions / failure handling | Common contract (D-F12-030 variant 1, D-F12-031): §11.4b.5 |
| Cost | V12 illustrative ₹0.15/invocation (excludes provider, retry, labour). Blueprint model estimate ₹0.00/run for 0 agent step(s) at Tier 1a (Part 7.3 prices, FX ₹90/USD, verify at time of implementation, as of 27 Nov 2026); Tier 2 not eligible (Confidential/personal data) |
| Usage limit (pilot, not approved) | Illustrative pilot: 100 onboarding case(s)/month; 1 concurrent run; configurable hard budget, provider quota and frequency limits. Not approved. |
| Data modalities / version | Text; structured records; service 2.0-target, workflow 2.0-target |
| Acceptance (V12 → blueprint) | SM-SVC-22-WF03-TC-{POS,INPUT,SCOPE,ENT,DUP,QUALITY,BUDGET,RECOVERY,APPROVAL,EFFECT} → TC-V12-D-101…110; SM-SVC-22-WF03-AT01 → TC-V12-D-111 |
| Release proposal | R2 (W5) alignment |

| Step ID | Action (V12) | V12 executor → node type | Blueprint handler | Output contract | Failure → run state | Model tier | Status |
|---|---|---|---|---|---|---|---|
| SM-SVC-22-WF03-STEP-01 | Check dependencies | Policy/validation engine → NT13-09 `policy.check` | PDP (AU-009) rule set | validation {passed,reason_codes,policy_version} | POLICY_DENIED → BLOCKED | Tier 0 / none | Matched |
| SM-SVC-22-WF03-STEP-02 | send eligible reminders | Effect adapter → NT13-13 `action.external` | Outbox → AU-009 dispatch recheck → ADP-EMAIL (SES) via outbox | effect_receipt {provider_ref,status,observed_at} | EFFECT_UNKNOWN → RECONCILING | none | Matched |
| SM-SVC-22-WF03-STEP-03 | escalate overdue tasks | Domain service → NT13-05 `data.write_internal` | `lifecycle.onboarding` service (revision check) | domain_result {artifact_ref,status,evidence_refs} | INVALID_STATE → HELD | Tier 0 / none | Matched |
| SM-SVC-22-WF03-STEP-04 | record acceptance | Domain service → NT13-05 `data.write_internal` | `lifecycle.onboarding` service (revision check) | domain_result {artifact_ref,status,evidence_refs} | INVALID_STATE → HELD | Tier 0 / none | Matched |

#### SM-SVC-22-WF04 Adaptive onboarding plans and readiness monitoring

| Field | Specification |
|---|---|
| V12 sources | BRD ch09 row; FSD ch12 lines 9824–9928; FSD ch13 registry row; App. B `urn:sm:dto:SM-SVC-22-WF04:v2`; workbook row "SM-SVC-22-WF04 — Adaptive onboarding plans and readiness monitoring" |
| Business outcome | Adaptive onboarding plans and readiness monitoring. Input → output: Customer requirements, plan template, evidence and dependencies → Onboarding plan and readiness status |
| Detailed functionality (workbook) | Generate scoped tasks; evaluate readiness; adapt due dates; escalate blockers |
| Blueprint mapping | WF-12; agents AG-025, AG-038; automations AU-043, AU-027 |
| What V12 adds | New: adaptive due-date recalculation and blocker escalation from readiness evaluation. |
| Behaviour status | Not covered → Matched |
| Trigger (V12) | Manual; scheduled or relevant validated business event; provider webhook only where authorized; Customer requirements, plan template, evidence and dependencies |
| Trigger kinds (registry, DEC-564) | `manual` (NT13-03); `scheduled` (NT13-02; default cadence per §11.4b, misfire `reschedule_once`); `event` (NT13-01; `sm.svc22.wf04.requested` or upstream domain event, §11.4b.6); `provider_callback` (signed, replay-checked) |
| Authority (V12) | R0 internal analysis/draft; L1 assisted; L3 approved read/draft; Approve source/data rights and applicable external actions; approve consequential communications, commitments and changes; routine steps only within preapproved policies. |
| Blueprint autonomy (DEC-566) | V12 L1 assisted / L3 approved read-draft → blueprint **L0–L1** (drafts and analysis only; no external effect). Approver: R02 |
| Human approval (workbook) | Approve source/data rights and applicable external actions; approve consequential communications, commitments and changes; routine steps only within preapproved policies. |
| Effect boundary | No external effect; internal artifacts only |
| Outputs produced (v3 projection) | `plan_ref`, `readiness_state`, `task_refs` |
| Workflow KPI | blocker recall; due-date change audit coverage; baseline and threshold approved in pilot; source service KPI Required readiness gates 100%; overdue escalation ≥99% |
| Preconditions / failure handling | Common contract (D-F12-030 variant 2, D-F12-031): §11.4b.5 |
| Cost | V12 illustrative ₹0.55/invocation (excludes provider, retry, labour). Blueprint model estimate ₹1.26/run for 1 agent step(s) at Tier 1a (Part 7.3 prices, FX ₹90/USD, verify at time of implementation, as of 27 Nov 2026); Tier 2 not eligible (Confidential/personal data) |
| Usage limit (pilot, not approved) | Illustrative pilot: 100 onboarding case(s)/month; 1 concurrent run; configurable hard budget, provider quota and frequency limits. Not approved. |
| Data modalities / version | Text; structured records; service 1.0-target, workflow 1.0-target |
| Acceptance (V12 → blueprint) | SM-SVC-22-WF04-TC-{POS,INPUT,SCOPE,ENT,DUP,QUALITY,BUDGET,RECOVERY} → TC-V12-D-101…108; SM-SVC-22-WF04-AT01 → TC-V12-D-111 |
| Release proposal | W6 / A1 |

| Step ID | Action (V12) | V12 executor → node type | Blueprint handler | Output contract | Failure → run state | Model tier | Status |
|---|---|---|---|---|---|---|---|
| SM-SVC-22-WF04-STEP-01 | Generate scoped tasks | Domain agent → NT13-08 `ai.task` + NT13-10 `approval.human` | AG-025 via gateway; routed to R02 | candidate {artifact_ref,confidence,reason_codes,review_state} | REVIEW_REQUIRED → AWAITING_APPROVAL | Tier 1b | Matched |
| SM-SVC-22-WF04-STEP-02 | evaluate readiness | Domain service → NT13-05 `data.write_internal` | `lifecycle.onboarding` service (revision check) | domain_result {artifact_ref,status,evidence_refs} | INVALID_STATE → HELD | Tier 0 / none | Matched |
| SM-SVC-22-WF04-STEP-03 | adapt due dates | Domain service → NT13-05 `data.write_internal` | `lifecycle.onboarding` service (revision check) | domain_result {artifact_ref,status,evidence_refs} | INVALID_STATE → HELD | Tier 0 / none | Matched |
| SM-SVC-22-WF04-STEP-04 | escalate blockers | Domain service → NT13-05 `data.write_internal` | `lifecycle.onboarding` service (revision check) | domain_result {artifact_ref,status,evidence_refs} | INVALID_STATE → HELD | Tier 0 / none | Matched |

### 11.4.5.12 SM-SVC-23 Customer Retention, Renewal & Feedback Automation

| Field | Specification |
|---|---|
| Family / objective | Customer lifecycle; Monitor renewal dates, customer engagement, feedback and lost-deal signals |
| Channels / providers | Email, WhatsApp where eligible, private tasks; Authorized communication provider or manual follow-up; customer feedback source |
| Optional producers / complementary | Included foundation; no mandatory upstream paid service; optional input producers: SM-SVC-22; SM-SVC-05; authorized equivalent input accepted. |
| Service KPI | Applicable consent/stop checks 100%; renewal reminders ≥99% |
| Availability / bundle | Full suite / Lifecycle & Business Intelligence bundle / selective (1 SKU); entitlement and usage approval required. |
| Interoperability / readiness | Optional authorized connector; external agent access disabled unless explicitly granted; Proposed; test and validate customer demand, provider access and economics |
| Open-source stack | Python; Django REST Framework; PostgreSQL; Celery / Beat; Valkey |
| Blueprint epic / module | EP-16 (ASSUMPTION-826) / `lifecycle.retention` |
| Effect adapter | ADP-EMAIL / ADP-WA via outbox |
| Service guardrail | Renewal reminders tighten from DEC-064 "up to L3" to V12 R2 "L2 exact approved effect" (stricter wins). |
| Functional requirement | FR-V12-D-123 (§11.4.5.29 register) |

**DTO `urn:sm:dto:SM-SVC-23-WF0n:v2` (one schema shared by the four workflows; v3 projection per workflow below):**

| Dir | Field | JSON Schema (App. B v2) | V12 validation | Blueprint storage target |
|---|---|---|---|---|
| in | `customer_ref` | string format=uuid | UUID / scoped external reference; input, validate authorized scope | crm_account / lcy customer (ENT-086 deal owner account) |
| in | `renewal_ref` | string format=uuid | UUID / scoped external reference; input, validate authorized scope | lcy_renewal.id (ENT-150) |
| in | `feedback_refs` | array maxItems=500 | array (typed references or structured items); input, validate authoriz | lcy_feedback.id[] (ENT-157) |
| in | `consent_ref` | string format=uuid | UUID / scoped external reference; input, validate authorized scope | gov_consent.id (ENT-027) |
| out | `renewal_task_ref` | string format=uuid | UUID / scoped external reference; output, validate schema and evidence | lcy_task.id |
| out | `risk_score` | string pattern=^-?\d{1,14}(\.\d{1,4})?$ | decimal; unit and bounds defined by metric policy; output, validate sc | numeric(5,2) 0–100 (V12 string: GAP-824) |
| out | `reason_codes` | array maxItems=50 | array of configured reason codes (reason-code registry); output, valid | text[] from versioned reason registry |
| out | `recommendation_ref` | string format=uuid | UUID / scoped external reference; output, validate schema and evidence | aut_artifact (domain recommendation) |

#### SM-SVC-23-WF01 Renewal and obligation reminders

| Field | Specification |
|---|---|
| V12 sources | BRD ch09 row; FSD ch12 lines 9930–10034; FSD ch13 registry row; App. B `urn:sm:dto:SM-SVC-23-WF01:v2`; workbook row "SM-SVC-23-WF01 — Renewal and obligation reminders" |
| Business outcome | Renewal and obligation reminders. Input → output: Contract terms, renewal date and consent → Renewal queue |
| Detailed functionality (workbook) | Calculate reminder schedule; check eligibility; assign tasks; avoid duplicate notices |
| Blueprint mapping | WF-12 renewal calendar; WF-31 (Part 9.8b); agents AG-038; automations AU-039, AU-009, AU-022 |
| What V12 adds | Renewal calendar exists (AU-039); V12 adds duplicate-notice guard and approval-bound reminders. |
| Behaviour status | Partially covered → Matched |
| Trigger (V12) | Scheduled or manual; scoped event on change; Contract terms, renewal date and consent |
| Trigger kinds (registry, DEC-564) | `manual` (NT13-03); `scheduled` (NT13-02; default cadence per §11.4b, misfire `reschedule_once`); `event` (NT13-01; `sm.svc23.wf01.requested` or upstream domain event, §11.4b.6) |
| Authority (V12) | R2 external communication/provider/access write; L2 mandatory approved effect; L3 only with separately approved bounded mandate where lawful; Approve renewal offers and material changes; suppression and frequency enforced |
| Blueprint autonomy (DEC-566) | V12 L2 exact approved effect → blueprint **L1 approval of the exact payload hash, then L2 dispatch** of that item through the outbox (DEC-064 publishing pattern); V12 L3 mandate only for routine replies/reminders within caps. Approver: R03 |
| Human approval (workbook) | Approve renewal offers and material changes; suppression and frequency enforced |
| Effect boundary | No external effect; approval gate inserted before state change (DEC-570) |
| Outputs produced (v3 projection) | `renewal_task_ref` |
| Workflow KPI | renewal date accuracy; duplicate reminders; baseline and threshold approved in pilot; source service KPI Applicable consent/stop checks 100%; renewal reminders ≥99% |
| Preconditions / failure handling | Common contract (D-F12-030 variant 1, D-F12-031): §11.4b.5 |
| Cost | V12 illustrative ₹0.15/invocation (excludes provider, retry, labour). Blueprint model estimate ₹0.03/run for 1 agent step(s) at Tier 1a (Part 7.3 prices, FX ₹90/USD, verify at time of implementation, as of 27 Nov 2026); Tier 2 not eligible (Confidential/personal data) |
| Usage limit (pilot, not approved) | Illustrative pilot: 500 customer review(s)/month; 1 concurrent run; configurable hard budget, provider quota and frequency limits. Not approved. |
| Data modalities / version | Text; structured records; service 2.0-target, workflow 2.0-target |
| Acceptance (V12 → blueprint) | SM-SVC-23-WF01-TC-{POS,INPUT,SCOPE,ENT,DUP,QUALITY,BUDGET,RECOVERY,APPROVAL,EFFECT} → TC-V12-D-101…110; SM-SVC-23-WF01-AT01 → TC-V12-D-111 |
| Release proposal | R2 (W5) alignment |

| Step ID | Action (V12) | V12 executor → node type | Blueprint handler | Output contract | Failure → run state | Model tier | Status |
|---|---|---|---|---|---|---|---|
| SM-SVC-23-WF01-STEP-01 | Calculate reminder schedule | Rules/analytics engine → NT13-07 `logic.compute` | AU-039 registered function | calculation {value,unit,assumptions,evidence_refs} | INVALID_METRIC → HELD | Tier 0 / none | Matched |
| SM-SVC-23-WF01-STEP-02 | check eligibility | Policy/validation engine → NT13-09 `policy.check` | PDP (AU-009) rule set | validation {passed,reason_codes,policy_version} | POLICY_DENIED → BLOCKED | Tier 0 / none | Matched |
| SM-SVC-23-WF01-STEP-03 | assign tasks | Domain agent → NT13-08 `ai.task` + NT13-10 `approval.human` | AG-038 via gateway; routed to R03 | candidate {artifact_ref,confidence,reason_codes,review_state} | REVIEW_REQUIRED → AWAITING_APPROVAL | Tier 1a | Matched |
| SM-SVC-23-WF01-STEP-04 | avoid duplicate notices | Domain service → NT13-05 `data.write_internal` | `lifecycle.retention` service (revision check) | domain_result {artifact_ref,status,evidence_refs} | INVALID_STATE → HELD | Tier 0 / none | Matched |

#### SM-SVC-23-WF02 Feedback and lost-deal analysis

| Field | Specification |
|---|---|
| V12 sources | BRD ch09 row; FSD ch12 lines 10035–10133; FSD ch13 registry row; App. B `urn:sm:dto:SM-SVC-23-WF02:v2`; workbook row "SM-SVC-23-WF02 — Feedback and lost-deal analysis" |
| Business outcome | Feedback and lost-deal analysis. Input → output: Approved feedback or loss reason → Feedback insights |
| Detailed functionality (workbook) | Classify sentiment and reasons; identify actionable themes; route support issue |
| Blueprint mapping | WF-12 lost-deal learning; WF-32 (Part 9.8b); agents AG-026, AG-068; automations AU-095 |
| What V12 adds | Classification of loss reasons and feedback exists (AG-026); V12 adds routing of support issues to SVC-33. |
| Behaviour status | Partially covered → Matched |
| Trigger (V12) | Manual request or validated upstream business event; Approved feedback or loss reason |
| Trigger kinds (registry, DEC-564) | `manual` (NT13-03); `event` (NT13-01; `sm.svc23.wf02.requested` or upstream domain event, §11.4b.6); `child_workflow` (registered dependency, depth ≤ 3) |
| Authority (V12) | R0 internal analysis/draft; L1 assisted; L3 approved read/draft; Approve renewal offers and material changes; suppression and frequency enforced |
| Blueprint autonomy (DEC-566) | V12 L1 assisted / L3 approved read-draft → blueprint **L0–L1** (drafts and analysis only; no external effect). Approver: R03 |
| Human approval (workbook) | Approve renewal offers and material changes; suppression and frequency enforced |
| Effect boundary | No external effect; internal artifacts only |
| Outputs produced (v3 projection) | `reason_codes` |
| Workflow KPI | theme classification accuracy; issue routing rate; baseline and threshold approved in pilot; source service KPI Applicable consent/stop checks 100%; renewal reminders ≥99% |
| Preconditions / failure handling | Common contract (D-F12-030 variant 1, D-F12-031): §11.4b.5 |
| Cost | V12 illustrative ₹0.87/invocation (excludes provider, retry, labour). Blueprint model estimate ₹0.09/run for 3 agent step(s) at Tier 1a (Part 7.3 prices, FX ₹90/USD, verify at time of implementation, as of 27 Nov 2026); Tier 2 not eligible (Confidential/personal data) |
| Usage limit (pilot, not approved) | Illustrative pilot: 500 customer review(s)/month; 1 concurrent run; configurable hard budget, provider quota and frequency limits. Not approved. |
| Data modalities / version | Text; structured records; service 2.0-target, workflow 2.0-target |
| Acceptance (V12 → blueprint) | SM-SVC-23-WF02-TC-{POS,INPUT,SCOPE,ENT,DUP,QUALITY,BUDGET,RECOVERY} → TC-V12-D-101…108; SM-SVC-23-WF02-AT01 → TC-V12-D-111 |
| Release proposal | R2 (W5) alignment |

| Step ID | Action (V12) | V12 executor → node type | Blueprint handler | Output contract | Failure → run state | Model tier | Status |
|---|---|---|---|---|---|---|---|
| SM-SVC-23-WF02-STEP-01 | Classify sentiment and reasons | Domain agent → NT13-08 `ai.task` + NT13-10 `approval.human` | AG-026 via gateway; routed to R03 | candidate {artifact_ref,confidence,reason_codes,review_state} | REVIEW_REQUIRED → AWAITING_APPROVAL | Tier 1a | Matched |
| SM-SVC-23-WF02-STEP-02 | identify actionable themes | Domain agent → NT13-08 `ai.task` + NT13-10 `approval.human` | AG-068 via gateway; routed to R03 | candidate {artifact_ref,confidence,reason_codes,review_state} | REVIEW_REQUIRED → AWAITING_APPROVAL | Tier 1a | Matched |
| SM-SVC-23-WF02-STEP-03 | route support issue | Domain agent → NT13-08 `ai.task` + NT13-10 `approval.human` | AG-026 via gateway; routed to R03 | candidate {artifact_ref,confidence,reason_codes,review_state} | REVIEW_REQUIRED → AWAITING_APPROVAL | Tier 1a | Matched |

#### SM-SVC-23-WF03 Retention and re-engagement plan

| Field | Specification |
|---|---|
| V12 sources | BRD ch09 row; FSD ch12 lines 10134–10232; FSD ch13 registry row; App. B `urn:sm:dto:SM-SVC-23-WF03:v2`; workbook row "SM-SVC-23-WF03 — Retention and re-engagement plan" |
| Business outcome | Retention and re-engagement plan. Input → output: Customer history and eligible preferences → Retention recommendation |
| Detailed functionality (workbook) | Identify risk; propose compliant next action or renewal draft; hold ineligible cases |
| Blueprint mapping | WF-31; agents AG-038; automations AU-093, AU-009 |
| What V12 adds | Retention next-best action exists (AG-038); V12 adds explicit hold of ineligible cases. |
| Behaviour status | Partially covered → Matched |
| Trigger (V12) | Manual request or validated upstream business event; Customer history and eligible preferences |
| Trigger kinds (registry, DEC-564) | `manual` (NT13-03); `event` (NT13-01; `sm.svc23.wf03.requested` or upstream domain event, §11.4b.6); `child_workflow` (registered dependency, depth ≤ 3) |
| Authority (V12) | R0 internal analysis/draft; L1 assisted; L3 approved read/draft; Approve renewal offers and material changes; suppression and frequency enforced |
| Blueprint autonomy (DEC-566) | V12 L1 assisted / L3 approved read-draft → blueprint **L0–L1** (drafts and analysis only; no external effect). Approver: R03 |
| Human approval (workbook) | Approve renewal offers and material changes; suppression and frequency enforced |
| Effect boundary | No external effect; internal artifacts only |
| Outputs produced (v3 projection) | `renewal_task_ref`, `risk_score`, `recommendation_ref` |
| Workflow KPI | eligible recommendation rate; unsupported offer count; baseline and threshold approved in pilot; source service KPI Applicable consent/stop checks 100%; renewal reminders ≥99% |
| Preconditions / failure handling | Common contract (D-F12-030 variant 1, D-F12-031): §11.4b.5 |
| Cost | V12 illustrative ₹0.75/invocation (excludes provider, retry, labour). Blueprint model estimate ₹1.29/run for 2 agent step(s) at Tier 1a (Part 7.3 prices, FX ₹90/USD, verify at time of implementation, as of 27 Nov 2026); Tier 2 not eligible (Confidential/personal data) |
| Usage limit (pilot, not approved) | Illustrative pilot: 500 customer review(s)/month; 1 concurrent run; configurable hard budget, provider quota and frequency limits. Not approved. |
| Data modalities / version | Text; structured records; service 2.0-target, workflow 2.0-target |
| Acceptance (V12 → blueprint) | SM-SVC-23-WF03-TC-{POS,INPUT,SCOPE,ENT,DUP,QUALITY,BUDGET,RECOVERY} → TC-V12-D-101…108; SM-SVC-23-WF03-AT01 → TC-V12-D-111 |
| Release proposal | R2 (W5) alignment |

| Step ID | Action (V12) | V12 executor → node type | Blueprint handler | Output contract | Failure → run state | Model tier | Status |
|---|---|---|---|---|---|---|---|
| SM-SVC-23-WF03-STEP-01 | Identify risk | Domain agent → NT13-08 `ai.task` + NT13-10 `approval.human` | AG-038 via gateway; routed to R03 | candidate {artifact_ref,confidence,reason_codes,review_state} | REVIEW_REQUIRED → AWAITING_APPROVAL | Tier 1a | Matched |
| SM-SVC-23-WF03-STEP-02 | propose compliant next action or renewal draft | Domain agent → NT13-08 `ai.task` + NT13-10 `approval.human` | AG-038 via gateway; routed to R03 | candidate {artifact_ref,confidence,reason_codes,review_state} | REVIEW_REQUIRED → AWAITING_APPROVAL | Tier 1b | Matched |
| SM-SVC-23-WF03-STEP-03 | hold ineligible cases | Policy/validation engine → NT13-09 `policy.check` | PDP (AU-009) rule set | validation {passed,reason_codes,policy_version} | POLICY_DENIED → BLOCKED | Tier 0 / none | Matched |

#### SM-SVC-23-WF04 Churn and customer expansion opportunity prediction

| Field | Specification |
|---|---|
| V12 sources | BRD ch09 row; FSD ch12 lines 10233–10331; FSD ch13 registry row; App. B `urn:sm:dto:SM-SVC-23-WF04:v2`; workbook row "SM-SVC-23-WF04 — Churn and customer expansion opportunity prediction" |
| Business outcome | Churn and customer expansion opportunity prediction. Input → output: Permitted usage, renewal dates, support and feedback → Retention and expansion recommendations |
| Detailed functionality (workbook) | Evaluate calibrated risk and expansion signals; explain uncertainty; route approved action |
| Blueprint mapping | WF-17 (Part 9.7b); agents AG-038, AG-067; automations AU-059, AU-093 |
| What V12 adds | Churn model is advisory only (DEC-383); V12 adds expansion signals and uncertainty explanation. |
| Behaviour status | Partially covered → Matched |
| Trigger (V12) | Manual; scheduled or relevant validated business event; provider webhook only where authorized; Permitted usage, renewal dates, support and feedback |
| Trigger kinds (registry, DEC-564) | `manual` (NT13-03); `scheduled` (NT13-02; default cadence per §11.4b, misfire `reschedule_once`); `event` (NT13-01; `sm.svc23.wf04.requested` or upstream domain event, §11.4b.6); `provider_callback` (signed, replay-checked) |
| Authority (V12) | R0 internal analysis/draft; L1 assisted; L3 approved read/draft; Approve source/data rights and applicable external actions; approve consequential communications, commitments and changes; routine steps only within preapproved policies. |
| Blueprint autonomy (DEC-566) | V12 L1 assisted / L3 approved read-draft → blueprint **L0–L1** (drafts and analysis only; no external effect). Approver: R03, R02 |
| Human approval (workbook) | Approve source/data rights and applicable external actions; approve consequential communications, commitments and changes; routine steps only within preapproved policies. |
| Effect boundary | No external effect; internal artifacts only |
| Outputs produced (v3 projection) | `risk_score`, `recommendation_ref` |
| Workflow KPI | churn calibration; expansion precision; baseline and threshold approved in pilot; source service KPI Applicable consent/stop checks 100%; renewal reminders ≥99% |
| Preconditions / failure handling | Common contract (D-F12-030 variant 2, D-F12-031): §11.4b.5 |
| Cost | V12 illustrative ₹0.55/invocation (excludes provider, retry, labour). Blueprint model estimate ₹0.03/run for 1 agent step(s) at Tier 1a (Part 7.3 prices, FX ₹90/USD, verify at time of implementation, as of 27 Nov 2026); Tier 2 not eligible (Confidential/personal data) |
| Usage limit (pilot, not approved) | Illustrative pilot: 500 customer review(s)/month; 1 concurrent run; configurable hard budget, provider quota and frequency limits. Not approved. |
| Data modalities / version | Text; structured records; service 1.0-target, workflow 1.0-target |
| Acceptance (V12 → blueprint) | SM-SVC-23-WF04-TC-{POS,INPUT,SCOPE,ENT,DUP,QUALITY,BUDGET,RECOVERY} → TC-V12-D-101…108; SM-SVC-23-WF04-AT01 → TC-V12-D-111 |
| Release proposal | A1 |

| Step ID | Action (V12) | V12 executor → node type | Blueprint handler | Output contract | Failure → run state | Model tier | Status |
|---|---|---|---|---|---|---|---|
| SM-SVC-23-WF04-STEP-01 | Evaluate calibrated risk and expansion signals | Domain service → NT13-05 `data.write_internal` | `lifecycle.retention` service (revision check) | domain_result {artifact_ref,status,evidence_refs} | INVALID_STATE → HELD | Tier 0 / none | Matched |
| SM-SVC-23-WF04-STEP-02 | explain uncertainty | Domain service → NT13-05 `data.write_internal` | `lifecycle.retention` service (revision check) | domain_result {artifact_ref,status,evidence_refs} | INVALID_STATE → HELD | Tier 0 / none | Matched |
| SM-SVC-23-WF04-STEP-03 | route approved action | Domain agent → NT13-08 `ai.task` + NT13-10 `approval.human` | AG-038 via gateway; routed to R03 | candidate {artifact_ref,confidence,reason_codes,review_state} | REVIEW_REQUIRED → AWAITING_APPROVAL | Tier 1a | Matched |

### 11.4.5.13 SM-SVC-24 Revenue, Attribution & Sales Forecast Automation

| Field | Specification |
|---|---|
| Family / objective | Analytics; Measure verified commercial outcomes, attribution, forecast and improvement opportunities |
| Channels / providers | Private dashboard, internal reports; Authorized accounting and campaign data or imports; transparent model assumptions |
| Optional producers / complementary | Included foundation; no mandatory upstream paid service; optional input producers: SM-SVC-05; SM-SVC-14; SM-SVC-21; authorized equivalent input accepted. |
| Service KPI | Revenue reconciliation 100% or explicit exception; forecast error tracked |
| Availability / bundle | Full suite / Lifecycle & Business Intelligence bundle / selective (1 SKU); entitlement and usage approval required. |
| Interoperability / readiness | Optional authorized connector; external agent access disabled unless explicitly granted; Proposed; test and validate customer demand, provider access and economics |
| Open-source stack | Python; Django REST Framework; PostgreSQL; Celery / Beat; Valkey |
| Blueprint epic / module | EP-17 (ASSUMPTION-826) / `analytics.revenue` |
| Effect adapter | none |
| Service guardrail | Forecasts are labelled estimates and never mixed with actuals (DEC-391); default attribution stays last non-direct (DEC-397). |
| Functional requirement | FR-V12-D-124 (§11.4.5.29 register) |

**DTO `urn:sm:dto:SM-SVC-24-WF0n:v2` (one schema shared by the four workflows; v3 projection per workflow below):**

| Dir | Field | JSON Schema (App. B v2) | V12 validation | Blueprint storage target |
|---|---|---|---|---|
| in | `outcome_refs` | array maxItems=500 | array (typed references or structured items); input, validate authoriz | lcy_outcome.id[] (ENT-158) |
| in | `attribution_model_ref` | string format=uuid | UUID / scoped external reference; input, validate authorized scope | attribution model registry (AU-096) |
| in | `period` | string maxLength=512 | string / ISO 8601 interval (start/end); input, validate authorized sco | daterange / ISO period |
| in | `assumption_refs` | array maxItems=500 | array (typed references or structured items); input, validate authoriz | aut_artifact items (forecast assumptions) |
| out | `report_ref` | string format=uuid | UUID / scoped external reference; output, validate schema and evidence | ana_metric_snapshot / aut_artifact report |
| out | `attributed_minor` | integer minimum=0 | int64, nonnegative except signed ledger deltas; output, validate schem | numeric(18,4) ↔ int64 minor |
| out | `forecast_minor` | integer minimum=0 | int64, nonnegative except signed ledger deltas; output, validate schem | ana_forecast amount ↔ int64 minor (label: estimate) |
| out | `error_metric` | string pattern=^-?\d{1,14}(\.\d{1,4})?$ | decimal; unit and bounds defined by metric policy; output, validate sc | numeric MAPE (KPI-29) (V12 string: GAP-824) |
| out | `confidence` | string pattern=^-?\d{1,14}(\.\d{1,4})?$ | decimal; unit and bounds defined by metric policy; output, validate sc | numeric 0–1 + interval (V12 string: GAP-824) |

#### SM-SVC-24-WF01 Revenue and attribution calculation

| Field | Specification |
|---|---|
| V12 sources | BRD ch09 row; FSD ch12 lines 10333–10434; FSD ch13 registry row; App. B `urn:sm:dto:SM-SVC-24-WF01:v2`; workbook row "SM-SVC-24-WF01 — Revenue and attribution calculation" |
| Business outcome | Revenue and attribution calculation. Input → output: Verified outcome and source events → Revenue attribution report |
| Detailed functionality (workbook) | Deduplicate outcome; reconcile currency and source; calculate approved attribution model |
| Blueprint mapping | AU-040 / AU-096 attribution (Part 9.8b); agents AG-053; automations AU-040, AU-096 |
| What V12 adds | Attribution and revenue reconciliation exist; V12 adds currency/source reconciliation step and typed report. |
| Behaviour status | Partially covered → Matched |
| Trigger (V12) | Manual request or validated upstream business event; Verified outcome and source events |
| Trigger kinds (registry, DEC-564) | `manual` (NT13-03); `event` (NT13-01; `sm.svc24.wf01.requested` or upstream domain event, §11.4b.6); `child_workflow` (registered dependency, depth ≤ 3) |
| Authority (V12) | R0 internal analysis/draft; L1 assisted; L3 approved read/draft; Finance validates revenue, attribution model and forecast assumptions; no guaranteed results |
| Blueprint autonomy (DEC-566) | V12 L1 assisted / L3 approved read-draft → blueprint **L0–L1** (drafts and analysis only; no external effect). Approver: R08, R02 |
| Human approval (workbook) | Finance validates revenue, attribution model and forecast assumptions; no guaranteed results |
| Effect boundary | No external effect; internal artifacts only |
| Outputs produced (v3 projection) | `report_ref`, `attributed_minor`, `confidence` |
| Workflow KPI | attribution reconciliation; unmatched outcome rate; baseline and threshold approved in pilot; source service KPI Revenue reconciliation 100% or explicit exception; forecast error tracked |
| Preconditions / failure handling | Common contract (D-F12-030 variant 1, D-F12-031): §11.4b.5 |
| Cost | V12 illustrative ₹0.15/invocation (excludes provider, retry, labour). Blueprint model estimate ₹0.00/run for 0 agent step(s) at Tier 1b (Part 7.3 prices, FX ₹90/USD, verify at time of implementation, as of 27 Nov 2026); Tier 2 not eligible (Confidential/personal data) |
| Usage limit (pilot, not approved) | Illustrative pilot: 100 analytics review(s)/month; 1 concurrent run; configurable hard budget, provider quota and frequency limits. Not approved. |
| Data modalities / version | Text; structured records; service 2.0-target, workflow 2.0-target |
| Acceptance (V12 → blueprint) | SM-SVC-24-WF01-TC-{POS,INPUT,SCOPE,ENT,DUP,QUALITY,BUDGET,RECOVERY} → TC-V12-D-101…108; SM-SVC-24-WF01-AT01 → TC-V12-D-111 |
| Release proposal | R2 (W5) alignment |

| Step ID | Action (V12) | V12 executor → node type | Blueprint handler | Output contract | Failure → run state | Model tier | Status |
|---|---|---|---|---|---|---|---|
| SM-SVC-24-WF01-STEP-01 | Deduplicate outcome | Identity/reconciliation engine → NT13-07 `logic.compute` | AU-096 registered function | match_result {matched_refs,unmatched_refs,conflict_refs} | CONFLICT → HELD | Tier 0 / none | Matched |
| SM-SVC-24-WF01-STEP-02 | reconcile currency and source | Identity/reconciliation engine → NT13-07 `logic.compute` | AU-096 registered function | match_result {matched_refs,unmatched_refs,conflict_refs} | CONFLICT → HELD | Tier 0 / none | Matched |
| SM-SVC-24-WF01-STEP-03 | calculate approved attribution model | Rules/analytics engine → NT13-07 `logic.compute` | AU-040 registered function | calculation {value,unit,assumptions,evidence_refs} | INVALID_METRIC → HELD | Tier 0 / none | Matched |

#### SM-SVC-24-WF02 Sales pipeline forecast

| Field | Specification |
|---|---|
| V12 sources | BRD ch09 row; FSD ch12 lines 10435–10536; FSD ch13 registry row; App. B `urn:sm:dto:SM-SVC-24-WF02:v2`; workbook row "SM-SVC-24-WF02 — Sales pipeline forecast" |
| Business outcome | Sales pipeline forecast. Input → output: Stage probabilities and verified pipeline → Forecast scenario |
| Detailed functionality (workbook) | Validate assumptions; calculate deterministic forecast scenarios; disclose uncertainty |
| Blueprint mapping | WF-29 forecast call (Part 9.8b); agents AG-054; automations AU-041, AU-087 |
| What V12 adds | Stage-weighted forecast exists; V12 adds explicit assumption validation and scenario set. |
| Behaviour status | Partially covered → Matched |
| Trigger (V12) | Manual request or validated upstream business event; Stage probabilities and verified pipeline |
| Trigger kinds (registry, DEC-564) | `manual` (NT13-03); `event` (NT13-01; `sm.svc24.wf02.requested` or upstream domain event, §11.4b.6); `child_workflow` (registered dependency, depth ≤ 3) |
| Authority (V12) | R0 internal analysis/draft; L1 assisted; L3 approved read/draft; Finance validates revenue, attribution model and forecast assumptions; no guaranteed results |
| Blueprint autonomy (DEC-566) | V12 L1 assisted / L3 approved read-draft → blueprint **L0–L1** (drafts and analysis only; no external effect). Approver: R02, R08 |
| Human approval (workbook) | Finance validates revenue, attribution model and forecast assumptions; no guaranteed results |
| Effect boundary | No external effect; internal artifacts only |
| Outputs produced (v3 projection) | `report_ref`, `forecast_minor`, `confidence` |
| Workflow KPI | forecast arithmetic accuracy; assumption coverage; baseline and threshold approved in pilot; source service KPI Revenue reconciliation 100% or explicit exception; forecast error tracked |
| Preconditions / failure handling | Common contract (D-F12-030 variant 1, D-F12-031): §11.4b.5 |
| Cost | V12 illustrative ₹0.51/invocation (excludes provider, retry, labour). Blueprint model estimate ₹0.00/run for 0 agent step(s) at Tier 1b (Part 7.3 prices, FX ₹90/USD, verify at time of implementation, as of 27 Nov 2026); Tier 2 not eligible (Confidential/personal data) |
| Usage limit (pilot, not approved) | Illustrative pilot: 100 analytics review(s)/month; 1 concurrent run; configurable hard budget, provider quota and frequency limits. Not approved. |
| Data modalities / version | Text; structured records; service 2.0-target, workflow 2.0-target |
| Acceptance (V12 → blueprint) | SM-SVC-24-WF02-TC-{POS,INPUT,SCOPE,ENT,DUP,QUALITY,BUDGET,RECOVERY} → TC-V12-D-101…108; SM-SVC-24-WF02-AT01 → TC-V12-D-111 |
| Release proposal | R2 (W5) alignment |

| Step ID | Action (V12) | V12 executor → node type | Blueprint handler | Output contract | Failure → run state | Model tier | Status |
|---|---|---|---|---|---|---|---|
| SM-SVC-24-WF02-STEP-01 | Validate assumptions | Policy/validation engine → NT13-09 `policy.check` | PDP (AU-009) rule set | validation {passed,reason_codes,policy_version} | POLICY_DENIED → BLOCKED | Tier 0 / none | Matched |
| SM-SVC-24-WF02-STEP-02 | calculate deterministic forecast scenarios | Rules/analytics engine → NT13-07 `logic.compute` | AU-041 registered function | calculation {value,unit,assumptions,evidence_refs} | INVALID_METRIC → HELD | Tier 0 / none | Matched |
| SM-SVC-24-WF02-STEP-03 | disclose uncertainty | Domain service → NT13-05 `data.write_internal` | `analytics.revenue` service (revision check) | domain_result {artifact_ref,status,evidence_refs} | INVALID_STATE → HELD | Tier 0 / none | Matched |

#### SM-SVC-24-WF03 Performance and optimization review

| Field | Specification |
|---|---|
| V12 sources | BRD ch09 row; FSD ch12 lines 10537–10644; FSD ch13 registry row; App. B `urn:sm:dto:SM-SVC-24-WF03:v2`; workbook row "SM-SVC-24-WF03 — Performance and optimization review" |
| Business outcome | Performance and optimization review. Input → output: KPIs, costs and prior outcomes → Optimization action plan |
| Detailed functionality (workbook) | Compare against target; identify bottlenecks; propose controlled changes; record baseline |
| Blueprint mapping | Part 2.4 RP-02, RP-16, RP-17 reviews; agents AG-029, AG-080; automations AU-097, AU-102 |
| What V12 adds | Weekly narratives exist (AG-029); V12 adds bottleneck identification and controlled-change proposals with baseline. |
| Behaviour status | Partially covered → Matched |
| Trigger (V12) | Scheduled or manual; scoped event on change; KPIs, costs and prior outcomes |
| Trigger kinds (registry, DEC-564) | `manual` (NT13-03); `scheduled` (NT13-02; default cadence per §11.4b, misfire `reschedule_once`); `event` (NT13-01; `sm.svc24.wf03.requested` or upstream domain event, §11.4b.6) |
| Authority (V12) | R0 internal analysis/draft; L1 assisted; L3 approved read/draft; Finance validates revenue, attribution model and forecast assumptions; no guaranteed results |
| Blueprint autonomy (DEC-566) | V12 L1 assisted / L3 approved read-draft → blueprint **L0–L1** (drafts and analysis only; no external effect). Approver: R02 |
| Human approval (workbook) | Finance validates revenue, attribution model and forecast assumptions; no guaranteed results |
| Effect boundary | No external effect; internal artifacts only |
| Outputs produced (v3 projection) | `report_ref` |
| Workflow KPI | baseline coverage; improvement measurement rate; baseline and threshold approved in pilot; source service KPI Revenue reconciliation 100% or explicit exception; forecast error tracked |
| Preconditions / failure handling | Common contract (D-F12-030 variant 1, D-F12-031): §11.4b.5 |
| Cost | V12 illustrative ₹1.01/invocation (excludes provider, retry, labour). Blueprint model estimate ₹2.52/run for 2 agent step(s) at Tier 1b (Part 7.3 prices, FX ₹90/USD, verify at time of implementation, as of 27 Nov 2026); Tier 2 not eligible (Confidential/personal data) |
| Usage limit (pilot, not approved) | Illustrative pilot: 100 analytics review(s)/month; 1 concurrent run; configurable hard budget, provider quota and frequency limits. Not approved. |
| Data modalities / version | Text; structured records; service 2.0-target, workflow 2.0-target |
| Acceptance (V12 → blueprint) | SM-SVC-24-WF03-TC-{POS,INPUT,SCOPE,ENT,DUP,QUALITY,BUDGET,RECOVERY} → TC-V12-D-101…108; SM-SVC-24-WF03-AT01 → TC-V12-D-111 |
| Release proposal | R2 (W5) alignment |

| Step ID | Action (V12) | V12 executor → node type | Blueprint handler | Output contract | Failure → run state | Model tier | Status |
|---|---|---|---|---|---|---|---|
| SM-SVC-24-WF03-STEP-01 | Compare against target | Rules/analytics engine → NT13-07 `logic.compute` | AU-097 registered function | calculation {value,unit,assumptions,evidence_refs} | INVALID_METRIC → HELD | Tier 0 / none | Matched |
| SM-SVC-24-WF03-STEP-02 | identify bottlenecks | Domain agent → NT13-08 `ai.task` + NT13-10 `approval.human` | AG-080 via gateway; routed to R02 | candidate {artifact_ref,confidence,reason_codes,review_state} | REVIEW_REQUIRED → AWAITING_APPROVAL | Tier 1b | Matched |
| SM-SVC-24-WF03-STEP-03 | propose controlled changes | Domain agent → NT13-08 `ai.task` + NT13-10 `approval.human` | AG-029 via gateway; routed to R02 | candidate {artifact_ref,confidence,reason_codes,review_state} | REVIEW_REQUIRED → AWAITING_APPROVAL | Tier 1b | Matched |
| SM-SVC-24-WF03-STEP-04 | record baseline | Domain service → NT13-05 `data.write_internal` | `analytics.revenue` service (revision check) | domain_result {artifact_ref,status,evidence_refs} | INVALID_STATE → HELD | Tier 0 / none | Matched |

#### SM-SVC-24-WF04 Revenue scenario simulation and forecast calibration

| Field | Specification |
|---|---|
| V12 sources | BRD ch09 row; FSD ch12 lines 10645–10752; FSD ch13 registry row; App. B `urn:sm:dto:SM-SVC-24-WF04:v2`; workbook row "SM-SVC-24-WF04 — Revenue scenario simulation and forecast calibration" |
| Business outcome | Revenue scenario simulation and forecast calibration. Input → output: Verified revenue, pipeline probabilities, assumptions → Forecast range and calibration report |
| Detailed functionality (workbook) | Calculate scenarios; backtest forecasts; report error and uncertainty; recommend changes |
| Blueprint mapping | AU-041 backtest (KPI-29 MAPE); agents AG-054; automations AU-041 |
| What V12 adds | Backtest exists; V12 adds scenario simulation and calibration report. |
| Behaviour status | Partially covered → Matched |
| Trigger (V12) | Manual; scheduled or relevant validated business event; provider webhook only where authorized; Verified revenue, pipeline probabilities, assumptions |
| Trigger kinds (registry, DEC-564) | `manual` (NT13-03); `scheduled` (NT13-02; default cadence per §11.4b, misfire `reschedule_once`); `event` (NT13-01; `sm.svc24.wf04.requested` or upstream domain event, §11.4b.6); `provider_callback` (signed, replay-checked) |
| Authority (V12) | R0 internal analysis/draft; L1 assisted; L3 approved read/draft; Approve source/data rights and applicable external actions; approve consequential communications, commitments and changes; routine steps only within preapproved policies. |
| Blueprint autonomy (DEC-566) | V12 L1 assisted / L3 approved read-draft → blueprint **L0–L1** (drafts and analysis only; no external effect). Approver: R08 |
| Human approval (workbook) | Approve source/data rights and applicable external actions; approve consequential communications, commitments and changes; routine steps only within preapproved policies. |
| Effect boundary | No external effect; internal artifacts only |
| Outputs produced (v3 projection) | `report_ref`, `forecast_minor`, `error_metric`, `confidence` |
| Workflow KPI | backtest error; interval coverage; baseline and threshold approved in pilot; source service KPI Revenue reconciliation 100% or explicit exception; forecast error tracked |
| Preconditions / failure handling | Common contract (D-F12-030 variant 2, D-F12-031): §11.4b.5 |
| Cost | V12 illustrative ₹1.05/invocation (excludes provider, retry, labour). Blueprint model estimate ₹1.26/run for 1 agent step(s) at Tier 1b (Part 7.3 prices, FX ₹90/USD, verify at time of implementation, as of 27 Nov 2026); Tier 2 not eligible (Confidential/personal data) |
| Usage limit (pilot, not approved) | Illustrative pilot: 100 analytics review(s)/month; 1 concurrent run; configurable hard budget, provider quota and frequency limits. Not approved. |
| Data modalities / version | Text; structured records; service 1.0-target, workflow 1.0-target |
| Acceptance (V12 → blueprint) | SM-SVC-24-WF04-TC-{POS,INPUT,SCOPE,ENT,DUP,QUALITY,BUDGET,RECOVERY} → TC-V12-D-101…108; SM-SVC-24-WF04-AT01 → TC-V12-D-111 |
| Release proposal | A1 |

| Step ID | Action (V12) | V12 executor → node type | Blueprint handler | Output contract | Failure → run state | Model tier | Status |
|---|---|---|---|---|---|---|---|
| SM-SVC-24-WF04-STEP-01 | Calculate scenarios | Rules/analytics engine → NT13-07 `logic.compute` | AU-041 registered function | calculation {value,unit,assumptions,evidence_refs} | INVALID_METRIC → HELD | Tier 0 / none | Matched |
| SM-SVC-24-WF04-STEP-02 | backtest forecasts | Rules/analytics engine → NT13-07 `logic.compute` | AU-041 registered function | calculation {value,unit,assumptions,evidence_refs} | INVALID_METRIC → HELD | Tier 0 / none | Matched |
| SM-SVC-24-WF04-STEP-03 | report error and uncertainty | Domain service → NT13-05 `data.write_internal` | `analytics.revenue` service (revision check) | domain_result {artifact_ref,status,evidence_refs} | INVALID_STATE → HELD | Tier 0 / none | Matched |
| SM-SVC-24-WF04-STEP-04 | recommend changes | Domain agent → NT13-08 `ai.task` + NT13-10 `approval.human` | AG-054 via gateway; routed to R08 | candidate {artifact_ref,confidence,reason_codes,review_state} | REVIEW_REQUIRED → AWAITING_APPROVAL | Tier 1b | Matched |

### 11.4.5.14 SM-SVC-25 Business Document & Knowledge Intelligence Automation

| Field | Specification |
|---|---|
| Family / objective | Document intelligence; Maintain scoped approved business knowledge and prepare reusable commercial documents |
| Channels / providers | Private workspace, authorized document exchange; Secure file storage and permitted document processing; optional OCR if needed |
| Optional producers / complementary | Included foundation; no mandatory upstream paid service; optional input producers: None; authorized equivalent input accepted. |
| Service KPI | Evidence grounding ≥95%; unauthorized retrieval = 0 |
| Availability / bundle | Full suite / Lifecycle & Business Intelligence bundle / selective (1 SKU); entitlement and usage approval required. |
| Interoperability / readiness | Optional authorized connector; external agent access disabled unless explicitly granted; Proposed; test and validate customer demand, provider access and economics |
| Open-source stack | Python; Django REST Framework; PostgreSQL; Celery / Beat; Valkey; pgvector if needed; approved extraction libraries |
| Blueprint epic / module | EP-02 (ASSUMPTION-826) / `catalog.knowledge` |
| Effect adapter | none |
| Service guardrail | All knowledge edits go through the M03 approval pipeline; no cross-client retrieval (RLS + per-startup index). |
| Functional requirement | FR-V12-D-125 (§11.4.5.29 register) |

**DTO `urn:sm:dto:SM-SVC-25-WF0n:v2` (one schema shared by the four workflows; v3 projection per workflow below):**

| Dir | Field | JSON Schema (App. B v2) | V12 validation | Blueprint storage target |
|---|---|---|---|---|
| in | `document_ref` | string format=uuid | UUID / scoped external reference; input, validate authorized scope | cat_document.id (ENT-024) |
| in | `taxonomy_ref` | string format=uuid | UUID / scoped external reference; input, validate authorized scope | document taxonomy registry |
| in | `claim_refs` | array maxItems=500 | array (typed references or structured items); input, validate authoriz | cat_claim.id[] (ENT-020) |
| in | `revision` | integer minimum=1 | positive integer; input, validate authorized scope | integer ≥ 1 (optimistic version) |
| out | `document_version` | integer minimum=1 | positive integer; output, validate schema and evidence | cat_document.revision |
| out | `claim_version_refs` | array maxItems=500 | array (typed references or structured items); output, validate schema  | cat_claim revision ids |
| out | `review_state` | string maxLength=64 | string / configured enum; length and allowed values in versioned schem | enum {staged, in_review, approved, rejected, held} |
| out | `correction_refs` | array maxItems=500 | array (typed references or structured items); output, validate schema  | aut_artifact items (correction queue) |

#### SM-SVC-25-WF01 Document intake and classification

| Field | Specification |
|---|---|
| V12 sources | BRD ch09 row; FSD ch12 lines 10754–10858; FSD ch13 registry row; App. B `urn:sm:dto:SM-SVC-25-WF01:v2`; workbook row "SM-SVC-25-WF01 — Document intake and classification" |
| Business outcome | Document intake and classification. Input → output: Authorized document and taxonomy → Indexed document and metadata |
| Detailed functionality (workbook) | Scan file; extract permitted text and metadata; classify; stage for reviewer |
| Blueprint mapping | WF-01 knowledge ingestion (§2.7); agents AG-001; automations AU-005, AU-004, AU-007 |
| What V12 adds | Upload, scan, extract and classify exist (AG-001); V12 adds typed taxonomy output and stage-for-review step. |
| Behaviour status | Partially covered → Matched |
| Trigger (V12) | Authorized business event or manual import; signed webhook if applicable; Authorized document and taxonomy |
| Trigger kinds (registry, DEC-564) | `manual` (NT13-03); `event` (NT13-01; `sm.svc25.wf01.requested` or upstream domain event, §11.4b.6); `provider_callback` (signed, replay-checked) |
| Authority (V12) | R0 internal analysis/draft; L1 assisted; L3 approved read/draft; Approve source rights, claims, sensitive content and revisions; no cross-client retrieval |
| Blueprint autonomy (DEC-566) | V12 L1 assisted / L3 approved read-draft → blueprint **L0–L1** (drafts and analysis only; no external effect). Approver: R10 |
| Human approval (workbook) | Approve source rights, claims, sensitive content and revisions; no cross-client retrieval |
| Effect boundary | No external effect; internal artifacts only |
| Outputs produced (v3 projection) | `document_version`, `review_state` |
| Workflow KPI | classification accuracy; unsafe file rejection; baseline and threshold approved in pilot; source service KPI Evidence grounding ≥95%; unauthorized retrieval = 0 |
| Preconditions / failure handling | Common contract (D-F12-030 variant 1, D-F12-031): §11.4b.5 |
| Cost | V12 illustrative ₹1.13/invocation (excludes provider, retry, labour). Blueprint model estimate ₹0.03/run for 1 agent step(s) at Tier 1b (Part 7.3 prices, FX ₹90/USD, verify at time of implementation, as of 27 Nov 2026); Tier 2 not eligible (Confidential/personal data) |
| Usage limit (pilot, not approved) | Illustrative pilot: 200 document processed(s)/month; 1 concurrent run; configurable hard budget, provider quota and frequency limits. Not approved. |
| Data modalities / version | Text; structured records; documents; service 2.0-target, workflow 2.0-target |
| Acceptance (V12 → blueprint) | SM-SVC-25-WF01-TC-{POS,INPUT,SCOPE,ENT,DUP,QUALITY,BUDGET,RECOVERY} → TC-V12-D-101…108; SM-SVC-25-WF01-AT01 → TC-V12-D-111 |
| Release proposal | R1 (W0) alignment |

| Step ID | Action (V12) | V12 executor → node type | Blueprint handler | Output contract | Failure → run state | Model tier | Status |
|---|---|---|---|---|---|---|---|
| SM-SVC-25-WF01-STEP-01 | Scan file | Evidence/ingestion engine → NT13-04 `data.read` | AU-007 source permission + AU-005 sanitizer, scoped read | evidence_set {items,source_ref,observed_at,hash,rights} | SOURCE_DENIED → HELD | Tier 0 / none | Matched |
| SM-SVC-25-WF01-STEP-02 | extract permitted text and metadata | Evidence/ingestion engine → NT13-04 `data.read` | AU-007 source permission + AU-005 sanitizer, scoped read | evidence_set {items,source_ref,observed_at,hash,rights} | SOURCE_DENIED → HELD | Tier 0 / none | Matched |
| SM-SVC-25-WF01-STEP-03 | classify | Domain agent → NT13-08 `ai.task` + NT13-10 `approval.human` | AG-001 via gateway; routed to R10 | candidate {artifact_ref,confidence,reason_codes,review_state} | REVIEW_REQUIRED → AWAITING_APPROVAL | Tier 1a | Matched |
| SM-SVC-25-WF01-STEP-04 | stage for reviewer | Domain service → NT13-05 `data.write_internal` | `catalog.knowledge` service (revision check) | domain_result {artifact_ref,status,evidence_refs} | INVALID_STATE → HELD | Tier 0 / none | Matched |

#### SM-SVC-25-WF02 Knowledge grounding and revision

| Field | Specification |
|---|---|
| V12 sources | BRD ch09 row; FSD ch12 lines 10859–10963; FSD ch13 registry row; App. B `urn:sm:dto:SM-SVC-25-WF02:v2`; workbook row "SM-SVC-25-WF02 — Knowledge grounding and revision" |
| Business outcome | Knowledge grounding and revision. Input → output: Approved facts and existing knowledge → Versioned knowledge entries |
| Detailed functionality (workbook) | Deduplicate claims; compare versions; cite source; approve and refresh scoped index |
| Blueprint mapping | WF-22 knowledge freshness (Part 9.7b); agents AG-055; automations AU-069, AU-046 |
| What V12 adds | Claim dedupe, version compare and re-index exist; V12 binds them to step IDs. |
| Behaviour status | Partially covered → Matched |
| Trigger (V12) | Manual request or validated upstream business event; Approved facts and existing knowledge |
| Trigger kinds (registry, DEC-564) | `manual` (NT13-03); `event` (NT13-01; `sm.svc25.wf02.requested` or upstream domain event, §11.4b.6); `child_workflow` (registered dependency, depth ≤ 3) |
| Authority (V12) | R1 scoped state write or safety control; L1/L2 review; L3 only for approved deterministic internal actions; Approve source rights, claims, sensitive content and revisions; no cross-client retrieval |
| Blueprint autonomy (DEC-566) | V12 L1/L2 review; L3 only for approved deterministic internal actions → blueprint **L1** for state writes, **L3** only for registered deterministic internal steps (DEC-064). Approver: R10 |
| Human approval (workbook) | Approve source rights, claims, sensitive content and revisions; no cross-client retrieval |
| Effect boundary | No external effect; internal artifacts only |
| Outputs produced (v3 projection) | `claim_version_refs` |
| Workflow KPI | claim provenance coverage; stale index rate; baseline and threshold approved in pilot; source service KPI Evidence grounding ≥95%; unauthorized retrieval = 0 |
| Preconditions / failure handling | Common contract (D-F12-030 variant 1, D-F12-031): §11.4b.5 |
| Cost | V12 illustrative ₹1.35/invocation (excludes provider, retry, labour). Blueprint model estimate ₹0.00/run for 0 agent step(s) at Tier 1b (Part 7.3 prices, FX ₹90/USD, verify at time of implementation, as of 27 Nov 2026); Tier 2 not eligible (Confidential/personal data) |
| Usage limit (pilot, not approved) | Illustrative pilot: 200 document processed(s)/month; 1 concurrent run; configurable hard budget, provider quota and frequency limits. Not approved. |
| Data modalities / version | Text; structured records; service 2.0-target, workflow 2.0-target |
| Acceptance (V12 → blueprint) | SM-SVC-25-WF02-TC-{POS,INPUT,SCOPE,ENT,DUP,QUALITY,BUDGET,RECOVERY} → TC-V12-D-101…108; SM-SVC-25-WF02-AT01 → TC-V12-D-111 |
| Release proposal | R1 alignment |

| Step ID | Action (V12) | V12 executor → node type | Blueprint handler | Output contract | Failure → run state | Model tier | Status |
|---|---|---|---|---|---|---|---|
| SM-SVC-25-WF02-STEP-01 | Deduplicate claims | Identity/reconciliation engine → NT13-07 `logic.compute` | AU-046 registered function | match_result {matched_refs,unmatched_refs,conflict_refs} | CONFLICT → HELD | Tier 0 / none | Matched |
| SM-SVC-25-WF02-STEP-02 | compare versions | Rules/analytics engine → NT13-07 `logic.compute` | AU-069 registered function | calculation {value,unit,assumptions,evidence_refs} | INVALID_METRIC → HELD | Tier 0 / none | Matched |
| SM-SVC-25-WF02-STEP-03 | cite source | Domain service → NT13-05 `data.write_internal` | `catalog.knowledge` service (revision check) | domain_result {artifact_ref,status,evidence_refs} | INVALID_STATE → HELD | Tier 0 / none | Matched |
| SM-SVC-25-WF02-STEP-04 | approve and refresh scoped index | Evidence/ingestion engine → NT13-04 `data.read` | AU-007 source permission + AU-005 sanitizer, scoped read | evidence_set {items,source_ref,observed_at,hash,rights} | SOURCE_DENIED → HELD | Tier 0 / none | Matched |

#### SM-SVC-25-WF03 Draft business document and expiry tracking

| Field | Specification |
|---|---|
| V12 sources | BRD ch09 row; FSD ch12 lines 10964–11068; FSD ch13 registry row; App. B `urn:sm:dto:SM-SVC-25-WF03:v2`; workbook row "SM-SVC-25-WF03 — Draft business document and expiry tracking" |
| Business outcome | Draft business document and expiry tracking. Input → output: Approved template, facts and due date → Draft document and task |
| Detailed functionality (workbook) | Retrieve evidence; prepare draft; validate claims; schedule expiry/reminder |
| Blueprint mapping | WF-09 templates; AU-063 expiry; agents AG-020; automations AU-036, AU-063, AU-012 |
| What V12 adds | Document assembly from approved templates exists; V12 adds expiry/reminder scheduling for every business document. |
| Behaviour status | Partially covered → Matched |
| Trigger (V12) | Scheduled or manual; scoped event on change; Approved template, facts and due date |
| Trigger kinds (registry, DEC-564) | `manual` (NT13-03); `scheduled` (NT13-02; default cadence per §11.4b, misfire `reschedule_once`); `event` (NT13-01; `sm.svc25.wf03.requested` or upstream domain event, §11.4b.6) |
| Authority (V12) | R1 scoped state write or safety control; L1/L2 review; L3 only for approved deterministic internal actions; Approve source rights, claims, sensitive content and revisions; no cross-client retrieval |
| Blueprint autonomy (DEC-566) | V12 L1/L2 review; L3 only for approved deterministic internal actions → blueprint **L1** for state writes, **L3** only for registered deterministic internal steps (DEC-064). Approver: R10, R02 |
| Human approval (workbook) | Approve source rights, claims, sensitive content and revisions; no cross-client retrieval |
| Effect boundary | No external effect; internal artifacts only |
| Outputs produced (v3 projection) | `document_version`, `claim_version_refs` |
| Workflow KPI | document fact accuracy; expiry task accuracy; baseline and threshold approved in pilot; source service KPI Evidence grounding ≥95%; unauthorized retrieval = 0 |
| Preconditions / failure handling | Common contract (D-F12-030 variant 1, D-F12-031): §11.4b.5 |
| Cost | V12 illustrative ₹1.27/invocation (excludes provider, retry, labour). Blueprint model estimate ₹2.52/run for 2 agent step(s) at Tier 1b (Part 7.3 prices, FX ₹90/USD, verify at time of implementation, as of 27 Nov 2026); Tier 2 not eligible (Confidential/personal data) |
| Usage limit (pilot, not approved) | Illustrative pilot: 200 document processed(s)/month; 1 concurrent run; configurable hard budget, provider quota and frequency limits. Not approved. |
| Data modalities / version | Text; structured records; documents; service 2.0-target, workflow 2.0-target |
| Acceptance (V12 → blueprint) | SM-SVC-25-WF03-TC-{POS,INPUT,SCOPE,ENT,DUP,QUALITY,BUDGET,RECOVERY} → TC-V12-D-101…108; SM-SVC-25-WF03-AT01 → TC-V12-D-111 |
| Release proposal | R2 alignment |

| Step ID | Action (V12) | V12 executor → node type | Blueprint handler | Output contract | Failure → run state | Model tier | Status |
|---|---|---|---|---|---|---|---|
| SM-SVC-25-WF03-STEP-01 | Retrieve evidence | Evidence/ingestion engine → NT13-04 `data.read` | AU-007 source permission + AU-005 sanitizer, scoped read | evidence_set {items,source_ref,observed_at,hash,rights} | SOURCE_DENIED → HELD | Tier 0 / none | Matched |
| SM-SVC-25-WF03-STEP-02 | prepare draft | Domain agent → NT13-08 `ai.task` + NT13-10 `approval.human` | AG-020 via gateway; routed to R10 | candidate {artifact_ref,confidence,reason_codes,review_state} | REVIEW_REQUIRED → AWAITING_APPROVAL | Tier 1b | Matched |
| SM-SVC-25-WF03-STEP-03 | validate claims | Policy/validation engine → NT13-09 `policy.check` | PDP (AU-009) rule set | validation {passed,reason_codes,policy_version} | POLICY_DENIED → BLOCKED | Tier 0 / none | Matched |
| SM-SVC-25-WF03-STEP-04 | schedule expiry/reminder | Domain agent → NT13-08 `ai.task` + NT13-10 `approval.human` | AG-020 via gateway; routed to R10 | candidate {artifact_ref,confidence,reason_codes,review_state} | REVIEW_REQUIRED → AWAITING_APPROVAL | Tier 1b | Matched |

#### SM-SVC-25-WF04 Continuous business knowledge validation and contradiction detection

| Field | Specification |
|---|---|
| V12 sources | BRD ch09 row; FSD ch12 lines 11069–11173; FSD ch13 registry row; App. B `urn:sm:dto:SM-SVC-25-WF04:v2`; workbook row "SM-SVC-25-WF04 — Continuous business knowledge validation and contradiction detection" |
| Business outcome | Continuous business knowledge validation and contradiction detection. Input → output: Approved knowledge revisions, provenance and expiry rules → Knowledge correction queue |
| Detailed functionality (workbook) | Detect conflicting or stale claims; trace source; hold affected outputs; request review |
| Blueprint mapping | WF-22; agents AG-055; automations AU-069, AU-009 |
| What V12 adds | Contradiction detection exists (AU-069, AG-055); V12 adds automatic hold of affected outputs. |
| Behaviour status | Partially covered → Matched |
| Trigger (V12) | Manual; scheduled or relevant validated business event; provider webhook only where authorized; Approved knowledge revisions, provenance and expiry rules |
| Trigger kinds (registry, DEC-564) | `manual` (NT13-03); `scheduled` (NT13-02; default cadence per §11.4b, misfire `reschedule_once`); `event` (NT13-01; `sm.svc25.wf04.requested` or upstream domain event, §11.4b.6); `provider_callback` (signed, replay-checked) |
| Authority (V12) | R0 internal analysis/draft; L1 assisted; L3 approved read/draft; Approve source/data rights and applicable external actions; approve consequential communications, commitments and changes; routine steps only within preapproved policies. |
| Blueprint autonomy (DEC-566) | V12 L1 assisted / L3 approved read-draft → blueprint **L0–L1** (drafts and analysis only; no external effect). Approver: R10 |
| Human approval (workbook) | Approve source/data rights and applicable external actions; approve consequential communications, commitments and changes; routine steps only within preapproved policies. |
| Effect boundary | No external effect; internal artifacts only |
| Outputs produced (v3 projection) | `claim_version_refs`, `review_state`, `correction_refs` |
| Workflow KPI | contradiction recall; stale claim hold rate; baseline and threshold approved in pilot; source service KPI Evidence grounding ≥95%; unauthorized retrieval = 0 |
| Preconditions / failure handling | Common contract (D-F12-030 variant 2, D-F12-031): §11.4b.5 |
| Cost | V12 illustrative ₹0.55/invocation (excludes provider, retry, labour). Blueprint model estimate ₹1.26/run for 1 agent step(s) at Tier 1b (Part 7.3 prices, FX ₹90/USD, verify at time of implementation, as of 27 Nov 2026); Tier 2 not eligible (Confidential/personal data) |
| Usage limit (pilot, not approved) | Illustrative pilot: 200 document processed(s)/month; 1 concurrent run; configurable hard budget, provider quota and frequency limits. Not approved. |
| Data modalities / version | Text; structured records; service 1.0-target, workflow 1.0-target |
| Acceptance (V12 → blueprint) | SM-SVC-25-WF04-TC-{POS,INPUT,SCOPE,ENT,DUP,QUALITY,BUDGET,RECOVERY} → TC-V12-D-101…108; SM-SVC-25-WF04-AT01 → TC-V12-D-111 |
| Release proposal | A1 |

| Step ID | Action (V12) | V12 executor → node type | Blueprint handler | Output contract | Failure → run state | Model tier | Status |
|---|---|---|---|---|---|---|---|
| SM-SVC-25-WF04-STEP-01 | Detect conflicting or stale claims | Domain agent → NT13-08 `ai.task` + NT13-10 `approval.human` | AG-055 via gateway; routed to R10 | candidate {artifact_ref,confidence,reason_codes,review_state} | REVIEW_REQUIRED → AWAITING_APPROVAL | Tier 1b | Matched |
| SM-SVC-25-WF04-STEP-02 | trace source | Domain service → NT13-05 `data.write_internal` | `catalog.knowledge` service (revision check) | domain_result {artifact_ref,status,evidence_refs} | INVALID_STATE → HELD | Tier 0 / none | Matched |
| SM-SVC-25-WF04-STEP-03 | hold affected outputs | Policy/validation engine → NT13-09 `policy.check` | PDP (AU-009) rule set | validation {passed,reason_codes,policy_version} | POLICY_DENIED → BLOCKED | Tier 0 / none | Matched |
| SM-SVC-25-WF04-STEP-04 | request review | Domain service → NT13-05 `data.write_internal` | `catalog.knowledge` service (revision check) | domain_result {artifact_ref,status,evidence_refs} | INVALID_STATE → HELD | Tier 0 / none | Matched |

### 11.4.5.15 SM-SVC-26 AI Voice & Intelligent Telephony Automation

| Field | Specification |
|---|---|
| Family / objective | Voice engagement; Manage authorized calls and voice enquiries |
| Channels / providers | Private Admin; approved client data and connectors; voice/telephony; Authorized telephony, speech recognition and synthesis; calling/recording permission |
| Optional producers / complementary | Included foundation; no mandatory upstream paid service; optional input producers: SM-SVC-07; SM-SVC-09; SM-SVC-10; authorized equivalent input accepted. |
| Service KPI | Consent and disclosure checks 100%; unauthorized calls = 0 |
| Availability / bundle | Full / Outreach & Conversations / selective (1 SKU); eligible inputs and approvals required. |
| Interoperability / readiness | Optional authorized connector; external agent access disabled unless explicitly granted; Provider, jurisdiction and specialist approval required before live operation |
| Open-source stack | Python; Django REST Framework; PostgreSQL; Celery/Beat; Valkey; pgvector if needed; specialist library/provider review pending |
| Blueprint epic / module | EP-08 (ASSUMPTION-826) / `engagement.voice` |
| Effect adapter | ADP-VOICE (telephony/CPaaS, not procured) |
| Service guardrail | Blocked by DEC-387 (voice deferred), DEC-218/DEC-386 (no recordings or transcripts) and DEC-392 (human-dialled calls only). |
| Functional requirement | FR-V12-D-126 (§11.4.5.29 register) |

**DTO `urn:sm:dto:SM-SVC-26-WF0n:v2` (one schema shared by the four workflows; v3 projection per workflow below):**

| Dir | Field | JSON Schema (App. B v2) | V12 validation | Blueprint storage target |
|---|---|---|---|---|
| in | `call_ref` | string format=uuid | UUID / scoped external reference; input, validate authorized scope | eng_call (proposed, ASSUMPTION-827) |
| in | `contact_ref` | string format=uuid | UUID / scoped external reference; input, validate authorized scope | intel_contact.id (ENT-074) |
| in | `script_ref` | string format=uuid | UUID / scoped external reference; input, validate authorized scope | eng_message_template (voice script) |
| in | `recording_permission_ref` | string format=uuid | UUID / scoped external reference; input, validate authorized scope | gov_consent.id (purpose = call_recording) |
| out | `disposition` | string maxLength=64 | string / configured enum; length and allowed values in versioned schem | enum call disposition registry |
| out | `transcript_ref` | string format=uuid | UUID / scoped external reference; output, validate schema and evidence | excluded by DEC-218 unless Founder approves |
| out | `booking_ref` | string format=uuid | UUID / scoped external reference; output, validate schema and evidence | eng_meeting.id (ENT-103) |
| out | `call_event_ref` | string format=uuid | UUID / scoped external reference; output, validate schema and evidence | eng_inbound_event / int_provider_event |

#### SM-SVC-26-WF01 Inbound AI voice enquiry and call routing

| Field | Specification |
|---|---|
| V12 sources | BRD ch09 row; FSD ch12 lines 11175–11273; FSD ch13 registry row; App. B `urn:sm:dto:SM-SVC-26-WF01:v2`; workbook row "SM-SVC-26-WF01 — Inbound AI voice enquiry and call routing" |
| Business outcome | Inbound AI voice enquiry and call routing. Input → output: Inbound call, approved knowledge, routing rules → Call disposition |
| Detailed functionality (workbook) | Disclose AI as required; classify intent; route or answer with evidence |
| Blueprint mapping | none (DEC-387); agents AG-058; automations AU-073 |
| What V12 adds | Inbound AI voice answering is deferred by DEC-387; WhatsApp concierge AG-058 is the nearest capability. |
| Behaviour status | Conflict → Pending Founder decision (CONFLICT-815) |
| Trigger (V12) | Manual; scheduled monitoring; validated business event; authorized provider webhook when available; Inbound call, approved knowledge, routing rules |
| Trigger kinds (registry, DEC-564) | `manual` (NT13-03); `scheduled` (NT13-02; default cadence per §11.4b, misfire `reschedule_once`); `event` (NT13-01; `sm.svc26.wf01.requested` or upstream domain event, §11.4b.6); `provider_callback` (signed, replay-checked) |
| Authority (V12) | R2 external communication/provider/access write; L2 mandatory approved effect; L3 only with separately approved bounded mandate where lawful; Approve source/data rights and applicable external actions; verify recipient permission, sender identity, disclosure, quiet hours and provider rules before contact. |
| Blueprint autonomy (DEC-566) | V12 L2 exact approved effect → blueprint **L1 approval of the exact payload hash, then L2 dispatch** of that item through the outbox (DEC-064 publishing pattern); V12 L3 mandate only for routine replies/reminders within caps. Approver: R10, R01 |
| Human approval (workbook) | Approve source/data rights and applicable external actions; verify recipient permission, sender identity, disclosure, quiet hours and provider rules before contact. |
| Effect boundary | No external effect; approval gate inserted before state change (DEC-570) |
| Outputs produced (v3 projection) | `disposition`, `call_event_ref` |
| Workflow KPI | routing accuracy; disclosure compliance; baseline and threshold approved in pilot; source service KPI Consent and disclosure checks 100%; unauthorized calls = 0 |
| Preconditions / failure handling | Common contract (D-F12-030 variant 2, D-F12-031): §11.4b.5 |
| Cost | V12 illustrative ₹0.55/invocation (excludes provider, retry, labour). Blueprint model estimate ₹1.29/run for 2 agent step(s) at Tier 1b (Part 7.3 prices, FX ₹90/USD, verify at time of implementation, as of 27 Nov 2026); Tier 2 not eligible (Confidential/personal data) |
| Usage limit (pilot, not approved) | Illustrative pilot: 100 Call minute(s)/month; 1 concurrent run; approved caps, provider quotas and hard budget required. |
| Data modalities / version | Text; structured records; audio/image/video where applicable and authorized; service 1.0-target, workflow 1.0-target |
| Acceptance (V12 → blueprint) | SM-SVC-26-WF01-TC-{POS,INPUT,SCOPE,ENT,DUP,QUALITY,BUDGET,RECOVERY,APPROVAL,EFFECT} → TC-V12-D-101…110; SM-SVC-26-WF01-AT01 → TC-V12-D-111 |
| Release proposal | Spec only (Founder) |

| Step ID | Action (V12) | V12 executor → node type | Blueprint handler | Output contract | Failure → run state | Model tier | Status |
|---|---|---|---|---|---|---|---|
| SM-SVC-26-WF01-STEP-01 | Disclose AI as required | Domain service → NT13-05 `data.write_internal` | `engagement.voice` service (revision check) | domain_result {artifact_ref,status,evidence_refs} | INVALID_STATE → HELD | Tier 0 / none | Pending Founder decision |
| SM-SVC-26-WF01-STEP-02 | classify intent | Domain agent → NT13-08 `ai.task` + NT13-10 `approval.human` | AG-058 via gateway; routed to R10 | candidate {artifact_ref,confidence,reason_codes,review_state} | REVIEW_REQUIRED → AWAITING_APPROVAL | Tier 1a | Pending Founder decision |
| SM-SVC-26-WF01-STEP-03 | route or answer with evidence | Domain agent → NT13-08 `ai.task` + NT13-10 `approval.human` | AG-058 via gateway; routed to R10 | candidate {artifact_ref,confidence,reason_codes,review_state} | REVIEW_REQUIRED → AWAITING_APPROVAL | Tier 1b | Pending Founder decision |

#### SM-SVC-26-WF02 Authorized outbound voice engagement

| Field | Specification |
|---|---|
| V12 sources | BRD ch09 row; FSD ch12 lines 11274–11372; FSD ch13 registry row; App. B `urn:sm:dto:SM-SVC-26-WF02:v2`; workbook row "SM-SVC-26-WF02 — Authorized outbound voice engagement" |
| Business outcome | Authorized outbound voice engagement. Input → output: Eligible contacts, call permission, approved script → Call event or hold |
| Detailed functionality (workbook) | Check consent, quiet hours and caps; initiate authorized call; record outcome |
| Blueprint mapping | WF-27 human call tasks (DEC-392); agents AG-011; automations AU-086, AU-009 |
| What V12 adds | Outbound AI-initiated calls conflict with DEC-392 (human-dialled only) and TR-R1 (no voice outreach W0-W5). |
| Behaviour status | Conflict → Pending Founder decision (CONFLICT-815) |
| Trigger (V12) | Manual; scheduled monitoring; validated business event; authorized provider webhook when available; Eligible contacts, call permission, approved script |
| Trigger kinds (registry, DEC-564) | `manual` (NT13-03); `scheduled` (NT13-02; default cadence per §11.4b, misfire `reschedule_once`); `event` (NT13-01; `sm.svc26.wf02.requested` or upstream domain event, §11.4b.6); `provider_callback` (signed, replay-checked) |
| Authority (V12) | R2 external communication/provider/access write; L2 mandatory approved effect; L3 only with separately approved bounded mandate where lawful; Approve source/data rights and applicable external actions; verify recipient permission, sender identity, disclosure, quiet hours and provider rules before contact. |
| Blueprint autonomy (DEC-566) | V12 L2 exact approved effect → blueprint **L1 approval of the exact payload hash, then L2 dispatch** of that item through the outbox (DEC-064 publishing pattern); V12 L3 mandate only for routine replies/reminders within caps. Approver: R10, R01 |
| Human approval (workbook) | Approve source/data rights and applicable external actions; verify recipient permission, sender identity, disclosure, quiet hours and provider rules before contact. |
| Effect boundary | Effect steps: STEP-02 via ADP-VOICE (telephony/CPaaS, not procured) |
| Outputs produced (v3 projection) | `call_event_ref` |
| Workflow KPI | unauthorized call count; call outcome reconciliation; baseline and threshold approved in pilot; source service KPI Consent and disclosure checks 100%; unauthorized calls = 0 |
| Preconditions / failure handling | Common contract (D-F12-030 variant 2, D-F12-031): §11.4b.5 |
| Cost | V12 illustrative ₹0.55/invocation (excludes provider, retry, labour). Blueprint model estimate ₹0.00/run for 0 agent step(s) at Tier 1b (Part 7.3 prices, FX ₹90/USD, verify at time of implementation, as of 27 Nov 2026); Tier 2 not eligible (Confidential/personal data) |
| Usage limit (pilot, not approved) | Illustrative pilot: 100 Call minute(s)/month; 1 concurrent run; approved caps, provider quotas and hard budget required. |
| Data modalities / version | Text; structured records; audio/image/video where applicable and authorized; service 1.0-target, workflow 1.0-target |
| Acceptance (V12 → blueprint) | SM-SVC-26-WF02-TC-{POS,INPUT,SCOPE,ENT,DUP,QUALITY,BUDGET,RECOVERY,APPROVAL,EFFECT} → TC-V12-D-101…110; SM-SVC-26-WF02-AT01 → TC-V12-D-111 |
| Release proposal | Spec only (Founder) |

| Step ID | Action (V12) | V12 executor → node type | Blueprint handler | Output contract | Failure → run state | Model tier | Status |
|---|---|---|---|---|---|---|---|
| SM-SVC-26-WF02-STEP-01 | Check consent, quiet hours and caps | Policy/validation engine → NT13-09 `policy.check` | PDP (AU-009) rule set | validation {passed,reason_codes,policy_version} | POLICY_DENIED → BLOCKED | Tier 0 / none | Pending Founder decision |
| SM-SVC-26-WF02-STEP-02 | initiate authorized call | Effect adapter → NT13-13 `action.external` | Outbox → AU-009 dispatch recheck → ADP-VOICE (telephony/CPaaS, not procured) | effect_receipt {provider_ref,status,observed_at} | EFFECT_UNKNOWN → RECONCILING | none | Pending Founder decision |
| SM-SVC-26-WF02-STEP-03 | record outcome | Domain service → NT13-05 `data.write_internal` | `engagement.voice` service (revision check) | domain_result {artifact_ref,status,evidence_refs} | INVALID_STATE → HELD | Tier 0 / none | Pending Founder decision |

#### SM-SVC-26-WF03 Multilingual voice conversation and appointment coordination

| Field | Specification |
|---|---|
| V12 sources | BRD ch09 row; FSD ch12 lines 11373–11471; FSD ch13 registry row; App. B `urn:sm:dto:SM-SVC-26-WF03:v2`; workbook row "SM-SVC-26-WF03 — Multilingual voice conversation and appointment coordination" |
| Business outcome | Multilingual voice conversation and appointment coordination. Input → output: Call session, language, calendar availability → Booking or handoff |
| Detailed functionality (workbook) | Recognize language; ground answers; confirm time with caller |
| Blueprint mapping | WF-07 meetings; agents AG-058, AG-050; automations AU-023 |
| What V12 adds | Multilingual voice conversation needs speech services deferred by DEC-387; booking logic exists (AU-023). |
| Behaviour status | Conflict → Pending Founder decision (CONFLICT-815) |
| Trigger (V12) | Manual; scheduled monitoring; validated business event; authorized provider webhook when available; Call session, language, calendar availability |
| Trigger kinds (registry, DEC-564) | `manual` (NT13-03); `scheduled` (NT13-02; default cadence per §11.4b, misfire `reschedule_once`); `event` (NT13-01; `sm.svc26.wf03.requested` or upstream domain event, §11.4b.6); `provider_callback` (signed, replay-checked) |
| Authority (V12) | R2 external communication/provider/access write; L2 mandatory approved effect; L3 only with separately approved bounded mandate where lawful; Approve source/data rights and applicable external actions; verify recipient permission, sender identity, disclosure, quiet hours and provider rules before contact. |
| Blueprint autonomy (DEC-566) | V12 L2 exact approved effect → blueprint **L1 approval of the exact payload hash, then L2 dispatch** of that item through the outbox (DEC-064 publishing pattern); V12 L3 mandate only for routine replies/reminders within caps. Approver: R10, R01 |
| Human approval (workbook) | Approve source/data rights and applicable external actions; verify recipient permission, sender identity, disclosure, quiet hours and provider rules before contact. |
| Effect boundary | No external effect; approval gate inserted before state change (DEC-570) |
| Outputs produced (v3 projection) | `booking_ref`, `call_event_ref` |
| Workflow KPI | language accuracy; booking confirmation rate; baseline and threshold approved in pilot; source service KPI Consent and disclosure checks 100%; unauthorized calls = 0 |
| Preconditions / failure handling | Common contract (D-F12-030 variant 2, D-F12-031): §11.4b.5 |
| Cost | V12 illustrative ₹0.55/invocation (excludes provider, retry, labour). Blueprint model estimate ₹0.00/run for 0 agent step(s) at Tier 1b (Part 7.3 prices, FX ₹90/USD, verify at time of implementation, as of 27 Nov 2026); Tier 2 not eligible (Confidential/personal data) |
| Usage limit (pilot, not approved) | Illustrative pilot: 100 Call minute(s)/month; 1 concurrent run; approved caps, provider quotas and hard budget required. |
| Data modalities / version | Text; structured records; audio/image/video where applicable and authorized; service 1.0-target, workflow 1.0-target |
| Acceptance (V12 → blueprint) | SM-SVC-26-WF03-TC-{POS,INPUT,SCOPE,ENT,DUP,QUALITY,BUDGET,RECOVERY,APPROVAL,EFFECT} → TC-V12-D-101…110; SM-SVC-26-WF03-AT01 → TC-V12-D-111 |
| Release proposal | Spec only (Founder) |

| Step ID | Action (V12) | V12 executor → node type | Blueprint handler | Output contract | Failure → run state | Model tier | Status |
|---|---|---|---|---|---|---|---|
| SM-SVC-26-WF03-STEP-01 | Recognize language | Evidence/ingestion engine → NT13-04 `data.read` | AU-007 source permission + AU-005 sanitizer, scoped read | evidence_set {items,source_ref,observed_at,hash,rights} | SOURCE_DENIED → HELD | Tier 0 / none | Pending Founder decision |
| SM-SVC-26-WF03-STEP-02 | ground answers | Domain service → NT13-05 `data.write_internal` | `engagement.voice` service (revision check) | domain_result {artifact_ref,status,evidence_refs} | INVALID_STATE → HELD | Tier 0 / none | Pending Founder decision |
| SM-SVC-26-WF03-STEP-03 | confirm time with caller | Domain service → NT13-05 `data.write_internal` | `engagement.voice` service (revision check) | domain_result {artifact_ref,status,evidence_refs} | INVALID_STATE → HELD | Tier 0 / none | Pending Founder decision |

#### SM-SVC-26-WF04 Call intelligence, permitted transcription and CRM synchronization

| Field | Specification |
|---|---|
| V12 sources | BRD ch09 row; FSD ch12 lines 11472–11570; FSD ch13 registry row; App. B `urn:sm:dto:SM-SVC-26-WF04:v2`; workbook row "SM-SVC-26-WF04 — Call intelligence, permitted transcription and CRM synchronization" |
| Business outcome | Call intelligence, permitted transcription and CRM synchronization. Input → output: Authorized recording or transcript, relationship ID → Call summary and CRM event |
| Detailed functionality (workbook) | Extract actions; redact restricted data; synchronize approved notes |
| Blueprint mapping | AG-037 staff-written notes (DEC-218); agents AG-037; automations AU-004 |
| What V12 adds | Call transcription conflicts with DEC-218/DEC-386 (recordings and transcripts excluded). |
| Behaviour status | Conflict → Pending Founder decision (CONFLICT-815) |
| Trigger (V12) | Manual; scheduled monitoring; validated business event; authorized provider webhook when available; Authorized recording or transcript, relationship ID |
| Trigger kinds (registry, DEC-564) | `manual` (NT13-03); `scheduled` (NT13-02; default cadence per §11.4b, misfire `reschedule_once`); `event` (NT13-01; `sm.svc26.wf04.requested` or upstream domain event, §11.4b.6); `provider_callback` (signed, replay-checked) |
| Authority (V12) | R1 scoped state write or safety control; L1/L2 review; L3 only for approved deterministic internal actions; Approve source/data rights and applicable external actions; verify recipient permission, sender identity, disclosure, quiet hours and provider rules before contact. |
| Blueprint autonomy (DEC-566) | V12 L1/L2 review; L3 only for approved deterministic internal actions → blueprint **L1** for state writes, **L3** only for registered deterministic internal steps (DEC-064). Approver: R10, R01 |
| Human approval (workbook) | Approve source/data rights and applicable external actions; verify recipient permission, sender identity, disclosure, quiet hours and provider rules before contact. |
| Effect boundary | No external effect; internal artifacts only |
| Outputs produced (v3 projection) | `transcript_ref`, `call_event_ref` |
| Workflow KPI | redaction recall; CRM sync correctness; baseline and threshold approved in pilot; source service KPI Consent and disclosure checks 100%; unauthorized calls = 0 |
| Preconditions / failure handling | Common contract (D-F12-030 variant 2, D-F12-031): §11.4b.5 |
| Cost | V12 illustrative ₹1.05/invocation (excludes provider, retry, labour). Blueprint model estimate ₹0.00/run for 0 agent step(s) at Tier 1b (Part 7.3 prices, FX ₹90/USD, verify at time of implementation, as of 27 Nov 2026); Tier 2 not eligible (Confidential/personal data) |
| Usage limit (pilot, not approved) | Illustrative pilot: 100 Call minute(s)/month; 1 concurrent run; approved caps, provider quotas and hard budget required. |
| Data modalities / version | Text; structured records; audio/image/video where applicable and authorized; service 1.0-target, workflow 1.0-target |
| Acceptance (V12 → blueprint) | SM-SVC-26-WF04-TC-{POS,INPUT,SCOPE,ENT,DUP,QUALITY,BUDGET,RECOVERY} → TC-V12-D-101…108; SM-SVC-26-WF04-AT01 → TC-V12-D-111 |
| Release proposal | Spec only (Founder) |

| Step ID | Action (V12) | V12 executor → node type | Blueprint handler | Output contract | Failure → run state | Model tier | Status |
|---|---|---|---|---|---|---|---|
| SM-SVC-26-WF04-STEP-01 | Extract actions | Evidence/ingestion engine → NT13-04 `data.read` | AU-007 source permission + AU-005 sanitizer, scoped read | evidence_set {items,source_ref,observed_at,hash,rights} | SOURCE_DENIED → HELD | Tier 0 / none | Pending Founder decision |
| SM-SVC-26-WF04-STEP-02 | redact restricted data | Domain service → NT13-05 `data.write_internal` | `engagement.voice` service (revision check) | domain_result {artifact_ref,status,evidence_refs} | INVALID_STATE → HELD | Tier 0 / none | Pending Founder decision |
| SM-SVC-26-WF04-STEP-03 | synchronize approved notes | Identity/reconciliation engine → NT13-07 `logic.compute` | AU-074 registered function | match_result {matched_refs,unmatched_refs,conflict_refs} | CONFLICT → HELD | Tier 0 / none | Pending Founder decision |

### 11.4.5.16 SM-SVC-27 Multimodal Creative & Localization Automation

| Field | Specification |
|---|---|
| Family / objective | Creative production; Produce approved visual, video and audio marketing material |
| Channels / providers | Private Admin; approved client data and connectors; Authorized image/video/audio generation and asset rights |
| Optional producers / complementary | Included foundation; no mandatory upstream paid service; optional input producers: SM-SVC-11; SM-SVC-12; SM-SVC-14; authorized equivalent input accepted. |
| Service KPI | Asset rights and factual claim review 100% before publication |
| Availability / bundle | Full / Digital Marketing & Acquisition / selective (1 SKU); eligible inputs and approvals required. |
| Interoperability / readiness | Optional authorized connector; external agent access disabled unless explicitly granted; Provider, jurisdiction and specialist approval required before live operation |
| Open-source stack | Python; Django REST Framework; PostgreSQL; Celery/Beat; Valkey; pgvector if needed; specialist library/provider review pending |
| Blueprint epic / module | EP-11 (ASSUMPTION-826) / `marketing.creative` |
| Effect adapter | ADP-MEDIA (generative media, not procured) |
| Service guardrail | CI-061 excluded image generation for cost and likeness risk; V12 re-introduces it. |
| Functional requirement | FR-V12-D-127 (§11.4.5.29 register) |

**DTO `urn:sm:dto:SM-SVC-27-WF0n:v2` (one schema shared by the four workflows; v3 projection per workflow below):**

| Dir | Field | JSON Schema (App. B v2) | V12 validation | Blueprint storage target |
|---|---|---|---|---|
| in | `brief_ref` | string format=uuid | UUID / scoped external reference; input, validate authorized scope | mkt_content_asset brief |
| in | `brand_ref` | string format=uuid | UUID / scoped external reference; input, validate authorized scope | brand kit config (tenant/startup) |
| in | `asset_rights_refs` | array maxItems=500 | array (typed references or structured items); input, validate authoriz | asset rights register rows |
| in | `target_language` | string maxLength=64 | string / configured enum; length and allowed values in versioned schem | BCP 47 tag; allowed set DEC-026 |
| out | `asset_ref` | string format=uuid | UUID / scoped external reference; output, validate schema and evidence | mkt_content_asset.id (ENT-105) |
| out | `revision` | integer minimum=1 | positive integer; output, validate schema and evidence | integer ≥ 1 (optimistic version) |
| out | `rights_state` | string maxLength=64 | string / configured enum; length and allowed values in versioned schem | enum {unknown, cleared, restricted, rejected} |
| out | `qa_state` | string maxLength=64 | string / configured enum; length and allowed values in versioned schem | enum {pending, passed, failed, held} |

#### SM-SVC-27-WF01 Marketing image and advertising creative generation

| Field | Specification |
|---|---|
| V12 sources | BRD ch09 row; FSD ch12 lines 11572–11670; FSD ch13 registry row; App. B `urn:sm:dto:SM-SVC-27-WF01:v2`; workbook row "SM-SVC-27-WF01 — Marketing image and advertising creative generation" |
| Business outcome | Marketing image and advertising creative generation. Input → output: Brand brief, asset rights, approved claims → Image drafts |
| Detailed functionality (workbook) | Generate variants; check layout and claims; route review |
| Blueprint mapping | WF-05 content (§2.11); agents AG-018; automations AU-076, AU-029 |
| What V12 adds | Image generation was excluded by CI-061 (cost, likeness, claims); approved brand assets are the baseline. |
| Behaviour status | Conflict → Pending Founder decision (CONFLICT-819) |
| Trigger (V12) | Manual; scheduled monitoring; validated business event; authorized provider webhook when available; Brand brief, asset rights, approved claims |
| Trigger kinds (registry, DEC-564) | `manual` (NT13-03); `scheduled` (NT13-02; default cadence per §11.4b, misfire `reschedule_once`); `event` (NT13-01; `sm.svc27.wf01.requested` or upstream domain event, §11.4b.6); `provider_callback` (signed, replay-checked) |
| Authority (V12) | R0 internal analysis/draft; L1 assisted; L3 approved read/draft; Approve source/data rights and applicable external actions; review rights, claims, brand and public publication. |
| Blueprint autonomy (DEC-566) | V12 L1 assisted / L3 approved read-draft → blueprint **L0–L1** (drafts and analysis only; no external effect). Approver: R05L, R10 |
| Human approval (workbook) | Approve source/data rights and applicable external actions; review rights, claims, brand and public publication. |
| Effect boundary | No external effect; internal artifacts only |
| Outputs produced (v3 projection) | `asset_ref`, `revision`, `rights_state`, `qa_state` |
| Workflow KPI | brand compliance; rights evidence coverage; baseline and threshold approved in pilot; source service KPI Asset rights and factual claim review 100% before publication |
| Preconditions / failure handling | Common contract (D-F12-030 variant 2, D-F12-031): §11.4b.5 |
| Cost | V12 illustrative ₹1.05/invocation (excludes provider, retry, labour). Blueprint model estimate ₹2.52/run for 2 agent step(s) at Tier 1b (Part 7.3 prices, FX ₹90/USD, verify at time of implementation, as of 27 Nov 2026); Tier 2 not eligible (Confidential/personal data) |
| Usage limit (pilot, not approved) | Illustrative pilot: 50 Creative asset(s)/month; 1 concurrent run; approved caps, provider quotas and hard budget required. |
| Data modalities / version | Text; structured records; audio/image/video where applicable and authorized; service 1.0-target, workflow 1.0-target |
| Acceptance (V12 → blueprint) | SM-SVC-27-WF01-TC-{POS,INPUT,SCOPE,ENT,DUP,QUALITY,BUDGET,RECOVERY} → TC-V12-D-101…108; SM-SVC-27-WF01-AT01 → TC-V12-D-111 |
| Release proposal | Spec only (Founder) |

| Step ID | Action (V12) | V12 executor → node type | Blueprint handler | Output contract | Failure → run state | Model tier | Status |
|---|---|---|---|---|---|---|---|
| SM-SVC-27-WF01-STEP-01 | Generate variants | Domain agent → NT13-08 `ai.task` + NT13-10 `approval.human` | AG-018 via gateway; routed to R05L | candidate {artifact_ref,confidence,reason_codes,review_state} | REVIEW_REQUIRED → AWAITING_APPROVAL | Tier 1b | Pending Founder decision |
| SM-SVC-27-WF01-STEP-02 | check layout and claims | Policy/validation engine → NT13-09 `policy.check` | PDP (AU-009) rule set | validation {passed,reason_codes,policy_version} | POLICY_DENIED → BLOCKED | Tier 0 / none | Matched |
| SM-SVC-27-WF01-STEP-03 | route review | Domain agent → NT13-08 `ai.task` + NT13-10 `approval.human` | AG-018 via gateway; routed to R05L | candidate {artifact_ref,confidence,reason_codes,review_state} | REVIEW_REQUIRED → AWAITING_APPROVAL | Tier 1b | Matched |

#### SM-SVC-27-WF02 Product demonstration and promotional video generation

| Field | Specification |
|---|---|
| V12 sources | BRD ch09 row; FSD ch12 lines 11671–11769; FSD ch13 registry row; App. B `urn:sm:dto:SM-SVC-27-WF02:v2`; workbook row "SM-SVC-27-WF02 — Product demonstration and promotional video generation" |
| Business outcome | Product demonstration and promotional video generation. Input → output: Product facts, approved storyboard, rights → Video draft |
| Detailed functionality (workbook) | Create storyboard and clips; validate factual depiction; review |
| Blueprint mapping | WF-05; agents AG-018; automations AU-029 |
| What V12 adds | Video generation is not in the blueprint; same exclusion basis as CI-061. |
| Behaviour status | Conflict → Pending Founder decision (CONFLICT-819) |
| Trigger (V12) | Manual; scheduled monitoring; validated business event; authorized provider webhook when available; Product facts, approved storyboard, rights |
| Trigger kinds (registry, DEC-564) | `manual` (NT13-03); `scheduled` (NT13-02; default cadence per §11.4b, misfire `reschedule_once`); `event` (NT13-01; `sm.svc27.wf02.requested` or upstream domain event, §11.4b.6); `provider_callback` (signed, replay-checked) |
| Authority (V12) | R0 internal analysis/draft; L1 assisted; L3 approved read/draft; Approve source/data rights and applicable external actions; review rights, claims, brand and public publication. |
| Blueprint autonomy (DEC-566) | V12 L1 assisted / L3 approved read-draft → blueprint **L0–L1** (drafts and analysis only; no external effect). Approver: R05L, R10 |
| Human approval (workbook) | Approve source/data rights and applicable external actions; review rights, claims, brand and public publication. |
| Effect boundary | No external effect; internal artifacts only |
| Outputs produced (v3 projection) | `asset_ref`, `revision`, `rights_state`, `qa_state` |
| Workflow KPI | factual depiction accuracy; storyboard adherence; baseline and threshold approved in pilot; source service KPI Asset rights and factual claim review 100% before publication |
| Preconditions / failure handling | Common contract (D-F12-030 variant 2, D-F12-031): §11.4b.5 |
| Cost | V12 illustrative ₹1.05/invocation (excludes provider, retry, labour). Blueprint model estimate ₹0.00/run for 0 agent step(s) at Tier 1b (Part 7.3 prices, FX ₹90/USD, verify at time of implementation, as of 27 Nov 2026); Tier 2 not eligible (Confidential/personal data) |
| Usage limit (pilot, not approved) | Illustrative pilot: 50 Creative asset(s)/month; 1 concurrent run; approved caps, provider quotas and hard budget required. |
| Data modalities / version | Text; structured records; audio/image/video where applicable and authorized; service 1.0-target, workflow 1.0-target |
| Acceptance (V12 → blueprint) | SM-SVC-27-WF02-TC-{POS,INPUT,SCOPE,ENT,DUP,QUALITY,BUDGET,RECOVERY} → TC-V12-D-101…108; SM-SVC-27-WF02-AT01 → TC-V12-D-111 |
| Release proposal | Spec only (Founder) |

| Step ID | Action (V12) | V12 executor → node type | Blueprint handler | Output contract | Failure → run state | Model tier | Status |
|---|---|---|---|---|---|---|---|
| SM-SVC-27-WF02-STEP-01 | Create storyboard and clips | Domain service → NT13-05 `data.write_internal` | `marketing.creative` service (revision check) | domain_result {artifact_ref,status,evidence_refs} | INVALID_STATE → HELD | Tier 0 / none | Pending Founder decision |
| SM-SVC-27-WF02-STEP-02 | validate factual depiction | Policy/validation engine → NT13-09 `policy.check` | PDP (AU-009) rule set | validation {passed,reason_codes,policy_version} | POLICY_DENIED → BLOCKED | Tier 0 / none | Matched |
| SM-SVC-27-WF02-STEP-03 | review | Domain service → NT13-05 `data.write_internal` | `marketing.creative` service (revision check) | domain_result {artifact_ref,status,evidence_refs} | INVALID_STATE → HELD | Tier 0 / none | Matched |

#### SM-SVC-27-WF03 Multilingual audio, subtitle and creative localization

| Field | Specification |
|---|---|
| V12 sources | BRD ch09 row; FSD ch12 lines 11770–11868; FSD ch13 registry row; App. B `urn:sm:dto:SM-SVC-27-WF03:v2`; workbook row "SM-SVC-27-WF03 — Multilingual audio, subtitle and creative localization" |
| Business outcome | Multilingual audio, subtitle and creative localization. Input → output: Approved asset, target language, voice rights → Localized asset |
| Detailed functionality (workbook) | Translate and localize; generate captions/audio; quality review |
| Blueprint mapping | WF-19 localization (Part 9.7b); agents AG-050; automations AU-076 |
| What V12 adds | Text/subtitle localization exists (AG-050, AU-076); synthetic audio is new and needs a speech provider. |
| Behaviour status | Conflict → Pending Founder decision (CONFLICT-819) |
| Trigger (V12) | Manual; scheduled monitoring; validated business event; authorized provider webhook when available; Approved asset, target language, voice rights |
| Trigger kinds (registry, DEC-564) | `manual` (NT13-03); `scheduled` (NT13-02; default cadence per §11.4b, misfire `reschedule_once`); `event` (NT13-01; `sm.svc27.wf03.requested` or upstream domain event, §11.4b.6); `provider_callback` (signed, replay-checked) |
| Authority (V12) | R0 internal analysis/draft; L1 assisted; L3 approved read/draft; Approve source/data rights and applicable external actions; review rights, claims, brand and public publication. |
| Blueprint autonomy (DEC-566) | V12 L1 assisted / L3 approved read-draft → blueprint **L0–L1** (drafts and analysis only; no external effect). Approver: R05L |
| Human approval (workbook) | Approve source/data rights and applicable external actions; review rights, claims, brand and public publication. |
| Effect boundary | No external effect; internal artifacts only |
| Outputs produced (v3 projection) | `asset_ref`, `revision`, `qa_state` |
| Workflow KPI | translation accuracy; caption sync quality; baseline and threshold approved in pilot; source service KPI Asset rights and factual claim review 100% before publication |
| Preconditions / failure handling | Common contract (D-F12-030 variant 2, D-F12-031): §11.4b.5 |
| Cost | V12 illustrative ₹1.05/invocation (excludes provider, retry, labour). Blueprint model estimate ₹1.26/run for 1 agent step(s) at Tier 1b (Part 7.3 prices, FX ₹90/USD, verify at time of implementation, as of 27 Nov 2026); Tier 2 not eligible (Confidential/personal data) |
| Usage limit (pilot, not approved) | Illustrative pilot: 50 Creative asset(s)/month; 1 concurrent run; approved caps, provider quotas and hard budget required. |
| Data modalities / version | Text; structured records; audio/image/video where applicable and authorized; service 1.0-target, workflow 1.0-target |
| Acceptance (V12 → blueprint) | SM-SVC-27-WF03-TC-{POS,INPUT,SCOPE,ENT,DUP,QUALITY,BUDGET,RECOVERY} → TC-V12-D-101…108; SM-SVC-27-WF03-AT01 → TC-V12-D-111 |
| Release proposal | A2 text part; audio Spec only |

| Step ID | Action (V12) | V12 executor → node type | Blueprint handler | Output contract | Failure → run state | Model tier | Status |
|---|---|---|---|---|---|---|---|
| SM-SVC-27-WF03-STEP-01 | Translate and localize | Domain service → NT13-05 `data.write_internal` | `marketing.creative` service (revision check) | domain_result {artifact_ref,status,evidence_refs} | INVALID_STATE → HELD | Tier 0 / none | Matched |
| SM-SVC-27-WF03-STEP-02 | generate captions/audio | Domain agent → NT13-08 `ai.task` + NT13-10 `approval.human` | AG-050 via gateway; routed to R05L | candidate {artifact_ref,confidence,reason_codes,review_state} | REVIEW_REQUIRED → AWAITING_APPROVAL | Tier 1b | Pending Founder decision |
| SM-SVC-27-WF03-STEP-03 | quality review | Domain service → NT13-05 `data.write_internal` | `marketing.creative` service (revision check) | domain_result {artifact_ref,status,evidence_refs} | INVALID_STATE → HELD | Tier 0 / none | Matched |

#### SM-SVC-27-WF04 Brand, copyright, factual claim and creative quality validation

| Field | Specification |
|---|---|
| V12 sources | BRD ch09 row; FSD ch12 lines 11869–11967; FSD ch13 registry row; App. B `urn:sm:dto:SM-SVC-27-WF04:v2`; workbook row "SM-SVC-27-WF04 — Brand, copyright, factual claim and creative quality validation" |
| Business outcome | Brand, copyright, factual claim and creative quality validation. Input → output: Asset draft, brand rules, licensing evidence → Creative QA record |
| Detailed functionality (workbook) | Review claims and rights; flag inconsistencies; approve or hold |
| Blueprint mapping | WF-05 claim approval; AU-029 publication; agents AG-012, AG-076; automations AU-029, AU-036 |
| What V12 adds | Claims guard and publication hash checks exist; V12 adds rights and brand checks for every creative asset. |
| Behaviour status | Partially covered → Matched |
| Trigger (V12) | Manual; scheduled monitoring; validated business event; authorized provider webhook when available; Asset draft, brand rules, licensing evidence |
| Trigger kinds (registry, DEC-564) | `manual` (NT13-03); `scheduled` (NT13-02; default cadence per §11.4b, misfire `reschedule_once`); `event` (NT13-01; `sm.svc27.wf04.requested` or upstream domain event, §11.4b.6); `provider_callback` (signed, replay-checked) |
| Authority (V12) | R0 internal analysis/draft; L1 assisted; L3 approved read/draft; Approve source/data rights and applicable external actions; review rights, claims, brand and public publication. |
| Blueprint autonomy (DEC-566) | V12 L1 assisted / L3 approved read-draft → blueprint **L0–L1** (drafts and analysis only; no external effect). Approver: R10, R05L |
| Human approval (workbook) | Approve source/data rights and applicable external actions; review rights, claims, brand and public publication. |
| Effect boundary | No external effect; internal artifacts only |
| Outputs produced (v3 projection) | `rights_state`, `qa_state` |
| Workflow KPI | rights violation detection; claim validation recall; baseline and threshold approved in pilot; source service KPI Asset rights and factual claim review 100% before publication |
| Preconditions / failure handling | Common contract (D-F12-030 variant 2, D-F12-031): §11.4b.5 |
| Cost | V12 illustrative ₹0.55/invocation (excludes provider, retry, labour). Blueprint model estimate ₹0.03/run for 1 agent step(s) at Tier 1b (Part 7.3 prices, FX ₹90/USD, verify at time of implementation, as of 27 Nov 2026); Tier 2 not eligible (Confidential/personal data) |
| Usage limit (pilot, not approved) | Illustrative pilot: 50 Creative asset(s)/month; 1 concurrent run; approved caps, provider quotas and hard budget required. |
| Data modalities / version | Text; structured records; audio/image/video where applicable and authorized; service 1.0-target, workflow 1.0-target |
| Acceptance (V12 → blueprint) | SM-SVC-27-WF04-TC-{POS,INPUT,SCOPE,ENT,DUP,QUALITY,BUDGET,RECOVERY} → TC-V12-D-101…108; SM-SVC-27-WF04-AT01 → TC-V12-D-111 |
| Release proposal | R1 alignment |

| Step ID | Action (V12) | V12 executor → node type | Blueprint handler | Output contract | Failure → run state | Model tier | Status |
|---|---|---|---|---|---|---|---|
| SM-SVC-27-WF04-STEP-01 | Review claims and rights | Domain service → NT13-05 `data.write_internal` | `marketing.creative` service (revision check) | domain_result {artifact_ref,status,evidence_refs} | INVALID_STATE → HELD | Tier 0 / none | Matched |
| SM-SVC-27-WF04-STEP-02 | flag inconsistencies | Domain agent → NT13-08 `ai.task` + NT13-10 `approval.human` | AG-076 via gateway; routed to R10 | candidate {artifact_ref,confidence,reason_codes,review_state} | REVIEW_REQUIRED → AWAITING_APPROVAL | Tier 1a | Matched |
| SM-SVC-27-WF04-STEP-03 | approve or hold | Policy/validation engine → NT13-09 `policy.check` | PDP (AU-009) rule set | validation {passed,reason_codes,policy_version} | POLICY_DENIED → BLOCKED | Tier 0 / none | Matched |

### 11.4.5.17 SM-SVC-28 Agentic Commerce & AI-to-AI Business Transaction Automation

| Field | Specification |
|---|---|
| Family / objective | Agentic commerce; Exchange offers and coordinate transactions with authorized agents |
| Channels / providers | Private Admin; approved client data and connectors; authorized agent-to-agent exchange; Supported agent protocols and authorized payment/commerce providers; verified mandates |
| Optional producers / complementary | Included foundation; no mandatory upstream paid service; optional input producers: SM-SVC-15; SM-SVC-17; SM-SVC-18; SM-SVC-20; SM-SVC-21; authorized equivalent input accepted. |
| Service KPI | Verified mandate and idempotency 100%; unauthorized transactions = 0 |
| Availability / bundle | Full / Commerce & Procurement / selective (1 SKU); eligible inputs and approvals required. |
| Interoperability / readiness | Protocol-agnostic agent/tool adapter; MCP/A2A or equivalent only after identity, scope, schema and provider validation; Design now; provider/protocol interoperability, security and mandate validation required before activation |
| Open-source stack | Python; Django REST Framework; PostgreSQL; Celery/Beat; Valkey; pgvector if needed; specialist library/provider review pending |
| Blueprint epic / module | EP-13 (ASSUMPTION-826) / `commerce.agentic` |
| Effect adapter | ADP-AGENT (MCP/A2A gateway, not procured) |
| Service guardrail | AI never signs, pays, submits or sets prices; external agents are untrusted callers (R18-equivalent) with scoped grants. |
| Functional requirement | FR-V12-D-128 (§11.4.5.29 register) |

**DTO `urn:sm:dto:SM-SVC-28-WF0n:v2` (one schema shared by the four workflows; v3 projection per workflow below):**

| Dir | Field | JSON Schema (App. B v2) | V12 validation | Blueprint storage target |
|---|---|---|---|---|
| in | `agent_ref` | string format=uuid | UUID / scoped external reference; input, validate authorized scope | int_external_agent (proposed) |
| in | `mandate_ref` | string format=uuid | UUID / scoped external reference; input, validate authorized scope | gov_mandate (proposed) |
| in | `offering_ref` | string format=uuid | UUID / scoped external reference; input, validate authorized scope | cat_offering.id (ENT-016) |
| in | `order_ref` | string format=uuid | UUID / scoped external reference; input, validate authorized scope | com_order.id (WF-10) |
| out | `quote_ref` | string format=uuid | UUID / scoped external reference; output, validate schema and evidence | com_quote.id (ENT-127) |
| out | `mandate_state` | string maxLength=64 | string / configured enum; length and allowed values in versioned schem | enum {draft, approved, expired, revoked} |
| out | `transaction_ref` | string format=uuid | UUID / scoped external reference; output, validate schema and evidence | com_payment / provider reference (record only) |
| out | `reconciliation_state` | string maxLength=64 | string / configured enum; length and allowed values in versioned schem | enum {staged, matched, partial, mismatch, exception, reconciled} |

#### SM-SVC-28-WF01 Machine-readable product and service catalog publication

| Field | Specification |
|---|---|
| V12 sources | BRD ch09 row; FSD ch12 lines 11969–12067; FSD ch13 registry row; App. B `urn:sm:dto:SM-SVC-28-WF01:v2`; workbook row "SM-SVC-28-WF01 — Machine-readable product and service catalog publication" |
| Business outcome | Machine-readable product and service catalog publication. Input → output: Approved offering catalog, access policy, structured schema → Machine-readable catalog |
| Detailed functionality (workbook) | Validate fields; publish to authorized client endpoint; record version |
| Blueprint mapping | WF-01 product truth; W-portal catalogue; agents AG-012; automations AU-029, AU-089 |
| What V12 adds | New: publish a machine-readable catalogue (approved offerings and price-book references) to an authorized client endpoint. |
| Behaviour status | Not covered → Matched |
| Trigger (V12) | Manual; scheduled monitoring; validated business event; authorized provider webhook when available; Approved offering catalog, access policy, structured schema |
| Trigger kinds (registry, DEC-564) | `manual` (NT13-03); `scheduled` (NT13-02; default cadence per §11.4b, misfire `reschedule_once`); `event` (NT13-01; `sm.svc28.wf01.requested` or upstream domain event, §11.4b.6); `provider_callback` (signed, replay-checked) |
| Authority (V12) | R2 external communication/provider/access write; L2 mandatory approved effect; L3 only with separately approved bounded mandate where lawful; Approve source/data rights and applicable external actions; verify agent identity, mandate, spending limits and approval before any transaction; reconcile via authorized provider. |
| Blueprint autonomy (DEC-566) | V12 L2 exact approved effect → blueprint **L1 approval of the exact payload hash, then L2 dispatch** of that item through the outbox (DEC-064 publishing pattern); V12 L3 mandate only for routine replies/reminders within caps. Approver: R02, R10 |
| Human approval (workbook) | Approve source/data rights and applicable external actions; verify agent identity, mandate, spending limits and approval before any transaction; reconcile via authorized provider. |
| Effect boundary | Effect steps: STEP-02 via ADP-AGENT (MCP/A2A gateway, not procured) |
| Outputs produced (v3 projection) | none of the shared output fields fit; `catalog_version_ref` proposed (GAP-824) |
| Workflow KPI | catalog schema accuracy; unauthorized exposure count; baseline and threshold approved in pilot; source service KPI Verified mandate and idempotency 100%; unauthorized transactions = 0 |
| Preconditions / failure handling | Common contract (D-F12-030 variant 2, D-F12-031): §11.4b.5 |
| Cost | V12 illustrative ₹0.55/invocation (excludes provider, retry, labour). Blueprint model estimate ₹0.00/run for 0 agent step(s) at Tier 1a (Part 7.3 prices, FX ₹90/USD, verify at time of implementation, as of 27 Nov 2026); Tier 2 not eligible (Confidential/personal data) |
| Usage limit (pilot, not approved) | Illustrative pilot: 50 Agent transaction case(s)/month; 1 concurrent run; approved caps, provider quotas and hard budget required. |
| Data modalities / version | Text; structured records; service 1.0-target, workflow 1.0-target |
| Acceptance (V12 → blueprint) | SM-SVC-28-WF01-TC-{POS,INPUT,SCOPE,ENT,DUP,QUALITY,BUDGET,RECOVERY,APPROVAL,EFFECT} → TC-V12-D-101…110; SM-SVC-28-WF01-AT01 → TC-V12-D-111 |
| Release proposal | A2 |

| Step ID | Action (V12) | V12 executor → node type | Blueprint handler | Output contract | Failure → run state | Model tier | Status |
|---|---|---|---|---|---|---|---|
| SM-SVC-28-WF01-STEP-01 | Validate fields | Policy/validation engine → NT13-09 `policy.check` | PDP (AU-009) rule set + AU-089 | validation {passed,reason_codes,policy_version} | POLICY_DENIED → BLOCKED | Tier 0 / none | Matched |
| SM-SVC-28-WF01-STEP-02 | publish to authorized client endpoint | Effect adapter → NT13-13 `action.external` | Outbox → AU-009 dispatch recheck → ADP-AGENT (MCP/A2A gateway, not procured) | effect_receipt {provider_ref,status,observed_at} | EFFECT_UNKNOWN → RECONCILING | none | Matched |
| SM-SVC-28-WF01-STEP-03 | record version | Domain service → NT13-05 `data.write_internal` | `commerce.agentic` service (revision check) | domain_result {artifact_ref,status,evidence_refs} | INVALID_STATE → HELD | Tier 0 / none | Matched |

#### SM-SVC-28-WF02 Authorized AI-agent requirement discovery and quotation exchange

| Field | Specification |
|---|---|
| V12 sources | BRD ch09 row; FSD ch12 lines 12068–12166; FSD ch13 registry row; App. B `urn:sm:dto:SM-SVC-28-WF02:v2`; workbook row "SM-SVC-28-WF02 — Authorized AI-agent requirement discovery and quotation exchange" |
| Business outcome | Authorized AI-agent requirement discovery and quotation exchange. Input → output: Verified agent identity, scoped mandate, requirements → Authorized quote exchange |
| Detailed functionality (workbook) | Validate identity and schema; match approved offerings; return scoped quotation draft |
| Blueprint mapping | WF-09 quote (§2.15); agents AG-066; automations AU-089, AU-080 |
| What V12 adds | New: accept requirement requests from verified external agents and return a quotation draft priced only by AU-089 from approved price books; human approves before release. |
| Behaviour status | Not covered → Matched |
| Trigger (V12) | Manual; scheduled monitoring; validated business event; authorized provider webhook when available; Verified agent identity, scoped mandate, requirements |
| Trigger kinds (registry, DEC-564) | `manual` (NT13-03); `scheduled` (NT13-02; default cadence per §11.4b, misfire `reschedule_once`); `event` (NT13-01; `sm.svc28.wf02.requested` or upstream domain event, §11.4b.6); `provider_callback` (signed, replay-checked) |
| Authority (V12) | R2 external communication/provider/access write; L2 mandatory approved effect; L3 only with separately approved bounded mandate where lawful; Approve source/data rights and applicable external actions; verify agent identity, mandate, spending limits and approval before any transaction; reconcile via authorized provider. |
| Blueprint autonomy (DEC-566) | V12 L2 exact approved effect → blueprint **L1 approval of the exact payload hash, then L2 dispatch** of that item through the outbox (DEC-064 publishing pattern); V12 L3 mandate only for routine replies/reminders within caps. Approver: R03L, R02 |
| Human approval (workbook) | Approve source/data rights and applicable external actions; verify agent identity, mandate, spending limits and approval before any transaction; reconcile via authorized provider. |
| Effect boundary | No external effect; approval gate inserted before state change (DEC-570) |
| Outputs produced (v3 projection) | `quote_ref` |
| Workflow KPI | mandate validation; quote scope accuracy; baseline and threshold approved in pilot; source service KPI Verified mandate and idempotency 100%; unauthorized transactions = 0 |
| Preconditions / failure handling | Common contract (D-F12-030 variant 2, D-F12-031): §11.4b.5 |
| Cost | V12 illustrative ₹0.55/invocation (excludes provider, retry, labour). Blueprint model estimate ₹1.26/run for 1 agent step(s) at Tier 1a (Part 7.3 prices, FX ₹90/USD, verify at time of implementation, as of 27 Nov 2026); Tier 2 not eligible (Confidential/personal data) |
| Usage limit (pilot, not approved) | Illustrative pilot: 50 Agent transaction case(s)/month; 1 concurrent run; approved caps, provider quotas and hard budget required. |
| Data modalities / version | Text; structured records; service 1.0-target, workflow 1.0-target |
| Acceptance (V12 → blueprint) | SM-SVC-28-WF02-TC-{POS,INPUT,SCOPE,ENT,DUP,QUALITY,BUDGET,RECOVERY,APPROVAL,EFFECT} → TC-V12-D-101…110; SM-SVC-28-WF02-AT01 → TC-V12-D-111 |
| Release proposal | A3 |

| Step ID | Action (V12) | V12 executor → node type | Blueprint handler | Output contract | Failure → run state | Model tier | Status |
|---|---|---|---|---|---|---|---|
| SM-SVC-28-WF02-STEP-01 | Validate identity and schema | Policy/validation engine → NT13-09 `policy.check` | PDP (AU-009) rule set + AU-089 | validation {passed,reason_codes,policy_version} | POLICY_DENIED → BLOCKED | Tier 0 / none | Matched |
| SM-SVC-28-WF02-STEP-02 | match approved offerings | Identity/reconciliation engine → NT13-07 `logic.compute` | AU-080 registered function | match_result {matched_refs,unmatched_refs,conflict_refs} | CONFLICT → HELD | Tier 0 / none | Matched |
| SM-SVC-28-WF02-STEP-03 | return scoped quotation draft | Domain agent → NT13-08 `ai.task` + NT13-10 `approval.human` | AG-066 via gateway; routed to R03L | candidate {artifact_ref,confidence,reason_codes,review_state} | REVIEW_REQUIRED → AWAITING_APPROVAL | Tier 1b | Matched |

#### SM-SVC-28-WF03 Agent-assisted purchasing and negotiation mandate coordination

| Field | Specification |
|---|---|
| V12 sources | BRD ch09 row; FSD ch12 lines 12167–12265; FSD ch13 registry row; App. B `urn:sm:dto:SM-SVC-28-WF03:v2`; workbook row "SM-SVC-28-WF03 — Agent-assisted purchasing and negotiation mandate coordination" |
| Business outcome | Agent-assisted purchasing and negotiation mandate coordination. Input → output: Mandate, price limits, negotiation policy → Mandate-linked decision |
| Detailed functionality (workbook) | Validate authority and budget; compare offers; route consequential decisions |
| Blueprint mapping | WF-09 negotiation; agents AG-021; automations AU-089, AU-009 |
| What V12 adds | Agent-to-agent negotiation mandates conflict with "AI never sets prices" and DEC-064 L1 caps. |
| Behaviour status | Conflict → Pending Founder decision (CONFLICT-816) |
| Trigger (V12) | Manual; scheduled monitoring; validated business event; authorized provider webhook when available; Mandate, price limits, negotiation policy |
| Trigger kinds (registry, DEC-564) | `manual` (NT13-03); `scheduled` (NT13-02; default cadence per §11.4b, misfire `reschedule_once`); `event` (NT13-01; `sm.svc28.wf03.requested` or upstream domain event, §11.4b.6); `provider_callback` (signed, replay-checked) |
| Authority (V12) | R3 financial/legal/commitment; L2 mandatory approved effect; L3 only with separately approved bounded mandate where lawful; Approve source/data rights and applicable external actions; verify agent identity, mandate, spending limits and approval before any transaction; reconcile via authorized provider. |
| Blueprint autonomy (DEC-566) | V12 L2 default → blueprint **L1 maximum** (human approval bound to the exact hash; money movement not supported, DEC-064). V12 "L3 bounded mandate" **not adopted** (CONFLICT-814, Pending Founder decision). Approver: R02, R08 |
| Human approval (workbook) | Approve source/data rights and applicable external actions; verify agent identity, mandate, spending limits and approval before any transaction; reconcile via authorized provider. |
| Effect boundary | No external effect; approval gate inserted before state change (DEC-570) |
| Outputs produced (v3 projection) | `mandate_state` |
| Workflow KPI | budget violation rejection; decision traceability; baseline and threshold approved in pilot; source service KPI Verified mandate and idempotency 100%; unauthorized transactions = 0 |
| Preconditions / failure handling | Common contract (D-F12-030 variant 2, D-F12-031): §11.4b.5 |
| Cost | V12 illustrative ₹0.55/invocation (excludes provider, retry, labour). Blueprint model estimate ₹0.03/run for 1 agent step(s) at Tier 1a (Part 7.3 prices, FX ₹90/USD, verify at time of implementation, as of 27 Nov 2026); Tier 2 not eligible (Confidential/personal data) |
| Usage limit (pilot, not approved) | Illustrative pilot: 50 Agent transaction case(s)/month; 1 concurrent run; approved caps, provider quotas and hard budget required. |
| Data modalities / version | Text; structured records; service 1.0-target, workflow 1.0-target |
| Acceptance (V12 → blueprint) | SM-SVC-28-WF03-TC-{POS,INPUT,SCOPE,ENT,DUP,QUALITY,BUDGET,RECOVERY,APPROVAL,EFFECT} → TC-V12-D-101…110; SM-SVC-28-WF03-AT01 → TC-V12-D-111 |
| Release proposal | Spec only (Founder) |

| Step ID | Action (V12) | V12 executor → node type | Blueprint handler | Output contract | Failure → run state | Model tier | Status |
|---|---|---|---|---|---|---|---|
| SM-SVC-28-WF03-STEP-01 | Validate authority and budget | Policy/validation engine → NT13-09 `policy.check` | PDP (AU-009) rule set + AU-089 | validation {passed,reason_codes,policy_version} | POLICY_DENIED → BLOCKED | Tier 0 / none | Matched |
| SM-SVC-28-WF03-STEP-02 | compare offers | Rules/analytics engine → NT13-07 `logic.compute` | AU-089 registered function | calculation {value,unit,assumptions,evidence_refs} | INVALID_METRIC → HELD | Tier 0 / none | Pending Founder decision |
| SM-SVC-28-WF03-STEP-03 | route consequential decisions | Domain agent → NT13-08 `ai.task` + NT13-10 `approval.human` | AG-021 via gateway; routed to R02 | candidate {artifact_ref,confidence,reason_codes,review_state} | REVIEW_REQUIRED → AWAITING_APPROVAL | Tier 1a | Pending Founder decision |

#### SM-SVC-28-WF04 Authorized transaction, payment mandate and outcome reconciliation

| Field | Specification |
|---|---|
| V12 sources | BRD ch09 row; FSD ch12 lines 12266–12364; FSD ch13 registry row; App. B `urn:sm:dto:SM-SVC-28-WF04:v2`; workbook row "SM-SVC-28-WF04 — Authorized transaction, payment mandate and outcome reconciliation" |
| Business outcome | Authorized transaction, payment mandate and outcome reconciliation. Input → output: Approved order, verified payment mandate, provider event → Auditable transaction record |
| Detailed functionality (workbook) | Verify authorization; execute only via approved provider; reconcile uncertain outcome |
| Blueprint mapping | WF-11 closure; agents AG-024; automations AU-037, AU-026 |
| What V12 adds | Payment mandates conflict with "money movement not supported" (DEC-064) and "AI never pays". |
| Behaviour status | Conflict → Pending Founder decision (CONFLICT-816) |
| Trigger (V12) | Manual; scheduled monitoring; validated business event; authorized provider webhook when available; Approved order, verified payment mandate, provider event |
| Trigger kinds (registry, DEC-564) | `manual` (NT13-03); `scheduled` (NT13-02; default cadence per §11.4b, misfire `reschedule_once`); `event` (NT13-01; `sm.svc28.wf04.requested` or upstream domain event, §11.4b.6); `provider_callback` (signed, replay-checked) |
| Authority (V12) | R3 financial/legal/commitment; L2 mandatory approved effect; L3 only with separately approved bounded mandate where lawful; Approve source/data rights and applicable external actions; verify agent identity, mandate, spending limits and approval before any transaction; reconcile via authorized provider. |
| Blueprint autonomy (DEC-566) | V12 L2 default → blueprint **L1 maximum** (human approval bound to the exact hash; money movement not supported, DEC-064). V12 "L3 bounded mandate" **not adopted** (CONFLICT-814, Pending Founder decision). Approver: R08, R09, R01 |
| Human approval (workbook) | Approve source/data rights and applicable external actions; verify agent identity, mandate, spending limits and approval before any transaction; reconcile via authorized provider. |
| Effect boundary | Effect steps: STEP-02 via ADP-AGENT (MCP/A2A gateway, not procured) |
| Outputs produced (v3 projection) | `mandate_state`, `transaction_ref`, `reconciliation_state` |
| Workflow KPI | duplicate transaction count; reconciliation accuracy; baseline and threshold approved in pilot; source service KPI Verified mandate and idempotency 100%; unauthorized transactions = 0 |
| Preconditions / failure handling | Common contract (D-F12-030 variant 2, D-F12-031): §11.4b.5 |
| Cost | V12 illustrative ₹0.55/invocation (excludes provider, retry, labour). Blueprint model estimate ₹0.00/run for 0 agent step(s) at Tier 1a (Part 7.3 prices, FX ₹90/USD, verify at time of implementation, as of 27 Nov 2026); Tier 2 not eligible (Confidential/personal data) |
| Usage limit (pilot, not approved) | Illustrative pilot: 50 Agent transaction case(s)/month; 1 concurrent run; approved caps, provider quotas and hard budget required. |
| Data modalities / version | Text; structured records; service 1.0-target, workflow 1.0-target |
| Acceptance (V12 → blueprint) | SM-SVC-28-WF04-TC-{POS,INPUT,SCOPE,ENT,DUP,QUALITY,BUDGET,RECOVERY,APPROVAL,EFFECT} → TC-V12-D-101…110; SM-SVC-28-WF04-AT01 → TC-V12-D-111 |
| Release proposal | Spec only (Founder) |

| Step ID | Action (V12) | V12 executor → node type | Blueprint handler | Output contract | Failure → run state | Model tier | Status |
|---|---|---|---|---|---|---|---|
| SM-SVC-28-WF04-STEP-01 | Verify authorization | Policy/validation engine → NT13-09 `policy.check` | PDP (AU-009) rule set | validation {passed,reason_codes,policy_version} | POLICY_DENIED → BLOCKED | Tier 0 / none | Matched |
| SM-SVC-28-WF04-STEP-02 | execute only via approved provider | Effect adapter → NT13-13 `action.external` | Outbox → AU-009 dispatch recheck → ADP-AGENT (MCP/A2A gateway, not procured) | effect_receipt {provider_ref,status,observed_at} | EFFECT_UNKNOWN → RECONCILING | none | Pending Founder decision |
| SM-SVC-28-WF04-STEP-03 | reconcile uncertain outcome | Identity/reconciliation engine → NT13-07 `logic.compute` | AU-037 registered function | match_result {matched_refs,unmatched_refs,conflict_refs} | CONFLICT → HELD | Tier 0 / none | Pending Founder decision |

### 11.4.5.18 SM-SVC-29 Account-Based Marketing & Enterprise Buying Group Automation

| Field | Specification |
|---|---|
| Family / objective | Account intelligence; Coordinate acquisition across enterprise stakeholders |
| Channels / providers | Private Admin; approved client data and connectors; Authorized CRM and professional/business data sources |
| Optional producers / complementary | Included foundation; no mandatory upstream paid service; optional input producers: SM-SVC-02; SM-SVC-03; SM-SVC-04; SM-SVC-05; SM-SVC-08; authorized equivalent input accepted. |
| Service KPI | Account and stakeholder evidence coverage ≥95%; unauthorized contacts = 0 |
| Availability / bundle | Full / Research & Lead Intelligence / selective (1 SKU); eligible inputs and approvals required. |
| Interoperability / readiness | Optional authorized connector; external agent access disabled unless explicitly granted; Proposed; test and validate customer demand, provider access and economics |
| Open-source stack | Python; Django REST Framework; PostgreSQL; Celery/Beat; Valkey; pgvector if needed; specialist library/provider review pending |
| Blueprint epic / module | EP-06 (ASSUMPTION-826) / `crm.accounts` |
| Effect adapter | outbox to WF-27 cadence (AU-086) |
| Service guardrail | Contact eligibility is never inferred from evidence (CJ-GL-02); LinkedIn and call steps stay human tasks (DEC-392). |
| Functional requirement | FR-V12-D-129 (§11.4.5.29 register) |

**DTO `urn:sm:dto:SM-SVC-29-WF0n:v2` (one schema shared by the four workflows; v3 projection per workflow below):**

| Dir | Field | JSON Schema (App. B v2) | V12 validation | Blueprint storage target |
|---|---|---|---|---|
| in | `account_ref` | string format=uuid | UUID / scoped external reference; input, validate authorized scope | intel_organization / crm account (ENT-063) |
| in | `icp_ref` | string format=uuid | UUID / scoped external reference; input, validate authorized scope | ICP definition (CFG) |
| in | `role_evidence_refs` | array maxItems=500 | array (typed references or structured items); input, validate authoriz | intel_role_hypothesis.id[] (ENT-075) |
| in | `engagement_refs` | array maxItems=500 | array (typed references or structured items); input, validate authoriz | crm_activity.id[] (ENT-088) |
| out | `plan_ref` | string format=uuid | UUID / scoped external reference; output, validate schema and evidence | aut_artifact (domain plan) or lcy_onboarding (ENT-147) |
| out | `buying_group_ref` | string format=uuid | UUID / scoped external reference; output, validate schema and evidence | buying-committee map (AU-085) |
| out | `journey_ref` | string format=uuid | UUID / scoped external reference; output, validate schema and evidence | eng_sequence / cadence id (WF-27) |
| out | `progress_report_ref` | string format=uuid | UUID / scoped external reference; output, validate schema and evidence | aut_artifact report |

#### SM-SVC-29-WF01 Strategic account selection and account growth planning

| Field | Specification |
|---|---|
| V12 sources | BRD ch09 row; FSD ch12 lines 12366–12464; FSD ch13 registry row; App. B `urn:sm:dto:SM-SVC-29-WF01:v2`; workbook row "SM-SVC-29-WF01 — Strategic account selection and account growth planning" |
| Business outcome | Strategic account selection and account growth planning. Input → output: Account list, ICP, business objectives → Account plan |
| Detailed functionality (workbook) | Score accounts; select priorities; prepare plan |
| Blueprint mapping | WF-25 account-based engagement (Part 9.8b); agents AG-061, AG-040; automations AU-084, AU-055 |
| What V12 adds | Account selection and plan exist (AG-061); V12 binds deterministic account scoring as a named step. |
| Behaviour status | Partially covered → Matched |
| Trigger (V12) | Manual; scheduled monitoring; validated business event; authorized provider webhook when available; Account list, ICP, business objectives |
| Trigger kinds (registry, DEC-564) | `manual` (NT13-03); `scheduled` (NT13-02; default cadence per §11.4b, misfire `reschedule_once`); `event` (NT13-01; `sm.svc29.wf01.requested` or upstream domain event, §11.4b.6); `provider_callback` (signed, replay-checked) |
| Authority (V12) | R0 internal analysis/draft; L1 assisted; L3 approved read/draft; Approve source/data rights and applicable external actions; approve consequential communications, commitments and changes; routine steps only within preapproved policies. |
| Blueprint autonomy (DEC-566) | V12 L1 assisted / L3 approved read-draft → blueprint **L0–L1** (drafts and analysis only; no external effect). Approver: R03 |
| Human approval (workbook) | Approve source/data rights and applicable external actions; approve consequential communications, commitments and changes; routine steps only within preapproved policies. |
| Effect boundary | No external effect; internal artifacts only |
| Outputs produced (v3 projection) | `plan_ref` |
| Workflow KPI | account fit precision; plan completeness; baseline and threshold approved in pilot; source service KPI Account and stakeholder evidence coverage ≥95%; unauthorized contacts = 0 |
| Preconditions / failure handling | Common contract (D-F12-030 variant 2, D-F12-031): §11.4b.5 |
| Cost | V12 illustrative ₹0.55/invocation (excludes provider, retry, labour). Blueprint model estimate ₹1.26/run for 1 agent step(s) at Tier 1b (Part 7.3 prices, FX ₹90/USD, verify at time of implementation, as of 27 Nov 2026); Tier 2 not eligible (Confidential/personal data) |
| Usage limit (pilot, not approved) | Illustrative pilot: 100 Account review(s)/month; 1 concurrent run; approved caps, provider quotas and hard budget required. |
| Data modalities / version | Text; structured records; service 1.0-target, workflow 1.0-target |
| Acceptance (V12 → blueprint) | SM-SVC-29-WF01-TC-{POS,INPUT,SCOPE,ENT,DUP,QUALITY,BUDGET,RECOVERY} → TC-V12-D-101…108; SM-SVC-29-WF01-AT01 → TC-V12-D-111 |
| Release proposal | A1 |

| Step ID | Action (V12) | V12 executor → node type | Blueprint handler | Output contract | Failure → run state | Model tier | Status |
|---|---|---|---|---|---|---|---|
| SM-SVC-29-WF01-STEP-01 | Score accounts | Rules/analytics engine → NT13-07 `logic.compute` | AU-084 registered function | calculation {value,unit,assumptions,evidence_refs} | INVALID_METRIC → HELD | Tier 0 / none | Matched |
| SM-SVC-29-WF01-STEP-02 | select priorities | Domain service → NT13-05 `data.write_internal` | `crm.accounts` service (revision check) | domain_result {artifact_ref,status,evidence_refs} | INVALID_STATE → HELD | Tier 0 / none | Matched |
| SM-SVC-29-WF01-STEP-03 | prepare plan | Domain agent → NT13-08 `ai.task` + NT13-10 `approval.human` | AG-061 via gateway; routed to R03 | candidate {artifact_ref,confidence,reason_codes,review_state} | REVIEW_REQUIRED → AWAITING_APPROVAL | Tier 1b | Matched |

#### SM-SVC-29-WF02 Buying committee and organizational relationship mapping

| Field | Specification |
|---|---|
| V12 sources | BRD ch09 row; FSD ch12 lines 12465–12557; FSD ch13 registry row; App. B `urn:sm:dto:SM-SVC-29-WF02:v2`; workbook row "SM-SVC-29-WF02 — Buying committee and organizational relationship mapping" |
| Business outcome | Buying committee and organizational relationship mapping. Input → output: Verified role and organization evidence → Buying group map |
| Detailed functionality (workbook) | Map roles and relationships; flag uncertain links |
| Blueprint mapping | WF-25; agents AG-061; automations AU-085, AU-074 |
| What V12 adds | Buying-committee mapping exists (AU-085, AG-061); V12 adds uncertain-link flags. |
| Behaviour status | Partially covered → Matched |
| Trigger (V12) | Manual; scheduled monitoring; validated business event; authorized provider webhook when available; Verified role and organization evidence |
| Trigger kinds (registry, DEC-564) | `manual` (NT13-03); `scheduled` (NT13-02; default cadence per §11.4b, misfire `reschedule_once`); `event` (NT13-01; `sm.svc29.wf02.requested` or upstream domain event, §11.4b.6); `provider_callback` (signed, replay-checked) |
| Authority (V12) | R0 internal analysis/draft; L1 assisted; L3 approved read/draft; Approve source/data rights and applicable external actions; approve consequential communications, commitments and changes; routine steps only within preapproved policies. |
| Blueprint autonomy (DEC-566) | V12 L1 assisted / L3 approved read-draft → blueprint **L0–L1** (drafts and analysis only; no external effect). Approver: R03 |
| Human approval (workbook) | Approve source/data rights and applicable external actions; approve consequential communications, commitments and changes; routine steps only within preapproved policies. |
| Effect boundary | No external effect; internal artifacts only |
| Outputs produced (v3 projection) | `buying_group_ref` |
| Workflow KPI | role map accuracy; uncertain link flag rate; baseline and threshold approved in pilot; source service KPI Account and stakeholder evidence coverage ≥95%; unauthorized contacts = 0 |
| Preconditions / failure handling | Common contract (D-F12-030 variant 2, D-F12-031): §11.4b.5 |
| Cost | V12 illustrative ₹0.55/invocation (excludes provider, retry, labour). Blueprint model estimate ₹0.03/run for 1 agent step(s) at Tier 1b (Part 7.3 prices, FX ₹90/USD, verify at time of implementation, as of 27 Nov 2026); Tier 2 not eligible (Confidential/personal data) |
| Usage limit (pilot, not approved) | Illustrative pilot: 100 Account review(s)/month; 1 concurrent run; approved caps, provider quotas and hard budget required. |
| Data modalities / version | Text; structured records; service 1.0-target, workflow 1.0-target |
| Acceptance (V12 → blueprint) | SM-SVC-29-WF02-TC-{POS,INPUT,SCOPE,ENT,DUP,QUALITY,BUDGET,RECOVERY} → TC-V12-D-101…108; SM-SVC-29-WF02-AT01 → TC-V12-D-111 |
| Release proposal | A1 |

| Step ID | Action (V12) | V12 executor → node type | Blueprint handler | Output contract | Failure → run state | Model tier | Status |
|---|---|---|---|---|---|---|---|
| SM-SVC-29-WF02-STEP-01 | Map roles and relationships | Domain service → NT13-05 `data.write_internal` | `crm.accounts` service (revision check) | domain_result {artifact_ref,status,evidence_refs} | INVALID_STATE → HELD | Tier 0 / none | Matched |
| SM-SVC-29-WF02-STEP-02 | flag uncertain links | Domain agent → NT13-08 `ai.task` + NT13-10 `approval.human` | AG-061 via gateway; routed to R03 | candidate {artifact_ref,confidence,reason_codes,review_state} | REVIEW_REQUIRED → AWAITING_APPROVAL | Tier 1a | Matched |

#### SM-SVC-29-WF03 Account-specific multichannel campaign coordination

| Field | Specification |
|---|---|
| V12 sources | BRD ch09 row; FSD ch12 lines 12558–12650; FSD ch13 registry row; App. B `urn:sm:dto:SM-SVC-29-WF03:v2`; workbook row "SM-SVC-29-WF03 — Account-specific multichannel campaign coordination" |
| Business outcome | Account-specific multichannel campaign coordination. Input → output: Account plan, eligible contacts and channels → Account campaign plan |
| Detailed functionality (workbook) | Build coordinated journey; apply consent and conflict rules |
| Blueprint mapping | WF-25; WF-27 cadence (Part 9.8b); agents AG-063; automations AU-086, AU-009, AU-030 |
| What V12 adds | Coordinated plays exist; V12 adds consent and conflict rules as an explicit step. |
| Behaviour status | Partially covered → Matched |
| Trigger (V12) | Manual; scheduled monitoring; validated business event; authorized provider webhook when available; Account plan, eligible contacts and channels |
| Trigger kinds (registry, DEC-564) | `manual` (NT13-03); `scheduled` (NT13-02; default cadence per §11.4b, misfire `reschedule_once`); `event` (NT13-01; `sm.svc29.wf03.requested` or upstream domain event, §11.4b.6); `provider_callback` (signed, replay-checked) |
| Authority (V12) | R2 external communication/provider/access write; L2 mandatory approved effect; L3 only with separately approved bounded mandate where lawful; Approve source/data rights and applicable external actions; approve consequential communications, commitments and changes; routine steps only within preapproved policies. |
| Blueprint autonomy (DEC-566) | V12 L2 exact approved effect → blueprint **L1 approval of the exact payload hash, then L2 dispatch** of that item through the outbox (DEC-064 publishing pattern); V12 L3 mandate only for routine replies/reminders within caps. Approver: R03, R05L |
| Human approval (workbook) | Approve source/data rights and applicable external actions; approve consequential communications, commitments and changes; routine steps only within preapproved policies. |
| Effect boundary | No external effect; approval gate inserted before state change (DEC-570) |
| Outputs produced (v3 projection) | `plan_ref`, `journey_ref` |
| Workflow KPI | consent compliance; journey conflict rate; baseline and threshold approved in pilot; source service KPI Account and stakeholder evidence coverage ≥95%; unauthorized contacts = 0 |
| Preconditions / failure handling | Common contract (D-F12-030 variant 2, D-F12-031): §11.4b.5 |
| Cost | V12 illustrative ₹0.55/invocation (excludes provider, retry, labour). Blueprint model estimate ₹0.00/run for 0 agent step(s) at Tier 1b (Part 7.3 prices, FX ₹90/USD, verify at time of implementation, as of 27 Nov 2026); Tier 2 not eligible (Confidential/personal data) |
| Usage limit (pilot, not approved) | Illustrative pilot: 100 Account review(s)/month; 1 concurrent run; approved caps, provider quotas and hard budget required. |
| Data modalities / version | Text; structured records; service 1.0-target, workflow 1.0-target |
| Acceptance (V12 → blueprint) | SM-SVC-29-WF03-TC-{POS,INPUT,SCOPE,ENT,DUP,QUALITY,BUDGET,RECOVERY,APPROVAL,EFFECT} → TC-V12-D-101…110; SM-SVC-29-WF03-AT01 → TC-V12-D-111 |
| Release proposal | A1 |

| Step ID | Action (V12) | V12 executor → node type | Blueprint handler | Output contract | Failure → run state | Model tier | Status |
|---|---|---|---|---|---|---|---|
| SM-SVC-29-WF03-STEP-01 | Build coordinated journey | Domain service → NT13-05 `data.write_internal` | `crm.accounts` service (revision check) | domain_result {artifact_ref,status,evidence_refs} | INVALID_STATE → HELD | Tier 0 / none | Matched |
| SM-SVC-29-WF03-STEP-02 | apply consent and conflict rules | Policy/validation engine → NT13-09 `policy.check` | PDP (AU-009) rule set | validation {passed,reason_codes,policy_version} | POLICY_DENIED → BLOCKED | Tier 0 / none | Matched |

#### SM-SVC-29-WF04 Account engagement, opportunity progression and expansion intelligence

| Field | Specification |
|---|---|
| V12 sources | BRD ch09 row; FSD ch12 lines 12651–12749; FSD ch13 registry row; App. B `urn:sm:dto:SM-SVC-29-WF04:v2`; workbook row "SM-SVC-29-WF04 — Account engagement, opportunity progression and expansion intelligence" |
| Business outcome | Account engagement, opportunity progression and expansion intelligence. Input → output: Account events, pipeline records, outcomes → Account progression report |
| Detailed functionality (workbook) | Measure engagement; identify stalled opportunities; recommend next actions |
| Blueprint mapping | WF-25; WF-29; agents AG-043, AG-064; automations AU-085, AU-088 |
| What V12 adds | Engagement measures and stalled-deal flags exist; V12 adds account-level expansion intelligence. |
| Behaviour status | Partially covered → Matched |
| Trigger (V12) | Manual; scheduled monitoring; validated business event; authorized provider webhook when available; Account events, pipeline records, outcomes |
| Trigger kinds (registry, DEC-564) | `manual` (NT13-03); `scheduled` (NT13-02; default cadence per §11.4b, misfire `reschedule_once`); `event` (NT13-01; `sm.svc29.wf04.requested` or upstream domain event, §11.4b.6); `provider_callback` (signed, replay-checked) |
| Authority (V12) | R0 internal analysis/draft; L1 assisted; L3 approved read/draft; Approve source/data rights and applicable external actions; approve consequential communications, commitments and changes; routine steps only within preapproved policies. |
| Blueprint autonomy (DEC-566) | V12 L1 assisted / L3 approved read-draft → blueprint **L0–L1** (drafts and analysis only; no external effect). Approver: R03 |
| Human approval (workbook) | Approve source/data rights and applicable external actions; approve consequential communications, commitments and changes; routine steps only within preapproved policies. |
| Effect boundary | No external effect; internal artifacts only |
| Outputs produced (v3 projection) | `progress_report_ref` |
| Workflow KPI | stalled opportunity recall; engagement coverage; baseline and threshold approved in pilot; source service KPI Account and stakeholder evidence coverage ≥95%; unauthorized contacts = 0 |
| Preconditions / failure handling | Common contract (D-F12-030 variant 2, D-F12-031): §11.4b.5 |
| Cost | V12 illustrative ₹1.05/invocation (excludes provider, retry, labour). Blueprint model estimate ₹2.52/run for 2 agent step(s) at Tier 1b (Part 7.3 prices, FX ₹90/USD, verify at time of implementation, as of 27 Nov 2026); Tier 2 not eligible (Confidential/personal data) |
| Usage limit (pilot, not approved) | Illustrative pilot: 100 Account review(s)/month; 1 concurrent run; approved caps, provider quotas and hard budget required. |
| Data modalities / version | Text; structured records; service 1.0-target, workflow 1.0-target |
| Acceptance (V12 → blueprint) | SM-SVC-29-WF04-TC-{POS,INPUT,SCOPE,ENT,DUP,QUALITY,BUDGET,RECOVERY} → TC-V12-D-101…108; SM-SVC-29-WF04-AT01 → TC-V12-D-111 |
| Release proposal | A1 |

| Step ID | Action (V12) | V12 executor → node type | Blueprint handler | Output contract | Failure → run state | Model tier | Status |
|---|---|---|---|---|---|---|---|
| SM-SVC-29-WF04-STEP-01 | Measure engagement | Rules/analytics engine → NT13-07 `logic.compute` | AU-085 registered function | calculation {value,unit,assumptions,evidence_refs} | INVALID_METRIC → HELD | Tier 0 / none | Matched |
| SM-SVC-29-WF04-STEP-02 | identify stalled opportunities | Domain agent → NT13-08 `ai.task` + NT13-10 `approval.human` | AG-064 via gateway; routed to R03 | candidate {artifact_ref,confidence,reason_codes,review_state} | REVIEW_REQUIRED → AWAITING_APPROVAL | Tier 1b | Matched |
| SM-SVC-29-WF04-STEP-03 | recommend next actions | Domain agent → NT13-08 `ai.task` + NT13-10 `approval.human` | AG-043 via gateway; routed to R03 | candidate {artifact_ref,confidence,reason_codes,review_state} | REVIEW_REQUIRED → AWAITING_APPROVAL | Tier 1b | Matched |

### 11.4.5.19 SM-SVC-30 Conversion Rate Optimization & Intelligent Experimentation Automation

| Field | Specification |
|---|---|
| Family / objective | Experimentation; Improve conversion based on measured evidence |
| Channels / providers | Private Admin; approved client data and connectors; Authorized analytics, experiment platform and client site access |
| Optional producers / complementary | Included foundation; no mandatory upstream paid service; optional input producers: SM-SVC-13; SM-SVC-14; SM-SVC-15; SM-SVC-24; authorized equivalent input accepted. |
| Service KPI | Experiment allocation and budget checks 100%; report uncertainty |
| Availability / bundle | Full / Digital Marketing & Acquisition / selective (1 SKU); eligible inputs and approvals required. |
| Interoperability / readiness | Optional authorized connector; external agent access disabled unless explicitly granted; Provider, jurisdiction and specialist approval required before live operation |
| Open-source stack | Python; Django REST Framework; PostgreSQL; Celery/Beat; Valkey; pgvector if needed; specialist library/provider review pending |
| Blueprint epic / module | EP-12 (ASSUMPTION-826) / `marketing.experiments` |
| Effect adapter | ADP-WEB publication (AU-029) |
| Service guardrail | Experiments are pre-registered (WF-20); offer arms may only use approved price-book revisions (DEC-395). |
| Functional requirement | FR-V12-D-130 (§11.4.5.29 register) |

**DTO `urn:sm:dto:SM-SVC-30-WF0n:v2` (one schema shared by the four workflows; v3 projection per workflow below):**

| Dir | Field | JSON Schema (App. B v2) | V12 validation | Blueprint storage target |
|---|---|---|---|---|
| in | `hypothesis_ref` | string format=uuid | UUID / scoped external reference; input, validate authorized scope | experiment registry hypothesis |
| in | `variant_refs` | array maxItems=500 | array (typed references or structured items); input, validate authoriz | experiment arms (approved content hashes) |
| in | `allocation_policy_ref` | string format=uuid | UUID / scoped external reference; input, validate authorized scope | AU-098 allocation config |
| in | `event_refs` | array maxItems=500 | array (typed references or structured items); input, validate authoriz | ops_domain_event.id[] (ENT-170) |
| out | `experiment_ref` | string format=uuid | UUID / scoped external reference; output, validate schema and evidence | experiment registry id |
| out | `allocation_ref` | string format=uuid | UUID / scoped external reference; output, validate schema and evidence | com_payment_allocation.id (Part 3.3 allocation rows) |
| out | `lift` | string pattern=^-?\d{1,14}(\.\d{1,4})?$ | decimal; unit and bounds defined by metric policy; output, validate sc | numeric (V12 string: GAP-824) |
| out | `interval` | object | object {lower, upper, confidence_level}; output, validate schema and e | object {low, high, level} |
| out | `decision_state` | string maxLength=64 | string / configured enum; length and allowed values in versioned schem | enum {running, stop_harm, inconclusive, ship, no_ship} |

#### SM-SVC-30-WF01 Conversion funnel and abandonment analysis

| Field | Specification |
|---|---|
| V12 sources | BRD ch09 row; FSD ch12 lines 12751–12852; FSD ch13 registry row; App. B `urn:sm:dto:SM-SVC-30-WF01:v2`; workbook row "SM-SVC-30-WF01 — Conversion funnel and abandonment analysis" |
| Business outcome | Conversion funnel and abandonment analysis. Input → output: Authorized event funnel, consent settings → Funnel report |
| Detailed functionality (workbook) | Validate event definitions; calculate drop-offs; prioritize hypotheses |
| Blueprint mapping | RP-02 funnel, RP-09 website analytics (Part 2.4); AU-102 semantic metrics (Part 9.9); agents AG-052; automations AU-102, AU-009 |
| What V12 adds | Funnel metrics exist; V12 adds abandonment drop-off calculation and hypothesis prioritisation. |
| Behaviour status | Partially covered → Matched |
| Trigger (V12) | Manual; scheduled monitoring; validated business event; authorized provider webhook when available; Authorized event funnel, consent settings |
| Trigger kinds (registry, DEC-564) | `manual` (NT13-03); `scheduled` (NT13-02; default cadence per §11.4b, misfire `reschedule_once`); `event` (NT13-01; `sm.svc30.wf01.requested` or upstream domain event, §11.4b.6); `provider_callback` (signed, replay-checked) |
| Authority (V12) | R0 internal analysis/draft; L1 assisted; L3 approved read/draft; Approve source/data rights and applicable external actions; approve experimental bounds, customer fairness, budget, pricing and publication before any live change. |
| Blueprint autonomy (DEC-566) | V12 L1 assisted / L3 approved read-draft → blueprint **L0–L1** (drafts and analysis only; no external effect). Approver: R05L |
| Human approval (workbook) | Approve source/data rights and applicable external actions; approve experimental bounds, customer fairness, budget, pricing and publication before any live change. |
| Effect boundary | No external effect; internal artifacts only |
| Outputs produced (v3 projection) | `decision_state` |
| Workflow KPI | event completeness; funnel arithmetic accuracy; baseline and threshold approved in pilot; source service KPI Experiment allocation and budget checks 100%; report uncertainty |
| Preconditions / failure handling | Common contract (D-F12-030 variant 2, D-F12-031): §11.4b.5 |
| Cost | V12 illustrative ₹1.05/invocation (excludes provider, retry, labour). Blueprint model estimate ₹0.00/run for 0 agent step(s) at Tier 1a (Part 7.3 prices, FX ₹90/USD, verify at time of implementation, as of 27 Nov 2026); Tier 2 not eligible (Confidential/personal data) |
| Usage limit (pilot, not approved) | Illustrative pilot: 30 Experiment(s)/month; 1 concurrent run; approved caps, provider quotas and hard budget required. |
| Data modalities / version | Text; structured records; service 1.0-target, workflow 1.0-target |
| Acceptance (V12 → blueprint) | SM-SVC-30-WF01-TC-{POS,INPUT,SCOPE,ENT,DUP,QUALITY,BUDGET,RECOVERY} → TC-V12-D-101…108; SM-SVC-30-WF01-AT01 → TC-V12-D-111 |
| Release proposal | A2 |

| Step ID | Action (V12) | V12 executor → node type | Blueprint handler | Output contract | Failure → run state | Model tier | Status |
|---|---|---|---|---|---|---|---|
| SM-SVC-30-WF01-STEP-01 | Validate event definitions | Policy/validation engine → NT13-09 `policy.check` | PDP (AU-009) rule set | validation {passed,reason_codes,policy_version} | POLICY_DENIED → BLOCKED | Tier 0 / none | Matched |
| SM-SVC-30-WF01-STEP-02 | calculate drop-offs | Rules/analytics engine → NT13-07 `logic.compute` | AU-102 registered function | calculation {value,unit,assumptions,evidence_refs} | INVALID_METRIC → HELD | Tier 0 / none | Matched |
| SM-SVC-30-WF01-STEP-03 | prioritize hypotheses | Domain service → NT13-05 `data.write_internal` | `marketing.experiments` service (revision check) | domain_result {artifact_ref,status,evidence_refs} | INVALID_STATE → HELD | Tier 0 / none | Matched |

#### SM-SVC-30-WF02 Controlled landing page and offer experimentation

| Field | Specification |
|---|---|
| V12 sources | BRD ch09 row; FSD ch12 lines 12853–12954; FSD ch13 registry row; App. B `urn:sm:dto:SM-SVC-30-WF02:v2`; workbook row "SM-SVC-30-WF02 — Controlled landing page and offer experimentation" |
| Business outcome | Controlled landing page and offer experimentation. Input → output: Approved variants, sample plan, budget → Experiment execution record |
| Detailed functionality (workbook) | Randomize eligible traffic; enforce limits; monitor safety |
| Blueprint mapping | WF-20 experiment lifecycle (Part 9.7b); agents AG-052; automations AU-098, AU-065, AU-029 |
| What V12 adds | Experiment allocation exists (AU-098); V12 classifies offer experiments R3; the L3 mandate path is not adopted. |
| Behaviour status | Partially covered → Matched (CONFLICT-814) |
| Trigger (V12) | Manual; scheduled monitoring; validated business event; authorized provider webhook when available; Approved variants, sample plan, budget |
| Trigger kinds (registry, DEC-564) | `manual` (NT13-03); `scheduled` (NT13-02; default cadence per §11.4b, misfire `reschedule_once`); `event` (NT13-01; `sm.svc30.wf02.requested` or upstream domain event, §11.4b.6); `provider_callback` (signed, replay-checked) |
| Authority (V12) | R3 financial/legal/commitment; L2 mandatory approved effect; L3 only with separately approved bounded mandate where lawful; Approve source/data rights and applicable external actions; approve experimental bounds, customer fairness, budget, pricing and publication before any live change. |
| Blueprint autonomy (DEC-566) | V12 L2 default → blueprint **L1 maximum** (human approval bound to the exact hash; money movement not supported, DEC-064). V12 "L3 bounded mandate" **not adopted** (CONFLICT-814, Pending Founder decision). Approver: R05L, R02, R08 |
| Human approval (workbook) | Approve source/data rights and applicable external actions; approve experimental bounds, customer fairness, budget, pricing and publication before any live change. |
| Effect boundary | No external effect; approval gate inserted before state change (DEC-570) |
| Outputs produced (v3 projection) | `experiment_ref` |
| Workflow KPI | assignment consistency; guardrail violations; baseline and threshold approved in pilot; source service KPI Experiment allocation and budget checks 100%; report uncertainty |
| Preconditions / failure handling | Common contract (D-F12-030 variant 2, D-F12-031): §11.4b.5 |
| Cost | V12 illustrative ₹0.55/invocation (excludes provider, retry, labour). Blueprint model estimate ₹0.00/run for 0 agent step(s) at Tier 1a (Part 7.3 prices, FX ₹90/USD, verify at time of implementation, as of 27 Nov 2026); Tier 2 not eligible (Confidential/personal data) |
| Usage limit (pilot, not approved) | Illustrative pilot: 30 Experiment(s)/month; 1 concurrent run; approved caps, provider quotas and hard budget required. |
| Data modalities / version | Text; structured records; service 1.0-target, workflow 1.0-target |
| Acceptance (V12 → blueprint) | SM-SVC-30-WF02-TC-{POS,INPUT,SCOPE,ENT,DUP,QUALITY,BUDGET,RECOVERY,APPROVAL,EFFECT} → TC-V12-D-101…110; SM-SVC-30-WF02-AT01 → TC-V12-D-111 |
| Release proposal | A2 |

| Step ID | Action (V12) | V12 executor → node type | Blueprint handler | Output contract | Failure → run state | Model tier | Status |
|---|---|---|---|---|---|---|---|
| SM-SVC-30-WF02-STEP-01 | Randomize eligible traffic | Rules/analytics engine → NT13-07 `logic.compute` | AU-098 registered function | calculation {value,unit,assumptions,evidence_refs} | INVALID_METRIC → HELD | Tier 0 / none | Matched |
| SM-SVC-30-WF02-STEP-02 | enforce limits | Policy/validation engine → NT13-09 `policy.check` | PDP (AU-009) rule set | validation {passed,reason_codes,policy_version} | POLICY_DENIED → BLOCKED | Tier 0 / none | Matched |
| SM-SVC-30-WF02-STEP-03 | monitor safety | Domain service → NT13-05 `data.write_internal` | `marketing.experiments` service (revision check) | domain_result {artifact_ref,status,evidence_refs} | INVALID_STATE → HELD | Tier 0 / none | Matched |

#### SM-SVC-30-WF03 Privacy-respecting journey personalization

| Field | Specification |
|---|---|
| V12 sources | BRD ch09 row; FSD ch12 lines 12955–13056; FSD ch13 registry row; App. B `urn:sm:dto:SM-SVC-30-WF03:v2`; workbook row "SM-SVC-30-WF03 — Privacy-respecting journey personalization" |
| Business outcome | Privacy-respecting journey personalization. Input → output: Approved segments, consent and journey context → Personalization decision |
| Detailed functionality (workbook) | Apply permitted rules; avoid sensitive inference; evaluate outcomes |
| Blueprint mapping | WF-19 personalization (Part 9.7b); agents AG-049; automations AU-009, AU-067 |
| What V12 adds | Personalization exists over deterministic segments (CI-063); V12 adds an explicit sensitive-inference guard. |
| Behaviour status | Partially covered → Matched |
| Trigger (V12) | Manual; scheduled monitoring; validated business event; authorized provider webhook when available; Approved segments, consent and journey context |
| Trigger kinds (registry, DEC-564) | `manual` (NT13-03); `scheduled` (NT13-02; default cadence per §11.4b, misfire `reschedule_once`); `event` (NT13-01; `sm.svc30.wf03.requested` or upstream domain event, §11.4b.6); `provider_callback` (signed, replay-checked) |
| Authority (V12) | R2 external communication/provider/access write; L2 mandatory approved effect; L3 only with separately approved bounded mandate where lawful; Approve source/data rights and applicable external actions; approve experimental bounds, customer fairness, budget, pricing and publication before any live change. |
| Blueprint autonomy (DEC-566) | V12 L2 exact approved effect → blueprint **L1 approval of the exact payload hash, then L2 dispatch** of that item through the outbox (DEC-064 publishing pattern); V12 L3 mandate only for routine replies/reminders within caps. Approver: R05L, R10 |
| Human approval (workbook) | Approve source/data rights and applicable external actions; approve experimental bounds, customer fairness, budget, pricing and publication before any live change. |
| Effect boundary | No external effect; approval gate inserted before state change (DEC-570) |
| Outputs produced (v3 projection) | `decision_state` |
| Workflow KPI | eligible personalization rate; prohibited inference count; baseline and threshold approved in pilot; source service KPI Experiment allocation and budget checks 100%; report uncertainty |
| Preconditions / failure handling | Common contract (D-F12-030 variant 2, D-F12-031): §11.4b.5 |
| Cost | V12 illustrative ₹0.55/invocation (excludes provider, retry, labour). Blueprint model estimate ₹0.00/run for 0 agent step(s) at Tier 1a (Part 7.3 prices, FX ₹90/USD, verify at time of implementation, as of 27 Nov 2026); Tier 2 not eligible (Confidential/personal data) |
| Usage limit (pilot, not approved) | Illustrative pilot: 30 Experiment(s)/month; 1 concurrent run; approved caps, provider quotas and hard budget required. |
| Data modalities / version | Text; structured records; service 1.0-target, workflow 1.0-target |
| Acceptance (V12 → blueprint) | SM-SVC-30-WF03-TC-{POS,INPUT,SCOPE,ENT,DUP,QUALITY,BUDGET,RECOVERY,APPROVAL,EFFECT} → TC-V12-D-101…110; SM-SVC-30-WF03-AT01 → TC-V12-D-111 |
| Release proposal | A2 |

| Step ID | Action (V12) | V12 executor → node type | Blueprint handler | Output contract | Failure → run state | Model tier | Status |
|---|---|---|---|---|---|---|---|
| SM-SVC-30-WF03-STEP-01 | Apply permitted rules | Policy/validation engine → NT13-09 `policy.check` | PDP (AU-009) rule set + AU-067 | validation {passed,reason_codes,policy_version} | POLICY_DENIED → BLOCKED | Tier 0 / none | Matched |
| SM-SVC-30-WF03-STEP-02 | avoid sensitive inference | Domain service → NT13-05 `data.write_internal` | `marketing.experiments` service (revision check) | domain_result {artifact_ref,status,evidence_refs} | INVALID_STATE → HELD | Tier 0 / none | Matched |
| SM-SVC-30-WF03-STEP-03 | evaluate outcomes | Domain service → NT13-05 `data.write_internal` | `marketing.experiments` service (revision check) | domain_result {artifact_ref,status,evidence_refs} | INVALID_STATE → HELD | Tier 0 / none | Matched |

#### SM-SVC-30-WF04 Experiment effectiveness and incremental conversion evaluation

| Field | Specification |
|---|---|
| V12 sources | BRD ch09 row; FSD ch12 lines 13057–13152; FSD ch13 registry row; App. B `urn:sm:dto:SM-SVC-30-WF04:v2`; workbook row "SM-SVC-30-WF04 — Experiment effectiveness and incremental conversion evaluation" |
| Business outcome | Experiment effectiveness and incremental conversion evaluation. Input → output: Experiment events, allocation and baseline → Experiment report |
| Detailed functionality (workbook) | Estimate lift and uncertainty; flag inconclusive results |
| Blueprint mapping | WF-20 readout; agents AG-052; automations AU-065 |
| What V12 adds | Statistics engine exists (AU-065); V12 adds incremental conversion with interval and inconclusive flag. |
| Behaviour status | Partially covered → Matched |
| Trigger (V12) | Manual; scheduled monitoring; validated business event; authorized provider webhook when available; Experiment events, allocation and baseline |
| Trigger kinds (registry, DEC-564) | `manual` (NT13-03); `scheduled` (NT13-02; default cadence per §11.4b, misfire `reschedule_once`); `event` (NT13-01; `sm.svc30.wf04.requested` or upstream domain event, §11.4b.6); `provider_callback` (signed, replay-checked) |
| Authority (V12) | R0 internal analysis/draft; L1 assisted; L3 approved read/draft; Approve source/data rights and applicable external actions; approve experimental bounds, customer fairness, budget, pricing and publication before any live change. |
| Blueprint autonomy (DEC-566) | V12 L1 assisted / L3 approved read-draft → blueprint **L0–L1** (drafts and analysis only; no external effect). Approver: R05L |
| Human approval (workbook) | Approve source/data rights and applicable external actions; approve experimental bounds, customer fairness, budget, pricing and publication before any live change. |
| Effect boundary | No external effect; internal artifacts only |
| Outputs produced (v3 projection) | `experiment_ref`, `lift` |
| Workflow KPI | interval coverage; inconclusive result handling; baseline and threshold approved in pilot; source service KPI Experiment allocation and budget checks 100%; report uncertainty |
| Preconditions / failure handling | Common contract (D-F12-030 variant 2, D-F12-031): §11.4b.5 |
| Cost | V12 illustrative ₹0.55/invocation (excludes provider, retry, labour). Blueprint model estimate ₹0.03/run for 1 agent step(s) at Tier 1a (Part 7.3 prices, FX ₹90/USD, verify at time of implementation, as of 27 Nov 2026); Tier 2 not eligible (Confidential/personal data) |
| Usage limit (pilot, not approved) | Illustrative pilot: 30 Experiment(s)/month; 1 concurrent run; approved caps, provider quotas and hard budget required. |
| Data modalities / version | Text; structured records; service 1.0-target, workflow 1.0-target |
| Acceptance (V12 → blueprint) | SM-SVC-30-WF04-TC-{POS,INPUT,SCOPE,ENT,DUP,QUALITY,BUDGET,RECOVERY} → TC-V12-D-101…108; SM-SVC-30-WF04-AT01 → TC-V12-D-111 |
| Release proposal | A2 |

| Step ID | Action (V12) | V12 executor → node type | Blueprint handler | Output contract | Failure → run state | Model tier | Status |
|---|---|---|---|---|---|---|---|
| SM-SVC-30-WF04-STEP-01 | Estimate lift and uncertainty | Rules/analytics engine → NT13-07 `logic.compute` | AU-065 registered function | calculation {value,unit,assumptions,evidence_refs} | INVALID_METRIC → HELD | Tier 0 / none | Matched |
| SM-SVC-30-WF04-STEP-02 | flag inconclusive results | Domain agent → NT13-08 `ai.task` + NT13-10 `approval.human` | AG-052 via gateway; routed to R05L | candidate {artifact_ref,confidence,reason_codes,review_state} | REVIEW_REQUIRED → AWAITING_APPROVAL | Tier 1a | Matched |
