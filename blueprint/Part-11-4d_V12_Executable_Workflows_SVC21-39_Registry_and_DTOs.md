### 11.4.5.20 SM-SVC-31 Marketplace & E-commerce Channel Operations Automation

| Field | Specification |
|---|---|
| Family / objective | Marketplace operations; Manage conventional marketplace operations |
| Channels / providers | Private Admin; approved client data and connectors; Authorized marketplace API and inventory/order system |
| Optional producers / complementary | Included foundation; no mandatory upstream paid service; optional input producers: SM-SVC-15; SM-SVC-20; SM-SVC-21; SM-SVC-24; authorized equivalent input accepted. |
| Service KPI | Verified order-event deduplication 100%; reconciliation accuracy target ≥99% |
| Availability / bundle | Full / Commerce & Procurement / selective (1 SKU); eligible inputs and approvals required. |
| Interoperability / readiness | Optional authorized connector; external agent access disabled unless explicitly granted; Provider, jurisdiction and specialist approval required before live operation |
| Open-source stack | Python; Django REST Framework; PostgreSQL; Celery/Beat; Valkey; pgvector if needed; specialist library/provider review pending |
| Blueprint epic / module | EP-14 (ASSUMPTION-826) / `commerce.marketplace` |
| Effect adapter | ADP-MKT (marketplace seller API, not procured) |
| Service guardrail | Listing prices come only from approved price-book revisions; marketplace order events are idempotent like AU-038 fulfilment events. |
| Functional requirement | FR-V12-D-131 (§11.4.5.29 register) |

**DTO `urn:sm:dto:SM-SVC-31-WF0n:v2` (one schema shared by the four workflows; v3 projection per workflow below):**

| Dir | Field | JSON Schema (App. B v2) | V12 validation | Blueprint storage target |
|---|---|---|---|---|
| in | `marketplace_ref` | string format=uuid | UUID / scoped external reference; input, validate authorized scope | int_integration (marketplace connection) |
| in | `sku_ref` | string format=uuid | UUID / scoped external reference; input, validate authorized scope | cat_offering SKU |
| in | `inventory_ref` | string format=uuid | UUID / scoped external reference; input, validate authorized scope | stock ledger (WF-10) |
| in | `event_refs` | array maxItems=500 | array (typed references or structured items); input, validate authoriz | ops_domain_event.id[] (ENT-170) |
| out | `listing_ref` | string format=uuid | UUID / scoped external reference; output, validate schema and evidence | mkt_marketplace_listing (proposed) |
| out | `inventory_version` | integer minimum=1 | positive integer; output, validate schema and evidence | integer ≥ 1 |
| out | `order_event_ref` | string format=uuid | UUID / scoped external reference; output, validate schema and evidence | int_provider_event.id |
| out | `net_minor` | integer minimum=0 | int64, nonnegative except signed ledger deltas; output, validate schem | numeric(18,4) ↔ int64 minor |

#### SM-SVC-31-WF01 Authorized marketplace product listing synchronization

| Field | Specification |
|---|---|
| V12 sources | BRD ch09 row; FSD ch12 lines 13154–13252; FSD ch13 registry row; App. B `urn:sm:dto:SM-SVC-31-WF01:v2`; workbook row "SM-SVC-31-WF01 — Authorized marketplace product listing synchronization" |
| Business outcome | Authorized marketplace product listing synchronization. Input → output: Approved SKU catalog, marketplace permissions → Listing state |
| Detailed functionality (workbook) | Map fields; validate content; publish eligible updates |
| Blueprint mapping | WF-01 offering catalogue; agents AG-018, AG-012; automations AU-029, AU-009 |
| What V12 adds | New: map approved offerings to marketplace listing fields and publish through a marketplace adapter. |
| Behaviour status | Not covered → Matched |
| Trigger (V12) | Manual; scheduled monitoring; validated business event; authorized provider webhook when available; Approved SKU catalog, marketplace permissions |
| Trigger kinds (registry, DEC-564) | `manual` (NT13-03); `scheduled` (NT13-02; default cadence per §11.4b, misfire `reschedule_once`); `event` (NT13-01; `sm.svc31.wf01.requested` or upstream domain event, §11.4b.6); `provider_callback` (signed, replay-checked) |
| Authority (V12) | R2 external communication/provider/access write; L2 mandatory approved effect; L3 only with separately approved bounded mandate where lawful; Approve source/data rights and applicable external actions; approve purchase/order commitments, pricing and any external listing or supplier change. |
| Blueprint autonomy (DEC-566) | V12 L2 exact approved effect → blueprint **L1 approval of the exact payload hash, then L2 dispatch** of that item through the outbox (DEC-064 publishing pattern); V12 L3 mandate only for routine replies/reminders within caps. Approver: R02, R10 |
| Human approval (workbook) | Approve source/data rights and applicable external actions; approve purchase/order commitments, pricing and any external listing or supplier change. |
| Effect boundary | Effect steps: STEP-03 via ADP-MKT (marketplace seller API, not procured) |
| Outputs produced (v3 projection) | `listing_ref` |
| Workflow KPI | listing field accuracy; duplicate publish count; baseline and threshold approved in pilot; source service KPI Verified order-event deduplication 100%; reconciliation accuracy target ≥99% |
| Preconditions / failure handling | Common contract (D-F12-030 variant 2, D-F12-031): §11.4b.5 |
| Cost | V12 illustrative ₹0.55/invocation (excludes provider, retry, labour). Blueprint model estimate ₹0.00/run for 0 agent step(s) at Tier 1a (Part 7.3 prices, FX ₹90/USD, verify at time of implementation, as of 27 Nov 2026); Tier 2 not eligible (Confidential/personal data) |
| Usage limit (pilot, not approved) | Illustrative pilot: 500 Marketplace order/event(s)/month; 1 concurrent run; approved caps, provider quotas and hard budget required. |
| Data modalities / version | Text; structured records; service 1.0-target, workflow 1.0-target |
| Acceptance (V12 → blueprint) | SM-SVC-31-WF01-TC-{POS,INPUT,SCOPE,ENT,DUP,QUALITY,BUDGET,RECOVERY,APPROVAL,EFFECT} → TC-V12-D-101…110; SM-SVC-31-WF01-AT01 → TC-V12-D-111 |
| Release proposal | A2 |

| Step ID | Action (V12) | V12 executor → node type | Blueprint handler | Output contract | Failure → run state | Model tier | Status |
|---|---|---|---|---|---|---|---|
| SM-SVC-31-WF01-STEP-01 | Map fields | Domain service → NT13-05 `data.write_internal` | `commerce.marketplace` service (revision check) | domain_result {artifact_ref,status,evidence_refs} | INVALID_STATE → HELD | Tier 0 / none | Matched |
| SM-SVC-31-WF01-STEP-02 | validate content | Policy/validation engine → NT13-09 `policy.check` | PDP (AU-009) rule set | validation {passed,reason_codes,policy_version} | POLICY_DENIED → BLOCKED | Tier 0 / none | Matched |
| SM-SVC-31-WF01-STEP-03 | publish eligible updates | Effect adapter → NT13-13 `action.external` | Outbox → AU-009 dispatch recheck → ADP-MKT (marketplace seller API, not procured) | effect_receipt {provider_ref,status,observed_at} | EFFECT_UNKNOWN → RECONCILING | none | Matched |

#### SM-SVC-31-WF02 Marketplace pricing, availability and inventory synchronization

| Field | Specification |
|---|---|
| V12 sources | BRD ch09 row; FSD ch12 lines 13253–13351; FSD ch13 registry row; App. B `urn:sm:dto:SM-SVC-31-WF02:v2`; workbook row "SM-SVC-31-WF02 — Marketplace pricing, availability and inventory synchronization" |
| Business outcome | Marketplace pricing, availability and inventory synchronization. Input → output: Approved prices, stock and channel rules → Availability update |
| Detailed functionality (workbook) | Reconcile inventory; validate prices; update authorized listings |
| Blueprint mapping | WF-10 stock reservation; agents none (deterministic only); automations AU-038, AU-089, AU-009 |
| What V12 adds | New: inventory and price sync; prices only from approved price-book revisions; R3 L3 mandate path not adopted. |
| Behaviour status | Not covered → Matched (CONFLICT-814) |
| Trigger (V12) | Manual; scheduled monitoring; validated business event; authorized provider webhook when available; Approved prices, stock and channel rules |
| Trigger kinds (registry, DEC-564) | `manual` (NT13-03); `scheduled` (NT13-02; default cadence per §11.4b, misfire `reschedule_once`); `event` (NT13-01; `sm.svc31.wf02.requested` or upstream domain event, §11.4b.6); `provider_callback` (signed, replay-checked) |
| Authority (V12) | R3 financial/legal/commitment; L2 mandatory approved effect; L3 only with separately approved bounded mandate where lawful; Approve source/data rights and applicable external actions; approve purchase/order commitments, pricing and any external listing or supplier change. |
| Blueprint autonomy (DEC-566) | V12 L2 default → blueprint **L1 maximum** (human approval bound to the exact hash; money movement not supported, DEC-064). V12 "L3 bounded mandate" **not adopted** (CONFLICT-814, Pending Founder decision). Approver: R02, R08 |
| Human approval (workbook) | Approve source/data rights and applicable external actions; approve purchase/order commitments, pricing and any external listing or supplier change. |
| Effect boundary | Effect steps: STEP-03 via ADP-MKT (marketplace seller API, not procured) |
| Outputs produced (v3 projection) | `listing_ref`, `inventory_version` |
| Workflow KPI | inventory consistency; stale price rejection; baseline and threshold approved in pilot; source service KPI Verified order-event deduplication 100%; reconciliation accuracy target ≥99% |
| Preconditions / failure handling | Common contract (D-F12-030 variant 2, D-F12-031): §11.4b.5 |
| Cost | V12 illustrative ₹0.55/invocation (excludes provider, retry, labour). Blueprint model estimate ₹0.00/run for 0 agent step(s) at Tier 1a (Part 7.3 prices, FX ₹90/USD, verify at time of implementation, as of 27 Nov 2026); Tier 2 not eligible (Confidential/personal data) |
| Usage limit (pilot, not approved) | Illustrative pilot: 500 Marketplace order/event(s)/month; 1 concurrent run; approved caps, provider quotas and hard budget required. |
| Data modalities / version | Text; structured records; service 1.0-target, workflow 1.0-target |
| Acceptance (V12 → blueprint) | SM-SVC-31-WF02-TC-{POS,INPUT,SCOPE,ENT,DUP,QUALITY,BUDGET,RECOVERY,APPROVAL,EFFECT} → TC-V12-D-101…110; SM-SVC-31-WF02-AT01 → TC-V12-D-111 |
| Release proposal | A2 |

| Step ID | Action (V12) | V12 executor → node type | Blueprint handler | Output contract | Failure → run state | Model tier | Status |
|---|---|---|---|---|---|---|---|
| SM-SVC-31-WF02-STEP-01 | Reconcile inventory | Identity/reconciliation engine → NT13-07 `logic.compute` | AU-038 registered function | match_result {matched_refs,unmatched_refs,conflict_refs} | CONFLICT → HELD | Tier 0 / none | Matched |
| SM-SVC-31-WF02-STEP-02 | validate prices | Policy/validation engine → NT13-09 `policy.check` | PDP (AU-009) rule set + AU-089 | validation {passed,reason_codes,policy_version} | POLICY_DENIED → BLOCKED | Tier 0 / none | Matched |
| SM-SVC-31-WF02-STEP-03 | update authorized listings | Effect adapter → NT13-13 `action.external` | Outbox → AU-009 dispatch recheck → ADP-MKT (marketplace seller API, not procured) | effect_receipt {provider_ref,status,observed_at} | EFFECT_UNKNOWN → RECONCILING | none | Matched |

#### SM-SVC-31-WF03 Order, cancellation and return-event coordination

| Field | Specification |
|---|---|
| V12 sources | BRD ch09 row; FSD ch12 lines 13352–13450; FSD ch13 registry row; App. B `urn:sm:dto:SM-SVC-31-WF03:v2`; workbook row "SM-SVC-31-WF03 — Order, cancellation and return-event coordination" |
| Business outcome | Order, cancellation and return-event coordination. Input → output: Verified marketplace order events and policies → Order event ledger |
| Detailed functionality (workbook) | Deduplicate events; update order state; route returns and exceptions |
| Blueprint mapping | WF-10 order and fulfilment (§2.16); agents AG-023; automations AU-038, AU-026 |
| What V12 adds | Idempotent order and fulfilment events exist (AU-038); V12 adds marketplace cancellation and return events. |
| Behaviour status | Partially covered → Matched |
| Trigger (V12) | Manual; scheduled monitoring; validated business event; authorized provider webhook when available; Verified marketplace order events and policies |
| Trigger kinds (registry, DEC-564) | `manual` (NT13-03); `scheduled` (NT13-02; default cadence per §11.4b, misfire `reschedule_once`); `event` (NT13-01; `sm.svc31.wf03.requested` or upstream domain event, §11.4b.6); `provider_callback` (signed, replay-checked) |
| Authority (V12) | R3 financial/legal/commitment; L2 mandatory approved effect; L3 only with separately approved bounded mandate where lawful; Approve source/data rights and applicable external actions; approve purchase/order commitments, pricing and any external listing or supplier change. |
| Blueprint autonomy (DEC-566) | V12 L2 default → blueprint **L1 maximum** (human approval bound to the exact hash; money movement not supported, DEC-064). V12 "L3 bounded mandate" **not adopted** (CONFLICT-814, Pending Founder decision). Approver: R07 |
| Human approval (workbook) | Approve source/data rights and applicable external actions; approve purchase/order commitments, pricing and any external listing or supplier change. |
| Effect boundary | No external effect; approval gate inserted before state change (DEC-570) |
| Outputs produced (v3 projection) | `order_event_ref` |
| Workflow KPI | order event dedup; invalid return transition rejection; baseline and threshold approved in pilot; source service KPI Verified order-event deduplication 100%; reconciliation accuracy target ≥99% |
| Preconditions / failure handling | Common contract (D-F12-030 variant 2, D-F12-031): §11.4b.5 |
| Cost | V12 illustrative ₹0.55/invocation (excludes provider, retry, labour). Blueprint model estimate ₹0.03/run for 1 agent step(s) at Tier 1a (Part 7.3 prices, FX ₹90/USD, verify at time of implementation, as of 27 Nov 2026); Tier 2 not eligible (Confidential/personal data) |
| Usage limit (pilot, not approved) | Illustrative pilot: 500 Marketplace order/event(s)/month; 1 concurrent run; approved caps, provider quotas and hard budget required. |
| Data modalities / version | Text; structured records; service 1.0-target, workflow 1.0-target |
| Acceptance (V12 → blueprint) | SM-SVC-31-WF03-TC-{POS,INPUT,SCOPE,ENT,DUP,QUALITY,BUDGET,RECOVERY,APPROVAL,EFFECT} → TC-V12-D-101…110; SM-SVC-31-WF03-AT01 → TC-V12-D-111 |
| Release proposal | A2 |

| Step ID | Action (V12) | V12 executor → node type | Blueprint handler | Output contract | Failure → run state | Model tier | Status |
|---|---|---|---|---|---|---|---|
| SM-SVC-31-WF03-STEP-01 | Deduplicate events | Identity/reconciliation engine → NT13-07 `logic.compute` | AU-038 registered function | match_result {matched_refs,unmatched_refs,conflict_refs} | CONFLICT → HELD | Tier 0 / none | Matched |
| SM-SVC-31-WF03-STEP-02 | update order state | Domain service → NT13-05 `data.write_internal` | `commerce.marketplace` service (revision check) | domain_result {artifact_ref,status,evidence_refs} | INVALID_STATE → HELD | Tier 0 / none | Matched |
| SM-SVC-31-WF03-STEP-03 | route returns and exceptions | Domain agent → NT13-08 `ai.task` + NT13-10 `approval.human` | AG-023 via gateway; routed to R07 | candidate {artifact_ref,confidence,reason_codes,review_state} | REVIEW_REQUIRED → AWAITING_APPROVAL | Tier 1a | Matched |

#### SM-SVC-31-WF04 Marketplace performance and reconciliation reporting

| Field | Specification |
|---|---|
| V12 sources | BRD ch09 row; FSD ch12 lines 13451–13543; FSD ch13 registry row; App. B `urn:sm:dto:SM-SVC-31-WF04:v2`; workbook row "SM-SVC-31-WF04 — Marketplace performance and reconciliation reporting" |
| Business outcome | Marketplace performance and reconciliation reporting. Input → output: Marketplace reports, fees, verified receipts → Marketplace reconciliation report |
| Detailed functionality (workbook) | Match sales and fees; report anomalies and net performance |
| Blueprint mapping | AU-040 revenue reconciliation; RP-14, RP-16; agents none (deterministic only); automations AU-040, AU-037 |
| What V12 adds | New: match marketplace sales, fees and settlements to orders and report net performance. |
| Behaviour status | Not covered → Matched |
| Trigger (V12) | Manual; scheduled monitoring; validated business event; authorized provider webhook when available; Marketplace reports, fees, verified receipts |
| Trigger kinds (registry, DEC-564) | `manual` (NT13-03); `scheduled` (NT13-02; default cadence per §11.4b, misfire `reschedule_once`); `event` (NT13-01; `sm.svc31.wf04.requested` or upstream domain event, §11.4b.6); `provider_callback` (signed, replay-checked) |
| Authority (V12) | R0 internal analysis/draft; L1 assisted; L3 approved read/draft; Approve source/data rights and applicable external actions; approve purchase/order commitments, pricing and any external listing or supplier change. |
| Blueprint autonomy (DEC-566) | V12 L1 assisted / L3 approved read-draft → blueprint **L0–L1** (drafts and analysis only; no external effect). Approver: R08 |
| Human approval (workbook) | Approve source/data rights and applicable external actions; approve purchase/order commitments, pricing and any external listing or supplier change. |
| Effect boundary | No external effect; internal artifacts only |
| Outputs produced (v3 projection) | `net_minor` |
| Workflow KPI | fee reconciliation accuracy; unmatched receipt rate; baseline and threshold approved in pilot; source service KPI Verified order-event deduplication 100%; reconciliation accuracy target ≥99% |
| Preconditions / failure handling | Common contract (D-F12-030 variant 2, D-F12-031): §11.4b.5 |
| Cost | V12 illustrative ₹0.55/invocation (excludes provider, retry, labour). Blueprint model estimate ₹0.00/run for 0 agent step(s) at Tier 1a (Part 7.3 prices, FX ₹90/USD, verify at time of implementation, as of 27 Nov 2026); Tier 2 not eligible (Confidential/personal data) |
| Usage limit (pilot, not approved) | Illustrative pilot: 500 Marketplace order/event(s)/month; 1 concurrent run; approved caps, provider quotas and hard budget required. |
| Data modalities / version | Text; structured records; service 1.0-target, workflow 1.0-target |
| Acceptance (V12 → blueprint) | SM-SVC-31-WF04-TC-{POS,INPUT,SCOPE,ENT,DUP,QUALITY,BUDGET,RECOVERY} → TC-V12-D-101…108; SM-SVC-31-WF04-AT01 → TC-V12-D-111 |
| Release proposal | A2 |

| Step ID | Action (V12) | V12 executor → node type | Blueprint handler | Output contract | Failure → run state | Model tier | Status |
|---|---|---|---|---|---|---|---|
| SM-SVC-31-WF04-STEP-01 | Match sales and fees | Identity/reconciliation engine → NT13-07 `logic.compute` | AU-037 registered function | match_result {matched_refs,unmatched_refs,conflict_refs} | CONFLICT → HELD | Tier 0 / none | Matched |
| SM-SVC-31-WF04-STEP-02 | report anomalies and net performance | Domain service → NT13-05 `data.write_internal` | `commerce.marketplace` service (revision check) | domain_result {artifact_ref,status,evidence_refs} | INVALID_STATE → HELD | Tier 0 / none | Matched |

### 11.4.5.21 SM-SVC-32 Partner, Distributor & Co-Selling Automation

| Field | Specification |
|---|---|
| Family / objective | Partner growth; Manage partner enablement and joint opportunities |
| Channels / providers | Private Admin; approved client data and connectors; Authorized partner portal, CRM and agreement evidence |
| Optional producers / complementary | Included foundation; no mandatory upstream paid service; optional input producers: SM-SVC-02; SM-SVC-16; SM-SVC-22; SM-SVC-24; authorized equivalent input accepted. |
| Service KPI | Deal-registration conflict checks 100%; approved sharing only |
| Availability / bundle | Full / Lifecycle & Business Intelligence / selective (1 SKU); eligible inputs and approvals required. |
| Interoperability / readiness | Optional authorized connector; external agent access disabled unless explicitly granted; Proposed; test and validate customer demand, provider access and economics |
| Open-source stack | Python; Django REST Framework; PostgreSQL; Celery/Beat; Valkey; pgvector if needed; specialist library/provider review pending |
| Blueprint epic / module | EP-16 (ASSUMPTION-826) / `lifecycle.partners` |
| Effect adapter | Portal grant (AU-090 pattern, R16P) |
| Service guardrail | Commission is record-only (DEC-046); partners see only their own registrations (DEC-393). |
| Functional requirement | FR-V12-D-132 (§11.4.5.29 register) |

**DTO `urn:sm:dto:SM-SVC-32-WF0n:v2` (one schema shared by the four workflows; v3 projection per workflow below):**

| Dir | Field | JSON Schema (App. B v2) | V12 validation | Blueprint storage target |
|---|---|---|---|---|
| in | `partner_ref` | string format=uuid | UUID / scoped external reference; input, validate authorized scope | lcy_partner.id (ENT-153) |
| in | `territory_ref` | string format=uuid | UUID / scoped external reference; input, validate authorized scope | territory rules (AU-082) |
| in | `material_refs` | array maxItems=500 | array (typed references or structured items); input, validate authoriz | mkt_content_asset.id[] |
| in | `deal_ref` | string format=uuid | UUID / scoped external reference; input, validate authorized scope | crm_deal.id (ENT-086) |
| out | `shortlist_ref` | string format=uuid | UUID / scoped external reference; output, validate schema and evidence | aut_artifact (domain shortlist) |
| out | `access_grant_ref` | string format=uuid | UUID / scoped external reference; output, validate schema and evidence | object grant (portal, R16P) |
| out | `registration_ref` | string format=uuid | UUID / scoped external reference; output, validate schema and evidence | partner deal registration (WF-30) |
| out | `performance_ref` | string format=uuid | UUID / scoped external reference; output, validate schema and evidence | aut_artifact report |

#### SM-SVC-32-WF01 Partner recruitment and territory opportunity identification

| Field | Specification |
|---|---|
| V12 sources | BRD ch09 row; FSD ch12 lines 13545–13643; FSD ch13 registry row; App. B `urn:sm:dto:SM-SVC-32-WF01:v2`; workbook row "SM-SVC-32-WF01 — Partner recruitment and territory opportunity identification" |
| Business outcome | Partner recruitment and territory opportunity identification. Input → output: Territory plan, partner criteria, permitted leads → Partner shortlist |
| Detailed functionality (workbook) | Identify candidates; score fit; route approved engagement |
| Blueprint mapping | WF-30 partner co-sell (Part 9.8b); agents AG-032, AG-069; automations AU-082 |
| What V12 adds | Partner due-diligence brief exists (AG-032); V12 adds territory-fit scoring step. |
| Behaviour status | Partially covered → Matched |
| Trigger (V12) | Manual; scheduled monitoring; validated business event; authorized provider webhook when available; Territory plan, partner criteria, permitted leads |
| Trigger kinds (registry, DEC-564) | `manual` (NT13-03); `scheduled` (NT13-02; default cadence per §11.4b, misfire `reschedule_once`); `event` (NT13-01; `sm.svc32.wf01.requested` or upstream domain event, §11.4b.6); `provider_callback` (signed, replay-checked) |
| Authority (V12) | R0 internal analysis/draft; L1 assisted; L3 approved read/draft; Approve source/data rights and applicable external actions; approve consequential communications, commitments and changes; routine steps only within preapproved policies. |
| Blueprint autonomy (DEC-566) | V12 L1 assisted / L3 approved read-draft → blueprint **L0–L1** (drafts and analysis only; no external effect). Approver: R02 |
| Human approval (workbook) | Approve source/data rights and applicable external actions; approve consequential communications, commitments and changes; routine steps only within preapproved policies. |
| Effect boundary | No external effect; internal artifacts only |
| Outputs produced (v3 projection) | `shortlist_ref` |
| Workflow KPI | partner fit precision; territory conflict recall; baseline and threshold approved in pilot; source service KPI Deal-registration conflict checks 100%; approved sharing only |
| Preconditions / failure handling | Common contract (D-F12-030 variant 2, D-F12-031): §11.4b.5 |
| Cost | V12 illustrative ₹0.55/invocation (excludes provider, retry, labour). Blueprint model estimate ₹0.06/run for 2 agent step(s) at Tier 1a (Part 7.3 prices, FX ₹90/USD, verify at time of implementation, as of 27 Nov 2026); Tier 2 not eligible (Confidential/personal data) |
| Usage limit (pilot, not approved) | Illustrative pilot: 100 Partner opportunity(s)/month; 1 concurrent run; approved caps, provider quotas and hard budget required. |
| Data modalities / version | Text; structured records; service 1.0-target, workflow 1.0-target |
| Acceptance (V12 → blueprint) | SM-SVC-32-WF01-TC-{POS,INPUT,SCOPE,ENT,DUP,QUALITY,BUDGET,RECOVERY} → TC-V12-D-101…108; SM-SVC-32-WF01-AT01 → TC-V12-D-111 |
| Release proposal | A1 |

| Step ID | Action (V12) | V12 executor → node type | Blueprint handler | Output contract | Failure → run state | Model tier | Status |
|---|---|---|---|---|---|---|---|
| SM-SVC-32-WF01-STEP-01 | Identify candidates | Domain agent → NT13-08 `ai.task` + NT13-10 `approval.human` | AG-032 via gateway; routed to R02 | candidate {artifact_ref,confidence,reason_codes,review_state} | REVIEW_REQUIRED → AWAITING_APPROVAL | Tier 1a | Matched |
| SM-SVC-32-WF01-STEP-02 | score fit | Rules/analytics engine → NT13-07 `logic.compute` | AU-082 registered function | calculation {value,unit,assumptions,evidence_refs} | INVALID_METRIC → HELD | Tier 0 / none | Matched |
| SM-SVC-32-WF01-STEP-03 | route approved engagement | Domain agent → NT13-08 `ai.task` + NT13-10 `approval.human` | AG-032 via gateway; routed to R02 | candidate {artifact_ref,confidence,reason_codes,review_state} | REVIEW_REQUIRED → AWAITING_APPROVAL | Tier 1a | Matched |

#### SM-SVC-32-WF02 Partner product enablement and sales material distribution

| Field | Specification |
|---|---|
| V12 sources | BRD ch09 row; FSD ch12 lines 13644–13742; FSD ch13 registry row; App. B `urn:sm:dto:SM-SVC-32-WF02:v2`; workbook row "SM-SVC-32-WF02 — Partner product enablement and sales material distribution" |
| Business outcome | Partner product enablement and sales material distribution. Input → output: Approved materials, partner permissions → Enablement record |
| Detailed functionality (workbook) | Prepare training and materials; grant scoped access; track completion |
| Blueprint mapping | WF-30; DEC-393 partner portal; agents AG-070; automations AU-090, AU-083 |
| What V12 adds | Partner portal and enablement tracking exist; V12 adds scoped access grant as an explicit effect step. |
| Behaviour status | Partially covered → Matched |
| Trigger (V12) | Manual; scheduled monitoring; validated business event; authorized provider webhook when available; Approved materials, partner permissions |
| Trigger kinds (registry, DEC-564) | `manual` (NT13-03); `scheduled` (NT13-02; default cadence per §11.4b, misfire `reschedule_once`); `event` (NT13-01; `sm.svc32.wf02.requested` or upstream domain event, §11.4b.6); `provider_callback` (signed, replay-checked) |
| Authority (V12) | R2 external communication/provider/access write; L2 mandatory approved effect; L3 only with separately approved bounded mandate where lawful; Approve source/data rights and applicable external actions; approve consequential communications, commitments and changes; routine steps only within preapproved policies. |
| Blueprint autonomy (DEC-566) | V12 L2 exact approved effect → blueprint **L1 approval of the exact payload hash, then L2 dispatch** of that item through the outbox (DEC-064 publishing pattern); V12 L3 mandate only for routine replies/reminders within caps. Approver: R02, R10 |
| Human approval (workbook) | Approve source/data rights and applicable external actions; approve consequential communications, commitments and changes; routine steps only within preapproved policies. |
| Effect boundary | Effect steps: STEP-02 via Portal grant (AU-090 pattern, R16P) |
| Outputs produced (v3 projection) | `access_grant_ref` |
| Workflow KPI | access scope accuracy; completion tracking; baseline and threshold approved in pilot; source service KPI Deal-registration conflict checks 100%; approved sharing only |
| Preconditions / failure handling | Common contract (D-F12-030 variant 2, D-F12-031): §11.4b.5 |
| Cost | V12 illustrative ₹0.55/invocation (excludes provider, retry, labour). Blueprint model estimate ₹1.26/run for 1 agent step(s) at Tier 1a (Part 7.3 prices, FX ₹90/USD, verify at time of implementation, as of 27 Nov 2026); Tier 2 not eligible (Confidential/personal data) |
| Usage limit (pilot, not approved) | Illustrative pilot: 100 Partner opportunity(s)/month; 1 concurrent run; approved caps, provider quotas and hard budget required. |
| Data modalities / version | Text; structured records; service 1.0-target, workflow 1.0-target |
| Acceptance (V12 → blueprint) | SM-SVC-32-WF02-TC-{POS,INPUT,SCOPE,ENT,DUP,QUALITY,BUDGET,RECOVERY,APPROVAL,EFFECT} → TC-V12-D-101…110; SM-SVC-32-WF02-AT01 → TC-V12-D-111 |
| Release proposal | A1 |

| Step ID | Action (V12) | V12 executor → node type | Blueprint handler | Output contract | Failure → run state | Model tier | Status |
|---|---|---|---|---|---|---|---|
| SM-SVC-32-WF02-STEP-01 | Prepare training and materials | Domain agent → NT13-08 `ai.task` + NT13-10 `approval.human` | AG-070 via gateway; routed to R02 | candidate {artifact_ref,confidence,reason_codes,review_state} | REVIEW_REQUIRED → AWAITING_APPROVAL | Tier 1b | Matched |
| SM-SVC-32-WF02-STEP-02 | grant scoped access | Effect adapter → NT13-13 `action.external` | Outbox → AU-009 dispatch recheck → Portal grant (AU-090 pattern, R16P) | effect_receipt {provider_ref,status,observed_at} | EFFECT_UNKNOWN → RECONCILING | none | Matched |
| SM-SVC-32-WF02-STEP-03 | track completion | Domain service → NT13-05 `data.write_internal` | `lifecycle.partners` service (revision check) | domain_result {artifact_ref,status,evidence_refs} | INVALID_STATE → HELD | Tier 0 / none | Matched |

#### SM-SVC-32-WF03 Deal registration, lead sharing and co-selling coordination

| Field | Specification |
|---|---|
| V12 sources | BRD ch09 row; FSD ch12 lines 13743–13841; FSD ch13 registry row; App. B `urn:sm:dto:SM-SVC-32-WF03:v2`; workbook row "SM-SVC-32-WF03 — Deal registration, lead sharing and co-selling coordination" |
| Business outcome | Deal registration, lead sharing and co-selling coordination. Input → output: Partner deal request, sharing consent, ownership rules → Deal registration |
| Detailed functionality (workbook) | Validate scope; resolve conflicts; register and route opportunity |
| Blueprint mapping | WF-30 deal registration; agents AG-069; automations AU-091, AU-080 |
| What V12 adds | Registration conflict checks exist (AU-091); V12 binds them to step IDs. |
| Behaviour status | Partially covered → Matched |
| Trigger (V12) | Manual; scheduled monitoring; validated business event; authorized provider webhook when available; Partner deal request, sharing consent, ownership rules |
| Trigger kinds (registry, DEC-564) | `manual` (NT13-03); `scheduled` (NT13-02; default cadence per §11.4b, misfire `reschedule_once`); `event` (NT13-01; `sm.svc32.wf03.requested` or upstream domain event, §11.4b.6); `provider_callback` (signed, replay-checked) |
| Authority (V12) | R2 external communication/provider/access write; L2 mandatory approved effect; L3 only with separately approved bounded mandate where lawful; Approve source/data rights and applicable external actions; approve consequential communications, commitments and changes; routine steps only within preapproved policies. |
| Blueprint autonomy (DEC-566) | V12 L2 exact approved effect → blueprint **L1 approval of the exact payload hash, then L2 dispatch** of that item through the outbox (DEC-064 publishing pattern); V12 L3 mandate only for routine replies/reminders within caps. Approver: R03, R02 |
| Human approval (workbook) | Approve source/data rights and applicable external actions; approve consequential communications, commitments and changes; routine steps only within preapproved policies. |
| Effect boundary | No external effect; approval gate inserted before state change (DEC-570) |
| Outputs produced (v3 projection) | `registration_ref` |
| Workflow KPI | duplicate deal rate; sharing eligibility pass; baseline and threshold approved in pilot; source service KPI Deal-registration conflict checks 100%; approved sharing only |
| Preconditions / failure handling | Common contract (D-F12-030 variant 2, D-F12-031): §11.4b.5 |
| Cost | V12 illustrative ₹0.55/invocation (excludes provider, retry, labour). Blueprint model estimate ₹0.03/run for 1 agent step(s) at Tier 1a (Part 7.3 prices, FX ₹90/USD, verify at time of implementation, as of 27 Nov 2026); Tier 2 not eligible (Confidential/personal data) |
| Usage limit (pilot, not approved) | Illustrative pilot: 100 Partner opportunity(s)/month; 1 concurrent run; approved caps, provider quotas and hard budget required. |
| Data modalities / version | Text; structured records; service 1.0-target, workflow 1.0-target |
| Acceptance (V12 → blueprint) | SM-SVC-32-WF03-TC-{POS,INPUT,SCOPE,ENT,DUP,QUALITY,BUDGET,RECOVERY,APPROVAL,EFFECT} → TC-V12-D-101…110; SM-SVC-32-WF03-AT01 → TC-V12-D-111 |
| Release proposal | A1 |

| Step ID | Action (V12) | V12 executor → node type | Blueprint handler | Output contract | Failure → run state | Model tier | Status |
|---|---|---|---|---|---|---|---|
| SM-SVC-32-WF03-STEP-01 | Validate scope | Policy/validation engine → NT13-09 `policy.check` | PDP (AU-009) rule set | validation {passed,reason_codes,policy_version} | POLICY_DENIED → BLOCKED | Tier 0 / none | Matched |
| SM-SVC-32-WF03-STEP-02 | resolve conflicts | Identity/reconciliation engine → NT13-07 `logic.compute` | AU-091 registered function | match_result {matched_refs,unmatched_refs,conflict_refs} | CONFLICT → HELD | Tier 0 / none | Matched |
| SM-SVC-32-WF03-STEP-03 | register and route opportunity | Domain agent → NT13-08 `ai.task` + NT13-10 `approval.human` | AG-069 via gateway; routed to R03 | candidate {artifact_ref,confidence,reason_codes,review_state} | REVIEW_REQUIRED → AWAITING_APPROVAL | Tier 1a | Matched |

#### SM-SVC-32-WF04 Partner performance, commission evidence and expansion monitoring

| Field | Specification |
|---|---|
| V12 sources | BRD ch09 row; FSD ch12 lines 13842–13940; FSD ch13 registry row; App. B `urn:sm:dto:SM-SVC-32-WF04:v2`; workbook row "SM-SVC-32-WF04 — Partner performance, commission evidence and expansion monitoring" |
| Business outcome | Partner performance, commission evidence and expansion monitoring. Input → output: Approved agreement, verified deal outcomes → Partner performance report |
| Detailed functionality (workbook) | Calculate evidence-backed performance; flag disputed commission; review |
| Blueprint mapping | WF-30 commission records; agents AG-069; automations AU-092 |
| What V12 adds | Commission is record-only (DEC-046); V12 adds disputed-commission flag; R3 L3 mandate path not adopted. |
| Behaviour status | Partially covered → Matched (CONFLICT-814) |
| Trigger (V12) | Manual; scheduled monitoring; validated business event; authorized provider webhook when available; Approved agreement, verified deal outcomes |
| Trigger kinds (registry, DEC-564) | `manual` (NT13-03); `scheduled` (NT13-02; default cadence per §11.4b, misfire `reschedule_once`); `event` (NT13-01; `sm.svc32.wf04.requested` or upstream domain event, §11.4b.6); `provider_callback` (signed, replay-checked) |
| Authority (V12) | R3 financial/legal/commitment; L2 mandatory approved effect; L3 only with separately approved bounded mandate where lawful; Approve source/data rights and applicable external actions; approve consequential communications, commitments and changes; routine steps only within preapproved policies. |
| Blueprint autonomy (DEC-566) | V12 L2 default → blueprint **L1 maximum** (human approval bound to the exact hash; money movement not supported, DEC-064). V12 "L3 bounded mandate" **not adopted** (CONFLICT-814, Pending Founder decision). Approver: R08, R09 |
| Human approval (workbook) | Approve source/data rights and applicable external actions; approve consequential communications, commitments and changes; routine steps only within preapproved policies. |
| Effect boundary | No external effect; approval gate inserted before state change (DEC-570) |
| Outputs produced (v3 projection) | `performance_ref` |
| Workflow KPI | commission reconciliation; dispute detection; baseline and threshold approved in pilot; source service KPI Deal-registration conflict checks 100%; approved sharing only |
| Preconditions / failure handling | Common contract (D-F12-030 variant 2, D-F12-031): §11.4b.5 |
| Cost | V12 illustrative ₹0.55/invocation (excludes provider, retry, labour). Blueprint model estimate ₹0.03/run for 1 agent step(s) at Tier 1a (Part 7.3 prices, FX ₹90/USD, verify at time of implementation, as of 27 Nov 2026); Tier 2 not eligible (Confidential/personal data) |
| Usage limit (pilot, not approved) | Illustrative pilot: 100 Partner opportunity(s)/month; 1 concurrent run; approved caps, provider quotas and hard budget required. |
| Data modalities / version | Text; structured records; documents; service 1.0-target, workflow 1.0-target |
| Acceptance (V12 → blueprint) | SM-SVC-32-WF04-TC-{POS,INPUT,SCOPE,ENT,DUP,QUALITY,BUDGET,RECOVERY,APPROVAL,EFFECT} → TC-V12-D-101…110; SM-SVC-32-WF04-AT01 → TC-V12-D-111 |
| Release proposal | A1 |

| Step ID | Action (V12) | V12 executor → node type | Blueprint handler | Output contract | Failure → run state | Model tier | Status |
|---|---|---|---|---|---|---|---|
| SM-SVC-32-WF04-STEP-01 | Calculate evidence-backed performance | Rules/analytics engine → NT13-07 `logic.compute` | AU-092 registered function | calculation {value,unit,assumptions,evidence_refs} | INVALID_METRIC → HELD | Tier 0 / none | Matched |
| SM-SVC-32-WF04-STEP-02 | flag disputed commission | Domain agent → NT13-08 `ai.task` + NT13-10 `approval.human` | AG-069 via gateway; routed to R08 | candidate {artifact_ref,confidence,reason_codes,review_state} | REVIEW_REQUIRED → AWAITING_APPROVAL | Tier 1a | Matched |
| SM-SVC-32-WF04-STEP-03 | review | Domain service → NT13-05 `data.write_internal` | `lifecycle.partners` service (revision check) | domain_result {artifact_ref,status,evidence_refs} | INVALID_STATE → HELD | Tier 0 / none | Matched |

### 11.4.5.22 SM-SVC-33 Customer Service & Support Operations Automation

| Field | Specification |
|---|---|
| Family / objective | Support operations; Resolve support issues and track SLA |
| Channels / providers | Private Admin; approved client data and connectors; Authorized ticket system and knowledge sources |
| Optional producers / complementary | Included foundation; no mandatory upstream paid service; optional input producers: SM-SVC-09; SM-SVC-22; SM-SVC-23; SM-SVC-25; authorized equivalent input accepted. |
| Service KPI | SLA measurement coverage 100%; grounded response target ≥95% |
| Availability / bundle | Full / Lifecycle & Business Intelligence / selective (1 SKU); eligible inputs and approvals required. |
| Interoperability / readiness | Optional authorized connector; external agent access disabled unless explicitly granted; Proposed; test and validate customer demand, provider access and economics |
| Open-source stack | Python; Django REST Framework; PostgreSQL; Celery/Beat; Valkey; pgvector if needed; specialist library/provider review pending |
| Blueprint epic / module | EP-20 (ASSUMPTION-826) / `support.cases` |
| Effect adapter | ADP-EMAIL reply via outbox; portal (W28/W34) |
| Service guardrail | Self-service actions are limited to an allowlisted, reversible catalogue; everything else escalates to a human. |
| Functional requirement | FR-V12-D-133 (§11.4.5.29 register) |

**DTO `urn:sm:dto:SM-SVC-33-WF0n:v2` (one schema shared by the four workflows; v3 projection per workflow below):**

| Dir | Field | JSON Schema (App. B v2) | V12 validation | Blueprint storage target |
|---|---|---|---|---|
| in | `customer_ref` | string format=uuid | UUID / scoped external reference; input, validate authorized scope | crm_account / lcy customer (ENT-086 deal owner account) |
| in | `enquiry_ref` | string format=uuid | UUID / scoped external reference; input, validate authorized scope | eng_inbound_event / eng_thread |
| in | `sla_policy_ref` | string format=uuid | UUID / scoped external reference; input, validate authorized scope | SLA policy config |
| in | `knowledge_refs` | array maxItems=500 | array (typed references or structured items); input, validate authoriz | cat_chunk.id[] (ENT-025) |
| out | `case_ref` | string format=uuid | UUID / scoped external reference; output, validate schema and evidence | sup_case (proposed) |
| out | `severity` | string maxLength=64 | string / configured enum; length and allowed values in versioned schem | enum {S1, S2, S3, S4} |
| out | `queue_ref` | string format=uuid | UUID / scoped external reference; output, validate schema and evidence | support queue config |
| out | `resolution_ref` | string format=uuid | UUID / scoped external reference; output, validate schema and evidence | aut_artifact (resolution) |
| out | `sla_state` | string maxLength=64 | string / configured enum; length and allowed values in versioned schem | enum {within, at_risk, breached, paused} |

#### SM-SVC-33-WF01 Customer support ticket creation, classification and routing

| Field | Specification |
|---|---|
| V12 sources | BRD ch09 row; FSD ch12 lines 13942–14043; FSD ch13 registry row; App. B `urn:sm:dto:SM-SVC-33-WF01:v2`; workbook row "SM-SVC-33-WF01 — Customer support ticket creation, classification and routing" |
| Business outcome | Customer support ticket creation, classification and routing. Input → output: Customer enquiry, entitlement, SLA policy → Support case |
| Detailed functionality (workbook) | Create or match case; classify severity; assign queue |
| Blueprint mapping | Portal support W28/W34; AG-031; agents AG-031; automations AU-074, AU-027 |
| What V12 adds | Ticket triage exists (AG-031); V12 adds case match/creation and queue assignment as step IDs. |
| Behaviour status | Partially covered → Matched |
| Trigger (V12) | Manual; scheduled monitoring; validated business event; authorized provider webhook when available; Customer enquiry, entitlement, SLA policy |
| Trigger kinds (registry, DEC-564) | `manual` (NT13-03); `scheduled` (NT13-02; default cadence per §11.4b, misfire `reschedule_once`); `event` (NT13-01; `sm.svc33.wf01.requested` or upstream domain event, §11.4b.6); `provider_callback` (signed, replay-checked) |
| Authority (V12) | R1 scoped state write or safety control; L1/L2 review; L3 only for approved deterministic internal actions; Approve source/data rights and applicable external actions; approve consequential communications, commitments and changes; routine steps only within preapproved policies. |
| Blueprint autonomy (DEC-566) | V12 L1/L2 review; L3 only for approved deterministic internal actions → blueprint **L1** for state writes, **L3** only for registered deterministic internal steps (DEC-064). Approver: R13 or tenant support lead |
| Human approval (workbook) | Approve source/data rights and applicable external actions; approve consequential communications, commitments and changes; routine steps only within preapproved policies. |
| Effect boundary | No external effect; internal artifacts only |
| Outputs produced (v3 projection) | `case_ref`, `severity`, `queue_ref` |
| Workflow KPI | routing accuracy; duplicate case count; baseline and threshold approved in pilot; source service KPI SLA measurement coverage 100%; grounded response target ≥95% |
| Preconditions / failure handling | Common contract (D-F12-030 variant 2, D-F12-031): §11.4b.5 |
| Cost | V12 illustrative ₹1.05/invocation (excludes provider, retry, labour). Blueprint model estimate ₹0.06/run for 2 agent step(s) at Tier 1a (Part 7.3 prices, FX ₹90/USD, verify at time of implementation, as of 27 Nov 2026); Tier 2 not eligible (Confidential/personal data) |
| Usage limit (pilot, not approved) | Illustrative pilot: 500 Support case(s)/month; 1 concurrent run; approved caps, provider quotas and hard budget required. |
| Data modalities / version | Text; structured records; service 1.0-target, workflow 1.0-target |
| Acceptance (V12 → blueprint) | SM-SVC-33-WF01-TC-{POS,INPUT,SCOPE,ENT,DUP,QUALITY,BUDGET,RECOVERY} → TC-V12-D-101…108; SM-SVC-33-WF01-AT01 → TC-V12-D-111 |
| Release proposal | R2 alignment |

| Step ID | Action (V12) | V12 executor → node type | Blueprint handler | Output contract | Failure → run state | Model tier | Status |
|---|---|---|---|---|---|---|---|
| SM-SVC-33-WF01-STEP-01 | Create or match case | Identity/reconciliation engine → NT13-07 `logic.compute` | AU-074 registered function | match_result {matched_refs,unmatched_refs,conflict_refs} | CONFLICT → HELD | Tier 0 / none | Matched |
| SM-SVC-33-WF01-STEP-02 | classify severity | Domain agent → NT13-08 `ai.task` + NT13-10 `approval.human` | AG-031 via gateway; routed to R13 or tenant support lead | candidate {artifact_ref,confidence,reason_codes,review_state} | REVIEW_REQUIRED → AWAITING_APPROVAL | Tier 1a | Matched |
| SM-SVC-33-WF01-STEP-03 | assign queue | Domain agent → NT13-08 `ai.task` + NT13-10 `approval.human` | AG-031 via gateway; routed to R13 or tenant support lead | candidate {artifact_ref,confidence,reason_codes,review_state} | REVIEW_REQUIRED → AWAITING_APPROVAL | Tier 1a | Matched |

#### SM-SVC-33-WF02 Evidence-grounded resolution and authorized self-service

| Field | Specification |
|---|---|
| V12 sources | BRD ch09 row; FSD ch12 lines 14044–14145; FSD ch13 registry row; App. B `urn:sm:dto:SM-SVC-33-WF02:v2`; workbook row "SM-SVC-33-WF02 — Evidence-grounded resolution and authorized self-service" |
| Business outcome | Evidence-grounded resolution and authorized self-service. Input → output: Case context, approved knowledge, action grants → Resolution or handover |
| Detailed functionality (workbook) | Retrieve evidence; propose fix; execute eligible self-service or escalate |
| Blueprint mapping | AG-031 / AG-014 grounded replies; agents AG-031, AG-014; automations AU-009, AU-022 |
| What V12 adds | Grounded reply drafts exist; V12 adds allowlisted self-service actions as approved effects. |
| Behaviour status | Partially covered → Matched |
| Trigger (V12) | Manual; scheduled monitoring; validated business event; authorized provider webhook when available; Case context, approved knowledge, action grants |
| Trigger kinds (registry, DEC-564) | `manual` (NT13-03); `scheduled` (NT13-02; default cadence per §11.4b, misfire `reschedule_once`); `event` (NT13-01; `sm.svc33.wf02.requested` or upstream domain event, §11.4b.6); `provider_callback` (signed, replay-checked) |
| Authority (V12) | R2 external communication/provider/access write; L2 mandatory approved effect; L3 only with separately approved bounded mandate where lawful; Approve source/data rights and applicable external actions; approve consequential communications, commitments and changes; routine steps only within preapproved policies. |
| Blueprint autonomy (DEC-566) | V12 L2 exact approved effect → blueprint **L1 approval of the exact payload hash, then L2 dispatch** of that item through the outbox (DEC-064 publishing pattern); V12 L3 mandate only for routine replies/reminders within caps. Approver: Tenant support lead |
| Human approval (workbook) | Approve source/data rights and applicable external actions; approve consequential communications, commitments and changes; routine steps only within preapproved policies. |
| Effect boundary | Effect steps: STEP-03 via ADP-EMAIL reply via outbox; portal (W28/W34) |
| Outputs produced (v3 projection) | `resolution_ref` |
| Workflow KPI | grounding quality; escalation recall; baseline and threshold approved in pilot; source service KPI SLA measurement coverage 100%; grounded response target ≥95% |
| Preconditions / failure handling | Common contract (D-F12-030 variant 2, D-F12-031): §11.4b.5 |
| Cost | V12 illustrative ₹0.55/invocation (excludes provider, retry, labour). Blueprint model estimate ₹1.26/run for 1 agent step(s) at Tier 1a (Part 7.3 prices, FX ₹90/USD, verify at time of implementation, as of 27 Nov 2026); Tier 2 not eligible (Confidential/personal data) |
| Usage limit (pilot, not approved) | Illustrative pilot: 500 Support case(s)/month; 1 concurrent run; approved caps, provider quotas and hard budget required. |
| Data modalities / version | Text; structured records; documents; service 1.0-target, workflow 1.0-target |
| Acceptance (V12 → blueprint) | SM-SVC-33-WF02-TC-{POS,INPUT,SCOPE,ENT,DUP,QUALITY,BUDGET,RECOVERY,APPROVAL,EFFECT} → TC-V12-D-101…110; SM-SVC-33-WF02-AT01 → TC-V12-D-111 |
| Release proposal | A1 |

| Step ID | Action (V12) | V12 executor → node type | Blueprint handler | Output contract | Failure → run state | Model tier | Status |
|---|---|---|---|---|---|---|---|
| SM-SVC-33-WF02-STEP-01 | Retrieve evidence | Evidence/ingestion engine → NT13-04 `data.read` | AU-007 source permission + AU-005 sanitizer, scoped read | evidence_set {items,source_ref,observed_at,hash,rights} | SOURCE_DENIED → HELD | Tier 0 / none | Matched |
| SM-SVC-33-WF02-STEP-02 | propose fix | Domain agent → NT13-08 `ai.task` + NT13-10 `approval.human` | AG-014 via gateway; routed to Tenant support lead | candidate {artifact_ref,confidence,reason_codes,review_state} | REVIEW_REQUIRED → AWAITING_APPROVAL | Tier 1b | Matched |
| SM-SVC-33-WF02-STEP-03 | execute eligible self-service or escalate | Effect adapter → NT13-13 `action.external` | Outbox → AU-009 dispatch recheck → ADP-EMAIL reply via outbox; portal (W28/W34) | effect_receipt {provider_ref,status,observed_at} | EFFECT_UNKNOWN → RECONCILING | none | Matched |

#### SM-SVC-33-WF03 SLA monitoring, escalation and service recovery

| Field | Specification |
|---|---|
| V12 sources | BRD ch09 row; FSD ch12 lines 14146–14247; FSD ch13 registry row; App. B `urn:sm:dto:SM-SVC-33-WF03:v2`; workbook row "SM-SVC-33-WF03 — SLA monitoring, escalation and service recovery" |
| Business outcome | SLA monitoring, escalation and service recovery. Input → output: Case timeline, SLA and owner → SLA exception |
| Detailed functionality (workbook) | Calculate deadline; alert risk; escalate overdue issue |
| Blueprint mapping | AU-027 SLA escalation; agents AG-031; automations AU-027 |
| What V12 adds | SLA timers and escalation ladders exist (AU-027); V12 adds per-case deadline calculation from SLA policy. |
| Behaviour status | Partially covered → Matched |
| Trigger (V12) | Manual; scheduled monitoring; validated business event; authorized provider webhook when available; Case timeline, SLA and owner |
| Trigger kinds (registry, DEC-564) | `manual` (NT13-03); `scheduled` (NT13-02; default cadence per §11.4b, misfire `reschedule_once`); `event` (NT13-01; `sm.svc33.wf03.requested` or upstream domain event, §11.4b.6); `provider_callback` (signed, replay-checked) |
| Authority (V12) | R1 scoped state write or safety control; L1/L2 review; L3 only for approved deterministic internal actions; Approve source/data rights and applicable external actions; approve consequential communications, commitments and changes; routine steps only within preapproved policies. |
| Blueprint autonomy (DEC-566) | V12 L1/L2 review; L3 only for approved deterministic internal actions → blueprint **L1** for state writes, **L3** only for registered deterministic internal steps (DEC-064). Approver: Tenant support lead |
| Human approval (workbook) | Approve source/data rights and applicable external actions; approve consequential communications, commitments and changes; routine steps only within preapproved policies. |
| Effect boundary | No external effect; internal artifacts only |
| Outputs produced (v3 projection) | `sla_state` |
| Workflow KPI | deadline accuracy; breach alert latency; baseline and threshold approved in pilot; source service KPI SLA measurement coverage 100%; grounded response target ≥95% |
| Preconditions / failure handling | Common contract (D-F12-030 variant 2, D-F12-031): §11.4b.5 |
| Cost | V12 illustrative ₹0.55/invocation (excludes provider, retry, labour). Blueprint model estimate ₹0.03/run for 1 agent step(s) at Tier 1a (Part 7.3 prices, FX ₹90/USD, verify at time of implementation, as of 27 Nov 2026); Tier 2 not eligible (Confidential/personal data) |
| Usage limit (pilot, not approved) | Illustrative pilot: 500 Support case(s)/month; 1 concurrent run; approved caps, provider quotas and hard budget required. |
| Data modalities / version | Text; structured records; service 1.0-target, workflow 1.0-target |
| Acceptance (V12 → blueprint) | SM-SVC-33-WF03-TC-{POS,INPUT,SCOPE,ENT,DUP,QUALITY,BUDGET,RECOVERY} → TC-V12-D-101…108; SM-SVC-33-WF03-AT01 → TC-V12-D-111 |
| Release proposal | R2 alignment |

| Step ID | Action (V12) | V12 executor → node type | Blueprint handler | Output contract | Failure → run state | Model tier | Status |
|---|---|---|---|---|---|---|---|
| SM-SVC-33-WF03-STEP-01 | Calculate deadline | Rules/analytics engine → NT13-07 `logic.compute` | AU-027 registered function | calculation {value,unit,assumptions,evidence_refs} | INVALID_METRIC → HELD | Tier 0 / none | Matched |
| SM-SVC-33-WF03-STEP-02 | alert risk | Domain agent → NT13-08 `ai.task` + NT13-10 `approval.human` | AG-031 via gateway; routed to Tenant support lead | candidate {artifact_ref,confidence,reason_codes,review_state} | REVIEW_REQUIRED → AWAITING_APPROVAL | Tier 1a | Matched |
| SM-SVC-33-WF03-STEP-03 | escalate overdue issue | Domain service → NT13-05 `data.write_internal` | `support.cases` service (revision check) | domain_result {artifact_ref,status,evidence_refs} | INVALID_STATE → HELD | Tier 0 / none | Matched |

#### SM-SVC-33-WF04 Support quality, recurring issue and resolution intelligence

| Field | Specification |
|---|---|
| V12 sources | BRD ch09 row; FSD ch12 lines 14248–14349; FSD ch13 registry row; App. B `urn:sm:dto:SM-SVC-33-WF04:v2`; workbook row "SM-SVC-33-WF04 — Support quality, recurring issue and resolution intelligence" |
| Business outcome | Support quality, recurring issue and resolution intelligence. Input → output: Case outcomes, feedback, permitted transcripts → Support quality report |
| Detailed functionality (workbook) | Analyze themes; identify repeat causes; recommend corrective work |
| Blueprint mapping | WF-32 VoC themes; agents AG-068, AG-028; automations AU-102 |
| What V12 adds | Theme synthesis exists (AG-068); V12 adds recurring-cause detection over support cases. |
| Behaviour status | Partially covered → Matched |
| Trigger (V12) | Manual; scheduled monitoring; validated business event; authorized provider webhook when available; Case outcomes, feedback, permitted transcripts |
| Trigger kinds (registry, DEC-564) | `manual` (NT13-03); `scheduled` (NT13-02; default cadence per §11.4b, misfire `reschedule_once`); `event` (NT13-01; `sm.svc33.wf04.requested` or upstream domain event, §11.4b.6); `provider_callback` (signed, replay-checked) |
| Authority (V12) | R0 internal analysis/draft; L1 assisted; L3 approved read/draft; Approve source/data rights and applicable external actions; approve consequential communications, commitments and changes; routine steps only within preapproved policies. |
| Blueprint autonomy (DEC-566) | V12 L1 assisted / L3 approved read-draft → blueprint **L0–L1** (drafts and analysis only; no external effect). Approver: Tenant support lead |
| Human approval (workbook) | Approve source/data rights and applicable external actions; approve consequential communications, commitments and changes; routine steps only within preapproved policies. |
| Effect boundary | No external effect; internal artifacts only |
| Outputs produced (v3 projection) | `resolution_ref` |
| Workflow KPI | recurring issue recall; corrective action coverage; baseline and threshold approved in pilot; source service KPI SLA measurement coverage 100%; grounded response target ≥95% |
| Preconditions / failure handling | Common contract (D-F12-030 variant 2, D-F12-031): §11.4b.5 |
| Cost | V12 illustrative ₹1.05/invocation (excludes provider, retry, labour). Blueprint model estimate ₹1.29/run for 2 agent step(s) at Tier 1a (Part 7.3 prices, FX ₹90/USD, verify at time of implementation, as of 27 Nov 2026); Tier 2 not eligible (Confidential/personal data) |
| Usage limit (pilot, not approved) | Illustrative pilot: 500 Support case(s)/month; 1 concurrent run; approved caps, provider quotas and hard budget required. |
| Data modalities / version | Text; structured records; service 1.0-target, workflow 1.0-target |
| Acceptance (V12 → blueprint) | SM-SVC-33-WF04-TC-{POS,INPUT,SCOPE,ENT,DUP,QUALITY,BUDGET,RECOVERY} → TC-V12-D-101…108; SM-SVC-33-WF04-AT01 → TC-V12-D-111 |
| Release proposal | A1 |

| Step ID | Action (V12) | V12 executor → node type | Blueprint handler | Output contract | Failure → run state | Model tier | Status |
|---|---|---|---|---|---|---|---|
| SM-SVC-33-WF04-STEP-01 | Analyze themes | Domain service → NT13-05 `data.write_internal` | `support.cases` service (revision check) | domain_result {artifact_ref,status,evidence_refs} | INVALID_STATE → HELD | Tier 0 / none | Matched |
| SM-SVC-33-WF04-STEP-02 | identify repeat causes | Domain agent → NT13-08 `ai.task` + NT13-10 `approval.human` | AG-028 via gateway; routed to Tenant support lead | candidate {artifact_ref,confidence,reason_codes,review_state} | REVIEW_REQUIRED → AWAITING_APPROVAL | Tier 1a | Matched |
| SM-SVC-33-WF04-STEP-03 | recommend corrective work | Domain agent → NT13-08 `ai.task` + NT13-10 `approval.human` | AG-068 via gateway; routed to Tenant support lead | candidate {artifact_ref,confidence,reason_codes,review_state} | REVIEW_REQUIRED → AWAITING_APPROVAL | Tier 1b | Matched |

### 11.4.5.23 SM-SVC-34 Product-Led Growth & Usage Intelligence Automation

| Field | Specification |
|---|---|
| Family / objective | Usage intelligence; Increase adoption and identify eligible expansion |
| Channels / providers | Private Admin; approved client data and connectors; Authorized product analytics and subscription system |
| Optional producers / complementary | Included foundation; no mandatory upstream paid service; optional input producers: SM-SVC-04; SM-SVC-15; SM-SVC-22; SM-SVC-23; SM-SVC-24; authorized equivalent input accepted. |
| Service KPI | Usage event integrity target ≥99%; unapproved upgrades = 0 |
| Availability / bundle | Full / Lifecycle & Business Intelligence / selective (1 SKU); eligible inputs and approvals required. |
| Interoperability / readiness | Optional authorized connector; external agent access disabled unless explicitly granted; Proposed; test and validate customer demand, provider access and economics |
| Open-source stack | Python; Django REST Framework; PostgreSQL; Celery/Beat; Valkey; pgvector if needed; specialist library/provider review pending |
| Blueprint epic / module | EP-20 (ASSUMPTION-826) / `lifecycle.usage` |
| Effect adapter | none (recommendations only) |
| Service guardrail | Product events enter only through the ADR-105 allowlisted ingress; no automatic plan change or charge. |
| Functional requirement | FR-V12-D-134 (§11.4.5.29 register) |

**DTO `urn:sm:dto:SM-SVC-34-WF0n:v2` (one schema shared by the four workflows; v3 projection per workflow below):**

| Dir | Field | JSON Schema (App. B v2) | V12 validation | Blueprint storage target |
|---|---|---|---|---|
| in | `account_ref` | string format=uuid | UUID / scoped external reference; input, validate authorized scope | intel_organization / crm account (ENT-063) |
| in | `event_refs` | array maxItems=500 | array (typed references or structured items); input, validate authoriz | ops_domain_event.id[] (ENT-170) |
| in | `feature_refs` | array maxItems=500 | array (typed references or structured items); input, validate authoriz | product feature registry |
| in | `plan_ref` | string format=uuid | UUID / scoped external reference; input, validate authorized scope | aut_artifact (domain plan) or lcy_onboarding (ENT-147) |
| out | `activation_state` | string maxLength=64 | string / configured enum; length and allowed values in versioned schem | enum {not_started, activating, activated, stalled} |
| out | `usage_report_ref` | string format=uuid | UUID / scoped external reference; output, validate schema and evidence | aut_artifact report |
| out | `expansion_ref` | string format=uuid | UUID / scoped external reference; output, validate schema and evidence | aut_artifact (expansion signal) |
| out | `recommendation_ref` | string format=uuid | UUID / scoped external reference; output, validate schema and evidence | aut_artifact (domain recommendation) |

#### SM-SVC-34-WF01 Authorized product usage and activation event analysis

| Field | Specification |
|---|---|
| V12 sources | BRD ch09 row; FSD ch12 lines 14351–14449; FSD ch13 registry row; App. B `urn:sm:dto:SM-SVC-34-WF01:v2`; workbook row "SM-SVC-34-WF01 — Authorized product usage and activation event analysis" |
| Business outcome | Authorized product usage and activation event analysis. Input → output: Consented event stream, account IDs, metric definitions → Usage scorecard |
| Detailed functionality (workbook) | Validate events; aggregate usage; identify activation state |
| Blueprint mapping | ADR-105 product-event ingress (Part 3.4); AU-042 metering; agents AG-067; automations AU-042, AU-103 |
| What V12 adds | Allowlisted product events and metering exist; V12 adds activation-state classification. |
| Behaviour status | Partially covered → Matched |
| Trigger (V12) | Manual; scheduled monitoring; validated business event; authorized provider webhook when available; Consented event stream, account IDs, metric definitions |
| Trigger kinds (registry, DEC-564) | `manual` (NT13-03); `scheduled` (NT13-02; default cadence per §11.4b, misfire `reschedule_once`); `event` (NT13-01; `sm.svc34.wf01.requested` or upstream domain event, §11.4b.6); `provider_callback` (signed, replay-checked) |
| Authority (V12) | R0 internal analysis/draft; L1 assisted; L3 approved read/draft; Approve source/data rights and applicable external actions; approve consequential communications, commitments and changes; routine steps only within preapproved policies. |
| Blueprint autonomy (DEC-566) | V12 L1 assisted / L3 approved read-draft → blueprint **L0–L1** (drafts and analysis only; no external effect). Approver: R03 |
| Human approval (workbook) | Approve source/data rights and applicable external actions; approve consequential communications, commitments and changes; routine steps only within preapproved policies. |
| Effect boundary | No external effect; internal artifacts only |
| Outputs produced (v3 projection) | `activation_state`, `usage_report_ref` |
| Workflow KPI | event validity; activation accuracy; baseline and threshold approved in pilot; source service KPI Usage event integrity target ≥99%; unapproved upgrades = 0 |
| Preconditions / failure handling | Common contract (D-F12-030 variant 2, D-F12-031): §11.4b.5 |
| Cost | V12 illustrative ₹1.05/invocation (excludes provider, retry, labour). Blueprint model estimate ₹0.03/run for 1 agent step(s) at Tier 1a (Part 7.3 prices, FX ₹90/USD, verify at time of implementation, as of 27 Nov 2026); Tier 2 not eligible (Confidential/personal data) |
| Usage limit (pilot, not approved) | Illustrative pilot: 200 Account usage review(s)/month; 1 concurrent run; approved caps, provider quotas and hard budget required. |
| Data modalities / version | Text; structured records; service 1.0-target, workflow 1.0-target |
| Acceptance (V12 → blueprint) | SM-SVC-34-WF01-TC-{POS,INPUT,SCOPE,ENT,DUP,QUALITY,BUDGET,RECOVERY} → TC-V12-D-101…108; SM-SVC-34-WF01-AT01 → TC-V12-D-111 |
| Release proposal | A2 |

| Step ID | Action (V12) | V12 executor → node type | Blueprint handler | Output contract | Failure → run state | Model tier | Status |
|---|---|---|---|---|---|---|---|
| SM-SVC-34-WF01-STEP-01 | Validate events | Policy/validation engine → NT13-09 `policy.check` | PDP (AU-009) rule set | validation {passed,reason_codes,policy_version} | POLICY_DENIED → BLOCKED | Tier 0 / none | Matched |
| SM-SVC-34-WF01-STEP-02 | aggregate usage | Rules/analytics engine → NT13-07 `logic.compute` | AU-042 registered function | calculation {value,unit,assumptions,evidence_refs} | INVALID_METRIC → HELD | Tier 0 / none | Matched |
| SM-SVC-34-WF01-STEP-03 | identify activation state | Domain agent → NT13-08 `ai.task` + NT13-10 `approval.human` | AG-067 via gateway; routed to R03 | candidate {artifact_ref,confidence,reason_codes,review_state} | REVIEW_REQUIRED → AWAITING_APPROVAL | Tier 1a | Matched |

#### SM-SVC-34-WF02 Trial conversion and customer activation journeys

| Field | Specification |
|---|---|
| V12 sources | BRD ch09 row; FSD ch12 lines 14450–14548; FSD ch13 registry row; App. B `urn:sm:dto:SM-SVC-34-WF02:v2`; workbook row "SM-SVC-34-WF02 — Trial conversion and customer activation journeys" |
| Business outcome | Trial conversion and customer activation journeys. Input → output: Trial state, product milestones, eligible channels → Activation journey |
| Detailed functionality (workbook) | Detect blockers; recommend approved onboarding action; monitor conversion |
| Blueprint mapping | §2.22.4 SaaS onboarding; WF-31; agents AG-030, AG-038; automations AU-009, AU-022 |
| What V12 adds | SaaS onboarding exists; V12 adds trial-blocker detection and approved activation actions. |
| Behaviour status | Partially covered → Matched |
| Trigger (V12) | Manual; scheduled monitoring; validated business event; authorized provider webhook when available; Trial state, product milestones, eligible channels |
| Trigger kinds (registry, DEC-564) | `manual` (NT13-03); `scheduled` (NT13-02; default cadence per §11.4b, misfire `reschedule_once`); `event` (NT13-01; `sm.svc34.wf02.requested` or upstream domain event, §11.4b.6); `provider_callback` (signed, replay-checked) |
| Authority (V12) | R2 external communication/provider/access write; L2 mandatory approved effect; L3 only with separately approved bounded mandate where lawful; Approve source/data rights and applicable external actions; approve consequential communications, commitments and changes; routine steps only within preapproved policies. |
| Blueprint autonomy (DEC-566) | V12 L2 exact approved effect → blueprint **L1 approval of the exact payload hash, then L2 dispatch** of that item through the outbox (DEC-064 publishing pattern); V12 L3 mandate only for routine replies/reminders within caps. Approver: R03 |
| Human approval (workbook) | Approve source/data rights and applicable external actions; approve consequential communications, commitments and changes; routine steps only within preapproved policies. |
| Effect boundary | No external effect; approval gate inserted before state change (DEC-570) |
| Outputs produced (v3 projection) | `activation_state` |
| Workflow KPI | blocker recall; conversion measurement coverage; baseline and threshold approved in pilot; source service KPI Usage event integrity target ≥99%; unapproved upgrades = 0 |
| Preconditions / failure handling | Common contract (D-F12-030 variant 2, D-F12-031): §11.4b.5 |
| Cost | V12 illustrative ₹0.55/invocation (excludes provider, retry, labour). Blueprint model estimate ₹1.29/run for 2 agent step(s) at Tier 1a (Part 7.3 prices, FX ₹90/USD, verify at time of implementation, as of 27 Nov 2026); Tier 2 not eligible (Confidential/personal data) |
| Usage limit (pilot, not approved) | Illustrative pilot: 200 Account usage review(s)/month; 1 concurrent run; approved caps, provider quotas and hard budget required. |
| Data modalities / version | Text; structured records; service 1.0-target, workflow 1.0-target |
| Acceptance (V12 → blueprint) | SM-SVC-34-WF02-TC-{POS,INPUT,SCOPE,ENT,DUP,QUALITY,BUDGET,RECOVERY,APPROVAL,EFFECT} → TC-V12-D-101…110; SM-SVC-34-WF02-AT01 → TC-V12-D-111 |
| Release proposal | A2 |

| Step ID | Action (V12) | V12 executor → node type | Blueprint handler | Output contract | Failure → run state | Model tier | Status |
|---|---|---|---|---|---|---|---|
| SM-SVC-34-WF02-STEP-01 | Detect blockers | Domain agent → NT13-08 `ai.task` + NT13-10 `approval.human` | AG-030 via gateway; routed to R03 | candidate {artifact_ref,confidence,reason_codes,review_state} | REVIEW_REQUIRED → AWAITING_APPROVAL | Tier 1a | Matched |
| SM-SVC-34-WF02-STEP-02 | recommend approved onboarding action | Domain agent → NT13-08 `ai.task` + NT13-10 `approval.human` | AG-038 via gateway; routed to R03 | candidate {artifact_ref,confidence,reason_codes,review_state} | REVIEW_REQUIRED → AWAITING_APPROVAL | Tier 1b | Matched |
| SM-SVC-34-WF02-STEP-03 | monitor conversion | Domain service → NT13-05 `data.write_internal` | `lifecycle.usage` service (revision check) | domain_result {artifact_ref,status,evidence_refs} | INVALID_STATE → HELD | Tier 0 / none | Matched |

#### SM-SVC-34-WF03 Feature adoption and expansion opportunity detection

| Field | Specification |
|---|---|
| V12 sources | BRD ch09 row; FSD ch12 lines 14549–14635; FSD ch13 registry row; App. B `urn:sm:dto:SM-SVC-34-WF03:v2`; workbook row "SM-SVC-34-WF03 — Feature adoption and expansion opportunity detection" |
| Business outcome | Feature adoption and expansion opportunity detection. Input → output: Usage metrics, feature entitlement, plan catalog → Expansion recommendation |
| Detailed functionality (workbook) | Detect adoption gaps and eligible expansion signals |
| Blueprint mapping | WF-31 expansion; agents AG-067; automations AU-093 |
| What V12 adds | Expansion readiness exists; V12 adds feature-adoption gap detection. |
| Behaviour status | Partially covered → Matched |
| Trigger (V12) | Manual; scheduled monitoring; validated business event; authorized provider webhook when available; Usage metrics, feature entitlement, plan catalog |
| Trigger kinds (registry, DEC-564) | `manual` (NT13-03); `scheduled` (NT13-02; default cadence per §11.4b, misfire `reschedule_once`); `event` (NT13-01; `sm.svc34.wf03.requested` or upstream domain event, §11.4b.6); `provider_callback` (signed, replay-checked) |
| Authority (V12) | R0 internal analysis/draft; L1 assisted; L3 approved read/draft; Approve source/data rights and applicable external actions; approve consequential communications, commitments and changes; routine steps only within preapproved policies. |
| Blueprint autonomy (DEC-566) | V12 L1 assisted / L3 approved read-draft → blueprint **L0–L1** (drafts and analysis only; no external effect). Approver: R03 |
| Human approval (workbook) | Approve source/data rights and applicable external actions; approve consequential communications, commitments and changes; routine steps only within preapproved policies. |
| Effect boundary | No external effect; internal artifacts only |
| Outputs produced (v3 projection) | `expansion_ref`, `recommendation_ref` |
| Workflow KPI | adoption gap accuracy; expansion precision; baseline and threshold approved in pilot; source service KPI Usage event integrity target ≥99%; unapproved upgrades = 0 |
| Preconditions / failure handling | Common contract (D-F12-030 variant 2, D-F12-031): §11.4b.5 |
| Cost | V12 illustrative ₹0.55/invocation (excludes provider, retry, labour). Blueprint model estimate ₹0.03/run for 1 agent step(s) at Tier 1a (Part 7.3 prices, FX ₹90/USD, verify at time of implementation, as of 27 Nov 2026); Tier 2 not eligible (Confidential/personal data) |
| Usage limit (pilot, not approved) | Illustrative pilot: 200 Account usage review(s)/month; 1 concurrent run; approved caps, provider quotas and hard budget required. |
| Data modalities / version | Text; structured records; service 1.0-target, workflow 1.0-target |
| Acceptance (V12 → blueprint) | SM-SVC-34-WF03-TC-{POS,INPUT,SCOPE,ENT,DUP,QUALITY,BUDGET,RECOVERY} → TC-V12-D-101…108; SM-SVC-34-WF03-AT01 → TC-V12-D-111 |
| Release proposal | A2 |

| Step ID | Action (V12) | V12 executor → node type | Blueprint handler | Output contract | Failure → run state | Model tier | Status |
|---|---|---|---|---|---|---|---|
| SM-SVC-34-WF03-STEP-01 | Detect adoption gaps and eligible expansion signals | Domain agent → NT13-08 `ai.task` + NT13-10 `approval.human` | AG-067 via gateway; routed to R03 | candidate {artifact_ref,confidence,reason_codes,review_state} | REVIEW_REQUIRED → AWAITING_APPROVAL | Tier 1a | Matched |

#### SM-SVC-34-WF04 Usage-based upgrade and customer engagement recommendations

| Field | Specification |
|---|---|
| V12 sources | BRD ch09 row; FSD ch12 lines 14636–14734; FSD ch13 registry row; App. B `urn:sm:dto:SM-SVC-34-WF04:v2`; workbook row "SM-SVC-34-WF04 — Usage-based upgrade and customer engagement recommendations" |
| Business outcome | Usage-based upgrade and customer engagement recommendations. Input → output: Account usage, approved offers, eligibility → Upgrade recommendation |
| Detailed functionality (workbook) | Compare plan fit; prepare recommendation; avoid automatic charges |
| Blueprint mapping | WF-31 expansion via CPQ; agents AG-066; automations AU-089, AU-042 |
| What V12 adds | Upgrade proposals are priced only by CPQ (DEC-395); V12 adds explicit "no automatic charge" step. |
| Behaviour status | Partially covered → Matched |
| Trigger (V12) | Manual; scheduled monitoring; validated business event; authorized provider webhook when available; Account usage, approved offers, eligibility |
| Trigger kinds (registry, DEC-564) | `manual` (NT13-03); `scheduled` (NT13-02; default cadence per §11.4b, misfire `reschedule_once`); `event` (NT13-01; `sm.svc34.wf04.requested` or upstream domain event, §11.4b.6); `provider_callback` (signed, replay-checked) |
| Authority (V12) | R0 internal analysis/draft; L1 assisted; L3 approved read/draft; Approve source/data rights and applicable external actions; approve consequential communications, commitments and changes; routine steps only within preapproved policies. |
| Blueprint autonomy (DEC-566) | V12 L1 assisted / L3 approved read-draft → blueprint **L0–L1** (drafts and analysis only; no external effect). Approver: R03L |
| Human approval (workbook) | Approve source/data rights and applicable external actions; approve consequential communications, commitments and changes; routine steps only within preapproved policies. |
| Effect boundary | No external effect; internal artifacts only |
| Outputs produced (v3 projection) | `usage_report_ref`, `recommendation_ref` |
| Workflow KPI | plan fit accuracy; unauthorized charge count; baseline and threshold approved in pilot; source service KPI Usage event integrity target ≥99%; unapproved upgrades = 0 |
| Preconditions / failure handling | Common contract (D-F12-030 variant 2, D-F12-031): §11.4b.5 |
| Cost | V12 illustrative ₹0.55/invocation (excludes provider, retry, labour). Blueprint model estimate ₹1.26/run for 1 agent step(s) at Tier 1a (Part 7.3 prices, FX ₹90/USD, verify at time of implementation, as of 27 Nov 2026); Tier 2 not eligible (Confidential/personal data) |
| Usage limit (pilot, not approved) | Illustrative pilot: 200 Account usage review(s)/month; 1 concurrent run; approved caps, provider quotas and hard budget required. |
| Data modalities / version | Text; structured records; service 1.0-target, workflow 1.0-target |
| Acceptance (V12 → blueprint) | SM-SVC-34-WF04-TC-{POS,INPUT,SCOPE,ENT,DUP,QUALITY,BUDGET,RECOVERY} → TC-V12-D-101…108; SM-SVC-34-WF04-AT01 → TC-V12-D-111 |
| Release proposal | A2 |

| Step ID | Action (V12) | V12 executor → node type | Blueprint handler | Output contract | Failure → run state | Model tier | Status |
|---|---|---|---|---|---|---|---|
| SM-SVC-34-WF04-STEP-01 | Compare plan fit | Rules/analytics engine → NT13-07 `logic.compute` | AU-089 registered function | calculation {value,unit,assumptions,evidence_refs} | INVALID_METRIC → HELD | Tier 0 / none | Matched |
| SM-SVC-34-WF04-STEP-02 | prepare recommendation | Domain agent → NT13-08 `ai.task` + NT13-10 `approval.human` | AG-066 via gateway; routed to R03L | candidate {artifact_ref,confidence,reason_codes,review_state} | REVIEW_REQUIRED → AWAITING_APPROVAL | Tier 1b | Matched |
| SM-SVC-34-WF04-STEP-03 | avoid automatic charges | Domain service → NT13-05 `data.write_internal` | `lifecycle.usage` service (revision check) | domain_result {artifact_ref,status,evidence_refs} | INVALID_STATE → HELD | Tier 0 / none | Matched |

### 11.4.5.24 SM-SVC-35 Brand Reputation & Review Intelligence Automation

| Field | Specification |
|---|---|
| Family / objective | Reputation; Detect reputation issues and prepare legitimate responses |
| Channels / providers | Private Admin; approved client data and connectors; Authorized review and brand monitoring sources |
| Optional producers / complementary | Included foundation; no mandatory upstream paid service; optional input producers: SM-SVC-01; SM-SVC-12; SM-SVC-23; authorized equivalent input accepted. |
| Service KPI | Review provenance 100%; fake review generation = 0 |
| Availability / bundle | Full / Digital Marketing & Acquisition / selective (1 SKU); eligible inputs and approvals required. |
| Interoperability / readiness | Optional authorized connector; external agent access disabled unless explicitly granted; Proposed; test and validate customer demand, provider access and economics |
| Open-source stack | Python; Django REST Framework; PostgreSQL; Celery/Beat; Valkey; pgvector if needed; specialist library/provider review pending |
| Blueprint epic / module | EP-11 (ASSUMPTION-826) / `marketing.reputation` |
| Effect adapter | none (human posts responses) |
| Service guardrail | No fake or incentivised reviews; review sources must pass AU-007 source permission. |
| Functional requirement | FR-V12-D-135 (§11.4.5.29 register) |

**DTO `urn:sm:dto:SM-SVC-35-WF0n:v2` (one schema shared by the four workflows; v3 projection per workflow below):**

| Dir | Field | JSON Schema (App. B v2) | V12 validation | Blueprint storage target |
|---|---|---|---|---|
| in | `brand_ref` | string format=uuid | UUID / scoped external reference; input, validate authorized scope | brand kit config (tenant/startup) |
| in | `review_refs` | array maxItems=500 | array (typed references or structured items); input, validate authoriz | intel_review / public review items |
| in | `source_ids` | array maxItems=500 | array (typed references or structured items); input, validate authoriz | intel_source.id[] (ENT-053) |
| in | `threshold_ref` | string format=uuid | UUID / scoped external reference; input, validate authorized scope | alert threshold config |
| out | `review_queue_ref` | string format=uuid | UUID / scoped external reference; output, validate schema and evidence | task queue id |
| out | `response_ref` | string format=uuid | UUID / scoped external reference; output, validate schema and evidence | eng_message_draft.id (ENT-091) |
| out | `incident_ref` | string format=uuid | UUID / scoped external reference; output, validate schema and evidence | gov_compliance_incident.id (ENT-039) |
| out | `improvement_ref` | string format=uuid | UUID / scoped external reference; output, validate schema and evidence | aut_artifact (plan) |

#### SM-SVC-35-WF01 Authorized review and brand reputation monitoring

| Field | Specification |
|---|---|
| V12 sources | BRD ch09 row; FSD ch12 lines 14736–14834; FSD ch13 registry row; App. B `urn:sm:dto:SM-SVC-35-WF01:v2`; workbook row "SM-SVC-35-WF01 — Authorized review and brand reputation monitoring" |
| Business outcome | Authorized review and brand reputation monitoring. Input → output: Permitted sources, brand terms → Review queue |
| Detailed functionality (workbook) | Collect allowed reviews; deduplicate; classify freshness |
| Blueprint mapping | AG-027 permitted public sources; agents AG-027; automations AU-007, AU-014 |
| What V12 adds | New: monitor authorized review sources for the tenant brand (not competitors only). |
| Behaviour status | Not covered → Matched |
| Trigger (V12) | Manual; scheduled monitoring; validated business event; authorized provider webhook when available; Permitted sources, brand terms |
| Trigger kinds (registry, DEC-564) | `manual` (NT13-03); `scheduled` (NT13-02; default cadence per §11.4b, misfire `reschedule_once`); `event` (NT13-01; `sm.svc35.wf01.requested` or upstream domain event, §11.4b.6); `provider_callback` (signed, replay-checked) |
| Authority (V12) | R0 internal analysis/draft; L1 assisted; L3 approved read/draft; Approve source/data rights and applicable external actions; approve consequential communications, commitments and changes; routine steps only within preapproved policies. |
| Blueprint autonomy (DEC-566) | V12 L1 assisted / L3 approved read-draft → blueprint **L0–L1** (drafts and analysis only; no external effect). Approver: R05L |
| Human approval (workbook) | Approve source/data rights and applicable external actions; approve consequential communications, commitments and changes; routine steps only within preapproved policies. |
| Effect boundary | No external effect; internal artifacts only |
| Outputs produced (v3 projection) | `review_queue_ref` |
| Workflow KPI | review dedup; source freshness; baseline and threshold approved in pilot; source service KPI Review provenance 100%; fake review generation = 0 |
| Preconditions / failure handling | Common contract (D-F12-030 variant 2, D-F12-031): §11.4b.5 |
| Cost | V12 illustrative ₹0.55/invocation (excludes provider, retry, labour). Blueprint model estimate ₹0.03/run for 1 agent step(s) at Tier 1a (Part 7.3 prices, FX ₹90/USD, verify at time of implementation, as of 27 Nov 2026); Tier 2 not eligible (Confidential/personal data) |
| Usage limit (pilot, not approved) | Illustrative pilot: 200 Review item(s)/month; 1 concurrent run; approved caps, provider quotas and hard budget required. |
| Data modalities / version | Text; structured records; service 1.0-target, workflow 1.0-target |
| Acceptance (V12 → blueprint) | SM-SVC-35-WF01-TC-{POS,INPUT,SCOPE,ENT,DUP,QUALITY,BUDGET,RECOVERY} → TC-V12-D-101…108; SM-SVC-35-WF01-AT01 → TC-V12-D-111 |
| Release proposal | A2 |

| Step ID | Action (V12) | V12 executor → node type | Blueprint handler | Output contract | Failure → run state | Model tier | Status |
|---|---|---|---|---|---|---|---|
| SM-SVC-35-WF01-STEP-01 | Collect allowed reviews | Evidence/ingestion engine → NT13-04 `data.read` | AU-007 source permission + AU-005 sanitizer, scoped read | evidence_set {items,source_ref,observed_at,hash,rights} | SOURCE_DENIED → HELD | Tier 0 / none | Matched |
| SM-SVC-35-WF01-STEP-02 | deduplicate | Identity/reconciliation engine → NT13-07 `logic.compute` | AU-014 registered function | match_result {matched_refs,unmatched_refs,conflict_refs} | CONFLICT → HELD | Tier 0 / none | Matched |
| SM-SVC-35-WF01-STEP-03 | classify freshness | Domain agent → NT13-08 `ai.task` + NT13-10 `approval.human` | AG-027 via gateway; routed to R05L | candidate {artifact_ref,confidence,reason_codes,review_state} | REVIEW_REQUIRED → AWAITING_APPROVAL | Tier 1a | Matched |

#### SM-SVC-35-WF02 Review classification and evidence-grounded response drafting

| Field | Specification |
|---|---|
| V12 sources | BRD ch09 row; FSD ch12 lines 14835–14933; FSD ch13 registry row; App. B `urn:sm:dto:SM-SVC-35-WF02:v2`; workbook row "SM-SVC-35-WF02 — Review classification and evidence-grounded response drafting" |
| Business outcome | Review classification and evidence-grounded response drafting. Input → output: Review, relevant verified facts, policy → Response draft |
| Detailed functionality (workbook) | Classify issue; draft respectful response; route review |
| Blueprint mapping | AG-014 reply pattern; agents AG-014, AG-012; automations AU-009 |
| What V12 adds | New: classify reviews and draft respectful, evidence-grounded responses; a human posts them. |
| Behaviour status | Not covered → Matched |
| Trigger (V12) | Manual; scheduled monitoring; validated business event; authorized provider webhook when available; Review, relevant verified facts, policy |
| Trigger kinds (registry, DEC-564) | `manual` (NT13-03); `scheduled` (NT13-02; default cadence per §11.4b, misfire `reschedule_once`); `event` (NT13-01; `sm.svc35.wf02.requested` or upstream domain event, §11.4b.6); `provider_callback` (signed, replay-checked) |
| Authority (V12) | R0 internal analysis/draft; L1 assisted; L3 approved read/draft; Approve source/data rights and applicable external actions; approve consequential communications, commitments and changes; routine steps only within preapproved policies. |
| Blueprint autonomy (DEC-566) | V12 L1 assisted / L3 approved read-draft → blueprint **L0–L1** (drafts and analysis only; no external effect). Approver: R05L, R10 |
| Human approval (workbook) | Approve source/data rights and applicable external actions; approve consequential communications, commitments and changes; routine steps only within preapproved policies. |
| Effect boundary | No external effect; internal artifacts only |
| Outputs produced (v3 projection) | `review_queue_ref`, `response_ref` |
| Workflow KPI | issue classification precision; claim accuracy; baseline and threshold approved in pilot; source service KPI Review provenance 100%; fake review generation = 0 |
| Preconditions / failure handling | Common contract (D-F12-030 variant 2, D-F12-031): §11.4b.5 |
| Cost | V12 illustrative ₹1.05/invocation (excludes provider, retry, labour). Blueprint model estimate ₹1.32/run for 3 agent step(s) at Tier 1a (Part 7.3 prices, FX ₹90/USD, verify at time of implementation, as of 27 Nov 2026); Tier 2 not eligible (Confidential/personal data) |
| Usage limit (pilot, not approved) | Illustrative pilot: 200 Review item(s)/month; 1 concurrent run; approved caps, provider quotas and hard budget required. |
| Data modalities / version | Text; structured records; documents; service 1.0-target, workflow 1.0-target |
| Acceptance (V12 → blueprint) | SM-SVC-35-WF02-TC-{POS,INPUT,SCOPE,ENT,DUP,QUALITY,BUDGET,RECOVERY} → TC-V12-D-101…108; SM-SVC-35-WF02-AT01 → TC-V12-D-111 |
| Release proposal | A2 |

| Step ID | Action (V12) | V12 executor → node type | Blueprint handler | Output contract | Failure → run state | Model tier | Status |
|---|---|---|---|---|---|---|---|
| SM-SVC-35-WF02-STEP-01 | Classify issue | Domain agent → NT13-08 `ai.task` + NT13-10 `approval.human` | AG-014 via gateway; routed to R05L | candidate {artifact_ref,confidence,reason_codes,review_state} | REVIEW_REQUIRED → AWAITING_APPROVAL | Tier 1a | Matched |
| SM-SVC-35-WF02-STEP-02 | draft respectful response | Domain agent → NT13-08 `ai.task` + NT13-10 `approval.human` | AG-012 via gateway; routed to R05L | candidate {artifact_ref,confidence,reason_codes,review_state} | REVIEW_REQUIRED → AWAITING_APPROVAL | Tier 1b | Matched |
| SM-SVC-35-WF02-STEP-03 | route review | Domain agent → NT13-08 `ai.task` + NT13-10 `approval.human` | AG-014 via gateway; routed to R05L | candidate {artifact_ref,confidence,reason_codes,review_state} | REVIEW_REQUIRED → AWAITING_APPROVAL | Tier 1a | Matched |

#### SM-SVC-35-WF03 Reputation incident detection and escalation

| Field | Specification |
|---|---|
| V12 sources | BRD ch09 row; FSD ch12 lines 14934–15032; FSD ch13 registry row; App. B `urn:sm:dto:SM-SVC-35-WF03:v2`; workbook row "SM-SVC-35-WF03 — Reputation incident detection and escalation" |
| Business outcome | Reputation incident detection and escalation. Input → output: Review trends, incident thresholds, ownership → Incident alert |
| Detailed functionality (workbook) | Identify credible spikes; verify evidence; escalate |
| Blueprint mapping | AU-031 compliance auto-pause; ops incident; agents AG-027; automations AU-116, AU-031 |
| What V12 adds | New: detect credible review spikes and open a reputation incident. |
| Behaviour status | Not covered → Matched |
| Trigger (V12) | Manual; scheduled monitoring; validated business event; authorized provider webhook when available; Review trends, incident thresholds, ownership |
| Trigger kinds (registry, DEC-564) | `manual` (NT13-03); `scheduled` (NT13-02; default cadence per §11.4b, misfire `reschedule_once`); `event` (NT13-01; `sm.svc35.wf03.requested` or upstream domain event, §11.4b.6); `provider_callback` (signed, replay-checked) |
| Authority (V12) | R1 scoped state write or safety control; L1/L2 review; L3 only for approved deterministic internal actions; Approve source/data rights and applicable external actions; approve consequential communications, commitments and changes; routine steps only within preapproved policies. |
| Blueprint autonomy (DEC-566) | V12 L1/L2 review; L3 only for approved deterministic internal actions → blueprint **L1** for state writes, **L3** only for registered deterministic internal steps (DEC-064). Approver: R05L, R10 |
| Human approval (workbook) | Approve source/data rights and applicable external actions; approve consequential communications, commitments and changes; routine steps only within preapproved policies. |
| Effect boundary | No external effect; internal artifacts only |
| Outputs produced (v3 projection) | `incident_ref` |
| Workflow KPI | incident alert precision; escalation latency; baseline and threshold approved in pilot; source service KPI Review provenance 100%; fake review generation = 0 |
| Preconditions / failure handling | Common contract (D-F12-030 variant 2, D-F12-031): §11.4b.5 |
| Cost | V12 illustrative ₹0.55/invocation (excludes provider, retry, labour). Blueprint model estimate ₹0.03/run for 1 agent step(s) at Tier 1a (Part 7.3 prices, FX ₹90/USD, verify at time of implementation, as of 27 Nov 2026); Tier 2 not eligible (Confidential/personal data) |
| Usage limit (pilot, not approved) | Illustrative pilot: 200 Review item(s)/month; 1 concurrent run; approved caps, provider quotas and hard budget required. |
| Data modalities / version | Text; structured records; service 1.0-target, workflow 1.0-target |
| Acceptance (V12 → blueprint) | SM-SVC-35-WF03-TC-{POS,INPUT,SCOPE,ENT,DUP,QUALITY,BUDGET,RECOVERY} → TC-V12-D-101…108; SM-SVC-35-WF03-AT01 → TC-V12-D-111 |
| Release proposal | A2 |

| Step ID | Action (V12) | V12 executor → node type | Blueprint handler | Output contract | Failure → run state | Model tier | Status |
|---|---|---|---|---|---|---|---|
| SM-SVC-35-WF03-STEP-01 | Identify credible spikes | Domain agent → NT13-08 `ai.task` + NT13-10 `approval.human` | AG-027 via gateway; routed to R05L | candidate {artifact_ref,confidence,reason_codes,review_state} | REVIEW_REQUIRED → AWAITING_APPROVAL | Tier 1a | Matched |
| SM-SVC-35-WF03-STEP-02 | verify evidence | Policy/validation engine → NT13-09 `policy.check` | PDP (AU-009) rule set | validation {passed,reason_codes,policy_version} | POLICY_DENIED → BLOCKED | Tier 0 / none | Matched |
| SM-SVC-35-WF03-STEP-03 | escalate | Domain service → NT13-05 `data.write_internal` | `marketing.reputation` service (revision check) | domain_result {artifact_ref,status,evidence_refs} | INVALID_STATE → HELD | Tier 0 / none | Matched |

#### SM-SVC-35-WF04 Verified feedback trend and reputation improvement planning

| Field | Specification |
|---|---|
| V12 sources | BRD ch09 row; FSD ch12 lines 15033–15131; FSD ch13 registry row; App. B `urn:sm:dto:SM-SVC-35-WF04:v2`; workbook row "SM-SVC-35-WF04 — Verified feedback trend and reputation improvement planning" |
| Business outcome | Verified feedback trend and reputation improvement planning. Input → output: Verified feedback, outcomes, business owners → Improvement plan |
| Detailed functionality (workbook) | Aggregate themes; prioritize improvement; track corrective actions |
| Blueprint mapping | WF-32 VoC loop; agents AG-068; automations AU-102 |
| What V12 adds | Theme synthesis and owned actions exist (WF-32); V12 extends to public reviews. |
| Behaviour status | Partially covered → Matched |
| Trigger (V12) | Manual; scheduled monitoring; validated business event; authorized provider webhook when available; Verified feedback, outcomes, business owners |
| Trigger kinds (registry, DEC-564) | `manual` (NT13-03); `scheduled` (NT13-02; default cadence per §11.4b, misfire `reschedule_once`); `event` (NT13-01; `sm.svc35.wf04.requested` or upstream domain event, §11.4b.6); `provider_callback` (signed, replay-checked) |
| Authority (V12) | R0 internal analysis/draft; L1 assisted; L3 approved read/draft; Approve source/data rights and applicable external actions; approve consequential communications, commitments and changes; routine steps only within preapproved policies. |
| Blueprint autonomy (DEC-566) | V12 L1 assisted / L3 approved read-draft → blueprint **L0–L1** (drafts and analysis only; no external effect). Approver: R05L |
| Human approval (workbook) | Approve source/data rights and applicable external actions; approve consequential communications, commitments and changes; routine steps only within preapproved policies. |
| Effect boundary | No external effect; internal artifacts only |
| Outputs produced (v3 projection) | `improvement_ref` |
| Workflow KPI | theme accuracy; action owner coverage; baseline and threshold approved in pilot; source service KPI Review provenance 100%; fake review generation = 0 |
| Preconditions / failure handling | Common contract (D-F12-030 variant 2, D-F12-031): §11.4b.5 |
| Cost | V12 illustrative ₹0.55/invocation (excludes provider, retry, labour). Blueprint model estimate ₹0.00/run for 0 agent step(s) at Tier 1a (Part 7.3 prices, FX ₹90/USD, verify at time of implementation, as of 27 Nov 2026); Tier 2 not eligible (Confidential/personal data) |
| Usage limit (pilot, not approved) | Illustrative pilot: 200 Review item(s)/month; 1 concurrent run; approved caps, provider quotas and hard budget required. |
| Data modalities / version | Text; structured records; service 1.0-target, workflow 1.0-target |
| Acceptance (V12 → blueprint) | SM-SVC-35-WF04-TC-{POS,INPUT,SCOPE,ENT,DUP,QUALITY,BUDGET,RECOVERY} → TC-V12-D-101…108; SM-SVC-35-WF04-AT01 → TC-V12-D-111 |
| Release proposal | A2 |

| Step ID | Action (V12) | V12 executor → node type | Blueprint handler | Output contract | Failure → run state | Model tier | Status |
|---|---|---|---|---|---|---|---|
| SM-SVC-35-WF04-STEP-01 | Aggregate themes | Rules/analytics engine → NT13-07 `logic.compute` | AU-102 registered function | calculation {value,unit,assumptions,evidence_refs} | INVALID_METRIC → HELD | Tier 0 / none | Matched |
| SM-SVC-35-WF04-STEP-02 | prioritize improvement | Domain service → NT13-05 `data.write_internal` | `marketing.reputation` service (revision check) | domain_result {artifact_ref,status,evidence_refs} | INVALID_STATE → HELD | Tier 0 / none | Matched |
| SM-SVC-35-WF04-STEP-03 | track corrective actions | Domain service → NT13-05 `data.write_internal` | `marketing.reputation` service (revision check) | domain_result {artifact_ref,status,evidence_refs} | INVALID_STATE → HELD | Tier 0 / none | Matched |

### 11.4.5.25 SM-SVC-36 AI Sales Enablement & Coaching Automation

| Field | Specification |
|---|---|
| Family / objective | Sales enablement; Improve sales knowledge and practice |
| Channels / providers | Private Admin; approved client data and connectors; Approved training materials and permitted meeting data |
| Optional producers / complementary | Included foundation; no mandatory upstream paid service; optional input producers: SM-SVC-09; SM-SVC-10; SM-SVC-17; SM-SVC-25; authorized equivalent input accepted. |
| Service KPI | Rubric and permission checks 100%; no automated employment decision |
| Availability / bundle | Full / Lifecycle & Business Intelligence / selective (1 SKU); eligible inputs and approvals required. |
| Interoperability / readiness | Optional authorized connector; external agent access disabled unless explicitly granted; Proposed; test and validate customer demand, provider access and economics |
| Open-source stack | Python; Django REST Framework; PostgreSQL; Celery/Beat; Valkey; pgvector if needed; specialist library/provider review pending |
| Blueprint epic / module | EP-21 (ASSUMPTION-826) / `enablement.coaching` |
| Effect adapter | none |
| Service guardrail | DEC-386: AI outputs never evaluate employees; coaching results are private to the learner. |
| Functional requirement | FR-V12-D-136 (§11.4.5.29 register) |

**DTO `urn:sm:dto:SM-SVC-36-WF0n:v2` (one schema shared by the four workflows; v3 projection per workflow below):**

| Dir | Field | JSON Schema (App. B v2) | V12 validation | Blueprint storage target |
|---|---|---|---|---|
| in | `learner_ref` | string format=uuid | UUID / scoped external reference; input, validate authorized scope | staff user id |
| in | `playbook_ref` | string format=uuid | UUID / scoped external reference; input, validate authorized scope | mkt_content_asset (playbook) |
| in | `scenario_ref` | string format=uuid | UUID / scoped external reference; input, validate authorized scope | practice scenario / pricing scenario artifact |
| in | `authorized_session_ref` | string format=uuid | UUID / scoped external reference; input, validate authorized scope | consent-checked session id (written notes only, DEC-386) |
| out | `playbook_revision` | integer minimum=1 | positive integer (monotonic revision); output, validate schema and evi | integer ≥ 1 |
| out | `practice_report_ref` | string format=uuid | UUID / scoped external reference; output, validate schema and evidence | aut_artifact (learner-private) |
| out | `feedback_ref` | string format=uuid | UUID / scoped external reference; output, validate schema and evidence | aut_artifact (learner-private) |
| out | `training_plan_ref` | string format=uuid | UUID / scoped external reference; output, validate schema and evidence | aut_artifact (learner-private) |

#### SM-SVC-36-WF01 Sales knowledge and product playbook generation

| Field | Specification |
|---|---|
| V12 sources | BRD ch09 row; FSD ch12 lines 15133–15231; FSD ch13 registry row; App. B `urn:sm:dto:SM-SVC-36-WF01:v2`; workbook row "SM-SVC-36-WF01 — Sales knowledge and product playbook generation" |
| Business outcome | Sales knowledge and product playbook generation. Input → output: Approved product facts, sales policies → Playbook |
| Detailed functionality (workbook) | Generate playbook; cite sources; verify claims |
| Blueprint mapping | AG-070 enablement coach (Part 9.8b); agents AG-070; automations AU-083, AU-009 |
| What V12 adds | Playbook recommendations exist (AG-070); V12 adds generation with citations and claim verification. |
| Behaviour status | Partially covered → Matched |
| Trigger (V12) | Manual; scheduled monitoring; validated business event; authorized provider webhook when available; Approved product facts, sales policies |
| Trigger kinds (registry, DEC-564) | `manual` (NT13-03); `scheduled` (NT13-02; default cadence per §11.4b, misfire `reschedule_once`); `event` (NT13-01; `sm.svc36.wf01.requested` or upstream domain event, §11.4b.6); `provider_callback` (signed, replay-checked) |
| Authority (V12) | R0 internal analysis/draft; L1 assisted; L3 approved read/draft; Approve source/data rights and applicable external actions; review recordings and training outputs; no automated employment decisions. |
| Blueprint autonomy (DEC-566) | V12 L1 assisted / L3 approved read-draft → blueprint **L0–L1** (drafts and analysis only; no external effect). Approver: R10, R03 |
| Human approval (workbook) | Approve source/data rights and applicable external actions; review recordings and training outputs; no automated employment decisions. |
| Effect boundary | No external effect; internal artifacts only |
| Outputs produced (v3 projection) | `playbook_revision` |
| Workflow KPI | claim evidence coverage; playbook accuracy; baseline and threshold approved in pilot; source service KPI Rubric and permission checks 100%; no automated employment decision |
| Preconditions / failure handling | Common contract (D-F12-030 variant 2, D-F12-031): §11.4b.5 |
| Cost | V12 illustrative ₹1.05/invocation (excludes provider, retry, labour). Blueprint model estimate ₹1.26/run for 1 agent step(s) at Tier 1b (Part 7.3 prices, FX ₹90/USD, verify at time of implementation, as of 27 Nov 2026); Tier 2 not eligible (Confidential/personal data) |
| Usage limit (pilot, not approved) | Illustrative pilot: 100 Coaching session(s)/month; 1 concurrent run; approved caps, provider quotas and hard budget required. |
| Data modalities / version | Text; structured records; service 1.0-target, workflow 1.0-target |
| Acceptance (V12 → blueprint) | SM-SVC-36-WF01-TC-{POS,INPUT,SCOPE,ENT,DUP,QUALITY,BUDGET,RECOVERY} → TC-V12-D-101…108; SM-SVC-36-WF01-AT01 → TC-V12-D-111 |
| Release proposal | A1 |

| Step ID | Action (V12) | V12 executor → node type | Blueprint handler | Output contract | Failure → run state | Model tier | Status |
|---|---|---|---|---|---|---|---|
| SM-SVC-36-WF01-STEP-01 | Generate playbook | Domain agent → NT13-08 `ai.task` + NT13-10 `approval.human` | AG-070 via gateway; routed to R10 | candidate {artifact_ref,confidence,reason_codes,review_state} | REVIEW_REQUIRED → AWAITING_APPROVAL | Tier 1b | Matched |
| SM-SVC-36-WF01-STEP-02 | cite sources | Domain service → NT13-05 `data.write_internal` | `enablement.coaching` service (revision check) | domain_result {artifact_ref,status,evidence_refs} | INVALID_STATE → HELD | Tier 0 / none | Matched |
| SM-SVC-36-WF01-STEP-03 | verify claims | Policy/validation engine → NT13-09 `policy.check` | PDP (AU-009) rule set | validation {passed,reason_codes,policy_version} | POLICY_DENIED → BLOCKED | Tier 0 / none | Matched |

#### SM-SVC-36-WF02 Simulated customer objection and negotiation training

| Field | Specification |
|---|---|
| V12 sources | BRD ch09 row; FSD ch12 lines 15232–15330; FSD ch13 registry row; App. B `urn:sm:dto:SM-SVC-36-WF02:v2`; workbook row "SM-SVC-36-WF02 — Simulated customer objection and negotiation training" |
| Business outcome | Simulated customer objection and negotiation training. Input → output: Scenario brief, approved negotiation rules → Practice report |
| Detailed functionality (workbook) | Simulate conversation; assess against rubric; provide feedback |
| Blueprint mapping | AG-046 objection-handling coach (Part 9.7b); agents AG-046; automations AU-083 |
| What V12 adds | Practice against synthetic personas exists (AG-046); V12 adds rubric assessment and feedback step IDs. |
| Behaviour status | Partially covered → Matched |
| Trigger (V12) | Manual; scheduled monitoring; validated business event; authorized provider webhook when available; Scenario brief, approved negotiation rules |
| Trigger kinds (registry, DEC-564) | `manual` (NT13-03); `scheduled` (NT13-02; default cadence per §11.4b, misfire `reschedule_once`); `event` (NT13-01; `sm.svc36.wf02.requested` or upstream domain event, §11.4b.6); `provider_callback` (signed, replay-checked) |
| Authority (V12) | R0 internal analysis/draft; L1 assisted; L3 approved read/draft; Approve source/data rights and applicable external actions; review recordings and training outputs; no automated employment decisions. |
| Blueprint autonomy (DEC-566) | V12 L1 assisted / L3 approved read-draft → blueprint **L0–L1** (drafts and analysis only; no external effect). Approver: R03 |
| Human approval (workbook) | Approve source/data rights and applicable external actions; review recordings and training outputs; no automated employment decisions. |
| Effect boundary | No external effect; internal artifacts only |
| Outputs produced (v3 projection) | `practice_report_ref`, `feedback_ref`, `training_plan_ref` |
| Workflow KPI | rubric agreement; feedback specificity; baseline and threshold approved in pilot; source service KPI Rubric and permission checks 100%; no automated employment decision |
| Preconditions / failure handling | Common contract (D-F12-030 variant 2, D-F12-031): §11.4b.5 |
| Cost | V12 illustrative ₹0.55/invocation (excludes provider, retry, labour). Blueprint model estimate ₹0.00/run for 0 agent step(s) at Tier 1b (Part 7.3 prices, FX ₹90/USD, verify at time of implementation, as of 27 Nov 2026); Tier 2 not eligible (Confidential/personal data) |
| Usage limit (pilot, not approved) | Illustrative pilot: 100 Coaching session(s)/month; 1 concurrent run; approved caps, provider quotas and hard budget required. |
| Data modalities / version | Text; structured records; service 1.0-target, workflow 1.0-target |
| Acceptance (V12 → blueprint) | SM-SVC-36-WF02-TC-{POS,INPUT,SCOPE,ENT,DUP,QUALITY,BUDGET,RECOVERY} → TC-V12-D-101…108; SM-SVC-36-WF02-AT01 → TC-V12-D-111 |
| Release proposal | A1 |

| Step ID | Action (V12) | V12 executor → node type | Blueprint handler | Output contract | Failure → run state | Model tier | Status |
|---|---|---|---|---|---|---|---|
| SM-SVC-36-WF02-STEP-01 | Simulate conversation | Domain service → NT13-05 `data.write_internal` | `enablement.coaching` service (revision check) | domain_result {artifact_ref,status,evidence_refs} | INVALID_STATE → HELD | Tier 0 / none | Matched |
| SM-SVC-36-WF02-STEP-02 | assess against rubric | Domain service → NT13-05 `data.write_internal` | `enablement.coaching` service (revision check) | domain_result {artifact_ref,status,evidence_refs} | INVALID_STATE → HELD | Tier 0 / none | Matched |
| SM-SVC-36-WF02-STEP-03 | provide feedback | Domain service → NT13-05 `data.write_internal` | `enablement.coaching` service (revision check) | domain_result {artifact_ref,status,evidence_refs} | INVALID_STATE → HELD | Tier 0 / none | Matched |

#### SM-SVC-36-WF03 Permitted sales meeting and conversation coaching

| Field | Specification |
|---|---|
| V12 sources | BRD ch09 row; FSD ch12 lines 15331–15429; FSD ch13 registry row; App. B `urn:sm:dto:SM-SVC-36-WF03:v2`; workbook row "SM-SVC-36-WF03 — Permitted sales meeting and conversation coaching" |
| Business outcome | Permitted sales meeting and conversation coaching. Input → output: Authorized recording/notes, coaching rubric → Coaching feedback |
| Detailed functionality (workbook) | Extract observable behaviors; offer coaching; protect privacy |
| Blueprint mapping | AG-045 conversation intelligence, written only (DEC-386); agents AG-045; automations AU-004 |
| What V12 adds | Coaching on recordings conflicts with DEC-218/DEC-386; written notes are allowed. |
| Behaviour status | Conflict → Pending Founder decision (CONFLICT-818) |
| Trigger (V12) | Manual; scheduled monitoring; validated business event; authorized provider webhook when available; Authorized recording/notes, coaching rubric |
| Trigger kinds (registry, DEC-564) | `manual` (NT13-03); `scheduled` (NT13-02; default cadence per §11.4b, misfire `reschedule_once`); `event` (NT13-01; `sm.svc36.wf03.requested` or upstream domain event, §11.4b.6); `provider_callback` (signed, replay-checked) |
| Authority (V12) | R0 internal analysis/draft; L1 assisted; L3 approved read/draft; Approve source/data rights and applicable external actions; review recordings and training outputs; no automated employment decisions. |
| Blueprint autonomy (DEC-566) | V12 L1 assisted / L3 approved read-draft → blueprint **L0–L1** (drafts and analysis only; no external effect). Approver: R10, R01 |
| Human approval (workbook) | Approve source/data rights and applicable external actions; review recordings and training outputs; no automated employment decisions. |
| Effect boundary | No external effect; internal artifacts only |
| Outputs produced (v3 projection) | `feedback_ref` |
| Workflow KPI | observable behavior accuracy; privacy compliance; baseline and threshold approved in pilot; source service KPI Rubric and permission checks 100%; no automated employment decision |
| Preconditions / failure handling | Common contract (D-F12-030 variant 2, D-F12-031): §11.4b.5 |
| Cost | V12 illustrative ₹0.55/invocation (excludes provider, retry, labour). Blueprint model estimate ₹0.00/run for 0 agent step(s) at Tier 1b (Part 7.3 prices, FX ₹90/USD, verify at time of implementation, as of 27 Nov 2026); Tier 2 not eligible (Confidential/personal data) |
| Usage limit (pilot, not approved) | Illustrative pilot: 100 Coaching session(s)/month; 1 concurrent run; approved caps, provider quotas and hard budget required. |
| Data modalities / version | Text; structured records; audio/image/video where applicable and authorized; service 1.0-target, workflow 1.0-target |
| Acceptance (V12 → blueprint) | SM-SVC-36-WF03-TC-{POS,INPUT,SCOPE,ENT,DUP,QUALITY,BUDGET,RECOVERY} → TC-V12-D-101…108; SM-SVC-36-WF03-AT01 → TC-V12-D-111 |
| Release proposal | Written-notes path A1; recordings Spec only |

| Step ID | Action (V12) | V12 executor → node type | Blueprint handler | Output contract | Failure → run state | Model tier | Status |
|---|---|---|---|---|---|---|---|
| SM-SVC-36-WF03-STEP-01 | Extract observable behaviors | Evidence/ingestion engine → NT13-04 `data.read` | AU-007 source permission + AU-005 sanitizer, scoped read | evidence_set {items,source_ref,observed_at,hash,rights} | SOURCE_DENIED → HELD | Tier 0 / none | Pending Founder decision |
| SM-SVC-36-WF03-STEP-02 | offer coaching | Domain service → NT13-05 `data.write_internal` | `enablement.coaching` service (revision check) | domain_result {artifact_ref,status,evidence_refs} | INVALID_STATE → HELD | Tier 0 / none | Matched |
| SM-SVC-36-WF03-STEP-03 | protect privacy | Domain service → NT13-05 `data.write_internal` | `enablement.coaching` service (revision check) | domain_result {artifact_ref,status,evidence_refs} | INVALID_STATE → HELD | Tier 0 / none | Matched |

#### SM-SVC-36-WF04 Sales capability-gap and training recommendation generation

| Field | Specification |
|---|---|
| V12 sources | BRD ch09 row; FSD ch12 lines 15430–15528; FSD ch13 registry row; App. B `urn:sm:dto:SM-SVC-36-WF04:v2`; workbook row "SM-SVC-36-WF04 — Sales capability-gap and training recommendation generation" |
| Business outcome | Sales capability-gap and training recommendation generation. Input → output: Training outcomes, role requirements → Training plan |
| Detailed functionality (workbook) | Identify learning gaps; recommend exercises; avoid employment decisions |
| Blueprint mapping | AG-070; DEC-386; agents AG-070; automations AU-083 |
| What V12 adds | Learning-gap recommendations are private to the learner; no employment decision (DEC-386). |
| Behaviour status | Partially covered → Matched |
| Trigger (V12) | Manual; scheduled monitoring; validated business event; authorized provider webhook when available; Training outcomes, role requirements |
| Trigger kinds (registry, DEC-564) | `manual` (NT13-03); `scheduled` (NT13-02; default cadence per §11.4b, misfire `reschedule_once`); `event` (NT13-01; `sm.svc36.wf04.requested` or upstream domain event, §11.4b.6); `provider_callback` (signed, replay-checked) |
| Authority (V12) | R0 internal analysis/draft; L1 assisted; L3 approved read/draft; Approve source/data rights and applicable external actions; review recordings and training outputs; no automated employment decisions. |
| Blueprint autonomy (DEC-566) | V12 L1 assisted / L3 approved read-draft → blueprint **L0–L1** (drafts and analysis only; no external effect). Approver: R03 (learner-private) |
| Human approval (workbook) | Approve source/data rights and applicable external actions; review recordings and training outputs; no automated employment decisions. |
| Effect boundary | No external effect; internal artifacts only |
| Outputs produced (v3 projection) | `training_plan_ref` |
| Workflow KPI | learning-gap precision; exercise alignment; baseline and threshold approved in pilot; source service KPI Rubric and permission checks 100%; no automated employment decision |
| Preconditions / failure handling | Common contract (D-F12-030 variant 2, D-F12-031): §11.4b.5 |
| Cost | V12 illustrative ₹1.05/invocation (excludes provider, retry, labour). Blueprint model estimate ₹2.52/run for 2 agent step(s) at Tier 1b (Part 7.3 prices, FX ₹90/USD, verify at time of implementation, as of 27 Nov 2026); Tier 2 not eligible (Confidential/personal data) |
| Usage limit (pilot, not approved) | Illustrative pilot: 100 Coaching session(s)/month; 1 concurrent run; approved caps, provider quotas and hard budget required. |
| Data modalities / version | Text; structured records; service 1.0-target, workflow 1.0-target |
| Acceptance (V12 → blueprint) | SM-SVC-36-WF04-TC-{POS,INPUT,SCOPE,ENT,DUP,QUALITY,BUDGET,RECOVERY} → TC-V12-D-101…108; SM-SVC-36-WF04-AT01 → TC-V12-D-111 |
| Release proposal | A1 |

| Step ID | Action (V12) | V12 executor → node type | Blueprint handler | Output contract | Failure → run state | Model tier | Status |
|---|---|---|---|---|---|---|---|
| SM-SVC-36-WF04-STEP-01 | Identify learning gaps | Domain agent → NT13-08 `ai.task` + NT13-10 `approval.human` | AG-070 via gateway; routed to R03 (learner-private) | candidate {artifact_ref,confidence,reason_codes,review_state} | REVIEW_REQUIRED → AWAITING_APPROVAL | Tier 1b | Matched |
| SM-SVC-36-WF04-STEP-02 | recommend exercises | Domain agent → NT13-08 `ai.task` + NT13-10 `approval.human` | AG-070 via gateway; routed to R03 (learner-private) | candidate {artifact_ref,confidence,reason_codes,review_state} | REVIEW_REQUIRED → AWAITING_APPROVAL | Tier 1b | Matched |
| SM-SVC-36-WF04-STEP-03 | avoid employment decisions | Domain service → NT13-05 `data.write_internal` | `enablement.coaching` service (revision check) | domain_result {artifact_ref,status,evidence_refs} | INVALID_STATE → HELD | Tier 0 / none | Matched |

### 11.4.5.26 SM-SVC-37 Pricing, Offer & Revenue Optimization Automation

| Field | Specification |
|---|---|
| Family / objective | Pricing intelligence; Improve pricing and margin decisions within approved policy |
| Channels / providers | Private Admin; approved client data and connectors; Authorized financial, pricing and demand data; approved experiment policy |
| Optional producers / complementary | Included foundation; no mandatory upstream paid service; optional input producers: SM-SVC-14; SM-SVC-17; SM-SVC-24; authorized equivalent input accepted. |
| Service KPI | Price/margin calculations reconcile 100%; unapproved changes = 0 |
| Availability / bundle | Full / Sales Conversion & Operations / selective (1 SKU); eligible inputs and approvals required. |
| Interoperability / readiness | Optional authorized connector; external agent access disabled unless explicitly granted; Provider, jurisdiction and specialist approval required before live operation |
| Open-source stack | Python; Django REST Framework; PostgreSQL; Celery/Beat; Valkey; pgvector if needed; specialist library/provider review pending |
| Blueprint epic / module | EP-13 (ASSUMPTION-826) / `commerce.pricing_analytics` |
| Effect adapter | none |
| Service guardrail | DEC-388 / DEC-395 / CI-071: AI never proposes, computes or changes a price; only deterministic analytics are allowed. |
| Functional requirement | FR-V12-D-137 (§11.4.5.29 register) |

**DTO `urn:sm:dto:SM-SVC-37-WF0n:v2` (one schema shared by the four workflows; v3 projection per workflow below):**

| Dir | Field | JSON Schema (App. B v2) | V12 validation | Blueprint storage target |
|---|---|---|---|---|
| in | `offer_ref` | string format=uuid | UUID / scoped external reference; input, validate authorized scope | cat_offering / bundle id |
| in | `cost_revision_ref` | string format=uuid | UUID / scoped external reference; input, validate authorized scope | cost revision register |
| in | `price_bounds_ref` | string format=uuid | UUID / scoped external reference; input, validate authorized scope | cat_price_version.id (ENT-021) |
| in | `history_refs` | array maxItems=500 | array (typed references or structured items); input, validate authoriz | quote/order history ids |
| out | `margin_minor` | integer minimum=0 | int64, nonnegative except signed ledger deltas; output, validate schem | numeric(18,4) ↔ int64 minor (AU-049) |
| out | `scenario_ref` | string format=uuid | UUID / scoped external reference; output, validate schema and evidence | practice scenario / pricing scenario artifact |
| out | `experiment_ref` | string format=uuid | UUID / scoped external reference; output, validate schema and evidence | experiment registry id |
| out | `exception_ref` | string format=uuid | UUID / scoped external reference; output, validate schema and evidence | aut_artifact (exception) |

#### SM-SVC-37-WF01 Pricing and product bundle profitability analysis

| Field | Specification |
|---|---|
| V12 sources | BRD ch09 row; FSD ch12 lines 15530–15628; FSD ch13 registry row; App. B `urn:sm:dto:SM-SVC-37-WF01:v2`; workbook row "SM-SVC-37-WF01 — Pricing and product bundle profitability analysis" |
| Business outcome | Pricing and product bundle profitability analysis. Input → output: Approved costs, prices, bundle components → Profitability report |
| Detailed functionality (workbook) | Calculate margin; compare bundle scenarios; flag low margin |
| Blueprint mapping | AU-049 contribution margin; AU-089 CPQ; agents none (deterministic only); automations AU-049, AU-089 |
| What V12 adds | Margin calculation exists (AU-049); V12 adds bundle scenario comparison and low-margin flags, all deterministic. |
| Behaviour status | Partially covered → Matched |
| Trigger (V12) | Manual; scheduled monitoring; validated business event; authorized provider webhook when available; Approved costs, prices, bundle components |
| Trigger kinds (registry, DEC-564) | `manual` (NT13-03); `scheduled` (NT13-02; default cadence per §11.4b, misfire `reschedule_once`); `event` (NT13-01; `sm.svc37.wf01.requested` or upstream domain event, §11.4b.6); `provider_callback` (signed, replay-checked) |
| Authority (V12) | R0 internal analysis/draft; L1 assisted; L3 approved read/draft; Approve source/data rights and applicable external actions; approve experimental bounds, customer fairness, budget, pricing and publication before any live change. |
| Blueprint autonomy (DEC-566) | V12 L1 assisted / L3 approved read-draft → blueprint **L0–L1** (drafts and analysis only; no external effect). Approver: R08, R02 |
| Human approval (workbook) | Approve source/data rights and applicable external actions; approve experimental bounds, customer fairness, budget, pricing and publication before any live change. |
| Effect boundary | No external effect; internal artifacts only |
| Outputs produced (v3 projection) | `margin_minor`, `scenario_ref` |
| Workflow KPI | margin calculation accuracy; low margin detection; baseline and threshold approved in pilot; source service KPI Price/margin calculations reconcile 100%; unapproved changes = 0 |
| Preconditions / failure handling | Common contract (D-F12-030 variant 2, D-F12-031): §11.4b.5 |
| Cost | V12 illustrative ₹1.05/invocation (excludes provider, retry, labour). Blueprint model estimate ₹0.00/run for 0 agent step(s) at Tier 0 (Part 7.3 prices, FX ₹90/USD, verify at time of implementation, as of 27 Nov 2026); Tier 2 not eligible (Confidential/personal data) |
| Usage limit (pilot, not approved) | Illustrative pilot: 50 Pricing scenario(s)/month; 1 concurrent run; approved caps, provider quotas and hard budget required. |
| Data modalities / version | Text; structured records; service 1.0-target, workflow 1.0-target |
| Acceptance (V12 → blueprint) | SM-SVC-37-WF01-TC-{POS,INPUT,SCOPE,ENT,DUP,QUALITY,BUDGET,RECOVERY} → TC-V12-D-101…108; SM-SVC-37-WF01-AT01 → TC-V12-D-111 |
| Release proposal | A2 |

| Step ID | Action (V12) | V12 executor → node type | Blueprint handler | Output contract | Failure → run state | Model tier | Status |
|---|---|---|---|---|---|---|---|
| SM-SVC-37-WF01-STEP-01 | Calculate margin | Rules/analytics engine → NT13-07 `logic.compute` | AU-049 registered function | calculation {value,unit,assumptions,evidence_refs} | INVALID_METRIC → HELD | Tier 0 / none | Matched |
| SM-SVC-37-WF01-STEP-02 | compare bundle scenarios | Rules/analytics engine → NT13-07 `logic.compute` | AU-049 registered function | calculation {value,unit,assumptions,evidence_refs} | INVALID_METRIC → HELD | Tier 0 / none | Matched |
| SM-SVC-37-WF01-STEP-03 | flag low margin | Domain agent → NT13-08 `ai.task` + NT13-10 `approval.human` | Deterministic flag rule + NT13-11 `task.human` (no model call) | candidate {artifact_ref,confidence,reason_codes,review_state} | REVIEW_REQUIRED → AWAITING_APPROVAL | Tier 0 / none | Matched |

#### SM-SVC-37-WF02 Demand, margin and price sensitivity scenario modelling

| Field | Specification |
|---|---|
| V12 sources | BRD ch09 row; FSD ch12 lines 15629–15721; FSD ch13 registry row; App. B `urn:sm:dto:SM-SVC-37-WF02:v2`; workbook row "SM-SVC-37-WF02 — Demand, margin and price sensitivity scenario modelling" |
| Business outcome | Demand, margin and price sensitivity scenario modelling. Input → output: Demand history, price assumptions, costs → Scenario report |
| Detailed functionality (workbook) | Estimate sensitivity with uncertainty; compare scenarios |
| Blueprint mapping | none (CI-071); agents none (deterministic only); automations AU-049 |
| What V12 adds | Price-sensitivity scenarios move toward price recommendation (CI-071, DEC-388). |
| Behaviour status | Conflict → Pending Founder decision (CONFLICT-817) |
| Trigger (V12) | Manual; scheduled monitoring; validated business event; authorized provider webhook when available; Demand history, price assumptions, costs |
| Trigger kinds (registry, DEC-564) | `manual` (NT13-03); `scheduled` (NT13-02; default cadence per §11.4b, misfire `reschedule_once`); `event` (NT13-01; `sm.svc37.wf02.requested` or upstream domain event, §11.4b.6); `provider_callback` (signed, replay-checked) |
| Authority (V12) | R0 internal analysis/draft; L1 assisted; L3 approved read/draft; Approve source/data rights and applicable external actions; approve experimental bounds, customer fairness, budget, pricing and publication before any live change. |
| Blueprint autonomy (DEC-566) | V12 L1 assisted / L3 approved read-draft → blueprint **L0–L1** (drafts and analysis only; no external effect). Approver: R08, R02, R01 |
| Human approval (workbook) | Approve source/data rights and applicable external actions; approve experimental bounds, customer fairness, budget, pricing and publication before any live change. |
| Effect boundary | No external effect; internal artifacts only |
| Outputs produced (v3 projection) | `margin_minor`, `scenario_ref` |
| Workflow KPI | sensitivity uncertainty coverage; assumption traceability; baseline and threshold approved in pilot; source service KPI Price/margin calculations reconcile 100%; unapproved changes = 0 |
| Preconditions / failure handling | Common contract (D-F12-030 variant 2, D-F12-031): §11.4b.5 |
| Cost | V12 illustrative ₹1.05/invocation (excludes provider, retry, labour). Blueprint model estimate ₹0.00/run for 0 agent step(s) at Tier 0 (Part 7.3 prices, FX ₹90/USD, verify at time of implementation, as of 27 Nov 2026); Tier 2 not eligible (Confidential/personal data) |
| Usage limit (pilot, not approved) | Illustrative pilot: 50 Pricing scenario(s)/month; 1 concurrent run; approved caps, provider quotas and hard budget required. |
| Data modalities / version | Text; structured records; service 1.0-target, workflow 1.0-target |
| Acceptance (V12 → blueprint) | SM-SVC-37-WF02-TC-{POS,INPUT,SCOPE,ENT,DUP,QUALITY,BUDGET,RECOVERY} → TC-V12-D-101…108; SM-SVC-37-WF02-AT01 → TC-V12-D-111 |
| Release proposal | Spec only (Founder) |

| Step ID | Action (V12) | V12 executor → node type | Blueprint handler | Output contract | Failure → run state | Model tier | Status |
|---|---|---|---|---|---|---|---|
| SM-SVC-37-WF02-STEP-01 | Estimate sensitivity with uncertainty | Rules/analytics engine → NT13-07 `logic.compute` | AU-049 registered function | calculation {value,unit,assumptions,evidence_refs} | INVALID_METRIC → HELD | Tier 0 / none | Pending Founder decision |
| SM-SVC-37-WF02-STEP-02 | compare scenarios | Rules/analytics engine → NT13-07 `logic.compute` | AU-049 registered function | calculation {value,unit,assumptions,evidence_refs} | INVALID_METRIC → HELD | Tier 0 / none | Pending Founder decision |

#### SM-SVC-37-WF03 Approved pricing and promotion experimentation

| Field | Specification |
|---|---|
| V12 sources | BRD ch09 row; FSD ch12 lines 15722–15820; FSD ch13 registry row; App. B `urn:sm:dto:SM-SVC-37-WF03:v2`; workbook row "SM-SVC-37-WF03 — Approved pricing and promotion experimentation" |
| Business outcome | Approved pricing and promotion experimentation. Input → output: Approved price bounds, eligible variants and sample plan → Pricing experiment result |
| Detailed functionality (workbook) | Simulate or run approved experiment; enforce limits; measure outcomes |
| Blueprint mapping | WF-20 experiments; agents none (deterministic only); automations AU-098, AU-065, AU-089 |
| What V12 adds | Live pricing experiments change prices customers see (DEC-064, DEC-395). |
| Behaviour status | Conflict → Pending Founder decision (CONFLICT-817) |
| Trigger (V12) | Manual; scheduled monitoring; validated business event; authorized provider webhook when available; Approved price bounds, eligible variants and sample plan |
| Trigger kinds (registry, DEC-564) | `manual` (NT13-03); `scheduled` (NT13-02; default cadence per §11.4b, misfire `reschedule_once`); `event` (NT13-01; `sm.svc37.wf03.requested` or upstream domain event, §11.4b.6); `provider_callback` (signed, replay-checked) |
| Authority (V12) | R3 financial/legal/commitment; L2 mandatory approved effect; L3 only with separately approved bounded mandate where lawful; Approve source/data rights and applicable external actions; approve experimental bounds, customer fairness, budget, pricing and publication before any live change. |
| Blueprint autonomy (DEC-566) | V12 L2 default → blueprint **L1 maximum** (human approval bound to the exact hash; money movement not supported, DEC-064). V12 "L3 bounded mandate" **not adopted** (CONFLICT-814, Pending Founder decision). Approver: R08, R02, R01 |
| Human approval (workbook) | Approve source/data rights and applicable external actions; approve experimental bounds, customer fairness, budget, pricing and publication before any live change. |
| Effect boundary | No external effect; approval gate inserted before state change (DEC-570) |
| Outputs produced (v3 projection) | `experiment_ref` |
| Workflow KPI | price guardrail compliance; assignment validity; baseline and threshold approved in pilot; source service KPI Price/margin calculations reconcile 100%; unapproved changes = 0 |
| Preconditions / failure handling | Common contract (D-F12-030 variant 2, D-F12-031): §11.4b.5 |
| Cost | V12 illustrative ₹0.55/invocation (excludes provider, retry, labour). Blueprint model estimate ₹0.00/run for 0 agent step(s) at Tier 0 (Part 7.3 prices, FX ₹90/USD, verify at time of implementation, as of 27 Nov 2026); Tier 2 not eligible (Confidential/personal data) |
| Usage limit (pilot, not approved) | Illustrative pilot: 50 Pricing scenario(s)/month; 1 concurrent run; approved caps, provider quotas and hard budget required. |
| Data modalities / version | Text; structured records; service 1.0-target, workflow 1.0-target |
| Acceptance (V12 → blueprint) | SM-SVC-37-WF03-TC-{POS,INPUT,SCOPE,ENT,DUP,QUALITY,BUDGET,RECOVERY,APPROVAL,EFFECT} → TC-V12-D-101…110; SM-SVC-37-WF03-AT01 → TC-V12-D-111 |
| Release proposal | Spec only (Founder) |

| Step ID | Action (V12) | V12 executor → node type | Blueprint handler | Output contract | Failure → run state | Model tier | Status |
|---|---|---|---|---|---|---|---|
| SM-SVC-37-WF03-STEP-01 | Simulate or run approved experiment | Domain service → NT13-05 `data.write_internal` | `commerce.pricing_analytics` service (revision check) | domain_result {artifact_ref,status,evidence_refs} | INVALID_STATE → HELD | Tier 0 / none | Pending Founder decision |
| SM-SVC-37-WF03-STEP-02 | enforce limits | Policy/validation engine → NT13-09 `policy.check` | PDP (AU-009) rule set + AU-089 | validation {passed,reason_codes,policy_version} | POLICY_DENIED → BLOCKED | Tier 0 / none | Pending Founder decision |
| SM-SVC-37-WF03-STEP-03 | measure outcomes | Rules/analytics engine → NT13-07 `logic.compute` | AU-098 registered function | calculation {value,unit,assumptions,evidence_refs} | INVALID_METRIC → HELD | Tier 0 / none | Pending Founder decision |

#### SM-SVC-37-WF04 Margin anomaly and commercial pricing-policy monitoring

| Field | Specification |
|---|---|
| V12 sources | BRD ch09 row; FSD ch12 lines 15821–15913; FSD ch13 registry row; App. B `urn:sm:dto:SM-SVC-37-WF04:v2`; workbook row "SM-SVC-37-WF04 — Margin anomaly and commercial pricing-policy monitoring" |
| Business outcome | Margin anomaly and commercial pricing-policy monitoring. Input → output: Actual sales, approved price rules, costs → Pricing exception report |
| Detailed functionality (workbook) | Detect price/margin deviation; flag and route approval |
| Blueprint mapping | AU-089 CPQ guardrails; AU-116 anomalies; agents AG-066; automations AU-089, AU-116 |
| What V12 adds | Guardrail evaluation exists; V12 adds monitoring of realised price and margin deviation. |
| Behaviour status | Partially covered → Matched |
| Trigger (V12) | Manual; scheduled monitoring; validated business event; authorized provider webhook when available; Actual sales, approved price rules, costs |
| Trigger kinds (registry, DEC-564) | `manual` (NT13-03); `scheduled` (NT13-02; default cadence per §11.4b, misfire `reschedule_once`); `event` (NT13-01; `sm.svc37.wf04.requested` or upstream domain event, §11.4b.6); `provider_callback` (signed, replay-checked) |
| Authority (V12) | R0 internal analysis/draft; L1 assisted; L3 approved read/draft; Approve source/data rights and applicable external actions; approve experimental bounds, customer fairness, budget, pricing and publication before any live change. |
| Blueprint autonomy (DEC-566) | V12 L1 assisted / L3 approved read-draft → blueprint **L0–L1** (drafts and analysis only; no external effect). Approver: R08 |
| Human approval (workbook) | Approve source/data rights and applicable external actions; approve experimental bounds, customer fairness, budget, pricing and publication before any live change. |
| Effect boundary | No external effect; internal artifacts only |
| Outputs produced (v3 projection) | `margin_minor`, `exception_ref` |
| Workflow KPI | price deviation recall; approval routing rate; baseline and threshold approved in pilot; source service KPI Price/margin calculations reconcile 100%; unapproved changes = 0 |
| Preconditions / failure handling | Common contract (D-F12-030 variant 2, D-F12-031): §11.4b.5 |
| Cost | V12 illustrative ₹0.55/invocation (excludes provider, retry, labour). Blueprint model estimate ₹0.00/run for 2 agent step(s) at Tier 0 (Part 7.3 prices, FX ₹90/USD, verify at time of implementation, as of 27 Nov 2026); Tier 2 not eligible (Confidential/personal data) |
| Usage limit (pilot, not approved) | Illustrative pilot: 50 Pricing scenario(s)/month; 1 concurrent run; approved caps, provider quotas and hard budget required. |
| Data modalities / version | Text; structured records; service 1.0-target, workflow 1.0-target |
| Acceptance (V12 → blueprint) | SM-SVC-37-WF04-TC-{POS,INPUT,SCOPE,ENT,DUP,QUALITY,BUDGET,RECOVERY} → TC-V12-D-101…108; SM-SVC-37-WF04-AT01 → TC-V12-D-111 |
| Release proposal | A2 |

| Step ID | Action (V12) | V12 executor → node type | Blueprint handler | Output contract | Failure → run state | Model tier | Status |
|---|---|---|---|---|---|---|---|
| SM-SVC-37-WF04-STEP-01 | Detect price/margin deviation | Domain agent → NT13-08 `ai.task` + NT13-10 `approval.human` | AG-066 via gateway; routed to R08 | candidate {artifact_ref,confidence,reason_codes,review_state} | REVIEW_REQUIRED → AWAITING_APPROVAL | Tier 0 | Matched |
| SM-SVC-37-WF04-STEP-02 | flag and route approval | Domain agent → NT13-08 `ai.task` + NT13-10 `approval.human` | AG-066 via gateway; routed to R08 | candidate {artifact_ref,confidence,reason_codes,review_state} | REVIEW_REQUIRED → AWAITING_APPROVAL | Tier 0 | Matched |

### 11.4.5.27 SM-SVC-38 SMS, RCS & Business Messaging Automation

| Field | Specification |
|---|---|
| Family / objective | Mobile messaging; Coordinate SMS and rich business messaging |
| Channels / providers | Private Admin; approved client data and connectors; SMS/RCS; Authorized SMS/RCS provider, sender registration and recipient permission |
| Optional producers / complementary | Included foundation; no mandatory upstream paid service; optional input producers: SM-SVC-06; SM-SVC-07; SM-SVC-08; SM-SVC-09; authorized equivalent input accepted. |
| Service KPI | Consent and suppression checks 100%; duplicate dispatch = 0 |
| Availability / bundle | Full / Outreach & Conversations / selective (1 SKU); eligible inputs and approvals required. |
| Interoperability / readiness | Optional authorized connector; external agent access disabled unless explicitly granted; Provider, jurisdiction and specialist approval required before live operation |
| Open-source stack | Python; Django REST Framework; PostgreSQL; Celery/Beat; Valkey; pgvector if needed; specialist library/provider review pending |
| Blueprint epic / module | EP-08 (ASSUMPTION-826) / `engagement.sms` |
| Effect adapter | ADP-SMS (DLT-registered SMS/RCS aggregator, not procured) |
| Service guardrail | TR-R1: DLT header and template registration plus NCPR/DND scrub are activation gates; no SMS in W0-W5. |
| Functional requirement | FR-V12-D-138 (§11.4.5.29 register) |

**DTO `urn:sm:dto:SM-SVC-38-WF0n:v2` (one schema shared by the four workflows; v3 projection per workflow below):**

| Dir | Field | JSON Schema (App. B v2) | V12 validation | Blueprint storage target |
|---|---|---|---|---|
| in | `sender_ref` | string format=uuid | UUID / scoped external reference; input, validate authorized scope | eng_channel_account.id (ENT-089) |
| in | `template_ref` | string format=uuid | UUID / scoped external reference; input, validate authorized scope | aut_workflow_template / eng_message_template by service |
| in | `recipient_refs` | array maxItems=500 | array (typed references or structured items); input, validate authoriz | intel_contact.id[] |
| in | `consent_refs` | array maxItems=500 | array (typed references or structured items); input, validate authoriz | gov_consent.id[] |
| out | `eligibility_state` | string maxLength=64 | string / configured enum; length and allowed values in versioned schem | enum {eligible, held, blocked} |
| out | `dispatch_ref` | string format=uuid | UUID / scoped external reference; output, validate schema and evidence | ops_outbox / eng_message.id |
| out | `delivery_state` | string maxLength=64 | string / configured enum; length and allowed values in versioned schem | enum {queued, sent, delivered, failed, unknown} |
| out | `suppression_state` | string maxLength=64 | string / configured enum; length and allowed values in versioned schem | enum {none, suppressed, complaint} |

#### SM-SVC-38-WF01 Sender registration, template and communication eligibility validation

| Field | Specification |
|---|---|
| V12 sources | BRD ch09 row; FSD ch12 lines 15915–16007; FSD ch13 registry row; App. B `urn:sm:dto:SM-SVC-38-WF01:v2`; workbook row "SM-SVC-38-WF01 — Sender registration, template and communication eligibility validation" |
| Business outcome | Sender registration, template and communication eligibility validation. Input → output: Sender account, approved template, opt-in records → Eligibility decision |
| Detailed functionality (workbook) | Verify provider approvals and eligibility; hold missing evidence |
| Blueprint mapping | TR-R1 activation gates (Part 4.1); agents none (deterministic only); automations AU-009, AU-044 |
| What V12 adds | New: verify DLT header/template registration and recipient eligibility; hold on missing evidence. |
| Behaviour status | Not covered → Matched |
| Trigger (V12) | Manual; scheduled monitoring; validated business event; authorized provider webhook when available; Sender account, approved template, opt-in records |
| Trigger kinds (registry, DEC-564) | `manual` (NT13-03); `scheduled` (NT13-02; default cadence per §11.4b, misfire `reschedule_once`); `event` (NT13-01; `sm.svc38.wf01.requested` or upstream domain event, §11.4b.6); `provider_callback` (signed, replay-checked) |
| Authority (V12) | R0 internal analysis/draft; L1 assisted; L3 approved read/draft; Approve source/data rights and applicable external actions; verify recipient permission, sender identity, disclosure, quiet hours and provider rules before contact. |
| Blueprint autonomy (DEC-566) | V12 L1 assisted / L3 approved read-draft → blueprint **L0–L1** (drafts and analysis only; no external effect). Approver: R10 |
| Human approval (workbook) | Approve source/data rights and applicable external actions; verify recipient permission, sender identity, disclosure, quiet hours and provider rules before contact. |
| Effect boundary | No external effect; internal artifacts only |
| Outputs produced (v3 projection) | `eligibility_state` |
| Workflow KPI | sender approval accuracy; ineligible rejection; baseline and threshold approved in pilot; source service KPI Consent and suppression checks 100%; duplicate dispatch = 0 |
| Preconditions / failure handling | Common contract (D-F12-030 variant 2, D-F12-031): §11.4b.5 |
| Cost | V12 illustrative ₹0.55/invocation (excludes provider, retry, labour). Blueprint model estimate ₹0.00/run for 0 agent step(s) at Tier 1a (Part 7.3 prices, FX ₹90/USD, verify at time of implementation, as of 27 Nov 2026); Tier 2 not eligible (Confidential/personal data) |
| Usage limit (pilot, not approved) | Illustrative pilot: 500 Message attempt(s)/month; 1 concurrent run; approved caps, provider quotas and hard budget required. |
| Data modalities / version | Text; structured records; service 1.0-target, workflow 1.0-target |
| Acceptance (V12 → blueprint) | SM-SVC-38-WF01-TC-{POS,INPUT,SCOPE,ENT,DUP,QUALITY,BUDGET,RECOVERY} → TC-V12-D-101…108; SM-SVC-38-WF01-AT01 → TC-V12-D-111 |
| Release proposal | A2 (post Release 2) |

| Step ID | Action (V12) | V12 executor → node type | Blueprint handler | Output contract | Failure → run state | Model tier | Status |
|---|---|---|---|---|---|---|---|
| SM-SVC-38-WF01-STEP-01 | Verify provider approvals and eligibility | Policy/validation engine → NT13-09 `policy.check` | PDP (AU-009) rule set + AU-044 | validation {passed,reason_codes,policy_version} | POLICY_DENIED → BLOCKED | Tier 0 / none | Matched |
| SM-SVC-38-WF01-STEP-02 | hold missing evidence | Policy/validation engine → NT13-09 `policy.check` | PDP (AU-009) rule set + AU-044 | validation {passed,reason_codes,policy_version} | POLICY_DENIED → BLOCKED | Tier 0 / none | Matched |

#### SM-SVC-38-WF02 Authorized SMS and rich-message campaign coordination

| Field | Specification |
|---|---|
| V12 sources | BRD ch09 row; FSD ch12 lines 16008–16106; FSD ch13 registry row; App. B `urn:sm:dto:SM-SVC-38-WF02:v2`; workbook row "SM-SVC-38-WF02 — Authorized SMS and rich-message campaign coordination" |
| Business outcome | Authorized SMS and rich-message campaign coordination. Input → output: Eligible recipients, content, budget, schedule → Delivery event |
| Detailed functionality (workbook) | Check consent and frequency; dispatch approved messages; log outcome |
| Blueprint mapping | WF-06 outreach pattern; agents AG-011; automations AU-009, AU-022, AU-002 |
| What V12 adds | New: approved SMS/RCS campaigns dispatched via outbox with consent, caps and quiet hours. |
| Behaviour status | Not covered → Matched |
| Trigger (V12) | Manual; scheduled monitoring; validated business event; authorized provider webhook when available; Eligible recipients, content, budget, schedule |
| Trigger kinds (registry, DEC-564) | `manual` (NT13-03); `scheduled` (NT13-02; default cadence per §11.4b, misfire `reschedule_once`); `event` (NT13-01; `sm.svc38.wf02.requested` or upstream domain event, §11.4b.6); `provider_callback` (signed, replay-checked) |
| Authority (V12) | R2 external communication/provider/access write; L2 mandatory approved effect; L3 only with separately approved bounded mandate where lawful; Approve source/data rights and applicable external actions; verify recipient permission, sender identity, disclosure, quiet hours and provider rules before contact. |
| Blueprint autonomy (DEC-566) | V12 L2 exact approved effect → blueprint **L1 approval of the exact payload hash, then L2 dispatch** of that item through the outbox (DEC-064 publishing pattern); V12 L3 mandate only for routine replies/reminders within caps. Approver: R05L, R10 |
| Human approval (workbook) | Approve source/data rights and applicable external actions; verify recipient permission, sender identity, disclosure, quiet hours and provider rules before contact. |
| Effect boundary | Effect steps: STEP-02 via ADP-SMS (DLT-registered SMS/RCS aggregator, not procured) |
| Outputs produced (v3 projection) | `dispatch_ref`, `delivery_state` |
| Workflow KPI | duplicate dispatch count; authorized send rate; baseline and threshold approved in pilot; source service KPI Consent and suppression checks 100%; duplicate dispatch = 0 |
| Preconditions / failure handling | Common contract (D-F12-030 variant 2, D-F12-031): §11.4b.5 |
| Cost | V12 illustrative ₹0.55/invocation (excludes provider, retry, labour). Blueprint model estimate ₹0.00/run for 0 agent step(s) at Tier 1a (Part 7.3 prices, FX ₹90/USD, verify at time of implementation, as of 27 Nov 2026); Tier 2 not eligible (Confidential/personal data) |
| Usage limit (pilot, not approved) | Illustrative pilot: 500 Message attempt(s)/month; 1 concurrent run; approved caps, provider quotas and hard budget required. |
| Data modalities / version | Text; structured records; service 1.0-target, workflow 1.0-target |
| Acceptance (V12 → blueprint) | SM-SVC-38-WF02-TC-{POS,INPUT,SCOPE,ENT,DUP,QUALITY,BUDGET,RECOVERY,APPROVAL,EFFECT} → TC-V12-D-101…110; SM-SVC-38-WF02-AT01 → TC-V12-D-111 |
| Release proposal | A2 (post Release 2) |

| Step ID | Action (V12) | V12 executor → node type | Blueprint handler | Output contract | Failure → run state | Model tier | Status |
|---|---|---|---|---|---|---|---|
| SM-SVC-38-WF02-STEP-01 | Check consent and frequency | Policy/validation engine → NT13-09 `policy.check` | PDP (AU-009) rule set + AU-002 | validation {passed,reason_codes,policy_version} | POLICY_DENIED → BLOCKED | Tier 0 / none | Matched |
| SM-SVC-38-WF02-STEP-02 | dispatch approved messages | Effect adapter → NT13-13 `action.external` | Outbox → AU-009 dispatch recheck → ADP-SMS (DLT-registered SMS/RCS aggregator, not procured) | effect_receipt {provider_ref,status,observed_at} | EFFECT_UNKNOWN → RECONCILING | none | Matched |
| SM-SVC-38-WF02-STEP-03 | log outcome | Domain service → NT13-05 `data.write_internal` | `engagement.sms` service (revision check) | domain_result {artifact_ref,status,evidence_refs} | INVALID_STATE → HELD | Tier 0 / none | Matched |

#### SM-SVC-38-WF03 Delivery, inbound response and approved channel fallback

| Field | Specification |
|---|---|
| V12 sources | BRD ch09 row; FSD ch12 lines 16107–16205; FSD ch13 registry row; App. B `urn:sm:dto:SM-SVC-38-WF03:v2`; workbook row "SM-SVC-38-WF03 — Delivery, inbound response and approved channel fallback" |
| Business outcome | Delivery, inbound response and approved channel fallback. Input → output: Verified provider events, relationship state, fallback policy → Relationship update |
| Detailed functionality (workbook) | Reconcile delivery; classify reply; use permitted fallback only |
| Blueprint mapping | WF-06 callbacks; AU-008 STOP handler; agents AG-013; automations AU-026, AU-008 |
| What V12 adds | New: delivery reconciliation, inbound STOP/replies, fallback only to a channel with its own consent. |
| Behaviour status | Not covered → Matched |
| Trigger (V12) | Manual; scheduled monitoring; validated business event; authorized provider webhook when available; Verified provider events, relationship state, fallback policy |
| Trigger kinds (registry, DEC-564) | `manual` (NT13-03); `scheduled` (NT13-02; default cadence per §11.4b, misfire `reschedule_once`); `event` (NT13-01; `sm.svc38.wf03.requested` or upstream domain event, §11.4b.6); `provider_callback` (signed, replay-checked) |
| Authority (V12) | R2 external communication/provider/access write; L2 mandatory approved effect; L3 only with separately approved bounded mandate where lawful; Approve source/data rights and applicable external actions; verify recipient permission, sender identity, disclosure, quiet hours and provider rules before contact. |
| Blueprint autonomy (DEC-566) | V12 L2 exact approved effect → blueprint **L1 approval of the exact payload hash, then L2 dispatch** of that item through the outbox (DEC-064 publishing pattern); V12 L3 mandate only for routine replies/reminders within caps. Approver: R05L |
| Human approval (workbook) | Approve source/data rights and applicable external actions; verify recipient permission, sender identity, disclosure, quiet hours and provider rules before contact. |
| Effect boundary | No external effect; approval gate inserted before state change (DEC-570) |
| Outputs produced (v3 projection) | `delivery_state` |
| Workflow KPI | fallback eligibility accuracy; delivery reconciliation; baseline and threshold approved in pilot; source service KPI Consent and suppression checks 100%; duplicate dispatch = 0 |
| Preconditions / failure handling | Common contract (D-F12-030 variant 2, D-F12-031): §11.4b.5 |
| Cost | V12 illustrative ₹0.55/invocation (excludes provider, retry, labour). Blueprint model estimate ₹0.03/run for 1 agent step(s) at Tier 1a (Part 7.3 prices, FX ₹90/USD, verify at time of implementation, as of 27 Nov 2026); Tier 2 not eligible (Confidential/personal data) |
| Usage limit (pilot, not approved) | Illustrative pilot: 500 Message attempt(s)/month; 1 concurrent run; approved caps, provider quotas and hard budget required. |
| Data modalities / version | Text; structured records; service 1.0-target, workflow 1.0-target |
| Acceptance (V12 → blueprint) | SM-SVC-38-WF03-TC-{POS,INPUT,SCOPE,ENT,DUP,QUALITY,BUDGET,RECOVERY,APPROVAL,EFFECT} → TC-V12-D-101…110; SM-SVC-38-WF03-AT01 → TC-V12-D-111 |
| Release proposal | A2 (post Release 2) |

| Step ID | Action (V12) | V12 executor → node type | Blueprint handler | Output contract | Failure → run state | Model tier | Status |
|---|---|---|---|---|---|---|---|
| SM-SVC-38-WF03-STEP-01 | Reconcile delivery | Identity/reconciliation engine → NT13-07 `logic.compute` | AU-026 registered function | match_result {matched_refs,unmatched_refs,conflict_refs} | CONFLICT → HELD | Tier 0 / none | Matched |
| SM-SVC-38-WF03-STEP-02 | classify reply | Domain agent → NT13-08 `ai.task` + NT13-10 `approval.human` | AG-013 via gateway; routed to R05L | candidate {artifact_ref,confidence,reason_codes,review_state} | REVIEW_REQUIRED → AWAITING_APPROVAL | Tier 1a | Matched |
| SM-SVC-38-WF03-STEP-03 | use permitted fallback only | Domain service → NT13-05 `data.write_internal` | `engagement.sms` service (revision check) | domain_result {artifact_ref,status,evidence_refs} | INVALID_STATE → HELD | Tier 0 / none | Matched |

#### SM-SVC-38-WF04 Messaging performance, usage and suppression monitoring

| Field | Specification |
|---|---|
| V12 sources | BRD ch09 row; FSD ch12 lines 16206–16304; FSD ch13 registry row; App. B `urn:sm:dto:SM-SVC-38-WF04:v2`; workbook row "SM-SVC-38-WF04 — Messaging performance, usage and suppression monitoring" |
| Business outcome | Messaging performance, usage and suppression monitoring. Input → output: Delivery metrics, complaints, usage, opt-outs → Messaging control report |
| Detailed functionality (workbook) | Calculate performance; enforce suppression and budget; flag risk |
| Blueprint mapping | AU-024 suppression; AU-031 auto-pause; agents AG-028; automations AU-024, AU-031, AU-012 |
| What V12 adds | New: SMS performance, usage and suppression monitoring. |
| Behaviour status | Not covered → Matched |
| Trigger (V12) | Manual; scheduled monitoring; validated business event; authorized provider webhook when available; Delivery metrics, complaints, usage, opt-outs |
| Trigger kinds (registry, DEC-564) | `manual` (NT13-03); `scheduled` (NT13-02; default cadence per §11.4b, misfire `reschedule_once`); `event` (NT13-01; `sm.svc38.wf04.requested` or upstream domain event, §11.4b.6); `provider_callback` (signed, replay-checked) |
| Authority (V12) | R1 scoped state write or safety control; L1/L2 review; L3 only for approved deterministic internal actions; Approve source/data rights and applicable external actions; verify recipient permission, sender identity, disclosure, quiet hours and provider rules before contact. |
| Blueprint autonomy (DEC-566) | V12 L1/L2 review; L3 only for approved deterministic internal actions → blueprint **L1** for state writes, **L3** only for registered deterministic internal steps (DEC-064). Approver: R05L |
| Human approval (workbook) | Approve source/data rights and applicable external actions; verify recipient permission, sender identity, disclosure, quiet hours and provider rules before contact. |
| Effect boundary | No external effect; internal artifacts only |
| Outputs produced (v3 projection) | `suppression_state` |
| Workflow KPI | complaint rate; suppression propagation latency; baseline and threshold approved in pilot; source service KPI Consent and suppression checks 100%; duplicate dispatch = 0 |
| Preconditions / failure handling | Common contract (D-F12-030 variant 2, D-F12-031): §11.4b.5 |
| Cost | V12 illustrative ₹0.55/invocation (excludes provider, retry, labour). Blueprint model estimate ₹0.03/run for 1 agent step(s) at Tier 1a (Part 7.3 prices, FX ₹90/USD, verify at time of implementation, as of 27 Nov 2026); Tier 2 not eligible (Confidential/personal data) |
| Usage limit (pilot, not approved) | Illustrative pilot: 500 Message attempt(s)/month; 1 concurrent run; approved caps, provider quotas and hard budget required. |
| Data modalities / version | Text; structured records; service 1.0-target, workflow 1.0-target |
| Acceptance (V12 → blueprint) | SM-SVC-38-WF04-TC-{POS,INPUT,SCOPE,ENT,DUP,QUALITY,BUDGET,RECOVERY} → TC-V12-D-101…108; SM-SVC-38-WF04-AT01 → TC-V12-D-111 |
| Release proposal | A2 (post Release 2) |

| Step ID | Action (V12) | V12 executor → node type | Blueprint handler | Output contract | Failure → run state | Model tier | Status |
|---|---|---|---|---|---|---|---|
| SM-SVC-38-WF04-STEP-01 | Calculate performance | Rules/analytics engine → NT13-07 `logic.compute` | AU-024 registered function | calculation {value,unit,assumptions,evidence_refs} | INVALID_METRIC → HELD | Tier 0 / none | Matched |
| SM-SVC-38-WF04-STEP-02 | enforce suppression and budget | Policy/validation engine → NT13-09 `policy.check` | PDP (AU-009) rule set | validation {passed,reason_codes,policy_version} | POLICY_DENIED → BLOCKED | Tier 0 / none | Matched |
| SM-SVC-38-WF04-STEP-03 | flag risk | Domain agent → NT13-08 `ai.task` + NT13-10 `approval.human` | AG-028 via gateway; routed to R05L | candidate {artifact_ref,confidence,reason_codes,review_state} | REVIEW_REQUIRED → AWAITING_APPROVAL | Tier 1a | Matched |

### 11.4.5.28 SM-SVC-39 Procurement & Supplier Management Automation

| Field | Specification |
|---|---|
| Family / objective | Procurement; Manage procurement separately from sales fulfillment |
| Channels / providers | Private Admin; approved client data and connectors; Authorized supplier records, approved purchasing policies and ERP connections |
| Optional producers / complementary | Included foundation; no mandatory upstream paid service; optional input producers: SM-SVC-02; SM-SVC-17; SM-SVC-20; SM-SVC-21; authorized equivalent input accepted. |
| Service KPI | Approved purchase commitment checks 100%; unmatched receipt escalated |
| Availability / bundle | Full / Commerce & Procurement / selective (1 SKU); eligible inputs and approvals required. |
| Interoperability / readiness | Optional authorized connector; external agent access disabled unless explicitly granted; Provider, jurisdiction and specialist approval required before live operation |
| Open-source stack | Python; Django REST Framework; PostgreSQL; Celery/Beat; Valkey; pgvector if needed; specialist library/provider review pending |
| Blueprint epic / module | EP-14 (ASSUMPTION-826) / `commerce.procurement` |
| Effect adapter | ADP-ERP (purchase order record/export, not procured) |
| Service guardrail | Payables stay separate from receivables (OrganicSpec, BR-S004); POs are human-approved commitments. |
| Functional requirement | FR-V12-D-139 (§11.4.5.29 register) |

**DTO `urn:sm:dto:SM-SVC-39-WF0n:v2` (one schema shared by the four workflows; v3 projection per workflow below):**

| Dir | Field | JSON Schema (App. B v2) | V12 validation | Blueprint storage target |
|---|---|---|---|---|
| in | `requirement_ref` | string format=uuid | UUID / scoped external reference; input, validate authorized scope | prc_requirement (proposed) |
| in | `supplier_refs` | array maxItems=500 | array (typed references or structured items); input, validate authoriz | intel_organization.id[] (supplier role) |
| in | `quote_refs` | array maxItems=500 | array (typed references or structured items); input, validate authoriz | prc_supplier_quote.id[] (proposed) |
| in | `budget_ref` | string format=uuid | UUID / scoped external reference; input, validate authorized scope | budget line (AU-002 hierarchy) |
| out | `shortlist_ref` | string format=uuid | UUID / scoped external reference; output, validate schema and evidence | aut_artifact (domain shortlist) |
| out | `comparison_ref` | string format=uuid | UUID / scoped external reference; output, validate schema and evidence | aut_artifact (comparison) |
| out | `purchase_order_ref` | string format=uuid | UUID / scoped external reference; output, validate schema and evidence | prc_purchase_order (proposed) |
| out | `exception_refs` | array maxItems=500 | array (typed references or structured items); output, validate schema  | aut_artifact items |

#### SM-SVC-39-WF01 Supplier qualification and procurement requirement preparation

| Field | Specification |
|---|---|
| V12 sources | BRD ch09 row; FSD ch12 lines 16306–16410; FSD ch13 registry row; App. B `urn:sm:dto:SM-SVC-39-WF01:v2`; workbook row "SM-SVC-39-WF01 — Supplier qualification and procurement requirement preparation" |
| Business outcome | Supplier qualification and procurement requirement preparation. Input → output: Approved requirements, supplier evidence, qualification rules → Supplier shortlist and requirement |
| Detailed functionality (workbook) | Validate need; score suppliers; flag gaps; route review |
| Blueprint mapping | WF-10 OrganicSpec buy orders; agents AG-032, AG-023; automations AU-007, AU-015 |
| What V12 adds | New: supplier qualification and requirement preparation (OrganicSpec buy side). |
| Behaviour status | Not covered → Matched |
| Trigger (V12) | Manual; scheduled monitoring; validated business event; authorized provider webhook when available; Approved requirements, supplier evidence, qualification rules |
| Trigger kinds (registry, DEC-564) | `manual` (NT13-03); `scheduled` (NT13-02; default cadence per §11.4b, misfire `reschedule_once`); `event` (NT13-01; `sm.svc39.wf01.requested` or upstream domain event, §11.4b.6); `provider_callback` (signed, replay-checked) |
| Authority (V12) | R0 internal analysis/draft; L1 assisted; L3 approved read/draft; Approve source/data rights and applicable external actions; approve purchase/order commitments, pricing and any external listing or supplier change. |
| Blueprint autonomy (DEC-566) | V12 L1 assisted / L3 approved read-draft → blueprint **L0–L1** (drafts and analysis only; no external effect). Approver: R07, R02 |
| Human approval (workbook) | Approve source/data rights and applicable external actions; approve purchase/order commitments, pricing and any external listing or supplier change. |
| Effect boundary | No external effect; internal artifacts only |
| Outputs produced (v3 projection) | `shortlist_ref` |
| Workflow KPI | supplier criteria coverage; conflict recall; baseline and threshold approved in pilot; source service KPI Approved purchase commitment checks 100%; unmatched receipt escalated |
| Preconditions / failure handling | Common contract (D-F12-030 variant 2, D-F12-031): §11.4b.5 |
| Cost | V12 illustrative ₹1.05/invocation (excludes provider, retry, labour). Blueprint model estimate ₹0.06/run for 2 agent step(s) at Tier 1a (Part 7.3 prices, FX ₹90/USD, verify at time of implementation, as of 27 Nov 2026); Tier 2 not eligible (Confidential/personal data) |
| Usage limit (pilot, not approved) | Illustrative pilot: 200 Procurement case(s)/month; 1 concurrent run; approved caps, provider quotas and hard budget required. |
| Data modalities / version | Text; structured records; service 1.0-target, workflow 1.0-target |
| Acceptance (V12 → blueprint) | SM-SVC-39-WF01-TC-{POS,INPUT,SCOPE,ENT,DUP,QUALITY,BUDGET,RECOVERY} → TC-V12-D-101…108; SM-SVC-39-WF01-AT01 → TC-V12-D-111 |
| Release proposal | A2 |

| Step ID | Action (V12) | V12 executor → node type | Blueprint handler | Output contract | Failure → run state | Model tier | Status |
|---|---|---|---|---|---|---|---|
| SM-SVC-39-WF01-STEP-01 | Validate need | Policy/validation engine → NT13-09 `policy.check` | PDP (AU-009) rule set + AU-007 | validation {passed,reason_codes,policy_version} | POLICY_DENIED → BLOCKED | Tier 0 / none | Matched |
| SM-SVC-39-WF01-STEP-02 | score suppliers | Rules/analytics engine → NT13-07 `logic.compute` | AU-015 registered function | calculation {value,unit,assumptions,evidence_refs} | INVALID_METRIC → HELD | Tier 0 / none | Matched |
| SM-SVC-39-WF01-STEP-03 | flag gaps | Domain agent → NT13-08 `ai.task` + NT13-10 `approval.human` | AG-032 via gateway; routed to R07 | candidate {artifact_ref,confidence,reason_codes,review_state} | REVIEW_REQUIRED → AWAITING_APPROVAL | Tier 1a | Matched |
| SM-SVC-39-WF01-STEP-04 | route review | Domain agent → NT13-08 `ai.task` + NT13-10 `approval.human` | AG-023 via gateway; routed to R07 | candidate {artifact_ref,confidence,reason_codes,review_state} | REVIEW_REQUIRED → AWAITING_APPROVAL | Tier 1a | Matched |

#### SM-SVC-39-WF02 RFQ generation and supplier quotation comparison

| Field | Specification |
|---|---|
| V12 sources | BRD ch09 row; FSD ch12 lines 16411–16509; FSD ch13 registry row; App. B `urn:sm:dto:SM-SVC-39-WF02:v2`; workbook row "SM-SVC-39-WF02 — RFQ generation and supplier quotation comparison" |
| Business outcome | RFQ generation and supplier quotation comparison. Input → output: Approved requirements, eligible supplier quotes → Quotation comparison |
| Detailed functionality (workbook) | Draft RFQ; normalize terms; compare price and quality |
| Blueprint mapping | WF-10 RFQ extraction (AG-023); agents AG-020, AG-023; automations AU-035 |
| What V12 adds | RFQ/PO extraction exists (AG-023); V12 adds RFQ drafting and normalized quote comparison. |
| Behaviour status | Partially covered → Matched |
| Trigger (V12) | Manual; scheduled monitoring; validated business event; authorized provider webhook when available; Approved requirements, eligible supplier quotes |
| Trigger kinds (registry, DEC-564) | `manual` (NT13-03); `scheduled` (NT13-02; default cadence per §11.4b, misfire `reschedule_once`); `event` (NT13-01; `sm.svc39.wf02.requested` or upstream domain event, §11.4b.6); `provider_callback` (signed, replay-checked) |
| Authority (V12) | R0 internal analysis/draft; L1 assisted; L3 approved read/draft; Approve source/data rights and applicable external actions; approve purchase/order commitments, pricing and any external listing or supplier change. |
| Blueprint autonomy (DEC-566) | V12 L1 assisted / L3 approved read-draft → blueprint **L0–L1** (drafts and analysis only; no external effect). Approver: R07 |
| Human approval (workbook) | Approve source/data rights and applicable external actions; approve purchase/order commitments, pricing and any external listing or supplier change. |
| Effect boundary | No external effect; internal artifacts only |
| Outputs produced (v3 projection) | `comparison_ref` |
| Workflow KPI | normalized quote accuracy; comparison completeness; baseline and threshold approved in pilot; source service KPI Approved purchase commitment checks 100%; unmatched receipt escalated |
| Preconditions / failure handling | Common contract (D-F12-030 variant 2, D-F12-031): §11.4b.5 |
| Cost | V12 illustrative ₹1.05/invocation (excludes provider, retry, labour). Blueprint model estimate ₹1.26/run for 1 agent step(s) at Tier 1a (Part 7.3 prices, FX ₹90/USD, verify at time of implementation, as of 27 Nov 2026); Tier 2 not eligible (Confidential/personal data) |
| Usage limit (pilot, not approved) | Illustrative pilot: 200 Procurement case(s)/month; 1 concurrent run; approved caps, provider quotas and hard budget required. |
| Data modalities / version | Text; structured records; service 1.0-target, workflow 1.0-target |
| Acceptance (V12 → blueprint) | SM-SVC-39-WF02-TC-{POS,INPUT,SCOPE,ENT,DUP,QUALITY,BUDGET,RECOVERY} → TC-V12-D-101…108; SM-SVC-39-WF02-AT01 → TC-V12-D-111 |
| Release proposal | A2 |

| Step ID | Action (V12) | V12 executor → node type | Blueprint handler | Output contract | Failure → run state | Model tier | Status |
|---|---|---|---|---|---|---|---|
| SM-SVC-39-WF02-STEP-01 | Draft RFQ | Domain agent → NT13-08 `ai.task` + NT13-10 `approval.human` | AG-020 via gateway; routed to R07 | candidate {artifact_ref,confidence,reason_codes,review_state} | REVIEW_REQUIRED → AWAITING_APPROVAL | Tier 1b | Matched |
| SM-SVC-39-WF02-STEP-02 | normalize terms | Domain service → NT13-05 `data.write_internal` | `commerce.procurement` service (revision check) | domain_result {artifact_ref,status,evidence_refs} | INVALID_STATE → HELD | Tier 0 / none | Matched |
| SM-SVC-39-WF02-STEP-03 | compare price and quality | Rules/analytics engine → NT13-07 `logic.compute` | AU-035 registered function | calculation {value,unit,assumptions,evidence_refs} | INVALID_METRIC → HELD | Tier 0 / none | Matched |

#### SM-SVC-39-WF03 Approved purchase order and supplier commitment coordination

| Field | Specification |
|---|---|
| V12 sources | BRD ch09 row; FSD ch12 lines 16510–16608; FSD ch13 registry row; App. B `urn:sm:dto:SM-SVC-39-WF03:v2`; workbook row "SM-SVC-39-WF03 — Approved purchase order and supplier commitment coordination" |
| Business outcome | Approved purchase order and supplier commitment coordination. Input → output: Approved requisition, selected quote, budget authority → Purchase order |
| Detailed functionality (workbook) | Calculate order; obtain purchasing approval; record supplier commitment |
| Blueprint mapping | WF-10 payables; agents none (deterministic only); automations AU-035, AU-009, AU-002 |
| What V12 adds | New: purchase order commitment after human approval (L1); R3 L3 mandate path not adopted. |
| Behaviour status | Not covered → Matched (CONFLICT-814) |
| Trigger (V12) | Manual; scheduled monitoring; validated business event; authorized provider webhook when available; Approved requisition, selected quote, budget authority |
| Trigger kinds (registry, DEC-564) | `manual` (NT13-03); `scheduled` (NT13-02; default cadence per §11.4b, misfire `reschedule_once`); `event` (NT13-01; `sm.svc39.wf03.requested` or upstream domain event, §11.4b.6); `provider_callback` (signed, replay-checked) |
| Authority (V12) | R3 financial/legal/commitment; L2 mandatory approved effect; L3 only with separately approved bounded mandate where lawful; Approve source/data rights and applicable external actions; approve purchase/order commitments, pricing and any external listing or supplier change. |
| Blueprint autonomy (DEC-566) | V12 L2 default → blueprint **L1 maximum** (human approval bound to the exact hash; money movement not supported, DEC-064). V12 "L3 bounded mandate" **not adopted** (CONFLICT-814, Pending Founder decision). Approver: R07, R08, R09 |
| Human approval (workbook) | Approve source/data rights and applicable external actions; approve purchase/order commitments, pricing and any external listing or supplier change. |
| Effect boundary | Effect steps: STEP-03 via ADP-ERP (purchase order record/export, not procured) |
| Outputs produced (v3 projection) | `purchase_order_ref` |
| Workflow KPI | budget violation rejection; duplicate PO count; baseline and threshold approved in pilot; source service KPI Approved purchase commitment checks 100%; unmatched receipt escalated |
| Preconditions / failure handling | Common contract (D-F12-030 variant 2, D-F12-031): §11.4b.5 |
| Cost | V12 illustrative ₹0.55/invocation (excludes provider, retry, labour). Blueprint model estimate ₹0.00/run for 0 agent step(s) at Tier 1a (Part 7.3 prices, FX ₹90/USD, verify at time of implementation, as of 27 Nov 2026); Tier 2 not eligible (Confidential/personal data) |
| Usage limit (pilot, not approved) | Illustrative pilot: 200 Procurement case(s)/month; 1 concurrent run; approved caps, provider quotas and hard budget required. |
| Data modalities / version | Text; structured records; service 1.0-target, workflow 1.0-target |
| Acceptance (V12 → blueprint) | SM-SVC-39-WF03-TC-{POS,INPUT,SCOPE,ENT,DUP,QUALITY,BUDGET,RECOVERY,APPROVAL,EFFECT} → TC-V12-D-101…110; SM-SVC-39-WF03-AT01 → TC-V12-D-111 |
| Release proposal | A2 |

| Step ID | Action (V12) | V12 executor → node type | Blueprint handler | Output contract | Failure → run state | Model tier | Status |
|---|---|---|---|---|---|---|---|
| SM-SVC-39-WF03-STEP-01 | Calculate order | Rules/analytics engine → NT13-07 `logic.compute` | AU-035 registered function | calculation {value,unit,assumptions,evidence_refs} | INVALID_METRIC → HELD | Tier 0 / none | Matched |
| SM-SVC-39-WF03-STEP-02 | obtain purchasing approval | Domain service → NT13-05 `data.write_internal` | `commerce.procurement` service (revision check) | domain_result {artifact_ref,status,evidence_refs} | INVALID_STATE → HELD | Tier 0 / none | Matched |
| SM-SVC-39-WF03-STEP-03 | record supplier commitment | Effect adapter → NT13-13 `action.external` | Outbox → AU-009 dispatch recheck → ADP-ERP (purchase order record/export, not procured) | effect_receipt {provider_ref,status,observed_at} | EFFECT_UNKNOWN → RECONCILING | none | Matched |

#### SM-SVC-39-WF04 Supplier performance, delivery and procurement exception monitoring

| Field | Specification |
|---|---|
| V12 sources | BRD ch09 row; FSD ch12 lines 16609–16707; FSD ch13 registry row; App. B `urn:sm:dto:SM-SVC-39-WF04:v2`; workbook row "SM-SVC-39-WF04 — Supplier performance, delivery and procurement exception monitoring" |
| Business outcome | Supplier performance, delivery and procurement exception monitoring. Input → output: Purchase order, verified receipts, supplier SLA → Supplier performance and exception report |
| Detailed functionality (workbook) | Track milestones and discrepancies; reconcile receipts; escalate |
| Blueprint mapping | WF-10 fulfilment ledger; agents none (deterministic only); automations AU-038, AU-037 |
| What V12 adds | Receipts and over-delivery checks exist (AU-038); V12 adds supplier SLA performance and exception report. |
| Behaviour status | Partially covered → Matched |
| Trigger (V12) | Manual; scheduled monitoring; validated business event; authorized provider webhook when available; Purchase order, verified receipts, supplier SLA |
| Trigger kinds (registry, DEC-564) | `manual` (NT13-03); `scheduled` (NT13-02; default cadence per §11.4b, misfire `reschedule_once`); `event` (NT13-01; `sm.svc39.wf04.requested` or upstream domain event, §11.4b.6); `provider_callback` (signed, replay-checked) |
| Authority (V12) | R1 scoped state write or safety control; L1/L2 review; L3 only for approved deterministic internal actions; Approve source/data rights and applicable external actions; approve purchase/order commitments, pricing and any external listing or supplier change. |
| Blueprint autonomy (DEC-566) | V12 L1/L2 review; L3 only for approved deterministic internal actions → blueprint **L1** for state writes, **L3** only for registered deterministic internal steps (DEC-064). Approver: R07 |
| Human approval (workbook) | Approve source/data rights and applicable external actions; approve purchase/order commitments, pricing and any external listing or supplier change. |
| Effect boundary | No external effect; internal artifacts only |
| Outputs produced (v3 projection) | `exception_refs` |
| Workflow KPI | receipt reconciliation; delivery exception recall; baseline and threshold approved in pilot; source service KPI Approved purchase commitment checks 100%; unmatched receipt escalated |
| Preconditions / failure handling | Common contract (D-F12-030 variant 2, D-F12-031): §11.4b.5 |
| Cost | V12 illustrative ₹0.55/invocation (excludes provider, retry, labour). Blueprint model estimate ₹0.00/run for 0 agent step(s) at Tier 1a (Part 7.3 prices, FX ₹90/USD, verify at time of implementation, as of 27 Nov 2026); Tier 2 not eligible (Confidential/personal data) |
| Usage limit (pilot, not approved) | Illustrative pilot: 200 Procurement case(s)/month; 1 concurrent run; approved caps, provider quotas and hard budget required. |
| Data modalities / version | Text; structured records; service 1.0-target, workflow 1.0-target |
| Acceptance (V12 → blueprint) | SM-SVC-39-WF04-TC-{POS,INPUT,SCOPE,ENT,DUP,QUALITY,BUDGET,RECOVERY} → TC-V12-D-101…108; SM-SVC-39-WF04-AT01 → TC-V12-D-111 |
| Release proposal | A2 |

| Step ID | Action (V12) | V12 executor → node type | Blueprint handler | Output contract | Failure → run state | Model tier | Status |
|---|---|---|---|---|---|---|---|
| SM-SVC-39-WF04-STEP-01 | Track milestones and discrepancies | Domain service → NT13-05 `data.write_internal` | `commerce.procurement` service (revision check) | domain_result {artifact_ref,status,evidence_refs} | INVALID_STATE → HELD | Tier 0 / none | Matched |
| SM-SVC-39-WF04-STEP-02 | reconcile receipts | Identity/reconciliation engine → NT13-07 `logic.compute` | AU-038 registered function | match_result {matched_refs,unmatched_refs,conflict_refs} | CONFLICT → HELD | Tier 0 / none | Matched |
| SM-SVC-39-WF04-STEP-03 | escalate | Domain service → NT13-05 `data.write_internal` | `commerce.procurement` service (revision check) | domain_result {artifact_ref,status,evidence_refs} | INVALID_STATE → HELD | Tier 0 / none | Matched |
