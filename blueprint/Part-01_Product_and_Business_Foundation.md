# AI Growth Engine: Employee Sales & Marketing Automation
## Application Blueprint: PART 1, Product and Business Foundation

| Field | Value |
|---|---|
| Document | Application Blueprint, Part 1 of 10 |
| Version | 1.0 |
| Date | 27 Nov 2026 |
| Baseline inputs | BRD, FRD; Part 0 (inventory and registers); Part 0A (decisions DEC-001…DEC-065) |
| Roles applied | Product Owner (lead), Business Systems Analyst, Lead UX Designer, Security/Compliance, FinOps, Solutions Architect (review) |

**Conventions.** Source citations follow Part 0 §0.1.2 (e.g. "BRD §7", "FRD §16.2 A029"). Decisions are cited as `DEC-###`. Additions beyond the source are tagged `[RECOMMENDATION-###]` and, where already accepted, give the deciding DEC. All money figures are **estimates** in INR unless stated otherwise.

---

## 1.1 Executive summary (draft for the final document)

**What we are building.** The AI Growth Engine is an independently deployed, multi-tenant, configuration-driven platform. Employees of 25+ owned startups, and of independently onboarded client companies, use it to find, win, deliver and renew **commercial business**. It covers market and tender discovery, evidence-based qualification, compliant omnichannel outreach, content and campaigns, proposals and quotations, contracts, orders and fulfilment, verified payment closure, onboarding and renewal. Fundraising and investor activity are **out of scope** (BRD §1; DEC-002).

**Why.** Today each startup's growth work is manual, scattered across tools, and hard to govern. Leads are not qualified on evidence. Consent and opt-outs are not enforced across channels. AI use is uncontrolled in cost and claims. "Won" deals are not reconciled with cash. The platform replaces this with **one governed engine**: rules-first automation, AI that drafts and classifies but never commits the business, and outcome metrics tied to verified receipts (BRD §12.1, §13.1).

**For whom.** Founders and startup heads (portfolio oversight and approvals), growth, marketing, research, bid and order staff (daily operations), finance and legal (maker-checker), automation leads (workflow governance), tenant administrators, and external customers, suppliers, institutions and SaaS clients (website and portal) (BRD §2, §9).

**How.** Two React frontends (public Website/Portal; confidential Admin Command Centre with seven views) on a Django REST modular monolith. PostgreSQL with row-level security, Celery/Valkey workers, a transactional outbox, provider adapters and a model gateway with Claude as the primary model, all behind a single deterministic **Policy Decision Point** that rechecks scope, consent, jurisdiction, budget and approval hash at dispatch (BRD §1.2, §5; DEC-007, DEC-009; RECOMMENDATION-012).

**Delivery.** Seven waves over 180 days (W0–W5), with selective expansion to Day 365 (W6). Planning effort is **287–483 person-days (₹13.05–32.93 lakh)**, delivered by **4.0 engineering FTE + 0.5 growth/compliance** (DEC-005). Pilot run cost is **₹16,675/month** (₹31,165 with optional enrichment and developer seats), with an AI inference ceiling of **₹3,000/month** at pilot and gated increases (DEC-004, DEC-008).

**Success.** By Day 30: ≥ 100 reviewed signals at ≥ 80% precision. By Day 60: 20 qualified accounts and 5 demo requests (targets, not guarantees). By Day 120: a complete synthetic deal plus one real controlled pilot closed on verified evidence. By Day 180: a 30-day monitored pilot with zero sends to suppressed recipients, 100% revenue reconciliation and ≥ 99% workflow timeliness. By Day 365: a 26th startup onboarded from a template with no code change, and ≥ 2 isolated external tenants (BRD §8, §15).

**Key risks.** Regulatory exposure (DPDP, children's data, global outreach), the AI budget ceiling, provider dependence (Meta, AWS, search APIs), and team capacity. Each is mitigated by design decisions in Part 0A and tracked in the Part 8 risk register.

---

## 1.2 Vision, mission and product principles

### 1.2.1 Vision
> *Every startup in the portfolio, and every client business we serve, grows through verified, compliant, evidence-based commercial relationships, operated by a small team amplified by safe automation.*

### 1.2.2 Mission
Give employees one governed workspace that turns **permitted public evidence and inbound interest** into **qualified opportunities**, and those opportunities into **signed agreements, fulfilled obligations and reconciled receipts**. Automate every routine step that is safe to automate, and keep humans accountable for every consequential decision.

### 1.2.3 Product principles (binding design rules)

| # | Principle | Source | Implication for design |
|---|---|---|---|
| PP-01 | **Outcomes over activity.** Measure qualified opportunities, meetings, awards, fulfilment, receipts, renewals and margin, never AI or message volume | BRD §8 Business goal, §12.1, §17.1 | KPI catalogue (§1.4) excludes vanity metrics; dashboards show numerator, denominator and as-of |
| PP-02 | **Rules first, AI second.** Calculations, permissions, state transitions and eligibility are deterministic; AI only drafts, classifies, extracts, matches and summarizes | FRD OPT-10-01; BRD §5 | Policy Decision Point; model gateway with Tier 0 |
| PP-03 | **Fail closed.** Unknown eligibility, stale revision, missing approval, uncertain provider result → no action, an actionable reason, and a human task | FRD §12.2, §11.1 | Global UI states; reconciliation console |
| PP-04 | **Recheck at execution.** Permission, scope, consent, jurisdiction, budget and approved hash are revalidated at dispatch, not only at planning | BRD §1.2, §5, §16 | Dispatch guard in every worker |
| PP-05 | **Evidence and provenance.** Every actionable record carries a permitted source, date, licence/permission and confidence; inference is never labelled confirmed | M12, M15, FRD OPT-11-01 | Evidence entity and provenance UI |
| PP-06 | **Approved truth only.** Only approved offering, claim, price and content versions reach external audiences; planned products are never promoted | M02, M34, M66; DEC-060 | Immutable approved snapshots and hashes |
| PP-07 | **Independent by default.** Product, tenant and startup data, credentials, budgets, senders and backups are isolated; no live cross-product joins | BRD §1, §2 | RLS, composite keys, per-scope ledgers |
| PP-08 | **Simulate before you act.** Every automation can run as a dry run with zero live effects | BRD §1.2, B-AUTO | Simulation mode in the workflow engine |
| PP-09 | **Open-source first, paid by exception.** Paid services and fallbacks are disabled by default and need a scoped, approved budget | BRD §10, OPT-03-01 | Integration registry, feature flags, budgets |
| PP-10 | **Configuration, not code, per startup.** New standard startups and clients are onboarded with templates and typed configuration | BRD §1.1, §17.1, AP-01 | Template library, config change centre |
| PP-11 | **Privacy and safety by design.** No patient/clinical data, no targeting of minors, no private scraping, no guessed emails | BRD §5, §7 (M10, M18, M32, M48, M50), §15 | Data classification, jurisdiction rule pack (DEC-029, DEC-030) |
| PP-12 | **Every action is explainable and auditable.** Correlation ID, actor, policy revision, evidence and outcome for every decision | BRD §5, FRD §5 | Append-only audit; A009, A110 |

---

## 1.3 Problem statement

### 1.3.1 Core problem
The owner runs a growing portfolio of startups with very different commercial models: global AI project bidding, institutional healthcare partnerships, education programmes and agricultural trade. Each needs continuous market discovery, compliant outreach, follow-up, quotation, contracting, fulfilment and collection, with a very small team. Without a governed engine:

| # | Problem | Who feels it | Consequence | Requirement response |
|---|---|---|---|---|
| PR-01 | Opportunity discovery is manual and unstructured; signals lack evidence and freshness | Research analysts, growth managers | Missed tenders and partnerships; time spent on poor-fit accounts | M10–M17, WF-02 |
| PR-02 | Contact data is unverified or improperly sourced; consent is not tracked | Growth managers, legal | Legal exposure (DPDP, TRAI, GDPR/CAN-SPAM), sender reputation damage | M04, M18, M19, M24, DEC-029 |
| PR-03 | Outreach and follow-up continue after replies, opt-outs or complaints | Prospects, compliance | Complaints, blocked channels, brand harm | M27, M28, M41, M57 |
| PR-04 | AI content can invent claims, relationships or diagnoses; AI spend is uncontrolled | Founder, compliance, finance | False claims, regulatory risk, runaway cost | M08, M25, M34, M53, DEC-007, DEC-008 |
| PR-05 | Proposals, quotes and discounts are inconsistent and unapproved; totals are miscalculated | Finance, startup heads | Margin leakage, disputes | M43, M44, M45, DEC-038 |
| PR-06 | "Won" is declared without signed contract or payment; revenue double-counted | Founder, finance | Misleading reporting and decisions | M46, M47, M52, DEC-054 |
| PR-07 | Each startup runs separate tools and spreadsheets; portfolio view is impossible without data mixing | Founder | No reliable oversight; confidentiality breaches | M61, B-TENANT, DEC-055, DEC-065 |
| PR-08 | Onboarding a new startup or client requires custom development | Founder, engineering | Slow expansion, high cost | B-TENANT, B-SVC, AP-01, AP-07 |
| PR-09 | Vertical-specific obligations (tender deadlines, child safety, clinical boundaries, trade units and ledgers) are not enforced | Vertical leads | Disqualified bids, safety incidents, reconciliation errors | BRD §4, §11; FRD §12.1 |
| PR-10 | No way to offer the capability to external businesses as a governed SaaS | Service owner | Lost revenue opportunity | B-SVC, W31–W34, A101 |

### 1.3.2 Problem statement (formal)
> **For** founders, startup leaders and growth employees operating multiple businesses with small teams,
> **who** must find and convert commercial opportunities across very different markets while staying compliant and within a tight budget,
> **the AI Growth Engine is** a governed, multi-tenant commercial operations platform
> **that** discovers permitted evidence, qualifies opportunities, automates safe outreach and follow-up, controls quotes, contracts and closure, and reports only verified outcomes.
> **Unlike** generic CRMs and marketing automation tools that optimize message volume and leave governance to the user,
> **our product** enforces consent, claims, budget and approval at execution, isolates every tenant and startup, and keeps AI from committing the business.

---

## 1.4 Goals, KPIs and OKRs

### 1.4.1 Business goals

| ID | Goal | Measured by | Source |
|---|---|---|---|
| G-01 | Increase **qualified** opportunities per startup, not contact volume | KPI-01, KPI-07, KPI-22 | BRD §8 Business goal |
| G-02 | Convert qualified opportunities into meetings, awards and signed agreements | KPI-06, KPI-09, KPI-11 | BRD §4 KPIs |
| G-03 | Close only on verified evidence and reconcile all receipts and payables | KPI-13, KPI-14, KPI-31 | M47, M52, BRD §13.1 |
| G-04 | Retain and renew customers with eligible, relevant engagement | KPI-15 | M50 |
| G-05 | Operate with zero unlawful or unwanted contact | KPI-17, KPI-18 | M04, M24, M57 |
| G-06 | Keep acquisition and AI cost per outcome falling while quality holds | KPI-10, KPI-21, KPI-22 | M53, OPT-10-01, OPT-12-04 |
| G-07 | Onboard new startups and clients by configuration, without code | KPI-25, AP-01 | BRD §17.1 |
| G-08 | Run SaaS clients profitably with isolation and portability | KPI-23, KPI-24 | OPT-20-01…04 |
| G-09 | Automate the routine; keep humans on consequential decisions | KPI-19, KPI-20 | OPT-04-08 |
| G-10 | Zero cross-scope data disclosure | KPI-30 | B-TENANT, NFR-032 |

### 1.4.2 KPI catalogue (definitions, formulas, targets)

Rules for every KPI (BRD §12.1, §13.1; FRD §2): count **distinct** de-duplicated records in the selected scope; display **numerator, denominator, as-of time and original currency**; **Unknown ≠ 0**; forecasts are labelled *estimate* and never mixed with actuals.

| KPI | Name | Formula | Target (source / decision) | Frequency | Owner | Data source |
|---|---|---|---|---|---|---|
| KPI-01 | Qualification precision | accepted-as-qualified ÷ AI/rule-proposed qualified (human-reviewed, same period) | **≥ 90%** on benchmark before L2/L3 (DEC-001) | Weekly | AI lead | Review (A027) |
| KPI-02 | Signal precision | correct signals ÷ reviewed signals | **≥ 80%** on ≥ 100 reviewed (M14; DEC-001) | Weekly (W1), then monthly | Research lead | A019 |
| KPI-03 | Verified contact rate | contacts with verified professional channel ÷ contacts discovered | Baseline in W1; **+10 pp by W5** [RECOMMENDATION-019] | Monthly | Research lead | A025 |
| KPI-04 | Eligible delivery rate | delivered ÷ eligible approved sends | **≥ 97%** [RECOMMENDATION-019] | Weekly | Growth lead | A037 |
| KPI-05 | Eligible reply rate | substantive replies ÷ eligible delivered first-touch messages | Baseline in W2; improve vs baseline (OPT-12-04) | Weekly | Growth lead | M27 intents |
| KPI-06 | Meetings held | count of meetings with attended status (not booked) | 5 demo requests by Day 60 (BRD §8) | Weekly | Growth manager | A040 |
| KPI-07 | Qualified accounts | distinct organizations with verified need, offering fit, eligible contact and owner | **20 by Day 60** (BRD §8; target, not guarantee) | Weekly | Product owner | A027/A029 |
| KPI-08 | Reviewed signals | count reviewed (accepted + rejected) | **100 by Day 30** (BRD §8) | Weekly | Research lead | A019 |
| KPI-09 | Win rate | won ÷ (won + lost) closed in period, per route | Baseline by W5 | Monthly | Startup head | A029 |
| KPI-10 | Acquisition spend per new customer | attributable acquisition cost (ads + provider + AI + tooling allocation) ÷ new customers with verified closure | Falling quarter on quarter (OPT-12-04) | Monthly | FinOps | A082/A012 |
| KPI-11 | Bid award rate (AppNAI) | awarded bids ÷ submitted bids | Baseline; track | Monthly | Bid manager | A104 |
| KPI-12 | Fulfilment accuracy (OrganicSpec etc.) | orders fully accepted without quantity/price discrepancy ÷ orders delivered | **≥ 98%** [RECOMMENDATION-019] | Monthly | Order coordinator | A105 |
| KPI-13 | Actual receipts | Σ reconciled customer receipts by issuer and currency | Reconciled 100% (M52) | Monthly | Finance | A074 |
| KPI-14 | Payables | Σ verified payables by state (due/settled) | 100% matched to fulfilment (BRD §11) | Monthly | Finance | A105/A074 |
| KPI-15 | Renewal rate | renewed ÷ due for renewal (period) | Baseline; track | Quarterly | Startup head | A079 |
| KPI-16 | Gross margin | (recognized revenue − attributable direct cost) ÷ recognized revenue | Per startup floor (default 25%, DEC-038) | Monthly | Finance | A083 |
| KPI-17 | Suppression breaches | sends to suppressed/ineligible recipients | **0** (OPT-04-03) | Continuous | Compliance | A047 |
| KPI-18 | Complaint rate | complaints ÷ delivered (per channel) | **< 0.1%** email [RECOMMENDATION-019; verify provider thresholds] | Weekly | Compliance | A047 |
| KPI-19 | Automation rate | automated eligible steps ÷ eligible steps | **≥ 90%** (OPT-04-08) | Monthly | Automation lead | A110 |
| KPI-20 | Workflow timeliness | eligible due runs started within window ÷ due runs | **≥ 99%** (OPT-04-07; DEC-032) | Daily | SRE | A110 |
| KPI-21 | AI cost per task | AI spend ÷ completed AI tasks, per agent | Within agent budget (Part 7) | Daily | FinOps | A012 |
| KPI-22 | Cost per qualified opportunity | (AI + data + channel + allocated infra) ÷ qualified opportunities | Falling vs baseline (BRD §8 scale gate) | Monthly | FinOps | A012/A082 |
| KPI-23 | SaaS contribution margin per tenant | service revenue − attributable/allocated delivery cost | Positive by W6 (OPT-20-01) | Monthly | Service owner | A101 |
| KPI-24 | Usage reconciliation | reconciled metered usage ÷ total metered usage | **100%** (OPT-20-02) | Per billing cycle | Service owner | A101 |
| KPI-25 | Standard onboarding time | time from approved application to active workspace | **≤ 1 business day** [RECOMMENDATION-019] | Per onboarding | Service owner | A099 |
| KPI-26 | Public qualified enquiries / portal completion | qualified public enquiries; completed portal tasks ÷ started | Measured independently of Admin pipeline (BRD §9.1) | Weekly | Product owner | A108 |
| KPI-27 | Source coverage | approved sources monitored ÷ registry by country/sector; restricted and not-covered shown | Visible 100% (BRD §12.1) | Monthly | Research lead | A010 |
| KPI-28 | Objection resolution | resolved ÷ raised; median elapsed time | Better than baseline (OPT-12-02) | Monthly | Growth lead | A069 |
| KPI-29 | Forecast error (estimate) | MAPE of forecast vs verified actuals | Reported, labelled estimate (M60) | Monthly | Startup head | A087 |
| KPI-30 | Cross-scope disclosure incidents | confirmed cross-tenant/startup exposures | **0** (B-TENANT) | Continuous | Security | A047/A014 |
| KPI-31 | Closure integrity | deals in Won without route-required evidence | **0** (M47) | Continuous | Finance | A073 |

### 1.4.3 OKRs by horizon

| Horizon | Objective | Key results | Source |
|---|---|---|---|
| **Day 1–30 (W0–W1)** | **O1. Stand up a trustworthy, compliant intelligence foundation** | KR1.1 W0 controls (M01–M09, M53, M56, M58) tested and owner/claims sign-off recorded · KR1.2 ≥ 100 reviewed signals at ≥ 80% precision · KR1.3 0 prohibited sources fetched; 100% evidence provenance · KR1.4 AI spend ≤ ₹3,000 with hard cap proven in test | BRD §8 Day 1–30; DEC-001, DEC-008 |
| **Day 31–90 (W2–W3)** | **O2. Turn intelligence and inbound interest into a qualified, compliant pipeline across channels** | KR2.1 20 qualified accounts and 5 demo requests (targets) · KR2.2 0 sends to suppressed/ineligible recipients; STOP and replay tests pass on email, WhatsApp and web · KR2.3 ≥ 99% of transactional runs within 15 min · KR2.4 approved public sites live for 4 seed startups with 0 draft/private exposure | BRD §8 Day 31–90; B-WEB |
| **Day 91–180 (W4–W5)** | **O3. Close only verified business and prove it end to end** | KR3.1 full synthetic deal + 1 real controlled pilot closed on verified contract/payment evidence · KR3.2 100% of receipts reconciled; 0 duplicate revenue · KR3.3 30-day monitored pilot passes budget and compliance gates · KR3.4 qualification precision ≥ 90% enables Supervised mode for ≥ 1 workflow | BRD §8 Day 91–180; M47, M52 |
| **Day 181–365 (W6)** | **O4. Scale selectively and open the platform to clients** | KR4.1 26th startup onboarded by template with no code change · KR4.2 ≥ 2 external tenants provisioned, metered, invoiced and exported independently · KR4.3 positive contribution margin per active tenant · KR4.4 insurer/API/phygital pilots only after readiness approval | BRD §8 Day 181–365, §15; B-SVC |

---

## 1.5 Scope

### 1.5.1 In scope

| Area | In scope (summary) | Source |
|---|---|---|
| Tenancy and configuration | Owner Portfolio Tenant with 25+ startup workspaces; independent external SaaS tenants; templates; capability profiles; configuration change control | BRD §1, §17; DEC-065 |
| Identity reuse | Reuse existing identity/security under a new product audience; RBAC/ABAC; MFA for privileged roles; scoped support access | M01; DEC-003, DEC-019, DEC-056 |
| Product truth | Offerings, capabilities, claims, price versions, readiness gates; knowledge documents with approval and citations | M02, M03, M66 |
| Governance | Consent, suppression, privacy requests, retention, compliance monitoring, jurisdiction rules, approval policies | M04, M24, M56, M57; DEC-028–030, DEC-038 |
| Intelligence | Source permissions, search planning, permitted public discovery, evidence extraction, accounts, signals, needs, matching, scoring, roles/contacts, verification, research review, social listening, competitor watch | M07, M10–M20, M33, M59 |
| Relationship management | CRM pipeline, lead capture, Customer 360, assignments | M21–M23 |
| Engagement | Eligibility, drafting, email, inbound processing, sequences, meetings, WhatsApp, web assistant, omnichannel routing | M24–M29, M31, M32, M41 |
| Marketing | Content studio, claims approval, social publishing, SEO, landing pages, attribution, campaigns, paid ads, webinars, referrals | M34–M40, M42 |
| Commercial conversion | Proposals, quotations, negotiation/objections, contracts/MoUs, bids/tenders, orders/fulfilment, payments and closure | M43–M47; A104, A105 |
| Post-sale | Onboarding/handoff, partner deployment, retention/renewal, lost-deal feedback | M48–M51 |
| Analytics | Growth and management dashboards, revenue and attribution, forecast (labelled estimate), Command Centre | M30, M52, M60, M61 |
| Automation | Workflow engine, autonomy modes, simulation, triggers, live monitor, conflict resolution, template/node library, emergency stop | M55, B-AUTO, A102, A109–A113 |
| AI | Model gateway, evaluation, cost control, Copilot (read-only, drafts), AI quality loop | M08, M53, M54; DEC-007, DEC-035 |
| Public web and portal | Approved websites per startup, enquiry forms, chat, booking, events, referrals, customer portal (quotes, agreements, orders, invoices, onboarding, support, preferences), SaaS client journey | B-WEB, W01–W34 |
| SaaS service | Plans, entitlements, metering, invoicing, suspension, import/export, offboarding | B-SVC, A101, A103 |
| Operations | DevSecOps, observability, release readiness, restore and rollback | M09, M58, M62 |
| Expansion pilots | Insurance institutional pilot, technology licensing, phygital expansion, future product launch gating | M63–M66 |

### 1.5.2 Out of scope (Won't, permanently for this product)

| # | Exclusion | Source |
|---|---|---|
| X-01 | Investor discovery, fundraising rounds, securities offers, cap table, investor data room, capital receipt processing | BRD §1; DEC-002 |
| X-02 | Patient/clinical records, diagnosis, medical advice, health data in marketing, ads or scoring | BRD §5, M32, M37, M48, M50 |
| X-03 | Insurance underwriting, eligibility, premium decisions, individual health profiling | M63, BRD §8 |
| X-04 | Direct targeting, profiling or advertising to minors | BRD §5, §15; DEC-030 |
| X-05 | Private scraping, private group scraping, restricted social profiles, automated social DMs, guessed emails | M18, M31, M33, M35 |
| X-06 | Autonomous money movement, AI signing contracts, AI making binding offers or discounts | BRD §2, §5, M46 |
| X-07 | Unauthorized tender-portal submission (automated submission of any kind) | BRD §5; DEC-053 |
| X-08 | Live cross-product joins or automatic data sharing with the investor product | BRD §1 |
| X-09 | Enterprise CRM purchase/integration (deferred by build/buy decision) | BRD §8 Build/buy |
| X-10 | Paid automation wrappers (Zapier/Make etc.) as runtime dependencies | BRD §10, FRD §6 M06 |
| X-11 | General ledger, payroll, HR, statutory accounting replacement | [ASSUMPTION; DEC-027] |
| X-12 | Native mobile applications | DEC-043 |

### 1.5.3 Later (deferred, not excluded)

| # | Deferred item | Earliest | Trigger to start |
|---|---|---|---|
| L-01 | Statutory GST e-invoice (IRN) integration | W6+ | A startup crosses the e-invoicing threshold and wants automation (DEC-027) |
| L-02 | International payment gateway (e.g. Stripe) | W6 | AppNAI international award requiring card/wire collection (DEC-022) |
| L-03 | Microsoft 365 calendar | W5 | First user requiring it (DEC-024) |
| L-04 | Regional-language UI chrome (beyond content locales) | W6+ | Measured demand (DEC-026) |
| L-05 | Warehouse/lot/batch inventory | W6+ | OrganicSpec volume threshold (DEC-045) |
| L-06 | Referral commission payouts | W6+ | Partner programme scale (DEC-046) |
| L-07 | Multi-region active-active hosting | Post-365 | Availability need above 99.9% (DEC-018) |
| L-08 | Public SaaS price list and self-serve checkout | W6 | Service Owner approval (DEC-047) |
| L-09 | Paid enrichment (Apollo or equivalent) as default | Scale gate | BRD §8 scale gate passes (B08) |

---

## 1.6 Release structure: delivery waves and MoSCoW

### 1.6.1 Wave plan (DEC-006, DEC-034, DEC-060–063)

| Wave | Days | Planning label | Theme | Business requirements delivered | Exit gate (source) |
|---|---|---|---|---|---|
| **W0** | 1–15 | Release 1 | Foundation and governance | M01, M02 (+ M66 readiness gate), M03, M04, M05, M06, M07, M08 (+ M54 eval harness), M09 (+ M62 pipeline), M53, M56, M58; B-TENANT core; M61 shell | Controls tested; owner and claims sign-off (BRD §8) |
| **W1** | 16–30 | Release 1 | Intelligence pilot | M10–M20 | 100 reviewed signals; precision ≥ 80% |
| **W2** | 31–60 | Release 1 | Sales foundation | M21–M30, M55; B-AUTO (Manual/Assisted/Supervised, simulation, stop); B-WEB core (W01–W05, W12–W13, W21–W22, W29–W30, A107–A108) | 20 qualified accounts, 5 demo requests (targets) |
| **W3** | 61–90 | Release 1 | Omnichannel and marketing | M31, M32, M33, M34, M35, M36, M37, M38, M39, M40, M41, M42, M57; B-WEB remainder | Channel opt-out and replay tests pass |
| **W4** | 91–120 | Release 2 | Commercial closure | M43–M51; A104, A105 (bids, orders, fulfilment); W14–W16, W23–W28 | Full synthetic deal + real controlled pilot |
| **W5** | 121–180 | Release 2 | Optimization and SaaS readiness | M52, M54 (feedback loop), M59, M60, M61 (complete), M62 (full E2E); B-AUTO Controlled Autonomous; B-SVC (W31–W34, A100, A101, A103) | 30-day monitored pilot; budget and compliance gates |
| **W6** | 181–365 | Future | Selective expansion | M63, M64, M65, M66 (launch workflow); later items L-01…L-09 as triggered | Validated contract and market-fit milestones |

### 1.6.2 MoSCoW summary

| Priority | Count of primary BRs | Share | Rationale |
|---|---|---|---|
| **Must** | 50 | 70% | High because ~40% of Musts are **safety, compliance and integrity controls** that cannot be descoped without violating the BRD's activation conditions (BRD §11, §12) |
| **Should** | 12 | 17% | Valuable channel and lifecycle features; first to slip into W6 if capacity is short (DEC-005) |
| **Could** | 9 | 13% | Expansion and optimization features with lower immediate value or high external dependency |
| **Won't (this product)** | X-01…X-12 | n/a | Section 1.5.2 |

The Must share is above the usual 60% guidance. **Mitigation:** effort-weighted, Musts are ≈ 62% of estimated person-days (controls are small modules), and the Should/Could buffer (≈ 38% of effort) is the planned contingency (Part 8).

---

## 1.7 Stakeholders

| ID | Stakeholder | Type | Interest | Influence | Key needs | Engagement |
|---|---|---|---|---|---|---|
| SH-01 | Founder / CTO (sponsor, Product Owner) | Internal, accountable | Very high | Very high | Portfolio growth, governance, cost control, approvals | Sprint reviews, approvals, wave gates |
| SH-02 | Startup heads: AppNAI, MedMaarg, EduVerse, OrganicSpec | Internal | High | High | Vertical workflows, pipeline, approvals | Vertical UAT, policy configuration |
| SH-03 | Growth, research, marketing, bid and order staff | Internal users | High | Medium | Productive daily workspace, fewer manual steps | Usability tests, UAT, training |
| SH-04 | Finance (maker/checker) | Internal | High | High | Accurate quotes, invoices, reconciliation, no false revenue | UAT of closure and reconciliation |
| SH-05 | Legal / compliance / privacy (DPO) | Internal | High | High | Lawful outreach, consent, children's safety, contracts | Policy sign-off, DPIA, compliance gates |
| SH-06 | Automation lead | Internal | High | Medium | Safe workflows, monitoring, stop controls | Workflow reviews |
| SH-07 | Engineering team (BE, FS, FE, QA, DevOps) | Delivery | High | Medium | Clear specs, stable scope, test data | Daily stand-up, refinement |
| SH-08 | Tenant administrators (owned and external) | Internal/external | Medium | Medium | Role, template and plan control | Admin UAT |
| SH-09 | Platform support and billing | Internal | Medium | Low | Safe, scoped diagnostics; billing accuracy | Runbooks, support training |
| SH-10 | External SaaS clients | External customers | High | Medium (commercial) | Easy onboarding, isolation, value, fair billing | Pilot onboarding, feedback |
| SH-11 | Prospects, customers, suppliers, institutions, guardians | External users | Medium | Low (but regulatory weight) | Relevant, respectful contact; easy opt-out; transparent status | Portal usability, preference centre |
| SH-12 | Providers: AWS, Anthropic, Meta (WhatsApp), Amazon SES, search/extraction APIs, payment and e-sign providers, calendar | External | Low | High (dependency) | Policy-compliant use, rate limits | Procurement verification, adapter contracts |
| SH-13 | Regulators and authorities: Data Protection Board of India, TRAI, foreign data-protection authorities | External | Low | Very high | Compliance with law | Compliance mapping, DPIA records |
| SH-14 | Investor-product team | Internal adjacent | Low | Medium | Boundary respected; shared IdP stable | Boundary ADR, interface agreement |

---

## 1.8 Personas

Persona IDs (P01–P16) are used in user stories (Part 5) and RBAC (Part 2). Personas **derived** by specializing a source actor are marked *(derived from …)*.

### P01 Founder / Portfolio Owner
- **Source:** "Owner/founder" (BRD §2). Role: oversees all owned startups; final approver for high-risk decisions.
- **Goals:** a portfolio view of verified pipeline and receipts; confidence that no unlawful contact or false claim goes out; approve strategy, pricing exceptions and launches quickly.
- **Pain points:** fragmented tools; numbers that don't reconcile; worry about AI saying wrong things; limited time.
- **Key journeys:** J-01 Review portfolio Overview → drill into one startup (read-only aggregate, DEC-055) · J-02 Approve exception (discount > 20%, cross-border contract) · J-03 Approve autonomous plan hash · J-04 Activate emergency stop.
- **Primary screens:** A089, A043, A082, A087, A066, A068, A072, A102, A033, A106.
- **Permission highlights:** all startups in the Owner Portfolio Tenant; mutations only after selecting one startup; no access to other tenants by default.
- **Success:** decisions in ≤ 2 clicks from notification; numbers reconcile (KPI-13, KPI-31).
- **Context:** desktop and mobile review; English.

### P02 Startup Head *(derived from "authorized management", BRD §9)*
- **Goals:** hit the startup's commercial objectives; approve bids, proposals and discounts within policy; manage the team's assignments.
- **Pains:** approval bottlenecks; unclear readiness of offerings; inconsistent proposals.
- **Journeys:** J-05 Configure offerings and claims (with approval) · J-06 Approve bid/no-bid and bid submission (AppNAI) · J-07 Approve proposal/quote within band · J-08 Review management dashboard.
- **Screens:** A004, A005, A027, A029, A030, A065–A068, A104, A043, A079.
- **Permissions:** one startup (or several by explicit grant); approver for discounts > 10% (DEC-038); bid submission approver.
- **Success:** proposal turnaround time; win rate (KPI-09).

### P03 Growth Manager / Sales Executive
- **Source:** "Employee / growth manager" (BRD §2).
- **Goals:** a prioritized queue of qualified opportunities with evidence; send relevant, compliant messages quickly; never miss a follow-up; book meetings.
- **Pains:** researching from scratch; unclear eligibility; duplicate or conflicting outreach; manual follow-up tracking.
- **Journeys:** J-09 Work the qualified queue → open Customer 360 → draft with AI → approve/send (WF-06) · J-10 Handle inbound reply → book meeting (WF-07) · J-11 Record objection → escalate exception (M45) · J-12 Move deal through stages.
- **Screens:** A022, A027, A029, A032, A034, A037, A038, A040, A045, A069, A106, Copilot.
- **Permissions:** assigned startup, account and team; permitted campaigns; no investor records; cannot approve own discount above 0%.
- **Success:** meetings held (KPI-06), reply rate (KPI-05), time saved per opportunity.

### P04 Research Analyst / Discovery Reviewer *(derived from "Research lead", BRD §12.1)*
- **Goals:** configure permitted research; review signals, needs and contacts efficiently; keep precision high.
- **Pains:** low-quality signals; unclear provenance; duplicate organizations; legal uncertainty about sources.
- **Journeys:** J-13 Create search plan within source policy (WF-02) · J-14 Review signals/needs with evidence panel · J-15 Verify contacts and roles · J-16 Approve qualified opportunity and alert owner.
- **Screens:** A010, A015–A028, A048, A049, A085, A086.
- **Permissions:** assigned startup; cannot activate new sources (needs compliance approval); can accept/reject evidence.
- **Success:** KPI-02, KPI-03, KPI-08, KPI-27.

### P05 Marketing & Content Specialist *(derived from "Employee", BRD §2; campaigns, BRD §5)*
- **Goals:** produce approved, on-brand, claim-safe content; run campaigns and landing pages within budget; publish on schedule.
- **Pains:** claim approval delays; inconsistent brand; unclear attribution; ad overspend risk.
- **Journeys:** J-17 Brief → AI draft → claims check → approval → schedule (WF-05) · J-18 Build landing page and form → approval → publish · J-19 Build campaign + audience → simulate → approval → launch · J-20 Review SEO backlog.
- **Screens:** A050–A063, A107, A108.
- **Permissions:** author but **not** approver of own content; spend within approved cap only.
- **Success:** qualified enquiries from campaigns (KPI-26), cost per conversion, zero unapproved claims.

### P06 Bid & Proposal Manager (AppNAI) *(derived from "Employee", BRD §4 AppNAI route)*
- **Goals:** never miss an eligible tender deadline; fast bid/no-bid with evidence; compliant bid packages; record awards accurately.
- **Pains:** scattered RFP sources; eligibility and deadline errors; manual checklists.
- **Journeys:** J-21 Tender discovered → eligibility checklist → bid/no-bid approval → proposal/quote → human submission with evidence → award/contract (WF-08).
- **Screens:** A104, A016, A017, A065–A068, A071, A072, A029.
- **Permissions:** AppNAI workspace; cannot submit; records submission evidence after approval (DEC-053).
- **Success:** KPI-11, zero late or ineligible submissions (FRD §12.1 bid expiry).

### P07 Order & Fulfilment Coordinator (OrganicSpec) *(derived from "Employee", BRD §4 OrganicSpec route)*
- **Goals:** accurate RFQ → quote → order with lines, units and quantities; track dispatch, receipt and acceptance; keep receivables and payables separate.
- **Pains:** unit/quantity errors; over-delivery; mixed buy and sell ledgers.
- **Journeys:** J-22 RFQ (W14) → quotation → sales order → dispatch → acceptance → receivable · J-23 Supplier enquiry (W16) → purchase order → receipt → payable (WF-10).
- **Screens:** A105, A067, A073, A074, A018, W14, W16, W25.
- **Permissions:** OrganicSpec workspace; cannot verify payments (finance only).
- **Success:** KPI-12, KPI-14.

### P08 Finance Officer (maker or checker)
- **Source:** "Finance and legal" (BRD §2).
- **Goals:** correct invoices and quotes; verified receipts; no premature closure; clean reconciliation; usage-based SaaS billing.
- **Pains:** manual matching; duplicate payments; FX confusion; unclear evidence.
- **Journeys:** J-24 Verify payment evidence (maker) → second verification (checker) → closure eligible · J-25 Reconcile receipts and payables · J-26 Approve discount/margin exceptions with founder · J-27 Run SaaS billing cycle.
- **Screens:** A068, A073, A074, A083, A101, A012.
- **Permissions:** maker and checker must be different people; no autonomous transfer; read access to deal context only for assigned startups.
- **Success:** KPI-13, KPI-14, KPI-24, KPI-31.

### P09 Legal, Compliance & Privacy Officer (DPO)
- **Source:** "Finance and legal" (BRD §2); "Privacy and compliance lead" (BRD §15).
- **Goals:** approve claims, contracts and policies; handle privacy requests on time; detect and contain violations.
- **Pains:** invisible outreach; ad-hoc claims; slow evidence gathering.
- **Journeys:** J-28 Approve legal version of contract · J-29 Process privacy request (verify → execute → audit) · J-30 Review compliance incident → contain → resolve · J-31 Approve source permissions and jurisdiction rules · J-32 Approve claims.
- **Screens:** A007, A010, A013, A047, A051, A072, A092, A094.
- **Permissions:** cross-startup read within tenant for compliance; approval rights; cannot send messages.
- **Success:** KPI-17, KPI-18, privacy SLA met (100% within legal deadline).

### P10 Automation Lead / Workflow Designer
- **Source:** "Automation lead" (BRD §12, §14).
- **Goals:** design, simulate and safely run workflows; monitor runs; resolve conflicts; stop quickly.
- **Pains:** runaway sequences; unclear failures; duplicate actions across workflows.
- **Journeys:** J-33 Build workflow from approved nodes → simulate → approve hash → enable (WF-13) · J-34 Monitor runs → pause → reconcile uncertain → resume · J-35 Resolve conflicts (A111) · J-36 Manage triggers (A109).
- **Screens:** A033, A102, A109–A113, A012, A014.
- **Permissions:** workflow configuration within the tenant; cannot loosen autonomy caps (DEC-064); emergency stop.
- **Success:** KPI-19, KPI-20, zero blind retries.

### P11 Tenant Administrator
- **Source:** BRD §2.
- **Goals:** manage users, roles, templates, plans and operational controls for the tenant.
- **Pains:** permission sprawl; onboarding effort.
- **Journeys:** J-37 Invite user → assign role and startup grants → enforce MFA · J-38 Apply business template → configure startup → approve config change (A112) · J-39 Approve support-access grant.
- **Screens:** A002, A099, A100, A112, A008.
- **Permissions:** own tenant only; **not** automatically a business approver (BRD §2).
- **Success:** onboarding time (KPI-25); access-review completion.

### P12 Platform Support & Billing Operator
- **Source:** BRD §2.
- **Goals:** diagnose incidents using operational metadata; manage billing operations; never see confidential business content unless granted.
- **Journeys:** J-40 Request scoped support grant → diagnose with metadata → close · J-41 Run usage reconciliation and invoices.
- **Screens:** A014, A009 (redacted), A101.
- **Permissions:** operational metadata; bounded, client-approved, time-limited grants (DEC-056).
- **Success:** mean time to resolve; zero unauthorized access.

### P13 SaaS Client Administrator (external)
- **Source:** BRD §17 (W31–W34), B-SVC.
- **Goals:** evaluate plans, register the business, configure it with AI help, run it independently, manage subscription and exports.
- **Pains:** complex setup; uncertainty about data isolation and cost.
- **Journeys:** J-42 Plans & demo (W31) → registration with administrator verification (W32) → AI onboarding wizard (W33, drafts only) → approval → provisioning → service portal (W34) → Admin workspace.
- **Permissions:** own tenant; applicant draft isolated until provisioning (FRD §16.3).
- **Success:** onboarding ≤ 1 business day after approval (KPI-25).

### P14 External Customer / Prospect (portal user), with four segment variants
- **Source:** "External prospect/customer" (BRD §2); Website-Portal surface (BRD §9).

| Variant | Who | Goals | Key journeys | Special constraints |
|---|---|---|---|---|
| P14a | Enterprise / IT-firm procurement contact (AppNAI) | Submit project requirements; review proposals and quotes; sign; track milestones and invoices | W15 → W23 → W24 → W25 → W26 | File uploads scanned and authenticated |
| P14b | Institutional health partner: hospital or clinic administrator, lab, corporate HR, insurer (MedMaarg) | Understand approved offerings; request a demo or pilot; manage the partnership | W13 → W18 → W23 → W24 → W27 | No patient data; clinical questions routed to humans (M32) |
| P14c | Education stakeholder: guardian, adult learner, school/college coordinator (EduVerse) | Find programmes; enquire and register; institutional MoU | W17 → W19 → W23/W24 → W27 | Under-18 handled via guardian/institution only (DEC-030) |
| P14d | Trade counterparty: buyer, supplier, distributor, FPO (OrganicSpec) | RFQ, supply enquiry, order status, invoices | W14/W16 → W23 → W25 → W26 | Units, quantities and certification validated |

- **Common pains:** irrelevant or repeated messages; hard to opt out; opaque status.
- **Common permissions:** own invite/portal records only; field-minimized DTOs; no staff permissions; tokens are not authorization by themselves (W24).
- **Success:** portal completion (KPI-26); opt-out honoured immediately.

### P15 Anonymous Website Visitor
- **Source:** Website-Public surface (BRD §9).
- **Goals:** learn about the business; find offerings; ask questions; submit an enquiry; book a meeting; register for an event.
- **Journeys:** J-43 Landing page → offering detail → enquiry with consent · J-44 Chat assistant → grounded answer → handover/lead with consent.
- **Screens:** W01–W20, W30, W31.
- **Constraints:** sees approved published snapshots only; rate-limited intake; no tracking of health events to ad pixels (M37).
- **Success:** qualified enquiries (KPI-26).

### P16 System and service identities (non-human actor)
- **Source:** "Internal/callback: service identities / verified providers" (BRD §9).
- **Examples:** Celery workers, scheduler, provider webhooks (SES, WhatsApp, calendar, e-sign, payments), AI agents acting through the gateway.
- **Rules:** no browser access; signature verification; idempotency; least-privilege service roles; every action carries a correlation ID and the initiating policy/plan.

### 1.8.1 Persona to actor to surface map

| Persona | Source actor (BRD §2) | Surface | Default autonomy they can approve |
|---|---|---|---|
| P01 | Owner/founder | Admin | Up to L3 within caps (not for DEC-064 L1-capped actions) |
| P02 | Authorized management | Admin | L1/L2 for startup workflows |
| P03 | Employee/growth manager | Admin | L1 (own drafts); runs approved sequences |
| P04 | Employee (research) | Admin | L1 |
| P05 | Employee (marketing) | Admin | Author only |
| P06 | Employee (bids) | Admin | Author; records submission |
| P07 | Employee (orders) | Admin | Author |
| P08 | Finance | Admin | Maker/checker |
| P09 | Legal/compliance | Admin | Legal/claims/policy approvals |
| P10 | Employee (automation) | Admin (Automation group) | Configure; enable needs approver |
| P11 | Tenant administrator | Admin | Tenant configuration only |
| P12 | Platform support/billing | Admin (ops) | None (operational) |
| P13 | External SaaS client admin | Website (W31–W34) → Admin of own tenant | Own tenant |
| P14 | External prospect/customer | Website-Portal | None (own requests only) |
| P15 | Anonymous visitor | Website-Public | None |
| P16 | Service identities | Internal/callback | Executes approved plans only |

---

## 1.9 Key journeys (summary; detailed flows in Part 2)

| Journey ID | Name | Personas | Workflow | Start → end | Primary screens |
|---|---|---|---|---|---|
| J-01 | Portfolio oversight | P01 | n/a | Overview → drill-down | A089, A043, A082 |
| J-05 | Product truth setup | P02, P09 | WF-01 | Draft offering → claims approval → available | A004–A006, A051 |
| J-13 | Permitted discovery | P04 | WF-02 | Plan → evidence → signal → need → match → score | A015–A022 |
| J-15 | Contact qualification | P04 | WF-03 | Role hypothesis → verified channel → eligibility | A024–A026 |
| J-09 | Outreach to qualified account | P03 | WF-06 | Qualified → draft → preflight → approve → send → reply | A034, A037 |
| J-10 | Reply to meeting | P03 | WF-07 | Inbound → intent → slot offer → booked → held | A037, A040 |
| J-43 | Inbound web enquiry | P15, P03 | WF-04 | Landing → form → dedupe → consent → lead → assign | W10, W12, A031 |
| J-17 | Content to publication | P05, P09 | WF-05 | Brief → draft → claims → approval → schedule → receipt | A050–A053 |
| J-21 | Tender bid (AppNAI) | P06, P02 | WF-08 | Tender → eligibility → bid/no-bid → package → submission evidence → award | A104 |
| J-07 | Proposal and quote | P03, P02, P08 | WF-09 | Draft → price snapshot → approval → portal review → accept | A065–A068, W23 |
| J-22/23 | Order and fulfilment (OrganicSpec) | P07, P14d | WF-10 | RFQ → quote → order → dispatch/receipt → acceptance → ledger | A105, W14, W25 |
| J-24 | Verified closure | P08, P01 | WF-11 | Evidence → maker → checker → won/paid | A073, A074 |
| J-48 | Onboarding and renewal | P03, P14 | WF-12 | Won → onboarding tasks → renewal due → review | A075–A080, W27, W28 |
| J-33 | Autonomous plan | P10, P01 | WF-13 | Objective → plan → simulation → approve hash → execute → monitor | A102, A110 |
| J-49 | Tenant suspension/offboarding | P11, P12, P13 | WF-14 | Suspend → stop schedules → revoke → export → retain | A099, A103 |
| J-42 | SaaS client onboarding | P13 | WF-14 (inverse) | Plans → register → verify → wizard → approve → provision | W31–W34, A099 |
| J-29 | Privacy request | P14, P09 | n/a | Request → verify → execute → suppress → audit | W29, W30, A013 |

---

## 1.10 Constraints

| ID | Constraint | Type | Source |
|---|---|---|---|
| CN-01 | Mandated stack: React/TypeScript, Django REST Framework, PostgreSQL (+ pgvector where justified), Celery/Beat, Valkey, object storage | Technical | BRD §1.2 |
| CN-02 | Independent deployment: separate origin, API audience, DB, storage, queues, credentials, budget, billing, audit, backup | Architectural | BRD §1 |
| CN-03 | Two separate frontends with separate sessions/clients; no Admin code in public bundles | Architectural/security | BRD §1; DEC-009 |
| CN-04 | Reuse existing authentication/security; no rebuild budgeted | Technical/budget | M01; DEC-003, DEC-019 |
| CN-05 | Open-source first; paid services disabled by default; no Zapier/Make | Financial/policy | BRD §10, FRD §6 M06 |
| CN-06 | Run-cost envelope: ₹16,675/month base (₹31,165 with optional items); AI ₹3,000/month at pilot | Financial | BRD §6; DEC-004, DEC-008 |
| CN-07 | Engineering envelope: 287–483 person-days; team 4.0 eng FTE + 0.5 growth/compliance | Financial/capacity | BRD §6; DEC-005 |
| CN-08 | Timeline: W0–W5 in 180 days; W6 to Day 365 | Schedule | BRD §8; DEC-006 |
| CN-09 | Indian law (DPDP, IT Act, TRAI) plus foreign rules for outbound contact | Regulatory | BRD §8 sources; DEC-029 |
| CN-10 | No patient/clinical data; no minors targeting; no private scraping | Regulatory/ethical | BRD §5, §7, §15 |
| CN-11 | Provider terms: Meta WhatsApp template/opt-in rules, social platform API limits, search API licences | External | FRD §6 M31, M33, M35, M10 |
| CN-12 | All routes, tables and provider terms require implementation validation; no executable migration asserted | Governance | BRD §1.2, FRD §5 |
| CN-13 | No production sign-off may be inferred from specifications or synthetic tests | Governance | BRD §12.2, §13 |
| CN-14 | Owner portfolio aggregate views are read-only for business mutations | Functional | BRD §1; DEC-055 |
| CN-15 | Legacy method/path contracts retained; new endpoints under `/api/v1/commercial/{public,portal,admin}/` | Technical | BRD §9 |

## 1.11 Dependencies

| ID | Dependency | Type | Needed by | Risk if late | Mitigation |
|---|---|---|---|---|---|
| DP-01 | Existing identity/security (H02/H03) compatible with a new audience | Internal | W0 (Sprint 1) | Blocks all authenticated work | Sprint 0 spike (DEC-019); fallback: Django-native auth module under a feature flag |
| DP-02 | AWS account, region ap-south-1, IaC baseline | External | Sprint 0 | No environments | Early provisioning |
| DP-03 | Anthropic API account, keys, budget alarms | External | W0 | No AI features | Tier 0 rules work without AI; stub adapter in tests |
| DP-04 | Approved product catalogue and claims per seed startup | Business | W0–W1 | Nothing can be promoted | Claims workshop per startup in Sprint 1 |
| DP-05 | Source permissions (search API licence, allowed hosts) | Business/legal | W1 | Discovery blocked | Tavily free tier / self-hosted extraction first (BRD §6) |
| DP-06 | Amazon SES production access, verified domains, DMARC | External | W2 | No email | Start the request in W0; sandbox meanwhile |
| DP-07 | Google Workspace calendar OAuth app verification | External | W2 | No booking | Manual booking link fallback |
| DP-08 | Meta WhatsApp Business Account, verified business, approved templates | External | W3 | No WhatsApp | Start verification in W1 |
| DP-09 | Social platform API access (publishing, listening) | External | W3 | Feature deferred | Should/Could priority |
| DP-10 | Payment gateway merchant account(s) | External | W4 | Manual bank/UPI evidence only | DEC-022 manual path |
| DP-11 | E-sign provider contract | External | W5 | Signed-PDF path only | DEC-023 |
| DP-12 | Legal confirmations: retention, jurisdictions, children, e-sign validity, GST | Legal | W0–W4 | Activation gates fail | Legal review backlog in Sprint 0 |
| DP-13 | Founder-authorized non-confidential business-fact snapshot | Business | W0 (optional) | Manual catalogue entry | A103 import |
| DP-14 | Domain names and DNS control for startup websites | Business | W2 | Websites not published | Collect in W0 |
| DP-15 | Investor-product team agreement on the IdP boundary | Internal | W0 | Audience/claims conflicts | Boundary ADR (Part 3) |

---

## 1.12 Business requirement register

### 1.12.1 Primary business requirements (71)

Columns: **ID** · **Title** · **Objective (source)** · **Business acceptance (source)** · **Depends on (source)** · **Personas** · **MoSCoW** · **Wave** · **Epic (prelim.)**. Every row's source is BRD §7 (objective/dependency) and BRD §12 (acceptance) unless stated otherwise.

| ID | Title | Objective | Acceptance | Depends on | Personas | MoSCoW | Wave | Epic |
|---|---|---|---|---|---|---|---|---|
| BR-M01 | Identity & access | Reuse existing login/security under the new product audience (DEC-003) | Cross-role access denied; session revoked | H02, H03 (DEC-019) | All | Must | W0 | EP-01 |
| BR-M02 | Product knowledge catalog | Approved startup offering truth (DEC-003) | Planned products blocked from promotion | M01 | P02, P05, P09 | Must | W0 | EP-02 |
| BR-M03 | Knowledge document ingestion | Extract deck, brochure, FAQ evidence | Every answer cites approved version | M02 | P02, P09, P15 | Must | W0 | EP-02 |
| BR-M04 | Consent and suppression | Enforce channel eligibility | Opt-out blocks all scoped sends | M01 | P09, P14 | Must | W0 | EP-03 |
| BR-M05 | Integration registry | Control external access and spend | Secrets never returned in API | M01, M04 | P11, P10 | Must | W0 | EP-01 |
| BR-M06 | Event and audit foundation | Reliable shared automation | Duplicate delivery has one effect | M01 | P16, P12 | Must | W0 | EP-01 |
| BR-M07 | Source permissions register | Only permitted public research | Unapproved URL blocked | M04, M05 | P04, P09 | Must | W0 | EP-05 |
| BR-M08 | AI gateway and evaluation | Controlled model execution | Invalid outputs rejected; cost cap enforced | M02, M05, M06 | P10, P16 | Must | W0 | EP-04 |
| BR-M53 | Cost and usage control | Prevent runaway API spend | Simulated cap stops requests | M05, M08 | P01, P08 | Must | W0 | EP-04 |
| BR-M56 | Privacy requests and retention | Honour deletion/correction rights | Deletion does not re-enable outreach | M04, M06 | P09, P14 | Must | W0 | EP-03 |
| BR-M09 | DevSecOps & environment | Reproducible releases | Restore drill; secret scan; smoke test | M01, M08 | P12, SH-07 | Must | W0 | EP-21 |
| BR-M58 | Operational observability | Ensure reliability | Provider outage does not lose events | M06, M09 | P12, P10 | Must | W0 | EP-21 |
| BR-M10 | Search query planner | Translate capabilities into research | No personal health targeting queries | M02, M07, M08 | P04 | Must | W1 | EP-05 |
| BR-M11 | Public web discovery | Find relevant account-level signals | Source URL/date recorded; blocked hosts rejected | M10 | P04 | Must | W1 | EP-05 |
| BR-M12 | Evidence extraction | Extract business facts, not assumptions | Evidence traceable; injection ignored | M11, M08 | P04 | Must | W1 | EP-05 |
| BR-M13 | Account discovery | Identify target organizations (hospitals, corporates, institutions, buyers, suppliers) | Duplicate domain/location merge safe | M12 | P04 | Must | W1 | EP-05 |
| BR-M14 | Buying signal classification | Detect relevant business developments | ≥ 80% precision on reviewed pilot sample (DEC-001) | M12, M13 | P04 | Must | W1 | EP-05 |
| BR-M15 | Business need discovery | Separate explicit vs inferred needs | No inference labelled confirmed | M14 | P04 | Must | W1 | EP-05 |
| BR-M16 | Product solution matching | Map need to deployable offering | Unavailable offering excluded from sales | M02, M15 | P04, P03 | Must | W1 | EP-05 |
| BR-M17 | Opportunity scoring | Prioritize actionable accounts | Score recalculates; consent independent (DEC-011) | M16 | P04, P03 | Must | W1 | EP-06 |
| BR-M18 | Decision-maker role discovery | Find legitimate professional channels | No private contacts or guessed emails | M13, M17 | P04 | Must | W1 | EP-06 |
| BR-M19 | Contact verification | Validate published work channels | Verified not synonymous with consent | M18, M04 | P04 | Must | W1 | EP-06 |
| BR-M20 | Research review and alerts | Deliver reviewed opportunity to sales | Rejected leads never sent to channel | M17, M19 | P04, P03 | Must | W1 | EP-06 |
| BR-M21 | CRM pipeline | Track opportunities end to end | Invalid stage transition rejected | M20, M06 | P03, P02 | Must | W2 | EP-07 |
| BR-M22 | Lead capture and forms | Inbound requests and consent | Duplicate submission → one lead | M04, M21 | P15, P03 | Must | W2 | EP-07 |
| BR-M23 | Customer 360 | One account record | Updates visible within 60 s | M21, M22 | P03 | Must | W2 | EP-07 |
| BR-M24 | Engagement eligibility | Prevent unwanted contact | No send when opt-out/unknown eligibility | M04, M19 | P03, P09, P16 | Must | W2 | EP-03 |
| BR-M55 | Workflow control center | Manage automations safely | Emergency stop blocks queued sends | M06, M24 | P10, P01 | Must | W2 | EP-18 |
| BR-M25 | Personalized message drafting | Relevant evidence-based outreach | No invented relationship or diagnosis | M08, M16, M24 | P03 | Must | W2 | EP-08 |
| BR-M26 | Email integration | Allowed email delivery and status | Replay no duplicate; bounce suppress | M24, M25, M05 | P03, P16 | Must | W2 | EP-08 |
| BR-M27 | Unified inbound processing | Automate replies and intent detection | STOP cancels; urgent/clinical routes to human | M26, M08 | P03, P16 | Must | W2 | EP-08 |
| BR-M28 | Follow-up sequences | Automate relevant follow-up | No follow-up after stop or reply | M24, M26, M27 | P03, P10 | Must | W2 | EP-08 |
| BR-M29 | Meeting and calendar | Book demos with qualified accounts | No invented availability; conflict handled | M27, M21 | P03, P14 | Must | W2 | EP-09 |
| BR-M30 | Growth dashboard | Management tracks sales funnel (DEC-013) | Counts reconcile with deal records | M20, M29 | P01, P02 | Must | W2 | EP-17 |
| BR-M31 | WhatsApp Business | Customer-initiated / opted-in messaging | No private group scrape; opt-in gate | M24, M27 | P03, P14 | Should | W3 | EP-10 |
| BR-M32 | Website conversational assistant | Answer product questions and collect leads | Clinical question routed; no medical data | M08, M22, M27 | P15 | Should | W3 | EP-10 |
| BR-M41 | Unified omnichannel routing | Consistent response across connected channels | No duplicate replies across linked channels | M27, M31, M32 | P03 | Should | W3 | EP-08 |
| BR-M57 | Compliance monitoring | Track policy breaches and complaints | Simulated complaints stop campaign | M24, M41 | P09 | Must | W3 | EP-03 |
| BR-M33 | Social listening | Monitor permitted organizational signals | No restricted profiles or automated DMs | M07, M14 | P04 | Could | W3 | EP-05 |
| BR-M34 | Content studio | Produce approved segment-specific content | Unapproved claims cannot publish | M02, M08 | P05 | Should | W3 | EP-11 |
| BR-M35 | Social publishing | Schedule approved posts | No unsupported DMs; idempotent publishing | M34, M05 | P05 | Should | W3 | EP-11 |
| BR-M36 | SEO and search visibility | Improve relevant search traffic | No fabricated ranking data | M07, M34 | P05 | Could | W3 | EP-11 |
| BR-M37 | Landing pages and attribution | Capture consented acquisition | No health events to ad pixels | M22, M34 | P05, P15 | Must | W3 | EP-12 |
| BR-M38 | Campaign management | Coordinate approved marketing | Suppression applied at execution | M24, M34, M37 | P05 | Should | W3 | EP-12 |
| BR-M39 | Paid ads integration | Controlled acquisition spending | Budget exceeded → pause; no sensitive data | M38, M05 | P05, P08 | Could | W3 | EP-12 |
| BR-M40 | Webinars and demonstrations | Nurture interested accounts | Opt-outs respected; attendance dedup | M22, M28, M29 | P05, P14 | Could | W3 | EP-09 |
| BR-M42 | Referral and partner lead capture | Track legitimate referrals | No unauthorized third-party contact enrolment | M22, M38 | P05, P03 | Should | W3 | EP-12 |
| BR-M43 | Proposal builder | Generate approved B2B pilot proposals | Only approved version externally shared | M21, M29, M02 | P03, P06, P02 | Must | W4 | EP-13 |
| BR-M44 | Quote and pricing engine | Accurate commercial terms | No unauthorized discount; totals exact (DEC-027, DEC-038) | M43, M02 | P03, P07, P08 | Must | W4 | EP-13 |
| BR-M45 | Negotiation and objection handling | Automate safe routine replies | Contract/price exception escalates | M41, M44 | P03, P02 | Should | W4 | EP-13 |
| BR-M46 | Contract and MoU workflow | Manage institutional agreements | No AI signs contract; signed version hash stored (DEC-023) | M43, M44 | P09, P02, P14 | Must | W4 | EP-13 |
| BR-M47 | Payment and closure | Close only on actual commercial evidence | Replay no duplicate revenue; no invented closure (DEC-022, DEC-054) | M46, M21 | P08, P01 | Must | W4 | EP-15 |
| BR-M48 | Onboarding and handoff | Transfer commercial customer to product team | No patient data copied | M47, M04 | P03, P14 | Must | W4 | EP-16 |
| BR-M49 | Partner deployment pipeline | Manage phygital and institutional pilots | No deployment claims before approval | M43, M46 | P02 | Should | W4 | EP-16 |
| BR-M50 | Retention and renewal | Maintain relationships | No medical data in scoring | M48, M28 | P03, P02 | Should | W4 | EP-16 |
| BR-M51 | Lost deal and feedback | Learn from commercial results | No auto-recontact after loss without policy | M21, M28 | P03, P02 | Should | W4 | EP-16 |
| BR-M52 | Revenue and attribution | Measure funnel economics | Revenue reconciles with finance; attribution caveat | M37, M47 | P01, P08 | Must | W5 | EP-15 |
| BR-M54 | AI quality and feedback | Improve accuracy and reduce false positives | Regression fails block deploy (DEC-061) | M08, M51 | P10, P04 | Must | W0 (harness) / W5 (loop) | EP-04 |
| BR-M59 | Competitor and market watch | Track public business changes | No unverified comparative claim | M10, M12 | P04, P02 | Could | W5 | EP-05 |
| BR-M60 | Forecast and sales optimization | Forecast from actual data | Forecast labelled estimate | M51, M52 | P01, P02 | Could | W5 | EP-17 |
| BR-M61 | Admin command center | Centralized governance | Admin totals reconcile; no direct unsafe DB edits (DEC-062) | M01, M60 | P01 | Must | W0 (shell) / W5 | EP-17 |
| BR-M62 | End-to-end production release | Validate complete user journey | All critical tests pass; rollback verified (DEC-063) | M01, M61 | SH-07 | Must | W0 (pipeline) / W5 | EP-21 |
| BR-M63 | Insurance institutional pilot | Explore organization-level benefits | No underwriting or personal profiling | M49, M57 | P02, P09 | Could | W6 | EP-16 |
| BR-M64 | Technology licensing pipeline | Evaluate API/white-label readiness | No promised unready API | M46, M49 | P02, P09 | Could | W6 | EP-16 |
| BR-M65 | Phygital expansion | Scale approved deployments | Deployment sign-off required | M49, M52 | P02 | Could | W6 | EP-16 |
| BR-M66 | Future product commercialization | Gate planned products | Planned offerings not promoted (DEC-060) | M02, M57 | P02, P09 | Must (gate W0) / launch workflow W6 | W0 / W6 | EP-02 |
| BR-TENANT | Independent tenant/startup operation | Provision 2 independent external tenants and 25 owned startup workspaces | Zero cross-scope disclosure or side effects | M01, M05, M06 | P11, P01 | Must | W0–W5 | EP-01, EP-14 |
| BR-WEB | Approved public website and external portal | Approved sites and a scoped external portal | Verified host serves approved snapshot only; external users access only granted objects; Admin routes deny external identities | M02, M22, BR-TENANT | P15, P14, P05 | Must | W2–W3 | EP-19 |
| BR-AUTO | Controlled autonomous operations | Simulate, check and execute safely | Simulate without side effects; recheck eligibility, budget and approval before dispatch; pause stops new actions; audit every state | M06, M24, M55 | P10, P01 | Must (Manual→Supervised W2) / Should (Controlled Autonomous W5) | W2 / W5 | EP-18 |
| BR-SVC | Service subscriptions and client portability | Run external clients as SaaS | Provision, meter, invoice, suspend and export one tenant without modifying another; reconcile charges to usage | BR-TENANT, M53 | P13, P12, P08 | Should | W5 | EP-20 |
| BR-QA | Reliable, independently verified delivery | Evidence-based delivery | Each approved requirement has implementation and test evidence; go-live gates passed; restore and rollback rehearsed | All | SH-07, P01 | Must | W0–W5 | EP-21 |

**Count check:** 66 module BRs + 5 cross-cutting = **71** ✔. MoSCoW: Must 50 / Should 12 / Could 9 ✔ (BR-M66 and BR-AUTO counted once as Must; BR-M54, BR-M61, BR-M62 counted once as Must).

### 1.12.2 Supplementary business requirements (140)

Columns: **ID** · **Requirement statement (condensed, faithful to source)** · **Source** · **Traces to** (primary BR / workflow / decision). Every statement is binding and will appear in the Part 9 traceability matrix.

**A. Vertical operating sequences and scoring (BRD §4)**

| ID | Statement | Source | Traces to |
|---|---|---|---|
| BR-S001 | AppNAI route: global RFP/project discovery → technical and eligibility review → bid/no-bid → proposal/quote → authorized submission → award/contract → accepted delivery → verified payment | BRD §4 | WF-08, M43, M44, M46, M47, A104 |
| BR-S002 | MedMaarg route: institutional wellness need → approved product match → decision-maker → demo/pilot → signed partnership → deployment and payment → renewal | BRD §4 | M16, M18, M29, M46, M47, M49, M50 |
| BR-S003 | EduVerse route: student/guardian/institution requirement → programme fit → approved counselling/demo → registration or MoU/educational order → delivery → receipt/renewal; school protection and institutional permissions; no commercial AI project acquisition | BRD §4 | W17, M22, M46, DEC-030, DEC-052 |
| BR-S004 | OrganicSpec route: buyer/supplier discovery → RFQ → quote → purchase/sales order with lines → dispatch/receipt/service/training acceptance → reconcile payable or receivable | BRD §4 | WF-10, A105, M44, M47 |
| BR-S005 | Source scoring: fit/evidence/intent/readiness/timing weighted 25/25/20/15/15; thresholds ≥ 75 / 50–74 / < 50; unknown separate; score is not authority to send; KPIs as listed; no predicted revenue as actual; lawful organization-level sources only | BRD §4 | M17, DEC-011, KPI catalogue |

**B. Workflow register (BRD §5)**

| ID | Statement | Source | Traces to |
|---|---|---|---|
| BR-S006 | WF-01 Startup catalogue: approve offering, price, claims, segment, customer roles, pipeline, workflow; no unapproved offerings or unscoped access | BRD §5 | M02, M66, A004 |
| BR-S007 | WF-02 Market discovery: plan query → evidence → signals/need → solution match → qualify; allowed sources, review, freshness, confidence | BRD §5 | M10–M17 |
| BR-S008 | WF-03 Professional contacts: find decision-maker, verify channel/source, deduplicate, eligibility; no private scraping; contact score ≠ permission | BRD §5 | M18, M19, M24 |
| BR-S009 | WF-04 Inbound acquisition: landing/chat/email/WhatsApp/social/event/referral → lead and attribution; scope, consent, dedupe; no medical records or minor targeting | BRD §5 | M22, M31, M32, M37, M40, M42 |
| BR-S010 | WF-05 Content/campaign: approved content, SEO, social, ad/landing plan, audience, budget; claim and channel approval; cost caps; actual publication | BRD §5 | M34–M39 |
| BR-S011 | WF-06 Outreach and replies: preview eligible contacts → approved messages → callback → classify intent; opt-out/complaint stop; response halts generic sequence | BRD §5 | M24–M28 |
| BR-S012 | WF-07 Follow-up & meetings: tasks by intent, preference, local time; verify calendar; caps, rejection and suppression stop | BRD §5 | M28, M29 |
| BR-S013 | WF-08 Project bid: AppNAI qualify RFP, deadline, bid/no-bid, proposal, authorized submission; no unauthorized portal submission; actual award proof | BRD §5 | A104, DEC-053 |
| BR-S014 | WF-09 Proposal/quote: approved pricing and terms; objections; controlled discount/negotiation; revisions and approvals; no unsupported promises | BRD §5 | M43–M45, DEC-038 |
| BR-S015 | WF-10 Order/fulfilment: buy/sell/service/training/project order with lines; delivery, receipt, acceptance; payables/receivables independent; quantity and evidence checked | BRD §5 | A105, DEC-045 |
| BR-S016 | WF-11 Commercial closure: verified signed contract/payment per route; actual receipts/obligations; onboarding; no duplicate cash or false won state | BRD §5 | M46, M47, M48, DEC-054 |
| BR-S017 | WF-12 Retention & renewal: handoff, milestones, feedback, renewal, eligible re-engagement; record outcomes and preferences; no duplicated revenue | BRD §5 | M48, M50, M51 |
| BR-S018 | WF-13 Autonomous plan: simulate workload, recipients, cost, deadlines; approve hash; execute; no live effect during dry run; revalidate at dispatch | BRD §5 | A102, B-AUTO |
| BR-S019 | WF-14 Suspend/offboard: stop schedules, revoke sender and client access, export/retain allowed records; reconcile unknown results | BRD §5 | A099, A103, B-SVC |

**C. Authority (BRD §2) and Command Centre views (BRD §3)**

| ID | Statement | Source | Traces to |
|---|---|---|---|
| BR-S020 | Owner/founder: authorized portfolio, selected-startup mutations, strategy and approval; no other tenant by default | BRD §2 | P01, DEC-055 |
| BR-S021 | Employee/growth manager: assigned startup/account/team, permitted campaigns and sales actions; no investor records | BRD §2 | P03–P07 |
| BR-S022 | Finance and legal: maker/checker for terms, finance and regulated approvals; actual evidence; no autonomous financial transfer | BRD §2 | P08, P09, DEC-038 |
| BR-S023 | Tenant administrator: own tenant roles, templates, plans, operation controls; not automatically business approver | BRD §2 | P11 |
| BR-S024 | Platform support/billing: operational metadata; bounded client-approved grant; no confidential business content by default | BRD §2 | P12, DEC-056 |
| BR-S025 | External prospect/customer: own invite/portal records; approved information only; no internal directory | BRD §2 | P14 |
| BR-S026 | Other application user: token audience and product entitlement deny access even with the same SSO identity | BRD §2 | DEC-058, NFR-001 |
| BR-S027 | View "Overview": commercial KPIs, pipeline, forecast, verified receipts/payables, campaign attribution, actions | BRD §3 | A089, A042, A043 |
| BR-S028 | View "Discovery": public sources, needs, organizations, contacts, project bids, buyers, suppliers | BRD §3 | A015–A028, A104 |
| BR-S029 | View "Outreach & Marketing": content, SEO, social, ads, landing pages, email, WhatsApp, events, campaigns, inbox | BRD §3 | A034–A064 |
| BR-S030 | View "Follow-ups": sequences, meetings, next action, tasks, onboarding, renewal | BRD §3 | A038–A041, A075–A080 |
| BR-S031 | View "Objections": approved factual answers, pricing/contract exceptions, escalation | BRD §3 | A069, A070 |
| BR-S032 | View "Closure": proposal, quote, tender award, contract, purchase/sales order, fulfilment, verified payment | BRD §3 | A065–A074, A104, A105 |
| BR-S033 | View "Automation": separate permissioned workspace: permissions, approvals, workflow builder, costs, tenant, billing (DEC-009) | BRD §3 | A033, A099–A103, A109–A113 |

**D. Vertical acceptance, success controls, outcomes, activation (BRD §11–§13)**

| ID | Statement | Source | Traces to |
|---|---|---|---|
| BR-S034 | AppNAI: verify tender eligibility, deadline, budget, technical requirements and authorized submission; track award and agreement separately; no submission without mandatory checks | BRD §11 | A104 |
| BR-S035 | MedMaarg: qualify organization-level needs, approved AI Hospital claims and pilot; exclude patient data; appropriate partnership handoff | BRD §11 | M16, M48, M49 |
| BR-S036 | EduVerse: route student/institutional training and school AI products/services with safeguarding; external AI projects belong to AppNAI; applicable consent | BRD §11 | DEC-030, DEC-052 |
| BR-S037 | OrganicSpec: verify supplier/buyer, SKU, unit, quantity, price, fulfilment, separate payable/receivable ledgers; accurate order, receipt and reconciliation | BRD §11 | A105, RECOMMENDATION-018 |
| BR-S038 | Commercial campaigns: validate audience, claims, consent, spend and attribution before publishing/sending; no unapproved spend, message or disclosure | BRD §11 | M38, M39, M34 |
| BR-S039 | Qualified opportunity counted only with evidence, fit and accountable owner; de-duplicated; unknown remains unqualified | BRD §12.1 | KPI-07, M20 |
| BR-S040 | Conversion outcome separates qualified lead, accepted agreement, fulfilled obligation and reconciled receipt; no double counting with procurement/payables | BRD §12.1 | M47, M52 |
| BR-S041 | Global coverage: approved sources monitored vs registry by country/sector; show restricted and not-yet-covered sources | BRD §12.1 | KPI-27, A010 |
| BR-S042 | Service economics: subscription revenue separate from business proceeds; unit economics include hosting, model, data and support | BRD §12.1 | KPI-23, A101 |
| BR-S043 | Delivery exit: no required FR without a tested result; waivers documented with owner and independent reviewer | BRD §12.1 | B-QA |
| BR-S044 | Qualified lead = distinct tenant/startup opportunity with verified need, offering fit and contact eligibility | BRD §13.1 | KPI-07 |
| BR-S045 | Won deal = approved contract/order plus route-specific verified conditions; distinguish awarded, signed, delivered, paid | BRD §13.1 | DEC-054 |
| BR-S046 | Commercial receipts = reconciled customer receipts by issuer and currency; exclude procurement payments, SaaS fees and investment | BRD §13.1 | KPI-13 |
| BR-S047 | Acquisition conversion = source/campaign → qualified lead → approved deal → won → verified receipt; report attribution model and denominator | BRD §13.1 | M52 |
| BR-S048 | Owned portfolio: staff operate only assigned startups; founder controls oversight | BRD §13.2 | DEC-065 |
| BR-S049 | External clients: separate tenant, role, entitlement, budgets and approved service activation | BRD §13.2 | B-SVC |
| BR-S050 | Uncertain opportunity: no guarantee of capital or sales; record evidence, human-reviewed exception, stop conditions, actual outcome | BRD §13.2 | M20, M51 |

**E. Optimization requirements (BRD §14)**

| ID | Statement | Source | Traces to |
|---|---|---|---|
| BR-S051 | OPT-03-01 Native vs paid plugins: reuse Django/Celery/Valkey and official APIs; benchmark paid alternatives; zero unapproved paid calls; full TCO comparison | BRD §14.1 | NFR-037, M05 |
| BR-S052 | OPT-04-01 Daily planning and discovery: scheduled objectives, source permissions, freshness, segments, bounded search budget; missed runs recover once; prohibited source never fetched | BRD §14.2 | M10, M11, A015 |
| BR-S053 | OPT-12-01 Qualified funnel by startup/channel/geography with numerator and denominator per stage | BRD §14.3 | M30, M52 |
| BR-S054 | OPT-12-02 Objections and next action: reason, evidence, resolution, escalation, follow-up timing; compare resolution rate and time vs baseline | BRD §14.3 | M45, KPI-28 |
| BR-S055 | OPT-12-03 Verified closure: commitment/proposal separate from verified commercial receipt and contract status; no forecast as actual (DEC-002) | BRD §14.3 | M47, M60 |
| BR-S056 | OPT-12-04 Acquisition experiments: approved cohorts and holdouts; monitor quality, opt-outs, cost; improvement vs baseline without guardrail degradation | BRD §14.3 | M38, M54 |
| BR-S057 | OPT-20-01 Unit economics: SaaS billing separate from customer receipts; allocate AI, provider, infra, support cost; contribution margin per tenant | BRD §14.4 | KPI-23 |
| BR-S058 | OPT-20-02 Entitlements and usage: versioned plans, quotas, pricing; reconcile metered usage and credits; 100% reconciled; no charge or service outside entitlement | BRD §14.4 | A101, KPI-24 |
| BR-S059 | OPT-20-03 Support and renewal: track onboarding effort, tickets, renewal/churn; no unverified SLA promise | BRD §14.4 | DEC-044 |
| BR-S060 | OPT-20-04 Client scalability and portability: self-service standard onboarding; custom needs estimated separately; export and revoke on offboard | BRD §14.4 | W32–W34, A103 |

**F. Acceptance procedures (BRD §15/§16, FRD §14/§15 merged per DEC-014)**

| ID | Statement | Source | Traces to |
|---|---|---|---|
| BR-S061 | AP-01 Onboard a synthetic 26th owned startup by template; customize offerings and commercial objectives without core code change | BRD §15 | B-TENANT, A100, A112 |
| BR-S062 | AP-02 Scope separation: owned routing AppNAI/EduVerse/MedMaarg/OrganicSpec; this product exposes no fundraising capability (DEC-002) | BRD §15 | DEC-052 |
| BR-S063 | AP-03 Opportunity qualification: eligible vs ineligible with score breakdown; only qualified enter funnel; reasons and owner visible | BRD §15 | M17, M20 |
| BR-S064 | AP-04 Closure and receipt distinction: partial then complete verified payment; reconcile ledger and closure state; no premature closure | BRD §15 | M47 |
| BR-S065 | AP-05 Sensitive data exclusions: patient and school-minor fixtures never enter acquisition workflows; no unauthorized child outreach | BRD §15 | DEC-030, X-02, X-04 |

**G. Commercial strategy and operating statements (BRD §8)**

| ID | Statement | Source | Traces to |
|---|---|---|---|
| BR-S066 | MedMaarg core product: Scanner → Planner without report; Advisor with report; wellness guidance, not diagnosis (claims must reflect this) | BRD §8 | M02, M34 |
| BR-S067 | Current traction figures (750+ users, ~150 monthly users, one Odisha location) are management claims, not audited; publish only with approved evidence | BRD §8 | DEC-021, A051 |
| BR-S068 | Commercial engine: B2C pay-per-report; B2B institutional packages; phygital deployment; SaaS/API licensing subject to readiness; preventive products/commerce planned | BRD §8 | M49, M64, M65, M66 |
| BR-S069 | GTM: start Odisha & Tamil Nadu (worldwide scope) with clinics/labs, corporate HR, warm partners; then hospital networks, institutional and insurer pilots; test before scaling | BRD §8 | M10, M38, M63 |
| BR-S070 | Insurance boundary: organization-level member wellness pilot only; no underwriting, eligibility, premium or individual profiling | BRD §8 | M63, X-03 |
| BR-S071 | Doctor Connect / Pathology Lab Connect require commercial and API readiness approval before promotion | BRD §8 | M66, M02 |
| BR-S072 | Business goal: optimize qualified opportunities, meetings, paid conversions and retention, not contact volume | BRD §8 | PP-01 |
| BR-S073 | Build/buy: build evidence matching, policy gates, CRM state, orchestration; buy licensed search, mail, WhatsApp, optional verification; defer enterprise CRM | BRD §8 | X-09, Part 3 ADRs |
| BR-S074 | Scope: multi-tenant growth system; two React apps (DEC-009); Django REST; product PostgreSQL; no medical-record storage | BRD §8 | DEC-009 |
| BR-S075 | Automation definition: automatic response/follow-up on eligible channels; policy-controlled transitions; humans for novel claims, negotiated pricing, contracts, complaints; no unrestricted sending | BRD §8 | DEC-064 |
| BR-S076 | Team/timeline assumption: lean team, 90-day foundation, 180-day rollout; validate availability (superseded by DEC-005) | BRD §8 | DEC-005 |
| BR-S077 | Implementation review uses multi-role perspectives as a checklist; no claim of independent parallel agents | BRD §8 | Cross-role reviews (Parts 3, 7, 9) |
| BR-S078 | Source limitation: 538 integration candidates screened, 53 mapped; vendor entitlement, cost, listing and India coverage need procurement validation | BRD §8 | DEC-021, Part 7 §7.5 |

**H. Phase gates (BRD §8; mapped per DEC-034)**

| ID | Statement | Source | Traces to |
|---|---|---|---|
| BR-S079 | Day 1–15 Foundation: secure environments, product truth, consent, core data model; W0 BRs tested; owner and claims sign-off | BRD §8 | W0 |
| BR-S080 | Day 16–30 Intelligence pilot: limited permitted sources; M10–M20; 100 reviewed signals; precision ≥ 80% | BRD §8 | W1 |
| BR-S081 | Day 31–60 Sales foundation: qualified opportunity, CRM, email/inbound demo, approval, follow-up; 20 qualified accounts, 5 demo requests (targets) | BRD §8 | W2 |
| BR-S082 | Day 61–90 Omnichannel: WhatsApp, website, content, social, ads with approved permissions; opt-out and replay tests pass | BRD §8 | W3 |
| BR-S083 | Day 91–120 Closure: pilot proposal, quotation, e-sign, payment/contract confirmation, onboarding; full synthetic deal and real controlled pilot | BRD §8 | W4 |
| BR-S084 | Day 121–180 Optimization: attribution, monitoring, growth, retention, additional channels; 30-day monitored pilot; budget and compliance gates | BRD §8 | W5 |
| BR-S085 | Day 181–365 Selective expansion: insurer/API and phygital only after commercial readiness; validated contract and market-fit milestones | BRD §8 | W6 |

**I. Budgets, volumes, cost lines and effort (BRD §6, §8)**

| ID | Statement | Source | Traces to |
|---|---|---|---|
| BR-S086 | Bootstrapped pilot illustrative range ₹15–60k/month excluding staff/ads/tax; superseded by B01–B11 | BRD §8 | DEC-004 |
| BR-S087 | Growth pilot illustrative ₹60–230k/month; scale only after measured consumption; not additive to B rows | BRD §8 | DEC-008 |
| BR-S088 | Engineering estimate: person-day calculation supersedes historical estimate | BRD §8 | DEC-012 |
| BR-S089 | Pilot volumes: 500 fetches/month, 100 reviewed signals, 20 qualified accounts, 5 requested demos, 2,000 emails, 1,000 WhatsApp templates; track conversion before increasing budget | BRD §8 | Part 7 sizing |
| BR-S090 | Scale gate: increase vendor spend only after verified cost per qualified opportunity, consent compliance and conversion justify it; measure India contact accuracy and opt-out compliance | BRD §8 | DEC-008, KPI-22 |
| BR-S091 | B01 AWS hosting ₹5,000/month (Django, workers, PostgreSQL, Valkey, storage, backups) | BRD §6 | DEC-020 |
| BR-S092 | B02 Production AI inference ₹3,000/month (illustrative reserve) | BRD §6 | DEC-008 |
| BR-S093 | B03 Public search API ₹1,500/month (500-fetch pilot; Tavily free credits; Exa alternative) | BRD §6 | M10, M11 |
| BR-S094 | B04 Extraction compute/overage ₹1,000/month (self-host first) | BRD §6 | M12 |
| BR-S095 | B05 Email delivery ₹500/month (2,000 eligible sends + buffer; SES) | BRD §6 | DEC-025 |
| BR-S096 | B06 WhatsApp Business ₹2,000/month (1,000 chargeable templates illustrative; verify pricing) | BRD §6 | M31 |
| BR-S097 | B07 Monitoring/security/CI ₹500/month (incremental) | BRD §6 | DEC-041 |
| BR-S098 | B08 Apollo paid enrichment reserve ₹9,000/month (optional cap, not confirmed price; free pilot first) | BRD §6 | L-09 |
| BR-S099 | B09 Claude Code developer seats ₹3,600/month (2 × $20 × ₹90; may be zero if existing seats) | BRD §6 | ASSUMPTION-020 |
| BR-S100 | B10 Optional integration reserve ₹1,000/month (calendar, social, validation, meetings, e-sign pilots) | BRD §6 | DEC-020 |
| BR-S101 | B11 Contingency 15% on selected monthly budgets | BRD §6 | DEC-004 |
| BR-S102 | Effort: 66 original commercial modules 194–323 person-days | BRD §6 | Part 8 |
| BR-S103 | Effort: tenant and independent SaaS controls 35–60 person-days | BRD §6 | Part 8 |
| BR-S104 | Effort: four-vertical projects, orders and fulfilment 30–52 person-days | BRD §6 | Part 8 |
| BR-S105 | Effort: autonomous planning, portability and independent QA 28–48 person-days | BRD §6 | Part 8 |

**J. Website surfaces and new interfaces (BRD §9, §17)**

| ID | Statement | Source | Traces to |
|---|---|---|---|
| BR-S106 | Website-Public: anonymous visitors see approved pages and bounded enquiry forms; no private contacts or internal financials | BRD §9 | B-WEB, P15 |
| BR-S107 | Website-Portal: authenticated external customer/supplier sees own permitted records; identity-bound grants; field minimization; no staff permissions | BRD §9 | B-WEB, P14 |
| BR-S108 | Admin: assigned employees and authorized management; confidential Command Centre, evidence, workflows, approvals | BRD §9 | All A-screens |
| BR-S109 | Internal/callback: service identities and verified providers; no browser access; signature and idempotency checks | BRD §9 | P16, M06 |
| BR-S110 | W31 SaaS introduction, plans & demo: separate from customer journey; no fundraising offers or implied outcomes; approved service terms only | BRD §17 | B-SVC, DEC-047 |
| BR-S111 | W32 Startup & third-party client registration: prove administrator authority; no provisioning before verified identity and approval | BRD §17 | B-SVC, FRD §16.3 |
| BR-S112 | W33 AI business onboarding & configuration wizard: configure without core code; AI proposals unverified; no dispatch or spend during onboarding | BRD §17 | B-SVC, AP-01 |
| BR-S113 | W34 SaaS client service portal: subscription and service lifecycle; client-only scoped billing; no cross-tenant records | BRD §17 | B-SVC |
| BR-S114 | A109 Event & Trigger Management Centre: event definitions, timers, webhooks; verify signatures and scope; dedupe; never replay a live side effect | BRD §17 | B-AUTO |
| BR-S115 | A110 Live Automation Execution Monitor: concurrent runs, step history; pause/resume revalidate; unknown outcome reconciles before retry | BRD §17 | B-AUTO |
| BR-S116 | A111 Automation Coordination & Conflict Resolution: resolve conflicting actions; no unrelated tenant data; idempotency and policy before dispatch | BRD §17 | B-AUTO |
| BR-S117 | A112 Business Configuration Change Centre: version comparison, safe rollout; running revisions immutable; no authorization expansion without review | BRD §17 | B-TENANT |
| BR-S118 | A113 Automation Template & Node Library: approved nodes only; no arbitrary code or secrets; immutable published versions | BRD §17 | B-AUTO, DEC-051 |

**K. Platform principles and governance statements (second-pass additions, DEC-059)**

| ID | Statement | Source | Traces to |
|---|---|---|---|
| BR-S119 | Deploy as an independent application (origin, API audience, membership, DB, storage/vector, queues, credentials, budget, billing, audit, backup); shared libraries allowed; confidential data not shared | BRD §1 | NFR-031, CN-02 |
| BR-S120 | Two distinct React frontends with separate origins, sessions, OAuth clients/audiences, route allowlists and builds; no Admin JS or private data in public bundles | BRD §1 | NFR-001, DEC-009 |
| BR-S121 | Tenancy: tenant = customer/security/billing boundary; startup = legal-entity workspace; 25+ owned startups and unrelated tenants; owner group view read-only for mutations; scoped, time-limited, audited support access | BRD §1 | DEC-055, DEC-056, DEC-065 |
| BR-S122 | Execution principles: open-source first; developer plugins are not runtime entitlements; Manual/Assisted/Supervised/Controlled Autonomous; simulation zero live effects; recheck scope, policy, eligibility, approved hash, budget and role at execution; one dependency-ordered plan | BRD §1.2 | ASSUMPTION-010, DEC-006 |
| BR-S123 | Server-side permission on every object, nested FK, search, vector retrieval, export, notification, worker and webhook; claims from current membership; separate sender credentials, budget ledgers, backups | BRD §2 | NFR-002 |
| BR-S124 | Command Centre persistent features: action centre, notifications, approved Copilot, saved views, budget, automation status, authorized stop; reusable panels/drawers; scope retained on navigation | BRD §3 | A106, DEC-035 |
| BR-S125 | Engine pattern: validated event → scope → immutable revision → permission → deterministic eligibility → budget reservation → approved action → outbox → worker → provider reconciliation → projection → notification; store correlation, attempt, error, actual side effect; no AI direct finance or binding terms; stop/pause/resume checks role, reply/opt-out, hash, entitlement, cap | BRD §5 | M06, M55, RECOMMENDATION-012 |
| BR-S126 | Routing: retain legacy contracts; separate website and Admin ingress allowlists, serializers and permission classes; new endpoints under `/api/v1/commercial/{public,portal,admin}/`; default deny; CORS is not authorization | BRD §9 | CN-15 |
| BR-S127 | Publication: verified domain maps to exactly one tenant/startup; unknown host 404; immutable snapshots with locale/slug/revision; expiring preview grants, no indexing; atomic publish/unpublish; tenant-keyed cache invalidation; scanned assets; portal content never in public snapshot/CDN | BRD §9 | NFR-020, A107, A108 |
| BR-S128 | Operational separation: public intake creates a scoped durable event and outbox, never a direct business approval; workers recheck identity, eligibility, policy, budget, duplicates, approval | BRD §9 | M22, M06 |
| BR-S129 | Estimate update: website templates, portal authorization adapters, publication storage/CMS, cache/CDN, accessibility and cross-boundary tests estimated independently; no multiplication by startup count | BRD §9 | Part 8 |
| BR-S130 | Website outcomes: measure public qualified enquiries and portal completion independently; each legal entity approves its own public content; client tenants publish only verified sites; attribution only where permitted | BRD §9.1 | KPI-26 |
| BR-S131 | Cost-efficient policy: core discovery, orchestration, CRM, approvals, follow-up, reporting and admin built in the open-source stack; measure gap vs self-hosted/first-party before buying; paid fallback disabled by default with separately approved budget | BRD §10 | NFR-037 |
| BR-S132 | Acceptance requires positive and negative unit, SIT and UAT evidence for Website, Portal and Admin; no launch on failed confidentiality, unauthorized action, payment accuracy, regulatory eligibility or rollback checks; auth reuse still needs compatibility tests | BRD §10 | B-QA, DEC-019 |
| BR-S133 | Commercial scope statement: AppNAI global external AI projects; MedMaarg AI Hospital partnerships; EduVerse education/products/services; OrganicSpec buy/sell/services/training; employee access by role and startup | BRD §10 | DEC-052 |
| BR-S134 | Product owner approves objectives, eligibility, outcomes and exclusions before engineering; changes identify affected journey, UI, API, persistence, cost and tests; no promise of conversion as acceptance | BRD §11 | Change control (Part 8) |
| BR-S135 | Delivery evidence recorded against build, environment, scope, reviewer, approval; open critical confidentiality, financial integrity or unauthorized-action defects block activation; targets and allowances provisional until measured | BRD §11 | B-QA, Part 6 severity |
| BR-S136 | Evidence record fields: responsible/reviewer, artefact/test evidence, decision (Pending/Pass/Fail/approved N/A), remediation, business acceptance | BRD §12.2 | Part 6 evidence template |
| BR-S137 | Boundary conditions: independent product/tenant/startup/principal scope per action; revalidate at execution; two-tenant fixture denies cross-scope access, rejects stale grants, verifies correct scope; record positive, denial and recovery evidence | BRD §16 | AP-10, NFR-032 |
| BR-S138 | Scope and business value: dynamic startup/tenant onboarding, independent SaaS clients, multiple scoped objectives; no new core code per ordinary startup; measure verified outcomes | BRD §17.1 | PP-10 |
| BR-S139 | SaaS billing model: approved plans and trial/usage quotas; metered base + included usage + approved overage; separate product billing and invoice evidence; margin = recognized fee − attributable cost; append-only credits/adjustments; suspension on expiry; export; regulated retention; managed-service/success fees need contractual and regulatory review | BRD §6 | B-SVC, DEC-047 |
| BR-S140 | Release condition: approved screen/contract/entity decisions, executed expanded tests, QC and acceptance evidence; no production approval implied by the specification | BRD §17 | M62, B-QA |

**Count check:** 5 + 14 + 14 + 17 + 10 + 5 + 13 + 7 + 20 + 13 + 22 = **140** ✔ (DEC-059).

### 1.12.3 Business requirement coverage summary

| Category | Count | Mapped to an epic (prelim.) | Mapped to a persona | Mapped to a wave |
|---|---|---|---|---|
| Primary (BR-M, BR-B) | 71 | 71 (100%) | 71 (100%) | 71 (100%) |
| Supplementary (BR-S) | 140 | 140 (100%) via primary BR/workflow/DEC links | n/a (inherit) | n/a (inherit) |

---

## 1.13 Benefits and value hypotheses

| ID | Hypothesis | Leading indicator | Lagging indicator | Validation point |
|---|---|---|---|---|
| VH-01 | Evidence-based discovery cuts research time per qualified account by ≥ 50% vs manual | Reviewed signals/hour | Qualified accounts per FTE-week | End W1 (time study) |
| VH-02 | Rules-first eligibility removes compliance incidents without reducing reply rate | Suppression breaches (0) | Complaint rate, reply rate | End W3 |
| VH-03 | Approved templates and AI drafts halve proposal turnaround | Draft → approval time | Win rate | End W4 |
| VH-04 | Verified closure eliminates revenue disputes and double counting | Closure integrity (0 violations) | Finance reconciliation effort | End W5 |
| VH-05 | Template-based onboarding makes adding a startup a ≤ 1-day configuration task | Config validation pass rate | KPI-25 | W6 (AP-01) |
| VH-06 | Caching, batching and model tiering keep AI cost ≤ ₹3,000/month at pilot volumes | AI cost per task | AI cost per qualified opportunity | Monthly from W1 |

---

## 1.14 ID registry (v1)

| Prefix | Meaning | Range allocated so far | Owner part |
|---|---|---|---|
| BR-M## / BR-TENANT / BR-WEB / BR-AUTO / BR-SVC / BR-QA | Primary business requirements | 71 IDs | Part 1 |
| BR-S### | Supplementary business requirements | S001–S140 | Part 1 |
| FR-W## / FR-A### / FR-OP### / FR-UX-… / FR-FLT / FR-STD / FR-DM / FR-UIS / FR-ENG / FR-PUB | Functional requirements | Reserved (150 + 147 + 32) | Part 2 |
| NFR-### | Non-functional requirements | 001–038 extracted; extension in Part 4 | Parts 0, 4 |
| DEC-### | Decisions | 001–065 | Part 0A |
| PP-## | Product principles | 01–12 | Part 1 |
| PR-## | Problem statements | 01–10 | Part 1 |
| G-## / KPI-## / O# / KR#.# | Goals, KPIs, objectives, key results | G-01–10; KPI-01–31; O1–O4 | Part 1 |
| P## | Personas | P01–P16 (P14a–d) | Part 1 |
| J-## | Journeys | J-01–J-49 (subset used) | Parts 1–2 |
| WF-## | Workflows | 01–14 | Part 0 |
| SH-## / CN-## / DP-## / X-## / L-## / VH-## | Stakeholders, constraints, dependencies, exclusions, later items, value hypotheses | As listed | Part 1 |
| AP-## | Acceptance procedures | 01–10 | Part 0A |
| BRL-### | Business rules | Reserved | Part 2 |
| EP-## / US-### / AC-### | Epics, stories, acceptance criteria | EP-01–21 prelim. | Part 5 |
| TS-### / TC-### | Test scenarios, test cases | Reserved | Part 6 |
| AG-### / AU-### | AI agents, automations | Reserved | Part 7 |
| ADR-### | Architecture decisions | Reserved | Part 3 |
| RSK-### | Risks | Reserved | Part 8 |
| RECOMMENDATION-### | Added best practice | 001–019 | Running |

**New recommendation in this part:** [RECOMMENDATION-019] Numeric targets for KPIs the source left unquantified (KPI-03, KPI-04, KPI-12, KPI-18, KPI-25). Each is marked as a recommendation, measured against a baseline first, and adjustable by the Product Owner.

---

## 1.15 Quality gate: Part 1

| # | Check | Result | Fixes applied / notes |
|---|---|---|---|
| 1 | Every requirement traced to a source section | **Pass** | All 71 primary and 140 supplementary BRs cite BRD §; derived personas labelled |
| 2 | Assumptions, gaps, conflicts tagged and logged | **Pass** | Decisions cited (DEC-###); RECOMMENDATION-019 added and tagged |
| 3 | IDs unique and consistent with earlier parts | **Pass** | Supplementary BR count updated from 118 → 140 consistent with DEC-059; epic IDs match Part 0 §0.10.2 |
| 4 | No story lacks AC; no requirement lacks a test | **N/A (Part 1)** | BR acceptance statements captured as the basis for test design (Part 6) |
| 5 | Negative, edge, security, accessibility considered | **Pass** | Exclusions X-01–X-12, principles PP-03/PP-11, safety-related BR acceptances retained verbatim |
| 6 | Agents have guardrail, fallback, KPI, cost | **N/A (Part 7)** | AI budget ceilings fixed (DEC-008) |
| 7 | Time-sensitive facts flagged "verify" | **Pass** | Provider shortlists, prices, regulatory items marked verify (inherited DEC) |
| 8 | No restricted data to free-tier models | **Pass** | DEC-007 restated in executive summary context |
| 9 | Consistent with earlier parts | **Pass** | MoSCoW and waves consistent with DEC-034/060–063; one correction noted (BR-S count) |

**Self-review corrections made in this part:**
1. M66 was first placed only in W6; it was split into a W0 gate plus a W6 workflow (DEC-060).
2. BR-AUTO was first marked "Should"; it was split, because Manual through Supervised modes, simulation and the emergency stop are prerequisites of M55/M28 and are therefore Must in W2.
3. KPI-06 was redefined as *held* meetings, not *booked* meetings, to match "actual meetings" (BRD §4).

---

**Status: Part 1 of 10 complete. Next: Part 2 (Functional design: modules, process flows, business rules, RBAC, state machines, UX/UI). Reply "continue".**
