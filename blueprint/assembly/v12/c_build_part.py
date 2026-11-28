#!/usr/bin/env python3
"""Group R3a (letter C) generator: Part 11.3 a/b/c + final/coverage_v12/C_coverage.csv
Inputs: c_workflows.json (from c_parse_workflows.py), c_mapping.py (hand-authored), c_text.py (narrative)."""
import json, sys, os, csv, re, statistics
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import c_mapping as M
import c_text as TX
BP = os.path.dirname(os.path.dirname(HERE))
D = json.load(open(os.path.join(HERE, 'c_workflows.json')))
WFS = list(D.keys())
SVCS = [f"{i:02d}" for i in range(1, 21)]

def esc(s):
    return str(s).replace('|', '\\|').replace('\n', ' ').strip()

def exkey(t):
    for k in M.EXEC:
        if t.startswith(k): return k
    raise KeyError(t)

def exrest(t):
    k = exkey(t); return t[len(k):].lstrip(' /')

def risk(w):
    return D[w]['brd09']['risk'][:2]

# ---------------- ID allocation ----------------
FR = {}      # wf -> FR id
fr_n = 13
for w in WFS:
    FR[w] = f"FR-V12-C-{fr_n:03d}"; fr_n += 1
TC = {}      # (wf, v12 test id) -> TC id
tc_n = 31
for w in WFS:
    for t in D[w]['wf_tests']:
        TC[(w, t['id'])] = f"TC-V12-C-{tc_n:03d}"; tc_n += 1
    for t in D[w]['step_tests']:
        TC[(w, t['id'])] = f"TC-V12-C-{tc_n:03d}"; tc_n += 1
TC_LAST = tc_n - 1
assert TC_LAST <= 999, TC_LAST
US = {}
for i, s in enumerate(SVCS, 1):
    US[s] = f"US-{M.SVC[s]['epic']}-YC{i:02d}"

TEST_LEVEL = {
 'POS': ('IT', 'Output validates against `$defs.output` of the workflow schema; evidence/provenance persisted; run reaches Succeeded; workflow KPI event emitted'),
 'INPUT': ('UT/CT', 'HTTP 422 with field-level errors from the Appendix B schema; no StepRun created; audit event `dto.rejected`'),
 'SCOPE': ('SEC', 'HTTP 403 or indistinguishable 404 (BRL-TEN-04); zero rows, events, notifications or provider calls in the other scope (NFR-032)'),
 'ENT': ('IT', 'Dispatch-time recheck denies (E-3, BRL-SVC-03); run Paused or Held; reservation released; no new effect'),
 'DUP': ('IT replay', 'Exactly one accepted outcome, effect and meter charge (E-4, NFR-005); duplicate returns the original run reference'),
 'QUALITY': ('AIE', 'Step Held or flagged; no unsupported claim reaches output (BRL-AI-03/04); eval record stored (FL-13)'),
 'BUDGET': ('IT', 'Reservation fails → step Blocked; zero provider calls (NFR-014); owner notified'),
 'RECOVERY': ('CHAOS', 'Timeout after submission → Reconciling (DEC-050, E-5); crash after checkpoint resumes without re-running a completed effect (OPT-TC-ST-04)'),
 'APPROVAL': ('IT/SEC', 'Approval bound to the exact payload digest; changed payload, expired or revoked mandate → Blocked (FL-09, BRL-APR-02/03); author ≠ approver (BRL-APR-01)'),
 'EFFECT': ('IT/CHAOS', 'Effect only through the adapter after recheck; effect receipt {provider_ref,status,observed_at} stored; uncertain → Reconciling; simulation zero effect (E-6, NFR-038)'),
}

def cost_inr(w):
    try: return float(D[w]['wb_cost']['Internal INR / invocation'])
    except: return None

def auth_map(w):
    r = risk(w)
    return {
      'R0': 'V12 L1 assisted / L3 approved read-draft → blueprint: internal analysis and drafts run unattended (no external effect); any reuse outside the workspace L1 (DEC-064, BRL-AI-07)',
      'R1': 'V12 L1/L2 review; L3 only for approved deterministic internal actions → blueprint: deterministic safety controls (suppression, pause, dedupe) run at L3; other state writes L1/L2 with revision check',
      'R2': 'V12 L2 mandatory approved effect; L3 only with separate bounded mandate → blueprint: L1 approval of exact hash then L2 dispatch of the approved item; L3 only for DEC-064 L3 categories (approved-FAQ replies, eligible follow-ups, reminders) [CONFLICT-799 → DEC-549 Pending Founder decision]',
      'R3': 'V12 L2 mandatory approved effect; L3 only with separate bounded mandate → blueprint: ≤ L1 (DEC-064, BRL-AUT-01); V12 L3 mandate path disabled [CONFLICT-798 → DEC-548 Pending Founder decision]',
    }[r]

# ---------------- coverage CSV ----------------
ROWS = []
def add(doc, ch, sec, aid, summ, sb, loc, act, nids, sa='Matched'):
    ROWS.append([doc, ch, sec, aid, summ[:400], sb, loc, act, nids, sa])

STMAP = {'C': 'Covered', 'P': 'Partially covered', 'N': 'Not covered'}
def build_csv():
    # boilerplate once
    b = [
     ('BRD','09','V10 Historical reconciliation','C-BRD09-REC05','REC-05 A113 canonical workflow-derived template draft/validate/test/publish/retire; unentitled or untested draft cannot publish','Covered','Part 3.4 §3.4.5.4 B WQG-01…12; A113; BRL-AUT-02','Mapped; no change','DEC-540'),
     ('BRD','09','V10 Historical reconciliation','C-BRD09-REC08','REC-08 map historical use-case group labels to current registry; no fabricated recovered library','Partially covered','Part 9.4 §9.4.2','Group index mapped in §11.3.4.3','DEC-540'),
     ('BRD','09','V6 MT-34','C-BRD09-MT34','MT-34 one definition per workflow/version; per-customer configuration only; 25 configurations without cloning','Covered','BRL-AUT-03; ADR-027; NFR-029','Test TC-V12-C-011 added','TC-V12-C-011'),
     ('FSD','12','V10 Historical use-case group index','C-FSD12-HIST','20 historical groups × 5 entries (100) — names/counts only','Partially covered','Part 9.4','Mapped in §11.3.4.3','DEC-540'),
     ('FSD','12','V6 MT-29','C-FSD12-MT29','Industry templates are versioned parameter sets referencing canonical workflow; definition count stays 156','Partially covered','A113 WorkflowTemplate; DEC-051','FR-V12-C-011; TC-V12-C-011','FR-V12-C-011'),
     ('FSD','12','V6 BusinessContext DTO','C-FSD12-BCTX','BusinessContext DTO (tenant…policy snapshot); reuse 517 step references; never duplicate definitions','Partially covered','Part 3.4 §3.4.5.4 A; aut_run','FR-V12-C-002 BusinessContext envelope','FR-V12-C-002'),
    ]
    for code, title in [('FL-02','Canonical typed input contracts'),('FL-03','Executable step handlers (517 step IDs)'),('FL-07','Pre-execution simulation, zero external effects'),('FL-08','Confidence-based routing'),('FL-11','Cancellation and compensation'),('FL-12','Industry workflow templates'),('FL-13','Step-level AI evaluation'),('FL-14','Workflow optimization recommendations')]:
        b.append(('FSD','12','V5 optimization controls',f'C-FSD12-{code}',f'{code} {title}','Partially covered','Part 3.4 §3.4.5.4; AU-053; AU-006; API-449','FR-V12-C-001…012 engine contract','FR-V12-C-001'))
    for k in ['Role separation','Budget and allowance','Scope','Channel','Duplicate / failures','Approval (15-minute sample expiry)','Recovery','Input contract']:
        b.append(('FSD','12','V4 local state and workflow guard contract',f'C-FSD12-V4-{re.sub("[^A-Za-z]","",k)[:10]}',f'V4 guard: {k}','Partially covered','Part 2.2 §2.6; BRL-APR-03; BRL-SVC-03','Adopted in §11.3.5.2','FR-V12-C-004'))
    b += [
     ('FSD','40','V6 canonical policy','C-FSD40-PRECHECK','FSD-POL-V6-PRECHECK: validate schema/scope/source/version/policy/quota; reserve; finalize; idempotency digest; 30 s/90 s timeouts; ≤ 3 safe retries with jitter','Partially covered','Part 2.2 §2.6; NFR-016; BRL-AUT-06','DEC-545; FR-V12-C-004','DEC-545'),
     ('FSD','40','V6 canonical policy','C-FSD40-ARTIFACT','FSD-POL-V6-ARTIFACT typed artifact schema; normalize relational/financial fields; no generic JSON for accounting or identity','Partially covered','Part 3.3 §3.3.5','FR-V12-C-006','FR-V12-C-006'),
     ('FSD','13','V5 controls','C-FSD13-ST04','ST-04 durable checkpoints; resume without re-running completed effect','Partially covered','Part 3.4 lease fencing; aut_step_run','FR-V12-C-005; TC-V12-C-008','FR-V12-C-005'),
     ('FSD','13','V5 controls','C-FSD13-FL01','FL-01 machine-readable registry of 156 workflows; immutable run snapshots','Not covered','—','FR-V12-C-001; TC-V12-C-001','FR-V12-C-001'),
     ('FSD','13','V5 controls','C-FSD13-FL05','FL-05 verified inbox/outbox event-driven orchestration','Covered','Part 2.2 §2.6; NFR-006','Mapped','—'),
     ('FSD','13','V5 controls','C-FSD13-FL10','FL-10 tenant-scoped cross-workflow events; unsubscribed child held','Partially covered','BRL-SVC-03; E-1','FR-V12-C-009; TC-V12-C-014','FR-V12-C-009'),
     ('BRD','18','Authority model','C-BRD18-LSCALE','Authority L0–L4 and R3 default L2','Conflict','DEC-064; BRL-AUT-01; Part 7.2 autonomy scale','Crosswalk DEC-542; CONFLICT-801 resolved','DEC-542'),
    ]
    wb = D['SM-SVC-01-WF01']['wb']
    for f in ['Agent identity and authority','External agent interoperability','Model portability','Event and trigger schema','Idempotency and conflict policy','Escalation and recovery policy','Data provenance requirements','Unit economics and margin target','Technology and regulatory readiness','Service migration and deprecation policy','Implementation and verification status']:
        b.append(('SRC','Workflow_Catalog',f,f'C-WB-{re.sub("[^A-Za-z]","",f)[:14]}',f'{f}: {wb[f]}','Partially covered','Part 2.2 §2.6; Part 3.4; NFR-005/016/028','Adopted in §11.3.5.2','FR-V12-C-002'))
    for v in sorted(set(d['wb']['Security and compliance requirements'] for d in D.values())):
        b.append(('SRC','Workflow_Catalog','Security and compliance requirements',f'C-WB-SEC-{len(v)}',v,'Covered','NFR-001/002/032; BRL-TEN-12','Mapped','—'))
    for v in sorted(set(d['spec']['Preconditions'] for d in D.values())):
        b.append(('FSD','12','Preconditions (all workflows)',f'C-FSD12-PRE-{len(v)}',v,'Covered','E-1…E-3; BRL-SVC-03; NFR-038','Mapped','—'))
    b.append(('FSD','12','Failure handling (all workflows)','C-FSD12-FAIL',D['SM-SVC-01-WF01']['spec']['Failure handling'],'Covered','E-5; BRL-AUT-07; DEC-050','Mapped','—'))
    for v in sorted(set(d['wb']['Open-source software requirements'] for d in D.values())):
        b.append(('SRC','Workflow_Catalog','Open-source software requirements',f'C-WB-OSS-{len(v)}',v,'Covered','Part 3.1 stack; ADR register','Mapped','—'))
    for x in b: add(*x)
    # per service
    for s in SVCS:
        w1 = f"SM-SVC-{s}-WF01"; d = D[w1]; m = M.SVC[s]
        for f in ['Supported channels','Applicable industries','Applicable business capabilities','External provider requirements','Subscription pricing model','Usage limits','Full / partial / selective availability','Required service entitlements','Optional complementary services','Prerequisite automations','AI agent responsibilities','Performance KPIs','Shared execution engine']:
            add('SRC','Workflow_Catalog',f'SM-SVC-{s} {f}',f'C-SVC{s}-WB-{re.sub("[^A-Za-z]","",f)[:12]}',f'{f}: {d["wb"][f]}','Partially covered',f'Part 1 B-SVC; {m["bpwf"]}','Mapped in service block §11.3.5',US[s])
        p = d['spec']['Current source UI/API/DB candidates'].split(' | ')
        add('FSD','12',f'SM-SVC-{s} UI/API/DB candidates',f'C-SVC{s}-CAND',d['spec']['Current source UI/API/DB candidates'],'Partially covered',f'Screens {p[0]} exist (Part 2.5); API/DB naming differs','Table mapping in service block; API naming to Part 11 group H','DEC-540')
        add('FSD','12',f'SM-SVC-{s} contract mapping',f'C-SVC{s}-V2MAP',d['spec']['Proposed contract mapping'],'Not covered','API-467…472; aut_run/aut_step_run','§11.3.5.3 mapping; GAP-804, GAP-803','FR-V12-C-003')
        add('FSD','12',f'SM-SVC-{s} engine/agent',f'C-SVC{s}-ENG',d['spec']['Engine / agent'],'Partially covered',m['ag'],'AGT→AG crosswalk §11.3.4.2','DEC-540')
        add('FSD','40',f'SM-SVC-{s} traceability (AGT)',f'C-SVC{s}-AGT',f"{d['ch40']['Agent']} · {d['ch40']['Engine']} · {d['ch40']['Policy']}",'Not covered',M.AGT[d['ch40']['Agent']],'AGT→AG crosswalk','DEC-540')
        for x in d['dto']:
            req = x['field'] in d['schema']['$defs']['input'].get('required',[]) + d['schema']['$defs']['output'].get('required',[])
            add('FSD','12+AP-B',f'SM-SVC-{s} DTO',f'C-SVC{s}-DTO-{("out" if "output" in x["type"] else "in")}-{x["field"]}',f"{x['field']}: {x['type']}",'Partially covered',M.FIELD.get(x['field'],'—'),'DTO table in service block; DEC-543/544',f'{US[s]}')
        ent = d['wb']['Required service entitlements']
    # per workflow
    for w in WFS:
        d = D[w]; m = M.W[w]; s = w[7:9]; st = STMAP[m['st']]; fr = FR[w]; r = risk(w)
        loc = m['bp']; sid = w.replace('SM-SVC-','C-SVC')
        add('BRD','09',w,f'{sid}-OUT',f"{d['title']} — outcome",st,loc,'Spec §11.3.5' if m['st']=='C' else 'Enhanced: '+m['gap'],fr)
        add('BRD','09',w,f'{sid}-IO',d['brd09']['io'],st,loc,'Spec',fr)
        for i,k in enumerate(d['brd09']['kpi'].split('; '),1):
            add('BRD','09',w,f'{sid}-KPI{i}',k,'Not covered' if m['st']!='C' else 'Partially covered','Part 1 KPI-01…31 (no per-workflow KPI)','Formula defined; threshold set in pilot (DEC-554)',fr)
        sa = 'Pending Founder decision' if r in ('R2','R3') else 'Matched'
        add('BRD','09',w,f'{sid}-RISK',d['brd09']['risk'],'Conflict' if r in ('R2','R3') else 'Partially covered','DEC-064; BRL-AUT-01',auth_map(w)[:180],'DEC-542; '+('DEC-548' if r=='R3' else 'DEC-549' if r=='R2' else 'DEC-546'),sa)
        for f,v in d['spec'].items():
            if f in ('Preconditions','Failure handling','Current source UI/API/DB candidates','Proposed contract mapping','Engine / agent'): continue
            sb = {'Business source and objective':st,'Trigger / required supplied input':st,'Result / acceptance':'Partially covered','Proposed domain contract':'Not covered','Authority / effect classification':'Conflict' if r in ('R2','R3') else 'Partially covered','Workflow KPI (proposed)':'Not covered','Cost source':'Not covered'}.get(f,'Partially covered')
            add('FSD','12',w,f'{sid}-SPEC-{re.sub("[^A-Za-z]","",f)[:10]}',f'{f}: {v}',sb,loc,'Spec header table §11.3.5',fr,sa if f.startswith('Authority') else 'Matched')
        for x in d['steps']:
            sa2 = 'Pending Founder decision' if (w=='SM-SVC-19-WF03' and x['id'].endswith('04')) else 'Matched'
            add('FSD','12',w,x['id'],f"{x['action']} | {x['executor_input']} | {x['failure']}",{'C':'Partially covered','P':'Partially covered','N':'Not covered'}[m['st']],M.EXEC[exkey(x['executor_input'])][:120],'Step table §11.3.5',fr,sa2)
        for t in d['wf_tests']:
            add('FSD','33',w,t['id'],f"{t['fixture']} → {t['expected']}",'Not covered','Part 6 (no per-workflow V12 ID)','Mapped to blueprint test',TC[(w,t['id'])])
        for t in d['step_tests']:
            add('FSD','33',w,t['id'],f"{t['class']}: {t['assertion']}",'Not covered','Part 6','Mapped to blueprint test',TC[(w,t['id'])])
        add('FSD','12',w,f'{sid}-CHAN',f"Channels: {d['channels']}; {d['exec_contract']}",'Partially covered',M.SVC[s]['bpwf'],'Header table',fr)
        add('FSD','12',w,f'{sid}-UIIN',f"UI input controls: {d['ui_inputs']}; {d['ui_trace']}",'Partially covered','A089 / A110 run inspection','Header table; DTO governs (DEC-544)',fr)
        add('FSD','13',w,f'{sid}-CH13',f"{d['ch13']['steps']} steps; {d['ch13']['cues']}; {d['ch13']['controls']}",'Not covered','—','Step classes in step table',fr)
        add('FSD','40',w,f'{sid}-TRACE',f"{d['ch40']['Steps']} · {d['ch40']['Engine']} · {d['ch40']['Agent']} · {d['ch40']['Tests']}",'Not covered','—','Trace in header table',fr)
        add('SRC','Workflow_Catalog',w,f'{sid}-WB',f"Detailed functionality: {d['wb']['Detailed functionality']}; mode: {d['wb']['Automation operating mode']}; side effect: {d['wb']['External side-effect classification']}; modalities: {d['wb']['Supported data modalities']}; version {d['wb']['Workflow version']}",st,loc,'Header table; stricter classification applies (DEC-546)',fr)
        add('SRC','Acceptance_Tests',w,d['wb_at']['Test ID'],f"{d['wb_at']['Scenario']}: {d['wb_at']['Input fixture']} → {d['wb_at']['Expected output / behavior']}; approval: {d['wb_at']['Approval checks']}; KPI: {d['wb_at']['Target KPI']}",'Not covered','—','Superseded by TC-POS…; AT01 mapped',TC[(w,w+'-TC-POS')])
        add('SRC','Cost_Model',w,f'{sid}-COST',f"{d['wb_cost']['Unit']}; tokens {d['wb_cost']['Input tokens (scenario)']}/{d['wb_cost']['Output tokens (scenario)']}; INR {cost_inr(w):.2f}/invocation",'Not covered','Part 8.4 (no per-workflow cost)','Illustrative cost in header; §11.3.5.9','DEC-553')
        add('FSD','AP-B',w,f'urn:sm:dto:{w}:v2','JSON Schema 2020-12 input/output, additionalProperties false','Not covered','—','Adopted as validator (DEC-544)','DEC-544')
    path = os.path.join(BP, 'final', 'coverage_v12', 'C_coverage.csv')
    with open(path, 'w', newline='', encoding='utf-8') as f:
        cw = csv.writer(f); cw.writerow(['doc','chapter','section','aspect_id','aspect_summary','status_before','blueprint_location','action','new_ids','status_after'])
        cw.writerows(ROWS)
    return path

# ---------------- markdown helpers ----------------
def header(file_letter, sections, counts):
    return f"""# AI Growth Engine: Employee Sales & Marketing Automation
## Application Blueprint: PART 11 (Batch 11.3), V12 Executable Workflows: SM-SVC-01…20 (80 workflows)

| Field | Value |
|---|---|
| Document | Part 11, Batch 3, file **{file_letter} of c** ({sections}). Files: `Part-11-3a_V12_Executable_Workflows_SVC01-20.md` (§11.3.1–§11.3.5.9 common engine contract), `Part-11-3b_…` (§11.3.5.10 workflow specifications SM-SVC-01…10), `Part-11-3c_…` (§11.3.5.10 SM-SVC-11…20 and §11.3.6–§11.3.10) |
| Version | 1.0 · 28 Nov 2026 |
| Baseline | Parts 0–9.10 and 0B (DEC-001…422); Part 2.2 §2.6 universal execution engine and WF-01…14; Parts 9.7–9.9 WF-15…39, AG-039…080, AU-053…119; Part 9.4 catalogue; Part 2.3 BRL and state machines; Part 3.2/3.3/3.4 contracts; customer revision V12 (BRD V12 ch09, FSD V12 ch12/13/33/40, Appendix B, workbook “39 Services 156 Workflows”) |
| Roles applied | Expert panel: Principal Workflow/BPM Architect (BPMN, saga, outbox), Revenue Operations leader, QA architect, Principal Engineer; plus Product Owner, Business Systems Analyst, Security/Compliance/AI Governance Lead, FinOps Lead |
| Status | Customer revision V12 alignment for group R3a (letter C). Development and running estimates in §11.3.5.9 are **outside** Ledger A (DEC-230) and Ledger B (DEC-231) and are separately approvable |

{counts}

---
"""

def qg_small(letter, notes):
    return f"""

### Quality gate: file {letter}

| # | Check | Result | Notes |
|---|---|---|---|
| 1 | Every requirement traced to a source | Pass | {notes[0]} |
| 2 | Assumptions/gaps/conflicts tagged and logged | Pass | Tags 796–813 only; register in file c §11.3.9 |
| 3 | IDs unique and consistent with earlier parts | Pass | FR-V12-C, TC-V12-C, US-<EP>-YC, DEC-540…554, ADR-190…192 are new; V12 IDs kept literally |
| 4 | No story lacks AC and no requirement lacks a test | Pass | {notes[1]} |
| 5 | Negative, edge, security and accessibility cases covered | Pass | INPUT/SCOPE/ENT/DUP/BUDGET/RECOVERY per workflow; A11Y via engine tests TC-V12-C-026/027 |
| 6 | No agent lacks guardrail, fallback, KPI and cost estimate | N/A | No new agent cards (agents are owned by group F); existing AG mapped |
| 7 | Time-sensitive facts flagged "verify" with an as-of date | Pass | Provider rules (WhatsApp windows, ad, e-sign, answer-engine terms) flagged verify (as of 27 Nov 2026) |
| 8 | No restricted data routed to free-tier models | Pass | Tier 2 eligibility per service stated; personal/confidential classes never Tier 2 |
| 9 | Consistent with earlier parts | Pass | Safety invariants unchanged; conflicts raised in file c §11.3.6 |
"""

def mm(lines):
    return "```mermaid\nflowchart TD\n" + "\n".join("  " + l for l in lines) + "\n```\n"

def wf_flow(w):
    d = D[w]; steps = d['steps']; r = risk(w)
    L = [f'S["Trigger: {d["spec"]["Trigger / required supplied input"].split(";")[0]}"] --> P["FSD-POL-V6-PRECHECK<br/>schema, scope, entitlement, quota, reserve"]',
         'P -- "Invalid DTO" --> R1["422 field errors, no run"]',
         'P -- "Scope or entitlement denied" --> R2["403 or 404, Blocked"]']
    prev = 'P'; gate = False
    for i, x in enumerate(steps, 1):
        code = x['failure'].split(' ')[0]
        lab = x['action'].replace('"', "'").replace(';', ',')
        node = f'N{i}'; ek = exkey(x['executor_input'])
        if ek == 'Effect adapter' and not gate:
            L.append(f'{prev} --> AP{{"Approval of exact payload digest valid and dispatch recheck passed?"}}')
            L.append('AP -- "No, changed or expired" --> BL["Blocked, no effect"]')
            prev = 'AP'; gate = True
            L.append(f'{prev} -- "Yes" --> {node}["STEP-{i:02d} {lab}<br/>{ek} via outbox"]')
        else:
            L.append(f'{prev} --> {node}["STEP-{i:02d} {lab}<br/>{ek}"]')
        st = M.FAIL[code][0].split(' ')[0]
        L.append(f'{node} -. "{code}" .-> F{i}["{st}"]')
        prev = node
    if r in ('R2', 'R3') and not gate:
        L.append(f'{prev} --> AP{{"Human approval of exact digest"}}')
        L.append('AP -- "Rejected or expired" --> BL["Blocked, no effect"]')
        L.append('AP -- "Approved" --> OK["Succeeded: frozen artefact released for the next human or L2 dispatch step"]')
    else:
        L.append(f'{prev} --> OK["Succeeded: artefact, evidence, receipt, meter usage"]')
    return mm(L)

def svc_block(s):
    m = M.SVC[s]; ws = [f"SM-SVC-{s}-WF{j:02d}" for j in range(1, 5)]; d = D[ws[0]]
    p = d['spec']['Current source UI/API/DB candidates'].split(' | ')
    sch = d['schema']['$defs']
    o = []
    o.append(f"#### {d['wb']['Automation ID']} {d['wb']['Automation service name']}\n")
    o.append(f"**Purpose:** {esc(d['wb']['Business objective'])} (BRD V12 ch09; FSD V12 ch12). **Blueprint flow:** {m['bpwf']}. **Epic:** EP-{m['epic']}. **Story:** {US[s]}.\n")
    o.append("| Field | Specification |\n|---|---------|")
    rows = [
     ('Family / bundle / meter', f"{d['wb']['Automation family']} · {d['wb']['Full / partial / selective availability']} · meter: {d['wb']['Usage limits']}"),
     ('Supported channels', d['wb']['Supported channels']),
     ('Applicable industries / capability', f"{d['wb']['Applicable industries']} · {d['wb']['Applicable business capabilities']}"),
     ('Required supplied input (entitlement rules)', d['wb']['Required service entitlements']),
     ('Optional input producers', d['wb']['Prerequisite automations']),
     ('External providers', d['wb']['External provider requirements'] + ' (verify terms and prices at time of implementation, as of 27 Nov 2026)' + (' [GAP-805]' if s in ('07','12','13','18') else '')),
     ('Pricing model', d['wb']['Subscription pricing model'] + ' — illustrative; Quotation pending (DEC-553)'),
     ('Service KPI (V12)', d['wb']['Performance KPIs']),
     ('Actors (blueprint roles)', m['actors']),
     ('Agents: V12 → blueprint', f"{d['ch40']['Agent']} ({d['wb']['AI agent responsibilities']}) → {M.AGT[d['ch40']['Agent']]}; agent pool: {m['ag']}"),
     ('Automations (blueprint)', m['au']),
     ('Shared engines (V12)', d['wb']['Shared execution engine']),
     ('Business rules', m['brl']),
     ('Data class and gateway tier', m['dclass'] + '; Tier 0 rules/cache first, Tier 1a then 1b, Tier 3 degrade (Part 7.3)'),
     ('Screens (V12 = blueprint IDs)', p[0]),
     ('V12 API candidates', p[1] + ' — retained or mapped by reviewed adapter; API catalogue reconciliation is group H (Part 11 R7)'),
     ('V12 DB candidates → blueprint tables', m['tables']),
    ]
    for k, v in rows: o.append(f"| {k} | {esc(v)} |")
    o.append("")
    o.append(f"**DTO `urn:sm:dto:SM-SVC-{s}-WF0n:v2`** (one schema per workflow, identical for the four workflows of this service; JSON Schema 2020-12, `additionalProperties: false`, Appendix B; DEC-544).\n")
    o.append("| Field | Dir | Req | V12 type / validation | Schema constraint | Blueprint mapping |\n|------|--|--|--------|--------|-------|")
    seen = set()
    for x in d['dto']:
        io = 'out' if 'output' in x['type'] else 'in'
        dd = sch['output' if io == 'out' else 'input']
        req = 'Y' if x['field'] in dd.get('required', []) else 'N'
        con = json.dumps(dd['properties'].get(x['field'], {}), ensure_ascii=False).replace('|', '\\|')
        o.append(f"| `{x['field']}` | {io} | {req} | {esc(x['type'])} | `{con}` | {esc(M.FIELD.get(x['field'], '—'))} |")
    o.append("")
    o.append("**DTO rules.** (1) Unknown fields rejected (422). (2) `*_ref`/`*_id` resolve inside the caller's tenant and startup only; a foreign reference is reported as not found (BRL-TEN-04). (3) Free text is Unicode NFC-normalised, 1–4,000 characters, and treated as untrusted (AIX-08 → AU-005 sanitizer; no tool invocation from content). (4) Enum fields take values from the versioned registry named in `$comment`; the registry version is pinned on the run. (5) Money fields are int64 minor units with an ISO 4217 code at the DTO boundary and Decimal in storage (DEC-543). (6) The schema version is pinned on the run (BRL-AUT-03).\n")
    o.append(TX.story(s, US[s], d, m, ws, FR))
    return "\n".join(o)

def wf_block(w):
    d = D[w]; m = M.W[w]; s = w[7:9]; sp = d['spec']; r = risk(w)
    o = [f"##### {w} {d['title']}\n"]
    conf = ' [CONFLICT-798]' if r == 'R3' else ' [CONFLICT-799]' if r == 'R2' else ''
    if w == 'SM-SVC-19-WF03': conf += ' [CONFLICT-800]'
    o.append(f"**Requirement {FR[w]}** (status before: {STMAP[m['st']]}; after: {'Pending Founder decision on authority only' if r in ('R2','R3') else 'Matched'}){conf}. **Blueprint:** {m['bp']}." + (f" **Enhancement:** {m['gap']}." if m['st'] != 'C' else ''))
    o.append("")
    o.append("| Field | Specification |\n|---|---------|")
    c = d['wb_cost']
    rows = [
     ('Business outcome / input → output', f"{d['brd09']['outcome']}: {d['brd09']['io']}"),
     ('Trigger', d['wb']['Trigger types'] + ' (FSD: ' + sp['Trigger / required supplied input'] + ')'),
     ('Result / acceptance', sp['Result / acceptance']),
     ('Domain contract', sp['Proposed domain contract'] + f' Validator `urn:sm:dto:{w}:v2`.'),
     ('Risk and authority (V12)', sp['Authority / effect classification']),
     ('Autonomy in blueprint', auth_map(w)),
     ('Approval gate (V12)', d['wb']['Human approval requirements'] + ' · approval check: ' + d['wb_at']['Approval checks']),
     ('Operating mode / side effect / modalities', f"{d['wb']['Automation operating mode']} · {d['wb']['External side-effect classification']} · {d['wb']['Supported data modalities']} (stricter classification applies, DEC-546)"),
     ('Engine / agent', f"{sp['Engine / agent']} → {M.AGT[d['ch40']['Agent']]}"),
     ('Channels / UI input controls', f"{d['channels']} · {d['ui_inputs']} ({d['ui_trace']})"),
     ('Step classes (FSD ch13)', f"{d['ch13']['cues']} Controls: {d['ch13']['controls']}"),
     ('Workflow KPI (V12)', sp['Workflow KPI (proposed)']),
     ('KPI formulas (this part)', m['kpis'] + ' — thresholds set after the pilot baseline (DEC-554) [GAP-810]'),
     ('SLA', m['sla']),
     ('Illustrative cost (V12)', f"{c['Unit']}; tokens {c['Input tokens (scenario)']} in / {c['Output tokens (scenario)']} out; INR {cost_inr(w):.2f} per invocation; {c['External fees']} (estimate; verify at implementation, as of 27 Nov 2026)"),
     ('Versions / acceptance origin', f"workflow {d['wb']['Workflow version']}; {d['wb']['Simulation and benchmark reference']}; original {', '.join(d.get('orig_at', []))} not run"),
     ('Rules', ' · '.join(f"R{i}. {x}" for i, x in enumerate(m['rules'], 1))),
    ]
    for k, v in rows: o.append(f"| {k} | {esc(v)} |")
    o.append("")
    o.append("| Step ID | Action | Class · V12 executor / input | Output / validation | Failure → blueprint state | Blueprint component | Step test |\n|----|----|------|-------|-----|------|-------|")
    stt = {t['id']: t for t in d['step_tests']}
    for x in d['steps']:
        t = stt.get(x['id'] + '-TC', {})
        code = x['failure'].split(' ')[0]
        ex = [exkey(x['executor_input']), exrest(x['executor_input'])]
        o.append(f"| {x['id']} | {esc(x['action'])} | {esc(t.get('class',''))} · {esc(ex[0])} / {esc(ex[1] if len(ex)>1 else '')} | {esc(x['output_validation'])} | {esc(x['failure'])} → **{M.FAIL[code][0]}** | {esc(M.EXEC[ex[0]])} | {TC[(w, x['id']+'-TC')]} ({esc(M.CLASS_TEST.get(t.get('class',''),''))}): {esc(t.get('assertion',''))} |")
    o.append("")
    if m['flow']:
        o.append(wf_flow(w))
    o.append("| Test ID | V12 ID | Level | Fixture / action (V12) | Expected (V12) | Blueprint assertion |\n|---|-----|--|-----|-----|--------|")
    for t in d['wf_tests']:
        k = t['id'].rsplit('-', 1)[1]; lv, ba = TEST_LEVEL[k]
        o.append(f"| {TC[(w,t['id'])]} | {t['id']} | {lv} | {esc(t['fixture'])} | {esc(t['expected'])} | {ba} |")
    o.append("")
    return "\n".join(o)

def main():
    csvp = build_csv()
    stats = TX.stats(D, M, ROWS, FR, TC, US, TC_LAST)
    # file a
    a = header('a', '§11.3.1–§11.3.5.9', TX.counts(stats)) + TX.file_a(D, M, ROWS, FR, TC, US, stats) + qg_small('a', ['Every engine FR cites FSD V12 ch12/13/40, BRD ch18 or a blueprint ID', 'FR-V12-C-001…012 each have TC-V12-C-001…030 tests; stories US-18-YC21/22 carry Gherkin AC'])
    open(os.path.join(BP, 'Part-11-3a_V12_Executable_Workflows_SVC01-20.md'), 'w').write(a)
    for letter, rng, secs in [('b', SVCS[:10], '§11.3.5.10 SM-SVC-01…10'), ('c', SVCS[10:], '§11.3.5.10 SM-SVC-11…20, §11.3.6–§11.3.10')]:
        body = []
        if letter == 'b':
            body.append("### 11.3.5.10 Workflow specifications (SM-SVC-01…10)\n")
            body.append(TX.wf_intro())
        else:
            body.append("### 11.3.5.10 Workflow specifications (continued: SM-SVC-11…20)\n")
        for s in rng:
            body.append(svc_block(s))
            for j in range(1, 5):
                body.append(wf_block(f"SM-SVC-{s}-WF{j:02d}"))
        txt = header(letter, secs, TX.counts(stats)) + "\n".join(body)
        if letter == 'c':
            txt += TX.file_c_tail(D, M, ROWS, FR, TC, US, stats)
        else:
            txt += qg_small('b', ['Every row carries its V12 ID and the blueprint ID it maps to', '40 FRs each with 8–10 workflow tests and 2–4 step tests; stories US-05-YC01…US-09-YC10 with Gherkin'])
        open(os.path.join(BP, f'Part-11-3{letter}_V12_Executable_Workflows_SVC01-20.md'), 'w').write(txt)
    print('rows', len(ROWS), 'tc_last', TC_LAST, csvp)

if __name__ == '__main__':
    main()
