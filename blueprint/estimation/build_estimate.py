#!/usr/bin/env python3
"""Build the end-to-end cost estimate: Markdown -> PDF and Word, plus an Excel workbook with formulas.

Usage: python3 blueprint/estimation/build_estimate.py
Outputs: blueprint/final/estimation/AI_Growth_Engine_Cost_Estimate_v1.0.{md,pdf,docx,xlsx}
"""
import collections
import os
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import model as M  # noqa: E402
import catalogue as C  # noqa: E402

BP = HERE.parent
OUT = BP / "final" / "estimation"
IMG = OUT / "img"
NAME = "AI_Growth_Engine_Cost_Estimate_v1.0"
OUT.mkdir(parents=True, exist_ok=True)
IMG.mkdir(exist_ok=True)


# ---------------------------------------------------------------- formatting
def ind(n):
    """Indian digit grouping."""
    n = round(n)
    neg = n < 0
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
    return ("-" if neg else "") + s


def inr(x):
    return "₹" + ind(x)


def lakh(x, d=2):
    return f"₹{x / M.L:,.{d}f} L"


def usd(x, d=0):
    return f"${x / M.FX:,.{d}f}"


def usdv(x, d=0):
    return f"${x:,.{d}f}"


def rng(lo, hi, f=lakh):
    return f"{f(lo)} – {f(hi)}"


def both(lo, hi, f=lakh):
    return f"{f(lo)} – {f(hi)}", f"{usd(lo)} – {usd(hi)}"


DOC = []
A = DOC.append


def table(header, rows, widths=None):
    A("| " + " | ".join(header) + " |")
    A("|" + "|".join("-" * max(3, w) for w in (widths or [3] * len(header))) + "|")
    for r in rows:
        A("| " + " | ".join(str(c).replace("|", "/").replace("\n", " ") for c in r) + " |")
    A("")


# ---------------------------------------------------------------- computations
cat = M.catalogue()
la = M.ledger_a_rows()
la_lo, la_hi = sum(r["lo"] for r in la), sum(r["hi"] for r in la)
assert abs(la_lo - 5_268_000) < 2_000 and abs(la_hi - 8_408_000) < 2_000, (la_lo, la_hi)

P = {p[0]: p for p in M.PACKAGES}
approved = ["CORE", "ALN", "A1"]
optional = ["PH2", "A2", "A3"]
ap_lo, ap_c, ap_hi = (sum(P[k][i] for k in approved) for i in (3, 4, 5))
all_lo, all_c, all_hi = (sum(P[k][i] for k in approved + optional) for i in (3, 4, 5))

base_lo = sum(r[4] for r in M.LEDGER_B)
base_hi = sum(r[5] for r in M.LEDGER_B)
run_lo, run_hi = base_lo * 1.15, base_hi * 1.15
runs_lo, runs_hi = run_lo + M.SEATS_B09, run_hi + M.SEATS_B09
add_lo = sum(r[2] for r in M.RUN_ADDITIONS)
add_hi = sum(r[3] for r in M.RUN_ADDITIONS)
adv_lo = sum(r[2] for r in M.RUN_ADDITIONS[1:])
adv_hi = sum(r[3] for r in M.RUN_ADDITIONS[1:])
aln_run = M.RUN_ADDITIONS[0][2:4]
B_DURING_BUILD = (147_000, 175_000)

# tooling (USD)
tool_rows = []
for t in M.TOOLS:
    name, purpose, plan, ulo, uhi, seats, req, after, note = t
    tool_rows.append(dict(name=name, purpose=purpose, plan=plan, ulo=ulo, uhi=uhi, seats=seats, req=req, after=after, note=note,
                          mlo=ulo * seats, mhi=uhi * seats, alo=ulo * after, ahi=uhi * after))
# add the third Pro seat for QA/growth/PO
tool_rows.insert(2, dict(name="Claude (Anthropic) – Pro for the third non-engineering user", purpose="Drafting stories, tests, UAT scripts, compliance notes", plan="Pro", ulo=20, uhi=20, seats=1, req="Approved (DEC-419)", after=1, note="With the 2 baseline Pro seats, covers QA, growth/compliance lead and PO", mlo=20, mhi=20, alo=20, ahi=20))
baseline_usd = sum(r["mlo"] for r in tool_rows if r["req"].startswith("Approved (B"))
rec_lo = sum(r["mlo"] for r in tool_rows if not r["req"].startswith("Optional") and not r["req"].startswith("Approved (B"))
rec_hi = sum(r["mhi"] for r in tool_rows if not r["req"].startswith("Optional") and not r["req"].startswith("Approved (B"))
opt_lo = sum(r["mlo"] for r in tool_rows if r["req"].startswith("Optional"))
opt_hi = sum(r["mhi"] for r in tool_rows if r["req"].startswith("Optional"))
after_lo = sum(r["alo"] for r in tool_rows if not r["req"].startswith("Optional") and not r["req"].startswith("Approved (B"))
after_hi = sum(r["ahi"] for r in tool_rows if not r["req"].startswith("Optional") and not r["req"].startswith("Approved (B"))
lean_claude = 9 * 20 - 40   # Pro for all 9 users, minus the 2 baseline seats

# effort by activity
core_eff = (532, 722, 921)
prog_eff = tuple(M.effort_pd(approved + optional, p) for p in ("low", "central", "high"))
ap_eff = tuple(M.effort_pd(approved, p) for p in ("low", "central", "high"))

# drafting
draft = []
for name, key, man, ai, bp, who in M.DRAFTING:
    n = M.ARTEFACTS[key]
    draft.append(dict(name=name, n=n, who=who, man=(n * man[0], n * man[1]), ai=(n * ai[0], n * ai[1]), bp=(n * bp[0], n * bp[1])))
strat_lo = sum(c * r[0] for _, c, r in M.STRATEGY_DOCS)
strat_hi = sum(c * r[1] for _, c, r in M.STRATEGY_DOCS)

# catalogue aggregates
kinds = {"AG": "AI agents", "AU": "Automations", "WF": "Workflows"}
by_kind = {k: [i for i in cat if i["kind"] == k] for k in kinds}
cat_pd_lo = sum(i["pd_lo"] for i in cat)
cat_pd_hi = sum(i["pd_hi"] for i in cat)
ag_run = [sum(i[f] for i in by_kind["AG"]) for f in ("run_lo", "run_base", "run_hi")]

# future-proofing per year
fp_rows = []
fp_lo = fp_hi = 0
for name, basis, lo, hi, kind in M.FUTURE:
    if kind == "pd":
        clo, chi = lo * M.PD_RATE[0], hi * M.PD_RATE[1]
    elif kind == "inr":
        clo, chi = lo, hi
    elif kind == "fx":
        clo, chi = 0.05 * (baseline_usd + rec_lo) * 12 * M.FX, 0.05 * (baseline_usd + rec_hi) * 12 * M.FX
    else:
        clo = chi = None
    fp_rows.append((name, basis, clo, chi))
    if clo is not None:
        fp_lo += clo
        fp_hi += chi

# cash flow (approved scope; central and range) month by month
months = ["Dec 2026", "Jan 2027", "Feb 2027", "Mar 2027", "Apr 2027", "May 2027", "Jun 2027", "Jul 2027",
          "Aug 2027", "Sep 2027", "Oct 2027", "Nov 2027", "Dec 2027", "Jan 2028", "Feb 2028", "Mar 2028",
          "Apr 2028", "May 2028", "Jun 2028", "Jul 2028"]
ramp_b = {"Dec 2026": (15_410, 18_055), "Jan 2027": (18_285, 20_930), "Feb 2027": (20_355, 23_575), "Mar 2027": (21_505, 24_725), "Apr 2027": (23_805, 27_025)}


def dev_month(m, key):
    lo, c, hi = P[key][3], P[key][4], P[key][5]
    spread = {
        "CORE": None,
        "ALN": ["Jan 2027", "Feb 2027", "Mar 2027", "Apr 2027", "May 2027", "Jun 2027"],
        "A1": ["Aug 2027", "Sep 2027", "Oct 2027", "Nov 2027", "Dec 2027"],
        "PH2": ["Aug 2027", "Sep 2027", "Oct 2027", "Nov 2027", "Dec 2027"],
        "A2": ["Dec 2027", "Jan 2028", "Feb 2028", "Mar 2028"],
        "A3": ["Apr 2028", "May 2028", "Jun 2028", "Jul 2028"],
    }[key]
    if key == "CORE":
        ph = {"Dec 2026": (540_000, 820_000)}
        for mm in ("Jan 2027", "Feb 2027", "Mar 2027", "Apr 2027", "May 2027"):
            ph[mm] = (3_730_000 / 5, 5_900_000 / 5)
        ph["Jun 2027"] = (1_000_000 * 0.6, 1_690_000 * 0.6)
        ph["Jul 2027"] = (1_000_000 * 0.4, 1_690_000 * 0.4)
        v = ph.get(m, (0, 0))
        return v[0], (v[0] + v[1]) / 2, v[1]
    if m in spread:
        n = len(spread)
        return lo / n, c / n, hi / n
    return 0, 0, 0


def run_month(m, scope):
    if m in ramp_b:
        lo, hi = ramp_b[m]
    else:
        lo, hi = runs_lo, runs_hi
    if months.index(m) >= months.index("Jun 2027"):
        lo += aln_run[0]
        hi += aln_run[1]
    # advanced running ramps: A1 35%, A2 70%, A3 100% (only for scope that includes them)
    idx = months.index(m)
    share = 0
    if idx >= months.index("Aug 2027"):
        share = 0.35
    if idx >= months.index("Dec 2027") and "A2" in scope:
        share = 0.70
    if idx >= months.index("Apr 2028") and "A3" in scope:
        share = 1.0
    lo += share * adv_lo
    hi += share * adv_hi
    return lo, (lo + hi) / 2, hi


def tools_month(m):
    return (baseline_usd * 0 + rec_lo) * M.FX, (rec_lo + rec_hi) / 2 * M.FX, rec_hi * M.FX


cash = []
cum = [0, 0, 0]
for m in months:
    dev = [0, 0, 0]
    for k in approved:
        v = dev_month(m, k)
        dev = [a + b for a, b in zip(dev, v)]
    rn = run_month(m, approved)
    tl = tools_month(m)
    tot = [dev[i] + rn[i] + tl[i] for i in range(3)]
    cum = [cum[i] + tot[i] for i in range(3)]
    cash.append(dict(m=m, dev=dev, run=rn, tools=tl, tot=tot, cum=list(cum)))

# 3-year TCO for two paths
def tco(path_keys):
    years = []
    # Year 0: Dec 2026 – Jul 2027
    y0_dev = [P["CORE"][i] + P["ALN"][i] for i in (3, 5)]
    y0_run = list(B_DURING_BUILD)
    y0_run = [y0_run[0] + 2 * aln_run[0] + runs_lo, y0_run[1] + 2 * aln_run[1] + runs_hi]   # Jun–Jul alignment adds + Jul running
    y0_tools = [rec_lo * 8 * M.FX, rec_hi * 8 * M.FX]
    years.append(("Year 0 (build): Dec 2026 – Jul 2027", y0_dev, y0_run, y0_tools, [0, 0], [0, 0]))
    # Year 1: Aug 2027 – Jul 2028
    y1_dev = [sum(P[k][i] for k in path_keys if k in ("A1", "A2", "A3", "PH2")) for i in (3, 5)]
    y1_run = [0, 0]
    for m in months[8:]:
        r = run_month(m, path_keys)
        y1_run = [y1_run[0] + r[0], y1_run[1] + r[2]]
    y1_tools = [rec_lo * 12 * M.FX, rec_hi * 12 * M.FX]
    cum_dev = [P["CORE"][3] + P["ALN"][3], P["CORE"][5] + P["ALN"][5]]
    y1_maint = [0.15 * cum_dev[0], 0.20 * cum_dev[1]]
    years.append(("Year 1: Aug 2027 – Jul 2028", y1_dev, y1_run, y1_tools, y1_maint, [fp_lo, fp_hi]))
    cum_dev = [cum_dev[0] + y1_dev[0], cum_dev[1] + y1_dev[1]]
    adv_share = 1.0 if "A3" in path_keys else 0.35
    # Year 2: growth design point
    y2_run = [(50_000 + adv_share * adv_lo + aln_run[0]) * 12, (70_000 + adv_share * adv_hi + aln_run[1]) * 12]
    y2_tools = [after_lo * 12 * M.FX + M.SEATS_B09 * 12, after_hi * 12 * M.FX + M.SEATS_B09 * 12]
    esc = 1.08
    years.append(("Year 2: Aug 2028 – Jul 2029 (growth gate)", [0, 0], y2_run, y2_tools, [0.15 * cum_dev[0] * esc, 0.20 * cum_dev[1] * esc], [fp_lo * esc, fp_hi * esc]))
    y3_run = [(130_000 + adv_share * adv_lo + aln_run[0]) * 12, (170_000 + adv_share * adv_hi + aln_run[1]) * 12]
    years.append(("Year 3: Aug 2029 – Jul 2030 (scale design point)", [0, 0], y3_run, y2_tools, [0.15 * cum_dev[0] * esc ** 2, 0.20 * cum_dev[1] * esc ** 2], [fp_lo * esc ** 2, fp_hi * esc ** 2]))
    return years


tco_ap = tco(approved)
tco_full = tco(approved + ["A2", "A3", "PH2"])


def tco_total(t):
    lo = sum(y[1][0] + y[2][0] + y[3][0] + y[4][0] + y[5][0] for y in t)
    hi = sum(y[1][1] + y[2][1] + y[3][1] + y[4][1] + y[5][1] for y in t)
    return lo, hi


# scenario matrix
scen = []
for sid, sname, keys in M.SCOPE_PACKAGES:
    for tid, tname, mult, basis in M.TEAM_MODELS:
        for pt in ("low", "central", "high"):
            if mult is not None:
                c = M.cost(keys, pt) * mult
            else:
                rate = {"low": M.ONSHORE_USD_HR[0], "central": sum(M.ONSHORE_USD_HR) / 2, "high": M.ONSHORE_USD_HR[1]}[pt]
                c = M.effort_pd(keys, pt) * M.HOURS_PER_DAY * rate * 1.15 * M.FX
            scen.append(dict(sid=sid, sname=sname, tid=tid, tname=tname, pt=pt, inr=c, eff=M.effort_pd(keys, pt)))


# ---------------------------------------------------------------- charts
def charts():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    plt.rcParams.update({"font.size": 10, "font.family": "DejaVu Sans"})
    navy, teal, grey, amber = "#0b3d6b", "#2a9d8f", "#9aa5b1", "#e9a23b"
    # 1 packages
    fig, ax = plt.subplots(figsize=(10, 4.2), dpi=150)
    keys = approved + optional
    short = {"CORE": "Core build (Ledger A)", "ALN": "Literal alignment", "A1": "Advanced A1", "PH2": "Phase-2 continuation", "A2": "Advanced A2", "A3": "Advanced A3"}
    names = [short[k] for k in keys]
    lo = [P[k][3] / M.L for k in keys]
    hi = [P[k][5] / M.L for k in keys]
    c = [P[k][4] / M.L for k in keys]
    y = range(len(keys))
    ax.barh(y, [h - l for l, h in zip(lo, hi)], left=lo, color=[navy if k in approved else grey for k in keys], alpha=0.85, height=0.55)
    ax.scatter(c, y, color=amber, zorder=3, label="Central")
    ax.set_yticks(list(y)); ax.set_yticklabels(names); ax.invert_yaxis()
    ax.set_xlabel("₹ lakh (one-time development)"); ax.set_title("One-time development cost by package (navy = approved, grey = optional/proposed)")
    for i, (l, h) in enumerate(zip(lo, hi)):
        ax.text(h + 1, i, f"{l:.1f}–{h:.1f} L", va="center", fontsize=8)
    ax.legend(loc="lower right"); fig.tight_layout(); fig.savefig(IMG / "packages.png"); plt.close(fig)
    # 2 cumulative cash flow
    fig, ax = plt.subplots(figsize=(10, 4.2), dpi=150)
    xs = [r["m"].replace(" 20", " '") for r in cash]
    ax.fill_between(range(len(cash)), [r["cum"][0] / M.L for r in cash], [r["cum"][2] / M.L for r in cash], color=teal, alpha=0.25, label="Low–high range")
    ax.plot(range(len(cash)), [r["cum"][1] / M.L for r in cash], color=navy, lw=2, label="Central")
    ax.set_xticks(range(len(cash))); ax.set_xticklabels(xs, rotation=60, fontsize=8)
    ax.set_ylabel("₹ lakh, cumulative"); ax.set_title("Cumulative cash: approved scope (core + alignment + A1), development + running + tooling")
    ax.legend(); ax.grid(alpha=0.3); fig.tight_layout(); fig.savefig(IMG / "cashflow.png"); plt.close(fig)
    # 3 cost share (approved, central)
    people = sum(r["pm"] for r in la) * sum(M.PM_RATE) / 2 + P["ALN"][4] + P["A1"][4]
    vendors = sum((r["lo"] + r["hi"]) / 2 for r in la if not r["pm"])
    subs = (B_DURING_BUILD[0] + B_DURING_BUILD[1]) / 2 + 12 * (runs_lo + runs_hi) / 2 + 20 * (rec_lo + rec_hi) / 2 * M.FX
    fig, ax = plt.subplots(figsize=(6.5, 4.2), dpi=150)
    vals = [people, vendors, subs]
    ax.pie(vals, labels=["People (build)", "External vendors", "Subscriptions + running\n(build + 12 months)"], colors=[navy, teal, amber],
           autopct=lambda p: f"{p:.0f}%", startangle=90, wedgeprops=dict(width=0.45))
    ax.set_title("Where the money goes (approved scope, central)")
    fig.tight_layout(); fig.savefig(IMG / "share.png"); plt.close(fig)
    # 4 catalogue by release
    rels = ["Release 1", "Release 2", "W6 / Phase 2", "Advanced A1", "Advanced A2", "Advanced A3 (after scale gate)"]
    fig, ax = plt.subplots(figsize=(10, 3.8), dpi=150)
    bottom = [0] * len(rels)
    for k, col in (("AG", navy), ("AU", teal), ("WF", amber)):
        v = [sum(1 for i in by_kind[k] if i["release"] == r) for r in rels]
        ax.bar(range(len(rels)), v, bottom=bottom, color=col, label=kinds[k])
        bottom = [a + b for a, b in zip(bottom, v)]
    ax.set_xticks(range(len(rels))); ax.set_xticklabels([r.replace(" (after scale gate)", "") for r in rels])
    ax.set_title("AI agents, automations and workflows by release"); ax.legend(); ax.grid(axis="y", alpha=0.3)
    fig.tight_layout(); fig.savefig(IMG / "catalogue.png"); plt.close(fig)
    return people, vendors, subs


people_c, vendors_c, subs_c = charts()


# ---------------------------------------------------------------- document
A("# AI Growth Engine: End-to-End Cost Estimate")
A("## Development, subscriptions, AI agents, automations, workflows and lifecycle costs, in INR and USD")
A("")
table(["Field", "Value"], [
    ["Document", "Cost Estimate v1.0 for the AI Growth Engine (Employee Sales & Marketing Automation)"],
    ["Date", f"{M.AS_OF}"],
    ["Basis", "Application Blueprint v1.1 (Parts 0–9.10, 342 decisions), approved budgets DEC-230/231, Founder decisions DEC-416…419"],
    ["Currency", f"INR and USD at **₹{M.FX:.0f} = $1** (blueprint rate, Part 8.4; verify at time of payment). Sensitivity at ₹85 and ₹95 in §13"],
    ["Prepared by", "FinOps Lead with Product Owner, Delivery Lead, Solutions Architect, QA Lead and AI Governance Lead (blueprint team)"],
    ["Classification", "Confidential: Founder and authorized delivery partners"],
    ["Companion files", f"`{NAME}.xlsx` (14 sheets with live formulas: change FX, rates or scope and every total recalculates), `{NAME}.docx` (editable)"],
])
A("**How to read this document.** Every figure is an **estimate** with a low, central and high value. Prices of third-party services are list prices as known on the date above and are marked **verify at time of purchase**. Amounts **exclude GST** unless a \"with GST\" column says otherwise. One-time development cost and recurring subscription/running cost are **always shown separately**.\n")

# 1 Executive summary
A("# 1. Executive summary\n")
A("## 1.1 Headline numbers\n")
rows = []
for k in approved + optional:
    p = P[k]
    rows.append([p[1], p[2], p[7], lakh(p[3]), lakh(p[4]), lakh(p[5]), usd(p[3]), usd(p[4]), usd(p[5])])
rows.append(["**Approved one-time development (core + alignment + A1)**", "Approved", "Dec 2026 – Dec 2027", f"**{lakh(ap_lo)}**", f"**{lakh(ap_c)}**", f"**{lakh(ap_hi)}**", f"**{usd(ap_lo)}**", f"**{usd(ap_c)}**", f"**{usd(ap_hi)}**"])
rows.append(["**Full programme, if every option is approved**", "Approved + optional", "Dec 2026 – Jul 2028", f"**{lakh(all_lo)}**", f"**{lakh(all_c)}**", f"**{lakh(all_hi)}**", f"**{usd(all_lo)}**", f"**{usd(all_c)}**", f"**{usd(all_hi)}**"])
table(["One-time development package", "Status", "When", "Low (INR)", "Central (INR)", "High (INR)", "Low (USD)", "Central (USD)", "High (USD)"], rows)

A("**Recurring subscriptions and running cost (separate from development).**\n")
table(["Recurring item", "Per month (INR)", "Per month (USD)", "Per year (INR)", "Per year (USD)"], [
    ["Running cost paid **during the build** (Day 1–208, ramping up), approved Ledger B", rng(*B_DURING_BUILD) + " for the whole build", rng(*B_DURING_BUILD, usd) + " total", "—", "—"],
    ["Approved **build-time tooling** (DEC-419: Claude for all engineers, GitHub, Figma, Workspace, Bitwarden, BrowserStack), in addition to Ledger B", rng(rec_lo * M.FX, rec_hi * M.FX, inr), rng(rec_lo, rec_hi, usdv), rng(rec_lo * M.FX * 12, rec_hi * M.FX * 12), rng(rec_lo * 12, rec_hi * 12, usdv)],
    ["Pilot running cost **after launch** (approved Ledger B base + 15% contingency + 2 Claude seats)", rng(runs_lo, runs_hi, inr), rng(runs_lo, runs_hi, usd), rng(runs_lo * 12, runs_hi * 12), rng(runs_lo * 12, runs_hi * 12, usd)],
    ["Plus literal-alignment running additions (CR-ALN-02, upper bound)", rng(*aln_run, inr), rng(*aln_run, usd), rng(aln_run[0] * 12, aln_run[1] * 12), rng(aln_run[0] * 12, aln_run[1] * 12, usd)],
    ["Plus advanced capabilities at full rollout (X1 + X2 + X3, after A3)", rng(adv_lo, adv_hi, inr), rng(adv_lo, adv_hi, usd), rng(adv_lo * 12, adv_hi * 12), rng(adv_lo * 12, adv_hi * 12, usd)],
    ["**All-in pilot running after the full advanced roadmap**", f"**{rng(runs_lo + add_lo, runs_hi + add_hi, inr)}**", f"**{rng(runs_lo + add_lo, runs_hi + add_hi, usd)}**", f"**{rng((runs_lo + add_lo) * 12, (runs_hi + add_hi) * 12)}**", f"**{rng((runs_lo + add_lo) * 12, (runs_hi + add_hi) * 12, usd)}**"],
    ["At the growth gate (Year-1 design point)", "₹50,000 – ₹70,000 + advanced lines", "$556 – $778 + advanced", "—", "—"],
    ["At scale (Year-2 design point)", "₹1.3 – 1.7 lakh + advanced lines", "$1,444 – $1,889 + advanced", "—", "—"],
])
t_ap, t_full = tco_total(tco_ap), tco_total(tco_full)
A(f"**Three-year total cost of ownership (build + 3 years of operation, maintenance and future-proofing):** approved path **{rng(*t_ap)}** ({rng(*t_ap, usd)}); full roadmap **{rng(*t_full)}** ({rng(*t_full, usd)}). See §12.\n")
A("![One-time development cost by package](img/packages.png)\n")
A("## 1.2 What drives the cost\n")
A(f"- **People dominate.** About **{people_c / (people_c + vendors_c + subs_c) * 100:.0f}%** of the approved-scope money (central) is the build team. External vendors (penetration tests, training content) are about **{vendors_c / (people_c + vendors_c + subs_c) * 100:.0f}%**. Subscriptions and running costs for the build plus 12 months of operation are about **{subs_c / (people_c + vendors_c + subs_c) * 100:.0f}%**.")
A(f"- **AI usage is small and capped.** All {len(by_kind['AG'])} AI agents together cost an estimated **{inr(ag_run[1])} per month** at pilot volume (base; {inr(ag_run[0])}–{inr(ag_run[2])}), inside the hard AI caps. Claude Sonnet stays the primary model (DEC-418).")
A("- **Subscriptions for building** are mainly developer seats, above all Claude for the engineers. The approved baseline has 2 Claude seats. The Founder approved Claude Code for all 6 engineers on 28 Nov 2026 (DEC-419). The extra cost is repaid if it saves about 1 engineer-day per engineer per month (§13.5).")
A("- **Lifecycle costs** after launch are maintenance (15–20% of development per year), future-proofing (model migrations, framework upgrades, security tests, DR drills) and running costs that step up only when the business passes the scale gates.\n")
A("![Where the money goes](img/share.png)\n")
A("## 1.3 Decisions already taken and still open\n")
table(["Item", "Status", "Reference"], [
    ["Core build budget (Ledger A) ₹52.68–84.08 L", "Approved", "DEC-230"],
    ["Pilot running budget (Ledger B) ₹19,895–26,335/month", "Approved", "DEC-231"],
    ["Literal-alignment work CR-ALN-01", "Approved (funded)", "DEC-416"],
    ["Advanced release A1 ≈ ₹28.0–55.4 L", "Approved", "DEC-417"],
    ["Claude Sonnet as primary model", "Approved", "DEC-418"],
    ["Phase-2 core continuation (W6) ₹25.8–38.7 L", "Open: decide at the Release 2 go/no-go", "Part 8.4"],
    ["Advanced A2 and A3", "Open: decide at gates G-A1 and G-A2", "DEC-411"],
    ["Build-time tooling (Claude for all engineers, GitHub, Figma, Workspace, Bitwarden, BrowserStack, domains)", "Approved 28 Nov 2026", "DEC-419; §7"],
    ["Items often missed (legal counsel, insurance, GST, etc.)", "Open: see §11", "§11"],
])

# 2 Basis
A("# 2. Estimation basis, method and assumptions\n")
A("## 2.1 Method\n")
table(["Technique", "Used for"], [
    ["**Top-down from approved budgets**", "Core build (Ledger A), alignment, A1: the figures the Founder approved (DEC-230, DEC-416, DEC-417)"],
    ["**Bottom-up by resource and calendar**", "Resource plan: FTE × months × loaded rate (§3, §4)"],
    ["**Effort-based (person-days)**", "Effort by activity, alignment and advanced packages, vendor scenarios (§5, §13)"],
    ["**Parametric**", "Build effort per AI agent, automation and workflow by complexity class (§6); drafting effort per user story and test case (§5.3)"],
    ["**Three-point (low / central / high)**", "Every line. Central = midpoint unless a blueprint central value exists"],
    ["**Unit pricing**", "Subscriptions and cloud: unit price × seats or volume, plus 15% contingency where the blueprint applies it"],
    ["**Scenario analysis (permutations)**", "Scope × team model × estimate point × FX × AI usage (§13)"],
])
A("## 2.2 Key parameters\n")
table(["Parameter", "Value", "Source"], [
    ["FX rate", f"₹{M.FX:.0f} per USD (sensitivity ₹85 / ₹95)", "Part 8.4 (verify)"],
    ["Loaded cost per person-month (India delivery)", f"{inr(M.PM_RATE[0])} – {inr(M.PM_RATE[1])} ({usd(M.PM_RATE[0])} – {usd(M.PM_RATE[1])})", "BRD §6"],
    ["Working days per month / hours per day", f"{M.DAYS_PER_MONTH} days / {M.HOURS_PER_DAY} hours = {M.HOURS_PER_MONTH} hours per month", "BRD §6"],
    ["Loaded cost per person-day", f"{inr(M.PD_RATE[0])} – {inr(M.PD_RATE[1])} ({usd(M.PD_RATE[0], 2)} – {usd(M.PD_RATE[1], 2)})", "Derived"],
    ["Loaded cost per hour", f"{inr(M.HR_RATE[0])} – {inr(M.HR_RATE[1])} ({usd(M.HR_RATE[0], 2)} – {usd(M.HR_RATE[1], 2)})", "Derived"],
    ["Contingency on running costs", "15% (line B11)", "BRD §6; DEC-004"],
    ["Management reserve (one-time)", f"{rng(*M.MGMT_RESERVE)}, held outside the totals, released only by change control", "Part 8.4"],
    ["GST", "18%, excluded from all totals (see the with-GST view in §11)", "Assumption"],
    ["Rate escalation from Year 2", "8% per year", "Assumption"],
    ["Plan of record", "Release 1 go/no-go Fri 4 Jun 2027 (Day 180); Release 2 build Fri 2 Jul 2027 (Day 208); W5 exit Fri 23 Jul 2027 (Day 229)", "DEC-228"],
])
A("## 2.3 What \"loaded cost\" includes\n")
A("Salary or contract fee, statutory benefits, paid leave, equipment allowance and management overhead for India-based delivery. It does not include recruitment fees, GST or travel (see §11).\n")

# 3 Rate card
A("# 3. Resource rate card (per hour, per day, per month)\n")
rows = []
for role, skills, tech, lo, hi, used in M.RATE_CARD:
    if lo == 0:
        rows.append([role, skills, tech, "Not costed", "—", "—", "—", used])
        continue
    rows.append([role, skills, tech, f"{inr(lo / M.HOURS_PER_MONTH)} – {inr(hi / M.HOURS_PER_MONTH)}", f"{usd(lo / M.HOURS_PER_MONTH, 2)} – {usd(hi / M.HOURS_PER_MONTH, 2)}",
                 f"{inr(lo / M.DAYS_PER_MONTH)} – {inr(hi / M.DAYS_PER_MONTH)}", f"{lakh(lo)} – {lakh(hi)} ({usd(lo)} – {usd(hi)})", used])
table(["Role", "Skill set", "Technology", "Per hour (INR)", "Per hour (USD)", "Per day (INR)", "Per month (INR, USD)", "Used in"], rows)
A(f"Role rates sit inside the BRD §6 loaded band of ₹1.0–1.5 lakh per person-month. The approved budgets use the band itself, so the totals do not depend on the role split. For other ways of sourcing the team (an Indian IT vendor, a hybrid model, or onshore contractors at ${M.ONSHORE_USD_HR[0]}–{M.ONSHORE_USD_HR[1]} per hour), see §13.2.\n")

# 4 Resource plan
A("# 4. Resource plan and development cost (one-time)\n")
A("## 4.1 Core build to the Release 2 gate (Ledger A, approved, DEC-230)\n")
rows = []
for r in la:
    rows.append([r["id"], r["item"], r["role"], f"{r['fte']:.1f}" if r["fte"] else "—", f"{r['months']:.2f}" if r["months"] else "—",
                 f"{r['pm']:.2f}" if r["pm"] else "—", ind(r["hours"]) if r["pm"] else "Fixed price",
                 f"{inr(r['hr_lo'])} – {inr(r['hr_hi'])}" if r["pm"] else "—", rng(r["lo"], r["hi"]), rng(r["lo"], r["hi"], usd), r["src"]])
pm_tot = sum(r["pm"] for r in la)
rows.append(["", "**Total Ledger A**", "", "", "", f"**{pm_tot:.2f}**", f"**{ind(pm_tot * M.HOURS_PER_MONTH)}**", "", f"**{rng(la_lo, la_hi)}**", f"**{rng(la_lo, la_hi, usd)}**", ""])
rows.append(["R", "Management reserve (outside the total)", "Change-control board", "", "", "", "", "", rng(*M.MGMT_RESERVE), rng(*M.MGMT_RESERVE, usd), "Part 8.4"])
table(["#", "Item", "Resource", "FTE", "Months", "Person-months", "Hours", "Rate per hour (INR)", "Cost (INR)", "Cost (USD)", "Source"], rows)
A("**Team composition (Option 2b, DEC-228/232).** 4 core engineers for Day 1–208, plus 2 contract engineers for Day 43–208, plus QA at 1.0 FTE from Sprint 3. A growth/compliance lead works 0.5 FTE, rising to 0.75 in W4–W5. A UX contractor, a DevOps front-load and an independent reviewer are also included. The Founder acts as Product Owner and is not costed. Peak team: about 8.5 FTE.\n")
A("## 4.2 Development cost by phase (core build)\n")
table(["Phase", "Days", "Dates", "Low (INR)", "High (INR)", "Low (USD)", "High (USD)"], [
    ["Sprint 0 and foundation (W0-A, W0-B)", "1–30", "Dec 2026", lakh(540_000), lakh(820_000), usd(540_000), usd(820_000)],
    ["Release 1 build (W1–W3 + Must enhancements)", "31–180", "Jan – 4 Jun 2027", lakh(3_730_000), lakh(5_900_000), usd(3_730_000), usd(5_900_000)],
    ["Release 2 build to gate (W4–W5)", "181–208", "Jun – 2 Jul 2027", lakh(1_000_000), lakh(1_690_000), usd(1_000_000), usd(1_690_000)],
    ["**Total**", "1–208", "", f"**{lakh(la_lo)}**", f"**{lakh(la_hi)}**", f"**{usd(la_lo)}**", f"**{usd(la_hi)}**"],
])
A("## 4.3 Further one-time packages\n")
rows = []
for k in ["ALN", "A1", "PH2", "A2", "A3"]:
    p = P[k]
    e = p[6]
    rows.append([p[1], p[2], p[7], " / ".join("—" if v is None else f"{v:,.0f}" for v in e), f"{(e[1] or 0) * M.HOURS_PER_DAY:,.0f}", rng(p[3], p[5]), rng(p[3], p[5], usd), p[8]])
table(["Package", "Status", "When", "Effort pd (low / central / high)", "Hours (central)", "Cost (INR)", "Cost (USD)", "Source"], rows)
A("**Advanced team (A1–A3).** The expert panels plan for about 6 FTE in A1:\n")
A("- 2 contract AI/LLM engineers;")
A("- 1 data/ML engineer;")
A("- 1 SRE/security engineer;")
A("- 2 full-stack engineers for revenue features;")
A("- QA and UX drawn from the core team.\n")
A("The team shrinks to about 3–4 FTE in A2 and 1–2 FTE in A3 (Parts 9.7b, 9.8b, 9.9b). Approved in principle for A1 (DEC-417); procurement starts at the Release 2 gate.\n")

# 5 Effort by activity and drafting
A("# 5. Effort by activity, including user stories, test strategy and test cases\n")
A("## 5.1 Effort and cost by activity\n")
A(f"Programme effort is **{core_eff[0]} / {core_eff[1]} / {core_eff[2]} person-days** for the core build (low/central/high) and **{prog_eff[0]:,.0f} / {prog_eff[1]:,.0f} / {prog_eff[2]:,.0f}** for the full programme. The table allocates the central effort by activity. It is an allocation of the same total, not an addition.\n")
rows = []
for name, share, who in M.ACTIVITY_SPLIT:
    c_pd = core_eff[1] * share
    f_pd = prog_eff[1] * share
    rows.append([name, f"{share * 100:.0f}%", f"{c_pd:,.0f}", f"{f_pd:,.0f}", f"{f_pd * M.HOURS_PER_DAY:,.0f}", rng(f_pd * M.PD_RATE[0], f_pd * M.PD_RATE[1]), rng(f_pd * M.PD_RATE[0], f_pd * M.PD_RATE[1], usd), who])
rows.append(["**Total**", "100%", f"**{core_eff[1]:,}**", f"**{prog_eff[1]:,.0f}**", f"**{prog_eff[1] * 8:,.0f}**", f"**{rng(prog_eff[1] * M.PD_RATE[0], prog_eff[1] * M.PD_RATE[1])}**", f"**{rng(prog_eff[1] * M.PD_RATE[0], prog_eff[1] * M.PD_RATE[1], usd)}**", ""])
table(["Activity", "Share", "Core build pd (central)", "Full programme pd (central)", "Hours", "Effort value (INR)", "Effort value (USD)", "Roles"], rows)
A("*Effort value* is effort × loaded day rate. Cash for an in-house team follows the calendar (§4), which also pays for meetings, onboarding and focus-factor losses.\n")
A("## 5.2 Volume of artefacts to produce\n")
table(["Artefact", "Count", "Where"], [
    ["User stories with Gherkin acceptance criteria", f"{M.ARTEFACTS['stories']} ({M.ARTEFACTS['stories_core']} core + {M.ARTEFACTS['stories_enh']} source-pack + {M.ARTEFACTS['stories_adv']} advanced)", "Parts 5, 2.6–8.3, 9.7–9.9"],
    ["Test cases and verification items (functional, NFR, AI evaluation, enhancement, alignment)", f"{M.ARTEFACTS['test_cases']:,}", "Parts 6, 6.8–6.10, 9.6–9.10"],
    ["Source-pack tests mapped (unit 75, SIT 422, UAT 302)", f"{M.ARTEFACTS['source_tests']}", "Part 6.8"],
    ["Functional requirements", f"{M.ARTEFACTS['frs']} (181 + 180 enhancement + 240 advanced)", "Parts 2.1, enhancement parts, 9.7–9.9"],
    ["Screens", f"{M.ARTEFACTS['screens']} (147 + 71 advanced)", "Parts 2.5, 2.7, 9.7–9.9"],
    ["API operations", f"{M.ARTEFACTS['apis']}", "Parts 3.2, 3.5"],
    ["AI agents / automations / workflows", f"{len(by_kind['AG'])} / {len(by_kind['AU'])} / {len(by_kind['WF'])}", "Part 9.4"],
])
A("## 5.3 Drafting effort: user stories, test cases and test strategies\n")
A("Three ways of working are compared:\n")
A("- **(a) from scratch, manually;**")
A("- **(b) AI-assisted drafting** with Claude, with a human writing and reviewing;")
A("- **(c) refining the drafts already in this blueprint.** All stories, acceptance criteria and test cases exist in draft and need review, refinement and estimation with the team.\n")
A("Option (c) is the plan of record. It is already inside the programme effort (§5.1, activities \"Requirements…\" and \"Test strategy…\").\n")
rows = []
for d in draft:
    rows.append([d["name"], f"{d['n']:,}", f"{d['man'][0] / 8:,.0f} – {d['man'][1] / 8:,.0f}", f"{d['ai'][0] / 8:,.0f} – {d['ai'][1] / 8:,.0f}", f"{d['bp'][0] / 8:,.0f} – {d['bp'][1] / 8:,.0f}",
                 rng(d["bp"][0] / 8 * M.PD_RATE[0], d["bp"][1] / 8 * M.PD_RATE[1]), d["who"]])
rows.append(["Test strategies and plans (§5.4)", f"{sum(c for _, c, _ in M.STRATEGY_DOCS)} documents", f"{strat_lo:.0f} – {strat_hi:.0f}", f"{strat_lo * 0.6:.0f} – {strat_hi * 0.6:.0f}", f"{strat_lo * 0.35:.0f} – {strat_hi * 0.35:.0f}",
             rng(strat_lo * 0.35 * M.PD_RATE[0], strat_hi * 0.35 * M.PD_RATE[1]), "QA lead"])
tm = [sum(d["man"][i] for d in draft) / 8 + (strat_lo, strat_hi)[i] for i in (0, 1)]
ta = [sum(d["ai"][i] for d in draft) / 8 + (strat_lo, strat_hi)[i] * 0.6 for i in (0, 1)]
tb = [sum(d["bp"][i] for d in draft) / 8 + (strat_lo, strat_hi)[i] * 0.35 for i in (0, 1)]
rows.append(["**Total**", "", f"**{tm[0]:,.0f} – {tm[1]:,.0f}**", f"**{ta[0]:,.0f} – {ta[1]:,.0f}**", f"**{tb[0]:,.0f} – {tb[1]:,.0f}**", f"**{rng(tb[0] * M.PD_RATE[0], tb[1] * M.PD_RATE[1])}**", ""])
table(["Artefact", "Count", "(a) Manual pd", "(b) AI-assisted pd", "(c) Refine blueprint drafts pd (plan)", "Cost of (c), INR", "Who"], rows)
A(f"Unit assumptions (hours per item, manual / AI-assisted / refine): user story 2.0–3.5 / 1.0–1.75 / 0.5–0.9; test case 0.33–0.5 / 0.15–0.25 / 0.08–0.15; source-test mapping 0.10–0.20 / 0.05–0.10 / 0.03–0.06. **Saving of (c) against (a): about {tm[0] - tb[0]:,.0f}–{tm[1] - tb[1]:,.0f} person-days ({rng((tm[0] - tb[0]) * M.PD_RATE[0], (tm[1] - tb[1]) * M.PD_RATE[1])}).**\n")
A("## 5.4 Test strategy documents to produce\n")
table(["Document", "Count", "pd each (manual)", "Notes"], [[n, c, f"{r[0]}–{r[1]}", "Drafts exist in Part 6.1 and Parts 6.8–6.10; refine per release"] for n, c, r in M.STRATEGY_DOCS])

# 6 AI catalogue
A("# 6. AI agents, automations and workflows: what they do, how automated, build and run cost, timeline\n")
A(f"The blueprint defines **{len(by_kind['AG'])} AI agents, {len(by_kind['AU'])} automations and {len(by_kind['WF'])} business workflows**, {len(cat)} items in total (Part 9.4).\n")
A("- **AI agents** use Claude through the model gateway. They draft, classify, extract, match and summarize; they never sign, pay, submit bids or set prices.")
A("- **Automations** are deterministic rules with no AI model.")
A("- **Workflows** orchestrate agents, automations and people, with human approval at consequential steps.\n")
A("![Catalogue by release](img/catalogue.png)\n")
A("## 6.1 Summary\n")
rows = []
for k in kinds:
    s = by_kind[k]
    rows.append([kinds[k], len(s), sum(1 for i in s if i["origin"].startswith("v1.0")), sum(1 for i in s if i["origin"].startswith("v1.1")),
                 f"{sum(i['pd_lo'] for i in s):,.0f} – {sum(i['pd_hi'] for i in s):,.0f}", rng(sum(i['cost_lo'] for i in s), sum(i['cost_hi'] for i in s)),
                 rng(sum(i['cost_lo'] for i in s), sum(i['cost_hi'] for i in s), usd),
                 f"{inr(sum(i['run_base'] for i in s))} ({inr(sum(i['run_lo'] for i in s))} – {inr(sum(i['run_hi'] for i in s))})" if k == "AG" else "Inside hosting (B01)"])
rows.append(["**Total**", len(cat), "", "", f"**{cat_pd_lo:,.0f} – {cat_pd_hi:,.0f}**", f"**{rng(sum(i['cost_lo'] for i in cat), sum(i['cost_hi'] for i in cat))}**", f"**{rng(sum(i['cost_lo'] for i in cat), sum(i['cost_hi'] for i in cat), usd)}**", f"**{inr(ag_run[1])}/month AI (base)**"])
table(["Type", "Count", "v1.0 baseline", "v1.1 advanced", "Build effort pd", "Build cost (INR)", "Build cost (USD)", "Run cost per month (INR, pilot)"], rows)
A("Build effort per item is a **parametric allocation inside the programme effort** (§5), not an extra cost. Complexity classes and person-days:\n")
A("| Type | Simple | Medium | Complex |\n|---|---|---|---|")
A("| AI agent | 2–3 pd | 4–6 pd | 7–10 pd |")
A("| Automation | 0.5–1 pd | 1–2 pd | 2.5–4 pd |")
A("| Workflow | 3–5 pd | 5–8 pd | 8–12 pd |")
A("")
A("Each estimate covers the prompt or rule contract, code, guardrails, evaluation or test set, and review UI hook. Screens shared with the module are excluded. AI run cost is the agent's own token formula at pilot volumes (Parts 7.2, 7.4b, 9.7b–9.9b), before a 25% overhead allowance.\n")
lv = collections.Counter((i["kind"], i["level"]) for i in cat)
A("## 6.2 Fully or partially automated\n")
table(["Automation level", "AI agents", "Automations", "Workflows", "Meaning"], [
    [lvl, lv.get(("AG", lvl), 0), lv.get(("AU", lvl), 0), lv.get(("WF", lvl), 0), mean]
    for lvl, mean in [
        ("Fully automated (deterministic rules within policy guardrails)", "Runs without a person, inside the Policy Decision Point; audited"),
        ("Fully automated within guardrails (post-hoc review)", "AI acts on low-risk internal items; a person reviews afterwards (L3)"),
        ("Mostly automated (acts; human reviews after)", "AI acts; a person can reverse (L2)"),
        ("Partially automated (AI drafts; human approves before use)", "AI prepares; a person approves before anything leaves the system (L1)"),
        ("Partially automated (rule engine prepares; human confirms)", "Rules prepare an action; a person confirms"),
        ("Assistive only (suggests; human acts)", "Suggestions only (L0)"),
        ("Partially automated (orchestrated end to end; human approval at consequential steps)", "End-to-end orchestration; consequential steps (quotes, contracts, bids, payments) always need a person (DEC-064)"),
    ]])
A("## 6.3 Timeline by release\n")
rows = []
for rk, (rname, days, dates) in C.RELEASES.items():
    s = [i for i in cat if i["rk"] == rk]
    if not s:
        continue
    rows.append([rname, days, dates, sum(1 for i in s if i["kind"] == "AG"), sum(1 for i in s if i["kind"] == "AU"), sum(1 for i in s if i["kind"] == "WF"),
                 f"{sum(i['pd_lo'] for i in s):,.0f} – {sum(i['pd_hi'] for i in s):,.0f}", rng(sum(i['cost_lo'] for i in s), sum(i['cost_hi'] for i in s))])
table(["Release", "Days", "Dates", "Agents", "Automations", "Workflows", "Build pd", "Build cost (INR)"], rows)
A("## 6.4 Skills and technology used\n")
table(["Type", "Skill set", "Technology"], [[kinds[k], C.SKILLS[k], C.TECH[k]] for k in kinds])
for k in kinds:
    A(f"## 6.{5 + list(kinds).index(k)} Full list: {kinds[k]} ({len(by_kind[k])})\n")
    rows = []
    for i in by_kind[k]:
        rc = f"{inr(i['run_base'])} ({inr(i['run_lo'])}–{inr(i['run_hi'])})" if k == "AG" else "In B01"
        rows.append([i["id"], i["name"], i["what"], i["level"].split(" (")[0], i["autonomy"] if k != "WF" else "L1 gates", i["tier"] if k == "AG" else "—",
                     i["complexity"], f"{i['pd_lo']:g}–{i['pd_hi']:g}", f"{rng(i['cost_lo'], i['cost_hi'], inr)}", f"{usd(i['cost_lo'])}–{usd(i['cost_hi'])}", rc,
                     f"{i['release']} ({i['dates']})"])
    table(["ID", "Name", "What it does", "Automation", "Autonomy", "Model tier", "Complexity", "Build pd", "Build cost INR", "Build cost USD", "Run INR/month", "Release and timeline"], rows,
          [5, 11, 34, 8, 9, 8, 6, 4, 9, 7, 8, 9])

# 7 Subscriptions during build
A("# 7. Subscriptions and tools needed to build the application\n")
A("## 7.1 Development-period tooling (per month)\n")
A("Prices are USD list prices per user per month, as known on the document date. **Verify at the time of purchase**; annual billing is usually cheaper. INR at ₹90 per USD.\n")
rows = []
for r in tool_rows:
    rows.append([r["name"], r["purpose"], r["plan"], f"{usdv(r['ulo'], 2)}–{usdv(r['uhi'], 2)}" if r["uhi"] != r["ulo"] else usdv(r["ulo"], 2), r["seats"],
                 f"{usdv(r['mlo'])}–{usdv(r['mhi'])}" if r["mhi"] != r["mlo"] else usdv(r["mlo"]), f"{inr(r['mlo'] * M.FX)}–{inr(r['mhi'] * M.FX)}" if r["mhi"] != r["mlo"] else inr(r["mlo"] * M.FX), r["req"], r["note"]])
table(["Tool", "Purpose", "Plan", "Unit $/user/month", "Seats (build)", "Per month (USD)", "Per month (INR)", "Status", "Notes"], rows)
A(f"- **Approved baseline:** {usdv(baseline_usd)} per month. This is 2 Claude seats plus delivery-team API use; it is already in Ledger B lines B09 and B23.")
A(f"- **Approved additions (DEC-419, 28 Nov 2026):** {rng(rec_lo, rec_hi, usdv)} per month ({rng(rec_lo * M.FX, rec_hi * M.FX, inr)}). Over the 8 core build months that is **{rng(rec_lo * 8, rec_hi * 8, usdv)}** ({rng(rec_lo * 8 * M.FX, rec_hi * 8 * M.FX)}).")
A(f"- **Optional:** Slack, {rng(opt_lo, opt_hi, usdv)} per month.")
A(f"- **Lean alternative:** Claude Pro for all 9 users instead of Max for engineers. This lowers the Claude line by {usdv(600 + 20 - lean_claude)} per month.\n")
A("## 7.2 Claude plans compared (for the build team)\n")
table(["Option", "Seats", "Per month (USD)", "Per month (INR)", "When to choose"], [
    ["Approved baseline: Claude Pro × 2", "2", "$40", inr(40 * M.FX), "Minimum: two engineers use Claude Code"],
    ["Lean: Claude Pro × 9 (all team members)", "9", "$180", inr(180 * M.FX), "Everyone drafts with Claude; lighter Claude Code use"],
    ["**Approved (DEC-419): Claude Max 5x × 6 engineers + Pro × 3**", "9", "**$660**", f"**{inr(660 * M.FX)}**", "Daily Claude Code use by all engineers (higher usage limits)"],
    ["Heavy: Claude Max 20x × 6 engineers + Pro × 3", "9", "$1,260", inr(1260 * M.FX), "Very heavy agentic coding"],
    ["Team plan (Standard seats + premium seats for engineers)", "9", "≈ $30 per standard seat, ≈ $150 per premium seat (verify)", "—", "If central billing, SSO and admin controls are required"],
])
A("The production application uses the **Claude API** (pay as you go, metered by the model gateway). It does not use the chat subscriptions above. API usage is in Ledger B lines B02 (production, hard cap ₹3,000) and B23 (delivery team, ≈ ₹1,000).\n")
A("## 7.3 Cloud and providers during the build (approved Ledger B ramp)\n")
table(["Month", "Lines active", "Per month incl. 15% and seats (INR)", "Per month (USD)"], [
    ["Dec 2026", "B01, B02 cap, B07, B20, B23", rng(15_410, 18_055, inr), rng(15_410, 18_055, usd)],
    ["Jan 2027", "+ B03, B04", rng(18_285, 20_930, inr), rng(18_285, 20_930, usd)],
    ["Feb 2027", "+ B05, B21", rng(20_355, 23_575, inr), rng(20_355, 23_575, usd)],
    ["Mar 2027", "+ B10", rng(21_505, 24_725, inr), rng(21_505, 24_725, usd)],
    ["Apr 2027", "+ B06", rng(23_805, 27_025, inr), rng(23_805, 27_025, usd)],
    ["May – Jul 2027", "All lines", rng(runs_lo, runs_hi, inr), rng(runs_lo, runs_hi, usd)],
    ["**Total Day 1–208**", "", f"**{rng(*B_DURING_BUILD)}**", f"**{rng(*B_DURING_BUILD, usd)}**"],
])

# 8 Subscriptions after build
A("# 8. Subscriptions and running costs after the build (recurring)\n")
A("## 8.1 Pilot running cost by line (approved Ledger B, DEC-231)\n")
rows = []
for line, catg, item, billing, lo, hi, start, nature in M.LEDGER_B:
    rows.append([line, catg, item, billing, rng(lo, hi, inr) if lo != hi else inr(lo), rng(lo, hi, usd) if lo != hi else usd(lo), rng(lo * 12, hi * 12, inr), start, nature])
rows.append(["", "", "**Base subtotal**", "", f"**{rng(base_lo, base_hi, inr)}**", f"**{rng(base_lo, base_hi, usd)}**", f"**{rng(base_lo * 12, base_hi * 12, inr)}**", "", ""])
rows.append(["B11", "Contingency", "15% on the base", "", rng(base_lo * 0.15, base_hi * 0.15, inr), rng(base_lo * 0.15, base_hi * 0.15, usd), "", "", ""])
rows.append(["B09", "Seats", "Claude seats (2 × $20, × 1.15)", "Fixed subscription", inr(M.SEATS_B09), usd(M.SEATS_B09), inr(M.SEATS_B09 * 12), "Dec 2026", "Subscription"])
rows.append(["", "", "**Total pilot running (with contingency and seats)**", "", f"**{rng(runs_lo, runs_hi, inr)}**", f"**{rng(runs_lo, runs_hi, usd)}**", f"**{rng(runs_lo * 12, runs_hi * 12, inr)}**", "", ""])
table(["Line", "Category", "Item", "Billing", "Per month (INR)", "Per month (USD)", "Per year (INR)", "Active from", "Nature"], rows)
A("## 8.2 Optional and conditional lines\n")
table(["Line", "Item", "Per month (INR)", "Per month (USD)", "When"], [[l, it, rng(lo, hi, inr) if lo else "Per use / pass-through", rng(lo, hi, usd) if lo else "—", w] for l, it, lo, hi, w in M.LEDGER_B_OPTIONAL])
A("## 8.3 Running-cost additions from v1.1 (alignment and advanced releases)\n")
table(["Line", "Item", "Per month (INR)", "Per month (USD)", "From", "Status"], [[l, it, rng(lo, hi, inr), rng(lo, hi, usd), f, s] for l, it, lo, hi, f, s in M.RUN_ADDITIONS])
A("## 8.4 Running cost as the business scales\n")
table(["Stage", "Hosting", "AI ceiling", "Typical total per month (INR)", "Per month (USD)", "Gate"], [[s, h, a, rng(*t, inr), rng(*t, usd), g] for s, h, a, t, g in M.SCALE_STAGES])
A("External SaaS tenants pay for their own AI, messaging and storage use through their plan and metered overage (DEC-008, DEC-047). Their usage is never charged to the platform's B02 line.\n")
A("## 8.5 Tools after the build (maintenance team)\n")
A(f"After the build the tooling seats fall to the maintenance team: about 2 engineers, a part-time QA, the growth lead and the PO. The approved tooling then costs **{rng(after_lo, after_hi, usdv)} per month** ({rng(after_lo * M.FX, after_hi * M.FX, inr)}), in addition to Ledger B.\n")

# 9 Cash flow
A("# 9. Timeline and month-by-month cash flow (approved scope)\n")
table(["Milestone", "Day", "Date"], [
    ["Programme start, Sprint 0", "1", "Dec 2026"],
    ["Foundation gates", "15 and 30", "Dec 2026 – Jan 2027"],
    ["Release 1 go/no-go", "180", "Fri 4 Jun 2027"],
    ["Release 2 build gate", "208", "Fri 2 Jul 2027"],
    ["W5 exit after 30-day monitored pilot", "229", "Fri 23 Jul 2027"],
    ["Advanced A1", "≈ 239–365", "Aug – Dec 2027"],
    ["Advanced A2 (if approved at G-A1)", "≈ 366–480", "Dec 2027 – Mar 2028"],
    ["Advanced A3 (after the scale gate)", "≈ 481–600", "Apr – Jul 2028"],
])
rows = []
for r in cash:
    rows.append([r["m"], lakh(r["dev"][1]), inr(r["run"][1]), inr(r["tools"][1]), lakh(r["tot"][1]), lakh(r["cum"][1]), rng(r["cum"][0], r["cum"][2]), usd(r["cum"][1])])
table(["Month", "Development (central)", "Running (central)", "Approved tools (central)", "Month total", "Cumulative (central)", "Cumulative range", "Cumulative (USD)"], rows)
A("![Cumulative cash flow](img/cashflow.png)\n")

# 10 Future-proofing
A("# 10. Future-proofing and lifecycle costs (annual, after launch)\n")
rows = []
for name, basis, lo, hi in fp_rows:
    if lo is None:
        rows.append([name, basis, "See §12 (applied to cumulative development)", "—"])
    else:
        rows.append([name, basis, rng(lo, hi), rng(lo, hi, usd)])
rows.append(["**Total future-proofing per year (excluding maintenance %)**", "", f"**{rng(fp_lo, fp_hi)}**", f"**{rng(fp_lo, fp_hi, usd)}**"])
table(["Item", "Basis", "Per year (INR)", "Per year (USD)"], rows)
cd = (P["CORE"][3] + P["ALN"][3], P["CORE"][5] + P["ALN"][5])
A(f"**Maintenance and support** on the core build and alignment: 15–20% of {rng(*cd)} = **{rng(0.15 * cd[0], 0.20 * cd[1])} per year** ({rng(0.15 * cd[0], 0.20 * cd[1], usd)}). This rises with each advanced release that goes live.\n")
A("**Why these matter.** Several things change underneath the platform over its life:\n")
A("- **Models.** Claude versions change roughly yearly. The evaluation suites (774 AI evaluation cases) make a migration a measured task, not a rewrite.")
A("- **Frameworks.** Django, React and PostgreSQL release long-term-support versions on fixed cycles.")
A("- **Rules and expectations.** Security expectations and DPDP rules evolve.\n")
A("Budgeting these items each year keeps the platform supportable and avoids a costly rebuild.\n")

# 11 Missed items
A("# 11. Items often missed, and how they are treated\n")
table(["Item", "What it is", "Treatment in this estimate", "Indicative cost"], [list(r) for r in M.MISSED])
A("## 11.1 With-GST view (indicative)\n")
table(["Item", "Excluding GST", "GST 18%", "Including GST"], [
    ["Approved one-time development (central)", lakh(ap_c), lakh(ap_c * M.GST), lakh(ap_c * (1 + M.GST))],
    ["Pilot running per month (high)", inr(runs_hi), inr(runs_hi * M.GST), inr(runs_hi * (1 + M.GST))],
    ["Approved tooling per month (high)", inr(rec_hi * M.FX), inr(rec_hi * M.FX * M.GST), inr(rec_hi * M.FX * (1 + M.GST))],
])
A("GST on salaries does not apply. GST on contractor, vendor and SaaS invoices is usually recoverable as input tax credit for a GST-registered company. Confirm with the finance advisor.\n")

# 12 TCO
A("# 12. Three-year total cost of ownership\n")
for title, t in (("Approved path: core + alignment + A1", tco_ap), ("Full roadmap: core + alignment + A1 + A2 + A3 + Phase 2", tco_full)):
    A(f"## 12.{1 if t is tco_ap else 2} {title}\n")
    rows = []
    for y in t:
        tot = (y[1][0] + y[2][0] + y[3][0] + y[4][0] + y[5][0], y[1][1] + y[2][1] + y[3][1] + y[4][1] + y[5][1])
        rows.append([y[0], rng(*y[1]), rng(*y[2]), rng(*y[3]), rng(*y[4]), rng(*y[5]), f"**{rng(*tot)}**", rng(*tot, usd)])
    tt = tco_total(t)
    rows.append(["**Total (build + 3 years)**", "", "", "", "", "", f"**{rng(*tt)}**", f"**{rng(*tt, usd)}**"])
    table(["Year", "Development (one-time)", "Running and subscriptions", "Tooling seats", "Maintenance", "Future-proofing", "Total (INR)", "Total (USD)"], rows)
A("Year 2 and Year 3 assume the growth and scale gates pass, because the running costs step up only then. Maintenance is 15% (low) or 20% (high) of cumulative development, with 8% annual escalation. If the gates do not pass, running costs stay at pilot level and these years cost less.\n")

# 13 Scenarios
A("# 13. Permutations and combinations: scenario analysis\n")
A("## 13.1 Scope packages × estimate point (in-house team, INR)\n")
rows = []
for sid, sname, keys in M.SCOPE_PACKAGES:
    rows.append([sid, sname, " + ".join(keys), f"{M.effort_pd(keys, 'central'):,.0f}", lakh(M.cost(keys, "low")), lakh(M.cost(keys, "central")), lakh(M.cost(keys, "high")), usd(M.cost(keys, "central"))])
table(["Scope", "Description", "Packages", "Effort pd (central)", "Low", "Central", "High", "Central (USD)"], rows)
A("## 13.2 Team sourcing models × scope (central)\n")
rows = []
for sid, sname, keys in M.SCOPE_PACKAGES:
    r = [sid]
    for tid, tname, mult, basis in M.TEAM_MODELS:
        v = next(s for s in scen if s["sid"] == sid and s["tid"] == tid and s["pt"] == "central")["inr"]
        r.append(f"{lakh(v)} ({usd(v)})")
    rows.append(r)
table(["Scope"] + [f"{t[0]}: {t[1]}" for t in M.TEAM_MODELS], rows)
table(["Model", "Basis"], [[f"{t[0]} {t[1]}", t[3]] for t in M.TEAM_MODELS])
A(f"All {len(scen)} combinations (6 scopes × 4 team models × 3 estimate points) are in the workbook sheet *Scenarios*, with FX sensitivity.\n")
A("## 13.3 FX sensitivity (approved one-time development, central)\n")
table(["₹ per USD", "Approved development (USD)", "Approved tooling per month (INR)"], [[f"₹{f:.0f}", f"${ap_c / f:,.0f}", f"{inr(rec_lo * f)} – {inr(rec_hi * f)}"] for f in M.FX_SENS])
A("## 13.4 AI usage scenarios (production inference)\n")
table(["Scenario", "AI per month (INR)", "AI per month (USD)", "Notes"], [
    ["All agents at pilot base volumes (catalogue estimate)", inr(ag_run[1] * 1.25), usd(ag_run[1] * 1.25), "Sum of the 80 agents' base cost + 25% overhead"],
    ["All agents at pilot high volumes / heavier Sonnet escalation", inr(ag_run[2] * 1.25), usd(ag_run[2] * 1.25), "High column of each agent"],
    ["Approved hard caps: B02 ₹3,000 + B23 ₹1,000 + B24 ₹2,000", inr(6_000), usd(6_000), "The gateway stops paid calls at the cap (M53); work degrades to Tier 0/3"],
    ["Growth gate ceiling", inr(12_000), usd(12_000), "DEC-008, after the scale gate"],
    ["Scale ceiling", inr(40_000), usd(40_000), "DEC-008, Year-2 design point"],
])
A("## 13.5 Does buying Claude for every engineer pay back?\n")
eng_month = 6 * M.mid(M.PM_RATE)
upg = (660 - 40) * M.FX
table(["Productivity gain on engineering time", "Value per month (INR)", "Extra Claude cost per month (INR)", "Net per month (INR)"], [[f"{g}%", inr(eng_month * g / 100), inr(upg), inr(eng_month * g / 100 - upg)] for g in (0, 5, 10, 20)])
A(f"Six engineers cost about {inr(eng_month)} per month (central). The upgrade pays back above about **{upg / eng_month * 100:.1f}%** productivity gain, roughly 1 engineer-day per engineer per month.\n")
A("## 13.6 Other combinations considered\n")
table(["Combination", "Effect on cost", "Recommendation"], [
    ["Release 1 only, stop before Release 2", "Saves ≈ ₹10–17 L of the core build; loses WF-11–14 (close, onboarding, plans, offboarding)", "Not recommended: Release 2 completes the revenue loop"],
    ["Option 1 staffing (no contract engineers)", "Saves ₹10.9–16.4 L; Release 1 moves to ≈ Day 236 (30 Jul 2027)", "Superseded by Option 2b (DEC-228)"],
    ["Skip alignment (stay at 98.7% match)", "Saves ₹2.8–11.6 L", "Not recommended: Founder asked for 100% (DEC-416)"],
    ["A1 only, no A2/A3", "Saves ₹50.2–87.6 L", "Decide at gate G-A1 with A1 results"],
    ["Self-hosted model first instead of Claude Sonnet primary", "May save part of B02 at scale; adds ₹4,600–13,800/month for a local-inference server and quality risk", "Not chosen (DEC-418)"],
    ["Paid enrichment (Apollo) from day one", "+ ₹10,350/month", "Only after the scale gate"],
    ["Fargate + ALB + ElastiCache at pilot (DEC-243)", "+ ₹4,500–8,000/month", "Conditional; otherwise at the scale gate"],
    ["RDS Multi-AZ from day one", "+ ₹2,875–6,900/month", "Only if availability < 99.9% two months running"],
])

# 14 Risks
A("# 14. Risks to the estimate and how they are controlled\n")
table(["Risk", "Effect", "Control"], [
    ["Scope growth during build", "Effort beyond 722 pd central", "Change-control board; management reserve ₹3.94–8.29 L; Sprint 3 and Sprint 7 re-estimates"],
    ["Vendor and SaaS price changes", "Subscriptions rise", "Verify before purchase; annual billing; open-source alternatives listed"],
    ["FX movement", "USD-billed items rise in INR", "5% FX buffer (§10); sensitivity (§13.3)"],
    ["AI usage above plan", "B02/B23/B24 exceed expectation", "Hard caps in the gateway; alerts at 70/90/100%"],
    ["Hiring delays for contract engineers", "Schedule slip", "Procurement starts in Sprint 0 (A1 team at Day 208)"],
    ["Legal requirements discovered late", "Rework", "Legal backlog in Sprint 0; legal counsel line in §11"],
    ["Scale arrives faster than planned", "Running cost steps up early", "Running cost rises only through approved scale gates; tenant plans carry their own cost"],
])

# 15 Assumptions
A("# 15. Assumptions, exclusions and verification list\n")
table(["#", "Assumption or exclusion"], [[i + 1, t] for i, t in enumerate([
    "Figures are estimates as of 28 Nov 2026; the approved budgets (DEC-230/231, DEC-416/417) govern where they differ.",
    "₹90 = $1 for conversion; all USD amounts are converted from INR (or INR from USD list prices) at this rate.",
    "Loaded India delivery rates of ₹1.0–1.5 lakh per person-month; 22 working days; 8 hours per day.",
    "GST, Founder time, paid ad media, external legal counsel and customer-funded tenant usage are excluded from totals.",
    "Third-party prices (Claude plans, GitHub, Figma, Google Workspace, BrowserStack, Bitwarden, AWS) are list prices to verify at purchase.",
    "Per-item build effort for agents, automations and workflows is a parametric allocation within programme effort.",
    "AI run cost per agent comes from each agent's token formula at pilot volumes; production is capped by the gateway.",
    "A2/A3 cost is split pro rata to effort (A2 64.7%, A3 35.3%) from the panels' per-release tables.",
    "Advanced running costs ramp 35% in A1, 70% in A2 and 100% after A3.",
    "Maintenance at 15–20% of cumulative development per year; 8% annual escalation from Year 2.",
    "Year-2 and Year-3 running costs assume the growth and scale gates pass.",
    "Drafting productivity factors (AI-assisted, refine blueprint drafts) are planning assumptions to validate in Sprint 1.",
])])

# 16 Glossary
A("# 16. Glossary\n")
table(["Term", "Meaning"], [
    ["Ledger A / Ledger B", "Approved one-time development budget / approved recurring running budget (Part 8.4)"],
    ["pd / PM / FTE", "Person-day / person-month / full-time equivalent"],
    ["Loaded rate", "Cost of a person including benefits, leave, equipment and overhead"],
    ["A1 / A2 / A3", "Advanced releases after Release 2 (Part 9.10)"],
    ["AG / AU / WF", "AI agent / deterministic automation / business workflow"],
    ["L0–L3", "Autonomy levels: suggest / draft for approval / act with post-review / act within guardrails"],
    ["B01–B24", "Running-cost lines in Ledger B"],
    ["CR-ALN-01 / 02", "Change requests for literal alignment: one-time / recurring"],
    ["Scale gate", "BRD §8 test (cost per qualified opportunity, consent compliance, conversion) before running costs step up"],
    ["TCO", "Total cost of ownership"],
])
A("**End of document.**")

md = "\n".join(DOC) + "\n"
(OUT / f"{NAME}.md").write_text(md, encoding="utf-8")
print("MD written", len(md))

# expose for the workbook builder
DATA = dict(cat=cat, la=la, tool_rows=tool_rows, scen=scen, cash=cash, tco_ap=tco_ap, tco_full=tco_full, fp_rows=fp_rows, draft=draft,
            strat=(strat_lo, strat_hi), runs=(runs_lo, runs_hi), base=(base_lo, base_hi), adv=(adv_lo, adv_hi), aln_run=aln_run,
            ap=(ap_lo, ap_c, ap_hi), all=(all_lo, all_c, all_hi), rec=(rec_lo, rec_hi), after=(after_lo, after_hi), ag_run=ag_run,
            prog_eff=prog_eff, core_eff=core_eff, B_DURING_BUILD=B_DURING_BUILD)

if __name__ == "__main__":
    import build_xlsx
    build_xlsx.build(DATA, OUT / f"{NAME}.xlsx")
    env = {**os.environ, "LANG": "C.UTF-8", "LC_ALL": "C.UTF-8"}
    subprocess.run([str(BP / "make_pdf.sh"), f"{NAME}.md", "Cost Estimate v1.0 · 28 Nov 2026 · Confidential"], cwd=OUT, check=True, env=env)
    import build_docx
    build_docx.build(OUT / f"{NAME}.md", OUT / f"{NAME}.docx")
