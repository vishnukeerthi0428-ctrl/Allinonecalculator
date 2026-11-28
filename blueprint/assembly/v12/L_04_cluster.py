"""Index IDs to their V12-normative and blueprint locations, attach provenance (originating register)
to every residual/partial unit, and cluster residual units into families and gap templates.

Outputs:
  OUT/idx_v12.json   ID -> first V12 normative location "BRD|FSD NN_file :: heading"
  OUT/idx_bp.json    ID -> first blueprint location "Part-xx :: heading"
  OUT/residual.jsonl residual requirement-like units with family + template + V12/BP anchors
  OUT/families.tsv   family, count, sample
"""
import glob, json, os, re, sys, collections
sys.path.insert(0, os.path.dirname(__file__))
from L_common import *

idx_v12, idx_bp = {}, {}
for f in sorted(glob.glob(V12 + '/BRD/*.txt') + glob.glob(V12 + '/FSD/*.txt')):
    b = os.path.basename(f)
    if b.startswith('ZZ_'):
        continue
    h = ''
    for line in open(f, encoding='utf-8', errors='replace'):
        m = HEAD.match(line)
        if m:
            h = HEAD.sub('', line).strip()[:90]
        for i in ID_RE.findall(line):
            idx_v12.setdefault(i, f"{os.path.basename(os.path.dirname(f))} {b[:-4]} :: {h}")
for f in sorted(glob.glob(BP + '/Part-0*.md')):  # v1.1 baseline only
    b = os.path.basename(f)[:-3]
    h = ''
    for line in open(f, encoding='utf-8', errors='replace'):
        if line.startswith('#'):
            h = line.strip('# \n')[:90]
        for i in ID_RE.findall(line):
            idx_bp.setdefault(i, f'{b} :: {h}')
json.dump(idx_v12, open(OUT + '/idx_v12.json', 'w'))
json.dump(idx_bp, open(OUT + '/idx_bp.json', 'w'))


def family(u):
    s, h, f = u['src'], u['heading'], u['file']
    if s in ('ANX-BRD', 'ANX-FSD', 'V1-BRD', 'V1-FSD'):
        h2 = re.sub(r'\b[A-Z][A-Z0-9]{0,9}(?:-[A-Z0-9]{1,12}){1,5}\b', '<ID>', h)
        m = re.search(r'\.xlsx / (.*)', h2)
        if m:  # keep the worksheet tab, normalised to the CSV twin name (e.g. 10_Development_Tasks)
            return f'{s[:3]}::' + h2[:m.start()] + '.xlsx/' + m.group(1).strip().replace(' ', '_')
        return f'{s[:3]}::{h2[:70]}'
    return f'{s}::{os.path.basename(f)}'


def tpl(s):
    s = ID_RE.sub('<ID>', s)
    s = re.sub(r'\d+(\.\d+)?', '<N>', s)
    s = re.sub(r'\{[^}]*\}', '{..}', s)
    return re.sub(r'\s+', ' ', s.lower())[:140]


fam = collections.Counter()
samp = {}
with open(OUT + '/compared.jsonl') as fi, open(OUT + '/residual.jsonl', 'w') as fo:
    for line in fi:
        u = json.loads(line)
        if u['band'] != 'RESIDUAL' or not u['req']:
            continue
        u['family'] = family(u)
        u['tpl'] = tpl(' ; '.join(u['gaps']) if u['gaps'] else u['text'])
        u['v12_anchor'] = next((idx_v12[i] for i in u['ids'] if i in idx_v12), '')
        u['bp_anchor'] = next((idx_bp[i] for i in u['ids'] if i in idx_bp), '')
        u['ids_in_v12'] = sum(1 for i in u['ids'] if i in idx_v12)
        fam[u['family']] += 1
        samp.setdefault(u['family'], u['text'][:200])
        fo.write(json.dumps(u, ensure_ascii=False) + '\n')
with open(OUT + '/families.tsv', 'w') as ff:
    for k, v in fam.most_common():
        ff.write(f'{k}\t{v}\t{samp[k]}\n')
print('families', len(fam), 'residual', sum(fam.values()), 'v12 ids', len(idx_v12), 'bp ids', len(idx_bp))
