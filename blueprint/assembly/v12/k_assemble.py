"""Group K: assemble Part 11.11a/b from templates and generated fragments. Usage: k_assemble.py <template> <frag_dir> <out_md>"""
import sys, re, pathlib
tpl, frag, out = sys.argv[1], pathlib.Path(sys.argv[2]), sys.argv[3]
s = open(tpl, encoding='utf-8').read()
s = re.sub(r'\{\{FRAG:([\w.]+)\}\}', lambda m: (frag / m.group(1)).read_text(encoding='utf-8').rstrip('\n'), s)
open(out, 'w', encoding='utf-8').write(s)
print(out, len(s))
