import sys
# Compact <HeadingN>/[TABLE]/---row format: one row per line, cells joined with ' | '
def compact(path):
    out=[];row=None;intable=False
    for line in open(path,encoding='utf-8'):
        line=line.rstrip('\n')
        if line=='[TABLE]': intable=True; row=None; continue
        if line=='[/TABLE]':
            if row is not None: out.append('  R: '+' | '.join(row))
            intable=False; row=None; continue
        if intable:
            if line=='---row':
                if row is not None: out.append('  R: '+' | '.join(row))
                row=[]; continue
            if row is None: row=[]
            row.append(line.strip()); continue
        if line.strip(): out.append(line)
    return '\n'.join(out)
if __name__=='__main__':
    print(compact(sys.argv[1]))
