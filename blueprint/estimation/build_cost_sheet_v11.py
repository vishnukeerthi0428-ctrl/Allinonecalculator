#!/usr/bin/env python3
"""Final cost sheet v1.1: the ₹90,00,000 optimized, discounted package with every section of the detailed
solo quotation v2.0 (scope, full AI catalogue, method, effort by activity, AI vs builder, technology, skills,
subscriptions while building and while using, pass-through, timeline, retainer, future options, trust, terms).

Usage: python3 blueprint/estimation/build_cost_sheet_v11.py
"""
import os
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import build_solo_quote_v2 as Q  # noqa: E402  (regenerates v2.0 markdown; provides scope, catalogue, effort rows)
import model as M  # noqa: E402

OUT = Q.OUT
NAME = "AI_Growth_Engine_Final_Cost_Sheet_Solo_AI_v1.1"
FX, GST, DAY = Q.FX, 0.18, Q.DAY_RATE
inr, lakh, usd = Q.inr, Q.lakh, Q.usd
PACKAGE = 9_000_000
BEFORE_OPT = 11_298_000

# ---------------------------------------------------------------- optimized phases
CORE_M, A1_M = Q.CORE["months"], Q.A1["months"]
MONTHS = CORE_M + A1_M
OPT_TOOLS = [  # (tool, $/month, months core, months A1, note)
    ("Claude Max 20x (Claude Code)", 200, CORE_M, A1_M, "Whole build"),
    ("GitHub Pro", 4, CORE_M, A1_M, "Whole build"),
    ("Figma Professional", 16, 8, 4, "Design months only"),
    ("BrowserStack Live", 29, 4, 2, "Pre-release checks only"),
    ("Google Workspace", 0, CORE_M, A1_M, "Client's existing workspace used"),
]


def phase(p, key):
    tools = sum(t[1] * (t[2] if key == "core" else t[3]) for t in OPT_TOOLS) * FX
    tokens = p["tokens"] * 0.8
    cont = 0.10 * (p["labour"] + tokens)
    return dict(pd=p["pd"], trad=p["trad"], months=p["months"], labour=p["labour"], tools=tools, tokens=tokens, cont=cont,
                cost=p["labour"] + tools + tokens + cont, rows=p["rows"], agent_pd=p["agent_pd"])


C = phase(Q.CORE, "core")
A1 = phase(Q.A1, "a1")
FEE_OPT = 7_010_000
COST = C["cost"] + A1["cost"]

# client pilot running (optimized): Ledger B lines (DEC-422) without B23 (builder AI, in fee), B10 (reserve, only when approved), B07+ (free tiers)
RUN_LINES = [r for r in M.LEDGER_B if r[0] not in ("B23", "B10", "B07+")]
R_LO = sum(r[4] for r in RUN_LINES)
R_HI = sum(r[5] for r in RUN_LINES)
PIL_LO, PIL_HI = R_LO * 1.15, R_HI * 1.15
PIL = (PIL_LO + PIL_HI) / 2
A1ADD = (0.35 * 11_051, 0.35 * 36_098)
STAGING = [("Vercel Pro", 20), ("Supabase Pro (staging project)", 25), ("AWS ap-south-1 small server (t4g.small) + S3", 15), ("Domain names (≈ 5)", 5)]
STAGING_M = sum(v for _, v in STAGING) * FX
ITEMS = [
    ("C1", "Independent penetration tests: 2 engagements (before Release 1; combined before Release 2 + A1), CERT-In-empanelled vendor", "At actuals", None, None, 650_000, "range ₹4,00,000 – ₹9,00,000"),
    ("C2", "Client hosting while building (staging only)", "Months 1–15", STAGING_M, 15, STAGING_M * 15, "Vercel, Supabase, AWS, domains ≈ $65/month"),
    ("C3", "Pilot running from Release 1 go-live to A1 go-live", f"Months 15–{MONTHS:.0f}", PIL, MONTHS - 15, PIL * (MONTHS - 15), f"{inr(PIL_LO)} – {inr(PIL_HI)} per month, §6.2"),
    ("C4", "Running cost, first 12 months after full go-live (C3 + A1 feature additions)", "12 months", PIL + sum(A1ADD) / 2, 12, (PIL + sum(A1ADD) / 2) * 12, "§6.2"),
]
RETAINER_M = 55_000
RETAINER = RETAINER_M * 12
AT_COST = sum(i[5] for i in ITEMS)
FEE = PACKAGE - RETAINER - AT_COST
DISCOUNT = FEE_OPT - FEE
share_core = C["cost"] / COST
FEE_CORE, FEE_A1 = FEE * share_core, FEE * (1 - share_core)

# ---------------------------------------------------------------- reuse sections of the detailed quotation
V2 = (OUT / "AI_Growth_Engine_Solo_Builder_Quote_v2.0.md").read_text(encoding="utf-8")


def section(start, end):
    i = V2.index(start)
    j = V2.index(end, i + 1) if end else len(V2)
    return V2[i:j].rstrip() + "\n\n"


S2 = section("# 2. What the client receives", "# 3. AI agents")
S3 = section("# 3. AI agents, automations and workflows in the quoted scope", "# 4. How the price is arrived at")
S44 = section("## 4.4 How AI agents do the work", "# 5. Technology and skill set")
S5 = section("# 5. Technology and skill set", "# 6. Subscriptions")
S2 = S2.replace("(indicative prices in §10)", "(indicative prices in §10)")

L = []
A = L.append


def table(h, rows, w=None):
    A("| " + " | ".join(h) + " |")
    A("|" + "|".join("-" * max(3, x) for x in (w or [3] * len(h))) + "|")
    for r in rows:
        A("| " + " | ".join(str(c).replace("|", "/") for c in r) + " |")
    A("")


A("# AI Growth Engine: Final Cost Sheet")
A("## Optimized, discounted all-inclusive package · Core platform + Advanced A1 · built by a solo builder with AI models and AI agents")
A("")
table(["Field", "Value"], [
    ["Prepared for", "[Client name]"],
    ["Prepared by", "[Your name / company]"],
    ["Version and date", "Final cost sheet v1.1 · 28 Nov 2026 · approved for issue (supersedes cost sheet v1.0 and the solo quotation v2.0 prices)"],
    ["Validity", "30 days"],
    ["Basis", "Application Blueprint v1.1 (346 decisions, incl. DEC-418 Claude Sonnet primary, DEC-421 Vercel + Supabase hosting, DEC-422 running budget); Cost Estimates v1.0 and v1.1; Solo-Builder Quotation v2.0"],
    ["Currency", f"INR; GST 18% shown separately; USD-billed items at ₹{FX:.0f} = $1 (verify at payment)"],
])

A("# 1. Package price and cost sheet\n")
A("## 1.1 Package price\n")
table(["", "Amount"], [
    ["**All-inclusive package (excluding GST)**", f"**{inr(PACKAGE)}**"],
    ["GST 18%", inr(PACKAGE * GST)],
    ["**All-inclusive package (including GST)**", f"**{inr(PACKAGE * (1 + GST))}**"],
    ["Period covered", f"Build (≈ {MONTHS:.0f} months) + first 12 months of operation after full go-live"],
    ["Reduction against the unoptimized package (≈ ₹1,12,98,000)", f"{inr(BEFORE_OPT - PACKAGE)} ({(BEFORE_OPT - PACKAGE) / BEFORE_OPT * 100:.0f}%)"],
    ["Compared with other ways of building the same scope (development only)", "Traditional team ≈ ₹1.16 crore · AI-assisted team ≈ ₹85.1 lakh · **this package's development fee ₹65.33 lakh**"],
])
A("## 1.2 Cost sheet\n")
rows = [
    ["A", "**Fixed development fee**: Core platform (Releases 1 and 2, aligned with the 38-document specification) + Advanced release A1", "Fixed", "—", "—", f"**{inr(FEE)}**", inr(FEE * GST), inr(FEE * (1 + GST))],
    ["", "  of which Core platform", "Fixed", "—", f"{C['months']:.1f}", inr(FEE_CORE), "", ""],
    ["", "  of which Advanced A1", "Fixed", "—", f"{A1['months']:.1f}", inr(FEE_A1), "", ""],
    ["B", "**Maintenance and support retainer**, first 12 months (includes the maintainer's Claude seat and GitHub)", "Fixed monthly", inr(RETAINER_M), "12", f"**{inr(RETAINER)}**", inr(RETAINER * GST), inr(RETAINER * (1 + GST))],
]
for cid, name, basis, rate, n, amt, note in ITEMS:
    rows.append([cid, f"{name} ({note})", basis, inr(rate) if rate else "—", f"{n:.1f}" if n else "—", inr(amt), inr(amt * GST), inr(amt * (1 + GST))])
rows.append(["", "**Total package**", "", "", "", f"**{inr(PACKAGE)}**", f"**{inr(PACKAGE * GST)}**", f"**{inr(PACKAGE * (1 + GST))}**"])
table(["#", "Item", "Basis", "Rate per month", "Months", "Amount (excl. GST)", "GST 18%", "Amount (incl. GST)"], rows, [3, 40, 9, 8, 5, 10, 8, 10])
A("**How to read it.** A and B are fixed prices. C1–C4 are client-owned costs paid to the providers at actuals; the figures are the estimates inside the package. The client owns the Vercel, Supabase, AWS, Anthropic and Meta accounts from day one, so it owns its infrastructure and data from the start.\n")

A(S2)
A(S3)

A("# 4. How the price is arrived at\n")
A("## 4.1 Method\n")
for s in [
    f"Start from the **traditional effort** in the blueprint: core build + literal alignment = {C['trad']:,.0f} person-days; Advanced A1 = {A1['trad']:,.0f} person-days.",
    f"Apply the **AI-built reduction for each activity** (Cost Estimate v1.1, central case). AI agents draft and code; the builder specifies, reviews, tests and releases. Weighted reduction **{Q.RED_C * 100:.1f}%**.",
    f"Add back the **new work AI creates**: agent specs and prompts, human review of every AI change, security and licence review, rework. That adds **{Q.OVH_C * 100:.1f}%**.",
    f"Subtract the **solo coordination saving** (no team meetings or hand-offs): **{Q.SOLO_EXTRA * 100:.0f}%**. Net saving **{Q.SAVE * 100:.1f}%**.",
    f"Value the builder's remaining days at **{inr(DAY)} per day** ({inr(DAY / 8)} per hour; ₹1.25 lakh per month, senior rate within the blueprint band of ₹1.0–1.5 lakh).",
    "Add the **builder's tools**, but only for the months each is needed (§6.1). Add **Claude API tokens** for the coding agents, reduced 20% by prompt caching and use of the Haiku model. Add **10% contingency** on time and tokens.",
    f"Round up to the optimized fee of {inr(FEE_OPT)}. Then apply the **package discount** of {inr(DISCOUNT)}, so that development, retainer and running costs together make **₹90,00,000**.",
]:
    A(f"- {s}")
A("")
A("## 4.2 Price build-up\n")
table(["Component", "Core platform", "Advanced A1", "Total", "Formula"], [
    ["Traditional effort (person-days)", f"{C['trad']:,.0f}", f"{A1['trad']:,.0f}", f"{C['trad'] + A1['trad']:,.0f}", "Blueprint (Parts 8.4, 9.10)"],
    ["Builder's effort with AI (person-days)", f"{C['pd']:,.0f}", f"{A1['pd']:,.0f}", f"{C['pd'] + A1['pd']:,.0f}", f"Traditional × (1 − {Q.SAVE:.3f})"],
    ["Builder's hours", f"{C['pd'] * 8:,.0f}", f"{A1['pd'] * 8:,.0f}", f"{(C['pd'] + A1['pd']) * 8:,.0f}", "Days × 8"],
    ["Duration (months)", f"{C['months']:.1f}", f"{A1['months']:.1f}", f"{MONTHS:.1f}", f"Days ÷ {Q.PROD_DAYS} productive days"],
    ["Builder's time", lakh(C["labour"]), lakh(A1["labour"]), lakh(C["labour"] + A1["labour"]), f"Days × {inr(DAY)}"],
    ["Builder's tools (optimized durations, §6.1)", lakh(C["tools"]), lakh(A1["tools"]), lakh(C["tools"] + A1["tools"]), "$/month × months used × ₹90"],
    ["Claude API tokens for coding agents (−20% optimization)", lakh(C["tokens"]), lakh(A1["tokens"]), lakh(C["tokens"] + A1["tokens"]), f"Agent-days ({C['agent_pd']:,.0f} + {A1['agent_pd']:,.0f}) × ${Q.USD_PD:.2f} × ₹90 × 0.8"],
    ["Contingency", lakh(C["cont"]), lakh(A1["cont"]), lakh(C["cont"] + A1["cont"]), "10% × (time + tokens)"],
    ["**Cost basis**", f"**{lakh(C['cost'])}**", f"**{lakh(A1['cost'])}**", f"**{lakh(COST)}**", ""],
    ["Optimized fee", "", "", lakh(FEE_OPT), "Cost basis rounded up"],
    ["Package discount", "", "", f"− {lakh(DISCOUNT)}", "To reach the ₹90,00,000 package"],
    ["**Fixed development fee (A)**", f"**{lakh(FEE_CORE)}**", f"**{lakh(FEE_A1)}**", f"**{lakh(FEE)}**", "Split pro rata to cost basis"],
])
A(f"**Effect of the discount.** The discount uses about {DISCOUNT / (C['cont'] + A1['cont']) * 100:.0f}% of the contingency; {inr(C['cont'] + A1['cont'] - DISCOUNT)} remains. Scope is therefore frozen at the blueprint and changed only by written change request at the day rate.\n")
A("## 4.3 Effort by activity (builder's days)\n")
rows = []
for (n, t, s), (n2, t2, s2) in zip(C["rows"], A1["rows"]):
    rows.append([n, f"{t:,.0f}" if t else "—", f"{s:,.0f}", f"{t2:,.0f}" if t2 else "—", f"{s2:,.0f}", f"{s + s2:,.0f}", lakh((s + s2) * DAY)])
rows.append(["**Total**", f"**{C['trad']:,.0f}**", f"**{C['pd']:,.0f}**", f"**{A1['trad']:,.0f}**", f"**{A1['pd']:,.0f}**", f"**{C['pd'] + A1['pd']:,.0f}**", f"**{lakh((C['pd'] + A1['pd']) * DAY)}**"])
table(["Activity", "Core: traditional pd", "Core: solo with AI pd", "A1: traditional pd", "A1: solo with AI pd", "Total solo pd", "Value"], rows, [30, 7, 7, 7, 7, 7, 8])
A("Activities include user-story drafting, test strategy and test-case drafting. The blueprint already contains drafts of all 461 stories and 4,156 test cases, and the builder refines them with AI assistance.\n")
A(S44)
A("## 4.5 How the package was optimized and discounted\n")
table(["Lever", "Saving"], [
    ["Builder tools trimmed (BrowserStack 6 months, Figma 12 months, client's own Workspace)", "₹2,06,000"],
    ["Claude tokens cut ≈ 20% (prompt caching, Haiku for simple tasks)", "₹81,000"],
    ["Contingency 15% → 10% (fully specified scope, change control)", "₹2,84,000"],
    ["Penetration tests 3 → 2 (combined Release 2 + A1 test)", "₹3,25,000"],
    ["Staging-only hosting until Release 1", "₹3,06,000"],
    ["Pilot running without team seats, delivery AI line and integration reserve; free monitoring tiers", "₹2,10,000"],
    ["Year 1: point-in-time recovery deferred to the growth gate; maintainer seat inside the retainer", "₹2,70,000"],
    ["Retainer ₹65,000 → ₹55,000 per month", "₹1,20,000"],
    ["Package discount on the development fee", inr(DISCOUNT)],
    [f"**Total reduction from ≈ {inr(BEFORE_OPT)}**", f"**{inr(BEFORE_OPT - PACKAGE)}**"],
])

A(S5)

A("# 6. Subscriptions: while building and while using the application\n")
A("## 6.1 While building (USD list prices; verify)\n")
rows = []
for name, m, mc, ma, note in OPT_TOOLS:
    rows.append([name, usd(m), f"{mc:.1f}", f"{ma:.1f}", inr(m * (mc + ma) * FX), note, "Builder (in fee A)"])
rows.append(["Claude API tokens for coding agents", f"≈ {usd((C['tokens'] + A1['tokens']) / FX / MONTHS)} average, capped at $300", f"{C['months']:.1f}", f"{A1['months']:.1f}", inr(C["tokens"] + A1["tokens"]), "Headless/parallel agents in CI", "Builder (in fee A)"])
for name, v in STAGING:
    rows.append([name, usd(v), "15", "—", inr(v * 15 * FX), "Staging until Release 1, then production (C3)", "Client (C2)"])
rows.append(["Sentry, Langfuse, open-source toolchain (Playwright, pytest, k6, OWASP ZAP, Trivy, Semgrep, axe-core, Bitwarden)", "$0", "—", "—", "₹0", "Free tiers / self-hosted", "—"])
table(["Subscription", "Per month", "Months (Core)", "Months (A1)", "Total over the build (INR)", "Note", "Paid by"], rows, [22, 10, 6, 6, 10, 18, 9])
A(f"Builder's tools and tokens in fee A: **{inr(C['tools'] + A1['tools'] + C['tokens'] + A1['tokens'])}**. Client staging hosting (C2): **{inr(STAGING_M * 15)}**.\n")
A("## 6.2 While using the application (pilot; per month; client-owned)\n")
rows = [[r[0], r[2], r[3], f"{inr(r[4])}–{inr(r[5])}" if r[5] != r[4] else inr(r[4]), f"{usd(r[4] / FX)}–{usd(r[5] / FX)}" if r[5] != r[4] else usd(r[4] / FX), r[6]] for r in RUN_LINES]
rows.append(["", "**Subtotal**", "", f"**{inr(R_LO)}–{inr(R_HI)}**", f"**{usd(R_LO / FX)}–{usd(R_HI / FX)}**", ""])
rows.append(["B11", "Contingency 15%", "", f"{inr(R_LO * 0.15)}–{inr(R_HI * 0.15)}", "", ""])
rows.append(["", "**Pilot running (C3), per month**", "", f"**{inr(PIL_LO)}–{inr(PIL_HI)}**", f"**{usd(PIL_LO / FX)}–{usd(PIL_HI / FX)}**", "From Release 1 go-live"])
rows.append(["A1", "Advanced A1 feature running additions (agent observability, signal and experimentation stores, extra jobs)", "Usage", f"{inr(A1ADD[0])}–{inr(A1ADD[1])}", f"{usd(A1ADD[0] / FX)}–{usd(A1ADD[1] / FX)}", "From A1 go-live"])
rows.append(["", "**Running after full go-live (C4), per month**", "", f"**{inr(PIL_LO + A1ADD[0])}–{inr(PIL_HI + A1ADD[1])}**", f"**{usd((PIL_LO + A1ADD[0]) / FX)}–{usd((PIL_HI + A1ADD[1]) / FX)}**", ""])
table(["Line", "Subscription / service", "Billing", "Per month (INR)", "Per month (USD)", "Active from"], rows, [5, 34, 12, 12, 10, 12])
A("Removed from the client's running cost by optimization:")
A("- the team Claude seats (B09), because the builder's Claude is in the fee and the maintainer's is in the retainer;")
A("- the delivery-team AI line (B23), which is in the fee;")
A("- the integration reserve (B10), added only when a pilot is approved;")
A("- paid synthetic probes (B07+), replaced by free tiers.\n")
ag = [i for i in Q.IN if i["kind"] == "AG"]
A(f"**Production AI usage.** The {len(ag)} AI agents in scope cost about **{inr(sum(i['run_base'] for i in ag))} per month** at pilot volume, or ≈ {inr(sum(i['run_base'] for i in ag) * 1.25)} with a 25% overhead. They use Claude, with Sonnet as the primary model. Hard caps in the gateway (₹3,000 core + ₹2,000 advanced per month) stop paid calls at the limit, and work then degrades safely.\n")
A("**As the business grows.** At the growth gate running is about ₹59,000–79,000 per month, including Supabase point-in-time recovery; at scale about ₹1.39–1.79 lakh per month (DEC-422). These apply only when measured business results pass the blueprint's scale gates. External SaaS tenants pay for their own usage through their plans.\n")
A("**Optional or conditional:** Apollo enrichment (≈ ₹10,350/month, only after the scale gate), Supabase point-in-time recovery (≈ ₹9,000/month, from the growth gate), e-signature (per envelope), payment-gateway fees (≈ 2% of collections), paid advertising (campaign budgets).\n")

A("# 7. Pass-through costs (billed at actuals)\n")
table(["Item", "Estimate", "In the package?", "Why separate"], [
    ["Independent penetration tests (C1)", "₹4,00,000 – ₹9,00,000 (₹6,50,000 used)", "Yes, as estimate", "Security must be certified by an independent tester"],
    ["Hosting and running (C2–C4)", "§6", "Yes, as estimate", "Client owns production accounts and data"],
    ["External legal counsel (DPDP, children's data, contracts)", "As quoted by counsel (indicatively ₹1.5–5 lakh)", "No", "Legal advice is outside the builder's scope"],
    ["Business costs (data purchases, advertising, payment-gateway fees)", "As used", "No", "Not platform build costs"],
])

A("# 8. Timeline and payment milestones\n")
ms = [("Contract signing (mobilisation)", 0.10, 0), ("Foundation gate: environments, identity, tenancy, model gateway", 0.10, 3),
      ("Release 1 functional complete (UAT start)", 0.15, 12), ("Release 1 go/no-go passed", 0.15, 15),
      ("Release 2 build gate passed", 0.15, round(C["months"]) - 1), ("30-day monitored pilot completed", 0.10, round(C["months"]) + 1),
      ("Advanced A1 mid-point demo", 0.10, round(C["months"] + A1["months"] / 2)), ("Advanced A1 go-live and acceptance", 0.15, round(MONTHS))]
table(["Milestone (fee A)", "Indicative month from start", "Share", "Amount (excl. GST)", "Amount (incl. GST)"],
      [[m, f"Month {mo}", f"{s * 100:.0f}%", inr(FEE * s), inr(FEE * s * (1 + GST))] for m, s, mo in ms] + [["**Total fee A**", "", "**100%**", f"**{inr(FEE)}**", f"**{inr(FEE * (1 + GST))}**"]])
A(f"The retainer (B) is billed monthly from go-live at {inr(RETAINER_M)} + GST. C1–C4 are paid by the client to the providers as incurred.\n")
A(f"**Important.** One builder needs about {MONTHS:.0f} months; an AI-assisted team would need about 12–13. If an earlier date matters more than price, the scope can be phased or contract engineers added under a revised quotation. Progress is reported monthly with measured throughput. If AI productivity is materially better than assumed, the remaining milestones move earlier at no extra cost, and the client pays less running cost during the build.\n")

A("# 9. Maintenance and support retainer\n")
A(f"**{inr(RETAINER_M)} + GST per month** from go-live, renewable yearly. It covers:\n")
A("- bug fixes, security patches and dependency upgrades;")
A("- Claude model-version migrations with re-evaluation;")
A("- monitoring and business-hours incident response;")
A("- a quarterly DR drill;")
A("- up to 6 days of small changes per month.\n")
A("The maintainer's Claude seat and GitHub are included. Larger changes are quoted at the day rate.\n")
A(f"**After the first year:** about **{inr(PIL + sum(A1ADD) / 2)} per month running + {inr(RETAINER_M)} per month maintenance** (plus GST).\n")

A("# 10. Future options (indicative, not part of this package)\n")
a2, a3 = 518 * (1 - Q.SAVE), 283 * (1 - Q.SAVE)
tool_m = 204 * FX
table(["Option", "Builder's effort (days)", "Indicative fee (excl. GST)", "Duration"], [
    ["Advanced A2: NBA, deal risk, ABM, intent hub, deal rooms, partners, QBR, semantic layer, NL analytics", f"{a2:,.0f}", lakh(a2 * DAY * 1.10 + a2 / Q.PROD_DAYS * tool_m), f"≈ {a2 / Q.PROD_DAYS:.0f} months"],
    ["Advanced A3 (after the scale gate): conversation intelligence, marketing mix, no-code builder, developer platform", f"{a3:,.0f}", lakh(a3 * DAY * 1.10 + a3 / Q.PROD_DAYS * tool_m), f"≈ {a3 / Q.PROD_DAYS:.0f} months"],
])

A("# 11. Why the buyer can trust this price\n")
for s in [
    "**Specified before priced.** The scope is defined in a 4,746-page blueprint: 461 user stories, 4,156 test cases, 579 API operations, 80 AI agents and 346 recorded decisions. Nothing is priced on guesswork.",
    "**Every number is traceable** to the blueprint's effort, the published AI-built factors and list prices, with formulas shown in §4 and §6.",
    f"**Cheaper than the alternatives.** The development fee ({lakh(FEE)}) is about {(1 - FEE / 8_510_000) * 100:.0f}% below an AI-assisted team ({lakh(8_510_000)}) and {(1 - FEE / 11_617_100) * 100:.0f}% below a traditional team ({lakh(11_617_100)}) for the same scope.",
    "**Safety does not depend on trust in AI.** Consequential actions always need a person, and policy is rechecked at dispatch. AI cost caps are hard, penetration tests are independent, and every AI-generated change gets human review.",
    "**The client owns everything:** code, infrastructure, data, accounts and IP on full payment.",
    "**Fixed price with milestones tied to evidence.** The client pays as gates are passed, not for time spent.",
]:
    A(f"- {s}")
A("")

A("# 12. Assumptions and terms\n")
for i, t in enumerate([
    "Scope is the Application Blueprint v1.1 (Core + Advanced A1) as of 28 Nov 2026; changes by written change request at the day rate.",
    f"The builder's time is valued at ₹1.25 lakh per month ({inr(DAY)} per day; {inr(DAY / 8)} per hour), with {Q.PROD_DAYS} productive days per month.",
    f"AI productivity is the central case of Cost Estimate v1.1 plus 4% for solo working (net {Q.SAVE * 100:.1f}%). These are planning assumptions; measured progress is reported monthly.",
    "Claude Sonnet is the primary production model (DEC-418). Hosting is Vercel + Supabase + AWS Mumbai (DEC-421); the running budget is DEC-422.",
    "C1–C4 are estimates at list prices as of 28 Nov 2026 and are paid at actuals; provider price changes pass through.",
    "The client provides timely approvals, UAT users, provider accounts (AWS, Supabase, Vercel, Anthropic, Meta) and legal confirmations.",
    "Build agents use synthetic data only; no production personal data is shared with them.",
    "GST at 18% applies to all fees; pass-through items carry the providers' own taxes.",
], 1):
    A(f"{i}. {t}")
A("")
for t in ["**Price type:** fixed price for A and B; C1–C4 at actuals.", "**Intellectual property:** transferred to the client on full payment.",
          "**Warranty:** 60 days after each go-live for defects against acceptance criteria.", "**Confidentiality:** all client data and documents are confidential.",
          "**Payment terms:** invoices payable within 15 days of milestone acceptance.", "**Validity:** 30 days."]:
    A(f"- {t}")
A("\n**Acceptance**\n")
table(["For the client", "For the builder"], [["Name: ______________________", "Name: ______________________"], ["Signature: __________________", "Signature: __________________"], ["Date: ______________________", "Date: ______________________"]])

(OUT / f"{NAME}.md").write_text("\n".join(L) + "\n", encoding="utf-8")
print("fee", round(FEE), "core", round(FEE_CORE), "a1", round(FEE_A1), "discount", round(DISCOUNT), "cost", round(COST), "at_cost", round(AT_COST), "pil", round(PIL_LO), round(PIL_HI))

if __name__ == "__main__":
    env = {**os.environ, "LANG": "C.UTF-8", "LC_ALL": "C.UTF-8"}
    subprocess.run([str(Q.BP / "make_pdf.sh"), f"{NAME}.md", "Final Cost Sheet v1.1 · 28 Nov 2026 · Confidential"], cwd=OUT, check=True, env=env)
    import build_docx
    build_docx.build(OUT / f"{NAME}.md", OUT / f"{NAME}.docx", header="AI Growth Engine — Final Cost Sheet v1.1 (solo builder with AI)    |    Confidential · 28 Nov 2026",
                     title="AI Growth Engine: Final Cost Sheet", subtitle="Optimized, discounted all-inclusive package: Core + Advanced A1, solo builder with AI (INR)",
                     version="Cost sheet v1.1 · 28 Nov 2026 · Valid for 30 days")
