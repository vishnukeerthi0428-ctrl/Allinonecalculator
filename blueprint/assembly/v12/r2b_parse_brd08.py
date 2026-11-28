"""R2/B: parse BRD V12 ch.08 per-service field tables. Usage: python3 -I r2b_parse_brd08.py <brd08.txt> <out.json>"""
import sys, json, re
lines = open(sys.argv[1], encoding='utf-8').read().split('\n')
svc = {}; cur = None; i = 0
while i < len(lines):
    l = lines[i]
    m = re.match(r'<Heading2> (SM-SVC-\d\d) — (.*)', l)
    if m: cur = m.group(1); svc[cur] = {'name': m.group(2)}
    elif l == '---row' and cur:
        k = lines[i+1]; v = lines[i+2]
        if k != 'Requirement / field': svc[cur][k] = v
        i += 2
    i += 1
json.dump(svc, open(sys.argv[2], 'w'), indent=1, ensure_ascii=False)
print(len(svc), 'services;', sorted({k for s in svc.values() for k in s}))
