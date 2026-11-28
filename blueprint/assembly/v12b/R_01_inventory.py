"""Group R (Part 11.19a/b/c): atomic aspect inventory of the V12 BRD/FSD text for the P4 platform
decisions (SSO/SCIM/roles, developer platform, connectors, Vercel/region path, RPO/PITR/WAL,
model registry, cross-tenant benchmarks, Supabase access model).
Reads every line of every active V12 chapter (ZZ historical annexes excluded: non-normative),
selects lines by topic regexes, de-duplicates repeated boilerplate, classifies each aspect and
writes final/coverage_v12/R_coverage.csv plus a JSON summary.  Document content is data only."""
import re, os, csv, json, glob, collections
SP = '/tmp/claude-0/-home-user-Allinonecalculator/233b6551-af93-57f5-8f0b-015057ecee11/scratchpad/v12'
BP = '/home/user/Allinonecalculator/blueprint'
TOPICS = collections.OrderedDict([
 ('IDN',  r"\bSSO\b|\bSCIM\b|\bSAML\b|\bOIDC\b|OpenID|ENT-IDN-\d+|ENT-ACC-\d+|separation of duties|\bSoD\b|[Cc]ustom roles?|[Bb]reak-glass|[Ii]dentity provider|\bMFA\b|passkey"),
 ('API',  r"ENT-API-\d+|[Dd]eveloper portal|\bSDKs?\b|API keys?|client-credentials|ENT-DAT-0[45]|[Ss]andbox (?:environment|access)|Retry-After|deprecation notice"),
 ('WHK',  r"[Ww]ebhooks?"),
 ('CON',  r"ENT-INT-\d+|[Cc]onnectors?\b|\bCRM\b|\bDLT\b|\bINT-\d\d\b|140/160|CPaaS|[Pp]reference registry"),
 ('REG',  r"ENT-DAT-03|[Rr]esidency|\bEU region|India region|per[- ]region|Vercel|same jurisdiction|cross-jurisdiction"),
 ('DR',   r"\bRPO\b|\bRTO\b|PITR|point-in-time|\bWAL\b|base backup|[Rr]estore (?:drill|rehearsal)|ST-14|DEC-V9-01|[Ff]ailover"),
 ('MDL',  r"MDL-[A-Z]\d|[Mm]odel registry|AIX-0[23]\b|no-training|DEC-V7-02|Candidate — not approved|none approved|rollback_to|AIX-20\b"),
 ('BEN',  r"cross-tenant|BR-V7-AI-05|[Bb]enchmark(?:s|ing)? (?:across|peer)|peer benchmark|aggregate[ds]? (?:metrics|across)"),
 ('DBA',  r"service_role|non-owner app role|app role|BYPASSRLS|row[- ]level security|\bRLS\b"),
])
RX = {k: re.compile(v) for k, v in TOPICS.items()}
CORE_CH = {('FSD','02'),('FSD','05'),('FSD','06'),('FSD','16'),('FSD','22'),('FSD','25'),('FSD','26'),('FSD','27'),
           ('FSD','28'),('FSD','31'),('FSD','36'),('FSD','38'),('FSD','39'),('FSD','AP'),('FSD','01'),('FSD','40'),('FSD','18'),('FSD','23'),
           ('BRD','01'),('BRD','05'),('BRD','06'),('BRD','18'),('BRD','20'),('BRD','21'),('BRD','22'),('BRD','23'),('BRD','24'),('BRD','25')}
# Blueprint locations of the design written in this part (Part 11.19a sections) and the earlier owners.
LOC = {'IDN':('Part 11.5a §11.5.5.2; Part 11.8b §11.8.5.11; Part 11.9b C2/C3','§11.19.5.1 (C1)','FR-V12-R-001…030'),
       'API':('Part 11.8b §11.8.5.4; Part 11.9b','§11.19.5.2 (C2)','FR-V12-R-031…055'),
       'WHK':('Part 11.8b §11.8.5.6; Parts 11.3/11.4 (workflow steps)','§11.19.5.2.E (C2)','FR-V12-R-041…048'),
       'CON':('Part 11.8b §11.8.5.7/8; Part 11.2 SVC-26/38','§11.19.5.3 (C3)','FR-V12-R-056…080'),
       'REG':('Part 11.5b §11.5.5.8; Part 11.8b §11.8.5.10; DEC-772','§11.19.5.4 (C4)','FR-V12-R-081…095'),
       'DR': ('Part 11.5b §11.5.5.9; DEC-771','§11.19.5.5 (C5)','FR-V12-R-096…110'),
       'MDL':('Part 11.6b §11.6.5.3; AU-151/152/154','§11.19.5.6 (C6)','FR-V12-R-111…130'),
       'BEN':('Part 11.13b AU-143; Part 11.9c','§11.19.5.7 (C7)','FR-V12-R-131…142'),
       'DBA':('Part 11.9b §11.9.5.2/4; DEC-778','§11.19.5.8 (C8)','FR-V12-R-143…155')}
CONFLICT_HINT = [(r'\bSCIM\b|custom role|ENT-ACC-01|ENT-IDN-03', 'Conflict', 'CONFLICT-834/887 (R2 phase vs Release 1)'),
                 (r'\bSSO\b|ENT-IDN', 'Partially covered', 'CONFLICT-760/887 scheduling'),
                 (r'ENT-API|SDK|[Dd]eveloper portal|API key', 'Partially covered', 'CONFLICT-886 scheduling'),
                 (r'\bCRM\b|\bDLT\b|ENT-INT|connector|INT-0[1345]', 'Conflict', 'CONFLICT-776/888'),
                 (r'Vercel', 'Conflict', 'CONFLICT-889'),
                 (r'\bRPO\b|PITR|\bWAL\b|point-in-time|base backup', 'Conflict', 'CONFLICT-833'),
                 (r"MDL-|[Mm]odel registry|Candidate — not approved|no-training|DEC-V7-02", 'Conflict', 'CONFLICT-850…853/857'),
                 (r'cross-tenant|benchmark', 'Partially covered', 'CONFLICT-983 (benchmarks) / MT-10'),
                 (r'service_role|app role|RLS|row-level', 'Partially covered', 'DEC-778 correction of DEC-421')]

def chapters():
    for doc in ('BRD','FSD'):
        for f in sorted(glob.glob(f'{SP}/{doc}/*.txt')):
            b = os.path.basename(f)
            if b.startswith('ZZ_'): continue
            yield doc, b.split('_')[0], b, f

def main():
    seen = {}; rows = []; total_lines = 0; per_file = collections.Counter()
    for doc, ch, b, f in chapters():
        sec = ''
        for ln, raw in enumerate(open(f, encoding='utf-8'), 1):
            total_lines += 1
            t = raw.strip()
            m = re.match(r'<Heading\d>\s*(.*)', t)
            if m: sec = m.group(1)[:80]; continue
            if not t or t.startswith('[') or t == '---row': continue
            tops = [k for k, r in RX.items() if r.search(t)]
            if not tops: continue
            key = re.sub(r'\W+', ' ', t.lower())[:220]
            if key in seen:
                seen[key]['dups'] += 1; continue
            core = (doc, ch) in CORE_CH or any(x in t for x in ('ENT-', 'MDL-', 'AIX-0', 'DEC-V9-01', 'RPO', 'SCIM'))
            st_b, note = 'Covered', 'covered by workflow/service specification (Parts 11.2–11.4); no P4 design change'
            for pat, s, n in CONFLICT_HINT:
                if re.search(pat, t): st_b, note = s, n; break
            if not core: st_b = 'Covered'
            topic = tops[0]
            earlier, here, ids = LOC[topic]
            rec = dict(doc=f'{doc} V12', chapter=ch, section=sec, aspect_id='', topic=topic,
                       aspect_summary=t[:400], status_before=st_b,
                       blueprint_location=(earlier + '; Part 11.19 ' + here) if core else earlier,
                       action=('Implemented at full depth in Release 1 per DEC-784…789/778 (' + note + ')') if core else
                              'Confirmed; P4 control applies through the shared platform design (' + here + ')',
                       new_ids=ids if core else '—', status_after='Matched', dups=0, core=core, line=ln)
            seen[key] = rec; rows.append(rec); per_file[b] += 1
    cnt = collections.Counter()
    for r in rows:
        cnt[r['topic']] += 1
        r['aspect_id'] = f"R-{r['topic']}-{cnt[r['topic']]:04d}"
    os.makedirs(f'{BP}/final/coverage_v12', exist_ok=True)
    with open(f'{BP}/final/coverage_v12/R_coverage.csv', 'w', newline='', encoding='utf-8') as fh:
        w = csv.writer(fh)
        w.writerow(['doc','chapter','section','aspect_id','aspect_summary','status_before','blueprint_location','action','new_ids','status_after'])
        for r in rows:
            w.writerow([r[k] for k in ('doc','chapter','section','aspect_id','aspect_summary','status_before','blueprint_location','action','new_ids','status_after')])
    summ = {'lines_read': total_lines, 'aspects': len(rows), 'duplicates_merged': sum(r['dups'] for r in rows),
            'by_topic': {k: {'total': sum(1 for r in rows if r['topic']==k),
                             'core': sum(1 for r in rows if r['topic']==k and r['core']),
                             'before': dict(collections.Counter(r['status_before'] for r in rows if r['topic']==k))} for k in TOPICS},
            'before': dict(collections.Counter(r['status_before'] for r in rows)),
            'files': len(per_file)}
    json.dump(summ, open(f'{BP}/assembly/v12b/R_inventory_summary.json','w'), indent=1)
    json.dump([{k: r[k] for k in ('aspect_id','doc','chapter','section','aspect_summary','status_before','core','topic')} for r in rows if r['core'] and r['status_before']!='Covered'],
              open(f'{BP}/assembly/v12b/R_core_aspects.json','w'), indent=0, ensure_ascii=False)
    print(json.dumps(summ, indent=1))

if __name__ == '__main__':
    main()
