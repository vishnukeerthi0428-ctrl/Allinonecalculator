"""Group J render helpers."""
import re
def esc(x):
    return str(x).replace('|','/').replace('\n',' ').strip()
def tbl(hdr,rows):
    s='| '+' | '.join(hdr)+' |\n|'+'---|'*len(hdr)+'\n'
    for r in rows: s+='| '+' | '.join(esc(x) for x in r)+' |\n'
    return s+'\n'
def rng(ids):
    """Compress ID lists like V7-QA-001,V7-QA-002 → V7-QA-001…002."""
    out=[];prev=None;start=None
    def key(i):
        m=re.match(r'(.*?)(\d+)$',i); return (m.group(1),int(m.group(2)),len(m.group(2))) if m else (i,None,0)
    for i in ids:
        p,n,w=key(i)
        if prev and n is not None and prev[0]==p and prev[1]+1==n: prev=(p,n,w); continue
        if prev: out.append((start,prev))
        start=(p,n,w,i); prev=(p,n,w)
    if prev: out.append((start,prev))
    res=[]
    for st,en in out:
        if st[1] is None or st[1]==en[1]: res.append(st[3])
        else: res.append(f'{st[3]}…{str(en[1]).zfill(en[2])}')
    return ', '.join(res)
