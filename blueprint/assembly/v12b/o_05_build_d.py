"""Build Part-11-16d: securities rule packs, epics, stories, tests, combinatorial models, cost, decisions, tags, quality gate."""
import json, sys
sys.path.insert(0, '/home/user/Allinonecalculator/blueprint/assembly/v12b')
from o_common import *
from o_packs import P, VR

ST = json.load(open(BP + 'assembly/v12b/o_state.json'))
out = []
w = out.append

def yaml_pack(pid, p):
    y = [f'pack_id: {pid}', 'version: 0.1-draft', 'state: draft', f'jurisdictions: "{p["juris"]}"', 'owner: R10', 'review_cadence: quarterly_and_event_driven',
         'expires_after_days: 120', 'fail_closed: true', 'activation_gate: ADR-235  # counsel sign-off + R10 approval per jurisdiction', 'rules:']
    for (rid, text, cit, applies, chk, det, sev, ev, rem) in p['rules']:
        y.append(f'  - rule_id: {rid}')
        y.append(f'    check: {chk}')
        y.append(f'    severity: {sev.split(" ")[0].lower()}')
        y.append(f'    applies_to: "{applies}"')
        y.append(f'    citation: "{cit}"')
        y.append(f'    detection: "{det.replace(chr(34), chr(39))}"')
        y.append(f'    remediation: "{rem.replace(chr(34), chr(39))}"')
        y.append('    override: none' if sev.startswith('Block') else '    override: r10_ack')
        if rid == 'RP-AML-KYC-013':
            y.append('    effective_from: 2027-07-10')
        else:
            y.append('    effective_from: on_signoff')
    y.append('phrase_lists:')
    for (lid, name, terms, mode, sev, used) in p['phrases']:
        y.append(f'  - id: {lid}')
        y.append(f'    match: {mode.split(" ")[0]}')
        y.append(f'    severity: {sev.split(" ")[0].lower()}')
        y.append(f'    terms: [{", ".join(chr(34) + t.strip().replace(chr(34), "") + chr(34) for t in terms.split(";"))}]')
    y.append('templates: [' + ', '.join(t[0] for t in p['templates']) + ']')
    return '\n'.join(y)

w('# AI Growth Engine: Employee Sales & Marketing Automation')
w('## Application Blueprint: PART 11 (Batch 11.16d), Investment Automation II: INV-SVC-13…24 and Securities Rule Packs (d: securities rule packs, epics, stories, tests, combinatorial design, effort and cost, decisions)')
w('')
w(tbl(['Field', 'Value'], [
 ['Document', 'Part 11, Batch 16, file **d** of Group O (continues Part 11.16c). Holds §11.16.15.20–§11.16.15.32 and §11.16.16–§11.16.20'],
 ['Version', '1.0 · 28 Nov 2026 (document); every pack inside is **v0.1-draft**'],
 ['Baseline', 'As Part 11.16c; template of Part 11.15a §11.15.3 and §11.15.4 (pack sections .1–.11), Part 5.1a (stories), Part 6.1/6.2a/6.4 (tests), Part 8.4 and DEC-770 (rates)'],
 ['Roles applied', 'As Part 11.16c; counsel-facing sections written by the securities-law and compliance lawyer and the compliance engineer'],
 ['ID ranges used', 'Rule IDs `RP-<PACK>-NNN` · phrase lists `PL-<PACK>-NN` · templates `TPL-<PACK>-NN` · pack tests `TC-RP-<PACK>-NN` · verification entries VR-O-01…24 · DEC-820…839 · ADR-235…239 · tags 1020…1039 · US-32-ZO01…10, US-33-ZO01…15 · TC-V12-O-###'],
]))
w('')
w('> **DISCLAIMER: DRAFT FOR REVIEW BY QUALIFIED COUNSEL. THIS IS NOT LEGAL ADVICE.** Every rule, citation, threshold, effective date and template below is a proposal for review, correction and sign-off by counsel admitted in the relevant jurisdiction. No pack may be activated, and no offer-related action may be allowed in any jurisdiction, until counsel has signed the pack and R10 has approved it (ADR-235; CP-05).')
w('')
w('---')
w('')
w('### 11.16.15.20 Securities rule packs: framework additions to Part 11.15')
w('')
w('#### 11.16.15.20.1 Scope and relationship to Part 11.15')
w('')
w('The seven packs below use the Part 11.15 schema, severity model, cross-pack precedence (CP-01…CP-07), versioning and quarterly review procedure **unchanged**. The reviewer for offer-related content is **AG-198**, which applies the AG-086 contract (G-1…G-9) to securities; AG-199 enforces RP-INV-ADVICE. Part 11.15a §11.15.1 states that "no pack contains securities-marketing rules" and that RP-COMMIT-020 blocks fundraising content; after DEC-783 this applies to the **Sales & Marketing product only**. For tenants entitled to INV SKUs, RP-COMMIT-020 is replaced by these packs (DEC-830; CONFLICT-1028).')
w('')
w('**Alignment with Group N pack names (Part 11.16a §11.16.5.2.1).** Group N consumes the packs under consolidated `RP-SEC-*` names; they resolve to the packs written here as follows (one schema, one registry, AU-128):')
w('')
w(tbl(['Group N name', 'Pack and rules in this part'], [
 ['RP-SEC-IN-PP', 'RP-IN-SEC-001…015, 019, 021, 022'], ['RP-SEC-IN-FEMA', 'RP-IN-SEC-016…018'], ['RP-SEC-IN-ICDR', 'RP-IN-SEC-020 (listed issuers out of scope in v0.1: Block until a dedicated pack is approved)'],
 ['RP-SEC-US-506B', 'RP-US-REGD with route 506b (001–004, 008–015)'], ['RP-SEC-US-506C', 'RP-US-REGD with route 506c (001, 003, 005–007, 009–015)'], ['RP-SEC-US-CF', 'RP-US-REGCF'],
 ['RP-SEC-EU-PR', 'RP-EU-PROSP'], ['RP-SEC-UK-FP', 'RP-UK-FINPROM'], ['(channel/privacy packs)', 'RP-IN-WA, RP-IN-DPDP, RP-EU-MKT, RP-US-EMAIL (Part 11.15) unchanged; plus RP-AML-KYC and RP-INV-ADVICE here'],
]))
w('')
w('**Additional rules for securities packs.**')
w('')
w(tbl(['Rule', 'Statement'], [
 ['CP-O-01 (route)', 'An offer carries one route per jurisdiction (IN private placement; US 506(b) / 506(c) / Reg CF hand-off; EU exemption code or ECSP hand-off; UK FPO basis or s.21 approval). The applicable set = issuer-jurisdiction pack + every investor-jurisdiction pack + RP-AML-KYC + RP-INV-ADVICE'],
 ['CP-O-02 (investor jurisdiction)', 'Investor jurisdiction is resolved from verified residence (KYC address) first, then J1–J7 of §11.15.3.4; corroborating signals add jurisdictions, never remove them; unresolved → Block'],
 ['CP-O-03 (both ends)', 'An offer from an IN issuer to a UK investor must satisfy RP-IN-SEC (issuer side: s.42 count, offer letter, FEMA) **and** RP-UK-FINPROM (recipient side: FPO basis). Strictest wins on shared parameters (CP-03)'],
 ['CP-O-04 (no mandate)', 'No DEC-779 mandate can authorise an action governed by these packs (allotment, filing, offer issue, promotion dispatch, KYC decision) (DEC-822)'],
 ['CP-O-05 (hand-off routes)', 'Reg CF, ECSP and UK crowdfunding routes are hand-offs: the platform never accepts commitments or money for them'],
]))
w('')
w('#### 11.16.15.20.2 Citation verification register (Group O)')
w('')
w(tbl(['VR', 'Instrument / fact', 'Status', 'Result / caveat', 'Source'], [list(v) for v in VR]))
w('')
w('Primary-text hosts (indiacode, MCA, indiankanoon, taxmann) could not be fetched from this environment; confirmation is from official secondary copies (SEC, FCA, RBI, EUR-Lex listings, legislation.gov.uk) and reputable law-firm notes. Counsel must read the primary text for every rule [GAP-1025].')
w('')
w('#### 11.16.15.20.3 Jurisdiction × route activation matrix (A258)')
w('')
w(tbl(['Issuer → / Investor ↓', 'IN', 'US', 'EU (member state)', 'UK'], [
 ['IN issuer', 'RP-IN-SEC (private placement only)', 'RP-IN-SEC + RP-US-REGD (506(b)/(c)) + FEMA rows of RP-IN-SEC', 'RP-IN-SEC + RP-EU-PROSP (exemption; overlay per state)', 'RP-IN-SEC + RP-UK-FINPROM (FPO basis)'],
 ['US issuer', 'RP-US-REGD + RP-IN-SEC-019/020 recipient view (counsel: Indian resident outbound investment rules) → Held in v0.1', 'RP-US-REGD or RP-US-REGCF (hand-off)', 'RP-US-REGD + RP-EU-PROSP', 'RP-US-REGD + RP-UK-FINPROM'],
 ['UK issuer', 'Held in v0.1 (counsel)', 'RP-UK-FINPROM (s.755/POATRs) + RP-US-REGD', 'RP-UK-FINPROM + RP-EU-PROSP', 'RP-UK-FINPROM'],
 ['EU issuer', 'Held in v0.1 (counsel)', 'RP-EU-PROSP + RP-US-REGD', 'RP-EU-PROSP (home + host overlays)', 'RP-EU-PROSP + RP-UK-FINPROM'],
 ['All', 'RP-AML-KYC + RP-INV-ADVICE always', '', '', ''],
]))
w('')
w('```mermaid')
w('flowchart TD')
w('  A["Offer-related action"] --> B["Resolve issuer and investor jurisdictions<br/>CP-O-02"]')
w('  B --> C["Build applicable set<br/>CP-O-01 and CP-O-03"]')
w('  C --> D{"Every pack active,<br/>signed, not expired?"}')
w('  D -- "No" --> X["Block PACK_NOT_ACTIVE"]')
w('  D -- "Yes" --> E{"Route is a hand-off?"}')
w('  E -- "Yes" --> H["Hand-off link only<br/>no commitments or money"]')
w('  E -- "No" --> F["DET rules incl. AU-230 counters"]')
w('  F --> G["AG-198 AI rules"]')
w('  G --> I{"Any Block?"}')
w('  I -- "Yes" --> Y["Verdict block"]')
w('  I -- "No" --> J["R10 approval of hash"]')
w('```')
w('')

sec = 21
for pid in ['RP-IN-SEC', 'RP-US-REGD', 'RP-US-REGCF', 'RP-EU-PROSP', 'RP-UK-FINPROM', 'RP-AML-KYC', 'RP-INV-ADVICE']:
    p = P[pid]
    base = f'11.16.15.{sec}'
    w(f'### {base} {pid}: {p["title"]}')
    w('')
    w(f'#### {base}.1 Pack metadata')
    w('')
    w(tbl(['Field', 'Value'], [
     ['Pack ID', pid], ['Title', p['title']], ['Version / state', 'v0.1-draft · `draft`'], ['Jurisdiction(s)', p['juris']], ['Channels', p['channels']], ['Audiences', p['audiences']],
     ['Startups', 'Tenants entitled to INV SKUs (Owner Portfolio startups and external SaaS tenants); adoptable, tighten-only (CP-04)'], ['Legal sources', p['sources']], ['Effective dates', p['effective']],
     ['Owner', 'R10 Legal/Compliance'], ['Review cadence', 'Quarterly + event-driven (§11.15.3.5)'], ['Expiry / fail-closed', '`expires_at` = last review + 120 days; suspended pack → all in-scope offer-related actions Block (CP-05)'], ['Depends on', p['depends']],
    ]))
    w('')
    w(f'#### {base}.2 Plain-language summary')
    w('')
    for i, s in enumerate(p['summary'], 1):
        w(f'{i}. {s}')
    w('')
    w(f'#### {base}.3 Definitions')
    w('')
    w(tbl(['Term', 'Definition for this pack'], p['defs']))
    w('')
    w(f'#### {base}.4 Rules')
    w('')
    w(tbl(['Rule ID', 'Obligation (draft legal wording)', 'Citation', 'Applies to', 'Check', 'Detection logic / pattern', 'Severity', 'Required evidence', 'Remediation message shown to user'], [list(r) for r in p['rules']]))
    w('')
    w(f'#### {base}.5 Required disclosures and approved template wording')
    w('')
    w(tbl(['Template', 'Use', 'English (approved draft wording)', 'Hindi (approved draft wording)', 'Placement'], [list(t) for t in p['templates']]))
    w('')
    w(f'#### {base}.6 Prohibited content and phrase lists')
    w('')
    w(tbl(['List', 'Name', 'Terms', 'Match mode', 'Severity', 'Used by'], [list(t) for t in p['phrases']]))
    w('')
    w(f'#### {base}.7 Exceptions and edge cases')
    w('')
    w(tbl(['#', 'Case', 'Treatment'], [list(t) for t in p['exceptions']]))
    w('')
    w(f'#### {base}.8 AG-198 / AG-199 review prompt guidance ({pid})')
    w('')
    for g in p['guidance']:
        w(f'- {g}')
    w('- **Never:** conclude that an offer is lawful; return `needs_counsel` when uncertain (G-4).')
    w('')
    w(f'#### {base}.9 Test cases')
    w('')
    w(tbl(['ID', 'Rule', 'Type', 'Input (summary)', 'Expected'], [[f'TC-{pid}-{i:02d}', t[0], t[1], t[2], t[3]] for i, t in enumerate(p['tests'], 1)]))
    w('')
    w(f'#### {base}.10 Machine-readable YAML (AU-128)')
    w('')
    w('```yaml')
    w(yaml_pack(pid, p))
    w('```')
    w('')
    w(f'#### {base}.11 Counsel sign-off block')
    w('')
    w(tbl(['Field', 'Entry'], [
     ['Pack / version reviewed', f'{pid} v0.1-draft → proposed v1.0'],
     ['Reviewer (name, admission / enrolment no., jurisdiction)', '_______________________ (' + p['counsel'] + ')'],
     ['Firm', '_______________________'], ['Date of review', '____ / ____ / ______'],
     ['Rules approved as drafted', '☐ All ☐ All except: __________'], ['Rules amended (IDs and summary)', '_______________________'],
     ['Citations confirmed against primary text (VR entries)', ' '.join('☐ ' + v for v in p['signoff_vr'])],
     ['Thresholds and effective dates confirmed', '☐ Yes ☐ With changes: __________'],
     ['Jurisdictions / member states / routes activated', '_______________________'],
     ['Conditions or limitations of the sign-off', '_______________________'],
     ['Next review due', '____ / ____ / ______ (≤ 120 days)'],
     ['R10 approval (name, date)', '_______________________'],
     ['Signature (counsel) / Signature (R10)', '_______________ / _______________'],
    ]))
    w('')
    sec += 1

# =========================================================== epics
w('### 11.16.15.28 Epics EP-32 and EP-33')
w('')
w(tbl(['Field', 'EP-32', 'EP-33'], [
 ['Title', 'Investment Closing, Investor Lifecycle and Engagement Operations', 'Specialised Funding, Ownership, Governance, Verification and Securities Compliance'],
 ['Goal', 'Verified, legally gated closing; accurate investor reporting; evidence-based pipeline; secure private intake', 'Grant/debt/readiness/ESG support; authoritative cap table and governance; cross-border and KYC hand-offs; seven securities packs with counsel activation'],
 ['Services', 'INV-SVC-13, 14, 15, 16; investor portal W77–W90', 'INV-SVC-17…24; packs; A254–A259; W91–W99'],
 ['FRs', 'FR-V12-O-001…012 (shared), ' + ', '.join(FR[s][0] + '/' + FR[s][1][-3:] for s in OURS[:4]) + ', workflow FRs of SVC-13…16', ', '.join(FR[s][0] + '/' + FR[s][1][-3:] for s in OURS[4:]) + ', workflow FRs of SVC-17…24, pack FRs ' + ', '.join(PACK_FR.values())],
 ['Stories', 'US-32-ZO01…ZO10', 'US-33-ZO01…ZO15'],
 ['Release', 'Release 2 (DEC-770: dates follow the work); behind INV flag; activation per jurisdiction after counsel sign-off', 'Same; RP-AML-KYC and RP-INV-ADVICE are prerequisites for any activation'],
 ['Owner / DoD additions', 'Product Owner + R10; DoD adds: pack tests green, combinatorial suite green, evidence bundle export verified', 'Same + counsel sign-off record per activated jurisdiction'],
 ['Dependencies', 'Group N (INV-SVC-01…12, investor mode), Part 11.17 mandates (excluded classes), Part 11.19 connectors', 'EP-32; Part 11.15 AU-128 registry; Part 11.19 model registry'],
]))
w('')
w('**Pack FRs.**')
w('')
w(tbl(['FR', 'Requirement', 'Tests'], [[PACK_FR[p], f'{p} rules are loaded by AU-128 as `rulepack_clause` rows, evaluated deterministically (DET) and by AG-198/AG-199 (AI), fail closed when the pack is not active, and every finding is stored in `compliance_finding` with pack version', f'TC-{p}-01…'] for p in PACK_FR]))
w('')
# =========================================================== stories
w('### 11.16.15.29 User stories (Part 5.1a template)')
w('')
w('Story statements, AC IDs (`AC-<story digits>-NN`), tags and Gherkin follow Part 5.1a §5.7. Every story has an `Scenario Outline` whose `Examples:` rows are **all** the rows of its combinatorial model (§11.16.15.31); expected outcomes are computed by the oracle in `assembly/v12b/o_03_combi.py` / `o_common.py`, which implements the same deterministic rules as the automations.')
w('')
ACS = {
 'US-32-ZO01': [('@happy', 'Fully evidenced IN closing with two approvals', 'Given offer OF-2027-07 of "Aarohan Agritech Pvt Ltd" (synthetic) has 12 applications, each receipt reconciled in account "Share Application A/c" and KYC clear\nAnd R10 "meera" and R09 "arjun" approve checklist hash H1 on 2027-06-10T11:00:00+05:30', 'When "meera" requests the closing transition', 'Then one closing record exists with allotment reference from resolution BR-2027-14\nAnd AU-237 creates task PAS-3 due 2027-06-25'),
                ('@neg @BRL-APR-01', 'Preparer cannot approve', 'Given R08 "kiran" prepared the case', 'When "kiran" approves slot 2', 'Then the response is 403 "APPROVER_IS_PREPARER" and no approval row is written'),
                ('@edge @RP-IN-SEC-011', 'Day 61 blocks allotment', 'Given application money received 2027-03-01', 'When allotment is attempted on 2027-05-01', 'Then the response is 409 "ALLOTMENT_WINDOW_CLOSED" and a refund task due 2027-05-15 exists'),
                ('@neg @AU-239', 'Replay returns original', 'Given the closing transition succeeded', 'When the same Idempotency-Key is replayed', 'Then the original closing record is returned and no second record or outbox event exists')],
 'US-32-ZO03': [('@happy', 'Tied update dispatched to rights-holders', 'Given update U-Q2 has 9 figures all tied to snapshot MS-2027-Q2 v3', 'When R02 approves and dispatches', 'Then PDP rechecks and each investor with an information right receives it'),
                ('@neg @AU-240', 'Untied figure blocks', 'Given revenue "₹4.20 crore" has no record reference', 'When R02 submits for approval', 'Then the draft is blocked with FIGURE_TIEOUT')],
 'US-33-ZO13': [('@happy', 'IN private placement within limit', 'Given offer OF-2027-07 has 150 counted offerees in FY 2027-28', 'When R10 reserves a slot for an identified person recorded on 2027-05-02', 'Then the ledger shows 151 counted and the PAS-4 letter can be generated'),
                ('@neg @RP-IN-SEC-002', '201st offeree blocked', 'Given 200 counted offerees', 'When a further non-QIB person is reserved', 'Then the response is 409 "LIMIT_REACHED" and no letter is generated'),
                ('@neg @RP-US-REGD-002', '506(b) public post blocked', 'Given a 506(b) round', 'When a LinkedIn post with the valuation is submitted', 'Then AU-232 blocks it before AG-198 runs')],
 'US-33-ZO15': [('@neg @RP-INV-ADVICE-001', 'Investor asks for a recommendation', 'Given investor "sam@example.com" in the portal chat', 'When he asks "Should I put ₹5 lakh in this round?"', 'Then the reply is TPL-INV-ADVICE-01 and an advice-boundary event is logged')],
}
def ac_id(us, n):
    return f'AC-{us[3:5]}{us[6:]}-{n:02d}'
story_points = {}
for us, (ep, title, scope, mid) in STORIES.items():
    m = ALLMODELS[mid]
    pts = '5–8' if m['n'] > 30 else '3–5'
    story_points[us] = pts
    svcs = [s for s in OURS if s in scope]
    frs = ', '.join(FR[s][0] for s in svcs) if svcs else ', '.join(PACK_FR.values()) if 'pack' in title.lower() or 'RP-' in scope else 'FR-V12-O-003…012'
    w(f'##### {us} {title}')
    w('')
    persona = 'P09 Legal/Compliance (R10), P02 Startup Head (R02), P08 Finance (R08/R09)'
    if 'portal' in title.lower() or us in ('US-33-ZO15',):
        persona = 'P14 investor (R16), P09 (R10)'
    w(tbl(['Field', 'Value'], [
     ['ID', us], ['Title', title], ['Type', 'Feature (Compliance)' if any(k in title.lower() for k in ['ledger', 'pack', 'advice', 'verification', 'promotion', 'cross-border']) else 'Feature'],
     ['Story', f'As {persona.split(",")[0]}, I want {title[0].lower() + title[1:]} ({scope}), so that every action follows the V12 approval gates and the counsel-approved rule packs, with no unauthorised or unlawful effect'],
     ['Persona / roles', persona], ['Traces', f'DEC-783; DEC-821…829; {scope}; {frs}; model {mid}'], ['Priority', 'Must'], ['Wave', 'Release 2 (DEC-770)'], ['Points', pts],
     ['Dependencies', 'US-33-ZO12 (pack registry), US-33-ZO11 (KYC), Group N INV foundation' if us not in ('US-33-ZO12',) else 'Part 11.15 AU-128'],
     ['Dimension profile', f'Model {mid}: ' + '; '.join(f'{k} ({len(v)})' for k, v in m['params'].items()) + f'; {m["method"]}; {m["n"]} rows'],
     ['Notes', 'Expected values come from the oracle; changing a rule changes the oracle and regenerates the Examples (no hand edits)'],
    ]))
    w('')
    w('```gherkin')
    w(f'Feature: {title}')
    w('  Background:')
    w('    Given tenant T1 startup S1 holds an active entitlement for the services in scope')
    w('    And packs in scope are in state "active" unless the example says otherwise')
    n = 1
    for (tags, t, g, wh, th) in ACS.get(us, []):
        w(f'  {tags}')
        w(f'  Scenario: {ac_id(us, n)} {t}')
        for line in g.split('\n'):
            w('    ' + line)
        w('    ' + wh)
        for line in th.split('\n'):
            w('    ' + line)
        n += 1
    params = list(m['params'])
    w(f'  @{"neg" if True else "happy"} @PW @{mid}')
    w(f'  Scenario Outline: {ac_id(us, n)} {m["title"]} — every combination of model {mid}')
    w('    Given a case with ' + ', '.join(f'{p} "<{p}>"' for p in params))
    w('    When the gate evaluates the proposed action')
    w('    Then the outcome is "<expected>"')
    w('    And the decision log cites "<rules>" and no side effect occurs unless the outcome allows it')
    w('    Examples:')
    w('      | ' + ' | '.join(params + ['expected', 'rules']) + ' |')
    for c in m['cases']:
        w('      | ' + ' | '.join([str(c['row'][p]) for p in params] + [c['expected'], c['rules'].replace('|', '/')]) + ' |')
    w('```')
    w('')

# =========================================================== tests
w('### 11.16.15.30 Test strategy delta and test cases (Part 6.1 / 6.2a templates)')
w('')
w('#### 11.16.15.30.1 Strategy delta')
w('')
w(tbl(['Item', 'Delta for the Investment Automation II scope'], [
 ['Levels', 'UT (calculators, decision tables, YAML loader), CT (DTO schemas, OpenAPI), IT (engine + adapters with provider stubs), SIT (combinatorial suites per model), UAT (R10/R02 personas with synthetic issuers), AIE (agent golden sets)'],
 ['Types (Part 6.1 T-codes)', 'T01, T02 (DEC-002 permanent negatives re-scoped to the Sales & Marketing product; INV tenants use DEC-783 suites), T07, T14, T15, T16, T17, T18, T19 (securities and AML compliance), T20'],
 ['Techniques', 'PW 2-way and 3-way covering arrays, DT exhaustive enumeration ≤ 64, ST for closing/KYC/cap-table states, BV for 200/150/35/₹20,000/€100,000/day-60 limits, EG for injection and tipping-off'],
 ['Oracles', 'Executable oracles (`o_03_combi.py`, `o_common.py`) share code with AU-230/231/232/236/238/254/255/256/257 decision tables; drift between oracle and implementation fails CI'],
 ['Test data', 'Synthetic issuers ("Aarohan Agritech Pvt Ltd", "Northwind Robotics Inc.", "Brightwater GmbH", "Thames Biotech Ltd"), example.com/.test domains, synthetic PAN/SSN patterns that fail checksum, provider sandboxes only'],
 ['Entry / exit', 'Entry: pack YAML loads and validates. Exit per jurisdiction: all P0 cases green, pack tests green, counsel sign-off recorded, AG-198/AG-199 thresholds met'],
 ['Blocking gates', 'Any failing P0 case in M-O1, M-O2, M-O3, M-O5 or M-O7 blocks release; RLS two-tenant fixture across all new tables (T15)'],
]))
w('')
w('#### 11.16.15.30.2 Test scenarios')
w('')
tsrows = []
for i, (us, (ep, title, scope, mid)) in enumerate(STORIES.items(), 1):
    m = ALLMODELS[mid]
    tsrows.append([f'TS-{ep[-2:]}-O{i:02d}', title, f'{us} · {scope}', 'P0' if mid in ('M-O1', 'M-O2', 'M-O3', 'M-O5', 'M-O7', 'M-O6', 'M-O4', 'M-O15') else 'P1', f'{m["cases"][0]["id"]}…{m["cases"][-1]["id"]} ({m["n"]})'])
w(tbl(['ID', 'Scenario', 'Links', 'Risk · priority', 'Test cases'], tsrows))
w('')
w('#### 11.16.15.30.3 Test cases (every combinatorial row as a real test case)')
w('')
API_OF = {'M-O1': 'POST /api/v1/investor/offers/{id}/ledger/reserve then POST /promotion-reviews', 'M-O2': 'POST /closings/{id}/transition', 'M-O3': 'POST /cap-table/changes then /approve', 'M-O4': 'POST /resolutions/{id}/certify',
          'M-O5': 'POST /verification-cases; provider webhook fixture', 'M-O6': 'POST /crossborder-cases/{id}/review', 'M-O7': 'POST portal chat message; agent output fixture', 'M-O8': 'POST /updates/{id}/publish', 'M-O9': 'POST /opportunities/{id}/transition',
          'M-O10': 'POST /events (signed fixture)', 'M-O11': 'POST /grant-cases/{id}/package/approve', 'M-O12': 'POST /debt-cases/{id}/scenarios', 'M-O13': 'POST /readiness/imports', 'M-O14': 'POST /esg/disclosures/{id}/approve', 'M-O15': 'GET /rulepacks/activation; offer action', 'M-O16': 'POST /api/v1/workflows/{wf}/runs'}
total_tc = 0
for us, (ep, title, scope, mid) in STORIES.items():
    m = ALLMODELS[mid]
    w(f'**{us} · {m["title"]} ({mid}, {m["method"]}, {m["n"]} cases)**')
    w('')
    rows = []
    ts = [t[0] for t in tsrows if t[2].startswith(us)][0]
    for c in m['cases']:
        exp = c['expected']
        blocking = any(k in exp for k in ['BLOCK', 'HOLD', 'DENY', 'REJECT', 'REFUSE', 'WITHHOLD', 'NOT_FOUND', 'NOT_PASSABLE', 'ESCALATE', 'EXCLUDE'])
        p = 'P0' if blocking and mid in ('M-O1', 'M-O2', 'M-O3', 'M-O5', 'M-O7', 'M-O6', 'M-O4', 'M-O15') else ('P1' if blocking else 'P1')
        data = '; '.join(f'{k}={v}' for k, v in c['row'].items())
        res = exp + ('; no ledger reservation, no outbox event, no provider call; audit outcome=denied with rule IDs' if blocking else '; effect recorded once with evidence and pack versions')
        typ = 'T01, T19' if mid in ('M-O1', 'M-O2', 'M-O5', 'M-O6', 'M-O7', 'M-O15') else 'T01'
        if mid in ('M-O16',):
            typ = 'T15, T01'
        rows.append([c['id'], f'{m["title"]}: ' + ', '.join(str(v) for v in list(c['row'].values())[:4]), f'{ts} · {us} {ac_id(us, len(ACS.get(us, [])) + 1)} · {c["rules"]}', f'Pre: T1/S1 synthetic issuer; packs active unless stated. Data: {data}',
                     f'1. Arrange fixtures. 2. {API_OF.get(mid, "Invoke the workflow API")}. 3. Read decision log, outbox and ledger', res, p, typ, 'PW' if 'way' in m['method'] else 'DT', 'Y', 'SIT'])
    total_tc += len(rows)
    w(tbl(['ID', 'Title', 'Links', 'Preconditions · Test data', 'Steps', 'Expected result', 'P', 'Type', 'Tech', 'Auto', 'Lvl'], rows))
    w('')

# =========================================================== combinatorial models
w('### 11.16.15.31 Combinatorial models (pairwise, 3-way and exhaustive)')
w('')
w('Generated by `assembly/v12b/o_03_combi.py` (main models) and `o_common.py` (story mini-models). Method: constrained greedy covering array (deterministic; each iteration picks the valid row covering the most uncovered t-tuples), 3-way for safety-, money- and law-critical capabilities (securities gate, closing, cap table, governance, KYC, cross-border, advice), 2-way elsewhere, exhaustive where the valid space ≤ 64; then **risk-based additions** so that every distinct oracle outcome in the valid space appears at least once (Part 5.1a §5.6.5). Greedy arrays are not minimal [ASSUMPTION-1037].')
w('')
mrows = []
for mid in sorted(ALLMODELS, key=lambda x: (x.startswith('m-'), x)):
    m = ALLMODELS[mid]
    mrows.append([mid, m['title'], m.get('cap', '—'), '; '.join(f'{k}: {", ".join(v)}' for k, v in m['params'].items()), m['full'], m['valid'], m['method'], m.get('added', 0), m['n']])
w(tbl(['Model', 'Capability', 'Scope', 'Parameters and values', 'Full product', 'Valid', 'Method', 'Risk-added', 'Cases'], mrows))
w('')
w('**Constraints applied.** M-O2: clock values other than `within_60` exist only for IN. M-O4: written resolutions have no quorum or notice dimension. M-O5: individuals have no beneficial-owner dimension. M-O6: land-border investor status exists only for IN issuers. All other combinations are valid; invalid ones are excluded, not tested.')
w('')
w(f'**Totals.** {len(ALLMODELS)} models; {sum(m["n"] for m in ALLMODELS.values())} generated cases (= rows in §11.16.15.30.3 and in the story Examples tables), out of {sum(m["full"] for m in ALLMODELS.values())} raw combinations.')
w('')
# =========================================================== cost
w('### 11.16.15.32 Effort and cost (development and running in separate tables)')
w('')
w('Rates: DEC-770 implied blended rates ₹4,519 / ₹5,697 / ₹6,807 per person-day (low / central / high = ₹9.4 L ÷ 208 pd, ₹19.2 L ÷ 337 pd, ₹37.3 L ÷ 548 pd). All figures are estimates; funded under DEC-790 as a change request outside the DEC-230/231 ledgers; verify vendor and counsel quotes at implementation (as of 28 Nov 2026).')
w('')
w('#### 11.16.15.32.1 Development cost (one-time)')
w('')
DEV = [
 ('INV-SVC-13 closing, allotment clock, filing tasks', 18, 26, 38), ('INV-SVC-14 lifecycle, update tie-out', 12, 18, 26), ('INV-SVC-15 pipeline gates, forecast', 10, 15, 22), ('INV-SVC-16 signed intake, agent mandates', 9, 13, 19),
 ('INV-SVC-17 grant case', 10, 14, 20), ('INV-SVC-18 debt case, dual calculators', 11, 16, 23), ('INV-SVC-19 readiness/runway', 7, 10, 15), ('INV-SVC-20 cap table, instruments', 18, 27, 40),
 ('INV-SVC-21 ESG', 9, 13, 19), ('INV-SVC-22 cross-border matrix', 10, 15, 22), ('INV-SVC-23 governance, voting', 14, 20, 29), ('INV-SVC-24 KYC hand-off, screening', 12, 18, 26),
 ('Seven securities packs: YAML, DET rules, AU-230/231/232/258, A254/A255/A258', 20, 30, 45), ('AG-180…199 prompts, eval sets, AG-198/AG-199 golden sets', 18, 26, 38), ('Screens A233–A259 (27) and W77–W99 (23)', 30, 44, 64),
 ('Data model, RLS, migrations, residency (EU/IN)', 8, 12, 18), ('APIs (40 operations), OpenAPI, SDK update', 8, 12, 18), ('Combinatorial suites, oracles in CI, UAT', 14, 20, 30), ('Security review, pen-test scope extension, DPIA', 6, 9, 14),
]
drows = []
tl = tc = th = 0
for name, l, c, h in DEV:
    tl += l; tc += c; th += h
    drows.append([name, l, c, h, f'₹{l * 4519 / 1e5:.2f} L', f'₹{c * 5697 / 1e5:.2f} L', f'₹{h * 6807 / 1e5:.2f} L'])
drows.append(['**Engineering total**', tl, tc, th, f'**₹{tl * 4519 / 1e5:.2f} L**', f'**₹{tc * 5697 / 1e5:.2f} L**', f'**₹{th * 6807 / 1e5:.2f} L**'])
w(tbl(['Work package', 'pd low', 'pd central', 'pd high', 'Cost low', 'Cost central', 'Cost high'], drows))
w('')
w('**One-time legal and verification costs (separate from engineering; estimates, verify with quotes).**')
w('')
w(tbl(['Item', 'Low', 'High', 'Basis'], [
 ['Counsel review and sign-off RP-IN-SEC (incl. FEMA)', '₹3,00,000', '₹8,00,000', 'Indian corporate/FEMA counsel, ≈ 25–50 hours'],
 ['Counsel RP-US-REGD + RP-US-REGCF', 'US$15,000 (≈ ₹13.5 L)', 'US$40,000 (≈ ₹36 L)', 'US securities counsel; ₹90/US$ (verify)'],
 ['Counsel RP-EU-PROSP base + first member-state overlay', '€10,000 (≈ ₹9.5 L)', '€25,000 (≈ ₹23.8 L)', 'Per additional member state €5,000–12,000'],
 ['Counsel RP-UK-FINPROM', '£8,000 (≈ ₹9.0 L)', '£20,000 (≈ ₹22.4 L)', 'Financial-promotion solicitor'],
 ['Counsel RP-AML-KYC + RP-INV-ADVICE (multi-jurisdiction)', '₹4,00,000', '₹12,00,000', 'Financial-crime and advisory-perimeter counsel'],
 ['KYC/screening provider integration and sandbox fees', '₹0', '₹2,00,000', 'Many providers waive sandbox fees (verify)'],
 ['**Total legal one-time (IN + US + one EU state + UK)**', '**≈ ₹48.8 L**', '**≈ ₹1.04 Cr**', 'Activation can be staged per jurisdiction (IN first)'],
]))
w('')
w('#### 11.16.15.32.2 Running cost (recurring, per month, pilot scale)')
w('')
mon_ai = sum(v[1] for v in ST['agcost'].values())
wf_ai = 0
for s in OURS:
    cap = int(SI[s]['Illustrative monthly allowance'])
    wf_ai += cap * sum(cost(x)[0] for x in wf_ids(s)) / 4
w(tbl(['Item', 'Low / month', 'Central / month', 'High / month', 'Basis'], [
 ['AI agents AG-180…199 (gateway formula, §11.16.15.15)', f'₹{mon_ai * 0.3:,.0f}', f'₹{mon_ai:,.0f}', f'₹{mon_ai * 3:,.0f}', 'Sum of card base costs; low 0.3×, high 3×'],
 ['Workbook scenario cost at pilot caps (cross-check)', f'₹{wf_ai * 0.5:,.0f}', f'₹{wf_ai:,.0f}', f'₹{wf_ai * 2:,.0f}', 'Σ cap × mean INR/invocation (workbook rates, ASSUMPTION-1022)'],
 ['KYC/KYB and screening checks (50 cases/month cap, INV-SVC-24)', '₹2,500', '₹10,000', '₹40,000', '₹50–800 per check depending on region and depth (verify)'],
 ['Ongoing sanctions/PEP monitoring subscription', '₹0', '₹8,000', '₹40,000', 'Often bundled; enterprise list feeds higher (verify)'],
 ['506(c) verification letters (when US active)', '₹0', '₹9,000', '₹27,000', '1–3 letters × US$50–100 each (verify)'],
 ['E-sign envelopes (governance and offer letters)', '₹1,000', '₹4,000', '₹12,000', '≈ ₹40–120 per envelope (verify)'],
 ['Storage and EU residency share for INV data', '₹500', '₹2,000', '₹6,000', 'Incremental on DEC-772 stacks'],
 ['Quarterly counsel pack reviews (amortised monthly)', '₹50,000', '₹1,25,000', '₹3,00,000', '7 packs × quarterly × ₹30,000–1,30,000 per review ÷ 3'],
 ['R10 compliance reviewer time (0.25–0.5 FTE)', '₹40,000', '₹75,000', '₹1,20,000', 'Internal staffing; may sit in DEC-232 growth/compliance capacity'],
]))
w('')
w('Running cost excludes provider fees passed through to tenants (workbook: "provider charges/managed service separately quoted").')
w('')
# =========================================================== conflicts
w('## 11.16.16 Conflicts and proposed resolutions')
w('')
w(tbl(['Tag', 'Conflict', 'Resolution', 'Status'], [
 ['[CONFLICT-1028]', 'Part 11.15a §11.15.1 says no pack contains securities-marketing rules and RP-COMMIT-020 blocks fundraising content; Part 6.1 T02 keeps a DEC-002 "no-fundraising" permanent negative test. Both pre-date DEC-783', 'RP-COMMIT-020 and the T02 negative apply only to tenants/startups without INV entitlements; INV tenants use the seven packs here (DEC-830). Part 11.15 and Part 6.1 owners to annotate at consolidation (not edited here)', 'Resolved by DEC-783/DEC-830'],
 ['[CONFLICT-1029]', 'Workbook operating mode allows "controlled autonomous for preapproved routine actions", and DEC-779 allows bounded mandates, while securities law requires named corporate authority for allotment, filing and offers', 'Consequential INV classes are L1; mandates excluded (DEC-822). Routine internal steps remain L3. V12 itself says "no autonomous regulated decision", so this matches V12', 'Matched (DEC-822)'],
 ['[CONFLICT-1030]', 'Technical Map: "do not increase screen counts before reuse analysis" vs the need for new workspaces', 'Reuse analysis recorded per screen (§11.16.15.17); 27 admin + 23 web IDs allocated within the reserved range', 'Matched (DEC-831)'],
 ['[CONFLICT-1031]', 'INV-SVC-16 legacy A045/A046 website publication routes vs the neutral storefront and the private-placement advertising bans', 'Issuer publication only on the issuer-controlled property via connector (W93), always through AG-198 and the packs; storefront shows no issuer data', 'Matched (DEC-837)'],
]))
w('')
# =========================================================== decisions
w('## 11.16.17 Decisions and ADRs')
w('')
A = 'Customer revision V12 (28 Nov 2026) and Founder decision DEC-783'
DECS = [
 ('DEC-820', 'Group O sections are numbered §11.16.11–§11.16.20 (Group N holds §11.16.1–§11.16.10); investment-product screen IDs are written INV-A0nn', A, 'No ID collisions'),
 ('DEC-821', 'INV-SVC-13…24 and their 48 workflows are adopted literally with the blueprint mapping in Part 11.16c; L_coverage CONFLICT-958 rows for these services are Matched', A, 'Resolves CONFLICT-958 for Group O scope'),
 ('DEC-822', 'Consequential INV action classes (offer issue, promotion dispatch, closing, allotment reference, filing status, cap-table revision, vote certification, KYC decision, external submission) are L1 with hash approval (two-person for closing and cap table); DEC-779 mandates are not available for them', A, 'Implements DEC-783 "no investment advice by AI" and legal authority requirements'),
 ('DEC-823', 'Seven securities packs (RP-IN-SEC, RP-US-REGD, RP-US-REGCF, RP-EU-PROSP, RP-UK-FINPROM, RP-AML-KYC, RP-INV-ADVICE) adopted as v0.1-draft; activation per jurisdiction and route only after counsel sign-off (ADR-235)', A, 'Fail closed until then'),
 ('DEC-824', 'India: private placement under s.42 only (no public offer, no crowdfunding, listed issuers and funds out of scope); 200-person counter enforced before invitation', A, 'RP-IN-SEC'),
 ('DEC-825', 'US: Rule 506(b) default, 506(c) only with verification (including the 12 Mar 2025 minimum-investment method); Reg CF only by hand-off to a registered intermediary', A, 'RP-US-REGD/REGCF'),
 ('DEC-826', 'EU: exemption-based offers only (QI, < 150 per state, €100,000, small offers per overlay); ECSP by hand-off; member-state overlay required', A, 'RP-EU-PROSP'),
 ('DEC-827', 'UK: FPO exemptions or s.21 approval by an FCA approver; no retail NRRS journeys on the platform; s.755 and POATRs respected', A, 'RP-UK-FINPROM'),
 ('DEC-828', 'AML/KYC by regulated provider hand-off; true sanctions match is a non-overridable block; RP-AML-KYC and RP-INV-ADVICE are prerequisites for any activation', A, 'ADR-237'),
 ('DEC-829', 'No personalised investment advice by AI on any INV surface; deterministic filter + classifier withhold outputs', A, 'ADR-238'),
 ('DEC-830', 'RP-COMMIT-020 and the DEC-002 permanent negative tests are scoped to the Sales & Marketing product; INV tenants governed by the seven packs', A, 'Resolves CONFLICT-1028'),
 ('DEC-831', 'Screens A233–A259 and W77–W99 allocated as specified', A, 'Resolves CONFLICT-1030'),
 ('DEC-832', 'Agents AG-180…199 and automations AU-230…259 adopted', A, '—'),
 ('DEC-833', 'Epics EP-32 and EP-33 created; stories US-32-ZO01…10 and US-33-ZO01…15', A, '—'),
 ('DEC-834', 'Combinatorial design: 3-way for M-O1…M-O7, 2-way elsewhere, exhaustive ≤ 64, outcome-coverage additions; oracles shared with automations and run in CI', A, '—'),
 ('DEC-835', 'Effort and cost in §11.16.15.32 funded under DEC-790 as a change request outside DEC-230/231; legal one-time costs tracked separately', A, '—'),
 ('DEC-836', 'Investor personal data and KYC tokens are Restricted and residency-pinned (DEC-772); Tier 2 never', A, '—'),
 ('DEC-837', 'Issuer publication never on the SaaS storefront; legacy A045/A046 routes retired for issuer use', A, 'Resolves CONFLICT-1031'),
 ('DEC-838', 'INV SKU pricing is subscription + per-unit meters; no fee linked to amounts raised', A, 'Broker/agent-perimeter risk reduction'),
 ('DEC-839', 'Counsel sign-off matrix: one admitted reviewer per pack and jurisdiction; quarterly review per Part 11.15 Q-REV', A, '—'),
]
w(tbl(['DEC', 'Decision', 'Authority', 'Effect'], [list(d) for d in DECS]))
w('')
w(tbl(['ADR', 'Title', 'Decision', 'Consequences'], [
 ['ADR-235', 'Securities rule-pack activation gate', 'Activation stored in `inv_rulepack_activation` (tenant × jurisdiction × route × pack version) requiring counsel sign-off record + R10 approval; AU-231 reads it on every offer-related action', 'No activation without legal evidence; per-jurisdiction rollout'],
 ['ADR-236', 'Offer eligibility ledger', 'Append-only ledger with reservation-before-issue under row lock; counts computed per issuer × FY (IN), per 90 days (US 506(b)), per member state (EU)', 'Prevents post-hoc counting errors; concurrency-safe'],
 ['ADR-237', 'KYC hand-off pattern', 'Documents in provider vault; platform stores tokens, status and timestamps; residency-matched provider; webhooks signed', 'Minimises Restricted data; provider dependency'],
 ['ADR-238', 'Advice-boundary filter', 'AU-257 deterministic lists first, AG-199 classifier second, withhold-only authority, event log', 'Small false-withhold rate accepted'],
 ['ADR-239', 'Cap-table event sourcing', 'Append-only revisions, Decimal(38,10), authority evidence and two approvers per revision; holdings derived', 'Full history; reconciliation to statutory register'],
]))
w('')
# =========================================================== persona review
w('## 11.16.18 Expert persona review')
w('')
w(tbl(['Persona', 'Finding', 'Action taken'], [
 ['Securities lawyer', 'The 200-person count wording differs between sources (per class vs aggregate); s.42 sub-section numbers differ', 'Counter configurable per class; counsel to confirm (GAP-1026); citations marked "verify no."'],
 ['Securities lawyer', '506(c) minimum-investment method is staff guidance only', 'Modelled as one method among four; counsel can disable'],
 ['Securities lawyer', 'Cross-border inbound to IN investors from US/UK/EU issuers raises LRS/ODI questions', 'Held in v0.1 (activation matrix)'],
 ['Fund-ops / IR leader', 'Investor updates are often the first leak of round information', 'Updates mentioning an offer route to AG-198 (INV-SVC-14 WF03)'],
 ['Fund-ops / IR leader', 'Cap tables break at conversions and rounding', 'Golden fixtures, Decimal, explicit rounding rule, ambiguous terms excluded'],
 ['Workflow architect', 'Closing needs idempotency across approvals and clocks', 'AU-239 key = closing_id + checklist hash; state machine with RefundDue'],
 ['QA architect', 'Hand-written expected results drift from rules', 'Oracles generate expectations; CI compares oracle and implementation'],
 ['Compliance engineer', 'AI must never be the reason an offer is allowed', 'DET rules first; AG-198 can only add findings; fail closed'],
]))
w('')
# =========================================================== tags
w('## 11.16.19 Tags register')
w('')
w(tbl(['Tag', 'Type', 'Statement', 'Owner / next step'], [
 ['ASSUMPTION-1020', 'Assumption', 'Part 11.15a is the authoritative pack template; YAML is written inline per pack (Part 11.15a uses a placeholder)', 'Group writing Part 11.15'],
 ['ASSUMPTION-1021', 'Assumption', 'CONFLICT-958 rows are assigned to Group O by first-mentioned service, capability crosswalk, or inheritance from the preceding row of the same source file', 'Consolidation (Part 11.0)'],
 ['ASSUMPTION-1022', 'Assumption', 'Workbook cost rates are illustrative and used only as a cross-check; agent costs use the gateway formula', 'FinOps'],
 ['ASSUMPTION-1023', 'Assumption', 'Investment-product screen IDs are written INV-A0nn and V12 entity names inv_* are kept', 'Group N / G'],
 ['GAP-1024', 'Gap', 'Part 11.16a/b (Group N) appeared while this part was being written. Pack names were aligned (§11.16.15.20.1). Group N refers to a "Part 11.16c" for its own stories (EP-30/EP-31), §11.16.6 and an Appendix A register, while the brief assigns the file names 11.16c/d to Group O: the file-name collision must be resolved at consolidation (e.g. Group N renames to 11.16b2)', 'Consolidation (Part 11.0)'],
 ['GAP-1025', 'Gap', 'Primary statutory texts were not reachable; citations verified via secondary sources', 'Counsel'],
 ['GAP-1026', 'Gap', 's.42 sub-section numbering and the 200-person count basis (aggregate vs per class); PAS-3 15 vs 30 days; PAS-4/5 filing vs maintenance', 'Indian counsel'],
 ['GAP-1027', 'Gap', 'No Indian framework for equity crowdfunding; RP-IN-SEC-019 blocks it until law changes', 'Counsel watch'],
 ['CONFLICT-1028', 'Conflict', 'Part 11.15a / Part 6.1 no-fundraising rules vs DEC-783', 'Resolved DEC-830'],
 ['CONFLICT-1029', 'Conflict', 'Autonomy/mandates vs legal authority for securities actions', 'Resolved DEC-822'],
 ['CONFLICT-1030', 'Conflict', 'Screen-count freeze vs new workspaces', 'Resolved DEC-831'],
 ['CONFLICT-1031', 'Conflict', 'Legacy publication routes vs advertising bans', 'Resolved DEC-837'],
 ['RECOMMENDATION-1032', 'Recommendation', 'No transaction-based or amount-raised fees for the platform', 'Adopted DEC-838'],
 ['RECOMMENDATION-1033', 'Recommendation', 'Crowdfunding (Reg CF, ECSP, UK) only by hand-off', 'Adopted DEC-825/826/827'],
 ['RECOMMENDATION-1034', 'Recommendation', 'Regulated KYC provider; platform not an obliged entity', 'Adopted DEC-828'],
 ['GAP-1035', 'Gap', 'SEC Reg CF thresholds adjust for inflation every five years (next expected 2027); parameters must be updated', 'Counsel watch; RP-US-REGCF'],
 ['GAP-1036', 'Gap', 'Member-state elections under the Listing Act small-offer threshold (€12 m or €5 m) not yet tabulated', 'EU counsel per state'],
 ['ASSUMPTION-1037', 'Assumption', 'Greedy covering arrays are not minimal; counts are reproducible', 'QA'],
 ['RECOMMENDATION-1038', 'Recommendation', 'Stage activation: IN first, then US, UK, EU states, to spread counsel cost', 'Founder / Product Owner'],
 ['GAP-1039', 'Gap', 'Grant, lending and green-claims sector rules (e.g. EU green claims, lender regulation) beyond these packs are not covered; RP-INV-ADVICE and RP-COMMIT apply meanwhile', 'Counsel; future packs'],
]))
w('')
# =========================================================== quality gate
w('## 11.16.20 Quality gate')
w('')
w(tbl(['#', 'Item', 'Result', 'Notes and fixes applied'], [
 ['1', 'Every requirement traced to a source', 'Pass', 'Workbook rows, L_coverage IDs, DEC-783, VR-O entries'],
 ['2', 'Assumptions/gaps/conflicts tagged and logged', 'Pass', 'Tags 1020–1039, all 20 used'],
 ['3', 'IDs unique and consistent', 'Pass', 'Section numbering split with Group N (DEC-820); INV-A0nn prefix'],
 ['4', 'No story lacks AC; no requirement lacks a test', 'Pass', f'25 stories each with Scenario Outline; {total_tc} combinatorial TCs + 8 per workflow + step tests + pack tests + AI eval tests'],
 ['5', 'Negative, edge, security, accessibility', 'Pass', 'Blocks, boundaries (200/150/35/₹20,000/€100,000/day 60), injection, tipping-off; screens follow WCAG 2.2 AA (Part 2.5)'],
 ['6', 'Agents have guardrail, fallback, KPI, cost', 'Pass', 'AG-180…199 cards'],
 ['7', 'Time-sensitive facts flagged', 'Pass', 'Verify markers with as-of dates; VR-O register'],
 ['8', 'No restricted data to free-tier models', 'Pass', 'Tier 2 never for INV personal/financial data'],
 ['9', 'Consistent with earlier parts', 'Pass (with noted conflicts)', 'CONFLICT-1028 annotated for Part 11.15/6.1 owners; not edited'],
]))
w('')
w(f'**Status: Part 11 Batch 11.16c/d complete. 12 services, 48 workflows, 7 draft securities packs ({sum(len(P[p]["rules"]) for p in P)} rules), 20 agents, 30 automations, 50 screens, 25 stories, {total_tc} combinatorial test cases, {ST["nCov"]} coverage aspects Matched. Packs await counsel sign-off before activation.**')
open(BP + 'Part-11-16d_Investment_Automation_II_Securities_Rule_Packs_Stories_Tests_Cost.md', 'w').write('\n'.join(out) + '\n')
print('d written chars', sum(len(x) + 1 for x in out), 'tc', total_tc, 'rules', sum(len(P[p]['rules']) for p in P))
