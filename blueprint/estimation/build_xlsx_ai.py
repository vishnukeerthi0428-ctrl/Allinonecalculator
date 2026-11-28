"""Excel workbook for the AI-built variant (v1.1), with live formulas: edit acceleration factors or token prices and totals update."""
from openpyxl import Workbook
from openpyxl.styles import Font
from openpyxl.workbook.defined_name import DefinedName

import ai_model as X
import model as M
from build_xlsx import INP, TOT, NAVY, header, style_rows, title

INR = '"₹"#,##,##0'
USD = '"$"#,##0'


def name(wb, nm, ref):
    wb.defined_names[nm] = DefinedName(nm, attr_text=ref)


def build(D, BE, path):
    wb = Workbook()
    ws = wb.active
    ws.title = "README"
    title(ws, "AI Growth Engine – Cost Estimate v1.1: building with AI models and AI agents (traditional vs AI-built)",
          "Edit yellow cells on 'Inputs' and 'Acceleration'; every AI-built figure recalculates. Running costs of the application are unchanged.")
    for i, t in enumerate([
        "Bifurcation: (1) one-time development, (2) build-time subscriptions and AI usage, (3) recurring running cost of the application, (4) lifecycle (maintenance, future-proofing).",
        "Traditional figures come from Cost Estimate v1.0 (approved budgets DEC-230/231, DEC-416/417, tooling DEC-419).",
        "AI acceleration factors are planning assumptions; calibrate at the Sprint 2 gate before changing the team or dates.",
        "Sheets: Inputs · Acceleration · Comparison · Effort by Activity · Team · Build Tooling · Agent Tokens · AI Catalogue · Timeline · Running Costs · TCO · Risks",
    ], 4):
        ws.cell(row=i, column=1, value=t)
    ws.column_dimensions["A"].width = 160

    # Inputs
    wi = wb.create_sheet("Inputs")
    title(wi, "Inputs (edit the yellow cells)")
    header(wi, 3, ["Name", "Parameter", "Value"], [14, 60, 14])
    t = X.TOKENS_PER_AGENT_PD
    inputs = [("FX", "₹ per USD", M.FX), ("PM_LO", "Loaded cost per person-month low (₹)", M.PM_RATE[0]), ("PM_HI", "Loaded cost per person-month high (₹)", M.PM_RATE[1]),
              ("DAYS", "Working days per month", M.DAYS_PER_MONTH), ("HRS", "Hours per day", M.HOURS_PER_DAY),
              ("TOK_IN", "Input tokens per agent-executed person-day (millions)", t["input_m"]), ("TOK_CACHE", "Share of input served from cache", t["cached_share"]),
              ("TOK_OUT", "Output tokens per agent-executed person-day (millions)", t["output_m"])]
    for m, (pin, pc, pout) in X.MODEL_PRICES.items():
        k = m.split("-")[0].upper()
        inputs += [(f"{k}_IN", f"{m} input $/M tokens", pin), (f"{k}_CACHE", f"{m} cached input $/M tokens", pc), (f"{k}_OUT", f"{m} output $/M tokens", pout),
                   (f"{k}_MIX", f"{m} share of agent work", X.MODEL_MIX[m])]
    inputs += [("MULT_OPT", "Token multiplier, optimistic", X.TOKEN_MULT["optimistic"]), ("MULT_C", "Token multiplier, central", X.TOKEN_MULT["central"]),
               ("MULT_CONS", "Token multiplier, conservative", X.TOKEN_MULT["conservative"]),
               ("MNT_AI_LO", "Maintenance % with AI agents (low)", X.MAINT_PCT_AI[0]), ("MNT_AI_HI", "Maintenance % with AI agents (high)", X.MAINT_PCT_AI[1])]
    for i, (nm, lab, v) in enumerate(inputs, 4):
        wi.cell(row=i, column=1, value=nm)
        wi.cell(row=i, column=2, value=lab)
        wi.cell(row=i, column=3, value=v).fill = INP
        name(wb, nm, f"Inputs!$C${i}")
    r = 4 + len(inputs)
    f = "+".join(f"{k}_MIX*(TOK_IN*(1-TOK_CACHE)*{k}_IN+TOK_IN*TOK_CACHE*{k}_CACHE+TOK_OUT*{k}_OUT)" for k in ("OPUS", "SONNET", "HAIKU"))
    for i, (nm, lab, fx) in enumerate([("USD_PD", "Token cost per agent-executed person-day (USD, central)", "=" + f),
                                       ("PD_LO", "Cost per person-day low (₹)", "=PM_LO/DAYS"), ("PD_HI", "Cost per person-day high (₹)", "=PM_HI/DAYS")], r):
        wi.cell(row=i, column=1, value=nm)
        wi.cell(row=i, column=2, value=lab)
        wi.cell(row=i, column=3, value=fx)
        name(wb, nm, f"Inputs!$C${i}")
    style_rows(wi, 4, r + 2, 3)

    # Acceleration
    wa = wb.create_sheet("Acceleration")
    title(wa, "Where AI agents save effort, and the new work they create (edit the yellow cells)")
    header(wa, 3, ["Activity", "Share of effort", "Reduction optimistic", "Reduction central", "Reduction conservative", "Executed by agents", "What the AI does", "What humans still do"],
           [52, 10, 11, 11, 11, 11, 55, 50])
    shares = {n: s for n, s, _ in M.ACTIVITY_SPLIT}
    for i, a in enumerate(X.ACCEL, 4):
        for j, v in enumerate([a[0], shares[a[0]], a[1], a[2], a[3], a[4], a[5], a[6]], 1):
            c = wa.cell(row=i, column=j, value=v)
            if 2 <= j <= 6:
                c.number_format = "0%"
                if j >= 3:
                    c.fill = INP
    n = 3 + len(X.ACCEL)
    wa.cell(row=n + 1, column=1, value="Weighted reduction").font = Font(bold=True)
    for col in "CDEF":
        wa[f"{col}{n + 1}"] = f"=SUMPRODUCT($B$4:$B${n},{col}4:{col}{n})"
        wa[f"{col}{n + 1}"].number_format = "0.0%"
        wa[f"{col}{n + 1}"].fill = TOT
    name(wb, "AGENT_SHARE", f"Acceleration!$F${n + 1}")
    o0 = n + 3
    header(wa, o0, ["New work created by AI-built delivery (% of traditional effort)", "", "Optimistic", "Central", "Conservative", "", "What it is", ""])
    for i, o in enumerate(X.OVERHEAD, o0 + 1):
        for j, v in ((1, o[0]), (3, o[1]), (4, o[2]), (5, o[3]), (7, o[4])):
            c = wa.cell(row=i, column=j, value=v)
            if j in (3, 4, 5):
                c.number_format = "0.0%"
                c.fill = INP
    on = o0 + len(X.OVERHEAD)
    wa.cell(row=on + 1, column=1, value="Total added work").font = Font(bold=True)
    wa.cell(row=on + 2, column=1, value="NET SAVING ON PEOPLE EFFORT").font = Font(bold=True, color=NAVY)
    for col, nm in (("C", "SAVE_OPT"), ("D", "SAVE_C"), ("E", "SAVE_CONS")):
        wa[f"{col}{on + 1}"] = f"=SUM({col}{o0 + 1}:{col}{on})"
        wa[f"{col}{on + 2}"] = f"={col}{n + 1}-{col}{on + 1}"
        for rr in (on + 1, on + 2):
            wa[f"{col}{rr}"].number_format = "0.0%"
            wa[f"{col}{rr}"].fill = TOT
        name(wb, nm, f"Acceleration!${col}${on + 2}")
    style_rows(wa, 4, on + 2, 8)

    # Comparison
    wc = wb.create_sheet("Comparison")
    title(wc, "(1) One-time development: traditional vs AI-built")
    cols = ["Key", "Package", "Status", "Traditional low ₹", "Traditional central ₹", "Traditional high ₹", "People low ₹", "People central ₹", "People high ₹", "Vendor low ₹", "Vendor central ₹", "Vendor high ₹",
            "AI-built low ₹", "AI-built central ₹", "AI-built high ₹", "Saving central ₹", "Saving %", "AI-built low $", "AI-built central $", "AI-built high $", "Approved (1/0)"]
    header(wc, 3, cols, [6, 46, 26] + [13] * 18)
    for i, k in enumerate(D["allk"], 4):
        a = D["AI"][k]
        p = next(x for x in M.PACKAGES if x[0] == k)
        vals = [k, p[1], p[2], *a["trad"], *a["people"], *a["vendor"],
                f"=G{i}*(1-SAVE_OPT)+J{i}", f"=H{i}*(1-SAVE_C)+K{i}", f"=I{i}*(1-SAVE_CONS)+L{i}", f"=E{i}-N{i}", f"=P{i}/E{i}",
                f"=M{i}/FX", f"=N{i}/FX", f"=O{i}/FX", 1 if p[2].startswith("Approved") else 0]
        for j, v in enumerate(vals, 1):
            c = wc.cell(row=i, column=j, value=v)
            if j == 17:
                c.number_format = "0%"
    n = 3 + len(D["allk"])
    for rr, lab, fx in ((n + 1, "Approved scope", "SUMPRODUCT({c}4:{c}%d,$U$4:$U$%d)" % (n, n)), (n + 2, "Full programme", "SUM({c}4:{c}%d)" % n)):
        wc.cell(row=rr, column=2, value=lab).font = Font(bold=True)
        for col in "DEFGHIJKLMNOPRST":
            wc[f"{col}{rr}"] = "=" + fx.format(c=col)
            wc[f"{col}{rr}"].fill = TOT
        wc[f"Q{rr}"] = f"=P{rr}/E{rr}"
        wc[f"Q{rr}"].number_format = "0%"
    style_rows(wc, 4, n + 2, 21, money_cols=range(4, 17), usd_cols=(18, 19, 20))
    for rr in range(4, n + 3):
        wc[f"Q{rr}"].number_format = "0%"

    # Effort by activity (core, central)
    we = wb.create_sheet("Effort by Activity")
    title(we, "Core build effort by activity, central case: traditional vs AI-built")
    header(we, 3, ["Activity", "Traditional pd", "Reduction (central)", "AI-built pd", "Agent-executed pd", "Saved pd"], [55, 13, 12, 13, 14, 12])
    ce = D["AI"]["CORE"]["trad_eff"][1]
    for i, a in enumerate(X.ACCEL, 4):
        for j, v in enumerate([a[0], f"={ce}*{shares[a[0]]}", f"=Acceleration!D{i}", f"=B{i}*(1-C{i})", f"=B{i}*Acceleration!F{i}", f"=B{i}-D{i}"], 1):
            c = we.cell(row=i, column=j, value=v)
            if j == 3:
                c.number_format = "0%"
    n = 3 + len(X.ACCEL)
    for i, o in enumerate(X.OVERHEAD, n + 1):
        for j, v in enumerate([f"Added: {o[0]}", 0, "", f"={ce}*Acceleration!D{4 + len(X.ACCEL) + 2 + (i - n)}", 0, f"=-D{i}"], 1):
            we.cell(row=i, column=j, value=v)
    t_ = n + len(X.OVERHEAD) + 1
    we.cell(row=t_, column=1, value="Total").font = Font(bold=True)
    for col in "BDEF":
        we[f"{col}{t_}"] = f"=SUM({col}4:{col}{t_ - 1})"
        we[f"{col}{t_}"].fill = TOT
    style_rows(we, 4, t_, 6)

    # Team
    wt = wb.create_sheet("Team")
    title(wt, "Team for the AI-built option A (same dates)")
    header(wt, 3, ["Role", "FTE at peak", "Responsibility"], [52, 12, 70])
    for i, (r_, f_, d_) in enumerate(X.AI_TEAM, 4):
        for j, v in enumerate([r_, f_, d_], 1):
            wt.cell(row=i, column=j, value=v)
    n = 3 + len(X.AI_TEAM)
    wt.cell(row=n + 1, column=1, value="Total (traditional peak ≈ 8.5 FTE)").font = Font(bold=True)
    wt[f"B{n + 1}"] = f"=SUM(B4:B{n})"
    style_rows(wt, 4, n + 1, 3)

    # Build tooling
    wb_ = wb.create_sheet("Build Tooling")
    title(wb_, "(2) Build-time subscriptions per month: AI-built vs traditional (USD list prices; verify)")
    header(wb_, 3, ["Item", "Purpose", "Unit $ low", "Unit $ high", "Seats (build)", "Seats (after build)", "Month $ low", "Month $ high", "Month ₹ low", "Month ₹ high", "After-build $ low", "After-build $ high", "Notes"],
           [52, 50, 10, 10, 9, 9, 11, 11, 12, 12, 11, 11, 40])
    rows = D["ai_tools_rows"]
    for i, r_ in enumerate(rows, 4):
        for j, v in enumerate([r_["name"], r_["purpose"], r_["ulo"], r_["uhi"], r_["seats"], r_["after"], f"=C{i}*E{i}", f"=D{i}*E{i}", f"=G{i}*FX", f"=H{i}*FX", f"=C{i}*F{i}", f"=D{i}*F{i}", r_["note"]], 1):
            c = wb_.cell(row=i, column=j, value=v)
            if 3 <= j <= 6:
                c.fill = INP
    i = 4 + len(rows)
    nc = D["nonclaude"]
    for j, v in enumerate(["Other DEC-419 tools (GitHub, Figma, Workspace, Bitwarden, BrowserStack, domains)", "Same as traditional", "", "", "", "", nc[0], nc[1], f"=G{i}*FX", f"=H{i}*FX", "", "", "Approved (DEC-419)"], 1):
        wb_.cell(row=i, column=j, value=v)
    wb_.cell(row=i + 1, column=1, value="Total AI-built tooling").font = Font(bold=True)
    for col in "GHIJKL":
        wb_[f"{col}{i + 1}"] = f"=SUM({col}4:{col}{i})"
        wb_[f"{col}{i + 1}"].fill = TOT
    wb_.cell(row=i + 2, column=1, value="Traditional tooling (DEC-419), for comparison").font = Font(bold=True)
    wb_[f"G{i + 2}"], wb_[f"H{i + 2}"] = D["trad_tools"]
    wb_[f"I{i + 2}"], wb_[f"J{i + 2}"] = f"=G{i + 2}*FX", f"=H{i + 2}*FX"
    wb_.cell(row=i + 3, column=1, value="Difference per month").font = Font(bold=True)
    for col in "GHIJ":
        wb_[f"{col}{i + 3}"] = f"={col}{i + 1}-{col}{i + 2}"
        wb_[f"{col}{i + 3}"].fill = TOT
    style_rows(wb_, 4, i + 3, 13, money_cols=(9, 10), usd_cols=(3, 4, 7, 8, 11, 12))

    # Agent tokens
    wk = wb.create_sheet("Agent Tokens")
    title(wk, "AI-agent token usage to build (Claude API for headless and parallel agents)")
    header(wk, 3, ["Package", "Effort pd low", "Effort pd central", "Effort pd high", "Agent pd optimistic", "Agent pd central", "Agent pd conservative",
                   "Tokens $ optimistic", "Tokens $ central", "Tokens $ conservative", "Tokens ₹ central", "Approved (1/0)"], [46, 11, 11, 11, 12, 12, 12, 13, 13, 13, 13, 10])
    for i, k in enumerate(D["allk"], 4):
        a = D["AI"][k]
        p = next(x for x in M.PACKAGES if x[0] == k)
        vals = [p[1], *a["trad_eff"], f"=B{i}*AGENT_SHARE", f"=C{i}*AGENT_SHARE", f"=D{i}*AGENT_SHARE", f"=E{i}*USD_PD*MULT_OPT", f"=F{i}*USD_PD*MULT_C", f"=G{i}*USD_PD*MULT_CONS",
                f"=I{i}*FX", 1 if p[2].startswith("Approved") else 0]
        for j, v in enumerate(vals, 1):
            wk.cell(row=i, column=j, value=v)
    n = 3 + len(D["allk"])
    for rr, lab, fx in ((n + 1, "Approved scope", "SUMPRODUCT({c}4:{c}%d,$L$4:$L$%d)" % (n, n)), (n + 2, "Full programme", "SUM({c}4:{c}%d)" % n)):
        wk.cell(row=rr, column=1, value=lab).font = Font(bold=True)
        for col in "HIJK":
            wk[f"{col}{rr}"] = "=" + fx.format(c=col)
            wk[f"{col}{rr}"].fill = TOT
    style_rows(wk, 4, n + 2, 12, money_cols=(11,), usd_cols=(8, 9, 10))

    # AI catalogue
    wcat = wb.create_sheet("AI Catalogue")
    title(wcat, f"AI agents, automations and workflows ({len(D['CAT'])}): traditional vs AI-built build effort; run cost unchanged")
    cols = ["ID", "Type", "Name", "What it does", "Automation level", "Complexity", "Trad. pd low", "Trad. pd high", "AI-built pd low", "AI-built pd high", "Trad. cost low ₹", "Trad. cost high ₹",
            "AI-built cost low ₹", "AI-built cost high ₹", "AI-built cost low $", "AI-built cost high $", "Run ₹/month base", "How it is built with AI", "Release", "Dates"]
    header(wcat, 3, cols, [9, 11, 32, 70, 30, 10, 9, 9, 10, 10, 13, 13, 13, 13, 12, 12, 12, 50, 18, 20])
    tmap = {"AG": "AI agent", "AU": "Automation", "WF": "Workflow"}
    for i, it in enumerate(D["CAT"], 4):
        vals = [it["id"], tmap[it["kind"]], it["name"], it["what"], it["level"], it["complexity"], it["pd_lo"], it["pd_hi"], f"=G{i}*(1-SAVE_OPT)", f"=H{i}*(1-SAVE_CONS)",
                f"=G{i}*PD_LO", f"=H{i}*PD_HI", f"=I{i}*PD_LO", f"=J{i}*PD_HI", f"=M{i}/FX", f"=N{i}/FX", it["run_base"], it["build_mode"], it["release"], it["dates"]]
        for j, v in enumerate(vals, 1):
            wcat.cell(row=i, column=j, value=v)
    n = 3 + len(D["CAT"])
    wcat.cell(row=n + 1, column=3, value="Total").font = Font(bold=True)
    for col in "GHIJKLMNOPQ":
        wcat[f"{col}{n + 1}"] = f"=SUM({col}4:{col}{n})"
        wcat[f"{col}{n + 1}"].fill = TOT
    style_rows(wcat, 4, n + 1, len(cols), money_cols=(11, 12, 13, 14, 17), usd_cols=(15, 16))
    wcat.auto_filter.ref = f"A3:T{n}"

    # Timeline
    wtl = wb.create_sheet("Timeline")
    title(wtl, "Timeline options: A = same dates with a smaller team (cost view); B = same team, earlier delivery (time view)")
    header(wtl, 3, ["Milestone", "Traditional (approved)", "AI-built optimistic (B)", "AI-built central (B)", "AI-built conservative (B)"], [34, 28, 28, 28, 28])
    TL, day = D["TL"], D["day"]
    rows = [("Release 1 go/no-go", "Fri 04 Jun 2027 (Day 180)", "r1"), ("Release 2 build gate", "Fri 02 Jul 2027 (Day 208)", "r2"), ("W5 exit", "Fri 23 Jul 2027 (Day 229)", "w5"),
            ("Advanced A1 complete", "Dec 2027", "a1e"), ("Advanced A2 complete", "Mar 2028", "a2e"), ("Advanced A3 complete", "Jul 2028", "a3e")]
    for i, (lab, trad, key) in enumerate(rows, 4):
        for j, v in enumerate([lab, trad] + [f"{day(TL[c][key])} (Day {TL[c][key]:.0f})" for c in X.CASES], 1):
            wtl.cell(row=i, column=j, value=v)
    style_rows(wtl, 4, 3 + len(rows), 5)

    # Running costs (unchanged)
    wr = wb.create_sheet("Running Costs")
    title(wr, "(3) Recurring running cost of the application: unchanged by the build approach")
    header(wr, 3, ["Item", "₹/month low", "₹/month high", "$/month low", "$/month high"], [70, 14, 14, 12, 12])
    rr = [("Pilot running after launch (approved Ledger B with contingency and seats)", BE.runs_lo, BE.runs_hi),
          ("Literal-alignment additions (CR-ALN-02, upper bound)", *BE.aln_run),
          ("Advanced capabilities at full rollout (X1 + X2 + X3)", BE.adv_lo, BE.adv_hi),
          ("Growth gate design point", 50_000, 70_000), ("Scale design point", 130_000, 170_000),
          ("AI-built tooling after the build (maintenance team, per month)", D["ai_tools_after"][0] * M.FX, D["ai_tools_after"][1] * M.FX)]
    for i, (lab, lo, hi) in enumerate(rr, 4):
        for j, v in enumerate([lab, lo, hi, f"=B{i}/FX", f"=C{i}/FX"], 1):
            wr.cell(row=i, column=j, value=v)
    style_rows(wr, 4, 3 + len(rr), 5, money_cols=(2, 3), usd_cols=(4, 5))

    # TCO
    wtc = wb.create_sheet("TCO")
    title(wtc, "(4) Three-year total cost of ownership: traditional vs AI-built")
    r = 3
    for lab, t_, a_ in (("Approved path", BE.tco_ap, D["TCO_AI_AP"]), ("Full roadmap", BE.tco_full, D["TCO_AI_FULL"])):
        wtc.cell(row=r, column=1, value=lab).font = Font(bold=True, color=NAVY)
        header(wtc, r + 1, ["Year", "Traditional low ₹", "Traditional high ₹", "AI-built dev low", "AI-built dev high", "Running low", "Running high", "AI tooling + tokens low", "AI tooling + tokens high",
                            "Maintenance low", "Maintenance high", "Future-proofing low", "Future-proofing high", "AI-built total low ₹", "AI-built total high ₹", "AI-built total low $", "AI-built total high $"], [40] + [14] * 16)
        r0 = r + 2
        for i, (yt, ya) in enumerate(zip(t_, a_), r0):
            tl = sum(yt[j][0] for j in range(1, 6))
            th = sum(yt[j][1] for j in range(1, 6))
            vals = [yt[0], tl, th, ya[1][0], ya[1][1], ya[2][0], ya[2][1], ya[3][0], ya[3][1], ya[4][0], ya[4][1], ya[5][0], ya[5][1],
                    f"=D{i}+F{i}+H{i}+J{i}+L{i}", f"=E{i}+G{i}+I{i}+K{i}+M{i}", f"=N{i}/FX", f"=O{i}/FX"]
            for j, v in enumerate(vals, 1):
                wtc.cell(row=i, column=j, value=v)
        rt = r0 + len(t_)
        wtc.cell(row=rt, column=1, value="Total").font = Font(bold=True)
        for col in "BCDEFGHIJKLMNOPQ":
            wtc[f"{col}{rt}"] = f"=SUM({col}{r0}:{col}{rt - 1})"
            wtc[f"{col}{rt}"].fill = TOT
        style_rows(wtc, r0, rt, 17, money_cols=range(2, 16), usd_cols=(16, 17))
        r = rt + 3
    wtc.freeze_panes = None

    # Risks
    wk2 = wb.create_sheet("Risks")
    title(wk2, "Risks specific to AI-built delivery, and the calibration gate")
    header(wk2, 3, ["Risk", "Effect", "Control"], [45, 40, 90])
    for i, row in enumerate([
        ("Productivity lower than assumed", "Savings shrink towards the conservative case", "Sprint 2 calibration gate (≈ Day 45): measure accepted points per engineer-week before reducing the team"),
        ("Subtle defects in generated code", "Rework, incidents", "Test-first; mandatory human review; rework allowance; SAST; mutation tests on critical modules"),
        ("Security weaknesses or vulnerable dependencies", "Data exposure", "Security agent + independent reviewer; pinning; secret scanning; external pen tests unchanged"),
        ("Licence and IP contamination", "Legal exposure", "Licence scanning; provenance log; AI-code policy; contracts assign IP"),
        ("Over-reliance and skills erosion", "Team cannot maintain code", "Engineers own design and reviews; ADRs current; pairing on critical modules"),
        ("Token cost overruns", "Higher build AI spend", "API budget caps and alerts; caching; model mix tuned"),
        ("Single model provider", "Disruption", "Model-agnostic specs and tests; conventional codebase"),
        ("Personal data reaching build agents", "DPDP breach", "Synthetic data only; no production access for agents"),
    ], 4):
        for j, v in enumerate(row, 1):
            wk2.cell(row=i, column=j, value=v)
    style_rows(wk2, 4, 11, 3)

    # put Comparison second
    wb.move_sheet("Comparison", offset=-2)
    wb.save(path)
    print("XLSX", path)
