#!/usr/bin/env python3
"""Cost estimate v1.1: building the application with AI models and AI agents, compared side by side with the traditional build.

Usage: python3 blueprint/estimation/build_ai_estimate.py
Outputs: blueprint/final/estimation/AI_Growth_Engine_Cost_Estimate_v1.1_AI_Built.{md,pdf,docx,xlsx}
"""
import datetime as dt
import os
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import build_estimate as BE  # noqa: E402  (recomputes the traditional v1.0 model)
import ai_model as X  # noqa: E402
import model as M  # noqa: E402

OUT = BE.OUT
IMG = BE.IMG
NAME = "AI_Growth_Engine_Cost_Estimate_v1.1_AI_Built"
ind, inr, lakh, usd, usdv, rng = BE.ind, BE.inr, BE.lakh, BE.usd, BE.usdv, BE.rng
P = BE.P

DOC = []
A = DOC.append


def table(header, rows, widths=None):
    A("| " + " | ".join(header) + " |")
    A("|" + "|".join("-" * max(3, w) for w in (widths or [3] * len(header))) + "|")
    for r in rows:
        A("| " + " | ".join(str(c).replace("|", "/").replace("\n", " ") for c in r) + " |")
    A("")


# ---------------------------------------------------------------- core arithmetic
SHARES = {name: share for name, share, _ in M.ACTIVITY_SPLIT}
CI = {"optimistic": 1, "central": 2, "conservative": 3}


def reduction(case):
    return sum(SHARES[a[0]] * a[CI[case]] for a in X.ACCEL)


def overhead(case):
    return sum(o[CI[case]] for o in X.OVERHEAD)


SAVE = {c: reduction(c) - overhead(c) for c in X.CASES}
AGENT_SHARE = sum(SHARES[a[0]] * a[4] for a in X.ACCEL)
USD_PD = X.usd_per_agent_pd()

# people share of each package (CORE has external vendors that AI does not change)
la = BE.la
core_people = (sum(r["pm"] for r in la) * M.PM_RATE[0], sum(r["pm"] for r in la) * M.PM_RATE[1])
core_vendor = (sum(r["lo"] for r in la if not r["pm"]), sum(r["hi"] for r in la if not r["pm"]))


def split(key):
    """(people low, central, high), (vendor low, central, high) for a package."""
    lo, c, hi = P[key][3], P[key][4], P[key][5]
    if key == "CORE":
        pl, ph = core_people
        vl, vh = core_vendor
        return (pl, (pl + ph) / 2, ph), (vl, (vl + vh) / 2, vh)
    return (lo, c, hi), (0, 0, 0)


AI = {}
for key in [p[0] for p in M.PACKAGES]:
    (pl, pc, ph), (vl, vc, vh) = split(key)
    eff = P[key][6]
    e = (eff[0] if eff[0] is not None else eff[1], eff[1], eff[2] if eff[2] is not None else eff[1])
    AI[key] = dict(
        trad=(P[key][3], P[key][4], P[key][5]), trad_eff=e,
        people=(pl, pc, ph), vendor=(vl, vc, vh),
        ai=(pl * (1 - SAVE["optimistic"]) + vl, pc * (1 - SAVE["central"]) + vc, ph * (1 - SAVE["conservative"]) + vh),
        ai_eff=(e[0] * (1 - SAVE["optimistic"]), e[1] * (1 - SAVE["central"]), e[2] * (1 - SAVE["conservative"])),
        agent_pd=(e[0] * AGENT_SHARE, e[1] * AGENT_SHARE, e[2] * AGENT_SHARE),
    )
    a = AI[key]
    a["tokens_usd"] = (a["agent_pd"][0] * USD_PD * X.TOKEN_MULT["optimistic"], a["agent_pd"][1] * USD_PD * X.TOKEN_MULT["central"], a["agent_pd"][2] * USD_PD * X.TOKEN_MULT["conservative"])

approved = ["CORE", "ALN", "A1"]
optional = ["PH2", "A2", "A3"]
allk = approved + optional


def tot(keys, field):
    return tuple(sum(AI[k][field][i] for k in keys) for i in range(3))


# tooling per month (USD)
dec419_nonclaude = [r for r in BE.tool_rows if "Claude" not in r["name"] and not r["req"].startswith("Optional")]
nonclaude = (sum(r["mlo"] for r in dec419_nonclaude), sum(r["mhi"] for r in dec419_nonclaude))
trad_claude = 40 + 600 + 20
trad_tools = (trad_claude + nonclaude[0], trad_claude + nonclaude[1])
ai_tools_rows = [dict(name=n, purpose=p, ulo=lo, uhi=hi, seats=s, note=no, after=af, mlo=lo * s, mhi=hi * s, alo=lo * af, ahi=hi * af) for n, p, lo, hi, s, no, af in X.AI_TOOLS]
ai_tools = (sum(r["mlo"] for r in ai_tools_rows) + nonclaude[0], sum(r["mhi"] for r in ai_tools_rows) + nonclaude[1])
nonclaude_after = (sum(r["alo"] for r in dec419_nonclaude), sum(r["ahi"] for r in dec419_nonclaude))
ai_tools_after = (sum(r["alo"] for r in ai_tools_rows) + nonclaude_after[0], sum(r["ahi"] for r in ai_tools_rows) + nonclaude_after[1])

# ---------------------------------------------------------------- timeline option B (same team, earlier)
DAY1 = dt.date(2026, 12, 7)


def day(n):
    d = DAY1 + dt.timedelta(days=round(n) - 1)
    return d.strftime("%a %d %b %Y")


def r1_day(s):
    return 30 * 0.85 + (150 - 20) * (1 - s) + 20


TL = {}
for c in X.CASES:
    s = SAVE[c]
    r1 = r1_day(s)
    r2 = r1 + 28 * (1 - s)
    w5 = r2 + 21
    a1s = w5 + 10
    a1e = a1s + 127 * (1 - s)
    a2e = a1e + 115 * (1 - s)
    a3e = a2e + 120 * (1 - s)
    TL[c] = dict(r1=r1, r2=r2, w5=w5, a1s=a1s, a1e=a1e, a2e=a2e, a3e=a3e)

# ---------------------------------------------------------------- TCO (AI-built), mirrors the traditional structure
def fp_ai():
    lo = hi = 0
    for name, basis, l_, h_, kind in M.FUTURE:
        if kind == "pd":
            lo += l_ * M.PD_RATE[0] * (1 - SAVE["optimistic"])
            hi += h_ * M.PD_RATE[1] * (1 - SAVE["conservative"])
        elif kind == "inr":
            lo += l_
            hi += h_
        elif kind == "fx":
            lo += 0.05 * ai_tools[0] * 12 * M.FX
            hi += 0.05 * ai_tools[1] * 12 * M.FX
    return lo, hi


FP_AI = fp_ai()


def tco_ai(path):
    years = []
    tok0 = [AI["CORE"]["tokens_usd"][0] + AI["ALN"]["tokens_usd"][0], AI["CORE"]["tokens_usd"][2] + AI["ALN"]["tokens_usd"][2]]
    y0_dev = [AI["CORE"]["ai"][0] + AI["ALN"]["ai"][0], AI["CORE"]["ai"][2] + AI["ALN"]["ai"][2]]
    y0_run = [BE.B_DURING_BUILD[0] + 2 * BE.aln_run[0] + BE.runs_lo, BE.B_DURING_BUILD[1] + 2 * BE.aln_run[1] + BE.runs_hi]
    y0_tools = [ai_tools[0] * 8 * M.FX + tok0[0] * M.FX, ai_tools[1] * 8 * M.FX + tok0[1] * M.FX]
    years.append(("Year 0 (build): Dec 2026 – Jul 2027", y0_dev, y0_run, y0_tools, [0, 0], [0, 0]))
    k1 = [k for k in path if k in ("A1", "A2", "A3", "PH2")]
    y1_dev = [sum(AI[k]["ai"][0] for k in k1), sum(AI[k]["ai"][2] for k in k1)]
    tok1 = [sum(AI[k]["tokens_usd"][0] for k in k1), sum(AI[k]["tokens_usd"][2] for k in k1)]
    y1_run = [0, 0]
    for m in BE.months[8:]:
        r = BE.run_month(m, path)
        y1_run = [y1_run[0] + r[0], y1_run[1] + r[2]]
    y1_tools = [ai_tools[0] * 12 * M.FX + tok1[0] * M.FX, ai_tools[1] * 12 * M.FX + tok1[1] * M.FX]
    cum = [y0_dev[0], y0_dev[1]]
    y1_m = [X.MAINT_PCT_AI[0] * cum[0], X.MAINT_PCT_AI[1] * cum[1]]
    years.append(("Year 1: Aug 2027 – Jul 2028", y1_dev, y1_run, y1_tools, y1_m, list(FP_AI)))
    cum = [cum[0] + y1_dev[0], cum[1] + y1_dev[1]]
    share = 1.0 if "A3" in path else 0.35
    esc = 1.08
    y2_run = [(50_000 + share * BE.adv_lo + BE.aln_run[0]) * 12, (70_000 + share * BE.adv_hi + BE.aln_run[1]) * 12]
    maint_tools = [(ai_tools_after[0]) * 12 * M.FX, (ai_tools_after[1]) * 12 * M.FX]
    years.append(("Year 2: Aug 2028 – Jul 2029 (growth gate)", [0, 0], y2_run, maint_tools, [X.MAINT_PCT_AI[0] * cum[0] * esc, X.MAINT_PCT_AI[1] * cum[1] * esc], [FP_AI[0] * esc, FP_AI[1] * esc]))
    y3_run = [(130_000 + share * BE.adv_lo + BE.aln_run[0]) * 12, (170_000 + share * BE.adv_hi + BE.aln_run[1]) * 12]
    years.append(("Year 3: Aug 2029 – Jul 2030 (scale design point)", [0, 0], y3_run, maint_tools, [X.MAINT_PCT_AI[0] * cum[0] * esc ** 2, X.MAINT_PCT_AI[1] * cum[1] * esc ** 2], [FP_AI[0] * esc ** 2, FP_AI[1] * esc ** 2]))
    return years


TCO_AI_AP = tco_ai(approved)
TCO_AI_FULL = tco_ai(approved + ["A2", "A3", "PH2"])
tt = BE.tco_total

# catalogue under AI build
CAT = BE.cat
for i in CAT:
    i["ai_pd_lo"] = i["pd_lo"] * (1 - SAVE["optimistic"])
    i["ai_pd_hi"] = i["pd_hi"] * (1 - SAVE["conservative"])
    i["ai_cost_lo"] = i["ai_pd_lo"] * M.PD_RATE[0]
    i["ai_cost_hi"] = i["ai_pd_hi"] * M.PD_RATE[1]
    i["build_mode"] = {"AG": "Coding agent scaffolds the agent, prompt contract and eval set; AI engineer owns guardrails and thresholds",
                       "AU": "Coding agent implements rules and tests from the rule table; engineer reviews",
                       "WF": "Coding agents build steps and screens; engineers design orchestration, approval gates and review"}[i["kind"]]


# ---------------------------------------------------------------- charts
def charts():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    navy, teal, grey, amber = "#0b3d6b", "#2a9d8f", "#9aa5b1", "#e9a23b"
    keys = allk
    short = {"CORE": "Core build", "ALN": "Alignment", "A1": "Advanced A1", "PH2": "Phase 2", "A2": "Advanced A2", "A3": "Advanced A3"}
    fig, ax = plt.subplots(figsize=(10, 4.2), dpi=150)
    x = range(len(keys))
    ax.bar([i - 0.2 for i in x], [AI[k]["trad"][1] / M.L for k in keys], 0.4, color=grey, label="Traditional build (central)")
    ax.bar([i + 0.2 for i in x], [AI[k]["ai"][1] / M.L for k in keys], 0.4, color=navy, label="AI-built (central)")
    for i, k in enumerate(keys):
        ax.text(i + 0.2, AI[k]["ai"][1] / M.L + 1, f"{AI[k]['ai'][1] / M.L:.1f}", ha="center", fontsize=8)
        ax.text(i - 0.2, AI[k]["trad"][1] / M.L + 1, f"{AI[k]['trad'][1] / M.L:.1f}", ha="center", fontsize=8)
    ax.set_xticks(list(x)); ax.set_xticklabels([short[k] for k in keys])
    ax.set_ylabel("₹ lakh (one-time development)"); ax.set_title("Traditional vs AI-built: one-time development cost by package (central)")
    ax.legend(); ax.grid(axis="y", alpha=0.3); fig.tight_layout(); fig.savefig(IMG / "ai_vs_trad.png"); plt.close(fig)
    fig, ax = plt.subplots(figsize=(10, 3.6), dpi=150)
    labels = [a[0].split(" (")[0][:34] for a in X.ACCEL]
    ax.barh(range(len(labels)), [a[2] * 100 for a in X.ACCEL], color=teal)
    ax.set_yticks(range(len(labels))); ax.set_yticklabels(labels, fontsize=8); ax.invert_yaxis()
    ax.set_xlabel("Effort reduction with AI agents, central case (%)"); ax.set_title("Where AI agents save effort (before oversight overheads)")
    ax.grid(axis="x", alpha=0.3); fig.tight_layout(); fig.savefig(IMG / "ai_accel.png"); plt.close(fig)


charts()

ap_t, ap_a = tot(approved, "trad"), tot(approved, "ai")
all_t, all_a = tot(allk, "trad"), tot(allk, "ai")
tok_ap, tok_all = tot(approved, "tokens_usd"), tot(allk, "tokens_usd")

# ---------------------------------------------------------------- document
A("# AI Growth Engine: Cost Estimate v1.1, Building the Application with AI Models and AI Agents")
A("## Traditional build vs AI-built: side-by-side costs in INR and USD")
A("")
table(["Field", "Value"], [
    ["Document", "Cost Estimate v1.1 (AI-built variant). Companion to Cost Estimate v1.0 (traditional build)"],
    ["Date", "28 Nov 2026"],
    ["Basis", "Application Blueprint v1.1; approved budgets DEC-230/231; Founder decisions DEC-416…419 (DEC-419: build-time tooling approved)"],
    ["Currency", f"INR and USD at ₹{M.FX:.0f} = $1 (verify). Amounts exclude GST"],
    ["What changes", "**Only how the software is built.** AI models and AI agents draft, code, test and document under human supervision. **The application itself, its features, its 80 production AI agents and its running costs do not change**"],
    ["Status", "**Approved approach (DEC-420, 28 Nov 2026):** AI-built delivery from Sprint 0, with a **Sprint 2 calibration gate (≈ Day 45)**. Team, dates and Ledger A stay as approved until the gate (§12)"],
])
A("**Bifurcation used throughout.** Every table separates four things:\n")
A("- **(1) one-time development** (people and vendors);")
A("- **(2) build-time subscriptions and AI usage** (tools and tokens used to build);")
A("- **(3) recurring running cost of the application** (cloud, AI inference, providers);")
A("- **(4) lifecycle cost** (maintenance and future-proofing).\n")
A("Each one is shown for the **traditional build** and the **AI-built** approach.\n")

A("# 1. Executive summary\n")
A("## 1.1 Side-by-side totals\n")
rows = []
for k in allk:
    t, a = AI[k]["trad"], AI[k]["ai"]
    rows.append([P[k][1], P[k][2], rng(t[0], t[2]), lakh(t[1]), rng(a[0], a[2]), lakh(a[1]), lakh(t[1] - a[1]), f"{(t[1] - a[1]) / t[1] * 100:.0f}%", usd(a[1])])
rows.append(["**Approved scope (core + alignment + A1)**", "Approved", f"**{rng(ap_t[0], ap_t[2])}**", f"**{lakh(ap_t[1])}**", f"**{rng(ap_a[0], ap_a[2])}**", f"**{lakh(ap_a[1])}**", f"**{lakh(ap_t[1] - ap_a[1])}**", f"**{(ap_t[1] - ap_a[1]) / ap_t[1] * 100:.0f}%**", f"**{usd(ap_a[1])}**"])
rows.append(["**Full programme (all options)**", "Approved + optional", f"**{rng(all_t[0], all_t[2])}**", f"**{lakh(all_t[1])}**", f"**{rng(all_a[0], all_a[2])}**", f"**{lakh(all_a[1])}**", f"**{lakh(all_t[1] - all_a[1])}**", f"**{(all_t[1] - all_a[1]) / all_t[1] * 100:.0f}%**", f"**{usd(all_a[1])}**"])
table(["(1) One-time development", "Status", "Traditional range", "Traditional central", "AI-built range", "AI-built central", "Saving (central)", "Saving %", "AI-built central (USD)"], rows, [26, 12, 14, 9, 14, 9, 9, 6, 9])
A("![Traditional vs AI-built](img/ai_vs_trad.png)\n")
table(["(2) Build-time subscriptions and AI usage", "Traditional (DEC-419)", "AI-built", "Difference"], [
    ["Tools and seats per month (all Claude seats + GitHub, Figma, Workspace, Bitwarden, BrowserStack, domains)", f"{rng(*trad_tools, usdv)} ({rng(trad_tools[0] * M.FX, trad_tools[1] * M.FX, inr)})", f"{rng(*ai_tools, usdv)} ({rng(ai_tools[0] * M.FX, ai_tools[1] * M.FX, inr)})", f"+ {rng(ai_tools[0] - trad_tools[0], ai_tools[1] - trad_tools[1], usdv)} per month"],
    ["AI-agent token usage (Claude API for headless/parallel coding agents), approved scope", "≈ $0 (interactive seats only)", f"{rng(tok_ap[0], tok_ap[2], usdv)} total (central {usdv(tok_ap[1])}) ≈ {rng(tok_ap[0] * M.FX, tok_ap[2] * M.FX)}", f"+ {rng(tok_ap[0], tok_ap[2], usdv)}"],
    ["AI-agent token usage, full programme", "≈ $0", f"{rng(tok_all[0], tok_all[2], usdv)} total (central {usdv(tok_all[1])})", ""],
])
table(["(3) Recurring running cost of the application", "Traditional", "AI-built"], [
    ["Pilot running per month after launch (approved Ledger B with contingency and seats)", rng(BE.runs_lo, BE.runs_hi, inr), "Same: **unchanged**"],
    ["All-in after the full advanced roadmap", rng(BE.runs_lo + BE.add_lo, BE.runs_hi + BE.add_hi, inr), "Same: **unchanged**"],
    ["Production AI inference by the application's 80 agents (Claude Sonnet primary)", f"≈ {inr(BE.ag_run[1])}/month base, capped", "Same: **unchanged**"],
])
ta_t, tf_t = tt(BE.tco_ap), tt(BE.tco_full)
ta_a, tf_a = tt(TCO_AI_AP), tt(TCO_AI_FULL)
table(["(4) Three-year total cost of ownership (build + 3 years)", "Traditional", "AI-built", "Saving"], [
    ["Approved path", rng(*ta_t), rng(*ta_a), f"{lakh(ta_t[0] - ta_a[0])} at the low end; {lakh(ta_t[1] - ta_a[1])} at the high end"],
    ["Full roadmap", rng(*tf_t), rng(*tf_a), f"{lakh(tf_t[0] - tf_a[0])} at the low end; {lakh(tf_t[1] - tf_a[1])} at the high end"],
    ["(USD) Approved path", rng(*ta_t, usd), rng(*ta_a, usd), ""],
    ["(USD) Full roadmap", rng(*tf_t, usd), rng(*tf_a, usd), ""],
])
A("A negative saving means the AI-built approach costs more. That happens only in the conservative case: the AI tooling continues for three years while the productivity gain stays small. This is why a calibration gate is recommended before the team is changed.\n")
A("## 1.2 What this means\n")
A(f"- **Net effort saving on people:** {SAVE['central'] * 100:.0f}% in the central case. The optimistic case is {SAVE['optimistic'] * 100:.0f}% and the conservative case {SAVE['conservative'] * 100:.0f}%. The saving is net of the new work that AI-built delivery creates: writing specs for agents, reviewing every AI pull request, security and licence checks, and rework.")
A(f"- **On the approved scope**, development falls from **{lakh(ap_t[1])}** to **{lakh(ap_a[1])}** central ({usd(ap_t[1])} → {usd(ap_a[1])}). The saving is about **{lakh(ap_t[1] - ap_a[1])}**.")
A(f"- **The AI cost of building is small.** Extra seats and tools add {rng(ai_tools[0] - trad_tools[0], ai_tools[1] - trad_tools[1], usdv)} per month. Agent tokens for the approved scope are about {usdv(tok_ap[1])} central (up to {usdv(tok_ap[2])} conservative). Both are a fraction of the people saving.")
A("- **External costs do not shrink.** Penetration tests, training content, legal review, provider onboarding, UAT with real users and the 30-day monitored pilot cost the same, and the calendar cannot compress them.")
A(f"- **Two ways to take the benefit.**")
A(f"  - **Option A:** same dates with a smaller team. The team falls from about {X.TRAD_TEAM_PEAK} to about {sum(t[1] for t in X.AI_TEAM):.1f} FTE at peak, and this is the cost view above.")
A(f"  - **Option B:** same team, earlier delivery. Release 1 go/no-go moves to about **{day(TL['central']['r1'])}** (Day {TL['central']['r1']:.0f}) instead of Fri 04 Jun 2027 (§9).")
A("- **The estimate is less certain than the traditional one.** Productivity gains from AI agents vary widely between teams and codebases. A **Sprint 2 calibration gate** measures the real throughput before the plan is locked (§12).\n")

A("# 2. How the application would be built with AI models and AI agents\n")
A("## 2.1 Operating model\n")
table(["Build agent (AI)", "What it does", "Model (Claude family)", "Human owner"], [
    ["Spec and story agent", "Turns blueprint FRs and screen contracts into refined stories, Gherkin AC and task specs", "Sonnet-class; Opus-class for complex specs", "Product Owner"],
    ["Coding agents (Claude Code, interactive and headless)", "Implement APIs, rules, workflows, React screens and migrations against specs and failing tests, in sandboxed branches", "Sonnet-class (bulk), Opus-class (hard problems), Haiku-class (simple edits)", "Senior engineers"],
    ["Test-generation agent", "Writes unit, API and UI tests and test data from AC; maintains traceability", "Sonnet-class", "QA lead"],
    ["Code-review agent", "First-pass review of every pull request: correctness, security, style, test gaps", "Sonnet/Opus-class via API in CI", "Engineering lead (final approval)"],
    ["Security and licence agent", "Runs SAST, dependency, secret and licence scans; explains findings", "Haiku/Sonnet-class + open-source scanners", "Independent reviewer"],
    ["AI-evaluation agent", "Builds and runs the eval sets for the 80 production agents", "Sonnet-class (judge) + deterministic checks", "AI engineer"],
    ["DevOps agent", "Writes IaC, pipelines, dashboards and runbooks", "Sonnet-class", "DevOps engineer"],
    ["Documentation agent", "Drafts runbooks, task cards, release notes, API docs", "Haiku/Sonnet-class", "Feature owners"],
])
A("## 2.2 Guardrails for AI-built software\n")
for g in [
    "Every change goes through a pull request reviewed and merged by a named engineer. Agents cannot merge to protected branches or deploy to production.",
    "Agents work in sandboxed branches and ephemeral environments with synthetic data only. No production data and no personal data reach build agents (DPDP).",
    "No secrets in prompts or repositories. Agent credentials are least-privilege and short-lived.",
    "SAST, dependency, secret and licence scans gate every merge. A provenance log records which agent, model and prompt produced each change.",
    "Test-first: agents implement against acceptance tests written or approved by humans. Coverage and mutation checks are tracked.",
    "Architecture, security design, PDP rules, money handling and AI guardrails stay human-owned. Agents may draft them, but humans decide.",
    "Budget caps on the Claude API keys used by build agents, with alerts at 70/90/100%.",
]:
    A(f"- {g}")
A("")

A("# 3. Assumptions: where AI agents save effort and what they add\n")
A("![Acceleration by activity](img/ai_accel.png)\n")
rows = []
for a in X.ACCEL:
    rows.append([a[0], f"{SHARES[a[0]] * 100:.0f}%", f"{a[1] * 100:.0f}%", f"{a[2] * 100:.0f}%", f"{a[3] * 100:.0f}%", f"{a[4] * 100:.0f}%", a[5], a[6]])
rows.append(["**Weighted reduction**", "100%", f"**{reduction('optimistic') * 100:.1f}%**", f"**{reduction('central') * 100:.1f}%**", f"**{reduction('conservative') * 100:.1f}%**", f"**{AGENT_SHARE * 100:.0f}%**", "", ""])
table(["Activity", "Share of effort", "Reduction optimistic", "Reduction central", "Reduction conservative", "Executed by agents", "What the AI does", "What humans still do"], rows, [20, 5, 6, 6, 6, 6, 24, 24])
rows = [[o[0], f"{o[1] * 100:.1f}%", f"{o[2] * 100:.1f}%", f"{o[3] * 100:.1f}%", o[4]] for o in X.OVERHEAD]
rows.append(["**Total added work**", f"**{overhead('optimistic') * 100:.1f}%**", f"**{overhead('central') * 100:.1f}%**", f"**{overhead('conservative') * 100:.1f}%**", ""])
rows.append(["**Net saving on people effort**", f"**{SAVE['optimistic'] * 100:.1f}%**", f"**{SAVE['central'] * 100:.1f}%**", f"**{SAVE['conservative'] * 100:.1f}%**", "Reduction minus added work"])
table(["New work created by AI-built delivery (% of traditional effort)", "Optimistic", "Central", "Conservative", "What it is"], rows)
A("**Basis.** These are planning assumptions, not measured results. They reflect three things:\n")
A("- this blueprint's unusual completeness: stories, AC, test cases, screen contracts and API field contracts already exist as drafts, which favours AI agents;")
A("- a mature, conventional stack: Django/DRF, React, PostgreSQL;")
A("- the parts that stay human by design: architecture, security, the PDP, money handling and AI guardrails.\n")
A("The low/central/high cost columns pair the traditional low with the optimistic case and the traditional high with the conservative case. The AI-built range is therefore wider than the traditional one.\n")

A("# 4. One-time development: package by package\n")
rows = []
for k in allk:
    a = AI[k]
    rows.append([P[k][1], " / ".join(f"{v:,.0f}" for v in a["trad_eff"]), " / ".join(f"{v:,.0f}" for v in a["ai_eff"]), rng(a["people"][0], a["people"][2]), rng(a["vendor"][0], a["vendor"][2]) if a["vendor"][2] else "—",
                 rng(a["trad"][0], a["trad"][2]), rng(a["ai"][0], a["ai"][2]), rng(a["ai"][0], a["ai"][2], usd)])
table(["Package", "Traditional effort pd (low/central/high)", "AI-built effort pd (opt./central/cons.)", "People cost (traditional)", "Vendor and fixed costs (unchanged)", "Traditional cost", "AI-built cost", "AI-built cost (USD)"], rows)
A("## 4.1 Effort by activity: core build (central)\n")
rows = []
ce = AI["CORE"]["trad_eff"][1]
for a in X.ACCEL:
    tpd = ce * SHARES[a[0]]
    apd = tpd * (1 - a[2])
    rows.append([a[0], f"{tpd:,.0f}", f"{apd:,.0f}", f"{tpd * a[4]:,.0f}", f"{tpd - apd:,.0f}"])
for o in X.OVERHEAD:
    rows.append([f"*Added:* {o[0]}", "—", f"{ce * o[2]:,.0f}", "—", f"−{ce * o[2]:,.0f}"])
rows.append(["**Total**", f"**{ce:,.0f}**", f"**{ce * (1 - SAVE['central']):,.0f}**", f"**{ce * AGENT_SHARE:,.0f}**", f"**{ce * SAVE['central']:,.0f}**"])
table(["Activity", "Traditional pd", "AI-built pd", "Of which agent-executed (pd equivalent)", "Saved pd"], rows)

A("# 5. Team, roles and rates\n")
A("## 5.1 Team for the AI-built option A (same dates)\n")
table(["Role", "FTE at peak", "Responsibility in an AI-built team"], [[r, f"{f:.2f}", d] for r, f, d in X.AI_TEAM] + [["**Total**", f"**{sum(t[1] for t in X.AI_TEAM):.2f}**", f"Traditional peak ≈ {X.TRAD_TEAM_PEAK} FTE"]])
A("## 5.2 Rate card (unchanged)\n")
A(f"Rates are the same as v1.0: loaded {inr(M.HR_RATE[0])}–{inr(M.HR_RATE[1])} per hour ({usd(M.HR_RATE[0], 2)}–{usd(M.HR_RATE[1], 2)}) for India delivery. AI-built teams lean towards senior engineers, because reviewing agent output well needs experience. The rate band already covers senior roles (v1.0 §3).\n")
A("## 5.3 Skills that matter more in an AI-built team\n")
for s_ in ["Writing precise specifications and acceptance tests that agents can implement",
           "Reviewing code quickly and critically; spotting plausible-but-wrong logic",
           "Security review of generated code and dependencies",
           "Prompt and context engineering for coding agents (CLAUDE.md, skills, repository conventions)",
           "Test design and evaluation of AI behaviour"]:
    A(f"- {s_}")
A("")

A("# 6. Build-time subscriptions and AI usage\n")
A("## 6.1 Tools and seats per month\n")
rows = [[r["name"], r["purpose"], f"{usdv(r['ulo'])}–{usdv(r['uhi'])}" if r["uhi"] != r["ulo"] else usdv(r["ulo"]), r["seats"], f"{usdv(r['mlo'])}–{usdv(r['mhi'])}" if r["mhi"] != r["mlo"] else usdv(r["mlo"]),
         f"{inr(r['mlo'] * M.FX)}–{inr(r['mhi'] * M.FX)}" if r["mhi"] != r["mlo"] else inr(r["mlo"] * M.FX), r["note"]] for r in ai_tools_rows]
rows.append(["Other DEC-419 tools (GitHub Team, Figma, Workspace, Bitwarden, BrowserStack, domains)", "Same as the traditional build", "—", "—", rng(*nonclaude, usdv), rng(nonclaude[0] * M.FX, nonclaude[1] * M.FX, inr), "Approved (DEC-419)"])
rows.append(["**Total AI-built tooling per month**", "", "", "", f"**{rng(*ai_tools, usdv)}**", f"**{rng(ai_tools[0] * M.FX, ai_tools[1] * M.FX, inr)}**", f"Traditional (DEC-419): {rng(*trad_tools, usdv)}"])
table(["Item", "Purpose", "Unit $/month", "Seats", "Per month (USD)", "Per month (INR)", "Notes"], rows)
A("The approved Ledger B line B09 (2 Claude seats, ₹4,140/month) is part of these Claude totals in both approaches. It is not added twice.\n")
A("## 6.2 AI-agent token usage (Claude API for headless and parallel agents)\n")
A(f"Token use is estimated per person-day of work executed by agents. The assumptions are 4.0 M input tokens per agent-executed person-day, 80% of them served from the prompt cache, plus 0.2 M output tokens. The model mix is {', '.join(f'{int(v * 100)}% {k}' for k, v in X.MODEL_MIX.items())}. List prices per million tokens (input / cached input / output) are:\n")
for k, v in X.MODEL_PRICES.items():
    A(f"- {k}: ${v[0]} / ${v[1]} / ${v[2]}")
A(f"\nThat gives **{usdv(USD_PD, 2)} per agent-executed person-day** in the central case; prices to verify. Multipliers for retries, parallel exploration and long contexts: optimistic ×0.5, conservative ×3.\n")
rows = []
for k in allk:
    a = AI[k]
    rows.append([P[k][1], " / ".join(f"{v:,.0f}" for v in a["agent_pd"]), f"{usdv(a['tokens_usd'][0])} / {usdv(a['tokens_usd'][1])} / {usdv(a['tokens_usd'][2])}", rng(a["tokens_usd"][0] * M.FX, a["tokens_usd"][2] * M.FX, inr)])
rows.append(["**Approved scope**", "", f"**{usdv(tok_ap[0])} / {usdv(tok_ap[1])} / {usdv(tok_ap[2])}**", f"**{rng(tok_ap[0] * M.FX, tok_ap[2] * M.FX, inr)}**"])
rows.append(["**Full programme**", "", f"**{usdv(tok_all[0])} / {usdv(tok_all[1])} / {usdv(tok_all[2])}**", f"**{rng(tok_all[0] * M.FX, tok_all[2] * M.FX, inr)}**"])
table(["Package", "Agent-executed pd (opt./central/cons.)", "Token cost USD (opt./central/cons.)", "Token cost INR"], rows)
A("These are **build costs**: the AI used to write the software. They are separate from the application's own production AI inference (Ledger B lines B02, B23, B24), which is unchanged.\n")

A("# 7. AI agents, automations and workflows: traditional vs AI-built build effort\n")
rows = []
for k, nm in (("AG", "AI agents"), ("AU", "Automations"), ("WF", "Workflows")):
    s_ = [i for i in CAT if i["kind"] == k]
    rows.append([nm, len(s_), f"{sum(i['pd_lo'] for i in s_):,.0f}–{sum(i['pd_hi'] for i in s_):,.0f}", f"{sum(i['ai_pd_lo'] for i in s_):,.0f}–{sum(i['ai_pd_hi'] for i in s_):,.0f}",
                 rng(sum(i['cost_lo'] for i in s_), sum(i['cost_hi'] for i in s_)), rng(sum(i['ai_cost_lo'] for i in s_), sum(i['ai_cost_hi'] for i in s_)), f"{inr(sum(i['run_base'] for i in s_))}/month" if k == "AG" else "In hosting"])
table(["Type", "Count", "Traditional build pd", "AI-built pd", "Traditional build cost", "AI-built build cost", "Run cost (unchanged)"], rows)
A("The full list of all 237 items is in §13 and in the workbook. For each item it gives what it does, its automation level, traditional and AI-built effort and cost, run cost, release and timeline.\n")

A("# 8. Drafting: user stories, test cases and test strategies\n")
rows = []
for d in BE.draft:
    rows.append([d["name"], f"{d['n']:,}", f"{d['man'][0] / 8:,.0f}–{d['man'][1] / 8:,.0f}", f"{d['bp'][0] / 8:,.0f}–{d['bp'][1] / 8:,.0f}", f"{d['bp'][0] / 8 * 0.5:,.0f}–{d['bp'][1] / 8 * 0.7:,.0f}", "Spec agent drafts; humans refine the blueprint drafts and accept"])
rows.append(["Test strategies and plans", f"{sum(c for _, c, _ in M.STRATEGY_DOCS)} docs", f"{BE.strat_lo:.0f}–{BE.strat_hi:.0f}", f"{BE.strat_lo * 0.35:.0f}–{BE.strat_hi * 0.35:.0f}", f"{BE.strat_lo * 0.2:.0f}–{BE.strat_hi * 0.3:.0f}", "Agent drafts from Part 6.1; QA lead owns"])
table(["Artefact", "Count", "Manual pd", "Traditional plan pd (refine drafts)", "AI-built pd", "How"], rows)

A("# 9. Timeline options\n")
A(f"**Option A (cost view): same dates, smaller team.** Release 1 go/no-go Fri 04 Jun 2027 (Day 180), Release 2 build Fri 02 Jul 2027 (Day 208), W5 exit Fri 23 Jul 2027 (Day 229). Team ≈ {sum(t[1] for t in X.AI_TEAM):.1f} FTE at peak.\n")
A("**Option B (time view): same team, earlier delivery.** Engineering phases shrink by the net saving. Foundation, legal, provider onboarding, penetration tests, UAT with users and the 30-day monitored pilot do not shrink. The cost is about the same as option A, because the same team works fewer months, but revenue starts earlier.\n")
rows = [["Release 1 go/no-go", "Fri 04 Jun 2027 (Day 180)"] + [f"{day(TL[c]['r1'])} (Day {TL[c]['r1']:.0f})" for c in X.CASES],
        ["Release 2 build gate", "Fri 02 Jul 2027 (Day 208)"] + [f"{day(TL[c]['r2'])} (Day {TL[c]['r2']:.0f})" for c in X.CASES],
        ["W5 exit (after monitored pilot)", "Fri 23 Jul 2027 (Day 229)"] + [f"{day(TL[c]['w5'])} (Day {TL[c]['w5']:.0f})" for c in X.CASES],
        ["Advanced A1 complete", "Dec 2027 (Day ≈ 365)"] + [f"{day(TL[c]['a1e'])}" for c in X.CASES],
        ["Advanced A2 complete", "Mar 2028 (Day ≈ 480)"] + [f"{day(TL[c]['a2e'])}" for c in X.CASES],
        ["Advanced A3 complete", "Jul 2028 (Day ≈ 600)"] + [f"{day(TL[c]['a3e'])}" for c in X.CASES]]
table(["Milestone", "Traditional (approved)", "AI-built optimistic", "AI-built central", "AI-built conservative"], rows)

A("# 10. Recurring running cost of the application (unchanged)\n")
A("Building with AI agents does not change what the application runs on, so the running costs in v1.0 §8 apply unchanged.\n")
table(["Item", "Per month (INR)", "Per month (USD)"], [
    ["Pilot running after launch (Ledger B, contingency, seats)", rng(BE.runs_lo, BE.runs_hi, inr), rng(BE.runs_lo, BE.runs_hi, usd)],
    ["Literal-alignment additions (CR-ALN-02)", rng(*BE.aln_run, inr), rng(*BE.aln_run, usd)],
    ["Advanced capabilities at full rollout", rng(BE.adv_lo, BE.adv_hi, inr), rng(BE.adv_lo, BE.adv_hi, usd)],
    ["Growth gate / scale design points", "₹50–70 thousand / ₹1.3–1.7 lakh", "$556–778 / $1,444–1,889"],
])
A(f"**After the build**, the AI tooling continues for the maintenance team at about **{rng(*ai_tools_after, usdv)} per month**. That covers 2 Claude Max 20x seats, 2 Pro seats, CI sandboxes and agent observability, plus the remaining DEC-419 tools.\n")

A("# 11. Lifecycle: maintenance, future-proofing and three-year TCO\n")
A(f"With AI agents, maintenance is assumed at **{X.MAINT_PCT_AI[0] * 100:.0f}–{X.MAINT_PCT_AI[1] * 100:.0f}%** of cumulative development per year, against 15–20% traditionally. Agents handle routine patches, dependency upgrades and test repair. Effort-based future-proofing items (model migration, framework upgrades, DR drills, documentation) shrink by the same net saving. Fixed-price items (penetration test, accessibility audit, DPDP review) do not. Future-proofing per year: **{rng(*FP_AI)}** (traditional {rng(BE.fp_lo, BE.fp_hi)}).\n")
for title, t_, a_ in (("Approved path", BE.tco_ap, TCO_AI_AP), ("Full roadmap", BE.tco_full, TCO_AI_FULL)):
    A(f"## {title}\n")
    rows = []
    for yt, ya in zip(t_, a_):
        tt_ = (sum(yt[j][0] for j in range(1, 6)), sum(yt[j][1] for j in range(1, 6)))
        ta_ = (sum(ya[j][0] for j in range(1, 6)), sum(ya[j][1] for j in range(1, 6)))
        rows.append([yt[0], rng(*yt[1]), rng(*ya[1]), rng(*ya[2]), rng(*ya[3]), rng(*ya[4]), rng(*ya[5]), rng(*tt_), f"**{rng(*ta_)}**"])
    T, Aa = tt(t_), tt(a_)
    rows.append(["**Total (build + 3 years)**", "", "", "", "", "", "", f"**{rng(*T)}**", f"**{rng(*Aa)}**"])
    table(["Year", "Development traditional", "Development AI-built", "Running (same)", "Tooling + tokens (AI-built)", "Maintenance (AI-built)", "Future-proofing (AI-built)", "Total traditional", "Total AI-built"], rows)

A("# 12. Risks, calibration gate and recommendation\n")
table(["Risk specific to AI-built delivery", "Effect", "Control"], [
    ["Productivity lower than assumed", "Savings shrink towards the conservative case (~7%)", "Sprint 2 calibration gate: measure accepted story points per engineer-week against the traditional baseline before reducing the team"],
    ["Subtle defects in generated code", "Rework, incidents", "Test-first development; mandatory human review; rework allowance; SAST; mutation testing on critical modules"],
    ["Security weaknesses or vulnerable dependencies", "Data exposure", "Security agent + independent reviewer; dependency pinning; secret scanning; two external pen tests unchanged"],
    ["Licence and IP contamination", "Legal exposure", "Licence scanning; provenance log; company policy on AI-generated code; contracts assign IP"],
    ["Over-reliance and skills erosion", "Team cannot maintain code", "Engineers own design and reviews; architecture docs and ADRs kept current; pairing on critical modules"],
    ["Token cost overruns", "Higher build AI spend", "API budget caps with alerts; prompt caching; model mix tuned (Haiku for simple tasks)"],
    ["Vendor dependency on one model provider", "Disruption", "Specs and tests are model-agnostic; the codebase is ordinary Django/React; agents can be switched"],
    ["Data protection", "Personal data reaching build agents", "Synthetic data only in agent sandboxes; no production access for agents"],
])
A("**Approved approach (DEC-420, Founder, 28 Nov 2026):**\n")
A("1. Start with the approved traditional team, using the AI tooling and the operating model in §2 from Sprint 0.")
A("2. At the **Sprint 2 calibration gate (about Day 45)**, compare measured throughput with the central assumptions.")
A("3. If the measured net saving is at least 20%, then either:")
A("   - release the second contract engineer and keep the dates (option A); or")
A("   - keep the team and bring Release 1 forward (option B).")
A("4. If the measured net saving is below 20%, keep the approved plan. The extra AI tooling costs about ₹45,000 per month, a small cost against the benefit.\n")
A("**Gate measurement and thresholds (DEC-420).**\n")
table(["Item", "Definition"], [
    ["Net saving", "1 − (actual engineer-days ÷ planned engineer-days for the scope accepted in Sprints 1–2), using the Part 8.1 sprint plan as the baseline"],
    ["Quality guard 1", "Defects escaping to SIT no more than 20% above the plan rate"],
    ["Quality guard 2", "No unresolved critical or high security findings in AI-generated code"],
    ["Quality guard 3", "Pull-request review backlog under 2 working days"],
    ["≥ 20% and guards hold", "Option A by default: keep the dates and release the second contract engineer from Sprint 3 (Ledger A updated by change control). The Founder may choose option B: keep the team and bring Release 1 forward"],
    ["10–20%", "Keep the approved team and dates; keep the AI tooling"],
    ["< 10%", "Keep the approved plan; revert to the DEC-419 tooling"],
    ["Build-agent API budget", "Hard cap $1,500 per month (₹1.35 L) with alerts at 70/90/100%"],
    ["Record", "The gate result and the option chosen are recorded as a new decision"],
])

A("# 13. Full list: AI agents, automations and workflows, traditional vs AI-built\n")
for k, nm in (("AG", "AI agents"), ("AU", "Automations"), ("WF", "Workflows")):
    A(f"## 13.{['AG', 'AU', 'WF'].index(k) + 1} {nm} ({sum(1 for i in CAT if i['kind'] == k)})\n")
    rows = []
    for i in [x for x in CAT if x["kind"] == k]:
        rows.append([i["id"], i["name"], i["what"][:240] + ("…" if len(i["what"]) > 240 else ""), i["level"].split(" (")[0], f"{i['pd_lo']:g}–{i['pd_hi']:g}", f"{i['ai_pd_lo']:.1f}–{i['ai_pd_hi']:.1f}",
                     rng(i["cost_lo"], i["cost_hi"], inr), rng(i["ai_cost_lo"], i["ai_cost_hi"], inr), f"{inr(i['run_base'])}" if k == "AG" else "In B01", f"{i['release']} ({i['dates']})"])
    table(["ID", "Name", "What it does", "Automation", "Trad. pd", "AI-built pd", "Trad. build cost", "AI-built build cost", "Run/month", "Release and timeline"], rows, [5, 11, 34, 8, 5, 6, 10, 10, 6, 10])

A("# 14. Assumptions\n")
for i, t_ in enumerate([
    "Everything in Cost Estimate v1.0 §15 applies unless stated here.",
    "AI acceleration factors and oversight overheads (§3) are planning assumptions to calibrate at Sprint 2.",
    "Only people costs scale with AI productivity; vendor and fixed-price items (pen tests, training content vendor, load-test windows) do not.",
    "Token prices are list prices for Claude Opus-, Sonnet- and Haiku-class models as known on the date; verify. Usage per agent-executed person-day: 4.0 M input (80% cached), 0.2 M output.",
    "Option A keeps the approved dates; option B keeps the approved team. Both have similar cost; option B starts revenue earlier.",
    "Maintenance with AI agents is 12–17% of cumulative development per year (traditional 15–20%).",
    "The application's own features, production AI agents and running costs are identical in both approaches.",
], 1):
    A(f"{i}. {t_}")
A("\n**End of document.**")

md = "\n".join(DOC) + "\n"
(OUT / f"{NAME}.md").write_text(md, encoding="utf-8")
print("AI-built MD", len(md), {c: round(SAVE[c], 4) for c in X.CASES}, "agent share", round(AGENT_SHARE, 3), "usd/pd", round(USD_PD, 2))

DATA = dict(AI=AI, SAVE=SAVE, AGENT_SHARE=AGENT_SHARE, USD_PD=USD_PD, CAT=CAT, ai_tools_rows=ai_tools_rows, nonclaude=nonclaude, trad_tools=trad_tools,
            ai_tools=ai_tools, ai_tools_after=ai_tools_after, TL=TL, TCO_AI_AP=TCO_AI_AP, TCO_AI_FULL=TCO_AI_FULL, day=day, allk=allk, approved=approved)

if __name__ == "__main__":
    import build_xlsx_ai
    build_xlsx_ai.build(DATA, BE, OUT / f"{NAME}.xlsx")
    env = {**os.environ, "LANG": "C.UTF-8", "LC_ALL": "C.UTF-8"}
    subprocess.run([str(BE.BP / "make_pdf.sh"), f"{NAME}.md", "Cost Estimate v1.1 (AI-built) · 28 Nov 2026 · Confidential"], cwd=OUT, check=True, env=env)
    import build_docx
    build_docx.build(OUT / f"{NAME}.md", OUT / f"{NAME}.docx", header="AI Growth Engine — Cost Estimate v1.1: AI-built vs traditional    |    Confidential · 28 Nov 2026",
                     title="AI Growth Engine: Cost Estimate v1.1 (AI-built)", subtitle="Building the application with AI models and AI agents: traditional vs AI-built, INR and USD", version="Version 1.1 · 28 Nov 2026 · Confidential")
