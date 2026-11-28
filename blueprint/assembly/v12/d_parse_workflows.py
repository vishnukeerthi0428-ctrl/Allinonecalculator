"""Group D (Part 11.4): parse every V12 source row for SM-SVC-21..39 workflows.
Sources: FSD ch12 (spec, DTO, steps, acceptance, channel, UI input), FSD ch13 (registry mapping),
BRD ch09 (business catalogue), FSD Appendix B (JSON Schemas), src Workflow_Catalog.csv (50 fields).
Output: d_workflows.json (one record per workflow) + d_counts.json."""
import csv, json, re, sys, glob, os
V12 = sys.argv[1]
OUT = os.path.dirname(os.path.abspath(__file__))
def rd(p): return open(p, encoding='utf-8').read().split('\n')
def svcnum(w): return int(w[7:9])
fsd12 = rd(glob.glob(V12+'/FSD/12_*')[0])
fsd13 = rd(glob.glob(V12+'/FSD/13_*')[0])
brd09 = rd(glob.glob(V12+'/BRD/09_*')[0])
apb = rd(glob.glob(V12+'/FSD/AP_Appendix_B_*')[0])
csvp = glob.glob(V12+'/src/*39_Services_156_Workflows*_csv/Workflow_Catalog.csv')[0]

def tables(lines):
    """yield (start_line, rows) for every [TABLE] block"""
    i = 0
    while i < len(lines):
        if lines[i].strip() == '[TABLE]':
            rows, cur, j = [], None, i+1
            while lines[j].strip() != '[/TABLE]':
                if lines[j].strip() == '---row':
                    if cur is not None: rows.append(cur)
                    cur = []
                else: cur.append(lines[j])
                j += 1
            if cur is not None: rows.append(cur)
            yield i, rows
            i = j
        i += 1

WF = {}
# ---- FSD 12 per-workflow entries
heads = [(i, l) for i, l in enumerate(fsd12) if l.startswith('<Heading')]
svc_title = {}
for k, (i, l) in enumerate(heads):
    m = re.match(r'<Heading2> (SM-SVC-\d\d) — (.*)', l)
    if m: svc_title[m.group(1)] = m.group(2)
    m = re.match(r'<Heading3> (SM-SVC-(\d\d)-WF0\d) — (.*)', l)
    if not m or int(m.group(2)) < 21: continue
    wid = m.group(1); end = heads[k+1][0] if k+1 < len(heads) else len(fsd12)
    block = fsd12[i:end]
    rec = {'id': wid, 'svc': wid[:9], 'title': m.group(3), 'fsd12_lines': [i+1, end]}
    tb = list(tables(block))
    rec['spec'] = {r[0]: ' '.join(r[1:]) for r in tb[0][1][1:]}
    rec['dto'] = [{'field': r[0], 'type': r[1]} for r in tb[1][1][1:]]
    rec['steps'] = [dict(zip(['step_id','action','executor_input','output_validation','failure'], r)) for r in tb[2][1][1:]]
    for l2 in block:
        if l2.startswith('Acceptance IDs:'):
            rec['acceptance'] = re.findall(r'SM-SVC-\d\d-WF0\d-TC-[A-Z]+', l2)
            rec['source_at'] = re.findall(r'SM-SVC-\d\d-WF0\d-AT\d\d', l2)
        if l2.startswith('Common contract:'): rec['common_contract'] = l2
    rec['extra_lines'] = [l2 for l2 in block[1:] if not l2.startswith(('[','---','Acceptance IDs','Common contract')) and l2 not in sum([sum(r, []) for _, r in tb], [])]
    WF[wid] = rec
svc_ids = sorted({w[:9] for w in WF})
# channel reconciliation + UI input contracts
for _, rows in tables(fsd12):
    hdr = rows[0]
    if hdr[:2] == ['Workflow ID / title', 'Service channel candidates']:
        for r in rows[1:]:
            wid = r[0][:14]
            if wid in WF: WF[wid]['channel'] = {'title': r[0][15:], 'channels': r[1], 'contracts': r[2]}
    if hdr[:3] == ['Workflow', 'Title', 'Input controls (candidate types)']:
        for r in rows[1:]:
            if r[0] in WF: WF[r[0]]['ui_input'] = {'title': r[1], 'controls': r[2], 'trace': r[3]}
# ---- FSD 13 registry mapping
for _, rows in tables(fsd13):
    if rows[0][:2] == ['Workflow ID', 'Steps']:
        for r in rows[1:]:
            if r[0] in WF: WF[r[0]]['registry'] = {'steps': int(r[1]), 'executor_cues': r[2], 'controls': r[3]}
# ---- BRD 09
for _, rows in tables(brd09):
    if rows[0][:2] == ['Workflow', 'Business outcome']:
        for r in rows[1:]:
            if r[0] in WF: WF[r[0]]['brd09'] = dict(zip(['outcome_title','io','kpi','risk'], r[1:]))
# ---- Appendix B
for l in apb:
    if l.startswith('{'):
        js = json.loads(l); wid = js['$id'].split(':')[3]
        if wid in WF: WF[wid]['schema'] = js
# ---- CSV
rows = list(csv.reader(open(csvp, encoding='utf-8')))
hdr = rows[3]
for r in rows[4:]:
    if len(r) < 4: continue
    wid = r[3][:14]
    if wid in WF: WF[wid]['csv'] = dict(zip(hdr, r))
# ---- validation
problems = []
for w, rec in WF.items():
    for k in ['spec','dto','steps','acceptance','channel','ui_input','registry','brd09','schema','csv']:
        if not rec.get(k): problems.append((w, k))
    if rec.get('registry') and rec['registry']['steps'] != len(rec['steps']): problems.append((w, 'stepcount', rec['registry']['steps'], len(rec['steps'])))
    if rec.get('schema'):
        f = set(rec['schema']['$defs']['input']['properties']) | set(rec['schema']['$defs']['output']['properties'])
        d = {x['field'] for x in rec['dto']}
        if f != d: problems.append((w, 'dto-schema mismatch', sorted(f ^ d)))
counts = {'workflows': len(WF), 'services': len(svc_ids), 'steps': sum(len(r['steps']) for r in WF.values()),
          'dto_fields': sum(len(r['dto']) for r in WF.values()), 'acceptance_ids': sum(len(r.get('acceptance', [])) for r in WF.values()),
          'source_at': sum(len(r.get('source_at', [])) for r in WF.values()), 'csv_fields': sum(len(r.get('csv', {})) for r in WF.values()),
          'problems': problems, 'svc_titles': {s: svc_title[s] for s in svc_ids}}
json.dump(WF, open(OUT+'/d_workflows.json', 'w'), indent=1, ensure_ascii=False)
json.dump(counts, open(OUT+'/d_counts.json', 'w'), indent=1, ensure_ascii=False)
print(json.dumps({k: v for k, v in counts.items() if k != 'svc_titles'}, indent=1))
