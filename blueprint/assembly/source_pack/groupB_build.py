#!/usr/bin/env python3
"""Assemble Part-03-4_Source_Pack_Architecture_and_Workflow_Enhancements.md from fragments.
Run after groupB_parse.py and groupB_aspects.py:  python3 -I groupB_build.py
"""
import os

BP = "/home/user/Allinonecalculator/blueprint"
SP = os.path.join(BP, "assembly/source_pack")
FR = os.path.join(SP, "groupB_frag")
OUT = os.path.join(BP, "Part-03-4_Source_Pack_Architecture_and_Workflow_Enhancements.md")

parts = [open(os.path.join(FR, f), encoding="utf-8").read() for f in sorted(os.listdir(FR)) if f.endswith(".md")]
doc = "\n".join(parts)
doc = doc.replace("<!--STATUS_COUNTS-->", open(os.path.join(SP, "groupB_out/status_counts.md"), encoding="utf-8").read())
doc = doc.replace("<!--REGISTER-->", open(os.path.join(SP, "groupB_out/register.md"), encoding="utf-8").read())
open(OUT, "w", encoding="utf-8").write(doc)
print(OUT, len(doc), "chars")
