"""Group K parser: parse [TABLE] blocks with section context from V12 FSD text files."""
import re, sys, json
def parse(path):
    lines = open(path, encoding='utf-8').read().split('\n')
    secs = []  # stack
    tables = []; prose = []
    i = 0; h = {1:'',2:'',3:''}
    while i < len(lines):
        l = lines[i]
        m = re.match(r'<Heading(\d)> (.*)', l)
        if m:
            lv = int(m.group(1)); h[lv] = m.group(2)
            for k in range(lv+1, 4): h[k] = ''
            i += 1; continue
        if l == '[TABLE]':
            rows = []; cur = None; start = i+1
            i += 1
            while i < len(lines) and lines[i] != '[/TABLE]':
                if lines[i] == '---row':
                    if cur is not None: rows.append(cur)
                    cur = []
                else:
                    cur.append(lines[i])
                i += 1
            if cur is not None: rows.append(cur)
            tables.append({'h2': h[2], 'h3': h[3], 'line': start, 'header': rows[0] if rows else [], 'rows': rows[1:]})
            i += 1; continue
        if l.strip():
            prose.append({'h2': h[2], 'h3': h[3], 'line': i+1, 'text': l})
        i += 1
    return tables, prose
if __name__ == '__main__':
    t, p = parse(sys.argv[1])
    for x in t:
        print(x['line'], '|', x['h2'], '|', x['h3'], '| hdr=', x['header'], '| rows=', len(x['rows']), '| ragged=', sum(1 for r in x['rows'] if len(r)!=len(x['header'])))
    print('prose lines', len(p))
