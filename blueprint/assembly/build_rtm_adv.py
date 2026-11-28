#!/usr/bin/env python3
"""Traceability for v1.1 additions (Parts 9.6a/b alignment and 9.7-9.9 advanced capabilities) and, from v1.2,
for the V12 IDs of Part 11 (FR-V12-*, US-<EP>-Y*/Z*, TC-V12-*), written to final/RTM_v12.csv.

Writes final/RTM_advanced.csv (one row per item) and prints coverage counts.
Links are taken from table rows and story blocks that mention both IDs.
Usage: python3 blueprint/assembly/build_rtm_adv.py
"""
import collections
import csv
import re
from pathlib import Path

BP = Path(__file__).resolve().parent.parent
FILES = sorted(BP.glob("Part-09-[6789]*_*.md"))
FR, US, TC = r"FR-ADV-X\d-\d{3}", r"US-\d{2}-V\d\d{2}", r"TC-ADV-X\d-\d{3}"
AG, AU, WF = r"AG-0(?:39|[4-7]\d|80)\b", r"AU-(?:0(?:5[3-9]|[6-9]\d)|1[01]\d)\b", r"WF-(?:1[5-9]|[23]\d|40)\b"
DEC, ALN = r"DEC-(?:2(?:3[4-9]|[4-9]\d)|3\d\d|40\d)\b", r"TC-ALN-[AB]-\d{3}"


def main():
    link = collections.defaultdict(set)
    where = {}
    for f in FILES:
        tx = f.read_text(encoding="utf-8")
        label = re.match(r"Part-(\d+)-(\d+[a-z]?)_", f.name)
        label = f"{int(label.group(1))}.{label.group(2)}"
        blocks = tx.splitlines()
        heads = list(re.finditer(rf"^#{{3,6}} .*?({US}|{AG}|WF-\d\d)", tx, re.M))
        for i, m in enumerate(heads):
            seg = tx[m.end(): heads[i + 1].start() if i + 1 < len(heads) else min(len(tx), m.end() + 6000)]
            blocks.append(m.group(1) + " " + seg.replace("\n", " "))
        for ln in blocks:
            ids = set()
            for p in (FR, US, TC, AG, AU, WF, DEC, ALN):
                ids |= set(re.findall(p, ln))
            for a in ids:
                where.setdefault(a, label)
                link[a] |= ids - {a}
    fam = lambda pat: sorted(x for x in where if re.fullmatch(pat, x))
    tests = lambda x: {t for t in link[x] if re.fullmatch(TC, t) or re.fullmatch(ALN, t)}
    rows, stats = [], {}
    def add(kind, items, ok):
        n = 0
        for x in items:
            via = tests(x) or {t for y in link[x] if re.fullmatch(FR, y) or re.fullmatch(US, y) for t in tests(y)}
            good = ok(x, via)
            n += good
            rows.append([kind, x, where[x], "; ".join(sorted(y for y in link[x] if re.fullmatch(FR, y)))[:200],
                         "; ".join(sorted(y for y in link[x] if re.fullmatch(US, y)))[:200],
                         "; ".join(sorted(via))[:300], "Traced" if good else "Open"])
        stats[kind] = (n, len(items))
    add("FR-ADV", fam(FR), lambda x, v: bool(v))
    add("Story", fam(US), lambda x, v: bool(v))
    add("Agent", fam(AG), lambda x, v: bool(v) or bool(link[x] & set(fam(FR))))
    add("Automation", fam(AU), lambda x, v: bool(v) or bool(link[x] & set(fam(FR))))
    add("Workflow", fam(WF), lambda x, v: bool(v) or bool(link[x] & (set(fam(FR)) | set(fam(AG)) | set(fam(AU)))))
    alltext = "\n".join(f.read_text(encoding="utf-8") for f in FILES)
    defined = set(re.findall(rf"^\|\s*\**({DEC})", alltext, re.M))
    add("Decision (9.6-9.9)", sorted(d for d in fam(DEC) if d in defined), lambda x, v: True)
    out = BP / "final" / "RTM_advanced.csv"
    with out.open("w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["Kind", "ID", "Part", "Linked FR-ADV", "Linked stories", "Tests (direct or via FR/story)", "Status"])
        w.writerows(rows)
    for k, (n, t) in stats.items():
        print(f"{k}: {n}/{t} ({n / t * 100 if t else 100:.0f}%)")
    print(out, len(rows))


# ------------------------------------------------------------------------------------------------
# v1.2: V12 traceability (Part 11): FR-V12-*, stories US-<EP>-Y*/Z*, tests TC-V12-* (and TC-W-*), agents, automations,
# workflows. Writes final/RTM_v12.csv. A row is "Traced" when the item links to a test directly or through a linked FR or
# story (FR, story), or to an FR/test (agent, automation, workflow). Links come from one table row, or from the block
# that follows a heading naming the ID (story and agent cards).
# ------------------------------------------------------------------------------------------------
V_FR = r"FR-V12-[A-Z]-\d{3,4}"
V_US = r"US-\d{2}-[YZ][A-Z]\d{2,3}"
V_TC = r"TC-V12-[A-Z]-(?:[A-Z]{1,3}\d?-)?\d{2,4}|TC-W-[A-Z]+-\d{2,3}"
V_AG, V_AU = r"AG-(?:0(?:8[1-9]|9\d)|1\d\d|2[01]\d)\b", r"AU-(?:1[2-9]\d|2\d\d)\b"
V_WF = r"WF-(?:4[1-9]|5\d|60)\b"


def main_v12():
    files = sorted((f for f in BP.glob("Part-11-*.md") if not f.name.startswith("Part-11-0_")),
                   key=lambda f: [int(x) if x.isdigit() else x for x in re.findall(r"\d+|[a-z]+", f.name.split("_")[0])])
    pats = [re.compile(x) for x in (V_FR, V_US, V_TC, V_AG, V_AU, V_WF, r"(?:SM|INV)-SVC-\d{2}-WF0?\d", r"\bTS-V12-[A-Z]-\d{2}", r"\bAPI-V12-[A-Z]-\d{3,4}", r"\b(?:DDL|DB)-V12-[A-Z]-\d{2,3}")]
    link = collections.defaultdict(set)
    where = {}
    defined = {"FR": set(), "US": set(), "TC": set()}
    gherkin_us = set()
    for f in files:
        tx = f.read_text(encoding="utf-8")
        m = re.match(r"Part-11-(\d+)([a-z]?)_", f.name)
        label = f"11.{int(m.group(1))}{m.group(2)}"
        lines = tx.splitlines()
        # table rows carry the IDs of their section context: the nearest heading and the paragraph just before the table
        blocks, head_ctx, para_ctx, prev_table = [], "", "", False
        for ln in lines:
            if ln.startswith("#"):
                head_ctx, para_ctx = ln, ""
            elif ln.startswith("|"):
                extra = ""
                mt = re.match(r"^\|\s*TC-V12-([A-Z])-\S+\s*\|", ln)
                if mt:
                    for cell in ln.strip().strip("|").split("|")[1:6]:
                        if re.fullmatch(r"\s*\d{3}(?:\s*(?:[,/]|and)\s*\d{3})*\s*", cell):
                            extra += " " + " ".join(f"FR-V12-{mt.group(1)}-{n}" for n in re.findall(r"\d{3}", cell))
                blocks.append(ln + " " + extra + " " + (head_ctx + " " + para_ctx if re.search(V_TC, ln) else ""))
            elif ln.strip():
                para_ctx = ln[:2000]
            prev_table = ln.startswith("|")
        heads = list(re.finditer(rf"^#{{3,6}} .*?({V_US}|{V_AG}|{V_WF}|{V_FR})", tx, re.M))
        for i, h in enumerate(heads):
            seg = tx[h.end(): heads[i + 1].start() if i + 1 < len(heads) else min(len(tx), h.end() + 6000)][:6000]
            blocks.append(h.group(1) + " " + seg.replace("\n", " "))
        for mm in re.finditer(rf"^\|\s*\**({V_FR})\b|^\*\*Requirement ({V_FR})\*\*", tx, re.M):
            defined["FR"].add(mm.group(1) or mm.group(2))
        for mm in re.finditer(rf"^\|\s*({V_US})\s*\||^#{{3,6}} ({V_US})\b|^\| ID \| ({V_US}) \|", tx, re.M):
            defined["US"].add(mm.group(1) or mm.group(2) or mm.group(3))
        for blk in re.findall(r"```gherkin(.*?)```", tx, flags=re.S):
            gherkin_us.update(re.findall(V_US, blk))
        hs = list(re.finditer(rf"^#{{3,6}} ({V_US})\b", tx, re.M))
        for i, h in enumerate(hs):
            seg = tx[h.end(): hs[i + 1].start() if i + 1 < len(hs) else h.end() + 8000]
            if re.search(r"```gherkin|^\s*Scenario", seg, re.M):
                gherkin_us.add(h.group(1))
        for mm in re.finditer(rf"^\s*\|\s*({V_TC})\s*\|", tx, re.M):
            defined["TC"].add(mm.group(1))
        blocks += [m2.group(0) for m2 in re.finditer(rf"^\*\*(?:US-|Requirement ).*$", tx, re.M)]
        for ln in blocks:
            ids = set()
            for p in pats:
                ids |= set(p.findall(ln))
            for rg in re.finditer(r"FR-V12-([A-Z])-(\d{3,4})\s*(?:…|–|\.\.)\s*(?:FR-V12-[A-Z]-)?(\d{3,4})", ln):
                a, b = int(rg.group(2)), int(rg.group(3))
                if 0 < b - a <= 60:
                    ids |= {f"FR-V12-{rg.group(1)}-{n:03d}" for n in range(a, b + 1)}
            if len(ids) < 2:
                for a in ids:
                    where.setdefault(a, label)
                continue
            for a in ids:
                where.setdefault(a, label)
                link[a] |= ids - {a}
    # FR <-> story links and story AC from the story inventory (assembly/v12b/u_01_inventory.py, ranges and
    # compressed forms such as "E: 021" expanded there); refreshed by (in assembly/v12b): U_MAXPART=22 python3 -I u_01_inventory.py ../.. u_out/u_reinventory.json
    has_ac = set()
    inv = BP / "assembly" / "v12b" / "u_out" / "u_reinventory.json"
    if inv.exists():
        import json
        d = json.loads(inv.read_text(encoding="utf-8"))
        for fr, v in d.get("fr", {}).items():
            for us in v.get("stories", []):
                link[fr].add(us); link[us].add(fr)
        has_ac = {u for u, v in d.get("stories", {}).items() if v.get("has_ac")}
        for u, v in d.get("stories", {}).items():
            where.setdefault(u, "11." + re.sub(r"^Part-11-(\d+[a-z]?)_.*", r"\1", v.get("file", "")))
    has_ac |= gherkin_us
    is_tc = lambda x: re.fullmatch(V_TC, x) is not None
    tests = lambda x: {t for t in link[x] if is_tc(t)}
    rows, stats = [], collections.OrderedDict()

    def add(kind, items, ok):
        n = 0
        for x in sorted(items):
            via = tests(x) or {t for y in link[x] if re.fullmatch(V_FR, y) or re.fullmatch(V_US, y) for t in tests(y)}
            good = ok(x, via)
            n += good
            rows.append([kind, x, where.get(x, ""), "; ".join(sorted(y for y in link[x] if re.fullmatch(V_FR, y)))[:200],
                         "; ".join(sorted(y for y in link[x] if re.fullmatch(V_US, y)))[:200],
                         "; ".join(sorted(via))[:300], "Traced" if good else "Open"])
        stats[kind] = (n, len(items))
    add("FR-V12", defined["FR"], lambda x, v: bool(v) or any(re.fullmatch(V_US, y) and y in has_ac for y in link[x]))
    add("Story V12", defined["US"] | has_ac, lambda x, v: x in has_ac and (bool(v) or any(re.fullmatch(V_FR, y) for y in link[x])))
    add("Test V12", defined["TC"], lambda x, v: any(re.fullmatch(V_FR, y) or re.fullmatch(V_US, y) or re.fullmatch(V_AG, y)
                                                    or re.fullmatch(V_AU, y) or re.fullmatch(V_WF, y)
                                                    or y.startswith(("SM-SVC", "INV-SVC", "TS-V12", "API-V12", "DDL-V12", "DB-V12")) for y in link[x]))
    for kind, pat in (("Agent V12", V_AG), ("Automation V12", V_AU), ("Workflow V12", V_WF)):
        items = {x for x in where if re.fullmatch(pat, x)}
        add(kind, items, lambda x, v: bool(v) or any(re.fullmatch(V_FR, y) or re.fullmatch(V_US, y) for y in link[x]))
    out = BP / "final" / "RTM_v12.csv"
    with out.open("w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["Kind", "ID", "Part", "Linked FR-V12", "Linked stories", "Tests (direct or via FR/story)", "Status"])
        w.writerows(rows)
    for k, (n, t) in stats.items():
        print(f"{k}: {n}/{t} ({n / t * 100 if t else 100:.1f}%)")
    print(out, len(rows))
    return stats


if __name__ == "__main__":
    main()
    main_v12()
