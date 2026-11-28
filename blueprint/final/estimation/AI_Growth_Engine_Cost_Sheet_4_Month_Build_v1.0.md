# AI Growth Engine: 4-Month Build Cost Sheet
## Core platform + Advanced A1 · solo builder with AI models and AI agents · delivered in 4 months

| Field | Value |
|---|---|
| Prepared for | [Client name] |
| Prepared by | [Your name / company] |
| Version and date | 4-month cost sheet v1.0 · 28 Nov 2026 |
| Validity | 30 days |
| Basis | Application Blueprint v1.1 (346 decisions; Claude Sonnet primary DEC-418; Vercel + Supabase + AWS Mumbai DEC-421; running budget DEC-422); Final Cost Sheet v1.1 |
| Currency | INR; GST 18% shown separately; USD items at ₹90 = $1 (verify) |

**Important.** The blueprint's estimate for one builder is about 44 months. Delivering in 4 months assumes the AI agents carry out almost all implementation, so the builder needs about 11 times the productivity assumed there. This sheet shows the **cost** of delivering in 4 months. It is not a recommendation that 4 months is achievable, and it is not the price to charge: the value of the same scope is ₹90,00,000 (Final Cost Sheet v1.1).

# 1. Summary

| Part | What it covers | Amount (excl. GST) | GST 18% | Amount (incl. GST) |
|---|---|---|---|---|
| **A. One-time build cost** | Builder's time, AI coding-agent tokens, contingency, security testing | **₹21,28,308** | ₹3,83,095 | ₹25,11,403 |
| **B. Subscriptions while building (months 1–4)** | Builder's AI and dev tools; client's Vercel, Supabase, AWS, domains | **₹1,58,040** | ₹28,447 | ₹1,86,487 |
| **C. Subscriptions and services after building (first 12 months)** | Running the application + maintenance retainer | **₹10,41,568** | ₹1,87,482 | ₹12,29,050 |
| **Total (build + first year)** |  | **₹33,27,916** | **₹5,99,025** | **₹39,26,940** |
| Ongoing after year 1, per month | Running + retainer | ₹86,797 | ₹15,624 | ₹1,02,421 |

# 2. A. One-time build cost

| # | Item | Basis | Amount (excl. GST) | Amount (USD) |
|---|---|---|---|---|
| A1 | Builder's time: specify, review every AI change, test, release, client demos | 4 months × ₹1,25,000 (84 days × ₹5,682/day) | ₹5,00,000 | $5,556 |
| A2 | Claude API tokens for coding agents: agents execute the implementation work of all 1,382 traditional person-days (parallel, headless) | 1,382 × $6.78 × ₹90 | ₹8,43,916 | $9,377 |
| A3 | Contingency on time and tokens | 10% × (A1 + A2) | ₹1,34,392 | $1,493 |
| A4 | Independent security testing: penetration test before go-live + retest after fixes (CERT-In-empanelled vendor) | Estimate, at actuals (range ₹4–9 lakh) | ₹6,50,000 | $7,222 |
|  | **Total A** |  | **₹21,28,308** | **$23,648** |

**How the 4 months are used.** The builder spends 84 working days writing specifications and acceptance tests, reviewing every AI-generated change, running UAT with the client and releasing. Coding agents do the equivalent of about 1,382 person-days of implementation, drafting and testing in parallel. That is why tokens are the largest build item after time.

**Delivery plan:**

| Month | Focus | Exit |
|---|---|---|
| 1 | Foundation: environments, identity, tenancy, policy engine, model gateway, design system; Release 1 workflows started | Foundation gate |
| 2 | Release 1 workflows WF-01…WF-10, Website and Admin screens, AI agents and automations for Release 1 | Release 1 UAT start |
| 3 | Release 2 workflows WF-11…WF-14, penetration test and fixes, Release 1 + 2 go-live | Go-live (core) |
| 4 | Advanced A1 agents, automations and workflows; retest; A1 go-live; handover | A1 go-live and acceptance |

# 3. B. Subscriptions needed while building (months 1–4)

| # | Subscription | Purpose | $ per month | ₹ per month | Months | Total (₹) | Paid by |
|---|---|---|---|---|---|---|---|
| B1 | Claude Max 20x (Claude Code) | AI pair-programmer and interactive coding agents for the builder | $200 | ₹18,000 | 4 | ₹72,000 | Builder |
| B2 | CI runners and agent sandboxes (GitHub larger runners / AWS dev sandboxes) | Parallel coding agents build and test branches safely | $125 | ₹11,250 | 4 | ₹45,000 | Builder |
| B3 | GitHub Pro | Repositories, Actions CI, Dependabot, secret scanning | $4 | ₹360 | 4 | ₹1,440 | Builder |
| B4 | Figma Professional | UX design, prototypes, design system | $16 | ₹1,440 | 4 | ₹5,760 | Builder |
| B5 | BrowserStack Live | Cross-browser and screen-reader checks (WCAG 2.2 AA) | $29 | ₹2,610 | 4 | ₹10,440 | Builder |
| B6 | Langfuse (agent tracing), Sentry, open-source toolchain | Tracing, errors, Playwright, pytest, k6, OWASP ZAP, Trivy, Semgrep, axe-core | $0 | ₹0 | 4 | ₹0 | Free |
| B7 | Vercel Pro | Website and Admin frontends: preview and production deployments | $20 | ₹1,800 | 4 | ₹7,200 | Client |
| B8 | Supabase Pro (Mumbai) | PostgreSQL with RLS and pgvector, storage, backups (staging then production) | $25 | ₹2,250 | 4 | ₹9,000 | Client |
| B9 | AWS ap-south-1 small server + S3 | Django API, Celery workers, Valkey for staging | $15 | ₹1,350 | 4 | ₹5,400 | Client |
| B10 | Domain names (≈ 5) | Platform and startup sites | $5 | ₹450 | 4 | ₹1,800 | Client |
|  | **Total B** |  | **$439** | **₹39,510** | 4 | **₹1,58,040** |  |

The Claude API tokens used by the coding agents are in A2. Client accounts (Vercel, Supabase, AWS, domains) are opened in the client's name from day one, so the client owns its infrastructure and data.

# 4. C. Subscriptions and services after building

| # | Item | Basis | Per month (excl. GST) | Months | First-year total (excl. GST) |
|---|---|---|---|---|---|
| C1 | Running the application (all lines in §5.2, with 15% contingency, A1 features live) | Client accounts, at actuals | ₹31,797 | 12 | ₹3,81,568 |
| C2 | Maintenance and support retainer (includes maintainer's Claude Max 5x seat and GitHub) | Fixed monthly | ₹55,000 | 12 | ₹6,60,000 |
|  | **Total C (first 12 months)** |  | **₹86,797** | 12 | **₹10,41,568** |

# 5. Every subscription after building, line by line

## 5.1 Maintenance retainer (C2)

**₹55,000 + GST per month.** It covers:

- bug fixes, security patches and dependency upgrades;
- Claude model-version migrations with re-evaluation;
- monitoring and business-hours incident response;
- a quarterly DR drill;
- up to 6 days of small changes per month.

The maintainer's Claude Max 5x seat and GitHub are included.

## 5.2 Running the application (C1; client-owned; per month)

| Line | Subscription / service | Billing | Per month (INR) | Category |
|------|----------------------------------------------------|----------------|----------------|----------|
| B01a | Vercel Pro: Website and Admin frontends, CDN, firewall, preview builds (DEC-421) | Subscription + usage | ₹1,800–₹3,600 | Cloud |
| B01b | Supabase Pro + production compute, Mumbai: PostgreSQL with RLS and pgvector, storage, daily backups (DEC-421) | Subscription + compute | ₹3,600–₹5,400 | Cloud |
| B01c | AWS ap-south-1: Django API, Celery workers, Valkey, S3 files (EC2/ECS on EC2) (DEC-421) | Usage | ₹2,700–₹4,050 | Cloud |
| B20 | Cross-region backup and DR storage | Usage | ₹300–₹600 | Cloud |
| B01+ | Source-pack additions: restore-check sandbox, control/finance worker, drift job, training tenant | Usage | ₹200–₹1,700 | Cloud |
| B02 | Production AI inference: Claude Haiku-class and Sonnet-class (primary, DEC-418) via the gateway; hard cap | Pay-as-you-go, hard cap | ₹3,000 | AI |
| B03 | Public search API (≈ 500 fetches/month) | Free credits, then usage | ₹1,500 | Providers |
| B04 | Extraction compute / overage (self-hosted first) | Usage | ₹1,000 | Providers |
| B05 | Email delivery: Amazon SES (≈ 2,000 sends) | Usage | ₹500 | Providers |
| B06 | WhatsApp Business: Meta Cloud API (≈ 1,000 chargeable templates) | Per conversation/template | ₹2,000 | Providers |
| B07 | Monitoring, security and CI (error tracking, CI minutes, paging) | Subscription / usage | ₹500 | Tools |
|  | **Subtotal** |  | **₹17,100–₹23,850** |  |
| B11 | Contingency 15% |  | ₹2,565–₹3,578 |  |
| A1 | Advanced A1 feature running additions | Usage | ₹3,868–₹12,634 | Advanced |
|  | **Running per month (range; central used above)** |  | **₹23,533–₹40,062** (central ₹31,797) |  |

**Production AI usage.** The 50 AI agents in scope cost about ₹3,381 per month at pilot volume. They run on Claude, with Sonnet as the primary model, under hard caps of ₹3,000 core and ₹2,000 advanced per month. **When the business grows:** running is ≈ ₹59,000–79,000 per month at the growth gate and ≈ ₹1.39–1.79 lakh at scale, only after the scale gates pass. **Optional:** Apollo enrichment, e-signature, payment-gateway fees, advertising.

# 6. AI agents, automations and workflows in scope

| Type | In scope | Fully automated | Mostly automated | Partially automated | Assistive only |
|---|---|---|---|---|---|
| AI agents | 50 | 8 | 7 | 23 | 12 |
| Automations | 85 | 80 | 0 | 5 | 0 |
| Workflows | 35 | 0 | 0 | 35 | 0 |
| **Total** | 170 | 88 | 7 | 63 | 12 |

| Automation level | Meaning |
|---|---|
| Fully automated | Runs without a person inside policy guardrails; audited |
| Mostly automated | AI acts; a person reviews afterwards and can reverse |
| Partially automated | AI or rules prepare; a person approves before anything leaves the system. AI never signs, pays, submits bids or sets prices |
| Assistive only | AI suggests; a person acts |

## 6.1 AI agents (50)

| ID | Name | What it does | Automation | Autonomy | Model | AI cost/month | Release |
|-----|------------|----------------------------------------|--------|---------|---------|------|-------|
| AG-001 | Knowledge & Claim Ingestion Assistant | Turns approved uploaded decks, brochures and FAQs into chunk summaries and claim candidates with page citations, so R10/R05 approve claims in minutes instead of reading whole documents. | Partially automated | L1 | 1a Haiku 5.5 | ₹5 | Release 1 |
| AG-002 | AI Quality Judge & Eval Runner | Scores generative outputs against rubrics (groundedness, claim compliance, tone, refusal correctness) for the CI regression gate and for a 5% sample of production outputs. | Mostly automated | L2 (scores recorded automatically; a h | 1b Sonnet 5.5 via Batch API | ₹139 | Release 1 |
| AG-003 | Research Query Planner | Expands approved capability codes, geography and organization types into scoped search queries within the plan's source and cost bounds. | Fully automated within guardrails | L3 within guardrails (queries only rea | Tier 0 templates first | ₹1 | Release 1 |
| AG-004 | Evidence Extractor | Extracts organization-level business facts (projects, tenders, expansions, hiring for relevant functions, budgets, dates) with quotes and provenance from permitted pages and permitted social posts. | Fully automated within guardrails | L3 within guardrails (writes evidence  | 1a Haiku 5.5 via Batch API | ₹19 | Release 1 |
| AG-005 | Buying Signal Classifier | Classifies each evidence item into the approved signal taxonomy with confidence; below-threshold items go to review. | Mostly automated | L2 (classification stored; items below | 1a Haiku 5.5 via Batch API | ₹6 | Release 1 |
| AG-006 | Need Discovery Agent | Derives business needs from signals and evidence and labels each as explicit (stated in a source) or inferred. | Mostly automated | L1 for inferred needs (reviewer verifi | 1a Haiku 5.5 via Batch | ₹6 | Release 1 |
| AG-007 | Solution Match Explainer | Explains why each deterministically ranked offering (AU-016) fits a need and why others were excluded (readiness, geography, capability). | Assistive only | L0 (suggestion only; ranking is determ | 1a Haiku 5.5 via Batch | ₹2 | Release 1 |
| AG-008 | Decision-Maker Role Extractor | Extracts role hypotheses (function, seniority) and published professional channels from official organization pages for qualified accounts. | Partially automated | L1 (contact records created as unverif | 1a Haiku 5.5 via Batch | ₹1 | Release 1 |
| AG-009 | Qualification Brief Assistant | Prepares a one-screen cited brief per opportunity (need, fit, evidence freshness, score components, open questions) for the reviewer; at L2 (after the 90% gate) proposes accept/reject. | Partially automated | L1 until benchmark precision ≥ 90% on  | 1a Haiku 5.5 pre-generated i | ₹11 | Release 1 |
| AG-010 | Import Mapping Assistant | Maps unmatched CSV/JSON column headers and value formats to versioned import templates after deterministic header matching. | Partially automated | L1 (user confirms mapping before impor | Tier 0 header dictionary fir | ₹0 | Release 1 |
| AG-011 | Outreach & Follow-up Message Drafter | Drafts evidence-cited first-touch emails, WhatsApp template variants, follow-up steps, event invitations and renewal reminders using approved claims only. | Mostly automated | L1 for personalised drafts (human appr | 1b Sonnet 5.5 | ₹165 | Release 1 |
| AG-012 | Claims & Policy Guard | Second-line check of every customer-facing draft (messages, content, proposals, chat answers sampled) for unsupported claims, prohibited content, tone and brand. | Fully automated within guardrails | L3 within guardrails for block/fix dec | Tier 0 deterministic rules f | ₹20 | Release 1 |
| AG-013 | Inbound Intent Classifier & Router | Classifies every inbound email, WhatsApp and web reply (positive, question, objection, out-of-office, complaint, urgent/clinical, wrong person, other), extracts proposed times and a one-line summary, and routes it. | Fully automated within guardrails | L3 for routing and sequence stop (clas | Tier 0: STOP keywords, auto- | ₹9 | Release 1 |
| AG-014 | Reply Assistant | Drafts answers to inbound questions from approved FAQ and knowledge with citations; at L3, sends only approved FAQ answers verbatim with variables. | Fully automated within guardrails | L1 by default; L3 only when the answer | Tier 0 semantic cache of app | ₹27 | Release 1 |
| AG-015 | Admin Copilot | Side-panel assistant that answers staff questions over records the user can already see and approved knowledge, with citations; briefs on accounts and meetings; proposes saved-view filters and drafts (message, task, note… | Assistive only | L0 answers; L1 drafts (DEC-035) | 1a Haiku 5.5 for lookups | ₹222 | Release 2 |
| AG-016 | Autonomous Commercial Planner | Proposes commercial plans (objective, eligible segment, channel mix, sequence, budget, schedule) and workflow drafts from approved node types; narrates simulation results. | Partially automated | L1 for the plan (approval of the exact | 1b Sonnet 5.5 | ₹26 | Release 2 |
| AG-017 | Website Assistant | Public chat on each verified startup site that answers from approved public knowledge with citations, captures a consented lead and hands over clinical, legal, pricing-negotiation and complaint topics. | Fully automated within guardrails | L3 for answers grounded in approved pu | Tier 0 FAQ cache | ₹13 | Release 1 |
| AG-018 | Content & Campaign Studio Drafter | Drafts articles, social variants, landing-page copy, ad copy, SEO titles/meta and translation drafts (hi-IN, ta-IN, or-IN) from a brief using approved claims. | Partially automated | L1 (content approver ≠ author; claims  | 1b Sonnet 5.5 | ₹98 | Release 1 |
| AG-019 | Bid / RFP Analyzer | Parses RFPs, tenders and submitted project requirements into eligibility criteria, deadlines, mandatory documents, evaluation criteria and a compliance matrix, plus an L0 bid/no-bid brief. | Assistive only | L1 for checklist items; L0 for bid/no- | 1b Sonnet 5.5 | ₹141 | Release 2 |
| AG-020 | Proposal & Bid Response Drafter | Drafts proposals and bid response sections from approved templates, meeting notes entered by staff, approved claims and the deterministic price snapshot (prices inserted by AU-035, never by the model). | Partially automated | L1 (DEC-064: proposals/quotes ≤ L1) | 1b Sonnet 5.5 | ₹63 | Release 2 |
| AG-021 | Objection & Negotiation Assistant | Classifies objections into the approved taxonomy, drafts approved responses, and prepares exception summaries for A070 when a request exceeds concession limits. | Partially automated | L1 (price/terms ≤ L1, DEC-064) | 1b Sonnet 5.5 | ₹22 | Release 2 |
| AG-022 | Contract Clause Reviewer | Compares counterparty redlines or third-party paper against the approved template and clause library; flags non-standard, missing or risky clauses for Legal with references. | Assistive only | L0 (suggest only) | 1b Sonnet 5.5 | ₹18 | Release 2 |
| AG-023 | Order Document Extractor | Extracts RFQ/PO lines (SKU, description, unit, quantity, requested price, delivery date/region) from uploaded documents and emails into a draft order or RFQ for OrganicSpec and other order-desk startups. | Partially automated | L1 (draft order; coordinator confirms) | 1a Haiku 5.5 | ₹5 | Release 2 |
| AG-024 | Payment Evidence Extractor | Pre-fills payment verification fields (UTR/reference, amount, currency, date, payer name, bank) from uploaded bank/UPI evidence for the Finance Maker. | Assistive only | L0 (pre-fill; maker confirms every fie | 1a Haiku 5.5 | ₹1 | Release 2 |
| AG-025 | Onboarding Handoff Summarizer | Produces the commercial-to-delivery handoff summary (scope, commitments, contacts' roles, open risks, approved terms references) when a deal closes. | Partially automated | L1 | 1a Haiku 5.5 via Batch | ₹0 | Release 2 |
| AG-026 | Loss & Feedback Analyzer | Classifies free-text loss reasons and customer feedback into the loss taxonomy and produces a monthly theme report. | Mostly automated | L2 (labels stored; owner can correct) | 1a Haiku 5.5 via Batch | ₹0 | Release 2 |
| AG-027 | Market & Competitor Watch Summarizer | Summarizes permitted public competitor and market events into internal alerts with sources. | Fully automated within guardrails | L3 for internal alerts only (no extern | 1a Haiku 5.5 via Batch | ₹1 | Release 2 |
| AG-028 | Ops & Incident Triage Agent | Clusters failed runs, DLQ items, provider errors and alerts; summarizes probable cause and links the runbook (RB-) for on-call staff. | Assistive only | L0 (suggestions only); remediation by  | 1a Haiku 5.5 | ₹7 | Release 2 |
| AG-029 | Insight Narrative Agent | Writes weekly 'what changed and why' narratives on deterministic KPI snapshots for startup heads and a portfolio digest for the founder. | Fully automated within guardrails | L3 for internal digest delivery | 1a Haiku 5.5 via Batch | ₹1 | Release 2 |
| AG-030 | SaaS Onboarding Configuration Assistant | During W33, proposes business profile, industry taxonomy, offering structure, objective templates and workflow bindings from the applicant's description. | Partially automated | L1 (applicant edits; platform approval | 1b Sonnet 5.5 | ₹35 | Release 2 |
| AG-031 | Support Desk Assistant | Triages portal support tickets (W28, W34) by category and severity, drafts replies from the help centre, answers authenticated customers' questions about their own records, and drafts KB articles from resolved tickets. | Mostly automated | L1 for replies; L2 for category/severi | 1a Haiku 5.5 | ₹14 | Release 2 |
| AG-033 | Requirements & Story Assistant | Drafts user stories, Gherkin AC, ADR and DPIA skeletons from FR/BRL/DEC text, and runs change-impact analysis over the traceability matrix. | Partially automated | L1 (PR review by PO) | Claude Code developer seats | ₹505 | Release 1 |
| AG-034 | Coding Assistant | Claude Code for implementation, refactoring, IaC, UI microcopy and accessibility fixes, with repository rules (RLS scoping, outbox, no secrets). | Partially automated | L1 (all changes through PR review + CI | Claude Code developer seats | ₹505 | Release 1 |
| AG-035 | PR, Security & Release Review Agent | Reviews each pull request for tenancy/RLS scoping, outbox use, secret exposure, OWASP issues, missing tests; triages CI failures and SAST/dependency findings; drafts release notes and go/no-go summaries; drafts threat-mo… | Assistive only | L0 (comments only; cannot approve or m | 1b Sonnet 5.5 via CI API key | ₹505 | Release 1 |
| AG-036 | Test & Synthetic Data Generator | Generates test cases from Gherkin AC (EP/BVA/decision-table techniques), synthetic two-tenant fixtures (RECOMMENDATION-017), injection corpora and eval cases from reviewed feedback. | Partially automated | L1 (QA review) | Claude Code seats + 1a Haiku | ₹6 | Release 1 |
| AG-037 | Meeting Notes & Action Summarizer | Turns staff-written meeting notes (and, only after GAP-143 is resolved with consent, authorized transcripts) into a structured summary, decisions and action items that distinguish confirmed from unconfirmed commitments, … | Partially automated | L1. Organizer approves the summary; ac | 1a Haiku 5.5; 15% escalation | ₹7 | Release 2 |
| AG-038 | Retention Next-Best-Action Advisor | For accounts entering the renewal window (AU-039), reads delivery milestones, feedback, support history and contract dates and proposes one next best action (check-in, success review, upsell discussion within approved of… | Assistive only | L0 (suggest only). Owner accepts, edit | 1a Haiku 5.5 via Batch; 10%  | ₹5 | Release 2 |
| AG-039 | Agent Supervisor and Planner | Turns a staff objective ("pursue account X for offering Y", "prepare RFP response", "prepare launch brief") into a typed, budgeted, approvable plan over registered agents and automations, so multi-step work starts in min… | Partially automated | L1. A plan containing any W1 step (dra | 1b Sonnet 5.5 (effort medium | ₹120 | Advanced A1 |
| AG-040 | Account Research Agent | Builds one cited, versioned account brief per organization from owned records (CRM, evidence, interactions) and permitted public sources only (AU-007), so every account-centric agent and person works from the same facts;… | Assistive only | L0. Brief is informational; memory pro | 1a Haiku 5.5 via Batch; 15%  | ₹20 | Advanced A1 |
| AG-047 | RFP Response Co-pilot | For each requirement extracted by AG-019, retrieves matching approved, unexpired answers from the answer library (AU-063), drafts the response with per-answer citations and confidence, lists gaps with owners, and fills t… | Partially automated | L1. Bid owner approves each answer (au | 1b Sonnet 5.5; RFP prefix ca | ₹401 | Advanced A1 |
| AG-055 | Knowledge Curator and RAG Freshness Agent | Reviews AU-069 findings (stale chunks, conflicting facts across documents, near-duplicates, coverage gaps from clustered abstentions and retrieval misses) and drafts concrete edits or new FAQ entries for knowledge owners… | Partially automated | L1. Owner approves; approved edits re- | 1a Haiku 5.5 via Batch; 10%  | ₹14 | Advanced A1 |
| AG-056 | Agent Red-Team and Drift Analyst | Generates mutations of the seed injection, jailbreak, cross-audience and data-exfiltration corpora (paraphrase, language switch to hi/ta/or, encoding, indirect via document/email/WhatsApp formats) for scheduled runs (AU-… | Mostly automated | L0 for findings; L2 for writing candid | 1b Sonnet 5.5 via Batch (lin | ₹84 | Advanced A1 |
| AG-060 | Data-Quality and Dedupe Steward | Reviews candidate duplicate pairs from AU-074 blocking (similar names, domains, addresses, aliases) and inconsistent fields, and proposes merge / keep-separate with field-level resolutions and evidence, so duplicates fal… | Partially automated | L1. R04 approves each merge in A018 me | 1a Haiku 5.5 via Batch; 10%  | ₹9 | Advanced A1 |
| AG-062 | Signal Fusion "Why-Now" Brief Writer | Writes a three-sentence "why now" brief for each surging account and for each newly routed hot lead, citing the deterministic intent components (AU-084) and evidence, so sellers act on timing within the SLA (KPI-ADV-X2-0… | Assistive only | L0. Advisory text shown on A132 and on | 1a; 10% escalation to 1b whe | ₹35 | Advanced A1 |
| AG-064 | Pipeline Inspection and Forecast Risk Analyst | For each open deal, turns deterministic facts and AU-088 flags into a short risk note with cited facts and three inspection questions; for the forecast roll-up, explains week-over-week changes. Managers inspect more deal… | Assistive only | L0. Advisory only; cannot change categ | 1a; 20% escalation to 1b for | ₹48 | Advanced A1 |
| AG-066 | CPQ Bundle Advisor and Guardrail Explainer | Given the stated need and the active price book, suggests up to three approved bundles or line sets with reasons, and explains guardrail results (AU-089) in plain language with the next allowed action, so time-to-quote f… | Assistive only | L0. Seller chooses; AU-089 and AU-035  | 1a; 10% escalation to 1b | ₹15 | Advanced A1 |
| AG-074 | AI Observability Drift Analyst | Turns trace aggregates, eval scores and feedback into a weekly per-agent health note with regressions linked to prompt or model revisions, so AI quality regressions are found ≤ 24 h after the alert and fixed before users… | Partially automated | L1. Report reviewed by AI lead; action | 1a Haiku 5.5; 10% escalation | ₹4 | Advanced A1 |
| AG-077 | Supply-Chain Risk Analyst | Shortens triage of new CVEs in deployed components by drafting exploitability notes and VEX candidates with evidence, so Critical findings are triaged ≤ 24 h and remediated within §4.16.3 SLAs | Partially automated | L1. A reviewer ≠ author accepts VEX (B | 1a Haiku 5.5; 15% escalation | ₹10 | Advanced A1 |
| AG-078 | Secrets Rotation Coordinator | For providers without a rotation API, drafts the exact console steps, overlap window and verification call, so guided rotations finish on time with no downtime (NFR-ADV-X3-14) | Partially automated | L1. Human performs provider console st | 1a Haiku 5.5; no escalation | ₹1 | Advanced A1 |
| AG-080 | FinOps Optimization Agent | Turns measured utilization and cost ledgers into a ranked list of savings with formulas and SLO risk, so ≥ 10% of infrastructure spend is identified as addressable per quarter without SLO violation (doc 36 OPT-03-04) and… | Partially automated | L1. Recommendations read-only until ap | 1a Haiku 5.5; 20% escalation | ₹9 | Advanced A1 |

## 6.2 Automations (85)

| ID | Name | What it does | Automation | Autonomy | Model | AI cost/month | Release |
|-----|------------|----------------------------------------|--------|---------|---------|------|-------|
| AU-001 | Model gateway router, Tier 0 cache & template responder | Routing decision table (§7.3.4); exact-match cache key = hash(agent, prompt version, model, normalized input, scope); semantic cache (pgvector cosine ≥ 0.92, same tenant/startup namespace, Public/Internal only); approved… | Fully automated | L3 (deterministic, within policy) | — | In hosting | Release 1 |
| AU-002 | Budget reservation, alerts & hard stop | Reserve estimated ₹ (max_tokens × output price + input estimate) against agent, startup, tenant and global budgets; reconcile actual usage; 80% alert, 100% hard stop; founder top-up audited | Fully automated | L3 (deterministic, within policy) | — | In hosting | Release 1 |
| AU-003 | Output schema validation & repair controller | Validate JSON against versioned schema; up to 2 repair retries with the validation error; then route per §7.3.4 (Tier 2 only if data class allows) else Tier 3 | Fully automated | L3 (deterministic, within policy) | — | In hosting | Release 1 |
| AU-004 | Data classification & PII redaction | Field-level classification from the data dictionary + Presidio analyzers (email, phone, Aadhaar/PAN patterns, names, health terms) with Indian recognizers; mask/pseudonymize; block Tier 2 if Restricted/Confidential remai… | Fully automated | L3 (deterministic, within policy) | — | In hosting | Release 1 |
| AU-005 | Untrusted-content sanitizer & injection pre-filter | HTML-to-text cleaning, hidden-text removal, length caps, delimiter wrapping with provenance, injection heuristics (instruction verbs aimed at the model, tool-call syntax, canary probes) flagging injection_suspected | Fully automated | L3 (deterministic, within policy) | — | In hosting | Release 1 |
| AU-006 | Eval regression CI gate | Run promptfoo/DeepEval suites per agent (deterministic graders + AG-002 judge); compare to thresholds in §7.6.9; block merge on failure | Fully automated | L3 (deterministic, within policy) | — | In hosting | Release 1 |
| AU-007 | Source permission & expiry enforcer | Check purpose, licence, robots/terms flag, quotas and expiry per source; stop collection on expiry (M07 trigger) | Fully automated | L3 (deterministic, within policy) | — | In hosting | Release 1 |
| AU-008 | STOP / opt-out handler & queued-send cancellation | Multilingual STOP lexicon, List-Unsubscribe, WhatsApp opt-out; suppression write; cancel queued sends in scope atomically | Fully automated | L3 (deterministic, within policy) | — | In hosting | Release 1 |
| AU-009 | Policy Decision Point dispatch guard | Recheck scope, role, consent, jurisdiction, quiet hours, caps, entitlement, budget reservation and approved hash at dispatch | Fully automated | L3 (deterministic, within policy) | — | In hosting | Release 1 |
| AU-010 | Provider health checks & circuit breakers | Synthetic health probe; error-rate/latency windows; open circuit after 5 consecutive failures or 50% errors in 60 s; half-open probe after 30 s | Fully automated | L3 (deterministic, within policy) | — | In hosting | Release 1 |
| AU-011 | Privacy request locator & retention purge | Identifier search across tables incl. AI run logs and caches; purge AI payloads after 90 days; keep digests; legal hold respected | Fully automated | L3 (deterministic, within policy) | — | In hosting | Release 1 |
| AU-012 | FinOps cost attribution & anomaly alerts | Cost per task/agent/startup/tenant/provider; z-score and >150% of 7-day baseline alerts; KPI anomaly thresholds | Fully automated | L3 (deterministic, within policy) | — | In hosting | Release 1 |
| AU-013 | Release pipeline gates | Secret scan, SAST, dependency update bot (Renovate-style), licence check, ID/trace lint, restore drill schedule, smoke test | Fully automated | L3 (deterministic, within policy) | — | In hosting | Release 1 |
| AU-014 | URL normalization, blocked-host & duplicate-content filter | Canonicalize URLs, strip tracking, reject blocked hosts, content-hash dedupe (saves AG-004 calls) | Fully automated | L3 (deterministic, within policy) | — | In hosting | Release 1 |
| AU-015 | Organization canonical upsert & safe merge | Match by domain + location + alias; conflicting attributes → merge task | Fully automated | L3 (deterministic, within policy) | — | In hosting | Release 1 |
| AU-016 | Readiness-gated solution match ranking | pgvector similarity between need and approved capability chunks + rule filters (readiness Approved and Available, geography, capability profile) | Fully automated | L3 (deterministic, within policy) | — | In hosting | Release 1 |
| AU-017 | Opportunity scoring | score = round(100 × Σ wᵢcᵢ / Σ w_known); Unknown if known weight < 0.60; bands | Fully automated | L3 (deterministic, within policy) | — | In hosting | Release 1 |
| AU-018 | Contact verification & freshness expiry | Provenance check (published on official page), channel syntax/MX check, freshness expiry and recheck | Fully automated | L3 (deterministic, within policy) | — | In hosting | Release 1 |
| AU-019 | Research review assignment & alerts | Round-robin/owner rules; SLA timers | Fully automated | L3 (deterministic, within policy) | — | In hosting | Release 1 |
| AU-020 | Lead dedupe, consent capture & form routing | Idempotency key; dedupe; consent with policy revision; route by typed fields; age band < 18 → guardian/institution path with no minor data beyond grade band | Fully automated | L3 (deterministic, within policy) | — | In hosting | Release 1 |
| AU-021 | Customer 360 projection | Event-sourced projection | Fully automated | L3 (deterministic, within policy) | — | In hosting | Release 1 |
| AU-022 | Sequence scheduler with stop-on-reply | Eligibility recheck, quiet hours, caps; stop on any substantive reply (AG-013) or STOP (AU-008) | Fully automated | L3 (deterministic, within policy) | — | In hosting | Release 1 |
| AU-023 | Meeting slot offer & booking conflict check | Free/busy query, buffers, time-zone conversion, hold-and-confirm | Fully automated | L3 (deterministic, within policy) | — | In hosting | Release 1 |
| AU-024 | Bounce/complaint suppression | Hard bounce/complaint → suppression; soft bounce counters | Fully automated | L3 (deterministic, within policy) | — | In hosting | Release 1 |
| AU-025 | Emergency stop & runaway guard | Kill switch at platform/tenant/startup/workflow/agent/tier/channel scope; caps on steps, retries, concurrency, actions per relationship, LLM calls and tokens per run | Fully automated | L3 (deterministic, within policy) | — | In hosting | Release 1 |
| AU-026 | Uncertain-outcome reconciliation | Query provider by reference; mark reconciled_confirmed/failed; block retry until reconciled | Fully automated | L3 (deterministic, within policy) | — | In hosting | Release 1 |
| AU-027 | Notification digest & approval SLA escalation | Severity routing, digests, escalation ladders | Fully automated | L3 (deterministic, within policy) | — | In hosting | Release 1 |
| AU-028 | Missed-schedule recovery | Recover once; further misses alert | Fully automated | L3 (deterministic, within policy) | — | In hosting | Release 1 |
| AU-029 | Publication pipeline & expiry monitor | Approved-hash check, atomic pointer swap, tenant-keyed cache invalidation; claim/knowledge expiry notifications | Fully automated | L3 (deterministic, within policy) | — | In hosting | Release 1 |
| AU-030 | Automation conflict resolution by priority rules | Hold both; priority compliance > transactional > sales > marketing; merge or escalate | Fully automated | L3 (deterministic, within policy) | — | In hosting | Release 1 |
| AU-031 | Compliance auto-pause on complaint threshold | Threshold per channel/campaign → pause + incident | Fully automated | L3 (deterministic, within policy) | — | In hosting | Release 1 |
| AU-032 | Ad spend cap & anomaly pause | Cap check and >150% anomaly → pause via provider API | Fully automated | L3 (deterministic, within policy) | — | In hosting | Release 1 |
| AU-033 | SEO technical audit | Crawl checks (status, canonical, sitemap, metadata length), Search Console metrics from authorized source | Fully automated | L3 (deterministic, within policy) | — | In hosting | Release 1 |
| AU-034 | Bid deadline & mandatory-checklist tracker | Deadline countdown (UTC, FR-DM-02), checklist completeness gate before human submission | Fully automated | L3 (deterministic, within policy) | — | In hosting | Release 2 |
| AU-035 | Quote calculator, invoice generation & approval routing | Decimal lines, ROUND_HALF_UP, tax profile; threshold routing to approvers | Fully automated | L3 (deterministic, within policy) | — | In hosting | Release 2 |
| AU-036 | Document assembly, hashing & diff | Assemble from approved templates and onboarding checklists; SHA-256 hash; deterministic diff between revisions for approvers | Fully automated | L3 (deterministic, within policy) | — | In hosting | Release 2 |
| AU-037 | Payment matching proposal & maker-checker routing | Match on amount, reference, date window, payer; propose to maker; checker ≠ maker | Fully automated | L3 (deterministic, within policy) | — | In hosting | Release 2 |
| AU-038 | Fulfilment ledger & over-delivery guard | Idempotent event keys; over-delivery rejection; reservation/release | Fully automated | L3 (deterministic, within policy) | — | In hosting | Release 2 |
| AU-039 | Renewal calendar & rule-based account health score | Rules on usage, tickets, payments, engagement (no medical data) | Fully automated | L3 (deterministic, within policy) | — | In hosting | Release 2 |
| AU-040 | Revenue attribution & reconciliation | Last non-direct touch default + alternative models with caveat | Fully automated | L3 (deterministic, within policy) | — | In hosting | Release 2 |
| AU-041 | Stage-weighted forecast & backtest | Stage probabilities from history; MAPE backtest (KPI-29); labelled estimate | Fully automated | L3 (deterministic, within policy) | — | In hosting | Release 2 |
| AU-042 | Usage metering & entitlement enforcement | Meter AI tasks per tenant (definition §7.5.4), messages, fetches, storage; 80/100% alerts; deny beyond entitlement | Fully automated | L3 (deterministic, within policy) | — | In hosting | Release 2 |
| AU-044 | Integration procurement gate & entitlement expiry monitor | Evaluates PG-01…PG-10 evidence; blocks Active without all; daily expiry scan (30/7/1-day notices); 60-day unused detection; monthly re-evaluation task | Fully automated | L3 rules | — | In hosting | Release 1 |
| AU-045 | Matched-sample provider benchmark harness | Validates dataset (non-empty, unique opaque sample and expected-result IDs, no negative/nonfinite costs or latencies, same currency); runs baseline and candidate on identical sources; computes micro P/R, nearest-rank p95… | Fully automated | L3 rules (verdict reviewed by QA) | — | In hosting | Release 1 |
| AU-046 | Knowledge revocation & derivative purge | Sets revoked_at; deletes embeddings; purges exact/semantic caches by knowledge revision; invalidates Copilot summaries; legal hold respected | Fully automated | L3 rules | — | In hosting | Release 1 |
| AU-047 | Dependency & model-weight licence gate | SBOM → licence register match; fail on unknown, AGPL-linked, weights without commercial use, stale review | Fully automated | L3 rules | — | In hosting | Release 1 |
| AU-048 | Provider invoice ↔ usage reconciliation | Matches invoice lines to metered usage by provider, account, period, unit; tolerance 2% or ₹100; dedupes usage events by provider event ID | Fully automated | L3 rules | — | In hosting | Release 2 |
| AU-049 | Tenant contribution-margin calculator | Margin = recognized service revenue − (direct provider cost + AI cost + allocated infra + allocated support), per tenant and cohort; allocation basis versioned | Fully automated | L3 rules | — | In hosting | Release 2 |
| AU-050 | Adapter retirement & credential revocation | Disable new calls; drain and reconcile pending events and invoices; export/delete provider-held data per policy; revoke credentials and webhooks; test replacement; mark Retired | Fully automated | L3 rules (owner signs off) | — | In hosting | Release 2 |
| AU-051 | Event registration capacity, dedupe & reminders | Capacity check with row lock; dedupe by normalized email + event; waitlist; consented reminders through outbox; attendance import | Fully automated | L3 rules | — | In hosting | Release 1 |
| AU-052 | Tender amendment detector & evidence refresh | Compares portal document hashes and deadline fields; on change creates amendment record, re-runs AG-019 checklist diff, updates AU-034 deadlines, notifies bid owner | Fully automated | L3 rules | — | In hosting | Release 2 |
| AU-053 | Supervisor plan validator and step guard | Rules PV-01…PV-10 (§9.7.4.2): registry enabled and pinned, DAG acyclic, ≤ 12 agent steps, Σ step cost ≤ reservation and ≤ ₹25 default, monotonic data class, guard + checkpoint after customer-facing drafts, minors/clinica… | Fully automated | L3 (deterministic, within policy) | — | In hosting | Advanced A1 |
| AU-054 | Agent version canary controller and auto-rollback | Hash (tenant_id, object_id) into buckets; route 5% → 25% → 100% with minimum dwell 48 h / 72 h; compare SLOs (AU-071) of canary vs control; rollback if any SLO burn rate > 2× over 1 h, any mandatory check fails once, or … | Fully automated | L3 (deterministic, within policy) | — | In hosting | Advanced A1 |
| AU-057 | Model and agent drift monitor | PSI per ML feature and score distribution (alert > 0.2); KS test on agent confidence distributions; 7-day trends in abstention, schema-repair, escalation share, accept/edit/reject; fairness slices per §7.6.6 | Fully automated | L3 (deterministic, within policy) | — | In hosting | Advanced A1 |
| AU-061 | Memory consent, retention and purge controller | Enforce ai_memory_policy (enabled, fact types, TTL); expire items past expires_at; purge on privacy request via AU-011 locator incl. memory_refs[] in envelopes; purge on tenant offboarding (WF-14); write purge certificat… | Fully automated | L3 (deterministic, within policy) | — | In hosting | Advanced A1 |
| AU-062 | Memory write gate | Rules §9.7.4.4: allowlisted fact types, evidence required, special-category lexicon + Presidio + regex block, ≤ 280 chars, natural persons as contact_id + role only, minors/clinical block, dedupe by value hash, contradic… | Fully automated | L3 (deterministic, within policy) | — | In hosting | Advanced A1 |
| AU-063 | RFP answer library freshness and expiry | Each answer has owner, evidence, claim IDs, review_by (default 180 days); expire on claim expiry or review_by; notify owner at 30/7/1 days; block retrieval of expired answers; usage counter per bid | Fully automated | L3 (deterministic, within policy) | — | In hosting | Advanced A1 |
| AU-067 | Compliance pre-check for plans and campaigns | Checks: purpose and privacy-notice revision cover the processing; consent basis per recipient class and channel; jurisdiction rule pack (DEC-029) for target countries; minors and clinical exclusions; claims cited are app… | Fully automated | L3 (deterministic, within policy) | — | In hosting | Advanced A1 |
| AU-068 | Gateway cost optimizer | From the cost ledger and eval results: cache-miss hot spots (same prefix, low hit rate), prompts > p95 size for their agent, sync calls eligible for Batch, Sonnet-routed tasks where the Haiku eval meets thresholds, Tier … | Fully automated | L3 (deterministic, within policy) | — | In hosting | Advanced A1 |
| AU-069 | RAG freshness and coverage monitor | Stale: chunk age > source freshness SLA or referencing superseded price/offering versions; conflict: same entity attribute with different values across approved chunks; duplicate: cosine ≥ 0.97 within namespace; gap: abs… | Fully automated | L3 (deterministic, within policy) | — | In hosting | Advanced A1 |
| AU-070 | Golden-set and red-team scheduler | Schedules AU-006 suites, AG-056 mutation runs and Tier 2 model resistance runs in the eval sandbox; compares with baseline (dataset hash pinned) | Fully automated | L3 (deterministic, within policy) | — | In hosting | Advanced A1 |
| AU-071 | Agent observability and AI SLO tracker | Per agent version SLOs (schema-valid ≥ 99.5%, groundedness ≥ 95% on sample, p95 latency, cost per task); 28-day error budget; multi-window burn-rate alerts (1 h and 6 h) | Fully automated | L3 (deterministic, within policy) | — | In hosting | Advanced A1 |
| AU-074 | Data-quality rules and dedupe blocking | Normalize names (legal suffixes, case, punctuation), domains, phone/address formats; blocking keys (domain root, normalized name trigram, city); Jaro-Winkler and token-set similarity; candidate pair if score ≥ 0.85 and s… | Fully automated | L3 (deterministic, within policy) | — | In hosting | Advanced A1 |
| AU-078 | Human feedback capture and label queue | Store diff and reason; sample stratified items into a labelling queue (A128) with redaction; reviewer labels → candidate eval items; promotion to an eval set only with R10 + AI lead approval and new dataset hash | Fully automated | L3 (deterministic, within policy) | — | In hosting | Advanced A1 |
| AU-079 | AI system inventory and model-card sync | Maintain one inventory row per agent/automation-with-model and version: intended purpose, risk class (§9.7.12.1), data classes, autonomy cap, model tier, eval run IDs, fairness results, known limitations, oversight desig… | Fully automated | L3 (deterministic, within policy) | — | In hosting | Advanced A1 |
| AU-080 | Lead-to-account matcher | Normalize email domain (public-suffix list), strip free-mail; organization name similarity (token-set ratio, RapidFuzz-class library), registered ID exact match, address match (libpostal-class normalizer), existing conta… | Fully automated | L3 (deterministic, within policy) | — | In hosting | Advanced A1 |
| AU-081 | Owner routing and speed-to-lead SLA clock | Routing order existing owner → account owner → territory → capacity-weighted round robin; skip ineligible; SLA due = start + class SLA on owner's business calendar; 75/100/200% escalation ladder | Fully automated | L3 (deterministic, within policy) | — | In hosting | Advanced A1 |
| AU-084 | Signal fusion and intent decay scorer | Intent = min(100, Σ type_weight × topic_fit × 0.5^(age/half-life)); components stored; expired evidence removed; surge = +15 points in 7 days | Fully automated | L3 (deterministic, within policy) | — | In hosting | Advanced A1 |
| AU-085 | Buying-committee coverage calculator | Coverage = filled and engaged required slots ÷ required slots; single-threaded = 1 engaged member on a deal above threshold | Fully automated | L3 (deterministic, within policy) | — | In hosting | Advanced A1 |
| AU-086 | Multichannel cadence orchestrator | For each due step: PDP dry-run; automated channels → outbox with dispatch recheck (AU-009); human steps → task (A137); global stop on any stop event for the person across all cadences; committee pause; cumulative cap acr… | Fully automated | L3 for scheduling (deterministic); dis | — | In hosting | Advanced A1 |
| AU-087 | Forecast roll-up and weekly snapshot | Sum by category and owner chain; manager adjustments with reason; immutable snapshot (payload hash); attainment = Closed-Verified ÷ prior Commit; slippage = deals leaving Commit | Fully automated | L3 (deterministic, within policy) | — | In hosting | Advanced A1 |
| AU-088 | Pipeline hygiene and inspection flags | Rules: no next step; close date past; stage age > p75 of won deals; single-threaded; no MAP above threshold; amount change > 20% in a week; owner lacks grant | Fully automated | L3 (deterministic, within policy) | — | In hosting | Advanced A1 |
| AU-089 | CPQ guardrail evaluator | Validate lines against active price-book revision; required/excluded options; quantity bounds and breaks; validity ≤ max; margin ≥ floor (Decimal); discount band → approver per DEC-038 | Fully automated | L3 (deterministic, within policy) | — | In hosting | Advanced A1 |
| AU-093 | Customer health score v2 | Score = round(100 × Σ wᵢcᵢ ÷ Σ w_known); Unknown if known weight < 0.60; bands by template; trend over 30/90 days; quarterly back-test vs renewal outcome | Fully automated | L3 (deterministic, within policy) | — | In hosting | Advanced A1 |
| AU-102 | Semantic metric compiler & parity check | Compile YAML → SQL templates; run parity fixture vs legacy RP outputs; mark parity status | Fully automated | L2 (internal) | — | In hosting | Advanced A1 |
| AU-105 | AI trace redaction & telemetry shipper | Apply AU-004 DLP; replace Restricted by type tokens; hash Confidential bodies unless sampling allowed; emit OTel GenAI spans; aggregate daily | Fully automated | L2 (internal) | — | In hosting | Advanced A1 |
| AU-107 | Chaos scheduler & abort guard | Check environment = staging; start FIS template; watch stop conditions; abort ≤ 60 s; record result | Fully automated | L2 (staging only) | — | In hosting | Advanced A1 |
| AU-108 | DR drill orchestrator | Restore snapshot/PITR in backup sandbox with dispatch off; run integrity suite; time RPO/RTO; file evidence; destroy | Fully automated | L2 (isolated account) | — | In hosting | Advanced A1 |
| AU-109 | Status page publisher | Compute component state from external probes; publish approved notices; email subscribers | Partially automated | L2 for component state; L1 for inciden | — | In hosting | Advanced A1 |
| AU-110 | JIT privileged access broker | Grant bundle permissions with TTL; revoke on expiry/withdrawal; propagate session revocation ≤ 60 s | Partially automated | L1 (approval by another person) | — | In hosting | Advanced A1 |
| AU-111 | Device posture & session risk evaluator | Check device cert validity and binding, browser in matrix, passkey amr; compute posture level | Fully automated | L2 (protective: read-only downgrade) | — | In hosting | Advanced A1 |
| AU-112 | Rights request orchestrator | Start clocks; call AU-011 locators per store; build step proposals; apply approved steps; tombstones to lake; generate evidence pack | Partially automated | L1 per execution step | — | In hosting | Advanced A1 |
| AU-114 | Secrets rotation executor | Managed: create new version, test, promote, revoke old after overlap. Guided: open task with AG-078 steps, one-time value form, verify, revoke | Partially automated | L1 for guided and emergency; L2 for ma | — | In hosting | Advanced A1 |
| AU-115 | Supply-chain verification gate | Generate SBOM + provenance; verify cosign signature and builder identity at deploy; upload SBOM; nightly CVE match on deployed set; scan marketplace partner artefacts | Fully automated | L2 (block-only, protective) | — | In hosting | Advanced A1 |
| AU-118 | Rightsizing & idle-resource detector | p95 utilization vs allocation; idle EIPs/volumes; S3 lifecycle gaps; log outliers; AI cache misses | Partially automated | L1 (read-only recommendations) | — | In hosting | Advanced A1 |

## 6.3 Workflows (35)

| ID | Name | What it does | Automation | Autonomy | Model | AI cost/month | Release |
|-----|------------|----------------------------------------|--------|---------|---------|------|-------|
| WF-01 | Startup catalogue (product truth) | approve offering, price, claims, segment, customer roles, pipeline and workflow; no unapproved offerings or unscoped access (BRD §5). | Partially automated | Human gates | — | In hosting | Release 1 |
| WF-02 | Market discovery | plan source query → evidence → signals/need → solution match → qualify, with allowed sources, review, freshness and confidence (BRD §5). | Partially automated | Human gates | — | In hosting | Release 1 |
| WF-03 | Professional contacts | find organization decision-makers, verify channel/source, deduplicate, eligibility; no private scraping; contact score ≠ permission (BRD §5). | Partially automated | Human gates | — | In hosting | Release 1 |
| WF-04 | Inbound acquisition | landing page, chat, email, WhatsApp, social, event or referral → lead and attribution, with scope, consent and dedupe; no medical records or minor targeting (BRD §5). | Partially automated | Human gates | — | In hosting | Release 1 |
| WF-05 | Content and campaign | generate approved content, SEO, social, ad/landing plan, audience and budget, with claim and channel approval, cost caps and actual publication (BRD §5). | Partially automated | Human gates | — | In hosting | Release 1 |
| WF-06 | Outreach and replies | preview eligible contacts → approved messages → callback → classify intent; opt-out/complaint stop; a response halts the generic sequence (BRD §5). | Partially automated | Human gates | — | In hosting | Release 1 |
| WF-07 | Follow-up and meetings | schedule tasks by intent, preference and local time; verify calendar; caps, rejection and suppression stop (BRD §5). | Partially automated | Human gates | — | In hosting | Release 1 |
| WF-08 | Project bid (AppNAI route, BRD §4 and BR-S001) | AppNAI qualify RFP/requirements, eligibility checklist, deadline guard, bid/no-bid, proposal and quote, human submission with recorded evidence, award proof, contract, delivery, verified payment (BRD §4–§5; DEC-053) | Partially automated | Human gates | — | In hosting | Release 1 |
| WF-09 | Proposal, quote and negotiation | Proposal and quote from approved templates and price versions; Decimal totals and tax; discount and legal approval thresholds; recipient review in portal; objections answered from approved facts or escalated (BRD §5; DEC… | Partially automated | Human gates | — | In hosting | Release 1 |
| WF-10 | Order and fulfilment (OrganicSpec route, BR-S004) | Buy/sell/service/training orders with SKU, unit and quantity lines; stock reservation; idempotent fulfilment events; over-delivery rejection; acceptance; separate receivable and payable ledgers (BRD §5; FR-DM-03) | Partially automated | Human gates | — | In hosting | Release 1 |
| WF-11 | Commercial closure (all routes) | Close only on route-specific verified evidence (signed contract or verified payment); finance maker-checker; partial payments; no duplicate revenue or false Won state (BRD §5; DEC-054) | Partially automated | Human gates | — | In hosting | Release 2 |
| WF-12 | Retention and renewal | Offering-specific onboarding and handoff (no patient data), milestones, feedback, renewal calendar and eligible reminders, lost-deal learning (BRD §5) | Partially automated | Human gates | — | In hosting | Release 2 |
| WF-13 | Autonomous plan | Objective-driven plan from approved templates; simulation of recipients, cost, deadlines and conflicts; approval of the exact plan hash; execution with dispatch-time recheck; live monitoring, budget hard stops and emerge… | Partially automated | Human gates | — | In hosting | Release 2 |
| WF-14 | Suspend and offboard (tenant or startup) | Suspend or offboard a tenant/startup: stop schedules and queued actions, revoke senders and access, reconcile uncertain outcomes, export allowed records, apply retention (BRD §5) | Partially automated | Human gates | — | In hosting | Release 2 |
| WF-15 | Supervised multi-agent account pursuit | Pursue a qualified account through research, brief, next action and first-touch draft as one supervised plan, with every approval of the baseline preserved (ADR-110; BR-AUTO; DEC-064). | Partially automated | Human gates | — | In hosting | Advanced A1 |
| WF-16 | Predictive model lifecycle | Train, validate, shadow, approve, serve, monitor and retire advisory ML models (AU-056, AU-059, AU-066) without ever changing DEC-011 scoring or any eligibility decision (ADR-113; DEC-383). | Partially automated | Human gates | — | In hosting | Advanced A1 |
| WF-17 | Deal-risk and churn early warning | Nightly detect at-risk open deals (AU-058, AG-044) and, from A3, at-risk customers (AU-059 feeding AG-038), and turn each into an owner task with reasons, so intervention happens before the forecast or renewal date (BR-M… | Partially automated | Human gates | — | In hosting | Advanced A1 |
| WF-18 | RFP response co-pilot (AppNAI) | Answer RFP requirements from the approved answer library with citations and gaps, inside WF-08, keeping bid/no-bid, pricing and submission human (BR-S001, DEC-053, DEC-064). | Partially automated | Human gates | — | In hosting | Advanced A1 |
| WF-19 | Localized personalization at scale | From a campaign brief and deterministic segments, generate guarded variants, localize them with TM and glossary, approve them as templates and test them, so personalized multilingual outreach scales under DEC-064 (BR-M25… | Partially automated | Human gates | — | In hosting | Advanced A1 |
| WF-20 | Experiment lifecycle | Pre-register, approve, run, monitor and read out experiments on messages, sequences, content, agent versions and NBA policies, so lift claims rest on valid statistics (ADR-118; BR-S090). | Partially automated | Human gates | — | In hosting | Advanced A1 |
| WF-21 | Agent release, canary and red-team | Release any new agent, prompt, model or ML version through offline evals, red-team, shadow and staged canary with automatic rollback, and keep it under continuous adversarial and drift monitoring (ADR-111, ADR-117; BR-M5… | Partially automated | Human gates | — | In hosting | Advanced A1 |
| WF-22 | Knowledge freshness and memory governance | Keep RAG knowledge current, consistent and complete (AU-069, AG-055) and keep long-term memory lawful (AU-061, AU-062), with all edits through the M03 approval pipeline and all memory under purpose, TTL and erasure (BR-M… | Partially automated | Human gates | — | In hosting | Advanced A1 |
| WF-23 | WhatsApp concierge with human handoff | Answer customer-initiated WhatsApp conversations within the service window from approved knowledge, offer meeting slots, and hand off to a human for sensitive topics or on request (BR-M31, BR-M41; DEC-030, DEC-064). | Partially automated | Human gates | — | In hosting | Advanced A1 |
| WF-25 | Account-based engagement | Select and tier target accounts, map the buying committee, approve an account plan and run coordinated plays across sales, marketing, success and partners, without any automatic outreach beyond approved, eligible steps (… | Partially automated | Human gates | — | In hosting | Advanced A1 |
| WF-26 | Lead-to-account match, route and speed-to-lead SLA | Attach every inbound lead to the right account, assign the right owner deterministically and measure response against the SLA, with escalation (F05, F06, F07). | Partially automated | Human gates | — | In hosting | Advanced A1 |
| WF-27 | Multichannel cadence under consent | Run approved cadences across email, WhatsApp, human LinkedIn tasks, human call tasks and meetings with one consent check, one frequency budget and global stop rules (F09, F26). | Partially automated | Human gates | — | In hosting | Advanced A1 |
| WF-28 | Deal room, mutual action plan and guarded quote | Give the buyer committee one portal space with approved materials and a confirmed mutual action plan, and build quotes inside approved price books with live guardrails (F10, F11, F12, F29). | Partially automated | Human gates | — | In hosting | Advanced A1 |
| WF-29 | Pipeline inspection and forecast call | Inspect open deals every week with deterministic flags and advisory risk notes, set commit categories with evidence and lock an immutable forecast snapshot labelled as estimate (F20, F21, F08). | Partially automated | Human gates | — | In hosting | Advanced A1 |
| WF-31 | Customer health, QBR, renewal and expansion | Score customer health daily, explain drivers, prepare approved QBR packs and run renewal and expansion cases priced only through CPQ (F15, F16, F17, F30–F32). | Partially automated | Human gates | — | In hosting | Advanced A1 |
| WF-32 | Voice of customer and win/loss learning loop | Collect NPS/CSAT from eligible adult business contacts, run win/loss reviews with consent, synthesize themes and close the loop with owned actions (F18, F19). | Partially automated | Human gates | — | In hosting | Advanced A1 |
| WF-33 | DPDP data-principal-rights request | Handle access, correction, erasure, objection, grievance and nomination requests end to end within statutory and internal deadlines, with evidence (CAP-X3-16; DP-R9; BRL-PRV-01…05). | Partially automated | Human gates | — | In hosting | Advanced A1 |
| WF-34 | SLO breach auto-remediation with human approval | Move from a burn-rate page to a verified, approved fix with consistent steps and a postmortem draft (CAP-X3-09, CAP-X3-12; DEC-407). | Partially automated | Human gates | — | In hosting | Advanced A1 |
| WF-35 | Automated DR drill and game day | Prove RPO/RTO targets (OKPI-18, 19, 32, 33, 34) and runbook readiness on a schedule without touching production dispatch (CAP-X3-10, CAP-X3-11). | Partially automated | Human gates | — | In hosting | Advanced A1 |
| WF-36 | Just-in-time privileged access elevation | Replace standing privileged permissions with time-boxed, approved elevation on a healthy device (CAP-X3-13, CAP-X3-14). | Partially automated | Human gates | — | In hosting | Advanced A1 |
| WF-39 | Secrets rotation with overlap | Rotate every secret on time without downtime, including providers without a rotation API (CAP-X3-18; §4.6.2; doc 27 §Secret lifecycle). | Partially automated | Human gates | — | In hosting | Advanced A1 |

# 7. Technology used

| Area | Technology | Where it runs |
|----------------|------------------------------------------------------------|------------------|
| Website / Portal frontend | React 18 + TypeScript, Vite, React Router, TanStack Query, design system with CSS variables, i18n-ready; WCAG 2.2 AA; 34 screens (W01–W34) + advanced screens | Vercel Pro (CDN, firewall, previews) |
| Admin Command Centre frontend | React + TypeScript, role-based navigation for 7 views, data grids, approval queues, live monitor, policy/budget/tenant admin; 113 screens (A001–A113) + advanced screens (A114–A169) | Vercel Pro, separate project and origin |
| Backend API | Python 3.12, Django + Django REST Framework modular monolith; OpenAPI contracts (579 operations); Pydantic validation | AWS ap-south-1 (EC2/ECS on EC2) |
| Background jobs and scheduling | Celery + Celery Beat; transactional outbox; idempotent provider adapters | AWS ap-south-1 |
| Cache, queues, rate limits | Valkey (Redis-compatible) | AWS ap-south-1 |
| Database | PostgreSQL with row-level security (tenant isolation), pgvector (AI retrieval), audit tables | Supabase Pro, Mumbai region |
| Files and backups | Supabase storage / Amazon S3; nightly logical backup and cross-region DR copy | Supabase + AWS S3 |
| Identity and access | Django identity, MFA and passkeys (WebAuthn), RBAC roles R01–R20, ABAC rules, just-in-time admin elevation; Supabase Auth not used | Backend |
| Policy and safety | Policy Decision Point with dispatch-time recheck (scope, consent, jurisdiction, budget, approval hash); emergency stop; autonomy caps (consequential actions ≤ L1) | Backend |
| AI model gateway | Claude: Tier 0 rules and cache → Haiku-class → Sonnet-class (primary, DEC-418) → non-personal free fallbacks (off by default) → graceful degradation; hard monthly caps | Anthropic API via backend |
| AI engineering | Prompt contracts and registry, pgvector RAG, Pydantic output schemas, evaluation sets, red-team and drift checks, Langfuse tracing | Backend + Langfuse |
| Messaging | Amazon SES (email), Meta WhatsApp Cloud API, consent ledger, quiet hours, suppression | AWS + Meta |
| Search and extraction | Public search API, self-hosted extraction first | Providers |
| Administration and operations | Tenant/startup onboarding, plans and metering, budgets and alerts, audit log, approvals, data-rights (DPDP) workflow, status page and trust centre | Admin Command Centre + backend |
| Security tooling | Semgrep (SAST), Trivy (dependencies/containers), OWASP ZAP (DAST), secret scanning, secrets rotation, independent penetration test | CI + vendor |
| Observability | Sentry (errors), Prometheus/Grafana or provider metrics, uptime checks, Langfuse (AI) | Free tiers / self-hosted |
| CI/CD and infrastructure | GitHub + GitHub Actions, infrastructure as code (Terraform), environment promotion with approvals | GitHub |
| Testing | pytest, Playwright (UI), k6 (load), axe-core (accessibility), AI evaluation harness | CI |
| Building with AI | Claude Code (Claude Max 20x) interactive and headless agents, Claude API in CI for parallel agents, sandboxed branches, human review of every pull request | Builder |

# 8. Skill set applied by the builder

| Role | Skills |
|---|---|
| Solutions architect and security designer | Multi-tenant SaaS, RLS, policy engines, threat modelling |
| Business analyst / product owner proxy | User stories, Gherkin acceptance criteria, UAT |
| Full-stack engineer | Django/DRF APIs and workflows; React/TypeScript screens |
| AI/LLM engineer | Prompt contracts, RAG, guardrails, evaluations, cost control |
| QA and test automation | Test strategy, automation, performance, accessibility |
| DevOps / SRE | CI/CD, IaC, monitoring, backups, DR |
| UX designer | Information architecture, accessible UI |
| AI-agent orchestrator | Writing specs for agents, running parallel agents, reviewing and merging their output |

# 9. Payment schedule (A, B builder items)

| Milestone | When | Share | Amount (excl. GST) |
|---|---|---|---|
| Contract signing | Week 0 | 20% | ₹3,22,590 |
| Foundation gate | End of month 1 | 20% | ₹3,22,590 |
| Release 1 UAT start | End of month 2 | 20% | ₹3,22,590 |
| Core go-live (Release 1 + 2) | End of month 3 | 20% | ₹3,22,590 |
| A1 go-live and acceptance | End of month 4 | 20% | ₹3,22,590 |
| **Total builder invoice** |  | 100% | **₹16,12,948** |

Penetration testing (A4) and client-owned subscriptions (B7–B10, C1) are paid to the providers at actuals; the retainer (C2) is billed monthly from go-live.

# 10. Assumptions

1. Scope: Application Blueprint v1.1, Core + Advanced A1. Changes are made by written change request.
2. The 4-month duration assumes AI agents execute almost all implementation; the blueprint's own solo estimate is about 44 months. If more time is needed, A1 time and B subscriptions rise in proportion.
3. Builder's time at ₹1,25,000 per month; token use ≈ $6.78 per agent-executed person-day, with list prices as of 28 Nov 2026 (verify).
4. Claude Sonnet primary (DEC-418); Vercel + Supabase + AWS Mumbai (DEC-421); running budget DEC-422.
5. Excluded: GST (shown separately), external legal counsel, paid data, advertising, payment-gateway fees.
6. Build agents use synthetic data only. Every AI-generated change gets human review, and AI never takes consequential actions on its own.
