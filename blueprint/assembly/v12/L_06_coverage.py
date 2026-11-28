"""Write final/coverage_v12/L_coverage.csv and OUT/stats.json for Part 11.12.

Rows (columns doc,chapter,section,aspect_id,aspect_summary,status_before,blueprint_location,action,new_ids,status_after):
  L-S-*   summary rows per material group and band (MATCH / PARTIAL / RESIDUAL, requirement-like or not)
  L-P-*   PARTIAL requirement-like units grouped by family with the register rule that governs them
  L-F-*   RESIDUAL families (one per family) with class counts
  L-A-*   class (a) aspects enhanced in Part 11.12 (one row each, with new IDs)
  L-C-*   conflicts and configuration-management findings
  L-U*    every RESIDUAL requirement-like unit individually (read and classified)
"""
import csv, json, os, re, sys, collections
sys.path.insert(0, os.path.dirname(__file__))
from L_common import *
from L_05_classify import classify

COV = BP + '/final/coverage_v12'
os.makedirs(COV, exist_ok=True)
SECT = 'Part 11.12'


def family(u):  # same as L_04_cluster.family
    s, h, f = u['src'], u['heading'], u['file']
    if s in ('ANX-BRD', 'ANX-FSD', 'V1-BRD', 'V1-FSD'):
        h2 = re.sub(r'\b[A-Z][A-Z0-9]{0,9}(?:-[A-Z0-9]{1,12}){1,5}\b', '<ID>', h)
        m = re.search(r'\.xlsx / (.*)', h2)
        if m:
            return f'{s[:3]}::' + h2[:m.start()] + '.xlsx/' + m.group(1).strip().replace(' ', '_')
        return f'{s[:3]}::{h2[:70]}'
    return f'{s}::{os.path.basename(f)}'


units_n = collections.Counter()
for l in open(OUT + '/units.jsonl'):
    units_n[json.loads(l)['src']] += 1
comp = [json.loads(l) for l in open(OUT + '/compared.jsonl')]
cls = [json.loads(l) for l in open(OUT + '/classified.jsonl')]

stats = dict(units=units_n, unique=collections.Counter(), req=collections.Counter(), band=collections.Counter(),
             ref_hit=collections.Counter(), cls=collections.Counter(), rule=collections.Counter(), partial_rule=collections.Counter())
for u in comp:
    s = u['src']
    stats['unique'][s] += 1
    if u['req']:
        stats['req'][s] += 1
    stats['band'][f"{s}|{'R' if u['req'] else 'N'}|{u['band']}"] += 1
    if u['req'] and u['band'] != 'RESIDUAL':
        for r, k in (('R1', 'c1'), ('R2', 'c2'), ('R3', 'c3')):
            if u[k] >= 0.8:
                stats['ref_hit'][r] += 1
for u in cls:
    stats['cls'][f"{u['src']}|{u['cls']}"] += 1
    stats['rule'][f"{u['rule']}|{u['cls']}"] += 1

rows = []


def row(doc, chapter, section, aid, summ, sb, loc, action, new, sa):
    rows.append([doc, chapter, section, aid, re.sub(r'\s+', ' ', summ)[:400], sb, loc, action, new, sa])


# L-S summary rows
for k in sorted(stats['band']):
    s, rq, b = k.split('|')
    n = stats['band'][k]
    sb = {'MATCH': 'Covered', 'PARTIAL': 'Partially covered', 'RESIDUAL': 'Not covered'}[b]
    sa = {'MATCH': 'Matched', 'PARTIAL': 'Matched (residual wording/value deltas governed by V12; DEC-V9-02)',
          'RESIDUAL': 'See L-F / L-U rows (classes a/b/c/m)'}[b]
    row(s, 'all files of group', 'band summary', f'L-S-{s}-{rq}-{b}',
        f"{n} unique {'requirement-like' if rq == 'R' else 'non-requirement'} units in band {b} (6-gram shingle and field-value coverage vs 38 docs + V12 normative + blueprint)",
        sb, 'R1 docs38 + final/coverage; R2 V12 BRD/FSD (non-ZZ); R3 blueprint Part-0*.md', 'Counted (L_03_compare.py)', '', sa)

# L-P partial families
pf = collections.defaultdict(collections.Counter)
for u in comp:
    if u['band'] == 'PARTIAL' and u['req']:
        u['family'] = family(u)
        h = classify(u)
        key = (u['family'], h[0] if h else 'unruled', h[1] if h else '-', h[3] if h else '')
        pf[key]['n'] += 1
        stats['partial_rule'][f"{key[1]}|{key[2]}"] += 1
for i, (k, c) in enumerate(sorted(pf.items(), key=lambda x: -x[1]['n']), 1):
    fam, rule, cl, cite = k
    row(fam.split('::')[0], fam.split('::', 1)[-1], 'PARTIAL family', f'L-P-{i:04d}',
        f"{c['n']} requirement-like units 40-80% present in references; governing register rule {rule}",
        'Partially covered', cite or 'see family', f'Register rule {rule} (class {cl}); differences are fixture/DTO/status deltas', '',
        'Matched (V12 governs; DEC-V9-02)' if cl in ('b', 'm', 'a') else ('Pending Founder decision (CONFLICT-958)' if rule in ('R-INV', 'M:C-INV') else 'Not applicable (not a requirement)'))

# L-F residual families
ff = collections.defaultdict(lambda: dict(n=0, cls=collections.Counter(), rule=collections.Counter(), cite='', sample=''))
for u in cls:
    f = ff[u['family']]
    f['n'] += 1
    f['cls'][u['cls']] += 1
    f['rule'][u['rule']] += 1
    f['cite'] = f['cite'] or u['cite']
    f['sample'] = f['sample'] or u['text'][:160]


def status_after(c, rule, cite):
    if rule in ('R-INV', 'M:C-INV'):
        return 'Pending Founder decision (CONFLICT-958)'
    if c == 'a':
        return 'Matched (enhanced in Part 11.12)'
    if c == 'm':
        return 'Matched (blueprint, semantic)'
    if c == 'b':
        return 'Not applicable (superseded by V12)'
    return 'Not applicable (not a requirement / out of scope)'


for i, (fam, f) in enumerate(sorted(ff.items(), key=lambda x: -x[1]['n']), 1):
    top = f['rule'].most_common(1)[0][0]
    c = f['cls'].most_common(1)[0][0]
    row(fam.split('::')[0], fam.split('::', 1)[-1], 'RESIDUAL family', f'L-F-{i:04d}',
        f"{f['n']} residual units; classes {dict(f['cls'])}; rules {dict(f['rule'])}; e.g. {f['sample']}",
        'Not covered (residual)', f['cite'], f'Read and classified ({top})', '', status_after(c, top, f['cite']))

# L-A class (a) aspects
A = []
G = [('G01', 'Admin workspace scope'), ('G02', 'Public/portal scope'), ('G03', 'Contextual filters'), ('G04', 'Capability filters'),
     ('G05', 'Omnichannel policy'), ('G06', 'Workflow operations'), ('G07', 'Record linkage'), ('G08', 'AI evidence'), ('G09', 'Financial controls'),
     ('G10', 'Approval and audit'), ('G11', 'Data lifecycle'), ('G12', 'UX and navigation'), ('G13', 'UI states'), ('G14', 'Simulation safeguards'),
     ('G15', 'Service lifecycle')]
for n, (g, t) in enumerate(G, 1):
    A.append(('Others/147_Screen_Field_csv/Global_fields.csv', 'Global fields', g, f'Cross-screen field-family rule {g} {t}', '§11.12.5.1', f'FR-V12-L-{n:03d}; TC-V12-L-{n:03d}'))
for n in range(1, 6):
    A.append(('Others/Expanded_Master_Workbook_csv/02_Business_Requirements.csv', 'UI expansion BR', f'UX-BR-0{n}', f'UI-expansion business requirement UX-BR-0{n} (stricter non-production acceptance)', '§11.12.5.2', f'FR-V12-L-{15 + n:03d}; TC-V12-L-{15 + n:03d}'))
TS = ['T01', 'T02', 'T03', 'T04', 'T05', 'T06', 'T07', 'T08', 'T09', 'T10', 'T11', 'T12', 'T13', 'T14', 'T15', 'T18', 'T19', 'T20', 'T21', 'T22', 'T23', 'T24', 'T25']
for n, t in enumerate(TS, 21):
    A.append(('Others/147_Screen_Field_csv/Acceptance.csv', 'Prototype acceptance', t, f'Configuration-scale acceptance scenario {t}', '§11.12.5.3', f'TC-V12-L-{n:03d}'))
for n in range(1, 29):
    A.append(('engineering/provider_benchmark_plan.csv', 'Provider benchmark plan', f'BENCH-{n:03d}', f'Provider benchmark plan BENCH-{n:03d}', '§11.12.5.4', 'FR-V12-L-021…026; TC-V12-L-044…049'))
for n, (aid, s) in enumerate([('CM-01', 'Annex precedence: V1/annex text non-normative; never cited as authority'), ('CM-02', 'Embedded archive SHA-256 verification control'),
                              ('CM-03', 'ID namespace qualification for colliding families (DEC, REC, KPI, AI, WF, R)'), ('CM-04', 'Embedded pack version-drift detection')], 27):
    A.append(('archive / annex (all)', 'Configuration management', aid, s, '§11.12.5.5', f'FR-V12-L-{n:03d}; TC-V12-L-{n + 23:03d}'))
for i, (doc, ch, sec, summ, where, new) in enumerate(A, 1):
    row(doc, ch, sec, f'L-A-{i:03d}', summ, 'Not covered', f'{SECT} {where}', 'Enhanced at full depth', new, 'Matched')

# L-C conflicts / CM findings
C = [('CONFLICT-958', 'Investment Automation sibling product (24 services / 96 workflows / 19-route website) and investor/fundraising objective mode in the commercial prototype vs DEC-002 (no investor discovery or fundraising)', 'Pending Founder decision'),
     ('CONFLICT-959', 'ID namespace collisions between V1/engineering, V12 and blueprint (DEC-001…180 vs DEC-001…; REC-01…30 vs REC-01…09; KPI-01…35 vs KPI-01…31; AI-01…18 (V1) vs AI-01… (V12); WF-01/02 vs WF-01…14; R-001…006)', 'Matched (DEC-722 qualification rule)'),
     ('CONFLICT-960', 'Historical effort/cost envelope 287–483 PD, task register 385/499 PD, INR 1.0–1.5 lakh per resource-month vs approved DEC-228/DEC-230', 'Matched (blueprint approved figures retained; V12 REC-12)'),
     ('GAP-961', 'Prototype acceptance list skips T16 and T17 (numbering gap in 147 Screen Field workbook)', 'Matched (recorded; no scenario invented)'),
     ('GAP-962', 'CURRENT_PACKAGE_SHA256.json lists html/* files whose hashes do not match the decoded neutral-website pack (5 mismatches, 7 absent); two engineering manifests refer to prior packages not in the archive', 'Matched (FR-V12-L-030 drift control)')]
for i, (cid, s, sa) in enumerate(C, 1):
    row('archive (all)', 'Conflicts and findings', cid, f'L-C-{i:02d}', s, 'Conflict' if cid.startswith('CONFLICT') else 'Not covered', f'{SECT} §11.12.6', 'Raised with proposed resolution', cid, sa)

# L-U every residual unit
for u in sorted(cls, key=lambda x: x['uid']):
    new = ''
    if u['cls'] == 'a':
        new = {'M:A-G': 'FR-V12-L-001…015', 'M:A-UXBR': 'FR-V12-L-016…020', 'M:A-T': 'TC-V12-L-021…043', 'M:A-BENCH': 'FR-V12-L-021…026'}.get(u['rule'], '')
    elif u['rule'] in ('R-INV', 'M:C-INV'):
        new = 'CONFLICT-958'
    row(u['src'], u['heading'][:120] or u['family'], u['loc'], u['uid'], u['text'],
        f"Not covered (residual; cf={u['cf']})", u['cite'] if u['cls'] in ('b', 'm', 'c') else f'{SECT} §11.12.5',
        f"Class {u['cls']} ({u['rule']}): {u['reason']}", new, status_after(u['cls'], u['rule'], u['cite']))

with open(COV + '/L_coverage.csv', 'w', newline='', encoding='utf-8') as f:
    w = csv.writer(f)
    w.writerow(['doc', 'chapter', 'section', 'aspect_id', 'aspect_summary', 'status_before', 'blueprint_location', 'action', 'new_ids', 'status_after'])
    w.writerows(rows)
stats['rows'] = collections.Counter(r[3][:4] for r in rows)
stats['status_after'] = collections.Counter(r[9].split(' (')[0] for r in rows if r[3].startswith('L-U'))
stats['partial_families'] = len(pf)
stats['residual_families'] = len(ff)
json.dump(stats, open(OUT + '/stats.json', 'w'), indent=1)
print('rows', len(rows), dict(stats['rows']))
print('status_after (units)', dict(stats['status_after']))
print('partial rules', stats['partial_rule'].most_common(12))
