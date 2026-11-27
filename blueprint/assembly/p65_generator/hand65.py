import h_ep01, h_ep02, h_ep03, h_ep04, h_ep05, h_ep06, h_ep07

MODS = {"EP-01": h_ep01, "EP-02": h_ep02, "EP-03": h_ep03, "EP-04": h_ep04, "EP-05": h_ep05, "EP-06": h_ep06, "EP-07": h_ep07}
EPIC = {k: dict(intro=m.INTRO, groups=m.GROUPS, extra_ts=m.EXTRA_TS) for k, m in MODS.items()}
TS_TITLE = {}
for m in MODS.values():
    TS_TITLE.update(m.TS_TITLE)

FRONT = r"""# AI Growth Engine: Employee Sales & Marketing Automation
## Application Blueprint: PART 6 (Batch 6.5), Test Scenarios and Test Cases: EP-01 to EP-07

| Field | Value |
|---|---|
| Document | Application Blueprint, Part 6 (Batch 6.5): test scenarios (TS) and test cases (TC) for **EP-01 Platform foundation, identity reuse and tenancy**, **EP-02 Product truth and knowledge**, **EP-03 Consent, privacy, eligibility and compliance**, **EP-04 AI gateway, cost control and AI quality**, **EP-05 Market intelligence and discovery**, **EP-06 Opportunity scoring, contacts and research review** and **EP-07 CRM, lead capture and Customer 360**, covering every story and acceptance criterion of Part 5.1 (files 1b and 1c). Includes the Sprint 0 enablers (identity compatibility spike, RLS, outbox, PDP, gateway and eval harness), the two-tenant isolation matrix, the eligibility decision tables, scoring boundary values (DEC-011), source permissions, and privacy and retention. The requirement-to-test traceability matrix is Batch 6.6 (`Part-06-6_Requirements_Traceability_Matrix.md`) |
| Version | 1.0 · 27 Nov 2026 |
| Baseline | Part 0 (NFR-001…038, epic map), Part 0A (DEC-001…065, binding), Part 1 (BR register, personas P01–P16, KPI-01…31), Part 2.1 (FR register, CA-* profiles), Part 2.2 (WF-01…14, engine invariants E-1…E-9), Part 2.3 (BRL rules, roles R01–R20, ABAC-01…12, state machines §2.27), Part 2.4 (isolation layers §2.35, rate limits, NT/NX), Part 2.5 (UI states §2.47, WCAG 2.2 AA), Part 4.1/4.2 (THR-, NFR-039…099), **Part 5.1** (files 1a–1c: 74 stories US-0101…US-0710, 505 Gherkin AC, dimension matrix DM-001…057 and DM-R01…R40), **Part 6.1** (test strategy: conventions §6.1.12, techniques §6.1.11, GSE-SYN §6.1.7, clock control §6.1.6.5, provider simulator §6.1.6.3), Part 7.1/7.2 (agent IDs AG-001…036, referenced only) |
| Roles applied | QA Lead (primary), Business Systems Analyst, Principal Engineer, Security/Compliance/AI Governance Lead, Data Architect/DBA, DevOps/SRE Lead, FinOps Lead, Lead UX/UI Designer, Product Owner |
| Tag ranges used | ASSUMPTION-194…196 · GAP-170…171 in this file; GAP-172 and RECOMMENDATION-080 are issued in Batch 6.6 (same allocation) |

**Acronyms used in this batch.** AC acceptance criterion · AP acceptance procedure · BFF Backend-for-Frontend · BVA boundary value analysis · CT contract test · DM dimension-matrix row (Part 5.1a §5.6) · DT decision table · E2E end-to-end · EG error guessing · EP equivalence partitioning (technique; epics are always written EP-##) · EVR evidence record · IT integration test · LIA legitimate-interest assessment · OTP one-time password · PBT property-based testing · PDP Policy Decision Point · PKCE Proof Key for Code Exchange · PW pairwise · RLS row-level security · SoD separation of duties · SPC standard post-condition · SSRF server-side request forgery · ST state-transition testing · SYS system test · TOTP time-based one-time password · UC use case · UT unit test.

**Time-sensitive facts.** Identity-provider behaviour, MFA methods, model names and prices (illustrative only, DEC-042), search API terms, AWS budget alarms, jurisdiction rule packs (DPDP, GDPR/UK GDPR, CAN-SPAM, UAE/SG/AU), the DPDP privacy response deadline and the verifiable-consent mechanism for minors, tool versions (pytest, Hypothesis, Playwright, axe-core, schemathesis, k6) and browser versions are **unverified; verify at time of implementation (as of 27 Nov 2026)**. Money values are Part 5.1 fixture values, not prices.

---

## 6.5.1 How to read this batch

### 6.5.1.1 Scope and sources

| Item | Rule applied |
|---|---|
| Stories in scope | All 74 stories of Part 5.1: EP-01 (US-0101…0117), EP-02 (US-0201…0208), EP-03 (US-0301…0311), EP-04 (US-0401…0408), EP-05 (US-0501…0512), EP-06 (US-0601…0608), EP-07 (US-0701…0710) |
| Coverage obligation | Every Part 5.1 AC (505) has ≥ 1 TC; every FR whose epic is EP-01…EP-07 plus FR-OP001 (45 FRs, Part 5.1 §5.9.2.1) has ≥ 1 TC; every BRL rule enforced by these stories (Part 5.1 §5.9.2.4) has ≥ 1 TC, with a decision-table or boundary TC wherever the rule has conditions or thresholds (Part 6.1 §6.1.9.6). Coverage tables are in §6.5.9 |
| Ownership of platform batteries | Per Part 6.1 §6.1.12.1 this batch **owns** the tenancy, RLS, identity and BFF batteries (EP-01), the consent/eligibility/privacy/retention/jurisdiction/children/health-data batteries (EP-03) and the gateway/budget/eval-harness batteries (EP-04). Batches 6.2 and 6.3 reuse them by reference. Dispatch-engine batteries (outbox relay at scale, simulation, emergency stop, uncertain outcomes) are owned by EP-18 (Batch 6.3); the outbox *framework* tests of US-0110 are here |
| AI cases | Deterministic gateway, routing, budget, schema and guardrail tests are TCs here. Statistical agent quality (groundedness, accuracy, bias, refusal, injection resistance, schema compliance, latency, cost per task, fallback per agent AG-001…AG-036) is **Batch 6.4** (TC-AI-…); this batch tests the harness (US-0402) that executes those cases |
| Conventions | Part 6.1 §6.1.12: TS-<epic>-<2 digits>, TC-<epic>-<3 digits>; priorities P0–P3 (§6.1.12.3); test types T01–T21 (§6.1.3.1); techniques EP, BVA, DT, ST, PW, EG, PBT, UC, EXP (§6.1.11); levels UT, IT, CT, SYS, E2E, UAT |
| Data | GSE-SYN `gse_syn 1.4.0`, profile `s` (`ci`), `m` (`test`) or `uat` (`staging`), with the edge packs of Part 6.1 §6.1.7.2; Part 5.1 fixture names map to stable keys in §6.5.1.4 [ASSUMPTION-194] |
| Time | Dates in 2027 are reached with clock control (Part 6.1 §6.1.6.5). Times are IST (UTC+05:30) unless stated. Boundary interpretations not fixed by the baseline are listed in §6.5.1.6 [ASSUMPTION-196] |
| Environment | `ci`/`test` for UT/IT/CT/SYS/E2E; `staging` for UAT and AP runs; provider simulator and sandbox adapters only (ABAC-12; TP-11); the outbound allowlist guard is on in every non-production environment |

### 6.5.1.2 Compact test case table

Each epic section has (1) a scenario table (one TS per story, plus platform batteries for EP-01), (2) technique groups with the decision table, transition matrix, partition table or boundary table that generated the cases, and (3) the test cases. The mandatory template fields of Part 6.1 §6.1.12.2 are placed as follows (same layout as Batches 6.2 and 6.3).

| Template field (§6.1.12.2) | Where it appears |
|---|---|
| ID, Title | Columns *ID* and *Title* |
| Linked requirement / story | Column *Links*: AC first (the parent story is the AC's story: AC-0304-06 → US-0304), then FR, BRL, NFR, DEC, ABAC, AP, KPI, and the DM row realized. SM-UAT/SM-UX-UAT aliases are listed per FR in Batch 6.6, not on every row |
| Scenario | Group heading: every group belongs to exactly one TS (named at the end of the heading) |
| Preconditions, Test data | Column *Pre-conditions and data* (role and scope, flags, clock, simulator mode; GSE-SYN keys and edge-pack items; DM row) |
| Steps | Column *Steps* (numbered; API method and path or UI control by accessible name) |
| Expected result | Column *Expected*, including the **no-side-effect assertion for every denial** |
| Priority, Type, Technique, Automation, Level | Columns *P*, *Type*, *Tech*, *Auto*, *Lvl* |
| Risk area, Wave | Epic introduction and scenario table |

**Standard post-conditions (SPC; apply to every TC unless the row says otherwise).**

| SPC | Assertion | Source |
|---|---|---|
| SPC-1 | Two-tenant fixture loaded; zero T2 rows in any T1 response and vice versa; KPI-30 = 0 | TP-07; NFR-032; AP-10 |
| SPC-2 | Every denial: no state change, no outbox row, no provider-simulator call, no budget reservation, one audit event with outcome=denied and the rule ID | Part 5.1a §5.7.2; TP-01 |
| SPC-3 | Every state change: one audit event with actor, before/after state, revision and correlation ID | NFR-018; FR-ENG-01 |
| SPC-4 | No send to a suppressed or ineligible recipient in any test (KPI-17 = 0); outbound allowlist guard never tripped | QO-2; TP-11 |
| SPC-5 | No secret, token, raw Restricted value or business content in logs or traces (redaction corpus) | NFR-004; D-15 |

### 6.5.1.3 How the cases were derived

Two kinds of test case appear in every epic.

1. **Hand-designed technique groups** (marked by a design table in the group). They target the P0 areas named in the brief: identity compatibility (12 checks), RLS, outbox atomicity, the two-tenant isolation matrix, the RBAC table test, the PDP decision table, jurisdiction partitions, quiet-hours/frequency/age boundaries, privacy and retention, gateway routing, budget caps, eval gates, source permissions, SSRF, scoring BVA (DEC-011), qualification, deal stages, guardian verification and intake limits. They add boundaries, sneak paths, precedence pairs and properties that the Gherkin does not state.
2. **Specification-by-example groups.** Every remaining Part 5.1 Gherkin scenario is executed as one TC: *Background* and *Given* become pre-conditions and data, *When* becomes the steps and *Then* the expected result, with the SPC-2 no-side-effect assertion appended to every denial. The TC adds priority, type, technique, level, automation and the DM row by these rules:

| Attribute | Rule (first match) |
|---|---|
| Priority | Should/Could story → P2 (P0 if cross-tenant) · accessibility → P1 · denial, permission, validation or edge scenario citing a confidentiality, eligibility, privacy, AI-routing, budget, approval-hash or source-permission rule (BRL-TEN/ELG/PRV/SRC-01/04, BRL-AI-06/07/08, BRL-APR-01/02, T5, `@sec`, I4) → P0 · story in a P0 risk area: negative/permission → P0, happy path of an enabler/security/compliance story → P0, otherwise P1 · P1 risk area → P1 (alternate and observability P2) · P2 risk area → P2 |
| Type | `@a11y`/WCAG → T08 · cross-tenant → T15 · `@sec` → T07 · `@obs` → T21 · uncertain outcome → T18 · duplicate/replay → T16 · simulation → T17 · eligibility/privacy/source rule → T19 · budget → T20 · AI harness/routing/guardrail stories → T14 · imports → T11 · p95 latency at volume → T03 · locale/DST → T13 · otherwise T01 |
| Technique | Scenario Outline, boundary or `@D3` → BVA · transitions, expiry or pinned/terminal states → ST · validation → EP · negative citing a rule → DT, otherwise EG · permission → EP (actor-class partition, §5.6.2) · happy/alternate → UC · duplicate, integration failure or volume → EG |
| Level | mobile 360 px, keyboard or WCAG → E2E · latency → SYS · CI/pull-request checks → CT · otherwise the story's default level (UT for PDP, routing and scoring; IT for RLS, outbox, consent ledger, imports and gateway; SYS for API stories) |
| Automation | Y, except assistive-technology passes and PO decision steps (N with reason) |
| DM row | The tags and data of the scenario are mapped to the Part 5.1a dimension values; cross-tenant (T5), portfolio mutation (T3), dispatch certainty, sensitive data, SoD on mobile, time boundaries, flag-OFF and volume map to the risk rows DM-R01…R40 (§6.5.1.5), otherwise the pairwise row DM-001…057 with the most matching values is cited |

Every TC carries the pytest/Playwright markers `tc`, `req`, `p0` and the DM tag (Part 6.1 §6.1.9.3); Batch 6.6 rebuilds coverage from these documents with `assembly/build_rtm.py`.

### 6.5.1.4 Fixture keys used in this file [ASSUMPTION-194]

Part 5.1 Gherkin names map to GSE-SYN stable keys as follows. Part 5.1's second tenant **"External-A" (startup "Acme Foods")** is the GSE-SYN two-tenant fixture **T2** (named "Client B" in Part 6.1 §6.1.7.1 and "Client Alpha" in Batch 6.3); the label differs, the fixture is the same.

| Part 5.1 name | GSE-SYN key | Role / content |
|---|---|---|
| Tenant "Owner Portfolio" (AppNAI, MedMaarg, EduVerse, OrganicSpec + 21 synthetic) | `T1` | DEC-065 owner tenant |
| Tenant "External-A", startup "Acme Foods" | `T2` | External SaaS tenant (isolation attacker) |
| Startup "GreenLeaf Agro" | `T1/GreenLeaf` (created at run time, AP-01) | 26th owned startup |
| founder@ownerportfolio.example.com | `U-FOUNDER` | R01 |
| priya.m@ownerportfolio.example.com | `U-PRIYA-AN` | R02 AppNAI (also MedMaarg head in US-0201) |
| ravi.k@ownerportfolio.example.com | `U-RAVI-MM` | R03 MedMaarg |
| neha.p@ownerportfolio.example.com | `U-NEHA-MM` | R03 MedMaarg (not owner) |
| lakshmi.v@ownerportfolio.example.com | `U-LAKSHMI-EV` | R04 EduVerse |
| anil.t@ownerportfolio.example.com | `U-ANIL-T1` | R12 T1 |
| dpo@ownerportfolio.example.com | `U-DPO` | R10 |
| fin.maker@ownerportfolio.example.com | `U-FINMAKER` | R08 |
| s.iyer@platform.example.com | `U-SUPPORT` | R13 |
| admin@external-a.example.com, tenant.admin@external-a.example.com | `U-T2-ADMIN` | R12 T2 |
| buyer@acme-foods.example.com | `U-T2-PORTAL` | R16 T2 |
| asha.r@appnai.example.com | `U-ASHA-IDP` | Spike test user (R03 AppNAI) |
| Contacts: dr.nair@kims-hospital.example.com, admin.office@kims-hospital.example.com, it.head@infra-co.example.in, procurement@stadtwerke.example.de, jan.devries@gmail.example.com, cfo@lnt-infra.example.com, old.buyer@freshmart.example.com, parent.k@example.com, kavita.rao@example.com | `T1/*/CON-*` and EDGE-JURIS, EDGE-MINORS, EDGE-DUP | Jurisdiction, consent, suppression and guardian fixtures |
| Objects: OPP-7001…7004, D-9001…9004, D-7781, D-1001, EV-881, EV-902, SIG-3001, ORG-3301, CLM-0101/0102, PV-3/PV-4, L-3381, L-4120, PRV-2027-0042, MR-1001, MR-4410 | Same IDs as stable keys in `T1` | Part 5.1 data |

### 6.5.1.5 Dimension-matrix rows (Part 5.1a §5.6) [ASSUMPTION-195]

Part 5.1a §5.6.4 lists the 57 pairwise rows DM-001…057 individually, but §5.6.5 gives the 40 risk-based rows only as counts per risk rule. This batch numbers them in table order:

| Risk rule | Rows | Numbering used |
|---|---|---|
| RR-1 tenant isolation (T5) | 19 | DM-R01…R18 = actor A1…A6 × channel C1, C2, C3 (A1·C1 = R01, A1·C2 = R02, A1·C3 = R03 … A6·C3 = R18); DM-R19 = A8·C3 |
| RR-2 portfolio mutation (T3) | 6 | DM-R20…R25 = A1·C1, A1·C2, A1·C3, A2·C1, A2·C2, A2·C3 |
| RR-3 dispatch certainty | 4 | DM-R26 I4·D5·S3; R27 I4·D5·S7; R28 I3·D5·S3; R29 I2·D6·S3 |
| RR-4 sensitive data (A7) | 4 | DM-R30 EduVerse under-18 C1; R31 same C2; R32 MedMaarg clinical free text C1; R33 same C2 |
| RR-5 SoD on mobile | 1 | DM-R34 A3·S2·C2 |
| RR-6 time boundaries | 2 | DM-R35 Lc·D3·S5·C1; DM-R36 Ld·D3·S5·C3 |
| RR-7 flag OFF | 2 | DM-R37 T6·C1·A1; DM-R38 T6·C3·A8 |
| RR-8 volume | 2 | DM-R39 D6·C2·A1; DM-R40 D6·C3·A8 |

The dimension-matrix battery (TS-01-20) realizes all 97 rows per FR as parameterized suites; individual TCs cite the row they exercise explicitly.

### 6.5.1.6 Test-oracle interpretations for EP-01…EP-07 [ASSUMPTION-196]

Where Part 5.1 gives a threshold without saying whether it is inclusive, these interpretations are the test oracle (they extend Part 6.1 ASSUMPTION-184 and must be confirmed by Part 3/Part 4 specifications; a different decision changes the tests, not the code silently):

| # | Rule | Interpretation used | Source |
|---|---|---|---|
| 1 | MFA freshness (ABAC-11) | Fresh while now − mfa_at < 12 h; at exactly 12 h step-up | AC-0105-02 |
| 2 | Support grant expiry | Valid while now < expires_at; denied at the expiry instant | AC-0109-05 |
| 3 | Feature-flag precedence | Store unreadable → OFF; startup explicit > tenant explicit > platform default | US-0117 notes |
| 4 | Retention purge | Purge-eligible at the first nightly run whose IST date ≥ anchor + period (calendar months or days) | AC-0308-01/02 |
| 5 | Evidence freshness and contact verification | Fresh through anchor + SLA − 1 day (23:59:59 IST); stale from anchor + SLA 00:00 IST | AC-0504-03; AC-0604-03 |
| 6 | Eval regression tolerance | A drop equal to the tolerance passes; fail only when strictly greater | AC-0402-02 |
| 7 | Guardian OTP validity | Valid if entered before 10 min 00 s after issue | AC-0706-03 |
| 8 | Age at evaluation | Birthday evaluated at IST midnight for Indian learners | DEC-030; AC-0706-06 |
"""

COVERAGE_INTRO = """Coverage is computed by the generator from the case tables above (and recomputed independently by `assembly/build_rtm.py` in Batch 6.6). A TC covers an AC when the AC ID is in its links; it covers an FR when the FR is in its links or it realizes an AC of a story that Part 5.1 §5.9.2.1 maps to that FR.

"""

XFR_TABLE = """
**Cross-cutting FRs exercised (Part 2.1 §2.4.10).** FR-ENG-01 (US-0104, US-0110, isolation matrix), FR-STD-01 (US-0104, US-0107), FR-STD-02 (US-0110, US-0401), FR-STD-03 (US-0201, US-0701), FR-STD-04 (US-0110, US-0111), FR-NEG-01 (US-0103, US-0114), FR-ADP-01 (US-0112, US-0503), FR-UIS-02 (US-0204, US-0504, US-0601), FR-UIS-03 (US-0304), FR-UIS-04 (US-0110, US-0401), FR-DM-04 (US-0704, US-0706, US-0508), FR-CSM-01 (US-0701, US-0702), FR-FLT-03 (US-0504), FR-SRCH-01 (isolation matrix layer only; feature cases in EP-17). FR-A103 import (owner EP-20) is exercised by US-0208/US-0708 cases; FR-A090 evidence by US-0114 cases. FR-COP-01 and the FR-FLT families other than FLT-03 have no cases here (owner EP-17; Part 5.1 §5.9.2.7).
"""

DM_NOTE = """
Rows not realized by an individual TC are realized by the parameterized dimension-matrix battery TS-01-20 (TC rows "Run the DM battery for EP-0x FRs"), which executes all 97 rows minus constraint exclusions for every FR of EP-01…EP-07. Individual TCs cite the row they exercise so that a failure points to a concrete combination.
"""

TAIL = r"""
## 6.5.10 Register of tags issued in this batch

### 6.5.10.1 Assumptions

| ID | Assumption | Basis | Validate by | Risk if wrong |
|---|---|---|---|---|
| ASSUMPTION-194 | Part 5.1 fixture names map to GSE-SYN stable keys as in §6.5.1.4; in particular Part 5.1's "External-A / Acme Foods" is the GSE-SYN two-tenant fixture T2, the same fixture that Part 6.1 calls "Client B" and Batch 6.3 calls "Client Alpha" | RECOMMENDATION-017; Part 6.1 ASSUMPTION-182; Part 5.1 Gherkin backgrounds | QA Lead aligns the GSE-SYN v1 manifest labels in Sprint 0 | Low: only labels differ; isolation assertions are fixture-key based |
| ASSUMPTION-195 | The 40 risk-based dimension rows of Part 5.1a §5.6.5 are numbered DM-R01…DM-R40 in table order as in §6.5.1.5 | Part 5.1a §5.6.5 gives counts per risk rule only | Part 5.1 owner confirms or publishes the enumerated list | Low: renumbering changes DM tags only |
| ASSUMPTION-196 | Test-oracle interpretations for thresholds Part 5.1 leaves open (MFA 12 h, grant expiry instant, flag precedence, retention purge date, freshness and verification expiry, eval tolerance equality, OTP 10 min, age at IST midnight), listed in §6.5.1.6 | Part 6.1 ASSUMPTION-184 pattern; TP-01 fail closed | Part 3 domain specifications and Product Owner/R10 confirmation before W0-B | Medium: a different interpretation changes the expected result of the boundary TCs |

### 6.5.10.2 Gaps

| ID | Gap | Impact | Proposed resolution | Owner |
|---|---|---|---|---|
| GAP-170 | Part 2.3 §2.25 states "162 business rules", but its family counts (TEN 12, ELG 18, SRC 10, SCR 9, AI 12, APR 11, SEQ 5, MTG 6, MKT 10, BID 6, QTE 7, CTR 5, ORD 6, FIN 8, LCY 6, PUB 6, AUT 10, PRV 7, SVC 7) sum to **161**, and 161 distinct BRL IDs are defined. Part 6.1 coverage formulas divide by 162 | BRL coverage % is understated by one rule if 162 is used | Batch 6.6 uses the 161 defined IDs as the denominator; Part 2.3 owner to correct the count or add the missing rule | Part 2.3 author; Part 9 |
| GAP-171 | Load-test IDs collide: Part 4.2 §4.26 defines LT-01…LT-12 differently from Part 6.1 §6.1.14.1 (for example LT-02 is "Soak at design load" in 4.2 but "Public website and portal" in 6.1; LT-05 is 50 webhooks/s for 10 min vs 2 min). ERRATA-30 says Part 6.1 owns LT-01…LT-12, but Part 4.2's NFR rows cite its own LT meanings | NFR → test traceability is ambiguous for performance NFRs | Batch 6.6 traces NFRs to the Part 6.1 LT catalogue and reports the Part 4.2 cited LT separately; Part 4.2 should rename its catalogue (e.g. LP-01…12) or adopt Part 6.1's | Part 4.2 author; Part 9 |

GAP-172 and RECOMMENDATION-080 belong to the same allocation and are issued and registered in Batch 6.6 §6.6.9.

### 6.5.10.3 Inconsistencies observed in other parts (reported, not fixed)

| # | Where | Observation | Suggested owner action |
|---|---|---|---|
| 1 | Part 2.3 §2.25 | Rule count 162 vs 161 defined (GAP-170) | Correct the count or add the missing rule |
| 2 | Part 4.2 §4.26 vs Part 6.1 §6.1.14.1 | LT-01…LT-12 defined twice with different meanings (GAP-171; ERRATA-30 not yet applied in Part 4.2) | Rename Part 4.2's catalogue |
| 3 | Part 5.1a §5.6.5 | Risk rows DM-R01…R40 are referenced by ID format but not enumerated (ASSUMPTION-195) | Publish the enumerated list |
| 4 | Part 5.1 vs Part 6.1 vs Batch 6.3 | Second-tenant fixture named "External-A", "Client B" and "Client Alpha" (ASSUMPTION-194) | Align labels in the GSE-SYN manifest |
| 5 | Part 5.1 §5.9.2.1 | US-0303 (PDP), US-0304 (eligibility), US-0110 (outbox), US-0113, US-0114, US-0115 and US-0117 are not mapped to any FR in the FR → stories table although their traces cite FRs (e.g. US-0304 → FR-A032, A034, A037–A039 as consumers) | Add a "cross-cutting / consumer" column to §5.9.2.1; this batch links their TCs to the traced FRs |
| 6 | Part 6.1 §6.1.4.3 | The risk matrix has no area for product truth and the readiness gate (EP-02); this batch uses RA-14 (promotion = publication risk) and RA-28 (editor) | Add an RA for product truth in the next revision of the risk matrix |
| 7 | Part 6.1 §6.1.12.1 | Example `TC-AI-AG07-012` uses a 2-digit agent number; Part 7 agent IDs have 3 digits (AG-024 → `AG024`) | Update the example; Batches 6.3/6.4 already use 3 digits |
| 8 | Part 5.1 US-0109 / US-0105 / US-0308 | Boundaries stated one second or one day away from the threshold (11:00:01, "exactly 12 h", 07-09 vs 07-11) without the threshold instant itself | Confirm the interpretations of ASSUMPTION-196 |

## 6.5.11 Quality gate: Batch 6.5

| # | Check | Result | Notes and fixes applied |
|---|---|---|---|
| 1 | Every requirement traced to a source | **Pass** | Every TC links at least one AC, FR, BRL or NFR; design tables cite BRL, DEC, NFR and Part 5.1 notes; thresholds not in the baseline are tagged (ASSUMPTION-196) |
| 2 | Assumptions, gaps and conflicts tagged and logged | **Pass** | ASSUMPTION-194…196 and GAP-170…171 issued from the allocated ranges and registered in §6.5.10; GAP-172 and RECOMMENDATION-080 registered in Batch 6.6; no conflicts raised; 8 inconsistencies reported in §6.5.10.3 |
| 3 | IDs unique and consistent with earlier parts | **Pass** | TS-01-01…TS-07-10 and TC-01-001…TC-07-{{LAST7}} sequential per epic (generator-assigned, no reuse); stories, AC, FR, BRL, DEC, NFR, ABAC, AP and KPI IDs taken from Parts 0A–5.1 by parser; three-digit AG format for any agent reference |
| 4 | No story lacks AC and no requirement lacks a test | **Pass** | 74/74 stories with TCs; **{{MISSING_AC}} of 505 AC uncovered**; FR coverage {{FR_OK}}; BRL coverage {{BRL_OK}} rules of §5.9.2.4 (script-checked in §6.5.9) |
| 5 | Negative, edge, security and accessibility cases covered | **Pass** | Denials with SPC-2 assertions; boundary tables per threshold; cross-tenant matrix over 13 isolation layers; SSRF, upload, token and CSRF cases; WCAG cases from US-0116, US-0310, US-0608 at E2E with manual assistive-technology passes; localization (Lb/Lc) and DST cases |
| 6 | No agent lacks guardrail, fallback, KPI and cost estimate | **N/A (agents) / Pass (platform)** | Per-agent cases are Batch 6.4. Platform guardrails (US-0406), fallback tiers (US-0403), cost reservation and caps (US-0404) and the eval harness (US-0402) are tested here |
| 7 | Time-sensitive facts flagged "verify" with an as-of date | **Pass** | IdP behaviour, model prices (illustrative), jurisdiction packs, DPDP deadlines, AWS alarms and tool versions flagged "verify at time of implementation (as of 27 Nov 2026)" |
| 8 | No restricted data routed to free-tier models | **Pass** | Routing decision table rule T6 and cases for Restricted and unclassified data; Tier 2 tested only with Public synthetic data in an opted-in test tenant; minors' data kept out of prompts (US-0706 case) |
| 9 | Consistent with earlier parts | **Pass, with findings** | PDP table, BVA lists, jurisdiction partitions and pairwise rules are those of Part 6.1 §6.1.11; risk areas and depth from §6.1.4.3; fixtures from §6.1.7; findings reported in §6.5.10.3. *Fixes applied while writing:* TC references inside design tables were removed where generator numbering could shift; the spike checklist table was verified against the generated IDs TC-01-001…013 |

**Status: Part 6 Batch 6.5 complete. {{TS}} test scenarios and {{TOTAL_TC}} test cases for EP-01 to EP-07 (P0 {{P0}}, P1 {{P1}}, P2 {{P2}}, P3 {{P3}}; {{HAND}} hand-designed technique cases and {{CONV}} specification-by-example cases; automation candidates {{AUTO}}). All 505 Part 5.1 acceptance criteria, all 45 EP-01…EP-07 FRs and the enforced BRL rules are covered; the requirement-to-test traceability matrix follows in Batch 6.6.**
"""
