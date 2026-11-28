#!/usr/bin/env python3
"""Render Part 11.1 §11.1.2 counts and §11.1.3 detailed register from A_coverage.csv.

Usage: python3 -I a_register_md.py <A_coverage.csv> <BRD_dir> <out_md_fragment>
Partially covered / Not covered / Conflict aspects are listed one per row;
Covered and Not applicable aspects are grouped per chapter.
"""
import csv, os, sys
from collections import Counter, defaultdict

rows = list(csv.DictReader(open(sys.argv[1], encoding="utf-8")))
SRC, OUT = sys.argv[2], sys.argv[3]
TITLES = {"00": "Front matter and reading guide", "AP": "Appendix: ID index"}
for fn in os.listdir(SRC):
    ch = fn.split("_")[0]
    if fn.startswith(("08_", "09_", "ZZ_")): continue
    TITLES.setdefault(ch, fn[3:-4].replace("_", " ") if ch not in ("00", "AP") else fn[:-4])

def esc(s):
    return s.replace("|", "/").replace("\n", " ")

def short(s, n):
    s = esc(s)
    return s if len(s) <= n else s[: n - 1] + "…"

by = defaultdict(list)
for r in rows: by[r["chapter"]].append(r)
out = []
# 11.1.2 per-chapter table
out.append("| Ch | Chapter | Aspects | Covered | Partial | Not covered | Conflict | N/A | **Matched** | **Pending Founder** | **N/A after** |")
out.append("|---|---|---|---|---|---|---|---|---|---|---|")
T = Counter()
for ch in sorted(by):
    b = Counter(x["status_before"].split(" (")[0] for x in by[ch])
    a = Counter(x["status_after"].split(" (")[0] for x in by[ch])
    vals = [len(by[ch]), b["Covered"], b["Partially covered"], b["Not covered"], b["Conflict"], b["Not applicable"],
            a["Matched"], a["Pending Founder decision"], a["Not applicable"]]
    for k, v in zip("n c p nc x na m pf na2".split(), vals): T[k] += v
    out.append(f"| {ch} | {short(TITLES.get(ch, ch), 48)} | " + " | ".join(str(v) for v in vals) + " |")
out.append("| **Total** | | " + " | ".join(f"**{T[k]}**" for k in "n c p nc x na m pf na2".split()) + " |")
out.append("")
out.append("<!-- REGISTER -->")
for ch in sorted(by):
    rs = by[ch]
    out.append(f"#### 11.1.3.{ch} Chapter {ch}: {TITLES.get(ch, ch)}")
    out.append("")
    cov = [r for r in rs if r["status_before"] == "Covered"]
    na = [r for r in rs if r["status_before"].startswith("Not applicable")]
    det = [r for r in rs if r["status_before"] in ("Partially covered", "Not covered", "Conflict")]
    if cov:
        locs = Counter(r["blueprint_location"] for r in cov)
        out.append(f"**Covered (grouped, {len(cov)}):** " + "; ".join(
            f"{', '.join(sorted(set(r['aspect_id'] for r in cov if r['blueprint_location']==l)))[:220]} → {esc(l)}" for l, _ in locs.most_common()) + ". All Matched.")
        out.append("")
    if na:
        reasons = Counter(r["status_before"] for r in na)
        out.append(f"**Not applicable (grouped, {len(na)}):** " + "; ".join(f"{v} × {k[16:-1]}" for k, v in reasons.items()) + ".")
        out.append("")
    if det:
        out.append("| Aspect | Summary (V12 wording, abridged) | Before | Blueprint location | Action | New IDs | After |")
        out.append("|---|---|---|---|---|---|---|")
        for r in det:
            out.append(f"| {esc(r['aspect_id'])} | {short(r['aspect_summary'], 150)} | {r['status_before']} | {short(r['blueprint_location'], 70)} | {short(r['action'], 90)} | {esc(r['new_ids'])} | {r['status_after']} |")
        out.append("")
open(OUT, "w", encoding="utf-8").write("\n".join(out) + "\n")
print("wrote", OUT, sum(1 for r in rows if r["status_before"] in ("Partially covered", "Not covered", "Conflict")), "detailed rows")
