"""Group J: parse doc 33 (training manual) - nav guide entries and practice table rows."""
import re, json, sys, glob
D = sys.argv[1]
p = glob.glob(D + '/33_*.txt')[0]
L = open(p, encoding='utf-8').read().split('\n')
# nav guide
nav = []
i = 0
while i < len(L):
    m = re.match(r'<Heading2> ([WA]\d{2,3})\s+(.*)', L[i])
    if m and i < 448:
        acc = L[i+1]
        steps = L[i+2]
        am = re.match(r'Access: ([^.]+)\. (.*)', acc)
        nav.append(dict(id=m.group(1), title=m.group(2).strip(), access=am.group(1) if am else acc, purpose=am.group(2) if am else '', steps=steps))
    i += 1
# practice table: lines 482..1180
rows = []
start = None
for k, l in enumerate(L):
    if l.startswith('Use the actual proposed screen names'):
        start = k
        break
k = start + 1
assert L[k] == '[TABLE]'
k += 1
hdr = L[k:k+4]; k += 4
cur = []
while L[k] != '[/TABLE]':
    if L[k] == '---row':
        if cur: rows.append(cur)
        cur = []
    else:
        cur.append(L[k])
    k += 1
if cur: rows.append(cur)
prac = []
for r in rows:
    if len(r) < 4: continue
    first = r[0]
    m = re.match(r'([WA]\d{2,3}) (.*)', first)
    sid = m.group(1)
    rest = m.group(2)
    # trainee persona glued at end: find known personas
    personas = ['Anonymous visitor','Authorized external user','Authorized employee','Administrator','Approver','Support operator','Owner','Authorized administrator','Security administrator','Finance approver','Authorized approver']
    trainee = ''
    for pz in sorted(set(re.findall(r'[a-z\)]([A-Z][A-Za-z /]+)$', rest))):
        pass
    mm = re.search(r'([a-z0-9\)])([A-Z][a-z]+(?: [a-z/]+)*(?: [A-Za-z/]+)*)$', rest)
    title, trainee = rest, ''
    for n in range(len(rest)-1, 0, -1):
        if rest[n].isupper() and rest[n-1].islower() or (rest[n].isupper() and rest[n-1] in ')'):
            title, trainee = rest[:n], rest[n:]
            break
    prac.append(dict(id=sid, title=title, trainee=trainee, procedure=r[1], success=r[2], uat=r[3]))
json.dump(dict(nav=nav, practice=prac, header=hdr), open(sys.argv[2], 'w'), indent=1)
print('nav', len(nav), 'practice', len(prac), 'hdr', hdr)
from collections import Counter
print(Counter(n['access'] for n in nav))
print(Counter(p['trainee'] for p in prac))
print(prac[0]['uat'], prac[-1]['uat'], prac[-1]['id'])
