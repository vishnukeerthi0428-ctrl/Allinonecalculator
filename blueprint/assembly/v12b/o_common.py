"""Shared helpers and ID allocation for the Group O builders."""
import json, re, sys
sys.path.insert(0, '/home/user/Allinonecalculator/blueprint/assembly/v12b')
from o_02_model import SVC, WF, AG, AU, SCR_A, SCR_W, ENT, PACKS, SEC_PACKS

BP = '/home/user/Allinonecalculator/blueprint/'
D = json.load(open(BP + 'assembly/v12b/o_data.json'))
C = json.load(open(BP + 'assembly/v12b/o_combi.json'))
OURS = [f'INV-SVC-{n:02d}' for n in range(13, 25)]

def cell(s):
    s = '' if s is None else str(s)
    s = s.replace('\r', '').replace('\n', '<br/>').replace('|', '/')
    parts = s.split('`')
    for i in range(0, len(parts), 2):
        parts[i] = parts[i].replace('$', '\\$')
    return '`'.join(parts).strip()

def tbl(header, rows):
    out = ['| ' + ' | '.join(header) + ' |', '|' + '|'.join(['---'] * len(header)) + '|']
    for r in rows:
        out.append('| ' + ' | '.join(cell(x) for x in r) + ' |')
    return '\n'.join(out)

SC = {r['Automation ID']: r for r in D['Service_Catalog.csv']['rows']}
WFROWS = {}
for r in D['Workflow_Catalog.csv']['rows']:
    wid = r['Sub-automation name'].split(' — ')[0].strip()
    WFROWS[wid] = r
SI = {r['Service ID']: r for r in D['Service_Index.csv']['rows']}
ER = {r['Service ID']: r for r in D['Entitlement_Rules.csv']['rows']}
MG = {r['Service ID']: r for r in D['Migration.csv']['rows']}
CM = {r['Workflow ID']: r for r in D['Cost_Model.csv']['rows']}
AT = {r['Test ID']: r for r in D['Acceptance_Tests.csv']['rows']}
TM = {}
for r in D['Technical_Map.csv']['rows']:
    TM.setdefault(r['Service ID'], []).append(r)

def wf_ids(s):
    return [f'{s}-WF0{i}' for i in range(1, 5)]

def wf_name(w):
    return WFROWS[w]['Sub-automation name'].split(' — ', 1)[1].strip()

# ---------------- ID allocation (deterministic)
FR = {}
n = 13
for s in OURS:
    FR[s] = [f'FR-V12-O-{n:03d}', f'FR-V12-O-{n + 1:03d}']
    n += 2
for s in OURS:
    for w in wf_ids(s):
        FR[w] = f'FR-V12-O-{n:03d}'
        n += 1
PACK_FR = {}
for p in PACKS:
    PACK_FR[p] = f'FR-V12-O-{n:03d}'
    n += 1
PLAT_FR_START = n  # platform FRs follow

# workflow tests: 8 per workflow, then step tests
TCW = {}
t = 1
for s in OURS:
    for w in wf_ids(s):
        TCW[w] = [f'TC-V12-O-{t + i:03d}' for i in range(8)]
        t += 8
TC_NEXT = [t]

def next_tc():
    v = TC_NEXT[0]
    TC_NEXT[0] += 1
    return f'TC-V12-O-{v:03d}'

def steps_of(w):
    txt = WFROWS[w]['Workflow steps']
    parts = [p.strip() for p in re.split(r';\s*', txt) if p.strip()]
    return parts

def cost(w):
    r = CM[w]
    return float(r['Internal INR / invocation']), int(r['Input tokens (scenario)']), int(r['Output tokens (scenario)']), r['Unit'], r['External fees']

STORIES = {
 'US-32-ZO01': ('EP-32', 'Closing readiness and authorised closing record', 'INV-SVC-13 WF01/WF02', 'M-O2'),
 'US-32-ZO02': ('EP-32', 'Statutory filing tasks and regulatory deadline monitoring', 'INV-SVC-13 WF03/WF04', 'm-filings'),
 'US-32-ZO03': ('EP-32', 'Investor update with figure tie-out and rights-scoped dispatch', 'INV-SVC-14 WF03/WF04', 'M-O8'),
 'US-32-ZO04': ('EP-32', 'Investor onboarding, obligations and use-of-funds milestones', 'INV-SVC-14 WF01/WF02', 'm-obligations'),
 'US-32-ZO05': ('EP-32', 'Fundraising pipeline stage gates and next actions', 'INV-SVC-15 WF01/WF02', 'M-O9'),
 'US-32-ZO06': ('EP-32', 'Probability-weighted forecast and bottleneck analytics', 'INV-SVC-15 WF03/WF04', 'm-forecast'),
 'US-32-ZO07': ('EP-32', 'Signed private enquiry intake and routing', 'INV-SVC-16 WF01/WF02', 'M-O10'),
 'US-32-ZO08': ('EP-32', 'Intake health monitoring and external AI-agent intake', 'INV-SVC-16 WF03/WF04', 'm-intakehealth'),
 'US-32-ZO09': ('EP-32', 'Single-SKU entitlement isolation for INV-SVC-13…24', 'INV-SVC-13…24 ENT-AT01', 'M-O16'),
 'US-32-ZO10': ('EP-32', 'Investor portal: offer letter, application, payment instructions and holdings', 'W77–W84', 'm-portal'),
 'US-33-ZO01': ('EP-33', 'Grant eligibility, drafting and submission readiness', 'INV-SVC-17 WF01–WF03', 'M-O11'),
 'US-33-ZO02': ('EP-33', 'Grant utilisation and milestone reporting', 'INV-SVC-17 WF04', 'm-grantutil'),
 'US-33-ZO03': ('EP-33', 'Debt readiness, dossier, scenarios and covenant monitoring', 'INV-SVC-18 WF01–WF04', 'M-O12'),
 'US-33-ZO04': ('EP-33', 'Continuous readiness, burn and runway', 'INV-SVC-19 WF01–WF04', 'M-O13'),
 'US-33-ZO05': ('EP-33', 'Cap-table reconciliation and authorised ownership change', 'INV-SVC-20 WF01/WF04', 'M-O3'),
 'US-33-ZO06': ('EP-33', 'ESG evidence and impact disclosure release', 'INV-SVC-21 WF01–WF04', 'M-O14'),
 'US-33-ZO07': ('EP-33', 'Cross-border requirement matrix and restriction routing', 'INV-SVC-22 WF01–WF04', 'M-O6'),
 'US-33-ZO08': ('EP-33', 'Dilution and instrument scenario modelling', 'INV-SVC-20 WF02/WF03', 'm-instruments'),
 'US-33-ZO09': ('EP-33', 'Board and shareholder meetings, notice, quorum and voting', 'INV-SVC-23 WF01/WF02', 'M-O4'),
 'US-33-ZO10': ('EP-33', 'Decision tracking and governance information packs', 'INV-SVC-23 WF03/WF04', 'm-govpack'),
 'US-33-ZO11': ('EP-33', 'Investor verification and screening hand-off', 'INV-SVC-24 WF01–WF04; RP-AML-KYC', 'M-O5'),
 'US-33-ZO12': ('EP-33', 'Securities rule-pack registry, counsel sign-off and activation', 'All seven packs; A254/A258', 'M-O15'),
 'US-33-ZO13': ('EP-33', 'Offer eligibility ledger and solicitation gate', 'RP-IN-SEC, RP-US-REGD, RP-US-REGCF, RP-EU-PROSP, RP-UK-FINPROM', 'M-O1'),
 'US-33-ZO14': ('EP-33', 'Financial promotion review and legends', 'AG-198; AU-258', 'm-promo'),
 'US-33-ZO15': ('EP-33', 'No personalised investment advice by AI', 'RP-INV-ADVICE; AG-199; AU-257', 'M-O7'),
}

# mini exhaustive models for stories without a main model
def _mini():
    import itertools
    mm = {}
    def add(mid, title, params, oracle):
        names = list(params)
        rows = [dict(zip(names, v)) for v in itertools.product(*[params[k] for k in names])]
        cases = []
        for i, r in enumerate(rows, 1):
            e, rl = oracle(r)
            cases.append(dict(id=f'TC-V12-O-{mid}-{i:03d}', row=r, expected=e, rules=rl))
        mm[mid] = dict(id=mid, title=title, t='exhaustive', params=params, full=len(rows), valid=len(rows), method='exhaustive', n=len(rows), cases=cases, added=0)
    def f_fil(r):
        J, ev = r['jurisdiction'], r['event']
        m = {('IN', 'allotment'): ('TASK PAS-3 due allotment+15d', 'RP-IN-SEC-013'), ('IN', 'nonresident_issue'): ('TASK FC-GPR due issue+30d', 'RP-IN-SEC-017'),
             ('IN', 'first_sale'): ('NO_TASK (IN uses allotment)', 'RP-IN-SEC-013'), ('US', 'first_sale'): ('TASK Form D due first_sale+15d; state notices', 'RP-US-REGD-009'),
             ('US', 'allotment'): ('TASK board consent record only', 'RP-US-REGD-009'), ('US', 'nonresident_issue'): ('HOLD counsel (Reg S)', 'RP-US-REGD-001'),
             ('UK', 'allotment'): ('TASK SH01 due allotment+1 month', 'RP-UK-FINPROM-010'), ('UK', 'first_sale'): ('NO_TASK', 'RP-UK-FINPROM-010'),
             ('UK', 'nonresident_issue'): ('TASK SH01 due allotment+1 month', 'RP-UK-FINPROM-010')}
        return m[(J, ev)]
    add('m-filings', 'Statutory filing task derivation', {'jurisdiction': ['IN', 'US', 'UK'], 'event': ['allotment', 'first_sale', 'nonresident_issue']}, f_fil)
    add('m-obligations', 'Obligation tasking', {'obligation': ['information_right', 'board_seat', 'consent_right', 'reporting_covenant'], 'owner': ['assigned', 'missing']},
        lambda r: ('TASK_CREATED', 'INV-SVC-14 WF01') if r['owner'] == 'assigned' else ('UNASSIGNED_TASK_TO_R02_WITHIN_1BD', 'INV-SVC-14 WF01'))
    add('m-forecast', 'Forecast inputs', {'history': ['ge_30_closed', 'lt_30_closed'], 'currency': ['single', 'mixed'], 'fx': ['snapshot', 'none']},
        lambda r: ('HOLD AGGREGATION_FX', 'BRL-V12-O-04') if (r['currency'] == 'mixed' and r['fx'] == 'none') else (('FORECAST TENANT_CALIBRATED', 'AU-243') if r['history'] == 'ge_30_closed' else ('FORECAST DOCUMENTED_PRIORS_FLAGGED', 'AU-243')))
    def f_ih(r):
        if r['source'] == 'external_agent' and r['mandate'] == 'none':
            return 'REJECT AGENT_MANDATE', 'AU-245'
        if r['schema'] == 'drift' or r['failure_rate'] == 'ge_5pct':
            return 'PAUSE_ENDPOINT NOTIFY_OWNER', 'AU-244'
        return 'HEALTHY', 'AU-244'
    add('m-intakehealth', 'Intake health and agent intake', {'failure_rate': ['lt_5pct', 'ge_5pct'], 'schema': ['same', 'drift'], 'source': ['issuer_form', 'external_agent'], 'mandate': ['active', 'none']}, f_ih)
    def f_portal(r):
        J, s = r['jurisdiction'], r['screen']
        if s == 'W80':
            return {'IN': ('SHOW PAS-4 BY NAME', 'RP-IN-SEC-005/006'), 'US': ('SHOW SUBSCRIPTION DOCS + 502(d) LEGEND', 'RP-US-REGD-011'),
                    'EU': ('SHOW EXEMPT LEGEND TPL-EU-PROSP-02', 'RP-EU-PROSP-009'), 'UK': ('SHOW FPO INDICATIONS', 'RP-UK-FINPROM-007')}[J]
        if s == 'W83':
            return ('OWN-ACCOUNT BANK TRANSFER ONLY TPL-IN-SEC-03', 'RP-IN-SEC-009') if J == 'IN' else ('BANK TRANSFER; CARD DISABLED', 'RP-AML-KYC-003')
        return ('HOLDING STATEMENT WITH LEGEND', 'RP-US-REGD-011') if J == 'US' else ('HOLDING STATEMENT', 'ADR-239')
    add('m-portal', 'Investor portal rendering per jurisdiction', {'jurisdiction': ['IN', 'US', 'EU', 'UK'], 'screen': ['W80', 'W83', 'W84']}, f_portal)
    def f_gu(r):
        if r['spend'] == 'ineligible':
            return 'FLAG INELIGIBLE_SPEND', 'AU-246'
        if r['spend'] == 'unmatched':
            return 'FLAG UNMATCHED_SPEND', 'AU-246'
        if r['milestone'] == 'overdue':
            return 'EXCEPTION MILESTONE', 'AU-241'
        return ('REPORT_READY HUMAN_SUBMITS', 'INV-SVC-17 WF04') if r['approval'] == 'yes' else ('HOLD OWNER_APPROVAL', 'INV-SVC-17 WF04')
    add('m-grantutil', 'Grant utilisation', {'spend': ['matched', 'unmatched', 'ineligible'], 'milestone': ['on_time', 'overdue'], 'approval': ['yes', 'no']}, f_gu)
    add('m-instruments', 'Instrument scenario inputs', {'instrument': ['pre_money_safe', 'post_money_safe', 'convertible_note', 'ccps', 'esop'], 'term_confirmed': ['yes', 'no']},
        lambda r: ('CALCULATE GOLDEN_FIXTURE_MATCH', 'AU-251') if r['term_confirmed'] == 'yes' else ('EXCLUDE AMBIGUOUS_TERM', 'AU-251; AG-192'))
    def f_gp(r):
        if r['content'] == 'includes_unapproved':
            return 'BLOCK UNAPPROVED_CONTENT', 'INV-SVC-23 WF04'
        if r['redaction'] == 'missing':
            return 'BLOCK REDACTION', 'INV-SVC-23 WF04'
        return ('ROUTE AG-198_SECURITIES_REVIEW', 'AU-232') if r['offer_material'] == 'yes' else ('RELEASE_AFTER_OWNER_APPROVAL', 'INV-SVC-23 WF04')
    add('m-govpack', 'Governance information pack', {'content': ['approved_only', 'includes_unapproved'], 'redaction': ['applied', 'missing'], 'offer_material': ['no', 'yes']}, f_gp)
    def f_pr(r):
        if r['finding'] == 'block':
            return 'RETURN_TO_AUTHOR', 'AG-198'
        if r['legend'] == 'missing':
            return 'BLOCK LEGEND_MISSING', 'AU-258'
        return 'QUEUE_FOR_R10_APPROVAL', 'A256'
    add('m-promo', 'Financial promotion review', {'jurisdiction': ['IN', 'US', 'EU', 'UK'], 'legend': ['present', 'missing'], 'finding': ['none', 'block']}, f_pr)
    return mm
MINI = _mini()
ALLMODELS = {m['id']: m for m in C}
ALLMODELS.update(MINI)
