"""Extract the blueprint API operation inventory (Part 3.2 API-001..555, Part 3.5b API-ENH-D-001..024, Part 9.7b API-ADV-X1-01..40)."""
import re, csv, sys, glob
B='/home/user/Allinonecalculator/blueprint/'
rows=[];seen=set()
def add(i,m,p,ns,purpose,src):
    if i in seen: return
    seen.add(i); rows.append(dict(id=i,method=m,path=p,ns=ns,purpose=purpose,part=src))
for line in open(B+'Part-03-2_API_and_Integration.md',encoding='utf-8'):
    m=re.match(r'^\| (API-\d{3})( ★)? \| (GET|POST|PUT|PATCH|DELETE) \| `([^`]+)` \| ([^|]+) \| ([^|]+) \|',line)
    if m: add(m.group(1),m.group(3),m.group(4),m.group(5).strip(),m.group(6).strip(),'3.2'+(' ★' if m.group(2) else ''))
for line in open(glob.glob(B+'Part-03-5b_*.md')[0],encoding='utf-8'):
    m=re.match(r'^\| (API-ENH-D-\d{3}) \| (GET|POST|PUT|PATCH|DELETE) \| `([^`]+)` \| ([^|]+) \| ([^|]+) \|',line)
    if m: add(m.group(1),m.group(2),m.group(3),m.group(4).strip(),m.group(5).strip(),'3.5b')
for line in open(glob.glob(B+'Part-09-7b_*.md')[0],encoding='utf-8'):
    m=re.match(r'^\| (API-ADV-X1-\d{2}) \| (GET|POST|PUT|PATCH|DELETE) \| `([^`]+)` \| ([^|]+) \|',line)
    if m: add(m.group(1),m.group(2),m.group(3),'admin',m.group(4).strip(),'9.7b')
w=csv.DictWriter(open(sys.argv[1],'w',newline=''),fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
import collections; print(len(rows), collections.Counter(r['part'] for r in rows))
