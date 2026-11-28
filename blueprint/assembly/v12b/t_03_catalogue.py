"""Group T (Part 11.21): master parameter catalogue and reference data (SKUs, roles, packs, locales).

Single source of truth for the parameter values used by every Part 11.21 model.  Values and rules
are taken from the cited blueprint parts; anything inferred is tagged in Part 11.21 (ASSUMPTION-1120…).
"""
import csv, glob, re, collections

BP = '/home/user/Allinonecalculator/blueprint'
SRC = '/tmp/claude-0/-home-user-Allinonecalculator/233b6551-af93-57f5-8f0b-015057ecee11/scratchpad/v12/src'

# ----------------------------------------------------------------------------- SKUs (39 + 24)
SM_FALLBACK = {}


def _read_index(pattern):
    out = collections.OrderedDict()
    files = glob.glob(SRC + '/' + pattern)
    if not files:
        return out
    for r in list(csv.reader(open(files[0], encoding='utf-8')))[4:]:
        if r and re.match(r'(SM|INV)-SVC-\d\d', r[0].strip()):
            out[r[0].strip()] = dict(name=r[1].strip(), family=r[2].strip(), bundle=r[3].strip(), meter=r[6].strip())
    return out


SM = _read_index('*39_Services*_csv/Service_Index.csv')
INV = _read_index('Investment*_csv/Service_Index.csv')
assert len(SM) == 39 and len(INV) == 24, (len(SM), len(INV))

# effect class of the SKU's consequential step (Part 11.17a §11.17.5.2; FSD 12 effect classes)
EFFECT = {}
for s in ['01', '02', '03', '04', '24', '25', '29', '34', '36']:
    EFFECT[s] = 'R0'
for s in ['05']:
    EFFECT[s] = 'R1'
for s in ['06', '07', '08', '09', '10', '11', '12', '13', '15', '16', '22', '23', '26', '27', '33', '35', '38']:
    EFFECT[s] = 'R2'
for s in ['14', '17', '18', '19', '20', '21', '28', '30', '31', '32', '37', '39']:
    EFFECT[s] = 'R3'
assert len(EFFECT) == 39

# mandate types per SKU (Part 11.17a §11.17.5.14 eligibility register)
MANDATE = {'06': 'MT-OUT', '07': 'MT-OUT', '09': 'MT-OUT', '10': 'MT-OUT', '12': 'MT-OUT', '16': 'MT-OUT',
           '11': 'MT-PUB', '13': 'MT-PUB', '14': 'MT-SPEND', '17': 'MT-COM', '18': 'MT-COM', '19': 'MT-BID',
           '20': 'MT-PROC/MT-PAY', '21': 'MT-COM', '28': 'MT-COM/MT-PAY', '30': 'MT-PRICE', '31': 'MT-COM/MT-PROC',
           '32': 'MT-PAY', '37': 'MT-PRICE', '39': 'MT-PROC/MT-PAY'}
L4_OK = {'06', '07', '09', '10', '12', '16', '28'}          # "L3 (L4 with plan)" rows of the register

# release in which the SKU's capability is first testable end to end (Part 11.10b §11.10.4.3; DEC-770)
REL_SKU = {}
for s in range(1, 40):
    k = '%02d' % s
    if s <= 16 or s == 25:
        REL_SKU[k] = 'R1'
    else:
        REL_SKU[k] = 'R2'

EPIC = {'01': 'EP-05', '02': 'EP-05', '03': 'EP-06', '04': 'EP-06', '05': 'EP-07', '06': 'EP-08', '07': 'EP-10',
        '08': 'EP-08', '09': 'EP-08', '10': 'EP-09', '11': 'EP-11', '12': 'EP-11', '13': 'EP-11', '14': 'EP-12',
        '15': 'EP-12', '16': 'EP-12', '17': 'EP-13', '18': 'EP-13', '19': 'EP-14', '20': 'EP-14', '21': 'EP-15',
        '22': 'EP-16', '23': 'EP-16', '24': 'EP-17', '25': 'EP-02', '26': 'EP-08', '27': 'EP-11', '28': 'EP-14',
        '29': 'EP-06', '30': 'EP-12', '31': 'EP-14', '32': 'EP-16', '33': 'EP-16', '34': 'EP-20', '35': 'EP-11',
        '36': 'EP-17', '37': 'EP-13', '38': 'EP-08', '39': 'EP-14'}

# ----------------------------------------------------------------------------- roles (Part 2.3 §2.26; Part 2.6 R21; Part 11.19 custom roles)
ROLES = collections.OrderedDict([
    ('R01', 'Founder / Portfolio Owner'), ('R02', 'Startup Head'), ('R03', 'Growth Manager'),
    ('R04', 'Research Analyst'), ('R05', 'Marketing Specialist'), ('R06', 'Bid Manager'),
    ('R07', 'Order Coordinator'), ('R08', 'Finance Maker'), ('R09', 'Finance Checker'),
    ('R10', 'Legal / Compliance / DPO'), ('R11', 'Automation Lead'), ('R12', 'Tenant Administrator'),
    ('R13', 'Platform Support (JIT grant)'), ('R14', 'Platform Billing'), ('R15', 'Auditor (read-only)'),
    ('R16', 'External Customer / Supplier (portal)'), ('R17', 'SaaS Client Applicant'),
    ('R18', 'Anonymous Visitor'), ('R19', 'Service Identity'), ('R20', 'AI Agent Identity'),
    ('R21', 'Managed-Service Operator (delegation grant)'), ('CUS', 'Custom role (Part 11.19)')])
ALL_SM = ['%02d' % i for i in range(1, 40)]
AI_SKUS = None  # filled from the EVAL register
ROLE_SKUS = {
    'R01': ALL_SM, 'R02': ALL_SM, 'R11': ALL_SM, 'R12': ALL_SM, 'R13': ALL_SM, 'R14': ALL_SM,
    'R15': ALL_SM, 'R17': ALL_SM, 'R19': ALL_SM, 'CUS': ALL_SM,
    'R03': ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '17', '22', '23', '26', '29', '32', '33', '36', '38'],
    'R04': ['01', '02', '03', '04', '24', '25', '29', '34'],
    'R05': ['11', '12', '13', '14', '15', '16', '27', '30', '35'],
    'R06': ['02', '19'],
    'R07': ['20', '28', '31', '39'],
    'R08': ['14', '20', '21', '24', '28', '32', '37', '39'],
    'R09': ['14', '20', '21', '24', '28', '32', '37', '39'],
    'R10': ['06', '07', '11', '13', '14', '15', '17', '18', '19', '25', '26', '27', '35', '38'],
    'R16': ['10', '17', '18', '20', '21', '22', '23', '33'],
    'R18': ['09', '10', '15', '16', '33'],
    'R21': ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '15', '16', '22', '23', '24', '29', '30', '33', '35', '38'],
}
ROLE_ACTION = {
    'R01': 'runs and approves (all startups; mutation per selected startup)', 'R02': 'approves as Startup Head',
    'R03': 'runs the workflow and submits for approval', 'R04': 'runs research and reviews evidence',
    'R05': 'authors; R05L approves content and campaigns', 'R06': 'prepares the bid package',
    'R07': 'coordinates the order, PO or commerce case', 'R08': 'makes the financial entry (maker)',
    'R09': 'checks the financial entry (checker, ≠ maker)', 'R10': 'reviews claims, legal and privacy',
    'R11': 'configures the workflow (cannot loosen caps)', 'R12': 'configures entitlement, users and templates (not a business approver)',
    'R13': 'reads run metadata under an active, time-boxed JIT grant', 'R14': 'reads meters and invoices only (no business content)',
    'R15': 'reads runs, evidence and audit (read-only)', 'R16': 'completes the portal step on own records (object grant)',
    'R17': 'purchases the SKU on the public website', 'R18': 'submits the public intake / chat / booking step',
    'R19': 'calls the API or delivers the event (least-privilege scope)', 'R20': 'executes the AI step through registered tools only (never approves)',
    'R21': 'operates inside the client tenant under an active delegation grant', 'CUS': 'acts with the custom role permission set (SoD rules enforced)'}
ADMIN_ROLES = ['R01', 'R02', 'R03', 'R04', 'R05', 'R06', 'R07', 'R08', 'R09', 'R10', 'R11', 'R12', 'R13', 'R14', 'R15', 'R21', 'CUS']

# ----------------------------------------------------------------------------- the other catalogue dimensions
TENANTS = ['T1-AppNAI', 'T1-MedMaarg', 'T1-EduVerse', 'T1-OrganicSpec', 'EXT-SMB', 'EXT-ENT', 'EXT-MSP']
TENANT_TEXT = {'T1-AppNAI': 'Owner Portfolio tenant T1, startup AppNAI', 'T1-MedMaarg': 'T1, startup MedMaarg (no patient data)',
               'T1-EduVerse': 'T1, startup EduVerse (no outreach to minors)', 'T1-OrganicSpec': 'T1, startup OrganicSpec (receivable and payable ledgers)',
               'EXT-SMB': 'external SaaS tenant, self-service', 'EXT-ENT': 'external SaaS tenant, enterprise (SSO/SCIM)',
               'EXT-MSP': 'external SaaS tenant served by a managed-service operator (R21)', 'INV-T': 'Investment Automation tenant (issuer company)'}
PLANS = ['FULL', 'BUNDLE', 'SELECT', 'TRIAL']
PLAN_TEXT = {'FULL': 'full suite (39 SKUs)', 'BUNDLE': 'partial bundle containing the SKU', 'SELECT': 'selective single-SKU subscription',
             'TRIAL': 'trial/sandbox plan (simulation only)'}
REGIONS = ['IN', 'EU']
ZONE = {'IN': 'IN zone (Mumbai: Supabase ap-south-1, AWS ap-south-1, Vercel bom1; verify region codes)',
        'EU': 'EU zone (Frankfurt: Supabase eu-central-1, AWS eu-central-1, Vercel fra1; verify region codes)'}
LOCALES = ['en-IN', 'hi-IN', 'ta-IN', 'or-IN', 'en-GB', 'de-DE', 'fr-FR', 'ar-AE']
LOCALE_REL = {'en-IN': 'R1', 'en-GB': 'R1', 'hi-IN': 'R2', 'ta-IN': 'R2', 'or-IN': 'R2', 'de-DE': 'R3', 'fr-FR': 'R3', 'ar-AE': 'R4',
              'bn-IN': 'R3', 'en-US': 'R3'}
LOCALE_ZONE = {'IN': ['en-IN', 'hi-IN', 'ta-IN', 'or-IN', 'ar-AE'], 'EU': ['en-GB', 'de-DE', 'fr-FR', 'ar-AE']}
CHANNELS = ['Admin web', 'Admin mobile web', 'Public website', 'Portal', 'Developer API', 'Event/webhook', 'Agent tool call']
UI_CHANNELS = {'Admin web', 'Admin mobile web', 'Public website', 'Portal'}
IDENTITIES = ['Password + MFA', 'SSO SAML', 'SSO OIDC', 'API key', 'OAuth client credentials', 'Signed webhook', 'Workload identity', 'Anonymous session']
DATA = ['Public', 'Internal', 'Personal', 'Confidential', 'Restricted']
CONSENT = ['Opt-in recorded', 'Legitimate interest + LIA', 'Contract / transactional', 'Not applicable']
PROVIDER = ['Available', 'Throttled (429)', 'Timeout after submit', 'Down before submit']
AUTONOMY = ['L0', 'L1', 'L2', 'L3', 'L4']
AI_ROUTE = ['Claude Sonnet (registry primary)', 'Lighter Claude tier (Tier 1a)', 'Open-weight in zone (masked)', 'Tier 2 free fallback (opt-in)', 'Tier 3 degrade (rules/cache)']
DEVICES = ['Desktop 1440', 'Laptop 1280', 'Tablet 768', 'Mobile 390', 'Mobile 320', 'Headless']
BROWSERS = ['Chrome', 'Edge', 'Firefox', 'Safari', 'Headless']
SLA = ['Standard 99.5%', 'Business 99.9%', 'Enterprise 99.95%']
REL_ORDER = {'R1': 1, 'R2': 2, 'R3': 3, 'R4': 4}


def rel_max(*rs):
    return max(rs, key=lambda r: REL_ORDER[r])


def load_eval_suites():
    rows = []
    f = glob.glob(BP + '/Part-11-6b_*.md')[0]
    for line in open(f, encoding='utf-8'):
        if re.match(r'^\| TC-V12-F-[23]\d\d \| EVAL-', line):
            c = [x.strip() for x in line.strip().strip('|').split('|')]
            rows.append(dict(tc=c[0], suite=c[1], workflow=c[2], ai_steps=c[3], agt=c[4], agents=c[5], gates=c[6],
                             cases=c[7], langs=c[8]))
    assert len(rows) == 111, len(rows)
    return rows


EVAL = load_eval_suites()
AI_SKUS = sorted({re.search(r'SM-SVC-(\d\d)', r['suite']).group(1) for r in EVAL})

# ----------------------------------------------------------------------------- catalogue table for the part text
CATALOGUE = [
    ('P-01', 'Tenant type', 'TEN', TENANTS + ['INV-T'], 'Part 1 personas; DEC-002 as amended by DEC-783; Part 2.6 R21; DEC-784', 'Owner Portfolio startups carry vertical rules (MedMaarg no patient data; EduVerse no outreach to minors; OrganicSpec separate ledgers)'),
    ('P-02', 'Plan / subscription', 'PLAN', PLANS + ['INV plan', '~SKU not in plan', '~Subscription suspended'], 'Part 11.2 entitlement engine; Workbook Entitlement_Rules; DEC-770', 'Values with ~ are invalid (negative) values'),
    ('P-03', 'SKU', 'SKU', ['SM-SVC-01…39 (39)', 'INV-SVC-01…24 (24)'], 'Service_Index.csv (both catalogues); Part 11.2a; Parts 11.16a–d', 'Each SKU carries effect class R0–R3, mandate types, meter unit, epic and first release'),
    ('P-04', 'Jurisdiction (recipient / counterparty / market)', 'JUR', ['IN', 'EU-DE', 'EU-FR', 'UK', 'US', 'AE', 'SG', '~not enabled (e.g. BR)'], 'Part 11.15 rule packs; DEC-776; DEC-029 as amended', 'Activation requires an Approved pack per jurisdiction ("where lawful")'),
    ('P-05', 'Residency region (zone)', 'REG', REGIONS + ['~UK/ME/APAC/US zone not provisioned'], 'DEC-772, DEC-776, DEC-786, DEC-787', 'Chosen at onboarding; never written to the other zone (CJ-TC-09)'),
    ('P-06', 'Locale', 'LOC', LOCALES + ['bn-IN', 'en-US', '~unsupported (xx-YY)'], 'DEC-026/404 as amended by DEC-776; Part 11.7c CONFLICT-872', 'ar-AE is right-to-left (R4); de-DE and fr-FR from R3; hi-IN, ta-IN, or-IN from R2'),
    ('P-07', 'Role', 'ROLE', list(ROLES) + ['~role without permission', '~R21 without active grant', '~SCIM de-provisioned user'], 'Part 2.3 §2.26; Part 2.6 (R21); Part 11.19 custom roles and SoD', 'R20 never approves; R15 never mutates; R14 never sees business content'),
    ('P-08', 'Channel / surface', 'CHN', CHANNELS + ['Email', 'WhatsApp', 'SMS/RCS', 'Voice', 'Agent-to-agent (SVC-28)'], 'Part 2.5; Part 11.7; Part 11.8; Parts 11.17–11.18', 'First seven are request surfaces (PM-T01); the last five are effect channels (PM-T03)'),
    ('P-09', 'Autonomy level / mandate state', 'AUT', AUTONOMY + ['~L2 payload changed', '~L2 approval expired', '~mandate Suspended', '~mandate Revoked', '~mandate Exhausted', '~L4 step outside plan graph', '~kill switch engaged'], 'Part 11.17a §11.17.5.2/5.8; DEC-779', 'L3 needs an Active two-person mandate; L4 needs a plan-bound L3 mandate'),
    ('P-10', 'Data class', 'DAT', DATA + ['Personal (masked)', '~Prohibited (patient health data, personal data of a minor)'], 'Part 3.3; Part 11.19b registry; DEC-788', 'Tier 2 free fallback: Public / Internal non-personal only, opt-in, default off'),
    ('P-11', 'Consent / lawful basis', 'CON', CONSENT + ['~Withdrawn / opted out', '~Unknown', '~Registry/DND-listed'], 'BRL-ELG; Part 11.15 RP-IN-DPDP, RP-EU-MKT, RP-IN-SMS', 'Rechecked by the PDP at dispatch'),
    ('P-12', 'Provider state', 'PRV', PROVIDER + ['~live key outside prod'], 'FR-ADP-01; FR-STD-02; NFR-005/007/026', 'Timeout after submit = Uncertain; reconcile before any retry'),
    ('P-13', 'AI route (model registry row)', 'AIR', AI_ROUTE + ['~unapproved candidate', '~Tier 2 with personal data'], 'DEC-788; Part 11.19b; Part 7.3 tiers', 'Claude Sonnet is the registry-approved primary'),
    ('P-14', 'Device / viewport', 'DEV', DEVICES, 'Part 2.5; DEC-043; WCAG 2.2 1.4.10 reflow (320 CSS px)', 'Headless = API or event surface'),
    ('P-15', 'Browser', 'BRW', BROWSERS + ['~unsupported legacy browser'], 'DEC-043 (last two versions)', 'Playwright projects Chromium, Firefox, WebKit; Edge channel'),
    ('P-16', 'SLA tier', 'SLA', SLA, 'DEC-774; Part 11.11b', 'Credit ladder per tier'),
    ('P-17', 'Identity method', 'IDN', IDENTITIES + ['~MFA older than policy for privileged action', '~revoked or expired credential'], 'DEC-784/785; Part 11.19a', 'SAML for EXT-ENT, EXT-MSP and T1 only'),
    ('P-18', 'Value vs cap', 'VAL', ['below per-action cap', 'exactly at cap', '~above per-action cap', '~crosses aggregate cap'], 'Part 11.17a §11.17.5.6; DEC-038', 'Caps are inclusive [ASSUMPTION-1121]'),
    ('P-19', 'Rule-pack state', 'PCK', ['Approved', '~Draft', '~In counsel review', '~Suspended', '~Expired', '~Withdrawn'], 'Part 11.15 §11.15.3.5; CJ-R19/R20', 'Only Approved packs activate a capability'),
    ('P-20', 'Kill switch', 'KS', ['off', '~mandate scope', '~tenant scope', '~platform scope'], 'Part 11.17a §11.17.5.13', 'Tightening is immediate'),
    ('P-21', 'Time window (recipient local)', 'WIN', ['09:00:00', '20:59:59', '~08:59:59', '~21:00:00', '~restricted day per pack'], 'DEC-777; Part 11.15 packs', 'Stricter pack wins; transactional messages exempt'),
    ('P-22', 'Currency', 'CUR', ['INR', 'EUR', 'GBP', 'USD', 'AED', 'SGD'], 'NFR-017; DEC-776 tax engine', 'Decimal amounts + ISO 4217'),
    ('P-23', 'Assistive technology', 'AT', ['keyboard only', 'NVDA + Chrome', 'JAWS + Edge', 'VoiceOver + Safari (macOS)', 'VoiceOver (iOS)', 'TalkBack (Android)', 'voice control'], 'WCAG 2.2 AA; Part 2.5 §2.46', 'Manual passes PP-07'),
    ('P-24', 'Theme / display', 'THM', ['light', 'dark', 'forced colors (high contrast)', 'reduced motion'], 'WCAG 2.2 1.4.3/1.4.11/2.3.3', ''),
    ('P-25', 'Load profile', 'LOAD', ['baseline', 'Year-2 peak', '10× pilot', 'stress 3×', 'spike 10× burst', 'soak 24 h / 72 h'], 'Part 6.1 §6.1.14.1 LT-01…12', 'New LT-13…24 in §11.21.3.4'),
    ('P-26', 'Failure mode', 'FAIL', ['AZ loss', 'queue/cache loss', 'worker crash mid-dispatch', 'Vercel function region outage', 'Supabase project unavailable', 'model provider outage', 'PSP outage', 'CPaaS outage', 'email/SMS provider outage', 'KMS key unavailable'], 'DEC-771/787; Part 11.19b DR-R1…R8', 'RTO ≤ 120 min, RPO ≤ 15 min'),
]
