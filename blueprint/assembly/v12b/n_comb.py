"""Group N combinatorial parameter models (PM-N-01...09), constraints and deterministic oracles.

Each oracle encodes the controls SEC-CTL-N-01...16 and BRL-V12-N-01...24 so every generated row is an
executable test case with a computed expected result. Run: python3 -I n_comb.py  (prints counts).
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from n_common import covering_array, exhaustive, verify_coverage

ROUTES = {'IN': ['s42_PP', 'ICDR_pref_listed', 'none'], 'US': ['506b', '506c', 'RegCF', 'none'],
          'EU': ['PR_QI_only', 'PR_lt150', 'none'], 'UK': ['FPO_exempt', 'none']}
ALLROUTES = sorted({r for v in ROUTES.values() for r in v})


# ---------------- PM-N-01 investor engagement dispatch (3-way)
P1 = [('jurisdiction', ['IN', 'US', 'EU', 'UK']),
      ('investor_type', ['retail', 'sophisticated_HNI', 'accredited_or_QI', 'QIB_institutional', 'unknown']),
      ('offering_route', ALLROUTES),
      ('channel', ['email', 'whatsapp', 'portal', 'manual_task']),
      ('mandate', ['none', 'active', 'expired', 'revoked']),
      ('data_class', ['Public', 'Personal', 'Confidential-Financial']),
      ('consent', ['granted', 'absent', 'withdrawn']),
      ('pack_state', ['active', 'draft', 'expired']),
      ('relationship', ['preexisting', 'none'])]


def c1(d):
    return d['offering_route'] in ROUTES[d['jurisdiction']]


def o1(d):
    r = d['offering_route']; it = d['investor_type']; ch = d['channel']
    if d['pack_state'] != 'active':
        return 'BLOCK', 'PACK_NOT_ACTIVE', 'SEC-CTL-N-01'
    if d['mandate'] in ('expired', 'revoked'):
        return 'BLOCK', 'MANDATE_INVALID', 'SEC-CTL-N-10'
    if d['consent'] == 'withdrawn' and ch != 'portal':
        return 'BLOCK', 'CONSENT_WITHDRAWN', 'SEC-CTL-N-06'
    if ch == 'whatsapp' and d['consent'] != 'granted':
        return 'BLOCK', 'NO_OPT_IN', 'SEC-CTL-N-06'
    if ch == 'email' and d['consent'] == 'absent' and d['jurisdiction'] in ('IN',):
        return 'BLOCK', 'NO_LAWFUL_BASIS', 'SEC-CTL-N-06'
    if ch == 'email' and d['consent'] == 'absent' and d['jurisdiction'] in ('EU', 'UK') and d['relationship'] == 'none':
        return 'BLOCK', 'NO_LAWFUL_BASIS', 'SEC-CTL-N-06'
    if d['data_class'] == 'Confidential-Financial' and ch in ('email', 'whatsapp'):
        return 'BLOCK', 'CLASS_PORTAL_ONLY', 'SEC-CTL-N-04'
    if r != 'none':
        if it == 'unknown':
            return 'HOLD', 'ELIGIBILITY_UNKNOWN', 'SEC-CTL-N-02'
        if r == 'RegCF':
            return 'BLOCK', 'REG_CF_PORTAL_ONLY', 'SEC-CTL-N-09'
        if r == 'ICDR_pref_listed':
            return 'HOLD', 'COUNSEL_REVIEW_LISTED', 'SEC-CTL-N-08'
        if r in ('s42_PP', '506b') and d['relationship'] == 'none':
            return 'BLOCK', 'GENERAL_SOLICITATION', 'SEC-CTL-N-03'
        if r == 's42_PP' and it == 'retail':
            return 'HOLD', 'COUNSEL_REVIEW_RETAIL', 'SEC-CTL-N-02'
        if r == '506b' and it == 'retail':
            return 'BLOCK', 'INELIGIBLE_FOR_ROUTE', 'SEC-CTL-N-02'
        if r == '506b' and it == 'sophisticated_HNI':
            return 'HOLD', 'NON_ACCREDITED_CAP_AND_DISCLOSURE', 'SEC-CTL-N-09'
        if r == '506c' and it in ('retail', 'sophisticated_HNI'):
            return 'BLOCK', 'INELIGIBLE_FOR_ROUTE', 'SEC-CTL-N-02'
        if r == 'PR_QI_only' and it in ('retail', 'sophisticated_HNI'):
            return 'BLOCK', 'INELIGIBLE_FOR_ROUTE', 'SEC-CTL-N-02'
        if r in ('PR_QI_only', 'PR_lt150') and d['relationship'] == 'none':
            return 'HOLD', 'COUNSEL_REVIEW_PRIVATE_PLACEMENT', 'SEC-CTL-N-03'
        if r == 'FPO_exempt' and it == 'retail':
            return 'BLOCK', 'FINANCIAL_PROMOTION', 'SEC-CTL-N-03'
        if r == 'FPO_exempt' and it == 'sophisticated_HNI':
            return 'HOLD', 'CERTIFICATION_REQUIRED', 'SEC-CTL-N-02'
    if ch == 'manual_task':
        return 'TASK_ONLY', 'NO_EXTERNAL_EFFECT', 'SEC-CTL-N-10'
    if d['mandate'] == 'none':
        return 'HOLD', 'APPROVAL_REQUIRED_L1', 'SEC-CTL-N-10'
    extra = ' (cap reserved)' if r in ('PR_lt150', '506b', 's42_PP') else ''
    return 'DISPATCH' + extra, 'ALLOWED_UNDER_MANDATE', 'SEC-CTL-N-10'


# ---------------- PM-N-02 data-room access (3-way)
P2 = [('eligibility', ['verified', 'pending', 'expired', 'failed']),
      ('kyc', ['cleared', 'pending', 'screening_hit']),
      ('nda', ['signed', 'missing', 'expired']),
      ('grant', ['active', 'expired', 'revoked', 'none']),
      ('doc_class', ['general', 'confidential', 'offering_doc', 'restricted_financial']),
      ('signoff', ['valid', 'void', 'missing']),
      ('region', ['same', 'cross'])]


def o2(d):
    if d['kyc'] == 'screening_hit':
        return 'DENY_404', 'SCREENING_HIT_R10_ALERT', 'SEC-CTL-N-07'
    if d['grant'] != 'active':
        return 'DENY_404', 'NO_ACTIVE_GRANT', 'SEC-CTL-N-04'
    if d['nda'] != 'signed':
        return 'DENY_403', 'NDA_REQUIRED', 'SEC-CTL-N-04'
    if d['doc_class'] in ('confidential', 'offering_doc', 'restricted_financial') and d['eligibility'] != 'verified':
        return 'DENY_403', 'ELIGIBILITY_NOT_VERIFIED', 'SEC-CTL-N-02'
    if d['doc_class'] in ('offering_doc', 'restricted_financial') and d['signoff'] != 'valid':
        return 'DENY_403', 'OFFERING_NOT_SIGNED_OFF', 'SEC-CTL-N-08'
    if d['doc_class'] == 'restricted_financial' and d['kyc'] != 'cleared':
        return 'DENY_403', 'KYC_NOT_CLEARED', 'SEC-CTL-N-07'
    tail = ' (served from tenant region)' if d['region'] == 'cross' else ''
    return 'ALLOW_WATERMARKED' + tail, 'GRANTED', 'SEC-CTL-N-04'


# ---------------- PM-N-03 formal offer issue (3-way)
P3 = [('route', ['s42_PP', '506b', '506c', 'PR_QI_only', 'PR_lt150', 'FPO_exempt']),
      ('recipient', ['eligible_verified', 'eligible_unverified', 'ineligible']),
      ('signoff', ['valid', 'expired', 'void_doc_changed']),
      ('approvals', ['two_distinct', 'one', 'same_person_twice']),
      ('cap', ['below', 'at_cap']),
      ('hash', ['match', 'mismatch']),
      ('kill_switch', ['off', 'on']),
      ('cross_border', ['no', 'yes'])]


def o3(d):
    if d['kill_switch'] == 'on':
        return 'BLOCK', 'KILL_SWITCH', 'SEC-CTL-N-15'
    if d['signoff'] != 'valid':
        return 'BLOCK', 'SIGNOFF_INVALID', 'SEC-CTL-N-08'
    if d['approvals'] != 'two_distinct':
        return 'BLOCK', 'APPROVAL_INCOMPLETE', 'SEC-CTL-N-10'
    if d['hash'] != 'match':
        return 'BLOCK', 'HASH_MISMATCH', 'SEC-CTL-N-10'
    if d['recipient'] == 'ineligible':
        return 'BLOCK', 'INELIGIBLE', 'SEC-CTL-N-02'
    if d['recipient'] == 'eligible_unverified':
        return 'HOLD', 'ELIGIBILITY_UNVERIFIED', 'SEC-CTL-N-02'
    if d['cross_border'] == 'yes':
        return 'HOLD', 'COUNSEL_CROSS_BORDER', 'SEC-CTL-N-14'
    if d['cap'] == 'at_cap':
        return 'BLOCK', 'CAP_REACHED', 'SEC-CTL-N-09'
    return 'ISSUE', 'SERIAL_ASSIGNED_REGISTERED', 'SEC-CTL-N-12'


# ---------------- PM-N-04 receipt reconciliation (3-way)
P4 = [('source', ['bank_statement', 'pa_webhook', 'manual_upload']),
      ('currency', ['matches', 'differs_fx_verified', 'differs_no_fx']),
      ('amount', ['exact', 'partial', 'over', 'no_match']),
      ('payer', ['subscriber_own', 'third_party', 'unknown']),
      ('duplicate', ['no', 'yes']),
      ('kyc', ['cleared', 'pending']),
      ('route', ['s42_PP', 'other'])]


def o4(d):
    if d['duplicate'] == 'yes':
        return 'REJECT', 'DUPLICATE_RECEIPT', 'SEC-CTL-N-11'
    if d['source'] == 'manual_upload':
        return 'HOLD', 'R08_VERIFY_MANUAL_EVIDENCE', 'SEC-CTL-N-11'
    if d['currency'] == 'differs_no_fx':
        return 'EXCEPTION', 'FX_SOURCE_MISSING', 'SEC-CTL-N-11'
    if d['kyc'] != 'cleared':
        return 'HOLD', 'KYC_NOT_CLEARED', 'SEC-CTL-N-07'
    if d['payer'] == 'unknown':
        return 'EXCEPTION', 'PAYER_UNKNOWN', 'SEC-CTL-N-11'
    if d['payer'] == 'third_party' and d['route'] == 's42_PP':
        return 'EXCEPTION', 'THIRD_PARTY_PAYER_S42', 'SEC-CTL-N-11'
    if d['amount'] == 'no_match':
        return 'EXCEPTION', 'UNMATCHED', 'SEC-CTL-N-11'
    if d['amount'] == 'over':
        return 'ALLOCATE+EXCEPTION', 'OVERPAYMENT_REFUND_HUMAN', 'SEC-CTL-N-11'
    if d['amount'] == 'partial':
        return 'ALLOCATE_PARTIAL', 'REMAINDER_OPEN', 'SEC-CTL-N-11'
    tp = ' (third-party payer noted)' if d['payer'] == 'third_party' else ''
    return 'ALLOCATE' + tp, 'MATCHED', 'SEC-CTL-N-11'


# ---------------- PM-N-05 no-advice guard (pairwise)
P5 = [('request', ['factual_company', 'valuation_opinion', 'should_i_invest', 'return_projection', 'tax_question', 'terms_question', 'document_request']),
      ('asker', ['issuer_staff', 'invited_investor', 'anonymous_web']),
      ('channel', ['portal', 'email', 'whatsapp', 'copilot_A226']),
      ('evidence', ['current', 'stale', 'none']),
      ('language', ['en', 'hi', 'de'])]


def c5(d):
    if d['asker'] == 'anonymous_web' and d['channel'] != 'portal':
        return False  # anonymous visitors only reach the public site (portal channel stands for W55-W73 forms)
    if d['asker'] != 'issuer_staff' and d['channel'] == 'copilot_A226':
        return False
    return True


def o5(d):
    rq, a = d['request'], d['asker']
    if a == 'anonymous_web':
        return 'NEUTRAL_SAAS_ANSWER', 'NO_ISSUER_CONTENT_PUBLIC', 'SEC-CTL-N-03'
    if a == 'invited_investor':
        if rq in ('valuation_opinion', 'should_i_invest', 'return_projection', 'tax_question'):
            return 'REFUSE_TPL-N-01+HANDOVER', 'ADVICE_CLASS', 'SEC-CTL-N-05'
        if rq == 'terms_question':
            return 'HANDOVER_R10', 'TERMS_HUMAN_ONLY', 'SEC-CTL-N-05'
        if rq == 'document_request':
            return ('REDIRECT_TO_W75' if d['channel'] != 'portal' else 'AU-204_ACCESS_CHECK'), 'OFFERING_DOC_GATING', 'SEC-CTL-N-04'
        if d['evidence'] == 'current':
            return 'GROUNDED_DRAFT_FOR_APPROVAL', 'CITED_FACTS_ONLY', 'SEC-CTL-N-13'
        return 'ABSTAIN+HANDOVER', 'NO_CURRENT_EVIDENCE', 'SEC-CTL-N-13'
    # issuer staff
    if rq in ('valuation_opinion', 'should_i_invest'):
        return 'SCENARIOS_ONLY_AU-219', 'NO_OPINION', 'SEC-CTL-N-05'
    if rq == 'return_projection':
        return 'LABELLED_SCENARIO_AU-219', 'FORWARD_LOOKING_LABEL', 'SEC-CTL-N-13'
    if rq == 'tax_question':
        return 'REFER_COUNSEL', 'TAX_LEGAL_ADVICE', 'SEC-CTL-N-05'
    if rq == 'terms_question':
        return 'TERM_COMPARISON_AG-177', 'INTERNAL_ANALYSIS', 'SEC-CTL-N-05'
    if rq == 'document_request':
        return 'ROLE_ACCESS_CHECK', 'RBAC', 'SEC-CTL-N-04'
    if d['evidence'] == 'current':
        return 'GROUNDED_ANSWER', 'CITED_FACTS_ONLY', 'SEC-CTL-N-13'
    return 'ABSTAIN', 'NO_CURRENT_EVIDENCE', 'SEC-CTL-N-13'


# ---------------- PM-N-06 investor-mode website (pairwise)
P6 = [('mode', ['inv', 'commercial']),
      ('route_kind', ['home', 'catalog', 'detail', 'compare', 'enquiry', 'booking', 'plans', 'register', 'wizard', 'dashboard', 'quote', 'billing', 'help']),
      ('auth', ['anonymous', 'demo_session', 'authenticated_client']),
      ('visitor_region', ['IN', 'US', 'EU', 'other']),
      ('payload', ['neutral_catalog', 'issuer_name', 'offering_terms', 'investor_record'])]
PRIVATE = {'wizard', 'dashboard', 'quote', 'billing'}


def o6(d):
    if d['payload'] != 'neutral_catalog':
        return 'BLOCK_AU-228', 'PUBLIC_PAYLOAD_LEAK', 'SEC-CTL-N-03'
    if d['route_kind'] in PRIVATE and d['auth'] == 'anonymous':
        return 'REDIRECT_W59', 'SIGN_IN_REQUIRED', 'SEC-CTL-N-16'
    banner = {'EU': 'GDPR opt-in consent banner', 'IN': 'DPDP notice', 'US': 'privacy notice', 'other': 'privacy notice'}[d['visitor_region']]
    label = 'fundraising-mode labels' if d['mode'] == 'inv' else 'commercial labels'
    return f'RENDER ({label}; {banner})', 'NEUTRAL_SAAS_ONLY', 'SEC-CTL-N-03'


# ---------------- PM-N-07 investor contact privacy (pairwise)
P7 = [('source', ['licensed_db', 'public_web_profile', 'client_list', 'investor_self']),
      ('purpose', ['fundraising_outreach', 'research_only']),
      ('region', ['IN', 'EU', 'UK', 'US']),
      ('lawful_basis', ['consent', 'legitimate_interest_LIA', 'none']),
      ('request', ['none', 'access', 'erasure', 'objection']),
      ('retention', ['within', 'past'])]


def o7(d):
    if d['request'] == 'erasure':
        return 'ERASE_+_SUPPRESSION_HASH', 'DSR_ERASURE', 'SEC-CTL-N-16'
    if d['request'] == 'objection':
        return 'SUPPRESS_ALL_OUTREACH', 'DSR_OBJECTION', 'SEC-CTL-N-06'
    if d['retention'] == 'past':
        return 'PURGE', 'RETENTION_EXPIRED', 'SEC-CTL-N-16'
    pre = 'EXPORT_WITHIN_SLA; ' if d['request'] == 'access' else ''
    if d['purpose'] == 'research_only':
        if d['lawful_basis'] == 'none':
            return pre + 'HOLD_NO_PROCESSING', 'NO_LAWFUL_BASIS', 'SEC-CTL-N-06'
        return pre + 'RESEARCH_ALLOWED', 'BASIS_OK', 'SEC-CTL-N-06'
    if d['lawful_basis'] == 'none':
        return pre + 'HOLD_NO_OUTREACH', 'NO_LAWFUL_BASIS', 'SEC-CTL-N-06'
    if d['region'] == 'IN' and d['lawful_basis'] != 'consent':
        return pre + 'HOLD_CONSENT_REQUIRED', 'DPDP_CONSENT', 'SEC-CTL-N-06'
    if d['region'] in ('EU', 'UK') and d['lawful_basis'] == 'legitimate_interest_LIA' and d['source'] != 'investor_self':
        return pre + 'OUTREACH_WITH_ART14_NOTICE', 'LIA_NOTICE', 'SEC-CTL-N-06'
    return pre + 'OUTREACH_ELIGIBLE', 'BASIS_OK', 'SEC-CTL-N-06'


# ---------------- PM-N-08 meeting recording (exhaustive, 36)
P8 = [('regime', ['one_party', 'all_party']), ('consent', ['all', 'some', 'none']), ('notice', ['given', 'not_given']),
      ('capture', ['audio', 'transcript_only', 'none'])]


def o8(d):
    if d['capture'] == 'none':
        return 'MEETING_NO_RECORDING', 'NOTHING_CAPTURED', 'SEC-CTL-N-06'
    if d['notice'] == 'not_given':
        return 'CAPTURE_BLOCKED', 'NOTICE_MISSING', 'SEC-CTL-N-06'
    if d['regime'] == 'all_party' and d['consent'] != 'all':
        return 'CAPTURE_BLOCKED', 'ALL_PARTY_CONSENT_MISSING', 'SEC-CTL-N-06'
    if d['consent'] == 'none':
        return 'CAPTURE_BLOCKED', 'PLATFORM_POLICY_CONSENT', 'SEC-CTL-N-06'
    return 'CAPTURE_ALLOWED', 'CONSENT_OK', 'SEC-CTL-N-06'


# ---------------- PM-N-09 SKU entitlement (exhaustive, 48)
P9 = [('selection', ['full', 'partial_bundle', 'selective']), ('sku_state', ['active', 'suspended', 'revoked', 'not_purchased']),
      ('budget', ['available', 'exhausted']), ('input', ['upstream_or_supplied', 'missing'])]


def o9(d):
    s = d['sku_state']
    if s == 'not_purchased':
        return '403', 'ENTITLEMENT_REQUIRED', 'AU-200'
    if s == 'revoked':
        return '403 + active runs paused', 'ENTITLEMENT_REVOKED', 'AU-200'
    if s == 'suspended':
        return 'PAUSED', 'ENTITLEMENT_SUSPENDED', 'AU-200'
    if d['budget'] == 'exhausted':
        return 'BLOCKED', 'BUDGET_EXHAUSTED', 'AU-200'
    if d['input'] == 'missing':
        return 'DRAFT_ONLY_HOLD', 'PREREQUISITE_INPUT_MISSING', 'AU-200'
    return 'RUN', 'ENTITLED', 'AU-200'


MODELS = [
 ('PM-N-01', 'Investor engagement dispatch', P1, c1, o1, 3, 'INV-SVC-04/05/06 dispatch; SEC-CTL-N-01/02/03/04/06/09/10', 'TS-N-21'),
 ('PM-N-02', 'Data-room access', P2, None, o2, 3, 'INV-SVC-10-WF02; SEC-CTL-N-02/04/07/08', 'TS-N-22'),
 ('PM-N-03', 'Formal offer issue', P3, None, o3, 3, 'INV-SVC-11-WF02; SEC-CTL-N-02/08/09/10/12/14/15', 'TS-N-23'),
 ('PM-N-04', 'Receipt reconciliation', P4, None, o4, 3, 'INV-SVC-12-WF01/02; SEC-CTL-N-07/11', 'TS-N-24'),
 ('PM-N-05', 'No-AI-advice guard', P5, c5, o5, 2, 'AG-166, AU-217; SEC-CTL-N-05/13', 'TS-N-25'),
 ('PM-N-06', 'Investor-mode website', P6, None, o6, 2, 'W55–W76, AU-228; SEC-CTL-N-03/16', 'TS-N-26'),
 ('PM-N-07', 'Investor contact privacy', P7, None, o7, 2, 'INV-SVC-03; SEC-CTL-N-06/16', 'TS-N-27'),
 ('PM-N-08', 'Meeting recording consent (exhaustive)', P8, None, o8, 'all', 'INV-SVC-08; SEC-CTL-N-06; DEC-782', 'TS-N-28'),
 ('PM-N-09', 'SKU entitlement (exhaustive)', P9, None, o9, 'all', 'AU-200; Entitlement Rules', 'TS-N-29'),
]


BASE = {  # risk-based base-choice slices: all gates satisfied except the varied parameters
 'PM-N-01': ({'channel': 'email', 'mandate': 'active', 'consent': 'granted', 'pack_state': 'active', 'relationship': 'preexisting', 'data_class': 'Personal'}, ['jurisdiction', 'offering_route', 'investor_type']),
 'PM-N-02': ({'eligibility': 'verified', 'nda': 'signed', 'grant': 'active', 'signoff': 'valid'}, ['doc_class', 'region', 'kyc']),
 'PM-N-03': ({'recipient': 'eligible_verified', 'signoff': 'valid', 'approvals': 'two_distinct', 'hash': 'match', 'kill_switch': 'off'}, ['route', 'cross_border', 'cap']),
 'PM-N-04': ({'source': 'bank_statement', 'currency': 'matches', 'duplicate': 'no', 'kyc': 'cleared'}, ['amount', 'payer', 'route']),
 'PM-N-06': ({'payload': 'neutral_catalog', 'visitor_region': 'EU', 'mode': 'inv'}, ['route_kind', 'auth']),
}


def base_rows(mid, params, cons):
    if mid not in BASE:
        return []
    fixed, var = BASE[mid]
    sub = [(n, v) for n, v in params if n in var]
    out = []
    for d in exhaustive(sub):
        d.update(fixed)
        d = {n: d[n] for n, _ in params}
        if cons is None or cons(d):
            out.append(d)
    return out


def build():
    res = []
    for mid, title, params, cons, oracle, t, scope, ts in MODELS:
        space = 1
        for p in params:
            space *= len(p[1])
        valid = len(exhaustive(params, cons))
        if t == 'all':
            rows = exhaustive(params, cons)
            cov = (len(rows), valid)
            pw = rows
        else:
            rows = covering_array(params, t, cons)
            cov = verify_coverage(params, rows, t, cons)
            pw = covering_array(params, 2, cons) if t == 3 else rows
        key = lambda r: tuple(r[n] for n, _ in params)
        seen = {key(r) for r in rows}
        base = [r for r in base_rows(mid, params, cons) if key(r) not in seen]
        for r in rows + base:
            r['_exp'] = oracle(r)
        for r in pw:
            r['_exp'] = oracle(r)
        res.append(dict(id=mid, title=title, params=params, t=t, space=space, valid=valid, rows=rows, base=base, pw=pw,
                        cov=cov, scope=scope, ts=ts, oracle=oracle))
    return res


if __name__ == '__main__':
    for m in build():
        print(m['id'], m['t'], 'space', m['space'], 'valid', m['valid'], 'rows', len(m['rows']), 'base', len(m['base']), 'pw', len(m['pw']), 'cov', m['cov'])
        from collections import Counter
        print('   ', Counter(r['_exp'][0].split(' (')[0] for r in m['rows']+m['base']))
