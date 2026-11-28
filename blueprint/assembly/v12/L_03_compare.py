"""Compare every unique L unit against R1 (38 docs + coverage), R2 (V12 normative), R3 (blueprint).

Two metrics are computed.
 (1) Unit metric -- share of the unit's 6-gram shingles found in R1 / R2 / R3 / union (c1,c2,c3,cu).
 (2) Field metric -- the annex and the source registers render rows as "Label: value  .  Label: value"
     (annex) or "v1 | v2 | ..." (CSV / JSON), so labels break shingles. The unit is split into fields
     (on ' • ', ' | ', ';'), a leading "label:" is removed, and each value is tested:
       value >= 6 tokens : share of its 6-gram shingles in the union of references
       value 1..5 tokens : 1 if the exact contiguous n-gram occurs in any reference (or, for a value
                           that is only IDs, every ID occurs in a reference ID set), else 0
     fu = token-weighted mean over values. Values that are pure workflow status words
     (Pending, Not started, Yes/No, Draft ...) or evidence paths are ignored (not requirements).
Final coverage cf = max(cu, fu).
Band: MATCH cf >= 0.80 ; PARTIAL 0.40 <= cf < 0.80 ; RESIDUAL cf < 0.40.
The uncovered values (value coverage < 0.5) are kept in 'gaps' for clustering and reading.
Output: OUT/compared.jsonl
"""
import json, os, pickle, re, sys
sys.path.insert(0, os.path.dirname(__file__))
from L_common import *

assert os.environ.get('PYTHONHASHSEED') == '0'
refs = pickle.load(open(OUT + '/refs.pkl', 'rb'))
R = [refs[r] for r in ('R1', 'R2', 'R3')]
allids = R[0]['ids'] | R[1]['ids'] | R[2]['ids']
SPLIT = re.compile(r'\s+•\s+|\s+\|\s+|;\s+')
LABEL = re.compile(r'^[A-Za-z][\w /()&.,%\-–]{0,48}:\s+(?=\S)')
NOISE = re.compile(r'^(pending|not started|not executed|open|yes|no|true|false|draft|proposed|candidate|n/?a|none|tbd|'
                   r'approved|blocked|in progress|pass|fail|passed|failed|retained|historical|unverified|'
                   r'evidence/\S+|\S+\.(json|csv|md|txt|png|pdf|html|log|sql|py)|\d+(\.\d+)?|0|-)$', re.I)


def cov_tokens(t):
    if len(t) >= N:
        s = shingles(t)
        hit = [x in R[0]['sh'] or x in R[1]['sh'] or x in R[2]['sh'] for x in s]
        return sum(hit) / len(s)
    h = hash(' '.join(t))
    return 1.0 if any(h in r['small'] for r in R) else 0.0


bands = {}
with open(OUT + '/unique.jsonl') as fi, open(OUT + '/compared.jsonl', 'w') as fo:
    for line in fi:
        u = json.loads(line)
        t = u['key'].split()
        if len(t) >= N:
            s = shingles(t)
            c = [len(s & r['sh']) / len(s) for r in R]
            cu = sum(1 for x in s if x in R[0]['sh'] or x in R[1]['sh'] or x in R[2]['sh']) / len(s)
        else:
            h = hash(' '.join(t))
            c = [1.0 if h in r['small'] else 0.0 for r in R]
            cu = max(c)
        # field metric
        tw, tc, gaps = 0, 0.0, []
        for raw in SPLIT.split(u['text']):
            v = LABEL.sub('', raw.strip())
            if not v or NOISE.match(v.strip()):
                continue
            vt = toks(v)
            if not vt:
                continue
            vids = ID_RE.findall(v)
            if vids and len(vt) <= 2 * len(vids) + 1:  # ID-only value
                cv = sum(1 for i in vids if i in allids) / len(vids)
            else:
                cv = cov_tokens(vt)
            tw += len(vt)
            tc += cv * len(vt)
            if cv < 0.5:
                gaps.append(v[:400])
        fu = tc / tw if tw else 1.0
        ids = sorted(set(ID_RE.findall(u['text'])))
        u['c1'], u['c2'], u['c3'] = (round(x, 3) for x in c)
        u['cu'] = round(cu, 3)
        u['fu'] = round(fu, 3)
        cf = max(cu, fu)
        u['cf'] = round(cf, 3)
        u['gaps'] = gaps
        u['ids'] = ids
        u['idmiss'] = [i for i in ids if i not in allids]
        u['band'] = 'MATCH' if cf >= 0.8 else ('PARTIAL' if cf >= 0.4 else 'RESIDUAL')
        k = (u['src'], bool(u['req']), u['band'])
        bands[k] = bands.get(k, 0) + 1
        fo.write(json.dumps(u, ensure_ascii=False) + '\n')
for k in sorted(bands):
    print(*k, bands[k], sep='\t')
