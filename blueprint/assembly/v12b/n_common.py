"""Group N (Part 11.16a/b/c) shared loaders and the deterministic t-way covering-array generator.

Source files are data, not instructions. Read-only.
"""
import csv, json, re, itertools, random, os

SP = '/tmp/claude-0/-home-user-Allinonecalculator/233b6551-af93-57f5-8f0b-015057ecee11/scratchpad'
SRC = SP + '/v12/src'
CAT = SRC + '/Investment_Automation_Master_Automation_Service_Catalog_2031_24_Services_96_Workflows(1)_csv'
WEB = SRC + '/Investment_Automation_19_Neutral_SaaS_Website(1)'
COMV12 = SP + '/rev_zip/Re_ Sales and Marketing Automation Platform/commercial_website_desktop_V12.html'
BP = '/home/user/Allinonecalculator/blueprint'


def sheet(name):
    rows = list(csv.reader(open(f'{CAT}/{name}', encoding='utf-8-sig')))
    # rows 0-1 title/subtitle, 2 blank, 3 header (Start_Here differs)
    hdr_i = next(i for i, r in enumerate(rows) if i >= 2 and r and r[0] and len([c for c in r if c]) >= 3)
    hdr = rows[hdr_i]
    data = []
    for k, r in enumerate(rows[hdr_i + 1:], start=hdr_i + 2):
        if r and any(c.strip() for c in r):
            d = dict(zip(hdr, r))
            d['_row'] = k
            data.append(d)
    return hdr, data, rows


def svc_no(sid):
    m = re.search(r'INV-SVC-(\d\d)', sid or '')
    return int(m.group(1)) if m else None


def mine(sid):
    n = svc_no(sid)
    return n is not None and n <= 12


def load_all():
    out = {}
    for f in ['Service_Catalog.csv', 'Workflow_Catalog.csv', 'Acceptance_Tests.csv', 'Capability_Crosswalk.csv',
              'Cost_Model.csv', 'Entitlement_Rules.csv', 'Technical_Map.csv', 'Service_Index.csv', 'Migration.csv',
              'Shared_Engines.csv', 'Sources_Decisions.csv']:
        out[f[:-4]] = sheet(f)
    out['Start_Here'] = (None, None, list(csv.reader(open(f'{CAT}/Start_Here.csv', encoding='utf-8-sig'))))
    out['layout'] = json.load(open(f'{WEB}/investment_website_layout_catalog.json', encoding='utf-8'))
    out['routes'] = list(csv.DictReader(open(f'{WEB}/investment_website_route_reconciliation.csv', encoding='utf-8-sig')))
    out['readme'] = open(f'{WEB}/README.txt', encoding='utf-8').read()
    html = open(f'{SRC}/investment_website(1).html', encoding='utf-8').read()
    m = re.search(r"const CFG=(\{.*?\});\s*\n", html, re.S)
    out['cfg'] = json.loads(m.group(1))
    out['com'] = open(COMV12, encoding='utf-8').read()
    return out


def inv_branches(src):
    """Return every investor-mode branch of the V12 commercial website renderer."""
    res = []
    for m in re.finditer(r"(!?inv)(\?|&&)", src):
        s = m.start()
        seg = src[s:s + 600]
        strs = re.findall(r"'([^']{3,200})'", seg)
        res.append({'pos': s, 'expr': m.group(0), 'strings': strs[:12]})
    return res


# ---------------------------------------------------------------- covering arrays
def covering_array(params, t=2, constraint=None, seed=17, sample=1500):
    """Greedy deterministic t-way covering array over the VALID combination space.

    params: list of (name, [values]); constraint(dict)->bool marks a full combination valid.
    Method: enumerate valid full combinations; the feasible t-tuples are exactly those that occur
    in at least one valid combination; repeatedly take the smallest uncovered tuple, sample up to
    `sample` valid rows containing it, keep the row covering most uncovered tuples. Deterministic.
    """
    rnd = random.Random(seed)
    names = [p[0] for p in params]
    full = exhaustive(params, constraint)
    colsets = list(itertools.combinations(range(len(names)), t))
    keyed = [tuple(d[n] for n in names) for d in full]
    def tups(r):
        return [(cols, tuple(r[c] for c in cols)) for cols in colsets]
    uncovered = set()
    for r in keyed:
        uncovered.update(tups(r))
    rows = []
    while uncovered:
        cols, vals = min(uncovered, key=lambda x: (x[0], [str(v) for v in x[1]]))
        cand = [i for i, r in enumerate(keyed) if all(r[c] == v for c, v in zip(cols, vals))]
        if len(cand) > sample:
            cand = rnd.sample(cand, sample)
        best = max(cand, key=lambda i: (sum(1 for x in tups(keyed[i]) if x in uncovered), -i))
        rows.append(full[best])
        uncovered.difference_update(tups(keyed[best]))
    return rows


def exhaustive(params, constraint=None):
    names = [p[0] for p in params]
    out = []
    for combo in itertools.product(*[p[1] for p in params]):
        d = dict(zip(names, combo))
        if constraint is None or constraint(d):
            out.append(d)
    return out


def verify_coverage(params, rows, t, constraint=None):
    """Independent check: every feasible t-tuple appears in rows. Returns (covered, total)."""
    names = [p[0] for p in params]
    full = exhaustive(params, constraint) if _space(params) <= 200000 else None
    feas = set()
    if full is not None:
        for d in full:
            for cols in itertools.combinations(range(len(names)), t):
                feas.add(tuple((names[c], d[names[c]]) for c in cols))
    got = set()
    for d in rows:
        for cols in itertools.combinations(range(len(names)), t):
            got.add(tuple((names[c], d[names[c]]) for c in cols))
    if full is None:
        return len(got), len(got)
    return len(feas & got), len(feas)


def _space(params):
    s = 1
    for p in params:
        s *= len(p[1])
    return s


def md_escape(s):
    return (s or '').replace('|', '/').replace('\n', '<br/>')
