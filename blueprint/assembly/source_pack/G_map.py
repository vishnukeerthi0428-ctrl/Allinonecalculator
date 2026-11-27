#!/usr/bin/env python3
"""Group G: build the complete source-test -> blueprint-TC mapping for document 22 (799 tests).

Usage: python3 G_map.py <doc22.json> <bp.json> <out_dir>
Writes:
  <BP>/final/coverage/G_test_mapping.csv   one row per source test (799)
  <out_dir>/G_map.json                     data used to generate the Part 6.8 tables
Inputs: G_parse_doc22.py output, G_blueprint_index.py output, curated equivalences in G_curated.py.
"""
import csv
import json
import math
import os
import re
import sys
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
BP = os.path.dirname(os.path.dirname(HERE)) + "/"
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.dirname(HERE))
import build_rtm as Bm  # noqa: E402
from G_blueprint_index import norm  # noqa: E402
import G_curated as C  # noqa: E402

src, bpj, outdir = sys.argv[1], sys.argv[2], sys.argv[3]
S = json.load(open(src))["records"]
B = json.load(open(bpj))
T = B["tcs"]
DEF = set(T)

# ------------------------------------------------------------------ helpers
STOP = set("the a an and or of to in on for with by is are be as at from that this it its no not only any all each into "
           "per via use used using than then when where which who after before must should can may verify record test "
           "case fixture synthetic scope run".split())


def tok(s):
    return [w for w in re.findall(r"[a-z][a-z0-9\-]{2,}", s.lower()) if w not in STOP]


DF = Counter()
for v in T.values():
    DF.update(set(tok(v["title"] + " " + v["text"])))
N = len(T)


def score(q, tid):
    qt = Counter(tok(q))
    dt = Counter(tok(T[tid]["title"] * 2 + " " + T[tid]["text"]))
    s = 0.0
    for w, n in qt.items():
        if w in dt:
            s += (1 + math.log(n)) * (1 + math.log(dt[w])) * (math.log((N + 1) / (DF[w] + 1)) + 1) ** 2
    return s / (1 + math.sqrt(sum(dt.values())))


def req_tcs(req):
    r = B["fr_tc"].get(req)
    out = Bm.expand_tc_ranges(r["tc_ids"], DEF) if r else []
    out += [k for k, v in T.items() if req in v["links"]]
    return list(dict.fromkeys(out))


def best(q, cands, k=3, levels=None):
    c = [t for t in cands if t in T and (not levels or T[t]["lvl"] in levels)]
    return [t for t, s in sorted(((t, score(q, t)) for t in c), key=lambda x: -x[1])[:k] if s > 0]


EPIC_PACK = {"EP-01": "UAT-PK-PORT", "EP-02": "UAT-PK-PORT", "EP-03": "UAT-PK-GOV", "EP-04": "UAT-PK-AUTO",
             "EP-05": "UAT-PK-AN/MM/EV/OS", "EP-06": "UAT-PK-AN/MM/EV/OS", "EP-07": "UAT-PK-WEB", "EP-08": "UAT-PK-GOV",
             "EP-09": "UAT-PK-WEB", "EP-10": "UAT-PK-MM", "EP-11": "UAT-PK-MKT (proposed)",
             "EP-12": "UAT-PK-MKT (proposed)", "EP-13": "UAT-PK-FIN", "EP-14": "UAT-PK-AN/OS", "EP-15": "UAT-PK-FIN",
             "EP-16": "UAT-PK-CS (proposed)", "EP-17": "UAT-PK-PORT", "EP-18": "UAT-PK-AUTO", "EP-19": "UAT-PK-WEB",
             "EP-20": "UAT-PK-SC", "EP-21": "UAT-PK-PORT"}


def screen_fr(screen):
    return "FR-" + screen


def pack_for(fr):
    r = B["fr_tc"].get(fr)
    return EPIC_PACK.get(r["epic"], "") if r else ""


# ------------------------------------------------------------------ operation matching (SIT-A)
ops_idx = defaultdict(list)
for o in B["ops"]:
    for m in o["method"].split("/"):
        ops_idx[(m, o["norm"])].append(o)
ADP = {"Object storage / document extraction": "AD-20 (malware scan) + S3; extraction AD-07",
       "AI inference / embeddings": "AD-13, AD-14", "Public web search": "AD-05, AD-06",
       "Permitted website fetch / extraction": "AD-07", "Apollo.io account / person enrichment": "AD-19",
       "Business contact verification provider": "AD-19 (EnrichmentPort, verification mode)",
       "Email delivery / inbound provider": "AD-01", "Calendar availability / booking": "AD-03, AD-04",
       "Meta WhatsApp Business API": "AD-02", "Authorized social listening API": "AD-08",
       "Official social publishing API": "AD-08", "Search Console / site audit": "AD-17",
       "Advertising provider API": "AD-09", "Webinar provider API": "AD-18", "E-sign provider API": "AD-10",
       "Payment gateway API": "AD-11", "CI/CD and health monitoring": "AD-15, AD-16 (+ CI, Part 4.3)"}
SYN = {"sales": "", "workspace": "", "control": "lifecycle"}


def path_tokens(p):
    out = []
    for seg in p.strip("/").split("/"):
        if seg == "{}":
            continue
        seg = SYN.get(seg, seg)
        if seg:
            out += re.split(r"[-_]", seg)
    return set(out)


def src_ns(path):
    if "/webhooks/" in path:
        return "hooks"
    if "/portal/" in path:
        return "portal"
    if "/public/" in path:
        return "public"
    if "/internal/" in path:
        return "internal"
    if "/admin/" in path:
        return "admin"
    return "any"


NS_OK = {"hooks": {"hooks", "public", "internal"}, "portal": {"portal", "admin+portal", "a+b", "bff-web"},
         "public": {"public", "portal", "admin+portal", "a+b", "bff-web"},
         "internal": {"internal", "admin"}, "any": {""}, "admin": {"admin", "admin+portal", "a+b", "bff", "bff-admin", "internal"}}


def ns_ok(src, o):
    ns = o["ns"].split()[0].strip()
    return any(ns.startswith(x) for x in NS_OK[src])


def match_op(meth, path, purpose):
    """Namespace-aware match of a source method/path to the Part 3.2 catalogue."""
    n = norm(path)
    n2 = re.sub(r"^/sales/", "/", n)
    sns = src_ns(path)
    for k in ((meth, n), (meth, n2)):
        c = [o for o in ops_idx.get(k, []) if ns_ok(sns, o)]
        if c:
            o = c[0]
            return o, ("exact" if o["star"] and k[1] == n and o["path"] == path else "normalized")
    if re.search(r"/(approve|review|decide)$", n2) and sns in ("admin", "any"):
        o = next(o for o in B["ops"] if o["id"] == "API-541")
        return o, "consolidated (Approval resource, Part 3.2 §3.2.2.1 step 4)"
    pt = path_tokens(n2)
    last = [x for x in n2.strip("/").split("/") if x != "{}"][-1:]
    last_t = set(re.split(r"[-_]", SYN.get(last[0], last[0]))) if last else set()
    best_o, best_s = None, 0.0
    for o in B["ops"]:
        if meth not in o["method"].split("/") or not ns_ok(sns, o):
            continue
        ot = path_tokens(o["norm"])
        if not ot or not pt or not (last_t <= ot):
            continue
        j = len(pt & ot) / len(pt | ot)
        j += 0.15 * len(set(tok(purpose)) & set(tok(o["purpose"]))) / (1 + len(set(tok(purpose))))
        if j > best_s:
            best_o, best_s = o, j
    if best_o and best_s >= 0.5:
        return best_o, "nearest (path tokens %.2f)" % best_s
    return None, "no blueprint operation"


CLASS_RULES = [
    ("TC-ENH-G-001", "Use verified Admin token for product A"),
    ("TC-ENH-G-002", "Seed authorized row A and foreign row B"),
    ("TC-ENH-G-003", "Use scoped fixture A, revision 1"),
    ("TC-ENH-G-004", "Use exact artifact hash and revision 1"),
    ("TC-ENH-G-005", "Stage approved hash a×64"),
    ("TC-ENH-G-006", "Use approved evidence A and foreign evidence B"),
    ("TC-ENH-G-007", "Use permitted example.invalid source"),
    ("TC-ENH-G-008", "Use an eligible contact then set opt-out"),
    ("TC-ENH-G-009", "Use object A and identity A"),
    ("TC-ENH-G-010", "Use approved DAG with two steps"),
    ("TC-ENH-G-011", "Use 1000.00 INR receipt"),
    ("TC-ENH-G-012", "Use own verified request and another identity"),
    ("TC-ENH-G-013", "Order 2 units at 150.00 INR"),
    ("TC-ENH-G-014", "Use deadline 2030-06-01T09:00Z"),
]


def op_classes(r):
    out = []
    if r["link"].startswith("ADAPTER") or "Use fake adapter only" in r["expected"]:
        out.append("TC-ENH-G-015")
    for cid, key in CLASS_RULES:
        if key in r["expected"]:
            out.append(cid)
    if r["group"] == "Provider callback":
        out.append("TC-ENH-G-016")
    if r["link"] in ("GET /api/v1/health", "GET /api/v1/ready"):
        out.append("TC-ENH-G-017")
    return out


# ------------------------------------------------------------------ build rows
rows = []
missing_tc = set()


def chk(lst):
    for t in lst:
        if t.startswith("TC-") and not t.startswith("TC-ENH") and t not in DEF:
            missing_tc.add(t)
    return lst


mods = {}
# Source SM-SIT-M### numbers follow document 22's table order, not the BRD module numbers used by BR-M## (ASSUMPTION-420):
# match by module name.
BRM_BY_NAME = {v["title"].strip().lower(): k for k, v in B["fr_tc"].items() if k.startswith("BR-M")}
for r in S:
    fam, sid = r["family"], r["id"]
    row = dict(source_id=sid, level=r["level"], family=fam, group=r["group"], title=r["title"], link=r["link"],
               bp_operation="", op_match="", bp_requirement="", status="", primary_tcs="", supporting_tcs="",
               tc_enh="", uat_pack="", note="", note_num="")
    q = " ".join([r["title"], r["steps"], r["expected"], r.get("negative", "")])
    if fam in ("UT", "SIT-F", "UAT-F") or sid.startswith("SM-UX-SIT-X"):
        cur = {"UT": C.UT, "SIT-F": C.SITF, "UAT-F": C.UATF}.get(fam, C.UXX)[sid]
        st, prim, enh, note = cur
        chk(prim)
        frs = sorted({l for t in prim if t in T for l in T[t]["links"] if l.startswith("FR-") or l.startswith("BRL-")})
        row.update(status=st, primary_tcs=" ".join(prim), tc_enh=" ".join(enh), note=note,
                   bp_requirement=" ".join(frs[:6]))
        if fam == "UAT-F":
            row["uat_pack"] = note.split(";")[0] if note.startswith("UAT-PK") else ("UAT-PK-MKT (proposed)" if sid in ("SM-UAT-F014", "SM-UAT-F015") else "UAT-PK-CS (proposed)" if sid == "SM-UAT-F017" else "UAT-PK-FIN")
    elif fam == "SIT-M":
        brm = BRM_BY_NAME.get(r["title"].strip().lower(), "BR-M" + sid[-2:])
        cands = req_tcs(brm)
        gate = r["expected"]
        top = best(gate + " " + r["title"], cands, 3)
        mods[sid] = dict(name=r["title"], br=brm, n=len(cands), top=top, gate=gate)
        ov = C.MOD_OVERRIDE.get(r["title"].strip())
        row.update(note_num=("same number" if brm[-2:] == sid[-2:] else "renumbered: source M%s = %s" % (sid[-3:], brm)),
                   bp_requirement=brm + " (" + B["fr_tc"].get(brm, {}).get("linked_fr", "") + ")",
                   primary_tcs=" ".join(top), supporting_tcs="%d TCs on %s (RTM)" % (len(cands), brm),
                   status=ov[0] if ov else ("E" if top else "N"), tc_enh=" ".join(ov[1]) if ov else "",
                   note=(ov[2] if ov else "Gate: " + gate))
    elif fam == "SIT-A":
        meth, _, path = r["link"].partition(" ")
        cls = op_classes(r)
        if meth == "ADAPTER":
            o, how = None, "adapter port"
            row["bp_operation"] = ADP.get(path, "")
            frs = []
        else:
            o, how = match_op(meth, path, r["title"])
            row["bp_operation"] = (o["id"] + " " + o["method"] + " " + o["path"]) if o else ""
            frs = re.findall(r"FR-(?:W\d{2}|A\d{3}|OP\d{3})", o["fr"]) if o else []
        cands = []
        for f in frs:
            cands += req_tcs(f)
        top = best(r["title"] + " " + path, list(dict.fromkeys(cands)), 3)
        if not top and meth != "ADAPTER":
            top = best(r["title"] + " " + path, list(T), 3, {"UT", "IT", "CT", "SYS", "E2E"})
        if meth == "ADAPTER":
            top = best(r["title"] + " " + path + " adapter contract sandbox fake", [t for t in T if T[t]["lvl"] in ("IT", "CT")], 3)
        row.update(op_match=how, bp_requirement=" ".join(frs), primary_tcs=" ".join(top), tc_enh=" ".join(cls),
                   status="M", note=("Functional TCs via " + " ".join(frs)) if frs else ("Adapter: " + row["bp_operation"]))
        if not o and meth != "ADAPTER":
            row["note"] = "No blueprint catalogue operation; covered by class TC and flagged GAP-421"
    elif fam == "UAT-S":
        n = int(sid[-3:])
        alias_fr = "FR-W%02d" % n if n <= 30 else "FR-A%03d" % (n - 30)
        scr = r["link"]
        ok = alias_fr == screen_fr(scr)
        cands = req_tcs(alias_fr)
        top = best(r["title"] + " " + r["steps"], cands, 3, {"E2E", "UAT", "SYS"})
        row.update(bp_requirement=alias_fr, primary_tcs=" ".join(top), supporting_tcs="%d TCs on %s" % (len(cands), alias_fr),
                   tc_enh="TC-ENH-G-036", uat_pack=pack_for(alias_fr), status="A" if ok else "C",
                   note=("Alias rule S###↔%s confirmed by source screen %s" % (alias_fr, scr)) if ok else "Alias rule mismatch")
    elif fam == "UX-UAT":
        fr = screen_fr(r["link"])
        cands = req_tcs(fr)
        cit = [k for k, v in T.items() if sid in v["aliases"]]
        top = cit[:3] if cit else best(r["title"] + " " + r["steps"], cands, 3)
        row.update(bp_requirement=fr + " / FR-UX-" + r["link"], primary_tcs=" ".join(top),
                   supporting_tcs="%d TCs cite %s; %d TCs on %s" % (len(cit), sid, len(cands), fr),
                   tc_enh="TC-ENH-G-037", uat_pack=pack_for(fr), status="A", note="DEC-017 alias SM-UX-UAT ↔ screen")
    elif fam in ("UX-UNIT", "UX-SIT"):
        fr = screen_fr(r["link"])
        cands = req_tcs(fr)
        lv = {"UT", "CT"} if fam == "UX-UNIT" else {"IT", "SYS", "E2E"}
        top = best(r["title"] + " " + r["steps"] + " " + r["expected"], cands, 3, lv)
        st = "E" if top else "P"
        enh = "" if top else "TC-ENH-G-038"
        row.update(bp_requirement=fr, primary_tcs=" ".join(top), supporting_tcs="%d TCs on %s" % (len(cands), fr),
                   status=st, tc_enh=enh, note="Level-matched TCs (%s)" % "/".join(sorted(lv)))
    rows.append(row)

assert len(rows) == 799
if missing_tc:
    print("WARNING undefined TC IDs in curated map:", sorted(missing_tc))
os.makedirs(BP + "final/coverage", exist_ok=True)
cols = ["source_id", "level", "family", "group", "title", "link", "bp_operation", "op_match", "bp_requirement", "status",
        "primary_tcs", "supporting_tcs", "tc_enh", "uat_pack", "note", "note_num"]
with open(BP + "final/coverage/G_test_mapping.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=cols)
    w.writeheader()
    w.writerows(rows)
json.dump(dict(rows=rows, mods=mods), open(os.path.join(outdir, "G_map.json"), "w"), ensure_ascii=False, indent=0)
print(Counter((r["family"], r["status"]) for r in rows))
print(Counter(r["op_match"].split(" (")[0] for r in rows if r["family"] == "SIT-A"))
print(Counter(c for r in rows for c in r["tc_enh"].split()))
