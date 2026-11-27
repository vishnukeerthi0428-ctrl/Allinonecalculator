#!/usr/bin/env python3
"""Assemble all blueprint parts into one .docx and one .pdf.

Usage:  python3 blueprint/assembly/assemble.py [--out-name NAME]
Inputs: blueprint/Part-*.md (ordered by part/batch), optional assembly/front_matter.md
Outputs: blueprint/final/<NAME>.pdf, blueprint/final/<NAME>.docx
Requires: pandoc, node + playwright, blueprint/.tools/mermaid.min.js, python-docx.
"""
import argparse, json, os, re, shutil, subprocess, sys, tempfile, zipfile
from pathlib import Path

BP = Path(__file__).resolve().parent.parent
ASM = BP / "assembly"
OUT = BP / "final"
MJS = BP / ".tools" / "mermaid.min.js"
CSS = BP / ".pdf-style.css"
TITLE = "AI Growth Engine: Employee Sales & Marketing Automation"
SUBTITLE = "End-to-End Application Blueprint"
HEADER = "AI Growth Engine — Application Blueprint"

PART_RE = re.compile(r"Part-(\d+)(A?)(?:-(\d+)([a-z]?))?_")


def part_key(p: Path):
    m = PART_RE.match(p.name)
    return (int(m.group(1)), m.group(2), int(m.group(3) or 0), m.group(4) or "")


def collect_parts():
    files = [p for p in BP.glob("Part-*.md") if PART_RE.match(p.name)]
    return sorted(files, key=part_key)


def transform_part(text: str) -> str:
    lines = text.splitlines()
    out, seen_title = [], False
    for ln in lines:
        if not seen_title and ln.startswith("# AI Growth Engine"):
            seen_title = True
            continue
        m = re.match(r"^## Application Blueprint:\s*(.*)$", ln)
        if m:
            out.append("# " + m.group(1).strip())
            continue
        out.append(ln)
    return "\n".join(out).strip() + "\n"


def headings(md: str):
    """H1/H2 headings outside fenced code."""
    res, fence = [], False
    for ln in md.splitlines():
        if ln.startswith("```"):
            fence = not fence
            continue
        if fence:
            continue
        m = re.match(r"^(#{1,2}) (.+)$", ln)
        if m:
            res.append((len(m.group(1)), m.group(2).strip()))
    return res


def plain(s: str) -> str:
    s = re.sub(r"[*_`]", "", s)
    s = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", s)
    return re.sub(r"\s+", " ", s).strip()


def build_master(parts):
    body = []
    fm = ASM / "front_matter.md"
    for p in parts:
        body.append(transform_part(p.read_text(encoding="utf-8")))
    return (fm.read_text(encoding="utf-8") if fm.exists() else ""), "\n\n".join(body)


# ---------------------------------------------------------------- PDF
def cover_html(nparts, date="27 Nov 2026"):
    return f"""
<div class="cover">
  <div class="cover-band"></div>
  <h1 class="cover-title">{TITLE}</h1>
  <p class="cover-sub">{SUBTITLE}</p>
  <p class="cover-meta">Multi-tenant · Configuration-driven · Independent operations</p>
  <table class="cover-table">
    <tr><td>Document</td><td>Application Blueprint (Parts 0–9, assembled in Part 10)</td></tr>
    <tr><td>Version</td><td>1.0</td></tr><tr><td>Date</td><td>{date}</td></tr>
    <tr><td>Classification</td><td>Confidential: internal and authorized delivery partners</td></tr>
    <tr><td>Inputs</td><td>01 Business Requirements (BRD), 02 Functional Specification (FRD)</td></tr>
    <tr><td>Source files</td><td>{nparts} part documents</td></tr>
  </table>
</div>"""


def toc_html(hs, pages=None):
    rows = []
    for i, (lvl, txt) in enumerate(hs):
        pg = pages[i] if pages and pages[i] else "000"
        rows.append(f'<div class="toc-l{lvl}"><span class="toc-t">{plain(txt)}</span><span class="toc-d"></span><span class="toc-p">{pg}</span></div>')
    return '<div class="toc"><h1 class="toc-h">Table of contents</h1>' + "\n".join(rows) + '<p class="toc-end">TOCENDSENTINEL</p></div>'


EXTRA_CSS = """
.cover{page-break-after:always;padding-top:40mm}
.cover-band{height:8mm;background:#0b3d6b;margin-bottom:18mm}
.cover-title{font-size:30pt;border:none;color:#0b3d6b;margin:0}
.cover-sub{font-size:18pt;color:#1f5a8c;margin:6mm 0 2mm}
.cover-meta{font-size:11pt;color:#555;margin-bottom:14mm}
.cover-table{width:60%;font-size:10pt}
.toc{page-break-after:always}
.toc-h{border:none}
.toc div{display:flex;align-items:baseline;font-size:9pt;line-height:1.5}
.toc-l1{font-weight:bold;margin-top:6px;color:#0b3d6b}
.toc-l2{padding-left:16px}
.toc-t{flex:0 1 auto}
.toc-d{flex:1 1 auto;border-bottom:1px dotted #999;margin:0 6px;transform:translateY(-3px)}
.toc-p{flex:0 0 auto}
.toc-end{color:#fff;font-size:1pt;margin:0}
h1{page-break-before:always}
.cover h1,.toc h1,.fm h1{page-break-before:avoid}
"""


def md_to_html(md_text, html_path, extra_css_path):
    src = Path(html_path).with_suffix(".md")
    src.write_text(md_text, encoding="utf-8")
    subprocess.run(["pandoc", str(src), "-f", "markdown+raw_html", "-s", "--metadata", f"title={TITLE}",
                    "-c", str(CSS), "-c", str(extra_css_path), "--embed-resources", "-o", str(html_path)],
                   check=True, env={**os.environ, "LANG": "C.UTF-8", "LC_ALL": "C.UTF-8"})


def render_pdf(html, pdf):
    subprocess.run(["node", str(ASM / "render_pdf.js"), str(html), str(pdf), str(MJS), HEADER], check=True)


def find_pages(pdf, hs, start_page):
    txt = subprocess.run(["pdftotext", "-layout", str(pdf), "-"], capture_output=True, text=True).stdout
    pages = [re.sub(r"\s+", " ", pg) for pg in txt.split("\f")]
    res, cur = [], start_page
    for _, h in hs:
        key = plain(h)[:38]
        found = None
        for i in range(cur, len(pages)):
            if key in pages[i]:
                found = i
                break
        if found is None:
            res.append("")
        else:
            res.append(str(found + 1))
            cur = found
    return res


def build_pdf(front, body, name, tmp):
    hs = headings(body)
    css2 = Path(tmp) / "extra.css"
    css2.write_text(EXTRA_CSS)
    nparts = len(collect_parts())
    def compose(pages):
        fm = f'<div class="fm">\n\n{front}\n\n</div>\n\n' if front else ""
        return cover_html(nparts) + "\n\n" + toc_html(hs, pages) + "\n\n" + fm + body
    html = Path(tmp) / "master.html"
    md_to_html(compose(None), html, css2)
    pdf1 = Path(tmp) / "pass1.pdf"
    render_pdf(html, pdf1)
    # TOC ends where the first body heading appears; search body headings after the TOC pages
    txt = subprocess.run(["pdftotext", str(pdf1), "-"], capture_output=True, text=True).stdout.split("\f")
    toc_end = next(i for i, pg in enumerate(txt) if "TOCENDSENTINEL" in pg) + 1
    pages = find_pages(pdf1, hs, toc_end)
    md_to_html(compose(pages), html, css2)
    out = OUT / f"{name}.pdf"
    render_pdf(html, out)
    missing = sum(1 for p in pages if not p)
    print(f"PDF: {out}  headings={len(hs)} unresolved_toc={missing}")
    return out


# ---------------------------------------------------------------- DOCX
def make_reference_docx(path):
    data = subprocess.run(["pandoc", "-o", str(path), "--print-default-data-file", "reference.docx"], check=True)
    from docx import Document
    from docx.shared import Mm, Pt, RGBColor
    from docx.enum.section import WD_ORIENT
    from docx.oxml.ns import qn
    from docx.oxml import OxmlElement
    d = Document(str(path))
    for s in d.sections:
        s.orientation = WD_ORIENT.LANDSCAPE
        s.page_width, s.page_height = Mm(297), Mm(210)
        s.left_margin = s.right_margin = Mm(15)
        s.top_margin = s.bottom_margin = Mm(18)
        hp = s.header.paragraphs[0]
        hp.text = HEADER + "    |    Confidential · v1.0 · 27 Nov 2026"
        hp.runs[0].font.size = Pt(8)
        hp.runs[0].font.color.rgb = RGBColor(0x66, 0x66, 0x66)
        fp = s.footer.paragraphs[0]
        fp.alignment = 1
        def field(par, instr):
            r = par.add_run()
            for tag, attr in (("w:fldChar", "begin"), (None, None), ("w:fldChar", "end")):
                if tag is None:
                    it = OxmlElement("w:instrText"); it.set(qn("xml:space"), "preserve"); it.text = instr
                    r._r.append(it)
                else:
                    fc = OxmlElement(tag); fc.set(qn("w:fldCharType"), attr); r._r.append(fc)
            r.font.size = Pt(8)
        r = fp.add_run("Page "); r.font.size = Pt(8)
        field(fp, "PAGE")
        r = fp.add_run(" of "); r.font.size = Pt(8)
        field(fp, "NUMPAGES")
    st = d.styles
    byname = {x.name.lower(): x for x in st}
    for nm, size, color in (("heading 1", 18, "0B3D6B"), ("heading 2", 14, "0B3D6B"), ("heading 3", 12, "1F5A8C")):
        if nm in byname:
            byname[nm].font.size = Pt(size); byname[nm].font.color.rgb = RGBColor.from_string(color)
    for nm in ("normal", "body text", "first paragraph", "compact"):
        if nm in byname:
            byname[nm].font.size = Pt(9.5)
    # Table style borders
    if "heading 1" in byname:
        pPr = byname["heading 1"]._element.get_or_add_pPr()
        pb = OxmlElement("w:pageBreakBefore"); pPr.append(pb)
    if "table" in byname:
        tbl = byname["table"]._element
        tblPr = tbl.find(qn("w:tblPr"))
        if tblPr is None:
            tblPr = OxmlElement("w:tblPr"); tbl.append(tblPr)
        borders = OxmlElement("w:tblBorders")
        for edge in ("top", "left", "bottom", "right", "insideH", "insideV"):
            e = OxmlElement(f"w:{edge}"); e.set(qn("w:val"), "single"); e.set(qn("w:sz"), "4"); e.set(qn("w:color"), "A6B8CC")
            borders.append(e)
        tblPr.append(borders)
    d.save(str(path))


def docx_markdown(front, body, tmp):
    """Replace mermaid blocks by PNG images; return markdown text."""
    jobs, out_lines, fence, buf, n = [], [], None, [], 0
    text = (front + "\n\n" if front else "") + body
    for ln in text.splitlines():
        if fence is None and ln.strip().startswith("```mermaid"):
            fence, buf = "m", []
            continue
        if fence == "m":
            if ln.strip().startswith("```"):
                n += 1
                jid = f"d{n:03d}"
                jobs.append({"id": jid, "code": "\n".join(buf)})
                out_lines.append(f"@@FIG:{jid}@@")
                fence = None
            else:
                buf.append(ln)
            continue
        out_lines.append(ln)
    figdir = Path(tmp) / "figs"
    jf = Path(tmp) / "jobs.json"
    jf.write_text(json.dumps(jobs))
    if jobs:
        subprocess.run(["node", str(ASM / "render_mermaid.js"), str(jf), str(figdir), str(MJS)], check=False)
    from PIL import Image
    md = "\n".join(out_lines)
    def repl(m):
        jid = m.group(1)
        f = figdir / f"{jid}.png"
        if not f.exists():
            return "*[Diagram could not be rendered]*"
        w, h = Image.open(f).size
        size = "width=9.8in" if (h / w) < (6.2 / 9.8) else "height=6.2in"
        return f"![]({f}){{{size}}}"
    return re.sub(r"@@FIG:(d\d+)@@", repl, md), len(jobs)


def build_docx(front, body, name, tmp):
    ref = Path(tmp) / "reference.docx"
    make_reference_docx(ref)
    md, nfig = docx_markdown(front, body, tmp)
    cover = (f"---\ntitle: \"{TITLE}\"\nsubtitle: \"{SUBTITLE}\"\ndate: \"Version 1.0 · 27 Nov 2026 · Confidential\"\n---\n\n")
    src = Path(tmp) / "master_docx.md"
    toc = """
```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
<w:p><w:pPr><w:pStyle w:val="TOCHeading"/></w:pPr><w:r><w:t>Table of contents</w:t></w:r></w:p>
<w:p><w:r><w:fldChar w:fldCharType="begin" w:dirty="true"/></w:r><w:r><w:instrText xml:space="preserve"> TOC \\o "1-2" \\h \\z \\u </w:instrText></w:r><w:r><w:fldChar w:fldCharType="separate"/></w:r><w:r><w:t>Update this field to build the table of contents.</w:t></w:r><w:r><w:fldChar w:fldCharType="end"/></w:r></w:p>
```
"""
    src.write_text(cover + toc + "\n\n" + md, encoding="utf-8")
    out = OUT / f"{name}.docx"
    subprocess.run(["pandoc", str(src), "-f", "markdown", "-t", "docx",
                    "--reference-doc", str(ref), "-o", str(out)], check=True,
                   env={**os.environ, "LANG": "C.UTF-8", "LC_ALL": "C.UTF-8"})
    # Ask Word to refresh the TOC/fields on open
    tmpz = Path(tmp) / "fix.docx"
    with zipfile.ZipFile(out) as zin, zipfile.ZipFile(tmpz, "w", zipfile.ZIP_DEFLATED) as zout:
        for item in zin.infolist():
            data = zin.read(item.filename)
            if item.filename == "word/settings.xml" and b"updateFields" not in data:
                data = data.replace(b"</w:settings>", b'<w:updateFields w:val="true"/></w:settings>')
            zout.writestr(item, data)
    shutil.move(str(tmpz), str(out))
    r = subprocess.run(["/usr/bin/python3", str(ASM / "update_toc.py"), str(out)], capture_output=True, text=True, timeout=900)
    print((r.stdout or r.stderr).strip()[-300:])
    print(f"DOCX: {out}  figures={nfig}")
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out-name", default="AI_Growth_Engine_Application_Blueprint_v1.0")
    ap.add_argument("--only", choices=["pdf", "docx"], default=None)
    a = ap.parse_args()
    OUT.mkdir(exist_ok=True)
    parts = collect_parts()
    print("Parts:", ", ".join(p.name for p in parts))
    front, body = build_master(parts)
    with tempfile.TemporaryDirectory() as tmp:
        if a.only in (None, "pdf"):
            build_pdf(front, body, a.out_name, tmp)
        if a.only in (None, "docx"):
            build_docx(front, body, a.out_name, tmp)


if __name__ == "__main__":
    main()
