#!/usr/bin/env python3
"""Excel version of the final cost sheet v1.1 (₹90,00,000 package), with live formulas driven by the Inputs sheet.

Usage: python3 blueprint/estimation/build_cost_sheet_xlsx.py
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import build_cost_sheet_v11 as S  # noqa: E402
import build_solo_quote_v2 as Q  # noqa: E402
import ai_model as X  # noqa: E402
from openpyxl import Workbook  # noqa: E402
from openpyxl.styles import Font  # noqa: E402
from openpyxl.workbook.defined_name import DefinedName  # noqa: E402
from build_xlsx import INP, TOT, NAVY, header, style_rows, title  # noqa: E402

OUT = S.OUT / "AI_Growth_Engine_Final_Cost_Sheet_Solo_AI_v1.1.xlsx"


def name(wb, nm, ref):
    wb.defined_names[nm] = DefinedName(nm, attr_text=ref)


def main():
    wb = Workbook()
    ws = wb.active
    ws.title = "README"
    title(ws, "AI Growth Engine – Final Cost Sheet v1.1 (solo builder with AI) · 28 Nov 2026",
          "Companion to the PDF/Word cost sheet. Edit yellow cells on 'Inputs'; the cost sheet, fee build-up and payment schedule recalculate.")
    for i, t in enumerate([
        "Package: Core platform (Releases 1 and 2) + Advanced A1, built by one builder with AI models and AI agents. Build ≈ 44 months + first 12 months of operation.",
        "A (development fee) and B (retainer) are fixed prices. C1–C4 are client-owned costs paid at actuals (estimates inside the package).",
        "The development fee is the package target minus the retainer and the at-cost estimates; the discount is the optimized fee minus that fee.",
        "Sheets: Inputs · Cost Sheet · Fee Build-up · Effort by Activity · Optimization · Build Subscriptions · Running Subscriptions · AI Catalogue · Payment Schedule · Future Options · Technology & Skills · Assumptions",
        "All figures exclude GST unless stated. Prices are list prices as of 28 Nov 2026; verify at purchase.",
    ], 4):
        ws.cell(row=i, column=1, value=t)
    ws.column_dimensions["A"].width = 160

    # ---------------------------------------------------------------- Inputs
    wi = wb.create_sheet("Inputs")
    title(wi, "Inputs (edit the yellow cells)")
    header(wi, 3, ["Name", "Parameter", "Value"], [14, 64, 16])
    inputs = [
        ("PACKAGE", "All-inclusive package target, excl. GST (₹)", S.PACKAGE),
        ("FX", "₹ per USD", S.FX),
        ("PM_RATE", "Builder's rate per month (₹)", 125_000),
        ("DAYS", "Working days per month (rate basis)", 22),
        ("PROD_DAYS", "Productive days per month (duration basis)", Q.PROD_DAYS),
        ("PD_CORE", "Builder's effort with AI, Core (days)", round(S.C["pd"], 2)),
        ("PD_A1", "Builder's effort with AI, Advanced A1 (days)", round(S.A1["pd"], 2)),
        ("TOK_CORE", "Claude tokens for coding agents, Core, before optimization (₹)", round(Q.CORE["tokens"])),
        ("TOK_A1", "Claude tokens for coding agents, A1, before optimization (₹)", round(Q.A1["tokens"])),
        ("TOK_RED", "Token reduction from caching and Haiku", 0.20),
        ("CONT", "Contingency on time and tokens", 0.10),
        ("FEE_OPT", "Optimized fee before discount (₹)", S.FEE_OPT),
        ("RET_M", "Maintenance retainer per month (₹)", S.RETAINER_M),
        ("RET_N", "Retainer months included", 12),
        ("PEN", "Penetration tests estimate (₹)", 650_000),
        ("STG_USD", "Client staging hosting per month (USD)", sum(v for _, v in S.STAGING)),
        ("STG_N", "Staging months (to Release 1)", 15),
        ("PIL", "Pilot running per month, central (₹)", round(S.PIL)),
        ("A1ADD", "A1 feature running additions per month, central (₹)", round(sum(S.A1ADD) / 2)),
        ("Y1_N", "Months of operation included after full go-live", 12),
        ("GST", "GST rate", 0.18),
    ]
    for i, (nm, lab, v) in enumerate(inputs, 4):
        wi.cell(row=i, column=1, value=nm)
        wi.cell(row=i, column=2, value=lab)
        c = wi.cell(row=i, column=3, value=v)
        c.fill = INP
        if nm in ("TOK_RED", "CONT", "GST"):
            c.number_format = "0%"
        name(wb, nm, f"Inputs!$C${i}")
    r = 4 + len(inputs)
    derived = [("DAY_RATE", "Builder's rate per day (₹)", "=PM_RATE/DAYS"), ("HOUR_RATE", "Builder's rate per hour (₹)", "=DAY_RATE/8"),
               ("M_CORE", "Duration, Core (months)", "=PD_CORE/PROD_DAYS"), ("M_A1", "Duration, A1 (months)", "=PD_A1/PROD_DAYS"),
               ("M_ALL", "Total build duration (months)", "=M_CORE+M_A1")]
    for i, (nm, lab, f) in enumerate(derived, r):
        wi.cell(row=i, column=1, value=nm)
        wi.cell(row=i, column=2, value=lab)
        wi.cell(row=i, column=3, value=f)
        name(wb, nm, f"Inputs!$C${i}")
    style_rows(wi, 4, r + len(derived) - 1, 3)

    # ---------------------------------------------------------------- Fee build-up
    wf = wb.create_sheet("Fee Build-up")
    title(wf, "How the development fee (A) is arrived at")
    header(wf, 3, ["Component", "Core platform", "Advanced A1", "Total", "Formula"], [52, 16, 16, 16, 60])
    tool_core = "+".join(f"{t[1]}*{t[2] if isinstance(t[2], (int, float)) and t[0] not in ('Claude Max 20x (Claude Code)', 'GitHub Pro', 'Google Workspace') else 'M_CORE'}" for t in S.OPT_TOOLS)
    tool_a1 = "+".join(f"{t[1]}*{t[3] if t[0] not in ('Claude Max 20x (Claude Code)', 'GitHub Pro', 'Google Workspace') else 'M_A1'}" for t in S.OPT_TOOLS)
    rows = [
        ("Builder's effort with AI (days)", "=PD_CORE", "=PD_A1", "=B4+C4", "Traditional effort × (1 − 32.8% net AI-built saving)"),
        ("Builder's hours", "=B4*8", "=C4*8", "=B5+C5", "Days × 8"),
        ("Duration (months)", "=M_CORE", "=M_A1", "=B6+C6", "Days ÷ productive days per month"),
        ("Builder's time (₹)", "=B4*DAY_RATE", "=C4*DAY_RATE", "=B7+C7", "Days × rate per day"),
        ("Builder's tools (₹)", f"=({tool_core})*FX", f"=({tool_a1})*FX", "=B8+C8", "Claude Max 20x + GitHub for the whole build; Figma 12 months; BrowserStack 6 months"),
        ("Claude API tokens for coding agents (₹)", "=TOK_CORE*(1-TOK_RED)", "=TOK_A1*(1-TOK_RED)", "=B9+C9", "Agent-executed days × $6.78 × ₹90, less caching/Haiku reduction"),
        ("Contingency (₹)", "=CONT*(B7+B9)", "=CONT*(C7+C9)", "=B10+C10", "Contingency × (time + tokens)"),
        ("Cost basis (₹)", "=B7+B8+B9+B10", "=C7+C8+C9+C10", "=B11+C11", ""),
        ("Optimized fee (₹)", "", "", "=FEE_OPT", "Cost basis rounded up"),
        ("Fixed development fee A (₹)", "=D13*B11/D11", "=D13*C11/D11", "='Cost Sheet'!F4", "Package target − retainer − at-cost estimates; split pro rata to cost basis"),
        ("Package discount (₹)", "", "", "=D12-D13", "Optimized fee − fee A"),
        ("Contingency remaining after discount (₹)", "", "", "=D10-D14", "If negative, the discount exceeds the contingency"),
    ]
    for i, (lab, b, c, d, f) in enumerate(rows, 4):
        for j, v in enumerate([lab, b, c, d, f], 1):
            wf.cell(row=i, column=j, value=v)
    wf["A11"].font = wf["A13"].font = Font(bold=True)
    for rr in (11, 13):
        for col in "BCD":
            wf[f"{col}{rr}"].fill = TOT
    style_rows(wf, 4, 3 + len(rows), 5, money_cols=(2, 3, 4))
    for rr in (4, 5, 6):
        for col in "BCD":
            wf[f"{col}{rr}"].number_format = "#,##0.0"

    # ---------------------------------------------------------------- Cost sheet
    wc = wb.create_sheet("Cost Sheet", 1)
    title(wc, "Final cost sheet: all-inclusive package (Core + Advanced A1, solo builder with AI)")
    header(wc, 3, ["#", "Item", "Basis", "Rate per month (₹)", "Months", "Amount excl. GST (₹)", "GST (₹)", "Amount incl. GST (₹)", "Amount excl. GST ($)"], [5, 70, 14, 15, 9, 18, 14, 18, 16])
    lines = [
        ("A", "Fixed development fee: Core platform (Releases 1 and 2) + Advanced release A1", "Fixed", "", "", "=PACKAGE-SUM(F5:F9)"),
        ("B", "Maintenance and support retainer (includes maintainer's Claude seat and GitHub)", "Fixed monthly", "=RET_M", "=RET_N", "=D5*E5"),
        ("C1", "Independent penetration tests: 2 engagements, CERT-In-empanelled vendor (range ₹4–9 lakh)", "At actuals", "", "", "=PEN"),
        ("C2", "Client hosting while building, staging only (Vercel, Supabase, AWS, domains)", "At actuals", "=STG_USD*FX", "=STG_N", "=D7*E7"),
        ("C3", "Pilot running from Release 1 go-live to A1 go-live", "At actuals", "=PIL", "=M_ALL-STG_N", "=D8*E8"),
        ("C4", "Running cost, first 12 months after full go-live (C3 + A1 additions)", "At actuals", "=PIL+A1ADD", "=Y1_N", "=D9*E9"),
    ]
    for i, (k, it, b, rt, m, amt) in enumerate(lines, 4):
        for j, v in enumerate([k, it, b, rt, m, amt, f"=F{i}*GST", f"=F{i}+G{i}", f"=F{i}/FX"], 1):
            wc.cell(row=i, column=j, value=v)
    wc.cell(row=10, column=2, value="Total package").font = Font(bold=True)
    for col in "FGHI":
        wc[f"{col}10"] = f"=SUM({col}4:{col}9)"
        wc[f"{col}10"].fill = TOT
        wc[f"{col}10"].font = Font(bold=True)
    wc.cell(row=12, column=2, value="Of which fixed (A + B)")
    wc["F12"] = "=F4+F5"
    wc.cell(row=13, column=2, value="Of which at actuals (C1–C4)")
    wc["F13"] = "=SUM(F6:F9)"
    wc.cell(row=14, column=2, value="Reduction against the unoptimized package (≈ ₹1,12,98,000)")
    wc["F14"] = f"={S.BEFORE_OPT}-F10"
    wc.cell(row=15, column=2, value="After year 1: running per month + retainer per month")
    wc["F15"] = "=PIL+A1ADD+RET_M"
    style_rows(wc, 4, 15, 9, money_cols=(4, 6, 7, 8), usd_cols=(9,))
    for rr in (4, 5, 6, 7, 8, 9):
        wc[f"E{rr}"].number_format = "0.0"

    # ---------------------------------------------------------------- Effort by activity
    we = wb.create_sheet("Effort by Activity")
    title(we, "Effort by activity: traditional vs solo builder with AI (days)")
    header(we, 3, ["Activity", "Core traditional", "Core solo with AI", "A1 traditional", "A1 solo with AI", "Total solo", "Value (₹)"], [62, 13, 13, 13, 13, 12, 15])
    for i, ((n, t, s), (_, t2, s2)) in enumerate(zip(S.C["rows"], S.A1["rows"]), 4):
        for j, v in enumerate([n, round(t, 1), round(s, 1), round(t2, 1), round(s2, 1), f"=C{i}+E{i}", f"=F{i}*DAY_RATE"], 1):
            we.cell(row=i, column=j, value=v)
    n = 3 + len(S.C["rows"])
    we.cell(row=n + 1, column=1, value="Total").font = Font(bold=True)
    for col in "BCDEFG":
        we[f"{col}{n + 1}"] = f"=SUM({col}4:{col}{n})"
        we[f"{col}{n + 1}"].fill = TOT
    style_rows(we, 4, n + 1, 7, money_cols=(7,))
    r0 = n + 3
    header(we, r0, ["Activity", "AI reduction", "What the AI agents do", "What the builder does", "", "", ""])
    for i, a in enumerate(X.ACCEL, r0 + 1):
        for j, v in enumerate([a[0], a[2], a[5], a[6].replace("PO", "client").replace("Engineers", "Builder")], 1):
            c = we.cell(row=i, column=j, value=v)
            if j == 2:
                c.number_format = "0%"
    style_rows(we, r0 + 1, r0 + len(X.ACCEL), 4)

    # ---------------------------------------------------------------- Optimization
    wo = wb.create_sheet("Optimization")
    title(wo, "How the package was optimized and discounted")
    header(wo, 3, ["Lever", "Saving (₹)"], [90, 16])
    levers = [("Builder tools trimmed (BrowserStack 6 months, Figma 12 months, client's own Workspace)", 206_000), ("Claude tokens cut ≈ 20% (prompt caching, Haiku)", 81_000),
              ("Contingency 15% → 10%", 284_000), ("Penetration tests 3 → 2 (combined Release 2 + A1 test)", 325_000), ("Staging-only hosting until Release 1", 306_000),
              ("Pilot running without team seats, delivery AI line and integration reserve; free monitoring tiers", 210_000),
              ("Year 1: point-in-time recovery deferred; maintainer seat in the retainer", 270_000), ("Retainer ₹65,000 → ₹55,000 per month", 120_000)]
    for i, (l_, v) in enumerate(levers, 4):
        wo.cell(row=i, column=1, value=l_)
        wo.cell(row=i, column=2, value=v)
    k = 4 + len(levers)
    wo.cell(row=k, column=1, value="Package discount on the development fee")
    wo.cell(row=k, column=2, value="='Fee Build-up'!D14")
    wo.cell(row=k + 1, column=1, value="Rounding of lever estimates and duration refinement")
    wo[f"B{k + 1}"] = f"={S.BEFORE_OPT}-'Cost Sheet'!F10-SUM(B4:B{k})"
    wo.cell(row=k + 2, column=1, value="Total reduction from ≈ ₹1,12,98,000 to the package").font = Font(bold=True)
    wo[f"B{k + 2}"] = f"=SUM(B4:B{k + 1})"
    wo[f"B{k + 2}"].fill = TOT
    style_rows(wo, 4, k + 2, 2, money_cols=(2,))

    # ---------------------------------------------------------------- Build subscriptions
    wb_ = wb.create_sheet("Build Subscriptions")
    title(wb_, "Subscriptions while building (USD list prices; verify)")
    header(wb_, 3, ["Subscription", "$ per month", "Months (Core)", "Months (A1)", "Total over build ($)", "Total over build (₹)", "Note", "Paid by"], [44, 12, 12, 12, 16, 16, 42, 18])
    rr = 4
    for nm_, m, mc, ma, note in S.OPT_TOOLS:
        full = nm_ in ("Claude Max 20x (Claude Code)", "GitHub Pro", "Google Workspace")
        vals = [nm_, m, "=M_CORE" if full else mc, "=M_A1" if full else ma, f"=B{rr}*(C{rr}+D{rr})", f"=E{rr}*FX", note, "Builder (in fee A)"]
        for j, v in enumerate(vals, 1):
            c = wb_.cell(row=rr, column=j, value=v)
            if j == 2:
                c.fill = INP
        rr += 1
    for j, v in enumerate(["Claude API tokens for coding agents", "", "=M_CORE", "=M_A1", f"=F{rr}/FX", "='Fee Build-up'!D9", "Capped at $300 per month", "Builder (in fee A)"], 1):
        wb_.cell(row=rr, column=j, value=v)
    rr += 1
    for nm_, v in S.STAGING:
        for j, x in enumerate([nm_, v, "=STG_N", 0, f"=B{rr}*C{rr}", f"=E{rr}*FX", "Staging until Release 1, then production (C3)", "Client (C2)"], 1):
            c = wb_.cell(row=rr, column=j, value=x)
            if j == 2:
                c.fill = INP
        rr += 1
    for j, v in enumerate(["Sentry, Langfuse, open-source toolchain, Bitwarden", 0, "", "", 0, 0, "Free tiers / self-hosted", "—"], 1):
        wb_.cell(row=rr, column=j, value=v)
    wb_.cell(row=rr + 1, column=1, value="Total").font = Font(bold=True)
    wb_[f"E{rr + 1}"] = f"=SUM(E4:E{rr})"
    wb_[f"F{rr + 1}"] = f"=SUM(F4:F{rr})"
    wb_[f"E{rr + 1}"].fill = wb_[f"F{rr + 1}"].fill = TOT
    style_rows(wb_, 4, rr + 1, 8, money_cols=(6,), usd_cols=(2, 5))
    for i in range(4, rr + 1):
        for col in "CD":
            wb_[f"{col}{i}"].number_format = "0.0"

    # ---------------------------------------------------------------- Running subscriptions
    wr = wb.create_sheet("Running Subscriptions")
    title(wr, "Subscriptions while using the application (pilot; per month; client-owned)")
    header(wr, 3, ["Line", "Subscription / service", "Billing", "₹ per month low", "₹ per month high", "$ per month low", "$ per month high", "Active from"], [8, 70, 22, 14, 14, 13, 13, 22])
    for i, r_ in enumerate(S.RUN_LINES, 4):
        for j, v in enumerate([r_[0], r_[2], r_[3], r_[4], r_[5], f"=D{i}/FX", f"=E{i}/FX", r_[6]], 1):
            c = wr.cell(row=i, column=j, value=v)
            if j in (4, 5):
                c.fill = INP
    n = 3 + len(S.RUN_LINES)
    extra = [("", "Subtotal", f"=SUM(D4:D{n})", f"=SUM(E4:E{n})"), ("B11", "Contingency 15%", f"=D{n + 1}*0.15", f"=E{n + 1}*0.15"),
             ("", "Pilot running (C3) per month", f"=D{n + 1}+D{n + 2}", f"=E{n + 1}+E{n + 2}"),
             ("A1", "Advanced A1 feature running additions", round(S.A1ADD[0]), round(S.A1ADD[1])),
             ("", "Running after full go-live (C4) per month", f"=D{n + 3}+D{n + 4}", f"=E{n + 3}+E{n + 4}")]
    for k, (ln, lab, lo, hi) in enumerate(extra, n + 1):
        wr.cell(row=k, column=1, value=ln)
        wr.cell(row=k, column=2, value=lab).font = Font(bold=lab.startswith(("Pilot", "Running", "Subtotal")))
        wr.cell(row=k, column=4, value=lo)
        wr.cell(row=k, column=5, value=hi)
        wr.cell(row=k, column=6, value=f"=D{k}/FX")
        wr.cell(row=k, column=7, value=f"=E{k}/FX")
        if lab.startswith(("Pilot", "Running")):
            for col in "DEFG":
                wr[f"{col}{k}"].fill = TOT
    ag = [i for i in Q.IN if i["kind"] == "AG"]
    notes = [
        f"Production AI usage: the {len(ag)} AI agents in scope cost ≈ ₹{sum(i['run_base'] for i in ag):,.0f} per month at pilot volume (Claude, Sonnet primary); hard caps ₹3,000 core + ₹2,000 advanced.",
        "Removed by optimization: team Claude seats (B09), delivery-team AI (B23), integration reserve (B10), paid synthetic probes (B07+).",
        "Growth gate ≈ ₹59,000–79,000 per month (incl. Supabase point-in-time recovery); scale ≈ ₹1.39–1.79 lakh per month (DEC-422).",
        "Optional/conditional: Apollo enrichment ≈ ₹10,350/month after the scale gate; e-signature per envelope; payment-gateway fees ≈ 2%; advertising budgets.",
    ]
    for i, t in enumerate(notes, n + 7):
        wr.cell(row=i, column=2, value=t)
    style_rows(wr, 4, n + 5, 8, money_cols=(4, 5), usd_cols=(6, 7))

    # ---------------------------------------------------------------- AI catalogue
    wa = wb.create_sheet("AI Catalogue")
    title(wa, f"AI agents, automations and workflows in scope ({len(Q.IN)})")
    header(wa, 3, ["ID", "Type", "Name", "What it does", "Automation level", "Autonomy", "Model", "AI cost ₹/month (base)", "Release"], [9, 12, 34, 90, 36, 22, 26, 14, 16])
    tmap = {"AG": "AI agent", "AU": "Automation", "WF": "Workflow"}
    for i, it in enumerate(Q.IN, 4):
        for j, v in enumerate([it["id"], tmap[it["kind"]], it["name"], it["what"], it["level"], it["autonomy"] if it["kind"] != "WF" else "Human approval gates",
                               it["tier"] if it["kind"] == "AG" else "—", it["run_base"] if it["kind"] == "AG" else 0, it["release"]], 1):
            wa.cell(row=i, column=j, value=v)
    n = 3 + len(Q.IN)
    wa.cell(row=n + 1, column=3, value="Total AI cost per month (base)").font = Font(bold=True)
    wa[f"H{n + 1}"] = f"=SUM(H4:H{n})"
    wa[f"H{n + 1}"].fill = TOT
    r0 = n + 3
    header(wa, r0, ["Summary", "Count", "", "", "", "", "", "", ""])
    summ = [("AI agents", "AG"), ("Automations", "AU"), ("Workflows", "WF")]
    for k, (lab, kind) in enumerate(summ, r0 + 1):
        wa.cell(row=k, column=1, value=lab)
        wa.cell(row=k, column=2, value=f'=COUNTIF(B4:B{n},"{tmap[kind]}")')
    for k, lvl in enumerate(["Fully automated*", "Mostly automated*", "Partially automated*", "Assistive only*"], r0 + 4):
        wa.cell(row=k, column=1, value=lvl.rstrip("*"))
        wa.cell(row=k, column=2, value=f'=COUNTIF(E4:E{n},"{lvl}")')
    style_rows(wa, 4, n + 1, 9, money_cols=(8,))
    wa.auto_filter.ref = f"A3:I{n}"

    # ---------------------------------------------------------------- Payment schedule
    wpy = wb.create_sheet("Payment Schedule")
    title(wpy, "Payment milestones on the development fee (A)")
    header(wpy, 3, ["Milestone", "Indicative month", "Share", "Amount excl. GST (₹)", "GST (₹)", "Amount incl. GST (₹)"], [60, 18, 9, 18, 14, 18])
    ms = [("Contract signing (mobilisation)", 0.10, 0), ("Foundation gate", 0.10, 3), ("Release 1 functional complete (UAT start)", 0.15, 12),
          ("Release 1 go/no-go passed", 0.15, 15), ("Release 2 build gate passed", 0.15, round(S.C["months"]) - 1), ("30-day monitored pilot completed", 0.10, round(S.C["months"]) + 1),
          ("Advanced A1 mid-point demo", 0.10, round(S.C["months"] + S.A1["months"] / 2)), ("Advanced A1 go-live and acceptance", 0.15, round(S.MONTHS))]
    for i, (m, sh, mo) in enumerate(ms, 4):
        for j, v in enumerate([m, f"Month {mo}", sh, f"=C{i}*'Cost Sheet'!$F$4", f"=D{i}*GST", f"=D{i}+E{i}"], 1):
            c = wpy.cell(row=i, column=j, value=v)
            if j == 3:
                c.number_format = "0%"
                c.fill = INP
    k = 4 + len(ms)
    wpy.cell(row=k, column=1, value="Total").font = Font(bold=True)
    for col in "CDEF":
        wpy[f"{col}{k}"] = f"=SUM({col}4:{col}{k - 1})"
        wpy[f"{col}{k}"].fill = TOT
    wpy[f"C{k}"].number_format = "0%"
    wpy.cell(row=k + 2, column=1, value="Retainer (B): billed monthly from go-live; C1–C4 paid by the client to providers as incurred.")
    style_rows(wpy, 4, k, 6, money_cols=(4, 5, 6))
    for i in range(4, k + 1):
        wpy[f"C{i}"].number_format = "0%"

    # ---------------------------------------------------------------- Future options
    wfo = wb.create_sheet("Future Options")
    title(wfo, "Future options (indicative, not part of this package)")
    header(wfo, 3, ["Option", "Builder's days", "Months", "Indicative fee excl. GST (₹)"], [90, 14, 10, 20])
    a2, a3 = 518 * (1 - Q.SAVE), 283 * (1 - Q.SAVE)
    for i, (lab, d) in enumerate([("Advanced A2: NBA, deal risk, ABM, intent hub, deal rooms, partners, QBR, semantic layer, NL analytics", a2),
                                   ("Advanced A3 (after the scale gate): conversation intelligence, marketing mix, no-code builder, developer platform", a3)], 4):
        for j, v in enumerate([lab, round(d, 1), f"=B{i}/PROD_DAYS", f"=B{i}*DAY_RATE*(1+CONT)+C{i}*204*FX"], 1):
            wfo.cell(row=i, column=j, value=v)
    style_rows(wfo, 4, 5, 4, money_cols=(4,))
    wfo["C4"].number_format = wfo["C5"].number_format = "0.0"

    # ---------------------------------------------------------------- Technology & skills
    wt = wb.create_sheet("Technology & Skills")
    title(wt, "Technology stack and the skill set the builder applies")
    header(wt, 3, ["Layer", "Technology", "Why"], [20, 90, 60])
    tech = [
        ("Frontends", "React + TypeScript (Vite), design system, WCAG 2.2 AA; hosted on Vercel (two projects, separate origins)", "Fast, accessible UIs; preview deployments"),
        ("Backend", "Python, Django REST Framework modular monolith; Celery + Celery Beat; Valkey", "Mature, secure, productive"),
        ("Database", "PostgreSQL on Supabase (Mumbai): row-level security, pgvector, storage", "Managed backups and scaling; India data residency"),
        ("Compute and files", "AWS ap-south-1: EC2/ECS for API and workers, S3, SES, DR copies", "Data stays in India; low cost at pilot scale"),
        ("AI", "Claude via the model gateway: Haiku-class and Sonnet-class (primary, DEC-418); Pydantic schemas; prompt registry; evaluation harness", "Quality with hard cost caps and human approval"),
        ("Messaging", "Meta WhatsApp Cloud API, Amazon SES, consent and quiet-hour rules", "Compliant outreach"),
        ("Security", "Policy Decision Point, RLS, passkeys, JIT admin, secrets rotation, Semgrep, Trivy, OWASP ZAP", "Fail-closed; independent pen tests"),
        ("Quality", "pytest, Playwright, k6, axe-core, AI evaluation sets", "Automated evidence per release"),
        ("DevOps", "GitHub + Actions CI/CD, infrastructure as code, Sentry, Langfuse, Prometheus/Grafana, status page", "Repeatable releases and observability"),
        ("Building with AI", "Claude Code (Claude Max 20x) and Claude API headless agents in sandboxed branches", "The reason the price is low"),
    ]
    for i, row in enumerate(tech, 4):
        for j, v in enumerate(row, 1):
            wt.cell(row=i, column=j, value=v)
    r0 = 4 + len(tech) + 1
    header(wt, r0, ["Role the builder plays", "Skills", "Share of time / how AI helps"])
    skills = [
        ("Solutions architect and security designer", "Multi-tenant SaaS, RLS, policy engines, threat modelling", "10% · AI drafts ADRs and threat checklists"),
        ("Business analyst / product owner proxy", "Requirements, user stories, Gherkin, UAT planning", "8% · AI refines the 461 drafted stories"),
        ("Full-stack engineer (Django, React)", "APIs, workflows, data models, React screens", "38% · coding agents implement; builder reviews every change"),
        ("AI/LLM engineer", "Prompt contracts, RAG, guardrails, evaluations, cost control", "12% · agents draft prompts and eval sets"),
        ("QA and test automation engineer", "Test strategy, automation, performance, accessibility", "14% · agents generate tests and data"),
        ("DevOps / SRE", "CI/CD, IaC, monitoring, backups, DR drills", "8% · agents write pipelines and runbooks"),
        ("UX designer", "Information architecture, accessible UI", "5% · agents generate variants from the design system"),
        ("Project manager and client liaison", "Planning, reporting, demos", "5% · AI drafts status reports and release notes"),
    ]
    for i, row in enumerate(skills, r0 + 1):
        for j, v in enumerate(row, 1):
            wt.cell(row=i, column=j, value=v)
    style_rows(wt, 4, r0 + len(skills), 3)

    # ---------------------------------------------------------------- Assumptions
    wz = wb.create_sheet("Assumptions")
    title(wz, "Assumptions and terms")
    for i, t in enumerate([
        "Scope: Application Blueprint v1.1 (Core + Advanced A1) as of 28 Nov 2026; changes by written change request at the day rate.",
        "Builder's time valued at ₹1.25 lakh per month (₹5,682 per day; ₹710 per hour); 21 productive days per month.",
        "AI productivity: central case of Cost Estimate v1.1 plus 4% for solo working (net 32.8%); planning assumptions, measured progress reported monthly.",
        "Claude Sonnet primary (DEC-418); hosting Vercel + Supabase + AWS Mumbai (DEC-421); running budget DEC-422.",
        "C1–C4 are estimates at list prices as of 28 Nov 2026, paid at actuals; provider price changes pass through.",
        "Client provides approvals, UAT users, provider accounts and legal confirmations; legal counsel, paid data and advertising not included.",
        "Build agents use synthetic data only.",
        "Fixed price for A and B; IP to the client on full payment; 60-day warranty after each go-live; invoices payable within 15 days; validity 30 days.",
        "The discount uses most of the contingency; scope is frozen at the blueprint.",
    ], 3):
        wz.cell(row=i, column=1, value=f"{i - 2}. {t}")
    wz.column_dimensions["A"].width = 150

    wb.save(OUT)
    print("XLSX", OUT)


if __name__ == "__main__":
    main()
