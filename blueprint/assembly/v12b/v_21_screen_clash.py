"""V-21: detect screen IDs (A###, W##) that are defined with different names in different parts (cross-part clash check)."""
import re, glob, os, json, difflib
from collections import defaultdict
BP = '/home/user/Allinonecalculator/blueprint'
def main():
    defs = defaultdict(list)
    for f in sorted(glob.glob(os.path.join(BP, 'Part-*.md'))):
        if 'Part-11-23' in f:
            continue
        lab = os.path.basename(f).split('_')[0].replace('Part-', '')
        for n, l in enumerate(open(f, encoding='utf-8'), 1):
            if l.startswith('> **Erratum v1.2'):   # v1.2 erratum markers (Part 11.25) are pointers, not content
                continue
            m = re.match(r'^#{2,6}\s+\**([AW]\d{2,3})\**\s+[—:\-–]?\s*(.+)', l) or re.match(r'^\|\s*\**([AW]\d{2,3})\**\s*\|\s*([^|]{3,70})\|', l)
            if m:
                sid = m.group(1); name = re.sub(r'[*`]', '', m.group(2)).strip()[:60]
                if re.match(r'^[AW]\d', name) or len(name) < 4 or re.match(r'^(P\d|R\d|EP-|Yes|No|—)', name):
                    continue
                defs[sid].append((lab, n, name))
    clash = []
    for sid, v in defs.items():
        num = int(sid[1:])
        if (sid[0] == 'A' and num < 114) or (sid[0] == 'W' and num < 35):
            continue
        firsts = {}
        for lab, n, name in v:
            firsts.setdefault(lab, (n, name))
        distinct = []
        for lab, (n, name) in firsts.items():
            k = re.sub(r'\W+', ' ', name.lower()).strip()
            if not any(difflib.SequenceMatcher(None, k, dk).ratio() > 0.55 or dk[:12] == k[:12] for _, _, _, dk in distinct):
                distinct.append((lab, n, name, k))
        if len(distinct) > 1:
            clash.append(dict(id=sid, defs=[dict(part=a, line=b, name=c) for a, b, c, _ in distinct]))
    clash.sort(key=lambda x: (x['id'][0], int(x['id'][1:])))
    json.dump(clash, open(os.path.join(BP, 'assembly', 'v12b', 'v_out', 'screen_clash.json'), 'w'), indent=0)
    print(len(clash), 'screen IDs with different names in different parts')
    for c in clash:
        print(c['id'], ' || '.join('%s L%d: %s' % (d['part'], d['line'], d['name'][:40]) for d in c['defs'])[:330])
if __name__ == '__main__':
    main()
