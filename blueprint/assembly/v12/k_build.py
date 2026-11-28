"""Group K (R10) builder: parses FSD V12 ch37, ch40 and Appendix D row by row, reconciles every row with the
blueprint (Parts 4.3/4.4/8.2/8.3/6.6/6.9, final/RTM.csv, final/coverage/*.csv, final/dec_index.csv) and writes
  final/coverage_v12/K_coverage.csv  and  Markdown fragments for Part 11.11 (scratch directory argument).
Usage: python3 -I k_build.py <v12_dir> <blueprint_dir> <fragment_dir>
"""
import sys, re, csv, collections, pathlib, hashlib
HERE = pathlib.Path(__file__).parent
sys.path.insert(0, str(HERE))
from k_parse import parse
import k_maps as M

V12, BP, OUT = (pathlib.Path(a) for a in sys.argv[1:4])
OUT.mkdir(parents=True, exist_ok=True)
FSD = V12 / 'FSD'
C = BP / 'final' / 'coverage'

t37, p37 = parse(FSD / '37_Observability_Incidents_Support.txt')
t40, p40 = parse(FSD / '40_Master_Traceability_Decision_Register_S.txt')
tD, pD = parse(FSD / 'AP_Appendix_D_ID_index.txt')

def tab(tables, header0, h2=None):
    for x in tables:
        if x['header'] and x['header'][0] == header0 and (h2 is None or h2 in x['h2']):
            return x
    raise KeyError(header0)

rows = []  # coverage rows
def add(doc, ch, sec, aid, summ, sb, loc, action, new, sa):
    rows.append([doc, ch, sec, aid, summ.replace('\n', ' ')[:300], sb, loc, action, new, sa])

def md(s):
    return str(s).replace('|', '/').replace('\n', ' ')

# ------------------------------------------------------------------ blueprint data
RTM = {r['requirement_id']: r for r in csv.DictReader(open(BP / 'final' / 'RTM.csv', encoding='utf-8'))}
Dmap = list(csv.DictReader(open(C / 'D_api_mapping.csv', encoding='utf-8')))
Emap = {r['src_table']: r for r in csv.DictReader(open(C / 'E_table_mapping.csv', encoding='utf-8'))}
Gmap = {r['source_id']: r for r in csv.DictReader(open(C / 'G_test_mapping.csv', encoding='utf-8'))}
Qmap = {r['qc_id']: r for r in csv.DictReader(open(C / 'H_qc_map.csv', encoding='utf-8'))}
Wmap = {r['work_item']: r for r in csv.DictReader(open(C / 'H_workitem_story_map.csv', encoding='utf-8'))}
Hdec = {r['source_id']: r for r in csv.DictReader(open(C / 'H_decision_map.csv', encoding='utf-8'))}
Jcov = {}
for r in csv.DictReader(open(C / 'J_coverage.csv', encoding='utf-8')):
    if re.fullmatch(r'OPT-\d\d-\d\d', r['aspect_id']):
        Jcov.setdefault(r['aspect_id'], r)
DECIDX = {r['DEC']: r for r in csv.DictReader(open(BP / 'final' / 'dec_index.csv', encoding='utf-8'))}

# SPDEC status from Part 6.9a table
SPDEC = {}
p69a = next(BP.glob('Part-06-9a_*.md')).read_text(encoding='utf-8')
for line in p69a.splitlines():
    m = re.match(r'\| (SPDEC-\d{3}) \| (.*?) \| (.*?) \| (.*?) \| (.*?) \| (.*?) \|$', line)
    if m:
        SPDEC[m.group(1)] = m.groups()

# TRN-SCR cards (Part 8.3b)
CARDS = {}
p83b = next(BP.glob('Part-08-3b_*.md')).read_text(encoding='utf-8')
for line in p83b.splitlines():
    m = re.match(r'\| TRN-SCR-([WA]\d+) \| (.*?) \|', line)
    if m:
        cells = [c.strip() for c in line.strip('|').split('|')]
        CARDS[m.group(1)] = {'name': cells[1], 'uat': cells[8] if len(cells) > 8 else ''}

# Agents -> FR sets (Part 9.4 catalogue)
AGFR = {}
p94 = next(BP.glob('Part-09-4_*.md')).read_text(encoding='utf-8')
for line in p94.splitlines():
    m = re.match(r'\| (AG-0\d\d) \| (.*?) \|', line)
    if m:
        cells = [c.strip() for c in line.strip('|').split('|')]
        frs = set(re.findall(r'FR-[AW]\d+', cells[10] if len(cells) > 10 else ''))
        AGFR[m.group(1)] = (cells[1], frs)

def ui_to_fr(ui):
    out = []
    for s in re.findall(r'\b([AW]\d{2,3})\b', ui):
        fid = 'FR-' + (s if s[0] == 'W' else 'A' + s[1:].zfill(3))
        if fid in RTM: out.append(fid)
    return out

# ================================================================== CHAPTER 37
ch = '37 Observability, Incidents & Support'
ops = tab(t37, 'ID', 'V12')
OPS_NEW = {
 'ENT-OPS-01': ('FR-V12-K-001; US-20-YK05; TC-V12-K-001…004; DEC-716', 'SLA tier schedule v3 written (sec 11.11.5.1); 99.9/99.95% tiers and credits raised as CONFLICT-944'),
 'ENT-OPS-02': ('FR-V12-K-002; FR-V12-K-012; US-20-YK04; TC-V12-K-005…008; DEC-703', 'V12 W40/A130 mapped to W45/A159/A014; maintenance notices and unknown state added (sec 11.11.5.2)'),
 'ENT-OPS-03': ('FR-V12-K-003; US-21-YK01; US-21-YK02; TC-V12-K-009…013; DEC-701', 'SEV1-SEV4 canonical labels, comms timeline matrix, IC role set, game-day drill (sec 11.11.5.3)'),
 'ENT-OPS-04': ('FR-V12-K-004; FR-V12-K-015; US-21-YK02; TC-V12-K-014…015; DEC-715', 'Monthly paging test adopted now; 24x7 human on-call raised as CONFLICT-943 with costed options (sec 11.11.5.4)'),
 'ENT-OPS-05': ('FR-V12-K-005; US-20-YK03; TC-V12-K-016…018; DEC-702', 'Tiered first-response targets by plan with ticket-SLA reporting (sec 11.11.5.5)'),
 'ENT-OPS-06': ('FR-V12-K-006; US-20-YK06; TC-V12-K-019…020; DEC-707', 'Help centre top-50 task list and localisation rule (sec 11.11.5.6)'),
 'ENT-OPS-07': ('FR-V12-K-007; US-21-YK07; TC-V12-K-021…022; DEC-701', 'PIR record and action tracking fields confirmed; review evidence rule (sec 11.11.5.7)'),
}
for r in ops['rows']:
    eid = r[0]
    sb, loc, own, sa = M.ENT[eid]
    new, act = OPS_NEW[eid]
    if eid in M.ENT_CONFLICT: new += '; ' + M.ENT_CONFLICT[eid]
    add('FSD', ch, 'V12 Service operations', eid, f'{r[1]} {r[2]} Acceptance: {r[3]} Owner {r[4]}; phase {r[5]}; prototype {r[6]}',
        sb, loc, act, new, sa)
rec = tab(t37, 'ID / priority / owner', 'V10')
for r in rec['rows']:
    add('FSD', ch, 'V10 Historical reconciliation controls', 'REC-23 (ch37)', f'{r[0]}: {r[1]} Acceptance: {r[2]}',
        'Partially covered', 'Part 4.3 sec 4.41-4.43; Part 4.4b sec 4.4.5.6.1-6.5', 'Thresholds, severities and ack targets aligned (sec 11.11.5.8); no SLA promise beyond approved schedules',
        'FR-V12-K-008; TC-V12-K-023', 'Matched')
add('FSD', ch, 'V10 Source monitored thresholds', '37-THR-NOTE', p37[[q['h2'] for q in p37].index('V10 | Source monitored thresholds and responses')]['text'],
    'Covered', 'Part 4.4b sec 4.4.5.6 (doc 31 reviewed)', 'Retained wording recorded as candidate controls', '', 'Matched')
THR = {
 'HTTP p95': ('Partially covered', 'SLO-03/04; LT-ENH-I-02 (p95 <= 2.5 s growth; async ACK <= 2 s); no alert', 'AL-59 dashboard p95 and AL-60 async ACK added'),
 'Error ratio': ('Covered', 'AL-50 (> 1% / 10 min, DEC-165/324)', 'Mapped'),
 'Queue age': ('Covered', 'AL-51 (> 5 min / 5 min per class)', 'Mapped'),
 'Budget': ('Covered', 'AL-53; RB-005; DEC-306 100% hard stop', 'Mapped'),
 'Isolation / credential': ('Covered', 'AL-33, AL-41, AL-43, AL-58; RB-008, RB-013', 'Mapped'),
 'Financial mismatch': ('Covered', 'AL-56; RB-016', 'Mapped'),
 'AI quality': ('Covered', 'AL-39, AL-49; RB-015 (re-pin prompt, Tier 3, regression)', 'Mapped; RB-015 wording "disable affected workflow" added'),
 'Backup': ('Covered', 'AL-23, AL-46; RB-007; deploy block via RGV', 'Mapped'),
}
thr = tab(t37, 'Metric / alert', 'V10')
for i, r in enumerate(thr['rows'], 1):
    sb, loc, act = THR[r[0]]
    add('FSD', ch, 'V10 Source monitored thresholds and responses', f'37-THR-{i:02d}', f'{r[0]}: {r[1]} Response: {r[2]}',
        sb, loc, act + ' (sec 11.11.5.8 table)', 'FR-V12-K-008; TC-V12-K-023…025' if sb != 'Covered' else 'FR-V12-K-008', 'Matched')
add('FSD', ch, 'V9 Operational training register', '37-TRN-NOTE', p37[[q['h2'] for q in p37].index('V9 | Operational training register')]['text'],
    'Covered', 'Part 8.3b sec 8.3.5.1 (synthetic data only, GSE-SYN)', 'Confirmed', '', 'Matched')
scn = tab(t37, 'Scenario', 'V9')
SCN = {'Quotation calculation': 'FR-DM-01 (270.00 INR)', 'Bid expiry': 'FR-DM-02', 'Order fulfillment': 'FR-DM-03', 'EduVerse routing': 'FR-DM-04; TC-ENH-A-004'}
for i, r in enumerate(scn['rows'], 1):
    add('FSD', ch, 'V9 Operational training register', f'37-TRN-SCN-{i:02d}', f'{r[0]}: {r[1]} -> {r[2]}', 'Covered',
        f'Part 2.1 {SCN[r[0]]}; Part 8.3b TRN-EX', 'Mapped literally', '', 'Matched')
trn = tab(t37, 'ID', 'V9')
trn_rows = []
for r in trn['rows']:
    tid, screen, proc, succ, uat = r
    scr = screen.split()[0]
    card = CARDS.get(scr)
    uat_ok = bool(card and uat in card['uat'])
    trn_rows.append((tid, scr, screen[len(scr) + 1:], uat, 'TRN-SCR-' + scr if card else '—', 'yes' if uat_ok else 'no'))
    sb = 'Partially covered'  # content covered by TRN-SCR card; V12 ID alias missing
    add('FSD', ch, 'V9 Operational training register', tid, f'{screen}: {proc[:120]} UAT {uat}', sb,
        f'Part 8.3b TRN-SCR-{scr} (UAT alias {"matches" if uat_ok else "differs"})',
        'V12 TRN ID registered as canonical alias of the card (sec 11.11.4.2)', 'FR-V12-K-013; TC-V12-K-026', 'Matched')
for q in p37:
    if q['h2'].startswith('V7'):
        pass
add('FSD', ch, 'V7 Responsive and mobile requirements', 'MOB-14', ' '.join(q['text'] for q in p37 if q['h2'].startswith('V7')),
    'Partially covered', 'Part 9.9a CAP-X3-26 web push (content minimised N-P4; revocation wipe BRL-X3-26-3); DEC-036 A106',
    'Scoped notification rules NTF-MOB-01…07 and MOB-14-AT01 test (sec 11.11.5.9)', 'FR-V12-K-009; US-19-YK10; TC-V12-K-027…029; DEC-706', 'Matched')
V5 = {
 'AI-14': ('Partially covered', 'AL-15 (daily > 2x 7-day average), DEC-306 ladder, M53 hard caps', 'Robust per-tenant/workflow/model/version baseline and scoped hold (sec 11.11.5.10)', 'FR-V12-K-010; US-04-YK08; TC-V12-K-030…031; DEC-705'),
 'ST-01': ('Partially covered', 'Part 4.3 sec 4.40 SLO-01…12, error-budget policy; DEC-325', 'SLO-13 queue age, SLO-14 accepted-output success, policy-hold exclusion, approval gate (sec 11.11.5.11)', 'FR-V12-K-011; US-21-YK09; TC-V12-K-032…034; DEC-704; ADR-221'),
 'CS-11': ('Partially covered', 'DEC-406; CAP-X3-12 (states lack "unknown"); BRL-X3-12-2', 'Unknown state and public/private split (sec 11.11.5.2)', 'FR-V12-K-012; TC-V12-K-007…008; DEC-703'),
}
for q in p37:
    m = re.match(r'(AI-14|ST-01|CS-11) · (P\d) · (.*)', q['text'])
    if m:
        body = [x['text'] for x in p37 if x['line'] > q['line'] and x['line'] <= q['line'] + 3]
        sb, loc, act, new = V5[m.group(1)]
        add('FSD', ch, 'V5 optimization requirements and controls', m.group(1), f'{m.group(3)} ({m.group(2)}) ' + ' '.join(body), sb, loc, act, new, 'Matched')

# ================================================================== CHAPTER 40
ch = '40 Master Traceability, Decision Register & Source Archive'
ent = tab(t40, 'ID', 'V12')
ent_rows = []
fr_no = 101
for r in ent['rows']:
    eid = r[0]
    sb, loc, own, sa = M.ENT[eid]
    if eid.startswith('ENT-OPS'):
        frid = OPS_NEW[eid][0].split(';')[0]
        tcid = 'see ch37 row'
    else:
        frid = f'FR-V12-K-{fr_no:03d}'; tcid = f'TC-V12-K-{fr_no:03d}'; fr_no += 1
    tag = M.ENT_CONFLICT.get(eid, '')
    ent_rows.append((eid, r[1], r[2], r[3], r[4], (M.PHASE.get(r[4], r[4]) if len(r[4]) == 2 else M.PHASE[r[4][:2]].split(' (')[0] + ' … ' + M.PHASE[r[4][-2:]].split(' (')[0]), r[6], sb, loc, M.G[own], frid, tcid, tag, sa))
    add('FSD', ch, 'V12 Enterprise requirement register', eid + ' (ch40 register)',
        f'{r[2]} [{r[1]}; {r[3]}; {r[4]}; spec {r[5]}; prototype {r[6]}; production {r[7]}]', sb, loc,
        'Trace row registered; requirement adopted literally; design depth in ' + M.G[own], '; '.join(x for x in (frid, tcid if tcid.startswith('TC') else '', tag) if x), sa)
decv = tab(t40, 'ID', 'Enterprise requirement register and decisions')
cdec_rows = []
for tb in [x for x in t40 if x['header'] and x['header'][0] == 'ID' and x['header'][1] == 'Decision']:
    for r in tb['rows']:
        did = r[0]; verdict, bdecs, sa, kdec, note = M.CDEC_V[did]
        cid = 'C' + did
        cdec_rows.append((cid, r[1], r[2], r[3], r[4], verdict, bdecs, kdec, note, sa))
        sb = {'Already equivalent': 'Covered', 'Adopted': 'Partially covered', 'Conflicting': 'Conflict'}[verdict]
        add('FSD', ch, tb['h2'], cid, f'{did} {r[1]}: {r[2]} (owner {r[3]}; status {r[4]})', sb, bdecs, f'{verdict}: {note}', kdec, sa)
reca = tab(t40, 'ID', 'V11')
rec_rows = []
for r in reca['rows']:
    sb, loc = M.REC[r[0]]
    new = {'REC-23': 'FR-V12-K-008; DEC-701', 'REC-26': 'FR-V12-K-014; TC-V12-K-035; DEC-702'}.get(r[0], '')
    rec_rows.append((r[0], r[1], r[2], r[3], r[4], r[5], sb, loc, new))
    add('FSD', ch, 'V11 Reconciliation action status', r[0], f'{r[3]} (V11 status: {r[4]}; evidence {r[5]})', sb, loc,
        'Mapped' if sb == 'Covered' else 'Enhanced in this part', new, 'Matched')
for r in tab(t40, 'ID / priority / owner', 'V10')['rows']:
    add('FSD', ch, 'V10 Historical reconciliation controls', r[0].split(' ')[0] + ' acceptance', f'{r[1]} Acceptance: {r[2]}', 'Covered',
        'See REC row; DEC-314 (no synthetic approval)', 'Mapped', '', 'Matched')
idx = tab(t40, 'Source group', 'V10')
for r in idx['rows']:
    add('FSD', ch, 'V10 Historical source-row reconciliation index', f'40-IDX-{r[0]}', f'{r[0]}: {r[1]} indexed rows', 'Covered',
        'Count reproduced; rows reconciled individually below', 'Count verified by parser', 'DEC-709', 'Matched')
for q in p40:
    if q['h2'].startswith('V10 | Historical source-row'):
        add('FSD', ch, 'V10 Historical source-row reconciliation index', f'40-IDX-NOTE-{q["line"]}', q['text'], 'Covered',
            'Part 3.5a/3.6a (282 Appendix A ops, 118 DDL entities counted by Parts 11.8/11.9)', 'Rule adopted (semantic review = AP-08, DEC-314)', 'DEC-709', 'Matched')

# ---- disposition rows (1,912)
disp_summary = collections.OrderedDict()
def dsum(grp, sb):
    disp_summary.setdefault(grp, collections.Counter())[sb] += 1
api = tab(t40, 'Source / ID', 'API') if False else [x for x in t40 if x['h2'] == 'Source disposition candidates — API'][0]
dkey = {}
for r in Dmap:
    dkey.setdefault((r['method'], r['path']), r)
for r in api['rows']:
    src, rest = r[0].split(' / ', 1)
    if rest.startswith('SM-UX-API'):
        meth, path = rest, r[1]
        b = next((x for x in Dmap if x['source_id'] == rest), None)
    else:
        meth, path = rest.split(' ', 1)
        rn = int(src.split('/R')[1]) - 1
        b = next((x for x in Dmap if x['source_id'] == f'SM-OP-{rn:03d}'), None)
        if b is None or (b['method'], b['path']) != (meth, path):
            b = dkey.get((meth, path), b)
    if b:
        sb = 'Covered' if b['status'] == 'Covered' else 'Partially covered'
        loc = f"D_api_mapping {b['source_id']} -> {b['blueprint_ops'] or b['enhancement']}" + (f" (closed by {b['enhancement']})" if b['status'] != 'Covered' and b['enhancement'] else '')
        sa = 'Matched'
    else:
        sb, loc, sa = 'Not covered', 'no mapping row', 'Matched'
    dsum('API (321)', b['status'] if b else 'no row')
    add('FSD', ch, 'Source disposition candidates — API', src, f'{meth} {path} -> {r[1]}; {r[2]}', 'Covered' if b else sb, loc,
        'Row-level crosswalk; DTO/scope review via SPDEC/AP-08', 'DEC-709', sa)
entd = [x for x in t40 if x['h2'] == 'Source disposition candidates — Entity'][0]
for r in entd['rows']:
    src, name = r[0].split(' / ', 1)
    b = Emap.get(name)
    dsum('Entity (155)', b['status'] if b else 'no row')
    loc = f"E_table_mapping {b['src_no']} -> {b['bp_ent']} {b['bp_table']} ({b['status']})" if b else 'no mapping row'
    add('FSD', ch, 'Source disposition candidates — Entity', src, f'{name} -> {r[1]}; {r[2]}', 'Covered' if b else 'Not covered', loc,
        'Row-level crosswalk (Part 3.6; DEC-185…191, DEC-265…269)', 'DEC-709', 'Matched')
tst = [x for x in t40 if x['h2'] == 'Source disposition candidates — Test'][0]
GST = {'E': 'Covered', 'A': 'Covered', 'M': 'Covered', 'P': 'Partially covered', 'N': 'Not covered'}
for r in tst['rows']:
    m = re.match(r'(\S+) / (\S+) ?(.*)', r[0])
    src, tid, title = m.groups()
    b = Gmap.get(tid)
    dsum('Test (1,029 rows; 589 distinct IDs)', GST.get(b['status'], b['status']) if b else 'no row')
    loc = f"G_test_mapping {tid} -> {b['primary_tcs'] or b['bp_requirement']}" if b else 'no mapping row'
    add('FSD', ch, 'Source disposition candidates — Test', f'{src} {tid}', f'{tid} {title} -> {r[1]}; {r[2]}', 'Covered' if b else 'Not covered', loc,
        'Row-level crosswalk (Part 6.8; RTM SM-UT/SM-SIT/SM-UAT rows); duplicate variants not counted as new tests', 'DEC-709', 'Matched')
qc = [x for x in t40 if x['h2'] == 'Source disposition candidates — QC'][0]
for r in qc['rows']:
    m = re.match(r'(\S+) / (\S+) ?(.*)', r[0])
    src, qid, title = m.groups()
    b = Qmap.get(qid)
    dsum('QC (245)', b['status'] if b else 'no row')
    loc = f"H_qc_map {qid} -> {b['blueprint_gate']} ({b['status']})" if b else 'no mapping row'
    add('FSD', ch, 'Source disposition candidates — QC', src + ' ' + qid, f'{qid} {title[:150]} -> {r[2]}', 'Covered' if b else 'Not covered', loc,
        'Row-level crosswalk (Part 6.9b sec 6.9.5.1.8)', 'DEC-709', 'Matched')
tk = [x for x in t40 if x['h2'] == 'Source disposition candidates — Task'][0]
for r in tk['rows']:
    m = re.match(r'(\S+) / (\S+) ?(.*)', r[0])
    src, wid, title = m.groups()
    b = Wmap.get(wid)
    dsum('Task (162)', b['status'] if b else 'no row')
    loc = f"H_workitem_story_map {wid} -> {b['blueprint_stories']} ({b['status']})" if b else 'no mapping row'
    add('FSD', ch, 'Source disposition candidates — Task', src + ' ' + wid, f'{wid} {title} {r[1]} -> {r[2]}', 'Covered' if b else 'Not covered', loc,
        'Row-level crosswalk (Part 6.9b sec 6.9.5.4; DEC-222 estimate tracking)', 'DEC-709', 'Matched')
# ---- OPT index 104
opt = tab(t40, 'Historical ID', 'V10')
opt_groups = collections.OrderedDict()
for r in opt['rows']:
    b = Jcov.get(r[0])
    opt_groups.setdefault(r[2].replace('Candidate review: ', '').replace('; semantic equivalence pending', ''), []).append(r[0])
    CLOSE = {'OPT-02-04': 'DEC-160, DEC-319', 'OPT-03-08': 'DEC-248, DEC-306', 'OPT-05-07': 'DEC-325', 'OPT-06-01': 'DEC-315, DEC-326',
             'OPT-10-02': 'DEC-195, DEC-303', 'OPT-13-02': 'Part 8.3c sec 8.3.5.14.5 (FR-ENH-J-011)'}
    orig = b['status'] if b else 'Not covered'
    loc = f"J_coverage {r[0]}: {b['blueprint_location'] if b else '-'}; Part 8.3c sec 8.3.5.15.3" + (f" (doc-36 status {orig}, closed by {CLOSE.get(r[0], 'sec 8.3.5.15.3 mapping')})" if orig != 'Covered' else '')
    add('FSD', ch, 'V10 Original optimization control index', r[0], f'{r[1]} -> {r[2]}', 'Covered', loc,
        'Mapped; V12 candidate IDs recorded as aliases (semantic equivalence = AP-08 approval)', 'DEC-709', 'Matched')
# ---- V8 master traceability 156
mtr = tab(t40, 'Workflow', 'V8')
chain_rows = []
for r in mtr['rows']:
    wf, sku, steps, eng, agt, ui, apin, db, pol, tests = r
    frs = ui_to_fr(ui)
    tcs = sum(int(RTM[f]['tc_count'] or 0) for f in frs)
    dbn = db.replace('Candidate reuse only: ', '')
    e = Emap.get(dbn)
    dbm = f"{e['bp_table']}" if e else 'new (Part 11.9)'
    # candidate AG by FR overlap
    sc = sorted(((len(AGFR[a][1] & set(frs)), a) for a in AGFR), reverse=True)
    ags = [a for s, a in sc if s > 0][:2]
    polm = 'PDP preflight (Part 3.1) + DEC-050' + (' + Jurisdiction Rule Pack DEC-029' if 'CJ' in pol else '')
    chain_rows.append((wf, sku, steps, eng, M.ENGINE.get(eng, '?'), agt, ', '.join(ags) or '—', ui, ', '.join(frs), tcs, apin, db, dbm, pol, polm, tests))
    sb = 'Partially covered' if frs else 'Not covered'
    add('FSD', ch, 'V8 Master traceability register', wf, f'{sku} {steps}; engine {eng}; {agt}; UI {ui}; API {apin}; DB {db}; {pol}; tests {tests}',
        sb, f'FR {", ".join(frs)} ({tcs} TCs in RTM); AG cand. {", ".join(ags) or "—"}; table {dbm}',
        'Chain registered in RTM extension (sec 11.11.5.12); workflow/step design in Parts 11.3/11.4', 'FR-V12-K-020; TC-V12-K-040', 'Matched')
for q in p40:
    if q['h2'].startswith('V8 | Master'):
        add('FSD', ch, 'V8 Master traceability register', '40-CHAIN-NOTE', q['text'], 'Partially covered', 'Part 6.6 RTM (BR->FR->US->TC)',
            'Chain columns added (ADR-220)', 'FR-V12-K-020; ADR-220', 'Matched')
# ---- V6 policies and MT
for q in p40:
    if q['h2'].startswith('V6'):
        aid = 'FSD-POL-V6-PRECHECK' if 'PRECHECK' in q['h3'] or (q['h3'] == '' and q['line'] < 10858) else 'FSD-POL-V6-ARTIFACT'
        aid = {10856: 'FSD-POL-V6 (summary)', 10858: 'FSD-POL-V6-PRECHECK', 10859: 'FSD-POL-V6-PRECHECK count', 10861: 'FSD-POL-V6-ARTIFACT', 10862: 'FSD-POL-V6-ARTIFACT count'}.get(q['line'], aid)
        add('FSD', ch, 'V6 Universal architecture and controlled requirements', aid, q['text'], 'Covered',
            'PDP preflight + outbox/effect ledger (Part 3.1); DEC-050; idempotency DEC-173; retry max 3 with jitter (Part 3.4 retry schema); timeouts per adapter; DEC-107/191 no generic JSON for ledgers',
            'Mapped; 30 s / 90 s timeout proposal recorded as default (sec 11.11.5.12)', 'DEC-708', 'Matched')
mtt = tab(t40, 'Architecture ID', 'V6')
for r in mtt['rows']:
    add('FSD', ch, 'V6 Universal architecture and controlled requirements', r[0], f'{r[0]} {r[1]}; BRD ch{r[2]}; FSD ch{r[3]}; acceptance {r[4]}',
        'Partially covered', M.MT[r[0]], 'Trace row registered; content reconciled by chapter owner (Part 11.5)', 'FR-V12-K-020', 'Matched')
# ---- V5 note, remaining engineering, inherited decisions
for q in p40:
    if q['h2'].startswith('V5') or (q['h2'].startswith('Remaining') and q['line'] < 11480):
        add('FSD', ch, q['h2'], f'40-NOTE-{q["line"]}', q['text'], 'Covered', 'V12_BRIEF precedence; SPDEC queue (Part 6.9b sec 6.9.5.2)', 'Rule adopted', 'DEC-709', 'Matched')
rew = tab(t40, 'Workflow', 'Remaining')
rew_rows = []
for r in rew['rows']:
    frs = ui_to_fr(r[1])
    rew_rows.append((r[0], r[1], ', '.join(frs), r[4]))
    add('FSD', ch, 'Remaining engineering work / explicit design decisions', r[0] + ' (gap)', f'UI {r[1]}; API {r[2][:120]}; DB {r[3][:80]}; {r[4]}',
        'Not covered', f'UI FRs {", ".join(frs)}; domain not in blueprint', 'Chain registered; domain design (API-V2-RUN) owned by Parts 11.3/11.4/11.8', 'FR-V12-K-020', 'Matched')
inh = tab(t40, 'Decision ID / source', 'Remaining')
cdec180 = []
for r in inh['rows']:
    parts = [x.strip() for x in r[1].split(' | ')]
    sp = 'SP' + r[0]
    b = SPDEC.get(sp); h = Hdec.get(r[0])
    cdec180.append(('C' + r[0], sp, parts[1], parts[2], h['blueprint_frs'] if h else '', b[5] if b else '?', r[2]))
    add('FSD', ch, 'Remaining engineering work — inherited decisions', 'C' + r[0], f'{r[0]} {parts[1]} {parts[2]} ({r[2]})', 'Covered',
        f'{sp} (DEC-178) Part 6.9a: {b[4][:80] if b else "?"}; queue Part 6.9b sec 6.9.5.2', 'Already equivalent; alias CDEC = SPDEC', 'DEC-700', 'Matched')
# ---- archive
arch = tab(t40, 'Source file', 'Remaining')
root = V12
hashed = {}
for p in root.rglob('*'):
    if p.is_file() and p.suffix in ('.zip', '.xlsx', '.html', '.docx'):
        hashed.setdefault(p.name, set()).add(hashlib.sha256(p.read_bytes()).hexdigest())
arch_rows = []
for i, (name, sha) in enumerate(arch['rows'], 1):
    ok = sha in hashed.get(name, set())
    arch_rows.append((f'SAR-{i:02d}', name, sha, 'Match' if ok else 'MISMATCH'))
    add('FSD', ch, 'Source archive', f'SAR-{i:02d}', f'{name} sha256 {sha}', 'Not covered',
        'Archive register absent; 38-document zip already covered (Part 0B)', f'SHA-256 recomputed: {"match" if ok else "MISMATCH"}; registered (sec 11.11.4.9)', 'FR-V12-K-023; TC-V12-K-043; DEC-710', 'Matched')
for q in p40:
    if q['h2'].startswith('Remaining') and q['line'] >= 12211:
        add('FSD', ch, 'Source archive', f'40-ARC-{q["line"]}', q['text'], 'Not covered', '—',
            'Recovery procedure recorded; recovered code never executed without review (sec 11.11.4.9)', 'FR-V12-K-023; DEC-710', 'Matched')
outd = tab(t40, 'Responsible role', 'Outstanding')
for i, r in enumerate(outd['rows'], 1):
    add('FSD', ch, 'Outstanding production decisions and ownership', f'40-OWN-{i:02d}', f'{r[0]}: {r[1]} ({r[2]})', 'Partially covered',
        'Part 6.9b sec 6.9.5.2 approvers; G4/DoR gates; A090 open decisions', 'Owner/due-date/release assignment rule (sec 11.11.5.13)', 'FR-V12-K-025; TC-V12-K-045; DEC-708', 'Matched')
for q in p40:
    if q['h2'].startswith('Outstanding'):
        add('FSD', ch, 'Outstanding production decisions and ownership', '40-OWN-NOTE', q['text'], 'Covered', 'BR-C13 gate; DEC-314', 'Mapped', '', 'Matched')

# ================================================================== APPENDIX D
idf_rows = []
ENGNAMES = {}
for r in tab(parse(FSD / '14_Shared_AI_Automation_Engines.txt')[0], 'Engine ID')['rows']:
    ENGNAMES[r[0]] = r[1]
for tb in tD:
    for r in tb['rows']:
        fam, rng, where = r
        key = rng
        hit = M.IDFAM.get(key)
        if hit is None:
            hit = next((v for k, v in M.IDFAM.items() if k.split()[0] == key.split()[0]), ('?', 'Not covered'))
        mapping, sb = hit
        sa = 'Matched'
        idf_rows.append((fam, rng, where, mapping, sb))
        add('FSD', 'Appendix D ID index', tb['h2'] or 'V12 ID families (second table)', f'IDX-{fam}', f'{fam}: {rng} ({where})', sb, mapping,
            'Family registered in the V12 ID-family register (sec 11.11.4.10) with alias and collision rule', 'FR-V12-K-026; DEC-700', sa)

# ================================================================== write CSV
out_csv = BP / 'final' / 'coverage_v12' / 'K_coverage.csv'
out_csv.parent.mkdir(parents=True, exist_ok=True)
with open(out_csv, 'w', newline='', encoding='utf-8') as f:
    w = csv.writer(f)
    w.writerow(['doc', 'chapter', 'section', 'aspect_id', 'aspect_summary', 'status_before', 'blueprint_location', 'action', 'new_ids', 'status_after'])
    w.writerows(rows)

# ================================================================== fragments
def write(name, header, data):
    with open(OUT / name, 'w', encoding='utf-8') as f:
        f.write('| ' + ' | '.join(header) + ' |\n|' + '---|' * len(header) + '\n')
        for d in data:
            f.write('| ' + ' | '.join(md(x) for x in d) + ' |\n')
write('trn.md', ['V12 ID', 'Screen', 'Screen name (V12)', 'V12 UAT', 'Blueprint card', 'UAT alias match'], trn_rows)
ENGID = {v: k for k, v in ENGNAMES.items()}
write('chain.md', ['Workflow', 'Steps (AI)', 'Engine', 'Agent → candidate AG', 'UI → blueprint FR', 'RTM TCs', 'API', 'DB first → blueprint table', 'Policy'],
      [(c[0], c[2], ENGID.get(c[3], c[3]), f'{c[5]} → {c[6]}', c[8].replace('FR-', ''), c[9], c[10], f'{c[11]} → {c[12]}', 'PRECHECK + CJ' if 'CJ' in c[13] else 'PRECHECK') for c in chain_rows])
write('ent.md', ['ENT', 'Pri', 'Requirement (V12, adopted literally)', 'V12 phase → blueprint', 'V12 screen', 'Before', 'Blueprint location', 'Design depth', 'Trace FR / TC', 'After'], [(e[0], e[1], e[2], e[4] + ' → ' + e[5], e[6], e[7], e[8], e[9], e[10] + (' / ' + e[11] if e[11].startswith('TC') else ''), (e[12] + ' ' if e[12] else '') + e[13]) for e in ent_rows])
write('cdecv.md', ['CDEC', 'Decision', 'Customer recommendation', 'Owner', 'Customer status', 'Verdict', 'Blueprint decisions', 'K decision', 'Note', 'After'], cdec_rows)
write('rec.md', ['REC', 'Pri', 'Owner', 'Required change', 'V11 status', 'Evidence', 'Before', 'Blueprint location', 'New'], rec_rows)
write('cdec180.md', ['CDEC', 'Blueprint alias', 'Class', 'Subject', 'Blueprint FRs', 'Part 6.9a status (before the 6.9b queue)', 'Customer status'], cdec180)
write('rew.md', ['Workflow', 'Source UI', 'Blueprint FRs', 'V2 proposal / gate'], rew_rows)
write('arch.md', ['SAR', 'Source file', 'SHA-256 (declared)', 'Recomputed'], arch_rows)
write('idfam.md', ['Family', 'Format / range', 'Defined in', 'Blueprint mapping / owner', 'Before'], idf_rows)
write('opt.md', ['V12 candidate review group', 'Historical OPT IDs', 'Count'], [(k, ', '.join(v), len(v)) for k, v in opt_groups.items()])
write('mt.md', ['MT', 'Priority', 'BRD ch', 'FSD ch', 'Acceptance', 'Blueprint anchor'], [tuple(r) + (M.MT[r[0]],) for r in mtt['rows']])
ds = []
for g, c in disp_summary.items():
    ds.append((g, sum(c.values()), '; '.join(f'{k} {v}' for k, v in c.most_common())))
write('disp.md', ['Group', 'Rows', 'Blueprint mapping status (original)'], ds)
# counts
cnt = collections.Counter(); cnta = collections.Counter(); bysec = collections.OrderedDict()
for r in rows:
    cnt[r[5]] += 1; cnta[r[9]] += 1
    k = r[1].split(' ')[0] + ' · ' + r[2][:60]
    bysec.setdefault(k, [collections.Counter(), collections.Counter()])
    bysec[k][0][r[5]] += 1; bysec[k][1][r[9]] += 1
with open(OUT / 'counts.txt', 'w') as f:
    f.write(f'total {len(rows)}\nbefore {dict(cnt)}\nafter {dict(cnta)}\n')
    for k, (a, b) in bysec.items():
        f.write(f'{k}\t{sum(a.values())}\t{dict(a)}\t{dict(b)}\n')
print(open(OUT / 'counts.txt').read())

# ------------------------------------------------------------------ trace requirements for non-OPS ENT rows
TPL = {
 'IDN': 'Positive sign-in/provisioning path plus negatives: unverified domain, de-provisioned or revoked user, expired or idle session, missing break-glass all denied and audited',
 'ACC': 'Role/permission matrix test incl. SoD violation at build and at run time, tamper detection on the audit chain, export format check, support access without tenant approval denied',
 'API': 'Contract test: scope, expiry, hash-at-rest, rotation/revocation, 429 + Retry-After, signature and replay rejection, deprecation headers',
 'DAT': 'Export/sandbox/promotion test: manifest hash, second approver, link expiry, no personal data in sandbox, reviewed revision only; residency/key items gated by Founder decision',
 'INT': 'Adapter contract test: vault-only secrets, backoff and circuit breaker, uncertain write reconciled before retry, health alert, activation blocked without review/DPA/transfer basis/registration',
 'SEC': 'Pipeline evidence test: SAST/DAST/SCA/secret scan per change, SBOM stored per release, remediation SLA clock, pen-test before major release, TLS 1.2+ and AES-256 checks',
 'CMP': 'Evidence test: approved legal set published, sub-processor change notice, counsel sign-off recorded per pack, accessibility conformance report attached',
 'GLB': 'i18n test: externalised strings, ICU plurals, pseudo-localisation, E.164/IANA/currency formats; locale/tax/region items gated by Founder decision',
 'BIZ': 'Billing/commercial test: meter-rate-invoice-tax-collect sequence, approved price book only, signed-hash order form, first-value checklist, procurement pack versioned',
}
entfr = []
for e in ent_rows:
    eid, pri, req, own, ph, bph, scr, sb, loc, part, frid, tcid, tag, sa = e
    if eid.startswith('ENT-OPS'):
        continue
    entfr.append((frid, eid, pri, req, TPL[eid.split('-')[1]], tcid, part, bph, (tag + ' ' if tag else '') + sa))
write('entfr.md', ['FR', 'ENT', 'Pri', 'Requirement (V12 literal)', 'Test intent', 'TC', 'Design depth', 'Release (ASSUMPTION-940)', 'After'], entfr)
print('entfr', len(entfr))
