"""Group G (R6) builder: atomic aspect inventory + coverage CSV + Markdown fragments for Part 11.7.
Usage: python3 -I g_build.py   (paths are fixed in g_common.py; inputs are treated as data)."""
import sys, os, re, json, csv
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from g_common import *
from g_screens import *

fsd, crawl, consts = load()
CORP = corpus()
ALLTXT = "\n".join(CORP.values())
CARDS = cards_27b()
OUT = G + "/out"
os.makedirs(OUT, exist_ok=True)
W = crawl["website"]; A = crawl["admin"]

ASPECTS = []
CNT = {}


def add(doc, chap, sec, src, summary, sb, loc, action, new_ids, sa="Matched"):
    CNT[src] = CNT.get(src, 0) + 1
    aid = f"G-{src}-{CNT[src]:04d}"
    ASPECTS.append(dict(doc=doc, chapter=chap, section=sec, aspect_id=aid, aspect_summary=summary.replace("\n", " ")[:400],
                        status_before=sb, blueprint_location=loc, action=action, new_ids=new_ids, status_after=sa))
    return aid

# ------------------------------------------------------------------ FR register (FR-V12-G-###)
FR = []  # (id, title, screens, source, release, epic)


def fr(title, screens, source, release, epic):
    i = f"{FR_BASE}{len(FR) + 1:03d}"
    FR.append((i, title, screens, source, release, epic))
    return i

FRW = {}
for i in range(1, 35):
    wid = f"W{i:02d}"
    meta = next(r for r in W["routeMeta"] if r["id"] == wid)
    FRW[wid] = fr(f"{wid} repurposed as '{meta['name']}' ({meta['access']}) per V12 neutral SaaS storefront", wid,
                  f"FSD V12 ch20 {wid}; route reconciliation CSV; prototype", "Release 1 (W0–W3)" if i <= 21 or i in (30, 31, 32) else "Release 2 (W4–W5)",
                  "EP-19" if i <= 22 or i == 30 else ("EP-20" if i >= 31 else "EP-13" if i in (23, 24) else "EP-14" if i == 25 else "EP-15" if i == 26 else "EP-16" if i in (27, 28) else "EP-03"))
FRN = {}
for sid, d in WEBNEW.items():
    FRN[sid] = fr(f"{sid} {d['name']} (V12 {d['v12']})", sid, f"FSD V12 ch22/ch24; prototype {d['v12']}", d["rel"], d["ep"])
for v, sid in zip(SVC_WS, range(170, 184)):
    meta = next(m for m in A["screenMeta"] if m["id"] == v)
    FRN[f"A{sid}"] = fr(f"A{sid} {meta['name']} (V12 {v}, {SVC_WS[v]['svc']})", f"A{sid}", f"FSD V12 ch21 domain panel; ch24 registry {v}; prototype", SVC_WS[v]["rel"], SVC_WS[v]["ep"])
for v, sid in zip(OPS, range(184, 192)):
    meta = next(m for m in A["screenMeta"] if m["id"] == v)
    FRN[f"A{sid}"] = fr(f"A{sid} {meta['name']} (V12 {v})", f"A{sid}", f"FSD V12 ch22; ch24 registry {v}; prototype", OPS[v]["rel"], OPS[v]["ep"])
for sid, d in UTIL.items():
    FRN[sid] = fr(f"{sid} {d['name']} (V12 utility view {d['v12']})", sid, "FSD V12 ch24 utility navigation; prototype", d["rel"], d["ep"])
for sid, d in V12NEW.items():
    FRN[sid] = fr(f"{sid} {d['name']} (V12 {d['v12']})", sid, f"FSD V12 ch24 V8 / ch22 V12 screen table; {d['reqs']}", d["rel"], d["ep"])
FRA = {}
for v12, (bid, nm, note) in ALIAS_NOTES.items():
    FRA[v12] = fr(f"{bid} {nm}: V12 {v12} delta", bid, f"FSD V12 ch22/ch24; prototype {v12}", "Release 1 (W0–W3)" if v12 in ("A115", "A117", "A120", "A123", "A124", "A128", "RUNS", "W35") else "Release 2 (W4–W5)", "EP-01" if v12 in ("A123", "A124") else "EP-04" if v12 in ("A115", "A117") else "EP-03" if v12 in ("A120", "W35") else "EP-20" if v12 in ("A125", "A126", "A131") else "EP-21" if v12 in ("A129", "A130", "W38", "W40") else "EP-19" if v12 == "W39" else "EP-18" if v12 == "RUNS" else "EP-01")
FRX = {}
for key, title, scr, src, rel, ep in [
    ("A089", "A089 Unified Command Centre: 14 management views, 9 optimisation perspectives, 17 context filters, saved views, native-currency reporting, relationship journey and evidence drill-down", "A089", "FSD V12 ch23; ch22 V5 lab; prototype A089", "Release 1 (W0–W3)", "EP-17"),
    ("A107", "A107 renamed 'Tenant-owned website intake configuration'", "A107", "FSD V12 ch24 registry", "Release 1 (W0–W3)", "EP-19"),
    ("A108", "A108 renamed 'Tenant-owned landing page review & intake analytics'", "A108", "FSD V12 ch24 registry", "Release 1 (W0–W3)", "EP-19"),
    ("A106", "A106 scoped action inbox separate from operator-wide incidents (REC-06)", "A106", "FSD V12 ch23 REC-06", "Release 1 (W0–W3)", "EP-17"),
    ("I18N", "Internationalisation: externalised ICU strings, pseudo-locale test, language switcher (en, hi, de, fr, ar), locale formats, RTL mirroring", "W01+ all website routes; Admin chrome", "ENT-GLB-01…04; prototype V12L/V12T", "Release 1 framework; locales per DEC-625", "EP-19"),
    ("COOKIE", "Cookie consent banner and preferences with notice version (CJ-R12)", "W01+ ; W30", "FSD V12 ch24 V8 behaviour; prototype v8Wbanner", "Release 1 (W0–W3)", "EP-03"),
    ("VALID", "Inline form validation: aria-invalid, aria-describedby message, focus to first invalid field, message clears when corrected", "All website forms", "FSD V12 ch24 V8 behaviour; MOB-04", "Release 1 (W0–W3)", "EP-19"),
    ("SKIP", "Skip link, route focus to main, aria-current on active navigation, labelled modal with keyboard close", "All routes both apps", "MOB-12; prototype v7Focus", "Release 1 (W0–W3)", "EP-19"),
    ("BOTTOM", "Mobile bottom navigation: website Home, Services, Select, Portal, Help; Admin shortcuts by access experience; full screen navigator retained", "Website; Admin", "MOB-02; prototype v7Nav", "Release 1 (W0–W3)", "EP-19"),
    ("TABLES", "Responsive records: labelled keyboard-focusable scroll regions for tables, single-column cards, compact KPI grids, no page-level horizontal overflow", "All table views", "MOB-08; prototype v7Tables", "Release 1 (W0–W3)", "EP-17"),
    ("FILTERS", "Contextual mobile filters in native disclosures preserving selections, open state and cascading logic (single filter state)", "A089, RUNS/A110, filter forms", "MOB-07; prototype v7Disclosure", "Release 1 (W0–W3)", "EP-17"),
    ("PARITY", "Device parity: every registered Website and Admin route renders in both layout classes from one build per frontend; presentation never changes privileges", "All", "MOB-01; ADR-200", "Release 1 (W0–W3)", "EP-21"),
    ("AUDX", "Four access experiences (Platform operator, Tenant workspace, Automation operations, Portfolio oversight) as navigation presets derived from roles and grants", "Admin shell", "FSD V12 ch24 registry 'Demo access'; prototype persona selector", "Release 1 (W0–W3)", "EP-01"),
    ("SELECT", "Public selection modes Full suite / Partial bundle (complete families, default five) / Selective; 39 selectable SKUs; 25 included foundations not separately purchasable; selection cart", "W02–W06, W31", "README; layout catalogue; prototype CFG", "Release 1 (W0–W3)", "EP-20"),
    ("QUOTE", "Quote request configuration: delivery model, billing cycle, quote currency; quote invalidation on any selection change; no checkout or payment", "W06, W14, W23", "FSD V12 ch20 W06; prototype invalidateQuote", "Release 1 (W0–W3)", "EP-20"),
    ("SAMPLES", "W05/W08 workflow sample library: four workflow previews per SKU, 156 curated fictional outputs, 3-preview session cap, download all four", "W05, W08", "FSD V12 ch20 156 examples; AT-07/08; prototype V4_EXAMPLES", "Release 1 (W0–W3)", "EP-19"),
    ("CALC", "Planning calculators: W01 illustrative savings, W06 TCO and 50% benefit sensitivity, selection worksheet save/restore; user-entered assumptions only", "W01, W06", "CV-06/07; prototype v5Wtco", "Release 1 (W0–W3)", "EP-19"),
    ("ASSESS", "Readiness assessment and opportunity report (objective, role, business model, four 0–5 readiness scores) with explainable recommendations, no automatic selection", "W07, W11", "AT-03/05/06, CV-03; prototype v5Wassessment", "Release 1 (W0–W3)", "EP-19"),
    ("SAVED", "Scope-keyed saved filter views revalidated on apply (REC-13); presets session-only in demo", "A089, A110", "REC-13; ch23 filter contract", "Release 1 (W0–W3)", "EP-17"),
    ("CASCADE", "Cascading context filters: changing tenant/company/division/brand/offer/market or bundle/SKU invalidates descendants; OR within, AND across; stale async cancelled", "All filtered Admin views", "MT-26, REC-14; ch23 filter contract", "Release 1 (W0–W3)", "EP-17"),
    ("RUNSTATE", "Run state display and separation of duties: Queued, Running, Awaiting approval, Held, Reconciling, Completed, Failed, Canceled; requester ≠ reviewer identically on mobile", "A110, A033, A193", "FSD V12 ch24 V8 behaviours; MOB-09", "Release 1 (W0–W3)", "EP-18"),
    ("DRAFT", "Session and draft recovery: logout clears private application state; server drafts with TTL, revocation, optimistic concurrency and explicit restore; no credentials persisted", "W21, W32, W33, W34", "MOB-11; ST-15", "Release 1 (W0–W3)", "EP-20"),
    ("WIZ", "W33 eight-stage universal business configuration wizard with hierarchy editor and reviewed export", "W33", "FSD V12 ch20 V6; prototype v6Steps", "Release 2 (W4–W5)", "EP-20"),
    ("PORTAL", "Private customer success planning and operating hierarchy panels on W22/W27/W34; requested service workspaces; first-value milestones", "W22, W27, W34", "RT-02/03; ch21 V5 portal additions", "Release 2 (W4–W5)", "EP-20"),
    ("CS", "Customer experience controls in UI: guided tours, human escalation, progress/hold visibility, explainable recommendations, feedback and regeneration, actionable errors, notification preferences, closed-loop feedback", "A089, W22, W28, A110", "CS-01…13 (ch24)", "Release 1–2", "EP-17"),
    ("DOMAIN", "Shared domain-panel component for 39 service workspaces with local draft/review, versioned edit, search, scoped export and four workflow entries", "A004–A105 mapped panels; A170–A183; A193", "FSD V12 ch21; ADR-202", "Release 1 (W0–W3)", "EP-18"),
    ("INVEST", "No investor / fundraising mode in the commercial product (DEC-002) — pending Founder decision on V12 investor mode", "Website build config; W01, W33", "Prototype CFG.inv; Investment Automation sibling pack", "Pending Founder decision", "EP-19"),
]:
    FRX[key] = fr(title, scr, src, rel, ep)

# ------------------------------------------------------------------ helpers
def bp_w_loc(wid):
    return f"Part 2.5 §2.43 {wid}; Part 2.7b card {wid} (pre-V12 semantics)"


def fsdtables(ch):
    return [b for b in fsd[ch] if b["type"] == "table"]


CH20, CH21, CH22, CH23, CH24 = [k for k in sorted(fsd)]
DOC = "FSD V12"

# ------------------------------------------------------------------ ch20
t = fsdtables(CH20)
for r in t[0]["rows"]:
    i = r[0]
    status = {"ENT-GLB-01": ("Partially covered", "DEC-026 (i18n-ready ICU); Part 2.5 §2.49"),
              "ENT-GLB-02": ("Conflict", "DEC-026 locales en-IN + hi/ta/or"),
              "ENT-GLB-03": ("Not covered", "No RTL layout rule in Part 2.5"),
              "ENT-GLB-04": ("Partially covered", "DEC-026/DEC-027; Part 2.7b R-FLD"),
              "ENT-GLB-05": ("Partially covered", "Part 8.3 tax (DEC-028); A101"),
              "ENT-GLB-06": ("Covered", "DEC-027 native-currency, FX evidence; CA-FIN"),
              "ENT-GLB-07": ("Partially covered", "A008/A044; DLT in Part 4.1"),
              "ENT-GLB-08": ("Not applicable", "Architecture/residency roadmap (Group E, Part 11.5)")}[i]
    na = status[0] == "Not applicable"
    add(DOC, "20", "V12 Enterprise website routes and localisation", "F20", f"{i} [{r[1]}] {r[2]} Acceptance: {r[3]} Phase {r[5]}; prototype {r[6]}",
        status[0], status[1], "None (owned by Part 11.5)" if na else ("DEC-625; §11.7.5.6 i18n/RTL" if i in ("ENT-GLB-01", "ENT-GLB-02", "ENT-GLB-03", "ENT-GLB-04") else "Alias delta A131→A101 (§11.7.5.5)"),
        "" if na else (FRX["I18N"] + ("; DEC-625; CONFLICT-872" if i == "ENT-GLB-02" else "") if i <= "ENT-GLB-04" else FRA["A131"] if i in ("ENT-GLB-05", "ENT-GLB-06") else FRA["A128"]),
        "Not applicable (residency roadmap is architecture scope, Part 11.5)" if na else "Matched")
OPT = {}
for b in fsd[CH20] + fsd[CH21] + fsd[CH22] + fsd[CH24]:
    pass


def opt_items(ch):
    items = []; cur = None
    for b in fsd[ch]:
        if b["type"] != "text":
            continue
        m = re.match(r"^([A-Z]{2,3}-\d{2}) · (P\d) · (.*)$", b["text"])
        if m:
            cur = dict(id=m.group(1), pri=m.group(2), title=m.group(3), lines=[]); items.append(cur); continue
        if cur is not None and (b["text"].startswith("Requirement:") or b["text"].startswith("Acceptance") or b["text"].startswith("Owner:")):
            cur["lines"].append(b["text"])
    return items


def opt_add(ch, item, chapname):
    own = " ".join(item["lines"])
    web = re.search(r"Website: ([^|]*)\|", own); adm = re.search(r"Admin: ([^|]*)\|", own)
    web = web.group(1).strip() if web else ""; adm = adm.group(1).strip() if adm else ""
    ui = not web.startswith("No new website interaction")
    route_ids = re.findall(r"W\d\d", web)
    summ = f"{item['id']} ({item['pri']}) {item['title']} — {own[:250]}"
    if ui:
        fid = {"AT-05": FRX["ASSESS"], "AT-06": FRX["ASSESS"], "AT-03": FRX["ASSESS"], "CV-03": FRX["ASSESS"], "AT-07": FRX["SAMPLES"], "AT-08": FRX["SAMPLES"],
               "AT-09": FRW["W08"], "CV-06": FRX["CALC"], "CV-07": FRX["CALC"], "CV-04": FRW["W31"], "AT-11": FRW["W16"], "AT-12": FRW["W30"],
               "CV-08": FRX["SAMPLES"], "AT-02": FRW["W07"], "RT-02": FRX["PORTAL"], "RT-03": FRX["PORTAL"], "CS-01": FRX["CS"], "CS-13": FRX["CS"]}.get(item["id"], FRX["CS"])
        add(DOC, ch, chapname, "F" + ch, summ, "Not covered", "No OPT-TC/AT/CV register in blueprint; nearest " + ", ".join(bp_w_loc(x) for x in route_ids[:1]) if route_ids else "Part 2.5", f"§11.7.5 route delta {', '.join(route_ids)}", fid)
    else:
        add(DOC, ch, chapname, "F" + ch, summ, "Not covered", "No equivalent UI; requirement register shown in A089 (V5 lab)", "A089 delta lists the item in the optimisation register panel; requirement substance reconciled by the optimisation-register owner group", FRX["A089"])


for b in fsd[CH20]:
    if b["type"] == "text" and b["path"].endswith("controlled requirements"):
        add(DOC, "20", "V6 Universal architecture", "F20", b["text"], "Partially covered", "Part 2.5 §2.43 W32–W34; Part 2.7b W33", "W33 eight-stage wizard; W22/W27/W34 setup summary", f"{FRX['WIZ']}; {FRX['PORTAL']}")
    if b["type"] == "text" and b["text"].startswith("V5 website route additions"):
        for clause in re.split(r"; ", b["text"].split(":", 1)[1]):
            add(DOC, "20", "V5 optimization requirements", "F20", "V5 website route addition: " + clause.strip(), "Not covered", "No equivalent in Part 2.5/2.7b", "Route delta cards §11.7.5.2", FRX["CALC"] if "W06" in clause else FRX["SAMPLES"] if "W08" in clause or "W05" in clause else FRX["ASSESS"] if "W11" in clause else FRW.get(re.findall(r"W\d\d", clause)[0], FRX["CS"]) if re.findall(r"W\d\d", clause) else FRX["CS"])
for it in opt_items(CH20):
    opt_add("20", it, "V5 optimization requirements and controls")
for r in t[1]["rows"]:
    wid = r[0].split()[0]
    add(DOC, "20", "Frontend scope and canonical route registry", "F20", f"{r[0]} — access {r[1]}; V3 design intent: {r[2]}", "Partially covered", bp_w_loc(wid), "DEC-621 repurpose; route delta card", FRW[wid])
for b in fsd[CH20]:
    if b["type"] == "text" and re.match(r"^34 route baseline|^V4 chapter guidance", b["text"]):
        add(DOC, "20", "Frontend scope and canonical route registry", "F20", b["text"], "Partially covered", "Part 2.5 §2.40.2", "DEC-621; ADR-204 anonymous catalogue projection", FRX["SELECT"])
    if b["type"] == "text" and re.match(r"^(Public catalogue|Verified membership)", b["text"]):
        wid = b["path"].split(">")[-1].strip().split()[0]
        add(DOC, "20", "Frontend scope and canonical route registry > " + wid, "F20", f"{wid}: {b['text']}", "Partially covered", bp_w_loc(wid), f"Route delta card {wid}; UAT {wid}-V2-UAT mapped to {TC_BASE} tests", FRW[wid])
    if b["type"] == "text" and b["path"].endswith("commercial transparency"):
        for sent in [s for s in re.split(r"(?<=\.) ", b["text"]) if s.strip()]:
            add(DOC, "20", "Workflow demonstrations and commercial transparency", "F20", sent, "Not covered", "No workflow preview library in blueprint", "W05 sample library; calculators", FRX["SAMPLES"] if "W05" in sent or "fictional" in sent or "No real" in sent else FRX["CALC"] if "ROI" in sent else FRX["I18N"])
for r in t[2]["rows"]:
    add(DOC, "20", "Website fictional output examples — 156 flows", "F20S", f"{r[0]} {r[1]}: {r[2]}", "Not covered", "No sample library", "Dataset DS-W05-SAMPLES row (§11.7.5.7, Part 11.7c appendix)", FRX["SAMPLES"])

# ------------------------------------------------------------------ ch21
t21 = fsdtables(CH21)
for r in t21[0]["rows"]:
    i = r[0].split(" · ")[0]
    add(DOC, "21", "V10 Historical reconciliation controls", "F21", f"{r[0]}: {r[1]} Acceptance: {r[2]}", "Partially covered",
        "A100 templates; W27 checklist (Part 2.5)", "W27/W34 activation checklist tied to selected services; A100 template-to-SKU mapping", FRX["PORTAL"])
for r in t21[1]["rows"]:
    add(DOC, "21", "V10 Service activation and offboarding workflow", "F21", f"Stage {r[0]}: {r[1]} Evidence: {r[2]}", "Partially covered",
        "Part 8.3 (SaaS onboarding SLA); A099/A101; W27/W34", "Operator screens A184–A191 + portal W27/W34 show each stage and its evidence", "; ".join([FRN["A185"], FRN["A186"], FRN["A187"], FRN["A189"], FRX["PORTAL"]]))
mobtxt = {}
for b in fsd[CH21] + fsd[CH23] + fsd[CH24]:
    if b["type"] == "text" and re.search(r"> MOB-\d\d", b["path"]):
        m = re.search(r"MOB-\d\d", b["path"]).group(0); mobtxt.setdefault(m, []).append(b["text"])
MOBFR = {"MOB-01": FRX["PARITY"], "MOB-02": FRX["BOTTOM"], "MOB-03": FRX["PARITY"], "MOB-05": FRX["PARITY"], "MOB-06": FRX["PARITY"], "MOB-07": FRX["FILTERS"],
         "MOB-08": FRX["TABLES"], "MOB-11": FRX["DRAFT"], "MOB-12": FRX["SKIP"], "MOB-17": FRX["PORTAL"]}
MOBST = {"MOB-01": ("Conflict", "DEC-043 Admin desktop-first"), "MOB-02": ("Partially covered", "Part 2.5 §2.40.2 portal bottom tab bar"), "MOB-03": ("Partially covered", "Part 2.5 §2.46 (no 44 px rule)"),
         "MOB-05": ("Partially covered", "Part 2.5 §2.48 portal XS"), "MOB-06": ("Conflict", "DEC-043; A089 not targeted on mobile"), "MOB-07": ("Partially covered", "Part 2.5 §2.48 facets in a sheet"),
         "MOB-08": ("Partially covered", "Part 2.5 §2.48 tables → stacked cards"), "MOB-11": ("Partially covered", "Part 2.5 W32 save-and-resume"), "MOB-12": ("Partially covered", "Part 2.5 §2.46"), "MOB-17": ("Partially covered", "W28/W29 (Part 2.5)")}
for m, lines in sorted(mobtxt.items()):
    ch = "21" if m in ("MOB-05", "MOB-11", "MOB-17") else "23" if m == "MOB-06" else "24"
    for ln in lines:
        sb, loc = MOBST[m]
        add(DOC, ch, "V7 Responsive and mobile requirements > " + m, "F" + ch, f"{m}: {ln}", sb, loc, "§11.7.5.8 mobile rules" + ("; DEC-623 amends DEC-043" if sb == "Conflict" else ""), MOBFR[m] + ("; DEC-623; CONFLICT-871" if sb == "Conflict" else ""))
for b in fsd[CH21]:
    if b["type"] == "text" and b["text"].startswith("V5 private portal additions"):
        for s_ in [x for x in re.split(r"(?<=\.) ", b["text"].split(":", 1)[1]) if x.strip()]:
            add(DOC, "21", "V5 optimization requirements", "F21", s_.strip(), "Not covered", "W22/W27/W34 (Part 2.5) lack success-plan cards", "Portal delta", FRX["PORTAL"])
for it in opt_items(CH21):
    opt_add("21", it, "V5 optimization requirements and controls")
PANEL = {}
for r in t21[2]["rows"]:
    svc = r[0].split(" — ")[0]; PANEL[svc] = r
for r in t21[3]["rows"]:
    PANEL[r[0]] = PANEL.get(r[0], []) + ["||"] + r
REG = {}
for t_ in fsdtables(CH24):
    if "Screen ID" in t_["header"][0]:
        for r in t_["rows"]:
            REG[r[0].split()[0]] = r
SVC2SCR = {}
for sid, r in REG.items():
    m = re.search(r"SM-SVC-\d\d", r[2])
    if m:
        SVC2SCR.setdefault(m.group(0), []).append(sid)
for svc in sorted(k for k in PANEL if k.startswith("SM-SVC")):
    p = PANEL[svc]; n = int(svc[-2:])
    hosts = SVC2SCR.get(svc, [])
    if n >= 26:
        tgt = f"A{170 + n - 26}"; sb = "Not covered"; loc = "No screen for " + svc; fid = FRN[tgt]
    else:
        tgt = ", ".join(hosts) if hosts else "A193"; sb = "Partially covered"; loc = "Part 2.7b cards " + tgt; fid = FRX["DOMAIN"]
    add(DOC, "21", "Service workspace master — 39 domain panels", "F21P", f"{p[0]}: fields {p[1]}; channels/pattern {p[2]}", sb, loc, f"Domain panel contract §11.7.5.4 → {tgt}", fid)
    if "||" in p:
        q = p[p.index("||") + 1:]
        add(DOC, "21", "Domain workbench — 39 service-specific evidence fields", "F21P", f"{q[0]} {q[1]}: evidence fields {q[2]}; lifecycle {q[3]}", sb, loc, f"Domain panel evidence fields §11.7.5.4 → {tgt}", fid)
for b in fsd[CH21]:
    if b["type"] == "text" and b["path"].endswith(("39 domain panels", "evidence fields")) and not b["text"].startswith("V4"):
        for s_ in [x for x in re.split(r"(?<=\.) ", b["text"]) if x.strip()]:
            add(DOC, "21", b["path"].split(">")[-1].strip(), "F21", s_, "Not covered", "No domain-panel component in blueprint", "ADR-202 shared domain panel; W34 entitled workspace links", FRX["DOMAIN"])
    if b["type"] == "text" and b["text"].startswith("V4 chapter guidance"):
        add(DOC, "21", "Guidance", "F21", b["text"], "Partially covered", "Part 2.7b", "§11.7.5.4", FRX["DOMAIN"])

# ------------------------------------------------------------------ ch22
t22 = fsdtables(CH22)
for r in t22[0]["rows"]:
    sid = r[0]
    if sid.startswith("A"):
        bid, kind = ADM_X[sid]
    elif sid.startswith("W") and sid in WEB_X:
        bid, kind = WEB_X[sid], WEB_KIND.get(sid, "same")
    else:
        bid, kind = "W01 chrome", "component"
    sb = "Not covered" if kind == "new" else "Partially covered"
    fid = FRN.get(bid) or FRA.get(sid) or FRX["I18N"]
    add(DOC, "22", "V12 Enterprise screens and routes", "F22", f"{sid} {r[1]} — audience {r[2]}; requirements {r[3]}", sb,
        f"Blueprint {bid} ({kind}); V12 ID collides with Part 9.7–9.9 {sid}" if sid[1:].isdigit() and sid in ADM_X or sid in WEB_KIND else f"Blueprint {bid}",
        f"Crosswalk V12 {sid} → {bid} (DEC-620); contract §11.7.5", fid + "; DEC-620")
for b in fsd[CH22]:
    if b["type"] == "text" and b["text"].startswith("V5 optimization laboratory"):
        for s_ in [x for x in re.split(r"(?<=\.) ", b["text"].split(":", 1)[1]) if x.strip()]:
            add(DOC, "22", "V5 optimization requirements", "F22", s_.strip(), "Not covered", "A089 (Part 2.5) has no optimisation laboratory", "A089 delta: 9 perspectives, audience filtering", FRX["A089"])
    if b["type"] == "text" and (b["text"].startswith("Operator manages") or b["text"].startswith("V4 chapter guidance")):
        for s_ in [x for x in re.split(r"(?<=\.) ", b["text"]) if x.strip()]:
            add(DOC, "22", "Operator scope", "F22", s_, "Partially covered", "A099/A101 (Part 2.5); R13/R14 (Part 2.3)", "Operator screens A184–A191", "; ".join(FRN[f"A{n}"] for n in range(184, 192)))
for it in opt_items(CH22):
    opt_add("22", it, "V5 optimization requirements and controls")

# ------------------------------------------------------------------ ch23
t23 = fsdtables(CH23)
for r in t23[0]["rows"]:
    i = r[0].split(" · ")[0]
    add(DOC, "23", "V10 Historical reconciliation controls", "F23", f"{r[0]}: {r[1]} Acceptance: {r[2]}", "Partially covered",
        "A106 (Part 2.5 §2.43.4)" if i == "REC-06" else "FR-FLT saved views (Part 2.7a)", "A106 delta" if i == "REC-06" else "Saved views scope-keyed", FRX["A106"] if i == "REC-06" else FRX["SAVED"])
for b in fsd[CH23]:
    if b["type"] != "text" or "MOB-06" in b["path"]:
        continue
    if b["text"].startswith("Command Centre alignment"):
        for s_ in [x for x in re.split(r"(?<=\.) ", b["text"].split(":", 1)[1]) if x.strip()]:
            add(DOC, "23", "V6 Universal architecture", "F23", s_.strip(), "Partially covered", "A089 (Part 2.5 §2.44.5); startup switcher §2.41", "A089 delta; ORG A197", f"{FRX['A089']}; {FRN['A197']}")
    elif re.match(r"^(Requirement|Acceptance|P0)", b["text"]):
        mt = b["path"].split(">")[-1].strip()
        add(DOC, "23", mt, "F23", f"{mt}: {b['text']}", "Partially covered", "Part 2.5 §2.41 startup selector; FR-FLT (Part 2.7a)", "A089 delta / cascade rules", FRX["A089"] if "MT-02" in mt else FRX["CASCADE"])
    elif b["text"].startswith("All 14 management views") or b["text"].startswith("Portfolio filter") or b["text"].startswith("V4 chapter"):
        for s_ in [x for x in re.split(r"(?<=\.) ", b["text"]) if x.strip()]:
            add(DOC, "23", "Command Centre view and filter contract", "F23", s_, "Partially covered", "A089 seven views (Part 2.5 §2.40.1)", "A089 delta", FRX["A089"])
for r in t23[1]["rows"]:
    add(DOC, "23", "Command Centre view and filter contract", "F23", f"Filter/feature {r[0]}: {r[1]}", "Partially covered", "FR-FLT-01…11 (Part 2.7a §2.7.5)", "A089 filter contract delta", FRX["CASCADE"] if "Cascading" in r[1] else FRX["SAVED"] if r[0] == "Preset" else FRX["A089"])

# ------------------------------------------------------------------ ch24
t24 = fsdtables(CH24)
add(DOC, "24", "V10 Historical reconciliation controls", "F24", " ".join(t24[0]["rows"][0]), "Covered", "Part 2.7a FR-FLT-RULES (OR within, AND across; cancel stale)", "Cross-reference only", FRX["CASCADE"])
for r in t24[1]["rows"]:
    sb = "Conflict" if r[0] in ("MOB-01", "MOB-06") else "Not applicable" if r[0] in ("MOB-10",) else "Partially covered"
    add(DOC, "24", "V8 Mobile requirement alignment", "F24", f"{r[0]} {r[1]} — V8 change: {r[2]} Evidence: {r[3]}", sb, MOBST.get(r[0], ("", "Part 2.5 §2.48"))[1],
        "None: PWA/offline unchanged; cookie choice is per-viewer local convenience" if sb == "Not applicable" else "§11.7.5.8", "" if sb == "Not applicable" else MOBFR.get(r[0], FRX["PARITY"]) + ("; DEC-623" if sb == "Conflict" else ""),
        "Not applicable (no V8 change; PWA/offline remains out of scope per Part 2.5)" if sb == "Not applicable" else "Matched")
for r in t24[2]["rows"]:
    bid, kind = ADM_X.get(r[0], (WEB_X.get(r[0]), WEB_KIND.get(r[0])))
    fid = FRN.get(bid) or FRA.get(r[0])
    add(DOC, "24", "V8 New and changed screens", "F24", f"{r[0]} {r[1]} ({r[2]}) audiences {r[3]}; interactions {r[4]}; requirements {r[5]}", "Not covered" if kind == "new" else "Partially covered",
        f"V12 ID collides with blueprint {r[0]}; nearest blueprint {bid}", f"Crosswalk {r[0]} → {bid} (DEC-620)", f"{fid}; DEC-620")
for r in t24[3]["rows"]:
    m = {"404 / not found": (FRN["W53"], "Partially covered", "Part 2.5 W03 'unknown host → 404'"), "Inline validation (Website)": (FRX["VALID"], "Partially covered", "Part 2.5 §2.46"),
         "Cookie consent (Website)": (FRX["COOKIE"], "Partially covered", "Part 4.1 cookie notes; W30"), "Demo identity (Admin)": (FRX["RUNSTATE"], "Covered", "BRL SoD; maker-checker Part 2.3"),
         "Run states (Admin)": (FRX["RUNSTATE"], "Partially covered", "Part 2.3 run state machine"), "Generic workspaces (Admin)": (FRX["DOMAIN"], "Not applicable", "Prototype seed behaviour"),
         "Service workspaces (Admin)": (FRX["DOMAIN"], "Not covered", "No service workspaces")}[r[0]]
    add(DOC, "24", "V8 New and changed screens (behaviours)", "F24", f"{r[0]}: {r[1]}", m[1], m[2], "§11.7.5 cross-cutting behaviour", m[0] if m[1] != "Not applicable" else "",
        "Not applicable (demo seed data; production uses tenant records)" if m[1] == "Not applicable" else "Matched")
for r in t24[4]["rows"]:
    add(DOC, "24", "V7 Desktop and mobile presentation inventory", "F24", f"{r[0]}: desktop {r[1]}, mobile {r[2]}, logical {r[3]}", "Partially covered", "Part 2.5 147 screens + Parts 9.7–9.9 71", "Route count reconciliation §11.7.4 (GAP-881)", FRX["PARITY"])
for r in t24[5]["rows"]:
    add(DOC, "24", "Website logical route crosswalk", "F24", f"{r[0]} {r[1]} — {r[2]}", "Partially covered", bp_w_loc(r[0]), "Crosswalk §11.7.4", FRW[r[0]])
for r in t24[6]["rows"]:
    bid, kind = ADM_X[r[0]]
    sb = "Covered" if kind == "same" and r[0] not in ("A107", "A108") else "Partially covered" if kind == "same" else "Not covered"
    add(DOC, "24", "Admin logical screen crosswalk", "F24", f"{r[0]} {r[1]} — experiences {r[2]}", sb, f"Part 2.5/2.7b {bid}" if kind == "same" else f"No blueprint screen (new {bid})",
        "Crosswalk §11.7.4; access-experience preset" if sb == "Covered" else "Rename (DEC-622)" if r[0] in ("A107", "A108") else f"New screen {bid}",
        FRX["AUDX"] if sb == "Covered" else FRX.get(r[0], FRN.get(bid, "")))
for b in fsd[CH24]:
    if b["type"] != "text":
        continue
    p = b["path"]
    if "presentation inventory" in p or "Admin logical screen crosswalk" in p or p.endswith("Universal architecture and controlled requirements") and b["text"].startswith("Frontend component"):
        for s_ in [x for x in re.split(r"(?<=\.) ", b["text"]) if x.strip()]:
            add(DOC, "24", p.split(">")[-1].strip(), "F24", s_, "Partially covered", "Part 2.5 §2.48; Part 3.1 frontend", "ADR-200/ADR-201; §11.7.5.8", FRX["PARITY"])
    elif re.search(r"MT-(26|37)", p):
        mt = re.search(r"MT-\d\d", p).group(0)
        add(DOC, "24", mt, "F24", f"{mt}: {b['text']}", "Partially covered", "FR-FLT (Part 2.7a); Part 2.5 §2.45.2 component library", "Cascade rules / component ownership", FRX["CASCADE"] if mt == "MT-26" else FRX["PARITY"])
    elif p.split(">")[-1].strip().startswith("Admin route registry"):
        for s_ in [x for x in re.split(r"(?<=\.) ", b["text"]) if x.strip()]:
            add(DOC, "24", "Admin route registry", "F24", s_, "Partially covered", "Part 2.7b cards", "§11.7.4 registry reconciliation", FRX["AUDX"])
for it in opt_items(CH24):
    st = {"CS-01": "Covered", "CS-03": "Covered", "CS-05": "Covered", "CS-08": "Covered", "CS-09": "Covered", "CS-10": "Covered", "FL-15": "Covered"}.get(it["id"])
    if st:
        loc = {"CS-01": "A161 Experience Studio tours (Part 9.9)", "CS-03": "W11 'Talk to a person', W28 (Part 2.5)", "CS-05": "Citation chips (Part 2.5 §2.45.2)", "CS-08": "Error envelope with correlation ID (Part 3.2)",
               "CS-09": "Notification preferences NT/NX (Part 2.4)", "CS-10": "Part 2.5 §2.46 WCAG 2.2 AA", "FL-15": "A169 Guided Workflow Builder (Part 9.9); A113"}[it["id"]]
        add(DOC, "24", "V5 optimization requirements and controls", "F24", f"{it['id']} ({it['pri']}) {it['title']} — {' '.join(it['lines'])[:250]}", "Covered", loc, "Cross-reference", FRX["CS"])
    else:
        opt_add("24", it, "V5 optimization requirements and controls")
REGTXT = {}
for sid, r in REG.items():
    bid, kind = ADM_X[sid]
    sb = "Covered" if kind == "same" and sid not in ("A107", "A108") else "Partially covered" if kind == "same" else "Not covered"
    add(DOC, "24", "Admin route registry — 135 registered screens", "F24R", f"{r[0]} — demo access {r[1]}; UI pattern {r[2]}", "Partially covered" if sb == "Covered" else sb,
        f"Part 2.7b {bid} (audience preset and domain-panel mapping new)" if kind == "same" else f"New {bid}", "Audience preset + domain-panel mapping (§11.7.4)",
        FRX["AUDX"] + ("; " + FRX["DOMAIN"] if "Domain panel" in r[2] else "") if kind == "same" else FRN.get(bid, ""))
# 113 screen specs
specs = [x for x in t24 if x["header"][:1] == ["Requirement / field"]]
heads = [b for b in fsd[CH24] if b["type"] == "table" and b["header"][:1] == ["Requirement / field"]]
FIELD_DELTA = []
for sp in heads:
    sid = sp["path"].split(">")[-1].strip().split()[0]
    card = CARDS.get(sid, "")
    rows = {r[0]: r[1] if len(r) > 1 else "" for r in sp["rows"]}
    for key, label in [("Fields (source candidate)", "source field"), ("Enhancement / removed fields", "enhancement field")]:
        for f_ in [x.strip() for x in rows.get(key, "").split(";") if x.strip()]:
            st = cover(f_, card)
            if st == "Not covered":
                FIELD_DELTA.append((sid, f_, label))
            add(DOC, "24", f"Admin screen spec {sid}", "F24F", f"{sid} {label}: {f_}", st, f"Part 2.7b card {sid} field contract", "None" if st == "Covered" else "Field delta table §11.7.5.3",
                "" if st == "Covered" else FRX["DOMAIN"])
    add(DOC, "24", f"Admin screen spec {sid}", "F24F", f"{sid} purpose/access: {rows.get('Purpose / access candidate', '')}", "Covered", f"Part 2.5 §2.43 {sid}", "None", "")
    add(DOC, "24", f"Admin screen spec {sid}", "F24F", f"{sid} action/gate: {rows.get('Action / gate', '')}", cover(rows.get("Action / gate", "").split(";")[0], card + ALLTXT[:0]),
        f"Part 2.7b card {sid} automation", "Gate wording adopted in alias table §11.7.5.3", "")
    for rt in [x.strip() for x in rows.get("Source route / data mapping", "").split(";") if x.strip()]:
        if re.match(r"^(GET|POST|PUT|PATCH|DELETE) ", rt):
            path = rt.split(" ", 1)[1]
            st = "Covered" if path in card else "Partially covered"
            add(DOC, "24", f"Admin screen spec {sid}", "F24F", f"{sid} route {rt}", st, f"Part 2.7b card {sid} legacy operations; Part 3.5a", "None" if st == "Covered" else "API mapping owned by Part 11.8 (Group H)", "")
        elif rt.startswith("ADAPTER"):
            st = cover(rt.replace("ADAPTER", ""), card)
            st = "Covered" if st == "Covered" else "Partially covered"
            add(DOC, "24", f"Admin screen spec {sid}", "F24F", f"{sid} adapter {rt}", st, f"Part 2.7b card {sid} integrations; Part 3.5b", "None" if st == "Covered" else "Integration mapping owned by Part 11.8 (Group H); screen shows provider state only", "")
        else:
            st = "Covered" if rt.replace("existing ", "").split()[0] in card or rt in card else "Partially covered"
            add(DOC, "24", f"Admin screen spec {sid}", "F24F", f"{sid} data mapping {rt}", st, f"Part 2.7b card {sid} tables; Part 3.6a", "None" if st == "Covered" else "Table mapping owned by Part 11.9 (Group I)", "")
    add(DOC, "24", f"Admin screen spec {sid}", "F24F", f"{sid} V2 rule: {rows.get('V2 rule', '')}", "Covered", "Part 2.5 §2.47 UI states; Part 2.7b acceptance", "None", "")
    add(DOC, "24", f"Admin screen spec {sid}", "F24F", f"{sid} trace: {rows.get('Trace', '')}", "Covered", "Part 2.1 alias scheme SM-UX-FR/SM-UX-UAT (DEC-017)", "None", "")

# fix statuses for 'Partially covered' F24F with empty action -> make action explicit
for a in ASPECTS:
    if a["status_before"] == "Partially covered" and a["new_ids"] == "" and a["aspect_id"].startswith("G-F24F"):
        a["new_ids"] = FRX["DOMAIN"]
        if a["action"].startswith("Gate wording"):
            a["action"] = "Gate wording adopted in §11.7.5.3 alias/gate table"

# ------------------------------------------------------------------ workbook 147 + website pack
DOCW = "Source workbook 147 Screen Field"
for r in csv_rows(WB + "/Website.csv", 2):
    if not r or not r[0].startswith("W"):
        continue
    add(DOCW, "Website", "Website screen field audit", "WB", f"{r[0]} {r[1]} | add {r[5]} | remove {r[6]} | automation {r[8]}", "Covered",
        f"Part 2.7b card {r[0]}; final/coverage C06-FLD-{r[0]}", "Reconciled to V12 neutral route semantics (DEC-621); retained field decisions apply to W54 tenant intake templates where startup-specific", FRW.get(r[0], ""))
for r in csv_rows(WB + "/Admin.csv", 3):
    if not r or not r[0].startswith("A"):
        continue
    add(DOCW, "Admin", "Admin screen field audit", "WB", f"{r[0]} {r[1]} | add {r[5]} | remove {r[6]}", "Covered", f"Part 2.7b card {r[0]}; final/coverage C06-FLD-{r[0]}", "None", "")
for r in csv_rows(WB + "/New_screens.csv", 3):
    if r and len(r) > 2:
        add(DOCW, "New screens", "9 proposed new layouts", "WB", f"{r[1]} {r[3]} — fields {r[6]}; gate {r[9]}", "Covered", f"Part 2.7b card {r[1]}; DEC-002 wording replacement for 'fundraising thesis'", "None", "")
for r in csv_rows(WB + "/Global_fields.csv", 3):
    if r and r[0].startswith("G"):
        add(DOCW, "Global", "Reusable cross-screen rules", "WB", f"{r[0]} {r[1]}: {r[2]} | {r[3]} | {r[4]}", "Covered", "Part 2.7a §2.7.5 (C06-G01…G15)", "None" if r[0] != "G02" else "G02 'authorized issuer' term retired by DEC-002", "")
for r in csv_rows(WB + "/Acceptance.csv", 3):
    if r and r[0].startswith("T"):
        add(DOCW, "Acceptance", "Prototype acceptance", "WB", f"{r[0]} {r[1]} → {r[2]}", "Covered", "Part 2.7a / Part 6.8 (TC-ENH-C)", "None", "")
for r in csv_rows(WB + "/Summary.csv", 3):
    if r and len(r) > 2:
        add(DOCW, "Summary", "Recommended totals", "WB", f"{r[1]} {r[2]}", "Partially covered", "Part 2.5 147 screens", "Totals superseded by V12 route count reconciliation §11.7.4", FRX["PARITY"])

DOCP = "Website pack 34"
readme = open(WEBPACK + "/README.txt", encoding="utf-8").read()
for s_ in [x.strip() for x in re.split(r"(?<=\.) ", readme.replace("\n", " ")) if len(x.strip()) > 25]:
    inv = "nvest" in s_
    add(DOCP, "README", "Developer handoff", "WP", s_, "Conflict" if inv else "Partially covered", "DEC-002 (no fundraising)" if inv else "Part 2.5 §2.40.2; Part 4.1",
        "CONFLICT-868 pending Founder" if inv else "Adopted in §11.7.5 storefront rules", FRX["INVEST"] if inv else FRX["SELECT"], "Pending Founder decision" if inv else "Matched")
for r in csv_rows(WEBPACK + "/commercial_website_route_reconciliation.csv", 1):
    if r:
        add(DOCP, "Route reconciliation", "commercial_website_route_reconciliation.csv", "WP", f"{r[0]}: '{r[1]}' ({r[2]}) → '{r[3]}' ({r[4]}); {r[5]}", "Conflict", f"{bp_w_loc(r[0])} uses previous name '{r[1]}'",
            "Adopt V12 (DEC-621); previous startup-site semantics move to tenant-owned intake W54 and A107/A108", FRW[r[0]] + "; DEC-621")
cat = json.load(open(WEBPACK + "/commercial_website_layout_catalog.json", encoding="utf-8"))
for it in cat["items"]:
    core = it.get("core")
    add(DOCP, "Layout catalogue", "items", "WPC", f"{it['id']} {it['name']} ({it['family']}){' — included foundation, not purchasable' if core else ''}", "Not covered" if core else "Partially covered",
        "No foundations list in blueprint" if core else "Service registry reconciled in Part 11.2 (Group B); W04 card lists offerings not SKUs", "W04/W05/W06/W31 display", FRX["SELECT"])
for g in cat["groups"]:
    add(DOCP, "Layout catalogue", "groups", "WPC", f"Family {g['name']} (core={g['core']}): {g['desc']}", "Not covered", "No service families on W02", "W02/W03 family cards", FRW["W02"])
for c in cat["channels"]:
    add(DOCP, "Layout catalogue", "channels", "WPC", f"Channel option: {c}", "Partially covered", "Channels in Part 2.1 modules", "W16 channel list", FRW["W16"])
for c in cat["industries"]:
    add(DOCP, "Layout catalogue", "industries", "WPC", f"Industry option: {c}", "Partially covered", "Industry taxonomy (Part 3.3)", "W07/W32 select options", FRW["W07"])
add(DOCP, "Layout catalogue", "starter", "WPC", f"Starter family: {cat['starter']}", "Not covered", "—", "W06 partial-bundle default", FRX["SELECT"])
vr = json.load(open(WEBPACK + "/verification_report.json", encoding="utf-8"))
for k, v in vr["commercial"].items():
    add(DOCP, "Verification report", "commercial", "WP", f"Prototype verification {k} = {v}", "Partially covered", "Part 6.1 E2E strategy", "Converted to production tests TC-V12-G", FRX["PARITY"] if "mobile" in k or "routes" in k else FRX["SELECT"])
for k, v in vr["investment"].items():
    add(DOCP, "Verification report", "investment", "WP", f"Investment storefront verification {k} = {v}", "Conflict", "DEC-002", "CONFLICT-868", FRX["INVEST"], "Pending Founder decision")

# ------------------------------------------------------------------ prototype: website
DOCH = "Prototype HTML website (desktop = mobile by layout class)"
ch_ = W["chrome"]
for n in ch_["nav"]:
    add(DOCH, "Chrome", "Top and bottom navigation", "PW", f"Navigation link: {n}", "Partially covered", "Part 2.5 §2.40.2", "Navigation contract §11.7.5.8", FRX["BOTTOM"])
for n in ch_["footer"][:8]:
    w = n.split("#")[-1]
    add(DOCH, "Chrome", "Footer", "PW", f"Footer link: {n}", "Partially covered" if w in ("W30",) else "Not covered", "Part 2.5 footer", "Footer contract", FRN.get(WEB_X.get(w, ""), FRA.get(w, FRW.get(w, ""))))
add(DOCH, "Chrome", "Footer", "PW", f"Prototype screen navigator listing {len(ch_['footer']) - 8} routes", "Not applicable", "—", "Prototype-only navigator; production uses sitemap", "", "Not applicable (prototype navigator; production sitemap per AT-01)")
for l in ch_["langs"]:
    add(DOCH, "Chrome", "Language switcher", "PW", f"Locale {l}", "Conflict" if l.split(":")[0] in ("de", "fr", "ar") else "Partially covered", "DEC-026", "DEC-625", FRX["I18N"])
for k in ("lang:hi", "lang:ar"):
    add(DOCH, "Chrome", "Language switcher", "PW", f"{k}: html lang={W[k]['lang']} dir={W[k]['dir']}; partial translation of navigation", "Not covered", "No RTL rule", "RTL mirroring rule §11.7.5.6", FRX["I18N"])
for x in ["Skip to main content link", "Demo strip banner 'V12.0 · DESKTOP/MOBILE UI' (layout class v7-desktop / mobile-preview)", "Cookie preferences dialog (role=dialog): Essential only / Accept analytics / Read privacy notice; notice version COOKIE-NOTICE-v1", "Cart count and selection bar", "Client sign-in / End demo session control", "Partial translation notice"]:
    st = "Not applicable" if x.startswith("Demo strip") else "Partially covered"
    add(DOCH, "Chrome", "Global components", "PW", x, st, "Part 2.5 §2.41/§2.45.2", "Component catalogue §11.7.5.9" if st != "Not applicable" else "None", FRX["COOKIE"] if "Cookie" in x else FRX["SKIP"] if "Skip" in x else FRX["SELECT"] if "Cart" in x else FRX["DRAFT"] if "sign-in" in x else FRX["I18N"] if "translation" in x else "",
        "Not applicable (prototype banner only)" if st == "Not applicable" else "Matched")
WEBTXT = {}
for sess in ("anon", "demo"):
    for k, x in W.items():
        if not k.startswith(sess + ":"):
            continue
        wid = k.split(":")[1]
        bid = WEB_X[wid]
        fid = FRW.get(wid) or FRN.get(bid) or FRA.get(wid)
        pre = "Partially covered" if wid in FRW else ("Not covered" if WEB_KIND.get(wid) == "new" else "Partially covered")
        loc = bp_w_loc(wid) if wid in FRW else f"Blueprint {bid}"
        if sess == "anon":
            if wid in FRW and next(r for r in W["routeMeta"] if r["id"] == wid)["access"] == "Private demo":
                add(DOCH, wid, "Signed-out guard", "PW", f"{wid} signed out shows '{x['h'][0][3:]}' with 'Open client sign-in'", "Partially covered", loc, "Guard state in route card", fid)
            continue
        add(DOCH, wid, "Screen", "PW", f"{wid} → {bid}: {x['title'].split('|')[-1].strip()} — sections: {' / '.join(h[3:] for h in x['h'])[:300]}", pre, loc, f"Route card {bid}", fid)
        card = CARDS.get(wid, "") if wid in FRW else ""
        for f_ in x["fields"]:
            lab = f_["label"] or f_["name"]
            st = cover(lab, card) if card else "Not covered"
            st = "Partially covered" if st == "Covered" else st  # semantics changed by repurpose
            add(DOCH, wid, "Form field", "PW", f"{wid} field '{lab}' [{f_['type']}{', required' if f_['required'] else ''}{', options: ' + ' | '.join(f_['options'][:12]) if f_.get('options') else ''}]", st, loc, f"Field contract in route card {bid}", fid)
        for btxt in sorted(set(b["text"] for b in x["buttons"])):
            add(DOCH, wid, "Action", "PW", f"{wid} action '{btxt}'", "Not covered" if not card else cover(btxt, card), loc, f"Action table in route card {bid}", fid)
        for tb in x["tables"]:
            add(DOCH, wid, "Table", "PW", f"{wid} table [{' / '.join(tb['head'])}] rows={tb['rows']}", "Not covered", loc, f"Route card {bid}", fid)
        for d_ in x["details"]:
            add(DOCH, wid, "Disclosure", "PW", f"{wid} disclosure '{d_}'", "Not covered", loc, f"Route card {bid}", fid)
        WEBTXT[wid] = x
# website datasets and state model
for nm, desc, fid in [("CFG.items", f"{len(cat['items'])} catalogue entries (39 SKUs with 4 workflows each + 25 foundations)", FRX["SELECT"]), ("V4_EXAMPLES", "39 × 4 curated fictional outputs (156)", FRX["SAMPLES"]),
                      ("W10", "Campaign overview groups and events", FRW["W10"]), ("V12L", "5 locales with direction", FRX["I18N"]), ("V12T", "Chrome translation table (hi, de, fr, ar)", FRX["I18N"]),
                      ("V4_SCHEMA SM-APPLICATION-6", "Private application export schema with 33 keys incl. selectedServiceIds, selectedAutomationIds, selectionMode, billingCycle, hierarchy", FRN["A185"]),
                      ("state", "Website state: auth, selected set, selection mode, step, submitted, revision, quote validity, app; cleared on logout (MOB-11)", FRX["DRAFT"]),
                      ("localStorage", "Per-viewer storage of cookie choice (sm-v8-consent) and language (sm-v12-lang) only", FRX["COOKIE"])]:
    add(DOCH, "Datasets", "Embedded data", "PWD", f"{nm}: {desc}", "Not covered", "—", "Dataset contract §11.7.5.7", fid)

# ------------------------------------------------------------------ prototype: admin
DOCA = "Prototype HTML admin (desktop = mobile by layout class)"
for aud in A["audiences"]:
    add(DOCA, "Chrome", "Access experience selector", "PA", f"Access experience '{aud}' → {AUD_ROLE[aud]}", "Not covered", "Roles R01–R20 (Part 2.3) have no experience presets", "DEC-624", FRX["AUDX"])
for x in ["Navigation: A089 Unified Command Centre; 39 service workspaces; 156 workflow registry; Execution & approvals (non-operator, non-portfolio); O01/O02 shortcuts (operator); Screen inventory & traceability; grouped screen list with counts; screen search",
          "Demo membership switch (one membership at a time) and Action role (Requester / Reviewer / Read-only auditor)", "Scope tag: 'Granted aggregate' (portfolio), 'Operator scope', tenant name", "Denied view: 'This route is not available in this access experience' with Back to Command Centre",
          "Drawer dialog (role=dialog, labelled, Close ×)", "Banner 'V12.0 · DESKTOP/MOBILE UI · INTERNAL'"]:
    st = "Not applicable" if x.startswith("Banner") else "Partially covered"
    add(DOCA, "Chrome", "Admin shell", "PA", x, st, "Part 2.5 §2.41 global shell", "Shell contract §11.7.5.8" if st != "Not applicable" else "None",
        FRX["AUDX"] if "Navigation" in x or "Scope" in x or "Denied" in x else FRX["RUNSTATE"] if "Action role" in x else FRX["SKIP"] if "Drawer" in x else "", "Not applicable (prototype banner)" if st == "Not applicable" else "Matched")
SHELL = {"Search local records", "Search records", "Status", "Create synthetic draft", "Export fictional records", "Inspect"}
ADMV = {}
ids = []
for k in A:
    if ":" in k:
        i = k.split(":", 1)[1]
        if i not in ids:
            ids.append(i)
for sid in ids:
    allowed = [u for u in A["audiences"] if not any("not available in this access" in h for h in A[u + ":" + sid]["h"])]
    x = A[(allowed[0] if allowed else A["audiences"][0]) + ":" + sid]
    key = "SVC-*" if sid.startswith("SVC-") else "WF-*" if sid.startswith("WF-") else sid
    bid, kind = ADM_X.get(key, (sid, "same"))
    ADMV[sid] = (x, allowed, bid, kind)
    meta = next((m for m in A["screenMeta"] if m["id"] == sid), {})
    fid = FRN.get(bid) or FRA.get(sid) or FRX.get(sid) or (FRX["A089"] if sid == "A089" else FRX["DOMAIN"])
    sb = {"same": "Covered", "alias": "Partially covered"}.get(kind, "Not covered")
    if sid in ("A107", "A108"):
        sb = "Conflict"
    add(DOCA, sid, "Screen", "PA", f"{sid} {meta.get('name', '')} → {bid} ({kind}); experiences: {', '.join(allowed)}; sections: {' / '.join(h[3:] for h in x['h'])[:240]}", sb,
        f"Part 2.5/2.7b {bid}" if kind in ("same", "alias") else "—", "Crosswalk + experience preset" if kind == "same" else f"Contract {bid}", fid if sb != "Covered" else FRX["AUDX"])
    if kind in ("same",) and sid not in ("A089",):
        continue  # A001–A113 fields are domain-panel fields counted via ch21 panels
    seen = set()
    for f_ in x["fields"]:
        lab = f_["label"] or f_["name"]
        if lab in SHELL or (lab, f_["type"]) in seen or not lab:
            continue
        seen.add((lab, f_["type"]))
        st = cover(lab, CARDS.get(bid, "")) if kind == "alias" else "Not covered"
        add(DOCA, sid, "Form field", "PA", f"{sid} field '{lab}' [{f_['type']}{', ' + str(f_.get('nopt')) + ' options' if f_.get('nopt') else ''}]", st, f"Blueprint {bid}", f"Field contract {bid}", fid)
    for btxt in sorted(set(b["text"] for b in x["buttons"]) - SHELL):
        if re.match(r"^SM-SVC-\d\d-WF0\d$", btxt):
            continue
        add(DOCA, sid, "Action", "PA", f"{sid} action '{btxt}'", "Not covered" if kind != "alias" else cover(btxt, CARDS.get(bid, "")), f"Blueprint {bid}", f"Action table {bid}", fid)
    for tb in x["tables"]:
        h = " / ".join(tb["head"])
        if h in ("Record / revision / Domain evidence / Updated / Action", "Record / Reference / details / State / Review", "Record / Summary / Status / Updated / Action"):
            continue
        add(DOCA, sid, "Table", "PA", f"{sid} table [{h}] rows={tb['rows']}", "Not covered", f"Blueprint {bid}", f"Contract {bid}", fid)
for nm, rows in consts.items():
    if nm in ("E12_SCREENS", "V8_SCREENS"):
        continue
    items = rows.items() if isinstance(rows, dict) else enumerate(rows)
    tgt = {"V8_RULES": "A200", "V8_TIERS": "A198", "V8_INJ": "A199", "PERMS": "A002", "SOD": "A002", "BUILTIN": "A002", "INT": "A008", "CERT": "A159", "VSLA": "A159", "TAX": "A101"}[nm]
    for k, v in items:
        vv = v if isinstance(v, list) else [v]
        add(DOCA, "Datasets", nm, "PAD", f"{nm} {k if isinstance(rows, dict) else ''} {' | '.join(str(z) for z in vv)[:300]}", "Not covered" if nm in ("V8_RULES", "V8_TIERS", "V8_INJ") else "Partially covered",
            f"Blueprint {tgt}", f"Dataset shown on {tgt}", FRN.get(tgt) or FRA.get({"A002": "A123", "A008": "A128", "A159": "A129", "A101": "A131"}.get(tgt, ""), ""))
for nm, desc, tgt in [("DATA.services", "39 services with family, domain, objective, input, output, channel, meter, allowance, price 'Quotation pending', provider", "A192"),
                      ("DATA.workflows", "156 workflows with trigger, input, output, 4 steps each (STEP IDs, engine, contract, failure → state), risk", "A194"),
                      ("DATA.screens", "135 screen definitions (113 A + 14 X + 8 O) with audiences, fields, originalFields, additions, removal, routes, tables, links", "A196"),
                      ("DATA.foundations", "25 included foundations SM-01-01 … SM-14-05", "A192"), ("DATA.engines", "15 logical engines ENG-01…15 with mapped services", "A192"),
                      ("V5_REGISTER", "135 optimisation requirements (9 groups × 15: AI, GC, SEC, ST, FL, AT, RT, CV, CS)", "A089"), ("V6_REGISTER", "40 multi-tenant requirements MT-01…40", "A197"),
                      ("R10", "Historical reconciliation register REC-01…30, weights, 20 automation groups, 7 journey events, 5 startup scenarios, 14 plays, 13 node types", "A089"),
                      ("states", "Execution states: Queued, Running, Awaiting approval, Held, Completed, Failed, Reconciling, Canceled", "A110"),
                      ("stages", "Pipeline stages: Discovered, Qualified, Engaged, Meeting, Proposal, Won, Lost", "A029"),
                      ("viewGroups", "14 management views mapped to the 7 Admin groups and service sets", "A089"), ("v5GroupLabels", "9 optimisation perspectives: AI cost, General cost, Security, Stability, AI flows, Attraction, Retention, Conversion, Satisfaction", "A089"),
                      ("V6_LABELS", "8 hierarchy entity types", "A197")]:
    fid = FRN.get(tgt) or (FRX["A089"] if tgt == "A089" else FRA["RUNS"] if tgt == "A110" else FRX["DOMAIN"])
    add(DOCA, "Datasets", nm, "PAD", f"{nm}: {desc}", "Partially covered" if tgt in ("A110", "A029") else "Not covered", f"Blueprint {tgt}", f"Dataset contract on {tgt}", fid)
# A089 view labels
for v in ["Executive Overview", "Market Intelligence", "Lead & Contact Intelligence", "Digital Marketing", "Omnichannel Engagement", "Follow-up & Meetings", "Objection & Negotiation", "Sales Pipeline & Closure",
          "Revenue & Financial Intelligence", "Customer Success", "Partner & Procurement", "AI & Automation Control", "Governance & Risk", "Optimization Intelligence"]:
    add(DOCA, "A089", "Management view", "PA", f"A089 management view '{v}'", "Partially covered", "A089 seven views (Part 2.5 §2.40.1)", "A089 delta §11.7.5.3", FRX["A089"])
for f_ in ["Tenant", "Business division", "Brand", "Product / service / programme", "Target market", "Target country", "State / region", "Channel account", "Industry", "Customer type", "Target segment", "Campaign", "Opportunity type", "Employee", "Team", "Risk / priority", "Authority level"]:
    add(DOCA, "A089", "Context filter (17)", "PA", f"A089 context filter '{f_}'", cover(f_, CARDS.get("A089", "")), "Part 2.7b A089; FR-FLT", "A089 filter delta", FRX["A089"])

# investor mode
add(DOCH, "Investor mode", "CFG.inv flag", "PW", "Website template contains an investor/fundraising objective mode (CFG.inv) with 'Automate your fundraising operations', 'eligible investors', 'Fundraising thesis' wording; commercial build sets inv=false", "Conflict", "DEC-002; CC-01; negative regression test (Part 6.1 T02)", "CONFLICT-868: remove mode from the commercial codebase; Founder decides on sibling product", FRX["INVEST"] + "; DEC-632", "Pending Founder decision")
add("Source archive", "Investment Automation", "Investment_Automation_19_Neutral_SaaS_Website + 24 services/96 workflows workbook", "SA", "Sibling investor/fundraising storefront and catalogue in the V12 source archive", "Conflict", "DEC-002", "CONFLICT-868", FRX["INVEST"], "Pending Founder decision")

# budget conflict aspect
add("Blueprint governance", "Budget", "UI scope added by V12", "BG", "New screens A170–A204, W50–W54, Admin mobile parity, locales de/fr/ar and RTL exceed approved Ledger A/B scope", "Conflict", "DEC-230/DEC-422/DEC-228", "CONFLICT-869; separate costed proposal §11.7.5.12", "DEC-633", "Pending Founder decision")

# ------------------------------------------------------------------ write CSV
os.makedirs(BP + "/final/coverage_v12", exist_ok=True)
with open(BP + "/final/coverage_v12/G_coverage.csv", "w", newline="", encoding="utf-8") as fh:
    w = csv.DictWriter(fh, fieldnames=["doc", "chapter", "section", "aspect_id", "aspect_summary", "status_before", "blueprint_location", "action", "new_ids", "status_after"])
    w.writeheader()
    for a in ASPECTS:
        w.writerow(a)
json.dump(dict(fr=FR, frw=FRW, frn=FRN, fra=FRA, frx=FRX, field_delta=FIELD_DELTA), open(OUT + "/ids.json", "w"), indent=1, ensure_ascii=False)
from collections import Counter
print("aspects", len(ASPECTS)); print(Counter(a["status_before"] for a in ASPECTS)); print(Counter(a["status_after"] for a in ASPECTS))
print(Counter(a["doc"] for a in ASPECTS)); print("FR", len(FR), "field delta", len(FIELD_DELTA))
