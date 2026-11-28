#!/usr/bin/env python3
"""Group R4 / letter E: atomic aspect register for FSD V12 platform chapters
00-10, 32, 35 (architecture parts), 36, 38, 39.

Writes final/coverage_v12/E_coverage.csv and a Markdown register fragment.
Catalogue rows (foundations, engines, tax rules, configuration variables,
CI/CD stages, SLOs, GO steps, maintenance cadences, R0-R5) are generated from
the parsed tables (E_parse_tables.py output) so that no row is skipped.
Usage: python3 -I E_coverage.py <E_tables.json> <out.csv> <out_register.md>
"""
import csv, json, sys
from collections import Counter, OrderedDict

C, P, N, X, NA = "Covered", "Partially covered", "Not covered", "Conflict", "Not applicable"
M, F = "Matched", "Pending Founder decision"
DOC = "FSD V12"
A = []  # (chapter, section, summary, before, location, action, new_ids, after)


def add(ch, sec, summ, before, loc, action, ids="", after=M):
    if before == NA and after == M:
        after = NA + " (" + action + ")"
    A.append((ch, sec, summ, before, loc, action, ids, after))


T = json.load(open(sys.argv[1], encoding="utf-8"))
def tab(prefix, i):
    for f, r in T.items():
        if f.startswith(prefix):
            return r["tables"][i]
    raise KeyError(prefix)

OWN = {"B": "group R2 (Part 11.2)", "C": "group R3a (Part 11.3)", "D": "group R3b (Part 11.4)",
       "F": "group R5 (Part 11.6)", "G": "group R6 (Part 11.7)", "H": "group R7 (Part 11.8)",
       "I": "group R8 (Part 11.9)", "J": "group R9 (Part 11.10)", "K": "group R10 (Part 11.11)",
       "L": "group R11 (Part 11.12)", "A": "group R1 (Part 11.1)"}
def own(g):
    return "allocated to " + OWN[g]

# ---------------- Chapter 00 ----------------
add("00", "Reading guide", "Reading order and precedence: V10 baseline first, then active chapters, compatible earlier sections, Appendices A-D; historical annex non-normative", P,
    "Part 9.10 DEC-415 precedence", "Precedence extended: V12 active chapters > earlier V-sections > blueprint text for platform scope (§11.5.7 DEC-580)", "DEC-580")
add("00", "Chapter list", "40-chapter FSD structure (01-40) and chapter-to-group mapping", NA, "V12_BRIEF allocation", "document navigation; chapters 01-10, 32, 35, 36, 38, 39 reviewed here, others " + "allocated to their groups")
add("00", "Front matter", "V12.0 28 Nov 2026, 2031 horizon; 39 services / 156 workflows / 25 foundations / 15 engines", P,
    "Part 1 BR register; no SKU/foundation/engine registers", "Foundations and engines registered (§11.5.5.4); SKU/workflow content " + own("B"), "FR-V12-E-048, FR-V12-E-049")
add("00", "Front matter", "Status: 233 controlled + 65 ENT requirements, 30 REC, 35 release KPIs, 13 ethics rules, 23+10 jurisdiction rules; specification and prototype only", P,
    "Part 0 inventory", "ENT-IDN/ACC/BIZ (17 of 65) and REC-04/20-27 handled here; remaining counts " + own("A"), "DEC-580")

# ---------------- Chapter 01 ----------------
add("01", "V12 baseline", "Enterprise-readiness baseline adds identity federation, governed access, developer platform, data control, integrations, security programme, legal/multi-market, localisation, operations, commercial operations", P,
    "Parts 4.1, 9.9 (partial)", "Platform-architecture ingredients specified in §11.5.5; developer platform/integrations " + own("H"), "FR-V12-E-010..022, FR-V12-E-070..089")
add("01", "V12 baseline", "Honest boundary: specification and prototype only; enterprise grade earned in production through R0-R5", C,
    "Part 0 status vocabulary; Part 9.3", "Status vocabulary restated in §11.5.0", "")
add("01", "V12 baseline", "Commercial unit rule: 39 service SKUs sold; 156 workflows included under parent SKU, never sold separately", N,
    "DEC-047 sells plan archetypes only", "Adopted: SKU grant is the commercial unit, workflows inherit (DEC-584, FR-V12-E-045, FR-V12-E-059)", "DEC-584, FR-V12-E-045, FR-V12-E-059")
for r in tab("01_", 0)[1:]:
    g = {"Service SKUs / workflows / steps": "B", "Website routes / Admin screens (each on desktop and mobile)": "G", "Requirements": "A",
         "Jurisdiction rules": "I", "API operations": "H", "Database tables": "I", "Locales in prototype": "G", "V12 browser checks": "J",
         "Automated accessibility": "J", "Weighted RCTCFE score": "K"}.get(r[0], "A")
    add("01", "V12 inventory", "Inventory count: " + r[0] + " = " + r[1], NA, "-", own(g))
area_map = {
    "Multi-tenant isolation": (C, "Part 3.1 ADR-002; Part 3.3 RLS; Part 4.1 AZ-10", "Hierarchy and isolation invariants restated (§11.5.5.1)", "FR-V12-E-001..005"),
    "Identity: SSO, SCIM, MFA, sessions": (P, "Part 4.1 §4.3 (IdP reuse, MFA, sessions); no SSO federation or SCIM", "Specified §11.5.5.2", "FR-V12-E-010..015"),
    "Custom roles, separation of duties, audit/SIEM": (P, "Part 2.3 R01-R20, ABAC-03 SoD; hash-chained audit; no custom roles or SIEM", "Specified §11.5.5.2", "FR-V12-E-016..019"),
    "Business operations: billing, support, contracts": (P, "Part 3.1 §3.1.4.9; Part 8.3c §8.3.5.13", "Specified §11.5.5.5-6", "FR-V12-E-055..089"),
    "Reliability: SLOs, incidents, status, DR": (P, "Part 4.3 §4.40-4.47; Part 3.1 §3.1.13", "Specified §11.5.5.7-9", "FR-V12-E-095..127"),
    "Global readiness: locales, RTL, tax, regions": (X, "DEC-421 single region; DEC-027 GST only", "Tax rules configured (§11.5.5.6); second region CONFLICT-832", "CONFLICT-832, FR-V12-E-074"),
}
for r in tab("01_", 1)[1:]:
    if r[0] in area_map:
        b, loc, act, ids = area_map[r[0]]
        add("01", "Enterprise readiness by area", r[0] + ": specified " + r[1] + "; prototype " + r[2] + "; production " + r[3], b, loc, act, ids,
            F if b == X else M)
    else:
        g = {"Product functionality (39 services / 156 workflows)": "B", "API platform, webhooks, SDKs, developer portal": "H",
             "Data export, residency, BYOK, sandboxes": "I", "Integrations / connectors": "H", "AI governance and evaluation": "F",
             "Compliance: jurisdictions, consent, DSAR, breach": "I", "Security programme and certifications": "I", "Accessibility": "G"}[r[0]]
        add("01", "Enterprise readiness by area", r[0] + ": specified " + r[1] + "; prototype " + r[2] + "; production " + r[3], NA, "-", own(g))
add("01", "Artifact checksums", "SHA-256 of the four V12 HTML prototypes (repeated in V12, V11, V10 sections)", NA, "-", own("G"))
for r in tab("01_", 3)[1:]:
    if r[0] == "C3":
        add("01", "V11 corrections", "C3 recovery objectives approved by product owner 28 Nov 2026 (DEC-V11-01); platform-owner cost confirmation open", P,
            "DEC-018; ADR-102 RC classes; CONFLICT-462 (growth RTO 2 h pending)", "Adopted as DEC-595; cost confirmation tied to CONFLICT-833", "DEC-595, FR-V12-E-123")
    else:
        add("01", "V11 corrections", r[0] + " " + r[1] + ": " + r[2][:90], NA, "-", "prototype defect/evidence item " + own("J"))
add("01", "V11 inventory", "V11 verified counts (39/156/517, 36/143, 233/30, 35/13/23, 77 checks, 0 axe violations, RCTCFE 8.40)", NA, "-", own("K"))
add("01", "V10 baseline", "V10 authoritative release baseline and source precedence; REC-01-30 are reconciliation actions, not features", C, "Part 9.10 DEC-415", "Precedence rule adopted for platform chapters (DEC-580)", "DEC-580")
add("01", "V10 baseline", "V10 inventory: 25 foundations / 15 engines / 20 agents; 179 unique screens; 35/21/13/23 KPIs", P, "No foundation or engine register", "Foundations/engines registered §11.5.5.4; agents " + own("F"), "FR-V12-E-048, FR-V12-E-049")
add("01", "V10 baseline", "Recovery objectives DEC-V9-01 approved (DEC-V11-01); production gate open", P, "DEC-018; ADR-102", "DEC-595", "DEC-595")
add("01", "V10 REC", "REC-29 one V10 precedence and inventory; checksums match", NA, "-", "document-owner action " + own("L"))
for r in tab("01_", 9)[1:]:
    if r[0] == "P4":
        add("01", "V9 promotions", "P4 go-live, rollback and handover sequence GO-01...08 normative in FSD ch39", P, "Part 4.4b DPL-SEQ, GL-E, RBK-T; Part 8.2", "GO IDs adopted with mapping (§11.5.5.10)", "FR-V12-E-130")
    elif r[0] == "P9":
        add("01", "V9 promotions", "P9 recovery objectives DEC-V9-01 (critical RPO <=15 min) normative in ch32, 36, 38", P, "DEC-018; ADR-102", "DEC-595", "DEC-595, FR-V12-E-123")
    else:
        add("01", "V9 promotions", r[0] + " " + r[2][:80], NA, "-", "promotion handled by owning group " + own("A"))
add("01", "V9 not promoted", "Page counts and API/table/test/traceability catalogues superseded by Appendices A-C", NA, "-", own("H"))
add("01", "V9/V8 inventories", "V9 and V8 verified inventory tables and checksums", NA, "-", own("K"))
add("01", "V8 source reconciliation", "Eleven V7 input artifacts with owners and SHA-256 prefixes", NA, "-", own("L"))
add("01", "V8 RCTCFE stage gates", "Eleven-stage RCTCFE gate register; stage 10 architecture/redundancy audit (one requirement per behaviour)", P, "Part 9.3 quality report", "One-requirement-per-behaviour rule applied to platform FRs (§11.5.3)", "")
for r in tab("01_", 16)[1:]:
    if r[0] == "D8":
        add("01", "V8 change control", "D8 architecture depth: deployment topology, environments, regions, queues, CI/CD, backup/DR runbooks", P, "Part 3.1 §3.1.6 (AWS-only, superseded by DEC-421)", "DEC-421 topology written in full (§11.5.5.8)", "FR-V12-E-105..116, ADR-150")
    elif r[0] == "D10":
        add("01", "V8 change control", "D10 separation of duties: requester != reviewer; Running -> Reconciling -> Completed", C, "ABAC-03; Part 2.3 run state machine", "SoD constraint extended to custom roles (FR-V12-E-017)", "FR-V12-E-017")
    elif r[0] == "D12":
        add("01", "V8 change control", "D12 prototype layering partial by design; production implements one behaviour once (ch35)", C, "Part 4.4a CS-GEN", "Rule restated §11.5.5.8", "")
    else:
        add("01", "V8 change control", r[0] + " " + r[1] + ": " + r[3][:80], NA, "-", "prototype/document correction " + own("J"))
add("01", "Status vocabulary", "Prototype != proposed specification != approved contract != implemented feature != production-verified outcome", C, "Part 0 / Part 9.3", "Applied to every V12 item in this part", "")
add("01", "V7/V6/V5 scope", "V7 six-artifact baseline, V6 universal architecture (169 screens), V5 135 OPT dimension table", NA, "-", own("A"))
add("01", "V6 precedence", "SM-APPLICATION-6 supersedes SM-APPLICATION-4; importer rejects old envelope versions; production migration adapter separately designed and tested", N, "No envelope contract", "FR-V12-E-030, FR-V12-E-031", "FR-V12-E-030, FR-V12-E-031")
brv3 = {
    "01": (P, "DEC-047 plans; no SKU registry", "SKU registry + commercial unit rule", "FR-V12-E-045, FR-V12-E-059"),
    "05": (P, "Part 3.1 §3.1.4.9 ApplicationDraft; FR-W32", "Envelope fields and wizard", "FR-V12-E-030, FR-V12-E-032"),
    "06": (N, "-", "Revision integrity", "FR-V12-E-031"),
    "07": (P, "BRL-SVC-01", "Intake validation, stale revision, no entitlement activation", "FR-V12-E-031, FR-V12-E-038"),
    "08": (C, "Part 2.3 R01-R20; DEC-056; Part 8.3c", "Customer parity restated; demo switch is not identity", "FR-V12-E-021"),
    "09": (P, "BRL-SVC-03/04; ENT-183 aggregated meter only", "Reservation ledger", "FR-V12-E-070, FR-V12-E-071"),
    "12": (P, "Part 8.3c CSO-01..12", "Quote/agreement/payment-evidence stages", "FR-V12-E-055..058"),
}
for r in tab("01_", 21)[1:]:
    key = r[0][6:8]
    if key in brv3:
        b, loc, act, ids = brv3[key]
        add("01", "Governing FRs", r[0] + ": " + r[1][:110], b, loc, act, ids)
    else:
        g = {"02": "B", "03": "B", "04": "G", "10": "K", "11": "B", "13": "C", "14": "J"}[key]
        add("01", "Governing FRs", r[0] + ": " + r[1][:110], NA, "-", own(g))
add("01", "Governing FRs note", "Reuse existing authentication and security after compatibility tests; do not rebuild merely to change framework", C, "DEC-003, DEC-019 Sprint 0 spike", "Extended to federation checks (FR-V12-E-010)", "FR-V12-E-010")
add("01", "Artifact status", "302 API / 149 entity historical candidates; 195 scenarios not run; 180 historical decisions pending", NA, "-", own("L"))

# ---------------- Chapter 02 ----------------
add("02", "V8 topology", "Topology proposed and provider-neutral; cloud provider is decision DEC-V7-03", C, "DEC-421 (Founder decision fills DEC-V7-03)", "Mapped to DEC-421 (ADR-150)", "DEC-589, ADR-150")
add("02", "V8 topology", "Must run in two isolated regions (India, EU); tenant data stays in onboarding region (CJ-R09)", X, "DEC-421 Mumbai only; ADR-019 single region", "CONFLICT-832: region-ready design now, EU stamp on Founder approval", "CONFLICT-832, DEC-590, ADR-151, FR-V12-E-004", F)
lay = {
    "Edge": (P, "ADR-043 CloudFront/WAF (superseded by DEC-421 Vercel CDN/firewall)", "Vercel edge + firewall; Django two-layer rate limits"),
    "Web": (C, "ADR-006 two SPAs; DEC-421 Vercel projects", "Two Vercel projects, CSP"),
    "API": (P, "ADR-001; DEC-421 AWS ap-south-1", "ECS on AWS, stateless tasks, autoscale"),
    "Policy": (C, "ADR-004 PDP in-process; fail closed", "Pack cache per region"),
    "Workers": (P, "ADR-021 queue topology (different names)", "Queue-class mapping table"),
    "Scheduler": (C, "ADR-028 Celery Beat with lock", "Single leader per region"),
    "AI gateway": (C, "ADR-008; DEC-418", "Region-pinned endpoints recorded"),
    "Provider gateway": (C, "ADR-009; ADR-103", "No change"),
    "Data": (P, "ADR-002, ADR-007; DEC-421 Supabase", "Supabase Postgres + read replica option"),
    "Cache/queue": (C, "ADR-101 Valkey", "Key prefix includes policy version"),
    "Objects": (C, "ADR-024 S3", "Per-region bucket, KMS"),
    "Secrets": (C, "ADR-014; Part 4.1 §4.6", "Supabase service key in Secrets Manager"),
    "Observability": (P, "ADR-025; Part 4.1 CERT-In logs", "In-region retention incl. Vercel/Supabase logs"),
}
for r in tab("02_", 0)[1:]:
    b, loc, act = lay[r[0]]
    add("02", "Topology layers", r[0] + " / " + r[1] + ": " + r[2][:70] + "; rule: " + r[3][:70], b, loc, act, "FR-V12-E-105, FR-V12-E-106" if r[0] == "Workers" else "FR-V12-E-105")
envs = {"dev": (P, "Part 3.1 §3.1.14 local/test"), "sit": (P, "test (CI) + nightly sandbox run"), "uat": (P, "staging"),
        "prod-in / prod-eu": (X, "prod (Mumbai only)")}
for r in tab("02_", 1)[1:]:
    b, loc = envs[r[0]]
    add("02", "Environments", r[0] + ": " + r[1] + "; data " + r[2] + "; gate " + r[3][:80], b, loc,
        "prod-eu reserved, not built (CONFLICT-832)" if b == X else "V12 names adopted with mapping (DEC-592)",
        "DEC-592, FR-V12-E-107" + (", CONFLICT-832" if b == X else ""), F if b == X else M)
add("02", "Context", "Public browser -> CDN/public read API; portal -> DRF policy middleware -> PostgreSQL; worker -> policy check -> provider/AI gateway; verified inbox; public build never sees tenant data", C,
    "Part 3.1 §3.1.2-3.1.3; ADR-010", "Restated on DEC-421 view", "FR-V12-E-105")
bnd = {"Public": "Part 3.1 ADR-010 snapshots; AZ-01", "Tenant": "Part 4.1 AZ-03..06", "Worker": "Part 4.1 AZ-11",
       "Provider": "ADR-103; Part 4.1 §4.6", "Portfolio": "Part 2.3 portfolio read-only; DEC-056"}
for r in tab("02_", 2)[1:]:
    add("02", "Boundaries", r[0] + ": " + r[1], C, bnd[r[0]], "Mapped (§11.5.5.1)", "FR-V12-E-003" if r[0] == "Portfolio" else "")

# ---------------- Chapter 03 ----------------
steps = ["RunRequest received; scope from verified membership; DTO validated; idempotency key checked",
         "Entitlement, configuration version, budget reservation and policy snapshot recorded; Queued or Held",
         "Steps dispatched by class: deterministic, evidence, AI inference via gateway, policy gate via engine/reviewer",
         "Untrusted-content steps run without effect tools (AIX-09); outputs validated against schema and claims",
         "Before effect: CJ preflight + approval (requester != reviewer) + budget recheck; intent persisted (outbox)",
         "Effect dispatched; Reconciling until signed receipt matched; uncertain stays Reconciling, never blind retry",
         "Usage ledger and ai_usage_event committed; KPIs and cost per accepted result; audit"]
for i, s in enumerate(steps, 1):
    b = P if i in (2, 7) else C
    add("03", "V8 runtime sequence", "Step %d: %s" % (i, s), b, "Part 2.2 execution engine; Part 3.1 §3.1.7.1; PDP C5",
        "Reservation and usage-ledger commit specified (FR-V12-E-071)" if b == P else "No change", "FR-V12-E-060, FR-V12-E-071" if b == P else "")
add("03", "GC-01", "Modular monolith discipline: extract only with measured bottleneck and total-cost comparison", C, "ADR-001", "No change")
add("03", "Stack", "React/TypeScript; Django REST; PostgreSQL; Celery/Beat, Valkey; object storage; pgvector when approved; outbox, inbox, per-tenant fairness; separate from Investment Automation", C, "Part 3.1 §3.1.8; DEC-058; DEC-421", "Stack restated on DEC-421 view")

# ---------------- Chapter 04 ----------------
add("04", "GC-12", "Reusable versioned React components and domain libraries; commercial and investment scope tests independent", C, "ADR-006; Part 3.4 FR-ENH-B-021", "No change")
comp = {"Catalogue": (N, "catalog app is product truth, not SKU catalogue", "FR-V12-E-045..051"),
        "Tenant & identity": (C, "core.tenancy, core.identity", "FR-V12-E-001..022"),
        "Commercial billing": (P, "saas app (plans, meters, invoices); no quote/agreement/payment chain", "FR-V12-E-055..089"),
        "Workflow control": (C, "automation app", ""), "Domain modules": (NA, "-", ""),
        "Provider gateway": (C, "integrations; ADR-103", ""), "Observability": (C, "ops; ADR-025", "")}
for r in tab("04_", 0)[1:]:
    b, loc, ids = comp[r[0]]
    if b == NA:
        add("04", "Components", r[0] + ": " + r[1], NA, "-", own("B"))
    else:
        add("04", "Components", r[0] + ": " + r[1], b, loc, "Specified §11.5.5" if b != C else "No change", ids)
add("04", "Transaction boundary", "Domain record + outbox in one commit; no transaction across external call; intent and idempotency before dispatch; reconcile separately", C, "ADR-003; Part 3.4 §3.4.5.3 B", "No change")

# ---------------- Chapter 05 ----------------
add("05", "V6 isolation contract", "All canonical entities carry trusted tenant_id; company-scoped carry company_id with composite FKs; tenant vs company membership vs portfolio grant distinguished", P,
    "ADR-002 (tenant_id, startup_id)", "Company = Startup mapping; Organization added (ADR-140)", "DEC-581, ADR-140, FR-V12-E-001, FR-V12-E-002")
add("05", "V6 isolation contract", "Server-derived session context, RLS non-owner role, cache/storage/vector keys, worker scope; operator config management does not imply CRM access", C, "Part 4.1 AZ-10..13; DEC-056", "No change", "FR-V12-E-005")
add("05", "MT-01", "Tenant is contract/security root; organization and company separately keyed; company cannot cross tenant via parent FK", P, "Tenant/Startup only", "Organization entity and composite FK", "FR-V12-E-001")
add("05", "GC-02", "Shared isolated infrastructure with fair quotas; dedicated tiers only when justified incl. maintenance cost", C, "ADR-002; ADR-021 fairness", "Dedicated tier = separate Supabase project option (§11.5.5.8)", "FR-V12-E-105")
add("05", "SEC-02", "Non-owner app role, RLS, scoped keys, transaction-local context; deny missing scope; pooled connection reuse cannot leak", P, "AZ-10; RLS fixture", "Supabase pooler (transaction mode) reset test added", "TC-V12-E-005")
add("05", "Scope rules", "Validate company belongs to tenant; composite scoped FK/unique; workers same restrictions; isolate object paths, vector filters, cache keys; support grant audited; test pooling; no global contact search", C, "Part 3.3 STD-T/STD-SA; AZ-11..13", "No change", "FR-V12-E-005")

# ---------------- Chapter 06 ----------------
ent = tab("06_", 0)[1:] + tab("06_", 1)[1:]
entmap = {"ENT-IDN-01": (N, "IdP reuse only (DEC-003); no tenant federation", "FR-V12-E-010", "ADR-141"),
          "ENT-IDN-02": (P, "Domain verification for websites only", "FR-V12-E-011", ""),
          "ENT-IDN-03": (N, "-", "FR-V12-E-012", "ADR-142"),
          "ENT-IDN-04": (P, "Part 4.1 §4.3.3 MFA per role; not tenant-configurable", "FR-V12-E-013", ""),
          "ENT-IDN-05": (P, "Part 4.1 §4.3.4 fixed values", "FR-V12-E-014", ""),
          "ENT-IDN-06": (P, "Break-glass role (Part 3.1 §3.1.14) for platform; not tenant", "FR-V12-E-015", ""),
          "ENT-ACC-01": (N, "Fixed roles R01-R20", "FR-V12-E-016", "ADR-143"),
          "ENT-ACC-02": (P, "ABAC-03 SoD at approval time", "FR-V12-E-017", "ADR-143"),
          "ENT-ACC-03": (P, "Hash-chained audit (Part 3.3); export format not specified", "FR-V12-E-018", ""),
          "ENT-ACC-04": (N, "Part 4.1 §4.10 log architecture; no tenant SIEM", "FR-V12-E-019", ""),
          "ENT-ACC-05": (C, "DEC-056 SupportAccessGrant (72 h max)", "FR-V12-E-020", "")}
for r in ent:
    b, loc, fr, adr = entmap[r[0]]
    add("06", "V12 enterprise identity", r[0] + " (" + r[1] + ", " + r[5] + ", " + r[6] + "): " + r[2] + " Acceptance: " + r[3], b, loc,
        "Specified in full (§11.5.5.2); scheduling under CONFLICT-834", ", ".join(x for x in [fr, adr, "DEC-582"] if x))
add("06", "V6 authorization matrix", "Anonymous / verified customer / tenant requester / reviewer / auditor / operator / portfolio / service principal; demo persona switch is not identity; effect checks server-enforced", C,
    "Part 2.3 R01-R20; Part 4.1 §4.4", "Role mapping table (§11.5.5.2)", "FR-V12-E-021")
add("06", "MT-07", "Independent portfolio grants: explicit, revocable, resource and aggregate scoped; independent clients excluded", P, "Owner Portfolio read-only (BRL-TEN)", "PortfolioGrant entity", "FR-V12-E-003")
add("06", "SEC-01", "Central authorization over identity, membership, role, resource, SKU, action, policy version and consent; enforced at API, worker and adapter", P, "AZ-01..15; PDP", "SKU dimension added to decision request", "FR-V12-E-021, FR-V12-E-060")
add("06", "SEC-03", "Privileged MFA/passkeys, recovery controls, fresh verification for sensitive changes", C, "Part 4.1 §4.3.3", "Tenant policy layer (FR-V12-E-013)", "FR-V12-E-013")
for r in tab("06_", 2)[1:]:
    b = P if r[0] in ("Service principal", "Tenant owner") else C
    add("06", "Role/control table", r[0] + ": " + r[1], b, "Part 2.3 roles; Part 4.1 §4.3.5", "Mapped (§11.5.5.2)", "FR-V12-E-021")
add("06", "Auth contract", "Reuse actual auth contract; MFA privileged; session revocation; recovery rate limits; CSRF/CORS; deny mismatched audience", C, "Part 4.1 §4.3.1-4.3.4", "No change")
add("06", "Policy precedence", "Emergency stop > revoke/suppression > mandatory regulation > tenant cap > action grant", C, "Part 3.1 §3.1.4.2 evaluator order, first deny wins", "Equivalence shown (§11.5.5.2)", "FR-V12-E-022")

# ---------------- Chapter 07 ----------------
add("07", "REC-04", "A112: compare candidate and active hierarchy fields, show affected workflows, versioned review and rollback drafts; no change rewrites in-flight snapshot", P, "A112; ConfigRevision", "Hierarchy diff + rollback-as-draft", "FR-V12-E-039")
add("07", "MOB-04", "Progressive onboarding of 14 customer types, eight stages on either device; mobile Step n of 8", P, "W33 wizard (single flow)", "Eight-stage contract; UI " + own("G"), "FR-V12-E-032")
add("07", "V6 envelope", "SM-APPLICATION-6: applicationId, revision, product=commercial, kind=request, configuration, local fingerprint; hierarchy object with customerType and eight collections", N, "-", "Server contract", "FR-V12-E-030")
add("07", "V6 validation", "Parent/relationship checks, allowed service/workflow IDs, same-company market linkage, identity, financial bounds, duplicate names before submit/import", N, "-", "Validator rules HV-01..10", "FR-V12-E-040")
add("07", "V6 completeness", "Every operating company must have an offering, target market and channel account", N, "-", "HV rule", "FR-V12-E-040")
add("07", "V6 fingerprint", "FNV-style local fingerprint is not a security signature; production uses authenticated API, cryptographic digest, idempotent constraints, verified scope; browser IDs/statuses untrusted", P, "BRL-SVC-01", "SHA-256 canonical digest + server record", "FR-V12-E-031")
add("07", "V6 saga", "Provisioning saga: tenant contract -> organization -> company nodes -> membership approvals -> graph review -> entitlement allocation -> provider verification -> activation", P, "Part 3.1 PROVX in core.tenancy (unspecified steps)", "Saga PS-01..08", "FR-V12-E-038, ADR-149")
add("07", "V6 rollback", "Rollback copies historical graph into new draft, keeps history, revalidates; retired nodes cannot execute; actor separation and version locking", P, "ConfigRevision", "Specified", "FR-V12-E-039")
mt7 = {"MT-03": (P, "No ceiling stated; Topology sizing", "FR-V12-E-035"), "MT-04": (N, "-", "FR-V12-E-034"),
       "MT-05": (P, "Tenant->startups", "FR-V12-E-002"), "MT-08": (P, "W33 wizard", "FR-V12-E-032"),
       "MT-17": (N, "Single country per startup", "FR-V12-E-036"), "MT-19": (P, "Tenant timezone/locale (Part 2.4 i18n)", "FR-V12-E-037")}
for k, (b, loc, fr) in mt7.items():
    add("07", "V6 MT", k + " requirement and acceptance MT-TC-" + k, b, loc, "Specified", fr)
add("07", "SEC-05", "Authenticated application integrity: signed identity, canonical digest, revision and idempotency; replay cannot create workspace", N, "-", "Specified", "FR-V12-E-031")
add("07", "CV-01", "Progressive onboarding: minimal fields first; incomplete draft resumes without premature quote/entitlement", C, "ApplicationDraft 30 days", "No change", "FR-V12-E-033")
add("07", "CV-02", "Server-backed authorized draft revisions; stale revision rejected; nothing sensitive in public cache", P, "ApplicationDraft revision", "Stale-revision rule", "FR-V12-E-033")
add("07", "V4 handoff", "V4 envelope binds application ID, revision, fingerprint, administrator email; import private and replay-safe; no inherited approval", N, "-", "Superseded by SM-APPLICATION-6 adapter", "FR-V12-E-030")
for r in tab("07_", 1)[1:]:
    add("07", "V4 JSON areas", r[0] + ": " + r[1][:120], N, "-", "Field catalogue (§11.5.5.3)", "FR-V12-E-030")
add("07", "V4 saga", "Verify account and approved quote -> allocate IDs -> membership/config version -> entitlement/quota -> verify storage/connector -> activate; idempotent unique provisioning key; held on failure; compensate only new resources", P, "Part 3.1 PROVX", "Saga PS-01..08 with compensation", "FR-V12-E-038")
add("07", "V4 config schema", "Legal entity, locale, ICP, offerings, claims, channel policy, roles, budgets, capability grants; preview diff and simulate before activation", C, "ConfigRevision; A112; Part 2.2 simulation", "No change", "FR-V12-E-039")
for r in tab("07_", 2)[1:]:
    add("07", "Canonical application V4", r[0] + ": " + r[1][:100] + " | " + r[2][:80], N if r[0] in ("Envelope", "Fingerprint", "Replay and revision") else P,
        "ApplicationDraft (ENT-187)", "Field and validation catalogue (§11.5.5.3)", "FR-V12-E-030, FR-V12-E-031")

# ---------------- Chapter 08 ----------------
add("08", "Foundation IDs", "Foundation IDs SM-xx-yy taken from prototype; foundations included and never priced separately", N, "-", "Register + rule", "FR-V12-E-048")
fmap = {"SM-01": "W33 wizard, AP-01 simulator", "SM-11": "saas module (trial, meters, entitlement, offboarding)", "SM-12": "AI gateway (Part 7.3)",
        "SM-13": "Part 3.1 §3.1.13; outbox reconcile", "SM-14": "Part 8.3c optimization model"}
for r in tab("08_", 0)[1:]:
    add("08", "Foundation register", r[0] + " " + r[1] + " (" + r[2] + ")", P, fmap[r[0][:5]], "Registered with blueprint owner module", "FR-V12-E-048")
for r in tab("08_", 1)[1:]:
    add("08", "Engine register", r[0] + " " + r[1] + ": " + r[2], P, "Part 3.1 modules (no engine IDs)", "Registered with module mapping", "FR-V12-E-049")
lc = {"Service SKU": ("FR-V12-E-045", N), "Workflow version": ("FR-V12-E-046", P), "Bundle": ("FR-V12-E-047", N), "Capability": ("FR-V12-E-050", N)}
for r in tab("08_", 2)[1:]:
    fr, b = lc[r[0]]
    add("08", "Entity lifecycle", r[0] + ": " + r[1], b, "WorkflowTemplate versions (Part 3.3)" if b == P else "-", "Specified", fr)
add("08", "Public projection", "Description, deliverables, readiness, prerequisites, approved pricing/quote CTA, locale; never expose internal records", P, "ADR-010 publication snapshots", "Catalogue projection", "FR-V12-E-051")

# ---------------- Chapter 09 ----------------
add("09", "REC-27", "Controlled suspension/offboarding: revoke credentials/grants/schedules, verified export, retention, reconciliation; no deletion under legal hold", C, "Part 8.3c CSO-11/12; BRL-SVC-06", "Lifecycle mapping", "FR-V12-E-058")
add("09", "V6 entitlement", "Subscription owns stable service grants, scope and quota; WorkflowConfiguration references offering, market, account, SKU, workflow version, cap, schedule, authority", N, "Entitlement per meter only", "SkuGrant + WorkflowConfiguration", "FR-V12-E-059")
add("09", "V6 entitlement", "Service selection limits configuration; workflow ID must belong to SKU; execution validates company, offering, market, account, entitlement, provider/consent/policy, authority, local and parent budgets; draft confers no approval", P, "PDP C1-C8", "Validation list EV-01..10", "FR-V12-E-059, FR-V12-E-060")
add("09", "MT-06", "Tenant lifecycle: pending, active, suspended, offboarding, retired; preserve ledger; revoke new execution on suspension", P, "Subscription states (trial, active, past_due, suspended, cancelled)", "Tenant lifecycle separate from subscription", "FR-V12-E-058")
add("09", "MT-16", "Configurations reference entitlement and SKU/workflow; scope by company/offer/market/account; no duplicate definition or forced purchase", N, "-", "Specified", "FR-V12-E-059")
add("09", "RT-11", "Plan changes: effective date, proration, usage reconciliation, pause/downgrade/cancellation; preview with no silent loss or charge", N, "-", "Specified", "FR-V12-E-062")
add("09", "CV-05", "Approved quote/rate, period, unit, tax, overage, pass-through; quote shows itemized approved version or pending", P, "DEC-047 no price until approval; Part 8.3c fee types", "Price book", "FR-V12-E-065")
add("09", "CV-12", "Accepted quote and agreement bound to verified signer and exact digest; material edit invalidates", P, "Startup commercial quotes (EP-13) only", "SaaS agreement acceptance", "FR-V12-E-056")
for r in tab("09_", 1)[1:]:
    add("09", "Commercial state machine", r[0] + ": " + r[1], N if "quote" in r[0].lower() or "accepted" in r[0].lower() or "payment" in r[0].lower() else P,
        "ENT-182 subscription states", "State machine SUB-T01..T10", "FR-V12-E-057")
add("09", "Enforcement points", "Check entitlement at API, enqueue, worker and effect", P, "PDP C5 at plan and dispatch", "Four-point enforcement", "FR-V12-E-060")
add("09", "Optional upstream", "Missing optional upstream service accepts authorized supplied input; missing required input holds", N, "-", "Specified", "FR-V12-E-061")
add("09", "Separation", "Pricing, usage, delivery, taxes and financial events kept separate from subscriber business revenue", C, "BRL-FIN-08; Part 8.3c", "No change", "FR-V12-E-079")
cl = {"Quote": "FR-V12-E-055", "Upgrade/downgrade": "FR-V12-E-062", "Suspension and renewal": "FR-V12-E-063",
      "Refund/cancellation": "FR-V12-E-064", "Pricing": "FR-V12-E-065"}
for r in tab("09_", 2)[1:]:
    add("09", "Commercial lifecycle", r[0] + ": " + r[1][:110] + " | " + r[2][:70], P, "Part 8.3c §8.3.5.13.2-4; BRL-SVC-05..07", "Specified", cl[r[0]])

# ---------------- Chapter 10 ----------------
bizmap = {"ENT-BIZ-01": (P, "saas meters, invoices, credits; no rating/dunning/rev-rec", "FR-V12-E-072..078"),
          "ENT-BIZ-02": (P, "DEC-047 pending prices", "FR-V12-E-065"),
          "ENT-BIZ-03": (P, "e-sign adapter for startup contracts (ADR-038)", "FR-V12-E-056"),
          "ENT-BIZ-04": (C, "Part 8.3c CSO stages; LJ-13", "FR-V12-E-089"),
          "ENT-BIZ-05": (N, "-", "FR-V12-E-087"),
          "ENT-BIZ-06": (N, "-", "FR-V12-E-088")}
for r in tab("10_", 0)[1:]:
    b, loc, fr = bizmap[r[0]]
    add("10", "V12 billing", r[0] + " (" + r[1] + ", " + r[5] + "): " + r[2] + " Acceptance: " + r[3], b, loc,
        "Specified (§11.5.5.6); go-live scheduling CONFLICT-834", fr + ", DEC-587")
for r in tab("10_", 1)[1:]:
    india = r[0].startswith("India") or r[0].startswith("Export")
    us = r[0].startswith("United States")
    add("10", "Tax engine", r[0] + ": " + r[1] + " (" + r[2] + ")", P if india else N,
        "DEC-027 GST; Part 4.1 §4.12.4" if india else "-",
        "Tax rule row TX-xx; live in India; other rows configured and disabled until market approval (CONFLICT-835)" if not india else "Tax rule row TX-xx",
        "FR-V12-E-074" + ("" if india else ", CONFLICT-835") + (", GAP-839" if us else ""), M if india else F)
add("10", "Tax note", "Tax rules are configuration pending tax-adviser approval (CJ-R16)", P, "DEC-027 verify", "Approval workflow on tax rule versions", "FR-V12-E-074, GAP-838")
add("10", "Tax note", "Invoice arithmetic in integer minor units; total = net + tax enforced in database (C2-T8)", N, "numeric(18,2) amounts", "CHECK constraint", "FR-V12-E-073")
add("10", "REC-26", "Service-specific SLA, delivery responsibility, monthly value and acceptance matrix; fees approval pending; separate usage, pass-through and support costs", P, "Part 8.3c SLA-01..12 (platform level)", "Per-SKU service sheet", "FR-V12-E-085")
add("10", "MOB-15", "Mobile totals equal desktop; never combine currencies without approved conversion; SaaS fees separate from subscriber revenue", C, "Part 2.4 FX; BRL-FIN-08", "No change", "FR-V12-E-080")
add("10", "V6 currency", "ISO currency, exact minor units/decimal quantity; native ledger immutable; FX needs rate, direction, date, source, version, precision, approval; missing rate excluded but counted", P, "FxSnapshot (DEC-016)", "FX rule set", "FR-V12-E-080")
add("10", "MT-14", "Subscriber offering price/currency/terms versioned separately from SaaS fee and quote", C, "OfferingVersion vs PlanVersion", "No change", "FR-V12-E-081")
add("10", "MT-21", "Multi-currency transactions and reporting with missing-rate exception", C, "Part 2.4; FxSnapshot", "No change", "FR-V12-E-080")
add("10", "Ledger proposal", "Separate estimate, reservation, consumption, release and reversal entries; append-only keyed by tenant, company, SKU, workflow_version, run, period, unit, currency, cost_category, idempotency_key", N, "UsageMeterReading hourly aggregates", "UsageLedgerEntry", "FR-V12-E-070, ADR-146")
add("10", "Ledger proposal", "Store provider receipt, price_version, allocation basis, correlation_id, evidence ref; atomic reservation before enqueue/effect; release unused; retain on uncertain effect; never overwrite", N, "-", "Specified", "FR-V12-E-070, FR-V12-E-071")
add("10", "GC-14", "Allocate direct fees, compute, support, overhead by documented bases; missing allocation shown unallocated", P, "Part 4.3 §4.46.3", "Allocation in ledger", "FR-V12-E-082")
add("10", "RT-07", "Remaining allowance, reservations, trend; alert before cap; no overage without approved terms", P, "Budget ladder (FR-ENH-B-022)", "Per-SKU forecast", "FR-V12-E-083")
add("10", "CV-13", "Approved payment provider, verified webhook, idempotent provisioning; duplicate receipt cannot activate twice; mismatch stays pending", P, "ADR-038 manual evidence path", "Collection adapter", "FR-V12-E-075, GAP-839")
add("10", "CS-14", "Billing disputes: itemized usage, invoice, credits, refund review; no refund before authorization and reconciliation", N, "-", "Dispute case", "FR-V12-E-084")
add("10", "Atomic reservation", "Per tenant/company/SKU/period, unique idempotency_key; lock or serializable; reserve <= remaining units and budget", N, "-", "Specified", "FR-V12-E-071")
add("10", "Ledger types", "Provider charge, SaaS invoice, subscriber payment, advertising spend use distinct ledger types and accounts", P, "BRL-FIN-08 separation", "ledger_type enum", "FR-V12-E-079")
add("10", "Rounding", "Deterministic tax and rounding policy by approved locale; reconcile duplicate and out-of-order webhooks", P, "ADR-030", "Rounding rule RND-01..04", "FR-V12-E-073, FR-V12-E-086")
add("10", "Metering contract", "Completed and active reservations counted; held/failed/canceled excluded; minor units; period bounds; unique keys; approved plan budget not UI cap", P, "BRL-SVC-03/04", "Specified", "FR-V12-E-070, FR-V12-E-071")

# ---------------- Chapter 32 ----------------
add("32", "Release rule", "Error-specific recovery: invalid input hold; read retry bounded; uncertain write reconcile; circuit-open defer to probe; crash resume after checkpoint; saturation backpressure", P, "Part 3.2 error model; Part 3.1 FM table", "Error class registry ERR-01..12", "FR-V12-E-095, ADR-152")
add("32", "Release rule", "Candidate SLO 99.9% monthly, p95 500 ms, critical RPO <=15 min / RTO <=4 h (DEC-V9-01) subject to drills; A089 lab not monitoring", P, "DEC-018 (99.5% pilot)", "SLO set with phase targets", "FR-V12-E-111, DEC-595")
st = {"ST-02": ("FR-V12-E-096", C, "Part 3.2 breaker (half-open)"), "ST-05": ("FR-V12-E-097", C, "ADR-023"),
      "ST-06": ("FR-V12-E-098", C, "Part 3.2 retry with jitter, Retry-After"), "ST-07": ("FR-V12-E-099", P, "DLQ after 5 failures; replay authorization not specified"),
      "ST-08": ("FR-V12-E-100", P, "ADR-035 rate limits; FR-ENH backpressure"), "ST-09": ("FR-V12-E-101", C, "FM-11"),
      "ST-10": ("FR-V12-E-102", C, "Part 4.3 synthetic journeys"), "ST-13": ("FR-V12-E-103", C, "Part 4.3 game days; ADR-135")}
for k, (fr, b, loc) in st.items():
    add("32", k, k + " requirement and OPT-TC-" + k + " acceptance", b, loc, "Parameters fixed (§11.5.5.7)" if b == P else "Mapped", fr)
for r in tab("32_", 0)[1:]:
    add("32", "Failure behaviour", r[0] + ": " + r[1], C if r[0] not in ("Conflict/version mismatch", "Incident / stop") else P,
        "Part 3.2 problem+json; FM table; RB-004", "ERR row", "FR-V12-E-095")

# ---------------- Chapter 35 ----------------
add("35", "REC-20", "Retain task IDs, predecessors, estimates; dependency-ordered slices", NA, "-", own("J"))
for r in tab("35_", 1)[1:]:
    if r[0] == "Repository structure":
        add("35", "Source coding controls", "Repository structure per product (website-react, admin-react, backend, tests, infra, docs); shared libraries without private data", C, "Part 4.3 §4.32 monorepo (ADR-060)", "Mapping note (§11.5.5.8)")
    else:
        add("35", "Source coding controls", r[0] + ": " + r[1][:90], NA, "-", own("J"))
add("35", "V8 prototype rule", "Production React/TypeScript implements each behaviour once from Appendices A-C; no prototype layering, demo identity switching or localStorage", C, "Part 4.4a CS-GEN", "No change")
add("35", "V8 coding paragraph", "Typed DTOs, scoped managers, PR evidence, backlog by foundation and SKU", NA, "-", own("J"))
add("35", "BUILD tasks", "SM-SVC-01...39-BUILD (39 rows): domain + four workflows + UI/adapter", NA, "-", own("J"))

# ---------------- Chapter 36 ----------------
add("36", "REC-21", "Engineering, pipeline and environment checklists with owners; protected branches, secret scanning, drift and locked builds tested", C, "Part 4.3 §4.32-4.35; Part 4.4b DPL-PRE", "Owner column added (§11.5.5.8)", "FR-V12-E-109")
for r in tab("36_", 1)[1:]:
    add("36", "CI/CD stages", r[0] + ": " + r[1] + " Failure: " + r[2], C if r[0] != "Activation" else P, "Part 4.3 §4.33; A090", "Stage mapping on DEC-421", "FR-V12-E-109" if r[0] != "Activation" else "FR-V12-E-132")
for r in tab("36_", 2)[1:]:
    b = C if r[0] in ("APP_ENV", "DATABASE_URL", "SECRET_MANAGER_REF", "PAID_FALLBACK_ENABLED", "LOG_REDACTION_POLICY") else P
    add("36", "Configuration contract", r[0] + " = " + r[1] + "; " + r[2], b, "Part 4.4b §4.4.5.3.2 ENV catalogue", "Variable adopted (CFG-V12 table)", "FR-V12-E-108")
for i, s in enumerate(["Commit: lint, type check, unit tests, secret scan, dependency audit (SBOM)",
                       "Contract: OpenAPI and JSON Schema contract tests; migration dry-run against Appendix C",
                       "Security: SAST, DAST on SIT, RLS negative suite, AI-INJ suite",
                       "AI: affected EVAL suites replay; block on regression (AIX-06)",
                       "Deploy: IaC per region; blue/green or canary; feature flags per tenant; automatic rollback on SLO breach"], 1):
    add("36", "V8 pipeline", s, C if i < 5 else P, "Part 4.3 §4.33-4.37", "Automatic SLO rollback rule fixed" if i == 5 else "No change", "FR-V12-E-109" if i < 5 else "FR-V12-E-110")
for r in tab("36_", 3)[1:]:
    b = P if r[0] in ("API availability", "Restore", "Effect reconciliation") else C
    add("36", "SLO", r[0] + ": " + r[1] + " (" + r[2] + ")", b, "Part 4.3 §4.40 SLO table; DEC-018", "SLO set (§11.5.5.8)", "FR-V12-E-111")
add("36", "Capacity", "No hardcoded customer count; stage 25+ owned then cohorts; measure p95 API/queue delay, quota isolation, fairness, recovery, cost-to-serve", C, "Part 3.4 ADR-108 growth profiles; Part 4.4b WP", "No change", "FR-V12-E-112")
add("36", "MT-39", "Provision 25 and staged higher volumes; check isolation, p95, queues, restores", P, "ADR-108", "Provisioning load test", "FR-V12-E-112")
add("36", "GC-03", "Autoscale by queue age, throughput, CPU, budget with cooldown and minimum capacity; no lost acknowledged jobs", P, "Part 3.1 §3.1.12.3", "ECS service autoscaling policy", "FR-V12-E-113")
add("36", "GC-04", "Benchmark serverless vs containers on identical workload; decision register with cost and p95", N, "ADR-013/100 chosen without benchmark", "Benchmark BM-01", "FR-V12-E-114")
add("36", "Accounts", "Separate dev/stage/prod accounts and data; IaC; private database; encryption; managed secrets; scoped service roles; no production data in dev", P, "Part 3.1 §3.1.6.1 accounts (AWS); DEC-421", "Account/project matrix incl. Vercel and Supabase", "FR-V12-E-115")

# ---------------- Chapter 38 ----------------
add("38", "REC-22", "Checkpoint migration/backfill, quarantine unknown scope, compare counts and financial aggregates; reversible", P, "Part 4.3 §4.37.2 expand/contract", "Quarantine table and reconciliation", "FR-V12-E-120")
for r in tab("38_", 1)[1:]:
    add("38", "Migration gates", r[0] + ": " + r[1][:120], C if r[0] in ("Expand", "Validate / contract", "Restore rehearsal") else P, "Part 4.3 §4.37.2, §4.47", "Gate MG-xx", "FR-V12-E-120" if r[0] not in ("Backup", "Restore rehearsal") else "FR-V12-E-122, FR-V12-E-124")
for r in tab("38_", 2)[1:]:
    add("38", "Recovery objectives", r[0] + ": RPO " + r[1] + ", RTO " + r[2] + " (" + r[3] + "); " + r[4], P if "Growth" in r[0] else C, "ADR-102 RC-1..3; CONFLICT-462", "DEC-595", "DEC-595, FR-V12-E-123")
add("38", "DR runbook", "PostgreSQL continuous WAL archiving + daily base backup, PITR 35 days, encrypted, same jurisdiction", X, "DEC-421: Supabase daily backups, PITR at growth gate", "CONFLICT-833", "CONFLICT-833, DEC-591, FR-V12-E-122", F)
add("38", "DR runbook", "Object storage versioning + cross-zone replication in region; no cross-jurisdiction replication of personal data", C, "ADR-024; S3 versioning", "No change", "FR-V12-E-122")
add("38", "DR runbook", "Quarterly restore drill per region (OPT-TC-ST-14); erasure requests replayed after restore", P, "Part 4.3 §4.47 drills", "Erasure replay step", "FR-V12-E-124")
add("38", "DR runbook", "Failover: replica promotion; DNS switch; effects queue paused until in-flight effects reconciled", P, "FM-02/04", "Effects pause step", "FR-V12-E-125")
add("38", "DR runbook", "Secrets and keys: KMS multi-zone; break-glass access audited", C, "Part 4.1 §4.5-4.6", "No change")
add("38", "GC-06", "Retention, legal hold, access, encryption per artifact class; archive only eligible data", C, "DEC-028; Part 3.3 retention", "No change", "FR-V12-E-126")
add("38", "ST-14", "Encrypted backups; restore test with integrity and scope checks; drill meets RPO/RTO or release blocker", C, "Part 3.1 §3.1.13.2; NFR-012", "No change", "FR-V12-E-124")
add("38", "CS-15", "Scoped export, retention/legal hold, verified deletion; revoke access and reconcile", C, "CSO-10/11; FR-A103", "No change", "FR-V12-E-127")
add("38", "Migration paragraph", "Map legacy capability IDs to SKU/workflow versions; preserve approved rights; dry-run; backup before change; active-run snapshot + current safety recheck; never claim restore without evidence", N, "-", "Capability migration", "FR-V12-E-121")

# ---------------- Chapter 39 ----------------
rp = {"R0": (C, "Waves W0-W1 (Part 8.1)", M), "R1": (P, "Release 1 (W0-W3)", F), "R2": (X, "Release 2 (W4-W5) + W6", F),
      "R3": (X, "Not in roadmap (DEC-421 single region)", F), "R4": (X, "Not in roadmap", F), "R5": (X, "Not in roadmap", F)}
for r in tab("39_", 0)[1:]:
    b, loc, after = rp[r[0]]
    add("39", "V12 roadmap", r[0] + " " + r[1] + ": scope " + r[2][:110] + " | exit " + r[3][:90], b, loc,
        "Phase mapping (§11.5.5.10)" + ("; CONFLICT-834/835" if after == F else ""),
        "FR-V12-E-134, DEC-596" + (", CONFLICT-834" if r[0] in ("R1", "R2") else "") + (", CONFLICT-835, CONFLICT-832" if r[0] in ("R3", "R4", "R5") else ""), after)
add("39", "V12 roadmap note", "Durations not estimated; engineering estimates at R0 planning from backlog (REC-20)", C, "Part 8.1 estimates", "Effort for this part §11.5.5.13", "")
add("39", "REC-24", "Maintenance cadence and evidence owners; overdue control escalates", C, "Part 8.3c MNT-*", "Mapping", "FR-V12-E-133")
for r in tab("39_", 2)[1:]:
    add("39", "Maintenance", r[0] + ": " + r[1][:110] + " | " + r[2][:60], C, "Part 8.3c §8.3.5.14.2 MNT calendar; Part 4.3 §4.46.6", "Mapped", "FR-V12-E-133")
for r in tab("39_", 3)[1:]:
    add("39", "Go-live sequence", r[0] + " " + r[1] + ": " + r[2][:110] + " | " + r[3][:70], C if r[0] not in ("GO-05",) else P,
        "Part 4.4b DPL-SEQ, DPL-ACT, GL-E, HO; RBK-T", "GO ID mapped", "FR-V12-E-130")
add("39", "Optimization release", "Pilot fixed workload; quality/consent/security/reliability gates before cheaper model or variant; flags and version snapshots; owner approval for pricing/provider/capacity/claims", C, "Part 8.3c §8.3.5.15.8; Part 7.3", "No change", "FR-V12-E-135")
add("39", "ST-11", "Feature flags, gradual exposure, error-budget gate, reversible release", C, "Part 4.3 §4.36-4.38", "No change", "FR-V12-E-131")
add("39", "Per-SKU release", "Release per SKU after requirements, provider permission, API/DB contracts, tests, security review, cost and SLA; progressive tenant cohort; reconcile completed effects rather than undo", N, "Release per wave and workflow", "SKU release gate", "FR-V12-E-132")

# ---------------- write ----------------
out = sys.argv[2]
with open(out, "w", newline="", encoding="utf-8") as fh:
    w = csv.writer(fh)
    w.writerow(["doc", "chapter", "section", "aspect_id", "aspect_summary", "status_before", "blueprint_location", "action", "new_ids", "status_after"])
    cnt = Counter()
    for i, a in enumerate(A, 1):
        ch, sec, summ, b, loc, act, ids, after = a
        cnt[ch] += 1
        aid = "E-%s-%03d" % (ch, cnt[ch])
        w.writerow([DOC, ch, sec, aid, summ, b, loc, act, ids, after])
        A[i - 1] = (aid,) + a

before = Counter(a[4] for a in A)
after = Counter(a[8].split(" (")[0] for a in A)
bych = OrderedDict()
for a in A:
    bych.setdefault(a[1], Counter())[a[4]] += 1
md = []
md.append("| Chapter | Aspects | Covered | Partially | Not covered | Conflict | N/A |")
md.append("|---|---|---|---|---|---|---|")
for ch, c in bych.items():
    md.append("| %s | %d | %d | %d | %d | %d | %d |" % (ch, sum(c.values()), c[C], c[P], c[N], c[X], c[NA]))
md.append("| **Total** | **%d** | **%d** | **%d** | **%d** | **%d** | **%d** |" % (len(A), before[C], before[P], before[N], before[X], before[NA]))
md.append("")
md.append("AFTER: " + ", ".join("%s %d" % kv for kv in after.items()))
md.append("")
md.append("| Aspect | Ch | Section | Aspect (V12) | Before | Blueprint location | Action | New IDs | After |")
md.append("|---|---|---|---|---|---|---|---|---|")
for a in A:
    if a[4] in (P, N, X):
        md.append("| %s | %s | %s | %s | %s | %s | %s | %s | %s |" % tuple(x.replace("|", "/") for x in (a[0], a[1], a[2], a[3], a[4], a[5], a[6], a[7], a[8])))
open(sys.argv[3], "w", encoding="utf-8").write("\n".join(md) + "\n")
print(len(A), dict(before), dict(after))
