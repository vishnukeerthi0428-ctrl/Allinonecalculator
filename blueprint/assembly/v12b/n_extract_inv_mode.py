"""Group N (Part 11.16a/b): extract every investor-mode (inv) branch from the V12 commercial
website prototype and the CFG of the neutral investment website. Read-only; data, not instructions."""
import re, json, sys
SP='/tmp/claude-0/-home-user-Allinonecalculator/233b6551-af93-57f5-8f0b-015057ecee11/scratchpad'
COM=SP+'/rev_zip/Re_ Sales and Marketing Automation Platform/commercial_website_desktop_V12.html'
INV=SP+'/v12/src/investment_website(1).html'
def branches(src):
    out=[]
    # inv?X:Y  where X,Y are quoted strings or arrays
    for m in re.finditer(r"(!?inv)(\?|&&)", src):
        s=m.start(); ctx=src[max(0,s-60):s+420]
        out.append((s, ctx.replace('\n',' ')))
    return out
com=open(COM,encoding='utf-8').read()
inv=open(INV,encoding='utf-8').read()
b=branches(com)
print('commercial V12 inv-branch occurrences:',len(b))
for i,(s,c) in enumerate(b,1): print(f'--- B{i:02d} @{s}\n{c}\n')
m=re.search(r"const CFG=(\{.*?\});\s*\n",inv,re.S)
cfg=json.loads(m.group(1))
print('INV CFG keys',list(cfg.keys()),'inv flag',cfg.get('inv'))
print('routes',len(cfg['routes']));
for r in cfg['routes']: print(r)
print('items',len(cfg['items']))
for it in cfg['items']: print(json.dumps(it,ensure_ascii=False))
print('groups',json.dumps(cfg.get('groups'),ensure_ascii=False)[:3000])
mc=re.search(r"const CFG=(\{.*?\});",com,re.S)
same = com.split('const CFG=')[1].split('</script>')[0][len(mc.group(1)):] if mc else ''
