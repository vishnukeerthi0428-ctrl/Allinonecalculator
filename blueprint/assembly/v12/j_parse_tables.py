"""Group J (R9): parse FSD V12 [TABLE] blocks into row dicts.
Usage: python3 j_parse_tables.py <file> -> prints JSON summary; importable."""
import sys, json, re
def parse(path):
    lines = open(path, encoding='utf-8').read().split('\n')
    heads = []  # stack of current headings
    tables = []; cur=None; row=None; h1=h2=h3=''
    for i,l in enumerate(lines):
        m = re.match(r'<Heading(\d)>\s*(.*)', l)
        if m:
            lv=int(m.group(1)); t=m.group(2).strip()
            if lv==1: h1,h2,h3=t,'',''
            elif lv==2: h2,h3=t,''
            else: h3=t
            continue
        if l.strip()=='[TABLE]':
            cur={'start':i+1,'h1':h1,'h2':h2,'h3':h3,'rows':[]}; row=None; continue
        if l.strip()=='[/TABLE]':
            if row is not None: cur['rows'].append(row)
            tables.append(cur); cur=None; row=None; continue
        if cur is not None:
            if l.strip()=='---row':
                if row is not None: cur['rows'].append(row)
                row=[]; continue
            if row is not None: row.append(l)
    for t in tables:
        t['header']=t['rows'][0] if t['rows'] else []
        t['data']=t['rows'][1:]
    return tables
if __name__=='__main__':
    ts=parse(sys.argv[1])
    for k,t in enumerate(ts):
        ids=[r[0] for r in t['data'] if r]
        print(k, t['start'], '|', t['h2'][:40], '|', t['h3'][:40], '| hdr=', t['header'][:8], '| n=',len(t['data']), '| ids', ids[:2], ids[-1:] )
