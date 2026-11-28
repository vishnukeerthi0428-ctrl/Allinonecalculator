"""Group R: assemble Part-11-19a/b/c from fragments and generated material."""
import csv, json, collections, re
BP = '/home/user/Allinonecalculator/blueprint'
F = BP + '/assembly/v12b/R_frag/'
rows = list(csv.DictReader(open(BP + '/final/coverage_v12/R_coverage.csv', encoding='utf-8')))
summ = json.load(open(BP + '/assembly/v12b/R_inventory_summary.json'))
combo = json.load(open(BP + '/assembly/v12b/R_combinatorics_summary.json'))
ex = json.load(open(F + 'examples.json'))
TOP = {'IDN': 'Identity: SSO, SCIM, MFA, roles, SoD', 'API': 'Developer API, keys, SDK, portal, sandbox', 'WHK': 'Webhooks',
       'CON': 'Connectors, CRM, SMS-DLT, voice', 'REG': 'Region, residency, hosting', 'DR': 'Recovery: RPO, RTO, WAL, PITR, drills',
       'MDL': 'Model registry and routing', 'BEN': 'Cross-tenant data and benchmarks', 'DBA': 'Database access, roles, RLS'}
def esc(s): return s.replace('|', '/').replace('\n', ' ')

# material table
by_file = collections.OrderedDict()
for r in rows:
    k = (r['doc'], r['chapter'])
    by_file.setdefault(k, [0, 0, collections.Counter()])
    by_file[k][0] += 1
    by_file[k][2][r['aspect_id'].split('-')[1]] += 1
    if r['new_ids'] != '—': by_file[k][1] += 1
inv = ['| # | Document · chapter | Aspects | Core aspects | Topics (count) |', '|---|---|---|---|---|']
for i, ((d, ch), (n, c, t)) in enumerate(by_file.items(), 1):
    inv.append(f'| {i} | {d} ch {ch} | {n} | {c} | ' + ', '.join(f'{k} {v}' for k, v in t.most_common()) + ' |')
inv.append(f"| | **Total** ({summ['lines_read']:,} lines read in {summ['files']} chapters with matches; {summ['duplicates_merged']} repeated statements merged) | **{len(rows)}** | **{sum(1 for r in rows if r['new_ids']!='—')}** | |")
INV = '\n'.join(inv)

# coverage summary
cov = ['| Topic | Aspects | Core | Covered before | Partially covered before | Conflict before | Matched after | Pending Founder after | Not applicable after |', '|---|---|---|---|---|---|---|---|---|']
tot = collections.Counter()
for k, name in TOP.items():
    rs = [r for r in rows if r['aspect_id'].split('-')[1] == k]
    c = collections.Counter(r['status_before'] for r in rs)
    core = sum(1 for r in rs if r['new_ids'] != '—')
    cov.append(f"| {k} {name} | {len(rs)} | {core} | {c['Covered']} | {c['Partially covered']} | {c['Conflict']} | {len(rs)} | 0 | 0 |")
    tot.update({'n': len(rs), 'core': core, 'cov': c['Covered'], 'part': c['Partially covered'], 'con': c['Conflict']})
cov.append(f"| **Total** | **{tot['n']}** | **{tot['core']}** | **{tot['cov']}** | **{tot['part']}** | **{tot['con']}** | **{tot['n']} (100%)** | **0** | **0** |")
COV = '\n'.join(cov)

reg = ['| Aspect ID | Source | V12 statement (literal, trimmed) | Before | Owner before / reason | Resolved by (Part 11.19) | After |', '|---|---|---|---|---|---|---|']
for r in rows:
    if r['status_before'] in ('Conflict', 'Partially covered'):
        loc = r['blueprint_location'].split('; Part 11.19 ')
        m = re.search(r'\((.*)\)$', r['action'])
        reason = m.group(1) if m else ''
        reg.append(f"| {r['aspect_id']} | {r['doc']} ch {r['chapter']} · {esc(r['section'][:50])} | {esc(r['aspect_summary'][:220])} | {r['status_before']} | {esc(loc[0])}; {esc(reason)} | {esc(loc[1] if len(loc)>1 else '')} · {r['new_ids']} | Matched |")
REG = '\n'.join(reg)
pend = sum(1 for r in rows if r['status_before'] == 'Conflict')

grp = ['| Topic | Covered aspects | Of which core | Earlier owner | Why no change was needed |', '|---|---|---|---|---|']
why = {'WHK': 'Workflow steps that receive or emit webhooks; the platform webhook contract (§11.19.5.2) applies unchanged',
       'CON': 'Workflow-level CRM/channel mentions; connector contract and gate (§11.19.5.3) apply',
       'IDN': 'Role and MFA mentions inside workflows and screens; identity design applies',
       'MDL': 'Workflow-level AI step mentions; routing through the registry applies',
       'DR': 'Error-handling and retry statements already specified in Part 11.5b §11.5.5.7',
       'REG': 'Locale/region statements already specified; residency routing applies',
       'API': 'Operation mentions already in the contract (Part 11.8a/b)',
       'BEN': 'Isolation tests and statements already covered by RLS suites',
       'DBA': 'DDL statements already reconciled in Part 11.9a/b'}
for k, name in TOP.items():
    rs = [r for r in rows if r['aspect_id'].split('-')[1] == k and r['status_before'] == 'Covered']
    core = sum(1 for r in rs if r['new_ids'] != '—')
    owner = rs[0]['blueprint_location'].split('; Part 11.19')[0] if rs else '—'
    grp.append(f'| {k} {name} | {len(rs)} | {core} | {esc(owner)} | {why[k]} |')
GRP = '\n'.join(grp)

cs = ['| Model | Capability | Parameters (values) | Raw product | Valid | Method | t-tuples | Cases | Pairwise-only size | TC range |', '|---|---|---|---|---|---|---|---|---|---|']
tc_total = 0
for mid, s in combo.items():
    if mid.startswith('_'): continue
    cs.append(f"| {mid} | {s['cap']} | {s['params']} ({s['values']}) | {s['raw']:,} | {s['valid']:,} | {s['method']} | {s['tuples'] if s['method']!='exhaustive' else '—'} | {s['cases']} | {s['pairwise_cases'] or '—'} | {s['first_tc']}…{s['last_tc']} |")
    tc_total += s['cases']
cs.append(f'| **Total** | | | | | | | **{tc_total}** | | TC-V12-R-101…{combo["_last_tc"][-4:].lstrip("-")} |')
CS = '\n'.join(cs)

subs = {'{{INV_TABLE}}': INV, '{{COV_SUMMARY}}': COV, '{{REGISTER}}': REG, '{{REGISTER_GROUPED}}': GRP,
        '{{PENDING_N}}': str(pend), '{{FR}}': open(F + 'fr.md').read(), '{{COMBO_SUMMARY}}': CS,
        '{{MODELS}}': open(F + 'models.md').read(), '{{TC_GEN}}': open(F + 'tc_generated.md').read(),
        '{{ASPECTS}}': f'{len(rows):,}', '{{TOTAL_TC}}': f'{86 + tc_total:,}', '{{GEN_TC}}': f'{tc_total:,}',
        '{{LAST_TC_NUM}}': combo['_last_tc'].split('-')[-1]}
for mid, block in ex.items():
    subs['{{EX:' + mid + '}}'] = block
parts = {'a': ['a_head.md', 'a_c1.md', 'a_c2.md', 'a_c3.md', 'a_c4.md'],
         'b': ['b_c5c6.md', 'b_c7c8.md', 'b_rest.md'],
         'c': ['c_stories1.md', 'c_stories2.md', 'c_tests1.md', 'c_end.md']}
names = {'a': 'Part-11-19a_Platform_Decisions_Identity_Developer_Platform_Connectors_Vercel.md',
         'b': 'Part-11-19b_Platform_Decisions_RPO_Model_Registry_Benchmarks_Supabase_Access.md',
         'c': 'Part-11-19c_Platform_Decisions_Stories_Combinatorial_Tests_Decisions.md'}
for p, fr in parts.items():
    txt = ''.join(open(F + f).read() for f in fr)
    for k, v in subs.items():
        txt = txt.replace(k, v)
    left = re.findall(r'\{\{[A-Z_:0-9]+\}\}', txt)
    assert not left, (p, left)
    open(BP + '/' + names[p], 'w', encoding='utf-8').write(txt)
    print(names[p], len(txt))
print('pending before', pend, 'aspects', len(rows), 'tc', 86 + tc_total)
