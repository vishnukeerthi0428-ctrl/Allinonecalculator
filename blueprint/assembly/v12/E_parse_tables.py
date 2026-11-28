#!/usr/bin/env python3
"""Group R4 / letter E: parse every line of the assigned FSD V12 chapters.

Counts lines, bytes, headings, tables and table rows per chapter and dumps
every table row (cells joined by ' | ') so that no row is skipped when the
aspect register (E_coverage.py) is built.  Usage:
    python3 -I E_parse_tables.py <FSD dir> <out.json>
"""
import json, os, re, sys

FILES = ["00_", "01_", "02_", "03_", "04_", "05_", "06_", "07_", "08_", "09_", "10_",
         "32_", "35_", "36_", "38_", "39_"]


def parse(path):
    lines = open(path, encoding="utf-8").read().split("\n")
    out = {"lines": len(lines), "bytes": os.path.getsize(path), "headings": [], "tables": []}
    tbl, row = None, None
    for ln in lines:
        m = re.match(r"<Heading(\d)>\s*(.*)", ln)
        if m:
            out["headings"].append((int(m.group(1)), m.group(2).strip()))
            continue
        if ln.strip() == "[TABLE]":
            tbl, row = [], None
            continue
        if ln.strip() == "[/TABLE]":
            if row is not None:
                tbl.append(row)
            out["tables"].append(tbl)
            tbl, row = None, None
            continue
        if tbl is not None:
            if ln.strip() == "---row":
                if row is not None:
                    tbl.append(row)
                row = []
            elif row is not None:
                row.append(ln.strip())
    return out


def main():
    src, dst = sys.argv[1], sys.argv[2]
    res = {}
    for pre in FILES:
        for f in sorted(os.listdir(src)):
            if f.startswith(pre) and f.endswith(".txt"):
                res[f] = parse(os.path.join(src, f))
    json.dump(res, open(dst, "w"), indent=1, ensure_ascii=False)
    tot = [0, 0, 0, 0, 0]
    print("file|lines|bytes|headings|tables|data_rows")
    for f, r in res.items():
        rows = sum(max(len(t) - 1, 0) for t in r["tables"])
        vals = [r["lines"], r["bytes"], len(r["headings"]), len(r["tables"]), rows]
        tot = [a + b for a, b in zip(tot, vals)]
        print("|".join([f] + [str(v) for v in vals]))
    print("|".join(["TOTAL"] + [str(v) for v in tot]))


if __name__ == "__main__":
    main()
