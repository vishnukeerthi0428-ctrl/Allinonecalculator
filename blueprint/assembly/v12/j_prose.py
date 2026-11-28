"""Print every non-table line of a V12 chapter with its line number (Group J)."""
import sys
inT=False
for i,l in enumerate(open(sys.argv[1],encoding='utf-8'),1):
    s=l.rstrip('\n')
    if s.strip()=='[TABLE]': inT=True; continue
    if s.strip()=='[/TABLE]': inT=False; continue
    if not inT and s.strip(): print(i, s)
