"""Single source of truth for the end-to-end cost estimate (INR and USD).

All money values are INR unless the name ends in _usd. Ranges are (low, high); central = midpoint unless stated.
Sources are the approved blueprint figures (Parts 8.4, 9.5, 9.6, 9.7–9.10) and the assumptions listed in ASSUMPTIONS.
"""
from catalogue import load as load_catalogue

AS_OF = "28 Nov 2026"
FX = 90.0                       # ₹ per USD (Part 8.4; verify)
FX_SENS = (85.0, 90.0, 95.0)
HOURS_PER_DAY = 8
DAYS_PER_MONTH = 22
HOURS_PER_MONTH = HOURS_PER_DAY * DAYS_PER_MONTH          # 176
PM_RATE = (100_000, 150_000)                               # loaded ₹ per person-month (BRD §6)
PD_RATE = (PM_RATE[0] / DAYS_PER_MONTH, PM_RATE[1] / DAYS_PER_MONTH)   # 4,545 – 6,818
HR_RATE = (PM_RATE[0] / HOURS_PER_MONTH, PM_RATE[1] / HOURS_PER_MONTH)  # 568 – 852
GST = 0.18
L = 100_000                                                # one lakh


def mid(r):
    return (r[0] + r[1]) / 2


def usd(x):
    return x / FX


# ---------------------------------------------------------------- rate card (per role)
# Loaded in-house/contract rates for India-based delivery, consistent with the BRD §6 band.
# Role differentiation sits inside the band; vendor/onshore alternatives are in SCENARIOS.
RATE_CARD = [
    # role, skills, technology, monthly low, monthly high, used in
    ("Engineering lead / solutions architect (hands-on)", "Architecture, Django/DRF, PostgreSQL RLS, security design, code review", "Python, Django, PostgreSQL, AWS, Terraform", 125_000, 150_000, "Core team (1 of 4)"),
    ("Senior full-stack engineer", "Django/DRF APIs, React/TypeScript, testing", "Python, Django, React, TypeScript, Playwright", 100_000, 150_000, "Core team (1 of 4), contract engineer"),
    ("AI/LLM engineer", "Prompt contracts, RAG, model gateway, evals, guardrails", "Claude API, pgvector, Pydantic, eval harness", 110_000, 150_000, "Core team (1 of 4), advanced A1–A3"),
    ("Backend / DevOps engineer", "Celery, Valkey, outbox, CI/CD, IaC, observability", "Celery, Valkey, AWS ECS/RDS/S3, GitHub Actions, Terraform, Prometheus/Grafana", 100_000, 150_000, "Core team (1 of 4), contract engineer"),
    ("Frontend engineer", "React/TypeScript, design system, WCAG 2.2 AA", "React, TypeScript, Vite, axe-core", 100_000, 140_000, "Contract engineer"),
    ("QA lead / test engineer", "Test strategy, SIT/UAT, automation, AI evaluation", "Playwright, pytest, k6, OWASP ZAP, promptfoo-style evals", 90_000, 135_000, "QA 1.0 FTE from Sprint 3"),
    ("UX/UI designer (contract)", "IA, interaction design, accessibility", "Figma", 90_000, 135_000, "UX contractor"),
    ("Growth / compliance lead (0.5–0.75 FTE)", "DPDP consent, outreach rules, playbooks, UAT", "Admin Command Centre, policy rules", 100_000, 150_000, "Growth/compliance"),
    ("Independent reviewer (architecture/security)", "Design and security review at gates", "Threat modelling, code review", 100_000, 150_000, "Gate reviews"),
    ("Data engineer / data scientist (advanced)", "Semantic layer, feature store, scoring models", "PostgreSQL, dbt-style models, Python ML", 110_000, 150_000, "Advanced A1–A3"),
    ("SRE / security engineer (advanced)", "SLOs, DR drills, zero trust, secrets rotation", "AWS, Prometheus, Vault-style secrets, WebAuthn", 110_000, 150_000, "Advanced A1–A3"),
    ("Product Owner (Founder)", "Backlog, approvals, acceptance", "—", 0, 0, "Internal, not costed"),
]

# ---------------------------------------------------------------- Ledger A (approved, DEC-230): resource plan to Day 208
# (id, item, role, FTE, months, person-months, vendor_low, vendor_high, source)
LEDGER_A = [
    ("A1", "Core engineering team, Day 1–180", "4 engineers (lead/architect, full-stack, AI/LLM, backend/DevOps)", 4.0, 6.0, 24.0, 0, 0, "Part 8.4 §8.4.2.1; DEC-005"),
    ("A2", "Core team extension, Day 181–208", "4 engineers + QA + growth/compliance", 5.0, 0.92, 4.6, 0, 0, "Part 8.4; Part 9.5"),
    ("A3a", "QA uplift to 1.0 FTE from Sprint 3", "QA lead / test engineer", None, None, 2.75, 0, 0, "Part 8.1 §8.1.6.5; DEC-232"),
    ("A3b", "DevOps front-load (Sprint 0–2)", "Backend / DevOps engineer", None, None, 0.60, 0, 0, "Part 8.1 §8.1.6.5"),
    ("A3c", "UX contractor", "UX/UI designer (contract)", None, None, 0.87, 0, 0, "Part 8.1 §8.1.6.5"),
    ("A3d", "Independent reviewer", "Independent reviewer", None, None, 0.55, 0, 0, "Part 8.1 §8.1.6.5"),
    ("A4", "Growth / compliance lead, Day 1–180", "Growth / compliance lead", 0.5, 6.0, 3.0, 0, 0, "Part 8.2 §8.2.7.6"),
    ("A5", "Two contract engineers (Option 2b), Day 43–208", "Senior full-stack / frontend engineers", 2.0, 5.46, 10.92, 0, 0, "DEC-228"),
    ("A6a", "QA extension (source pack)", "QA lead / test engineer", None, None, 0.46, 0, 0, "Part 9.5 §9.5.2.6"),
    ("A6b", "UX extension (source pack)", "UX/UI designer (contract)", None, None, 0.22, 0, 0, "Part 9.5 §9.5.2.6"),
    ("A6c", "Training content: 147 task cards", "Vendor / technical writer (fixed price)", None, None, 0, 66_000, 191_000, "Part 9.5 §9.5.2.6"),
    ("A6d", "Penetration-test scope uplift", "Security vendor (fixed price)", None, None, 0, 100_000, 200_000, "Part 9.5 §9.5.2.6"),
    ("A6e", "Load-test staging windows", "Cloud usage", None, None, 0, 5_000, 21_000, "Part 9.5 §9.5.2.6"),
    ("A7", "External penetration tests (before Release 1 and Release 2)", "Security vendor (2 engagements)", None, None, 0, 300_000, 800_000, "Part 8.2 §8.2.7.4; DEC-126"),
]
MGMT_RESERVE = (394_000, 829_000)   # outside the total (Part 8.4)


def ledger_a_rows():
    rows = []
    for r in LEDGER_A:
        pid, item, role, fte, months, pm, vlo, vhi, src = r
        lo = pm * PM_RATE[0] + vlo
        hi = pm * PM_RATE[1] + vhi
        hrs = pm * HOURS_PER_MONTH
        rows.append(dict(id=pid, item=item, role=role, fte=fte, months=months, pm=pm, hours=hrs,
                         hr_lo=HR_RATE[0] if pm else None, hr_hi=HR_RATE[1] if pm else None,
                         lo=lo, hi=hi, src=src, kind="People" if pm else "External / fixed price"))
    return rows


# ---------------------------------------------------------------- one-time development packages
# (key, name, status, low, central, high, effort pd low/central/high, window, source)
PACKAGES = [
    ("CORE", "Core build to the Release 2 gate (Ledger A)", "Approved (DEC-230)", 5_268_000, 6_838_000, 8_408_000, (532, 722, 921), "Dec 2026 – 2 Jul 2027 (Day 1–208)", "Part 8.4"),
    ("ALN", "Literal alignment to the 38-document pack (CR-ALN-01)", "Approved (DEC-416)", 278_400, 609_100, 1_164_500, (61.25, 107.2, 170.8), "Within Releases 1–2", "Part 9.10 §9.10.10"),
    ("A1", "Advanced release A1 (AI, revenue, platform)", "Approved (DEC-417)", 2_800_000, 4_170_000, 5_540_000, (376, 553, 790), "Aug – Dec 2027", "Part 9.10 §9.10.7"),
    ("PH2", "Phase-2 core continuation (W6 Should/Could, hypercare, expansion pilots)", "Optional, not yet approved", 2_580_000, 3_225_000, 3_870_000, (None, 100, None), "Aug – Dec 2027", "Part 8.4 §8.4.2.4"),
    ("A2", "Advanced release A2", "Proposed; decided at gate G-A1", 3_246_000, 4_456_000, 5_665_000, (353, 518, 733), "Dec 2027 – Mar 2028", "Part 9.10 (A2+A3 split pro rata to effort)"),
    ("A3", "Advanced release A3 (after the scale gate)", "Proposed; decided at gate G-A2", 1_774_000, 2_434_000, 3_095_000, (197, 283, 402), "Apr – Jul 2028", "Part 9.10 (A2+A3 split pro rata to effort)"),
]
# A2+A3 total = 78.2–143.0 L minus A1 28.0–55.4 L = 50.2–87.6 L (central 68.9 L); effort 550/801/1,135 pd.
# Split pro rata to central effort A2 518 : A3 283 (64.67% : 35.33%), from the panels' per-release tables.

# ---------------------------------------------------------------- Ledger B (approved, DEC-231): monthly running, pilot scale
# (line, category, item, billing, low ₹/month, high ₹/month, active from, nature)
LEDGER_B = [
    ("B01", "Cloud", "AWS hosting: production + scheduled staging (ECS on EC2, RDS PostgreSQL, Valkey, S3)", "Usage / 1-year commitment", 5_000, 7_000, "Dec 2026 (Day 1)", "Infrastructure"),
    ("B20", "Cloud", "Cross-region backup and DR storage", "Usage", 300, 600, "Dec 2026", "Infrastructure"),
    ("B21", "Cloud", "CloudFront CDN + AWS WAF", "Fixed per rule + usage", 1_300, 1_800, "Feb 2027 (Day 68)", "Subscription"),
    ("B01+", "Cloud", "Source-pack additions: restore-check sandbox, control/finance worker, drift job, training tenant", "Usage", 200, 1_700, "Release 1", "Infrastructure"),
    ("B02", "AI", "Production AI inference: Claude Haiku-class and Sonnet-class (primary, DEC-418) via the gateway; hard cap", "Pay-as-you-go, hard cap", 3_000, 3_000, "Dec 2026 (Day 15)", "Usage (capped)"),
    ("B23", "AI", "Delivery-team AI: CI review, evaluation judge, fixture generation (Claude API)", "Pay-as-you-go, capped", 1_000, 1_000, "Dec 2026 (Day 15)", "Usage (capped)"),
    ("B03", "Providers", "Public search API (≈ 500 fetches/month)", "Free credits, then usage", 1_500, 1_500, "Jan 2027 (Day 36)", "Usage"),
    ("B04", "Providers", "Extraction compute / overage (self-hosted first)", "Usage", 1_000, 1_000, "Jan 2027 (Day 36)", "Usage"),
    ("B05", "Providers", "Email delivery: Amazon SES (≈ 2,000 sends)", "Usage", 500, 500, "Jan 2027 (Day 56)", "Usage"),
    ("B06", "Providers", "WhatsApp Business: Meta Cloud API (≈ 1,000 chargeable templates)", "Per conversation/template", 2_000, 2_000, "Apr 2027 (Day 113)", "Usage"),
    ("B10", "Providers", "Optional integration reserve (calendar/social/validation pilots)", "Per approval", 1_000, 1_000, "Feb 2027 (Day 82)", "Reserve"),
    ("B07", "Tools", "Monitoring, security and CI (error tracking, CI minutes, paging)", "Subscription / usage", 500, 500, "Dec 2026", "Subscription"),
    ("B07+", "Tools", "Synthetic availability probes, extra CI gates", "Subscription / usage", 0, 1_300, "Release 1", "Subscription"),
]
CONTINGENCY = 0.15
SEATS_B09 = 4_140    # 2 × $20 Claude seats × 1.15 (approved baseline)

# Conditional / optional running lines
LEDGER_B_OPTIONAL = [
    ("B08", "Apollo paid enrichment (OFF until the scale gate) × 1.15", 10_350, 10_350, "Scale gate only"),
    ("B22", "LLM observability, self-hosted Langfuse, at growth", 2_250, 2_700, "Growth gate"),
    ("B13", "E-signature provider (pilot uses signed-PDF path)", 0, 0, "W5/W6, per envelope"),
    ("B14", "Payment gateway fees (pass-through, % of collections)", 0, 0, "Day 140+, per transaction"),
    ("B12", "Paid ads media (per startup campaign budget; not a platform cost)", 0, 0, "W6"),
    ("B15–B19", "Calendar, social APIs, SEO data, contact verification, vector overage (free tiers)", 0, 0, "Off in pilot"),
]

# v1.1 additions to running cost (separately approved per release)
RUN_ADDITIONS = [
    ("CR-ALN-02", "Literal-alignment running additions (self-hosted observability etc.; upper bound after DEC-418)", 1_495, 10_120, "From Release 1", "Approved with DEC-416 (upper bound)"),
    ("B24/X1", "Advanced AI agents: tools, hosting and AI line B24 (capped ₹2,000 in pilot)", 4_544, 10_532, "From A1, ramps to A3", "A1 approved (DEC-417)"),
    ("X2", "Advanced revenue-growth capabilities (open-source first; paid tools off until benchmarked)", 2_148, 6_867, "From A1", "A1 approved (DEC-417)"),
    ("X3", "Advanced platform, data, security and experience (cloud, tools)", 4_359, 18_699, "From A1", "A1 approved (DEC-417)"),
]

SCALE_STAGES = [
    ("Pilot (after Release 2)", "₹5,000–7,000", "₹3,000 cap", (20_000, 26_000), "—"),
    ("Year-1 design point (growth gate)", "≈ ₹21,000", "₹12,000 cap", (50_000, 70_000), "BRD §8 scale gate: cost per qualified opportunity, consent compliance, conversion"),
    ("Year-2 design point (scale)", "≈ ₹66,600", "₹40,000 cap", (130_000, 170_000), "Tenant plans carry attributable cost (NFR-035)"),
]

# ---------------------------------------------------------------- build-time tooling subscriptions (USD list prices, verify)
# (tool, purpose, plan, unit_usd_low, unit_usd_high, seats, required?, during build, after build seats, note)
TOOLS = [
    ("Claude (Anthropic) – coding and drafting assistant", "AI pair-programming (Claude Code), story/test drafting, reviews", "Approved baseline B09: Pro × 2", 20, 20, 2, "Approved (B09)", 2, "Baseline in Ledger B (₹4,140/month incl. 15%)"),
    ("Claude (Anthropic) – recommended full-team upgrade", "Claude Code for all 6 engineers (Max 5x) + Pro for QA, growth lead, PO", "Max 5x × 6 + Pro × 3 (minus baseline 2 × Pro)", 100, 100, 6, "Recommended", 2, "Replaces B09 if adopted: $660/month gross; Team plan with premium seats is an alternative (verify)"),
    ("Claude API (Anthropic Console)", "CI review bots, evaluation judge, fixture generation", "Pay-as-you-go, capped", 11, 11, 1, "Approved (B23)", 1, "≈ ₹1,000/month cap, already in Ledger B"),
    ("GitHub Team", "Source control, pull requests, Actions CI, Dependabot, secret scanning", "Team", 4, 4, 9, "Required", 4, "Actions minutes beyond the included quota in B07"),
    ("Figma Professional", "UX design, prototypes, design system", "Professional full seat", 16, 20, 2, "Required", 1, "Developers use free view seats"),
    ("Jira Software / Confluence", "Backlog, sprints, documentation", "Free (≤ 10 users)", 0, 0, 9, "Required (free tier)", 4, "Standard plan ≈ $8–9/user if > 10 users (verify)"),
    ("Google Workspace Business Starter", "Email, documents, video meetings for the team", "Business Starter", 7, 8.4, 9, "Recommended (if not already owned)", 5, "Use existing company workspace if available"),
    ("Slack Pro (optional)", "Team chat and alert channels", "Pro", 7.25, 8.75, 9, "Optional", 5, "Google Chat inside Workspace is a free alternative"),
    ("Bitwarden Teams", "Shared secrets for the team (not production secrets)", "Teams", 4, 4, 9, "Recommended", 5, "Production secrets stay in AWS Secrets Manager (B01)"),
    ("BrowserStack Live (or LambdaTest)", "Cross-browser and assistive-technology checks for WCAG 2.2 AA", "Live, 1 parallel", 29, 39, 1, "Recommended", 1, "Playwright + axe-core (free) cover automation"),
    ("Postman", "API exploration and contract checks", "Free", 0, 0, 9, "Optional (free)", 4, "Schemathesis/OpenAPI tests are free"),
    ("Domain names", "Platform and startup site domains (≈ 5)", "Annual registration", 1, 2, 5, "Required", 5, "≈ $12–24 per domain per year; shown per month"),
    ("Open-source toolchain", "Playwright, pytest, k6, OWASP ZAP, Trivy, SonarQube Community, axe-core, Mermaid, draw.io, Prometheus, Grafana, Langfuse (self-hosted)", "Free / self-hosted", 0, 0, 1, "Required (free)", 1, "Hosting inside B01"),
]
BUILD_MONTHS_CORE = 8            # Dec 2026 – Jul 2027
BUILD_MONTHS_ADV = 12            # Aug 2027 – Jul 2028 (A1–A3)

# ---------------------------------------------------------------- effort by activity (allocation of programme effort)
ACTIVITY_SPLIT = [
    ("Requirements analysis, backlog and user-story drafting", 0.07, "Product Owner, BA (engineering lead), growth/compliance lead"),
    ("UX/UI design and accessibility", 0.06, "UX designer, frontend engineer"),
    ("Architecture, security and data design", 0.06, "Engineering lead, independent reviewer"),
    ("Backend development (APIs, rules, workflows, data)", 0.27, "Backend and full-stack engineers"),
    ("Frontend development (Website and Admin)", 0.15, "Frontend and full-stack engineers"),
    ("AI engineering (agents, gateway, RAG, evaluations)", 0.10, "AI/LLM engineer"),
    ("Test strategy and test-case drafting", 0.04, "QA lead"),
    ("Test automation and execution (unit, SIT, UAT, performance, security)", 0.11, "QA, engineers"),
    ("DevOps, infrastructure, observability and release", 0.06, "Backend/DevOps engineer"),
    ("Project management, ceremonies and reporting", 0.05, "Engineering lead, PO"),
    ("Documentation, training content and handover", 0.03, "All roles"),
]

# ---------------------------------------------------------------- artefact drafting (bottom-up check)
ARTEFACTS = dict(stories=461, stories_core=230, stories_enh=135, stories_adv=96, test_cases=4156, source_tests=799,
                 ai_eval_cases=774, frs=181 + 180 + 240, screens=147 + 71, apis=579, entities=199, decisions=342)
# hours per unit (low, high) for three ways of working
DRAFTING = [
    ("User stories with Gherkin acceptance criteria", "stories", (2.0, 3.5), (1.0, 1.75), (0.5, 0.9), "BA / PO + engineer review"),
    ("Test cases (functional, NFR, AI evaluation, alignment)", "test_cases", (0.33, 0.5), (0.15, 0.25), (0.08, 0.15), "QA lead"),
    ("Mapping of source-pack tests (unit 75, SIT 422, UAT 302)", "source_tests", (0.1, 0.2), (0.05, 0.1), (0.03, 0.06), "QA lead"),
]
STRATEGY_DOCS = [
    ("Master test strategy", 1, (5, 8)),
    ("Level strategies: unit, SIT, UAT, performance, security, AI evaluation, accessibility, DR", 8, (1.5, 3)),
    ("Release test plans: R1, R2, W6, A1, A2, A3", 6, (1, 2)),
    ("Test data and environment strategy", 1, (2, 4)),
    ("UAT scripts and sign-off packs per startup (AppNAI, MedMaarg, EduVerse, OrganicSpec)", 4, (1, 2)),
]

# ---------------------------------------------------------------- future-proofing and lifecycle (annual, after launch)
FUTURE = [
    ("Maintenance and support (bug fixes, patches, minor changes)", "15–20% of cumulative development cost per year (industry norm, assumption)", None, None, "pct"),
    ("Model migration and AI re-evaluation (new Claude versions, prompt/eval regression)", "2 migrations/year × 5–10 pd", 10, 20, "pd"),
    ("Framework and dependency upgrades (Django LTS, React, PostgreSQL major, Python)", "10–20 pd/year", 10, 20, "pd"),
    ("Annual external penetration test", "1 engagement/year (quote to verify)", 150_000, 400_000, "inr"),
    ("DR drills and chaos game days", "4 per year × 1–2 pd", 4, 8, "pd"),
    ("Accessibility re-audit (WCAG 2.2 AA)", "Annual, external (optional)", 50_000, 150_000, "inr"),
    ("DPDP compliance refresh (DPIA, notices, consent audit)", "Annual legal/compliance review (verify)", 50_000, 200_000, "inr"),
    ("Architecture runway and technical-debt allocation", "15% of enhancement capacity (≈ 0.5 FTE-month per quarter)", 2.0 * DAYS_PER_MONTH, 2.0 * DAYS_PER_MONTH, "pd"),
    ("Documentation and training refresh", "3–5 pd per release × 3 releases/year", 9, 15, "pd"),
    ("FX and price-change buffer on USD subscriptions", "5% of USD-billed subscriptions", None, None, "fx"),
]

# ---------------------------------------------------------------- items often missed
MISSED = [
    ("GST on services and subscriptions", "18% GST on Indian services; reverse charge on imported SaaS (Claude, GitHub, Figma)", "Excluded from estimates; usually creditable for a GST-registered company", "18% of taxable spend (see with-GST view)"),
    ("External legal counsel", "DPDP, children's data (EduVerse), outreach rules, e-sign, contract templates", "Not estimated in the baseline (GAP-174)", "₹1.5–5.0 lakh one-time (market estimate, obtain quotes)"),
    ("Recruitment / agency fee for contract engineers", "If hired through an agency", "Not in baseline", "8–12% of contract value, or ₹0 if direct"),
    ("Laptops and hardware", "Only if the team does not bring its own", "Not in baseline", "₹70,000–1,20,000 per engineer, one-time"),
    ("Cyber insurance", "Liability for data incidents", "Not in baseline", "₹50,000–2,00,000 per year (verify)"),
    ("SOC 2 / ISO 27001 readiness and audit", "Only if enterprise customers require it", "Optional (X3 provides readiness evidence)", "$10,000–30,000 per audit cycle (verify)"),
    ("Bug bounty / vulnerability disclosure", "Public disclosure policy; paid bounty optional", "Optional", "₹0 (VDP) to ₹2 lakh per year"),
    ("Hypercare after Release 2", "30-day monitored pilot and fixes", "Inside Phase 2 / core extension", "Included"),
    ("Knowledge transfer and handover", "If the build team changes", "Inside documentation allocation", "Included"),
    ("Founder / Product Owner time", "Approvals, UAT, backlog", "Internal", "Not costed"),
    ("Paid ad media and data purchases", "Campaign budgets per startup", "Not a platform cost (B12)", "Per campaign"),
    ("Payment gateway fees", "Percentage of collections", "Pass-through (B14)", "≈ 2% of domestic collections (verify)"),
    ("Annual rate escalation", "Salary/contract increases from Year 2", "Applied in the 3-year view", "8% per year (assumption)"),
    ("FX movement on USD subscriptions", "INR/USD changes", "Sensitivity at ₹85 / ₹90 / ₹95", "± 5.6%"),
    ("Data residency or multi-region", "Only if a customer requires a second region", "Not in scope", "≈ +60–90% of hosting (estimate)"),
    ("Customer support tooling", "Helpdesk for external SaaS tenants", "Inside the platform's own support workflow", "Optional third-party: $15–50/agent/month (verify)"),
]

SCOPE_PACKAGES = [
    ("S1", "Core build only (Release 1 + 2)", ["CORE"]),
    ("S2", "Core + literal alignment (approved plan of record)", ["CORE", "ALN"]),
    ("S3", "S2 + advanced A1 (approved)", ["CORE", "ALN", "A1"]),
    ("S4", "S3 + Phase-2 core continuation", ["CORE", "ALN", "A1", "PH2"]),
    ("S5", "S3 + A2 + A3 (full advanced roadmap)", ["CORE", "ALN", "A1", "A2", "A3"]),
    ("S6", "Everything (S5 + Phase 2)", ["CORE", "ALN", "A1", "A2", "A3", "PH2"]),
]
TEAM_MODELS = [
    ("T1", "In-house / direct contract team in India (baseline)", 1.00, "BRD §6 loaded rates; calendar-based cash"),
    ("T2", "Hybrid: core in-house + specialist vendor for advanced work", 1.20, "≈ 20% blended premium for vendor margin and management"),
    ("T3", "Indian IT services vendor (fixed-price/T&M)", 1.45, "Vendor margin 30–50% + PM overhead (assumption)"),
    ("T4", "Global/onshore contractors (USD 45–90/hour)", None, "Effort hours × USD rate + 15% PM overhead; illustrative"),
]
ONSHORE_USD_HR = (45, 90)


def package(key):
    return next(p for p in PACKAGES if p[0] == key)


def effort_pd(keys, point):
    i = {"low": 0, "central": 1, "high": 2}[point]
    tot = 0
    for k in keys:
        e = package(k)[6]
        v = e[i] if e[i] is not None else e[1]
        tot += v
    return tot


def cost(keys, point):
    i = {"low": 3, "central": 4, "high": 5}[point]
    return sum(package(k)[i] for k in keys)


def run_monthly(include_seats=True):
    lo = sum(r[4] for r in LEDGER_B)
    hi = sum(r[5] for r in LEDGER_B)
    lo, hi = lo * (1 + CONTINGENCY), hi * (1 + CONTINGENCY)
    if include_seats:
        lo, hi = lo + SEATS_B09, hi + SEATS_B09
    return lo, hi


def catalogue():
    return load_catalogue(PD_RATE)
