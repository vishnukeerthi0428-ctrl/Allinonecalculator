# Document control

| Version | Date | Author / authority | Change |
|---|---|---|---|
| 0.1 | 27 Nov 2026 | Blueprint team (virtual enterprise team) | Part 0: ingestion and validation of BRD and FRD |
| 0.2 | 27 Nov 2026 | Delegated Product Owner authority | Part 0A: 65 decisions resolving all conflicts, gaps and open questions |
| 0.3–0.9 | 27 Nov 2026 | Blueprint team | Parts 1–8 drafted, reviewed and rendered |
| 1.0 | 27 Nov 2026 | Blueprint team | Part 9 errata (DEC-066…140), registers, final quality report; Part 10 assembly (this document) |

| Item | Value |
|---|---|
| Inputs | 01 Business Requirements (BRD), 02 Functional Specification (FRD) |
| Classification | Confidential: internal and authorized delivery partners |
| Decision authority | Product Owner delegated decision-making to the blueprint team (27 Nov 2026). Every decision is listed (DEC-001…140) and can be overridden through change control (BRD §11) |
| Precedence | Part 9.1 errata decisions override conflicting text in earlier parts; Part 0A decisions override the source documents where they resolve conflicts or gaps |
| Time-sensitive facts | Prices, model names, free tiers, provider terms and regulatory dates are marked "verify at time of implementation (as of 27 Nov 2026)" |

# Executive summary

**What we are building.** The **AI Growth Engine** is an independently deployed, multi-tenant, configuration-driven platform. Employees of 25+ owned startups, and of independently onboarded client companies, use it to find, win, deliver and renew commercial business:
- market and tender discovery;
- evidence-based qualification;
- compliant omnichannel outreach;
- content and campaigns;
- proposals, quotations and contracts;
- orders and fulfilment;
- verified payment closure, onboarding and renewal.

The four seed businesses are AppNAI (global AI project bids), MedMaarg (institutional wellness partnerships, with no patient data), EduVerse (education, with no direct outreach to minors) and OrganicSpec (agri buy/sell, with separate receivable and payable ledgers). Fundraising and investor activity are out of scope.

**How it works.** The platform has two React frontends:
- a public **Website and Portal** (34 screens);
- a confidential **Admin Command Centre** (113 screens in seven views).

Behind them sits a **Django modular monolith** on AWS Mumbai, with PostgreSQL row-level security, Celery/Valkey workers and a transactional outbox. A deterministic **Policy Decision Point** rechecks scope, consent, jurisdiction, budget and the approval hash at the moment of every external action.

**AI** drafts, classifies, extracts and matches through a model gateway:
- rules and cache first;
- then Claude Haiku-class for simple, high-volume tasks;
- then Claude Sonnet for complex or customer-facing work;
- free fallbacks only for non-personal data;
- otherwise graceful degradation.

AI never signs, pays, submits bids or sets prices.

**What the blueprint contains.**

| Area | Count |
|---|---|
| Business requirements | 71 primary + 140 supplementary, traced to source |
| Functional requirements | 181 (150 interface/operation + 31 cross-cutting) |
| Business rules | 161 |
| Roles | 20 |
| State machines | 38 |
| Screens, each described | 147 |
| Data entities | 199 |
| API operations | 555 |
| Architecture decision records | 70 |
| Non-functional requirements | 99 |
| Security threats | 82 |
| User stories | 230, with about 1,357 Gherkin scenarios |
| Test cases | ≈ 2,900+ functional plus 774 AI/automation evaluation cases |
| AI agents and automations | 79, each with guardrails, fallbacks, KPIs and costs |
| Decisions | 140 |

**Delivery.**
- **Team:** 4 engineers + QA (1.0 FTE from Sprint 3) + a growth/compliance lead (0.5–0.75), with the founder as Product Owner.
- **Effort:** **314 / 416 / 518 person-days** (low/central/high) against the BRD envelope of 287–483. The central cost is **₹18.9–28.4 lakh**.
- **Timeline:** foundation gates at **Day 15** and **Day 30**; **Release 1 go/no-go about Day 152** (about Day 124 with an optional ₹5.5–8.3 L acceleration); **Release 2 built by Day 180**; 30-day monitored pilot exit about Day 201; selective expansion to Day 365.
- **Run cost:** **₹19,665–22,885 per month** including contingency at pilot scale. AI inference is about **₹1,150 per month** at base against a **₹3,000** hard ceiling, with gated ceilings of ₹12,000 and ₹40,000 for growth.

**Top risks and mitigations.**

| Risk | Mitigation |
|---|---|
| Pending legal confirmations (DPDP, children's data, global outreach rules) | Legal backlog in Sprint 0; fail-closed jurisdiction rules |
| Front-loaded Release 1 scope | Re-baselined plan; MoSCoW deferral; optional acceleration |
| QA and UAT capacity | QA uplift; UAT plan per wave |
| Founder approval bottleneck | Delegation rules; approval SLAs |
| Provider onboarding lead times (email, WhatsApp, payments) | Requests started in Sprint 0 |

**Decisions needed from the owner (confirm or override).**
1. Accept the re-baselined schedule, or fund the acceleration (DEC-124).
2. Confirm the QA uplift and the 0.75 growth/compliance allocation in W4–W5 (DEC-132/133).
3. Confirm the revised monthly run budget (DEC-128).
4. Obtain the legal confirmations listed in Part 8.

All other decisions are recorded and can proceed as defaulted.

# How to read this document

| Part | Purpose | Primary readers |
|---|---|---|
| 0 / 0A | Inventory of requirements; resolution of conflicts and gaps (DEC-001…065) | Everyone |
| 1 | Vision, goals, KPIs, scope, personas, business requirement register | Founder, startup heads, PO |
| 2 (2.1–2.5) | Functional design: modules, FR register, flows, business rules, roles, state machines, cross-cutting functions, UX/UI | BSA, engineers, UX, QA |
| 3 (3.1–3.3) | Architecture, API and integration, data | Architects, engineers, DBA |
| 4 (4.1–4.3) | Security and compliance, NFRs, DevOps and operations | Security, SRE, engineers |
| 5 | Epics and user stories with Gherkin acceptance criteria | Scrum team, PO |
| 6 | Test strategy, test cases, AI evaluations, traceability | QA, engineers, PO |
| 7 | AI agents and automations: catalogue, specs, model strategy, cost, governance | AI lead, engineers, FinOps, compliance |
| 8 | Delivery plan: roadmap, releases, sprints, team, risks, go-live, hypercare, budget | Founder, PO, delivery lead |
| 9 | Errata decisions, glossary, registers, final quality report | Everyone |

**Conventions.**
- Sources are cited as *BRD §n / FRD §n* (numbering per Part 0 §0.1.2).
- Additions beyond the source are tagged **[ASSUMPTION / GAP / CONFLICT / RECOMMENDATION-###]**.
- Cost figures are estimates, with their formulas shown.
