"""Group V (Part 11.23) shared helpers: paths, tokenisation, ID and number extraction.
Independent audit: nothing here reads the self-reported coverage CSVs."""
import re, os, glob, json, hashlib
BP = '/home/user/Allinonecalculator/blueprint'
V12 = '/tmp/claude-0/-home-user-Allinonecalculator/233b6551-af93-57f5-8f0b-015057ecee11/scratchpad/v12'
OUT = os.path.join(BP, 'assembly', 'v12b', 'v_out')
os.makedirs(OUT, exist_ok=True)
OWN_PREFIX = 'Part-11-23'   # this part's own files (excluded from the "before" measurement)

STOP = set("""a an the and or of to in on for with by from at as is are be been being was were it its this that these those
which who whom whose what when where how than then there their they them we our you your he she his her not no nor
any all each every per via into onto only same such so do does done can may might shall must should will would could
if else also but both either neither more most less least other others own up down out over under again further once here
very just one two three new use used using within without across before after during between among through about above below""".split())

# Requirement-like IDs: uppercase family with at least one hyphen and one digit, e.g. SM-SVC-06-WF01, ENT-DAT-04, MT-TC-MT-06, V12-QA-002
ID_RE = re.compile(r'(?<![A-Za-z0-9_\-])([A-Z][A-Z0-9]{0,11}(?:-[A-Za-z0-9]{1,12}){1,6})(?![A-Za-z0-9_])')
SCREEN_RE = re.compile(r'(?<![A-Za-z0-9_\-])([AW]\d{3}|W\d{2})(?![A-Za-z0-9_\-])')
NUM_RE = re.compile(r'(?<![A-Za-z0-9\-])(?:₹\s?|\$|€|£)?(\d{1,3}(?:,\d{2,3})+|\d+(?:\.\d+)?)\s*(%|ms|s\b|sec|min|minutes|hours?|h\b|days?|d\b|weeks?|months?|years?|MB|GB|KB|TB|lakh|L\b|k\b|x\b|×)?')
TOK_RE = re.compile(r"[a-z0-9][a-z0-9_]*")
BAD_ID = re.compile(r'^(UTF|ISO|RFC|SHA|AES|TLS|HTTP|HTTPS|PG|JSON|UUID|WCAG|OWASP|OAUTH|NIST|PCI|GDPR|DPDP|COVID|IEC|ECMA|ES|IPV)-')

def norm_id(s):
    return s.strip().upper()

def ids_in(text):
    out = []
    for m in ID_RE.finditer(text):
        t = m.group(1)
        if not re.search(r'\d', t):
            continue
        if re.match(r'^[A-Z]+-\d{4}(-\d{2})?(-\d{2})?$', t) and t.split('-')[0] in ('ISO', 'RFC', 'NIST', 'UTF', 'SHA', 'AES', 'IEC'):
            continue
        if BAD_ID.match(t):
            continue
        out.append(t.upper())
    for m in SCREEN_RE.finditer(text):
        out.append(m.group(1))
    seen = []
    for x in out:
        if x not in seen:
            seen.append(x)
    return seen

def strip_ids(text):
    return SCREEN_RE.sub(' ', ID_RE.sub(' ', text))

UNIT = {'minutes': 'min', 'minute': 'min', 'hour': 'h', 'hours': 'h', 'day': 'd', 'days': 'd', 'week': 'w', 'weeks': 'w',
        'month': 'mo', 'months': 'mo', 'year': 'y', 'years': 'y', 'sec': 's'}

THR_RE = re.compile(r'(?<![A-Za-z0-9\-_@])(≤|≥|<=|>=|<|>|=|±|\bmax(?:imum)?\s|\bmin(?:imum)?\s|\bat least\s|\bat most\s|\bwithin\s|\bup to\s|\bunder\s|\bover\s)?\s*(₹\s?|INR\s?|USD\s?|\$|€|£)?(\d{1,3}(?:,\d{2,3})+|\d+(?:\.\d+)?)\s*(%|ms\b|s\b|sec\b|seconds?\b|min\b|minutes?\b|hours?\b|h\b|days?\b|d\b|weeks?\b|months?\b|years?\b|MB\b|GB\b|KB\b|TB\b|lakh\b|L\b|k\b|×|x\b|/month|/min|/day|/hour|pd\b|tenants?\b|calls?\b|tokens?\b|requests?\b|attempts?\b|retries\b|characters?\b|chars?\b|items?\b|rows?\b|per\b)?', re.I)

def numbers_in(text, thresholds_only=True):
    """Threshold-bearing numbers: carry a unit, a comparator, a currency, or a decimal point.
    Bare integers (chapter numbers, ordinals, row numbers) are ignored when thresholds_only."""
    t = strip_ids(text)
    t = re.sub(r'(?i)\b(chapter|ch|row|table|section|§|sm_op_|op_|part|wave|release|R|V|step|appendix|D|T)\s?\d+', ' ', t)
    t = re.sub(r'@\d+', ' ', t)
    t = re.sub(r'\b[0-9a-f]{12,}\b', ' ', t)
    out = []
    for m in THR_RE.finditer(t):
        cmp_, cur, n, u = m.group(1), m.group(2), m.group(3), m.group(4)
        n = n.replace(',', '')
        try:
            v = float(n)
        except ValueError:
            continue
        u = (u or '').strip().lower()
        u = UNIT.get(u, u)
        if u in ('second', 'seconds'):
            u = 's'
        if u in ('minute',):
            u = 'min'
        if thresholds_only and not (cmp_ or cur or u or '.' in n):
            continue
        key = ('%g' % v) + (u if u not in ('per', 'tenant', 'tenants', 'call', 'calls', 'item', 'items', 'row', 'rows', 'request', 'requests', 'token', 'tokens', 'attempt', 'attempts', 'retries', 'character', 'characters', 'char', 'chars') else '')
        if key not in out:
            out.append(key)
    return out

def numbers_in_old(text):
    t = strip_ids(text)
    out = []
    for m in NUM_RE.finditer(t):
        n = m.group(1).replace(',', '')
        u = (m.group(2) or '').strip()
        u = UNIT.get(u.lower(), u.lower()) if u else ''
        try:
            v = float(n)
        except ValueError:
            continue
        # trivial ordinals / single digits without unit carry no threshold meaning
        if not u and v < 10 and '.' not in n:
            continue
        key = (('%g' % v) + u)
        if key not in out:
            out.append(key)
    return out

def num_keys_loose(text):
    """Numbers in a passage (unit-insensitive set plus unit-qualified set)."""
    ks = set()
    for k in numbers_in(text, thresholds_only=False):
        ks.add(k)
        ks.add(re.match(r'[\d.e+\-]+', k).group(0))
    return ks

def toks(text):
    return TOK_RE.findall(text.lower())

def content_toks(text):
    return [w for w in toks(strip_ids(text)) if w not in STOP and len(w) > 2 and not w.isdigit()]

def stem(w):
    for suf in ('ations', 'ation', 'ingly', 'ments', 'ment', 'ings', 'ing', 'ies', 'ied', 'ed', 'es', 's', 'ly'):
        if len(w) > len(suf) + 3 and w.endswith(suf):
            return w[:-len(suf)]
    return w

def ctoks(text):
    return [stem(w) for w in content_toks(text)]

def shingles(text, n=6):
    w = [stem(x) for x in toks(text)]
    return {hashlib.blake2b((' '.join(w[i:i + n])).encode(), digest_size=8).hexdigest() for i in range(max(0, len(w) - n + 1))}

def part_files(include_own=False):
    fs = sorted(glob.glob(os.path.join(BP, 'Part-*.md')))
    if not include_own:
        fs = [f for f in fs if not os.path.basename(f).startswith(OWN_PREFIX)]
    return fs

def part_label(fname):
    b = os.path.basename(fname)
    m = re.match(r'Part-(\d+)(?:-(\d+))?([a-z]?)([A-Z]?)_', b)
    if not m:
        return b
    p, s, sub, letter = m.groups()
    lab = str(int(p)) + (letter or '')
    if s:
        lab += '.' + str(int(s))
    return lab + (sub or '')
