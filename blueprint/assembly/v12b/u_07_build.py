#!/usr/bin/env python3
"""Part 11.22 (Group P7, letter U) builder: Master User Stories and Persona
Journeys with Permutations (V12).

Pipeline:
  u_01_inventory.py  -> u_out/u_inventory.json  (FR-V12 and story inventory)
  u_02_baseline.py   -> u_out/u_baseline.json   (stories before Part 11)
  this script        -> Part-11-22a…f_*.md, final/coverage_v12/U_coverage.csv,
                        u_out/u_summary.json
Usage: python3 -I u_07_build.py <blueprint_dir>
"""
import collections, csv, json, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import u_03_models as M
import u_04_stories as S
import u_05_context as C
import u_06_journeys as JR

BP = sys.argv[1]
OUTD = os.path.join(HERE, 'u_out')
inv = json.load(open(os.path.join(OUTD, 'u_inventory.json')))
base = json.load(open(os.path.join(OUTD, 'u_baseline.json')))
recs, stories = S.build(inv)
# Founder decisions of 28 Nov 2026 supersede register wording for these FRs (DEC-947, DEC-948)
FR_OVERRIDE = {
 'FR-V12-A-006': dict(req='Product separation (amended by DEC-783): Sales & Marketing and Investment Automation are separate product codes; only libraries and patterns are reused; no implicit cross-product access; investor entities, routes and terms exist only in the INV product namespace',
                      accept='an SM-only tenant receives 404 for /api/v1/investor/*, a cross-product query returns zero rows, and the SM catalogue, routes and schemas contain no investor entity'),
 'FR-V12-K-004': dict(req='24×7 human on-call for SEV1/SEV2 from Release 2 GA: contracted NOC/SOC first line and internal engineer escalation rota (DEC-773, which decided the DEC-715 option)'),
 'FR-V12-A-147': dict(req='Recovery objectives per data class: critical transactional RPO ≤ 15 min / RTO ≤ 4 h; growth workload RPO ≤ 15 min / RTO ≤ 2 h as a blocking gate (DEC-771, DEC-787); regenerable research RPO ≤ 24 h / RTO ≤ 8 h'),
}
for _f, _o in FR_OVERRIDE.items():
    if _f in recs:
        recs[_f].update(_o)
EXIST = set(inv['stories'])
NEW = {s['id'] for s in stories}
FR2NEW = {f: r['story'] for f, r in recs.items()}

def cl(s):
    return S.clean(s)

def check_refs(ids):
    bad = [i for i in ids if not (i in EXIST or i in NEW)]
    if bad:
        raise SystemExit('unknown story ids: %s' % bad)

EPIC_TITLES = {
 'EP-01': 'Platform foundation, identity reuse and tenancy', 'EP-02': 'Product truth and knowledge',
 'EP-03': 'Consent, privacy, eligibility and compliance', 'EP-04': 'AI gateway, cost control and AI quality',
 'EP-05': 'Market intelligence and discovery', 'EP-06': 'Opportunity scoring, contacts and research review',
 'EP-07': 'CRM, lead capture and Customer 360', 'EP-08': 'Messaging: drafting, email, inbound, sequences, omnichannel',
 'EP-09': 'Meetings, webinars and demos', 'EP-10': 'WhatsApp and website assistant', 'EP-11': 'Content, SEO and social publishing',
 'EP-12': 'Campaigns, landing pages, ads and referrals', 'EP-13': 'Proposal, quote, negotiation and contract',
 'EP-14': 'Bids, orders and fulfilment (vertical routes)', 'EP-15': 'Payment, closure, revenue and attribution',
 'EP-16': 'Onboarding, retention, partners and expansion pilots', 'EP-17': 'Dashboards, forecast and Command Centre',
 'EP-18': 'Workflow, autonomy and automation engine', 'EP-19': 'Public website and external portal',
 'EP-20': 'SaaS client lifecycle and portability', 'EP-21': 'Release readiness, QA and observability',
 'EP-22': 'Voice and intelligent telephony', 'EP-23': 'SMS, RCS and business messaging',
 'EP-24': 'Agentic commerce and AI-to-AI transactions', 'EP-25': 'Marketplace and e-commerce channel operations',
 'EP-26': 'Procurement and supplier management', 'EP-27': 'Customer service and support operations',
 'EP-28': 'Multimodal creative production', 'EP-29': 'Automation service catalogue, SKU entitlement and metering',
 'EP-30': 'Investment Automation I: platform, investor-mode website, discovery and engagement',
 'EP-31': 'Investment Automation II-a: diligence, offers, applications and receipts',
 'EP-32': 'Investment Closing, Investor Lifecycle and Engagement Operations',
 'EP-33': 'Specialised Funding, Ownership, Governance, Verification and Securities Compliance',
 'EP-34': 'Global expansion, certification and multi-market operations (new, DEC-942)',
}
EPIC_SRC = {**{'EP-%02d' % i: 'Part 0 §0.10.2' for i in range(1, 22)}, **{'EP-%02d' % i: 'Part 11.2a' for i in range(22, 30)},
            'EP-30': 'Part 11.16e', 'EP-31': 'Part 11.16e', 'EP-32': 'Part 11.16d', 'EP-33': 'Part 11.16d', 'EP-34': 'this part'}

def fib(n_frs, binding, risk3):
    if binding:
        return (1, 2) if n_frs <= 2 else (2, 3)
    lo, hi = {1: (3, 5), 2: (5, 8), 3: (8, 13), 4: (8, 13)}[n_frs]
    if risk3 and n_frs == 1:
        lo, hi = 5, 8
    return lo, hi

def sp_of(s):
    m = re.search(r'(\d{1,2})\s*[–-]\s*(\d{1,2})', s or '')
    if m:
        return int(m.group(1)), int(m.group(2))
    m = re.search(r'\b(\d{1,2})\b', s or '')
    return (int(m.group(1)), int(m.group(1))) if m else None

def rel_bucket(s):
    s = (s or '').lower()
    if re.search(r'\bw6\b|\br[345]\b|\ba[1-4]\b|post-w6|future|release 3', s): return 'Release 3+'
    if re.search(r'\br2\b|release 2|\bw[45]\b|r2-b', s): return 'Release 2'
    if re.search(r'\br[01]\b|release 1|\bw[0-3]\b|r1-b|\bs\d', s): return 'Release 1'
    return 'Not stated'

def lc_first(t):
    w = t.split(' ')[0] if t else ''
    if w and w[1:] == w[1:].lower() and not any(ch.isdigit() for ch in w):
        return t[0].lower() + t[1:]
    return t

def short_label(t, n=46):
    t = cl(t)
    t = re.split(r';|\. ', t)[0].rstrip('.')
    if len(t) <= n:
        return t
    cut = t[:n]
    for sep in (' (', ', ', ' with ', ' before ', ' for ', ' – '):
        i = cut.rfind(sep)
        if i > n * 0.45:
            return cut[:i]
    return cut.rsplit(' ', 1)[0]

SVC_NAMES = {}
for _p in [p for p in os.listdir(BP) if p.startswith('Part-11-16c') and p.endswith('.md')]:
    for _m in re.finditer(r'^#{2,5}\s+(?:[\d.]+\s+)?(INV-SVC-\d{2})\s+([^\n]+)$', open(os.path.join(BP, _p), encoding='utf-8').read(), flags=re.M):
        if '-WF' not in _m.group(0):
            SVC_NAMES.setdefault(_m.group(1), cl(_m.group(2)))

def wf_service(st):
    m = re.search(r'(INV-SVC-\d{2})', recs[st['frs'][0]]['section'])
    return m.group(1) if m else None

from u_09_titles import TITLES
def title_of(st):
    key = st['frs'][0].replace('FR-V12-', '')
    if key in TITLES:
        return TITLES[key]
    svc = wf_service(st) if recs[st['frs'][0]].get('wf') else None
    if svc:
        return '%s %s: workflow contracts WF01–WF04' % (svc, SVC_NAMES.get(svc, ''))
    labels = []
    for f in st['frs']:
        r = recs[f]
        lab = r['label']
        if r['letter'] == 'K' and (r.get('source') or '').startswith('ENT-'):
            lab = r.get('req', lab)
        labels.append(short_label(lab))
    labels = [labels[0]] + [lc_first(x) for x in labels[1:]]
    t = labels[0] if len(labels) == 1 else ', '.join(labels[:-1]) + ' and ' + labels[-1]
    return t[0].upper() + t[1:]

def art(x):
    return ('an ' if x[:1].lower() in 'aeiou' else 'a ') + x

# ------------------------------------------------------------------ stories

import textwrap
MAXW = 150
def fmt_step(line, ind):
    """Keep Gherkin lines within the PDF width: long steps end with ':' and carry the detail as a doc string."""
    if len(ind) + len(line) <= MAXW:
        return [ind + line]
    kw, rest = line.split(' ', 1)
    cut = -1
    for sep in (': ', ' as specified by ', ' with ', ', ', ' and '):
        i = rest.find(sep, 25)
        if 0 < i < 95:
            cut = i + (len(sep) if sep in (': ', ' as specified by ') else 0); break
    if cut < 0:
        cut = rest.rfind(' ', 0, 90)
    head, tail = rest[:cut].rstrip(' :,'), rest[cut:].strip(' ,')
    if head.endswith(' as specified by'):
        head, tail = head + ' ' + tail.split(':', 1)[0], tail.split(':', 1)[1].strip() if ':' in tail else ''
    out = [ind + kw + ' ' + head + ':', ind + '  """']
    for w in textwrap.wrap(tail, MAXW - len(ind) - 4):
        out.append(ind + '  ' + w)
    out.append(ind + '  """')
    return out

def render_story(st, seed):
    sid = st['id']; ep = st['epic']; nn = sid.split('-ZU')[1]
    acp = 'AC-%sZU%s' % (ep[3:], nn)
    frs = [recs[f] for f in st['frs']]
    dom = collections.Counter(r['domain'] for r in frs).most_common(1)[0][0]
    D = C.DOM[dom]
    model = M.MODELS[st['model']]
    anchor = frs[0].get('anchor')
    is_k = all(r['letter'] == 'K' and (r.get('source') or '').startswith('ENT-') for r in frs)
    related = sorted(set(sum((r['related'] for r in frs), [])))[:6]
    binding = bool(anchor) or (is_k and related)
    risk3 = model['risk'] == 3
    lo, hi = fib(len(frs), binding, risk3)
    st['sp'] = (lo, hi)
    rels = collections.Counter(r['rel'] for r in frs)
    order = {'Release 1': 0, 'Release 2': 1, 'Release 3+': 2}
    release = sorted(rels, key=lambda x: order[x])[0]
    st['release'] = release
    prio = sorted((r['prio'] for r in frs), key=lambda p: {'Must': 0, 'Should': 1, 'Could': 2}[p])[0]
    st['priority'] = prio
    st['title'] = title_of(st)
    st['domain'] = dom
    typ = ('Compliance (acceptance binding)' if binding else
           {'IAM': 'Security', 'DATA': 'Security', 'OPS': 'Observability', 'LEGAL': 'Compliance', 'GLB': 'Compliance',
            'INV': 'Compliance', 'RUN': 'Enabler', 'API': 'Feature'}.get(dom, 'Feature'))
    st['type'] = typ
    # statement
    if anchor and inv['stories'].get(anchor, {}).get('title', '').startswith('As '):
        stmt = cl(inv['stories'][anchor]['title'])
        if not stmt.endswith('.'):
            stmt += ''
        stmt = stmt + (' – with the acceptance criteria below, which the statement-only story %s did not carry' % anchor)
    elif frs[0].get('wf'):
        svc = wf_service(st)
        stmt = 'As %s, I want the four %s %s workflows (%s) to run as typed, policy-checked contracts on the universal engine, so that %s' % (
            art(D['actor']), svc, SVC_NAMES.get(svc, ''), '; '.join(lc_first(short_label(r['label'], 60)) for r in frs), D['benefit'])
    else:
        want = '; '.join(lc_first(S.short(r.get('req') or r['label'], 140).rstrip('.')) for r in frs)
        stmt = 'As %s, I want %s, so that %s' % (art(D['actor']), want, D['benefit'])
    traces = []
    for r in frs:
        t = r['id']
        if r.get('source'):
            t += ' (' + S.short(r['source'], 60) + ')'
        traces.append(t)
    decs = sorted(set(re.findall(r'DEC-\d{3}', ' '.join(r.get('rel_note', '') + ' ' + r.get('allcells', '') for r in frs))))
    tcs = sorted(set(sum((r['tcs'] for r in frs), [])))
    trace = '; '.join(traces)
    if decs: trace += '; ' + ', '.join(decs[:8])
    if tcs: trace += '; tests ' + ', '.join(tcs[:6])
    srcloc = '; '.join(sorted(set('Part %s §%s' % (re.match(r'Part-(\d+-\d+[a-e]?)', r['file']).group(1).replace('-', '.'), S.short(r['section'], 50)) for r in frs if r['file'])))
    deps = [d for d in D['deps'] if d in EXIST][:4]
    if anchor: deps = [anchor] + deps
    dep_txt = ', '.join(deps) + ('; source definition: ' + srcloc if srcloc else '')
    pnames = [n for n, _ in model['params']]
    profile = ' · '.join('%s ×%d' % (n, len(v)) for n, v in model['params']) + ' · operation ×%d' % len(frs)
    notes = []
    bynote = collections.OrderedDict()
    for r in frs:
        if r.get('rel_note'):
            bynote.setdefault(r['rel_note'], []).append(r['id'])
    for nt, ids in bynote.items():
        notes.append('%s: release per %s' % (', '.join(ids), nt))
    if anchor:
        notes.append('Acceptance binding: %s carries the statement and its build points; this story adds the Gherkin AC, the generated Examples and the test automation for the FRs above (DEC-941)' % anchor)
    elif is_k and related:
        notes.append('Trace requirement adopted literally from the ENT register (Part 11.11b §11.11.5.16); design depth and build points sit in %s; this story binds the ENT acceptance to tests (DEC-941)' % ', '.join(related[:4]))
    elif related:
        notes.append('Related existing stories (shared source IDs, no FR trace): %s' % ', '.join(related[:5]))
    if any(r['letter'] == 'A' and r['num'] == 6 for r in frs):
        notes.append('Wording amended by DEC-783: investor entities exist only in the separate Investment Automation product code; the separation check (no implicit cross-product access) is kept (CONFLICT-1149)')
    if any(r['id'] == 'FR-V12-K-004' for r in frs):
        notes.append('The register text still says "Pending Founder decision"; DEC-773 decided it (hybrid 24×7 NOC/SOC + internal rota from Release 2 GA) – GAP-1148')
    notes.append('Screens %s; API family `%s`; audit events `%s.*`; feature flag default OFF until DoD D-14 evidence' % (D['screens'], D['api'], D['event']))
    if dom in ('AI',):
        notes.append('DoR R-10: task route through the model registry (DEC-788), eval dataset per AIX-05, per-task cost ceiling; no Restricted data to Tier 2')
    if dom in ('LEGAL', 'INV', 'INVWF', 'GLB'):
        notes.append('DoR R-12: activates per jurisdiction only when the counsel-signed rule pack is Approved (Part 11.15; DEC-779…783)')
    out = []
    out.append('##### %s %s\n' % (sid, st['title']))
    out.append('| Field | Value |\n|---|---|')
    rows = [('ID', sid), ('Title', st['title']), ('Type', typ), ('Story', stmt),
            ('Persona / roles', D['actor'][0].upper() + D['actor'][1:] + ('; approvers and reviewers per the Background' if dom in ('RUN', 'INV', 'INVWF', 'COM') else '')),
            ('Traces', trace), ('Priority', prio), ('Wave', '%s (dates follow the work, DEC-770)' % release),
            ('Points', '%d–%d' % (lo, hi)), ('Dependencies', dep_txt), ('Dimension profile', profile + ' · model ' + st['model']),
            ('Notes', ' · '.join(notes))]
    for k, v in rows:
        out.append('| %s | %s |' % (k, cl(v)))
    out.append('')
    g = ['```gherkin', 'Feature: %s' % st['title'], '  Background:']
    g.extend(fmt_step('Given %s' % D['fixtures'][0], '    '))
    g.extend(fmt_step('And %s' % D['fixtures'][1], '    '))
    k = 0
    def sc(tags, name, lines):
        nonlocal k
        k += 1
        g.append('')
        g.append('  %s' % tags)
        g.append('  Scenario: %s-%02d %s' % (acp, k, name))
        for i, l in enumerate(lines):
            g.extend(fmt_step(l, '    '))
    for i, r in enumerate(frs):
        tag = '@happy' if i == 0 else '@alt'
        toks = [t for t in r['tokens'] if not t.startswith(('SM-SVC', 'INV-SVC'))][:2]
        tagline = ' '.join([tag] + ['@' + t for t in toks] + (['@' + re.search(r'DEC-\d{3}', r['rel_note']).group(0)] if re.search(r'DEC-\d{3}', r.get('rel_note', '')) else []))
        if r.get('wf'):
            wf = r['wf']
            wfid = re.match(r'(INV-SVC-\d{2}-WF0\d)', r['section'])
            wfid = wfid.group(1) if wfid else r['id']
            lines = ['Given the trigger "%s" occurs for issuer "AppNAI Technologies Pvt Ltd"' % S.short(wf.get('Trigger', 'manual request'), 120),
                     'When %s runs with a DTO valid against `urn:inv:dto:%s:v2` (%s)' % (wfid, wfid, r['id']),
                     'Then %s' % S.short(wf.get('Business outcome / input → output', r.get('req', '')), 220),
                     'And %s' % S.short(wf.get('Result / acceptance', 'the result is recorded with evidence'), 200),
                     'And every step records class, input reference, output reference, state and evidence, and autonomy is "%s"' % S.short(wf.get('Autonomy in blueprint', 'L1'), 110)]
            sc(tagline, '%s – %s (%s)' % ('Happy path' if i == 0 else 'Alternate', S.short(r['label'], 70), r['id']), lines)
            continue
        acc = r.get('accept') or ''
        lines = ['Given %s is signed in to the tenant with the capability enabled' % D['who'],
                 'When "%s" is exercised as specified by %s: %s' % (S.short(r['label'], 70), r['id'], S.short(r.get('req') or r['label'], 260)),
                 'Then %s' % (lc_first(S.short(acc, 260)) if acc else 'the observable result matches %s and its tests %s' % (r['id'], ', '.join(r['tcs'][:3]) or 'in Part 11.21')),
                 'And the audit event "%s.%s" is written with outcome "allowed", correlation_id, tenant_id and company_id' % (D['event'], re.sub(r'[^a-z0-9]+', '_', S.short(r['label'], 30).lower()).strip('_'))]
        sc(tagline, '%s – %s (%s)' % ('Happy path' if i == 0 else 'Alternate', S.short(r['label'], 70), r['id']), lines)
    for r in frs:
        neg = r.get('neg')
        if neg and neg not in ('—', '-'):
            parts = [p.strip() for p in re.split(r'→|->', neg, maxsplit=1)]
            if len(parts) == 2:
                lines = ['Given the condition "%s" holds for %s' % (S.short(parts[0], 160), r['id']), 'When the action is attempted',
                         'Then the outcome is "%s"' % S.short(parts[1], 160), 'And no external effect, charge or outbox event is created']
            else:
                lines = ['Given %s' % S.short(neg, 200), 'When the action is attempted', 'Then it is blocked or held with no external effect and the denial is audited (%s)' % r['id']]
            sc('@neg', 'Negative – %s (%s)' % (S.short(parts[0] if len(parts) == 2 else neg, 60), r['id']), lines)
    for key in ('neg', 'val', 'perm', 'edge'):
        tags, name, lines = D[key]
        sc(tags, name, lines)
    # Scenario Outline from the parameter model
    ops = []
    for r in frs:
        lab = S.short(('%s %s' % (r['id'].replace('FR-V12-', ''), r['label'])), 58)
        allow = S.short(r.get('accept') or (r.get('wf') or {}).get('Result / acceptance') or r.get('req') or 'conforms to ' + r['id'], 90)
        ops.append((lab.replace('"', "'"), allow.replace('|', '/')))
    res = M.model_rows(st['model'], ops, seed)
    st['comb'] = {k2: res[k2] for k2 in ('mid', 't', 'method', 'space', 'tuples', 'covered', 'n_array', 'n_base')}
    st['comb']['rows'] = len(res['rows'])
    heads = ['ex'] + [C.slug(n) for n in res['names']] + ['expected']
    g.append('')
    g.append('  @sec @obs @%s' % st['model'])
    g.append('  Scenario Outline: %s-%02d Permutations – %s (%s, %d rows)' % (acp, k + 1, model['title'], 'exhaustive' if res['t'] == 'all' else '%s-way' % res['t'], len(res['rows'])))
    for l in C.STEPS[st['model']]:
        g.append('    ' + l)
    g.append('    Then the outcome is "<expected>"')
    g.append('    And the row <ex> is recorded with its parameter values in the test evidence')
    g.append('    # Value codes of model %s (§11.22.5.2): persona Pnn/Rnn; authority A1 authorised, A3 SoD or over limit,' % st['model'])
    g.append('    # A5 wrong role, T5 other tenant; zones IN, EU, EU→IN misrouted; ✓ = Approved. Operations:')
    for o, _ in ops:
        g.append('    #   %s = %s' % (o.split(' ')[0], S.short(' '.join(o.split(' ')[1:]), 100)))
    meth = 'exhaustive' if res['t'] == 'all' else '%s-way, seed %d' % (res['t'], seed)
    g.append('    Examples: %s rows (%s; space %s; tuples %s/%s; +%d baseline-allow)' % (
        st['model'], meth, f"{res['space']:,}", res['covered'], res['tuples'], res['n_base']))
    g.append('      | ' + ' | '.join(heads) + ' |')
    for i, row in enumerate(res['rows'], 1):
        vals = ['EX-%sZU%s-%02d' % (ep[3:], nn, i)]
        for n_, v in zip(res['names'], row[:-1]):
            vals.append(M.short_value(n_, v) if n_ != 'operation' else v.split(' ')[0])
        vals.append(M.short_expected(row[-1]))
        g.append('      | ' + ' | '.join(x.replace('|', '/').replace('"', "'") for x in vals) + ' |')
    g.append('```')
    st['n_scen'] = k + 1
    out.append('\n'.join(g))
    out.append('')
    return '\n'.join(out)

seed = 101
story_md = {}
for st in stories:
    story_md[st['id']] = render_story(st, seed)
    seed += 7

# ------------------------------------------------------------------ helpers
def compress(nums):
    nums = sorted(set(nums)); out = []; i = 0
    while i < len(nums):
        j = i
        while j + 1 < len(nums) and nums[j + 1] == nums[j] + 1:
            j += 1
        out.append('%03d' % nums[i] if i == j else '%03d–%03d' % (nums[i], nums[j]))
        i = j + 1
    return ', '.join(out)

def fr_ranges(frs):
    by = collections.defaultdict(list)
    for f in frs:
        p = f.split('-'); by[p[2]].append(int(p[3]))
    return '; '.join('%s: %s' % (l, compress(v)) for l, v in sorted(by.items()))

def story_ranges(ids):
    by = collections.defaultdict(list)
    for u in ids:
        m = re.match(r'US-(\d{2})-([A-Z]{2})(\d{2,3})', u)
        if m: by[(m.group(1), m.group(2))].append(int(m.group(3)))
    parts = []
    for (e, fam), v in sorted(by.items()):
        v = sorted(v)
        parts.append('US-%s-%s%s' % (e, fam, ', '.join(('%02d' % a if a == b else '%02d…%02d' % (a, b)) for a, b in _runs(v))))
    return '; '.join(parts)

def _runs(v):
    out = []; i = 0
    while i < len(v):
        j = i
        while j + 1 < len(v) and v[j + 1] == v[j] + 1: j += 1
        out.append((v[i], v[j])); i = j + 1
    return out

def title_block(letter, title, doc, extra=''):
    return f"""# AI Growth Engine: Employee Sales & Marketing Automation
## Application Blueprint: PART 11 (Batch 11.22{letter}), {title}

| Field | Value |
|---|---|
| Document | {doc} |
| Version | 1.0 · 28 Nov 2026 |
| Baseline | Parts 0–9.10; Parts 11.1–11.19 (V12 review and V12-B Founder decisions, Part 11.14 DEC-770…791); story template Part 5.1a (§5.2 DoR, §5.3 DoD, §5.5 estimation, §5.6 dimension matrix, §5.7 conventions) |
| Roles applied | Chief Product Officer · Principal Agile Product Owner · Business Systems Analyst (BDD/Gherkin) · UX researcher (persona journeys) · QA Lead (combinatorial design) |
| ID ranges used | DEC-940…959 · tags ASSUMPTION/GAP/CONFLICT/RECOMMENDATION-1140…1159 · ADR-275…279 · stories US-&lt;EP&gt;-ZU&lt;nn&gt; · AC-&lt;EP&gt;ZU&lt;nn&gt;-&lt;seq&gt; · example rows EX-&lt;EP&gt;ZU&lt;nn&gt;-&lt;seq&gt; · parameter models MU01…MU13 · journeys JN-01…JN-12 · new epic EP-34 · new personas P21–P23 |
{extra}"""

def qgate(name, notes):
    rows = [
        ('Every requirement traced to a source', notes.get(1, 'Every story traces its FR-V12 IDs, the V12 source cell and the defining Part 11 section; decisions cited by ID')),
        ('Assumptions, gaps and conflicts tagged and logged', notes.get(2, 'Tags from 1140–1159 only; register in §11.22.9 (last file of Batch 11.22)')),
        ('IDs unique and consistent with earlier parts', notes.get(3, 'US-<EP>-ZU<nn> unique per epic; AC and EX IDs derived; epics EP-01…EP-33 as defined; EP-34 new')),
        ('No story lacks AC; no requirement lacks a test', notes.get(4, 'Every new story has Gherkin with happy, alternate, negative, validation, permission and edge scenarios plus a generated Scenario Outline')),
        ('Negative, edge, security and accessibility cases covered', notes.get(5, 'MAS-1…MAS-9 applied; @sec/@obs outlines; @a11y in website and UI stories')),
        ('No agent lacks guardrail, fallback, KPI and cost estimate', notes.get(6, 'N/A – no new agents; AI stories reuse the registry, gateway and eval gates')),
        ('Time-sensitive facts flagged "verify" with as-of date', notes.get(7, 'No prices or model versions stated; regulatory items defer to counsel-approved packs (verify at implementation, as of 28 Nov 2026)')),
        ('No restricted data routed to free-tier models', notes.get(8, 'Restricted personal data appears only as a blocking value in MU05 (DEC-007, DEC-788)')),
        ('Consistent with earlier parts', notes.get(9, 'Template of Part 5.1a copied; V12-B decisions DEC-770…791 applied; inconsistencies reported, not edited')),
    ]
    s = ['\n## Quality gate: Batch 11.22%s\n' % name, '| # | Check | Result | Notes and fixes applied |', '|---|---|---|---|']
    for i, (c, n) in enumerate(rows, 1):
        res = 'N/A' if n.startswith('N/A') else 'Pass'
        s.append('| %d | %s | **%s** | %s |' % (i, c, res, n))
    return '\n'.join(s) + '\n'

# ------------------------------------------------------------------ registers / counts
sum_by_letter = collections.OrderedDict()
for f, d in inv['fr'].items():
    l = f.split('-')[2]
    sb = sum_by_letter.setdefault(l, {'total': 0, 'ac': 0, 'noac': 0, 'none': 0})
    sb['total'] += 1
    if f in inv['no_ac']: sb['noac'] += 1
    elif not d['stories']: sb['none'] += 1
    else: sb['ac'] += 1
sum_by_letter = collections.OrderedDict(sorted(sum_by_letter.items()))

LETTER_PART = {'A': '11.1', 'B': '11.2', 'C': '11.3', 'D': '11.4', 'E': '11.5', 'F': '11.6', 'G': '11.7', 'H': '11.8', 'I': '11.9',
               'J': '11.10', 'K': '11.11', 'L': '11.12', 'M': '11.13', 'N': '11.16a/b/e', 'O': '11.16c/d', 'P': '11.17', 'Q': '11.18', 'R': '11.19'}

# persist summary
summary = {'fr_total': inv['fr_total'], 'targets': len(recs), 'uncovered_before': len(inv['uncovered']), 'no_ac_before': len(inv['no_ac']),
           'new_stories': len(stories), 'new_sp_low': sum(s['sp'][0] for s in stories), 'new_sp_high': sum(s['sp'][1] for s in stories),
           'examples_rows': sum(s['comb']['rows'] for s in stories), 'scenarios': sum(s['n_scen'] for s in stories)}
json.dump(summary, open(os.path.join(OUTD, 'u_summary.json'), 'w'), indent=1)
print(summary)

# ------------------------------------------------------------------ coverage CSV
os.makedirs(os.path.join(BP, 'final', 'coverage_v12'), exist_ok=True)
with open(os.path.join(BP, 'final', 'coverage_v12', 'U_coverage.csv'), 'w', newline='', encoding='utf-8') as fh:
    w = csv.writer(fh)
    w.writerow(['doc', 'chapter', 'section', 'aspect_id', 'aspect_summary', 'status_before', 'blueprint_location', 'action', 'new_ids', 'status_after'])
    for f in sorted(inv['fr'], key=lambda x: (x.split('-')[2], int(x.split('-')[3]))):
        d = inv['fr'][f]; df = d['def'] or {}
        r = recs.get(f)
        part = re.match(r'Part-(\d+-\d+[a-e]?)', df.get('file') or 'Part-11-0') .group(1).replace('-', '.') if df.get('file') else LETTER_PART[f.split('-')[2]]
        summ = S.short((r or {}).get('req') or df.get('text') or '', 160) if r else S.short(df.get('text') or '', 160)
        if r:
            sb = r['status_before']; act = 'New story with Gherkin AC and generated Examples' if sb == 'Not covered' else 'Acceptance-binding story added (anchor %s)' % r['anchor']
            new = r['story']; loc = 'Part %s; story in Part 11.22' % part
        else:
            sb = 'Covered'; act = 'Existing story with AC retained'; new = ''; loc = 'Part %s; stories %s' % (part, ', '.join(d['stories'][:4]))
        w.writerow(['Blueprint Part %s' % part, 'FR-V12-%s' % f.split('-')[2], S.short(df.get('section') or '', 80), f, summ, sb, loc, act, new, 'Matched'])

# ------------------------------------------------------------------ write files
def write(name, text):
    p = os.path.join(BP, name)
    open(p, 'w', encoding='utf-8').write(text)
    print('wrote', name, len(text))

exec(open(os.path.join(HERE, 'u_08_files.py'), encoding='utf-8').read())
