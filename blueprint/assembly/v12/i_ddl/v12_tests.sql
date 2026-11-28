-- Reproduction of FSD V12 ch26 DB-T1..T9 and C2-T1..T11 on PostgreSQL 16.15 (Group I, Part 11.9)
\set ON_ERROR_STOP off
\pset format unaligned
DO $$ BEGIN IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname='app_user') THEN CREATE ROLE app_user NOLOGIN; END IF; END $$;
GRANT USAGE ON SCHEMA public TO app_user;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO app_user;
GRANT USAGE ON ALL SEQUENCES IN SCHEMA public TO app_user;
-- fixtures as owner (RLS forced: owner must set context)
BEGIN;
SET LOCAL app.tenant_id='00000000-0000-0000-0000-00000000000a';
INSERT INTO tenant VALUES ('00000000-0000-0000-0000-00000000000a','owned','IN','active',now()),('00000000-0000-0000-0000-00000000000b','client','IN','active',now()) ON CONFLICT DO NOTHING;
INSERT INTO organization(tenant_id,organization_id,name) VALUES ('00000000-0000-0000-0000-00000000000a','00000000-0000-0000-0000-0000000000a1','Org A') ON CONFLICT DO NOTHING;
INSERT INTO company(tenant_id,company_id,organization_id,legal_name) VALUES ('00000000-0000-0000-0000-00000000000a','00000000-0000-0000-0000-0000000000c1','00000000-0000-0000-0000-0000000000a1','Co A') ON CONFLICT DO NOTHING;
COMMIT;
BEGIN; SET LOCAL app.tenant_id='00000000-0000-0000-0000-00000000000b';
INSERT INTO organization(tenant_id,organization_id,name) VALUES ('00000000-0000-0000-0000-00000000000b','00000000-0000-0000-0000-0000000000b1','Org B') ON CONFLICT DO NOTHING;
INSERT INTO company(tenant_id,company_id,organization_id,legal_name) VALUES ('00000000-0000-0000-0000-00000000000b','00000000-0000-0000-0000-0000000000c2','00000000-0000-0000-0000-0000000000b1','Co B') ON CONFLICT DO NOTHING;
COMMIT;
SET ROLE app_user;
\echo 'DB-T1 expect error (composite FK)'
BEGIN; SET LOCAL app.tenant_id='00000000-0000-0000-0000-00000000000a';
INSERT INTO company(tenant_id,company_id,organization_id,legal_name) VALUES ('00000000-0000-0000-0000-00000000000a',gen_random_uuid(),'00000000-0000-0000-0000-0000000000b1','X'); ROLLBACK;
\echo 'DB-T2 expect error (no context)'
SELECT count(*) FROM company;
\echo 'DB-T3 expect 1'
BEGIN; SET LOCAL app.tenant_id='00000000-0000-0000-0000-00000000000a'; SELECT count(*) FROM company; COMMIT;
\echo 'DB-T4 expect RLS error'
BEGIN; SET LOCAL app.tenant_id='00000000-0000-0000-0000-00000000000a';
INSERT INTO organization(tenant_id,name) VALUES ('00000000-0000-0000-0000-00000000000b','Sneaky'); ROLLBACK;
\echo 'DB-T5 expect check error'
BEGIN; SET LOCAL app.tenant_id='00000000-0000-0000-0000-00000000000a';
INSERT INTO workflow_run(tenant_id,company_id,sku_id,wf_id,wf_version,business_context,input,status,requested_by,reviewed_by,idempotency_key)
VALUES ('00000000-0000-0000-0000-00000000000a','00000000-0000-0000-0000-0000000000c1','SM-SVC-01','SM-SVC-01-WF1',1,'{}','{}','Queued','00000000-0000-0000-0000-000000000001','00000000-0000-0000-0000-000000000001','k1'); ROLLBACK;
\echo 'DB-T6 expect check error'
BEGIN; SET LOCAL app.tenant_id='00000000-0000-0000-0000-00000000000a';
INSERT INTO effect(tenant_id,run_id,step_id,idempotency_key,preflight_verdict,status) VALUES ('00000000-0000-0000-0000-00000000000a',gen_random_uuid(),'s1','e1','HOLD','Intended'); ROLLBACK;
\echo 'DB-T7 expect check error'
BEGIN; SET LOCAL app.tenant_id='00000000-0000-0000-0000-00000000000a';
INSERT INTO workflow_run(tenant_id,company_id,run_id,sku_id,wf_id,wf_version,business_context,input,status,requested_by,idempotency_key)
VALUES ('00000000-0000-0000-0000-00000000000a','00000000-0000-0000-0000-0000000000c1','00000000-0000-0000-0000-0000000000e1','SM-SVC-01','SM-SVC-01-WF1',1,'{}','{}','Queued','00000000-0000-0000-0000-000000000001','k7');
INSERT INTO workflow_step_run(tenant_id,run_id,step_id,step_class,status,model_id) VALUES ('00000000-0000-0000-0000-00000000000a','00000000-0000-0000-0000-0000000000e1','s1','deterministic','Running','m1'); ROLLBACK;
\echo 'DB-T8 expect unique error'
BEGIN; SET LOCAL app.tenant_id='00000000-0000-0000-0000-00000000000a';
INSERT INTO workflow_run(tenant_id,company_id,sku_id,wf_id,wf_version,business_context,input,status,requested_by,idempotency_key)
VALUES ('00000000-0000-0000-0000-00000000000a','00000000-0000-0000-0000-0000000000c1','SM-SVC-01','SM-SVC-01-WF1',1,'{}','{}','Queued','00000000-0000-0000-0000-000000000001','dup');
INSERT INTO workflow_run(tenant_id,company_id,sku_id,wf_id,wf_version,business_context,input,status,requested_by,idempotency_key)
VALUES ('00000000-0000-0000-0000-00000000000a','00000000-0000-0000-0000-0000000000c1','SM-SVC-01','SM-SVC-01-WF1',1,'{}','{}','Queued','00000000-0000-0000-0000-000000000001','dup'); ROLLBACK;
\echo 'DB-T9 expect 0'
BEGIN; SET LOCAL app.tenant_id='00000000-0000-0000-0000-00000000000a';
INSERT INTO workflow_run(tenant_id,company_id,sku_id,wf_id,wf_version,business_context,input,status,requested_by,idempotency_key)
VALUES ('00000000-0000-0000-0000-00000000000a','00000000-0000-0000-0000-0000000000c1','SM-SVC-01','SM-SVC-01-WF1',1,'{}','{}','Queued','00000000-0000-0000-0000-000000000001','t9'); COMMIT;
BEGIN; SET LOCAL app.tenant_id='00000000-0000-0000-0000-00000000000b'; SELECT count(*) FROM workflow_run; COMMIT;
\echo 'C2-T1 expect SoD error'
BEGIN; SET LOCAL app.tenant_id='00000000-0000-0000-0000-00000000000a';
INSERT INTO custom_role(tenant_id,role_id,name) VALUES ('00000000-0000-0000-0000-00000000000a','00000000-0000-0000-0000-0000000000f1','Ops');
INSERT INTO role_permission VALUES ('00000000-0000-0000-0000-00000000000a','00000000-0000-0000-0000-0000000000f1','Runs:create');
INSERT INTO role_permission VALUES ('00000000-0000-0000-0000-00000000000a','00000000-0000-0000-0000-0000000000f1','Runs:approve'); ROLLBACK;
\echo 'C2-T2 expect check error'
BEGIN; SET LOCAL app.tenant_id='00000000-0000-0000-0000-00000000000a';
INSERT INTO export_job(tenant_id,scope,format,requested_by,approved_by,status) VALUES ('00000000-0000-0000-0000-00000000000a','full','jsonl','00000000-0000-0000-0000-000000000001','00000000-0000-0000-0000-000000000001','Running'); ROLLBACK;
\echo 'C2-T3 expect check error'
BEGIN; SET LOCAL app.tenant_id='00000000-0000-0000-0000-00000000000a';
INSERT INTO sandbox_environment(tenant_id,sandbox_id,name,copies_configuration) VALUES ('00000000-0000-0000-0000-00000000000a','00000000-0000-0000-0000-0000000000d1','sb',true);
INSERT INTO config_promotion(tenant_id,sandbox_id,requested_by,approved_by,status) VALUES ('00000000-0000-0000-0000-00000000000a','00000000-0000-0000-0000-0000000000d1','00000000-0000-0000-0000-000000000001','00000000-0000-0000-0000-000000000001','Approved'); ROLLBACK;
\echo 'C2-T4 expect check error'
BEGIN; SET LOCAL app.tenant_id='00000000-0000-0000-0000-00000000000a';
INSERT INTO identity_provider VALUES ('00000000-0000-0000-0000-00000000000a','SAML 2.0','https://idp.example','iss','example.com',false,NULL,true,'required',8,30); ROLLBACK;
\echo 'C2-T5 expect check error'
BEGIN; SET LOCAL app.tenant_id='00000000-0000-0000-0000-00000000000a';
INSERT INTO sandbox_environment(tenant_id,name,copies_configuration,contains_personal_data) VALUES ('00000000-0000-0000-0000-00000000000a','sb',true,true); ROLLBACK;
\echo 'C2-T6 expect check error'
BEGIN; SET LOCAL app.tenant_id='00000000-0000-0000-0000-00000000000a';
INSERT INTO connector_installation(tenant_id,connector_id,environment,credential_ref,status) VALUES ('00000000-0000-0000-0000-00000000000a','crm','production','vault://x','Active'); ROLLBACK;
\echo 'C2-T7 expect check error'
BEGIN; INSERT INTO security_finding(title,severity,found_at,due_at) VALUES ('x','Critical','2026-11-01','2026-11-20'); ROLLBACK;
\echo 'C2-T8 expect check error'
BEGIN; SET LOCAL app.tenant_id='00000000-0000-0000-0000-00000000000a';
INSERT INTO invoice(tenant_id,number,currency,net_minor,tax_minor,total_minor,status) VALUES ('00000000-0000-0000-0000-00000000000a','INV-1','INR',1000,180,1000,'Issued'); ROLLBACK;
\echo 'C2-T9 expect 0'
SELECT count(*) FROM information_schema.columns WHERE table_name='api_key' AND column_name IN ('key','api_key','plaintext_key','secret');
\echo 'C2-T10 expect 0 then error'
BEGIN; SET LOCAL app.tenant_id='00000000-0000-0000-0000-00000000000a';
INSERT INTO api_key(tenant_id,name,prefix,last4,key_hash,scopes,expires_at) VALUES ('00000000-0000-0000-0000-00000000000a','k','agx','abcd','\x00','{runs:read}',now()+interval '90 days'); COMMIT;
BEGIN; SET LOCAL app.tenant_id='00000000-0000-0000-0000-00000000000b'; SELECT count(*) FROM api_key; COMMIT;
SELECT count(*) FROM api_key;
\echo 'C2-T11 expect accepted'
BEGIN; SET LOCAL app.tenant_id='00000000-0000-0000-0000-00000000000a';
INSERT INTO custom_role(tenant_id,role_id,name) VALUES ('00000000-0000-0000-0000-00000000000a','00000000-0000-0000-0000-0000000000f2','Viewer');
INSERT INTO role_permission VALUES ('00000000-0000-0000-0000-00000000000a','00000000-0000-0000-0000-0000000000f2','Runs:read');
INSERT INTO invoice(tenant_id,number,currency,net_minor,tax_minor,total_minor,status) VALUES ('00000000-0000-0000-0000-00000000000a','INV-2','INR',1000,180,1180,'Issued');
SELECT 'accepted'; ROLLBACK;
RESET ROLE;
