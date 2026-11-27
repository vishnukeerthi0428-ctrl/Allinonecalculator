"""Build Group I coverage CSV and Markdown register fragments from aspects_I.py.
Usage: python3 -I build_register_I.py <blueprint_dir>"""
import csv, sys, pathlib, collections, importlib.util
BP = pathlib.Path(sys.argv[1])
here = pathlib.Path(__file__).parent
spec = importlib.util.spec_from_file_location("aspects_I", here / "aspects_I.py")
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
NAME = {"C": "Covered", "P": "Partially covered", "N": "Not covered", "X": "Conflict", "NA": "Not applicable"}
DOCS = ["18", "25", "26", "27", "29", "30", "31", "32"]
rows, cnt = [], collections.defaultdict(int)
for doc, sec, summ, st, loc, act, new in m.A:
    key = "OPT" if sec.startswith("Optimization engineering (") else doc
    cnt[key] += 1
    aid = f"I-{key}-{cnt[key]:03d}"
    rows.append(dict(doc=doc, key=key, section=sec, aspect_id=aid, aspect_summary=summ, status=NAME[st], st=st,
                     blueprint_location=loc, action=act, new_ids=new))
out = BP / "final" / "coverage" / "I_coverage.csv"
with out.open("w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["doc", "section", "aspect_id", "aspect_summary", "status", "blueprint_location", "action", "new_ids"])
    for r in rows:
        w.writerow([r["doc"] if r["key"] != "OPT" else "OPT(" + r["doc"] + ")", r["section"], r["aspect_id"], r["aspect_summary"],
                    r["status"], r["blueprint_location"], r["action"], r["new_ids"]])
# summary
order = DOCS + ["OPT"]
summ = collections.defaultdict(collections.Counter)
for r in rows:
    summ[r["key"]][r["st"]] += 1
def esc(s): return s.replace("|", "/")
L = ["| Doc | Covered | Partially covered | Not covered | Conflict | Not applicable | Total |", "|---|---|---|---|---|---|---|"]
tot = collections.Counter()
for k in order:
    c = summ[k]; tot.update(c)
    label = {"OPT": "OPT controls (inventoried once)"}.get(k, "Doc " + k)
    L.append(f"| {label} | {c['C']} | {c['P']} | {c['N']} | {c['X']} | {c['NA']} | {sum(c.values())} |")
L.append(f"| **Total** | **{tot['C']}** | **{tot['P']}** | **{tot['N']}** | **{tot['X']}** | **{tot['NA']}** | **{sum(tot.values())}** |")
(here / "frag_summary.md").write_text("\n".join(L) + "\n", encoding="utf-8")
# detailed register
D = []
for k in order:
    sub = [r for r in rows if r["key"] == k]
    title = "Optimization controls OPT-xx-yy (inventoried once across the eight documents)" if k == "OPT" else f"Document {k}"
    D.append(f"#### 4.4.3.{order.index(k)+1} {title}\n")
    gaps = [r for r in sub if r["st"] in ("P", "N", "X")]
    if gaps:
        D.append("| Aspect | Section | Aspect summary | Status | Blueprint location | Action | New IDs |")
        D.append("|---|---|---|---|---|---|---|")
        for r in gaps:
            D.append(f"| {r['aspect_id']} | {esc(r['section'])} | {esc(r['aspect_summary'])} | **{r['status']}** | {esc(r['blueprint_location'])} | {esc(r['action'])} | {esc(r['new_ids'])} |")
        D.append("")
    ok = [r for r in sub if r["st"] in ("C", "NA")]
    if ok:
        D.append("Covered and not-applicable aspects (grouped by section):\n")
        D.append("| Section | Aspect IDs | Status | Blueprint location (representative) |")
        D.append("|---|---|---|---|")
        grp = collections.OrderedDict()
        for r in ok:
            grp.setdefault((r["section"], r["st"]), []).append(r)
        for (sec, st), rs in grp.items():
            ids = ", ".join(x["aspect_id"].split("-")[-1] for x in rs)
            locs = "; ".join(dict.fromkeys(x["blueprint_location"] for x in rs))
            if len(locs) > 160: locs = locs[:157] + "…"
            D.append(f"| {esc(sec)} | {ids} | {NAME[st]} | {esc(locs)} |")
        D.append("")
(here / "frag_register.md").write_text("\n".join(D) + "\n", encoding="utf-8")
print({k: dict(summ[k]) for k in order}, sum(tot.values()))
