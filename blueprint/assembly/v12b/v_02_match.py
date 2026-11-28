"""V-02: measure coverage of every extracted V12 statement in the blueprint (Part-*.md).
Measures per statement: exact ID presence; 6-gram containment (global); token containment in the best-matching
blueprint passage (line +/-2); number/threshold presence in that passage or in the lines carrying the statement's IDs.
Usage: python3 v_02_match.py before|after   ('before' excludes this part's own files Part-11-23*)."""
import sys, os, re, json, math
from collections import defaultdict, Counter
from v_common import OUT, part_files, part_label, ids_in, ctoks, shingles, num_keys_loose

MODE = sys.argv[1] if len(sys.argv) > 1 else 'before'

def build_index(files):
    lines = []; meta = []; heads = []
    for fi, f in enumerate(files):
        cur = ''
        for ln, t in enumerate(open(f, encoding='utf-8', errors='replace'), 1):
            t = t.rstrip('\n')
            if t.startswith('#'):
                cur = t.lstrip('#').strip()[:90]
            lines.append(t); meta.append((fi, ln)); heads.append(cur)
    idx = defaultdict(list); post = defaultdict(list); sh = set(); ltok = []
    for i, t in enumerate(lines):
        for x in ids_in(t):
            idx[x].append(i)
        ts = frozenset(ctoks(t)); ltok.append(ts)
        for w in ts:
            post[w].append(i)
        if len(t) > 20:
            sh |= shingles(t)
    df = {w: len(v) for w, v in post.items()}
    global LIT, NUMIDX
    NUMIDX = defaultdict(list)
    for i, t in enumerate(lines):
        if re.search(r'\d', t):
            for k in num_keys_loose(t):
                NUMIDX[k].append(i)
    LIT = set(idx)
    # Range-implied IDs: "V7-QA-004…039", "AIX-01–15", "SM-UAT-S001 to S135" -> every member counts as present (implied)
    rng = re.compile(r'([A-Z][A-Z0-9]*(?:-[A-Z0-9]*[A-Z][A-Z0-9]*)*-)([A-Z]?)(\d{1,4})\s*(?:…|\.\.\.|–|—|to)\s*(?:\1)?\2?(\d{1,4})\b')
    for i, t in enumerate(lines):
        for m in rng.finditer(t):
            pre, let, a, b = m.group(1), m.group(2), m.group(3), m.group(4)
            ia, ib = int(a), int(b)
            if ib <= ia or ib - ia > 2000:
                continue
            w = len(a)
            for k in range(ia + 1, ib + 1):
                x = (pre + let + str(k).zfill(w)).upper()
                if x not in idx:
                    idx[x].append(i)
    # Compressed workflow test catalogue (Part 11.10b section 11.10.4.2): one row per workflow lists
    # scenario-test suffixes and numbered step tests -> expand to <wf>-TC-<SUF> and <wf>-STEP-<nn>-TC
    for i, t in enumerate(lines):
        m = re.match(r'\|\s*(SM-SVC-\d{2}-WF\d+)\s*\|', t)
        if not m:
            continue
        cells = [c.strip() for c in t.strip().strip('|').split('|')]
        if len(cells) < 6:
            continue
        wf = m.group(1)
        for suf in re.findall(r'\b(POS|INPUT|SCOPE|ENT|DUP|QUALITY|BUDGET|RECOVERY|APPROVAL|EFFECT)\b', cells[3]):
            idx[wf + '-TC-' + suf].append(i)
        if re.search(r'\b\d{2} (ER|AI|DC|DL|PG|IR|EX):', cells[5]):
            idx[wf + '-TC'].append(i)
            for n in re.findall(r'\b(\d{2}) (?:ER|AI|DC|DL|PG|IR|EX):', cells[5]):
                idx[wf + '-STEP-' + n + '-TC'].append(i)
    return lines, meta, heads, idx, post, df, sh, ltok

def main():
    files = part_files(include_own=(MODE == 'after'))
    lines, meta, heads, idx, post, df, sh, ltok = build_index(files)
    N = len(lines)
    stmts = json.load(open(os.path.join(OUT, 'statements.json')))
    sec_ids = {}
    res = []
    for s in stmts:
        st = set(ctoks(s['text']))
        ids = s['ids']
        ctx = ids_in(s['sec'])
        present = [x for x in ids if x in idx]
        # candidate lines
        cand = Counter()
        anchor = ids if ids else ctx
        anchor_lines = []
        for x in anchor:
            anchor_lines.extend(idx.get(x, [])[:300])
        for i in anchor_lines:
            cand[i] += 5.0
        rare = sorted((w for w in st if w in df and df[w] <= 4000), key=lambda w: df[w])[:7]
        for w in rare:
            wt = math.log(N / df[w])
            for i in post[w]:
                cand[i] += wt
        best = 0.0; bi = None; bnum = 0.0
        nums = s['nums']
        for i, _ in cand.most_common(40):
            fi = meta[i][0]
            pas = set()
            for j in range(max(0, i - 2), min(N, i + 3)):
                if meta[j][0] == fi:
                    pas |= ltok[j]
            c = len(st & pas) / len(st) if st else 0.0
            if c > best:
                best = c; bi = i
        # ID-context containment (union of lines carrying the statement's own IDs)
        idc = 0.0
        if anchor_lines:
            u = set()
            for i in anchor_lines[:400]:
                u |= ltok[i]
            idc = len(st & u) / len(st) if st else 0.0
        # numbers
        if nums:
            pool = set()
            if bi is not None:
                fi = meta[bi][0]
                for j in range(max(0, bi - 3), min(N, bi + 4)):
                    if meta[j][0] == fi:
                        pool |= num_keys_loose(lines[j])
            for i in anchor_lines[:400]:
                pool |= num_keys_loose(lines[i])
            hit = 0
            for k in nums:
                if k in pool or re.match(r'[\d.]+', k).group(0) in pool:
                    hit += 1; continue
                # fallback: the same threshold anywhere in the blueprint on a line sharing >=50% of the statement's content tokens
                for i in NUMIDX.get(k, [])[:3000]:
                    if st and len(st & ltok[i]) / len(st) >= 0.5:
                        hit += 1; break
            bnum = hit / len(nums)
        ssh = shingles(s['text'])
        ng = (len(ssh & sh) / len(ssh)) if ssh else None
        tok = max(best, idc * 0.9)
        idp = (len(present) / len(ids)) if ids else None
        # composite level
        if ng is not None and ng >= 0.8:
            lvl = 'exact'
        elif (ng is not None and ng >= 0.5) or tok >= 0.8 or (idp == 1 and tok >= 0.6):
            lvl = 'strong'
        elif tok >= 0.6 or (idp == 1 and tok >= 0.45) or (ng is not None and ng >= 0.3):
            lvl = 'moderate'
        elif tok >= 0.35 or (idp or 0) > 0:
            lvl = 'weak'
        else:
            lvl = 'none'
        loc = ''
        if bi is not None:
            loc = 'Part %s L%d (%s)' % (part_label(files[meta[bi][0]]), meta[bi][1], heads[bi])
        res.append(dict(sid=s['sid'], ids=len(ids), ids_present=len(present), ids_literal=sum(1 for x in ids if x in LIT), idp=idp, ng=None if ng is None else round(ng, 3),
                        tok=round(tok, 3), num=None if not nums else round(bnum, 3), level=lvl, loc=loc,
                        missing_ids=[x for x in ids if x not in idx]))
    json.dump(res, open(os.path.join(OUT, 'match_%s.json' % MODE), 'w'))
    c = Counter(r['level'] for r in res)
    tot = len(res)
    summ = dict(mode=MODE, files=len(files), lines=N, statements=tot, levels=dict(c),
                matched_pct=round(100 * (c['exact'] + c['strong'] + c['moderate']) / tot, 2),
                id_literal_pct=round(100 * sum(r['ids_literal'] for r in res) / max(1, sum(r['ids'] for r in res)), 2),
                distinct_ids=len({x for st in stmts for x in st['ids']}),
                distinct_ids_missing=len({x for r in res for x in r['missing_ids']}),
                statements_with_thresholds=sum(1 for r in res if r['num'] is not None),
                id_presence_pct=round(100 * sum(r['ids_present'] for r in res) / max(1, sum(r['ids'] for r in res)), 2),
                ngram6_mean=round(sum(r['ng'] for r in res if r['ng'] is not None) / sum(1 for r in res if r['ng'] is not None), 4),
                token_mean=round(sum(r['tok'] for r in res) / tot, 4),
                number_presence_pct=round(100 * sum(r['num'] for r in res if r['num'] is not None) / max(1, sum(1 for r in res if r['num'] is not None)), 2))
    json.dump(summ, open(os.path.join(OUT, 'match_%s_summary.json' % MODE), 'w'), indent=1)
    print(json.dumps(summ, indent=1))

if __name__ == '__main__':
    main()
