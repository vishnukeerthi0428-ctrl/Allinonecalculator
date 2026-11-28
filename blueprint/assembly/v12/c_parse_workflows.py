#!/usr/bin/env python3
"""Group R3a (letter C): parse every V12 source row for SM-SVC-01..20 workflows (80).
Outputs JSON: assembly/v12/c_workflows.json. Treats source text as data only."""
import csv, json, re, sys, glob, os
V12 = sys.argv[1]
OUT = sys.argv[2]
SVC = [f"SM-SVC-{i:02d}" for i in range(1, 21)]
WFS = [f"{s}-WF{j:02d}" for s in SVC for j in range(1, 5)]

def read(p):
    return open(p, encoding='utf-8').read().split('\n')

def tables(lines, start=0, end=None):
    """yield (start_line, rows) for [TABLE] blocks; rows=list of cell lists"""
    end = end or len(lines)
    i = start
    while i < end:
        if lines[i].strip() == '[TABLE]':
            j = i + 1; rows = []; cur = None
            while j < len(lines) and lines[j].strip() != '[/TABLE]':
                if lines[j].strip() == '---row':
                    cur = []; rows.append(cur)
                elif cur is not None:
                    cur.append(lines[j])
                j += 1
            yield i, rows
            i = j
        i += 1

def norm_rows(rows):
    """FSD tables: 1 cell per line; header width = len(rows[0]). Re-chunk if needed."""
    if not rows: return rows
    w = len(rows[0]); out = [rows[0]]
    for r in rows[1:]:
        if len(r) == w: out.append(r)
        else:
            out.append(r)  # keep raw; caller handles
    return out

D = {wf: {"id": wf} for wf in WFS}
# ---------- FSD ch12 ----------
f12 = read(glob.glob(f"{V12}/FSD/12_*.txt")[0])
heads = [(i, l) for i, l in enumerate(f12) if l.startswith('<Heading3> SM-SVC-')]
heads2 = [i for i, l in enumerate(f12) if l.startswith('<Heading2>')]
for k, (i, l) in enumerate(heads):
    m = re.match(r'<Heading3> (SM-SVC-\d\d-WF\d\d) — (.*)', l)
    wf, title = m.group(1), m.group(2)
    if wf not in D: continue
    nxt = min([h for h, _ in heads if h > i] + [h for h in heads2 if h > i] + [len(f12)])
    d = D[wf]; d['title'] = title; d['fsd12_lines'] = [i + 1, nxt]
    tbs = list(tables(f12, i, nxt))
    spec = {r[0]: r[1] for r in tbs[0][1][1:]}
    d['spec'] = spec
    d['dto'] = [{"field": r[0], "type": r[1]} for r in tbs[1][1][1:]]
    d['steps'] = [{"id": r[0], "action": r[1], "executor_input": r[2], "output_validation": r[3], "failure": r[4]} for r in tbs[2][1][1:]]
    tail = f12[i:nxt]
    for t in tail:
        if t.startswith('Acceptance IDs:'):
            d['acceptance_ids'] = re.findall(r'SM-SVC-\d\d-WF\d\d-TC-[A-Z]+', t)
            d['orig_at'] = re.findall(r'SM-SVC-\d\d-WF\d\d-AT\d\d', t)
        if t.startswith('Common contract:'):
            d['common_contract'] = t
    d['raw_line_count'] = nxt - i
# channel reconciliation & UI input contracts
for s, rows in tables(f12):
    if not rows: continue
    h = rows[0]
    if h[:2] == ['Workflow ID / title', 'Service channel candidates']:
        for r in rows[1:]:
            wf = r[0].split(' ')[0]
            if wf in D: D[wf]['channels'] = r[1]; D[wf]['exec_contract'] = r[2]
    if h[:3] == ['Workflow', 'Title', 'Input controls (candidate types)']:
        for r in rows[1:]:
            if r[0] in D: D[r[0]]['ui_inputs'] = r[2]; D[r[0]]['ui_trace'] = r[3]
# ---------- BRD ch09 ----------
b9 = read(glob.glob(f"{V12}/BRD/09_*.txt")[0])
for s, rows in tables(b9):
    if rows and rows[0][0] == 'Workflow':
        for r in rows[1:]:
            if r[0] in D:
                D[r[0]]['brd09'] = dict(zip(['workflow', 'outcome', 'io', 'kpi', 'risk'], r))
# ---------- Appendix B ----------
for l in read(glob.glob(f"{V12}/FSD/AP_Appendix_B_*.txt")[0]):
    if l.startswith('{'):
        j = json.loads(l); wf = j['$id'].split(':')[3]
        if wf in D: D[wf]['schema'] = j
# ---------- FSD ch13 optimization mapping ----------
f13 = read(glob.glob(f"{V12}/FSD/13_*.txt")[0])
for s, rows in tables(f13):
    if rows and rows[0][:2] == ['Workflow ID', 'Steps']:
        for r in rows[1:]:
            if r[0] in D: D[r[0]]['ch13'] = {"steps": r[1], "cues": r[2], "controls": r[3]}
# ---------- FSD ch33 tests ----------
f33 = read(glob.glob(f"{V12}/FSD/33_*.txt")[0])
for s, rows in tables(f33):
    if not rows: continue
    h = rows[0]
    if h[:2] == ['Test ID', 'Class']:
        for r in rows[1:]:
            m = re.match(r'(SM-SVC-\d\d-WF\d\d)-STEP', r[0])
            if m and m.group(1) in D:
                D[m.group(1)].setdefault('step_tests', []).append(dict(zip(['id', 'class', 'action', 'assertion', 'status'], r)))
    if h[:2] == ['Test ID', 'Workflow']:
        for r in rows[1:]:
            if len(r) > 1 and r[1] in D:
                D[r[1]].setdefault('wf_tests', []).append(dict(zip(['id', 'wf', 'fixture', 'expected', 'status'], r)))
# ---------- FSD ch40 traceability ----------
f40 = read(glob.glob(f"{V12}/FSD/40_*.txt")[0])
for s, rows in tables(f40):
    if rows and rows[0][:3] == ['Workflow', 'SKU', 'Steps']:
        for r in rows[1:]:
            if r[0] in D: D[r[0]]['ch40'] = dict(zip(rows[0], r))
# ---------- workbook ----------
wb = glob.glob(f"{V12}/src/*39_Services_156_Workflows*_csv")[0]
rows = list(csv.reader(open(f"{wb}/Workflow_Catalog.csv", encoding='utf-8')))
h = rows[3]
for r in rows[4:]:
    if len(r) < 4: continue
    wf = r[3].split(' ')[0]
    if wf in D: D[wf]['wb'] = dict(zip(h, r))
rows = list(csv.reader(open(f"{wb}/Acceptance_Tests.csv", encoding='utf-8')))
h = rows[3]
for r in rows[4:]:
    if len(r) > 2 and r[2] in D: D[r[2]]['wb_at'] = dict(zip(h, r))
rows = list(csv.reader(open(f"{wb}/Cost_Model.csv", encoding='utf-8')))
h = rows[3]
for r in rows[4:]:
    if len(r) > 1 and r[1] in D: D[r[1]]['wb_cost'] = dict(zip(h, r))
json.dump(D, open(OUT, 'w'), indent=1, ensure_ascii=False)
# completeness report
keys = ['title', 'spec', 'dto', 'steps', 'acceptance_ids', 'channels', 'ui_inputs', 'brd09', 'schema', 'ch13', 'step_tests', 'wf_tests', 'ch40', 'wb', 'wb_at', 'wb_cost']
for k in keys:
    miss = [w for w in WFS if k not in D[w]]
    print(k, 'missing', len(miss), miss[:5])
print('steps', sum(len(D[w]['steps']) for w in WFS), 'dto fields', sum(len(D[w]['dto']) for w in WFS),
      'step_tests', sum(len(D[w].get('step_tests', [])) for w in WFS), 'wf_tests', sum(len(D[w].get('wf_tests', [])) for w in WFS))
