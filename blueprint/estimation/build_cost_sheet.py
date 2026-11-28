#!/usr/bin/env python3
"""Final revised cost sheet: optimized, discounted all-inclusive package (solo builder with AI), Word and PDF.

Usage: python3 blueprint/estimation/build_cost_sheet.py
"""
import os
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import model as M  # noqa: E402

BP = HERE.parent
OUT = BP / "final" / "estimation"
NAME = "AI_Growth_Engine_Final_Cost_Sheet_Solo_AI_v1.0"
FX = 90.0
GST = 0.18
DAY = 125_000 / 22
PD = 929.0
MONTHS = 44.2
PACKAGE = 9_000_000

# ---- optimized fee build-up (before discount)
labour = PD * DAY
tools = (204 * MONTHS + 16 * 12 + 29 * 6) * FX
tokens = 405_000 * 0.8
cont = 0.10 * (labour + tokens)
fee_opt = 7_010_000

# ---- optimized running (client-owned, at cost)
base_lo = sum(r[4] for r in M.LEDGER_B)
base_hi = sum(r[5] for r in M.LEDGER_B)
pil_lo = (base_lo - 2_000) * 1.15
pil_hi = (base_hi - 3_300) * 1.15
pil = (pil_lo + pil_hi) / 2
a1add = (0.35 * 11_051 + 0.35 * 36_098) / 2
staging_m = 65 * FX
ITEMS = [
    ("C1", "Independent penetration tests: 2 engagements (before Release 1; combined before Release 2 + A1), CERT-In-empanelled vendor", "At actuals", None, None, 650_000, "Range ₹4,00,000 – ₹9,00,000"),
    ("C2", "Client hosting while building (staging only): Vercel Pro, Supabase Pro, small AWS Mumbai server, domains", "Months 1–15", staging_m, 15, staging_m * 15, "≈ $65 per month"),
    ("C3", "Pilot running from Release 1 go-live to A1 go-live (Vercel, Supabase, AWS, Claude API with hard caps, email, WhatsApp, search, extraction, DR storage, 15% contingency)", "Months 15–44", pil, MONTHS - 15, pil * (MONTHS - 15), f"₹{pil_lo:,.0f} – ₹{pil_hi:,.0f} per month"),
    ("C4", "Running cost, first 12 months after full go-live (C3 lines + A1 feature additions)", "12 months", pil + a1add, 12, (pil + a1add) * 12, "Growth-gate step-ups only if the gate passes"),
]
retainer = 55_000 * 12
at_cost = sum(i[5] for i in ITEMS)
fee = PACKAGE - retainer - at_cost
discount = fee_opt - fee
before_opt = 11_298_000


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


L = []
A = L.append


def table(h, rows, w=None):
    A("| " + " | ".join(h) + " |")
    A("|" + "|".join("-" * max(3, x) for x in (w or [3] * len(h))) + "|")
    for r in rows:
        A("| " + " | ".join(str(c) for c in r) + " |")
    A("")


A("# AI Growth Engine: Final Cost Sheet")
A("## Optimized, discounted all-inclusive package · Core platform + Advanced A1 · built by a solo builder with AI")
A("")
table(["Field", "Value"], [
    ["Prepared for", "[Client name]"],
    ["Prepared by", "[Your name / company]"],
    ["Version and date", "Final cost sheet v1.0 · 28 Nov 2026 · approved for issue"],
    ["Validity", "30 days"],
    ["Basis", "Application Blueprint v1.1 (346 decisions, incl. DEC-418 Claude Sonnet primary, DEC-421 Vercel + Supabase hosting, DEC-422 running budget); Final Solo-Builder Quotation v2.0"],
    ["Currency", "INR; GST 18% shown separately"],
])

A("# 1. Package price\n")
table(["", "Amount"], [
    ["**All-inclusive package (excluding GST)**", f"**{inr(PACKAGE)}**"],
    ["GST 18%", inr(PACKAGE * GST)],
    ["**All-inclusive package (including GST)**", f"**{inr(PACKAGE * (1 + GST))}**"],
    ["Period covered", f"Build (≈ {MONTHS:.0f} months) + first 12 months of operation after full go-live"],
    ["Saving against the unoptimized package (≈ ₹1,12,98,000)", f"{inr(before_opt - PACKAGE)} ({(before_opt - PACKAGE) / before_opt * 100:.0f}%)"],
])

A("# 2. Cost sheet\n")
rows = [
    ["A", "**Fixed development fee**: Core platform (Releases 1 and 2, aligned with the 38-document specification) + Advanced release A1", "Fixed", "—", "—", f"**{inr(fee)}**", inr(fee * GST), inr(fee * (1 + GST))],
    ["B", "**Maintenance and support retainer**, first 12 months (includes the maintainer's Claude seat)", "Fixed monthly", inr(55_000), "12", f"**{inr(retainer)}**", inr(retainer * GST), inr(retainer * (1 + GST))],
]
for cid, name, basis, rate, n, amt, note in ITEMS:
    rows.append([cid, f"{name} ({note})", basis, inr(rate) if rate else "—", f"{n:.1f}" if n else "—", inr(amt), inr(amt * GST), inr(amt * (1 + GST))])
rows.append(["", "**Total**", "", "", "", f"**{inr(PACKAGE)}**", f"**{inr(PACKAGE * GST)}**", f"**{inr(PACKAGE * (1 + GST))}**"])
table(["#", "Item", "Basis", "Rate per month", "Months", "Amount (excl. GST)", "GST 18%", "Amount (incl. GST)"], rows, [3, 40, 9, 8, 5, 10, 8, 10])
A("A and B are fixed prices. C1–C4 are client-owned costs paid at actuals: the figures are the estimates inside the package. The client owns the Vercel, Supabase, AWS, Anthropic and Meta accounts from day one.\n")

A("# 3. How the development fee is arrived at\n")
table(["Component", "Basis", "Amount"], [
    ["Builder's effort with AI", f"{PD:,.0f} days (traditional 1,382 days × (1 − 32.8% AI-built saving))", "—"],
    ["Builder's time", f"{PD:,.0f} days × {inr(DAY)} per day ({inr(DAY / 8)} per hour; ₹1.25 lakh per month)", inr(labour)],
    ["Builder's tools", f"Claude Max 20x $200 + GitHub $4 for {MONTHS:.0f} months; Figma $16 for 12 months; BrowserStack $29 for 6 months; at ₹{FX:.0f}/$", inr(tools)],
    ["Claude API tokens for coding agents", "≈ 663 agent-executed days × $6.78, less 20% with prompt caching and the Haiku model", inr(tokens)],
    ["Contingency", "10% of time and tokens", inr(cont)],
    ["**Optimized fee**", "Cost basis rounded up", f"**{inr(fee_opt)}**"],
    ["Package discount", "Applied to reach the ₹90,00,000 package", f"− {inr(discount)}"],
    ["**Fixed development fee (A)**", "", f"**{inr(fee)}**"],
])
A(f"**Effect of the discount.** It uses about {discount / cont * 100:.0f}% of the contingency. The remaining contingency is {inr(cont - discount)}. Scope is therefore frozen at the blueprint and changed only by written change request at the day rate.\n")

A("# 4. How the package was optimized\n")
table(["Lever", "Saving"], [
    ["Builder tools trimmed (BrowserStack 6 months, Figma 12 months, client's own Workspace)", "₹2,06,000"],
    ["Claude tokens cut ≈ 20% (prompt caching, Haiku for simple tasks)", "₹81,000"],
    ["Contingency 15% → 10% (fully specified scope, change control)", "₹2,84,000"],
    ["Penetration tests 3 → 2 (combined Release 2 + A1 test)", "₹3,25,000"],
    ["Staging-only hosting until Release 1", "₹3,06,000"],
    ["Pilot running without team seats, delivery AI line and integration reserve; free monitoring tiers", "₹2,10,000"],
    ["Year 1: point-in-time recovery deferred to the growth gate; maintainer seat inside the retainer", "₹2,70,000"],
    ["Retainer ₹65,000 → ₹55,000 per month", "₹1,20,000"],
    ["Package discount on the development fee", inr(discount)],
    [f"**Total reduction from ≈ {inr(before_opt)}**", f"**{inr(before_opt - PACKAGE)}**"],
])

A("# 5. What is included\n")
table(["Item", "Detail"], [
    ["Applications", "Public Website/Portal (34 screens) and Admin Command Centre (113 screens), plus the A1 screens; React/TypeScript on Vercel"],
    ["Platform", "Multi-tenant Django REST backend, PostgreSQL on Supabase (RLS, pgvector), Celery/Valkey on AWS Mumbai, policy engine, outbox, audit"],
    ["AI agents, automations, workflows", "170 in scope: 50 AI agents, 85 automations, 35 workflows. 88 fully automated, 7 mostly automated, 63 partially automated (human approval), 12 assistive. AI never signs, pays, submits bids or sets prices"],
    ["AI model", "Claude, through a gateway with hard monthly caps: Haiku-class for simple tasks, Sonnet-class as the primary model"],
    ["Quality", "Automated tests, AI evaluation sets, UAT support, release evidence packs, two independent penetration tests"],
    ["Handover", "Source code, infrastructure code, documentation, runbooks, training task cards; IP to the client on full payment"],
    ["Support", "12-month retainer: fixes, patches, upgrades, Claude model migrations, monitoring, quarterly DR drill, up to 6 days of small changes per month"],
])
A("Full lists of agents, automations, workflows, technology and skills: Final Solo-Builder Quotation v2.0.\n")

A("# 6. Subscriptions\n")
table(["Subscription", "While building", "While using the application", "Paid by"], [
    ["Claude Max 20x (Claude Code)", "$200 per month", "Maintainer seat inside the retainer", "Builder (in fee / retainer)"],
    ["Claude API (coding agents)", "≈ $82 per month average, capped", "—", "Builder (in fee)"],
    ["Claude API (application's AI agents)", "Within C3 once live", "Hard caps ₹3,000 core + ₹2,000 advanced per month", "Client (C3/C4)"],
    ["Vercel Pro", "$20 per month", "$20–40 per month", "Client"],
    ["Supabase Pro (Mumbai)", "$25 per month (staging)", "$40–60 per month (production compute)", "Client"],
    ["AWS ap-south-1 (API, workers, Valkey, S3, SES, DR)", "≈ $15 per month (staging)", "≈ ₹3,000–4,650 per month", "Client"],
    ["WhatsApp (Meta), search API, extraction", "From Release 1", "≈ ₹4,500 per month", "Client"],
    ["GitHub", "$4 per month", "Inside the retainer", "Builder"],
    ["Figma, BrowserStack", "12 months / 6 months only", "—", "Builder (in fee)"],
    ["Domains (≈ 5)", "≈ $5–8 per month", "≈ $5–8 per month", "Client"],
    ["Monitoring (Sentry, uptime)", "Free tiers", "Free tiers", "—"],
])

A("# 7. Payment schedule\n")
ms = [("Contract signing", 0.10, "Month 0"), ("Foundation gate", 0.10, "Month 3"), ("Release 1 functional complete", 0.15, "Month 12"),
      ("Release 1 go/no-go", 0.15, "Month 15"), ("Release 2 build gate", 0.15, "Month 26"), ("30-day pilot completed", 0.10, "Month 28"),
      ("Advanced A1 mid-point demo", 0.10, "Month 35"), ("Advanced A1 go-live and acceptance", 0.15, "Month 44")]
table(["Milestone (fee A)", "Indicative month", "Share", "Amount (excl. GST)", "Amount (incl. GST)"],
      [[m, mo, f"{s * 100:.0f}%", inr(fee * s), inr(fee * s * (1 + GST))] for m, s, mo in ms] + [["**Total fee A**", "", "**100%**", f"**{inr(fee)}**", f"**{inr(fee * (1 + GST))}**"]])
A(f"The retainer (B) is billed monthly from go-live at {inr(55_000)} + GST. Items C1–C4 are paid by the client to the providers as incurred.\n")

A("# 8. After the first year\n")
A(f"The ongoing cost is about **{inr(pil + a1add)} per month for running plus {inr(55_000)} per month for maintenance** (plus GST). Running costs rise only if the business passes the growth gate (≈ ₹59,000–79,000 per month, DEC-422). External SaaS tenants pay for their own usage.\n")

A("# 9. Assumptions and terms\n")
for i, t in enumerate([
    "Scope is the Application Blueprint v1.1 (Core + Advanced A1) as of 28 Nov 2026; changes by written change request at the day rate.",
    f"One builder with AI agents; about {MONTHS:.0f} months to A1 go-live. AI productivity follows Cost Estimate v1.1 (central case) plus 4% for solo working; progress is reported monthly.",
    "Items C1–C4 are estimates at list prices as of 28 Nov 2026 and are paid at actuals; changes in provider prices pass through.",
    "The client provides timely approvals, UAT users, provider accounts and legal confirmations. External legal counsel, paid data and advertising are not included.",
    "Build agents use synthetic data only; no production personal data is shared with them.",
    "Fixed price for A and B; IP transfers to the client on full payment; 60-day warranty after each go-live; invoices payable within 15 days of milestone acceptance.",
], 1):
    A(f"{i}. {t}")
A("\n**Acceptance**\n")
table(["For the client", "For the builder"], [["Name: ______________________", "Name: ______________________"], ["Signature: __________________", "Signature: __________________"], ["Date: ______________________", "Date: ______________________"]])

(OUT / f"{NAME}.md").write_text("\n".join(L) + "\n", encoding="utf-8")
print("fee", round(fee), "at_cost", round(at_cost), "discount", round(discount), "cont left", round(cont - discount), [round(i[5]) for i in ITEMS])

if __name__ == "__main__":
    env = {**os.environ, "LANG": "C.UTF-8", "LC_ALL": "C.UTF-8"}
    subprocess.run([str(BP / "make_pdf.sh"), f"{NAME}.md", "Final Cost Sheet · 28 Nov 2026 · Confidential"], cwd=OUT, check=True, env=env)
    import build_docx
    build_docx.build(OUT / f"{NAME}.md", OUT / f"{NAME}.docx", header="AI Growth Engine — Final Cost Sheet (solo builder with AI)    |    Confidential · 28 Nov 2026",
                     title="AI Growth Engine: Final Cost Sheet", subtitle="Optimized, discounted all-inclusive package: Core + Advanced A1, solo builder with AI (INR)",
                     version="Cost sheet v1.0 · 28 Nov 2026 · Valid for 30 days")
