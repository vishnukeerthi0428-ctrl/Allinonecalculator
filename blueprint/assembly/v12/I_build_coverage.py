"""Group I (Part 11.9) coverage builder: FSD V12 ch26, ch29, ch31, Appendix C/C2 DDL and src/engineering database files.
Run: python3 -I I_build_coverage.py  (needs the scratch PostgreSQL cluster with database v12 = Appendix C + C2).
Writes final/coverage_v12/I_coverage.csv and assembly/v12/i_ddl/I_stats.json."""
import csv, json, os, re, subprocess, sys, collections
BP = '/home/user/Allinonecalculator/blueprint'
SRC = '/tmp/claude-0/-home-user-Allinonecalculator/233b6551-af93-57f5-8f0b-015057ecee11/scratchpad/v12'
sys.path.insert(0, BP + '/assembly/v12/i_ddl')
from parse_tables import parse
PSQL = ['psql', '-h', '/tmp/pgv12', '-p', '55432', '-U', 'postgres', '-d', 'v12', '-At', '-F', '\t', '-c']
def q(sql): return [l.split('\t') for l in subprocess.run(PSQL + [sql], capture_output=True, text=True, check=True).stdout.rstrip('\n').split('\n') if l]
rows = []
def add(doc, ch, sec, aid, summ, sb, loc, action, new, sa='Matched'):
    rows.append(dict(doc=doc, chapter=ch, section=sec, aspect_id=aid, aspect_summary=summ[:400], status_before=sb, blueprint_location=loc, action=action, new_ids=new, status_after=sa))
bptext = ''.join(open(f'{BP}/{f}', encoding='utf-8').read() for f in ['Part-03-3_Data_Architecture.md', 'Part-03-6b_Source_Pack_Data_Catalog_Reconciliation.md', 'Part-09-9a_Advanced_Platform_Data_Security_Experience.md', 'Part-04-1_Security_and_Compliance.md'])
def bp_has(tok): return f'`{tok}`' in bptext
emap = {r['src_table']: r for r in csv.DictReader(open(f'{BP}/final/coverage/E_table_mapping.csv', encoding='utf-8'))}
ecov = list(csv.DictReader(open(f'{BP}/final/coverage/E_coverage.csv', encoding='utf-8')))
F = 'FSD V12'
# ------------------------------------------------------------------ chapter 26
t26, p26 = parse(f'{SRC}/FSD/26_PostgreSQL_Database_Schema_Master.txt')
ent_dat = {'ENT-DAT-01': ('Partially covered', 'Part 3.3 ENT-189 saas_export_job; Part 9.9 CAP-X3-07', 'export_job adopted: second approver CHECK (C2-T2), jsonl/csv/parquet, manifest hash, 7-day link CHECK (C3-04)', 'DEC-673, FR-V12-I-020, TC-V12-I-020', 'Matched'),
  'ENT-DAT-02': ('Partially covered', 'Part 9.9 CAP-X3-15 ten_tenant_key (AWS KMS, ap-south-1 only, ASSUMPTION-704)', 'Multi-cloud KEK adapters (AWS KMS, Azure Key Vault, GCP KMS), per-tenant DEKs, revocation crypto-shred trigger (C3-09)', 'DEC-671, ADR-213, CONFLICT-910, FR-V12-I-021, TC-V12-I-015', 'Matched'),
  'ENT-DAT-03': ('Conflict', 'DEC-421 Supabase Mumbai only; Part 11.5a CONFLICT-832', 'tenant.data_region fixed at onboarding + per-region database guard (C3-05); EU activation held', 'CONFLICT-832 (Part 11.5a), DEC-667, TC-V12-I-011/012', 'Pending Founder decision'),
  'ENT-DAT-04': ('Not covered', 'DEC-420 agent sandboxes synthetic only (build tooling, not tenant sandboxes)', 'sandbox_environment adopted with contains_personal_data=false CHECK; synthetic seed generator; reviewer promotion', 'DEC-674, FR-V12-I-022', 'Matched'),
  'ENT-DAT-05': ('Partially covered', 'Part 3.3 ENT-168 aut_config_revision (immutable approved revision)', 'config_promotion + configuration_revision (C3-11) with requester<>reviewer and immutability', 'DEC-674, FR-V12-I-022', 'Matched')}
for r in t26[0]['rows']:
    sb, loc, act, new, sa = ent_dat[r[0]]
    add(F, '26', 'V12 Data control', r[0], f'{r[0]} {r[1]} {r[2]} | Acceptance: {r[3]} | {r[4]}, {r[5]}, {r[6]}', sb, loc, act, new, sa)
for r in t26[1]['rows']:
    add(F, '26', 'V12 C2 tests', r[0], f'{r[0]}: {r[1]} -> {r[2]}', 'Not covered', 'No equivalent DB test in Part 3.3/6.x', 'Reproduced on PostgreSQL 16.15 (assembly/v12/i_ddl/v12_tests.out) and re-run on the C3 build (TC-V12-I-032)', 'TC-V12-I-032', 'Matched')
for r in t26[2]['rows']:
    loc = {'DB-T1': 'Part 3.3 §3.3.5.3 composite FK', 'DB-T2': 'Part 3.3 §3.3.9.6 unset-variable test (zero rows)', 'DB-T3': 'Part 3.3 §3.3.9.6 two-tenant fixture', 'DB-T4': 'Part 3.3 §3.3.9.2 WITH CHECK', 'DB-T5': 'Part 3.3 CK-13 maker<>checker', 'DB-T6': 'Part 3.1 PDP recheck at dispatch', 'DB-T7': 'Part 3.3 CK-16 (tier rows)', 'DB-T8': 'Part 3.3 UQ-IDEM-06/11', 'DB-T9': 'Part 3.3 §3.3.9.6'}[r[0]]
    sb = 'Conflict' if r[0] == 'DB-T2' else ('Partially covered' if r[0] in ('DB-T6', 'DB-T7') else 'Covered')
    add(F, '26', 'V8 DB tests', r[0], f'{r[0]}: {r[1]} -> {r[2]}', sb, loc, 'Reproduced (v12_tests.out); re-run on C3 build (c3_v12_regression.out)' + ('; missing context now raises an error (DEC-662)' if r[0] == 'DB-T2' else ''), 'TC-V12-I-032' + (', CONFLICT-909, DEC-662' if r[0] == 'DB-T2' else ''))
for pr in p26:
    txt = pr['text']; h = pr['heading']
    if txt.startswith('Common contract'): continue
    add(F, '26', h.split('>')[-1].strip()[:60], 'I-26-P-%03d' % (len([x for x in rows if x['aspect_id'].startswith('I-26-P')]) + 1), txt, 'Partially covered', 'Part 3.3 §3.3.5, §3.3.9; Part 3.6a', 'Adopted in Part 11.9 §11.9.5 (DDL-V12-I conventions)', 'DEC-661, DEC-662', 'Matched')
v6 = {'Tenant': ('Covered', 'ENT-001 ten_tenant'), 'Organization': ('Not covered', 'new (DEC-581 Part 11.5a; ten_organization)'), 'Company': ('Covered', 'ENT-002 ten_startup (company alias, DEC-581)'),
      'CompanyOperatingCountry': ('Not covered', 'new company_operating_country (C3-11)'), 'Division': ('Partially covered', 'ENT-003 ten_business_line'), 'Brand': ('Not covered', 'new ten_brand'),
      'Offering': ('Partially covered', 'ENT-016 cat_offering (+brand_id)'), 'Market': ('Not covered', 'new ten_market'), 'OfferingMarket': ('Not covered', 'new offering_market (C3-11)'),
      'ChannelAccount': ('Covered', 'ENT-089 eng_channel_account'), 'ChannelAccountMarket': ('Not covered', 'new channel_account_market (C3-11)'), 'WorkflowConfiguration': ('Not covered', 'new workflow_configuration (C3-11)'),
      'ConfigurationRevision': ('Partially covered', 'ENT-168 aut_config_revision (+C3-11 configuration_revision)'), 'PortfolioGrant': ('Partially covered', 'ten_membership_grant (Owner Portfolio)'),
      'BusinessEvent': ('Partially covered', 'ENT-124 mkt_attribution_event + ops_domain_event'), 'FXRate': ('Partially covered', 'ENT-198 ana_fx_snapshot')}
for r in t26[3]['rows']:
    sb, loc = v6[r[0]]
    add(F, '26', 'V6 entity graph', 'I-26-V6-' + r[0], f'{r[0]}: {r[1]} | {r[2]}', sb, loc, 'Full DDL in Appendix C or C3-11; mapping §11.9.4.2', 'DEC-660, FR-V12-I-010')
for mt in ['MT-09', 'MT-10', 'MT-11', 'MT-18', 'MT-33']:
    add(F, '26', 'V6 controlled requirements', mt, f'{mt} (requirement, acceptance MT-TC-{mt}, P0/P1, Data architecture)', 'Partially covered', 'Part 3.3 §3.3.4.1; Part 11.5a DEC-581', 'Hierarchy DDL with composite company-pinned FKs (C3-11) and scoped unique normalized names', 'DEC-660, FR-V12-I-010, TC-V12-I-030')
optmap = {'opt_usage_event': ('Covered', 'ENT-050 ai_usage, ENT-183 saas_usage_meter_reading'), 'opt_model_evaluation': ('Covered', 'ENT-048 ai_eval_run'), 'opt_scoped_cache': ('Covered', 'ai_semantic_cache (Part 7); Tier 0 exact cache'),
  'opt_step_checkpoint': ('Partially covered', 'ENT-163 aut_step_run'), 'opt_control_event': ('Covered', 'ENT-172 ops_audit_event, ENT-032 gov_policy_decision'), 'opt_sli_sample': ('Not covered', 'new sli_sample (C3-12)'),
  'opt_customer_value': ('Not covered', 'new customer_value (C3-12)'), 'opt_feedback_case': ('Partially covered', 'crm_survey_response; new feedback_case (C3-12)'), 'opt_journey_event': ('Partially covered', 'ENT-124 mkt_attribution_event; new journey_event (C3-12)')}
for r in t26[4]['rows']:
    sb, loc = optmap[r[0]]
    add(F, '26', 'V5 candidate entities', 'I-26-V5-' + r[0], f'{r[0]}: {r[1]} | {r[2]}', sb, loc, 'Mapped or created in C3-12', 'FR-V12-I-030')
dbv2 = {'DB-V2-RUN': 'ENT-162 aut_run / workflow_run', 'DB-V2-STEP': 'ENT-163 aut_step_run', 'DB-V2-ARTIFACT': 'generic domain shape + domain_schema_registry (C3-10)', 'DB-V2-EVIDENCE': 'ENT-059 intel_evidence',
  'DB-V2-EFFECT': 'effect (Appendix C) -> aut_effect', 'DB-V2-APPROVAL': 'ENT-034 gov_approval', 'DB-V2-USAGE': 'ENT-183 + usage_reservation (C3-12)', 'DB-V2-INBOX/OUTBOX': 'ENT-043/ENT-169', 'DB-V2-SUBSCRIPTION': 'ENT-182 saas_subscription', 'DB-V2-CONFIG': 'ENT-168 aut_config_revision'}
for r in t26[5]['rows']:
    add(F, '26', 'V5 proposed entities', r[0], f'{r[0]}: {r[1]}', 'Covered' if r[0] not in ('DB-V2-ARTIFACT', 'DB-V2-EFFECT', 'DB-V2-USAGE') else 'Partially covered', dbv2[r[0]], 'Mapped (§11.9.4.3)', 'DEC-661')
for t in t26[6:45]:
    svc = re.search(r'Domain schema (\w+) — (SM-SVC-\d\d)', t['heading'])
    for r in t['rows']:
        typed = bp_has(r[0])
        add(F, '26', f'Domain schema {svc.group(1)} {svc.group(2)}', f'I-26-DS-{svc.group(2)}-{r[0]}', f'{svc.group(1)}.{r[0]}: {r[1]}', 'Covered' if typed else 'Partially covered',
            'typed column of the same name in Part 3.3/3.6b' if typed else 'blueprint entity of the service (no column of this name)',
            'Validated in payload by domain_schema_registry (required keys, status vocabulary) and Appendix B JSON Schema; typed column where filterable', 'DEC-661, ADR-211, FR-V12-I-011')
for r in t26[45]['rows']:
    m = emap.get(r[0])
    add(F, '26', 'Historical entity (149)', 'I-26-HIST-' + r[0].replace(' ', '_'), f'{r[0]}: {r[1]}', 'Covered', f"{m['bp_ent']} {m['bp_table']} (Part 3.6a §3.6.4.3, match {m['match_type']})", 'Reconciled in Part 3.6a/b; V12 status line "candidate review schema only" kept as migration gate MT-36', '')
v4 = {'application': 'ENT-187 saas_application_draft', 'domain_record_version': 'new domain_record_version (C3-12)', 'usage_reservation': 'new usage_reservation (C3-12); ai_cost_ledger reserve', 'approval_decision': 'ENT-034 gov_approval', 'workflow_step_event': 'ENT-163 aut_step_run + ops_domain_event'}
for r in t26[46]['rows']:
    add(F, '26', 'Proposed V4 persistence additions', 'I-26-V4-' + r[0], f'{r[0]}: {r[1]} | {r[2]}', 'Partially covered' if 'new' in v4[r[0]] else 'Covered', v4[r[0]], 'Mapped or created (C3-12)', 'FR-V12-I-031')
# ------------------------------------------------------------------ Appendix C / C2 (catalogue of database v12)
core = {'tenant': 'ENT-001 ten_tenant', 'organization': 'new ten_organization (DEC-581)', 'company': 'ENT-002 ten_startup', 'division': 'ENT-003 ten_business_line', 'brand': 'new ten_brand', 'offering': 'ENT-016 cat_offering',
 'market': 'new ten_market', 'channel_account': 'ENT-089 eng_channel_account', 'workflow_run': 'ENT-162 aut_run', 'workflow_step_run': 'ENT-163 aut_step_run', 'effect': 'new aut_effect', 'outbox': 'ENT-169 ops_outbox',
 'inbox': 'ENT-043 int_provider_event', 'audit_event': 'ENT-172 ops_audit_event', 'portfolio_grant': 'ten_membership_grant', 'fx_rate': 'ENT-198 ana_fx_snapshot', 'jurisdiction_pack': 'new gov_jurisdiction_pack',
 'jurisdiction_rule': 'ENT-030 gov_jurisdiction_rule', 'consent_record': 'ENT-027 gov_consent', 'suppression': 'ENT-028 gov_suppression', 'dsar_request': 'ENT-036 gov_privacy_request', 'incident': 'ENT-039 gov_compliance_incident',
 'incident_notification': 'new gov_incident_notification', 'ai_model': 'new ai_model', 'prompt_version': 'ENT-045 ai_prompt_version', 'eval_suite': 'new ai_eval_suite', 'eval_run': 'ENT-048 ai_eval_run', 'ai_usage_event': 'ENT-050 ai_usage',
 'ai_budget': 'ENT-052 ai_budget', 'identity_provider': 'new sec_identity_provider', 'scim_token': 'new sec_scim_token', 'custom_role': 'ENT-007 ten_role', 'role_permission': 'new ten_role_permission', 'sod_conflict': 'new ref_sod_conflict',
 'api_key': 'saas_api_credential (Part 9.9)', 'webhook_endpoint': 'saas_webhook_subscription (Part 9.9)', 'webhook_delivery': 'saas_webhook_delivery (Part 9.9)', 'audit_sink': 'new ops_audit_sink', 'export_job': 'ENT-189 saas_export_job',
 'tenant_key_config': 'ten_tenant_key (Part 9.9)', 'sandbox_environment': 'new saas_sandbox_environment', 'config_promotion': 'new aut_config_promotion', 'connector_installation': 'ENT-040 int_integration', 'security_finding': 'new sec_security_finding',
 'ops_incident': 'ENT-176 ops_incident', 'tax_rule': 'ENT-022 cat_tax_profile', 'invoice': 'ENT-184 saas_service_invoice', 'locale_bundle': 'new ref_locale_bundle'}
tables = [r[0] for r in q("select c.relname from pg_class c where c.relnamespace='public'::regnamespace and c.relkind='r' order by c.oid")]
c2set = {'identity_provider','scim_token','custom_role','role_permission','sod_conflict','api_key','webhook_endpoint','webhook_delivery','audit_sink','export_job','tenant_key_config','sandbox_environment','config_promotion','connector_installation','security_finding','ops_incident','tax_rule','invoice','locale_bundle'}
std = {'tenant_id', 'company_id', 'id', 'created_at', 'updated_at', 'status', 'version', 'created_by'}
newcols = {'schema_ref', 'payload', 'evidence_refs'}
for t in tables:
    app = 'Appendix C2' if t in c2set else 'Appendix C'
    if t in core:
        loc = core[t]; sb = 'Not covered' if loc.startswith('new') else 'Partially covered'
    else:
        m = emap[t]; loc = f"{m['bp_ent']} {m['bp_table']}"; sb = 'Partially covered'
    add(F, app, 'Table', f'I-DDL-TBL-{t}', f'{app} table {t}', sb, loc, 'Adopted as canonical logical table; physical mapping §11.9.4; gaps fixed in DDL-V12-I (C3)', 'DEC-660, DEC-661')
for t, c, typ, nul, dflt in q("select table_name, column_name, data_type, is_nullable, coalesce(column_default,'') from information_schema.columns where table_schema='public' order by table_name, ordinal_position"):
    if t in core:
        newtab = core[t].startswith('new')
        sb = 'Not covered' if newtab else ('Covered' if (c in std or bp_has(c)) else 'Not covered')
        loc = core[t] + ('' if sb == 'Not covered' else f'.{c}')
    else:
        sb = 'Covered' if c in std - {'status', 'version'} else ('Partially covered' if c in ('status', 'version') else 'Not covered')
        loc = emap[t]['bp_table'] + ('.state / .revision' if c in ('status', 'version') else '')
    add(F, 'Appendix C2' if t in c2set else 'Appendix C', 'Column', f'I-DDL-COL-{t}.{c}', f'{t}.{c} {typ} {"NULL" if nul=="YES" else "NOT NULL"} {dflt}'.strip(), sb, loc,
        'Column adopted (DEC-661)' + ('; generic domain column added to typed table' if c in newcols else ''), 'DEC-661')
for con, t, typ, d in q("select conname, conrelid::regclass::text, contype::text, regexp_replace(pg_get_constraintdef(oid), '\s+', ' ', 'g') from pg_constraint where connamespace='public'::regnamespace order by 2,1"):
    kind = {'p': 'PK', 'f': 'FK', 'c': 'CHECK', 'u': 'UNIQUE'}[typ]
    weak = (t == 'role_permission' and kind in ('FK','PK')) or (t, kind) in (('webhook_delivery', 'FK'), ('config_promotion', 'FK'), ('inbox', 'PK'))
    add(F, 'Appendix C2' if t in c2set else 'Appendix C', 'Constraint', f'I-DDL-CON-{con}', f'{kind} {t}: {d}', 'Partially covered' if weak else ('Covered' if kind in ('PK', 'FK') else 'Partially covered'),
        (core.get(t) or emap[t]['bp_table']), 'Strengthened in C3-03 (tenant-pinned key)' if weak else 'Adopted', 'GAP-915, DEC-669' if weak else 'DEC-661')
for t, p, cmd in q("select tablename, policyname, cmd from pg_policies order by 1"):
    add(F, 'Appendix C2' if t in c2set else 'Appendix C', 'RLS policy', f'I-DDL-POL-{p}', f'{p} ON {t} FOR {cmd} USING/WITH CHECK tenant_id = current_setting(app.tenant_id)::uuid',
        'Partially covered', 'Part 3.3 §3.3.9 (tenant+startup, command-split)', 'Replaced by command-split tenant+company policies rls_<t>__select/insert/update (C3-13)', 'GAP-912, DEC-662, ADR-210')
for t in ['tenant', 'inbox', 'incident', 'portfolio_grant']:
    add(F, 'Appendix C', 'RLS gap', f'I-DDL-NORLS-{t}', f'{t} carries tenant_id but has no RLS in Appendix C', 'Not covered', 'Part 3.3 §3.3.9.6 CI guard', 'RLS + FORCE + policies added (C3-13); CI guard TC-V12-I-027', 'GAP-913')
add(F, 'Appendix C2', 'Trigger', 'I-DDL-TRG-role_permission_sod', 'enforce_sod() BEFORE INSERT on role_permission (ENT-ACC-02)', 'Partially covered', 'Part 2.3 SoD rules (application layer)', 'Extended to UPDATE and to user-level SoD (C3-06)', 'GAP-915, DEC-669, TC-V12-I-005/006')
for a, b in q("select permission_a, permission_b from sod_conflict"):
    add(F, 'Appendix C2', 'Seed', f'I-DDL-SEED-sod-{a}-{b}', f'sod_conflict seed ({a}, {b})', 'Covered', 'Part 2.3 BRL-APR maker-checker', 'Adopted; extra pairs RECOMMENDATION-920', 'DEC-669')
for e in ['pgcrypto', 'vector (pgvector, only when approved)']:
    add(F, 'Appendix C', 'Extension', f'I-DDL-EXT-{e.split()[0]}', f'CREATE EXTENSION {e}', 'Covered', 'Part 3.3 §3.3.5.1 extensions', 'Supabase: verify extension availability (as of 27 Nov 2026)', 'RECOMMENDATION-919')
for i, txt in enumerate(['App connects as non-owner app_user and sets SET LOCAL app.tenant_id / app.company_ids', 'Every tenant-scoped table has tenant_id; company-scoped tables add company_id with composite FK',
                         'Domain tables referenced by the 156 workflows use a common scoped shape; payload validated by Appendix B', 'Missing context fails closed: current_setting raises when app.tenant_id is unset',
                         'Appendix C2: apply after Appendix C; tested C2-T1..T11', 'Proposed DDL requires data-architecture approval before production migration (MT-36)'], 1):
    add(F, 'Appendix C', 'Convention', f'I-DDL-CONV-{i:02d}', txt, 'Partially covered' if i in (1, 3, 4) else 'Covered', 'Part 3.3 §3.3.5, §3.3.9', 'Adopted with C3 (company predicate actually enforced; ge_app = app_user = app_rw)', 'DEC-662, DEC-663')
for g in [('I-DDL-GAP-INDEX', '110 foreign keys without supporting index; 0 secondary indexes in Appendix C/C2', 'GAP-914'), ('I-DDL-GAP-GRANTS', 'No roles, grants or REVOKE in Appendix C/C2; audit and consent tables mutable', 'GAP-915'),
          ('I-DDL-GAP-ENUM', '109 status/state/type columns without CHECK vocabulary', 'GAP-915'), ('I-DDL-GAP-NULLSCOPE', 'Nullable tenant_id on outbox, inbox, portfolio_grant, incident', 'GAP-913'),
          ('I-DDL-GAP-VECTOR', 'growth_embedding has no vector column although pgvector is enabled', 'GAP-916'), ('I-DDL-GAP-SUPABASE', 'Supabase Data API roles (anon/authenticated) and service_role BYPASSRLS not addressed', 'CONFLICT-906')]:
    add(F, 'Appendix C/C2', 'Analysis finding', g[0], g[1], 'Not covered', 'assembly/v12/i_ddl/analyze_catalog.out', 'Fixed in DDL-V12-I (C3) and verified by TC-V12-I tests', g[2])
# ------------------------------------------------------------------ chapter 29
t29, p29 = parse(f'{SRC}/FSD/29_Analytics_Attribution_KPI_Engineering.txt')
add(F, '29', 'V10 reconciliation', 'REC-15', ' '.join(t29[0]['rows'][0]), 'Partially covered', 'Part 2.4 §2.31 (RPT-R rules); NFR-015 cursor', 'Drill-down contract: as-of timestamp, record count, unknown indicator, native currency; totals reconcile; bulk re-check (§11.9.5.11)', 'FR-V12-I-040, TC-V12-I-040')
for r in t29[1]['rows']:
    add(F, '29', 'V9 load profiles', r[0], f'{r[0]} {r[1]}: {r[2]} -> {r[3]}', 'Partially covered', 'Part 4.2 NFR-001..038 load tests LT-xx; DEC-031 design points', 'Adopted as binding performance acceptance profile (§11.9.5.12)', 'DEC-676, FR-V12-I-041')
for r in t29[2]['rows']:
    add(F, '29', 'V9 release KPIs', 'V12 ' + r[0], f'V12 {r[0]} {r[1]} {r[2]} ({r[3]})', 'Conflict', f'Blueprint {r[0]} has a different meaning (Part 1 KPI register)', 'Namespaced as "V12 KPI-nn" (DEC-665); target adopted; sli_sample + metric_definition rows (C3-12)', 'CONFLICT-907, DEC-665, MET-V12-I')
names = ['V6 event attribution', 'MT-13', 'MT-27', 'MT-31', 'V5 instrumentation', 'AT-14', 'CV-14', 'CS-12', 'Metric contract', 'V4 KPI mapping preamble']
for pr in p29:
    txt = pr['text']
    aid = 'I-29-P-%03d' % (len([x for x in rows if x['aspect_id'].startswith('I-29-P')]) + 1)
    m = re.match(r'^(MT-\d\d|AT-14|CV-14|CS-12)\b', txt)
    sb = 'Partially covered'
    add(F, '29', pr['heading'].split('>')[-1].strip()[:60], aid, txt, sb, 'Part 2.4 §2.31; Part 3.3 ENT-124, ENT-191..199; Part 9.9 CAP-X3-04', 'Specified in §11.9.5.11 (BusinessEvent fact, metric contract, attribution, consent-aware analytics)', 'DEC-672, ADR-214, FR-V12-I-042')
for r in t29[3]['rows']:
    add(F, '29', 'Fourteen management views', f'I-29-VIEW-{int(r[0]):02d}', f'View {r[0]} {r[1]}: {r[2]} ({r[3]})', 'Partially covered', 'Part 2.4 RP-01..30; Part 2.5 dashboards A087-A089', 'Each label mapped to a production metric with formula (§11.9.5.11 table) and "synthetic" labelling rule', 'FR-V12-I-043, MET-V12-I-01..56')
# ------------------------------------------------------------------ chapter 31
t31, p31 = parse(f'{SRC}/FSD/31_Cybersecurity_Privacy_Threat_Management.txt')
sec_loc = {'ENT-SEC-01': ('Covered', 'Part 4.1 §4.16.1 gates; Part 4.3 pipeline'), 'ENT-SEC-02': ('Partially covered', 'Part 4.1 SBOM (CycloneDX); Part 9.9 CAP-X3-19 (signing)'), 'ENT-SEC-03': ('Conflict', 'Part 4.1 §4.16.3 (Low = next maintenance)'),
           'ENT-SEC-04': ('Partially covered', 'Part 8.4 A7 two pen tests (R1, R2)'), 'ENT-SEC-05': ('Partially covered', 'Part 4.1 RECOMMENDATION-048 (bug bounty considered at W6)'), 'ENT-SEC-06': ('Covered', 'Part 4.1 §4.5'),
           'ENT-SEC-07': ('Covered', 'Part 4.1 §4.6; Part 9.9 CAP-X3-18'), 'ENT-SEC-08': ('Conflict', 'Part 4.3 out-of-hours paging Sev1 only (CONFLICT-113, DEC-044)')}
for r in t31[0]['rows']:
    sb, loc = sec_loc[r[0]]
    sa = 'Pending Founder decision' if r[0] == 'ENT-SEC-08' else 'Matched'
    new = {'ENT-SEC-03': 'CONFLICT-911, DEC-666', 'ENT-SEC-08': 'CONFLICT-905', 'ENT-SEC-05': 'DEC-675', 'ENT-SEC-04': 'DEC-675', 'ENT-SEC-02': 'DEC-675'}.get(r[0], 'FR-V12-I-050')
    add(F, '31', 'V12 security programme', r[0], f'{r[0]} {r[1]} {r[2]} | {r[3]} | {r[4]} {r[5]} {r[6]}', sb, loc, 'Specified in §11.9.5.13', new, sa)
for r in t31[1]['rows']:
    add(F, '31', 'V9 penetration-test plan', r[0], f'{r[0]} {r[1]}: {r[2]} | blocking: {r[3]}', 'Partially covered', 'Part 4.1 §4.16.2 pen-test scope', 'PEN-01..08 adopted as mandatory scope of every pen test; mapped to THR and TC (§11.9.5.13)', 'DEC-675, TC-V12-I-050..057')
for pr in p31:
    txt = pr['text']
    aid = 'I-31-P-%03d' % (len([x for x in rows if x['aspect_id'].startswith('I-31-P')]) + 1)
    if txt.startswith('Threats:'):
        for i, th in enumerate([x.strip() for x in txt.split('Controls:')[0].replace('Threats:', '').strip(' .').split(',')], 1):
            add(F, '31', 'V5 threats', f'I-31-THR-{i:02d}', 'Threat: ' + th, 'Covered', 'Part 4.1 §4.2 THR-001..082; Part 9.9 THR-X3', 'Mapped to STRIDE register §11.9.5.14', 'THR-V12-I')
        ctl = txt.split('Controls:')[1].split('. Test')[0]
        for i, c in enumerate([x.strip() for x in ctl.split(',')], 1):
            add(F, '31', 'V5 controls', f'I-31-CTL-{i:02d}', 'Control: ' + c, 'Covered', 'Part 4.1 §4.7 SC-01..50', 'Mapped §11.9.5.14', 'SC-V12-I')
        add(F, '31', 'V5 testing note', aid, 'Test OWASP-style API/browser risks and actual dependency vulnerabilities; legal and data processing approval per region; no compliance certification asserted', 'Covered', 'Part 4.1 §4.8, §4.12.10', 'Adopted', '')
        continue
    sb = 'Covered' if any(k in txt for k in ['CERT-In', 'GDPR Art. 32', 'Breach handling']) else 'Partially covered'
    add(F, '31', pr['heading'].split('>')[-1].strip()[:60], aid, txt, sb, 'Part 4.1 §4.10–4.12, §4.16; Part 9.9 CAP-X3-26 PWA', 'Specified in §11.9.5.13–11.9.5.15', 'DEC-675, FR-V12-I-051')
# ------------------------------------------------------------------ src/engineering database files
E = 'V12 src/engineering'
eng = f'{SRC}/src/engineering/engineering'
for r in csv.DictReader(open(f'{eng}/closure/database_confirmation_plan.csv', encoding='utf-8-sig')):
    add(E, 'closure', 'database_confirmation_plan.csv', f"I-ENG-CONF-{r['decision_id']}", f"V12-ENG {r['decision_id']} {r['source_key']}: {r['proposed_resolution']} [{r['status']}]", 'Conflict',
        'ID collides with blueprint DEC-039..042; content covered by Part 3.6a rows 001-003 and 010 (RECOMMENDATION-039 halfvec(1024), GAP-111)', 'Namespaced "V12-ENG DEC-nnn" (DEC-665); confirmation evidence = Django introspection + two-tenant test at Sprint 0', 'CONFLICT-907, DEC-665' + (', GAP-916' if r['decision_id'] == 'DEC-042' else ''))
for i, r in enumerate(csv.DictReader(open(f'{eng}/database_constraint_proposals.csv', encoding='utf-8-sig')), 1):
    m = emap.get(r['table'])
    add(E, 'engineering', 'database_constraint_proposals.csv', f'I-ENG-CONP-{i:02d}', f"{r['table']}: {r['constraint']} ({r['basis']}; {r['approval']})", 'Covered', f"{m['bp_ent']} {m['bp_table']} (Part 3.6a §3.6.4.7; composite (tenant_id, startup_id) FKs §3.3.5.3)", 'Adopted', '')
for r in csv.DictReader(open(f'{eng}/ui_upgrade/candidate_database_register.csv', encoding='utf-8-sig')):
    m = emap.get(r['entity'])
    add(E, 'ui_upgrade', 'candidate_database_register.csv', f"I-ENG-CAND-{r['entity']}", f"{r['entity']}: {r['purpose']} | {r['constraints']}", 'Covered', f"{m['bp_ent']} {m['bp_table']} (Part 3.6a)", 'Adopted', '')
for r in csv.DictReader(open(f'{eng}/database_contract_review.csv', encoding='utf-8-sig')):
    m = emap.get(r['entity'])
    add(E, 'engineering', 'database_contract_review.csv', 'I-ENG-CR-' + r['entity'].replace(' ', '_'), f"{r['entity']} [{r['exposure']}] {r['fields'][:150]} | {r['status']}", 'Covered', f"{m['bp_ent']} {m['bp_table']}; exposure class Part 3.6a §3.6.4.9", 'Status "Not started" becomes Sprint 0 migration task (MT-36 gate)', '')
sdr = {}
for x in ecov:
    if x['aspect_id'].startswith('08-SDR'): sdr[x['aspect_summary'].split(':')[0].strip()] = x
for i, r in enumerate(csv.DictReader(open(f'{eng}/database_field_resolution_proposals.csv', encoding='utf-8-sig')), 1):
    key = f"{r['entity']}.{r['field']}"
    x = next((v for k, v in sdr.items() if k.startswith(r['entity']) and r['field'] in v['aspect_summary']), None)
    add(E, 'engineering', 'database_field_resolution_proposals.csv', f'I-ENG-FRP-{i:03d}', f"{key} -> {r['proposed_sql_type'] or '(blocked)'} {r['allowed_values']} [{r['disposition']}]", 'Covered',
        (x['aspect_id'] + ' ' + x['blueprint_location']) if x else 'Part 3.6b §3.6.5.3 schema decision register (SDR)', 'Adopted; monetary columns use *_minor bigint per DEC-664', 'DEC-664' if r['proposed_sql_type'].startswith('numeric') else '')
for i, r in enumerate(csv.DictReader(open(f'{eng}/starter/database_field_review.csv', encoding='utf-8-sig')), 1):
    add(E, 'starter', 'database_field_review.csv', f'I-ENG-FRV-{i:03d}', f"{r['entity']}.{r['field']}: {r['issue'][:90]}", 'Covered', 'Duplicate of database_field_resolution_proposals.csv row %03d (verified identical keys)' % i, 'Covered with I-ENG-FRP-%03d' % i, '')
for obj, loc in [('growth_reference.tenant', 'ENT-001'), ('growth_reference.startup', 'ENT-002'), ('growth_reference.budget (reserved+spent<=hard_limit)', 'ENT-052 ai_budget; BRL-AI-08'), ('growth_reference.action_outbox (idempotency, payload_hash)', 'ENT-169 ops_outbox UQ-IDEM-13'),
                 ('growth_reference.receipt UNIQUE(tenant_id,provider,provider_ref)', 'ENT-142 com_payment UQ-IDEM-02'), ('reserve_budget() atomic reservation function', 'ai_cost_ledger reserve (NFR-014)'), ('action_outbox_ready_idx', 'ixp_ops_outbox__pending'),
                 ('smoke: initial reservation succeeds', 'TC-V12-I-033'), ('smoke: overspend rejected', 'TC-V12-I-033'), ('smoke: foreign scope rejected', 'TC-V12-I-033'), ('smoke: duplicate provider receipt rejected', 'TC-V12-I-033'), ('sandbox name guard growth_reference_*', 'DEC-420 agent sandboxes')]:
    add(E, 'starter', 'reference_schema.sql / reference_schema_smoke.sql', 'I-ENG-REF-' + re.sub(r'\W+', '_', obj)[:40], obj, 'Covered', loc, 'Adopted as reference fixture', '')
rev = open(f'{eng}/starter/catalog_schema_review_enhanced.sql', encoding='utf-8').read()
for t in re.findall(r'CREATE TABLE catalog_review\."(\w+)"', rev):
    m = emap.get(t)
    add(E, 'starter', 'catalog_schema_review(_enhanced).sql', f'I-ENG-CSR-{t}', f'catalog_review.{t} review DDL (146 tables in each file; identical table set)', 'Covered', f"{m['bp_ent']} {m['bp_table']}" if m else 'Part 3.6a', 'Superseded by Part 3.3/3.6 typed DDL + C3', '')
for f, n in [('database_catalog.json', 149), ('ui_upgrade/current_database_inventory.json', 155)]:
    add(E, 'engineering', f, 'I-ENG-JSON-' + f.split('/')[-1], f'{f}: {n} entities (same set as database_contract_review.csv + 6 candidates)', 'Covered', 'Part 3.6a §3.6.4.3 (155 rows)', 'Verified counts', '')
# ------------------------------------------------------------------ write
os.makedirs(f'{BP}/final/coverage_v12', exist_ok=True)
with open(f'{BP}/final/coverage_v12/I_coverage.csv', 'w', newline='', encoding='utf-8') as fh:
    w = csv.DictWriter(fh, fieldnames=['doc', 'chapter', 'section', 'aspect_id', 'aspect_summary', 'status_before', 'blueprint_location', 'action', 'new_ids', 'status_after'])
    w.writeheader(); w.writerows(rows)
ids = collections.Counter(r['aspect_id'] for r in rows)
dup = [k for k, v in ids.items() if v > 1]
stats = {'rows': len(rows), 'dupe_ids': dup[:20], 'before': collections.Counter(r['status_before'] for r in rows), 'after': collections.Counter(r['status_after'] for r in rows),
         'by_section': collections.Counter((r['chapter'], r['section']) for r in rows).most_common()}
json.dump({k: (dict(v) if isinstance(v, collections.Counter) else v) for k, v in stats.items()}, open(f'{BP}/assembly/v12/i_ddl/I_stats.json', 'w'), indent=1, default=str)
print(len(rows), 'dupes', len(dup), dup[:5]); print(stats['before']); print(stats['after'])
bych = collections.defaultdict(collections.Counter)
for r in rows: bych[r['chapter'] + ' ' + (r['section'] if r['chapter'] in ('Appendix C', 'Appendix C2') else '')][r['status_before']] += 1
for k, v in sorted(bych.items()): print(k, dict(v))
