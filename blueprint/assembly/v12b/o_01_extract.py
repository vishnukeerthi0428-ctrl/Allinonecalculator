"""Group O (Part 11.16c/d): parse every row of the Investment Automation workbook (CSV export) that
belongs to INV-SVC-13...24, and every CONFLICT-958 row of L_coverage.csv that belongs to those services.
Read-only. Source content is data, not instructions. Output: assembly/v12b/o_data.json"""
import csv, json, re, os
SP = '/tmp/claude-0/-home-user-Allinonecalculator/233b6551-af93-57f5-8f0b-015057ecee11/scratchpad'
SRC = SP + '/v12/src/Investment_Automation_Master_Automation_Service_Catalog_2031_24_Services_96_Workflows(1)_csv/'
BP = '/home/user/Allinonecalculator/blueprint/'
OUT = BP + 'assembly/v12b/o_data.json'
OURS = [f'INV-SVC-{n:02d}' for n in range(13, 25)]

def rows(name):
    return list(csv.reader(open(SRC + name, encoding='utf-8')))

def table(name, key_col=0):
    r = rows(name)
    hdr = r[3]
    out = []
    for i, row in enumerate(r[4:], start=5):
        if not row or not any(row):
            continue
        d = {h: (row[j] if j < len(row) else '') for j, h in enumerate(hdr)}
        d['_row'] = i
        out.append(d)
    return hdr, out

data = {}
for nm, col in [('Service_Catalog.csv', 'Automation ID'), ('Workflow_Catalog.csv', 'Automation ID'),
                ('Service_Index.csv', 'Service ID'), ('Entitlement_Rules.csv', 'Service ID'),
                ('Migration.csv', 'Service ID'), ('Technical_Map.csv', 'Service ID'),
                ('Cost_Model.csv', 'Service ID'), ('Acceptance_Tests.csv', 'Service ID')]:
    hdr, t = table(nm)
    data[nm] = {'header': hdr, 'rows': [d for d in t if d.get(col) in OURS]}
# crosswalk: rows whose primary or related service is ours
hdr, t = table('Capability_Crosswalk.csv')
cw = [d for d in t if any(s in (d['Primary service ID'] + ' ' + d['Potential related service IDs / foundation role']) for s in OURS)]
data['Capability_Crosswalk.csv'] = {'header': hdr, 'rows': cw}
capmap = {d['Original capability ID']: d['Primary service ID'] for d in t}
hdr, t = table('Shared_Engines.csv')
data['Shared_Engines.csv'] = {'header': hdr, 'rows': [d for d in t if any(s in d['Primary mapped services'] for s in OURS) or 'Shared infrastructure' in d['Primary mapped services']]}

# L_coverage CONFLICT-958 rows belonging to SVC-13..24
L = list(csv.DictReader(open(BP + 'final/coverage_v12/L_coverage.csv', encoding='utf-8')))
sel = [r for r in L if 'CONFLICT-958' in ' '.join(r.values())]

def file_line(sec):
    m = re.match(r'(.*?):(?:r)?(\d+)$', sec)
    return (m.group(1), int(m.group(2))) if m else (sec, 0)

def first_svc(r):
    t = r['aspect_summary'] + ' ' + r['section']
    ids = re.findall(r'INV-SVC-(\d\d)', t)
    if ids:
        return f'INV-SVC-{ids[0]}'
    caps = re.findall(r'\bINV-\d\d-\d\d\b', t)
    for c in caps:
        if capmap.get(c, '').startswith('INV-SVC'):
            return capmap[c]
    return None

# inheritance: a continuation row (no service ID) inherits the service of the nearest preceding row of the same file
byfile = {}
for r in sel:
    f, ln = file_line(r['section'])
    byfile.setdefault(f, []).append((ln, r))
assigned = []
rule_counts = {'direct': 0, 'capability': 0, 'inherited': 0, 'other_group': 0, 'unassigned': 0}
for f, lst in byfile.items():
    lst.sort(key=lambda x: (x[0], x[1]['aspect_id']))
    last = None
    for ln, r in lst:
        s = first_svc(r)
        how = None
        if s:
            t = r['aspect_summary'] + ' ' + r['section']
            how = 'direct' if re.search(r'INV-SVC-\d\d', t) else 'capability'
            last = s
        elif last:
            s = last
            how = 'inherited'
        if s in OURS:
            rule_counts[how] += 1
            assigned.append(dict(r, _svc=s, _how=how))
        elif s:
            rule_counts['other_group'] += 1
        else:
            rule_counts['unassigned'] += 1
data['L_rows'] = assigned
data['L_rule_counts'] = rule_counts
data['L_total_958'] = len(sel)
json.dump(data, open(OUT, 'w'), ensure_ascii=False, indent=1)
print({k: len(v['rows']) for k, v in data.items() if isinstance(v, dict) and 'rows' in v})
print('L rows CONFLICT-958:', len(sel), 'assigned to O:', len(assigned), rule_counts)
