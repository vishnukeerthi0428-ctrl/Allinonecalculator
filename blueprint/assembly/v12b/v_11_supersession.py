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
    # (3) baseline rows whose own text states a rule that a Founder decision changed (read-with amendment)
    STALE = [
        (re.compile(r'09:00\s*[–-]\s*19:00|19:00 Mon', re.I), 'DEC-777', 'Promotional window is now 09:00-21:00 recipient local time unless a rule pack is stricter'),
        (re.compile(r'(no|not|never|exclud\w*|out of scope)[^|]{0,40}(investor|fundrais)|(investor|fundrais)\w*[^|]{0,40}(exclud|out of scope|not in scope|prohibit)', re.I), 'DEC-783', 'Investor/fundraising adopted with securities rule packs (Parts 11.16a-e)'),
        (re.compile(r'(no|not|never|exclud\w*|block\w*|prohibit\w*)[^|]{0,30}(AI voice|voice call|outbound call|call recording|recordings?)\b', re.I), 'DEC-782', 'AI voice and recordings adopted with AI disclosure, consent, calling windows and retention controls (Part 11.18)'),
        (re.compile(r'(never|not|no)[^|]{0,25}submit\w*[^|]{0,15}bids?|bid submission[^|]{0,30}(human|manual) only', re.I), 'DEC-781', 'Automatic bid submission allowed only under a per-tender bounded mandate (Part 11.17b); unmandated submission still blocked'),
        (re.compile(r'capped at (autonomy )?L1|L1 cap|max(imum)? (autonomy )?L1\b|never (sign|pay)s?', re.I), 'DEC-779', 'L1 cap lifted only for actions under an Active, eligible bounded mandate in an approved jurisdiction (DEC-841)'),
        (re.compile(r'service key', re.I), 'DEC-778', 'API connects as least-privilege role app_rw under RLS; service_role only for CI migrations (DEC-894)'),
        (re.compile(r'RTO\s*(≤|<=)?\s*4\s*h', re.I), 'DEC-771', 'Growth RTO <= 120 min is release-blocking; RPO <= 15 min (DEC-787)'),
        (re.compile(r'business[- ]hours support|support[^|]{0,20}business hours', re.I), 'DEC-773', '24x7 human on-call for SEV1/SEV2 from Release 2 GA'),
        (re.compile(r'PostgreSQL 17|Amazon RDS|RDS for PostgreSQL', re.I), 'DEC-421', 'Database is Supabase PostgreSQL (DEC-421, DEC-772 regions, DEC-778/894 roles)'),
        (re.compile(r'single[- ]region|ap-south-1 only|Mumbai only', re.I), 'DEC-772', 'India (Mumbai) and EU residency stacks; further regions per DEC-776 when their rule pack is approved'),
    ]
    for f in sorted(glob.glob(os.path.join(BP, 'Part-0*.md'))):
        lab = part_label(f)
        for n, l in enumerate(open(f, encoding='utf-8'), 1):
            m = re.match(r'^(?:\|\s*|#+\s*)\**([A-Z][A-Z0-9]*(?:-[A-Za-z0-9]+)+|[AW]\d{2,3})\**\s*(?:\||[ :.—-])', l.strip())
            if not m or m.group(1) not in base:
                continue
            for pat, auth, rule in STALE:
                if pat.search(l):
                    ev[m.group(1)].append(dict(rank=3, status='amended', auth=auth, repl=[], loc='Part %s L%d (baseline row)' % (lab, n),
                                               text='Read with %s: %s' % (auth, rule)))
                    break
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
