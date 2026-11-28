"""Group W: parse every table definition the blueprint gives in Markdown into one machine model.

Inputs : Part 3.3 (§3.3.3.2 catalogue, §3.3.6 column dictionaries, §3.3.7 compact dictionary, §3.3.8 index tables),
         Part 3.6a/b (ENT-ENH-E-01…04 dictionaries, ALTER … ADD COLUMN deltas, IX-ENH-E indexes),
         Part 11.9a §11.9.4.2 (V12 core/enterprise table → physical table mapping), §11.9.4.4 (89 domain tables → typed tables),
         Parts 11.16a/c, 11.17b, 11.18b (new entity tables and ER diagrams).
Output : w_frag/data_model.json
"""
import re, sys, os, json, collections
sys.path.insert(0, os.path.dirname(__file__))
from w_common import *

model = {'tables': {}, 'v12_core_map': {}, 'v12_domain_map': {}, 'alter_sql': [], 'index_sql': [], 'key_indexes': [], 'notes': []}
T = model['tables']

# ------------------------------------------------------------------ standard column sets (Part 3.3 §3.3.6.1)
STD_S = [('id', 'uuid', 'N', '', 'PK'), ('tenant_id', 'uuid', 'N', '', ''), ('startup_id', 'uuid', 'N', '', ''),
         ('revision', 'integer', 'N', '1', 'CHECK (revision >= 1)'), ('created_at', 'timestamptz', 'N', 'now()', ''),
         ('created_by', 'uuid', 'Y', '', ''), ('created_by_type', 'text', 'N', "'user'",
          "CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'))"),
         ('updated_at', 'timestamptz', 'N', 'now()', ''), ('updated_by', 'uuid', 'Y', '', ''),
         ('archived_at', 'timestamptz', 'Y', '', ''), ('archived_by', 'uuid', 'Y', '', ''),
         ('archive_reason', 'text', 'Y', '', 'CHECK (length(archive_reason) <= 500)')]
STD_SA = [c for c in STD_S if c[0] in ('id', 'tenant_id', 'startup_id', 'created_at', 'created_by', 'created_by_type')] + \
         [('correlation_id', 'uuid', 'Y', '', '')]
STD_V = [('version_no', 'integer', 'N', '1', 'CHECK (version_no >= 1)'), ('status', 'text', 'N', "'draft'", ''),
         ('content_hash', 'char(64)', 'Y', '', "CHECK (content_hash ~ '^[0-9a-f]{64}$')"), ('approval_id', 'uuid', 'Y', '', ''),
         ('approved_at', 'timestamptz', 'Y', '', ''), ('effective_from', 'timestamptz', 'Y', '', ''),
         ('effective_to', 'timestamptz', 'Y', '', ''), ('supersedes_id', 'uuid', 'Y', '', '')]
STD_W = [('is_simulated', 'boolean', 'N', 'false', ''), ('run_id', 'uuid', 'Y', '', ''), ('correlation_id', 'uuid', 'Y', '', '')]
P_MIN = [('id', 'uuid', 'N', '', 'PK'), ('revision', 'integer', 'N', '1', 'CHECK (revision >= 1)'),
         ('created_at', 'timestamptz', 'N', 'now()', ''), ('updated_at', 'timestamptz', 'N', 'now()', '')]


def std_columns(sets, scope, imm):
    s = (sets or '').upper()
    cols = []
    def addl(lst):
        for c in lst:
            if c[0] not in [x[0] for x in cols]:
                cols.append(c)
    if 'STD-SA' in s or (imm == 'A' and scope in ('S', 'T', 'X') and 'STD-S' not in s.replace('STD-SA', '')):
        addl(STD_SA)
    elif 'STD-S' in s or 'STD-T' in s or 'STD-X' in s or scope in ('S', 'T', 'X'):
        addl(STD_S)
    else:
        addl(P_MIN)
    if scope in ('T', 'X') or 'STD-T' in s or 'STD-X' in s:
        cols = [(c[0], c[1], 'Y', c[3], c[4]) if c[0] == 'startup_id' else c for c in cols]
    if scope == 'X' or 'STD-X' in s:
        cols = [(c[0], c[1], 'Y', c[3], c[4]) if c[0] == 'tenant_id' else c for c in cols]
    if scope == 'P':
        cols = [c for c in cols if c[0] not in ('tenant_id', 'startup_id')]
    if 'MINUS STARTUP_ID' in s or 'NO STARTUP_ID' in s:
        cols = [c for c in cols if c[0] != 'startup_id']
    if 'STD-V' in s or imm == 'V':
        addl(STD_V)
    if 'STD-W' in s:
        addl(STD_W)
    return [dict(name=c[0], type=c[1], null=c[2], default=c[3], constraint=c[4], cls='Int', std=True) for c in cols]


# ------------------------------------------------------------------ 1. catalogue (199 entities)
f33 = part('Part-03-3_')[0]
for heads, hdr, rows, ln in tables(f33):
    if hdr[:3] == ['ENT', 'Entity (logical)', 'Physical table']:
        for r in rows:
            t = r[2].strip('`')
            T[t] = dict(ent=r[0], entity=r[1], table=t, domain=r[3], origin=r[4], basis=r[5], scope=r[6].split()[0].strip(),
                        imm=r[7].strip(), ret=r[8], source='Part 3.3 §3.3.3.2', sets='', columns=[], constraints=[])
    if hdr[:2] == ['Table', 'Joins']:
        for r in rows:
            t = r[0].strip('`')
            T[t] = dict(ent='ASSOC', entity=r[1], table=t, domain='Association', origin='D', basis=r[3], scope='S',
                        imm='M', ret='BUS', source='Part 3.3 §3.3.3.3', sets='STD-S', columns=[], constraints=[], assoc_key=r[2])

TYPE_RE = re.compile(r'^(uuid|text|integer|int|bigint|smallint|boolean|bool|date|timestamptz|jsonb|bytea|inet|cidr|citext|tsvector|'
                     r'char\(\d+\)|varchar\(\d+\)|numeric\(\d+,\s*\d+\)|numeric|halfvec\(\d+\)|vector\(\d+\)|interval|int4range|tstzrange|daterange)(\[\])?$', re.I)


def norm_type(t):
    t = t.strip().strip('`').lower().replace(' ', '')
    t = t.replace('bool', 'boolean') if t in ('bool', 'bool[]') else t
    t = 'integer' if t == 'int' else t
    t = re.sub(r'numeric\((\d+),(\d+)\)', r'numeric(\1,\2)', t)
    return t


def parse_col_table(t, rows):
    for r in rows:
        if len(r) < 7:
            continue
        name = r[0].strip().strip('`')
        if not name:
            if r[4]:
                T[t]['constraints'].append(r[4])
            continue
        for nm in [x.strip().strip('`') for x in name.split('/')]:
            typ = norm_type(r[1]) if r[1] else 'text'
            if not TYPE_RE.match(typ):
                model['notes'].append(f'{t}.{nm}: type "{r[1]}" mapped to text')
                typ = 'text'
            T[t]['columns'].append(dict(name=nm, type=typ, null=r[2].strip() or 'Y', default=r[3].strip().strip('`'),
                                        constraint=r[4], cls=r[5], desc=r[6]))


# ------------------------------------------------------------------ 2. column dictionaries (Part 3.3 §3.3.6, Part 3.6b)
for path in [f33] + part('Part-03-6b_'):
    L = open(path, encoding='utf-8').read().split('\n')
    cur = None
    i = 0
    while i < len(L):
        m = re.match(r'^\*\*(ENT-[A-Z0-9-]+) ([^(*]+?)\s*\(`([a-z0-9_]+)`\)\*\*(.*)', L[i])
        if m:
            ent, ename, t, rest = m.groups()
            if t not in T:
                sc = re.search(r'[Ss]cope \*{0,2}([STXP])\b', rest)
                im = re.search(r'Imm\.? \*{0,2}([MVFA])', rest)
                T[t] = dict(ent=ent, entity=ename.strip(), table=t, domain='Part 3.6 addition', origin='D', basis=rest[:160],
                            scope=sc.group(1) if sc else 'S', imm=im.group(1) if im else ('V' if 'STD-V' in rest else 'M'),
                            ret='BUS', source='Part 3.6b §3.6.5', sets='', columns=[], constraints=[])
            ss = re.search(r'Sets?: ([^.]*(?:\.[^ ][^.]*)*)', rest)
            T[t]['sets'] = (ss.group(1) if ss else rest)[:200]
            sc = re.search(r'scope \*{0,2}([STXP])\b', rest)
            if sc:
                T[t]['scope'] = sc.group(1)
            cur = t
        elif cur and L[i].startswith('| Column | Type |'):
            rows = []
            j = i + 2
            while j < len(L) and L[j].startswith('|'):
                rows.append(cells(L[j])); j += 1
            parse_col_table(cur, rows)
            i = j
            continue
        elif L[i].startswith('#'):
            cur = None
        i += 1

# ------------------------------------------------------------------ 3. compact dictionary (Part 3.3 §3.3.7)
def split_top(s):
    out, depth, buf = [], 0, ''
    for ch in s:
        if ch in '({[':
            depth += 1
        elif ch in ')}]':
            depth -= 1
        if ch == ',' and depth == 0:
            out.append(buf); buf = ''
        else:
            buf += ch
    if buf.strip():
        out.append(buf)
    return [x.strip() for x in out if x.strip()]


def infer_type(name):
    n = name
    if n.endswith('_ids'):
        return 'uuid[]'
    if n.endswith('_id') or n in ('id',):
        return 'uuid'
    if n.endswith('_at'):
        return 'timestamptz'
    if n.endswith('_date') or n.endswith('_until') or n in ('valid_from', 'valid_to', 'period_start', 'period_end'):
        return 'date' if not n.startswith('valid_') else 'timestamptz'
    if n.startswith(('is_', 'has_')) or n.endswith('_flag'):
        return 'boolean'
    if n.endswith('_hash') or n.endswith('_hmac'):
        return 'char(64)'
    if n.endswith('_enc'):
        return 'bytea'
    if n.endswith('_pct') or n.endswith('_rate') or n in ('confidence', 'weight', 'probability'):
        return 'numeric(7,4)'
    if n == 'currency' or n.endswith('_currency'):
        return 'char(3)'
    if any(k in n for k in ('amount', 'total', 'price', 'cost', 'value_inr', 'budget', 'revenue', 'balance', 'fee')) and not n.endswith(('_ref', '_code', '_type')):
        return 'numeric(18,2)'
    if any(k in n for k in ('qty', 'quantity')):
        return 'numeric(18,4)'
    if n.endswith(('_count', '_no', '_seconds', '_ms', '_days', '_minutes', '_hours')) or n in ('priority', 'sort_order', 'attempt', 'attempts', 'rank', 'tokens', 'version'):
        return 'integer'
    if 'score' in n:
        return 'numeric(9,4)'
    if n.endswith(('_json', '_spec', '_config', '_payload', '_snapshot', '_map', '_rules', '_metrics', '_schema')) or n in (
            'attributes', 'payload', 'metadata', 'config', 'settings', 'capabilities', 'filter_spec', 'metrics', 'thresholds', 'parameters', 'inputs', 'outputs', 'details', 'result', 'scope', 'limits'):
        return 'jsonb'
    if n.endswith('s') and n in ('tags', 'actions', 'channels', 'languages', 'regions', 'locales', 'scopes', 'permissions', 'sectors', 'stages'):
        return 'text[]'
    return 'text'


def parse_item(item):
    """'`name` (a, b, c)' or '`name` char(3) PK' or '`a`, `b`' -> list of column dicts."""
    names = re.findall(r'`([a-z][a-z0-9_]*)`', item)
    if not names:
        return []
    cls = 'Int'
    mcls = re.search(r'\((Conf|Rest|Int|Pub)\)', item)
    if mcls:
        cls = mcls.group(1)
    typ, check = None, None
    after = item.split('`')[-1]
    mt = re.search(r'\b(uuid\[\]|text\[\]|uuid|text|integer|int|bigint|smallint|boolean|bool|date|timestamptz|jsonb|bytea|inet|citext|char\(\d+\)|numeric\(\d+,\s*\d+\)|halfvec\(\d+\)|tsvector)\b', after)
    if mt:
        typ = norm_type(mt.group(1))
    me = re.search(r'\(([^()]*)\)', after)
    if me and not mt:
        vals = [v.strip() for v in me.group(1).split(',')]
        if len(vals) >= 2 and all(re.match(r'^[a-z][a-z0-9_]*$', v) for v in vals):
            check = vals
    out = []
    for n in names[:1] if len(names) == 1 else names:
        t = typ or infer_type(n)
        if check:
            t = 'text'
        out.append(dict(name=n, type=t, null='Y', default='', constraint=('CHECK (' + n + ' IN (' + ','.join("'" + v + "'" for v in check) + '))') if check and len(names) == 1 else '',
                        cls=cls, desc='compact dictionary', inferred=typ is None))
    return out


for heads, hdr, rows, ln in tables(f33):
    if hdr[:3] == ['ENT', 'Table', 'Std set']:
        for r in rows:
            t = r[1].strip('`')
            if t not in T:
                T[t] = dict(ent=r[0], entity=t, table=t, domain='?', origin='D', basis='', scope='S', imm='M', ret='BUS',
                            source='Part 3.3 §3.3.7', sets='', columns=[], constraints=[])
            T[t]['sets'] = r[2]
            if T[t]['source'].startswith('Part 3.3 §3.3.3'):
                T[t]['source'] = 'Part 3.3 §3.3.3.2 + §3.3.7'
            for it in split_top(r[3]):
                for c in parse_item(it):
                    if c['name'] not in [x['name'] for x in T[t]['columns']]:
                        T[t]['columns'].append(c)
            T[t]['constraints'].append(r[4])
    if hdr[:3] == ['Index', 'Table', 'Definition']:
        for r in rows:
            model['key_indexes'].append(dict(name=r[0].strip('`'), table=r[1].split(' ')[0].strip('`'), definition=r[2].strip('`'), serves=r[3] if len(r) > 3 else ''))

# ------------------------------------------------------------------ 4. Part 3.6b SQL deltas (ALTER … ADD COLUMN; indexes)
for path in part('Part-03-6b_'):
    txt = open(path, encoding='utf-8').read()
    for blk in re.findall(r'```sql\n(.*?)```', txt, re.S):
        for line in blk.split('\n'):
            s = line.strip()
            if re.match(r'^ALTER TABLE \w+ ADD COLUMN', s):
                model['alter_sql'].append(s)
            elif re.match(r'^CREATE (UNIQUE )?INDEX', s):
                model['index_sql'].append(s)

# ------------------------------------------------------------------ 5. Part 11.9a mappings
for heads, hdr, rows, ln in tables(part('Part-11-9a_')[0]):
    if hdr[:3] == ['V12 table (source)', 'Physical table', 'ENT / origin']:
        for r in rows:
            v12 = re.match(r'`([a-z_0-9]+)`', r[0]).group(1)
            phys = re.match(r'`([a-z_0-9]+)`', r[1]).group(1)
            model['v12_core_map'][v12] = dict(physical=phys, ent=r[2], scope=r[3], imm=r[4], before=r[5], added=r[6], rules=r[7])
    if len(hdr) > 3 and hdr[1] == 'V12 domain table':
        for r in rows:
            model['v12_domain_map'][r[1].strip('`')] = dict(ent=r[2], physical=r[3].strip('`'), scope_imm=r[4])


# ------------------------------------------------------------------ 6. Parts 11.16–11.18 new entity tables
def er_entities(txt):
    ents = {}
    for blk in re.findall(r'```mermaid\n(erDiagram.*?)```', txt, re.S):
        for m in re.finditer(r'^\s*([a-z][a-z0-9_]+)\s*\{([^}]*)\}', blk, re.M):
            name, body = m.group(1), m.group(2)
            attrs = []
            for a in re.split(r'\n|(?<=[a-zA-Z0-9_]) (?=(?:uuid|string|int|decimal|timestamp|date|boolean|bigint|text|json|float|numeric) )', body):
                toks = a.split()
                if len(toks) >= 2:
                    attrs.append((toks[0], toks[1], ' '.join(toks[2:])))
            ents.setdefault(name, []).extend(attrs)
    return ents

ER_T = {'uuid': 'uuid', 'string': 'text', 'int': 'integer', 'decimal': 'numeric(20,4)', 'timestamp': 'timestamptz', 'date': 'date',
        'boolean': 'boolean', 'bigint': 'bigint', 'text': 'text', 'json': 'jsonb', 'float': 'numeric', 'numeric': 'numeric'}

NEW_SRC = [('Part-11-16a_', 'Part 11.16a §11.16.5.10', 'investment'), ('Part-11-16c_', 'Part 11.16c §11.16.15.18', 'investment'),
           ('Part-11-17b_', 'Part 11.17b §11.17.9.2', 'mandates'), ('Part-11-18b_', 'Part 11.18b §11.18.5.24', 'voice')]
for pref, src, dom in NEW_SRC:
    for path in part(pref):
        txt = open(path, encoding='utf-8').read()
        ers = er_entities(txt)
        # entity tables
        for heads, hdr, rows, ln in tables(path):
            h0 = hdr[0].lower()
            if h0 not in ('entity', 'entity / group', 'table') or len(hdr) < 2:
                continue
            for r in rows:
                names = re.findall(r'\b((?:inv|mandate|kill|payment|commerce|bid|portal|agent|voice|coaching|effect|counterparty|negotiation|psp|recon|settlement|dispute|refund)[a-z0-9_]*)\b', r[0])
                if not names:
                    continue
                ik = next((k for k, h in enumerate(hdr) if 'key' in h.lower()), 2 if pref == 'Part-11-16a_' else 1)
                keycell = r[ik] if ik < len(r) else ''
                if pref == 'Part-11-16c_':
                    keycell = re.sub(r'^[^,]*?\bwith\b', '', keycell)
                items = []
                for it in split_top(keycell.replace(';', ',')):
                    it = it.strip()
                    m0 = re.match(r'`?([a-z][a-z0-9_]*)(\[\]|\{\})?`?(?:\s+(uuid|text|jsonb|integer|int|bigint|boolean|date|timestamptz|char\(\d+\)|numeric\(\d+,\d+\)))?', it)
                    if not m0:
                        continue
                    k, br, ty = m0.groups()
                    if k in ('id', 'tenant_id', 'startup_id', 'company_id', 'version', 'and', 'or', 'of', 'the', 'per', 'with', 'from', 'by', 'to', 'for', 'in', 'same', 'normalised', 'as', 'new', 'derived') or len(k) < 2:
                        continue
                    if pref == 'Part-11-16c_' and '_' not in k and len(items) == 0 and not br:
                        pass
                    t2 = norm_type(ty) if ty else ('jsonb' if br == '{}' else ((('uuid[]' if k.endswith('_ids') else 'text[]')) if br == '[]' else infer_type(k)))
                    items.append((k, t2, ty is None and not br))
                for n in names:
                    if n in T:
                        continue
                    T[n] = dict(ent='NEW', entity=n, table=n, domain=dom, origin='V12-B', basis=r[1][:200] if len(r) > 1 else '',
                                scope='S', imm='A' if re.search(r'append-only|ledger|_event$|_log$|_result$|_vote$', n + ' ' + ' '.join(r)) else 'M',
                                ret=r[4] if pref == 'Part-11-16a_' and len(r) > 4 else 'BUS', source=src, sets='STD-S', columns=[], constraints=[])
                    for k, t2, inf in items:
                        if k not in [c['name'] for c in T[n]['columns']]:
                            T[n]['columns'].append(dict(name=k, type=t2, null='Y', default='', constraint='', cls='Int', desc=src, inferred=inf))
        # ER attributes (typed) override / add
        for n, attrs in ers.items():
            if n not in T:
                T[n] = dict(ent='NEW', entity=n, table=n, domain=dom, origin='V12-B', basis='ER diagram', scope='S',
                            imm='A' if re.search(r'_event$|_log$|_ledger$|_result$|_vote$|consumption|decision', n) else 'M',
                            ret='BUS', source=src + ' (ER)', sets='STD-S', columns=[], constraints=[])
            have = {c['name']: c for c in T[n]['columns']}
            for typ, nm, key in attrs:
                if nm in ('id', 'tenant_id', 'company_id', 'startup_id'):
                    continue
                ty = ER_T.get(typ.lower(), 'text')
                if nm in have:
                    have[nm]['type'] = ty; have[nm]['inferred'] = False
                else:
                    T[n]['columns'].append(dict(name=nm, type=ty, null='Y', default='', constraint='', cls='Int', desc=src + ' ER', inferred=False))

# Part 3.3: payable entry has the same structure as receivable entry (ENT-145/146)
if 'com_receivable_entry' in T and not T['com_payable_entry']['columns']:
    T['com_payable_entry']['columns'] = [dict(c) for c in T['com_receivable_entry']['columns']]
    T['com_payable_entry']['sets'] = T['com_receivable_entry']['sets']
for t, v in T.items():
    if v.get('assoc_key') and not v['columns']:
        for k in re.findall(r'([a-z_]+_(?:id|ref|role|code))', v['assoc_key']):
            v['columns'].append(dict(name=k, type='uuid' if k.endswith('_id') else 'text', null='N', default='', constraint='', cls='Int', desc='association key'))
        v['constraints'].append('UQ ' + v['assoc_key'])
# mark investment Imm. A tables named in 11.16c
for n in ('inv_offer_ledger', 'inv_cap_table_revision', 'inv_vote', 'inv_kyc_provider_result', 'inv_advice_boundary_event'):
    if n in T:
        T[n]['imm'] = 'A'

stats = collections.Counter(v['source'].split(' §')[0] for v in T.values())
model['stats'] = dict(tables=len(T), by_source=dict(stats), columns=sum(len(v['columns']) for v in T.values()),
                      tables_without_columns=[k for k, v in T.items() if not v['columns']],
                      alter_sql=len(model['alter_sql']), index_sql=len(model['index_sql']), key_indexes=len(model['key_indexes']),
                      v12_core_map=len(model['v12_core_map']), v12_domain_map=len(model['v12_domain_map']))
save_json('data_model.json', model)
print(json.dumps(model['stats'], indent=1)[:4000])
