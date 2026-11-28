"""Group G (R6) renderer: Markdown fragments for Part 11.7a/b/c from the coverage CSV, crawl and screen master.
Usage: python3 -I g_render.py"""
import sys, os, re, json, csv
from collections import Counter, defaultdict, OrderedDict
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from g_common import *
from g_screens import *

fsd, crawl, consts = load()
W = crawl["website"]; A = crawl["admin"]
IDS = json.load(open(G + "/out/ids.json", encoding="utf-8"))
FR, FRW, FRN, FRA, FRX = IDS["fr"], IDS["frw"], IDS["frn"], IDS["fra"], IDS["frx"]
ROWS = list(csv.DictReader(open(BP + "/final/coverage_v12/G_coverage.csv", encoding="utf-8")))
CARDS = cards_27b()
OUT = G + "/out"


def esc(s):
    return str(s).replace("|", "\\|").replace("\n", " ").strip()


def tbl(head, rows):
    o = ["| " + " | ".join(head) + " |", "|" + "---|" * len(head)]
    for r in rows:
        o.append("| " + " | ".join(esc(x) for x in r) + " |")
    return "\n".join(o) + "\n"


def write(name, text):
    open(OUT + "/" + name, "w", encoding="utf-8").write(text)


# ====================================================================== summaries
src_name = {"F20": "FSD ch20 Public SaaS Website", "F20S": "FSD ch20 156 fictional outputs", "F21": "FSD ch21 Tenant portal", "F21P": "FSD ch21 39 domain panels + evidence fields",
            "F22": "FSD ch22 Platform operator", "F23": "FSD ch23 Portfolio Command Centre", "F24": "FSD ch24 UI/UX master (prose, MOB, V8, crosswalks)", "F24R": "FSD ch24 Admin route registry (135)",
            "F24F": "FSD ch24 113 per-screen specs (field, route, rule atoms)", "WB": "Workbook 147 Screen Field (6 sheets)", "WP": "Website pack (README, reconciliation, verification)",
            "WPC": "Website pack layout catalogue", "PW": "Prototype website (41 routes + 404, chrome)", "PWD": "Prototype website datasets", "PA": "Prototype admin (153 screens + utility views, chrome)",
            "PAD": "Prototype admin datasets", "SA": "Source archive (Investment sibling)", "BG": "Blueprint governance (budget)"}
by = defaultdict(Counter)
after = defaultdict(Counter)
for r in ROWS:
    s = r["aspect_id"].split("-")[1]
    by[s][r["status_before"]] += 1
    after[s]["Matched" if r["status_after"] == "Matched" else "Pending" if r["status_after"].startswith("Pending") else "N/A"] += 1
STB = ["Covered", "Partially covered", "Not covered", "Conflict", "Not applicable"]
rows = []
tot = Counter(); tota = Counter()
for s in src_name:
    if s not in by:
        continue
    b = by[s]; a = after[s]
    tot.update(b); tota.update(a)
    rows.append([s, src_name[s], sum(b.values())] + [b[x] for x in STB] + [a["Matched"], a["Pending"], a["N/A"]])
rows.append(["**Total**", "", f"**{sum(tot.values())}**"] + [f"**{tot[x]}**" for x in STB] + [f"**{tota['Matched']}**", f"**{tota['Pending']}**", f"**{tota['N/A']}**"])
summary = tbl(["Src", "Material", "Aspects", "Covered", "Partial", "Not covered", "Conflict", "N/A", "Matched (after)", "Pending Founder", "N/A (after)"], rows)
write("summary.md", summary)
json.dump(dict(total=sum(tot.values()), before=dict(tot), after=dict(tota)), open(OUT + "/summary.json", "w"))

# ====================================================================== detailed register (non-covered individually)
reg = []
grouped = OrderedDict()
for r in ROWS:
    if r["status_before"] == "Covered":
        continue
    s = r["aspect_id"].split("-")[1]
    if s in ("PW", "PA") and re.match(r"^(A\d{3}|X\d\d|O\d\d|W\d\d|W99X|SVC-|WF-|INDEX|SERVICES|WORKFLOWS|RUNS|ORG)", r["chapter"]) and r["section"] in ("Form field", "Action", "Table", "Disclosure"):
        key = (s, r["chapter"], r["section"])
        grouped.setdefault(key, []).append(r)
        continue
    reg.append(r)
by_src = OrderedDict()
for r in reg:
    by_src.setdefault(r["aspect_id"].split("-")[1], []).append(r)
parts = []
for s, rs in by_src.items():
    if s == "F20S":
        parts.append(f"\n#### Register F20S: FSD ch20 156 fictional outputs ({len(rs)} aspects)\n\nAll 156 rows were Not covered before and are Matched by {FRX['SAMPLES']}; each row is listed individually with its aspect ID in the W05 sample library dataset (Part 11.7c §11.7.5.15).\n")
        continue
    parts.append(f"\n#### Register {s}: {src_name.get(s, s)} ({len(rs)} aspects)\n\n")
    parts.append(tbl(["Aspect", "Summary", "Before", "Blueprint location", "Action", "New IDs", "After"],
                     [[r["aspect_id"], r["aspect_summary"][:230], r["status_before"], r["blueprint_location"][:90], r["action"][:110], r["new_ids"][:80], r["status_after"][:40]] for r in rs]))
parts.append(f"\n#### Register PW/PA itemised screen elements ({sum(len(v) for v in grouped.values())} aspects in {len(grouped)} rows)\n\nEach row names every individual field, action, table or disclosure of one prototype screen that was not already covered; each item is a separate aspect ID in `G_coverage.csv`.\n\n")
gr = []
for (s, ch, sec), rs in grouped.items():
    items = "; ".join(re.sub(r"^\S+ (field|action|table|disclosure) ", "", r["aspect_summary"])[:70] for r in rs)
    gr.append([f"{rs[0]['aspect_id']}…{rs[-1]['aspect_id'].split('-')[-1]}", ch, sec, len(rs), items[:900], Counter(r["status_before"] for r in rs).most_common(1)[0][0], rs[0]["new_ids"][:40], "Matched"])
parts.append(tbl(["Aspect IDs", "Screen", "Element", "n", "Items (each an aspect)", "Before (mode)", "New IDs", "After"], gr))
write("register.md", "".join(parts))
cov = Counter((r["aspect_id"].split("-")[1]) for r in ROWS if r["status_before"] == "Covered")
write("covered_groups.md", tbl(["Src", "Material", "Covered aspects (grouped)", "Where covered"], [[s, src_name.get(s, s), n, {"F24F": "Part 2.7b per-screen cards (field, route, table, rule) and Part 2.1 alias scheme", "WB": "Part 2.7a/2.7b and coverage C06 (same field audit as source doc 06)", "F24": "Part 2.7a FR-FLT; Part 2.5 §2.46; CS items in Parts 2.4, 3.2, 9.9", "PA": "Part 2.5/2.7b A001–A113 (screen identity unchanged)", "PW": "Part 2.5 chrome"}.get(s, "Part 2.5/2.7")] for s, n in cov.items()]))

# ====================================================================== crosswalks
wrows = []
recon = {r[0]: r for r in csv_rows(WEBPACK + "/commercial_website_route_reconciliation.csv", 1) if r}
for r in W["routeMeta"] + [{"id": f"W{i}", "name": W.get(f"demo:W{i}", {}).get("title", "").split("·")[-1].strip(), "access": "Public"} for i in range(35, 42)] + [{"id": "W99X", "name": "Page not found", "access": "Public"}]:
    wid = r["id"]; bid = WEB_X[wid]
    prev = recon.get(wid, ["", "", "", "", "", ""])[1]
    kind = "repurposed (DEC-621)" if wid in FRW else WEB_KIND.get(wid)
    fid = FRW.get(wid) or FRN.get(bid) or FRA.get(wid)
    wrows.append([("V12 " if wid >= "W35" else "") + (wid if wid != "W99X" else "(unknown)"), r["name"], r["access"], bid, prev or ("Part 9.9 " + bid if WEB_KIND.get(wid) == "alias" else "—"), kind, fid])
write("xwalk_web.md", tbl(["V12 route", "V12 name", "V12 access", "Blueprint ID", "Previous blueprint name", "Relation", "FR"], wrows))
REG = {}
for t_ in [b for b in fsd[sorted(fsd)[4]] if b["type"] == "table" and "Screen ID" in b["header"][0]]:
    for rr in t_["rows"]:
        REG[rr[0].split()[0]] = rr
arows = []
SMETA = {m["id"]: m for m in A["screenMeta"]}
ids = []
for k in A:
    if ":" in k:
        i = k.split(":", 1)[1]
        if i not in ids:
            ids.append(i)
names = {}
for m in A["screenMeta"]:
    names[m["id"]] = m["name"]
for e in consts["V8_SCREENS"] + consts["E12_SCREENS"]:
    names[e[0]] = e[1]
for sid in ids:
    key = "SVC-*" if sid.startswith("SVC-") else "WF-*" if sid.startswith("WF-") else sid
    if key in ("SVC-*", "WF-*") and sid not in ("SVC-SM-SVC-01", "WF-SM-SVC-01-WF01"):
        continue
    bid, kind = ADM_X.get(key, (sid, "same"))
    allowed = [u for u in A["audiences"] if not any("not available in this access" in h for h in A[u + ":" + sid]["h"])]
    v12name = names.get(sid, {"A089": "Unified admin command centre", "INDEX": "Screen inventory & traceability", "SERVICES": "39 service workspaces", "WORKFLOWS": "156 workflow registry", "RUNS": "Execution & approvals", "ORG": "Business & Organization Management Centre"}.get(sid, sid))
    bpname = ""
    if kind in ("same", "alias"):
        c = CARDS.get(bid, "")
        m = re.match(r"### [0-9.]+ [AW]\d+[^:]*: ([^\n]*)", c)
        bpname = m.group(1) if m else next((ALIAS_NOTES[x][1] for x in ALIAS_NOTES if ALIAS_NOTES[x][0] == bid), "")
    else:
        bpname = {**{f"A{170 + i}": names.get(f"X{26 + i}") for i in range(14)}, **{f"A{184 + i}": names.get(f"O0{1 + i}") for i in range(8)}, **{k: v["name"] for k, v in UTIL.items()}, **{k: v["name"] for k, v in V12NEW.items()}}.get(bid, "")
    fid = FRN.get(bid) or FRA.get(sid) or FRX.get(sid) or FRX["AUDX"]
    arows.append([("V12 " + sid) if sid in [e[0] for e in consts["V8_SCREENS"] + consts["E12_SCREENS"]] else sid.replace("SVC-SM-SVC-01", "SVC-* (dynamic)").replace("WF-SM-SVC-01-WF01", "WF-* (dynamic)"), v12name,
                  " ".join(AUD_SHORT[u] for u in allowed), bid + (" + " + ADM_ALSO[sid] if sid in ADM_ALSO else ""), bpname or "(new)", kind if sid not in ("A107", "A108") else "same ID, renamed (DEC-622)", fid])
write("xwalk_adm.md", tbl(["V12 screen", "V12 name", "Experiences", "Blueprint ID", "Blueprint name", "Relation", "FR"], arows))


# ====================================================================== field rule inference
def rule(lab, typ, req, opts):
    l = lab.lower()
    m = re.search(r"\((\d+)\s*[–-]\s*(\d+)[^)]*\)", lab)
    if typ == "email":
        r = "RFC 5322 address, lower-cased, ≤ 254 chars; stored encrypted with HMAC lookup (Part 2.7b R-FLD)"
    elif typ == "url":
        r = "https:// URL only, ≤ 2,048 chars; no credentials in URL"
    elif typ == "number":
        r = (f"Integer/decimal {m.group(1)}–{m.group(2)}" if m else "Integer 1–60" if l.startswith("months") else "Percentage 0–100" if "%" in l else
             ("Decimal ≥ 0, exact decimal; currency shown; labelled estimate" if re.search(r"cost|price|budget|fee|amount|value|invoice|receipt|₹|rate|subscription|support|setup|estimate|labor|limit", l) else "Integer ≥ 0; bounded server-side"))
    elif typ in ("select-one", "select-multiple"):
        r = "Allowlist: " + (" | ".join(opts[:10]) + (" …" if len(opts) > 10 else "") if opts else "server-provided options")
    elif typ == "checkbox":
        r = "Must be checked to submit" if req else "Optional; default unchecked"
    elif typ == "textarea":
        r = "Plain text ≤ 2,000 chars; no personal data beyond purpose; HTML stripped"
    elif typ == "date":
        r = "ISO date; not in the past where it is a booking"
    elif typ == "time":
        r = "HH:MM in the selected IANA time zone"
    elif typ == "file":
        r = "JSON ≤ 1 MB; schema SM-APPLICATION-6 or worksheet schema; parsed client-side, validated server-side"
    elif typ == "search":
        r = "Free text ≤ 200 chars; allowlisted fields"
    else:
        r = "Text ≤ 200 chars; trimmed; validated server-side"
    return r + ("; required" if req else "")


def field_table(fields, skip=()):
    seen = set(); rows = []
    for f in fields:
        lab = f.get("label") or f.get("name")
        if not lab or lab in skip or (lab, f["type"]) in seen:
            continue
        seen.add((lab, f["type"]))
        rows.append([len(rows) + 1, lab, f["type"], "Yes" if f.get("required") else "No", rule(lab, f["type"], f.get("required"), f.get("options") or [])])
    return tbl(["#", "Field (label as prototype)", "Control", "Req.", "Validation and rule"], rows) if rows else "_No input fields (content or table screen)._\n"


def actions_list(btns, skip=()):
    out = sorted(set(b["text"] for b in btns if b["text"] and b["text"] not in skip))
    return "; ".join(out) if out else "—"


# ====================================================================== W01–W34 route delta cards
specs = {}
for b in fsd[sorted(fsd)[0]]:
    if b["type"] == "text" and re.search(r"> W\d\d — ", b["path"]):
        specs[b["path"].split(">")[-1].strip().split()[0]] = b["text"]
reco = recon
prev = {}
for wid in [f"W{i:02d}" for i in range(1, 35)]:
    c = CARDS.get(wid, "")
    m = re.match(r"### [0-9.]+ W\d+: ([^\n]*)", c)
    prev[wid] = m.group(1) if m else ""
DISPOSITION = {
    "W02": "Startup directory retired from the platform site; owned startups publish on their own sites (W54 intake).", "W03": "Startup website moves to tenant-owned sites (A107/A108, W54).",
    "W04": "Offering catalogue becomes the SaaS automation catalogue; startup offerings stay in A004/A005 and tenant sites.", "W05": "Offering details become SKU details with four workflow previews.",
    "W06": "Startup price packages become SaaS plan selection; startup pricing remains private (A139/A067).", "W07": "Industry pages become neutral industry guide with readiness assessment.",
    "W08": "Knowledge centre becomes automation guides and sample laboratory.", "W09": "Case studies become illustrative (fictional) use cases; no customer claims.", "W10": "Campaign landing pages move to tenant-owned sites; W10 becomes campaign automation overview.",
    "W11": "AI chat assistant becomes the rule-based selection assistant; tenant chat assistants remain in A046/A045.", "W12": "General enquiry becomes SaaS service enquiry; startup enquiry form → W54 template 'enquiry'.",
    "W13": "Demo/partnership enquiry retained for the SaaS; startup variant → W54 'demo'.", "W14": "RFQ becomes custom SaaS quotation request; OrganicSpec/AppNAI RFQ → W54 'rfq'.", "W15": "Project requirement submission becomes automation requirements builder; AppNAI project intake → W54 'requirement'.",
    "W16": "Supplier registration replaced by channel & integration options; OrganicSpec supplier intake → W54 'supplier'.", "W17": "Student/institutional enquiry replaced by delivery models; EduVerse intake with under-18 guardian branch (DEC-030) → W54 'training'.",
    "W18": "Booking retained for SaaS consultations; startup booking → W54 'booking' + A040.", "W19": "Webinar registration retained for product webinars; startup events → W43/W54 'event'.", "W20": "Partner referral becomes service referral programme; startup referral → W54 'referral'.",
    "W21": "Sign-in retained (SaaS client).", "W22": "Customer dashboard becomes client service dashboard.", "W23": "Proposal/quotation review becomes subscription quotation review; startup customer quotes remain portal objects under R16 grants (W23 pattern reused).",
    "W24": "Agreement review becomes service agreement review; startup customer agreements reuse the same pattern under grants.", "W25": "Order status becomes subscription order status; OrganicSpec orders reuse the pattern under grants.",
    "W26": "Payment status becomes SaaS billing & invoice status; tenant customer invoices reuse the pattern under grants.", "W27": "Onboarding becomes private onboarding checklist.", "W28": "Support retained with feedback and renewal.",
    "W29": "Preferences retained.", "W30": "Contact/privacy/help retained with trust FAQ and jurisdiction notices.", "W31": "Retained as bundle comparison.", "W32": "Retained as private client registration.", "W33": "Retained as eight-stage configuration wizard.", "W34": "Retained as client service portal.", "W01": "Homepage becomes neutral SaaS proposition."}
cards = []
for wid in [f"W{i:02d}" for i in range(1, 35)]:
    x = W["demo:" + wid]; an = W["anon:" + wid]
    meta = next(r for r in W["routeMeta"] if r["id"] == wid)
    secs = " / ".join(h[3:] for h in x["h"])
    tb = "; ".join(f"[{' / '.join(t['head'])}] {t['rows']} rows" for t in x["tables"]) or "—"
    det = "; ".join(x["details"]) or "—"
    guard = f"Signed out: '{an['h'][0][3:]}' + 'Open client sign-in'" if meta["access"] == "Private demo" else "Public: renders signed out; no tenant data in anonymous payload (ADR-204)"
    cards.append(f"""
##### {wid} {meta['name']} (V12; previously "{prev[wid]}")

| Attribute | Value |
|---|---|
| V12 access · prototype kind | {meta['access']} · `{meta['kind']}` |
| FR · release | {FRW[wid]} · {next(f for f in FR if f[0] == FRW[wid])[4]} |
| V12 route rule (FSD ch20) | {esc(specs.get(wid, ''))} |
| Sections (prototype order) | {esc(secs)} |
| Actions | {esc(actions_list(x['buttons']))} |
| Tables / disclosures | {esc(tb)} · {esc(det)} |
| Guard state | {esc(guard)} |
| Former semantics disposition (DEC-621) | {esc(DISPOSITION.get(wid, ''))} |
| Tests | {TC_BASE}{int(FRW[wid].split('-')[-1]) * 2 - 1:03d} (conformance), {TC_BASE}{int(FRW[wid].split('-')[-1]) * 2:03d} (negative/scope); V12 UAT alias {wid}-V2-UAT |

{field_table(x['fields'])}""")
write("cards_web.md", "".join(cards))

# ====================================================================== new website screens
nw = []
for sid, d in WEBNEW.items():
    v = {"W50": "W36", "W51": "W37", "W52": "W41", "W53": "W99X"}.get(sid)
    x = W.get("demo:" + v) if v else None
    secs = " / ".join(h[3:] for h in x["h"]) if x else "Form title; template-driven field set; consent notice; success reference"
    tb = "; ".join(f"[{' / '.join(t['head'])}] {t['rows']} rows" for t in x["tables"]) if x else "—"
    fidn = int(FRN[sid].split("-")[-1])
    extra = ""
    if sid == "W54":
        extra = tbl(["Template", "Replaces former blueprint semantics", "Key fields (from Part 2.5 rows, retained)", "Gate"], [
            ["enquiry", "W12 General business enquiry", "Name, organization, email, country, message, preferred channel, timezone, consent", "Rate limit; CAPTCHA after 3/min; consent record with notice version"],
            ["demo", "W13 Demo and partnership enquiry", "Request type by capability, meeting preference, partnership category, company size band, consent", "Slot picker only if A040 eligible"],
            ["rfq", "W14 Request for quotation", "Line items (SKU/service, quantity + unit, required by, delivery region/terms), currency, notes", "No automatic quote; unit per SKU"],
            ["requirement", "W15 Project requirement submission", "Organization/contact; scope/technology/delivery model; deadline (timezone); budget optional; attachments after sign-in", "Upload scan; AppNAI capability check (T18)"],
            ["supplier", "W16 Supplier registration", "Supplier legal name; product lines (SKU, grade, unit, quantity, lead time); certifications with expiry; delivery terms", "OrganicSpec payable side only"],
            ["training", "W17 Student training and institutional enquiry", "Who is enquiring (institution / adult learner / parent or guardian / learner under 18) first; programme, mode, cohort, language", "Under 18 → guardian details + OTP verification + declaration (DEC-030); minimal learner data; no direct outreach to minors"],
            ["booking", "W18 Meeting and appointment booking", "Purpose, duration, timezone, slot grid, confirmation", "Slot held 15 min; confirm after provider evidence"],
            ["event", "W19 Webinar and event registration", "Event, visitor timezone, capacity, registration fields, accessibility needs, consent", "Waitlist when full"],
            ["referral", "W20 Partner referral form", "Referrer, referral organization, relationship, minimal referred-person details, consent attestation", "Warning against unnecessary personal data"]])
    nw.append(f"""
#### {sid} {d['name']} (V12 {d['v12']})

| Attribute | Value |
|---|---|
| Surface · pattern | Website public · {d['pattern']} |
| Purpose | {esc(d['purpose'])} |
| Requirements | {esc(d['reqs'])} |
| FR · epic · release | {FRN[sid]} · {d['ep']} · {d['rel']} |
| Sections | {esc(secs)} |
| Tables | {esc(tb or '—')} |
| States | Loading; content; 404 for unknown slug; translated-partially notice when locale ≠ en (ENT-GLB-02) |
| Mobile and accessibility | Single column ≤ 599 px; tables in labelled focusable scroll regions; headings in order; links underlined (V8 contrast fix); route focus to `main` |
| Tests | {TC_BASE}{fidn * 2 - 1:03d}, {TC_BASE}{fidn * 2:03d} |

{field_table(x['fields']) if x else ''}{extra}""")
write("cards_webnew.md", "".join(nw))

# ====================================================================== new admin screens
PANELS = {}
t21 = [b for b in fsd[sorted(fsd)[1]] if b["type"] == "table"]
for r in t21[2]["rows"]:
    PANELS[r[0].split(" — ")[0]] = [r[0], r[1], r[2]]
for r in t21[3]["rows"]:
    PANELS.setdefault(r[0], []).extend([r[1], r[2], r[3]])
SVCS = {}
SHELL = {"Search local records", "Search records", "Status", "Create synthetic draft", "Export fictional records", "Inspect"}


def adm_view(v):
    for u in A["audiences"]:
        x = A.get(u + ":" + v)
        if x and not any("not available in this access" in h for h in x["h"]):
            return x
    return None


def allowed(v):
    return [u for u in A["audiences"] if A.get(u + ":" + v) and not any("not available in this access" in h for h in A[u + ":" + v]["h"])]


na = []
for i, (v, d) in enumerate(SVC_WS.items()):
    sid = f"A{170 + i}"; x = adm_view(v); m = SMETA[v]; p = PANELS.get(d["svc"], [])
    wfs = [h[3:] for h in x["h"] if h[3:].startswith(d["svc"] + "-WF")]
    fidn = int(FRN[sid].split("-")[-1])
    na.append(f"""
#### {sid} {m['name']} (V12 {v})

| Attribute | Value |
|---|---|
| Service · purpose | {d['svc']} · {esc(m['purpose'])} |
| Access experiences → roles | {', '.join(allowed(v))} → {AUD_ROLE['Tenant workspace']}; {AUD_ROLE['Automation operations']}. Entitlement to {d['svc']} required for actions; otherwise read-only 'not entitled' tag |
| Pattern · epic · release | {d['pattern']} · {d['ep']} · {d['rel']} |
| Regions (prototype) | {esc(' / '.join(h[3:] for h in x['h']))} |
| Four workflows | {esc('; '.join(wfs))} |
| Domain panel (FSD ch21) | Fields: {esc(p[1] if len(p) > 1 else '')} · channels/pattern: {esc(p[2] if len(p) > 2 else '')} · evidence fields: {esc(p[4] if len(p) > 4 else '')} · lifecycle: {esc(p[5] if len(p) > 5 else '')} |
| Catalogue fields (DATA.screens) | {esc('; '.join(m['fields']))} |
| Actions and gates | {esc(actions_list(x['buttons'], SHELL | {d['svc'] + '-WF0' + str(k) for k in range(1, 5)}))}. Local draft → Needs review → Reviewed by a different user (SoD); 'Prepare simulation' never dispatches; production effects pass the PDP at dispatch |
| Safety and policy | {esc(d['safety'])} |
| States | {COMMON_STATES}; 'Read-only / not entitled' |
| Related screens | A033, A110, A106, A193, A195 |
| Mobile and accessibility | Domain table in labelled scroll region; record cards ≤ 599 px with identical actions; 44 px targets; filter disclosure (MOB-07) |
| FR · tests | {FRN[sid]} · {TC_BASE}{fidn * 2 - 1:03d}, {TC_BASE}{fidn * 2:03d} |

{field_table(x['fields'], SHELL)}""")
write("cards_admnew.md", "".join(na)); na = []
for i, (v, d) in enumerate(OPS.items()):
    sid = f"A{184 + i}"; x = adm_view(v); m = SMETA[v]
    fidn = int(FRN[sid].split("-")[-1])
    tbs = "; ".join(f"[{' / '.join(t['head'])}] {t['rows']} rows" for t in x["tables"])
    na.append(f"""
#### {sid} {m['name']} (V12 {v})

| Attribute | Value |
|---|---|
| Purpose | {esc(d['purpose'])} |
| Access | Platform operator experience only → {AUD_ROLE['Platform operator']}. No default read of tenant CRM or business data; tenant data only through an A189 (V12 O06) support grant |
| Pattern · epic · release | {d['pattern']} · {d['ep']} · {d['rel']} |
| Requirements | {esc(d['reqs'])} |
| Catalogue fields (DATA.screens) | {esc('; '.join(m['fields']))} |
| Prototype regions · tables | {esc(' / '.join(h[3:] for h in x['h']))} · {esc(tbs or '—')} |
| API (V12 FSD ch25 / App. A2) | {esc('; '.join(d['api']))} |
| Data | {esc(d['data'])} |
| States | {COMMON_STATES} |
| Related | A089, A099, A101 |
| FR · tests | {FRN[sid]} · {TC_BASE}{fidn * 2 - 1:03d}, {TC_BASE}{fidn * 2:03d} |

{tbl(['Action', 'Gate / permission', 'Result'], d['actions'])}
{field_table(x['fields'], SHELL)}""")
for sid, d in list(UTIL.items()) + list(V12NEW.items()):
    v = d["v12"].split()[0]
    vv = {"SVC-<SM-SVC-##>": "SVC-SM-SVC-01", "WF-<SM-SVC-##-WF#>": "WF-SM-SVC-01-WF01"}.get(v, v)
    x = adm_view(vv)
    fidn = int(FRN[sid].split("-")[-1])
    tbs = "; ".join(f"[{' / '.join(t['head'])}] {t['rows']} rows" for t in x["tables"]) if x else "—"
    extra = ""
    if sid == "A198":
        extra = tbl(["Tier ID", "Tier", "Model type", "Tasks", "Data classes", "Region", "V12 status", "Blueprint gateway mapping"], [r + [{"MDL-R0": "Tier 0 rules/cache", "MDL-S1": "Tier 1a lighter Claude (DEC-418)", "MDL-M1": "Tier 1b Claude Sonnet (DEC-418)", "MDL-L1": "Tier 1b (escalation)", "MDL-E1": "Embedding (pgvector)", "MDL-G1": "Safety classifier"}[r[0]]] for r in consts["V8_TIERS"]])
    if sid == "A199":
        extra = tbl(["Test", "Source", "Attack", "Expected control"], consts["V8_INJ"])
    if sid == "A200":
        extra = tbl(["Rule", "Market", "Channel", "Legal source (verify at time of implementation, as of 27 Nov 2026)"], [[r[0], r[1], r[2], r[4]] for r in consts["V8_RULES"]])
    na.append(f"""
#### {sid} {d['name']} (V12 {d['v12']})

| Attribute | Value |
|---|---|
| Purpose | {esc(d['purpose'])} |
| Access experiences → roles | {esc(', '.join(f"{a} ({AUD_ROLE[a]})" for a in d['aud']))} |
| Pattern · epic · release | {d['pattern']} · {d['ep']} · {d['rel']} |
| Requirements | {esc(d.get('reqs', 'V12 ch24 utility navigation (not a registered route; DEC-628)'))} |
| Prototype regions · tables | {esc(' / '.join(h[3:] for h in x['h']) if x else '')} · {esc(tbs)} |
| API | {esc('; '.join(d['api']))} |
| States | {COMMON_STATES} |
| Mobile and accessibility | Tables in labelled, keyboard-focusable scroll regions; forms single column ≤ 599 px; status chips use text + icon, never colour alone |
| FR · tests | {FRN[sid]} · {TC_BASE}{fidn * 2 - 1:03d}, {TC_BASE}{fidn * 2:03d} |

{tbl(['Action', 'Gate / permission', 'Result'], d['actions'])}
{field_table(x['fields'], SHELL) if x else ''}{extra}""")
write("cards_admops.md", "".join(na))

# ====================================================================== alias deltas
al = []
for v12, (bid, nm, note) in ALIAS_NOTES.items():
    x = W.get("demo:" + v12) if v12.startswith("W") else adm_view(v12)
    fidn = int(FRA[v12].split("-")[-1])
    tbs = "; ".join(f"[{' / '.join(t['head'])}] {t['rows']} rows" for t in x["tables"]) if x else "—"
    al.append(f"""
#### {bid} {nm} ← V12 {v12}

| Attribute | Value |
|---|---|
| Delta | {esc(note)} |
| Also affects | {ADM_ALSO.get(v12, '—')} |
| V12 audiences | {esc(', '.join(allowed(v12)) if not v12.startswith('W') else 'Public')} |
| Prototype sections · tables | {esc(' / '.join(h[3:] for h in x['h']))} · {esc(tbs)} |
| Prototype actions | {esc(actions_list(x['buttons'], SHELL))} |
| FR · tests | {FRA[v12]} · {TC_BASE}{fidn * 2 - 1:03d}, {TC_BASE}{fidn * 2:03d} |

{field_table(x['fields'], SHELL)}""")
write("cards_alias.md", "".join(al))
# datasets for alias screens
ds = []
ds.append("\n##### PERMS × actions and SoD (A002 delta)\n\n" + tbl(["Resource", "Actions"], [[k, ", ".join(v)] for k, v in consts["PERMS"].items()]) + "\n" + tbl(["Blocked pair (same user)", "Second permission"], consts["SOD"]) + "\n" + tbl(["Built-in role", "Permissions"], consts["BUILTIN"]))
ds.append("\n##### Connector catalogue (A008 delta)\n\n" + tbl(["ID", "Category", "Examples (verify at time of implementation, as of 27 Nov 2026)", "Auth", "Scope"], consts["INT"]))
ds.append("\n##### Certification programme and vulnerability SLA (A159/A165 delta)\n\n" + tbl(["Programme", "Status", "Target phase", "Scope"], consts["CERT"]) + "\n" + tbl(["Severity", "Remediation SLA (days, proposed)"], [[k, v] for k, v in consts["VSLA"].items()]))
ds.append("\n##### Tax rule table (A101 delta, ENT-GLB-05)\n\n" + tbl(["Jurisdiction rule", "Invoice tax line", "Rate %"], [[k, v[0], "enter" if v[1] is None else v[1]] for k, v in consts["TAX"].items()]) + "\nTax rates must be verified at time of implementation (as of 27 Nov 2026); the screen never sums mixed currencies without an approved FX rate (MT-21).\n")
write("datasets.md", "".join(ds))

# ====================================================================== domain panels
pr = []
for svc in sorted(PANELS):
    p = PANELS[svc]
    hosts = [k for k, r in REG.items() if svc in r[2]]
    n = int(svc[-2:])
    pr.append([svc, p[0].split(" — ")[1] if " — " in p[0] else p[0], p[1], p[2], p[4] if len(p) > 4 else "", ", ".join(hosts) if hosts else "—", f"A{170 + n - 26}" if n >= 26 else "A193"])
write("panels.md", tbl(["Service", "Panel", "Local form fields and action", "Channels / pattern", "Additional evidence fields", "Hosting A-screens (V12 registry)", "Blueprint workspace"], pr))

# ====================================================================== samples
t20 = [b for b in fsd[sorted(fsd)[0]] if b["type"] == "table"]
SAID = {r["aspect_summary"].split(" ")[0]: r["aspect_id"] for r in ROWS if r["aspect_id"].startswith("G-F20S")}
write("samples.md", tbl(["Aspect", "Workflow", "Title", "Illustrative example (fictional; labelled on screen)"], [[SAID.get(r[0], ""), r[0], r[1], r[2]] for r in t20[2]["rows"]]))

# ====================================================================== FR / TC / US
frrows = [[f[0], f[1], f[2], f[3], f[4], f[5]] for f in FR]
write("fr.md", tbl(["FR", "Requirement", "Screens", "Source", "Release", "Epic"], frrows))
TCS = []
for f in FR:
    n = int(f[0].split("-")[-1])
    pos = f"Render {f[2]} in each permitted access experience at 360, 768 and 1280 px; every field, action, table and state in the contract is present with the specified validation; axe-core 0 violations; keyboard-only path completes"
    neg = f"Out-of-scope user, non-entitled tenant or anonymous visitor opens {f[2]}: server denies (403/404), no data in payload, denied view shown; invalid inputs rejected with inline announced errors"
    if f[0] == FRX["INVEST"]:
        pos = "Build the commercial website and Admin; search bundles, routes, strings and API schema for investor, fundraising, issuer and thesis terms and for a mode flag: none present (DEC-002 regression)"
        neg = "Attempt to enable an investor mode via configuration or query parameter: rejected; build fails if CFG-style inv flag exists"
    if f[2] == "A172":
        neg = "Agent-to-agent message instructs the workspace to pay or accept a quote: no effect; mandate draft requires named human approval within spending limit; PDP blocks dispatch without approval hash"
    if f[2] == "A181":
        neg = "AI scenario proposes a price outside the approved price book: shown as proposal only; cannot be applied without the approval matrix; no price change event emitted"
    if f[2] == "W54":
        neg = "Training template: selecting 'learner under 18' requires guardian details and OTP verification; no learner contact field is offered; submission without guardian verification is held (DEC-030)"
    TCS.append([f"{TC_BASE}{n * 2 - 1:03d}", f[0], "Conformance", pos])
    TCS.append([f"{TC_BASE}{n * 2:03d}", f[0], "Negative / scope / safety", neg])
write("tc.md", tbl(["Test", "FR", "Type", "Steps and expected result"], TCS))
US = []
epc = Counter()
PERS = {"EP-19": "an anonymous visitor (R18)", "EP-20": "a SaaS client admin (R17/R12) or operator (R13/R14)", "EP-03": "the DPO (R10)", "EP-04": "the AI lead (R11)", "EP-01": "the tenant administrator (R12)",
        "EP-17": "a startup head (R02)", "EP-18": "an automation lead (R11)", "EP-21": "a release manager (R13)", "EP-07": "a visitor on a tenant-owned site (R18)"}
for f in FR:
    ep = f[5] if f[5].startswith("EP-") else "EP-19"
    epc[ep] += 1
    us = f"US-{ep[3:]}-YG{epc[ep]:02d}"
    US.append([us, f[0], f"As {PERS.get(ep, 'a permitted user')}, I want {f[1][:120]} so that the V12 behaviour is available with scope, consent and approval controls intact",
               f"Given my role and grants When I use {f[2]} Then {TC_BASE}{int(f[0].split('-')[-1]) * 2 - 1:03d} and {TC_BASE}{int(f[0].split('-')[-1]) * 2:03d} pass"])
write("us.md", tbl(["Story", "FR", "Story", "Acceptance criteria"], US))
print("rendered", len(ROWS), "aspects;", len(FR), "FR;", len(TCS), "TC;", len(US), "US")
for fn in sorted(os.listdir(OUT)):
    print(fn, os.path.getsize(OUT + "/" + fn))
