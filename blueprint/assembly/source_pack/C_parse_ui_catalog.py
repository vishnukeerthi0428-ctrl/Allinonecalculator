"""Group C: parse Doc 06 (UI Screen Filter API and Table Catalog) and Doc 17 (Command Centre UI/UX)
and reconcile every screen's fields, filters, actions, APIs, tables and test associations against the
blueprint (Parts 2.1, 2.5, 3.2, 3.3, 6.x).

Usage:  python3 -I C_parse_ui_catalog.py <docs38_dir> <blueprint_dir> <out_dir>
Outputs (in out_dir): c_screens.json, c_recon_summary.json, c_fields.csv, c_ops.csv, c_tables.csv,
c_tests.csv, c_plugins.csv, c_related.csv
"""
import re, json, sys, csv, os, collections

D, BP, OUT = sys.argv[1], sys.argv[2], sys.argv[3]
os.makedirs(OUT, exist_ok=True)
F06 = os.path.join(D, '06_UI_Screen_Filter_API_and_Table_Catalog.txt')
F17 = os.path.join(D, '17_Unified_Sales_and_Marketing_Command_Centre_UI_UX_and_Interaction_Design.txt')
F02 = os.path.join(D, '02_Functional_Specification.txt')
L06 = open(F06, encoding='utf-8').read().split('\n')
L17 = open(F17, encoding='utf-8').read().split('\n')
L02 = open(F02, encoding='utf-8').read().split('\n')

def find(lines, prefix, start=0):
    for i in range(start, len(lines)):
        if lines[i].startswith(prefix):
            return i
    return -1

SID = re.compile(r'^<Heading[23]> ([WA]\d{2,3}) — (.+?)(?: \(existing (\d{3})\))?$')
CAP = re.compile(r'^<Heading3> Existing capability (\d{3}) — ')

# ---------------------------------------------------------------- doc 06 part A/B blocks
def parse_blocks(lines, start, stop):
    blocks, cur = collections.OrderedDict(), None
    for i in range(start, stop):
        ln = lines[i]
        m = SID.match(ln); c = CAP.match(ln)
        if m and ln.startswith('<Heading2>'):
            cur = {'id': m.group(1), 'name': m.group(2), 'legacy': m.group(3), 'line': i + 1}
            blocks[m.group(1)] = cur; continue
        if c:
            cur = {'id': 'CAP' + c.group(1), 'name': 'Existing capability ' + c.group(1), 'line': i + 1}
            blocks[cur['id']] = cur; continue
        if ln.startswith('<Heading'):
            if not ln.startswith('<Heading3> Existing'):
                cur = None if ln.startswith('<Heading1>') or ln.startswith('<Heading2>') else cur
            continue
        if cur is None:
            continue
        if ':' in ln[:40]:
            k, v = ln.split(':', 1)
            cur.setdefault(k.strip(), v.strip())
        else:
            cur.setdefault('_desc', ln.strip())
    return blocks

a_start = find(L06, '<Heading1> Part A')
op_contract = find(L06, '<Heading1> Website and confidential Admin operating contract')
blocks06 = parse_blocks(L06, a_start, op_contract)

# ---------------------------------------------------------------- implementation controls table (doc 06)
impl_start = find(L06, '<Heading1> Implementation, verification and delivery controls')
t0 = find(L06, '[TABLE]', impl_start); t1 = find(L06, '[/TABLE]', t0)
rows, cur = [], []
for ln in L06[t0 + 1:t1]:
    if ln == '---row':
        if cur: rows.append(cur)
        cur = []
    else:
        cur.append(ln)
if cur: rows.append(cur)
impl = collections.OrderedDict()
for r in rows[1:]:
    if len(r) < 3: continue
    m = re.match(r'([WA]\d{2,3}) (.+?)(Public / Portal|Public|Portal|Admin|Authentication)$', r[0])
    if not m: continue
    sid = m.group(1)
    fr = re.findall(r'SM-FR-[WA]\d{2,3}', r[1])
    traces = re.sub(r'Unit:.*', '', r[1])
    traces = re.sub(r'SM-FR-[WA]\d{2,3}', '', traces).strip(' ;')
    impl[sid] = {'access': m.group(3), 'sm_fr': fr, 'trace': traces,
                 'unit': re.findall(r'SM-UT-\d{3}', r[1]), 'uat': re.findall(r'SM-UAT-S\d{3}', r[1]),
                 'checks': r[2]}

# ---------------------------------------------------------------- field decisions (doc 06, 17, 02)
def parse_decisions(lines):
    s = find(lines, '<Heading2> Screen-specific field and automation decisions')
    out, cur = collections.OrderedDict(), None
    for i in range(s + 1, len(lines)):
        ln = lines[i]
        m = SID.match(ln)
        if m and ln.startswith('<Heading3>'):
            cur = {'id': m.group(1), 'name': m.group(2)}; out[m.group(1)] = cur; continue
        if ln.startswith('<Heading'):
            break
        if cur is None: continue
        if ln.startswith('Current declared fields:'):
            m2 = re.match(r'Current declared fields: (.*?)\. Add or standardize: (.*?)\. Remove / replace: (.*)$', ln)
            cur['current'], cur['add'], cur['remove'] = m2.group(1), m2.group(2), m2.group(3)
        elif ln.startswith('Automation:'):
            parts = [p.strip() for p in ln.split('|')]
            for p in parts:
                k, v = p.split(':', 1)
                cur[k.strip().lower()] = v.strip().rstrip('.')
        elif ln.startswith('REST:'):
            rest, ent = ln[5:].split('| Entities:')
            cur['rest'] = rest.strip(); cur['entities'] = ent.strip().rstrip('.')
    return out

dec06, dec17, dec02 = parse_decisions(L06), parse_decisions(L17), parse_decisions(L02)

def strip_rest(d):
    return {k: {kk: vv for kk, vv in v.items() if kk not in ('rest', 'entities')} for k, v in d.items()}
diff_06_02 = [k for k in dec06 if strip_rest(dec06).get(k) != strip_rest(dec02).get(k)]
diff_06_17 = [k for k in dec06 if strip_rest(dec06).get(k) != strip_rest(dec17).get(k)]

# ---------------------------------------------------------------- doc 17 interaction blocks
a17 = find(L17, '<Heading1> Part A'); c17 = find(L17, '<Heading1> Website and confidential Admin operating contract')
blocks17 = parse_blocks(L17, a17, c17)
interaction_patterns = collections.Counter(b.get('Interaction', '(none: new-interface block)') for b in blocks17.values())

# ---------------------------------------------------------------- blueprint text
def rd(name):
    return open(os.path.join(BP, name), encoding='utf-8').read()
P21, P25, P32, P33 = (rd('Part-02-1_Functional_Design_Modules_and_FR_Register.md'), rd('Part-02-5_UX_UI_Design.md'),
                     rd('Part-03-2_API_and_Integration.md'), rd('Part-03-3_Data_Architecture.md'))
P6 = ''.join(rd(f) for f in sorted(os.listdir(BP)) if f.startswith('Part-06') and f.endswith('.md'))

def row_for(text, key):
    for ln in text.split('\n'):
        if ln.startswith('| ' + key + ' |'):
            return ln
    return ''

def norm(s):
    s = s.lower().replace('&', 'and')
    s = re.sub(r'\(.*?\)', ' ', s)
    return re.sub(r'[^a-z0-9 ]', ' ', s)

STOP = {'and', 'or', 'the', 'of', 'a', 'id', 'to', 'by', 'for', 'per', 'in', 'on'}
SYN = {'organisation': 'organization', 'fulfilment': 'fulfillment', 'catalogue': 'catalog', 'enrolment': 'enrollment',
       'programme': 'program', 'colour': 'color'}
def toks(s):
    out = set()
    for t in norm(s).split():
        t = SYN.get(t, t)
        if t in STOP: continue
        if t.endswith('s') and len(t) > 3: t = t[:-1]
        out.add(t)
    return out

def field_covered(field, text):
    ft = toks(field)
    if not ft: return True
    tt = toks(text)
    return len(ft & tt) / len(ft) >= 0.5

# ---------------------------------------------------------------- field reconciliation
field_rows = []
for sid, d in dec06.items():
    fr_row = row_for(P21, 'FR-' + sid)
    ux_row = row_for(P25, sid)
    text = fr_row + ' ' + ux_row
    seen = set()
    for kind in ('current', 'add'):
        for f in [x.strip() for x in d.get(kind, '').split(';') if x.strip()]:
            if f.lower() in seen: continue
            seen.add(f.lower())
            if f.startswith('Contextual'):
                st = 'Not applicable'
            else:
                st = 'Covered' if field_covered(f, text) else 'Partially covered'
            field_rows.append({'screen': sid, 'kind': kind, 'field': f, 'status': st,
                               'fr_in_bp': bool(fr_row), 'ux_in_bp': bool(ux_row)})
    rem = d.get('remove', '')
    if rem and rem not in ('No catalog field removed.', 'No catalog field removed', 'New layout.', 'New layout'):
        st = 'Covered' if field_covered(rem.split(':')[0], text) else 'Partially covered'
        field_rows.append({'screen': sid, 'kind': 'remove/replace', 'field': rem.rstrip('.'), 'status': st,
                           'fr_in_bp': bool(fr_row), 'ux_in_bp': bool(ux_row)})

# ---------------------------------------------------------------- API reconciliation
OPRE = re.compile(r'\b(GET|POST|PATCH|PUT|DELETE)\s+(/[^\s;\]|]+)')
bp_ops = []
for ln in P32.split('\n'):
    m = re.match(r'\| (API-\d{3})(?: ★)? \| ([A-Z/]+) \| `([^`]+)` \| ([^|]*)\| ([^|]*)\| ([^|]*)\|', ln)
    if m:
        p = m.group(3).replace('~/', '/api/v1/commercial/')
        bp_ops.append({'id': m.group(1), 'method': m.group(2).strip(), 'path': p, 'ns': m.group(4).strip(),
                       'purpose': m.group(5).strip(), 'fr': m.group(6).strip(), 'star': '★' in ln})

def pnorm(p):
    p = re.sub(r'\{[^}]+\}', '{}', p.rstrip('/'))
    if not p.startswith('/api/'):
        p = '/api/v1' + p
    return p

bp_index = collections.defaultdict(list)
for o in bp_ops:
    for meth in o['method'].split('/'):
        bp_index[(meth, pnorm(o['path']))].append(o['id'])
bp_path_only = collections.defaultdict(list)
for o in bp_ops:
    bp_path_only[pnorm(o['path'])].append(o['id'])

def last_resource(p):
    segs = [s for s in pnorm(p).split('/') if s and s != '{}' and s not in ('api', 'v1')]
    return segs[-1] if segs else ''

def resource_equiv(sid, meth, path):
    """Same screen + same method + same final resource noun in the blueprint catalogue."""
    res = last_resource(path)
    res_alt = {res, res.rstrip('s'), res + 's', res.replace('-', '_')}
    cands = []
    for o in bp_ops:
        if sid not in o['fr'] and ('FR-' + sid) not in o['fr']:
            continue
        if meth not in o['method'].split('/'):
            continue
        if last_resource(o['path']) in res_alt or any(r in o['path'] for r in res_alt if len(r) > 3):
            cands.append(o['id'])
    return cands

op_rows = []
def add_ops(sid, src, text):
    for meth, path in OPRE.findall(text or ''):
        path = path.rstrip('.')
        key = (meth, pnorm(path))
        if key in bp_index:
            st, ids, how = 'Covered', bp_index[key], 'exact'
        elif pnorm(path) in bp_path_only:
            st, ids, how = 'Partially covered', bp_path_only[pnorm(path)], 'path match, method differs'
        else:
            eq = resource_equiv(sid, meth, path)
            if eq:
                st, ids, how = 'Partially covered', eq, 'resource-equivalent DERIVED path on same screen'
            else:
                res = last_resource(path)
                alts = {res, res.rstrip('s'), res + 's'}
                eq2 = [o['id'] for o in bp_ops if meth in o['method'].split('/') and last_resource(o['path']) in alts
                       and (res not in ('control', 'approve', 'review', 'resolve', 'complete', 'pause', 'resume'))]
                if eq2:
                    st, ids, how = 'Partially covered', eq2, 'resource-equivalent path elsewhere in catalogue'
                else:
                    st, ids, how = 'Not covered', [], 'no exact or equivalent operation'
        op_rows.append({'screen': sid, 'source': src, 'method': meth, 'path': path, 'status': st,
                        'bp_ops': ';'.join(ids[:4]), 'match': how})

for sid, b in blocks06.items():
    add_ops(sid, 'doc06 block', b.get('REST operations') or b.get('REST/adapter operations') or b.get('Original service associations'))
for sid, d in dec06.items():
    if sid not in blocks06:
        add_ops(sid, 'doc06 decisions', d.get('rest'))
# Optimization Intelligence integration points
oi = find(L06, '<Heading2> Optimization Intelligence')
for ln in L06[oi + 1: oi + 10]:
    if ': GET' in ln or ': POST' in ln:
        add_ops('OPT-INT', 'doc06 optimization intelligence', ln.split('Persistence')[0])

# dedupe (screen, method, path)
seen, op_rows_u = set(), []
for r in op_rows:
    k = (r['screen'], r['method'], r['path'])
    if k in seen: continue
    seen.add(k); op_rows_u.append(r)
op_rows = op_rows_u
distinct_ops = {}
for r in op_rows:
    distinct_ops.setdefault((r['method'], r['path']), r)

# ---------------------------------------------------------------- table reconciliation
bp_ents = []
for ln in P33.split('\n'):
    m = re.match(r'\| (ENT-\d{3}) \| ([^|]+)\| `([a-z_]+)` \|', ln)
    if m:
        bp_ents.append({'id': m.group(1), 'name': m.group(2).strip(), 'table': m.group(3)})
suffix = {}
for e in bp_ents:
    suffix.setdefault(e['table'].split('_', 1)[1], e)
MANUAL = {  # source table -> blueprint table (judged synonyms)
    'growth_product': 'cat_offering', 'growth_document_chunk': 'cat_chunk', 'growth_api_usage': 'ai_usage',
    'growth_org_alias': 'intel_alias', 'growth_org_location': 'intel_location', 'growth_solution_match': 'intel_match',
    'growth_content_version': 'mkt_content_version', 'growth_ad_spend_event': 'mkt_spend_event',
    'growth_event_registration': 'mkt_registration', 'growth_event_attendance': 'mkt_attendance',
    'growth_business_event': 'ops_domain_event', 'growth_workflow_execution': 'aut_run', 'growth_subscription': 'lcy_customer_subscription',
    'growth_website_publication': 'mkt_publication', 'growth_feedback': 'lcy_feedback', 'growth_deal_outcome': 'lcy_outcome',
    'sales_tenant': 'ten_tenant', 'sales_startup': 'ten_startup', 'sales_membership': 'ten_membership',
    'sales_brand_domain': 'ten_domain', 'sales_external_access_grant': 'ten_portal_grant',
    'sales_support_grant': 'saas_support_access_grant', 'sales_business_template': None,
    'sales_service_plan': 'saas_plan', 'sales_service_subscription': 'saas_subscription',
    'sales_service_invoice': 'saas_service_invoice', 'sales_usage_charge': 'saas_usage_meter_reading',
    'sales_data_transfer': 'saas_export_job', 'sales_action_plan': 'aut_autonomy_plan', 'sales_bid': 'com_bid',
    'sales_order': 'com_order', 'sales_order_line': 'com_order_line', 'sales_fulfillment': 'com_fulfillment_event',
    'sales_ui_application': 'saas_application_draft', 'sales_ui_config_revision': 'aut_config_revision',
    'sales_ui_trigger_revision': 'aut_trigger', 'sales_ui_template_revision': 'aut_workflow_template',
    'sales_ui_conflict': 'aut_conflict_case', 'sales_ui_service_request': None,
    'growth_quota': 'int_quota', 'growth_eligibility_decision': 'gov_eligibility_decision',
    'growth_score_version': 'intel_score_version', 'growth_capability': 'cat_capability', 'growth_embedding': 'cat_embedding',
    'growth_document': 'cat_document', 'growth_claim': 'cat_claim', 'growth_price_version': 'cat_price_version',
    'growth_launch_approval': 'cat_launch_approval', 'existing user table': 'ten_user',
    'existing role table': 'ten_role', 'existing membership table': 'ten_membership',
    'growth_message_template': 'eng_message_template',
}
by_table = {e['table']: e for e in bp_ents}
TABRE = re.compile(r'\b(?:growth|sales)_[a-z_]+|existing (?:user|role|membership) table')
src_tables = collections.OrderedDict()
for sid, b in list(blocks06.items()):
    for t in TABRE.findall((b.get('PostgreSQL tables') or '') + ';' + (b.get('PostgreSQL entities (server-side only)') or '') + ';' + (b.get('PostgreSQL entities') or '')):
        src_tables.setdefault(t, set()).add(sid)
for sid, d in dec06.items():
    for t in TABRE.findall(d.get('entities', '')):
        src_tables.setdefault(t, set()).add(sid)
for ln in L06[oi + 1: oi + 10]:
    for t in TABRE.findall(ln):
        src_tables.setdefault(t, set()).add('OPT-INT')
tab_rows = []
for t, sids in src_tables.items():
    if t in MANUAL:
        bt = MANUAL[t]; how = 'judged synonym' if bt else 'no blueprint entity'
    else:
        sfx = t.split('_', 1)[1]
        e = suffix.get(sfx)
        bt = e['table'] if e else None; how = 'suffix match' if e else 'no blueprint entity'
    ent = by_table.get(bt) if bt else None
    st = 'Covered' if ent and how == 'suffix match' else ('Partially covered' if ent else 'Not covered')
    tab_rows.append({'source_table': t, 'screens': ';'.join(sorted(sids)), 'bp_table': bt or '',
                     'bp_ent': ent['id'] if ent else '', 'status': st, 'match': how})

# ---------------------------------------------------------------- test alias reconciliation
test_rows = []
uat_seq = []
for sid, r in impl.items():
    uat_seq.append((sid, r['uat']))
    for u in r['uat']:
        test_rows.append({'screen': sid, 'alias': u, 'kind': 'UAT', 'in_bp': u in P6 or u in rd('Part-06-6_Requirements_Traceability_Matrix.md')})
    for u in r['unit']:
        test_rows.append({'screen': sid, 'alias': u, 'kind': 'Unit', 'in_bp': u in P6})
# verify S-number rule S001-S030 = W01-W30, S031-S138 = A001-A108
rule_ok = all((sid.startswith('W') and u == ['SM-UAT-S%03d' % int(sid[1:])]) or
              (sid.startswith('A') and u == ['SM-UAT-S%03d' % (30 + int(sid[1:]))]) for sid, u in uat_seq)
ut_fr_count = collections.Counter(u for r in impl.values() for u in set(r['unit']))
ux_uat_missing = [sid for sid in dec06 if ('SM-UX-UAT-' + sid) not in (P21 + P6)]
ux_fr_missing = [sid for sid in dec06 if ('SM-UX-FR-' + sid) not in P21]

# ---------------------------------------------------------------- plugin / integration associations
plug_rows = []
for sid, b in blocks06.items():
    integ = b.get('Integration')
    if not integ: continue
    names = [x.strip() for x in integ.split(',')]
    for n in names:
        if n.lower().startswith('internal'):
            st = 'Covered'; loc = 'Internal React/Django (Part 3.1)'
        else:
            st = 'Covered' if re.search(re.escape(n), P32 + rd('Part-03-1_Architecture.md'), re.I) else 'Not covered'
            loc = 'Part 3.1/3.2' if st == 'Covered' else ''
        plug_rows.append({'screen': sid, 'integration': n, 'licence_note': (b.get('Licence') or '')[:160],
                          'status': st, 'bp_location': loc, 'build_reuse': b.get('Build/reuse', ''),
                          'admin_location': b.get('Admin role / location', '')})

# ---------------------------------------------------------------- related-screen graph
rel_rows = []
for sid, d in dec06.items():
    for r in [x.strip() for x in d.get('related', '').split(';') if x.strip()]:
        rel_rows.append({'from': sid, 'to': r, 'in_p25_row': r in row_for(P25, sid)})

# ---------------------------------------------------------------- screen coverage
screens = []
for sid in dec06:
    screens.append({'id': sid, 'name': dec06[sid]['name'], 'in_p21': bool(row_for(P21, 'FR-' + sid)),
                    'in_p25': bool(row_for(P25, sid)), 'legacy': (blocks06.get(sid) or {}).get('legacy'),
                    'access': (impl.get(sid) or {}).get('access') or (blocks06.get(sid) or {}).get('Access', ''),
                    'build': (blocks06.get(sid) or {}).get('Build/reuse', ''),
                    'location': (blocks06.get(sid) or {}).get('Admin role / location', ''),
                    'modules': (blocks06.get(sid) or {}).get('Business modules', ''),
                    'automation': dec06[sid].get('automation', ''), 'acceptance': dec06[sid].get('acceptance', ''),
                    'related': dec06[sid].get('related', ''), 'interaction17': (blocks17.get(sid) or {}).get('Interaction', ''),
                    'intent17': (blocks17.get(sid) or {}).get('Intent', '')})

def wcsv(name, rows):
    if not rows: return
    with open(os.path.join(OUT, name), 'w', newline='', encoding='utf-8') as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
wcsv('c_fields.csv', field_rows); wcsv('c_ops.csv', op_rows); wcsv('c_tables.csv', tab_rows)
wcsv('c_tests.csv', test_rows); wcsv('c_plugins.csv', plug_rows); wcsv('c_related.csv', rel_rows)
json.dump({'screens': screens, 'impl': impl, 'blocks06': blocks06, 'dec06': dec06}, open(os.path.join(OUT, 'c_screens.json'), 'w'), indent=1)

C = collections.Counter
summary = {
    'doc06_blocks': len([k for k in blocks06 if not k.startswith('CAP')]), 'doc06_retained_caps': len([k for k in blocks06 if k.startswith('CAP')]),
    'impl_rows': len(impl), 'decisions06': len(dec06), 'decisions17': len(dec17), 'decisions02': len(dec02),
    'decision_text_diff_06_vs_02': diff_06_02, 'decision_text_diff_06_vs_17': diff_06_17,
    'screens_in_p21': sum(s['in_p21'] for s in screens), 'screens_in_p25': sum(s['in_p25'] for s in screens),
    'fields': dict(C(r['status'] for r in field_rows)), 'fields_total': len(field_rows),
    'ops_screen_rows': dict(C(r['status'] for r in op_rows)), 'ops_screen_rows_total': len(op_rows),
    'ops_distinct': dict(C(r['status'] for r in distinct_ops.values())), 'ops_distinct_total': len(distinct_ops),
    'tables': dict(C(r['status'] for r in tab_rows)), 'tables_total': len(tab_rows),
    'test_aliases': dict(C((r['kind'], r['in_bp']) for r in test_rows).items()) if False else {f"{k[0]}:{k[1]}": v for k, v in C((r['kind'], r['in_bp']) for r in test_rows).items()},
    'distinct_unit_aliases': sorted({r['alias'] for r in test_rows if r['kind'] == 'Unit'}),
    'uat_rule_ok': rule_ok, 'ut_fr_count': dict(sorted(ut_fr_count.items())), 'ux_uat_missing': ux_uat_missing, 'ux_fr_missing': ux_fr_missing,
    'plugins': dict(C(r['status'] for r in plug_rows)), 'plugins_distinct': sorted({r['integration'] for r in plug_rows}),
    'plugins_not_covered': sorted({r['integration'] for r in plug_rows if r['status'] == 'Not covered'}),
    'related_edges': len(rel_rows), 'related_in_p25': sum(r['in_p25_row'] for r in rel_rows),
    'interaction_patterns17': {k[:60]: v for k, v in interaction_patterns.items()},
    'build_reuse': dict(C(s['build'] for s in screens)), 'admin_location': dict(C(s['location'] for s in screens)),
}
json.dump(summary, open(os.path.join(OUT, 'c_recon_summary.json'), 'w'), indent=1)
print(json.dumps(summary, indent=1)[:6000])
