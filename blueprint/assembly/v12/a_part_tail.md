
---

## 11.1.4 Catalogue reconciliation

### 11.1.4.1 V12 inventory against the blueprint (business view)

| V12 inventory item (BRD 00, 01 §V12) | V12 count | Blueprint today | Reconciliation | Owner of detail |
|---|---|---|---|---|
| Sellable service SKUs | 39 (SM-SVC-01…39) | No SKU concept; 66 modules M01–M66, plan archetypes (DEC-047) | Adopted: 39 SKUs are the commercial unit (DEC-501, CONFLICT-767); SKU → module crosswalk §11.1.4.3 | Group B (service specs) |
| Included workflows | 156 (four per SKU, never sold separately) | WF-01…14 (Part 2.2) + WF-15…38 (Part 9.4) | Adopted as included contracts under the parent SKU (DEC-501); registry FR-V12-A-002 | Groups C/D |
| Steps | 517 (159 AI-inference steps) | Flow steps inside WF-01…38 | Recorded; step contracts by Groups C/D; AI steps by Group F | Groups C/D/F |
| Included foundations | 25 (SM-01-01…SM-14-05) | Platform modules M01–M09, M53–M58 | Included, never charged (DEC-501) | Group B |
| Logical engines | 15 (V12 adds subscription/bundle/entitlement, billing/metering/reconciliation, SaaS catalogue/service registry, platform operator administration, authorized portfolio command centre) | Module catalogue Part 2.1; SaaS module `saas` | Engines map to modules; new business rules here (FR-V12-A-010…035, 120…125) | Group E |
| Agent roles | 20 | AG-001…080 (Part 9.4) | Recorded; mapping by Group F | Group F |
| Website routes / Admin screens | 41 / 153 (W01–W41, A001–A131, X26–X39, O01–O08) | 34 W + 113 A + 71 added screens (W35–W44, A114–A149 etc.) | **ID collision** (same numbers, different meaning) → namespacing recommended (RECOMMENDATION-773); purpose of W01–W34 changes to a neutral storefront (CONFLICT-764) | Group G |
| Controlled requirements | 233 = 135 OPT + 40 MT + 18 MOB + 20 AIX + 20 CJ-R; plus 65 ENT and 10 BR-V12 | BR-M01…M66, BR-S001…S140, FR registers | This part maps every OPT, MT, MOB, BR-V3, BR-C, BR-V7, BR-V12 and BR-OBJ that appears in the assigned chapters (§11.1.4.4) | Groups A (business) + E/F/I (engineering detail) |
| Release KPIs / blocking | 35 / 21 | OKPI-01…35 (Part 8.3c §8.3.5.15.4) | V12 `KPI-nn` ≡ blueprint `OKPI-nn` (DEC-511); collision with Part 1 KPI-01…31 kept resolved by the existing OKPI rule | Group A |
| Data-ethics rules | 13 (CJ-GL-01…13) | BR-M18, M19, M56, M02, M16, M66, M04, M27, M28, M41, M25, M32, M10, M37, M48, M50, M31, M33, M35, M57, M51, M42, M43, M46, M36, M59, M60 | Covered (§11.1.4.6); non-relaxable by tenants (DEC-507) | Group A |
| Jurisdiction rules | 23 (IN 11, EU 10, UK 1, US 1) + 10 draft (US, UK, CA, AU, SG, AE, BR) | DEC-029 rule pack (IN, EU/EEA/UK, US, UAE, SG, AU) | Adopted with V12 market-opening rule (DEC-507, CONFLICT-766) | Groups A + I |
| API operations | 282 + 48 ENT | 579 operations | Group H | Group H |
| Database tables | 118 + 19 ENT | Part 3.3 / 3.6 entities | Group I | Group I |
| Locales | en, hi, de, fr, ar (RTL) | en-IN; hi/ta/or content W5 (DEC-026) | Adopted sequence (DEC-516, CONFLICT-777) | Groups A + G |

### 11.1.4.2 V12 ID families and their blueprint aliases

| V12 family (Appendix ID index and chapters) | Range in V12 | Blueprint treatment | Alias rule |
|---|---|---|---|
| Service SKU | SM-SVC-01…39 | New canonical ID | Kept literally; crosswalk to modules §11.1.4.3 |
| Workflow | SM-SVC-nn-WF01…04 (156) | New canonical ID | Kept literally; WF-01…38 remain blueprint flow IDs (Groups C/D map them) |
| Foundation | SM-01-01…SM-14-05 (25) | New | Kept literally (Group B) |
| Business requirement | BR-V3-01…14, BR-C01…15, BR-V7-AI-01…08, BR-V7-CJ-01…12, BR-V7-WEB-01…04, BR-V7-ADM-01…03, BR-V12-01…10, BR-OBJ-01…05 | New canonical BR IDs beside BR-M/BR-S | Kept literally; each mapped in A_coverage.csv and traced in §11.1.5.15 |
| Optimization | 135 OPT: AI-, GC-, SEC-, ST-, FL-, AT-, RT-, CV-, CS- (each 01…15) | Not present (the blueprint's OPT-01-01…OPT-20-04 come from source-pack document 36 and are a different family) | Kept literally with prefix in prose "V12 OPT AI-01"; acceptance IDs OPT-TC-{ID} aliased to TC-V12-A (§11.1.5.15) |
| Architecture | MT-01…40 | Not present | Kept literally; acceptance MT-TC-MT-nn aliased to TC-V12-A |
| Mobile | MOB-01…18 | Not present | Kept literally; acceptance MOB-nn-AT01 aliased |
| Jurisdiction rule | CJ-IN-01…11, CJ-EU-01…10, CJ-UK-01…03, CJ-US-01…04, CJ-CA-01, CJ-AU-01, CJ-SG-01, CJ-AE-01, CJ-BR-01, CJ-GL-01…13 | DEC-029 rule pack entries | Kept literally as rule-pack rule codes |
| Engineering requirement | AIX-01…20, CJ-R01…20 | FSD-level (Groups F and I) | Referenced only |
| Release KPI | KPI-01…35 | **OKPI-01…35** | Alias (collision with Part 1 KPI-01…31) |
| Enterprise requirement | ENT-IDN, ENT-ACC, ENT-API, ENT-DAT, ENT-INT, ENT-SEC, ENT-CMP, ENT-GLB, ENT-OPS, ENT-BIZ | Not present | Kept literally; BR-V12 → ENT trace in §11.1.5.13 |
| Reconciliation action | REC-01…30 (V10) and an older REC-01…12 series (chapter 25) | Not present | V10 series kept literally; the chapter 25 series is cited as **REC-V2-nn** (GAP-768) |
| Decision | DEC-V7-01…08, DEC-V9-01…04, DEC-V11-01…02, DEC-V12-01…07 (+180 inherited) | Blueprint DEC-001…422 | Kept literally as customer decision IDs; imported by DEC-518 (§11.1.4.8) |
| Prototype check | V8-QA-001…071 | Not present | Aliased to blueprint tests (§11.1.4.7) |
| Go-live, scenario, event | GO-01…08, XS-01…10, E-001…007 | GO-/XS- not present; E-001…007 present (Part 2.6) | Kept literally |
| Persona journey | P-01…06 | Personas P01…P16 (no hyphen) | Kept; P-0n journey ≠ P0n persona (mapping in A_coverage.csv chapter 04) |
| Change | C1…C8, D1…D15, CJ, AI, M1, A11Y, EVD | Not present | Recorded as history (Not applicable where prototype-only) |
| Website route / Admin screen | W01…W41 / A001…A131, X26…X39, O01…O08 | W01…W34 / A001…A113 plus 71 added | Collision; RECOMMENDATION-773 (Group G decides) |
| Roadmap phase | R0…R5 | Waves W0…W6, releases A1…A3 | Mapped by DEC-512 (ASSUMPTION-770) |

### 11.1.4.3 SKU crosswalk: SM-SVC-01…39 → blueprint modules, epics and release groups

V12 release groups (BRD 23 §V5): **Foundation**; **R1 intelligence** SVC 01–05, 25; **R2 engagement** SVC 06–13, 15–16; **R3 conversion** SVC 17–24, 29, 32–33; **R4 advanced** SVC 14, 26–28, 30–31, 34–39. "Blueprint wave" is where the underlying capability is already planned; "New" means the blueprint has no equivalent capability and Group B specifies it.

| SKU | V12 name (BRD 13–17) | V12 outcome (abridged) | Blueprint modules / features | Epic | Blueprint wave | V12 group | Coverage of capability |
|---|---|---|---|---|---|---|---|
| SM-SVC-01 | Market & Competitive Intelligence | Evidence-linked market signals, competitor updates, trend reports | M10, M11, M12, M59 | EP-05 | W1 | R1 | Covered |
| SM-SVC-02 | Global Business Opportunity Discovery | Evidence-linked opportunity records and alerts | M13, M14, M15, M16 | EP-05 | W1 | R1 | Covered |
| SM-SVC-03 | B2B Contact & Decision-Maker Intelligence | Verified contact candidates, role mapping, channel eligibility | M18, M19, M24 | EP-06 | W1 | R1 | Covered |
| SM-SVC-04 | Lead Qualification & Intelligent Matching | Qualified or held opportunities, fit explanation, assignment | M16, M17, M20 | EP-06 | W1 | R1 | Covered |
| SM-SVC-05 | CRM & Sales Pipeline | Shared CRM records, pipeline state, next-action queue | M21, M23 | EP-07 | W2 | R1 | Covered |
| SM-SVC-06 | Email Marketing & Outreach | Drafts, dispatch status, delivery evidence | M25, M26 | EP-08 | W2 | R2 | Covered |
| SM-SVC-07 | WhatsApp Business Marketing | Template decisions, message records, conversation updates | M31 | EP-10 | W3 | R2 | Covered |
| SM-SVC-08 | Omnichannel Follow-up & Lead Nurturing | Scheduled steps, drafts, paused sequences, handover | M28, M41 | EP-08 | W2–W3 | R2 | Covered |
| SM-SVC-09 | AI Chat, Unified Inbox & Objection | Intent, grounded response, shared timeline, escalation | M27, M32, M45 | EP-08, EP-10, EP-13 | W2–W4 | R2 | Covered |
| SM-SVC-10 | Meeting, Demo & Appointment | Appointments, briefings, reminders, tasks | M29, M40 | EP-09 | W2–W3 | R2 | Covered |
| SM-SVC-11 | Content Marketing | Calendar, drafts, verified claims, approval queue | M34, M02 | EP-11 | W3 | R2 | Covered |
| SM-SVC-12 | Social Media Publishing & Listening | Scheduled publications, provider status, permitted signals | M33, M35 | EP-05, EP-11 | W3 | R2 | Covered |
| SM-SVC-13 | SEO & Search Visibility | Issue backlog, keyword plan, optimization drafts | M36 | EP-11 | W3 | R2 | Covered |
| SM-SVC-14 | Paid Digital Advertising | Campaign configuration, spend alerts, conversion report | M39, M38 | EP-12 | W3 | R4 | Covered (V12 places it in R4) |
| SM-SVC-15 | Landing Page & Website Lead Intake | Page draft, versioned form, captured leads, routing health | M22, M37; **tenant-property publication** (DEC-505) | EP-07, EP-12 | W2–W3 | R2 | Covered; publication moves to client property |
| SM-SVC-16 | Webinar, Event & Referral Acquisition | Registrations, reminders, attendance follow-up, referrals | M40, M42 | EP-09, EP-12 | W3 | R2 | Covered |
| SM-SVC-17 | Proposal & Quotation | Proposal and calculated quote with revision, approval, validity | M43, M44 | EP-13 | W4 | R3 | Covered |
| SM-SVC-18 | Negotiation, Contract & MoU | Notes, contract draft, approved agreement, signature status | M45, M46 | EP-13 | W4 | R3 | Covered |
| SM-SVC-19 | Tender & Project Bid | Bid/no-bid, draft response, submission and deadline tasks | WF-08, A104 (submission human-only, DEC-053) | EP-14 | W4 | R3 | Covered |
| SM-SVC-20 | Sales Order & Fulfillment | Order drafts, validated totals, milestones, acceptance | WF-10, A105 | EP-14 | W4 | R3 | Covered |
| SM-SVC-21 | Payment, Invoice & Reconciliation | Matched balances, discrepancy queue, verified closure | M47, M52 | EP-15 | W4–W5 | R3 | Covered |
| SM-SVC-22 | Customer, Partner & Institutional Onboarding | Plan, milestones, pilot readiness, handover | M48, M49 | EP-16 | W4 | R3 | Covered |
| SM-SVC-23 | Customer Retention, Renewal & Feedback | Renewal tasks, feedback insights, re-engagement | M50, M51 | EP-16 | W5 | R3 | Covered |
| SM-SVC-24 | Revenue, Attribution & Sales Forecast | Dashboards, attribution, forecast scenarios | M52, M60, M30 | EP-15, EP-17 | W5 | R3 | Covered |
| SM-SVC-25 | Business Document & Knowledge Intelligence | Versioned knowledge, metadata, drafts, expiry reminders | M02, M03 | EP-02 | W0 | R1 | Covered |
| SM-SVC-26 | AI Voice & Intelligent Telephony | Call disposition, call event or hold, booking, summary | None (calls are human tasks, Part 9.8) | — | — | R4 | **New** (Group B); TRAI 140/160 series rule CJ-IN-07 (FR-V12-A-133) |
| SM-SVC-27 | Multimodal Creative & Localization | Image and video drafts, localized asset, creative QA | M34 (text only) | EP-11 | — | R4 | **New** (Group B) |
| SM-SVC-28 | Agentic Commerce & AI-to-AI Transaction | Machine-readable catalog, authorized quote exchange, mandate-linked decision | None | — | — | R4 | **New** (Group B); mandates limited by CONFLICT-762 |
| SM-SVC-29 | ABM & Enterprise Buying Group | Account plan, buying group map, progression | Part 9.8 ABM (WF-25) | EP-12 | A1–A2 | R3 | Covered (advanced) |
| SM-SVC-30 | Conversion Rate Optimization & Experimentation | Funnel report, experiment record, personalization decision | M37 experiments; Part 9.8 experiments | EP-12 | W3, A1 | R4 | Partially (Group B) |
| SM-SVC-31 | Marketplace & E-commerce Channel Operations | Listing state, availability, order event ledger, reconciliation | None (OrganicSpec orders are direct, DEC-045) | — | — | R4 | **New** (Group B) |
| SM-SVC-32 | Partner, Distributor & Co-Selling | Shortlist, enablement, deal registration, partner performance | M42, M49; Part 9.8 partner portal | EP-16 | W4, A1 | R3 | Covered |
| SM-SVC-33 | Customer Service & Support Operations | Support case, resolution or handover, SLA exception | Platform support (Part 4.45) is operator-side only | — | — | R3 | **New** as subscriber service (Group B) |
| SM-SVC-34 | Product-Led Growth & Usage Intelligence | Usage scorecard, activation journey, expansion and upgrade recommendations | Part 8.3c service report; Part 9.8 expansion | EP-16 | A1 | R4 | Partially (Group B) |
| SM-SVC-35 | Brand Reputation & Review Intelligence | Review queue, response draft, incident alert, improvement plan | M33 (listening) | EP-05 | — | R4 | Partially (Group B) |
| SM-SVC-36 | AI Sales Enablement & Coaching | Playbook, practice report, coaching feedback, training plan | Part 9.8 enablement hub | EP-16 | A1–A2 | R4 | Partially; coaching never used for employment decisions (BRD 15) |
| SM-SVC-37 | Pricing, Offer & Revenue Optimization | Profitability, scenarios, pricing experiment, exceptions | M44 price books (AI never sets prices) | EP-13 | — | R4 | Partially; outputs are recommendations only (safety invariant) |
| SM-SVC-38 | SMS, RCS & Business Messaging | Eligibility decision, delivery event, control report | DLT SMS rules (Part 4.1) | EP-08 | — | R4 | **New** channel (Group B) |
| SM-SVC-39 | Procurement & Supplier Management | Supplier shortlist, quotation comparison, PO, supplier performance | OrganicSpec payables (BRD §11), W16 supplier registration, A105 | EP-14 | W4 | R4 | Partially (Group B) |

Summary: 25 SKUs map to capabilities already planned in W0–W5, 6 to advanced releases or partial capabilities, and 8 are new capabilities whose specification and costing belong to Group B (Part 11.2). Business rules that apply to all 39 (entitlement, meter, first value, acceptance) are in Part 11.1b.

### 11.1.4.4 V12 optimization requirements (135 OPT) in the assigned chapters

| Family (V12 dimension) | IDs in assigned chapters | Covered | Partial | Not covered | Conflict | Main blueprint locations | Enhancements |
|---|---|---|---|---|---|---|---|
| AI- AI cost optimization | AI-01…15 (ch 11) | 12 | 3 | 0 | 0 | Part 7.3 routing, cache, evaluation, caps; DEC-418 tier order | FR-V12-A-113 (context budget, summarisation, multimodal tiers); detail Group F |
| GC- general cost | GC-01…15 (ch 06, 11) | 12 | 3 | 0 | 0 | Part 3.1, Part 4.2, Part 8.4, DEC-421 | FR-V12-A-023, 165 |
| SEC- application security | SEC-01…15 (ch 07, 20) | 14 | 1 | 0 | 0 | Part 4.1, Part 4.4a | FR-V12-A-096 |
| ST- stability | ST-01…15 (ch 21) | 15 | 0 | 0 | 0 | Part 4.2, 4.3, 4.4a | — |
| FL- AI flow automation | FL-01…15 (ch 07, 18) | 9 | 5 | 0 | 1 (FL-09) | DEC-051, outbox, A109–A113 | FR-V12-A-002, 094, 112 |
| AT- customer attraction | AT-01…15 (ch 05, 12) | 4 | 10 | 0 | 1 (AT-13) | W07, W08, W20, cookie consent | FR-V12-A-050…061, 073 |
| RT- retention | RT-01…15 (ch 10, 17) | 2 | 12 | 1 (RT-11) | 0 | CSO-08/09, Part 9.8 QBR | FR-V12-A-015, 016, 160…170 |
| CV- conversion | CV-01…15 (ch 07, 10, 11, 12) | 7 | 8 | 0 | 0 | W18, DEC-022/023/024 | FR-V12-A-017, 030, 056…060, 091 |
| CS- satisfaction | CS-01…15 (ch 11, 17, 20, 21, 22) | 8 | 6 | 1 (CS-14) | 0 | A110, A084, Part 2.4 §2.30 | FR-V12-A-034, 142, 153, 166…169 |

All 135 V12 OPT IDs appear in the assigned chapters: the parser found 15 distinct IDs in each of the nine families across chapters 05–22 (totals: 83 Covered, 48 Partially covered, 2 Not covered, 2 Conflict; ST and SEC are almost entirely covered by Parts 4.1–4.4, while the attraction and retention families carry most of the new business work). The 54 P0 / 76 P1 / 5 P2 split (BRD 01 §V5, 23 §V5) is adopted as the gating rule in FR-V12-A-191.

### 11.1.4.5 Release KPIs

V12 KPI-01…35 (BRD 22 §V9) are the same 35 rows, names, targets and gates as source-pack document 38, already registered in the blueprint as **OKPI-01…35** (Part 8.3c §8.3.5.15.4; mandatory flags Part 6.6). Every row is Covered except KPI-32 (growth critical RTO ≤ 120 min), which stays the open item of CONFLICT-462 and is now CONFLICT-765 because the customer has recorded product-owner approval (DEC-V11-01) while the platform-owner cost confirmation is still open. The 7 AI/compliance KPIs and the 12 business KPIs of chapter 22 are registered as KPI-V12-A-01…19 (Part 11.1b §11.1.5.11).

### 11.1.4.6 Data-ethics rules CJ-GL-01…13 → blueprint rules

| V12 rule | Inherited source (BRD 20) | Blueprint enforcement | Status |
|---|---|---|---|
| CJ-GL-01 Published professional channels only; no guessed emails | M18 | BR-M18; X-05; contact verification M19 | Covered |
| CJ-GL-02 Verified contact ≠ consent | M19 | BR-M19; eligibility M24 | Covered |
| CJ-GL-03 Deletion never re-enables outreach; hashed suppression | M56 | BRL-PRV-03 | Covered |
| CJ-GL-04 Planned/unavailable offerings not promoted, matched or quoted | M02, M16, M66 | DEC-060 readiness gate | Covered |
| CJ-GL-05 STOP/opt-out/reply cancels scoped follow-ups across channels | M04, M27, M28, M41 | BRL-SEQ-02; M41 routing | Covered |
| CJ-GL-06 Urgent/clinical enquiries to a human; no medical advice | M25, M27, M32 | X-02; website assistant guardrails | Covered |
| CJ-GL-07 No health targeting, no health events to ad pixels | M10, M37, M48, M50 | X-02; BRL-PRV-06 | Covered |
| CJ-GL-08 No private-group scraping or automated DMs | M31, M33, M35 | X-05 | Covered |
| CJ-GL-09 Complaints above threshold pause the campaign | M57 | KPI-18; M57 compliance monitoring | Covered |
| CJ-GL-10 No automatic re-contact after a lost deal without policy | M51 | M51 lost-deal rules | Covered |
| CJ-GL-11 Referral leads never enrol third parties without basis | M42 | BR-M42; DEC-046 | Covered |
| CJ-GL-12 AI never signs; only approved document versions shared, hash stored | M43, M46 | X-06; DEC-023 | Covered |
| CJ-GL-13 No fabricated rankings or forecasts presented as facts | M36, M59, M60 | KPI-29 labelled estimate; claim approval | Covered |

DEC-V9-03 makes these rules active for all markets and tenants and not relaxable by tenant configuration; DEC-507 adopts that wording (BRL tightening-only rule of DEC-038 already applies).

### 11.1.4.7 Prototype checks V8-QA-001…071 → blueprint behaviour and tests

| V8-QA checks | Behaviour | Blueprint requirement | Blueprint / new test |
|---|---|---|---|
| 001–002, 014–016, 029–031 | Cookie banner on first visit; choice persists; banner above mobile navigation | BR-V7-CJ-09; cookie consent before analytics (Part 4.1) | TC-V12-A-090 (+ existing EP-19 tests) |
| 003, 017, 032, 045, 059 | Every route renders a heading, no horizontal overflow | DEC-043; Part 2.5 responsive rules | TC-V12-A-091 |
| 004, 018, 033, 046, 060 | Unknown route → not-found view | BR-V7-WEB-01; BRL-TEN-10 | TC-V12-A-091 |
| 005–006, 019–020, 034–035 | Inline, announced field errors; invalid email and `javascript:` URL rejected | BR-V7-WEB-02; WCAG 2.2 AA | TC-V12-A-092 |
| 007, 021, 036 | Valid registration proceeds to the wizard | MT-08; FR-V12-A-090 | TC-V12-A-095 |
| 008, 022, 037 | HTML in business name rendered as text | SEC-11; output encoding | TC-V12-A-092 |
| 009, 023, 038 | Data-rights request: inline errors; EU erasure gets reference and one-month due date | BR-V7-CJ-05; FR-V12-A-053 | TC-V12-A-053 |
| 010–011, 024–025, 039–040 | AI transparency page; sample output carries AI disclosure | BR-V7-AI-01; FR-V12-A-054, 114 | TC-V12-A-054 |
| 012, 027, 042 | Skip link focus | WCAG 2.2 AA | TC-V12-A-092 |
| 013, 028, 043, 057, 071 | No runtime errors | Part 6.1 quality gates | TC-V12-A-091 |
| 026, 041 | Mobile menu lists all routes | MOB-02 | TC-V12-A-091 |
| 044, 058 | 143 screens × 4 personas: access counts per persona | RBAC R01–R20 (Part 2.3) | Group G / Group J |
| 047, 061 | Preflight: IN SMS allow/hold; EU undisclosed AI hold; IN WhatsApp without opt-in hold | BR-V7-CJ-02, 04; PDP; DEC-029 | TC-V12-A-131 |
| 048, 062 | Injection screen flags override, exfiltration, invisible characters | BR-V7-AI-06; SEC-08 | Part 6.4 injection suite |
| 049, 063 | Consent withdrawal holds queued run on that channel | REC-10; BR-V7-CJ-03 | Existing consent tests (EP-03) |
| 050, 064 | Requester cannot approve own run; Running → Reconciling → Completed | BR-V7-ADM-01, 02; BRL-APR-01; DEC-050 | Existing EP-18 tests |
| 051, 065 | Run drawer keyboard focus | WCAG 2.2 AA | TC-V12-A-092 |
| 052, 066 | Units 0 and 100001 rejected; over-allowance creates Held run | BRL-SVC-03; FR-V12-A-014 | TC-V12-A-014 |
| 053, 067 | Mixed currency: missing-rate records excluded and counted; negative rate rejected | MT-21; DEC-027 | TC-V12-A-036 |
| 054, 068 | Model promotion blocked without passing evaluation | BR-V7-AI-03; DEC-061 | Part 6.4 |
| 055, 069 | DSAR erasure under legal hold blocked with reason | BRL-PRV-04 | Existing EP-03 tests |
| 056, 070 | Template screen shows seeded searchable records | BR-V7-ADM-03 | Group G |

### 11.1.4.8 Customer decision register (V12 chapter 25) → blueprint

| Customer decision | Customer status | Blueprint position | Resulting blueprint decision |
|---|---|---|---|
| DEC-V12-01 Certification sequence (SOC 2 Type I R2 → Type II + ISO 27001 R3 → ISO 27701 + 42001 R4) | Proposed | Readiness only (CAP-X3-17, A2/A3) | DEC-513 — Pending Founder (CONFLICT-760) |
| DEC-V12-02 Okta, Entra ID, Google first; SCIM at R2 | Proposed | OIDC/SAML reuse of AppNAI identity (DEC-003/019); no SCIM | DEC-513 — Pending Founder (CONFLICT-760) |
| DEC-V12-03 SLA tiers 99.5 / 99.9 / 99.95% with credits | Open | SLA-02 99.5% (Starter/Growth), 99.9% Scale after scale gate; credits placeholder | DEC-510 (Standard/Business adopted as templates; Enterprise 99.95% Pending Founder) |
| DEC-V12-04 Locale sequence en + hi (R2), de + fr (R3), ar (R4) | Proposed | DEC-026 | DEC-516 (CONFLICT-777 adopted) |
| DEC-V12-05 US sales-tax and global tax provider before R5 | Open | GST engine (DEC-027) only | DEC-514 — Pending Founder (with EU/US region) |
| DEC-V12-06 Region order IN → EU → UK/ME/APAC → US | Open | ap-south-1 only (DEC-421) | DEC-514 — Pending Founder (CONFLICT-761) |
| DEC-V12-07 Additional jurisdiction packs need counsel review | Open | DEC-029 allowed some outbound in Year 1 | DEC-507 (CONFLICT-766 adopted) |
| DEC-V11-01 Approval evidence for DEC-V9-01/02 (28 Nov 2026) | Recorded; platform-owner cost confirmation open | — | DEC-518 records it; cost part DEC-515 Pending Founder |
| DEC-V11-02 V11 final controlled baseline | Approved 28 Nov 2026 | — | Superseded by V12 itself; recorded (DEC-518) |
| DEC-V9-01 Stricter recovery objectives | Approved per DEC-V11-01 | DEC-018 RPO 15 min / RTO 4 h; CONFLICT-462 | DEC-515 — Pending Founder (CONFLICT-765) |
| DEC-V9-02 Promoted retained specifications normative | Approved per DEC-V11-01 | Part 0B / 9.6 covered all 38 documents | Recorded (DEC-518) |
| DEC-V9-03 CJ-GL-01…13 active for all tenants | Active; legal wording pending | BR-M rules | DEC-507 |
| DEC-V9-04 Contact-data vendors only licensed, after transfer register and DPA | Open | Apollo reserve optional (DEC-004); open-source first | Recorded (DEC-518): vendor use stays behind DPA and CJ-GL-01 |
| DEC-V7-01 EU second market | Open — recommendation | DEC-029 | DEC-507 |
| DEC-V7-02 AI providers and models per tier | Open | Answered: DEC-418 (Claude Sonnet primary, tier order) | Recorded (DEC-518) |
| DEC-V7-03 One cloud with India and EU regions; managed Kubernetes | Open | DEC-421 (Vercel + Supabase + AWS Mumbai) | DEC-514 — Pending Founder |
| DEC-V7-04 Promotional window 09:00–21:00 recipient time; DSAR timeline | Open | Quiet hours per jurisdiction rule pack; BRL-PRV-02 | Recorded (DEC-518) |
| DEC-V7-05 DLT operator and scrubbing API | Open | DLT rules Part 4.1 | Recorded; selection stays open |
| DEC-V7-06 Evaluation thresholds (accuracy ≥ 90%, claims 100%, citations ≥ 95%, schema 100%) | Open | DEC-001; OKPI-13 schema ≥ 99.5% | Recorded; Group F reconciles the schema 100% vs 99.5% difference |
| DEC-V7-07 Tenant AI budget defaults (soft cap 80%, hard cap per plan) | Open | DEC-008 hard caps; M53 alerts | Recorded (DEC-518); 80% soft alert adopted in FR-V12-A-015 |
| DEC-V7-08 Region chosen at onboarding and fixed | Open — recommendation | India only | DEC-514 — Pending Founder |

### 11.1.4.9 The two REC series

Chapter 25 contains an older table whose rows are labelled "REC-01/05", "REC-02/03", "REC-04", "REC-06", "REC-07/08", "REC-09/11", "REC-10", "REC-12". Their meanings (for example "REC-10 Investment comparator not commercial functionality") differ from the V10 reconciliation actions REC-01…30 of the same document (for example "REC-10 consent withdrawal matches scoped contact"). The blueprint cites the older series as **REC-V2-01…12** to keep both resolvable [GAP-768]. All REC-V2 items are Covered: REC-V2-01/05 by CONFLICT-764 (neutral storefront), REC-V2-02/03 by DEC-501, REC-V2-04 by the 147-screen baseline, REC-V2-06 by DEC-022/023 and server identity, REC-V2-07/08 by Groups C/D, REC-V2-09/11 by Parts 3.5/3.6, REC-V2-10 by DEC-002/DEC-517, REC-V2-12 by Part 6 evidence rules.

*Part 11.1 continues in Part 11.1b: §11.1.5 Enhancements, §11.1.6 Conflicts, §11.1.7 Decisions, §11.1.8 Expert persona review, §11.1.9 Tags register, §11.1.10 Quality gate.*

**Status: Part 11 Batch 11.1a complete (review, coverage and catalogue reconciliation). Quality gate for the whole of Part 11.1 is in Part 11.1b §11.1.10.**
