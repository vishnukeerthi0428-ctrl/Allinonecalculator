#!/usr/bin/env python3
"""Final solo-builder quotation v2.0: Core platform + Advanced A1 together, with full price derivation,
AI catalogue for the quoted scope, subscriptions (build and run), technology and skills.

Usage: python3 blueprint/estimation/build_solo_quote_v2.py
"""
import math
import os
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import ai_model as X  # noqa: E402
import catalogue as C  # noqa: E402
import model as M  # noqa: E402

BP = HERE.parent
OUT = BP / "final" / "estimation"
NAME = "AI_Growth_Engine_Solo_Builder_Quote_v2.0"
FX = 90.0
DAY_RATE = 125_000 / 22               # ₹5,682 per day (₹1.25 lakh per month, senior)
HOUR_RATE = DAY_RATE / 8
PROD_DAYS = 21                        # productive days per month, one person
SOLO_EXTRA = 0.04                     # no team coordination
GST = 0.18
TRAD = {"core": 722 + 107.2, "a1": 553}   # traditional effort pd: core build + literal alignment; advanced A1
USD_PD = X.usd_per_agent_pd()
SH = {n: s for n, s, _ in M.ACTIVITY_SPLIT}
ACC = {a[0]: a for a in X.ACCEL}
OVH_C = sum(o[2] for o in X.OVERHEAD)
AGENT_SHARE = sum(SH[a[0]] * a[4] for a in X.ACCEL)
RED_C = sum(SH[a[0]] * a[2] for a in X.ACCEL)
SAVE = RED_C - OVH_C + SOLO_EXTRA


def ind(n):
    n = round(n)
    s = str(abs(int(n)))
    if len(s) > 3:
        head, tail = s[:-3], s[-3:]
        parts = []
        while len(head) > 2:
            parts.insert(0, head[-2:])
            head = head[:-2]
        if head:
            parts.insert(0, head)
        s = ",".join(parts) + "," + tail
    return ("-" if n < 0 else "") + s


def inr(x):
    return "₹" + ind(x)


def lakh(x):
    return f"₹{x / 100_000:,.2f} L"


def usd(x):
    return f"${x:,.0f}"


# ---------------------------------------------------------------- build-time subscriptions (solo; USD list prices, verify)
# (name, purpose, plan, usd_low, usd_high, required?, category)
BUILD_SUBS = [
    ("Claude Max 20x (Anthropic)", "Claude Code: AI pair-programmer and coding agents for the builder; story/test drafting; reviews", "Max 20x, 1 seat", 200, 200, "Required", "AI"),
    ("Vercel Pro", "Hosting and preview deployments for the two React frontends (Website and Admin) on separate projects/origins", "Pro, 1 member (includes usage credit)", 20, 40, "Required", "Hosting"),
    ("Supabase Pro", "Managed PostgreSQL with row-level security, pgvector and storage; staging project during build", "Pro org + 1 extra Micro project", 35, 45, "Required", "Database"),
    ("AWS ap-south-1 (Mumbai) dev/staging", "Django API, Celery workers and Valkey for staging; S3 for files and backups", "EC2 t4g.small + EBS + S3", 15, 30, "Required", "Hosting"),
    ("GitHub Pro", "Private repositories, Actions CI, Dependabot, secret scanning", "Pro, 1 user", 4, 4, "Required", "Dev tools"),
    ("Figma Professional", "UX design, prototypes, design system", "1 full seat", 16, 20, "Recommended", "Design"),
    ("Google Workspace Business Starter", "Business email, documents, meetings with the client", "1 user", 7, 8.4, "Recommended", "Productivity"),
    ("BrowserStack Live", "Cross-browser and screen-reader checks for WCAG 2.2 AA", "1 parallel", 29, 39, "Recommended", "Testing"),
    ("Sentry", "Error tracking for staging", "Developer (free)", 0, 0, "Required (free)", "Monitoring"),
    ("Langfuse", "Tracing and cost of AI agents during development", "Hobby (free) or self-hosted", 0, 0, "Required (free)", "AI ops"),
    ("Domain names (≈ 5)", "Platform and startup sites", "≈ $12–20 per domain per year", 5, 8, "Required", "Domains"),
    ("Open-source toolchain", "Playwright, pytest, k6, OWASP ZAP, Trivy, Semgrep, axe-core, Mermaid, draw.io, Bitwarden (free)", "Free", 0, 0, "Required (free)", "Dev tools"),
]
CLIENT_OWNED = {"Vercel Pro", "Supabase Pro", "AWS ap-south-1 (Mumbai) dev/staging", "Domain names (≈ 5)", "Sentry", "Langfuse"}
BUILD_LO = sum(r[3] for r in BUILD_SUBS)
BUILD_HI = sum(r[4] for r in BUILD_SUBS)
BTOOLS_LO = sum(r[3] for r in BUILD_SUBS if r[0] not in CLIENT_OWNED)      # builder's own tools, in the fee
BTOOLS_HI = sum(r[4] for r in BUILD_SUBS if r[0] not in CLIENT_OWNED)
BINFRA_LO = BUILD_LO - BTOOLS_LO                                           # client-owned infrastructure, pass-through
BINFRA_HI = BUILD_HI - BTOOLS_HI

# ---------------------------------------------------------------- running subscriptions after go-live (pilot, core + A1 live)
# Recommended solo-optimized stack (Vercel + Supabase + AWS Mumbai for workers). INR per month.
RUN_SOLO = [
    ("Vercel Pro", "Website and Admin frontends, CDN, firewall, preview builds", "Subscription + usage", 20 * FX, 40 * FX, "Hosting"),
    ("Supabase Pro + Small compute (production)", "PostgreSQL with RLS and pgvector, storage, daily backups (Mumbai region)", "Subscription + compute", 40 * FX, 60 * FX, "Database"),
    ("Supabase point-in-time recovery (optional, from growth)", "Restore to any second in the last 7 days", "Add-on", 0, 100 * FX, "Database"),
    ("AWS ap-south-1: Django API, Celery workers, Valkey", "EC2 t4g.medium + EBS (or ECS on EC2), S3 files", "Usage", 30 * FX, 45 * FX, "Hosting"),
    ("AWS cross-region backup and DR storage", "Copies of database dumps and files", "Usage", 300, 600, "Hosting"),
    ("Claude API: production AI inference (Haiku-class + Sonnet-class primary)", "The application's AI agents, through the model gateway with hard caps", "Pay-as-you-go, hard cap", 3_000, 5_000, "AI"),
    ("Claude API: maintenance AI (CI review, evaluation judge)", "Keeps AI quality checks running", "Pay-as-you-go, capped", 1_000, 1_000, "AI"),
    ("Claude Max 5x (maintainer seat)", "Claude Code for maintenance and small changes", "Subscription", 100 * FX, 100 * FX, "AI"),
    ("Public search API", "Account discovery (≈ 500 fetches/month)", "Usage", 1_500, 1_500, "Providers"),
    ("Extraction compute / overage", "Document and page extraction (self-hosted first)", "Usage", 1_000, 1_000, "Providers"),
    ("Amazon SES", "Transactional and outreach email (≈ 2,000 sends)", "Usage", 500, 500, "Providers"),
    ("WhatsApp Business (Meta Cloud API)", "≈ 1,000 chargeable template messages", "Per conversation/template", 2_000, 2_000, "Providers"),
    ("Integration reserve", "Calendar, social or validation pilots when approved", "Per approval", 1_000, 1_000, "Providers"),
    ("Sentry Team (or free tier)", "Production error tracking and alerts", "Subscription", 0, 26 * FX, "Monitoring"),
    ("Uptime and status page", "Synthetic checks and public status page", "Free tier / low-cost plan", 0, 1_300, "Monitoring"),
    ("GitHub Pro + Google Workspace", "Code, CI and business email for the maintainer", "Subscription", 11 * FX, 12.4 * FX, "Dev tools"),
    ("Domain names", "≈ 5 domains", "Annual, shown per month", 5 * FX, 8 * FX, "Domains"),
    ("Advanced A1 feature running additions", "Agent observability, signal and experimentation stores, extra jobs (35% of the full advanced additions)", "Usage", 0.35 * 11_051, 0.35 * 36_098, "Advanced"),
]
RS_LO = sum(r[3] for r in RUN_SOLO)
RS_HI = sum(r[4] for r in RUN_SOLO)
RS_LO_C, RS_HI_C = RS_LO * 1.15, RS_HI * 1.15
# Blueprint baseline (AWS-only) running for comparison
BL_LO = 24_035 + 1_495 + 0.35 * 11_051
BL_HI = 30_475 + 10_120 + 0.35 * 36_098

# ---------------------------------------------------------------- effort and price
def phase(trad):
    pd = trad * (1 - SAVE)
    rows = []
    for a in X.ACCEL:
        t = trad * SH[a[0]]
        rows.append((a[0], t, t * (1 - a[2])))
    for o in X.OVERHEAD:
        rows.append(("Added by AI-built delivery: " + o[0], 0, trad * o[2]))
    raw = sum(r[2] for r in rows)
    scale = pd / raw                       # applies the 4% solo coordination saving across activities
    rows = [(n, t, s * scale) for n, t, s in rows]
    months = pd / PROD_DAYS
    labour = pd * DAY_RATE
    tools = (BTOOLS_LO + BTOOLS_HI) / 2 * months * FX
    tokens = trad * AGENT_SHARE * USD_PD * FX
    cont = 0.15 * (labour + tokens)
    return dict(trad=trad, pd=pd, rows=rows, months=months, labour=labour, tools=tools, tokens=tokens, cont=cont,
                cost=labour + tools + tokens + cont, agent_pd=trad * AGENT_SHARE)


CORE = phase(TRAD["core"])
A1 = phase(TRAD["a1"])
COST = CORE["cost"] + A1["cost"]
QUOTE = math.ceil(COST / 50_000) * 50_000
SEPARATE = 4_900_000 + 3_100_000
RETAINER = 65_000                     # per month, core + A1 live
MONTHS = CORE["months"] + A1["months"]

# ---------------------------------------------------------------- catalogue in scope
CAT = C.load((DAY_RATE, DAY_RATE))
IN = [i for i in CAT if i["rk"] in ("Release 1", "Release 2", "A1")]
OUTS = [i for i in CAT if i not in IN]
ag = [i for i in IN if i["kind"] == "AG"]
ai_run_base = sum(i["run_base"] for i in ag) * 1.25

L = []
A = L.append


def table(h, rows, w=None):
    A("| " + " | ".join(h) + " |")
    A("|" + "|".join("-" * max(3, x) for x in (w or [3] * len(h))) + "|")
    for r in rows:
        A("| " + " | ".join(str(c).replace("|", "/") for c in r) + " |")
    A("")


A("# AI Growth Engine: Final Solo-Builder Quotation")
A("## Core platform + Advanced release A1, built single-handedly with AI models and AI agents · fixed price in INR")
A("")
table(["Field", "Value"], [
    ["Quotation", "AI Growth Engine – Employee Sales & Marketing Automation platform: **Core platform (Releases 1 and 2) + Advanced release A1**"],
    ["Prepared for", "[Client name]"],
    ["Prepared by", "[Your name / company]"],
    ["Version and date", "Final quotation v2.0 · 28 Nov 2026 (supersedes the solo quotation v1.0)"],
    ["Validity", "30 days"],
    ["Basis", "Application Blueprint v1.1 (Parts 0–9.10, 345 decisions incl. DEC-421 hosting stack); Cost Estimates v1.0 (traditional) and v1.1 (AI-built)"],
    ["Currency", f"INR. GST at 18% is added to every fee. USD-billed subscriptions converted at ₹{FX:.0f} = $1 (verify at payment)"],
])

A("# 1. The quotation at a glance\n")
table(["Item", "Excluding GST", "GST 18%", "Including GST", "Basis"], [
    ["**Fixed development fee: Core platform + Advanced A1**", f"**{inr(QUOTE)}**", inr(QUOTE * GST), f"**{inr(QUOTE * (1 + GST))}**", f"Cost-based (§4); ≈ {MONTHS:.0f} months; one builder with AI agents"],
    ["Same scope bought separately (solo quotation v1.0)", inr(SEPARATE), inr(SEPARATE * GST), inr(SEPARATE * (1 + GST)), "Core ₹49,00,000 + A1 ₹31,00,000"],
    ["**Bundle saving**", f"**{inr(SEPARATE - QUOTE)}**", "", f"**{inr((SEPARATE - QUOTE) * (1 + GST))}**", "Fee set at the cost basis rounded up to the next ₹50,000"],
    ["Maintenance and support retainer (after go-live)", f"{inr(RETAINER)} per month", f"{inr(RETAINER * GST)}", f"{inr(RETAINER * (1 + GST))} per month", "§9"],
    ["Pass-through: independent security testing (3 tests)", "₹5,50,000 – ₹14,00,000", "As invoiced", "As invoiced", "At actuals with receipts (§7)"],
    ["Pass-through: client-owned infrastructure while building (Vercel, Supabase, AWS staging, domains)", f"{inr(BINFRA_LO * FX)} – {inr(BINFRA_HI * FX)} per month", "As invoiced", "As invoiced", "§6.1"],
    ["Pass-through: running the application after go-live", f"{inr(RS_LO_C)} – {inr(RS_HI_C)} per month", "As invoiced", "As invoiced", "§6.2 (with 15% contingency)"],
])
A(f"**Who pays for which subscription while building.**\n")
A(f"- **In the fee:** the builder's own tools for the whole build, {lakh(CORE['tools'] + A1['tools'])} (§4). These are Claude Max 20x, GitHub, Figma, BrowserStack and Workspace.")
A("- **Paid by the client:** Vercel, Supabase, AWS and the domains. These are opened in the client's own name from day one, so the client owns its infrastructure and data from the start.\n")
A(f"**Why this price is fair.** A traditional team would charge about **₹1.16 crore**, and an AI-assisted team about **₹85 lakh**, for the same scope (Cost Estimates v1.0 and v1.1, central). This quotation is **{inr(QUOTE)}**. The client pays only for the effort that remains after AI agents do most of the drafting, coding and testing. The trade-off is time: about {MONTHS:.0f} months, against about 12–13 months for a team.\n")

A("# 2. What the client receives\n")
A("## 2.1 Core platform (Releases 1 and 2)\n")
for s in [
    "Public Website/Portal (34 screens) and confidential Admin Command Centre (113 screens) as separate React/TypeScript applications on separate origins.",
    "Multi-tenant platform: Owner Portfolio tenant with AppNAI, MedMaarg, EduVerse and OrganicSpec, plus onboarding of external SaaS tenants with plans and metering.",
    "Business workflows WF-01 to WF-14: product catalogue, discovery, outreach under consent, inbound handling, qualification, meetings, bids, proposals and quotes, orders, verified close, onboarding, plans and offboarding.",
    "Policy Decision Point with dispatch-time recheck of scope, consent, jurisdiction, budget and approval; transactional outbox; audit trail; emergency stop.",
    "Model gateway with Claude Sonnet as the primary model (DEC-418): rules and cache first, then Haiku-class, then Sonnet-class, then non-personal free fallbacks (off by default), then graceful degradation; hard monthly caps.",
    "100% literal alignment work with the 38-document specification (99.97% literal match; the three remaining items follow the approved Claude-primary and Vercel + Supabase decisions, DEC-418 and DEC-421).",
]:
    A(f"- {s}")
A("\n## 2.2 Advanced release A1\n")
for s in [
    "AI: agent supervisor/planner, account research, predictive score explanations (advisory), RFP response co-pilot, knowledge freshness, agent red-team and drift checks, data-quality steward, prompt/agent registry with canary rollout.",
    "Revenue growth: pipeline inspection and forecast risk, lead-to-account routing with speed-to-lead SLAs, multichannel cadences under consent (LinkedIn and calls as human tasks), CPQ guardrails inside approved price books, buying-committee suggestions, customer-health explanations.",
    "Platform: AI observability, disaster-recovery drills, passkeys, just-in-time admin access, secrets rotation, supply-chain checks, FinOps insights, automated DPDP data-rights workflow, status page and trust centre.",
]:
    A(f"- {s}")
A("\n## 2.3 Deliverables with every release\n")
A("Source code and infrastructure code in the client's repository, automated tests (unit, API, UI), AI evaluation sets, release evidence packs, runbooks, training task cards, architecture decision records, and a handover session.\n")
A("## 2.4 Not included\n")
A("Advanced releases A2 and A3 (indicative prices in §10), Phase-2 (W6) Should/Could items, paid data and advertising, legal advice, and third-party fees listed in §7.\n")

A("# 3. AI agents, automations and workflows in the quoted scope\n")
lv = {}
for i in IN:
    k = (i["kind"], i["level"].split(" (")[0])
    lv[k] = lv.get(k, 0) + 1
rows = []
for kind, nm in (("AG", "AI agents"), ("AU", "Automations"), ("WF", "Business workflows")):
    s = [i for i in IN if i["kind"] == kind]
    full = sum(1 for i in s if i["level"].startswith("Fully"))
    mostly = sum(1 for i in s if i["level"].startswith("Mostly"))
    part = sum(1 for i in s if i["level"].startswith("Partially"))
    assist = sum(1 for i in s if i["level"].startswith("Assistive"))
    rows.append([nm, len(s), full, mostly, part, assist, f"{inr(sum(i['run_base'] for i in s))}/month" if kind == "AG" else "Inside hosting"])
rows.append(["**Total in scope**", f"**{len(IN)}**", f"**{sum(r[2] for r in rows)}**", f"**{sum(r[3] for r in rows)}**", f"**{sum(r[4] for r in rows)}**", f"**{sum(r[5] for r in rows)}**", f"**≈ {inr(ai_run_base)}/month incl. 25% overhead**"])
table(["Type", "In scope", "Fully automated", "Mostly automated", "Partially automated", "Assistive only", "AI run cost (pilot)"], rows)
table(["Automation level", "Meaning"], [
    ["Fully automated", "Runs without a person inside policy guardrails. Deterministic automations, and AI agents acting only on low-risk internal items (L3), are always audited"],
    ["Mostly automated", "AI acts and a person reviews afterwards and can reverse (L2)"],
    ["Partially automated", "AI or rules prepare; a person approves before anything leaves the system (L1). All consequential actions (quotes, discounts, contracts, bids, payments) are here or manual: **AI never signs, pays, submits bids or sets prices**"],
    ["Assistive only", "AI suggests; a person acts (L0)"],
])
A(f"Outside the quoted scope (future options): {sum(1 for i in OUTS if i['kind'] == 'AG')} agents, {sum(1 for i in OUTS if i['kind'] == 'AU')} automations and {sum(1 for i in OUTS if i['kind'] == 'WF')} workflows in A2, A3 and Phase 2.\n")
for kind, nm in (("AG", "AI agents"), ("AU", "Automations"), ("WF", "Business workflows")):
    A(f"## 3.{['AG', 'AU', 'WF'].index(kind) + 1} {nm} included ({sum(1 for i in IN if i['kind'] == kind)})\n")
    rows = []
    for i in [x for x in IN if x["kind"] == kind]:
        what = i["what"][:230] + ("…" if len(i["what"]) > 230 else "")
        rows.append([i["id"], i["name"], what, i["level"].split(" (")[0], i["autonomy"][:40] if kind != "WF" else "Human gates", i["tier"][:30] if kind == "AG" else "—",
                     inr(i["run_base"]) if kind == "AG" else "In hosting", i["release"]])
    table(["ID", "Name", "What it does", "Automation", "Autonomy", "Model", "AI cost/month", "Release"], rows, [5, 12, 40, 8, 9, 9, 6, 7])

A("# 4. How the price is arrived at\n")
A("## 4.1 Method\n")
for s in [
    f"Start from the **traditional effort** in the blueprint: core build + literal alignment = {TRAD['core']:,.0f} person-days; Advanced A1 = {TRAD['a1']:,.0f} person-days.",
    f"Apply the **AI-built reduction for each activity** (Cost Estimate v1.1, central case). AI agents draft and code; the builder specifies, reviews, tests and releases. Weighted reduction **{RED_C * 100:.1f}%**.",
    f"Add back the **new work AI creates**: agent specs and prompts, human review of every AI change, security and licence review, rework. That adds **{OVH_C * 100:.1f}%**.",
    f"Subtract the **solo coordination saving** (no team meetings or hand-offs): **{SOLO_EXTRA * 100:.0f}%**. Net saving **{SAVE * 100:.1f}%**.",
    f"Value the builder's remaining days at **{inr(DAY_RATE)} per day** ({inr(HOUR_RATE)} per hour; ₹1.25 lakh per month, senior rate within the blueprint band of ₹1.0–1.5 lakh).",
    f"Add the **builder's tools** for the build duration (§6.1; client-owned infrastructure is billed separately), **Claude API tokens** for the coding agents ({AGENT_SHARE * 100:.0f}% of the work executed by agents at ≈ ${USD_PD:.2f} per agent-day), and **15% contingency** on time and tokens.",
    "Round up to the next ₹50,000. No further margin: the builder's income is the day rate.",
]:
    A(f"- {s}")
A("")
A("## 4.2 Price build-up\n")
table(["Component", "Core platform", "Advanced A1", "Total", "Formula"], [
    ["Traditional effort (person-days)", f"{CORE['trad']:,.0f}", f"{A1['trad']:,.0f}", f"{CORE['trad'] + A1['trad']:,.0f}", "Blueprint (Parts 8.4, 9.10)"],
    ["Builder's effort with AI (person-days)", f"{CORE['pd']:,.0f}", f"{A1['pd']:,.0f}", f"{CORE['pd'] + A1['pd']:,.0f}", f"Traditional × (1 − {SAVE:.3f})"],
    ["Builder's hours", f"{CORE['pd'] * 8:,.0f}", f"{A1['pd'] * 8:,.0f}", f"{(CORE['pd'] + A1['pd']) * 8:,.0f}", "Days × 8"],
    ["Duration (months)", f"{CORE['months']:.1f}", f"{A1['months']:.1f}", f"{MONTHS:.1f}", f"Days ÷ {PROD_DAYS} productive days"],
    ["Builder's time", lakh(CORE["labour"]), lakh(A1["labour"]), lakh(CORE["labour"] + A1["labour"]), f"Days × {inr(DAY_RATE)}"],
    ["Builder's tools (Claude Max 20x, GitHub, Figma, BrowserStack, Workspace)", lakh(CORE["tools"]), lakh(A1["tools"]), lakh(CORE["tools"] + A1["tools"]), f"≈ ${(BTOOLS_LO + BTOOLS_HI) / 2:,.0f} per month × months × ₹{FX:.0f}"],
    ["Claude API tokens for coding agents", lakh(CORE["tokens"]), lakh(A1["tokens"]), lakh(CORE["tokens"] + A1["tokens"]), f"Agent-days ({CORE['agent_pd']:,.0f} + {A1['agent_pd']:,.0f}) × ${USD_PD:.2f} × ₹{FX:.0f}"],
    ["Contingency", lakh(CORE["cont"]), lakh(A1["cont"]), lakh(CORE["cont"] + A1["cont"]), "15% × (time + tokens)"],
    ["**Cost basis**", f"**{lakh(CORE['cost'])}**", f"**{lakh(A1['cost'])}**", f"**{lakh(COST)}**", ""],
    ["**Quoted fixed fee**", "", "", f"**{lakh(QUOTE)}**", "Rounded up to the next ₹50,000"],
])
A("## 4.3 Effort by activity (builder's days)\n")
rows = []
for (n, t, s), (n2, t2, s2) in zip(CORE["rows"], A1["rows"]):
    rows.append([n, f"{t:,.0f}" if t else "—", f"{s:,.0f}", f"{t2:,.0f}" if t2 else "—", f"{s2:,.0f}", f"{s + s2:,.0f}", lakh((s + s2) * DAY_RATE)])
rows.append(["**Total**", f"**{CORE['trad']:,.0f}**", f"**{CORE['pd']:,.0f}**", f"**{A1['trad']:,.0f}**", f"**{A1['pd']:,.0f}**", f"**{CORE['pd'] + A1['pd']:,.0f}**", f"**{lakh((CORE['pd'] + A1['pd']) * DAY_RATE)}**"])
table(["Activity", "Core: traditional pd", "Core: solo with AI pd", "A1: traditional pd", "A1: solo with AI pd", "Total solo pd", "Value"], rows, [30, 7, 7, 7, 7, 7, 8])
A("Activities include user-story drafting, test strategy and test-case drafting. The blueprint already contains drafts of all 461 stories and 4,156 test cases, and the builder refines them with AI assistance.\n")
A("## 4.4 How AI agents do the work, and what the builder still does\n")
table(["Activity", "AI reduction", "What the AI agents do", "What the builder does"], [[a[0], f"{a[2] * 100:.0f}%", a[5], a[6].replace("PO", "client").replace("Engineers", "Builder").replace("engineer", "builder")] for a in X.ACCEL], [22, 6, 36, 36])

A("# 5. Technology and skill set\n")
A("## 5.1 Technology stack\n")
table(["Layer", "Technology", "Why"], [
    ["Frontends", "React + TypeScript (Vite), design system, WCAG 2.2 AA; hosted on **Vercel** (two projects, separate origins)", "Fast, accessible UIs; preview deployments for client review"],
    ["Backend", "Python, **Django REST Framework** modular monolith; Celery + Celery Beat; **Valkey**", "Mature, secure, productive; background jobs and schedules"],
    ["Database", "**PostgreSQL on Supabase** (Mumbai): row-level security for tenant isolation, **pgvector** for AI retrieval, storage", "Managed backups, scaling and security; India data residency"],
    ["Compute and files", "**AWS ap-south-1 (Mumbai)**: EC2/ECS for API and workers, S3 for files and DR copies, SES for email", "Data stays in India; low cost at pilot scale"],
    ["AI", "**Claude** via the model gateway: Haiku-class and **Sonnet-class (primary, DEC-418)**; Pydantic schemas; prompt registry; evaluation harness", "High-quality drafting and extraction with hard cost caps and human approval"],
    ["Messaging", "Meta WhatsApp Cloud API, Amazon SES, consent and quiet-hour rules", "Compliant outreach"],
    ["Security", "Policy Decision Point, RLS, passkeys, JIT admin access, secrets rotation, SAST (Semgrep), dependency and container scanning (Trivy), OWASP ZAP", "Fail-closed by design; independent pen tests"],
    ["Quality", "pytest, Playwright, k6, axe-core, AI evaluation sets", "Automated evidence for every release"],
    ["DevOps", "GitHub + Actions CI/CD, infrastructure as code, Sentry, Langfuse, Prometheus/Grafana, status page", "Repeatable releases and observability"],
    ["Building with AI", "**Claude Code** (Claude Max 20x) as pair-programmer and coding agents; Claude API for headless agents in CI; sandboxed branches", "The reason the price is low"],
])
A("**Hosting choice.** The blueprint's baseline runs entirely on AWS. This quotation recommends **Vercel + Supabase + AWS (Mumbai)**, which reduces the operational work one person must carry. Both keep data in India and support every blueprint control. **This stack is approved and recorded in the blueprint as DEC-421 (28 Nov 2026).** Both stacks keep data in India and support every blueprint control. The AWS-only running cost is shown in §6.2 for comparison.\n")
A("## 5.2 Skill set the builder applies\n")
table(["Role the builder plays", "Share of time", "Skills", "How AI helps"], [
    ["Solutions architect and security designer", "10%", "Multi-tenant SaaS, RLS, policy engines, threat modelling", "Drafts ADRs and threat checklists; builder decides"],
    ["Business analyst and product owner proxy", "8%", "Requirements, user stories, Gherkin, UAT planning", "Refines the 461 drafted stories; builder confirms with client"],
    ["Full-stack engineer (Django, React)", "38%", "APIs, workflows, data models, React screens", "Coding agents implement against specs and tests; builder reviews every change"],
    ["AI/LLM engineer", "12%", "Prompt contracts, RAG, guardrails, evaluations, cost control", "Agents draft prompts and eval sets; builder sets thresholds"],
    ["QA and test automation engineer", "14%", "Test strategy, automation, performance, accessibility", "Agents generate tests and data; builder owns coverage and UAT"],
    ["DevOps / SRE", "8%", "CI/CD, IaC, monitoring, backups, DR drills", "Agents write pipelines and runbooks; builder approves production changes"],
    ["UX designer", "5%", "Information architecture, accessible UI", "Agents generate variants from the design system; builder curates"],
    ["Project manager and client liaison", "5%", "Planning, reporting, demos", "AI drafts status reports and release notes"],
])

A("# 6. Subscriptions: while building and while using the application\n")
A("## 6.1 While building (per month, USD list prices; verify)\n")
rows = [[r[0], r[1], r[2], f"{usd(r[3])}–{usd(r[4])}" if r[4] != r[3] else usd(r[3]), f"{inr(r[3] * FX)}–{inr(r[4] * FX)}" if r[4] != r[3] else inr(r[3] * FX), r[5], "Client (pass-through)" if r[0] in CLIENT_OWNED else "Builder (in fee)"] for r in BUILD_SUBS]
rows.append(["**Builder's tools (in the fee)**", "", "", f"**{usd(BTOOLS_LO)}–{usd(BTOOLS_HI)}**", f"**{inr(BTOOLS_LO * FX)}–{inr(BTOOLS_HI * FX)}**", "", ""])
rows.append(["**Client-owned infrastructure (pass-through)**", "", "", f"**{usd(BINFRA_LO)}–{usd(BINFRA_HI)}**", f"**{inr(BINFRA_LO * FX)}–{inr(BINFRA_HI * FX)}**", "", ""])
rows.append(["**Total per month while building**", "", "", f"**{usd(BUILD_LO)}–{usd(BUILD_HI)}**", f"**{inr(BUILD_LO * FX)}–{inr(BUILD_HI * FX)}**", "", ""])
rows.append(["Claude API tokens for coding agents (average per month)", "Headless/parallel agents in CI", "Pay-as-you-go, capped at $300/month", f"≈ {usd((CORE['tokens'] + A1['tokens']) / FX / MONTHS)}", f"≈ {inr((CORE['tokens'] + A1['tokens']) / MONTHS)}", "Required", "Builder (in fee)"])
table(["Subscription", "Purpose", "Plan", "Per month (USD)", "Per month (INR)", "Status", "Paid by"], rows, [15, 28, 11, 8, 10, 6, 8])
A(f"Over the ≈ {MONTHS:.0f}-month build, the fee includes **{lakh(CORE['tools'] + A1['tools'])}** for the builder's tools and **{lakh(CORE['tokens'] + A1['tokens'])}** for tokens (§4.2). The client-owned infrastructure is about {lakh(BINFRA_LO * FX * MONTHS)}–{lakh(BINFRA_HI * FX * MONTHS)} over the same period, billed at actuals.\n")
A("## 6.2 While using the application (pilot, after go-live; per month)\n")
rows = [[r[0], r[1], r[2], f"{inr(r[3])}–{inr(r[4])}" if r[4] != r[3] else inr(r[3]), f"{usd(r[3] / FX)}–{usd(r[4] / FX)}" if r[4] != r[3] else usd(r[3] / FX), r[5]] for r in RUN_SOLO]
rows.append(["**Subtotal**", "", "", f"**{inr(RS_LO)}–{inr(RS_HI)}**", f"**{usd(RS_LO / FX)}–{usd(RS_HI / FX)}**", ""])
rows.append(["Contingency 15%", "", "", f"{inr(RS_LO * 0.15)}–{inr(RS_HI * 0.15)}", "", ""])
rows.append(["**Total running cost (recommended stack)**", "", "", f"**{inr(RS_LO_C)}–{inr(RS_HI_C)}**", f"**{usd(RS_LO_C / FX)}–{usd(RS_HI_C / FX)}**", ""])
rows.append(["For comparison: blueprint baseline (AWS only) incl. alignment and A1 additions", "", "", f"{inr(BL_LO)}–{inr(BL_HI)}", f"{usd(BL_LO / FX)}–{usd(BL_HI / FX)}", ""])
table(["Subscription / service", "Purpose", "Billing", "Per month (INR)", "Per month (USD)", "Category"], rows, [18, 28, 10, 11, 9, 7])
A("**Why the recommended stack's range is higher than the AWS-only baseline.** It includes three things the baseline leaves out:\n")
A("- the maintainer's Claude Max seat (₹9,000);")
A("- optional point-in-time recovery (up to ₹9,000);")
A("- paid error tracking (up to ₹2,340).\n")
A("Hosting compared like for like is within a few thousand rupees per month. In exchange, one person no longer has to operate the database, backups and CDN.\n")
A(f"**Production AI usage.** The {len(ag)} AI agents in scope cost about **{inr(sum(i['run_base'] for i in ag))} per month** at pilot volume, or ≈ {inr(ai_run_base)} with a 25% overhead (high case ≈ {inr(sum(i['run_hi'] for i in ag) * 1.25)}). Hard caps in the gateway (₹3,000 core + ₹2,000 advanced) stop paid calls if a limit is reached, and work then degrades safely.\n")
A("**As the business grows.** At the growth gate, running costs are about ₹50,000–70,000 per month; at scale, about ₹1.3–1.7 lakh per month. They rise only when measured business results pass the blueprint's scale gates. External SaaS tenants pay for their own usage through their plans.\n")
A("**Optional or conditional:** Apollo enrichment (≈ ₹10,350/month, only after the scale gate), e-signature (per envelope), payment-gateway fees (≈ 2% of collections), paid advertising (campaign budgets).\n")

A("# 7. Pass-through costs (not in the fee; billed at actuals)\n")
table(["Item", "Estimate", "Why separate"], [
    ["Independent penetration tests: before Release 1, before Release 2, before A1 go-live", "₹5,50,000 – ₹14,00,000", "Security must be certified by an independent tester"],
    ["Running the application (client-owned accounts)", f"{inr(RS_LO_C)} – {inr(RS_HI_C)} per month after go-live; less during the build", "Client owns production accounts and data"],
    ["External legal counsel (DPDP, children's data, contracts)", "As quoted by counsel (indicatively ₹1.5–5 lakh)", "Legal advice is outside the builder's scope"],
    ["Business costs (data purchases, advertising, payment-gateway fees)", "As used", "Not platform build costs"],
])

A("# 8. Timeline and payment milestones\n")
ms = [("Contract signing (mobilisation)", 0.10, 0), ("Foundation gate: environments, identity, tenancy, model gateway", 0.10, 3),
      ("Release 1 functional complete (UAT start)", 0.15, 12), ("Release 1 go/no-go passed", 0.15, 15),
      ("Release 2 build gate passed", 0.15, round(CORE["months"]) - 1), ("30-day monitored pilot completed", 0.10, round(CORE["months"]) + 1),
      ("Advanced A1 mid-point demo", 0.10, round(CORE["months"] + A1["months"] / 2)), ("Advanced A1 go-live and acceptance", 0.15, round(MONTHS))]
table(["Milestone", "Indicative month from start", "Share", "Amount (excl. GST)", "Amount (incl. GST)"],
      [[m, f"Month {mo}", f"{s * 100:.0f}%", inr(QUOTE * s), inr(QUOTE * s * (1 + GST))] for m, s, mo in ms] + [["**Total**", "", "**100%**", f"**{inr(QUOTE)}**", f"**{inr(QUOTE * (1 + GST))}**"]])
A(f"**Important.** One builder needs about {MONTHS:.0f} months; an AI-assisted team would need about 12–13. If an earlier date matters more than price, the scope can be phased or contract engineers added under a revised quotation. Progress is reported monthly with measured throughput. If measured AI productivity is materially better than assumed, the remaining milestones' dates move earlier at no extra cost.\n")

A("# 9. Maintenance and support retainer\n")
A(f"**{inr(RETAINER)} + GST per month** from go-live (core and A1 live), renewable yearly; about 10% of the fee per year. It covers:\n")
A("- bug fixes, security patches and dependency upgrades;")
A("- Claude model-version migrations with re-evaluation;")
A("- monitoring and business-hours incident response;")
A("- quarterly DR drill;")
A("- up to 6 days of small changes per month.\n")
A("Larger changes are quoted at the day rate.\n")

A("# 10. Future options (indicative, not part of this quotation)\n")
a2 = 518 * (1 - SAVE)
a3 = 283 * (1 - SAVE)
table(["Option", "Builder's effort (days)", "Indicative fee (excl. GST)", "Duration"], [
    ["Advanced A2: NBA, deal risk, ABM, intent hub, deal rooms, partners, QBR, semantic layer, NL analytics", f"{a2:,.0f}", lakh(a2 * DAY_RATE * 1.15 + a2 / PROD_DAYS * (BTOOLS_LO + BTOOLS_HI) / 2 * FX), f"≈ {a2 / PROD_DAYS:.0f} months"],
    ["Advanced A3 (after the scale gate): conversation intelligence, marketing mix, no-code builder, developer platform", f"{a3:,.0f}", lakh(a3 * DAY_RATE * 1.15 + a3 / PROD_DAYS * (BTOOLS_LO + BTOOLS_HI) / 2 * FX), f"≈ {a3 / PROD_DAYS:.0f} months"],
])

A("# 11. Why the buyer can trust this price\n")
for s in [
    "**Specified before priced.** The scope is defined in a 4,745-page blueprint: 461 user stories, 4,156 test cases, 579 API operations, 80 AI agents and 344 recorded decisions. Nothing is priced on guesswork.",
    "**Every number is traceable** to the blueprint's effort, the published AI-built factors and list prices, with formulas shown in §4.",
    "**Cheaper than the alternatives.** It costs about a third less than an AI-assisted team and a little over half the price of a traditional team, for the same scope.",
    "**Safety does not depend on trust in AI.** Consequential actions always need a person, and policy is rechecked at dispatch. Hard AI cost caps, independent penetration tests and human review of every AI-generated change are all built in.",
    "**The client owns everything:** code, infrastructure, data, accounts and IP on full payment.",
    "**Fixed price with milestones tied to evidence.** The client pays as gates are passed, not for time spent.",
]:
    A(f"- {s}")
A("")

A("# 12. Assumptions and terms\n")
for i, t in enumerate([
    "Scope is the Application Blueprint v1.1 as of 28 Nov 2026; changes are priced by written change request at the day rate.",
    f"The builder's time is valued at ₹1.25 lakh per month ({inr(DAY_RATE)} per day; {inr(HOUR_RATE)} per hour), with {PROD_DAYS} productive days per month.",
    f"AI productivity is the central case of Cost Estimate v1.1 plus 4% for solo working (net {SAVE * 100:.1f}%). These are planning assumptions; measured progress is reported monthly.",
    "Claude Sonnet is the primary production model. Subscription and token prices are list prices as of the date; changes above 10% are passed through.",
    "The client provides timely approvals, UAT users, provider accounts (AWS, Supabase, Vercel, Anthropic, Meta), and legal confirmations.",
    "Build agents work with synthetic data only; no production personal data is shared with them.",
    "GST at 18% applies to all fees. Pass-through costs are invoiced at actuals with receipts.",
], 1):
    A(f"{i}. {t}")
A("")
for t in ["**Price type:** fixed price for the defined scope.", "**Intellectual property:** transferred to the client on full payment.",
          "**Warranty:** 60 days after each go-live for defects against acceptance criteria.", "**Confidentiality:** all client data and documents are confidential.",
          "**Payment terms:** invoices payable within 15 days of milestone acceptance.", "**Validity:** 30 days."]:
    A(f"- {t}")
A("\n**Acceptance**\n")
table(["For the client", "For the builder"], [["Name: ______________________", "Name: ______________________"], ["Signature: __________________", "Signature: __________________"], ["Date: ______________________", "Date: ______________________"]])

md = "\n".join(L) + "\n"
(OUT / f"{NAME}.md").write_text(md, encoding="utf-8")
print(f"SAVE {SAVE:.4f} cost {COST:,.0f} quote {QUOTE:,} months {MONTHS:.1f} build/mo ${BUILD_LO}-{BUILD_HI} run {RS_LO_C:,.0f}-{RS_HI_C:,.0f} in-scope {len(IN)}")

if __name__ == "__main__":
    env = {**os.environ, "LANG": "C.UTF-8", "LC_ALL": "C.UTF-8"}
    subprocess.run([str(BP / "make_pdf.sh"), f"{NAME}.md", "Final Solo-Builder Quotation v2.0 · 28 Nov 2026 · Confidential"], cwd=OUT, check=True, env=env)
    import build_docx
    build_docx.build(OUT / f"{NAME}.md", OUT / f"{NAME}.docx", header="AI Growth Engine — Final Solo-Builder Quotation v2.0    |    Confidential · 28 Nov 2026",
                     title="AI Growth Engine: Final Solo-Builder Quotation", subtitle="Core platform + Advanced A1, built single-handedly with AI models and AI agents (fixed price, INR)",
                     version="Quotation v2.0 · 28 Nov 2026 · Valid for 30 days")
