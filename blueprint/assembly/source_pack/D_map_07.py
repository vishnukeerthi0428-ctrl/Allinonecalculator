#!/usr/bin/env python3
"""Group D: map source doc 07 operations (302 + 19 candidates + 17 adapters) to blueprint Part 3.2.

Reads the JSON written by D_parse_07.py. Writes:
  - final/coverage/D_api_mapping.csv (one row per source operation / candidate)
  - <scratch>/map.json (for the Markdown generator)
Usage: python3 -I D_map_07.py <d07.json> <mapping.csv> <map.json>
Relations: exact = same method and path (legacy path retained) · alias = same semantics, blueprint path
differs · split = one source op maps to several blueprint ops (action enum split into sub-resources) ·
approval = consolidated into the Approval resource (API-541 submit + API-539 decide) · partial = some
semantics missing (enhancement op added) · none = not covered (enhancement op added) · adapter = AD-##.
"""
import csv
import json
import re
import sys

d = json.load(open(sys.argv[1]))
APPROVAL = "API-541;API-539"

# Manual semantic mapping for every operation whose method+path is not identical in Part 3.2.
# value: (relation, blueprint ops, note, enhancement op id or "")
M = {
    "003": ("alias", "API-019", "Legacy reuse alias of user directory", ""),
    "004": ("alias", "API-021;API-020", "Role assignment = grant change; invite via API-020", ""),
    "005": ("split", "API-007;API-012", "Logout per BFF client (admin, web)", ""),
    "007": ("alias", "API-054", "Product = Offering detail", ""),
    "008": ("alias", "API-053", "Product = Offering draft", ""),
    "009": ("split", "API-055;API-056", "Edit draft + create OfferingVersion", ""),
    "011": ("alias", "API-057", "Price version", ""),
    "013": ("alias", "API-061", "", ""),
    "014": ("approval", APPROVAL, "Approval type knowledge_document", ""),
    "017": ("alias", "API-083", "Token preference read (namespace differs: CONFLICT-367)", ""),
    "020": ("alias", "API-071", "", ""),
    "021": ("split", "API-072;API-073", "Draft + publish policy version", ""),
    "022": ("split", "API-074;API-076", "Suppression search + consent history", ""),
    "024": ("alias", "API-097", "", ""),
    "026": ("alias", "API-099", "", ""),
    "028": ("alias", "API-124", "", ""),
    "032": ("partial", "API-179", "Expire covered; revise (scope/licence change) missing", "API-ENH-D-001"),
    "035": ("alias", "API-142", "", ""),
    "036": ("none", "", "Eval case (fixture) listing absent; only eval runs exist", "API-ENH-D-002"),
    "040": ("alias", "API-144", "Per-budget pause carried as budget_id in API-144 body", ""),
    "042": ("alias", "API-084", "", ""),
    "043": ("split", "API-085;API-086;API-087", "Verify, fulfil, restrict", ""),
    "044": ("alias", "API-091", "Blueprint allows tightening override only (DEC-028)", ""),
    "048": ("split", "API-129;API-130", "Acknowledge + resolve", ""),
    "049": ("alias", "API-180", "", ""),
    "052": ("alias", "API-181", "", ""),
    "054": ("alias", "API-183", "", ""),
    "057": ("alias", "API-186", "", ""),
    "061": ("alias", "API-189", "", ""),
    "062": ("split", "API-190;API-191", "Merge preview + merge", ""),
    "065": ("partial", "API-047", "Signal taxonomy readable as reference data; no write operation", "API-ENH-D-003"),
    "068": ("alias", "API-192", "", ""),
    "072": ("split", "API-194;API-195", "Draft scoring version + simulate", ""),
    "074": ("alias", "API-196", "", ""),
    "075": ("partial", "API-199", "Per-contact mapping exists; tenant role-mapping rule set missing", "API-ENH-D-004"),
    "077": ("alias", "API-200", "", ""),
    "079": ("alias", "API-197", "", ""),
    "083": ("alias", "API-202", "Research review thresholds = alert/review rule type", ""),
    "084": ("none", "", "No mark-read operation for research alerts (A028)", "API-ENH-D-005"),
    "087": ("split", "API-214;API-217", "Deal detail + timeline", ""),
    "089": ("alias", "API-218", "", ""),
    "090": ("split", "API-219;API-220", "", ""),
    "091": ("alias", "API-216", "", ""),
    "092": ("alias", "API-228", "slug vs id path parameter (CONFLICT-367)", ""),
    "094": ("alias", "API-221", "", ""),
    "095": ("split", "API-222;API-223", "Draft + publish form", ""),
    "099": ("split", "API-446;API-448", "Create workflow + revision", ""),
    "101": ("partial", "API-469;API-450", "Run resume and enable exist; workflow-scope resume after pause missing", "API-ENH-D-006"),
    "102": ("alias", "API-466", "Runs filtered by workflow_id", ""),
    "104": ("alias", "API-255", "", ""),
    "105": ("alias", "API-256", "", ""),
    "106": ("approval", APPROVAL, "Approval type message_draft", ""),
    "107": ("alias", "API-540", "", ""),
    "110": ("partial", "API-252;API-257", "Outbox list and thread exist; single message delivery-status read missing", "API-ENH-D-007"),
    "114": ("alias", "API-257", "", ""),
    "115": ("alias", "API-259", "Handoff = human takeover", ""),
    "116": ("alias", "API-261", "", ""),
    "117": ("alias", "API-262", "", ""),
    "119": ("alias", "API-264", "", ""),
    "120": ("alias", "API-263", "", ""),
    "121": ("alias", "API-268", "", ""),
    "122": ("alias", "API-272", "Token-bound slot read (CONFLICT-367)", ""),
    "125": ("alias", "API-110", "", ""),
    "128": ("alias", "API-265", "", ""),
    "129": ("alias", "API-266", "", ""),
    "130": ("partial", "API-109;API-102", "Template list and health exist; WABA account list missing", "API-ENH-D-008"),
    "131": ("alias", "API-107", "", ""),
    "132": ("alias", "API-108", "", ""),
    "135": ("alias", "API-241", "Threads filtered by channel=whatsapp", ""),
    "138": ("partial", "API-280", "FAQ draft exists; chat enablement and transcript retention settings missing", "API-ENH-D-009"),
    "141": ("alias", "API-283", "", ""),
    "143": ("alias", "API-094", "", ""),
    "145": ("alias", "API-206", "", ""),
    "147": ("alias", "API-299", "", ""),
    "149": ("alias", "API-301", "PATCH vs POST versions (new revision)", ""),
    "151": ("alias", "API-302", "", ""),
    "154": ("alias", "API-113", "", ""),
    "155": ("alias", "API-303", "", ""),
    "159": ("alias", "API-289", "Audit run is a type of SEO task", ""),
    "161": ("alias", "API-308", "", ""),
    "162": ("alias", "API-309", "", ""),
    "163": ("alias", "API-492", "Landing page publication via publications resource", ""),
    "166": ("alias", "API-311", "", ""),
    "169": ("alias", "API-316", "Pause = suspend", ""),
    "172": ("alias", "API-318", "", ""),
    "173": ("alias", "API-319", "", ""),
    "175": ("alias", "API-322", "", ""),
    "176": ("alias", "API-323", "", ""),
    "177": ("alias", "API-326", "", ""),
    "180": ("alias", "API-325", "", ""),
    "183": ("alias", "API-327", "", ""),
    "184": ("approval", APPROVAL, "Approval type referral", ""),
    "185": ("split", "API-334;API-335", "", ""),
    "187": ("approval", APPROVAL, "Approval type proposal_version", ""),
    "188": ("alias", "API-338", "", ""),
    "191": ("alias", "API-343", "", ""),
    "193": ("alias", "API-347", "", ""),
    "194": ("alias", "API-348", "", ""),
    "196": ("alias", "API-358", "Token route vs portal session (CONFLICT-367)", ""),
    "197": ("alias", "API-359", "", ""),
    "198": ("approval", APPROVAL, "Approval type contract_legal", ""),
    "201": ("alias", "API-393", "Payments filtered by deal", ""),
    "202": ("alias", "API-390", "", ""),
    "203": ("alias", "API-409", "Token payment status vs portal invoice (CONFLICT-367)", ""),
    "206": ("split", "API-394;API-395;API-396", "Maker, checker, match", ""),
    "207": ("alias", "API-398", "Source admits portal caller too; blueprint admin only (CONFLICT-366)", ""),
    "210": ("alias", "API-437", "Token onboarding read vs portal session (CONFLICT-367)", ""),
    "212": ("alias", "API-425", "", ""),
    "213": ("alias", "API-427", "", ""),
    "216": ("alias", "API-419", "Partner pilot = pilot with type partner", ""),
    "219": ("alias", "API-429", "", ""),
    "222": ("alias", "API-431", "", ""),
    "224": ("alias", "API-405", "", ""),
    "226": ("split", "API-147;API-148", "", ""),
    "228": ("alias", "API-208", "", ""),
    "230": ("partial", "API-407", "Backtest exists; forecast model settings revision missing", "API-ENH-D-010"),
    "234": ("alias", "API-132", "", ""),
    "236": ("none", "", "No pilot list operation (insurance or partner)", "API-ENH-D-011"),
    "238": ("approval", APPROVAL, "Approval type insurance_pilot", ""),
    "239": ("alias", "API-433", "", ""),
    "241": ("approval", APPROVAL, "Approval type licensing_scope", ""),
    "243": ("approval", APPROVAL, "Approval type deployment_readiness", ""),
    "244": ("alias", "API-435", "", ""),
    "245": ("alias", "API-064", "", ""),
    "247": ("alias", "API-026", "", ""),
    "248": ("alias", "API-027", "", ""),
    "249": ("alias", "API-028", "", ""),
    "250": ("alias", "API-029", "", ""),
    "251": ("alias", "API-030", "", ""),
    "252": ("split", "API-031;API-039", "Capabilities + config revision", ""),
    "253": ("split", "API-020;API-022", "Invite + revoke", ""),
    "254": ("split", "API-024;API-025", "Grant + revoke", ""),
    "255": ("alias", "API-033", "", ""),
    "256": ("alias", "API-034", "", ""),
    "257": ("split", "API-035;API-036;API-037;" + APPROVAL, "validate/apply/retire + approval", ""),
    "258": ("alias", "API-044", "", ""),
    "259": ("alias", "API-045", "", ""),
    "260": ("partial", "API-046", "Verify covered; disable domain mapping missing", "API-ENH-D-012"),
    "261": ("alias", "API-519", "", ""),
    "262": ("split", "API-520;" + APPROVAL, "Draft rate revision + approval plan_version", ""),
    "263": ("alias", "API-521", "", ""),
    "264": ("split", "API-522;API-523;API-524;API-525", "start/change/suspend/cancel", ""),
    "265": ("alias", "API-526", "", ""),
    "266": ("none", "", "Service invoice receipt reconciliation missing (only issue)", "API-ENH-D-013"),
    "267": ("partial", "API-528", "Meters exist; usage charge ledger list missing", "API-ENH-D-014"),
    "268": ("none", "", "Approved credit adjustment to usage charge missing", "API-ENH-D-015"),
    "269": ("alias", "API-453", "", ""),
    "270": ("split", "API-454;API-455", "Generate + dry-run (simulate)", ""),
    "271": ("split", "API-456;API-457;API-458;" + APPROVAL, "start/pause/stop + approval autonomy_plan", ""),
    "272": ("alias", "API-530", "", ""),
    "273": ("split", "API-531;API-534", "Import or export intent", ""),
    "274": ("alias", "API-532", "", ""),
    "275": ("split", "API-536;" + APPROVAL, "cancel/expire + approval import/export", ""),
    "276": ("alias", "API-535", "", ""),
    "277": ("alias", "API-362", "", ""),
    "278": ("alias", "API-363", "", ""),
    "279": ("alias", "API-365", "", ""),
    "280": ("split", "API-366;API-367;API-368;API-369;" + APPROVAL, "decision/submission/withdraw/award + approval", ""),
    "281": ("alias", "API-370", "", ""),
    "282": ("alias", "API-371", "", ""),
    "283": ("alias", "API-373", "", ""),
    "284": ("split", "API-374;API-375;API-376;API-378", "approve/issue/cancel/complete", ""),
    "285": ("alias", "API-377", "", ""),
    "286": ("partial", "API-383;API-384", "Portal acceptance exists; Admin-side acceptance/dispute (buy orders) missing", "API-ENH-D-016"),
    "287": ("alias", "API-549", "", ""),
    "288": ("split", "API-550;API-552", "read=acknowledge; archive", ""),
    "289": ("alias", "API-290", "New commercial public path vs legacy path (CONFLICT-360)", ""),
    "290": ("alias", "API-486", "", ""),
    "291": ("split", "API-487;API-488", "", ""),
    "292": ("split", "API-489;API-490;API-492;API-494;API-495;" + APPROVAL, "action enum split", ""),
    "293": ("alias", "API-227", "", ""),
    "294": ("none", "", "External grant revoke/expire/rotate missing", "API-ENH-D-017"),
    "295": ("alias", "API-013", "Invite redemption inside registration", ""),
    "296": ("alias", "API-235", "", ""),
    "297": ("partial", "API-236", "Status read exists; explicit complete-upload action missing", "API-ENH-D-018"),
    "298": ("alias", "API-436", "", ""),
    "299": ("split", "API-354;API-355", "", ""),
    "300": ("split", "API-356;API-357", "accept / request_revision", ""),
    "301": ("alias", "API-382", "", ""),
    "302": ("split", "API-440;API-069", "support/feedback/renewal case; privacy routed separately", ""),
}
# Adapters
A = {
    "016": ("partial", "AD-20", "Malware scan covered; object storage + text extraction port not catalogued", "AD-D01"),
    "037": ("split", "AD-13;AD-14", "", ""),
    "055": ("split", "AD-05;AD-06", "", ""),
    "058": ("alias", "AD-07", "", ""),
    "076": ("alias", "AD-19", "", ""),
    "080": ("partial", "AD-19", "Enrichment covered; dedicated contact verification port (email deliverability check) missing", "AD-D02"),
    "111": ("alias", "AD-01", "Resend alternative (DEC-025)", ""),
    "126": ("split", "AD-03;AD-04", "", ""),
    "136": ("alias", "AD-02", "", ""),
    "146": ("alias", "AD-08", "Read permitted organizational signals", ""),
    "156": ("alias", "AD-08", "Postiz self-host option (CONFLICT-371)", ""),
    "160": ("partial", "AD-17", "Search Console covered; owned-site technical audit crawler not catalogued", "AD-D03"),
    "174": ("alias", "AD-09", "", ""),
    "181": ("alias", "AD-18", "", ""),
    "200": ("alias", "AD-10", "Provider shortlist differs (CONFLICT-371)", ""),
    "208": ("alias", "AD-11", "", ""),
    "235": ("split", "AD-15;AD-16;API-133", "CI evidence via API-133", ""),
}
C = {
    "SM-UX-API-01": ("alias", "API-501", "", ""),
    "SM-UX-API-02": ("split", "API-503;API-505;API-506", "Start, verify e-mail, submit", ""),
    "SM-UX-API-03": ("partial", "API-507", "Status read only; applicant draft configuration read missing", "API-ENH-D-019"),
    "SM-UX-API-04": ("split", "API-504;API-509", "", ""),
    "SM-UX-API-05": ("alias", "API-511", "", ""),
    "SM-UX-API-06": ("split", "API-513;API-514;API-515", "", ""),
    "SM-UX-API-07": ("partial", "API-516;API-517;API-440", "support/plan_change/export covered; offboarding request kind missing", "API-ENH-D-020"),
    "SM-UX-API-08": ("alias", "API-459", "", ""),
    "SM-UX-API-09": ("alias", "API-460", "", ""),
    "SM-UX-API-10": ("split", "API-464;API-465;" + APPROVAL, "approve/enable/disable", ""),
    "SM-UX-API-11": ("alias", "API-466", "", ""),
    "SM-UX-API-12": ("alias", "API-473", "", ""),
    "SM-UX-API-13": ("split", "API-475;API-476", "hold/select/cancel + escalate", ""),
    "SM-UX-API-14": ("alias", "API-038", "", ""),
    "SM-UX-API-15": ("alias", "API-039", "", ""),
    "SM-UX-API-16": ("split", "API-041;API-042;API-043;" + APPROVAL, "simulate/activate(schedule)/rollback + approval", ""),
    "SM-UX-API-17": ("alias", "API-477", "", ""),
    "SM-UX-API-18": ("partial", "API-479;API-480", "Clone/configure exist; create template from scratch missing", "API-ENH-D-021"),
    "SM-UX-API-19": ("split", "API-481;API-482;" + APPROVAL, "test/deprecate + approval workflow_template (publish = approval effect)", ""),
}

bp = {b["id"]: b for b in d["bpops"]}


def norm(p):
    if not p.startswith("/api/v1"):
        p = "/api/v1" + p
    return re.sub(r"\{[^}]+\}", "{x}", p)


idx = {}
for b in d["bpops"]:
    idx.setdefault((b["method"], norm(b["full"])), []).append(b["id"])

BOUND_NS = {"Admin": {"admin"}, "Portal": {"portal", "public+portal"}, "Public": {"public", "public+portal"},
            "Provider callback": {"hooks"}, "Internal worker": {"internal"},
            "Authentication (separate audience)": {"bff", "admin+portal", "bff-admin", "bff-web", "admin"},
            "Portal + Admin (separate policy/DTO)": {"admin+portal"}}

rows = []
for o in d["ops"]:
    n = o["num"]
    f = o["fields"]
    if o["method"] == "ADAPTER":
        rel, ops, note, enh = A[n]
    else:
        k = (o["method"], norm(o["path"]))
        if k in idx:
            rel, ops, note, enh = "exact", ";".join(idx[k]), "Legacy path retained (★)" if bp[idx[k][0]]["star"] else "Same path", ""
        else:
            rel, ops, note, enh = M[n]
    status = {"exact": "Covered", "alias": "Covered", "split": "Covered", "approval": "Covered",
              "partial": "Partially covered", "none": "Not covered"}[rel]
    first = ops.split(";")[0] if ops else ""
    ns = bp[first]["ns"] if first in bp else ""
    ns_conflict = ""
    if first in bp and o["boundary"] in BOUND_NS and ns not in BOUND_NS[o["boundary"]]:
        ns_conflict = f'{o["boundary"]} vs {ns}'
    rows.append({
        "source_id": "SM-OP-" + n, "sit_id": o["sit_id"], "method": o["method"], "path": o["path"],
        "boundary": o["boundary"], "interface_type": f.get("Interface type", "Website/portal addition"),
        "module": f.get("Module", ""), "purpose": f.get("Purpose", ""), "contract_kind": o["contract_kind"],
        "req_fields": ";".join(x["name"] + ":" + x["type"] + ("[" + x["enum"] + "]" if x["enum"] else "") + ("" if x["required"] else "?") for x in o["req_fields"]),
        "res_fields": ";".join(x["name"] + ":" + x["type"] + ("[" + x["enum"] + "]" if x["enum"] else "") + ("" if x["required"] else "?") for x in o["res_fields"]),
        "proposed_status": o["proposed_status"], "tables": f.get("Tables", f.get("PostgreSQL entities", "")),
        "integration": f.get("Integration", ""), "allocation": f.get("Allocation", ""),
        "relation": rel, "blueprint_ops": ops, "blueprint_ns": ns, "ns_conflict": ns_conflict,
        "status": status, "note": note, "enhancement": enh,
        "field_contract": "Added in Part 3.5 §3.5.5.3" if o["contract_kind"] in ("explicit_dto", "public_allowlist", "cursor_list") else ("Added in Part 3.5 §3.5.5.4 (SRC07-DEC)" if o["contract_kind"] == "review_required" else "Adapter contract §3.5.5.6"),
        "test": "TC-ENH-D-" + n,
        "sit_assertion": o["sit_assertion"],
    })
for c in d["cands"]:
    rel, ops, note, enh = C[c["id"]]
    status = {"alias": "Covered", "split": "Covered", "partial": "Partially covered", "none": "Not covered"}[rel]
    first = ops.split(";")[0]
    rows.append({
        "source_id": c["id"], "sit_id": "", "method": c["method"], "path": c["path"], "boundary": c["audience"],
        "interface_type": "Candidate HTTP", "module": c["screen"], "purpose": c["title"],
        "contract_kind": "candidate_schema", "req_fields": c["req_schema"][:400], "res_fields": c["res_schema"][:400],
        "proposed_status": c["success"], "tables": c["entities"], "integration": "", "allocation": "",
        "relation": rel, "blueprint_ops": ops, "blueprint_ns": bp[first]["ns"] if first in bp else "",
        "ns_conflict": "", "status": status, "note": note, "enhancement": enh,
        "field_contract": "Added in Part 3.5 §3.5.5.5", "test": "TC-ENH-D-C" + c["id"][-2:],
        "sit_assertion": c["control"],
    })

with open(sys.argv[2], "w", newline="", encoding="utf-8") as fh:
    w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
    w.writeheader()
    w.writerows(rows)
json.dump(rows, open(sys.argv[3], "w"), indent=1, ensure_ascii=False)

from collections import Counter
print("rows", len(rows))
print(Counter(r["relation"] for r in rows))
print(Counter(r["status"] for r in rows))
print("ns conflicts", [(r["source_id"], r["ns_conflict"], r["blueprint_ops"]) for r in rows if r["ns_conflict"]])
used = set()
for r in rows:
    for x in r["blueprint_ops"].split(";"):
        if x.startswith("API-"):
            used.add(x)
print("distinct blueprint ops referenced", len(used), "of", len(d["bpops"]))
star_unused = [b["id"] for b in d["bpops"] if b["star"] and b["id"] not in used]
print("star ops not referenced", star_unused)
json.dump(sorted(used), open(sys.argv[3] + ".used", "w"))
