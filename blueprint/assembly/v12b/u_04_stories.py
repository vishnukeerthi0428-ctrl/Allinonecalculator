#!/usr/bin/env python3
"""Part 11.22 (Group U): normalise target FRs and group them into new stories.

Target FRs = FRs with no story (u_01 'uncovered') + FRs whose only stories carry
no acceptance criteria (u_01 'no_ac'). Each target FR is normalised from its
register row (header-driven), assigned an epic, a domain (-> parameter model),
a release bucket, then grouped into stories US-<EP>-ZU<nn>.
Imported by u_05_build.py.
"""
import json, re, collections

TOK_RE = re.compile(r'\b(ENT-[A-Z]{3}-\d{2}|AIX-\d{2}|CTRL-AI-\d{2}|MT-API-\d{2}|MT-\d{2}|GC-\d{2}|CJ-R\d{2}|REC-\d{2}|SEC-\d{2}|MOB-\d{2}|RT-\d{2}|CS-\d{2}|AT-\d{2}|OPT-API-\d{2}|INV-SVC-\d{2}(?:-WF0\d)?|SM-SVC-\d{2}|SEC-CTL-N-\d{2}|PERF-\d{2}|FL-\d{2}|CV-\d{2}|BR-C\d{2})\b')

def clean(s):
    s = (s or '').replace('\\|', '/').replace('|', '/')
    s = re.sub(r'\*\*', '', s)
    s = re.sub(r'\s+', ' ', s).strip()
    return s

HMAP = [
    ('req', ('requirement', 'requirement (v12 literal)', 'capability (v12)', 'business requirement (literal)',
             'field family — add or standardize (literal)')),
    ('label', ('rule (source id)',)),
    ('source', ('v12 source', 'source', 'source (v12)', 'ent', 'br', 'trace', 'source id')),
    ('accept', ('rule / acceptance', 'acceptance', 'acceptance (positive)', 'v12 acceptance', 'test intent',
                'acceptance evidence (literal)', 'automation behaviour (literal)')),
    ('neg', ('negative / boundary', 'remove / hide / condition (literal)')),
    ('pri', ('priority', 'pri', 'moscow')),
    ('release', ('release', 'wave', 'wave / release', 'release / epic', 'release (v12 phase → wave)',
                 'v12 phase → release', 'release (assumption-940)', 'proposed release', 'release · epic')),
    ('epiccol', ('epic',)),
    ('tests', ('test', 'tests', 'tc')),
    ('impl', ('implemented by', 'realised by', 'design depth', 'package', 'blueprint capability',
              'existing blueprint coverage', 'items', 'delta specified here', 'strengthening adopted (dec-723)', 'gap added')),
]

def normalise(fr, inv):
    df = inv['fr'][fr]['def'] or {}
    rec = {'id': fr, 'letter': fr.split('-')[2], 'num': int(fr.split('-')[3]), 'file': df.get('file', ''),
           'line': df.get('line', 0), 'section': clean(df.get('section', ''))}
    cells, header = df.get('cells'), df.get('header') or []
    if cells:
        for h, c in zip(header, cells):
            h = h.strip('* ').lower()
            for key, names in HMAP:
                if h in names and key not in rec:
                    rec[key] = clean(c)
        if 'req' not in rec and len(cells) > 1:
            rec['req'] = clean(cells[1])
        rec['allcells'] = ' '.join(cells)
    else:
        para = df.get('para', '')
        rec['req'] = ''
        fields = dict(re.findall(r'^\|\s*([^|]+?)\s*\|\s*(.+?)\s*\|\s*$', para, flags=re.M))
        rec['wf'] = {clean(k): clean(v) for k, v in fields.items() if k.strip() not in ('Field', '---')}
        bo = rec['wf'].get('Business outcome / input → output', '')
        rec['req'] = bo
        rec['accept'] = rec['wf'].get('Result / acceptance', '')
        rec['impl'] = clean(re.sub(r'^.*?\*\*Blueprint:\*\*', '', para.split('\n')[0]))
        rec['allcells'] = para
    # label: bold prefix or first clause
    raw = (df.get('cells') or ['', ''])[1] if df.get('cells') else ''
    m = re.match(r'\s*\*\*(.+?)\*\*', raw or '')
    if 'label' in rec and rec['label']:
        pass
    elif m:
        rec['label'] = clean(m.group(1))
    elif rec['letter'] == 'O' and rec.get('wf'):
        rec['label'] = re.sub(r'^INV-SVC-\d{2}-WF0\d\s*', '', rec['section'])
    else:
        rec['label'] = short(rec.get('req', ''), 70)
    m = re.search(r'\b(EP-\d{2})\b', (rec.get('epiccol') or '') + ' ' + (rec.get('release') or ''))
    rec['epic'] = m.group(1) if m else ''
    rec['tokens'] = sorted(set(TOK_RE.findall(rec.get('allcells', '') + ' ' + rec.get('section', ''))))
    tc = re.findall(r'TC-V12-[A-Z]-\d{3}[a-z]?|TC-\d{3}', rec.get('allcells', ''))
    rec['tcs'] = sorted(set(tc))[:6]
    return rec

def short(s, n):
    s = clean(s)
    if len(s) <= n:
        return s
    cut = s[:n]
    for sep in ('; ', ', ', ' – ', ' ('):
        i = cut.rfind(sep)
        if i > n * 0.55:
            return cut[:i]
    return cut.rsplit(' ', 1)[0] + '…'

# --------------------------------------------------------------- epic fallback
def assign_epic(rec, anchor):
    if anchor:
        return 'EP-' + anchor.split('-')[1]
    if rec['epic']:
        return rec['epic']
    L, n, sec = rec['letter'], rec['num'], rec['section']
    if L == 'O':
        m = re.search(r'INV-SVC-(\d{2})', sec)
        svc = int(m.group(1)) if m else 0
        if n <= 20 or 13 <= svc <= 16:
            return 'EP-32'
        return 'EP-33'
    if L == 'N':
        return 'EP-30' if n in (21, 23) else 'EP-31'
    if L == 'D':
        return 'EP-18'
    if L == 'H':
        return {8: 'EP-20', 9: 'EP-20', 10: 'EP-20', 13: 'EP-03', 14: 'EP-20', 15: 'EP-17', 16: 'EP-01', 17: 'EP-04',
                19: 'EP-18', 20: 'EP-18', 21: 'EP-18', 24: 'EP-08', 25: 'EP-08', 26: 'EP-18', 27: 'EP-18', 28: 'EP-20',
                29: 'EP-20', 30: 'EP-20', 31: 'EP-21', 32: 'EP-21', 33: 'EP-03', 34: 'EP-20', 38: 'EP-01', 39: 'EP-20',
                40: 'EP-20', 41: 'EP-20'}.get(n, 'EP-20')
    if L == 'I':
        if n in (8, 9, 13, 25, 26): return 'EP-01'
        if n in (22, 24): return 'EP-20'
        if n == 16: return 'EP-04'
        if n in (41, 53, 54, 55, 56, 58): return 'EP-21'
        if n == 43: return 'EP-17'
        if n == 45: return 'EP-12'
        if n == 59: return 'EP-19'
        return 'EP-01'
    if L == 'K':
        ent = (rec.get('source') or '')
        fam = ent[4:7] if ent.startswith('ENT-') else ''
        if fam in ('IDN', 'ACC'): return 'EP-01'
        if fam == 'API': return 'EP-20'
        if fam == 'INT': return 'EP-18'
        if fam == 'DAT': return 'EP-01' if ent in ('ENT-DAT-02', 'ENT-DAT-03') else 'EP-20'
        if fam == 'SEC': return 'EP-21'
        if fam == 'CMP': return 'EP-34' if ent in ('ENT-CMP-01', 'ENT-CMP-02', 'ENT-CMP-03') else 'EP-03'
        if fam == 'GLB': return 'EP-34'
        if fam == 'BIZ': return {'ENT-BIZ-04': 'EP-16', 'ENT-BIZ-05': 'EP-16'}.get(ent, 'EP-20')
        return 'EP-21'
    if L == 'E':
        return 'EP-18'
    if L == 'J':
        return 'EP-21'
    return 'EP-21'

# --------------------------------------------------------------- domain
def domain(rec, epic):
    L, n = rec['letter'], rec['num']
    txt = (rec.get('label', '') + ' ' + rec.get('req', '')).lower()
    if L == 'O' and rec.get('wf'):
        return 'INVWF'
    if L in ('N', 'O'):
        return 'INV'
    if L == 'K' and (rec.get('source') or '').startswith('ENT-'):
        fam = rec['source'][4:7]
        return {'IDN': 'IAM', 'ACC': 'IAM', 'API': 'API', 'INT': 'API', 'DAT': 'DATA', 'SEC': 'OPS', 'OPS': 'OPS',
                'GLB': 'GLB', 'BIZ': 'COM'}.get(fam, 'LEGAL' if fam == 'CMP' and rec['source'] >= 'ENT-CMP-04' else 'GLB')
    if L == 'F':
        if n in range(42, 48): return 'LEGAL'
        if n in (40, 41, 48): return 'RUN'
        return 'AI'
    if L in ('D', 'J') or (L == 'E' and epic == 'EP-18'):
        return 'RUN' if L != 'J' else 'OPS'
    if L == 'H':
        if n in (13, 33): return 'LEGAL'
        if n == 15: return 'ANL'
        if n in (16, 38): return 'IAM'
        if n == 40: return 'DATA'
        return 'API'
    if L == 'I':
        if n == 8: return 'IAM'
        if n in (41, 53, 54, 55, 56, 58): return 'OPS'
        if n in (43, 45): return 'ANL'
        if n == 59: return 'WEB'
        if n == 16: return 'AI'
        return 'DATA'
    if L == 'L':
        return 'WEB' if re.search(r'public|portal|website|visitor', txt) else 'ANL'
    if L == 'M':
        return 'AI'
    if L == 'E':
        return {'EP-01': 'IAM', 'EP-20': 'COM', 'EP-15': 'COM', 'EP-21': 'OPS', 'EP-03': 'LEGAL'}.get(epic, 'RUN')
    if L == 'A' and n in A_DOMAIN:
        return A_DOMAIN[n]
    if L == 'K':
        return 'OPS' if n != 14 else 'COM'
    if re.search(r'\bai\b|context budget|step inventory|\bllm\b|prompt', txt): return 'AI'
    if re.search(r'status page|recovery|\brpo\b|\brto\b|release gate|phase map|priority gating|decision ownership|sla|incident|sev', txt): return 'OPS'
    if re.search(r'perspective|metric|kpi|dashboard|command centre|drill|filter|currency|denominator', txt): return 'ANL'
    if re.search(r'pric|billing|invoice|quote|bundle|sku|subscription|lifecycle|consumption|tco|cost|dispute|meter|plan|entitlement|ledger|tax|cancel', txt): return 'COM'
    if re.search(r'pack|consent|grievance|legal|counsel|dsar|privacy', txt): return 'LEGAL'
    if re.search(r'identity|sso|scim|role|portfolio grant|tenant per|company', txt): return 'IAM'
    return 'WEB'

A_DOMAIN = {4: 'COM', 5: 'COM', 6: 'IAM', 12: 'COM', 13: 'COM', 15: 'COM', 23: 'API', 24: 'COM', 30: 'COM', 31: 'COM',
            32: 'COM', 33: 'COM', 34: 'COM', 35: 'COM', 36: 'ANL', 54: 'WEB', 58: 'WEB', 59: 'WEB', 60: 'WEB', 61: 'WEB',
            73: 'IAM', 75: 'IAM', 76: 'IAM', 77: 'IAM', 78: 'LEGAL', 79: 'COM', 80: 'COM', 91: 'COM', 92: 'COM', 93: 'IAM',
            94: 'RUN', 95: 'WEB', 113: 'AI', 114: 'AI', 115: 'AI', 116: 'AI', 117: 'AI', 118: 'AI', 121: 'ANL', 122: 'ANL',
            123: 'ANL', 124: 'ANL', 140: 'OPS', 141: 'OPS', 142: 'OPS', 143: 'OPS', 144: 'WEB', 145: 'OPS', 146: 'LEGAL',
            147: 'OPS', 150: 'ANL', 151: 'ANL', 152: 'ANL', 153: 'WEB', 160: 'WEB', 161: 'WEB', 162: 'WEB', 163: 'COM',
            164: 'API', 165: 'WEB', 166: 'WEB', 167: 'COM', 168: 'COM', 169: 'AI', 170: 'WEB',
            **{i: 'OPS' for i in range(180, 193)}, 200: 'OPS', 201: 'OPS', 202: 'OPS', 210: 'OPS', 220: 'ANL', 221: 'ANL', 222: 'WEB'}

DOMAIN_MODEL = {'COM': 'MU01', 'IAM': 'MU02', 'API': 'MU03', 'DATA': 'MU04', 'AI': 'MU05', 'LEGAL': 'MU06',
                'RUN': 'MU07', 'INV': 'MU08', 'INVWF': 'MU09', 'OPS': 'MU10', 'WEB': 'MU11', 'GLB': 'MU12', 'ANL': 'MU13'}

# --------------------------------------------------------------- release
OVERRIDE = {
    # Founder decisions of 28 Nov 2026 that move or confirm a release
    **{f'FR-V12-K-{i}': ('Release 1', 'DEC-784 (SSO/SCIM and enterprise access in Release 1)') for i in range(101, 112)},
    **{f'FR-V12-K-{i}': ('Release 1', 'DEC-785 (developer platform and connectors in Release 1)') for i in list(range(112, 119)) + list(range(124, 129))},
    'FR-V12-H-019': ('Release 1', 'DEC-785'), 'FR-V12-H-020': ('Release 1', 'DEC-785'), 'FR-V12-H-021': ('Release 1', 'DEC-785'),
    'FR-V12-H-026': ('Release 1', 'DEC-785'), 'FR-V12-H-038': ('Release 1', 'DEC-784 (SIEM streaming with enterprise access)'),
    'FR-V12-K-004': ('Release 2', 'DEC-773 (24×7 on-call from Release 2 GA; resolves the DEC-715 pending option)'),
    'FR-V12-K-136': ('Release 2', 'DEC-773 (24×7 security monitoring from Release 2 GA)'),
    'FR-V12-K-137': ('Release 2', 'DEC-775 (SOC 2 Type I at Release 2)'),
    'FR-V12-K-138': ('Release 3+', 'DEC-775 (SOC 2 Type II and ISO/IEC 27001 at R3)'),
    'FR-V12-K-139': ('Release 3+', 'DEC-775 (ISO/IEC 27701 and 42001 at R4)'),
    'FR-V12-K-120': ('Release 3+', 'DEC-776 (BYOK across clouds)'),
    'FR-V12-K-121': ('Release 1', 'DEC-772 and DEC-776 (residency chosen at onboarding from Release 1; EU stack on first EU contract)'),
    'FR-V12-I-013': ('Release 1', 'DEC-772 (EU residency adopted; no longer pending)'),
    'FR-V12-A-147': ('Release 1', 'DEC-771 and DEC-787 (growth RTO ≤ 120 min blocking; RPO ≤ 15 min)'),
    'FR-V12-K-145': ('Release 1', 'DEC-776 (i18n framework is the base for every market)'),
    'FR-V12-K-146': ('Release 2', 'DEC-776 (en/hi Release 2; de/fr R3; ar R4 – one story, staged locales)'),
    'FR-V12-K-147': ('Release 3+', 'DEC-776 (Arabic RTL)'), 'FR-V12-K-152': ('Release 3+', 'DEC-776 (UK, Middle East, APAC, US)'),
    'FR-V12-K-149': ('Release 2', 'DEC-776 (tax engine TX-04…09 per market, adviser approval)'),
    'FR-V12-K-150': ('Release 2', 'DEC-776'), 'FR-V12-K-151': ('Release 2', 'DEC-776'),
    'FR-V12-K-141': ('Release 2', 'DEC-776 (EU DPIA and EU AI Act before EU launch)'),
    'FR-V12-K-133': ('Release 3+', 'ENT-SEC-05 (after R3)'),
}

def release(rec):
    if rec['id'] in OVERRIDE:
        return OVERRIDE[rec['id']]
    s = (rec.get('release') or '').lower()
    if re.search(r'\bw6\b|\br[345]\b|\ba[123]\b|post-w6|future|after r3|r3 →|r4 →', s):
        return ('Release 3+', '')
    if re.search(r'\br2\b|release 2|\bw[45]\b|r2-b|r1–r2', s):
        return ('Release 2', '')
    if re.search(r'\br[01]\b|release 1|\bw[0-3]\b|r1-b|r1–r3', s):
        return ('Release 1', '')
    if rec['letter'] in ('N', 'O'):
        return ('Release 2', 'DEC-783, DEC-770 (Investment Automation in Release 2; activation per counsel-approved pack)')
    return ('Release 2', 'DEC-770, DEC-790 (no release stated; funded change request scheduled in Release 2)')

def priority(rec):
    p = (rec.get('pri') or '').strip()
    if p.startswith('P0') or p.lower().startswith('must'): return 'Must'
    if p.startswith('P1') or p.lower().startswith('should'): return 'Should'
    if p.startswith('P2') or p.lower().startswith('could'): return 'Could'
    if rec['letter'] in ('N', 'O', 'F', 'I', 'D'): return 'Must'
    return 'Should'

# --------------------------------------------------------------- grouping
def family(rec, anchor):
    if anchor:
        return 'anchor:' + anchor
    if rec['letter'] == 'O' and rec.get('wf'):
        m = re.search(r'INV-SVC-(\d{2})', rec['section']); return 'svc:' + (m.group(1) if m else '?')
    if rec['letter'] == 'K' and (rec.get('source') or '').startswith('ENT-'):
        return 'ent:' + rec['source'][4:7]
    return 'sec:' + rec['file'] + '#' + rec['section']

def build(inv):
    targets = [u['fr'] for u in inv['uncovered']] + list(inv['no_ac'])
    status = {f: 'Not covered' for f in (u['fr'] for u in inv['uncovered'])}
    status.update({f: 'Covered without AC' for f in inv['no_ac']})
    recs = {}
    for f in targets:
        anchor = None
        if f in inv['no_ac']:
            anchor = sorted(inv['fr'][f]['stories'])[0]
        r = normalise(f, inv)
        r['anchor'] = anchor
        r['status_before'] = status[f]
        r['epic'] = assign_epic(r, anchor)
        r['domain'] = domain(r, r['epic'])
        r['model'] = DOMAIN_MODEL[r['domain']]
        r['rel'], r['rel_note'] = release(r)
        r['prio'] = priority(r)
        r['family'] = family(r, anchor)
        # related existing stories by shared source tokens
        rel = []
        for u, s in inv['stories'].items():
            if set(s.get('tokens', [])) & set(t for t in r['tokens'] if not t.startswith(('SM-SVC', 'INV-SVC'))):
                rel.append(u)
        if r['letter'] == 'O' and r.get('wf'):
            m = re.search(r'(INV-SVC-\d{2})', r['section'])
            if m:
                rel = [u for u, s in inv['stories'].items() if m.group(1) in s.get('tokens', [])] or rel
        r['related'] = sorted(set(rel))[:6]
        recs[f] = r
    # group
    buckets = collections.OrderedDict()
    for f in sorted(recs, key=lambda x: (recs[x]['epic'], recs[x]['family'], recs[x]['letter'], recs[x]['num'])):
        r = recs[f]
        key = (r['epic'], r['family'])
        buckets.setdefault(key, []).append(f)
    stories = []
    for (epic, fam), frs in buckets.items():
        size = 4 if fam.startswith('svc:') or fam.startswith('anchor:') else 3
        for i in range(0, len(frs), size):
            part = frs[i:i + size]
            model = collections.Counter(recs[f]['model'] for f in part).most_common(1)[0][0]
            stories.append({'epic': epic, 'family': fam, 'model': model, 'frs': part})
    # number per epic
    per = collections.Counter()
    stories.sort(key=lambda s: (s['epic'], recs[s['frs'][0]]['letter'], recs[s['frs'][0]]['num']))
    for s in stories:
        per[s['epic']] += 1
        s['id'] = 'US-%s-ZU%02d' % (s['epic'][3:], per[s['epic']])
        for f in s['frs']:
            recs[f]['story'] = s['id']
    return recs, stories
