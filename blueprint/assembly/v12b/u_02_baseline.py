#!/usr/bin/env python3
"""Part 11.22 baseline story census (Parts 2-10, i.e. everything before Part 11).

Counts every story defined before V12 (Part 5 US-EEnn stories, source-pack
enhancement stories US-EE-Xnn, advanced stories US-EE-Vnnn) per epic, with its
story points (Fibonacci range) and wave where the story states them.
Usage: python3 -I u_02_baseline.py <blueprint_dir> <out_json>
"""
import glob, json, os, re, sys, collections

BP, OUT = sys.argv[1], sys.argv[2]
files = [p for p in sorted(glob.glob(os.path.join(BP, 'Part-*.md')))
         if not os.path.basename(p).startswith('Part-11')]
ID = r'US-(?:\d{4}|\d{2}-[A-Z][A-Z0-9]?\d{2,3})'
HEAD = re.compile(r'^#{3,6}\s+(' + ID + r')\b\s*(.*)')
ROW = re.compile(r'^\|\s*\**(' + ID + r')\**\s*\|')
stories = {}
for p in files:
    fn = os.path.basename(p)
    lines = open(p, encoding='utf-8').read().split('\n')
    cur = None; header = None
    for i, line in enumerate(lines):
        m = HEAD.match(line)
        if m:
            cur = m.group(1)
            stories.setdefault(cur, {'file': fn, 'title': m.group(2).strip()})
            continue
        if line.startswith('#'):
            cur = None
        if cur:
            f = re.match(r'^\|\s*([^|]*?)\s*\|\s*(.*?)\s*\|', line)
            if f:
                names = [n.strip().lower() for n in re.split(r'[·/]', f.group(1))]
                vals = [v.strip() for v in (f.group(2).split('·') if '·' in f.group(2) else [f.group(2)])]
                if len(names) == len(vals):
                    for n, v in zip(names, vals):
                        if n in ('points', 'wave', 'priority', 'release', 'size'):
                            stories[cur]['points' if n == 'size' else n] = v
        if line.startswith('|'):
            cells = [c.strip() for c in line.strip().strip('|').split('|')]
            if i + 1 < len(lines) and re.match(r'^\|[\s:|-]+\|\s*$', lines[i + 1]):
                header = [c.lower() for c in cells]; continue
            r = ROW.match(line)
            if r and r.group(1) not in stories and header and header[0].strip('* ') in ('id', 'story', 'story id', 'us'):
                st = {'file': fn, 'title': cells[1][:120] if len(cells) > 1 else ''}
                for h, c in zip(header, cells):
                    if re.search(r'\b(sp|points|story points|size)\b', h) and re.search(r'\d', c):
                        st['points'] = c
                    if re.search(r'wave|release', h):
                        st['wave'] = c
                stories[r.group(1)] = st

def epic(u):
    m = re.match(r'US-(\d{2})', u); return 'EP-' + m.group(1)
def sp(s):
    m = re.search(r'(\d{1,2})\s*[–-]\s*(\d{1,2})', s or '')
    if m: return int(m.group(1)), int(m.group(2))
    m = re.search(r'\b(\d{1,2})\b', s or '')
    if m: return int(m.group(1)), int(m.group(1))
    return None
agg = collections.defaultdict(lambda: {'stories': 0, 'with_points': 0, 'sp_low': 0, 'sp_high': 0, 'families': collections.Counter()})
for u, s in stories.items():
    a = agg[epic(u)]; a['stories'] += 1
    fam = 'Part 5' if re.match(r'US-\d{4}$', u) else ('advanced (Part 9.7-9.9)' if re.match(r'US-\d{2}-V', u) else 'source-pack enhancement')
    a['families'][fam] += 1
    r = sp(s.get('points'))
    if r:
        a['with_points'] += 1; a['sp_low'] += r[0]; a['sp_high'] += r[1]
json.dump({'stories': stories, 'by_epic': agg, 'total': len(stories)}, open(OUT, 'w'), indent=1, default=dict)
print('baseline stories', len(stories), 'with points', sum(a['with_points'] for a in agg.values()))
for e in sorted(agg):
    print(e, agg[e]['stories'], agg[e]['with_points'], agg[e]['sp_low'], agg[e]['sp_high'], dict(agg[e]['families']))
