"""Builds final/coverage_v12/N_coverage.csv: (1) every CONFLICT-958 row of L_coverage.csv that belongs to
INV-SVC-01...12, the website or the common investment platform; (2) Group N's own atomic aspect inventory of
the source pack (services, workflows, acceptance, cost, entitlement, migration, technical map, crosswalk, index,
engines, decisions, start-here, website routes, layout items, investor-mode branches, README)."""
import sys, os, re, csv, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import n_ctx as C
import n_spec as SP

BP = '/home/user/Allinonecalculator/blueprint'
OUT = BP + '/final/coverage_v12/N_coverage.csv'
PA = 'Part 11.16a'; PB = 'Part 11.16b'; PC = 'Part 11.16e'
rows = []
def add(doc, chapter, section, aid, summary, before, loc, action, new_ids):
    rows.append(dict(doc=doc, chapter=chapter, section=section, aspect_id=aid, aspect_summary=summary[:400], status_before=before,
                     blueprint_location=loc, action=action, new_ids=new_ids, status_after='Matched'))

# ---------------- (1) L rows
SVC_RE = re.compile(r'(?:Primary service ID:\s*|^|Service ID:\s*)(INV-SVC-(\d\d))')
def primary(r):
    t = r['aspect_summary']
    m = re.search(r'Primary service ID:\s*(INV-SVC-\d\d|ALL)', t)
    if m:
        return m.group(1)
    m = re.match(r'\s*(INV-SVC-\d\d)\b', t) or re.search(r'Service ID:\s*(INV-SVC-\d\d)', t)
    if m:
        return m.group(1)
    m = re.search(r'\b(INV-(\d\d)-\d\d)\b', t)
    if m:
        cw = {x['Original capability ID']: x['Primary service ID'] for x in C.CW}
        return cw.get(m.group(1), 'ALL')
    return None

def loc_for(r, p):
    t = r['aspect_summary']; ch = r['chapter'] + ' ' + r['section']
    n = C.svc_no(p) if p and p != 'ALL' else None
    if 'Workflow' in ch and n:
        m = re.search(r'(INV-SVC-\d\d-WF\d\d)', t)
        return f'{PB} §11.16.5.12 {m.group(1) if m else p}', (C.FR_WF.get(m.group(1)) if m else '')
    if ('accepta' in ch.lower() or 'Acceptance' in ch) and n:
        m = re.search(r'(INV-SVC-\d\d-(?:WF\d\d|ENT)-AT01)', t)
        if m and 'ENT' in m.group(1):
            return f'{PB} entitlement acceptance; {PA} §11.16.4.3', C.TC[('ENT', n)]
        if m:
            return f'{PB} §11.16.5.12; {PA} §11.16.4.3', C.TC[(m.group(1)[:-5], 'POS')]
    if ('cost' in ch.lower()) and n:
        return f'{PA} §11.16.4.4; {PC} §11.16.5.16', ''
    if ('Technical' in ch) and n:
        return f'{PA} §11.16.4.5, §11.16.5.9–§11.16.5.11', ''
    if ('Crosswalk' in ch or 'capability mapping' in ch.lower()):
        return f'{PA} §11.16.4.6' + (f'; §11.16.5.6.{n}' if n else '; §11.16.5.1 foundation'), ''
    if ('Entitlement' in ch or 'entitlement' in ch) and n:
        return f'{PA} §11.16.4.1, §11.16.5.6.{n} Entitlements', C.TC[('ENT', n)]
    if ('Migration' in ch or 'migra' in ch) and n:
        return f'{PA} §11.16.4.1; §11.16.5.6.{n} Migration', 'FR-V12-N-008'
    if n:
        return f'{PA} §11.16.5.6.{n}', ', '.join(SP.S[n]['fr'])
    if 'WEB' in r['doc'] or 'website' in ch.lower() or 'html' in ch.lower() or 'route' in ch.lower() or 'items' in ch:
        return f'{PA} §11.16.5.5, §11.16.4.8–§11.16.4.9', 'W55–W76; FR-V12-N-011…018; AU-228'
    if 'Engine' in ch:
        return f'{PA} §11.16.4.7, §11.16.5.1', 'ADR-230'
    if 'Sources' in ch or 'decision' in ch.lower():
        return f'{PA} §11.16.1, §11.16.5.1; {PC} §11.16.7', 'DEC-800…819'
    return f'{PA} §11.16.5.1 (common investment platform); {PC} §11.16.7', 'DEC-800; FR-V12-N-001…010'

Lrows = [r for r in csv.DictReader(open(BP + '/final/coverage_v12/L_coverage.csv')) if 'CONFLICT-958' in ','.join(r.values())]
skipped_O = 0
for r in Lrows:
    p = primary(r)
    if p and p != 'ALL' and not C.mine(p):
        skipped_O += 1
        continue
    loc, ids = loc_for(r, p)
    add(r['doc'], r['chapter'], r['section'], r['aspect_id'], r['aspect_summary'], r['status_before'], loc,
        'Reconciled by Group N: CONFLICT-958 resolved by DEC-783; specified at full depth' + (f' for {p}' if p and p != 'ALL' else ' (common investment platform / website)'),
        ('DEC-783; ' + ids).strip('; '))

# ---------------- (2) own inventory
B0 = 'Not covered (CONFLICT-958; DEC-002 exclusion)'
CSVP = 'src/Investment_Automation_Master_Automation_Service_Catalog_2031_24_Services_96_Workflows(1)_csv/'
for n, r in sorted(C.SVC.items()):
    for f in C.SC_H:
        if not f:
            continue
        add('INV-CAT', 'Service_Catalog.csv', f'{CSVP}Service_Catalog.csv:r{r["_row"]}', f'N-SC-{n:02d}-{C.SC_H.index(f)+1:02d}', f'{C.svc_key(n)} · {f}: {r.get(f, "")}', B0,
            f'{PA} §11.16.5.6.{n} field "{f}"', 'Adopted literally; blueprint mapping added', ', '.join(SP.S[n]['fr']))
BOILER = {6, 26, 29, 37, 38, 40, 41, 43, 44, 45, 47, 48, 49}
seen_b = set()
for r in C.WFS:
    for i, f in enumerate(C.WC_H):
        if not f:
            continue
        if i in BOILER:
            key = (f, r.get(f))
            if key in seen_b:
                continue
            seen_b.add(key)
            add('INV-CAT', 'Workflow_Catalog.csv (boilerplate, listed once)', f'{CSVP}Workflow_Catalog.csv', f'N-WC-B{i+1:02d}-{len(seen_b):02d}', f'{f}: {r.get(f, "")}', B0,
                f'{PB} §11.16.5.12 (every workflow header); {PA} §11.16.5.1', 'Adopted as platform rule', 'FR-V12-N-001…010')
            continue
        add('INV-CAT', 'Workflow_Catalog.csv', f'{CSVP}Workflow_Catalog.csv:r{r["_row"]}', f'N-WC-{r["_key"]}-{i+1:02d}', f'{r["_code"]} · {f}: {r.get(f, "")}', B0,
            f'{PB} §11.16.5.12 {r["_code"]}', 'Adopted literally; DTO, steps, controls, SLA, KPI, tests added', C.FR_WF[r['_code']])
for tid, r in sorted(C.ATM.items()):
    n = C.svc_no(r['Service ID'])
    t = C.TC[('ENT', n)] if '-ENT-' in tid else C.TC[(tid[:-5], 'POS')]
    add('INV-CAT', 'Acceptance_Tests.csv', f'{CSVP}Acceptance_Tests.csv:r{r["_row"]}', f'N-AT-{tid}', f'{tid} · {r["Scenario"]} · {r["Expected output / behavior"]} · {r["Negative and boundary checks"]}', B0,
        f'{PB} test tables; {PA} §11.16.4.3', 'Mapped to executable TC with negative classes', t)
for code, r in sorted(C.CMM.items()):
    add('INV-CAT', 'Cost_Model.csv', f'{CSVP}Cost_Model.csv:r{r["_row"]}', f'N-CM-{code}', f'{code} · {r["Workflow"]} · {r["Input tokens (scenario)"]}/{r["Output tokens (scenario)"]} tokens · INR {r["Internal INR / invocation"]}', B0,
        f'{PA} §11.16.4.4; {PC} §11.16.5.16', 'Retained as illustrative; re-costed per agent', 'CR-V12-N-02')
for r in C.CM:
    if r.get('Planning assumption'):
        add('INV-CAT', 'Cost_Model.csv (rates)', f'{CSVP}Cost_Model.csv:r{r["_row"]}', f'N-CM-RATE-{r["_row"]}', f'{r["Planning assumption"]} = {r["INR / unit"]}', B0, f'{PA} §11.16.4.4', 'Retained as illustrative [GAP-1010]', 'GAP-1010')
for n, r in sorted(C.ERM.items()):
    for f in C.ER_H:
        if f:
            add('INV-CAT', 'Entitlement_Rules.csv', f'{CSVP}Entitlement_Rules.csv:r{r["_row"]}', f'N-ER-{n:02d}-{C.ER_H.index(f)+1:02d}', f'{C.svc_key(n)} · {f}: {r.get(f, "")}', B0,
                f'{PA} §11.16.5.6.{n} Entitlements; §11.16.4.1', 'Adopted; AU-200 enforces', C.TC[('ENT', n)])
for n, r in sorted(C.MGM.items()):
    add('INV-CAT', 'Migration.csv', f'{CSVP}Migration.csv:r{r["_row"]}', f'N-MG-{n:02d}', ' · '.join(f'{k}: {v}' for k, v in r.items() if not k.startswith('_')), B0, f'{PA} §11.16.4.1; §11.16.5.6.{n}', 'Adopted', 'FR-V12-N-008')
for n, r in sorted(C.SIM.items()):
    add('INV-CAT', 'Service_Index.csv', f'{CSVP}Service_Index.csv:r{r["_row"]}', f'N-SI-{n:02d}', ' · '.join(f'{k}: {v}' for k, v in r.items() if not k.startswith('_')), B0, f'{PA} §11.16.4.1', 'Adopted', 'FR-V12-N-009')
for n in range(1, 13):
    for j, r in enumerate(C.TMM[n], 1):
        add('INV-CAT', 'Technical_Map.csv', f'{CSVP}Technical_Map.csv:r{r["_row"]}', f'N-TM-{n:02d}-{j:02d}', f'{r["Service ID"]} · {r["Admin screen ID"]} {r["Existing admin screen title"]} · {r["Reuse decision"]}', B0,
            f'{PA} §11.16.4.5, §11.16.5.9', 'Screen re-identified; routes and entities adopted', f'{SP.A_OF.get(r["Admin screen ID"], "")}; DEC-801')
for r in C.CW:
    p = r['Primary service ID']
    if p == 'ALL' or C.mine(p):
        add('INV-CAT', 'Capability_Crosswalk.csv', f'{CSVP}Capability_Crosswalk.csv:r{r["_row"]}', f'N-CW-{r["Original capability ID"]}', f'{r["Original capability ID"]} {r["Original capability name"]} → {p} ({r["Commercial classification"]})', B0,
            f'{PA} §11.16.4.6' + ('; §11.16.5.1 foundation' if p == 'ALL' else f'; §11.16.5.6.{C.svc_no(p)}'), 'Mapped; no double billing', 'FR-V12-N-003' if p == 'ALL' else ', '.join(SP.S[C.svc_no(p)]['fr']))
for r in C.SE:
    add('INV-CAT', 'Shared_Engines.csv', f'{CSVP}Shared_Engines.csv:r{r["_row"]}', f'N-SE-{r["Engine ID"]}', f'{r["Engine ID"]} {r["Logical engine"]} · {r["Primary mapped services"]}', B0, f'{PA} §11.16.4.7', 'Mapped to platform engines', 'ADR-230')
for r in C.SD:
    add('INV-CAT', 'Sources_Decisions.csv', f'{CSVP}Sources_Decisions.csv:r{r["_row"]}', f'N-SD-{r["_row"]:02d}', ' · '.join(f'{k}: {v}' for k, v in r.items() if not k.startswith('_'))[:400], B0, f'{PA} §11.16.1, §11.16.5.1; {PC} §11.16.7', 'Adopted as constraint', 'DEC-800…819')
for i, r in enumerate(C.D['Start_Here'][2], 1):
    if any(c.strip() for c in r):
        add('INV-CAT', 'Start_Here.csv', f'{CSVP}Start_Here.csv:r{i}', f'N-SH-{i:02d}', ' | '.join(c for c in r if c), B0, f'{PA} §11.16.1, §11.16.4.1', 'Metrics reconciled', 'DEC-783')
for r in C.D['routes']:
    ws = next(s for s in SP.SCREENS_W if s[1] == r['id'])
    add('WEB-INV', 'investment_website_route_reconciliation.csv', 'route ' + r['id'], f'N-WR-{r["id"]}', ' · '.join(f'{k}: {v}' for k, v in r.items()), B0, f'{PA} §11.16.4.9, §11.16.5.5.2', 'Re-identified', ws[0] + '; DEC-801')
for it in C.D['layout']['items']:
    p = next((x['Primary service ID'] for x in C.CW if x['Original capability ID'] == it['id']), 'ALL')
    owner = 'N' if (p == 'ALL' or C.mine(p)) else 'O (catalogue rendering by N)'
    add('WEB-INV', 'investment_website_layout_catalog.json', f'$.items[{it["id"]}]', f'N-WL-{it["id"]}', f'{it["id"]} {it["name"]} · {it["family"]} · core={it["core"]} · primary {p} · {owner}', B0,
        f'{PA} §11.16.5.5.2 W56/W57', 'Rendered in neutral catalogue', 'FR-V12-N-017')
for g in C.D['layout']['groups']:
    add('WEB-INV', 'investment_website_layout_catalog.json', '$.groups', f'N-WG-{g["name"][:20].replace(" ", "_")}', f'{g["name"]} (core={g["core"]}): {g["desc"]}', B0, f'{PA} §11.16.5.5.2', 'Rendered', 'FR-V12-N-017')
for i, b in enumerate(C.BRANCHES, 1):
    add('WEB-SMA', 'commercial_website_desktop_V12.html', f'html-js inv branch B{i:02d} @{b["pos"]}', f'N-IB-{i:02d}', f'{b["expr"]} · ' + ' · '.join(b['strings'][:5]), 'Conflict (CONFLICT-868/958)',
        f'{PA} §11.16.4.8, §11.16.5.5.1', 'Investor-mode strings adopted literally (W74)', 'W74; FR-V12-N-011…013')
for i, para in enumerate([p for p in C.D['readme'].split('\n\n') if p.strip()], 1):
    for j, sent in enumerate([s.strip() for s in re.split(r'(?<=\.)\s+', para) if s.strip()], 1):
        add('WEB-INV', 'README.txt', f'para {i}', f'N-RM-{i:02d}-{j:02d}', sent, B0, f'{PA} §11.16.5.5', 'Adopted as website constraint', 'DEC-813; AU-228')
import json
vr = json.load(open(C.WEB + '/verification_report.json')) if hasattr(C, 'WEB') else None
from n_common import WEB
vr = json.load(open(WEB + '/verification_report.json'))
for k, v in vr['investment'].items():
    add('WEB-INV', 'verification_report.json', '$.investment', f'N-VR-{k}', f'{k} = {v}', B0, f'{PA} §11.16.5.5.2; {PC} PM-N-06', 'Adopted as acceptance check', 'FR-V12-N-017')

os.makedirs(os.path.dirname(OUT), exist_ok=True)
with open(OUT, 'w', newline='') as f:
    wr = csv.DictWriter(f, fieldnames=['doc', 'chapter', 'section', 'aspect_id', 'aspect_summary', 'status_before', 'blueprint_location', 'action', 'new_ids', 'status_after'])
    wr.writeheader()
    for r in rows:
        wr.writerow(r)
ids = [r['aspect_id'] for r in rows]
dup = [k for k, v in collections.Counter(ids).items() if v > 1]
print('rows', len(rows), 'L rows total', len(Lrows), 'to Group O', skipped_O, 'dups', len(dup), dup[:5])
