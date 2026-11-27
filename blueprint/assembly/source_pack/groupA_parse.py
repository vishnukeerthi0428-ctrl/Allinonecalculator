"""Group A source-pack parser: splits docs 03/11/12/13/14/37 into headings, tables, rows and lines;
marks common-core lines (text that occurs in >= 5 of the 38 documents) so they are counted once."""
import collections, json, pathlib, re, sys
D = pathlib.Path(sys.argv[1])
docs = sorted(D.glob('*.txt'))
occ = collections.Counter()
for p in docs:
    seen = set(l.strip() for l in p.read_text(encoding='utf-8').splitlines() if len(l.strip()) > 25)
    occ.update(seen)
GROUP = ['03', '11', '12', '13', '14', '37']
out = {}
for p in docs:
    nn = p.name[:2]
    if nn not in GROUP:
        continue
    lines = p.read_text(encoding='utf-8').splitlines()
    head = None; stats = collections.Counter(); sections = []
    in_table = False
    uniq = []
    for l in lines:
        s = l.strip()
        m = re.match(r'<Heading(\d)> (.*)', s)
        if m:
            head = m.group(2); sections.append((int(m.group(1)), head)); stats['headings'] += 1; continue
        if s == '[TABLE]': in_table = True; stats['tables'] += 1; continue
        if s == '[/TABLE]': in_table = False; continue
        if s == '---row': stats['rows'] += 1; continue
        if not s: continue
        stats['lines'] += 1
        core = occ[s] >= 5
        stats['core_lines' if core else 'unique_lines'] += 1
        if not core:
            uniq.append((head, s))
    out[nn] = {'file': p.name, 'bytes': p.stat().st_size, 'stats': dict(stats),
               'sections': sections, 'unique_by_section': collections.Counter(h for h, _ in uniq)}
json.dump(out, open(sys.argv[2], 'w'), indent=1, default=list)
for nn, v in out.items():
    print(nn, v['file'], v['bytes'], v['stats'])
