"""R2/B generator: Part 11.2 (a/b/c) service specifications + final/coverage_v12/B_coverage.csv.
Usage: python3 -I r2b_build.py <workbook.json> <brd08.json> <fsd11.json> <fsd08.txt> <blueprint_dir>
Inputs come from r2b_parse_services.py and r2b_parse_brd08.py. Mapping data from r2b_data.py (same folder)."""
import sys, json, csv, os, re, collections, importlib.util
here = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location('r2b_data', os.path.join(here, 'r2b_data.py'))
D = importlib.util.module_from_spec(spec); spec.loader.exec_module(D)
WB = json.load(open(sys.argv[1])); BRD = json.load(open(sys.argv[2])); FSD = json.load(open(sys.argv[3]))
FSD08 = open(sys.argv[4], encoding='utf-8').read(); OUT = sys.argv[5]

SC = {r['Automation ID']: r for r in WB['Service_Catalog']['rows']}
ENT = {r['Service ID']: r for r in WB['Entitlement_Rules']['rows']}
IDX = {r['Service ID']: r for r in WB['Service_Index']['rows']}
MIG = {r['Service ID']: r for r in WB['Migration']['rows']}
WFC = WB['Workflow_Catalog']['rows']
COST = collections.defaultdict(list)
for r in WB['Cost_Model']['rows']: COST[r['Service ID']].append(r)
TMAP = collections.defaultdict(list)
for r in WB['Technical_Map']['rows']: TMAP[r['Service ID']].append(r)
AT = WB['Acceptance_Tests']['rows']
SIDS = sorted(SC)

def esc(s): return str(s).replace('|', '/').replace('\n', '<br/>').strip()

# ---------------- ID allocation ----------------
FR = []   # (id, svc or 'COMMON', text, pos, neg)
n = 0
for t in D.COMMON_FR:
    n += 1; FR.append(('FR-V12-B-%03d' % n, 'COMMON', *t))
SVC_FR = collections.defaultdict(list)
for sid in SIDS:
    for t in D.S[sid]['nfr']:
        n += 1; fid = 'FR-V12-B-%03d' % n; FR.append((fid, sid, *t)); SVC_FR[sid].append(fid)
FRD = {f[0]: f for f in FR}

def short(t, n=80):
    t = t.split(';')[0].strip()
    if len(t) <= n: return t.rstrip('.')
    cut = t[:n].rsplit(' ', 1)[0]
    return cut.rstrip(',(') + '…'
def ep_num(ep): return ep.split(',')[0].strip().replace('EP-', '')
# stories
STORY = []  # (id, epic, title, frs, svc)
cnt = collections.Counter()
def add_story(ep, title, frs, sid):
    e = ep_num(ep); cnt[e] += 1
    STORY.append(('US-%s-YB%02d' % (e, cnt[e]), 'EP-' + e, title, frs, sid))
common_groups = [
 ('Service, workflow and bundle registry', [1, 2, 3, 28]), ('Foundation inclusion and selection modes', [4, 5, 11]),
 ('Per-action SKU entitlement in the PDP', [6, 7, 8, 26]), ('Meters, caps and commercial model', [9, 10, 29]),
 ('Migration and legacy entitlements', [12]), ('Event envelope, idempotency and recovery', [13, 14, 15, 16]),
 ('Agent identity, interoperability and model portability', [17, 18, 19]), ('Side-effect class and autonomy cap', [20]),
 ('First value, enhancement metrics and outcome acceptance', [21, 22, 30]), ('Shared engines', [23]),
 ('Public service catalogue projection', [24]), ('Readiness gate and catalogue administration', [25, 27])]
for title, idx in common_groups:
    add_story('EP-29', title, ['FR-V12-B-%03d' % i for i in idx], 'All')
NEW_EP = {e[0] for e in D.NEW_EPICS}
for sid in SIDS:
    m = D.S[sid]; frs = SVC_FR[sid]
    if not frs: continue
    pep = m['ep'].split(',')[0].strip()
    if pep in NEW_EP:
        for f in frs: add_story(pep, short(FRD[f][2]), [f], sid)
    else:
        add_story(pep, '%s %s: V12 SKU deltas' % (sid, SC[sid]['Automation service name']), frs, sid)
SVC_STORY = collections.defaultdict(list)
for s in STORY: SVC_STORY[s[4]].append(s[0])

# tests
TC = []  # (id, title, fr, pre, steps, expected, type, level, prio)
t = 0
def add_tc(title, fr, pre, steps, exp, typ, lvl, prio):
    global t; t += 1; TC.append(('TC-V12-B-%03d' % t, title, fr, pre, steps, exp, typ, lvl, prio))
for f in FR:
    sid = f[1]; pre = 'Tenant T, startup S; active entitlement for %s; synthetic fixtures; provider stub' % ('the SKU under test' if sid == 'COMMON' else sid)
    add_tc('Positive: ' + f[2][:70], f[0], pre, 'Execute the behaviour in %s' % f[0], f[3], 'Positive', 'SIT', 'P1')
    add_tc('Negative/boundary: ' + f[2][:62], f[0], pre, 'Attempt the prohibited or boundary case', f[4], 'Negative', 'SIT', 'P0' if any(k in f[4].lower() for k in ['never', 'refused', 'blocked', 'rejected']) else 'P1')
ENT_TC = {}
for a in AT:
    if '-ENT-' in a['Test ID']:
        add_tc('Entitlement isolation %s (%s)' % (a['Service ID'], a['Test ID']), 'FR-V12-B-026', esc(a['Preconditions']), esc(a['Execution steps']), esc(a['Expected output / behavior']) + '; ' + esc(a['Negative and boundary checks']), 'Security', 'SIT/UAT', 'P0')
        ENT_TC[a['Service ID']] = TC[-1][0]
for sw in D.SWR:
    add_tc('Accessibility WCAG 2.2 AA: %s' % sw[1], 'FR-V12-B-027' if sw[2] == 'All' else (SVC_FR[sw[2]][0] if SVC_FR.get(sw[2]) else 'FR-V12-B-027'), 'Screen built for %s' % sw[0], 'Keyboard-only run; screen reader; contrast; status messages', 'No WCAG 2.2 AA failure; focus order logical; errors announced', 'Accessibility', 'UAT', 'P1')
add_tc('Cross-tenant isolation across all 39 SKUs', 'FR-V12-B-006', 'Tenants T1 and T2 with different SKUs', 'T1 user calls every SKU endpoint with T2 object IDs', '0 records disclosed; 403/404 only; audit events written', 'Security', 'SIT', 'P0')
add_tc('Fundraising capability absent from catalogue', 'FR-V12-B-024', 'Catalogue loaded', 'Search public and admin catalogue for investor/fundraising capability', 'No SKU, workflow or route offers investor discovery or fundraising (DEC-002)', 'Negative', 'SIT', 'P0')
add_tc('Free-tier routing refused for personal data in new SKUs', 'FR-V12-B-019', 'Tier 2 opt-in on', 'Run SM-SVC-26, 33, 38 with personal data', 'Gateway never selects Tier 2; decision log shows data class', 'Security', 'SIT', 'P0')
FR_TC = collections.defaultdict(list)
for x in TC: FR_TC[x[2]].append(x[0])

# ---------------- helpers ----------------
def wf_list(sid):
    rows = [dict(w, WID=w['Sub-automation name'].split(' ')[0]) for w in WFC if w['Sub-automation name'].startswith(sid + '-WF')]
    return rows
def scr_titles(sid):
    out = []
    for r in TMAP[sid]:
        out.append('%s %s' % (r['Admin screen ID'], r['Existing admin screen title']) if not r['Admin screen ID'].startswith('TBD') else 'Design gap: ' + r['Existing admin screen title'])
    return out
def cost(sid):
    v = [float(r['Internal INR / invocation']) for r in COST[sid]]
    return sum(v), sum(v) / len(v)
def cap(sid): return int(ENT[sid]['Proposed pilot cap'])

TITLE = '# AI Growth Engine: Employee Sales & Marketing Automation\n## Application Blueprint: PART 11 (Batch 11.2%s), V12 Master Automation Service Catalogue: 39 Services%s\n\n'
HDR = ('| Item | Detail |\n|---|---|\n| Document | Part 11.2%s, V12 Master Automation Service Catalogue: 39 Services%s |\n| Version | 1.0 · 28 Nov 2026 |\n'
       '| Baseline | Parts 0–9.10 (DEC-001…422); BRD V12 ch. 08; FSD V12 ch. 08 and ch. 11; source workbook "Master Automation Service Catalog 2031: 39 Services 156 Workflows" (12 sheets) |\n'
       '| Roles applied | Chief Revenue Officer, Head of Marketing Automation, Principal Solutions Architect, Principal Business Systems Analyst, AI Product Lead; with Product Owner, QA Lead, Security/AI Governance and FinOps review |\n'
       '| Group / ID ranges | R2, letter B: tags 778–795, DEC-520…539, ADR-185…189, FR-V12-B-###, US-<EP>-YB<nn>, TC-V12-B-###, BRL-V12-B-##, new epics EP-22…EP-29 |\n\n')

def service_spec(sid):
    r = SC[sid]; e = ENT[sid]; ix = IDX[sid]; mg = MIG[sid]; b = BRD[sid]; f = FSD[sid]; m = D.S[sid]
    num = int(sid[-2:]); tot, avg = cost(sid)
    wfs = wf_list(sid)
    wf_txt = '<br/>'.join('**%s** %s (%s; acceptance %s-AT01)' % (w['WID'], w['Sub-automation name'].split('—', 1)[-1].strip(), 'new in V12' if (w['WID'].endswith('WF04') or num >= 26) else 'retained', w['WID']) for w in wfs)
    em = b['Enhancement metrics'].split(' | ')
    em_txt = '<br/>'.join('WF0%d: %s' % (i + 1, x) for i, x in enumerate(em))
    fv = 'First reviewed and accepted %s; activation and acceptance timestamps recorded; owner validates evidence and agreed quality (BRD 08 V5 register)' % r['Expected output']
    st_after = 'Matched' if m['st'] != 'Conflict' else 'Matched, except the items marked Pending Founder decision'
    new_frs = SVC_FR[sid]
    rows = [
     ('Identity and source', '%s · family %s · bundle %s · service version %s · %s. Sources: BRD V12 ch. 08 §%s; FSD V12 ch. 11 §%s (%s); FSD ch. 08 engine register; workbook Service Catalog, Service Index, Entitlement Rules, Migration, Technical Map, Cost Model, Acceptance Tests rows for %s' % (sid, r['Automation family'], e['Partial bundle'], r['Service version'], mg['Decision'], sid, sid, f['Business source'], sid)),
     ('Blueprint home', 'Epic %s · modules %s · status before: **%s** → after: **%s**' % (m['ep'], m['mod'], m['st'], st_after)),
     ('Purpose and value', '%s. Functionality: %s Industries: %s. Capability: %s. Independent purchase: %s Outcome: %s' % (r['Business objective'].rstrip('.'), r['Detailed functionality'], r['Applicable industries'], r['Applicable business capabilities'], r['Independent purchase justification'], r['Measurable customer outcome'])),
     ('First-value milestone', fv),
     ('Entitlements', 'Required: %s. Availability: %s Order separately: %s. Foundation: %s. Optional input producers: %s; complementary: %s. Required supplied input: %s. Provider/permission: %s. Missing prerequisite: %s. Revocation: %s. Approval status: %s. Entitlement acceptance: %s-ENT-AT01 → %s' % (r['Required service entitlements'], r['Full / partial / selective availability'], e['Order separately'], e['Included foundation'], e['Optional input producers (service IDs)'], r['Optional complementary services'], e['Required supplied input'], e['Required provider / permission'], e['Missing prerequisite behavior'], e['Revocation behavior'], e['Approval status'], sid, ENT_TC.get(sid, ''))),
     ('Commercial and metering', 'Meter: %s · illustrative pilot cap %s/month (not approved) · price status %s. Pricing model: %s Usage limits: %s Illustrative internal AI cost (workbook scenario, ASSUMPTION-789): ₹%.2f for one run of each of the four workflows, mean ₹%.2f per invocation; at the pilot cap ≈ ₹%.0f per month (cap × mean). External fees excluded and quoted separately' % (e['Meter unit'], e['Proposed pilot cap'], ix['Price status'], r['Subscription pricing model'], r['Usage limits'], tot, avg, cap(sid) * avg)),
     ('Inputs', r['Required input data']),
     ('Outputs', r['Expected output']),
     ('Workflows (IDs only; detail in Part 11.3/11.4, Groups C/D)', wf_txt + '<br/>Migration: %s (%s → %s workflows)' % (mg['Workflow transition'], mg['Previous workflows'], mg['Target workflows'])),
     ('Workflow steps (summary)', esc(r['Workflow steps'])),
     ('Triggers and events', '%s Event envelope and idempotency: FR-V12-B-013, FR-V12-B-014' % r['Trigger types']),
     ('Functional requirements', 'Baseline: %s%s. Catalogue framework: FR-V12-B-001…030. New in this part: %s' % (m['fr'], ('; advanced: ' + m['adv']) if m['adv'] else '', ', '.join(new_frs) if new_frs else 'none')),
     ('Business rules', 'Approval gate (V12): %s. Baseline rules: %s. New rules: %s; framework BRL-V12-B-19…22' % (r['Human approval requirements'], m['brl'], ', '.join(x[0] for x in D.BRL if sid in x[2] or (x[2].startswith('SM-SVC-26…39') and num >= 26)) or 'none')),
     ('Agents and automations', 'V12 AI responsibilities: %s. Operating mode: %s Reused agents: %s. Reused automations: %s.%s%s Autonomy cap: %s. Side-effect class: %s' % (r['AI agent responsibilities'], r['Automation operating mode'], m['ag'], m['au'], (' New agent capability (handoff to Group F): ' + m['acr'] + '.') if m['acr'] else '', (' New automation capability (handoff to Group F): ' + m['aur'] + '.') if m['aur'] else '', m['auto'], r['External side-effect classification'])),
     ('Model tier and data class', m['dc'] + '. Model portability: ' + r['Model portability']),
     ('Integrations', 'Providers: %s. V12 provider requirement: %s. Open-source: %s. Shared engines: %s. Agent identity: %s External agents: %s. API operations (%d, all present in Part 3.2/3.5): %s' % (m['integ'], r['External provider requirements'], r['Open-source software requirements'], r['Shared execution engine'], r['Agent identity and authority'] + '.', r['External agent interoperability'], len([a for a in re.split(r';\s*', r['Related API operations']) if re.match(r'(Candidate reuse only: )?(GET|POST|PATCH|PUT|DELETE) ', a)]), r['Related API operations'])),
     ('KPIs', 'Service KPIs: %s (%s-KPI-1/2). Enhancement metrics:<br/>%s<br/>Blueprint KPIs: %s; time-to-first-value (FR-V12-B-021)' % (r['Performance KPIs'], sid, em_txt, m['kpi'])),
     ('Data', 'Entities: %s. Domain artifact (FSD 11): %s. Modalities: %s. Provenance: %s' % (r['Related database entities'], f['Proposed domain artifact'], r['Supported data modalities'], r['Data provenance requirements'])),
     ('Screens', 'Workbook mapping: %s.%s%s' % ('; '.join(scr_titles(sid)), (' Additional blueprint screens: ' + m['scrp'] + '.') if m['scrp'] else '', (' Workspace requirement (handoff to Group G, IDs A170–A259): ' + m['swr'] + '.') if m['swr'] else '')),
     ('Security and compliance', r['Security and compliance requirements']),
     ('Risks and controls', '<br/>'.join('%s → %s' % x for x in m['rsk']) + '<br/>Escalation: ' + r['Escalation and recovery policy'] + '<br/>Readiness: ' + r['Technology and regulatory readiness'] + '; ' + b['Readiness']),
     ('Migration and versioning', r['Service migration and deprecation policy'] + '. Entitlement transition: ' + mg['Entitlement transition']),
     ('Simulation and benchmark', r['Simulation and benchmark reference']),
     ('Release placement', m['wave'] + '. WF04 delta: ' + m['wf4']),
     ('Stories and tests', 'Stories: %s. Tests: %s' % (', '.join(SVC_STORY.get(sid, [])) or 'framework stories of EP-29 only', ', '.join(sum((FR_TC[x] for x in new_frs), [])) + ((', ' if new_frs else '') + ENT_TC.get(sid, '')))),
    ]
    out = ['### 11.2.5.%d %s %s\n' % (num + 10, sid, r['Automation service name']), '| Field | Specification |', '|---|---|']
    out += ['| %s | %s |' % (k, esc(v)) for k, v in rows]
    if new_frs:
        out += ['', '**New functional requirements for %s**' % sid, '', '| FR | Requirement | Acceptance (positive) | Negative / boundary | Tests |', '|---|---|---|---|---|']
        out += ['| %s | %s | %s | %s | %s |' % (fid, esc(FRD[fid][2]), esc(FRD[fid][3]), esc(FRD[fid][4]), ', '.join(FR_TC[fid])) for fid in new_frs]
    return '\n'.join(out) + '\n'

# ---------------- coverage CSV ----------------
COV = []
def cov(doc, ch, sec, aid, summ, sb, loc, act, nids, sa):
    COV.append([doc, ch, sec, aid, summ[:300], sb, loc, act, nids, sa])
BOILER = {'Estimated execution cost', 'Implementation and verification status', 'Workflow version', 'Agent identity and authority', 'Model portability', 'Event and trigger schema', 'Idempotency and conflict policy', 'Escalation and recovery policy', 'Data provenance requirements', 'Unit economics and margin target', 'Service migration and deprecation policy'}
COMMERCIAL_P = {'Subscription pricing model', 'Usage limits', 'Full / partial / selective availability', 'Required service entitlements'}
COMMERCIAL_N = {'Service version', 'Independent purchase justification', 'Simulation and benchmark reference', 'Measurable customer outcome', 'Optional complementary services', 'Shared execution engine', 'Acceptance test references'}
FUNC_COVERED = {'Related UI screen IDs', 'Related API operations', 'Related database entities', 'Open-source software requirements'}
PENDING = {('SM-SVC-28', 'Automation operating mode'), ('SM-SVC-28', 'Human approval requirements'), ('SM-SVC-28', 'External side-effect classification'), ('SM-SVC-28', 'Workflow steps'), ('SM-SVC-28', 'Sub-automation name'), ('SM-SVC-28', 'Technology and regulatory readiness'),
           ('SM-SVC-26', 'Workflow steps'), ('SM-SVC-26', 'Sub-automation name'), ('SM-SVC-26', 'Automation operating mode'), ('SM-SVC-26', 'Human approval requirements'),
           ('SM-SVC-19', 'Workflow steps'), ('SM-SVC-19', 'Human approval requirements')}
CONF_IDS = {'SM-SVC-28': 'CONFLICT-778', 'SM-SVC-26': 'CONFLICT-779', 'SM-SVC-19': 'CONFLICT-781'}
def status_for(sid, field):
    m = D.S[sid]; num = int(sid[-2:])
    if (sid, field) in PENDING: return 'Conflict'
    if field in COMMERCIAL_N: return 'Not covered'
    if field in COMMERCIAL_P: return 'Partially covered'
    if field in FUNC_COVERED: return 'Covered' if num <= 25 or field != 'Related database entities' else 'Partially covered'
    if m['st'] == 'Not covered': return 'Not covered'
    if field in ('Sub-automation name', 'Workflow steps', 'Detailed functionality', 'Performance KPIs'): return 'Partially covered'
    if num <= 25: return 'Covered'
    return 'Partially covered'
def loc_for(sid):
    m = D.S[sid]; return '%s; %s; %s' % (m['ep'], m['mod'], m['fr'][:120])
def after(sb, sid, field):
    return 'Pending Founder decision' if (sid, field) in PENDING else 'Matched'
spec_loc = lambda sid: 'Part 11.2%s §11.2.5.%d' % ('b' if int(sid[-2:]) <= 20 else 'c', int(sid[-2:]) + 10)

# BRD 08
FOUND = [('SM-01-0%d' % i) for i in range(1, 6)] + [('SM-1%d-0%d' % (j, i)) for j in range(1, 5) for i in range(1, 6)]
FMAP = {'SM-01-01': 'AG-030; EP-20 (US-2001)', 'SM-01-02': 'FR-A100 templates', 'SM-01-03': 'AG-030; FR-A100', 'SM-01-04': 'FR-A099; EP-20', 'SM-01-05': 'FR-A099/A101 activation', 'SM-11-01': 'EP-20 trial (DEC-047)', 'SM-11-02': 'FR-A101', 'SM-11-03': 'AU-042; API-529', 'SM-11-04': 'AU-042; BRL-SVC-03; ENT-181', 'SM-11-05': 'WF-14; FR-A103',
        'SM-12-01': 'AU-001; M08', 'SM-12-02': 'AU-068', 'SM-12-03': 'AU-069; AG-055', 'SM-12-04': 'AU-003', 'SM-12-05': 'AG-002; AU-006; M54', 'SM-13-01': 'M58; AU-010', 'SM-13-02': 'BRL-AUT-07', 'SM-13-03': 'AU-010; gateway Tier 3', 'SM-13-04': 'AU-026', 'SM-13-05': 'AG-028; M58',
        'SM-14-01': 'M30, M52; KPI-01…31', 'SM-14-02': 'AU-088; AG-054', 'SM-14-03': 'AG-043; Part 8.3 OKPI', 'SM-14-04': 'BRL-AUT-04; FR-A102', 'SM-14-05': 'OKPI-01…35 (Part 8.3)'}
XW = {r['Original capability ID']: r for r in WB['Capability_Crosswalk']['rows']}
for fid in FOUND:
    cov('BRD V12', '08', 'V8 Included foundation capabilities', 'B-BRD08-FND-' + fid, '%s %s (included, never priced)' % (fid, XW[fid]['Original capability name']), 'Partially covered', FMAP[fid], 'Mapped foundation ID to blueprint capability; non-removable rule FR-V12-B-004', 'FR-V12-B-004; DEC-522', 'Matched')
for sid in SIDS:
    cov('BRD V12', '08', 'V5 first-value milestone register', 'B-BRD08-FV-' + sid, 'First-value evidence for ' + sid, 'Not covered', '—', 'First-value milestone specified per service', 'FR-V12-B-021; ' + spec_loc(sid), 'Matched')
BND = [('Research & Lead Intelligence', 6, 24), ('Outreach & Conversations', 7, 28), ('Digital Marketing & Acquisition', 9, 36), ('Sales Conversion & Operations', 6, 24), ('Lifecycle & Business Intelligence', 8, 32), ('Commerce & Procurement', 3, 12)]
for i, (bn, c, w) in enumerate(BND):
    cov('BRD V12', '08', 'Commercial product catalogue and packaging', 'B-BRD08-BND-%d' % (i + 1), '%s: %d services, %d flows' % (bn, c, w), 'Not covered', 'DEC-047 plan archetypes only', 'Bundle registry', 'FR-V12-B-003; DEC-520', 'Matched')
for i, txt in enumerate(['Select 39 SKUs via full-suite, partial-bundle or selective requests', 'All four flows covered subject to entitlement, readiness, provider and approval', 'Do not sell 156 individual workflow SKUs', 'No service represented as approved for live sale; public design offers quote requests', 'Customer-owned companies never listed on the SaaS storefront', 'BR-V3-01–04: 39 SKUs and 156 flows canonical']):
    cov('BRD V12', '08', 'Commercial product catalogue and packaging', 'B-BRD08-PKG-%d' % (i + 1), txt, 'Partially covered' if i in (3, 4) else 'Not covered', 'DEC-047; BRL-PUB-05' if i in (3, 4) else '—', 'Packaging rule specified', 'FR-V12-B-005; FR-V12-B-010; FR-V12-B-024; DEC-520; DEC-521', 'Matched')
BRD_FIELD_MAP = {'Business objective': 'Business objective', 'Applicable customer / sector': 'Applicable industries', 'Channels / capabilities': 'Supported channels', 'Customer inputs and rights': 'Required input data', 'Deliverable / outcome': 'Expected output', 'Independent mode': 'Independent purchase justification', 'Provider and prerequisite': 'External provider requirements', 'Bundle / meter': 'Usage limits', 'Commercial terms': 'Subscription pricing model', 'Business acceptance': 'Performance KPIs', 'Risk / limits': 'Human approval requirements', 'Complementary services': 'Optional complementary services', 'Traceability': 'Acceptance test references'}
for sid in SIDS:
    for k, wf in BRD_FIELD_MAP.items():
        sb = status_for(sid, wf)
        cov('BRD V12', '08', sid, 'B-BRD08-%s-%s' % (sid[-2:], re.sub(r'[^A-Za-z]', '', k)[:12]), '%s: %s' % (k, BRD[sid][k]), sb, loc_for(sid) if sb != 'Not covered' else '—', 'Specified in service spec', spec_loc(sid) + ('; ' + CONF_IDS[sid] if (sid, wf) in PENDING else ''), after(sb, sid, wf))
    em = BRD[sid]['Enhancement metrics'].split(' | ')
    for i, x in enumerate(em):
        cov('BRD V12', '08', sid, 'B-BRD08-%s-EM-WF0%d' % (sid[-2:], i + 1), 'Enhancement metrics %s-WF0%d: %s' % (sid, i + 1, x), 'Not covered', '—', 'Metric emitters per workflow', 'FR-V12-B-022; ' + spec_loc(sid), 'Matched')
cov('BRD V12', '08', 'All services', 'B-BRD08-READINESS', 'Readiness: Planned / proposed; release individually only after scope, permission, pricing, benchmark, SLA and acceptance sign-off (39× boilerplate)', 'Partially covered', 'Part 8.1 release gates; FR-A090', 'Per-SKU readiness gate', 'FR-V12-B-025', 'Matched')
# FSD 08
for fid in FOUND:
    cov('FSD V12', '08', 'V8 Foundation register', 'B-FSD08-FND-' + fid, '%s %s (family Included foundations)' % (fid, XW[fid]['Original capability name']), 'Partially covered', FMAP[fid], 'Same as BRD register; ID mapping', 'FR-V12-B-004', 'Matched')
EMAP = {'ENG-01': 'M10–M12, M59', 'ENG-02': 'M18, M19', 'ENG-03': 'M03, M08 RAG', 'ENG-04': 'new (EP-22, EP-28) + M08', 'ENG-05': 'M25–M28, M31, M35, M41', 'ENG-06': 'M29, M40', 'ENG-07': 'M01 + new mandate register (EP-24)', 'ENG-08': 'M34, M43, M46; WeasyPrint', 'ENG-09': 'M44, M52, M60', 'ENG-10': 'M47; AU-037', 'ENG-11': 'M17; AU-056, AU-059', 'ENG-12': 'AU-065; A125', 'ENG-13': 'M55; Celery', 'ENG-14': 'M24 PDP, M06 audit, M57', 'ENG-15': 'Part 8.3 optimization; AU-068'}
for r in WB['Shared_Engines']['rows']:
    cov('FSD V12', '08', 'Engine register', 'B-FSD08-' + r['Engine ID'], '%s %s: %s' % (r['Engine ID'], r['Logical engine'], r['Primary mapped services']), 'Partially covered', EMAP[r['Engine ID']], 'Engine mapped to modules', 'FR-V12-B-023; DEC-526', 'Matched')
for i, (ent, lc) in enumerate([('Service SKU', 'draft → reviewed → pilot/released → restricted/deprecated; no public draft'), ('Workflow version', 'draft → validated → approved → released; immutable active-run snapshot'), ('Bundle', 'versioned list of eligible SKU IDs; foundation automatically included'), ('Capability', '100 legacy IDs mapped; 25 foundation not separately priced')]):
    cov('FSD V12', '08', 'Lifecycle register', 'B-FSD08-LC-%d' % (i + 1), '%s: %s' % (ent, lc), 'Partially covered' if i == 1 else 'Not covered', 'BRL-AUT-03 (pinned revision)' if i == 1 else '—', 'Lifecycle state machine', ['FR-V12-B-001', 'FR-V12-B-002', 'FR-V12-B-003', 'FR-V12-B-011'][i], 'Matched')
cov('FSD V12', '08', 'Public projection', 'B-FSD08-PROJ', 'Public projection: description, deliverables, readiness, prerequisites, approved pricing/quote CTA, locale; never internal records', 'Partially covered', 'BRL-PUB-05; DEC-047', 'Public projection rule', 'FR-V12-B-024; DEC-536', 'Matched')
# FSD 11
FSD_FIELD_MAP = {'Business source': None, 'Functional objective': 'Business objective', 'Input / output': 'Required input data', 'Channels, operating mode': 'Automation operating mode', 'Agent responsibility / engines': 'AI agent responsibilities', 'Required provider / approval': 'Human approval requirements', 'Service dependency / permission': 'Required service entitlements', 'Source UI / API / entities': 'Related UI screen IDs', 'Proposed domain artifact': None, 'Meter / cost': 'Usage limits', 'Quality and provenance': 'Performance KPIs', 'Migration / readiness': 'Service migration and deprecation policy'}
for sid in SIDS:
    for k, wf in FSD_FIELD_MAP.items():
        if wf is None:
            sb = 'Not covered'; loc = '—'
        elif wf in BOILER: sb = 'Partially covered'; loc = 'Part 3.1 versioning; BRL-AUT-03'
        else: sb = status_for(sid, wf); loc = loc_for(sid) if sb != 'Not covered' else '—'
        cov('FSD V12', '11', sid, 'B-FSD11-%s-%s' % (sid[-2:], re.sub(r'[^A-Za-z]', '', k)[:12]), '%s: %s' % (k, FSD[sid][k]), sb, loc, 'Specified in service spec' + ('; domain artifact name adopted, field schema owned by FSD ch. 26 group (GAP-785)' if k == 'Proposed domain artifact' else ''), spec_loc(sid) + ('; ' + CONF_IDS[sid] if wf and (sid, wf) in PENDING else ''), after(sb, sid, wf or ''))
# Workbook
for sid in SIDS:
    r = SC[sid]
    for k, v in r.items():
        if k in BOILER or k == 'Automation ID': continue
        if k in ('Trigger types', 'Automation operating mode') and (sid, k) not in PENDING: continue
        sb = status_for(sid, k)
        cov('Workbook', 'Service_Catalog', sid, 'B-WB-SC-%s-%s' % (sid[-2:], re.sub(r'[^A-Za-z]', '', k)[:14]), '%s: %s' % (k, v), sb, loc_for(sid) if sb != 'Not covered' else '—', 'Specified in service spec', spec_loc(sid) + ('; ' + CONF_IDS[sid] if (sid, k) in PENDING else ''), after(sb, sid, k))
for k in sorted(BOILER) + ['Trigger types', 'Automation operating mode']:
    vals = collections.Counter(SC[s][k] for s in SIDS)
    for j, (v, c) in enumerate(vals.most_common()):
        cov('Workbook', 'Service_Catalog', 'All services (boilerplate ×%d)' % c, 'B-WB-SC-BOIL-%s-%d' % (re.sub(r'[^A-Za-z]', '', k)[:14], j + 1), '%s: %s' % (k, v), 'Partially covered', 'BRL-AUT-03/07/08; AU-026; M06; gateway (Part 7.3)', 'Framework requirement', {'Estimated execution cost': 'FR-V12-B-029', 'Implementation and verification status': 'FR-V12-B-025', 'Workflow version': 'FR-V12-B-002', 'Agent identity and authority': 'FR-V12-B-017', 'Model portability': 'FR-V12-B-019', 'Event and trigger schema': 'FR-V12-B-013', 'Idempotency and conflict policy': 'FR-V12-B-014', 'Escalation and recovery policy': 'FR-V12-B-015', 'Data provenance requirements': 'FR-V12-B-016', 'Unit economics and margin target': 'FR-V12-B-029; GAP-788', 'Service migration and deprecation policy': 'FR-V12-B-012; FR-V12-B-028', 'Trigger types': 'FR-V12-B-013', 'Automation operating mode': 'FR-V12-B-020'}[k], 'Matched')
for sid in SIDS:
    x = IDX[sid]; cov('Workbook', 'Service_Index', sid, 'B-WB-IDX-' + sid[-2:], ' · '.join(x.values()), 'Not covered', '—', 'Service index row reconciled (§11.2.4.1)', 'FR-V12-B-001; DEC-520', 'Matched')
    e = ENT[sid]; cov('Workbook', 'Entitlement_Rules', sid, 'B-WB-ENT-' + sid[-2:], 'Entitlement rule: bundle %s; meter %s; cap %s; gate %s' % (e['Partial bundle'], e['Meter unit'], e['Proposed pilot cap'], e['Approval gate']), 'Partially covered', 'DEC-047; AU-042; BRL-SVC-03', 'Per-SKU entitlement rule', 'FR-V12-B-006…009; ' + spec_loc(sid), 'Pending Founder decision' if sid == 'SM-SVC-28' else 'Matched')
    mg = MIG[sid]; cov('Workbook', 'Migration', sid, 'B-WB-MIG-' + sid[-2:], '%s: %s; %s; %s' % (mg['Decision'], mg['2031 service'], mg['Workflow transition'], mg['Entitlement transition']), 'Not covered', '—', 'Migration rule', 'FR-V12-B-012; DEC-524' + ('; BRL-V12-B-05' if sid in ('SM-SVC-20', 'SM-SVC-39') else ''), 'Matched')
for i, r in enumerate(WB['Start_Here']['rows']):
    cov('Workbook', 'Start_Here', 'Scope metric', 'B-WB-START-%02d' % (i + 1), ' · '.join(v for v in r.values() if v), 'Partially covered' if i in (6, 9) else 'Not covered', 'Part 2.5 (34/113 screens); BRL-PUB-05' if i in (6, 9) else '—', 'Scope metric reconciled (§11.2.4.1)', 'DEC-520; DEC-535' if i == 0 else 'DEC-520', 'Pending Founder decision' if i == 0 else 'Matched')
for i, r in enumerate(WB['Sources_Decisions']['rows']):
    cov('Workbook', 'Sources_Decisions', 'Source / decision', 'B-WB-SRC-%02d' % (i + 1), ' · '.join(v for v in r.values() if v), 'Partially covered', 'Part 0B; Part 9.10 source registers', 'Source decision recorded (§11.2.4.6)', 'DEC-520…538', 'Matched')
for r in WB['Capability_Crosswalk']['rows']:
    cid = r['Original capability ID']
    found = r['Primary service ID'] == 'ALL'
    cov('Workbook', 'Capability_Crosswalk', cid, 'B-WB-XW-' + cid, '%s %s → %s (%s)' % (cid, r['Original capability name'], r['Primary service ID'], r['Commercial classification']), 'Partially covered', FMAP.get(cid, D.S.get(r['Primary service ID'], {}).get('mod', '')) if True else '', 'Crosswalk mapping (§11.2.4.3)', 'FR-V12-B-011' + ('; FR-V12-B-004' if found else ''), 'Matched')
for i, r in enumerate(WB['Technical_Map']['rows']):
    sid = r['Service ID']; tbd = r['Admin screen ID'].startswith('TBD')
    cov('Workbook', 'Technical_Map', sid, 'B-WB-TM-%03d' % (i + 1), '%s %s: %s' % (r['Admin screen ID'], r['Existing admin screen title'], r['Reuse decision']), 'Not covered' if tbd else ('Conflict' if r['Reuse decision'].startswith('Legacy publication') else 'Covered'), '—' if tbd else 'Part 2.5 screen ' + r['Admin screen ID'], ('Workspace requirement ' + D.S[sid]['swr'] + ' handed to Group G (GAP-786)') if tbd and D.S[sid]['swr'] else ('Mapped to existing X1/X2 screens ' + D.S[sid]['scrp'] if tbd else ('Legacy route isolated to separate client property (DEC-536)' if r['Reuse decision'].startswith('Legacy') else 'Reuse confirmed; service-specific tests added')), (D.S[sid]['swr'].split(' ')[0] if tbd and D.S[sid]['swr'] else (D.S[sid]['scrp'] if tbd else ('DEC-536' if r['Reuse decision'].startswith('Legacy') else ENT_TC.get(sid, '')))), 'Matched')
for r in WB['Cost_Model']['rows']:
    cov('Workbook', 'Cost_Model', r['Service ID'], 'B-WB-COST-' + r['Workflow ID'][3:], '%s: %s in / %s out tokens; ₹%.2f per invocation' % (r['Workflow ID'], r['Input tokens (scenario)'], r['Output tokens (scenario)'], float(r['Internal INR / invocation'])), 'Not covered', '—', 'Rolled up into service illustrative cost (ASSUMPTION-789)', 'FR-V12-B-029; ' + spec_loc(r['Service ID']), 'Matched')
for k, v in [('Input tokens per 1,000', '0.2'), ('Output tokens per 1,000', '0.8'), ('Compute / orchestration per invocation', '0.15'), ('Tokens per pricing unit', '1000')]:
    cov('Workbook', 'Cost_Model', 'Rate assumptions', 'B-WB-COST-RATE-' + re.sub(r'[^A-Za-z]', '', k)[:12], '%s = ₹%s (illustrative, not vendor quote)' % (k, v), 'Conflict', 'Part 7.3 gateway pricing (verify)', 'Kept as illustrative scenario; gateway actuals govern', 'ASSUMPTION-789; FR-V12-B-029', 'Matched')
for a in AT:
    ent = '-ENT-' in a['Test ID']
    cov('Workbook', 'Acceptance_Tests', a['Service ID'], 'B-WB-AT-' + a['Test ID'], '%s: %s; KPI %s' % (a['Test ID'], a['Scenario'], a['Target KPI']), 'Not covered', '—', 'Mapped to TC (entitlement) ' if ent else 'Referenced in service spec; workflow test detail Groups C/D/J', ENT_TC[a['Service ID']] if ent else spec_loc(a['Service ID']), 'Matched')
cov('Workbook', 'Workflow_Catalog', '156 workflows × 50 fields', 'B-WB-WFC', '156 workflow rows (50 fields each); IDs used in service specs', 'Not applicable', 'Owned by Groups C (SVC-01…20) and D (SVC-21…39)', 'Workflow IDs and names referenced only', 'Part 11.3 / 11.4', 'Not applicable (workflow detail owned by Groups C/D)')

# ---------------- write CSV ----------------
os.makedirs(os.path.join(OUT, 'final', 'coverage_v12'), exist_ok=True)
with open(os.path.join(OUT, 'final', 'coverage_v12', 'B_coverage.csv'), 'w', newline='', encoding='utf-8') as fh:
    w = csv.writer(fh); w.writerow(['doc', 'chapter', 'section', 'aspect_id', 'aspect_summary', 'status_before', 'blueprint_location', 'action', 'new_ids', 'status_after']); w.writerows(COV)
ids = [c[3] for c in COV]; dup = [k for k, v in collections.Counter(ids).items() if v > 1]
assert not dup, dup[:5]
CB = collections.Counter(c[5] for c in COV); CA = collections.Counter(c[9] for c in COV)
CBD = collections.defaultdict(collections.Counter)
for c in COV: CBD[c[0] + ' ' + c[1]][c[5]] += 1
json.dump({'before': CB, 'after': CA, 'by': CBD, 'n': len(COV), 'fr': len(FR), 'us': len(STORY), 'tc': len(TC)}, open(os.path.join(here, 'r2b_counts.json'), 'w'), indent=1)
pickle_out = {'FR': FR, 'STORY': STORY, 'TC': TC, 'ENT_TC': ENT_TC, 'SVC_FR': dict(SVC_FR), 'SVC_STORY': dict(SVC_STORY), 'CB': CB, 'CA': CA, 'CBD': {k: dict(v) for k, v in CBD.items()}, 'NCOV': len(COV)}
json.dump(pickle_out, open(os.path.join(here, 'r2b_ids.json'), 'w'), indent=0, ensure_ascii=False)
# write specs fragments for the part writer
with open(os.path.join(here, 'r2b_specs_b.md'), 'w') as fh:
    fh.write('\n'.join(service_spec(s) for s in SIDS if int(s[-2:]) <= 20))
with open(os.path.join(here, 'r2b_specs_c.md'), 'w') as fh:
    fh.write('\n'.join(service_spec(s) for s in SIDS if int(s[-2:]) > 20))
print('coverage rows', len(COV), dict(CB), dict(CA)); print('FR', len(FR), 'stories', len(STORY), 'tests', len(TC))
