#!/usr/bin/env python3
"""Group H generator: builds mapping CSVs, the coverage CSV and Markdown table fragments
for Part 6.9 (Source Pack QC, RTM and Backlog Reconciliation).
Usage: python3 -I H_generate.py <parsed.json> <bp.json> <blueprint_dir> <frag_dir>
"""
import csv, json, re, sys, collections
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import H_maps as MP  # noqa: E402

P = json.load(open(sys.argv[1], encoding="utf-8"))
B = json.load(open(sys.argv[2], encoding="utf-8"))
BP = Path(sys.argv[3]); FR_DIR = Path(sys.argv[4]); FR_DIR.mkdir(parents=True, exist_ok=True)
COV = BP / "final" / "coverage"; COV.mkdir(parents=True, exist_ok=True)
ST = {"C": "Covered", "P": "Partially covered", "N": "Not covered", "X": "Conflict", "NA": "Not applicable"}
cov_rows = []  # doc, section, aspect_id, summary, status, location, action, new_ids

def cov(doc, sec, aid, summ, status, loc, action, new=""):
    cov_rows.append([doc, sec, aid, summ.replace("\n", " ")[:300], status, loc, action, new])

def wcsv(name, header, rows):
    with open(COV / name, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f); w.writerow(header); w.writerows(rows)

def md_table(header, rows):
    out = ["| " + " | ".join(header) + " |", "|" + "---|" * len(header)]
    for r in rows:
        out.append("| " + " | ".join(str(c).replace("|", "/").replace("\n", " ") for c in r) + " |")
    return "\n".join(out) + "\n"

def frag(name, text):
    (FR_DIR / f"{name}.md").write_text(text, encoding="utf-8")

def pts(s):
    m = re.findall(r"(\d+(?:\.\d+)?)", s or "")
    if not m: return 0.0
    a = [float(x) for x in m[:2]]
    return sum(a) / len(a)

stories, frst, sprint = B["stories"], B["fr_stories"], B["story_sprint"]
def story_list(ids):
    return ", ".join(sorted(set(ids)))
def sprints_of(ids):
    s = sorted({sprint.get(i, "spill/W6") for i in ids}, key=lambda x: (len(x), x))
    return ", ".join(s)

# =========================================================== 1. BR map (76)
normbr = lambda x: "BR-" + x.replace("B-", "")
src_br = sorted({b for r in P["rtm"] for b in r["brs"]} | {r["br"] for r in P["nonscreen"]},
                key=lambda x: (x[0] != "M", x))
bpname = {v["name"].lower(): k[3:] for k, v in B["br"].items() if k.startswith("BR-M")}
name2m = {m["module"]: bpname[m["module"].lower()] for m in P["modules"]}
mods = {int(name2m[m["module"]][1:]): m for m in P["modules"]}
br_rows, br_md = [], []
for i in range(1, 67):
    mid = "M%02d" % i; bid = "BR-" + mid; bp = B["br"].get(bid)
    m = mods[i]
    dep_src = sorted({name2m.get(d.strip(), d.strip()) for d in m["dependency"].split(";") if d.strip()})
    dep_bp = sorted(set(re.findall(r"M\d\d", bp["dependency"]))) if bp else []
    dep_src_m = [d for d in dep_src if re.match(r"M\d\d", d)]
    same = set(dep_src_m) == set(dep_bp)
    status = "C" if bp and same else ("P" if bp else "N")
    note = "Dependencies match" if same else f"Source deps {';'.join(dep_src) or '—'} vs blueprint {';'.join(dep_bp) or '—'}"
    in_rtm = mid in src_br
    br_rows.append([mid, bid, m["module"] + f" (seq {m['seq']})", m["acceptance"], ";".join(dep_src), ";".join(dep_bp), bp["epic"] if bp else "", bp["wave"] if bp else "", ST[status], note, "yes" if in_rtm else "no"])
    cov("24/20", "BR register / module backlog", mid, f"{m['module']}: {m['acceptance']}", ST[status], f"Part 1 {bid} ({bp['epic'] if bp else ''})", "Mapped; dependency compared" + ("" if same else "; difference recorded (§6.9.5.4.5)"))
for x in ["B-TENANT", "B-WEB", "B-AUTO", "B-SVC", "B-QA"]:
    bid = normbr(x); bp = B["br"][bid]
    br_rows.append([x, bid, bp["name"], bp["acceptance"], "", bp["dependency"], bp["epic"], bp["wave"], "Covered", "Cross-cutting BR present in Part 1", "yes"])
    cov("24/01", "BR register", x, bp["name"], "Covered", f"Part 1 {bid}", "Mapped 1:1")
for k in range(1, 6):
    br_rows.append([f"XBR-0{k} (unnumbered)", "BR-S138", ["Dynamic startup/tenant onboarding", "Independent SaaS clients", "Multiple scoped business objectives", "No new core code per ordinary startup", "Measure verified outcomes, not message volume"][k-1], "Doc 38 counts 5 added BRs without IDs", "", "", "EP-20/EP-18", "W5", "Partially covered", "[GAP-440] [ASSUMPTION-441] interpreted as the five BRD §17.1 scope statements", "no"])
    cov("38/24", "BR count 76 = 71 + 5", f"XBR-0{k}", "Expansion business requirement counted in doc 38 but not enumerated", "Partially covered", "Part 1 BR-S138", "Interpreted and mapped [GAP-440]", f"XBR-0{k}")
wcsv("H_br_map.csv", ["source_br", "blueprint_br", "name", "source_acceptance", "source_dependencies", "blueprint_dependencies", "epic", "wave", "status", "note", "cited_in_doc24_rtm"], br_rows)
br_diff = [r for r in br_rows[:66] if r[8] != "Covered"]
frag("br_diff", md_table(["Source BR", "Module", "Source dependencies (doc 20)", "Blueprint dependencies (Part 1)", "Epic", "Proposed handling"],
     [[r[0], r[2], r[4] or "—", r[5] or "—", r[6], "Keep Part 1 (DEC-034 order); add source edge as soft dependency in Part 8.1 critical-path review"] for r in br_diff]))

# =========================================================== 2. FR map (288) + RTM trace rows
fr_rows, fr_md, sit_alias = [], [], collections.defaultdict(set)
mism = []
for i, r in enumerate(P["rtm"]):
    fr = "FR-" + r["fr"][6:]; bpf = B["fr"].get(fr); fs = frst.get(fr, {})
    src = {normbr(x) for x in r["brs"]}
    bpbr = set(re.findall(r"BR-(?:M\d\d|TENANT|WEB|AUTO|SVC|QA)", bpf["traces"])) if bpf else set()
    missing = sorted(src - bpbr)
    status = "Covered" if bpf and not missing else ("Conflict" if bpf else "Not covered")
    if missing: mism.append((fr, sorted(src), sorted(bpbr), missing))
    for s in r["sit"]: sit_alias[s].add(fr)
    st = fs.get("stories", [])
    fr_rows.append([r["fr"], fr, r["screen"], r["title"], r["access"], ";".join(r["brs"]), ";".join(sorted(bpbr)), ";".join(missing),
                    ";".join(r["ops"]), ";".join(r["entities"]), ";".join(r["unit"]), ";".join(r["sit"]), ";".join(r["uat"]),
                    story_list(st), fs.get("tc_total", ""), bpf["wave_epic"] if bpf else "", status, "SM-FR alias of blueprint FR (Part 0 §0.4; DEC-017)"])
    fr_md.append([r["fr"], fr, r["title"][:44], ";".join(r["brs"]), "+" + ",".join(m[3:] for m in missing) if missing else "=",
                  len(r["sit"]), r["uat"][0], ", ".join(x[3:] for x in st), fs.get("tc_total", ""), status])
    cov("24", f"RTM row {r['screen']}", r["fr"], f"{r['title']}: {r['implement'][:160]}", status, f"Part 2.1 {fr}; Part 6.6 §6.6.4",
        "Alias confirmed; BR traces compared" + (f"; add {', '.join(missing)} [CONFLICT-447]" if missing else ""), "")
for r in P["nonscreen"]:
    fr = "FR-" + r["fr"][6:]; bpf = B["fr"][fr]; fs = frst[fr]
    bpbr = set(re.findall(r"BR-(?:M\d\d|TENANT|WEB|AUTO|SVC|QA)", bpf["traces"]))
    ok = normbr(r["br"]) in bpbr
    for s in r["sit"]: sit_alias[s].add(fr)
    fr_rows.append([r["fr"], fr, "—", r["op"], "Internal", r["br"], ";".join(sorted(bpbr)), "" if ok else normbr(r["br"]), r["op"].split(" ")[0] + " " + r["op"].split(" ")[1], "", ";".join(r["unit"]), ";".join(r["sit"]), "", story_list(fs["stories"]), fs["tc_total"], bpf["wave_epic"], "Covered" if ok else "Partially covered", "Non-screen operation"])
    fr_md.append([r["fr"], fr, r["op"][:44], r["br"], "=" if ok else "+" + r["br"], len(r["sit"]), "—", ", ".join(x[3:] for x in fs["stories"]), fs["tc_total"], "Covered" if ok else "Partial"])
    cov("24", "Non-screen requirement", r["fr"], r["op"], "Covered" if ok else "Partially covered", f"Part 2.1 {fr}", "Alias confirmed; monitoring-only exposure verified by US-2102 / US-0401")
for u in P["ux_fr"]:
    fr = "FR-" + u["screen"]; bpf = B["fr"].get(fr); fs = frst.get(fr, {})
    fr_rows.append([u["fr"], "FR-UX-" + u["screen"] + " (field spec of " + fr + ")", u["screen"], bpf["title"] if bpf else "", "", "", "", "", "", "", "", "", u["uat"],
                    story_list(fs.get("stories", [])), fs.get("tc_total", ""), bpf["wave_epic"] if bpf else "", "Covered" if bpf else "Not covered",
                    "SM-UX-FR = screen field/automation spec; Part 0 alias FR-UX-*; key fields in Part 2.1 §2.4 and Part 2.5 §2.43"])
    cov("24", "Expansion traceability (SM-UX-FR)", u["fr"], f"Field and journey spec for {u['screen']}; UAT {u['uat']} {u['status']}", "Covered" if bpf else "Not covered",
        f"Part 0 §0.4 FR-UX-{u['screen']}; Part 2.1 {fr} key fields; Part 2.5 §2.43", "Alias confirmed; field-level reconciliation owned by the doc 06/17 review")
wcsv("H_fr_map.csv", ["source_fr", "blueprint_fr", "screen", "title", "access", "source_brs", "blueprint_brs", "source_brs_missing_in_blueprint", "source_operations", "source_entities", "source_unit", "source_sit", "source_uat", "blueprint_stories", "blueprint_tc_total", "wave_epic", "status", "note"], fr_rows)
frag("fr_table", md_table(["Source FR", "Blueprint FR", "Interface", "Source BR", "BR check", "# SIT", "UAT alias", "Stories (US-)", "# TC", "Status"], fr_md))
frag("br_mismatch", md_table(["FR", "Source BR (doc 24)", "Blueprint traces (Part 2.1)", "Missing in blueprint", "Proposed resolution"],
     [[a, ", ".join(b), ", ".join(c), ", ".join(d), "Add as secondary trace in the Part 2.1 errata batch; no scope change"] for a, b, c, d in mism]))
# SIT alias register
sit_rows = []
for s in sorted(sit_alias):
    frs = sorted(sit_alias[s]); st = sorted({x for f in frs for x in frst.get(f, {}).get("stories", [])})
    sit_rows.append([s, ";".join(frs), story_list(st), "TCs of the listed stories that carry the FR in their Links cell (Part 6.6 §6.6.4)"])
wcsv("H_sit_alias_map.csv", ["sm_sit_id", "blueprint_frs", "blueprint_stories", "alias_rule"], sit_rows)
for s in sit_rows:
    cov("24", "SIT association", s[0], f"SIT case cited for {s[1]}", "Partially covered", f"Part 6.6 rows {s[1]}", "FR-level alias added here (§6.9.5.3.2); operation-level TC mapping in Part 6.8 (G_test_mapping.csv) [GAP-442]", s[0])
multi = sum(1 for s in sit_rows if ";" in s[1])
frag("sit_summary", md_table(["Metric", "Value"], [["Distinct SM-SIT IDs cited in doc 24", len(sit_rows)], ["Cited by exactly one FR", len(sit_rows) - multi], ["Cited by two or more FRs (shared operations)", multi],
     ["Cited by most FRs", max(sit_rows, key=lambda r: r[1].count(";"))[0] + " (" + str(max(r[1].count(";") for r in sit_rows) + 1) + " FRs)"], ["Already aliased in Part 6.6 / final/RTM.csv", 0]]))

# =========================================================== 3. QC map (245)
L = MP.LAYER
qc_rows, qc_md = [], []
for k, q in P["qc"].items():
    st, refs, note = MP.QC[k]
    lay = q["layer"]; anchors, role, gate, qcl = L[lay]
    qc_rows.append([k, qcl, lay, q["title"], q["acceptance"], q["priority"], q["owner"], q["reviewer"], role, gate, refs, anchors, q["command"], q["evidence"], ST[st], note])
    qc_md.append([k, qcl, q["title"][:60], q["priority"], role, refs, gate, ST[st] + (f": {note}" if note and st != "C" else "")])
    cov("23", f"QC layer {lay}", k, f"{q['title']}: {q['acceptance'][:150]}", ST[st], f"{refs}; register §6.9.5.1.8",
        "Mapped; QC register row, owner, evidence path and gate added" + (f"; {note}" if st != "C" else ""), f"{qcl}; {k}")
wcsv("H_qc_map.csv", ["qc_id", "layer_id", "layer", "check", "acceptance", "priority", "source_owner", "source_reviewer", "blueprint_signoff_role", "blueprint_gate", "blueprint_verification_refs", "layer_anchor_refs", "source_command_template", "evidence_path", "status", "note"], qc_rows)
frag("qc_table", md_table(["QC", "Layer", "Check", "Prio", "Blueprint sign-off role", "Blueprint verification", "Gate", "Status"], qc_md))
lay_cnt = collections.OrderedDict()
for k, q in P["qc"].items():
    d = lay_cnt.setdefault(q["layer"], collections.Counter()); d["n"] += 1; d[q["priority"]] += 1; d[MP.QC[k][0]] += 1
frag("qc_layers", md_table(["Layer ID", "Layer (doc 23)", "Checks", "Critical", "High", "Covered", "Partial / Conflict / Not", "Blueprint anchors", "Sign-off role", "Signed at"],
     [[L[l][3], l, c["n"], c["Critical"], c["High"], c["C"], c["P"] + c["X"] + c["N"], L[l][0], L[l][1], L[l][2]] for l, c in lay_cnt.items()]))
qc_np = [[k, P["qc"][k]["layer"], P["qc"][k]["title"], ST[MP.QC[k][0]], MP.QC[k][1], MP.QC[k][2]] for k in P["qc"] if MP.QC[k][0] != "C"]
frag("qc_partial", md_table(["QC", "Layer", "Check", "Status", "Blueprint location", "Gap and action"], qc_np))
# mandatory gates
okpi = {"Successful unauthorized cross-tenant access": "OKPI-01", "Successful Website-to-Admin access": "OKPI-02", "Unresolved critical security findings": "OKPI-03",
        "Exposed live secrets": "OKPI-04", "Initial dashboard p95": "OKPI-05", "Duplicate financial side effects": "OKPI-07", "Duplicate external message execution": "OKPI-08",
        "Unapproved paid provider calls": "OKPI-11", "Unauthorized budget overspend": "OKPI-12", "Mandatory regression pass rate": "OKPI-16", "Mandatory QC completion": "OKPI-17",
        "Critical RPO": "OKPI-18", "Initial critical RTO": "OKPI-19", "Approved traceability mappings": "OKPI-20", "Verified transaction reconciliation": "OKPI-22",
        "Applicable accessibility criteria passed": "OKPI-23", "Growth dashboard p95": "OKPI-26", "Async acknowledgement p95": "OKPI-27", "Projection refresh": "OKPI-28",
        "Growth critical RTO": "OKPI-32", "Disallowed dispatch or formal offer": "OKPI-35"}
gmap = {"OKPI-01": ("C", "NFR-032; GL-S04"), "OKPI-02": ("C", "NFR-001; QC-079"), "OKPI-03": ("C", "NFR-067; GL-S01…S03"), "OKPI-04": ("C", "NFR-068"),
        "OKPI-05": ("C", "Part 4.2 C10 (p95 800 ms)"), "OKPI-07": ("C", "NFR-005; AP-04"), "OKPI-08": ("C", "NFR-005, NFR-066"), "OKPI-11": ("C", "NFR-037"), "OKPI-12": ("C", "NFR-014"),
        "OKPI-16": ("C", "RBR-5; GL-T02"), "OKPI-17": ("P", "No QC register in blueprint → §6.9.5.1"), "OKPI-18": ("C", "NFR-056; DEC-018"), "OKPI-19": ("C", "NFR-057; DEC-079"),
        "OKPI-20": ("X", "AP-08 10% spot check [CONFLICT-442]"), "OKPI-22": ("C", "AP-04; NFR-035"), "OKPI-23": ("C", "NFR-088/089"), "OKPI-26": ("P", "Year 2 profile differs [CONFLICT-441]"),
        "OKPI-27": ("C", "NFR-051"), "OKPI-28": ("X", "NFR-047 15 min [CONFLICT-443]"), "OKPI-32": ("X", "No 2 h growth RTO [CONFLICT-444]"), "OKPI-35": ("C", "BLK-7; KPI-17")}
g_md = []
for g in P["qc_mandatory_gates"]:
    o = okpi[g[0]]; s, ref = gmap[o]
    g_md.append([o, g[0], g[1], g[2], ref, ST[s]])
    cov("23", "Mandatory measurable gates", o, f"{g[0]} {g[1]} ({g[2]})", ST[s], ref, "Bound to the combined preflight (§6.9.5.6)")
frag("gates", md_table(["OKPI", "Metric", "Target", "Verification context", "Blueprint", "Status"], g_md))
for l in P["qc_layers"]:
    pass

# =========================================================== 4. Decisions (352)
dec_rows, dec_md = [], []
op2fr = collections.defaultdict(set)
for r in P["rtm"]:
    for o in r["ops"]: op2fr[o].add("FR-" + r["fr"][6:])
for r in P["nonscreen"]:
    op2fr[" ".join(r["op"].split(" ")[:2])].add("FR-" + r["fr"][6:])
scr2fr = {r["screen"]: "FR-" + r["fr"][6:] for r in P["rtm"]}
for d in P["decisions"]:
    n = int(d["id"][4:]); sp = "SPDEC-%03d" % n
    if n <= 5:
        cls, res, st = "Exact API contract (identity reuse)", "DEC-019, DEC-003; US-0101 12-check spike; Part 3.2 BFF rows", "C"
        frs = sorted(op2fr.get(d["subject"].strip(), []))
    elif n <= 38:
        frs = sorted(op2fr.get(d["subject"].strip(), []))
        cls, res, st = "Exact API contract", f"DEC-015 derived contract; Part 3.2 rows for {', '.join(frs) or 'see op'}; approval record §6.9.5.2", "P"
    elif n <= 41:
        frs = ["FR-A001", "FR-A002"]; cls, res, st = "Database reuse confirmation (identity)", "DEC-019; Part 3.3 identity mapping; QC-112", "C"
    elif n == 42:
        frs = ["FR-A006", "FR-OP001"]; cls, res, st = "Database field confirmation (embedding)", "DEC-088 provisional dimension; DEC-042", "C"
    else:
        scr = d["subject"].split(" / ")[0].strip(); frs = [scr2fr.get(scr, "")]
        cls, res, st = "UI semantic mapping approval", f"{frs[0]}; AP-08; Part 6.6 §6.6.8.2; 100% approval [CONFLICT-442]", "P"
    dec_rows.append([d["id"], sp, cls, d["subject"], d["source_doc"], ";".join(frs), d["source_requirement"][:200], d["proposed"][:240], d["owner"].replace("Owner:", "").strip()[:80], res, ST[st]])
    dec_md.append([sp, d["subject"][:48], cls.split(" (")[0], ", ".join(frs), res[:90], ST[st]])
    cov(d["source_doc"], "Engineering decision", d["id"], f"{d['subject']}: {d['proposed'][:150]}", ST[st], res, f"Aliased as {sp}; decision record and queue (§6.9.5.2)", sp)
# expansion decisions
for u in P["ux_fr"]:
    fr = "FR-" + u["screen"]; xid = "SPDEC-X-" + u["screen"]
    dec_rows.append(["(unnumbered)", xid, "Expansion field decision (FRD §16.2 add/standardize/remove)", f"{u['screen']} field set", "06/17/24", fr, "Current declared fields / add or standardize / remove or replace", "Adopt standardized field set", "Product owner + technical lead", f"Part 2.1 {fr} Key fields column (binding); Part 2.5 §2.43", "Covered"])
    cov("38/24", "Expansion decisions", xid, f"Field decision for {u['screen']}", "Covered", f"Part 2.1 {fr}", "Mapped [ASSUMPTION-440]", xid)
uxapi = [("01", "W31", "Published plans", "FR-W31"), ("02", "W32", "Register client application", "FR-W32"), ("03", "W33", "Read own configuration draft", "FR-W33"), ("04", "W33", "Save configuration draft", "FR-W33"),
         ("05", "W33", "Submit draft for review", "FR-W33"), ("06", "W34", "Own service overview", "FR-W34"), ("07", "W34", "Request support, plan change or export", "FR-W34"), ("08", "A109", "List scoped triggers", "FR-A109"),
         ("09", "A109", "Create trigger revision", "FR-A109"), ("10", "A109", "Approve, enable or disable trigger", "FR-A109"), ("11", "A110", "List scoped concurrent executions", "FR-A110"), ("12", "A111", "List workflow conflicts", "FR-A111"),
         ("13", "A111", "Resolve or hold competing actions", "FR-A111"), ("14", "A112", "List configuration revisions", "FR-A112"), ("15", "A112", "Propose configuration revision", "FR-A112"),
         ("16", "A112", "Simulate, approve, activate or rollback configuration", "FR-A112"), ("17", "A113", "List entitled automation templates", "FR-A113"), ("18", "A113", "Create template revision", "FR-A113"), ("19", "A113", "Test, approve, publish or deprecate template", "FR-A113")]
for n, scr, purp, fr in uxapi:
    xid = f"SPDEC-X-API-{n}"
    dec_rows.append(["(unnumbered)", xid, "Candidate HTTP operation approval", f"SM-UX-API-{n} {purp}", "38/06", fr, purp, "Reuse or approve contract", "Backend lead + product owner", f"DEC-015; Part 3.2 §3.2.2.4 rows for {fr}", "Covered"])
    cov("38", "Candidate operations", f"SM-UX-API-{n}", f"{scr} {purp}", "Covered", f"Part 3.2 rows for {fr}", "Mapped; contract reconciliation owned by the doc 07 review", xid)
ents = [("sales_ui_application", "ENT-187 ApplicationDraft", "Covered"), ("sales_ui_config_revision", "ENT-168 ConfigRevision", "Covered"), ("sales_ui_trigger_revision", "ENT-161 Trigger (revisioned via ENT-160 WorkflowRevision)", "Partially covered"),
        ("sales_ui_conflict", "ENT-165 ConflictCase", "Covered"), ("sales_ui_template_revision", "ENT-166 NodeTemplate / ENT-167 WorkflowTemplate", "Partially covered"), ("sales_ui_service_request", "— (no SaaS service request entity)", "Not covered")]
for e, m, s in ents:
    xid = "SPDEC-X-ENT-" + e.replace("sales_ui_", "")
    dec_rows.append(["(unnumbered)", xid, "Candidate entity approval", e, "38/08", "", "", "Reuse or migrate", "Database lead", f"Part 3.3 {m}", s])
    cov("38", "Candidate entities", e, f"Candidate entity {e}", s, f"Part 3.3 {m}", "Mapped" + ("; GAP-448 entity proposed §6.9.5.7" if s == "Not covered" else ("; revision versioning note §6.9.5.7" if s.startswith("Partially") else "")), xid)
wcsv("H_decision_map.csv", ["source_id", "alias", "class", "subject", "source_doc", "blueprint_frs", "source_requirement", "proposed_resolution", "source_owner", "blueprint_resolution", "status"], dec_rows)
frag("dec_table", md_table(["Alias", "Subject", "Class", "FR", "Blueprint resolution", "Status"], dec_md))
dc = collections.Counter((r[2].split(" (")[0], r[10]) for r in dec_rows)
classes = collections.OrderedDict()
for r in dec_rows:
    c = r[2].split(" (")[0]; classes.setdefault(c, collections.Counter())[r[10]] += 1
frag("dec_summary", md_table(["Decision class", "Source IDs", "Count", "Covered", "Partial", "Not covered", "Blueprint home"],
     [[c, {"Exact API contract": "DEC-001…038 (doc 07)", "Database reuse confirmation": "DEC-039…041 (doc 08)", "Database field confirmation": "DEC-042 (doc 08)", "UI semantic mapping approval": "DEC-043…180 (doc 24)",
           "Expansion field decision": "147 unnumbered (FRD §16.2)", "Candidate HTTP operation approval": "SM-UX-API-01…19", "Candidate entity approval": "6 candidate entities"}.get(c, ""),
       sum(v.values()), v["Covered"], v["Partially covered"], v["Not covered"],
       {"Exact API contract": "DEC-015, DEC-019; Part 3.2", "Database reuse confirmation": "DEC-019; Part 3.3", "Database field confirmation": "DEC-088", "UI semantic mapping approval": "AP-08; Part 6.6",
        "Expansion field decision": "Part 2.1 key fields; Part 2.5", "Candidate HTTP operation approval": "DEC-015; Part 3.2", "Candidate entity approval": "DEC-016, DEC-084; Part 3.3"}.get(c, "")] for c, v in classes.items()]
     + [["**Total**", "", len(dec_rows), sum(v["Covered"] for v in classes.values()), sum(v["Partially covered"] for v in classes.values()), sum(v["Not covered"] for v in classes.values()), ""]]))

# =========================================================== 5. Work items (162) -> stories
wi_rows, wi_md = [], []
for t in P["tasks"] + P["uxtasks"]:
    tid = t["id"]
    m = re.match(r"(?:UX-)?TASK-([WA]\d+|OP\d+)$", tid)
    if m and not tid.startswith("UX-TASK-") or (tid.startswith("UX-TASK-") and re.match(r"UX-TASK-[WA]\d+$", tid)):
        key = tid.split("-")[-1]
        fr = "FR-" + key
        st = frst.get(fr, {}).get("stories", [])
        status, note = ("Covered", "Via FR → story trace (Part 6.6 §6.6.4)") if st else ("Not covered", "")
    else:
        fr = ""; st = MP.TASK_STORY.get(tid, [])
        note = MP.TASK_NOTE.get(tid, "Mapped by scope")
        status = "Partially covered" if tid in MP.TASK_NOTE else ("Covered" if st else "Not covered")
    sp = sum(pts(stories[s]["points"]) for s in st if s in stories)
    wi_rows.append([tid, t["title"], ";".join(t["pred"]), t["low"], t["base"], t["high"], t.get("owner", ""), fr, story_list(st), round(sp, 1), round(sp * 0.7, 1), sprints_of(st) if st else "", status, note])
    wi_md.append([tid, t["title"][:46], f"{t['low']:g}/{t['base']:g}/{t['high']:g}", fr or "—", ", ".join(s[3:] for s in st), sprints_of(st) if st else "—", status if status == "Covered" else status + ": " + note.split(": ", 1)[-1][:70]])
    cov("20", "Task register" if tid.startswith("TASK") else "Expansion backlog", tid, f"{t['title']} ({t['low']:g}/{t['base']:g}/{t['high']:g} PD; preds {';'.join(t['pred'])})", status,
        f"Part 5 {story_list(st)}; Part 8.1 §8.1.4.6", "Mapped to stories" + (f"; {note}" if status != "Covered" else ""), "")
wcsv("H_workitem_story_map.csv", ["work_item", "title", "predecessors", "low_pd", "base_pd", "high_pd", "source_owner", "blueprint_fr", "blueprint_stories", "stories_sp_mid_total", "stories_pd_central", "sprints", "status", "note"], wi_rows)
frag("wi_table", md_table(["Work item", "Title", "PD L/B/H", "FR", "Stories (US-)", "Sprints", "Status"], wi_md))
frag("wi_summary", md_table(["Metric", "Source (doc 20)", "Blueprint", "Note"], [
    ["Work items", "149 + 13 = 162", f"{len(stories)} stories (Part 5); 205 scheduled S0–S12 (Part 8.1)", "Many-to-many: a work item is a screen/API slice; a story is a user outcome"],
    ["Work items mapped to ≥ 1 story", "—", str(sum(1 for r in wi_rows if r[8])), "All 162"],
    ["Base effort", "385.0 PD (149 items); +114 PD expansion", "382.2 pd central committed S0–S12 (546 SP × 0.7)", "Difference 2.8 pd (0.7%) on the 149-item baseline; expansion overlap per [CONFLICT-446]"],
    ["Low / high envelope", "287 / 483 PD (+62 / +196)", "287–483 PD (DEC-012)", "Same envelope"],
    ["Dependency-only longest path", "113.5 PD (verified: FND01→FND02→FND03→FND05→A008→…→W25→FND06→FND07→FND08)", "Part 8.1 §8.1.7 critical chain", "Recomputed by H_generate (DAG valid, no cycle, 2 symbolic predecessors)"],
    ["Approval review effort", "32.55 / 62.85 / 123.70 PD", "Not budgeted", "[GAP-450] §6.9.5.4.2"]]))
# module table compact
frag("module_table", md_table(["M", "Module", "Acceptance (doc 20)", "Blueprint BR / epic / wave", "Status"],
     [[r[0], r[2], r[3][:60], f"{r[1]} · {r[6]} · {r[7]}", r[8]] for r in br_rows[:66]]))

# =========================================================== 6. runbook / ops / capacity / DoD / costs
ops_rows = []
for rb in P["runbook"]:
    s, ref, note = MP.RUNBOOK[rb["routine"]]
    ops_rows.append(["Runbook", rb["routine"], rb["action"], ST[s], ref, note])
    cov("20", "Production runbook", "RUN-" + rb["routine"].replace(" ", "_"), f"{rb['routine']}: {rb['action']}", ST[s], ref, note or "Mapped", "RB-ENH-H" if s != "C" else "")
for w in P["work_packages"]:
    s, ref = MP.WORKPKG[w["order"]]
    ops_rows.append(["Work package", f"{w['order']} {w['package']}", w["evidence"], ST[s], ref, ""])
    cov("20", "Dependency-ordered implementation", "WP-" + w["order"], f"{w['package']}: {w['evidence']}", ST[s], ref, "Mapped to waves")
for c in P["capacity"]:
    s, ref, note = MP.CAPACITY[c[0]]
    ops_rows.append(["Capacity", c[0], f"Initial {c[1]}; growth {c[2]}", ST[s], ref, note])
    cov("20", "Capacity, reliability and recovery acceptance", "CAP-" + c[0][:30].replace(" ", "_"), f"{c[0]}: initial {c[1]}, growth {c[2]}", ST[s], ref, note or "Mapped")
for d in P["dod"]:
    s, ref = MP.DOD[d["item"]]
    ops_rows.append(["Execution backlog", d["item"], d["acceptance"], ST[s], ref, ""])
    cov("20", "Execution backlog and definition of done", "DOD-" + d["item"].replace(" ", "_"), d["acceptance"], ST[s], ref, "Mapped" if s == "C" else "Enhanced §6.9.5.4–§6.9.5.5")
costmap = {"AWS shared hosting": "B01", "Production AI inference": "B02", "Public search API": "B03", "Extraction compute / overage": "B04", "Email delivery": "B05", "WhatsApp Business": "B06",
           "Monitoring / security / CI": "B07", "Apollo paid enrichment reserve": "B08", "Claude Code developer seats": "B09", "Optional integration reserve": "B10", "Contingency rate": "B11"}
for c in P["pilot_costs"]:
    ops_rows.append(["Pilot cost", c[0], f"{c[1]} — {c[2][:90]}", "Covered", f"DEC-020 {costmap.get(c[0], '')}; DEC-004; Part 8.2 §8.2.7.2", "Figures identical to BRD §6 (verify provider prices at implementation, as of 27 Nov 2026)"])
    cov("20", "Operating cost assumptions", costmap.get(c[0], c[0]), f"{c[0]} {c[1]}", "Covered", f"DEC-020; Part 8.2 §8.2.7.2", "Mapped")
for e in P["effort"]:
    ops_rows.append(["Effort", e[0], e[1], "Covered", "DEC-012; BR-S102…S105; Part 8.1 §8.1.6", ""])
    cov("20", "Consolidated effort", "EFF-" + e[0][:25].replace(" ", "_"), f"{e[0]} {e[1]}", "Covered", "DEC-012; BR-S102…S105", "Mapped")
wcsv("H_ops_runbook_map.csv", ["kind", "item", "source_text", "status", "blueprint_location", "note"], ops_rows)
frag("ops_table", md_table(["Kind", "Item", "Source", "Status", "Blueprint", "Note"], [[a, b, c[:80], d, e, f] for a, b, c, d, e, f in ops_rows if a != "Pilot cost" and a != "Effort"]))

# =========================================================== 7. misc doc aspects (prose / numbers)
misc = [
 ("24", "Traceability method and status", "RTM-METHOD", "Populated mapping = proposal; PO/QA review each association; commits and evidence populated during engineering", "Covered", "Part 6.6 §6.6.1; AP-08", "Mapped"),
 ("24", "Non-screen review", "RTM-NONSCREEN", "Review unmapped routes/tables for internal use; do not delete because no screen", "Partially covered", "Part 6.6 §6.6.4.1", "Orphan review procedure added §6.9.5.3.6"),
 ("24", "Acceptance workflow", "RTM-ACCEPT-FLOW", "Assign BR/FR IDs, map unit rules, validate route/table links, attach immutable build and evidence, close defects, approve by business owner", "Partially covered", "Part 6.1 §6.1.5.4; US-2110", "Workflow states added §6.9.5.3.5"),
 ("24", "Traceability exception disposition", "RTM-EXCEPTIONS", "138 screen associations populated; 0 structural exceptions; reject false links", "Covered", "Part 6.6 §6.6.8", "Mapped"),
 ("24", "Change impact assessment", "AP-CIA", "List affected UI/API/DB/workflow/test before merge; no stale dependent contract", "Partially covered", "Part 8.2 §8.2.2.4", "FR-ENH-H-004 §6.9.5.3.4"),
 ("24", "Requirements traceability semantic approval", "AP-RTSA", "100% applicable mappings approved or justified exception; no synthetic approval", "Conflict", "AP-08 10% spot check", "[CONFLICT-442] §6.9.5.3.5"),
 ("24/20", "Outstanding approval gates", "GATE-COUNTS", "Exact API definitions 38; partial API 0; DB confirmations 4; UI semantic approvals 138", "Partially covered", "DEC-015; DEC-019; AP-08", "Decision queue §6.9.5.2"),
 ("24", "Optimization Intelligence reuse of Admin screens", "OPT-INTEL", "Optimization metrics reuse A089, A009, A012, A014, A084, A042, A082; unassessed when no denominator", "Covered", "Part 2.4 RP-; FR-A012/A014/A084", "Common core; optimization group owns metric contracts"),
 ("24/23/20", "Optimization controls (OPT-xx-yy)", "OPT-COMMON", "OPT-01-01…OPT-20-01 repeated per document", "Not applicable", "Part 2.1 §2.4.11", "Common core: see doc 36 review"),
 ("24/23/20", "Purpose and operating boundary", "CORE-BOUNDARY", "Employee-operated growth; no investor functions; independent product; 25+ startups", "Covered", "BR-S119…S121; FR-NEG-01", "Common core: see document 01/02 coverage"),
 ("24/23/20", "Completion and approval roles", "SIGNOFF-ROLES", "Responsible lead, independent reviewer/QA, product owner or delegate", "Covered", "Part 6.1 §6.1.5.4 EVR; §6.1.10.3 sign-offs", "Layer sign-off sheet §6.9.5.1.7"),
 ("24/23/20", "Acceptance and evidence record", "EVR-FIELDS", "Responsible/reviewer; artefact/test evidence; decision; remediation; business acceptance", "Covered", "Part 6.1 §6.1.5.4; Part 8.2 §8.2.4.2", "Mapped; EVR entity added §6.9.5.7"),
 ("23", "Quality gates and disposition", "QC-DISPOSITION", "Pass requires evidence; Fail requires defect and retest; Pending ≠ acceptance; N/A requires rationale; critical defect blocks", "Partially covered", "Part 6.1 §6.1.8.5 RBR; EVR decision", "QC state machine §6.9.5.1.3"),
 ("23", "Evidence gate and independent reviewer procedure", "QC-EVIDENCE-GATE", "Artifact manifest: control ID, expected, observed, executor, different reviewer, owner approval, path, SHA-256", "Not covered", "—", "Manifest schema §6.9.5.1.4 [GAP-443]"),
 ("23", "Evidence gate fail-closed", "AP-EGFC", "Delete row, duplicate ID, mandatory N/A in synthetic fixture → all rejected", "Not covered", "—", "TC-ENH-H-001…006"),
 ("23", "Granular QC and evidence", "AP-GQC", "Enforce required ID baseline; pending blocks release", "Not covered", "—", "FR-ENH-H-001/002"),
 ("23", "Go-live and rollback gate", "AP-GLRG", "Rehearse deployment with incomplete QC evidence; no activation on pending gate", "Partially covered", "GL-T05; RBR-6", "TC-ENH-H-012"),
 ("23", "Fail-closed evidence inventory", "AP-FCEI", "Authoritative required-ID list from immutable baseline; register cannot define its own scope", "Not covered", "—", "FR-ENH-H-002"),
 ("23", "Evidence integrity and final acceptance", "AP-EIFA", "Blank evidence, identical executor/reviewer after trim/case normalisation rejected; hash verified; signed approvals via change management", "Partially covered", "EVR responsible ≠ reviewer", "FR-ENH-H-002 normalisation rule"),
 ("23", "Combined preflight for production acceptance", "AP-CPPA", "1,188 required records across six groups; recompute 21 mandatory KPIs", "Not covered", "A090 gate table", "FR-ENH-H-005 (nine groups, 1,545 records) §6.9.5.6"),
 ("23", "Offline completeness command", "QC-OFFLINE-CMD", "release_gate.py register evidence-root → exit code 2 while pending", "Not covered", "—", "Gate evaluator exit-code contract §6.9.5.1.5"),
 ("23", "Expansion QC release condition", "UX-QC-RELEASE", "Combined gate includes baseline and expansion; no N/A bypass", "Partially covered", "GL-B02", "§6.9.5.6"),
 ("20", "Task-level estimates and discipline split", "EST-DISCIPLINE", "Frontend 90.68; Backend 111.55; DB 52.85; AI 36.23; QA 65.64; DevOps/security 28.05 PD", "Partially covered", "Part 8.1 §8.1.6 (per-epic, not per discipline)", "Reconciliation §6.9.5.4.2 [GAP-451]"),
 ("20", "Dependency-only longest path", "EST-LONGEST", "113.5 PD; not a schedule", "Covered", "Part 8.1 §8.1.7", "Recomputed: 113.5 PD"),
 ("20", "Expansion incremental estimate", "EST-EXPANSION", "62/114/196 PD before overlap reconciliation", "Conflict", "Part 8.1 §8.1.6.4 (287–483 includes W31–A113)", "[CONFLICT-446]"),
 ("20", "Approval review effort", "EST-REVIEW", "32.55/62.85/123.70 PD", "Not covered", "—", "[GAP-450] §6.9.5.4.2"),
 ("20", "Artifact and version consistency", "AP-AVC", "Compare package manifests and catalog hashes", "Not covered", "—", "FR-ENH-H-008"),
 ("20", "Complete document inventory", "AP-CDI", "Open all documents; verify unique numbers", "Not covered", "—", "FR-ENH-H-008 (38 documents)"),
 ("20", "Development dependencies", "AP-DD", "No missing/cyclic dependency; low ≤ base ≤ high", "Partially covered", "Part 8.1 §8.1.7", "FR-ENH-H-007 DAG validation"),
 ("20", "Workbook source and formulas", "AP-WSF", "All workbook tabs preserved; formulas compute", "Partially covered", "final/AI_Growth_Engine_Blueprint_Workbook_v1.0.xlsx", "Workbook check in §6.9.5.5"),
 ("20", "Unresolved contract decision management", "AP-UCDM", "Every blocker has a decision queue; no unapproved contract in production", "Not covered", "—", "FR-ENH-H-003 §6.9.5.2"),
 ("20", "Resource and deployment approval", "AP-RDA", "Estimate incremental effort per change; approve before promising cost or SLA", "Partially covered", "Part 8.2 §8.2.2.4", "§6.9.5.4.2"),
 ("20", "Optimization estimate reconciliation", "EST-OPT", "104 optimization controls proposed against existing tasks", "Not applicable", "—", "Common core: see doc 36 review"),
 ("20", "Website and Admin operating contract", "WEB-ADMIN-CONTRACT", "Surfaces, routing decision, configuration, separation, estimate update", "Covered", "BR-S106…S130", "Common core: see document 01/02 coverage"),
 ("20", "Deployment and operational runbook (website)", "WEB-DEPLOY-RB", "Separate builds, audiences, CSP; deploy schema+DRF policy before routes; independent rollback; monitor separately; emergency disable intake", "Partially covered", "Part 4.3 §4.37–§4.38; RB-012", "Website kill switch step added to RB-ENH-H-01"),
 ("20", "Implementation backlog and release-to-operations gate", "REL-OPS-GATE", "Licence register, backup evidence, budget kill switch, ownership of exceptions, cost per tenant", "Covered", "Part 4.3 §4.48; GL-L06; §4.46", "Mapped"),
 ("20", "Operational delivery and lifecycle", "OPS-LIFECYCLE", "Immutable artefacts; handover runbooks, ownership, access inventory, training", "Partially covered", "Part 8.2 §8.2.2, §8.2.5", "Access inventory §6.9.5.5"),
 ("20", "SaaS billing model", "SAAS-BILLING", "Plans, quotas, metered base + included + overage; margin formula", "Covered", "BR-S139; DEC-047", "Mapped"),
 ("20", "Initial startup configurations", "STARTUP-PROFILES", "AppNAI, MedMaarg, EduVerse, OrganicSpec profiles", "Covered", "Part 1; DEC-052", "Common core"),
 ("38", "Required evidence records", "EVID-1545", "Nine groups, 1,545 required records (180+624+235+104+24+21+172+175+10)", "Not covered", "—", "FR-ENH-H-005"),
]
for m in misc: cov(*m)

# coverage CSV
with open(COV / "H_coverage.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f); w.writerow(["doc", "section", "aspect_id", "aspect_summary", "status", "blueprint_location", "action", "new_ids"]); w.writerows(cov_rows)
# summary per doc
sm = collections.OrderedDict()
for r in cov_rows:
    d = r[0].split("/")[0]; sm.setdefault(d, collections.Counter())[r[4]] += 1
order = ["Covered", "Partially covered", "Not covered", "Conflict", "Not applicable"]
rows = [[d] + [c[o] for o in order] + [sum(c.values())] for d, c in sm.items()]
tot = [sum(r[i] for r in rows) for i in range(1, 7)]
frag("cov_summary", md_table(["Doc (primary)"] + order + ["Total"], rows + [["**Total**"] + tot]))
# aspect-type summary
ty = collections.OrderedDict()
for r in cov_rows:
    t = r[1].split(" ")[0] if not r[1].startswith("RTM row") else "RTM"
    key = {"QC": "Quality controls (QC)", "RTM": "Trace rows (SM-FR)", "Non-screen": "Trace rows (SM-FR)", "Expansion": "Expansion trace (SM-UX-FR) / backlog", "SIT": "SIT associations", "Engineering": "Decisions (numbered)", "BR": "Business requirements", "Task": "Work items"}.get(t, r[1])
    ty.setdefault(key, collections.Counter())[r[4]] += 1
frag("cov_types", md_table(["Aspect group"] + order + ["Total"], [[k] + [c[o] for o in order] + [sum(c.values())] for k, c in ty.items()]))
non_cov = [[r[0], r[2], r[3][:110], r[4], r[5][:70], r[6][:90]] for r in cov_rows if r[4] in ("Not covered", "Conflict") or (r[4] == "Partially covered" and not r[1].startswith("SIT association") and not r[1].startswith("Engineering decision"))]
frag("noncov", md_table(["Doc", "Aspect", "Summary", "Status", "Blueprint location", "Action"], non_cov))
print("coverage rows", len(cov_rows), {o: sum(1 for r in cov_rows if r[4] == o) for o in order}, "noncov listed", len(non_cov))

# =========================================================== 8. extra fragments for 6.9b
REV = {"Product Owner (R01 delegate)": "QA Lead", "Product Owner + Principal Engineer": "QA Lead", "Product Owner": "QA Lead or Auditor (R15)"}
sign_rows = []
for l, c in lay_cnt.items():
    anchors, role, gate, qcl = L[l]
    srcown = collections.Counter(P["qc"][k]["owner"] for k in P["qc"] if P["qc"][k]["layer"] == l).most_common(1)[0][0]
    rev = REV.get(role, "QA Lead (or Security Lead for QA-owned layers)") if "QA" not in role else "Independent engineer not on the change, or Auditor (R15)"
    cad = "Every release (R1, R2) and every later activation" if c["Critical"] else "Every wave gate that changes the layer"
    sign_rows.append([qcl, l, srcown, role, rev, gate, cad, f"evr/qc/<release>/{qcl}-signoff.json"])
frag("qc_signoff", md_table(["Layer", "Name", "Source owner", "Blueprint signatory", "Independent reviewer", "Signed at", "Cadence", "Sign-off evidence key"], sign_rows))
wv = collections.OrderedDict()
for r in dec_rows:
    if r[2] == "UI semantic mapping approval":
        f = r[5]; w = B["fr"].get(f, {}).get("wave_epic", "").split(" · ")[0] or "—"
        wv.setdefault(w, []).append(r[1])
frag("dec_wave", md_table(["Wave of the FR", "UI semantic approvals (SPDEC)", "Count", "Must be approved before"],
     [[w, ", ".join(sorted(v))[:400] if len(v) < 12 else f"{min(v)} … {max(v)} ({len(v)} records; see H_decision_map.csv)", len(v), f"G4 of the release containing {w}"] for w, v in sorted(wv.items())]))
