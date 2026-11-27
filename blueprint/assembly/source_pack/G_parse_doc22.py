#!/usr/bin/env python3
"""Group G: parse every test record of source document 22 (Unit, SIT and UAT Test Case Specification).

Usage: python3 -I G_parse_doc22.py <path to 22_Unit_SIT_and_UAT_Test_Case_Specification.txt> <out.json>

Record fields: id, level (Unit/SIT/UAT), family, group, title, link (FR / screen / module / method+path),
pre (preconditions / setup), steps, expected, negative, boundary, data (fixture), variant (negative variant
from the 'Implementation, verification and delivery controls' tables).
Counts are asserted against document 38 (799 = Unit 75 + SIT 422 + UAT 302).
"""
import json
import re
import sys
from collections import Counter, OrderedDict

src, out = sys.argv[1], sys.argv[2]
lines = open(src, encoding="utf-8").read().split("\n")


def tables(start, stop):
    """Yield (header, [rows]) for each [TABLE] between line indexes start..stop; a row is a list of cell lines."""
    i = start
    while i < stop:
        if lines[i].strip() == "[TABLE]":
            j = i + 1
            cur, rows, header = [], [], None
            while lines[j].strip() != "[/TABLE]":
                if lines[j].strip() == "---row":
                    if header is None:
                        header = cur
                    else:
                        rows.append(cur)
                    cur = []
                else:
                    cur.append(lines[j])
                j += 1
            if cur:
                rows.append(cur)
            yield i, header, rows
            i = j
        i += 1


def find(pat, start=0):
    for k in range(start, len(lines)):
        if re.match(pat, lines[k]):
            return k
    raise SystemExit("heading not found: " + pat)


recs = OrderedDict()


def add(r):
    if r["id"] in recs:
        raise SystemExit("duplicate " + r["id"])
    base = dict(id="", level="", family="", group="", title="", link="", pre="", steps="", expected="",
                negative="", boundary="", data="", variant="", src_section="")
    base.update(r)
    recs[r["id"]] = base


# ---------------------------------------------------------------- §4 unit catalogue
s4, s5 = find(r"<Heading1> 4\. Unit"), find(r"<Heading1> 5\. System")
group = ""
for k in range(s4, s5):
    m = re.match(r"<Heading2> (.*)", lines[k])
    if m:
        group = m.group(1).strip()
    if lines[k].strip() == "[TABLE]":
        for _, hdr, rows in tables(k, k + 2000):
            for row in rows:
                m = re.match(r"(SM-UT-\d{3})(.*)", row[0])
                add(dict(id=m.group(1), level="Unit", family="UT", group=group, title=m.group(2).strip(),
                         steps=row[1], expected=" ".join(row[2:]), src_section="§4 " + group))
            break

# ---------------------------------------------------------------- §5 SIT end-to-end
s6 = find(r"<Heading1> 6\. Commercial")
cur = None
for k in range(s5, s6):
    m = re.match(r"<Heading2> (SM-SIT-F\d{3}) — (.*)", lines[k])
    if m:
        cur = dict(id=m.group(1), level="SIT", family="SIT-F", group="End-to-end", title=m.group(2).strip(),
                   src_section="§5")
        add(cur)
        continue
    for key, fld in (("Preconditions:", "pre"), ("Steps:", "steps"), ("Expected:", "expected")):
        if cur and lines[k].startswith(key):
            recs[cur["id"]][fld] = lines[k][len(key):].strip()

# ---------------------------------------------------------------- §6 module acceptance
s7 = find(r"<Heading1> 7\. SIT operation")
for _, hdr, rows in tables(s6, s7):
    for row in rows:
        m = re.match(r"(SM-SIT-M\d{3})(.*)", row[0])
        purpose_setup = row[1]
        add(dict(id=m.group(1), level="SIT", family="SIT-M", group="Module acceptance", title=m.group(2).strip(),
                 link="M" + m.group(1)[-2:], pre=purpose_setup, expected=" ".join(row[2:]), src_section="§6"))

# ---------------------------------------------------------------- §7 operation contracts
s8 = find(r"<Heading1> 8\. User Acceptance")
grp = ""
ops_by_group = Counter()
for k in range(s7, s8):
    m = re.match(r"<Heading2> (.*?) — (\d+) operations", lines[k])
    if m:
        grp = m.group(1)
        declared = int(m.group(2))
        cnt = 0
        for _, hdr, rows in tables(k, s8):
            for row in rows:
                m2 = re.match(r"(SM-SIT-A\d{3})(GET|POST|PUT|PATCH|DELETE|ADAPTER|INTERNAL|WORKER|CALLBACK)?\s*(.*)", row[0])
                if not m2:
                    m2 = re.match(r"(SM-SIT-A\d{3})(\S*)\s*(.*)", row[0])
                meth, path = (m2.group(2) or ""), m2.group(3).strip()
                setup = row[1]
                exp = row[2] if len(row) > 2 else ""
                srcres = " ".join(row[3:])
                purpose = setup.split("|", 1)[1].split(". Source request")[0].strip() if "|" in setup else ""
                insp = re.search(r"Inspect (.*?)\. Not run", exp)
                add(dict(id=m2.group(1), level="SIT", family="SIT-A", group=grp, title=purpose,
                         link=(meth + " " + path).strip(), pre=setup, expected=exp + " " + srcres,
                         data=insp.group(1) if insp else "", src_section="§7 " + grp))
                cnt += 1
            break
        ops_by_group[grp] = (declared, cnt)

# ---------------------------------------------------------------- §8 UAT journeys
s9 = find(r"<Heading1> 9\. UAT screen")
cur = None
for k in range(s8, s9):
    m = re.match(r"<Heading2> (SM-UAT-F\d{3}) — (.*)", lines[k])
    if m:
        cur = m.group(1)
        add(dict(id=cur, level="UAT", family="UAT-F", group="Business journey", title=m.group(2).strip(),
                 src_section="§8"))
        continue
    for key, fld in (("Acceptance user:", "pre"), ("User steps:", "steps"), ("Business acceptance:", "expected")):
        if cur and lines[k].startswith(key):
            recs[cur][fld] = lines[k][len(key):].strip()

# ---------------------------------------------------------------- §9 UAT screens
s10 = find(r"<Heading1> 10\. Defect")
for _, hdr, rows in tables(s9, s10):
    for row in rows:
        m = re.match(r"(SM-UAT-S\d{3})([WA]\d{2,3}) — (.*)", row[0])
        title = m.group(3)
        aud = re.search(r"(Public|Existing|Workspace|Admin|Portal|Restricted|External|Owner|Client)$", title)
        add(dict(id=m.group(1), level="UAT", family="UAT-S", group="Screen acceptance",
                 title=title[: aud.start()] if aud else title, link=m.group(2),
                 pre="Audience: " + (aud.group(1) if aud else ""), steps=row[1], expected=" ".join(row[2:]),
                 src_section="§9"))

# ---------------------------------------------------------------- variant tables (Implementation controls)
sImpl = find(r"<Heading1> Implementation, verification and delivery controls")
sFix = find(r"<Heading1> Concrete high-risk")
nvar = Counter()
for _, hdr, rows in tables(sImpl, sFix):
    for row in rows:
        m = re.match(r"(SM-(?:SIT-A|UAT-F|UAT-S)\d{3})", row[0])
        if m and m.group(1) in recs:
            recs[m.group(1)]["variant"] = " ".join(row[1:])
            nvar[m.group(1)[:8]] += 1

# ---------------------------------------------------------------- current-scope SM-UX cases
sCur = find(r"<Heading1> Current multi-startup")
for k in range(sCur, len(lines)):
    m = re.match(r"<Heading3> (SM-UX-(UAT|UNIT|SIT)-([WAX]\d{2,3})) — (.*)", lines[k])
    if not m:
        continue
    body = lines[k + 1]
    parts = [p.strip() for p in body.split("|")]
    d = dict(id=m.group(1), level={"UAT": "UAT", "UNIT": "Unit", "SIT": "SIT"}[m.group(2)],
             family="UX-" + m.group(2), group="Current scope (UX)", title=m.group(4).strip(), link=m.group(3),
             data=parts[0], src_section="Current scope")
    for p in parts[1:]:
        for key, fld in (("Execute:", "steps"), ("Expected:", "expected"), ("Negative:", "negative"),
                         ("Boundary:", "boundary")):
            if p.startswith(key):
                d[fld] = p[len(key):].strip()
    add(d)

# ---------------------------------------------------------------- core fixtures (not test records; kept for reference)
fixtures = []
for _, hdr, rows in tables(sFix, sFix + 60):
    for row in rows:
        fixtures.append(dict(id=row[0], scenario=row[1], inputs=row[2], expected=row[3]))
    break

lv = Counter(r["level"] for r in recs.values())
fam = Counter(r["family"] for r in recs.values())
print("records", len(recs), dict(lv))
print("families", dict(fam))
print("operation groups (declared, parsed)", dict(ops_by_group))
print("variants attached", dict(nvar))
assert len(recs) == 799 and lv == Counter(Unit=75, SIT=422, UAT=302), "count mismatch with document 38"
for g, (d, c) in ops_by_group.items():
    assert d == c, g
json.dump(dict(records=list(recs.values()), fixtures=fixtures), open(out, "w"), indent=1, ensure_ascii=False)
