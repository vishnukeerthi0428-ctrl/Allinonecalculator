"""R2/B: parse the 39-service Master Automation Service Catalogue workbook (CSV export).
Usage: python3 -I r2b_parse_services.py <csv_dir> <out_json>
Reads every sheet, skips the 2-line title block + blank line, and emits one JSON with all rows."""
import csv, json, sys, os, collections
d, out = sys.argv[1], sys.argv[2]
data = {}
for fn in sorted(os.listdir(d)):
    if not fn.endswith('.csv'): continue
    with open(os.path.join(d, fn), newline='', encoding='utf-8') as f:
        rows = list(csv.reader(f))
    title, note = rows[0][0], rows[1][0]
    # header = first row after title block that is non-empty
    i = 2
    while i < len(rows) and not any(c.strip() for c in rows[i]): i += 1
    hdr = rows[i]
    recs = []
    for r in rows[i+1:]:
        if not any(c.strip() for c in r): continue
        recs.append({(h or f'col{j}'): (r[j] if j < len(r) else '') for j, h in enumerate(hdr)})
    data[fn[:-4]] = {'title': title, 'note': note, 'header': hdr, 'rows': recs}
json.dump(data, open(out, 'w'), indent=1, ensure_ascii=False)
for k, v in data.items():
    print(f"{k}: {len(v['rows'])} rows, {len(v['header'])} cols")
