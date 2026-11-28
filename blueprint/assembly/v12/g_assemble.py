"""Group G (R6): fill {{fragment.md}} placeholders in tpl_*.md and write Part-11-7[a|b|c] files.
Usage: python3 -I g_assemble.py"""
import re, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from g_common import G, BP
NAMES = {"a": "Part-11-7a_V12_Website_Portal_Operator_Portfolio_UIUX_Prototypes.md",
         "b": "Part-11-7b_V12_Website_Portal_Operator_Portfolio_UIUX_Prototypes.md",
         "c": "Part-11-7c_V12_Website_Portal_Operator_Portfolio_UIUX_Prototypes.md"}
for k, name in NAMES.items():
    p = f"{G}/tpl_{k}.md"
    if not os.path.exists(p):
        continue
    t = open(p, encoding="utf-8").read()
    t = re.sub(r"\{\{([\w.]+)\}\}", lambda m: open(f"{G}/out/{m.group(1)}", encoding="utf-8").read().strip() + "\n", t)
    open(f"{BP}/{name}", "w", encoding="utf-8").write(t)
    print(name, len(t))
