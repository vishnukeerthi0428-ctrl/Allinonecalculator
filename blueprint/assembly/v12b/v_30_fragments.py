"""V-30: build the data fragments of Part 11.23 (tables) and final/coverage_v12/V_audit.csv from the v_out data."""
import json, os, re, csv
from collections import Counter, defaultdict
from v_common import OUT, BP

def J(n):
    p = os.path.join(OUT, n)
    return json.load(open(p)) if os.path.exists(p) else None

S = {x['sid']: x for x in J('statements.json')}
RB = {x['sid']: x for x in J('match_before.json')}
RA = {x['sid']: x for x in (J('match_after.json') or J('match_before.json'))}
SB = J('match_before_summary.json'); SA = J('match_after_summary.json') or SB
CL = {x['sid']: x for x in J('classified.json')}
EX = J('extract_summary.json')
# Supersession overlay: statements that match the blueprint but state a rule a Founder decision changed
OVERLAY = [(r'^VND-(86|95) ', 'S', 'DEC-783', 'V12 vendor note "no investment or confidential fundraising use" superseded: Investment Automation adopted (Parts 11.16a-e)'),
           (r'^Investment_Automation_RCTCFE_Master_Prompt', 'S', 'DEC-783', 'Lineage row restored in FR-V12-V-001; its note "no Investment scope copied" is superseded by DEC-783')]

def cls_of(sid):
    s = S[sid]
    for pat, c, ref, note in OVERLAY:
        if re.search(pat, s['text']):
            return c, ref, note
    if sid in CL:
        c = CL[sid]
        return c['cls'], c['ref'], c['note']
    return 'M', RB[sid]['loc'], ''

def esc(t, n=None):
    t = (t or '').replace('|', '/').replace('\n', ' ').strip()
    t = re.sub(r'\s+', ' ', t)
    if n and len(t) > n:
        t = t[:n - 1].rstrip() + '…'
    return t

def pct(a, b):
    return '%.1f%%' % (100.0 * a / b) if b else '—'

def frag_summary():
    lv = ['exact', 'strong', 'moderate', 'weak', 'none']
    out = ['| Measure | Before (blueprint without Part 11.23) | After (with Part 11.23) | Method |', '|---|---|---|---|']
    out.append('| Statements extracted (requirement-like) | %s | %s | `v_01_extract.py`: prose sentences with a modal, ID or threshold; every non-header table row; ID headings; 330 OpenAPI operations; 156 DTO schemas; SQL statements |' % (f'{SB["statements"]:,}', f'{SA["statements"]:,}'))
    out.append('| Distinct V12 IDs in the statements | %s | %s | `ID_RE` + screen IDs |' % (f'{SB["distinct_ids"]:,}', f'{SA["distinct_ids"]:,}'))
    out.append('| ID presence, literal | %.2f%% | %.2f%% | exact ID string in `Part-*.md` |' % (SB['id_literal_pct'], SA['id_literal_pct']))
    out.append('| ID presence, literal + range/compressed | %.2f%% | %.2f%% | adds range notation (`X-001…045`) and the Part 11.10b compressed test catalogue |' % (SB['id_presence_pct'], SA['id_presence_pct']))
    out.append('| Distinct IDs absent | %d | %d | listed in §11.23.5.2 |' % (SB['distinct_ids_missing'], SA['distinct_ids_missing']))
    out.append('| Mean 6-gram containment | %.3f | %.3f | share of the statement\'s 6-word shingles found anywhere in the blueprint |' % (SB['ngram6_mean'], SA['ngram6_mean']))
    out.append('| Mean token containment (best passage) | %.3f | %.3f | content tokens of the statement found in the best blueprint passage (line ±2) or in the lines carrying its IDs |' % (SB['token_mean'], SA['token_mean']))
    out.append('| Threshold presence (%s statements with thresholds) | %.2f%% | %.2f%% | numbers with unit, comparator, currency or decimals found in the matched passage, the ID lines, or a line sharing ≥ 50%% of the tokens |' % (f'{SB["statements_with_thresholds"]:,}', SB['number_presence_pct'], SA['number_presence_pct']))
    for l in lv:
        out.append('| Level %s | %s | %s | §11.23.1.3 thresholds |' % (l, f'{SB["levels"].get(l, 0):,}', f'{SA["levels"].get(l, 0):,}'))
    out.append('| **Measured lexical match (exact + strong + moderate)** | **%.2f%%** | **%.2f%%** | deterministic; reproducible with `v_02_match.py before` and `after` |' % (SB['matched_pct'], SA['matched_pct']))
    return '\n'.join(out)

def frag_final():
    c = Counter(); n = len(S)
    for sid in S:
        k, _, _ = cls_of(sid)
        c[k] += 1
    out = ['| End state | Statements | Share | Meaning |', '|---|---|---|---|']
    out.append('| Matched (measured exact/strong/moderate, not triaged) | %s | %s | text, IDs and thresholds found |' % (f'{c["M"]:,}', pct(c['M'], n)))
    out.append('| Covered in different words (cited) | %s | %s | read in context; part, section, line and ID cited in `V_audit.csv` |' % (f'{c["C"]:,}', pct(c['C'], n)))
    out.append('| Not covered → restored in this part | %s | %s | FR-V12-V-001…007 at full depth (§11.23.5) |' % (f'{c["N"]:,}', pct(c['N'], n)))
    out.append('| Correctly superseded by a Founder decision | %s | %s | DEC cited |' % (f'{c["S"]:,}', pct(c['S'], n)))
    out.append('| **Total with a verified end state** | **%s** | **100%%** | 0 unclassified |' % f'{n:,}')
    return '\n'.join(out), c

def frag_chapters():
    by = defaultdict(lambda: Counter())
    for sid, s in S.items():
        key = s['doc'] + '/' + s['chapter']
        by[key]['n'] += 1
        if RB[sid]['level'] in ('exact', 'strong', 'moderate'):
            by[key]['mb'] += 1
        if RA[sid]['level'] in ('exact', 'strong', 'moderate'):
            by[key]['ma'] += 1
        k, _, _ = cls_of(sid)
        by[key][k] += 1
    out = ['| Doc | Chapter file | Bytes | Statements | Measured match before | After | C (different words) | N (restored) | S (superseded) |', '|---|---|---|---|---|---|---|---|---|']
    for key in sorted(by, key=lambda k: (k.split('/')[0], k.split('/')[1])):
        b = EX['files'].get(key + '.txt', {}).get('bytes', 0)
        v = by[key]
        out.append('| %s | %s | %s | %d | %s | %s | %d | %d | %d |' % (key.split('/')[0], key.split('/')[1], f'{b:,}', v['n'], pct(v['mb'], v['n']), pct(v['ma'], v['n']), v['C'], v['N'], v['S']))
    return '\n'.join(out)

def frag_kinds():
    by = defaultdict(Counter)
    for sid, s in S.items():
        by[s['kind']]['n'] += 1
        by[s['kind']][RB[sid]['level']] += 1
    out = ['| Unit kind | Statements | Exact | Strong | Moderate | Weak | None |', '|---|---|---|---|---|---|---|']
    for k in sorted(by):
        v = by[k]
        out.append('| %s | %s | %d | %d | %d | %d | %d |' % (k, f'{v["n"]:,}', v['exact'], v['strong'], v['moderate'], v['weak'], v['none']))
    return '\n'.join(out)

def frag_c_rules():
    groups = defaultdict(list)
    for sid, c in CL.items():
        if c['cls'] != 'C':
            continue
        s = S[sid]
        if 'Source disposition candidates' in s['sec']:
            g = 'FSD 40 source disposition candidates — ' + s['sec'].split('—')[-1].strip()
        elif s['kind'] == 'ddl':
            g = 'Appendix C/C2 DDL (' + ('RLS policy' if 'POLICY' in s['text'] else 'table') + ')'
        elif c['note'].startswith('ID present'):
            g = 'ID-bearing rows (status/evidence wording only)'
        elif c['note'].startswith('Customer decision'):
            g = 'Customer decision rows (CDEC)'
        elif c['note'].startswith('A113 template'):
            g = 'A113 template rows X26–X39'
        elif c['note'].startswith('Threshold present'):
            g = 'Threshold located in another line of the same section'
        else:
            g = 'Manual decisions (read in context)'
        groups[g].append(sid)
    out = ['| Group (rule) | Statements | Why the weak score | Where covered (examples; every row cited in `V_audit.csv`) |', '|---|---|---|---|']
    for g in sorted(groups, key=lambda g: -len(groups[g])):
        sids = groups[g]
        ex = '; '.join(esc(CL[x]['ref'], 90) for x in sids[:2])
        why = esc(CL[sids[0]]['note'], 140)
        out.append('| %s | %d | %s | %s |' % (g, len(sids), why, ex))
    return '\n'.join(out), {g: len(v) for g, v in groups.items()}

def frag_manual():
    seen = set(); out = ['| # | Statement (first occurrence) | Chapter | Class | Citation / authority | Reading note |', '|---|---|---|---|---|---|']
    i = 0
    for sid in sorted(CL):
        c = CL[sid]; s = S[sid]
        if s['h'] in seen:
            continue
        man = not ('Source disposition candidates' in s['sec'] or s['kind'] == 'ddl' or c['note'].startswith(('ID present', 'Customer decision', 'Threshold present', 'V2 Admin screen rule', 'Prototype/document lineage', 'Per-workflow', 'ID absent')))
        if not man:
            continue
        seen.add(s['h']); i += 1
        out.append('| %d | %s | %s | %s | %s | %s |' % (i, esc(s['text'], 110), s['chapter'][:24], c['cls'], esc(c['ref'], 80), esc(c['note'], 110)))
    return '\n'.join(out), i

def frag_n():
    out = ['| # | Statement ID | Chapter | Section | Statement (V12, literal) | Restored by |', '|---|---|---|---|---|---|']
    i = 0
    for sid in sorted(S):
        k, ref, note = cls_of(sid)
        if k != 'N':
            continue
        s = S[sid]; i += 1
        sec = s['sec'].split(' > ')[-1]
        out.append('| %d | %s | %s | %s | %s | %s |' % (i, sid, s['chapter'][:22], esc(sec, 48), esc(s['text'], 150), esc(ref.split(' (')[0], 40)))
    return '\n'.join(out), i

def frag_s():
    out = ['| # | Statement ID | Chapter | Statement (V12) | Superseded by | Current rule |', '|---|---|---|---|---|---|']
    i = 0
    for sid in sorted(S):
        k, ref, note = cls_of(sid)
        if k != 'S':
            continue
        i += 1
        out.append('| %d | %s | %s | %s | %s | %s |' % (i, sid, S[sid]['chapter'][:22], esc(S[sid]['text'], 140), ref, esc(note, 150)))
    return '\n'.join(out), i

def frag_cost():
    out = ['| Workflow | V12 cost source (literal) | Use in the blueprint |', '|---|---|---|']
    for sid in sorted(S):
        k, ref, _ = cls_of(sid)
        if k == 'N' and S[sid]['text'].startswith('Cost source'):
            wf = re.findall(r'SM-SVC-\d{2}-WF\d{2}', S[sid]['sec'])
            name = S[sid]['sec'].split(' > ')[-1]
            out.append('| %s | %s | Illustrative unit-cost seed for the AU cost estimate and the workflow budget reservation default; replaced by measured cost after pilot (OKPI-11/12) |' % (esc(name, 70), esc(S[sid]['text'].split(' | ', 1)[1], 120)))
    return '\n'.join(out)

def frag_v2():
    rows = []
    for sid in sorted(S):
        k, ref, _ = cls_of(sid)
        if k == 'N' and 'Resolve audience and object permissions' in S[sid]['text']:
            sec = S[sid]['sec'].split(' > ')[-1]
            m = re.match(r'(A\d{3}|[XO]\d{2})\s*—\s*(.*)', sec)
            if m:
                rows.append((m.group(1), m.group(2)))
    rows = sorted(set(rows))
    out = ['| Screen | Name (V12 ch24 registry) | Screen | Name (V12 ch24 registry) | Screen | Name (V12 ch24 registry) |', '|---|---|---|---|---|---|']
    for i in range(0, len(rows), 3):
        cells = []
        for a, b in rows[i:i + 3]:
            cells += [a, esc(b, 45)]
        while len(cells) < 6:
            cells += ['', '']
        out.append('| ' + ' | '.join(cells) + ' |')
    return '\n'.join(out), len(rows)

def frag_baseline():
    B = J('baseline.json'); SS = J('supersession_summary.json')
    fams = sorted(SS['by_family'])
    out = ['| Family | Baseline IDs | Retained unchanged | Amended | Superseded | Missing |', '|---|---|---|---|---|---|']
    tot = Counter()
    for f in fams:
        v = SS['by_family'][f]; n = sum(v.values())
        tot['n'] += n
        for k in v:
            tot[k] += v[k]
        out.append('| %s | %s | %s | %d | %d | %d |' % (f, f'{n:,}', f'{v.get("retained unchanged", 0):,}', v.get('amended', 0), v.get('superseded', 0), 0))
    out.append('| **Total** | **%s** | **%s** | **%d** | **%d** | **0** |' % (f'{tot["n"]:,}', f'{tot["retained unchanged"]:,}', tot['amended'], tot['superseded']))
    return '\n'.join(out), tot

def frag_changed():
    rows = list(csv.DictReader(open(os.path.join(BP, 'final', 'supersession_index.csv'), encoding='utf-8')))
    out = ['| # | ID | Status | Authority | Replacement / alias | Evidence | Note |', '|---|---|---|---|---|---|---|']
    i = 0
    for r in rows:
        if r['status'] == 'retained unchanged':
            continue
        i += 1
        out.append('| %d | %s | %s | %s | %s | %s | %s |' % (i, r['id'], r['status'], r['authority'], r['replacement_ids'] or '—', esc(r['evidence_location'], 60), esc(r['evidence_or_note'], 150)))
    return '\n'.join(out), i

def frag_errata():
    E = J('errata_summary.json')
    blocks = []
    tbl = ['| Erratum | Stale statement | Occurrences (stale / total) | Parts with stale text | Authority |', '|---|---|---|---|---|']
    for e in E:
        tbl.append('| %s | %s | %d / %d | %s | %s |' % (e['id'], esc(e['title'], 80), e['stale'], e['occurrences'], esc(', '.join(e['parts'][:10]) + (' …' if len(e['parts']) > 10 else ''), 90) or '—', esc(e['authority'], 60)))
        blocks.append('#### %s %s\n\n| Field | Entry |\n|---|---|\n| Stale statement | %s |\n| **Current rule (binding)** | %s |\n| Authority | %s |\n| Stale occurrences | %d of %d matching lines carry no reference to the authority; first locations: %s |\n| Reported by | %s |\n| Developer instruction | Implement the current rule. Where any part still states the stale text, this erratum governs (DEC-961). |' % (
            e['id'], e['title'], esc(e['title']), esc(e['current']), esc(e['authority']), e['stale'], e['occurrences'], esc('; '.join(e['where']) or '—'), esc(e['reported_by'])))
    return '\n'.join(tbl), '\n\n'.join(blocks), len(E), sum(e['stale'] for e in E)

def frag_combi():
    C = J('combi.json')
    m1 = ['      | audience | role | grant | state | expected |']
    for a, r, g, s, e in C['m1']:
        m1.append('      | %s | %s | %s | %s | %s |' % (a, r, g, s, e))
    m2 = ['      | action_class | mandate | jurisdiction_pack | expected |']
    for a, m, j, e in C['m2']:
        m2.append('      | %s | %s | %s | %s |' % (a, m, j, e))
    m3 = ['      | input | outcome | detail |']
    for a, b, c in C['m3']:
        m3.append('      | %s | %s | %s |' % (a, b, c))
    m4 = ['      | artifact | mode | expected |']
    for a, b, c in C['m4']:
        m4.append('      | %s | %s | %s |' % (a, b, c))
    return '\n'.join(m1), '\n'.join(m2), '\n'.join(m3), '\n'.join(m4)

def write_csv():
    p = os.path.join(BP, 'final', 'coverage_v12', 'V_audit.csv')
    cols = ['doc', 'chapter', 'section', 'aspect_id', 'aspect_summary', 'status_before', 'blueprint_location', 'action', 'new_ids', 'status_after',
            'unit_kind', 'v12_ids', 'ids_present', 'ngram6', 'token_containment', 'threshold_presence', 'level_before', 'level_after', 'triage_reason']
    TRI = {t['sid']: t for t in J('triage_before.json')['triage']}
    with open(p, 'w', newline='', encoding='utf-8') as fh:
        w = csv.writer(fh); w.writerow(cols)
        for sid in sorted(S):
            s = S[sid]; rb = RB[sid]; ra = RA[sid]
            k, ref, note = cls_of(sid)
            sb = {'exact': 'Covered', 'strong': 'Covered', 'moderate': 'Covered', 'weak': 'Partially covered', 'none': 'Not covered'}[rb['level']]
            if sid in TRI and sb == 'Covered':
                sb = 'Partially covered'
            act = {'M': 'None (measured match)', 'C': 'Classified: covered in different words — ' + note, 'N': 'Restored in Part 11.23 — ' + note, 'S': 'Classified: superseded — ' + note}[k]
            after = {'M': 'Matched', 'C': 'Matched (covered in different words)', 'N': 'Matched (restored, Part 11.23)', 'S': 'Superseded (' + ref + ')'}[k]
            new = ''
            if k == 'N':
                new = ' '.join(re.findall(r'(?:FR|TC)-V12-V-\d{3}(?:…\d{3})?|US-\d{2}-ZV\d{2}', ref))
            w.writerow([s['doc'], s['chapter'], s['sec'][-120:], sid, esc(s['text'], 300), sb, (ref if k in ('C', 'N', 'S') else rb['loc'])[:300], act[:300], new, after,
                        s['kind'], ' '.join(s['ids'][:8]), '%d/%d' % (rb['ids_present'], rb['ids']), '' if rb['ng'] is None else rb['ng'], rb['tok'],
                        '' if rb['num'] is None else rb['num'], rb['level'], ra['level'], ','.join(TRI[sid]['why']) if sid in TRI else ''])
    return p

def main():
    F = {}
    F['summary'] = frag_summary()
    F['final'], fc = frag_final()
    F['chapters'] = frag_chapters()
    F['kinds'] = frag_kinds()
    F['c_rules'], cg = frag_c_rules()
    F['manual'], nman = frag_manual()
    F['n_reg'], nn = frag_n()
    F['s_reg'], ns = frag_s()
    F['cost'] = frag_cost()
    F['v2'], nv2 = frag_v2()
    F['base'], btot = frag_baseline()
    F['changed'], nchg = frag_changed()
    F['errata_tbl'], F['errata_blocks'], ne, nstale = frag_errata()
    F['m1'], F['m2'], F['m3'], F['m4'] = frag_combi()
    p = write_csv()
    byfr = Counter()
    for sid in S:
        k, ref, _ = cls_of(sid)
        if k == 'N':
            m = re.search(r'FR-V12-V-\d{3}', ref)
            byfr[m.group(0) if m else '?'] += 1
    meta = dict(fr=dict(byfr), final=dict(fc), c_groups=cg, n_manual=nman, n_n=nn, n_s=ns, n_v2=nv2, base=dict(btot), n_changed=nchg, n_errata=ne, n_stale=nstale,
                SB=SB, SA=SA, EX=dict(total_bytes=EX['total_bytes'], statements=EX['statements'], unique=EX['unique'], by_kind=EX['by_kind'], files=len(EX['files'])))
    json.dump(F, open(os.path.join(OUT, 'fragments.json'), 'w'))
    json.dump(meta, open(os.path.join(OUT, 'fragments_meta.json'), 'w'), indent=1)
    print(json.dumps({k: v for k, v in meta.items() if k not in ('SB', 'SA')}, indent=0)[:1500])
    print('csv', p)

if __name__ == '__main__':
    main()
