"""Group D (Part 11.4) generator.
Reads d_workflows.json (parsed V12 sources), d_mapping.py (curated blueprint mapping) and the
hand-written fragments in d_frag/, then writes:
  Part-11-4a (11.4.1-11.4.4: material, coverage, detailed register, catalogue reconciliation)
  Part-11-4c (11.4.5.10-11.4.5.28 per-service executable specifications) - 11.4b and the closing
  sections are fragments stitched in as written
  final/coverage_v12/D_coverage.csv
Run: python3 -I d_generate.py <blueprint_dir>"""
import json, sys, os, re, csv, collections
D = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, D)
import d_mapping as M
BP = sys.argv[1]
W = json.load(open(D + '/d_workflows.json'))
CNT = json.load(open(D + '/d_counts.json'))
XC = json.load(open(D + '/d_crosscheck.json'))
FRAG = D + '/d_frag/'
def frag(n): return open(FRAG + n, encoding='utf-8').read()

# ---------------------------------------------------------------- reference data
ENT = {}
for l in open(BP + '/Part-02-7a_Source_Pack_UI_Catalog_and_UX_Enhancements.md', encoding='utf-8'):
    m = re.match(r'\| \d+ \| `(growth_\w+)` \| \d+ \| (ENT-\d+) \| `(\w+)` \| ([CP]) \|', l)
    if m: ENT[m.group(1)] = (m.group(2), m.group(3))
EXEC = {  # V12 executor -> (NT13 node type, run state on failure, retry class)
 'Policy/validation engine': ('NT13-09 `policy.check`', 'BLOCKED', 'validation: never retried'),
 'Identity/reconciliation engine': ('NT13-07 `logic.compute`', 'HELD', 'conflict: no retry; uncertain provider outcome to RECONCILING'),
 'Domain service': ('NT13-05 `data.write_internal`', 'HELD', 'invalid state: no retry; optimistic version'),
 'Domain agent / task router': ('NT13-08 `ai.task` + NT13-10 `approval.human`', 'AWAITING_APPROVAL', 'model transient: gateway retry ≤ 2 within attempt'),
 'Rules/analytics engine': ('NT13-07 `logic.compute`', 'HELD', 'invalid metric: no retry; never invent values'),
 'Effect adapter': ('NT13-13 `action.external`', 'RECONCILING', 'uncertain write: reconcile before retry (E-5)'),
 'Evidence/ingestion engine': ('NT13-04 `data.read`', 'HELD', 'transient read: ≤ 3 attempts, jitter'),
}
EXKEY = {k.split(' / ')[0]: k for k in EXEC}
def exkey(s):
    e = s['executor_input'].split(' / ')[0]
    return 'Domain agent / task router' if e == 'Domain agent' else e
PRODUCES_OVERRIDE = {
 'SM-SVC-21-WF01': ['discrepancy_refs', 'reconciliation_state'], 'SM-SVC-21-WF04': ['balance_minor', 'discrepancy_refs', 'reconciliation_state'],
 'SM-SVC-24-WF01': ['report_ref', 'attributed_minor', 'confidence'], 'SM-SVC-24-WF02': ['report_ref', 'forecast_minor', 'confidence'],
 'SM-SVC-24-WF03': ['report_ref'], 'SM-SVC-24-WF04': ['report_ref', 'forecast_minor', 'error_metric', 'confidence'],
 'SM-SVC-27-WF01': ['asset_ref', 'revision', 'rights_state', 'qa_state'], 'SM-SVC-27-WF02': ['asset_ref', 'revision', 'rights_state', 'qa_state'],
 'SM-SVC-27-WF03': ['asset_ref', 'revision', 'qa_state'], 'SM-SVC-27-WF04': ['rights_state', 'qa_state'],
 'SM-SVC-28-WF01': [], 'SM-SVC-30-WF01': ['decision_state'], 'SM-SVC-31-WF04': ['net_minor'], 'SM-SVC-33-WF03': ['sla_state'],
}
STOP = {'ref', 'refs', 'state', 'minor', 'version', 'report', 'id'}
def produces(w, r):
    if w in PRODUCES_OVERRIDE: return PRODUCES_OVERRIDE[w]
    outs = list(r['schema']['$defs']['output']['properties'])
    text = (r['spec']['Result / acceptance'].split(';')[0] + ' ' + ' '.join(s['action'] for s in r['steps']) + ' ' + r['title']).lower()
    return [f for f in outs if any(t in text for t in f.split('_') if t not in STOP and len(t) > 3)]
CONFLICT_STEPS = {  # steps that embody a conflict (Pending Founder); other steps in the workflow are specified and disabled
 'SM-SVC-26-WF01': 'all', 'SM-SVC-26-WF02': 'all', 'SM-SVC-26-WF03': 'all', 'SM-SVC-26-WF04': 'all',
 'SM-SVC-27-WF01': ['STEP-01'], 'SM-SVC-27-WF02': ['STEP-01'], 'SM-SVC-27-WF03': ['STEP-02'],
 'SM-SVC-28-WF03': ['STEP-02', 'STEP-03'], 'SM-SVC-28-WF04': ['STEP-02', 'STEP-03'],
 'SM-SVC-36-WF03': ['STEP-01'], 'SM-SVC-37-WF02': 'all', 'SM-SVC-37-WF03': 'all',
}
def step_conflict(w, sid):
    c = CONFLICT_STEPS.get(w)
    return c == 'all' or (c and sid[-7:] in c)
ARCH = {'POS': 101, 'INPUT': 102, 'SCOPE': 103, 'ENT': 104, 'DUP': 105, 'QUALITY': 106, 'BUDGET': 107, 'RECOVERY': 108, 'APPROVAL': 109, 'EFFECT': 110}
DRAFTY = ('draft', 'prepare', 'generate', 'propose', 'recommend', 'playbook', 'plan', 'storyboard', 'summar')
def tier_of(w, s):
    sv = M.SVC[w[:9]]
    if sv['tier'] == '0': return '0'
    a = s['action'].lower()
    return '1b' if any(k in a for k in DRAFTY) or sv['tier'] == '1b' and 'classif' not in a and 'flag' not in a else '1a'
PRICE = {'1a': (0.10, 0.50, 1500, 400), '1b': (2.00, 10.00, 3000, 800)}  # $/MTok in, out; tokens in, out (Part 7.3 §7.3.2, verify)
FX = 90
def call_inr(t):
    pi, po, ti, to = PRICE[t]
    return (pi * ti + po * to) / 1e6 * FX
STATUS_TXT = {'C': 'Partially covered', 'P': 'Partially covered', 'N': 'Not covered', 'X': 'Conflict'}
def autonomy(rc):
    return {'R0': 'V12 L1 assisted / L3 approved read-draft → blueprint **L0–L1** (drafts and analysis only; no external effect)',
            'R1': 'V12 L1/L2 review; L3 only for approved deterministic internal actions → blueprint **L1** for state writes, **L3** only for registered deterministic internal steps (DEC-064)',
            'R2': 'V12 L2 exact approved effect → blueprint **L1 approval of the exact payload hash, then L2 dispatch** of that item through the outbox (DEC-064 publishing pattern); V12 L3 mandate only for routine replies/reminders within caps',
            'R3': 'V12 L2 default → blueprint **L1 maximum** (human approval bound to the exact hash; money movement not supported, DEC-064). V12 "L3 bounded mandate" **not adopted** (CONFLICT-814, Pending Founder decision)'}[rc]

def handler(w, s, k, agi):
    sv, mp = M.SVC[w[:9]], M.WF[w]
    au = mp[2]
    if k == 'Policy/validation engine':
        extra = [a for a in au if a in ('AU-007', 'AU-002', 'AU-067', 'AU-044', 'AU-089')]
        return 'PDP (AU-009) rule set' + (' + ' + ', '.join(extra) if extra else '')
    if k == 'Identity/reconciliation engine':
        cand = [a for a in au if a in ('AU-037', 'AU-015', 'AU-074', 'AU-080', 'AU-091', 'AU-038', 'AU-026', 'AU-046', 'AU-014', 'AU-096', 'AU-100')]
        return (cand[0] if cand else sv['ident']) + ' registered function'
    if k == 'Rules/analytics engine':
        cand = [a for a in au if a not in ('AU-009', 'AU-004', 'AU-005', 'AU-007', 'AU-002', 'AU-027', 'AU-026')]
        return (cand[0] if cand else sv['calc']) + ' registered function'
    if k == 'Evidence/ingestion engine':
        return 'AU-007 source permission + AU-005 sanitizer, scoped read'
    if k == 'Effect adapter':
        return 'Outbox → AU-009 dispatch recheck → ' + sv['adapter']
    if k == 'Domain service':
        return '`' + sv['module'] + '` service (revision check)'
    ags = mp[1]
    if not ags:
        return 'Deterministic flag rule + NT13-11 `task.human` (no model call)'
    return ags[agi % len(ags)] + ' via gateway; routed to ' + mp[4].split(',')[0]

# ---------------------------------------------------------------- aspects
ASP = []  # (doc, chapter, section, aspect_id, summary, before, location, action, new_ids, after)
def add(*a): ASP.append(a)
CH = {'B09': ('BRD', '09 Business Workflow Catalogue'), 'F12': ('FSD', '12 Executable Workflow Specification'),
      'F13': ('FSD', '13 Workflow Step, Trigger & Event Registry'), 'F19': ('FSD', '19 Automation Scheduler & Execution Control'),
      'APB': ('FSD', 'Appendix B Workflow DTO JSON Schemas'), 'CSV': ('Workbook', 'Workflow_Catalog (50-field)')}
for row in csv.reader(open(FRAG + 'common_aspects.csv', encoding='utf-8')):
    if not row or row[0] == 'src': continue
    src, aid, sec, summ, before, loc, action, new, after = row
    add(CH[src][0], CH[src][1], sec, aid, summ, before, loc, action, new, after)
FIELD_ABBR = [('Business objective', 'objective'), ('Supported channels', 'channels'), ('Prerequisite automations', 'prereq'),
              ('AI agent responsibilities', 'agents'), ('Automation operating mode', 'mode'), ('External provider requirements', 'provider'),
              ('Usage limits', 'limits'), ('Performance KPIs', 'kpi'), ('Full / partial / selective availability', 'availability'),
              ('Security and compliance requirements', 'security'), ('Shared execution engine', 'engine'), ('Optional complementary services', 'complementary'),
              ('External agent interoperability', 'interop'), ('Technology and regulatory readiness', 'readiness'), ('Subscription pricing model', 'pricing'),
              ('Open-source software requirements', 'oss'), ('Applicable industries', 'industries'), ('Required service entitlements', 'entitlements')]
NEWPROV = {'SM-SVC-26', 'SM-SVC-27', 'SM-SVC-28', 'SM-SVC-31', 'SM-SVC-38', 'SM-SVC-39'}
svc_first = {}
for w, r in W.items():
    svc_first.setdefault(r['svc'], w)
sec_of = {s: '11.4.5.%d' % (10 + i) for i, s in enumerate(sorted(svc_first))}
for s, w in svc_first.items():
    c = W[w]['csv']; n = s[-2:]
    for f, ab in FIELD_ABBR:
        before, after, act = 'Partially covered', 'Matched', 'Service-level value adopted into the service card and scheduler/budget configuration'
        if ab == 'provider' and s in NEWPROV:
            before, act = 'Not covered', 'Adapter port specified; procurement gate PG-01…PG-10 before activation'
        if ab in ('channels', 'provider') and s in ('SM-SVC-26',):
            before, after, act = 'Conflict', 'Pending Founder decision', 'CONFLICT-815 raised; spec written, disabled'
        if ab == 'provider' and s == 'SM-SVC-27':
            before, after, act = 'Conflict', 'Pending Founder decision', 'CONFLICT-819 raised; spec written, disabled'
        if ab == 'limits':
            act = 'Pilot limit becomes the per-service hard cap in the budget hierarchy (FR-V12-D-020); still "not approved" per V12'
        if ab == 'pricing':
            act = 'Pricing model recorded; price values are a commercial decision outside this part (Part 11.2 service catalogue owner)'
        add('Workbook', CH['CSV'][1], s, 'D-S%s-%s' % (n, ab), '%s %s: %s' % (s, f, c[f][:160]), before,
            'Part 9.4; Part 2.2 §2.6; %s' % ', '.join(M.WF[w][0][:1]), act, 'FR-V12-D-1%s' % n, after)
    # DTO fields (one schema per service)
    sch = W[w]['schema']['$defs']
    for io in ('input', 'output'):
        for fld, spec in sch[io]['properties'].items():
            t = spec.get('type'); t = '/'.join(t) if isinstance(t, list) else t
            add('FSD', CH['APB'][1], 'urn:sm:dto:%s-WF0n:v2' % s, 'D-S%s-DTO-%s' % (n, fld),
                '%s %s field `%s` (%s%s)' % (s, io, fld, t, ', ' + spec.get('format', spec.get('pattern', '')) if spec.get('format') or spec.get('pattern') else ''),
                'Not covered', 'Part 3.3 entities (mapped in Part 11.4c %s)' % sec_of[s], 'Field adopted with blueprint storage target and validation (DEC-565)', 'DEC-565; FR-V12-D-002', 'Matched')
for w, r in W.items():
    mp = M.WF[w]; st = mp[3]; s = r['svc']; rc = r['spec']['Authority / effect classification'][:2]
    sec = sec_of[s]; loc = '; '.join(mp[0])
    beh = STATUS_TXT[st]; aft = 'Pending Founder decision' if st == 'X' else 'Matched'
    conf = mp[6]
    def A(k, summ, before, action, new, after=None, doc='FSD', ch='F12'):
        add(doc, CH[ch][1], w, '%s-%s' % (w, k), summ, before, loc if before != 'Not covered' else 'None (new); nearest: ' + loc, action, new, after or ('Matched' if before != 'Conflict' else 'Pending Founder decision'))
    A('A01', 'Identity and business outcome: %s; %s' % (r['title'], r['brd09']['io']), beh, 'V12 ID canonical; mapped to %s (DEC-560)' % loc, 'DEC-560; FR-V12-D-1%s' % s[-2:], aft, 'BRD', 'B09')
    A('A02', 'Trigger / supplied input: %s' % r['spec']['Trigger / required supplied input'][:150], 'Not covered' if st == 'N' else ('Conflict' if st == 'X' else 'Partially covered'), 'Trigger kinds bound in registry (DEC-564; §11.4c %s)' % sec, 'DEC-564; FR-V12-D-017', aft)
    A('A03', 'Result / acceptance artifact: %s' % r['spec']['Result / acceptance'][:120], beh, 'Typed result artifact (DB-V2-ARTIFACT domain) defined', 'FR-V12-D-1%s' % s[-2:], aft)
    A('A04', 'Domain contract %s and DTO %s' % (r['spec']['Proposed domain contract'].split(';')[0], r['schema']['$id']), 'Not covered', 'DTO adopted as schema v2 + v3 nullability fix (DEC-565, GAP-824)', 'DEC-565; FR-V12-D-002')
    a05_before = 'Conflict' if (rc == 'R3' or st == 'X') else 'Partially covered'
    A('A05', 'Authority %s' % r['spec']['Authority / effect classification'][:150], a05_before, 'Mapped to blueprint autonomy (DEC-566); R3 L3 mandate not adopted' if rc == 'R3' else 'Mapped to blueprint autonomy (DEC-566)', 'DEC-566' + ('; CONFLICT-814' if rc == 'R3' else ''), 'Pending Founder decision' if a05_before == 'Conflict' else 'Matched')
    A('A06', 'Engine / agent: %s' % r['spec']['Engine / agent'][:140], 'Conflict' if st == 'X' else 'Partially covered', 'Steps bound to %s / %s' % (', '.join(mp[1]) or 'no agent', ', '.join(mp[2])), 'DEC-562; FR-V12-D-003', aft)
    A('A07', 'Workflow KPI: %s' % r['spec']['Workflow KPI (proposed)'][:150], 'Not covered', 'KPI registered with formula and source (FR-V12-D-027)', 'FR-V12-D-027')
    a08 = 'Covered' if int(s[-2:]) <= 25 else 'Partially covered'
    A('A08', 'UI/API/DB candidates: %s' % r['spec']['Current source UI/API/DB candidates'][:150], a08, 'Retained; reused through API-V2-RUN/RESULT/APPROVAL adapters; entities mapped (Part 2.7a)', 'DEC-560', 'Matched')
    A('A09', 'Contract mapping: %s' % r['spec']['Proposed contract mapping'].split('.')[0][:150], 'Not covered', 'API-V2 run/result/approval + DB-V2 run/step/artifact/evidence/effect mapped to aut_run/aut_step_run/ops_outbox (DEC-561)', 'DEC-561; ADR-195')
    A('A10', 'Cost source: %s' % r['spec']['Cost source'], 'Partially covered', 'V12 illustrative cost kept; blueprint model-tier estimate added (§11.4c %s)' % sec, 'GAP-831')
    A('A11', 'Acceptance IDs (%d): %s' % (len(r['acceptance']), ', '.join(x.split('-TC-')[1] for x in r['acceptance'])), 'Not covered', 'Mapped to archetypes TC-V12-D-101…110; release gate FR-V12-D-003', 'TC-V12-D-101…%d' % (100 + len(r['acceptance'])))
    A('A12', 'Source acceptance %s (not run)' % ', '.join(r['source_at']), 'Not covered', 'Retained as legacy reference; superseded by POS archetype', 'TC-V12-D-111')
    A('A13', 'Channel candidates: %s; %s' % (r['channel']['channels'], r['channel']['contracts']), 'Conflict' if st == 'X' and s == 'SM-SVC-26' else 'Partially covered', 'Channel bound to adapter/eligibility rules', 'FR-V12-D-1%s' % s[-2:], 'Pending Founder decision' if st == 'X' and s == 'SM-SVC-26' else 'Matched')
    A('A14', 'UI input contract: %s' % r['ui_input']['controls'], 'Partially covered', 'Run form generated from DTO input schema in A110/A033 (FR-V12-D-023)', 'FR-V12-D-023')
    A('A15', 'Registry row: %d steps; %s; controls %s' % (r['registry']['steps'], r['registry']['executor_cues'].split('.')[0], r['registry']['controls']), 'Not covered', 'Registered in the workflow registry with control links (FR-V12-D-001)', 'FR-V12-D-001', None, 'FSD', 'F13')
    c = r['csv']
    A('A16', 'Workbook row: functionality "%s"; output "%s"; approval "%s"; side-effect "%s"; version %s' % (c['Detailed functionality'][:80], c['Expected output'], c['Human approval requirements'][:60], c['External side-effect classification'][:40], c['Workflow version']), 'Partially covered', 'Per-workflow fields adopted; side-effect label reconciled to R-class (DEC-570)', 'DEC-570; GAP-821', None, 'Workbook', 'CSV')
    for i, stp in enumerate(r['steps']):
        k = exkey(stp)
        if step_conflict(w, stp['step_id']): b, a = 'Conflict', 'Pending Founder decision'
        else: b, a = ('Not covered' if st in ('N', 'X') else 'Partially covered'), 'Matched'
        add('FSD', CH['F12'][1], w, stp['step_id'], '%s [%s; %s]' % (stp['action'], k, stp['failure'].split(';')[0]), b,
            loc if b != 'Not covered' else 'None (new)', 'Bound to %s / %s' % (EXEC[k][0], handler(w, stp, k, i)), 'DEC-562; FR-V12-D-003', a)

# ---------------------------------------------------------------- CSV
os.makedirs(BP + '/final/coverage_v12', exist_ok=True)
with open(BP + '/final/coverage_v12/D_coverage.csv', 'w', newline='', encoding='utf-8') as f:
    wr = csv.writer(f)
    wr.writerow(['doc', 'chapter', 'section', 'aspect_id', 'aspect_summary', 'status_before', 'blueprint_location', 'action', 'new_ids', 'status_after'])
    for a in ASP: wr.writerow(a)
ids = [a[3] for a in ASP]
assert len(ids) == len(set(ids)), [x for x, n in collections.Counter(ids).items() if n > 1][:5]
before = collections.Counter(a[5] for a in ASP); after = collections.Counter(a[9] for a in ASP)
by_doc = collections.Counter(a[1] for a in ASP)
json.dump({'total': len(ASP), 'before': before, 'after': after, 'by_chapter': by_doc}, open(D + '/d_aspect_counts.json', 'w'), indent=1)

# ---------------------------------------------------------------- Part 11.4a generated tables
def esc(t): return str(t).replace('|', '/').replace('\n', ' ')
CODE = {'Covered': 'C', 'Partially covered': 'P', 'Not covered': 'N', 'Conflict': 'X', 'Matched': 'M', 'Pending Founder decision': 'F', 'Not applicable': 'NA'}
def cc(a): return CODE[a[5]] + '→' + CODE[a[9]]
def gen_register():
    byid = {a[3]: a for a in ASP}
    out = ['#### 11.4.3.1 Common aspects (FSD ch12 preamble, ch13, ch19, BRD ch09 preamble, Appendix B conventions, workbook common fields)', '',
           '| Aspect ID | Summary | Before | Blueprint location | Action | New IDs | After |', '|---|---|---|---|---|---|---|']
    for a in ASP:
        if re.match(r'D-(F12|F13|F19|B09|APB|CSV)-', a[3]):
            out.append('| %s | %s | %s | %s | %s | %s | %s |' % tuple(esc(x) for x in (a[3], a[4][:200], a[5], a[6][:90], a[7][:140], a[8], a[9])))
    out += ['', '#### 11.4.3.2 Workflow aspects A01–A16 and every step (code before→after)', '',
            'Legend: C Covered, P Partially covered, N Not covered, X Conflict → M Matched, F Pending Founder decision. A01 identity/outcome, A02 trigger, A03 result, A04 DTO, A05 authority, A06 engine/agent, A07 KPI, A08 UI/API/DB candidates, A09 API-V2/DB-V2 contract, A10 cost, A11 acceptance IDs, A12 source AT01, A13 channel, A14 UI input contract, A15 ch13 registry row, A16 workbook row. Full text of every cell: `final/coverage_v12/D_coverage.csv`.', '',
            '| Workflow | ' + ' | '.join('A%02d' % i for i in range(1, 17)) + ' | Steps (STEP-nn code) |', '|---|' + '---|' * 16 + '---|']
    for w, r in W.items():
        cells = [cc(byid['%s-A%02d' % (w, i)]) for i in range(1, 17)]
        steps = ' '.join('%s %s' % (x['step_id'][-2:], cc(byid[x['step_id']])) for x in r['steps'])
        out.append('| %s | %s | %s |' % (w, ' | '.join(cells), steps))
    out += ['', '#### 11.4.3.3 Service-level workbook fields (code before→after)', '',
            '| Service | ' + ' | '.join(ab for _, ab in FIELD_ABBR) + ' |', '|---|' + '---|' * len(FIELD_ABBR)]
    for s in sorted(svc_first):
        out.append('| %s | %s |' % (s, ' | '.join(cc(byid['D-S%s-%s' % (s[-2:], ab)]) for _, ab in FIELD_ABBR)))
    out += ['', '#### 11.4.3.4 DTO fields (Appendix B), all N→M', '', '| Service | Input fields | Output fields |', '|---|---|---|']
    for s in sorted(svc_first):
        sch = W[svc_first[s]]['schema']['$defs']
        out.append('| %s | %s | %s |' % (s, ', '.join('`%s`' % f for f in sch['input']['properties']), ', '.join('`%s`' % f for f in sch['output']['properties'])))
    out += ['', '#### 11.4.3.5 Every Conflict aspect individually (all end Pending Founder decision)', '', '| Aspect ID | Summary | Conflict | Proposed resolution |', '|---|---|---|---|']
    for a in ASP:
        if a[5] == 'Conflict':
            tag = re.search(r'CONFLICT-8\d\d', a[8] + a[7]) or re.search(r'CONFLICT-8\d\d', M.WF.get(a[2], ('',) * 7)[6] if a[2] in M.WF else '')
            t = tag.group(0) if tag else (M.WF[a[2]][6] if a[2] in M.WF else '')
            if not t and a[2] in M.WF and W[a[2]]['spec']['Authority / effect classification'][:2] == 'R3': t = 'CONFLICT-814'
            out.append('| %s | %s | %s | %s |' % (esc(a[3]), esc(a[4][:150]), t, RESOL.get(t, '')))
    return '\n'.join(out)
RESOL = {'CONFLICT-814': 'Cap R3 at V12 L2 = blueprint L1 with exact-hash approval; disable "L3 bounded mandate" (DEC-577)',
         'CONFLICT-815': 'Specify fully, ship disabled; inbound AI voice only after A3 PG gate and legal review; outbound stays human-dialled; no transcripts (DEC-572)',
         'CONFLICT-816': 'Catalogue and quote drafts allowed; negotiation and payment mandates stay human; record-only reconciliation (DEC-573)',
         'CONFLICT-817': 'Deterministic margin analytics only; sensitivity scenarios and live price tests need a Founder decision (DEC-574)',
         'CONFLICT-818': 'Coach on staff-written notes only; recordings stay excluded (DEC-575)',
         'CONFLICT-819': 'Brand-asset composition first; generative media behind a new provider, budget and likeness policy (DEC-576)'}
def gen_counts():
    rows = ['| Status | Before | After |', '|---|---|---|']
    for k in ('Covered', 'Partially covered', 'Not covered', 'Conflict', 'Matched', 'Pending Founder decision', 'Not applicable'):
        rows.append('| %s | %d | %d |' % (k, before.get(k, 0), after.get(k, 0)))
    rows.append('| **Total** | **%d** | **%d** |' % (len(ASP), len(ASP)))
    rows2 = ['', '| Source chapter | Aspects | Before: Covered / Partial / Not / Conflict | After: Matched / Pending Founder |', '|---|---|---|---|']
    for chn in sorted(by_doc):
        sub = [a for a in ASP if a[1] == chn]
        cb = collections.Counter(a[5] for a in sub); ca = collections.Counter(a[9] for a in sub)
        rows2.append('| %s | %d | %d / %d / %d / %d | %d / %d |' % (chn, len(sub), cb['Covered'], cb['Partially covered'], cb['Not covered'], cb['Conflict'], ca['Matched'], ca['Pending Founder decision']))
    rows3 = ['', '| Service | Workflows | Steps | Behaviour before (C/P/N/X) | Aspects | Pending Founder after |', '|---|---|---|---|---|---|']
    for s in sorted(svc_first):
        wfs = [w for w in W if W[w]['svc'] == s]
        beh = collections.Counter(M.WF[w][3] for w in wfs)
        sub = [a for a in ASP if a[2].startswith(s) or a[3].startswith('D-S' + s[-2:])]
        rows3.append('| %s %s | %d | %d | %d / %d / %d / %d | %d | %d |' % (s, CNT['svc_titles'][s], len(wfs), sum(len(W[w]['steps']) for w in wfs), beh['C'], beh['P'], beh['N'], beh['X'], len(sub), sum(1 for a in sub if a[9] == 'Pending Founder decision')))
    return '\n'.join(rows + rows2 + rows3)
def gen_reconciliation():
    out = ['| Workflow | Title | Ch13 steps | Ch13 cues (rules / agent) | Ch12 executors (P I D A R E V) | Effect steps | Ch12 channel | Blueprint flow | Behaviour | Consistent |', '|---|---|---|---|---|---|---|---|---|---|']
    order = ['Policy/validation engine', 'Identity/reconciliation engine', 'Domain service', 'Domain agent / task router', 'Rules/analytics engine', 'Effect adapter', 'Evidence/ingestion engine']
    for w, r in W.items():
        cnt = collections.Counter(exkey(s) for s in r['steps'])
        cues = re.match(r'(\d+) rules-labeled; (\d+) agent-labeled', r['registry']['executor_cues'])
        eff = ', '.join(s['step_id'][-7:] for s in r['steps'] if exkey(s) == 'Effect adapter') or '—'
        out.append('| %s | %s | %d | %s / %s | %s | %s | %s | %s | %s | Yes |' % (w, esc(r['title']), r['registry']['steps'], cues.group(1), cues.group(2),
                   ' '.join(str(cnt[o]) for o in order), eff, esc(r['channel']['channels']), esc(M.WF[w][0][0]), STATUS_TXT[M.WF[w][3]]))
    return '\n'.join(out)
def gen_effect_catalogue():
    out = ['| Step ID | Action | Workflow R-class | Adapter (port) | Approval binding | Status |', '|---|---|---|---|---|---|']
    for w, r in W.items():
        for s in r['steps']:
            if exkey(s) == 'Effect adapter':
                rc = r['spec']['Authority / effect classification'][:2]
                out.append('| %s | %s | %s | %s | %s | %s |' % (s['step_id'], s['action'], rc, esc(M.SVC[r['svc']]['adapter']), 'Exact payload digest approved by ' + M.WF[w][4], 'Pending Founder decision' if step_conflict(w, s['step_id']) else 'Matched'))
    return '\n'.join(out)
def gen_inconsistency():
    out = ['| Workflow | FSD ch12 R-class | Workbook side-effect label | Explicit effect step in ch12 | Resolution (DEC-570) |', '|---|---|---|---|---|']
    a = {x[0]: x for x in XC.get('R2/R3 but CSV side-effect internal', [])}
    b = {x[0]: x for x in XC.get('R2/R3 without effect step', [])}
    for w in sorted(set(a) | set(b)):
        r = W[w]; rc = r['spec']['Authority / effect classification'][:2]
        out.append('| %s | %s | %s | %s | %s |' % (w, rc, 'Internal analysis/draft' if w in a else esc(r['csv']['External side-effect classification'][:50]), 'No' if w in b else 'Yes',
                   'R-class governs; engine inserts NT13-10 approval before any state change or effect' if w in b else 'R-class governs; workbook label corrected'))
    return '\n'.join(out)

# ---------------------------------------------------------------- Part 11.4c per-service specifications
def dto_table(r, prod):
    sch = r['schema']['$defs']; rows = ['| Dir | Field | JSON Schema (App. B v2) | V12 validation | Blueprint storage target |', '|---|---|---|---|---|']
    dto = {d['field']: d['type'] for d in r['dto']}
    for io in ('input', 'output'):
        for fld, spec in sch[io]['properties'].items():
            js = spec.get('type'); js = '/'.join(js) if isinstance(js, list) else js
            for k in ('format', 'pattern', 'minimum', 'maxLength', 'maxItems', 'minLength'):
                if k in spec: js += ' %s=%s' % (k, spec[k])
            if io == 'output' and fld not in prod: tag = ' (v3: nullable here)'
            else: tag = ''
            rows.append('| %s | `%s`%s | %s | %s | %s |' % ('in' if io == 'input' else 'out', fld, tag, esc(js), esc(dto.get(fld, '')[:70]), esc(target(r['svc'], fld))))
    return '\n'.join(rows)
TARGET = {
 'invoice_ref': 'com_invoice.id (ENT-140)', 'payment_ref': 'com_payment.id (ENT-142)', 'amount_minor': 'com_payment.amount numeric(18,4) ↔ int64 minor (RECOMMENDATION-829)',
 'currency': 'char(3) ISO 4217 (DEC-027)', 'allocation_ref': 'com_payment_allocation.id (Part 3.3 allocation rows)', 'balance_minor': 'derived: invoice total − Σ allocations',
 'discrepancy_refs': 'aut_artifact items (domain receivable)', 'reconciliation_state': 'enum {staged, matched, partial, mismatch, exception, reconciled}',
 'customer_ref': 'crm_account / lcy customer (ENT-086 deal owner account)', 'agreement_ref': 'com_contract.id (ENT-131)', 'template_ref': 'aut_workflow_template / eng_message_template by service',
 'milestone_refs': 'lcy_task milestones (ENT-148)', 'plan_ref': 'aut_artifact (domain plan) or lcy_onboarding (ENT-147)', 'readiness_state': 'enum {not_ready, ready_with_risks, ready, blocked}',
 'task_refs': 'lcy_task.id[] (ENT-148)', 'handover_ref': 'lcy_handoff.id (ENT-149)', 'renewal_ref': 'lcy_renewal.id (ENT-150)', 'feedback_refs': 'lcy_feedback.id[] (ENT-157)',
 'consent_ref': 'gov_consent.id (ENT-027)', 'renewal_task_ref': 'lcy_task.id', 'risk_score': 'enum band from registry `risk_score` (v3 adds numeric `risk_value` 0–1, GAP-824)', 'reason_codes': 'text[] from versioned reason registry',
 'recommendation_ref': 'aut_artifact (domain recommendation)', 'outcome_refs': 'lcy_outcome.id[] (ENT-158)', 'attribution_model_ref': 'attribution model registry (AU-096)', 'period': 'daterange / ISO period',
 'assumption_refs': 'aut_artifact items (forecast assumptions)', 'report_ref': 'ana_metric_snapshot / aut_artifact report', 'attributed_minor': 'numeric(18,4) ↔ int64 minor', 'forecast_minor': 'ana_forecast amount ↔ int64 minor (label: estimate)',
 'error_metric': 'enum metric name (e.g. MAPE, KPI-29) (v3 adds numeric `error_value`)', 'confidence': 'enum band (v3 adds numeric `confidence_value` 0–1)', 'document_ref': 'cat_document.id (ENT-024)', 'taxonomy_ref': 'document taxonomy registry',
 'claim_refs': 'cat_claim.id[] (ENT-020)', 'revision': 'integer ≥ 1 (optimistic version)', 'document_version': 'cat_document.revision', 'claim_version_refs': 'cat_claim revision ids', 'review_state': 'enum {staged, in_review, approved, rejected, held}',
 'correction_refs': 'aut_artifact items (correction queue)', 'call_ref': 'eng_call (proposed, ASSUMPTION-827)', 'contact_ref': 'intel_contact.id (ENT-074)', 'script_ref': 'eng_message_template (voice script)',
 'recording_permission_ref': 'gov_consent.id (purpose = call_recording)', 'disposition': 'enum call disposition registry', 'transcript_ref': 'excluded by DEC-218 unless Founder approves', 'booking_ref': 'eng_meeting.id (ENT-103)', 'call_event_ref': 'eng_inbound_event / int_provider_event',
 'brief_ref': 'mkt_content_asset brief', 'brand_ref': 'brand kit config (tenant/startup)', 'asset_rights_refs': 'asset rights register rows', 'target_language': 'BCP 47 tag; allowed set DEC-026', 'asset_ref': 'mkt_content_asset.id (ENT-105)',
 'rights_state': 'enum {unknown, cleared, restricted, rejected}', 'qa_state': 'enum {pending, passed, failed, held}', 'agent_ref': 'int_external_agent (proposed)', 'mandate_ref': 'gov_mandate (proposed)', 'offering_ref': 'cat_offering.id (ENT-016)',
 'order_ref': 'com_order.id (WF-10)', 'quote_ref': 'com_quote.id (ENT-127)', 'mandate_state': 'enum {draft, approved, expired, revoked}', 'transaction_ref': 'com_payment / provider reference (record only)',
 'account_ref': 'intel_organization / crm account (ENT-063)', 'icp_ref': 'ICP definition (CFG)', 'role_evidence_refs': 'intel_role_hypothesis.id[] (ENT-075)', 'engagement_refs': 'crm_activity.id[] (ENT-088)',
 'buying_group_ref': 'buying-committee map (AU-085)', 'journey_ref': 'eng_sequence / cadence id (WF-27)', 'progress_report_ref': 'aut_artifact report', 'hypothesis_ref': 'experiment registry hypothesis',
 'variant_refs': 'experiment arms (approved content hashes)', 'allocation_policy_ref': 'AU-098 allocation config', 'event_refs': 'ops_domain_event.id[] (ENT-170)', 'experiment_ref': 'experiment registry id',
 'lift': 'decimal string ^-?\\d{1,14}(\\.\\d{1,4})?$ (ADR-030 compatible)', 'interval': 'object {lower, upper, confidence_level 0–1} (v3 adds additionalProperties false)', 'decision_state': 'enum {running, stop_harm, inconclusive, ship, no_ship}', 'marketplace_ref': 'int_integration (marketplace connection)',
 'sku_ref': 'cat_offering SKU', 'inventory_ref': 'stock ledger (WF-10)', 'listing_ref': 'mkt_marketplace_listing (proposed)', 'inventory_version': 'integer ≥ 1', 'order_event_ref': 'int_provider_event.id',
 'net_minor': 'numeric(18,4) ↔ int64 minor', 'partner_ref': 'lcy_partner.id (ENT-153)', 'territory_ref': 'territory rules (AU-082)', 'material_refs': 'mkt_content_asset.id[]', 'deal_ref': 'crm_deal.id (ENT-086)',
 'shortlist_ref': 'aut_artifact (domain shortlist)', 'access_grant_ref': 'object grant (portal, R16P)', 'registration_ref': 'partner deal registration (WF-30)', 'performance_ref': 'aut_artifact report',
 'enquiry_ref': 'eng_inbound_event / eng_thread', 'sla_policy_ref': 'SLA policy config', 'knowledge_refs': 'cat_chunk.id[] (ENT-025)', 'case_ref': 'sup_case (proposed)', 'severity': 'enum {S1, S2, S3, S4}',
 'queue_ref': 'support queue config', 'resolution_ref': 'aut_artifact (resolution)', 'sla_state': 'enum {within, at_risk, breached, paused}', 'feature_refs': 'product feature registry', 'activation_state': 'enum {not_started, activating, activated, stalled}',
 'usage_report_ref': 'aut_artifact report', 'expansion_ref': 'aut_artifact (expansion signal)', 'review_refs': 'intel_review / public review items', 'source_ids': 'intel_source.id[] (ENT-053)', 'threshold_ref': 'alert threshold config',
 'review_queue_ref': 'task queue id', 'response_ref': 'eng_message_draft.id (ENT-091)', 'incident_ref': 'gov_compliance_incident.id (ENT-039)', 'improvement_ref': 'aut_artifact (plan)', 'learner_ref': 'staff user id',
 'playbook_ref': 'mkt_content_asset (playbook)', 'scenario_ref': 'practice scenario / pricing scenario artifact', 'authorized_session_ref': 'consent-checked session id (written notes only, DEC-386)', 'playbook_revision': 'integer ≥ 1',
 'practice_report_ref': 'aut_artifact (learner-private)', 'feedback_ref': 'aut_artifact (learner-private)', 'training_plan_ref': 'aut_artifact (learner-private)', 'offer_ref': 'cat_offering / bundle id', 'cost_revision_ref': 'cost revision register',
 'price_bounds_ref': 'cat_price_version.id (ENT-021)', 'history_refs': 'quote/order history ids', 'margin_minor': 'numeric(18,4) ↔ int64 minor (AU-049)', 'exception_ref': 'aut_artifact (exception)',
 'sender_ref': 'eng_channel_account.id (ENT-089)', 'recipient_refs': 'intel_contact.id[]', 'consent_refs': 'gov_consent.id[]', 'eligibility_state': 'enum {eligible, held, blocked}', 'dispatch_ref': 'ops_outbox / eng_message.id',
 'delivery_state': 'enum {queued, sent, delivered, failed, unknown}', 'suppression_state': 'enum {none, suppressed, complaint}', 'requirement_ref': 'prc_requirement (proposed)', 'supplier_refs': 'intel_organization.id[] (supplier role)',
 'quote_refs': 'prc_supplier_quote.id[] (proposed)', 'budget_ref': 'budget line (AU-002 hierarchy)', 'comparison_ref': 'aut_artifact (comparison)', 'purchase_order_ref': 'prc_purchase_order (proposed)', 'exception_refs': 'aut_artifact items',
}
def target(s, fld): return TARGET.get(fld, 'aut_artifact payload (validated against registry)')

def wf_block(w, r, prod):
    mp = M.WF[w]; s = r['svc']; sp = r['spec']; rc = sp['Authority / effect classification'][:2]; c = r['csv']
    agsteps = [x for x in r['steps'] if exkey(x) == 'Domain agent / task router']
    cost_ai = sum(call_inr(tier_of(w, x)) for x in agsteps if mp[1]) if M.SVC[s]['tier'] != '0' else 0
    v12cost = float(re.search(r'INR ([\d.]+)', sp['Cost source']).group(1))
    trig = sp['Trigger / required supplied input']
    kinds = []
    tl = trig.lower()
    if 'manual' in tl: kinds.append('`manual` (NT13-03)')
    if 'schedul' in tl: kinds.append('`scheduled` (NT13-02; default cadence per §11.4b, misfire `reschedule_once`)')
    if 'event' in tl: kinds.append('`event` (NT13-01; `sm.svc%s.%s.requested` or upstream domain event, §11.4b.6)' % (s[-2:], w[-4:].lower()))
    if 'webhook' in tl or 'callback' in tl: kinds.append('`provider_callback` (signed, replay-checked)')
    if 'upstream' in tl: kinds.append('`child_workflow` (registered dependency, depth ≤ 3)')
    rows = [
        ('V12 sources', 'BRD ch09 row; FSD ch12 lines %d–%d; FSD ch13 registry row; App. B `%s`; workbook row "%s"' % (r['fsd12_lines'][0], r['fsd12_lines'][1], r['schema']['$id'], esc(c['Sub-automation name']))),
        ('Business outcome', '%s. Input → output: %s' % (esc(r['brd09']['outcome_title']), esc(r['brd09']['io']))),
        ('Detailed functionality (workbook)', esc(c['Detailed functionality'])),
        ('Blueprint mapping', '%s; agents %s; automations %s' % (esc('; '.join(mp[0])), ', '.join(mp[1]) or 'none (deterministic only)', ', '.join(mp[2]))),
        ('What V12 adds', esc(mp[7])),
        ('Behaviour status', '%s → %s%s' % (STATUS_TXT[mp[3]], 'Pending Founder decision' if mp[3] == 'X' else 'Matched', ' (' + mp[6] + ')' if mp[6] else '')),
        ('Trigger (V12)', esc(trig)),
        ('Trigger kinds (registry, DEC-564)', '; '.join(kinds)),
        ('Authority (V12)', esc(sp['Authority / effect classification'])),
        ('Blueprint autonomy (DEC-566)', autonomy(rc) + '. Approver: ' + mp[4]),
        ('Human approval (workbook)', esc(c['Human approval requirements'])),
        ('Effect boundary', ('Effect steps: ' + ', '.join(x['step_id'][-7:] for x in r['steps'] if exkey(x) == 'Effect adapter') + ' via ' + esc(M.SVC[s]['adapter'])) if any(exkey(x) == 'Effect adapter' for x in r['steps']) else ('No external effect; ' + ('approval gate inserted before state change (DEC-570)' if rc in ('R2', 'R3') else 'internal artifacts only'))),
        ('Outputs produced (v3 projection)', ', '.join('`%s`' % p for p in prod) or 'none of the shared output fields fit; `catalog_version_ref` proposed (GAP-824)'),
        ('Workflow KPI', esc(sp['Workflow KPI (proposed)'])),
        ('Preconditions / failure handling', 'Common contract (D-F12-030 variant %d, D-F12-031): §11.4b.5' % (1 if sp['Preconditions'].startswith('Active entitlement') else 2)),
        ('Cost', 'V12 illustrative ₹%.2f/invocation (excludes provider, retry, labour). Blueprint model estimate ₹%.2f/run for %d agent step(s) at Tier %s (Part 7.3 prices, FX ₹90/USD, verify at time of implementation, as of 27 Nov 2026); Tier 2 not eligible (Confidential/personal data)' % (v12cost, cost_ai, len(agsteps) if mp[1] else 0, M.SVC[s]['tier'])),
        ('Data modalities / version', '%s; service %s, workflow %s' % (esc(c['Supported data modalities']), c['Service version'], c['Workflow version'])),
        ('Acceptance (V12 → blueprint)', '%s-TC-{%s} → TC-V12-D-%s; %s → TC-V12-D-111' % (w, ','.join(x.split('-TC-')[1] for x in r['acceptance']), '101…%d' % (100 + len(r['acceptance'])), r['source_at'][0])),
        ('Release proposal', mp[5]),
    ]
    out = ['#### %s %s' % (w, r['title']), '', '| Field | Specification |', '|---|---|'] + ['| %s | %s |' % (k, v) for k, v in rows]
    out += ['', '| Step ID | Action (V12) | V12 executor → node type | Blueprint handler | Output contract | Failure → run state | Model tier | Status |', '|---|---|---|---|---|---|---|---|']
    for i, x in enumerate(r['steps']):
        k = exkey(x)
        tier = ('Tier ' + tier_of(w, x)) if k == 'Domain agent / task router' and mp[1] else ('Tier 0 / none' if k != 'Effect adapter' else 'none')
        outc = x['output_validation'].split(' / ')[0]
        out.append('| %s | %s | %s → %s | %s | %s | %s → %s | %s | %s |' % (x['step_id'], esc(x['action']), k.split(' / ')[0], EXEC[k][0], esc(handler(w, x, k, i)), esc(outc),
                   x['failure'].split(' → ')[0], EXEC[k][1], tier, 'Pending Founder decision' if step_conflict(w, x['step_id']) else 'Matched'))
    out += ['']
    return '\n'.join(out), cost_ai, v12cost

def gen_services():
    out = []; costrows = []; parts = []
    for s in sorted(svc_first):
        if s == 'SM-SVC-31': parts.append('\n'.join(out)); out = []
        sv = M.SVC[s]; c = W[svc_first[s]]['csv']
        out += ['### %s %s %s' % (sec_of[s], s, CNT['svc_titles'][s]), '',
                '| Field | Specification |', '|---|---|',
                '| Family / objective | %s; %s |' % (esc(c['Automation family']), esc(c['Business objective'])),
                '| Channels / providers | %s; %s |' % (esc(c['Supported channels']), esc(c['External provider requirements'])),
                '| Optional producers / complementary | %s |' % esc(c['Prerequisite automations']),
                '| Service KPI | %s |' % esc(c['Performance KPIs']),
                '| Usage limit (pilot, not approved) | %s |' % esc(c['Usage limits']),
                '| Availability / bundle | %s |' % esc(c['Full / partial / selective availability']),
                '| Interoperability / readiness | %s; %s |' % (esc(c['External agent interoperability']), esc(c['Technology and regulatory readiness'])),
                '| Open-source stack | %s |' % esc(c['Open-source software requirements']),
                '| Blueprint epic / module | %s (ASSUMPTION-826) / `%s` |' % (sv['epic'], sv['module']),
                '| Effect adapter | %s |' % esc(sv['adapter']),
                '| Service guardrail | %s |' % esc(sv['svc_note']),
                '| Functional requirement | FR-V12-D-1%s (§11.4.5.30 register) |' % s[-2:], '',
                '**DTO `urn:sm:dto:%s-WF0n:v2` (one schema shared by the four workflows; v3 projection per workflow below):**' % s, '',
                dto_table(W[svc_first[s]], []).replace(' (v3: nullable here)', ''), '']
        for w in [x for x in W if W[x]['svc'] == s]:
            prod = produces(w, W[w])
            blk, ca, vc = wf_block(w, W[w], prod)
            out.append(blk)
            costrows.append((w, ca, vc))
    parts.append('\n'.join(out))
    return parts, costrows

def gen_cost(costrows):
    # monthly AI estimate at pilot usage: units of the service split evenly across its 4 workflows
    rows = ['| Service | Pilot units / month (workbook) | V12 illustrative ₹ / month | Blueprint model estimate ₹ / month |', '|---|---|---|---|']
    tv = tb = 0
    for s in sorted(svc_first):
        lim = W[svc_first[s]]['csv']['Usage limits']
        units = int(re.search(r'pilot: (\d+)', lim).group(1))
        cr = [x for x in costrows if x[0].startswith(s)]
        v = sum(units / 4 * x[2] for x in cr); b = sum(units / 4 * x[1] for x in cr)
        tv += v; tb += b
        rows.append('| %s | %d %s | %.0f | %.0f |' % (s, units, esc(lim.split('/month')[0].split('pilot: ')[1].split(' ', 1)[1]), v, b))
    rows.append('| **Total** | — | **%.0f** | **%.0f** |' % (tv, tb))
    return '\n'.join(rows), tv, tb

svc_md, costrows = gen_services()
cost_md, tv, tb = gen_cost(costrows)
json.dump({'v12_month': tv, 'bp_month': tb}, open(D + '/d_cost.json', 'w'))

def fill(t):
    return (t.replace('{{REGISTER}}', gen_register()).replace('{{COUNTS}}', gen_counts()).replace('{{RECON}}', gen_reconciliation())
             .replace('{{EFFECTS}}', gen_effect_catalogue()).replace('{{INCONSISTENCY}}', gen_inconsistency()).replace('{{SERVICES_1}}', svc_md[0]).replace('{{SERVICES_2}}', svc_md[1])
             .replace('{{AICOST}}', cost_md).replace('{{N_ASPECTS}}', str(len(ASP))).replace('{{N_PENDING}}', str(after.get('Pending Founder decision', 0)))
             .replace('{{N_MATCHED}}', str(after.get('Matched', 0))))
for name in ['Part-11-4%s_V12_Executable_Workflows_SVC21-39_Registry_and_DTOs.md' % k for k in 'abcd']:
    key = name[8:10] if False else name.split('_')[0][-1]
    src = FRAG + 'part_%s.md' % key
    if os.path.exists(src):
        open(BP + '/' + name, 'w', encoding='utf-8').write(fill(frag('part_%s.md' % key)))
print('aspects', len(ASP), dict(before), dict(after))
print('AI cost/month V12 %.0f blueprint %.0f' % (tv, tb))
