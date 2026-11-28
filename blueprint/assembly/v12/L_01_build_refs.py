"""Build the three reference indexes used by the L audit.

R1 = original 38-document pack (docs38/*.txt) + 38-doc coverage registers (final/coverage/*.csv)
R2 = V12 normative chapters (v12/BRD/*.txt and v12/FSD/*.txt excluding ZZ_*)
R3 = blueprint Part-0*.md (v1.1 baseline Parts 0-9.10)

For each reference: 6-gram shingle hash set over the whole token stream, 1..5-gram hash sets
(for short units), the set of ID strings, and token document frequencies.
Output: OUT/refs.pkl
"""
import glob, os, pickle, re, sys
sys.path.insert(0, os.path.dirname(__file__))
from L_common import *

assert os.environ.get('PYTHONHASHSEED') == '0', 'run via L_run_all.sh'


def files_for(ref):
    if ref == 'R1':
        return sorted(glob.glob(DOCS38 + '/*.txt')) + sorted(glob.glob(BP + '/final/coverage/*.csv'))
    if ref == 'R2':
        return sorted(f for f in glob.glob(V12 + '/BRD/*.txt') + glob.glob(V12 + '/FSD/*.txt')
                      if not os.path.basename(f).startswith('ZZ_'))
    if ref == 'R3':
        return sorted(glob.glob(BP + '/Part-0*.md'))  # v1.1 baseline Parts 0-9.10; sibling Part-11 files excluded for determinism


refs = {}
for ref in ('R1', 'R2', 'R3'):
    sh, small, ids = set(), set(), set()
    ntok = 0
    fl = files_for(ref)
    for f in fl:
        txt = open(f, encoding='utf-8', errors='replace').read()
        txt = re.sub(r'<Heading\d>|\[/?TABLE\]|---row', ' ', txt)
        ids.update(ID_RE.findall(txt))
        t = toks(txt)
        ntok += len(t)
        sh |= shingles(t)
        for n in range(1, N):
            for i in range(len(t) - n + 1):
                small.add(hash(' '.join(t[i:i + n])))
    refs[ref] = dict(files=[os.path.relpath(f, SCR) if f.startswith(SCR) else os.path.relpath(f, BP) for f in fl],
                     sh=sh, small=small, ids=ids, ntok=ntok)
    print(ref, len(fl), 'files', ntok, 'tokens', len(sh), 'shingles', len(ids), 'ids', flush=True)

pickle.dump(refs, open(OUT + '/refs.pkl', 'wb'), protocol=4)
