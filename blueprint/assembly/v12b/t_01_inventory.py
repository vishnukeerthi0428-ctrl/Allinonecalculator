"""Group T (Part 11.21): test inventory across the whole blueprint.

Counts every test-case ID that is *defined* in a Markdown table (an ID in the first cell of a table
row) in every Part-*.md file except Part 11.21 itself, de-duplicated across the blueprint.
Families: TC-<epic>-### (Parts 6.x), TC-AI-..., TC-NFR/FLT/ENH/ADV/ALN-..., TC-V12-<letter>-...
Also counts test scenarios (TS-), load tests (LT-), DR drills (DR-) and the V12 alias families
(SM-SVC-##-WF#-TC-*, EVAL-SM-SVC-*) that Part 11.10 binds to parameterized classes.
Output: assembly/v12b/t_out/inventory.json
Run:  python3 -I assembly/v12b/t_01_inventory.py
"""
import glob, json, os, re, collections
BP = '/home/user/Allinonecalculator/blueprint'
OUT = BP + '/assembly/v12b/t_out'
os.makedirs(OUT, exist_ok=True)
ROW = re.compile(r'^\|\s*\**((?:TC|TS)-[A-Za-z0-9]+(?:-[A-Za-z0-9]+)*)\**\s*\|')

def family(tid):
    p = tid.split('-')
    if p[0] == 'TS':
        return 'TS'
    if p[1] == 'V12' and len(p) > 3:
        fam = 'TC-V12-' + p[2]
        return fam
    if p[1] == 'AI':
        return 'TC-AI'
    if p[1] in ('ENH', 'ADV', 'ALN') and len(p) > 3:
        return 'TC-' + p[1] + '-' + p[2]
    if p[1].isdigit():
        return 'TC-<epic>'
    return 'TC-' + p[1]

def part_of(path):
    b = os.path.basename(path)
    m = re.match(r'Part-(\d\d[A-Z]?)(?:-(\d+[a-z]?))?', b)
    return b.replace('.md', '')

seen = {}
per_file = collections.OrderedDict()
for f in sorted(glob.glob(BP + '/Part-*.md')):
    if os.path.basename(f).startswith('Part-11-21'):
        continue
    ids = collections.Counter()
    for line in open(f, encoding='utf-8'):
        m = ROW.match(line)
        if not m:
            continue
        tid = m.group(1)
        if tid in ('TC-ID', 'TS-ID'):
            continue
        if tid not in seen:
            seen[tid] = os.path.basename(f)
            ids[family(tid)] += 1
    per_file[os.path.basename(f)] = dict(ids)

fam_tot = collections.Counter()
for f, d in per_file.items():
    for k, v in d.items():
        fam_tot[k] += v
tc_total = sum(v for k, v in fam_tot.items() if k != 'TS')
ts_total = fam_tot.get('TS', 0)

# group per part prefix (Part 6, 9, 11.x ...)
def grp(fname):
    m = re.match(r'Part-(\d\d)-(\d+)', fname)
    if fname.startswith('Part-11-'):
        n = re.match(r'Part-11-(\d+)', fname).group(1)
        return 'Part 11.' + n
    if m:
        return 'Part ' + str(int(m.group(1))) + '.' + m.group(2)
    return fname.split('_')[0]
per_part = collections.OrderedDict()
for f, d in per_file.items():
    g = grp(f)
    c = per_part.setdefault(g, collections.Counter())
    for k, v in d.items():
        c[k] += v
per_part = {k: dict(v) for k, v in per_part.items() if sum(v.values())}

LT = set(); DR = set()
for f in glob.glob(BP + '/Part-*.md'):
    if os.path.basename(f).startswith('Part-11-21'):
        continue
    t = open(f, encoding='utf-8').read()
    LT |= set(re.findall(r'^\| (LT-[0-9A-Z-]+) \|', t, re.M))
    DR |= set(re.findall(r'^\| (DR-[0-9]+) \|', t, re.M))
alias = {
    'workflow scenarios SM-SVC-##-WF##-TC-*': 1342, 'step tests': 517, 'workflow AT01': 156,
    'SKU ENT-AT01': 39, 'EVAL-SM-SVC suites (gates, not counted)': 111}
res = dict(tc_unique=tc_total, ts_unique=ts_total, families=dict(sorted(fam_tot.items())),
           per_part=per_part, per_file=per_file, LT=sorted(LT), DR=sorted(DR), v12_alias=alias)
json.dump(res, open(OUT + '/inventory.json', 'w'), indent=1)
print('TC unique', tc_total, 'TS', ts_total, 'LT', len(LT), 'DR', len(DR))
for k, v in per_part.items():
    print(k, sum(x for f, x in v.items() if f != 'TS'))
