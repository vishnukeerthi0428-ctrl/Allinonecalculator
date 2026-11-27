# Document control

| Version | Date | Author / authority | Change |
|---|---|---|---|
| 0.1 | 27 Nov 2026 | Blueprint team (virtual enterprise team) | Part 0: ingestion and validation of BRD and FRD |
| 0.2 | 27 Nov 2026 | Delegated Product Owner authority | Part 0A: 65 decisions resolving all conflicts, gaps and open questions |
| 0.3–0.9 | 27 Nov 2026 | Blueprint team | Parts 1–8 drafted, reviewed and rendered |
| 0.95 | 27 Nov 2026 | Blueprint team | Part 9 errata (DEC-066…156), registers, final quality report |
| 1.0 | 27 Nov 2026 | Blueprint team + Founder | Full 38-document source-pack review (Part 0B and ten enhancement parts); decisions DEC-157…227 (Part 9.5); Founder approval of Option 2b (DEC-228); Part 10 assembly (this document) |

| Item | Value |
|---|---|
| Inputs | The complete 38-document engineering package (01 BRD, 02 FRD, 03–36 domain specifications, 37 illustrative workflow, 38 all numbers). Coverage of every document is reported in Part 0B |
| Classification | Confidential: internal and authorized delivery partners |
| Decision authority | Product Owner delegated decision-making to the blueprint team (27 Nov 2026). Every decision is listed (DEC-001…228) and can be overridden through change control (BRD §11) |
| Precedence | Later decisions override earlier text: Part 9.5 (DEC-157…228) > Part 9.1 (DEC-066…156) > Part 0A (DEC-001…065) > earlier part text > source documents, where a decision resolves a conflict or gap |
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
| Data entities | 199 + source-pack additions (Part 3.6); all 155 source tables and 799 columns reconciled |
| API operations | 579 (555 + 24 from the source-pack API catalogue), with field-level contracts for every source operation |
| Architecture decision records | 70 |
| Non-functional requirements | 99 |
| Security threats | 82 |
| User stories | 230, with about 1,357 Gherkin scenarios |
| Test cases | 2,912 (2,138 functional, NFR, filter and BR-S + 774 AI/automation evaluations) plus 48 verification items; **100% traceability at every level** |
| AI agents and automations | 90 (38 agents + 52 automations), each with guardrails, fallbacks, KPIs and costs; plus a 100-use-case automation library |
| Decisions | 228 |
| Source-pack coverage | 11,269 aspects of the 38 documents reviewed line by line; every gap and conflict addressed (Part 0B) |
| Optimization model | 21 dimensions, 104 controls, 24 scenarios, 35 optimization KPIs OKPI-01…35 (21 mandatory) |

**Delivery.**
- **Team (approved, DEC-228):** 4 engineers + **2 contract engineers from Sprint 3 to the Release 2 build gate** + QA (1.0 FTE from Sprint 3) + a growth/compliance lead (0.5–0.75), with the founder as Product Owner.
- **Effort:** **532 / 722 / 921 person-days** (low/central/high). That is the original plan (314 / 416 / 518) plus the net source-pack enhancements (218 / 306 / 403). Must items go into Releases 1–2; about 100 pd of Should/Could items go to W6. The central figure is about 49% above the BRD's 483 pd, mainly because of the engineering controls that documents 18–36 require.
- **Timeline (plan of record):** foundation gates at **Day 15** and **Day 30**; **Release 1 go/no-go Fri 4 Jun 2027 (Day 180)**; **Release 2 built Fri 2 Jul 2027 (Day 208)**; W5 exit after the 30-day monitored pilot **Fri 23 Jul 2027 (Day 229)**; selective expansion thereafter.
- **Programme cash to the Release 2 gate:** **₹53.6–85.1 lakh** (estimate, including the contract engineers at ₹10.9–16.4 L).
- **Run cost:** **₹19,665–22,885 per month** including contingency at pilot scale (plus ₹230–3,450 from the enhancements). AI inference is about **₹1,150 per month** at base against a **₹3,000** hard ceiling, with gated ceilings of ₹12,000 and ₹40,000 for growth.

**Top risks and mitigations.**

| Risk | Mitigation |
|---|---|
| Pending legal confirmations (DPDP, children's data, global outreach rules) | Legal backlog in Sprint 0; fail-closed jurisdiction rules |
| Scope growth from the source pack (722 pd central) | Option 2b contract engineers (DEC-228); MoSCoW triage with Should/Could to W6; Sprint 3 and Sprint 7 estimate reviews |
| QA and UAT capacity | QA uplift; UAT plan per wave |
| Founder approval bottleneck | Delegation rules; approval SLAs |
| Provider onboarding lead times (email, WhatsApp, payments) | Requests started in Sprint 0 |

**Decisions needed from the owner (confirm or override).**
1. ~~Choose the staffing option~~: **done; Option 2b approved (DEC-228).** Start procuring the two contract engineers in Sprint 0.
2. Confirm the QA uplift and the 0.75 growth/compliance allocation in W4–W5 (DEC-132/133).
3. Confirm the revised monthly run budget (DEC-128 and Part 9.5 §9.5.2.6).
4. Confirm the reading of the source pack's "+5 business requirements" as expansion statements XBR-01…05 (Part 9.5, ASSUMPTION-506).
5. Obtain the legal confirmations listed in Part 8.

All other decisions are recorded and can proceed as defaulted.

# How to read this document

| Part | Purpose | Primary readers |
|---|---|---|
| 0 / 0A / 0B | Inventory of requirements; resolution of conflicts and gaps (DEC-001…065); coverage of the 38-document source pack | Everyone |
| 1 | Vision, goals, KPIs, scope, personas, business requirement register | Founder, startup heads, PO |
| 2 (2.1–2.7) | Functional design: modules, FR register, flows, business rules, roles, state machines, cross-cutting functions, UX/UI | BSA, engineers, UX, QA |
| 3 (3.1–3.6) | Architecture, API and integration, data, with source-pack architecture/API/data reconciliation | Architects, engineers, DBA |
| 4 (4.1–4.4) | Security and compliance, NFRs, DevOps and operations, coding standards | Security, SRE, engineers |
| 5 | Epics and user stories with Gherkin acceptance criteria | Scrum team, PO |
| 6 (6.1–6.10) | Test strategy, test cases, AI evaluations, traceability, source-pack test/QC/RTM reconciliation | QA, engineers, PO |
| 7 (7.1–7.4) | AI agents and automations: catalogue, specs, model strategy, cost, governance, prompts/RAG/plugins | AI lead, engineers, FinOps, compliance |
| 8 (8.1–8.3) | Delivery plan: roadmap, releases, sprints, team, risks, go-live, hypercare, budget; training manual, SaaS service, maintenance, optimization | Founder, PO, delivery lead |
| 9 (9.1–9.5) | Errata decisions, glossary, registers, final quality report, AI/workflow catalogue, source-pack decisions and re-plan | Everyone |

**Conventions.**
- Sources are cited as *BRD §n / FRD §n* (numbering per Part 0 §0.1.2).
- Additions beyond the source are tagged **[ASSUMPTION / GAP / CONFLICT / RECOMMENDATION-###]**.
- Cost figures are estimates, with their formulas shown.
