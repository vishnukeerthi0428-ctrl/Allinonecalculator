#!/usr/bin/env python3
"""Part 11.22 (Group P7, letter U) inventory.

Lists every FR-V12-* requirement defined or referenced in Parts 11.1-11.19,
every existing V12 story (US-<EP>-Y?nn / Z?nn / EHnn), and the story -> FR
trace links, then reports every FR that has no story.

Definitions
  FR defined   : FR ID is the first cell of a Markdown table row, or the
                 subject of a heading, or appears as "Functional requirement | FR-..."
  FR referenced: any other mention (single, list, range "001…135", "001..135",
                 "001–135", slash "104/105").
  Story defined: heading "#... US-..", first cell of a table row "| US-.. |",
                 or "| ID | US-.. |" field row.
  Story -> FR  : (a) FR IDs (incl. ranges) inside a story block (heading to next
                 heading of same or higher level); (b) FR IDs in any table row that
                 also names a story ID; (c) bare 3-digit lists in a cell of a
                 story table row, resolved to the story family's letter
                 (YA->A ... ZR->R).
Usage: python3 -I u_01_inventory.py <blueprint_dir> <out_json>
"""
import json, os, re, sys, glob, collections

BP = sys.argv[1] if len(sys.argv) > 1 else '.'
OUT = sys.argv[2] if len(sys.argv) > 2 else 'u_inventory.json'

PARTS = [p for p in sorted(glob.glob(os.path.join(BP, 'Part-11-*.md')))
         if re.match(r'Part-11-(1[0-9]?|[2-9])[a-e]?_', os.path.basename(p))]
# keep 11.1 .. 11.19 only (exclude 11.0 report, 11.20+ written by other groups)
def part_no(p):
    m = re.match(r'Part-11-(\d+)', os.path.basename(p)); return int(m.group(1))
PARTS = [p for p in PARTS if 1 <= part_no(p) <= 19]

FR_RE = re.compile(r'FR-V12-([A-Z])-(\d{3,4})((?:\s*(?:…|\.\.|–|/|,\s*)\s*(?:FR-V12-[A-Z]-)?\d{3,4})*)')
US_RE = re.compile(r'US-(\d{2})-((?:Y|Z)[A-Z]|EH)(\d{2,3})((?:\s*(?:…|–|/|,)\s*(?:US-\d{2}-)?(?:(?:Y|Z)[A-Z]|EH)?\d{2,3})*)')
HEAD_RE = re.compile(r'^(#{2,6})\s+(.*)$')

def expand_fr(m):
    letter, first, tail = m.group(1), int(m.group(2)), m.group(3) or ''
    ids = {first}
    prev = first
    for sep, num in re.findall(r'(…|\.\.|–|/|,)\s*(?:FR-V12-[A-Z]-)?(\d{3,4})', tail):
        n = int(num)
        if sep in ('…', '..', '–') and prev < n <= prev + 400:
            ids.update(range(prev, n + 1))
        else:
            ids.add(n)
        prev = n
    return {f'FR-V12-{letter}-{i:03d}' for i in ids}

def expand_us(m):
    ep, fam, first, tail = m.group(1), m.group(2), int(m.group(3)), m.group(4) or ''
    ids = {first}; prev = first
    for sep, fam2, num in re.findall(r'(…|–|/|,)\s*(?:US-\d{2}-)?((?:Y|Z)[A-Z]|EH)?(\d{2,3})', tail):
        n = int(num)
        if fam2 and fam2 != fam:
            continue
        if sep in ('…', '–') and prev < n <= prev + 60:
            ids.update(range(prev, n + 1))
        else:
            ids.add(n)
        prev = n
    return {f'US-{ep}-{fam}{i:02d}' for i in ids}

DIRECT = collections.defaultdict(set)
def frs_in(text):
    out = set()
    for m in FR_RE.finditer(text):
        out |= expand_fr(m)
        DIRECT[m.group(1)].add(int(m.group(2)))
        for n in re.findall(r'(?:FR-V12-[A-Z]-)?(\d{3,4})', m.group(3) or ''):
            DIRECT[m.group(1)].add(int(n))
    return out

def uss_in(text):
    out = set()
    for m in US_RE.finditer(text):
        out |= expand_us(m)
    return out

NUMLIST = re.compile(r'^\s*\d{3}(\s*(,|–|…|-|and)\s*\d{3})*\s*$')
def bare_numbers(cell):
    c = re.sub(r'\(.*?\)', '', cell).strip()
    if not NUMLIST.match(c):
        return set()
    nums = set(); prev = None
    for tok in re.findall(r'(–|…|-)?\s*(\d{3})', c):
        sep, n = tok[0], int(tok[1])
        if sep and prev is not None and prev < n <= prev + 200:
            nums.update(range(prev, n + 1))
        else:
            nums.add(n)
        prev = n
    return nums

fr_def = {}            # FR -> {file, line, text}
fr_refs = collections.defaultdict(set)   # FR -> files
stories = {}           # US -> {file, line, title, epic, family, format, points, release}
story_frs = collections.defaultdict(set)
fr_stories = collections.defaultdict(set)

TOK_RE = re.compile(r'\b(ENT-[A-Z]{3}-\d{2}|AIX-\d{2}|CTRL-AI-\d{2}|MT-API-\d{2}|MT-\d{2}|GC-\d{2}|CJ-R\d{2}|REC-\d{2}|SEC-\d{2}|MOB-\d{2}|RT-\d{2}|CS-\d{2}|AT-\d{2}|OPT-API-\d{2}|INV-SVC-\d{2}(?:-WF0\d)?|SM-SVC-\d{2}|SEC-CTL-N-\d{2}|PERF-\d{2}|FL-\d{2}|CV-\d{2}|BR-C\d{2})\b')
story_tok = collections.defaultdict(set)
def link(us, fr):
    story_frs[us].add(fr); fr_stories[fr].add(us)

FIB_RANGE = re.compile(r'^\s*\*?\*?(\d{1,2})\s*[–-]\s*(\d{1,2})\*?\*?\s*$')
for path in PARTS:
    fn = os.path.basename(path)
    lines = open(path, encoding='utf-8').read().split('\n')
    # ---- pass 1: story blocks by heading
    block_us = None; block_level = 9; header_cells = None; last_head = ''
    for i, line in enumerate(lines):
        hm = HEAD_RE.match(line)
        if hm:
            level = len(hm.group(1)); title = hm.group(2)
            if block_us and level <= block_level:
                block_us = None
            sm = re.match(r'(US-\d{2}-(?:(?:Y|Z)[A-Z]|EH)\d{2,3})\b\s*[–:-]?\s*(.*)', title)
            last_head = title
            if sm:
                block_us = sm.group(1); block_level = level
                st = stories.setdefault(block_us, {'file': fn, 'line': i + 1, 'title': sm.group(2).strip(), 'format': 'block'})
                st['format'] = 'block'; st['file'] = fn; st['title'] = sm.group(2).strip() or st.get('title', '')
            # FR heading definitions
            for fr in frs_in(title):
                if title.strip().startswith(fr):
                    fr_def.setdefault(fr, {'file': fn, 'line': i + 1, 'text': title[len(fr):].strip(' –:-')[:300]})
            header_cells = None
            continue
        pm = re.match(r'^\*\*(US-\d{2}-(?:(?:Y|Z)[A-Z]|EH)\d{2,3})\b\s*[—–:-]?\s*([^*]*)\*\*', line)
        if pm:
            block_us = pm.group(1); block_level = 7
            stories.setdefault(block_us, {'file': fn, 'line': i + 1, 'title': pm.group(2).strip(' .'), 'format': 'paragraph'})
        for fr in frs_in(line):
            fr_refs[fr].add(fn)
        bm = re.match(r'^\*\*(?:Requirement\s+)?(FR-V12-[A-Z]-\d{3,4})\*\*\s*(.*)', line)
        if bm:
            para = '\n'.join(lines[i:i + 16])
            fr_def.setdefault(bm.group(1), {'file': fn, 'line': i + 1, 'text': re.sub(r'\s+', ' ', bm.group(2))[:300],
                                            'para': para[:4000], 'section': last_head})
        if block_us:
            story_tok[block_us] |= set(TOK_RE.findall(line))
            for fr in frs_in(line):
                link(block_us, fr)
            fm = re.match(r'^\|\s*([^|]*?)\s*\|\s*(.*?)\s*\|', line)
            if fm:
                names = [n.strip().lower() for n in re.split(r'[·/]', fm.group(1))]
                vals = [v.strip() for v in (fm.group(2).split('·') if '·' in fm.group(2) else [fm.group(2)])]
                if len(names) == len(vals):
                    for n, v in zip(names, vals):
                        if n in ('points', 'wave', 'priority', 'release', 'size', 'sp'):
                            stories[block_us]['points' if n in ('size', 'sp') else n] = v
        if line.startswith('|'):
            cells = [c.strip() for c in line.strip().strip('|').split('|')]
            if re.match(r'^[-: ]+$', ''.join(cells)):
                continue
            first = cells[0].strip('* ')
            # header detection: next line is separator
            if i + 1 < len(lines) and re.match(r'^\|[\s:|-]+\|\s*$', lines[i + 1]):
                header_cells = [c.lower() for c in cells]
                continue
            # FR definitions
            mfr = re.match(r'^(FR-V12-[A-Z]-\d{3,4})$', first)
            if mfr:
                fr = mfr.group(1)
                if fr not in fr_def:
                    txt = ''
                    for c in cells[1:]:
                        if len(c) > 25 and not c.startswith('C') or len(c) > 40:
                            txt = c; break
                    if not txt and len(cells) > 1:
                        txt = cells[1]
                    fr_def[fr] = {'file': fn, 'line': i + 1, 'text': re.sub(r'\s+', ' ', txt)[:300],
                                  'cells': cells, 'header': header_cells or [], 'section': last_head,
                                  'epic': next((re.search(r'EP-\d{2}', c).group(0) for c in cells if re.search(r'\bEP-\d{2}\b', c)), ''),
                                  'release': next((c for c in cells if re.match(r'^(R[0-9]|Release [12]|W[0-6]|Future)', c)), '')}
            if first in ('Functional requirement', 'FR', 'Requirement') and len(cells) > 1:
                for fr in frs_in(cells[1]):
                    fr_def.setdefault(fr, {'file': fn, 'line': i + 1, 'text': '(defined in register; see block)'})
            # stories in this row
            row_us = uss_in(line)
            mus = re.match(r'^(US-\d{2}-(?:(?:Y|Z)[A-Z]|EH)\d{2,3})$', first)
            if first == 'ID' and len(cells) > 1 and re.match(r'^US-\d{2}-', cells[1]):
                pass
            elif mus and mus.group(1) not in stories:
                us = mus.group(1)
                title = ''
                for c in cells[1:]:
                    if c.startswith('As ') or (len(c) > 15 and not c.startswith('FR-')):
                        title = c; break
                st = {'file': fn, 'line': i + 1, 'title': re.sub(r'\s+', ' ', title)[:200], 'format': 'table'}
                if header_cells:
                    for hc, c in zip(header_cells, cells):
                        if re.search(r'\b(sp|points|story points|size)\b', hc) and re.search(r'\d', c):
                            st['points'] = c
                        if re.search(r'release|wave', hc):
                            st['release'] = c
                        if hc.strip('* ') in ('title', 'story title', 'name'):
                            st['title'] = c
                stories[us] = st
            if row_us:
                for us in row_us:
                    story_tok[us] |= set(TOK_RE.findall(line))
                frs = frs_in(line)
                fams = {u.split('-')[2][:2] for u in row_us}
                for c in cells:
                    nums = bare_numbers(c)
                    if nums:
                        for fam in fams:
                            if fam != 'EH':
                                frs |= {f'FR-V12-{fam[1]}-{n:03d}' for n in nums}
                for us in row_us:
                    for fr in frs:
                        link(us, fr)

# ---- acceptance-criteria detection per story
has_ac = set()
for path in PARTS:
    text = open(path, encoding='utf-8').read()
    for blk in re.findall(r'```gherkin(.*?)```', text, flags=re.S):
        has_ac |= uss_in(blk)
    for line in text.split('\n'):
        if line.startswith('|') and re.search(r'\b(Given|AC-\d|AC-[0-9A-Z]+-\d|Scenario)\b', line):
            has_ac |= uss_in(line)
        if re.match(r'^\s*Feature:', line):
            has_ac |= uss_in(line)
# block stories: AC if their block contains a gherkin fence (detected during pass 1)
for path in PARTS:
    lines = open(path, encoding='utf-8').read().split('\n')
    cur = None; lvl = 9
    for line in lines:
        hm = HEAD_RE.match(line)
        if hm:
            l = len(hm.group(1))
            if cur and l <= lvl: cur = None
            sm = re.match(r'(US-\d{2}-(?:(?:Y|Z)[A-Z]|EH)\d{2,3})\b', hm.group(2))
            if sm: cur, lvl = sm.group(1), l
            continue
        pm = re.match(r'^\*\*(US-\d{2}-(?:(?:Y|Z)[A-Z]|EH)\d{2,3})\b', line)
        if pm: cur, lvl = pm.group(1), 7
        if cur and ('```gherkin' in line or re.match(r'^\s*(Scenario|Given)\b', line)):
            has_ac.add(cur)
# stories mentioned in ID field rows only (block format already caught)
all_fr = set(fr_def) | set(fr_refs)
# keep only FR whose letter belongs to groups A..R
all_fr = {f for f in all_fr if f.split('-')[2] in 'ABCDEFGHIJKLMNOPQR'}
defined = {f for f in all_fr if f in fr_def}
ref_only = sorted(all_fr - defined)
# a referenced-only id inside a declared range of a group's register is kept as a requirement
# only when its letter's register has definitions spanning it (guards against expanded ranges
# that overshoot, e.g. TC ranges mis-read). Otherwise it is reported as 'reference only'.
maxdef = collections.defaultdict(int)
for l, ns in DIRECT.items():
    maxdef[l] = max(ns)
direct_ids = {f'FR-V12-{l}-{n:03d}' for l, ns in DIRECT.items() for n in ns}
inventory = sorted(defined | (direct_ids & all_fr),
                   key=lambda f: (f.split('-')[2], int(f.split('-')[3])))
covered = [f for f in inventory if fr_stories.get(f)]
uncovered = [f for f in inventory if not fr_stories.get(f)]
no_ac = [f for f in covered if not any(u in has_ac for u in fr_stories[f])]

def epic_of(us): return 'EP-' + us.split('-')[1]
res = {
    'parts_scanned': [os.path.basename(p) for p in PARTS],
    'fr_total': len(inventory),
    'fr_defined': len(defined),
    'fr_reference_only_in_range': len(set(inventory) - defined),
    'fr_by_letter': collections.Counter(f.split('-')[2] for f in inventory),
    'stories_total': len(stories),
    'stories_by_epic': collections.Counter(epic_of(u) for u in stories),
    'fr_covered': len(covered),
    'fr_uncovered': len(uncovered),
    'fr_covered_without_ac': len(no_ac),
    'no_ac': no_ac,
    'stories_with_ac': len([u for u in stories if u in has_ac]),
    'uncovered': [{'fr': f, **fr_def.get(f, {'file': sorted(fr_refs.get(f, []))[:1], 'text': '(reference only)'})} for f in uncovered],
    'fr': {f: {'def': fr_def.get(f), 'stories': sorted(fr_stories.get(f, []))} for f in inventory},
    'stories': {u: {**stories[u], 'frs': sorted(story_frs.get(u, [])), 'has_ac': u in has_ac, 'tokens': sorted(story_tok.get(u, []))} for u in sorted(stories)},
}
json.dump(res, open(OUT, 'w'), indent=1, default=list)
print('parts', len(PARTS), 'FR', len(inventory), 'defined', len(defined), 'stories', len(stories),
      'covered', len(covered), 'uncovered', len(uncovered))
print('covered but no story with AC', len(no_ac), collections.Counter(f.split('-')[2] for f in no_ac), 'stories with AC', len([u for u in stories if u in has_ac]))
print('uncovered by letter', collections.Counter(f.split('-')[2] for f in uncovered))
print('FR by letter', dict(res['fr_by_letter']))
