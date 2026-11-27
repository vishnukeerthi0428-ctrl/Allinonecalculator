"""Group E: column-level reconciliation of Doc 08 tables against Part 3.3 entities.
usage: python3 -I E_reconcile.py <doc08.json> <part33.json> <out_dir>"""
import json, sys, csv, os, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from E_mapping import M
from E_overrides import O
d = json.load(open(sys.argv[1])); bp = json.load(open(sys.argv[2])); out = sys.argv[3]
bp['ENT-146']['columns'] = bp['ENT-145']['columns']; bp['ENT-146']['std_columns'] = bp['ENT-145'].get('std_columns', [])
JOIN = {"ten_membership_grant": ["membership_id","role_id","startup_id","granted_by","valid_from","valid_to","tenant_id"],
        "aut_run_conflict": ["run_id","conflict_case_id"]}
SYN = {  # source column -> candidate blueprint names
 'state':['state','status','lifecycle_state','verification_state'], 'status':['status','state','lifecycle_state'],
 'product_id':['offering_id','offering_version_id'], 'active':['is_active','status','state','active'],
 'version':['version_no','revision','plan_revision'], 'sha256':['content_hash','sha256','file_sha256'],
 'owner_id':['owner_id','owner_user_id','assigned_to'], 'value_inr':['expected_value','amount','value'],
 'amount_inr':['amount','total_amount','amount_inr','gross_amount'], 'subject_key':['subject_hash','subject_key','contact_id','email_hmac'],
 'approved_by':['approved_by','approval_id','approver_id'], 'reviewer_id':['reviewer_id','reviewed_by','decided_by'],
 'actor_id':['actor_id','created_by'], 'recipient_id':['recipient_user_id','user_id','recipient_id'],
 'canonical_domain':['domain','canonical_domain','website'], 'professional_name':['full_name','display_name','name_enc','professional_name'],
 'work_email':['email_enc','email_hmac','work_email'], 'business_phone':['phone_enc','phone_hmac','business_phone'],
 'object_key':['storage_key','file_storage_key','object_key'], 'secret_ref':['secret_arn','secret_ref','secrets_manager_arn'],
 'payload_ref':['payload_storage_key','payload_ref','payload'], 'result_ref':['output_ref','result_ref','output_storage_key','result'],
 'body':['body','body_text','body_ref','text','content'], 'event_key':['event_key','dedupe_key','idempotency_key','event_type'],
 'provider_event_key':['provider_event_id','provider_event_key','dedupe_key'], 'next_retry':['next_attempt_at','next_retry_at','next_retry'],
 'available_at':['available_at','next_attempt_at'], 'limit':['limit_value','quota_limit','limit'], 'used':['used_value','used'],
 'limit_inr':['ceiling_amount','limit_amount','limit_inr','amount'], 'reserved_inr':['reserved_amount','reserved'], 'spent_inr':['spent_amount','consumed_amount','spent'],
 'forecast_inr':['weighted_value','forecast_value'], 'budget_inr':['budget_amount','budget_cap','budget'],
 'starts_at':['starts_at','start_at'], 'template_id':['template_id','message_template_id'],
 'date':['metric_date','date','period_start'], 'period_start':['period_start','period','metric_date'],
 'model':['model_id','model','embedding_model'], 'confidence':['confidence','confidence_score'],
 'opaque_token_hash':['session_token_hash','token_hash','opaque_token_hash'], 'external_subject_hash':['external_subject_hash','subject_hash'],
 'deal_id':['deal_id','object_id'], 'organization_id':['organization_id','org_id','party_ref'],
 'existing_user_id':['user_id'], 'role':['role_id','role_code'], 'permissions':['permissions','approval_limits'],
 'region':['home_region','region'], 'kind':['kind','ownership_type','service_model','offering_kind','type'],
 'legal_name':['legal_name'], 'brand':['display_name','brand'], 'industry':['industry','sector'], 'currency':['currency','base_currency'],
 'hostname':['hostname'], 'verification_hash':['verification_token_hash'], 'plan_key':['plan_code','code'], 'plan_id':['plan_id','plan_version_id'],
 'plan_revision':['plan_version_id','version_no'], 'trial_end':['trial_ends_at','trial_end'], 'period_end':['current_period_end','period_end'],
 'granted_to':['grantee_user_id','granted_to','support_user_id'], 'actions':['actions','scope','permitted_actions'],
 'direction':['direction','request_type'], 'dataset':['entity_selection','template_code','dataset'], 'object_ref':['file_storage_key'],
 'objective':['objective_code'], 'autonomy':['mode'], 'estimated_cost':['simulation_cost','budget_cap'], 'actions_plan':['actions'],
 'opportunity_id':['opportunity_id'], 'deadline':['submission_deadline','deadline'], 'submission_ref':['submission_reference','submission_ref'],
 'total':['total_amount','total','line_total'], 'price':['unit_price'], 'tax':['tax_amount','tax'], 'line_id':['order_line_id'],
 'milestone_key':['milestone_code','event_type'], 'evidence_ref':['evidence_ref','evidence_storage_key','evidence_id'],
 'external_identity_ref':['subject_user_id'], 'resource_type':['object_type'], 'resource_id':['object_id'], 'allowed_actions':['actions'],
 'invite_secret_hash':['invite_token_hash'], 'blocks':['blocks','content','snapshot'], 'locale':['locale'], 'slug':['slug','path'],
 'approval_ref':['approval_id'], 'published':['current_snapshot_id','state','published'], 'actor_ref':['created_by','published_by'],
 'application_ref':['application_ref','opaque_ref','reference_hash','draft_token_hash'], 'business_email':['email_enc','business_email','contact_email_enc'],
 'country':['country_code','country'], 'terms_revision':['terms_version','terms_revision'], 'verified_principal_ref':['applicant_user_id'],
 'expires_at':['expires_at','link_expires_at','valid_to'], 'configuration':['config','configuration','payload'], 'configuration_hash':['content_hash'],
 'approved_by_ref':['approval_id','approved_by'], 'base_revision':['base_version_no','supersedes_id'], 'workflow_revision_id':['workflow_revision_id'],
 'definition':['definition','graph','schedule','config'], 'timezone':['timezone','business_timezone'], 'concurrency_limit':['concurrency_limit'],
 'next_due_at':['next_fire_at','next_due_at'], 'relationship_ref':['relationship_ref'], 'action_key':['duplicate_key','action_key'],
 'run_refs':['run_id'], 'decision':['resolution','decision','outcome'], 'resolved_at':['resolved_at'], 'template_key':['template_code','template_key','code'],
 'capability':['business_capability','capability'], 'graph':['graph','definition','node_types'], 'input_schema':['input_schema'], 'output_schema':['output_schema'],
 'schema':['schema','json_schema','field_schema'], 'defaults':['defaults'], 'hash':['content_hash'], 'approval_id':['approval_id'],
 'charge_key':['meter_code','idempotency_key','charge_key'], 'units':['quantity','units'], 'unit_price':['unit_price'], 'amount':['amount','total_amount'],
 'usage_id':['reading_id','usage_id'], 'invoice_id':['invoice_id','service_invoice_id','applied_invoice_id'], 'subscription_id':['subscription_id'],
 'reverses_id':['reverses_id'], 'period_key':['period_start'], 'payment_ref':['payment_ref','provider_payment_ref'],
 'feature_limits':['limits','entitlements','feature_limits'], 'rate_card':['rate_card','price_list','base_fee'],
 'entitlements':['entitlement_snapshot','entitlements'], 'profile':['profile','settings'], 'policy':['policy','settings'],
 'approved_hash':['approved_hash','content_hash'], 'input_hash':['input_hash'], 'policy_hash':['policy_hash'], 'simulation':['simulation_result','simulation'],
}
rows = []; per_ent = []
ents = d['entities'] + d['candidates']
for e in ents:
    key = e['no'] if e['no'] is not None else e['name']
    prim, sec, mtype, note = M[key]
    targets = [prim] + sec
    have = set(['id','tenant_id','startup_id','revision','created_at','updated_at','created_by','updated_by'])
    for t in targets:
        if t in bp:
            have |= set(bp[t]['columns']) | set(bp[t].get('std_columns', [])) | set(bp[t].get('key_text_cols', []))
        elif t in JOIN: have |= set(JOIN[t])
    matched = unmatched = 0
    for c in e['columns']:
        n = c['name']
        if mtype.startswith('New') and n not in ('id','tenant_id','startup_id','revision','created_at','updated_at'):
            st, via = 'Gap - new entity in Part 3.6', prim
        elif n == '(existing)':
            st, via = 'Covered (reuse)', 'identity mirror'
        else:
            cands = [n] + SYN.get(n, [])
            hit = [x for x in cands if x in have]
            if hit: st, via = ('Covered' if hit[0] == n else 'Covered (renamed)'), hit[0]
            elif (key, n) in O:
                code, v = O[(key, n)]
                st = {'S':'Covered (semantic)','G':'Gap - column added in Part 3.6','C':'Conflict','N':'Not adopted (reason)'}[code]; via = v
            elif mtype.startswith('New'):
                st, via = 'Gap - new entity in Part 3.6', prim
            else: st, via = 'Not matched', ''
        if st.startswith('Covered') or st.startswith('Not adopted'): matched += 1
        else: unmatched += 1
        rows.append(dict(src_no=key, src_table=e['name'], column=n, src_type=c['type'], bp_ent=prim, bp_table=bp.get(prim,{}).get('table',''),
                         status=st, bp_column=via))
    per_ent.append(dict(src_no=key, src_table=e['name'], bp_ent=prim, bp_table=bp.get(prim,{}).get('table','(new)'), secondary=';'.join(sec),
                        match_type=mtype, src_cols=len(e['columns']), matched=matched, unmatched=unmatched, note=note,
                        exposure=e.get('Exposure','')[:60], fks=e.get('Foreign keys',''), constraints=e.get('Constraints and indexes',''),
                        protection=e.get('Protection',''), build=e.get('Build/reuse','')))
with open(os.path.join(out,'columns.csv'),'w',newline='') as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
json.dump(per_ent, open(os.path.join(out,'per_ent.json'),'w'), indent=1)
from collections import Counter
print(Counter(r['status'] for r in rows))
for r in rows:
    if r['status']=='Not matched': print(r['src_no'], r['src_table'], r['column'], r['src_type'], '->', r['bp_ent'], r['bp_table'])
