#!/usr/bin/env python3
"""Group D: build Markdown table fragments and the coverage CSV for Part 3.5 (doc 07 reconciliation).

Usage: python3 -I D_build_07.py <d07.json> <map.json> <providers.json> <frag_dir> <coverage.csv>
Fragments are inserted into the hand-written Part 3.5 skeletons by D_assemble_07.py.
"""
import csv
import json
import os
import re
import sys
from collections import Counter, OrderedDict

d = json.load(open(sys.argv[1]))
rows = json.load(open(sys.argv[2]))
prov = json.load(open(sys.argv[3]))
FR = sys.argv[4]
os.makedirs(FR, exist_ok=True)
bp = {b["id"]: b for b in d["bpops"]}
ops = {o["num"]: o for o in d["ops"]}

DOM = OrderedDict([
    ("Identity", "IDN"), ("Tenancy", "TEN"), ("Catalogue", "CAT"), ("Governance", "GOV"), ("Integrations", "INT"),
    ("Events", "OPS"), ("AI gateway", "AI"), ("Intelligence", "INTL"), ("CRM", "CRM"), ("Engagement", "ENG"),
    ("Marketing", "MKT"), ("Commerce", "COM"), ("Vertical", "DSK"), ("Finance", "FIN"), ("Lifecycle", "LCY"),
    ("Automation", "AUT"), ("Website", "WEB"), ("SaaS", "SVC"), ("Command", "CMD")])


def dcode(b):
    for k, v in DOM.items():
        if b["domain"].startswith(k):
            return v
    return "?"


def esc(s):
    return str(s).replace("|", "\\|").replace("\n", " ")


def write(name, text):
    open(os.path.join(FR, name), "w", encoding="utf-8").write(text)


# Enhancement operations (new) — mirrored in the hand-written §3.5.5.2 detail
ENH = [
    # id, method, path, ns, purpose, source, FR/screen, roles, idem, SE, PDP, RL, domain
    ("API-ENH-D-001", "PATCH", "~/admin/sources/{id}", "admin", "Revise source approval (licence, purpose, scope, expiry) as a new SourcePolicy revision; voids prior approval", "SM-OP-032", "FR-A010; A010", "R04, R10", "If-Match", "W", "—", "RL-ADM", "INTL"),
    ("API-ENH-D-002", "GET", "~/admin/evals/cases", "admin", "List evaluation cases (task, dataset revision, label provenance, tags); cursor", "SM-OP-036", "FR-A011, FR-A084; A011, A084", "R11, R01, R10", "Safe", "R", "—", "RL-ADM", "AI"),
    ("API-ENH-D-003", "POST", "~/admin/signal-types", "admin", "Draft signal taxonomy revision (code, label, vertical, evidence rule)", "SM-OP-065", "FR-A019, FR-A023; A023", "R02, R04 (draft); R02 approves", "Key", "W", "—", "RL-ADM", "INTL"),
    ("API-ENH-D-004", "POST", "~/admin/role-mappings", "admin", "Draft role-mapping rule-set revision (title pattern to decision role hypothesis, confidence)", "SM-OP-075", "FR-A026; A026", "R04 (draft); R02 approves", "Key", "W", "—", "RL-ADM", "INTL"),
    ("API-ENH-D-005", "POST", "~/admin/alerts/{id}/read", "admin", "Mark own research alert read", "SM-OP-084", "FR-A028; A028", "Recipient (own)", "Yes", "W", "—", "RL-ADM", "INTL"),
    ("API-ENH-D-006", "POST", "~/admin/workflows/{id}/resume", "admin", "Resume a paused workflow scope after PDP recheck (budget, consent, approval validity, stop state)", "SM-OP-101", "FR-A033; A033", "R11 (L2), R01 (L3)", "Key + If-Match", "W", "P", "RL-ADM", "AUT"),
    ("API-ENH-D-007", "GET", "~/admin/messages/{id}", "admin", "Single message with delivery state and provider event timeline (provider ref masked)", "SM-OP-110", "FR-A037; A037", "R03, R05, R02 (scope)", "Safe", "R", "—", "RL-ADM", "ENG"),
    ("API-ENH-D-008", "GET", "~/admin/channels/whatsapp/accounts", "admin", "WABA accounts, numbers, quality rating, messaging tier, template counts (never tokens)", "SM-OP-130", "FR-A044; A044", "R11, R02, R10", "Safe", "R", "—", "RL-ADM", "INT"),
    ("API-ENH-D-009", "PUT", "~/admin/chat/settings", "admin", "Website assistant settings per startup: enabled, languages, handover hours, transcript retention, daily AI budget", "SM-OP-138", "FR-A046, FR-W11; A046", "R02; loosening R01 + R10", "If-Match", "W", "P", "RL-ADM", "ENG"),
    ("API-ENH-D-010", "POST", "~/admin/forecast-models/{id}/versions", "admin", "Draft forecast assumption revision (stage probabilities, horizon, seasonality); approval type forecast_model", "SM-OP-230", "FR-A088; A088", "R09, R01 approves", "Key", "W", "—", "RL-ADM", "FIN"),
    ("API-ENH-D-011", "GET", "~/admin/pilots", "admin", "List pilots by type (insurance, partner, institutional), stage, approvals, data-agreement state", "SM-OP-236", "FR-A077, FR-A091; A077, A091, A092", "R02, R01, R10", "Safe", "R", "—", "RL-ADM", "LCY"),
    ("API-ENH-D-012", "POST", "~/admin/domains/{id}/disable", "admin", "Disable brand-domain mapping: host returns 404 UNKNOWN_HOST, tenant-keyed cache purge", "SM-OP-260", "FR-A107; A100, A107", "R12, R01", "Key + If-Match", "W", "—", "RL-ADM", "TEN"),
    ("API-ENH-D-013", "POST", "~/admin/service-invoices/{id}/receipts", "admin", "Record service receipt and reconcile (maker); checker via API-ENH-D-013 action=verify", "SM-OP-266", "FR-A101; A101", "R08 maker, R09 checker (different person)", "Key", "F", "—", "RL-ADM", "SVC"),
    ("API-ENH-D-014", "GET", "~/admin/usage-charges", "admin", "Usage charge ledger: period, dimension, quantity, rate version, amount, adjustments", "SM-OP-267", "FR-A101; A101", "R01, R08, R09, R12 (own tenant)", "Safe", "R", "—", "RL-ADM", "SVC"),
    ("API-ENH-D-015", "POST", "~/admin/usage-charges/{id}/credits", "admin", "Append approved credit adjustment (original charge immutable)", "SM-OP-268", "FR-A101; A101", "R08 maker; R01 approves above threshold", "Key", "F", "—", "RL-ADM", "SVC"),
    ("API-ENH-D-016", "POST", "~/admin/orders/{id}/acceptances", "admin", "Record acceptance or dispute of received goods/services (buy direction) with evidence", "SM-OP-286", "FR-A105; A105", "R07, R02", "Key + If-Match", "F", "—", "RL-ADM", "DSK"),
    ("API-ENH-D-017", "POST", "~/admin/external-grants/{id}/revoke", "admin", "Revoke external portal grant (PortalGrant) immediately; sessions using it re-authorize", "SM-OP-294", "FR-A032, CA-PORTAL; A032", "R02, R03 (assigned), R10", "Key + If-Match", "W", "—", "RL-ADM", "CRM"),
    ("API-ENH-D-018", "POST", "~/portal/uploads/{id}/complete", "portal", "Complete own quarantined upload: checksum match, enqueue malware scan", "SM-OP-297", "FR-W15, FR-W27; W27", "R16 (grant)", "Key", "Q", "—", "RL-PORTAL", "CRM"),
    ("API-ENH-D-019", "GET", "~/portal/onboarding-wizard/{app}", "portal", "Read own applicant configuration draft (JSON, revision, validation state)", "SM-UX-API-03", "FR-W33; W33", "Applicant (verified)", "Safe", "R", "—", "RL-PORTAL", "SVC"),
    ("API-ENH-D-020", "POST", "~/portal/service/offboarding-requests", "portal", "Request offboarding (WF-14) with export preference; no automatic action", "SM-UX-API-07", "FR-W34; W34", "R17 client admin", "Key", "W", "—", "RL-PORTAL", "SVC"),
    ("API-ENH-D-021", "POST", "~/admin/workflow-templates", "admin", "Create workflow template draft (allowlisted nodes, bounded graph, input/output schemas)", "SM-UX-API-18", "FR-A113; A113", "R11", "Key", "W", "—", "RL-ADM", "AUT"),
    ("API-ENH-D-022", "POST", "~/admin/external-grants/{id}/rotate", "admin", "Rotate invitation secret (previous invite invalid), keep grant scope", "SM-OP-294", "FR-A032; A032", "R02, R03 (assigned)", "Key + If-Match", "X", "P+D", "RL-ADM", "CRM"),
    ("API-ENH-D-023", "GET", "~/admin/external-grants", "admin", "List external grants by counterparty/object with expiry and state", "SM-OP-293/294", "FR-A032; A032", "R02, R03 (assigned), R10", "Safe", "R", "—", "RL-ADM", "CRM"),
    ("API-ENH-D-024", "POST", "~/admin/privacy-requests", "admin", "Record privacy request received offline on behalf of a subject (identity verification pending)", "SM-OP-041", "FR-A013; A013", "R10", "Key", "Q", "—", "RL-ADM", "GOV"),
]

# ---------- 1. Full mapping table ----------
REL = {"exact": "Exact", "alias": "Alias", "split": "Split", "approval": "Approval", "partial": "Partial", "none": "New"}
out = ["| Source op | SIT | Method | Source path / adapter | Source boundary | Blueprint operation(s) | Relation | Status | Enhancement |",
       "|---|---|---|---|---|---|---|---|---|"]
for r in rows:
    if r["source_id"].startswith("SM-UX"):
        continue
    out.append(f'| {r["source_id"]} | {r["sit_id"]} | {r["method"]} | `{esc(r["path"])}` | {esc(r["boundary"])} | {r["blueprint_ops"].replace(";", ", ")} | {REL.get(r["relation"], r["relation"])} | {r["status"]} | {r["enhancement"] or "—"} |')
write("map_ops.md", "\n".join(out) + "\n")

out = ["| Candidate | Method | Path | Screen | Audience | Blueprint operation(s) | Relation | Status | Enhancement |",
       "|---|---|---|---|---|---|---|---|---|"]
for r in rows:
    if r["source_id"].startswith("SM-UX"):
        out.append(f'| {r["source_id"]} | {r["method"]} | `{r["path"]}` | {r["module"]} | {esc(r["boundary"])} | {r["blueprint_ops"].replace(";", ", ")} | {REL.get(r["relation"], r["relation"])} | {r["status"]} | {r["enhancement"] or "—"} |')
write("map_cands.md", "\n".join(out) + "\n")

# ---------- 2. Counts ----------
src_ops = [r for r in rows if not r["source_id"].startswith("SM-UX")]
c_rel = Counter(r["relation"] for r in src_ops)
c_rel_c = Counter(r["relation"] for r in rows if r["source_id"].startswith("SM-UX"))
http = [r for r in src_ops if r["method"] != "ADAPTER"]
adp = [r for r in src_ops if r["method"] == "ADAPTER"]
c_h = Counter(r["relation"] for r in http)
c_a = Counter(r["relation"] for r in adp)
order = ["exact", "alias", "split", "approval", "partial", "none"]
t = ["| Relation | Meaning | HTTP (285) | Adapters (17) | Retained total (302) | Candidates (19) | All (321) |", "|---|---|---|---|---|---|---|"]
mean = {"exact": "Same method and path; legacy contract retained in Part 3.2 (104 FRD-named ★ plus 2 same-path)",
        "alias": "Same semantics; Part 3.2 uses the derived `~/` path (or AD-## for adapters)",
        "split": "One source operation (often an `action` enum) maps to several Part 3.2 action sub-resources",
        "approval": "Source per-object approve/review route consolidated into the Approval resource (API-541 submit, API-539 decide)",
        "partial": "Part of the semantics exists; the missing part is added in §3.5.5.2 / §3.5.5.6",
        "none": "No Part 3.2 equivalent; new operation added in §3.5.5.2"}
for k in order:
    t.append(f"| {REL[k]} | {mean[k]} | {c_h.get(k,0)} | {c_a.get(k,0)} | {c_rel.get(k,0)} | {c_rel_c.get(k,0)} | {c_rel.get(k,0)+c_rel_c.get(k,0)} |")
t.append(f"| **Total** | | **{len(http)}** | **{len(adp)}** | **{len(src_ops)}** | **{sum(c_rel_c.values())}** | **{len(rows)}** |")
write("counts_rel.md", "\n".join(t) + "\n")

# boundary x relation
cb = Counter((r["boundary"], r["status"]) for r in src_ops)
bnds = sorted(set(r["boundary"] for r in src_ops), key=lambda b: -sum(v for (bb, s), v in cb.items() if bb == b))
t = ["| Source access boundary | Operations | Covered | Partially covered | Not covered | Part 3.2 namespace(s) used |", "|---|---|---|---|---|---|"]
for b in bnds:
    nss = Counter(r["blueprint_ns"] for r in src_ops if r["boundary"] == b and r["blueprint_ns"])
    t.append(f'| {b} | {sum(v for (bb, s), v in cb.items() if bb == b)} | {cb.get((b,"Covered"),0)} | {cb.get((b,"Partially covered"),0)} | {cb.get((b,"Not covered"),0)} | {", ".join(f"{k} ({v})" for k, v in nss.most_common()) or "AD-## adapters"} |')
write("counts_boundary.md", "\n".join(t) + "\n")

# contract kind
ck = Counter(ops[r["source_id"][6:]]["contract_kind"] for r in src_ops)
lab = {"explicit_dto": "Proposed explicit DTO (request + result fields, status, SIT assertion)",
       "public_allowlist": "Proposed public response allowlist", "cursor_list": "Proposed cursor/page-size list (result DTO blocked)",
       "review_required": "Review required (descriptive payload; SRC07-DEC-001…038)", "adapter_review": "Adapter contract review (no browser endpoint)"}
t = ["| Source contract maturity | Count | Part 3.2 before this batch | Part 3.5 action |", "|---|---|---|---|"]
act = {"explicit_dto": "Field contract normalized to blueprint conventions (§3.5.5.3)", "public_allowlist": "Public allowlist adopted (§3.5.5.3)",
       "cursor_list": "Query/response envelope defined (§3.5.5.3)", "review_required": "Proposed DTO per SRC07-DEC (§3.5.5.4)",
       "adapter_review": "Adapter command/result envelope (§3.5.5.6)"}
for k in ["explicit_dto", "public_allowlist", "cursor_list", "review_required", "adapter_review"]:
    t.append(f"| {lab[k]} | {ck.get(k,0)} | Purpose, roles, idempotency, side-effect class, PDP and rate-limit class only; no field-level DTO | {act[k]} |")
t.append(f"| **Total** | **{sum(ck.values())}** | | |")
write("counts_kind.md", "\n".join(t) + "\n")

# ---------- 3. Reverse mapping ----------
used = set()
for r in rows:
    for x in r["blueprint_ops"].split(";"):
        used.add(x)
by = OrderedDict()
for b in d["bpops"]:
    by.setdefault(b["domain"], []).append(b)
t = ["| Part 3.2 domain | Ops | Referenced by a source operation | Blueprint-only (DERIVED beyond the source) | Blueprint-only operation IDs |", "|---|---|---|---|---|"]
tot = [0, 0, 0]
for dom, lst in by.items():
    u = [b for b in lst if b["id"] in used]
    nu = [b["id"] for b in lst if b["id"] not in used]
    tot[0] += len(lst); tot[1] += len(u); tot[2] += len(nu)
    t.append(f"| {dom.split('(')[0].strip()} | {len(lst)} | {len(u)} | {len(nu)} | {', '.join(x[4:] for x in nu) or '—'} |")
t.append(f"| **Total** | **{tot[0]}** | **{tot[1]}** | **{tot[2]}** | IDs shown without the `API-` prefix |")
write("reverse.md", "\n".join(t) + "\n")
REV = tot

# ---------- 4. Status-code reconciliation ----------
def final_status(se, method, srcst, path):
    if method == "GET":
        return "200"
    if se in ("Q", "X"):
        return "202"
    if se == "I":
        return "202" if "public" in path else "200"
    if se == "F":
        return "201"
    if se == "W" and method == "POST" and srcst == "201":
        return "201"
    return "200"


t = ["| Source op | Method and source path | Source proposed | Part 3.2 op (SE class) | Normative status (Part 3.5) | Reason |", "|---|---|---|---|---|---|"]
nstat = 0
for r in src_ops:
    if not r["proposed_status"] or r["relation"] not in ("exact", "alias"):
        continue
    f = r["blueprint_ops"].split(";")[0]
    if f not in bp:
        continue
    se = bp[f]["se"]
    fs = final_status(se, r["method"], r["proposed_status"], r["path"])
    if fs != r["proposed_status"]:
        nstat += 1
        reason = {"202": ("Public intake: durable acknowledgement, processing asynchronous; duplicate returns the same reference" if se == "I" else "Asynchronous work or external effect (SE Q/X): 202 + run reference (§3.2.1.10/11)"),
                  "200": "Synchronous state change/decision on an existing resource", "201": "Resource or ledger entry created synchronously"}[fs]
        t.append(f'| {r["source_id"]} | {r["method"]} `{r["path"]}` | {r["proposed_status"]} | {f} ({se}) | **{fs}** | {reason} |')
write("status.md", "\n".join(t) + "\n")
NSTAT = nstat

# ---------- 5. Field contract register ----------
ERRP = {
    "R": "E-R", "W": "E-W", "Q": "E-Q", "X": "E-X", "A": "E-A", "F": "E-F", "I": "E-I", "S": "E-S"}


def extras(o, b):
    p = o["path"] + " " + o["fields"].get("Purpose", "")
    e = []
    if re.search(r"bid", p, re.I):
        e.append("DEADLINE_PASSED")
    if re.search(r"milestone|fulfil", p, re.I):
        e.append("OVER_DELIVERY")
    if re.search(r"payment|reconcile|invoice|receipt|usage-charges", p, re.I):
        e.append("DUPLICATE")
    if re.search(r"publish|pages/\{id\}/control|landing", p, re.I):
        e.append("PUBLICATION_MOVED")
    if re.search(r"documents/\{id\}/complete|uploads", p, re.I):
        e.append("CHECKSUM_MISMATCH, SCAN_PENDING")
    if re.search(r"/control|transition|/close|/approve|/review|decide|/stop|/pause|/resume|/cancel|/complete|/lost|/status", p):
        e.append("INVALID_TRANSITION")
    if re.search(r"budget|ads/|campaign|research/run|ai/run|enrich|discover", p, re.I):
        e.append("BUDGET_EXHAUSTED")
    if re.search(r"merge", p, re.I):
        e.append("DUPLICATE")
    return ", ".join(dict.fromkeys(e))


def hdrs(b):
    h = []
    idem = b["idem"]
    if "Key" in idem:
        h.append("Idempotency-Key")
    if "If-Match" in idem:
        h.append("If-Match")
    if b["ns"].startswith("admin") and b["method"] != "GET":
        h.append("X-Scope-Token, X-CSRF-Token")
    elif b["ns"].startswith("admin"):
        h.append("X-Scope-Token")
    elif b["method"] != "GET" and b["ns"] in ("portal", "public+portal", "admin+portal"):
        h.append("X-CSRF-Token")
    return ", ".join(h) or "—"


TYPEMAP = {"uuid": "uuid", "string": "str", "integer": "int", "array": "array", "object": "object", "date-time": "date-time",
           "boolean": "bool", "email": "email", "date": "date", "uri": "https-url"}


def fmt_fields(fl, drop=True):
    s = []
    for x in fl:
        if drop and x["name"] in ("idempotency_key", "expected_revision"):
            continue
        ty = TYPEMAP.get(x["type"], x["type"])
        if x["name"] in ("amount", "total", "budget", "budget_limit", "price", "unit_price", "credit_amount") and ty == "str":
            ty = "decimal-str"
        if x["name"] == "currency":
            ty = "ISO-4217"
        en = f'∈{{{x["enum"].replace("|", "/")}}}' if x["enum"] else ""
        s.append(f'`{x["name"]}`:{ty}{en}{"" if x["required"] else "?"}')
    return "; ".join(s) or "—"


def moved(fl):
    m = []
    names = [x["name"] for x in fl]
    if "idempotency_key" in names:
        m.append("idempotency_key → Idempotency-Key")
    if "expected_revision" in names:
        m.append("expected_revision → If-Match")
    return "; ".join(m)


groups = OrderedDict()
for r in src_ops:
    o = ops[r["source_id"][6:]]
    if o["contract_kind"] not in ("explicit_dto", "public_allowlist", "cursor_list"):
        continue
    f = r["blueprint_ops"].split(";")[0]
    b = bp.get(f)
    if b is None:  # new op
        e = [x for x in ENH if x[0] == r["enhancement"]][0]
        b = {"id": e[0], "method": e[1], "ns": e[3], "idem": e[8], "se": e[9], "rl": e[11], "domain": "", "pdp": e[10]}
        dc = e[12]
    else:
        dc = dcode(b)
    groups.setdefault(dc, []).append((r, o, b))
FCOUNT = sum(len(v) for v in groups.values())
parts = []
for dc in DOM.values():
    if dc not in groups:
        continue
    parts.append(f"\n**Domain {dc}: {len(groups[dc])} source operations**\n")
    parts.append("| Source op | Part 3.5 target | Request (body or query) | Headers | Response (normative) | Status | Errors (profile + specific) | RL | Source → blueprint translation |")
    parts.append("|---|---|---|---|---|---|---|---|---|")
    for r, o, b in groups[dc]:
        se = b["se"]
        if o["contract_kind"] == "cursor_list":
            req = "query: `limit`:int 1–100 (default 25); `cursor`:str?; `filter[…]` per allowlist (source: " + esc(o["fields"].get("Request contract", ""))[:90] + ")"
            res = "`data[]` + `page.next_cursor` + `meta.as_of`, `meta.total_estimate`"
            trans = "page_size → limit; items → data; next_cursor → page.next_cursor"
        else:
            req = fmt_fields(o["req_fields"])
            rf = o["res_fields"]
            names = [x["name"] for x in rf]
            if "job_id" in names:
                res = "`run_id`:uuid; `status_url`; `state`∈{queued/running/waiting}; `simulated`:bool"
            else:
                res = fmt_fields(rf, drop=False) + (" + `ETag`" if "revision" in names else "")
            trans = "; ".join(x for x in [moved(o["req_fields"]), "job_id → run_id; held/pending → waiting/queued; simulated → flag" if "job_id" in names else ""] if x) or "Fields adopted as named"
        st = final_status(se, b["method"], o["proposed_status"], r["path"]) if b["method"] != "GET" else "200"
        if b["ns"] == "hooks":
            st = "200"
        if r["relation"] in ("split", "approval"):
            tl = [x for x in r["blueprint_ops"].split(";") if x in bp]
            st = ", ".join(f'{x[4:]}:{final_status(bp[x]["se"], bp[x]["method"], o["proposed_status"], r["path"])}' for x in tl)
        err = ERRP.get(se, "E-W") + ((" + " + extras(o, b)) if extras(o, b) else "")
        tgt = b["id"] if r["relation"] not in ("partial", "none") else (r["enhancement"] + (" (+" + r["blueprint_ops"].replace(";", ", ") + ")" if r["blueprint_ops"] else ""))
        if r["relation"] in ("split", "approval"):
            tgt = r["blueprint_ops"].replace(";", ", ")
        parts.append(f'| {r["source_id"]} {o["method"]} `{esc(o["path"])}` | {tgt} | {req} | {hdrs(b)} | {res} | {st} | {err} | {b["rl"]} | {trans} |')
write("fields.md", "\n".join(parts) + "\n")

# ---------- 6. SRC07-DEC register ----------
t = ["| SRC07-DEC | Source op | Part 3.2 target | Source requirement | Proposed resolution (source) | Part 3.5 normative contract | Owner / status |", "|---|---|---|---|---|---|---|"]
opmap = {f'{r["method"]} {r["path"]}': r for r in src_ops}


def dec_contract(dc, r):
    res = dc["resolution"]
    if res.startswith("Reuse existing identity"):
        return "BFF/OIDC contract of DEC-019 (API-003…012); legacy path is a logical alias; response = session status DTO of API-005/API-010; no password or token handled by this product"
    if res.startswith("Normalize only after verifying"):
        return "Raw-body signature check (§3.2.6.1) → ProviderEvent UNIQUE (connection, provider_event_id) → 200 `{\"received\": true}` within NFR-051; duplicate 200 no effect; invalid 401 WEBHOOK_SIGNATURE_INVALID; stale 401 WEBHOOK_REPLAY_REJECTED; GET challenge echoes hub.challenge only when verify token matches"
    m = re.search(r"HTTP 200: (.*?)\. Proposed allowlist", res)
    body = m.group(1) if m else ""
    q = re.search(r"query: (.*?); HTTP", res)
    qq = q.group(1) if q else ""
    body = body.replace(";", "; ").replace("items", "items[]").replace("next_cursor:s?", "page.next_cursor")
    qq = qq.replace("page_size:p?", "limit:int 1–100").replace("cursor:s?", "cursor:str?")
    return f"query: {qq}; 200: {body} (notation §3.5.5.1)"


for dc in d["decs"]:
    r = opmap.get(dc["op"])
    tgt = r["blueprint_ops"].replace(";", ", ") if r else "?"
    sid = r["source_id"] if r else "?"
    t.append(f'| {dc["id"]} | {sid} `{dc["op"]}` | {tgt} | {esc(dc["source_req"])[:120]} | {esc(dc["resolution"])[:160]} | {esc(dec_contract(dc, r))} | {esc(dc["owner"].replace("Status: ", ""))} |')
write("decs.md", "\n".join(t) + "\n")

# ---------- 7. Candidates contract ----------
t = ["| Candidate | Part 3.5 target | Candidate request (JSON Schema summary) | Candidate response | Success | Entities (source) | Normative delta |", "|---|---|---|---|---|---|---|"]


def schema_summary(s):
    if not s or s == "null":
        return "none (GET)"
    try:
        j = json.loads(s)
    except Exception:
        return esc(s[:120])
    req = set(j.get("required", []))
    out = []
    for k, v in j.get("properties", {}).items():
        ty = v.get("type", "")
        if "enum" in v:
            ty += "∈{" + "/".join(v["enum"]) + "}"
        if v.get("format"):
            ty += "(" + v["format"] + ")"
        if v.get("pattern"):
            ty += " /" + v["pattern"] + "/"
        out.append(f"`{k}`:{ty}{'' if k in req else '?'}")
    return "; ".join(out) + ("; additionalProperties:false" if j.get("additionalProperties") is False else "")


for c in d["cands"]:
    r = [x for x in rows if x["source_id"] == c["id"]][0]
    tgt = (r["enhancement"] + " + " if r["enhancement"] else "") + r["blueprint_ops"].replace(";", ", ")
    delta = "Envelope `data`/`page` replaces `items`/`next_cursor`" if "next_cursor" in c["res_schema"] else (
        "expected_revision → If-Match; add Idempotency-Key" if "expected_revision" in c["req_schema"] else "Add Idempotency-Key header" if c["method"] != "GET" else "Adopted")
    t.append(f'| {c["id"]} | {tgt} | {schema_summary(c["req_schema"])} | {schema_summary(c["res_schema"])} | {c["success"]} | {c["entities"]} | {delta} |')
write("cands.md", "\n".join(t) + "\n")

# ---------- 8. Provider register ----------
CLS = {}
for n in ["django auth", "django", "drf", "pgvector", "celery", "celery beat", "redis", "deepeval", "pydantic ai", "react", "react forms", "postgresql", "playwright", "pytest"]:
    CLS[n] = "OSS library"
for n in ["document skills dev", "document skills", "mcp server dev", "agent sdk dev", "claude code setup", "claude.md management", "security guidance", "plugin developer toolkit", "customer-sales-automation", "sales", "content studio", "content-marketing", "marketing", "seo-content-creation", "skill creator", "social-publishing", "seo-analysis-monitoring", "seo-technical-optimization"]:
    CLS[n] = "Developer plugin"
for n in ["clay", "leadfeeder", "common room", "endgame", "socialinsider", "writesonic", "adspirer", "crossbeam skills"]:
    CLS[n] = "Unapproved SaaS"
BPMAP = {
    "django auth": ("Part 3.1 identity reuse; DEC-019", "Covered"), "django": ("Part 3.1 stack", "Covered"), "drf": ("Part 3.1 stack", "Covered"),
    "pgvector": ("Part 3.3 vector store", "Covered"), "celery": ("Part 3.1 workers", "Covered"), "celery beat": ("Part 3.1 scheduler", "Covered"),
    "redis": ("Valkey (Part 3.1; ADR-035)", "Covered"), "deepeval": ("Part 6.4 / Part 7 eval harness", "Covered"), "pydantic ai": ("Part 7.3 (gateway library option)", "Covered"),
    "react": ("Part 3.1 SPAs", "Covered"), "react forms": ("Part 2.5 forms", "Covered"), "postgresql": ("Part 3.3", "Covered"), "playwright": ("Part 6.1 E2E", "Covered"), "pytest": ("Part 6.1", "Covered"),
    "claude api": ("AD-13 (B02)", "Covered"), "claude/openai api": ("AD-13; OpenAI not approved (DEC-007 tiers)", "Conflict"), "llm gateway": ("AD-13 via model gateway", "Covered"), "llm": ("AD-13", "Covered"), "rag": ("AD-13 + AD-14", "Covered"),
    "pubmed": ("Not in Part 3.2", "Not covered"), "s3": ("Part 3.1 storage; AD-D01 (new)", "Partially covered"), "aws secrets manager": ("AD-12", "Covered"), "aws": ("Part 3.1 / 4.3", "Covered"),
    "aws core": ("Part 4.3", "Covered"), "aws serverless": ("Part 4.3 (not used for API)", "Covered"), "cloudwatch": ("AD-16", "Covered"), "github": ("Part 4.3 CI", "Covered"), "sentry": ("AD-15", "Covered"),
    "postman": ("Dev tool; CT suites replace", "Not applicable"), "figma": ("Design tool (Part 2.5)", "Not applicable"), "tavily": ("AD-05 (B03)", "Covered"), "exa": ("AD-06 (B03, off)", "Covered"),
    "firecrawl": ("AD-07 (B04)", "Covered"), "hunter": ("AD-19 / AD-D02 (B10/B18)", "Covered"), "apollo.io": ("AD-19 (B08)", "Covered"), "resend": ("AD-01 alternative (DEC-025)", "Covered"),
    "ses": ("AD-01 (B05)", "Covered"), "calendar api": ("AD-03/AD-04 (B15)", "Conflict"), "meta cloud api": ("AD-02 (B06)", "Covered"), "meta whatsapp business api": ("AD-02", "Covered"), "whatsapp": ("AD-02", "Covered"),
    "canva": ("Design tool; not runtime", "Not applicable"), "postiz": ("AD-08 option (AGPL)", "Conflict"), "search console": ("AD-17 (B17)", "Covered"), "posthog": ("First-party analytics API-291", "Not applicable"),
    "zoom": ("AD-18 (B10)", "Conflict"), "pandadoc": ("AD-10 shortlist differs (DEC-023)", "Conflict"), "langfuse": ("B22 LLM observability (reserved)", "Partially covered"),
}
t = ["| Provider / tool (source spelling) | Source ops | Class | Licence (source) | Free quota (source; verify) | Paid rate (source; verify) | Source allocation | Blueprint location | Status |", "|---|---|---|---|---|---|---|---|---|"]
pc = Counter()
for n, v in prov.items():
    cls = CLS.get(n, "Runtime provider")
    loc, st = BPMAP.get(n, ("Not a runtime entitlement (source: plugins are not runtime entitlements)" if cls == "Developer plugin" else "Excluded: ₹0 committed, procurement not approved" if cls == "Unapproved SaaS" else "?", "Not applicable"))
    pc[(cls, st)] += 1
    first = lambda k: esc((v.get(k) or [""])[0])[:110]
    t.append(f'| {n} | {len(v.get("ops", []))} | {cls} | {first("Licence")} | {first("Free quota")} | {first("Paid rate")} | {first("Allocation")} | {loc} | {st} |')
write("providers.md", "\n".join(t) + "\n")
PCOUNT = pc

# ---------- 9. Tests ----------
FAM = {"R": "N01, N02, N03, N05", "W": "N01, N02, N03, N04, N06, N07", "Q": "N01, N02, N04, N06, N07, N09",
       "X": "N01, N02, N04, N06, N07, N09, N10, N11, N12", "A": "N01, N02, N04, N06, N07, N08", "F": "N01, N02, N04, N06, N07, N08",
       "I": "N02, N04, N05, N13", "S": "N01, N02"}
t = ["| Test ID | Source SIT | Source op | Part 3.5 target | Positive oracle (from source SIT assertion, adapted) | Negative families (§3.5.5.12.1) | Type | Priority |", "|---|---|---|---|---|---|---|---|"]
for r in src_ops:
    o = ops[r["source_id"][6:]]
    f = r["blueprint_ops"].split(";")[0]
    b = bp.get(f)
    if r["method"] == "ADAPTER":
        se, fam, ty = "X", "N09, N10, N11, N14, N15", "Adapter contract (CT-08/09)"
    elif b is not None and b["ns"] == "hooks":
        se, fam, ty = "I", "N13, N16, N17, N05", "Webhook contract (CT-10)"
    else:
        se = b["se"] if b else [x for x in ENH if x[0] == r["enhancement"]][0][9]
        fam, ty = FAM.get(se, "N01, N02"), "API SIT (CT-04/05)"
    tgt = r["blueprint_ops"].replace(";", ", ") if r["relation"] not in ("partial", "none") else r["enhancement"] + (", " + r["blueprint_ops"].replace(";", ", ") if r["blueprint_ops"] else "")
    pri = "P0" if se in ("X", "A", "F", "I") or "portal" in r["path"] or "public" in r["path"] else "P1"
    pos = esc(o["sit_assertion"]).rstrip(".")
    sr = esc(o["sit_result"]).rstrip(".")
    pos = pos + (f"; expect {sr}" if sr else "")
    t.append(f'| TC-ENH-D-{o["num"]} | {r["sit_id"]} | {r["source_id"]} | {tgt} | {pos[:220]} | {fam} | {ty} | {pri} |')
for c in d["cands"]:
    r = [x for x in rows if x["source_id"] == c["id"]][0]
    tgt = (r["enhancement"] + ", " if r["enhancement"] else "") + r["blueprint_ops"].replace(";", ", ")
    t.append(f'| TC-ENH-D-C{c["id"][-2:]} | — (expansion test) | {c["id"]} | {tgt} | {esc(c["control"])}; expect {c["success"]} with candidate response schema | {"N01, N02, N03, N05" if c["method"]=="GET" else "N01, N02, N04, N06, N07"} | API SIT (CT-04/05) | P0 |')
for e in ENH:
    fam = FAM.get(e[9], "N01, N02")
    t.append(f'| TC-ENH-D-E{e[0][-3:]} | — | {e[5]} | {e[0]} | {esc(e[4])}: authorized role succeeds with documented status; audit event written | {fam} | API SIT (CT-04/05) | {"P0" if e[9] in ("X","F","A") else "P1"} |')
write("tests.md", "\n".join(t) + "\n")

# ---------- 10. Enhancement ops table ----------
t = ["| Op ID | Method | Path | NS | Purpose | Source | FR / screen | Auth / roles | Idempotent | SE | PDP | RL class |", "|---|---|---|---|---|---|---|---|---|---|---|---|"]
for e in ENH:
    t.append(f"| {e[0]} | {e[1]} | `{e[2]}` | {e[3]} | {esc(e[4])} | {e[5]} | {e[6]} | {e[7]} | {e[8]} | {e[9]} | {e[10]} | {e[11]} |")
write("enh_ops.md", "\n".join(t) + "\n")

# ---------- 11. Namespace differences ----------
t = ["| Source op | Method and path | Source boundary | Part 3.2 op and namespace | Assessment | Resolution |", "|---|---|---|---|---|---|"]
RES = {
    "SM-OP-017": ("Conflict (CONFLICT-367)", "Classify API-083 as `portal` (signed token route) per Part 3.2 rule (3); serve on api-web; RL-PUB-W"),
    "SM-OP-018": ("Compatible split", "Admin/internal consent capture stays API-066; portal consent changes use API-082 (own preferences) with a portal serializer"),
    "SM-OP-019": ("Compatible", "Part 3.2 already treats opt-out as a token-bound portal route on the website ingress; no change"),
    "SM-OP-041": ("Partial (CONFLICT-366)", "Keep API-069 for subjects; add API-ENH-D-024 for staff recording an offline request"),
    "SM-OP-097": ("Compatible superset", "Internal mount is for PDP pre-checks by workers; Admin behaviour identical"),
    "SM-OP-123": ("Compatible split (CONFLICT-366)", "Admin booking API-243; portal/public booking through API-273/274 (hold then confirm)"),
    "SM-OP-207": ("Conflict (CONFLICT-366)", "Payment-link creation stays Admin (R08) because it starts an external effect; portal users read the issued link through API-410"),
    "SM-OP-211": ("Compatible split", "Admin completion API-413; customer completes own steps via API-438"),
    "SM-OP-221": ("Compatible superset", "No change"),
    "SM-OP-286": ("Partial", "Portal acceptance (sell direction) API-383/384; Admin acceptance for buy direction API-ENH-D-016"),
}
for r in src_ops:
    if r["ns_conflict"]:
        a, res = RES.get(r["source_id"], ("Review", ""))
        t.append(f'| {r["source_id"]} | {r["method"]} `{r["path"]}` | {r["boundary"]} | {r["blueprint_ops"].replace(";", ", ")} ({r["blueprint_ns"]}) | {a} | {res} |')
write("ns.md", "\n".join(t) + "\n")

# ---------- 12. Coverage CSV ----------
cov = []
# per operation endpoint + field contract + test
for r in src_ops:
    o = ops[r["source_id"][6:]]
    sec = "Commercial REST and external adapter register" if int(o["num"]) <= 288 else "Website publishing and external-portal additions"
    loc = "Part 3.2 §3.2.2.4 " + r["blueprint_ops"].replace(";", ", ") if r["blueprint_ops"] else "—"
    if r["method"] == "ADAPTER":
        loc = "Part 3.2 §3.2.4.2–3 " + r["blueprint_ops"].replace(";", ", ")
    act = {"Covered": "Mapped (" + REL[r["relation"]] + ")", "Partially covered": "Missing semantics added", "Not covered": "New operation added"}[r["status"]]
    cov.append(["07", sec, r["source_id"], f'{r["method"]} {r["path"]}: {r["purpose"]}', r["status"], loc, act + ("; " + r["note"] if r["note"] else ""), r["enhancement"]])
    if r["method"] != "ADAPTER":
        kind = o["contract_kind"]
        cov.append(["07", sec, r["source_id"] + "-DTO", f'Field contract ({kind}) for {r["method"]} {r["path"]}', "Not covered",
                    "Part 3.2 has no per-operation DTO", "Normalized field contract written", "Part 3.5 §3.5.5.3" if kind != "review_required" else "Part 3.5 §3.5.5.4"])
    else:
        cov.append(["07", sec, r["source_id"] + "-CTX", f'Adapter command/result context for {r["path"]}', "Partially covered",
                    "Part 3.2 §3.2.4.1 IP-01 AdapterResult", "AdapterCommand/AdapterResult envelope completed", "Part 3.5 §3.5.5.6"])
    cov.append(["07", "Implementation, verification and delivery controls (SIT table)", r["sit_id"], f'Operation SIT for {r["method"]} {r["path"]}', "Partially covered",
                "Part 3.2 §3.2.5 CT-04/05/08/10 (generic); Part 6 has no per-operation TC", "Per-operation test added", "TC-ENH-D-" + o["num"]])
for r in rows:
    if r["source_id"].startswith("SM-UX"):
        cov.append(["07", "Current multi-startup scope: API design", r["source_id"], f'{r["method"]} {r["path"]}: {r["purpose"]}', r["status"],
                    "Part 3.2 §3.2.2.4 " + r["blueprint_ops"].replace(";", ", "), "Mapped; candidate schema normalized" + ("; " + r["note"] if r["note"] else ""), (r["enhancement"] + "; " if r["enhancement"] else "") + "TC-ENH-D-C" + r["source_id"][-2:]])
for dc in d["decs"]:
    r = opmap.get(dc["op"])
    cov.append(["07", "Implementation acceptance and final decision controls", dc["id"], f'Contract decision for {dc["op"]}', "Not covered",
                "Part 3.2 (ID collides with blueprint DEC-###)", "Renamed SRC07-DEC; normative contract proposed", "Part 3.5 §3.5.5.4; CONFLICT-364"])
for n, v in prov.items():
    cls = CLS.get(n, "Runtime provider")
    loc, st = BPMAP.get(n, ("Not a runtime entitlement" if cls == "Developer plugin" else "Excluded: procurement not approved", "Not applicable"))
    st2 = {"Conflict": "Conflict"}.get(st, st)
    cov.append(["07", "Per-operation Integration/Licence/Quota/Rate/Allocation columns", "PROV-" + re.sub(r"[^a-z0-9]+", "-", n).strip("-"), f"Provider/tool '{n}' ({cls}) on {len(v.get('ops', []))} ops", st2, loc,
                "Classified in provider register" + ("; conflict resolved" if st == "Conflict" else ""), "Part 3.5 §3.5.5.6.4" + ("; CONFLICT-368/371" if st == "Conflict" else "")])
for oid, title, a, b2, own in d["opts"]:
    cov.append(["07", "Optimization engineering and acceptance", oid, f"{title}: {a[:80]}", "Covered" if not oid.startswith("OPT-09") else "Partially covered",
                "Part 4.2 NFRs (see §3.5.5.10)", "Mapped" if not oid.startswith("OPT-09") else "API-level control and evidence added", "Part 3.5 §3.5.5.10"])
json.dump({"cov": cov}, open(os.path.join(FR, "cov_ops.json"), "w"))
print("fragments written; field rows", FCOUNT, "status diffs", NSTAT, "reverse", REV, "providers", dict(PCOUNT))
print("cov rows (ops part)", len(cov))
