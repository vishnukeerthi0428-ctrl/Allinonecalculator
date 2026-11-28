"""Group R (Part 11.19): combinatorial parameter models, covering-array generation (pairwise and
3-way, constraint-aware greedy) and the test oracle for every generated case.

Method: for each model, enumerate every *valid* full combination (constraints applied), list every
valid t-tuple (t = 2 or 3), then greedily pick the valid row that covers the most uncovered
t-tuples (ties broken by enumeration order, so the output is deterministic). Small spaces (<= 64
valid rows) are enumerated exhaustively instead.  Each selected row is passed to the model's
oracle, which returns the expected result, priority, type and level.  Output: Markdown fragments
in assembly/v12b/R_frag/ and a JSON count summary used by the Part 11.19 text.
Run:  python3 -I assembly/v12b/R_02_combinatorics.py
"""
import itertools, json, os, collections
BP = '/home/user/Allinonecalculator/blueprint'
OUT = BP + '/assembly/v12b/R_frag'
os.makedirs(OUT, exist_ok=True)

# ----------------------------------------------------------------------------- covering arrays
def valid_rows(params, constraint):
    names = list(params)
    rows = []
    for combo in itertools.product(*[params[n] for n in names]):
        r = dict(zip(names, combo))
        if constraint(r):
            rows.append(r)
    return names, rows

def covering(params, constraint, t):
    names, rows = valid_rows(params, constraint)
    if len(rows) <= 64:
        return rows, len(rows), 'exhaustive', len(rows)
    idx_sets = list(itertools.combinations(range(len(names)), t))
    def tuples(r):
        return {(ix, tuple(r[names[i]] for i in ix)) for ix in idx_sets}
    rt = [tuples(r) for r in rows]
    uncovered = set().union(*rt)
    n_tuples = len(uncovered)
    chosen = []
    while uncovered:
        best, bi = -1, -1
        for i, s in enumerate(rt):
            g = len(s & uncovered)
            if g > best:
                best, bi = g, i
        chosen.append(rows[bi]); uncovered -= rt[bi]
    return chosen, len(rows), f'{t}-way', n_tuples

# ----------------------------------------------------------------------------- models and oracles
M = collections.OrderedDict()

def model(mid, title, cap, t, params, constraint, oracle, common, level='SYS', story='', links=''):
    M[mid] = dict(title=title, cap=cap, t=t, params=params, constraint=constraint, oracle=oracle,
                  common=common, level=level, story=story, links=links)

# M01 SSO login -------------------------------------------------------------------------------
PRIV = {'R12 tenant admin', 'R02 startup head', 'Custom privileged role'}
def o_m01(r):
    a = r['assertion']
    if a != 'valid':
        code = {'wrong audience': '401 `SSO_AUDIENCE_MISMATCH`', 'wrong issuer': '401 `SSO_ISSUER_MISMATCH`',
                'expired (NotOnOrAfter + 60 s skew passed)': '401 `SSO_ASSERTION_EXPIRED`',
                'replayed assertion or code': '401 `SSO_REPLAY_DETECTED`; `identity.sso.replay` SEV3 security event',
                'unsigned or alg none': '401 `SSO_SIGNATURE_INVALID`; SEV3 security event'}[a]
        return f"{code}; no session cookie; audit `outcome=denied` in the {r['region']} region store; NSE", 'P0', 'T07'
    if r['domain'] == 'unverified':
        return ("Home-realm discovery does not route to the tenant IdP; user is offered the local sign-in of the reused IdP only; "
                "`SSO_DOMAIN_UNVERIFIED` shown to tenant admin on A122"), 'P1', 'T01'
    mfa = r['mfa']
    role = r['role']
    tail = f"session issued by the {r['region']} stack only (cookie `__Host-ge_{r['region'].lower()}`), audit and session rows written in {r['region']}"
    if role in PRIV and mfa != 'phishing-resistant (amr hwk/webauthn)':
        ex = 'session limited to step-up: WebAuthn ceremony required before any privileged API (403 `STEP_UP_REQUIRED` until done)'
        p = 'P0'
    elif mfa == 'none' and role not in PRIV:
        ex = 'session created; MFA satisfied by platform policy `required_privileged` (non-privileged role); sensitive exports still step-up'
        p = 'P1'
    else:
        ex = 'session created with `acr`/`amr` recorded; no step-up for 12 h (ABAC-11)'
        p = 'P1'
    if r['domain'] == 'verification lost (TXT missing twice)':
        ex += '; banner "Domain verification lost" for R12 and High notification; enforcement continues until R12 confirms (no surprise lockout)'
    if r['enforcement'] == 'on' and role != 'R12 tenant admin':
        ex += '; local password sign-in for this domain returns 403 `SSO_ENFORCED`'
    return f"{ex}; {tail}", p, 'T07'

model('M01', 'Tenant SSO sign-in: IdP × protocol × role × region × domain × enforcement × MFA × assertion', 'C1', 3,
      collections.OrderedDict([
        ('idp', ['Okta', 'Microsoft Entra ID', 'Google Workspace', 'Generic SAML IdP', 'Generic OIDC IdP']),
        ('protocol', ['SAML 2.0', 'OIDC']),
        ('role', ['R12 tenant admin', 'R02 startup head', 'R03 executive', 'R15 auditor', 'Custom privileged role']),
        ('region', ['IN', 'EU']),
        ('domain', ['verified', 'unverified', 'verification lost (TXT missing twice)']),
        ('enforcement', ['off', 'on']),
        ('mfa', ['phishing-resistant (amr hwk/webauthn)', 'OTP (amr otp)', 'none']),
        ('assertion', ['valid', 'wrong audience', 'wrong issuer', 'expired (NotOnOrAfter + 60 s skew passed)', 'replayed assertion or code', 'unsigned or alg none'])]),
      lambda r: not (r['idp'] == 'Generic SAML IdP' and r['protocol'] != 'SAML 2.0') and not (r['idp'] == 'Generic OIDC IdP' and r['protocol'] != 'OIDC')
                and not (r['enforcement'] == 'on' and r['domain'] == 'unverified'),
      o_m01,
      'Pre: PP-01 per region stack (IN = Mumbai, EU = Frankfurt); tenant "Kestrel Analytics" (IN) or "Nordlicht GmbH" (EU); IdP simulator with signed metadata, two active signing certificates; clock CLK-0. Steps: 1. POST `/bff/admin/sso/discover` {email}. 2. Follow redirect to the IdP simulator, which returns the assertion/code variant in the row. 3. Callback to the BFF; read session, audit and security-event tables in the tenant region; call one privileged API (`PATCH /api/v1/tenants/{id}/security-policy`).',
      story='US-01-ZR01, US-01-ZR02', links='FR-V12-R-001…010; ENT-IDN-01/02/04/05/06; DEC-784; DEC-772')

# M02 SCIM -------------------------------------------------------------------------------------
def o_m02(r):
    if r['endpoint'] == 'other-region host':
        return '401 `invalidToken` (tokens are region-bound; lookup in the other region misses); no row read or written in either region; NSE', 'P0', 'T15'
    tok = r['token']
    if tok != 'valid':
        return f"401 SCIM error `invalidToken` ({tok}); NSE; `identity.scim.auth_failed` counter +1; 5 failures in 10 min → R12 notification", 'P0', 'T07'
    op, us, gm = r['op'], r['user'], r['mapping']
    if us == 'break-glass account' and op in ('PATCH active=false', 'DELETE', 'PUT replace'):
        return '409 `mutability` "break-glass accounts are not SCIM-managed"; account unchanged; audit', 'P0', 'T07'
    if op == 'POST create':
        if us == 'active member' or us == 'break-glass account':
            return '409 SCIM `uniqueness`; no duplicate membership', 'P1', 'T01'
        if us == 'deprovisioned':
            return '201; membership re-activated in state `provisioned` with **no roles** until a mapped group is assigned; old API keys stay revoked', 'P1', 'T01'
        return '201; membership `provisioned`; `identity.scim.user_provisioned` event; no role until a mapped group arrives', 'P1', 'T01'
    if us == 'not yet provisioned':
        return '404 SCIM `noTarget`; NSE', 'P2', 'T01'
    if op in ('PATCH active=false', 'DELETE'):
        if us == 'deprovisioned':
            return '200/204 idempotent; no new event; nothing changes', 'P1', 'T16'
        return ('204/200; membership `deprovisioned`; sessions revoked ≤ 60 s; API keys and OAuth clients created by the user disabled; '
                'pending approvals re-queued to R12; scheduled jobs re-assigned (never cancelled); end-to-end ≤ 15 min from IdP change (AU-291 measures)'), 'P0', 'T07'
    if op == 'PUT replace':
        return '200; attributes replaced; `active` honoured; role set recomputed from mapped groups; SoD re-checked', 'P1', 'T01'
    if op == 'PATCH group add':
        if gm == 'unmapped group':
            return '200; group membership stored; **no role granted**; task "Map group" for R12 on A122', 'P1', 'T01'
        if gm == 'mapped to conflicting custom role':
            return '409 `SOD_CONFLICT_ON_ASSIGNMENT`; group stored, role not granted; SoD violation event to R10', 'P0', 'T07'
        return f'200; role from {gm} granted; permission cache invalidated ≤ 60 s', 'P1', 'T01'
    if op == 'PATCH group remove':
        return '200; role removed; open sessions re-evaluated within 60 s; privileged session demoted', 'P1', 'T07'
    return '200', 'P2', 'T01'

model('M02', 'SCIM 2.0 provisioning: IdP × operation × user state × group mapping × token × region endpoint', 'C1', 3,
      collections.OrderedDict([
        ('idp', ['Okta', 'Microsoft Entra ID', 'Google Workspace']),
        ('op', ['POST create', 'PUT replace', 'PATCH active=false', 'DELETE', 'PATCH group add', 'PATCH group remove']),
        ('user', ['not yet provisioned', 'active member', 'deprovisioned', 'break-glass account']),
        ('mapping', ['mapped to built-in role', 'mapped to custom role', 'mapped to conflicting custom role', 'unmapped group']),
        ('token', ['valid', 'revoked', 'expired', 'other tenant']),
        ('endpoint', ['home-region host', 'other-region host'])]),
      lambda r: not (r['op'] not in ('PATCH group add',) and r['mapping'] == 'mapped to conflicting custom role'),
      o_m02,
      'Pre: PP-01; SCIM base `https://api.<region>.<platform-domain>/scim/v2`; tenant token issued for the home region; IdP simulator replays the provider-specific payload shapes (Okta, Entra ID, Google). Steps: send the SCIM request in the row; read membership, session, API-key, approval-queue and outbox tables; read the AU-291 SLA record.',
      story='US-01-ZR03', links='FR-V12-R-011…016; ENT-IDN-03; RFC 7643/7644; DEC-784')

# M03 custom roles and SoD ---------------------------------------------------------------------
def o_m03(r):
    if r['actor'] == 'R13 operator support (no JIT grant)':
        return '403 `TENANT_SCOPE_REQUIRED` (operator has no default tenant access, ENT-ACC-05); NSE', 'P0', 'T15'
    if r['actor'] == 'Custom admin lacking billing.approve':
        if 'Billing' in r['pair']:
            return '403 `PERMISSION_NOT_HELD` (a role cannot grant a permission its creator lacks); NSE', 'P0', 'T07'
    conflict = r['pair'] != 'Leads:read + Leads:write (no conflict)'
    if not conflict:
        return '201/200; role or assignment saved; `access.role.created`/`.updated`; permission cache invalidated ≤ 60 s', 'P1', 'T01'
    msg = {'API role save': '422 `SOD_CONFLICT` naming both permissions',
           'Direct DB insert as app_rw': 'PostgreSQL exception "separation of duties violation" from trigger `role_permission_sod` (C2-T1); transaction rolled back',
           'Membership assignment of two roles': '409 `SOD_CONFLICT_ON_ASSIGNMENT` from the `membership_role` trigger and API check',
           'SCIM group mapping': '409 `SOD_CONFLICT_ON_ASSIGNMENT`; mapping saved as `blocked`; R10 notified'}[r['path']]
    return f"{msg}; NSE; audit `outcome=denied` rule ENT-ACC-02", 'P0', 'T07'

model('M03', 'Custom roles and separation of duties: permission pair × path × scope × actor', 'C1', 2,
      collections.OrderedDict([
        ('pair', ['Runs:create + Runs:approve', 'Configuration:edit + Configuration:approve', 'Billing:view + Billing:approve',
                  'Runs:approve + Runs:dispatch', 'Finance:verify_first + Finance:verify_second', 'Leads:read + Leads:write (no conflict)']),
        ('path', ['API role save', 'Direct DB insert as app_rw', 'Membership assignment of two roles', 'SCIM group mapping']),
        ('scope', ['tenant-wide', 'company-scoped']),
        ('actor', ['R12 tenant admin', 'R01 founder (owned tenant)', 'R13 operator support (no JIT grant)', 'Custom admin lacking billing.approve'])]),
      lambda r: True, o_m03,
      'Pre: PP-01 / PP-05 (direct DB path uses the IT profile with role `app_rw` and `app.tenant_id` set). Steps: attempt the save or assignment through the path in the row; read `custom_role`, `role_permission`, `membership_role`, audit.',
      story='US-01-ZR04', links='FR-V12-R-017…022; ENT-ACC-01/02; C2-T1; DEC-784')

# M04 developer credentials --------------------------------------------------------------------
def o_m04(r):
    if r['host'] == 'browser host (admin/web origin)':
        return '401 `TOKEN_NOT_ACCEPTED_ON_BROWSER_HOST`; bearer credentials are accepted only on `api.<region>.<platform-domain>`; NSE', 'P0', 'T07'
    if r['region'] == 'other region host':
        return '401 `INVALID_CREDENTIAL` (credential registry is per region; no cross-region lookup); NSE', 'P0', 'T15'
    st = r['state']
    if st != 'active':
        code = {'expired': '401 `API_KEY_EXPIRED`', 'revoked (≤ 60 s ago)': '401 `API_KEY_REVOKED`', 'IP not in allowlist': '403 `IP_NOT_ALLOWED`'}[st]
        return f'{code}; NSE; `developer.auth_failed` metric', 'P0', 'T07'
    sc = r['scope']
    if sc == 'approve/send/pay (non-existent scope)':
        return '403 `SCOPE_NOT_GRANTABLE`; there is no scope for consequential actions; mandate-bound execution only through Part 11.17 controls; NSE', 'P0', 'T07'
    if sc == 'missing scope':
        return '403 `INSUFFICIENT_SCOPE` with `required_scope`; NSE', 'P1', 'T07'
    if r['rate'] == 'over limit':
        return '429 `RATE_LIMITED` + `Retry-After` + `RateLimit-Policy`; NSE; other tenants unaffected', 'P1', 'T03'
    ok = {'leads:read': '200 with masked contact fields', 'leads:write': '201 draft record; no send', 'runs:create': '202 run `held_for_approval` or `draft`; never executes a consequential step without a human or a valid mandate'}[sc]
    if r['rate'] == 'at limit':
        ok += '; `RateLimit: remaining=0`'
    return ok + f"; audit attributes `credential_id`, `{r['cred']}`", 'P1', 'T01'

model('M04', 'Developer API credentials: credential × state × scope × region × host × rate', 'C2', 3,
      collections.OrderedDict([
        ('cred', ['API key gek_', 'OAuth client private_key_jwt', 'OAuth client client_secret_basic']),
        ('state', ['active', 'expired', 'revoked (≤ 60 s ago)', 'IP not in allowlist']),
        ('scope', ['leads:read', 'leads:write', 'runs:create', 'missing scope', 'approve/send/pay (non-existent scope)']),
        ('region', ['home region host', 'other region host']),
        ('host', ['developer host', 'browser host (admin/web origin)']),
        ('rate', ['under limit', 'at limit', 'over limit'])]),
      lambda r: True, o_m04,
      'Pre: PP-01 developer host; tenant with one API key and two OAuth clients (one per auth method); RL-KEY 300/min per key. Steps: call `GET /api/v1/leads`, `POST /api/v1/leads` or `POST /api/v2/workflow-runs` as the scope column implies; read audit, rate-limit counters and outbox.',
      story='US-20-ZR06, US-20-ZR07', links='FR-V12-R-031…040; ENT-API-01/02/03; DEC-785')

# M05 webhook delivery -------------------------------------------------------------------------
SCHED = {1: 'T+5 min', 2: 'T+30 min', 3: 'T+2 h', 4: 'T+6 h', 5: 'T+15 h', 6: '—'}
def o_m05(r):
    if r['endpoint'] == 'unverified (challenge not passed)':
        return 'No delivery; event retained 7 days in the outbox projection; endpoint shows "Verify endpoint"; NSE at the receiver', 'P1', 'T01'
    resp, att = r['response'], int(r['attempt'])
    if resp == '2xx within 10 s':
        return f'`developer.webhook_delivery.succeeded`; attempt {att} recorded with signature timestamp; no further attempts', 'P1', 'T16'
    if resp == '410 Gone':
        return 'Endpoint disabled immediately (`developer.webhook_endpoint.disabled`, reason 410); no retry; R12 notified', 'P1', 'T01'
    if att == 6:
        return f'`developer.webhook_delivery.exhausted` after attempt 6 (≤ 24 h after first); endpoint flagged; replay available from A125 for 30 days', 'P1', 'T18'
    return f'`developer.webhook_delivery.failed`; next attempt {att+1} at {SCHED[att]} ±10% jitter; redirects not followed; same `event_id`, new signature timestamp', 'P1', 'T18'

model('M05', 'Outbound webhook delivery: event × endpoint response × attempt × endpoint state × region', 'C2', 2,
      collections.OrderedDict([
        ('event', ['lead.created', 'run.awaiting_approval', 'invoice.issued', 'connector.degraded']),
        ('response', ['2xx within 10 s', '5xx', 'timeout > 10 s', '410 Gone', 'TLS failure', '3xx redirect']),
        ('attempt', ['1', '3', '6']),
        ('endpoint', ['verified', 'unverified (challenge not passed)']),
        ('region', ['IN', 'EU'])]),
      lambda r: True, o_m05,
      'Pre: PP-05 with the webhook receiver simulator; endpoint secret v2 active; virtual clock. Steps: emit the event in the row; let the delivery worker run; drive the simulator response; read `webhook_delivery` rows and events.',
      story='US-20-ZR08', links='FR-V12-R-041…046; ENT-API-05; DEC-785')

# M06 webhook signature verification (exhaustive) ----------------------------------------------
def o_m06(r):
    ts, sig, rp = r['timestamp'], r['signature'], r['replay']
    if sig in ('tampered body', 'wrong secret', 'previous secret after 24 h overlap'):
        return 'SDK `verify()` raises `SignatureInvalid`; receiver returns 400; sender counts a failure', 'P0', 'T07'
    if ts in ('301 s old', '301 s in the future'):
        return 'SDK `verify()` raises `TimestampOutsideTolerance` (±300 s)', 'P0', 'T07'
    if rp == 'duplicate event_id':
        return 'SDK verifies; receiver idempotency store returns 200 "already processed"; no second effect', 'P0', 'T16'
    return 'SDK `verify()` returns the parsed event; receiver processes once', 'P1', 'T01'

model('M06', 'Webhook signature verification in the SDKs: timestamp × signature × replay (exhaustive)', 'C2', 2,
      collections.OrderedDict([
        ('timestamp', ['fresh', '299 s old', '301 s old', '301 s in the future']),
        ('signature', ['valid current secret', 'valid previous secret within 24 h overlap', 'previous secret after 24 h overlap', 'tampered body', 'wrong secret']),
        ('replay', ['first delivery', 'duplicate event_id'])]),
      lambda r: True, o_m06,
      'Pre: PP-04 unit profile; SDK under test (TypeScript, Python and Java each run the same table); header `GE-Signature: t=<unix>,v1=<hex HMAC-SHA256(secret, t + "." + body)>`. Steps: call `verify(headers, body, secrets)`; then the sample receiver.',
      level='UT', story='US-20-ZR08, US-20-ZR10', links='FR-V12-R-042, 052; ENT-API-05/06')

# M07 connectors ---------------------------------------------------------------------------------
CRM = {'Salesforce', 'HubSpot', 'Zoho CRM'}
def o_m07(r):
    c, f, g, env = r['connector'], r['failure'], r['gate'], r['env']
    if env == 'production' and g != 'complete':
        return f'Activation refused: 409 `CONNECTOR_GATE_INCOMPLETE` listing "{g}"; installation stays `PendingGate`; no provider call; NSE', 'P0', 'T19'
    pre = 'Sandbox adapter and provider test account only; ' if env == 'sandbox' else ''
    if f == 'none':
        out = {'SMS-DLT aggregator': 'SMS submitted with entity, header and template IDs; delivery report reconciled',
               'Voice CPaaS (140/160 series)': 'call placed from the correct number series; status webhook reconciled',
              }.get(c, 'upsert by external ID; sync cursor advanced; consent and approvals remain platform-owned')
        return pre + out + f"; data stays in the {r['residency']} zone except fields listed in the transfer entry", 'P1', 'T01'
    m = {'429 throttled': ('retry with backoff and jitter within the per-connector budget; breaker stays closed', 'P1', 'T01'),
         '5xx': ('retry 3 times; breaker opens at 50% errors over 20 calls; connector `Degraded`; AU-295 alert', 'P1', 'T21'),
         '401 token revoked': ('installation `Disabled` after 3 consecutive 401; R12 task "Reconnect"; no further calls', 'P0', 'T07'),
         'timeout on write (uncertain)': ('effect marked `Uncertain`; reconcile by external ID/message reference before any retry; never a duplicate write', 'P0', 'T18'),
         'validation 4xx': ('permanent failure; record to exception queue with field errors; no retry', 'P2', 'T01'),
         'DLT template mismatch': ('HOLD `DLT_TEMPLATE_MISMATCH` before dispatch (PDP); no SMS sent; template task to R10', 'P0', 'T19'),
         'DND/preference-registry hit': ('HOLD `REGISTRY_SCRUB_BLOCKED`; promotional message not sent; transactional allowed only on service series', 'P0', 'T19'),
         'missed provider event (gap)': ('gap detected by cursor/sequence; repair fetch; no duplicate record', 'P1', 'T16')}[f]
    return pre + m[0], m[1], m[2]

model('M07', 'Connectors: connector × auth × failure mode × residency × environment × activation gate', 'C3', 3,
      collections.OrderedDict([
        ('connector', ['Salesforce', 'HubSpot', 'Zoho CRM', 'SMS-DLT aggregator', 'Voice CPaaS (140/160 series)']),
        ('auth', ['OAuth 2.0 auth code + PKCE', 'OAuth 2.0 client credentials / JWT bearer', 'API key in vault']),
        ('failure', ['none', '429 throttled', '5xx', '401 token revoked', 'timeout on write (uncertain)', 'validation 4xx',
                     'DLT template mismatch', 'DND/preference-registry hit', 'missed provider event (gap)']),
        ('residency', ['IN', 'EU']),
        ('env', ['sandbox', 'production']),
        ('gate', ['complete', 'DPA missing', 'transfer basis CJ-R15 missing', 'DLT registration missing', 'security review missing'])]),
      lambda r: ((r['connector'] in CRM) == (r['auth'] != 'API key in vault'))
                and not (r['failure'] in ('DLT template mismatch',) and r['connector'] != 'SMS-DLT aggregator')
                and not (r['failure'] == 'DND/preference-registry hit' and r['connector'] in CRM)
                and not (r['gate'] == 'DLT registration missing' and r['connector'] in CRM)
                and not (r['env'] == 'sandbox' and r['gate'] != 'complete'),
      o_m07,
      'Pre: PP-05 with provider simulators for Salesforce, HubSpot, Zoho CRM, the SMS-DLT aggregator and the voice CPaaS; installation in the row environment; credential reference in Secrets Manager (region of the tenant). Steps: request activation (production rows) then trigger one sync or send; drive the failure mode from the simulator; read installation state, effect ledger, exception queue and events.',
      story='US-18-ZR11, US-07-ZR12, US-07-ZR13, US-23-ZR14, US-22-ZR15', links='FR-V12-R-056…080; ENT-INT-01…05; INT-01/04/05; CJ-IN-06/07; DEC-785')

# M08 Vercel data path -----------------------------------------------------------------------------
def o_m08(r):
    if r['function_region'] == 'deployed to a non-home region':
        return 'Deployment rejected by the CI region-pin check (AU-296 rule VD-02); production alias stays on the last compliant deployment; request served by it', 'P0', 'T19'
    if r['header'] == 'X-Origin-Verify missing (direct-to-origin)':
        return '403 at AWS WAF (rule `origin-verify`); request never reaches Django; WAF log only', 'P0', 'T07'
    out = f"Served by the `{r['surface'].split()[0].lower()}-{r['region'].lower()}` Vercel project; function region {'bom1' if r['region']=='IN' else 'fra1'} (verify); upstream origin in {'ap-south-1' if r['region']=='IN' else 'eu-central-1'}"
    if r['header'] == 'non-allowlisted header added':
        out += '; non-allowlisted header stripped before forwarding (allowlist VD-05)'
    if r['logging'] == 'body capture attempted':
        out += '; lint rule VD-07 blocks the build if code logs bodies; runtime log drain shows metadata only (method, path template, status, duration, region)'
    else:
        out += '; log record has no body, query string or cookie'
    if r['request'] in ('API POST with personal data', 'file upload (portal document)'):
        out += '; response `Cache-Control: no-store`; no edge cache entry'
    return out, ('P0' if r['request'] != 'page GET (no personal data)' else 'P1'), 'T19'

model('M08', 'Vercel personal-data path: surface × tenant region × request × header × logging × function region', 'C4', 3,
      collections.OrderedDict([
        ('surface', ['Website (startup domain)', 'Portal (customer)', 'Admin', 'Developer portal']),
        ('region', ['IN', 'EU']),
        ('request', ['page GET (no personal data)', 'API POST with personal data', 'file upload (portal document)', 'auth callback']),
        ('header', ['allowlisted only', 'non-allowlisted header added', 'X-Origin-Verify missing (direct-to-origin)']),
        ('logging', ['metadata only', 'body capture attempted']),
        ('function_region', ['pinned to home region', 'deployed to a non-home region'])]),
      lambda r: not (r['surface'] == 'Developer portal' and r['request'] != 'page GET (no personal data)')
                and not (r['surface'] == 'Website (startup domain)' and r['request'] == 'file upload (portal document)'),
      o_m08,
      'Pre: PP-02/PP-03/PP-01 on the region stack; Vercel preview deployment plus production alias; WAF rule set v3; log drain to the in-region collector. Steps: deploy (for the function-region rows) or send the request; inspect the response headers, the Vercel log drain, the WAF log and the origin access log.',
      story='US-21-ZR16, US-21-ZR17', links='FR-V12-R-081…095; DEC-786; DEC-772')

# M09 RPO and restore ------------------------------------------------------------------------------
def o_m09(r):
    age = int(r['wal_age'].split()[0])
    path, f = r['path'], r['failure']
    if f == 'Supabase project unavailable' and path == 'Supabase PITR to new project':
        return 'Path not available (provider control plane unreachable); runbook DR-R2 switches to the AWS WAL-G replica path; decision logged within 10 min', 'P0', 'T21'
    if f == 'region loss' and path != 'AWS WAL-G archive restore (in-zone secondary region)':
        return 'Path refused: in-region copies are lost; runbook DR-R5 uses the in-zone secondary-region WAL-G archive (IN→IN, EU→EU only)', 'P0', 'T21'
    rpo = 'RPO met' if age <= 15 else 'RPO **breached**: SEV1, release blocker if in a drill; AU-297 had paged at 10 min'
    tgt = {'IN': 'Mumbai or Hyderabad (in zone)', 'EU': 'Frankfurt or another EU region (in zone)'}[r['region']]
    return (f"Restore to T−{age} min via {path}; {rpo}; growth workload RTO ≤ 120 min, critical ≤ 4 h measured; RLS smoke, audit-chain verify, "
            f"ledger reconciliation, erasure replay; target location {tgt}; effects paused until reconciled"), 'P0', 'T21'

model('M09', 'Recovery: region × failure × WAL archive age × restore path × release gate', 'C5', 3,
      collections.OrderedDict([
        ('region', ['IN', 'EU']),
        ('failure', ['row corruption by bug', 'bad migration', 'accidental tenant delete', 'Supabase project unavailable', 'AZ loss', 'region loss']),
        ('wal_age', ['1 min', '5 min', '14 min', '16 min']),
        ('path', ['Supabase PITR to new project', 'AWS WAL-G archive restore', 'AWS WAL-G archive restore (in-zone secondary region)', 'Nightly logical dump']),
        ('gate', ['Release 1 gate', 'Release 2 gate', 'Quarterly drill'])]),
      lambda r: not (r['path'] == 'Nightly logical dump' and r['failure'] not in ('accidental tenant delete',)),
      o_m09,
      'Pre: drill environment cloned from production topology per region (synthetic data volume profile `l`); AU-297 monitors running; virtual incident clock. Steps: inject the failure; execute the runbook in the row path; record timestamps; run the post-restore verification pack PRV-01…08.',
      level='E2E', story='US-21-ZR18, US-21-ZR19', links='FR-V12-R-096…110; DEC-787; DEC-771; KPI-18/19/32; OPT-TC-ST-14')

# M10 model registry routing ---------------------------------------------------------------------
REGION_OK = {'Claude Sonnet (approved primary)': {'IN', 'EU'}, 'Claude Haiku-class': {'IN', 'EU'}, 'Claude larger model (MDL-L1)': {'IN', 'EU'},
             'OpenAI GPT family': {'EU'}, 'Google Gemini': {'IN', 'EU'}, 'Open-weight in region (Llama/Mistral/Qwen)': {'IN', 'EU'},
             'Free Tier 2 provider': set()}
def o_m10(r):
    c, st, dc, reg = r['candidate'], r['state'], r['data'], r['region']
    reasons = []
    if st != 'approved':
        reasons.append(f'registry state `{st}`')
    if reg not in REGION_OK[c]:
        reasons.append(f'no approved {reg} processing location')
    if c == 'Free Tier 2 provider' and dc not in ('Public', 'Internal (non-personal)'):
        reasons.append('Tier 2 accepts Public/Internal-non-personal only (invariant)')
    if c.startswith('Open-weight') and dc in ('Personal (unmasked)', 'Restricted'):
        reasons.append('open-weight rows accept Personal only when masked (MDL-S1)')
    if dc == 'Restricted' and c not in ('Claude Sonnet (approved primary)', 'Claude Haiku-class', 'Claude larger model (MDL-L1)'):
        reasons.append('Restricted data only to rows with a signed DPA, no-training, in-zone processing and a Restricted approval')
    if reasons:
        return ('Not routed: ' + '; '.join(reasons) + '. Router takes the next eligible approved row for (task, locale, class, region); '
                'if none: `HELD_FOR_REVIEWER` (quality) or Tier 3 template (availability). Never silently to an unapproved model'), 'P0', 'T14'
    out = f'Routed to {c} in {reg}; run record stores `mdl_id`, version, region, prompt version'
    if r['availability'] == '5xx / timeout':
        out += '; on failure: fallback only to a row with the same output schema, same region and same-or-stricter class (AU-298 eligibility); else HOLD'
    return out, 'P0' if dc in ('Restricted', 'Personal (unmasked)') else 'P1', 'T14'

model('M10', 'Model registry routing: task × data class × region × candidate × registry state × availability', 'C6', 3,
      collections.OrderedDict([
        ('task', ['classification', 'drafting', 'complex synthesis', 'embedding', 'safety screening']),
        ('data', ['Public', 'Internal (non-personal)', 'Personal (masked)', 'Personal (unmasked)', 'Restricted']),
        ('region', ['IN', 'EU']),
        ('candidate', list(REGION_OK)),
        ('state', ['approved', 'candidate', 'suspended', 'DPA expired', 'eval suite failed']),
        ('availability', ['ok', '5xx / timeout'])]),
      lambda r: not (r['task'] == 'embedding' and r['candidate'] not in ('Open-weight in region (Llama/Mistral/Qwen)', 'OpenAI GPT family', 'Google Gemini'))
                and not (r['task'] == 'safety screening' and r['candidate'] not in ('Open-weight in region (Llama/Mistral/Qwen)', 'Claude Haiku-class'))
                and not (r['task'] == 'complex synthesis' and r['candidate'] in ('Claude Haiku-class', 'Free Tier 2 provider')),
      o_m10,
      'Pre: PP-05 with the gateway simulator; registry fixture `REG-FIX-3` (all candidates in all states, regions per §11.19.5.6.C); EVAL suites marked passing for the task and locale unless the state says otherwise. Steps: submit one AI-inference step with the task, data class and tenant region in the row; read the route decision, run record and fallback log.',
      story='US-04-ZR22, US-04-ZR23', links='FR-V12-R-111…130; DEC-788; AIX-02/03; AU-151/152/298')

# M11 benchmarks ---------------------------------------------------------------------------------
def o_m11(r):
    if r['participant'] != 'opted in':
        return ('Tenant excluded from contributions and **cannot view** benchmarks (reciprocity rule BM-04); '
                + ('withdrawal applies from the next period; published cells are not recomputed' if r['participant'] == 'withdrawn' else 'A042 Benchmarks tab shows the opt-in explanation')), 'P0', 'T19'
    if r['owner'] == 'Owner Portfolio startup without R01 opt-in':
        return 'Owned startup excluded (BM-06); viewer sees benchmark built without its data', 'P0', 'T15'
    n = int(r['cohort'].split()[0])
    if n < 10:
        return f'Cell suppressed: "Not enough peers" (k = {n} < 10); no value, no count shown', 'P0', 'T19'
    if r['dominance'] == 'one tenant > 30% of events':
        return 'Cell suppressed (dominance rule BM-03); no value shown', 'P0', 'T19'
    if r['budget'] == 'ε budget exhausted for the period':
        return 'No new release this period; last published value shown with its period label; ledger entry `budget_exhausted`', 'P1', 'T19'
    scope = {'IN zone': 'computed in Mumbai from IN tenants only', 'EU zone': 'computed in Frankfurt from EU tenants only',
             'global': 'composed from the two noised regional cells only (no raw data crosses zones)'}[r['scope']]
    return f"Published: {r['metric']} cell with Laplace noise (ε = 0.5 per metric per period), clipped contributions, rounded; {scope}; shows k band (10–24 / 25+) not exact n", 'P1', 'T19'

model('M11', 'Cross-tenant benchmarks: cohort size × dominance × participation × metric × scope × owner flag × budget', 'C7', 3,
      collections.OrderedDict([
        ('cohort', ['9 tenants', '10 tenants', '25 tenants']),
        ('dominance', ['no tenant > 30%', 'one tenant > 30% of events']),
        ('participant', ['opted in', 'not opted in', 'withdrawn']),
        ('metric', ['reply rate', 'lead-to-meeting cycle time', 'win rate']),
        ('scope', ['IN zone', 'EU zone', 'global']),
        ('owner', ['external tenant', 'Owner Portfolio startup without R01 opt-in', 'Owner Portfolio startup with R01 opt-in']),
        ('budget', ['ε budget available', 'ε budget exhausted for the period'])]),
      lambda r: True, o_m11,
      'Pre: PP-05 benchmark pipeline (AU-299) with synthetic tenant set BM-FIX-1 in both zones; cohort industry "B2B software", size band "11–50". Steps: run the monthly aggregation for the period; open A042 dashboards, Benchmarks tab, as R12 of the viewer tenant; read `benchmark_cell`, `benchmark_privacy_ledger`.',
      story='US-17-ZR24, US-17-ZR25', links='FR-V12-R-131…142; DEC-789; CONFLICT-983 resolution')

# M12 Supabase access model --------------------------------------------------------------------------
def o_m12(r):
    role, ctx, op, path = r['role'], r['context'], r['op'], r['path']
    if role in ('anon via Data API', 'authenticated via Data API'):
        return 'Data API disabled for application schemas: 404 from the Data API; even if re-enabled, `permission denied` (no grants on schema `ge`); NSE', 'P0', 'T07'
    if role in ('service_role', 'postgres'):
        if path == 'CI migration with break-glass approval':
            return 'Allowed only for the migration job; audit `db.break_glass.used` with approver, ticket and expiry ≤ 2 h; SEV3 notice to R10', 'P0', 'T07'
        return 'Blocked: secret not present in API/worker task definitions (VD/SB policy check fails the deploy); runtime detector AU-292 raises SEV2 if a session with this role appears from an app subnet', 'P0', 'T07'
    if role == 'app_migrator':
        if path == 'CI migration with break-glass approval' or path == 'CI migration (normal)':
            return 'DDL allowed (`SET ROLE app_owner`); no DML on tenant rows except reviewed backfills', 'P1', 'T07'
        return 'Login refused: `app_migrator` may connect only from the CI runner IP set', 'P0', 'T07'
    if path in ('CI migration (normal)', 'CI migration with break-glass approval'):
        return f'{role} used by the migration job: refused by the pipeline policy (migrations run as app_migrator)', 'P1', 'T07'
    if ctx == 'app.tenant_id not set':
        return 'RLS denies: SELECT returns 0 rows, INSERT/UPDATE fail `WITH CHECK`; `ge.require_ctx()` raises `CONTEXT_MISSING`', 'P0', 'T15'
    if ctx == 'company not in app.company_ids':
        return '0 rows for SELECT; INSERT rejected by WITH CHECK on company scope', 'P0', 'T15'
    if op == 'UPDATE row of another tenant':
        return '0 rows affected (RLS USING); audit anomaly counter if the API expected 1', 'P0', 'T15'
    return {'SELECT own rows': 'rows of the tenant and permitted companies only', 'INSERT own row': 'row inserted with `tenant_id` from context',
            'DELETE own row': 'allowed only on tables with a delete policy; append-only tables raise'}[op], 'P1', 'T15'

model('M12', 'Supabase access model: database role × context × operation × path', 'C8', 2,
      collections.OrderedDict([
        ('role', ['app_rw', 'app_worker', 'app_migrator', 'service_role', 'postgres', 'anon via Data API', 'authenticated via Data API']),
        ('context', ['tenant and companies set', 'app.tenant_id not set', 'company not in app.company_ids']),
        ('op', ['SELECT own rows', 'INSERT own row', 'UPDATE row of another tenant', 'DELETE own row']),
        ('path', ['Django API', 'Celery worker', 'CI migration (normal)', 'CI migration with break-glass approval', 'Browser'])]),
      lambda r: not (r['path'] == 'Browser' and r['role'] not in ('anon via Data API', 'authenticated via Data API'))
                and not (r['role'] in ('anon via Data API', 'authenticated via Data API') and r['path'] != 'Browser'),
      o_m12,
      'Pre: PP-05 against a Supabase branch project per region with DDL-V12-I + DDL-V12-R applied; Data API settings as production. Steps: connect as the role through the path in the row, set the context, run the operation; read results, `pg_stat_activity` detector output and audit.',
      level='IT', story='US-01-ZR26, US-01-ZR27', links='FR-V12-R-143…155; DEC-778; SB-01…SB-10')

# M13 multimodal/registry approval (exhaustive) -------------------------------------------------------
def o_m13(r):
    ev = r['evidence']; ap = r['approvers']
    if ap == 'one approver':
        return 'Approval refused: two distinct authorised approvers required (R10 AI governance + R01 or delegate); row stays `candidate`', 'P0', 'T19'
    if ap == 'same person twice':
        return 'Second approval rejected `SAME_APPROVER`; row stays `candidate`', 'P0', 'T19'
    if ev != 'complete':
        return f'Approval refused: evidence missing "{ev}"; AU-298 checklist shows the gap', 'P0', 'T19'
    return f"Row `approved` for {r['modality']} with a 12-month re-certification date; routable only for listed task classes", 'P1', 'T19'

model('M13', 'Registry approval: modality × evidence × approvers (exhaustive)', 'C6', 2,
      collections.OrderedDict([
        ('modality', ['text LLM', 'embedding', 'image generation', 'video generation', 'voice (TTS/ASR)']),
        ('evidence', ['complete', 'DPA no-training clause', 'region/processing location', 'EVAL suites', 'red-team pass', 'security review', 'cost per accepted result']),
        ('approvers', ['two distinct approvers', 'one approver', 'same person twice'])]),
      lambda r: not (r['approvers'] != 'two distinct approvers' and r['evidence'] != 'complete'),
      o_m13,
      'Pre: PP-01 A114 model registry; candidate row with the evidence set in the row. Steps: R10 approves, then the second approver approves; read row state and audit.',
      story='US-04-ZR21', links='FR-V12-R-111…118; DEC-788')

# ----------------------------------------------------------------------------- render
def md_cell(s):
    return str(s).replace('|', '/').replace('\n', ' ')

summary = collections.OrderedDict()
tc = 101
frag_tc = []
frag_models = []
for mid, m in M.items():
    rows, nvalid, method, ntuples = covering(m['params'], m['constraint'], m['t'])
    names = list(m['params'])
    raw = 1
    for v in m['params'].values(): raw *= len(v)
    # also pairwise size for 3-way models (reported)
    pw = None
    if m['t'] == 3 and method != 'exhaustive':
        pw = len(covering(m['params'], m['constraint'], 2)[0])
    summary[mid] = dict(title=m['title'], cap=m['cap'], params=len(names), values=sum(len(v) for v in m['params'].values()),
                        raw=raw, valid=nvalid, method=method, tuples=ntuples, cases=len(rows), pairwise_cases=pw,
                        first_tc=f'TC-V12-R-{tc:03d}', last_tc=f'TC-V12-R-{tc+len(rows)-1:03d}')
    # parameter model fragment
    pm = [f"#### {mid} {m['title']}", '', f"Capability {m['cap']} · stories {m['story']} · traces {m['links']}", '',
          '| Parameter | Values | Count |', '|---|---|---|']
    for n, v in m['params'].items():
        pm.append(f'| `{n}` | ' + ' · '.join(md_cell(x) for x in v) + f' | {len(v)} |')
    pm += ['', f"Raw product {raw:,} · valid after constraints {nvalid:,} · method **{method}** "
           + (f"· {ntuples:,} valid {m['t']}-tuples · " if method != 'exhaustive' else '· ')
           + f"**{len(rows)} cases** ({summary[mid]['first_tc']}…{summary[mid]['last_tc']})"
           + (f" · pairwise alone would need {pw}" if pw else ''), '']
    frag_models.append('\n'.join(pm))
    # test-case fragment (parameterized form)
    out = [f"#### Group TC-V12-R-{mid}: {'Pairwise' if m['t']==2 else '3-way'} combinatorial cases – {m['title']}", '',
           f"**Common for {summary[mid]['first_tc']}…{summary[mid]['last_tc']}:** {m['common']} Links for every row: TS-V12-R-{mid[1:]} · {m['story']} · {m['links']}. Technique {'PW' if m['t']==2 else 'PW (3-way)'}{' and exhaustive' if method=='exhaustive' else ''}; generated by `assembly/v12b/R_02_combinatorics.py` (model {mid}).", '',
           '| ID | ' + ' | '.join(names) + ' | Expected result | P | Type | Tech | Auto | Lvl |',
           '|' + '---|' * (len(names) + 7)]
    for r in rows:
        exp, p, ty = m['oracle'](r)
        tech = 'PW' if m['t'] == 2 else 'PW3'
        if method == 'exhaustive': tech = 'EXH'
        out.append(f'| TC-V12-R-{tc:03d} | ' + ' | '.join(md_cell(r[n]) for n in names) + f' | {md_cell(exp)} | {p} | {ty} | {tech} | Y | {m["level"]} |')
        r['_tc'] = f'TC-V12-R-{tc:03d}'; r['_exp'] = exp
        tc += 1
    frag_tc.append('\n'.join(out) + '\n')
    m['rows'] = rows

open(OUT + '/models.md', 'w').write('\n'.join(frag_models))
open(OUT + '/tc_generated.md', 'w').write('\n'.join(frag_tc))

# Gherkin Examples blocks (first n rows per model) for Scenario Outlines in the stories
ex = {}
for mid, m in M.items():
    names = list(m['params'])
    lines = ['    Examples: ' + f'{mid} generated rows (see {summary[mid]["first_tc"]}…)',
             '      | ' + ' | '.join(names + ['tc', 'expected']) + ' |']
    for r in m['rows'][:12]:
        e = r['_exp']
        e = e.split(';')[0][:110]
        lines.append('      | ' + ' | '.join(md_cell(r[n]) for n in names) + f" | {r['_tc']} | {md_cell(e)} |")
    ex[mid] = '\n'.join(lines)
json.dump(ex, open(OUT + '/examples.json', 'w'), indent=0, ensure_ascii=False)
summary['_total_cases'] = tc - 101
summary['_last_tc'] = f'TC-V12-R-{tc-1:03d}'
json.dump(summary, open(BP + '/assembly/v12b/R_combinatorics_summary.json', 'w'), indent=1)
for k, v in summary.items():
    print(k, v if k.startswith('_') else (v['method'], v['valid'], v['cases'], v['pairwise_cases'], v['first_tc'], v['last_tc']))
