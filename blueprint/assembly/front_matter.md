# Document control

| Version | Date | Author / authority | Change |
|---|---|---|---|
| 0.1 | 27 Nov 2026 | Blueprint team (virtual enterprise team) | Part 0: ingestion and validation of BRD and FRD |
| 0.2 | 27 Nov 2026 | Delegated Product Owner authority | Part 0A: 65 decisions resolving all conflicts, gaps and open questions |
| 0.3–0.9 | 27 Nov 2026 | Blueprint team | Parts 1–8 drafted, reviewed and rendered |
| 0.95 | 27 Nov 2026 | Blueprint team | Part 9 errata (DEC-066…156), registers, final quality report |
| 1.0 | 27 Nov 2026 | Blueprint team + Founder | Full 38-document source-pack review (Part 0B and ten enhancement parts); decisions DEC-157…227 (Part 9.5); Founder approvals of Option 2b (DEC-228), both budgets, the QA/growth uplift and the XBR reading (DEC-230…233); Part 10 assembly (this document) |
| 1.1 | 28 Nov 2026 | Blueprint team + expert panels + Founder | **100% literal match** with the 38-document source pack (Parts 9.6a/b, DEC-234…270 and DEC-300…332); **advanced capabilities** from three expert panels: AI agents (Part 9.7), revenue growth (Part 9.8), platform, data, security and experience (Part 9.9); consolidation, roadmap A1–A3 and separately approvable budget (Part 9.10, DEC-410…415); Founder decisions 28 Nov 2026: alignment funded (DEC-416), advanced A1 approved (DEC-417), **Claude Sonnet kept as primary model** (DEC-418) |

| Item | Value |
|---|---|
| Inputs | The complete 38-document engineering package (01 BRD, 02 FRD, 03–36 domain specifications, 37 illustrative workflow, 38 all numbers). Coverage of every document is reported in Part 0B |
| Classification | Confidential: internal and authorized delivery partners |
| Decision authority | Product Owner delegated decision-making to the blueprint team (27 Nov 2026). Every decision is listed (DEC-001…233, DEC-234…270, DEC-300…332, DEC-380…418) and can be overridden through change control (BRD §11) |
| Precedence | Later decisions override earlier text: Part 9.10 (DEC-410…418) > Parts 9.6–9.9 (DEC-234…409) > Part 9.5 §9.5.2.9 (DEC-230…233) > Part 8.4 (DEC-229) > Part 9.5 (DEC-157…228) > Part 9.1 (DEC-066…156) > Part 0A (DEC-001…065) > earlier part text > source documents, where a decision resolves a conflict or gap |
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
| Test cases | 2,912 (2,138 functional, NFR, filter and BR-S + 774 AI/automation evaluations) + 952 enhancement cases (TC-ENH, including 64 closure cases in Part 6.10) plus verification items; 799 source-pack tests mapped; **100% traceability at every level, including the 38-document source pack** |
| AI agents, automations and workflows | **80 agents, 119 automations and 38 workflows** (v1.0: 38 + 52 + 14; v1.1 advanced: 42 + 67 + 24), each with guardrails, fallbacks, KPIs and costs; plus a 100-use-case automation library |
| Decisions | 342 (v1.0: 233; v1.1: 37 + 33 literal-alignment decisions, 30 expert-panel decisions, 9 consolidation and Founder decisions) |
| Source-pack match | 11,269 aspects of the 38 documents reviewed line by line. **Literal match 99.98%: 11,129 of 11,131 applicable aspects**, with 138 confirmed not applicable. All 141 conflicts were aligned (Parts 9.6a/b). The two remaining aspects (local model in front of Claude) are Founder-approved deviations: Claude Sonnet stays primary (DEC-418). Every applicable aspect has an approved disposition (Part 0B §0B.7) |
| Advanced capabilities (v1.1) | 94 capabilities from 17 expert personas; 240 FR-ADV, 96 stories, 258 TC-ADV and 91 TC-ALN tests, 71 screens; 100% traced (Part 9.10 §9.10.8) |
| Optimization model | 21 dimensions, 104 controls, 24 scenarios, 35 optimization KPIs OKPI-01…35 (21 mandatory) |

**Delivery.**
- **Team (approved, DEC-228):** 4 engineers + **2 contract engineers from Sprint 3 to the Release 2 build gate** + QA (1.0 FTE from Sprint 3) + a growth/compliance lead (0.5–0.75), with the founder as Product Owner.
- **Effort:** **532 / 722 / 921 person-days** (low/central/high). That is the original plan (314 / 416 / 518) plus the net source-pack enhancements (218 / 306 / 403). Must items go into Releases 1–2; about 100 pd of Should/Could items go to W6. The central figure is about 49% above the BRD's 483 pd, mainly because of the engineering controls that documents 18–36 require.
- **Timeline (plan of record):** foundation gates at **Day 15** and **Day 30**; **Release 1 go/no-go Fri 4 Jun 2027 (Day 180)**; **Release 2 built Fri 2 Jul 2027 (Day 208)**; W5 exit after the 30-day monitored pilot **Fri 23 Jul 2027 (Day 229)**; selective expansion thereafter.
- **Costs are kept in two separate ledgers (DEC-229, Part 8.4):**

  | Ledger | What it covers | Estimate |
  |---|---|---|
  | **A. Development cost (one-time)** | Core team, 2 contract engineers, QA, DevOps, UX, growth/compliance lead, penetration tests, training content, to the Release 2 gate (Day 208) | **₹52.7–84.1 lakh** |
  | A2. Phase-2 development (W6, optional, approved separately) | Deferred Should/Could scope and expansion, Day 209–365 | ₹25.8–38.7 lakh |
  | **B. Subscriptions and running cost (recurring)** | AWS hosting, backups, CDN/WAF, AI usage (hard-capped), search/extraction/email/WhatsApp providers, monitoring/CI tools | **₹19,895–26,335 per month** (≈ ₹2.4–3.2 lakh per year); ₹24,035–30,475 with developer seats |
  | B during the build | Running cost paid while building (Day 1–208) | ₹1.5–1.9 lakh |

  At pilot scale about 97% of the money to reach Release 2 is development. AI inference is expected at about ₹1,150 per month against a ₹3,000 hard cap, with gated ceilings of ₹12,000 and ₹40,000 for growth. Running costs rise only after the scale gates: ≈ ₹50–70 thousand/month at the Year-1 design point and ≈ ₹1.3–1.7 lakh/month at Year 2.

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
2. ~~Confirm the QA uplift and the 0.75 growth/compliance allocation in W4–W5~~: **done; confirmed (DEC-232).**
3. ~~Approve the two budgets~~: **done; Ledger A development ₹52.7–84.1 L approved (DEC-230) and Ledger B running cost ₹19,895–26,335 per month approved (DEC-231).**
4. ~~Confirm the reading of the "+5 business requirements" as XBR-01…05~~: **done; confirmed (DEC-233).**
5. Obtain the legal confirmations listed in Part 8.
6. ~~v1.1 decisions~~ (Part 9.10 §9.10.10), **all done on 28 Nov 2026:**
   - Release 1 alignment work funded: CR-ALN-01 ₹2.79–11.64 L (DEC-416). Dates unchanged.
   - Advanced A1 approved at ≈ ₹28.0–55.4 L one-time (DEC-417). A2 and A3 are decided at their gates.
   - **Claude Sonnet kept as primary model** (DEC-418).

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
| 8 (8.1–8.4) | Delivery plan: roadmap, releases, sprints, team, risks, go-live, hypercare, budget; training manual, SaaS service, maintenance, optimization; **cost model with development and subscription costs separated** | Founder, PO, delivery lead |
| 9 (9.1–9.5) | Errata decisions, glossary, registers, final quality report, AI/workflow catalogue, source-pack decisions and re-plan | Everyone |

**Conventions.**
- Sources are cited as *BRD §n / FRD §n* (numbering per Part 0 §0.1.2).
- Additions beyond the source are tagged **[ASSUMPTION / GAP / CONFLICT / RECOMMENDATION-###]**.
- Cost figures are estimates, with their formulas shown.
