"""Group J (training / SaaS / maintenance / optimization) - data extraction.

Reads the source pack documents 33-36 and 38 (plain-text extractions) and the
blueprint (Part 2.1 FR register, Part 2.3 RBAC matrix, Part 2.5 screen
inventory, final/RTM.csv) and writes one JSON with every row parsed, so that the
document generator (J_build_docs.py) and the coverage CSV never skip a row.

Usage:
  python3 -I J_build_data.py <docs38_dir> <blueprint_dir> <out_json>
"""
import csv, glob, json, re, sys

DOCS, BP, OUT = sys.argv[1], sys.argv[2], sys.argv[3]


def doc(n):
    p = glob.glob(f"{DOCS}/{n:02d}_*.txt")[0]
    return p, open(p, encoding="utf-8").read().split("\n")


def tables(lines):
    """Return list of (start_line, header, rows) for [TABLE] blocks (one cell per line)."""
    out, i = [], 0
    while i < len(lines):
        if lines[i] == "[TABLE]":
            j = i + 1
            block = []
            while lines[j] != "[/TABLE]":
                block.append(lines[j]); j += 1
            groups, cur = [], []
            for c in block:
                if c == "---row":
                    groups.append(cur); cur = []
                else:
                    cur.append(c)
            if cur:
                groups.append(cur)
            out.append((i + 1, groups[0], groups[1:]))
            i = j
        i += 1
    return out


data = {}

# ---------------------------------------------------------------- doc 33
p, L = doc(33)
nav = []
for i, l in enumerate(L):
    m = re.match(r"<Heading2> ([WA]\d{2,3})\s+(.*)", l)
    if m and l.find("Heading2") >= 0 and i < 448:
        am = re.match(r"Access: ([^.]+)\. (.*)", L[i + 1])
        nav.append(dict(id=m.group(1), title=m.group(2).strip(), access=am.group(1), purpose=am.group(2), steps=L[i + 2]))
prac = []
for (ln, hdr, rows) in tables(L):
    if hdr[:1] == ["Screen / trainee"]:
        for r in rows:
            m = re.match(r"([WA]\d{2,3}) (.*)", r[0])
            rest = m.group(2)
            title, trainee = rest, ""
            for n in range(len(rest) - 1, 0, -1):
                if rest[n].isupper() and (rest[n - 1].islower() or rest[n - 1] == ")"):
                    title, trainee = rest[:n], rest[n:]
                    break
            prac.append(dict(id=m.group(1), title=title, trainee=trainee, procedure=r[1], success=r[2], uat=r[3]))
journeys = []
for i, l in enumerate(L):
    if l.startswith("<Heading2>") and 13 <= i <= 31:
        journeys.append(dict(name=l.replace("<Heading2> ", ""), steps=L[i + 1], practice=L[i + 2]))
recovery = []
for i, l in enumerate(L[448:462]):
    if l.startswith("<Heading2>"):
        recovery.append(dict(name=l.replace("<Heading2> ", ""), action=L[448 + i + 1], evidence=L[448 + i + 2]))
exer = [r for (ln, h, rows) in tables(L) if h[:1] == ["Scenario"] for r in rows]
optrain = [r for (ln, h, rows) in tables(L) if h[:1] == ["Control / scenario"] for r in rows]
data["d33"] = dict(path=p, lines=len(L), bytes=len("\n".join(L).encode()), nav=nav, practice=prac,
                   journeys=journeys, recovery=recovery, exercises=exer, operating_training=optrain)

# ---------------------------------------------------------------- doc 36
p, L = doc(36)
dims = [dict(name=r[0], weight=int(r[1]), owner=r[2]) for (ln, h, rows) in tables(L) if h[:1] == ["Dimension"] for r in rows]
controls, cur_dim = [], None
for i, l in enumerate(L):
    if l.startswith("<Heading1> 4."):
        break
    if l.startswith("<Heading2>"):
        cur_dim = l.replace("<Heading2> ", "")
    m = re.match(r"(OPT-(\d\d)-(\d\d)) • (.*?) — (.*)", l)
    if m:
        acc = L[i + 1]
        am = re.match(r"Acceptance / evidence: (.*) \| Accountable: (.*)\.", acc)
        controls.append(dict(id=m.group(1), dim_no=int(m.group(2)), dim=cur_dim, name=m.group(4), control=m.group(5),
                             acceptance=am.group(1), owner=am.group(2)))
kpis = []
for (ln, h, rows) in tables(L):
    if h[:1] == ["KPI / metric"]:
        for r in rows:
            m = re.match(r"KPI-(\d\d) (.*)", r[0])
            kpis.append(dict(n=int(m.group(1)), metric=m.group(2), target=r[1], context=r[2]))
scen = []
for l in L:
    m = re.match(r"OPT-TEST-(\d\d) — ([^:]+): (.*?) Expected: (.*?) Status: (.*)\.$", l)
    if m:
        scen.append(dict(n=int(m.group(1)), dim=m.group(2), test=m.group(3), expected=m.group(4), status=m.group(5)))
bench = [r for (ln, h, rows) in tables(L) if h[:1] == ["Candidate"] for r in rows]
uxqc = [r for (ln, h, rows) in tables(L) if h[:1] == ["Control"] for r in rows]
procs = []
sec = None
for i, l in enumerate(L):
    if l.startswith("<Heading1> Implementation acceptance and verification"):
        sec = "v"
    elif l.startswith("<Heading1>") and sec == "v":
        sec = None
    if sec == "v" and l.startswith("<Heading2>"):
        procs.append(dict(name=l.replace("<Heading2> ", ""), body=" ".join(L[i + 1:i + 4])))
panel = [l for l in L if " | GET " in l or " | POST " in l]
data["d36"] = dict(path=p, lines=len(L), bytes=len("\n".join(L).encode()), dims=dims, controls=controls, kpis=kpis,
                   scenarios=scen, bench=bench, uxqc=uxqc, procedures=procs, panel=panel)

# ---------------------------------------------------------------- doc 38
p, L = doc(38)
d38 = []
for (ln, h, rows) in tables(L):
    # nearest preceding heading
    k = ln - 1
    while k > 0 and not L[k].startswith("<Heading"):
        k -= 1
    d38.append(dict(line=ln, heading=L[k].split("> ", 1)[-1], header=h, rows=rows))
mand = {}
for t in d38:
    if t["header"][:1] == ["ID"] and t["header"][-1] == "Mandatory":
        for r in t["rows"]:
            mand[int(r[0][4:])] = dict(metric=r[1], target=r[2], mandatory=r[3])
data["d38"] = dict(path=p, lines=len(L), bytes=len("\n".join(L).encode()), tables=d38, kpi_mandatory=mand)

# ---------------------------------------------------------------- docs 34, 35 (headings + tables)
for n in (34, 35):
    p, L = doc(n)
    hs = [(i, l) for i, l in enumerate(L) if l.startswith("<Heading")]
    data[f"d{n}"] = dict(path=p, lines=len(L), bytes=len("\n".join(L).encode()),
                         headings=[l for i, l in hs], tables=[dict(line=ln, header=h, rows=r) for (ln, h, r) in tables(L)])

# ---------------------------------------------------------------- blueprint
fr = {}
for l in open(f"{BP}/Part-02-1_Functional_Design_Modules_and_FR_Register.md", encoding="utf-8"):
    m = re.match(r"\| (FR-[WA]\d{2,3}) \| ([^|]*) \| ([^|]*) \| ([^|]*) \|", l)
    if m:
        cells = [c.strip() for c in l.strip().strip("|").split("|")]
        fr[m.group(1)] = dict(title=cells[1], surface=cells[2], requirement=cells[3], fields=cells[4],
                              automation=cells[5], wave_epic=cells[-1])
scr, group = {}, None
for l in open(f"{BP}/Part-02-5_UX_UI_Design.md", encoding="utf-8"):
    if l.startswith("### 2.43."):
        group = re.sub(r"^### 2\.43\.\d+ ", "", l.strip())
    m = re.match(r"\| ([WA]\d{2,3}) \| ", l)
    if m and group:
        cells = [c.strip() for c in l.strip().strip("|").split("|")]
        scr[m.group(1)] = dict(title=cells[1], pattern=cells[2], regions=cells[3], actions=cells[4], notes=cells[5] if len(cells) > 5 else "", group=group)
# RBAC
rb = {}
roles = None
txt = open(f"{BP}/Part-02-3_Business_Rules_RBAC_State_Machines.md", encoding="utf-8").read().split("\n")
on = False
for l in txt:
    if l.startswith("### 2.26.3"):
        on = True
    elif l.startswith("### 2.26.4"):
        break
    if on and l.startswith("| Screen group | Screens | R01"):
        roles = [c.strip() for c in l.strip().strip("|").split("|")][2:]
        continue
    if on and roles and l.startswith("| ") and not l.startswith("|---") and not l.startswith("| Screen group"):
        cells = [c.strip() for c in l.strip().strip("|").split("|")]
        if len(cells) == len(roles) + 2:
            ids = []
            for part in cells[1].split(","):
                part = part.strip()
                m = re.match(r"A(\d{3})–A(\d{3})", part)
                if m:
                    ids += [f"A{k:03d}" for k in range(int(m.group(1)), int(m.group(2)) + 1)]
                elif re.match(r"A\d{3}$", part):
                    ids.append(part)
            for sid in ids:
                rb.setdefault(sid, {})
                for role, perm in zip(roles, cells[2:]):
                    if perm and perm != "—":
                        prev = rb[sid].get(role)
                        rb[sid][role] = perm if not prev else prev + "; " + perm
rtm = {}
for r in csv.DictReader(open(f"{BP}/final/RTM.csv", encoding="utf-8")):
    if r["requirement_type"] in ("FR", "NFR", "US"):
        rtm[r["requirement_id"]] = dict(title=r["title"], epic=r["epic"], wave=r["wave"], us=r["linked_us"],
                                        aliases=r["aliases"], tc_count=r["tc_count"], tc_ids=r["tc_ids"], flag=r["coverage_flag"])
data["bp"] = dict(fr=fr, screens=scr, rbac=rb, rtm=rtm)

# referenced OPT ids and SM-UAT ids in blueprint
bp_text = "\n".join(open(f, encoding="utf-8").read() for f in sorted(glob.glob(f"{BP}/Part-0*.md")) if "Source_Pack" not in f)
data["bp"]["opt_refs"] = sorted(set(re.findall(r"OPT-\d\d-\d\d", bp_text)))
data["bp"]["smuat_refs"] = sorted(set(re.findall(r"SM-UAT-S\d{3}", bp_text)))
json.dump(data, open(OUT, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print("nav", len(nav), "practice", len(prac), "journeys", len(journeys), "recovery", len(recovery), "exercises", len(exer), "optrain", len(optrain))
print("dims", len(dims), sum(d["weight"] for d in dims), "controls", len(controls), "kpis", len(kpis), "scenarios", len(scen), "bench", len(bench), "uxqc", len(uxqc), "procs", len(procs), "panel", len(panel))
print("d38 tables", len(d38), "mandatory", sum(1 for v in mand.values() if v["mandatory"] == "Yes"))
print("bp fr", len(fr), "screens", len(scr), "rbac screens", len(rb), "rtm", len(rtm), "opt refs", len(data["bp"]["opt_refs"]), "smuat", len(data["bp"]["smuat_refs"]))
