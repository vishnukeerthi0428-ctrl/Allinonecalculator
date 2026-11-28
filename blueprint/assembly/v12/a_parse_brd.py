#!/usr/bin/env python3
"""R1 / Group A: parse BRD V12 business chapters (00, 01-07, 10-25, AP) into atomic aspects.

Usage: python3 -I a_parse_brd.py <BRD_dir> <out_json>
Excludes 08, 09 (other groups) and ZZ_Historical_annex (R11).
Every table row (except header rows), every paragraph line and every
<Heading3>/OPT requirement block becomes one aspect. Exact repeats are
listed once (repeat count kept).
"""
import json, os, re, sys

SRC, OUT = sys.argv[1], sys.argv[2]
SKIP = ("08_", "09_", "ZZ_")
OPT_RE = re.compile(r"^([A-Z]{2,3}-\d{2}) · (P\d) · (.+)$")
ID_RE = re.compile(r"^(BR-[A-Z0-9-]+|MT-\d+|MOB-\d+|REC-\d+|CJ-[A-Z]+-\d+|KPI-\d+|DEC-[A-Z0-9-]+|ENT-[A-Z]+-\d+|"
                   r"SM-SVC-\d+(?:-ENT-AT01)?|GO-\d+|XS-\d+|E-\d+|P-\d+|V8-QA-\d+|C\d|D\d+|M1|CJ|AI|A11Y|EVD|"
                   r"P\d|R\d|W\d+|L\d|AT-\d+|RT-\d+|CV-\d+|CS-\d+|SEC-\d+|ST-\d+|FL-\d+|GC-\d+|AI-\d+)\b")

def chapter_of(fn):
    return fn.split("_")[0]

aspects, seen = [], {}

def add(ch, h2, h3, kind, key, text, header=None):
    text = re.sub(r"\s+", " ", text).strip()
    if not text:
        return
    norm = re.sub(r"V\d+(\.\d)?", "V", text.lower())
    sig = (kind, norm[:400])
    if sig in seen:
        aspects[seen[sig]]["repeats"] += 1
        return
    seen[sig] = len(aspects)
    aspects.append(dict(chapter=ch, section=(h2 or h3 or "").strip(), sub=(h3 or "").strip(),
                        kind=kind, key=key, text=text, header=header, repeats=0))

for fn in sorted(os.listdir(SRC)):
    if fn.startswith(SKIP) or not fn.endswith(".txt"):
        continue
    ch = chapter_of(fn)
    lines = open(os.path.join(SRC, fn), encoding="utf-8").read().split("\n")
    h2 = h3 = ""
    i = 0
    in_table = False
    rows, row = [], []
    opt = None
    def flush_opt():
        global opt
        if opt:
            add(ch, h2, h3, "requirement", opt[0], " | ".join(opt[1]))
            opt = None
    while i < len(lines):
        ln = lines[i].rstrip()
        i += 1
        if ln.startswith("[TABLE]"):
            flush_opt(); in_table = True; rows, row = [], []; continue
        if ln.startswith("[/TABLE]"):
            if row: rows.append(row)
            if rows:
                header = rows[0]
                for r in rows[1:]:
                    k = r[0] if r else ""
                    tok = k.split(" ")[0]
                    add(ch, h2, h3, "table_row", tok if (ID_RE.match(k) and (re.search(r"\d", tok) or k == tok)) else k[:60],
                        " | ".join(f"{h}: {c}" for h, c in zip(header, r)) if len(header) == len(r) else " | ".join(r), header)
            in_table = False
            rest = ln[len("[/TABLE]"):].strip()
            if rest:
                add(ch, h2, h3, "paragraph", "", rest)
            continue
        if in_table:
            if ln == "---row":
                if row: rows.append(row)
                row = []
            else:
                row.append(ln)
            continue
        m = re.match(r"^<Heading(\d)> ?(.*)$", ln)
        if m:
            flush_opt()
            lvl, title = int(m.group(1)), m.group(2)
            if lvl == 1: h2 = h3 = ""; continue
            if lvl == 2: h2, h3 = title, ""; continue
            h3 = title
            mid = ID_RE.match(title)
            if mid:  # requirement block (MT-, MOB-)
                body = [title]
                while i < len(lines) and lines[i] and not lines[i].startswith(("<Heading", "[TABLE]")):
                    body.append(lines[i]); i += 1
                add(ch, h2, h3, "requirement", mid.group(1), " | ".join(body))
            continue
        if not ln.strip():
            continue
        mo = OPT_RE.match(ln)
        if mo:
            flush_opt(); opt = (mo.group(1), [ln]); continue
        if opt and ln.startswith(("Requirement:", "Acceptance", "Owner:")):
            opt[1].append(ln); continue
        flush_opt()
        add(ch, h2, h3, "paragraph", "", ln)
    flush_opt()

json.dump(aspects, open(OUT, "w"), ensure_ascii=False, indent=1)
from collections import Counter
print(len(aspects), "aspects;", sum(a["repeats"] for a in aspects), "exact repeats folded")
print(Counter(a["chapter"] for a in aspects))
print(Counter(a["kind"] for a in aspects))
