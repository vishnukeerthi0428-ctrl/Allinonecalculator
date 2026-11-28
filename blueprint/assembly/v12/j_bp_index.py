"""Group J: index blueprint test cases (| TC-... | title |) from Part-*.md, excluding Part-11 files."""
import re,glob,json,os
B='/home/user/Allinonecalculator/blueprint/'
def build():
    idx={}
    for f in sorted(glob.glob(B+'Part-*.md')):
        if os.path.basename(f).startswith('Part-11'): continue
        for l in open(f,encoding='utf-8'):
            m=re.match(r'^\|\s*(TC-[A-Z0-9][A-Za-z0-9-]*)\s*\|\s*([^|]+)\|',l)
            if m and m.group(1) not in idx:
                idx[m.group(1)]={'title':m.group(2).strip(),'file':os.path.basename(f)[:10],'row':l[:600]}
    return idx
if __name__=='__main__':
    i=build(); json.dump(i,open('j_bp_tc_index.json','w'),indent=0)
    from collections import Counter
    print(len(i)); print(Counter(re.sub(r'-?\d+[a-z]?$','',k) for k in i).most_common(60))
