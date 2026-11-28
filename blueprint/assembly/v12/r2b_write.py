"""R2/B part writer: assembles Part-11-2a/b/c from generated fragments and hand-written sections.
Usage: python3 -I r2b_write.py <blueprint_dir>   (run r2b_build.py first)"""
import sys, os, json, csv, collections, importlib.util
here = os.path.dirname(os.path.abspath(__file__)); OUT = sys.argv[1]
spec = importlib.util.spec_from_file_location('r2b_data', os.path.join(here, 'r2b_data.py'))
D = importlib.util.module_from_spec(spec); spec.loader.exec_module(D)
I = json.load(open(os.path.join(here, 'r2b_ids.json')))
WB = json.load(open(os.path.join(here, 'r2b_wb.json')))
FR, STORY, TC = I['FR'], I['STORY'], I['TC']; FRD = {f[0]: f for f in FR}
SC = {r['Automation ID']: r for r in WB['Service_Catalog']['rows']}; ENT = {r['Service ID']: r for r in WB['Entitlement_Rules']['rows']}
SIDS = sorted(SC)
cov = list(csv.reader(open(os.path.join(OUT, 'final/coverage_v12/B_coverage.csv'), encoding='utf-8')))[1:]
def esc(s): return str(s).replace('|', '/').replace('\n', '<br/>')
TITLE = '# AI Growth Engine: Employee Sales & Marketing Automation\n## Application Blueprint: PART 11 (Batch 11.2%s), V12 Master Automation Service Catalogue: 39 Services%s\n\n'
def header(l, sub):
    return (TITLE % (l, sub) + '| Item | Detail |\n|---|---|\n'
     '| Document | Part 11.2%s, V12 Master Automation Service Catalogue: 39 Services%s |\n| Version | 1.0 · 28 Nov 2026 |\n'
     '| Baseline | Parts 0–9.10 (DEC-001…422; AG-001…080; AU-001…119; WF-01…40; EP-01…21); BRD V12 ch. 08; FSD V12 ch. 08 and ch. 11; source workbook "Master Automation Service Catalog 2031: 39 Services 156 Workflows" (12 sheets) |\n'
     '| Roles applied | Chief Revenue Officer, Head of Marketing Automation, Principal Solutions Architect, Principal Business Systems Analyst, AI Product Lead; Product Owner, QA Lead, Security/AI Governance Lead and FinOps Lead as reviewers |\n'
     '| Group and ID ranges | R2, letter B: tags 778–795; DEC-520…539; ADR-185…189; FR-V12-B-###; BRL-V12-B-##; US-<EP>-YB<nn>; TC-V12-B-###; new epics EP-22…EP-29 |\n'
     '| Part map | **11.2a** material, coverage, register, catalogue reconciliation, framework, new epics, handoffs, costs, stories and tests · **11.2b** service specifications SM-SVC-01…20 · **11.2c** service specifications SM-SVC-21…39, conflicts, decisions, ADRs, persona review, tags, quality gate |\n\n'
     '**Acronyms.** SKU stock-keeping unit (one purchasable service) · PDP Policy Decision Point · WF workflow · AT acceptance test · ENT entitlement · ENG shared engine · DLT Distributed Ledger Technology registration platform for Indian commercial SMS/voice (TRAI) · NCPR National Customer Preference Register (DND, Do Not Disturb) · RCS Rich Communication Services · CPaaS communications platform as a service · ASR/TTS speech recognition/synthesis · MCP Model Context Protocol · A2A agent-to-agent protocol · RFQ request for quotation · PO purchase order · SLA service level agreement · SoD separation of duties · SWR screen workspace requirement · ACR/AUR agent / automation capability requirement.\n\n')

CB = collections.Counter(c[5] for c in cov); CA = collections.Counter(c[9] for c in cov)
byd = collections.defaultdict(collections.Counter); bya = collections.defaultdict(collections.Counter)
for c in cov: byd[(c[0], c[1])][c[5]] += 1; bya[(c[0], c[1])][c[9]] += 1
ST = ['Covered', 'Partially covered', 'Not covered', 'Conflict', 'Not applicable']

def gate(rows):
    s = '| # | Quality gate item | Result | Notes and fixes applied |\n|---|---|---|---|\n'
    for i, (a, b, c) in enumerate(rows): s += '| %d | %s | %s | %s |\n' % (i + 1, a, b, c)
    return s
GATE = [
 ('Every requirement traced to a source', 'Pass', 'Every service row cites BRD 08 §SM-SVC-xx, FSD 11 §SM-SVC-xx and the workbook sheets; every new FR cites its service and V12 field; baseline links cite FR-, BRL-, DEC-, KPI-, AG-, AU- IDs verified by grep against Parts 0–9.10'),
 ('Assumptions, gaps, conflicts tagged and logged', 'Pass', 'Tags 778–795 only; register in §11.2.9 (Part 11.2c)'),
 ('IDs unique and consistent with earlier parts', 'Pass', 'Generator asserts unique aspect IDs; FR-V12-B-001…105, TC-V12-B-001…264, US-xx-YBnn, BRL-V12-B-01…24, EP-22…29 are new; all 167 workbook API operations and 89 tables were found in Part 3 before reuse'),
 ('No story lacks AC and no requirement lacks a test', 'Pass', 'Each of the 78 stories has Gherkin with a positive and a negative scenario; each of the 105 FRs has a positive and a negative test; each SKU has an entitlement test'),
 ('Negative, edge, security and accessibility cases covered', 'Pass', '105 negative/boundary tests, 39 entitlement-isolation tests, cross-tenant, Tier 2 refusal and DEC-002 negative tests, 12 WCAG 2.2 AA tests for new workspaces'),
 ('No agent lacks guardrail, fallback, KPI and cost estimate', 'N/A (handoff)', 'No new AG card is issued here (IDs belong to Groups F and M); ACR-B-01…08 and AUR-B-01…07 state guardrail, fallback, KPI and cost basis for the receiving group'),
 ('Time-sensitive facts flagged verify with as-of date', 'Pass', 'Provider APIs, telecom rules (TRAI TCCCPR/DLT), marketplace APIs, agent protocols and model prices carry "verify at time of implementation (as of 27 Nov 2026)"; workbook rates labelled illustrative'),
 ('No restricted data routed to free-tier models', 'Pass', 'Every service states its data class; Tier 2 only for Public/Internal non-personal research and content (opt-in, default off); voice, SMS, support, procurement, payments, commerce: no Tier 2; TC for refusal'),
 ('Consistent with earlier parts', 'Pass with conflicts raised', 'Safety invariants unchanged; deviations raised as CONFLICT-778…783 with DEC-520…538; Founder-pending items listed; no earlier file edited'),
]

# ============ PART A ============
A = [header('a', ' (a: framework, reconciliation, epics, stories, tests)')]
A.append('''## 11.2.1 Material reviewed

| File | Size | Sections / rows | Purpose | Pattern | Aspects |
|---|---|---|---|---|---|
| BRD V12 `08_Master_Automation_Service_Catalogue_39.txt` | 2,228 lines · 115,756 bytes | V8 foundation register (25), V5 first-value register (39), packaging table (6 bundles + 6 rules), 39 service field tables (14 fields each) | Business definition of the 39 SKUs | `[TABLE]` per service, layered V4/V5/V8 sections | %d |
| FSD V12 `08_SaaS_Catalogue_Service_Registry.txt` | 192 lines · 3,346 bytes | Foundation register (25), engine register (15), lifecycle register (4), public projection rule | Registry and lifecycle | Three tables + one rule | %d |
| FSD V12 `11_Master_Functional_Specification_39_Serv.txt` | 1,638 lines · 99,442 bytes | 39 service tables × 12 fields (business source, objective, I/O, mode, agents/engines, provider/approval, dependency/permission, UI/API/entities, domain artifact, meter/cost, quality/provenance, migration/readiness) | Functional specification per SKU | One table per SKU | %d |
| Workbook `…39_Services_156_Workflows(1)_csv/` (12 sheets) | 1,294,470 bytes | Service_Catalog 39 × 50 fields; Workflow_Catalog 156 × 50; Service_Index 39; Entitlement_Rules 39 × 15; Migration 39; Shared_Engines 15; Capability_Crosswalk 100; Technical_Map 178; Cost_Model 156 + 4 rates; Acceptance_Tests 195; Start_Here 13; Sources_Decisions 19 | Authoritative source of the catalogue | CSV export, multi-line cells | %d |

**Method.** Every line of the three chapters was read. Every row of the 12 workbook sheets was parsed by `assembly/v12/r2b_parse_services.py`; BRD 08 and FSD 11 tables by `r2b_parse_brd08.py`. A programmatic cross-check found **0 differences** between BRD 08, FSD 11 and the workbook for objective, KPIs, UI, API and entity fields (FSD 11 adds the domain artifact name; BRD 08 adds enhancement metrics and readiness). All **167 API operations** and **89 database tables** named in the workbook already exist in Part 3.2/3.3/3.5/3.6. The service catalogue spec and coverage register are generated by `r2b_build.py` from the parsed rows plus the curated mapping `r2b_data.py`, so no service, field or ID was skipped. Repeated boilerplate (12 constant Service_Catalog fields, the readiness sentence) is listed once.

**Out of scope for Group B (referenced only).** Workflow detail (Workflow_Catalog 156 × 50) belongs to Groups C/D (Part 11.3/11.4); FSD ch. 12 DTOs and ch. 26 field schemas belong to their groups (GAP-785); screen IDs A170–A259 belong to Group G (GAP-786); agent and automation IDs belong to Groups F and M (GAP-787).

''' % (sum(v for k, x in byd.items() if k[0] == 'BRD V12' for v in x.values()), sum(v for k, x in byd.items() if k == ('FSD V12', '08') for v in x.values()), sum(v for k, x in byd.items() if k == ('FSD V12', '11') for v in x.values()), sum(v for k, x in byd.items() if k[0] == 'Workbook' for v in x.values())))

A.append('## 11.2.2 Coverage summary\n\n| Source | Aspects | ' + ' | '.join(ST) + ' | Matched after | Pending Founder | N/A after |\n|---|---|' + '---|' * (len(ST) + 3) + '\n')
for k in sorted(byd):
    tot = sum(byd[k].values())
    A[-1] += '| %s %s | %d | %s | %d | %d | %d |\n' % (k[0], k[1], tot, ' | '.join(str(byd[k][s]) for s in ST), bya[k]['Matched'], bya[k]['Pending Founder decision'], sum(v for x, v in bya[k].items() if x.startswith('Not applicable')))
A[-1] += '| **Total** | **%d** | %s | **%d** | **%d** | **%d** |\n\n' % (len(cov), ' | '.join('**%d**' % CB[s] for s in ST), CA['Matched'], CA['Pending Founder decision'], sum(v for x, v in CA.items() if x.startswith('Not applicable')))
A[-1] += ('**Reading.** Before this part the blueprint covered the *capabilities* of SM-SVC-01…25 (modules M01–M66, screens A001–A113, X1/X2 agents) but had **no service-SKU construct**: no per-SKU entitlement, meter, bundle, first-value milestone, enhancement metric or migration rule (DEC-047 plans only). Of the 14 services new in V12, four were capability-covered by the advanced parts (SM-SVC-29, 30, 32, 36), five partly (27, 33, 34, 35, 37, 39), two not at all (31, 38) and two conflicted with decisions or invariants (26 voice, 28 agentic commerce); SM-SVC-19 conflicts on bid submission. '
             'After this part **%d of %d aspects (%.1f%%) are Matched**, **%d are Pending Founder decision** (CONFLICT-778, 779, 780, 781) and 1 is Not applicable (workflow detail owned by Groups C/D).\n\n') % (CA['Matched'], len(cov), 100.0 * CA['Matched'] / len(cov), CA['Pending Founder decision'])

# 11.2.3 register
A.append('## 11.2.3 Detailed register\n\nThe CSV `final/coverage_v12/B_coverage.csv` lists **all %d atomic aspects individually** (doc, chapter, section, aspect_id, summary, status before, blueprint location, action, new IDs, status after). The tables below give the per-service register at dimension level and list every conflict aspect individually.\n\n' % len(cov))
A[-1] += '### 11.2.3.1 Per-service register\n\n| SKU | Service | Status before | SKU commercial aspects (bundle, meter, cap, pricing, version, first value, metrics) | Functional aspects (objective, I/O, approvals, agents, KPIs) | UI / API / data | WF04 | Action and new IDs | Status after |\n|---|---|---|---|---|---|---|---|---|\n'
for s in SIDS:
    m = D.S[s]; n = int(s[-2:])
    func = 'Covered (modules %s)' % m['mod'] if n <= 25 and m['st'] != 'Conflict' else ('Conflict: %s' % {'SM-SVC-19': 'bid submission', 'SM-SVC-26': 'AI voice outreach', 'SM-SVC-28': 'autonomous transaction'}[s] if m['st'] == 'Conflict' else m['st'])
    ui = 'Covered (all screens, APIs, tables exist)' if n <= 25 else ('Partially: reuse candidates; %s' % (m['swr'].split(' ')[0] if m['swr'] else 'X1/X2 screens ' + m['scrp']))
    A[-1] += '| %s | %s | %s | Not covered / partially (DEC-047 plan entitlements only) | %s | %s | %s | Spec §11.2.5.%d; %s; %s | %s |\n' % (s, SC[s]['Automation service name'], m['st'], func, ui, esc(m['wf4']), n + 10, ', '.join(I['SVC_FR'].get(s, [])) or 'framework FRs', ', '.join(I['SVC_STORY'].get(s, [])) or 'EP-29 stories', 'Matched' if m['st'] != 'Conflict' else 'Matched; conflict items Pending Founder decision')
A[-1] += '\n### 11.2.3.2 Framework and catalogue-level aspects\n\n| Aspect group | Count | Status before | Blueprint location before | Action | New IDs | Status after |\n|---|---|---|---|---|---|---|\n'
for g, cnt, sb, loc, act, ids in [
 ('Foundation capabilities SM-01-01…SM-14-05 (BRD 08, FSD 08)', '25 + 25', 'Partially covered', 'Capabilities exist (AU-001, AU-042, M08, M58 …) without SM IDs', 'ID mapping table §11.2.4.2; non-removable, never priced', 'FR-V12-B-004; DEC-522'),
 ('First-value milestones', '39', 'Not covered', '—', 'Milestone per SKU', 'FR-V12-B-021'),
 ('Bundles and packaging rules', '6 + 6', 'Not covered (2 partially)', 'DEC-047 archetypes', 'Bundle registry; selection modes; quote-only', 'FR-V12-B-003/005/010; DEC-521'),
 ('Enhancement metrics', '156', 'Not covered', '—', 'Metric emitters per workflow', 'FR-V12-B-022'),
 ('Shared engines ENG-01…15', '15', 'Partially covered', 'Modules', 'Engine-to-module map §11.2.4.4', 'FR-V12-B-023; DEC-526'),
 ('Lifecycle register and public projection', '4 + 1', 'Not covered / partially', 'BRL-AUT-03; BRL-PUB-05', 'State machines; projection rule', 'FR-V12-B-001/002/024'),
 ('Capability crosswalk', '100', 'Partially covered', 'Capabilities in modules', 'Crosswalk table §11.2.4.3', 'FR-V12-B-011'),
 ('Technical map rows', '178', '162 covered, 14 not covered (TBD workspaces), 2 conflict (legacy publication)', 'Part 2.5 screens', 'Reuse confirmed; SWR-B-01…10; DEC-536', 'SWR-B-xx; DEC-536'),
 ('Cost model rows and rates', '156 + 4', 'Not covered; rates conflict with gateway pricing', 'Part 7.3', 'Illustrative roll-up; gateway actuals govern', 'FR-V12-B-029; ASSUMPTION-789'),
 ('Acceptance scenarios', '195', 'Not covered', '—', '39 ENT → TC; 156 WF ATs referenced (Groups C/D/J)', 'TC-V12-B-211…249'),
 ('Migration rows', '39', 'Not covered', '—', 'Migration rules; SVC-20 split', 'FR-V12-B-012; BRL-V12-B-05; DEC-524'),
 ('Start_Here scope metrics', '13', 'Not covered (2 partially)', 'Part 2.5', 'Reconciled §11.2.4.1; funding of the 14 new SKUs pending', 'DEC-520; DEC-535; CONFLICT-780'),
 ('Sources and decisions', '19', 'Partially covered', 'Part 0B', 'Recorded §11.2.4.6', 'DEC-520…538')]:
    A[-1] += '| %s | %s | %s | %s | %s | %s | %s |\n' % (g, cnt, sb, loc, act, ids, 'Pending Founder decision (funding only)' if 'Start_Here' in g else 'Matched')
A[-1] += '\n### 11.2.3.3 Conflict aspects (listed individually)\n\n| Aspect ID | Summary | Resolution | Status after |\n|---|---|---|---|\n'
for c in cov:
    if c[5] == 'Conflict': A[-1] += '| %s | %s | %s | %s |\n' % (c[3], esc(c[4][:160]), esc(c[8]), c[9])
A[-1] += '\n**Founder-pending aspects that were not conflicts before** (funding/scope): %s.\n\n' % ', '.join(c[3] for c in cov if c[9].startswith('Pending') and c[5] != 'Conflict')

# 11.2.4 catalogue reconciliation
A.append('## 11.2.4 Catalogue reconciliation\n\n### 11.2.4.1 Counts\n\n| Item | V12 source | Blueprint before | Blueprint after (this part) | Check |\n|---|---|---|---|---|\n'
 '| Purchasable services (SKUs) | 39 (25 retained + 14 new; Start_Here) | 0 SKUs; 66 modules; DEC-047 plans | 39 SKUs in the service registry (FR-V12-B-001) | 39 rows in every sheet ✔ |\n'
 '| Workflows | 156 (4 per SKU; WF01–03 retained, WF04 new for 01–25) | WF-01…40 (process flows) | 156 workflow IDs referenced per SKU; detail Groups C/D | 156 ✔ |\n'
 '| Bundles | 6 (6 + 7 + 9 + 6 + 8 + 3 = 39 SKUs; 24 + 28 + 36 + 24 + 32 + 12 = 156 flows) | none | Bundle registry (FR-V12-B-003) | sums ✔ |\n'
 '| Foundations | 25 included, never priced | capabilities without SM IDs | Mapped §11.2.4.2 | 25 ✔ |\n'
 '| Legacy capabilities | 100 (25 foundation + 75 selectable) | — | Crosswalk §11.2.4.3 | 100 ✔ |\n'
 '| Shared engines | 15 | — | Engine map §11.2.4.4 | 15 ✔ |\n'
 '| Catalogue fields | 50 (30 original + 20 new) | — | All 50 fields carried into each service spec (11.2b/c) | 50 ✔ |\n'
 '| Acceptance scenarios | 195 (156 workflow + 39 entitlement), all Not run | — | 39 ENT → TC-V12-B-211…249; WF ATs referenced | 195 ✔ |\n'
 '| Admin screens | 34 Website / 113 Admin (existing route counts) | 147 + 71 screens | 0 new IDs here; 12 workspace requirements to Group G | ✔ |\n'
 '| API operations referenced | 167 distinct | 579 operations | 0 new endpoints; specialized contracts TBD for SVC-26…39 (Group H) | 167/167 present ✔ |\n'
 '| Database tables referenced | 89 distinct | catalogue in Part 3.3/3.6 | domain artifacts named; new entities to Group I | 89/89 present ✔ |\n'
 '| Illustrative AI cost at pilot caps (all 39 SKUs) | Cost_Model × Entitlement caps | — | ≈ ₹6,748 per tenant-month (₹4,964 for SVC-01…25, ₹1,784 for SVC-26…39), illustrative only | formula Σ cap × mean(WF ₹) |\n\n')
SVCX = ''
A[-1] += '### 11.2.4.2 Service index and blueprint home\n\n| SKU | Service | Family | Bundle | Meter | Pilot cap (not approved) | Version | V12 decision | Epic | Status before → after |\n|---|---|---|---|---|---|---|---|---|---|\n'
MIG = {r['Service ID']: r for r in WB['Migration']['rows']}
for s in SIDS:
    A[-1] += '| %s | %s | %s | %s | %s | %s | %s | %s | %s | %s → %s |\n' % (s, SC[s]['Automation service name'], SC[s]['Automation family'], ENT[s]['Partial bundle'], ENT[s]['Meter unit'], ENT[s]['Proposed pilot cap'], SC[s]['Service version'], MIG[s]['Decision'], D.S[s]['ep'], D.S[s]['st'], 'Matched' if D.S[s]['st'] != 'Conflict' else 'Matched / Pending Founder')
A[-1] += '\n**Foundation mapping (SM-xx-yy → blueprint).** SM-01-01 Business analysis → AG-030, EP-20 · SM-01-02 Template recommendation → FR-A100 · SM-01-03 Configuration generation → AG-030, FR-A100 · SM-01-04 Workspace readiness → FR-A099 · SM-01-05 Activation review → FR-A099/A101 · SM-11-01 Trial provisioning → EP-20 trial (DEC-047) · SM-11-02 Subscription monitoring → FR-A101 · SM-11-03 Usage metering → AU-042, API-529 · SM-11-04 Entitlement enforcement → AU-042, BRL-SVC-03, ENT-181 · SM-11-05 Offboarding → WF-14, FR-A103 · SM-12-01 Model routing → AU-001, M08 · SM-12-02 Token optimization → AU-068 · SM-12-03 Knowledge refresh → AU-069, AG-055 · SM-12-04 Output validation → AU-003 · SM-12-05 Quality evaluation → AG-002, AU-006, M54 · SM-13-01 Failure detection → M58, AU-010 · SM-13-02 Eligible retry → BRL-AUT-07 · SM-13-03 Approved fallback → AU-010, gateway Tier 3 · SM-13-04 Reconciliation → AU-026 · SM-13-05 Incident escalation → AG-028, M58 · SM-14-01 KPI measurement → M30, M52, KPI-01…31 · SM-14-02 Bottleneck identification → AU-088, AG-054 · SM-14-03 Recommendations → AG-043, Part 8.3 · SM-14-04 Controlled simulation → BRL-AUT-04, FR-A102 · SM-14-05 Improvement verification → OKPI-01…35.\n\n'
A[-1] += '### 11.2.4.3 Capability crosswalk (100 legacy IDs)\n\n| Family | Capability IDs | Primary service | Related services / foundation role | Classification |\n|---|---|---|---|---|\n'
fam = collections.OrderedDict()
for r in WB['Capability_Crosswalk']['rows']:
    fam.setdefault((r['Original family'], r['Commercial classification']), []).append(r)
for (f, cl), rows in fam.items():
    prim = collections.Counter(r['Primary service ID'] for r in rows)
    A[-1] += '| %s | %s | %s | %s | %s |\n' % (f, ', '.join('%s %s' % (r['Original capability ID'], r['Original capability name']) for r in rows), ', '.join('%s (×%d)' % kv for kv in prim.items()), esc(rows[0]['Potential related service IDs / foundation role']), cl)
A[-1] += '\nRule: original IDs and names are preserved; selectable families may share internals without a duplicate purchase charge; foundation entries are never sold (FR-V12-B-011, FR-V12-B-004).\n\n'
A[-1] += '### 11.2.4.4 Shared engines to blueprint modules\n\n| Engine | Logical engine | Services | Blueprint modules / automations | Commercial treatment |\n|---|---|---|---|---|\n'
EMAP = {'ENG-01': 'M10–M12, M59', 'ENG-02': 'M18, M19; AU-018', 'ENG-03': 'M03, M08 (RAG); AG-055', 'ENG-04': 'New in EP-22/EP-28 behind M08 gateway', 'ENG-05': 'M25–M28, M31, M35, M41; new SMS/RCS adapter (EP-23)', 'ENG-06': 'M29, M40', 'ENG-07': 'M01 identity + mandate register (EP-24)', 'ENG-08': 'M34, M43, M46; WeasyPrint (ADR-032)', 'ENG-09': 'M44, M52, M60', 'ENG-10': 'M47; AU-037, AU-040', 'ENG-11': 'M17; AU-056, AU-059', 'ENG-12': 'AU-065, AU-098; A125', 'ENG-13': 'M55; Celery/Beat', 'ENG-14': 'M24 PDP, M06 audit, M57 compliance', 'ENG-15': 'Part 8.3 optimization; AU-068'}
for r in WB['Shared_Engines']['rows']:
    A[-1] += '| %s | %s | %s | %s | Not billed; tenant/startup data private |\n' % (r['Engine ID'], r['Logical engine'], r['Primary mapped services'], EMAP[r['Engine ID']])
A[-1] += '\n### 11.2.4.5 Technical map reconciliation\n\n178 rows: **117** "existing catalog mapping — candidate reuse" (services 01–25; reuse confirmed, every screen exists in Part 2.5), **45** "candidate reuse only" (services 26–39; existing screens reused as tabs or references), **14** "TBD — design gap" specialized workspaces (one per new service; resolved as SWR-B-01…10 handoffs or mapped to existing X1/X2 screens for SM-SVC-29, 30, 32, 36), **2** "legacy publication route" rows (SM-SVC-15 A107/A108) resolved by DEC-536: client content is published only to a separate verified client-controlled property, never the SaaS storefront. Existing UI UAT references are related references only, not proof (all Not run).\n\n'
A[-1] += '### 11.2.4.6 Source decisions carried from the workbook\n\n| Source / decision | Constraint carried into the blueprint | Where |\n|---|---|---|\n'
for r in WB['Sources_Decisions']['rows']:
    A[-1] += '| %s | %s | DEC-520…538; §11.2.5 |\n' % (esc(r['Source / decision']), esc(r['Interpretation and constraint']))

# 11.2.5 framework
A.append('''## 11.2.5 Enhancements

### 11.2.5.1 Service catalogue framework (applies to all 39 SKUs)

The catalogue turns the blueprint's capability modules into **39 independently purchasable services**. A service is a commercial wrapper (entitlement, meter, bundle, KPI, readiness, migration) over existing modules, agents and automations, plus new capability where V12 adds it. It does not create a second execution engine: every workflow still runs on the M55 workflow engine, through the model gateway and the transactional outbox, and every external effect is rechecked by the PDP.

```mermaid
flowchart TD
  F["25 foundation capabilities<br/>included, never priced"]
  R["Service registry<br/>39 SKUs SM-SVC-01 to 39"]
  B1["Research and Lead Intelligence<br/>6 SKUs, 24 flows"]
  B2["Outreach and Conversations<br/>7 SKUs, 28 flows"]
  B3["Digital Marketing and Acquisition<br/>9 SKUs, 36 flows"]
  B4["Sales Conversion and Operations<br/>6 SKUs, 24 flows"]
  B5["Lifecycle and Business Intelligence<br/>8 SKUs, 32 flows"]
  B6["Commerce and Procurement<br/>3 SKUs, 12 flows"]
  W["156 workflows SM-SVC-nn-WF1 to WF4<br/>M55 engine, pinned revision"]
  E["15 shared engines ENG-01 to 15<br/>not billed"]
  P["Policy Decision Point<br/>scope, SKU entitlement, consent, budget, approval hash"]
  O["Transactional outbox and adapters"]
  F --> R
  R --> B1
  R --> B2
  R --> B3
  R --> B4
  R --> B5
  R --> B6
  B1 --> W
  B2 --> W
  B3 --> W
  B4 --> W
  B5 --> W
  B6 --> W
  W --> E
  W --> P
  P --> O
```

**Per-action entitlement check (FR-V12-B-006).** The PDP gains one input, the SKU entitlement, evaluated before the existing scope, consent, jurisdiction, budget and approval-hash checks. It fails closed.

```mermaid
sequenceDiagram
  participant U as User or trigger
  participant WF as Workflow step (M55)
  participant PDP as Policy Decision Point
  participant EN as Entitlement service
  participant GW as Model gateway
  participant OB as Outbox and adapter
  U->>WF: event envelope with service_id and workflow_revision
  WF->>PDP: decide(action, scope, service_id)
  PDP->>EN: active SKU grant for tenant and startup
  EN-->>PDP: grant revision, meter, remaining cap
  PDP->>PDP: scope, consent, jurisdiction, budget, approval hash
  alt allowed
    PDP-->>WF: allow with decision id
    WF->>GW: model call with budget reservation
    WF->>OB: external effect with idempotency key
    OB->>PDP: recheck at dispatch
  else denied
    PDP-->>WF: deny ENTITLEMENT_MISSING or other reason
    WF->>WF: draft-only, task-only or hold
  end
```

**SKU lifecycle (FR-V12-B-001).**

```mermaid
stateDiagram-v2
  [*] --> Draft
  Draft --> Reviewed : product, legal, provider, technical review
  Reviewed --> Pilot : scope, permission, pricing, benchmark, SLA, acceptance sign-off
  Pilot --> Released : pilot acceptance and owner approval
  Released --> Restricted : risk, provider or legal issue
  Restricted --> Released : issue closed
  Released --> Deprecated : approved migration with entitlement mapping
  Restricted --> Deprecated : approved migration
  Deprecated --> [*]
```

**Procurement split (SM-SVC-20 → SM-SVC-39, FR-V12-B-012, BRL-V12-B-05).**

```mermaid
stateDiagram-v2
  [*] --> LegacyCombined
  LegacyCombined --> TransitionProposed : SM-SVC-39 approved
  TransitionProposed --> SubscriberNotified : entitlement mapping prepared
  SubscriberNotified --> Split : approved transition date
  Split --> [*]
  LegacyCombined --> LegacyCombined : buy-side orders honoured
```

**Side-effect class to autonomy cap (FR-V12-B-020; DEC-064 unchanged).**

| V12 side-effect class | Services (workbook, service level) | Autonomy cap | PDP behaviour |
|---|---|---|---|
| Internal analysis/draft; no external action without separate authorization | 35 services | Up to L3 for internal analysis; any external use follows the class of that use | No external adapter call |
| Potential external write/communication; controlled only after permission and policy approval | SM-SVC-06, 10, 12 (and WF01–02 of SM-SVC-28) | L1 approval of content/campaign (hash), then L2 dispatch; approved FAQ replies and reminders up to L3 | Recheck consent, suppression, quiet hours, caps, approval hash at dispatch |
| Consequential financial/legal or authority-bearing action; prepare only until authorized | SM-SVC-28 (WF04) | **L1 maximum**: human approval per transaction on the exact payload | Mandate check + approval hash + provider reconciliation; money movement never initiated by AI |

''')
A[-1] += '### 11.2.5.2 Framework functional requirements (FR-V12-B-001…030)\n\n| FR | Requirement | Acceptance (positive) | Negative / boundary | Epic | Tests |\n|---|---|---|---|---|---|\n'
FR_TC = collections.defaultdict(list)
for x in TC: FR_TC[x[2]].append(x[0])
for f in FR:
    if f[1] == 'COMMON': A[-1] += '| %s | %s | %s | %s | EP-29 | %s |\n' % (f[0], esc(f[2]), esc(f[3]), esc(f[4]), ', '.join(FR_TC[f[0]][:4]) + (' …' if len(FR_TC[f[0]]) > 4 else ''))
A[-1] += '\n### 11.2.5.3 Business rules introduced (BRL-V12-B-01…24)\n\n| Rule | Statement | Services | Enforcement |\n|---|---|---|---|\n'
for b in D.BRL:
    A[-1] += '| %s | %s | %s | PDP / service validation; audited; tested by the service FR tests |\n' % b
A[-1] += '\n### 11.2.5.4 New epics EP-22…EP-29\n\nThese epics give a home to the V12 services that no existing epic (EP-01…21) can hold. Retained services stay in their existing epics and add stories (US-<EP>-YBnn).\n\n| Epic | Title | Services | Scope | FRs | Stories | Release | Dependencies | Definition of done |\n|---|---|---|---|---|---|---|---|---|\n'
for e in D.NEW_EPICS:
    frs = [f[0] for f in FR if (f[1] == 'COMMON' and e[0] == 'EP-29') or (f[1] != 'COMMON' and D.S[f[1]]['ep'].split(',')[0].strip() == e[0])]
    sts = [s[0] for s in STORY if s[1] == e[0]]
    A[-1] += '| %s | %s | %s | %s | %s | %s | %s | EP-29 registry and entitlement; EP-03 consent/PDP; EP-04 gateway; EP-18 workflow engine | All FRs tested; ENT test passed; WCAG 2.2 AA for its workspace; provider procurement gate PG-01…10 passed; activation approval recorded |\n' % (e[0], e[1], e[2], e[3], (frs[0] + '…' + frs[-1]) if frs else '—', ', '.join(sts), e[4])
A[-1] += '\n**Unused range.** EP-30 is not needed and stays reserved.\n\n'
# handoffs
A[-1] += '### 11.2.5.5 Screen workspace requirements (handoff to Group G)\n\nScreen IDs A170–A259 belong to Group G. This part states *what* each workspace must do; Group G assigns IDs, layouts and field lists (GAP-786).\n\n| SWR | Workspace | Service | Required content | Reuse / extend | Accessibility |\n|---|---|---|---|---|---|\n'
for sw in D.SWR:
    A[-1] += '| %s | %s | %s | %s | %s | WCAG 2.2 AA; keyboard; status messages; test %s |\n' % (sw[0], sw[1], sw[2], sw[3], 'extends existing screen' if 'extends' in sw[1] else 'new route', [x[0] for x in TC if x[1].endswith(sw[1])][0] if [x for x in TC if x[1].endswith(sw[1])] else '—')
A[-1] += '''
### 11.2.5.6 Agent and automation capability requirements (handoff to Groups F and M)

No AG or AU ID is issued here (ranges belong to Groups F and M, GAP-787). Each requirement states the guardrail, fallback, KPI and cost basis the receiving group must carry into its card.

| Requirement | Service | Capability | Autonomy / tier / data class | Guardrails | Fallback | KPI | Cost basis |
|---|---|---|---|---|---|---|---|
| ACR-B-01 Voice conversation agent | SM-SVC-26 | Speech intent, grounded answer from approved knowledge, disclosure, human handoff, verbal slot confirmation | L3 inbound answers only; outbound L1 per campaign; Tier 1a/1b; Personal, no Tier 2 | Disclosure first; no prices, commitments or payment capture; minors and patient topics blocked | Transfer to human; voicemail task | Disclosure 100%; unauthorized calls 0; routing accuracy | Gateway tokens + ASR/TTS per minute (quote) |
| ACR-B-02 Multimodal creative generator and checker | SM-SVC-27 | Image/video/audio variants from approved brief; claim, rights and brand checks | L3 drafts; publication L1; Internal; personal likeness Personal | Approved claims only; rights evidence; no real-person likeness without consent | Text-only draft; human designer task | Rights review 100% before publication | Provider per-asset fee (quote) + gateway review tokens |
| ACR-B-03 Agent-protocol counterpart verifier and quotation responder | SM-SVC-28 | Verify counterpart identity and grant; map requirement to approved offerings; ask deterministic quote engine | L1 for every quotation release; Confidential, no Tier 2 | No transaction authority; untrusted counterpart content; mandate cap enforced by AUR-B-03 | Human quote task | Unauthorized transactions 0; mandate validation 100% | Gateway tokens; protocol hosting |
| ACR-B-04 Marketplace listing mapper | SM-SVC-31 | Map approved catalogue fields to marketplace schemas; content validation | L1 publication; Confidential | Approved price version and claims only | Manual listing task | Listing field accuracy; duplicate publish 0 | Gateway tokens (Tier 1a) |
| ACR-B-05 Supplier quotation normalizer and comparator | SM-SVC-39 | Extract and normalize supplier quotes (unit, currency, terms, lead time) | L3 normalization; selection L1; Confidential | Unknown units held; no supplier selection by AI | Manual comparison sheet | Normalized quote accuracy; comparison completeness | Gateway tokens (extends AG-023 pattern) |
| ACR-B-06 Support case classifier and resolution drafter | SM-SVC-33 | Case classification, grounded resolution drafts, self-service suggestion | L2 within approved grants; refunds/credits L1; Personal | Grant list only; abstain when ungrounded | Human agent queue | Grounded response ≥95%; routing accuracy | Gateway tokens (extends AG-031) |
| ACR-B-07 Review classifier and response drafter | SM-SVC-35 | Classify review issues; draft respectful evidence-based responses | L1 responses; Personal | No fake reviews; no personal data disclosure | Human response task | Review provenance 100%; fake review generation 0 | Gateway tokens |
| ACR-B-08 Answer-engine visibility monitor | SM-SVC-13 | Summarize authorized AI-answer observations; recommend improvements | L3 internal; Public, Tier 2 eligible (opt-in) | Measured vs estimated labelled; no guarantees | Manual observation import | Query observation coverage; citation accuracy | Gateway tokens; observation source (quote) |
| AUR-B-01 SKU entitlement evaluator | All | Deterministic grant lookup per action (extends AU-042 and AU-009) | L3 deterministic | Fail closed; cached ≤60 s with revocation invalidation | Deny | Entitlement enforcement 100% | ₹0 incremental (PostgreSQL/Valkey) |
| AUR-B-02 Telecom eligibility gate | SM-SVC-26, 38 | DLT entity/header/template match, NCPR/DND scrub, quiet hours, frequency | L3 deterministic | Fail closed when registry evidence missing | Hold | Unauthorized calls/messages 0 | Scrub provider fee (quote) |
| AUR-B-03 Mandate verifier | SM-SVC-28 | Identity, scope, item and price limits, cap, expiry, approval hash on exact payload | L3 deterministic | Changed payload, expired or revoked mandate blocks effect | Deny and route to human | Verified mandate 100% | ₹0 incremental |
| AUR-B-04 Marketplace event dedupe and order-event ledger | SM-SVC-31 | Idempotent event ingestion; valid state transitions | L3 deterministic | Signature verification; replay protection | DLQ and reconciliation | Order-event dedup 100% | ₹0 incremental |
| AUR-B-05 Case SLA clock and breach escalation | SM-SVC-33 | SLA deadline, risk alert at 80%, breach escalation (extends AU-081 pattern) | L3 deterministic | Business calendar and timezone aware | Manual escalation | SLA coverage 100% | ₹0 incremental |
| AUR-B-06 Three-way match | SM-SVC-39 | PO vs goods receipt vs supplier invoice; tolerance rules (extends AU-037/AU-038) | L3 proposal; acceptance L1 | Buy-side SoD; no netting | Finance queue | Unmatched receipt escalated 100% | ₹0 incremental |
| AUR-B-07 Call-minute meter and recording-consent gate | SM-SVC-26 | Reserve minutes; block recording without consent evidence | L3 deterministic | Hard budget; consent required | Metadata-only log | Recording without consent 0 | ₹0 incremental |

'''
# costs
A[-1] += '''### 11.2.5.7 Cost of the enhancements (outside the approved budgets)

Nothing here changes DEC-230 (Ledger A), DEC-231/DEC-422 (Ledger B) or DEC-228 (staffing). The work is a **separately approvable proposal**: change request **CR-V12-B-01** (development, one-time) and **CR-V12-B-02** (running, recurring), placed in W6 / Phase 2 unless the Founder decides otherwise (DEC-535, CONFLICT-780). Rates: ₹4,545–6,818 per person-day (Part 8.4). Estimates are ranges with the basis shown [ASSUMPTION-791].

**Development (one-time), CR-V12-B-01**

| Item | Scope | Low pd | Likely pd | High pd | Basis |
|---|---|---|---|---|---|
| EP-29 catalogue framework | Registry, bundles, foundations, per-SKU entitlement in PDP, meters/caps, migration, public projection, first-value and 156 metric emitters | 20 | 30 | 42 | Extends ENT-181, AU-042, A101; 30 FRs |
| WF04 and SKU deltas, SM-SVC-01…25 | 25 services × 1.5 / 2.5 / 4 pd | 37.5 | 62.5 | 100 | 31 FRs; many reuse X1/X2 items |
| SKU wrappers over X1/X2 (SM-SVC-29, 30, 32, 36) | 4 × 2 / 3 / 5 pd | 8 | 12 | 20 | Assumes the X1/X2 capabilities are built under their own approvals |
| Tabs SM-SVC-34, 35, 37 | 3 × 6 / 9 / 13 pd | 18 | 27 | 39 | Extend A142, A145, A139 |
| EP-27 support operations (SM-SVC-33) | Cases, SLA, self-service grants, intelligence | 18 | 25 | 35 | 4 FRs, new workspace |
| EP-26 procurement (SM-SVC-39) | Supplier register, RFQ, PO, three-way match | 14 | 20 | 28 | Reuses Buy orders in A105 |
| EP-25 marketplace (SM-SVC-31) | One marketplace adapter, ledger, reconciliation | 20 | 28 | 40 | +8–12 pd per further marketplace |
| EP-23 SMS/RCS (SM-SVC-38) | Adapter, DLT gate, templates, fallback | 10 | 15 | 22 | Reuses M04/M24/M26 patterns |
| EP-28 creative production (SM-SVC-27) | Provider adapter, QA record, localization tracks | 18 | 26 | 38 | Reuses AU-076, AG-050 |
| EP-22 voice (SM-SVC-26) | Telephony adapter, ASR/TTS, disclosure, consent, meter | 30 | 42 | 60 | New real-time channel |
| EP-24 agentic commerce (SM-SVC-28) | Catalogue endpoint, counterpart verification, mandate register, approvals, logs | 28 | 40 | 58 | Protocol maturity risk |
| Acceptance (195 scenarios + 264 TC) | QA execution and evidence | 15 | 22 | 30 | QA 1.0 FTE rate |
| **Total** | | **236.5** | **349.5** | **512** | |
| **₹ (one-time)** | | **≈ ₹10.7 lakh** (236.5 × ₹4,545) | **≈ ₹19.9 lakh** (349.5 × ₹5,682 mid) | **≈ ₹34.9 lakh** (512 × ₹6,818) | Estimates; exclude legal counsel (GAP-174) |

**Running (recurring), CR-V12-B-02**

| Line | Driver | Estimate per month | Basis / status |
|---|---|---|---|
| Model gateway usage for SKU workflows (owner portfolio) | Σ pilot cap × mean workflow cost, all 39 SKUs | ≈ ₹6,748 per tenant at full pilot caps (₹4,964 for 01–25; ₹1,784 for 26–39) | Workbook illustrative rates (ASSUMPTION-789); for the owner portfolio it sits inside the DEC-008 AI ceilings (₹3,000 / ₹12,000 / ₹40,000) and the gateway hard caps; reconcile with actual Tier 1a/1b prices (verify, as of 27 Nov 2026) |
| SaaS tenant usage | Same formula per tenant | Customer-funded | Excluded from Ledger B (Part 8.4 convention); recovered through per-SKU metering |
| Telephony and ASR/TTS (SM-SVC-26) | Minutes × per-minute rate + number rental + DLT | Quote required | GAP-784; activation pending CONFLICT-779 |
| SMS/RCS (SM-SVC-38) | Messages × rate + DLT fees | Quote required | GAP-784 |
| Image/video/audio generation (SM-SVC-27) | Assets × per-asset rate | Quote required | GAP-784; paid by exception (PG-01…10) |
| Marketplace and agent-protocol connectors (SM-SVC-28, 31) | API fees, hosting | Quote required | GAP-784 |
| Storage for recordings and creative assets | GB-month on Supabase/S3 | Small; size after pilot | Retention per DEC-028 and BRL-V12-B-23 |

'''
# stories
A[-1] += '### 11.2.5.8 User stories (US-<EP>-YBnn) with acceptance criteria\n\nEvery story has a positive and a negative Gherkin scenario taken from the acceptance statements of its FRs. Priority: Must for framework and safety rules; Should for WF04 deltas and new services (W6).\n\n'
for s in STORY:
    sid = s[4]; frs = s[3]
    who = 'Service Owner' if sid == 'All' else 'tenant growth user of %s' % sid
    A[-1] += '#### %s %s\n\n| Field | Value |\n|---|---|\n| Epic | %s |\n| Story | As a %s, I want %s, so that the V12 service works within entitlement, approval and safety rules |\n| FRs | %s |\n| Priority / release | %s |\n| Tests | %s |\n\n```gherkin\nFeature: %s\n' % (s[0], esc(s[2]), s[1], who, esc(FRD[frs[0]][2][:160]).rstrip('.').lower() if len(frs) == 1 else 'the capabilities in ' + ', '.join(frs), ', '.join(frs), 'Must · EP-29 registry first' if sid == 'All' else ('Should · ' + D.S[sid]['wave'].split('.')[-1].strip() if D.S[sid]['wave'] else 'Should'), ', '.join(sum((FR_TC[f] for f in frs), [])), s[0])
    for f in frs:
        ff = FRD[f]
        A[-1] += '  Scenario: %s positive\n    Given the tenant holds an active entitlement for %s in the selected startup scope\n    And the required approvals, consent and budget reservation exist\n    When the behaviour of %s is executed\n    Then %s\n  Scenario: %s negative or boundary\n    Given the same tenant and scope\n    When the prohibited or boundary condition of %s occurs\n    Then %s\n' % (f, 'the SKU under test' if sid == 'All' else sid, f, ff[3].replace('\n', ' '), f, f, ff[4].replace('\n', ' '))
    A[-1] += '```\n\n'
# tests
A[-1] += '### 11.2.5.9 Test cases (TC-V12-B-001…%03d)\n\n| TC | Title | FR | Preconditions | Steps | Expected | Type | Level | Priority |\n|---|---|---|---|---|---|---|---|---|\n' % len(TC)
for x in TC: A[-1] += '| %s |\n' % ' | '.join(esc(v) for v in x)
A[-1] += '\n**Traceability.** Each SM-SVC-xx-ENT-AT01 maps to one TC (Security type); each workflow acceptance scenario SM-SVC-xx-WF0n-AT01 is referenced in its service specification and detailed by Groups C/D/J. All start "Not run" (FR-V12-B-025).\n\n'
A.append('### Quality gate (Part 11.2a)\n\n' + gate(GATE) + '\n**Status: Part 11 Batch 11.2a complete. Framework, reconciliation, eight new epics, %d stories and %d tests written; service specifications follow in 11.2b and 11.2c.**\n' % (len(STORY), len(TC)))

# ============ PART B ============
Bp = [header('b', ' (b: service specifications SM-SVC-01…20)'), '## 11.2.5 Enhancements (continued)\n\n### 11.2.5.10 How to read a service specification\n\nEach specification carries all 50 workbook fields, the BRD 08 and FSD 11 fields, and the blueprint mapping: epic and modules; baseline and new FRs; approval gate and rules; agents, automations and autonomy cap; model tier and data class; integrations and APIs; KPIs and the 4 × 2 enhancement metrics; data; screens; security, risks and controls; migration; release; stories and tests. Workflows are listed by ID only; their steps and DTOs are specified by Groups C (SM-SVC-01…20) and D (SM-SVC-21…39). Costs are illustrative workbook scenarios, not prices.\n\n', open(os.path.join(here, 'r2b_specs_b.md')).read(),
      '\n### Quality gate (Part 11.2b)\n\n' + gate(GATE) + '\n**Status: Part 11 Batch 11.2b complete. 20 service specifications (SM-SVC-01…20) written with blueprint mapping, new FRs and tests.**\n']

# ============ PART C ============
C = [header('c', ' (c: service specifications SM-SVC-21…39, conflicts, decisions)'), '## 11.2.5 Enhancements (continued)\n\n', open(os.path.join(here, 'r2b_specs_c.md')).read()]
C.append('''
### 11.2.5.50 Agentic commerce control flow (SM-SVC-28)

```mermaid
flowchart TD
  A["External agent request"]
  B{"Verified identity and scoped grant?"}
  C["Refuse and audit"]
  D["Match approved offerings<br/>deterministic quote engine"]
  E["Quotation draft"]
  F{"Human approves quotation hash?"}
  G["Return quotation to agent"]
  H["Counter-offer or purchase intent"]
  I{"Within mandate scope, cap, expiry?"}
  J["Reject, notify owner"]
  K["Approval request with comparison"]
  L{"Human approves exact payload?"}
  M["Execute via approved provider<br/>idempotency key"]
  N["Reconcile outcome"]
  A --> B
  B -- "no" --> C
  B -- "yes" --> D
  D --> E
  E --> F
  F -- "no" --> J
  F -- "yes" --> G
  G --> H
  H --> I
  I -- "no" --> J
  I -- "yes" --> K
  K --> L
  L -- "no" --> J
  L -- "yes" --> M
  M --> N
```

The mandate narrows what may be proposed; it never replaces the human approval of a transaction (BRL-V12-B-09). Payment is never initiated by the AI; WF04 executes an already-approved payload through the provider (DEC-022) and reconciles uncertain outcomes (AU-026).

### 11.2.5.51 Voice call gates (SM-SVC-26)

```mermaid
flowchart TD
  IN["Inbound call"]
  DS["AI disclosure played"]
  IQ{"Disclosure confirmed?"}
  HU["Transfer to human"]
  IC["Classify intent, answer from approved knowledge"]
  UN{"Uncertain, sensitive or human requested?"}
  BK["Verbal slot confirmation, book via calendar"]
  OUT["Outbound request"]
  EL{"Call permission or callback, DLT and NCPR scrub,<br/>quiet hours, caps, approved script hash?"}
  HD["Hold, no call"]
  CL["Place one call with disclosure"]
  RC{"Recording consent from all parties?"}
  MT["Metadata only"]
  TR["Transcribe, redact, summarize to Customer 360"]
  IN --> DS
  DS --> IQ
  IQ -- "no" --> HU
  IQ -- "yes" --> IC
  IC --> UN
  UN -- "yes" --> HU
  UN -- "no" --> BK
  OUT --> EL
  EL -- "no" --> HD
  EL -- "yes" --> CL
  CL --> RC
  BK --> RC
  RC -- "no" --> MT
  RC -- "yes" --> TR
```

## 11.2.6 Conflicts and proposed resolutions

| Tag | Conflict | V12 text | Blueprint / invariant | Proposed resolution | Status |
|---|---|---|---|---|---|
| [CONFLICT-778] | Agentic commerce could transact under a standing mandate | SM-SVC-28: "controlled autonomous for preapproved routine actions"; WF04 "Verify authorization; execute only via approved provider"; input "verified payment mandate"; BRD 01/20 "Real external actions require exact approval **or eligible bounded mandate**" | Safety invariant: AI never pays or transacts without a human; DEC-064 consequential actions L1, money movement unsupported; BRL-AI-07 | Keep the invariant: a mandate bounds negotiation; every transaction, order acceptance and payment instruction needs a human approval hash on the exact payload (L1); payment executed only by the approved provider after that approval; no autonomous mandate execution. SM-SVC-28 designed now, activation after Founder decision (DEC-532) | **Pending Founder decision** |
| [CONFLICT-779] | AI voice outbound calls and AI-conducted conversations | SM-SVC-26-WF02 "initiate authorized call"; WF04 transcription | DEC-387 voice deferred (Founder instruction 28 Nov 2026); DEC-392 calls human-dialled only, no auto-dialler, no recording; Part 4.1 TR-R1 no SMS/voice outreach W0–W5 | Catalogue SM-SVC-26 as a Future (W6+) SKU; inbound AI voice with disclosure first; outbound only to callback requests or recorded call permission after DLT/NCPR scrub and an approved script hash (L1 per campaign); recordings only with all-party consent; activation through the DEC-387 gates PG-01…10 (DEC-531) | **Pending Founder decision** |
| [CONFLICT-780] | Scope and funding of 14 new services and 39 WF04 deltas | Start_Here: 25 → 39 services, 75 → 156 workflows; "design target, not rollout commitment" | DEC-230/231/422 approved budgets; DEC-228 staffing; Release plan W0–W5 | Place all new services and WF04 deltas in W6/Phase 2 as CR-V12-B-01 (₹10.7–34.9 lakh one-time) and CR-V12-B-02 (running, mostly quote-dependent); the EP-29 registry may enter Release 2 hardening only if the Founder funds it (DEC-535) | **Pending Founder decision** |
| [CONFLICT-781] | Bid submission by the system | SM-SVC-19-WF03 "coordinate authorized submission"; gate "no automatic submission to restricted portal" (implies automatic submission elsewhere) | Invariant: AI never submits bids; BRL-BID-04 human submission; DEC-064 bid submission L1 | Keep human submission on every portal; the system prepares the package and records the receipt (BRL-V12-B-04, DEC-533) | **Pending Founder decision** |
| [CONFLICT-782] | Plan archetypes vs per-SKU subscriptions | Per-SKU full/partial/selective model; 6 bundles; per-SKU meters | DEC-047, DEC-210, DEC-326 plan archetypes and meter list | Adopt V12: entitlements are granted per SKU; plan archetypes become packaging presets over SKU grants; DEC-047 meters extended with the 39 SKU meter units (DEC-521) | Resolved (Customer V12) |
| [CONFLICT-783] | Recordings and transcripts | SM-SVC-10-WF04, SM-SVC-26-WF04, SM-SVC-36-WF03 use authorized recordings/transcripts | DEC-218: recordings and transcripts stay excluded | Adopt V12 with all-party consent evidence, redaction, retention and no Tier 2 (BRL-V12-B-23, DEC-529) | Resolved (Customer V12) |

**Not conflicts (checked).** SM-SVC-37 and SM-SVC-30 price experiments: V12 itself requires approval of pricing before any live change, so only human-approved price points are allocated (DEC-534; the invariant "AI never sets prices" holds). SM-SVC-21 "no autonomous money transfer", SM-SVC-14 "no autonomous uncapped spend", SM-SVC-34 "avoid automatic charges", SM-SVC-36 "no automated employment decisions" all match the invariants. Every service carries "no private fundraising", consistent with DEC-002; the website investor mode is handled by Group G.

## 11.2.7 Decisions

| DEC | Decision | Authority | Effect |
|---|---|---|---|
| DEC-520 | The 39-SKU Master Automation Service Catalogue (SM-SVC-01…39, 156 workflows SM-SVC-nn-WF1…4, 6 bundles) is canonical; V12 IDs are used as-is and mapped to blueprint modules and epics (§11.2.4.2) | Customer revision V12 (28 Nov 2026) | Service registry FR-V12-B-001…003 |
| DEC-521 | Commercial model per SKU (full / partial bundle / selective; monthly base + metered excess; annual option; quote-only until rate cards approved); plan archetypes of DEC-047/210/326 become packaging presets over SKU grants; SKU meter units added to the DEC-047 meter list | Customer revision V12 (28 Nov 2026) | Amends DEC-047, DEC-210, DEC-326; resolves CONFLICT-782 |
| DEC-522 | The 25 foundation capabilities are included in every subscription, never priced and not removable | Customer revision V12 (28 Nov 2026) | FR-V12-B-004 |
| DEC-523 | The PDP checks SKU entitlement on every action and fails closed; each SKU has an entitlement-isolation acceptance test | Customer revision V12 (28 Nov 2026) | FR-V12-B-006…008, 026; ADR-185 |
| DEC-524 | Migration: retained IDs, WF04 added; SM-SVC-20 procurement split to SM-SVC-39 with legacy rights honoured; new SKUs not activated or billed before owner approval | Customer revision V12 (28 Nov 2026) | FR-V12-B-012; BRL-V12-B-05, 20, 21 |
| DEC-525 | Meter units and pilot caps are illustrative and unapproved; all prices "Quotation pending"; the workbook cost model is an illustrative scenario reconciled against gateway actuals | Customer revision V12 (28 Nov 2026) | FR-V12-B-009, 010, 029 |
| DEC-526 | Shared engines ENG-01…15 are logical capabilities mapped to blueprint modules, never billed | Customer revision V12 (28 Nov 2026) | §11.2.4.4 |
| DEC-527 | Per-SKU KPIs, 156 enhancement metrics and first-value milestones are adopted as acceptance measures; outcomes are never guaranteed | Customer revision V12 (28 Nov 2026) | FR-V12-B-021, 022, 030 |
| DEC-528 | New epics EP-22…EP-29 are created for services without a blueprint home; EP-30 reserved | Customer revision V12 (28 Nov 2026) | §11.2.5.4 |
| DEC-529 | Recordings and transcripts may be processed only with all-party consent, redaction and retention controls; never Tier 2 | Customer revision V12 (28 Nov 2026) | Amends DEC-218; resolves CONFLICT-783 |
| DEC-530 | SM-SVC-38 SMS/RCS is a Future (W6+) SKU behind DLT/NCPR activation gates; the W0–W5 "no SMS/voice outreach" rule (TR-R1) is unchanged | Customer revision V12 (28 Nov 2026) | EP-23; AUR-B-02 |
| DEC-531 | SM-SVC-26 voice: catalogued now; inbound AI voice with disclosure first; outbound only under BRL-V12-B-07; activation through DEC-387 gates | Pending Founder decision | Would amend DEC-387 and DEC-392 if approved; CONFLICT-779 |
| DEC-532 | SM-SVC-28 agentic commerce: mandate bounds negotiation only; human approval per transaction; no AI-initiated payment | Pending Founder decision | Keeps the safety invariant; CONFLICT-778; ADR-186 |
| DEC-533 | SM-SVC-19 bid submission stays human on every portal | Pending Founder decision | CONFLICT-781; BRL-V12-B-04 |
| DEC-534 | Price and offer experiments (SM-SVC-30, 37) allocate only human-approved price points within approved bounds; AI never sets prices | Customer revision V12 (28 Nov 2026) | BRL-V12-B-11 |
| DEC-535 | New services and WF04 deltas are placed in W6 / Phase 2 and costed as CR-V12-B-01/02 outside the approved budgets | Pending Founder decision | CONFLICT-780; DEC-228/230/231/422 unchanged |
| DEC-536 | Public storefront is a neutral SaaS catalogue (projection rule); client content is published only on a separate verified client-controlled property; legacy publication route isolated | Customer revision V12 (28 Nov 2026) | FR-V12-B-024; SM-SVC-15 |
| DEC-537 | Screen workspace requirements SWR-B-01…12 go to Group G; agent and automation requirements ACR-B-01…08 and AUR-B-01…07 go to Groups F/M | Customer revision V12 (28 Nov 2026) | GAP-786, GAP-787 |
| DEC-538 | Side-effect class drives the autonomy cap per workflow; DEC-064 caps unchanged | Customer revision V12 (28 Nov 2026) | FR-V12-B-020 |

**DEC-539** is not used.

### 11.2.7.1 Architecture decision records

| ADR | Title | Decision | Alternatives rejected | Consequences |
|---|---|---|---|---|
| ADR-185 | SKU entitlement inside the PDP | Entitlement is one more fail-closed PDP input (AUR-B-01) backed by `saas_entitlement` rows per SKU with revision, meter and cap; cached ≤60 s, invalidated on revocation | Separate entitlement microservice (latency, second policy point); entitlement only at UI (bypassable) | One policy point; every denial audited with reason |
| ADR-186 | Mandate model for agentic commerce | Mandate = signed record (principal, counterpart identity, scope, limits, cap, expiry, approval hash); verifier AUR-B-03; transactions need a separate human approval of the exact payload | Mandate as standing authority (breaks invariant); no mandate (cannot bound negotiation) | Safe by construction; slower autonomous commerce by design |
| ADR-187 | Telecom channel adapters | Voice, SMS and RCS adapters behind the outbox share a telecom eligibility gate (AUR-B-02) and per-minute/per-message meters; feature-flagged per tenant and jurisdiction | Provider-specific logic in workflows | Activation needs DLT evidence; provider swap without workflow change |
| ADR-188 | Marketplace connector and order-event ledger | One adapter per marketplace normalizes events into an append-only order-event ledger with idempotency and settlement reconciliation | Direct writes into sales orders | Replays are harmless; reconciliation reproducible |

ADR-189 is not used.

## 11.2.8 Expert persona review

| Persona | Review focus | Findings | Changes made |
|---|---|---|---|
| Chief Revenue Officer | Can the catalogue be sold and does it protect revenue integrity? | 39 SKUs in 6 bundles are sellable only as quotes; selective purchase without forced upstream SKUs lowers entry price; revenue integrity depends on ledger-derived outcomes | Quote-only CTA, per-SKU meters, first-value milestones, outcome acceptance never guaranteed (FR-V12-B-010, 021, 030); legacy rights honoured (BRL-V12-B-21) |
| Head of Marketing Automation | Are channels compliant and non-duplicative? | SMS/RCS and voice add regulatory exposure (DLT/NCPR); cross-channel duplication risk grows with 5 communication SKUs | Telecom gate AUR-B-02; frequency caps across channels; SMS only when SM-SVC-38 active (SM-SVC-08 FR); W6 placement |
| Principal Solutions Architect | Does it fit the modular monolith and safety design? | No second engine needed; services are wrappers over M55, gateway and PDP; new real-time voice and agent protocols are the main architectural risks | ADR-185…188; entitlement inside PDP; adapters behind the outbox; external agents disabled by default |
| Principal Business Systems Analyst | Is every V12 field traceable and testable? | 3,457 aspects inventoried; 0 BRD/FSD/workbook inconsistencies; 167/167 APIs and 89/89 tables exist | Service specs carry all 50 fields; 105 FRs, 78 stories, 264 tests; coverage CSV with status before/after |
| AI Product Lead | Are AI responsibilities bounded and evaluable? | AI roles are mostly drafting/classification; two services (26, 28) push autonomy; multimodal generation adds rights risk | Autonomy caps by side-effect class; CONFLICT-778/779 raised; ACR handoffs carry guardrails, fallbacks and KPIs; Tier 2 refused for personal data |

**Inconsistencies observed in earlier parts (reported, not fixed).** (1) Part 4.1 TR-R1 and DEC-392 forbid AI voice/SMS outreach in W0–W5 while V12 lists SM-SVC-26/38 without a wave; handled by W6 placement and CONFLICT-779. (2) DEC-047 meter dimensions (workspaces, users, AI tasks, outbound messages, research fetches, storage GB) have no per-SKU meter; GAP-145 ("AI tasks" unit undefined) remains open and now affects SKU metering. (3) The workbook Cost_Model rates (₹0.20 / ₹0.80 per 1,000 tokens) do not match the Part 7.3 gateway price assumptions; treated as illustrative (ASSUMPTION-789).

## 11.2.9 Tags register

| Tag | Type | Statement | Owner | Resolution |
|---|---|---|---|---|
| CONFLICT-778 | Conflict | Agentic commerce mandate autonomy vs "AI never pays/transacts without a human" | Founder | DEC-532 (pending) |
| CONFLICT-779 | Conflict | AI voice outbound and recording vs DEC-387, DEC-392, TR-R1 | Founder | DEC-531 (pending) |
| CONFLICT-780 | Conflict | 14 new services and WF04 deltas vs approved budgets and staffing | Founder | DEC-535 (pending) |
| CONFLICT-781 | Conflict | Bid submission wording vs human submission invariant | Founder | DEC-533 (pending) |
| CONFLICT-782 | Conflict | Per-SKU model vs DEC-047/210/326 plans | Product Owner | DEC-521 (resolved) |
| CONFLICT-783 | Conflict | Recordings/transcripts vs DEC-218 | DPO / Legal | DEC-529 (resolved) |
| GAP-784 | Gap | Providers and prices for telephony, ASR/TTS, SMS/RCS, media generation, marketplaces and agent protocols not selected or quoted | Procurement (PG-01…10) | Quotes before activation |
| GAP-785 | Gap | FSD ch. 26 field schemas and ch. 12 DTOs for the 39 domain artifacts are owned by other groups | Groups C/D/I | Domain artifact names adopted |
| GAP-786 | Gap | Screen IDs for SWR-B-01…12 not allocated here | Group G | A170–A259 |
| GAP-787 | Gap | Agent and automation cards for ACR-B-01…08 and AUR-B-01…07 not issued here | Groups F/M | AG-100…139, AU-150…179 |
| GAP-788 | Gap | Rate cards, margin targets and unit economics per SKU are "TBD by owner" | Service Owner (GAP-176) | Before any SKU release |
| ASSUMPTION-789 | Assumption | Workbook cost rates are illustrative and used only for sizing | FinOps | Reconcile with gateway actuals |
| ASSUMPTION-790 | Assumption | Pilot caps are used as the sizing basis for running estimates, though unapproved | FinOps | Replace with approved caps |
| ASSUMPTION-791 | Assumption | Effort ranges assume X1/X2 capabilities are built under their own approvals and one marketplace adapter | Delivery lead | Re-estimate at Phase-2 planning |
| RECOMMENDATION-792 | Recommendation | Sequence: EP-29 registry → SKU wrappers 29/30/32/36 → 33, 39, 31 → 38 → 27 → 26 and 28 last | Product Owner | Phase-2 plan |
| RECOMMENDATION-793 | Recommendation | Engage counsel for telecom (TCCCPR), marketplace terms, agentic commerce and review-platform policies before activation | Legal | Extends GAP-660 |
| RECOMMENDATION-794 | Recommendation | Keep Starter/Growth/Scale as packaging presets to avoid re-pricing existing pilots | Service Owner | DEC-521 |
| RECOMMENDATION-795 | Recommendation | Apply BRL-ELG-13 (no minors) and BRL-ELG-14 / BRL-LCY-02 (no patient data) explicitly to SM-SVC-26, 27, 33, 34, 38 activation checklists | Compliance | Activation gate |

''')
C.append('## 11.2.10 Quality gate and status\n\n' + gate(GATE) + '\n**Status: Part 11 Batch 11.2 complete (11.2a, 11.2b, 11.2c). %d aspects inventoried; %d Matched, %d Pending Founder decision, 1 Not applicable. 39 service specifications, 105 FRs, 24 rules, 8 new epics, %d stories, %d tests, 19 decisions (DEC-520…538), 4 ADRs, 18 tags.**\n' % (len(cov), CA['Matched'], CA['Pending Founder decision'], len(STORY), len(TC)))

names = {'a': 'Part-11-2a_V12_Master_Automation_Service_Catalogue_39_Services.md', 'b': 'Part-11-2b_V12_Master_Automation_Service_Catalogue_39_Services.md', 'c': 'Part-11-2c_V12_Master_Automation_Service_Catalogue_39_Services.md'}
for k, parts in (('a', A), ('b', Bp), ('c', C)):
    open(os.path.join(OUT, names[k]), 'w', encoding='utf-8').write(''.join(parts))
    print(names[k], os.path.getsize(os.path.join(OUT, names[k])))
