"""Part 11.8 (Group H) build: parse V12 API/integration/plugin material, reconcile with the blueprint,
write final/coverage_v12/H_coverage.csv and Markdown fragments, then expand {{PLACEHOLDERS}} in the
Part 11.8 templates into the final Part files.
Usage: python3 -I h_build.py <scratch_dir>
<scratch_dir> must hold hc/v12_ops.csv (h_parse_openapi.py), hc/bp_ops.csv (h_blueprint_ops.py) and the compacted
chapters hc/25_*.txt, hc/27_*.txt, hc/28_*.txt (h_compact.py)."""
import csv, json, re, sys, os, glob, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from h_data import NEW_OPS, V8, PREFIXED, CAND, A2

S = sys.argv[1]
B = '/home/user/Allinonecalculator/blueprint/'
V = S + '/v12/'
E = V + 'src/engineering/engineering/'
OUT = B + 'assembly/v12/h_fragments/'
os.makedirs(OUT, exist_ok=True)
os.makedirs(B + 'final/coverage_v12', exist_ok=True)

ops = list(csv.DictReader(open(S + '/hc/v12_ops.csv')))
bp = {r['id']: r for r in csv.DictReader(open(S + '/hc/bp_ops.csv'))}
dm = list(csv.DictReader(open(B + 'final/coverage/D_api_mapping.csv')))
F = list(csv.DictReader(open(B + 'final/coverage/F_integration_candidates.csv')))
hist = {(r['method'], r['path']): r for r in dm if r['source_id'].startswith('SM-OP')}
ux = [r for r in dm if r['source_id'].startswith('SM-UX')]
newids = {o['id'] for o in NEW_OPS}

def check_ids(s):
    for t in re.findall(r'API-(?:ENH-D-\d{3}|ADV-X1-\d{2}|V12-H-\d{3}|\d{3})', s):
        assert t in bp or t in newids, 'unknown op id ' + t
for d in (V8, A2):
    for v in d.values(): check_ids(v[0] + ' ' + v[3])
for c in CAND: check_ids(c[4] + ' ' + c[7])

def esc(s): return str(s).replace('|', '\\|').replace('\n', ' ')
def bpops(r):
    s = (r['blueprint_ops'] or '').replace(',', ';').strip()
    if r.get('enhancement') and r['enhancement'] not in s:
        s = (s + '; ' if s else '') + r['enhancement']
    return s or '—'
def relname(r):
    return {'none': 'New (Part 3.5b)'}.get(r['relation'], r['relation'].capitalize())

rows = []  # coverage rows
def add(doc, chap, sec, aid, summ, sb, loc, action, new, sa='Matched'):
    rows.append(dict(doc=doc, chapter=chap, section=sec, aspect_id=aid, aspect_summary=summ, status_before=sb,
                     blueprint_location=loc, action=action, new_ids=new, status_after=sa))

PEND = 'Pending Founder decision'
# ------------------------------------------------------------------ FSD 25 -------------------------------------------
c25 = open(S + '/hc/25_REST_API_Event_Contract_Master.txt').read().split('\n')
ent = [l for l in c25 if re.match(r'\s+R: ENT-API-\d\d ', l)]
ENT_MAP = {
 'ENT-API-01': ('Partially covered', 'Part 9.9a CAP-X3-23, ADR-138 (A3 Year 2 proposal only)', 'API-V12-H-001…004; FR-V12-H-001; ADR-205; R1 phase', PEND),
 'ENT-API-02': ('Partially covered', 'Part 9.9a ADR-138 (client-credentials apps, A3 proposal)', 'API-V12-H-005…008; FR-V12-H-002; ADR-205', 'Matched'),
 'ENT-API-03': ('Partially covered', 'Part 3.2 §3.2.1.7 (per user/tenant/IP; no per-key class)', 'RL-KEY class; FR-V12-H-003; R1 phase', PEND),
 'ENT-API-04': ('Conflict', 'Part 3.2 §3.2.1.3 (≥ 6 months public/portal; ≥ 1 release Admin)', 'DEC-646 amends to ≥ 12 months; FR-V12-H-004', 'Matched'),
 'ENT-API-05': ('Conflict', 'Part 3.2 §3.2.1.13 ("Outbound webhooks to tenants: Not offered in W0–W6"); Part 9.9a CAP-X3-23', 'API-V12-H-009…014; ADR-206; DEC-645; FR-V12-H-005; R1 phase', PEND),
 'ENT-API-06': ('Partially covered', 'Part 3.2 §3.2.1.14 (TypeScript clients only); CAP-X3-23 (TS, Python)', 'FR-V12-H-006; RECOMMENDATION-903 (Java at R3)', 'Matched'),
 'ENT-API-07': ('Partially covered', 'Part 3.2 §3.2.1.14 (docs); CAP-X3-23 sandbox tenant', 'FR-V12-H-007; developer portal W39 from Appendix A/A2', 'Matched'),
}
for l in ent:
    c = [x.strip() for x in l.split('R:', 1)[1].split('|')]
    sb, loc, new, sa = ENT_MAP[c[0]]
    add('FSD V12', '25', 'V12 Developer platform', 'H25-' + c[0], f'{c[0]} {c[1]} {c[2]} Acceptance: {c[3]} Phase {c[5]}; prototype {c[6]}', sb, loc, 'Adopted literally; see §11.8.5', new, sa)
add('FSD V12', '25', 'V12 Developer platform', 'H25-A2-STMT', 'Enterprise operations are in Appendix A2 (48 operations, OpenAPI 3.1, validated)', 'Not covered', '—', '48 A2 operations parsed and mapped (§11.8.4.3)', 'API-V12-H-001…048 (subset)', 'Matched')
add('FSD V12', '25', 'V10 Historical reconciliation', 'H25-REC-18', 'REC-18 P0: row-level source disposition index for APIs and entities; exact matches separate from semantic review; no unreviewed historical endpoint auto-deployed', 'Partially covered', 'Part 3.5a §3.5.4.2–3 (relation Exact/Alias/Split/Approval/Partial/New); D_api_mapping.csv', 'This part extends the index to Appendix A/A2 and all V12 candidates (H_coverage.csv relation column); DEC-640', 'DEC-640', 'Matched')
add('FSD V12', '25', 'V8 API convention', 'H25-V8-STMT', 'All routes use /api/v1 prefix (D5); 10 MT/OPT candidate routes normalised in place; complete proposed contract is Appendix A (282 operations, validated)', 'Partially covered', 'Part 3.2 §3.2.1.1 (legacy /api/v1 + ~/ derived)', '282 Appendix A operations parsed (§11.8.4.2); prefix rule kept; v2 namespace only for run gateway (DEC-647)', 'DEC-640, DEC-647', 'Matched')
for (m, p), v in V8.items():
    add('FSD V12', '25', 'V8 API convention and new operations', f'H25-V8 {m} {p}', f'{m} {p}', v[2], v[0], f'Relation {v[1]}', v[3] or '—', 'Matched')
add('FSD V12', '25', 'V7 MOB-16', 'H25-MOB-16', 'MOB-16 cross-device application handoff: SM-APPLICATION-6 envelope; canonical graph shared; fingerprint demo-only; production authenticated signed or server-owned request, replay protection, idempotent revision handling; no subscription activation during import; acceptance MOB-16-AT01', 'Partially covered', 'Part 3.2 API-503/504 (If-Match revision), API-ENH-D-019; §3.2.1.5 idempotency', 'Production handoff = server-owned application draft (API-504) read on the other device (API-ENH-D-019); DEC-658', 'DEC-658; TC-V12-H-090', 'Matched')
add('FSD V12', '25', 'V6 Universal architecture', 'H25-V6-AUTH', 'API contract authority: proposed routes require reconciliation with inherited inventory and code; avoid duplicate endpoints; enforce server authorization and version checks; proposals are not existing endpoints', 'Covered', 'Part 3.5a §3.5.4 (no duplicate mounting); Part 3.2 §3.2.1.12', 'Rule applied to every V12 operation here (DEC-640)', 'DEC-640', 'Matched')
add('FSD V12', '25', 'V6 MT-36', 'H25-MT-36', 'MT-36 P0: one authoritative registry with alias and migration map; physical schema constraints approved before deployment; MT-TC-MT-36 detect conflicting path/entity names; contract tests against versioned schemas', 'Partially covered', 'Part 3.2 §3.2.2 (catalogue), §3.2.5 contract tests; Part 3.5a mapping', 'Registry = Part 3.2 catalogue + x-v12-operation-id + x-v12-path + route-alias register RA-V12-H (§11.8.5.2); CI duplicate-path check', 'DEC-640; TC-V12-H-081', 'Matched')
for c in CAND:
    if c[0].startswith('MT-API'):
        add('FSD V12', '25', 'V6 MT candidate routes', 'H25-' + c[0], f'{c[0]} {c[1]} {c[2]} — {c[3]}', c[6], c[4], f'Relation {c[5]}', c[7] or '—', 'Matched')
add('FSD V12', '25', 'V5 optimization', 'H25-V5-STMT', 'Extend versioned DRF APIs rather than duplicate; scope derived from verified membership; server validates DTO version, role, resource, idempotency; safe error with correlation ID; map operation IDs at contract review', 'Covered', 'Part 3.2 §3.2.1.2, §3.2.1.5, §3.2.1.9, §3.2.1.12', 'Error envelope aligned to V12 Error schema (DEC-641)', 'DEC-641', 'Matched')
for c in CAND:
    if c[0].startswith('OPT-API'):
        add('FSD V12', '25', 'V5 OPT candidate operations', 'H25-' + c[0], f'{c[0]} {c[1]} {c[2]} — {c[3]}', c[6], c[4], f'Relation {c[5]}', c[7] or '—', 'Matched')
add('FSD V12', '25', 'V5 common run gateway', 'H25-RUNGW', 'Common run gateway resolves workflow access gaps without one endpoint per workflow; does not replace domain DTOs, adapter contracts or legacy routes; versioned; server-derived scope; cursor pagination, allowlisted filters, bounded payload; correlation ID; safe error {code,message,correlation_id,field_errors}', 'Not covered', 'Part 3.2 §3.2.1.11 (run resources; no generic start)', 'Run gateway v2 API-V12-H-068…072 (ADR-208, DEC-647); error envelope DEC-641', 'API-V12-H-068…072', 'Matched')
for c in CAND:
    if c[0].startswith('API-V2'):
        add('FSD V12', '25', 'V5 run gateway operations', 'H25-' + c[0], f'{c[0]} {c[1]} {c[2]} — {c[3]}', c[6], c[4], f'Relation {c[5]}', c[7] or '—', 'Matched')
add('FSD V12', '25', 'V5 historical registry', 'H25-HIST-STMT', 'Historical API registry: exact source operations retained as candidates; public site publication, startup listing, product publication or tenant-specific public lookup retired; explicit route review required', 'Covered', 'Part 3.5a §3.5.4.3, §3.5.4.6; Part 3.2 rule (3) public token routes', 'Confirmed: no tenant-specific public lookup route exists (public routes resolve by verified host only)', '—', 'Matched')
for r in dm:
    if not r['source_id'].startswith('SM-OP'): continue
    loc = f"Part 3.2/3.5 {bpops(r)} ({r['relation']}; Part 3.5 status {r['status']})"
    act = 'Closed in Part 3.5b by ' + r['enhancement'] if r['enhancement'] else 'Mapping retained (Part 3.5a)'
    add('FSD V12', '25', 'V5 historical registry rows', 'H25-' + r['sit_id'], f"{r['method']} {r['path']} — {r['purpose']} [{r['boundary']}]", 'Covered', loc, act, '—', 'Matched')
add('FSD V12', '25', 'V4 canonical additions', 'H25-V4-STMT', 'V4 names are candidate contracts; reconcile with DRF router, authentication and prior IDs; every response scoped, redacted and linked to correlation ID', 'Covered', 'Part 3.2 §3.2.1.4, §3.2.1.12', '—', '—', 'Matched')
for c in CAND:
    if c[0].startswith('V4-API'):
        add('FSD V12', '25', 'V4 canonical additions', 'H25-' + c[0], f'{c[1]} {c[2]} — {c[3]}', c[6], c[4], f'Relation {c[5]}', c[7] or '—', 'Matched')

# ------------------------------------------------------------------ FSD 27 -------------------------------------------
c27 = open(S + '/hc/27_External_Integrations_Provider_Adapters.txt').read().split('\n')
ENT_INT = {
 'ENT-INT-01': ('Partially covered', 'Part 3.2 §3.2.4.1 IP-01 port/adapter; §3.2.5 contract tests', 'Connector framework contract CF-01…12 (§11.8.5.7); API-V12-H-037/038; R1', PEND),
 'ENT-INT-02': ('Covered', 'Part 3.2 AD-12 Secrets Manager; §3.2.1.12 output rule; Part 4.1 secrets', 'Re-affirmed; DB inspection test TC-V12-H-085', 'Matched'),
 'ENT-INT-03': ('Covered', 'Part 3.2 §3.2.7 retry, breaker, bulkhead; IP-04 uncertain reconciliation', 'Per-connector limits added to CF-07', 'Matched'),
 'ENT-INT-04': ('Partially covered', 'Part 3.2 API-102 health; A008', 'API-V12-H-074 health summary with sync lag and alerts', 'Matched'),
 'ENT-INT-05': ('Partially covered', 'Part 7.4b procurement gate PG-01…PG-10; AD-19 OFF by default (W1 pilot if approved)', 'Activation gate CF-11 (security review, DPA, CJ-R15 transfer basis, DLT/WhatsApp registration); contact-data blocked until DEC-V9-04 (DEC-649); R1', PEND),
}
for l in c27:
    m = re.match(r'\s+R: (ENT-INT-\d\d) \| (.+)$', l)
    if m:
        c = [x.strip() for x in m.group(2).split('|')]
        sb, loc, new, sa = ENT_INT[m.group(1)]
        add('FSD V12', '27', 'V12 Connector catalogue', 'H27-' + m.group(1), f'{m.group(1)} {c[0]} {c[1]} Acceptance: {c[2]} Phase {c[4]}; {c[5]}', sb, loc, 'Adopted literally (§11.8.5.7)', new, sa)
INT = {
 'INT-01': ('Not covered', 'Native CRM (M21–M23); Part 7.4a capability 05 "Native PostgreSQL records"', 'AD-V12-H-01 CRM sync adapter (BYO credentials); RECOMMENDATION-902', PEND),
 'INT-02': ('Covered', 'AD-01 Amazon SES (+ Resend after approval, DEC-025)', 'SendGrid/Postmark accepted as "equivalent" alternates behind EmailPort (AD-V12-H-11)', 'Matched'),
 'INT-03': ('Covered', 'AD-02 Meta WhatsApp Cloud API', 'CJ-IN-08 opt-in rule cross-referenced', 'Matched'),
 'INT-04': ('Not covered', 'AD-02 fallback text "no SMS in W0–W5"', 'AD-V12-H-02 SMS India DLT aggregator; CONFLICT-888', PEND),
 'INT-05': ('Not covered', '—', 'AD-V12-H-03 Voice CPaaS (140/160 series pools); R3+ ', 'Matched'),
 'INT-06': ('Covered', 'AD-03 Google Calendar, AD-04 Microsoft Graph', '—', 'Matched'),
 'INT-07': ('Partially covered', 'AD-09 Meta/Google Ads (LinkedIn Ads not listed)', 'LinkedIn Marketing API added to AdsPort scope; CJ-GL-07 no health data to ads', 'Matched'),
 'INT-08': ('Covered', 'AD-11 Razorpay/Cashfree/PayU; Stripe internationally', 'Refunds recorded only (no AI-initiated refund)', 'Matched'),
 'INT-09': ('Partially covered', 'Part 9.9a CAP-X3-07 BYO-warehouse export (A3)', 'AD-V12-H-04 warehouse export adapter (BigQuery/Snowflake/Postgres), service account in vault', 'Matched'),
 'INT-10': ('Partially covered', 'DEC-019 shared IdP (OIDC); no per-tenant SAML/SCIM', 'AD-V12-H-05 enterprise IdP federation + SCIM (API-V12-H-015…028)', 'Matched'),
 'INT-11': ('Partially covered', 'AD-19 Apollo/Hunter OFF by default; B08 reserve', 'Blocked pending legal (DEC-V9-04, CJ-GL-01) — stricter than AD-19 W1 pilot (DEC-649)', 'Matched'),
}
for l in c27:
    m = re.match(r'\s+R: (INT-\d\d) \| (.+)$', l)
    if m:
        c = [x.strip() for x in m.group(2).split('|')]
        sb, loc, new, sa = INT[m.group(1)]
        add('FSD V12', '27', 'V12 Connector catalogue', 'H27-' + m.group(1), f'{m.group(1)} {c[0]}: {c[1]}; auth {c[2]}; {c[3]}', sb, loc, 'Adapter mapped (§11.8.5.8)', new, sa)
add('FSD V12', '27', 'V6 MT-22', 'H27-MT-22', 'MT-22 P0: company may have multiple channel accounts; offering-market mapping and independent eligibility; MT-TC-MT-22 Email and WhatsApp accounts for two markets preserved in handoff', 'Partially covered', 'Part 3.2 API-097, API-104 (sender identities per startup)', 'ChannelAccount gains market_ids/offering_ids; eligibility evaluated per account (CF-05)', 'FR-V12-H-024; TC-V12-H-086', 'Matched')
add('FSD V12', '27', 'V6 MT-23', 'H27-MT-23', 'MT-23 P0: scoped provider identity, credential reference and sender aliases; no credential secrets in HTML or public artifacts; MT-TC-MT-23 two senders under one channel; wrong-company account denied', 'Covered', 'Part 3.2 API-104/105 senders; AD-12; §3.2.1.12', 'Wrong-company denial test added', 'FR-V12-H-025; TC-V12-H-087', 'Matched')
add('FSD V12', '27', 'V5 GC-08', 'H27-GC-08', 'GC-08 P1 incremental provider sync: webhooks, cursors, ETags, change windows; reconcile gaps and provider reset; OPT-TC-GC-08 unchanged source no full fetch; missed event repaired without duplicates', 'Partially covered', 'Part 3.2 IP-05 scheduled reconciliation, §3.2.6', 'CF-08 sync contract (cursor/ETag/window, gap repair)', 'FR-V12-H-026; TC-V12-H-088', 'Matched')
add('FSD V12', '27', 'V5 SEC-04', 'H27-SEC-04', 'SEC-04 P0 short-lived scoped credentials: vault references, rotate and revoke; no credentials in logs or prompts; OPT-TC-SEC-04 expired/revoked token fails; seeded-secret log scan zero exposure', 'Covered', 'Part 3.2 AD-12, §3.2.4.3; Part 4.4a SEC-04', 'Re-affirmed for API keys, SCIM tokens, webhook secrets', 'FR-V12-H-019', 'Matched')
FAM = [('Search / licensed sources', 'AD-05/06/07 (rights, cache, source policy)', 'Partially covered', 'Benchmark coverage & freshness fields added (CF-12)'),
       ('Email', 'AD-01 (DKIM sender, SNS signature, bounce/complaint, X-GE-Message-Id)', 'Covered', '—'),
       ('WhatsApp / SMS / RCS', 'AD-02 (WhatsApp only)', 'Partially covered', 'SMS-DLT and RCS via AD-V12-H-02 with country/route policy'),
       ('Calendar / meetings', 'AD-03/04 (OAuth scopes, conflict check, client event ID)', 'Covered', 'Time-zone field explicit'),
       ('Paid ads / social', 'AD-08/09 (grant, approved payload, reconciliation)', 'Covered', '—'),
       ('Voice / media', '—', 'Not covered', 'AD-V12-H-03 (consent/recording rights, disclosure, quiet hours, asset licence)'),
       ('Payments / marketplace', 'AD-11 (signed events, amount/currency, dedupe, no card storage)', 'Partially covered', 'Marketplace (SVC-31) settlement events mapped to PaymentPort; reconciliation (CF-09)'),
       ('AI / embeddings', 'AD-13/14 (model/prompt version, data class, fallback)', 'Covered', 'DEC-418 routing retained')]
for i, (f, loc, sb, act) in enumerate(FAM, 1):
    add('FSD V12', '27', 'V5 adapter family contract', f'H27-FAM-{i:02d}', f'Adapter family {f}: required contract / selection gate', sb, 'Part 3.2 §3.2.4.2–3 ' + loc, act, 'CF-01…12', 'Matched')
add('FSD V12', '27', 'V5 provider shortlist', 'H27-SHORTLIST', 'Provider shortlist is capability-based, not a vendor commitment; API versions, fees, quotas, residency and rights verified before implementation; credentials in secret manager; OAuth rotation/revocation; no raw tokens in logs', 'Covered', 'Part 3.2 §3.2.4.2 [ASSUMPTION-108] verify rule; Part 7.4b PG gate', '—', '—', 'Matched')

# ------------------------------------------------------------------ FSD 28 -------------------------------------------
c28 = open(S + '/hc/28_Open_Source_Paid_Plugin_Optimization.txt').read().split('\n')
add('FSD V12', '28', 'V9 replacement register', 'H28-V9-STMT', 'Retained strategy; contact-data vendors "replace core; licensed data only" and additionally need transfer-register entry (CJ-R15), a DPA and CJ-GL-01 compliance before activation (DEC-V9-04); every candidate disabled until benchmark, licence, legal and budget evidence exist', 'Partially covered', 'Part 7.4a §7.4.4.2; Part 7.4b PG-01…PG-10; F_integration_candidates.csv activation_default', 'Contact-data activation conditions added to PG gate (DEC-649, FR-V12-H-033)', 'FR-V12-H-033', 'Matched')
MEAN = [('Replace', 'Implement reusable native/OSS adapter; benchmark'), ('Retain OSS', 'Pin version; verify licence, security and maintenance'),
        ('Conditional external service', 'Disabled until justified, legally authorized and budget-approved'), ('Defer / exclude', 'No installation, subscription or credential access')]
for i, (d, a) in enumerate(MEAN, 1):
    add('FSD V12', '28', 'V9 decision vocabulary', f'H28-DEC-{i}', f'Decision "{d}": default action {a}', 'Covered', 'Part 7.4a §7.4.4.2 decision vocabulary; Part 7.4b §7.4.5.8', '—', '—', 'Matched')
counts = [l for l in c28 if re.match(r'\s+R: [A-Z][^|]+\| \d+$', l)]
for l in counts:
    d, n = [x.strip() for x in l.split('R:', 1)[1].split('|')]
    add('FSD V12', '28', 'V9 decision counts', 'H28-CNT-' + d[:24].replace(' ', '_'), f'{d}: {n} candidates', 'Covered', 'F_integration_candidates.csv decision_doc21', 'Count re-verified programmatically (§11.8.4.6)', '—', 'Matched')
vnd = []
for l in c28:
    m = re.match(r'\s+R: (VND-\d+) \| (.+?) \| (.+?) \| (.+)$', l)
    if m: vnd.append(m.groups())
byname = {r['candidate'].strip().lower(): r for r in F}
vrows = []
for v in vnd:
    r = byname[v[1].strip().lower()]
    assert r['decision_doc21'].strip() == v[2].strip()
    cap = v[3].split(' — ')[0]
    pend = 'Matched'
    extra = ''
    if 'licensed data only' in v[2]: extra = '; contact-data activation conditions (CJ-R15, DPA, CJ-GL-01, DEC-V9-04)'
    if 'investor' in cap.lower(): extra = '; commercial market research only, investor use excluded (DEC-002, DEC-656)'
    add('FSD V12', '28', 'V9 paid plugin replacement register', 'H28-' + v[0], f'{v[0]} {v[1]}: {v[2]} — {v[3]}', 'Covered',
        f"Part 7.4a §7.4.4.2 IC-{r['no']}; {r['blueprint_adapter_or_module'] or '—'}; {r['blueprint_replacement_decision']}",
        f'VND ID adopted as canonical key of IC-{r["no"]}' + extra, v[0], pend)
    vrows.append((v, r, extra))
GC28 = [('GC-09', 'P0 provider shortlist rationalization: evaluate inherited 538 candidates on capabilities, licence, privacy, support, TCO, fallback; retain evidence; OPT-TC-GC-09 each release connector has approved shortlist decision and owner; redundant archived', 'Covered', 'Part 7.4a §7.4.4.2 (538 rows); Part 7.4b PG gate', 'Owner and release columns added to connector catalogue (FR-V12-H-027)', 'FR-V12-H-027'),
        ('GC-10', 'P1 bring-your-own-provider accounts: isolated credential references, allocated fees, permissions, support, revocation; OPT-TC-GC-10 BYO charges separate; revocation blocks calls', 'Partially covered', 'Part 9.9a (BYO-warehouse only)', 'Installation ownership platform|tenant_byo (API-V12-H-038); charge separation in usage ledger', 'FR-V12-H-028'),
        ('GC-11', 'P2 provider volume and tier planning: forecast usage; compare tiers, commitments, overages; OPT-TC-GC-11 includes unused commitments; purchasing approval', 'Not covered', '—', 'API-V12-H-076 tier scenarios (R3)', 'FR-V12-H-029'),
        ('GC-13', 'P1 self-service operations: setup checklist, connector diagnostics, knowledge troubleshooting with human escalation; OPT-TC-GC-13 setup without staff; unresolved to support', 'Partially covered', 'Part 8.3 help/support; API-102 health', 'API-V12-H-075 diagnostics', 'FR-V12-H-030'),
        ('GC-15', 'P1 idle resource detection: unused connectors, idle infrastructure, orphaned artifacts; safe cleanup with ownership review; OPT-TC-GC-15 idle flagged, active/retained not deleted automatically', 'Partially covered', 'Part 9.9a CAP-X3-21 FinOps findings (A3)', 'Idle-connector finding type pulled into R2 via API-V12-H-074 + FinOps findings; never auto-delete', 'FR-V12-H-031')]
for g, s, sb, loc, act, new in GC28:
    add('FSD V12', '28', 'V5 optimization controls', 'H28-' + g, f'{g} {s}', sb, loc, act, new, 'Matched')
add('FSD V12', '28', 'V5 closing statement', 'H28-538', '538 historical plugin candidates are research, not a procurement order; prefer native policy/billing/CRM/orchestration; OSS where licence and TCO approved; paid APIs where authorized data or provider access cannot be replaced; matched benchmark (coverage, accuracy, p95, reliability, licence, hosting/maintenance, fees); blocked until evidence', 'Covered', 'Part 7.4a §7.4.4.2–3; Part 7.4b §7.4.5.8; F_integration_candidates.csv (538 rows)', '—', '—', 'Matched')

# ------------------------------------------------------------------ Appendix A ---------------------------------------
A = [o for o in ops if o['src'] == 'A']
A2o = [o for o in ops if o['src'] == 'A2']
add('FSD V12', 'Appendix A', 'Header', 'HAA-HDR', 'OpenAPI 3.1 proposed contract: 282 operations on 251 paths; validated with openapi-spec-validator; not deployed; generated from workflow, screen, MT/OPT and V7 registers', 'Partially covered', 'Part 3.2 §3.2.1.14 (OpenAPI per namespace, drf-spectacular)', f'Parsed: {len(A)} operations on {len(set(o["path"] for o in A))} paths (h_parse_openapi.py)', 'DEC-640', 'Matched')
COMP = [('info.description', 'Scope derived server-side from verified membership; never from request fields', 'Covered', 'Part 3.2 §3.2.1.2 Scope row', '—'),
        ('servers', 'https://api.example.invalid placeholder', 'Not applicable', '—', 'Hosts per DEC-421 ingress table §11.8.5.10'),
        ('securitySchemes.bearerAuth', 'HTTP bearer, JWT; global security', 'Conflict', 'Part 3.2 §3.2.1.12 (no bearer tokens from browsers; DEC-019)', 'Two schemes: bffSession (browsers) + bearerAuth (integration surface) — DEC-643, CONFLICT-891'),
        ('parameters.cursor', 'cursor query string', 'Covered', 'Part 3.2 §3.2.1.6', '—'),
        ('parameters.limit', 'limit integer 1..200, default 50', 'Conflict', 'Part 3.2 §3.2.1.6 (default 25, max 100)', 'V12 adopted: default 50, max 200 (DEC-641)'),
        ('responses.Error', 'Safe error response', 'Covered', 'Part 3.2 §3.2.1.9', '—'),
        ('schemas.Error', 'required code, message, correlation_id; field_errors map', 'Partially covered', 'Part 3.2 §3.2.1.9 problem+json (code, detail, correlation_id, errors[])', 'Superset envelope adds message and field_errors (DEC-641)'),
        ('schemas.Page', 'items[] of Record; next_cursor string|null', 'Conflict', 'Part 3.2 §3.2.1.6 {data, page.next_cursor}', 'V12 adopted: {items, next_cursor} (+ optional meta) (DEC-641)'),
        ('schemas.Record', 'id uuid, version ≥ 1, status, payload, updated_at', 'Partially covered', 'Part 3.2 §3.2.1.8 revision + ETag', 'Wire field `version` = revision (DEC-641)'),
        ('schemas.Command', 'expected_version ≥ 0, payload, reason ≤ 2000', 'Partially covered', 'Part 3.2 If-Match header', 'expected_version accepted; must equal If-Match when both sent (DEC-641)'),
        ('schemas.RunRequest', 'workflow_id ^SM-SVC-\\d{2}-WF0[1-4]$, workflow_version, business_context, input (urn:sm:dto:<wf>:v2), dry_run', 'Not covered', '—', 'API-V12-H-068 (DEC-647)'),
        ('schemas.BusinessContext', 'company_id, offering_id, market_id required; division, brand, channel_account, campaign', 'Partially covered', 'Part 3.2 scope from session', 'BusinessContext validated against session scope; never authorizes (DEC-647)'),
        ('schemas.PreflightRequest', 'market IN/EU/UK/US; channel Email/SMS/Voice/WhatsApp/Social/Web; purpose Promotional/Service; contact_id; send_at_local; template_id; ai_generated; ai_disclosed', 'Partially covered', 'Part 3.2 API-068 eligibility check', 'PreflightRequest adopted as API-068 DTO (§11.8.5.3)'),
        ('schemas.PreflightResult', 'verdict ALLOW/HOLD/REVIEW; reasons[rule_id, effect, message]; pack_versions', 'Partially covered', 'Part 3.2 API-068 (rule IDs)', 'PreflightResult adopted (§11.8.5.3)'),
        ('x-idempotency', 'Idempotency-Key header required on every POST/PUT/PATCH command', 'Covered', 'Part 3.2 §3.2.1.5', '—'),
        ('response codes', 'Reads 200/304/400/403/404/409; commands 200/202/400/403/404/409', 'Partially covered', 'Part 3.2 §3.2.1.10 (adds 401, 413, 415, 429, 503)', 'Blueprint superset retained; 422 added (DEC-642)'),
        ('tags', 'SM-SVC-## (workflow usage), Screens, AI, Compliance', 'Not covered', '—', 'x-v12-tag kept on every operation; service/workflow traceability (DEC-640)'),
        ('security: []', '2 public operations (cookie consent, DSAR intake)', 'Covered', 'Part 3.2 public namespace', '—')]
for i, (k, s, sb, loc, act) in enumerate(COMP, 1):
    sa = 'Not applicable (placeholder host; real hosts in §11.8.5.10)' if sb == 'Not applicable' else 'Matched'
    add('FSD V12', 'Appendix A', 'Components and conventions', f'HAA-C{i:02d}', f'{k}: {s}', sb, loc, act, re.findall(r'DEC-\d+', act) and ';'.join(re.findall(r'DEC-\d+', act)) or '—', sa)

def norm(p): return re.sub(r'\{[^}]+\}', '{id}', p)
histn = {(r["method"], norm(r["path"])): r for r in dm}
amap = []
for i, o in enumerate(A, 1):
    k = (o['method'], o['path'])
    if k in V8:
        v = V8[k]; bpo, rel, sb, new = v; src = 'V8'
    elif k in PREFIXED:
        r = hist[PREFIXED[k]]; bpo, rel, sb, new = bpops(r), 'Alias (prefix)', 'Covered', ''; src = r['source_id']
    else:
        r = histn[(o['method'], norm(o['path']))]; bpo, rel, sb, new = bpops(r), relname(r), 'Covered', ''; src = r['source_id']
    amap.append((i, o, src, bpo, rel, sb, new))
    add('FSD V12', 'Appendix A', 'Operations', f'HAA-{o["operationId"]}', f'{o["method"]} {o["path"]} [{o["tags"]}] {o["summary"]}; request {o["request"] or "—"}; response {o["response"]}; codes {o["codes"]}', sb, bpo, f'Relation {rel}; x-v12-operation-id={o["operationId"]}; conventions DEC-641/642', new or '—', 'Matched')
for i, o in enumerate(A2o, 1):
    v = A2[(o['method'], o['path'])]
    add('FSD V12', 'Appendix A2', 'Enterprise operations', f'HA2-{o["operationId"]}', f'{o["method"]} {o["path"]} [{o["tags"]}] {o["summary"]}', v[2], v[0], f'Relation {v[1]}', v[3] or '—', 'Matched')
add('FSD V12', 'Appendix A2', 'Header', 'HA2-HDR', '48 operations on 33 paths; validated; SCIM endpoints follow RFC 7643/7644 resource shapes', 'Not covered', '—', f'Parsed {len(A2o)} operations on {len(set(o["path"] for o in A2o))} paths; SCIM served at /scim/v2 on the developer host (ADR-207)', 'ADR-207', 'Matched')

# ------------------------------------------------------------------ Engineering files --------------------------------
cat = json.load(open(E + 'api_catalog.json'))
def oas(f):
    d = json.load(open(f)); return [(m.upper(), p) for p, it in d['paths'].items() for m in it if m in ('get', 'post', 'put', 'patch', 'delete')]
clo = oas(E + 'closure/openapi_closure_candidate.json'); sta = oas(E + 'starter/openapi_catalog_draft.json'); uio = oas(E + 'ui_upgrade/candidate_openapi.json')
fp = list(csv.DictReader(open(E + 'api_field_proposals.csv', encoding='utf-8-sig')))
cr = list(csv.DictReader(open(E + 'api_contract_review.csv', encoding='utf-8-sig')))
pr = list(csv.DictReader(open(E + 'starter/api_payload_review.csv', encoding='utf-8-sig')))
cc = list(csv.DictReader(open(E + 'closure/api_candidate_contracts.csv', encoding='utf-8-sig')))
histall = set(hist) | {(r['method'], r['path']) for r in ux}
eng = [('src/engineering/api_catalog.json', f'{len(cat)} operations (A–Y source columns incl. licence, quota, allocation)', len({(x["method"], x["path"]) for x in cat} - set(hist))),
       ('src/engineering/api_contract_review.csv', f'{len(cr)} rows; contract_status: ' + '; '.join(f'{k} {v}' for k, v in collections.Counter(r["contract_status"] for r in cr).items()), len({tuple(r['operation'].split(' ', 1)) for r in cr if not r['operation'].startswith('ADAPTER')} - set(hist))),
       ('src/engineering/api_field_proposals.csv', f'{len(fp)} field rows for {len(set(r["operation"] for r in fp))} operations (body {sum(r["location"]=="body" for r in fp)}, response {sum(r["location"]=="response" for r in fp)}, query {sum(r["location"]=="query" for r in fp)}, path {sum(r["location"]=="path" for r in fp)}); all approval Pending', len({tuple(r['operation'].split(' ', 1)) for r in fp} - set(hist))),
       ('src/engineering/closure/api_candidate_contracts.csv/.json', f'{len(cc)} decision rows (25 candidate DTOs, 8 provider bindings, 5 identity reuse) = SRC07-DEC-001…038', len({tuple(r['operation'].split(' ', 1)) for r in cc if not r['operation'].startswith('ADAPTER')} - histall)),
       ('src/engineering/closure/openapi_closure_candidate.json/.yaml', f'{len(clo)} operations on {len(set(p for _, p in clo))} paths; no component schemas', len(set(clo) - set(hist))),
       ('src/engineering/starter/openapi_catalog_draft.json/.yaml', f'{len(sta)} operations; identical operation set to the closure candidate', len(set(sta) - set(hist))),
       ('src/engineering/starter/api_payload_review.csv', f'{len(pr)} rows; source_typed No for all; reviews Pending', len({tuple(r['operation'].split(' ', 1)) for r in pr} - set(hist))),
       ('src/engineering/ui_upgrade/candidate_openapi.json', f'{len(uio)} operations = SM-UX-API-01…19', len(set(uio) - histall))]
for i, (f, s, extra) in enumerate(eng, 1):
    add('FSD V12 source archive', 'engineering', f, f'HENG-{i:02d}', s, 'Covered', 'Part 3.5a §3.5.4.3–4; Part 3.5b §3.5.5.3–4; D_api_mapping.csv', f'Verified: {extra} operations outside the reconciled 302 + 19 set', '—', 'Matched')
fpops = collections.defaultdict(collections.Counter)
for r in fp: fpops[r['operation']][r['location']] += 1
for op, cnt in sorted(fpops.items()):
    r = hist[tuple(op.split(' ', 1))]
    add('FSD V12 source archive', 'engineering', 'api_field_proposals.csv', 'HENG-FP ' + op, f'{op}: {sum(cnt.values())} proposed fields (' + ', '.join(f'{k} {v}' for k, v in sorted(cnt.items())) + ')', 'Covered', f'Part 3.5b §3.5.5.3 field contract for {bpops(r)}', 'Field-level contract retained; V12 conventions DEC-641', '—', 'Matched')
for r in ux:
    add('FSD V12 source archive', 'engineering', 'ui_upgrade candidate', 'HENG-' + r['source_id'], f"{r['method']} {r['path']} — {r['purpose']}", 'Covered', f"{bpops(r)} ({r['relation']})", 'Closed in Part 3.5b by ' + r['enhancement'] if r['enhancement'] else 'Mapping retained (Part 3.5a)', '—', 'Matched')

# ------------------------------------------------------------------ Events (derived) ---------------------------------
EVA = [('HEV-01', 'FSD 27 INT-02', 'ESP webhooks: send, bounce, complaint, unsubscribe', 'Covered', 'Part 3.2 §3.2.3.3 engagement.message.sent/.bounced/.complained; engagement.optout.received', '—'),
       ('HEV-02', 'FSD 25 ENT-API-05', 'Outbound signed webhook events to tenant endpoints (event catalogue for subscription)', 'Not covered', 'Part 3.2 §3.2.1.13 (not offered)', 'Outbound projection v1, 24 event types (§11.8.5.6)'),
       ('HEV-03', 'Appendix C2 webhook_delivery', 'Delivery record per attempt (1..6), status code, signed_at, delivered_at', 'Not covered', '—', 'developer.webhook_delivery.* events; API-V12-H-013'),
       ('HEV-04', 'FSD 25 API-V2-WEBHOOK', 'Connector provider events → accepted event receipt (signature/time/account mapping; duplicate safe)', 'Partially covered', 'ops.webhook.received; API-483', 'API-V12-H-073'),
       ('HEV-05', 'FSD 25 V8 incidents', 'Incident open starts clocks; authority/principal notification recorded', 'Partially covered', 'governance.compliance_incident.opened/.resolved', 'governance.compliance_incident.notification_recorded'),
       ('HEV-06', 'FSD 25 V8 consents', 'Consent withdrawal and suppression', 'Partially covered', 'governance.consent.recorded; engagement.optout.received', 'governance.consent.withdrawn'),
       ('HEV-07', 'FSD 25 V8 AI', 'Kill switch, promotion request, content screen flags', 'Not covered', 'ai.eval.gate_failed only', 'ai.kill_switch.activated/.released; ai.model.promotion_requested; ai.content.flagged'),
       ('HEV-08', 'Appendix A2 identity/SCIM/roles', 'SSO, domain, MFA policy, SCIM, custom role lifecycle', 'Not covered', 'identity.membership.changed; identity.session.revoked', 'identity.* and access.role.* events (§11.8.5.6)'),
       ('HEV-09', 'FSD 25 ENT-API-01/02', 'API key and OAuth client lifecycle', 'Not covered', '—', 'developer.api_key.*, developer.oauth_client.*'),
       ('HEV-10', 'FSD 27 ENT-INT-04/05', 'Connector installation gate and health', 'Not covered', '—', 'connector.installation.*, connector.health.*'),
       ('HEV-11', 'Appendix A2 data/ops/security', 'Sandbox, promotion, key change, SIEM sink, status publication, findings', 'Not covered', 'ops.incident.opened/.resolved', 'data.*, audit.siem_sink.*, ops.status.published, security.finding.*'),
       ('HEV-12', 'FSD 25 MT-API-10', 'Portfolio grant change audit', 'Not covered', 'identity.membership.changed', 'governance.portfolio_grant.changed')]
for aid, src, s, sb, loc, act in EVA:
    add('FSD V12 (derived event contract)', 'events', src, aid, s, sb, loc, act, 'Event catalogue §11.8.5.6', 'Matched')

# ------------------------------------------------------------------ write CSV ----------------------------------------
fn = ['doc', 'chapter', 'section', 'aspect_id', 'aspect_summary', 'status_before', 'blueprint_location', 'action', 'new_ids', 'status_after']
with open(B + 'final/coverage_v12/H_coverage.csv', 'w', newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=fn); w.writeheader(); w.writerows(rows)
ids = [r['aspect_id'] for r in rows]
dup = [k for k, v in collections.Counter(ids).items() if v > 1]
assert not dup, dup

# ------------------------------------------------------------------ fragments ----------------------------------------
frag = {}
def table(head, data):
    s = '| ' + ' | '.join(head) + ' |\n|' + '---|' * len(head) + '\n'
    for d in data: s += '| ' + ' | '.join(esc(x) for x in d) + ' |\n'
    return s
# counts
def cnt(filterf=lambda r: True):
    c = collections.Counter(r['status_before'] for r in rows if filterf(r)); a = collections.Counter(r['status_after'].split(' (')[0] for r in rows if filterf(r))
    return c, a
groups = [('FSD 25 REST API & Event Contract Master', lambda r: r['chapter'] == '25'), ('FSD 27 External Integrations', lambda r: r['chapter'] == '27'),
          ('FSD 28 Open-Source & Paid Plugin', lambda r: r['chapter'] == '28'), ('Appendix A OpenAPI 3.1', lambda r: r['chapter'] == 'Appendix A'),
          ('Appendix A2 Enterprise API', lambda r: r['chapter'] == 'Appendix A2'), ('Source archive engineering files', lambda r: r['chapter'] == 'engineering'),
          ('Derived event contract', lambda r: r['doc'].startswith('FSD V12 (derived'))]
sts = ['Covered', 'Partially covered', 'Not covered', 'Conflict', 'Not applicable']
data = []; tot = collections.Counter(); tota = collections.Counter()
for g, f_ in groups:
    c, a = cnt(f_); tot.update(c); tota.update(a)
    data.append([g, sum(c.values())] + [c.get(s, 0) for s in sts] + [a.get('Matched', 0), a.get(PEND, 0), a.get('Not applicable', 0)])
data.append(['**Total**', f'**{sum(tot.values())}**'] + [f'**{tot.get(s,0)}**' for s in sts] + [f'**{tota.get("Matched",0)}**', f'**{tota.get(PEND,0)}**', f'**{tota.get("Not applicable",0)}**'])
frag['COUNTS'] = table(['Material', 'Aspects', 'Covered', 'Partially covered', 'Not covered', 'Conflict', 'N/A', 'After: Matched', 'After: Pending Founder', 'After: N/A'], data)
frag['TOTAL_ASPECTS'] = str(len(rows))
frag['TOTAL_MATCHED'] = str(tota.get('Matched', 0)); frag['TOTAL_PENDING'] = str(tota.get(PEND, 0)); frag['TOTAL_NA'] = str(tota.get('Not applicable', 0))
frag['TOTAL_COVERED_BEFORE'] = str(tot.get('Covered', 0))
# detailed register of non-covered aspects
nc = [r for r in rows if r['status_before'] != 'Covered']
frag['REGISTER'] = table(['Aspect', 'Source', 'Summary', 'Status before', 'Blueprint location', 'Action / new IDs', 'Status after'],
                         [[r['aspect_id'], f"{r['doc']} {r['chapter']}", r['aspect_summary'][:260], r['status_before'], r['blueprint_location'], (r['action'] + ('; ' + r['new_ids'] if r['new_ids'] not in ('—', '') else ''))[:260], r['status_after']] for r in nc])
frag['REGISTER_COUNT'] = str(len(nc))
# Appendix A mapping
frag['APPX_A'] = table(['#', 'V12 operationId', 'Method', 'V12 path', 'V12 tag / summary', 'Source', 'Blueprint operation(s)', 'Relation', 'Before', 'Enhancement'],
                       [[i, o['operationId'], o['method'], '`' + o['path'] + '`', f"{o['tags']}: {o['summary']}", src, bpo, rel, sb, new or '—'] for i, o, src, bpo, rel, sb, new in amap])
relc = collections.Counter(x[4] for x in amap); sbc = collections.Counter(x[5] for x in amap); srcc = collections.Counter('V8 register' if x[2] == 'V8' else ('UX candidate (SM-UX-API)' if x[2].startswith('SM-UX') else 'Historical registry (SM-OP)') for x in amap)
frag['APPX_A_SUMMARY'] = table(['Dimension', 'Value', 'Operations'], [['Origin', k, v] for k, v in srcc.items()] + [['Relation', k, v] for k, v in sorted(relc.items())] + [['Status before', k, v] for k, v in sbc.items()] +
                               [['Method', k, v] for k, v in collections.Counter(o['method'] for o in A).items()] + [['Request schema', k or '(none: read)', v] for k, v in collections.Counter(o['request'] for o in A).items()] +
                               [['Response schema', k, v] for k, v in collections.Counter(o['response'] for o in A).items()] + [['Response-code set', k, v] for k, v in collections.Counter(o['codes'] for o in A).items()])
tagc = collections.Counter(o['tags'] for o in A)
frag['APPX_A_TAGS'] = ', '.join(f'{k} {v}' for k, v in sorted(tagc.items()))
inA = {(o['method'], norm(o['path'])) for o in A}
notinA = [r for r in dm if r['source_id'].startswith('SM-OP') and r['method'] != 'ADAPTER' and (r['method'], norm(r['path'])) not in inA and (r['method'], norm('/api/v1' + r['path'])) not in inA]
frag['HIST_NOT_IN_A'] = table(['Source op', 'Method', 'Path', 'Purpose', 'Blueprint op(s)'], [[r['source_id'], r['method'], '`' + r['path'] + '`', r['purpose'], bpops(r)] for r in notinA])
frag['HIST_NOT_IN_A_N'] = str(len(notinA))
frag['A2'] = table(['#', 'V12 operationId', 'Method', 'V12 path', 'Tag', 'Summary', 'Blueprint operation(s) before', 'Relation', 'Before', 'Blueprint operation after'],
                   [[i, o['operationId'], o['method'], '`' + o['path'] + '`', o['tags'], o['summary']] + list(A2[(o['method'], o['path'])][:3]) + [A2[(o['method'], o['path'])][3] or 'existing'] for i, o in enumerate(A2o, 1)])
frag['CAND'] = table(['V12 candidate', 'Method', 'Path', 'Result / contract', 'Blueprint operation(s)', 'Relation', 'Before', 'Enhancement'],
                     [[c[0], c[1], '`' + c[2] + '`', c[3], c[4], c[5], c[6], c[7] or '—'] for c in CAND])
frag['V8'] = table(['Method', 'V12 path', 'Blueprint operation(s)', 'Relation', 'Before', 'Enhancement'], [[k[0], '`' + k[1] + '`', v[0], v[1], v[2], v[3] or '—'] for k, v in V8.items()])
hrel = collections.Counter(r['relation'] for r in dm if r['source_id'].startswith('SM-OP')); hst = collections.Counter(r['status'] for r in dm if r['source_id'].startswith('SM-OP'))
frag['HIST_SUMMARY'] = table(['Relation (Part 3.5a)', 'Operations'], sorted(hrel.items())) + '\n' + table(['Part 3.5a status (before Part 3.5b enhancements)', 'Operations', 'Status for V12 (after Part 3.5b)'], [[k, v, 'Covered'] for k, v in hst.items()])
frag['ENG'] = table(['File', 'Parsed content', 'Operations outside reconciled set', 'Disposition'], [[f, s, x, 'Covered by Part 3.5a/3.5b; V12 conventions (DEC-641) apply'] for f, s, x in eng])
# VND
frag['VND'] = table(['VND', 'Candidate', 'V12 decision (= blueprint doc 21 decision)', 'Capability', 'Blueprint IC row', 'Blueprint replacement decision', 'Adapter / module', 'Activation default', 'Addition'],
                    [[v[0], v[1], v[2], v[3].split(' — ')[0], 'IC-' + r['no'], r['blueprint_replacement_decision'], r['blueprint_adapter_or_module'] or '—', (r['activation_default'] or '—')[:60], extra.lstrip('; ') or '—'] for v, r, extra in vrows])
vd = collections.Counter(v[2] for v, r, e in vrows)
frag['VND_COUNTS'] = table(['V12 decision', 'V12 count (stated)', 'Parsed VND rows', 'Blueprint rows with the same doc-21 decision (of 538)'],
                           [[k, k2, vd.get(k, 0), sum(1 for r in F if r['decision_doc21'] == k)] for k, k2 in [(l.split('R:', 1)[1].split('|')[0].strip(), l.split('|')[-1].strip()) for l in counts]])
# New ops
frag['NEWOPS'] = table(['Op ID', 'Method', 'Path', 'NS', 'Purpose', 'V12 source', 'FR / screen', 'Auth / roles', 'Idempotent', 'SE', 'PDP', 'RL class', 'V12 phase'],
                       [[o['id'], o['m'], '`' + o['p'] + '`', o['ns'], o['purpose'], o['src'], o['fr'], o['roles'], o['idem'], o['se'], o['pdp'], o['rl'], o['rel']] for o in NEW_OPS])
frag['NEWOPS_DETAIL'] = table(['Op ID', 'Request', 'Response', 'Business rules and authorization', 'Specific errors', 'Event emitted'],
                              [[o['id'], o['req'], o['resp'], o['rules'], o['err'], o['ev']] for o in NEW_OPS])
frag['NEWOPS_N'] = str(len(NEW_OPS))
frag['NEWOPS_BY_PHASE'] = ', '.join(f'{k} {v}' for k, v in sorted(collections.Counter(o['rel'] for o in NEW_OPS).items()))
frag['NEWOPS_BY_NS'] = ', '.join(f'{k} {v}' for k, v in sorted(collections.Counter(o['ns'] for o in NEW_OPS).items()))
# Tests per new op
NEG = {'R': 'out-of-scope object → 404; unknown filter → 400 FILTER_NOT_ALLOWED; API key without read scope → 403',
       'W': 'missing Idempotency-Key → 400; stale If-Match/expected_version → 409 STALE_REVISION; role without permission → 403',
       'A': 'requester approves own request → 403 SEPARATION_OF_DUTIES; changed payload after approval → 409 APPROVAL_VOIDED',
       'Q': 'duplicate key, same body → replayed 202; same key, different body → 409 IDEMPOTENCY_KEY_REUSED',
       'X': 'PDP deny at dispatch (emergency stop) → no external call; uncertain outcome blocks retry',
       'F': 'maker = checker → 403; missing evidence → 400', 'I': 'bad signature → 401 and payload discarded; duplicate event ID → 200 no effect'}
tcs = []
for i, o in enumerate(NEW_OPS, 1):
    tcs.append([f'TC-V12-H-{i:03d}', o['id'], f"{o['m']} {o['p']}", f"Authorized role succeeds with documented status ({o['resp'][:70]}…); audit row written", NEG.get(o['se'], ''), 'Contract (Schemathesis/OpenAPI) + API SIT', 'P0' if o['rel'] == 'R1' else 'P1'])
frag['TCS'] = table(['Test', 'Operation', 'Route', 'Positive assertion', 'Negative / security assertions', 'Level', 'Priority'], tcs)

# ------------------------------------------------------------------ expand templates ---------------------------------
for tpl in sorted(glob.glob(B + 'assembly/v12/h_templates/*.md')):
    t = open(tpl, encoding='utf-8').read()
    for k, v in frag.items(): t = t.replace('{{' + k + '}}', v)
    left = re.findall(r'\{\{[A-Z_0-9]+\}\}', t); assert not left, left
    open(B + os.path.basename(tpl), 'w', encoding='utf-8').write(t)
for k, v in frag.items(): open(OUT + k + '.md', 'w', encoding='utf-8').write(v)
print('aspects', len(rows), dict(tot), dict(tota), 'appxA', len(A), 'A2', len(A2o), 'new ops', len(NEW_OPS), 'hist not in A', len(notinA))
