#!/usr/bin/env python3
"""Index the blueprint artefacts that group H reconciles against.
Usage: python3 -I H_blueprint_index.py <blueprint_dir> <out_json>
"""
import json, re, sys
from pathlib import Path

B = Path(sys.argv[1]); OUT = Path(sys.argv[2])
txt = lambda pat: "\n".join(p.read_text(encoding="utf-8") for p in sorted(B.glob(pat)))

def cells(line):
    return [c.strip() for c in line.strip().strip("|").split("|")]

idx = {}
# ---- Part 1 BR register
p1 = txt("Part-01_*.md")
brs = {}
for l in p1.splitlines():
    m = re.match(r"^\| (BR-(?:M\d\d|TENANT|WEB|AUTO|SVC|QA)) \|", l)
    if m:
        c = cells(l)
        brs[m.group(1)] = dict(id=c[0], name=c[1], need=c[2], acceptance=c[3], dependency=c[4], personas=c[5],
                               moscow=c[6], wave=c[7], epic=c[8] if len(c) > 8 else "")
    m = re.match(r"^\| (BR-S\d{3}) \|", l)
    if m:
        c = cells(l); brs[m.group(1)] = dict(id=c[0], name=c[1], source=c[2], traces=c[3] if len(c) > 3 else "")
idx["br"] = brs
# ---- Part 2.1 FR register
p21 = txt("Part-02-1_*.md")
frs = {}
for l in p21.splitlines():
    m = re.match(r"^\| (FR-(?:W\d\d|A\d{3}|OP\d{3})) \|", l)
    if m:
        c = cells(l)
        frs[m.group(1)] = dict(id=c[0], title=c[1], traces=c[-2], wave_epic=c[-1], raw=l)
    m = re.match(r"^\| (FR-[A-Z]+-[0-9A-Z]+) \|", l)
    if m and m.group(1) not in frs:
        c = cells(l); frs[m.group(1)] = dict(id=c[0], title=c[1], traces=c[-1], wave_epic="", raw=l)
# OP rows: traces column is second-to-last, wave last
idx["fr"] = frs
# ---- Part 5 stories
stories = {}
for p in sorted(B.glob("Part-05-*.md")):
    t = p.read_text(encoding="utf-8")
    for m in re.finditer(r"^#{4,5} (US-\d{4}) (.*)$", t, re.M):
        sid = m.group(1)
        blk = t[m.end(): m.end() + 6000]
        def f(name):
            mm = re.search(r"^\| " + name + r" \| (.*?) \|$", blk, re.M)
            return mm.group(1).strip() if mm else ""
        pwp = f("Priority · Wave · Points").split(" · ")
        stories[sid] = dict(id=sid, title=m.group(2).strip(), type=f("Type"), traces=f("Traces") or f("Linked"),
                            priority=f("Priority") or (pwp[0] if pwp else ""), wave=f("Wave") or (pwp[1] if len(pwp) > 1 else ""),
                            points=f("Points") or (pwp[-1] if len(pwp) > 2 else ""), deps=f("Dependencies"), part=p.name)
idx["stories"] = stories
# ---- Part 6.6 FR -> stories
p66 = txt("Part-06-6_*.md")
fr_st = {}
for l in p66.splitlines():
    m = re.match(r"^\| (FR-(?:W\d\d|A\d{3}|OP\d{3})) \|", l)
    if m:
        c = cells(l)
        fr_st[m.group(1)] = dict(aliases=c[3], stories=re.findall(r"US-\d{4}", c[4]), tc_explicit=c[5], tc_total=c[6], status=c[-1])
idx["fr_stories"] = fr_st
# ---- Part 8.1 sprint allocation
p81 = txt("Part-08-1_*.md")
sprint = {}
for l in p81.splitlines():
    m = re.match(r"^\| (S\d{1,2}) \| ", l)
    if m:
        c = cells(l)
        for s in re.findall(r"\b\d{4}\b", c[-1]):
            sprint["US-" + s] = m.group(1)
idx["story_sprint"] = sprint
# ---- runbooks
p43 = txt("Part-04-3_*.md")
idx["runbooks"] = {m.group(1): m.group(2) for m in re.finditer(r"^### (RB-\d{3}) (.*)$", p43, re.M)}
# ---- decisions
dec = {}
for pat in ("Part-00A_*.md", "Part-09-1_*.md"):
    for l in txt(pat).splitlines():
        m = re.match(r"^\| (DEC-\d{3}) \|", l)
        if m and m.group(1) not in dec:
            c = cells(l); dec[m.group(1)] = " | ".join(c[1:4])[:300]
idx["decisions"] = dec
# ---- go-live checklist, DoD, AP
p82 = txt("Part-08-2_*.md")
idx["golive"] = {m.group(1): m.group(2)[:160] for m in re.finditer(r"^\| ((?:GL-[A-Z]\d\d)|(?:BLK-\d+)) \| (.*)$", p82, re.M)}
p51 = txt("Part-05-1a_*.md")
idx["dod"] = {m.group(1): m.group(2)[:160] for m in re.finditer(r"^\| (D-\d+|R-\d+) \| (.*)$", p51, re.M)}
# ---- all IDs present anywhere (existence checks)
allt = txt("Part-*.md")
idx["id_exists"] = sorted(set(re.findall(r"\b(?:NFR-\d{3}|BRL-[A-Z]+-\d\d|RB-\d{3}|GL-[A-Z]\d\d|BLK-\d+|AP-\d\d|TC-[A-Z0-9]+-[0-9A-Z-]+|ADR-\d{3}|RSK-\d{3}|LT-\d\d|DR-\d|EVR|CFG-\d\d|RP-\d\d|NT-\d{3})\b", allt)))
OUT.write_text(json.dumps(idx, indent=1, ensure_ascii=False))
print({k: len(v) for k, v in idx.items()})
