#!/usr/bin/env python3
"""Assemble Part 6.9a/6.9b from templates and generated fragments.
Usage: python3 -I H_assemble.py <frag_dir> <blueprint_dir>
"""
import csv, collections, re, sys
from pathlib import Path

FR = Path(sys.argv[1]); BP = Path(sys.argv[2]); HERE = Path(__file__).resolve().parent
rows = list(csv.DictReader(open(BP / "final/coverage/H_coverage.csv", encoding="utf-8")))
bydoc = collections.Counter(r["doc"].split("/")[0] for r in rows)
st = collections.Counter(r["status"] for r in rows)
vals = {"covered": st["Covered"], "partial": st["Partially covered"], "notcov": st["Not covered"],
        "conflict": st["Conflict"], "na": st["Not applicable"]}

def fill(text):
    text = re.sub(r"\{\{frag:(\w+)\}\}", lambda m: (FR / f"{m.group(1)}.md").read_text(encoding="utf-8").rstrip("\n"), text)
    text = re.sub(r"\{\{count:(\w+)\}\}", lambda m: f"{bydoc[m.group(1)]:,}", text)
    text = re.sub(r"\{\{(covered|partial|notcov|conflict|na)\}\}", lambda m: f"{vals[m.group(1)]:,}", text)
    assert "{{" not in text, re.findall(r"\{\{[^}]*\}\}", text)[:5]
    return text

for t, out in (("H_tmpl_a.md", "Part-06-9a_Source_Pack_QC_RTM_and_Backlog_Reconciliation.md"),
               ("H_tmpl_b.md", "Part-06-9b_Source_Pack_QC_RTM_and_Backlog_Reconciliation.md")):
    (BP / out).write_text(fill((HERE / t).read_text(encoding="utf-8")), encoding="utf-8")
    print("wrote", out)
