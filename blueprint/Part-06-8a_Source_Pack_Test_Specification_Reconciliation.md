# AI Growth Engine: Employee Sales & Marketing Automation
## Application Blueprint: PART 6 (Batch 6.8a), Source Pack Test Specification Reconciliation: Documents, Coverage Summary and Detailed Register

| Field | Value |
|---|---|
| Document | Application Blueprint · Part 6.8a. Reconciles source documents 19 (Testing, QA and UAT) and 22 (Unit, SIT and UAT Test Case Specification, 799 tests) against Part 6. This file: §6.8.1 documents reviewed, §6.8.2 coverage summary, §6.8.3 detailed coverage register. Part 6.8b holds the catalogue reconciliation (§6.8.4); Part 6.8c holds the new test cases and decisions (§6.8.5–§6.8.9) |
| Version | 1.0 · 27 Nov 2026 |
| Baseline | Part 6.1 (test strategy, template §6.1.12.2, alias rules §6.1.12.5, UAT packs §6.1.13.3, EVR §6.1.5.4, severity §6.1.8.2), Batches 6.2–6.5 and 6.7 (2,912 TCs), Part 6.6 RTM and `final/RTM.csv`, Part 3.2 API catalogue (API-001…555, AD-01…20), Part 2.1 module and FR register, DEC-015, DEC-017, DEC-018, DEC-093, DEC-094; source pack documents 19 and 22 (DOCX extractions), document 38 counts |
| Roles applied | QA Lead / Test Architect (primary), UAT Manager, Business Systems Analyst (journey acceptance), Principal Engineer (operation contracts), Security/Compliance Lead (negative fixtures), FinOps Lead (budget and billing cases), Product Owner (sign-off model) |
| Tag ranges used | ASSUMPTION-420…424, GAP-420…425, CONFLICT-420…424, RECOMMENDATION-420…425 (register in Part 6.8c §6.8.8) |


**Acronyms used in this part.** API application programming interface · BR business requirement · CT contract test · DTO data transfer object · E2E end-to-end · ENH enhancement test case (TC-ENH-G-###) · EVR evidence record · FR functional requirement · IT integration test · OKPI optimization KPI of the source pack (document 38, renamed to avoid the Part 1 KPI collision) · RTM requirements traceability matrix · SIT system integration testing · SYS system test · TC test case · UAT user acceptance testing · UT unit test.

**How to read Part 6.8.** Every one of the 799 source tests has exactly one row in `final/coverage/G_test_mapping.csv` and in the tables of Part 6.8b. The mapping status is one of: **Equivalent** (a blueprint TC asserts the same condition and outcome), **Alias-equivalent** (DEC-017 alias rule maps the source ID to a requirement whose TCs and UAT pack cover it; an execution template TC-ENH-G-036/037 makes the per-screen steps explicit), **Class-mapped** (operation-level SIT contract case mapped to a parameterized operation-contract TC plus the functional TCs of the operation's FR), **Partial + ENH** (blueprint TCs cover the requirement; the missing assertion is written as a TC-ENH-G case in Part 6.8c) and **New ENH** (no equivalent; a new TC-ENH-G case is written). Source IDs are retained as aliases (RECOMMENDATION-423).

**Time-sensitive facts.** Tool names and versions (pytest, Vitest, Playwright, schemathesis, k6, axe-core), provider sandbox behaviour and API limits are design intent: verify at time of implementation (as of 27 Nov 2026).

---

## 6.8.1 Documents reviewed

| Item | Document 19: Testing, Quality Assurance and User Acceptance | Document 22: Unit, SIT and UAT Test Case Specification |
|---|---|---|
| Size (plain-text extraction) | 35,265 bytes; 603 lines; 13 tables | 1,015,801 bytes; 5,670 lines; 45 tables; 799 test records |
| Sections | Product purpose and boundary; initial startup configurations; technology principles; acceptance and regression test matrix (21 rows); capacity, reliability and recovery acceptance (9 metrics); original commercial module acceptance gates (66); Website/Admin operating contract; cross-interface acceptance; executable test design and gates; exit criteria and traceability; implementation, verification and delivery controls (5 layer gates); evidence record; test execution evidence and blocking rules; optimization engineering (OPT-01-01, 02-01, 05-01, 10-01, 17-01…04, 18-01); implementation acceptance procedures; final decision controls incl. combined preflight; current scope testing strategy (10 scenarios) | §1 purpose and scope (level table); §2 environment and reusable fixtures (11 fixture families); §3 tooling and execution rules and gates; §4 unit catalogue SM-UT-001…066 in 19 groups; §5 SIT end-to-end SM-SIT-F001…F035; §6 commercial module acceptance SM-SIT-M001…M066; §7 SIT operation-level contracts SM-SIT-A001…A302 in 8 audiences; §8 UAT journeys SM-UAT-F001…F017; §9 UAT screen acceptance SM-UAT-S001…S138; §10 defect management and sign-off; execution sign-off; implementation controls with positive/negative/boundary variants for 302 operations and 155 journeys/screens; acceptance and evidence record; SM-CORE-01…04 fixtures; optimization controls; implementation acceptance procedures; current scope: SM-UX-UAT ×147, SM-UX-UNIT ×9, SM-UX-SIT ×9 + X01…X10 |
| What it is trying to tell | The quality contract: what must be proven, at which layer, with which evidence, before any external activation; it is the policy layer above document 22 and repeats the common core | The executable test design: every case with fixture, action and expected result, so that it can be converted to pytest/Playwright and to managed QA execution records; nothing is claimed as executed |
| Pattern | Common core (product boundary, operating contract, vertical statements, optimization block) + QA policy | Common core blocks + the full 799-case catalogue (document 38: Unit 75, SIT 422, UAT 302) |
| Atomic aspects found | 88 | 835 (799 test records + 36 prose aspects) |


**Programmatic parsing.** `assembly/source_pack/G_parse_doc22.py` parses every table row and heading block of document 22 into 799 records (ID, level, family, group, title, linked FR/screen/module/method+path, preconditions/setup, steps, expected result, negative and boundary variants, fixture data, inspected entities) and asserts the document 38 totals: **Unit 75 (66 SM-UT + 9 SM-UX-UNIT), SIT 422 (35 SM-SIT-F + 66 SM-SIT-M + 302 SM-SIT-A + 9 SM-UX-SIT screen + 10 SM-UX-SIT-X), UAT 302 (17 SM-UAT-F + 138 SM-UAT-S + 147 SM-UX-UAT)**. The 302 operation cases are asserted per audience group (Authentication 3, Admin 242, Internal adapter 17, Portal 14, Portal + Admin 5, Public 10, Internal worker 3, Provider callback 8). `G_blueprint_index.py` indexes the 2,912 blueprint TCs (through `assembly/build_rtm.py`), `final/RTM.csv`, the 555 Part 3.2 operations and 20 adapters. `G_similarity.py` proposes candidates (TF-IDF); `G_curated.py` holds the reviewed equivalences; `G_map.py` writes the mapping; `G_aspects.py` the coverage register; `G_render.py` the generated tables in this file and Part 6.8b.

---

## 6.8.2 Coverage register summary

### 6.8.2.1 Aspects by status per document

| Document | Covered | Partially covered | Not covered | Conflict | Not applicable | Common core | Total |
|---|---|---|---|---|---|---|---|
| 19 Testing QA and UAT | 58 | 20 | 3 | 2 | 1 | 4 | 88 |
| 22 Unit SIT UAT catalogue | 491 | 338 | 2 | 2 | 1 | 1 | 835 |
| **Total** | 549 | 358 | 5 | 4 | 2 | 5 | 923 |


"Partially covered" for the 302 operation cases means that the blueprint verifies the behaviour through the operation's FR test cases and the generic contract layers CT-03/CT-05 (Part 3.2 §3.2.5), which have no TC IDs; Part 6.8c closes this with the operation-class cases TC-ENH-G-001…017 (GAP-420).

### 6.8.2.2 Source tests by family and mapping status

| Family | Level | Tests | Equivalent | Alias-equivalent | Class-mapped | Partial + ENH | New ENH |
|---|---|---|---|---|---|---|---|
| UT | Unit | 66 | 54 | 0 | 0 | 11 | 1 |
| UX-UNIT | Unit | 9 | 9 | 0 | 0 | 0 | 0 |
| SIT-F | SIT | 35 | 31 | 0 | 0 | 4 | 0 |
| SIT-M | SIT | 66 | 63 | 0 | 0 | 3 | 0 |
| SIT-A | SIT | 302 | 0 | 0 | 302 | 0 | 0 |
| UX-SIT | SIT | 19 | 16 | 0 | 0 | 3 | 0 |
| UAT-F | UAT | 17 | 14 | 0 | 0 | 3 | 0 |
| UAT-S | UAT | 138 | 0 | 138 | 0 | 0 | 0 |
| UX-UAT | UAT | 147 | 0 | 147 | 0 | 0 | 0 |
| **Total** |  | 799 | 187 | 285 | 302 | 24 | 1 |


### 6.8.2.3 Headline results

| # | Result | Evidence |
|---|---|---|
| 1 | All 799 source tests are mapped: 187 Equivalent, 285 Alias-equivalent, 302 Class-mapped, 24 Partial + ENH, 1 New ENH | `final/coverage/G_test_mapping.csv` |
| 2 | 45 new blueprint test cases TC-ENH-G-001…045 written at template depth: 17 parameterized operation-contract classes, 2 parameterized screen templates, 26 specific cases | Part 6.8c §6.8.5.2 |
| 3 | The SM-UAT-S alias rule of Part 6.1 §6.1.12.5 (S001–S030 = W01–W30; S031–S138 = A001–A108) is **confirmed for all 138 rows** by the screen code printed in each source row | §6.8.4.9 |
| 4 | SM-UT-037, -049 and -050 do exist in the source (webhook signature, offering publication, need matching); DEC-094 ("unassigned, no obligation") is superseded | CONFLICT-420 |
| 5 | The inferred SM-UT family labels (ASSUMPTION-180) are replaced by the source titles; coverage stays FR-based | §6.8.4.3 |
| 6 | SM-SIT-M numbers follow document 22's table order: 50 of 66 differ from the BRD module number used by BR-M##; mapping is by module name | ASSUMPTION-420; §6.8.4.6 |
| 7 | Operations: 101 exact path, 73 normalized namespace match, 21 nearest, 9 consolidated into the Approval resource, 17 adapter ports, **81 with no Part 3.2 counterpart** | GAP-421; §6.8.4.7 |
| 8 | Two UAT packs are missing for source journeys (marketing; renewals/customer success) | GAP-422; UAT-PK-MKT, UAT-PK-CS proposed |


---

## 6.8.3 Detailed coverage register

Every Not covered, Partial and Conflict aspect is listed individually. Covered test records are listed in Part 6.8b; covered prose aspects are listed here so the register is complete for both documents.

### 6.8.3.1 Document 19 aspects

| ID | Section | Aspect | Status | Blueprint location | Action | New IDs |
|---|---|---|---|---|---|---|
| G19-001 | Product purpose and operating boundary | Product boundary, independent deployment, two React frontends, 25+ startups and external tenants | Common core | Part 1; Part 3.1; DEC-002, DEC-058 | Common core: see document 01/02 coverage |  |
| G19-002 | Initial startup configurations | Four legal entities and commercial focus; AppNAI owns external AI projects; EduVerse education only | Common core | Part 1 §1.3; FR-DM-04 | Common core: see document 01/02 coverage |  |
| G19-003 | Technology and execution principles | Stack; autonomy modes; simulation zero effect; execution-time recheck | Common core | Part 3.1; NFR-038; DEC-064 | Common core: see document 01/02 coverage |  |
| G19-M01 | Acceptance and regression test matrix | Product boundary: Commercial token on investor endpoint → 401/403/uniform 404 | Covered | TC-01-029, TC-17-010, TC-NFR-031 | Mapped |  |
| G19-M02 | Acceptance and regression test matrix | Cross-tenant scope: Tenant B guesses A's object/export/vector IDs → no data, logged denial | Covered | TC-NFR-032, TC-01-111, TC-01-114, TC-FLT-030 | Mapped |  |
| G19-M03 | Acceptance and regression test matrix | Scope switch: In-flight requests cancelled; old data never rendered | Covered | TC-17-003, TC-FLT-017 | Mapped |  |
| G19-M04 | Acceptance and regression test matrix | Configuration: Invalid typed filter or unapproved template → validation error, no activation | Covered | TC-FLT-005, TC-20-080, TC-AU-AU003-004 | Mapped |  |
| G19-M05 | Acceptance and regression test matrix | Read-only aggregate: Group-level send/close denied until single startup selected | Covered | TC-FLT-014, TC-17-013 | Mapped |  |
| G19-M06 | Acceptance and regression test matrix | Simulation: Planner dry run with adapters mocked → no send, charge or mutation | Covered | TC-NFR-038, TC-08-019, TC-21-062 | Mapped |  |
| G19-M07 | Acceptance and regression test matrix | Eligibility: Opt-out after queue before dispatch → suppressed, reservation released | Covered | TC-03-001, TC-12-083, TC-AU-AU022-002 | Mapped |  |
| G19-M08 | Acceptance and regression test matrix | Outbox: Crash between DB commit and dispatch → durable event, one action | Covered | TC-01-069, TC-01-067 | Mapped |  |
| G19-M09 | Acceptance and regression test matrix | Replay: Same callback twice / bad signature → one effect, invalid rejected | Covered | TC-NFR-005, TC-15-005, TC-10-003 | Mapped |  |
| G19-M10 | Acceptance and regression test matrix | Cost: Concurrent jobs exhaust budget → atomic reservation, no overspend | Partially covered | TC-08-008, TC-NFR-014 | Added assertion | TC-ENH-G-021 |
| G19-M11 | Acceptance and regression test matrix | Recovery: Unknown provider result → reconcile before retry | Covered | TC-01-071, TC-18-070, TC-AU-AU026-001 | Mapped |  |
| G19-M12 | Acceptance and regression test matrix | Source trust: Web content instructs agent → no tool action or leakage | Covered | TC-17-087, TC-AI-AG004-008 | Mapped |  |
| G19-M13 | Acceptance and regression test matrix | RAG: Revoked document or other client query → no restricted chunk or citation | Partially covered | TC-20-096, TC-AI-AG001-005 | Added assertion | TC-ENH-G-029 |
| G19-M14 | Acceptance and regression test matrix | Billing: Trial expiry, duplicate charge, credit → stop dispatch, one charge, approved offset | Covered | TC-20-086, TC-20-035, TC-20-045 | Mapped |  |
| G19-M15 | Acceptance and regression test matrix | Offboarding: Export then revoke → only authorized dataset, access stopped, retention audit | Covered | TC-21-063, TC-20-068, TC-20-071 | Mapped |  |
| G19-M16 | Acceptance and regression test matrix | Recovery exercise: Restore independent DB and queues; reconcile external effects | Covered | TC-21-091, TC-21-077, TC-NFR-057 | Mapped |  |
| G19-M17 | Acceptance and regression test matrix | Startup routing: External AI project routed to EduVerse → reroute to AppNAI | Covered | TC-14-008, TC-BRS-012 | Mapped |  |
| G19-M18 | Acceptance and regression test matrix | Bidding: Missing mandatory RFP requirements → no submission | Covered | TC-14-022, TC-AI-AG019-003, TC-21-055 | Mapped |  |
| G19-M19 | Acceptance and regression test matrix | Order: Buy order treated as revenue → payable only | Covered | TC-14-062, TC-14-074 | Mapped |  |
| G19-M20 | Acceptance and regression test matrix | Campaign: Invalid claim or suppressed contact → no publish/send | Covered | TC-11-008, TC-12-083 | Mapped |  |
| G19-M21 | Acceptance and regression test matrix | Education/health: Minor or patient record imported for targeting → reject/quarantine | Partially covered | TC-07-038, TC-16-070, TC-14-086 | Added assertion | TC-ENH-G-045 |
| G19-C01 | Capacity, reliability and recovery accep | Owned startups / external tenants 25/10 → 50+/100 | Partially covered | NFR-030; TC-01-054; Part 4.2 §4.24 sizing | Capacity acceptance case added | TC-ENH-G-038, GAP-424 |
| G19-C02 | Capacity, reliability and recovery accep | Concurrent staff sessions 50 → 250 | Partially covered | Part 4.2 sizing (≈45/≈220 users); LT-01 80 VU | Capacity acceptance case added | TC-ENH-G-038, GAP-424 |
| G19-C03 | Capacity, reliability and recovery accep | Scoped opportunities 100,000 → 1,000,000 | Covered | TC-NFR-048; Part 4.2 volume model | Mapped | TC-ENH-G-038 |
| G19-C04 | Capacity, reliability and recovery accep | Concurrent jobs / scheduled actions per day 50/10,000 → 250/100,000 | Partially covered | TC-18-095 (20 concurrent runs); LT-04, LT-06 | Capacity acceptance case added | TC-ENH-G-038, GAP-424 |
| G19-C05 | Capacity, reliability and recovery accep | Dashboard query p95 ≤ 2 s → ≤ 2.5 s | Covered | NFR-046; LT-03 | Mapped | TC-ENH-G-038 |
| G19-C06 | Capacity, reliability and recovery accep | Async/webhook acknowledgement p95 ≤ 2 s | Covered | LT-05; TC-21-042 | Mapped | TC-ENH-G-038 |
| G19-C07 | Capacity, reliability and recovery accep | Projection refresh ≤ 60 s | Covered | TC-NFR-008 | Mapped | TC-ENH-G-038 |
| G19-C08 | Capacity, reliability and recovery accep | Critical RPO/RTO ≤ 15 min/≤ 4 h → ≤ 15 min/≤ 2 h | Conflict | DEC-018; NFR-057; CONFLICT-424 | Capacity acceptance case added | TC-ENH-G-038, CONFLICT-424 |
| G19-C09 | Capacity, reliability and recovery accep | Regenerable research RPO/RTO ≤ 24 h/≤ 8 h | Not covered | No data class for regenerable research in Part 4.2/4.3 | Capacity acceptance case added | TC-ENH-G-038, GAP-424 |
| G19-040 | Capacity… | Targets are proposals, not demonstrated capacity; fairness and independent budget/recovery on shared resources | Covered | Part 6.1 §6.1.5.5 certification ladder; NFR-031 | Mapped |  |
| G19-041 | Capacity… | Test pyramid: domain state machines, serializers, policy; PostgreSQL RLS/FK integration; fake adapters; contract; browser journeys; load/soak/recovery/security | Covered | Part 6.1 §6.1.9.1 | Mapped |  |
| G19-042 | Capacity… | Synthetic records for 4 startups, 25+ owned and 10/100 external tenants | Partially covered | GSE-SYN §6.1.7.1 (T1–T3) | Scale fixture case added | TC-ENH-G-030 |
| G19-043 | Capacity… | Provider rate-limit, partial failure and unknown outcomes tested | Covered | T18; TC-AI-AG001-009; TC-01-071 | Mapped |  |
| G19-044 | Capacity… | Evidence record fields; no sensitive data; no launch on unresolved isolation/financial/permission defect | Covered | §6.1.5.4 EVR; §6.1.8.5 RBR-1 | Mapped |  |
| G19-045 | Original commercial module acceptance ga | 66 module gates (identical to SM-SIT-M001…M066 expected gates) | Covered | Part 6.8b §6.8.4.6 | Mapped by module name (ASSUMPTION-420) | TC-ENH-G-029, -027, -040 |
| G19-046 | Website and confidential Admin operating | Surface/audience/exposure table; routing decision; configuration; operational separation | Common core | Part 2.5; Part 3.2 §3.2.1.1; DEC-019 | Common core: see document 01/02 coverage |  |
| G19-X01 | Cross-interface acceptance and regressio | Anonymous Admin route → denied | Covered | TC-17-008, TC-21-010 | Mapped |  |
| G19-X02 | Cross-interface acceptance and regressio | External portal identity with staff endpoint → denied | Covered | TC-01-125, TC-17-008 | Mapped |  |
| G19-X03 | Cross-interface acceptance and regressio | Foreign tenant/issuer ID → uniform denied | Covered | TC-01-049 | Mapped |  |
| G19-X04 | Cross-interface acceptance and regressio | Expired token → denied | Covered | TC-01-062, TC-19-070 | Mapped |  |
| G19-X05 | Cross-interface acceptance and regressio | Unapproved draft/preview → no public content | Covered | TC-11-024, TC-19-028 | Mapped |  |
| G19-X06 | Cross-interface acceptance and regressio | Public cached payload has no internal fields | Covered | TC-19-044, TC-19-058 | Mapped |  |
| G19-X07 | Cross-interface acceptance and regressio | Scope switch clears private cache | Covered | TC-FLT-017, TC-17-003 | Mapped |  |
| G19-X08 | Cross-interface acceptance and regressio | Website enquiry → exactly one scoped workflow | Covered | TC-12-016, TC-21-054 | Mapped |  |
| G19-X09 | Cross-interface acceptance and regressio | Webhook replay → no duplicate receipt | Covered | TC-15-004, TC-NFR-005 | Mapped |  |
| G19-X10 | Cross-interface acceptance and regressio | Public AI prompt asks for private records → no disclosure | Covered | TC-AI-AG017-*, TC-10-036 | Mapped |  |
| G19-X11 | Cross-interface acceptance and regressio | Publish/unpublish reflects approved revision | Covered | TC-19-033, TC-11-022 | Mapped |  |
| G19-X12 | Cross-interface acceptance and regressio | Disabled client site returns safe unavailable | Not covered | — | New case | TC-ENH-G-042 |
| G19-X13 | Cross-interface acceptance and regressio | Keyboard, screen-reader names, contrast, mobile forms | Covered | T08; TC-17-067, TC-10-054 | Mapped |  |
| G19-060 | Executable test design | Deterministic UT; SIT with PostgreSQL/Celery/Valkey and sandbox contracts; browser UAT per journey and per UI item | Covered | §6.1.2; §6.1.13 | Mapped |  |
| G19-061 | Executable test design | Every case records ID, requirement, setup, input, action, expected, evidence, severity, result, owner, sign-off | Covered | §6.1.12.2 template; §6.1.5.4 EVR | Mapped |  |
| G19-062 | Executable test design | Every catalogued operation and screen: happy path + access negative; callbacks invalid signature/replay; consequential writes idempotency; regulated/finance blocked cases | Partially covered | CT-03/CT-05/CT-10 (Part 3.2 §3.2.5) without TC IDs | Operation-class TCs with IDs and per-operation data | TC-ENH-G-001…017; GAP-420 |
| G19-063 | Executable test design | No test represented as passed until execution evidence exists | Covered | §6.1.5.5 ladder; RBR-6 | Mapped |  |
| G19-064 | Executable test design | Acceptance journeys: AppNAI bid, MedMaarg pilot, EduVerse adult/school, OrganicSpec purchase/sales/service/training, campaigns, quotations, renewal; no investor records | Partially covered | UAT-PK-AN/MM/EV/OS/FIN; no marketing or renewal pack | UAT packs MKT and CS proposed | TC-ENH-G-032…034; GAP-422 |
| G19-065 | Testing exit criteria and traceability | Every catalogued operation and interface maps to an applicable test; critical cases pass; performance/recovery/security/accessibility evidence | Partially covered | Part 6.6 RTM (FR-level) | Source-test mapping CSV and operation mapping added | G_test_mapping.csv |
| G19-066 | Testing exit criteria and traceability | Vertical acceptance statements (AppNAI, MedMaarg, EduVerse, OrganicSpec, campaigns) | Covered | §6.1.13.3 packs (BRD §11 quotes) | Mapped |  |
| G19-067 | Implementation, verification and deliver | 624 cases Not run; every screen and operation has mapped acceptance or contract test | Partially covered | Part 6.6 | Mapping completed here | G_test_mapping.csv |
| G19-L01 | Test layer entry/exit gates | Unit: critical branch coverage ≥ 90% proposed; deterministic fixtures | Conflict | §6.1.9.6 (≥ 90% domain core); NFR-082; CONFLICT-421 | Resolution proposed | CONFLICT-421 |
| G19-L02 | Test layer entry/exit gates | SIT: reviewed contracts; scoped data; mock/sandbox; mandatory positive/negative/failure checks | Covered | §6.1.5.1 | Mapped |  |
| G19-L03 | Test layer entry/exit gates | UAT: integrated stable environment; business owner scenario; all flows accepted | Covered | §6.1.13.4–5 | Mapped |  |
| G19-L04 | Test layer entry/exit gates | Specialist: security, load, restore, rollback rehearsals | Covered | §6.1.14 | Mapped |  |
| G19-L05 | Test layer entry/exit gates | Release: QC evidence, approvals, training, monitoring; go-live record, digest, rollback readiness | Covered | Part 8.2; A090 | Mapped |  |
| G19-080 | Acceptance and evidence record | Responsible/reviewer; artifact evidence; decision Pending/Pass/Fail/approved N/A; remediation; business acceptance | Covered | §6.1.5.4 EVR | Mapped |  |
| G19-G01 | Test execution evidence and blocking rul | Contract fixture checks: 164 request, 164 invalid, 165 response examples validated offline | Partially covered | CT-04 example round-trip | Recommendation | RECOMMENDATION-424 |
| G19-G02 | Test execution evidence and blocking rul | Reference suite: 522 offline checks; product cases Not run | Not applicable | No reference starter in blueprint; ladder L-S rule applies | Noted |  |
| G19-G03 | Test execution evidence and blocking rul | Product test: implement mapped Unit/SIT/UAT; record expected/observed, state diffs, audit IDs, build hash | Covered | §6.1.5.4 | Mapped |  |
| G19-G04 | Test execution evidence and blocking rul | Quality gate: no unresolved critical/high privacy, authz, financial, regulated, deployment defect | Covered | §6.1.8.5 RBR-1…8 | Mapped |  |
| G19-G05 | Test execution evidence and blocking rul | Retest: defect → owner → fix → reproduce → regression → close with evidence | Covered | §6.1.8.1 | Mapped |  |
| OPT-01-01 | Optimization engineering and acceptance | Authentication and privileged sessions — zero revoked/wrong-audience/privileged bypass | Covered | TC-01-001…013, TC-01-062 | Mapped (common optimization core also reviewed by document 36 group) |  |
| OPT-02-01 | Optimization engineering and acceptance | Public website assets — LCP p75 ≤ 2.5 s, INP ≤ 200 ms, CLS ≤ 0.1 | Covered | NFR (Part 4.2); LT-02; T03 | Mapped (common optimization core also reviewed by document 36 group) |  |
| OPT-05-01 | Optimization engineering and acceptance | Transactional outbox — crash between commit and publish recovers | Covered | TC-01-069 | Mapped (common optimization core also reviewed by document 36 group) |  |
| OPT-10-01 | Optimization engineering and acceptance | Rules-first model routing — compare quality, latency and INR per task | Covered | Part 7.3; TC-AI | Mapped (common optimization core also reviewed by document 36 group) |  |
| OPT-17-01 | Optimization engineering and acceptance | Risk-based tests by operation; 100% mandatory regression; no pass without execution | Partially covered | §6.1.4; §6.1.12; ID not referenced | OPT crosswalk added (§6.8.5.1.5) |  |
| OPT-17-02 | Optimization engineering and acceptance | Automated evidence with integrity validation; missing evidence blocks | Partially covered | §6.1.5.4; RBR-6 | OPT crosswalk added (§6.8.5.1.5) | TC-ENH-G-039 |
| OPT-17-03 | Optimization engineering and acceptance | Traceability and orphan review to UI/API/data/workflow/test/optimization control | Partially covered | Part 6.6 (no operation/optimization-control columns) | OPT crosswalk added (§6.8.5.1.5) |  |
| OPT-17-04 | Optimization engineering and acceptance | Test efficiency: parallel, isolated data and clocks, flake measured, fail on external side effect | Covered | §6.1.6.4 outbound guard; §6.1.9.7 flaky policy | Mapped (common optimization core also reviewed by document 36 group) |  |
| OPT-18-01 | Optimization engineering and acceptance | Independent CI/CD; build once; promote digest; rollback per component | Covered | Part 4.3 | Mapped (common optimization core also reviewed by document 36 group) |  |
| G19-P01 | Implementation acceptance procedures | Test fixture reuse without leakage | Covered | §6.1.7.3 generation rules; §6.1.7.6 | Mapped |  |
| G19-P02 | Implementation acceptance procedures | AI-assisted coding quality: review generated code for licensing, scope, correctness, tests, secrets | Partially covered | §6.1.9.4 (tests only); TC-AI-AG034-002 | Added | TC-ENH-G-043 |
| G19-P03 | Implementation acceptance procedures | Product Unit/SIT/UAT coverage vs screen and operation inventories | Partially covered | Part 6.6 | Added | G_test_mapping.csv |
| G19-P04 | Implementation acceptance procedures | Fail-closed evidence inventory from immutable required-ID baseline; reject missing/extra/duplicate IDs, mandatory N/A | Partially covered | RBR-6; A090 fail closed | Added | TC-ENH-G-039 |
| G19-P05 | Implementation acceptance procedures | Evidence integrity: blank evidence, executor = reviewer after trim/case-fold, artifact hashes | Partially covered | EVR responsible ≠ reviewer | Added | TC-ENH-G-039 |
| G19-P06 | Implementation acceptance procedures | Combined preflight: 1,188 records in six groups incl. 21 mandatory KPIs; CTO + PO signed approval | Not covered | — | Added | TC-ENH-G-040; GAP-425 |
| G19-100 | Current scope — testing strategy | 10 shared scenarios (= SM-UX-SIT-X01…X10) | Partially covered | See X01…X10 rows | Mapped; 3 added | TC-ENH-G-030, -031, -035 |


### 6.8.3.2 Document 22 prose aspects (fixtures, rules, gates, evidence)


| ID | Section | Aspect | Status | Blueprint location | Action | New IDs |
|---|---|---|---|---|---|---|
| G22-001 | §1 | Purpose: proposed catalogue; all cases Not run; targets proposed interfaces | Covered | §6.1.5.5; GAP-167 now resolved | Catalogue received and reconciled |  |
| G22-002 | §1 | Test level table: 66 UT, 35 SIT-E2E, 302 SIT-ops, 66 SIT-module, 17 UAT journeys, 138 UAT screens = 624; +175 current-scope = 799 | Not covered | GAP-003/GAP-167 (catalogue was missing) | All 799 parsed and mapped | G_test_mapping.csv |
| G22-003 | §2 | Fixture T1 owned portfolio (S-A, S-M, S-E, S-O, S-05) | Partially covered | GSE-SYN §6.1.7.1 | Fixture crosswalk | ASSUMPTION-424 |
| G22-004 | §2 | Fixture T2 external client (S-X) and T3 forbidden look-alike tenant | Covered | GSE-SYN T2/T3; TC-01-X matrix | Crosswalk | ASSUMPTION-424 |
| G22-005 | §2 | Internal identities O1, D1/E1, L1, F1, A1, N1 with MFA/revoked | Partially covered | Persona fixtures (Part 6.5 §6.5.1.4) | Crosswalk | ASSUMPTION-424 |
| G22-006 | §2 | External identities X1, X2, X3, V1 (distinct token audience) | Partially covered | PP-03 portal profiles | Crosswalk | ASSUMPTION-424 |
| G22-007 | §2 | Publication fixtures R1/H1 approved, R2/H2 unapproved, verified/unknown host, two locales | Covered | TC-19-0xx fixtures | Crosswalk |  |
| G22-008 | §2 | Evidence fixtures: permitted snapshot, stale, conflicting, denied domain | Covered | EP-05 fixtures (F1–F6) | Crosswalk |  |
| G22-009 | §2 | Workflow fixtures: approved/cyclic DAG, fake clock, budget 10 units, provider 429/timeout/unknown, duplicates | Covered | §6.1.6.3 simulator; §6.1.6.5 clock | Crosswalk |  |
| G22-010 | §2 | Financial fixtures ₹1,000 split ₹600 + ₹400; wrong beneficiary/currency; duplicate callback; over-allocation; refund | Partially covered | EP-15 fixtures (different values) | Class TC uses source values | TC-ENH-G-011, TC-ENH-G-023 |
| G22-011 | §2 | Files and AI fixtures: benign PDF, oversized, malware test file, wrong-scope knowledge, prompt injection | Covered | TC-02-020; T14 red-team set | Mapped |  |
| G22-012 | §2 | Environment: isolated PostgreSQL/Valkey/Celery, test storage, SMTP sandbox, no live credentials, fake clock, fixed seed, trace IDs | Covered | §6.1.6 | Mapped |  |
| G22-013 | §2 | Preconditions for all cases: reset per case, never real recipient, record trace IDs, signed test callbacks | Covered | §6.1.6.4 outbound allowlist guard | Mapped |  |
| G22-014 | §3 | Tooling: pytest/pytest-django, Vitest/RTL, Playwright, AI regression, security/load/recovery suites | Covered | §6.1.9.2 (versions verify at implementation, as of 27 Nov 2026) | Mapped |  |
| G22-015 | §3 | Gates: no unresolved critical/high; 100% critical policy and state-transition cases; all ops/screens executed or dispositioned; ≥ 80% domain-service branch coverage | Conflict | §6.1.9.6; NFR-082 | Resolution proposed | CONFLICT-421 |
| G22-016 | §3 | Unit pass not a substitute for SIT/UAT; report skips, blocked providers, failed cases, untested routes | Partially covered | §6.1.10.3 readiness report | Untested-route and blocked-provider lines added to A090 report | TC-ENH-G-044 |
| G22-017 | §10 | Severity Critical/P0…Low/P3 with required disposition | Conflict | §6.1.8.2 S1–S4 + FP1–FP4 | Crosswalk | CONFLICT-423 |
| G22-018 | §10 | Execution record fields incl. status Not run/Pass/Fail/Blocked/N/A | Partially covered | EVR decision Pending/Pass/Fail/Approved N/A | Execution-status extension | GAP-423, RECOMMENDATION-422, TC-ENH-G-044 |
| G22-019 | §10 | Acceptance gates: Unit/SIT/UAT complete, security and financial gate, production authorization, with sign-off owners | Covered | §6.1.5.1–5.3; AP-01…AP-10 | Crosswalk |  |
| G22-020 | §10 | No real secrets, investor, patient or learner records in evidence; N/A must be approved | Covered | §6.1.7.6; EVR Approved N/A | Mapped |  |
| G22-021 | Execution and quality sign-off | Retain test IDs; Not run until executed; nonfunctional gates supplement | Covered | §6.1.5.5 | Mapped; SM-* IDs retained as aliases | RECOMMENDATION-423 |
| G22-022 | Implementation controls | Operation-specific positive/negative/boundary variants for all 302 SIT operations | Partially covered | CT-03/CT-05 generic | Class TCs with per-operation data | TC-ENH-G-001…017 |
| G22-023 | Implementation controls | Screen and journey negative/recovery variants for 17 journeys and 138 screens | Partially covered | Packs; per-screen states in Part 2.5 | Screen template | TC-ENH-G-036 |
| G22-024 | Implementation controls | 16 offline reference unit tests on the engineering starter are not product executions | Not applicable | No starter repository in the blueprint | Noted |  |
| G22-025 | Concrete fixtures | SM-CORE-01 quotation 2 × INR 150.00 at 10% = 270.00 | Covered | TC-13-016 | Mapped |  |
| G22-026 | Concrete fixtures | SM-CORE-02 bid expiry 2030-06-01 09:00 UTC at/after deadline | Covered | TC-14-022…024 | Mapped |  |
| G22-027 | Concrete fixtures | SM-CORE-03 order 2 kg; 1 kg twice same key; +2 kg rejected | Covered | TC-21-058, TC-14-089 | Mapped |  |
| G22-028 | Concrete fixtures | SM-CORE-04 EduVerse routing: external AI dev → AppNAI; school AI → EduVerse | Covered | TC-14-008, TC-14-002 | Mapped |  |
| G22-029 | Concrete fixtures | 164 candidate payloads and 165 response examples schema-validated offline | Partially covered | CT-04 | Recommendation | RECOMMENDATION-424 |
| G22-030 | Optimization | OPT-01-01, 02-01, 04-01, 05-01, 07-01, 08-01, 10-01, 11-01, 19-01 (common optimization core) | Common core | Document 36 group coverage | Not re-listed |  |
| G22-031 | Optimization | OPT-17-01…04 testing and QC controls | Partially covered | See G19 OPT rows | OPT crosswalk | TC-ENH-G-039 |
| G22-032 | Implementation acceptance | Authorization and error contract: wrong role, scope, malformed field, conflict, rate limit; no confidential fields in errors/logs | Covered | CT-05; TC-21-015; TC-NFR-004 | Mapped; class TCs add per-operation | TC-ENH-G-001…003 |
| G22-033 | Implementation acceptance | Structured output quality ≥ 99.5% schema-valid; invalid output never drives side effects | Covered | TC-AI-AG*-schema-valid; TC-04-040 | Mapped |  |
| G22-034 | Implementation acceptance | Reference test integrity: rerun reference/contract/optimization tests; skipped/failed separately | Partially covered | §6.1.10.1 metrics | Added to evidence preflight | TC-ENH-G-039 |
| G22-035 | Implementation acceptance | Evidence integrity and final acceptance (executor ≠ reviewer after trim/case-fold; hashes; signed approvals) | Partially covered | EVR | Added | TC-ENH-G-039 |
| G22-036 | Current scope | Release condition: approved screen/contract/entity decisions, expanded tests, QC and original acceptance evidence | Covered | A090; RBR-6 | Mapped |  |


### 6.8.3.3 Document 22 test records that are Partial or New (listed individually)

The 302 class-mapped operation cases are listed in §6.8.4.7 (all are Partial by definition and closed by TC-ENH-G-001…017).


| Source test | Level | Title | Gap found | Blueprint TCs kept | Added |
|---|---|---|---|---|---|
| SM-UT-005 | Unit | Support grant | Read-only support grant + write attempt not asserted explicitly | TC-15-087 TC-01-061 TC-08-166 | TC-ENH-G-018 |
| SM-UT-014 | Unit | Input normalization | Size limit covered; normalization and markup escaping not asserted | TC-07-072 TC-AI-AG017-008 | TC-ENH-G-019 |
| SM-UT-015 | Unit | Idempotency | Same-key replay covered; same key + changed body conflict not asserted | TC-04-004 TC-12-016 TC-03-061 | TC-ENH-G-020 |
| SM-UT-033 | Unit | Atomic reservation | Cap crossing covered; two concurrent reservations 7+7 of 10 not asserted | TC-08-008 TC-04-001 TC-NFR-014 | TC-ENH-G-021 |
| SM-UT-036 | Unit | Retry policy | Permanent 4xx and back-off cap covered; Retry-After honouring not asserted | TC-08-170 TC-21-043 | TC-ENH-G-022 |
| SM-UT-041 | Unit | Receipt identity | Currency/amount mismatch covered; beneficiary/issuer account mismatch not asserted | TC-15-040 TC-15-038 | TC-ENH-G-023 |
| SM-UT-045 | Unit | KPI computation | Potential vs commitment vs receipt with repeated receipt not asserted as one KPI case | TC-15-098 TC-15-074 TC-FLT-004 | TC-ENH-G-024 |
| SM-UT-050 | Unit | Need matching | Alias was 'unassigned' under DEC-094; cross-offering wellness need match with evidence + confidence added | TC-05-058 TC-02-035 | TC-ENH-G-041 |
| SM-UT-054 | Unit | Healthcare data segregation | Attachment scanning covered for onboarding; public enquiry upload of a patient report not asserted | TC-16-070 TC-16-018 | TC-ENH-G-025 |
| SM-UT-057 | Unit | Quote line calculation | Percentage discount covered; absolute INR discount before tax not modelled (CONFLICT-422) | TC-13-016 TC-13-017 | TC-ENH-G-026 |
| SM-UT-062 | Unit | Attribution | Attribution model applied once under conversion replay not asserted | TC-12-015 TC-12-082 | TC-ENH-G-027 |
| SM-UT-064 | Unit | Webinar capacity | Sequential capacity covered; concurrent last-seat race not asserted | TC-09-038 TC-09-046 | TC-ENH-G-028 |
| SM-SIT-F009 | SIT | Knowledge ingestion | Revocation of an approved document then re-query not asserted | TC-AI-AG001-005 TC-20-096 TC-01-114 TC-02-020 | TC-ENH-G-029 |
| SM-SIT-F013 | SIT | Budget concurrency | Competing reserve calls not asserted | TC-20-037 TC-04-028 TC-20-085 | TC-ENH-G-021 |
| SM-SIT-F029 | SIT | Campaign, ads and attribution | Attribution replay added | TC-12-082 TC-12-035 TC-12-015 | TC-ENH-G-027 |
| SM-SIT-F031 | SIT | Event and referral | Concurrent last seat added | TC-12-065 TC-09-033 TC-09-046 | TC-ENH-G-028 |
| SM-SIT-M003 | SIT | Knowledge document ingestion | Every answer cites approved version; revocation re-query added | TC-02-033 TC-02-031 TC-02-028 | TC-ENH-G-029 |
| SM-SIT-M043 | SIT | Landing pages and attribution | Landing pages and attribution: replay-once assertion added | TC-12-005 TC-12-082 TC-AI-AG018-002 | TC-ENH-G-027 |
| SM-SIT-M062 | SIT | End-to-end production release | End-to-end production release: combined evidence preflight added | TC-21-081 TC-NFR-013 TC-21-100 | TC-ENH-G-040 |
| SM-UAT-F014 | UAT | Marketing publishing and SEO | No marketing UAT pack; proposed UAT-PK-MKT | TC-AI-AG018-001 TC-19-028 TC-11-019 | TC-ENH-G-032 |
| SM-UAT-F015 | UAT | Campaign and attribution | E2E exists; business-owner UAT pack missing (UAT-PK-MKT) | TC-12-082 TC-12-083 | TC-ENH-G-033 |
| SM-UAT-F017 | UAT | Renewals and service | No customer-success UAT pack; proposed UAT-PK-CS | TC-16-029 TC-16-031 TC-16-071 | TC-ENH-G-034 |
| SM-UX-SIT-X01 | SIT | Scope and onboarding | 26th startup covered; 10 client tenants × 2 startups + role-switch reload not asserted | TC-01-054 TC-02-009 TC-FLT-011 | TC-ENH-G-030 |
| SM-UX-SIT-X07 | SIT | Shared closure state | ID consistency across CRM, quotation, order and portal projection not asserted | TC-19-089 TC-21-064 TC-07-013 | TC-ENH-G-031 |
| SM-UX-SIT-X10 | SIT | Accessibility and navigation | Keyboard/viewport covered per screen group; full route crawl with JS-error assertion missing | TC-17-067 TC-10-054 TC-17-009 | TC-ENH-G-035 |


### 6.8.3.4 Source operations with no Part 3.2 catalogue counterpart (GAP-421)

These operations are still fully covered by their operation-class TC and nearest functional TCs (§6.8.4.7). The catalogue gap itself is routed to the API catalogue owner (Part 3.2; source document 07 reconciliation) for an alias row or a candidate operation under DEC-015.


| Source test | Method and path | Purpose | Class TC | Functional TCs |
|---|---|---|---|---|
| SM-SIT-A005 | POST /auth/logout | Reuse session revocation | TC-ENH-G-001 | TC-01-012 TC-01-013 TC-NFR-001 |
| SM-SIT-A004 | POST /admin/users/{id}/roles | Reuse authorized role assignment | TC-ENH-G-003 | TC-07-017 TC-BRS-011 TC-BRS-005 |
| SM-SIT-A009 | PATCH /api/v1/admin/products/{id} | Version product changes | TC-ENH-G-003 | TC-01-010 TC-01-009 TC-FLT-021 |
| SM-SIT-A011 | POST /api/v1/admin/products/{id}/prices | Version approved pricing | TC-ENH-G-004 | TC-AI-AG017-012 TC-AI-AG014-003 TC-AI-AG030-002 |
| SM-SIT-A032 | PATCH /api/v1/admin/sources/{id} | Revise or expire source approval | TC-ENH-G-007 | TC-19-037 TC-15-103 TC-AU-AU007-001 |
| SM-SIT-A036 | GET /api/v1/admin/ai/eval-cases | List approved test fixtures | TC-ENH-G-006 | TC-19-088 TC-01-091 TC-19-087 |
| SM-SIT-A040 | POST /api/v1/admin/budgets/{id}/pause | Emergency pause controlled spend | TC-ENH-G-010 | TC-04-030 TC-AU-AU032-003 TC-12-045 |
| SM-SIT-A043 | POST /api/v1/admin/privacy/requests/{id}/resolve | Resolve after identity verification | TC-ENH-G-012 | TC-03-064 TC-21-031 TC-19-001 |
| SM-SIT-A044 | POST /api/v1/admin/retention-policies | Version data-class retention | TC-ENH-G-012 | TC-NFR-081 TC-NFR-076 TC-19-088 |
| SM-SIT-A065 | POST /api/v1/admin/signal-types | Configure signal taxonomy | TC-ENH-G-007 | TC-16-080 TC-16-075 TC-AI-AG021-001 |
| SM-SIT-A072 | POST /api/v1/admin/scoring-rules | Version scoring configuration | TC-ENH-G-003 | TC-AU-AU039-002 TC-20-005 TC-20-083 |
| SM-SIT-A074 | POST /api/v1/organizations/{id}/contacts/discover | Queue permitted contact discovery; Apollo optional | TC-ENH-G-007 | TC-BRS-005 TC-03-060 TC-06-037 |
| SM-SIT-A075 | POST /api/v1/admin/role-mappings | Update role hypotheses and mappings | TC-ENH-G-003 | TC-01-073 TC-NFR-018 TC-06-018 |
| SM-SIT-A077 | GET /api/v1/contacts/verification-queue | List verification work | TC-ENH-G-007 | TC-01-074 TC-AU-AU018-003 TC-15-029 |
| SM-SIT-A083 | POST /api/v1/admin/research-review-rules | Set approval thresholds | TC-ENH-G-007 | TC-19-088 TC-02-013 TC-AI-AG031-007 |
| SM-SIT-A084 | POST /api/v1/alerts/{id}/read | Mark alert read | TC-ENH-G-003 | TC-AU-AU042-002 TC-NFR-045 TC-NFR-091 |
| SM-SIT-A089 | GET /api/v1/admin/pipeline-stages | Read stage configuration | TC-ENH-G-002 | TC-08-092 TC-20-005 TC-20-083 |
| SM-SIT-A090 | POST /api/v1/admin/pipeline-stages | Version stage and assignment policies | TC-ENH-G-003 | TC-08-092 TC-07-017 TC-07-015 |
| SM-SIT-A101 | POST /api/v1/admin/workflows/{id}/resume | Resume after policy recheck | TC-ENH-G-010 | TC-AU-AU025-009 TC-18-109 TC-20-044 |
| SM-SIT-A102 | GET /api/v1/workflows/{id}/executions | Inspect step execution | TC-ENH-G-010 | TC-03-064 TC-12-033 TC-18-020 |
| SM-SIT-A104 | GET /api/v1/admin/message-templates | Read approved template inventory | TC-ENH-G-008 | TC-NFR-001 TC-01-111 TC-NFR-031 |
| SM-SIT-A105 | POST /api/v1/admin/message-templates | Version approved templates | TC-ENH-G-008 | TC-AI-AG020-002 TC-10-021 TC-18-057 |
| SM-SIT-A114 | GET /api/v1/threads/{id}/messages | Read conversation timeline | TC-ENH-G-008 | TC-10-026 TC-07-054 TC-08-080 |
| SM-SIT-A115 | POST /api/v1/threads/{id}/handoff | Route uncertain response to human | TC-ENH-G-008 | TC-10-026 TC-16-002 TC-AI-AG031-002 |
| SM-SIT-A125 | POST /api/v1/admin/calendar-links | Configure authorized calendar | TC-ENH-G-003 | TC-BRS-011 TC-09-021 TC-06-046 |
| SM-SIT-A130 | GET /api/v1/admin/whatsapp/accounts | List WABA and template metadata | TC-ENH-G-008 | TC-08-184 TC-10-006 TC-BRS-001 |
| SM-SIT-A135 | GET /api/v1/whatsapp/conversations | Read WhatsApp threads | TC-ENH-G-008 | TC-10-026 TC-10-027 TC-18-047 |
| SM-SIT-A138 | POST /api/v1/admin/chat/settings | Configure approved FAQ and retention | TC-ENH-G-012 | TC-10-051 TC-10-059 TC-NFR-081 |
| SM-SIT-A149 | PATCH /api/v1/content/{id} | Create revised version | TC-ENH-G-003 | TC-09-031 TC-AU-AU014-003 TC-02-001 |
| SM-SIT-A159 | POST /api/v1/seo/audit/run | Queue permitted audit | TC-ENH-G-003 | TC-AI-AG018-004 TC-11-064 TC-AI-AG009-007 |
| SM-SIT-A163 | POST /api/v1/landing-pages/{id}/publish | Publish approved page | TC-ENH-G-005 | TC-AU-AU029-001 TC-19-035 TC-18-034 |
| SM-SIT-A175 | GET /api/v1/events/business | List business events | TC-ENH-G-002 | TC-AU-AU021-002 TC-AU-AU021-001 TC-18-060 |
| SM-SIT-A176 | POST /api/v1/events/business | Create event | TC-ENH-G-003 | TC-AU-AU021-001 TC-AU-AU021-002 TC-09-031 |
| SM-SIT-A180 | POST /api/v1/admin/events/{id}/settings | Set reminder policy | TC-ENH-G-003 | TC-17-049 TC-16-034 TC-09-043 |
| SM-SIT-A191 | GET /api/v1/deals/{id}/objections | Read negotiation state | TC-ENH-G-006 | TC-AI-AG021-001 TC-13-068 TC-AI-AG014-005 |
| SM-SIT-A206 | POST /api/v1/payments/{id}/reconcile | Reconcile payment evidence | TC-ENH-G-011 | TC-AU-AU040-003 TC-20-046 TC-18-070 |
| SM-SIT-A216 | POST /api/v1/partner-pilots | Create pilot record | TC-ENH-G-003 | TC-16-055 TC-NFR-060 TC-16-006 |
| SM-SIT-A219 | POST /api/v1/admin/renewal-policies | Set approved renewal reminder policy | TC-ENH-G-004 | TC-16-035 TC-20-051 TC-16-034 |
| SM-SIT-A224 | POST /api/v1/admin/kpi-definitions | Version KPI definitions | TC-ENH-G-003 | TC-15-079 TC-FLT-020 TC-19-088 |
| SM-SIT-A226 | GET /api/v1/admin/evals/results | Read evaluation results | TC-ENH-G-006 | TC-05-004 TC-17-062 TC-17-060 |
| SM-SIT-A228 | POST /api/v1/admin/competitor-sources | Register approved monitor | TC-ENH-G-007 | TC-NFR-029 TC-05-068 TC-05-072 |
| SM-SIT-A230 | POST /api/v1/admin/forecast-settings | Version model assumptions | TC-ENH-G-003 | TC-17-044 TC-19-088 TC-17-080 |
| SM-SIT-A236 | GET /api/v1/insurance/pilots | Read organization-level insurance pilots | TC-ENH-G-007 | TC-16-053 TC-16-056 TC-16-052 |
| SM-SIT-A253 | POST /api/v1/sales/memberships | Invite/revoke employee | TC-ENH-G-001 | TC-18-090 TC-16-054 TC-AU-AU030-001 |
| SM-SIT-A257 | POST /api/v1/sales/templates/{id}/control | Validate, approve, apply or retire | TC-ENH-G-004 | TC-18-090 TC-19-036 TC-16-068 |
| SM-SIT-A260 | POST /api/v1/sales/domains/{id}/control | Verify DNS/TLS or disable | TC-ENH-G-003 | TC-19-001 TC-05-074 TC-NFR-069 |
| SM-SIT-A261 | GET /api/v1/sales/service-plans | List plans | TC-ENH-G-002 | TC-18-090 TC-AI-AG016-001 TC-AU-AU030-001 |
| SM-SIT-A262 | POST /api/v1/sales/service-plans | Approve rate revision | TC-ENH-G-004 | TC-13-052 TC-18-090 TC-AU-AU030-001 |
| SM-SIT-A263 | GET /api/v1/sales/service-subscriptions | List subscriptions | TC-ENH-G-002 | TC-18-090 TC-AU-AU030-001 TC-20-004 |
| SM-SIT-A264 | POST /api/v1/sales/service-subscriptions/{id}/control | Start/change/suspend/cancel | TC-ENH-G-003 | TC-18-090 TC-20-048 TC-20-093 |
| SM-SIT-A266 | POST /api/v1/sales/service-invoices/{id}/reconcile | Reconcile service receipt | TC-ENH-G-011 | TC-AU-AU040-003 TC-18-070 TC-AU-AU042-003 |
| SM-SIT-A267 | GET /api/v1/sales/usage-charges | List charge ledger | TC-ENH-G-011 | TC-18-090 TC-20-024 TC-AU-AU030-001 |
| SM-SIT-A268 | POST /api/v1/sales/usage-charges/{id}/adjust | Append approved credit | TC-ENH-G-011 | TC-20-045 TC-20-032 TC-18-090 |
| SM-SIT-A269 | GET /api/v1/sales/action-plans | List plans | TC-ENH-G-010 | TC-18-090 TC-AI-AG016-001 TC-AU-AU030-001 |
| SM-SIT-A270 | POST /api/v1/sales/action-plans | Generate or dry-run | TC-ENH-G-010 | TC-18-090 TC-AU-AU030-001 TC-20-004 |
| SM-SIT-A271 | POST /api/v1/sales/action-plans/{id}/control | Approve/start/pause/stop | TC-ENH-G-010 | TC-AU-AU032-003 TC-13-052 TC-18-090 |
| SM-SIT-A272 | GET /api/v1/sales/data-transfers | List scoped jobs | TC-ENH-G-012 | TC-18-090 TC-AU-AU030-001 TC-AU-AU016-004 |
| SM-SIT-A273 | POST /api/v1/sales/data-transfers | Create intent | TC-ENH-G-012 | TC-18-090 TC-AU-AU030-001 TC-20-004 |
| SM-SIT-A274 | POST /api/v1/sales/data-transfers/{id}/complete | Validate artifact | TC-ENH-G-012 | TC-18-090 TC-AU-AU030-001 TC-20-004 |
| SM-SIT-A275 | POST /api/v1/sales/data-transfers/{id}/control | Approve/cancel/expire | TC-ENH-G-012 | TC-13-052 TC-18-090 TC-05-012 |
| SM-SIT-A276 | GET /api/v1/sales/data-transfers/{id}/download | Export link | TC-ENH-G-012 | TC-15-103 TC-03-070 TC-20-068 |
| SM-SIT-A280 | POST /api/v1/sales/bids/{id}/control | Approve, submit, withdraw or record award | TC-ENH-G-014 | TC-14-088 TC-14-005 TC-13-052 |
| SM-SIT-A284 | POST /api/v1/sales/orders/{id}/control | Approve/issue/cancel/complete | TC-ENH-G-013 | TC-13-052 TC-18-090 TC-20-041 |
| SM-SIT-A285 | POST /api/v1/sales/orders/{id}/milestones | Record actual fulfillment | TC-ENH-G-013 | TC-18-090 TC-AU-AU030-001 TC-20-004 |
| SM-SIT-A286 | POST /api/v1/sales/milestones/{id}/accept | Accept/dispute delivery | TC-ENH-G-013 | TC-14-085 TC-14-076 TC-06-037 |
| SM-SIT-A288 | PATCH /api/v1/sales/notifications/{id} | Mark own notification read/archive | TC-ENH-G-003 | TC-AU-AU027-002 TC-18-090 TC-01-116 |
| SM-SIT-A290 | GET /api/v1/commercial/admin/website/pages | List startup-owned website drafts and publications. | TC-ENH-G-005 | TC-01-003 TC-21-079 TC-11-036 |
| SM-SIT-A291 | POST /api/v1/commercial/admin/website/pages | Create immutable draft or edit by creating next draft revision. | TC-ENH-G-005 | TC-19-034 TC-16-025 TC-11-072 |
| SM-SIT-A292 | POST /api/v1/commercial/admin/website/pages/{id}/control | Validate/preview/submit/approve/publish/unpublish or rollback approved | TC-ENH-G-005 | TC-21-079 TC-19-025 TC-AU-AU029-001 |
| SM-SIT-A293 | POST /api/v1/commercial/admin/external-grants | Issue scoped external invitation for verified counterparty; no staff m | TC-ENH-G-009 | TC-19-045 TC-01-026 TC-01-044 |
| SM-SIT-A294 | POST /api/v1/commercial/admin/external-grants/{id}/control | Revoke, expire or rotate an external grant without changing staff perm | TC-ENH-G-009 | TC-19-006 TC-19-070 TC-01-065 |
| SM-SIT-A122 | GET /api/v1/public/meeting-slots/{token} | Read scoped available slots | TC-ENH-G-002 | TC-AI-AG017-009 TC-10-044 TC-09-004 |
| SM-SIT-A203 | GET /api/v1/public/payment-status/{token} | Read scoped payment status | TC-ENH-G-009 | TC-15-070 TC-AI-AG017-009 TC-10-044 |
| SM-SIT-A295 | POST /api/v1/commercial/portal/external-grants/accept | Redeem a one-time invitation after identity verification; bind grant t | TC-ENH-G-009 | TC-03-064 TC-17-008 TC-15-027 |
| SM-SIT-A296 | POST /api/v1/commercial/portal/documents | Request upload for a specifically granted onboarding or project reques | TC-ENH-G-009 | TC-14-084 TC-20-015 TC-19-088 |
| SM-SIT-A297 | POST /api/v1/commercial/portal/documents/{id}/complete | Complete own quarantined document upload and enqueue scan. | TC-ENH-G-009 | TC-20-015 TC-15-046 TC-16-016 |
| SM-SIT-A298 | GET /api/v1/commercial/portal/overview | Own customer dashboard with authorized lead, agreement, order and onbo | TC-ENH-G-009 | TC-BRS-003 TC-19-089 TC-16-004 |
| SM-SIT-A299 | GET /api/v1/commercial/portal/quotations/{id} | Read approved recipient-specific quote/proposal. | TC-ENH-G-009 | TC-21-064 TC-BRS-004 TC-19-088 |
| SM-SIT-A300 | POST /api/v1/commercial/portal/quotations/{id}/respond | Accept or request revision of an approved quotation; creates internal | TC-ENH-G-009 | TC-BRS-004 TC-13-012 TC-FLT-039 |
| SM-SIT-A302 | POST /api/v1/commercial/portal/requests | Own support, feedback, renewal or privacy request with typed kind. | TC-ENH-G-009 | TC-AU-AU020-003 TC-20-051 TC-03-071 |
| SM-SIT-A207 | POST /api/v1/invoices/{id}/payment-link | Create scoped payment link through approved gateway | TC-ENH-G-011 | TC-13-062 TC-20-051 TC-15-010 |


---

### Quality gate: Part 6.8a

| # | Check | Result | Notes |
|---|---|---|---|
| 1 | Every requirement traced to a source | Pass | Every aspect row cites its document section and blueprint location |
| 2 | Assumptions/gaps/conflicts tagged and logged | Pass | Tags referenced here are registered in Part 6.8c §6.8.8 |
| 3 | IDs unique and consistent | Pass | G19-/G22- aspect IDs are local to the coverage CSV; TC IDs resolved against the 2,912 defined TCs (script check: 0 undefined) |
| 4 | No requirement lacks a test | Pass | 799/799 source tests mapped |
| 5 | Negative, edge, security, accessibility | Pass | See Part 6.8c |
| 6 | Agents: guardrail, fallback, KPI, cost | N/A | No agents defined in this part |
| 7 | Time-sensitive facts flagged | Pass | Tooling marked verify (as of 27 Nov 2026) |
| 8 | No restricted data to free-tier models | Pass | Not applicable to the register; Part 6.8c cases assert DEC-007 where relevant |
| 9 | Consistent with earlier parts | Pass, with findings | CONFLICT-420…424 and GAP-420…425 (Part 6.8c) |

**Status: Part 6 Batch 6.8a complete. 923 aspects registered for documents 19 and 22; every Partial, Not covered and Conflict item listed individually.**
