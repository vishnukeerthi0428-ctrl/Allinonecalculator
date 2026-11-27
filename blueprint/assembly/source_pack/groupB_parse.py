#!/usr/bin/env python3
"""Group B source-pack parser and reconciler.

Parses documents 04, 05, 09 and 10 of the 38-document source pack (plain-text
extractions with <HeadingN>, [TABLE], ---row and [/TABLE] markers, one cell per
line) and reconciles their catalogues against the blueprint parts.

Outputs (JSON) to assembly/source_pack/groupB_out/:
  sections.json        heading tree with line ranges per document
  tables.json          every table, every row, per document
  backlog66.json       doc 04 commercial module backlog vs Part 1 BR-M register
  modulecards.json     doc 05 module cards (API paths, entities) vs Part 3.2/3.3
  opt_controls.json    every OPT-xx-yy control in the four documents vs blueprint
  estimates.json       discipline, UX-TASK DAG and cost recomputation checks
  summary.json         counts used in Part 3.4
Run:  python3 -I groupB_parse.py
"""
import json
import os
import re
import sys
from collections import defaultdict, OrderedDict

SRC = "/tmp/claude-0/-home-user-Allinonecalculator/233b6551-af93-57f5-8f0b-015057ecee11/scratchpad/docs38"
BP = "/home/user/Allinonecalculator/blueprint"
OUT = os.path.join(BP, "assembly/source_pack/groupB_out")
DOCS = {
    "04": "04_Solution_Architecture_and_Delivery_Plan.txt",
    "05": "05_Workflow_Automation_and_Engagement_Playbook.txt",
    "09": "09_High_Level_Design.txt",
    "10": "10_Detailed_Level_Design.txt",
}
os.makedirs(OUT, exist_ok=True)


def read(p):
    with open(p, encoding="utf-8") as fh:
        return fh.read().split("\n")


def parse(lines):
    """Return sections [{level,title,start,end,prose[],tables[]}]."""
    sections = []
    cur = {"level": 0, "title": "(front matter)", "start": 1, "prose": [], "tables": []}
    in_table = False
    table = None
    row = []
    for i, ln in enumerate(lines, 1):
        m = re.match(r"<Heading(\d)>\s*(.*)", ln)
        if m and not in_table:
            cur["end"] = i - 1
            sections.append(cur)
            cur = {"level": int(m.group(1)), "title": m.group(2).strip(), "start": i,
                   "prose": [], "tables": []}
            continue
        if ln.strip() == "[TABLE]":
            in_table = True
            table = {"header": [], "rows": [], "line": i}
            row = []
            continue
        if ln.strip() == "[/TABLE]":
            if row:
                if not table["header"]:
                    table["header"] = row
                else:
                    table["rows"].append(row)
            cur["tables"].append(table)
            in_table = False
            continue
        if in_table:
            if ln.strip() == "---row":
                if not table["header"]:
                    table["header"] = row
                else:
                    table["rows"].append(row)
                row = []
            else:
                row.append(ln.strip())
            continue
        if ln.strip():
            cur["prose"].append(ln.strip())
    cur["end"] = len(lines)
    sections.append(cur)
    return sections


def bp_text():
    txt = {}
    for f in sorted(os.listdir(BP)):
        if f.startswith("Part-") and f.endswith(".md"):
            with open(os.path.join(BP, f), encoding="utf-8") as fh:
                txt[f] = fh.read()
    return txt


def where(bp, needle, flags=re.I):
    hits = []
    for f, t in bp.items():
        if re.search(needle, t, flags):
            hits.append(f.split("_")[0].replace("Part-", ""))
    return hits


def main():
    bp = bp_text()
    docs = {k: parse(read(os.path.join(SRC, v))) for k, v in DOCS.items()}
    raw = {k: read(os.path.join(SRC, v)) for k, v in DOCS.items()}

    # ---------- sections and tables ----------
    sec_out, tab_out = {}, {}
    for k, secs in docs.items():
        sec_out[k] = [{"level": s["level"], "title": s["title"], "start": s["start"],
                       "end": s["end"], "prose_lines": len(s["prose"]),
                       "tables": len(s["tables"]),
                       "rows": sum(len(t["rows"]) for t in s["tables"])} for s in secs]
        tab_out[k] = [{"section": s["title"], "line": t["line"], "header": t["header"],
                       "rows": t["rows"]} for s in secs for t in s["tables"]]
    json.dump(sec_out, open(os.path.join(OUT, "sections.json"), "w"), indent=1, ensure_ascii=False)
    json.dump(tab_out, open(os.path.join(OUT, "tables.json"), "w"), indent=1, ensure_ascii=False)

    # common core: lines identical with doc 04 before divergence
    core = {}
    for k in DOCS:
        n = 0
        for a, b in zip(raw["04"], raw[k]):
            n += 1
            if a != b and n > 6:
                break
        core[k] = n

    # ---------- doc 04 backlog (66 modules) vs Part 1 BR-M ----------
    p1 = bp["Part-01_Product_and_Business_Foundation.md"]
    brm = {}
    for m in re.finditer(r"^\| BR-M(\d\d) \| ([^|]+)\| ([^|]+)\| ([^|]+)\| ([^|]+)\|", p1, re.M):
        brm[int(m.group(1))] = {"name": m.group(2).strip(), "objective": m.group(3).strip(),
                                "acceptance": m.group(4).strip(), "deps": m.group(5).strip()}
    backlog = None
    for t in tab_out["04"]:
        if t["header"][:2] == ["Sequence", "Module"]:
            backlog = t
            break
    name_to_seq = {}
    rows = []
    for r in backlog["rows"]:
        seq = int(r[0])
        name_to_seq[r[1].strip().lower()] = seq
    for r in backlog["rows"]:
        seq, name = int(r[0]), r[1].strip()
        depacc = r[2]
        dep, acc = (depacc.split(" | ", 1) + [""])[:2] if " | " in depacc else (depacc, "")
        deps = []
        for d in re.split(r";\s*", dep):
            d = d.strip()
            if d.lower() in name_to_seq:
                deps.append(name_to_seq[d.lower()])
            elif d:
                deps.append(d)  # e.g. H02,H03 (pre-existing capability ids)
        byname = {v["name"].lower(): (kk, v) for kk, v in brm.items()}
        brnum, b = byname.get(name.lower(), (None, {}))
        seq_to_br = {sq: byname.get(nm, (None, None))[0] for nm, sq in name_to_seq.items()}
        bp_deps = sorted(int(x) for x in re.findall(r"M(\d\d)", b.get("deps", "")))
        pk_deps = sorted(seq_to_br[x] for x in deps if isinstance(x, int) and seq_to_br.get(x))
        acc_norm = re.sub(r"\W+", " ", acc.lower()).strip()
        bacc_norm = re.sub(r"\W+", " ", b.get("acceptance", "").lower()).strip()
        rows.append({
            "seq": seq, "br": "BR-M%02d" % brnum if brnum else None, "module": name, "pack_deps": deps, "pack_deps_br": pk_deps, "pack_acceptance": acc.strip(),
            "bp_name": b.get("name"), "bp_acceptance": b.get("acceptance"), "bp_deps": bp_deps,
            "name_match": brnum is not None,
            "acceptance_match": acc_norm == bacc_norm,
            "deps_match": pk_deps == bp_deps,
        })
    # DAG checks over pack dependencies
    graph = {r["seq"]: [d for d in r["pack_deps"] if isinstance(d, int)] for r in rows}
    color, cyc = {}, []

    def dfs(u, stack):
        color[u] = 1
        for v in graph.get(u, []):
            if color.get(v) == 1:
                cyc.append(stack + [v])
            elif not color.get(v):
                dfs(v, stack + [v])
        color[u] = 2
    for u in graph:
        if not color.get(u):
            dfs(u, [u])
    level = {}

    def lvl(u):
        if u in level:
            return level[u]
        level[u] = 1 + max([lvl(v) for v in graph[u]] or [0])
        return level[u]
    for u in graph:
        lvl(u)
    # longest chain
    best = {}

    def chain(u):
        if u in best:
            return best[u]
        c = max([chain(v) for v in graph[u]] or [[]], key=len)
        best[u] = c + [u]
        return best[u]
    longest = max((chain(u) for u in graph), key=len)
    forward = [(r["seq"], d) for r in rows for d in r["pack_deps"] if isinstance(d, int) and d >= r["seq"]]
    json.dump({"rows": rows, "cycles": cyc, "levels": level, "longest_chain": longest,
               "forward_refs": forward,
               "counts": {"rows": len(rows),
                          "name_match": sum(r["name_match"] for r in rows),
                          "acceptance_match": sum(r["acceptance_match"] for r in rows),
                          "deps_match": sum(r["deps_match"] for r in rows),
                          "max_level": max(level.values())}},
              open(os.path.join(OUT, "backlog66.json"), "w"), indent=1, ensure_ascii=False)

    # ---------- doc 05 module cards ----------
    cards = []
    for s in docs["05"]:
        if s["level"] == 2 and any(p.startswith("Objective:") for p in s["prose"]):
            f = OrderedDict()
            for p in s["prose"]:
                if ":" in p:
                    k, v = p.split(":", 1)
                    f[k.strip()] = v.strip()
            api = f.get("REST API / runtime interface", "")
            ents = f.get("Database entities", "")
            ops = re.findall(r"(GET|POST|PUT|PATCH|DELETE)\s+(/[^\s;]+)", api)
            op_res = []
            p32 = bp["Part-03-2_API_and_Integration.md"]
            for meth, path in ops:
                pat = re.escape("`/api/v1" + path + "`")
                hit = re.search(r"\| (API-\d+)[^|]*\| " + meth + r" \| " + pat, p32)
                op_res.append({"method": meth, "path": path, "api_id": hit.group(1) if hit else None})
            ent_res = []
            p33 = bp["Part-03-3_Data_Architecture.md"]
            for e in [x.strip() for x in ents.split(",") if x.strip()]:
                ent_res.append({"entity": e, "in_3_3": bool(re.search(r"\b" + re.escape(e) + r"\b", p33)),
                                "in_2_1": bool(re.search(r"\b" + re.escape(e) + r"\b",
                                               bp["Part-02-1_Functional_Design_Modules_and_FR_Register.md"]))})
            cand = f.get("Integration candidates", "")
            cards.append({"module": s["title"], "fields": f, "ops": op_res, "entities": ent_res,
                          "integration_candidates": cand,
                          "candidates_in_bp": {c.strip(): bool(where(bp, re.escape(c.strip())))
                                               for c in cand.split(",") if c.strip()}})
    json.dump(cards, open(os.path.join(OUT, "modulecards.json"), "w"), indent=1, ensure_ascii=False)

    # ---------- OPT controls ----------
    opt = OrderedDict()
    for k, secs in docs.items():
        for s in secs:
            for p in s["prose"]:
                for m in re.finditer(r"(OPT-\d\d-\d\d) • ([^—]+) — (.+)", p):
                    oid = m.group(1)
                    rec = opt.setdefault(oid, {"id": oid, "title": m.group(2).strip(),
                                               "control": m.group(3).strip(), "docs": [],
                                               "dimension": s["title"]})
                    if k not in rec["docs"]:
                        rec["docs"].append(k)
                m2 = re.match(r"Acceptance / evidence: (.+) \| Accountable: (.+)\.", p)
                if m2 and opt:
                    last = list(opt.values())[-1]
                    last.setdefault("acceptance", m2.group(1).strip())
                    last.setdefault("accountable", m2.group(2).strip())
    frd = "\n".join(read(os.path.join(SRC, "02_Functional_Specification.txt")))
    for oid, rec in opt.items():
        rec["in_frd"] = oid in frd
        rec["bp_parts_citing_id"] = where(bp, re.escape(oid))
    json.dump(list(opt.values()), open(os.path.join(OUT, "opt_controls.json"), "w"), indent=1, ensure_ascii=False)

    # ---------- estimates ----------
    est = {}
    for t in tab_out["04"]:
        if t["header"] and t["header"][0] == "Discipline":
            tot = 0.0
            chk = []
            for r in t["rows"]:
                pdv = float(r[1])
                tot += pdv
                lo = round(pdv / 22 * 100000)
                hi = round(pdv / 22 * 150000)
                chk.append({"discipline": r[0], "pd": pdv, "src_1L": r[2], "calc_1L": lo,
                            "src_1_5L": r[3], "calc_1_5L": hi})
            est["discipline"] = {"rows": chk, "total_pd": round(tot, 2)}
        if t["header"] and t["header"][0] == "Task":
            tasks = {}
            for r in t["rows"]:
                lo, base, hi = [float(x) for x in r[3].split("/")]
                preds = [x.strip() for x in r[2].split(";") if x.strip().startswith("UX-TASK")]
                tasks[r[0]] = {"title": r[1], "preds": preds, "low": lo, "base": base, "high": hi}
            sums = {x: sum(v[x] for v in tasks.values()) for x in ("low", "base", "high")}
            memo = {}

            def cp(u, key):
                if (u, key) in memo:
                    return memo[(u, key)]
                best_ = max([cp(p, key) for p in tasks[u]["preds"]] or [(0, [])], key=lambda x: x[0])
                memo[(u, key)] = (best_[0] + tasks[u][key], best_[1] + [u])
                return memo[(u, key)]
            est["ux_tasks"] = {"tasks": tasks, "sums": sums,
                               "critical_path": {k_: cp("UX-TASK-QA", k_) for k_ in ("low", "base", "high")}}
        if t["header"] and t["header"][0] == "Pilot item":
            items = {r[0]: float(r[1]) for r in t["rows"]}
            base = sum(v for kk, v in items.items() if kk not in ("Apollo paid enrichment reserve",
                                                                     "Claude Code developer seats",
                                                                     "Contingency rate"))
            opt_ = items["Apollo paid enrichment reserve"] + items["Claude Code developer seats"]
            est["cost"] = {"items": items, "base_before_contingency": base,
                           "base_with_contingency": base * 1.15,
                           "with_optional_with_contingency": (base + opt_) * 1.15}
        if t["header"] and t["header"][0] == "Work package":
            est["work_packages"] = {r[0]: r[1] for r in t["rows"]}
        if t["header"] and t["header"][0] == "Metric":
            est["capacity"] = [{"metric": r[0], "initial": r[1], "growth": r[2]} for r in t["rows"]]
    json.dump(est, open(os.path.join(OUT, "estimates.json"), "w"), indent=1, ensure_ascii=False)

    summary = {
        "doc_sizes_bytes": {k: os.path.getsize(os.path.join(SRC, v)) for k, v in DOCS.items()},
        "doc_lines": {k: len(raw[k]) for k in raw},
        "common_core_identical_lines_vs_04": core,
        "sections": {k: len(v) for k, v in sec_out.items()},
        "tables": {k: len(v) for k, v in tab_out.items()},
        "table_rows": {k: sum(len(t["rows"]) for t in v) for k, v in tab_out.items()},
        "backlog66": json.load(open(os.path.join(OUT, "backlog66.json")))["counts"],
        "module_cards": len(cards),
        "module_card_ops": sum(len(c["ops"]) for c in cards),
        "module_card_ops_found": sum(1 for c in cards for o in c["ops"] if o["api_id"]),
        "module_card_entities": sum(len(c["entities"]) for c in cards),
        "module_card_entities_in_3_3": sum(1 for c in cards for e in c["entities"] if e["in_3_3"]),
        "opt_controls": len(opt),
        "opt_in_frd": sum(1 for r in opt.values() if r["in_frd"]),
        "opt_cited_in_bp": sum(1 for r in opt.values() if r["bp_parts_citing_id"]),
    }
    json.dump(summary, open(os.path.join(OUT, "summary.json"), "w"), indent=1, ensure_ascii=False)
    print(json.dumps(summary, indent=1))


if __name__ == "__main__":
    sys.exit(main())
