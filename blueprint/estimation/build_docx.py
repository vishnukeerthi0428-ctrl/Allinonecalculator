"""Word version of the cost estimate: pandoc with a landscape reference document, then TOC refresh via LibreOffice."""
import os
import subprocess
import sys
from pathlib import Path

ASM = Path(__file__).resolve().parent.parent / "assembly"
sys.path.insert(0, str(ASM))


def build(md, out):
    import assemble as AS
    from docx import Document
    from docx.shared import Pt
    md, out = Path(md), Path(out)
    ref = md.parent / "reference.docx"
    AS.make_reference_docx(ref)
    d = Document(str(ref))
    for s in d.sections:
        hp = s.header.paragraphs[0]
        for r in hp.runs:
            r.text = ""
        hp.runs[0].text = "AI Growth Engine — End-to-End Cost Estimate v1.0    |    Confidential · 28 Nov 2026"
        hp.runs[0].font.size = Pt(8)
    d.save(str(ref))
    meta = md.parent / "meta.yaml"
    meta.write_text('---\ntitle: "AI Growth Engine: End-to-End Cost Estimate"\nsubtitle: "Development, subscriptions, AI agents, automations, workflows and lifecycle costs (INR and USD)"\n'
                    'date: "Version 1.0 · 28 Nov 2026 · Confidential"\ntoc-title: "Contents"\n---\n', encoding="utf-8")
    env = {**os.environ, "LANG": "C.UTF-8", "LC_ALL": "C.UTF-8"}
    subprocess.run(["pandoc", str(meta), str(md), "-f", "markdown+pipe_tables", "-t", "docx", "--toc", "--toc-depth=2",
                    "--reference-doc", str(ref), "--resource-path", str(md.parent), "-o", str(out)], check=True, env=env, cwd=md.parent)
    r = subprocess.run(["/usr/bin/python3", str(ASM / "update_toc.py"), str(out)], capture_output=True, text=True, timeout=900)
    print("DOCX", out, (r.stdout or r.stderr).strip()[-200:])
    ref.unlink(missing_ok=True)
    meta.unlink(missing_ok=True)
