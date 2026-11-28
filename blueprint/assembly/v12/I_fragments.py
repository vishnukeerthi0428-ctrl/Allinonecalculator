"""Group I: generate Markdown fragments (registers) for Part 11.9 from I_coverage.csv and the C3 catalogue."""
import csv, collections, subprocess, re, json
BP = '/home/user/Allinonecalculator/blueprint'; D = BP + '/assembly/v12/i_ddl'
rows = list(csv.DictReader(open(BP + '/final/coverage_v12/I_coverage.csv', encoding='utf-8')))
def esc(s): return s.replace('|', '\\|').replace('\n', ' ')
out = {}
# ---- 11.9.2 summary table
grp = collections.OrderedDict()
def gkey(r):
    if r['chapter'] in ('Appendix C', 'Appendix C2', 'Appendix C/C2'): return f"{r['chapter']} · {r['section']}"
    if r['doc'].startswith('V12 src'): return f"src/engineering · {r['section']}"
    sec = r['section']
    if sec.startswith('Domain schema'): sec = 'Domain schemas (39 services)'
    return f"ch{r['chapter']} · {sec}"
for r in rows:
    k = gkey(r); grp.setdefault(k, collections.Counter())
    grp[k][r['status_before']] += 1; grp[k]['after:' + r['status_after']] += 1; grp[k]['n'] += 1
lines = ['| Aspect group | Aspects | Covered | Partially covered | Not covered | Conflict | After: Matched | After: Pending Founder |', '|---|---|---|---|---|---|---|---|']
tot = collections.Counter()
for k, c in grp.items():
    lines.append(f"| {esc(k)} | {c['n']} | {c['Covered']} | {c['Partially covered']} | {c['Not covered']} | {c['Conflict']} | {c['after:Matched']} | {c['after:Pending Founder decision']} |")
    tot.update(c)
lines.append(f"| **Total** | **{tot['n']}** | **{tot['Covered']}** | **{tot['Partially covered']}** | **{tot['Not covered']}** | **{tot['Conflict']}** | **{tot['after:Matched']}** | **{tot['after:Pending Founder decision']}** |")
out['summary'] = '\n'.join(lines)
# ---- 11.9.3 detailed register: non-covered aspects listed individually (compact by group)
reg = []
# (a) prose/requirement aspects individually
for r in rows:
    if r['status_before'] == 'Covered': continue
    if r['section'] in ('Column', 'Constraint', 'RLS policy', 'Table') or r['section'].startswith('Domain schema'): continue
    reg.append(f"| {esc(r['aspect_id'])} | {esc(r['aspect_summary'][:170])} | {r['status_before']} | {esc(r['blueprint_location'][:90])} | {esc(r['action'][:150])} | {esc(r['new_ids'])} | {r['status_after']} |")
out['register_req'] = '| Aspect | Summary (V12) | Before | Blueprint location | Enhancement | New IDs | After |\n|---|---|---|---|---|---|---|\n' + '\n'.join(reg)
# (b) DDL tables: per table, list non-covered columns, partial constraints, policies
bytab = collections.OrderedDict()
for r in rows:
    if r['section'] not in ('Column', 'Constraint', 'RLS policy', 'Table'): continue
    if r['section'] == 'Table':
        t = r['aspect_id'].replace('I-DDL-TBL-', ''); bytab.setdefault(t, {'tbl': r, 'cols': [], 'con': [], 'pol': []}); continue
    if r['section'] == 'Column':
        t, c = r['aspect_id'].replace('I-DDL-COL-', '').split('.', 1)
        if r['status_before'] != 'Covered': bytab[t]['cols'].append(c + ('' if r['status_before'] == 'Not covered' else '°'))
    elif r['section'] == 'Constraint':
        t = r['aspect_summary'].split(' ', 2)[1].rstrip(':')
        if r['status_before'] != 'Covered': bytab.setdefault(t, {'tbl': None, 'cols': [], 'con': [], 'pol': []})['con'].append(r['aspect_id'].replace('I-DDL-CON-', ''))
    else:
        t = r['aspect_summary'].split(' ON ')[1].split(' ')[0]
        bytab[t]['pol'].append(r['aspect_id'].replace('I-DDL-POL-', ''))
lines = ['| V12 table | Blueprint target | Table status | Columns not covered (° = partial) | Constraints strengthened | Policies replaced |', '|---|---|---|---|---|---|']
for t, v in bytab.items():
    tr = v['tbl']
    lines.append(f"| `{t}` | {esc(tr['blueprint_location'])} | {tr['status_before']} | {', '.join(v['cols']) or '—'} | {', '.join(v['con']) or '—'} | {', '.join(v['pol']) or '—'} |")
out['register_ddl'] = '\n'.join(lines)
# (c) domain-schema fields partially covered: per service list
ds = collections.OrderedDict()
for r in rows:
    if r['section'].startswith('Domain schema'):
        k = r['section'].replace('Domain schema ', '')
        ds.setdefault(k, [[], []])[0 if r['status_before'] == 'Covered' else 1].append(r['aspect_id'].split('-', 5)[-1] if False else r['aspect_summary'].split(':')[0].split('.', 1)[1])
lines = ['| Domain schema (service) | Fields with a typed blueprint column (Covered) | Fields carried in validated payload (Partially covered → Matched by DEC-661) |', '|---|---|---|']
for k, (a, b) in ds.items():
    lines.append(f"| {esc(k)} | {', '.join(a) or '—'} | {', '.join(b) or '—'} |")
out['register_ds'] = '\n'.join(lines)
# ---- 11.9.4 mapping: domain tables with workflows
sql = open(D + '/appendix_c.sql').read()
wf = {m.group(1): [w.strip() for w in m.group(2).split(',') if w.strip()] for m in re.finditer(r"CREATE TABLE (growth_\w+|sales_\w+) \(.*?\);\s*--\s*([^\n]*)", sql, re.S)}
emap = {r['src_table']: r for r in csv.DictReader(open(BP + '/final/coverage/E_table_mapping.csv', encoding='utf-8'))}
lines = ['| # | V12 domain table | Blueprint ENT | Blueprint table | Scope / Imm. | Workflows cited in Appendix C (first 10 as printed) |', '|---|---|---|---|---|---|']
for i, (t, w) in enumerate(wf.items(), 1):
    m = emap[t]
    trunc = ' (list truncated in source)' if len(w) == 10 else ''
    lines.append(f"| {i} | `{t}` | {m['bp_ent']} | `{m['bp_table']}` | {m['bp_scope']} / {m['bp_imm']} | {', '.join(x.replace('SM-SVC-', '') for x in w)}{trunc} |")
out['map_domain'] = '\n'.join(lines)
# ---- policy and index registers
pol = list(csv.DictReader(open(D + '/c3_policy_register.csv')))
c = collections.Counter(p['template'] for p in pol)
lines = ['| Template | Tables | Table list |', '|---|---|---|']
by = collections.defaultdict(list)
for p in pol: by[p['template']].append(p['table'])
for k, v in by.items(): lines.append(f"| {esc(k)} | {len(v)} | {', '.join('`'+x+'`' for x in v)} |")
out['policy_register'] = '\n'.join(lines)
idx = list(csv.DictReader(open(D + '/c3_index_register.csv')))
byp = collections.defaultdict(list)
for x in idx: byp[x['purpose']].append(x)
lines = ['| Purpose | Count | Indexes (name: table (definition)) |', '|---|---|---|']
for k, v in byp.items():
    if k == 'FK support (IX-R1)':
        lines.append(f"| {k} | {len(v)} | " + '; '.join(f"`{x['table']}`({x['definition']})" for x in v) + ' |')
    elif k in ('V5 common physical design', 'registry lookup'):
        lines.append(f"| {k} | {len(v)} | one per V12 domain table: `ix_<table>__" + ('scope_status_upd` (tenant_id, company_id, status, updated_at DESC)' if k.startswith('V5') else 'schema_ref` (tenant_id, company_id, schema_ref)') + ' |')
    else:
        lines.append(f"| {esc(k)} | {len(v)} | " + '; '.join(f"`{x['index']}`: {x['table']} ({esc(x['definition'])})" for x in v) + ' |')
out['index_register'] = '\n'.join(lines)
json.dump(out, open(D + '/fragments.json', 'w'), indent=0)
for k, v in out.items(): print(k, len(v), v.count('\n'))
