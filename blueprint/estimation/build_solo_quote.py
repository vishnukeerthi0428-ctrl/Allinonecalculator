#!/usr/bin/env python3
"""Solo-builder quote (one person building with AI models and agents), PDF and Word.

Usage: python3 blueprint/estimation/build_solo_quote.py
"""
import os
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import ai_model as X  # noqa: E402

BP = HERE.parent
OUT = BP / "final" / "estimation"
NAME = "AI_Growth_Engine_Solo_Builder_Quote_v1.0"
FX = 90.0
PD = 125_000 / 22                      # ₹ per day, senior solo rate (₹1.25 L per month)
DAYS_PER_MONTH = 21                    # productive days per month for one person
SAVE = 0.288 + 0.04                    # AI-built central net saving + solo coordination saving
TOOLS_USD = 300                        # per month
USD_PD = X.usd_per_agent_pd()          # ≈ $6.78 per agent-executed person-day
AGENT_SHARE = 0.48
GST = 0.18


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


def phase(trad_pd):
    pd = trad_pd * (1 - SAVE)
    months = pd / DAYS_PER_MONTH
    labour = pd * PD
    tools = TOOLS_USD * months * FX
    tokens = trad_pd * AGENT_SHARE * USD_PD * FX
    cont = 0.15 * (labour + tokens)
    return dict(pd=pd, months=months, labour=labour, tools=tools, tokens=tokens, cont=cont, cost=labour + tools + tokens + cont)


core = phase(722 + 107.2)
a1 = phase(553)
CORE_FEE = 4_900_000
A1_FEE = 3_100_000
RETAINER = 55_000

L = []
A = L.append


def table(h, rows, w=None):
    A("| " + " | ".join(h) + " |")
    A("|" + "|".join("-" * max(3, x) for x in (w or [3] * len(h))) + "|")
    for r in rows:
        A("| " + " | ".join(str(c) for c in r) + " |")
    A("")


A("# AI Growth Engine: Solo-Builder Quotation")
A("## Fixed-price quotation for building the application single-handedly with AI models and AI agents (INR)")
A("")
table(["Field", "Value"], [
    ["Quotation", "AI Growth Engine – Employee Sales & Marketing Automation platform"],
    ["Prepared for", "[Client name]"],
    ["Prepared by", "[Your name / company]"],
    ["Date", "28 Nov 2026"],
    ["Validity", "30 days from the date above"],
    ["Basis", "Application Blueprint v1.1 (Parts 0–9.10, 344 decisions) and Cost Estimates v1.0 and v1.1"],
    ["Currency", "Indian Rupees (INR). GST at 18% is added to every fee"],
])

A("# 1. Summary of the quotation\n")
table(["Item", "Fee (excl. GST)", "GST 18%", "Fee (incl. GST)", "Duration"], [
    ["**Core platform: Releases 1 and 2, 100% aligned with the 38-document specification**", f"**{inr(CORE_FEE)}**", inr(CORE_FEE * GST), f"**{inr(CORE_FEE * (1 + GST))}**", f"≈ {core['months']:.0f} months"],
    ["Optional: Advanced release A1 (advanced AI agents, revenue-growth and platform capabilities)", inr(A1_FEE), inr(A1_FEE * GST), inr(A1_FEE * (1 + GST)), f"≈ {a1['months']:.0f} further months"],
    ["Maintenance and support retainer after go-live", f"{inr(RETAINER)} per month", f"{inr(RETAINER * GST)} per month", f"{inr(RETAINER * (1 + GST))} per month", "Monthly, from go-live"],
    ["Pass-through costs (at actuals, see §5)", "Security testing ₹4–10 lakh; running costs ≈ ₹15,000–30,475 per month", "As invoiced", "As invoiced", "—"],
])
A(f"**Headline: core platform for {inr(CORE_FEE)} + GST, fixed price, delivered by one builder using AI agents in about {core['months']:.0f} months.**\n")

A("# 2. What the client receives (scope)\n")
A("The core platform as specified in the Application Blueprint v1.1:\n")
for s in [
    "Public Website/Portal (34 screens) and the confidential Admin Command Centre (113 screens), as separate React/TypeScript applications.",
    "Multi-tenant backend (Django REST Framework, PostgreSQL with row-level security and pgvector, Celery/Valkey, S3) on AWS ap-south-1.",
    "Owner Portfolio tenant with the four launch startups (AppNAI, MedMaarg, EduVerse, OrganicSpec) and onboarding of external SaaS tenants.",
    "Workflows WF-01 to WF-14: catalogue, discovery, outreach under consent, inbound handling, qualification, meetings, bids, proposals and quotes, orders, verified close, onboarding, plans and offboarding.",
    "The release-1 and release-2 AI agents and automations, using Claude Sonnet as the primary model through the model gateway, with hard cost caps and human approval for consequential actions.",
    "Literal alignment with all 38 source documents (99.98% literal match; the two remaining items are the approved Claude-primary decision).",
    "Tests and evidence: automated unit, integration and UI tests, AI evaluation sets, UAT support, and release evidence packs.",
    "Deployment, monitoring, backups, disaster-recovery drill, runbooks, training task cards and handover documentation.",
]:
    A(f"- {s}")
A("\nThe advanced capabilities in Parts 9.7–9.9 (42 further AI agents, revenue-growth and platform features) are **not** in the core fee. Release A1 is quoted as an option (§6).\n")

A("# 3. How the price is built\n")
table(["Component", "Basis", "Core platform", "Advanced A1 (option)"], [
    ["Builder's time", f"{core['pd']:,.0f} days (core) and {a1['pd']:,.0f} days (A1) at {inr(PD)} per day (senior rate, ₹1.25 lakh per month)", lakh(core["labour"]), lakh(a1["labour"])],
    ["AI and build tools", f"Claude Max 20x, GitHub, Figma, BrowserStack, CI sandboxes, domains: ≈ ${TOOLS_USD} per month × duration", lakh(core["tools"]), lakh(a1["tools"])],
    ["Claude API tokens for coding agents", f"≈ ${USD_PD:.2f} per agent-executed day; {AGENT_SHARE * 100:.0f}% of the work executed by agents", lakh(core["tokens"]), lakh(a1["tokens"])],
    ["Contingency", "15% of time and tokens", lakh(core["cont"]), lakh(a1["cont"])],
    ["**Cost basis**", "", f"**{lakh(core['cost'])}**", f"**{lakh(a1['cost'])}**"],
    ["**Quoted fee**", "Rounded, small margin", f"**{lakh(CORE_FEE)}**", f"**{lakh(A1_FEE)}**"],
])
A(f"**Effort basis.** A traditional team would need about 829 person-days for the core platform and 553 for A1. Building with AI agents saves about 29% (central case of Cost Estimate v1.1). A single builder saves about 4% more, because there is no team to coordinate. That leaves about {core['pd']:,.0f} and {a1['pd']:,.0f} days of the builder's own work: specifying, reviewing every AI-generated change, testing and releasing.\n")

A("# 4. Payment milestones (core platform)\n")
ms = [("On signing (mobilisation)", 0.15), ("Foundation gate passed (environments, identity, tenancy, gateway)", 0.20),
      ("Release 1 go/no-go passed", 0.25), ("Release 2 build gate passed", 0.25), ("30-day monitored pilot completed", 0.15)]
table(["Milestone", "Share", "Amount (excl. GST)", "Amount (incl. GST)"], [[m, f"{s * 100:.0f}%", inr(CORE_FEE * s), inr(CORE_FEE * s * (1 + GST))] for m, s in ms]
      + [["**Total**", "**100%**", f"**{inr(CORE_FEE)}**", f"**{inr(CORE_FEE * (1 + GST))}**"]])
A("Invoices are payable within 15 days. Each milestone is accepted against the evidence defined in the blueprint's release gates.\n")

A("# 5. Pass-through costs (billed at actuals, not included in the fee)\n")
table(["Item", "Estimate", "Why it is separate"], [
    ["Two external penetration tests and scope uplift", "₹4,00,000 – ₹10,00,000", "Independent security testing; a solo builder must not certify their own security"],
    ["Cloud, AI inference and providers during the build", "≈ ₹15,000 – ₹30,000 per month (ramps up)", "Client-owned accounts (AWS, Anthropic, Meta WhatsApp, Amazon SES)"],
    ["Running cost after go-live (pilot)", "₹24,035 – ₹30,475 per month", "Client-owned; hard caps on AI spend"],
    ["External legal counsel (data protection, contracts)", "As quoted by counsel", "Legal advice is outside the builder's scope"],
    ["Paid data, advertising media, payment-gateway fees", "As used", "Business costs, not platform build costs"],
])

A("# 6. Option: Advanced release A1\n")
A(f"**{inr(A1_FEE)} + GST** ({inr(A1_FEE * (1 + GST))} incl. GST), about {a1['months']:.0f} further months after the core platform. Scope as defined for A1 in Parts 9.7–9.10. Highlights:\n")
A("- the supervisor/planner over existing agents;")
A("- the RFP response co-pilot and account research;")
A("- predictive scoring with explanations;")
A("- pipeline inspection and forecasting;")
A("- multichannel cadences under consent and CPQ guardrails;")
A("- AI observability, passkeys, just-in-time admin access, secrets rotation, the DPDP rights workflow and the trust centre.\n")
A("Releases A2 and A3 can be quoted separately later.\n")

A("# 7. Maintenance and support retainer\n")
A(f"**{inr(RETAINER)} + GST per month** from go-live, renewable yearly. It covers:\n")
A("- bug fixes, security patches and dependency upgrades;")
A("- model-version migrations with re-evaluation;")
A("- monitoring and incident response in business hours;")
A("- up to 6 days of small changes per month.\n")
A("Larger changes are quoted separately.\n")

A("# 8. Timeline\n")
table(["Phase", "Indicative duration (solo)", "With a team (for reference)"], [
    ["Foundation (environments, identity, tenancy, gateway)", "≈ 3 months", "1 month"],
    ["Release 1 build and go/no-go", "≈ 15 months from start", "≈ 6 months (4 Jun 2027)"],
    ["Release 2 build and pilot", f"≈ {core['months']:.0f} months from start, plus the 30-day pilot", "≈ 7.5 months (23 Jul 2027)"],
    ["Advanced A1 (option)", f"≈ {a1['months']:.0f} further months", "≈ 5 months"],
])
A("**Important:** a single builder cannot meet the team plan's June 2027 date. If an earlier date is essential, the scope can be phased further, or contract engineers added under a revised quotation.\n")

A("# 9. Comparison with other ways of building it\n")
table(["Approach", "Core + alignment (excl. GST)", "Duration"], [
    ["Traditional team", "≈ ₹74.5 lakh", "≈ 7 months"],
    ["AI-assisted team (approved approach, DEC-420)", "≈ ₹55.4 lakh", "≈ 7 months"],
    [f"**This quotation: solo builder with AI**", f"**{lakh(CORE_FEE)} + security tests at actuals**", f"**≈ {core['months']:.0f} months**"],
])

A("# 10. Assumptions\n")
for i, t in enumerate([
    "Scope is the Application Blueprint v1.1 as of 28 Nov 2026; changes go through written change requests priced at the day rate above.",
    f"The builder's time is valued at ₹1.25 lakh per month ({inr(PD)} per day), with {DAYS_PER_MONTH} productive days per month.",
    "AI productivity: 29% net saving (central case) plus 4% for solo working. These are planning assumptions. Plausible outcomes range from about 7% to 44%, and the builder will report measured progress monthly.",
    "Claude Sonnet is the primary production model (DEC-418). Tool and token prices are list prices as of the date and may change.",
    "The client provides timely approvals, test users for UAT, provider accounts (AWS, Anthropic, Meta, payment gateway) and legal confirmations.",
    "Agents work on synthetic data only; no production personal data is shared with build agents.",
    "GST at 18% is added to all fees. Pass-through costs are invoiced at actuals with receipts.",
], 1):
    A(f"{i}. {t}")
A("")

A("# 11. Terms\n")
for t in [
    "**Price type:** fixed price for the defined scope; change requests are priced separately.",
    "**Intellectual property:** transferred to the client on full payment, including source code, infrastructure code, documentation and test assets.",
    "**Warranty:** 60 days after the pilot completes for defects against the agreed acceptance criteria.",
    "**Confidentiality:** all client data and documents are treated as confidential.",
    "**Validity:** 30 days.",
]:
    A(f"- {t}")
A("\n**Acceptance**\n")
table(["For the client", "For the builder"], [["Name: ______________________", "Name: ______________________"], ["Signature: __________________", "Signature: __________________"], ["Date: ______________________", "Date: ______________________"]])

md = "\n".join(L) + "\n"
(OUT / f"{NAME}.md").write_text(md, encoding="utf-8")
print("core", {k: round(v) for k, v in core.items()}, "a1", {k: round(v) for k, v in a1.items()})

if __name__ == "__main__":
    env = {**os.environ, "LANG": "C.UTF-8", "LC_ALL": "C.UTF-8"}
    subprocess.run([str(BP / "make_pdf.sh"), f"{NAME}.md", "Solo-Builder Quotation · 28 Nov 2026 · Confidential"], cwd=OUT, check=True, env=env)
    import build_docx
    build_docx.build(OUT / f"{NAME}.md", OUT / f"{NAME}.docx", header="AI Growth Engine — Solo-Builder Quotation    |    Confidential · 28 Nov 2026",
                     title="AI Growth Engine: Solo-Builder Quotation", subtitle="Fixed-price quotation for building the application single-handedly with AI models and AI agents (INR)",
                     version="Quotation · 28 Nov 2026 · Valid for 30 days")
