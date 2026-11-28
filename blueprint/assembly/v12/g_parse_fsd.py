"""Group G (R6): parse FSD V12 chapters 20-24 into heading-scoped tables and prose blocks.
Usage: python3 -I g_parse_fsd.py <fsd_dir> <out_json>"""
import sys, json, re, glob, os
fsd, out = sys.argv[1], sys.argv[2]
res = {}
for pat in ["20_*", "21_*", "22_*", "23_*", "24_*"]:
    path = glob.glob(os.path.join(fsd, pat))[0]
    lines = open(path, encoding="utf-8").read().split("\n")
    heads = []; blocks = []; i = 0
    while i < len(lines):
        ln = lines[i]
        m = re.match(r"<Heading(\d)>\s*(.*)", ln)
        if m:
            lvl = int(m.group(1)); heads = [h for h in heads if h[0] < lvl] + [(lvl, m.group(2).strip())]
            i += 1; continue
        if ln.strip() == "[TABLE]":
            rows = []; cur = None; i += 1
            while i < len(lines) and lines[i].strip() != "[/TABLE]":
                if lines[i].strip() == "---row":
                    cur = []; rows.append(cur)
                elif cur is not None:
                    cur.append(lines[i])
                i += 1
            i += 1
            hdr = rows[0] if rows else []
            blocks.append({"type": "table", "path": " > ".join(h[1] for h in heads), "header": hdr, "rows": rows[1:]})
            continue
        if ln.strip():
            blocks.append({"type": "text", "path": " > ".join(h[1] for h in heads), "text": ln})
        i += 1
    res[os.path.basename(path)] = blocks
json.dump(res, open(out, "w"), indent=1, ensure_ascii=False)
for k, v in res.items():
    t = [b for b in v if b["type"] == "table"]
    print(k, "blocks", len(v), "tables", len(t), "rows", sum(len(b["rows"]) for b in t), "text", len(v) - len(t))
