#!/usr/bin/env python3
"""Group D: assemble Part 3.5a/3.5b Markdown from skeletons + fragments; write D_coverage.csv.

Usage: python3 -I D_assemble_07.py <d07.json> <map.json> <frag_dir> <skeleton_dir> <blueprint_dir>
"""
import csv
import importlib.util
import json
import os
import sys
from collections import Counter, OrderedDict

d = json.load(open(sys.argv[1]))
rows = json.load(open(sys.argv[2]))
FR, SK, BP = sys.argv[3], sys.argv[4], sys.argv[5]
spec = importlib.util.spec_from_file_location("asp", os.path.join(SK, "D_aspects_07.py"))
asp = importlib.util.module_from_spec(spec)
spec.loader.exec_module(asp)
bp = {b["id"]: b for b in d["bpops"]}
cov_ops = json.load(open(os.path.join(FR, "cov_ops.json")))["cov"]
STATUSES = ["Covered", "Partially covered", "Not covered", "Conflict", "Not applicable"]


def esc(s):
    return str(s).replace("|", "\\|")


def frag(name):
    return open(os.path.join(FR, name), encoding="utf-8").read().rstrip("\n")


# ---------- OPT mapping ----------
OPTMAP = {
    "OPT-01-01": ("NFR-003, NFR-050; DEC-058", "Covered", "Revoked/wrong-audience requests in N02; step-up in E-S"),
    "OPT-02-01": ("NFR-041, NFR-042, NFR-043", "Covered", "Blueprint targets equal (LCP 2.5 s, INP 200 ms, CLS 0.1)"),
    "OPT-02-02": ("NFR-027, NFR-044", "Covered", "Latest filter wins; scope switch clears cache"),
    "OPT-02-03": ("NFR-039, NFR-044, NFR-046; §3.2.1.6", "Covered", "Blueprint stricter than source p95 dashboard ≤ 2 s; field allowlists in §3.5.5.3"),
    "OPT-02-04": ("FR-A032 (Customer 360 ≤ 60 s); NFR-027; ADR-034", "Covered", "Projection cache keyed by permission revision"),
    "OPT-02-05": ("NFR-040, NFR-045", "Covered", "Sync part ≤ 800 ms is stricter than source ACK ≤ 2 s"),
    "OPT-02-06": ("NFR-039, NFR-060", "Partially covered", "Per-operation query budget added (RECOMMENDATION-371, FR-ENH-D-005)"),
    "OPT-02-07": ("NFR-062; §3.2.7.3 bulkheads", "Covered", "—"),
    "OPT-08-01": ("NFR-017; Part 3.3", "Covered", "—"),
    "OPT-08-02": ("Part 3.3 index strategy", "Covered", "—"),
    "OPT-08-03": ("Part 3.3; NFR-039", "Partially covered", "N+1 gate via x-perf max_queries (FR-ENH-D-005)"),
    "OPT-08-04": ("NFR-017; CA-FIN; FR-DM-01", "Covered", "Money as decimal string (§3.5.5.1)"),
    "OPT-08-05": ("NFR-002; Part 3.3 vector scope", "Covered", "—"),
    "OPT-08-06": ("NFR-056, NFR-057; Part 3.3 migrations", "Covered", "—"),
    "OPT-09-01": ("NFR-015; §3.5.5.3, §3.5.5.9", "Partially covered", "Field contracts and approval gate added"),
    "OPT-09-02": ("§3.2.1.2 field minimization; CT-06", "Partially covered", "Bytes per operation measured via x-perf"),
    "OPT-09-03": ("§3.2.7; IP-09; CT-08", "Covered", "AdapterResult latency/status fields added"),
    "OPT-09-04": ("NFR-051, NFR-005; CT-10", "Covered", "Blueprint p95 ≤ 500 ms is stricter than source ≤ 2 s"),
    "OPT-09-05": ("NFR-035, NFR-037, NFR-093; IP-06", "Partially covered", "metered_units in AdapterResult (§3.5.5.6.1)"),
    "OPT-19-01": ("NFR-028; DEC-030; BR-M07", "Covered", "—"),
}
t = ["| OPT control | Requirement (source) | Acceptance / evidence (source) | Accountable (source) | Blueprint NFR / location | Status | Addition in this batch |", "|---|---|---|---|---|---|---|"]
for oid, title, a, b2, own in d["opts"]:
    loc, st, add = OPTMAP[oid]
    t.append(f"| {oid} | **{esc(title)}**: {esc(a)} | {esc(b2)} | {esc(own)} | {loc} | {st} | {add} |")
    cov_ops.append(["07", "Optimization engineering and acceptance", oid, f"{title}: {a[:90]}", st, loc, add if add != "—" else "None", "§3.5.5.10" if st != "Covered" else ""])
OPT_TABLE = "\n".join(t)

# ---------- reuse table ----------
t = ["| Candidate | Source reuse suggestion | Source note | Part 3.2 operation(s) used | Decision |", "|---|---|---|---|---|"]
for c in d["cands"]:
    r = [x for x in rows if x["source_id"] == c["id"]][0]
    dec = "Reuse existing derived operation(s)" if r["relation"] in ("alias", "split") else "Reuse plus enhancement " + r["enhancement"]
    t.append(f'| {c["id"]} | {esc(c.get("reuse_ops", ""))} | {esc(c.get("note", ""))} | {r["blueprint_ops"].replace(";", ", ")} | {dec} |')
REUSE = "\n".join(t)

# ---------- adapter table ----------
t = ["| Source op | Source adapter | Source purpose | Source integrations | Source SIT assertion | Part 3.2 adapter(s) | Relation | Delta added here |", "|---|---|---|---|---|---|---|---|"]
for r in rows:
    if r["method"] != "ADAPTER":
        continue
    o = [x for x in d["ops"] if "SM-OP-" + x["num"] == r["source_id"]][0]
    t.append(f'| {r["source_id"]} | {esc(r["path"])} | {esc(r["purpose"])} | {esc(o["fields"].get("Integration", ""))} | {esc(o["sit_assertion"])} | {r["blueprint_ops"].replace(";", ", ")} | {r["relation"]} | {esc(r["note"]) or "Envelope §3.5.5.6.1"}{(" · " + r["enhancement"]) if r["enhancement"] else ""} |')
ADAPTERS = "\n".join(t)

# ---------- allowlist ----------
WEBNS = {"public", "portal", "public+portal", "admin+portal", "bff-web", "bff"}
t = ["| # | Operation | Method | Path | Classification on website ingress | Rate-limit class |", "|---|---|---|---|---|---|"]
n = 0
for b in d["bpops"]:
    if b["ns"] in WEBNS:
        n += 1
        cls = b["ns"]
        if b["id"] == "API-083":
            cls = "portal (reclassified, CONFLICT-367)"
        if b["ns"] == "admin+portal":
            cls = "portal mount only (separate serializer)"
        if b["ns"] == "bff":
            cls = "bff (legacy alias; delegates to BFF login)"
        t.append(f'| {n} | {b["id"]} | {b["method"]} | `{b["path"]}` | {cls} | {b["rl"]} |')
for e in [("API-ENH-D-018", "POST", "~/portal/uploads/{id}/complete"), ("API-ENH-D-019", "GET", "~/portal/onboarding-wizard/{app}"), ("API-ENH-D-020", "POST", "~/portal/service/offboarding-requests")]:
    n += 1
    t.append(f"| {n} | {e[0]} | {e[1]} | `{e[2]}` | portal (new) | RL-PORTAL |")
n += 1
t.append(f"| {n} | API-290 (alias) | GET | `/api/v1/commercial/public/site/pages/{{slug}}` | public (canonical path, CONFLICT-360) | RL-PUB-R |")
ALLOW = "\n".join(t) + f"\n\n**Total: {n} website-ingress routes.** Every other route (Admin, internal, hooks) is absent from the `urls_web` map; hooks are served by the separate hooks distribution (Part 3.2 §3.2.1.1)."
NALLOW = n

# ---------- aspects (prose) ----------
prose = [list(a) for a in asp.ASPECTS]
t = ["| Aspect | Source section | Aspect | Status | Blueprint location | Action | New IDs / tags |", "|---|---|---|---|---|---|---|"]
for a in prose:
    t.append("| " + " | ".join(esc(x) for x in a) + " |")
ASPECTS_TABLE = "\n".join(t)

# ---------- coverage CSV ----------
allcov = [["07", a[1], a[0], a[2], a[3], a[4], a[5], a[6]] for a in prose] + cov_ops
with open(os.path.join(BP, "final/coverage/D_coverage.csv"), "w", newline="", encoding="utf-8") as fh:
    w = csv.writer(fh)
    w.writerow(["doc", "section", "aspect_id", "aspect_summary", "status", "blueprint_location", "action", "new_ids"])
    w.writerows(allcov)


def fam(aid, row):
    if aid.startswith("SM-UX"):
        return "Candidate operations (endpoint + schema)"
    if aid.startswith("SM-OP") and aid.endswith("-DTO"):
        return "Field contracts (HTTP operations)"
    if aid.startswith("SM-OP") and aid.endswith("-CTX"):
        return "Adapter command/result context"
    if aid.startswith("SM-OP"):
        return "Operation endpoints (302 retained, incl. 17 adapters)"
    if aid.startswith("SM-SIT"):
        return "Operation SIT tests"
    if aid.startswith("SRC07-DEC"):
        return "Contract decisions SRC07-DEC"
    if aid.startswith("PROV-"):
        return "Providers and tools"
    if aid.startswith("OPT-"):
        return "Optimization controls"
    if aid.startswith("07-CC"):
        return "Common core (listed once)"
    return "Prose, contract and control aspects"


fc = OrderedDict()
for r in allcov:
    f = fam(r[2], r)
    fc.setdefault(f, Counter())[r[4]] += 1
tot = Counter()
t = ["| Aspect family | Aspects | " + " | ".join(STATUSES) + " |", "|---|---|" + "---|" * len(STATUSES)]
for f, c in fc.items():
    tot.update(c)
    t.append(f"| {f} | {sum(c.values())} | " + " | ".join(str(c.get(s, 0)) for s in STATUSES) + " |")
t.append(f"| **Document 07 total** | **{sum(tot.values())}** | " + " | ".join(f"**{tot.get(s, 0)}**" for s in STATUSES) + " |")
SUMMARY = "\n".join(t)
ASPECT_COUNT = "\n".join([
    "| Aspect family | Count | Basis |", "|---|---|---|"] + [
    f"| {f} | {sum(c.values())} | " + {
        "Prose, contract and control aspects": "Engineering contracts, operating contract, adapter contract, lifecycle, implementation controls, field-level approval, acceptance procedures, current scope, security readings",
        "Common core (listed once)": "Purpose/boundary, startup configurations, technology principles (not re-assessed per document)",
        "Operation endpoints (302 retained, incl. 17 adapters)": "One aspect per operation (method/path or adapter, boundary, purpose)",
        "Field contracts (HTTP operations)": "One aspect per HTTP operation's request/response contract",
        "Adapter command/result context": "One aspect per adapter's context and result envelope",
        "Operation SIT tests": "One aspect per SM-SIT-A### row",
        "Candidate operations (endpoint + schema)": "SM-UX-API-01…19",
        "Contract decisions SRC07-DEC": "DEC-001…038 sections",
        "Providers and tools": "Distinct names in Integration columns",
        "Optimization controls": "OPT-01-01 … OPT-19-01",
    }.get(f, "") + " |" for f, c in fc.items()] + [f"| **Total atomic aspects** | **{sum(tot.values())}** | |"])

fam_rows = []
for f, c in fc.items():
    if f.startswith("Prose") or f.startswith("Common"):
        continue
    where = {"Operation endpoints (302 retained, incl. 17 adapters)": "§3.5.4.3", "Field contracts (HTTP operations)": "File b §3.5.5.3–4",
             "Adapter command/result context": "File b §3.5.5.6", "Operation SIT tests": "File b §3.5.5.12.2", "Candidate operations (endpoint + schema)": "§3.5.4.4; file b §3.5.5.5",
             "Contract decisions SRC07-DEC": "File b §3.5.5.4", "Providers and tools": "File b §3.5.5.6.4", "Optimization controls": "File b §3.5.5.10"}.get(f, "CSV")
    fam_rows.append(f"| {f} | {sum(c.values())} | {c.get('Covered',0)} | {c.get('Partially covered',0)} | {c.get('Not covered',0)} | {c.get('Conflict',0)} | {where} |")
FAMROWS = "\n".join(fam_rows)

# provider summary
pc = Counter()
for r in cov_ops:
    if r[2].startswith("PROV-"):
        cls = r[3].split("(")[1].split(")")[0]
        pc[(cls, r[4])] += 1
t = ["| Class | Covered | Partially covered | Not covered | Conflict | Not applicable | Total |", "|---|---|---|---|---|---|---|"]
for cls in ["Runtime provider", "OSS library", "Developer plugin", "Unapproved SaaS"]:
    vals = [pc.get((cls, s), 0) for s in ["Covered", "Partially covered", "Not covered", "Conflict", "Not applicable"]]
    t.append(f"| {cls} | " + " | ".join(map(str, vals)) + f" | {sum(vals)} |")
PSUM = "\n".join(t)

def escape_dollars(text):
    out, fence = [], False
    for line in text.split("\n"):
        if line.startswith("```"):
            fence = not fence
            out.append(line)
            continue
        if fence:
            out.append(line)
            continue
        parts = line.split("`")
        for i in range(0, len(parts), 2):
            parts[i] = parts[i].replace("\\$", "$").replace("$", "\\$")
        out.append("`".join(parts))
    return "\n".join(out)


REPL = {
    "<<ASPECT_COUNT_TABLE>>": ASPECT_COUNT, "<<SUMMARY_TABLE>>": SUMMARY, "<<ASPECTS_TABLE>>": ASPECTS_TABLE,
    "<<CATALOGUE_FAMILY_ROWS>>": FAMROWS, "<<COUNTS_REL>>": frag("counts_rel.md"), "<<COUNTS_BOUNDARY>>": frag("counts_boundary.md"),
    "<<COUNTS_KIND>>": frag("counts_kind.md"), "<<REUSE_TABLE>>": REUSE, "<<ADAPTER_TABLE>>": ADAPTERS, "<<PROVIDER_SUMMARY>>": PSUM,
    "<<ALLOWLIST_TABLE>>": ALLOW, "<<OPT_TABLE>>": OPT_TABLE,
}
for sk, out in [("D_skeleton_a.md", "Part-03-5a_Source_Pack_API_Catalog_Reconciliation.md"), ("D_skeleton_b.md", "Part-03-5b_Source_Pack_API_Catalog_Reconciliation.md")]:
    s = open(os.path.join(SK, sk), encoding="utf-8").read()
    for k, v in REPL.items():
        s = s.replace(k, v)
    while "<<FRAG:" in s:
        i = s.index("<<FRAG:")
        j = s.index(">>", i)
        s = s[:i] + frag(s[i + 7:j]) + s[j + 2:]
    s = s.replace("website ingress allowlist (80 operations)", f"website ingress allowlist ({NALLOW} operations)")
    s = escape_dollars(s)
    assert "<<" not in s, s[s.index("<<"):s.index("<<") + 40]
    open(os.path.join(BP, out), "w", encoding="utf-8").write(s)
    print(out, len(s))
print("coverage rows", len(allcov), dict(tot))
for f, c in fc.items():
    print(f, dict(c))
