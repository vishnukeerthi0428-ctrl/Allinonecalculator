"""V-01: extract every requirement-like statement from the V12 normative chapters (BRD/ and FSD/, ZZ_* annex excluded).
Units: prose sentences with a modal / ID / number; every non-header table row; ID-bearing headings;
OpenAPI operations (App. A, A2); DTO schemas (App. B); SQL statements (App. C, C2)."""
import os, re, json, glob, hashlib
from v_common import V12, OUT, ids_in, numbers_in, toks

MODAL = re.compile(r'\b(shall|must|should|required|requires|require|mandatory|never|only|cannot|can ?not|may not|blocking|blocked|prohibited|forbidden|at least|at most|no more than|within|minimum|maximum|limit|cap|threshold|target)\b', re.I)

def chapter_of(path):
    b = os.path.basename(path)
    return b[:-4]

def split_sentences(line):
    parts = re.split(r'(?<=[.;])\s+(?=[A-Z(“"])', line)
    return [p.strip() for p in parts if p.strip()]

def parse_text(path, doc):
    out = []
    h = ['', '', '', '']
    in_table = False; row = []; header = None; rows_seen = 0
    lines = open(path, encoding='utf-8', errors='replace').read().split('\n')
    def flush_row(ln):
        nonlocal header, rows_seen
        if not row:
            return
        cells = [c.strip() for c in row if c.strip()]
        if not cells:
            return
        if rows_seen == 0:
            header = cells
        else:
            out.append(dict(kind='row', text=' | '.join(cells), header=' | '.join(header or []), sec=' > '.join(x for x in h if x), line=ln))
        rows_seen += 1
    cur_ln = 0
    for i, raw in enumerate(lines, 1):
        s = raw.strip()
        m = re.match(r'<Heading(\d)>\s*(.*)', s)
        if m:
            lvl = int(m.group(1)); title = m.group(2).strip()
            if 1 <= lvl <= 4:
                h[lvl - 1] = title
                for k in range(lvl, 4):
                    h[k] = ''
            if ids_in(title) and lvl >= 2:
                out.append(dict(kind='heading', text=title, header='', sec=' > '.join(x for x in h[:lvl - 1] if x), line=i))
            continue
        if s == '[TABLE]':
            in_table = True; row = []; header = None; rows_seen = 0; continue
        if s == '[/TABLE]':
            flush_row(cur_ln); in_table = False; row = []; continue
        if in_table:
            if s == '---row':
                flush_row(cur_ln); row = []; cur_ln = i
            else:
                row.append(s)
            continue
        if not s:
            continue
        for sent in split_sentences(s):
            if len(toks(sent)) < 3 and not ids_in(sent):
                continue
            if MODAL.search(sent) or ids_in(sent) or numbers_in(sent):
                out.append(dict(kind='prose', text=sent, header='', sec=' > '.join(x for x in h if x), line=i))
    return out

def parse_openapi(path):
    out = []
    lines = open(path, encoding='utf-8').read().split('\n')
    p = None; meth = None; op = None
    head = ''
    for i, l in enumerate(lines, 1):
        m = re.match(r'^  (/[^:]*):\s*$', l)
        if m:
            p = m.group(1); continue
        m = re.match(r'^    (get|post|put|patch|delete):\s*$', l)
        if m and p:
            meth = m.group(1).upper(); op = dict(kind='api', text='', header='', sec='paths', line=i, path=p, method=meth, opid='', summary=''); out.append(op); continue
        m = re.match(r'^      operationId:\s*(\S+)', l)
        if m and op is not None:
            op['opid'] = m.group(1)
        m = re.match(r'^      summary:\s*"?(.*?)"?\s*$', l)
        if m and op is not None:
            op['summary'] = m.group(1)
        if l.startswith('      x-idempotency') and op is not None:
            op['idem'] = True
    for o in out:
        o['text'] = '%s %s (%s) %s%s' % (o['method'], o['path'], o['opid'], o['summary'], '; Idempotency-Key required' if o.get('idem') else '')
    # prose header lines before 'openapi:' are captured by parse_text-like handling
    for i, l in enumerate(lines[:4], 1):
        if l.strip() and not l.startswith('<Heading') and not l.startswith('openapi'):
            out.append(dict(kind='prose', text=l.strip(), header='', sec='preamble', line=i))
    return out

def parse_dto(path):
    out = []
    for i, l in enumerate(open(path, encoding='utf-8'), 1):
        l = l.strip()
        if l.startswith('{'):
            try:
                j = json.loads(l)
            except Exception:
                continue
            wid = j.get('$id', '').split(':')[3] if j.get('$id', '').count(':') >= 3 else j.get('$id', '')
            inp = j['$defs']['input']; outp = j['$defs']['output']
            out.append(dict(kind='dto', text='%s DTO input required [%s] output required [%s]' % (wid, ', '.join(inp.get('required', [])), ', '.join(outp.get('required', []))),
                            header='', sec='Appendix B', line=i, wf=wid, fields=list(inp.get('properties', {})) + list(outp.get('properties', {}))))
        elif l and not l.startswith('<Heading'):
            out.append(dict(kind='prose', text=l, header='', sec='Appendix B preamble', line=i))
    return out

def parse_sql(path):
    out = []
    buf = []; start = 0; in_dollar = False; sec = ''
    for i, l in enumerate(open(path, encoding='utf-8'), 1):
        s = l.rstrip('\n')
        if s.startswith('<Heading'):
            sec = re.sub(r'<Heading\d>\s*', '', s); continue
        if not buf:
            if not s.strip() or (s.strip().startswith('--') and not in_dollar):
                if s.strip().startswith('--') and len(s.strip()) > 8:
                    out.append(dict(kind='prose', text=s.strip().lstrip('-').strip(), header='', sec=sec, line=i))
                continue
            if not re.match(r'\s*(CREATE|ALTER|INSERT|GRANT|REVOKE|COMMENT|DROP|SELECT|DO|SET|BEGIN|COMMIT|REFRESH)\b', s, re.I) and not in_dollar:
                if re.search(r'[A-Za-z]{4}', s):
                    out.append(dict(kind='prose', text=s.strip(), header='', sec=sec, line=i))
                continue
            start = i
        buf.append(s)
        if s.count('$$') % 2 == 1:
            in_dollar = not in_dollar
        code = s.split('--')[0].rstrip()
        if not in_dollar and code.endswith(';'):
            stmt = ' '.join(x.strip() for x in buf)
            for part in re.split(r';\s+(?=(?:ALTER|CREATE|INSERT|GRANT|REVOKE|COMMENT)\b)', stmt):
                out.append(dict(kind='ddl', text=part.strip(), header='', sec=sec or 'DDL', line=start))
            buf = []
    return out

def main():
    stmts = []
    files = []
    for doc in ('BRD', 'FSD'):
        for f in sorted(glob.glob(os.path.join(V12, doc, '*.txt'))):
            b = os.path.basename(f)
            if b.startswith('ZZ_'):
                continue
            files.append((doc, f))
    stats = {}
    for doc, f in files:
        b = os.path.basename(f)
        if b.startswith('AP_Appendix_A'):
            items = parse_openapi(f)
        elif b.startswith('AP_Appendix_B'):
            items = parse_dto(f)
        elif b.startswith('AP_Appendix_C'):
            items = parse_sql(f)
        else:
            items = parse_text(f, doc)
        for it in items:
            it['doc'] = doc; it['chapter'] = chapter_of(f)
            it['ids'] = ids_in(it['text'])
            it['nums'] = numbers_in(it['text'])
            it['h'] = hashlib.md5(re.sub(r'\W+', ' ', it['text'].lower()).strip().encode()).hexdigest()[:12]
        stats[doc + '/' + b] = dict(bytes=os.path.getsize(f), statements=len(items))
        stmts.extend(items)
    for n, s in enumerate(stmts, 1):
        s['sid'] = 'VS-%06d' % n
    json.dump(stmts, open(os.path.join(OUT, 'statements.json'), 'w'))
    tot_bytes = sum(v['bytes'] for v in stats.values())
    uniq = len({s['h'] for s in stmts})
    json.dump(dict(files=stats, total_bytes=tot_bytes, statements=len(stmts), unique=uniq,
                   by_kind={k: sum(1 for s in stmts if s['kind'] == k) for k in sorted({s['kind'] for s in stmts})}),
              open(os.path.join(OUT, 'extract_summary.json'), 'w'), indent=1)
    print(len(files), 'files', tot_bytes, 'bytes', len(stmts), 'statements', uniq, 'unique')

if __name__ == '__main__':
    main()
