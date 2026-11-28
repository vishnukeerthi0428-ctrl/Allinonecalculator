"""Build the sentence / row level inventory of the L material.

Material groups (src label -> files):
  ANX-BRD  v12/BRD/ZZ_Historical_annex.txt          (V1 retained text, non-normative)
  ANX-FSD  v12/FSD/ZZ_Historical_annex.txt
  V1-BRD   src/Sales_Marketing_Automation_BRD_V1.txt (lines merged with ANX-BRD by de-duplication)
  V1-FSD   src/Sales_Marketing_Automation_FSD_V1.txt
  OTH-EMW  src/Others/.../Expanded_Master_Workbook_csv/*.csv (30 tabs)
  OTH-147  src/Others/.../147_Screen_Field_csv/*.csv + START_HERE.txt + CURRENT_PACKAGE_SHA256.json
  ENG      src/engineering/** (csv, json, txt, md, py, sql, yaml<100KB, tf, js, tsx, sh, yml, dot, env)
  WEB-SMA  src/Sales_Marketing_Automation_34_Neutral_SaaS_Website(1)/* + src/commercial_website(1).html
  WEB-INV  src/Investment_Automation_19_Neutral_SaaS_Website(1)/* + src/investment_website(1).html
  INV-CAT  src/Investment_Automation_Master_..._24_Services_96_Workflows(1)_csv/*.csv

Excluded with reason (logged to OUT/excluded.tsv): binary images (png), xlsx (CSV twins parsed),
docx (TXT twins parsed), openapi *.yaml > 100 KB (JSON twins parsed), catalog_dependency_graph.svg
(DOT twin parsed), the 39-service SMA catalogue (owned by groups B/C/D).

Output: OUT/units.jsonl (every unit), OUT/unique.jsonl (de-duplicated by normalised text).
"""
import glob, json, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from L_common import *

E = SRC + '/engineering/engineering'
groups = []


def add(label, f):
    groups.append((label, f))


add('ANX-BRD', V12 + '/BRD/ZZ_Historical_annex.txt')
add('ANX-FSD', V12 + '/FSD/ZZ_Historical_annex.txt')
add('V1-BRD', SRC + '/Sales_Marketing_Automation_BRD_V1.txt')
add('V1-FSD', SRC + '/Sales_Marketing_Automation_FSD_V1.txt')
for f in sorted(glob.glob(SRC + '/Others/Others/Sales_Marketing_Automation_Expanded_Master_Workbook_csv/*.csv')):
    add('OTH-EMW', f)
for f in sorted(glob.glob(SRC + '/Others/Others/Sales_Marketing_Automation_147_Screen_Field_csv/*.csv')):
    add('OTH-147', f)
add('OTH-147', SRC + '/Others/Others/START_HERE.txt')
add('OTH-147', SRC + '/Others/Others/CURRENT_PACKAGE_SHA256.json')
excluded = []
for f in sorted(glob.glob(E + '/**/*', recursive=True) + glob.glob(E + '/.github/**/*', recursive=True)
                + glob.glob(E + '/starter/.github/**/*', recursive=True)):
    if os.path.isdir(f):
        continue
    ext = os.path.splitext(f)[1].lower()
    if ext in ('.png', '.svg') or (ext == '.yaml' and os.path.getsize(f) > 100000):
        excluded.append((f, 'binary/graphic or YAML twin of parsed JSON'))
        continue
    add('ENG', f)
for f in sorted(glob.glob(SRC + '/Sales_Marketing_Automation_34_Neutral_SaaS_Website(1)/*')):
    if f.endswith('.png'):
        excluded.append((f, 'preview image'))
        continue
    add('WEB-SMA', f)
add('WEB-SMA', SRC + '/commercial_website(1).html')
for f in sorted(glob.glob(SRC + '/Investment_Automation_19_Neutral_SaaS_Website(1)/*')):
    if f.endswith('.png'):
        excluded.append((f, 'preview image'))
        continue
    add('WEB-INV', f)
add('WEB-INV', SRC + '/investment_website(1).html')
for f in sorted(glob.glob(SRC + '/Investment_Automation_Master_Automation_Service_Catalog_2031_24_Services_96_Workflows(1)_csv/*.csv')):
    add('INV-CAT', f)
for f in glob.glob(SRC + '/*.xlsx') + glob.glob(SRC + '/*.docx') + glob.glob(SRC + '/Others/Others/*.xlsx'):
    excluded.append((f, 'binary twin; CSV/TXT extraction parsed'))
for f in glob.glob(SRC + '/Sales_Marketing_Automation_Master_Automation_Service_Catalog_2031_39_Services_156_Workflows(1)_csv/*'):
    excluded.append((f, 'SMA 39-service catalogue: owned by groups B/C/D (Parts 11.2-11.4)'))

dedup_seen = {}
nunits = 0
with open(OUT + '/units.jsonl', 'w') as fu:
    for label, f in groups:
        rel = os.path.relpath(f, V12)
        ext = os.path.splitext(f)[1].lower()
        if ext == '.csv':
            it, kind = csv_units(f, rel), 'row'
        elif ext == '.json':
            it, kind = json_units(f, rel), 'json'
        elif ext == '.html':
            it, kind = html_units(f, rel), 'html'
        elif label.startswith(('ANX', 'V1')):
            it, kind = text_units(f, rel), 'text'
        else:
            code = ext in ('.py', '.sql', '.js', '.tsx', '.tf', '.sh', '.yml', '.yaml', '.dot', '.jsonl') or 'Dockerfile' in f or 'requirements' in f
            kind = 'code' if code else 'text'
            it = ((f'{rel}:{i}', l.strip(), False, '') for i, l in enumerate(open(f, encoding='utf-8', errors='replace'), 1) if l.strip())
        for loc, text, is_row, heading in it:
            t = toks(text)
            if not t:
                continue
            key = ' '.join(t)
            u = dict(src=label, file=rel, loc=loc, kind=kind, is_row=is_row, heading=heading, text=text,
                     ntok=len(t), req=req_like(text, is_row))
            fu.write(json.dumps(u, ensure_ascii=False) + '\n')
            nunits += 1
            if key in dedup_seen:
                d = dedup_seen[key]
                d['count'] += 1
                d['srcs'][label] = d['srcs'].get(label, 0) + 1
            else:
                u['count'] = 1
                u['srcs'] = {label: 1}
                u['key'] = key
                dedup_seen[key] = u

with open(OUT + '/unique.jsonl', 'w') as fq:
    for i, u in enumerate(dedup_seen.values(), 1):
        u['uid'] = f'L-U{i:06d}'
        fq.write(json.dumps(u, ensure_ascii=False) + '\n')
with open(OUT + '/excluded.tsv', 'w') as fx:
    for f, r in excluded:
        fx.write(f'{os.path.relpath(f, V12)}\t{r}\n')
with open(OUT + '/files.tsv', 'w') as ff:
    for label, f in groups:
        ff.write(f'{label}\t{os.path.relpath(f, V12)}\t{os.path.getsize(f)}\n')
print('files', len(groups), 'units', nunits, 'unique', len(dedup_seen), 'excluded', len(excluded))
