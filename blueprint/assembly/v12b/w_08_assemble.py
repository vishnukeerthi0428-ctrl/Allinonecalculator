"""Group W (Part 11.24): assemble the three Part 11.24 Markdown files from w_tmpl/*.md and the generated fragments."""
import sys, os, re
sys.path.insert(0, os.path.dirname(__file__))
from w_common import *

NAMES = {'a': 'Part-11-24a_Developer_Build_and_Production_Deployment_Pack.md',
         'b': 'Part-11-24b_Developer_Build_and_Production_Deployment_Pack.md',
         'c': 'Part-11-24c_Developer_Build_and_Production_Deployment_Pack.md'}
T = os.path.join(os.path.dirname(__file__), 'w_tmpl/')
for k, n in NAMES.items():
    s = open(T + k + '.md', encoding='utf-8').read()
    def rep(m):
        return open(FRAG + m.group(1) + '.md', encoding='utf-8').read().rstrip('\n')
    s = re.sub(r'<!--FRAG:([a-z_]+)-->', rep, s)
    assert '<!--FRAG' not in s
    write(B + n, s)
    print(n, len(s))
