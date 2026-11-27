"""Group J document generator.

Reads J_data.json (from J_build_data.py) and the hand-written templates in
J_templates/, fills every {{PLACEHOLDER}} with generated tables, writes the three
Part 8.3 files and the coverage CSV.

Usage:
  python3 -I J_build_docs.py <J_data.json> <blueprint_dir>
"""
import csv, json, os, re, sys
from collections import Counter, OrderedDict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from J_maps import CONTROL_MAP, DIM_ROLE, OKPI_MAP, SCEN_MAP, D38_RECON, D34, D35, D33_EXTRA, D36_EXTRA  # noqa: E402

D = json.load(open(sys.argv[1], encoding="utf-8"))
BP = sys.argv[2]
D["d38"]["kpi_mandatory"] = {int(k): v for k, v in D["d38"]["kpi_mandatory"].items()}
TPL = os.path.join(os.path.dirname(os.path.abspath(__file__)), "J_templates")


def esc(s):
    return str(s).replace("|", "/").replace("\n", " ").strip()


def table(header, rows):
    out = ["| " + " | ".join(header) + " |", "|" + "|".join(["---"] * len(header)) + "|"]
    for r in rows:
        out.append("| " + " | ".join(esc(c) for c in r) + " |")
    return "\n".join(out)


# ------------------------------------------------------------------ screen dataset
nav = {n["id"]: n for n in D["d33"]["nav"]}
prac = {p["id"]: p for p in D["d33"]["practice"]}
fr = D["bp"]["fr"]
scr = D["bp"]["screens"]
rbac = D["bp"]["rbac"]
rtm = D["bp"]["rtm"]
ALL = [f"W{i:02d}" for i in range(1, 35)] + [f"A{i:03d}" for i in range(1, 114)]
NEW = ["W31", "W32", "W33", "W34", "A109", "A110", "A111", "A112", "A113"]

# practice families (doc 33 "Success and troubleshooting" domain sentences)
FAM = OrderedDict([
 ("PF-PUB", ("Publication and public projection", r"Test verified domain, approved immutable revision", "Verified host; approved revision R2; draft R3; stale CDN entry", "Only R2 served; R3 404 on public host; publish/rollback swaps pointer and purges tenant cache ≤ 60 s", "Wrong tenant/domain → 404; unapproved version rejected", "BRL-PUB-01/02/05; NFR-020")),
 ("PF-PRV", ("Private preview and staged publication", r"preview not indexed", "Preview link (24 h grant); approval by a second person", "Preview `noindex`; only approved hash becomes public; audit retained", "Author approves own page → denied (BRL-APR-01)", "BRL-PUB-03; BRL-APR-01/02")),
 ("PF-CMP", ("Campaign audience, budget and attribution", r"Test eligible audience, approved campaign budget", "Audience of 50 eligible + 2 suppressed; budget INR 5,000.00; duplicate attribution event", "Suppressed excluded; spend stops at cap; attribution counted once", "Exhausted spend → pause; unapproved publish denied", "BRL-MKT-04/05; BRL-ELG-02")),
 ("PF-EVD", ("Research evidence and provenance", r"Provide duplicate, stale, restricted and missing evidence", "Duplicate page, stale source (> freshness SLA), restricted source, missing licence", "Provenance kept; unknown stays Unknown; blocked sources never fetched; score never overrides eligibility", "Restricted source fetch → blocked and logged", "BRL-SRC-01…09; BRL-SCR-02/04")),
 ("PF-DSP", ("Automation dispatch and exactly-once", r"Simulate without external effects", "Workflow run in simulation; identical event replayed; transient then permanent provider failure", "Simulation: 0 provider calls; one logical outcome; durable exception record", "Stop after planning, before dispatch → no external call", "BRL-AUT-04/07/08; NFR-038")),
 ("PF-ORD", ("Buy/sell orders and fulfilment", r"Validate direction \(buy vs sell\)", "Sell order 2 × SKU-A @ INR 150.00; delivery 1 + 1 with same key; extra 2", "Decimal totals recomputed; duplicate no effect; over-delivery rejected; partial delivery retained; separate payable/receivable", "Unapproved discount → rejected", "BRL-ORD-01…06; BRL-QTE-01/02")),
 ("PF-FIN", ("Payment evidence and reconciliation", r"Submit duplicate provider reference", "Payment INR 27,000.00 against invoice; duplicate provider ID; wrong currency USD; out-of-order callback", "Duplicate no ledger movement; mismatch held in reconciliation with evidence", "Wrong issuer/account → discrepancy, not allocation", "BRL-FIN-02…05; DEC-027")),
 ("PF-MED", ("MedMaarg non-clinical boundary", r"Check approved nonclinical claims", "Hospital enquiry with diagnosis text; claim not in approved list", "Clinical text quarantined; only approved non-clinical claims usable", "Unapproved healthcare outcome claim → cannot approve", "BRL-ELG-14; BRL-LCY-02; BRL-MKT-01")),
 ("PF-EDU", ("EduVerse safeguarding and routing", r"Check learner eligibility", "Student enquiry (age 16); institution enquiry; external AI-development request", "No direct outreach to minor; guardian/institution path; development → AppNAI", "Child data in discovery → blocked", "BRL-ELG-13; BRL-BID-06; DEC-030")),
 ("PF-REN", ("Renewal and retention eligibility", r"Verify actual eligible renewal date", "Contract end 2027-12-31; customer suppressed on 2027-10-01", "No renewal message after suppression or cancellation; renewal date from contract", "Cancelled contract → no reminder", "BRL-CTR-05; BRL-ELG-02")),
 ("PF-TEN", ("Tenant and membership isolation", r"Use two tenants and two startup memberships", "Tenants T-A, T-B with identical external identifiers", "Only own-scope rows; cross-scope access denied and audited", "Wrong product/tenant/startup → 403", "BRL-TEN-01…04; NFR-032")),
 ("PF-REV", ("Mid-session revocation and revisions", r"Revoke permission mid-session", "Permission revoked while form open; template revision changed", "Server scope and pinned revision authoritative; next action denied ≤ 60 s", "Stale revision → 409", "NFR-050; NFR-025; BRL-AUT-03")),
 ("PF-VAL", ("Input validation and unauthorized object", r"Use valid scoped input, then missing required field", "Valid record; missing mandatory field; other tenant object ID", "Field-level error; no mutation; 404 for foreign object", "No false success message", "NFR-015; BRL-TEN-04")),
 ("PF-FLT", ("Typed filters, cursor and export", r"Apply compound typed filters", "Compound filter + sort; startup switch mid-request; export request", "Stale request aborted; totals equal source; unauthorized export denied", "Scope change clears cache", "NFR-027; NFR-046; BRL-PRV-07")),
 ("PF-RAG", ("Grounded AI and untrusted content", r"Use approved scoped evidence, then remove or expire it", "Approved evidence; then expired; page with injected instruction", "Schema-valid output; unsupported assertion refused; unresolved → reviewer task", "Injected instruction ignored; 0 tool misuse", "BRL-AI-02…05; BRL-SRC-07")),
 ("PF-OUT", ("Eligible outreach and receipts", r"Use a permitted professional contact then introduce opt-out", "Permitted contact; opt-out; recent reply; quiet hours; duplicate key; uncertain receipt", "No duplicate or ineligible delivery; uncertain reconciled before retry", "Opt-out → suppressed at dispatch", "BRL-ELG-02/08/10/18; BRL-AUT-07")),
 ("PF-CNS", ("Consent revocation while queued", r"Apply opt-out or revoked purpose while actions are queued", "Queued sends; opt-out arrives; legal hold on record", "Pending actions suppressed at dispatch; held data restricted not leaked", "Revoked purpose → no send", "BRL-ELG-18; BRL-PRV-04")),
 ("PF-BID", ("Bid deadline and submission evidence", r"Reject an expired deadline", "Deadline 2030-06-01 09:00 UTC; missing mandatory document", "Submission blocked; exception task; human submission recorded only with evidence", "Unauthorized submission → denied", "BRL-BID-01…05")),
 ("PF-APR", ("Hash-bound approval", r"Attempt obsolete revision and unauthorized approver", "Approved revision R1; edit to R2; approver without authority", "Changed hash voids approval; issue/sign blocked until current approval", "Rejected action does not bind company", "BRL-APR-01/02; BRL-QTE-06")),
 ("PF-DOC", ("Document grants and quarantine", r"Test valid grant and approved clean document", "Valid grant; revoked grant; other tenant object; quarantined file", "Clean document downloadable once per grant; denied paths issue no signed URL", "Quarantined file never served", "NFR-021; BRL-TEN-04")),
 ("PF-BUD", ("Entitlement and budget reservation", r"Use allowed entitlement and remaining budget", "Remaining budget; exhausted quota; paid fallback disabled", "Atomic reservation; unapproved provider call rejected", "Over quota → block (BRL-SVC-03)", "NFR-014; BRL-AI-08; BRL-SVC-03")),
 ("PF-MTG", ("Booking and attendance", r"Use an available slot then a conflicting booking", "Free slot; conflicting booking; expired invitation", "No double booking; provider confirmation stored; attendance ≠ consent", "Expired invitation → denied", "BRL-MTG-01/02/05")),
 ("PF-AUTH", ("External authentication", r"Correct external audience, no staff privileges", "Customer login; revoked session", "External audience only; revoked session denied", "Staff route → 403", "BRL-TEN-02; NFR-003")),
])


def families(sid):
    s = prac.get(sid, {}).get("success", "")
    return [k for k, v in FAM.items() if re.search(v[1], s)]


# training modules by screen
MODULES = OrderedDict([
 ("TM-04", ("Workspace, identity and tenant administration", ["A001", "A002", "A003", "A099", "A100", "A106"])),
 ("TM-05", ("Product truth, knowledge and launch readiness", ["A004", "A005", "A006", "A097", "A098"])),
 ("TM-06", ("Consent, privacy and compliance operations", ["A007", "A013", "A047"])),
 ("TM-07", ("Integrations, sources and AI configuration", ["A008", "A010", "A011", "A036", "A041", "A044", "A049", "A053", "A086"])),
 ("TM-08", ("Audit, cost, budget and platform health", ["A009", "A012", "A014", "A090"])),
 ("TM-09", ("Market discovery and research", ["A015", "A016", "A017", "A018", "A019", "A020", "A021", "A023", "A048", "A085"])),
 ("TM-10", ("Qualification and contact verification", ["A022", "A024", "A025", "A026", "A027", "A028"])),
 ("TM-11", ("CRM pipeline and Customer 360", ["A029", "A030", "A031", "A032"])),
 ("TM-12", ("Outreach, inbox, sequences and omnichannel", ["A034", "A035", "A037", "A038", "A039", "A045", "A046"])),
 ("TM-13", ("Meetings, webinars and events", ["A040", "A062", "A063"])),
 ("TM-14", ("Content, claims, SEO and social", ["A050", "A051", "A052", "A054", "A055"])),
 ("TM-15", ("Website, landing pages and publication", ["A056", "A057", "A107", "A108"])),
 ("TM-16", ("Campaigns, advertising and referrals", ["A058", "A059", "A060", "A061", "A064"])),
 ("TM-17", ("Proposals, quotes, negotiation and contracts", ["A065", "A066", "A067", "A068", "A069", "A070", "A071", "A072"])),
 ("TM-18", ("Bid and tender desk (AppNAI route)", ["A104"])),
 ("TM-19", ("Purchase, sales order and fulfilment desk (OrganicSpec route)", ["A105"])),
 ("TM-20", ("Payments, closure, revenue and attribution", ["A073", "A074", "A082", "A083"])),
 ("TM-21", ("Onboarding, partners, renewal and lost deals", ["A075", "A076", "A077", "A078", "A079", "A080", "A081"])),
 ("TM-22", ("Dashboards, forecast and command centre", ["A042", "A043", "A087", "A088", "A089"])),
 ("TM-23", ("Expansion pilots and licensing", ["A091", "A092", "A093", "A094", "A095", "A096"])),
 ("TM-24", ("Automation engineering and live operations", ["A033", "A102", "A109", "A110", "A111", "A112", "A113"])),
 ("TM-25", ("SaaS billing, import/export and portability", ["A101", "A103"])),
 ("TM-26", ("AI quality and feedback review", ["A084"])),
 ("TM-31", ("Customer and supplier portal self-service", ["W06", "W14", "W15", "W16", "W17", "W18", "W21", "W22", "W23", "W24", "W25", "W26", "W27", "W28", "W29"])),
 ("TM-32", ("SaaS client onboarding and service portal", ["W31", "W32", "W33", "W34"])),
 ("TM-33", ("Public website and assistant (help content, verified by marketing)", ["W01", "W02", "W03", "W04", "W05", "W07", "W08", "W09", "W10", "W11", "W12", "W13", "W19", "W20", "W30"])),
])
MOD_OF = {s: m for m, (t, ss) in MODULES.items() for s in ss}
assert set(MOD_OF) == set(ALL), set(ALL) - set(MOD_OF)

ROLE_NAMES = {"R01": "Founder", "R02": "Startup Head", "R03": "Growth Manager", "R04": "Research Analyst", "R05": "Marketing Specialist",
              "R06": "Bid Manager", "R07": "Order Coordinator", "R08": "Finance Maker", "R09": "Finance Checker", "R10": "Legal/DPO",
              "R11": "Automation Lead", "R12": "Tenant Admin", "R13": "Platform Support", "R14": "Platform Billing", "R15": "Auditor"}
EXT = {"W": None}


def operators(sid):
    if sid.startswith("W"):
        n = int(sid[1:])
        if n <= 11 or n in (19, 20, 30):
            return "R18 visitor (R16/R17 view)", "Marketing (R05) verifies publication"
        if 12 <= n <= 18:
            return "R18 / R16 / R17 submit", "R03 triages in A029/A031"
        if n == 21:
            return "R16, R17 (self)", "R12 manages invitations"
        if 22 <= n <= 28:
            return "R16 (own records via grants)", "R03/R06/R07/R08 counterpart screens"
        if n == 29:
            return "R16/R17 own; R18 signed token", "R10 monitors A007/A047"
        if n == 31:
            return "R18, R16, R17 view", "Service Owner approves plans in A101"
        if n in (32, 33):
            return "R17 (own draft)", "R12/Founder approve in A099"
        if n == 34:
            return "R17 (own tenant)", "R13/R14 in A099/A101"
    perms = rbac.get(sid, {})
    op = [r for r, p in perms.items() if re.search(r"\b[CEAXS]\b|[CEAXS]\(", p)]
    vw = [r for r, p in perms.items() if r not in op]
    return ", ".join(op) or "—", ", ".join(vw) or "—"


def tc_short(sid):
    r = rtm.get("FR-" + sid, {})
    t = r.get("tc_ids", "")
    parts = [p.strip() for p in t.split(",") if p.strip()]
    return ", ".join(parts[:3]) + (f" (+{len(parts) - 3})" if len(parts) > 3 else "")


def task_text(sid):
    s = scr[sid]
    acts = s["actions"]
    return acts


GENERIC = "Open the named function within the assigned workspace"


def purpose_of(sid):
    """doc 33 purpose line; for the Admin entries whose doc 33 line is generic, the Part 2.1 FR text."""
    n = nav.get(sid)
    if n and not n["purpose"].startswith(GENERIC):
        return n["purpose"]
    f = fr["FR-" + sid]
    if sid.startswith("A"):
        return f["surface"] + (" (FR-" + sid + "; doc 33 line generic)" if n else " (FR-" + sid + ")")
    return f["requirement"] + " (FR-" + sid + ")"


def card_rows(ids):
    rows = []
    for sid in ids:
        s = scr[sid]
        n = nav.get(sid)
        purpose = purpose_of(sid)
        fams = families(sid) if sid in prac else []
        op, vw = operators(sid)
        if sid in prac:
            uat = prac[sid]["uat"]
        else:
            uat = f"SM-UX-UAT-{sid}"
        drill = "; ".join(FAM[f][4] for f in fams[:2]) if fams else NEWDRILL.get(sid, "")
        practice = "; ".join(f"{f} {FAM[f][0]}" for f in fams) if fams else NEWPRAC.get(sid, "")
        rows.append([f"TRN-SCR-{sid}", f"{sid} {s['title']}", MOD_OF[sid], op, purpose, s["actions"], practice, drill,
                     f"{uat}; SM-UX-UAT-{sid}" if sid in prac else uat, tc_short(sid)])
    return rows


NEWPRAC = {
 "W31": "Read approved plans and terms; open demo request; confirm no private offers or implied outcomes",
 "W32": "Register synthetic client 'Alpha Retail' with administrator proof; observe 'pending verification'",
 "W33": "Complete wizard draft; review AI proposals marked Unverified; run dry-run cost report (0 live calls)",
 "W34": "Open own service overview; request support, plan change and export; view invoices",
 "A109": "Create trigger revision; verify webhook signature test; approve and enable; disable",
 "A110": "Inspect 20 concurrent simulated runs; pause one; resume (policy revalidated); open UNKNOWN step",
 "A111": "Two workflows target one relationship; hold competing action; resolve with reason",
 "A112": "Propose configuration revision 2; simulate; approve; activate; roll back",
 "A113": "Clone template; edit node parameters; test with fixtures; submit for approval; publish; deprecate",
}
NEWDRILL = {
 "W31": "Unapproved plan price never shown ('Price on request')",
 "W32": "Provisioning attempt before verification → blocked (BRL-SVC-01)",
 "W33": "Applicant tries to mutate active startup → denied (BRL-SVC-02)",
 "W34": "Other tenant invoice ID → 404",
 "A109": "Invalid signature → rejected; replay → single event",
 "A110": "Retry of UNKNOWN before reconciliation → blocked (BRL-AUT-07)",
 "A111": "Unrelated tenant conflict never visible",
 "A112": "Running runs keep pinned revision (BRL-AUT-03); authorization expansion needs review",
 "A113": "Code node or secret value in parameters → rejected (BRL-AUT-02)",
}

# ------------------------------------------------------------------ coverage aspects
aspects = []  # doc, section, id, summary, status, location, action, new_ids


def add(doc, section, aid, summary, status, loc, action, new=""):
    aspects.append([doc, section, aid, summary, status, loc, action, new])


for (aid, sec, summ, st, loc, act, new) in D33_EXTRA:
    add("33", sec, aid, summ, st, loc, act, new)
for sid in ALL:
    if sid in nav:
        n = nav[sid]
        add("33", "Screen navigation guide", f"33-NAV-{sid}", f"{sid} {n['title']} ({n['access']}): {purpose_of(sid)}", "Partially covered",
            f"Part 2.5 §2.43 ({scr[sid]['group']}); FR-{sid}", "Screen exists with FR, stories and tests; no operating procedure for users. Added training task card", f"TRN-SCR-{sid}; {MOD_OF[sid]}")
        p = prac[sid]
        fams = families(sid)
        add("33", "Practice procedure and UAT", f"33-UAT-{sid}", f"{p['uat']} {sid} trainee '{p['trainee']}'; families {', '.join(fams)}", "Covered",
            f"Part 6.6 RTM FR-{sid} alias {p['uat']}; {tc_short(sid)}", "Alias resolves to test cases; reused as training practice", f"TRN-SCR-{sid}")
    else:
        add("33", "Expansion training", f"33-NEW-{sid}", f"{sid} {scr[sid]['title']}: training practice for new interface", "Not covered",
            f"Part 2.5 §2.43; FR-{sid}", "Training task card and exercise added", f"TRN-SCR-{sid}; {MOD_OF[sid]}")
for (aid, sec, summ, st, loc, act, new) in D34:
    add("34", sec, aid, summ, st, loc, act, new)
for (aid, sec, summ, st, loc, act, new) in D35:
    add("35", sec, aid, summ, st, loc, act, new)
dims = D["d36"]["dims"]
for i, d in enumerate(dims, 1):
    add("36", "Weighted scorecard", f"36-DIM-{i:02d}", f"OPT-{i:02d} {d['name']} weight {d['weight']}%; accountable {d['owner']}", "Not covered",
        "—", "Dimension added with weight and blueprint owner", f"OPT-{i:02d}")
for c in D["d36"]["controls"]:
    st, refs, enh = CONTROL_MAP[c["id"]]
    add("36", f"Controls: {c['dim']}", c["id"], f"{c['name']}: {c['control']}", st, refs, "Mapped" + ("" if enh == "—" else f"; {enh}"),
        "")
for k in D["d36"]["kpis"]:
    m = OKPI_MAP[k["n"]]
    add("36", "KPI acceptance matrix", f"OKPI-{k['n']:02d}", f"{k['metric']} {k['target']} ({k['context']})", m[3], f"{m[0]}; {m[1]}", m[4], f"OKPI-{k['n']:02d}")
for s in D["d36"]["scenarios"]:
    sm = SCEN_MAP[s["n"]]
    add("36", "Executable acceptance planning", f"OPT-TEST-{s['n']:02d}", f"{s['dim']}: {s['test']}", "Not covered", "—",
        "Scenario specified as test case", sm[0])
for i, r in enumerate(D["d36"]["uxqc"], 1):
    add("36", "Expansion UX-QC", r[0], r[1], "Partially covered", "EP-18/EP-20 stories and TCs", "Wrapped as acceptance test", f"TC-ENH-J-{24 + i:03d}")
for (aid, sec, summ, st, loc, act, new) in D36_EXTRA:
    add("36", sec, aid, summ, st, loc, act, new)
for i, (sec, metric, src, bpv, st, expl) in enumerate(D38_RECON, 1):
    add("38", f"§{sec}", f"38-{i:02d}", f"{metric}: {src}", st, bpv, expl, "")
for n, v in sorted(D["d38"]["kpi_mandatory"].items()):
    m = OKPI_MAP[n]
    add("38", "§07–08 KPI thresholds", f"38-OKPI-{n:02d}", f"KPI-{n:02d} {v['metric']} {v['target']} mandatory={v['mandatory']}", m[3], f"{m[0]}; {m[1]}", "Renamed OKPI (ID collision with KPI-01…31)", f"OKPI-{n:02d}")
for t in D["d38"]["tables"]:
    if t["header"][:1] == ["Category"]:
        for r in t["rows"]:
            add("38", "§09 Automation categories", f"38-CAT-{r[0][:12]}", f"{r[0]}: {r[1]} use cases", "Partially covered", "Part 9.4 catalogue", "GAP-490 (library content owned by automation group)", "")

status_order = ["Covered", "Partially covered", "Not covered", "Conflict", "Not applicable"]
cnt = {d: Counter(a[4] for a in aspects if a[0] == d) for d in ("33", "34", "35", "36", "38")}

# ------------------------------------------------------------------ tables for templates
P = {}
DOCMETA = {
 "33": ("End User, Administrator & Operational Training Manual", D["d33"]),
 "34": ("SaaS Client Onboarding, Service Delivery, SLA & Commercial Operations", D["d34"]),
 "35": ("Product Maintenance, Continuous Improvement & Lifecycle Management", D["d35"]),
 "36": ("Comprehensive Product Optimization Engineering", D["d36"]),
 "38": ("Sales & Marketing Automation — All Numbers", D["d38"]),
}
P["STATUS_SUMMARY"] = table(["Document", "Aspects"] + status_order,
    [[f"{d} {DOCMETA[d][0]}", sum(cnt[d].values())] + [cnt[d].get(s, 0) for s in status_order] for d in cnt] +
    [["**Total**", sum(sum(c.values()) for c in cnt.values())] + [sum(c.get(s, 0) for c in cnt.values()) for s in status_order]])
P["DOC_SIZES"] = table(["Doc", "Title", "Bytes (text extraction)", "Lines", "Atomic aspects"],
    [[d, DOCMETA[d][0], f"{DOCMETA[d][1]['bytes']:,}", DOCMETA[d][1]['lines'], sum(cnt[d].values())] for d in cnt])

def reg(doc, prefix=None, only_non_covered=False):
    rows = [a for a in aspects if a[0] == doc and (prefix is None or a[2].startswith(prefix))]
    if only_non_covered:
        rows = [a for a in rows if a[4] != "Covered"]
    return table(["Aspect", "Section", "Summary", "Status", "Blueprint location", "Action", "New IDs"], [[a[2], a[1], a[3], a[4], a[5], a[6], a[7]] for a in rows])

P["REG_D33_EXTRA"] = reg("33", "33-0") + "\n" + "\n".join(reg("33", "33-").split("\n")[2:]) if False else table(
    ["Aspect", "Section", "Summary", "Status", "Blueprint location", "Action", "New IDs"],
    [[a[2], a[1], a[3], a[4], a[5], a[6], a[7]] for a in aspects if a[0] == "33" and re.match(r"33-\d\d$", a[2])])
P["REG_D33_SCREENS"] = table(["Screen", "Access (doc 33)", "Purpose (doc 33, or FR text where doc 33 is generic)", "Navigation-procedure status", "UAT alias status", "Blueprint location", "New IDs"],
    [[sid, nav[sid]["access"] if sid in nav else "new", purpose_of(sid),
      "Partially covered" if sid in nav else "Not covered", "Covered" if sid in prac else "Covered (SM-UX-UAT)",
      f"FR-{sid}; {scr[sid]['group'].split(' (')[0]}", f"TRN-SCR-{sid}"] for sid in ALL])
P["REG_D34"] = reg("34")
P["REG_D35"] = reg("35")
P["REG_D36_EXTRA"] = reg("36", "36-")
P["REG_D38"] = table(["Aspect", "Section", "Inventory item (source value)", "Status", "Blueprint value", "Explanation"],
    [[a[2], a[1], a[3], a[4], a[5], a[6]] for a in aspects if a[0] == "38" and re.match(r"38-\d\d$", a[2])])

# screens reconciliation
title_diff = []
def norm(s): return re.sub(r"[^a-z0-9]", "", s.lower().replace("&", "and").replace("catalog", "catalogue").replace("fulfillment", "fulfilment"))
for sid in ALL:
    if sid in nav and norm(nav[sid]["title"]) != norm(fr["FR-" + sid]["title"]):
        title_diff.append([sid, nav[sid]["title"], fr["FR-" + sid]["title"], scr[sid]["title"]])
P["TITLE_DIFF"] = table(["Screen", "Doc 33 title", "Part 2.1 FR title", "Part 2.5 screen title"], title_diff)
P["N_TITLE_DIFF"] = str(len(title_diff))
acc = Counter(n["access"] for n in nav.values())
P["ACCESS_COUNTS"] = ", ".join(f"{k} {v}" for k, v in acc.items())
fam_counts = Counter(f for sid in prac for f in families(sid))
P["FAMILY_TABLE"] = table(["Family", "Name", "Screens (count)", "Synthetic input", "Expected result", "Negative drill", "Rules / NFR"],
    [[k, v[0], f"{', '.join(s for s in prac if k in families(s))} ({fam_counts[k]})", v[2], v[3], v[4], v[5]] for k, v in FAM.items()])
nofam = [s for s in prac if not families(s)]
P["NOFAM"] = ", ".join(nofam) if nofam else "none"
P["N_SMUAT_RESOLVED"] = str(len(set(p["uat"] for p in prac.values()) & set(D["bp"]["smuat_refs"])))

# per view task cards
GROUPS = OrderedDict()
for sid in ALL:
    GROUPS.setdefault(scr[sid]["group"], []).append(sid)
hdr = ["Card", "Screen", "Module", "Operators (C/E/A/X/S)", "Purpose (doc 33 / FR)", "Key actions (Part 2.5)", "Practice families", "Denied / edge drill", "UAT aliases", "Blueprint TCs"]
cards = []
for g, ids in GROUPS.items():
    cards.append(f"#### {g}\n\n" + table(hdr, card_rows(ids)))
P["TASK_CARDS"] = "\n\n".join(cards)

# modules table
mod_rows = []
for m, (t, ss) in MODULES.items():
    ops = Counter()
    for s in ss:
        o, _ = operators(s)
        for r in re.findall(r"R\d\d", o):
            ops[r] += 1
    eps = Counter(rtm.get("FR-" + s, {}).get("epic", "") for s in ss)
    us = sorted(set(u for s in ss for u in rtm.get("FR-" + s, {}).get("us", "").split() if u))
    labmin = 12 * len(ss)
    mod_rows.append([m, t, f"{len(ss)}: {', '.join(ss)}", ", ".join(r for r, _ in ops.most_common(6)) or "external", ", ".join(e for e in eps if e),
                     f"{labmin // 60} h {labmin % 60:02d} min", f"{len(us)} stories ({us[0]}…{us[-1]})" if us else "—"])
P["MODULE_TABLE"] = table(["Module", "Title", "Screens", "Primary operator roles", "Epics", "Screen-lab time (12 min/screen)", "Linked stories"], mod_rows)

# role matrix
roles = [f"R{i:02d}" for i in range(1, 16)]
rm_rows = []
for r in roles:
    op = [s for s in ALL if s.startswith("A") and r in operators(s)[0].split(", ")]
    vw = [s for s in ALL if s.startswith("A") and r in rbac.get(s, {}) and s not in op]
    mods = sorted(set(MOD_OF[s] for s in op))
    rm_rows.append([r, ROLE_NAMES[r], len(op), ", ".join(op) if op else "—", len(vw), ", ".join(mods) or "—", f"{(len(op) * 12 + len(vw) * 4) / 60:.1f} h"])
P["ROLE_MATRIX"] = table(["Role", "Name", "Operator screens", "Operator screen IDs", "View-only screens", "Modules required", "Screen-lab time (12 min operate + 4 min view)"], rm_rows)

# dimensions
P["DIM_TABLE"] = table(["Dim", "Dimension", "Weight", "Source accountable role", "Blueprint owner", "Controls", "OKPIs", "Scenario"],
    [[f"OPT-{i:02d}", d["name"], f"{d['weight']}%", d["owner"], DIM_ROLE.get(d["owner"], d["owner"]),
      sum(1 for c in D["d36"]["controls"] if c["dim_no"] == i), "", f"OPT-TEST-{i:02d}"] for i, d in enumerate(dims, 1)]
    + [["G0", "Blocking gate (non-weighted) [CONFLICT-486]", "0% (blocking)", "Security, privacy, financial and mandatory delivery leads", "Veto holders of Part 8.2 §8.2.4.1", "21 mandatory OKPIs", "", "OPT-TEST-17"]])
# fill OKPI per dim mapping (hand)
OKPI_DIM = {1: [1, 2, 3, 4], 2: [5, 26, 27, 28, 29, 30, 31], 3: [11, 12, 21], 4: [9, 10, 35], 5: [6, 7, 8], 6: [], 7: [], 8: [22], 9: [27], 10: [13, 14],
            11: [15], 12: [24, 25], 13: [], 14: [], 15: [23], 16: [], 17: [16, 17, 20], 18: [18, 19, 32, 33, 34], 19: [35], 20: [21]}
lines = P["DIM_TABLE"].split("\n")
for i in range(1, 21):
    cells = lines[i + 1].split(" | ")
    cells[6] = ", ".join(f"OKPI-{k:02d}" for k in OKPI_DIM[i]) or "—"
    lines[i + 1] = " | ".join(cells)
P["DIM_TABLE"] = "\n".join(lines)

# controls table
crow = []
for c in D["d36"]["controls"]:
    st, refs, enh = CONTROL_MAP[c["id"]]
    pre = "yes" if c["id"] in D["bp"]["opt_refs"] else "no"
    crow.append([c["id"], c["name"], c["control"], c["acceptance"], DIM_ROLE.get(c["owner"], c["owner"]), refs, pre, st, enh])
P["CONTROL_TABLE"] = table(["Control", "Name", "Control (source)", "Acceptance / evidence (source)", "Blueprint owner", "Blueprint mapping", "Cited before", "Status", "Enhancement"], crow)
cst = Counter(CONTROL_MAP[c["id"]][0] for c in D["d36"]["controls"])
P["CONTROL_COUNTS"] = ", ".join(f"{k} {v}" for k, v in cst.items())
P["N_OPT_PRE"] = str(len(D["bp"]["opt_refs"]))
bydim = []
for i, d in enumerate(dims, 1):
    cs = [c for c in D["d36"]["controls"] if c["dim_no"] == i]
    cc = Counter(CONTROL_MAP[c["id"]][0] for c in cs)
    bydim.append([f"OPT-{i:02d}", d["name"], len(cs), sum(1 for c in cs if c["id"] in D["bp"]["opt_refs"])] + [cc.get(s, 0) for s in status_order[:4]])
bydim.append(["", "**Total**", sum(r[2] for r in bydim), sum(r[3] for r in bydim)] + [sum(r[4 + k] for r in bydim) for k in range(4)])
P["RECON_OPT_BY_DIM"] = table(["Dim", "Dimension", "Controls", "Cited in blueprint before", "Covered", "Partially covered", "Not covered", "Conflict"], bydim)

# OKPI table
orow = []
for k in D["d36"]["kpis"]:
    m = OKPI_MAP[k["n"]]
    mand = D["d38"]["kpi_mandatory"][k["n"]]["mandatory"]
    orow.append([f"OKPI-{k['n']:02d}", k["metric"], k["target"], "Yes" if mand == "Yes" else "No", k["context"], m[0], m[1], m[2], m[5], m[6], m[3], m[4]])
P["OKPI_TABLE"] = table(["OKPI", "Metric", "Target", "Mandatory (blocking)", "Measurement context (source)", "Blueprint NFR", "Blueprint KPI / SLO", "Tests", "Screen", "Owner", "Status", "Note"], orow)
ost = Counter(OKPI_MAP[k][3] for k in OKPI_MAP)
P["OKPI_COUNTS"] = ", ".join(f"{k} {v}" for k, v in ost.items())
P["N_MAND"] = str(sum(1 for v in D["d38"]["kpi_mandatory"].values() if v["mandatory"] == "Yes"))
P["MAND_LIST"] = ", ".join(f"OKPI-{n:02d}" for n, v in sorted(D["d38"]["kpi_mandatory"].items()) if v["mandatory"] == "Yes")

# scenarios table
srow = []
for s in D["d36"]["scenarios"]:
    sm = SCEN_MAP[s["n"]]
    srow.append([sm[0], f"OPT-TEST-{s['n']:02d}", s["dim"], s["test"], s["expected"], sm[3], sm[4], sm[1], sm[2]])
P["SCEN_TABLE"] = table(["Test case", "Source scenario", "Dimension / route", "Source test", "Source expected", "Synthetic data and steps (blueprint)", "Expected result (measurable)", "OKPIs", "Rules / NFR"], srow)
uxrow = []
UXMAP = ["US-2012, US-0105; TC-ENH-J-014", "BRL-BID-06; US-2004", "BRL-AUT-03; LT-06", "BRL-AUT-08/09", "BRL-ELG-02/10; RP-07", "NFR-014, NFR-026", "BRL-QTE-01; BRL-FIN-06", "US-2002, US-2008; BRL-PUB-05", "BRL-AUT-03; BRL-SVC-06; US-2010", "NFR-088; NFR-098"]
for i, r in enumerate(D["d36"]["uxqc"], 1):
    uxrow.append([f"TC-ENH-J-{24 + i:03d}", r[0], r[1], r[2], UXMAP[i - 1]])
P["UXQC_TABLE"] = table(["Test case", "Source control", "Verification (source)", "Acceptance (source)", "Blueprint basis"], uxrow)
P["BENCH_TABLE"] = table(["Candidate", "Compare", "Guardrail / decision"], D["d36"]["bench"])
P["PANEL"] = "\n".join(f"- `{l}`" for l in D["d36"]["panel"])
P["RECON_D38"] = P["REG_D38"]
P["N_ASPECTS"] = str(len(aspects))
P["N_GENERIC"] = str(sum(1 for n in nav.values() if n["purpose"].startswith(GENERIC)))
P["P_ACCESS"] = P["ACCESS_COUNTS"]
for d in cnt:
    P[f"N_D{d}"] = str(sum(cnt[d].values()))

# ------------------------------------------------------------------ write files
for name in sorted(os.listdir(TPL)):
    if not name.endswith(".md"):
        continue
    txt = open(os.path.join(TPL, name), encoding="utf-8").read()
    def sub(m):
        k = m.group(1)
        if k not in P:
            raise KeyError(k)
        return P[k]
    txt = re.sub(r"\{\{([A-Z0-9_]+)\}\}", sub, txt)
    open(os.path.join(BP, name), "w", encoding="utf-8").write(txt)
    print("wrote", name, len(txt))

os.makedirs(os.path.join(BP, "final", "coverage"), exist_ok=True)
with open(os.path.join(BP, "final", "coverage", "J_coverage.csv"), "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["doc", "section", "aspect_id", "aspect_summary", "status", "blueprint_location", "action", "new_ids"])
    for a in aspects:
        w.writerow(a)
print("aspects", len(aspects), {d: dict(c) for d, c in cnt.items()})
print("controls", dict(cst), "okpi", dict(ost), "families", dict(fam_counts), "nofam", nofam)
