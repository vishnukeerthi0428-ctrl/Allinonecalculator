"""Group N build context: parses the source pack once and allocates every ID deterministically
(FR-V12-N, TC-V12-N, API-V12-N, step IDs), so Parts 11.16a/b/c and N_coverage.csv agree."""
import re, sys, os, json, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from n_common import load_all, mine, svc_no, inv_branches, md_escape
import n_spec as SP
import n_comb

D = load_all()
SC_H, SC, _ = D['Service_Catalog']
WC_H, WC, _ = D['Workflow_Catalog']
AT_H, AT, _ = D['Acceptance_Tests']
CW_H, CW, _ = D['Capability_Crosswalk']
CM_H, CM, _ = D['Cost_Model']
ER_H, ER, _ = D['Entitlement_Rules']
TM_H, TM, _ = D['Technical_Map']
SI_H, SI, _ = D['Service_Index']
MG_H, MG, _ = D['Migration']
SE_H, SE, _ = D['Shared_Engines']
SD_H, SD, _ = D['Sources_Decisions']

SVC = {svc_no(r['Automation ID']): r for r in SC if mine(r['Automation ID'])}
WFS = [r for r in WC if mine(r['Automation ID'])]
for r in WFS:
    r['_code'] = re.match(r'(INV-SVC-\d\d-WF\d\d)', r['Sub-automation name']).group(1)
    r['_name'] = r['Sub-automation name'].split('—', 1)[1].strip()
    r['_key'] = r['_code'][8:]  # '01-WF01'
ATM = {r['Test ID']: r for r in AT if mine(r['Service ID'])}
CMM = {r['Workflow ID']: r for r in CM if mine(r['Service ID'])}
ERM = {svc_no(r['Service ID']): r for r in ER if mine(r['Service ID'])}
SIM = {svc_no(r['Service ID']): r for r in SI if mine(r['Service ID'])}
MGM = {svc_no(r['Service ID']): r for r in MG if mine(r['Service ID'])}
TMM = collections.defaultdict(list)
for r in TM:
    if mine(r['Service ID']):
        TMM[svc_no(r['Service ID'])].append(r)
BRANCHES = inv_branches(D['com'])

# ------------------------------------------------------------------ step parsing and classification
EXT_VERBS = ('queue', 'send', 'dispatch', 'issue limited access', 'create event', 'confirm', 'prepare controlled delivery',
             'hold or dispatch', 'revoke', 'issue')
def classify(step, wkey, risk):
    s = step.lower()
    external_wf = risk.startswith('R2') or risk.startswith('R3')
    if external_wf and any(v in s for v in ('queue', 'send', 'dispatch', 'create event', 'confirm;', 'confirm', 'issue limited', 'controlled delivery', 'revoke when due')):
        return 'External effect (outbox)'
    if any(v in s for v in ('notify', 'alert', 'reminder')):
        return 'Internal notification'
    if any(v in s for v in ('route', 'assign', 'escalate', 'review', 'hold', 'request verification', 'require explicit approval', 'pause')):
        if not any(v in s for v in ('classify', 'draft', 'summar')):
            return 'Human review routing'
    if any(v in s for v in ('retrieve', 'fetch', 'poll', 'scan', 'collect', 'import', 'query authorized', 'transcribe')):
        return 'Evidence retrieval'
    if any(v in s for v in ('consent', 'jurisdiction', 'suppression', 'eligib', 'policy', 'budget', 'grant', 'nda', 'window',
                            'caps', 'template', 'scope', 'identity', 'issuer', 'signature', 'opted-in', 'required fields', 'authentication')):
        return 'Policy check (PDP)'
    if any(v in s for v in ('classify', 'draft', 'summar', 'extract', 'detect language', 'simulate', 'generate', 'explain',
                            'ground', 'assemble', 'select eligible', 'rank eligible', 'recommend', 'evaluate factual', 'qualify novelty', 'personali', 'localize')):
        return 'AI inference'
    if any(v in s for v in ('calculate', 'compare', 'score', 'match', 'validate', 'normalize', 'deduplicate', 'detect', 'rank',
                            'check', 'calibrate', 'show sensitivity', 'flag', 'invalidate', 'suppress duplicate')):
        return 'Deterministic calculation'
    return 'Domain persistence'

CLS = {
 'Evidence retrieval': ('Ingestion / connector engine', 'evidence_set {items, source_ref, observed_at, hash, rights}', 'SOURCE_DENIED → **Held**', 'Ingestion via AU-007 source permission, AU-014 host filter, AU-005 sanitizer', 'IT (adapter stub) + SEC', 'unauthorised or stale source rejected; provenance hash and rights stored'),
 'AI inference': ('Model gateway + agent', 'candidate {artifact_ref, confidence, reason_codes, review_state}', 'REVIEW_REQUIRED → **Waiting (AWAITING_APPROVAL)**', 'Model gateway AU-001 (Tier 0 → 1a → 1b; Tier 3 degrade), AU-003 schema validation, AG-166 guard on investor-facing text; output is a draft only', 'AIE + CT schema', 'output validates against schema; claims cited; AG-166 verdict recorded; untrusted input cannot invoke tools'),
 'Deterministic calculation': ('Rules / calculation engine', 'calculation {value, unit, assumptions, evidence_refs}', 'INVALID_INPUT → **Held**', 'Deterministic domain service; Decimal (DEC-027); zero model calls', 'UT golden fixture', 'golden fixture exact; missing value never invented'),
 'Policy check (PDP)': ('PDP + AU-201/AU-202/AU-203/AU-208', 'decision {allow|hold|block, reason_codes, pack_versions}', 'POLICY_DENIED → **Blocked**', 'PDP (Part 3.1) extended with securities gate (ADR-231); fail closed', 'UT decision table + IT', 'every rule branch exercised; unknown → hold/block; reason code and pack version audited'),
 'External effect (outbox)': ('Dispatcher via transactional outbox', 'effect {effect_id, provider_ref, state}', 'TIMEOUT_AFTER_SUBMIT → **Reconciling**', 'Outbox (M06) + dispatch-time PDP recheck (scope, consent, pack, eligibility, budget, approval hash) + idempotency key', 'IT replay + CHAOS', 'exactly one effect per idempotency key; recheck denies after revocation; uncertain → reconcile before retry'),
 'Internal notification': ('Notification service (NT)', 'notification {recipient_role, channel=in-app/email-internal, dedupe_key}', 'DUPLICATE → **Suppressed**', 'Notification service NT/NX (Part 2.4); dedupe key', 'IT', 'one notification per dedupe key; internal recipients only'),
 'Human review routing': ('Work queue / approval service', 'task {queue, assignee_role, sla_due, reason}', 'SLA_BREACH → **Escalated**', 'Approval/task service (A207/A220); SLA timers', 'IT + SYS', 'task created with correct role and SLA; automation paused until disposition'),
 'Domain persistence': ('Domain service (investment app)', 'domain_result {artifact_ref, status, evidence_refs}', 'INVALID_STATE → **Held**', 'Domain module: revision check (NFR-025), single transaction with audit and outbox', 'UT + IT', 'state change atomic with audit and outbox row'),
}

OVR = {('01-WF01', 1): 'AI inference', ('01-WF01', 3): 'AI inference', ('01-WF03', 2): 'Deterministic calculation',
       ('02-WF02', 1): 'Policy check (PDP)', ('02-WF04', 2): 'Deterministic calculation', ('03-WF03', 2): 'Policy check (PDP)',
       ('04-WF03', 1): 'Policy check (PDP)', ('04-WF03', 3): 'Domain persistence', ('04-WF04', 3): 'Domain persistence',
       ('05-WF04', 4): 'External effect (outbox)', ('06-WF04', 1): 'AI inference', ('06-WF04', 4): 'Domain persistence',
       ('07-WF01', 3): 'Deterministic calculation', ('07-WF02', 3): 'Deterministic calculation', ('08-WF01', 2): 'Deterministic calculation',
       ('08-WF02', 2): 'AI inference', ('09-WF03', 3): 'Human review routing', ('09-WF02', 3): 'Deterministic calculation',
       ('06-WF02', 2): 'Policy check (PDP)'}


def step_class(r, k, st):
    return OVR.get((r['_key'], k)) or classify(st, r['_key'], SP.W[r['_key']]['risk'])


def steps_of(r):
    return [s.strip() for s in r['Detailed functionality'].split(';') if s.strip()]

# ------------------------------------------------------------------ ID allocation
FR_WF = {}
for i, r in enumerate(WFS):
    FR_WF[r['_code']] = 'FR-V12-N-%03d' % (101 + i)

TC = collections.OrderedDict()   # key -> TC id
TC_INFO = {}
_n = [0]
def tc(key, info):
    _n[0] += 1
    t = 'TC-V12-N-%03d' % _n[0]
    TC[key] = t
    TC_INFO[t] = info
    return t

CLASSES = ['POS', 'INPUT', 'SCOPE', 'ENT', 'DUP', 'QUALITY', 'BUDGET', 'RECOVERY', 'SEC']
for r in WFS:
    w = SP.W[r['_key']]
    for k, st in enumerate(steps_of(r), 1):
        tc((r['_code'], 'STEP', k), {'wf': r['_code']})
    if any(step_class(r, k, st) == 'External effect (outbox)' for k, st in enumerate(steps_of(r), 1)) or w['risk'][:2] in ('R2', 'R3'):
        tc((r['_code'], 'STEP', 'GATE'), {'wf': r['_code']})
    cls = CLASSES + (['APPROVAL', 'EFFECT'] if w['risk'][:2] in ('R2', 'R3') else [])
    for c in cls:
        tc((r['_code'], c), {'wf': r['_code']})
for n in range(1, 13):
    tc(('ENT', n), {'svc': n})
MODELS = n_comb.build()
for m in MODELS:
    for i, row in enumerate(m['rows'] + m['base'], 1):
        tc((m['id'], i), {'model': m['id']})
TC_LAST = _n[0]

# APIs
def api_ops():
    ops = collections.OrderedDict()
    for n in range(1, 13):
        for r in TMM[n]:
            for op in r['Existing route inventory'].split(';'):
                op = op.strip()
                if op and op not in ops:
                    ops[op] = set()
                if op:
                    ops[op].add(n)
        for op in SVC[n]['Related API operations'].split(';'):
            op = op.strip()
            if op:
                ops.setdefault(op, set()).add(n)
    out = []
    for i, (op, svcs) in enumerate(sorted(ops.items(), key=lambda x: (x[0].split(' ', 1)[1], x[0])), 1):
        out.append(('API-V12-N-%03d' % i, op, sorted(svcs)))
    base = len(out)
    for j, (m, p, d, role, ent) in enumerate(SP.EXTRA_API, 1):
        out.append(('API-V12-N-%03d' % (base + j), f'{m} {p}', [], d, role, ent))
    return out
APIS = api_ops()

def wf_screens(r):
    ids = [x.strip() for x in r['Related UI screen IDs'].split(';') if x.strip()]
    return [SP.A_OF.get(x, x) for x in ids]

def svc_key(n):
    return 'INV-SVC-%02d' % n

def cost_ag(t):
    inp, cache, out, calls, e = t
    h = 90 * ((inp - cache) * 0.10 + cache * (0.6 * 0.01 + 0.4 * 0.125) + out * 0.50) / 1e6
    s = 90 * ((inp - cache) * 2 + cache * (0.6 * 0.10 + 0.4 * 2.50) + out * 10) / 1e6
    b = (1 - e) * h + e * s
    base = b * calls
    return h, s, b, base * 0.3, base, base * 3

if __name__ == '__main__':
    print('services', len(SVC), 'workflows', len(WFS), 'AT', len(ATM), 'CM', len(CMM), 'TM', sum(len(v) for v in TMM.values()))
    print('TC last', TC_LAST, 'APIs', len(APIS), 'branches', len(BRANCHES))
    c = collections.Counter()
    for r in WFS:
        for st in steps_of(r):
            c[classify(st, r['_key'], SP.W[r['_key']]['risk'])] += 1
    print(c)
