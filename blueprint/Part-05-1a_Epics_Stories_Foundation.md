# AI Growth Engine: Employee Sales & Marketing Automation
## Application Blueprint: PART 5 (Batch 5.1a), Epics and User Stories: Front Matter (Purpose, DoR, DoD, INVEST, Estimation, Dimension Matrix, Conventions)

| Field | Value |
|---|---|
| Document | Application Blueprint, Part 5, Batch 5.1 (file 1a of 3). File 1b (`Part-05-1b_Epics_Stories_Foundation.md`) holds §5.8.1–§5.8.4 (EP-01 to EP-04); file 1c (`Part-05-1c_Epics_Stories_Foundation.md`) holds §5.8.5–§5.8.7 (EP-05 to EP-07) and §5.9 (size summary, coverage tables, tag register, findings, batch quality gate) |
| Version | 1.0 · 27 Nov 2026 |
| Baseline | BRD, FRD; Part 0 (requirement inventory, NFR-001…038, epic map §0.10.2); Part 0A (DEC-001…DEC-065, binding); Part 1 (BR register, personas P01–P16, KPIs, waves, MoSCoW); Part 2.1 (module catalogue, acceptance profiles CA-*, FR register); Part 2.2 (execution engine, WF-01…WF-14); Part 2.3 (BRL rules, roles R01–R20, ABAC-01…12, state machines); Part 2.4 (notifications, search, configuration, audit, multi-tenancy, localization); Part 2.5 (IA, 147 screens, WCAG 2.2 AA, UI states) |
| Roles applied | Product Owner (lead), Business Systems Analyst, QA Lead, Principal Engineer, Security/Compliance/AI Governance Lead, DevOps/SRE Lead, Lead UX Designer, FinOps Lead |
| Tags issued in this batch | RECOMMENDATION-050…053 · ASSUMPTION-150…159 · GAP-150…154 · CONFLICT-130…132 (full register in file 1c §5.9.3) |

**Acronyms used in this part.** AC = acceptance criterion · BFF = Backend-for-Frontend · CI/CD = continuous integration / continuous delivery · DAST = dynamic application security testing · DoD = Definition of Done · DoR = Definition of Ready · DPIA = Data Protection Impact Assessment · DPDP = Digital Personal Data Protection (India) · IaC = Infrastructure as Code · IdP = identity provider · INVEST = Independent, Negotiable, Valuable, Estimable, Small, Testable · MAS = minimum AC set (§5.6.6) · MFA = multi-factor authentication · OIDC = OpenID Connect · PDP = Policy Decision Point · PITR = point-in-time recovery · PKCE = Proof Key for Code Exchange · RLS = PostgreSQL row-level security · SAST = static application security testing · SCA = software composition analysis · SoD = separation of duties · SP = story point · SSRF = server-side request forgery · TOTP = time-based one-time password · WCAG = Web Content Accessibility Guidelines.

---

## 5.1 Purpose and structure of Part 5

### 5.1.1 Purpose

Part 5 turns the business requirements (Part 1), functional requirements (Part 2.1), business rules (Part 2.3) and binding decisions (Part 0A) into a **delivery backlog**. A team can plan sprints, estimate, build and accept work from it without further clarification. Each epic and story:

- traces to its BR, FR, NFR, BRL and DEC sources (client rule 1);
- carries a priority that is never higher than its BR's MoSCoW priority in Part 1 §1.12.1, and the wave of its FR in Part 2.1;
- carries a Fibonacci estimate given as a range, with the basis of estimate in §5.5;
- carries Gherkin acceptance criteria for the happy, alternate, negative, validation, permission and edge paths, built from the dimension matrix in §5.6.

Part 5 does **not** define test cases (Part 6), agent specifications (Part 7) or the sprint-by-sprint plan (Part 8). It gives Part 6 the scenarios to expand, Part 7 the AI stories to bound, and Part 8 the sized backlog to schedule.

### 5.1.2 Batch structure

| Batch | File(s) | Epics | Content |
|---|---|---|---|
| **5.1** (this batch) | `Part-05-1a_…` (this file, §5.1–§5.7), `Part-05-1b_…` (§5.8.1–§5.8.4), `Part-05-1c_…` (§5.8.5–§5.8.7, §5.9) | EP-01 to EP-07 | Part 5 front matter (binding on all batches); Sprint 0 enablers and spikes; foundation, product truth, governance, AI, discovery, qualification and CRM stories; coverage tables for EP-01 to EP-07 |
| 5.2 | `Part-05-2_Epics_Stories_Engagement_and_Commerce.md` (§5.10 onwards) | EP-08 to EP-14 | Messaging, meetings, WhatsApp/assistant, content, campaigns, proposal-to-contract, bids and orders |
| 5.3 | `Part-05-3_Epics_Stories_Closure_Automation_Web_SaaS.md` (§5.30–§5.41) | EP-15 to EP-21 | Closure and revenue, lifecycle, dashboards, automation engine, website/portal, SaaS, release and observability |

### 5.1.3 How to read a story

| Element | Meaning |
|---|---|
| Header table | ID, title, type, story statement, persona and roles, traces, priority, wave, points, dependencies, **dimension profile** (which matrix values the AC exercise, §5.6), notes |
| Gherkin block | `Feature:` = story title. Each `Scenario:` starts with its AC ID (`AC-0101-01`). Tag lines classify the path (§5.7.3) and cite the business rule a negative scenario enforces |
| Acceptance profiles | Every story also inherits the acceptance profiles of its FRs (CA-ALL, CA-ADMIN, CA-PUB, CA-INTAKE, CA-PORTAL, CA-APPROVE, CA-DISPATCH, CA-AI, CA-FIN, CA-CONFIG; Part 2.1 §2.3). Inherited conditions are binding even when not repeated in the Gherkin |
| Epic summary | Story count, SP range, person-day range, central estimate and the deviation from the indicative mid-point in the Part 5 brief |

---

## 5.2 Definition of Ready (DoR)

A story enters a sprint only when every applicable item below is checked. The Product Owner (founder/CTO, DEC-005) confirms DoR at refinement; the QA Lead confirms items 6–9.

| # | Criterion | Evidence of "ready" | Applies to |
|---|---|---|---|
| R-1 | Story statement uses a persona (P01–P16) and a role (R01–R20); the benefit is a business outcome, not a technical task | Header table complete | All except Enabler/Spike (which name the consuming epic instead) |
| R-2 | Traces: ≥ 1 FR or NFR, the parent BR, and every BRL/DEC the AC enforce | Trace row filled; IDs exist in Parts 0A/1/2 | All |
| R-3 | Priority ≤ BR priority; wave = FR wave (or earlier for an enabler) | Checked against Part 1 §1.12.1 and Part 2.1 | All |
| R-4 | Dependencies identified and either Done or scheduled earlier in the same sprint; external dependencies (DP-01…DP-15) have an owner and date | Dependency row; Part 1 §1.11 | All |
| R-5 | Estimated by the team as a Fibonacci range ≤ 13; anything larger is split | Points row | All |
| R-6 | Gherkin AC cover the MAS (§5.6.6): happy, ≥ 1 alternate, ≥ 1 negative citing a BRL, ≥ 1 validation, ≥ 1 permission denial, edge cases for the story's dimension profile | AC reviewed by QA Lead | All |
| R-7 | Test data identified: which synthetic fixture (US-0113) or which DM row (§5.6.5) the AC use | Fixture IDs referenced | All |
| R-8 | UX: screen reference (A###/W###) and UI states (Part 2.5 §2.47) known; new patterns have a wireframe | Screen ID; wireframe link if new | Stories with UI |
| R-9 | Data: entities, migrations and RLS policy impact known; retention class (DEC-028) and data classification (RECOMMENDATION-004) stated for new personal data | Notes row | Stories that persist data |
| R-10 | AI: task route (Tier 0–3), schema, eval dataset and per-task cost ceiling named (DEC-007, DEC-008, DEC-061) | Notes row; eval dataset ID | Stories with CA-AI |
| R-11 | External side effect: adapter, feature flag (default OFF), sandbox available, PDP checks listed (CA-DISPATCH) | Notes row | Stories with CA-DISPATCH |
| R-12 | Legal/compliance inputs available where the AC depend on them (jurisdiction pack, retention, DPIA, guardian consent) or the story is explicitly built behind a flag pending them (DP-12) | Link to legal note or flag name | Compliance stories |
| R-13 | Spike: question, time-box (pd), exit criteria and the decision it unblocks are written | Spike header | Spikes |

**Not ready → not pulled.** A story that fails R-2, R-6 or R-12 returns to refinement. A team may pull a story that fails only R-4 if the blocking dependency is completed earlier in the same sprint and the sprint plan shows it.

---

## 5.3 Definition of Done (DoD)

A story is Done only when every applicable item is satisfied **and** the evidence record (§5.3.2) is complete. "Applicable" is decided at DoR (R-8…R-12); an item marked N/A needs a reason (BRD §12.2 "approved N/A with reason").

### 5.3.1 DoD checklist

| # | Area | Done means | Gate / tool (verify versions at implementation, as of 27 Nov 2026) |
|---|---|---|---|
| D-1 | Code | Merged to the main branch through a pull request; builds reproducibly; no `TODO` without a linked ticket; no secrets in code or config (NFR-004); Django settings via environment/secret references only | CI build; secret scan (e.g. gitleaks) blocks merge |
| D-2 | Review | ≥ 1 reviewer other than the author; security-sensitive code (auth, RLS, PDP, finance, AI gateway, webhook verification) reviewed by a second engineer; migration reviewed by the data owner | PR approval rules (CODEOWNERS) |
| D-3 | Unit tests | New/changed business logic unit-tested, including every BRL the story enforces (one test per rule outcome: allow, deny, boundary) | pytest, Vitest/Jest |
| D-4 | Integration / API tests | Each endpoint: 200/201/202, 400, 401, 403/404 (uniform), 409 stale revision, 429 where rate-limited (NFR-015, FR-ENG-01); idempotency replay returns the original result | pytest + DRF test client; OpenAPI schema test |
| D-5 | Isolation tests | Every new table has `tenant_id`/`startup_id`, a composite FK and an RLS policy; the **two-tenant fixture** test proves zero cross-scope reads/writes (AP-10, NFR-032, BRL-TEN-03) | RLS test suite (US-0107, US-0114) |
| D-6 | Contract tests | Every provider adapter and webhook has a consumer-driven contract test with sandbox fixtures (RECOMMENDATION-011) | Contract test stage |
| D-7 | E2E tests | Stories that complete a user journey add or extend a Playwright journey (Website mobile 360 px and Admin desktop 1280 px; DEC-043) | Playwright in CI (smoke) and nightly (full) |
| D-8 | Coverage thresholds | Backend business modules: line ≥ 80%, branch ≥ 70%; **PDP, RLS policy code, finance/ledger code, AI gateway guards: line ≥ 90%, branch ≥ 85%**; frontend components ≥ 70% line. Coverage may not fall on changed files [ASSUMPTION-158] | Coverage report gate in CI |
| D-9 | Security scans | SAST (e.g. Semgrep/Bandit) 0 High/Critical; SCA/dependency scan 0 Critical, High only with a dated waiver; container image scan 0 Critical; DAST baseline (e.g. OWASP ZAP) on public/portal endpoints touched; OWASP Top 10 checklist item ticked for the story's risk (Part 4) | CI security stage; waivers recorded |
| D-10 | Accessibility | UI stories: axe-core 0 critical/serious violations; keyboard-only path works; visible focus; target size ≥ 24×24 px; screen-reader check (NVDA + Chrome or VoiceOver + Safari) for new components and public/portal pages; WCAG 2.2 AA (RECOMMENDATION-001, Part 2.5 §2.46) | axe in CI; manual checklist in PR |
| D-11 | AI evaluation gate | Stories with CA-AI: the task's eval suite passes its thresholds on the frozen dataset; any regression vs the last approved baseline blocks merge (DEC-061, NFR-033, BRL-AI-09); per-task cost within the ceiling; no Restricted data reaches Tier 2 (DEC-007) | Eval harness (US-0402) in CI |
| D-12 | Performance | Changed endpoints meet p95 ≤ 500 ms reads / ≤ 800 ms writes in staging with seed volume at 10× pilot (DEC-018, DEC-031); public pages meet the Part 2.5 §2.48 budgets | k6/Locust smoke; Lighthouse CI for public |
| D-13 | Documentation | OpenAPI updated; data dictionary entries for new fields; runbook entry for any new alert or job; ADR for any new runtime dependency (NFR-029); user-facing help text/microcopy per Part 2.5 §2.49 | Docs check in PR template |
| D-14 | Feature flag | Every external channel, paid adapter, autonomy mode, Tier 2 route and W5+/W6 capability ships behind a flag that **defaults OFF** in production (RECOMMENDATION-005, CFG-31); the flag's owner and removal criterion are recorded | Flag registry (US-0117) |
| D-15 | Observability | Structured logs carry `correlation_id`, `tenant_id`, `startup_id`, no business content or secrets; metrics for success/failure/latency; alerts for new failure modes routed per Part 4; audit events for every state change (CA-ALL, Part 2.4 §2.34) | Log redaction test; alert rule in IaC |
| D-16 | Data and privacy | Migrations are reversible or have a documented forward-fix; new personal-data fields have a retention class (DEC-028) and classification; exports/redaction rules updated (BRL-PRV-07) | Migration review |
| D-17 | Product Owner acceptance | PO (or delegated startup head for vertical stories) has accepted the story in staging against its AC; acceptance recorded with date | Acceptance in tracker |
| D-18 | Evidence record | The BRD §12.2 evidence record (§5.3.2) is complete and linked to the story | Evidence record template |

### 5.3.2 Evidence record per story (BRD §12.2, BR-S136)

The source requires an accountable owner to record "decision, approved scope, implementation commit/artifact digest, actual test result, independent reviewer and evidence" and states that no production sign-off may be inferred from the specification (BRD §12.2, CN-13). Each story's evidence record holds:

| Evidence field (BRD §12.2) | Required record for a Part 5 story |
|---|---|
| Responsible / reviewer | Implementing engineer (name, role) and independent reviewer (not the author; for security-sensitive code a second engineer; for compliance stories the Legal/Compliance officer, R10) |
| Artifact / test evidence | Commit SHA and container image digest; environment (test/staging); scenario IDs executed (AC IDs and the DM rows they used); actual result per AC; link to CI run, coverage report, scan reports, axe report, eval report |
| Decision | Pending / Pass / Fail / approved N/A with reason (per DoD item) |
| Remediation | Defect IDs, owner, corrective action and retest result for any failed AC or gate |
| Business acceptance | PO (or authorized startup head) sign-off after required gates pass, with date. Activation of compliance-gated capability also needs R10 sign-off (BRD §11, BR-S135) |

### 5.3.3 Done at epic and wave level

| Level | Additional Done conditions |
|---|---|
| Epic | All Must stories Done; epic-level isolation regression (two-tenant fixture) passes; KPI instrumentation for the epic's KPIs live; open Critical/High defects = 0 for confidentiality, financial integrity or unauthorized action (BR-S135) |
| Wave | Wave exit gate from Part 1 §1.6.1 met with evidence (e.g. W1: ≥ 100 reviewed signals at ≥ 80% precision, DEC-001); release readiness (FR-A090) approved by an independent reviewer (BR-S043) |

---

## 5.4 INVEST guidance with examples

| Letter | Rule for this backlog | Good example (this product) | Anti-pattern and fix |
|---|---|---|---|
| **I**ndependent | A story can be built and accepted on its own once its listed dependencies are Done. Shared mechanisms are built once as Enablers (outbox, RLS, PDP, gateway) and consumed by later stories | US-0501 *Register and approve a research source* depends only on US-0107 (RLS) and US-0110 (outbox); it can be accepted before any search runs | "Build discovery" (one story spanning A010–A021) → split along the WF-02 steps (US-0501…US-0508) |
| **N**egotiable | The statement fixes the outcome; layout, library and field order stay open until refinement. Binding constraints (BRL, DEC) are not negotiable | US-0601 says *what* the score must do (DEC-011 formula, Unknown < 0.60 weight); the UI may use bars or a table | Story text prescribing "use react-table v8" → move to technical notes; keep the outcome |
| **V**aluable | Each Feature story delivers value to a persona; each Enabler names the epic(s) it unblocks and the risk it retires | US-0303 *PDP skeleton* retires the "external action without recheck" risk for every dispatch story (E-3, BRL-ELG-18) | "Create tables for consent" (no user value) → fold into US-0301 *opt-out blocks all scoped sends* |
| **E**stimable | The team understands the rules and data well enough to give a Fibonacci range; uncertainty that prevents estimation becomes a Spike | US-0101 Spike time-boxed at 2–3 pd (DEC-019) because the IdP's behaviour is unknown | Estimating SSO integration before the spike → estimate after US-0101's report |
| **S**mall | ≤ 13 SP and normally ≤ 8 SP; fits in one sprint with test and evidence work | US-0606 *Qualified opportunity review* (3–5 SP) | "Customer 360 with timeline, invitations, eligibility and stop" at 21 SP → split projection (US-0707) from portal invitation (EP-19) |
| **T**estable | Every AC is observable: an HTTP status, a stored record, an audit event, a UI state, a metric. No AC says "fast", "secure" or "user-friendly" without a threshold | AC-0707-02 *timeline shows the reply within 60 s* (NFR-008) | "Customer 360 should be up to date" → "visible within 60 s, measured from event commit" |

**Splitting patterns used in this batch:** by workflow step (WF-02), by rule family (BRL-ELG in US-0304), by surface (public W29 vs Admin A013), by happy path then variants (US-0704 general enquiry, then US-0705/US-0706 variants), by enabler then feature (US-0401 gateway skeleton → US-0403 routing), and by wave (M66 gate in W0 US-0205 → launch workflow in W6 US-0207).

---

## 5.5 Estimation basis

### 5.5.1 Story points and person-days [ASSUMPTION-150]

> **Erratum v1.2 (E-V-39):** superseded by budget DEC-230 plus the funded V12 change requests (DEC-770/790). See Part 11.23c.


| Parameter | Value | Basis |
|---|---|---|
| Scale | Fibonacci 1, 2, 3, 5, 8, 13, written as a range (e.g. "3–5"); > 13 must be split | Part 5 brief |
| Conversion | **1 SP ≈ 0.5–1.0 person-day (pd), central 0.7 pd** for this team | [ASSUMPTION-150]; DEC-005 team mix (senior-heavy, part-time QA and DevOps) |
| What a point includes | Design, code, unit/integration/E2E tests, isolation test, scans, accessibility checks, docs, evidence record (DoD D-1…D-18) | [ASSUMPTION-152] |
| What a point excludes | Business-user UAT time, the 0.5 growth/compliance lead's work (labelling, legal liaison), provider procurement and verification lead times (SES production access, WhatsApp Business verification, OAuth app verification) | [ASSUMPTION-152], [ASSUMPTION-159] |
| Epic person-day range | **low = Σ SP_low × 0.5; high = Σ SP_high × 1.0; central = Σ SP_mid × 0.7** where SP_mid = (SP_low + SP_high) / 2 per story | Part 5 brief formula; central rate from [ASSUMPTION-150] |
| Programme envelope | All 21 epics must land within **287–483 pd** (BRD §6; DEC-012) | Checked per batch; batch 5.1 total in file 1c §5.9.1 |

### 5.5.2 Team velocity at 4.0 engineering FTE, 2-week sprints

**Formula.**

```text
capacity_pd_per_sprint = engineering_FTE × working_days_per_sprint × focus_factor
                       = 4.0 × 10 × 0.8 = 32 pd per sprint                       (DEC-005: 4.0 FTE, 0.8 focus)

velocity_SP_per_sprint = capacity_pd_per_sprint ÷ pd_per_SP
   at 1.0 pd/SP (pessimistic)   = 32 ÷ 1.0 = 32 SP
   at 0.7 pd/SP (central)       = 32 ÷ 0.7 ≈ 46 SP
   at 0.5 pd/SP (optimistic)    = 32 ÷ 0.5 = 64 SP
```

| Item | Value | Note |
|---|---|---|
| Engineering FTE | 4.0 = 1 backend + 1 full-stack + 1 frontend + 0.5 QA automation + 0.5 DevOps/SRE | DEC-005; the 0.5 growth/compliance lead and the founder/PO are not in velocity |
| Working days per sprint | 10 | 2-week sprints (ASSUMPTION-006, retained) |
| Focus factor | 0.8 | DEC-005 |
| **Expected velocity range** | **32–64 SP per sprint; planning value 40–46 SP** | Planning value = central (46) less ≈ 13% for meetings beyond focus loss, rounded to a 40–46 band |
| Ramp-up | Sprint 0 and Sprint 1 at **≈ 70% of planning value (≈ 28–32 SP)** | [ASSUMPTION-157] new team, new codebase, environment set-up |
| Sprints in W0–W5 | 125 working days ÷ 10 ≈ **12.5 sprints** → ≈ 400 pd capacity (DEC-005) | Overflow beyond the midpoint goes to W6 by MoSCoW (DEC-005) |
| Re-baseline | After Sprint 2, replace the planning value with the measured 3-sprint rolling average; keep the 0.5–1.0 pd/SP band for budget checks | Part 8 owns the plan |

**Fallback team (DEC-005).** With 3.0 engineering FTE: capacity = 3.0 × 10 × 0.8 = 24 pd/sprint → 24–48 SP (central ≈ 34 SP).

### 5.5.3 Consequence for Wave 0 [CONFLICT-130]

The W0 window (Day 1–15) holds ≈ 1.5 sprints ≈ 48 pd at full capacity, or ≈ 34 pd with the Sprint 0 ramp-up. Batch 5.1 alone books **≈ 113.5 SP mid (≈ 79 pd central; 35 stories)** of W0 stories (file 1c §5.9.1), before EP-17 (Command Centre shell) and EP-21 (release pipeline) add their W0 work. W1 adds a further ≈ 54 SP mid (≈ 38 pd central; 19 stories) in this batch, so W0 + W1 content (≈ 167.5 SP, ≈ 117 pd) exceeds the ≈ 3 sprints (≈ 96 pd at full capacity, less with ramp-up) available by Day 30. The W0 scope set by DEC-034 (M01–M09 + M53 + M56 + M58, plus the M66 gate, the M54 harness and the M61 shell) therefore **cannot be completed by Day 15** at DEC-005 capacity. This is logged as **[CONFLICT-130]** with the proposed resolution **[RECOMMENDATION-050]**: split the W0 exit gate into **Gate W0-A (Day 15)**, which proves the minimum control set that every later story depends on, and **Gate W0-B (Day 30)**, which completes the remaining W0 stories in parallel with W1 set-up. The W1 intelligence pilot (BRD §8 Day 16–30) starts discovery runs only after Gate W0-A, so no control is bypassed.

| Gate | Stories that must be Done (batch 5.1) | Why first |
|---|---|---|
| **W0-A (Day 15)** | US-0101 (spike report), US-0102, US-0103, US-0104, US-0107, US-0110, US-0113, US-0117, US-0301, US-0303, US-0401, US-0402, US-0404 | Identity, isolation, outbox, consent/suppression, PDP, gateway, cost cap and seed data are prerequisites of every other story and of the BRD §8 "controls tested" condition for anything that runs |
| **W0-B (Day 30)** | All other W0 stories in batch 5.1 (US-0105, US-0106, US-0108, US-0109, US-0111, US-0112, US-0114–US-0116, US-0201–US-0205, US-0302, US-0307, US-0308, US-0403, US-0405, US-0406, US-0408, US-0501) | Admin screens, document approval, privacy queue UI and retention purge can follow the controls they use; owner and claims sign-off (BRD §8) is recorded at W0-B |

Gate W0-A holds 46.5 SP mid (≈ 32.6 pd central), which fits Sprint 0 plus the first half of Sprint 1 at ramp-up velocity (§5.5.2). Gate W0-B holds the remaining 67 SP mid (≈ 47 pd central) of batch 5.1's W0 stories.

Part 8 owns the final schedule and must confirm or replace this split. Because W0-B overlaps W1, the W1 exit target (100 reviewed signals at ≥ 80% precision, BRD §8 Day 16–30) is **at risk of slipping to ≈ Day 40–45** unless W0-B screens that are not on the discovery path (US-0109, US-0111, US-0116, US-0307 UI, US-0308) are scheduled after the discovery stories US-0501–US-0506; this is part of [CONFLICT-130].

---

## 5.6 Dimension matrix and coverage rationale

The client asks that acceptance criteria cover the permutation space *persona/role × permission level × object state × data condition × channel × tenant/config variation × integration availability × locale*. This section defines the space **once**; all Part 5 batches apply it.

### 5.6.1 Dimension values (raw)

| # | Dimension | Raw values | Count | Source |
|---|---|---|---|---|
| 1 | Persona / role | R01 Founder · R02 Startup Head · R03 Growth Manager (incl. R03L) · R04 Research Analyst · R05 Marketing (incl. R05L) · R06 Bid Manager · R07 Order Coordinator · R08 Finance Maker · R09 Finance Checker · R10 Legal/Compliance/DPO · R11 Automation Lead · R12 Tenant Admin · R13 Platform Support · R14 Platform Billing · R15 Auditor · R16 External Customer/Supplier · R17 SaaS Applicant/Client Admin · R18 Anonymous Visitor · R19 Service Identity · R20 AI Agent Identity (personas P01–P16 map onto these per Part 2.3 §2.26.1) | 20 | Part 2.3 §2.26.1; Part 1 §1.8 |
| 2 | Permission level | — none · V view · C create · E edit own/assigned · A approve · X execute/dispatch · S configure · G time-bound grant (valid or expired) | 8 | Part 2.3 §2.26.2 |
| 3 | Object state (generic classes over all state machines) | S1 New/Draft · S2 Pending approval / in review · S3 Approved / Active / Published · S4 Terminal (closed, rejected, archived, withdrawn) · S5 Stale / Expired · S6 Pinned / locked (in flight, running revision) · S7 Uncertain / held (DEC-050) | 7 | Part 2.3 §2.27 |
| 4 | Data condition | D1 valid · D2 invalid · D3 boundary · D4 null / missing / Unknown · D5 duplicate / replay · D6 large (volume, file size, page size) | 6 | Part 5 brief; FRD §10 |
| 5 | Channel | C1 web desktop (Admin 1280 px, Website) · C2 mobile web (360 px; Website/Portal, Admin review screens per DEC-043) · C3 API (REST, webhooks, workers) | 3 | DEC-043; ASSUMPTION-014; NFR-015 |
| 6 | Tenant / config variation | AppNAI · MedMaarg · EduVerse · OrganicSpec (owned startups) · synthetic 26th startup from template (AP-01) · portfolio aggregate scope (DEC-055) · external SaaS tenant (DEC-065) · cross-tenant attempt from tenant B (AP-10) · feature flag OFF / tightened policy variant (RECOMMENDATION-005, BRL-APR-11) | 9 | BRD §1.1; DEC-055, DEC-065; AP-01, AP-10 |
| 7 | Integration availability | I1 up · I2 degraded (slow, 429, partial) · I3 down (error before submission) · I4 uncertain (timeout after submission) | 4 | FRD §11.1; DEC-050 |
| 8 | Locale and timezone | en-IN · Asia/Kolkata · hi-IN content · ta-IN content · or-IN content (each IST) · en-IN with America/New_York (DST) · en-IN with Europe/London (DST) · UTC ISO-8601 (API) | 7 | DEC-026; Part 2.4 §2.36 |

**Raw combination count per operation:**

```text
20 roles × 8 permission levels × 7 states × 6 data conditions × 3 channels × 9 tenant/config × 4 integration × 7 locale
= 20 × 8 = 160 → × 7 = 1,120 → × 6 = 6,720 → × 3 = 20,160 → × 9 = 181,440 → × 4 = 725,760 → × 7 = 5,080,320
```

**5,080,320 raw combinations per operation.** Across the ≈ 250 operations named or derived for the 150 interface FRs this is over 10⁹ combinations. Exhaustive testing is impossible and unnecessary; the reduction below keeps every risk-bearing interaction.

### 5.6.2 Reduction step 1: merges (equivalence classes)

| Dimension | Merge applied | Result | Why this is safe |
|---|---|---|---|
| Role × permission (20 × 8 = 160) | Merged into **8 actor classes** by the authorization *outcome* the PDP/permission classes compute: **A1** authorized author/operator · **A2** approver within authority · **A3** approver over limit or SoD conflict (author = approver, maker = checker) · **A4** read-only internal (incl. R15 Auditor, R13 metadata) · **A5** unauthorized internal (wrong role, wrong startup, expired membership or grant) · **A6** external authenticated (R16/R17) · **A7** anonymous (R18) · **A8** service/AI identity (R19/R20) | 8 | Every role reaches the decision through the same code path (BRL-TEN-01, ABAC-01…12). **The full role × screen-group matrix is still tested exhaustively** by one table-driven test generated from Part 2.3 §2.26.3: 42 internal screen-group rows × 15 roles + 10 external rows × 4 role columns = **670 cells** [RECOMMENDATION-053]. Stories therefore test classes; the matrix test proves each role lands in the right class |
| Tenant/config (9) | AppNAI, MedMaarg, EduVerse, OrganicSpec merged into **T1 owned startup (rotating vertical)**; the others kept: **T2** synthetic 26th startup · **T3** portfolio aggregate · **T4** external SaaS tenant · **T5** cross-tenant attempt · **T6** feature flag OFF / tightened policy | 6 | Generic behaviour is vertical-independent (template- and capability-driven, BRL-TEN-11). Vertical-specific rules (minors, health data, bids, orders, routing FR-DM-04) are covered by **risk rows** and by vertical stories, not by rotation alone |
| Locale (7) | hi-IN, ta-IN, or-IN merged into **Lb Indic content (rotating)**; America/New_York and Europe/London merged into **Lc DST timezone (rotating)**; kept **La** en-IN·IST and **Ld** UTC/API | 4 | Indic locales share one i18n pipeline (ICU, UTF-8, fallback chain; I18N-01…11). DST zones share one conversion path. Each merged value is still exercised at least once in the suite by rotation (EP-11/EP-19 content stories use all three Indic locales) |

Merged space: 8 × 7 × 6 × 3 × 6 × 4 × 4 = **96,768** combinations.

### 5.6.3 Reduction step 2: exclusions (impossible or prohibited combinations)

| Excluded combination | Reason | How the exclusion itself is verified |
|---|---|---|
| A7 anonymous on C3 internal APIs, on T3 portfolio scope, on S2/S6/S7 objects, or with I4 dispatch outcomes | Anonymous users reach only public pages and intake (BRD §9; R18) | One negative test per surface: Admin/API routes deny external and anonymous identities (BR-WEB acceptance) |
| A8 service/AI identity on C1/C2 | No browser access for service identities (BR-S109) | Negative test: service token rejected by BFF origins |
| A6/A7/A8 with T3 portfolio | Portfolio scope is an Admin concept for internal owners (DEC-055) | Covered by portfolio read-only tests (BRL-TEN-05) |
| Ld (UTC/API) on C1/C2; Lb on C3 | UI renders local time; API exchanges ISO-8601 UTC (I18N-03); content locale is a payload attribute, not an API channel variant | Contract tests on date fields |
| Admin UI in hi/ta/or | Admin UI is en-IN only (DEC-026) | Not tested; strings externalized only |
| Native mobile app channel | Out of scope (X-12, DEC-043) | Not applicable |
| Integration availability for operations without an external dependency | No adapter involved | N/A in the story's dimension profile |
| Restricted data × Tier 2 free model | Prohibited (DEC-007, BRL-AI-06) | Kept **only as a negative test** (AC-0403-03): the router must refuse; never a positive combination |

After constraints the merged space holds **57,600 valid combinations** and **594 valid value pairs** (computed by enumeration over the constrained space).

### 5.6.4 Reduction step 3: pairwise covering array

A constrained pairwise (all-pairs) covering array was generated over the seven merged dimensions with the exclusion constraints above (greedy covering algorithm, best of five seeds; regenerate with a tool such as PICT in Part 6 and keep the same constraints). **57 rows cover all 594 valid pairs.** The theoretical lower bound is 53 (8 actor classes × 7 states, less the 3 excluded anonymous-state pairs), so 57 is within 8% of optimal.

| DM row | Actor | State | Data | Channel | Tenant/config | Integration | Locale |
|---|---|---|---|---|---|---|---|
| DM-001 | A1 | S2 | D6 | C1 | T1 (AppNAI) | I2 | Lb |
| DM-002 | A1 | S4 | D1 | C1 | T1 (MedMaarg) | I1 | La |
| DM-003 | A2 | S7 | D6 | C1 | T1 (EduVerse) | I2 | La |
| DM-004 | A3 | S2 | D1 | C1 | T1 (OrganicSpec) | I1 | La |
| DM-005 | A3 | S3 | D4 | C2 | T1 (AppNAI) | I3 | La |
| DM-006 | A4 | S6 | D3 | C1 | T1 (MedMaarg) | I1 | La |
| DM-007 | A5 | S5 | D5 | C3 | T1 (EduVerse) | I1 | Ld |
| DM-008 | A6 | S4 | D1 | C1 | T1 (OrganicSpec) | I1 | La |
| DM-009 | A7 | S1 | D2 | C1 | T1 (AppNAI) | I1 | La |
| DM-010 | A7 | S1 | D4 | C1 | T1 (MedMaarg) | I1 | La |
| DM-011 | A8 | S3 | D1 | C3 | T1 (EduVerse) | I1 | La |
| DM-012 | A8 | S6 | D5 | C3 | T1 (OrganicSpec) | I4 | Lc |
| DM-013 | A8 | S7 | D4 | C3 | T1 (AppNAI) | I1 | La |
| DM-014 | A1 | S5 | D3 | C1 | T2 | I1 | La |
| DM-015 | A2 | S2 | D5 | C3 | T2 | I3 | Ld |
| DM-016 | A3 | S4 | D2 | C1 | T2 | I2 | La |
| DM-017 | A4 | S3 | D6 | C3 | T2 | I1 | Lc |
| DM-018 | A5 | S6 | D4 | C1 | T2 | I2 | La |
| DM-019 | A5 | S7 | D1 | C2 | T2 | I4 | Lb |
| DM-020 | A6 | S1 | D6 | C1 | T2 | I1 | La |
| DM-021 | A7 | S1 | D5 | C1 | T2 | I1 | La |
| DM-022 | A8 | S5 | D3 | C3 | T2 | I1 | La |
| DM-023 | A1 | S3 | D4 | C1 | T3 | I1 | La |
| DM-024 | A1 | S6 | D1 | C3 | T3 | I3 | Ld |
| DM-025 | A2 | S3 | D3 | C1 | T3 | I1 | Lc |
| DM-026 | A3 | S5 | D2 | C1 | T3 | I4 | Lc |
| DM-027 | A4 | S2 | D2 | C1 | T3 | I1 | La |
| DM-028 | A4 | S7 | D5 | C2 | T3 | I2 | La |
| DM-029 | A5 | S1 | D3 | C2 | T3 | I3 | Lb |
| DM-030 | A5 | S4 | D6 | C1 | T3 | I1 | La |
| DM-031 | A1 | S7 | D2 | C1 | T4 | I3 | La |
| DM-032 | A2 | S1 | D1 | C1 | T4 | I1 | La |
| DM-033 | A2 | S4 | D4 | C3 | T4 | I4 | Ld |
| DM-034 | A3 | S6 | D6 | C1 | T4 | I4 | Lb |
| DM-035 | A4 | S5 | D1 | C1 | T4 | I1 | La |
| DM-036 | A5 | S3 | D5 | C1 | T4 | I1 | Lc |
| DM-037 | A6 | S5 | D4 | C2 | T4 | I2 | Lb |
| DM-038 | A7 | S4 | D3 | C2 | T4 | I2 | Lc |
| DM-039 | A8 | S2 | D1 | C3 | T4 | I3 | Lc |
| DM-040 | A1 | S2 | D4 | C2 | T5 | I1 | Lc |
| DM-041 | A2 | S5 | D1 | C1 | T5 | I1 | La |
| DM-042 | A3 | S7 | D3 | C3 | T5 | I1 | Ld |
| DM-043 | A4 | S4 | D5 | C1 | T5 | I3 | Lb |
| DM-044 | A5 | S2 | D2 | C1 | T5 | I1 | La |
| DM-045 | A6 | S3 | D2 | C3 | T5 | I4 | Ld |
| DM-046 | A6 | S6 | D5 | C1 | T5 | I1 | La |
| DM-047 | A7 | S5 | D6 | C2 | T5 | I3 | La |
| DM-048 | A8 | S1 | D2 | C3 | T5 | I2 | Ld |
| DM-049 | A1 | S1 | D5 | C1 | T6 | I4 | Lc |
| DM-050 | A2 | S6 | D2 | C2 | T6 | I1 | Lb |
| DM-051 | A3 | S1 | D5 | C1 | T6 | I1 | La |
| DM-052 | A4 | S1 | D4 | C3 | T6 | I4 | Ld |
| DM-053 | A5 | S5 | D1 | C1 | T6 | I1 | La |
| DM-054 | A6 | S2 | D3 | C3 | T6 | I4 | La |
| DM-055 | A6 | S7 | D6 | C1 | T6 | I3 | Lc |
| DM-056 | A7 | S3 | D1 | C1 | T6 | I2 | Lb |
| DM-057 | A8 | S4 | D6 | C3 | T6 | I1 | Ld |

Codes: A1–A8 actor classes and T1–T6, La–Ld as defined in §5.6.2; S1–S7, D1–D6, C1–C3, I1–I4 as in §5.6.1. T1 rows rotate AppNAI → MedMaarg → EduVerse → OrganicSpec in order of appearance.

### 5.6.5 Reduction step 4: risk-based additions

Pairwise coverage finds two-factor faults. The highest-risk faults in this product need specific three- or four-factor combinations, so the following rows are **added** to the pairwise set (DM-R01…DM-R40). Combinations already present in the 57 pairwise rows were not duplicated.

| Risk rule | Combination added (other dimensions at baseline A1·S3·D1·C1·T1·I1·La unless stated) | Rows added | Risk retired | Source |
|---|---|---|---|---|
| RR-1 Tenant isolation | T5 cross-tenant × every actor class that can authenticate (A1–A6 on C1, C2, C3; A8 on C3) | 19 | Cross-scope disclosure or side effect (KPI-30 = 0) | B-TENANT, AP-10, NFR-032, BRL-TEN-03/04 |
| RR-2 Portfolio mutation | T3 portfolio × A1, A2 × C1, C2, C3 attempting a mutation | 6 | Mutation in aggregate scope | DEC-055, BRL-TEN-05 |
| RR-3 Dispatch certainty | A8 on C3 × {I4·D5·S3, I4·D5·S7, I3·D5·S3, I2·D6·S3} | 4 | Duplicate external effect; blind retry after uncertain outcome | NFR-005, NFR-026, DEC-050, E-4/E-5 |
| RR-4 Sensitive data | A7 × {C1, C2} × EduVerse under-18 without guardian (D4) and MedMaarg free text with clinical detail (D2) | 4 | Minor outreach; health data in acquisition | DEC-030, AP-05, BRL-ELG-13/14, BRL-PRV-06 |
| RR-5 Separation of duties | A3 × S2 on C2 (mobile approval screen) | 1 | Self-approval; over-limit approval from mobile | BRL-APR-01/04, DEC-043 |
| RR-6 Time boundaries | Lc DST × D3 boundary × S5 expired on C1; Ld UTC × D3 × S5 on C3 | 2 | Expiry or deadline evaluated in the wrong timezone | I18N-03, BRL-SRC-06, FR-DM-02 |
| RR-7 Flag OFF | T6 on C1 (A1) and on C3 (A8) | 2 | Disabled capability reachable through UI or API | RECOMMENDATION-005, NFR-037 |
| RR-8 Volume | D6 on C2 (A1) and on C3 (A8) | 2 | Timeouts, memory exhaustion, unbounded pages | DEC-018, NFR-015 cursor pagination |
| **Total** | | **40** | | |

**Representative combinations: 57 pairwise + 40 risk-based = 97 per full-dimension operation** (from 5,080,320 raw; a reduction of ≈ 99.998%). Role × permission is additionally covered exhaustively by the 670-cell RBAC table test [RECOMMENDATION-053].

### 5.6.6 How each story's AC apply the matrix

**Notation used by batches 5.2 and 5.3.** Those batches label each *dimension* by its row number in §5.6.1 (**D1** persona/role, **D2** permission level, **D3** object state, **D4** data condition, **D5** channel, **D6** tenant/config, **D7** integration availability, **D8** locale) and list raw values (e.g. "D6 T1/T2", meaning tenant fixtures 1 and 2 of the two-tenant set). Batch 5.1 uses the merged *value* codes (A1–A8, S1–S7, D1–D6 for data-condition values, C1–C3, T1–T6, I1–I4, La–Ld). Both notations map onto the same matrix; where "D1–D6" appears in a 5.1 dimension profile it always means data-condition values. Part 6 normalizes both to DM row IDs.

1. **Dimension profile.** Every story header lists the dimension values its AC exercise (e.g. `A1,A2,A3,A5 · S1–S3,S5 · D1–D5 · C1,C3 · T1(MedMaarg),T3,T5 · I1,I3 · La,Lc`). Dimensions that do not apply are marked n/a with a reason (e.g. "I n/a: no external dependency").
2. **Minimum AC set (MAS).** Every story's Gherkin contains at least:

| MAS item | Rule | Dimension values typically used |
|---|---|---|
| MAS-1 Happy path | Authorized actor, valid data, primary channel, owned startup, integration up | A1 or A2 · D1 · C1/C3 · T1 · I1 · La |
| MAS-2 Alternate path | A legitimate variant (another state, vertical, channel, or optional branch) | S-variant, T1 rotation, C2 |
| MAS-3 Negative path | A prohibited outcome with the **BRL rule cited** in a tag | Relevant S, D, T |
| MAS-4 Validation | Invalid, boundary or null input with the exact error (a `@val` scenario, or an `@edge` scenario tagged D2/D3/D4) | D2, D3, D4 |
| MAS-5 Permission / scope | **At least one explicit denial** (A5, A3, T5 or T3 mutation); the story's acceptance profile (CA-ADMIN, CA-PORTAL …) is inherited in addition | A3/A5/T3/T5 |
| MAS-6 Duplicate / idempotency | Required when the story writes through an idempotent API, webhook or outbox | D5 |
| MAS-7 Integration failure | Required when the story calls an adapter: I3 down and/or I4 uncertain | I2/I3/I4 |
| MAS-8 Locale / time | Required when the story stores or displays dates, deadlines or content locales | Lb/Lc/Ld |
| MAS-9 Volume | Required for lists, imports, exports, uploads and searches | D6 |

3. **Remaining rows go to Part 6.** The 97 DM rows that a story's MAS does not exercise are realized as Part 6 test cases (TC) for the FRs of that story, labelled with their DM row. A story is not Done until its MAS scenarios pass; Part 6 coverage reports track the DM rows per FR.

### 5.6.7 Covered, merged and excluded: summary by dimension value

| Dimension | Covered directly in story AC (MAS) | Merged (covered by rotation or class) | Excluded (with reason) |
|---|---|---|---|
| Role | R01–R12, R16–R20 as actor classes in their epics | R13, R14, R15 → A4/A5 classes; all 20 via 670-cell RBAC test | None |
| Permission | V, C, E, A, X, S, G (valid/expired) | Into A1–A8 | None |
| State | S1–S7 where the object has the state | — | States that the object's machine lacks (e.g. S7 for non-dispatch objects) |
| Data | D1–D6 per MAS | — | D6 for single-field settings with fixed size |
| Channel | C1, C2 (Website/Portal; Admin review screens), C3 | — | Native mobile (X-12); C2 for Admin configuration screens (DEC-043 desktop-first) |
| Tenant/config | T1–T6 | AppNAI/MedMaarg/EduVerse/OrganicSpec rotate within T1, plus RR-4 vertical rows and vertical stories | None |
| Integration | I1–I4 for adapter stories | — | Stories with no external dependency (n/a) |
| Locale | La, Lc, Ld; Lb in content stories | hi/ta/or rotate within Lb; New York/London within Lc | hi/ta/or for Admin UI (DEC-026); RTL (I18N-10) |

---

## 5.7 Story-writing conventions (recap, binding on batches 5.1–5.3)

### 5.7.1 Identifiers and fields

| Item | Convention |
|---|---|
| Epic ID | EP-01…EP-21, titles from Part 0 §0.10.2 / Part 1 §1.12.1 |
| Story ID | `US-<epic 2 digits><sequence 2 digits>` (e.g. US-0101) |
| AC ID | `AC-<story digits>-<2-digit seq>` (e.g. AC-0101-01); each `Scenario:` line starts with it |
| Story types | Feature · Enabler · Spike · Security · Accessibility · Observability · Data-migration · Compliance |
| Personas and roles | P01–P16 (Part 1 §1.8); R01–R20 (Part 2.3 §2.26.1) |
| Priority | MoSCoW ≤ the BR's priority (Part 1 §1.12.1) |
| Wave | = the FR's wave (Part 2.1); enablers may be earlier than their consumers, never later |
| Points | Fibonacci range ≤ 13 |
| Statement | "As a [persona (role)], I want [capability] so that [benefit]." Enablers and spikes: "As the [team/consuming epic], we need … so that …" |

### 5.7.2 Gherkin style

> **Erratum v1.2 (E-V-17):** superseded by promotional window 09:00–21:00 recipient local time unless a stricter rule pack applies (DEC-777). See Part 11.23c.


- One `Feature:` per story (= story title). `Background:` holds shared fixtures (tenant, startup, user, flags).
- Concrete data: INR amounts as Decimal with two places (`₹1,250.00`), ISO-8601 timestamps with offset (`2027-01-15T10:00:00+05:30`), quantities with units (`2 kg`), synthetic names and `example.com`/`.test` domains [ASSUMPTION-153].
- Default policy values come from Part 2.3 (e.g. quiet hours 09:00–19:00, frequency caps 2 per 7 days) and are parameters, not constants [ASSUMPTION-155].
- Denials assert the **status code, the error code and the absence of side effects** (no row, no outbox event, no provider call), and the audit event `outcome=denied` with the rule ID.
- Out-of-scope objects return a **uniform 404** (BRL-TEN-04) unless the AC says 403.

### 5.7.3 Scenario tags [RECOMMENDATION-051]

Each scenario has one tag line: a path tag and, where applicable, rule and DM tags.

| Tag | Meaning |
|---|---|
| `@happy` `@alt` `@neg` `@val` `@perm` `@edge` | Path type (MAS-1…MAS-5; edge for MAS-6…MAS-9) |
| `@sec` `@a11y` `@obs` | Security, accessibility, observability assertion |
| `@BRL-XXX-nn` / `@DEC-nnn` | The rule or decision the scenario enforces |
| `@DM-nnn` / `@DM-Rnn` | Matrix row realized by the scenario (optional in Part 5; mandatory in Part 6 TCs) |

Part 6 counts tags to report path coverage per story and DM-row coverage per FR.

### 5.7.4 Sprint 0 enablers and spikes in this batch

| Enabler / spike (task list) | Story | Epic |
|---|---|---|
| Identity compatibility spike, 12 checks (DEC-019) | US-0101 | EP-01 |
| AWS / IaC baseline (DEC-040, RECOMMENDATION-010) | US-0102 | EP-01 [ASSUMPTION-151] |
| CI pipeline skeleton (M09, DEC-063) | US-0103 | EP-01 [ASSUMPTION-151] |
| RLS framework (BRL-TEN-03) | US-0107 | EP-01 |
| Outbox framework (NFR-006, M06) | US-0110 | EP-01 |
| Seed synthetic data sets (RECOMMENDATION-017) | US-0113 | EP-01 |
| Feature-flag framework (RECOMMENDATION-005) | US-0117 | EP-01 |
| PDP skeleton (RECOMMENDATION-012) | US-0303 | EP-03 |
| Model gateway skeleton with eval harness (DEC-061) | US-0401, US-0402 | EP-04 |
| Data import for seed catalogues (DEC-039) | US-0208 | EP-02 |
| Data import for organizations, contacts and open deals (DEC-039) | US-0708 | EP-07 |

## Quality gate: Batch 5.1a (front matter)

| # | Check | Result | Notes and fixes applied |
|---|---|---|---|
| 1 | Every requirement traced to a source | **Pass** | DoR/DoD cite BRD §12.2 (BR-S136), DEC-005, DEC-018, DEC-043, DEC-061, RECOMMENDATION-001/-005/-011; matrix values cite Part 2.3, DEC-026, DEC-043, DEC-055, DEC-065 |
| 2 | Assumptions, gaps and conflicts tagged and logged | **Pass** | Tags used here: ASSUMPTION-150, -151, -152, -153, -155, -157, -158, -159; CONFLICT-130; RECOMMENDATION-050, -051, -053. Full register in file 1c §5.9.3 |
| 3 | IDs unique and consistent with earlier parts | **Pass** | Section numbers §5.1–§5.7 do not collide with batch 5.2 (§5.10+) or 5.3 (§5.30–§5.41); DM row IDs DM-001…057 and DM-R01…R40 are new |
| 4 | No story lacks AC; no requirement lacks a test | **N/A (front matter)** | Stories are in files 1b and 1c; the MAS (§5.6.6) defines the minimum AC per story |
| 5 | Negative, edge, security and accessibility cases covered | **Pass** | MAS-3/MAS-5 mandate negative and denial scenarios; RR-1…RR-8 risk rows; DoD D-5, D-9, D-10 |
| 6 | No agent lacks guardrail, fallback, KPI and cost | **N/A** | DoD D-11 requires the eval gate and cost ceiling for every AI story; agents in Part 7 |
| 7 | Time-sensitive facts flagged "verify" with as-of date | **Pass** | Tool versions (scanners, axe, flag library, IaC), all "verify at implementation (as of 27 Nov 2026)" |
| 8 | No restricted data routed to free-tier models | **Pass** | Restricted × Tier 2 kept only as a mandatory negative combination (§5.6.3); DoD D-11 |
| 9 | Consistent with earlier parts | **Pass** | Estimation basis 0.5/0.7/1.0 pd per SP shared with batches 5.2 and 5.3; velocity derived from DEC-005 |

**Self-review corrections:** (1) the first pairwise generator counted value pairs that no constrained row can contain; it was rebuilt to enumerate completable pairs only (594 pairs, 57 rows). (2) W0 and W1 loads in §5.5.3 were recomputed from the final story tables (35 W0 stories, 113.5 SP mid; 19 W1 stories, 54 SP mid). (3) US-0208 was removed from the W0-B list because FR-A103 imports are W1.

**Status: Part 5 Batch 5.1a complete (front matter §5.1–§5.7, binding on batches 5.1–5.3). Continue with Batch 5.1b (EP-01 to EP-04).**
