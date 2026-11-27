"""Assemble Group I Part 4.4 files from sources and generated fragments."""
import pathlib, sys
here = pathlib.Path(__file__).parent; BP = pathlib.Path(sys.argv[1])
a = (here / "part_a_src.md").read_text(encoding="utf-8")
a = a.replace("{{SUMMARY}}", (here / "frag_summary.md").read_text(encoding="utf-8").strip())
a = a.replace("{{REGISTER}}", (here / "frag_register.md").read_text(encoding="utf-8").strip())
(BP / "Part-04-4a_Source_Pack_Security_DevOps_Operations_Enhancements.md").write_text(a, encoding="utf-8")
b = here / "part_b_src.md"
if b.exists():
    (BP / "Part-04-4b_Source_Pack_Security_DevOps_Operations_Enhancements.md").write_text(b.read_text(encoding="utf-8"), encoding="utf-8")
print("ok")
