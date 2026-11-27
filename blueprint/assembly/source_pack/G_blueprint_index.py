#!/usr/bin/env python3
"""Group G: index the blueprint for test reconciliation.

Builds (as JSON) from the blueprint Markdown:
  - tcs:   every TC row of Part 6.2-6.7 (via assembly/build_rtm.py load_tcs): id, file, title, links, steps text,
           level, priority, cited (method, normalized path) pairs, aliases cited
  - fr_tc: FR/BR -> TC list (RTM.csv)
  - ops:   Part 3.2 API catalogue rows (API-###, method, path, FR/screen)
  - adp:   Part 3.2 adapter catalogue rows (AD-##)
  - mod:   Part 2.1 module M## -> FRs
Usage: python3 G_blueprint_index.py <out.json>
"""
import csv
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
BP = os.path.dirname(os.path.dirname(HERE)) + "/"
sys.path.insert(0, os.path.dirname(HERE))
import build_rtm as B  # noqa: E402


def norm(path):
    p = path.strip().strip("`").split("?")[0].rstrip(".,;:)")
    p = p.replace("~/", "/api/v1/commercial/")
    for pre in ("/api/v1/commercial/workspace/", "/api/v1/commercial/", "/api/v1/"):
        if p.startswith(pre):
            p = "/" + p[len(pre):]
            break
    p = re.sub(r"\{[^}]*\}", "{}", p)
    p = re.sub(r"^/(admin|public|portal|internal|workspace)/", "/", p)
    p = re.sub(r"^/(admin|public|portal|internal)/", "/", p)
    return p.lower().rstrip("/")


PATH_RE = re.compile(r"\b(GET|POST|PATCH|PUT|DELETE)\s+`?((?:~|/)[A-Za-z0-9_{}\-/.]+)")


def main(out):
    st = B.batch_status()
    tcs, resolved = B.load_tcs(st)
    T = {}
    for tid, v in tcs.items():
        c = B.cells(v["row"])
        # compact table: ID | Title | Links | Pre | Steps | Expected | P | Type | Tech | Auto | Lvl
        title = c[1] if len(c) > 1 else ""
        lvl = c[-1] if c and re.fullmatch(r"(UT|IT|CT|SYS|E2E|UAT|[A-Z/ +]+)", c[-1] or "") else ""
        T[tid] = dict(file=v["file"], title=title, links=sorted(v["links"]), prio=v["prio"], tech=v["tech"],
                      lvl=lvl, text=v["row"],
                      paths=sorted({(m.group(1), norm(m.group(2))) for m in PATH_RE.finditer(v["row"])}),
                      aliases=sorted(set(re.findall(r"SM-(?:UT-\d{3}|UAT-S\d{3}|UX-UAT-[WA]\d{2,3})", v["row"]))))
    fr_tc = {}
    with open(BP + "final/RTM.csv", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            fr_tc[r["requirement_id"]] = dict(type=r["requirement_type"], title=r["title"], epic=r["epic"],
                                              wave=r["wave"], tc_ids=r["tc_ids"], tc_count=r["tc_count"],
                                              flag=r["coverage_flag"], linked_fr=r["linked_fr"],
                                              aliases=r["aliases"])
    ops = []
    t = open(BP + "Part-03-2_API_and_Integration.md", encoding="utf-8").read()
    for line in t.split("\n"):
        m = re.match(r"\| (API-\d{3})( ★)? \| (\w+(?:/\w+)?) \| `([^`]+)` \| ([^|]*) \| ([^|]*) \| ([^|]*) \|", line)
        if m:
            ops.append(dict(id=m.group(1), star=bool(m.group(2)), method=m.group(3), path=m.group(4),
                            ns=m.group(5).strip(), purpose=m.group(6).strip(), fr=m.group(7).strip(),
                            norm=norm(m.group(4))))
    adp = []
    for line in t.split("\n"):
        m = re.match(r"\| (AD-\d{2}) \| \*\*(.*?)\*\* ?(.*?) \| (.*?) \|", line)
        if m:
            adp.append(dict(id=m.group(1), name=m.group(2), port=m.group(3), purpose=m.group(4)))
    mod = {}
    t21 = open(BP + "Part-02-1_Functional_Design_Modules_and_FR_Register.md", encoding="utf-8").read()
    for line in t21.split("\n"):
        m = re.match(r"\| \*?\*?M(\d{2})\*?\*? \| ([^|]*) \|(.*)", line)
        if m and ("M" + m.group(1)) not in mod:
            mod["M" + m.group(1)] = dict(name=m.group(2).strip(), frs=sorted(set(re.findall(r"FR-(?:W\d{2}|A\d{3})", m.group(3)))),
                                         row=line[:600])
    json.dump(dict(tcs=T, fr_tc=fr_tc, ops=ops, adp=adp, mod=mod), open(out, "w"), ensure_ascii=False)
    print("tcs", len(T), "rtm rows", len(fr_tc), "ops", len(ops), "adapters", len(adp), "modules", len(mod))


if __name__ == "__main__":
    main(sys.argv[1])
