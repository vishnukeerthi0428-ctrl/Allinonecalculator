#!/usr/bin/env python3
"""Part 11.22 (Group U) parameter models, covering-array generator and oracles.

Imported by u_04_build.py. Every story's Scenario Outline `Examples:` rows are
generated here from a declared parameter model:
  * a t-way covering array (t = 2 pairwise, or t = 3 for safety-, money- or
    law-critical capabilities) built greedily with a deterministic seed,
    constraint-aware (forbidden partial assignments are never generated);
  * plus one "baseline allow" row per operation value (risk-based addition, as
    Part 5.1a §5.6.5 does with DM-R rows) so the happy path is always present;
  * an exhaustive enumeration where the model space is <= 64 combinations.
The oracle computes the expected result of each row from the precedence of the
Policy Decision Point checks (scope -> authentication -> entitlement ->
permission / separation of duties -> residency -> jurisdiction pack -> consent
-> data class -> autonomy / mandate -> provider -> budget), so no expected
result is typed by hand.
"""
import itertools, random

# ---------------------------------------------------------------- generator
def covering_array(names, doms, t, seed=11, candidates=40, valid=None):
    k = len(names)
    ok = valid or (lambda d: True)
    rng = random.Random(seed)
    t = min(t, k)
    combos = list(itertools.combinations(range(k), t))
    uncovered = set()
    for cols in combos:
        for vals in itertools.product(*[range(len(doms[c])) for c in cols]):
            if ok({names[c]: doms[c][v] for c, v in zip(cols, vals)}):
                uncovered.add((cols, vals))
    total = len(uncovered)
    rows = []
    while uncovered:
        best, bestg = None, -1
        pool = list(uncovered)
        for _ in range(candidates):
            cols, vals = pool[rng.randrange(len(pool))]
            row = [None] * k
            for c, v in zip(cols, vals):
                row[c] = v
            order = [i for i in range(k) if row[i] is None]
            rng.shuffle(order)
            for i in order:
                bv, bg = None, -1
                cand = list(range(len(doms[i])))
                rng.shuffle(cand)
                for v in cand:
                    row[i] = v
                    part = {names[j]: doms[j][row[j]] for j in range(k) if row[j] is not None}
                    if not ok(part):
                        continue
                    g = sum(1 for cs in combos if i in cs and all(row[c] is not None for c in cs)
                            and (cs, tuple(row[c] for c in cs)) in uncovered)
                    if g > bg:
                        bv, bg = v, g
                row[i] = bv if bv is not None else 0
            full = {names[j]: doms[j][row[j]] for j in range(k)}
            if not ok(full):
                continue
            g = sum(1 for cs in combos if (cs, tuple(row[c] for c in cs)) in uncovered)
            if g > bestg:
                best, bestg = list(row), g
        if best is None or bestg <= 0:
            # fall back: drop tuples that cannot be completed into a valid row
            cols, vals = pool[0]
            uncovered.discard((cols, vals)); total -= 1
            continue
        rows.append(best)
        for cs in combos:
            uncovered.discard((cs, tuple(best[c] for c in cs)))
    return [[doms[j][r[j]] for j in range(k)] for r in rows], total

def verify(names, doms, rows, t, valid=None):
    ok = valid or (lambda d: True)
    idx = [{v: i for i, v in enumerate(d)} for d in doms]
    need = set()
    for cols in itertools.combinations(range(len(names)), min(t, len(names))):
        for vals in itertools.product(*[range(len(doms[c])) for c in cols]):
            if ok({names[c]: doms[c][v] for c, v in zip(cols, vals)}):
                need.add((cols, vals))
    have = set()
    for r in rows:
        ri = [idx[j][r[j]] for j in range(len(names))]
        for cols in itertools.combinations(range(len(names)), min(t, len(names))):
            have.add((cols, tuple(ri[c] for c in cols)))
    return len(need), len(need & have)

def space(doms):
    n = 1
    for d in doms:
        n *= len(d)
    return n

# ---------------------------------------------------------------- values
# Each value is (label, effect) where effect is None (passes this check) or
# (precedence, outcome text). Lower precedence wins (PDP order).
X = None
AUTH = {
    'A1 authorised': X,
    'A3 SoD conflict or over limit': (4, '403 `SOD_CONFLICT` – routed to a second, distinct approver; no effect'),
    'A5 wrong role or company': (4, '403 `PERMISSION_DENIED`; NSE; audit outcome=denied'),
    'T5 other tenant': (1, 'uniform 404 `NOT_FOUND`; zero rows, events or provider calls (BRL-TEN-04)'),
}
REGION = {
    'IN tenant · Mumbai': X,
    'EU tenant · EU region': X,
    'EU tenant · routed to Mumbai': (5, '409 `RESIDENCY_ZONE_MISMATCH` – nothing written outside the EU zone (DEC-772)'),
}
JURIS = {
    'IN pack Approved': X,
    'EU pack Approved': X,
    'UK pack Draft': (6, 'HOLD `PACK_NOT_ACTIVE` – capability built, not active in UK until counsel sign-off'),
}
CHANNEL = {'C1 web desktop': X, 'C2 mobile web': X, 'C3 API': X}
DATACLASS = {
    'Public': X, 'Internal': X, 'Confidential': X,
    'Restricted personal': (8, 'Tier 2 and unapproved models excluded; masked or region-pinned approved model only (DEC-788)'),
}
AUTONOMY = {
    'L1 human approval': (9, 'PENDING_APPROVAL – effect only after a named human approves the payload hash'),
    'L2 exact-item approval': (9, 'PENDING_APPROVAL – exact item hash approved, then one effect'),
    'L3 active mandate': X,
    'L3 mandate revoked': (9, 'ROUTE `MANDATE_INACTIVE` – falls back to L2 approval; no mandated effect (DEC-779)'),
}
SKU = {
    'SKU active': X,
    'SKU suspended': (3, '409 `SUBSCRIPTION_SUSPENDED` – read-only; no new run; ledger preserved'),
    'SKU not subscribed': (3, '403 `ENTITLEMENT_REQUIRED`; no reservation'),
}
CONSENT = {
    'consent valid': X,
    'consent withdrawn': (7, 'HOLD `CONSENT_WITHDRAWN` – queued effects held; suppression applied'),
    'consent unknown': (7, 'HOLD `CONSENT_UNKNOWN` – no outbound effect'),
}
PROVIDER = {
    'I1 provider up': X,
    'I3 provider down': (10, 'retry with backoff; circuit opens; no duplicate effect'),
    'I4 outcome uncertain': (10, 'RECONCILING – uncertain write reconciled before any retry (DEC-050)'),
}

def P(*labels):
    return {l: X for l in labels}

# ---------------------------------------------------------------- models
# risk: 3 -> 3-way, 2 -> pairwise. params: ordered list of (name, value map)
MODELS = {
 'MU01': dict(title='Commercial catalogue, subscription and billing', risk=2, params=[
    ('persona', P('P13 SaaS client admin (R17)', 'P08 finance (R08)', 'P12 platform billing (R14)')),
    ('authority', AUTH), ('service/SKU', SKU), ('channel', CHANNEL), ('jurisdiction', {
        'IN GST rules Approved': X, 'EU VAT rules Approved': X,
        'UK VAT rules Draft': (6, 'HOLD `TAX_RULE_NOT_APPROVED` – invoice line held for the tax adviser (DEC-776)')}),
    ('region', REGION)]),
 'MU02': dict(title='Enterprise identity, access and audit', risk=3, params=[
    ('persona', P('P11 tenant admin (R12)', 'P02 startup head (R02)', 'P12 platform support (R13)')),
    ('authority', AUTH), ('channel', CHANNEL),
    ('session/MFA', {'phishing-resistant MFA': X, 'OTP only': (4, '403 `STEP_UP_REQUIRED` for privileged actions'),
                     'session expired or revoked': (2, '401 `SESSION_REVOKED` – sign in again; no action')}),
    ('region', REGION)]),
 'MU03': dict(title='Developer platform, API contracts and connectors', risk=2, params=[
    ('persona', P('P18 integration admin (R12I)', 'P10 automation lead (R11)', 'P13 SaaS client developer (R17)')),
    ('authority', AUTH), ('channel', {'C3 API key': X, 'C3 OAuth client': X, 'webhook / worker': X}),
    ('credential', {'vault reference valid': X, 'secret expired': (3, '401 `CREDENTIAL_EXPIRED` – owner alerted; no call'),
                    'credential revoked': (3, '401 `CREDENTIAL_REVOKED`; calls blocked')}),
    ('provider', PROVIDER), ('region', REGION)]),
 'MU04': dict(title='Data platform, residency and records', risk=3, params=[
    ('persona', P('P11 tenant admin (R12)', 'P01 owner (R01)', 'P16 service identity (R19)')),
    ('authority', AUTH),
    ('data class', DATACLASS),
    ('db context', {'app.tenant_id and company set': X,
                    'tenant context missing': (1, 'SQLSTATE 42501 – statement refused (DB-T2)'),
                    'company scope missing': (2, 'zero rows returned; no write')}),
    ('region', REGION), ('channel', P('C3 API', 'worker job'))]),
 'MU05': dict(title='AI governance, evaluation, prompts and cost', risk=3, params=[
    ('persona', P('P10 AI lead (R11)', 'P03 growth manager (R03)', 'P16 AI agent identity (R20)')),
    ('data class', DATACLASS),
    ('registry state', {'model Approved for class and zone': X,
                        'model candidate only': (8, 'BLOCK `MODEL_NOT_APPROVED` – registry gate (DEC-788)'),
                        'prompt version unapproved': (8, 'BLOCK `PROMPT_NOT_APPROVED` – PRM gate (AU-153)')}),
    ('autonomy/mandate', {'L1 human approval': AUTONOMY['L1 human approval'], 'L3 active mandate': X,
                          'L3 mandate revoked': AUTONOMY['L3 mandate revoked']}),
    ('budget', {'within budget': X, 'soft cap 80%': X, 'hard cap reached': (11, 'HELD `AI_BUDGET_EXHAUSTED` – no provider call')}),
    ('region', REGION)]),
 'MU06': dict(title='Jurisdiction packs, consent and legal controls', risk=3, params=[
    ('persona', P('P09 DPO / counsel (R10)', 'P05 marketer (R05)', 'P03 sales executive (R03)')),
    ('jurisdiction', {'IN pack Approved': X, 'EU pack Approved': X, 'UK pack Draft': JURIS['UK pack Draft'],
                      'US pack Expired': (6, 'HOLD `PACK_EXPIRED` – stricter outcome until re-approved')}),
    ('consent', CONSENT), ('channel', P('email', 'SMS / voice', 'WhatsApp')),
    ('data class', {'Internal': X, 'Confidential': X, 'Restricted personal': X}),
    ('region', REGION)]),
 'MU07': dict(title='Workflow runtime, preflight, autonomy and mandates', risk=3, params=[
    ('persona', P('P10 automation lead (R11)', 'P03 requester (R03)', 'P02 approver (R02)')),
    ('authority', AUTH), ('autonomy/mandate', AUTONOMY),
    ('run state', {'Queued': X, 'Running (pinned revision)': X,
                   'Uncertain effect': (10, 'RECONCILING – no retry until the effect is reconciled')}),
    ('budget', {'within budget': X, 'hard cap reached': (11, 'HELD `BUDGET_EXHAUSTED`; reservation released')}),
    ('service/SKU', SKU)]),
 'MU08': dict(title='Investor securities controls', risk=3, params=[
    ('persona', P('P21 investor-relations user (R03, INV)', 'P09 counsel (R10)', 'P22 invited investor (R21, Part 11.16a)')),
    ('jurisdiction', {'IN s.42 pack Approved': X, 'US 506(b) pack Approved': X, 'US 506(c) pack Approved': X,
                      'UK FPO pack Draft': (6, 'HOLD `PACK_NOT_ACTIVE` – no offer material (DEC-783)')}),
    ('investor eligibility', {'verified eligible': X, 'unverified': (6, 'BLOCK `ELIGIBILITY_UNVERIFIED` – no offer material'),
                              'sanctions possible match': (5, 'HOLD for R10 review; no tip-off')}),
    ('solicitation', {'pre-existing relationship': X, 'no relationship': (6, 'BLOCK `GENERAL_SOLICITATION` for private routes')}),
    ('autonomy/mandate', {'L1 two-person approval': (9, 'PENDING two approvals (R02 + R10) on the content hash'),
                          'L3 mandate (inv_ir_message only)': X}),
    ('region', REGION)]),
 'MU09': dict(title='Investment Automation workflows (INV-SVC-13…24)', risk=3, params=[
    ('persona', P('P21 investor-relations user (R03, INV)', 'P08 finance (R08)', 'P09 counsel (R10)')),
    ('authority', AUTH),
    ('jurisdiction', {'IN pack Approved': X, 'US pack Approved': X, 'UK pack Draft': JURIS['UK pack Draft']}),
    ('approval', {'two approvals on hash': X, 'one approver only': (9, 'HELD `TWO_APPROVALS_REQUIRED`'),
                  'hash changed after approval': (9, 'HOLD `APPROVAL_STALE` – re-approval required')}),
    ('service/SKU', SKU), ('region', REGION)]),
 'MU10': dict(title='Operations, security programme and release evidence', risk=2, params=[
    ('persona', P('P12 platform operator (R13)', 'P10 release manager (R11)', 'P15 auditor (R15)')),
    ('authority', AUTH),
    ('evidence', {'evidence complete': X, 'evidence missing': (4, 'GATE BLOCKED `EVIDENCE_MISSING`'),
                  'evidence stale': (4, 'GATE BLOCKED `EVIDENCE_STALE` – re-run required')}),
    ('severity', P('SEV1', 'SEV3', 'no incident')), ('region', REGION),
    ('channel', P('C1 web desktop', 'C3 API', 'pager / phone'))]),
 'MU11': dict(title='Website, acquisition, help and customer success', risk=2, params=[
    ('persona', P('P15 anonymous visitor (R18)', 'P14 external customer (R16)', 'P13 SaaS client admin (R17)')),
    ('channel', P('C1 web desktop', 'C2 mobile web 360 px', 'assistive technology')),
    ('locale', P('en-IN', 'hi-IN', 'de-DE')), ('consent', CONSENT),
    ('service/SKU', P('SKU released', 'SKU pilot', 'SKU planned')), ('region', REGION)]),
 'MU12': dict(title='Global expansion, certification and tax', risk=3, params=[
    ('persona', P('P01 owner (R01)', 'P09 counsel (R10)', 'P08 finance (R08)')),
    ('market', {'India': X, 'EU (DE)': X, 'UAE': X,
                'US': (6, 'NOT ACTIVE – market opens only after counsel pack and tax adviser approval (DEC-776)')}),
    ('locale', P('en-IN', 'de-DE', 'ar-AE (RTL)')),
    ('tax/currency', {'rule Approved · native currency': X, 'FX rate missing': (6, 'converted total withheld; native shown with `FX_RATE_MISSING`'),
                      'tax rule Draft': (6, 'HOLD `TAX_RULE_NOT_APPROVED`')}),
    ('evidence', {'evidence complete': X, 'evidence missing': (4, 'BLOCKED `EVIDENCE_MISSING`')}),
    ('region', REGION)]),
 'MU13': dict(title='Analytics, metrics and management views', risk=2, params=[
    ('persona', P('P01 owner (R01)', 'P02 startup head (R02)', 'P13 SaaS client admin (R17)')),
    ('authority', AUTH),
    ('scope', {'single company': X, 'portfolio grant aggregate': X,
               'portfolio grant revoked': (2, '403 `GRANT_REVOKED` – aggregates hidden')}),
    ('currency', P('INR only', 'INR + EUR with approved rate', 'INR + EUR rate missing')),
    ('consent', CONSENT), ('channel', P('C1 web desktop', 'C2 mobile web', 'C3 API'))]),
}

def model_rows(mid, ops, seed):
    """ops: list of (label, allow_text). Returns dict with params, rows (with expected),
    method, counts."""
    m = MODELS[mid]
    names = ['operation'] + [n for n, _ in m['params']]
    eff = {'operation': {lbl: X for lbl, _ in ops}}
    for n, vmap in m['params']:
        eff[n] = vmap
    doms = [list(eff[n].keys()) for n in names]
    t = m['risk']
    def valid(d):
        # constraints: anonymous visitors never use the API; service identities never use browser channels
        p = d.get('persona', '')
        c = d.get('channel', '')
        if 'anonymous' in p and ('API' in c):
            return False
        if ('service identity' in p or 'AI agent identity' in p) and c.startswith(('C1', 'C2')):
            return False
        if 'invited investor' in p and d.get('authority', '') == 'A3 SoD conflict or over limit':
            return False
        return True
    sp = space(doms)
    if sp <= 64:
        rows = [list(r) for r in itertools.product(*doms) if valid(dict(zip(names, r)))]
        method, need = 'exhaustive enumeration', None
    else:
        rows, need = covering_array(names, doms, t, seed=seed, valid=valid)
        method = ('3-way' if t == 3 else 'pairwise (2-way)') + ' greedy covering array, constraint-aware, seed %d' % seed
    n_need, n_have = verify(names, doms, rows, t if sp > 64 else 1, valid)
    # risk-based additions: one baseline-allow row per operation
    base = []
    for lbl, _ in ops:
        r = [lbl]
        for n in names[1:]:
            r.append(next(v for v, e in eff[n].items() if e is None) if any(e is None for e in eff[n].values()) else list(eff[n])[0])
        if valid(dict(zip(names, r))) and r not in rows:
            base.append(r)
    allow = dict(ops)
    out = []
    for r in rows + base:
        effects = [eff[n][v] for n, v in zip(names, r) if eff[n][v] is not None]
        if effects:
            effects.sort(key=lambda e: e[0])
            exp = effects[0][1]
        else:
            exp = 'ALLOW – ' + allow[r[0]]
        out.append(r + [exp])
    return dict(mid=mid, title=m['title'], names=names, doms=doms, t=t if sp > 64 else 'all',
                method=method, space=sp, tuples=n_need, covered=n_have, n_array=len(rows),
                n_base=len(base), rows=out)

# ---------------------------------------------------------------- display codes (Examples rows stay within the PDF line width)
import re as _re
SHORT = {
    'IN tenant · Mumbai': 'IN', 'EU tenant · EU region': 'EU', 'EU tenant · routed to Mumbai': 'EU→IN (misrouted)',
    'A1 authorised': 'A1', 'A3 SoD conflict or over limit': 'A3 SoD/limit', 'A5 wrong role or company': 'A5 wrong role', 'T5 other tenant': 'T5 other tenant',
    'C1 web desktop': 'C1 web', 'C2 mobile web': 'C2 mobile', 'C2 mobile web 360 px': 'C2 360 px', 'C3 API': 'C3 API', 'C3 API key': 'C3 key',
    'C3 OAuth client': 'C3 OAuth', 'webhook / worker': 'webhook', 'assistive technology': 'AT reader',
    'phishing-resistant MFA': 'passkey MFA', 'session expired or revoked': 'session revoked',
    'vault reference valid': 'vault ref ok', 'secret expired': 'secret expired', 'credential revoked': 'cred revoked',
    'I1 provider up': 'I1 up', 'I3 provider down': 'I3 down', 'I4 outcome uncertain': 'I4 uncertain',
    'Restricted personal': 'Restricted', 'app.tenant_id and company set': 'context set', 'tenant context missing': 'no tenant ctx',
    'company scope missing': 'no company scope', 'model Approved for class and zone': 'model Approved', 'model candidate only': 'candidate only',
    'prompt version unapproved': 'prompt unapproved', 'L1 human approval': 'L1', 'L2 exact-item approval': 'L2', 'L3 active mandate': 'L3 mandate',
    'L3 mandate revoked': 'L3 revoked', 'L1 two-person approval': 'L1 two-person', 'L3 mandate (inv_ir_message only)': 'L3 IR-msg mandate',
    'within budget': 'in budget', 'soft cap 80%': 'soft cap', 'hard cap reached': 'hard cap', 'Running (pinned revision)': 'Running',
    'Uncertain effect': 'Uncertain', 'IN s.42 pack Approved': 'IN s42 ✓', 'US 506(b) pack Approved': 'US 506b ✓', 'US 506(c) pack Approved': 'US 506c ✓',
    'UK FPO pack Draft': 'UK FPO draft', 'verified eligible': 'eligible', 'sanctions possible match': 'sanctions match?',
    'pre-existing relationship': 'relationship', 'no relationship': 'no relationship', 'two approvals on hash': '2 approvals',
    'one approver only': '1 approver', 'hash changed after approval': 'hash changed', 'evidence complete': 'complete', 'evidence missing': 'missing',
    'evidence stale': 'stale', 'consent valid': 'valid', 'consent withdrawn': 'withdrawn', 'consent unknown': 'unknown',
    'SKU active': 'active', 'SKU suspended': 'suspended', 'SKU not subscribed': 'not subscribed', 'SKU released': 'released', 'SKU pilot': 'pilot', 'SKU planned': 'planned',
    'IN pack Approved': 'IN ✓', 'EU pack Approved': 'EU ✓', 'UK pack Draft': 'UK draft', 'US pack Expired': 'US expired', 'US pack Approved': 'US ✓',
    'IN GST rules Approved': 'IN GST ✓', 'EU VAT rules Approved': 'EU VAT ✓', 'UK VAT rules Draft': 'UK VAT draft',
    'rule Approved · native currency': 'rule ✓ native', 'FX rate missing': 'FX missing', 'tax rule Draft': 'tax draft',
    'single company': 'company', 'portfolio grant aggregate': 'portfolio grant', 'portfolio grant revoked': 'grant revoked',
    'INR + EUR with approved rate': 'INR+EUR rate ✓', 'INR + EUR rate missing': 'INR+EUR no rate', 'INR only': 'INR',
    'ar-AE (RTL)': 'ar-AE RTL', 'EU (DE)': 'EU-DE', 'pager / phone': 'pager', 'SMS / voice': 'SMS/voice', 'no incident': 'none',
}
def short_value(name, v):
    if v in SHORT:
        return SHORT[v]
    if name == 'persona':
        p = _re.search(r'\bP\d{2}\b', v); r = _re.search(r'\bR\d{2}[A-Z]?\b', v)
        return '%s/%s' % (p.group(0) if p else v.split(' ')[0], r.group(0)) if r else (p.group(0) if p else v)
    return v

def short_expected(e):
    if e.startswith('ALLOW – '):
        t = e[8:]
        t = _re.split(r';|\. ', t)[0]
        return 'ALLOW: ' + (t if len(t) <= 52 else t[:52].rsplit(' ', 1)[0])
    t = e.replace('`', '')
    t = _re.split(r' – |; ', t)[0]
    return t if len(t) <= 60 else t[:60].rsplit(' ', 1)[0]
