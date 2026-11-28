"""V-10: baseline retention check (pre-V12 blueprint -> revised blueprint).
Baseline = Parts 0, 0A, 0B, 1-9.10 (files last modified before the V12 receipt, 28 Nov 2026 14:50) plus the pre-V12
registers in final/ (RTM.csv, dec_index.csv, adr_index.csv, coverage/*.csv). git is not run (task constraint).
For every ID of the audited families: retained unchanged / amended / superseded / missing (-> restored in Part 11.23)."""
import re, os, glob, csv, json
from collections import defaultdict, Counter
from v_common import BP, OUT, part_label, ids_in

FAMS = ['BR', 'FR', 'NFR', 'US', 'AC', 'TC', 'VER', 'API', 'ENT', 'AG', 'AU', 'WF', 'DEC', 'ADR', 'RSK', 'KPI', 'OKPI', 'BRL', 'CFG', 'RP', 'SCREEN']
NEWFAM = re.compile(r'^(FR|TC|US|AC|VER|API|BR|NFR)-V12-|^US-\d{2}-[YZ]|^AC-\d{2}-?[YZ]|^TC-V12|^FR-V12|^BR-V12|^BR-V7|^NFR-V12')

def family(i):
    if re.match(r'^[AW]\d{2,3}$', i):
        return 'SCREEN'
    p = i.split('-')[0]
    return p if p in FAMS else None

def baseline_files():
    fs = sorted(glob.glob(os.path.join(BP, 'Part-*.md')))
    return [f for f in fs if re.match(r'Part-0\d', os.path.basename(f))]

def revised_files():
    fs = sorted(glob.glob(os.path.join(BP, 'Part-*.md')))
    return [f for f in fs if not os.path.basename(f).startswith('Part-11-23')]

RANGE = re.compile(r'([A-Z][A-Z0-9]*(?:-[A-Z0-9]*[A-Z][A-Z0-9]*)*-)([A-Z]?)(\d{1,4})\s*(?:…|\.\.\.|–|—|to)\s*(?:\1)?\2?(\d{1,4})\b')
SCR_RANGE = re.compile(r'\b([AW])(\d{2,3})\s*(?:…|–|—|to)\s*\1?(\d{2,3})\b')

def scan(files, with_ranges=True):
    lit = defaultdict(list); imp = defaultdict(list)
    for f in files:
        lab = part_label(f); head = ''
        for n, l in enumerate(open(f, encoding='utf-8'), 1):
            if l.startswith('#'):
                head = l.lstrip('#').strip()[:80]
            for i in ids_in(l):
                if family(i):
                    lit[i].append((lab, n, head))
            if with_ranges:
                for m in RANGE.finditer(l):
                    pre, let, a, b = m.groups(); ia, ib = int(a), int(b)
                    if ib > ia and ib - ia <= 3000:
                        for k in range(ia + 1, ib + 1):
                            imp[(pre + let + str(k).zfill(len(a))).upper()].append((lab, n, head))
                for m in SCR_RANGE.finditer(l):
                    p, a, b = m.groups(); ia, ib = int(a), int(b)
                    if ib > ia and ib - ia <= 300:
                        for k in range(ia + 1, ib + 1):
                            imp[p + str(k).zfill(len(a))].append((lab, n, head))
    return lit, imp

VERB_SUP = re.compile(r'supersed|replac|withdrawn|retire|obsolete|no longer|lifted|removed', re.I)
VERB_AMD = re.compile(r'amend|extend|aliased|alias|renumber|renamed|re-?planned|indicative|updated|re-?baselin|crosswalk|mapped to|revised', re.I)

def main():
    bfiles = baseline_files(); rfiles = revised_files()
    blit, bimp = scan(bfiles)
    rlit, rimp = scan(rfiles)
    base_ids = {i for i in blit if not NEWFAM.match(i)}
    # descriptor: first table row / heading line that starts with the ID, else first mention
    desc = {}
    for f in bfiles:
        lab = part_label(f)
        for n, l in enumerate(open(f, encoding='utf-8'), 1):
            s = l.strip()
            m = re.match(r'^(?:\|\s*|#+\s*)\**([A-Z][A-Z0-9]*(?:-[A-Za-z0-9]+)+|[AW]\d{2,3})\**\s*(?:\||[ :.—-])\s*(.*)', s)
            if m and m.group(1) in base_ids and m.group(1) not in desc:
                txt = re.sub(r'\s*\|\s*', ' | ', m.group(2)).strip(' |')
                desc[m.group(1)] = ('%s L%d' % (lab, n), txt[:160])
    # Part 11 statements about baseline IDs
    p11 = [f for f in rfiles if os.path.basename(f).startswith('Part-11')]
    events = defaultdict(list)
    for f in p11:
        lab = part_label(f); head = ''
        for n, l in enumerate(open(f, encoding='utf-8'), 1):
            if l.startswith('#'):
                head = l.lstrip('#').strip()[:80]
            ids = ids_in(l)
            bas = [i for i in ids if i in base_ids]
            if not bas:
                continue
            sup = VERB_SUP.search(l); amd = VERB_AMD.search(l)
            if not (sup or amd):
                continue
            news = [i for i in ids if i not in base_ids and family(i)]
            decs = [i for i in news if i.startswith('DEC-')]
            for b in bas:
                events[b].append(dict(loc='Part %s L%d' % (lab, n), head=head, kind='sup' if sup else 'amd', decs=decs[:4],
                                      repl=[x for x in news if family(x) == family(b) and not x.startswith('DEC-')][:4], text=l.strip()[:220]))
    json.dump(dict(base_count=len(base_ids)), open(os.path.join(OUT, 'baseline_meta.json'), 'w'))
    # missing: register IDs (pre-V12 final/ registers) that no current part carries
    reg_ids = defaultdict(set)
    regs = [os.path.join(BP, 'final', x) for x in ('RTM.csv', 'RTM_advanced.csv', 'dec_index.csv', 'adr_index.csv')] + sorted(glob.glob(os.path.join(BP, 'final', 'coverage', '*.csv')))
    for r in regs:
        for line in open(r, encoding='utf-8', errors='replace'):
            for i in ids_in(line):
                if family(i) and not NEWFAM.match(i):
                    reg_ids[i].add(os.path.relpath(r, BP))
    allpresent = set(rlit) | set(rimp)
    missing_reg = sorted(i for i in reg_ids if i not in allpresent and i not in blit)
    missing_base = sorted(i for i in base_ids if i not in rlit)
    json.dump(dict(missing_reg={i: sorted(reg_ids[i]) for i in missing_reg}, missing_base=missing_base,
                   events={k: v for k, v in events.items()}, desc=desc,
                   base_ids=sorted(base_ids), first={i: blit[i][0] for i in base_ids},
                   rcount={i: len(rlit.get(i, [])) for i in base_ids}),
              open(os.path.join(OUT, 'baseline.json'), 'w'))
    c = Counter(family(i) for i in base_ids)
    print('baseline IDs', len(base_ids), dict(sorted(c.items())))
    print('baseline IDs absent from revised parts:', len(missing_base))
    print('register IDs absent from every part:', len(missing_reg), missing_reg[:60])
    print('baseline IDs with Part 11 supersession/amendment statements:', len(events))

if __name__ == '__main__':
    main()
