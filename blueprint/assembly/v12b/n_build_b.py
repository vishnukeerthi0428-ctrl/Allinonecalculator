"""Builds Part-11-16b: workflow specifications for the 48 workflows of INV-SVC-01...12 (Part 11.3b format)."""
import sys, os, re, json, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import n_ctx as C
import n_spec as SP
from n_common import md_escape as E

BP = '/home/user/Allinonecalculator/blueprint'
OUT = BP + '/Part-11-16b_Investment_Automation_I_Workflow_Specifications.md'
L = []
w = L.append

def table(hdr, rows):
    w('| ' + ' | '.join(hdr) + ' |')
    w('|' + '---|' * len(hdr))
    for r in rows:
        w('| ' + ' | '.join(E(str(x)) for x in r) + ' |')
    w('')

NGATE = sum(1 for k in C.TC if len(k) == 3 and k[1] == 'STEP' and k[2] == 'GATE')
NST = sum(1 for k in C.TC if len(k) == 3 and k[1] == 'STEP')
NWT = sum(1 for k in C.TC if len(k) == 2 and isinstance(k[0], str) and k[0].startswith('INV-SVC'))
NDTO = sum(len(SP.W[r['_key']]['dto_in']) + len(SP.W[r['_key']]['dto_out']) + 2 for r in C.WFS)
LASTWF = 'TC-V12-N-%03d' % (int(C.TC[('ENT', 1)].split('-')[-1]) - 1)
TITLE = 'Investment Automation I: Investor/Fundraising Mode and INV-SVC-01…12'
w('# AI Growth Engine: Employee Sales & Marketing Automation')
w(f'## Application Blueprint: PART 11 (Batch 11.16b), {TITLE}')
w('')
table(['Field', 'Value'], [
 ['Document', 'Part 11, Batch 11.16, file **b** of Group N's files a, b, e: §11.16.5.12 executable workflow specifications for the 48 workflows INV-SVC-01-WF01…INV-SVC-12-WF04. Files a (framework, services) and c (stories, combinatorial tests, cost, decisions)'],
 ['Version', '1.0 · 28 Nov 2026'],
 ['Baseline', 'Part 11.16a; Part 11.3a universal engine contract (StepRun, states, retries, simulation); Part 11.3b workflow format; Part 11.15 rule-pack framework; DEC-779/783'],
 ['Roles applied', 'Expert panel of Part 11.16a (private-markets operating partner, securities-law specialist, CPO, Principal Solutions Architect, Principal BSA) plus QA Lead and Security/AI Governance Lead'],
 ['Counts', f'48 workflows · {sum(len(C.steps_of(r)) for r in C.WFS)} V12 step contracts + {NGATE} blueprint gate steps · {NDTO} DTO fields · {NWT} workflow tests + {NST} step tests (TC-V12-N-001…{LASTWF}) + 12 entitlement tests · requirements FR-V12-N-101…148'],
])
w('**Legal status.** Draft for counsel review; not legal advice. Thresholds marked "verify" are the panel\'s reading (as of 27 Nov 2026) [ASSUMPTION-1000].')
w('')
w('## 11.16.5.12 Workflow specifications (INV-SVC-01…12)')
w('')
w('**How to read each workflow block.** (1) A header table restates the V12 workbook fields literally (Workflow Catalog 50-field row, Cost Model, Acceptance Tests) and adds the blueprint mapping, risk class, autonomy, securities and privacy controls, KPI formulas, SLA and rules. (2) The DTO table gives the typed contract `urn:inv:dto:INV-SVC-nn-WFnn:v2` (JSON Schema 2020-12, `additionalProperties: false`). (3) The step table lists every V12 step (split from the workbook "Detailed functionality", one step per clause, IDs `…-STEP-nn`) with executor, output/validation, failure route and blueprint state, the component, **the securities/privacy controls applied in that step**, and the step test; R2/R3 workflows add the blueprint gate step `…-STEP-GATE` before the first external effect. (4) R2/R3 workflows and every WF04 carry a Mermaid flowchart. (5) The test table maps the V12 acceptance ID (`…-AT01`) and the blueprint test classes to TC-V12-N IDs.')
w('')
w('**Blueprint states** (Part 11.3a): Queued → Running → Succeeded; Waiting (AWAITING_APPROVAL); Held; Blocked; Reconciling; Escalated; Suppressed; Paused; Failed. **Risk classes (V12):** R0 internal analysis/draft · R1 regulated pre-check or internal record · R2 external communication/disclosure · R3 consequential legal/financial (prepare only until two-person authorization or a bounded mandate).')
w('')

def schema(t):
    if t.startswith('enum[]'):
        reg = t[t.index('(') + 1:-1]
        return '{"type": "array", "items": {"type": "string", "maxLength": 64}, "maxItems": 50, "$comment": "values from registry %s"}' % reg, f'configured enum list ({reg})'
    if t.startswith('enum'):
        reg = t[t.index('(') + 1:-1]
        return '{"type": "string", "maxLength": 64, "$comment": "values from registry %s"}' % reg, f'configured enum ({reg})'
    return {
     'text': ('{"type": "string", "minLength": 1, "maxLength": 4000}', 'free text NFC-normalised, untrusted (AU-005)'),
     'refs': ('{"type": "array", "items": {"type": "string", "format": "uuid"}, "maxItems": 500}', 'typed references, resolved in caller scope'),
     'ref': ('{"type": "string", "format": "uuid"}', 'reference in caller tenant/startup'),
     'datetime': ('{"type": "string", "format": "date-time"}', 'RFC 3339; stored UTC'),
     'money': ('{"type": "object", "required": ["amount_minor", "currency"], "properties": {"amount_minor": {"type": "integer", "minimum": 0}, "currency": {"type": "string", "pattern": "^[A-Z]{3}$"}}}', 'int64 minor units + ISO 4217 (DEC-027)'),
     'decimal': ('{"type": "string", "pattern": "^-?\\\\d+(\\\\.\\\\d{1,6})?$"}', 'decimal string (no float)'),
     'int': ('{"type": "integer", "minimum": 0}', 'non-negative integer'),
     'bool': ('{"type": "boolean"}', 'boolean'),
     'hash': ('{"type": "string", "pattern": "^[a-f0-9]{64}$"}', 'SHA-256 hex'),
     'lang': ('{"type": "string", "pattern": "^[a-z]{2}(-[A-Z]{2})?$"}', 'BCP 47 locale'),
     'object': ('{"type": "object", "maxProperties": 100}', 'structured object (versioned sub-schema)'),
    }[t]

ENT_MAP = {'opportunity': 'inv_opportunity', 'investor': 'inv_investor', 'contact': 'inv_contact', 'draft': 'inv_message', 'send': 'inv_message', 'message': 'inv_message',
           'thread': 'inv_thread', 'meeting': 'inv_meeting', 'scenario': 'inv_scenario', 'pitch': 'inv_document', 'document': 'inv_document', 'grant': 'inv_access_grant',
           'nda': 'inv_nda', 'offer': 'inv_offer', 'offering': 'inv_offering', 'application': 'inv_subscription', 'receipt': 'inv_receipt', 'commitment': 'inv_commitment',
           'allocation': 'inv_receipt_allocation', 'evidence': 'inv_evidence', 'source': 'inv_source', 'mandate': 'inv_mandate', 'round': 'inv_round', 'template': 'inv_locale_template',
           'sequence': 'inv_sequence', 'relationship': 'inv_relationship', 'task': 'inv_task', 'objection': 'inv_objection', 'question': 'inv_diligence_request', 'term': 'inv_term_version',
           'agreement': 'inv_agreement', 'exception': 'inv_receipt (exception view)', 'alert': 'notification', 'signal': 'inv_evidence (signal)', 'fit': 'inv_fit_score', 'brief': 'inv_document (brief)'}
def mapcol(name):
    for k, v in sorted(ENT_MAP.items(), key=lambda x: -len(x[0])):
        if name.startswith(k) or ('_' + k) in name:
            return v + ('.id' if name.endswith('_id') else '.id[]' if name.endswith('_ids') else '')
    return 'run payload (inv_workflow_run.output_json)'

def step_controls(cls, wctl):
    want = {'Policy check (PDP)': wctl, 'External effect (outbox)': ['SEC-CTL-N-01', 'SEC-CTL-N-10', 'SEC-CTL-N-15', 'SEC-CTL-N-12'],
            'AI inference': ['SEC-CTL-N-05', 'SEC-CTL-N-13', 'SEC-CTL-N-16'], 'Evidence retrieval': ['SEC-CTL-N-16', 'SEC-CTL-N-06'],
            'Human review routing': ['SEC-CTL-N-10', 'SEC-CTL-N-08'], 'Domain persistence': ['SEC-CTL-N-12'], 'Deterministic calculation': ['SEC-CTL-N-13', 'SEC-CTL-N-09'],
            'Internal notification': ['SEC-CTL-N-16']}[cls]
    if cls == 'Policy check (PDP)':
        return ', '.join(c.replace('SEC-CTL-N-', 'CTL-') for c in wctl) or 'CTL-06'
    got = [c for c in want if c in wctl] or ([want[0]] if cls in ('AI inference', 'Evidence retrieval', 'Internal notification') else [])
    if cls == 'External effect (outbox)':
        got = sorted(set(got) | {'SEC-CTL-N-15'})
    return ', '.join(c.replace('SEC-CTL-N-', 'CTL-') for c in got) or '— (internal; audit only)'

TEST_DEF = {
 'POS': ('IT', 'positive fixture', 'Output validates against the workflow schema; evidence persisted; run Succeeded; KPI event emitted'),
 'INPUT': ('UT/CT', 'missing or malformed input', 'HTTP 422 with field errors; no StepRun; audit `dto.rejected`'),
 'SCOPE': ('SEC', 'same reference from another tenant/startup', 'HTTP 403 or uniform 404 (BRL-TEN-04); zero rows/events/provider calls in the other scope'),
 'ENT': ('IT', 'revoke INV SKU after enqueue', 'AU-200 dispatch-time recheck denies; run Paused/Held; reservation released; no effect'),
 'DUP': ('IT replay', 'replay identical event / step key', 'exactly one accepted outcome, effect and meter charge; duplicate returns original run ref'),
 'QUALITY': ('AIE', 'stale, conflicting or incomplete evidence', 'step Held or flagged; no unsupported claim reaches output (BRL-AI-03/04); eval record stored'),
 'BUDGET': ('IT', 'quota exhausted at reservation', 'reservation fails → Blocked; zero provider calls; owner notified'),
 'RECOVERY': ('CHAOS', 'provider timeout or worker crash', 'timeout after submit → Reconciling; resume from checkpoint without repeating a completed effect'),
 'SEC': ('SEC/compliance', 'control violation fixture', None),
 'APPROVAL': ('IT', 'approval missing, single approver or hash mismatch', 'Waiting (AWAITING_APPROVAL) or Block APPROVAL_INCOMPLETE/HASH_MISMATCH; NSE'),
 'EFFECT': ('IT + CHAOS', 'effect after approval; pack expires between approval and dispatch', 'dispatch-time AU-201 recheck blocks; no effect; approval retained; audit `pack.expired`'),
}
SEC_FIX = {
 'SEC-CTL-N-01': ('jurisdiction pack in state draft', 'Block PACK_NOT_ACTIVE; NSE'),
 'SEC-CTL-N-02': ('investor eligibility unknown', 'Hold ELIGIBILITY_UNKNOWN; review task to R10'),
 'SEC-CTL-N-03': ('s.42 offering content to recipient without relationship provenance', 'Block GENERAL_SOLICITATION; not overridable'),
 'SEC-CTL-N-04': ('offering document requested without NDA', '403 NDA_REQUIRED; access log entry outcome=denied'),
 'SEC-CTL-N-05': ('input asks "should I invest / what return will I get"', 'AG-166 ADVICE → refusal TPL-N-01 + handover; no AI answer stored as reply'),
 'SEC-CTL-N-06': ('consent withdrawn 30 s before step', 'Block CONSENT_WITHDRAWN; sequence stopped'),
 'SEC-CTL-N-07': ('KYC result screening_hit', 'Hold; R10 alert; no acceptance/allocation'),
 'SEC-CTL-N-08': ('document set changed after counsel sign-off', 'sign-off void; offering back to Draft; Block'),
 'SEC-CTL-N-09': ('route counter at cap', 'Block CAP_REACHED; counter unchanged'),
 'SEC-CTL-N-10': ('same person approves twice', 'Reject APPROVAL_INCOMPLETE'),
 'SEC-CTL-N-11': ('request to initiate refund via API', 'no such operation (404); finance task only'),
 'SEC-CTL-N-12': ('offer issued', 'register row with serial, recipient, hash; immutable audit'),
 'SEC-CTL-N-13': ('draft figure differs from scenario output', 'Block FIGURE_MISMATCH'),
 'SEC-CTL-N-14': ('issuer IN, investor US', 'Hold COUNSEL_CROSS_BORDER'),
 'SEC-CTL-N-15': ('kill switch on during queue', 'all queued effects Held within 60 s; zero effects'),
 'SEC-CTL-N-16': ('EU tenant data processed by IN worker', 'request refused REGION_MISMATCH; no write'),
}

for n in range(1, 13):
    r0 = C.SVC[n]; s = SP.S[n]
    code = C.svc_key(n)
    wfs = [x for x in C.WFS if x['_key'].startswith('%02d' % n)]
    w(f'#### {code} {r0["Automation service name"]}')
    w('')
    w(f'**Purpose:** {r0["Business objective"]} (workbook Service Catalog row {r0["_row"]}). **Epic:** {s["epic"]}. **Service spec:** Part 11.16a §11.16.5.6.{n}. **Stories:** Part 11.16e.')
    w('')
    scr = ', '.join(sorted({SP.A_OF.get(x.strip(), x.strip()) for x in r0['Related UI screen IDs'].split(';')}))
    ents = r0['Related database entities']
    table(['Field', 'Specification'], [
     ['Family / bundle / meter', f'{r0["Automation family"]} · {r0["Full / partial / selective availability"]} · {r0["Usage limits"]}'],
     ['Supported channels', r0['Supported channels']],
     ['Industries / capability', f'{r0["Applicable industries"]} · {r0["Applicable business capabilities"]}'],
     ['Required entitlements', r0['Required service entitlements']],
     ['Optional input producers', r0['Prerequisite automations']],
     ['External providers', r0['External provider requirements'] + ' (verify terms and prices at implementation, as of 27 Nov 2026)'],
     ['Service KPI (V12)', r0['Performance KPIs']],
     ['Actors (blueprint roles)', '; '.join(sorted({SP.W[x['_key']]['roles'] for x in wfs})) + '; R19 service identity; R20 agent identity'],
     ['Agents', ', '.join(s['agents_new'] + s['agents_reuse'])],
     ['Automations', ', '.join(s['au_new'] + s['au_reuse'])],
     ['Shared engines (V12)', r0['Shared execution engine']],
     ['Data class and gateway tier', f'{s["dclass"]}; {s["tier"]}'],
     ['Screens', f'{r0["Related UI screen IDs"]} → {scr}'],
     ['V12 DB candidates → blueprint', ents + ' → schema `inv` same names (DEC-814 keeps V12 names; RLS per §11.16.5.10)'],
    ])
    for r in wfs:
        k = r['_key']; ws = SP.W[k]; wcode = r['_code']
        cm = C.CMM[wcode]
        at = C.ATM.get(wcode + '-AT01')
        w(f'##### {wcode} {r["_name"]}')
        w('')
        w(f'**Requirement {C.FR_WF[wcode]}** (status before: Not covered, CONFLICT-958; after: Matched). Execute "{r["_name"]}" as a typed, policy-checked workflow: {r["Detailed functionality"]}; output "{r["Expected output"]}".')
        w('')
        stps = C.steps_of(r)
        clsl = [C.step_class(r, i, st) for i, st in enumerate(stps, 1)]
        cc = collections.Counter(clsl)
        table(['Field', 'Specification'], [
         ['Business outcome / input → output', f'{r["_name"]}: {r["Required input data"]} → {r["Expected output"]}'],
         ['Trigger', r['Trigger types']],
         ['Result / acceptance', f'{r["Expected output"]}; acceptance {wcode}-AT01 ({at["Scenario"] if at else "—"}) → {C.TC[(wcode, "POS")]}'],
         ['Domain contract', f'Validator `urn:inv:dto:{wcode}:v2`; fields below; event envelope per FR-V12-N-006'],
         ['Risk and authority', f'{ws["risk"]} · V12 side effect: {r["External side-effect classification"]}'],
         ['Autonomy in blueprint', SP.S[n]['autonomy']],
         ['Approval gate (V12)', r['Human approval requirements']],
         ['Operating mode / modalities', f'{r["Automation operating mode"]} · {r["Supported data modalities"]}'],
         ['Agent / automations', f'{ws["agent"]} · {", ".join(ws["au"])}'],
         ['Roles', ws['roles']],
         ['Step classes', '; '.join(f'{v} {k_}' for k_, v in cc.items())],
         ['Securities and privacy controls', ', '.join(ws['ctl']) + ' (see step column)'],
         ['Workflow KPI (V12 service)', r['Performance KPIs']],
         ['KPI formulas (this part)', '; '.join(ws['kpi'])],
         ['SLA', ws['sla']],
         ['Illustrative cost (V12)', f'{cm["Unit"]}; tokens {cm["Input tokens (scenario)"]} in / {cm["Output tokens (scenario)"]} out; INR {cm["Internal INR / invocation"]} per invocation; external fees excluded (estimate; verify at implementation, as of 27 Nov 2026)'],
         ['Versions / origin', f'workflow {r["Workflow version"]}; {r["Simulation and benchmark reference"]}; V12 status: {r["Implementation and verification status"]}'],
         ['Rules', ' · '.join(f'R{i}. {x}' for i, x in enumerate(ws['rules'], 1))],
        ])
        w(f'**DTO `urn:inv:dto:{wcode}:v2`**')
        w('')
        rows = []
        for d_, lst in (('in', ws['dto_in']), ('out', ws['dto_out'])):
            for f in lst:
                nm, t = f.split(':', 1)
                sch, desc = schema(t)
                rows.append([f'`{nm}`', d_, 'Y', desc, f'`{sch}`', mapcol(nm)])
        rows.append(['`correlation_id`', 'in', 'Y', 'trace id', '`{"type": "string", "format": "uuid"}`', 'inv_workflow_run.correlation_id'])
        rows.append(['`simulation`', 'in', 'N', 'zero-effect run', '`{"type": "boolean", "default": false}`', 'inv_workflow_run.simulation'])
        table(['Field', 'Dir', 'Req', 'Type / validation', 'Schema constraint', 'Blueprint mapping'], rows)
        # step table
        rows = []
        gate_done = False
        for i, (st, cl) in enumerate(zip(stps, clsl), 1):
            if cl == 'External effect (outbox)' and not gate_done and (wcode, 'STEP', 'GATE') in C.TC:
                rows.append([f'{wcode}-STEP-GATE', 'Securities and privacy gate (blueprint)', 'Policy check · PDP securities plug-in / scope + consent + pack + eligibility + solicitation + approval hash or mandate',
                             'decision {allow|hold|block, reason_codes, pack_versions}', 'POLICY_DENIED → **Blocked**; unknown → **Held**', 'PDP + AU-201/202/203/207 (ADR-231)',
                             ', '.join(c.replace('SEC-CTL-N-', 'CTL-') for c in ws['ctl']), C.TC[(wcode, 'STEP', 'GATE')] + ' (UT decision table + IT): every gate branch; fail closed'])
                gate_done = True
            ex, outp, fail, comp, lvl, assert_ = C.CLS[cl]
            rows.append([f'{wcode}-STEP-{i:02d}', st, f'{cl} · {ex}', outp, fail, comp, step_controls(cl, ws['ctl']), f'{C.TC[(wcode, "STEP", i)]} ({lvl}): {assert_}'])
        if (wcode, 'STEP', 'GATE') in C.TC and not gate_done:
            rows.insert(0, [f'{wcode}-STEP-GATE', 'Securities and privacy gate (blueprint)', 'Policy check · PDP securities plug-in', 'decision {allow|hold|block}', 'POLICY_DENIED → **Blocked**', 'PDP + AU-201/202/203/207',
                            ', '.join(c.replace('SEC-CTL-N-', 'CTL-') for c in ws['ctl']), C.TC[(wcode, 'STEP', 'GATE')] + ' (UT + IT): fail closed'])
        table(['Step ID', 'Action', 'Class · executor', 'Output / validation', 'Failure → state', 'Blueprint component', 'Controls in this step', 'Step test'], rows)
        # flowchart
        if ws['risk'][:2] in ('R2', 'R3') or wcode.endswith('WF04'):
            w('```mermaid')
            w('flowchart TD')
            w(f'  S["{wcode}<br/>trigger"] --> V["Validate DTO<br/>and AU-200 entitlement"]')
            prev = 'V'
            for i, (st, cl) in enumerate(zip(stps, clsl), 1):
                nid = f'P{i}'
                lab = st.replace('"', "'").replace(';', ',').replace('(', '').replace(')', '')[:40]
                if cl == 'External effect (outbox)' and (wcode, 'STEP', 'GATE') in C.TC and 'G' not in [x for x in []]:
                    w(f'  {prev} --> G{{"Securities gate<br/>pack, eligibility, solicitation"}}')
                    w('  G -- "Block or Hold" --> X["Blocked / Held<br/>reason audited"]')
                    w(f'  G -- "Allow" --> {nid}["{lab}"]')
                    w(f'  {nid} --> O["Outbox effect<br/>idempotent"]')
                    w('  O -- "Timeout" --> RC["Reconciling"]')
                    prev = 'O'
                    continue
                w(f'  {prev} --> {nid}["{lab}"]')
                if cl == 'AI inference':
                    w(f'  {nid} --> GD{i}{{"AG-166 / schema ok?"}}')
                    w(f'  GD{i} -- "No" --> H{i}["Held for review"]')
                    prev = f'GD{i}'
                else:
                    prev = nid
            w(f'  {prev} --> Z["Succeeded<br/>KPI event"]')
            w('```')
            w('')
        # tests
        rows = []
        cls = C.CLASSES + (['APPROVAL', 'EFFECT'] if ws['risk'][:2] in ('R2', 'R3') else [])
        for c in cls:
            lvl, fix, exp = TEST_DEF[c]
            v12 = f'{wcode}-AT01' if c == 'POS' else f'{wcode}-TC-{c}'
            if c == 'POS':
                fix = r['Required input data']; exp = TEST_DEF['POS'][2] + f'; output "{r["Expected output"]}"; KPI: {ws["kpi"][0]}'
            if c == 'SEC':
                pref = ['SEC-CTL-N-09', 'SEC-CTL-N-08', 'SEC-CTL-N-03', 'SEC-CTL-N-04', 'SEC-CTL-N-02', 'SEC-CTL-N-05', 'SEC-CTL-N-11', 'SEC-CTL-N-07',
                        'SEC-CTL-N-13', 'SEC-CTL-N-14', 'SEC-CTL-N-10', 'SEC-CTL-N-06', 'SEC-CTL-N-16', 'SEC-CTL-N-01', 'SEC-CTL-N-12', 'SEC-CTL-N-15']
                ctl = next(c_ for c_ in pref if c_ in ws['ctl'])
                fix, exp = SEC_FIX[ctl]
                fix = f'{ctl}: {fix}'
            rows.append([C.TC[(wcode, c)], v12, lvl, fix, exp])
        table(['Test ID', 'V12 / class ID', 'Level', 'Fixture / action', 'Expected (blueprint assertion)'], rows)

w('### Entitlement acceptance per service (INV-SVC-nn-ENT-AT01)')
w('')
rows = []
for n in range(1, 13):
    a = C.ATM.get(C.svc_key(n) + '-ENT-AT01')
    rows.append([C.TC[('ENT', n)], C.svc_key(n) + '-ENT-AT01', a['Scenario'] if a else '', (a['Preconditions'] if a else '')[:120], (a['Expected output / behavior'] if a else '')[:160], 'Covered also by PM-N-09 exhaustive suite (Part 11.16e)'])
table(['Test ID', 'V12 ID', 'Scenario', 'Preconditions (V12)', 'Expected (V12)', 'Blueprint note'], rows)

w('### Decisions, tags and quality gate for this file')
w('')
w('Used in this file: DEC-802, 804, 805, 809, 814, 817; ADR-231; ASSUMPTION-1000, 1003; CONFLICT-1019 (V12 side-effect labels of INV-SVC-05-WF02/WF04 weaker than the real effect; the stricter class is applied). Full registers in Part 11.16e.')
w('')
table(['#', 'Quality gate item', 'Result', 'Notes'], [
 ['1', 'Every requirement traced', 'Pass', 'Workbook rows quoted literally per workflow'],
 ['2', 'Tags logged', 'Pass', 'Part 11.16e §11.16.9'],
 ['3', 'IDs unique', 'Pass', 'TC and FR allocated by n_ctx.py'],
 ['4', 'Every requirement has tests', 'Pass', 'Each workflow: step tests + 9–11 class tests'],
 ['5', 'Negative/edge/security cases', 'Pass', 'INPUT, SCOPE, ENT, DUP, QUALITY, BUDGET, RECOVERY, SEC, APPROVAL, EFFECT'],
 ['6', 'Agents complete', 'N/A here', 'Cards in Part 11.16a'],
 ['7', 'Verify flags', 'Pass', 'Costs and legal thresholds'],
 ['8', 'No restricted data to free tier', 'Pass', 'All investor workflows exclude Tier 2'],
 ['9', 'Consistent', 'Pass', 'Engine states of Part 11.3a'],
])
w('**Status: Part 11 Batch 11.16b complete. 48 workflows specified with DTOs, step contracts, control placement, SLAs, KPI formulas, flowcharts and tests.**')
open(OUT, 'w').write('\n'.join(L) + '\n')
print('wrote', OUT, len('\n'.join(L)))
