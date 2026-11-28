"""Group W (Part 11.24) shared helpers: paths, markdown table parsing, output locations."""
import glob, os, re, json

B = '/home/user/Allinonecalculator/blueprint/'
OUT = B + 'final/build/'
V12 = B + 'assembly/v12/'
FRAG = B + 'assembly/v12b/w_frag/'
os.makedirs(OUT, exist_ok=True)
os.makedirs(FRAG, exist_ok=True)


def part(prefix):
    """Return the single Part-*.md file whose name starts with prefix (e.g. 'Part-03-2_')."""
    c = sorted(glob.glob(B + prefix + '*.md'))
    if not c:
        raise FileNotFoundError(prefix)
    return c


def cells(line):
    """Split a markdown table row into stripped cells (no leading/trailing empty)."""
    s = line.strip()
    if not s.startswith('|'):
        return None
    s = s[1:-1] if s.endswith('|') else s[1:]
    # protect escaped pipes
    s = s.replace('\\|', '\u2502')
    return [c.strip().replace('\u2502', '|') for c in s.split('|')]


def tables(path):
    """Yield (heading_stack, header_cells, rows[cells], first_line_no) for every markdown table in a file."""
    L = open(path, encoding='utf-8').read().split('\n')
    heads = {}
    i = 0
    while i < len(L):
        m = re.match(r'^(#{1,6})\s+(.*)', L[i])
        if m:
            lvl = len(m.group(1))
            heads = {k: v for k, v in heads.items() if k < lvl}
            heads[lvl] = m.group(2).strip()
        if L[i].startswith('|') and i + 1 < len(L) and re.match(r'^\|\s*:?-{2,}', L[i + 1]):
            hdr = cells(L[i])
            rows = []
            j = i + 2
            while j < len(L) and L[j].startswith('|'):
                rows.append(cells(L[j]))
                j += 1
            yield dict(heads), hdr, rows, i + 1
            i = j
            continue
        i += 1


def write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(text)


def md_table(header, rows):
    out = ['| ' + ' | '.join(header) + ' |', '|' + '|'.join(['---'] * len(header)) + '|']
    for r in rows:
        out.append('| ' + ' | '.join(str(x).replace('|', '\\|').replace('\n', ' ') for x in r) + ' |')
    return '\n'.join(out) + '\n'


def save_json(name, obj):
    write(FRAG + name, json.dumps(obj, indent=1, ensure_ascii=False))


def load_json(name):
    return json.load(open(FRAG + name, encoding='utf-8'))
