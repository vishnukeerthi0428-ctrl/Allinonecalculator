#!/usr/bin/env python3
"""Group F: parse every integration candidate in source document 16 (538 records),
the named-decision table and supporting inventory in document 21, and the budget
register in document 16. Writes final/coverage/F_integration_candidates.csv and a
JSON summary used to write Part 7.4.

Usage: python3 -I F_parse_doc16_21.py <docs38_dir> <blueprint_dir>
"""
import csv, json, re, sys, collections, os

DOCS = sys.argv[1]
BP = sys.argv[2]
d16 = open(os.path.join(DOCS, "16_Plugin_API_Open_Source_and_Cost_Management.txt"), encoding="utf-8").read().splitlines()
d21 = open(os.path.join(DOCS, "21_Paid_Plugin_Replacement_and_Open_Source_Automation_Strategy.txt"), encoding="utf-8").read().splitlines()

FIELDS = ["Category", "Source priority", "Decision / cost treatment", "Application", "Commercial modules",
          "Interface", "Trigger", "Acceptance", "Procurement", "Licence", "Free tier", "Paid API",
          "Allocation", "Official / evidence URL", "Verification status"]

# ---------- document 16 candidate register ----------
cands = []
cur = None
in_reg = False
for line in d16:
    if line.startswith("<Heading1> Individual candidate register"):
        in_reg = True; continue
    if in_reg and line.startswith("<Heading1>"):
        break
    if not in_reg:
        continue
    m = re.match(r"<Heading2> (\d{3})\. (.+)$", line)
    if m:
        cur = {"no": m.group(1), "name": m.group(2).strip()}
        cands.append(cur); continue
    if cur is None:
        continue
    for f in FIELDS:
        if line.startswith(f + ":"):
            v = line[len(f) + 1:].strip()
            # strip the "Name:" prefix used in licence/fee fields
            pref = cur["name"] + ":"
            if v.startswith(pref):
                v = v[len(pref):].strip()
            cur[f] = v
            break
assert len(cands) == 538, len(cands)
for c in cands:
    for f in FIELDS:
        assert f in c, (c["no"], f)

# ---------- document 21 named decisions ----------
named = {}
i = 0
in7 = False
rows = []
while i < len(d21):
    l = d21[i]
    if l.startswith("<Heading1> 7. Named integration decisions"):
        in7 = True
    elif in7 and l.startswith("<Heading1>"):
        break
    if in7 and l == "---row":
        if i + 3 < len(d21) and d21[i + 1] not in ("[/TABLE]",):
            rows.append((d21[i + 1], d21[i + 2], d21[i + 3]))
    i += 1
for n, dec, rat in rows:
    if n == "[/TABLE]":
        continue
    cap = rat.split(" — ")[0]
    named[n] = {"decision21": dec, "capability21": cap, "rationale21": rat}

# supporting inventory (section 8)
support = {}
sec = None
for j, l in enumerate(d21):
    m = re.match(r"<Heading2> (.+) — (\d+) candidates", l)
    if m:
        sec = (m.group(1), int(m.group(2)), d21[j + 1], d21[j + 2]); continue
    if sec and l and not l.startswith("<") and l.endswith(".") and "," in l and j > 0 and d21[j - 1].startswith("Decision:"):
        names = [x.strip().rstrip(".") for x in l.split(", ")]
        assert len(names) == sec[1], (sec[0], len(names), sec[1])
        cap = re.search(r"where justified: (.+?)\.", sec[2])
        for nm in names:
            support[nm] = {"inv_category": sec[0], "decision21": "Defer; no runtime need established",
                           "capability21": cap.group(1) if cap else ""}
        sec = None

# doc 21 benchmark category counts
bench = {}
k = [i for i, l in enumerate(d21) if l == "Benchmark state"]
if k:
    j = k[0] + 1
    while j < len(d21) and d21[j] != "[/TABLE]":
        if d21[j] == "---row" and d21[j + 1] != "[/TABLE]":
            bench[d21[j + 1]] = int(d21[j + 2])
        j += 1

# ---------- classification helpers ----------
BUDGET_RE = re.compile(r"\bB(\d{2})\b")
def budgets(c):
    s = " ".join(c[f] for f in ("Decision / cost treatment", "Allocation"))
    return sorted(set("B" + b for b in BUDGET_RE.findall(s)))

def licence_class(l):
    t = l.lower()
    if t.startswith("unverified"): return "Unverified (not established)"
    if t.startswith("claude skill"): return "Developer plugin (licence unverified)"
    if "agpl" in t: return "Hybrid AGPL self-host / proprietary cloud"
    if t.startswith("open source"): return "Open source (permissive)"
    if "hybrid" in t or "commercial service" in t: return "Commercial / hybrid (edition unverified)"
    if t.startswith("proprietary"): return "Proprietary service"
    return "Other"

def fee_class(c):
    t = c["Paid API"].lower(); f = c["Free tier"].lower()
    if t.startswith("not verified"): return "Not verified (no assumed price)"
    if "₹0 software" in t or "₹0 self-host" in t: return "₹0 licence; hosting extra"
    if "claude" in f or "installation fee" in t: return "Developer seat usage (B09/B02)"
    if "$" in t: return "Published rate (verify)"
    return "Plan/quote required"

# Map doc-21 capability -> blueprint adapter / module and blueprint replacement decision
CAP_MAP = {
 "Workflow orchestration and RPA": ("M55 workflow engine; ADR-071 (Celery+PostgreSQL)", "AU-025…AU-030; AG-016", "Replace (native)"),
 "Public market / investor search": ("AD-05 Tavily / AD-06 Exa (SearchPort)", "AG-003; AU-007, AU-014", "Replace core; investor use excluded (DEC-002 scope)"),
 "Website extraction": ("AD-07 Firecrawl self-hosted (ExtractionPort)", "AG-004; AU-014", "Retain OSS / self-host"),
 "Professional contact discovery": ("AD-19 Apollo/Hunter (EnrichmentPort, OFF)", "AG-008; AU-018", "Conditional external service (B08/B18)"),
 "CRM / relationship pipeline": ("M21–M23 native CRM", "AU-020, AU-021", "Replace (native)"),
 "LLM / agent framework": ("AD-13 Anthropic via ai.gateway (ADR-070)", "AU-001…AU-006", "Replace (native gateway)"),
 "Embeddings, knowledge and enterprise search": ("AD-14 EmbeddingPort; pgvector (ADR-077)", "AG-001; TL-01", "Retain OSS"),
 "Email automation and inbox": ("AD-01 Amazon SES (DEC-025)", "AU-022, AU-024; AG-011", "Conditional external service (B05)"),
 "WhatsApp, SMS and social messaging": ("AD-02 WhatsApp Cloud API", "AG-013, AG-014", "Conditional external service (B06)"),
 "Meeting scheduling and video": ("AD-03/AD-04 Calendar; AD-18 Webinar", "AU-023", "Conditional external service (B15)"),
 "Document generation / secure storage": ("AU-036 document assembly; S3", "AU-036", "Replace (native)"),
 "Electronic signing and identity verification": ("AD-10 ESignPort (manual first, DEC-023)", "AG-022", "Conditional external service (B13)"),
 "Banking, receipts and billing": ("AD-11 PaymentPort (manual first, DEC-022)", "AG-024; AU-037", "Conditional external service (B14)"),
 "Observability, error tracking, metrics and security": ("AD-15 Sentry, AD-16 CloudWatch; ADR-078", "AG-028; AU-010, AU-012", "Retain OSS / existing"),
 "Cloud infrastructure and storage": ("AWS ap-south-1 (DEC-040)", "AU-013", "Retain existing (B01)"),
 "Developer tools, QA and project coordination": ("Delivery tooling (Part 7.3 §7.5.2)", "AG-033…AG-036", "Defer (developer-only)"),
 "Analytics, reporting and forecasting": ("RP-01…30; AU-040, AU-041", "AG-029", "Replace (native)"),
 "Customer support / collaboration": ("M63 support; NT notifications", "AG-031", "Replace (native)"),
 "Marketing content and localization": ("M34 content studio", "AG-018, AG-012", "Replace (native)"),
 "SEO and AI search visibility": ("AD-17 Search Console", "AU-033", "Replace (native) + official API"),
 "Social listening and publishing": ("AD-08 SocialPort", "AG-018; AU-029", "Conditional external service (B16)"),
 "Marketing campaigns and attribution": ("M39 campaigns; AU-040", "AU-040", "Replace (native)"),
 "Advertising and paid acquisition": ("AD-09 AdsPort", "AU-032", "Conditional external service (B12/B16)"),
 "Website and landing page builder": ("B-WEB publication service (A107, A108)", "AU-029", "Replace (native)"),
 "Project / tender discovery and bid preparation": ("WF-08 bids; AU-034 (DEC-053)", "AG-019, AG-020", "Replace (native); no auto-submission"),
 "Supplier, order, procurement and retention": ("WF-10 orders; AU-035, AU-038", "AG-023", "Replace (native)"),
 "Webinar and demo registration": ("AD-18 EventsPort", "AU-023", "Conditional external service (B10)"),
 "No runtime requirement established": ("—", "—", "Exclude / defer"),
}

def norm(s):
    return re.sub(r"[^a-z0-9]", "", s.lower())
named_n = {norm(k): v for k, v in named.items()}
support_n = {norm(k): v for k, v in support.items()}

out = []
cat_ct = collections.Counter(); pri_ct = collections.Counter(); lic_ct = collections.Counter()
dec_ct = collections.Counter(); bp_ct = collections.Counter(); bud_ct = collections.Counter()
fee_ct = collections.Counter(); trig_ct = collections.Counter(); ver_ct = collections.Counter()
matched_named = 0; matched_support = 0; unmatched = []
for c in cands:
    n = norm(c["name"])
    if n in named_n:
        d = named_n[n]; src21 = "§7 named"; matched_named += 1
    elif n in support_n:
        d = support_n[n]; src21 = "§8 supporting"; matched_support += 1
    else:
        d = {"decision21": "Not listed in doc 21 (default: Defer)", "capability21": ""}
        src21 = "not listed"; unmatched.append(c["name"])
    cap = d.get("capability21", "")
    adapter, agau, bpdec = CAP_MAP.get(cap, ("—", "—", "Exclude / defer"))
    # blueprint status
    dec21 = d["decision21"]
    if cap in ("", "No runtime requirement established"):
        status = "Not applicable (no runtime need; deferred)"
    elif dec21.startswith("Defer"):
        status = "Covered (deferred by default; capability covered natively)"
    elif "Replace" in dec21 or "Self-host" in dec21:
        status = "Covered (native capability exists)" if adapter != "—" else "Partially covered"
    else:
        status = "Partially covered"
    # specific blueprint adapters that are named explicitly
    explicit = {"firecrawl": "AD-07", "apolloio": "AD-19", "hunter": "AD-19", "tavily": "AD-05", "exa": "AD-06",
                "resend": "AD-01 alt (DEC-025)", "zoom": "AD-18", "sentry": "AD-15", "langfuse": "ADR-078 / B22",
                "deepeval": "ADR-079", "pydanticai": "Part 7.3 §7.5.3", "playwright": "Part 6 tooling",
                "github": "Part 4.3 CI", "postman": "Part 3.2 §3.2.5"}
    exp = explicit.get(n, "")
    if exp:
        status = "Covered (named in blueprint)"
    b = budgets(c)
    lc = licence_class(c["Licence"]); fc = fee_class(c)
    trig = "Development environment" if c["Trigger"].lower().startswith("development") else c["Trigger"][:40]
    row = {
        "no": c["no"], "candidate": c["name"], "category": c["Category"], "priority": c["Source priority"],
        "licence": c["Licence"], "licence_class": lc, "free_tier": c["Free tier"], "paid_rate": c["Paid API"],
        "fee_class": fc, "allocation": c["Allocation"], "budget_ids": ";".join(b),
        "decision_doc16": c["Decision / cost treatment"], "application": c["Application"],
        "commercial_modules": c["Commercial modules"], "interface": c["Interface"], "trigger": c["Trigger"],
        "verification_status": c["Verification status"], "evidence_url": c["Official / evidence URL"],
        "doc21_listing": src21, "decision_doc21": dec21, "capability_doc21": cap,
        "blueprint_adapter_or_module": exp or adapter, "blueprint_ag_au": agau, "blueprint_replacement_decision": bpdec,
        "blueprint_status": status, "activation_default": "Disabled; procurement gate PG-01…PG-10 (Part 7.4 §7.4.5.6)",
    }
    out.append(row)
    cat_ct[c["Category"]] += 1; pri_ct[c["Source priority"]] += 1; lic_ct[lc] += 1
    dec_ct[dec21] += 1; bp_ct[status] += 1; fee_ct[fc] += 1; trig_ct[trig] += 1
    for x in b: bud_ct[x] += 1
    ver_ct["checked 2026-11-24" if "2026-11-24" in c["Verification status"] else "other"] += 1

os.makedirs(os.path.join(BP, "final", "coverage"), exist_ok=True)
with open(os.path.join(BP, "final", "coverage", "F_integration_candidates.csv"), "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(out[0].keys()))
    w.writeheader(); w.writerows(out)

# ---------- budget register (doc 16) ----------
bud = []
s = d16.index("<Heading1> Source operating budget register")
j = s
while d16[j] != "[/TABLE]":
    if d16[j] == "---row":
        bud.append((d16[j + 1], d16[j + 2], d16[j + 3]))
    j += 1

summary = {
    "candidates": len(cands), "named_doc21": len(named), "support_doc21": len(support),
    "matched_named": matched_named, "matched_support": matched_support, "unmatched": unmatched,
    "category": cat_ct.most_common(), "priority": pri_ct.most_common(), "licence_class": lic_ct.most_common(),
    "fee_class": fee_ct.most_common(), "decision_doc21": dec_ct.most_common(), "blueprint_status": bp_ct.most_common(),
    "budget_refs": bud_ct.most_common(), "trigger": trig_ct.most_common(), "verification": ver_ct.most_common(),
    "bench_categories": bench, "bench_total": sum(bench.values()), "budget_register": bud,
    "p0p1": [(r["no"], r["candidate"], r["priority"], r["licence"], r["free_tier"], r["paid_rate"], r["allocation"], r["budget_ids"], r["decision_doc21"], r["blueprint_adapter_or_module"]) for r in out if r["priority"] in ("P0", "P1")],
    "named_rows": [(r["no"], r["candidate"], r["priority"], r["decision_doc21"], r["capability_doc21"], r["licence"], r["free_tier"], r["paid_rate"], r["allocation"], r["budget_ids"], r["blueprint_adapter_or_module"], r["blueprint_status"]) for r in out if r["doc21_listing"] == "§7 named"],
}
json.dump(summary, open(sys.argv[3] if len(sys.argv) > 3 else "/dev/stdout", "w"), indent=1, ensure_ascii=False)
