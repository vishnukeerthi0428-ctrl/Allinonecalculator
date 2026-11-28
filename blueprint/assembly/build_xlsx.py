#!/usr/bin/env python3
"""Build the companion Excel workbook from the blueprint Markdown.

Sheets: README, Traceability (from final/RTM.csv if present), User Stories, Test Cases,
AI Agents & Automations, Business Requirements, Functional Requirements, Decisions, Tags Register.
Usage: python3 blueprint/assembly/build_xlsx.py
"""
import csv, re
from pathlib import Path
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.utils import get_column_letter

BP = Path(__file__).resolve().parent.parent
OUT = BP / "final" / "AI_Growth_Engine_Blueprint_Workbook_v1.1.xlsx"
HDR_FILL = PatternFill("solid", fgColor="0B3D6B")


def cells(line):
    return [c.strip() for c in line.strip().strip("|").split("|")]


def md_tables(text):
    """Yield (header, rows) for every pipe table."""
    lines = text.splitlines()
    i = 0
    while i < len(lines) - 1:
        if lines[i].startswith("|") and re.match(r"^\|\s*:?-{3,}", lines[i + 1]):
            hdr = cells(lines[i]); rows = []; j = i + 2
            while j < len(lines) and lines[j].startswith("|"):
                rows.append(cells(lines[j])); j += 1
            yield hdr, rows
            i = j
        else:
            i += 1


def clean(s):
    return re.sub(r"\*\*|`", "", s or "").strip()


def add_sheet(wb, title, header, rows, widths=None):
    ws = wb.create_sheet(title[:31])
    ws.append(header)
    for c in ws[1]:
        c.font = Font(bold=True, color="FFFFFF"); c.fill = HDR_FILL
        c.alignment = Alignment(wrap_text=True, vertical="top")
    for r in rows:
        ws.append([clean(str(x)) for x in r])
    for idx, _ in enumerate(header, 1):
        ws.column_dimensions[get_column_letter(idx)].width = (widths or {}).get(idx, 28)
    for row in ws.iter_rows(min_row=2):
        for c in row:
            c.alignment = Alignment(wrap_text=True, vertical="top")
    ws.freeze_panes = "A2"
    ws.auto_filter.ref = ws.dimensions
    return ws


def parse_stories():
    out = []
    for f in sorted(list(BP.glob("Part-05-*.md")) + [q for q in BP.glob("Part-*.md") if not q.name.startswith("Part-05")]):
        text = f.read_text(encoding="utf-8")
        heads = list(re.finditer(r"^#{3,6} (US-\d{4}|US-\d{2}-(?:E[A-Z]|V\d)\d{2})\s*[:—–-]?\s*(.*)$", text, re.M))
        for k, m in enumerate(heads):
            seg = text[m.end(): heads[k + 1].start() if k + 1 < len(heads) else len(text)]
            kv = {}
            for ln in seg.splitlines():
                if ln.startswith("```"):
                    break
                if ln.startswith("|") and not re.match(r"^\|\s*:?-{3,}", ln):
                    c = cells(ln)
                    if len(c) >= 2 and c[0].lower() not in ("field",):
                        kv[c[0].lower()] = " | ".join(c[1:])
            def pick(*keys):
                for key in keys:
                    for kk, vv in kv.items():
                        if key in kk:
                            return vv
                return ""
            scen = len(re.findall(r"^\s*Scenario( Outline)?:", seg, re.M))
            sid = m.group(1)
            out.append([sid, "EP-" + sid[3:5], clean(m.group(2)), pick("type"), pick("persona"),
                        pick("story", "statement"), pick("link"), pick("priority"), pick("wave"),
                        pick("point"), pick("depend"), scen, f.name])
    seen, uniq = set(), []
    for r in out:
        if r[0] not in seen:
            seen.add(r[0]); uniq.append(r)
    return uniq


def parse_by_prefix(globpat, id_re):
    rows, hdr_used = [], None
    for f in sorted(BP.glob(globpat)):
        for hdr, rs in md_tables(f.read_text(encoding="utf-8")):
            for r in rs:
                if r and re.match(id_re, clean(r[0])):
                    rows.append([clean(r[0])] + [" | ".join(f"{h}: {v}" for h, v in zip(hdr[1:], r[1:]))] + [f.name])
    seen, uniq = set(), []
    for r in rows:
        if r[0] not in seen:
            seen.add(r[0]); uniq.append(r)
    return uniq


def parse_table_rows(globpat, id_re, want_cols=None):
    rows = []
    for f in sorted(BP.glob(globpat)):
        for hdr, rs in md_tables(f.read_text(encoding="utf-8")):
            for r in rs:
                if r and re.match(id_re, clean(r[0])):
                    rows.append((hdr, r, f.name))
    return rows


def main():
    wb = Workbook(); ws = wb.active; ws.title = "README"
    ws.append(["AI Growth Engine – Application Blueprint workbook (v1.1, 28 Nov 2026)"])
    ws.append(["Generated from the blueprint Markdown by assembly/build_xlsx.py. The Markdown/PDF/DOCX remain authoritative."])
    ws.append(["Sheets: Traceability, User Stories, Test Cases, AI Agents & Automations, Business Requirements, Functional Requirements, Decisions, Cost Ledgers, Advanced FRs (v1.1), Traceability v1.1, Literal Alignment, Source Pack Coverage, Tags Register"])
    ws.column_dimensions["A"].width = 140
    ws["A1"].font = Font(bold=True, size=14)

    rtm = BP / "final" / "RTM.csv"
    if rtm.exists():
        with rtm.open(encoding="utf-8") as fh:
            rd = list(csv.reader(fh))
        if rd:
            add_sheet(wb, "Traceability", rd[0], rd[1:])

    stories = parse_stories()
    have = {r[0] for r in stories}
    for hdr, r, fn in parse_table_rows("Part-*.md", r"^US-\d{2}-(?:E[A-Z]|V\d)\d{2}$"):
        sid = clean(r[0])
        if sid in have:
            continue
        have.add(sid)
        d = {h.lower(): clean(v) for h, v in zip(hdr, r)}
        g = lambda *ks: next((v for k, v in d.items() for kk in ks if kk in k), "")
        stories.append([sid, "EP-" + sid[3:5], g("title", "story"), "Enhancement", "", g("story", "statement", "as the"),
                        g("fr", "link", "trace"), g("prior", "moscow"), g("wave"), g("point", "sp"), g("depend"), "", fn])
    add_sheet(wb, "User Stories", ["Story ID", "Epic", "Title", "Type", "Persona", "Story statement", "Links",
                                   "Priority", "Wave", "Points", "Dependencies", "Gherkin scenarios", "Source file"],
              stories, {3: 40, 6: 70, 7: 50, 11: 40})

    tcs = parse_by_prefix("Part-*.md", r"^(TC-|VER-)")
    add_sheet(wb, "Test Cases", ["Test case / verification ID", "Details (column: value)", "Source file"], tcs, {2: 160})

    ags = parse_by_prefix("Part-09-4_*.md", r"^(AG|AU|WF)-\d{2,3}$") or parse_by_prefix("Part-07-*.md", r"^(AG|AU)-\d{3}$")
    add_sheet(wb, "AI Agents & Automations", ["ID", "Details (column: value)", "Source file"], ags, {2: 160})

    brs = parse_by_prefix("Part-01_*.md", r"^BR-(M\d{2}|TENANT|WEB|AUTO|SVC|QA|S\d{3})$")
    add_sheet(wb, "Business Requirements", ["BR ID", "Details (column: value)", "Source file"], brs, {2: 160})

    frs = parse_by_prefix("Part-02-1_*.md", r"^FR-")
    add_sheet(wb, "Functional Requirements", ["FR ID", "Details (column: value)", "Source file"], frs, {2: 160})

    decs = sum((parse_by_prefix(g, r"^\**DEC-\d{3}\**$") for g in ("Part-00A_*.md", "Part-09-1_*.md", "Part-09-5_*.md", "Part-08-4_*.md", "Part-09-6*_*.md", "Part-09-7*_*.md", "Part-09-8*_*.md", "Part-09-9*_*.md", "Part-09-10_*.md")), [])
    decs = sorted({r[0]: r for r in decs}.values())
    add_sheet(wb, "Decisions", ["DEC ID", "Details (column: value)", "Source file"], decs, {2: 160})

    costs = parse_table_rows("Part-08-4_*.md", r"^(A\d|B\d|[A-Z]\d\.\d|Total|\*\*)")
    add_sheet(wb, "Cost Ledgers", ["Item", "Details (column: value)", "Source file"],
              [[clean(r[0])] + [" | ".join(f"{h}: {v}" for h, v in zip(h_[1:], r[1:]))] + [fn] for h_, r, fn in costs], {2: 160})

    adv = parse_by_prefix("Part-09-[789]*_*.md", r"^FR-ADV-X\d-\d{3}$")
    add_sheet(wb, "Advanced FRs (v1.1)", ["FR-ADV ID", "Details (column: value)", "Source file"], adv, {2: 160})
    rtma = BP / "final" / "RTM_advanced.csv"
    if rtma.exists():
        with rtma.open(encoding="utf-8") as fh:
            rd = list(csv.reader(fh))
        add_sheet(wb, "Traceability v1.1", rd[0], rd[1:], {4: 50, 5: 50, 6: 60})
    aln = []
    for f in sorted((BP / "final" / "coverage").glob("alignment_*.csv")):
        with f.open(encoding="utf-8") as fh:
            for r in csv.DictReader(fh):
                aln.append([r.get(k, "") for k in ("group", "doc", "aspect_id", "old_status", "new_status", "alignment_type", "dec", "new_ids", "note")])
    add_sheet(wb, "Literal Alignment", ["Group", "Doc", "Aspect ID", "Old status", "New status", "Alignment type", "DEC", "New IDs", "Note"], aln, {9: 80})

    cov = []
    for f in sorted((BP / "final" / "coverage").glob("?_coverage.csv")):
        with f.open(encoding="utf-8") as fh:
            for r in csv.DictReader(fh):
                cov.append([f.stem[0]] + [r.get(k, "") for k in ("doc", "section", "aspect_id", "aspect_summary", "status", "blueprint_location", "action", "new_ids")])
    add_sheet(wb, "Source Pack Coverage", ["Group", "Doc", "Section", "Aspect ID", "Aspect", "Status", "Blueprint location", "Action", "New IDs"],
              cov, {5: 70, 7: 40, 8: 60})

    tags = []
    pat = re.compile(r"\[(ASSUMPTION|GAP|CONFLICT|RECOMMENDATION)-(\d{3})\]")
    for f in sorted(BP.glob("Part-*.md")):
        for ln in f.read_text(encoding="utf-8").splitlines():
            for m in pat.finditer(ln):
                tags.append([f"{m.group(1)}-{m.group(2)}", m.group(1), f.name, clean(ln)[:400]])
    first = {}
    for t in tags:
        first.setdefault(t[0], t)
    add_sheet(wb, "Tags Register", ["Tag", "Type", "First seen in", "Context (first occurrence)"],
              sorted(first.values()), {4: 140})

    OUT.parent.mkdir(exist_ok=True)
    wb.save(OUT)
    print(f"{OUT}: stories={len(stories)} test_cases={len(tcs)} agents={len(ags)} BRs={len(brs)} FRs={len(frs)} DECs={len(decs)} tags={len(first)}")


if __name__ == "__main__":
    main()
