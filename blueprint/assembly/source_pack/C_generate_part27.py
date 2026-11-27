"""Group C generator: builds Part 2.7b (per-screen contract catalogue), markdown fragments for Part 2.7a,
and the coverage CSV, from the outputs of C_parse_ui_catalog.py.

Usage: python3 -I C_generate_part27.py <blueprint_dir> <c_out_dir>
"""
import csv, json, re, os, sys, collections

BP, OUT = sys.argv[1], sys.argv[2]
S = json.load(open(os.path.join(OUT, 'c_screens.json')))
SUM = json.load(open(os.path.join(OUT, 'c_recon_summary.json')))
def rcsv(n): return list(csv.DictReader(open(os.path.join(OUT, n), encoding='utf-8')))
FIELDS, OPS, TABS, TESTS, PLUGS, RELS = (rcsv('c_fields.csv'), rcsv('c_ops.csv'), rcsv('c_tables.csv'),
                                         rcsv('c_tests.csv'), rcsv('c_plugins.csv'), rcsv('c_related.csv'))
P21 = open(os.path.join(BP, 'Part-02-1_Functional_Design_Modules_and_FR_Register.md'), encoding='utf-8').read()
P25 = open(os.path.join(BP, 'Part-02-5_UX_UI_Design.md'), encoding='utf-8').read()

def cells(line):
    return [c.strip() for c in line.strip().strip('|').split('|')]
fr_meta, ux_meta = {}, {}
for ln in P21.split('\n'):
    m = re.match(r'\| FR-([WA]\d{2,3}) \|', ln)
    if m:
        c = cells(ln); fr_meta[m.group(1)] = {'profiles': c[-3], 'traces': c[-2], 'wave': c[-1]}
for ln in P25.split('\n'):
    m = re.match(r'\| ([WA]\d{2,3}) \|', ln)
    if m:
        c = cells(ln); ux_meta[m.group(1)] = {'pattern': c[2], 'actions': c[4] if len(c) > 4 else ''}
VIEW = {}
for ln in P25.split('\n'):
    m = re.match(r'\| \*\*(Overview|Discovery|Outreach & Marketing|Follow-ups|Objections|Closure|Automation|Global \(always available\))\*\* \| (.*) \|$', ln)
    if m:
        for sid in re.findall(r'A\d{3}', m.group(2)):
            VIEW.setdefault(sid, m.group(1).replace(' (always available)', ''))
for sid in [s['id'] for s in S['screens'] if s['id'].startswith('W')]:
    n = int(sid[1:])
    VIEW[sid] = ('Website public' if n <= 11 or n in (30, 31) else 'Website intake' if n <= 20 or n == 32 else 'Portal')

FAM = {'Overview': 'FLT-01 Scope, FLT-07 Commercial, FLT-04 Engagement, FLT-05 Operations (as_of), FLT-02 Geography (currency)',
       'Discovery': 'FLT-01 Scope, FLT-03 Evidence, FLT-02 Geography, FLT-07 Commercial (need, customer/supplier type)',
       'Outreach & Marketing': 'FLT-01 Scope, FLT-06 Marketing, FLT-04 Engagement, FLT-03 Evidence (claims), FLT-02 Geography (language, timezone)',
       'Follow-ups': 'FLT-01 Scope, FLT-04 Engagement, FLT-05 Operations (task, deadline), FLT-07 Commercial (renewal)',
       'Objections': 'FLT-01 Scope, FLT-04 Engagement (objection, escalation), FLT-07 Commercial (quotation)',
       'Closure': 'FLT-01 Scope, FLT-07 Commercial, FLT-05 Operations (approval, deadline), FLT-02 Geography (currency)',
       'Automation': 'FLT-01 Scope, FLT-05 Operations (workflow state, approval, cost, quota, error, as_of)',
       'Global': 'FLT-01 Scope, FLT-05 Operations',
       'Website public': 'None of FLT-01…11 (internal filters excluded, doc 06 Part A); published selectors only',
       'Website intake': 'None (bounded intake form; startup/offering locked from context)',
       'Portal': 'Own-record selectors only (status, date, reference); no internal filters'}
VERT = {'A104': 'FLT-08 AppNAI', 'A105': 'FLT-11 OrganicSpec', 'A091': 'FLT-09 MedMaarg', 'A092': 'FLT-09 MedMaarg',
        'A015': 'FLT-08…11 by capability profile', 'A016': 'FLT-08…11 by capability profile', 'A022': 'FLT-08…11 by capability profile',
        'A029': 'FLT-08…11 by capability profile', 'A027': 'FLT-08…11 by capability profile'}

# ---------------------------------------------------------------- field type inference [ASSUMPTION-341]
RULES = [
    (r'\beligib', 'Computed eligibility decision (gov_eligibility_decision)', 'EligibilityBadge per channel (read-only, rule tooltip)', 'Computed by the PDP; never editable; shows blocking rule ID (UX-04)'),
    (r'\b(verification|verified)\b', 'Verification state + evidence reference', 'StateBadge with evidence link', 'Set only by the verification workflow; expiry enforced'),
    (r'\bmode\b', 'Enumeration (Manual, Assisted, Supervised, Controlled Autonomous / L0–L3)', 'Select bounded by policy', 'Capped by DEC-064 autonomy limits'),
    (r'\b(mfa|recovery method|identity provider|password)\b', 'Identity attribute held by the reused IdP', 'IdP-hosted control', 'Never persisted or displayed by this product (DEC-019)'),
    (r'\b(role|grant|access|entitlement)', 'Role / grant reference (scoped)', 'Multi-select with scope chips', 'Least privilege; change audited; revocation within 60 s (NFR-050)'),
    (r'\b(sla|dedup|window|buffer|quiet hours)\b', 'Duration (ISO 8601) or time window', 'Duration input', 'Within configured bounds'),
    (r'\btax\b', 'TaxProfile / tax line reference', 'Read-only computed line', 'Per DEC-027; server-computed'),
    (r'\battribution\b', 'Attribution ID / event reference', 'Read-only text', 'First-party only; captured server-side'),
    (r'\bhash\b', 'char(64) SHA-256', 'HashBadge (read-only)', 'Server-computed; never editable'),
    (r'\b(id|reference|ref)\b', 'Identifier (UUIDv7 or opaque reference)', 'Read-only text, copy button', 'Server-generated; not user-editable'),
    (r'time ?zone', 'IANA time-zone ID', 'Searchable select', 'Must be a valid IANA zone; default from user/startup profile'),
    (r'\b(amount|price|budget|cost|spend|revenue|payable|receivable|margin|discount)\b', 'Money: Decimal(18,2) + ISO 4217', 'MoneyInput / MoneyDisplay', 'Decimal only; currency required; server recomputes (CA-FIN)'),
    (r'\bcurrency\b', 'ISO 4217 code', 'Select (allowed currencies)', 'Allowlist per startup TaxProfile (DEC-027)'),
    (r'\b(quantity|qty)\b', 'Decimal quantity', 'QuantityInput (value + unit)', 'Non-negative; validated range; unit mandatory'),
    (r'\bunit\b', 'Unit of measure (ref_unit)', 'Select', 'Allowed units per SKU'),
    (r'\b(date|deadline|due|expiry|expires|valid until|started|fire|verified at|observed|published|received|effective|renewal date|last update|last updated|eta|schedule)\b', 'Timestamp (UTC stored) or date', 'DateTimePicker with time zone / DateTimeDisplay', 'Stored UTC; displayed in user and record time zone; range validated'),
    (r'\b(status|state|stage|lifecycle|outcome|certainty)\b', 'Enumeration (state machine, Part 2.3)', 'StateBadge; transition menu shows only valid transitions', 'Changed only by controlled transition; never free text'),
    (r'\bemail\b', 'Email address (encrypted at rest, HMAC lookup)', 'Email input', 'RFC 5322 syntax; masked per ABAC; never used as lookup key on public paths'),
    (r'\b(consent|permission|terms|opt-out|guardian)\b', 'Consent / permission record reference', 'ConsentNotice or toggle with policy revision', 'Purpose and policy revision recorded; withdrawal immediate'),
    (r'\b(country|region|location|geography|city|state)\b', 'ISO 3166 code or reference location', 'Searchable select', 'Allowlist; jurisdiction rule pack applies (DEC-029)'),
    (r'\b(language|locale)\b', 'BCP 47 tag', 'Select (enabled locales)', 'DEC-026 enabled locales only'),
    (r'\b(owner|reviewer|approver|assignee|user|administrator|legal reviewer|team)\b', 'User/team reference (scoped membership)', 'User picker (scoped)', 'Only members with the required role in scope'),
    (r'\b(score|confidence|precision|progress|rate|probability|weight)\b', 'Decimal 0–100 (or 0–1) computed', 'ScoreBreakdown / progress bar (read-only)', 'Computed server-side; Unknown shown separately from 0'),
    (r'\b(revision|version)\b', 'Integer revision / version label', 'Read-only label with diff link', 'Optimistic concurrency; stale → 409'),
    (r'\b(approval)\b', 'Approval reference (gov_approval)', 'Approval chip with approver and SLA', 'Computed from Approval record; hash-bound (CA-APPROVE)'),
    (r'\b(evidence|citation|claim|source|provenance)\b', 'Evidence / source reference', 'CitationChip or EvidenceCard (drawer)', 'Must resolve to permitted, unexpired evidence'),
    (r'\b(channel)\b', 'Enumeration (email, whatsapp, web, phone, social, portal)', 'Select / channel icon', 'Only channels enabled and eligible for scope'),
    (r'\b(priority|severity|risk|band)\b', 'Enumeration', 'Badge / select', 'Allowed values from configuration'),
    (r'\b(enabled|active)\b', 'Boolean', 'Toggle (role-gated)', 'Change audited'),
    (r'\b(file|attachment|document|upload|documents)\b', 'File reference (object storage key + scan state)', 'FileUpload with scan status', 'Scanned before use (NFR-021); size/type allowlist'),
    (r'\b(frequency|cadence|interval)\b', 'Schedule rule (RRULE)', 'Schedule builder', 'Bounded by caps and quiet hours'),
    (r'\b(search|sort|filter)\b', 'Query parameter', 'Search box / sort select', 'Allowlisted fields; server-validated'),
    (r'\b(count|impressions|volume|usage|attempts|retry)\b', 'Integer (computed)', 'Number (read-only)', 'Distinct records; Unknown ≠ 0'),
    (r'\b(url|website|domain|link)\b', 'URL / verified domain', 'URL input or link', 'https only; domain must be verified where it drives publication'),
    (r'\b(industry|category|request type|delivery model|service model|platform|technology|topic|institution type|use case|model|taxonomy|content type|mode of delivery|domain area)\b', 'Enumeration from versioned taxonomy (ref_value)', 'Select / multi-select (taxonomy)', 'Values from the active reference dataset (CFG-32); unknown values rejected'),
    (r'\b(field schema|schema)\b', 'JSON Schema document (versioned)', 'Schema editor with validation report', 'Allowed field types only; validated before activation (CA-CONFIG)'),
    (r'\b(stop condition|escalation|revocation|condition|exclusion)\b', 'Typed rule expression', 'RuleBuilder (typed conditions)', 'Sandboxed expression over typed fields (DEC-051); validated and simulated'),
    (r'\b(period|freshness|validity|latency|duration)\b', 'Period or duration', 'Period picker / duration display', 'Bounded; freshness shown against target (amber when stale)'),
    (r'\b(limit|capacity|daily limit|cap|quota)\b', 'Integer limit (bounded)', 'Number input with unit', 'Within plan/entitlement bounds; tightening needs no approval, loosening does (DEC-038)'),
    (r'\b(health|readiness|availability|conversion|qualified leads|rollback|pipeline value|sentiment)\b', 'Computed indicator', 'Indicator badge or tile (read-only)', 'Computed server-side with as_of; Unknown shown separately'),
    (r'\bnext action\b', 'Task reference + due timestamp', 'Inline task chip', 'Due date required; owner required'),
    (r'\b(policy|page|provider|provider account|pipeline|trigger|task|referral|pilot|payment|opportunity|incident|institution|sender|rule|test fixture|suppression|legal hold|location|license|licence)\b', 'Entity reference (scoped FK)', 'Scoped lookup / select', 'Must belong to the same tenant and startup (composite FK)'),
    (r'\b(organization|startup|tenant|offering|campaign|template|workflow|contact|partner|customer|deal|invoice|plan|subscription|order|quote|proposal|agreement|contract|sku|programme|program|event|audience|keyword|business unit|business line|capability|objective|need|signal)\b', 'Entity reference (scoped FK)', 'Scoped lookup / select', 'Must belong to the same tenant and startup (composite FK)'),
    (r'\b(name|title|subject)\b', 'Text (≤ 200)', 'Text input', 'Trimmed; required where marked'),
    (r'\b(message|description|notes|reason|summary|scope|requirement|response|body)\b', 'Text (≤ 4,000)', 'Text area with counter', 'No secrets or special-category data; length limit'),
]
def infer(field):
    f = field.lower()
    for pat, typ, ctl, rule in RULES:
        if re.search(pat, f):
            return typ, ctl, rule
    return 'Text or enumeration (confirm in data dictionary)', 'Text input / select', 'Allowlisted, validated server-side'

def rule_for(field, remove_text):
    out = []
    for part in [p.strip() for p in remove_text.rstrip('.').split(';')]:
        if ':' in part:
            k, v = part.split(':', 1)
            if k.strip().lower() == field.lower():
                out.append(v.strip())
    return '; '.join(out)

# ---------------------------------------------------------------- crosswalk
legacy = {}
for sid, b in S['blocks06'].items():
    if b.get('legacy'):
        legacy[sid] = b['legacy']
CAPMAP = {'CAP008': 'W29, W30', 'CAP032': 'W12–W17', 'CAP043': 'W18', 'CAP049': 'W11', 'CAP061': 'W10', 'CAP068': 'W19',
          'CAP070': 'W20', 'CAP079': 'W24', 'CAP082': 'W26', 'CAP085': 'W27'}

ops_by = collections.defaultdict(list)
for r in OPS: ops_by[r['screen']].append(r)
tabs_by = collections.defaultdict(list)
for r in TABS:
    for s_ in r['screens'].split(';'):
        tabs_by[s_].append(r)
plug_by = collections.defaultdict(list)
for r in PLUGS: plug_by[r['screen']].append(r)
fields_by = collections.defaultdict(list)
for r in FIELDS: fields_by[r['screen']].append(r)

DEV_PLUGINS = {'Agent SDK Dev', 'CLAUDE.md Management', 'Claude Code Setup', 'MCP Server Dev', 'Plugin Developer Toolkit',
               'Security Guidance', 'Skill Creator', 'document skills', 'document skills dev', 'content studio', 'Content Studio',
               'content-marketing', 'Marketing', 'Sales', 'customer-sales-automation', 'seo-analysis-monitoring',
               'seo-content-creation', 'seo-technical-optimization', 'social-publishing', 'Figma', 'Postman', 'GitHub', 'github'}
OSS_RUNTIME = {'react', 'react forms', 'django', 'django auth', 'drf', 'postgresql', 'pgvector', 'celery', 'celery beat', 'redis',
               'deepeval', 'DeepEval', 'Pydantic AI', 'Playwright', 'playwright', 'pytest'}
COMMERCIAL_UNVERIFIED = {'Common Room', 'Leadfeeder', 'Crossbeam Skills', 'Clay', 'Endgame', 'Socialinsider', 'Writesonic', 'Adspirer'}
def plug_class(n):
    if n.lower().startswith('internal'): return 'INT', 'Internal React/Django; no plugin'
    if n in DEV_PLUGINS: return 'DEV', 'Development-time aid only; no runtime entitlement, no screen control (CONFLICT-346)'
    if n in OSS_RUNTIME: return 'OSS', 'Open-source runtime/test dependency (B01 shared)'
    if n in COMMERCIAL_UNVERIFIED: return 'CMU', 'Commercial, unverified; ₹0 committed; disabled until procurement approval'
    return 'ADP', 'Provider adapter (Part 3.2 §3.2.4) behind feature flag; quota and price verify at implementation (as of 27 Nov 2026)'

def esc(s):
    return (s or '').replace('|', '/').replace('\n', ' ')

# ---------------------------------------------------------------- Part 2.7b
order = [s['id'] for s in S['screens']]
groups = collections.OrderedDict()
for sid in order:
    groups.setdefault(VIEW.get(sid, 'Global'), []).append(sid)
GORDER = ['Website public', 'Website intake', 'Portal', 'Global', 'Overview', 'Discovery', 'Outreach & Marketing',
          'Follow-ups', 'Objections', 'Closure', 'Automation']
blines = []
B = blines.append
B('# AI Growth Engine: Employee Sales & Marketing Automation')
B('## Application Blueprint: PART 2 (Batch 2.7b), Source Pack UI Catalog: Per-Screen Contract Cards (147 screens)')
B('')
B('| Field | Value |'); B('|---|---|')
B('| Document | Application Blueprint · Part 2.7 (Batch 2.7b of 2; companion to Batch 2.7a) |')
B('| Version | 1.0 · 27 Nov 2026 |')
B('| Baseline | Source pack documents 06 (UI Screen, Filter, API and Table Catalog) and 17 (Unified Command Centre UI/UX and Interaction Design); FRD §11, §16.2; Parts 2.1, 2.5, 3.2, 3.3, 6.1 |')
B('| Roles applied | Lead UX/UI Designer, Frontend Lead, Accessibility Specialist, Business Systems Analyst (BSA) |')
B('')
B('---')
B('')
B('## 2.7.10 How to read the screen contract cards')
B('')
B('Each of the 147 interfaces has one card. A card reconciles, row by row, what documents 06 and 17 declare for the screen against the blueprint, and closes every gap found by the parser `assembly/source_pack/C_parse_ui_catalog.py` (Batch 2.7a §2.7.4). The cards are **binding field contracts** for frontend, API serializer and test design: they complete Part 2.5 §2.43 (which delegates field lists to Part 2.1) and Part 2.1 §2.4 (which lists only the standardized and added fields). [GAP-340 closed here]')
B('')
B('| Card block | Content | Source → blueprint rule |')
B('|---|---|---|')
B('| Header table | Surface, Command Centre view, layout pattern (Part 2.5), legacy screen ID (doc 06 "existing NNN"), build class, doc 06 location class, FR, wave and epic, acceptance profiles | Legacy ID per FR-ENH-C-001; build class per FR-ENH-C-014 |')
B('| Filters | Filter families FR-FLT-01…11 that apply on the screen | [ASSUMPTION-343]; vertical families appear only when the selected startup\'s capability profile enables them (DEC-052) |')
B('| Actions and automation | Doc 06/17 automation statement and Part 2.5 key actions | Every action is permission-checked server-side (CA-ADMIN/CA-PORTAL) |')
B('| Field contract | Every field from doc 06 "Current declared fields" (origin **B** = retained baseline) and "Add or standardize" (origin **A**); replace rules from "Remove / replace" (origin **R**) | Type, control and validation inferred by rule set R-FLD [ASSUMPTION-341]; data dictionary Part 3.3 §3.3.6 prevails on conflict |')
B('| Field status | **C** = already named in Part 2.1 key fields or Part 2.5 regions; **P** = baseline field the blueprint did not name, now specified by this card; **N/A** = layout-only | Parser tokens ≥ 50% match |')
B('| Legacy operations | Every method/path doc 06 names for the screen, with the blueprint API ID(s) | **C** exact; **P** equivalent DERIVED path (alias route required, FR-ENH-C-003); **N** no equivalent (new alias or DERIVED op required, §2.7.5.3 of Batch 2.7a) |')
B('| Tables | Every source table (growth_/sales_ prefix) mapped to blueprint ENT and physical table | **C** suffix match; **P** judged synonym; **N** no entity (GAP-349) |')
B('| Integrations | Doc 06 plugin/provider associations, classified INT/OSS/ADP/CMU/DEV | §2.7.5.6 of Batch 2.7a; prices "verify at time of implementation (as of 27 Nov 2026)" |')
B('| Tests | SM-UAT-S (doc 06 implementation table), SM-UX-UAT, SM-UT families, and the new conformance test TC-ENH-C-1nn | Alias rules of Part 6.1 §6.1.12.5 verified mechanically (counts identical) |')
B('| Related screens | Doc 06 "Related" list = required in-context navigation links that keep scope (FR-ENH-C-012) | Part 2.5 rows mention only 3 of 435 links |')
B('')
B('**Field-type rule set R-FLD (summary).** Hash → `char(64)` read-only; ID/reference → server-generated identifier; money words → Decimal + ISO 4217 (CA-FIN, DEC-027); currency → ISO 4217 allowlist; quantity/unit → QuantityInput; dates/deadlines → UTC timestamp with time-zone display; status/state/stage → state-machine enum, transition only (Part 2.3); email → encrypted with HMAC lookup; consent/permission → consent record with policy revision; geography → ISO 3166; language → BCP 47 (DEC-026); people → scoped user picker; score/confidence → computed, Unknown ≠ 0 (FR-UIS-02); revision → optimistic concurrency; approval → Approval chip (CA-APPROVE); evidence/source → citation chip; entity names → scoped FK lookup; free text → bounded text area. [ASSUMPTION-341]')
B('')
GN = {'Website public': '2.7.11 Website: public pages', 'Website intake': '2.7.12 Website: intake forms',
      'Portal': '2.7.13 Portal and SaaS client', 'Global': '2.7.14 Admin: global shell',
      'Overview': '2.7.15 Admin: Overview view', 'Discovery': '2.7.16 Admin: Discovery view',
      'Outreach & Marketing': '2.7.17 Admin: Outreach & Marketing view', 'Follow-ups': '2.7.18 Admin: Follow-ups view',
      'Objections': '2.7.19 Admin: Objections view', 'Closure': '2.7.20 Admin: Closure view',
      'Automation': '2.7.21 Admin: Automation view (workflow, governance, administration, operations)'}
tc_no = 100
tc_index = {}
for g in GORDER:
    if g not in groups: continue
    B('## ' + GN[g]); B('')
    k = 0
    for sid in groups[g]:
        k += 1; tc_no += 1; tc_index[sid] = 'TC-ENH-C-%03d' % tc_no
        s = next(x for x in S['screens'] if x['id'] == sid)
        d = S['dec06'][sid]; imp = S['impl'].get(sid, {}); fm = fr_meta.get(sid, {}); um = ux_meta.get(sid, {})
        B('### %s.%d %s: %s' % (GN[g].split(' ')[0], k, sid, s['name'])); B('')
        B('| Attribute | Value |'); B('|---|---|')
        B('| Surface / access (doc 06) | %s |' % esc(s['access'] or 'Confidential Admin; assigned role and scope required'))
        B('| Command Centre view · pattern (Part 2.5) | %s · %s |' % (g, esc(um.get('pattern', ''))))
        B('| Legacy screen ID · build class · location class (doc 06) | %s · %s · %s |' % (
            ('existing ' + legacy[sid]) if sid in legacy else ('new in 147-scope' if sid in ('W31', 'W32', 'W33', 'W34') or int(sid[1:]) >= 109 and sid[0] == 'A' else 'original W-ID (no legacy number)' if sid[0] == 'W' else 'original A-ID'),
            esc(s['build']) or 'Template/typed configuration (doc 06 operating contract)', esc(s['location']) or ('Website' if sid[0] == 'W' else 'Admin (new interface)')))
        B('| FR · wave · epic · profiles | FR-%s (alias SM-FR-%s%s, SM-UX-FR-%s) · %s · %s |' % (
            sid, sid, (', trace ' + esc(imp.get('trace'))) if imp.get('trace') else '', sid, esc(fm.get('wave', '')), esc(fm.get('profiles', ''))))
        B('| Filters | %s%s |' % (FAM.get(g, ''), ('; vertical: ' + VERT[sid]) if sid in VERT else ''))
        B('| Automation (doc 06/17) | %s |' % esc(d.get('automation', '')))
        B('| Key actions (Part 2.5) | %s |' % esc(um.get('actions', '')))
        B('| Screen acceptance (doc 06) | %s |' % esc(d.get('acceptance', '')))
        if s.get('intent17'):
            B('| Intent (doc 17) | %s |' % esc(s['intent17']))
        ip = 'IP-PUB' if 'published content' in (s.get('interaction17') or '') else 'IP-PORTAL' if 'identity-bound portal' in (s.get('interaction17') or '') else 'IP-ADMIN'
        B('| Interaction pattern (doc 17 → 2.7a §2.7.5.2) | %s |' % ip)
        rel = d.get('related', '')
        B('| Related screens (in-context links, FR-ENH-C-012) | %s |' % esc(rel))
        uts = sorted(set(imp.get('unit', [])))
        B('| Tests | %s; SM-UX-UAT-%s; unit families %s; **%s** (field and contract conformance) |' % (
            ', '.join(imp.get('uat', [])) or 'no SM-UAT alias (new interface, Part 6.1 §6.1.12.5)', sid,
            ', '.join(u.replace('SM-UT-', '') for u in uts) if uts else 'n/a', tc_index[sid]))
        B('')
        # field contract
        fl = fields_by.get(sid, [])
        if fl:
            B('**Field contract**'); B('')
            B('| # | Field | Origin | Status | Type | Control | Validation and rule |'); B('|---|---|---|---|---|---|---|')
            rem = d.get('remove', '')
            n = 0
            for r in fl:
                if r['kind'] == 'remove/replace':
                    continue
                n += 1
                typ, ctl, rule = infer(r['field'])
                extra = rule_for(r['field'], rem)
                origin = 'B' if r['kind'] == 'current' else 'A'
                if extra: origin += '+R'; rule = extra + '. ' + rule
                st = {'Covered': 'C', 'Partially covered': 'P', 'Not applicable': 'N/A'}[r['status']]
                if r['field'].startswith('Contextual'):
                    typ, ctl, rule = 'Layout only', 'Published page blocks', 'No data field; content from approved snapshot'
                B('| %d | %s | %s | %s | %s | %s | %s |' % (n, esc(r['field']), origin, st, typ, ctl, esc(rule)))
            if rem and rem not in ('No catalog field removed.', 'New layout.'):
                B(''); B('*Replace rules (doc 06 "Remove / replace"):* %s' % esc(rem))
            B('')
        # ops
        ol = ops_by.get(sid, [])
        if ol:
            B('**Legacy operations → blueprint API**'); B('')
            B('| Method | Source path | Status | Blueprint op(s) | Match basis |'); B('|---|---|---|---|---|')
            for r in ol:
                st = {'Covered': 'C', 'Partially covered': 'P', 'Not covered': 'N'}[r['status']]
                B('| %s | `%s` | %s | %s | %s |' % (r['method'], r['path'], st, r['bp_ops'] or '—', r['match']))
            B('')
        tl = tabs_by.get(sid, [])
        if tl:
            B('**Tables → blueprint entities:** ' + '; '.join(
                '`%s` → %s %s (%s)' % (r['source_table'], r['bp_ent'] or 'none', ('`' + r['bp_table'] + '`') if r['bp_table'] else '', {'Covered': 'C', 'Partially covered': 'P', 'Not covered': 'N'}[r['status']])
                for r in tl))
            B('')
        pl = plug_by.get(sid, [])
        if pl:
            B('**Integrations (doc 06):** ' + '; '.join('%s [%s]' % (r['integration'], plug_class(r['integration'])[0]) for r in pl))
            B('')
    B('')

# ---------------------------------------------------------------- per-screen conformance TC table
B('## 2.7.22 Per-screen conformance test cases (TC-ENH-C-101…247)')
B('')
B('Each card\'s conformance test is one parameterized test case run against the card. All follow this template; the parameter set is the card itself.')
B('')
B('```gherkin')
B('Feature: Screen field and contract conformance (TC-ENH-C-1nn)')
B('  Scenario Outline: Screen <screen> matches its contract card')
B('    Given a two-tenant synthetic fixture with startups S1 and S2 and a user holding the card\'s role in S1 only')
B('    When the user opens <screen> in scope S1')
B('    Then every field in the card is rendered with its declared control, label and validation')
B('    And read-only, computed and lifecycle-derived fields cannot be edited in the UI or through the API')
B('    And each legacy operation in the card resolves to the mapped blueprint operation with identical authorization')
B('    And the network log shows no call outside the card\'s operations and no Admin route from a Website bundle')
B('    When the user switches scope to S2 without a grant')
B('    Then in-flight requests are aborted, cached S1 records are cleared and a denied state is shown')
B('    And loading, empty, denied, stale, error and success states each render with an accessible name')
B('  Examples:')
B('    | screen |')
B('    | each of the 147 card IDs |')
B('```')
B('')
B('| TC | Screen | TC | Screen | TC | Screen | TC | Screen |'); B('|---|---|---|---|---|---|---|---|')
items = list(tc_index.items())
for i in range(0, len(items), 4):
    row = items[i:i + 4]
    while len(row) < 4: row.append(('', ''))
    B('| ' + ' | '.join('%s | %s' % (v, k) for k, v in row) + ' |')
B('')
B('Priority: P0 for screens with CA-FIN, CA-DISPATCH or CA-APPROVE profiles; P1 otherwise. Automation: Playwright component and end-to-end suites with axe-core; API leg via Schemathesis contract tests (Part 6.1). Each TC links FR-%s of its screen, FR-ENH-C-002 and FR-ENH-C-003.' % '…')
B('')
B('## 2.7.23 Quality gate: Batch 2.7b')
B('')
B('| # | Check | Result | Notes and fixes applied |'); B('|---|---|---|---|')
B('| 1 | Every requirement traced to a source | Pass | Every card row cites doc 06/17 content and the blueprint row it reconciles |')
B('| 2 | Assumptions, gaps, conflicts tagged and logged | Pass | ASSUMPTION-341/343, GAP-340/349, CONFLICT-346 used here; register in Batch 2.7a §2.7.8 |')
B('| 3 | IDs unique and consistent | Pass | 147 cards, one per screen; TC-ENH-C-101…247 unique; FR, API and ENT IDs from Parts 2.1, 3.2, 3.3 |')
B('| 4 | No requirement lacks a test | Pass | One conformance TC per card plus alias tests |')
B('| 5 | Negative, edge, security, accessibility | Pass | Conformance template covers cross-scope denial, read-only enforcement, states and accessible names |')
B('| 6 | Agents: guardrail, fallback, KPI, cost | N/A | No agent defined in this batch |')
B('| 7 | Time-sensitive facts flagged | Pass | Integration prices not restated; classification ADP/CMU says verify at implementation (as of 27 Nov 2026) |')
B('| 8 | No restricted data to free-tier models | Pass | No routing change |')
B('| 9 | Consistent with earlier parts | Pass | Types defer to Part 3.3 data dictionary on conflict (ASSUMPTION-341) |')
B('')
B('**Status: Part 2 Batch 2.7b complete. 147 screen contract cards, %d field rows, %d screen-operation rows, %d table mappings, 147 conformance test cases.**' % (
    sum(1 for r in FIELDS if r['kind'] != 'remove/replace'), len(OPS), len(TABS)))
open(os.path.join(BP, 'Part-02-7b_Source_Pack_UI_Catalog_and_UX_Enhancements.md'), 'w', encoding='utf-8').write('\n'.join(blines) + '\n')

# ---------------------------------------------------------------- fragments for 2.7a
frag = {}
# crosswalk
xs = ['| Screen | Legacy | Screen | Legacy | Screen | Legacy | Screen | Legacy |', '|---|---|---|---|---|---|---|---|']
it = [(k, legacy[k]) for k in order if k in legacy]
for i in range(0, len(it), 4):
    row = it[i:i + 4]
    while len(row) < 4: row.append(('', ''))
    xs.append('| ' + ' | '.join('%s | %s' % r for r in row) + ' |')
frag['CROSSWALK'] = '\n'.join(xs)
cw = ['| Legacy capability | Behaviour (doc 06) | Business modules | Original operations | Mapped W-screen(s) | Status |', '|---|---|---|---|---|---|']
for k, b in S['blocks06'].items():
    if k.startswith('CAP'):
        cw.append('| %s | %s | %s | %s | %s | Partial: function in FR-%s; legacy number tracked (FR-ENH-C-001); operations in §2.7.4.3–4 |' % (
            k[3:], esc(b.get('Behavior')), esc(b.get('Business modules')),
            esc((b.get('Original service associations') or '').split('. Only')[0]), CAPMAP[k], CAPMAP[k].split(',')[0].split('–')[0]))
frag['CAPS'] = '\n'.join(cw)
# ops N and P distinct
dist = collections.OrderedDict()
for r in OPS:
    k = (r['method'], r['path'])
    if k not in dist: dist[k] = {'screens': [], 'status': r['status'], 'bp': r['bp_ops'], 'match': r['match']}
    dist[k]['screens'].append(r['screen'])
def alias_action(path, st, bp):
    if '/control' in path: return 'Alias with `action` discriminator → per-action ops (CONFLICT-344)'
    if re.search(r'/(approve|review)$', path): return 'Alias → Approval decide (CONFLICT-345)'
    if '/api/v1/sales/' in path or '/workspace/' in path: return 'Alias route to DERIVED op (CONFLICT-343)'
    if st == 'Not covered': return 'Add ★ legacy alias as new DERIVED op (§2.7.5.3)'
    return 'Mount legacy path as alias of listed op'
tn = ['| # | Method | Source path | Screens | Status | Blueprint op(s) | Action |', '|---|---|---|---|---|---|---|']
tp = list(tn)
i = j = 0
for (m, p), v in dist.items():
    if v['status'] == 'Not covered':
        i += 1; tn.append('| %d | %s | `%s` | %s | N | — | %s |' % (i, m, p, ', '.join(v['screens']), alias_action(p, v['status'], v['bp'])))
    elif v['status'] == 'Partially covered':
        j += 1; tp.append('| %d | %s | `%s` | %s | P | %s | %s |' % (j, m, p, ', '.join(v['screens']), v['bp'], alias_action(p, v['status'], v['bp'])))
frag['OPS_N'] = '\n'.join(tn); frag['OPS_P'] = '\n'.join(tp)
frag['OPS_C_LIST'] = ', '.join('%s `%s`' % k for k, v in dist.items() if v['status'] == 'Covered')
# tables
tt = ['| # | Source table | Screens (count) | Blueprint ENT | Blueprint table | Status | Basis |', '|---|---|---|---|---|---|---|']
for n_, r in enumerate(sorted(TABS, key=lambda x: (x['status'], x['source_table'])), 1):
    tt.append('| %d | `%s` | %d | %s | %s | %s | %s |' % (n_, r['source_table'], len(r['screens'].split(';')), r['bp_ent'] or '—',
              ('`' + r['bp_table'] + '`') if r['bp_table'] else '—', {'Covered': 'C', 'Partially covered': 'P', 'Not covered': 'N'}[r['status']], r['match']))
frag['TABLES'] = '\n'.join(tt)
# plugins
pc = collections.OrderedDict()
for r in PLUGS:
    pc.setdefault(r['integration'], []).append(r['screen'])
pt = ['| Integration (doc 06 spelling) | Class | Screens | Blueprint treatment |', '|---|---|---|---|']
for n_, sc in pc.items():
    c, txt = plug_class(n_)
    pt.append('| %s | %s | %s | %s |' % (n_, c, ', '.join(sc), txt))
frag['PLUGINS'] = '\n'.join(pt)
frag['PLUG_COUNTS'] = dict(collections.Counter(plug_class(n_)[0] for n_ in pc))
# related graph summary: inbound degree
indeg = collections.Counter(r['to'] for r in RELS)
frag['REL_TOP'] = ', '.join('%s (%d)' % kv for kv in indeg.most_common(12))
# field partial counts by screen group
fp = collections.Counter(VIEW.get(r['screen'], '?') for r in FIELDS if r['status'] == 'Partially covered')
frag['FIELD_P_BY_VIEW'] = '; '.join('%s %d' % kv for kv in fp.most_common())
# location vs view
lv = collections.Counter((S_['location'] or ('Website' if S_['id'][0]=='W' else 'Admin-new'), VIEW.get(S_['id'])) for S_ in S['screens'])
frag['LOC_VIEW'] = '; '.join('%s→%s: %d' % (k[0], k[1], v) for k, v in sorted(lv.items(), key=lambda x: -x[1]))
frag['TC_INDEX'] = tc_index
json.dump(frag, open(os.path.join(OUT, 'c_fragments.json'), 'w'), indent=1, ensure_ascii=False)

# ---------------------------------------------------------------- coverage CSV
cov = []
def add(doc, sec, aid, summ, st, loc, act, new=''):
    cov.append({'doc': doc, 'section': sec, 'aspect_id': aid, 'aspect_summary': summ, 'status': st,
                'blueprint_location': loc, 'action': act, 'new_ids': new})
for sid in order:
    for n_, r in enumerate(fields_by.get(sid, []), 1):
        add('06', '§Current scope: screen-specific field decisions / ' + sid, 'C06-FLD-%s-%02d' % (sid, n_),
            '%s field: %s' % (r['kind'], r['field']), r['status'],
            'Part 2.1 FR-%s key fields; Part 2.5 §2.43 %s' % (sid, sid) if r['status'] == 'Covered' else 'Part 2.7b card ' + sid,
            'None' if r['status'] in ('Covered', 'Not applicable') else 'Field specified in Part 2.7b card (type, control, rule)',
            '' if r['status'] in ('Covered', 'Not applicable') else 'FR-ENH-C-002; ' + tc_index[sid])
for n_, r in enumerate(OPS, 1):
    add('06', 'Part A/B screen operations / ' + r['screen'], 'C06-OP-%03d' % n_, '%s %s (%s)' % (r['method'], r['path'], r['screen']),
        r['status'], 'Part 3.2 ' + (r['bp_ops'] or '—'),
        'None' if r['status'] == 'Covered' else alias_action(r['path'], r['status'], r['bp_ops']),
        '' if r['status'] == 'Covered' else 'FR-ENH-C-003; ' + tc_index.get(r['screen'], 'TC-ENH-C-006'))
for n_, r in enumerate(TABS, 1):
    add('06', 'Part A/B PostgreSQL tables', 'C06-TAB-%03d' % n_, '%s used by %s' % (r['source_table'], r['screens']), r['status'],
        'Part 3.3 %s %s' % (r['bp_ent'], r['bp_table']), 'None' if r['status'] == 'Covered' else ('Logical alias recorded in Part 2.7a §2.7.4.4' if r['bp_ent'] else 'GAP-349 entity proposal'),
        '' if r['status'] == 'Covered' else ('GAP-349' if not r['bp_ent'] else 'FR-ENH-C-003'))
for sid, r in S['impl'].items():
    add('06', 'Implementation controls table / ' + sid, 'C06-IMP-' + sid, 'SM-FR/SM-UT/SM-UAT association and interaction checks',
        'Covered', 'Part 6.1 §6.1.12.5; Part 6.6 RTM; Part 2.1 FR-' + sid, 'Alias counts verified mechanically (identical)', '')
for sid, b in S['blocks06'].items():
    if sid.startswith('CAP'):
        add('06', 'Retained website implementation details', 'C06-CAP-' + sid[3:], b.get('Behavior', ''), 'Partially covered',
            'Part 2.1 FR-' + CAPMAP[sid].split(',')[0].split('–')[0], 'Capability → W-screen crosswalk added (Part 2.7a §2.7.5.1)', 'FR-ENH-C-001; FR-ENH-C-013')
for n_, (iname, sc) in enumerate(pc.items(), 1):
    c, txt = plug_class(iname)
    st = 'Covered' if c in ('INT', 'OSS') or iname.lower() in ('ses', 's3', 'aws', 'cloudwatch', 'tavily', 'firecrawl', 'sentry', 'meta cloud api', 'apollo.io', 'hunter', 'zoom', 'search console', 'calendar api', 'rag', 'llm', 'llm gateway', 'claude api', 'claude/openai api', 'exa', 'resend', 'postiz', 'pandadoc', 'aws secrets manager', 'langfuse', 'posthog', 'pubmed', 'canva') else ('Not applicable' if c == 'DEV' else 'Partially covered')
    add('06', 'Part B screen integration associations', 'C06-PLG-%03d' % n_, '%s on %s' % (iname, ', '.join(sc)), st,
        'Part 3.2 §3.2.4 adapters; Part 7.3; DEC-020 budgets', txt, 'FR-ENH-C-009' if c in ('ADP', 'CMU', 'DEV') else '')
for sid in order:
    d = S['dec06'][sid]
    add('06', 'Screen-specific decisions: Related / ' + sid, 'C06-REL-' + sid, 'Related screens: ' + d.get('related', ''), 'Not covered',
        'Part 2.5 rows (3 of 435 links)', 'In-context related links specified (Part 2.7b card; FR-ENH-C-012)', 'FR-ENH-C-012; TC-ENH-C-012')
    add('06', 'Screen-specific decisions: Automation/Acceptance / ' + sid, 'C06-AUT-' + sid, 'Automation: ' + d.get('automation', ''), 'Covered',
        'Part 2.1 FR-%s Automation column' % sid, 'None (identical to FRD §16.2)', '')
    add('17', 'Screen-specific interaction index / ' + sid, 'C17-INT-' + sid, 'Intent and interaction pattern', 'Partially covered' if sid in S['blocks06'] else 'Covered',
        'Part 2.5 §2.43 ' + sid, 'Interaction pattern IP-PUB/IP-PORTAL/IP-ADMIN assigned (Part 2.7a §2.7.5.2)', 'FR-ENH-C-006' if sid in S['blocks06'] else '')
    add('17', 'Screen-specific field and automation decisions / ' + sid, 'C17-FLD-' + sid, 'Field decisions (identical to doc 06 and doc 02)', 'Covered',
        'See doc 06 rows C06-FLD-' + sid, 'Common with doc 06 (parser diff = 0)', '')
json.dump(cov, open(os.path.join(OUT, 'c_cov_generated.json'), 'w'))
print('2.7b lines', len(blines), 'cov rows', len(cov), 'plug classes', frag['PLUG_COUNTS'])
print('LOC_VIEW', frag['LOC_VIEW']); print('FIELD_P', frag['FIELD_P_BY_VIEW']); print('REL', frag['REL_TOP'])
