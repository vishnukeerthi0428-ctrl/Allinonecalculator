"""Excel workbook for the cost estimate, with live formulas driven by the Inputs sheet."""
from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter
from openpyxl.workbook.defined_name import DefinedName

import model as M

NAVY = "0B3D6B"
HDR = PatternFill("solid", fgColor=NAVY)
INP = PatternFill("solid", fgColor="FFF4CC")
TOT = PatternFill("solid", fgColor="E8EEF5")
THIN = Side(style="thin", color="C9D3DD")
BOX = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)
INR = '"₹"#,##,##0'
INR_L = '"₹"#,##0.00,,"0 L"'   # not used for formulas (lakh shown via /100000)
USD = '"$"#,##0'


def header(ws, row, cols, widths=None):
    for j, c in enumerate(cols, 1):
        cell = ws.cell(row=row, column=j, value=c)
        cell.font = Font(bold=True, color="FFFFFF")
        cell.fill = HDR
        cell.alignment = Alignment(wrap_text=True, vertical="center")
        cell.border = BOX
    if widths:
        for j, w in enumerate(widths, 1):
            ws.column_dimensions[get_column_letter(j)].width = w
    ws.freeze_panes = ws.cell(row=row + 1, column=1)


def style_rows(ws, r0, r1, ncol, money_cols=(), usd_cols=(), wrap=True):
    for r in range(r0, r1 + 1):
        for c in range(1, ncol + 1):
            cell = ws.cell(row=r, column=c)
            cell.border = BOX
            cell.alignment = Alignment(wrap_text=wrap, vertical="top")
            if c in money_cols:
                cell.number_format = INR
            if c in usd_cols:
                cell.number_format = USD


def title(ws, text, sub=None):
    ws["A1"] = text
    ws["A1"].font = Font(bold=True, size=14, color=NAVY)
    if sub:
        ws["A2"] = sub
        ws["A2"].font = Font(italic=True, color="555555")


def build(D, path):
    wb = Workbook()
    # ------------------------------------------------ README
    ws = wb.active
    ws.title = "README"
    title(ws, "AI Growth Engine – End-to-End Cost Estimate v1.0 (28 Nov 2026)", "Companion to the PDF/Word estimate. Change yellow cells on 'Inputs' and every formula recalculates.")
    lines = [
        "Basis: Application Blueprint v1.1 (342 decisions); approved budgets DEC-230/231; Founder decisions DEC-416…418 (Claude Sonnet primary).",
        "Currency: INR with USD at the FX rate on 'Inputs' (default ₹90 = $1, verify). Amounts exclude GST unless stated.",
        "One-time development and recurring subscriptions/running costs are kept on separate sheets and never mixed.",
        "Sheets: Inputs · Summary · Rate Card · Resource Plan · Packages · Effort by Activity · Drafting Effort · AI Catalogue · Build Tooling · Running Costs · Cash Flow · Future-proofing · TCO · Scenarios · Missed Items · Assumptions",
        "All figures are estimates. Third-party prices are list prices to verify at purchase.",
    ]
    for i, t in enumerate(lines, 4):
        ws.cell(row=i, column=1, value=t)
    ws.column_dimensions["A"].width = 160

    # ------------------------------------------------ Inputs
    wi = wb.create_sheet("Inputs")
    title(wi, "Inputs (edit the yellow cells)")
    inputs = [
        ("FX", "₹ per USD", M.FX),
        ("PM_LO", "Loaded cost per person-month, low (₹)", M.PM_RATE[0]),
        ("PM_HI", "Loaded cost per person-month, high (₹)", M.PM_RATE[1]),
        ("DAYS", "Working days per month", M.DAYS_PER_MONTH),
        ("HRS", "Hours per day", M.HOURS_PER_DAY),
        ("CONT", "Contingency on running costs", M.CONTINGENCY),
        ("GST", "GST rate (shown separately)", M.GST),
        ("ESC", "Annual rate escalation from Year 2", 0.08),
        ("MNT_LO", "Maintenance % of cumulative development (low)", 0.15),
        ("MNT_HI", "Maintenance % of cumulative development (high)", 0.20),
        ("ONS_LO", "Onshore contractor rate, low (USD/hour)", M.ONSHORE_USD_HR[0]),
        ("ONS_HI", "Onshore contractor rate, high (USD/hour)", M.ONSHORE_USD_HR[1]),
    ]
    header(wi, 3, ["Name", "Parameter", "Value"], [12, 52, 16])
    for i, (nm, lab, v) in enumerate(inputs, 4):
        wi.cell(row=i, column=1, value=nm)
        wi.cell(row=i, column=2, value=lab)
        c = wi.cell(row=i, column=3, value=v)
        c.fill = INP
        wb.defined_names[nm] = DefinedName(nm, attr_text=f"Inputs!$C${i}")
    r = 4 + len(inputs)
    derived = [("PD_LO", "Cost per person-day, low (₹)", "=PM_LO/DAYS"), ("PD_HI", "Cost per person-day, high (₹)", "=PM_HI/DAYS"),
               ("HR_LO", "Cost per hour, low (₹)", "=PM_LO/(DAYS*HRS)"), ("HR_HI", "Cost per hour, high (₹)", "=PM_HI/(DAYS*HRS)")]
    for i, (nm, lab, f) in enumerate(derived, r):
        wi.cell(row=i, column=1, value=nm)
        wi.cell(row=i, column=2, value=lab)
        wi.cell(row=i, column=3, value=f).number_format = INR
        wb.defined_names[nm] = DefinedName(nm, attr_text=f"Inputs!$C${i}")
    style_rows(wi, 4, r + len(derived) - 1, 3)

    # ------------------------------------------------ Rate Card
    wr = wb.create_sheet("Rate Card")
    title(wr, "Resource rate card (loaded, India delivery)")
    cols = ["Role", "Skill set", "Technology", "Used in", "Per month low ₹", "Per month high ₹", "Per day low ₹", "Per day high ₹", "Per hour low ₹", "Per hour high ₹", "Per hour low $", "Per hour high $"]
    header(wr, 3, cols, [40, 45, 40, 28, 14, 14, 13, 13, 13, 13, 12, 12])
    for i, (role, sk, tech, lo, hi, used) in enumerate(M.RATE_CARD, 4):
        vals = [role, sk, tech, used, lo, hi, f"=E{i}/DAYS", f"=F{i}/DAYS", f"=E{i}/(DAYS*HRS)", f"=F{i}/(DAYS*HRS)", f"=I{i}/FX", f"=J{i}/FX"]
        for j, v in enumerate(vals, 1):
            wr.cell(row=i, column=j, value=v)
    style_rows(wr, 4, 3 + len(M.RATE_CARD), 12, money_cols=range(5, 11), usd_cols=(11, 12))
    for i in range(4, 4 + len(M.RATE_CARD)):
        wr.cell(row=i, column=11).number_format = '"$"#,##0.00'
        wr.cell(row=i, column=12).number_format = '"$"#,##0.00'

    # ------------------------------------------------ Resource Plan (Ledger A)
    wp = wb.create_sheet("Resource Plan")
    title(wp, "Core build to the Release 2 gate: Ledger A (approved, DEC-230)")
    cols = ["#", "Item", "Resource", "FTE", "Months", "Person-months", "Hours", "Vendor/fixed low ₹", "Vendor/fixed high ₹", "Cost low ₹", "Cost high ₹", "Cost low $", "Cost high $", "Source"]
    header(wp, 3, cols, [6, 48, 40, 7, 8, 12, 10, 14, 14, 14, 14, 12, 12, 30])
    for i, (pid, item, role, fte, months, pm, vlo, vhi, src) in enumerate(M.LEDGER_A, 4):
        vals = [pid, item, role, fte, months, pm, f"=F{i}*DAYS*HRS", vlo, vhi, f"=F{i}*PM_LO+H{i}", f"=F{i}*PM_HI+I{i}", f"=J{i}/FX", f"=K{i}/FX", src]
        for j, v in enumerate(vals, 1):
            wp.cell(row=i, column=j, value=v)
    n = 3 + len(M.LEDGER_A)
    t = n + 1
    wp.cell(row=t, column=2, value="Total Ledger A").font = Font(bold=True)
    for col in "FGHIJKLM":
        wp[f"{col}{t}"] = f"=SUM({col}4:{col}{n})"
        wp[f"{col}{t}"].font = Font(bold=True)
        wp[f"{col}{t}"].fill = TOT
    wp.cell(row=t + 1, column=2, value="Management reserve (outside the total)")
    wp.cell(row=t + 1, column=10, value=M.MGMT_RESERVE[0])
    wp.cell(row=t + 1, column=11, value=M.MGMT_RESERVE[1])
    style_rows(wp, 4, t + 1, 14, money_cols=(8, 9, 10, 11), usd_cols=(12, 13))

    # ------------------------------------------------ Packages
    wk = wb.create_sheet("Packages")
    title(wk, "One-time development packages (INR and USD)")
    cols = ["Key", "Package", "Status", "When", "Effort pd low", "Effort pd central", "Effort pd high", "Low ₹", "Central ₹", "High ₹", "Low $", "Central $", "High $", "Approved? (1/0)", "Source"]
    header(wk, 3, cols, [7, 50, 30, 26, 10, 10, 10, 14, 14, 14, 12, 12, 12, 10, 30])
    for i, p in enumerate(M.PACKAGES, 4):
        key, name, status, lo, c, hi, eff, when, src = p
        appr = 1 if status.startswith("Approved") else 0
        vals = [key, name, status, when, eff[0], eff[1], eff[2], lo, c, hi, f"=H{i}/FX", f"=I{i}/FX", f"=J{i}/FX", appr, src]
        for j, v in enumerate(vals, 1):
            cell = wk.cell(row=i, column=j, value=v)
            if j == 14:
                cell.fill = INP
    n = 3 + len(M.PACKAGES)
    wk.cell(row=n + 1, column=2, value="Approved one-time development").font = Font(bold=True)
    wk.cell(row=n + 2, column=2, value="All packages (if every option is approved)").font = Font(bold=True)
    for col in "HIJKLM":
        wk[f"{col}{n + 1}"] = f"=SUMPRODUCT({col}4:{col}{n},$N$4:$N${n})"
        wk[f"{col}{n + 2}"] = f"=SUM({col}4:{col}{n})"
        for rr in (n + 1, n + 2):
            wk[f"{col}{rr}"].fill = TOT
            wk[f"{col}{rr}"].font = Font(bold=True)
    style_rows(wk, 4, n + 2, 15, money_cols=(8, 9, 10), usd_cols=(11, 12, 13))
    pk_total_row = n + 1

    # ------------------------------------------------ Effort by activity
    we = wb.create_sheet("Effort by Activity")
    title(we, "Effort and value by activity (allocation of programme effort, central)")
    header(we, 3, ["Activity", "Share", "Core pd", "Programme pd", "Hours", "Value low ₹", "Value high ₹", "Value low $", "Value high $", "Roles"], [55, 8, 10, 12, 10, 14, 14, 12, 12, 45])
    core_c = D["core_eff"][1]
    prog_c = D["prog_eff"][1]
    for i, (name, share, who) in enumerate(M.ACTIVITY_SPLIT, 4):
        vals = [name, share, f"=B{i}*{core_c}", f"=B{i}*{prog_c}", f"=D{i}*HRS", f"=D{i}*PD_LO", f"=D{i}*PD_HI", f"=F{i}/FX", f"=G{i}/FX", who]
        for j, v in enumerate(vals, 1):
            we.cell(row=i, column=j, value=v)
        we.cell(row=i, column=2).number_format = "0%"
    n = 3 + len(M.ACTIVITY_SPLIT)
    for col in "BCDEFGHI":
        we[f"{col}{n + 1}"] = f"=SUM({col}4:{col}{n})"
        we[f"{col}{n + 1}"].fill = TOT
    we[f"B{n + 1}"].number_format = "0%"
    style_rows(we, 4, n + 1, 10, money_cols=(6, 7), usd_cols=(8, 9))

    # ------------------------------------------------ Drafting effort
    wd = wb.create_sheet("Drafting Effort")
    title(wd, "User stories, test cases and test strategies: drafting effort (three ways of working)")
    header(wd, 3, ["Artefact", "Count", "Manual h/unit low", "Manual h/unit high", "AI-assisted h/unit low", "AI-assisted h/unit high", "Refine drafts h/unit low", "Refine drafts h/unit high",
                   "Manual pd low", "Manual pd high", "AI pd low", "AI pd high", "Refine pd low", "Refine pd high", "Refine cost low ₹", "Refine cost high ₹", "Who"],
           [42, 9, 9, 9, 9, 9, 9, 9, 10, 10, 10, 10, 10, 10, 14, 14, 26])
    for i, (name, key, man, ai, bp, who) in enumerate(M.DRAFTING, 4):
        vals = [name, M.ARTEFACTS[key], man[0], man[1], ai[0], ai[1], bp[0], bp[1],
                f"=B{i}*C{i}/HRS", f"=B{i}*D{i}/HRS", f"=B{i}*E{i}/HRS", f"=B{i}*F{i}/HRS", f"=B{i}*G{i}/HRS", f"=B{i}*H{i}/HRS", f"=M{i}*PD_LO", f"=N{i}*PD_HI", who]
        for j, v in enumerate(vals, 1):
            c = wd.cell(row=i, column=j, value=v)
            if 3 <= j <= 8:
                c.fill = INP
    r0 = 4 + len(M.DRAFTING) + 1
    wd.cell(row=r0, column=1, value="Test strategy documents").font = Font(bold=True)
    header(wd, r0 + 1, ["Document", "Count", "pd each low", "pd each high", "Total pd low", "Total pd high"])
    for i, (name, cnt, rr) in enumerate(M.STRATEGY_DOCS, r0 + 2):
        for j, v in enumerate([name, cnt, rr[0], rr[1], f"=B{i}*C{i}", f"=B{i}*D{i}"], 1):
            wd.cell(row=i, column=j, value=v)
    style_rows(wd, 4, r0 + 1 + len(M.STRATEGY_DOCS), 17, money_cols=(15, 16))

    # ------------------------------------------------ AI catalogue
    wc = wb.create_sheet("AI Catalogue")
    title(wc, f"AI agents, automations and workflows ({len(D['cat'])}): what they do, automation level, build and run cost, timeline")
    cols = ["ID", "Type", "Name", "What it does", "Automation level", "Autonomy", "Model tier", "Complexity", "Build pd low", "Build pd high", "Build cost low ₹", "Build cost high ₹",
            "Build cost low $", "Build cost high $", "Run ₹/month low", "Run ₹/month base", "Run ₹/month high", "Run $/month base", "Run-cost note", "Release", "Window", "Dates", "Skill set", "Technology", "Origin"]
    header(wc, 3, cols, [9, 11, 34, 70, 30, 16, 22, 10, 8, 8, 13, 13, 11, 11, 10, 10, 10, 10, 30, 18, 16, 20, 45, 45, 13])
    tmap = {"AG": "AI agent", "AU": "Automation", "WF": "Workflow"}
    for i, it in enumerate(D["cat"], 4):
        vals = [it["id"], tmap[it["kind"]], it["name"], it["what"], it["level"], it["autonomy"], it["tier"], it["complexity"], it["pd_lo"], it["pd_hi"],
                f"=I{i}*PD_LO", f"=J{i}*PD_HI", f"=K{i}/FX", f"=L{i}/FX", it["run_lo"], it["run_base"], it["run_hi"], f"=P{i}/FX", it["run_note"],
                it["release"], it["window"], it["dates"], it["skills"], it["tech"], it["origin"]]
        for j, v in enumerate(vals, 1):
            wc.cell(row=i, column=j, value=v)
    n = 3 + len(D["cat"])
    wc.cell(row=n + 1, column=3, value="Total").font = Font(bold=True)
    for col in "IJKLMNOPQR":
        wc[f"{col}{n + 1}"] = f"=SUM({col}4:{col}{n})"
        wc[f"{col}{n + 1}"].fill = TOT
    style_rows(wc, 4, n + 1, len(cols), money_cols=(11, 12, 15, 16, 17), usd_cols=(13, 14, 18))
    wc.auto_filter.ref = f"A3:{get_column_letter(len(cols))}{n}"

    # ------------------------------------------------ Build tooling
    wt = wb.create_sheet("Build Tooling")
    title(wt, "Subscriptions and tools needed to build (USD list prices per user per month; verify)")
    cols = ["Tool", "Purpose", "Plan", "Unit $ low", "Unit $ high", "Seats (build)", "Seats (after build)", "Status", "Month $ low", "Month $ high", "Month ₹ low", "Month ₹ high",
            "Build months", "Build total ₹ low", "Build total ₹ high", "After-build month $ low", "After-build month $ high", "Notes"]
    header(wt, 3, cols, [42, 45, 28, 9, 9, 8, 8, 18, 10, 10, 12, 12, 8, 14, 14, 10, 10, 45])
    for i, r in enumerate(D["tool_rows"], 4):
        vals = [r["name"], r["purpose"], r["plan"], r["ulo"], r["uhi"], r["seats"], r["after"], r["req"], f"=D{i}*F{i}", f"=E{i}*F{i}", f"=I{i}*FX", f"=J{i}*FX",
                M.BUILD_MONTHS_CORE, f"=K{i}*M{i}", f"=L{i}*M{i}", f"=D{i}*G{i}", f"=E{i}*G{i}", r["note"]]
        for j, v in enumerate(vals, 1):
            c = wt.cell(row=i, column=j, value=v)
            if j in (4, 5, 6, 7, 13):
                c.fill = INP
    n = 3 + len(D["tool_rows"])
    wt.cell(row=n + 1, column=1, value="Total (all rows, including approved baseline and optional)").font = Font(bold=True)
    for col in "IJKLNOPQ":
        wt[f"{col}{n + 1}"] = f"=SUM({col}4:{col}{n})"
        wt[f"{col}{n + 1}"].fill = TOT
    style_rows(wt, 4, n + 1, len(cols), money_cols=(11, 12, 14, 15), usd_cols=(4, 5, 9, 10, 16, 17))

    # ------------------------------------------------ Running costs
    wrn = wb.create_sheet("Running Costs")
    title(wrn, "Recurring subscriptions and running costs after and during the build (Ledger B, DEC-231, plus v1.1 additions)")
    cols = ["Line", "Category", "Item", "Billing", "₹/month low", "₹/month high", "$/month low", "$/month high", "₹/year low", "₹/year high", "Active from", "Nature"]
    header(wrn, 3, cols, [9, 12, 60, 24, 12, 12, 11, 11, 13, 13, 20, 18])
    for i, (line, catg, item, billing, lo, hi, start, nature) in enumerate(M.LEDGER_B, 4):
        vals = [line, catg, item, billing, lo, hi, f"=E{i}/FX", f"=F{i}/FX", f"=E{i}*12", f"=F{i}*12", start, nature]
        for j, v in enumerate(vals, 1):
            c = wrn.cell(row=i, column=j, value=v)
            if j in (5, 6):
                c.fill = INP
    n = 3 + len(M.LEDGER_B)
    rows = [("Base subtotal", f"=SUM(E4:E{n})", f"=SUM(F4:F{n})"),
            ("B11 contingency", f"=E{n + 1}*CONT", f"=F{n + 1}*CONT"),
            ("B09 Claude seats (2 × $20 × 1.15)", M.SEATS_B09, M.SEATS_B09),
            ("Total pilot running (approved)", f"=E{n + 1}+E{n + 2}+E{n + 3}", f"=F{n + 1}+F{n + 2}+F{n + 3}")]
    for k, (lab, a, b) in enumerate(rows, n + 1):
        wrn.cell(row=k, column=3, value=lab).font = Font(bold=True)
        wrn.cell(row=k, column=5, value=a)
        wrn.cell(row=k, column=6, value=b)
        for col, f in (("G", f"=E{k}/FX"), ("H", f"=F{k}/FX"), ("I", f"=E{k}*12"), ("J", f"=F{k}*12")):
            wrn[f"{col}{k}"] = f
        for col in "EFGHIJ":
            wrn[f"{col}{k}"].fill = TOT
    k0 = n + 6
    wrn.cell(row=k0, column=1, value="v1.1 additions (separately approved per release)").font = Font(bold=True)
    for k, (line, item, lo, hi, frm, st) in enumerate(M.RUN_ADDITIONS, k0 + 1):
        for j, v in enumerate([line, "v1.1", item, st, lo, hi, f"=E{k}/FX", f"=F{k}/FX", f"=E{k}*12", f"=F{k}*12", frm, "Recurring"], 1):
            wrn.cell(row=k, column=j, value=v)
    k1 = k0 + len(M.RUN_ADDITIONS) + 1
    wrn.cell(row=k1, column=3, value="All-in pilot running after the full advanced roadmap").font = Font(bold=True)
    wrn[f"E{k1}"] = f"=E{n + 4}+SUM(E{k0 + 1}:E{k1 - 1})"
    wrn[f"F{k1}"] = f"=F{n + 4}+SUM(F{k0 + 1}:F{k1 - 1})"
    for col, f in (("G", f"=E{k1}/FX"), ("H", f"=F{k1}/FX"), ("I", f"=E{k1}*12"), ("J", f"=F{k1}*12")):
        wrn[f"{col}{k1}"] = f
    for col in "EFGHIJ":
        wrn[f"{col}{k1}"].fill = TOT
    k2 = k1 + 2
    wrn.cell(row=k2, column=1, value="Optional / conditional lines").font = Font(bold=True)
    for k, (line, item, lo, hi, when) in enumerate(M.LEDGER_B_OPTIONAL, k2 + 1):
        for j, v in enumerate([line, "Optional", item, when, lo, hi, f"=E{k}/FX", f"=F{k}/FX", f"=E{k}*12", f"=F{k}*12", when, "Conditional"], 1):
            wrn.cell(row=k, column=j, value=v)
    k3 = k2 + len(M.LEDGER_B_OPTIONAL) + 2
    wrn.cell(row=k3, column=1, value="Running cost as the business scales").font = Font(bold=True)
    for k, (stage, host, ai, tot, gate) in enumerate(M.SCALE_STAGES, k3 + 1):
        for j, v in enumerate(["Scale", stage, f"Hosting {host}; AI {ai}", gate, tot[0], tot[1], f"=E{k}/FX", f"=F{k}/FX", f"=E{k}*12", f"=F{k}*12", "", ""], 1):
            wrn.cell(row=k, column=j, value=v)
    style_rows(wrn, 4, k3 + len(M.SCALE_STAGES), 12, money_cols=(5, 6, 9, 10), usd_cols=(7, 8))

    # ------------------------------------------------ Cash flow
    wf = wb.create_sheet("Cash Flow")
    title(wf, "Month-by-month cash flow: approved scope (core + alignment + A1)")
    cols = ["Month", "Development low ₹", "Development central ₹", "Development high ₹", "Running central ₹", "Tooling central ₹", "Total central ₹", "Cumulative low ₹", "Cumulative central ₹", "Cumulative high ₹", "Cumulative central $"]
    header(wf, 3, cols, [12, 15, 15, 15, 14, 14, 15, 16, 16, 16, 14])
    for i, r in enumerate(D["cash"], 4):
        vals = [r["m"], r["dev"][0], r["dev"][1], r["dev"][2], r["run"][1], r["tools"][1], f"=C{i}+E{i}+F{i}", r["cum"][0], f"=I{i - 1}+G{i}" if i > 4 else f"=G{i}", r["cum"][2], f"=I{i}/FX"]
        for j, v in enumerate(vals, 1):
            wf.cell(row=i, column=j, value=v)
    style_rows(wf, 4, 3 + len(D["cash"]), 11, money_cols=range(2, 11), usd_cols=(11,))

    # ------------------------------------------------ Future-proofing
    wfp = wb.create_sheet("Future-proofing")
    title(wfp, "Future-proofing and lifecycle costs per year (after launch)")
    header(wfp, 3, ["Item", "Basis", "Per year low ₹", "Per year high ₹", "Per year low $", "Per year high $"], [60, 55, 15, 15, 13, 13])
    for i, (name, basis, lo, hi) in enumerate(D["fp_rows"], 4):
        for j, v in enumerate([name, basis, lo if lo is not None else "15–20% of cumulative development (see TCO)", hi if hi is not None else "", f"=IF(ISNUMBER(C{i}),C{i}/FX,\"\")", f"=IF(ISNUMBER(D{i}),D{i}/FX,\"\")"], 1):
            wfp.cell(row=i, column=j, value=v)
    n = 3 + len(D["fp_rows"])
    wfp.cell(row=n + 1, column=1, value="Total per year (excluding maintenance %)").font = Font(bold=True)
    for col in "CDEF":
        wfp[f"{col}{n + 1}"] = f"=SUM({col}4:{col}{n})"
        wfp[f"{col}{n + 1}"].fill = TOT
    style_rows(wfp, 4, n + 1, 6, money_cols=(3, 4), usd_cols=(5, 6))

    # ------------------------------------------------ TCO
    wtc = wb.create_sheet("TCO")
    title(wtc, "Three-year total cost of ownership (build + 3 years)")
    r = 3
    for lab, t in (("Approved path: core + alignment + A1", D["tco_ap"]), ("Full roadmap: core + alignment + A1 + A2 + A3 + Phase 2", D["tco_full"])):
        wtc.cell(row=r, column=1, value=lab).font = Font(bold=True, color=NAVY)
        header(wtc, r + 1, ["Year", "Development low", "Development high", "Running low", "Running high", "Tooling low", "Tooling high", "Maintenance low", "Maintenance high",
                            "Future-proofing low", "Future-proofing high", "Total low ₹", "Total high ₹", "Total low $", "Total high $"], [42] + [14] * 14)
        r0 = r + 2
        for i, y in enumerate(t, r0):
            vals = [y[0], y[1][0], y[1][1], y[2][0], y[2][1], y[3][0], y[3][1], y[4][0], y[4][1], y[5][0], y[5][1],
                    f"=B{i}+D{i}+F{i}+H{i}+J{i}", f"=C{i}+E{i}+G{i}+I{i}+K{i}", f"=L{i}/FX", f"=M{i}/FX"]
            for j, v in enumerate(vals, 1):
                wtc.cell(row=i, column=j, value=v)
        rt = r0 + len(t)
        wtc.cell(row=rt, column=1, value="Total").font = Font(bold=True)
        for col in "BCDEFGHIJKLMNO":
            wtc[f"{col}{rt}"] = f"=SUM({col}{r0}:{col}{rt - 1})"
            wtc[f"{col}{rt}"].fill = TOT
        style_rows(wtc, r0, rt, 15, money_cols=range(2, 14), usd_cols=(14, 15))
        r = rt + 3
    wtc.freeze_panes = None

    # ------------------------------------------------ Scenarios
    wsn = wb.create_sheet("Scenarios")
    title(wsn, f"Permutations: {len(D['scen'])} combinations of scope × team model × estimate point (INR; USD and FX sensitivity by formula)")
    header(wsn, 3, ["Scope", "Scope description", "Team model", "Team description", "Estimate point", "Effort pd", "Cost ₹", "Cost $ (FX input)", "Cost $ at ₹85", "Cost $ at ₹95"],
           [7, 45, 8, 48, 10, 10, 15, 14, 14, 14])
    for i, s in enumerate(D["scen"], 4):
        for j, v in enumerate([s["sid"], s["sname"], s["tid"], s["tname"], s["pt"], s["eff"], s["inr"], f"=G{i}/FX", f"=G{i}/85", f"=G{i}/95"], 1):
            wsn.cell(row=i, column=j, value=v)
    style_rows(wsn, 4, 3 + len(D["scen"]), 10, money_cols=(7,), usd_cols=(8, 9, 10))
    wsn.auto_filter.ref = f"A3:J{3 + len(D['scen'])}"

    # ------------------------------------------------ Missed items
    wm = wb.create_sheet("Missed Items")
    title(wm, "Items often missed and how they are treated")
    header(wm, 3, ["Item", "What it is", "Treatment", "Indicative cost"], [36, 55, 45, 45])
    for i, row in enumerate(M.MISSED, 4):
        for j, v in enumerate(row, 1):
            wm.cell(row=i, column=j, value=v)
    style_rows(wm, 4, 3 + len(M.MISSED), 4)

    # ------------------------------------------------ Summary (formulas)
    wsu = wb.create_sheet("Summary", 1)
    title(wsu, "Summary: one-time development vs recurring subscriptions (INR and USD)")
    header(wsu, 3, ["Item", "Low ₹", "Central ₹", "High ₹", "Low $", "Central $", "High $", "Notes"], [62, 15, 15, 15, 13, 13, 13, 50])
    items = [
        ("ONE-TIME DEVELOPMENT", None, None, None, ""),
        ("Approved one-time development (core + alignment + A1)", f"=Packages!H{pk_total_row}", f"=Packages!I{pk_total_row}", f"=Packages!J{pk_total_row}", "Packages sheet, Approved = 1"),
        ("All packages if every option is approved", f"=Packages!H{pk_total_row + 1}", f"=Packages!I{pk_total_row + 1}", f"=Packages!J{pk_total_row + 1}", "Adds Phase 2, A2, A3"),
        ("Core build Ledger A (resource plan)", f"='Resource Plan'!J{3 + len(M.LEDGER_A) + 1}", None, f"='Resource Plan'!K{3 + len(M.LEDGER_A) + 1}", "Approved DEC-230"),
        ("RECURRING (SUBSCRIPTIONS AND RUNNING)", None, None, None, ""),
        ("Pilot running per month (approved Ledger B with contingency and seats)", f"='Running Costs'!E{3 + len(M.LEDGER_B) + 4}", None, f"='Running Costs'!F{3 + len(M.LEDGER_B) + 4}", "Per month"),
        ("All-in running per month after the full advanced roadmap", f"='Running Costs'!E{3 + len(M.LEDGER_B) + 6 + len(M.RUN_ADDITIONS) + 1}", None, f"='Running Costs'!F{3 + len(M.LEDGER_B) + 6 + len(M.RUN_ADDITIONS) + 1}", "Per month"),
        ("Running cost paid during the build (Day 1–208)", D["B_DURING_BUILD"][0], None, D["B_DURING_BUILD"][1], "Total for the build period"),
        ("Approved build-time tooling per month (DEC-419; excl. Ledger B baseline and optional)", D["rec"][0] * M.FX, None, D["rec"][1] * M.FX, "See Build Tooling (DEC-419 rows)"),
        ("THREE-YEAR TCO", None, None, None, ""),
        ("Approved path (build + 3 years)", f"=TCO!L{3 + 2 + len(D['tco_ap'])}", None, f"=TCO!M{3 + 2 + len(D['tco_ap'])}", "TCO sheet"),
        ("Full roadmap (build + 3 years)", f"=TCO!L{3 + 2 + len(D['tco_ap']) + 3 + 2 + len(D['tco_full'])}", None, f"=TCO!M{3 + 2 + len(D['tco_ap']) + 3 + 2 + len(D['tco_full'])}", "TCO sheet"),
    ]
    for i, (lab, lo, c, hi, note) in enumerate(items, 4):
        wsu.cell(row=i, column=1, value=lab)
        if lo is None:
            wsu.cell(row=i, column=1).font = Font(bold=True, color=NAVY)
            continue
        wsu.cell(row=i, column=2, value=lo)
        wsu.cell(row=i, column=3, value=c if c is not None else f"=(B{i}+D{i})/2")
        wsu.cell(row=i, column=4, value=hi)
        wsu.cell(row=i, column=5, value=f"=B{i}/FX")
        wsu.cell(row=i, column=6, value=f"=C{i}/FX")
        wsu.cell(row=i, column=7, value=f"=D{i}/FX")
        wsu.cell(row=i, column=8, value=note)
    style_rows(wsu, 4, 3 + len(items), 8, money_cols=(2, 3, 4), usd_cols=(5, 6, 7))

    # ------------------------------------------------ Assumptions
    wa = wb.create_sheet("Assumptions")
    title(wa, "Assumptions and exclusions")
    for i, t in enumerate([
        "Figures are estimates as of 28 Nov 2026; approved budgets (DEC-230/231, DEC-416/417) govern where they differ.",
        "INR/USD at the FX input (default ₹90 = $1, verify).",
        "Loaded India delivery rates ₹1.0–1.5 lakh per person-month; 22 working days; 8 hours per day.",
        "GST, Founder time, paid ad media, external legal counsel and customer-funded tenant usage are excluded from totals.",
        "Third-party prices are list prices to verify at purchase.",
        "Per-item build effort for agents/automations/workflows is a parametric allocation within programme effort.",
        "AI run cost per agent comes from each agent's token formula at pilot volumes; production is capped by the gateway.",
        "A2/A3 cost split pro rata to effort (A2 64.7%, A3 35.3%).",
        "Advanced running costs ramp 35% in A1, 70% in A2 and 100% after A3.",
        "Maintenance 15–20% of cumulative development per year; 8% annual escalation from Year 2.",
        "Year-2/Year-3 running costs assume the growth and scale gates pass.",
    ], 3):
        wa.cell(row=i, column=1, value=f"{i - 2}. {t}")
    wa.column_dimensions["A"].width = 140

    wb.save(path)
    print("XLSX", path)
