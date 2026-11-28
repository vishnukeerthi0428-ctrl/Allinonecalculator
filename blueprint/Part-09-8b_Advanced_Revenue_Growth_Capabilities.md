# AI Growth Engine: Employee Sales & Marketing Automation
## Application Blueprint: PART 9 (Batch 9.8), Advanced Revenue Growth Capabilities

| Field | Value |
|---|---|
| Document | Part 9, Batch 8, file **b of b** (§9.8.5–§9.8.17). File a (`Part-09-8a_Advanced_Revenue_Growth_Capabilities.md`) holds the expert panel, opportunity inventory, improvement plan and the 32 feature specifications with rules BRL-ADV-X2-01…44 |
| Version | 1.0 · 27 Nov 2026 |
| Baseline | Parts 0–9.5; Part 7.2 tool registry TL-01…20 and autonomy scale; Part 7.3 cost formula (FX ₹90/USD, BRD §6); Part 8.4 Ledgers A/B (DEC-229…231); Part 9.4 catalogue |
| Roles applied | Expert panel of file a, plus AI Governance Lead (agent cards), QA Lead (tests), FinOps Lead (effort and cost), Security/Compliance Lead (risks, decisions) |
| Status | Separately approvable proposal (DEC-390). Costs in §9.8.13 are **outside** Ledger A (DEC-230), Ledger B (DEC-231) and the Phase-2 envelope |

**Counts in this file.** 10 agents (AG-061…070) · 20 automations (AU-080…099) · 8 workflows (WF-25…32) · 96 functional requirements (FR-ADV-X2-001…096) · 32 user stories · 104 test cases (TC-ADV-X2-001…104) · 20 KPIs (KPI-ADV-X2-01…20) · 10 decisions (DEC-390…399) · 6 ADRs (ADR-120…125) · 12 risks · tags 650–669.

---

## 9.8.5 Agent specification cards (AG-061…AG-070)

**Common to all ten agents.** Pattern per Part 7.2: deterministic code computes every number, eligibility and state; the agent only drafts text, classifies, extracts or explains. All are **Tier 2 ineligible** because they read personal or confidential business data (DEC-007, BRL-ADV-X2-44). TL-13 `dispatch.request` is never granted. Untrusted inputs (notes, verbatims, partner submissions, web content) pass AU-004 redaction and AU-005 sanitization first. Model names: Tier 1a = Claude Haiku-class (currently "Haiku 5.5"), Tier 1b = Claude Sonnet-class (currently "Sonnet 5.5"); **verify model names and prices at time of implementation (as of 27 Nov 2026)**. Cost formula (Part 7.3): per call = FX × b × [(I − S)·p_in + S·(h·p_cr + (1 − h)·p_cw) + O·p_out] ÷ 10⁶ with FX ₹90/USD, b = 0.5 for Batch API runs; Haiku p_in 0.10, p_cr 0.01, p_cw 0.125, p_out 0.50; Sonnet p_in 2, p_cr 0.10, p_cw 2.50, p_out 10 (USD per MTok, the Part 7.4b reference set; verify). Monthly low = 0.3 × base, high = 3 × base, before the 25% overhead allowance [ASSUMPTION-666].

**New tool scopes (extend the Part 7.2 registry; read-only).**

| Tool | Name | Class | Scope rule | Used by |
|---|---|---|---|---|
| TL-X2-01 | `pricebook.read` | R0 | Active approved price-book revision for the caller's startup, currency and region only | AG-066 |
| TL-X2-02 | `health.components.read` | R0 | Health score components and explanation inputs for customers in the caller's scope; prohibited fields never present (BRL-ADV-X2-26) | AG-067 |
| TL-X2-03 | `pipeline.facts.read` | R0 | Deal facts, flags, MAP milestones, activity counts, forecast category history for deals in the caller's scope | AG-064, AG-065 |
| TL-X2-04 | `partner.records.read` | R0 | Partner profile, capability tags, approved registrations; never another partner's records | AG-069 |

#### AG-061 Account Plan and Buying-Committee Mapper

| Field | Specification |
|---|---|
| Type | Agent · Generator (planner/drafter) · scope: Startup |
| Purpose and business outcome | For a target account, drafts the account plan (objectives, whitespace among approved offerings, plays, risks) and proposes buying-committee slots and role hypotheses from permitted evidence, so tier-1 accounts get a reviewed plan within one day instead of a week, and deals become multi-threaded (KPI-ADV-X2-02) |
| Linked BR / FR / US | BR-M13, BR-M18, BR-M21, BR-M23; FR-ADV-X2-001…009; FR-A018, FR-A032; WF-25; US-06-V201, US-06-V202, US-07-V203 |
| Persona | P03 Growth Manager, P03a, P03b (authors); P02 Startup Head (approver of tier-1 plans) |
| Trigger | User action "Draft plan" or "Suggest committee" on A131; event `target_account.tier_set(1)` creates a queued draft request (no auto-run for tiers 2–3) |
| Inputs and data sources | Organization record and evidence (permitted sources only), DEC-011 score components, intent score components, Customer 360 timeline summary, committee template for the vertical, approved offering list with readiness, existing contacts with verification state (no contact details beyond role and verification flag) |
| Tools / APIs (registry §7.2.4) | TL-02 `records.read` (organization, opportunity, committee; caller scope), TL-03 `evidence.read`, TL-20 `offering.match_rank`, TL-01 `knowledge.search` (approved offerings), TL-06 `draft.create` (plan draft, committee suggestions) |
| Outputs | JSON `{objectives[], whitespace[{offering_id, reason, evidence_ids[]}], plays[{type, owner_role, due_in_days}], risks[], committee_suggestions[{slot_code, role_hypothesis, evidence_id, confidence}], open_questions[]}` |
| Autonomy and HITL | **L1.** Owner edits and saves; tier-1 plans need R02 approval of the exact hash; committee suggestions become members only when the owner accepts each one |
| Model tier | 1a with 30% escalation to 1b for tier-1 accounts with > 20 evidence items |
| Tier 2 eligibility · data class | No · Confidential (business strategy; names of roles) |
| Prompt / context strategy | Static system prompt, schema and vertical rules (≈ 1,500 tokens, cached); evidence top-k 8 summaries; Customer 360 pre-summarized; synchronous with streaming |
| Guardrails | Whitespace only from offerings with readiness Approved and Available (BRL-MKT-02); every objective and suggestion cites an evidence ID or record (deterministic citation check); MedMaarg prompts forbid patient or clinical-person roles; EduVerse prompts forbid students and under-18 roles (BRL-ADV-X2-03); no contact details invented; no claims beyond approved claims |
| Failure modes and fallback | Schema failure → 2 repairs → Tier 3: blank plan template with evidence list. Missing citations → suggestion dropped. Budget stop → queued with notice |
| Success KPIs | ≥ 80% of plans approved with ≤ 3 edits; 0 suggestions without citations (sampled weekly); tier-1 plan lead time < 1 business day |
| Eval dimensions | Groundedness, offering-readiness compliance, role-policy compliance (vertical), schema, cost, fallback |
| Tokens, calls, cost | 6,000 in (1,500 cacheable, hit 60%), 1,200 out; 60 calls/month. Haiku per call = 90 × [4,500×0.10 + 1,500×(0.6×0.01 + 0.4×0.125) + 1,200×0.50] ÷ 10⁶ = **₹0.102**; Sonnet per call = 90 × [4,500×2 + 1,500×(0.6×0.10 + 0.4×2.50) + 1,200×10] ÷ 10⁶ = **₹2.033**; blended at e = 30% = **₹0.681**. **Monthly (pilot): low ₹12 · base ₹41 · high ₹123** (before 25% overhead) |
| Dependencies | AU-001, AU-003, AU-004, AU-005, AU-084, AU-085; F01, F02 |
| Release | Release A1 (W6) for committee suggestions; plan drafting Release A2 |

#### AG-062 Signal Fusion "Why-Now" Brief Writer

| Field | Specification |
|---|---|
| Type | Agent · Generator (summarizer) · scope: Startup |
| Purpose and business outcome | Writes a three-sentence "why now" brief for each surging account and for each newly routed hot lead, citing the deterministic intent components (AU-084) and evidence, so sellers act on timing within the SLA (KPI-ADV-X2-03) |
| Linked BR / FR / US | BR-M14, BR-M22; FR-ADV-X2-010…018; WF-25, WF-26; US-05-V204, US-07-V206 |
| Persona | P03 Growth Manager, P05 Marketing Specialist (readers) |
| Trigger | Schedule: nightly batch for accounts whose intent score rose ≥ 15 points in 7 days; event `lead.routed(class=hot)` (synchronous, Haiku only) |
| Inputs and data sources | Intent score components (topic codes, counts, dates, sources), evidence-signal summaries, lead form fields (redacted: no free-text personal data beyond the stated business need), offering topic map |
| Tools / APIs (registry §7.2.4) | TL-12 `metrics.query` (intent components), TL-03 `evidence.read`, TL-06 `draft.create` (brief) |
| Outputs | JSON `{brief, cited_components[], suggested_topic_offering_ids[], confidence_label}` |
| Autonomy and HITL | **L0.** Advisory text shown on A132 and on the routed lead; no task, enrolment or message is created by the agent |
| Model tier | 1a; 10% escalation to 1b when components conflict |
| Tier 2 eligibility · data class | No · Confidential (account engagement linked to identified contacts) |
| Prompt / context strategy | Cached system prompt and examples (≈ 1,000 tokens); input ≤ 2,000 tokens of structured components; nightly via Batch API (b = 0.5) |
| Guardrails | Must not state intent as fact ("visited pricing page 3 times" allowed; "is ready to buy" forbidden); no individual browsing narrative beyond topic level; health-related pages never present (BRL-ADV-X2-05); deterministic check that every number in the brief appears in the inputs |
| Failure modes and fallback | Number mismatch → brief replaced by the component table (Tier 0 template). Schema failure → Tier 3 template |
| Success KPIs | ≥ 90% of sampled briefs rated accurate by sellers; 0 briefs with numbers absent from inputs; surge-to-meeting conversion tracked (RP-ADV-X2-02) |
| Eval dimensions | Numeric faithfulness, overclaim detection, privacy (no individual narrative), schema, cost |
| Tokens, calls, cost | 3,000 in (1,000 cacheable, hit 70%), 400 out; 600 calls/month, batch. Haiku per call = 90 × 0.5 × [2,000×0.10 + 1,000×(0.7×0.01 + 0.3×0.125) + 400×0.50] ÷ 10⁶ = **₹0.020**; Sonnet per call = 90 × 0.5 × [2,000×2 + 1,000×(0.7×0.10 + 0.3×2.50) + 400×10] ÷ 10⁶ = **₹0.397**; blended at e = 10% = **₹0.058**. **Monthly (pilot): low ₹10 · base ₹35 · high ₹104** |
| Dependencies | AU-084, AU-080, AU-001, AU-004 |
| Release | Release A1 (W6) |

#### AG-063 Multichannel Cadence Composer

| Field | Specification |
|---|---|
| Type | Agent · Generator (drafter) · scope: Startup |
| Purpose and business outcome | Proposes cadence structures from approved step templates for an objective and segment, and drafts per-recipient variants of approved templates (email, WhatsApp template variables) plus human-task briefs (LinkedIn research note, call opener from approved talk tracks), so sellers run coordinated, compliant, personalized cadences without writing each step (KPI-ADV-X2-06) |
| Linked BR / FR / US | BR-M25, BR-M28, BR-M31; FR-ADV-X2-025…027, FR-ADV-X2-049…051, FR-ADV-X2-076…078; WF-27, WF-31; US-08-V209, US-16-V217, US-09-V226 |
| Persona | P03, P05 (authors); P03L/P05L (approvers of cadence revisions) |
| Trigger | User action on A136 ("Suggest cadence", "Personalize step"); event `event.attendance_imported` creates post-event drafts for approval |
| Inputs and data sources | Approved templates and talk tracks with claim IDs, recipient role, organization evidence summary, prior conversation summary (redacted), eligibility pre-check result (TL-10), jurisdiction rule summary, locale |
| Tools / APIs (registry §7.2.4) | TL-01 `knowledge.search` (approved templates and talk tracks), TL-09 `claims.lookup`, TL-10 `pdp.check_eligibility` (dry-run), TL-02 `records.read`, TL-06 `draft.create` |
| Outputs | JSON `{cadence_proposal{steps[{channel, template_id, wait_rule}]}, step_drafts[{step_id, variables{}, citations[]}], human_task_briefs[{step_id, brief, talk_track_id}], excluded_channels[{channel, reason_rule_id}]}` |
| Autonomy and HITL | **L1.** Cadence structures need R03L or R05L approval of the revision hash; step drafts are queued for owner approval unless the template is pre-approved and only variables change, in which case the dispatch is the baseline L2 path for approved items (DEC-064) |
| Model tier | 1a; 15% escalation to 1b for multi-language or committee-wide drafts |
| Tier 2 eligibility · data class | No · Confidential (contact names, conversation context) |
| Prompt / context strategy | Cached system prompt with channel rules and examples (≈ 1,200 tokens); retrieval of top-4 approved templates; ≤ 2,300 tokens variable context |
| Guardrails | Never proposes a channel the PDP dry-run excluded; never drafts a LinkedIn message for automated sending (human brief only); call briefs only for eligible call tasks (BRL-ADV-X2-16); no new claims (claims lookup mandatory); MedMaarg: no clinical content, EduVerse: no student-directed content (BRL-ADV-X2-42); AG-012 Claims and Policy Guard checks every customer-facing draft |
| Failure modes and fallback | Claims guard failure → draft held with reasons. Schema failure → Tier 3: template without personalization. Budget stop → human writes variables |
| Success KPIs | ≥ 85% of step drafts approved with ≤ 2 edits; 0 drafts proposing excluded channels; meaningful reply rate per eligible enrolment vs baseline (KPI-ADV-X2-06) |
| Eval dimensions | Claim compliance, channel-rule compliance, personalization accuracy (citations), tone, multilingual quality, schema, cost |
| Tokens, calls, cost | 3,500 in (1,200 cacheable, hit 60%), 700 out; 200 calls/month. Haiku per call = 90 × [2,300×0.10 + 1,200×(0.6×0.01 + 0.4×0.125) + 700×0.50] ÷ 10⁶ = **₹0.058**; Sonnet per call = 90 × [2,300×2 + 1,200×(0.6×0.10 + 0.4×2.50) + 700×10] ÷ 10⁶ = **₹1.158**; blended at e = 15% = **₹0.223**. **Monthly (pilot): low ₹13 · base ₹45 · high ₹134** |
| Dependencies | AU-086, AU-009, AG-012, AU-004, AU-005 |
| Release | Release A1 (W6); post-event drafts Release A3 |

#### AG-064 Pipeline Inspection and Forecast Risk Analyst

| Field | Specification |
|---|---|
| Type | Agent · Classifier and explainer · scope: Startup |
| Purpose and business outcome | For each open deal, turns deterministic facts and AU-088 flags into a short risk note with cited facts and three inspection questions; for the forecast roll-up, explains week-over-week changes. Managers inspect more deals in less time and commit categories carry evidence (KPI-ADV-X2-07, KPI-ADV-X2-08) |
| Linked BR / FR / US | BR-M21, BR-M60; FR-ADV-X2-058…063; WF-29; US-17-V220, US-17-V221 |
| Persona | P03L Sales Lead, P02 Startup Head (readers); P03 owner (responds) |
| Trigger | Schedule: Thursday 18:00 local (before the Friday forecast call), batch; user action "Explain change" on A140 |
| Inputs and data sources | Deal facts (stage, age, amount history, close-date history), flags, MAP milestone states, committee coverage, activity counts, forecast category history; no free-text email bodies |
| Tools / APIs (registry §7.2.4) | TL-X2-03 `pipeline.facts.read`, TL-12 `metrics.query`, TL-06 `draft.create` (risk note) |
| Outputs | JSON `{risk_level_label, drivers[{fact_ref, statement}], inspection_questions[3], change_explanations[]}` |
| Autonomy and HITL | **L0.** Advisory only; cannot change category, stage, amount or date (BRL-ADV-X2-34) |
| Model tier | 1a; 20% escalation to 1b for deals with > 30 history events |
| Tier 2 eligibility · data class | No · Confidential (deal values, names) |
| Prompt / context strategy | Cached system prompt and examples (≈ 1,200 tokens); structured facts ≤ 3,800 tokens; Batch API (b = 0.5) |
| Guardrails | Every driver cites a fact reference (deterministic check); the agent's `risk_level_label` is displayed next to, never instead of, deterministic flags; no prediction stated as fact; no personal judgement about the owner |
| Failure modes and fallback | Citation failure → note suppressed, flags still shown. Schema failure → Tier 3: flags only |
| Success KPIs | ≥ 75% of inspection questions rated useful by R03L (monthly sample); 0 notes without fact citations; forecast accuracy trend (KPI-ADV-X2-07) |
| Eval dimensions | Fact faithfulness, flag consistency, neutrality of language, schema, cost |
| Tokens, calls, cost | 5,000 in (1,200 cacheable, hit 60%), 600 out; 300 calls/month, batch. Haiku per call = 90 × 0.5 × [3,800×0.10 + 1,200×(0.6×0.01 + 0.4×0.125) + 600×0.50] ÷ 10⁶ = **₹0.034**; Sonnet per call = 90 × 0.5 × [3,800×2 + 1,200×(0.6×0.10 + 0.4×2.50) + 600×10] ÷ 10⁶ = **₹0.669**; blended at e = 20% = **₹0.161**. **Monthly (pilot): low ₹14 · base ₹48 · high ₹145** |
| Dependencies | AU-087, AU-088, AU-041 |
| Release | Release A1 (W6) |

#### AG-065 Deal Room and Mutual Action Plan Assistant

| Field | Specification |
|---|---|
| Type | Agent · Generator (drafter) · scope: Startup |
| Purpose and business outcome | Drafts MAP milestones from the proposal scope, RFP checklist (AG-019 output), approved meeting summaries (AG-037) and the vertical MAP template; drafts deal-room welcome text and weekly room updates from approved items, so buyers see one clear path to a decision (KPI-ADV-X2-09) |
| Linked BR / FR / US | BR-M43, BR-M46, BR-WEB; FR-ADV-X2-028…033, FR-ADV-X2-085…087; WF-28; US-19-V210, US-13-V211, US-14-V229 |
| Persona | P03, P06 (authors); P14 buyer stakeholders (see only approved output) |
| Trigger | User action on A138 ("Draft MAP", "Draft update") |
| Inputs and data sources | Opportunity facts, approved proposal sections (hashes), RFP checklist items, approved meeting summaries, MAP template for the vertical, list of approved room items |
| Tools / APIs (registry §7.2.4) | TL-X2-03 `pipeline.facts.read`, TL-14 `document.parse` (approved proposal only), TL-01 `knowledge.search`, TL-06 `draft.create` |
| Outputs | JSON `{milestones[{title, owner_side, suggested_due, source_ref}], room_update_draft, citations[]}` |
| Autonomy and HITL | **L1.** Owner approves each milestone and each update; nothing is visible to guests until approved; buyer confirmation is a separate human step (BRL-ADV-X2-19) |
| Model tier | 1a; 30% escalation to 1b for multi-workstream bids |
| Tier 2 eligibility · data class | No · Confidential |
| Prompt / context strategy | Cached system prompt, schema, MAP templates (≈ 1,200 tokens); ≤ 3,800 tokens context; synchronous |
| Guardrails | No price, discount or legal term in milestones or updates (pattern and number check); all dates proposed, never "agreed"; only approved items referenced; AG-012 checks updates; AppNAI: "submission" milestones always owned by the human bid manager (DEC-053) |
| Failure modes and fallback | Guard failure → draft held with reasons. Schema failure → Tier 3: template milestones |
| Success KPIs | ≥ 80% of MAP drafts approved with ≤ 3 edits; 0 price or legal terms in approved MAPs; MAP on-time milestone rate (KPI-ADV-X2-09) |
| Eval dimensions | Groundedness to approved sources, term-leak detection, date logic, schema, cost |
| Tokens, calls, cost | 5,000 in (1,200 cacheable, hit 60%), 1,000 out; 40 calls/month. Haiku per call = 90 × [3,800×0.10 + 1,200×(0.6×0.01 + 0.4×0.125) + 1,000×0.50] ÷ 10⁶ = **₹0.085**; Sonnet per call = 90 × [3,800×2 + 1,200×(0.6×0.10 + 0.4×2.50) + 1,000×10] ÷ 10⁶ = **₹1.698**; blended at e = 30% = **₹0.569**. **Monthly (pilot): low ₹7 · base ₹23 · high ₹68** |
| Dependencies | AU-090, AU-036, AG-012, AG-019, AG-037 |
| Release | Release A2 (W6); AppNAI bid MAP Release A1 |

#### AG-066 CPQ Bundle Advisor and Guardrail Explainer

| Field | Specification |
|---|---|
| Type | Agent · Matcher and explainer · scope: Startup |
| Purpose and business outcome | Given the stated need and the active price book, suggests up to three approved bundles or line sets with reasons, and explains guardrail results (AU-089) in plain language with the next allowed action, so time-to-quote falls and fewer quotes hit red (KPI-ADV-X2-10). **It never sets, changes or negotiates a price** |
| Linked BR / FR / US | BR-M44; FR-ADV-X2-034…036, FR-ADV-X2-094…096; WF-28; US-13-V212, US-14-V232 |
| Persona | P03, P06, P07 (sellers) |
| Trigger | User action "Suggest bundle" or "Why blocked?" on A067 |
| Inputs and data sources | Need summary (structured), active price-book lines, bundles and option rules, guardrail results with rule IDs; OrganicSpec quantity and unit fields |
| Tools / APIs (registry §7.2.4) | TL-X2-01 `pricebook.read`, TL-20 `offering.match_rank`, TL-06 `draft.create` (suggestion only) |
| Outputs | JSON `{suggestions[{bundle_code or lines[{sku, qty, unit}], reason, rule_checks_expected}], guardrail_explanations[{rule_id, plain_text, allowed_next_action}]}`; **no price fields in the schema** |
| Autonomy and HITL | **L0.** Seller chooses; AU-089 and AU-035 compute prices and totals; approvals per DEC-038 |
| Model tier | 1a; 10% escalation to 1b |
| Tier 2 eligibility · data class | No · Confidential (commercial terms) |
| Prompt / context strategy | Cached system prompt (≈ 1,000 tokens); price-book subset top-20 lines by match (no price values are sent to the model, only SKU, description, units and rules) [RECOMMENDATION-670] |
| Guardrails | Output schema has no price, discount or total fields (structural guardrail); suggestions validated against price-book rules before display; invalid suggestions dropped |
| Failure modes and fallback | Validation failure → suggestion dropped with reason. Schema failure → Tier 3: manual line picker |
| Success KPIs | ≥ 60% of suggestions accepted; median time-to-quote −30% vs baseline; 0 suggestions violating option rules shown to users |
| Eval dimensions | Rule compliance, need fit, explanation accuracy, schema, cost |
| Tokens, calls, cost | 2,500 in (1,000 cacheable, hit 70%), 400 out; 150 calls/month. Haiku per call = 90 × [1,500×0.10 + 1,000×(0.7×0.01 + 0.3×0.125) + 400×0.50] ÷ 10⁶ = **₹0.036**; Sonnet per call = 90 × [1,500×2 + 1,000×(0.7×0.10 + 0.3×2.50) + 400×10] ÷ 10⁶ = **₹0.704**; blended at e = 10% = **₹0.102**. **Monthly (pilot): low ₹5 · base ₹15 · high ₹46** |
| Dependencies | AU-089, AU-035 |
| Release | Release A1 (W6) |

#### AG-067 Customer Health and QBR Narrative Analyst

| Field | Specification |
|---|---|
| Type | Agent · Generator (explainer/drafter) · scope: Startup |
| Purpose and business outcome | Explains deterministic health-score drivers (AU-093) in plain words, drafts the QBR narrative over the AU-094 metric snapshot, and proposes expansion hypotheses limited to approved offerings, so CSMs prepare reviews in an hour instead of a day and catch churn risk early (KPI-ADV-X2-12, KPI-ADV-X2-13) |
| Linked BR / FR / US | BR-M48, BR-M50, BR-M52; FR-ADV-X2-043…051; WF-31; US-16-V215, US-16-V216, US-16-V217 |
| Persona | P03c Customer Success Manager (author); P02 (approver); P14 customer (sees approved pack only) |
| Trigger | Event `health.band_changed` (explanation only); user action "Draft QBR" on A143; schedule: 14 days before QBR due |
| Inputs and data sources | Health components and trend (no prohibited fields), metric snapshot (verified ledgers), milestones, support summary (redacted), NPS/CSAT themes, approved offerings and readiness |
| Tools / APIs (registry §7.2.4) | TL-X2-02 `health.components.read`, TL-12 `metrics.query`, TL-01 `knowledge.search`, TL-09 `claims.lookup`, TL-06 `draft.create` |
| Outputs | JSON `{driver_explanations[], qbr_sections[{section, text, metric_refs[]}], expansion_hypotheses[{offering_id, rationale, evidence_refs[]}], risks[]}` |
| Autonomy and HITL | **L1.** CSM edits; R02 approves the exact pack hash before sharing (BRL-ADV-X2-28); hypotheses become growth cases only by CSM action |
| Model tier | 1a; 30% escalation to 1b for QBR narratives |
| Tier 2 eligibility · data class | No · Confidential (customer commercial data) |
| Prompt / context strategy | Cached system prompt and pack schema (≈ 1,200 tokens); metric snapshot as compact table; synchronous with streaming |
| Guardrails | Every number must match the snapshot (deterministic numeric check); no medical, patient or minors' data in inputs (TL-X2-02 scope) or outputs (AU-004 output scan); expansion only for approved and available offerings; no promises of outcomes; AG-012 checks customer-facing sections |
| Failure modes and fallback | Numeric mismatch → section replaced by metric table. Schema failure → Tier 3: pack with metrics and empty narrative |
| Success KPIs | ≥ 80% of narratives approved with ≤ 3 edits; 0 numeric mismatches in shared packs; QBR preparation time −50% (survey) |
| Eval dimensions | Numeric faithfulness, prohibited-data leakage, claim compliance, usefulness, schema, cost |
| Tokens, calls, cost | 6,000 in (1,200 cacheable, hit 60%), 1,200 out; 40 calls/month. Haiku per call = 90 × [4,800×0.10 + 1,200×(0.6×0.01 + 0.4×0.125) + 1,200×0.50] ÷ 10⁶ = **₹0.103**; Sonnet per call = 90 × [4,800×2 + 1,200×(0.6×0.10 + 0.4×2.50) + 1,200×10] ÷ 10⁶ = **₹2.058**; blended at e = 30% = **₹0.690**. **Monthly (pilot): low ₹8 · base ₹28 · high ₹83** |
| Dependencies | AU-093, AU-094, AG-012, AG-038 |
| Release | Release A1 (explanations) · Release A2 (QBR, expansion) |

#### AG-068 Win/Loss and Voice-of-Customer Insight Synthesizer

| Field | Specification |
|---|---|
| Type | Agent · Classifier and summarizer · scope: Startup |
| Purpose and business outcome | Classifies redacted survey verbatims and win/loss review notes into the theme taxonomy, extracts competitor mentions present in the text, and produces a monthly theme synthesis with counts and example quotes, so product, marketing and sales act on evidence (KPI-ADV-X2-15). Builds on AG-026 loss-reason classification rather than replacing it |
| Linked BR / FR / US | BR-M51, BR-M59; FR-ADV-X2-052…057; WF-32; US-16-V218, US-16-V219 |
| Persona | P03c, P03L, P05L, P02 (readers) |
| Trigger | Event `survey.response_received` and `winloss.review_completed` (batched hourly); schedule: monthly synthesis on the 2nd business day |
| Inputs and data sources | Redacted verbatims (AU-004), structured factors, loss reason (AG-026), theme taxonomy, offering list |
| Tools / APIs (registry §7.2.4) | TL-08 `classification.write` (theme labels with confidence), TL-02 `records.read`, TL-06 `draft.create` (synthesis) |
| Outputs | Per item: `{themes[{code, confidence}], sentiment_label, competitor_mentions[]}`; monthly: `{themes[{code, count, trend, quotes[]}], suggested_actions[]}` |
| Autonomy and HITL | **L0** for labels (reviewable, previous label kept); synthesis is a draft for R02/R05L; actions become insights only by a human |
| Model tier | 1a; 10% escalation to 1b for the monthly synthesis |
| Tier 2 eligibility · data class | No · Confidential (customer opinions; redacted but contextual) |
| Prompt / context strategy | Cached taxonomy and examples (≈ 800 tokens); per-item ≤ 1,200 tokens; Batch API (b = 0.5) |
| Guardrails | Competitor statements are quoted as customer opinion, never as verified comparative claims (BR-M59); quotes only from consented, redacted text; MedMaarg verbatims with any health content are blocked from synthesis by AU-004 and flagged for human review; no theme about individual employees |
| Failure modes and fallback | Low confidence (< 0.6) → "Unclassified" for human labelling. Schema failure → Tier 3 unlabelled |
| Success KPIs | Theme labelling accuracy ≥ 85% on a monthly 50-item sample; 0 health-content quotes in synthesis; insight closure rate (KPI-ADV-X2-15) |
| Eval dimensions | Classification accuracy, competitor-claim handling, privacy leakage, schema, cost |
| Tokens, calls, cost | 2,000 in (800 cacheable, hit 70%), 250 out; 300 calls/month, batch. Haiku per call = 90 × 0.5 × [1,200×0.10 + 800×(0.7×0.01 + 0.3×0.125) + 250×0.50] ÷ 10⁶ = **₹0.013**; Sonnet per call = 90 × 0.5 × [1,200×2 + 800×(0.7×0.10 + 0.3×2.50) + 250×10] ÷ 10⁶ = **₹0.250**; blended at e = 10% = **₹0.036**. **Monthly (pilot): low ₹3 · base ₹11 · high ₹33** |
| Dependencies | AU-004, AU-095, AG-026 |
| Release | Release A2 (W6) |

#### AG-069 Partner Match and Co-sell Brief Assistant

| Field | Specification |
|---|---|
| Type | Agent · Matcher and generator · scope: Startup |
| Purpose and business outcome | Explains the deterministic partner-to-opportunity ranking (capability tags, region, tier, past verified outcomes), and drafts the co-sell brief that an owner may share with an approved partner, containing only fields allowed by BRL-ADV-X2-25. Grows partner-sourced revenue without data leakage (KPI-ADV-X2-11) |
| Linked BR / FR / US | BR-M42, BR-M49; FR-ADV-X2-037…042; WF-30; US-12-V213, US-19-V214 |
| Persona | P03d Partner Manager (R03P), P03 owner |
| Trigger | User action on A141 or A138 ("Find partner", "Draft co-sell brief") |
| Inputs and data sources | Partner profiles (TL-X2-04), opportunity facts (organization, offering line, region, stage band), deterministic ranking scores, approved co-sell field list |
| Tools / APIs (registry §7.2.4) | TL-X2-04 `partner.records.read`, TL-X2-03 `pipeline.facts.read`, TL-06 `draft.create` |
| Outputs | JSON `{ranked_explanations[{partner_id, reasons[]}], cosell_brief{fields{}, narrative}, withheld_fields[]}` |
| Autonomy and HITL | **L1.** Owner and R03P approve the brief hash before a co-sell grant; the agent never contacts partners |
| Model tier | 1a; 20% escalation to 1b |
| Tier 2 eligibility · data class | No · Confidential |
| Prompt / context strategy | Cached system prompt and allowed-field schema (≈ 1,000 tokens); ≤ 2,500 tokens context |
| Guardrails | Output limited to an allowlisted field schema; deterministic diff strips any non-allowlisted value (contact details, internal notes, prices); no partner sees another partner's existence; no ranking based on personal attributes |
| Failure modes and fallback | Allowlist violation → brief rejected. Schema failure → Tier 3: manual brief template |
| Success KPIs | 0 non-allowlisted fields in approved briefs; ≥ 70% of briefs approved with ≤ 2 edits; partner-sourced verified revenue share (KPI-ADV-X2-11) |
| Eval dimensions | Data-minimization compliance, explanation faithfulness, schema, cost |
| Tokens, calls, cost | 3,500 in (1,000 cacheable, hit 60%), 600 out; 60 calls/month. Haiku per call = 90 × [2,500×0.10 + 1,000×(0.6×0.01 + 0.4×0.125) + 600×0.50] ÷ 10⁶ = **₹0.055**; Sonnet per call = 90 × [2,500×2 + 1,000×(0.6×0.10 + 0.4×2.50) + 600×10] ÷ 10⁶ = **₹1.085**; blended at e = 20% = **₹0.261**. **Monthly (pilot): low ₹5 · base ₹16 · high ₹47** |
| Dependencies | AU-091, AU-092, AG-032 |
| Release | Release A2 (W6) |

#### AG-070 Enablement and Playbook Coach

| Field | Specification |
|---|---|
| Type | Agent · Retriever and generator · scope: Startup |
| Purpose and business outcome | In context (account plan, deal room, task workbench, editorial calendar), recommends approved enablement assets, the next play step from the vertical playbook, and short coaching tips derived from approved talk tracks and won-deal patterns, so sellers use approved material consistently (KPI-ADV-X2-18) |
| Linked BR / FR / US | BR-M34; FR-ADV-X2-073…075, FR-ADV-X2-082…084; WF-25, WF-27; US-11-V225, US-11-V228, US-17-V227 |
| Persona | P03, P06, P07, P03c (readers); P05 (editorial briefs) |
| Trigger | Side-panel open on A131, A137, A138, A148; user question in the panel (≤ 20 turns/user/day shared with the Copilot quota) |
| Inputs and data sources | Enablement index (approved, unexpired), playbook template, context object facts (stage, vertical, persona), aggregate usage analytics |
| Tools / APIs (registry §7.2.4) | TL-01 `knowledge.search` (enablement namespace), TL-02 `records.read`, TL-12 `metrics.query` (usage aggregates), TL-06 `draft.create` (brief outline) |
| Outputs | JSON `{recommended_assets[{asset_id, why}], next_play_step, tips[], brief_outline?}` |
| Autonomy and HITL | **L0.** Recommendations only; sharing an asset is a user action subject to BRL-ADV-X2-41 |
| Model tier | 1a; 10% escalation to 1b |
| Tier 2 eligibility · data class | No · Internal-Confidential (deal context) |
| Prompt / context strategy | Cached system prompt (≈ 1,200 tokens); retrieval top-6 assets; semantic cache for repeated questions per startup (cosine ≥ 0.92, AU-001) |
| Guardrails | Recommends only approved, unexpired assets (filter before retrieval); tips cite a talk track or asset; no performance judgement of individuals; no gamification nudges toward activity volume (BRL-ADV-X2-40) |
| Failure modes and fallback | Retrieval empty → "No approved asset found; request content" action. Schema failure → Tier 3 list of top assets by stage |
| Success KPIs | Asset click-through ≥ 30% of recommendations; 0 expired or unapproved assets recommended; usage-to-win association reported (KPI-ADV-X2-18) |
| Eval dimensions | Retrieval relevance, approval-filter compliance, groundedness, schema, cost |
| Tokens, calls, cost | 3,000 in (1,200 cacheable, hit 60%), 500 out; 400 calls/month. Haiku per call = 90 × [1,800×0.10 + 1,200×(0.6×0.01 + 0.4×0.125) + 500×0.50] ÷ 10⁶ = **₹0.045**; Sonnet per call = 90 × [1,800×2 + 1,200×(0.6×0.10 + 0.4×2.50) + 500×10] ÷ 10⁶ = **₹0.888**; blended at e = 10% = **₹0.129**. **Monthly (pilot): low ₹15 · base ₹52 · high ₹155** |
| Dependencies | AU-083, AU-001 |
| Release | Release A2 (W6) |

**AI cost summary (pilot).** Σ base = ₹41 + 35 + 45 + 48 + 23 + 15 + 28 + 11 + 16 + 52 = **₹314** before overhead (low ₹94, high ₹938; component rounding), **≈ ₹390/month with the 25% overhead** (low ₹118, high ₹1,171). This fits inside the DEC-008 pilot AI ceiling of ₹3,000/month alongside the expected baseline spend of ≈ ₹1,150 (Part 8.4), so no ceiling change is requested (DEC-399).

