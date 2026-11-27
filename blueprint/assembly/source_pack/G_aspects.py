#!/usr/bin/env python3
"""Group G: atomic aspect inventory for documents 19 and 22 (non-test-record aspects), plus one row per
document 22 test record taken from G_map.json. Writes final/coverage/G_coverage.csv and G_aspects.json.

Usage: python3 G_aspects.py <G_map.json> <out_dir>
Status vocabulary: Covered, Partially covered, Not covered, Conflict, Not applicable, Common core.
"""
import csv
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
BP = os.path.dirname(os.path.dirname(HERE)) + "/"
M = json.load(open(sys.argv[1]))
out_dir = sys.argv[2]

CC = "Common core: see document 01/02 coverage"
A = []  # (doc, section, id, summary, status, location, action, new_ids)


def add(doc, sec, aid, summ, st, loc, act, new=""):
    A.append(dict(doc=doc, section=sec, aspect_id=aid, aspect_summary=summ, status=st, blueprint_location=loc,
                  action=act, new_ids=new))


D19 = "19_Testing_Quality_Assurance_and_User_Acceptance"
D22 = "22_Unit_SIT_and_UAT_Test_Case_Specification"

# ------------------------------------------------------------------ document 19
add(D19, "Product purpose and operating boundary", "G19-001", "Product boundary, independent deployment, two React frontends, 25+ startups and external tenants", "Common core", "Part 1; Part 3.1; DEC-002, DEC-058", CC)
add(D19, "Initial startup configurations", "G19-002", "Four legal entities and commercial focus; AppNAI owns external AI projects; EduVerse education only", "Common core", "Part 1 §1.3; FR-DM-04", CC)
add(D19, "Technology and execution principles", "G19-003", "Stack; autonomy modes; simulation zero effect; execution-time recheck", "Common core", "Part 3.1; NFR-038; DEC-064", CC)
matrix = [
    ("Product boundary", "Commercial token on investor endpoint → 401/403/uniform 404", "Covered", "TC-01-029, TC-17-010, TC-NFR-031", ""),
    ("Cross-tenant scope", "Tenant B guesses A's object/export/vector IDs → no data, logged denial", "Covered", "TC-NFR-032, TC-01-111, TC-01-114, TC-FLT-030", ""),
    ("Scope switch", "In-flight requests cancelled; old data never rendered", "Covered", "TC-17-003, TC-FLT-017", ""),
    ("Configuration", "Invalid typed filter or unapproved template → validation error, no activation", "Covered", "TC-FLT-005, TC-20-080, TC-AU-AU003-004", ""),
    ("Read-only aggregate", "Group-level send/close denied until single startup selected", "Covered", "TC-FLT-014, TC-17-013", ""),
    ("Simulation", "Planner dry run with adapters mocked → no send, charge or mutation", "Covered", "TC-NFR-038, TC-08-019, TC-21-062", ""),
    ("Eligibility", "Opt-out after queue before dispatch → suppressed, reservation released", "Covered", "TC-03-001, TC-12-083, TC-AU-AU022-002", ""),
    ("Outbox", "Crash between DB commit and dispatch → durable event, one action", "Covered", "TC-01-069, TC-01-067", ""),
    ("Replay", "Same callback twice / bad signature → one effect, invalid rejected", "Covered", "TC-NFR-005, TC-15-005, TC-10-003", ""),
    ("Cost", "Concurrent jobs exhaust budget → atomic reservation, no overspend", "Partially covered", "TC-08-008, TC-NFR-014", "TC-ENH-G-021"),
    ("Recovery", "Unknown provider result → reconcile before retry", "Covered", "TC-01-071, TC-18-070, TC-AU-AU026-001", ""),
    ("Source trust", "Web content instructs agent → no tool action or leakage", "Covered", "TC-17-087, TC-AI-AG004-008", ""),
    ("RAG", "Revoked document or other client query → no restricted chunk or citation", "Partially covered", "TC-20-096, TC-AI-AG001-005", "TC-ENH-G-029"),
    ("Billing", "Trial expiry, duplicate charge, credit → stop dispatch, one charge, approved offset", "Covered", "TC-20-086, TC-20-035, TC-20-045", ""),
    ("Offboarding", "Export then revoke → only authorized dataset, access stopped, retention audit", "Covered", "TC-21-063, TC-20-068, TC-20-071", ""),
    ("Recovery exercise", "Restore independent DB and queues; reconcile external effects", "Covered", "TC-21-091, TC-21-077, TC-NFR-057", ""),
    ("Startup routing", "External AI project routed to EduVerse → reroute to AppNAI", "Covered", "TC-14-008, TC-BRS-012", ""),
    ("Bidding", "Missing mandatory RFP requirements → no submission", "Covered", "TC-14-022, TC-AI-AG019-003, TC-21-055", ""),
    ("Order", "Buy order treated as revenue → payable only", "Covered", "TC-14-062, TC-14-074", ""),
    ("Campaign", "Invalid claim or suppressed contact → no publish/send", "Covered", "TC-11-008, TC-12-083", ""),
    ("Education/health", "Minor or patient record imported for targeting → reject/quarantine", "Partially covered", "TC-07-038, TC-16-070, TC-14-086", "TC-ENH-G-045"),
]
for i, (sc, t, st, loc, new) in enumerate(matrix, 1):
    add(D19, "Acceptance and regression test matrix", "G19-M%02d" % i, sc + ": " + t, st, loc,
        "Mapped" if not new else "Added assertion", new)
cap = [
    ("Owned startups / external tenants 25/10 → 50+/100", "Partially covered", "NFR-030; TC-01-054; Part 4.2 §4.24 sizing"),
    ("Concurrent staff sessions 50 → 250", "Partially covered", "Part 4.2 sizing (≈45/≈220 users); LT-01 80 VU"),
    ("Scoped opportunities 100,000 → 1,000,000", "Covered", "TC-NFR-048; Part 4.2 volume model"),
    ("Concurrent jobs / scheduled actions per day 50/10,000 → 250/100,000", "Partially covered", "TC-18-095 (20 concurrent runs); LT-04, LT-06"),
    ("Dashboard query p95 ≤ 2 s → ≤ 2.5 s", "Covered", "NFR-046; LT-03"),
    ("Async/webhook acknowledgement p95 ≤ 2 s", "Covered", "LT-05; TC-21-042"),
    ("Projection refresh ≤ 60 s", "Covered", "TC-NFR-008"),
    ("Critical RPO/RTO ≤ 15 min/≤ 4 h → ≤ 15 min/≤ 2 h", "Conflict", "DEC-018; NFR-057; CONFLICT-424"),
    ("Regenerable research RPO/RTO ≤ 24 h/≤ 8 h", "Not covered", "No data class for regenerable research in Part 4.2/4.3"),
]
for i, (t, st, loc) in enumerate(cap, 1):
    add(D19, "Capacity, reliability and recovery acceptance", "G19-C%02d" % i, t, st, loc,
        "Capacity acceptance case added" if st != "Covered" else "Mapped",
        "TC-ENH-G-038" + (", CONFLICT-424" if st == "Conflict" else ", GAP-424" if st != "Covered" else ""))
add(D19, "Capacity…", "G19-040", "Targets are proposals, not demonstrated capacity; fairness and independent budget/recovery on shared resources", "Covered", "Part 6.1 §6.1.5.5 certification ladder; NFR-031", "Mapped")
add(D19, "Capacity…", "G19-041", "Test pyramid: domain state machines, serializers, policy; PostgreSQL RLS/FK integration; fake adapters; contract; browser journeys; load/soak/recovery/security", "Covered", "Part 6.1 §6.1.9.1", "Mapped")
add(D19, "Capacity…", "G19-042", "Synthetic records for 4 startups, 25+ owned and 10/100 external tenants", "Partially covered", "GSE-SYN §6.1.7.1 (T1–T3)", "Scale fixture case added", "TC-ENH-G-030")
add(D19, "Capacity…", "G19-043", "Provider rate-limit, partial failure and unknown outcomes tested", "Covered", "T18; TC-AI-AG001-009; TC-01-071", "Mapped")
add(D19, "Capacity…", "G19-044", "Evidence record fields; no sensitive data; no launch on unresolved isolation/financial/permission defect", "Covered", "§6.1.5.4 EVR; §6.1.8.5 RBR-1", "Mapped")
add(D19, "Original commercial module acceptance gates", "G19-045", "66 module gates (identical to SM-SIT-M001…M066 expected gates)", "Covered", "Part 6.8b §6.8.4.6", "Mapped by module name (ASSUMPTION-420)", "TC-ENH-G-029, -027, -040")
add(D19, "Website and confidential Admin operating contract", "G19-046", "Surface/audience/exposure table; routing decision; configuration; operational separation", "Common core", "Part 2.5; Part 3.2 §3.2.1.1; DEC-019", CC)
xi = [
    ("Anonymous Admin route → denied", "Covered", "TC-17-008, TC-21-010"),
    ("External portal identity with staff endpoint → denied", "Covered", "TC-01-125, TC-17-008"),
    ("Foreign tenant/issuer ID → uniform denied", "Covered", "TC-01-049"),
    ("Expired token → denied", "Covered", "TC-01-062, TC-19-070"),
    ("Unapproved draft/preview → no public content", "Covered", "TC-11-024, TC-19-028"),
    ("Public cached payload has no internal fields", "Covered", "TC-19-044, TC-19-058"),
    ("Scope switch clears private cache", "Covered", "TC-FLT-017, TC-17-003"),
    ("Website enquiry → exactly one scoped workflow", "Covered", "TC-12-016, TC-21-054"),
    ("Webhook replay → no duplicate receipt", "Covered", "TC-15-004, TC-NFR-005"),
    ("Public AI prompt asks for private records → no disclosure", "Covered", "TC-AI-AG017-*, TC-10-036"),
    ("Publish/unpublish reflects approved revision", "Covered", "TC-19-033, TC-11-022"),
    ("Disabled client site returns safe unavailable", "Not covered", "—"),
    ("Keyboard, screen-reader names, contrast, mobile forms", "Covered", "T08; TC-17-067, TC-10-054"),
]
for i, (t, st, loc) in enumerate(xi, 1):
    add(D19, "Cross-interface acceptance and regression", "G19-X%02d" % i, t, st, loc,
        "Mapped" if st == "Covered" else "New case", "" if st == "Covered" else "TC-ENH-G-042")
add(D19, "Executable test design", "G19-060", "Deterministic UT; SIT with PostgreSQL/Celery/Valkey and sandbox contracts; browser UAT per journey and per UI item", "Covered", "§6.1.2; §6.1.13", "Mapped")
add(D19, "Executable test design", "G19-061", "Every case records ID, requirement, setup, input, action, expected, evidence, severity, result, owner, sign-off", "Covered", "§6.1.12.2 template; §6.1.5.4 EVR", "Mapped")
add(D19, "Executable test design", "G19-062", "Every catalogued operation and screen: happy path + access negative; callbacks invalid signature/replay; consequential writes idempotency; regulated/finance blocked cases", "Partially covered", "CT-03/CT-05/CT-10 (Part 3.2 §3.2.5) without TC IDs", "Operation-class TCs with IDs and per-operation data", "TC-ENH-G-001…017; GAP-420")
add(D19, "Executable test design", "G19-063", "No test represented as passed until execution evidence exists", "Covered", "§6.1.5.5 ladder; RBR-6", "Mapped")
add(D19, "Executable test design", "G19-064", "Acceptance journeys: AppNAI bid, MedMaarg pilot, EduVerse adult/school, OrganicSpec purchase/sales/service/training, campaigns, quotations, renewal; no investor records", "Partially covered", "UAT-PK-AN/MM/EV/OS/FIN; no marketing or renewal pack", "UAT packs MKT and CS proposed", "TC-ENH-G-032…034; GAP-422")
add(D19, "Testing exit criteria and traceability", "G19-065", "Every catalogued operation and interface maps to an applicable test; critical cases pass; performance/recovery/security/accessibility evidence", "Partially covered", "Part 6.6 RTM (FR-level)", "Source-test mapping CSV and operation mapping added", "G_test_mapping.csv")
add(D19, "Testing exit criteria and traceability", "G19-066", "Vertical acceptance statements (AppNAI, MedMaarg, EduVerse, OrganicSpec, campaigns)", "Covered", "§6.1.13.3 packs (BRD §11 quotes)", "Mapped")
add(D19, "Implementation, verification and delivery controls", "G19-067", "624 cases Not run; every screen and operation has mapped acceptance or contract test", "Partially covered", "Part 6.6", "Mapping completed here", "G_test_mapping.csv")
layers = [("Unit", "critical branch coverage ≥ 90% proposed; deterministic fixtures", "Conflict", "§6.1.9.6 (≥ 90% domain core); NFR-082; CONFLICT-421"),
          ("SIT", "reviewed contracts; scoped data; mock/sandbox; mandatory positive/negative/failure checks", "Covered", "§6.1.5.1"),
          ("UAT", "integrated stable environment; business owner scenario; all flows accepted", "Covered", "§6.1.13.4–5"),
          ("Specialist", "security, load, restore, rollback rehearsals", "Covered", "§6.1.14"),
          ("Release", "QC evidence, approvals, training, monitoring; go-live record, digest, rollback readiness", "Covered", "Part 8.2; A090")]
for i, (l, t, st, loc) in enumerate(layers, 1):
    add(D19, "Test layer entry/exit gates", "G19-L%02d" % i, l + ": " + t, st, loc, "Mapped" if st == "Covered" else "Resolution proposed", "CONFLICT-421" if st == "Conflict" else "")
add(D19, "Acceptance and evidence record", "G19-080", "Responsible/reviewer; artifact evidence; decision Pending/Pass/Fail/approved N/A; remediation; business acceptance", "Covered", "§6.1.5.4 EVR", "Mapped")
gates = [("Contract fixture checks: 164 request, 164 invalid, 165 response examples validated offline", "Partially covered", "CT-04 example round-trip", "RECOMMENDATION-424"),
         ("Reference suite: 522 offline checks; product cases Not run", "Not applicable", "No reference starter in blueprint; ladder L-S rule applies", ""),
         ("Product test: implement mapped Unit/SIT/UAT; record expected/observed, state diffs, audit IDs, build hash", "Covered", "§6.1.5.4", ""),
         ("Quality gate: no unresolved critical/high privacy, authz, financial, regulated, deployment defect", "Covered", "§6.1.8.5 RBR-1…8", ""),
         ("Retest: defect → owner → fix → reproduce → regression → close with evidence", "Covered", "§6.1.8.1", "")]
for i, (t, st, loc, new) in enumerate(gates, 1):
    add(D19, "Test execution evidence and blocking rules", "G19-G%02d" % i, t, st, loc, "Mapped" if st == "Covered" else "Recommendation" if new else "Noted", new)
opt = [("OPT-01-01", "Authentication and privileged sessions — zero revoked/wrong-audience/privileged bypass", "Covered", "TC-01-001…013, TC-01-062"),
       ("OPT-02-01", "Public website assets — LCP p75 ≤ 2.5 s, INP ≤ 200 ms, CLS ≤ 0.1", "Covered", "NFR (Part 4.2); LT-02; T03"),
       ("OPT-05-01", "Transactional outbox — crash between commit and publish recovers", "Covered", "TC-01-069"),
       ("OPT-10-01", "Rules-first model routing — compare quality, latency and INR per task", "Covered", "Part 7.3; TC-AI"),
       ("OPT-17-01", "Risk-based tests by operation; 100% mandatory regression; no pass without execution", "Partially covered", "§6.1.4; §6.1.12; ID not referenced"),
       ("OPT-17-02", "Automated evidence with integrity validation; missing evidence blocks", "Partially covered", "§6.1.5.4; RBR-6"),
       ("OPT-17-03", "Traceability and orphan review to UI/API/data/workflow/test/optimization control", "Partially covered", "Part 6.6 (no operation/optimization-control columns)"),
       ("OPT-17-04", "Test efficiency: parallel, isolated data and clocks, flake measured, fail on external side effect", "Covered", "§6.1.6.4 outbound guard; §6.1.9.7 flaky policy"),
       ("OPT-18-01", "Independent CI/CD; build once; promote digest; rollback per component", "Covered", "Part 4.3")]
for i, (oid, t, st, loc) in enumerate(opt, 1):
    add(D19, "Optimization engineering and acceptance", oid, t, st, loc,
        "OPT crosswalk added (§6.8.5.1.5)" if st != "Covered" else "Mapped (common optimization core also reviewed by document 36 group)",
        "TC-ENH-G-039" if oid in ("OPT-17-02",) else "")
procs = [("Test fixture reuse without leakage", "Covered", "§6.1.7.3 generation rules; §6.1.7.6", ""),
         ("AI-assisted coding quality: review generated code for licensing, scope, correctness, tests, secrets", "Partially covered", "§6.1.9.4 (tests only); TC-AI-AG034-002", "TC-ENH-G-043"),
         ("Product Unit/SIT/UAT coverage vs screen and operation inventories", "Partially covered", "Part 6.6", "G_test_mapping.csv"),
         ("Fail-closed evidence inventory from immutable required-ID baseline; reject missing/extra/duplicate IDs, mandatory N/A", "Partially covered", "RBR-6; A090 fail closed", "TC-ENH-G-039"),
         ("Evidence integrity: blank evidence, executor = reviewer after trim/case-fold, artifact hashes", "Partially covered", "EVR responsible ≠ reviewer", "TC-ENH-G-039"),
         ("Combined preflight: 1,188 records in six groups incl. 21 mandatory KPIs; CTO + PO signed approval", "Not covered", "—", "TC-ENH-G-040; GAP-425")]
for i, (t, st, loc, new) in enumerate(procs, 1):
    add(D19, "Implementation acceptance procedures", "G19-P%02d" % i, t, st, loc, "Mapped" if st == "Covered" else "Added", new)
add(D19, "Current scope — testing strategy", "G19-100", "10 shared scenarios (= SM-UX-SIT-X01…X10)", "Partially covered", "See X01…X10 rows", "Mapped; 3 added", "TC-ENH-G-030, -031, -035")

# ------------------------------------------------------------------ document 22 non-record aspects
p22 = [
    ("§1", "Purpose: proposed catalogue; all cases Not run; targets proposed interfaces", "Covered", "§6.1.5.5; GAP-167 now resolved", "Catalogue received and reconciled", ""),
    ("§1", "Test level table: 66 UT, 35 SIT-E2E, 302 SIT-ops, 66 SIT-module, 17 UAT journeys, 138 UAT screens = 624; +175 current-scope = 799", "Not covered", "GAP-003/GAP-167 (catalogue was missing)", "All 799 parsed and mapped", "G_test_mapping.csv"),
    ("§2", "Fixture T1 owned portfolio (S-A, S-M, S-E, S-O, S-05)", "Partially covered", "GSE-SYN §6.1.7.1", "Fixture crosswalk", "ASSUMPTION-424"),
    ("§2", "Fixture T2 external client (S-X) and T3 forbidden look-alike tenant", "Covered", "GSE-SYN T2/T3; TC-01-X matrix", "Crosswalk", "ASSUMPTION-424"),
    ("§2", "Internal identities O1, D1/E1, L1, F1, A1, N1 with MFA/revoked", "Partially covered", "Persona fixtures (Part 6.5 §6.5.1.4)", "Crosswalk", "ASSUMPTION-424"),
    ("§2", "External identities X1, X2, X3, V1 (distinct token audience)", "Partially covered", "PP-03 portal profiles", "Crosswalk", "ASSUMPTION-424"),
    ("§2", "Publication fixtures R1/H1 approved, R2/H2 unapproved, verified/unknown host, two locales", "Covered", "TC-19-0xx fixtures", "Crosswalk", ""),
    ("§2", "Evidence fixtures: permitted snapshot, stale, conflicting, denied domain", "Covered", "EP-05 fixtures (F1–F6)", "Crosswalk", ""),
    ("§2", "Workflow fixtures: approved/cyclic DAG, fake clock, budget 10 units, provider 429/timeout/unknown, duplicates", "Covered", "§6.1.6.3 simulator; §6.1.6.5 clock", "Crosswalk", ""),
    ("§2", "Financial fixtures ₹1,000 split ₹600 + ₹400; wrong beneficiary/currency; duplicate callback; over-allocation; refund", "Partially covered", "EP-15 fixtures (different values)", "Class TC uses source values", "TC-ENH-G-011, TC-ENH-G-023"),
    ("§2", "Files and AI fixtures: benign PDF, oversized, malware test file, wrong-scope knowledge, prompt injection", "Covered", "TC-02-020; T14 red-team set", "Mapped", ""),
    ("§2", "Environment: isolated PostgreSQL/Valkey/Celery, test storage, SMTP sandbox, no live credentials, fake clock, fixed seed, trace IDs", "Covered", "§6.1.6", "Mapped", ""),
    ("§2", "Preconditions for all cases: reset per case, never real recipient, record trace IDs, signed test callbacks", "Covered", "§6.1.6.4 outbound allowlist guard", "Mapped", ""),
    ("§3", "Tooling: pytest/pytest-django, Vitest/RTL, Playwright, AI regression, security/load/recovery suites", "Covered", "§6.1.9.2 (versions verify at implementation, as of 27 Nov 2026)", "Mapped", ""),
    ("§3", "Gates: no unresolved critical/high; 100% critical policy and state-transition cases; all ops/screens executed or dispositioned; ≥ 80% domain-service branch coverage", "Conflict", "§6.1.9.6; NFR-082", "Resolution proposed", "CONFLICT-421"),
    ("§3", "Unit pass not a substitute for SIT/UAT; report skips, blocked providers, failed cases, untested routes", "Partially covered", "§6.1.10.3 readiness report", "Untested-route and blocked-provider lines added to A090 report", "TC-ENH-G-044"),
    ("§10", "Severity Critical/P0…Low/P3 with required disposition", "Conflict", "§6.1.8.2 S1–S4 + FP1–FP4", "Crosswalk", "CONFLICT-423"),
    ("§10", "Execution record fields incl. status Not run/Pass/Fail/Blocked/N/A", "Partially covered", "EVR decision Pending/Pass/Fail/Approved N/A", "Execution-status extension", "GAP-423, RECOMMENDATION-422, TC-ENH-G-044"),
    ("§10", "Acceptance gates: Unit/SIT/UAT complete, security and financial gate, production authorization, with sign-off owners", "Covered", "§6.1.5.1–5.3; AP-01…AP-10", "Crosswalk", ""),
    ("§10", "No real secrets, investor, patient or learner records in evidence; N/A must be approved", "Covered", "§6.1.7.6; EVR Approved N/A", "Mapped", ""),
    ("Execution and quality sign-off", "Retain test IDs; Not run until executed; nonfunctional gates supplement", "Covered", "§6.1.5.5", "Mapped; SM-* IDs retained as aliases", "RECOMMENDATION-423"),
    ("Implementation controls", "Operation-specific positive/negative/boundary variants for all 302 SIT operations", "Partially covered", "CT-03/CT-05 generic", "Class TCs with per-operation data", "TC-ENH-G-001…017"),
    ("Implementation controls", "Screen and journey negative/recovery variants for 17 journeys and 138 screens", "Partially covered", "Packs; per-screen states in Part 2.5", "Screen template", "TC-ENH-G-036"),
    ("Implementation controls", "16 offline reference unit tests on the engineering starter are not product executions", "Not applicable", "No starter repository in the blueprint", "Noted", ""),
    ("Concrete fixtures", "SM-CORE-01 quotation 2 × INR 150.00 at 10% = 270.00", "Covered", "TC-13-016", "Mapped", ""),
    ("Concrete fixtures", "SM-CORE-02 bid expiry 2030-06-01 09:00 UTC at/after deadline", "Covered", "TC-14-022…024", "Mapped", ""),
    ("Concrete fixtures", "SM-CORE-03 order 2 kg; 1 kg twice same key; +2 kg rejected", "Covered", "TC-21-058, TC-14-089", "Mapped", ""),
    ("Concrete fixtures", "SM-CORE-04 EduVerse routing: external AI dev → AppNAI; school AI → EduVerse", "Covered", "TC-14-008, TC-14-002", "Mapped", ""),
    ("Concrete fixtures", "164 candidate payloads and 165 response examples schema-validated offline", "Partially covered", "CT-04", "Recommendation", "RECOMMENDATION-424"),
    ("Optimization", "OPT-01-01, 02-01, 04-01, 05-01, 07-01, 08-01, 10-01, 11-01, 19-01 (common optimization core)", "Common core", "Document 36 group coverage", "Not re-listed", ""),
    ("Optimization", "OPT-17-01…04 testing and QC controls", "Partially covered", "See G19 OPT rows", "OPT crosswalk", "TC-ENH-G-039"),
    ("Implementation acceptance", "Authorization and error contract: wrong role, scope, malformed field, conflict, rate limit; no confidential fields in errors/logs", "Covered", "CT-05; TC-21-015; TC-NFR-004", "Mapped; class TCs add per-operation", "TC-ENH-G-001…003"),
    ("Implementation acceptance", "Structured output quality ≥ 99.5% schema-valid; invalid output never drives side effects", "Covered", "TC-AI-AG*-schema-valid; TC-04-040", "Mapped", ""),
    ("Implementation acceptance", "Reference test integrity: rerun reference/contract/optimization tests; skipped/failed separately", "Partially covered", "§6.1.10.1 metrics", "Added to evidence preflight", "TC-ENH-G-039"),
    ("Implementation acceptance", "Evidence integrity and final acceptance (executor ≠ reviewer after trim/case-fold; hashes; signed approvals)", "Partially covered", "EVR", "Added", "TC-ENH-G-039"),
    ("Current scope", "Release condition: approved screen/contract/entity decisions, expanded tests, QC and original acceptance evidence", "Covered", "A090; RBR-6", "Mapped", ""),
]
for i, (sec, t, st, loc, act, new) in enumerate(p22, 1):
    add(D22, sec, "G22-%03d" % i, t, st, loc, act, new)

# ------------------------------------------------------------------ one row per test record
STMAP = {"E": "Covered", "A": "Covered", "P": "Partially covered", "N": "Not covered", "M": "Partially covered", "C": "Conflict"}
for r in M["rows"]:
    loc = "; ".join(x for x in [r["primary_tcs"], r["bp_requirement"], r["bp_operation"]] if x)
    act = {"E": "Mapped to equivalent TC(s)", "A": "Mapped via DEC-017 alias + execution template",
           "P": "Mapped; missing assertion added", "N": "New TC written", "M": "Mapped to operation-class TC + functional TCs"}[r["status"]]
    add(D22, r["group"], r["source_id"], (r["title"] + " " + r["link"]).strip()[:160], STMAP[r["status"]], loc, act, r["tc_enh"])

with open(BP + "final/coverage/G_coverage.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=["doc", "section", "aspect_id", "aspect_summary", "status", "blueprint_location", "action", "new_ids"])
    w.writeheader()
    w.writerows(A)
json.dump(A, open(os.path.join(out_dir, "G_aspects.json"), "w"), ensure_ascii=False, indent=0)
from collections import Counter  # noqa: E402
print(len(A), Counter((a["doc"][:2], a["status"]) for a in A))
