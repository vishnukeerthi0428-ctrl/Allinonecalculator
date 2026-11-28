#!/usr/bin/env python3
"""Traceability for v1.1 additions (Parts 9.6a/b alignment and 9.7-9.9 advanced capabilities).

Writes final/RTM_advanced.csv (one row per item) and prints coverage counts.
Links are taken from table rows and story blocks that mention both IDs.
Usage: python3 blueprint/assembly/build_rtm_adv.py
"""
import collections
import csv
import re
from pathlib import Path

BP = Path(__file__).resolve().parent.parent
FILES = sorted(BP.glob("Part-09-[6789]*_*.md"))
FR, US, TC = r"FR-ADV-X\d-\d{3}", r"US-\d{2}-V\d\d{2}", r"TC-ADV-X\d-\d{3}"
AG, AU, WF = r"AG-0(?:39|[4-7]\d|80)\b", r"AU-(?:0(?:5[3-9]|[6-9]\d)|1[01]\d)\b", r"WF-(?:1[5-9]|[23]\d|40)\b"
DEC, ALN = r"DEC-(?:2(?:3[4-9]|[4-9]\d)|3\d\d|40\d)\b", r"TC-ALN-[AB]-\d{3}"


def main():
    link = collections.defaultdict(set)
    where = {}
    for f in FILES:
        tx = f.read_text(encoding="utf-8")
        label = re.match(r"Part-(\d+)-(\d+[a-z]?)_", f.name)
        label = f"{int(label.group(1))}.{label.group(2)}"
        blocks = tx.splitlines()
        heads = list(re.finditer(rf"^#{{3,6}} .*?({US}|{AG}|WF-\d\d)", tx, re.M))
        for i, m in enumerate(heads):
            seg = tx[m.end(): heads[i + 1].start() if i + 1 < len(heads) else min(len(tx), m.end() + 6000)]
            blocks.append(m.group(1) + " " + seg.replace("\n", " "))
        for ln in blocks:
            ids = set()
            for p in (FR, US, TC, AG, AU, WF, DEC, ALN):
                ids |= set(re.findall(p, ln))
            for a in ids:
                where.setdefault(a, label)
                link[a] |= ids - {a}
    fam = lambda pat: sorted(x for x in where if re.fullmatch(pat, x))
    tests = lambda x: {t for t in link[x] if re.fullmatch(TC, t) or re.fullmatch(ALN, t)}
    rows, stats = [], {}
    def add(kind, items, ok):
        n = 0
        for x in items:
            via = tests(x) or {t for y in link[x] if re.fullmatch(FR, y) or re.fullmatch(US, y) for t in tests(y)}
            good = ok(x, via)
            n += good
            rows.append([kind, x, where[x], "; ".join(sorted(y for y in link[x] if re.fullmatch(FR, y)))[:200],
                         "; ".join(sorted(y for y in link[x] if re.fullmatch(US, y)))[:200],
                         "; ".join(sorted(via))[:300], "Traced" if good else "Open"])
        stats[kind] = (n, len(items))
    add("FR-ADV", fam(FR), lambda x, v: bool(v))
    add("Story", fam(US), lambda x, v: bool(v))
    add("Agent", fam(AG), lambda x, v: bool(v) or bool(link[x] & set(fam(FR))))
    add("Automation", fam(AU), lambda x, v: bool(v) or bool(link[x] & set(fam(FR))))
    add("Workflow", fam(WF), lambda x, v: bool(v) or bool(link[x] & (set(fam(FR)) | set(fam(AG)) | set(fam(AU)))))
    alltext = "\n".join(f.read_text(encoding="utf-8") for f in FILES)
    defined = set(re.findall(rf"^\|\s*\**({DEC})", alltext, re.M))
    add("Decision (9.6-9.9)", sorted(d for d in fam(DEC) if d in defined), lambda x, v: True)
    out = BP / "final" / "RTM_advanced.csv"
    with out.open("w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["Kind", "ID", "Part", "Linked FR-ADV", "Linked stories", "Tests (direct or via FR/story)", "Status"])
        w.writerows(rows)
    for k, (n, t) in stats.items():
        print(f"{k}: {n}/{t} ({n / t * 100 if t else 100:.0f}%)")
    print(out, len(rows))


if __name__ == "__main__":
    main()
