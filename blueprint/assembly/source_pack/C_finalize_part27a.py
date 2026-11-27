"""Group C finalizer: adds global aspects of docs 06/17, writes final/coverage/C_coverage.csv and renders
Part-02-7a from the template C_part27a.tpl.md.
Usage: python3 -I C_finalize_part27a.py <blueprint_dir> <c_out_dir> <template>
"""
import csv, json, os, sys, collections
BP, OUT, TPL = sys.argv[1], sys.argv[2], sys.argv[3]
cov = json.load(open(os.path.join(OUT, 'c_cov_generated.json')))
frag = json.load(open(os.path.join(OUT, 'c_fragments.json')))
SUM = json.load(open(os.path.join(OUT, 'c_recon_summary.json')))
OPS = list(csv.DictReader(open(os.path.join(OUT, 'c_ops.csv'))))
TABS = list(csv.DictReader(open(os.path.join(OUT, 'c_tables.csv'))))

C, P, N, X, NA = 'Covered', 'Partially covered', 'Not covered', 'Conflict', 'Not applicable'
G06 = [
 ('Product purpose and operating boundary', 'Employee-operated commercial scope; no investor/fundraising capability; independent deployment', NA, 'Common core: see document 01/02 coverage (Part 1; DEC-002; FR-NEG-01)', 'None', ''),
 ('Initial startup configurations', 'Four startup profiles (AppNAI, MedMaarg, EduVerse, OrganicSpec) and routing of AI projects to AppNAI', NA, 'Common core: see document 01/02 coverage (Part 1; DEC-052)', 'None', ''),
 ('Technology and execution principles', 'Stack, open-source first, autonomy modes, recheck at execution, implementation validation', NA, 'Common core: see document 01/02 coverage (Part 3.1; DEC-064)', 'None', ''),
 ('Global filter hierarchy', 'Scope family: tenant → startup → business line → offering → opportunity type; aggregate read-only', C, 'Part 2.1 FR-FLT-01; DEC-002 ("issuer thesis" replaced); DEC-055', 'None', ''),
 ('Global filter hierarchy', 'Geography family (country, state, city, location, delivery geography, currency, language, timezone)', C, 'FR-FLT-02; DEC-002 ("investment geography" removed)', 'None', ''),
 ('Global filter hierarchy', 'Evidence family', C, 'FR-FLT-03', 'None', ''),
 ('Global filter hierarchy', 'Engagement family', C, 'FR-FLT-04', 'None', ''),
 ('Global filter hierarchy', 'Operations family', C, 'FR-FLT-05', 'None', ''),
 ('Global filter hierarchy', 'Marketing family', C, 'FR-FLT-06', 'None', ''),
 ('Global filter hierarchy', 'Commercial family', C, 'FR-FLT-07', 'None', ''),
 ('Global filter hierarchy', 'AppNAI family', C, 'FR-FLT-08', 'None', ''),
 ('Global filter hierarchy', 'MedMaarg family', C, 'FR-FLT-09', 'None', ''),
 ('Global filter hierarchy', 'EduVerse family', C, 'FR-FLT-10; DEC-030', 'None', ''),
 ('Global filter hierarchy', 'OrganicSpec family', C, 'FR-FLT-11', 'None', ''),
 ('Global filter hierarchy', 'Filter rules (OR/AND, Unknown ≠ 0, allowlists, reset, cancel, saved views, cursor, distinct KPIs, server recheck of export/bulk)', C, 'FR-FLT-RULES; FR-UIS-01', 'Per-screen family assignment added in 2.7b cards', 'ASSUMPTION-343'),
 ('Seven primary views', 'Overview view purpose', C, 'Part 2.5 §2.40.1', 'None', ''),
 ('Seven primary views', 'Discovery view purpose', C, 'Part 2.5 §2.40.1', 'None', ''),
 ('Seven primary views', 'Outreach & Marketing view purpose', C, 'Part 2.5 §2.40.1', 'None', ''),
 ('Seven primary views', 'Follow-ups view purpose', C, 'Part 2.5 §2.40.1', 'None', ''),
 ('Seven primary views', 'Objections view purpose', C, 'Part 2.5 §2.40.1', 'None', ''),
 ('Seven primary views', 'Closure view purpose', C, 'Part 2.5 §2.40.1', 'None', ''),
 ('Seven primary views', 'Automation view purpose (connected separate admin workspace)', C, 'Part 2.5 §2.40.1 (Automation: governance, administration, operations)', 'None', ''),
 ('Seven primary views', 'Persistent action centre, notifications, Copilot, saved views, budget, automation status, stop control; reusable drawers', C, 'Part 2.5 §2.41; DEC-035; DEC-036', 'None', ''),
 ('Interface implementation register', '138 proposed items; preserve source identities for engineering tracking', P, 'Part 2.5 §2.43 (IDs) — legacy numbers absent', 'Legacy crosswalk §2.7.4.1', 'FR-ENH-C-001; GAP-341'),
 ('Part A Website', 'Public pages use published snapshot only; portal requires external auth and object grant; internal filters excluded', C, 'CA-PUB; CA-PORTAL; NFR-020', 'None', ''),
 ('Part B Admin', 'All Part B items Admin-only; legacy identifiers in brackets do not denote extra screens', C, 'CA-ADMIN; §2.7.4.1', 'None', ''),
 ('Operating contract', '147 = 34 Website + 113 Admin; 138 retained + 9 new; templates not per-startup code', C, 'Part 2.5 §2.43 count check; DEC-033', 'None', ''),
 ('Operating contract', 'Surface table (Website public, Website portal, Admin, Internal/callback)', C, 'Part 3.2 §3.2.1.1; NFR-001', 'None', ''),
 ('Operating contract', 'Routing decision: retain legacy contracts; separate ingress allowlists; new endpoints in /api/v1/commercial/{public,portal,admin}', X, 'Part 3.2 §3.2.2 (FRD-named only retained)', 'Alias layer §2.7.5.3', 'CONFLICT-343; FR-ENH-C-003'),
 ('Operating contract', 'Legacy token routes under /public/ are restricted portal endpoints; deny-by-default website routes; CORS not authorization', P, 'Part 3.2 §3.2.1.12 (CORS, allowlist); token routes not mapped', 'Token-route classification', 'FR-ENH-C-013'),
 ('Operating contract', 'Verified domain → one tenant/startup; unknown host 404; immutable snapshot; expiring preview grants; atomic pointer; cache invalidation; scanned assets; no portal content in CDN', C, 'CA-PUB; NFR-020; NFR-021; FR-PUB-01', 'None', ''),
 ('Operating contract', 'Intake creates scoped event and outbox, not approval; workers recheck; synthetic tests', C, 'CA-INTAKE; CA-DISPATCH', 'None', ''),
 ('Replacement options', 'Integration/cost/workflow/approval/exception panels show adapter, licence status, free capacity, residual cost, limits, benchmark, fallback approval; no keys or budgets on public pages', P, 'Part 2.5 A008/A012 regions (partial)', 'AdapterCard spec', 'FR-ENH-C-009; RECOMMENDATION-343; GAP-344'),
 ('Replacement options', 'Verify role, inputs, loading/empty/validation/denied/retry/success per UI item; scoped operations; sandbox adapters', C, 'CA-ALL; Part 6.1', 'None', ''),
 ('Interface acceptance and mapping', 'Scoped role, validated input, safe states, keyboard and mobile, API contract and persistence mapping per interface', P, 'CA-ALL; Part 2.5 (persistence mapping per screen absent)', 'Per-screen tables mapping in 2.7b', 'FR-ENH-C-002'),
 ('Interface acceptance and mapping', 'Counts: 302 operations, 149 entities, 624 tests retained; 19 + 6 + 175 candidates', P, 'Part 3.2 GAP-103; Part 3.3 §3.3.3.4; Part 6.1 GAP-167', 'Screen-level operation and table maps (§2.7.4)', 'GAP-342'),
 ('Interface acceptance and mapping', 'Delivery evidence against build, environment, scope, reviewer; critical defects block activation; targets provisional', C, 'Part 6.1 EVR; Part 8.2', 'None', ''),
 ('Implementation controls', 'Shared implementation-controls preamble', NA, 'Common core: see document 01/02 coverage', 'None', ''),
 ('Global interaction contract', 'Filter hierarchy row (server returns allowed vocabulary)', C, 'FR-FLT-01; Part 3.2 §3.2.1.6', 'None', ''),
 ('Global interaction contract', 'Object scope row (no Admin panels in Website bundle)', C, 'NFR-001', 'None', ''),
 ('Global interaction contract', 'Mutations row (preview object, cost and approval; revision and idempotency key)', C, 'UX-07; CA-DISPATCH; NFR-015', 'None', ''),
 ('Global interaction contract', 'Access changes row (abort, clear cache and drafts on revoke)', C, 'FR-UIS-01; NFR-050', 'None', ''),
 ('Acceptance and evidence record', 'Five evidence fields (responsible/reviewer, artefact, decision, remediation, business acceptance)', C, 'Part 6.1 EVR', 'None', ''),
 ('Four-state UI matrix', 'Public Website row', C, 'CA-PUB', 'None', ''),
 ('Four-state UI matrix', 'External portal row', C, 'CA-PORTAL; Part 2.5 §2.47 expired grant', 'None', ''),
 ('Four-state UI matrix', 'Admin row', C, 'CA-ADMIN; DEC-055', 'None', ''),
 ('Four-state UI matrix', 'Workflow action row (preview count, blocked, max spend; queued/held/failed/uncertain)', C, 'UX-07; DEC-050; Part 2.5 §2.47', 'None', ''),
 ('Engineering mapping', 'Interface owner confirms exact method/path and entities; website calls no Admin API', P, 'Part 3.2 FR/screen column (DERIVED paths only)', 'Per-screen legacy op maps; Website allowlist', 'FR-ENH-C-003; FR-ENH-C-013'),
 ('Engineering mapping', 'Acceptance evidence: build digest, screenshots, network payload evidence, reviewer', P, 'Part 6.1 EVR (screenshots per role absent)', 'Evidence pack', 'FR-ENH-C-011; GAP-347'),
 ('Optimization: Performance', 'OPT-02-01 public assets (LCP/INP/CLS p75)', C, 'NFR-042; NFR-043; Part 2.5 §2.48', 'None', ''),
 ('Optimization: Performance', 'OPT-02-02 React rendering and filters (latest filter wins, no scope flash)', P, 'FR-UIS-01; NFR-044', 'Filter performance behaviours', 'FR-ENH-C-015; TC-ENH-C-017'),
 ('Optimization: Performance', 'OPT-02-03 payload and pagination; dashboard p95 ≤ 2 s / ≤ 2.5 s', P, 'NFR-039; Part 3.2 §3.2.1.6', 'Dashboard latency scenario', 'FR-ENH-C-017; GAP-346'),
 ('Optimization: Performance', 'OPT-02-04 read projections refresh ≤ 60 s', X, 'NFR-047 (≤ 15 min); NFR-008 (≤ 60 s 360)', 'Freshness tiers', 'CONFLICT-348; RECOMMENDATION-348'),
 ('Optimization: Performance', 'OPT-02-05 async acknowledgement p95 ≤ 2 s', C, 'NFR-040 (stricter ≤ 800 ms)', 'None', ''),
 ('Optimization: Performance', 'OPT-02-06 database and network profiling', C, 'Part 4.2 load tests LT-01…08', 'None', ''),
 ('Optimization: Performance', 'OPT-02-07 parallel and batch operations', C, 'Part 4.2 LT; Part 3.1 worker design', 'None', ''),
 ('Optimization: API & Integration', 'OPT-09-01 typed contracts', C, 'Part 3.2 §3.2.5; NFR-015', 'None', ''),
 ('Optimization: API & Integration', 'OPT-09-02 consolidation and batching', C, 'Part 3.2 §3.2.2 step 4', 'None', ''),
 ('Optimization: API & Integration', 'OPT-09-03 adapter reliability', C, 'Part 3.2 §3.2.7', 'None', ''),
 ('Optimization: API & Integration', 'OPT-09-04 webhook processing p95 ACK ≤ 2 s', C, 'NFR-051 (stricter); Part 3.2 §3.2.6', 'None', ''),
 ('Optimization: API & Integration', 'OPT-09-05 API cost metering', C, 'NFR-014; NFR-037', 'None', ''),
 ('Optimization: UI/UX', 'OPT-15-01 adaptive navigation', C, 'Part 2.1 §2.4.11; NFR-034; NFR-090', 'None', ''),
 ('Optimization: UI/UX', 'OPT-15-02 accessibility and response states', C, 'Part 2.5 §2.46, §2.47', 'None', ''),
 ('Optimization: UI/UX', 'OPT-15-03 external portal usability ("authorized investor/customer")', X, 'Part 2.5 portal; DEC-002', 'Wording fix', 'CONFLICT-340; TC-ENH-C-020'),
 ('Optimization: UI/UX', 'OPT-15-04 saved views and bulk actions', C, 'FR-FLT-RULES; UX-07; NFR-038', 'None', ''),
 ('Optimization Intelligence', 'OI contextual Admin panel; unassessed when no denominator; stale labels; no public access', N, '—', 'OI panel spec', 'FR-ENH-C-004; GAP-345'),
 ('Optimization Intelligence', 'Seven OI integration points (A089, A009, A012, A014, A084, A042, A082) with persistence sources', P, 'Part 3.2 operations (mapped in §2.7.4)', 'Operation maps; panel placement', 'FR-ENH-C-004'),
 ('Optimization Intelligence', 'Acceptance protocol (baseline, candidate, dataset, digest, cost, outcome, reviewer; missing = Pending)', P, 'Part 6.1 EVR', 'Included in FR-ENH-C-004/011', 'FR-ENH-C-011'),
 ('Acceptance procedures', 'Dashboard latency 50/250 staff, 100k/1m opportunities', P, 'NFR-039; NFR-044', 'LT-ENH-C-01', 'FR-ENH-C-017; CONFLICT-349'),
 ('Acceptance procedures', 'Independent products and frontends ("two products, four frontends")', X, 'DEC-009; DEC-058; NFR-001', 'Interpretation', 'CONFLICT-341'),
 ('Acceptance procedures', 'Catalog integrity (138 UI, 302 ops, 149 entities preserved; 147 reconcile)', P, 'Part 3.2 GAP-103; Part 3.3 GAP-112', 'This batch parser = integrity check for UI and screen-level ops/tables', 'GAP-342'),
 ('Acceptance procedures', 'UI component reuse', C, 'UX-09; Part 2.5 §2.45.2', 'None', ''),
 ('Acceptance procedures', 'Public/portal/Admin separation', C, 'NFR-001; CA-PUB; CA-PORTAL', 'None', ''),
 ('Acceptance procedures', 'Adaptive filters and saved views', C, 'FR-FLT-RULES; FR-UIS-01', 'None', ''),
 ('Acceptance procedures', 'Loading, empty and error states', C, 'Part 2.5 §2.47', 'None', ''),
 ('Final decision controls', 'Same seven procedures restated with owner and evidence rule', C, 'DEC-014 (duplicated procedures consolidated)', 'None', ''),
 ('Final decision controls', 'Boundary: two-tenant fixture, deny cross-scope, reject stale grants', C, 'Part 6.1 negative packs', 'None', ''),
 ('Current scope', 'Nine new interfaces table (W31–W34, A109–A113) purpose and acceptance', C, 'DEC-033; FR-W31…W34; FR-A109…A113', 'Investor wording handled by CONFLICT-340', 'CONFLICT-340'),
 ('Current scope', 'Release condition: no production approval implied', C, 'Part 8.2 go-live gates', 'None', ''),
]
G17 = [
 ('Purpose, startups, technology, views, filters', 'Shared with document 06 and 01/02', NA, 'Common core: see document 01/02 coverage and doc 06 rows', 'None', ''),
 ('Reusable shell', 'Header region (product, tenant, startup, role, scope, user, notification)', P, 'Part 2.5 §2.41 (role chip absent)', 'Role chip', 'FR-ENH-C-007'),
 ('Reusable shell', 'Navigation region (seven views, context-aware labels)', C, 'Part 2.5 §2.40, §2.41', 'None', ''),
 ('Reusable shell', 'Filter toolbar (clear/apply/save, result count, as_of)', P, 'Part 2.5 §2.41 (result count absent)', 'Result count', 'FR-ENH-C-008; GAP-348'),
 ('Reusable shell', 'KPI cards (distinct verified outcomes; forecast not as actual)', C, 'Part 2.5 DV-2; FR-FLT-RULES', 'None', ''),
 ('Reusable shell', 'Results (stable-cursor table or pipeline; confidence and status)', C, 'LP-LIST; LP-BOARD', 'None', ''),
 ('Reusable shell', 'Detail drawer (profile, chronology, evidence, actions, approval state)', C, 'LP-DETAIL; context panel', 'None', ''),
 ('Reusable shell', 'Action centre (mark read affects own notification only)', C, 'FR-A106', 'None', ''),
 ('Reusable shell', 'Copilot (read/draft/propose; exact scope; confirmation before live effect)', C, 'DEC-035; FR-COP-01', 'None', ''),
 ('Reusable shell', 'Footer/status (last refresh, degraded provider, pending job, support)', P, 'Part 2.5 status bar (automation, budget, STOP)', 'Status footer', 'FR-ENH-C-007; GAP-348'),
 ('Reusable shell', 'Interaction list: keyboard, focus restoration, visible focus, labels, non-colour status, contrast, table-to-card, virtualization, accessible validation, abort on switch, no success on queue acceptance, bulk preview', P, 'Part 2.5 §2.46, §2.47, §2.48 (focus restoration absent)', 'Focus restoration', 'FR-ENH-C-008'),
 ('Operating contract', 'Same as doc 06 (surfaces, routing, configuration, separation)', C, 'See doc 06 rows', 'None', ''),
 ('Layout wireframe', 'Header/Body/Portal/Footer regions for Website and Admin', C, 'Part 2.5 §2.40.2, §2.41', 'None', ''),
 ('Layout wireframe', 'Breakpoints desktop ≥ 1200, tablet 768–1199, mobile < 768', X, 'Part 2.5 §2.48; DEC-043', 'Mapping and test matrix', 'CONFLICT-342; FR-ENH-C-005'),
 ('Layout wireframe', 'WCAG 2.2 AA, focus, error announcements, reduced motion', C, 'Part 2.5 §2.46', 'None', ''),
 ('Layout wireframe', 'Index only after approval; portal/Admin noindex plus auth, not robots.txt security', C, 'Part 2.3/3.1 noindex rules; CA-PUB', 'None', ''),
 ('Layout compositions', 'Public homepage composition', C, 'Part 2.5 W01, W03', 'None', ''),
 ('Layout compositions', 'Authenticated external portal composition', C, 'Part 2.5 §2.40.2 portal navigation', 'None', ''),
 ('Layout compositions', 'Command Centre composition', C, 'Part 2.5 §2.41', 'None', ''),
 ('Replacement controls', 'Adapter preference, capability, entitlement, estimated cost, metering, paid fallback approval; no misleading free/verified badge', P, 'Part 2.5 A008, A011, A012', 'AdapterCard', 'FR-ENH-C-009; RECOMMENDATION-343'),
 ('Replacement controls', 'Per-screen verification (keyboard, SR, responsive, focus, labels, filter persistence, states); synthetic UAT', C, 'Part 2.5 §2.46; Part 6.1', 'Per-screen TC-ENH-C-1nn', ''),
 ('Design quality and release evidence', 'Role-based screenshots and user walkthroughs after implementation', N, '—', 'Evidence pack', 'FR-ENH-C-011; GAP-347'),
 ('Interaction state and accessibility spec', 'Responsive shell; test 360/768/1440 and keyboard flow', X, 'Part 2.5 §2.48', 'Test matrix', 'CONFLICT-342; FR-ENH-C-005'),
 ('Interaction state and accessibility spec', 'Scoped global controls; no aggregate mutation', C, 'FR-FLT-01; DEC-055', 'None', ''),
 ('Interaction state and accessibility spec', 'Loading/empty/error with retry and correlation ID', C, 'Part 2.5 §2.47', 'None', ''),
 ('Interaction state and accessibility spec', 'Action preview (affected, excluded, effect, cost, approval)', C, 'UX-07', 'None', ''),
 ('Interaction state and accessibility spec', 'External portal (own grant; expired grant recovery path)', C, 'CA-PORTAL; §2.47', 'None', ''),
 ('Interaction state and accessibility spec', 'Forms (labels, requiredness, privacy purpose, opaque reference)', C, 'PP-FORM; CA-INTAKE', 'None', ''),
 ('Interaction state and accessibility spec', 'Quality acceptance (exact UAT, keyboard, contrast)', C, 'Part 6.1', 'None', ''),
 ('Design handoff', 'Component, breakpoints, states, filter types, labels, role/mutation permission, exact API operation, visible fields', N, '—', 'Handoff record from 2.7b cards', 'FR-ENH-C-010; GAP-347'),
 ('UI interaction rules', 'Startup switch resets queries and filters ("no stale previous issuer/company data")', X, 'FR-UIS-01; DEC-002', 'Wording fix', 'CONFLICT-340'),
 ('UI interaction rules', 'Persistent command controls (role-based action, preview, confirmation, cost, approval)', C, 'UX-07; CA-APPROVE', 'None', ''),
 ('UI interaction rules', 'Accessibility (keyboard, focus, labels, contrast, 360/768/1440)', P, 'Part 2.5 §2.46', 'Test matrix', 'FR-ENH-C-005'),
 ('UI interaction rules', 'Portal privacy (no internal search, forecast, employee records, private AI knowledge)', C, 'CA-PORTAL; NFR-001', 'None', ''),
 ('UI interaction rules', 'Publishing (draft preview behind Admin auth; immutable DTO; unpublish invalidates cache)', C, 'FR-PUB-01; NFR-020', 'None', ''),
 ('Optimization', 'Optimization view Admin-only; measured vs proposed targets; no fictitious scores', N, '—', 'OI panel', 'FR-ENH-C-004; GAP-345'),
 ('Optimization', 'OPT-06-01 startup templates and tenants (25+10 initial; 50+ and 100 external growth)', X, 'DEC-031', 'Stress-level interpretation', 'CONFLICT-349'),
 ('Optimization', 'OPT-14-01 shared code libraries; independent runtime configs', C, 'UX-09; Part 3.1', 'None', ''),
 ('Optimization', 'OPT-19-01 minimize data and source eligibility', C, 'Part 4.1; DEC-030; BRL-SRC', 'None', ''),
 ('Optimization', 'OPT-02-01…07 and OPT-15-01…04 (same as doc 06)', C, 'See doc 06 rows', 'None', ''),
 ('Acceptance procedures', 'Public website responsiveness (RUM or lab proxy labelled)', P, 'NFR-042 (lab proxy labelling absent)', 'Labelling rule', 'FR-ENH-C-017'),
 ('Acceptance procedures', 'Inbound and outbound journeys ("lead/investor record")', X, 'Part 6 E2E packs; DEC-002', 'Wording fix', 'CONFLICT-340'),
 ('Acceptance procedures', 'Accessibility review (automated plus manual)', C, 'Part 2.5 §2.46', 'None', ''),
 ('Acceptance procedures', 'User productivity (baseline vs candidate task time and errors)', P, 'NFR-090', 'Protocol', 'FR-ENH-C-016; RECOMMENDATION-347'),
 ('Acceptance procedures', 'Dashboard latency, component reuse, separation, filters, states (same as doc 06)', C, 'See doc 06 rows', 'None', ''),
 ('Current scope: UI interaction', 'Distinguish HTML demo interactions from declared field enhancements; simulation never authenticates production users', P, 'Not stated', 'Handoff rule', 'FR-ENH-C-010'),
 ('Screen interaction index', 'Three interaction patterns across 138 blocks', P, 'Part 2.5 layout patterns (interaction checklist absent)', 'IP-PUB/IP-PORTAL/IP-ADMIN', 'FR-ENH-C-006'),
]
for i, (sec, summ, st, loc, act, new) in enumerate(G06, 1):
    cov.append({'doc': '06', 'section': sec, 'aspect_id': 'C06-G%02d' % i, 'aspect_summary': summ, 'status': st,
                'blueprint_location': loc, 'action': act, 'new_ids': new})
for i, (sec, summ, st, loc, act, new) in enumerate(G17, 1):
    cov.append({'doc': '17', 'section': sec, 'aspect_id': 'C17-G%02d' % i, 'aspect_summary': summ, 'status': st,
                'blueprint_location': loc, 'action': act, 'new_ids': new})
os.makedirs(os.path.join(BP, 'final', 'coverage'), exist_ok=True)
with open(os.path.join(BP, 'final', 'coverage', 'C_coverage.csv'), 'w', newline='', encoding='utf-8') as fh:
    w = csv.DictWriter(fh, fieldnames=['doc', 'section', 'aspect_id', 'aspect_summary', 'status', 'blueprint_location', 'action', 'new_ids'])
    w.writeheader(); w.writerows(cov)

ST = [C, P, N, X, NA]
by = collections.defaultdict(collections.Counter)
for r in cov: by[r['doc']][r['status']] += 1
st_tab = ['| Document | ' + ' | '.join(ST) + ' | Total |', '|---|' + '---|' * (len(ST) + 1)]
for d in ('06', '17'):
    st_tab.append('| %s | ' % d + ' | '.join(str(by[d][s]) for s in ST) + ' | %d |' % sum(by[d].values()))
tot = collections.Counter(r['status'] for r in cov)
st_tab.append('| **Total** | ' + ' | '.join('**%d**' % tot[s] for s in ST) + ' | **%d** |' % len(cov))

def gtable(rows, prefix):
    t = ['| ID | Section | Aspect | Status | Blueprint location | Action / new IDs |', '|---|---|---|---|---|---|']
    for i, (sec, summ, st, loc, act, new) in enumerate(rows, 1):
        t.append('| %s-G%02d | %s | %s | %s | %s | %s |' % (prefix, i, sec, summ, st, loc, (act + ('; ' + new if new else '')) if act != 'None' else ('None' + ('; ' + new if new else ''))))
    return '\n'.join(t)

grp = collections.OrderedDict()
def gkey(a):
    for k, lab in (('C06-FLD', 'Doc 06 field decisions (current/add/replace)'), ('C06-OP', 'Doc 06 screen operations'),
                   ('C06-TAB', 'Doc 06 tables'), ('C06-IMP', 'Doc 06 test associations (SM-FR/UT/UAT)'),
                   ('C06-CAP', 'Doc 06 retained website capabilities'), ('C06-PLG', 'Doc 06 integration associations (distinct names)'),
                   ('C06-REL', 'Doc 06 related-screen sets'), ('C06-AUT', 'Doc 06 automation/acceptance statements'),
                   ('C17-INT', 'Doc 17 screen intent and interaction'), ('C17-FLD', 'Doc 17 field decisions (common with doc 06)'),
                   ('C06-G', 'Doc 06 global aspects'), ('C17-G', 'Doc 17 global aspects')):
        if a.startswith(k): return lab
    return 'Other'
where = {'Doc 06 field decisions (current/add/replace)': 'Part 2.7b cards (each P row individually)',
         'Doc 06 screen operations': '§2.7.4.3 (N), §2.7.4.4 (P), cards', 'Doc 06 tables': '§2.7.4.5',
         'Doc 06 test associations (SM-FR/UT/UAT)': '§2.7.4.6', 'Doc 06 retained website capabilities': '§2.7.4.1',
         'Doc 06 integration associations (distinct names)': '§2.7.4.7', 'Doc 06 related-screen sets': 'Part 2.7b cards; FR-ENH-C-012',
         'Doc 06 automation/acceptance statements': 'Part 2.1 FR rows', 'Doc 17 screen intent and interaction': 'Part 2.7b cards; §2.7.5.2',
         'Doc 17 field decisions (common with doc 06)': 'Doc 06 rows', 'Doc 06 global aspects': '§2.7.3.1', 'Doc 17 global aspects': '§2.7.3.2'}
for r in cov:
    grp.setdefault(gkey(r['aspect_id']), collections.Counter())[r['status']] += 1
gr = []
for k, c in grp.items():
    gr.append('| %s | %d | %d | %d | %d | %d | %s |' % (k, sum(c.values()), c[C], c[P], c[N] + c[X], c[NA], where.get(k, '')))

dist = {}
for r in OPS: dist.setdefault((r['method'], r['path']), r)
nc = [k for k, v in dist.items() if v['status'] == N]
ctrl = sum(1 for k, v in dist.items() if v['status'] != C and '/control' in k[1])
appr = sum(1 for k, v in dist.items() if v['status'] != C and (k[1].endswith('/approve') or k[1].endswith('/review')))
ns = sum(1 for k, v in dist.items() if v['status'] != C and ('/api/v1/sales/' in k[1] or '/workspace/' in k[1]))
fl = [r for r in cov if r['aspect_id'].startswith('C06-FLD')]
V = {
 'N06': sum(by['06'].values()), 'N17': sum(by['17'].values()),
 'N06_FLD': len(fl), 'N06_OP': len(OPS), 'N06_TAB': len(TABS), 'N06_IMP': 138,
 'N06_PLG': sum(1 for r in cov if r['aspect_id'].startswith('C06-PLG')), 'N06_G': len(G06), 'N17_G': len(G17),
 'STATUS_TABLE': '\n'.join(st_tab), 'FLD_TOTAL': len(fl), 'FLD_C': sum(1 for r in fl if r['status'] == C),
 'FLD_P': sum(1 for r in fl if r['status'] == P), 'FIELD_P_BY_VIEW': frag['FIELD_P_BY_VIEW'],
 'OPS_DIST': len(dist), 'OPS_ROWS': len(OPS), 'OPS_DC': sum(1 for v in dist.values() if v['status'] == C),
 'OPS_DP': sum(1 for v in dist.values() if v['status'] == P), 'OPS_DN': len(nc),
 'OPS_CONTROL': ctrl, 'OPS_APPROVE': appr, 'OPS_NS': ns,
 'TAB_TOTAL': len(TABS), 'TAB_C': sum(1 for r in TABS if r['status'] == C), 'TAB_P': sum(1 for r in TABS if r['status'] == P),
 'TAB_N': sum(1 for r in TABS if r['status'] == N), 'CSV_ROWS': len(cov),
 'G06_TABLE': gtable(G06, 'C06'), 'G17_TABLE': gtable(G17, 'C17'), 'GROUP_ROWS': '\n'.join(gr),
 'CROSSWALK': frag['CROSSWALK'], 'CAPS': frag['CAPS'], 'OPS_N': frag['OPS_N'], 'OPS_P': frag['OPS_P'],
 'OPS_C_LIST': frag['OPS_C_LIST'], 'TABLES': frag['TABLES'], 'PLUGINS': frag['PLUGINS'],
 'PLUG_COUNTS': ', '.join('%s %d' % kv for kv in frag['PLUG_COUNTS'].items()), 'REL_TOP': frag['REL_TOP'], 'LOC_VIEW': frag['LOC_VIEW'],
}
t = open(TPL, encoding='utf-8').read()
for k, v in V.items():
    t = t.replace('{{%s}}' % k, str(v))
assert '{{' not in t, t[t.index('{{'):t.index('{{') + 40]
open(os.path.join(BP, 'Part-02-7a_Source_Pack_UI_Catalog_and_UX_Enhancements.md'), 'w', encoding='utf-8').write(t)
print({k: v for k, v in V.items() if not isinstance(v, str) or len(v) < 60})
print(dict(tot))
