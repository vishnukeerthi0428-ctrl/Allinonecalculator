"""Group E: build coverage CSV, table-mapping CSV and generated Markdown fragments for Part 3.6.
usage: python3 -I E_build_data.py <scratch_E_dir> <blueprint_dir>"""
import json, csv, sys, os, re
from collections import Counter, OrderedDict
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from E_mapping import M
from E_overrides import O
from E_aspects import A
SD, BD = sys.argv[1], sys.argv[2]
d = json.load(open(f'{SD}/doc08.json')); bp = json.load(open(f'{SD}/part33.json'))
cols = list(csv.DictReader(open(f'{SD}/columns.csv'))); cons = list(csv.DictReader(open(f'{SD}/constraints.csv')))
ents = d['entities'] + d['candidates']
def key(e): return e['no'] if e['no'] is not None else e['name']
EXP = lambda ex: ('EXP-PUB' if ex.startswith('public API') else 'EXP-PRT' if 'own authorized object' in ex else
                  'EXP-WEB' if 'Authorized website' in ex else 'EXP-ADM' if ex else 'EXP-ADM (candidate)')
PRO = lambda p: ('PII-R' if 'PII' in p else 'AUDFIN-R' if 'audit/finance' in p else 'SECRET' if 'Secret' in p else
                 'SCOPE' if 'Scope by' in p else 'INT' if p else 'SCOPE (candidate)')
# ---- constraint fixes (curated proposals for the 57 gaps) ----
CF = {
 (5,'unique(product_id,code)'):('Gap','uq_cat_capability__code (tenant_id, startup_id, code) WHERE archived_at IS NULL; offering link already UQ in cat_offering_capability'),
 (11,'index(subject_key,channel,purpose,occurred_at)'):('Covered','ix_gov_consent__current (tenant_id, startup_id, subject_hmac, channel, purpose, effective_at DESC), Part 3.3 §3.3.8.2'),
 (16,'unique(integration_id,period)'):('Gap','uq_int_quota__period (tenant_id, startup_id, integration_id, unit, period)'),
 (19,'unique(job_key)'):('Gap','uq_ops_job_run__job_key (COALESCE(tenant_id, zero-uuid), job_key) on new column job_key'),
 (19,'index(status,next_retry)'):('Gap',"ixp_ops_job_run__retry (next_retry_at) WHERE state IN ('failed','retry_scheduled')"),
 (24,'unique(case_key)'):('Gap','uq_ai_eval_case__code (COALESCE(tenant_id, zero-uuid), suite_code, case_code, version_no)'),
 (26,'unique(scope,period_start)'):('Gap',"uq_ai_budget__scope_period (COALESCE(tenant_id, zero-uuid), scope_level, scope_ref, period) WHERE status = 'active'"),
 (27,'unique(entry_key)'):('Gap','uq_ai_cost_ledger__entry_key (tenant_id, entry_key) on new column entry_key (complements UQ-IDEM-15)'),
 (28,'index(state,due_at)'):('Gap',"ixp_gov_privacy_request__due (tenant_id, due_at) WHERE state NOT IN ('completed','rejected','withdrawn')"),
 (30,'unique(version,environment)'):('Gap','uq_ops_release__tag_env (version_tag, environment) on new column environment'),
 (31,'index(state,severity)'):('Gap',"ixp_ops_incident__open (severity, opened_at DESC) WHERE state <> 'closed'"),
 (33,'unique(job_run_id)'):('Gap','uq_intel_query_run__correlation (tenant_id, startup_id, correlation_id) WHERE correlation_id IS NOT NULL'),
 (34,'unique(source_id,canonical_url,content_hash)'):('Gap','uq_intel_source_record__version (tenant_id, startup_id, source_id, url_hash, content_hash) on new column content_hash'),
 (35,'index(source_id,fetched_at)'):('Gap','ix_intel_fetch_log__source_time (tenant_id, startup_id, source_id, created_at DESC) on new column source_id'),
 (38,'index(organization_id,country,region)'):('Gap','ix_intel_location__org_geo (tenant_id, startup_id, organization_id, country_code, subdivision_code)'),
 (41,'unique(organization_id,evidence_id,signal_type_id)'):('Gap',"uq_intel_signal__dedupe (tenant_id, startup_id, dedupe_key) WHERE state <> 'rejected'; dedupe_key = sha256(organization_id|signal_type_id|sorted evidence ids)"),
 (44,'unique(need_id,capability_id)'):('Gap','uq_intel_match__need_target (tenant_id, startup_id, need_id, offering_version_id, COALESCE(capability_id, zero-uuid))'),
 (46,'unique(opportunity_id,version)'):('Gap','uq_intel_score_version__seq (opportunity_id, version_no) on new column version_no integer NOT NULL'),
 (48,'unique(opportunity_id,role_title)'):('Gap','uq_intel_role_hypothesis__opp_role (tenant_id, startup_id, opportunity_id, role_code) WHERE opportunity_id IS NOT NULL'),
 (50,'index(contact_id,channel,expires_at)'):('Gap','ix_intel_contact_verification__expiry (tenant_id, startup_id, contact_id, channel, expires_at DESC)'),
 (56,'unique(slug,version)'):('Gap','uq_crm_form__code (tenant_id, startup_id, form_code) WHERE archived_at IS NULL; version uniqueness by STD-V on crm_form_version'),
 (58,'index(state,owner_id)'):('Gap',"ixp_crm_lead__queue (tenant_id, startup_id, state, owner_id) WHERE archived_at IS NULL"),
 (61,'unique(workflow_key,version)'):('Gap','uq_aut_workflow__code (tenant_id, startup_id, workflow_code); version uniqueness by STD-V on aut_workflow_revision'),
 (64,'unique(template_key,version,channel)'):('Gap','uq_eng_message_template__code (tenant_id, startup_id, template_code, channel, locale, version_no)'),
 (66,'unique(channel,external_thread_ref)'):('Gap','uq_eng_thread__external (channel_account_id, external_thread_ref) WHERE external_thread_ref IS NOT NULL'),
 (69,'unique(integration_id,provider_event_key)'):('Covered','UQ-IDEM-05 (channel_account_id, provider_message_id) and UQ-IDEM-01 provider event key'),
 (70,'unique(inbound_event_id)'):('Gap','uq_eng_intent__inbound (inbound_event_id) WHERE superseded_by IS NULL; one current intent per inbound event'),
 (74,'unique(integration_id,external_calendar_id)'):('Gap','uq_eng_calendar_link__external (integration_id, external_calendar_id) on new column external_calendar_id'),
 (78,'index(object_type,object_id)'):('Gap','ix_gov_approval__object (tenant_id, startup_id, object_type, object_id, created_at DESC)'),
 (81,'unique(channel_account_id,external_subject_hash)'):('Gap','uq_eng_identity_link__address (tenant_id, startup_id, channel_account_id, address_hmac)'),
 (82,'unique(channel,priority)'):('Gap',"uq_eng_routing_rule__priority (tenant_id, startup_id, COALESCE(channel,'*'), priority) WHERE status = 'active'"),
 (83,'index(action_key)'):('Gap','ix_gov_policy_decision__action (tenant_id, startup_id, action, created_at DESC)'),
 (84,'index(state,severity)'):('Gap',"ixp_gov_compliance_incident__open (tenant_id, severity, opened_at DESC) WHERE state <> 'closed'"),
 (85,'unique(source_record_id,external_post_id)'):('Gap','uq_intel_social_post__ref (tenant_id, startup_id, platform, post_ref)'),
 (86,'index(product_id,state)'):('Gap','ix_mkt_content_asset__offering_state (tenant_id, startup_id, offering_id, state)'),
 (87,'unique(content_asset_id,version)'):('Covered','STD-V version_no UNIQUE within parent asset_id (Part 3.3 §3.3.6.1)'),
 (90,'index(state,page_url)'):('Gap',"ixp_mkt_seo_issue__open (tenant_id, startup_id, page_id, severity) WHERE state <> 'resolved'"),
 (91,'unique(page_url,date,metric_key)'):('Gap','uq_mkt_page_metric__day (tenant_id, startup_id, page_id, COALESCE(keyword_id, zero-uuid), metric_date, source)'),
 (93,'unique(event_key)'):('Gap','uq_mkt_attribution_event__key (tenant_id, startup_id, event_key) on new column event_key'),
 (95,'index(state)'):('Gap','ix_mkt_campaign__state (tenant_id, startup_id, state, starts_at)'),
 (98,'unique(event_key)'):('Gap','uq_mkt_spend_event__key (ad_campaign_id, event_key); for manual/CSV spend rows, UQ-IDEM-19 covers provider reports'),
 (99,'index(starts_at,state)'):('Gap','ix_mkt_event__starts (tenant_id, startup_id, starts_at, state)'),
 (100,'unique(event_id,lead_id)'):('Gap','uq_mkt_registration__event_contact (event_id, contact_id)'),
 (101,'unique(registration_id,provider_ref)'):('Gap','uq_mkt_attendance__provider (registration_id, provider_ref) WHERE provider_ref IS NOT NULL'),
 (104,'index(deal_id,state)'):('Gap','ix_com_proposal__deal_state (tenant_id, startup_id, deal_id, state)'),
 (106,'index(deal_id,state)'):('Gap','ix_com_quote__deal_state (tenant_id, startup_id, deal_id, state)'),
 (108,'index(deal_id,state)'):('Gap','ix_com_objection__deal_state (tenant_id, startup_id, deal_id, state)'),
 (110,'unique(deal_id,version)'):('Covered','UNIQUE (tenant_id, startup_id, contract_no) + amendment chain (Part 3.3 §3.3.6.9)'),
 (114,'unique(deal_id)'):('Gap','uq_lcy_onboarding__deal (tenant_id, startup_id, deal_id) WHERE archived_at IS NULL'),
 (115,'unique(onboarding_id,task_id)'):('Gap','uq_lcy_handoff__task (onboarding_id, task_id) WHERE task_id IS NOT NULL on new column task_id'),
 (123,'index(prompt_version_id,passed)'):('Gap','ix_ai_eval_run__prompt_gate (prompt_version_id, gate_result, created_at DESC)'),
 (124,'unique(domain)'):('Gap','uq_intel_competitor__website (tenant_id, startup_id, lower(website)) WHERE website IS NOT NULL'),
 (125,'unique(competitor_id,evidence_id,event_type)'):('Gap','uq_intel_market_event__dedupe (tenant_id, startup_id, competitor_id, evidence_id, event_type)'),
 (126,'unique(stage_id,period_start)'):('Gap','uq_ana_stage_metric__period (tenant_id, startup_id, pipeline_id, stage_code, period)'),
 (127,'unique(period_start,model_version)'):('Gap','uq_ana_forecast__period (tenant_id, startup_id, period, scenario, model_version) on new column model_version'),
 (129,'index(release_id,status)'):('Gap','ix_ops_test_run__release (release_id, result, executed_at DESC)'),
 (130,'unique(deal_id)'):('Gap','uq_lcy_integration_deal__deal (tenant_id, startup_id, deal_id) WHERE deal_id IS NOT NULL'),
 (135,'Approved immutable revision'):('Gap','Imm. V on new ten_business_template (STD-V)'),
 (137,'Immutable approved price and entitlement revision'):('Covered','saas_plan_version and saas_entitlement are Imm. V (Part 3.3)'),
}
ixn = 0
for r in cons:
    try: k = (int(r['src_no']), r['constraint'])
    except ValueError: k = (r['src_no'], r['constraint'])
    if k in CF:
        st, prop = CF[k]; r['status'] = st
        if st == 'Gap':
            ixn += 1; r['new_id'] = f'IX-ENH-E-{ixn:02d}'
        r['blueprint'] = prop if st == 'Covered' else r['blueprint']; r['action'] = prop
    r.setdefault('new_id', '')
json.dump(cons, open(f'{SD}/cons_final.json','w'), indent=1)
# ---- per-table summary ----
by = OrderedDict()
for r in cols: by.setdefault(r['src_no'], []).append(r)
mapping_rows = []
for e in ents:
    k = key(e); prim, sec, mt, note = M[k]; b = bp.get(prim, {})
    rs = by[str(k)]
    c = Counter(r['status'] for r in rs)
    cov = sum(v for s, v in c.items() if s.startswith('Covered') or s.startswith('Not adopted'))
    gaps = sum(v for s, v in c.items() if s.startswith('Gap'))
    conf = c.get('Conflict', 0)
    ops = len([x for x in (e.get('Operations') or e.get('REST operations') or '').split(';') if x.strip()])
    status = 'Not covered (new entity)' if mt.startswith('New') else 'Conflict' if conf else 'Partially covered' if gaps else 'Covered'
    mapping_rows.append(OrderedDict(
        src_no=(f'{k:03d}' if isinstance(k, int) else 'C' + str(['sales_ui_application','sales_ui_config_revision','sales_ui_trigger_revision','sales_ui_conflict','sales_ui_template_revision','sales_ui_service_request'].index(k)+1)),
        src_table=e['name'], src_logical=e.get('Logical entity', e.get('purpose','candidate')), src_build=e.get('Build/reuse','Candidate'),
        src_exposure=EXP(e.get('Exposure','')), src_protection=PRO(e.get('Protection','')),
        bp_ent=prim, bp_table=b.get('table','(new) ' + {'ENT-ENH-E-01':'ten_business_template','ENT-ENH-E-02':'saas_service_request'}.get(prim,'')),
        bp_logical=b.get('logical',''), bp_domain=b.get('domain',''), bp_scope=b.get('scope',''), bp_imm=b.get('imm',''), bp_ret=b.get('ret',''),
        secondary=';'.join(sec), match_type=mt, src_columns=len(rs), covered_columns=cov, gap_columns=gaps, conflict_columns=conf,
        src_fk=e.get('Foreign keys',''), src_constraints=e.get('Constraints and indexes',''), src_operations=ops, status=status, note=note))
with open(f'{BD}/final/coverage/E_table_mapping.csv','w',newline='') as f:
    w = csv.DictWriter(f, fieldnames=list(mapping_rows[0].keys())); w.writeheader(); w.writerows(mapping_rows)
json.dump(mapping_rows, open(f'{SD}/mapping_rows.json','w'), indent=1)
# ---- coverage CSV ----
cov_rows = []
def add(doc, sec, aid, summ, st, loc, act, ids):
    st = {'Covered (ID not traced)':'Covered','Not applicable (other group)':'Not applicable','Not covered (new entity)':'Not covered'}.get(st, st)
    cov_rows.append(OrderedDict(doc=doc, section=sec, aspect_id=aid, aspect_summary=summ, status=st, blueprint_location=loc, action=act, new_ids=ids))
for a in A:
    a = list(a) + [''] * (8 - len(a)); add(*a[:8])
for m in mapping_rows:
    add('08', 'Commercial PostgreSQL entity register', f"08-ENT-{m['src_no']}", f"Table {m['src_table']} ({m['src_columns']} source columns; exposure {m['src_exposure']}; protection {m['src_protection']})",
        m['status'], f"Part 3.3 {m['bp_ent']} {m['bp_table']}" + (f" (+{m['secondary']})" if m['secondary'] else ''),
        f"{m['match_type']}; {m['covered_columns']} columns covered, {m['gap_columns']} added in Part 3.6, {m['conflict_columns']} conflict", 'GAP-388' if m['status'].startswith('Not') else ('GAP-389' if m['gap_columns'] else ''))
for r in cols:
    st = r['status']
    s2 = ('Covered' if st.startswith('Covered') else 'Not applicable' if st.startswith('Not adopted') else 'Conflict' if st == 'Conflict' else 'Not covered')
    ids = 'CONFLICT-381' if r['src_no']=='10' and st=='Conflict' else 'CONFLICT-383' if st=='Conflict' and r['src_no']=='147' else 'CONFLICT-387' if st=='Conflict' else ('GAP-388' if 'new entity' in st else 'GAP-389' if st.startswith('Gap') else '')
    add('08', 'Column', f"08-COL-{r['src_table']}.{r['column']}", f"{r['src_table']}.{r['column']} {r['src_type']}", s2,
        f"{r['bp_ent']} {r['bp_table']}.{r['bp_column'].split(' ')[0] if st.startswith('Covered') else ''}".strip(), r['bp_column'] if not st.startswith('Covered (') else f"maps to {r['bp_column']}", ids)
for i, r in enumerate(cons):
    s2 = 'Covered' if r['status'].startswith('Covered') else 'Partially covered' if r['status']=='Partial' else 'Not covered'
    add('08', 'Constraint/index', f"08-CON-{r['src_table']}-{i+1:03d}", f"{r['src_table']}: {r['constraint']}", s2, r['blueprint'], r['action'], r['new_id'] or ('GAP-390' if s2!='Covered' else ''))
for i, r in enumerate(d['resolution']):
    fld = r['field'].split(' ')[0].split(':')[0]
    c = [x for x in cols if x['src_table']==r['entity'] and x['column']==fld]
    st = c[0]['status'] if c else ('Blocked' if 'Blocked' in r['decision'] else 'Covered')
    s2 = 'Covered' if st.startswith('Covered') or st=='Blocked' or st.startswith('Not adopted') else 'Conflict' if st=='Conflict' else 'Not covered'
    add('08', 'Physical schema resolution', f"08-SDR-{i+1:03d}", f"{r['entity']} / {r['field']}: {r['decision'][:60]}", s2,
        'Part 3.6 §3.6.4.8 SDR', 'Resolved by DEC-003/DEC-019 (identity) or DEC-088 (embedding), see CONFLICT-381/382' if 'Blocked' in r['decision'] else ('Column added' if s2=='Not covered' else 'Type confirmed against Part 3.3'), 'SDR-%03d' % (i+1))
for r in d['doc28_inventory']:
    add('28', 'Logical entity inventory for migration planning', f"28-INV-{r['entity']}", f"{r['entity']}: {r['classification']}", 'Covered', 'Part 3.6 §3.6.4.9 exposure register', 'Consistent with doc 08 exposure', '')
with open(f'{BD}/final/coverage/E_coverage.csv','w',newline='') as f:
    w = csv.DictWriter(f, fieldnames=list(cov_rows[0].keys())); w.writeheader(); w.writerows(cov_rows)
json.dump(cov_rows, open(f'{SD}/cov_rows.json','w'), indent=1)
summ = Counter((r['doc'], r['section'] if r['section'] in ('Column','Constraint/index','Physical schema resolution','Commercial PostgreSQL entity register','Logical entity inventory for migration planning') else 'Prose', r['status']) for r in cov_rows)
for k2 in sorted(summ): print(k2, summ[k2])
print('coverage rows', len(cov_rows), 'mapping rows', len(mapping_rows), 'constraint gaps', ixn)
print(Counter(m['status'] for m in mapping_rows))
