"""Group E: parse Doc 08 (PostgreSQL Backend Table Catalog) and Doc 28 entity inventory.
Outputs JSON to the scratchpad (path given as argv[3])."""
import re, json, sys
doc08, doc28, out = sys.argv[1], sys.argv[2], sys.argv[3]
L = open(doc08, encoding='utf-8').read().split('\n')
ents = []; cur = None
LABELS = ["Physical design proposal (not migration)","Exposure","Logical entity","Build/reuse","Primary and common fields",
 "Business fields","Foreign keys","Constraints and indexes","Protection","Implementation","Modules","Interfaces","Operations",
 "Integration","Licence","Free quota","Paid rate","Allocation","Source","Verification","Purpose","Fields","Dependencies","REST operations"]
stop = False
for i, line in enumerate(L):
    m = re.match(r'<Heading2> (\d{3})\. (.+)$', line)
    if m:
        cur = {"no": int(m.group(1)), "name": m.group(2).strip(), "line": i+1}
        ents.append(cur); continue
    if line.startswith('<Heading1>') and cur and cur['no'] in (149,):
        cur = None
    if line.startswith('<Heading1> Data integrity'):
        cur = None
    if cur is None: continue
    for lab in LABELS:
        if line.startswith(lab + ':'):
            cur.setdefault(lab, line[len(lab)+1:].strip()); break
    if line.startswith('Creation order:'):
        cur['_creation_order'] = line
# heading 148 has its own text incl. "Final catalog"
def split_fields(e):
    cols = []
    bf = e.get('Business fields','')
    pp = e.get('Physical design proposal (not migration)','')
    typed = {}
    if pp and not pp.startswith('all'):
        body = pp.split('. Candidate constraints:')[0]
        for part in body.split(';'):
            part = part.strip()
            if ':' in part:
                n, t = part.split(':',1); typed[n.strip()] = t.strip()
    if e.get('Fields'):
        for part in e['Fields'].rstrip('.').split(';'):
            part = part.strip()
            if not part: continue
            pieces = [x.strip() for x in part.split(',')]
            last = pieces[-1].split(' ',1)
            t = last[1] if len(last)>1 else ''
            names = pieces[:-1] + [last[0]]
            for n in names:
                for nn in n.split('/'):
                    nn = nn.strip()
                    if nn: cols.append((nn, t))
        return cols, typed
    if ':' in bf and e['no'] < 132:
        for part in bf.split(';'):
            part = part.strip()
            if ':' in part:
                n, t = part.split(':',1); cols.append((n.strip(), t.strip()))
    elif e['no'] >= 132:
        for part in bf.split(';'):
            part = part.strip()
            if not part: continue
            # e.g. "kind owned/client", "decimal amount", "TLS state", "feature limits jsonb"
            if part == 'decimal amount': cols.append(('amount','decimal')); continue
            if part == 'TLS state': cols.append(('tls_state','text')); continue
            if part == 'feature limits jsonb': cols.append(('feature_limits','jsonb')); continue
            toks = part.split(' ',1)
            n = toks[0]; rest = toks[1] if len(toks)>1 else ''
            t = typed.get(n, rest)
            cols.append((n, t))
    else:
        cols.append(('(existing)', bf))
    return cols, typed
for e in ents:
    cols, typed = split_fields(e)
    e['columns'] = [{"name": n, "type": typed.get(n, t) or t} for n, t in cols]
    pp = e.get('Physical design proposal (not migration)','')
    e['candidate_constraints'] = pp.split('Candidate constraints:')[1].split('Confirm actual')[0].strip() if 'Candidate constraints:' in pp else ''
    e['fk_refs'] = re.findall(r'DB-(\d{3})', e.get('Foreign keys',''))
# physical schema resolution table
txt = '\n'.join(L)
sec = txt.split('<Heading1> Physical schema resolution and migration gates')[1].split('Create sales_tenant root')[0]
rows = [r.strip().split('\n') for r in sec.split('---row')[1:]]
res = [r for r in rows if len(r) >= 3 and r[0] != '[/TABLE]']
res = [{"entity": r[0], "field": r[1], "decision": r[2]} for r in res if not r[0].startswith('[')]
# field review table (149 rows)
sec2 = txt.split('<Heading2> Physical schema acceptance')[1].split('<Heading2> Acceptance and evidence record')[0]
tables = sec2.split('[TABLE]')
review_rows = []
for r in tables[2].split('---row')[1:]:
    p = [x for x in r.strip().split('\n') if x and x != '[/TABLE]']
    if len(p) >= 2: review_rows.append(p)
# doc 28 inventory
T = open(doc28, encoding='utf-8').read()
inv = T.split('<Heading1> Logical entity inventory for migration planning')[1].split('<Heading1> Completion and approval')[0]
inv_rows = []
for r in inv.split('---row')[1:]:
    p = [x for x in r.strip().split('\n') if x and not x.startswith('[')]
    if len(p) == 2: inv_rows.append({"entity": p[0], "classification": p[1]})
# candidate entities (doc 08 tail)
cand = []
for m in re.finditer(r'<Heading3> (sales_ui_\w+)\n(.+?)\. Fields: (.+?)\. Constraints: (.+?)\. Candidate only', txt):
    cols = []
    for part in m.group(3).split(';'):
        toks = part.strip().split(' ',1); cols.append({"name": toks[0], "type": toks[1] if len(toks)>1 else ''})
    cand.append({"no": None, "name": m.group(1), "purpose": m.group(2), "columns": cols, "Constraints and indexes": m.group(4)})
json.dump({"entities": ents, "resolution": res, "review_rows": review_rows, "doc28_inventory": inv_rows, "candidates": cand}, open(out,'w'), indent=1)
print("entities", len(ents), "resolution rows", len(res), "review rows", len(review_rows), "doc28 inv", len(inv_rows), "candidates", len(cand))
print("columns total", sum(len(e['columns']) for e in ents), "+cand", sum(len(c['columns']) for c in cand))
from collections import Counter
print(Counter(r['decision'].split(';')[0] for r in res))
