"""Group D: cross-source consistency checks for SM-SVC-21..39 (BRD09, FSD12, FSD13, AppB, CSV)."""
import json, re, collections, os
D = os.path.dirname(os.path.abspath(__file__))
W = json.load(open(D+'/d_workflows.json'))
res = collections.defaultdict(list)
for w, r in W.items():
    s, c, b = r['spec'], r['csv'], r['brd09']
    titles = {r['title'], r['channel']['title'], r['ui_input']['title'], b['outcome_title'], c['Sub-automation name'].split(' — ', 1)[1]}
    if len(titles) > 1: res['title'].append((w, titles))
    rcls = s['Authority / effect classification'][:2]
    if not b['risk'].startswith(rcls): res['risk BRD09 vs FSD12'].append((w, b['risk'], rcls))
    kpi = s['Workflow KPI (proposed)'].split('; baseline')[0]
    if kpi != b['kpi']: res['kpi'].append((w, kpi, b['kpi']))
    io_in, io_out = b['io'].split(' → ')
    if io_out != c['Expected output']: res['output BRD vs CSV'].append((w, io_out, c['Expected output']))
    acts = '; '.join(x['action'] for x in r['steps'])
    if acts != c['Workflow steps']: res['steps CSV vs FSD12'].append((w, acts, c['Workflow steps']))
    fx = c['External side-effect classification']
    if rcls in ('R2', 'R3') and fx.startswith('Internal'): res['R2/R3 but CSV side-effect internal'].append((w, rcls, fx[:60]))
    if any(x['executor_input'].startswith('Effect adapter') for x in r['steps']) and rcls in ('R0',): res['effect step in R0'].append(w)
    if rcls in ('R2','R3') and not any(x['executor_input'].startswith('Effect adapter') for x in r['steps']): res['R2/R3 without effect step'].append((w, rcls))
    ver = (c['Service version'], c['Workflow version'])
    res['versions'].append((w, ver))
    if len(r['acceptance']) == 10 and rcls not in ('R2','R3'): res['APPROVAL/EFFECT TCs on R0/R1'].append((w, rcls))
    if len(r['acceptance']) == 8 and rcls in ('R2','R3'): res['no APPROVAL/EFFECT TCs on R2/R3'].append((w, rcls))
    sch = r['schema']['$id']
    if not sch.endswith(':v2') or '@2' not in s['Proposed domain contract']: res['schema version'].append(w)
out = {k: v for k, v in res.items() if k != 'versions'}
out['version_counts'] = collections.Counter(str(v) for _, v in res['versions'])
json.dump(out, open(D+'/d_crosscheck.json', 'w'), indent=1, default=str, ensure_ascii=False)
for k, v in out.items(): print(k, len(v) if not isinstance(v, collections.Counter) else dict(v)); [print('   ', x) for x in (v[:6] if isinstance(v, list) else [])]
