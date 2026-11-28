"""Configuration-management integrity checks for the L material (Part 11.12 section 11.12.1.3).

1. Annex vs V1: normalised non-empty line sets of BRD/FSD ZZ_Historical_annex.txt vs src V1 .txt.
2. SHA-256 manifests shipped inside the archive (Others/CURRENT_PACKAGE_SHA256.json,
   engineering/closure/final_artifact_manifest_sha256.json, any *manifest_sha256.json) are
   re-verified against the decoded files (match / mismatch / not present in decoded archive).
3. 38 documents.zip members are hashed and compared with the manifest 'documents/NN_*.docx' entries
   and with the SHA-256 printed in the annex 'Source chapter NN' headings.
4. Duplicate copies (commercial/investment HTML at src root vs pack) are compared byte-for-byte.
Output: OUT/integrity.json
"""
import glob, hashlib, json, os, re, sys, zipfile
sys.path.insert(0, os.path.dirname(__file__))
from L_common import *

res = {}


def sha(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()


def lineset(p):
    return {HEAD.sub('', l.strip()) for l in open(p, encoding='utf-8', errors='replace') if l.strip()}


for k, a, b in (('BRD', V12 + '/BRD/ZZ_Historical_annex.txt', SRC + '/Sales_Marketing_Automation_BRD_V1.txt'),
                ('FSD', V12 + '/FSD/ZZ_Historical_annex.txt', SRC + '/Sales_Marketing_Automation_FSD_V1.txt')):
    A, B = lineset(a), lineset(b)
    res[f'annex_vs_v1_{k}'] = dict(annex_unique_lines=len(A), v1_unique_lines=len(B), only_in_annex=len(A - B),
                                    only_in_v1=len(B - A), sample_only_in_v1=sorted(B - A)[:5])

# index decoded files by basename and by relative tail
allfiles = [p for p in glob.glob(SRC + '/**/*', recursive=True) if os.path.isfile(p)]
allfiles += [p for p in glob.glob(SRC + '/**/.*/**/*', recursive=True) if os.path.isfile(p)]


def find(rel):
    rel = rel.replace('\\', '/')
    c = [p for p in allfiles if p.endswith('/' + rel)]
    if not c:
        c = [p for p in allfiles if os.path.basename(p) == os.path.basename(rel)]
    return c


manifests = [SRC + '/Others/Others/CURRENT_PACKAGE_SHA256.json'] + sorted(glob.glob(SRC + '/engineering/**/*manifest*sha256*.json', recursive=True))
zip38 = V12 + '/archive_files/38 documents.zip'
zhash = {}
if os.path.exists(zip38):
    with zipfile.ZipFile(zip38) as z:
        for n in z.namelist():
            if not n.endswith('/'):
                zhash[os.path.basename(n)] = hashlib.sha256(z.read(n)).hexdigest()
res['zip38_members'] = len(zhash)
for m in manifests:
    try:
        d = json.load(open(m))
    except Exception as e:
        res[os.path.relpath(m, V12)] = dict(error=str(e))
        continue
    def flat(o, pre=''):
        for k, v in (o.items() if isinstance(o, dict) else []):
            if isinstance(v, dict):
                yield from flat(v, pre)
            else:
                yield (k, v)
    items = list(flat(d)) if isinstance(d, dict) else [(x.get('path') or x.get('file'), x.get('sha256')) for x in d if isinstance(x, dict)]
    st = dict(entries=0, match=0, mismatch=0, absent=0, zip_match=0, mismatch_files=[])
    for rel, h in items:
        if not isinstance(h, str) or not re.fullmatch(r'[0-9a-f]{64}', h or ''):
            if isinstance(h, dict) and 'sha256' in h:
                h = h['sha256']
            else:
                continue
        st['entries'] += 1
        base = os.path.basename(rel)
        if base in zhash and zhash[base] == h:
            st['zip_match'] += 1
            continue
        c = find(rel)
        if not c:
            st['absent'] += 1
            continue
        if any(sha(p) == h for p in c):
            st['match'] += 1
        else:
            st['mismatch'] += 1
            st['mismatch_files'].append(rel)
    st['mismatch_files'] = st['mismatch_files'][:15]
    st['source_archive'] = d.get('source_archive', '') if isinstance(d, dict) else ''
    res[os.path.relpath(m, V12)] = st

# annex-printed SHA-256 for source chapters vs zip
annex = open(V12 + '/BRD/ZZ_Historical_annex.txt', encoding='utf-8', errors='replace').read() + open(V12 + '/FSD/ZZ_Historical_annex.txt', encoding='utf-8', errors='replace').read()
pr = dict(re.findall(r'38 documents/([^ |]+\.docx) \| SHA-256 ([0-9a-f]{64})', annex))
res['annex_printed_chapter_hashes'] = dict(n=len(pr), match_zip=sum(1 for k, v in pr.items() if zhash.get(k) == v))
for a, b in ((SRC + '/commercial_website(1).html', SRC + '/Sales_Marketing_Automation_34_Neutral_SaaS_Website(1)/commercial_website.html'),
             (SRC + '/investment_website(1).html', SRC + '/Investment_Automation_19_Neutral_SaaS_Website(1)/investment_website.html')):
    res['identical:' + os.path.basename(a)] = sha(a) == sha(b)
json.dump(res, open(OUT + '/integrity.json', 'w'), indent=1)
print(json.dumps(res, indent=1)[:3000])
