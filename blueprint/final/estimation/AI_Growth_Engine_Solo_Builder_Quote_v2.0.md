# AI Growth Engine: Final Solo-Builder Quotation
## Core platform + Advanced release A1, built single-handedly with AI models and AI agents · fixed price in INR

| Field | Value |
|---|---|
| Quotation | AI Growth Engine – Employee Sales & Marketing Automation platform: **Core platform (Releases 1 and 2) + Advanced release A1** |
| Prepared for | [Client name] |
| Prepared by | [Your name / company] |
| Version and date | Final quotation v2.0 · 28 Nov 2026 (supersedes the solo quotation v1.0) |
| Validity | 30 days |
| Basis | Application Blueprint v1.1 (Parts 0–9.10, 344 decisions); Cost Estimates v1.0 (traditional) and v1.1 (AI-built) |
| Currency | INR. GST at 18% is added to every fee. USD-billed subscriptions converted at ₹90 = $1 (verify at payment) |

# 1. The quotation at a glance

| Item | Excluding GST | GST 18% | Including GST | Basis |
|---|---|---|---|---|
| **Fixed development fee: Core platform + Advanced A1** | **₹76,00,000** | ₹13,68,000 | **₹89,68,000** | Cost-based (§4); ≈ 44 months; one builder with AI agents |
| Same scope bought separately (solo quotation v1.0) | ₹80,00,000 | ₹14,40,000 | ₹94,40,000 | Core ₹49,00,000 + A1 ₹31,00,000 |
| **Bundle saving** | **₹4,00,000** |  | **₹4,72,000** | Fee set at the cost basis rounded up to the next ₹50,000 |
| Maintenance and support retainer (after go-live) | ₹65,000 per month | ₹11,700 | ₹76,700 per month | §9 |
| Pass-through: independent security testing (3 tests) | ₹5,50,000 – ₹14,00,000 | As invoiced | As invoiced | At actuals with receipts (§7) |
| Pass-through: client-owned infrastructure while building (Vercel, Supabase, AWS staging, domains) | ₹6,750 – ₹11,070 per month | As invoiced | As invoiced | §6.1 |
| Pass-through: running the application after go-live | ₹37,614 – ₹71,024 per month | As invoiced | As invoiced | §6.2 (with 15% contingency) |

**Who pays for which subscription while building.**

- **In the fee:** the builder's own tools for the whole build, ₹10.50 L (§4). These are Claude Max 20x, GitHub, Figma, BrowserStack and Workspace.
- **Paid by the client:** Vercel, Supabase, AWS and the domains. These are opened in the client's own name from day one, so the client owns its infrastructure and data from the start.

**Why this price is fair.** A traditional team would charge about **₹1.16 crore**, and an AI-assisted team about **₹85 lakh**, for the same scope (Cost Estimates v1.0 and v1.1, central). This quotation is **₹76,00,000**. The client pays only for the effort that remains after AI agents do most of the drafting, coding and testing. The trade-off is time: about 44 months, against about 12–13 months for a team.

# 2. What the client receives

## 2.1 Core platform (Releases 1 and 2)

- Public Website/Portal (34 screens) and confidential Admin Command Centre (113 screens) as separate React/TypeScript applications on separate origins.
- Multi-tenant platform: Owner Portfolio tenant with AppNAI, MedMaarg, EduVerse and OrganicSpec, plus onboarding of external SaaS tenants with plans and metering.
- Business workflows WF-01 to WF-14: product catalogue, discovery, outreach under consent, inbound handling, qualification, meetings, bids, proposals and quotes, orders, verified close, onboarding, plans and offboarding.
- Policy Decision Point with dispatch-time recheck of scope, consent, jurisdiction, budget and approval; transactional outbox; audit trail; emergency stop.
- Model gateway with Claude Sonnet as the primary model (DEC-418): rules and cache first, then Haiku-class, then Sonnet-class, then non-personal free fallbacks (off by default), then graceful degradation; hard monthly caps.
- 100% literal alignment work with the 38-document specification (99.98% literal match; the two remaining items follow the approved Claude-primary decision).

## 2.2 Advanced release A1

- AI: agent supervisor/planner, account research, predictive score explanations (advisory), RFP response co-pilot, knowledge freshness, agent red-team and drift checks, data-quality steward, prompt/agent registry with canary rollout.
- Revenue growth: pipeline inspection and forecast risk, lead-to-account routing with speed-to-lead SLAs, multichannel cadences under consent (LinkedIn and calls as human tasks), CPQ guardrails inside approved price books, buying-committee suggestions, customer-health explanations.
- Platform: AI observability, disaster-recovery drills, passkeys, just-in-time admin access, secrets rotation, supply-chain checks, FinOps insights, automated DPDP data-rights workflow, status page and trust centre.

## 2.3 Deliverables with every release

Source code and infrastructure code in the client's repository, automated tests (unit, API, UI), AI evaluation sets, release evidence packs, runbooks, training task cards, architecture decision records, and a handover session.

## 2.4 Not included

Advanced releases A2 and A3 (indicative prices in §10), Phase-2 (W6) Should/Could items, paid data and advertising, legal advice, and third-party fees listed in §7.

# 3. AI agents, automations and workflows in the quoted scope

| Type | In scope | Fully automated | Mostly automated | Partially automated | Assistive only | AI run cost (pilot) |
|---|---|---|---|---|---|---|
| AI agents | 50 | 8 | 7 | 23 | 12 | ₹3,381/month |
| Automations | 85 | 80 | 0 | 5 | 0 | Inside hosting |
| Business workflows | 35 | 0 | 0 | 35 | 0 | Inside hosting |
| **Total in scope** | **170** | **88** | **7** | **63** | **12** | **≈ ₹4,226/month incl. 25% overhead** |

| Automation level | Meaning |
|---|---|
| Fully automated | Runs without a person inside policy guardrails. Deterministic automations, and AI agents acting only on low-risk internal items (L3), are always audited |
| Mostly automated | AI acts and a person reviews afterwards and can reverse (L2) |
| Partially automated | AI or rules prepare; a person approves before anything leaves the system (L1). All consequential actions (quotes, discounts, contracts, bids, payments) are here or manual: **AI never signs, pays, submits bids or sets prices** |
| Assistive only | AI suggests; a person acts (L0) |

Outside the quoted scope (future options): 30 agents, 34 automations and 3 workflows in A2, A3 and Phase 2.

## 3.1 AI agents included (50)

| ID | Name | What it does | Automation | Autonomy | Model | AI cost/month | Release |
|-----|------------|----------------------------------------|--------|---------|---------|------|-------|
| AG-001 | Knowledge & Claim Ingestion Assistant | Turns approved uploaded decks, brochures and FAQs into chunk summaries and claim candidates with page citations, so R10/R05 approve claims in minutes instead of reading whole documents. | Partially automated | L1 | 1a Haiku 5.5 | ₹5 | Release 1 |
| AG-002 | AI Quality Judge & Eval Runner | Scores generative outputs against rubrics (groundedness, claim compliance, tone, refusal correctness) for the CI regression gate and for a 5% sample of production outputs. | Mostly automated | L2 (scores recorded automatically; a hum | 1b Sonnet 5.5 via Batch API | ₹139 | Release 1 |
| AG-003 | Research Query Planner | Expands approved capability codes, geography and organization types into scoped search queries within the plan's source and cost bounds. | Fully automated within guardrails | L3 within guardrails (queries only reach | Tier 0 templates first | ₹1 | Release 1 |
| AG-004 | Evidence Extractor | Extracts organization-level business facts (projects, tenders, expansions, hiring for relevant functions, budgets, dates) with quotes and provenance from permitted pages and permitted social posts. | Fully automated within guardrails | L3 within guardrails (writes evidence re | 1a Haiku 5.5 via Batch API | ₹19 | Release 1 |
| AG-005 | Buying Signal Classifier | Classifies each evidence item into the approved signal taxonomy with confidence; below-threshold items go to review. | Mostly automated | L2 (classification stored; items below t | 1a Haiku 5.5 via Batch API | ₹6 | Release 1 |
| AG-006 | Need Discovery Agent | Derives business needs from signals and evidence and labels each as explicit (stated in a source) or inferred. | Mostly automated | L1 for inferred needs (reviewer verifies | 1a Haiku 5.5 via Batch | ₹6 | Release 1 |
| AG-007 | Solution Match Explainer | Explains why each deterministically ranked offering (AU-016) fits a need and why others were excluded (readiness, geography, capability). | Assistive only | L0 (suggestion only; ranking is determin | 1a Haiku 5.5 via Batch | ₹2 | Release 1 |
| AG-008 | Decision-Maker Role Extractor | Extracts role hypotheses (function, seniority) and published professional channels from official organization pages for qualified accounts. | Partially automated | L1 (contact records created as unverifie | 1a Haiku 5.5 via Batch | ₹1 | Release 1 |
| AG-009 | Qualification Brief Assistant | Prepares a one-screen cited brief per opportunity (need, fit, evidence freshness, score components, open questions) for the reviewer; at L2 (after the 90% gate) proposes accept/reject. | Partially automated | L1 until benchmark precision ≥ 90% on ≥  | 1a Haiku 5.5 pre-generated in  | ₹11 | Release 1 |
| AG-010 | Import Mapping Assistant | Maps unmatched CSV/JSON column headers and value formats to versioned import templates after deterministic header matching. | Partially automated | L1 (user confirms mapping before import) | Tier 0 header dictionary first | ₹0 | Release 1 |
| AG-011 | Outreach & Follow-up Message Drafter | Drafts evidence-cited first-touch emails, WhatsApp template variants, follow-up steps, event invitations and renewal reminders using approved claims only. | Mostly automated | L1 for personalised drafts (human approv | 1b Sonnet 5.5 | ₹165 | Release 1 |
| AG-012 | Claims & Policy Guard | Second-line check of every customer-facing draft (messages, content, proposals, chat answers sampled) for unsupported claims, prohibited content, tone and brand. | Fully automated within guardrails | L3 within guardrails for block/fix decis | Tier 0 deterministic rules fir | ₹20 | Release 1 |
| AG-013 | Inbound Intent Classifier & Router | Classifies every inbound email, WhatsApp and web reply (positive, question, objection, out-of-office, complaint, urgent/clinical, wrong person, other), extracts proposed times and a one-line summary, and routes it. | Fully automated within guardrails | L3 for routing and sequence stop (classi | Tier 0: STOP keywords, auto-re | ₹9 | Release 1 |
| AG-014 | Reply Assistant | Drafts answers to inbound questions from approved FAQ and knowledge with citations; at L3, sends only approved FAQ answers verbatim with variables. | Fully automated within guardrails | L1 by default; L3 only when the answer i | Tier 0 semantic cache of appro | ₹27 | Release 1 |
| AG-015 | Admin Copilot | Side-panel assistant that answers staff questions over records the user can already see and approved knowledge, with citations; briefs on accounts and meetings; proposes saved-view filters and drafts (message, task, note). | Assistive only | L0 answers; L1 drafts (DEC-035) | 1a Haiku 5.5 for lookups | ₹222 | Release 2 |
| AG-016 | Autonomous Commercial Planner | Proposes commercial plans (objective, eligible segment, channel mix, sequence, budget, schedule) and workflow drafts from approved node types; narrates simulation results. | Partially automated | L1 for the plan (approval of the exact p | 1b Sonnet 5.5 | ₹26 | Release 2 |
| AG-017 | Website Assistant | Public chat on each verified startup site that answers from approved public knowledge with citations, captures a consented lead and hands over clinical, legal, pricing-negotiation and complaint topics. | Fully automated within guardrails | L3 for answers grounded in approved publ | Tier 0 FAQ cache | ₹13 | Release 1 |
| AG-018 | Content & Campaign Studio Drafter | Drafts articles, social variants, landing-page copy, ad copy, SEO titles/meta and translation drafts (hi-IN, ta-IN, or-IN) from a brief using approved claims. | Partially automated | L1 (content approver ≠ author; claims ap | 1b Sonnet 5.5 | ₹98 | Release 1 |
| AG-019 | Bid / RFP Analyzer | Parses RFPs, tenders and submitted project requirements into eligibility criteria, deadlines, mandatory documents, evaluation criteria and a compliance matrix, plus an L0 bid/no-bid brief. | Assistive only | L1 for checklist items; L0 for bid/no-bi | 1b Sonnet 5.5 | ₹141 | Release 2 |
| AG-020 | Proposal & Bid Response Drafter | Drafts proposals and bid response sections from approved templates, meeting notes entered by staff, approved claims and the deterministic price snapshot (prices inserted by AU-035, never by the model). | Partially automated | L1 (DEC-064: proposals/quotes ≤ L1) | 1b Sonnet 5.5 | ₹63 | Release 2 |
| AG-021 | Objection & Negotiation Assistant | Classifies objections into the approved taxonomy, drafts approved responses, and prepares exception summaries for A070 when a request exceeds concession limits. | Partially automated | L1 (price/terms ≤ L1, DEC-064) | 1b Sonnet 5.5 | ₹22 | Release 2 |
| AG-022 | Contract Clause Reviewer | Compares counterparty redlines or third-party paper against the approved template and clause library; flags non-standard, missing or risky clauses for Legal with references. | Assistive only | L0 (suggest only) | 1b Sonnet 5.5 | ₹18 | Release 2 |
| AG-023 | Order Document Extractor | Extracts RFQ/PO lines (SKU, description, unit, quantity, requested price, delivery date/region) from uploaded documents and emails into a draft order or RFQ for OrganicSpec and other order-desk startups. | Partially automated | L1 (draft order; coordinator confirms) | 1a Haiku 5.5 | ₹5 | Release 2 |
| AG-024 | Payment Evidence Extractor | Pre-fills payment verification fields (UTR/reference, amount, currency, date, payer name, bank) from uploaded bank/UPI evidence for the Finance Maker. | Assistive only | L0 (pre-fill; maker confirms every field | 1a Haiku 5.5 | ₹1 | Release 2 |
| AG-025 | Onboarding Handoff Summarizer | Produces the commercial-to-delivery handoff summary (scope, commitments, contacts' roles, open risks, approved terms references) when a deal closes. | Partially automated | L1 | 1a Haiku 5.5 via Batch | ₹0 | Release 2 |
| AG-026 | Loss & Feedback Analyzer | Classifies free-text loss reasons and customer feedback into the loss taxonomy and produces a monthly theme report. | Mostly automated | L2 (labels stored; owner can correct) | 1a Haiku 5.5 via Batch | ₹0 | Release 2 |
| AG-027 | Market & Competitor Watch Summarizer | Summarizes permitted public competitor and market events into internal alerts with sources. | Fully automated within guardrails | L3 for internal alerts only (no external | 1a Haiku 5.5 via Batch | ₹1 | Release 2 |
| AG-028 | Ops & Incident Triage Agent | Clusters failed runs, DLQ items, provider errors and alerts; summarizes probable cause and links the runbook (RB-) for on-call staff. | Assistive only | L0 (suggestions only); remediation by hu | 1a Haiku 5.5 | ₹7 | Release 2 |
| AG-029 | Insight Narrative Agent | Writes weekly 'what changed and why' narratives on deterministic KPI snapshots for startup heads and a portfolio digest for the founder. | Fully automated within guardrails | L3 for internal digest delivery | 1a Haiku 5.5 via Batch | ₹1 | Release 2 |
| AG-030 | SaaS Onboarding Configuration Assistant | During W33, proposes business profile, industry taxonomy, offering structure, objective templates and workflow bindings from the applicant's description. | Partially automated | L1 (applicant edits; platform approval b | 1b Sonnet 5.5 | ₹35 | Release 2 |
| AG-031 | Support Desk Assistant | Triages portal support tickets (W28, W34) by category and severity, drafts replies from the help centre, answers authenticated customers' questions about their own records, and drafts KB articles from resolved tickets. | Mostly automated | L1 for replies; L2 for category/severity | 1a Haiku 5.5 | ₹14 | Release 2 |
| AG-033 | Requirements & Story Assistant | Drafts user stories, Gherkin AC, ADR and DPIA skeletons from FR/BRL/DEC text, and runs change-impact analysis over the traceability matrix. | Partially automated | L1 (PR review by PO) | Claude Code developer seats | ₹505 | Release 1 |
| AG-034 | Coding Assistant | Claude Code for implementation, refactoring, IaC, UI microcopy and accessibility fixes, with repository rules (RLS scoping, outbox, no secrets). | Partially automated | L1 (all changes through PR review + CI g | Claude Code developer seats | ₹505 | Release 1 |
| AG-035 | PR, Security & Release Review Agent | Reviews each pull request for tenancy/RLS scoping, outbox use, secret exposure, OWASP issues, missing tests; triages CI failures and SAST/dependency findings; drafts release notes and go/no-go summaries; drafts threat-model update… | Assistive only | L0 (comments only; cannot approve or mer | 1b Sonnet 5.5 via CI API key | ₹505 | Release 1 |
| AG-036 | Test & Synthetic Data Generator | Generates test cases from Gherkin AC (EP/BVA/decision-table techniques), synthetic two-tenant fixtures (RECOMMENDATION-017), injection corpora and eval cases from reviewed feedback. | Partially automated | L1 (QA review) | Claude Code seats + 1a Haiku 5 | ₹6 | Release 1 |
| AG-037 | Meeting Notes & Action Summarizer | Turns staff-written meeting notes (and, only after GAP-143 is resolved with consent, authorized transcripts) into a structured summary, decisions and action items that distinguish confirmed from unconfirmed commitments, so follow-… | Partially automated | L1. Organizer approves the summary; acti | 1a Haiku 5.5; 15% escalation t | ₹7 | Release 2 |
| AG-038 | Retention Next-Best-Action Advisor | For accounts entering the renewal window (AU-039), reads delivery milestones, feedback, support history and contract dates and proposes one next best action (check-in, success review, upsell discussion within approved offerings, r… | Assistive only | L0 (suggest only). Owner accepts, edits  | 1a Haiku 5.5 via Batch; 10% es | ₹5 | Release 2 |
| AG-039 | Agent Supervisor and Planner | Turns a staff objective ("pursue account X for offering Y", "prepare RFP response", "prepare launch brief") into a typed, budgeted, approvable plan over registered agents and automations, so multi-step work starts in minutes with … | Partially automated | L1. A plan containing any W1 step (draft | 1b Sonnet 5.5 (effort medium;  | ₹120 | Advanced A1 |
| AG-040 | Account Research Agent | Builds one cited, versioned account brief per organization from owned records (CRM, evidence, interactions) and permitted public sources only (AU-007), so every account-centric agent and person works from the same facts; no person… | Assistive only | L0. Brief is informational; memory propo | 1a Haiku 5.5 via Batch; 15% es | ₹20 | Advanced A1 |
| AG-047 | RFP Response Co-pilot | For each requirement extracted by AG-019, retrieves matching approved, unexpired answers from the answer library (AU-063), drafts the response with per-answer citations and confidence, lists gaps with owners, and fills the complia… | Partially automated | L1. Bid owner approves each answer (auth | 1b Sonnet 5.5; RFP prefix cach | ₹401 | Advanced A1 |
| AG-055 | Knowledge Curator and RAG Freshness Agent | Reviews AU-069 findings (stale chunks, conflicting facts across documents, near-duplicates, coverage gaps from clustered abstentions and retrieval misses) and drafts concrete edits or new FAQ entries for knowledge owners, so groun… | Partially automated | L1. Owner approves; approved edits re-en | 1a Haiku 5.5 via Batch; 10% es | ₹14 | Advanced A1 |
| AG-056 | Agent Red-Team and Drift Analyst | Generates mutations of the seed injection, jailbreak, cross-audience and data-exfiltration corpora (paraphrase, language switch to hi/ta/or, encoding, indirect via document/email/WhatsApp formats) for scheduled runs (AU-070), and … | Mostly automated | L0 for findings; L2 for writing candidat | 1b Sonnet 5.5 via Batch (line  | ₹84 | Advanced A1 |
| AG-060 | Data-Quality and Dedupe Steward | Reviews candidate duplicate pairs from AU-074 blocking (similar names, domains, addresses, aliases) and inconsistent fields, and proposes merge / keep-separate with field-level resolutions and evidence, so duplicates fall and prop… | Partially automated | L1. R04 approves each merge in A018 merg | 1a Haiku 5.5 via Batch; 10% es | ₹9 | Advanced A1 |
| AG-062 | Signal Fusion "Why-Now" Brief Writer | Writes a three-sentence "why now" brief for each surging account and for each newly routed hot lead, citing the deterministic intent components (AU-084) and evidence, so sellers act on timing within the SLA (KPI-ADV-X2-03) | Assistive only | L0. Advisory text shown on A132 and on t | 1a; 10% escalation to 1b when  | ₹35 | Advanced A1 |
| AG-064 | Pipeline Inspection and Forecast Risk Analyst | For each open deal, turns deterministic facts and AU-088 flags into a short risk note with cited facts and three inspection questions; for the forecast roll-up, explains week-over-week changes. Managers inspect more deals in less … | Assistive only | L0. Advisory only; cannot change categor | 1a; 20% escalation to 1b for d | ₹48 | Advanced A1 |
| AG-066 | CPQ Bundle Advisor and Guardrail Explainer | Given the stated need and the active price book, suggests up to three approved bundles or line sets with reasons, and explains guardrail results (AU-089) in plain language with the next allowed action, so time-to-quote falls and f… | Assistive only | L0. Seller chooses; AU-089 and AU-035 co | 1a; 10% escalation to 1b | ₹15 | Advanced A1 |
| AG-074 | AI Observability Drift Analyst | Turns trace aggregates, eval scores and feedback into a weekly per-agent health note with regressions linked to prompt or model revisions, so AI quality regressions are found ≤ 24 h after the alert and fixed before users notice (d… | Partially automated | L1. Report reviewed by AI lead; actions  | 1a Haiku 5.5; 10% escalation | ₹4 | Advanced A1 |
| AG-077 | Supply-Chain Risk Analyst | Shortens triage of new CVEs in deployed components by drafting exploitability notes and VEX candidates with evidence, so Critical findings are triaged ≤ 24 h and remediated within §4.16.3 SLAs | Partially automated | L1. A reviewer ≠ author accepts VEX (BRL | 1a Haiku 5.5; 15% escalation | ₹10 | Advanced A1 |
| AG-078 | Secrets Rotation Coordinator | For providers without a rotation API, drafts the exact console steps, overlap window and verification call, so guided rotations finish on time with no downtime (NFR-ADV-X3-14) | Partially automated | L1. Human performs provider console step | 1a Haiku 5.5; no escalation | ₹1 | Advanced A1 |
| AG-080 | FinOps Optimization Agent | Turns measured utilization and cost ledgers into a ranked list of savings with formulas and SLO risk, so ≥ 10% of infrastructure spend is identified as addressable per quarter without SLO violation (doc 36 OPT-03-04) and KPI-21/22… | Partially automated | L1. Recommendations read-only until appr | 1a Haiku 5.5; 20% escalation | ₹9 | Advanced A1 |

## 3.2 Automations included (85)

| ID | Name | What it does | Automation | Autonomy | Model | AI cost/month | Release |
|-----|------------|----------------------------------------|--------|---------|---------|------|-------|
| AU-001 | Model gateway router, Tier 0 cache & template responder | Routing decision table (§7.3.4); exact-match cache key = hash(agent, prompt version, model, normalized input, scope); semantic cache (pgvector cosine ≥ 0.92, same tenant/startup namespace, Public/Internal only); approved template … | Fully automated | L3 (deterministic, within policy) | — | In hosting | Release 1 |
| AU-002 | Budget reservation, alerts & hard stop | Reserve estimated ₹ (max_tokens × output price + input estimate) against agent, startup, tenant and global budgets; reconcile actual usage; 80% alert, 100% hard stop; founder top-up audited | Fully automated | L3 (deterministic, within policy) | — | In hosting | Release 1 |
| AU-003 | Output schema validation & repair controller | Validate JSON against versioned schema; up to 2 repair retries with the validation error; then route per §7.3.4 (Tier 2 only if data class allows) else Tier 3 | Fully automated | L3 (deterministic, within policy) | — | In hosting | Release 1 |
| AU-004 | Data classification & PII redaction | Field-level classification from the data dictionary + Presidio analyzers (email, phone, Aadhaar/PAN patterns, names, health terms) with Indian recognizers; mask/pseudonymize; block Tier 2 if Restricted/Confidential remains | Fully automated | L3 (deterministic, within policy) | — | In hosting | Release 1 |
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
| AU-045 | Matched-sample provider benchmark harness | Validates dataset (non-empty, unique opaque sample and expected-result IDs, no negative/nonfinite costs or latencies, same currency); runs baseline and candidate on identical sources; computes micro P/R, nearest-rank p95, failure … | Fully automated | L3 rules (verdict reviewed by QA) | — | In hosting | Release 1 |
| AU-046 | Knowledge revocation & derivative purge | Sets revoked_at; deletes embeddings; purges exact/semantic caches by knowledge revision; invalidates Copilot summaries; legal hold respected | Fully automated | L3 rules | — | In hosting | Release 1 |
| AU-047 | Dependency & model-weight licence gate | SBOM → licence register match; fail on unknown, AGPL-linked, weights without commercial use, stale review | Fully automated | L3 rules | — | In hosting | Release 1 |
| AU-048 | Provider invoice ↔ usage reconciliation | Matches invoice lines to metered usage by provider, account, period, unit; tolerance 2% or ₹100; dedupes usage events by provider event ID | Fully automated | L3 rules | — | In hosting | Release 2 |
| AU-049 | Tenant contribution-margin calculator | Margin = recognized service revenue − (direct provider cost + AI cost + allocated infra + allocated support), per tenant and cohort; allocation basis versioned | Fully automated | L3 rules | — | In hosting | Release 2 |
| AU-050 | Adapter retirement & credential revocation | Disable new calls; drain and reconcile pending events and invoices; export/delete provider-held data per policy; revoke credentials and webhooks; test replacement; mark Retired | Fully automated | L3 rules (owner signs off) | — | In hosting | Release 2 |
| AU-051 | Event registration capacity, dedupe & reminders | Capacity check with row lock; dedupe by normalized email + event; waitlist; consented reminders through outbox; attendance import | Fully automated | L3 rules | — | In hosting | Release 1 |
| AU-052 | Tender amendment detector & evidence refresh | Compares portal document hashes and deadline fields; on change creates amendment record, re-runs AG-019 checklist diff, updates AU-034 deadlines, notifies bid owner | Fully automated | L3 rules | — | In hosting | Release 2 |
| AU-053 | Supervisor plan validator and step guard | Rules PV-01…PV-10 (§9.7.4.2): registry enabled and pinned, DAG acyclic, ≤ 12 agent steps, Σ step cost ≤ reservation and ≤ ₹25 default, monotonic data class, guard + checkpoint after customer-facing drafts, minors/clinical exclusio… | Fully automated | L3 (deterministic, within policy) | — | In hosting | Advanced A1 |
| AU-054 | Agent version canary controller and auto-rollback | Hash (tenant_id, object_id) into buckets; route 5% → 25% → 100% with minimum dwell 48 h / 72 h; compare SLOs (AU-071) of canary vs control; rollback if any SLO burn rate > 2× over 1 h, any mandatory check fails once, or cost per t… | Fully automated | L3 (deterministic, within policy) | — | In hosting | Advanced A1 |
| AU-057 | Model and agent drift monitor | PSI per ML feature and score distribution (alert > 0.2); KS test on agent confidence distributions; 7-day trends in abstention, schema-repair, escalation share, accept/edit/reject; fairness slices per §7.6.6 | Fully automated | L3 (deterministic, within policy) | — | In hosting | Advanced A1 |
| AU-061 | Memory consent, retention and purge controller | Enforce ai_memory_policy (enabled, fact types, TTL); expire items past expires_at; purge on privacy request via AU-011 locator incl. memory_refs[] in envelopes; purge on tenant offboarding (WF-14); write purge certificate | Fully automated | L3 (deterministic, within policy) | — | In hosting | Advanced A1 |
| AU-062 | Memory write gate | Rules §9.7.4.4: allowlisted fact types, evidence required, special-category lexicon + Presidio + regex block, ≤ 280 chars, natural persons as contact_id + role only, minors/clinical block, dedupe by value hash, contradiction → rev… | Fully automated | L3 (deterministic, within policy) | — | In hosting | Advanced A1 |
| AU-063 | RFP answer library freshness and expiry | Each answer has owner, evidence, claim IDs, review_by (default 180 days); expire on claim expiry or review_by; notify owner at 30/7/1 days; block retrieval of expired answers; usage counter per bid | Fully automated | L3 (deterministic, within policy) | — | In hosting | Advanced A1 |
| AU-067 | Compliance pre-check for plans and campaigns | Checks: purpose and privacy-notice revision cover the processing; consent basis per recipient class and channel; jurisdiction rule pack (DEC-029) for target countries; minors and clinical exclusions; claims cited are approved and … | Fully automated | L3 (deterministic, within policy) | — | In hosting | Advanced A1 |
| AU-068 | Gateway cost optimizer | From the cost ledger and eval results: cache-miss hot spots (same prefix, low hit rate), prompts > p95 size for their agent, sync calls eligible for Batch, Sonnet-routed tasks where the Haiku eval meets thresholds, Tier 0 candidat… | Fully automated | L3 (deterministic, within policy) | — | In hosting | Advanced A1 |
| AU-069 | RAG freshness and coverage monitor | Stale: chunk age > source freshness SLA or referencing superseded price/offering versions; conflict: same entity attribute with different values across approved chunks; duplicate: cosine ≥ 0.97 within namespace; gap: abstention/re… | Fully automated | L3 (deterministic, within policy) | — | In hosting | Advanced A1 |
| AU-070 | Golden-set and red-team scheduler | Schedules AU-006 suites, AG-056 mutation runs and Tier 2 model resistance runs in the eval sandbox; compares with baseline (dataset hash pinned) | Fully automated | L3 (deterministic, within policy) | — | In hosting | Advanced A1 |
| AU-071 | Agent observability and AI SLO tracker | Per agent version SLOs (schema-valid ≥ 99.5%, groundedness ≥ 95% on sample, p95 latency, cost per task); 28-day error budget; multi-window burn-rate alerts (1 h and 6 h) | Fully automated | L3 (deterministic, within policy) | — | In hosting | Advanced A1 |
| AU-074 | Data-quality rules and dedupe blocking | Normalize names (legal suffixes, case, punctuation), domains, phone/address formats; blocking keys (domain root, normalized name trigram, city); Jaro-Winkler and token-set similarity; candidate pair if score ≥ 0.85 and same tenant… | Fully automated | L3 (deterministic, within policy) | — | In hosting | Advanced A1 |
| AU-078 | Human feedback capture and label queue | Store diff and reason; sample stratified items into a labelling queue (A128) with redaction; reviewer labels → candidate eval items; promotion to an eval set only with R10 + AI lead approval and new dataset hash | Fully automated | L3 (deterministic, within policy) | — | In hosting | Advanced A1 |
| AU-079 | AI system inventory and model-card sync | Maintain one inventory row per agent/automation-with-model and version: intended purpose, risk class (§9.7.12.1), data classes, autonomy cap, model tier, eval run IDs, fairness results, known limitations, oversight design, owner, … | Fully automated | L3 (deterministic, within policy) | — | In hosting | Advanced A1 |
| AU-080 | Lead-to-account matcher | Normalize email domain (public-suffix list), strip free-mail; organization name similarity (token-set ratio, RapidFuzz-class library), registered ID exact match, address match (libpostal-class normalizer), existing contact link; w… | Fully automated | L3 (deterministic, within policy) | — | In hosting | Advanced A1 |
| AU-081 | Owner routing and speed-to-lead SLA clock | Routing order existing owner → account owner → territory → capacity-weighted round robin; skip ineligible; SLA due = start + class SLA on owner's business calendar; 75/100/200% escalation ladder | Fully automated | L3 (deterministic, within policy) | — | In hosting | Advanced A1 |
| AU-084 | Signal fusion and intent decay scorer | Intent = min(100, Σ type_weight × topic_fit × 0.5^(age/half-life)); components stored; expired evidence removed; surge = +15 points in 7 days | Fully automated | L3 (deterministic, within policy) | — | In hosting | Advanced A1 |
| AU-085 | Buying-committee coverage calculator | Coverage = filled and engaged required slots ÷ required slots; single-threaded = 1 engaged member on a deal above threshold | Fully automated | L3 (deterministic, within policy) | — | In hosting | Advanced A1 |
| AU-086 | Multichannel cadence orchestrator | For each due step: PDP dry-run; automated channels → outbox with dispatch recheck (AU-009); human steps → task (A137); global stop on any stop event for the person across all cadences; committee pause; cumulative cap across channe… | Fully automated | L3 for scheduling (deterministic); dispa | — | In hosting | Advanced A1 |
| AU-087 | Forecast roll-up and weekly snapshot | Sum by category and owner chain; manager adjustments with reason; immutable snapshot (payload hash); attainment = Closed-Verified ÷ prior Commit; slippage = deals leaving Commit | Fully automated | L3 (deterministic, within policy) | — | In hosting | Advanced A1 |
| AU-088 | Pipeline hygiene and inspection flags | Rules: no next step; close date past; stage age > p75 of won deals; single-threaded; no MAP above threshold; amount change > 20% in a week; owner lacks grant | Fully automated | L3 (deterministic, within policy) | — | In hosting | Advanced A1 |
| AU-089 | CPQ guardrail evaluator | Validate lines against active price-book revision; required/excluded options; quantity bounds and breaks; validity ≤ max; margin ≥ floor (Decimal); discount band → approver per DEC-038 | Fully automated | L3 (deterministic, within policy) | — | In hosting | Advanced A1 |
| AU-093 | Customer health score v2 | Score = round(100 × Σ wᵢcᵢ ÷ Σ w_known); Unknown if known weight < 0.60; bands by template; trend over 30/90 days; quarterly back-test vs renewal outcome | Fully automated | L3 (deterministic, within policy) | — | In hosting | Advanced A1 |
| AU-102 | Semantic metric compiler & parity check | Compile YAML → SQL templates; run parity fixture vs legacy RP outputs; mark parity status | Fully automated | L2 (internal) | — | In hosting | Advanced A1 |
| AU-105 | AI trace redaction & telemetry shipper | Apply AU-004 DLP; replace Restricted by type tokens; hash Confidential bodies unless sampling allowed; emit OTel GenAI spans; aggregate daily | Fully automated | L2 (internal) | — | In hosting | Advanced A1 |
| AU-107 | Chaos scheduler & abort guard | Check environment = staging; start FIS template; watch stop conditions; abort ≤ 60 s; record result | Fully automated | L2 (staging only) | — | In hosting | Advanced A1 |
| AU-108 | DR drill orchestrator | Restore snapshot/PITR in backup sandbox with dispatch off; run integrity suite; time RPO/RTO; file evidence; destroy | Fully automated | L2 (isolated account) | — | In hosting | Advanced A1 |
| AU-109 | Status page publisher | Compute component state from external probes; publish approved notices; email subscribers | Partially automated | L2 for component state; L1 for incident  | — | In hosting | Advanced A1 |
| AU-110 | JIT privileged access broker | Grant bundle permissions with TTL; revoke on expiry/withdrawal; propagate session revocation ≤ 60 s | Partially automated | L1 (approval by another person) | — | In hosting | Advanced A1 |
| AU-111 | Device posture & session risk evaluator | Check device cert validity and binding, browser in matrix, passkey amr; compute posture level | Fully automated | L2 (protective: read-only downgrade) | — | In hosting | Advanced A1 |
| AU-112 | Rights request orchestrator | Start clocks; call AU-011 locators per store; build step proposals; apply approved steps; tombstones to lake; generate evidence pack | Partially automated | L1 per execution step | — | In hosting | Advanced A1 |
| AU-114 | Secrets rotation executor | Managed: create new version, test, promote, revoke old after overlap. Guided: open task with AG-078 steps, one-time value form, verify, revoke | Partially automated | L1 for guided and emergency; L2 for mana | — | In hosting | Advanced A1 |
| AU-115 | Supply-chain verification gate | Generate SBOM + provenance; verify cosign signature and builder identity at deploy; upload SBOM; nightly CVE match on deployed set; scan marketplace partner artefacts | Fully automated | L2 (block-only, protective) | — | In hosting | Advanced A1 |
| AU-118 | Rightsizing & idle-resource detector | p95 utilization vs allocation; idle EIPs/volumes; S3 lifecycle gaps; log outliers; AI cache misses | Partially automated | L1 (read-only recommendations) | — | In hosting | Advanced A1 |

## 3.3 Business workflows included (35)

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
| WF-09 | Proposal, quote and negotiation | Proposal and quote from approved templates and price versions; Decimal totals and tax; discount and legal approval thresholds; recipient review in portal; objections answered from approved facts or escalated (BRD §5; DEC-038) | Partially automated | Human gates | — | In hosting | Release 1 |
| WF-10 | Order and fulfilment (OrganicSpec route, BR-S004) | Buy/sell/service/training orders with SKU, unit and quantity lines; stock reservation; idempotent fulfilment events; over-delivery rejection; acceptance; separate receivable and payable ledgers (BRD §5; FR-DM-03) | Partially automated | Human gates | — | In hosting | Release 1 |
| WF-11 | Commercial closure (all routes) | Close only on route-specific verified evidence (signed contract or verified payment); finance maker-checker; partial payments; no duplicate revenue or false Won state (BRD §5; DEC-054) | Partially automated | Human gates | — | In hosting | Release 2 |
| WF-12 | Retention and renewal | Offering-specific onboarding and handoff (no patient data), milestones, feedback, renewal calendar and eligible reminders, lost-deal learning (BRD §5) | Partially automated | Human gates | — | In hosting | Release 2 |
| WF-13 | Autonomous plan | Objective-driven plan from approved templates; simulation of recipients, cost, deadlines and conflicts; approval of the exact plan hash; execution with dispatch-time recheck; live monitoring, budget hard stops and emergency stop (… | Partially automated | Human gates | — | In hosting | Release 2 |
| WF-14 | Suspend and offboard (tenant or startup) | Suspend or offboard a tenant/startup: stop schedules and queued actions, revoke senders and access, reconcile uncertain outcomes, export allowed records, apply retention (BRD §5) | Partially automated | Human gates | — | In hosting | Release 2 |
| WF-15 | Supervised multi-agent account pursuit | Pursue a qualified account through research, brief, next action and first-touch draft as one supervised plan, with every approval of the baseline preserved (ADR-110; BR-AUTO; DEC-064). | Partially automated | Human gates | — | In hosting | Advanced A1 |
| WF-16 | Predictive model lifecycle | Train, validate, shadow, approve, serve, monitor and retire advisory ML models (AU-056, AU-059, AU-066) without ever changing DEC-011 scoring or any eligibility decision (ADR-113; DEC-383). | Partially automated | Human gates | — | In hosting | Advanced A1 |
| WF-17 | Deal-risk and churn early warning | Nightly detect at-risk open deals (AU-058, AG-044) and, from A3, at-risk customers (AU-059 feeding AG-038), and turn each into an owner task with reasons, so intervention happens before the forecast or renewal date (BR-M21, BR-M50… | Partially automated | Human gates | — | In hosting | Advanced A1 |
| WF-18 | RFP response co-pilot (AppNAI) | Answer RFP requirements from the approved answer library with citations and gaps, inside WF-08, keeping bid/no-bid, pricing and submission human (BR-S001, DEC-053, DEC-064). | Partially automated | Human gates | — | In hosting | Advanced A1 |
| WF-19 | Localized personalization at scale | From a campaign brief and deterministic segments, generate guarded variants, localize them with TM and glossary, approve them as templates and test them, so personalized multilingual outreach scales under DEC-064 (BR-M25, BR-M34, … | Partially automated | Human gates | — | In hosting | Advanced A1 |
| WF-20 | Experiment lifecycle | Pre-register, approve, run, monitor and read out experiments on messages, sequences, content, agent versions and NBA policies, so lift claims rest on valid statistics (ADR-118; BR-S090). | Partially automated | Human gates | — | In hosting | Advanced A1 |
| WF-21 | Agent release, canary and red-team | Release any new agent, prompt, model or ML version through offline evals, red-team, shadow and staged canary with automatic rollback, and keep it under continuous adversarial and drift monitoring (ADR-111, ADR-117; BR-M54; OKPI-16… | Partially automated | Human gates | — | In hosting | Advanced A1 |
| WF-22 | Knowledge freshness and memory governance | Keep RAG knowledge current, consistent and complete (AU-069, AG-055) and keep long-term memory lawful (AU-061, AU-062), with all edits through the M03 approval pipeline and all memory under purpose, TTL and erasure (BR-M03, BR-M56… | Partially automated | Human gates | — | In hosting | Advanced A1 |
| WF-23 | WhatsApp concierge with human handoff | Answer customer-initiated WhatsApp conversations within the service window from approved knowledge, offer meeting slots, and hand off to a human for sensitive topics or on request (BR-M31, BR-M41; DEC-030, DEC-064). | Partially automated | Human gates | — | In hosting | Advanced A1 |
| WF-25 | Account-based engagement | Select and tier target accounts, map the buying committee, approve an account plan and run coordinated plays across sales, marketing, success and partners, without any automatic outreach beyond approved, eligible steps (F01–F04). | Partially automated | Human gates | — | In hosting | Advanced A1 |
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

# 4. How the price is arrived at

## 4.1 Method

- Start from the **traditional effort** in the blueprint: core build + literal alignment = 829 person-days; Advanced A1 = 553 person-days.
- Apply the **AI-built reduction for each activity** (Cost Estimate v1.1, central case). AI agents draft and code; the builder specifies, reviews, tests and releases. Weighted reduction **44.3%**.
- Add back the **new work AI creates**: agent specs and prompts, human review of every AI change, security and licence review, rework. That adds **15.5%**.
- Subtract the **solo coordination saving** (no team meetings or hand-offs): **4%**. Net saving **32.8%**.
- Value the builder's remaining days at **₹5,682 per day** (₹710 per hour; ₹1.25 lakh per month, senior rate within the blueprint band of ₹1.0–1.5 lakh).
- Add the **builder's tools** for the build duration (§6.1; client-owned infrastructure is billed separately), **Claude API tokens** for the coding agents (48% of the work executed by agents at ≈ $6.78 per agent-day), and **15% contingency** on time and tokens.
- Round up to the next ₹50,000. No further margin: the builder's income is the day rate.

## 4.2 Price build-up

| Component | Core platform | Advanced A1 | Total | Formula |
|---|---|---|---|---|
| Traditional effort (person-days) | 829 | 553 | 1,382 | Blueprint (Parts 8.4, 9.10) |
| Builder's effort with AI (person-days) | 557 | 372 | 929 | Traditional × (1 − 0.328) |
| Builder's hours | 4,458 | 2,973 | 7,431 | Days × 8 |
| Duration (months) | 26.5 | 17.7 | 44.2 | Days ÷ 21 productive days |
| Builder's time | ₹31.66 L | ₹21.11 L | ₹52.77 L | Days × ₹5,682 |
| Builder's tools (Claude Max 20x, GitHub, Figma, BrowserStack, Workspace) | ₹6.30 L | ₹4.20 L | ₹10.50 L | ≈ $264 per month × months × ₹90 |
| Claude API tokens for coding agents | ₹2.43 L | ₹1.62 L | ₹4.05 L | Agent-days (398 + 265) × $6.78 × ₹90 |
| Contingency | ₹5.11 L | ₹3.41 L | ₹8.52 L | 15% × (time + tokens) |
| **Cost basis** | **₹45.50 L** | **₹30.35 L** | **₹75.85 L** |  |
| **Quoted fixed fee** |  |  | **₹76.00 L** | Rounded up to the next ₹50,000 |

## 4.3 Effort by activity (builder's days)

| Activity | Core: traditional pd | Core: solo with AI pd | A1: traditional pd | A1: solo with AI pd | Total solo pd | Value |
|------------------------------|-------|-------|-------|-------|-------|--------|
| Requirements analysis, backlog and user-story drafting | 58 | 25 | 39 | 16 | 41 | ₹2.33 L |
| UX/UI design and accessibility | 50 | 35 | 33 | 23 | 59 | ₹3.34 L |
| Architecture, security and data design | 50 | 38 | 33 | 25 | 63 | ₹3.56 L |
| Backend development (APIs, rules, workflows, data) | 224 | 95 | 149 | 63 | 159 | ₹9.01 L |
| Frontend development (Website and Admin) | 124 | 53 | 83 | 35 | 88 | ₹5.00 L |
| AI engineering (agents, gateway, RAG, evaluations) | 83 | 55 | 55 | 37 | 91 | ₹5.19 L |
| Test strategy and test-case drafting | 33 | 11 | 22 | 7 | 18 | ₹1.04 L |
| Test automation and execution (unit, SIT, UAT, performance, security) | 91 | 52 | 61 | 34 | 86 | ₹4.89 L |
| DevOps, infrastructure, observability and release | 50 | 31 | 33 | 20 | 51 | ₹2.89 L |
| Project management, ceremonies and reporting | 41 | 33 | 28 | 22 | 55 | ₹3.15 L |
| Documentation, training content and handover | 25 | 9 | 17 | 6 | 16 | ₹0.89 L |
| Added by AI-built delivery: Agent orchestration, specification and prompt engineering | — | 31 | — | 21 | 52 | ₹2.96 L |
| Added by AI-built delivery: Human review and verification of AI output | — | 55 | — | 37 | 91 | ₹5.19 L |
| Added by AI-built delivery: Security, licence and provenance review of AI-generated code | — | 12 | — | 8 | 20 | ₹1.11 L |
| Added by AI-built delivery: Rework allowance for AI defects | — | 23 | — | 16 | 39 | ₹2.22 L |
| **Total** | **829** | **557** | **553** | **372** | **929** | **₹52.77 L** |

Activities include user-story drafting, test strategy and test-case drafting. The blueprint already contains drafts of all 461 stories and 4,156 test cases, and the builder refines them with AI assistance.

## 4.4 How AI agents do the work, and what the builder still does

| Activity | AI reduction | What the AI agents do | What the builder does |
|----------------------|------|------------------------------------|------------------------------------|
| Requirements analysis, backlog and user-story drafting | 55% | Drafts and refines stories, Gherkin AC and estimates from the blueprint drafts | client prioritizes and accepts; growth lead checks rules |
| UX/UI design and accessibility | 25% | Generates screen variants, copy, component code from the design system; accessibility checks | Designer owns IA, flows, usability tests and final design |
| Architecture, security and data design | 20% | Drafts ADRs, schemas, threat-model checklists, IaC skeletons | Lead architect decides; independent reviewer signs off |
| Backend development (APIs, rules, workflows, data) | 55% | Coding agents implement APIs, rules, migrations and workflows from specs and tests | Builder write specs, review every pull request, own design and merges |
| Frontend development (Website and Admin) | 55% | Agents build React screens from the screen contracts and design system | Builder review, fix edge cases, verify accessibility |
| AI engineering (agents, gateway, RAG, evaluations) | 30% | Drafts prompt contracts, eval sets, fixtures; scaffolds agents | AI builder owns guardrails, routing, evaluation thresholds |
| Test strategy and test-case drafting | 65% | Generates test cases, data and traceability from stories and FRs | QA lead reviews coverage and risk focus |
| Test automation and execution (unit, SIT, UAT, performance, security) | 40% | Writes unit/API/UI tests, triages failures, proposes fixes | QA executes UAT with users; performance and pen tests unchanged |
| DevOps, infrastructure, observability and release | 35% | Writes IaC, pipelines, dashboards and runbooks | DevOps builder approves changes to production |
| Project management, ceremonies and reporting | 15% | Status summaries, burn-down analysis, meeting notes | Lead and client run ceremonies and decisions |
| Documentation, training content and handover | 60% | Drafts docs, runbooks, task cards and release notes | Owners review for accuracy |

# 5. Technology and skill set

## 5.1 Technology stack

| Layer | Technology | Why |
|---|---|---|
| Frontends | React + TypeScript (Vite), design system, WCAG 2.2 AA; hosted on **Vercel** (two projects, separate origins) | Fast, accessible UIs; preview deployments for client review |
| Backend | Python, **Django REST Framework** modular monolith; Celery + Celery Beat; **Valkey** | Mature, secure, productive; background jobs and schedules |
| Database | **PostgreSQL on Supabase** (Mumbai): row-level security for tenant isolation, **pgvector** for AI retrieval, storage | Managed backups, scaling and security; India data residency |
| Compute and files | **AWS ap-south-1 (Mumbai)**: EC2/ECS for API and workers, S3 for files and DR copies, SES for email | Data stays in India; low cost at pilot scale |
| AI | **Claude** via the model gateway: Haiku-class and **Sonnet-class (primary, DEC-418)**; Pydantic schemas; prompt registry; evaluation harness | High-quality drafting and extraction with hard cost caps and human approval |
| Messaging | Meta WhatsApp Cloud API, Amazon SES, consent and quiet-hour rules | Compliant outreach |
| Security | Policy Decision Point, RLS, passkeys, JIT admin access, secrets rotation, SAST (Semgrep), dependency and container scanning (Trivy), OWASP ZAP | Fail-closed by design; independent pen tests |
| Quality | pytest, Playwright, k6, axe-core, AI evaluation sets | Automated evidence for every release |
| DevOps | GitHub + Actions CI/CD, infrastructure as code, Sentry, Langfuse, Prometheus/Grafana, status page | Repeatable releases and observability |
| Building with AI | **Claude Code** (Claude Max 20x) as pair-programmer and coding agents; Claude API for headless agents in CI; sandboxed branches | The reason the price is low |

**Hosting choice.** The blueprint's baseline runs entirely on AWS. This quotation recommends **Vercel + Supabase + AWS (Mumbai)**, which reduces the operational work one person must carry. Both keep data in India and support every blueprint control. The client may choose either; the fee is the same. Running costs for both are in §6.2. Adopting Vercel + Supabase would be recorded as a blueprint decision when the contract is signed.

## 5.2 Skill set the builder applies

| Role the builder plays | Share of time | Skills | How AI helps |
|---|---|---|---|
| Solutions architect and security designer | 10% | Multi-tenant SaaS, RLS, policy engines, threat modelling | Drafts ADRs and threat checklists; builder decides |
| Business analyst and product owner proxy | 8% | Requirements, user stories, Gherkin, UAT planning | Refines the 461 drafted stories; builder confirms with client |
| Full-stack engineer (Django, React) | 38% | APIs, workflows, data models, React screens | Coding agents implement against specs and tests; builder reviews every change |
| AI/LLM engineer | 12% | Prompt contracts, RAG, guardrails, evaluations, cost control | Agents draft prompts and eval sets; builder sets thresholds |
| QA and test automation engineer | 14% | Test strategy, automation, performance, accessibility | Agents generate tests and data; builder owns coverage and UAT |
| DevOps / SRE | 8% | CI/CD, IaC, monitoring, backups, DR drills | Agents write pipelines and runbooks; builder approves production changes |
| UX designer | 5% | Information architecture, accessible UI | Agents generate variants from the design system; builder curates |
| Project manager and client liaison | 5% | Planning, reporting, demos | AI drafts status reports and release notes |

# 6. Subscriptions: while building and while using the application

## 6.1 While building (per month, USD list prices; verify)

| Subscription | Purpose | Plan | Per month (USD) | Per month (INR) | Status | Paid by |
|---------------|----------------------------|-----------|--------|----------|------|--------|
| Claude Max 20x (Anthropic) | Claude Code: AI pair-programmer and coding agents for the builder; story/test drafting; reviews | Max 20x, 1 seat | $200 | ₹18,000 | Required | Builder (in fee) |
| Vercel Pro | Hosting and preview deployments for the two React frontends (Website and Admin) on separate projects/origins | Pro, 1 member (includes usage credit) | $20–$40 | ₹1,800–₹3,600 | Required | Client (pass-through) |
| Supabase Pro | Managed PostgreSQL with row-level security, pgvector and storage; staging project during build | Pro org + 1 extra Micro project | $35–$45 | ₹3,150–₹4,050 | Required | Client (pass-through) |
| AWS ap-south-1 (Mumbai) dev/staging | Django API, Celery workers and Valkey for staging; S3 for files and backups | EC2 t4g.small + EBS + S3 | $15–$30 | ₹1,350–₹2,700 | Required | Client (pass-through) |
| GitHub Pro | Private repositories, Actions CI, Dependabot, secret scanning | Pro, 1 user | $4 | ₹360 | Required | Builder (in fee) |
| Figma Professional | UX design, prototypes, design system | 1 full seat | $16–$20 | ₹1,440–₹1,800 | Recommended | Builder (in fee) |
| Google Workspace Business Starter | Business email, documents, meetings with the client | 1 user | $7–$8 | ₹630–₹756 | Recommended | Builder (in fee) |
| BrowserStack Live | Cross-browser and screen-reader checks for WCAG 2.2 AA | 1 parallel | $29–$39 | ₹2,610–₹3,510 | Recommended | Builder (in fee) |
| Sentry | Error tracking for staging | Developer (free) | $0 | ₹0 | Required (free) | Client (pass-through) |
| Langfuse | Tracing and cost of AI agents during development | Hobby (free) or self-hosted | $0 | ₹0 | Required (free) | Client (pass-through) |
| Domain names (≈ 5) | Platform and startup sites | ≈ $12–20 per domain per year | $5–$8 | ₹450–₹720 | Required | Client (pass-through) |
| Open-source toolchain | Playwright, pytest, k6, OWASP ZAP, Trivy, Semgrep, axe-core, Mermaid, draw.io, Bitwarden (free) | Free | $0 | ₹0 | Required (free) | Builder (in fee) |
| **Builder's tools (in the fee)** |  |  | **$256–$271** | **₹23,040–₹24,426** |  |  |
| **Client-owned infrastructure (pass-through)** |  |  | **$75–$123** | **₹6,750–₹11,070** |  |  |
| **Total per month while building** |  |  | **$331–$394** | **₹29,790–₹35,496** |  |  |
| Claude API tokens for coding agents (average per month) | Headless/parallel agents in CI | Pay-as-you-go, capped at $300/month | ≈ $102 | ≈ ₹9,158 | Required | Builder (in fee) |

Over the ≈ 44-month build, the fee includes **₹10.50 L** for the builder's tools and **₹4.05 L** for tokens (§4.2). The client-owned infrastructure is about ₹2.99 L–₹4.90 L over the same period, billed at actuals.

## 6.2 While using the application (pilot, after go-live; per month)

| Subscription / service | Purpose | Billing | Per month (INR) | Per month (USD) | Category |
|------------------|----------------------------|----------|-----------|---------|-------|
| Vercel Pro | Website and Admin frontends, CDN, firewall, preview builds | Subscription + usage | ₹1,800–₹3,600 | $20–$40 | Hosting |
| Supabase Pro + Small compute (production) | PostgreSQL with RLS and pgvector, storage, daily backups (Mumbai region) | Subscription + compute | ₹3,600–₹5,400 | $40–$60 | Database |
| Supabase point-in-time recovery (optional, from growth) | Restore to any second in the last 7 days | Add-on | ₹0–₹9,000 | $0–$100 | Database |
| AWS ap-south-1: Django API, Celery workers, Valkey | EC2 t4g.medium + EBS (or ECS on EC2), S3 files | Usage | ₹2,700–₹4,050 | $30–$45 | Hosting |
| AWS cross-region backup and DR storage | Copies of database dumps and files | Usage | ₹300–₹600 | $3–$7 | Hosting |
| Claude API: production AI inference (Haiku-class + Sonnet-class primary) | The application's AI agents, through the model gateway with hard caps | Pay-as-you-go, hard cap | ₹3,000–₹5,000 | $33–$56 | AI |
| Claude API: maintenance AI (CI review, evaluation judge) | Keeps AI quality checks running | Pay-as-you-go, capped | ₹1,000 | $11 | AI |
| Claude Max 5x (maintainer seat) | Claude Code for maintenance and small changes | Subscription | ₹9,000 | $100 | AI |
| Public search API | Account discovery (≈ 500 fetches/month) | Usage | ₹1,500 | $17 | Providers |
| Extraction compute / overage | Document and page extraction (self-hosted first) | Usage | ₹1,000 | $11 | Providers |
| Amazon SES | Transactional and outreach email (≈ 2,000 sends) | Usage | ₹500 | $6 | Providers |
| WhatsApp Business (Meta Cloud API) | ≈ 1,000 chargeable template messages | Per conversation/template | ₹2,000 | $22 | Providers |
| Integration reserve | Calendar, social or validation pilots when approved | Per approval | ₹1,000 | $11 | Providers |
| Sentry Team (or free tier) | Production error tracking and alerts | Subscription | ₹0–₹2,340 | $0–$26 | Monitoring |
| Uptime and status page | Synthetic checks and public status page | Free tier / low-cost plan | ₹0–₹1,300 | $0–$14 | Monitoring |
| GitHub Pro + Google Workspace | Code, CI and business email for the maintainer | Subscription | ₹990–₹1,116 | $11–$12 | Dev tools |
| Domain names | ≈ 5 domains | Annual, shown per month | ₹450–₹720 | $5–$8 | Domains |
| Advanced A1 feature running additions | Agent observability, signal and experimentation stores, extra jobs (35% of the full advanced additions) | Usage | ₹3,868–₹12,634 | $43–$140 | Advanced |
| **Subtotal** |  |  | **₹32,708–₹61,760** | **$363–$686** |  |
| Contingency 15% |  |  | ₹4,906–₹9,264 |  |  |
| **Total running cost (recommended stack)** |  |  | **₹37,614–₹71,024** | **$418–$789** |  |
| For comparison: blueprint baseline (AWS only) incl. alignment and A1 additions |  |  | ₹29,398–₹53,229 | $327–$591 |  |

**Why the recommended stack's range is higher than the AWS-only baseline.** It includes three things the baseline leaves out:

- the maintainer's Claude Max seat (₹9,000);
- optional point-in-time recovery (up to ₹9,000);
- paid error tracking (up to ₹2,340).

Hosting compared like for like is within a few thousand rupees per month. In exchange, one person no longer has to operate the database, backups and CDN.

**Production AI usage.** The 50 AI agents in scope cost about **₹3,381 per month** at pilot volume, or ≈ ₹4,226 with a 25% overhead (high case ≈ ₹10,242). Hard caps in the gateway (₹3,000 core + ₹2,000 advanced) stop paid calls if a limit is reached, and work then degrades safely.

**As the business grows.** At the growth gate, running costs are about ₹50,000–70,000 per month; at scale, about ₹1.3–1.7 lakh per month. They rise only when measured business results pass the blueprint's scale gates. External SaaS tenants pay for their own usage through their plans.

**Optional or conditional:** Apollo enrichment (≈ ₹10,350/month, only after the scale gate), e-signature (per envelope), payment-gateway fees (≈ 2% of collections), paid advertising (campaign budgets).

# 7. Pass-through costs (not in the fee; billed at actuals)

| Item | Estimate | Why separate |
|---|---|---|
| Independent penetration tests: before Release 1, before Release 2, before A1 go-live | ₹5,50,000 – ₹14,00,000 | Security must be certified by an independent tester |
| Running the application (client-owned accounts) | ₹37,614 – ₹71,024 per month after go-live; less during the build | Client owns production accounts and data |
| External legal counsel (DPDP, children's data, contracts) | As quoted by counsel (indicatively ₹1.5–5 lakh) | Legal advice is outside the builder's scope |
| Business costs (data purchases, advertising, payment-gateway fees) | As used | Not platform build costs |

# 8. Timeline and payment milestones

| Milestone | Indicative month from start | Share | Amount (excl. GST) | Amount (incl. GST) |
|---|---|---|---|---|
| Contract signing (mobilisation) | Month 0 | 10% | ₹7,60,000 | ₹8,96,800 |
| Foundation gate: environments, identity, tenancy, model gateway | Month 3 | 10% | ₹7,60,000 | ₹8,96,800 |
| Release 1 functional complete (UAT start) | Month 12 | 15% | ₹11,40,000 | ₹13,45,200 |
| Release 1 go/no-go passed | Month 15 | 15% | ₹11,40,000 | ₹13,45,200 |
| Release 2 build gate passed | Month 26 | 15% | ₹11,40,000 | ₹13,45,200 |
| 30-day monitored pilot completed | Month 28 | 10% | ₹7,60,000 | ₹8,96,800 |
| Advanced A1 mid-point demo | Month 35 | 10% | ₹7,60,000 | ₹8,96,800 |
| Advanced A1 go-live and acceptance | Month 44 | 15% | ₹11,40,000 | ₹13,45,200 |
| **Total** |  | **100%** | **₹76,00,000** | **₹89,68,000** |

**Important.** One builder needs about 44 months; an AI-assisted team would need about 12–13. If an earlier date matters more than price, the scope can be phased or contract engineers added under a revised quotation. Progress is reported monthly with measured throughput. If measured AI productivity is materially better than assumed, the remaining milestones' dates move earlier at no extra cost.

# 9. Maintenance and support retainer

**₹65,000 + GST per month** from go-live (core and A1 live), renewable yearly; about 10% of the fee per year. It covers:

- bug fixes, security patches and dependency upgrades;
- Claude model-version migrations with re-evaluation;
- monitoring and business-hours incident response;
- quarterly DR drill;
- up to 6 days of small changes per month.

Larger changes are quoted at the day rate.

# 10. Future options (indicative, not part of this quotation)

| Option | Builder's effort (days) | Indicative fee (excl. GST) | Duration |
|---|---|---|---|
| Advanced A2: NBA, deal risk, ABM, intent hub, deal rooms, partners, QBR, semantic layer, NL analytics | 348 | ₹26.68 L | ≈ 17 months |
| Advanced A3 (after the scale gate): conversation intelligence, marketing mix, no-code builder, developer platform | 190 | ₹14.58 L | ≈ 9 months |

# 11. Why the buyer can trust this price

- **Specified before priced.** The scope is defined in a 4,745-page blueprint: 461 user stories, 4,156 test cases, 579 API operations, 80 AI agents and 344 recorded decisions. Nothing is priced on guesswork.
- **Every number is traceable** to the blueprint's effort, the published AI-built factors and list prices, with formulas shown in §4.
- **Cheaper than the alternatives.** It costs about a third less than an AI-assisted team and a little over half the price of a traditional team, for the same scope.
- **Safety does not depend on trust in AI.** Consequential actions always need a person, and policy is rechecked at dispatch. Hard AI cost caps, independent penetration tests and human review of every AI-generated change are all built in.
- **The client owns everything:** code, infrastructure, data, accounts and IP on full payment.
- **Fixed price with milestones tied to evidence.** The client pays as gates are passed, not for time spent.

# 12. Assumptions and terms

1. Scope is the Application Blueprint v1.1 as of 28 Nov 2026; changes are priced by written change request at the day rate.
2. The builder's time is valued at ₹1.25 lakh per month (₹5,682 per day; ₹710 per hour), with 21 productive days per month.
3. AI productivity is the central case of Cost Estimate v1.1 plus 4% for solo working (net 32.8%). These are planning assumptions; measured progress is reported monthly.
4. Claude Sonnet is the primary production model. Subscription and token prices are list prices as of the date; changes above 10% are passed through.
5. The client provides timely approvals, UAT users, provider accounts (AWS, Supabase, Vercel, Anthropic, Meta), and legal confirmations.
6. Build agents work with synthetic data only; no production personal data is shared with them.
7. GST at 18% applies to all fees. Pass-through costs are invoiced at actuals with receipts.

- **Price type:** fixed price for the defined scope.
- **Intellectual property:** transferred to the client on full payment.
- **Warranty:** 60 days after each go-live for defects against acceptance criteria.
- **Confidentiality:** all client data and documents are confidential.
- **Payment terms:** invoices payable within 15 days of milestone acceptance.
- **Validity:** 30 days.

**Acceptance**

| For the client | For the builder |
|---|---|
| Name: ______________________ | Name: ______________________ |
| Signature: __________________ | Signature: __________________ |
| Date: ______________________ | Date: ______________________ |

