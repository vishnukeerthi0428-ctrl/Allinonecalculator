"""Parse V12 text format ([TABLE] / ---row / [/TABLE], one cell per line) into table records.
Usage: python3 -I parse_tables.py <file> -> prints JSON list of {heading, header, rows}"""
import sys, json
def parse(path):
    lines = open(path, encoding='utf-8').read().split('\n')
    out, heading, i = [], [], 0
    prose = []
    while i < len(lines):
        l = lines[i]
        if l.startswith('<Heading'):
            lvl = int(l[8]); heading = heading[:lvl-1] + [l.split('>',1)[1].strip()]
        elif l.strip() == '[TABLE]':
            rows, cur = [], None
            i += 1
            while i < len(lines) and lines[i].strip() != '[/TABLE]':
                if lines[i].strip() == '---row':
                    if cur is not None: rows.append(cur)
                    cur = []
                elif cur is not None:
                    cur.append(lines[i])
                i += 1
            if cur is not None: rows.append(cur)
            out.append({'heading': ' > '.join(heading), 'header': rows[0] if rows else [], 'rows': rows[1:]})
        elif l.strip():
            prose.append({'heading': ' > '.join(heading), 'text': l})
        i += 1
    return out, prose
if __name__ == '__main__':
    t, p = parse(sys.argv[1])
    json.dump({'tables': t, 'prose': p}, sys.stdout, ensure_ascii=False, indent=0)
