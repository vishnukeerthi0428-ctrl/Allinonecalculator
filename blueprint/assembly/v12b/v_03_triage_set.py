"""V-03: build the triage set (weak/none matches, threshold misses, statements carrying an ID absent from the blueprint)
and cluster it into templates so every member is read with its context."""
import json, os, re
from collections import defaultdict, Counter
from v_common import OUT
S = {x['sid']: x for x in json.load(open(os.path.join(OUT, 'statements.json')))}
R = json.load(open(os.path.join(OUT, 'match_before.json')))

def sig(t):
    x = t['text']
    x = re.sub(r'[A-Z][A-Z0-9]*(?:-[A-Za-z0-9]+)+', '<ID>', x)
    x = re.sub(r'\b[AW]\d{2,3}\b', '<SCR>', x)
    x = re.sub(r'\d+(\.\d+)?', '<N>', x)
    x = re.sub(r'\b[0-9a-f]{12,}\b', '<HASH>', x)
    if t['kind'] == 'ddl':
        m = re.match(r'(CREATE \w+|ALTER TABLE|INSERT INTO|CREATE UNIQUE INDEX|CREATE INDEX)', t['text'])
        x = (m.group(1) if m else 'SQL') + (' POLICY tenant' if 'current_setting' in t['text'] and 'POLICY' in t['text'] else '')
    sec = t['sec'].split(' > ')
    sec = sec[1] if len(sec) > 1 else sec[0]
    sec = re.sub(r'[A-Z][A-Z0-9]*(?:-[A-Za-z0-9]+)+|\b[AW]\d{3}\b', '<ID>', sec)
    sec = re.sub(r'\d+', '<N>', sec)
    head = ' | '.join(x.split(' | ')[:2])[:90]
    return t['chapter'] + ' :: ' + sec[:70] + ' :: ' + head

def main():
    tri = []
    for r in R:
        why = []
        if r['level'] in ('weak', 'none'):
            why.append('weak-match')
        if r['num'] is not None and r['num'] < 1:
            why.append('threshold-miss')
        if r['missing_ids']:
            why.append('id-missing')
        if why:
            tri.append(dict(sid=r['sid'], why=why, level=r['level'], tok=r['tok'], ng=r['ng'], num=r['num'], missing_ids=r['missing_ids'], loc=r['loc']))
    cl = defaultdict(list)
    for t in tri:
        cl[sig(S[t['sid']])].append(t['sid'])
    clusters = []
    for k, v in sorted(cl.items(), key=lambda kv: (-len(kv[1]), kv[0])):
        clusters.append(dict(cid='VC-%03d' % (len(clusters) + 1), sig=k, n=len(v), sids=v))
    json.dump(dict(triage=tri, clusters=clusters), open(os.path.join(OUT, 'triage_before.json'), 'w'), indent=0)
    print(len(tri), 'statements in triage;', len(clusters), 'clusters;', Counter(w for t in tri for w in t['why']))

if __name__ == '__main__':
    main()
