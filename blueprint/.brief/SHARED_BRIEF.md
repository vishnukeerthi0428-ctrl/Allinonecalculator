# Shared brief for blueprint contributors (read fully before writing)

## What you are writing
You are writing one part of a multi-part **enterprise application blueprint** for the product **"AI Growth Engine: Employee Sales & Marketing Automation"**. A development team must be able to plan, build, test, deploy, operate and cost-manage the application from this blueprint with no further clarification. The client asked for output that is **as descriptive and elaborate as possible**. There is no page limit. Match or exceed the depth of the existing parts.

Act as a virtual enterprise team: Product Owner, Business Systems Analyst, Solutions/Technical Architect, Principal Engineer, Lead UX/UI Designer, Data Architect/DBA, QA Lead, Security/Compliance/AI Governance Lead, DevOps/SRE Lead, FinOps Lead. Use category-leading platforms (Workday, Salesforce, Jira, ServiceNow) only as a quality bar. Do not copy proprietary designs.

## Baseline you MUST read first (do not contradict; cite)
Directory: `/home/user/Allinonecalculator/blueprint/`
- `Part-00_Document_Ingestion_and_Validation.md`: requirement inventory, citation convention (§0.1.2: BRD §n / FRD §n numbering), NFR-001…038, epics EP-01…EP-21 (§0.10.2), waves.
- `Part-00A_Issue_Resolution_Decisions.md`: **DEC-001…DEC-065 are binding decisions** (team, AI budget ceilings, model routing tiers, providers, tax, retention, jurisdictions, children, approval thresholds, SLOs, autonomy caps, tenancy model, and more).
- `Part-01_Product_and_Business_Foundation.md`: BR register (BR-M01…M66, BR-TENANT/WEB/AUTO/SVC/QA, BR-S001…S140), personas P01–P16, KPIs KPI-01…31, OKRs, waves W0–W6, MoSCoW, constraints CN-, dependencies DP-.
- `Part-02-1_Functional_Design_Modules_and_FR_Register.md`: capability map, 66-module catalogue (entities and APIs named in the FRD), acceptance profiles CA-*, **FR register** (FR-W01…W34, FR-A001…A113, FR-OP001–003, cross-cutting FRs) with wave and epic per FR.
- `Part-02-2_Functional_Design_Process_Flows.md`: execution engine, WF-01…WF-14, vertical routes, cross-cutting flows.
- `Part-02-3_Business_Rules_RBAC_State_Machines.md`: 162 business rules BRL-<domain>-##, roles R01–R20, ABAC-01…12, state machines.
- `Part-02-4_Cross_Cutting_Functions.md`: notifications NT/NX, reports RP-01…30, search SR-, config CFG-01…32, audit, multi-tenancy, i18n.
- `Part-02-5_UX_UI_Design.md`: IA, 147-screen inventory, design system, WCAG 2.2 AA, UI states.

Source documents (plain-text extraction, for verification only): `/tmp/claude-0/-home-user-Allinonecalculator/233b6551-af93-57f5-8f0b-015057ecee11/scratchpad/docs/brd.txt` and `frd.txt`.

## Product in one paragraph
This is an independently deployed, multi-tenant, configuration-driven commercial growth platform. It serves an Owner Portfolio tenant with 25+ owned startups: AppNAI (global AI project bids), MedMaarg (institutional wellness partnerships, no patient data), EduVerse (education, no direct outreach to minors) and OrganicSpec (agri buy/sell orders with separate receivable and payable ledgers). It also serves independently onboarded external SaaS tenants. It has two React/TypeScript frontends: the public Website/Portal (34 screens, W01–W34) and the confidential Admin Command Centre (113 screens, A001–A113, seven views). The backend is a Django REST Framework modular monolith with PostgreSQL (RLS, pgvector), Celery/Celery Beat, Valkey and S3, deployed on AWS ap-south-1. A transactional outbox and a deterministic Policy Decision Point recheck scope, consent, jurisdiction, budget and approval hash at dispatch. A model gateway applies Tier 0 rules/cache → Tier 1a lighter Claude → Tier 1b Claude Sonnet → Tier 2 free fallbacks (Public/Internal-non-personal data only, opt-in, default off) → Tier 3 degrade. AI drafts, classifies, extracts and matches. It never signs, pays, submits bids or sets prices. Team: 4.0 engineering FTE + 0.5 growth/compliance (DEC-005). Effort: 287–483 person-days (₹13.05–32.93 lakh). Pilot run cost: ₹16,675/month (₹31,165 with optional items). AI ceilings: ₹3,000 / ₹12,000 / ₹40,000 per month (DEC-008). Waves W0 (Day 1–15) … W5 (Day 121–180), W6 (Day 181–365); Release 1 = W0–W3, Release 2 = W4–W5, Future = W6 (DEC-006).

## Non-negotiable writing rules (from the client)
1. **Grounding:** cite sources for every requirement-derived statement: `BRD §n`, `FRD §n`, `DEC-###`, `BR-…`, `FR-…`, `BRL-…`, `NFR-…`.
2. **No silent invention:** tag anything not in the baseline as `[ASSUMPTION-###]`, `[GAP-###]`, `[CONFLICT-###]` or `[RECOMMENDATION-###]`, **using only the number range allocated to you** in your task. Keep a register of the tags you issue at the end of your part.
3. **Verify before stating:** model names, prices, free-tier limits, provider terms, regulatory dates and cloud prices must say "verify at time of implementation (as of 27 Nov 2026)". Never present a guessed price as fact. Cost figures are **estimates** with formulas and assumptions shown.
4. **No filler.** Prefer tables, checklists and structured specs. Every section must be actionable.
5. **Estimates as ranges** with the basis of estimate.
6. **IDs** stay consistent with the baseline: BR-, FR-, NFR-, EP-, US-, AC-, TC-, TS-, AG-, AU-, RSK-, ADR-, DEC-, BRL-, P##, R##, KPI-.
7. Plain, precise language. Define acronyms on first use in your part.

## Formatting conventions (match the existing parts exactly)
- File is Markdown. Start with a title block:
  `# AI Growth Engine: Employee Sales & Marketing Automation`
  `## Application Blueprint: PART X (Batch X.Y), <Title>`
  then a 2-column table (Document, Version `1.0 · 27 Nov 2026`, Baseline, Roles applied).
- Numbered headings continue the part number (Part 3 uses `## 3.1`, `### 3.1.1` …).
- Tables for structured data. Mermaid for diagrams. Gherkin (```gherkin fenced) for acceptance criteria.
- End every file with a **Quality gate** table that has these items: (1) every requirement traced to a source; (2) assumptions/gaps/conflicts tagged and logged; (3) IDs unique and consistent with earlier parts; (4) no story lacks AC and no requirement lacks a test (N/A where not applicable); (5) negative, edge, security and accessibility cases covered; (6) no agent lacks guardrail, fallback, KPI and cost estimate (N/A where not applicable); (7) time-sensitive facts flagged "verify" with an as-of date; (8) no restricted data routed to free-tier models; (9) consistent with earlier parts. Give Pass/Fail per item with notes and fixes applied.
- Then a status line: `**Status: Part X Batch X.Y complete. …**`

## Mermaid rules (the PDF renderer is strict)
- Allowed: `flowchart TD`, `sequenceDiagram`, `stateDiagram-v2`, `erDiagram`. **Do not use C4 syntax**: draw C4 views with `flowchart` and `subgraph`.
- Put node labels in double quotes, e.g. `A["Policy Decision Point"]`. Inside labels avoid double quotes, semicolons and unbalanced brackets. Use `<br/>` for line breaks.
- Never use `end` as a node ID. Keep each diagram ≤ ~25 nodes; split larger ones.
- erDiagram: attribute lines are `type name` with single-token types (e.g. `uuid id PK`, `decimal amount`, `string currency`); keys PK/FK/UK only; relationship labels in double quotes.

## Rendering and self-check (required)
After writing each file run:
```
/home/user/Allinonecalculator/blueprint/make_pdf.sh /home/user/Allinonecalculator/blueprint/<file>.md "Application Blueprint · Part X.Y"
pdftotext /home/user/Allinonecalculator/blueprint/<file>.pdf - | grep -ci "diagram error"
```
The first command prints `(N diagrams)` and writes a WARNING to stderr if a diagram failed. The second must print `0`. Fix and re-render until clean.

## Boundaries
- Write only the files named in your task, inside `/home/user/Allinonecalculator/blueprint/`.
- **Do NOT run git commit or push.** Do not edit any other part's files.
- If you find an inconsistency or error in an earlier part, do not fix it. Report it.

## What to report back (final message, ≤ 300 words)
File names and page counts; a summary of contents with key counts; the tags you issued (by ID); inconsistencies found in earlier parts; anything you could not complete.
