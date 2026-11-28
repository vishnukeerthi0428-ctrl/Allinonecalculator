"""Group T (Part 11.21): assign TC-V12-T IDs, render every generated case in the Part 6.2a / 6.4
templates, compute the traceability rollup and assemble the Part 11.21a–e files from the prose
sources in assembly/v12b/t_src/ (placeholders {{NAME}} are replaced by generated tables).

Run (after t_01_inventory.py and t_04_models.py):
    python3 -I assembly/v12b/t_05_build.py
"""
import json, os, re, sys, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import t_03_catalogue as C  # noqa: E402

BP = C.BP
V = BP + '/assembly/v12b'
OUT = V + '/t_out'
SRC = V + '/t_src'
models = json.load(open(OUT + '/models.json'))
summary = json.load(open(OUT + '/summary.json'))
inv = json.load(open(OUT + '/inventory.json'))
sys.path.insert(0, V)
import t_04_models as TM  # noqa: E402

FR = {}


def esc(s):
    return str(s).replace('|', '\\|').replace('\n', ' ')


# =============================================================================================
# E2E cross-capability scenario suites (full form, Part 6.2a)
# =============================================================================================
J = [
    dict(j='J-T-01', title='Tenant onboards, buys a bundle, runs mandated outreach, quotes, collects payment, reconciles and exports audit',
         regions=[('IN', 'Kestrel Analytics Pvt Ltd (EXT-SMB, en-IN), UPI AutoPay/e-NACH collection'), ('EU', 'Nordlicht GmbH (EXT-SMB, de-DE), SEPA Direct Debit collection')],
         links='SM-SVC-06/10/17/21/32; MT-OUT, MT-COM, MT-PAY; DEC-770, 772, 777, 779, 780; FR-V12-P-001…099; CJ-TC-09',
         steps='1. R17 applies on W-pages, verifies e-mail, picks residency zone {Z} at onboarding and buys bundle "Outreach & Conversations" + SM-SVC-17/21 (checkout W). 2. Provisioning creates the tenant in {Z}; R12 invites R03, R05L, R08, R09, R10 (password + MFA). 3. R03 creates MT-OUT mandate (templates v1, 200 msgs/day, 2 per recipient per 7 d); R05L and R10 approve (two-person). 4. SM-SVC-06-WF02 sends at L3 to 40 consented contacts inside 09:00–21:00 local. 5. One reply → SM-SVC-09 intent → SM-SVC-10 meeting booked. 6. SM-SVC-17-WF02 quote within the discount band under MT-COM; customer accepts on Portal (R16). 7. SM-SVC-21 invoice; collection under MT-PAY via the zone PSP; pre-debit notice. 8. Signed PSP webhook → reconciliation. 9. R15 exports the audit pack',
         expected='Tenant, data, logs and backups only in {Z}; mandate Active only after both approvals and Approved packs ({P}); 40 sends exactly once, none outside the window or to suppressed contacts; meeting, quote (hash-bound), invoice and collection posted once; reconciliation match = 100%, 0 breaks; consumption ledger reserve→commit for every L3 effect; audit export complete with evidence IDs; axe 0 critical/serious on every page; all money as Decimal + ISO 4217 ({CUR})',
         P='P0', typ='T01, T19, T20', rel='R2'),
    dict(j='J-T-02', title='Enterprise tenant: SSO + SCIM, custom roles with SoD, API key, CRM connector, webhooks, then SCIM de-provisioning',
         regions=[('IN', 'Saffron Retail Ltd (EXT-ENT, Okta SAML)'), ('EU', 'Nordlicht GmbH Enterprise (EXT-ENT, Entra ID OIDC)')],
         links='DEC-784, 785, 786; FR-V12-R-001…055; US-01-ZR01…05, US-20-ZR06…10, US-18-ZR11, US-07-ZR12/13',
         steps='1. R12 verifies the domain, configures the IdP and enforces SSO. 2. SCIM pushes 25 users and 4 groups. 3. R12 creates custom role "Campaign Approver" (SoD: cannot author). 4. R12 issues a zone-bound API key and an OAuth client. 5. CRM connector activated through the activation gate; bi-directional sync of 500 contacts. 6. Outbound webhook subscription receives `run.completed`. 7. SCIM deletes 3 users',
         expected='SSO sessions issued only by the {Z} stack; SCIM objects created ≤ 5 s p95; SoD rule refuses author+approve on one item; API key works only on {Z} host; CRM sync respects field ownership and protected consent; webhook payload has references and digests only, signature verifies; de-provisioned users lose sessions ≤ 60 s; every step audited in {Z}',
         P='P0', typ='T07, T01', rel='R1'),
    dict(j='J-T-03', title='Agentic commerce: counterparty agent negotiation, order, pay-out, settlement, dispute and reconciliation',
         regions=[('IN', 'OrganicSpec (T1) selling to a verified buyer agent; UPI/e-NACH rails'), ('EU', 'Atelier Lumière SAS (EXT-SMB, fr-FR) buying from a verified supplier agent; SEPA rails')],
         links='SM-SVC-28-WF01…04; MT-COM, MT-PAY; DEC-780; FR-V12-P-070…099; RP-GL-AGENTCOM, RP-IN-AGENTCOM/RP-EU-AGENTCOM, RP-IN-PAY/RP-EU-PAY',
         steps='1. Publish the approved catalog version to authorized agent endpoints (MT-PUB). 2. Counterparty agent presents a verifiable credential; negotiation within bounds (max discount, min margin, rounds). 3. Order accepted under MT-COM (L3). 4. Pay-out or collection under MT-PAY through the licensed PSP. 5. PSP settles; one item disputed; chargeback evidence pack built. 6. Daily reconciliation',
         expected='Credential verified (issuer trusted, not revoked); offers beyond bounds rejected with a counter-offer inside bounds; signed acceptance; exactly one PSP instruction per order; commerce sub-ledger double-entry balanced; dispute flow opens a case and freezes the related mandate amount; reconciliation 100% matched or breaks routed to R08/R09; kill switch test during step 3 blocks the next order',
         P='P0', typ='T19, T20, T16', rel='R2'),
    dict(j='J-T-04', title='OrganicSpec procurement: RFQ, supplier comparison, PO under MT-PROC, receipt, supplier pay-out under MT-PAY',
         regions=[('IN', 'T1 OrganicSpec, payable ledger, UPI pay-out')],
         links='SM-SVC-39-WF01…04; MT-PROC + MT-PAY; BRL-APR-06/07; DEC-779, 780',
         steps='1. Need validated (approval-binding TC-V12-J-209). 2. RFQ to 3 approved suppliers; AI compares quotations (EVAL-SM-SVC-39-WF02). 3. R07 and R02/R08 approve MT-PROC; PO committed at L3 within per-PO cap. 4. Goods received. 5. Pay-out under MT-PAY (R08 maker + R09 checker mandate)',
         expected='PO only to allowlisted suppliers; per-PO and aggregate caps enforced; payable posted once; pay-out once with idempotency key; receivable and payable ledgers separate; reconciliation match; evidence pack complete',
         P='P0', typ='T19, T20', rel='R2'),
    dict(j='J-T-05', title='Automatic bid submission of the exact approved package under MT-BID, receipt, award and order',
         regions=[('IN', 'T1 AppNAI, GeM-type portal simulator, DSC signer'), ('EU', 'Nordlicht GmbH, eSubmission simulator, eIDAS signer')],
         links='SM-SVC-19-WF01…04; MT-BID; DEC-781; Part 11.17b; RP-IN-PROC / RP-EU-PROC',
         steps='1. Tender discovered (SM-SVC-02). 2. R06 prepares the package; compliance check (SM-SVC-19-WF04). 3. R02 and R10 approve package hash, price, terms and portal; MT-BID issued (count 1). 4. Agent submits before the deadline. 5. Portal receipt stored. 6. Award → SM-SVC-20 order',
         expected='Submission only if portal terms permit automation ({P} Approved); submitted bytes hash = approved hash; second submission impossible (mandate Exhausted); receipt and evidence stored in {Z}; a changed price after approval blocks submission',
         P='P0', typ='T19, T07', rel='R2'),
    dict(j='J-T-06', title='Inbound AI voice call: disclosure, multilingual booking, recording consent, transcript and coaching',
         regions=[('IN', 'T1 MedMaarg (hi-IN caller), institutional enquiry'), ('EU', 'Nordlicht GmbH (de-DE caller), all-party recording consent')],
         links='SM-SVC-26-WF01/03/04, SM-SVC-36-WF03; DEC-782; FR-V12-Q; US-22-ZQ01, US-08-ZQ01',
         steps='1. Caller dials the tenant number. 2. AI identifies itself as AI in the caller language. 3. Recording consent prompt per pack. 4. Booking via the calendar adapter with verbal read-back. 5. Transcript and summary; CRM sync approved. 6. Coaching feedback generated from the consented recording',
         expected='Disclosure within the first utterance; recording only after the consent the pack requires (all-party in DE); booking once; transcript persisted only with a recording basis; coaching uses only recordings with a coaching purpose; human hand-off offered and works; all audio and transcripts in {Z}',
         P='P0', typ='T19, T14', rel='R2'),
    dict(j='J-T-07', title='Outbound AI voice campaign with registry scrubbing, calling window and hand-off',
         regions=[('IN', 'Kestrel Analytics, NCPR scrub, DLT-registered number series'), ('EU', 'Atelier Lumière SAS, Bloctel scrub, FR calling hours')],
         links='SM-SVC-26-WF02; DEC-777, 782; RP-IN-SMS (voice), RP-EU-MKT; TC-V12-Q-C3',
         steps='1. Campaign approved (script hash). 2. AU-280 preflight scrubs the list. 3. Calls placed inside the effective window. 4. One callee asks for a human. 5. One number is registry-listed',
         expected='Registry-listed numbers never dialled; calls only inside the stricter of 09:00–21:00 and the pack hours; AI disclosure; hand-off within the SLA; caller ID compliant; outcome per callee recorded once',
         P='P0', typ='T19', rel='R2'),
    dict(j='J-T-08', title='Investor journey: investor-mode website, private enquiry, eligibility and KYC, data room, two-person offer, receipt, allotment',
         regions=[('IN', 'Lumen Robotics Pvt Ltd, private placement to named investors (RP-IN-SEC)'), ('EU', 'Lumen Robotics GmbH, prospectus-exempt offer to qualified investors (RP-EU-PROSP)')],
         links='INV-SVC-01…16, 24; DEC-783; FR-V12-N/O; RP-AML-KYC, RP-INV-ADVICE; M-O1, M-O2 (Part 11.16d), PM-N-01…03 (Part 11.16e)',
         steps='1. Visitor submits a private enquiry (no offer content shown). 2. KYC and eligibility verification. 3. NDA and data-room grant. 4. Offer document approved by two people and issued to the named eligible investor. 5. Funds received from the investor\'s own account; reconciliation. 6. Allotment and statutory filing tasks',
         expected='No general solicitation; offer terms only to verified-eligible recipients; AI never gives investment advice; data-room access watermarked and logged; receipt reconciled before allotment; statutory clocks tracked; everything in {Z}',
         P='P0', typ='T19, T07', rel='R2'),
    dict(j='J-T-09', title='Managed-service operator runs a client campaign under a delegation grant until the grant expires',
         regions=[('IN', 'Harbor Foods Pvt Ltd (EXT-MSP) and operator Corvid Managed Services (R21)')],
         links='FR-ENH-A-015; ABAC-ENH-A-01…03; NT-ENH-A-05; TC-ENH-A-024…026',
         steps='1. Client approves grant G-1 (Outreach, sender S-1, budget B-1, 90 days). 2. R21 builds and runs a campaign. 3. R21 tries export and approval of claims. 4. Clock advanced past expiry',
         expected='Actions stamped with grant_id; export and claims approval refused; after expiry 403 DELEGATION_SCOPE and session context cleared; client sees the full trail',
         P='P0', typ='T07', rel='R2'),
    dict(j='J-T-10', title='Kill switch and mandate revocation while outreach, commerce and bid work is in flight',
         regions=[('IN', 'T1 portfolio'), ('EU', 'Nordlicht GmbH')],
         links='Part 11.17a §11.17.5.13; DEC-779; XT-15; PM-T03',
         steps='1. Start MT-OUT batch, MT-COM negotiation and MT-BID submission preparation. 2. R10 engages the tenant kill switch. 3. Resume with two-person approval. 4. Revoke MT-COM',
         expected='No new effect after the switch time (±1 s); reservations released; in-flight items held and reconciled; resume needs two people; revoked mandate never dispatches again',
         P='P0', typ='T19, T18', rel='R2'),
    dict(j='J-T-11', title='Disaster-recovery drill with an active mandate: standby promotion, RPO and RTO measured (KPI-32)',
         regions=[('IN', 'IN zone stack'), ('EU', 'EU zone stack')],
         links='DEC-771, 787; KPI-32; DR-V12-T-01…08; Part 11.19b DR-R1…R8; PM-T09',
         steps='1. Run LT-04 load with an MT-PAY pay-out batch. 2. Make the Supabase primary unavailable. 3. Promote the in-zone standby; replay the outbox. 4. Reconcile PSP truth',
         expected='Achieved RPO ≤ 15 min and RTO ≤ 120 min recorded in the drill evidence; no cross-zone copy used; no duplicate pay-out; drill evidence signed by SRE and QA',
         P='P0', typ='T12', rel='R1'),
    dict(j='J-T-12', title='Data-subject rights: export and erasure across database, files, recordings, indexes, logs and backups',
         regions=[('IN', 'DPDP request (RP-IN-DPDP)'), ('EU', 'GDPR request (RP-EU-MKT, GDPR rights)')],
         links='Part 4.1 privacy; RP-IN-DPDP; DEC-772; PM-T04',
         steps='1. Data principal submits a request. 2. Identity verified. 3. Export package built. 4. Erasure executed with legal-hold check. 5. Backups age out per retention',
         expected='Export complete within the statutory clock (verify); erasure covers rows, objects, recordings, embeddings and caches; legal-hold items retained with reason; backups never restored without re-applying erasures; all within {Z}',
         P='P0', typ='T19', rel='R2'),
    dict(j='J-T-13', title='Rule-pack lifecycle: counsel sign-off activates a capability; expiry suspends mandates',
         regions=[('IN', 'RP-IN-PAY for MT-PAY')],
         links='Part 11.15 §11.15.3.5; XT-10; DEC-779/780',
         steps='1. Pack in counsel review. 2. Counsel signs; AU-128 loads. 3. MT-PAY mandate activates. 4. Review date passes',
         expected='Capability inactive before signature; active after; on expiry every MT-PAY mandate in IN suspends within 1 min and R10 is notified',
         P='P0', typ='T19', rel='R2'),
    dict(j='J-T-14', title='Arabic right-to-left tenant: UI works in ar-AE, AE market blocked until its pack and zone are approved',
         regions=[('EU', 'Al Noor Trading FZ-LLC (EXT-SMB, ar-AE UI, EU zone by choice)')],
         links='DEC-776; Part 11.7c CONFLICT-872; PM-T06, PM-T07',
         steps='1. Onboard with ar-AE. 2. Use Admin and Website in RTL. 3. Try outreach to AE recipients',
         expected='RTL layout, mirrored icons, bidi-safe IDs; AE outreach blocked JURISDICTION_NOT_ENABLED until the AE pack is Approved; no data written outside the chosen zone',
         P='P1', typ='T13, T08', rel='R4'),
    dict(j='J-T-15', title='Vertical safety: EduVerse never contacts minors; MedMaarg never stores patient data',
         regions=[('IN', 'T1 EduVerse and MedMaarg')],
         links='DEC-030; MedMaarg rule; RP-EDU-MINORS, RP-HEALTH',
         steps='1. Import a list containing a learner aged 16. 2. Run SM-SVC-06 at L3. 3. Upload a document containing a patient record to MedMaarg',
         expected='Minor excluded before any draft; no message; patient record quarantined PROHIBITED_DATA_CLASS; R10 task; no AI call on the record',
         P='P0', typ='T19', rel='R1'),
    dict(j='J-T-16', title='Model registry change: candidate onboarding, affected EVAL suites, two-person approval, canary and rollback',
         regions=[('IN', 'IN registry rows'), ('EU', 'EU registry rows')],
         links='DEC-788; PM-T16; AU-054/057/154',
         steps='1. Add a candidate model row. 2. AU-154 selects affected suites. 3. Suites pass; two approvers approve. 4. Canary 5%. 5. Inject drift; roll back',
         expected='Candidate never routable before approval; canary limited; rollback restores the previous row in ≤ 5 min; all evaluation evidence stored per zone',
         P='P0', typ='T14', rel='R2'),
    dict(j='J-T-17', title='Cross-tenant benchmark published only for cohorts of at least 10 opted-in tenants with noise',
         regions=[('IN', 'IN cohort'), ('EU', 'EU cohort')],
         links='DEC-789; Part 11.19 M11',
         steps='1. 9 then 12 tenants opt in. 2. Compute reply-rate benchmark. 3. Tenant withdraws',
         expected='No publication at 9; publication at 12 with noise and no tenant-level value; withdrawal excludes the tenant from the next period; nothing crosses zones',
         P='P0', typ='T19, T15', rel='R2'),
    dict(j='J-T-18', title='Tenant offboarding: cancellation, portability export, retention and deletion schedule',
         regions=[('IN', 'Kestrel Analytics'), ('EU', 'Nordlicht GmbH')],
         links='Part 11.2 subscription engine; EP-20; DEC-772',
         steps='1. R12 cancels. 2. Portability export. 3. Grace period. 4. Deletion executed',
         expected='Export complete and signed; access ends at period end; deletion certificate; backups expire on schedule; meter and invoices final',
         P='P1', typ='T01, T19', rel='R1'),
]
PACKS = {'IN': 'IN packs', 'EU': 'EU packs'}
CURR = {'IN': 'INR', 'EU': 'EUR'}


def e2e_rows():
    out = []
    n = 1
    for j in J:
        for z, fx in j['regions']:
            tc = 'TC-V12-T-%03d' % n
            n += 1
            st = j['steps'].replace('{Z}', z)
            ex = j['expected'].replace('{Z}', z).replace('{P}', PACKS[z]).replace('{CUR}', CURR[z])
            out.append(dict(id=tc, j=j['j'], z=z, title='%s (%s zone): %s' % (j['j'], z, j['title']), links='TS-V12-T-17 · %s · %s' % (j['j'], j['links']),
                            pre='Pre: PP-06 (Chromium + WebKit) and PP-01 in the %s zone; SYN-T fixtures; provider simulators; clock control. Data: %s' % (z, fx),
                            steps=st, exp=ex, P=j['P'], typ=j['typ'], rel=j['rel']))
    return out


E2E = e2e_rows()

# =============================================================================================
# ID assignment for generated models
# =============================================================================================
ORDER = ['PM-T01', 'PM-T01N', 'PM-T02', 'PM-T02N', 'PM-T03', 'PM-T03P', 'PM-T03N', 'PM-T04', 'PM-T05', 'PM-T09',
         'XT-10', 'XT-11', 'XT-12', 'XT-13', 'XT-14', 'XT-15', 'PM-T06', 'PM-T07', 'PM-T08', 'PM-T16']
IDS = {}
n = 101
for mid in ORDER:
    rows = models[mid]
    IDS[mid] = (n, n + len(rows) - 1)
    for r in rows:
        r['id'] = 'TC-V12-T-%d' % n if n >= 1000 else 'TC-V12-T-%03d' % n
        n += 1
LAST = n - 1

SHORT = {'tenant': 'TEN', 'plan': 'PLAN', 'sku': 'SKU', 'region': 'REG', 'locale': 'LOC', 'role': 'ROLE', 'channel': 'CHN',
         'identity': 'IDN', 'device': 'DEV', 'browser': 'BRW', 'data': 'DAT', 'consent': 'CON', 'provider': 'PRV', 'autonomy': 'AUT',
         'ai_route': 'AIR', 'sla': 'SLA'}
MT = {'PM-T01': 'TC-V12-T-M01', 'PM-T01N': 'TC-V12-T-M01N', 'PM-T02': 'TC-V12-T-M02', 'PM-T02N': 'TC-V12-T-M02N',
      'PM-T03': 'TC-V12-T-M03', 'PM-T03P': 'TC-V12-T-M03P', 'PM-T03N': 'TC-V12-T-M03N', 'PM-T04': 'TC-V12-T-M04',
      'PM-T05': 'TC-V12-T-M05', 'PM-T06': 'TC-V12-T-M06', 'PM-T07': 'TC-V12-T-M07', 'PM-T08': 'TC-V12-T-M08',
      'PM-T09': 'TC-V12-T-M09', 'XT-10': 'TC-V12-T-X10', 'XT-11': 'TC-V12-T-X11', 'XT-12': 'TC-V12-T-X12',
      'XT-13': 'TC-V12-T-X13', 'XT-14': 'TC-V12-T-X14', 'XT-15': 'TC-V12-T-X15', 'PM-T16': 'TC-V12-T-A16'}


def data_cell(mid, row):
    r = row['row']
    if mid in ('PM-T01', 'PM-T01N'):
        parts = []
        for k, v in r.items():
            if k == 'sku':
                v = 'SM-SVC-' + v
            parts.append('%s %s' % (SHORT[k], v))
        return ' · '.join(parts)
    if mid in ('PM-T02', 'PM-T02N'):
        return ' · '.join(('INV-SVC-' + v) if k == 'sku' else v for k, v in r.items())
    return ' · '.join(str(v) for v in r.values())


def links_cell(mid, row):
    m = summary[mid] if mid in summary else {}
    ts = m.get('ts', '')
    r = row['row']
    rel = row.get('rel', '')
    if mid in ('PM-T01', 'PM-T01N'):
        s = r['sku']
        x = '%s · SM-SVC-%s (%s; %s%s) · %s' % (ts, s, C.EPIC[s], C.EFFECT[s], ('; ' + C.MANDATE[s]) if s in C.MANDATE else '', rel)
        if mid == 'PM-T01N':
            x += ' · fault %s' % row['neg'][1]
        return x
    if mid in ('PM-T02', 'PM-T02N'):
        x = '%s · INV-SVC-%s · %s' % (ts, r['sku'], rel)
        if mid == 'PM-T02N':
            x += ' · fault %s' % row['neg'][1]
        return x
    if mid.startswith('PM-T03'):
        wf = TM.EFFECTS[r['effect']][0]
        x = '%s · %s · %s' % (ts, wf, rel)
        if mid == 'PM-T03N':
            x += ' · fault %s=%s' % tuple(row['neg'])
        return x
    return '%s · %s' % (ts, rel)


def params_table(mid):
    m = TM.MODELS.get(mid)
    if m is None or m.get('params') is None:
        return ''
    lines = ['| Parameter | Values | Count |', '|---|---|---|']
    for k, vals in m['params'].items():
        vv = list(vals)
        if mid == 'PM-T16' and k == 'suite':
            show = 'EVAL-SM-SVC-01-WF01 … EVAL-SM-SVC-39-WF02 (the 111 suites of Part 11.6b, TC-V12-F-201…311)'
        elif k == 'sku' and mid == 'PM-T01':
            show = 'SM-SVC-01 … SM-SVC-39 (Service_Index.csv)'
        elif k == 'sku' and mid == 'PM-T02':
            show = 'INV-SVC-01 … INV-SVC-24'
        else:
            show = ' · '.join(map(str, vv))
        lines.append('| `%s` | %s | %d |' % (k, esc(show), len(vv)))
    return '\n'.join(lines)


def model_header(mid):
    s = summary[mid]
    m = TM.MODELS.get(mid)
    lo, hi = IDS[mid]
    rng = 'TC-V12-T-%s…TC-V12-T-%s' % (('%03d' % lo) if lo < 1000 else lo, ('%03d' % hi) if hi < 1000 else hi)
    out = []
    if m and m.get('params') is not None:
        out.append(params_table(mid))
        out.append('')
    v = s.get('verify', {})
    raw = s.get('raw')
    valid = s.get('valid')
    line = '**Method:** %s. ' % s['method']
    if raw:
        line += 'Raw product %s · valid %s · ' % ('{:,}'.format(raw), '{:,}'.format(valid) if valid else 'not enumerated (product too large; feasibility by AC-3 + search)')
    if s.get('tuples') and not s['method'].startswith('Exhaustive'):
        line += 'required t-tuples %s · ' % '{:,}'.format(v.get('required', s['tuples']))
    line += '**%d cases** (%s)' % (s['rows'], rng)
    if s.get('pw_only'):
        line += ' · pairwise alone would need %d' % s['pw_only']
    line += ' · verification: %d missing tuples, %d invalid rows%s.' % (v.get('missing', 0), v.get('invalid_rows', 0),
                                                                        (', %d tuples excluded by constraint' % v['excluded']) if v.get('excluded') else '')
    out.append(line)
    return '\n'.join(out)


def gen_table(mid):
    m = TM.MODELS.get(mid) or TM.MODELS.get(mid.rstrip('NP')) or TM.MODELS.get(mid[:-1])
    base = mid[:-1] if mid.endswith(('N', 'P')) and mid[:-1] in TM.MODELS else mid
    mm = TM.MODELS.get(mid) or TM.MODELS.get(base)
    lo, hi = IDS[mid]
    rng = 'TC-V12-T-%s…TC-V12-T-%s' % (('%03d' % lo) if lo < 1000 else lo, ('%03d' % hi) if hi < 1000 else hi)
    tech = mm['tech'] if mm else 'PW'
    if mid.endswith('N'):
        tech = 'EG, EP (single fault)'
    hdr = ['**Common for %s:** %s Links for every row: %s. Generated by `assembly/v12b/t_04_models.py` (model %s); IDs assigned by `t_05_build.py`.' % (
        rng, mm['common'] if mm else '', mm['links'] if mm else '', mid), '',
        '| ID | Data | Expected | Links | P | Type | Tech | Auto | Lvl |', '|---|---|---|---|---|---|---|---|---|']
    for r in models[mid]:
        auto = r.get('auto', 'Y')
        hdr.append('| %s | %s | %s | %s | %s | %s | %s | %s | %s |' % (r['id'], esc(data_cell(mid, r)), esc(r['exp']), esc(links_cell(mid, r)),
                                                                     r['P'], r['type'], tech, auto, r.get('lvl', 'SYS')))
    return '\n'.join(hdr)


def ai_table():
    mid = 'PM-T16'
    lines = ['| ID | Title | Links | Test data | Steps | Expected result | P | Type | Tech | Auto | Level |', '|---|---|---|---|---|---|---|---|---|---|---|']
    ev = {e['suite']: e for e in C.EVAL}
    for r in models[mid]:
        e = ev[r['row']['suite']]
        exp = r['exp'].split('. Expected: ')
        test_data = 'Gold set of %s, %s; %s cases per suite (labelled + adversarial), slice %s; agents %s; registry fixture REG-FIX-3 (%s)' % (
            e['suite'], e['workflow'], e['cases'], r['row']['locale_slice'], e['agents'], r['row']['zone'])
        steps = '1. Apply the trigger "%s". 2. AU-154 selects %s. 3. Replay on "%s" in the %s zone (%s). 4. Score with the gate families %s; inject "%s". 5. Read gate decision, AU-154 sign-off state and alerts' % (
            r['row']['trigger'], e['suite'], r['row']['model_row'], r['row']['zone'], r['row']['judge'], e['gates'], r['row']['injected'])
        links = 'TS-V12-T-16 · %s · %s (%s) · %s · AIX-05, AIX-19 · %s' % (e['tc'], e['suite'], e['agt'], e['workflow'], r['rel'])
        lines.append('| %s | %s | %s | %s | %s | %s | %s | %s | %s | %s | %s |' % (
            r['id'], esc(r['title']), esc(links), esc(test_data), esc(steps), esc(exp[1] if len(exp) > 1 else exp[0]), r['P'], r['type'], 'PW (VS)', 'Y', r['lvl']))
    return '\n'.join(lines)


def e2e_table():
    lines = ['| ID | Title | Links | Preconditions · Test data | Steps | Expected result | P | Type | Tech | Auto | Lvl |', '|---|---|---|---|---|---|---|---|---|---|---|']
    for r in E2E:
        lines.append('| %s | %s | %s | %s | %s | %s | %s | %s | UC | Y | E2E |' % (r['id'], esc(r['title']), esc(r['links'] + ' · ' + r['rel']),
                                                                             esc(r['pre']), esc(r['steps']), esc(r['exp']), r['P'], r['typ']))
    return '\n'.join(lines)


def e2e_register():
    lines = ['| Journey | Title | Zones | TCs | Release | UAT pack |', '|---|---|---|---|---|---|']
    pk = {'J-T-01': 'UAT-PK-V12-01', 'J-T-02': 'UAT-PK-V12-02', 'J-T-03': 'UAT-PK-V12-03', 'J-T-04': 'UAT-PK-V12-03',
          'J-T-05': 'UAT-PK-V12-04', 'J-T-06': 'UAT-PK-V12-05', 'J-T-07': 'UAT-PK-V12-05', 'J-T-08': 'UAT-PK-V12-06',
          'J-T-09': 'UAT-PK-V12-07', 'J-T-10': 'UAT-PK-V12-08', 'J-T-11': 'UAT-PK-V12-09', 'J-T-12': 'UAT-PK-V12-10',
          'J-T-13': 'UAT-PK-V12-08', 'J-T-14': 'UAT-PK-V12-11', 'J-T-15': 'UAT-PK-V12-12', 'J-T-16': 'UAT-PK-V12-13',
          'J-T-17': 'UAT-PK-V12-13', 'J-T-18': 'UAT-PK-V12-10'}
    for j in J:
        ids = [r['id'] for r in E2E if r['j'] == j['j']]
        lines.append('| %s | %s | %s | %s | %s | %s |' % (j['j'], esc(j['title']), ', '.join(z for z, _ in j['regions']), ', '.join(ids), j['rel'], pk[j['j']]))
    return '\n'.join(lines)


def counts_table():
    lines = ['| Model | Title | Parameters (values) | Raw product | Valid | Method | Required t-tuples | Cases | Pairwise-only size | Missing after verification | TC range |',
             '|---|---|---|---|---|---|---|---|---|---|---|']
    tot = 0
    for mid in ORDER:
        s = summary[mid]
        lo, hi = IDS[mid]
        par = s.get('params') or {}
        ptxt = '%d (%d)' % (len(par), sum(par.values())) if par and mid != 'XT-14' else ('2 (boundary set)' if mid == 'XT-14' else '— (layer of the parent model)')
        raw = s.get('raw')
        valid = s.get('valid')
        req = s.get('verify', {}).get('required', '—')
        lines.append('| %s | %s | %s | %s | %s | %s | %s | %d | %s | %s | TC-V12-T-%s…%s |' % (
            mid, esc(s['title']), ptxt, '{:,}'.format(raw) if raw else '—', '{:,}'.format(valid) if valid else ('not enumerated' if raw else '—'),
            esc(s['method']), '{:,}'.format(req) if isinstance(req, int) else req, s['rows'], s.get('pw_only') or '—',
            s.get('verify', {}).get('missing', 0), ('%03d' % lo) if lo < 1000 else lo, ('%03d' % hi) if hi < 1000 else hi))
        tot += s['rows']
    lines.append('| **Total generated** | | | | | | | **%d** | | **0** | TC-V12-T-101…%d |' % (tot, LAST))
    return '\n'.join(lines), tot


COUNTS, GEN_TOTAL = counts_table()


def ts_table():
    rows = [('TS-V12-T-01', 'Platform SKU invocation across tenant, plan, SKU, zone, locale, role, channel, identity, device, browser, data, consent, provider, autonomy, AI route and SLA', 'PM-T01, PM-T01N', 'P0'),
            ('TS-V12-T-02', 'Investment Automation SKU invocation with securities packs and investor eligibility', 'PM-T02, PM-T02N', 'P0'),
            ('TS-V12-T-03', 'Consequential-effect gateway: every effect type under every control (money, law, safety)', 'PM-T03, PM-T03P, PM-T03N', 'P0'),
            ('TS-V12-T-04', 'Data residency India and EU across components, operations and actors (CJ-TC-09)', 'PM-T04', 'P0'),
            ('TS-V12-T-05', 'Multi-tenant isolation and RLS across access paths', 'PM-T05', 'P0'),
            ('TS-V12-T-06', 'Localization and right-to-left', 'PM-T06', 'P1'),
            ('TS-V12-T-07', 'Accessibility WCAG 2.2 AA', 'PM-T07', 'P1'),
            ('TS-V12-T-08', 'Performance, load, stress, spike and soak', 'PM-T08', 'P0'),
            ('TS-V12-T-09', 'Resilience and DR with consequential work in flight', 'PM-T09', 'P0'),
            ('TS-V12-T-10', 'Rule-pack state × capability activation', 'XT-10', 'P0'),
            ('TS-V12-T-11', 'Subscription, entitlement and metering', 'XT-11', 'P0'),
            ('TS-V12-T-12', 'Messaging window boundaries', 'XT-12', 'P0'),
            ('TS-V12-T-13', 'On-call and incident communication by tier', 'XT-13', 'P0'),
            ('TS-V12-T-14', 'Service-credit ladder boundaries', 'XT-14', 'P1'),
            ('TS-V12-T-15', 'Two-person approval and SoD for mandates', 'XT-15', 'P0'),
            ('TS-V12-T-16', 'AI evaluation gates of the 111 V12 suites', 'PM-T16', 'P0'),
            ('TS-V12-T-17', 'Cross-capability end-to-end journeys per zone', 'J-T-01…18', 'P0')]
    lines = ['| ID | Title | Model / journeys | Test cases | Priority |', '|---|---|---|---|---|']
    for ts, t, mods, p in rows:
        if ts == 'TS-V12-T-17':
            rng = '%s…%s' % (E2E[0]['id'], E2E[-1]['id'])
        else:
            ms = [m.strip() for m in mods.split(',')]
            lo = min(IDS[m][0] for m in ms)
            hi = max(IDS[m][1] for m in ms)
            rng = 'TC-V12-T-%s…TC-V12-T-%s' % (('%03d' % lo) if lo < 1000 else lo, hi)
        lines.append('| %s | %s | %s | %s | %s |' % (ts, t, mods, rng, p))
    return '\n'.join(lines)


# ----------------------------------------------------------------------------- traceability rollup
def rollup_tables():
    pp = inv['per_part']
    lines = ['| Part (group) | Test cases defined (unique IDs) | Main families |', '|---|---|---|']
    pre, post = 0, 0
    for part, fams in pp.items():
        tc = sum(v for k, v in fams.items() if k != 'TS')
        fam = ', '.join('%s %d' % (k, v) for k, v in sorted(fams.items(), key=lambda x: -x[1]) if k != 'TS')
        lines.append('| %s | %d | %s |' % (part, tc, fam))
        if part.startswith('Part 11'):
            post += tc
        else:
            pre += tc
    t1 = '\n'.join(lines)
    j_classes = 19
    j_inst = 2275
    total_rows = inv['tc_unique']
    exec_total = total_rows - j_classes + j_inst
    t11 = len(E2E) + GEN_TOTAL
    lines = ['| Measure | Count | Basis |', '|---|---|---|',
             '| Test cases defined in Parts 2.6–9.10 (before V12) | %d | `t_01_inventory.py` scan of table rows; the V12 brief quotes 4,156 (difference: worked examples and aliases counted once in rows) |' % pre,
             '| Test cases defined in Parts 11.1–11.19 | %d | Same scan |' % post,
             '| Unique test-case IDs defined before Part 11.21 | %d | Same scan, de-duplicated across files |' % total_rows,
             '| minus Part 11.10 class definitions TC-V12-J-001…019 (counted through instances) | −%d | Part 11.10b §11.10.4.5 |' % j_classes,
             '| plus executable instances of those classes (1,342 scenarios, 517 steps, 156 AT01, 39 ENT-AT01, 221 canonical acceptance rows) | +%d | Part 11.10b §11.10.4.5 |' % j_inst,
             '| **Executable test cases before Part 11.21** | **%d** | |' % exec_total,
             '| Part 11.21 end-to-end journey cases (full form) | +%d | §11.21.7 |' % len(E2E),
             '| Part 11.21 generated combinatorial cases | +%d | §11.21.6 |' % GEN_TOTAL,
             '| **Executable test cases after Part 11.21** | **%d** | |' % (exec_total + t11),
             '| Test scenarios (TS) defined | %d + 17 | scan + TS-V12-T-01…17 |' % inv['ts_unique'],
             '| Evaluation suites bound as gates (not counted as tests) | 111 | EVAL-SM-SVC-##-WF## |']
    t2 = '\n'.join(lines)
    return t1, t2, exec_total, exec_total + t11


ROLL1, ROLL2, EXEC_BEFORE, EXEC_AFTER = rollup_tables()


def release_table():
    c = collections.defaultdict(collections.Counter)
    for mid in ORDER:
        for r in models[mid]:
            c[mid][r.get('rel', 'R1')] += 1
    for r in E2E:
        c['E2E (J-T)'][r['rel']] += 1
    lines = ['| Model | R1 | R2 | R3 | R4 | Total |', '|---|---|---|---|---|---|']
    tot = collections.Counter()
    for mid in ORDER + ['E2E (J-T)']:
        cc = c[mid]
        lines.append('| %s | %d | %d | %d | %d | %d |' % (mid, cc['R1'], cc['R2'], cc['R3'], cc['R4'], sum(cc.values())))
        tot.update(cc)
    lines.append('| **Total** | **%d** | **%d** | **%d** | **%d** | **%d** |' % (tot['R1'], tot['R2'], tot['R3'], tot['R4'], sum(tot.values())))
    cum = []
    run = 0
    for rr in ('R1', 'R2', 'R3', 'R4'):
        run += tot[rr]
        cum.append('%s %d' % (rr, run))
    return '\n'.join(lines) + '\n\nCumulative regression size of the Part 11.21 cases at each release gate: ' + ' · '.join(cum) + '.', tot


REL_TABLE, REL_TOT = release_table()


def prio_table():
    c = collections.Counter()
    for mid in ORDER:
        for r in models[mid]:
            c[r['P']] += 1
    for r in E2E:
        c[r['P']] += 1
    return ' · '.join('%s %d' % (k, c[k]) for k in ('P0', 'P1', 'P2', 'P3'))


PRIO = prio_table()


def catalogue_table():
    lines = ['| ID | Dimension | Code | Values | Source | Notes |', '|---|---|---|---|---|---|']
    for pid, dim, code, vals, src, note in C.CATALOGUE:
        lines.append('| %s | %s | %s | %s | %s | %s |' % (pid, dim, code, esc(' · '.join(vals)), esc(src), esc(note)))
    return '\n'.join(lines)


def sku_table():
    lines = ['| SKU | Service | Bundle | Meter unit | Effect class | Mandate type | Max level | Epic | First release | AI suites |', '|---|---|---|---|---|---|---|---|---|---|']
    ev = collections.Counter(re.search(r'SM-SVC-(\d\d)', e['suite']).group(1) for e in C.EVAL)
    for k, v in C.SM.items():
        s = k[-2:]
        mx = 'L4 (plan)' if s in C.L4_OK else ('L3' if s in C.MANDATE else ('L4 internal' if C.EFFECT[s] in ('R0', 'R1') else 'L2'))
        lines.append('| %s | %s | %s | %s | %s | %s | %s | %s | %s | %d |' % (k, esc(v['name']), esc(v['bundle']), esc(v['meter']), C.EFFECT[s],
                                                                          C.MANDATE.get(s, '—'), mx, C.EPIC[s], C.REL_SKU[s], ev.get(s, 0)))
    return '\n'.join(lines)


def inv_sku_table():
    lines = ['| SKU | Service | Group | Roles that operate it (PM-T02) | Offer content |', '|---|---|---|---|---|']
    for k, v in C.INV.items():
        s = k[-2:]
        roles = ', '.join(r for r, sk in TM.INV_ROLE.items() if s in sk)
        lines.append('| %s | %s | %s | %s | %s |' % (k, esc(v['name']), esc(v['bundle']), roles, 'Yes' if s in TM.OFFER_SKUS else 'No'))
    return '\n'.join(lines)


def role_table():
    lines = ['| Role | Name | Action in PM-T01 | Channels | Identity methods | SKUs operated |', '|---|---|---|---|---|---|']
    for r, nm in C.ROLES.items():
        sk = TM.ROLE_SKUS[r]
        sks = 'all 39' if len(sk) == 39 else ('%d: ' % len(sk) + ', '.join(sk))
        lines.append('| %s | %s | %s | %s | %s | %s |' % (r, esc(nm), esc(C.ROLE_ACTION[r]), ', '.join(TM.ROLE_CH[r]), ', '.join(TM.ROLE_IDN[r]), sks))
    return '\n'.join(lines)


def neg_table(neglist, model):
    lines = ['| Parameter | Invalid value | Expected (oracle) | P |', '|---|---|---|---|']
    for x in neglist:
        p, v = x[0], x[1]
        exp = x[3] if model == '01' else x[2]
        P = x[4] if model == '01' else x[3]
        lines.append('| `%s` | %s | %s | %s |' % (p, esc(v.lstrip('~')), esc(exp), P))
    return '\n'.join(lines)


def effects_table():
    lines = ['| Effect | Workflow | Mandate type | Personal recipient | ALLOW outcome (oracle) |', '|---|---|---|---|---|']
    for e, (wf, mt, pers, allow) in TM.EFFECTS.items():
        lines.append('| %s | %s | %s | %s | %s |' % (e, wf, mt or 'none (per-item approval only)', 'Yes' if pers else 'No', esc(allow)))
    return '\n'.join(lines)


def verdict_line(mid):
    c = collections.Counter(r.get('verdict') for r in models[mid])
    return 'Outcome mix: ALLOW %d · HOLD %d · BLOCK %d.' % (c['ALLOW'], c['HOLD'], c['BLOCK'])


PH = {
    'CATALOGUE': catalogue_table(), 'SKU_TABLE': sku_table(), 'INV_SKU_TABLE': inv_sku_table(), 'ROLE_TABLE': role_table(),
    'COUNTS': COUNTS, 'GEN_TOTAL': str(GEN_TOTAL), 'TS_TABLE': ts_table(), 'E2E_TABLE': e2e_table(), 'E2E_REGISTER': e2e_register(),
    'E2E_COUNT': str(len(E2E)), 'ROLL_PARTS': ROLL1, 'ROLL_TOTAL': ROLL2, 'EXEC_BEFORE': '{:,}'.format(EXEC_BEFORE),
    'EXEC_AFTER': '{:,}'.format(EXEC_AFTER), 'REL_TABLE': REL_TABLE, 'PRIO': PRIO, 'AI_TABLE': ai_table(),
    'NEG01_TABLE': neg_table(TM.NEG01, '01'), 'NEG02_TABLE': neg_table(TM.NEG02, '02'), 'EFFECTS_TABLE': effects_table(),
    'ALL_TOTAL': str(GEN_TOTAL + len(E2E)), 'LAST_ID': str(LAST), 'TC_UNIQUE': '{:,}'.format(inv['tc_unique']),
}
for mid in ORDER:
    PH['HDR_' + mid] = model_header(mid)
    PH['TAB_' + mid] = gen_table(mid) if mid != 'PM-T16' else ai_table()
for mid in ('PM-T03', 'PM-T03P', 'PM-T03N'):
    PH['VERDICT_' + mid] = verdict_line(mid)


def build(src, dst):
    t = open(SRC + '/' + src, encoding='utf-8').read()

    def rep(m):
        k = m.group(1)
        if k not in PH:
            raise KeyError(k)
        return PH[k]
    t = re.sub(r'\{\{([A-Z0-9_-]+)\}\}', rep, t)
    open(BP + '/' + dst, 'w', encoding='utf-8').write(t)
    print(dst, len(t))


FILES = [('a.md', 'Part-11-21a_Master_Test_Strategy_Organisation_Logistics_and_Capability_Strategies.md'),
         ('b.md', 'Part-11-21b_Master_Parameter_Catalogue_Combinatorial_Design_and_Platform_Cases.md'),
         ('c.md', 'Part-11-21c_Combinatorial_Cases_Money_Law_Safety_Residency_Isolation_Resilience.md'),
         ('d.md', 'Part-11-21d_Combinatorial_Cases_Localization_Accessibility_Performance_AI_Evaluation.md'),
         ('e.md', 'Part-11-21e_End_to_End_Suites_Traceability_Rollup_Regression_and_Decisions.md')]
if __name__ == '__main__':
    json.dump(dict(gen_total=GEN_TOTAL, e2e=len(E2E), last=LAST, ids={k: v for k, v in IDS.items()}, exec_before=EXEC_BEFORE,
                   exec_after=EXEC_AFTER, prio=PRIO, rel=dict(REL_TOT)), open(OUT + '/build.json', 'w'), indent=1)
    for s, d in FILES:
        if os.path.exists(SRC + '/' + s):
            build(s, d)
    print('generated', GEN_TOTAL, 'e2e', len(E2E), 'last', LAST, 'exec before', EXEC_BEFORE, 'after', EXEC_AFTER, PRIO)
