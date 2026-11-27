"""Group E: extract the blueprint Part 3.3 entity catalogue and column dictionary (ENT -> table, scope, columns)."""
import re, json, sys
src, out = sys.argv[1], sys.argv[2]
T = open(src, encoding='utf-8').read(); L = T.split('\n')
cat = {}
for line in L:
    m = re.match(r'\| (ENT-\d{3}) \| (.+?) \| `(\w+)` \| (.+?) \| (.+?) \| (.+?) \| (.+?) \| (.+?) \| (.+?) \|$', line)
    if m:
        cat[m.group(1)] = dict(ent=m.group(1), logical=m.group(2), table=m.group(3), domain=m.group(4), origin=m.group(5),
                               basis=m.group(6), scope=m.group(7), imm=m.group(8), ret=m.group(9), columns=[], dict_section=None)
STD = {'STD-S': ['id','tenant_id','startup_id','revision','created_at','created_by','created_by_type','updated_at','updated_by','archived_at','archived_by','archive_reason'],
       'STD-SA': ['id','tenant_id','startup_id','created_at','created_by','created_by_type','correlation_id'],
       'STD-V': ['version_no','status','content_hash','approval_id','approved_at','effective_from','effective_to','supersedes_id'],
       'STD-W': ['is_simulated','run_id','correlation_id']}
STD['STD-T'] = STD['STD-S']; STD['STD-X'] = STD['STD-S']
cur = None
for i, line in enumerate(L):
    m = re.match(r'\*\*(ENT-\d{3}) .*?\(`(\w+)`\)\*\*:(.*)', line)
    if m:
        cur = m.group(1); e = cat.get(cur)
        if e is None: continue
        e['dict_section'] = '3.3.6'
        sets = re.findall(r'STD-[A-Z]+', m.group(3))
        std = []
        for s in sets: std += STD.get(s, [])
        if not sets: std = ['id','revision','created_at','created_by','updated_at','updated_by']
        e['std_columns'] = sorted(set(std)); continue
    if cur and line.startswith('| `'):
        cell = line.split('|')[1]
        for nm in re.findall(r'`([a-z_0-9]+)`', cell): cat[cur]['columns'].append(nm)
        continue
    if cur and (line.startswith('## ') or line.startswith('### ')): cur = None
    m2 = re.match(r'\| (ENT-\d{3}) \| `(\w+)` \| (.+?) \| (.+?) \| (.+?) \|$', line)
    if m2 and m2.group(1) in cat:
        e = cat[m2.group(1)]
        e['dict_section'] = '3.3.7'
        sets = re.findall(r'STD-[A-Z]+', m2.group(3)); std = []
        for s in sets: std += STD.get(s, [])
        if not sets: std = ['id','revision','created_at','created_by','updated_at','updated_by']
        e['std_columns'] = sorted(set(std))
        e['columns'] += re.findall(r'`(\w+)`', m2.group(4))
        e['keys_text'] = m2.group(5)
        e['key_text_cols'] = re.findall(r'`(\w+)`', m2.group(5))
json.dump(cat, open(out,'w'), indent=1)
print(len(cat), 'entities;', sum(1 for e in cat.values() if e['dict_section']), 'with dictionary;', sum(len(e['columns']) for e in cat.values()), 'specific columns')
print([k for k,e in cat.items() if not e['dict_section']])
