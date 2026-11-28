"""Group W (Part 11.24): build ONE merged OpenAPI 3.1 contract from every API catalogue table in the blueprint.

Sources (catalogue tables, not reconciliation/mapping tables):
  Part 3.2   API-001..555 (baseline)                 Part 3.5b  API-ENH-D-001..024 (baseline; 555+24 = 579)
  Part 9.7b  API-ADV-X1-01..40                         Part 11.8b API-V12-H-001..076
  Part 11.13b API-V12-M-01..24                         Part 11.16a API-V12-N-001..152
  Part 11.16c investor operations (no IDs)             Part 11.17b mandate/commerce/payments/bids operations (no IDs)
  Part 11.18b API-V12-Q-001..040 (voice)               Part 11.19a/b API-V12-R-001..052
  Part 11.5b  V12 platform-architecture operations (no IDs)
Operations without a source ID receive API-V12-W-#### (this part). Paths are normalised (`~/` = /api/v1/commercial/),
multi-route cells are expanded, and duplicates (same method + same templated path) are merged with x-also-defined-as.
Outputs: final/build/openapi.yaml, final/build/api_index.csv, w_frag/openapi_stats.json, w_frag/openapi_rows.json
"""
import re, sys, csv, json, collections, os
sys.path.insert(0, os.path.dirname(__file__))
from w_common import *
import yaml

METHODS = ('GET', 'POST', 'PUT', 'PATCH', 'DELETE')
ABS = ('/api/', '/scim/', '/oauth/', '/hooks/', '/bff/', '/.well-known/', '/health', '/ready', '/agent/')
rows = []          # harvested raw operations
unparsed = []      # cells we could not turn into operations
excluded = []      # e.g. WSS media streams


def norm_path(p, base):
    p = p.strip().strip('`').strip()
    p = p.split('?')[0].split(' ')[0].rstrip('.,;:')
    p = p.replace('…', '…')
    if p.startswith('~/'):
        p = '/api/v1/commercial/' + p[2:]
    if not p.startswith('/'):
        p = '/' + p
    if not p.startswith(ABS) and base:
        p = base.rstrip('/') + p
    p = re.sub(r'/+', '/', p)
    if len(p) > 1:
        p = p.rstrip('/')
    return p


LAST = None


def expand_cell(cell, methods, base):
    """Turn a cell like '`GET/POST /api/v1/x`, `POST …/{id}/y`' into [(method, path)]."""
    out = []
    txt = cell.replace('`', ' ` ')
    # tokens: method groups, paths (/..., ~/..., …/...)
    toks = re.findall(r'((?:GET|POST|PUT|PATCH|DELETE)(?:/(?:GET|POST|PUT|PATCH|DELETE))*)(?![A-Za-z])|((?:…|\.\.\.)?~?/[^\s`,;()]*)', txt)
    global LAST
    cur = [x.strip() for x in methods] if methods else []
    prev = LAST
    for mg, pth in toks:
        if mg:
            cur = mg.split('/')
            continue
        if not pth or pth in ('/',):
            continue
        if pth.startswith('…') or pth.startswith('...'):
            rel = pth.lstrip('….')
            if prev is None:
                unparsed.append(cell); continue
            first = rel.strip('/').split('/')[0]
            segs = prev.split('/')
            if first and '/' + first in prev:
                cut = prev.index('/' + first)
                full = prev[:cut] + rel
            else:
                full = prev + rel
            full = norm_path(full, None)
        else:
            nseg = len([s for s in pth.strip('/').split('/') if s])
            if prev is not None and nseg == 1 and not pth.startswith(ABS) and not pth.startswith('~') \
                    and len(prev.strip('/').split('/')) >= 2 and not pth.startswith('/{'):
                # sibling action: replace last segment of previous path (e.g. `/pause`, `/resume`)
                full = norm_path(prev.rsplit('/', 1)[0] + pth, None) if prev.count('/') > 1 else norm_path(pth, base)
                # only treat as sibling when previous was an action path or a list under the same parent
            else:
                full = norm_path(pth, base)
        if not cur:
            unparsed.append(cell); continue
        for m in cur:
            out.append((m, full))
        prev = full
        LAST = full
    return out


def add(src_id, method, path, **kw):
    r = dict(src_id=src_id, method=method, path=path)
    r.update(kw)
    rows.append(r)


def col(hdr, *names):
    for n in names:
        for i, h in enumerate(hdr):
            if h.lower().startswith(n.lower()):
                return i
    return None


# ---------------------------------------------------------------- 1. Part 3.2 and 3.5b (baseline 579) + 11.8b (H)
DETAIL = {}
for pref, fam in (('Part-03-2_', '3.2'), ('Part-03-5b_', '3.5b'), ('Part-11-8b_', '11.8b')):
    for f in part(pref):
        for heads, hdr, trs, ln in tables(f):
            LAST = None
            if hdr[:2] == ['Op ID', 'Request']:
                for r in trs:
                    if len(r) >= 6:
                        DETAIL[r[0].replace(' ★', '')] = dict(request=r[1], response=r[2], rules=r[3], errors=r[4], event=r[5])
                continue
            if hdr[:3] != ['Op ID', 'Method', 'Path']:
                continue
            tag = heads.get(4) or heads.get(3) or 'Catalogue'
            if fam == '3.5b':
                tag = 'Source-pack additions API-ENH-D (Part 3.5b)'
            elif fam == '11.8b':
                tag = 'V12 developer platform and enterprise API-V12-H (Part 11.8b)'
            iNS, iP, iFR, iA, iI, iSE, iPDP, iRL = (col(hdr, x) for x in ('NS', 'Purpose', 'FR', 'Auth', 'Idempotent', 'SE', 'PDP', 'RL'))
            iSrc = col(hdr, 'Source', 'V12 source'); iPh = col(hdr, 'V12 phase')
            for r in trs:
                if not r or not re.match(r'API-', r[0]):
                    continue
                oid = r[0].replace(' ★', '').strip(); star = '★' in r[0]
                for m, p in expand_cell(r[2], r[1].split('/'), None):
                    add(oid, m, p, ns=r[iNS], purpose=r[iP], fr=r[iFR], roles=r[iA], idem=r[iI], se=r[iSE], pdp=r[iPDP],
                        rl=r[iRL], tag=re.sub(r'\s*\(.*', '', tag), part=fam, star=star,
                        v12src=r[iSrc] if iSrc is not None else '', phase=r[iPh] if iPh is not None else '',
                        baseline=fam in ('3.2', '3.5b'))

# ---------------------------------------------------------------- 2. Part 9.7b ADV-X1
for f in part('Part-09-7b_'):
    for heads, hdr, trs, ln in tables(f):
        LAST = None
        if hdr[:3] == ['ID', 'Method', 'Path']:
            for r in trs:
                if r and r[0].startswith('API-ADV'):
                    for m, p in expand_cell(r[2], r[1].split('/'), None):
                        add(r[0], m, p, ns='admin', purpose=r[3], roles=r[4], idem=r[5], fr=r[6], part='9.7b',
                            tag='Advanced AI agents (Part 9.7b)', se='Q' if m == 'POST' else 'R', pdp='', rl='RL-ADM-H')

# ---------------------------------------------------------------- 3. Part 11.13b M, 11.19 R, 11.5b (Method and path)
for pref, fam, tagname in (('Part-11-13b_', '11.13b', 'AI improvement (Part 11.13b)'),
                           ('Part-11-19a_', '11.19a', 'Platform decisions: identity, developer platform, connectors (Part 11.19a)'),
                           ('Part-11-19b_', '11.19b', 'Platform decisions: RPO, model registry, benchmarks (Part 11.19b)'),
                           ('Part-11-5b_', '11.5b', 'V12 platform architecture (Part 11.5b)')):
    for f in part(pref):
        for heads, hdr, trs, ln in tables(f):
            LAST = None
            if 'Method and path' not in hdr:
                continue
            iMP = hdr.index('Method and path')
            for k, r in enumerate(trs):
                if not r or len(r) <= iMP:
                    continue
                sid = r[0] if iMP > 0 else ''
                if iMP > 0 and not re.match(r'API-', sid):
                    continue
                cell = r[iMP]
                ops = []
                if sid in ('API-V12-R-011', 'API-V12-R-012'):
                    res = 'Users' if sid.endswith('011') else 'Groups'
                    ops = [('GET', f'/scim/v2/{res}'), ('POST', f'/scim/v2/{res}')] + \
                          [(m, f'/scim/v2/{res}/{{id}}') for m in ('GET', 'PUT', 'PATCH', 'DELETE')]
                    if res == 'Groups':
                        ops += [('POST', '/scim/v2/Bulk'), ('GET', '/scim/v2/ServiceProviderConfig'),
                                ('GET', '/scim/v2/Schemas'), ('GET', '/scim/v2/ResourceTypes')]
                elif cell.strip().startswith('`/scim/'):
                    ops = []   # SCIM listing without verbs: covered by API-V12-R-011/012
                    continue
                else:
                    ops = expand_cell(cell, [], None)
                if not ops:
                    unparsed.append(f'{fam} {sid} {cell}')
                rest = r[iMP + 1:]
                for m, p in ops:
                    add(sid or '', m, p, ns='admin' if '/admin' in p else ('hooks' if p.startswith('/hooks') else 'tenant-api'),
                        purpose=rest[0] if rest else '', roles=rest[1] if len(rest) > 1 else (rest[0] if rest else ''),
                        fr=rest[-1] if pref == 'Part-11-5b_' else '', part=fam, tag=tagname,
                        idem='Key' if m == 'POST' else ('If-Match' if m in ('PUT', 'PATCH', 'DELETE') else 'Safe'),
                        se='R' if m == 'GET' else 'W', pdp='', rl='RL-ADM')

# ---------------------------------------------------------------- 4. Part 11.16a N (API | Operation | Services | Class / note | Origin)
for f in part('Part-11-16a_'):
    for heads, hdr, trs, ln in tables(f):
        LAST = None
        if hdr[:2] == ['API', 'Operation']:
            for r in trs:
                if r and r[0].startswith('API-V12-N'):
                    for m, p in expand_cell(r[1], [], None):
                        add(r[0], m, p, ns='investor' if '/investor' in p or '/investment' in p else 'admin',
                            purpose=r[3], roles=re.sub(r'.*role ', '', r[3]) if 'role ' in r[3] else '',
                            fr='INV-SVC-' + r[2], part='11.16a', tag='Investment Automation I (Part 11.16a)',
                            idem='Key' if m == 'POST' else 'Safe', se='R' if m == 'GET' else ('X' if 'Effect' in r[3] else 'W'),
                            pdp='P+D' if 'Effect' in r[3] else '', rl='RL-ADM', v12src=r[4])

# ---------------------------------------------------------------- 5. Part 11.16c investor (no IDs), 11.17b (no IDs), 11.18b (Q)
for f in part('Part-11-16c_'):
    for heads, hdr, trs, ln in tables(f):
        LAST = None
        if len(hdr) > 1 and hdr[0] == 'Method' and hdr[1].startswith('Path (/api/v1/investor'):
            for r in trs:
                for m, p in expand_cell(r[1], [r[0]], '/api/v1/investor'):
                    add('', m, p, ns='investor', purpose=r[2], roles=r[3], fr=r[4], errors=r[5], part='11.16c',
                        tag='Investment Automation II (Part 11.16c)', idem='Key' if m == 'POST' else 'Safe',
                        se='R' if m == 'GET' else 'W', pdp='P+D' if 'PDP' in r[4] else '', rl='RL-ADM')
for f in part('Part-11-17b_'):
    for heads, hdr, trs, ln in tables(f):
        LAST = None
        if hdr[:2] == ['Method', 'Path'] and 'Idempotency' in hdr:
            for r in trs:
                for m, p in expand_cell(r[1], r[0].split('/'), '/api/v2'):
                    add('', m, p, ns='hooks' if '/webhooks/' in p else ('public' if '/.well-known' in p or '/agent' in p else 'admin'),
                        purpose=r[2], roles=r[3], idem=r[4], errors=r[5], part='11.17b',
                        tag='Bounded mandates, agentic commerce, payments, bids (Part 11.17)',
                        se='R' if m == 'GET' else ('X' if any(k in p for k in ('submissions', 'payments', 'kill')) else 'A' if 'approvals' in p else 'W'),
                        pdp='P+D' if m != 'GET' else '', rl='RL-ADM')
for f in part('Part-11-18b_'):
    for heads, hdr, trs, ln in tables(f):
        LAST = None
        if hdr[:3] == ['API', 'Method', 'Path']:
            for r in trs:
                if not r or not r[0].startswith('API-V12-Q'):
                    continue
                if r[1] == 'WSS':
                    excluded.append((r[0], r[1], r[2], 'WebSocket media stream (not an HTTP operation; documented in x-websockets)'))
                    continue
                surf = r[3]
                cellp = r[2]
                base = '/api/v2/admin/voice' if surf.startswith('admin') else ('/api/v2/public/voice' if surf.startswith('public') else None)
                if surf.startswith('public'):
                    cellp = cellp.replace('/public/', '/')
                for m, p in expand_cell(cellp, r[1].split('/'), base):
                    add(r[0], m, p, ns=surf, purpose=r[4], roles=r[5], fr=r[6], notes=r[7], part='11.18b',
                        tag='AI voice and recordings (Part 11.18)', idem='Key' if m == 'POST' else ('If-Match' if m in ('PUT', 'PATCH') else 'Safe'),
                        se='R' if m == 'GET' else ('X' if any(k in p for k in ('takeover', 'kill', 'switch')) else 'W'),
                        pdp='P+D' if m == 'POST' and surf.startswith('admin') else '', rl='RL-HOOK' if surf.startswith('hooks') else 'RL-ADM')

# ---------------------------------------------------------------- 6. merge
def key(m, p):
    return m + ' ' + re.sub(r'\{[^}]+\}', '{}', p)

merged = collections.OrderedDict()
wseq = 0
for r in rows:
    if not r['src_id']:
        wseq += 1
        r['src_id'] = f'API-V12-W-{wseq:04d}'
    k = key(r['method'], r['path'])
    if k in merged:
        merged[k]['also'].append(r['src_id'])
    else:
        r['also'] = []
        merged[k] = r

# operationId must be unique; one source row can expand into several ops
seen = collections.Counter()
for k, r in merged.items():
    seen[r['src_id']] += 1
    r['operationId'] = r['src_id'] if seen[r['src_id']] == 1 else f"{r['src_id']}.{seen[r['src_id']]}"

# unify path-parameter spellings for equivalent templated paths
canon = {}
for r in merged.values():
    t = re.sub(r'\{[^}]+\}', '{}', r['path'])
    canon.setdefault(t, r['path'])
for r in merged.values():
    r['path'] = canon[re.sub(r'\{[^}]+\}', '{}', r['path'])]


# ---------------------------------------------------------------- 7. emit OpenAPI 3.1
def clean(s):
    return re.sub(r'\s+', ' ', (s or '').replace('`', '')).strip()

SEC = {
    'admin': [{'bffAdminSession': []}], 'portal': [{'bffWebSession': []}], 'public': [{}],
    'hooks': [{'webhookSignature': []}], 'internal': [{'workloadIdentity': []}], 'investor': [{'bffAdminSession': []}],
    'tenant-api': [{'bffAdminSession': []}, {'apiKey': []}, {'oauth2ClientCredentials': []}],
}

def security_for(r):
    ns = (r.get('ns') or 'admin').split('+')[0].split(' ')[0]
    p = r['path']
    if p.startswith('/scim/'):
        return [{'scimBearer': []}]
    if p.startswith('/oauth/'):
        return [{'oauthClientAuth': []}]
    if p.startswith('/bff/') or p.startswith('/.well-known') or p in ('/health', '/ready', '/api/v1/health', '/api/v1/ready'):
        return [{}]
    if p.startswith('/hooks/') or '/webhooks/' in p:
        return [{'webhookSignature': []}]
    return SEC.get(ns, [{'bffAdminSession': []}])

paths = {}
tags = {}
for r in merged.values():
    p, m = r['path'], r['method'].lower()
    params = []
    for pn in re.findall(r'\{([^}]+)\}', p):
        params.append({'name': pn, 'in': 'path', 'required': True,
                       'schema': {'type': 'string'} if pn in ('ref', 'token', 'provider', 'protocol', 'psp', 'port', 'workflow', 'task', 'locale', 'zone', 'date', 'v', 'installation') else {'type': 'string', 'format': 'uuid'}})
    params.append({'$ref': '#/components/parameters/XRequestId'})
    idem = (r.get('idem') or '')
    if m == 'post' and ('Key' in idem or 'key' in idem or idem == ''):
        if not (p.startswith('/hooks/') or p.startswith('/bff/') or p.startswith('/scim/') or p.startswith('/oauth/')):
            params.append({'$ref': '#/components/parameters/IdempotencyKey'})
    if m in ('put', 'patch', 'delete') or 'If-Match' in idem:
        params.append({'$ref': '#/components/parameters/IfMatch'})
    if (r.get('ns') or '').startswith('admin'):
        params.append({'$ref': '#/components/parameters/XScopeToken'})
    if m == 'get' and re.search(r'^(List|Search|Browse)|list|\(cursor|cursor', r.get('purpose') or '', re.I):
        params += [{'$ref': '#/components/parameters/Limit'}, {'$ref': '#/components/parameters/Cursor'}]
    se = (r.get('se') or '').strip()
    ok = '202' if se == 'Q' else ('201' if m == 'post' and re.search(r'^(Create|Submit|Register|Add|Open|Start|Upload|Record|Draft|Request)', r.get('purpose') or '') else '200')
    det = DETAIL.get(r['src_id'], {})
    responses = {ok: {'description': clean(det.get('response')) or 'Success',
                      'content': {'application/json': {'schema': {'$ref': '#/components/schemas/' + ('Page' if m == 'get' and ok == '200' and 'cursor' in str(params) else ('RunAccepted' if ok == '202' else 'Resource'))}}}}}
    for code in (['400', '401', '403', '404', '409', '422', '429'] if m != 'get' else ['400', '401', '403', '404', '429']):
        responses[code] = {'$ref': '#/components/responses/P' + code}
    tag = clean(r.get('tag')) or 'Other'
    tags.setdefault(tag, 0); tags[tag] += 1
    op = {'operationId': r['operationId'], 'summary': clean(r.get('purpose'))[:240] or r['operationId'],
          'tags': [tag], 'parameters': params, 'responses': responses, 'security': security_for(r),
          'x-source-part': 'Part ' + r['part'], 'x-namespace': clean(r.get('ns')),
          'x-roles': clean(r.get('roles')), 'x-fr': clean(r.get('fr')), 'x-idempotency': clean(r.get('idem')),
          'x-side-effect-class': se, 'x-pdp': clean(r.get('pdp')), 'x-rate-limit-class': clean(r.get('rl')),
          'x-baseline': bool(r.get('baseline'))}
    if r.get('star'):
        op['x-frd-named'] = True
    if r['also']:
        op['x-also-defined-as'] = r['also']
    if r.get('v12src'):
        op['x-v12-source'] = clean(r['v12src'])
    if r.get('phase'):
        op['x-v12-phase'] = clean(r['phase'])
    desc = []
    for lbl, kk in (('Request', 'request'), ('Business rules', 'rules'), ('Specific errors', 'errors'), ('Event emitted', 'event')):
        v = clean(det.get(kk) or (r.get(kk) if kk == 'errors' else ''))
        if v and v != '—':
            desc.append(f'**{lbl}:** {v}')
    if r.get('notes'):
        desc.append('**Notes:** ' + clean(r['notes']))
    if desc:
        op['description'] = '\n\n'.join(desc)
    if m in ('post', 'put', 'patch'):
        op['requestBody'] = {'required': m != 'post' or se not in ('R',), 'content': {'application/json': {'schema': {'$ref': '#/components/schemas/Command'}}}}
    paths.setdefault(p, {})[m] = op

problem = {'type': 'object', 'required': ['type', 'title', 'status'], 'properties': {
    'type': {'type': 'string', 'format': 'uri-reference'}, 'title': {'type': 'string'}, 'status': {'type': 'integer'},
    'detail': {'type': 'string'}, 'instance': {'type': 'string'}, 'code': {'type': 'string', 'description': 'Stable error code, e.g. STALE_REVISION'},
    'rule_id': {'type': 'string', 'description': 'Business rule ID (BRL-, RP-, MC-)'}, 'correlation_id': {'type': 'string', 'format': 'uuid'},
    'title_key': {'type': 'string'}, 'errors': {'type': 'array', 'items': {'type': 'object'}}}}
codes = {'400': 'Validation failed (VALIDATION_FAILED, FILTER_NOT_ALLOWED, IDEMPOTENCY_KEY_REQUIRED)', '401': 'Not authenticated or step-up required',
         '403': 'Forbidden (RBAC/ABAC/PDP deny)', '404': 'Not found or out of scope (uniform 404, BRL-TEN-04)',
         '409': 'Conflict (STALE_REVISION, IDEMPOTENCY_KEY_REUSED, SCOPE_CHANGED, HASH_CHANGED, DIGEST_MISMATCH)',
         '422': 'Business rule violation (rule_id in body)', '429': 'Rate limited (Retry-After, RateLimit headers)'}
spec = {
    'openapi': '3.1.0',
    'info': {'title': 'AI Growth Engine: consolidated API contract (Part 11.24)', 'version': '12.0.0-build.1',
             'summary': 'Single merged contract generated from every API catalogue table of the blueprint',
             'description': ('Generated by assembly/v12b/w_01_openapi.py. Baseline 579 operations (Part 3.2 API-001…555 + Part 3.5b '
                             'API-ENH-D-001…024) plus Part 9.7b, Part 11.5b, 11.8b, 11.13b, 11.16a/c, 11.17b, 11.18b and 11.19a/b. '
                             'Per-namespace documents (public, portal, admin, internal, hooks) are produced from this file by filtering on '
                             'x-namespace (Part 3.2 §3.2.1.3). Precedence: Part 11.24 > 11.14–11.23 > 11.1–11.13 > earlier parts.'),
             'license': {'name': 'Proprietary', 'identifier': 'LicenseRef-Proprietary'}},
    'jsonSchemaDialect': 'https://spec.openapis.org/oas/3.1/dialect/base',
    'servers': [{'url': 'https://api.in.{domain}', 'description': 'India residency zone (ap-south-1 / Supabase Mumbai)', 'variables': {'domain': {'default': 'example.invalid'}}},
                {'url': 'https://api.eu.{domain}', 'description': 'EU residency zone (eu-central-1 / Supabase Frankfurt)', 'variables': {'domain': {'default': 'example.invalid'}}}],
    'tags': [{'name': t, 'description': f'{n} operations'} for t, n in tags.items()],
    'paths': paths,
    'components': {
        'schemas': {
            'Problem': problem,
            'Resource': {'type': 'object', 'description': 'Resource representation (snake_case, revision, scope metadata; Part 3.2 §3.2.1.2)',
                         'properties': {'id': {'type': 'string', 'format': 'uuid'}, 'revision': {'type': 'integer', 'minimum': 1},
                                        'scope': {'type': 'object'}, 'content_hash': {'type': 'string', 'pattern': '^[0-9a-f]{64}$'}},
                         'additionalProperties': True},
            'Command': {'type': 'object', 'description': 'Request body; per-operation fields are listed in the operation description and in the source part. Unknown fields are rejected (additionalProperties false in the generated per-namespace documents).', 'additionalProperties': True},
            'Page': {'type': 'object', 'required': ['data', 'page'], 'properties': {
                'data': {'type': 'array', 'items': {'$ref': '#/components/schemas/Resource'}},
                'page': {'type': 'object', 'properties': {'next_cursor': {'type': ['string', 'null']}, 'prev_cursor': {'type': ['string', 'null']}, 'limit': {'type': 'integer'}}},
                'meta': {'type': 'object', 'properties': {'as_of': {'type': 'string', 'format': 'date-time'}, 'total_estimate': {'type': 'integer'}, 'total_exact': {'type': 'boolean'}}}}},
            'RunAccepted': {'type': 'object', 'properties': {'run_id': {'type': 'string', 'format': 'uuid'}, 'status_url': {'type': 'string'}, 'state': {'type': 'string'}}},
            'Money': {'type': 'object', 'required': ['amount', 'currency'], 'properties': {'amount': {'type': 'string', 'pattern': '^-?[0-9]+(\\.[0-9]{1,4})?$'}, 'currency': {'type': 'string', 'pattern': '^[A-Z]{3}$'}}},
        },
        'parameters': {
            'XRequestId': {'name': 'X-Request-Id', 'in': 'header', 'required': False, 'schema': {'type': 'string'}},
            'IdempotencyKey': {'name': 'Idempotency-Key', 'in': 'header', 'required': True, 'schema': {'type': 'string', 'minLength': 22, 'maxLength': 128}},
            'IfMatch': {'name': 'If-Match', 'in': 'header', 'required': True, 'schema': {'type': 'string', 'pattern': '^"r[0-9]+"$'}},
            'XScopeToken': {'name': 'X-Scope-Token', 'in': 'header', 'required': True, 'schema': {'type': 'string'}},
            'Limit': {'name': 'limit', 'in': 'query', 'schema': {'type': 'integer', 'minimum': 1, 'maximum': 100, 'default': 25}},
            'Cursor': {'name': 'cursor', 'in': 'query', 'schema': {'type': 'string'}},
        },
        'responses': {'P' + c: {'description': d, 'content': {'application/problem+json': {'schema': {'$ref': '#/components/schemas/Problem'}}}} for c, d in codes.items()},
        'securitySchemes': {
            'bffAdminSession': {'type': 'apiKey', 'in': 'cookie', 'name': '__Host-ge_admin', 'description': 'BFF-admin session cookie (OIDC code+PKCE, DEC-019); CSRF header required on unsafe methods'},
            'bffWebSession': {'type': 'apiKey', 'in': 'cookie', 'name': '__Host-ge_web', 'description': 'BFF-web session cookie for portal users (R16, R17, R21)'},
            'apiKey': {'type': 'http', 'scheme': 'bearer', 'description': 'Developer-platform API key gek_<env>_<prefix>_<secret> (DEC-785, API-V12-R-019)'},
            'oauth2ClientCredentials': {'type': 'oauth2', 'flows': {'clientCredentials': {'tokenUrl': '/oauth/token', 'scopes': {}}}},
            'oauthClientAuth': {'type': 'http', 'scheme': 'basic', 'description': 'OAuth client authentication at the token endpoint'},
            'scimBearer': {'type': 'http', 'scheme': 'bearer', 'description': 'Per-tenant SCIM token (hash stored only; ≤ 397 days)'},
            'webhookSignature': {'type': 'apiKey', 'in': 'header', 'name': 'X-Signature', 'description': 'Provider HMAC/JWS signature; timestamp + nonce replay window 5 min'},
            'workloadIdentity': {'type': 'mutualTLS', 'description': 'IAM-signed request or mTLS for internal callers (R19, R20)'},
        },
    },
    'x-websockets': [{'id': e[0], 'path': e[2].strip('`'), 'note': e[3]} for e in excluded],
}

write(OUT + 'openapi.yaml', yaml.safe_dump(spec, sort_keys=False, allow_unicode=True, width=200))

# index CSV and stats
with open(OUT + 'api_index.csv', 'w', newline='', encoding='utf-8') as fh:
    w = csv.writer(fh)
    w.writerow(['operationId', 'method', 'path', 'namespace', 'tag', 'source_part', 'side_effect', 'pdp', 'rate_limit', 'baseline', 'also_defined_as', 'summary'])
    for r in merged.values():
        w.writerow([r['operationId'], r['method'], r['path'], clean(r.get('ns')), clean(r.get('tag')), r['part'], r.get('se', ''),
                    clean(r.get('pdp')), clean(r.get('rl')), 'yes' if r.get('baseline') else 'no', ';'.join(r['also']), clean(r.get('purpose'))[:160]])

by_part_rows = collections.Counter(r['part'] for r in rows)
by_part_ops = collections.Counter(r['part'] for r in merged.values())
ids = collections.Counter(re.sub(r'(\.\d+)?$', '', r['src_id']) for r in rows)
stats = dict(
    rows_harvested=len(rows), unique_operations=len(merged), paths=len(paths), tags=len(tags),
    duplicates_merged=len(rows) - len(merged), excluded=len(excluded), unparsed=unparsed,
    by_part_rows=dict(by_part_rows), by_part_ops=dict(by_part_ops),
    by_method=dict(collections.Counter(r['method'] for r in merged.values())),
    by_ns=dict(collections.Counter((clean(r.get('ns')) or '?') for r in merged.values())),
    baseline_ids=len({r['src_id'] for r in rows if r.get('baseline')}),
    w_ids_assigned=wseq,
    families={fam: len({r['src_id'] for r in rows if r['src_id'].startswith(fam)}) for fam in
              ('API-0', 'API-1', 'API-2', 'API-3', 'API-4', 'API-5', 'API-ENH-D', 'API-ADV-X1', 'API-V12-H', 'API-V12-M', 'API-V12-N', 'API-V12-Q', 'API-V12-R', 'API-V12-W')},
    tag_counts=dict(tags),
)
save_json('openapi_stats.json', stats)
save_json('openapi_rows.json', [{k: v for k, v in r.items()} for r in merged.values()])
print(json.dumps({k: v for k, v in stats.items() if k not in ('tag_counts',)}, indent=1, ensure_ascii=False))
