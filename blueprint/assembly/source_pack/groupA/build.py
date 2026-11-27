"""Build group A outputs: coverage CSV, generated Markdown fragments and the assembled Part 2.6 file."""
import collections, csv, difflib, pathlib, re, sys
HERE = pathlib.Path(__file__).resolve().parent
BP = HERE.parents[2]
SRC = pathlib.Path(sys.argv[1])
sys.path.insert(0, str(HERE))
from register import R
GEN = HERE / 'gen'; GEN.mkdir(exist_ok=True)
docname = {'03':'03 End User Personas','11':'11 Global Market Intelligence & Opportunity Discovery','12':'12 Digital Marketing & Customer Acquisition Automation',
           '13':'13 Sales Intelligence & Commercial Conversion','14':'14 Global Customer, Partner & Account Acquisition Strategy','37':'37 Sales & Marketing Automation Illustrative Workflow'}
# ---- uniqueness
ids = [r[2] for r in R]; dup = [k for k,v in collections.Counter(ids).items() if v>1]
assert not dup, dup
# ---- CSV
out = BP/'final'/'coverage'/'A_coverage.csv'
with open(out,'w',newline='',encoding='utf-8') as f:
    w = csv.writer(f); w.writerow(['doc','section','aspect_id','aspect_summary','status','blueprint_location','action','new_ids'])
    for r in R: w.writerow(r)
# ---- summary
ST = ['Covered','Partially covered','Not covered','Conflict','Not applicable']
cnt = collections.defaultdict(collections.Counter)
for r in R: cnt[r[0]][r[4]] += 1
order = ['ALL (01-37 common core)','03','11','12','13','14','37']
lines = ['| Document | Covered | Partially covered | Not covered | Conflict | Not applicable | Total aspects |','|---|---|---|---|---|---|---|']
tot = collections.Counter()
for d in order:
    c = cnt[d]; tot.update(c)
    lines.append(f"| {docname.get(d,'Common core (shared by all 38 documents)')} | " + ' | '.join(str(c[s]) for s in ST) + f" | {sum(c.values())} |")
lines.append('| **Total** | ' + ' | '.join(f'**{tot[s]}**' for s in ST) + f' | **{sum(tot.values())}** |')
(GEN/'summary.md').write_text('\n'.join(lines)+'\n')
# ---- detailed register
def esc(s): return s.replace('|','/')
det = []
for d in order:
    title = docname.get(d,'Common core (shared by all 38 documents; reported once)')
    det.append(f'\n#### Document {title}\n')
    det.append('| Aspect ID | Section | Aspect | Status | Blueprint location | Action / new IDs |'); det.append('|---|---|---|---|---|---|')
    for r in R:
        if r[0]!=d: continue
        act = r[6] + (f' → {r[7]}' if r[7] else '')
        st = r[4] if r[4]=='Covered' else f'**{r[4]}**'
        det.append(f'| {r[2]} | {esc(r[1])} | {esc(r[3])} | {st} | {esc(r[5])} | {esc(act)} |')
(GEN/'detailed.md').write_text('\n'.join(det)+'\n')
# ---- API and entity reconciliation (document 13 capability cards)
api_txt = (BP/'Part-03-2_API_and_Integration.md').read_text(encoding='utf-8')
dm_txt = (BP/'Part-03-3_Data_Architecture.md').read_text(encoding='utf-8')
d13 = next(SRC.glob('13_*.txt')).read_text(encoding='utf-8')
ops = re.findall(r'REST API / runtime interface: (.*)', d13)
oprows = []; found = 0; n = 0
for line in ops:
    for op in [o.strip() for o in line.split(';')]:
        meth, path = op.split(' ',1); n += 1
        pat = re.compile(r'\|\s*(API-\d+)[^|]*\|\s*' + meth + r'\s*\|\s*`[^`]*' + re.escape(path) + r'`')
        m = pat.search(api_txt)
        apid = m.group(1) if m else '—'
        found += bool(m)
        oprows.append(f'| {meth} {path} | {apid} | {"Covered" if m else "Not found"} |')
ents = sorted(set(e.strip() for l in re.findall(r'Database entities: (.*)', d13) for e in l.split(',')))
entrows = []; ef = 0
for e in ents:
    k = len(re.findall(r'\b'+e+r'\b', dm_txt)); ef += k>0
    entrows.append(f'| {e} | {k} | {"Covered" if k else "Not found"} |')
(GEN/'recon_api.md').write_text(f'**Result: {found}/{n} operations and {ef}/{len(ents)} entities found.**\n\n| Source operation (doc 13) | Part 3.2 ID | Status |\n|---|---|---|\n' + '\n'.join(oprows) +
    '\n\n| Source entity (doc 13) | Mentions in Part 3.3 | Status |\n|---|---|---|\n' + '\n'.join(entrows) + '\n')
# ---- screen ID reconciliation
ui = (BP/'Part-02-5_UX_UI_Design.md').read_text(encoding='utf-8')
inv = set(re.findall(r'^\| ([AW]\d{2,3}) \|', ui, re.M))
def expand(t):
    res=set()
    for a_,b_ in re.findall(r'\b([AW]\d{2,3})[–-]([AW]?\d{2,3})\b', t):
        p=a_[0]; s=int(a_[1:]); e=int(b_.lstrip('AW'));
        for i in range(s,e+1): res.add(f'{p}{i:03d}' if p=='A' else f'{p}{i:02d}')
    res |= set(re.findall(r'\b([AW]\d{2,3})\b', t))
    return {x for x in res if (x[0]=='A' and len(x)==4) or (x[0]=='W' and len(x)==3)}
srows=[]
for nn in ['03','11','12','13','14','37']:
    t = next(SRC.glob(nn+'_*.txt')).read_text(encoding='utf-8')
    ids_ = expand(t)
    miss = sorted(ids_-inv)
    srows.append(f'| {docname[nn]} | {len(ids_)} | {len(ids_&inv)} | {", ".join(miss) if miss else "none"} |')
(GEN/'recon_screens.md').write_text(f'Part 2.5 inventory rows parsed: **{len(inv)}** screen IDs.\n\n| Document | Screen IDs referenced (ranges expanded) | Found in Part 2.5 | Missing |\n|---|---|---|---|\n'+'\n'.join(srows)+'\n')
# ---- duplicate-section verification for doc 14
d11 = next(SRC.glob('11_*.txt')).read_text(encoding='utf-8').splitlines()
d12 = next(SRC.glob('12_*.txt')).read_text(encoding='utf-8').splitlines()
d14 = next(SRC.glob('14_*.txt')).read_text(encoding='utf-8').splitlines()
r1 = d11[36:318]==d14[55:337]; r2 = d12[36:239]==d14[337:540]
(GEN/'recon_dup.md').write_text(f'| Check | Lines compared | Result |\n|---|---|---|\n| Document 14 lines 56–337 vs document 11 lines 37–318 | {318-36} | {"Identical" if r1 else "Differs"} |\n| Document 14 lines 338–540 vs document 12 lines 37–239 | {239-36} | {"Identical" if r2 else "Differs"} |\n')
# ---- assemble
parts = sorted((HERE/'frag').glob('*.md'))
txt = ''
for p in parts:
    s = p.read_text(encoding='utf-8')
    for g in GEN.glob('*.md'):
        s = s.replace('{{'+g.stem+'}}', g.read_text(encoding='utf-8'))
    txt += s.rstrip()+'\n\n'
left = re.findall(r'\{\{\w+\}\}', txt)
assert not left, left
(BP/'Part-02-6_Source_Pack_Business_Domain_Enhancements.md').write_text(txt, encoding='utf-8')
print('aspects', len(R), dict(tot)); print('api', found, n, 'ent', ef, len(ents)); print('dup', r1, r2)
