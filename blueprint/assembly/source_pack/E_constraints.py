"""Group E: constraint/index-level reconciliation (Doc 08 'Constraints and indexes' + candidate constraints) vs Part 3.3.
usage: python3 -I E_constraints.py <doc08.json> <part33.json> <columns.csv> <out_csv>"""
import json, sys, csv, re, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from E_mapping import M
d = json.load(open(sys.argv[1])); bp = json.load(open(sys.argv[2]))
colmap = {}
for r in csv.DictReader(open(sys.argv[3])):
    colmap[(r['src_table'], r['column'])] = r['bp_column'] or r['column']
rows = []
def bpcol(t, c):
    v = colmap.get((t, c), c)
    return v.split(' ')[0].split('/')[0].strip() if v else c
for e in d['entities'] + d['candidates']:
    key = e['no'] if e['no'] is not None else e['name']
    prim = M[key][0]; b = bp.get(prim, {})
    text = (b.get('text','') + ' ' + ' '.join(b.get('sec8', []))).lower()
    imm = b.get('imm', '')
    atoms = [a.strip() for a in re.split(r';\s*', e.get('Constraints and indexes') or '') if a.strip() and a.strip() != 'None']
    atoms += ['[candidate] ' + a.strip() for a in re.split(r';\s*', e.get('candidate_constraints','').rstrip('.')) if a.strip()]
    for a in atoms:
        al = a.lower()
        st, loc, act = '', '', ''
        m = re.search(r'(unique|index)\(([^)]+)\)', al)
        if m:
            kind, cols = m.group(1), [c.strip() for c in m.group(2).split(',')]
            mapped = [bpcol(e['name'], c) for c in cols]
            present = all(mc.lower() in text for mc in mapped)
            has_uq = ('unique' in text or 'uq' in text)
            if kind == 'unique':
                if present and has_uq:
                    st, loc, act = 'Covered (scoped)', f"{prim} {b.get('table','')} UQ on {', '.join(mapped)} scoped by tenant/startup", 'Blueprint key is tenant/startup-scoped; source key is global (CONFLICT-384 resolution: keep scoped)'
                else:
                    st, loc, act = 'Gap', f"{prim} {b.get('table','')}", f"Add UQ ({', '.join(['tenant_id','startup_id'] + mapped)}) in Part 3.6 index/constraint catalogue"
            else:
                st, loc, act = ('Covered' if any(mapped[0] in l.lower() for l in b.get('sec8', [])) else 'Gap'), f"{prim} {b.get('table','')}", f"Index ({', '.join(['tenant_id','startup_id'] + mapped)}) listed in Part 3.6 IX catalogue"
        elif 'append-only' in al or 'immutable' in al:
            st, loc, act = ('Covered' if imm in ('A','F','V') else 'Partial'), f"{prim} Imm.={imm} (Part 3.3 §3.3.5.9)", 'Immutability trigger profile'
        elif a.startswith('[candidate]'):
            if 'sales_tenant' in al or 'sales_startup' in al or 'unique(tenant_id,id)' in al:
                st, loc, act = 'Covered', 'Part 3.3 §3.3.5.3 composite scope FK; STD-S/T', 'sales_tenant/sales_startup = ten_tenant/ten_startup'
            elif 'allowed values' in al:
                st, loc, act = 'Covered (values reconciled)', f"{prim} CHECK (Part 3.3 CK-22)", 'Value mapping in Part 3.6 §3.6.4.6'
            elif '> 0' in al:
                st, loc, act = 'Covered', 'CK-01', ''
            elif 'unique' in al:
                st, loc, act = ('Covered (scoped)' if 'unique' in text or 'uq' in text else 'Gap'), f"{prim}", ''
            else:
                st, loc, act = 'Covered (process)', 'Part 3.6 §3.6.4.3 schema decision register', 'Approve source-described constraints'
        else:
            st, loc, act = 'Covered (rule)', f"{prim} {b.get('table','')} + BRL/CK/PDP", 'Service/PDP rule; DB enforcement listed in Part 3.6 where feasible'
        rows.append(dict(src_no=key, src_table=e['name'], constraint=a, status=st, blueprint=loc, action=act))
with open(sys.argv[4], 'w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
from collections import Counter
print(len(rows), Counter(r['status'] for r in rows))
for r in rows:
    if r['status'] in ('Gap','Partial'): print(r['src_no'], r['src_table'], '|', r['constraint'], '|', r['action'])
