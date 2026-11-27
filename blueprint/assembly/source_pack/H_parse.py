#!/usr/bin/env python3
"""Group H parser: docs 20 (backlog/runbook), 23 (QC checklist), 24 (RTM/acceptance)
plus decision records in docs 07/08. Writes H_parsed.json next to this script's output dir.
Usage: python3 -I H_parse.py <docs38_dir> <out_json>
"""
import json, re, sys
from pathlib import Path

D = Path(sys.argv[1]); OUT = Path(sys.argv[2])

def read(prefix):
    return next(D.glob(prefix + "_*.txt")).read_text(encoding="utf-8").splitlines()

def tables(lines):
    """Yield (start_line, heading_context, header_cells, rows) for each [TABLE] block."""
    i, ctx = 0, []
    h1 = h2 = ""
    while i < len(lines):
        l = lines[i]
        if l.startswith("<Heading1>"): h1 = l[10:].strip(); h2 = ""
        elif l.startswith("<Heading2>"): h2 = l[10:].strip()
        if l.strip() == "[TABLE]":
            start = i; i += 1; header = []
            while i < len(lines) and lines[i].strip() not in ("---row", "[/TABLE]"):
                header.append(lines[i]); i += 1
            rows, cur = [], None
            while i < len(lines) and lines[i].strip() != "[/TABLE]":
                if lines[i].strip() == "---row":
                    if cur is not None: rows.append(cur)
                    cur = []
                else:
                    cur.append(lines[i])
                i += 1
            if cur: rows.append(cur)
            yield start, h1, h2, header, rows
        i += 1

out = {}

# ---------------- Doc 23: QCs ----------------
L23 = read("23")
qcs = {}
for start, h1, h2, header, rows in tables(L23):
    for r in rows:
        if not r: continue
        m = re.match(r"^((?:UX-)?QC-\d+)\s+(.*)$", r[0])
        if m and len(r) >= 3:
            qid, title = m.group(1), m.group(2).strip()
            body = r[1] if len(r) > 1 else ""
            acc, proc, cmd, ev = body, "", "", ""
            mm = re.match(r"^(.*?)Procedure: (.*?)Command template: (.*?)Evidence: (.*)$", body)
            if mm: acc, proc, cmd, ev = [x.strip() for x in mm.groups()]
            own = r[2] if len(r) > 2 else ""
            owner, reviewer = own, ""
            m2 = re.match(r"^(.*?)Reviewer: (.*)$", own)
            if m2: owner, reviewer = m2.group(1).strip(), m2.group(2).strip()
            ps = r[3] if len(r) > 3 else ""
            m3 = re.match(r"^(Critical|High|Medium|Low)(.*)$", ps)
            prio, status = (m3.group(1), m3.group(2)) if m3 else (ps, "")
            qcs[qid] = dict(id=qid, layer=h2, section=h1, title=title, acceptance=acc, procedure=proc,
                            command=cmd, evidence=ev, owner=owner, reviewer=reviewer, priority=prio,
                            status=status, line=start)
        elif r[0].startswith("UX-QC-"):
            qid = r[0].strip()
            qcs[qid] = dict(id=qid, layer="Expansion QC and sign-off", section=h1, title=r[1] if len(r)>1 else "",
                            acceptance=r[2] if len(r)>2 else "", procedure=r[1] if len(r)>1 else "",
                            command="", evidence=f"evidence/qc/{qid}.json", owner="QA lead + product owner",
                            reviewer="Independent reviewer", priority="Critical", status="Pending", line=start)
out["qc"] = qcs
# layer summary (25 layers + business invariants, heading-based summary sections)
layers = []
for i, l in enumerate(L23[:140]):
    m = re.match(r"<Heading2> (\d\d)  (.*)$", l)
    if m:
        own = L23[i+1]; chk = L23[i+2]; pe = L23[i+3]
        layers.append(dict(no=m.group(1), name=m.group(2).strip(), owner=own.split("|")[0].replace("Owner:", "").strip(),
                           check=chk.replace("Check:", "").strip(), pass_evidence=pe.replace("Pass evidence:", "").strip()))
out["qc_layers"] = layers
# mandatory gates table in doc 23
gates = []
for start, h1, h2, header, rows in tables(L23):
    if h2 == "Mandatory measurable gates":
        for r in rows: gates.append(r)
out["qc_mandatory_gates"] = gates

# ---------------- Doc 24: RTM ----------------
L24 = read("24")
rtm = []
i = 0
while i < len(L24):
    m = re.match(r"<Heading2> ([WA]\d{2,3}) — (.*)$", L24[i])
    if m and i + 8 < len(L24) and L24[i+2].startswith("Access:"):
        sid, title = m.group(1), m.group(2).strip()
        acc = L24[i+2]
        ma = re.match(r"Access: (.*?) \| Functional requirement: (\S+) \| Business requirements: (.*)$", acc)
        brdesc = L24[i+3]; impl = L24[i+4]
        ops = L24[i+5].replace("REST operations:", "").strip()
        ents = L24[i+6].replace("Data entities:", "").strip()
        tl = L24[i+7]
        mt = re.match(r"Proposed Unit: (.*?) \| SIT: (.*?) \| UAT: (.*?) \| QC: (.*?) \| Acceptance: (.*)$", tl)
        rtm.append(dict(screen=sid, title=title, access=ma.group(1), fr=ma.group(2),
                        brs=[b.strip() for b in ma.group(3).split(";")], br_desc=brdesc, implement=impl,
                        ops=[o.strip() for o in ops.split(";") if o.strip()],
                        entities=[e.strip() for e in ents.split(";") if e.strip()],
                        unit=[u.strip() for u in mt.group(1).split(";")], sit=[s.strip() for s in mt.group(2).split(";")],
                        uat=[u.strip() for u in mt.group(3).split(";")], qc=mt.group(4), acceptance=mt.group(5)))
        i += 8; continue
    i += 1
out["rtm"] = rtm
nonscreen = []
for start, h1, h2, header, rows in tables(L24):
    if header and header[0].startswith("Non-screen requirement"):
        for r in rows:
            fr, br = r[0].split()
            op = r[1]; t = r[2]
            unit, sit = t.split(" / ")
            nonscreen.append(dict(fr=fr, br=br, op=op, unit=[u.strip() for u in unit.split(";")], sit=[sit.strip()]))
    if header and header[0] == "Screen" and len(header) == 3 and header[1] == "Functional ID":
        out["ux_fr"] = [dict(screen=r[0], fr=r[1], uat=r[2].split(" — ")[0], status=r[2].split(" — ")[1]) for r in rows]
    if header and header[0] == "ID" and header[1] == "New interface":
        out["new_interfaces"] = [dict(id=r[0], title=r[1], purpose=r[2]) for r in rows]
out["nonscreen"] = nonscreen

def decisions(lines, src):
    res = []
    for i, l in enumerate(lines):
        m = re.match(r"<Heading2> (DEC-\d{3}) — (.*)$", l)
        if m:
            blk = lines[i+1:i+5]
            g = lambda p: next((x[len(p):].strip() for x in blk if x.startswith(p)), "")
            own = next((x for x in blk if x.startswith("Owner:")), "")
            res.append(dict(id=m.group(1), subject=m.group(2).strip(), source_doc=src,
                            source_requirement=g("Source requirement:"), proposed=g("Proposed resolution:"),
                            evidence=g("Review evidence:"), owner=own))
    return res
decs = decisions(read("07"), "07") + decisions(read("08"), "08") + decisions(L24, "24")
out["decisions"] = decs

# ---------------- Doc 20: backlog ----------------
L20 = read("20")
tasks, uxtasks, modules, runbook, workpk, capacity, dod, costs, effort = [], [], [], [], [], [], [], [], []
for start, h1, h2, header, rows in tables(L20):
    hdr = "|".join(header)
    if hdr.startswith("Task / work item"):
        for r in rows:
            m = re.match(r"^(TASK-[A-Z]+\d+)(.*)$", r[0])
            pd = [float(x) for x in r[2].split(" / ")]
            tasks.append(dict(id=m.group(1), title=m.group(2).strip(), pred=[p.strip() for p in r[1].split(";")],
                              low=pd[0], base=pd[1], high=pd[2], owner=r[3] if len(r) > 3 else ""))
    elif hdr.startswith("Task|Work item"):
        for r in rows:
            pd = [float(x) for x in r[3].split("/")]
            uxtasks.append(dict(id=r[0], title=r[1], pred=[p.strip() for p in r[2].split(";")], low=pd[0], base=pd[1], high=pd[2]))
    elif hdr.startswith("Sequence|Module"):
        for r in rows:
            dep, _, acc = r[2].partition(" | ")
            modules.append(dict(seq=int(r[0]), module=r[1], dependency=dep, acceptance=acc))
    elif hdr.startswith("Routine / incident"):
        runbook = [dict(routine=r[0], action=r[1]) for r in rows]
    elif hdr.startswith("Order|Work package"):
        workpk = [dict(order=r[0], package=r[1], evidence=r[2]) for r in rows]
    elif hdr.startswith("Metric|Initial target"):
        capacity = [r for r in rows]
    elif hdr.startswith("Work / decision") and h2 == "Execution backlog and definition of done":
        dod = [dict(item=r[0], acceptance=r[1], role=r[2]) for r in rows]
    elif hdr.startswith("Pilot item"):
        costs = [r for r in rows]
    elif hdr.startswith("Work package|Person-days"):
        effort = [r for r in rows]
out.update(tasks=tasks, uxtasks=uxtasks, modules=modules, runbook=runbook, work_packages=workpk,
           capacity=capacity, dod=dod, pilot_costs=costs, effort=effort)

OUT.write_text(json.dumps(out, indent=1, ensure_ascii=False))
print({k: (len(v) if hasattr(v, "__len__") else v) for k, v in out.items()})
