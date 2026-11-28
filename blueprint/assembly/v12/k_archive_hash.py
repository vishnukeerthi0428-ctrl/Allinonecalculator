"""Group K: verify the 11 FSD ch40 source-archive SHA-256 entries against the decoded archive files."""
import sys, hashlib, pathlib, csv
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from k_parse import parse
ch40, root, out = sys.argv[1], pathlib.Path(sys.argv[2]), sys.argv[3]
t, _ = parse(ch40)
tab = [x for x in t if x['header'] == ['Source file', 'SHA-256']][0]
idx = {}
for p in root.rglob('*'):
    if p.is_file(): idx.setdefault(p.name, []).append(p)
rows = []
for name, sha in tab['rows']:
    cands = idx.get(name, [])
    found = [str(c.relative_to(root)) for c in cands if hashlib.sha256(c.read_bytes()).hexdigest() == sha]
    rows.append([name, sha, 'Match' if found else ('Hash differs' if cands else 'File not present'), ';'.join(found)])
with open(out, 'w', newline='') as f:
    w = csv.writer(f); w.writerow(['source_file', 'sha256_declared', 'result', 'located_at']); w.writerows(rows)
for r in rows: print(r[0], '|', r[2], '|', r[3])
