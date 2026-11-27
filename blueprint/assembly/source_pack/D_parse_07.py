#!/usr/bin/env python3
"""Group D: parse source document 07 (REST API & External Integration Catalog).

Outputs JSON with: operations (302), sit table, dec entries (38), candidates (19 SM-UX-API),
and Part 3.2 blueprint catalogue rows (API-###, AD-##, events).
Usage: python3 -I D_parse_07.py <doc07.txt> <Part-03-2.md> <out.json>
"""
import json
import re
import sys

src, bp, out = sys.argv[1], sys.argv[2], sys.argv[3]
lines = open(src, encoding="utf-8").read().split("\n")

FIELD_KEYS = [
    "Implementation contract (proposed; approval required)", "Access boundary", "Website interface associations",
    "Interface type", "Purpose", "Data effect", "Request contract", "Response contract", "Authorization",
    "Acceptance", "Implementation", "Module", "Screens", "Tables", "Integration", "Licence", "Free quota",
    "Paid rate", "Allocation", "Source", "Verification", "PostgreSQL entities", "Interfaces",
]
KEY_RE = re.compile(r"^(" + "|".join(re.escape(k) for k in FIELD_KEYS) + r"):\s?(.*)$")
HEAD_RE = re.compile(r"^<Heading2> (\d{3})\. (GET|POST|PATCH|PUT|DELETE|ADAPTER) (.+)$")

ops = []
cur = None
for i, ln in enumerate(lines):
    m = HEAD_RE.match(ln)
    if m:
        cur = {"num": m.group(1), "method": m.group(2), "path": m.group(3).strip(), "line": i + 1, "fields": {}}
        ops.append(cur)
        continue
    if ln.startswith("<Heading"):
        cur = None
        continue
    if cur is not None:
        km = KEY_RE.match(ln)
        if km:
            cur["fields"][km.group(1)] = km.group(2).strip()


def parse_fields(spec):
    """Parse 'name:type [enum] required; name2:type optional/review' into list."""
    res = []
    for part in spec.split(";"):
        part = part.strip().rstrip(".")
        if not part:
            continue
        mm = re.match(r"([A-Za-z_][A-Za-z0-9_]*):([A-Za-z\-]+)(?:\s*\[([^\]]*)\])?\s*(required|optional/review)?", part)
        if mm:
            res.append({"name": mm.group(1), "type": mm.group(2), "enum": (mm.group(3) or ""),
                        "required": mm.group(4) == "required"})
    return res


for op in ops:
    ic = op["fields"].get("Implementation contract (proposed; approval required)", "")
    op["contract_kind"] = (
        "explicit_dto" if ic.startswith("Proposed explicit DTO") else
        "public_allowlist" if ic.startswith("Proposed public response allowlist") else
        "cursor_list" if ic.startswith("Proposed cursor/page-size") else
        "adapter_review" if ic.startswith("Adapter contract review") else
        "review_required" if ic.startswith("Review required") else "other")
    rq = re.search(r"Request fields: (.*?)\. (?:Synthetic request|Result fields)", ic)
    rs = re.search(r"Result fields: (.*?)\. (?:Proposed status|SIT assertion)", ic)
    st = re.search(r"Proposed status (\d{3})", ic)
    sit = re.search(r"SIT assertion: (.*?)(?:\. Assert source result: (.*))?$", ic)
    syn = re.search(r"Synthetic request: (\{.*?\})\. Result fields", ic)
    qex = re.search(r"Query example: (\{.*?\})", ic)
    op["req_fields"] = parse_fields(rq.group(1)) if rq else []
    op["res_fields"] = parse_fields(rs.group(1)) if rs else []
    op["proposed_status"] = st.group(1) if st else ""
    op["sit_assertion"] = sit.group(1).strip() if sit else ""
    op["sit_result"] = (sit.group(2) or "").strip() if sit else ""
    op["synthetic_request"] = syn.group(1) if syn else ""
    op["query_example"] = qex.group(1) if qex else ""
    ab = op["fields"].get("Access boundary", "")
    op["boundary"] = ab.split(".")[0].strip()

# SIT IDs table
sit_map = {}
text = "\n".join(lines)
for m in re.finditer(r"---row\n((?:GET|POST|PATCH|PUT|DELETE|ADAPTER) [^\n]+)\n([^\n]*)\n([^\n]*)\n([^\n]*)\n(SM-SIT-A\d{3})", text):
    sit_map[m.group(5)] = {"op": m.group(1), "boundary": m.group(2), "req": m.group(3), "res": m.group(4)}
for op in ops:
    sid = "SM-SIT-A" + op["num"]
    op["sit_id"] = sid if sid in sit_map else ""
    if sid in sit_map and sit_map[sid]["op"] != f'{op["method"]} {op["path"]}':
        op["sit_mismatch"] = sit_map[sid]["op"]

# DEC entries (source-local, renamed SRC07-DEC)
decs = []
for m in re.finditer(r"<Heading2> DEC-(\d{3}) — ((?:GET|POST|PATCH|PUT|DELETE) \S+)\nSource requirement: (.*)\nProposed resolution: (.*)\nReview evidence: (.*)\nOwner: (.*)", text):
    decs.append({"id": "SRC07-DEC-" + m.group(1), "op": m.group(2), "source_req": m.group(3),
                 "resolution": m.group(4), "evidence": m.group(5), "owner": m.group(6)})

# Candidates SM-UX-API
cands = []
for m in re.finditer(r"<Heading3> (SM-UX-API-\d{2}) — (GET|POST|PATCH) (\S+)\n(.*)\n(.*)\n(.*)", text):
    head = [x.strip() for x in m.group(4).split("|")]
    req = re.search(r"Candidate request: (.*?)Candidate response: (.*)$", m.group(5))
    tail = [x.strip() for x in m.group(6).split("|")]
    cands.append({"id": m.group(1), "method": m.group(2), "path": m.group(3), "title": head[0],
                  "screen": head[1] if len(head) > 1 else "", "audience": head[2] if len(head) > 2 else "",
                  "control": head[3] if len(head) > 3 else "",
                  "req_schema": req.group(1) if req else "", "res_schema": req.group(2) if req else "",
                  "entities": tail[0].replace("Entities: ", ""), "success": tail[1].replace("Success: ", "")})
reuse = {}
for m in re.finditer(r"^(SM-UX-API-\d{2}) — (.*?) \| (.*?) \| (Pending reuse approval\.)$", text, re.M):
    reuse[m.group(1)] = {"reuse_ops": m.group(2), "note": m.group(3)}
for c in cands:
    c.update(reuse.get(c["id"], {}))

# OPT controls
opts = re.findall(r"^(OPT-\d{2}-\d{2}) • (.*?) — (.*)\nAcceptance / evidence: (.*?) \| Accountable: (.*)$", text, re.M)

# Blueprint Part 3.2
bpl = open(bp, encoding="utf-8").read().split("\n")
bpops = []
dom = ""
for ln in bpl:
    if ln.startswith("#### "):
        dom = ln[5:].strip()
    m = re.match(r"^\| (API-\d{3})( ★)? \| (\w+) \| `([^`]+)` \| ([^|]+) \| ([^|]*) \| ([^|]*) \| ([^|]*) \| ([^|]*) \| ([^|]*) \| ([^|]*) \| ([^|]*) \|", ln)
    if m:
        p = m.group(4)
        full = p.replace("~/", "/api/v1/commercial/")
        bpops.append({"id": m.group(1), "star": bool(m.group(2)), "method": m.group(3), "path": p, "full": full,
                      "ns": m.group(5).strip(), "purpose": m.group(6).strip(), "fr": m.group(7).strip(),
                      "auth": m.group(8).strip(), "idem": m.group(9).strip(), "se": m.group(10).strip(),
                      "pdp": m.group(11).strip(), "rl": m.group(12).strip(), "domain": dom})
ads = []
for ln in bpl:
    m = re.match(r"^\| (AD-\d{2}) \| (.*?) \| (.*?) \|", ln)
    if m and not any(a["id"] == m.group(1) for a in ads):
        ads.append({"id": m.group(1), "provider": m.group(2), "purpose": m.group(3)})

json.dump({"ops": ops, "sit": sit_map, "decs": decs, "cands": cands, "opts": opts,
           "bpops": bpops, "ads": ads}, open(out, "w"), indent=1, ensure_ascii=False)
print("ops", len(ops), "sit", len(sit_map), "decs", len(decs), "cands", len(cands), "opts", len(opts),
      "bpops", len(bpops), "ads", len(ads))
from collections import Counter
print(Counter(o["method"] for o in ops))
print(Counter(o["contract_kind"] for o in ops))
print(Counter(o["boundary"] for o in ops))
print(Counter(o["fields"].get("Interface type", "-") for o in ops))
print("sit mismatches", [o["num"] for o in ops if o.get("sit_mismatch")])
print("bp star", sum(1 for b in bpops if b["star"]))
