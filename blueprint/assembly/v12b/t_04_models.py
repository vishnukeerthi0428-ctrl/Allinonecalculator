"""Group T (Part 11.21): master combinatorial models, rule-based oracles and generation.

Run:  python3 -I assembly/v12b/t_04_models.py
Writes assembly/v12b/t_out/models.json (every generated row with its expected result) and
assembly/v12b/t_out/summary.json (counts and verification results).

Models (IDs used in Part 11.21):
  PM-T01  platform SKU invocation, valid set              pairwise (2-way)
  PM-T01N platform SKU invocation, invalid values         single-fault, each invalid value x tenant and x region
  PM-T02  Investment Automation SKU invocation            pairwise + single-fault layer
  PM-T03  consequential-effect gateway (money/law/safety) variable strength: 3-way among controls, 2-way effect x control (L1);
                                                          3-way positive sub-space (L2); single-fault x effect (L3)
  PM-T04  data residency                                  3-way
  PM-T05  multi-tenant isolation and RLS                  3-way caller x target x operation + 2-way path x each
  PM-T06  localization and RTL                            pairwise
  PM-T07  accessibility (WCAG 2.2 AA)                     pairwise
  PM-T08  performance, load and soak workload profiles    pairwise
  PM-T09  resilience with consequential work in flight    3-way
  XT-10…XT-15  exhaustive small spaces (<= 64)
  PM-T16  AI evaluation suites (111) x change trigger…    variable strength: each suite once + pairwise among the rest
"""
import json, os, sys, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from t_02_engine import generate, verify, raw_product, valid_count, exhaustive  # noqa: E402
import t_03_catalogue as C  # noqa: E402

OUT = C.BP + '/assembly/v12b/t_out'
os.makedirs(OUT, exist_ok=True)
NEG = '~'


def neg(v):
    return isinstance(v, str) and v.startswith(NEG)


MODELS = collections.OrderedDict()


def add_model(mid, **kw):
    MODELS[mid] = kw


# =============================================================================================
# PM-T01 platform SKU invocation
# =============================================================================================
ROLE_CH = {r: ['Admin web', 'Admin mobile web'] for r in C.ADMIN_ROLES}
ROLE_CH.update({'R16': ['Portal'], 'R17': ['Public website'], 'R18': ['Public website'],
                'R19': ['Developer API', 'Event/webhook'], 'R20': ['Agent tool call']})
ROLE_IDN = {r: ['Password + MFA', 'SSO SAML', 'SSO OIDC'] for r in C.ADMIN_ROLES}
ROLE_IDN.update({'R16': ['Password + MFA', 'SSO OIDC'], 'R17': ['Password + MFA', 'SSO OIDC'], 'R18': ['Anonymous session'],
                 'R19': ['API key', 'OAuth client credentials', 'Signed webhook'], 'R20': ['Workload identity']})
CH_IDN = {'Developer API': ['API key', 'OAuth client credentials'], 'Event/webhook': ['Signed webhook'],
          'Agent tool call': ['Workload identity']}
CH_DEV = {'Admin web': ['Desktop 1440', 'Laptop 1280', 'Tablet 768'], 'Admin mobile web': ['Tablet 768', 'Mobile 390', 'Mobile 320'],
          'Public website': ['Desktop 1440', 'Laptop 1280', 'Tablet 768', 'Mobile 390', 'Mobile 320'],
          'Portal': ['Desktop 1440', 'Laptop 1280', 'Tablet 768', 'Mobile 390', 'Mobile 320'],
          'Developer API': ['Headless'], 'Event/webhook': ['Headless'], 'Agent tool call': ['Headless']}
ROLE_SKUS = dict(C.ROLE_SKUS)
ROLE_SKUS['R20'] = C.AI_SKUS


def role_sku_ok(role, sku):
    return sku in ROLE_SKUS[role]


def c01(r, skip=()):
    g = lambda k: None if (k in skip or neg(r.get(k))) else r.get(k)  # noqa: E731
    t, plan, sku, reg, loc, role, ch = g('tenant'), g('plan'), g('sku'), g('region'), g('locale'), g('role'), g('channel')
    dat, con, prv, aut, air, dev, brw, sla, idn = (g('data'), g('consent'), g('provider'), g('autonomy'), g('ai_route'),
                                                   g('device'), g('browser'), g('sla'), g('identity'))
    if t and plan:
        if t.startswith('T1') and plan != 'FULL':
            return False
        if t in ('EXT-ENT', 'EXT-MSP') and plan == 'TRIAL':
            return False
    if t and reg and t.startswith('T1') and reg != 'IN':
        return False
    if reg and loc and loc not in C.LOCALE_ZONE[reg]:
        return False
    if t and sla:
        if t.startswith('T1') and sla != 'Business 99.9%':
            return False
        if t == 'EXT-SMB' and sla == 'Enterprise 99.95%':
            return False
        if t == 'EXT-ENT' and sla == 'Standard 99.5%':
            return False
    if role and t:
        if role == 'R21' and t != 'EXT-MSP':
            return False
        if role == 'R17' and t.startswith('T1'):
            return False
    if role and sku and not role_sku_ok(role, sku):
        return False
    if role and ch and ch not in ROLE_CH[role]:
        return False
    if role and idn and idn not in ROLE_IDN[role]:
        return False
    if ch and idn and ch in CH_IDN and idn not in CH_IDN[ch]:
        return False
    if ch and dev and dev not in CH_DEV[ch]:
        return False
    if dev and brw and ((dev == 'Headless') != (brw == 'Headless')):
        return False
    if idn == 'SSO SAML' and t and t not in ('EXT-ENT', 'EXT-MSP') and not t.startswith('T1'):
        return False
    if dat and con:
        if con == 'Not applicable' and dat not in ('Public', 'Internal', 'Confidential'):
            return False
        if con != 'Not applicable' and dat not in ('Personal', 'Confidential', 'Restricted'):
            return False
    if dat and air:
        if air.startswith('Tier 2') and dat not in ('Public', 'Internal'):
            return False
        if air.startswith('Open-weight') and dat == 'Restricted':
            return False
    if t == 'T1-MedMaarg' and dat == 'Restricted':
        return False
    if sku in ('07', '38', '26') and con == 'Legitimate interest + LIA':
        return False
    if role == 'R18' and dat in ('Restricted', 'Confidential'):
        return False
    if sku and aut in ('L3', 'L4'):
        if C.EFFECT[sku] in ('R2', 'R3') and sku not in C.MANDATE:
            return False
        if aut == 'L4' and C.EFFECT[sku] in ('R2', 'R3') and sku not in C.L4_OK:
            return False
    return True


P01 = collections.OrderedDict([
    ('tenant', C.TENANTS), ('plan', C.PLANS), ('sku', C.ALL_SM), ('region', C.REGIONS), ('locale', C.LOCALES),
    ('role', list(C.ROLES)), ('channel', C.CHANNELS), ('identity', C.IDENTITIES), ('device', C.DEVICES),
    ('browser', C.BROWSERS), ('data', C.DATA), ('consent', C.CONSENT), ('provider', C.PROVIDER),
    ('autonomy', C.AUTONOMY), ('ai_route', C.AI_ROUTE), ('sla', C.SLA)])

PROV_TXT = {'Available': 'provider accepts; run Completed',
            'Throttled (429)': '429 handled by exponential backoff with jitter (≤ 3 retries, NFR-016); exactly one effect (NFR-005)',
            'Timeout after submit': 'outcome Uncertain → Reconciling; no retry before the provider is queried by idempotency key (NFR-026, FR-STD-02); at most one effect',
            'Down before submit': '≤ 3 retries with backoff, then exception queue and task to the owner; run Held; no effect'}
DEV_TXT = {'Desktop 1440': '1440 px', 'Laptop 1280': '1280 px', 'Tablet 768': '768 px', 'Mobile 390': '390 px', 'Mobile 320': '320 CSS px (reflow, WCAG 1.4.10)'}


def sku_label(s):
    return 'SM-SVC-%s %s' % (s, C.SM[('SM-SVC-' + s)]['name'].replace(' Automation', ''))


def o01(r):
    sku, role, t, reg = r['sku'], r['role'], r['tenant'], r['region']
    eff = C.EFFECT[sku]
    parts = []
    meter = C.SM['SM-SVC-' + sku]['meter']
    if r['plan'] == 'TRIAL':
        parts.append('Entitlement: trial plan → run in simulation; 0 provider calls; 0 ledger or budget consumption (BRL-AUT-04); meter `%s` recorded as trial' % meter)
    elif role == 'R17':
        parts.append('Purchase on W-checkout creates the %s entitlement for SM-SVC-%s; invoice and meter schedule created; tenant activation follows onboarding' % (C.PLAN_TEXT[r['plan']], sku))
    else:
        parts.append('Entitlement passes (%s); meter `%s` +1 in the %s meter ledger' % (C.PLAN_TEXT[r['plan']], meter, reg))
    parts.append('%s %s via %s (%s)' % (role, C.ROLE_ACTION[role], r['channel'], r['identity']))
    if role == 'R21':
        parts.append('every action stamped with `grant_id`; no export; no approval of client claims, budgets or autonomy (ABAC-ENH-A-01…03)')
    if role in ('R13',):
        parts.append('business content only through the grant; grant expiry ends the session view')
    if role in ('R14', 'R15'):
        parts.append('any mutation attempt returns 403 with NSE')
    parts.append('all rows, files, cache keys, logs and the audit event written in the %s zone; Vercel function and model call pinned to %s (CJ-TC-09)' % (reg, reg))
    loc = r['locale']
    if r['channel'] in C.UI_CHANNELS:
        d = 'rtl, mirrored layout' if loc == 'ar-AE' else 'ltr'
        parts.append('UI in %s (dir=%s; CLDR %s dates, numbers, currency)' % (loc, d, loc))
    else:
        parts.append('problem details and generated text localized by `Accept-Language: %s`' % loc)
    air, dat = r['ai_route'], r['data']
    if sku in C.AI_SKUS or role == 'R20':
        if air.startswith('Tier 2'):
            parts.append('AI step on Tier 2 only because data class is %s, the tenant opt-in flag is on and the AU-004 personal-data check is clean' % dat)
        elif air.startswith('Open-weight'):
            parts.append('masking (AU-004) applied before the in-zone open-weight model; un-masking only in the %s zone' % reg)
        elif air.startswith('Tier 3'):
            parts.append('no model call; rules/cache output labelled "degraded"; human review task')
        else:
            parts.append('AI step through the registry row "%s" (approved, DPA no-training, %s processing)' % (air, reg))
    else:
        parts.append('no AI step in this SKU path; registry row not used')
    if dat in ('Personal', 'Restricted', 'Confidential') and r['consent'] != 'Not applicable':
        parts.append('lawful basis "%s" verified by the PDP at dispatch' % r['consent'])
    if t == 'T1-MedMaarg':
        parts.append('health-data classifier passes (no patient data)')
    if t == 'T1-EduVerse' and dat in ('Personal', 'Restricted'):
        parts.append('age-band check: recipient is an adult or institution, never a minor (DEC-030)')
    aut = r['autonomy']
    if aut == 'L0':
        parts.append('L0: the human records the manual action with evidence; no system dispatch')
    elif aut == 'L1':
        parts.append('L1: AI draft created; no external effect until the human acts')
    elif aut == 'L2':
        parts.append('L2: one dispatch of the exact approved payload hash; a replay returns the first result')
    elif aut in ('L3', 'L4'):
        if eff in ('R0', 'R1'):
            parts.append('%s: internal %s step runs automatically (no mandate needed)' % (aut, eff))
        else:
            parts.append('%s: dispatch under an Active %s mandate: reserve → commit in the consumption ledger, caps checked, effect visible in A263 ≤ 1 min' % (aut, C.MANDATE[sku]))
            if aut == 'L4':
                parts[-1] += '; plan step is inside the approved graph'
    if eff in ('R2', 'R3') or r['provider'] != 'Available':
        parts.append(PROV_TXT[r['provider']])
    if r['device'] != 'Headless':
        parts.append('%s on %s: no horizontal scroll, targets ≥ 24×24 CSS px, axe 0 critical/serious' % (DEV_TXT[r['device']], r['browser']))
    parts.append('SLO attribution: %s' % r['sla'])
    exp = '; '.join(parts)
    p0 = (aut in ('L3', 'L4') and eff in ('R2', 'R3')) or eff == 'R3' or dat == 'Restricted' or \
         (r['provider'] == 'Timeout after submit' and eff in ('R2', 'R3')) or air.startswith('Tier 2') or role in ('R21', 'R13')
    types = ['T01']
    if r['channel'] in C.UI_CHANNELS:
        types.append('T10')
    if r['provider'] == 'Timeout after submit':
        types.append('T18')
    elif air.startswith('Tier 2') or air.startswith('Open-weight'):
        types.append('T14')
    elif dat in ('Personal', 'Restricted'):
        types.append('T19')
    rel = C.rel_max(C.REL_SKU[sku], C.LOCALE_REL[loc], 'R2' if aut in ('L3', 'L4') else 'R1')
    lvl = 'E2E' if r['channel'] in C.UI_CHANNELS else 'SYS'
    return dict(exp=exp, P='P0' if p0 else 'P1', type=', '.join(types[:3]), lvl=lvl, rel=rel)


add_model('PM-T01', title='Platform SKU invocation (valid set)', params=P01, constraint=c01, oracle=o01,
          groups=[(list(P01), 2)], method='Pairwise (2-way), valid values only', seed=921, ncand=6,
          ts='TS-V12-T-01', links='FR-V12-B (39 SKU specifications, Part 11.2); FR-V12-I (RLS, Part 11.9b); FR-V12-R-143…155; DEC-770, 772, 779, 784–788',
          common='Pre: PP-01 per zone (IN stack in Mumbai, EU stack in Frankfurt or the EU-configured test cell); tenant fixtures from SYN-T (§11.21.2.4) matching the row; the SKU entitled per the row plan; approved policy, template and price versions; provider simulator in the row state; clock CLK-0. Steps: 1. Authenticate with the row identity on the row channel and device/browser (Playwright project for UI rows; API client for headless rows). 2. Start the SKU\'s primary workflow (WF01, or the first workflow with an effect step for R2/R3 SKUs) with the fixture FX-<wf>-v1 at the row autonomy level. 3. Drive the run to its effect step. 4. Read run, step, outbox, ledger, meter, audit and simulator logs in the row zone. 5. For UI rows run axe and the viewport checks.',
          tech='PW')


# ------------------------------------------------------------------------------- PM-T01N (single fault)
NEG01 = [
    ('plan', '~SKU not in plan', None, '403 `ENTITLEMENT_REQUIRED`; upgrade prompt on A-screen; workflow not started; NSE', 'P0', 'T07'),
    ('plan', '~Subscription suspended', None, '403 `SUBSCRIPTION_SUSPENDED`; read and export of own data still allowed; no new runs or effects; NSE', 'P0', 'T01'),
    ('region', '~UK zone not provisioned', None, '409 `RESIDENCY_ZONE_UNAVAILABLE`; fail closed; nothing written in IN or EU on behalf of the UK zone', 'P0', 'T19'),
    ('role', '~role without permission for the SKU action', None, '403 `PERMISSION_DENIED` (U404 for objects outside scope, BRL-TEN-04); NSE; denial audit event', 'P0', 'T07'),
    ('role', '~R21 without active delegation grant', 'EXT-MSP', '403 `DELEGATION_SCOPE` (ABAC-ENH-A-01); NSE; audit', 'P0', 'T07'),
    ('role', '~SCIM de-provisioned user', None, '401; sessions revoked ≤ 60 s after the SCIM delete (Part 11.19a); NSE', 'P0', 'T07'),
    ('identity', '~MFA older than policy for privileged action', None, '403 `STEP_UP_REQUIRED` until WebAuthn step-up (ABAC-11); NSE', 'P0', 'T07'),
    ('identity', '~revoked or expired credential', None, '401 `CREDENTIAL_REVOKED`; no partial processing; security event', 'P0', 'T07'),
    ('data', '~Prohibited (patient health data or personal data of a minor)', None, '422 `PROHIBITED_DATA_CLASS`; record quarantined; R10 task; no AI call, no dispatch (DEC-030; MedMaarg rule)', 'P0', 'T19'),
    ('consent', '~Withdrawn / opted out', None, 'PDP deny `SUPPRESSED` at dispatch; queued items Cancelled; KPI-17 stays 0', 'P0', 'T19'),
    ('consent', '~Unknown', None, 'PDP hold `ELIGIBILITY_UNKNOWN`; review task; no effect', 'P0', 'T19'),
    ('autonomy', '~L2 payload changed after approval', None, 'Block `APPROVAL_HASH_MISMATCH`; new approval required; NSE', 'P0', 'T07'),
    ('autonomy', '~L2 approval expired', None, 'Block `APPROVAL_EXPIRED`; NSE', 'P0', 'T07'),
    ('autonomy', '~L3 mandate Suspended', None, 'Block `MANDATE_NOT_ACTIVE`; reservation released; NSE', 'P0', 'T19'),
    ('autonomy', '~L3 mandate Revoked', None, 'Block `MANDATE_NOT_ACTIVE`; in-flight held; reconciliation task; NSE', 'P0', 'T19'),
    ('autonomy', '~L3 requested for a workflow outside the eligibility register', None, 'Mandate rejected at submit `MANDATE_TYPE_NOT_ELIGIBLE`; workflow stays ≤ L2 (FR-V12-P-013)', 'P0', 'T19'),
    ('autonomy', '~kill switch engaged (tenant)', None, 'Block `KILL_SWITCH_ENGAGED`; reservations released; NSE', 'P0', 'T19'),
    ('ai_route', '~Tier 2 requested with personal data', None, 'Gateway refuses Tier 2 (DEC-007/788); routes to the approved primary or Tier 3; 0 calls to the free provider', 'P0', 'T14'),
    ('ai_route', '~unapproved registry candidate', None, 'Route refused `MODEL_NOT_APPROVED`; approved primary used; registry audit', 'P0', 'T14'),
    ('provider', '~live provider key outside prod', None, 'Start-up fails `ENV_GUARD` (ABAC-12); no outbound call', 'P0', 'T07'),
    ('browser', '~unsupported legacy browser', None, 'Upgrade notice; read paths usable; no data loss; no mutation submitted with a broken form', 'P2', 'T10'),
    ('locale', '~unsupported locale (xx-YY)', None, 'Fallback to the tenant default locale with notice; no mixed-direction layout', 'P2', 'T13'),
    ('channel', '~Admin route on the public origin', None, '404 (NFR-001 separate origins and route allowlists); no Admin bundle served', 'P0', 'T07'),
]


def build_neg01():
    rows = []
    for k, (p, v, need_t, exp, P, typ) in enumerate(NEG01):
        params = collections.OrderedDict((n, list(vals)) for n, vals in P01.items())
        params[p] = [v]
        if need_t:
            params['tenant'] = [need_t]
        if p == 'role':
            params['role'] = [v]
        # applicability: denial must be observable in the row
        def cons(r, p=p, v=v):
            if not c01(r, skip=(p,)):
                return False
            if p == 'consent' and r.get('data') in ('Public', 'Internal'):
                return False
            if p in ('consent', 'autonomy') and r.get('sku') and C.EFFECT[r['sku']] not in ('R2', 'R3'):
                return False
            if p == 'autonomy' and 'L3' in v and r.get('sku') and 'eligibility' not in v and r['sku'] not in C.MANDATE:
                return False
            if p == 'autonomy' and 'eligibility' in v and r.get('sku') and (r['sku'] in C.MANDATE or C.EFFECT[r['sku']] in ('R0', 'R1')):
                return False
            if p == 'ai_route' and r.get('sku') and r['sku'] not in C.AI_SKUS:
                return False
            if p == 'ai_route' and 'personal' in v and r.get('data') not in ('Personal', 'Restricted', None):
                return False
            if p == 'browser' and r.get('device') == 'Headless':
                return False
            if p == 'channel' and r.get('role') and r['role'] not in C.ADMIN_ROLES:
                return False
            if p == 'identity' and 'MFA' in v and r.get('role') not in ('R01', 'R02', 'R08', 'R09', 'R10', 'R12', None):
                return False
            if p == 'identity' and 'MFA' in v and r.get('identity') is not None and False:
                return False
            return True
        if p == 'identity':
            params['role'] = ['R01', 'R02', 'R08', 'R09', 'R10', 'R12'] if 'MFA' in v else list(C.ROLES)
        if p == 'channel':
            params['device'] = ['Desktop 1440', 'Laptop 1280']
        groups = [([p, 'tenant'], 2), ([p, 'region'], 2)]
        rs, req = generate(params, cons, groups, seed=930 + k, ncand=4)
        ver = verify(params, cons, groups, rs)
        for r in rs:
            rows.append(dict(row=r, neg=(p, v), exp=exp, P=P, type=typ, ver=ver))
    return rows


# =============================================================================================
# PM-T02 Investment Automation SKU invocation
# =============================================================================================
INV_SKUS = ['%02d' % i for i in range(1, 25)]
INV_ROLE = collections.OrderedDict([
    ('R01', INV_SKUS), ('R03', ['01', '02', '03', '04', '05', '06', '07', '08', '15', '16', '17', '19', '21']),
    ('R08', ['09', '12', '14', '18', '19', '20']), ('R09', ['09', '12', '14', '18', '19', '20']),
    ('R10', ['10', '11', '13', '21', '22', '23', '24']), ('R12', INV_SKUS), ('R15', INV_SKUS),
    ('R16', ['08', '10', '11', '13', '14', '16', '23', '24']), ('R18', ['16']), ('R19', INV_SKUS)])
INV_CH = {r: ['Admin web', 'Admin mobile web'] for r in ('R01', 'R03', 'R08', 'R09', 'R10', 'R12', 'R15')}
INV_CH.update({'R16': ['Portal'], 'R18': ['Public website'], 'R19': ['Developer API', 'Event/webhook']})
INV_LOC = {'IN': ['en-IN', 'hi-IN', 'ar-AE'], 'EU': ['en-GB', 'de-DE', 'fr-FR', 'ar-AE']}
PACK = {'IN': 'RP-IN-SEC + RP-AML-KYC', 'US': 'RP-US-REGD / RP-US-REGCF + RP-AML-KYC', 'EU': 'RP-EU-PROSP + RP-AML-KYC',
        'UK': 'RP-UK-FINPROM + RP-AML-KYC'}
OFFER_SKUS = {'09', '11', '13'}
P02 = collections.OrderedDict([
    ('sku', INV_SKUS), ('region', C.REGIONS), ('investor_jurisdiction', ['IN', 'US', 'EU', 'UK']),
    ('locale', ['en-IN', 'hi-IN', 'en-GB', 'de-DE', 'fr-FR', 'ar-AE']), ('role', list(INV_ROLE)),
    ('channel', ['Admin web', 'Admin mobile web', 'Portal', 'Public website', 'Developer API', 'Event/webhook']),
    ('device', C.DEVICES), ('browser', C.BROWSERS),
    ('data', ['Public', 'Personal', 'Confidential-Financial', 'Restricted (KYC)']),
    ('investor_status', ['verified eligible', 'not applicable (no offer content)'])])


def c02(r, skip=()):
    g = lambda k: None if (k in skip or neg(r.get(k))) else r.get(k)  # noqa: E731
    sku, reg, loc, role, ch, dev, brw, dat, st = (g('sku'), g('region'), g('locale'), g('role'), g('channel'), g('device'),
                                                   g('browser'), g('data'), g('investor_status'))
    if reg and loc and loc not in INV_LOC[reg]:
        return False
    if role and sku and sku not in INV_ROLE[role]:
        return False
    if role and ch and ch not in INV_CH[role]:
        return False
    if ch and dev and dev not in CH_DEV[ch]:
        return False
    if dev and brw and ((dev == 'Headless') != (brw == 'Headless')):
        return False
    if dat == 'Restricted (KYC)' and sku and sku not in ('10', '12', '13', '22', '24'):
        return False
    if role == 'R18' and dat in ('Restricted (KYC)', 'Confidential-Financial'):
        return False
    if sku in OFFER_SKUS and role == 'R16' and st and st != 'verified eligible':
        return False
    return True


def o02(r):
    sku, reg, jur, role = r['sku'], r['region'], r['investor_jurisdiction'], r['role']
    name = C.INV['INV-SVC-' + sku]['name'].replace(' Automation', '')
    parts = ['INV-SVC-%s %s: %s via %s' % (sku, name, {'R16': 'investor completes the portal step on own records',
                                                       'R18': 'visitor submits the private enquiry (no offer content)',
                                                       'R19': 'integration calls the API / delivers the signed event',
                                                       'R15': 'auditor reads evidence (read-only)',
                                                       'R12': 'tenant admin configures entitlement and templates'}.get(role, 'issuer staff ' + C.ROLE_ACTION[role]), r['channel'])]
    parts.append('jurisdiction pack %s Approved for %s; strictest-wins precedence (Part 11.15 §11.15.3.3)' % (PACK[jur], jur))
    if sku in OFFER_SKUS:
        if r['investor_status'] == 'verified eligible':
            parts.append('offer terms rendered only to the verified-eligible investor; legends of the %s pack shown; two-person approval hash bound' % jur)
        else:
            parts.append('issuer-side preparation only; no offer terms leave the data room until an eligible recipient is verified')
    else:
        parts.append('non-offer content only; no general solicitation unless the %s pack route permits it' % jur)
    parts.append('no personalised investment advice (RP-INV-ADVICE; AG-199 guard): output is neutral and factual')
    if r['data'] == 'Restricted (KYC)':
        parts.append('KYC evidence stored in the %s zone, viewer watermark, never sent by email or WhatsApp' % reg)
    elif r['data'] == 'Confidential-Financial':
        parts.append('financial figures delivered only through the portal or data room (CLASS_PORTAL_ONLY)')
    parts.append('records and audit in the %s zone' % reg)
    if r['device'] != 'Headless':
        d = 'rtl' if r['locale'] == 'ar-AE' else 'ltr'
        parts.append('%s, dir=%s, %s on %s: axe 0 critical/serious' % (r['locale'], d, DEV_TXT[r['device']], r['browser']))
    p0 = sku in OFFER_SKUS or r['data'] in ('Restricted (KYC)', 'Confidential-Financial') or sku in ('12', '20', '22', '23', '24')
    rel = C.rel_max('R2', C.LOCALE_REL[r['locale']])
    return dict(exp='; '.join(parts), P='P0' if p0 else 'P1', type='T01, T19' if p0 else 'T01',
                lvl='E2E' if r['channel'] in C.UI_CHANNELS else 'SYS', rel=rel)


add_model('PM-T02', title='Investment Automation SKU invocation (valid set)', params=P02, constraint=c02, oracle=o02,
          groups=[(list(P02), 2)], method='Pairwise (2-way), valid values only', seed=922, ncand=8, ts='TS-V12-T-02',
          links='FR-V12-N / FR-V12-O (Parts 11.16a–e); INV-SVC-01…24; RP-IN-SEC, RP-US-REGD, RP-US-REGCF, RP-EU-PROSP, RP-UK-FINPROM, RP-AML-KYC, RP-INV-ADVICE; DEC-783',
          common='Pre: PP-01 per zone; Investment Automation tenant "Lumen Robotics Pvt Ltd" (IN) or "Lumen Robotics GmbH" (EU) on the INV plan; securities packs of the row jurisdiction Approved (synthetic approval in test, counsel-signed in production); investor fixtures with KYC state per row. Steps: 1. Authenticate as the row role on the row channel. 2. Run the SKU\'s first workflow with FX-INV-<sku>-v1. 3. Read rendered content, outbox, data-room access log, audit and simulator logs in the zone.',
          tech='PW')

NEG02 = [
    ('investor_jurisdiction', '~SG (no Approved pack)', 'Block `JURISDICTION_NOT_ENABLED`; investor-facing step not started; issuer told which pack is missing', 'P0'),
    ('investor_jurisdiction', '~AE (no Approved pack)', 'Block `JURISDICTION_NOT_ENABLED`', 'P0'),
    ('investor_status', '~self-certified only (verification required by route)', 'Hold `VERIFICATION_REQUIRED`; offer terms withheld; KYC/eligibility task (RP-AML-KYC; 506(c)-type routes)', 'P0'),
    ('investor_status', '~retail / unknown investor for a restricted route', 'Block `INVESTOR_NOT_ELIGIBLE`; non-offer content only; no solicitation', 'P0'),
    ('data', '~AI asked "should I invest" (advice request)', 'Neutral refusal with factual information and a pointer to an adviser; no recommendation stored or sent (RP-INV-ADVICE)', 'P0'),
    ('investor_status', '~pack Draft (counsel not signed)', 'Block `PACK_NOT_APPROVED` (CJ-R19/R20); capability inactive for that jurisdiction', 'P0'),
]


def build_neg02():
    rows = []
    for k, (p, v, exp, P) in enumerate(NEG02):
        params = collections.OrderedDict((n, list(vals)) for n, vals in P02.items())
        params[p] = [v]
        if v.startswith('~AI asked'):
            params['role'] = ['R16', 'R01', 'R03']
        cons = lambda r, p=p: c02(r, skip=(p,))  # noqa: E731
        groups = [([p, 'role'], 2), ([p, 'region'], 2)]
        rs, req = generate(params, cons, groups, seed=960 + k, ncand=4)
        ver = verify(params, cons, groups, rs)
        for r in rs:
            rows.append(dict(row=r, neg=(p, v), exp=exp, P=P, type='T19', ver=ver))
    return rows


# =============================================================================================
# PM-T03 consequential-effect gateway (cross-capability PDP at dispatch)
# =============================================================================================
EFFECTS = collections.OrderedDict([
    ('E01 email outreach send', ('SM-SVC-06-WF02', 'MT-OUT', True, 'Email sent once via the zone SES identity; outbox row; Delivered by signed webhook')),
    ('E02 WhatsApp template send', ('SM-SVC-07-WF02', 'MT-OUT', True, 'Approved template sent once via WhatsApp Cloud API; signed delivery receipt')),
    ('E03 SMS/RCS send', ('SM-SVC-38-WF02', None, True, 'DLT-registered template sent once via the aggregator; DLR stored')),
    ('E04 outbound AI voice call', ('SM-SVC-26-WF02', None, True, 'Call placed; AI identifies itself as AI at the start; recording only per pack; human hand-off offered')),
    ('E05 content/page publication', ('SM-SVC-11-WF03', 'MT-PUB', False, 'Approved content version published (atomic pointer swap, hash-bound)')),
    ('E06 ad budget change', ('SM-SVC-14-WF02', 'MT-SPEND', False, 'Budget change applied once on the ad account; spend ledger updated')),
    ('E07 quote issue within discount band', ('SM-SVC-17-WF02', 'MT-COM', False, 'Quote issued at the approved price-book revision; discount ≤ band')),
    ('E08 purchase order to supplier', ('SM-SVC-39-WF03', 'MT-PROC', False, 'PO committed to the approved supplier; payable commitment posted')),
    ('E09 supplier pay-out via PSP', ('SM-SVC-39-WF03', 'MT-PAY', False, 'Pay-out instruction to the licensed PSP with idempotency key; Dr Payable / Cr PSP clearing; daily reconciliation match')),
    ('E10 receivable collection via PSP mandate', ('SM-SVC-32-WF04', 'MT-PAY', False, 'Collection through the registered PSP mandate after pre-debit notice; receivable ledger updated; reconciliation match')),
    ('E11 AI-to-AI order acceptance', ('SM-SVC-28-WF03', 'MT-COM', False, 'Order accepted from a verified counterparty agent within negotiation bounds; signed acceptance; commerce sub-ledger posting')),
    ('E12 automatic bid submission', ('SM-SVC-19-WF03', 'MT-BID', False, 'Exact approved package hash submitted to the portal; submission receipt stored; mandate count 1 → Exhausted')),
    ('E13 price experiment exposure', ('SM-SVC-37-WF03', 'MT-PRICE', False, 'Exposure switched between the two approved price-book revisions within the exposure cap')),
    ('E14 investor outreach message', ('INV-SVC-04-WF02', 'MT-OUT (INV)', True, 'Investor message sent once to a verified recipient; no offer terms unless eligible')),
    ('E15 formal securities offer issue', ('INV-SVC-11-WF02', None, True, 'Offer document issued to the named eligible investor after two-person approval; legends per pack')),
])
L4_EFFECTS = {'E01 email outreach send', 'E02 WhatsApp template send', 'E11 AI-to-AI order acceptance', 'E14 investor outreach message'}
AUTH_POS = ['L1 human dispatch', 'L2 approved hash valid', 'L3 mandate Active', 'L4 step in approved plan graph']
AUTH_NEG = ['L2 payload changed', 'L2 approval expired', 'L3 mandate Suspended', 'L3 mandate Revoked', 'L3 mandate Exhausted', 'L4 step outside plan graph']
P03 = collections.OrderedDict([
    ('effect', list(EFFECTS)), ('authorization', AUTH_POS + AUTH_NEG),
    ('value', ['below per-action cap', 'exactly at cap', 'above per-action cap', 'crosses aggregate cap']),
    ('pack', ['IN pack Approved', 'EU pack Approved', 'pack Draft', 'jurisdiction not enabled']),
    ('region', ['IN zone', 'EU zone']), ('kill_switch', ['off', 'tenant scope', 'platform scope']),
    ('consent', ['valid basis', 'withdrawn', 'unknown', 'registry/DND-listed']),
    ('data', ['Public/Internal', 'Personal', 'Restricted'])])
POS03 = dict(authorization=AUTH_POS, value=['below per-action cap', 'exactly at cap'], pack=['IN pack Approved', 'EU pack Approved'],
             kill_switch=['off'], consent=['valid basis'], data=['Public/Internal', 'Personal'])


def c03(r):
    return True


def o03(r):
    e, a, val, pk, reg, ks, con, dat = (r['effect'], r['authorization'], r['value'], r['pack'], r['region'], r['kill_switch'],
                                        r['consent'], r['data'])
    wf, mt, personal, allow = EFFECTS[e]
    zone = reg.split()[0]
    tail = '; audit and evidence in the %s zone; NSE' % zone
    lvl = a.split()[0]
    if ks != 'off':
        return 'BLOCK `KILL_SWITCH_ENGAGED` (%s); reservation released; plan Paused if L4' % ks + tail, 'BLOCK'
    if pk == 'jurisdiction not enabled':
        return 'BLOCK `JURISDICTION_NOT_ENABLED`' + tail, 'BLOCK'
    if pk == 'pack Draft':
        return 'BLOCK `PACK_NOT_APPROVED` (CJ-R19/R20: Draft never enforced as Approved)' + tail, 'BLOCK'
    if lvl in ('L3', 'L4') and mt is None:
        return 'BLOCK `MANDATE_TYPE_NOT_ELIGIBLE`: %s has no mandate path (eligibility register; per-item approval only)' % wf + tail, 'BLOCK'
    if lvl == 'L4' and e not in L4_EFFECTS:
        return 'BLOCK `LEVEL_ABOVE_MAX`: %s maximum is L3' % mt + tail, 'BLOCK'
    if a == 'L2 payload changed':
        return 'BLOCK `APPROVAL_HASH_MISMATCH`; new approval required' + tail, 'BLOCK'
    if a == 'L2 approval expired':
        return 'BLOCK `APPROVAL_EXPIRED`' + tail, 'BLOCK'
    if a in ('L3 mandate Suspended', 'L3 mandate Revoked'):
        return 'BLOCK `MANDATE_NOT_ACTIVE`; in-flight items held for reconciliation' + tail, 'BLOCK'
    if a == 'L3 mandate Exhausted':
        return 'BLOCK `MANDATE_EXHAUSTED`; renewal needs a new two-person approval' + tail, 'BLOCK'
    if a == 'L4 step outside plan graph':
        return 'BLOCK `PLAN_STEP_NOT_IN_GRAPH`; plan Paused; R11 and mandate owner alerted' + tail, 'BLOCK'
    if personal:
        if con == 'withdrawn':
            return 'BLOCK `SUPPRESSED`; queued items for the recipient Cancelled (KPI-17 = 0)' + tail, 'BLOCK'
        if con == 'registry/DND-listed':
            if e in ('E03 SMS/RCS send', 'E04 outbound AI voice call'):
                return 'BLOCK `REGISTRY_LISTED` (NCPR/DNC/TPS/Bloctel scrub per pack)' + tail, 'BLOCK'
            return 'BLOCK `SUPPRESSED`: registry not applicable to the channel, contact on the suppression list' + tail, 'BLOCK'
        if con == 'unknown':
            return 'HOLD `ELIGIBILITY_UNKNOWN`; review task; no effect' + tail, 'HOLD'
    if dat == 'Restricted' and e not in ('E09 supplier pay-out via PSP', 'E10 receivable collection via PSP mandate'):
        return 'BLOCK `DATA_CLASS_NOT_PERMITTED`: Restricted fields never leave in an external payload' + tail, 'BLOCK'
    if dat == 'Personal' and e == 'E05 content/page publication':
        return 'HOLD `CONSENT_EVIDENCE_REQUIRED`: personal data in public content needs the subject\'s publication consent' + tail, 'HOLD'
    if e == 'E12 automatic bid submission' and val != 'exactly at cap':
        return 'BLOCK `BID_PACKAGE_MISMATCH`: price/package differs from the approved hash (only the exact approved package may be submitted)' + tail, 'BLOCK'
    if val == 'above per-action cap':
        if lvl in ('L3', 'L4'):
            return 'BLOCK `CAP_PER_ACTION`; anomaly rule AU-267 evaluated' + tail, 'BLOCK'
        return 'HOLD `ESCALATE_APPROVER`: value above the DEC-038 threshold of the approver; higher approver required' + tail, 'HOLD'
    if val == 'crosses aggregate cap':
        if lvl in ('L3', 'L4'):
            return 'BLOCK `CAP_AGGREGATE`; reservation refused; nothing committed' + tail, 'BLOCK'
        return 'HOLD `BUDGET_EXCEEDED`: reservation refused before any provider call (NFR-014)' + tail, 'HOLD'
    how = {'L1': 'human action dispatches after the full PDP recheck', 'L2': 'system dispatches the exact approved hash once',
           'L3': 'dispatch under the Active %s mandate: reserve → commit; caps, counterparty and window rechecked' % mt,
           'L4': 'plan step inside the approved graph; plan budget ≤ mandate remaining; reserve → commit'}[lvl]
    extra = ''
    if e == 'E04 outbound AI voice call':
        extra = '; 09:00–21:00 recipient local window or stricter pack (DEC-777)'
    if e == 'E15 formal securities offer issue':
        extra = '; recipient verified eligible; no public offer'
    at = ' (cap inclusive)' if val == 'exactly at cap' and e != 'E12 automatic bid submission' else ''
    return 'ALLOW: %s%s; %s%s; idempotency key prevents a second effect; audit and evidence in the %s zone' % (allow, at, how, extra, zone), 'ALLOW'


def o03w(r):
    exp, verdict = o03(r)
    e = r['effect']
    money = e[:3] in ('E06', 'E07', 'E08', 'E09', 'E10', 'E11', 'E12', 'E13')
    typ = 'T19, T20' if money else 'T19, T07'
    if r['effect'][:3] in ('E01', 'E02', 'E03', 'E04', 'E05', 'E06'):
        rel = 'R1' if r['authorization'].split()[0] in ('L1', 'L2') and e[:3] in ('E01', 'E02', 'E05', 'E06') else 'R2'
    else:
        rel = 'R2'
    return dict(exp=exp, P='P0', type=typ, lvl='SYS', rel=rel, verdict=verdict)


CTRL = ['authorization', 'value', 'pack', 'region', 'kill_switch', 'consent', 'data']
add_model('PM-T03', title='Consequential-effect gateway: full space (layer L1)', params=P03, constraint=c03, oracle=o03w,
          groups=[(CTRL, 3)] + [(['effect', c], 2) for c in CTRL], method='Variable strength: 3-way among the 7 control parameters + 2-way effect × each control',
          seed=923, ncand=10, ts='TS-V12-T-03',
          links='FR-V12-P-001…069 (mandate engine), FR-V12-P-070…099 (commerce and payments), FR-V12-P bids (Part 11.17b), FR-V12-Q (voice), FR-V12-N/O (investor); §11.17.5.12 PDP order; DEC-779…783',
          common='Pre: PP-01 in the row zone; mandate, approval, pack, kill-switch, consent and data-class fixtures seeded per row through the test-only seeding API (never in production); provider simulators for SES, WhatsApp, DLT aggregator, CPaaS, CMS, ad platform, PSP (UPI/e-NACH in IN, SEPA in EU), counterparty agent and tender portal. Steps: 1. Seed the row state. 2. Release the effect step of the named workflow through the dispatcher. 3. Read the PDP decision log (rule order of §11.17.5.12), outbox, consumption ledger, provider simulator log, reconciliation queue and audit in the zone.',
          tech='PW3 (VS)')


def c03pos(r):
    return True


P03P = collections.OrderedDict((k, POS03.get(k, v)) for k, v in P03.items())
add_model('PM-T03P', title='Consequential-effect gateway: positive sub-space (layer L2)', params=P03P, constraint=c03pos, oracle=o03w,
          groups=[(list(P03P), 3)], method='3-way over the gate-passing values (deep paths unmasked)', seed=924, ncand=8,
          ts='TS-V12-T-03', links=MODELS['PM-T03']['links'], common=MODELS['PM-T03']['common'], tech='PW3')


def build_neg03():
    rows = []
    invalid = [(p, v) for p, vals in P03.items() if p in POS03 for v in vals if v not in POS03[p]]
    i = 0
    for p, v in invalid:
        for e in EFFECTS:
            personal = EFFECTS[e][2]
            r = collections.OrderedDict()
            r['effect'] = e
            r['authorization'] = 'L2 approved hash valid'
            r['value'] = 'exactly at cap' if e.startswith('E12') else ['below per-action cap', 'exactly at cap'][i % 2]
            r['pack'] = ['IN pack Approved', 'EU pack Approved'][i % 2]
            r['region'] = ['IN zone', 'EU zone'][(i // 2) % 2]
            r['kill_switch'] = 'off'
            r['consent'] = 'valid basis'
            r['data'] = 'Personal' if (personal and i % 3 == 0) else 'Public/Internal'
            r[p] = v
            rows.append(dict(row=r, neg=(p, v)))
            i += 1
    return rows


# =============================================================================================
# PM-T04 data residency
# =============================================================================================
COMP = ['Postgres (Supabase)', 'Object storage (S3)', 'Valkey cache/queue', 'Vector index (pgvector)', 'Model inference call',
        'Vercel function', 'Email/SMS/voice provider processing', 'Call recordings and transcripts', 'Logs and traces',
        'Audit / SIEM export', 'Backup and WAL archive', 'DR standby / secondary copy']
P04 = collections.OrderedDict([
    ('tenant_zone', ['IN', 'EU']), ('component', COMP),
    ('operation', ['write', 'read', 'replicate/backup', 'restore', 'export (DSAR/portability)']),
    ('actor', ['user in the same zone', 'user travelling in the other zone', 'platform operator in the other zone (JIT)']),
    ('data', ['Internal', 'Personal', 'Restricted'])])
REPL = {'Postgres (Supabase)', 'Object storage (S3)', 'Backup and WAL archive', 'DR standby / secondary copy', 'Logs and traces', 'Call recordings and transcripts', 'Vector index (pgvector)'}
RESTORE = {'Postgres (Supabase)', 'Object storage (S3)', 'Backup and WAL archive', 'DR standby / secondary copy', 'Vector index (pgvector)'}
EXPORT = {'Postgres (Supabase)', 'Object storage (S3)', 'Call recordings and transcripts', 'Audit / SIEM export', 'Logs and traces'}


def c04(r):
    c, op = r.get('component'), r.get('operation')
    if c and op:
        if op == 'replicate/backup' and c not in REPL:
            return False
        if op == 'restore' and c not in RESTORE:
            return False
        if op.startswith('export') and c not in EXPORT:
            return False
    if c == 'Model inference call' and r.get('data') == 'Restricted' and False:
        return False
    return True


def o04(r):
    z, c, op, act, dat = r['tenant_zone'], r['component'], r['operation'], r['actor'], r['data']
    other = 'EU' if z == 'IN' else 'IN'
    sec = {'IN': 'in-zone secondary region (e.g. Hyderabad; verify)', 'EU': 'in-zone secondary EU region (verify)'}[z]
    s = []
    if op == 'write':
        s.append('%s write lands only in the %s zone' % (c, z))
    elif op == 'read':
        s.append('read served by the %s stack' % z)
    elif op == 'replicate/backup':
        s.append('replica/backup target stays inside the %s residency zone (%s); no %s copy (DEC-772, DEC-787)' % (z, sec, other))
    elif op == 'restore':
        s.append('restore target created in the %s zone only; RPO ≤ 15 min, RTO ≤ 120 min measured' % z)
    else:
        s.append('export generated in the %s zone; signed URL served from the %s bucket; expiry ≤ 24 h' % (z, z))
    if act.startswith('user travelling'):
        s.append('request from the %s geography is routed by the edge to the %s-pinned Vercel function; nothing cached or persisted in %s' % (other, z, other))
    elif act.startswith('platform operator'):
        s.append('operator access only through a JIT grant via the in-zone bastion/session; Restricted values masked; grant and every query audited in %s' % z)
    if c == 'Model inference call':
        s.append('registry row with %s processing only; Restricted minimized, never to Tier 2' % z)
    if c == 'Logs and traces' or c == 'Vercel function':
        s.append('no request/response body logging; header allowlist (DEC-786)')
    if c == 'Email/SMS/voice provider processing':
        s.append('provider account/region configured for %s; DPA lists the processing location (verify)' % z)
    s.append('residency probe CJ-TC-09 finds 0 %s-tenant rows/objects/keys in the %s zone' % (z, other))
    p = 'P0'
    rel = 'R1'
    if c == 'Call recordings and transcripts':
        rel = 'R2'
    return dict(exp='; '.join(s), P=p, type='T19, T15', lvl='SYS', rel=rel)


add_model('PM-T04', title='Data residency (India and EU) across components and operations', params=P04, constraint=c04, oracle=o04,
          groups=[(list(P04), 3)], method='3-way', seed=925, ncand=10, ts='TS-V12-T-04',
          links='DEC-772, DEC-776, DEC-786, DEC-787; CJ-TC-09 (both directions); FR-V12-R-056…095 (Vercel path, recovery); ENT-DAT-02/03',
          common='Pre: both zone stacks (or the EU-configured test cell) with tenants "Kestrel Analytics" (IN) and "Nordlicht GmbH" (EU); residency probe AU-296/CJ-TC-09 scanner with read access to every store in both zones; operator account with JIT workflow. Steps: 1. Perform the row operation on the row component as the row actor. 2. Run the residency probe across all stores of the other zone (DB, buckets, cache keys, index, logs, SIEM, backups). 3. Inspect provider/region metadata and the audit trail.',
          tech='PW3')

# =============================================================================================
# PM-T05 multi-tenant isolation and RLS
# =============================================================================================
CALLERS = ['T1 AppNAI R03 (assigned)', 'T1 MedMaarg R03', 'T1 R01 Founder', 'Tenant X R12 admin', 'Tenant Y R03',
           'R21 operator with grant to X (Outreach)', 'R13 support with JIT read grant to X']
TARGETS = ['object of X company X1', 'object of X company X2 (caller not member)', 'object of T1 AppNAI',
           'object of T1 MedMaarg', 'T1 portfolio aggregate']
PATHS = ['Admin BFF API', 'Developer API key of X', 'Search', 'Export / report', 'AI retrieval (RAG context)',
         'Outbound webhook payload', 'Notification / digest', 'Benchmark API', 'Supabase Data API (PostgREST)']
P05 = collections.OrderedDict([('caller', CALLERS), ('target', TARGETS), ('operation', ['read', 'list/count', 'update', 'delete']),
                               ('path', PATHS)])


def c05(r):
    if r.get('path') == 'Developer API key of X' and r.get('caller') and not r['caller'].startswith(('Tenant X', 'R21')):
        return False
    return True


def allowed05(caller, target, op, path):
    if path == 'Supabase Data API (PostgREST)':
        return False, '404: Data API disabled for application schemas (DEC-778)'
    if path == 'Benchmark API':
        return False, 'U404 for object-level access; only noised cohort aggregates (≥ 10 tenants) exist (DEC-789)'
    mem = {'T1 AppNAI R03 (assigned)': {'object of T1 AppNAI'}, 'T1 MedMaarg R03': {'object of T1 MedMaarg'},
           'T1 R01 Founder': {'object of T1 AppNAI', 'object of T1 MedMaarg', 'T1 portfolio aggregate'},
           'Tenant X R12 admin': {'object of X company X1', 'object of X company X2 (caller not member)'},
           'Tenant Y R03': set(), 'R21 operator with grant to X (Outreach)': {'object of X company X1'},
           'R13 support with JIT read grant to X': {'object of X company X1'}}[caller]
    if target not in mem:
        return False, 'U404 (existence not revealed; same size and timing as not-found)'
    if target == 'T1 portfolio aggregate' and op in ('update', 'delete'):
        return False, '403 `AGGREGATE_READ_ONLY` (mutation per selected startup only, BRL-TEN-05)'
    if caller.startswith('R13') and op in ('update', 'delete'):
        return False, '403 `GRANT_READ_ONLY`'
    if caller.startswith('R21') and op == 'delete':
        return False, '403 `DELEGATION_SCOPE` (R21 cannot delete client records)'
    if caller.startswith('R21') and path == 'Export / report':
        return False, '403 `DELEGATION_SCOPE` (R21 cannot export)'
    if caller == 'Tenant X R12 admin' and op in ('update', 'delete') and path not in ('Admin BFF API', 'Developer API key of X'):
        return False, '405/403: path is read-only'
    if path in ('Search', 'AI retrieval (RAG context)', 'Notification / digest', 'Outbound webhook payload') and op in ('update', 'delete'):
        return False, '405: path is read-only'
    return True, 'allowed'


def o05(r):
    ok, why = allowed05(r['caller'], r['target'], r['operation'], r['path'])
    if ok:
        exp = 'Allowed: %s by %s through %s; RLS context `app.tenant_id`/`app.company_ids` set per transaction (role `app_rw`); result contains only permitted rows; audit event' % (
            r['operation'], r['caller'], r['path'])
        if r['caller'].startswith('R13'):
            exp += '; grant ID stamped; Restricted fields masked'
        if r['caller'].startswith('R21'):
            exp += '; `grant_id` stamped; modules limited to Outreach'
        if r['path'] == 'Outbound webhook payload':
            exp += '; payload carries references and digests only, never Restricted fields'
    else:
        exp = 'Denied: %s; NSE; denial audit event; no row of the target appears in logs, search snippets, embeddings, counts or webhook bodies' % why
    return dict(exp=exp, P='P0', type='T15, T07', lvl='IT' if r['path'] == 'Supabase Data API (PostgREST)' else 'SYS', rel='R1')


add_model('PM-T05', title='Multi-tenant isolation and RLS across access paths', params=P05, constraint=c05, oracle=o05,
          groups=[(['caller', 'target', 'operation'], 3), (['path', 'caller'], 2), (['path', 'target'], 2), (['path', 'operation'], 2)],
          method='Variable strength: 3-way caller × target × operation + 2-way path × each', seed=926, ncand=10, ts='TS-V12-T-05',
          links='NFR-001, NFR-002, NFR-031, NFR-032; BRL-TEN-03/04/05; ABAC-01/02/09; ABAC-ENH-A-01…03; DEC-778, DEC-789; AP-10; KPI-30',
          common='Pre: PP-05 (real PostgreSQL with RLS, role `app_rw`, never `service_role`) and PP-01; tenants X (companies X1, X2) and Y plus T1 (AppNAI, MedMaarg) from SYN-T; R21 grant G-1 to X (Outreach); R13 JIT read grant to X valid 1 h. Steps: 1. Authenticate as the caller. 2. Perform the operation on the target through the path. 3. Assert response, body, headers, timing class, side effects, search/embedding/webhook/notification contents and audit.',
          tech='PW3 (VS)')

# =============================================================================================
# PM-T06 localization and RTL
# =============================================================================================
L06 = ['en-IN', 'hi-IN', 'ta-IN', 'or-IN', 'bn-IN', 'en-GB', 'de-DE', 'fr-FR', 'ar-AE', 'en-US']
SURF = ['Website page', 'Admin screen', 'Portal screen', 'Email template', 'WhatsApp/SMS template', 'Voice prompt (TTS/ASR)',
        'PDF quote/invoice', 'In-app notification', 'Developer portal docs', 'API problem details']
FMT = ['date/time with zone', 'number grouping', 'currency amount', 'ICU plural/gender', 'name and address', 'sorting/collation', 'bidi mixed text']
P06 = collections.OrderedDict([('locale', L06), ('surface', SURF), ('format', FMT), ('expansion', ['baseline', '+35% pseudo', '+100% long words']),
                               ('device', ['Desktop 1440', 'Tablet 768', 'Mobile 390', 'Headless'])])
CUR = {'en-IN': 'INR ₹1,23,45,678.50 (Indian grouping)', 'hi-IN': '₹1,23,45,678.50 with Devanagari text, Latin digits by default (verify CLDR)',
       'ta-IN': '₹1,23,45,678.50, Tamil text', 'or-IN': '₹1,23,45,678.50, Odia text', 'bn-IN': '₹1,23,45,678.50, Bengali text',
       'en-GB': '£12,345,678.50', 'de-DE': '12.345.678,50 €', 'fr-FR': '12 345 678,50 € (narrow no-break space)',
       'ar-AE': 'AED amount with CLDR ar-AE digits and RTL placement (verify numbering system)', 'en-US': '$12,345,678.50'}


def c06(r):
    s, d = r.get('surface'), r.get('device')
    if s and d:
        if s in ('API problem details', 'Voice prompt (TTS/ASR)', 'Email template', 'WhatsApp/SMS template', 'PDF quote/invoice') and d != 'Headless':
            return False
        if s not in ('API problem details', 'Voice prompt (TTS/ASR)', 'Email template', 'WhatsApp/SMS template', 'PDF quote/invoice') and d == 'Headless':
            return False
    return True


def o06(r):
    loc, s, f, x, d = r['locale'], r['surface'], r['format'], r['expansion'], r['device']
    rtl = loc == 'ar-AE'
    out = ['%s rendered in %s (dir=%s%s)' % (s, loc, 'rtl' if rtl else 'ltr', ', icons and progress mirrored, numbers and IDs isolated with bidi marks' if rtl else '')]
    fm = {'date/time with zone': 'dates per CLDR %s with the recipient zone name; stored UTC (NFR-017)' % loc,
          'number grouping': 'grouping per CLDR %s%s' % (loc, ' (lakh/crore)' if loc.endswith('-IN') else ''),
          'currency amount': 'amount shown as %s; Decimal end to end' % CUR[loc],
          'ICU plural/gender': 'ICU plural categories of %s complete (0/1/few/many/other where the language needs them); lint passes' % loc,
          'name and address': 'name order and address lines per %s template; no forced Western first/last split' % loc,
          'sorting/collation': 'lists sorted by ICU collation for %s' % loc,
          'bidi mixed text': 'Latin IDs, emails and amounts inside %s text keep correct order (FSI/PDI isolation)' % loc}[f]
    out.append(fm)
    if x != 'baseline':
        out.append('%s text: no truncation of meaning, no overlap, wrapping instead of clipping; buttons grow' % x)
    if s == 'Voice prompt (TTS/ASR)':
        out.append('TTS voice and ASR model approved for %s in the registry; if not, call offers human hand-off or another language (Part 11.18 language tiers)' % loc)
    if s in ('Email template', 'WhatsApp/SMS template'):
        out.append('approved localized template version exists for %s; else send blocked `TEMPLATE_LOCALE_MISSING` (no machine translation at send time)' % loc)
    if d != 'Headless':
        out.append('layout at %s without horizontal scroll' % d)
    rel = C.LOCALE_REL[loc]
    p = 'P1' if s in ('PDF quote/invoice', 'Email template', 'WhatsApp/SMS template', 'Voice prompt (TTS/ASR)') or f == 'currency amount' else 'P2'
    return dict(exp='; '.join(out), P=p, type='T13', lvl='SYS' if d == 'Headless' else 'E2E', rel=rel)


add_model('PM-T06', title='Localization and right-to-left', params=P06, constraint=c06, oracle=o06, groups=[(list(P06), 2)],
          method='Pairwise (2-way)', seed=927, ncand=10, ts='TS-V12-T-06',
          links='DEC-026, DEC-404 as amended by DEC-776; I18N-01…11; NFR-024; Part 11.7c CONFLICT-872 resolution; ENT-GLB-02/03',
          common='Pre: PP-02/PP-06; locale bundles at the release version; pseudo-locale build; fixture tenants with the row locale as user and recipient locale. Steps: 1. Render the surface (Playwright screenshot diff for UI, rendered artefact for email/SMS/PDF, synthesized prompt and ASR round-trip for voice, JSON for API). 2. Apply the format fixture (amount 12345678.50, date 2027-03-28 01:30 UTC, names with diacritics and Indic scripts, mixed Arabic + Latin ID). 3. Compare with the CLDR/ICU oracle and the linguistic review checklist.',
          tech='PW')

# =============================================================================================
# PM-T07 accessibility
# =============================================================================================
SCREENS = ['Public pages (W)', 'SKU purchase/checkout (W)', 'Portal quote/accept', 'Admin approval queue', 'Mandate console (A260-series)',
           'Dashboards and charts', 'Data tables', 'Long forms and wizards', 'Voice/recording console', 'Investor portal and data room',
           'Developer portal', 'Modals and command palette']
AT = ['keyboard only', 'NVDA + Chrome', 'JAWS + Edge', 'VoiceOver + Safari (macOS)', 'VoiceOver (iOS)', 'TalkBack (Android)', 'voice control']
VIEW = ['1280 at 100%', '1280 at 200%', '320 CSS px (400%)', 'Tablet 768', 'Mobile 390']
P07 = collections.OrderedDict([('screen', SCREENS), ('at', AT), ('viewport', VIEW),
                               ('theme', ['light', 'dark', 'forced colors']), ('direction', ['LTR', 'RTL']),
                               ('motion', ['default', 'reduced motion'])])


def c07(r):
    a, v = r.get('at'), r.get('viewport')
    if a and v:
        if a in ('VoiceOver (iOS)', 'TalkBack (Android)') and v not in ('Tablet 768', 'Mobile 390'):
            return False
        if a in ('NVDA + Chrome', 'JAWS + Edge') and v in ('Tablet 768', 'Mobile 390'):
            return False
    if r.get('theme') == 'forced colors' and a in ('VoiceOver (iOS)', 'TalkBack (Android)', 'VoiceOver + Safari (macOS)'):
        return False
    return True


SC = {'Public pages (W)': '1.1.1, 1.4.3, 2.4.4, 2.4.11', 'SKU purchase/checkout (W)': '3.3.7 redundant entry, 3.3.8 accessible authentication, 3.3.1/3.3.3',
      'Portal quote/accept': '3.3.4 error prevention (legal/financial), 2.5.8 target size', 'Admin approval queue': '4.1.3 status messages, 2.4.11 focus not obscured',
      'Mandate console (A260-series)': '3.3.4 confirm/review before two-person approval, 1.4.11 non-text contrast of cap gauges',
      'Dashboards and charts': '1.1.1 text alternative/data table for each chart, 1.4.1 not colour alone',
      'Data tables': '1.3.1 headers and scope, 2.1.1 keyboard sort/filter', 'Long forms and wizards': '3.3.7, 2.4.6, 1.3.5 input purpose',
      'Voice/recording console': '1.2.x captions/transcript for recordings, 2.2.2 pause, 2.1.2 no keyboard trap',
      'Investor portal and data room': '1.4.10 reflow of documents, 2.4.2 titles, 3.2.6 consistent help',
      'Developer portal': '1.3.1 code blocks, 2.4.5 multiple ways', 'Modals and command palette': '2.1.2, 2.4.3 focus order, 2.4.11, 2.5.7 dragging alternative'}


def o07(r):
    s = SC[r['screen']]
    out = ['%s operable with %s at %s, %s theme, %s, %s: WCAG 2.2 AA criteria %s pass' % (
        r['screen'], r['at'], r['viewport'], r['theme'], r['direction'], r['motion'], s)]
    if r['viewport'] in ('320 CSS px (400%)', 'Mobile 390', '1280 at 200%'):
        out.append('no two-dimensional scrolling except data tables and charts (1.4.10); text spacing override safe (1.4.12)')
    if r['theme'] == 'forced colors':
        out.append('focus indicator, borders and state icons visible in forced colors')
    if r['motion'] == 'reduced motion':
        out.append('no non-essential animation; live updates still announced (2.3.3, 4.1.3)')
    if r['direction'] == 'RTL':
        out.append('reading and focus order follow RTL; mirrored chevrons; screen reader announces in order')
    out.append('axe 0 critical/serious; manual AT script steps complete without help')
    p = 'P1' if r['screen'] in ('SKU purchase/checkout (W)', 'Portal quote/accept', 'Admin approval queue', 'Mandate console (A260-series)', 'Investor portal and data room') else 'P2'
    rel = 'R4' if r['direction'] == 'RTL' else ('R2' if r['screen'] in ('Mandate console (A260-series)', 'Voice/recording console', 'Investor portal and data room') else 'R1')
    auto = 'N (AT pass)' if r['at'] not in ('keyboard only',) else 'Y'
    return dict(exp='; '.join(out), P=p, type='T08', lvl='SYS-M' if auto.startswith('N') else 'E2E', rel=rel, auto=auto)


add_model('PM-T07', title='Accessibility (WCAG 2.2 AA) across screens, assistive technology and display', params=P07, constraint=c07,
          oracle=o07, groups=[(list(P07), 2)], method='Pairwise (2-way)', seed=928, ncand=10, ts='TS-V12-T-07',
          links='RECOMMENDATION-001 (WCAG 2.2 AA); NFR-023; Part 2.5 §2.46; Part 11.7c; BRL-PUB-06',
          common='Pre: PP-06 for keyboard rows, PP-07 (manual AT pass) for screen-reader and voice-control rows; build of the nightly E2E run; fixture data with long names and RTL samples. Steps: 1. Set viewport, zoom, theme, direction and motion preference. 2. Complete the screen\'s primary task with the AT using the AT script. 3. Run axe and the 2.2-specific checks (focus not obscured, target size, dragging alternative, redundant entry, accessible authentication, consistent help).',
          tech='PW')

# =============================================================================================
# PM-T08 performance / load / soak
# =============================================================================================
P08 = collections.OrderedDict([
    ('profile', ['baseline 60 min', 'Year-2 peak', '10× pilot', 'stress to 3×', 'spike 10× burst', 'soak 24 h / 72 h']),
    ('zone', ['IN', 'EU']), ('tenant_mix', ['single tenant', '50 tenants uniform', 'noisy neighbour (1 tenant = 60%)']),
    ('workload', ['website and portal reads', 'Admin API CRUD', 'workflow engine and outbox dispatch', 'webhook ingestion',
                  'AI gateway calls', 'voice concurrent calls', 'payments and reconciliation', 'SCIM bulk and SSO logins']),
    ('cache', ['warm', 'cold']), ('sla', ['Standard', 'Business', 'Enterprise'])])
THR = {'website and portal reads': 'TTFB p95 ≤ 200 ms cached / ≤ 800 ms uncached; LCP ≤ 2.5 s (LT-02, LT-12)',
       'Admin API CRUD': 'p95 read ≤ 500 ms, write ≤ 800 ms; errors < 0.5% (LT-01)',
       'workflow engine and outbox dispatch': 'outbox lag p95 ≤ 60 s; transactional runs start ≤ 15 min (DEC-032); 0 duplicates (LT-04)',
       'webhook ingestion': 'all valid events persisted before ack; duplicates no effect; queue drains ≤ 10 min (LT-05)',
       'AI gateway calls': 'gateway overhead p95 ≤ 150 ms excluding model time; budget reservation before every call; Tier 3 under saturation (LT-V12-T-01)',
       'voice concurrent calls': 'answer ≤ 2 rings; AI turn latency p95 ≤ 1.5 s; 0 dropped recordings with consent (LT-V12-T-02)',
       'payments and reconciliation': 'PSP instruction p95 ≤ 2 s excl. PSP; reconciliation of 10,000 items ≤ 15 min; 0 duplicate pay-outs (LT-V12-T-03)',
       'SCIM bulk and SSO logins': 'SCIM 100 ops ≤ 5 s p95; SSO callback p95 ≤ 700 ms (LT-V12-T-04)'}


def c08(r):
    if r.get('workload') == 'voice concurrent calls' and r.get('profile') == 'soak 24 h / 72 h' and False:
        return False
    return True


def o08(r):
    out = ['%s in the %s zone, %s, %s cache, %s tier: %s' % (r['profile'], r['zone'], r['tenant_mix'], r['cache'], r['sla'], THR[r['workload']])]
    pr = r['profile']
    if pr == 'stress to 3×':
        out.append('graceful degradation (429/503, Tier 3); no data loss or duplicate effect; recovery to SLO ≤ 10 min after load drops (LT-08)')
    if pr == 'spike 10× burst':
        out.append('transactional work not starved by the burst; autoscaling or queueing absorbs the spike')
    if pr.startswith('soak'):
        out.append('memory growth < 10% after warm-up; no worker restarts; connection pool stable; outbox lag within target (LT-06)')
    if pr == '10× pilot':
        out.append('all DEC-018/NFR targets met without architecture change (LT-11)')
    if r['tenant_mix'].startswith('noisy'):
        out.append('per-tenant rate limits and fair queues keep the other tenants\' p95 within target')
    if r['sla'] == 'Enterprise':
        out.append('error budget consumption consistent with 99.95% monthly')
    p = 'P1'
    if r['workload'] in ('payments and reconciliation', 'workflow engine and outbox dispatch') or pr == 'stress to 3×':
        p = 'P0'
    typ = {'stress to 3×': 'T04', 'spike 10× burst': 'T06', 'soak 24 h / 72 h': 'T05'}.get(pr, 'T03')
    rel = 'R2' if r['workload'] in ('voice concurrent calls', 'payments and reconciliation') else 'R1'
    return dict(exp='; '.join(out), P=p, type=typ, lvl='SYS', rel=rel)


add_model('PM-T08', title='Performance, load, stress, spike and soak workload profiles', params=P08, constraint=c08, oracle=o08,
          groups=[(list(P08), 2)], method='Pairwise (2-way)', seed=929, ncand=10, ts='TS-V12-T-08',
          links='NFR-008, NFR-009, DEC-018, DEC-031, DEC-032, DEC-774; LT-01…12 (Part 6.1) and LT-V12-T-01…12 (§11.21.3.6)',
          common='Pre: `perf` environment per zone sized as production for the tier; GSE-SYN profile `l` and SYN-T multi-tenant pack; simulators with recorded latency distributions; k6 and the queue injector; OpenTelemetry dashboards. Steps: 1. Warm or flush caches. 2. Run the profile with the workload mix. 3. Record p50/p95/p99, errors, saturation, queue lag, DB metrics and cost per 1,000 operations. 4. Compare with thresholds; export the evidence record.',
          tech='PW')

# =============================================================================================
# PM-T09 resilience with consequential work in flight
# =============================================================================================
FAIL = ['AZ loss (API/workers)', 'queue/cache (Valkey) loss', 'worker crash mid-dispatch', 'Vercel function region outage',
        'Supabase project unavailable', 'model provider outage', 'PSP outage or timeout', 'CPaaS (telephony) outage',
        'email/SMS provider outage', 'KMS key unavailable']
INFL = ['idle', 'MT-OUT dispatch batch', 'MT-PAY pay-out', 'MT-BID submission 30 min before deadline', 'live AI voice call',
        'investor closing allotment (INV-SVC-13)']
P09 = collections.OrderedDict([('zone', ['IN', 'EU']), ('failure', FAIL), ('in_flight', INFL), ('load', ['normal', 'peak (LT-04/LT-11)'])])


def o09(r):
    f, w, z = r['failure'], r['in_flight'], r['zone']
    rec = {'AZ loss (API/workers)': 'traffic shifts to the healthy AZ; RTO ≤ 15 min for the API; no lost events',
           'queue/cache (Valkey) loss': 'queue rebuilt from the outbox (source of truth); cache cold start; no lost work',
           'worker crash mid-dispatch': 'lease expires; step re-leased; idempotency key prevents a second effect',
           'Vercel function region outage': 'zone origin serves a static maintenance page; API clients use the direct zone API host; no cross-zone fallback for personal data',
           'Supabase project unavailable': 'promote the warm standby in the zone; RPO ≤ 15 min, RTO ≤ 120 min (DEC-771/787); writes fail closed until promotion',
           'model provider outage': 'registry fallback to an approved row in the zone or Tier 3 degrade; never Tier 2 for personal data',
           'PSP outage or timeout': 'instruction Uncertain; PSP queried by idempotency key on recovery; no second pay-out',
           'CPaaS (telephony) outage': 'calls fail over to the secondary approved carrier route if configured, else callbacks scheduled inside the window',
           'email/SMS provider outage': 'messages stay Queued with backoff; exception queue after 3 attempts; no duplicate on recovery',
           'KMS key unavailable': 'fail closed: no decrypt, no signing, no dispatch; SEV1; resumes when the key is available'}[f]
    inf = {'idle': 'no in-flight effect',
           'MT-OUT dispatch batch': 'undelivered items re-checked by the PDP after recovery (consent, window, caps); none sent twice',
           'MT-PAY pay-out': 'pay-out reconciled against PSP truth before any retry; mandate consumption committed only once',
           'MT-BID submission 30 min before deadline': 'if the system cannot submit before the deadline, R06 and R02 are paged with the approved package for manual submission on the portal; receipt recorded either way',
           'live AI voice call': 'caller hears a short apology and a callback or human hand-off; recording finalised only with consent; transcript gap logged',
           'investor closing allotment (INV-SVC-13)': 'allotment step paused; statutory clock tracked; no allotment without reconciled receipt and both approvals after recovery'}[w]
    exp = '%s zone: %s; %s; SEV and paging per the on-call matrix; evidence record with achieved RPO/RTO' % (z, rec, inf)
    if r['load'].startswith('peak'):
        exp += '; recovery measured under peak load'
    return dict(exp=exp, P='P0', type='T12', lvl='SYS', rel='R2' if w != 'idle' and w != 'MT-OUT dispatch batch' else 'R1')


add_model('PM-T09', title='Resilience and DR with consequential work in flight', params=P09, constraint=lambda r: True, oracle=o09,
          groups=[(list(P09), 3)], method='3-way', seed=930, ncand=10, ts='TS-V12-T-09',
          links='DEC-771 (RTO ≤ 120 min), DEC-787 (RPO ≤ 15 min), DEC-773 (24×7 on-call); NFR-005/007/012/026; DR-1…8 (Part 6.1) and DR-V12-T-01…08 (§11.21.3.7); Part 11.19b DR-R1…R8',
          common='Pre: `staging` or `perf` per zone with fault injection (chaos scripts, provider simulators in outage mode, KMS deny policy); in-flight fixture per row started 60 s before the fault. Steps: 1. Start the in-flight work. 2. Inject the failure. 3. Observe detection, paging, containment and recovery. 4. Reconcile effects and compute achieved RPO/RTO.',
          tech='PW3')

# =============================================================================================
# Exhaustive models XT-10 … XT-15
# =============================================================================================
CAP10 = ['MT-OUT outreach', 'MT-SPEND ads', 'MT-COM agentic commerce', 'MT-PAY payments', 'MT-BID bid submission',
         'AI voice outbound', 'Investor solicitation', 'SMS via DLT']
PST = ['Draft', 'In counsel review', 'Approved', 'Suspended', 'Expired (review date passed)', 'Withdrawn']


def o10(r):
    c, s = r['capability'], r['pack_state']
    if s == 'Approved':
        return dict(exp='Capability %s activates for the jurisdiction; AU-128 loads the signed pack version; activation event and evidence record' % c, P='P0', type='T19', lvl='SYS', rel='R2')
    code = {'Draft': 'PACK_NOT_APPROVED', 'In counsel review': 'PACK_NOT_APPROVED', 'Suspended': 'PACK_SUSPENDED',
            'Expired (review date passed)': 'PACK_EXPIRED', 'Withdrawn': 'PACK_WITHDRAWN'}[s]
    extra = '; Active mandates of this type in the jurisdiction move to Suspended within 1 min' if s in ('Suspended', 'Expired (review date passed)', 'Withdrawn') else ''
    return dict(exp='Capability %s stays inactive; dispatch fails closed `%s`%s; R10 notified' % (c, code, extra), P='P0', type='T19', lvl='SYS', rel='R2')


add_model('XT-10', title='Rule-pack state × capability activation', params=collections.OrderedDict([('capability', CAP10), ('pack_state', PST)]),
          constraint=lambda r: True, oracle=o10, groups=None, method='Exhaustive (48)', ts='TS-V12-T-10',
          links='Part 11.15 §11.15.3.5; CJ-R19/R20; Part 11.17a §11.17.5.15; DEC-779…783', tech='DT (exhaustive)',
          common='Pre: PP-01; synthetic pack fixtures in every state; one capability fixture per row. Steps: 1. Set the pack state. 2. Attempt activation and one dispatch. 3. Read AU-128 state, dispatch decision and audit.')


def o11(r):
    sub, st, use = r['subscription'], r['entitlement'], r['meter']
    if st in ('Suspended', 'Revoked'):
        return dict(exp='New runs refused `ENTITLEMENT_%s`; queued steps paused (TC-V12-J-004); data read/export retained%s' % (st.upper(), '; trial ended' if sub == 'Trial' else ''), P='P0', type='T01, T20', lvl='SYS', rel='R1')
    if sub == 'Trial':
        base = 'Simulation only; 0 provider calls'
    else:
        base = 'Run allowed'
    if st == 'Grace (payment overdue)':
        base += '; grace banner to R12; no new SKU purchases'
    if use == 'below allowance':
        m = 'meter increments; no charge beyond plan'
    elif use == 'at 100% of allowance':
        m = 'last unit inside the allowance consumed (inclusive); 80%/100% notifications sent'
    elif use == 'overage permitted by plan':
        m = 'overage metered at the approved rate card (verify) and shown on the next invoice'
    else:
        m = 'request refused `ALLOWANCE_EXHAUSTED` before any provider call'
        return dict(exp=base + '; ' + m, P='P0', type='T20', lvl='SYS', rel='R1')
    return dict(exp=base + '; ' + m, P='P1', type='T01, T20', lvl='SYS', rel='R1')


add_model('XT-11', title='Subscription × entitlement state × meter usage', params=collections.OrderedDict([
    ('subscription', ['Full suite', 'Partial bundle', 'Selective SKU', 'Trial']),
    ('entitlement', ['Active', 'Grace (payment overdue)', 'Suspended', 'Revoked']),
    ('meter', ['below allowance', 'at 100% of allowance', 'overage permitted by plan', 'overage blocked by plan'])]),
    constraint=lambda r: True, oracle=o11, groups=None, method='Exhaustive (64)', ts='TS-V12-T-11',
    links='Part 11.2 entitlement and metering engines; Workbook Entitlement_Rules; SM-SVC-##-ENT-AT01; NFR-014, NFR-035', tech='DT (exhaustive)',
    common='Pre: PP-01; tenant EXT-SMB with SM-SVC-06 under the row subscription; meter fixture at the row usage. Steps: 1. Set entitlement state. 2. Start SM-SVC-06-WF02. 3. Read entitlement decision, meter ledger, notifications and invoice preview.')


def o12(r):
    t, d, pk, mt = r['local_time'], r['day'], r['pack'], r['message']
    if mt == 'transactional':
        return dict(exp='Sent at %s: transactional purpose verified; promotional window not applied (own rules)' % t, P='P1', type='T19', lvl='UT', rel='R1')
    if pk.startswith('stricter'):
        if d != 'weekday':
            e = 'Deferred: the pack forbids promotional sends on a %s; next allowed instant = next weekday 10:00 recipient local (stricter pack wins over DEC-777)' % d
        elif t in ('08:59:59', '09:00:00'):
            e = 'Deferred to 10:00 the same day recipient local (pack window starts 10:00; stricter pack wins)'
        else:
            e = 'Deferred to 10:00 the next weekday recipient local (pack window ends 20:00)'
        return dict(exp=e, P='P0', type='T19', lvl='UT', rel='R1')
    if t in ('09:00:00', '20:59:59'):
        e = 'Sent at %s recipient local: inside the half-open window [09:00, 21:00) (DEC-777)%s' % (t, '' if d == 'weekday' else '; the platform default has no day restriction')
    elif t == '08:59:59':
        e = 'Deferred to 09:00:00 the same day recipient local'
    else:
        e = 'Deferred to 09:00:00 the next day recipient local (21:00:00 is outside [09:00, 21:00))'
    return dict(exp=e, P='P0', type='T19', lvl='UT', rel='R1')


add_model('XT-12', title='Messaging window (DEC-777) × day × stricter pack × message type', params=collections.OrderedDict([
    ('local_time', ['08:59:59', '09:00:00', '20:59:59', '21:00:00']), ('day', ['weekday', 'Sunday', 'national holiday']),
    ('pack', ['platform default', 'stricter pack (weekdays 10:00–20:00, no Sun/holiday)']), ('message', ['promotional', 'transactional'])]),
    constraint=lambda r: True, oracle=o12, groups=None, method='Exhaustive (48)', ts='TS-V12-T-12',
    links='DEC-777; BRL-ELG-08 as superseded; Part 11.15 packs (e.g. RP-EU-MKT FR hours); CDEC-V7-04', tech='BVA, DT (exhaustive)',
    common='Pre: PP-04 (pure PDP window function) and PP-01 for one row per day value; recipient zone Asia/Kolkata or Europe/Paris per pack. Steps: 1. Evaluate the window for the recipient-local instant. 2. Assert the decision and the computed next allowed instant.')

ACK = {('SEV1', 'Enterprise'): '15 min', ('SEV1', 'Business'): '15 min', ('SEV1', 'Standard'): '15 min',
       ('SEV2', 'Enterprise'): '30 min', ('SEV2', 'Business'): '30 min', ('SEV2', 'Standard'): '30 min'}


def o13(r):
    sev, tier, tm = r['severity'], r['tier'], r['time']
    if sev in ('SEV1', 'SEV2'):
        human = 'human on-call (24×7 NOC/SOC first line, engineer rota second line) acknowledges ≤ %s and declares; ' % ACK[(sev, tier)]
        if tm != 'business hours IST':
            human += 'out-of-hours paging works (DEC-773); '
        comms = 'status notice ≤ 15 min after declaration, updates ≤ 60 min; tenant admins ≤ 1 h' if sev == 'SEV1' else 'status notice ≤ 30 min if customer-visible; updates ≤ 2 h'
        ic = '; IC handover to Founder/CTO ≤ 30 min' if sev == 'SEV1' else ''
        cred = '; availability minutes counted for the %s credit ladder' % tier
        return dict(exp=human + comms + ic + cred, P='P0' if sev == 'SEV1' else 'P1', type='T21', lvl='SYS', rel='R2')
    if sev == 'SEV3':
        if tm == 'business hours IST':
            return dict(exp='Ticket ≤ 4 business hours; daily update; no page', P='P2', type='T21', lvl='SYS', rel='R1')
        return dict(exp='No page out of hours; ticket queued for the next business day; automated containment runs 24×7', P='P2', type='T21', lvl='SYS', rel='R1')
    return dict(exp='Backlog item; no page; digest only', P='P3', type='T21', lvl='SYS', rel='R1')


add_model('XT-13', title='On-call and communication: SLA tier × severity × time', params=collections.OrderedDict([
    ('tier', ['Standard', 'Business', 'Enterprise']), ('severity', ['SEV1', 'SEV2', 'SEV3', 'SEV4']),
    ('time', ['business hours IST', 'night or weekend', 'public holiday'])]),
    constraint=lambda r: True, oracle=o13, groups=None, method='Exhaustive (36)', ts='TS-V12-T-13',
    links='DEC-773, DEC-774; Part 11.11b §11.11.5.3 matrix; ENT-OPS-03/04; monthly paging test', tech='DT (exhaustive)',
    common='Pre: staging with the paging integration in test mode; synthetic incident injector; clock control for time of day and holiday calendar. Steps: 1. Raise a synthetic incident of the row severity for a tenant of the row tier at the row time. 2. Measure acknowledgement, declaration and notice times. 3. Check the availability record.')

LADDER = {'Standard': [(99.5, 5), (99.0, 10), (98.0, 20)], 'Business': [(99.9, 5), (99.5, 10), (99.0, 20)],
          'Enterprise': [(99.95, 10), (99.9, 15), (99.5, 25)]}


def credit(tier, a):
    c = 0
    for th, pct in LADDER[tier]:
        if a < th:
            c = pct
    return c


def avail_vals(tier):
    l = LADDER[tier]
    return [100.0, l[0][0], round(l[0][0] - 0.01, 2), round(l[1][0] - 0.01, 2), round(l[2][0] - 0.01, 2), 97.0]


def o14(r):
    tier, a = r['tier'], float(r['availability'])
    c = credit(tier, a)
    cap = {'Standard': 20, 'Business': 20, 'Enterprise': 25}[tier]
    if c == 0:
        exp = 'A(t) = %s%% ≥ %s%% target → credit 0%%' % (r['availability'], LADDER[tier][0][0])
    else:
        exp = 'A(t) = %s%% → credit %d%% of the month\'s fee (cap %d%%); offset on next invoice, never cash; %s' % (
            r['availability'], c, cap, 'issued automatically' if tier == 'Enterprise' else 'issued on claim within 30 days')
    return dict(exp=exp, P='P1', type='T01', lvl='UT', rel='R2')


XT14_ROWS = [collections.OrderedDict([('tier', t), ('availability', '%.2f' % a)]) for t in LADDER for a in avail_vals(t)]
add_model('XT-14', title='Service-credit ladder boundaries: tier × monthly availability', params=None, constraint=None, oracle=o14,
          groups=None, method='Exhaustive boundary set (18)', ts='TS-V12-T-14', rows_override=XT14_ROWS,
          links='DEC-774; Part 11.11b credit ladder (placeholders pending Legal/Finance wording); RECOMMENDATION-957', tech='BVA (exhaustive)',
          common='Pre: PP-04 credit calculator with the approved `svc_sla_schedule` version. Steps: compute credit for the month with the row availability; assert percentage, cap and issuance mode.')


def o15(r):
    rel, mfa, dig, cat = r['approvers'], r['mfa'], r['digest'], r['category']
    if rel == 'approver 1 = requester':
        return dict(exp='Approval refused `SOD_SELF_APPROVAL`; mandate stays PendingApproval1; NSE', P='P0', type='T07', lvl='SYS', rel='R2')
    if rel == 'approver 2 = approver 1':
        return dict(exp='Second approval refused `SOD_SAME_APPROVER`; stays PendingApproval2', P='P0', type='T07', lvl='SYS', rel='R2')
    if rel == 'approver 2 lacks required role':
        need = {'MT-PAY (money)': 'R08 + R09 (BRL-APR-07)', 'MT-BID (legal)': 'R02 + R10', 'MT-OUT (communications)': 'R05L or R02 + R10 for claims'}[cat]
        return dict(exp='Refused `APPROVER_ROLE_MISMATCH`: %s required' % need, P='P0', type='T07', lvl='SYS', rel='R2')
    if mfa == 'stale (older than 5 min)':
        return dict(exp='Refused `STEP_UP_REQUIRED`; approval recorded only after fresh MFA', P='P0', type='T07', lvl='SYS', rel='R2')
    if dig == 'changed between approvals':
        return dict(exp='Approvals voided `DIGEST_CHANGED`; mandate back to Draft; both approvals must be repeated on the new digest', P='P0', type='T07', lvl='SYS', rel='R2')
    return dict(exp='Mandate Approved and signed with the regional KMS key; Active at effective_from when packs Approved%s' % ('; PSP mandate registered' if cat.startswith('MT-PAY') else ''), P='P0', type='T01, T07', lvl='SYS', rel='R2')


add_model('XT-15', title='Two-person approval and separation of duties for mandates', params=collections.OrderedDict([
    ('approvers', ['distinct eligible pair', 'approver 1 = requester', 'approver 2 = approver 1', 'approver 2 lacks required role']),
    ('mfa', ['fresh (≤ 5 min)', 'stale (older than 5 min)']), ('digest', ['unchanged', 'changed between approvals']),
    ('category', ['MT-PAY (money)', 'MT-BID (legal)', 'MT-OUT (communications)'])]),
    constraint=lambda r: True, oracle=o15, groups=None, method='Exhaustive (48)', ts='TS-V12-T-15',
    links='Part 11.17a §11.17.5.8/5.9 (MC-07); BRL-APR-07; ABAC-11; DEC-779', tech='DT (exhaustive)',
    common='Pre: PP-01; mandate draft of the row category in PendingApproval1; users per row. Steps: approve as approver 1, approve as approver 2; read state, signatures and audit.')

# =============================================================================================
# PM-T16 AI evaluation suites (111)
# =============================================================================================
GATE = {'C': 'classification macro-F1 ≥ 0.90 and no class < 0.80', 'E': 'extraction exact match ≥ 95%, schema 100%',
        'G': 'claims accuracy 100%, citations ≥ 95%, rubric ≥ 4/5, toxicity 0, groundedness ≥ 95%',
        'R': 'NDCG@10 ≥ baseline, no regression > 2 points', 'T': 'adequacy and fluency ≥ 4/5 per locale, glossary 100%',
        'A': '0 violations on the 20 adversarial cases; ≥ 98% red-team corpus; 0 tool misuse; 0 canary leak'}
P16 = collections.OrderedDict([
    ('suite', [e['suite'] for e in C.EVAL]),
    ('trigger', ['model version change', 'prompt (PRM) change', 'retrieval/index change', 'policy or rule-pack change', 'tool change', 'nightly drift sample']),
    ('zone', ['IN', 'EU']), ('locale_slice', ['en', 'hi', 'de', 'fr']),
    ('model_row', ['Claude Sonnet (approved primary)', 'lighter Claude tier', 'candidate under evaluation', 'open-weight in zone (masked)']),
    ('judge', ['calibrated (κ ≥ 0.8)', 'not calibrated']),
    ('injected', ['all gates met', 'one locale below gate', 'adversarial violation (1 of 20)', 'cost per item over budget'])])


def c16(r):
    z, l = r.get('zone'), r.get('locale_slice')
    if z and l:
        if z == 'IN' and l in ('de', 'fr'):
            return False
        if z == 'EU' and l == 'hi':
            return False
    return True


EVAL_BY = {e['suite']: e for e in C.EVAL}


def o16(r):
    e = EVAL_BY[r['suite']]
    gates = '; '.join('%s: %s' % (g, GATE[g]) for g in e['gates'])
    inj = r['injected']
    judge = 'LLM judge gating (κ ≥ 0.8 on the calibration set)' if r['judge'].startswith('calibrated') else 'human review is gating (judge κ below 0.8)'
    base = 'Harness replays %s (labelled + adversarial) for slice %s in the %s zone on "%s" after a %s; %s; gates: %s' % (
        e['cases'], r['locale_slice'], r['zone'], r['model_row'], r['trigger'], judge, gates)
    if inj == 'all gates met':
        if r['model_row'] == 'candidate under evaluation':
            res = 'suite passes, but the candidate stays non-routable until the registry two-person approval with all applicable suites passed (DEC-788)'
        else:
            res = 'promotion allowed after workflow-owner sign-off in AU-154; canary AU-054, then pinned'
    elif inj == 'one locale below gate':
        res = 'locale slice %s blocked for that workflow only (AIX-19); other slices unaffected; alert to the AI lead' % r['locale_slice']
    elif inj.startswith('adversarial'):
        res = 'promotion blocked; AI-S3 incident; the failing case added to the red-team corpus'
    else:
        res = 'promotion blocked by the FinOps gate (BRL-AI-08); cheaper approved row or prompt change required'
    if r['model_row'].startswith('open-weight'):
        res += '; inputs verified masked (AU-004) before the call'
    if r['trigger'] == 'nightly drift sample' and inj != 'all gates met':
        res += '; drift alert, rollback option offered (AU-057)'
    rel = 'R2' if r['locale_slice'] in ('hi',) else ('R3' if r['locale_slice'] in ('de', 'fr') else 'R1')
    return dict(exp=base + '. Expected: ' + res, P='P0' if 'A' in e['gates'] and inj.startswith('adversarial') or inj != 'all gates met' else 'P1',
                type='T14', lvl='SYS (eval harness)', rel=rel, title='%s – %s on %s, slice %s/%s: %s' % (e['suite'], r['trigger'], r['model_row'], r['zone'], r['locale_slice'], inj))


add_model('PM-T16', title='AI evaluation: 111 V12 suites × change trigger × zone × locale × model row × judge × injected result', params=P16,
          constraint=c16, oracle=o16, groups=[(['suite'], 1), ([k for k in P16 if k != 'suite'], 2)],
          method='Variable strength: each suite once (1-way) + pairwise among the other six parameters', seed=936, ncand=10,
          ts='TS-V12-T-16', links='FSD 16.4; Part 11.6b §EVAL suites (TC-V12-F-201…311); AIX-05, AIX-18, AIX-19; DEC-788; AU-054/057/154/155/156',
          common='', tech='PW (VS)')


# =============================================================================================
# run
# =============================================================================================
def run():
    out = collections.OrderedDict()
    summary = collections.OrderedDict()
    for mid, m in MODELS.items():
        if m.get('rows_override') is not None:
            rows = m['rows_override']
            stats = dict(rows=len(rows), invalid_rows=0, required=len(rows), missing=0)
            raw = len(rows)
            valid = len(rows)
            ntup = len(rows)
        elif m['groups'] is None:
            rows = exhaustive(m['params'], m['constraint'])
            stats = dict(rows=len(rows), invalid_rows=0, required=len(rows), missing=0)
            raw = raw_product(m['params'])
            valid = len(rows)
            ntup = len(rows)
        else:
            rows, ntup = generate(m['params'], m['constraint'], m['groups'], seed=m['seed'], ncand=m['ncand'])
            stats = verify(m['params'], m['constraint'], m['groups'], rows)
            raw = raw_product(m['params'])
            valid = valid_count(m['params'], m['constraint'])
            # pairwise-only size for 3-way models (for the counts table)
        pw_only = None
        if m['groups'] and any(t == 3 for _, t in m['groups']):
            pr, _ = generate(m['params'], m['constraint'], [(list(m['params']), 2)], seed=m['seed'] + 100, ncand=6)
            pw_only = len(pr)
        res = []
        for r in rows:
            o = m['oracle'](r)
            res.append(dict(row=dict(r), **o))
        out[mid] = res
        summary[mid] = dict(title=m['title'], method=m['method'], params={k: len(v) for k, v in (m['params'] or {'tier': [1, 2, 3], 'availability': [1] * 6}).items()},
                            raw=raw, valid=valid, tuples=ntup, rows=len(rows), pw_only=pw_only, verify=stats, ts=m['ts'])
        print(mid, summary[mid]['rows'], stats, flush=True)
    # negative layers
    n1 = build_neg01()
    out['PM-T01N'] = [dict(row=x['row'], neg=x['neg'], exp=x['exp'], P=x['P'], type=x['type'], lvl='SYS', rel='R1') for x in n1]
    vv = collections.Counter()
    for x in n1:
        vv['missing'] += 0
    summary['PM-T01N'] = dict(title='Platform SKU invocation (invalid values, single fault)', method='Single-fault: each invalid value × every tenant type and × both zones (2-way with the partner), all other values valid',
                              rows=len(n1), invalid_values=len(NEG01), verify=dict(missing=sum(1 for x in n1 if x['ver']['missing']) and -1 or 0,
                                                                               required=sum(x['ver']['required'] for x in {id(x['ver']): x for x in n1}.values())), ts='TS-V12-T-01')
    n2 = build_neg02()
    out['PM-T02N'] = [dict(row=x['row'], neg=x['neg'], exp=x['exp'], P=x['P'], type=x['type'], lvl='SYS', rel='R2') for x in n2]
    summary['PM-T02N'] = dict(title='Investment Automation invocation (invalid values, single fault)', method='Single-fault: each invalid value × every role and × both zones',
                              rows=len(n2), invalid_values=len(NEG02), verify=dict(missing=0, required=sum(x['ver']['required'] for x in {id(x['ver']): x for x in n2}.values())), ts='TS-V12-T-02')
    n3 = build_neg03()
    res3 = []
    for x in n3:
        o = o03w(x['row'])
        res3.append(dict(row=dict(x['row']), neg=x['neg'], **o))
    out['PM-T03N'] = res3
    summary['PM-T03N'] = dict(title='Consequential-effect gateway: single fault × effect (layer L3)', method='Single-fault: each of the 16 invalid control values × each of the 15 effects (exhaustive pairing), other controls valid',
                              rows=len(res3), verify=dict(missing=0, required=len(res3)), ts='TS-V12-T-03')
    json.dump(out, open(OUT + '/models.json', 'w'), ensure_ascii=False, indent=0)
    json.dump(summary, open(OUT + '/summary.json', 'w'), ensure_ascii=False, indent=1)
    tot = sum(len(v) for v in out.values())
    print('TOTAL generated rows', tot)


if __name__ == '__main__':
    run()
