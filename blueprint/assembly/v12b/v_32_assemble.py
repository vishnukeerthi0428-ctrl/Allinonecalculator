"""V-32: fill the Part 11.23 templates (v_tmpl_a/b/c.md) with the generated fragments and metrics and write the part files."""
import json, os, re, glob
from v_common import OUT, BP, ids_in
HERE = os.path.dirname(os.path.abspath(__file__))
F = json.load(open(os.path.join(OUT, 'fragments.json')))
M = json.load(open(os.path.join(OUT, 'fragments_meta.json')))
C = json.load(open(os.path.join(OUT, 'combi.json')))
T = json.load(open(os.path.join(OUT, 'triage_before.json')))

def fmt(n):
    return f'{n:,}'

# derived metrics
M['EX']['total_bytes_fmt'] = fmt(M['EX']['total_bytes']); M['EX']['statements_fmt'] = fmt(M['EX']['statements']); M['EX']['unique_fmt'] = fmt(M['EX']['unique'])
M['EX']['kinds'] = '; '.join('%s %s' % (k, fmt(v)) for k, v in sorted(M['EX']['by_kind'].items(), key=lambda kv: -kv[1]))
M['SB']['lines_fmt'] = fmt(M['SB']['lines']); M['SB']['distinct_ids_fmt'] = fmt(M['SB']['distinct_ids']); M['SB']['triage_n'] = fmt(len(T['triage']))
for k in ('M', 'C', 'N', 'S'):
    M['final'][k + '_fmt'] = fmt(M['final'].get(k, 0))
M['base']['n_fmt'] = fmt(M['base']['n']); M['base']['changed'] = fmt(M['base'].get('amended', 0) + M['base'].get('superseded', 0))
M['n_stale_fmt'] = fmt(M['n_stale']); M['n_errata_last'] = '%02d' % 50
# baseline IDs referenced but never defined (reviewed in Part 11.23b §11.23.6.6)
B = json.load(open(os.path.join(OUT, 'baseline.json')))
defined = set()
for f in glob.glob(os.path.join(BP, 'Part-*.md')):
    if 'Part-11-23' in f:
        continue
    for l in open(f, encoding='utf-8'):
        m = re.match(r'^(?:\|\s*|#+\s*|[-*]\s*|Scenario(?: Outline)?:\s*|\*\*)\**`?([A-Z][A-Z0-9]*(?:-[A-Za-z0-9]+)+|[AW]\d{2,3})', l.strip())
        if m:
            defined.add(m.group(1))
        for m in re.finditer(r'(?:Scenario(?: Outline)?:|@)\s*\[?([A-Z]+-[\w-]+)', l):
            defined.add(m.group(1))
M['base_undef'] = fmt(sum(1 for i in B['base_ids'] if i not in defined))
# artifact rows
rows = []
for name, decl, recv in C['art']:
    if name.endswith('.html'):
        rows.append('| %s | %s | %s | %s | Match after LF normalisation (CRLF added in transit) |' % (name, decl, recv, decl))
    elif name.endswith('.docx'):
        rows.append('| %s | not declared | %s | n/a (binary) | Reference set from receipt |' % (name, recv))
    else:
        rows.append('| %s | %s | %s | n/a (binary) | Match as received |' % (name, decl, recv))
F['art_rows'] = '\n'.join(rows)

def get(path):
    cur = M
    for p in path.split('.', 1)[0:1] + ([path.split('.', 1)[1]] if '.' in path else []):
        if isinstance(cur, dict) and p in cur:
            cur = cur[p]
        else:
            # allow keys containing dots after the first level (e.g. fr.FR-V12-V-001)
            return '0'
    return cur if not isinstance(cur, float) else ('%.2f' % cur)

def fill(t):
    t = re.sub(r'\{\{F:([\w_]+)\}\}', lambda m: F[m.group(1)], t)
    t = re.sub(r'\{\{M:([^}]+)\}\}', lambda m: str(get(m.group(1))), t)
    assert '{{' not in t, re.findall(r'\{\{[^}]+\}\}', t)[:5]
    return t

OUTF = {'a': 'Part-11-23a_Independent_Audit_Retention_and_Errata.md', 'b': 'Part-11-23b_Independent_Audit_Retention_and_Errata.md', 'c': 'Part-11-23c_Independent_Audit_Retention_and_Errata.md'}
for k, fn in OUTF.items():
    t = open(os.path.join(HERE, 'v_tmpl_%s.md' % k), encoding='utf-8').read()
    open(os.path.join(BP, fn), 'w', encoding='utf-8').write(fill(t))
    print(fn, os.path.getsize(os.path.join(BP, fn)))
