#!/usr/bin/env python3
"""4-month build cost sheet (solo builder with AI agents): Word, PDF and Excel.

Clearly separates (A) one-time build cost, (B) subscriptions needed while building (months 1-4),
and (C) subscriptions and services that continue after building. Includes the full AI catalogue in scope,
automation levels, and the technology for frontend, backend, administration and operations.

Usage: python3 blueprint/estimation/build_cost_sheet_4m.py
"""
import os
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import build_cost_sheet_v11 as S  # noqa: E402
import build_solo_quote_v2 as Q  # noqa: E402
from openpyxl import Workbook  # noqa: E402
from openpyxl.styles import Font  # noqa: E402
from openpyxl.workbook.defined_name import DefinedName  # noqa: E402
from build_xlsx import INP, TOT, NAVY, header, style_rows, title  # noqa: E402

OUT = S.OUT
NAME = "AI_Growth_Engine_Cost_Sheet_4_Month_Build_v1.0"
FX, GST = 90.0, 0.18
inr, usd = Q.inr, Q.usd
MONTHS = 4
PM_RATE = 125_000
PROD_DAYS = 21
TRAD_PD = Q.CORE["trad"] + Q.A1["trad"]              # 1,382 traditional person-days (core + alignment + A1)
USD_PD = Q.USD_PD                                     # ≈ $6.78 per agent-executed person-day
HUMAN_DAYS = MONTHS * PROD_DAYS

# ---------------------------------------------------------------- A. one-time build cost
A_ITEMS = [
    ("A1", "Builder's time: specify, review every AI change, test, release, client demos", f"{MONTHS} months × {inr(PM_RATE)} ({HUMAN_DAYS} days × {inr(PM_RATE / 22)}/day)", MONTHS * PM_RATE),
    ("A2", "Claude API tokens for coding agents: agents execute the implementation work of all 1,382 traditional person-days (parallel, headless)", f"1,382 × ${USD_PD:.2f} × ₹{FX:.0f}", TRAD_PD * USD_PD * FX),
]
CONT = 0.10 * (A_ITEMS[0][3] + A_ITEMS[1][3])
A_ITEMS.append(("A3", "Contingency on time and tokens", "10% × (A1 + A2)", CONT))
A_ITEMS.append(("A4", "Independent security testing: penetration test before go-live + retest after fixes (CERT-In-empanelled vendor)", "Estimate, at actuals (range ₹4–9 lakh)", 650_000))
A_TOTAL = sum(i[3] for i in A_ITEMS)

# ---------------------------------------------------------------- B. subscriptions while building (months 1–4)
B_ITEMS = [  # (id, name, purpose, $ per month, months, paid by)
    ("B1", "Claude Max 20x (Claude Code)", "AI pair-programmer and interactive coding agents for the builder", 200, MONTHS, "Builder"),
    ("B2", "CI runners and agent sandboxes (GitHub larger runners / AWS dev sandboxes)", "Parallel coding agents build and test branches safely", 125, MONTHS, "Builder"),
    ("B3", "GitHub Pro", "Repositories, Actions CI, Dependabot, secret scanning", 4, MONTHS, "Builder"),
    ("B4", "Figma Professional", "UX design, prototypes, design system", 16, MONTHS, "Builder"),
    ("B5", "BrowserStack Live", "Cross-browser and screen-reader checks (WCAG 2.2 AA)", 29, MONTHS, "Builder"),
    ("B6", "Langfuse (agent tracing), Sentry, open-source toolchain", "Tracing, errors, Playwright, pytest, k6, OWASP ZAP, Trivy, Semgrep, axe-core", 0, MONTHS, "Free"),
    ("B7", "Vercel Pro", "Website and Admin frontends: preview and production deployments", 20, MONTHS, "Client"),
    ("B8", "Supabase Pro (Mumbai)", "PostgreSQL with RLS and pgvector, storage, backups (staging then production)", 25, MONTHS, "Client"),
    ("B9", "AWS ap-south-1 small server + S3", "Django API, Celery workers, Valkey for staging", 15, MONTHS, "Client"),
    ("B10", "Domain names (≈ 5)", "Platform and startup sites", 5, MONTHS, "Client"),
]
B_TOTAL = sum(i[3] * i[4] for i in B_ITEMS) * FX

# ---------------------------------------------------------------- C. continue after building (per month; first 12 months)
RUN_LINES = S.RUN_LINES
PIL_LO, PIL_HI, PIL = S.PIL_LO, S.PIL_HI, S.PIL
A1ADD = S.A1ADD
RUN_M = PIL + sum(A1ADD) / 2
RET_M = 55_000
C_ITEMS = [
    ("C1", "Running the application (all lines in §5.2, with 15% contingency, A1 features live)", "Client accounts, at actuals", RUN_M, 12),
    ("C2", "Maintenance and support retainer (includes maintainer's Claude Max 5x seat and GitHub)", "Fixed monthly", RET_M, 12),
]
C_TOTAL = sum(i[3] * i[4] for i in C_ITEMS)
TOTAL = A_TOTAL + B_TOTAL + C_TOTAL

IN = Q.IN
TMAP = {"AG": "AI agent", "AU": "Automation", "WF": "Workflow"}

TECH = [
    ("Website / Portal frontend", "React 18 + TypeScript, Vite, React Router, TanStack Query, design system with CSS variables, i18n-ready; WCAG 2.2 AA; 34 screens (W01–W34) + advanced screens", "Vercel Pro (CDN, firewall, previews)"),
    ("Admin Command Centre frontend", "React + TypeScript, role-based navigation for 7 views, data grids, approval queues, live monitor, policy/budget/tenant admin; 113 screens (A001–A113) + advanced screens (A114–A169)", "Vercel Pro, separate project and origin"),
    ("Backend API", "Python 3.12, Django + Django REST Framework modular monolith; OpenAPI contracts (579 operations); Pydantic validation", "AWS ap-south-1 (EC2/ECS on EC2)"),
    ("Background jobs and scheduling", "Celery + Celery Beat; transactional outbox; idempotent provider adapters", "AWS ap-south-1"),
    ("Cache, queues, rate limits", "Valkey (Redis-compatible)", "AWS ap-south-1"),
    ("Database", "PostgreSQL with row-level security (tenant isolation), pgvector (AI retrieval), audit tables", "Supabase Pro, Mumbai region"),
    ("Files and backups", "Supabase storage / Amazon S3; nightly logical backup and cross-region DR copy", "Supabase + AWS S3"),
    ("Identity and access", "Django identity, MFA and passkeys (WebAuthn), RBAC roles R01–R20, ABAC rules, just-in-time admin elevation; Supabase Auth not used", "Backend"),
    ("Policy and safety", "Policy Decision Point with dispatch-time recheck (scope, consent, jurisdiction, budget, approval hash); emergency stop; autonomy caps (consequential actions ≤ L1)", "Backend"),
    ("AI model gateway", "Claude: Tier 0 rules and cache → Haiku-class → Sonnet-class (primary, DEC-418) → non-personal free fallbacks (off by default) → graceful degradation; hard monthly caps", "Anthropic API via backend"),
    ("AI engineering", "Prompt contracts and registry, pgvector RAG, Pydantic output schemas, evaluation sets, red-team and drift checks, Langfuse tracing", "Backend + Langfuse"),
    ("Messaging", "Amazon SES (email), Meta WhatsApp Cloud API, consent ledger, quiet hours, suppression", "AWS + Meta"),
    ("Search and extraction", "Public search API, self-hosted extraction first", "Providers"),
    ("Administration and operations", "Tenant/startup onboarding, plans and metering, budgets and alerts, audit log, approvals, data-rights (DPDP) workflow, status page and trust centre", "Admin Command Centre + backend"),
    ("Security tooling", "Semgrep (SAST), Trivy (dependencies/containers), OWASP ZAP (DAST), secret scanning, secrets rotation, independent penetration test", "CI + vendor"),
    ("Observability", "Sentry (errors), Prometheus/Grafana or provider metrics, uptime checks, Langfuse (AI)", "Free tiers / self-hosted"),
    ("CI/CD and infrastructure", "GitHub + GitHub Actions, infrastructure as code (Terraform), environment promotion with approvals", "GitHub"),
    ("Testing", "pytest, Playwright (UI), k6 (load), axe-core (accessibility), AI evaluation harness", "CI"),
    ("Building with AI", "Claude Code (Claude Max 20x) interactive and headless agents, Claude API in CI for parallel agents, sandboxed branches, human review of every pull request", "Builder"),
]
SKILLS = [
    ("Solutions architect and security designer", "Multi-tenant SaaS, RLS, policy engines, threat modelling"),
    ("Business analyst / product owner proxy", "User stories, Gherkin acceptance criteria, UAT"),
    ("Full-stack engineer", "Django/DRF APIs and workflows; React/TypeScript screens"),
    ("AI/LLM engineer", "Prompt contracts, RAG, guardrails, evaluations, cost control"),
    ("QA and test automation", "Test strategy, automation, performance, accessibility"),
    ("DevOps / SRE", "CI/CD, IaC, monitoring, backups, DR"),
    ("UX designer", "Information architecture, accessible UI"),
    ("AI-agent orchestrator", "Writing specs for agents, running parallel agents, reviewing and merging their output"),
]

# ---------------------------------------------------------------- markdown
L = []
P = L.append


def table(h, rows, w=None):
    P("| " + " | ".join(h) + " |")
    P("|" + "|".join("-" * max(3, x) for x in (w or [3] * len(h))) + "|")
    for r in rows:
        P("| " + " | ".join(str(c).replace("|", "/") for c in r) + " |")
    P("")


P("# AI Growth Engine: 4-Month Build Cost Sheet")
P("## Core platform + Advanced A1 · solo builder with AI models and AI agents · delivered in 4 months")
P("")
table(["Field", "Value"], [
    ["Prepared for", "[Client name]"], ["Prepared by", "[Your name / company]"],
    ["Version and date", "4-month cost sheet v1.0 · 28 Nov 2026"], ["Validity", "30 days"],
    ["Basis", "Application Blueprint v1.1 (346 decisions; Claude Sonnet primary DEC-418; Vercel + Supabase + AWS Mumbai DEC-421; running budget DEC-422); Final Cost Sheet v1.1"],
    ["Currency", f"INR; GST 18% shown separately; USD items at ₹{FX:.0f} = $1 (verify)"],
])
P("**Important.** The blueprint's estimate for one builder is about 44 months. Delivering in 4 months assumes the AI agents carry out almost all implementation, so the builder needs about 11 times the productivity assumed there. This sheet shows the **cost** of delivering in 4 months. It is not a recommendation that 4 months is achievable, and it is not the price to charge: the value of the same scope is ₹90,00,000 (Final Cost Sheet v1.1).\n")

P("# 1. Summary\n")
table(["Part", "What it covers", "Amount (excl. GST)", "GST 18%", "Amount (incl. GST)"], [
    ["**A. One-time build cost**", "Builder's time, AI coding-agent tokens, contingency, security testing", f"**{inr(A_TOTAL)}**", inr(A_TOTAL * GST), inr(A_TOTAL * (1 + GST))],
    ["**B. Subscriptions while building (months 1–4)**", "Builder's AI and dev tools; client's Vercel, Supabase, AWS, domains", f"**{inr(B_TOTAL)}**", inr(B_TOTAL * GST), inr(B_TOTAL * (1 + GST))],
    ["**C. Subscriptions and services after building (first 12 months)**", "Running the application + maintenance retainer", f"**{inr(C_TOTAL)}**", inr(C_TOTAL * GST), inr(C_TOTAL * (1 + GST))],
    ["**Total (build + first year)**", "", f"**{inr(TOTAL)}**", f"**{inr(TOTAL * GST)}**", f"**{inr(TOTAL * (1 + GST))}**"],
    ["Ongoing after year 1, per month", "Running + retainer", f"{inr(RUN_M + RET_M)}", inr((RUN_M + RET_M) * GST), inr((RUN_M + RET_M) * (1 + GST))],
])

P("# 2. A. One-time build cost\n")
table(["#", "Item", "Basis", "Amount (excl. GST)", "Amount (USD)"], [[i[0], i[1], i[2], inr(i[3]), usd(i[3] / FX)] for i in A_ITEMS] + [["", "**Total A**", "", f"**{inr(A_TOTAL)}**", f"**{usd(A_TOTAL / FX)}**"]])
P(f"**How the 4 months are used.** The builder spends {HUMAN_DAYS} working days writing specifications and acceptance tests, reviewing every AI-generated change, running UAT with the client and releasing. Coding agents do the equivalent of about 1,382 person-days of implementation, drafting and testing in parallel. That is why tokens are the largest build item after time.\n")
P("**Delivery plan:**\n")
table(["Month", "Focus", "Exit"], [
    ["1", "Foundation: environments, identity, tenancy, policy engine, model gateway, design system; Release 1 workflows started", "Foundation gate"],
    ["2", "Release 1 workflows WF-01…WF-10, Website and Admin screens, AI agents and automations for Release 1", "Release 1 UAT start"],
    ["3", "Release 2 workflows WF-11…WF-14, penetration test and fixes, Release 1 + 2 go-live", "Go-live (core)"],
    ["4", "Advanced A1 agents, automations and workflows; retest; A1 go-live; handover", "A1 go-live and acceptance"],
])

P("# 3. B. Subscriptions needed while building (months 1–4)\n")
table(["#", "Subscription", "Purpose", "$ per month", "₹ per month", "Months", "Total (₹)", "Paid by"],
      [[i[0], i[1], i[2], usd(i[3]), inr(i[3] * FX), i[4], inr(i[3] * i[4] * FX), i[5]] for i in B_ITEMS] +
      [["", "**Total B**", "", f"**{usd(sum(i[3] for i in B_ITEMS))}**", f"**{inr(sum(i[3] for i in B_ITEMS) * FX)}**", MONTHS, f"**{inr(B_TOTAL)}**", ""]])
P("The Claude API tokens used by the coding agents are in A2. Client accounts (Vercel, Supabase, AWS, domains) are opened in the client's name from day one, so the client owns its infrastructure and data.\n")

P("# 4. C. Subscriptions and services after building\n")
table(["#", "Item", "Basis", "Per month (excl. GST)", "Months", "First-year total (excl. GST)"],
      [[i[0], i[1], i[2], inr(i[3]), i[4], inr(i[3] * i[4])] for i in C_ITEMS] + [["", "**Total C (first 12 months)**", "", f"**{inr(RUN_M + RET_M)}**", 12, f"**{inr(C_TOTAL)}**"]])

P("# 5. Every subscription after building, line by line\n")
P("## 5.1 Maintenance retainer (C2)\n")
P(f"**{inr(RET_M)} + GST per month.** It covers:\n")
P("- bug fixes, security patches and dependency upgrades;")
P("- Claude model-version migrations with re-evaluation;")
P("- monitoring and business-hours incident response;")
P("- a quarterly DR drill;")
P("- up to 6 days of small changes per month.\n")
P("The maintainer's Claude Max 5x seat and GitHub are included.\n")
P("## 5.2 Running the application (C1; client-owned; per month)\n")
rows = [[r[0], r[2], r[3], f"{inr(r[4])}–{inr(r[5])}" if r[5] != r[4] else inr(r[4]), r[1]] for r in RUN_LINES]
rows.append(["", "**Subtotal**", "", f"**{inr(sum(r[4] for r in RUN_LINES))}–{inr(sum(r[5] for r in RUN_LINES))}**", ""])
rows.append(["B11", "Contingency 15%", "", f"{inr(sum(r[4] for r in RUN_LINES) * 0.15)}–{inr(sum(r[5] for r in RUN_LINES) * 0.15)}", ""])
rows.append(["A1", "Advanced A1 feature running additions", "Usage", f"{inr(A1ADD[0])}–{inr(A1ADD[1])}", "Advanced"])
rows.append(["", "**Running per month (range; central used above)**", "", f"**{inr(PIL_LO + A1ADD[0])}–{inr(PIL_HI + A1ADD[1])}** (central {inr(RUN_M)})", ""])
table(["Line", "Subscription / service", "Billing", "Per month (INR)", "Category"], rows, [6, 52, 16, 16, 10])
ag = [i for i in IN if i["kind"] == "AG"]
P(f"**Production AI usage.** The {len(ag)} AI agents in scope cost about {inr(sum(i['run_base'] for i in ag))} per month at pilot volume. They run on Claude, with Sonnet as the primary model, under hard caps of ₹3,000 core and ₹2,000 advanced per month. **When the business grows:** running is ≈ ₹59,000–79,000 per month at the growth gate and ≈ ₹1.39–1.79 lakh at scale, only after the scale gates pass. **Optional:** Apollo enrichment, e-signature, payment-gateway fees, advertising.\n")

P("# 6. AI agents, automations and workflows in scope\n")
cnt = lambda k, lvl=None: sum(1 for i in IN if i["kind"] == k and (lvl is None or i["level"].startswith(lvl)))
table(["Type", "In scope", "Fully automated", "Mostly automated", "Partially automated", "Assistive only"],
      [[n, cnt(k), cnt(k, "Fully"), cnt(k, "Mostly"), cnt(k, "Partially"), cnt(k, "Assistive")] for k, n in (("AG", "AI agents"), ("AU", "Automations"), ("WF", "Workflows"))]
      + [["**Total**", len(IN), sum(cnt(k, "Fully") for k in TMAP), sum(cnt(k, "Mostly") for k in TMAP), sum(cnt(k, "Partially") for k in TMAP), sum(cnt(k, "Assistive") for k in TMAP)]])
table(["Automation level", "Meaning"], [
    ["Fully automated", "Runs without a person inside policy guardrails; audited"],
    ["Mostly automated", "AI acts; a person reviews afterwards and can reverse"],
    ["Partially automated", "AI or rules prepare; a person approves before anything leaves the system. AI never signs, pays, submits bids or sets prices"],
    ["Assistive only", "AI suggests; a person acts"],
])
for k, n in (("AG", "AI agents"), ("AU", "Automations"), ("WF", "Workflows")):
    P(f"## 6.{list(TMAP).index(k) + 1} {n} ({cnt(k)})\n")
    rows = []
    for i in [x for x in IN if x["kind"] == k]:
        what = i["what"][:220] + ("…" if len(i["what"]) > 220 else "")
        rows.append([i["id"], i["name"], what, i["level"].split(" (")[0], i["autonomy"][:38] if k != "WF" else "Human gates", i["tier"][:28] if k == "AG" else "—", inr(i["run_base"]) if k == "AG" else "In hosting", i["release"]])
    table(["ID", "Name", "What it does", "Automation", "Autonomy", "Model", "AI cost/month", "Release"], rows, [5, 12, 40, 8, 9, 9, 6, 7])

P("# 7. Technology used\n")
table(["Area", "Technology", "Where it runs"], [list(t) for t in TECH], [16, 60, 18])
P("# 8. Skill set applied by the builder\n")
table(["Role", "Skills"], [list(s) for s in SKILLS])

P("# 9. Payment schedule (A, B builder items)\n")
fee = A_TOTAL - 650_000 + sum(i[3] * i[4] for i in B_ITEMS if i[5] == "Builder") * FX
ms = [("Contract signing", 0.20, "Week 0"), ("Foundation gate", 0.20, "End of month 1"), ("Release 1 UAT start", 0.20, "End of month 2"),
      ("Core go-live (Release 1 + 2)", 0.20, "End of month 3"), ("A1 go-live and acceptance", 0.20, "End of month 4")]
table(["Milestone", "When", "Share", "Amount (excl. GST)"], [[m, w, f"{s * 100:.0f}%", inr(fee * s)] for m, s, w in ms] + [["**Total builder invoice**", "", "100%", f"**{inr(fee)}**"]])
P("Penetration testing (A4) and client-owned subscriptions (B7–B10, C1) are paid to the providers at actuals; the retainer (C2) is billed monthly from go-live.\n")

P("# 10. Assumptions\n")
for n, t in enumerate([
    "Scope: Application Blueprint v1.1, Core + Advanced A1. Changes are made by written change request.",
    "The 4-month duration assumes AI agents execute almost all implementation; the blueprint's own solo estimate is about 44 months. If more time is needed, A1 time and B subscriptions rise in proportion.",
    f"Builder's time at {inr(PM_RATE)} per month; token use ≈ ${USD_PD:.2f} per agent-executed person-day, with list prices as of 28 Nov 2026 (verify).",
    "Claude Sonnet primary (DEC-418); Vercel + Supabase + AWS Mumbai (DEC-421); running budget DEC-422.",
    "Excluded: GST (shown separately), external legal counsel, paid data, advertising, payment-gateway fees.",
    "Build agents use synthetic data only. Every AI-generated change gets human review, and AI never takes consequential actions on its own.",
], 1):
    P(f"{n}. {t}")

(OUT / f"{NAME}.md").write_text("\n".join(L) + "\n", encoding="utf-8")


# ---------------------------------------------------------------- Excel
def build_xlsx(path):
    wb = Workbook()
    ws = wb.active
    ws.title = "Summary"
    title(ws, "AI Growth Engine – 4-Month Build Cost Sheet (Core + Advanced A1, solo builder with AI)", "A = one-time build · B = subscriptions while building · C = subscriptions and services after building. Edit yellow cells on 'Inputs'.")
    wi = wb.create_sheet("Inputs")
    title(wi, "Inputs (edit the yellow cells)")
    header(wi, 3, ["Name", "Parameter", "Value"], [14, 60, 16])
    inputs = [("FX", "₹ per USD", FX), ("MONTHS", "Build duration (months)", MONTHS), ("PM_RATE", "Builder's rate per month (₹)", PM_RATE),
              ("TRAD_PD", "Traditional effort executed by agents (person-days)", round(TRAD_PD, 1)), ("USD_PD", "Token cost per agent-executed person-day ($)", round(USD_PD, 3)),
              ("CONT", "Contingency on time and tokens", 0.10), ("PEN", "Penetration test + retest (₹)", 650_000), ("RUN_M", "Running the application per month, central (₹)", round(RUN_M)),
              ("RET_M", "Maintenance retainer per month (₹)", RET_M), ("YEAR_N", "Months after building included", 12), ("GST", "GST rate", GST)]
    for i, (nm, lab, v) in enumerate(inputs, 4):
        wi.cell(row=i, column=1, value=nm)
        wi.cell(row=i, column=2, value=lab)
        c = wi.cell(row=i, column=3, value=v)
        c.fill = INP
        if nm in ("CONT", "GST"):
            c.number_format = "0%"
        wb.defined_names[nm] = DefinedName(nm, attr_text=f"Inputs!$C${i}")
    style_rows(wi, 4, 3 + len(inputs), 3)

    wa = wb.create_sheet("A. Build Cost")
    title(wa, "A. One-time build cost")
    header(wa, 3, ["#", "Item", "Basis", "Amount (₹)", "Amount ($)"], [6, 80, 40, 16, 14])
    fa = ["=MONTHS*PM_RATE", "=TRAD_PD*USD_PD*FX", "=CONT*(D4+D5)", "=PEN"]
    for i, (it, f) in enumerate(zip(A_ITEMS, fa), 4):
        for j, v in enumerate([it[0], it[1], it[2], f, f"=D{i}/FX"], 1):
            wa.cell(row=i, column=j, value=v)
    wa.cell(row=8, column=2, value="Total A").font = Font(bold=True)
    wa["D8"], wa["E8"] = "=SUM(D4:D7)", "=SUM(E4:E7)"
    wa["D8"].fill = wa["E8"].fill = TOT
    style_rows(wa, 4, 8, 5, money_cols=(4,), usd_cols=(5,))

    wb_ = wb.create_sheet("B. While Building")
    title(wb_, "B. Subscriptions needed while building")
    header(wb_, 3, ["#", "Subscription", "Purpose", "$ per month", "₹ per month", "Months", "Total (₹)", "Paid by"], [6, 46, 60, 12, 13, 9, 14, 10])
    for i, it in enumerate(B_ITEMS, 4):
        for j, v in enumerate([it[0], it[1], it[2], it[3], f"=D{i}*FX", "=MONTHS", f"=E{i}*F{i}", it[5]], 1):
            c = wb_.cell(row=i, column=j, value=v)
            if j == 4:
                c.fill = INP
    n = 3 + len(B_ITEMS)
    wb_.cell(row=n + 1, column=2, value="Total B").font = Font(bold=True)
    for col in "DEG":
        wb_[f"{col}{n + 1}"] = f"=SUM({col}4:{col}{n})"
        wb_[f"{col}{n + 1}"].fill = TOT
    style_rows(wb_, 4, n + 1, 8, money_cols=(5, 7), usd_cols=(4,))

    wc = wb.create_sheet("C. After Building")
    title(wc, "C. Subscriptions and services after building")
    header(wc, 3, ["#", "Item", "Basis", "Per month (₹)", "Months", "Total (₹)"], [6, 80, 26, 15, 9, 16])
    for i, (it, f) in enumerate(zip(C_ITEMS, ["=RUN_M", "=RET_M"]), 4):
        for j, v in enumerate([it[0], it[1], it[2], f, "=YEAR_N", f"=D{i}*E{i}"], 1):
            wc.cell(row=i, column=j, value=v)
    wc.cell(row=6, column=2, value="Total C").font = Font(bold=True)
    wc["D6"], wc["F6"] = "=SUM(D4:D5)", "=SUM(F4:F5)"
    wc["D6"].fill = wc["F6"].fill = TOT
    r0 = 8
    wc.cell(row=r0, column=2, value="Running the application, line by line (per month, client-owned)").font = Font(bold=True, color=NAVY)
    header(wc, r0 + 1, ["Line", "Subscription / service", "Billing", "Low (₹)", "High (₹)", "Category"])
    for i, r_ in enumerate(RUN_LINES, r0 + 2):
        for j, v in enumerate([r_[0], r_[2], r_[3], r_[4], r_[5], r_[1]], 1):
            wc.cell(row=i, column=j, value=v)
    k = r0 + 2 + len(RUN_LINES)
    for lab, lo, hi in (("Contingency 15%", f"=SUM(D{r0 + 2}:D{k - 1})*0.15", f"=SUM(E{r0 + 2}:E{k - 1})*0.15"), ("A1 feature running additions", round(A1ADD[0]), round(A1ADD[1]))):
        wc.cell(row=k, column=2, value=lab)
        wc.cell(row=k, column=4, value=lo)
        wc.cell(row=k, column=5, value=hi)
        k += 1
    wc.cell(row=k, column=2, value="Running per month").font = Font(bold=True)
    wc[f"D{k}"], wc[f"E{k}"] = f"=SUM(D{r0 + 2}:D{k - 1})", f"=SUM(E{r0 + 2}:E{k - 1})"
    wc[f"D{k}"].fill = wc[f"E{k}"].fill = TOT
    style_rows(wc, 4, k, 6, money_cols=(4, 5, 6))

    wcat = wb.create_sheet("AI Catalogue")
    title(wcat, f"AI agents, automations and workflows in scope ({len(IN)})")
    header(wcat, 3, ["ID", "Type", "Name", "What it does", "Automation level", "Autonomy", "Model", "AI cost ₹/month", "Release"], [9, 12, 34, 90, 36, 22, 26, 14, 16])
    for i, it in enumerate(IN, 4):
        for j, v in enumerate([it["id"], TMAP[it["kind"]], it["name"], it["what"], it["level"], it["autonomy"] if it["kind"] != "WF" else "Human approval gates",
                               it["tier"] if it["kind"] == "AG" else "—", it["run_base"] if it["kind"] == "AG" else 0, it["release"]], 1):
            wcat.cell(row=i, column=j, value=v)
    n = 3 + len(IN)
    style_rows(wcat, 4, n, 9, money_cols=(8,))
    wcat.auto_filter.ref = f"A3:I{n}"
    r0 = n + 2
    header(wcat, r0, ["Summary", "Count", "", "", "", "", "", "", ""])
    for k_, (lab, f) in enumerate([("AI agents", f'=COUNTIF(B4:B{n},"AI agent")'), ("Automations", f'=COUNTIF(B4:B{n},"Automation")'), ("Workflows", f'=COUNTIF(B4:B{n},"Workflow")'),
                                   ("Fully automated", f'=COUNTIF(E4:E{n},"Fully automated*")'), ("Mostly automated", f'=COUNTIF(E4:E{n},"Mostly automated*")'),
                                   ("Partially automated", f'=COUNTIF(E4:E{n},"Partially automated*")'), ("Assistive only", f'=COUNTIF(E4:E{n},"Assistive only*")'),
                                   ("AI cost per month (base)", f"=SUM(H4:H{n})")], r0 + 1):
        wcat.cell(row=k_, column=1, value=lab)
        wcat.cell(row=k_, column=2, value=f)

    wt = wb.create_sheet("Technology")
    title(wt, "Technology used: frontend, backend, administration, AI, operations")
    header(wt, 3, ["Area", "Technology", "Where it runs"], [30, 110, 34])
    for i, row in enumerate(TECH, 4):
        for j, v in enumerate(row, 1):
            wt.cell(row=i, column=j, value=v)
    style_rows(wt, 4, 3 + len(TECH), 3)
    r0 = 5 + len(TECH)
    header(wt, r0, ["Role the builder plays", "Skills", ""])
    for i, row in enumerate(SKILLS, r0 + 1):
        for j, v in enumerate(row, 1):
            wt.cell(row=i, column=j, value=v)
    style_rows(wt, r0 + 1, r0 + len(SKILLS), 2)

    # summary formulas
    header(ws, 4, ["Part", "Amount excl. GST (₹)", "GST (₹)", "Amount incl. GST (₹)", "Amount excl. GST ($)"], [58, 20, 16, 20, 18])
    parts = [("A. One-time build cost", "='A. Build Cost'!D8"), ("B. Subscriptions while building (months 1–4)", f"='B. While Building'!G{4 + len(B_ITEMS)}"),
             ("C. Subscriptions and services after building (first 12 months)", "='C. After Building'!F6")]
    for i, (lab, f) in enumerate(parts, 5):
        for j, v in enumerate([lab, f, f"=B{i}*GST", f"=B{i}+C{i}", f"=B{i}/FX"], 1):
            ws.cell(row=i, column=j, value=v)
    ws.cell(row=8, column=1, value="Total (build + first year)").font = Font(bold=True)
    for col in "BCDE":
        ws[f"{col}8"] = f"=SUM({col}5:{col}7)"
        ws[f"{col}8"].fill = TOT
    ws.cell(row=9, column=1, value="Ongoing after year 1, per month (running + retainer)")
    ws["B9"] = "='C. After Building'!D6"
    style_rows(ws, 5, 9, 5, money_cols=(2, 3, 4), usd_cols=(5,))
    ws.cell(row=11, column=1, value="Note: the blueprint's solo estimate is ≈ 44 months; 4 months assumes AI agents execute almost all implementation. This is the cost of a 4-month delivery, not the price; value of the scope ₹90,00,000 (Final Cost Sheet v1.1).")
    wb.save(path)


if __name__ == "__main__":
    print(f"A {A_TOTAL:,.0f}  B {B_TOTAL:,.0f}  C {C_TOTAL:,.0f}  TOTAL {TOTAL:,.0f}")
    build_xlsx(OUT / f"{NAME}.xlsx")
    env = {**os.environ, "LANG": "C.UTF-8", "LC_ALL": "C.UTF-8"}
    subprocess.run([str(Q.BP / "make_pdf.sh"), f"{NAME}.md", "4-Month Build Cost Sheet · 28 Nov 2026 · Confidential"], cwd=OUT, check=True, env=env)
    import build_docx
    build_docx.build(OUT / f"{NAME}.md", OUT / f"{NAME}.docx", header="AI Growth Engine — 4-Month Build Cost Sheet    |    Confidential · 28 Nov 2026",
                     title="AI Growth Engine: 4-Month Build Cost Sheet", subtitle="Core + Advanced A1 · solo builder with AI · build cost, subscriptions while building, subscriptions after building (INR)",
                     version="v1.0 · 28 Nov 2026 · Valid for 30 days")
