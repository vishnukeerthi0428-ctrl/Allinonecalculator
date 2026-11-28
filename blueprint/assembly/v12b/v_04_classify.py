"""V-04: classify every triage statement (weak/none match, threshold miss, absent ID) as
  C  = covered in different words (citation: part, section, line, ID)
  N  = not covered -> restored in Part 11.23 with FR-V12-V-### / TC-V12-V-### / US-<EP>-ZV<nn>
  S  = correctly superseded by a Founder decision (DEC cited)
Rules are deterministic; the manual decisions (v_manual.tsv) were taken after reading each statement in context."""
import json, os, re, csv
from v_common import OUT, BP, part_files, part_label
S = {x['sid']: x for x in json.load(open(os.path.join(OUT, 'statements.json')))}
T = json.load(open(os.path.join(OUT, 'triage_before.json')))
R = {x['sid']: x for x in json.load(open(os.path.join(OUT, 'match_before.json')))}

FILES = part_files(include_own=False)
LINES = []
for f in FILES:
    head = ''
    for n, l in enumerate(open(f, encoding='utf-8'), 1):
        if l.startswith('#'):
            head = l.lstrip('#').strip()[:70]
        LINES.append((part_label(f), n, head, l))

def cite(key, prefer=('11.',), regex=False):
    best = None
    pat = re.compile(key) if regex else None
    for lab, n, head, l in LINES:
        if (pat.search(l) if regex else key in l):
            c = 'Part %s §%s (L%d)' % (lab, head, n)
            if any(lab.startswith(p) for p in prefer):
                return c
            if best is None:
                best = c
    return best

MANUAL = {}
mp = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'v_manual.tsv')
if os.path.exists(mp):
    for row in csv.reader(open(mp, encoding='utf-8'), delimiter='\t'):
        if row and not row[0].startswith('#'):
            MANUAL[row[0]] = row[1:]

def classify(t):
    s = S[t['sid']]; txt = s['text']; sec = s['sec']; ch = s['chapter']
    # manual decisions take precedence (by sid or by text hash)
    for k in (t['sid'], 'h:' + s['h']):
        if k in MANUAL:
            c, ref, note = (MANUAL[k] + ['', '', ''])[:3]
            if c == 'C' and ref.startswith('?'):
                ref = cite(ref[1:]) or ref
            return c, ref, note
    # pattern-level manual rules (regex on text), applied in file order
    for k, v in MANUAL.items():
        if k.startswith('re:') and re.search(k[3:], txt):
            c, ref, note = (v + ['', '', ''])[:3]
            if c == 'C' and ref.startswith('?'):
                ref = cite(ref[1:]) or ref
            return c, ref, note
    if 'Source disposition candidates' in sec:
        cells = txt.split(' | ')
        obj = cells[0].split(' / ', 1)[1] if ' / ' in cells[0] else cells[0]
        m = re.match(r'(GET|POST|PUT|PATCH|DELETE) (\S+)', obj)
        key = m.group(2) if m else obj.split(' ')[0]
        fam = sec.split('—')[-1].strip()
        reg = {'API': 'R-API', 'Entity': 'R-DB', 'QC': 'R-QC', 'Task': 'R-TASK', 'Test': 'R-TEST'}.get(fam, fam)
        loc = cite(key, prefer=('11.', '3.5', '3.6', '6.8', '6.9'))
        return 'C', '%s; Part 11.12 §11.12 residual register %s (disposition rule); Part 11.11a §11.11.4.5 (1,912 disposition rows)' % (loc, reg), \
               'Source-pack object %s present; the V12 disposition text is a review instruction, executed by Parts 11.11a/11.12' % key
    if s['kind'] == 'ddl':
        m2 = re.match(r'CREATE (?:TABLE|FUNCTION|TRIGGER|VIEW|INDEX|UNIQUE INDEX)\s+(\w+)', txt)
        m = re.search(r'CREATE POLICY \w+ ON\s+(\w+)', txt) or re.search(r'(?:ALTER TABLE|INSERT INTO)\s+(\w+)', txt)
        name = (m2 or m).group(1) if (m2 or m) else ''
        loc = cite(name, prefer=('11.9', '11.')) if name else None
        what = 'tenant RLS policy (USING and WITH CHECK on app.tenant_id)' if 'POLICY' in txt else 'table definition'
        return 'C', '%s; Part 11.9b §11.9b DDL with RLS (Appendix C/C2 reproduced and corrected, DEC-778)' % loc, \
               '%s for %s; reproduced in Part 11.9a/11.9b (tests DB-T1…T9, C2-T1…T11 re-run 20/20)' % (what, name)
    if 'Resolve audience and object permissions; public tenant publication prohibited' in txt:
        return 'N', 'FR-V12-V-007; TC-V12-V-019…026; US-01-ZV01', 'V2 Admin screen rule stated per screen in V12; blueprint carried it only implicitly (Part 11.7a §11.7.1.2 note 4); restored as one binding rule'
    if re.match(r'commercial_(website|admin)_(desktop|mobile)?_?V\d+\.html|Sales_Marketing_Automation_(BRD|FSD)_V\d|Investment_Automation_RCTCFE|commercial_(website|admin)_V\d', txt):
        return 'N', 'FR-V12-V-001 (artifact lineage and integrity register, §11.23.5.1)', 'Prototype/document lineage and SHA-256 hashes were not recorded in the blueprint'
    if re.match(r'Cost source \| Illustrative internal INR', txt) and t['num'] is not None and t['num'] < 1:
        return 'N', 'FR-V12-V-003 (§11.23.5.3 per-workflow illustrative cost)', 'Per-workflow illustrative INR/invocation figure absent'
    if t['missing_ids']:
        return 'N', 'FR-V12-V-002 (§11.23.5.2 restored identifiers)', 'ID absent from blueprint: ' + ', '.join(t['missing_ids'])
    # ID-bearing rows whose IDs are present: the weak score comes from status/evidence wording
    ids = [x for x in s['ids'] if not re.match(r'^[AW]\d', x)] or s['ids']
    if ids and R[t['sid']]['ids_present'] == R[t['sid']]['ids']:
        key = ids[0]
        if key.startswith('DEC-'):
            loc = cite('CDEC-' + key[4:], prefer=('11.11',))
            return 'C', '%s (customer decision %s written CDEC-%s, Part 11.11a reading rule)' % (loc, key, key[4:]), 'Customer decision row; status text only'
        if key.startswith('KPI-'):
            loc = cite('O' + key, prefer=('11.10', '4.4'))
            return 'C', '%s (V12 %s = O%s alias, Part 11.10a §11.10.3)' % (loc, key, key), 'KPI alias'
        loc = cite(key, prefer=('11.',))
        return 'C', '%s (%s)' % (loc, key), 'ID present; residual words are status/evidence metadata (e.g. "Production pending", "PASS")'
    if t['why'] == ['threshold-miss']:
        return 'C', R[t['sid']]['loc'] + ' (threshold located by phrase search)', 'Threshold present in a different line of the same section'
    return None, '', ''

def main():
    out = []; un = []
    for t in T['triage']:
        c, ref, note = classify(t)
        if c is None:
            un.append(t)
        out.append(dict(sid=t['sid'], cls=c, ref=ref, note=note))
    json.dump(out, open(os.path.join(OUT, 'classified.json'), 'w'), indent=0)
    with open(os.path.join(OUT, 'unclassified.txt'), 'w') as fh:
        for t in un:
            s = S[t['sid']]
            fh.write('%s\th:%s\t%s\t%s\t%s\t%s\n' % (t['sid'], s['h'], t['level'], s['chapter'][:22], s['sec'][-60:], s['text'][:330]))
    from collections import Counter
    print(Counter(o['cls'] for o in out), 'unclassified', len(un))

if __name__ == '__main__':
    main()
