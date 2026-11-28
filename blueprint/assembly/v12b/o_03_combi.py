"""Group O combinatorial test design (Part 11.16d).
Generates t-way covering arrays (greedy, deterministic) over constrained parameter models, or exhaustive
enumeration where the valid space is <= 64, and computes the expected outcome of every row with an
oracle that IS the deterministic rule logic of the securities packs and services (so expected results are
derived from the rules, never typed by hand). Output: assembly/v12b/o_combi.json"""
import itertools, json

def covering(params, t, valid):
    names = list(params)
    full = [dict(zip(names, vals)) for vals in itertools.product(*[params[n] for n in names])]
    cand = [r for r in full if valid(r)]
    if len(cand) <= 64:
        return full, cand, cand, 'exhaustive'
    # all t-tuples that occur in at least one valid row must be covered
    need = set()
    for r in cand:
        for combo in itertools.combinations(names, t):
            need.add(tuple((n, r[n]) for n in combo))
    chosen = []
    keys = [[tuple((n, r[n]) for n in combo) for combo in itertools.combinations(names, t)] for r in cand]
    while need:
        best, bi = -1, None
        for i, ks in enumerate(keys):
            g = sum(1 for k in ks if k in need)
            if g > best:
                best, bi = g, i
        chosen.append(cand[bi])
        for k in keys[bi]:
            need.discard(k)
    return full, cand, chosen, f'{t}-way greedy covering array'

M = []
def model(mid, title, cap, t, params, valid, oracle, story):
    M.append(dict(id=mid, title=title, cap=cap, t=t, params=params, valid=valid, oracle=oracle, story=story))

# ---------------- M-O1 securities offer gate (3-way)
def v1(r):
    return True
def o1(r):
    J, route, inv, pack, kyc, head, ver = r['jurisdiction'], r['route'], r['investor'], r['pack_state'], r['kyc'], r['headroom'], r['status_evidence']
    if pack != 'active':
        return 'BLOCK PACK_NOT_ACTIVE', 'AU-231; CP-05'
    if kyc == 'possible_match':
        return 'HOLD SANCTIONS_REVIEW', 'AU-256; RP-AML-KYC-005'
    if kyc in ('pending', 'expired'):
        return 'HOLD KYC_NOT_CLEAR', 'AU-255; RP-AML-KYC-003'
    if route == 'portal_crowdfunding':
        return {'US': ('HANDOFF REGCF_INTERMEDIARY', 'RP-US-REGCF-001/002'), 'EU': ('HANDOFF ECSP_PROVIDER', 'RP-EU-PROSP-012'),
                'IN': ('BLOCK NO_CROWDFUNDING_ROUTE', 'RP-IN-SEC-019'), 'UK': ('HANDOFF FCA_AUTHORISED_PLATFORM', 'RP-UK-FINPROM-012')}[J]
    if route == 'general_solicitation':
        if J == 'IN':
            return 'BLOCK PUBLIC_ADVERTISEMENT', 'RP-IN-SEC-004'
        if J == 'US':
            if inv == 'qualified' and ver == 'verified':
                return 'ALLOW 506C_VERIFIED', 'RP-US-REGD-005/006'
            return 'BLOCK 506C_VERIFICATION_REQUIRED', 'RP-US-REGD-002/006'
        if J == 'EU':
            return 'BLOCK PROSPECTUS_OR_EXEMPTION_REQUIRED', 'RP-EU-PROSP-001/008'
        return 'BLOCK S21_APPROVAL_REQUIRED', 'RP-UK-FINPROM-001/002'
    # private_named
    if J == 'IN':
        if inv in ('qualified', 'employee_esop'):
            return 'ALLOW NOT_COUNTED', 'RP-IN-SEC-002/003'
        if head == 'at_limit':
            return 'BLOCK OFFEREE_LIMIT_200', 'RP-IN-SEC-002; AU-230'
        return 'ALLOW COUNTED', 'RP-IN-SEC-002; AU-230'
    if J == 'US':
        if inv == 'qualified':
            return 'ALLOW 506B_ACCREDITED', 'RP-US-REGD-003/004'
        if head == 'at_limit':
            return 'BLOCK NON_ACCREDITED_LIMIT_35', 'RP-US-REGD-004; AU-230'
        return 'ALLOW 506B_NONACCREDITED_WITH_DISCLOSURE', 'RP-US-REGD-004/008'
    if J == 'EU':
        if inv == 'qualified':
            return 'ALLOW QUALIFIED_INVESTOR_EXEMPTION', 'RP-EU-PROSP-002'
        if head == 'at_limit':
            return 'BLOCK 150_PERSON_LIMIT', 'RP-EU-PROSP-003; AU-230'
        return 'ALLOW UNDER_150_EXEMPTION', 'RP-EU-PROSP-003'
    if inv == 'qualified':
        return 'ALLOW FPO_ART19_PROFESSIONAL', 'RP-UK-FINPROM-003'
    if inv == 'hnw_or_sophisticated':
        if ver == 'none':
            return 'HOLD INVESTOR_STATEMENT_MISSING', 'RP-UK-FINPROM-004/005'
        return 'ALLOW FPO_ART48_50A_STATEMENT', 'RP-UK-FINPROM-004/005'
    if inv == 'employee_esop':
        return 'ALLOW FPO_ART60_EMPLOYEE_SCHEME', 'RP-UK-FINPROM-006'
    return 'BLOCK NO_FPO_EXEMPTION', 'RP-UK-FINPROM-001'
model('M-O1', 'Securities offer and solicitation gate', 'RP-IN-SEC, RP-US-REGD, RP-US-REGCF, RP-EU-PROSP, RP-UK-FINPROM, RP-AML-KYC; AU-230/231/232/255/256', 3,
      {'jurisdiction': ['IN', 'US', 'EU', 'UK'], 'route': ['private_named', 'general_solicitation', 'portal_crowdfunding'],
       'investor': ['retail', 'qualified', 'hnw_or_sophisticated', 'employee_esop'], 'pack_state': ['active', 'draft', 'expired'],
       'kyc': ['clear', 'pending', 'possible_match', 'expired'], 'headroom': ['below', 'at_limit'],
       'status_evidence': ['verified', 'self_declared', 'none']}, v1, o1, 'US-33-ZO13')

# ---------------- M-O2 closing (3-way)
def o2(r):
    if r['pack_state'] != 'active':
        return 'BLOCK PACK_NOT_ACTIVE', 'AU-231'
    if r['event'] == 'replay':
        return 'RETURN_ORIGINAL NO_NEW_RECORD', 'AU-239'
    if r['receipt'] == 'cash_or_third_party':
        return 'HOLD FUNDS_NOT_FROM_INVESTOR_BANK_ACCOUNT', 'AU-235; RP-IN-SEC-009'
    if r['receipt'] == 'partial':
        return 'HOLD AMOUNT_MISMATCH', 'AU-238; BRL-V12-O-01'
    if r['kyc'] != 'clear':
        return 'HOLD KYC_NOT_CLEAR', 'AU-255'
    if r['approvals'] != 'legal_and_finance':
        return 'HOLD TWO_APPROVALS_REQUIRED', 'AU-238; BRL-APR-01'
    if r['jurisdiction'] == 'IN' and r['clock'] == 'day_61_75':
        return 'BLOCK ALLOTMENT_WINDOW_CLOSED REFUND_WITH_INTEREST_DUE', 'AU-236; RP-IN-SEC-011'
    if r['jurisdiction'] == 'IN' and r['clock'] == 'beyond_75':
        return 'ESCALATE REFUND_OVERDUE', 'AU-236; RP-IN-SEC-011'
    return 'ALLOW CLOSING_RECORD_AND_FILING_TASKS', 'AU-238; AU-237'
model('M-O2', 'Closing and allotment gate', 'INV-SVC-13 WF01–WF04', 3,
      {'jurisdiction': ['IN', 'US', 'UK', 'EU'], 'receipt': ['reconciled', 'partial', 'cash_or_third_party'],
       'approvals': ['legal_and_finance', 'legal_only', 'none'], 'clock': ['within_60', 'day_61_75', 'beyond_75'],
       'kyc': ['clear', 'pending'], 'event': ['first', 'replay'], 'pack_state': ['active', 'draft']},
      lambda r: not (r['jurisdiction'] != 'IN' and r['clock'] != 'within_60'), o2, 'US-32-ZO01')

# ---------------- M-O3 cap table change (3-way)
def o3(r):
    if r['authority'] == 'none':
        return 'BLOCK NO_AUTHORITY_EVIDENCE', 'BRL-V12-O-07; AU-250'
    if r['instrument'] in ('equity', 'ccps', 'safe_or_note_conversion') and r['authority'] != 'board_and_shareholder':
        return 'BLOCK AUTHORITY_INSUFFICIENT', 'BRL-V12-O-07; RP-IN-SEC-001'
    if r['approvers'] != 'two_distinct':
        return 'HOLD SOD_TWO_DISTINCT_APPROVERS', 'BRL-APR-01; AU-239'
    if r['register'] == 'mismatch':
        return 'HOLD REGISTER_RECONCILIATION', 'AU-250'
    note = ' ROUND_DOWN_WHOLE_SHARES' if r['rounding'] == 'fractional' else ''
    fx = ' FX_SNAPSHOT_REQUIRED' if r['currency'] != 'INR' else ''
    return 'ALLOW NEW_REVISION' + note + fx, 'AU-250; AU-251; ADR-239'
model('M-O3', 'Cap-table change control', 'INV-SVC-20 WF01–WF04', 3,
      {'instrument': ['equity', 'ccps', 'safe_or_note_conversion', 'esop_option'], 'authority': ['board_and_shareholder', 'board_only', 'none'],
       'register': ['match', 'mismatch'], 'approvers': ['two_distinct', 'one', 'same_person_twice'],
       'rounding': ['exact', 'fractional'], 'currency': ['INR', 'USD', 'EUR']}, lambda r: True, o3, 'US-33-ZO05')

# ---------------- M-O4 governance (3-way)
def o4(r):
    if r['notice'] == 'short_no_consent' and r['meeting'] != 'written_resolution':
        return 'BLOCK INVALID_NOTICE', 'AU-254; BRL-V12-O-08'
    if r['meeting'] != 'written_resolution' and r['quorum'] == 'not_met':
        return 'NOT_PASSABLE QUORUM_NOT_MET', 'AU-254'
    pre = 'EXCLUDE_INELIGIBLE_AND_RETALLY; ' if r['voter_roll'] == 'ineligible_included' else ''
    if r['meeting'] == 'written_resolution' and r['esign'] == 'none':
        return pre + 'HOLD SIGNATURES_REQUIRED', 'AU-254'
    return pre + 'TALLY_THEN_CERTIFY_BY_CHAIR', 'AU-254; BRL-V12-O-08'
model('M-O4', 'Board and shareholder resolution validity', 'INV-SVC-23 WF01–WF04', 3,
      {'meeting': ['board', 'general', 'written_resolution'], 'jurisdiction': ['IN', 'UK', 'US_DE'],
       'notice': ['compliant', 'short_with_consent', 'short_no_consent'], 'quorum': ['met', 'not_met'],
       'voter_roll': ['eligible', 'ineligible_included'], 'esign': ['approved', 'none']},
      lambda r: not (r['meeting'] == 'written_resolution' and (r['quorum'] == 'not_met' or r['notice'] != 'compliant')), o4, 'US-33-ZO09')

# ---------------- M-O5 KYC (3-way)
def o5(r):
    reg = f" STORE_IN_{r['residency']}"
    if r['legal_basis'] == 'absent':
        return 'BLOCK NO_LEGAL_BASIS_NO_COLLECTION', 'RP-AML-KYC-002'
    if r['result'] == 'true_match':
        return 'PERMANENT_BLOCK ESCALATE_R10_R01' + reg, 'AU-256; RP-AML-KYC-006'
    if r['result'] == 'possible_match':
        return 'HOLD HUMAN_REVIEW' + reg, 'AU-256; RP-AML-KYC-005'
    if r['result'] == 'provider_error':
        return 'HOLD RETRY_RECONCILE' + reg, 'AU-255'
    if r['investor'] != 'individual' and r['beneficial_owner'] == 'unresolved':
        return 'HOLD BO_UNRESOLVED' + reg, 'RP-AML-KYC-004'
    if r['age'] == 'expired':
        return 'HOLD RECHECK_REQUIRED' + reg, 'AU-255; RP-AML-KYC-007'
    if r['age'] == 'expiring':
        return 'CLEAR RECHECK_TASK_T30' + reg, 'AU-255'
    return 'CLEAR' + reg, 'AU-255; AU-259'
model('M-O5', 'Investor verification and screening hand-off', 'INV-SVC-24; RP-AML-KYC', 3,
      {'investor': ['individual', 'entity', 'trust_or_fund'], 'result': ['clear', 'possible_match', 'true_match', 'provider_error'],
       'age': ['fresh', 'expiring', 'expired'], 'legal_basis': ['present', 'absent'], 'residency': ['IN', 'EU'],
       'beneficial_owner': ['resolved', 'unresolved']}, lambda r: not (r['investor'] == 'individual' and r['beneficial_owner'] == 'unresolved'), o5, 'US-33-ZO11')

# ---------------- M-O6 cross-border (3-way)
def o6(r):
    if r['investor'] == 'sanctioned':
        return 'BLOCK SANCTIONS', 'AU-256'
    if r['reviewer'] == 'rejected':
        return 'BLOCK REVIEWER_REJECTED', 'BRL-V12-O-10'
    if r['issuer'] == 'IN' and r['investor'] == 'nonresident_land_border' and r['reviewer'] != 'approved':
        return 'HOLD GOVERNMENT_ROUTE_APPROVAL_REQUIRED', 'RP-IN-SEC-016; AU-253'
    if r['issuer'] == 'IN' and r['investor'] != 'resident' and r['instrument'] == 'debt' and r['reviewer'] != 'approved':
        return 'HOLD ECB_ROUTE_REVIEW', 'RP-IN-SEC-018; AU-253'
    if r['reviewer'] == 'pending':
        return 'HOLD PROFESSIONAL_REVIEW', 'BRL-V12-O-10'
    if r['deadline'] == 'overdue':
        return 'ESCALATE LATE_FILING_COUNSEL', 'AU-253; RP-IN-SEC-017'
    if r['deadline'] == 'due_soon':
        return 'PROCEED ALERT_DEADLINE', 'AU-237'
    return 'PROCEED', 'AU-253'
model('M-O6', 'Cross-border funding restriction routing', 'INV-SVC-22', 3,
      {'issuer': ['IN', 'US', 'UK', 'EU'], 'investor': ['resident', 'nonresident_other', 'nonresident_land_border', 'sanctioned'],
       'instrument': ['equity', 'convertible', 'debt'], 'reviewer': ['approved', 'pending', 'rejected'], 'deadline': ['ok', 'due_soon', 'overdue']},
      lambda r: not (r['issuer'] != 'IN' and r['investor'] == 'nonresident_land_border'), o6, 'US-33-ZO07')

# ---------------- M-O7 advice boundary (3-way)
def o7(r):
    if r['request'] in ('recommend_buy_sell_hold', 'suitability_for_me'):
        return 'REFUSE TPL-INV-ADVICE-01', 'RP-INV-ADVICE-001/002; AU-257'
    if r['model_output'] == 'contains_recommendation':
        return 'WITHHOLD TPL-INV-ADVICE-01', 'AU-257; AG-199; RP-INV-ADVICE-003'
    if r['subject'] == 'third_party_securities':
        return 'REFUSE OUT_OF_SCOPE', 'RP-INV-ADVICE-004'
    if r['request'] == 'scenario_calculation':
        if r['audience'] == 'investor_portal':
            return 'ALLOW GENERIC_ILLUSTRATION TPL-INV-ADVICE-03', 'RP-INV-ADVICE-005/006'
        return 'ALLOW LABELLED_ESTIMATE TPL-INV-ADVICE-03', 'RP-INV-ADVICE-006'
    return 'ALLOW FACTUAL_WITH_SOURCE', 'RP-INV-ADVICE-007'
model('M-O7', 'No personalised investment advice by AI', 'RP-INV-ADVICE; AG-199; AU-257', 3,
      {'audience': ['issuer_user', 'investor_portal'], 'request': ['factual_info', 'scenario_calculation', 'recommend_buy_sell_hold', 'suitability_for_me'],
       'subject': ['own_company_securities', 'third_party_securities'], 'jurisdiction': ['IN', 'US', 'EU', 'UK'],
       'model_output': ['neutral', 'contains_recommendation']}, lambda r: True, o7, 'US-33-ZO15')

# ---------------- pairwise models
def o8(r):
    if r['figures'] == 'untied':
        return 'BLOCK FIGURE_TIEOUT', 'AU-240'
    if r['recipients'] == 'beyond_rights':
        return 'BLOCK RECIPIENT_SCOPE', 'BRL-V12-O-03'
    if r['approval'] == 'none':
        return 'HOLD OWNER_APPROVAL', 'INV-SVC-14 gate'
    if r['mentions_offer'] == 'yes':
        return 'ROUTE AG-198_SECURITIES_REVIEW', 'AU-232; AG-198'
    if r['channel'] == 'email' and r['consent'] == 'no':
        return 'DELIVER PORTAL_ONLY', 'BRL-ELG-01'
    return 'DISPATCH', 'PDP recheck'
model('M-O8', 'Investor update dispatch', 'INV-SVC-14', 2,
      {'figures': ['tied', 'untied'], 'recipients': ['rights_holders', 'beyond_rights'], 'mentions_offer': ['no', 'yes'],
       'approval': ['owner_approved', 'none'], 'consent': ['yes', 'no'], 'locale': ['en', 'hi', 'de'], 'channel': ['portal', 'email']},
      lambda r: True, o8, 'US-32-ZO03')

def o9(r):
    if r['transition'] in ('to_committed', 'to_funded', 'skip_stage') and r['evidence'] == 'absent':
        return 'DENY EVIDENCE_REQUIRED', 'AU-242'
    if r['action'] == 'cold_outreach' and r['solicitation'] == 'private':
        return 'DENY SOLICITATION_MODE', 'AU-232'
    if r['currency'] == 'mixed' and r['fx'] == 'none':
        return 'HOLD AGGREGATION_FX', 'BRL-V12-O-04'
    return 'ALLOW', 'AU-242'
model('M-O9', 'Fundraising pipeline stage and action control', 'INV-SVC-15', 2,
      {'transition': ['normal_next', 'to_committed', 'to_funded', 'skip_stage'], 'evidence': ['present', 'absent'],
       'currency': ['single', 'mixed'], 'fx': ['snapshot', 'none'], 'solicitation': ['private', 'general_506c'],
       'action': ['internal_task', 'cold_outreach']}, lambda r: True, o9, 'US-32-ZO05')

def o10(r):
    if r['signature'] != 'valid':
        return 'REJECT SIGNATURE', 'AU-244'
    if r['timestamp'] == 'stale':
        return 'REJECT STALE', 'AU-244'
    if r['nonce'] == 'replay':
        return 'REJECT DUPLICATE', 'AU-244'
    if r['source'] == 'external_agent' and r['mandate'] == 'none':
        return 'REJECT AGENT_MANDATE', 'AU-245'
    if r['consent'] == 'absent':
        return 'HOLD CONSENT', 'BRL-ELG-01'
    if r['pack'] == 'inactive':
        return 'STORE ENQUIRY_ONLY_NO_OFFER_MATERIAL', 'AU-231'
    return 'ROUTE', 'AG-186'
model('M-O10', 'Private enquiry intake', 'INV-SVC-16', 2,
      {'signature': ['valid', 'invalid', 'missing'], 'timestamp': ['fresh', 'stale'], 'nonce': ['new', 'replay'],
       'consent': ['present', 'absent'], 'source': ['issuer_form', 'external_agent'], 'mandate': ['active', 'none'], 'pack': ['active', 'inactive']},
      lambda r: True, o10, 'US-32-ZO07')

def o11(r):
    if r['criterion'] == 'not_met':
        return 'INELIGIBLE STOP', 'INV-SVC-17 WF01'
    if r['criterion'] == 'unknown':
        return 'HOLD ELIGIBILITY_UNKNOWN', 'INV-SVC-17 WF01'
    if r['citation'] == 'absent':
        return 'ABSTAIN NEEDS_INPUT', 'AG-188'
    if r['budget'] != 'eligible':
        return 'BLOCK_READY BUDGET', 'AU-246'
    if r['attachments'] == 'missing':
        return 'BLOCK_READY ATTACHMENTS', 'AU-246'
    if r['approval'] == 'none':
        return 'READY_NOT_SUBMITTABLE', 'INV-SVC-17 WF03'
    return 'SUBMISSION_READY HUMAN_SUBMITS', 'INV-SVC-17 WF03'
model('M-O11', 'Grant application readiness', 'INV-SVC-17', 2,
      {'criterion': ['met', 'unknown', 'not_met'], 'citation': ['present', 'absent'], 'budget': ['eligible', 'ineligible_line', 'over_cap'],
       'attachments': ['complete', 'missing'], 'approval': ['hash_approved', 'none']}, lambda r: True, o11, 'US-33-ZO01')

def o12(r):
    if r['calc'] == 'engines_differ':
        return 'HOLD CALCULATION_MISMATCH', 'AU-247'
    if r['share_scope'] == 'beyond_checklist':
        return 'BLOCK SCOPE', 'INV-SVC-18 WF02'
    if r['approval'] == 'no':
        return 'HOLD SHARE_APPROVAL', 'INV-SVC-18 WF02'
    if r['covenant'] == 'breach':
        return 'ALERT BREACH', 'AU-241'
    if r['covenant'] == 'near_breach':
        return 'ALERT T30', 'AU-241'
    if r['payment'] == 'missing':
        return 'EXCEPTION PAYMENT', 'AU-241'
    return 'OK', 'AU-247'
model('M-O12', 'Debt case calculation, sharing and covenant monitoring', 'INV-SVC-18', 2,
      {'calc': ['engines_agree', 'engines_differ'], 'covenant': ['headroom', 'near_breach', 'breach'], 'payment': ['reconciled', 'missing'],
       'share_scope': ['checklist_only', 'beyond_checklist'], 'approval': ['yes', 'no']}, lambda r: True, o12, 'US-33-ZO03')

def o13(r):
    if r['freshness'] == 'stale':
        return 'NO_ALERT DATA_STALE', 'AU-248'
    if r['totals'] == 'mismatch':
        return 'HOLD IMPORT_RECONCILIATION', 'AU-248'
    if r['missing'] == 'some':
        return 'FLAG MISSING_NOT_IMPUTED', 'AU-248'
    if r['runway'] == 'below_threshold':
        return 'ALERT OWNER_ACTION_PLAN', 'AU-248; AG-191'
    return 'OK', 'AU-248'
model('M-O13', 'Readiness and runway monitoring', 'INV-SVC-19', 2,
      {'freshness': ['fresh', 'stale'], 'totals': ['reconcile', 'mismatch'], 'missing': ['none', 'some'], 'runway': ['above', 'below_threshold']},
      lambda r: True, o13, 'US-33-ZO04')

def o14(r):
    if r['unit'] == 'invalid' or r['period'] == 'mismatch':
        return 'HOLD VALIDATION', 'AU-252'
    if r['source'] == 'absent':
        return 'BLOCK UNTRACEABLE', 'INV-SVC-21 KPI'
    if r['claim'] == 'generic_unsubstantiated':
        return 'BLOCK UNSUPPORTED_CLAIM', 'AG-193; RP-EU-PROSP-010'
    if r['approval'] == 'no':
        return 'HOLD OWNER_APPROVAL', 'INV-SVC-21 WF03'
    return 'RELEASE', 'INV-SVC-21 WF03'
model('M-O14', 'ESG disclosure release', 'INV-SVC-21', 2,
      {'unit': ['valid', 'invalid'], 'period': ['match', 'mismatch'], 'source': ['present', 'absent'],
       'claim': ['specific_substantiated', 'generic_unsubstantiated'], 'approval': ['yes', 'no']}, lambda r: True, o14, 'US-33-ZO06')

def o15(r):
    if r['jurisdiction_match'] == 'no':
        return 'NOT_APPLICABLE', 'CP-01'
    if r['state'] != 'active':
        return 'BLOCK PACK_NOT_ACTIVE', 'CP-05; AU-231'
    if r['signoff'] == 'absent':
        return 'BLOCK INTEGRITY_NO_SIGNOFF', 'ADR-235'
    if r['expiry'] == 'expired':
        return 'BLOCK PACK_EXPIRED_SUSPEND', 'CP-05'
    return 'PACK_CONTRIBUTES', 'AU-231'
model('M-O15', 'Securities rule-pack lifecycle and activation', 'All seven packs; A254/A258', 2,
      {'state': ['draft', 'counsel_review', 'approved', 'active', 'suspended', 'retired'], 'signoff': ['present', 'absent'],
       'expiry': ['valid', 'expired'], 'jurisdiction_match': ['yes', 'no']}, lambda r: True, o15, 'US-33-ZO12')

def o16(r):
    if r['tenant'] == 'foreign':
        return 'NOT_FOUND 404', 'BRL-TEN-04'
    if r['entitlement'] != 'active':
        return 'DENY ENTITLEMENT', 'BRL-SVC-03'
    return 'RUN', 'entitlement check'
model('M-O16', 'Single-SKU entitlement isolation (INV-SVC-13…24-ENT-AT01)', 'INV-SVC-13…24', 2,
      {'sku': [f'INV-SVC-{n}' for n in range(13, 25)], 'entitlement': ['active', 'revoked', 'none'], 'tenant': ['own', 'foreign'], 'workflow': ['WF01', 'WF02', 'WF03', 'WF04']},
      lambda r: True, o16, 'US-32-ZO09')

out = []
for m in M:
    full, valid, rows, method = covering(m['params'], m['t'], m['valid'])
    # risk-based additions: every distinct oracle outcome in the valid space must appear at least once
    seen = {m['oracle'](r)[0] for r in rows}
    added = 0
    for r in valid:
        o = m['oracle'](r)[0]
        if o not in seen:
            rows = rows + [r]; seen.add(o); added += 1
    outcomes_valid = len({m['oracle'](r)[0] for r in valid})
    cases = []
    for i, r in enumerate(rows, 1):
        exp, rules = m['oracle'](r)
        cases.append(dict(id=f"TC-V12-O-{m['id'][2:]}-{i:03d}", row=r, expected=exp, rules=rules))
    out.append(dict(id=m['id'], title=m['title'], cap=m['cap'], t=m['t'], params=m['params'], full=len(full), valid=len(valid),
                    method=method, n=len(cases), cases=cases, story=m['story'], added=added, outcomes=outcomes_valid))
    print(m['id'], m['title'], 'full', len(full), 'valid', len(valid), method, 'cases', len(cases), 'risk-added', added, 'outcomes', outcomes_valid)
json.dump(out, open('/home/user/Allinonecalculator/blueprint/assembly/v12b/o_combi.json', 'w'), indent=1)
print('total cases', sum(x['n'] for x in out))
