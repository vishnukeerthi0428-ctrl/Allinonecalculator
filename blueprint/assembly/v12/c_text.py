# -*- coding: utf-8 -*-
"""Narrative sections for Part 11.3 (group R3a, letter C)."""
import collections, statistics, json

def _svcs(): return [f"{i:02d}" for i in range(1, 21)]

def stats(D, M, ROWS, FR, TC, US, TC_LAST):
    S = {}
    S['wf'] = len(D); S['steps'] = sum(len(d['steps']) for d in D.values())
    S['dto'] = sum(len(d['dto']) for d in D.values()); S['dto_svc'] = sum(len(D[f'SM-SVC-{s}-WF01']['dto']) for s in _svcs())
    S['wft'] = sum(len(d['wf_tests']) for d in D.values()); S['stt'] = sum(len(d['step_tests']) for d in D.values())
    S['risk'] = collections.Counter(d['brd09']['risk'][:2] for d in D.values())
    S['st'] = collections.Counter(M.W[w]['st'] for w in D)
    S['before'] = collections.Counter(r[5] for r in ROWS); S['after'] = collections.Counter(r[9] for r in ROWS)
    S['rows'] = len(ROWS); S['tc_last'] = TC_LAST
    S['flows'] = sum(1 for w in D if M.W[w]['flow'])
    S['fail'] = collections.Counter(x['failure'].split(' ')[0] for d in D.values() for x in d['steps'])
    S['cls'] = collections.Counter(t['class'] for d in D.values() for t in d['step_tests'])
    S['exec'] = None
    return S

def counts(S):
    return (f"**Counts in this part (files a–c).** {S['wf']} V12 workflows (SM-SVC-01-WF01…SM-SVC-20-WF04) · {S['steps']} step contracts · {S['dto']} DTO field rows "
            f"({S['dto_svc']} distinct per service) · {S['wft']} workflow acceptance tests + {S['stt']} step tests from FSD ch33 mapped to TC-V12-C-031…{S['tc_last']:03d} · 30 engine tests TC-V12-C-001…030 · "
            f"92 requirements FR-V12-C-001…092 · 22 stories US-<EP>-YC01…YC22 · {S['flows']} workflow flowcharts + 4 engine diagrams · 15 decisions DEC-540…554 · 3 ADRs ADR-190…192 · tags 796–813 · "
            f"{S['rows']:,} coverage aspects in `final/coverage_v12/C_coverage.csv`.")

def story(s, us, d, m, ws, FR):
    name = d['wb']['Automation service name']
    frs = ', '.join(FR[w] for w in ws)
    risky = [w for w in ws if d and True]
    g = [f"**{us} — {name}.** As {m['actors'].split(',')[0].split('(')[0].strip()}, I want the four {d['wb']['Automation ID']} workflows to run as typed, policy-checked contracts on the universal engine, so that {d['wb']['Business objective'][0].lower()+d['wb']['Business objective'][1:]} without any unauthorized effect. Requirements: {frs}. Epic EP-{m['epic']}.\n",
         "```gherkin",
         f"Feature: {d['wb']['Automation ID']} {name} contract conformance",
         "  Background:",
         f"    Given tenant T1 startup S1 holds an active {d['wb']['Automation ID']} entitlement with a monthly allowance",
         "    And the workflow schema version is pinned on each run",
         "  Scenario: Valid input produces the expected artefact",
         f"    When a requester starts {ws[0]} with a DTO valid against urn:sm:dto:{ws[0]}:v2",
         "    Then every step records class, input reference, output reference, state and evidence",
         f"    And the result validates against the output schema",
         "  Scenario: Invalid or foreign input is rejected before any step",
         "    When the DTO has an unknown field or a reference from tenant T2",
         "    Then the API returns 422 or an indistinguishable 404 and no StepRun exists",
         "  Scenario: Entitlement revoked after enqueue",
         "    Given a run is queued",
         "    When the entitlement is revoked",
         "    Then the dispatch-time recheck blocks the next step and releases the reservation",
         "```", ""]
    return "\n".join(g)

def wf_intro():
    return """**How to read each workflow block.** (1) A header table restates every V12 field literally (BRD ch09 row, FSD ch12 specification table, workbook 50-field row, FSD ch13 step classes, FSD ch40 trace, cost model) and adds the blueprint mapping, autonomy, KPI formulas, SLA and rules. (2) The step table lists every V12 step ID with its executor, output/validation and failure route, the blueprint state the failure maps to (DEC-541), the blueprint component that executes it, and the step test (V12 `…-STEP-nn-TC` → TC-V12-C-###). (3) Representative or complex workflows (all R3 with an external effect, the R2 dispatch workflows and the net-new WF04s) carry a Mermaid flowchart. (4) The test table maps every V12 acceptance ID (TC-POS, INPUT, SCOPE, ENT, DUP, QUALITY, BUDGET, RECOVERY and, for R2/R3, APPROVAL and EFFECT) to a TC-V12-C ID with the blueprint assertion that makes it executable. Each service opens with its SKU block, the DTO table (Appendix B schema constraint and blueprint column) and its user story with Gherkin.

"""

def file_a(D, M, ROWS, FR, TC, US, S):
    o = []
    o.append("""## 11.3.1 Material reviewed

| File (V12, 28 Nov 2026) | Size | Sections used | Purpose | Pattern | Aspects |
|---|---|---|---|---|---|
| `BRD/09_Business_Workflow_Catalogue_156_Workflo.txt` | 41.7 KB, 1,307 lines | V10 REC-05/REC-08, V6 MT-34, SM-SVC-01…20 tables (80 rows) | Business outcome, input → output, workflow KPI pair, risk class per workflow | `[TABLE]` 5 columns × 4 rows per service | 80 × 5 + 3 |
| `FSD/12_Executable_Workflow_Specification_156_W.txt` | 834 KB, 17,495 lines (lines 787–9,110 for SVC-01…20) | V10 controls, historical group index, V6 MT-29, V5 FL-02/03/07/08/11/12/13/14, V4 guard contract (8 controls), workflow-to-channel reconciliation, 80 workflow entries, candidate UI input contracts | Executable contract: 11-field specification, DTO table, step table, common contract, acceptance IDs | 3 tables per workflow (spec 11 rows; DTO 8–10 rows; steps 2–4 rows) | 80 × (11 + 2–4 steps + 8–10 tests) + 676 DTO rows |
| `FSD/AP_Appendix_B_Workflow_DTO_JSON_Schemas_156.txt` | 152 KB | 80 of 156 one-line JSON Schemas | `$id urn:sm:dto:<workflow>:v2`, `$defs.input` / `$defs.output` | JSON Schema 2020-12 | 80 schemas, 20 distinct |
| `FSD/13_Workflow_Step_Trigger_Event_Registry.txt` | 30 KB | V5 ST-04, FL-01, FL-05, FL-10; optimization mapping rows (80) | Step classes, control links | Table | 80 + 4 |
| `FSD/33_Unit_SIT_UAT_AI_Test_Specifications.txt` | (chapter) | §33.3 step tests (286 of 517) and workflow scenarios (682 of 1,342) | Test IDs and assertions | Table | 968 |
| `FSD/40_Master_Traceability…txt` | (chapter) | Workflow trace rows (80); FSD-POL-V6-PRECHECK and -ARTIFACT | Engine, AGT agent, policy, tests | Table + canonical text | 80 + 2 |
| `FSD/15_AI_Agent_Registry_Orchestration.txt` | 6.4 KB | AGT-01…15 | Agent roles, allowed and never-allowed tools | Table | 15 |
| `BRD/18_AI_Automation_Authority_Business_Govern.txt` | 11.7 KB | Authority table L0–L4, R3 default L2 | Authority model | Table | 6 |
| Workbook `…39_Services_156_Workflows(1)_csv/` | 1.3 MB (12 sheets) | `Workflow_Catalog.csv` (80 × 50 fields), `Acceptance_Tests.csv` (80 AT01), `Cost_Model.csv` (80), `Service_Index.csv` and `Entitlement_Rules.csv` (20) | Source workbook | CSV | 80 × 50 + 240 |

**Method.** Every row was parsed programmatically by `assembly/v12/c_parse_workflows.py` (output `assembly/v12/c_workflows.json`) and cross-checked: step counts agree across FSD ch12 step tables, the channel reconciliation table, FSD ch13 and the workbook (286 steps); DTO field sets equal the Appendix B schema properties for all 80 workflows; acceptance IDs in ch12 equal the ch33 scenario rows (682); titles agree between BRD ch09 and FSD ch12. Zero parsing mismatches. The document is generated by `assembly/v12/c_build_part.py` from the parsed data plus the hand-authored mapping `assembly/v12/c_mapping.py` and narrative `assembly/v12/c_text.py`, so every V12 value is carried literally.

**Shape of the material.** """ + f"Risk classes: R0 internal analysis/draft {S['risk']['R0']}, R1 scoped state write or safety control {S['risk']['R1']}, R2 external communication/provider/access write {S['risk']['R2']}, R3 financial/legal/commitment {S['risk']['R3']}. Step classes (FSD ch33): " + ", ".join(f"{k} {v}" for k, v in S['cls'].most_common()) + ". Failure routes: " + ", ".join(f"{k} {v}" for k, v in S['fail'].most_common()) + ".\n")

    o.append(f"""## 11.3.2 Coverage summary

The blueprint already has the **behaviour** of most of these workflows (universal engine Part 2.2 §2.6, WF-01…39, AG-001…080, AU-001…119, BRL catalogue), but it has none of the V12 **executable contract layer**: SKU-level workflow IDs, typed DTOs, step IDs and classes, failure codes, risk classes R0–R3, per-workflow KPIs, per-invocation cost and the TC-POS…EFFECT acceptance taxonomy. Capability status per workflow before this part: **Covered {S['st']['C']}**, **Partially covered {S['st']['P']}**, **Not covered {S['st']['N']}** (the not-covered ones are all new WF04 capabilities or community response).

| Status | Before (aspects) | After (aspects) |
|---|---|---|
""" + "\n".join(f"| {k} | {S['before'].get(k,0):,} | {S['after'].get(k,0):,} |" for k in ['Covered','Partially covered','Not covered','Conflict','Matched','Pending Founder decision']) + f"""
| **Total** | **{S['rows']:,}** | **{S['rows']:,}** |

Pending Founder decision: the authority aspects of the 12 R2 and 9 R3 workflows (V12 allows an L3 “separately approved bounded mandate” path that DEC-064 and the safety invariants do not), and SM-SVC-19-WF03 step 04 (bid submission, DEC-053). Every other aspect is Matched.

| Workflow capability status | Count | Workflows |
|---|---|---|
| Covered (contract layer added) | {S['st']['C']} | all others |
| Partially covered (enhanced here) | {S['st']['P']} | {', '.join(w[7:] for w in D if M.W[w]['st']=='P')} |
| Not covered (specified here) | {S['st']['N']} | {', '.join(w[7:] for w in D if M.W[w]['st']=='N')} |
""")
    # register
    o.append("""## 11.3.3 Detailed register

Every aspect is listed individually in `final/coverage_v12/C_coverage.csv` (columns doc, chapter, section, aspect_id, aspect_summary, status_before, blueprint_location, action, new_ids, status_after). In this document each workflow's aspects are enumerated individually in its block in §11.3.5.10 (header fields, every step, every test); the table below is the per-workflow register.

| Workflow | Title | Risk | Capability before | Aspects | Not covered / conflict before | Blueprint location | Action | New IDs | After |
|---|---|---|---|---|---|---|---|---|---|""")
    by = collections.defaultdict(list)
    for r in ROWS:
        for w in D:
            if w in r[2] or r[3].startswith(w) or r[3].startswith(w.replace('SM-SVC-','C-SVC')) or r[3] == f'urn:sm:dto:{w}:v2':
                by[w].append(r); break
    for w, d in D.items():
        rs = by[w]; nc = sum(1 for r in rs if r[5] in ('Not covered','Conflict')); m = M.W[w]
        after = 'Pending Founder (authority)' if d['brd09']['risk'][:2] in ('R2','R3') else 'Matched'
        o.append(f"| {w} | {d['title']} | {d['brd09']['risk'][:2]} | {M and {'C':'Covered','P':'Partially','N':'Not covered'}[m['st']]} | {len(rs)} | {nc} | {m['bp'].replace('|','/')} | {'Contract layer' if m['st']=='C' else m['gap'].replace('|','/')} | {FR[w]} | {after} |")
    o.append("")
    # catalogue reconciliation
    o.append("""## 11.3.4 Catalogue reconciliation

### 11.3.4.1 Counts

| Item | V12 source count (SVC-01…20) | Check | Blueprint after this part |
|---|---|---|---|
| Services (SKUs) | 20 of 39 | Service_Index = Entitlement_Rules = ch09 headings | 20 service blocks; SKU commercial model is group B (Part 11.2) |
| Workflows | 80 of 156 | BRD ch09 = FSD ch12 = workbook = Appendix B = ch13 = ch40 | 80 workflow blocks, FR-V12-C-013…092 |
""" + f"""| Steps | {S['steps']} of 517 | ch12 step tables = ch12 reconciliation = ch13 = workbook “Workflow steps” | {S['steps']} step rows with blueprint component and state |
| DTO fields | {S['dto']} rows ({S['dto_svc']} per service) | ch12 DTO tables = Appendix B properties | 20 DTO tables |
| Workflow acceptance tests | {S['wft']} (80 × 8 + 21 × 2) | ch12 acceptance IDs = ch33 rows | TC-V12-C mapped |
| Step tests | {S['stt']} | ch33 §33.3 = step tables | TC-V12-C mapped |
| Original acceptance (AT01) | 80 | workbook Acceptance_Tests | superseded by TC-POS mapping; still “not run” |
| Cost rows | 80 | workbook Cost_Model | illustrative cost per workflow |
| Agents (AGT) | 15 (AGT-01…15) | ch15 = ch40 trace | mapped to AG-003…AG-066 (no new agent) |
| Engines (V12 shared) | 9 of 15 used | Shared_Engines | mapped to blueprint modules |
""" + """
### 11.3.4.2 V12 agent (AGT) → blueprint agent crosswalk

V12 FSD ch15 gives each AGT role “scoped read, retrieval (own tenant), draft/score output” and never “send, publish, spend, change live state, read other tenants”. This equals the blueprint rule that agents draft, classify, extract and match and never act (BRL-AI-07; Part 7.2 tool registry). No new agent card is needed; the AGT ID becomes an alias on the mapped AgentDefinition (`ai_agent_definition.external_alias`) so traces show both IDs (DEC-540).

| AGT | V12 role | Workflows | Blueprint agents |
|---|---|---|---|""")
    agt = collections.defaultdict(list)
    for w, d in D.items(): agt[d['ch40']['Agent']].append(w[7:])
    roles = {}
    for w, d in D.items(): roles.setdefault(d['ch40']['Agent'], d['wb']['AI agent responsibilities'])
    for k in sorted(agt):
        o.append(f"| {k} | {roles[k]} | {', '.join(agt[k])} | {M.AGT[k]} |")
    o.append("""
### 11.3.4.3 Service → blueprint workflow crosswalk

The V12 SM-SVC workflows are **SKU-level executable contracts**; the blueprint WF-01…39 are **end-to-end business flows** that chain several contracts. Both are kept: a WF-xx step that performs the work of an SM-SVC workflow invokes that contract through the engine (DEC-540). The historical use-case groups of FSD ch12 V10 (20 groups × 5 entries) map as: Onboarding → WF-01/§2.22.4; Research, Market intelligence → SM-SVC-01/02 (WF-02); Contact intelligence → SM-SVC-03 (WF-03); Qualification → SM-SVC-04; Outreach, Follow-up → SM-SVC-06/07/08 (WF-06/07/27); Conversation → SM-SVC-09; Meetings → SM-SVC-10; Content marketing, Digital marketing → SM-SVC-11…14 (WF-05); Website, Conversion → SM-SVC-15/16 (WF-04); Documents → SM-SVC-17/18 (WF-09); Financial → SM-SVC-20 (WF-10/11) and SM-SVC-21 (group D); Customer lifecycle → SM-SVC-22/23 (group D); SaaS, AI operations, Reliability, Optimization → engine (this §11.3.5) and group E. The Part 9.4 catalogue should list, per WF-xx, the SM-SVC contracts it invokes [RECOMMENDATION-808].

""")
    o.append(mm_svcmap(D, M, 1, 10)); o.append(mm_svcmap(D, M, 11, 20))
    o.append(file_a_engine(D, M, S, FR, TC))
    return "\n".join(o)

def mm_svcmap(D, M, a, b):
    L = ["```mermaid", "flowchart TD"]
    wfset = {}
    for i in range(a, b + 1):
        s = f"{i:02d}"; d = D[f'SM-SVC-{s}-WF01']
        L.append(f'  S{s}["SM-SVC-{s}<br/>{d["wb"]["Automation service name"].replace("&","and")[:38]}"]')
        for wf in __import__('re').findall(r'WF-\d\d', M.SVC[s]['bpwf']):
            wfset.setdefault(wf, 1)
            L.append(f'  S{s} --> {wf.replace("-","")}')
    titles = {'WF-02':'Market discovery','WF-03':'Professional contacts','WF-04':'Inbound acquisition','WF-05':'Content and campaign','WF-06':'Outreach and replies','WF-07':'Follow-up and meetings','WF-08':'Project bid','WF-09':'Proposal, quote, negotiation','WF-10':'Order and fulfilment','WF-11':'Commercial closure','WF-16':'Predictive model lifecycle','WF-17':'Deal-risk early warning','WF-18':'RFP co-pilot','WF-20':'Experiment lifecycle','WF-23':'WhatsApp concierge','WF-26':'Lead route and SLA','WF-27':'Multichannel cadence','WF-28':'Deal room and guarded quote','WF-29':'Pipeline inspection','WF-30':'Partner referral and co-sell'}
    for wf in wfset:
        L.insert(2, f'  {wf.replace("-","")}["{wf} {titles.get(wf,"")}"]')
    L.append("```\n")
    return "\n".join(L)

def file_a_engine(D, M, S, FR, TC):
    return r"""## 11.3.5 Enhancements

### 11.3.5.1 Engine-level requirements (FR-V12-C-001…012)

| FR | Requirement | Source (V12) | Blueprint basis | Rules | Tests |
|---|---|---|---|---|---|
| FR-V12-C-001 | **Workflow contract registry.** Register the 80 workflows SM-SVC-01-WF01…SM-SVC-20-WF04 (group D registers the other 76) in `aut_workflow` with the V12 ID as the stable key, title, service (SKU) ID, workflow version (2.0-target for WF01–03, 1.0-target for WF04), schema URN, ordered step IDs with class, risk class R0–R3, approval gate text, meter unit, KPI definitions and acceptance IDs. Run creation snapshots the definition (immutable); an unapproved version is rejected. | FSD ch13 FL-01; ch12 V6; BRD ch09 MT-34 | ENT-159/160 Workflow/Revision; BRL-AUT-03; WQG-01…12 | Definition count for these services stays 80 whatever the number of tenants or templates | TC-V12-C-001, -002, -011 |
| FR-V12-C-002 | **BusinessContext and event envelope.** Every run carries `BusinessContext` {tenant, organization, company/startup, division, brand, offering, target market, account, campaign/configuration, SKU, workflow ID and revision, actor, policy snapshot}. Trigger events use the V12 envelope `event_id, tenant_id, startup_id, service_id, workflow_revision, input_ref, occurred_at, correlation_id`; scope fields are taken from membership, never from the payload (E-1). | FSD ch12 V6; workbook “Event and trigger schema” | Part 3.4 §3.4.5.2 D canonical inbound event; E-1 | Mismatched scope → reject (403/404) | TC-V12-C-003, -004 |
| FR-V12-C-003 | **Run, result and approval contract.** V12 API-V2-RUN → trigger/start (API-460/462 for events; proposed `POST ~/admin/workflows/{workflow_id}/runs` with DTO body, 202 + run reference) [GAP-804]; API-V2-RESULT → `GET ~/admin/runs/{id}` (API-467) step timeline with artefact and evidence references, API-472 evidence export; API-V2-APPROVAL → API-541/542 submit/detail and API-539 decide. Existing `/api/v1/…` operations listed per service are retained or mapped by a reviewed adapter (not deployed endpoints). | FSD ch12 “Proposed contract mapping” | API-449, 460–472, 539–545 | Approval decision binds the payload digest | TC-V12-C-005, -006 |
| FR-V12-C-004 | **Precheck and finalize policy (FSD-POL-V6-PRECHECK).** Precheck: validate schema, scope, source, version, policy and quota; reserve units. Finalize: persist accepted output reference, provenance, step states, effect receipt, usage actuals, release reservation, audit. Step idempotency key = digest(tenant, company/startup, run, version, step, target). Timeouts: read 30 s, AI 90 s, provider per verified adapter. Max 3 safe retries with full jitter (NFR-016 base 30 s, factor 2, max 15 min); never replay an uncertain write. Long-running media/calls use asynchronous poll/callback. V4 guard controls adopted for production: role separation (requester ≠ reviewer; auditor read-only), period allowance ledger (remaining = allowance − active or completed units in the month; approval excludes its own reservation), portfolio aggregates only (DEC-055), per-service channel allowlist (e.g. SM-SVC-14 paid ads only), duplicate reference+workflow+channel → Held, approval expiry (15 min in the simulator; production per BRL-APR-03), pause → Held, cancel/retry/reconcile with policy recheck. | FSD ch40 V6 canonical policy; FSD ch12 V4 guard contract | E-1…E-9; BRL-AUT-06/07; NFR-014/016 | DEC-545 | TC-V12-C-007, -009, -010 |
| FR-V12-C-005 | **Step state and reason model.** StepRun states: Pending, Running, Waiting (AWAITING_APPROVAL), Held, **Blocked** (new), Reconciling, Succeeded, Failed, Cancelled. V12 failure codes become reason codes on StepRun: SOURCE_DENIED, REVIEW_REQUIRED, INVALID_METRIC, INVALID_STATE, POLICY_DENIED, CONFLICT, EFFECT_UNKNOWN (plus engine codes ENTITLEMENT_REVOKED, BUDGET_EXHAUSTED, CONSENT_REVOKED, DUPLICATE). Durable checkpoint before acknowledgement (ST-04) with the lease fencing token of Part 3.4 §3.4.5.4 A. | FSD ch12 step tables; ch13 ST-04 | Part 2.3 §2.27.14; DEC-050 | DEC-541, ADR-192 | TC-V12-C-008, -012, -013 |
| FR-V12-C-006 | **Typed artefact, evidence and effect receipt.** Each step persists a typed artefact reference (schema-validated candidate per FSD-POL-V6-ARTIFACT), evidence set `{items, source_ref, observed_at, hash, rights}`, candidate `{artifact_ref, confidence, reason_codes, review_state}`, calculation `{value, unit, assumptions, evidence_refs}`, domain_result `{artifact_ref, status, evidence_refs}`, match_result `{matched_refs, unmatched_refs, conflict_refs}`, effect_receipt `{provider_ref, status, observed_at}`. Financial, identity and uniqueness fields are normalized into domain tables, never kept only as JSON. Physical DDL (V12 DB-V2-RUN/STEP/ARTIFACT/EVIDENCE/EFFECT) is owned by Part 11 data group I/E [GAP-803]. | FSD ch12 step outputs; ch40 ARTIFACT | ENT-059 Evidence; ENT-162/163 | — | TC-V12-C-015, -016 |
| FR-V12-C-007 | **Step-class handler library.** Seven reusable handlers implement all 286 steps by configuration: Evidence retrieval, AI inference, Deterministic calculation, Deterministic domain logic, Policy gate / human review, Deterministic identity / reconciliation, External effect. Only AI-inference steps may call the model gateway; External-effect steps hold the only effect tools and never read untrusted content in the same step (AIX-09). An incomplete handler mapping blocks release of the workflow (FL-03). | FSD ch12 V5 FL-03; ch13; ch15 | AU-001/003/006/009/026; WQG | ADR-190 | TC-V12-C-017, -018, -019 |
| FR-V12-C-008 | **DTO validation.** Appendix B JSON Schema 2020-12 documents are the canonical validators at run creation and at each step boundary (`additionalProperties: false`; uuid, date-time, ISO 4217 `^[A-Z]{3}$`, decimal string `^-?\d{1,14}(\.\d{1,4})?$`, reason codes `^[A-Z][A-Z0-9_]{2,63}$`, arrays ≤ 500 items, free text 1–4,000 characters NFC). Money in DTOs is int64 minor units; storage stays Decimal (DEC-027) with exact conversion by `ref_currency.minor_units`. The V4 simulator’s heuristic text inputs never become schemas (FL-02). | Appendix B; FSD ch12 DTO tables; V5 FL-02 | NFR-015/017; Part 3.5b Money | DEC-543, DEC-544, ADR-191 | TC-V12-C-020, -021, -022 |
| FR-V12-C-009 | **Optional producers and equivalent input.** A workflow never requires another paid SKU: a client may supply equivalent authorized input (workbook “Prerequisite automations”). A cross-workflow event starts a child only when the child SKU is entitled or the input is supplied; otherwise the child is Held with ENTITLEMENT_MISSING and no data crosses scope (FL-10). | Workbook; FSD ch13 FL-10; Entitlement_Rules | BRL-SVC-03; E-1 | — | TC-V12-C-014 |
| FR-V12-C-010 | **Risk class enforcement.** The PDP reads the workflow’s risk class and enforces the autonomy crosswalk (§11.3.5.4): R0 no external effect; R1 deterministic safety controls at L3, other writes reviewed; R2 L1 approval of exact hash then L2 dispatch, L3 only for DEC-064 L3 categories; R3 ≤ L1. Where V12 sources disagree, the stricter class applies (DEC-546). | BRD ch09 risk; ch12 authority; BRD ch18 | DEC-064; BRL-AUT-01; AU-009 | DEC-542, 546, 548, 549 | TC-V12-C-023, -024, -025 |
| FR-V12-C-011 | **Templates as parameter sets.** Industry/business templates (MT-29, FL-12) are versioned parameter sets referencing a canonical workflow; applying one needs explicit review and never grants entitlement or overrides policy; 25 customer configurations create no definition clone (MT-34). | FSD ch12 MT-29; BRD ch09 MT-34 | A113; DEC-051 | — | TC-V12-C-011 |
| FR-V12-C-012 | **Workflow KPI and metering events.** Each completed step emits KPI numerator/denominator events for the workflow’s two KPIs (formulas in each block) and a meter event in the service’s meter unit; simulated runs are flagged and excluded (BRL-AUT-04); meter events reconcile to invoices (BRL-SVC-04, NFR-035). Thresholds are set from the pilot baseline (DEC-554). | BRD ch09 KPI column; workbook usage limits | KPI-19/20; AU-042 | DEC-554 | TC-V12-C-028, -029, -030 |

### 11.3.5.2 Execution sequence for every SM-SVC workflow

```mermaid
sequenceDiagram
  autonumber
  participant R as Requester or trigger
  participant API as Run API
  participant REG as Contract registry
  participant PDP as Policy Decision Point
  participant DB as PostgreSQL
  participant H as Step-class handler
  participant GW as Model gateway
  participant AD as Effect adapter
  R->>API: Start workflow with DTO and idempotency key
  API->>REG: Resolve approved definition and schema URN
  API->>API: Validate DTO against input schema
  API->>PDP: Precheck scope, entitlement, policy, quota, risk class
  PDP-->>API: Allow or Deny with reason
  API->>DB: One transaction: run snapshot, reservation, audit, outbox
  API-->>R: 202 with run reference
  loop each step in order
    DB->>H: Outbox event for step
    H->>PDP: Dispatch-time recheck
    alt AI inference step
      H->>GW: Tier 0 then 1a or 1b, schema and eval gate
    else External effect step
      H->>AD: Approved action ref, digest, idempotency key
      AD-->>H: Receipt or timeout
    end
    H->>DB: Checkpoint: state, reason code, artefact, evidence, usage
  end
  DB-->>API: Finalize: release reservation, meter, KPI events
```

### 11.3.5.3 Step state model (DEC-541, ADR-192)

```mermaid
stateDiagram-v2
  [*] --> Pending
  Pending --> Running : precheck passed
  Running --> Waiting : REVIEW_REQUIRED
  Waiting --> Running : approval of exact digest
  Waiting --> Blocked : approval rejected or expired
  Running --> Held : SOURCE_DENIED or INVALID_STATE or INVALID_METRIC or CONFLICT
  Held --> Running : reviewer resolves and policy recheck passes
  Running --> Blocked : POLICY_DENIED or budget or entitlement
  Running --> Reconciling : EFFECT_UNKNOWN
  Reconciling --> Succeeded : reconciled confirmed
  Reconciling --> Failed : reconciled failed
  Running --> Succeeded : output validated
  Running --> Failed : permanent error after safe retries
  Held --> Cancelled : owner cancels
  Blocked --> [*]
  Succeeded --> [*]
  Failed --> [*]
  Cancelled --> [*]
```

| V12 failure route | Steps | Blueprint state | Behaviour |
|---|---|---|---|
""" + "\n".join(f"| {k} | {S['fail'][k]} | {v[0]} | {v[1]} |" for k, v in M.FAIL.items()) + r"""

**Run-level roll-up.** A run is Waiting when any step is Waiting; Held when any step is Held; Reconciling when any step is Reconciling; Blocked (terminal, reason recorded) when a Blocked step has no alternative path; Succeeded only when every step is Succeeded. Part 3.2 run states (`queued → running → waiting → succeeded | failed | cancelled | uncertain → reconciled_*`) map as queued = Pending, uncertain = Reconciling, blocked = new value `blocked` [RECOMMENDATION-813].

### 11.3.5.4 Authority crosswalk V12 L0–L4 / R0–R3 → blueprint (DEC-542)

| V12 authority | V12 meaning (BRD ch18) | Blueprint equivalent | Notes |
|---|---|---|---|
| L0 | Manual action recorded | L0 (human task, no send) | Same |
| L1 | AI proposes or drafts; human decides | L1 (draft awaits human approval) | Same |
| L2 | Exact approved action with reviewer, expiry and limits | L1 approval of exact hash **then** L2 dispatch of that item (DEC-064 publishing pattern) | Equivalent control; no consequential action without the exact-digest approval |
| L3 | Bounded routine actions under approved mandate, scope, expiry and caps | L3 within caps, **only** for DEC-064 L3 categories (approved-FAQ replies, eligible follow-ups, reminders) and deterministic internal safety controls | V12 extends L3 to R2/R3 “where lawful” → CONFLICT-798/799 |
| L4 | Adaptive orchestration inside L3 constraints; never expands authority | Supervisor orchestration (WF-13, WF-15, AU-053) with L3 as the ceiling | Label adopted; no new authority |

| Risk class | Count | V12 rule | Blueprint enforcement | Status |
|---|---|---|---|---|
| R0 internal analysis/draft | """ + str(S['risk']['R0']) + """ | L1 assisted; L3 approved read/draft | Unattended internal drafting and analysis; no external effect; reuse outside workspace needs approval | Matched |
| R1 scoped state write or safety control | """ + str(S['risk']['R1']) + """ | L1/L2 review; L3 only for approved deterministic internal actions | Suppression, stop, dedupe, pause at L3 (AU-008/024/025); other writes reviewed | Matched |
| R2 external communication/provider/access write | """ + str(S['risk']['R2']) + """ | L2 mandatory approved effect; L3 with bounded mandate where lawful | L1 + L2 dispatch; L3 only DEC-064 categories | Pending Founder (CONFLICT-799, DEC-549) |
| R3 financial/legal/commitment | """ + str(S['risk']['R3']) + """ | Default L2; L3 with bounded mandate where lawful | ≤ L1 (DEC-064); AI never signs, pays, submits bids or sets prices | Pending Founder (CONFLICT-798, DEC-548) |

### 11.3.5.5 Step-class handler library (ADR-190)

| Class (FSD ch33) | Steps | V12 executor | Input → output | Handler obligations | Test technique |
|---|---|---|---|---|---|
""" + "\n".join(f"| {c} | {S['cls'][c]} | {e} | {io} | {ob} | {M.CLASS_TEST[c]} |" for c, e, io, ob in [
 ('Evidence retrieval', 'Evidence/ingestion engine', 'permitted source or artefact refs + scope + source policy → evidence_set', 'Reject stale or unauthorized source; preserve original and confidence; hash and rights stored; transient read retry ≤ 3'),
 ('AI inference', 'Domain agent / task router', 'scoped evidence + approved configuration + prior results → candidate', 'Gateway only (BRL-AI-01); typed schema; claims check; draft cannot change live state; untrusted input cannot invoke tools; EVAL-SM-SVC-<wf> gate'),
 ('Deterministic calculation', 'Rules/analytics engine', 'versioned inputs + policy/metric_version → calculation', 'Zero model calls; validate denominator, units, calibration and bounds; never invent missing values'),
 ('Deterministic domain logic', 'Domain service', 'validated payload + prior result → domain_result', 'Version check; explicit authorization before state change; one transaction with audit and outbox'),
 ('Policy gate / human review', 'Policy/validation engine', 'payload + subject + policy version → decision', 'PDP decision record; approval routing with SLA (BRL-APR-10); no external effect on deny'),
 ('Deterministic identity / reconciliation', 'Identity/reconciliation engine', 'scoped object refs + version + evidence_set → match_result', 'Unique source event; no cross-company merge; financial allocations atomic; uncertain provider outcome reconciled'),
 ('External effect', 'Effect adapter', 'approved_action_ref + target/version + idempotency_key → effect_receipt', 'Approval payload digest and scope exact; dispatch recheck; reconcile ambiguous response before repeat; simulation adapter returns synthetic receipt only'),
]) + r"""

### 11.3.5.6 ADRs

| ADR | Title | Context | Decision | Consequences |
|---|---|---|---|---|
| ADR-190 | Step-class handler library for SKU workflows | 286 steps in 80 workflows (517 in 156) share seven behaviour classes; writing one handler per step would duplicate logic (MT-34) | Implement seven parameterized handlers; bind steps by configuration in the contract registry; FL-03 release gate requires a complete binding | Fewer code paths, uniform tests generated from the registry [RECOMMENDATION-807]; new step behaviour needs a new class through ADR review |
| ADR-191 | JSON Schema 2020-12 validation at the run boundary | Appendix B provides validated schemas; Part 3.5b uses decimal-string money | Validate DTOs with Appendix B schemas at run creation and each step boundary; money as int64 minor units in DTOs, Decimal in storage | Exact, testable contracts; converter must be total and reversible for every ISO 4217 minor-unit value |
| ADR-192 | Explicit Blocked state and V12 reason codes | V12 distinguishes BLOCKED (policy, no effect) from HELD (resolvable) | Add Blocked step state; store V12 failure code as reason code; roll-up rules in §11.3.5.3 | Clear operator queues (Held = work, Blocked = stop); Part 2.3 diagram owner to update |

### 11.3.5.7 Engine tests (TC-V12-C-001…030)

| Test | Requirement | Scenario | Expected | Level |
|---|---|---|---|---|
| TC-V12-C-001 | FR-V12-C-001 | Load registry; list SM-SVC-01…20 | Exactly 80 workflow IDs, 286 step IDs; each with schema URN, risk class and KPI pair | CT |
| TC-V12-C-002 | FR-V12-C-001 | Start a run on an unapproved definition version | 409; no run | IT |
| TC-V12-C-003 | FR-V12-C-002 | Event envelope with startup_id of another tenant | Rejected; no run; audit | SEC |
| TC-V12-C-004 | FR-V12-C-002 | BusinessContext missing policy snapshot | Run creation fails closed | UT |
| TC-V12-C-005 | FR-V12-C-003 | Start run via DTO endpoint | 202 with run reference; `GET ~/admin/runs/{id}` shows steps | IT |
| TC-V12-C-006 | FR-V12-C-003 | Approve, then alter payload before dispatch | Digest mismatch → Blocked | SEC |
| TC-V12-C-007 | FR-V12-C-004 | AI step exceeds 90 s | Timeout; safe retry ≤ 3 with jitter; then Failed with reason | CHAOS |
| TC-V12-C-008 | FR-V12-C-005 | Kill worker after checkpoint of an effect step | Resume without second effect (ST-04) | CHAOS |
| TC-V12-C-009 | FR-V12-C-004 | Allowance exhausted by active same-month runs | Reservation denied → Blocked BUDGET_EXHAUSTED | IT |
| TC-V12-C-010 | FR-V12-C-004 | Requester tries to approve own run | Refused (BRL-APR-01) | SEC |
| TC-V12-C-011 | FR-V12-C-011 | Apply a template to 25 configurations | Definition count unchanged; regression IDs stable (MT-34, MT-29) | IT |
| TC-V12-C-012 | FR-V12-C-005 | Each V12 failure code fixture | State per §11.3.5.3 table; reason code stored | UT |
| TC-V12-C-013 | FR-V12-C-005 | Lease expired worker commits late | Write rejected by fencing token | IT |
| TC-V12-C-014 | FR-V12-C-009 | Event targets an unentitled child SKU | Child Held ENTITLEMENT_MISSING; no data crosses scope (FL-10) | IT |
| TC-V12-C-015 | FR-V12-C-006 | Effect step completes | effect_receipt {provider_ref,status,observed_at} stored and linked to approval digest | IT |
| TC-V12-C-016 | FR-V12-C-006 | Financial calculation output | Normalized into domain table; JSON artefact alone rejected | CT |
| TC-V12-C-017 | FR-V12-C-007 | Workflow with an unmapped step | Release blocked (FL-03) | CT |
| TC-V12-C-018 | FR-V12-C-007 | Prompt-injection text in evidence for an AI step | No tool call; output schema-valid; flagged (AIX-08/09) | AIE |
| TC-V12-C-019 | FR-V12-C-007 | Deterministic step golden fixture | Exact output; zero model calls (gateway counter = 0) | UT |
| TC-V12-C-020 | FR-V12-C-008 | DTO with extra property | 422 field error | CT |
| TC-V12-C-021 | FR-V12-C-008 | `budget_minor` = 123456 INR minor units | Stored Decimal 1234.56 INR; round-trip exact | UT |
| TC-V12-C-022 | FR-V12-C-008 | Currency `inr` (lower case) | 422 pattern violation | CT |
| TC-V12-C-023 | FR-V12-C-010 | R3 workflow configured with an L3 mandate | PDP denies; mandate path disabled pending DEC-548 | SEC |
| TC-V12-C-024 | FR-V12-C-010 | R2 first-touch send configured at L3 | Denied; L1 approval required (DEC-549 pending) | SEC |
| TC-V12-C-025 | FR-V12-C-010 | Sources disagree on class (workbook internal vs FSD R3) | Stricter class applied (DEC-546) | UT |
| TC-V12-C-026 | FR-V12-C-003 | Run inspection screen A110 with keyboard and screen reader | Step table, states and reason codes announced; WCAG 2.2 AA (NFR-023) | A11Y |
| TC-V12-C-027 | FR-V12-C-005 | Held and Blocked badges | Text label plus icon; contrast ≥ 4.5:1; not colour only | A11Y |
| TC-V12-C-028 | FR-V12-C-012 | Simulated run completes | KPI and meter events flagged simulated and excluded (BRL-AUT-04) | IT |
| TC-V12-C-029 | FR-V12-C-012 | Month-end meter reconciliation | 100% meter events match invoice lines (NFR-035) | IT |
| TC-V12-C-030 | FR-V12-C-012 | EduVerse lead under 18 enters SM-SVC-06/07/14 | Blocked POLICY_DENIED; no outreach or ad audience (DEC-030, BRL-ELG-13); MedMaarg health data rejected (BRL-ELG-14) | SEC |

**Engine stories.**

**US-18-YC21 — Contract registry and typed runs.** As R11 Automation Lead, I want every SM-SVC workflow registered with its DTO schema, step classes, risk class and KPIs, so that runs are reproducible, validated and comparable across tenants. Requirements FR-V12-C-001…009, 011, 012.

```gherkin
Feature: Typed SKU workflow runs
  Scenario: Run snapshot is immutable
    Given SM-SVC-04-WF02 revision 3 is approved
    When a run starts and revision 4 is approved during the run
    Then the run keeps revision 3 and its schema URN
  Scenario: Uncertain effect is never replayed
    Given SM-SVC-06-WF02 step 03 timed out after submission
    When an operator requests a retry
    Then the request is refused until reconciliation completes
```

**US-18-YC22 — Authority crosswalk and risk classes.** As R10 Legal/Compliance, I want V12 risk classes enforced by the PDP with blueprint autonomy caps, so that no R2/R3 workflow acts without the exact approval the blueprint requires. Requirement FR-V12-C-010.

```gherkin
Feature: Risk class enforcement
  Scenario: R3 effect requires exact approval
    Given SM-SVC-17-WF03 has an approved quote revision with digest D1
    When the dispatch payload digest is D2
    Then the step is Blocked with reason POLICY_DENIED and no external effect occurs
  Scenario: V12 bounded mandate is not honoured for R3
    Given a bounded mandate is configured for SM-SVC-14-WF02
    When the activation step runs
    Then the PDP requires a per-action approval until the Founder decides DEC-548
```

### 11.3.5.8 Release placement

| Scope | Release / wave | Basis |
|---|---|---|
| Engine contract (FR-V12-C-001…012), WF01–03 contract conformance for SVC-01…05 | Release 1 (W1–W3), inside existing EP-05/06/07/18 work | Behaviour already planned; adds contracts and tests |
| WF01–03 conformance for SVC-06…16 | Release 1 W2–W3 (messaging, content) and Release 2 W4 (ads, events) per epic wave | Part 0 epic waves |
| WF01–03 conformance for SVC-17…20 | Release 2 (W4–W5) | EP-13/14 waves |
| WF04 capabilities (20) | Phase 2 (W6) unless the Founder funds earlier (DEC-552 Pending Founder decision) | V12 marks WF04 1.0-target; outside approved budgets |

### 11.3.5.9 Effort and cost (separately approvable; outside DEC-230/231)

""" + cost_tables(D, M, S) 

def cost_tables(D, M, S):
    import csv, glob
    svcs = _svcs()
    nP = S['st']['P']; nN = S['st']['N']
    dev = [
     ('Contract registry, 80 definitions, schema URN registry', 6, 10),
     ('DTO validators (20 schemas), minor-unit converter, enum registries', 6, 10),
     ('Step-class handler library (7 classes)', 14, 24),
     ('Binding 286 steps (80 workflows × 0.3–0.6 pd)', 24, 48),
     ('Run/result/approval API and DTO start-run endpoint', 4, 8),
     ('Step state/reason model, Blocked state, effect receipts', 5, 9),
     ('KPI and meter events for 160 workflow KPIs', 8, 16),
     ('Test automation: 968 mapped tests (80 fixture sets × 0.4–0.8 pd) + 30 engine tests', 38, 74),
     (f'Partially covered enhancements ({nP} × 1.5–3 pd)', round(nP*1.5), nP*3),
     (f'Not covered capabilities ({nN} × 4–8 pd)', nN*4, nN*8),
     ('Runbooks, operator guides, documentation', 3, 6),
    ]
    lo = sum(x[1] for x in dev); hi = sum(x[2] for x in dev)
    o = ["**Development (one-time).** Rates ₹4,545–6,818 per person-day (Part 8.4, BRD §6). Basis: component estimates below; base = midpoint [ASSUMPTION-806].\n",
         "| Component | Low pd | High pd |\n|---|---|---|"]
    for n, a, b in dev: o.append(f"| {n} | {a} | {b} |")
    base = (lo + hi) / 2
    o.append(f"| **Total** | **{lo}** | **{hi}** |\n")
    o.append(f"Development cost: low {lo} pd × ₹4,545 = **₹{lo*4545/1e5:.2f} lakh**; base {base:.0f} pd × ₹5,682 = **₹{base*5682/1e5:.2f} lakh**; high {hi} pd × ₹6,818 = **₹{hi*6818/1e5:.2f} lakh**. Of this, the WF04 and not-covered share ({round(nP*1.5)+nN*4}–{nP*3+nN*8} pd) belongs to Phase 2 (DEC-552).\n")
    # running
    base_dir = glob.glob('/tmp/claude-0/-home-user-Allinonecalculator/233b6551-af93-57f5-8f0b-015057ecee11/scratchpad/v12/src/*39_Services_156_Workflows*_csv')[0]
    rows = list(csv.reader(open(base_dir + '/Service_Index.csv', encoding='utf-8')))[4:]
    allow = {r[0]: (r[6], int(r[7])) for r in rows if r and r[0].startswith('SM-SVC-')}
    o.append("**Running (recurring, monthly) at the illustrative pilot allowance.** Formula: monthly base = allowance × mean V12 INR/invocation of the service’s four workflows (text/compute only; provider, media, ad spend, human review and retries excluded, as V12 states); low = 0.3 × base; high = 3 × base [ASSUMPTION-806]. These are estimates from V12 illustrative rates, not vendor quotes; verify at time of implementation (as of 27 Nov 2026). AI inference within these figures is billed against the DEC-008 ceilings through the model gateway budget lines.\n")
    o.append("| Service | Meter unit | Allowance / month | Mean INR / invocation | Low ₹ | Base ₹ | High ₹ |\n|---|---|---|---|---|---|---|")
    tl = tb = th = 0
    for s in svcs:
        k = f'SM-SVC-{s}'; mu, a = allow[k]
        c = statistics.mean(float(D[f'{k}-WF{j:02d}']['wb_cost']['Internal INR / invocation']) for j in range(1, 5))
        b = a * c; tl += 0.3*b; tb += b; th += 3*b
        o.append(f"| {k} | {mu} | {a:,} | {c:.2f} | {0.3*b:,.0f} | {b:,.0f} | {3*b:,.0f} |")
    o.append(f"| **Total** | | | | **{tl:,.0f}** | **{tb:,.0f}** | **{th:,.0f}** |\n")
    o.append("Running cost is per tenant at the full illustrative allowance of all 20 services; actual cost scales with entitled services and usage. No new subscription is introduced by this part.\n")
    return "\n".join(o)

def file_c_tail(D, M, ROWS, FR, TC, US, S):
    r3 = [w for w, d in D.items() if d['brd09']['risk'][:2] == 'R3']
    r2 = [w for w, d in D.items() if d['brd09']['risk'][:2] == 'R2']
    return f"""
## 11.3.6 Conflicts and proposed resolutions

| Tag | Conflict | V12 position | Blueprint position | Proposed resolution | Status |
|---|---|---|---|---|---|
| CONFLICT-798 | R3 workflows may run at L3 under a “separately approved bounded mandate where lawful” | {', '.join(r3)} (9) | DEC-064 and BRL-AUT-01: quotes, discounts, contracts, legal terms, bid submission ≤ L1; spend activation L1 approval; safety invariant “consequential actions capped at L1” | Keep ≤ L1 (V12 L2 = blueprint L1 + L2 dispatch of the exact item); keep the mandate data model but disable the L3 path by a non-tenant-editable flag; revisit only with legal opinion per jurisdiction | **Pending Founder decision** (DEC-548) |
| CONFLICT-799 | R2 workflows may run at L3 with a bounded mandate | {', '.join(r2)} (12) | DEC-064: L3 only for approved-FAQ replies, eligible follow-ups and reminders; first-touch outreach and publication L1 | Allow the V12 mandate only for DEC-064 L3 categories (SM-SVC-09-WF02 approved FAQ, SM-SVC-10-WF01/02 and SM-SVC-16-WF02 reminders/bookings, eligible follow-ups); all others L1 + L2 dispatch | **Pending Founder decision** (DEC-549) |
| CONFLICT-800 | SM-SVC-19-WF03 step 04 “coordinate authorized submission and track receipt”; workbook “manual submission unless permitted API” | Submission by permitted API possible | DEC-053: tender submission never automated; human submits; AI never submits bids (safety invariant) | Step 04 = human submission task with evidence capture (BRL-BID-04); no portal API submission adapter | **Pending Founder decision** (DEC-550) |
| CONFLICT-801 | Authority scale L0–L4 vs blueprint L0–L3 | L2 = exact approved action; L4 adaptive orchestration | L0–L3 (Part 7.2; DEC-064) | Crosswalk §11.3.5.4; L4 is a label for supervisor orchestration with L3 ceiling | Resolved — adopt V12 labels (DEC-542) |
| CONFLICT-802 | DTO money as int64 minor units | `budget_minor`, `spend_minor`, `total_minor`, `tax_minor` | DEC-027 Decimal; Part 3.5b Money decimal string | Minor units at the workflow DTO boundary; Decimal storage; exact conversion | Resolved — adopt V12 (DEC-543, amends Part 3.5b for workflow DTOs) |
| CONFLICT-809 | V12 sources disagree on side-effect classification for some workflows | e.g. SM-SVC-14-WF04, SM-SVC-17-WF02/03/04 and SM-SVC-20-WF02 are R3 in BRD/FSD but “Internal analysis/draft” in the workbook; SM-SVC-19-WF04 and SM-SVC-08-WF01 are R0/R1 but “Potential external write” | — | Apply the stricter classification per workflow and step | Resolved (DEC-546) |

No item weakens a safety invariant. Investor/fundraising scope: no workflow in SM-SVC-01…20 targets investors; BRL-TEN-12 and DEC-002 negative tests apply to SM-SVC-02 discovery [RECOMMENDATION-812].

## 11.3.7 Decisions

| DEC | Decision | Authority | Effect |
|---|---|---|---|
| DEC-540 | Adopt SM-SVC-01-WF01…SM-SVC-20-WF04 and their step IDs as canonical workflow-contract IDs; WF-01…39 remain business-flow views that invoke them; AGT-01…15 become aliases on existing agents | Customer revision V12 (28 Nov 2026) | Registry, traces and RTM carry V12 IDs |
| DEC-541 | Add the Blocked step state; V12 failure codes are StepRun reason codes; AWAITING_APPROVAL = Waiting | Customer revision V12 (28 Nov 2026) | Amends Part 2.3 §2.27.14 and Part 3.2 run states |
| DEC-542 | Authority crosswalk L0–L4/R0–R3 → blueprint autonomy (§11.3.5.4); DEC-064 caps unchanged | Customer revision V12 (28 Nov 2026) | Amends Part 7.2 autonomy labels |
| DEC-543 | Workflow DTO money = int64 minor units + ISO 4217; storage Decimal | Customer revision V12 (28 Nov 2026) | Amends Part 3.5b Money for workflow DTOs; DEC-027 storage unchanged |
| DEC-544 | Appendix B JSON Schemas are the canonical validators (`urn:sm:dto:<wf>:v2`), pinned per run | Customer revision V12 (28 Nov 2026) | FR-V12-C-008 |
| DEC-545 | FSD-POL-V6-PRECHECK adopted: idempotency digest, timeouts 30 s / 90 s, ≤ 3 safe retries with jitter, finalize contents | Customer revision V12 (28 Nov 2026) | Complements NFR-016, BRL-AUT-06/07 |
| DEC-546 | Where V12 sources disagree on risk or side-effect class, the stricter applies | Customer revision V12 (28 Nov 2026) | Resolves CONFLICT-809 |
| DEC-547 | Per-workflow acceptance taxonomy (POS, INPUT, SCOPE, ENT, DUP, QUALITY, BUDGET, RECOVERY; +APPROVAL, EFFECT for R2/R3) is a release gate per workflow | Customer revision V12 (28 Nov 2026) | 682 + 286 tests mapped to TC-V12-C |
| DEC-548 | R3 workflows stay ≤ L1; V12 bounded-mandate L3 path disabled | Pending Founder decision | CONFLICT-798 |
| DEC-549 | R2 L3 mandate only for DEC-064 L3 categories | Pending Founder decision | CONFLICT-799 |
| DEC-550 | SM-SVC-19-WF03 submission remains human (DEC-053) | Pending Founder decision | CONFLICT-800 |
| DEC-551 | The 20 WF04 workflows are in scope as V12 contracts with the specifications in this part | Customer revision V12 (28 Nov 2026) | The WF04 requirements FR-V12-C-016, 020, 024 … 092 (every fourth FR) |
| DEC-552 | WF04 and not-covered capability build is placed in Phase 2 (W6) unless funded earlier; cost per §11.3.5.9 | Pending Founder decision | Budget envelope outside DEC-230/231 |
| DEC-553 | V12 per-invocation INR figures are illustrative metering inputs, not prices (Quotation pending) | Customer revision V12 (28 Nov 2026) | Cost columns in each block |
| DEC-554 | 160 workflow KPIs adopted with the formulas in this part; thresholds set after the pilot baseline | Customer revision V12 (28 Nov 2026) | FR-V12-C-012; GAP-810 |

## 11.3.8 Expert persona review

| Persona | Finding | Action taken |
|---|---|---|
| Principal Workflow/BPM Architect | V12 workflows are SKU-level activities; the blueprint WF-xx are end-to-end processes. Mixing them would duplicate orchestration. Failure routes need a compensating path for R3 effects (saga). | Crosswalk §11.3.4.3 keeps both layers; step state model with Blocked and Reconciling; effects only via outbox and adapter; compensation limited to authorized reversible actions (FL-11) |
| Principal Workflow/BPM Architect | 286 steps reduce to 7 behaviour classes | ADR-190 handler library; FL-03 release gate |
| Revenue Operations leader | Workflow KPIs had no formulas or owners; per-invocation cost is not a price | 160 KPI formulas, thresholds after pilot (DEC-554); cost labelled illustrative (DEC-553); meter events per service (FR-V12-C-012) |
| Revenue Operations leader | Quotes, contracts, ad spend and bids must never gain autonomy through a mandate | CONFLICT-798/799/800 raised; ≤ L1 retained pending Founder |
| QA architect | V12 gives 8–10 scenario types per workflow and one test per step but no executable assertions | Each mapped to TC-V12-C with level and blueprint assertion; 30 engine tests incl. chaos, replay, A11Y and minors/health negatives |
| QA architect | AT01 original acceptance is still “not run” | Kept as origin reference; superseded by TC-POS mapping; evidence links required at execution |
| Principal Engineer | DTO money representation differs from Part 3.5b; physical DDL for artefacts/effects is not in the blueprint | DEC-543/ADR-191; GAP-803 handed to data group; logical fields in FR-V12-C-006 |
| Principal Engineer | Start-run endpoint for catalogued workflows with typed DTO is missing | Proposed endpoint in FR-V12-C-003; GAP-804 to API group |
| Security/AI Governance Lead | Multimodal enquiries (SM-SVC-09-WF04, SM-SVC-10) add audio/image personal data | Tier 1b only, never Tier 2; recording consent verify [ASSUMPTION-811] |
| FinOps Lead | Development effort for 80 contracts was not in Ledger A | §11.3.5.9 separately approvable estimate; WF04 share deferred to W6 (DEC-552) |

## 11.3.9 Tags register

| Tag | Statement | Location | Owner / next step |
|---|---|---|---|
| ASSUMPTION-796 | SLA targets where V12 says “baseline and threshold approved in pilot” (e.g. 2 h report draft, 2-business-day verification, 30 min import, 15 min handover) are planning values | Workflow blocks (SLA rows) | Product owner confirms after pilot |
| ASSUMPTION-797 | Score agreement tolerance ±5 points for SM-SVC-04-WF02 | SM-SVC-04-WF02 | RevOps confirms with labelled sample |
| CONFLICT-798 | R3 L3 bounded-mandate path vs DEC-064 / safety invariant | §11.3.6 | Founder (DEC-548) |
| CONFLICT-799 | R2 L3 bounded-mandate path beyond DEC-064 L3 categories | §11.3.6 | Founder (DEC-549) |
| CONFLICT-800 | Bid submission coordination vs DEC-053 | §11.3.6 | Founder (DEC-550) |
| CONFLICT-801 | L0–L4 vs L0–L3 authority scale | §11.3.5.4 | Resolved DEC-542 |
| CONFLICT-802 | Minor-unit money in DTOs vs Decimal | §11.3.5.1 | Resolved DEC-543 |
| GAP-803 | Physical DDL for run artefact, evidence and effect receipt (V12 DB-V2-*) | FR-V12-C-006 | Part 11 data group (I/E) |
| GAP-804 | Typed start-run endpoint for catalogued workflows (V12 API-V2-RUN) | FR-V12-C-003 | Part 11 API group (H) |
| GAP-805 | Provider terms for answer-engine observation, social listening APIs, WhatsApp commerce messages and e-sign evidence are unverified | SM-SVC-07/12/13/18 blocks | Verify at time of implementation (as of 27 Nov 2026) |
| ASSUMPTION-806 | Cost basis: V12 illustrative INR/invocation; meter unit ≈ one invocation; low 0.3× / high 3×; effort component estimates | §11.3.5.9 | FinOps re-baseline at approval |
| RECOMMENDATION-807 | Implement the 286 steps through the 7-class handler library and generate tests from the registry | ADR-190 | Principal Engineer |
| RECOMMENDATION-808 | Regenerate the Part 9.4 catalogue so each WF-xx lists the SM-SVC contracts it invokes | §11.3.4.3 | Documentation owner |
| CONFLICT-809 | V12 internal inconsistency of side-effect classes | §11.3.6 | Resolved DEC-546 |
| GAP-810 | No numeric thresholds for 160 workflow KPIs in V12 | Workflow blocks | Set after pilot baseline (DEC-554) |
| ASSUMPTION-811 | Multimodal enquiries processed only at Tier 1b with recording consent; jurisdictional consent rules to verify | SM-SVC-09-WF04, SM-SVC-10 | Legal/DPO |
| RECOMMENDATION-812 | Keep BRL-TEN-12 / DEC-002 negative tests on SM-SVC-02 discovery (no investor targets) | §11.3.6 | QA |
| RECOMMENDATION-813 | Part 2.3 §2.27.14 and Part 3.2 run states to add `blocked` | §11.3.5.3 | Owners of Parts 2.3/3.2 |

**Inconsistencies observed in earlier parts (reported, not fixed).** (1) Part 3.2 run states (`queued, running, waiting, succeeded, failed, cancelled, uncertain, reconciled_*`) and Part 2.3 §2.27.14 states (Pending, Running, Waiting, Held, Paused, Reconciling, Succeeded, Failed, Cancelled) use different vocabularies for the same object; neither has Blocked. (2) Part 3.3 §3.3.5 says money storage is always 2 dp while Part 3.5b allows up to 4 decimals in the Money pattern. (3) Part 9.4 lists WF-01…39 but WF-24 is not present in Part 9.7b (numbering gap).

## 11.3.10 Quality gate: Batch 11.3 (files a, b and c)

| # | Check | Result | Notes and fixes applied |
|---|---|---|---|
| 1 | Every requirement traced to a source | Pass | Every block cites BRD V12 ch09, FSD V12 ch12/13/33/40, Appendix B and the workbook row; blueprint mappings cite WF, AG, AU, BRL, DEC, NFR |
| 2 | Assumptions/gaps/conflicts tagged and logged | Pass | 18 tags (796–813) in §11.3.9; 3 Founder conflicts, 3 resolved conflicts |
| 3 | IDs unique and consistent with earlier parts | Pass | DEC-540…554, ADR-190…192, FR-V12-C-001…092, TC-V12-C-001…{S['tc_last']:03d}, US-<EP>-YC01…22 are in the allocated ranges; no AG/AU/WF IDs issued (owned by other groups); V12 IDs kept literally |
| 4 | No story lacks AC and no requirement lacks a test | Pass | 22 stories with Gherkin; 92 FRs, each with tests (engine FRs → TC-001…030; workflow FRs → 10–14 tests each) |
| 5 | Negative, edge, security and accessibility cases covered | Pass | INPUT, SCOPE, ENT, DUP, BUDGET, RECOVERY per workflow (480); APPROVAL/EFFECT (42); engine SEC, CHAOS, A11Y and minors/health tests |
| 6 | No agent lacks guardrail, fallback, KPI and cost estimate | N/A | No new agents; AGT roles mapped to existing AG cards which carry these fields |
| 7 | Time-sensitive facts flagged "verify" with an as-of date | Pass | Provider rules, prices and cost rates flagged (as of 27 Nov 2026) |
| 8 | No restricted data routed to free-tier models | Pass | Tier 2 eligibility stated per service; contact, conversation, commercial and multimodal data never Tier 2 |
| 9 | Consistent with earlier parts | Pass | Safety invariants kept (L1 cap, PDP recheck, simulation zero effect, no minors, no patient data, human bid submission); approved budgets unchanged |

**Status: Part 11 Batch 11.3 complete (files a, b and c). 80 V12 workflows, 286 steps, {S['dto']} DTO rows, {S['wft']+S['stt']} V12 tests mapped plus 30 engine tests; {S['rows']:,} aspects: {S['after'].get('Matched',0):,} Matched, {S['after'].get('Pending Founder decision',0)} Pending Founder decision; 3 conflicts pending the Founder (DEC-548/549/550).**
"""
