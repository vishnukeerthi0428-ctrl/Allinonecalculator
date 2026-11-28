"""Group R11 / letter L -- shared helpers for the V12 historical-annex / V1 / source-archive
completeness audit (Part 11.12).

Normalisation, unit extraction (text, CSV, JSON, HTML), 6-gram shingling, requirement-likeness.
All scripts must run with PYTHONHASHSEED=0 (see L_run_all.sh) so hashed shingles are stable.
"""
import csv, json, os, re, sys, unicodedata, glob

csv.field_size_limit(10 ** 9)

SCR = '/tmp/claude-0/-home-user-Allinonecalculator/233b6551-af93-57f5-8f0b-015057ecee11/scratchpad'
V12 = SCR + '/v12'
SRC = V12 + '/src'
DOCS38 = SCR + '/docs38'
BP = '/home/user/Allinonecalculator/blueprint'
OUT = SCR + '/v12_L'
os.makedirs(OUT, exist_ok=True)

N = 6  # shingle size

_DASH = re.compile('[‐-―−]')
_TOK = re.compile(r'[a-z0-9]+')
ID_RE = re.compile(r'\b[A-Z][A-Z0-9]{0,9}(?:-[A-Z0-9]{1,12}){1,5}\b')
MODAL_RE = re.compile(r'\b(shall|must|should|required|mandatory|never|only|cannot|may not|no more than|at least|at most|within)\b', re.I)
NUM_RE = re.compile(r'(\d[\d,.]*\s*(%|ms|s\b|sec|min|minutes|hours|h\b|days|d\b|months|lakh|crore|pd|gb|mb|tb|rps|tps|x\b)|[₹$]\s*\d|[<>≤≥]=?\s*\d|\b\d+(\.\d+)?\b)', re.I)


def norm(s):
    s = unicodedata.normalize('NFKC', s)
    s = _DASH.sub('-', s)
    s = s.replace('≤', ' <= ').replace('≥', ' >= ').replace('₹', ' inr ')
    return s.lower()


def toks(s):
    return _TOK.findall(norm(s))


def shingles(t, n=N):
    return {hash(' '.join(t[i:i + n])) for i in range(len(t) - n + 1)}


def ngram_hash(t):
    return hash(' '.join(t))


def req_like(text, is_row=False):
    """Return a short code for why a unit is requirement-like ('' if not)."""
    why = []
    if MODAL_RE.search(text):
        why.append('modal')
    if ID_RE.search(text):
        why.append('id')
    if NUM_RE.search(text):
        why.append('num')
    if is_row:
        why.append('row')
    return '+'.join(why)


_SENT = re.compile(r'(?<=[.;!?])\s+(?=[A-Z0-9“"(])')
HEAD = re.compile(r'^<Heading(\d)>\s*')


def split_sentences(line):
    if len(line) < 220:
        return [line]
    parts = [p.strip() for p in _SENT.split(line) if p.strip()]
    return parts or [line]


def text_units(path, label):
    """Yield (loc, text, is_row, heading) from a <HeadingN>/[TABLE] text file."""
    heading = ''
    in_table = False
    row = []
    rowno = 0
    with open(path, encoding='utf-8', errors='replace') as fh:
        for ln, raw in enumerate(fh, 1):
            line = raw.rstrip('\n').strip()
            if not line:
                continue
            m = HEAD.match(line)
            if m:
                heading = HEAD.sub('', line)[:160]
                yield (f'{label}:{ln}', heading, False, heading)
                continue
            if line == '[TABLE]':
                in_table, row, rowno = True, [], 0
                continue
            if line == '[/TABLE]':
                if row:
                    yield (f'{label}:{ln}', ' | '.join(row), True, heading)
                in_table, row = False, []
                continue
            if in_table:
                if line == '---row':
                    if row:
                        rowno += 1
                        yield (f'{label}:{ln}', ' | '.join(row), True, heading)
                    row = []
                else:
                    row.append(line)
                continue
            for s in split_sentences(line):
                yield (f'{label}:{ln}', s, False, heading)


def csv_units(path, label):
    with open(path, encoding='utf-8-sig', errors='replace', newline='') as fh:
        rows = list(csv.reader(fh))
    if not rows:
        return
    hdr = rows[0]
    for i, r in enumerate(rows, 1):
        cells = [c.strip() for c in r if c and c.strip()]
        if not cells:
            continue
        yield (f'{label}:r{i}', ' | '.join(cells), True, ' | '.join(hdr)[:160])


def _walk_json(o, path, out):
    if isinstance(o, dict):
        scal = []
        for k, v in o.items():
            if isinstance(v, (str, int, float, bool)) and v not in ('', None):
                scal.append(f'{k}: {v}')
            elif isinstance(v, list) and v and all(isinstance(x, (str, int, float)) for x in v):
                scal.append(f'{k}: ' + '; '.join(map(str, v)))
            else:
                _walk_json(v, f'{path}.{k}', out)
        if scal:
            out.append((path, ' | '.join(scal)))
    elif isinstance(o, list):
        for i, v in enumerate(o):
            _walk_json(v, f'{path}[{i}]', out)
    elif isinstance(o, str) and len(o.split()) >= 3:
        out.append((path, o))


def json_units(path, label):
    try:
        d = json.load(open(path, encoding='utf-8', errors='replace'))
    except Exception:
        return
    out = []
    _walk_json(d, '$', out)
    for p, t in out:
        # very long flattened objects (OpenAPI schemas) are split into 600-char windows
        if len(t) > 1500:
            for j in range(0, len(t), 1200):
                yield (f'{label}:{p}#{j}', t[j:j + 1500], True, p[:160])
        else:
            yield (f'{label}:{p}', t, True, p[:160])


_TAG = re.compile(r'<[^>]+>')
_JSSTR = re.compile(r'"((?:[^"\\]|\\.){12,})"|\'((?:[^\'\\]|\\.){12,})\'|`((?:[^`\\]|\\.){12,})`')


def html_units(path, label):
    html = open(path, encoding='utf-8', errors='replace').read()
    seen = set()
    # visible text outside <script>/<style>
    body = re.sub(r'(?is)<(script|style)[^>]*>.*?</\1>', ' ', html)
    for chunk in re.split(r'(?i)<(?:p|div|li|h\d|td|th|tr|section|article|button|label|option|span|a)\b', body):
        t = re.sub(r'\s+', ' ', _TAG.sub(' ', chunk)).strip()
        if len(t.split()) >= 2 and t not in seen:
            seen.add(t)
            yield (f'{label}:text', t, False, 'html-text')
    # string literals in scripts (screens + data live in embedded JS)
    for sc in re.findall(r'(?is)<script[^>]*>(.*?)</script>', html):
        for m in _JSSTR.finditer(sc):
            t = next(g for g in m.groups() if g)
            t = re.sub(r'\\[nt]', ' ', t)
            t = re.sub(r'\s+', ' ', _TAG.sub(' ', t)).strip()
            if len(t.split()) >= 3 and not re.search(r'[{};=]\s*$|function\s*\(|=>', t) and t not in seen:
                seen.add(t)
                yield (f'{label}:js', t, False, 'html-js')
