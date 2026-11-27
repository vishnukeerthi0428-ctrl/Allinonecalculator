#!/usr/bin/env python3
"""Group B atomic aspect inventory for source-pack documents 04, 05, 09, 10.

Each aspect: (doc, section, aspect_id, summary, status, blueprint_location, action, new_ids)
status: Covered | Partially covered | Not covered | Conflict | Not applicable
Writes:
  final/coverage/B_coverage.csv
  assembly/source_pack/groupB_out/register.md   (markdown tables for Part 3.4 §3.4.3)
  assembly/source_pack/groupB_out/status_counts.md (table for §3.4.2)
Run: python3 -I groupB_aspects.py
"""
import csv
import os
from collections import Counter, OrderedDict

BP = "/home/user/Allinonecalculator/blueprint"
C, P, N, X, NA = "Covered", "Partially covered", "Not covered", "Conflict", "Not applicable"
CC = "Common core: see document 01/02 coverage"

A = []


def a(doc, sec, aid, summ, st, loc, act, new=""):
    A.append((doc, sec, aid, summ, st, loc, act, new))


# ---------------- Common core (identical text in 04, 05, 09, 10 and in 01/02) ----------------
for i, (sec, s) in enumerate([
    ("Product purpose and operating boundary", "Employee-operated commercial growth; no investor/fundraising functions"),
    ("Product purpose and operating boundary", "Independent deployment: own origin, API audience, DB, storage, queues, credentials, budget, billing, audit, backup"),
    ("Product purpose and operating boundary", "Two React frontends (commercial-website-react, commercial-admin-react), separate origins/sessions/OAuth clients"),
    ("Product purpose and operating boundary", "25+ owned startups and independent external tenants; tenant vs startup definitions; read-only owner group view"),
    ("Product purpose and operating boundary", "Support access client-approved, scope- and time-limited, audited"),
    ("Initial startup configurations", "AppNAI, MedMaarg, EduVerse, OrganicSpec profiles and commercial focus (4 rows)"),
    ("Initial startup configurations", "New startups by templates; genuinely new integrations may need engineering"),
    ("Technology and execution principles", "Stack, open-source-first, four autonomy policies, simulation zero effect, dispatch recheck"),
    ("Engineering contracts", "REST JSON, typed I/O, cursor pagination, idempotency, status codes 200-503, outbox, callbacks"),
    ("Engineering contracts", "Independent PostgreSQL, UUID PK, UTC, composite tenant/startup FKs, RLS, immutable approvals, decimal money"),
    ("Website and confidential Admin operating contract", "147 interfaces (34 W + 113 A); surfaces table; routing decision; publication snapshot; operational separation"),
    ("Implementation, verification and delivery controls", "Intro: proposed contracts, not production approval; scope reminders"),
    ("Acceptance and evidence record", "Evidence fields: responsible/reviewer, artefact/test evidence, decision, remediation, business acceptance"),
    ("Optimization engineering and acceptance", "Acceptance protocol: baseline, candidate, digest, actual cost/outcome, reviewer; missing evidence = Pending"),
    ("Current multi-startup, omnichannel and automation scope", "Nine added interfaces W31-W34, A109-A113 with purpose/acceptance; release condition"),
    ("Implementation acceptance and final decision controls", "Boundary and acceptance conditions: two-tenant fixture, revalidate at execution"),
], 1):
    a("04/05/09/10", sec, "B-CC-%02d" % i, s, C,
      "Part 0 §0.1–0.10; Part 1 §1.x; Part 2.1 §2.2; Part 2.5; Part 3.1 §3.1.1; Part 3.2 §3.2.1; Part 3.3",
      CC)

# ---------------- Sections shared by 04, 09, 10 only (not in 01/02) ----------------
S = "04/09/10"
a(S, "Independent deployment topology", "B-AR-01", "Browser layer: separate product origin, shared component library only, scoped cache", C, "Part 3.1 §3.1.3.2 C01/C02, ADR-006, §3.1.11", "Mapped")
a(S, "Independent deployment topology", "B-AR-02", "Identity layer: existing SSO if compatible, unique audience, independent memberships, token invalidation", C, "Part 3.1 ADR-005, ADR-033; DEC-003, DEC-019", "Mapped")
a(S, "Independent deployment topology", "B-AR-03", "API layer: independent Django runtime, serializers, permissions, scoped query, domain transactions", P, "Part 3.1 C03–C05; Part 3.2 §3.2.1.12", "Named DRF permission-class taxonomy added", "FR-ENH-B-005; ADR-109")
a(S, "Independent deployment topology", "B-AR-04", "Domain layer limited to market, marketing, account, bidding, procurement, sales, renewal", C, "Part 2.1 §2.2 module catalogue", "Mapped")
a(S, "Independent deployment topology", "B-AR-05", "Persistence: independent PostgreSQL, credentials, migrations, storage keys, vector namespace", C, "Part 3.1 C12/C14; Part 3.3", "Mapped")
a(S, "Independent deployment topology", "B-AR-06", "Workers: separate broker/queue namespace, schedule, outbox, budget reservation, DLQ", C, "Part 3.1 C06–C09, ADR-003, ADR-021; Part 3.2 §3.2.7.4", "Mapped")
a(S, "Independent deployment topology", "B-AR-07", "External adapters: account-bound secrets, validated callbacks, independent quotas, no cross-product dispatch", C, "Part 3.1 ADR-009, ADR-014; Part 3.2 §3.2.4", "Mapped")
a(S, "Independent deployment topology", "B-AR-08", "Admin layer: product policy, tenant support, billing, audit, emergency stops", C, "Part 2.1 A001–A113; Part 2.3 §2.26", "Mapped")
a(S, "Independent deployment topology", "B-AR-09", "Operations: independent deployment, health, logs, backup restore, incident; no shared confidential logs", C, "Part 4.3 §4.39–§4.47", "Mapped")
for i, (m, ini, gro, st, loc, act, new) in enumerate([
    ("Owned startups / external tenants", "25 / 10", "50+ / 100", X, "DEC-031 (Year 2: 100 workspaces / 30 tenants); Part 3.1 §3.1.12.1", "Validation profile added; CONFLICT logged", "CONFLICT-321; LT-ENH-B-01; NFR-ENH-B-01"),
    ("Concurrent staff sessions", "50", "250", N, "Part 3.1 §3.1.12 uses 60/200 internal users, a = 0.5", "Capacity formula and load profile added", "NFR-ENH-B-02; LT-ENH-B-01"),
    ("Scoped opportunities", "100,000", "1,000,000", N, "Part 3.3 volume model (no opportunity-count design point)", "Data-volume profile added", "NFR-ENH-B-03; LT-ENH-B-02"),
    ("Concurrent jobs / scheduled actions per day", "50 / 10,000", "250 / 100,000", P, "Part 3.1 §3.1.12.2 (≈ 20,000 tasks/day Y1); ADR-021 20 runs/startup", "Concurrency profile added", "NFR-ENH-B-04; LT-ENH-B-03"),
    ("Dashboard query p95", "≤ 2 s", "≤ 2.5 s", N, "NFR-039 (API p95 ≤ 500 ms) covers single calls only", "Composite dashboard NFR added", "NFR-ENH-B-05; GAP-333"),
    ("Async/webhook acknowledgement p95", "≤ 2 s", "≤ 2 s", C, "SLO-08, NFR-051/055; ARP-09", "Mapped"," "),
    ("Projection refresh", "≤ 60 s", "≤ 60 s", C, "NFR-008, SLO-09", "Mapped", ""),
    ("Critical data RPO / RTO", "≤ 15 min / ≤ 4 h", "≤ 15 min / ≤ 2 h", X, "DEC-018 (RTO ≤ 4 h), CONFLICT-101/112", "Growth RTO path defined; CONFLICT logged", "CONFLICT-322; ADR-102; NFR-ENH-B-06"),
    ("Regenerable research RPO / RTO", "≤ 24 h / ≤ 8 h", "≤ 24 h / ≤ 8 h", N, "Part 3.1 §3.1.13 (single class)", "Recovery classes RC-1..RC-3 added", "ADR-102; GAP-321; RECOMMENDATION-321"),
], 1):
    a(S, "Capacity, reliability and recovery acceptance", "B-CAP-%02d" % i, "%s: initial %s, growth %s" % (m, ini, gro), st, loc, act, new.strip())
a(S, "Capacity, reliability and recovery acceptance", "B-CAP-10", "Targets are proposed test targets, not client SLA; shared resources enforce fairness", C, "Part 4.2 NFR notes; ADR-021 fair scheduling; DEC-044", "Mapped")
for i, s in enumerate([
    "Activation sequence: template → offering → users → policies/knowledge/sources → entitlement → dry run → approver activation",
    "Configuration immutable once approved; clone to change",
    "Domain verification and TLS precede custom routing",
    "Trial entitlement expiry blocks dispatch, not authorized export",
    "Offboarding revokes tokens/sender credentials, stops jobs, exports, applies retention",
], 1):
    a(S, "Configuration and activation", "B-CFG-%02d" % i, s, C, ["Part 2.2 §2.22.4, WF-01", "ARP-07; BRL-AUT-03; A112", "FR-A107; Part 3.1 §3.1.6.1 DNS", "Part 2.3 BRL-SVC; §2.27.18", "Part 2.2 WF-14"][i - 1], "Mapped")

# ---------------- Technical component rows (04 and 09) ----------------
S = "04/09"
comp = [
    ("React website and portal: TypeScript, React Router, TanStack Query, no vendor secrets; poll/SSE", C, "Part 3.1 §3.1.8 (React Router 7, TanStack Query 5), ADR-034", "Mapped", ""),
    ("Separate React Admin: separate build/domain, SSO/MFA, Django admin break-glass only", C, "ADR-006, ADR-005; Part 4.1", "Mapped", ""),
    ("Django apps named accounts, catalog, intelligence, crm, engagement, campaigns, deals, governance, reporting", X, "Part 3.1 §3.1.4 (core.*, governance, intelligence, crm, engagement, marketing, commerce, automation, ai, web, saas)", "Name mapping table; blueprint names govern", "CONFLICT-329"),
    ("Worker & scheduler: Celery + Redis broker; Beat; queues research, AI, messaging, billing; PG outbox", X, "ADR-003, ADR-021, ADR-028 (Valkey; 12 named queues)", "Valkey governs; queue mapping", "CONFLICT-320; ADR-101"),
    ("Data and RAG: PostgreSQL source of truth, pgvector optional, S3 encrypted, product-only retrieval, citations", C, "ADR-007 (pgvector adopted, errata 26), Part 7.2", "Mapped", ""),
    ("Channel adapters: official APIs, webhook verify, unique external event ID, canonical event model", P, "Part 3.2 §3.2.6; ProviderEvent", "Canonical inbound event field mapping added", "FR-ENH-B-007"),
    ("AI runtime: LLM gateway, JSON schema, token ceilings, model/version logging; policy outside model", C, "ADR-008; Part 7.3", "Mapped", ""),
    ("Deployment: ALB/ECS Fargate, RDS, ElastiCache Redis, S3/CloudFront, Secrets Manager, CloudWatch/WAF", X, "ADR-013 (ECS on EC2, no ALB at pilot), C13 Valkey, DEC-081 WAF", "ADR-100 reconciles", "CONFLICT-320; ADR-100"),
    ("State machine: account discovered → verified → … → won/lost → onboarding → renewal; closure only on evidence", P, "Part 2.3 §2.27.1–2.27.8 (separate machines)", "Composite commercial journey projection added", "FR-ENH-B-011; ADR-106"),
    ("Security boundary: marketing DB separate from clinical app; event allowlist; no medical results or pixels", P, "BR-M43, DEC-009; Part 3.3 (no clinical tables)", "Product-event ingress allowlist added", "FR-ENH-B-010; ADR-105"),
    ("Delivery engineering: monorepo apps/growth-ui, apps/admin-ui, server/*, infra, tests; drf-spectacular; pytest; Playwright", X, "ADR-006, ADR-060 (apps/website, apps/admin, packages/*)", "Path mapping; ADR-060 governs", "CONFLICT-329"),
    ("Admin auto-driven: every mutation emits domain event; projections; versioned audited admin changes", C, "Part 3.2 §3.2.3; ADR-034; Part 3.3 projections", "Mapped", ""),
]
for i, (s, st, loc, act, new) in enumerate(comp, 1):
    a(S, "Technical design contracts (component rows)", "B-TC-%02d" % i, s, st, loc, act, new)

# ---------------- Document 04 specific ----------------
S = "04"
wp = ["Tenant/product boundaries and reuse", "Startup configuration and source policies", "Discovery and qualification",
      "Engagement and follow-up", "Route-specific conversion", "Independent operations", "Production verification"]
for i, w in enumerate(wp, 1):
    a(S, "Dependency-ordered implementation and operations", "B-04-WP%d" % i, "Work package %d: %s with completion evidence" % (i, w), C,
      "Part 8.1 §8.1.2 waves W0–W6, §8.1.2.5 gates", "Mapped to waves (§3.4.5.7)")
a(S, "Dependency-ordered implementation and operations", "B-04-001", "Vertical slice: migration → service → API → screen → worker/outbox → stub → evidence → review", P, "Part 5 DoD; Part 8.1 §8.1.4.1", "Slice checklist added", "FR-ENH-B-025")
a(S, "Dependency-ordered implementation and operations", "B-04-002", "PR requires schema, scoped permission, idempotency, tests, observability", C, "Part 4.3 §4.32.2, §4.33.2 PL gates", "Mapped")
a(S, "Dependency-ordered implementation and operations", "B-04-003", "Expand/backfill/validate/switch/contract migrations; verify counts; no blind production migration", C, "Part 4.3 §4.37.2", "Mapped")
a(S, "Commercial module delivery backlog", "B-04-004", "66-module backlog: name, dependency and acceptance (66 rows parsed)", C, "Part 1 BR-M01…M66 (66/66 names; 66/66 dependency sets; 52 exact + 13 spelling/DEC-suffix acceptance matches)", "Programmatic reconciliation §3.4.4.1")
a(S, "Commercial module delivery backlog", "B-04-005", "M01 acceptance worded as existing capability with predecessors H02,H03", P, "BR-M01 acceptance 'Cross-role access denied; session revoked'; DEC-003", "Reuse validation acceptance appended", "TC-ENH-B-021")
a(S, "Commercial module delivery backlog", "B-04-006", "Backlog dependency DAG (acyclic; 27-level longest chain)", P, "Part 8.1 §8.1.7 critical path (story level)", "DAG analysis published", "§3.4.4.1")
rb = [("Predeployment", C, "Part 4.3 §4.48 readiness checklist; §4.37"), ("Release", C, "Part 4.3 §4.37.1, §4.38"),
      ("Daily operations", N, "No daily checklist runbook"), ("Provider outage", C, "RB-001"), ("Budget cap", C, "RB-005"),
      ("Data incident", P, "RB-008, RB-013 (no containment-to-restart runbook)"), ("Recovery", C, "RB-007; §4.47"),
      ("Client offboard", P, "WF-14 (process), no operator runbook")]
for i, (r, st, loc) in enumerate(rb, 1):
    new = {"Daily operations": "RB-ENH-B-01; GAP-327", "Data incident": "RB-ENH-B-03", "Client offboard": "RB-ENH-B-02"}.get(r, "")
    a(S, "Production runbook", "B-04-RB%d" % i, "Runbook: %s" % r, st, loc, "Runbook added" if new else "Mapped", new)
a(S, "Consolidated effort and operating cost assumptions", "B-04-007", "Effort 287–483 PD by work package (194–323, 35–60, 30–52, 28–48)", C, "BRD §6; Part 1; Part 8.1 §8.1.6.4", "Mapped")
a(S, "Consolidated effort and operating cost assumptions", "B-04-008", "Resource cost ₹1–1.5 L/resource-month, 22 days; ₹13.05–32.93 L", C, "Part 8.1 §8.1.6.4", "Mapped")
for i, (it, v) in enumerate([("AWS shared hosting", "5,000"), ("Production AI inference", "3,000"), ("Public search API", "1,500"),
                              ("Extraction compute/overage", "1,000"), ("Email delivery", "500"), ("WhatsApp Business", "2,000"),
                              ("Monitoring/security/CI", "500"), ("Apollo paid enrichment reserve", "9,000"),
                              ("Claude Code developer seats", "3,600"), ("Optional integration reserve", "1,000"),
                              ("Contingency rate", "15%")], 1):
    a(S, "Consolidated effort and operating cost assumptions", "B-04-C%02d" % i, "Pilot cost line %s: %s" % (it, v), C,
      "DEC-020 B01–B11; Part 4.3 §4.46.4; Part 8.2 (B01 revised ₹5,000–7,000)", "Recomputed §3.4.4.3")
a(S, "Consolidated effort and operating cost assumptions", "B-04-009", "₹14,500 base → ₹16,675 with 15%; ₹31,165 with Apollo + seats", C, "Part 0A; errata 68 (Part 8 revised band ₹19,665–22,885)", "Recomputed; Part 8 revision governs")
a(S, "Consolidated effort and operating cost assumptions", "B-04-010", "SaaS: plans, metered base + overage, margin = fee − attributable cost, append-only credits", C, "Part 2.3 BRL-SVC; Part 4.3 §4.46.5; OPT-20-01", "Mapped")
a(S, "Website and confidential Admin operating contract", "B-04-011", "Estimate update: independently estimate templates, portal adapters, CMS, cache/CDN, accessibility; no multiplication by startup count", C, "Part 8.1 §8.1.6 (story-level estimates)", "Mapped")
a(S, "Four independent frontend deployment boundaries", "B-04-012", "Separate origin/pipeline/OAuth clients/CSP/rollback; shared library imports no privileged modules", C, "ADR-006, ADR-060; PL-13; NFR-001", "Mapped")
a(S, "Four independent frontend deployment boundaries", "B-04-013", "Build sequence: identity/host routing → projection/CMS → intake → portal grants → workflow linkage → isolation tests", C, "Part 8.1 EP-19 sequencing", "Mapped")
a(S, "Four independent frontend deployment boundaries", "B-04-014", "Retained baseline 302 ops / 149 entities / 624 tests + 19 ops / 6 entities / 175 tests candidates", C, "Part 3.2 §3.2.2.5 (555 ops superset); Part 3.3 (199 entities); errata 24/42", "Mapped")
a(S, "Replacement-first engineering delivery", "B-04-015", "Benchmark alternative providers before paid activation; no independent paid automation engine", P, "CN-05; DEC-020 flags OFF; ADR-017", "Provider candidate register and benchmark gate added", "FR-ENH-B-023; RECOMMENDATION-327")
a(S, "Replacement-first engineering delivery", "B-04-016", "Cost reserves are conditional ceilings; rebaseline after measured workloads; no double counting", C, "Part 4.3 §4.46; Part 8.2", "Mapped")
a(S, "Engineering delivery gates", "B-04-017", "Gate sequence incl. restore drill, security and load acceptance, handover; open critical defects block activation", C, "Part 8.1 §8.1.3.4; Part 4.3 §4.48", "Mapped")
wb = ["Identity compatibility (Security/architect)", "Domain foundation (Database lead)", "Vertical slices (Engineering lead)",
      "External integration: mock adapter first, benchmark native alternative (Integration lead)",
      "Quality and deployment effort not hidden (CTO/QA)", "Resource allocation: named owners; estimate each task once (PM)"]
for i, w in enumerate(wb, 1):
    a(S, "Dependency-based work breakdown and cost discipline", "B-04-WB%d" % i, w, C if i not in (4, 6) else P,
      "Part 8.1 §8.1.5.5 RACI; §8.1.6" if i not in (4, 6) else ("Part 3.2 IP-08" if i == 4 else "Part 8.1 §8.1.5.1"),
      "Mapped" if i not in (4, 6) else "Added", "" if i not in (4, 6) else ("FR-ENH-B-023" if i == 4 else "FR-ENH-B-025"))
a(S, "Dependency-based work breakdown and cost discipline", "B-04-018", "Cost model: labour = Σ task PD × rate; operating = infra + metered + support + recovery", C, "Part 8.1 §8.1.6.4; Part 4.3 §4.46.3", "Mapped")
for i, (s_, g) in enumerate([("Identity and tenant setup", "Cross-product/tenant deny tests"), ("Catalog and contracts", "No unreviewed production contract"),
                             ("Website / portal", "No private DTO"), ("Admin / workflows", "No unauthorized or duplicate dispatch"),
                             ("Closure and reporting", "Correct outcome accounting"), ("Delivery", "Go-live approval")], 1):
    a(S, "Dependency-based work breakdown and cost discipline", "B-04-DS%d" % i, "Delivery slice gate: %s → %s" % (s_, g), C,
      "Part 8.1 §8.1.2.5 wave gates; §8.1.3.4", "Mapped")
a(S, "Task-level estimates and executable predecessor plan", "B-04-019", "Base allocation 385 PD over 149 work items; first-owned shared work counted once", X, "Part 8.1 §8.1.6.4 (central 416 pd, 602 SP)", "Reconciled; Part 8 governs", "CONFLICT-328; FR-ENH-B-025")
a(S, "Task-level estimates and executable predecessor plan", "B-04-020", "Discipline split: React/UX 90.68, Django/API 111.55, PostgreSQL 52.85, AI/integration 36.23, QA 65.64, DevOps/security 28.05", N, "Part 8.1 (no discipline split)", "Discipline reconciliation and capacity check added", "FR-ENH-B-025; RECOMMENDATION-328")
a(S, "Task-level estimates and executable predecessor plan", "B-04-021", "Dependency-only longest path 113.5 days (unlimited resources)", X, "Part 8.1 §8.1.7.1 critical path; CONFLICT-142", "Part 8 governs", "CONFLICT-328")
a(S, "Task-level estimates and executable predecessor plan", "B-04-022", "Foundations order: identity reuse → scoped data/migration → API contracts; provider benchmark precedes paid integration", C, "Part 8.1 §8.1.7", "Mapped")
for i, (oid, t) in enumerate([("OPT-03-01", "Native vs paid plugins"), ("OPT-03-02", "Model and token costs"), ("OPT-03-03", "Research and contact costs"),
                              ("OPT-03-04", "Cloud and worker sizing"), ("OPT-03-05", "Storage and retention costs"),
                              ("OPT-03-06", "Communication and subscription costs"), ("OPT-03-07", "Budget reservation"),
                              ("OPT-03-08", "Usage anomaly control 70/90%"), ("OPT-06-01", "Startup templates and tenants"),
                              ("OPT-06-02", "Concurrent users and jobs"), ("OPT-06-03", "Data and scheduling volume"),
                              ("OPT-06-04", "Regional expansion"), ("OPT-06-05", "Noisy neighbour"),
                              ("OPT-07-01", "Modular monolith"), ("OPT-07-02", "Four frontends and two backends"),
                              ("OPT-07-03", "Domain and adapter boundaries"), ("OPT-07-04", "Configuration-driven design"),
                              ("OPT-07-05", "Complexity and reuse review"), ("OPT-13-01", "Code health"),
                              ("OPT-14-01", "Shared code libraries"), ("OPT-14-02", "Template reuse"), ("OPT-14-03", "Component contracts"),
                              ("OPT-16-01", "Standard setup"), ("OPT-16-02", "Vertical slices and estimates"),
                              ("OPT-16-03", "AI-assisted development"), ("OPT-20-01", "Unit economics"),
                              ("OPT-20-02", "Entitlements and usage"), ("OPT-20-03", "Support and renewal"),
                              ("OPT-20-04", "Client scalability and portability")], 1):
    pass  # OPT controls are registered once below (dedupe across docs)
proc = [("Task and operating cost estimates", P, "Part 8.1 §8.1.6", "FR-ENH-B-025"),
        ("Capacity and region decisions", P, "DEC-040; ADR-019", "LT-ENH-B-01..04; CONFLICT-325"),
        ("Independent products and frontends", C, "ADR-006, ADR-033; NFR-031", ""),
        ("Architecture decision rationale", C, "Part 3.1 §3.1.9 ADR template (alternatives, consequences, review trigger)", ""),
        ("Repository and modular boundaries", C, "ARP-01; import-linter; ADR-060", ""),
        ("Existing identity reuse", C, "ADR-005; US-0101 identity spike", ""),
        ("Development dependencies (DAG, low ≤ base ≤ high)", P, "Part 8.1 (story dependencies)", "FR-ENH-B-025; TC-ENH-B-030"),
        ("Resource and deployment approval", C, "Part 8.1 §8.1.3.4; Part 8.2 go-live", ""),
        ("Approval review effort 32.55 / 62.85 / 123.70 PD", N, "Not in Part 8", "FR-ENH-B-024; GAP-330")]
for i, (t, st, loc, new) in enumerate(proc, 1):
    a(S, "Implementation acceptance and final decision controls", "B-04-AP%d" % i, "Acceptance procedure: %s" % t, st, loc,
      "Added" if new and st != C else "Mapped", new)
a(S, "Architecture and delivery (expansion)", "B-04-023", "UX-TASK DAG for 9 expansion interfaces: 62/114/196 PD; critical path 36/64/110 PD", N, "Part 8.1 (stories US-20xx/US-18xx for W31–W34, A109–A113)", "Reconciliation added", "FR-ENH-B-026")

# ---------------- Document 05 specific ----------------
S = "05"
a(S, "Workflow register — end-to-end execution", "B-05-001", "14 workflows with trigger/processing and stop (duplicated twice in 05)", C, "Part 2.2 WF-01…WF-14", CC)
a(S, "Workflow register — end-to-end execution", "B-05-002", "Engine: validated event, scope, immutable revision, eligibility, reservation, outbox, worker, reconciliation, projection", C, "Part 2.2 §2.6; E-1…E-9", CC)
ch = [("Email: verified domain, SPF/DKIM/DMARC, bounce/complaint suppression, unsubscribe, rate cap, delivery/reply events", C, "Part 3.2 AD-01; Part 2.3 BRL-ELG", "", "Mapped"),
      ("WhatsApp: official API, permitted recipient, template/category, opt-out immediate", C, "ADR-039; BRL-ELG; AU-008", "", "Mapped"),
      ("Web/portal: approved information, identity/consent, scoped enquiry, actual confirmation", C, "WF-04; CA-PORTAL", "", "Mapped"),
      ("Calendar/events: availability, time zone, invitation status, no recording without permission", P, "DEC-024 free/busy only; GAP-143", "Recording prohibition rule and notes-only path added", "FR-ENH-B-015; GAP-335"),
      ("Referrals: consent and context; no automatic sharing of private contacts", C, "BR-M42; BRL-MKT", "", "Mapped"),
      ("Social sources: approved publication via official API; claims approval", C, "ADR-040; BRL-MKT", "", "Mapped")]
for i, (s_, st, loc, act, new) in enumerate(ch, 1):
    a(S, "Channel and communication policies", "B-05-CH%d" % i, s_, st, loc, act or "Mapped", new)
a(S, "Channel and communication policies", "B-05-003", "Outbound includes startup identity, purpose, evidence; reserve budget and recheck suppression before send", C, "E-2, E-3; Part 3.1 §3.1.7.1", "Mapped")
a(S, "Channel and communication policies", "B-05-004", "Reply classes: interest, decline, objection, unsubscribe, bounce, out-of-office, meeting, escalation", P, "AG-013 classes (positive, question, objection, OOO, complaint, urgent/clinical, wrong person, other); AU-008, AU-024", "Taxonomy alignment added", "FR-ENH-B-014; GAP-326")
a(S, "Channel and communication policies", "B-05-005", "Never infer delivery from enqueue/provider acceptance; reconcile uncertain sends; caps/quiet hours not bypassable", C, "§2.27.9 outbound message; BRL-ELG-08; IP-04", "Mapped")
ib = ["Content and SEO", "Social publishing", "Landing pages", "Website assistant", "Campaign audiences", "Paid ads", "Webinars and demos", "Attribution (first/last touch, window, unknown bucket)"]
for i, s_ in enumerate(ib, 1):
    a(S, "Inbound marketing acquisition", "B-05-IB%d" % i, "Inbound capability: %s" % s_, C, "Part 2.1 M34–M42; WF-04/05; Part 3.2 marketing ops", "Mapped")
mods = ["WhatsApp Business", "Website conversational assistant", "Unified omnichannel routing", "Social listening", "Content studio",
        "Social publishing", "SEO and search visibility", "Landing pages and attribution", "Campaign management", "Paid ads integration",
        "Webinars and demonstrations", "Referral and partner lead capture", "Proposal builder", "Quote and pricing engine",
        "Negotiation and objection handling", "Contract and MoU workflow", "Payment and closure", "Onboarding and handoff",
        "Partner deployment pipeline", "Retention and renewal", "Lost deal and feedback", "Revenue and attribution"]
for i, m in enumerate(mods, 1):
    a(S, "Module cards (inbound and conversion)", "B-05-MC%02d" % i, "Module card: %s (objective, dependency, acceptance, owner, scope, UX, backend, admin, entities, API, trigger, tools, cost)" % m,
      C, "Part 1 BR-M; Part 2.1 §2.2; Part 3.2 catalogue (17/17 API paths found); Part 3.3 (27/27 entities)", "Programmatic reconciliation §3.4.4.2")
a(S, "Module cards (inbound and conversion)", "B-05-006", "Integration candidates PandaDoc, Crossbeam Skills, Socialinsider, PostHog (licence/quota unverified)", P, "ADR-038 manual e-sign first; ADR-011 first-party analytics; not named", "Candidate register added", "FR-ENH-B-023; GAP-331")
a(S, "Module cards (inbound and conversion)", "B-05-007", "LLM gateway rate: Haiku 5.5 $0.10/$0.50, Sonnet 5.5 $2/$10 per M tokens", C, "Part 7.3 §7.3.1 (verify at implementation, as of 27 Nov 2026)", "Mapped; verify flag retained")
a(S, "Module cards (inbound and conversion)", "B-05-008", "Budget IDs B01/B02/B10 and C03 shared; no duplicate allocation", C, "DEC-020; Part 4.3 §4.46.4", "Mapped")
for i, b in enumerate(["AppNAI", "MedMaarg", "EduVerse", "OrganicSpec"], 1):
    a(S, "Business-specific acquisition and commercial conversion", "B-05-BS%d" % i, "%s operating sequence" % b, C, "Part 2.2 WF-08, WF-10, §2.21.1, §2.21.2", CC)
a(S, "Business-specific acquisition and commercial conversion", "B-05-009", "Source scoring 25/25/20/15/15; thresholds ≥75, 50–74, <50; score not send authority", C, "DEC-011; BRL-SCR; AU-017", CC)
a(S, "Business-specific acquisition and commercial conversion", "B-05-010", "Conversion KPIs list (precision, verified contacts, replies, meetings, win rate, CAC, awards, receipts, payables, renewal, margin)", C, "Part 1 KPI-01…31", "Mapped")
a(S, "Business-specific acquisition and commercial conversion", "B-05-011", "Transition evidence table (bid, proposal/quote, order, closure, renewal) and quote/order rules", C, "Part 2.3 §2.27.4–2.27.8; BRL-QTE/ORD/FIN", "Mapped")
a(S, "Website-to-Admin workflow", "B-05-012", "Verified host → validation → consent → dedupe/outbox → routing → queue → response → status projection; safe retry reference; portal upload quarantine", C, "Part 2.2 WF-04; §2.22.3; ADR-024", "Mapped")
a(S, "Provider-neutral automation and recovery", "B-05-013", "Workflow execution order (11 steps); dry run uses fake adapters", C, "Part 2.2 §2.6.1; IP-08", "Mapped")
a(S, "Provider-neutral automation and recovery", "B-05-014", "Operational regression: 10 scenarios × business workflows with observable result and recovery procedure", P, "Part 6 TCs per epic (not as one matrix)", "Workflow regression matrix added", "FR-ENH-B-016; TC-ENH-B-001…010; RECOMMENDATION-325")
a(S, "Provider-neutral automation and recovery", "B-05-015", "Never treat procurement payable as revenue", C, "BRL-FIN; DEC-054", "Mapped")
a(S, "Workflow quality gates", "B-05-016", "Before activation validate graph, trigger, scope, approval hash, eligibility, budget, retries, termination", P, "BRL-AUT-01…09; A033/A113", "Activation gate checklist WQG-01…12 added", "FR-ENH-B-013")
a(S, "Workflow quality gates", "B-05-017", "Per-vertical gates (AppNAI, MedMaarg, EduVerse, OrganicSpec, campaigns)", C, "Part 2.2 WF-05/08/10, §2.21", "Mapped")
a(S, "Implementation, verification and delivery controls", "B-05-018", "Five workflow control rows (trigger, preconditions, durable outcome, stop/recovery)", C, "Part 2.2 WF-02/04–06/09–12", "Mapped (§3.4.5.4 table)")
a(S, "Implementation, verification and delivery controls", "B-05-019", "Persisted run fields and worker lease/reload/reserve/invoke-outside-lock pattern", C, "Part 3.3 WorkflowRun/StepRun; ARP-03; §3.2.7", "Mapped")
a(S, "Proposed workflow fixture", "B-05-020", "Fixture: trigger, steps, max_attempts 3, stop_on [...], paid_fallback false, uncertain_result reconcile_before_retry", P, "Part 3.3 max_attempts; BRL-AUT-06 ≤ 3 retries", "Execution-policy block schema added", "FR-ENH-B-012; ADR-107; GAP-325")
for i, (r, t) in enumerate([("Planned", "pin scope, objective, versions, cost cap; simulate first"), ("Eligible", "check at enqueue and lease"),
                            ("Dispatch", "outbox + reservation same transaction; scoped key"), ("Provider timeout", "uncertain; reconcile"),
                            ("Reply/opt-out/expiry", "stop, cancel, release reservation"), ("Verified closure", "evidence + audit; never from AI draft")], 1):
    a(S, "Workflow execution and recovery decision table", "B-05-DT%d" % i, "Decision: %s → %s" % (r, t), C, "E-1…E-9; §2.27.14; IP-02/IP-04", "Mapped")
for i, (f, loc) in enumerate([("Quotation 2 × 150.00, 10% → 270.00", "Part 6.2 TC-13-036…049; FRD"), ("Bid expiry 2030-06-01 09:00 UTC", "DEC-068; Part 6.2b"),
                              ("Order 2 kg, duplicate event, over-delivery", "BRL-ORD; AU-038"), ("EduVerse vs AppNAI routing", "DEC-052; WF-04")], 1):
    a(S, "Business regression fixtures", "B-05-RF%d" % i, "Fixture: %s" % f, C, loc, "Mapped")
for i, (t, st, loc, new) in enumerate([
    ("Async acknowledgement p95 ≤ 2 s measured separately from completion", C, "SLO-08; LT-05", ""),
    ("Workflow trigger and state with persisted event ID and policy revision", C, "Part 6 EP-18 TCs", ""),
    ("Follow-up stop conditions (reply, opt-out, pause, policy revision before dispatch)", C, "AU-008, AU-022; BRL-SEQ", ""),
    ("Autonomy and approval at all autonomy levels", C, "DEC-064; NFR-010", ""),
    ("Simulation side effects: zero network/outbox/charge/financial write", C, "E-6; NFR-038", ""),
    ("Workflow failure orchestration: timeout before/after unknown outcome, DLQ", C, "§3.2.7; AU-026", ""),
    ("Inbound and outbound journeys: website enquiry creates scoped lead/investor record", X, "WF-04 (lead only; investor out of scope)", "CONFLICT-326"),
    ("Objection resolution: approved answer or specialist escalation", C, "AG-021; BRL-MKT claims", ""),
    ("Shared workflow and adapter code without shared credentials", P, "ADR-009; ARP-14", "TC-ENH-B-022"),
], 1):
    a(S, "Implementation acceptance and verification", "B-05-AP%d" % i, "Acceptance procedure: %s" % t, st, loc, "Added" if new else "Mapped", new)
a(S, "Current multi-startup scope", "B-05-021", "Workflow design: versioned allowlisted graph, trigger registration, branches, run state, waits, pause, cancel", C, "ADR-027; A109–A113; node types (Part 2.1)", "Mapped")

# ---------------- Document 09 specific ----------------
S = "09"
for i, v in enumerate(["Overview", "Discovery", "Outreach & Marketing", "Follow-ups", "Objections", "Closure", "Automation"], 1):
    a(S, "Unified Command Centre — seven primary views", "B-09-V%d" % i, "View: %s" % v, C, "Part 2.5 IA; Part 2.1 A-screens", CC)
a(S, "Unified Command Centre — seven primary views", "B-09-001", "Persistent action centre, Copilot, saved views, budget, automation status, stop control; scope retained", C, "Part 2.5; Part 2.4", CC)
a(S, "High-level interface topology", "B-09-002", "Internet → CDN/WAF → public allowlist; portal no-store; Admin SSO/MFA; private workers and hooks; separate public/private object storage", C, "Part 3.1 §3.1.3, C15; Part 3.2 §3.2.1.1", "Mapped")
a(S, "Provider-independent architecture and resilience", "B-09-003", "Reusable adapters/gateway/workers; runtime resources per product; no hosted automation subscription", C, "ADR-009, ADR-027; CN-05", "Mapped")
a(S, "Provider-independent architecture and resilience", "B-09-004", "Availability acceptance: load, fairness, failure isolation, secret redaction, restore, idempotent replay", C, "Part 6.1 LT-01…12; §4.47", "Mapped")
a(S, "Deployment and architecture acceptance", "B-09-005", "Two independently deployed React frontends per product; private backend/DB/queue/storage", C, "ADR-006; §3.1.6.1", "Mapped")
pb = [("Independent products: separate Website/Admin, runtime, DB, storage, vector, queues, secrets, logs", C, "CN-02; ADR-033; §3.1.6.1 accounts", "", ""),
      ("Ingress: public DNS/CDN/WAF; Admin staff audience; private workers; authenticated callbacks", C, "C15; DEC-081 WAF", "", ""),
      ("Data durability: critical RPO ≤ 15 min, RTO ≤ 4 h / ≤ 2 h growth; regenerable 24 h / 8 h", X, "DEC-018; CONFLICT-101", "ADR-102", "CONFLICT-322; ADR-102"),
      ("Scaling: 25+10 → 50+ / 100; 50/250 staff; 100k/1M opportunities; 50/250 jobs; queue partitioning, per-tenant quotas", P, "§3.1.12; ADR-021", "Growth profiles", "LT-ENH-B-01..04"),
      ("Failure boundaries: cache keys scope product/tenant/startup/audience; circuit breakers", C, "§3.1.11; §3.2.7.3", "", ""),
      ("Regional strategy: residency per contract/regulation; no cross-region replication before approval", X, "ADR-019 cross-region backup copies from day one; DEC-040", "Resolution", "CONFLICT-325")]
for i, (s_, st, loc, act, new) in enumerate(pb, 1):
    a(S, "Production boundary and deployment decisions", "B-09-PB%d" % i, s_, st, loc, act or "Mapped", new)
a(S, "Production boundary and deployment decisions", "B-09-006", "Suggested AWS design: separate account/IAM boundary per product+env, LB/API gateway, containers, PITR PostgreSQL, Valkey, versioned storage, secrets, budgets", C, "§3.1.6.1 (3 accounts), ADR-013, ADR-014", "Mapped")
for i, (s_, loc) in enumerate([("Network: separate account or strict IAM/network boundary; private subnets", "§3.1.6.1"),
                               ("Frontend: two origins; public CDN only published snapshots", "ADR-010"),
                               ("Backend: Django behind ingress; workers no inbound; PG outbox; independent Valkey", "C03–C13"),
                               ("Data: encrypted PostgreSQL, storage, vector; independent keys, backups, restore rehearsals", "ADR-014; §4.47"),
                               ("Recovery: RPO ≤ 15 min; RTO ≤ 4 h initial, ≤ 2 h growth; measured, not SLA", "§3.1.13; ADR-102"),
                               ("Operational approval: region, VPC, TLS/DNS, capacity, identity, cost before IaC apply", "§4.34; Part 8.2 go-live")], 1):
    a(S, "Independent AWS deployment boundaries and availability", "B-09-AD%d" % i, s_, C if i != 5 else P, loc, "Mapped" if i != 5 else "Growth RTO path", "" if i != 5 else "ADR-102")
for i, (t, st, loc, new) in enumerate([
    ("Product and audience isolation: investor/customer tokens on opposite product and Admin API", P, "NFR-031; ADR-033 (no executable cross-product token test)", "TC-ENH-B-020; CONFLICT-326"),
    ("Growth workload matrix 25/50+ startups, 10/100 tenants, concurrency targets", N, "LT-11 (10× pilot only)", "LT-ENH-B-01..04"),
    ("Capacity and region decisions (residency, saturation)", P, "DEC-040; LT-08", "LT-ENH-B-04"),
    ("Independent products and frontends inventory", C, "ADR-006; §3.1.6.1", ""),
    ("Shared library boundaries: wrong product config in synthetic deployment; no tenant state in library", N, "ADR-060 (no runtime test)", "TC-ENH-B-022"),
    ("Architecture decision rationale", C, "§3.1.9", ""),
    ("Infrastructure as code completeness in sandbox; no production apply without approval", C, "§4.34 (OpenTofu plan/apply gates)", ""),
], 1):
    a(S, "Implementation acceptance and verification", "B-09-AP%d" % i, "Acceptance procedure: %s" % t, st, loc, "Added" if new and st != C else "Mapped", new)
a(S, "Current scope: high-level design", "B-09-007", "Applicant intake separate from provisioning; immutable sanitized snapshots; handoff by authenticated API, never browser storage", C, "§2.22.4; Part 3.3 applicant draft (FRD)", CC)

# ---------------- Document 10 specific ----------------
S = "10"
for i, f in enumerate(["Scope", "Geography", "Evidence", "Engagement", "Operations", "Marketing", "Commercial", "AppNAI", "MedMaarg", "EduVerse", "OrganicSpec"], 1):
    a(S, "Global filter hierarchy and contextual filters", "B-10-F%02d" % i, "Filter family: %s" % f, C, "Part 2.4 §2.3x filters; Part 2.5 global filter bar", CC)
a(S, "Global filter hierarchy and contextual filters", "B-10-001", "Filter semantics: OR within, AND across, unknown ≠ zero, reset child on scope change, cancel stale, cursor + id, as_of", C, "Part 2.4; Part 3.2 §3.2.1.6; NFR-027", CC)
ai = [("Knowledge", "AG-001"), ("Research", "AG-003"), ("Signal", "AG-005"), ("Matching", "AU-016 + AG-007"), ("Contact", "AG-008 + AU-018"),
      ("Engagement", "AG-011"), ("Response", "AG-013"), ("Objection", "AG-021"), ("Planner", "AG-016"), ("Meeting", "GAP-143 (excluded)"),
      ("Forecast", "AU-041 (deterministic)"), ("Quality", "AG-002"), ("Cost routing", "AU-001 + AU-002"), ("Copilot", "AG-015"),
      ("Business need", "AG-006"), ("Content and SEO", "AG-018 + AU-033"), ("Proposal", "AG-020"), ("Retention", "AU-039 + AG-026")]
for i, (r, m) in enumerate(ai, 1):
    st = P if r == "Meeting" else C
    a(S, "Logical AI responsibilities and typed prompt contracts", "B-10-AI%02d" % i, "AI responsibility %s (inputs, output, envelope, evaluation)" % r, st,
      "Part 7.1/7.2 %s" % m, "Mapped (§3.4.5.5)" if st == C else "Notes-only summarization proposed", "" if st == C else "FR-ENH-B-015; GAP-335")
a(S, "Logical AI responsibilities and typed prompt contracts", "B-10-002", "Required envelope: tenant_id, startup_id, purpose, schema_revision, evidence_ids, confidence, missing_fields, policy_flags, proposed_action, requires_approval, cost_estimate", P, "Part 7.2 §7.2.7 (7 of 11 fields absent)", "Envelope v1.1 added", "FR-ENH-B-009; ADR-104; GAP-323")
a(S, "Logical AI responsibilities and typed prompt contracts", "B-10-003", "Shared prompt instruction: retrieved docs untrusted, structured JSON, unknown when unsupported, no external execution", C, "BRL-AI-03/05/07; Part 7.2 prompt strategy", "Mapped")
a(S, "Logical AI responsibilities and typed prompt contracts", "B-10-004", "Evaluation: schema, scope isolation, factual support, injection, unknown handling, policy gate, regression", C, "Part 6.4; AU-006", "Mapped")
a(S, "Logical AI responsibilities and typed prompt contracts", "B-10-005", "RAG: ACL before retrieval and after ranking, version/checksum/expiry, revoke chunks, citations; no cross-client learning", C, "ADR-041; Part 7.2; Part 3.3 vectors", "Mapped")
dc = [("REST contract: /api/v1, JSON, cursor, 400/401/403/409/429, request_id, OpenAPI", C, "Part 3.2 §3.2.1", "", ""),
      ("Canonical inbound event: event_id, provider, external_id, channel, received_at, sender_ref, thread_id, text_ref, consent_scope, schema_version; unique(provider, external_id)", P, "ProviderEvent / inbound message (Part 3.3)", "Field mapping + 3 fields", "FR-ENH-B-007"),
      ("Outbound intent: intent_id, contact_id, channel, template_version, evidence_ids, policy_version, scheduled_at, idempotency_key, status, approver, expires_at", P, "§2.27.9; Part 3.3 eng_message", "Contract mapping", "FR-ENH-B-008"),
      ("Database conventions: UUID, UTC, FKs, unique domain+location, indexes on stage/due_at/status/source-date, lawful soft delete", C, "Part 3.3 STD-S", "", ""),
      ("State transition locking: select_for_update, expected version, event/outbox same txn, unique key", C, "ARP-03; §3.2.1.8", "", ""),
      ("AI schema: need_type, organization_id, evidence_ids, confidence, explicit_or_inferred, product_id, readiness, recommended_action", P, "AG-006 (category, basis), AU-016, AG-007", "Mapping table", "FR-ENH-B-009"),
      ("Queue retry: backoff + jitter, capped, permanent → DLQ, unknown → reconcile", C, "§3.2.7.2", "", ""),
      ("Webhook security: raw-body signature, minimal payload, quick 2xx after persistence", C, "§3.2.1.13, §3.2.6", "", ""),
      ("Channel reply routing: opt-out → suppress; complaint/clinical/urgent → human; FAQ; positive → meeting; price exception → approval", C, "AG-013/AG-014; AU-008", "", ""),
      ("Closure rule: won only after verified payment/executed contract; lost with reason; stop sequences; onboarding event", C, "BRL-FIN; KPI-31", "", ""),
      ("Admin authorization: MFA, scopes, audit reason, dual approval for budget/claims/policy; no direct DB edits", C, "Part 2.3 BRL-APR; DEC-062", "", ""),
      ("Data isolation: clinical system emits only commercial event ID, SKU, timestamp, payment status, account ref", P, "BR-M43; DEC-009", "Allowlist contract", "FR-ENH-B-010"),
      ("Budget model: reserve before call, reconcile, hard stop, alert at 80%", C, "BRL-AI-08; AU-002; NT-025", "", ""),
      ("Scoring model 25/25/20/15/15 with thresholds; calibration", C, "DEC-011; AU-017", "", ""),
      ("Security testing: CSRF, CORS, HTTPS, rate limits, object permissions, rotation, SAST, restore", C, "Part 4.1; §3.2.1.12", "", ""),
      ("Performance: non-AI API p95 < 500 ms; webhook ack < 2 s; 99% job success excluding vendor outages", C, "NFR-039; SLO-08; NFR-009", "", ""),
      ("Agent decomposition: six runtime responsibilities; scoring, consent, sending, closure outside AI", X, "Part 7.1 (28 product agents + 43 automations)", "Mapping", "CONFLICT-327"),
      ("Commercial metrics: precision, cost per qualified, CAC, win rate; zero denominator unavailable", C, "Part 1 KPI definitions; Part 2.4 RP-xx", "", ""),
      ("Clinical escalation: approved nonclinical info only; medical → clinician; emergency text → urgent care", C, "AG-013 urgent/clinical; AG-017 guardrails; errata 55", "", ""),
      ("Development vs runtime: Claude Code helps author; production uses licensed APIs; smoke test without Claude Code", C, "ASSUMPTION-020; Part 7.1 delivery agents", "", "")]
for i, (s_, st, loc, act, new) in enumerate(dc, 1):
    a(S, "Detailed design contracts", "B-10-DC%02d" % i, s_, st, loc, act or "Mapped", new)
a(S, "Detailed frontend, API and publication design", "B-10-006", "Website routes /, /businesses, /business/{slug}, /page/{slug}, /enquiry, /login, /portal/*; Admin /admin/*", N, "Part 2.5 screens (no URL map)", "Route map added", "FR-ENH-B-006; GAP-332")
a(S, "Detailed frontend, API and publication design", "B-10-007", "Cache key = product + host + startup + locale + slug + revision; no-store portal/Admin; abort + clear QueryClient on scope switch", P, "§3.1.11 cache safety rules; ADR-010", "Formula stated in route map", "FR-ENH-B-006")
a(S, "Detailed frontend, API and publication design", "B-10-008", "DRF classes PublicPublishedRead, ExternalGrantPermission, StaffRolePermission, ServiceIdentityPermission", P, "§3.2.1.12 authorization order (no class names)", "Permission taxonomy added", "FR-ENH-B-005; ADR-109")
a(S, "Detailed frontend, API and publication design", "B-10-009", "Reject unknown fields; public DTO allowlist; object query scoped before lookup; CSRF, exact CORS, CSP, signed state; no token in logs", C, "§3.2.1.12", "Mapped")
a(S, "Detailed adapter execution and test harness", "B-10-010", "Adapter registry with capabilities and versioned policy; resolve only after permission/source/revision/quota", C, "ADR-009; IP-01", "Mapped")
a(S, "Detailed adapter execution and test harness", "B-10-011", "Adapter interface estimate/execute/reconcile/health; statuses accepted, retryable, permanent, uncertain, denied", P, "ADR-009 AdapterResult failure classes (no estimate/health ops, no 'denied')", "Port contract v2 added", "FR-ENH-B-004; ADR-103; GAP-322")
a(S, "Detailed adapter execution and test harness", "B-10-012", "Test layers: unit, real PostgreSQL SIT, fake adapters, sandbox contract, Playwright", C, "Part 6.1 test strategy", "Mapped")
a(S, "Detailed adapter execution and test harness", "B-10-013", "Coverage: 100% critical permission/finance/policy branches; ≥ 80% domain-service branch coverage", P, "NFR-082 line coverage ≥ 80% (≥ 90% critical modules)", "Branch-coverage rule added", "FR-ENH-B-018; GAP-328")
a(S, "Detailed design implementation contracts", "B-10-014", "Per service: typed DTO, scope, transaction boundary, outbox key, retry class, telemetry, error path", P, "Part 3.2 catalogue columns; ARP-03", "Service contract card template added", "FR-ENH-B-027")
a(S, "Canonical event envelope", "B-10-015", "Envelope: event_id, product, tenant_id, startup_id, event_type, schema_revision, actor_ref, correlation_id, idempotency_key, occurred_at, payload_ref", C, "§3.2.3.1 (CloudEvents-aligned superset; product implicit)", "Mapping table §3.4.5.2")
sl = [("HTTP request: middleware auth, scope resolution, serializer validation, scoped query; no role from request field", C, "ARP-02; §3.2.1.12"),
      ("Atomic domain write: select-for-update; domain row + audit + outbox together; provider call outside txn", C, "ARP-03; ADR-003"),
      ("Worker claim: lease with expiry, bounded attempts, idempotent; recheck before side effect", C, "C06/C07; ARP-04"),
      ("Publication pointer: exact content hash; atomic revision swap; invalidate cache; never draft via public", C, "ADR-010; §3.1.7.3"),
      ("Financial reconciliation: webhook once; verify reference, account, entity, currency, amount, state; allocation auditable", C, "IP-05; BRL-FIN"),
      ("Provider adapter: normalize success/transient/permanent/uncertain; unknown never resent", C, "§3.2.7.2"),
      ("RAG and AI: verify scoped approved evidence before ranking; validate; escalate unknown/protected", C, "ADR-041; AU-003")]
for i, (s_, st, loc) in enumerate(sl, 1):
    a(S, "Service-level execution decisions", "B-10-SL%d" % i, s_, st, loc, "Mapped")
a(S, "Atomic transaction pattern", "B-10-016", "Reference pattern: scoped select_for_update → verify revision/role/transition → reserve budget → save → audit → outbox; dispatch after commit", C, "ARP-03; Part 3.3", "Reference implementation added (§3.4.5.3)", "FR-ENH-B-027")
for i, (s_, loc) in enumerate([("Authorized command from verified server context", "ARP-02"), ("Revision lock or optimistic revision; stale → 409", "§3.2.1.8"),
                               ("Budget/outbox in one txn with unique key", "ARP-03; ADR-023"), ("Receipt: signed event, designated account, Decimal, row lock; duplicate ref one receipt", "BRL-FIN; ADR-030"),
                               ("Projection refresh ≤ 60 s; filter allowlist; read-only aggregate", "NFR-008"), ("Recovery: transient only; uncertain reconciled; permanent escalated", "§3.2.7")], 1):
    a(S, "Service execution contracts and concurrency", "B-10-TP%d" % i, s_, C, loc, "Mapped")
for i, (t, st, loc, new) in enumerate([
    ("Hierarchical budget controls: platform, tenant, startup, workflow reservations", C, "ADR-083; AU-002", ""),
    ("Workflow trigger and state", C, "EP-18 TCs", ""),
    ("Simulation side effects", C, "E-6", ""),
    ("Workflow failure orchestration", C, "§3.2.7; AU-026", ""),
    ("Idempotency: concurrent identical key; changed payload rejected", C, "ADR-023 (409 IDEMPOTENCY_KEY_REUSED)", ""),
    ("Stable transactions and outbox: interrupt before/after commit", C, "ADR-003; NFR-006", ""),
    ("Noisy neighbour: tenant A flood vs tenant B progress", C, "ADR-021; Part 6.7 noisy-neighbour TC", ""),
    ("Architecture decision rationale", C, "§3.1.9", ""),
    ("Tenant ownership constraints: foreign tenant child rejected by DB", C, "ADR-002 composite FKs; Part 3.3", ""),
    ("Financial exactness: decimal, currency, duplicate, excess, partial receipts", C, "ADR-030; BRL-FIN", ""),
    ("Typed request/response completeness for unresolved DTOs", P, "Part 3.2 DERIVED catalogue (DTOs not yet exact)", "FR-ENH-B-024"),
    ("Webhook and provider reliability: stale timestamp, duplicate, quota", C, "§3.2.6.1", ""),
    ("Deduplication and entity resolution with aliases and provenance", C, "AU-015", ""),
    ("Closure and receipt distinction: partial then complete", C, "BRL-FIN; KPI-31", ""),
    ("Outstanding approval gates: 38 exact API definitions, 0 partial, 4 DB confirmations, 138 UI semantic mappings", N, "Not tracked", "FR-ENH-B-024; GAP-330"),
], 1):
    a(S, "Implementation acceptance and verification", "B-10-AP%02d" % i, "Acceptance procedure: %s" % t, st, loc, "Added" if new else "Mapped", new)
a(S, "Current scope: detailed-level design", "B-10-017", "Transactionally reserve budget, dedupe keys, pin revision, enqueue outbox; worker rechecks; reconcile unknown", C, "ARP-03/04; E-2/E-3", "Mapped")
a(S, "Applicant draft boundary and reuse-first decision", "B-10-018", "Applicant only opaque expiring draft reference; isolated intake storage; provisioning after verified authority", C, "§2.22.4; Part 3.3 applicant draft", CC)

# ---------------- OPT controls (deduplicated across docs) ----------------
OPT = [
    ("OPT-01-01", "09", "Authentication and privileged sessions", C, "DEC-019; ADR-005; Part 4.1", "", ""),
    ("OPT-02-01", "10", "Public website assets; LCP ≤ 2.5 s, INP ≤ 200 ms, CLS ≤ 0.1", C, "NFR-042; LT-12", "", ""),
    ("OPT-03-01", "04", "Native vs paid plugins; zero unapproved paid calls; TCO", C, "CN-05; DEC-020 flags OFF", "", ""),
    ("OPT-03-02", "04", "Model and token costs; INR/task", C, "Part 7.3; ADR-008", "", ""),
    ("OPT-03-03", "04", "Research and contact costs; cost per qualified verified opportunity", C, "KPI cost per qualified; Part 7.3", "", ""),
    ("OPT-03-04", "04", "Cloud and worker sizing; cost/1000 tasks, queue age", P, "§3.1.12.3; Part 4.3 §4.46.5", "Metric added", "NFR-ENH-B-07"),
    ("OPT-03-05", "04", "Storage and retention costs; GB-month and restore test", C, "Part 3.3 lifecycle; Part 4.3", "", ""),
    ("OPT-03-06", "04", "Communication and subscription costs; cost per meaningful response", C, "Part 4.3 §4.46.5 unit economics", "", ""),
    ("OPT-03-07", "04", "Budget reservation; zero overspend under parallel reservation", C, "IP-06; AU-002", "", ""),
    ("OPT-03-08", "04", "Usage anomaly control; alert 70/90%, pause optional jobs at cap", X, "BRL-AI-08 80/100; AWS Budgets 50/80/100", "Threshold reconciliation", "CONFLICT-324; FR-ENH-B-022"),
    ("OPT-04-01", "05/10", "Daily planning and discovery; missed runs recover once", C, "AU-028; FRD OPT-04-01", "", ""),
    ("OPT-04-02", "05/10", "Qualification precision ≥ 90%", C, "NFR-011", "", ""),
    ("OPT-04-03", "05/10", "Outreach and response; zero sends to suppressed", C, "KPI-17; AU-008", "", ""),
    ("OPT-04-04", "05/10", "Objection and meetings; no double-booking", C, "AU-023; AG-021", "", ""),
    ("OPT-04-05", "05/10", "Documents and approvals; snapshot hashes", C, "DEC-064; AU-036", "", ""),
    ("OPT-04-06", "05/10", "Financial and business closure; 100% reconciled", C, "AU-037; KPI-31", "", ""),
    ("OPT-04-07", "05/10", "Exception and learning; completion ≥ 99%", C, "NFR-009", "", ""),
    ("OPT-04-08", "05/10", "Autonomy and stop controls; ≥ 90% steps automated", C, "NFR-010", "", ""),
    ("OPT-05-01", "05/09/10", "Transactional outbox; crash recovery", C, "ADR-003; NFR-006", "", ""),
    ("OPT-05-02", "05/10", "Idempotency and concurrency; key + payload fingerprint", C, "ADR-023", "", ""),
    ("OPT-05-03", "05/10", "Timeout and retry; circuit breaker; redacted DLQ", C, "§3.2.7", "", ""),
    ("OPT-05-04", "05/10", "Durable workflow state; lease fencing", P, "ADR-027; C06 leader lock", "Fencing token rule added", "FR-ENH-B-012"),
    ("OPT-05-05", "05/10", "Backpressure and fair scheduling; urgent capacity", C, "ADR-021; RL classes", "", ""),
    ("OPT-05-06", "05/10", "Config and AI failures; fail startup on missing mandatory config", P, "AU-003 (AI part only)", "Fail-fast settings contract added", "FR-ENH-B-019; GAP-334"),
    ("OPT-05-07", "05/10", "Availability 99.9% critical over rolling 30 days", X, "DEC-018 99.5% pilot; SLO-01 28-day", "Resolution", "CONFLICT-323"),
    ("OPT-06-01", "04/05/09", "Startup templates and tenants 25+10 → 50+ / 100", X, "DEC-031", "Validation profile", "CONFLICT-321; LT-ENH-B-01"),
    ("OPT-06-02", "04/09", "Concurrent users and jobs 50/250", N, "§3.1.12", "Profile added", "LT-ENH-B-01; LT-ENH-B-03"),
    ("OPT-06-03", "04/09", "Data and scheduling volume 100k/1M, 10k/100k per day", N, "Part 3.3 volume model", "Profile added", "LT-ENH-B-02; LT-ENH-B-03"),
    ("OPT-06-04", "04/09", "Regional expansion: locale, time zone, currency, residence", C, "Part 2.4 i18n; ADR-019; ADR-030", "", ""),
    ("OPT-06-05", "04/09", "Noisy neighbour: per-tenant concurrency, quota, fair queue", C, "ADR-021; Part 6.7", "", ""),
    ("OPT-07-01", "04/05/09/10", "Modular monolith; split only with measured need", C, "ADR-001", "", ""),
    ("OPT-07-02", "04/09/10", "Four frontends and two backends", C, "ADR-006; ADR-033", "", ""),
    ("OPT-07-03", "04/09/10", "Domain and adapter boundaries; external calls outside txn", C, "ARP-01/06; ADR-009", "", ""),
    ("OPT-07-04", "04/09/10", "Configuration-driven design; new startup without code", C, "AD-10", "", ""),
    ("OPT-07-05", "04/09/10", "Complexity and reuse review; no arbitrary count reductions", C, "Part 3.2 §3.2.2.5", "", ""),
    ("OPT-08-01", "09/10", "Normalization and ownership; validated JSONB", C, "Part 3.3", "", ""),
    ("OPT-08-02", "10", "Query plans EXPLAIN (ANALYZE, BUFFERS); index actual predicates", C, "Part 3.3 index rationale; LT-03", "", ""),
    ("OPT-08-03", "10", "ORM and connections; N+1; pool sizing", C, "§3.1.12.2; Part 4.3", "", ""),
    ("OPT-08-04", "10", "Financial storage: Decimal, currency, allocations, reversals", C, "ADR-030; Part 3.3 ledgers", "", ""),
    ("OPT-08-05", "10", "Vector and cache lifecycle; invalidate on permission change", C, "ADR-007; §3.1.11", "", ""),
    ("OPT-08-06", "10", "Migration and archive; legal hold; row counts", C, "§4.37.2; Part 3.3", "", ""),
    ("OPT-09-01", "05/10", "Typed contracts 100% before activation", P, "Part 3.2 DERIVED catalogue", "Approval-gate register", "FR-ENH-B-024"),
    ("OPT-09-02", "10", "Consolidation and batching; compare calls and bytes", C, "Part 3.2 §3.2.1.6", "", ""),
    ("OPT-09-03", "10", "Adapter reliability; timeouts, rate limits, breakers, entitlement fallback", C, "§3.2.7", "", ""),
    ("OPT-09-04", "10", "Webhook processing; replay window; p95 ACK ≤ 2 s", C, "§3.2.6; SLO-08", "", ""),
    ("OPT-09-05", "10", "API costs and monitoring; meter by provider/operation/tenant", C, "ARP-15; AU-012", "", ""),
    ("OPT-10-01", "05/10", "Rules-first model routing", C, "ADR-008; DEC-007", "", ""),
    ("OPT-11-01", "05", "Provenance and source rights; 100% permitted provenance", C, "BR-M07; AU-007", "", ""),
    ("OPT-13-01", "04/10", "Code health; no blocking lint or critical dependency at merge", C, "PL gates §4.33", "", ""),
    ("OPT-13-02", "10", "Technical debt register; monthly review", N, "Not specified", "Register added", "FR-ENH-B-020; GAP-329"),
    ("OPT-13-03", "10", "Documentation and debugging; runbooks synchronized; new maintainer reproduces", P, "RB-001…015; ADR docs", "Docs-sync check added", "FR-ENH-B-020"),
    ("OPT-13-04", "10", "Dependencies pinned; isolated upgrades; deprecation monitoring", C, "§4.32 (uv hash-pinned, renovate)", "", ""),
    ("OPT-14-01", "04/10", "Shared code libraries; independent runtime config", C, "ADR-060", "", ""),
    ("OPT-14-02", "04/10", "Template reuse; versioned templates and presets", C, "A100; A113", "", ""),
    ("OPT-14-03", "04/10", "Component contracts; consumer contract tests", C, "Part 3.2 §3.2.5", "", ""),
    ("OPT-16-01", "04", "Standard setup; fresh developer runs offline checks", C, "Part 4.3 §4.35 (docker compose)", "", ""),
    ("OPT-16-02", "04", "Vertical slices and estimates; PD actual vs estimate", P, "Part 8.1 velocity (SP)", "PD tracking added", "FR-ENH-B-025"),
    ("OPT-16-03", "04", "AI-assisted development; independent review", C, "AG-034/035; Part 4.3", "", ""),
    ("OPT-17-01", "10", "Risk-based tests; no test marked pass without execution", C, "Part 6.1", "", ""),
    ("OPT-18-01", "09", "Independent CI/CD; build once, promote digest", C, "Part 4.3 §4.33", "", ""),
    ("OPT-20-01", "04", "Unit economics; contribution margin per tenant", C, "Part 4.3 §4.46.5", "", ""),
    ("OPT-20-02", "04", "Entitlements and usage reconciled 100%", C, "AU-042", "", ""),
    ("OPT-20-03", "04", "Support and renewal by cohort", C, "Part 2.4 RP; DEC-044", "", ""),
    ("OPT-20-04", "04", "Client scalability and portability", C, "B-SVC; A103", "", ""),
]
for oid, docs, s_, st, loc, act, new in OPT:
    a(docs, "Optimization engineering and acceptance", oid, s_, st, loc, act or "Mapped (OPT ID cross-reference §3.4.4.4)", new)


def main():
    os.makedirs(os.path.join(BP, "final/coverage"), exist_ok=True)
    ids = [x[2] for x in A]
    dup = [k for k, v in Counter(ids).items() if v > 1]
    assert not dup, dup
    with open(os.path.join(BP, "final/coverage/B_coverage.csv"), "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["doc", "section", "aspect_id", "aspect_summary", "status", "blueprint_location", "action", "new_ids"])
        for r in A:
            w.writerow(r)
    # status counts per doc group
    order = [C, P, N, X, NA]
    groups = OrderedDict()
    for r in A:
        groups.setdefault(r[0], Counter())[r[4]] += 1
    lines = ["| Document(s) | " + " | ".join(order) + " | Total |", "|---|" + "---|" * (len(order) + 1)]
    tot = Counter()
    for g, c in groups.items():
        lines.append("| %s | " % g + " | ".join(str(c[s]) for s in order) + " | %d |" % sum(c.values()))
        tot.update(c)
    lines.append("| **All** | " + " | ".join("**%d**" % tot[s] for s in order) + " | **%d** |" % sum(tot.values()))
    out = os.path.join(BP, "assembly/source_pack/groupB_out")
    os.makedirs(out, exist_ok=True)
    open(os.path.join(out, "status_counts.md"), "w").write("\n".join(lines) + "\n")
    # register: covered grouped compactly, others listed individually
    reg = []
    for g in groups:
        rows = [r for r in A if r[0] == g]
        reg.append("\n#### Document(s) %s\n" % g)
        reg.append("| Aspect ID | Section | Aspect | Status | Blueprint location | Action | New IDs |")
        reg.append("|---|---|---|---|---|---|---|")
        for r in rows:
            s = r[4] if r[4] != C else "Covered"
            reg.append("| %s | %s | %s | %s | %s | %s | %s |" % (r[2], r[1], r[3].replace("|", "/"), s, r[5].replace("|", "/"), r[6], r[7] or "—"))
    open(os.path.join(out, "register.md"), "w").write("\n".join(reg) + "\n")
    print("aspects", len(A), dict(tot))


if __name__ == "__main__":
    main()
