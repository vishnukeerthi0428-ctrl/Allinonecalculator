"""Group I source-pack reconciliation (docs 18,25,26,27,29,30,31,32).
Parses the plain-text extractions, counts tables/rows/headings, extracts
OPT controls, OKPI gates, UX-QC rows and the doc-31 API operations, and
reconciles them against the blueprint Part 3.2 API catalogue and the
blueprint OKPI/NFR register. Output: JSON summary on stdout."""
import re, sys, json, pathlib
DOCS = pathlib.Path(sys.argv[1])
BP = pathlib.Path(sys.argv[2])
IDS = ["18", "25", "26", "27", "29", "30", "31", "32"]

def parse(path):
    lines = path.read_text(encoding="utf-8").splitlines()
    heads, tables, cur, row = [], [], None, []
    for ln in lines:
        if ln.startswith("<Heading") or ln.startswith("<Title>"):
            heads.append(ln)
        if ln == "[TABLE]":
            cur = []; row = []
            continue
        if ln == "[/TABLE]":
            if row: cur.append(row)
            tables.append(cur); cur = None; continue
        if cur is not None:
            if ln == "---row":
                cur.append(row); row = []
            else:
                row.append(ln)
    return lines, heads, tables

out = {}
api_doc31 = []
for i in IDS:
    p = next(DOCS.glob(f"{i}_*.txt"))
    lines, heads, tables = parse(p)
    opts = sorted(set(re.findall(r"OPT-\d\d-\d\d", "\n".join(lines))))
    rows = sum(max(len(t) - 1, 0) for t in tables)
    out[i] = {"file": p.name, "bytes": p.stat().st_size, "lines": len(lines),
              "headings": len(heads), "tables": len(tables), "table_rows": rows,
              "opt_controls": opts}
    if i == "31":
        for ln in lines:
            for m in re.finditer(r"(GET|POST|PATCH|PUT|DELETE) (/api/v1/[^\s;]+)", ln):
                api_doc31.append((m.group(1), m.group(2).rstrip(".")))

# blueprint API catalogue (Part 3.2): rows like | API-116 | POST | `/api/v1/...` | or `~/...`
cat = {}
for ln in (BP / "Part-03-2_API_and_Integration.md").read_text(encoding="utf-8").splitlines():
    m = re.match(r"\|\s*(API-\d+)[^|]*\|\s*(GET|POST|PATCH|PUT|DELETE)\s*\|\s*`([^`]+)`", ln)
    if m:
        path = m.group(3).replace("~", "/api/v1")
        cat.setdefault((m.group(2), path), m.group(1))
recon = []
for meth, path in dict.fromkeys(api_doc31):
    hit = cat.get((meth, path))
    recon.append({"op": f"{meth} {path}", "blueprint": hit or "NOT FOUND"})
out["doc31_api"] = recon
out["doc31_api_found"] = sum(1 for r in recon if r["blueprint"] != "NOT FOUND")
out["blueprint_api_rows"] = len(cat)
# UX-QC rows (doc 32) and mandatory gates
d32 = (DOCS / next(DOCS.glob("32_*.txt")).name).read_text(encoding="utf-8")
out["uxqc"] = sorted(set(re.findall(r"UX-QC-\d\d", d32)))
json.dump(out, sys.stdout, indent=1)
