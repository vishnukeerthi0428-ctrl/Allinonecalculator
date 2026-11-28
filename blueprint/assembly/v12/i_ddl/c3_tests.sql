-- TC-V12-I-001..032: verification of DDL-V12-I (Appendix C3) on PostgreSQL 16.15. Run as owner for fixtures, ge_app for tests.
\set ON_ERROR_STOP on
\pset format unaligned
SET client_min_messages = notice;
-- helper: expect an error (any SQLSTATE in list) from dynamic SQL
CREATE OR REPLACE FUNCTION t_expect_error(p_id text, p_sql text, p_states text[] DEFAULT NULL) RETURNS void LANGUAGE plpgsql AS $$
BEGIN
  BEGIN EXECUTE p_sql;
  EXCEPTION WHEN OTHERS THEN
    IF p_states IS NULL OR SQLSTATE = ANY (p_states) THEN RAISE NOTICE 'PASS % (rejected: % %)', p_id, SQLSTATE, left(SQLERRM, 90); RETURN; END IF;
    RAISE EXCEPTION 'FAIL % wrong error % %', p_id, SQLSTATE, SQLERRM;
  END;
  RAISE EXCEPTION 'FAIL % statement was accepted: %', p_id, left(p_sql, 120);
END $$;
CREATE OR REPLACE FUNCTION t_expect_value(p_id text, p_sql text, p_expected text) RETURNS void LANGUAGE plpgsql AS $$
DECLARE v text; BEGIN EXECUTE p_sql INTO v;
  IF v IS DISTINCT FROM p_expected THEN RAISE EXCEPTION 'FAIL % expected % got %', p_id, p_expected, v; END IF;
  RAISE NOTICE 'PASS % (value %)', p_id, v; END $$;
CREATE OR REPLACE FUNCTION t_ctx(p_tenant text, p_companies text, p_write text, p_kind text DEFAULT 'internal') RETURNS void LANGUAGE sql AS $$
  SELECT set_config('app.tenant_id', p_tenant, true), set_config('app.company_ids', p_companies, true),
         set_config('app.write_company_id', p_write, true), set_config('app.actor_kind', p_kind, true),
         set_config('app.actor_id', '00000000-0000-0000-0000-0000000000aa', true) $$;
GRANT EXECUTE ON FUNCTION t_expect_error(text,text,text[]), t_expect_value(text,text,text), t_ctx(text,text,text,text) TO ge_app;
SET app.deployment_region = 'IN';
-- ---------- fixtures (owner, with context because RLS is forced)
BEGIN;
SELECT t_ctx('00000000-0000-0000-0000-00000000000a','{}','');
INSERT INTO tenant VALUES ('00000000-0000-0000-0000-00000000000a','owned','IN','active',now()),('00000000-0000-0000-0000-00000000000b','client','IN','active',now());
INSERT INTO organization(tenant_id,organization_id,name) VALUES ('00000000-0000-0000-0000-00000000000a','00000000-0000-0000-0000-0000000000a1','Org A');
SELECT t_ctx('00000000-0000-0000-0000-00000000000a','{00000000-0000-0000-0000-0000000000c1}','00000000-0000-0000-0000-0000000000c1');
INSERT INTO company(tenant_id,company_id,organization_id,legal_name) VALUES ('00000000-0000-0000-0000-00000000000a','00000000-0000-0000-0000-0000000000c1','00000000-0000-0000-0000-0000000000a1','Co A1');
SELECT t_ctx('00000000-0000-0000-0000-00000000000a','{00000000-0000-0000-0000-0000000000c3}','00000000-0000-0000-0000-0000000000c3');
INSERT INTO company(tenant_id,company_id,organization_id,legal_name) VALUES ('00000000-0000-0000-0000-00000000000a','00000000-0000-0000-0000-0000000000c3','00000000-0000-0000-0000-0000000000a1','Co A2');
INSERT INTO workflow_run(tenant_id,company_id,run_id,sku_id,wf_id,wf_version,business_context,input,status,requested_by,idempotency_key)
 VALUES ('00000000-0000-0000-0000-00000000000a','00000000-0000-0000-0000-0000000000c3','00000000-0000-0000-0000-0000000000e3','SM-SVC-02','SM-SVC-02-WF1',1,'{}','{}','Queued','00000000-0000-0000-0000-000000000001','c3run');
SELECT t_ctx('00000000-0000-0000-0000-00000000000a','{00000000-0000-0000-0000-0000000000c1}','00000000-0000-0000-0000-0000000000c1');
INSERT INTO workflow_run(tenant_id,company_id,run_id,sku_id,wf_id,wf_version,business_context,input,status,requested_by,idempotency_key)
 VALUES ('00000000-0000-0000-0000-00000000000a','00000000-0000-0000-0000-0000000000c1','00000000-0000-0000-0000-0000000000e1','SM-SVC-01','SM-SVC-01-WF1',1,'{}','{}','Queued','00000000-0000-0000-0000-000000000001','c1run');
INSERT INTO custom_role(tenant_id,role_id,name) VALUES ('00000000-0000-0000-0000-00000000000a','00000000-0000-0000-0000-0000000000f1','Requester'),('00000000-0000-0000-0000-00000000000a','00000000-0000-0000-0000-0000000000f2','Approver');
INSERT INTO role_permission VALUES ('00000000-0000-0000-0000-00000000000a','00000000-0000-0000-0000-0000000000f1','Runs:create'),('00000000-0000-0000-0000-00000000000a','00000000-0000-0000-0000-0000000000f1','Runs:read'),('00000000-0000-0000-0000-00000000000a','00000000-0000-0000-0000-0000000000f2','Runs:approve');
INSERT INTO user_role_assignment VALUES ('00000000-0000-0000-0000-00000000000a','00000000-0000-0000-0000-00000000001a','00000000-0000-0000-0000-0000000000f1','00000000-0000-0000-0000-0000000000aa',now(),NULL,NULL);
INSERT INTO inbox(provider,provider_account,provider_event_id,tenant_id,signature_ok) VALUES ('razorpay','acct_a','evt_1','00000000-0000-0000-0000-00000000000a',true);
INSERT INTO incident(incident_id,tenant_id,severity,detected_at,aware_at,personal_data,summary) VALUES ('00000000-0000-0000-0000-0000000000d9','00000000-0000-0000-0000-00000000000a','SEV2',now(),now(),true,'fixture');
INSERT INTO domain_schema_registry VALUES ('SM-SVC-03/contact',1,'growth_contact','{draft,verified,archived}','{professional_name}','{}','Restricted','BUS',262144,'Approved','00000000-0000-0000-0000-0000000000aa',now());
INSERT INTO metric_definition VALUES ('KPI-27',1,'Async ack p95','p95(ack_ms)','q_ack',NULL,'ms','{run.accepted}','no_currency','Asia/Kolkata','day','{}','none',NULL,'SRE',NULL,2000,'<=','operator','Approved','00000000-0000-0000-0000-0000000000aa');
INSERT INTO tenant_key_config(tenant_id,mode,kms_key_ref,rotation_days,provider) VALUES ('00000000-0000-0000-0000-00000000000a','customer','arn:aws:kms:ap-south-1:111:key/x',90,'aws-kms');
INSERT INTO tenant_data_key(tenant_id,dek_id,wrapped_dek,kek_ref,kek_provider) VALUES ('00000000-0000-0000-0000-00000000000a','00000000-0000-0000-0000-00000000002a','\x0102','arn:aws:kms:ap-south-1:111:key/x','aws-kms');
COMMIT;
BEGIN; SELECT t_ctx('00000000-0000-0000-0000-00000000000b','{}','');
INSERT INTO organization(tenant_id,organization_id,name) VALUES ('00000000-0000-0000-0000-00000000000b','00000000-0000-0000-0000-0000000000b1','Org B');
SELECT t_ctx('00000000-0000-0000-0000-00000000000b','{00000000-0000-0000-0000-0000000000c2}','00000000-0000-0000-0000-0000000000c2');
INSERT INTO company(tenant_id,company_id,organization_id,legal_name) VALUES ('00000000-0000-0000-0000-00000000000b','00000000-0000-0000-0000-0000000000c2','00000000-0000-0000-0000-0000000000b1','Co B');
INSERT INTO custom_role(tenant_id,role_id,name) VALUES ('00000000-0000-0000-0000-00000000000b','00000000-0000-0000-0000-0000000000f9','B role');
COMMIT;
SET ROLE ge_app;
-- ---------- tests
BEGIN; SELECT t_ctx('00000000-0000-0000-0000-00000000000a','{00000000-0000-0000-0000-0000000000c1}','00000000-0000-0000-0000-0000000000c1');
SELECT t_expect_value('TC-V12-I-001 cross-company read denied inside one tenant', 'SELECT count(*)::text FROM workflow_run', '1');
SELECT t_expect_value('TC-V12-I-001b company table shows only scoped company', 'SELECT count(*)::text FROM company', '1');
SELECT t_expect_error('TC-V12-I-001c write to non-selected company denied', $q$INSERT INTO workflow_run(tenant_id,company_id,sku_id,wf_id,wf_version,business_context,input,status,requested_by,idempotency_key) VALUES ('00000000-0000-0000-0000-00000000000a','00000000-0000-0000-0000-0000000000c3','SM-SVC-01','SM-SVC-01-WF1',1,'{}','{}','Queued','00000000-0000-0000-0000-000000000001','x1')$q$, '{42501}');
ROLLBACK;
BEGIN; SELECT t_ctx('00000000-0000-0000-0000-00000000000a','{00000000-0000-0000-0000-0000000000c1,00000000-0000-0000-0000-0000000000c3}','');
SELECT t_expect_value('TC-V12-I-002 portfolio mode reads permitted companies', 'SELECT count(*)::text FROM workflow_run', '2');
SELECT t_expect_error('TC-V12-I-002b portfolio mode cannot write', $q$INSERT INTO workflow_run(tenant_id,company_id,sku_id,wf_id,wf_version,business_context,input,status,requested_by,idempotency_key) VALUES ('00000000-0000-0000-0000-00000000000a','00000000-0000-0000-0000-0000000000c1','SM-SVC-01','SM-SVC-01-WF1',1,'{}','{}','Queued','00000000-0000-0000-0000-000000000001','x2')$q$, '{42501}');
ROLLBACK;
SELECT t_expect_error('TC-V12-I-003 no tenant context fails closed (error)', 'SELECT count(*) FROM growth_contact', '{42501}');
BEGIN; SELECT t_ctx('00000000-0000-0000-0000-00000000000b','{00000000-0000-0000-0000-0000000000c2}','00000000-0000-0000-0000-0000000000c2');
SELECT t_expect_error('TC-V12-I-004 tenant B cannot attach permission to tenant A role', $q$INSERT INTO role_permission VALUES ('00000000-0000-0000-0000-00000000000b','00000000-0000-0000-0000-0000000000f1','Billing:view')$q$, '{23503}');
SELECT t_expect_value('TC-V12-I-008 tenant B sees no tenant A inbox rows', 'SELECT count(*)::text FROM inbox', '0');
SELECT t_expect_value('TC-V12-I-009 tenant B sees no tenant A incidents', 'SELECT count(*)::text FROM incident', '0');
ROLLBACK;
BEGIN; SELECT t_ctx('00000000-0000-0000-0000-00000000000a','{00000000-0000-0000-0000-0000000000c1}','00000000-0000-0000-0000-0000000000c1');
SELECT t_expect_error('TC-V12-I-005 SoD bypass by UPDATE rejected', $q$UPDATE role_permission SET permission='Runs:approve' WHERE role_id='00000000-0000-0000-0000-0000000000f1' AND permission='Runs:read'$q$, '{23514}');
SELECT t_expect_error('TC-V12-I-006 SoD across two roles of one user rejected', $q$INSERT INTO user_role_assignment VALUES ('00000000-0000-0000-0000-00000000000a','00000000-0000-0000-0000-00000000001a','00000000-0000-0000-0000-0000000000f2','00000000-0000-0000-0000-0000000000aa',now(),NULL,NULL)$q$, '{23514}');
SELECT t_expect_error('TC-V12-I-006b self-granted role rejected', $q$INSERT INTO user_role_assignment VALUES ('00000000-0000-0000-0000-00000000000a','00000000-0000-0000-0000-0000000000aa','00000000-0000-0000-0000-0000000000f2','00000000-0000-0000-0000-0000000000aa',now(),NULL,NULL)$q$, '{23514}');
SELECT t_expect_error('TC-V12-I-007a direct audit INSERT denied to app role', $q$INSERT INTO audit_event(tenant_id,action) VALUES ('00000000-0000-0000-0000-00000000000a','x')$q$, '{42501}');
SELECT fn_append_audit('00000000-0000-0000-0000-0000000000c1','00000000-0000-0000-0000-0000000000aa','run.created','run:e1','workflow_run','POL-1','00000000-0000-0000-0000-0000000000cc','{"k":"v"}');
SELECT fn_append_audit('00000000-0000-0000-0000-0000000000c1','00000000-0000-0000-0000-0000000000aa','run.approved','run:e1','workflow_run','POL-1','00000000-0000-0000-0000-0000000000cc','{}');
SELECT t_expect_value('TC-V12-I-007b audit chain verifies', $q$SELECT bool_and(ok)::text FROM fn_verify_audit_chain('00000000-0000-0000-0000-00000000000a')$q$, 'true');
SELECT t_expect_error('TC-V12-I-007c audit UPDATE rejected', $q$UPDATE audit_event SET action='x'$q$, '{42501,P0001}');
SELECT t_expect_error('TC-V12-I-007d audit DELETE rejected', $q$DELETE FROM audit_event$q$, '{42501,P0001}');
SELECT set_config('app.actor_kind','service',true);
SELECT t_expect_error('TC-V12-I-008b unsigned inbound callback rejected', $q$INSERT INTO inbox(provider,provider_account,provider_event_id,tenant_id,signature_ok) VALUES ('razorpay','acct_a','evt_2','00000000-0000-0000-0000-00000000000a',false)$q$, '{23514}');
SELECT set_config('app.actor_kind','internal',true);
SELECT t_expect_error('TC-V12-I-010 portfolio wildcard grant rejected', $q$INSERT INTO portfolio_grant(portfolio_id,tenant_id,company_id,dimensions,expires_at) VALUES ('00000000-0000-0000-0000-00000000004a','00000000-0000-0000-0000-00000000000a','00000000-0000-0000-0000-0000000000c1','{*}',now()+interval '30 days')$q$, '{23514}');
SELECT t_expect_error('TC-V12-I-010b portfolio grant without expiry rejected', $q$INSERT INTO portfolio_grant(portfolio_id,tenant_id,company_id,dimensions) VALUES ('00000000-0000-0000-0000-00000000004a','00000000-0000-0000-0000-00000000000a','00000000-0000-0000-0000-0000000000c1','{revenue}')$q$, '{23514}');
SELECT t_expect_error('TC-V12-I-013 effect with run in another company rejected', $q$INSERT INTO effect(tenant_id,company_id,run_id,step_id,idempotency_key,preflight_verdict,status) VALUES ('00000000-0000-0000-0000-00000000000a','00000000-0000-0000-0000-0000000000c1','00000000-0000-0000-0000-0000000000e3','s1','eff-x','ALLOW','Intended')$q$, '{23503,42501}');
INSERT INTO effect(tenant_id,company_id,effect_id,run_id,step_id,idempotency_key,preflight_verdict,status) VALUES ('00000000-0000-0000-0000-00000000000a','00000000-0000-0000-0000-0000000000c1','00000000-0000-0000-0000-0000000000ef','00000000-0000-0000-0000-0000000000e1','s1','eff-1','ALLOW','Intended');
SELECT t_expect_error('TC-V12-I-013b effect Intended->Confirmed skip rejected', $q$UPDATE effect SET status='Confirmed' WHERE effect_id='00000000-0000-0000-0000-0000000000ef'$q$, '{23514}');
UPDATE effect SET status='Dispatched' WHERE effect_id='00000000-0000-0000-0000-0000000000ef';
SELECT t_expect_error('TC-V12-I-013c effect delete rejected', $q$DELETE FROM effect$q$, '{42501,P0001}');
SELECT t_expect_error('TC-V12-I-016a unknown schema_ref rejected', $q$INSERT INTO growth_contact(tenant_id,company_id,schema_ref,status,payload,created_by) VALUES ('00000000-0000-0000-0000-00000000000a','00000000-0000-0000-0000-0000000000c1','SM-SVC-99/x','draft','{}','00000000-0000-0000-0000-0000000000aa')$q$, '{23514}');
SELECT t_expect_error('TC-V12-I-016b status outside vocabulary rejected', $q$INSERT INTO growth_contact(tenant_id,company_id,schema_ref,status,payload,created_by) VALUES ('00000000-0000-0000-0000-00000000000a','00000000-0000-0000-0000-0000000000c1','SM-SVC-03/contact','sent','{"professional_name":"A"}','00000000-0000-0000-0000-0000000000aa')$q$, '{23514}');
SELECT t_expect_error('TC-V12-I-016c payload missing required key rejected', $q$INSERT INTO growth_contact(tenant_id,company_id,schema_ref,status,payload,created_by) VALUES ('00000000-0000-0000-0000-00000000000a','00000000-0000-0000-0000-0000000000c1','SM-SVC-03/contact','draft','{"x":1}','00000000-0000-0000-0000-0000000000aa')$q$, '{23514}');
INSERT INTO growth_contact(tenant_id,company_id,id,schema_ref,status,payload,created_by) VALUES ('00000000-0000-0000-0000-00000000000a','00000000-0000-0000-0000-0000000000c1','00000000-0000-0000-0000-00000000003a','SM-SVC-03/contact','draft','{"professional_name":"A"}','00000000-0000-0000-0000-0000000000aa');
SELECT t_expect_error('TC-V12-I-016d stale version update rejected', $q$UPDATE growth_contact SET status='verified', version=5 WHERE id='00000000-0000-0000-0000-00000000003a'$q$, '{40001}');
UPDATE growth_contact SET status='verified', version=2 WHERE id='00000000-0000-0000-0000-00000000003a';
SELECT t_expect_value('TC-V12-I-016e valid optimistic update accepted', $q$SELECT status FROM growth_contact WHERE id='00000000-0000-0000-0000-00000000003a'$q$, 'verified');
SELECT t_expect_error('TC-V12-I-017a amount without currency rejected', $q$INSERT INTO business_event(tenant_id,company_id,idempotency_key,event_type,amount_minor,occurred_at) VALUES ('00000000-0000-0000-0000-00000000000a','00000000-0000-0000-0000-0000000000c1','be1','deal_won',100000,now())$q$, '{23514}');
SELECT t_expect_error('TC-V12-I-017b demo fixture counted as live rejected', $q$INSERT INTO business_event(tenant_id,company_id,idempotency_key,event_type,source_kind,occurred_at) VALUES ('00000000-0000-0000-0000-00000000000a','00000000-0000-0000-0000-0000000000c1','be2','deal_won','demo_fixture',now())$q$, '{23514}');
INSERT INTO business_event(tenant_id,company_id,event_id,idempotency_key,event_type,run_id,amount_minor,currency,occurred_at) VALUES ('00000000-0000-0000-0000-00000000000a','00000000-0000-0000-0000-0000000000c1','00000000-0000-0000-0000-0000000000b9','be3','deal_won','00000000-0000-0000-0000-0000000000e1',100000,'INR',now());
SELECT t_expect_value('TC-V12-I-017c run-attributed event inherits evidenced SKU/WF only', $q$SELECT sku_id||'/'||wf_id||'/'||coalesce(offering_id::text,'null') FROM business_event WHERE event_id='00000000-0000-0000-0000-0000000000b9'$q$, 'SM-SVC-01/SM-SVC-01-WF1/null');
SELECT t_expect_error('TC-V12-I-017d business event immutable', $q$UPDATE business_event SET amount_minor=1$q$, '{42501,P0001}');
SELECT t_expect_error('TC-V12-I-018 experiment winner without independent decision rejected', $q$INSERT INTO experiment(tenant_id,company_id,name,hypothesis,primary_metric_id,primary_metric_version,allocation,consent_class,min_sample_per_arm,stopping_rule,max_duration_days,status,winner_arm,decided_by,created_by) VALUES ('00000000-0000-0000-0000-00000000000a','00000000-0000-0000-0000-0000000000c1','e','h','KPI-27',1,'{"A":0.5,"B":0.5}','analytics',100,'fixed horizon',14,'Concluded','B','00000000-0000-0000-0000-0000000000aa','00000000-0000-0000-0000-0000000000aa')$q$, '{23514}');
SELECT t_expect_error('TC-V12-I-019 missing survey response cannot carry a score', $q$INSERT INTO feedback_case(tenant_id,company_id,milestone,responded,consent_class,state,invited_at,nps) VALUES ('00000000-0000-0000-0000-00000000000a','00000000-0000-0000-0000-0000000000c1','renewal',false,'analytics','Expired',now(),10)$q$, '{23514}');
SELECT t_expect_error('TC-V12-I-020 export link longer than 7 days rejected', $q$INSERT INTO export_job(tenant_id,scope,format,requested_by,approved_by,approved_at,status,manifest_hash,expires_at) VALUES ('00000000-0000-0000-0000-00000000000a','full','parquet','00000000-0000-0000-0000-000000000001','00000000-0000-0000-0000-000000000002',now(),'Ready','\x01',now()+interval '8 days')$q$, '{23514}');
SELECT t_expect_error('TC-V12-I-021 API key lifetime > 397 days rejected', $q$INSERT INTO api_key(tenant_id,name,prefix,last4,key_hash,scopes,expires_at) VALUES ('00000000-0000-0000-0000-00000000000a','k','agx_1','abcd',digest('k','sha256'),'{runs:read}',now()+interval '2 years')$q$, '{23514}');
SELECT t_expect_error('TC-V12-I-023 AI step without prompt version rejected', $q$INSERT INTO workflow_step_run(tenant_id,company_id,run_id,step_id,step_class,status,model_id) VALUES ('00000000-0000-0000-0000-00000000000a','00000000-0000-0000-0000-0000000000c1','00000000-0000-0000-0000-0000000000e1','s2','ai_inference','Running','claude-sonnet')$q$, '{23514}');
SELECT t_expect_error('TC-V12-I-026 app role cannot DELETE business rows', $q$DELETE FROM growth_contact$q$, '{42501}');
SELECT t_expect_error('TC-V12-I-029 late-event aggregate v2 without reason rejected', $q$INSERT INTO metric_aggregate(tenant_id,company_id,metric_id,metric_version,period_start,dimension_hash,aggregate_version,numerator,denominator,source_event_count) VALUES ('00000000-0000-0000-0000-00000000000a','00000000-0000-0000-0000-0000000000c1','KPI-27',1,date_trunc('day',now()),'\x00',2,10,10,10)$q$, '{23514}');
SELECT t_expect_error('TC-V12-I-031 strictly necessary event carrying pseudonymous id rejected', $q$INSERT INTO journey_event(event_id,audience,tenant_id,consent_class,pseudonymous_ref,stage,occurred_at) VALUES (gen_random_uuid(),'subscriber','00000000-0000-0000-0000-00000000000a','necessary',digest('x','sha256'),'visit',now())$q$, '{23514}');
ROLLBACK;
RESET ROLE;
-- owner-level tests (platform / migration paths)
BEGIN; SELECT t_ctx('00000000-0000-0000-0000-00000000000a','{}','');
SELECT t_expect_error('TC-V12-I-011 cross-region tenant insert rejected in IN database', $q$INSERT INTO tenant VALUES (gen_random_uuid(),'client','EU','pending',now())$q$, '{23514}');
SELECT t_expect_error('TC-V12-I-012 data_region change rejected', $q$UPDATE tenant SET data_region='EU' WHERE tenant_id='00000000-0000-0000-0000-00000000000a'$q$, '{23514}');
SELECT t_expect_error('TC-V12-I-014 CERT-In deadline beyond 6 hours rejected', $q$INSERT INTO incident_notification VALUES ('00000000-0000-0000-0000-0000000000d9','CERT-In',now()+interval '7 hours',NULL,NULL)$q$, '{23514}');
UPDATE tenant_key_config SET key_state='revoked' WHERE tenant_id='00000000-0000-0000-0000-00000000000a';
SELECT t_expect_value('TC-V12-I-015 key revocation crypto-shreds tenant DEKs', $q$SELECT count(*)::text FROM tenant_data_key WHERE tenant_id='00000000-0000-0000-0000-00000000000a' AND wrapped_dek IS NULL AND destroyed_at IS NOT NULL$q$, '1');
SELECT t_expect_error('TC-V12-I-022 Tier 2 model with Confidential data rejected', $q$INSERT INTO ai_model VALUES ('free-x','T2','vendor','1','{ap-south-1}','{Public,Confidential}',8000,NULL,'Candidate',NULL)$q$, '{23514}');
SELECT t_expect_error('TC-V12-I-024 workflow configuration SKU/WF mismatch rejected', $q$INSERT INTO workflow_configuration(tenant_id,company_id,offering_id,market_id,sku_id,wf_id,wf_version,budget_minor,currency,authority,status,config_revision_id) VALUES ('00000000-0000-0000-0000-00000000000a','00000000-0000-0000-0000-0000000000c1',gen_random_uuid(),gen_random_uuid(),'SM-SVC-01','SM-SVC-02-WF1',1,0,'INR','L1','Draft',gen_random_uuid())$q$, '{23514,23503}');
SELECT t_expect_error('TC-V12-I-030 brand from another company rejected', $q$INSERT INTO offering(tenant_id,company_id,brand_id,offering_type,status) VALUES ('00000000-0000-0000-0000-00000000000a','00000000-0000-0000-0000-0000000000c1',gen_random_uuid(),'service','draft')$q$, '{23503,42501}');
ROLLBACK;
SELECT t_expect_value('TC-V12-I-025 Supabase anon/authenticated hold no table privileges', $q$SELECT count(*)::text FROM pg_class c, LATERAL (VALUES ('anon'),('authenticated')) r(n) WHERE c.relnamespace='public'::regnamespace AND c.relkind='r' AND has_table_privilege(r.n, c.oid, 'SELECT,INSERT,UPDATE,DELETE')$q$, '0');
SELECT t_expect_value('TC-V12-I-027 CI guard: tenant tables without RLS+FORCE', $q$SELECT count(*)::text FROM pg_class c JOIN pg_attribute a ON a.attrelid=c.oid AND a.attname='tenant_id' WHERE c.relnamespace='public'::regnamespace AND c.relkind='r' AND NOT (c.relrowsecurity AND c.relforcerowsecurity) AND c.relname NOT IN ('customer_value_x')$q$, '0');
SELECT t_expect_value('TC-V12-I-028 CI guard: foreign keys without supporting index', $q$SELECT count(*)::text FROM pg_constraint c WHERE contype='f' AND connamespace='public'::regnamespace AND NOT EXISTS (SELECT 1 FROM pg_index i WHERE i.indrelid=c.conrelid AND (i.indkey::int2[])[0:array_length(c.conkey,1)-1] @> c.conkey AND (i.indkey::int2[])[0:array_length(c.conkey,1)-1] <@ c.conkey)$q$, '0');
SELECT t_expect_value('TC-V12-I-027b CI guard: tenant-scoped tables without a SELECT policy', $q$SELECT count(*)::text FROM pg_class c JOIN pg_attribute a ON a.attrelid=c.oid AND a.attname='tenant_id' WHERE c.relnamespace='public'::regnamespace AND c.relkind='r' AND NOT EXISTS (SELECT 1 FROM pg_policies p WHERE p.tablename=c.relname AND p.cmd IN ('SELECT','ALL'))$q$, '0');
\echo 'ALL TC-V12-I TESTS EXECUTED'
