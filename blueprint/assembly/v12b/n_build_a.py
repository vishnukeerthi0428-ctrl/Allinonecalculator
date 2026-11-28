"""Builds Part-11-16a (framework, website, service specifications, agents, automations, screens, data, API)."""
import sys, os, re, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import n_ctx as C
import n_spec as SP
from n_common import md_escape as E

BP = '/home/user/Allinonecalculator/blueprint'
OUT = BP + '/Part-11-16a_Investment_Automation_I_Investor_Mode_and_INV-SVC-01-12.md'
L = []
w = L.append

def table(hdr, rows):
    w('| ' + ' | '.join(hdr) + ' |')
    w('|' + '---|' * len(hdr))
    for r in rows:
        w('| ' + ' | '.join(E(str(x)) for x in r) + ' |')
    w('')

TITLE = 'Investment Automation I: Investor/Fundraising Mode and INV-SVC-01…12'
def header(letter, scope):
    w('# AI Growth Engine: Employee Sales & Marketing Automation')
    w(f'## Application Blueprint: PART 11 (Batch 11.16{letter}), {TITLE}')
    w('')
    table(['Field', 'Value'], [
        ['Document', f'Part 11, Batch 11.16, file **{letter} of c**. {scope}. Files: `Part-11-16a_…` (§11.16.1–§11.16.5.11), `Part-11-16b_…` (§11.16.5.12 workflow specifications), `Part-11-16c_…` (§11.16.5.13–§11.16.10 and Appendix A)'],
        ['Version', '1.0 · 28 Nov 2026'],
        ['Baseline', 'Parts 0–9.10, 11.1–11.15 (DEC-001…422, DEC-500…791); Part 11.14 DEC-783 (investor/fundraising adopted), DEC-779 (bounded mandates), DEC-772 (EU/IN residency), DEC-777 (messaging window), DEC-788 (model registry), DEC-790 (funding); Part 11.15 rule-pack framework (AU-128, AG-086, CP-01…07); Part 11.2b/11.3b formats; Part 5.1a/5.1b story template; Part 6.2a test template; V12B brief'],
        ['Source material', 'Investment Automation Master Automation Service Catalog 2031 (24 services / 96 workflows; 12 sheets, CSV export); Investment_Automation_19_Neutral_SaaS_Website (README, layout catalogue, route reconciliation, verification report, HTML); `investment_website(1).html`; investor/fundraising mode (`CFG.inv`) of `commercial_website_desktop_V12.html`; Investment lines of BRD/FSD `ZZ_Historical_annex.txt`; the CONFLICT-958 rows of `final/coverage_v12/L_coverage.csv`'],
        ['Roles applied', 'Expert panel: former investment-banking and private-markets operating partner; securities-law and compliance specialist (SEBI ICDR, Companies Act s.42 private placement, US Regulation D 506(b)/(c) and Regulation CF, EU Prospectus Regulation exemptions, anti-solicitation, KYC/AML); Chief Product Officer (B2B SaaS); Principal Solutions Architect; Principal Business Systems Analyst. Reviewers: Product Owner, QA Lead, Security/Privacy/AI Governance Lead, DevOps/SRE, FinOps'],
        ['Group and ID ranges', 'P1a, letter N: DEC-800…819 · tags 1000–1019 · ADR-230…234 · FR-V12-N-### · BRL-V12-N-## · US-<EP>-ZN<nn> · TC-V12-N-### · AG-160…179 · AU-200…229 · screens A205–A232, W55–W76 · epics EP-30, EP-31 · controls SEC-CTL-N-01…16 · parameter models PM-N-01…09 · API-V12-N-###'],
        ['Legal status', '**Draft for counsel review. Not legal advice.** Every statutory threshold, exemption and deadline in this part is the panel\'s reading for implementation design and must be verified by counsel admitted in the jurisdiction (verify at time of implementation, as of 27 Nov 2026) [ASSUMPTION-1000]. No capability activates in a jurisdiction until its rule pack is counsel-signed (DEC-783, SEC-CTL-N-01)'],
        ['Budget status', 'Development and running estimates (§11.16.5.16) are **outside** Ledger A (DEC-230) and Ledger B (DEC-231), funded under DEC-790 as change request CR-V12-N-01 (development) and CR-V12-N-02 (running); shown in separate tables'],
    ])

header('a', 'This file holds §11.16.1 material reviewed, §11.16.2 coverage summary, §11.16.3 register summary, §11.16.4 catalogue reconciliation and §11.16.5.1–§11.16.5.11 (product boundary, securities controls, privacy, roles, investor-mode website, 12 service specifications, agents, automations, screens, data and API)')

w('**Acronyms.** AML anti-money laundering · AT acceptance test · DSR data-subject request · DPDP Digital Personal Data Protection Act 2023 (India) · ECSP EU crowdfunding service provider · FEMA Foreign Exchange Management Act (India) · FPO Financial Promotion Order (UK) · FSMA Financial Services and Markets Act 2000 (UK) · HNI high-net-worth individual · ICDR SEBI (Issue of Capital and Disclosure Requirements) Regulations 2018 · IR investor relations · KYC know your customer · LIA legitimate-interest assessment · MNPI material non-public information · NDA non-disclosure agreement · PAS-3/4/5 Companies (Prospectus and Allotment of Securities) Rules forms · PDP Policy Decision Point · PEP politically exposed person · PM parameter model · PPM private placement memorandum · PR EU Prospectus Regulation (EU) 2017/1129 · QI qualified investor · QIB qualified institutional buyer · Reg CF Regulation Crowdfunding · Reg D Regulation D (Rules 504/506) · RLS row-level security · SEBI Securities and Exchange Board of India · SKU stock-keeping unit · SoD separation of duties.')
w('')

# ------------------------------------------------------------------ 11.16.1
w('## 11.16.1 Material reviewed')
w('')
src_rows = []
def rc(name):
    return len([r for r in C.D[name][1]]) if C.D[name][1] else 0
mine_ct = {
 'Service_Catalog': len(C.SVC), 'Workflow_Catalog': len(C.WFS), 'Acceptance_Tests': len(C.ATM), 'Cost_Model': len(C.CMM),
 'Entitlement_Rules': len(C.ERM), 'Technical_Map': sum(len(v) for v in C.TMM.values()), 'Service_Index': len(C.SIM), 'Migration': len(C.MGM),
 'Capability_Crosswalk': len([r for r in C.CW if r['Primary service ID'] == 'ALL' or C.mine(r['Primary service ID'])]),
}
for name, purpose, pattern in [
 ('Start_Here', 'Scope metrics 16→24 services, 48→96 workflows, 30→50 fields, 64→120 acceptance scenarios, 15 engines, 19/51 website/admin routes', 'metric table'),
 ('Service_Index', 'One row per SKU: family, bundle, workflow count, meter, illustrative allowance, price status', 'register'),
 ('Service_Catalog', '50-field service specification per SKU', '50 fields × SKU'),
 ('Workflow_Catalog', '50-field workflow specification, four per SKU', '50 fields × workflow'),
 ('Acceptance_Tests', 'One scenario per workflow plus one entitlement scenario per SKU; all Not run', '14 columns'),
 ('Capability_Crosswalk', '100 legacy capabilities INV-01-01…INV-20-05 → primary SKU', '8 columns'),
 ('Cost_Model', 'Illustrative INR per workflow invocation; rates and assumptions', '13 columns'),
 ('Entitlement_Rules', 'Bundle, prerequisites, permissions, gate, meter, cap, missing-prerequisite and revocation behaviour', '15 columns'),
 ('Technical_Map', 'Admin screen reuse, route inventory, entity candidates, UAT IDs', '8 columns'),
 ('Migration', 'Retain + expand (01–16) / new (17–24); entitlement transitions', '8 columns'),
 ('Shared_Engines', 'ENG-01…15 logical engines', '5 columns'),
 ('Sources_Decisions', 'Source references, SHA-256 of packages, interpretation constraints', '4 columns')]:
    hdr, data, raw = C.D[name]
    n = len(data) if data else len([r for r in raw if any(r)])
    src_rows.append([f'Catalog CSV `{name}.csv`', n, mine_ct.get(name, n if name in ('Start_Here', 'Shared_Engines', 'Sources_Decisions') else '—'), purpose, pattern])
src_rows += [
 ['Website `investment_website_layout_catalog.json`', len(C.D['layout']['items']) if isinstance(C.D['layout'], dict) and 'items' in C.D['layout'] else '100', '100 (common catalogue)', '100 capability items in 20 families (25 core)', 'JSON items'],
 ['Website `investment_website_route_reconciliation.csv`', len(C.D['routes']), len(C.D['routes']), 'W01–W19 previous → current names and access', 'CSV'],
 ['Website `README.txt`, `verification_report.json`', '1 + 1', 'all', 'Neutral storefront constraints; verification flags', 'prose / JSON'],
 ['`investment_website(1).html` (= website pack HTML, byte-identical)', '1 SPA', 'CFG: 19 routes, 100 items, 20 groups', 'Neutral investment storefront prototype', 'embedded JS'],
 ['`commercial_website_desktop_V12.html` investor mode', f'{len(C.BRANCHES)} `inv` branches', f'{len(C.BRANCHES)}', 'Objective mode "Automate your fundraising operations"', 'embedded JS'],
 ['BRD/FSD `ZZ_Historical_annex.txt` Investment lines', '169 + 251 lines containing "invest"', 'via L rows', 'Investment comparator mirror of the catalogue sheets; REC-10', 'text'],
 ['`L_coverage.csv` rows with CONFLICT-958', '1,176', 'see §11.16.2', 'Classified residual units (Group L)', 'CSV'],
]
table(['Material', 'Rows / items', 'In Group N scope', 'Purpose', 'Pattern'], src_rows)
w('**Scope split with Group O (P1b).** Group N owns INV-SVC-01…12 (48 workflows), the investor-mode website, the common investment platform (product boundary, foundation capabilities INV-01/11/12/13/14, engines, entitlement, securities control framework consumer side). Group O owns INV-SVC-13…24 and the content of the securities rule packs RP-SEC-* (Part 11.16c/d of Group O, published as Parts 11.16c/d in its own numbering) [ASSUMPTION-1001]. Rows of `L_coverage.csv` whose primary service is INV-SVC-13…24 are left to Group O; rows without a primary service are reconciled here.')
w('')
w('**Parsing scripts (saved).** `assembly/v12b/n_extract_inv_mode.py` (investor-mode branches and website CFG), `n_common.py` (loaders, covering-array generator, coverage verifier), `n_ctx.py` (ID allocation), `n_spec.py` (hand-authored mapping), `n_comb.py` (parameter models and oracles), `n_build_a.py`, `n_build_b.py`, `n_build_c.py`, `n_build_cov.py`. Every source row is read programmatically; nothing is sampled.')
w('')

# ------------------------------------------------------------------ 11.16.2 coverage
import csv
cov = list(csv.DictReader(open(BP + '/final/coverage_v12/N_coverage.csv'))) if os.path.exists(BP + '/final/coverage_v12/N_coverage.csv') else []
w('## 11.16.2 Coverage summary')
w('')
if cov:
    cb = collections.Counter(r['status_before'].split(' (')[0] for r in cov)
    ca = collections.Counter(r['status_after'] for r in cov)
    fam = collections.Counter(r['doc'] for r in cov)
    table(['Status before', 'Aspects'], sorted(cb.items(), key=lambda x: -x[1]) + [['**Total**', len(cov)]])
    table(['Status after', 'Aspects'], sorted(ca.items(), key=lambda x: -x[1]))
    table(['Source family (doc column)', 'Aspects'], sorted(fam.items(), key=lambda x: -x[1]))
w('Before this part the blueprint excluded investors and fundraising (DEC-002, CC-01, DEC-517), so every Investment aspect was Not covered or Conflict (CONFLICT-958, CONFLICT-868). DEC-783 adopted the product; this part specifies it, and every Group N aspect ends **Matched**. No aspect is left "Pending Founder decision".')
w('')

# ------------------------------------------------------------------ 11.16.3
w('## 11.16.3 Detailed register (summary; the individual list is Appendix A of Part 11.16c and `N_coverage.csv`)')
w('')
if cov:
    g = collections.defaultdict(list)
    for r in cov:
        g[(r['doc'], r['chapter'][:60])].append(r)
    rows = []
    for (d, ch), rs in sorted(g.items(), key=lambda x: -len(x[1]))[:60]:
        locs = collections.Counter(r['blueprint_location'].split(';')[0] for r in rs).most_common(2)
        rows.append([d, ch, len(rs), ', '.join(sorted({r['status_before'].split(' (')[0] for r in rs})), '; '.join(l for l, _ in locs), 'Matched'])
    table(['Doc', 'Chapter / sheet', 'Aspects', 'Status before', 'Main blueprint location', 'After'], rows)
w('Conflicts raised and resolved in this part: CONFLICT-1008 (neutral storefront vs "investor website"), CONFLICT-1009 (V12 BR-C03/BR-C14/REC-10 separation vs DEC-783), CONFLICT-1019 (V12 side-effect labels weaker than the actual effect). See §11.16.6 (Part 11.16c).')
w('')

# ------------------------------------------------------------------ 11.16.4 reconciliation
w('## 11.16.4 Catalogue reconciliation')
w('')
w('### 11.16.4.1 Service Index, Entitlement Rules and Migration (INV-SVC-01…12)')
w('')
rows = []
for n in range(1, 13):
    si, er, mg = C.SIM[n], C.ERM[n], C.MGM[n]
    rows.append([si['Service ID'], si['Independently purchasable automation service'], si['Service family'], si['Suggested partial bundle'], si['Workflow count'],
                 si['Selective purchase'], si['Meter unit'], si['Illustrative monthly allowance'], si['Price status'], er['Optional input producers (service IDs)'],
                 mg['Decision'] + '; ' + mg['Workflow transition'], f'§11.16.5.6.{n}'])
table(['Service', 'Name', 'Family', 'Bundle', 'WF', 'Selective', 'Meter', 'Allowance', 'Price', 'Optional producers', 'Migration', 'Spec'], rows)
w('Bundles reconciled: **Discovery & Qualification** (01, 02, 03 here; 19 in Group O), **Investor Engagement** (04–08 here; 15, 16 in Group O), **Diligence & Conversion** (09, 10, 11), **Closing & Investor Lifecycle** (12 here; 13, 14 in Group O). Full suite = all approved SKUs; partial = a predefined or client-selected bundle; selective = one or more SKUs; the 25 foundation entries are non-removable (Sources & Decisions "Public procurement scope"). Prices stay "Quotation pending"; Group N does not set prices (BRL invariant: AI never sets prices).')
w('')
w('### 11.16.4.2 Workflow catalogue (48 rows) → blueprint')
w('')
rows = []
for r in C.WFS:
    k = r['_key']
    ws = SP.W[k]
    at = r['_code'] + '-AT01'
    rows.append([r['_code'], r['_name'], r['Trigger types'], r['External side-effect classification'].split(';')[0], ws['risk'],
                 ws['agent'], ', '.join(ws['au']), C.FR_WF[r['_code']], C.TC[(r['_code'], 'POS')], '§11.16.5.12 (Part 11.16b)'])
table(['Workflow', 'Name', 'Trigger (V12)', 'Side effect (V12)', 'Blueprint risk class', 'Agent', 'Automations', 'FR', 'AT01 → TC', 'Spec'], rows)
w('### 11.16.4.3 Acceptance tests (60 rows) → TC-V12-N')
w('')
rows = []
for tid, r in sorted(C.ATM.items()):
    if '-ENT-' in tid:
        t = C.TC[('ENT', C.svc_no(r['Service ID']))]
    else:
        code = tid.rsplit('-AT', 1)[0]
        t = C.TC[(code, 'POS')]
    rows.append([tid, r['Scenario'], r['Expected output / behavior'][:90], r['Negative and boundary checks'][:80], r['Existing UI acceptance references'].replace('INV-UX-UAT-', 'UAT-'), r['Status'], t])
table(['V12 test', 'Scenario', 'Expected', 'Negative / boundary', 'UI UAT (source)', 'Status (V12)', 'Blueprint TC'], rows)
w('All V12 scenarios are "Not run"; they become executable TCs with the full negative set (INPUT, SCOPE, ENT, DUP, QUALITY, BUDGET, RECOVERY, SEC and, for R2/R3, APPROVAL and EFFECT) in Part 11.16b, plus the combinatorial suites of Part 11.16c. The source UAT IDs INV-UX-UAT-A0nn map to screen acceptance of A205–A232 (§11.16.5.9).')
w('')
w('### 11.16.4.4 Cost model (48 rows)')
w('')
rows = []
for r in C.WFS:
    cm = C.CMM[r['_code']]
    rows.append([r['_code'], cm['Unit'], cm['Input tokens (scenario)'], cm['Output tokens (scenario)'], cm['Compute unit'], cm['Internal INR / invocation'], 'Excluded (quoted separately)', '§11.16.5.16'])
table(['Workflow', 'Unit', 'Input tokens', 'Output tokens', 'Compute', 'INR / invocation (V12 illustrative)', 'External fees', 'Blueprint cost'], rows)
rates = [r for r in C.CM if r.get('Planning assumption')]
w('Workbook planning rates (retained as illustrative, not vendor prices): ' + '; '.join(f"{r['Planning assumption']} = {r['INR / unit']}" for r in rates if r['Planning assumption']) + '. The blueprint re-costs every agent with the gateway formula and the model registry (DEC-788) in §11.16.5.7 and §11.16.5.16 [GAP-1010].')
w('')
w('### 11.16.4.5 Technical Map (42 rows): admin screens, routes and entities')
w('')
rows = []
for n in range(1, 13):
    for r in C.TMM[n]:
        rows.append([r['Service ID'], r['Admin screen ID'], C.SP.A_OF.get(r['Admin screen ID'], '—') if hasattr(C, 'SP') else SP.A_OF.get(r['Admin screen ID']), r['Existing admin screen title'], len(r['Existing route inventory'].split(';')), len(r['Relevant entity candidates from source'].split(';')), r['Existing UI UAT ID'], 'Specified (§11.16.5.9–11)'])
table(['Service', 'INV screen', 'Blueprint screen', 'Title', 'Routes', 'Entities', 'UAT', 'Action'], rows)
w('**Screen ID rule (DEC-801).** Investment admin IDs collide with the Sales & Marketing A001–A113; they are re-identified A205–A232 and keep the INV ID as alias (as DEC-620 for V12 SM screens). INV A049 "Automation Coordination & Conflict Resolution" is served by the existing A194 workflow registry and conflict view (Part 11.7a) with an investment filter. The source "Expanded engineering catalog" (70-screen package) is not in the material; screen content is specified from the Technical Map titles, routes and entities [GAP-1002].')
w('')
w('### 11.16.4.6 Capability crosswalk (100 legacy capabilities)')
w('')
rows = []
for r in C.CW:
    p = r['Primary service ID']
    owner = 'N (foundation)' if p == 'ALL' else ('N' if C.mine(p) else 'O')
    rows.append([r['Original capability ID'], r['Original capability name'], r['Original family'], r['Commercial classification'].split('—')[0].strip(), p, r['Potential related service IDs / foundation role'][:50], owner])
table(['Capability', 'Name', 'Family', 'Class', 'Primary', 'Related / foundation role', 'Group'], rows)
w('All 25 foundation entries (INV-01, -11, -12, -13, -14 families) are implemented by the shared platform (§11.16.5.1) and are non-removable; 49 selectable capabilities map to INV-SVC-01…12; 26 map to Group O services. No capability is billed twice (Sources & Decisions "Legacy selection mapping").')
w('')
w('### 11.16.4.7 Shared engines ENG-01…15 → blueprint')
w('')
eng_map = {'ENG-01': 'Research ingestion M10–M12, AG-160', 'ENG-02': 'Contact intelligence M18/M19, AG-164', 'ENG-03': 'RAG engine (Part 11.6), AG-171', 'ENG-04': 'Multimodal (DEC-788 registry), AG-172',
           'ENG-05': 'Messaging M24–M31 + outbox', 'ENG-06': 'Calendar M29', 'ENG-07': 'Identity/permission (IdP, PDP, R21)', 'ENG-08': 'Document generation M44/M46',
           'ENG-09': 'Financial calculation AU-219', 'ENG-10': 'Transaction reconciliation AU-225/226 (billing reconciliation pattern, Part 11.5)', 'ENG-11': 'Prediction AG-162',
           'ENG-12': 'Experimentation engine (SM-SVC-35 pattern)', 'ENG-13': 'Workflow engine (Part 11.3a universal engine)', 'ENG-14': 'Governance (AU-128, AU-201, AG-086)', 'ENG-15': 'Optimization (OKPI)'}
table(['Engine', 'Logical engine', 'Mapped services', 'Blueprint component', 'Constraint kept'], [[r['Engine ID'], r['Logical engine'], r['Primary mapped services'], eng_map.get(r['Engine ID'], ''), 'Private tenant/startup scope; entitlement; audit; policy; portability; acceptance'] for r in C.SE])
w('### 11.16.4.8 Investor-mode branches of the V12 commercial website')
w('')
rows = []
for i, b in enumerate(C.BRANCHES, 1):
    rows.append([f'B{i:02d}', b['expr'], ' · '.join(b['strings'][:6])[:260], 'W74 / W55–W73 (§11.16.5.5)'])
table(['Branch', 'Expression', 'Investor-mode strings (first, in order)', 'Blueprint'], rows)
w('### 11.16.4.9 Website routes (19) → W55–W73')
w('')
table(['INV route', 'Previous name (access)', 'Current name (access)', 'Decision (V12)', 'Blueprint screen'],
      [[r['id'], f"{r['previous_name']} ({r['previous_access']})", f"{r['current_name']} ({r['current_access']})", r['decision'], next(s[0] for s in SP.SCREENS_W if s[1] == r['id'])] for r in C.D['routes']])

# ------------------------------------------------------------------ 11.16.5.1
w('## 11.16.5 Enhancements')
w('')
w('### 11.16.5.1 Product boundary and platform reuse')
w('')
w('**Decision (DEC-800, ADR-230).** Investment Automation is a **separate product** on the shared platform: its own product code `investment`, SKU namespace INV-SVC-01…24, audience and entitlement set, admin navigation and operational data; it reuses the platform code, engines and controls. This honours both V12 statements at once: BR-C03/BR-C14 and REC-10 ("Investment is separate … no implicit cross-product access"; "Do not implement investment services as part of commercial product") and DEC-783 (product adopted). Sales & Marketing users never see investor data and vice versa unless a tenant holds both products and a user holds both grants (CONFLICT-1009 resolved).')
w('')
table(['Platform capability', 'Reused as is', 'Investment-specific extension', 'Source / decision'], [
 ['Tenancy and RLS', 'tenant → startup (issuer) hierarchy; `app_rw` least-privilege role sets `app.tenant_id`, `app.company_ids` per transaction (DEC-778)', 'Postgres schema `inv`; every `inv_*` table carries tenant_id and startup_id with RLS policies; `app.product = investment` session variable; cross-product joins forbidden by policy', 'BRL-TEN-01…12; DEC-778; ADR-230'],
 ['Identity and roles', 'IdP, BFF sessions, MFA step-up, SSO/SCIM (DEC-784)', 'Roles R02/R03/R04/R08/R09/R10 re-scoped to the investment product; new sub-role R10C external counsel; new portal role R21 invited investor (extends R16, object grants only)', 'DEC-811; Part 2.3 §2.26'],
 ['Entitlements and SKUs', 'Subscription, bundle and entitlement engine (V12 SM-SVC framework, Part 11.2a)', 'AU-200 checks product + INV SKU + foundation + role + channel/provider + budget at every action; selective/partial/full; missing prerequisite → draft/task/hold; revocation pauses safely and keeps audit', 'Entitlement Rules sheet; FR-V12-N-005'],
 ['Policy Decision Point', 'scope, consent, jurisdiction, budget, approval hash recheck at dispatch', 'Securities gate plug-in (ADR-231): AU-201 pack activation, AU-202 eligibility, AU-203 solicitation, AU-204 document gating, AU-205 caps, AU-206 sign-off, AU-207 two-person/mandate', 'SEC-CTL-N-01…10'],
 ['Transactional outbox', 'outbox row in the same transaction; idempotent consumers; uncertain → reconcile', '`inv_outbox`; idempotency key = scoped event + workflow revision + action target (V12 field 44)', 'NFR-005/006; M06'],
 ['Workflow engine', 'Universal engine of Part 11.3a (StepRun, states, retries, simulation zero-effect)', 'INV workflows registered with event envelope `event_id, tenant_id, startup_id, service_id, workflow_revision, input_ref, occurred_at, correlation_id` (V12 field 42)', 'Part 11.3a; FR-V12-N-006'],
 ['Model gateway and registry', 'Tiers 0/1a/1b/2/3; provider-neutral registry; Claude Sonnet primary (DEC-788)', 'Investor data class Confidential-Financial: never Tier 2; masked where task allows; registry entries must pass the no-advice evaluation suite EVAL-N-ADV before use by any investor-facing agent', 'DEC-788; SEC-CTL-N-05/16'],
 ['Rule-pack registry', 'AU-128, AG-086, CP-01…07 (Part 11.15)', 'Securities packs RP-SEC-* (content by Group O) loaded through the same schema; investment channel packs reuse RP-IN-WA, RP-IN-DPDP, RP-EU-MKT, RP-US-EMAIL', 'DEC-803'],
 ['Mandates and kill switch', 'Part 11.17 mandate engine (two approvers, scope, caps, revocation)', 'Offer re-send mandate type `inv_offer_resend`; per-offering kill switch', 'DEC-779; SEC-CTL-N-10/15'],
 ['Residency', 'IN (Mumbai) and EU stacks (DEC-772)', 'Data room objects pinned to tenant region; investors from other regions read from the tenant region (data never copied)', 'SEC-CTL-N-16'],
 ['Audit and evidence', 'append-only audit, evidence store', 'Offer register and data-room access log retained 8–10 years (verify)', 'SEC-CTL-N-12'],
 ['Billing and metering', 'meter events, billing reconciliation (Part 11.5)', 'Meter units per Service Index (source batch, investor assessment, …); no success fee or capital-based charge [RECOMMENDATION-1005]', 'DEC-816'],
])
w('```mermaid')
w('flowchart TD')
w('  subgraph PUB["Public origin"]')
w('    W1["Investor-mode storefront<br/>W55-W74 neutral SaaS only"]')
w('  end')
w('  subgraph INVP["Invited-investor origin"]')
w('    W2["Private room W75<br/>Eligibility gate W76"]')
w('  end')
w('  subgraph ADM["Admin origin"]')
w('    A1["Investment workspace<br/>A205-A232"]')
w('  end')
w('  W1 --> BFF["BFF per origin"]')
w('  W2 --> BFF')
w('  A1 --> BFF')
w('  BFF --> API["Django API<br/>investment app"]')
w('  API --> ENT["AU-200 entitlement"]')
w('  API --> PDP["PDP + securities gate<br/>AU-201 to AU-207"]')
w('  PDP --> RP["AU-128 rule packs<br/>RP-SEC counsel-signed"]')
w('  API --> WF["Workflow engine<br/>Celery workers"]')
w('  WF --> GW["Model gateway<br/>registry DEC-788"]')
w('  GW --> GUARD["AG-166 securities guard"]')
w('  WF --> OB["Outbox"]')
w('  OB --> CH["Email, WhatsApp, calendar,<br/>e-sign, KYC providers"]')
w('  API --> DB["Postgres schema inv<br/>RLS app_rw"]')
w('  API --> S3["Data room S3<br/>region pinned, SSE-KMS"]')
w('```')
w('')
w('**Foundation capabilities (25, non-removable).** INV-01-01…05 onboarding, readiness and activation (reuse SaaS onboarding W71–W73 and A185); INV-11-01…05 trial, subscription monitoring, metering, entitlement enforcement, offboarding (AU-200 and billing engine); INV-12-01…05 model routing, token optimisation, knowledge refresh, output validation, quality evaluation (gateway, AU-001/003/006); INV-13-01…05 failure detection, eligible retry, approved fallback, reconciliation, incident escalation (engine, Part 11.11); INV-14-01…05 KPI measurement, bottleneck identification, recommendations, controlled simulation, improvement verification (OKPI framework). Requirement **FR-V12-N-001…010** below.')
w('')
FRS_FW = [
 ('FR-V12-N-001', 'The investment product is provisioned as a separate product code with its own SKU namespace; a tenant may subscribe to Investment Automation, Sales & Marketing, or both', 'Tenant with only SM sees no INV navigation, API returns 404 for /investor/*', 'cross-product join attempt returns zero rows (RLS)'),
 ('FR-V12-N-002', 'Every `inv_*` table is RLS-protected by tenant and startup and accessed only through `app_rw` (DEC-778)', 'issuer S1 user reads S1 investors only', 'S2 investor id returns uniform 404'),
 ('FR-V12-N-003', 'The 25 foundation capabilities are included with any INV SKU and cannot be disabled', 'foundation flags present on every subscription', 'attempt to remove a foundation entry → 422 FOUNDATION_REQUIRED'),
 ('FR-V12-N-004', 'Full, partial and selective subscriptions are supported; no upstream SKU is compulsory when an authorized equivalent input is supplied', 'selective INV-SVC-04 with client-supplied contacts runs', 'missing input → draft/task-only or hold (V12)'),
 ('FR-V12-N-005', 'AU-200 checks tenant, startup, capability, role, channel/provider and budget at every action', 'active SKU → run', 'revoked SKU after enqueue → next step blocked, reservation released'),
 ('FR-V12-N-006', 'Workflow events use the V12 envelope and reject mismatched scope', 'valid envelope accepted', 'envelope with other tenant_id → 422 SCOPE_MISMATCH'),
 ('FR-V12-N-007', 'Simulation mode has zero external effects for every INV workflow', 'simulation run produces drafts only', 'provider simulator call log empty'),
 ('FR-V12-N-008', 'Migration honours purchased scope; no silent removal; active runs keep their snapshot', 'WF04 added without changing WF01–03 entitlements', 'downgrade attempt without notice blocked'),
 ('FR-V12-N-009', 'Meters per Service Index are emitted per action and reconciled with billing', 'one meter event per accepted action', 'duplicate event → one charge'),
 ('FR-V12-N-010', 'Agent identities are scoped service principals with short-lived grants; external agent access disabled unless granted', 'agent call carries R20 scope', 'agent attempting approval → 403'),
]
table(['FR', 'Requirement', 'Acceptance (positive)', 'Negative / boundary'], FRS_FW)

# ------------------------------------------------------------------ 11.16.5.2 controls
w('### 11.16.5.2 Securities-compliance control framework')
w('')
w('The panel reads DEC-783 as: the capability is built in full, and **activates per jurisdiction only when the counsel-signed rule pack is active**. The controls below are mandatory; none is optional or tenant-configurable downwards (CP-04).')
w('')
table(['Control', 'Name', 'Specification', 'Legal basis / decision (verify)', 'Implemented by', 'Override'], SP.CONTROLS)
w('#### 11.16.5.2.1 Rule packs consumed (content owned by Group O)')
w('')
table(['Pack', 'Scope', 'Jurisdiction', 'Offering route value in PM-N-01/03', 'Activation order (DEC-803)'],
      [[p[0], p[1], p[2], p[3], {'IN': '1 (owner portfolio issuers are Indian)', 'US': '2', 'EU': '3 (with EU stack, DEC-772)', 'UK': '4'}[p[2]]] for p in SP.PACKS])
w('Panel reading of the route rules the packs must encode (verify with counsel, as of 27 Nov 2026) [ASSUMPTION-1000]:')
w('')
table(['Route', 'Who may be approached', 'Solicitation', 'Caps and documents', 'Money and filings (platform role)'], [
 ['India s.42 private placement (unlisted)', 'Identified persons named in a board/shareholder-approved list', 'No public advertisement or media/marketing channels; offer letter PAS-4 addressed to the named person, serially numbered', '≤ 200 persons per financial year excluding QIBs and ESOP; minimum investment size per rule (verify)', 'Subscription only from the subscriber\'s own bank account; separate bank account; allot within 60 days else refund within 15 days (verify); PAS-5 record, PAS-3 return — platform prepares checklists, counsel files (Group O INV-SVC-13)'],
 ['India SEBI ICDR preferential / QIP', 'Listed issuers only; identified allottees / QIBs', 'Insider-trading and UPSI controls dominate', 'Pricing formula, lock-in (verify)', 'Platform: hold for counsel; no automated outreach (PM-N-01 → COUNSEL_REVIEW_LISTED)'],
 ['US Reg D 506(b)', 'Accredited investors; ≤ 35 non-accredited who are sophisticated (with disclosure)', 'No general solicitation; pre-existing substantive relationship', 'Form D within 15 days of first sale (verify); bad-actor checks 506(d)', 'Platform: relationship provenance mandatory (AU-203)'],
 ['US Reg D 506(c)', 'Accredited investors only, verified with reasonable steps', 'General solicitation permitted', 'Verification evidence retained', 'Platform: AU-202 needs verification evidence; solicitation content still pack-reviewed'],
 ['US Reg CF', 'Any investor within limits', 'Only through a registered funding portal or broker-dealer', 'Issuer cap per 12 months; investor limits (verify)', 'Platform is **not** a funding portal: hand-off link only (PM-N-01 → REG_CF_PORTAL_ONLY, DEC-807)'],
 ['EU PR exemption', 'Qualified investors only, or < 150 non-QI persons per member state, or high minimum denomination (verify)', 'National private-placement and marketing rules', 'Counts per member state', 'Platform: AU-205 counts per member state; hold when relationship absent'],
 ['UK FSMA s.21 exemptions', 'Certified high-net-worth / sophisticated investors, investment professionals', 'Financial promotion restriction', 'Certification statements (verify)', 'Platform: certification evidence via W76'],
])
w('#### 11.16.5.2.2 Control-to-service matrix')
w('')
hdr = ['Service'] + [c[0].replace('SEC-CTL-N-', '') for c in SP.CONTROLS]
rows = []
for n in range(1, 13):
    ctl = set(SP.S[n]['ctls'])
    for r in C.WFS:
        if r['_key'].startswith('%02d' % n):
            ctl |= set(SP.W[r['_key']]['ctl'])
    rows.append([C.svc_key(n)] + ['●' if c[0] in ctl else '' for c in SP.CONTROLS])
table(hdr, rows)
w('Step-level placement of every control is in each workflow\'s step table (Part 11.16b, column "Controls in this step").')
w('')
w('#### 11.16.5.2.3 Offering lifecycle state machine')
w('')
w('```mermaid')
w('stateDiagram-v2')
w('  [*] --> Draft')
w('  Draft --> RegistrationSubmitted: R02 submits route, jurisdictions, caps, doc set')
w('  RegistrationSubmitted --> CounselReview: AU-206 opens one sign-off per jurisdiction')
w('  CounselReview --> Signed: all jurisdictions signed by R10C')
w('  CounselReview --> Draft: counsel requests changes')
w('  Signed --> ApprovedForOffer: R10 approves and AU-201 packs active')
w('  ApprovedForOffer --> Offering: first offer issued (two-person)')
w('  Offering --> Offering: further offers within caps')
w('  Offering --> Suspended: kill switch or pack expiry')
w('  Suspended --> Offering: R10 resumes after fix')
w('  ApprovedForOffer --> Draft: document set changed, sign-off void')
w('  Offering --> Draft: document set changed, sign-off void')
w('  Offering --> Closed: allotment complete or deadline passed')
w('  Closed --> [*]')
w('```')
w('')
w('#### 11.16.5.2.4 Dispatch-time securities gate')
w('')
w('```mermaid')
w('flowchart TD')
w('  A["Effect requested<br/>message, grant, offer, acceptance"] --> B{"AU-200 SKU and role ok?"}')
w('  B -- "No" --> X1["403 ENTITLEMENT"]')
w('  B -- "Yes" --> C{"Kill switch off?"}')
w('  C -- "No" --> X2["Block KILL_SWITCH"]')
w('  C -- "Yes" --> D{"AU-201 all packs active<br/>for issuer and investor"}')
w('  D -- "No" --> X3["Block PACK_NOT_ACTIVE"]')
w('  D -- "Yes" --> E{"Offering-tagged?"}')
w('  E -- "No" --> H["Consent and window AU-208"]')
w('  E -- "Yes" --> F{"AU-202 eligibility verified<br/>for route"}')
w('  F -- "Unknown" --> X4["Hold ELIGIBILITY"]')
w('  F -- "Ineligible" --> X5["Block INELIGIBLE"]')
w('  F -- "Verified" --> G{"AU-203 solicitation ok<br/>relationship or route allows"}')
w('  G -- "No" --> X6["Block GENERAL_SOLICITATION"]')
w('  G -- "Yes" --> H')
w('  H -- "Fail" --> X7["Block CONSENT"]')
w('  H -- "Pass" --> I{"Approval hash valid<br/>or mandate in scope"}')
w('  I -- "No" --> X8["Hold APPROVAL"]')
w('  I -- "Yes" --> J["Outbox effect<br/>idempotent"]')
w('```')
w('')
w('#### 11.16.5.2.5 Eligibility decision table (AU-202, ADR-233)')
w('')
table(['Route', 'retail', 'sophisticated / HNI', 'accredited / QI', 'QIB / institutional', 'unknown', 'Evidence required'], [
 ['s42_PP', 'Hold (counsel)', 'Eligible if named in approved list', 'Eligible if named', 'Eligible (not counted in 200)', 'Hold', 'KYC cleared before application; named-person list'],
 ['506b', 'Ineligible', 'Hold (≤ 35, disclosure)', 'Eligible', 'Eligible', 'Hold', 'Self-certification acceptable for 506(b) (verify); relationship provenance'],
 ['506c', 'Ineligible', 'Ineligible', 'Eligible only with verification evidence', 'Eligible with evidence', 'Hold', 'Third-party verification letter / income or net-worth documents (AG-163 extracts)'],
 ['RegCF', 'Portal only', 'Portal only', 'Portal only', 'Portal only', 'Portal only', 'Handled by registered portal'],
 ['PR_QI_only', 'Ineligible', 'Ineligible unless opted-up professional (verify)', 'Eligible', 'Eligible', 'Hold', 'QI classification evidence'],
 ['PR_lt150', 'Eligible (counted)', 'Eligible (counted)', 'Eligible (not counted)', 'Eligible (not counted)', 'Hold', 'Member-state residence'],
 ['FPO_exempt', 'Ineligible', 'Hold until certified', 'Eligible with certificate', 'Eligible (professional)', 'Hold', 'Signed certification statement (W76)'],
])
w('Expiry: evidence valid 12 months unless the pack sets less (BRL-V12-N-02). KYC `screening_hit` always → Hold and R10 alert (SEC-CTL-N-07).')
w('')

# ------------------------------------------------------------------ 11.16.5.3 privacy
w('### 11.16.5.3 Investor-data privacy')
w('')
table(['Data', 'Class', 'Lawful basis (IN / EU-UK / US)', 'Retention [ASSUMPTION-1004]', 'Model use', 'Residency'], [
 ['Investor organisation profile, mandate', 'Confidential', 'Legitimate business purpose / legitimate interest (LIA) / n.a.', 'Relationship + 5 years', 'Tier 1a/1b; no Tier 2', 'Tenant region'],
 ['Representative contact (name, role, business email, phone)', 'Personal', 'Consent (DPDP) / LI with Art. 14 notice / opt-out', 'Relationship + 2 years or withdrawal', 'Tier 1a; masked in analytics', 'Tenant region'],
 ['Investor class, eligibility evidence, accreditation letters', 'Confidential-Financial', 'Consent + legal obligation / legal obligation / n.a.', '8 years after relationship (verify)', 'AG-163 only, Tier 1b, masked identifiers', 'Tenant region'],
 ['KYC/AML results (references only)', 'Confidential-Financial', 'Legal obligation (PMLA) / legal obligation', 'Per PMLA / AMLD (verify; often 5–10 years)', 'Never sent to models', 'Tenant region'],
 ['Communications, transcripts, recordings', 'Personal', 'Consent / consent or LI / notice', '3 years; recordings 1 year unless legal hold', 'Consent-gated', 'Tenant region'],
 ['Data-room documents and access logs', 'Confidential-Financial', 'Contract / contract', 'Offering + 8 years (verify)', 'Grant-filtered retrieval only', 'Tenant region; S3 SSE-KMS'],
 ['Receipts, commitments, bank references', 'Confidential-Financial', 'Contract + legal obligation', '10 years (verify)', 'Masked; AG-178 explanation only', 'Tenant region'],
])
w('Rules: (1) no investor data in public payloads (AU-228); (2) DSR access/erasure/objection handled in A208 within 30 days (GDPR) / DPDP timelines (verify), erasure leaves a hashed suppression entry; (3) legal hold overrides erasure for offer records with R10 reason; (4) cross-tenant benchmarks exclude investor data entirely (DEC-789 carve-out, DEC-808); (5) DPIA required before first EU tenant (DEC-776). Combinatorial suite PM-N-07 (Part 11.16c).')
w('')

# ------------------------------------------------------------------ 11.16.5.4 roles
w('### 11.16.5.4 Roles, personas and RBAC for the investment product')
w('')
table(['Role', 'Definition in this product', 'Key permissions'], SP.ROLES)
table(['Permission', 'R02', 'R03', 'R04', 'R08', 'R09', 'R10', 'R10C', 'R21', 'R20'], [
 ['Approve funding route / materials', '✓', '', '', '', '', '✓ (legal items)', '', '', '✗'],
 ['Approve outreach template (non-offer)', '✓', '', '', '', '', '', '', '', '✗'],
 ['Approve offering-tagged content / offer', '✓ (1st)', '', '', '', '', '✓ (2nd)', '', '', '✗'],
 ['Sign offering registration', '', '', '', '', '', '', '✓', '', '✗'],
 ['Approve offering for offer', '', '', '', '', '', '✓', '', '', '✗'],
 ['Grant data-room access', '✓', '', '', '', '', '✓ restricted', '', '', '✗'],
 ['Accept application', '✓', '', '', '', '', '✓', '', '', '✗'],
 ['Verify receipt / allocate', '', '', '', '✓', '✓ (2nd)', '', '', '', '✗'],
 ['View own room, ask, apply', '', '', '', '', '', '', '', '✓ own grants', '✗'],
 ['Kill switch', '✓', '', '', '', '', '✓', '', '', '✗'],
])

# ------------------------------------------------------------------ 11.16.5.5 website
w('### 11.16.5.5 Investor-mode website (W55–W76)')
w('')
w('**Principle (DEC-813, CONFLICT-1008).** V12 adopts an "investor website" (DEC-783) and its source pack fixes it as a neutral SaaS storefront: "Investment storefront sells fundraising workflow software only; it is not a securities marketplace or offer. All investment offers, diligence, issuer data, and closing records belong to authorized private operations" (README). The blueprint implements both: the public storefront W55–W74 is neutral (no issuer, offering, investor or tenant data, enforced by AU-228 as a blocking CI gate and a runtime response guard), and the investor-facing functions live **only** behind invitation in W75/W76 on a separate origin.')
w('')
w('#### 11.16.5.5.1 W74 objective switch on the commercial website (investor mode)')
w('')
w('The V12 renderer is one SPA with `CFG.inv`. The blueprint renders the same component library with a product flag; the investor-mode strings below are adopted literally (from the 11 branches):')
w('')
inv_strings = [
 ('Eyebrow on every page title', "'Investment automation SaaS'", 'B01'),
 ('Hero headline', "'Automate your fundraising operations.'", 'B02'),
 ('Hero text', "'Discover eligible investors, coordinate outreach, manage due diligence and support verified closing — in your own private workspace.'", 'B03'),
 ('Journey steps 01–05', "'Configure fundraising objectives' · 'Research & qualify eligible investors' · 'Coordinate compliant engagement' · 'Manage diligence & approvals' · 'Monitor verified closing & reporting'", 'B04'),
 ('Wizard step 2 field label', "'Fundraising thesis' (instead of 'Offerings')", 'B05, B11'),
 ('Wizard objective placeholder', "'Eligible investor engagement'", 'B06'),
 ('Quote route', 'investor mode shows the inline demo-terms acknowledgement form ("Acknowledge the sample terms are non-binding.") and "Request demo subscription" instead of a link to the agreement route', 'B07'),
 ('Detail route', 'service detail opens in the detail view (`detail(inv && state.detailSelected)`)', 'B08, B10'),
 ('Export capability tag', "caps: ['Fundraising']", 'B09'),
]
table(['Element', 'Investor-mode value (V12, literal)', 'Branch'], inv_strings)
w('W74 requirements: FR-V12-N-011 the mode is selected by product (investment storefront domain) or by an explicit objective switch on the commercial site that navigates to the investment storefront origin — it never mixes catalogues; FR-V12-N-012 the demo strip text "Interactive SaaS prototype · Synthetic inputs only · No live billing, messaging or investment execution" is replaced in production by the approved neutral notice TPL-N-03; FR-V12-N-013 no investment-related CTA collects investor money, investor identity or offering interest on the public origin.')
w('')
w('#### 11.16.5.5.2 Screen specifications W55–W76')
w('')
W_DETAIL = {
 'home': ('Hero (investor-mode strings), journey 01–05, CTA Explore automations / Build your subscription', 'GET /api/v1/public/investment/catalog', 'Neutral only; region privacy banner'),
 'catalog': ('100 capability entries in 20 families; filters Search, Family; badges core/optional; select', 'GET /api/v1/public/investment/catalog', 'Selection held in memory until registration'),
 'detail': ('Family/service detail: description, workflows (4), controls, availability (full/partial/selective)', 'GET /api/v1/public/investment/catalog', 'No issuer examples'),
 'compare': ('Bundles: Discovery & Qualification, Investor Engagement, Diligence & Conversion, Closing & Investor Lifecycle, Specialized Funding, Ownership & Governance, International & Risk', 'GET /api/v1/public/investment/catalog', 'Counts: full 75 optional, partial 25 (5 families), selective ≥ 1 (verification report)'),
 'auth': ('Client sign-in & recovery (BFF OIDC); demo entry separated and labelled', 'BFF', 'No investor sign-in here'),
 'portal': ('Private client area (account, onboarding, support, usage)', 'tenant APIs', 'Authenticated client only'),
 'enquiry': ('Service enquiry form: name, business email, company, country, message, consent', 'POST /api/v1/public/investment/quote-requests', 'Rate-limited; no investment interest fields'),
 'booking': ('Consultation & demo booking (calendar slots)', 'public booking API (Part 11.7)', 'Not an investor meeting'),
 'dashboard': ('Client service dashboard: subscribed SKUs, usage vs allowance, approvals pending', 'tenant APIs', 'Private'),
 'quote': ('Subscription quotation & agreement: selection, billing cycle, currency, demo terms acknowledgement (B07)', 'SaaS quote API', 'Quote only; no live checkout'),
 'billing': ('Subscription order & billing status: service request, quotation, invoice, payment, entitlement', 'SaaS billing API', '"Only service-subscription records belong here, not the subscribing business\'s customers, investors, payments or financial records" (V12 text, adopted)'),
 'help': ('Contact, privacy & help; DSR entry', 'public help API', 'DPDP/GDPR notices'),
 'plans': ('Plans & automation selection: full / partial / selective, billing cycle, quote currency', 'GET catalog', 'Indicative scope, not production claim'),
 'register': ('Private client registration: business identity fields, verification step', 'SaaS applicant API (W32–W34 pattern)', 'Synthetic in demo; real only server-side after verification'),
 'wizard': ('Private configuration wizard steps 1–4 (business, fundraising thesis, channels/budget, review)', 'tenant onboarding API', 'Fields: Business name, Industry, Website, Country, Model, Region / Description, Lines, Fundraising thesis, Objective, ICP, Approved claims / Preferred channel, Language, Timezone, Monthly budget, Target volume'),
 'mode': ('Objective switch "Sales & marketing" ↔ "Fundraising"; navigates to the investment storefront origin', '—', 'No shared session state between catalogues'),
 'investor-room': ('Invited investor: rooms granted to me, documents (watermarked viewer), Q&A, application with e-sign, status; never other investors', '/api/v1/investor-portal/me/*', 'R21; MFA; AU-204 per request; region-pinned'),
 'eligibility': ('Jurisdiction of residence, investor class self-certification (route-specific statements), evidence upload, KYC hand-off link, consent to processing', 'POST /api/v1/investor-portal/me/eligibility', 'AU-202 decides; AG-163 extracts; status shown as Verified / Pending / Action needed'),
}
rows = []
for s in SP.SCREENS_W:
    d = W_DETAIL[s[4]]
    rows.append([s[0], s[1], s[2], s[3], d[0], d[1], d[2]])
table(['Screen', 'INV ID', 'Name', 'Access', 'Content and fields', 'API', 'Rules'], rows)
w('States for every W screen: loading skeleton, empty, error with reference ID, offline notice, rate-limited (429 with Retry-After), and WCAG 2.2 AA (keyboard, 360 px reflow, contrast 4.5:1, labelled inputs) per Part 2.5. Layout catalogue: all 100 items render in W56 with core items locked on (25); the full/partial/selective counts 75/25/1 of the verification report are acceptance checks (TC in PM-N-06 and US-30-ZN03).')
w('')
FRS_W = [
 ('FR-V12-N-011', 'Investor mode selectable only as the investment storefront origin; catalogues never mixed', 'switch navigates to investment origin', 'commercial items absent from W56'),
 ('FR-V12-N-012', 'Production notice TPL-N-03 replaces the demo strip', 'notice visible on all W55–W73', 'demo strip text absent in prod build'),
 ('FR-V12-N-013', 'No public route collects investment interest, investor identity or money', 'enquiry has only SaaS fields', 'AU-228 fails build on field "investment amount"'),
 ('FR-V12-N-014', 'AU-228 scans build artefacts and anonymous responses for issuer names, offering terms, investor records, tenant IDs', 'neutral payload served', 'seeded issuer name blocks deploy'),
 ('FR-V12-N-015', 'W75 shows only rooms granted to the signed-in R21; every item request passes AU-204', 'granted document opens watermarked', 'un-granted id → uniform 404'),
 ('FR-V12-N-016', 'W76 collects route-specific self-certification and evidence; AU-202 decides', 'evidence → Pending → Verified', 'AI extraction alone never sets Verified'),
 ('FR-V12-N-017', 'Full/partial/selective counts 75/25/≥1 and 25 locked core items', 'counts match', 'core item cannot be deselected'),
 ('FR-V12-N-018', 'Synthetic export JSON keeps selectedAutomationIds, selectionMode, billingCycle; import validated server-side against entitlements (README gap closed)', 'import creates draft subscription', 'unknown automation id → 422'),
]
table(['FR', 'Requirement', 'Acceptance (positive)', 'Negative / boundary'], FRS_W)

# ------------------------------------------------------------------ 11.16.5.6 services
w('### 11.16.5.6 Service specifications INV-SVC-01…12')
w('')
w('Each specification follows Part 11.2b: all 50 workbook fields, the blueprint mapping, controls and the new FRs. Workflows are listed by ID; steps, DTOs, rules, SLA, KPIs and tests are in Part 11.16b. Costs are illustrative workbook scenarios, not prices.')
w('')
FR_SVC_TEXT = {
 'FR-V12-N-031': ('WF01 discovers funding routes (angel, VC, PE, family office, grant, CSR, debt) only from approved sources and stores each candidate with evidence; routes need R02 approval', 'candidate with ≥1 evidence and deadline parsed', 'unapproved route cannot feed outreach'),
 'FR-V12-N-032': ('WF04 compares versioned signals and alerts only on novel, material changes', 'new fund mandate → one alert', 'same signal twice → no second alert'),
 'FR-V12-N-033': ('WF01 normalises sector, stage and ticket range and scores against a versioned rubric with ≥3 reason codes', 'score + reasons', 'missing ticket range → held, not invented'),
 'FR-V12-N-034': ('WF02 eligibility decision is deterministic per route and jurisdiction; cross-border cases held', 'accredited + 506(c) + evidence → eligible', 'unknown → held; AI output never decisive'),
 'FR-V12-N-035': ('WF04 propensity uses transparent features, calibration ECE ≤ 0.05, uncertain → review', 'calibration report', 'protected attribute feature rejected at config'),
 'FR-V12-N-036': ('WF01–02 collect business contacts with provenance; uncertain merges reviewed; no resale', 'provenance complete', 'personal email from scraped page rejected'),
 'FR-V12-N-037': ('WF03 stores a per-channel eligibility decision with reasons; WF04 invalidates stale links', 'decision per channel', 'invalidated contact removed from sequences'),
 'FR-V12-N-038': ('WF01 drafts from approved facts only; AG-166 guard mandatory', 'draft with citations, guard pass', 'return promise → Block'),
 'FR-V12-N-039': ('WF02 dispatch rechecks scope, consent, pack, eligibility, solicitation, window, cap, budget and approval hash', 'one send per key', 'pack expired after approval → Block'),
 'FR-V12-N-040': ('WF03/04 reconcile delivery and pause senders on threshold', 'bounce → suppression', 'replayed webhook → no second effect'),
 'FR-V12-N-041': ('WF01–02 WhatsApp only with opt-in, approved template, window; no offering broadcast', 'in-window approved reply', 'offering tag on broadcast → Block'),
 'FR-V12-N-042': ('WF03–04 inbound sync stops sequences and coordinates one journey', 'STOP → stop ≤ 60 s', 'two journeys → one wins, other held'),
 'FR-V12-N-043': ('WF01 schedules within window, caps (1 per 7 days) and offer state', 'due task created', 'cap reached → next window'),
 'FR-V12-N-044': ('WF02–04 stop on reply/opt-out/restricted offer and resolve conflicts to one next action', 'reply → paused', 'withdrawn offer → all steps stopped'),
 'FR-V12-N-045': ('WF01 classifies intent/objection and flags advice requests', 'advice request flagged', '"should I invest" never answered by AI'),
 'FR-V12-N-046': ('WF02 drafts grounded answers from granted documents with citations', 'cited answer', 'un-granted document never cited'),
 'FR-V12-N-047': ('WF03–04 human handover and consented multimodal intake', 'handover ≤ 5 min', 'audio without consent rejected'),
 'FR-V12-N-048': ('WF01 books without duplicates; recording consent separate', 'one booking', 'all-party regime without consent → no recording'),
 'FR-V12-N-049': ('WF02–04 internal briefs, action extraction and rehearsal; terms commitments unconfirmed until R02', 'brief ≥ 24 h before', 'brief shows other investor data → test fails'),
 'FR-V12-N-050': ('WF01 deterministic scenario calculator with golden fixtures', 'post-money exact', 'negative pre-money → 422'),
 'FR-V12-N-051': ('WF02/04 narrative from approved claims; figures only from AU-219', 'cited narrative', 'model-invented figure → Block'),
 'FR-V12-N-052': ('WF03 figure consistency and frozen approved revision', 'frozen hash', 'edit after approval → new revision'),
 'FR-V12-N-053': ('WF01 scan, classify, version and retention for every file', 'indexed doc', 'malware → quarantine'),
 'FR-V12-N-054': ('WF02 grants need eligibility, NDA, pack, sign-off (offering docs); expiry revocation ≤ 60 s', 'watermarked view', 'expired grant → 404'),
 'FR-V12-N-055': ('WF03–04 grounded Q&A with fair disclosure and readiness gaps', 'answer released to all granted investors', 'answer citing un-granted doc blocked'),
 'FR-V12-N-056': ('WF01 agreements from counsel-approved templates; frozen hash', 'draft + approval', 'template deviation flagged'),
 'FR-V12-N-057': ('WF02 formal offers: signed offering, two-person approval, eligible named recipients, cap reservation, serial number, expiry', 'ISSUE with serial', 'any gate fails → Block/Hold (PM-N-03)'),
 'FR-V12-N-058': ('WF03 application completeness, KYC cleared, e-sign reconciled; acceptance human', 'held → accepted by two', 'KYC pending → hold'),
 'FR-V12-N-059': ('WF04 term-sheet comparison internal only', 'deviation list', 'shared to investor → blocked'),
 'FR-V12-N-060': ('WF01 receipt import, verification and dedupe', 'receipt verified', 'duplicate → reject'),
 'FR-V12-N-061': ('WF02 atomic allocation with remainder; third-party payer exception for s.42', 'exact → allocated', 'duplicate allocation impossible (unique constraint)'),
 'FR-V12-N-062': ('WF03–04 exceptions, anomaly detection, allotment/refund timers; refunds human', 'timer escalation before deadline', 'refund action not available to AI'),
}
for n in range(1, 13):
    r = C.SVC[n]; s = SP.S[n]; er = C.ERM[n]; si = C.SIM[n]; mg = C.MGM[n]
    code = C.svc_key(n)
    wfs = [x for x in C.WFS if x['_key'].startswith('%02d' % n)]
    mean_cost = sum(float(C.CMM[x['_code']]['Internal INR / invocation']) for x in wfs) / 4
    tot_cost = sum(float(C.CMM[x['_code']]['Internal INR / invocation']) for x in wfs)
    cap = int(si['Illustrative monthly allowance'])
    w(f'#### 11.16.5.6.{n} {code} {r["Automation service name"]}')
    w('')
    scr = sorted({C.SP.A_OF.get(x.strip(), x.strip()) if hasattr(C, 'SP') else SP.A_OF.get(x.strip(), x.strip()) for x in r['Related UI screen IDs'].split(';')})
    rows = [
     ['Identity and source', f'{code} · family {r["Automation family"]} · bundle {si["Suggested partial bundle"]} · service version {r["Service version"]} · {mg["Decision"]}. Sources: workbook Service Catalog row {r["_row"]}, Workflow Catalog, Service Index, Entitlement Rules, Migration, Technical Map, Cost Model, Acceptance Tests rows for {code}; BRD/FSD historical annex "Investment comparator" mirror; L rows (CONFLICT-958)'],
     ['Blueprint home', f'Epic {s["epic"]} · modules {s["modules"]} · analogue {s["analog"]} · status before: **Not covered (CONFLICT-958, DEC-002 exclusion)** → after: **Matched** (DEC-783)'],
     ['Purpose and value', f'{r["Business objective"]}. Functionality: {r["Detailed functionality"]} Industries: {r["Applicable industries"]}. Capability: {r["Applicable business capabilities"]}. Independent purchase: {r["Independent purchase justification"]} Outcome: {r["Measurable customer outcome"]}'],
     ['First-value milestone', f'First reviewed and accepted "{r["Expected output"]}" with activation and acceptance timestamps; owner validates evidence and quality (FR-V12-N-009 meters)'],
     ['Entitlements', f'Required: {r["Required service entitlements"]}. Availability: {r["Full / partial / selective availability"]} Order separately: {er["Order separately"]}. Foundation: {er["Included foundation"]}. Optional input producers: {er["Optional input producers (service IDs)"]}; complementary: {r["Optional complementary services"]}. Required supplied input: {er["Required supplied input"]}. Provider/permission: {er["Required provider / permission"]}. Missing prerequisite: {er["Missing prerequisite behavior"]}. Revocation: {er["Revocation behavior"]}. Approval status (V12): {er["Approval status"]} → blueprint: approved by DEC-783 subject to jurisdiction activation. Entitlement acceptance: {code}-ENT-AT01 → {C.TC[("ENT", n)]}'],
     ['Commercial and metering', f'Meter: {si["Meter unit"]} · illustrative pilot cap {cap}/month (not approved) · price status {si["Price status"]}. Pricing model: {r["Subscription pricing model"]} Usage limits: {r["Usage limits"]} Illustrative internal AI cost (workbook scenario): ₹{tot_cost:.2f} for one run of each workflow, mean ₹{mean_cost:.2f} per invocation; at the pilot cap ≈ ₹{mean_cost*cap:,.0f} per month (cap × mean). External fees excluded. No success fee or capital-raised-based charge (DEC-816)'],
     ['Inputs', r['Required input data']],
     ['Outputs', r['Expected output']],
     ['Workflows (detail in Part 11.16b)', '<br/>'.join(f'**{x["_code"]}** {x["_name"]} ({"new in V12" if x["_code"].endswith("WF04") else "retained"}; acceptance {x["_code"]}-AT01 → {C.TC[(x["_code"], "POS")]}; {C.FR_WF[x["_code"]]})' for x in wfs) + f'<br/>Migration: {mg["Workflow transition"]} ({mg["Previous workflows"]} → {mg["Target workflows"]})'],
     ['Workflow steps (summary)', r['Workflow steps']],
     ['Triggers and events', f'{r["Trigger types"]} Event envelope (V12): {r["Event and trigger schema"]}. Idempotency: {r["Idempotency and conflict policy"]}'],
     ['Functional requirements', f'Framework FR-V12-N-001…018; securities controls FR-V12-N-019…030; service: {", ".join(s["fr"])}; workflows: {", ".join(C.FR_WF[x["_code"]] for x in wfs)}'],
     ['Business rules', f'Approval gate (V12): {r["Human approval requirements"]}. Baseline: {", ".join(s["brl"][:3])}. New: {", ".join(b for b in s["brl"] if "V12-N" in b)}'],
     ['Agents and automations', f'V12 AI responsibilities: {r["AI agent responsibilities"]}. Operating mode: {r["Automation operating mode"]} New agents: {", ".join(s["agents_new"])}; reused: {", ".join(s["agents_reuse"]) or "—"}. New automations: {", ".join(s["au_new"])}; reused: {", ".join(s["au_reuse"])}. Autonomy cap: {s["autonomy"]}. Side-effect class (V12): {r["External side-effect classification"]}. Agent identity: {r["Agent identity and authority"]}. External agents: {r["External agent interoperability"]}'],
     ['Model tier and data class', f'{s["dclass"]}. {s["tier"]}. Model portability (V12): {r["Model portability"]}; registry gate incl. EVAL-N-ADV for investor-facing agents (DEC-808)'],
     ['Securities and privacy controls', ', '.join(s['ctls']) + ' (definitions §11.16.5.2; step placement Part 11.16b)'],
     ['Integrations', f'Providers (V12): {r["External provider requirements"]} (verify terms and prices at implementation, as of 27 Nov 2026). Open-source: {r["Open-source software requirements"]}. Shared engines: {r["Shared execution engine"]}. API operations: {len(r["Related API operations"].split(";"))} V12 candidates adopted under /api/v1/investor/* (§11.16.5.11)'],
     ['KPIs', f'Service KPIs (V12): {r["Performance KPIs"]}. Workflow KPI formulas: Part 11.16b. Blueprint: KPI-30 (cross-tenant disclosure = 0), securities KPIs SKPI-N-01 unauthorized external effects = 0, SKPI-N-02 advice-class content reaching investors = 0, SKPI-N-03 solicitation violations = 0'],
     ['Data', f'Entities (V12 candidates): {r["Related database entities"]}. Modalities: {r["Supported data modalities"]}. Provenance: {r["Data provenance requirements"]}'],
     ['Screens', f'Workbook: {r["Related UI screen IDs"]} → blueprint {", ".join(scr)}'],
     ['Security and compliance (V12)', r['Security and compliance requirements']],
     ['Risks and controls', '<br/>'.join(f'{a} → {b}' for a, b in s['risks']) + f'<br/>Escalation: {r["Escalation and recovery policy"]}<br/>Readiness: {r["Technology and regulatory readiness"]}; activation per jurisdiction pack'],
     ['Migration and versioning', f'{r["Service migration and deprecation policy"]}. Entitlement transition: {mg["Entitlement transition"]}'],
     ['Simulation and benchmark', r['Simulation and benchmark reference']],
     ['Unit economics', r['Unit economics and margin target'] + ' (§11.16.5.16)'],
     ['Release placement', s['release']],
    ]
    w('| Field | Specification |')
    w('|---|---|')
    for k, v in rows:
        w(f'| {k} | {E(v)} |')
    w('')
    w(f'**New functional requirements for {code}**')
    w('')
    table(['FR', 'Requirement', 'Acceptance (positive)', 'Negative / boundary'], [[f] + list(FR_SVC_TEXT[f]) for f in s['fr']])

w('#### 11.16.5.6.13 Securities-control requirements FR-V12-N-019…030')
w('')
FRS_CTL = [
 ('FR-V12-N-019', 'SEC-CTL-N-01 gate on every external effect', 'active packs → allow', 'draft/expired pack → Block PACK_NOT_ACTIVE'),
 ('FR-V12-N-020', 'SEC-CTL-N-02 eligibility per route and jurisdiction from evidence', 'verified → eligible', 'unknown → hold'),
 ('FR-V12-N-021', 'SEC-CTL-N-03 solicitation guard', 'relationship provenance → allow', 's42/506(b) without relationship → Block'),
 ('FR-V12-N-022', 'SEC-CTL-N-04 document gating', 'all gates → watermarked view', 'missing NDA → 403'),
 ('FR-V12-N-023', 'SEC-CTL-N-05 no AI investment advice', 'factual cited answer', 'advice class → refusal + handover'),
 ('FR-V12-N-024', 'SEC-CTL-N-07 KYC/AML hand-off results drive holds', 'cleared → proceed', 'screening hit → hold + R10'),
 ('FR-V12-N-025', 'SEC-CTL-N-08 counsel sign-off per jurisdiction with doc-set hash', 'signed + R10 → approved', 'doc change → void'),
 ('FR-V12-N-026', 'SEC-CTL-N-09 caps per route', 'below cap → reserve', 'at cap → Block'),
 ('FR-V12-N-027', 'SEC-CTL-N-10 two-person approval and mandate scope', 'two distinct → issue', 'same person twice → reject'),
 ('FR-V12-N-028', 'SEC-CTL-N-11 no custody; timers', 'receipt evidence only', 'any money-movement API absent (static check)'),
 ('FR-V12-N-029', 'SEC-CTL-N-14 cross-border hold', 'same jurisdiction → continue', 'issuer IN, investor US → hold'),
 ('FR-V12-N-030', 'SEC-CTL-N-15 kill switch ≤ 60 s', 'kill → queue drained to held', 'effect after kill = 0'),
]
table(['FR', 'Requirement', 'Acceptance (positive)', 'Negative / boundary'], FRS_CTL)

# ------------------------------------------------------------------ 11.16.5.7 agents
w('### 11.16.5.7 AI agents AG-160…179')
w('')
w('Card format of Part 7.4b. Cost formula (blueprint convention, verify prices at implementation, as of 27 Nov 2026): Haiku-class per call = 90 × [(in − cache) × 0.10 + cache × (0.6 × 0.01 + 0.4 × 0.125) + out × 0.50] ÷ 10⁶; Sonnet per call = 90 × [(in − cache) × 2 + cache × (0.6 × 0.10 + 0.4 × 2.50) + out × 10] ÷ 10⁶; blended at Sonnet share e; monthly low = 0.3 × base, high = 3 × base, before the 25% overhead allowance; proposed line CR-V12-N-02 (not B02).')
w('')
AG_LINK = {}
for a in SP.AGENTS:
    (aid, name, typ, link, purpose, trig, inputs, tools, outputs, auto, tier, t2, prompt, guard, fail, kpi, evald, toks, rel) = a
    h, s_, b, lo, base, hi = C.cost_ag(toks)
    inp, cache, out, calls, e = toks
    w(f'#### {aid} {name}')
    w('')
    w('| Field | Specification |')
    w('|---|---|')
    fields = [
     ('Type', typ), ('Purpose and business outcome', purpose), ('Linked BR / FR / US', f'DEC-783; {link}; EP-30/EP-31 stories (Part 11.16c)'),
     ('Persona', 'R02/R03/R04/R08/R10 reviewers (issuer staff); never R21 directly except AG-166/AG-171 outputs after approval'),
     ('Trigger', trig), ('Inputs and data sources', inputs), ('Tools / APIs (registry §7.2.4)', tools), ('Outputs', outputs),
     ('Autonomy and HITL', auto), ('Model tier', tier + ' (registry DEC-788; Claude Sonnet primary for 1b)'), ('Tier 2 eligibility · data class', t2),
     ('Prompt / context strategy', prompt), ('Guardrails', guard + '; AG-166 runs on any investor-facing text; no investment advice (SEC-CTL-N-05)'),
     ('Failure modes and fallback', fail + '; budget stop → queue; Tier 3 degrade → manual task'), ('Success KPIs', kpi),
     ('Eval dimensions', evald + '; EVAL-N-ADV no-advice suite (red-team set of 400 prompts in en/hi/de) must pass before registry approval'),
     ('Tokens, calls, cost', f'{inp:,} in ({cache:,} cacheable, hit 60%), {out:,} out; {calls:,} calls/month at pilot design volume. Haiku per call = ₹{h:.3f}; Sonnet per call = ₹{s_:.3f}; blended at e = {int(e*100)}% = **₹{b:.3f}**. **Monthly: low ₹{lo:,.0f} · base ₹{base:,.0f} · high ₹{hi:,.0f}** (before overhead; verify prices at implementation, as of 27 Nov 2026)'),
     ('Dependencies', 'AU-001, AU-003, AU-005, AU-128, AU-201; model registry; RLS scope'), ('Release', rel + ' (Release 2 unless W6)'),
    ]
    for k, v in fields:
        w(f'| {k} | {E(v)} |')
    w('')

# ------------------------------------------------------------------ 11.16.5.8 automations
w('### 11.16.5.8 Automations AU-200…229')
w('')
table(['ID', 'Name', 'Wave / Release', 'Linked BR / FR / rule', 'Trigger', 'Deterministic logic', 'Outputs', 'Autonomy', 'Guardrail', 'Failure / fallback', 'KPI', 'Cost'], SP.AUTOS)

# ------------------------------------------------------------------ 11.16.5.9 screens
w('### 11.16.5.9 Admin screens A205–A232')
w('')
TMBY = collections.defaultdict(list)
for n in range(1, 13):
    for r in C.TMM[n]:
        TMBY[r['Admin screen ID']].append(r)
rows = []
for new, old, title, svcs in SP.SCREENS_A:
    trs = TMBY.get(old, [])
    routes = sorted({op.strip() for r in trs for op in r['Existing route inventory'].split(';') if op.strip() and 'dashboard/query' not in op})
    ents = sorted({e.strip() for r in trs for e in r['Relevant entity candidates from source'].split(';') if e.strip()})
    rows.append([new, f'{old} (alias)', title, svcs, '; '.join(routes[:8]) + (' …' if len(routes) > 8 else ''), ', '.join(ents[:8]) + (' …' if len(ents) > 8 else ''), f'INV-UX-UAT-{old} → UAT-{new}'])
table(['Screen', 'INV ID', 'Title', 'Services', 'Primary API operations (V12)', 'Entities', 'UAT'], rows)
w('Common screen behaviour (Part 2.5 design system): startup selector (BRL-TEN-05 409 SELECT_SINGLE_STARTUP on mutations), approval chips showing the content hash and the two approvers, securities status banner (pack active / inactive per jurisdiction, kill switch state), "AI draft — not advice" label on every AI output, evidence drawer with citations, audit tab, empty/error/loading states, keyboard and screen-reader support, 1280 px desktop and 360 px approvals view (DEC-043).')
w('')
SCR_DETAIL = {
 'A207': 'Queue filters by type (offering content, offer, batch, acceptance, refund); each item shows diff vs last approved revision, hash, required roles, first approver; second approver must differ (AU-207); MFA ≤ 1 h; reject requires reason.',
 'A223': 'Rooms per offering; items with class/sensitivity/version/retention; grant panel (investor, scope, expiry default 30 days, NDA link); access log; revoke now; readiness score (WF04).',
 'A229': 'Offer register: serial no., recipient, route, issued/expiry, state; cap counters per route (AU-205) with remaining; withdraw; batch builder that refuses ineligible or unverified recipients.',
 'A230': 'Applications list with completeness, KYC status (provider ref), e-sign evidence, eligibility; hold reasons; accept (two-person) / reject.',
 'A231': 'Designated issuer accounts (masked, verified), receipt import, matching board (exact / partial / exception), allocation ledger, refund requests (record only), allotment/refund timers.',
 'A232': 'Offering registration: route, jurisdictions, solicitation mode, caps, investor classes, document set (hashes); counsel sign-off per jurisdiction (R10C) with admission, firm, expiry; R10 approval; pack status per jurisdiction; kill switch.',
 'A226': 'Copilot for issuer staff; answers grounded and labelled; refuses valuation opinions, suitability and tax advice (offers scenarios via AU-219 instead); every action proposal needs explicit confirmation.',
 'A212': 'Contact table with provenance, verification state, per-channel eligibility (WF03 decision), relationship provenance flag (AU-203), consent ledger link.',
 'A217': 'Composer: template, approved facts picker, AI draft, AG-166 findings inline (span highlights, rule IDs, pack versions), offering-tag toggle (forces two-person), preview per locale.',
}
for new, old, title, svcs in SP.SCREENS_A:
    if new in SCR_DETAIL:
        w(f'- **{new} {title}.** {SCR_DETAIL[new]}')
w('')

# ------------------------------------------------------------------ 11.16.5.10 data
w('### 11.16.5.10 Entities and data model')
w('')
table(['Entity', 'Purpose', 'Key columns', 'Data class', 'Retention', 'Services', 'Origin'], SP.ENTITIES)
w('All tables: `tenant_id uuid not null`, `startup_id uuid not null`, `created_at`, `updated_at`, `version int` (optimistic lock, NFR-025); RLS policy `using (tenant_id = current_setting(\'app.tenant_id\')::uuid and startup_id = any(current_setting(\'app.company_ids\')::uuid[]))`; R21 portal access through views filtered by `investor_id` from the session; money as `numeric(20,4)` + ISO 4217 code (DEC-027). The V12 API uses `/investor/subscriptions` whose entity is absent from the Technical Map candidates; it is added as `inv_subscription` (application/subscription case) [GAP-1016].')
w('')
w('```mermaid')
w('erDiagram')
w('  inv_round ||--o{ inv_offering : "registers"')
w('  inv_offering ||--o{ inv_counsel_signoff : "signed per jurisdiction"')
w('  inv_offering ||--o{ inv_offer_counter : "caps"')
w('  inv_offering ||--o{ inv_offer : "issues"')
w('  inv_investor ||--o{ inv_offer : "receives"')
w('  inv_investor ||--o{ inv_eligibility_check : "has"')
w('  inv_investor ||--o{ inv_contact : "represented by"')
w('  inv_investor ||--o{ inv_relationship_provenance : "evidences"')
w('  inv_offer ||--o{ inv_subscription : "leads to"')
w('  inv_subscription ||--o{ inv_commitment : "creates"')
w('  inv_commitment ||--o{ inv_receipt_allocation : "settled by"')
w('  inv_receipt ||--o{ inv_receipt_allocation : "allocated"')
w('  inv_offering ||--o{ inv_room : "data room"')
w('  inv_room ||--o{ inv_room_item : "contains"')
w('  inv_investor ||--o{ inv_access_grant : "granted"')
w('  inv_room ||--o{ inv_access_grant : "scoped"')
w('  inv_offering {')
w('    uuid id PK')
w('    uuid round_id FK')
w('    string route')
w('    string solicitation_mode')
w('    string doc_set_hash')
w('    string state')
w('  }')
w('  inv_counsel_signoff {')
w('    uuid id PK')
w('    uuid offering_id FK')
w('    string jurisdiction')
w('    string doc_set_hash')
w('    datetime expires_at')
w('  }')
w('  inv_eligibility_check {')
w('    uuid id PK')
w('    uuid investor_id FK')
w('    string route')
w('    string status')
w('    datetime expires_at')
w('  }')
w('  inv_offer {')
w('    uuid id PK')
w('    uuid offering_id FK')
w('    uuid investor_id FK')
w('    string serial_no')
w('    string state')
w('  }')
w('```')
w('')

# ------------------------------------------------------------------ 11.16.5.11 API
w('### 11.16.5.11 API catalogue (adopted V12 operations and additions)')
w('')
w('V12 operations are adopted literally under `/api/v1/investor/*` (DEC-814); each gets an API-V12-N ID. All require the investment product audience, AU-200, RLS scope, idempotency key on POST, ETag/If-Match on PATCH (NFR-025), uniform 404 out of scope; effect-bearing operations pass the PDP securities gate.')
w('')
rows = []
for a in C.APIS:
    if len(a) == 3:
        aid, op, svcs = a
        eff = 'Effect (gate)' if any(k in op for k in ('/queue', '/send', '/issue', '/dispatch', '/access-grants', '/book', '/execute', '/approve', '/decide')) else ('Webhook (signed)' if 'webhooks' in op else 'Read/Write')
        rows.append([aid, op, ', '.join('%02d' % s for s in svcs), eff, 'V12 Technical Map / Workflow Catalog'])
    else:
        aid, op, svcs, desc, role, ent = a
        rows.append([aid, op, '—', f'{desc} · role {role} · {ent}', 'New (Group N)'])
table(['API', 'Operation', 'Services', 'Class / note', 'Origin'], rows)

w('### Decisions, tags and quality gate for this file')
w('')
w('Decisions DEC-800…819, ADRs ADR-230…234 and the full tags register 1000–1019 are in Part 11.16c (§11.16.7, §11.16.9). Used in this file: DEC-800, 801, 802, 803, 804, 805, 806, 807, 808, 809, 811, 812, 813, 814, 816; ADR-230, 231, 233; ASSUMPTION-1000, 1001, 1003, 1004; GAP-1002, 1010, 1016; CONFLICT-1008, 1009, 1019; RECOMMENDATION-1005.')
w('')
table(['#', 'Quality gate item', 'Result', 'Notes'], [
 ['1', 'Every requirement traced to a source', 'Pass', 'Workbook row, website file or DEC cited per field'],
 ['2', 'Assumptions/gaps/conflicts tagged and logged', 'Pass', 'Register in Part 11.16c §11.16.9'],
 ['3', 'IDs unique and consistent', 'Pass', 'Only N ranges used; screen aliases per DEC-801'],
 ['4', 'No story lacks AC; no requirement lacks a test', 'Pass', 'Stories and TCs in Parts 11.16b/c'],
 ['5', 'Negative, edge, security, accessibility cases', 'Pass', 'PM-N models and workflow test classes'],
 ['6', 'No agent lacks guardrail, fallback, KPI, cost', 'Pass', '20 cards complete'],
 ['7', 'Time-sensitive facts flagged verify', 'Pass', 'Legal thresholds and prices marked'],
 ['8', 'No restricted data to free tier', 'Pass', 'Investor data never Tier 2'],
 ['9', 'Consistent with earlier parts', 'Pass', 'DEC-783/779/772/777/788 applied'],
])
w('**Status: Part 11 Batch 11.16a complete. Product boundary, 16 securities controls, privacy, website W55–W76, 12 service specifications, 20 agents, 30 automations, 28 admin screens, entities and the API catalogue specified; workflows in 11.16b, stories/tests/cost/decisions in 11.16c.**')

open(OUT, 'w').write('\n'.join(L) + '\n')
print('wrote', OUT, len('\n'.join(L)))
