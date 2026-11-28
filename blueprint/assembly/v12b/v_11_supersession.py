"""V-11: status of every baseline ID in the revised blueprint and the supersession index (final/supersession_index.csv).
Evidence order: (1) decision rows (| DEC-### | ... |) in Parts 11.x, sentence by sentence; (2) other Part 11 lines that
name a baseline ID with a supersede/amend verb; (3) curated overrides (v_overrides.tsv) for scoped supersessions.
Status: retained unchanged | amended | superseded | missing (restored in Part 11.23)."""
import re, os, glob, csv, json
from collections import defaultdict, Counter
from v_common import BP, OUT, part_label, ids_in
from v_10_baseline import family, NEWFAM

SUP = re.compile(r'\b(supersed\w*|replac\w*|withdraw\w*|retir\w*|obsolete|lifted|no longer applies|closes?\b)', re.I)
AMD = re.compile(r'\b(amend\w*|extend\w*|alias\w*|renumber\w*|renam\w*|re-?plan\w*|indicative|refin\w*|narrow\w*|align\w*|restat\w*|read with|updat\w*|re-identif\w*|crosswalk|mapped|brought forward|adds?)\b', re.I)
SCOPED = re.compile(r'\b(for actions|only for|only|where|scoped|for mandated|the part of|in part|wording|for (?:the )?(?:Admin|EU|tenders?|mandated)|except|unless|for .* covered by)\b', re.I)

def main():
    B = json.load(open(os.path.join(OUT, 'baseline.json')))
    base = set(B['base_ids']); desc = B['desc']; first = B['first']
    p11 = sorted(f for f in glob.glob(os.path.join(BP, 'Part-11-*.md')) if not os.path.basename(f).startswith('Part-11-23'))
    ev = defaultdict(list)
    for f in p11:
        lab = part_label(f); head = ''
        for n, l in enumerate(open(f, encoding='utf-8'), 1):
            if l.startswith('#'):
                head = l.lstrip('#').strip()[:70]
            m = re.match(r'^\|\s*\**(DEC-\d{3})\**\s*\|', l)
            if m and int(m.group(1)[4:]) >= 423:
                auth = m.group(1)
                cells = [c.strip() for c in l.strip().strip('|').split('|')]
                body = ' | '.join(cells[1:])
                for sent in re.split(r'(?<=[.;])\s+|\s\|\s', body):
                    bas = [i for i in ids_in(sent) if i in base and i != auth]
                    if not bas:
                        continue
                    if SUP.search(sent):
                        st = 'amended' if SCOPED.search(sent) else 'superseded'
                    elif AMD.search(sent):
                        st = 'amended'
                    else:
                        continue
                    repl = [x for x in ids_in(sent) if x not in base and family(x) and not x.startswith('DEC-')]
                    for b in bas:
                        ev[b].append(dict(rank=1, status=st, auth=auth, repl=[x for x in repl if family(x) == family(b)][:4],
                                          loc='Part %s §%s (L%d)' % (lab, head, n), text=sent[:200]))
                continue
            bas = [i for i in ids_in(l) if i in base]
            if not bas:
                continue
            sup = SUP.search(l); amd = AMD.search(l)
            if not (sup or amd):
                continue
            news = [x for x in ids_in(l) if x not in base and family(x)]
            decs = [x for x in news if re.match(r'^DEC-\d{3}$', x) and int(x[4:]) >= 423]
            if not decs:
                continue  # without a post-baseline decision on the line, a verb alone is not evidence of change
            for b in bas:
                if b in decs:
                    continue
                st = 'amended'
                if sup and re.search(re.escape(b) + r'[^|]{0,60}' + r'(supersed|replac|withdraw|lifted)|(supersed\w*|replac\w*|withdraw\w*)[^|]{0,60}' + re.escape(b), l, re.I) and not SCOPED.search(l):
                    st = 'superseded'
                ev[b].append(dict(rank=2, status=st, auth=decs[0], repl=[x for x in news if family(x) == family(b) and not x.startswith('DEC-')][:4],
                                  loc='Part %s §%s (L%d)' % (lab, head, n), text=l.strip()[:200]))
    # curated overrides
    ov = {}
    op = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'v_overrides.tsv')
    for row in csv.reader(open(op, encoding='utf-8'), delimiter='\t'):
        if row and not row[0].startswith('#'):
            ov[row[0]] = row[1:]
    rows = []
    for i in sorted(base, key=lambda x: (family(x), x)):
        fl = first[i]
        bl = 'Part %s L%d' % (fl[0], fl[1])
        d = desc.get(i, ('', ''))[1]
        if i in ov:
            st, auth, repl, loc, note = (ov[i] + [''] * 5)[:5]
        elif ev.get(i):
            e = sorted(ev[i], key=lambda e: (e['rank'], 0 if e['status'] == 'superseded' else 1))
            top = e[0]
            st = top['status']; auth = top['auth']; repl = ' '.join(top['repl']); loc = top['loc']
            note = top['text'].replace('\n', ' ')
            if len({x['auth'] for x in e}) > 1:
                note = 'Also: ' + ', '.join(sorted({x['auth'] for x in e if x['auth'] != auth})[:6]) + '. ' + note
        else:
            st, auth, repl, loc, note = 'retained unchanged', '', '', bl, ''
        rows.append(dict(id=i, family=family(i), baseline_location=bl, baseline_descriptor=d, status=st,
                         authority=auth, replacement_ids=repl, evidence_location=loc, evidence_or_note=note[:240]))
    # missing (none expected; kept for the record)
    for i in B['missing_base']:
        rows.append(dict(id=i, family=family(i), baseline_location='', baseline_descriptor='', status='missing (restored in Part 11.23 §11.23.6)',
                         authority='Part 11.23', replacement_ids='', evidence_location='', evidence_or_note=''))
    os.makedirs(os.path.join(BP, 'final'), exist_ok=True)
    with open(os.path.join(BP, 'final', 'supersession_index.csv'), 'w', newline='', encoding='utf-8') as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader(); w.writerows(rows)
    c = Counter(r['status'] for r in rows)
    fc = defaultdict(Counter)
    for r in rows:
        fc[r['family']][r['status']] += 1
    json.dump(dict(status=dict(c), by_family={k: dict(v) for k, v in fc.items()}), open(os.path.join(OUT, 'supersession_summary.json'), 'w'), indent=1)
    print(dict(c))
    for k in sorted(fc):
        print(k, dict(fc[k]))

if __name__ == '__main__':
    main()
