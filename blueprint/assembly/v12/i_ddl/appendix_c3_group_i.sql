-- =====================================================================================
-- DDL-V12-I  "Appendix C3" addendum (Group I, Part 11.9). Apply after FSD V12 Appendix C and C2.
-- Tested on PostgreSQL 16.15 (scratch cluster), as owner for DDL and as role ge_app for tests.
-- Target: Supabase Pro PostgreSQL, Mumbai region (DEC-421). Production schema `ge` (not `public`);
-- this reference run uses `public` so that it applies unchanged on top of Appendix C/C2.
-- Every statement is idempotent where PostgreSQL allows it. Not a Django migration (MT-36 approval).
-- =====================================================================================

-- C3-01 Roles. Supabase creates anon, authenticated, service_role; emulate them for the reference run.
DO $$ BEGIN
  IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname='anon') THEN CREATE ROLE anon NOLOGIN; END IF;
  IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname='authenticated') THEN CREATE ROLE authenticated NOLOGIN; END IF;
  IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname='ge_owner') THEN CREATE ROLE ge_owner NOLOGIN NOBYPASSRLS; END IF;
  IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname='ge_app') THEN CREATE ROLE ge_app NOLOGIN NOBYPASSRLS; END IF;          -- LOGIN in production via Supavisor
  IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname='ge_worker') THEN CREATE ROLE ge_worker NOLOGIN NOBYPASSRLS; END IF;
  IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname='ge_readonly') THEN CREATE ROLE ge_readonly NOLOGIN NOBYPASSRLS; END IF;
  IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname='ge_retention') THEN CREATE ROLE ge_retention NOLOGIN NOBYPASSRLS; END IF;
  IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname='ge_audit_writer') THEN CREATE ROLE ge_audit_writer NOLOGIN NOBYPASSRLS; END IF;
  IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname='ge_platform_sec') THEN CREATE ROLE ge_platform_sec NOLOGIN NOBYPASSRLS; END IF;
END $$;
-- The Supabase Data API (PostgREST) must never reach business tables: no grants to anon/authenticated/PUBLIC.
REVOKE ALL ON ALL TABLES IN SCHEMA public FROM PUBLIC, anon, authenticated;
REVOKE ALL ON ALL SEQUENCES IN SCHEMA public FROM PUBLIC, anon, authenticated;
REVOKE ALL ON ALL FUNCTIONS IN SCHEMA public FROM PUBLIC, anon, authenticated;
ALTER DEFAULT PRIVILEGES IN SCHEMA public REVOKE ALL ON TABLES FROM PUBLIC, anon, authenticated;
ALTER DEFAULT PRIVILEGES IN SCHEMA public REVOKE EXECUTE ON FUNCTIONS FROM PUBLIC, anon, authenticated;
GRANT USAGE ON SCHEMA public TO ge_app, ge_worker, ge_readonly, ge_retention, ge_audit_writer, ge_platform_sec;
GRANT EXECUTE ON FUNCTION digest(bytea, text), digest(text, text), hmac(bytea, bytea, text), gen_random_bytes(int) TO ge_app, ge_worker;   -- pgcrypto, after the PUBLIC revoke

-- C3-02 Context functions (fail closed). app_tenant() raises when the context is missing (V12 DB-T2 semantics);
-- company and write-scope helpers return an empty set / NULL so that predicates evaluate to false.
CREATE OR REPLACE FUNCTION app_tenant() RETURNS uuid LANGUAGE plpgsql STABLE AS $$
DECLARE v text := current_setting('app.tenant_id', true);
BEGIN
  IF v IS NULL OR v = '' THEN RAISE EXCEPTION 'tenant context missing' USING ERRCODE = '42501'; END IF;
  RETURN v::uuid;
END $$;
CREATE OR REPLACE FUNCTION app_company_ids() RETURNS uuid[] LANGUAGE sql STABLE AS
$$ SELECT COALESCE(NULLIF(current_setting('app.company_ids', true), '')::uuid[], '{}'::uuid[]) $$;
CREATE OR REPLACE FUNCTION app_write_company() RETURNS uuid LANGUAGE sql STABLE AS
$$ SELECT NULLIF(current_setting('app.write_company_id', true), '')::uuid $$;
CREATE OR REPLACE FUNCTION app_actor_id() RETURNS uuid LANGUAGE sql STABLE AS
$$ SELECT NULLIF(current_setting('app.actor_id', true), '')::uuid $$;
CREATE OR REPLACE FUNCTION app_actor_kind() RETURNS text LANGUAGE sql STABLE AS
$$ SELECT COALESCE(NULLIF(current_setting('app.actor_kind', true), ''), 'none') $$;
CREATE OR REPLACE FUNCTION app_portfolio_id() RETURNS uuid LANGUAGE sql STABLE AS
$$ SELECT NULLIF(current_setting('app.portfolio_id', true), '')::uuid $$;
GRANT EXECUTE ON FUNCTION app_tenant(), app_company_ids(), app_write_company(), app_actor_id(), app_actor_kind(), app_portfolio_id()
  TO ge_app, ge_worker, ge_readonly, ge_retention, ge_audit_writer;

-- C3-03 Scope integrity: NOT NULL scope keys and composite (tenant-pinned) foreign keys.
ALTER TABLE outbox ALTER COLUMN tenant_id SET NOT NULL;
ALTER TABLE portfolio_grant ALTER COLUMN tenant_id SET NOT NULL, ALTER COLUMN company_id SET NOT NULL, ALTER COLUMN portfolio_id SET NOT NULL;
ALTER TABLE portfolio_grant ADD CONSTRAINT portfolio_grant_company_fk FOREIGN KEY (tenant_id, company_id) REFERENCES company(tenant_id, company_id);
ALTER TABLE portfolio_grant ADD CONSTRAINT portfolio_grant_no_wildcard CHECK (cardinality(dimensions) > 0 AND NOT ('*' = ANY (dimensions)));
ALTER TABLE portfolio_grant ADD CONSTRAINT portfolio_grant_expiry_required CHECK (expires_at IS NOT NULL);
ALTER TABLE custom_role ADD CONSTRAINT custom_role_tenant_role_uq UNIQUE (tenant_id, role_id);
ALTER TABLE role_permission DROP CONSTRAINT role_permission_role_id_fkey;
ALTER TABLE role_permission DROP CONSTRAINT role_permission_pkey;
ALTER TABLE role_permission ADD CONSTRAINT role_permission_pkey PRIMARY KEY (tenant_id, role_id, permission);  -- no cross-tenant uniqueness oracle
ALTER TABLE role_permission ADD CONSTRAINT role_permission_role_fk FOREIGN KEY (tenant_id, role_id) REFERENCES custom_role(tenant_id, role_id);
ALTER TABLE role_permission ADD CONSTRAINT role_permission_format CHECK (permission ~ '^[A-Z][A-Za-z]+:[a-z]+$');
ALTER TABLE webhook_endpoint ADD CONSTRAINT webhook_endpoint_tenant_uq UNIQUE (tenant_id, endpoint_id);
ALTER TABLE webhook_delivery DROP CONSTRAINT webhook_delivery_endpoint_id_fkey;
ALTER TABLE webhook_delivery ADD CONSTRAINT webhook_delivery_endpoint_fk FOREIGN KEY (tenant_id, endpoint_id) REFERENCES webhook_endpoint(tenant_id, endpoint_id);
ALTER TABLE sandbox_environment ADD CONSTRAINT sandbox_environment_tenant_uq UNIQUE (tenant_id, sandbox_id);
ALTER TABLE config_promotion DROP CONSTRAINT config_promotion_sandbox_id_fkey;
ALTER TABLE config_promotion ADD CONSTRAINT config_promotion_sandbox_fk FOREIGN KEY (tenant_id, sandbox_id) REFERENCES sandbox_environment(tenant_id, sandbox_id);
-- company scope on run children (company isolation of steps and effects)
ALTER TABLE workflow_run ADD CONSTRAINT workflow_run_company_run_uq UNIQUE (tenant_id, company_id, run_id);
ALTER TABLE workflow_step_run ADD COLUMN IF NOT EXISTS company_id uuid;
ALTER TABLE effect ADD COLUMN IF NOT EXISTS company_id uuid;
ALTER TABLE effect ADD CONSTRAINT effect_run_fk FOREIGN KEY (tenant_id, company_id, run_id) REFERENCES workflow_run(tenant_id, company_id, run_id);
ALTER TABLE workflow_step_run ADD CONSTRAINT workflow_step_run_company_fk FOREIGN KEY (tenant_id, company_id, run_id) REFERENCES workflow_run(tenant_id, company_id, run_id);
ALTER TABLE workflow_step_run ALTER COLUMN company_id SET NOT NULL;
ALTER TABLE effect ALTER COLUMN company_id SET NOT NULL;
ALTER TABLE consent_record ALTER COLUMN company_id SET NOT NULL;
ALTER TABLE consent_record ADD CONSTRAINT consent_record_contact_fk FOREIGN KEY (tenant_id, contact_id) REFERENCES growth_contact(tenant_id, id);
-- outbox / audit / usage carry company for company-level RLS where the event is company-scoped
ALTER TABLE outbox ADD COLUMN IF NOT EXISTS company_id uuid;
ALTER TABLE outbox ADD COLUMN IF NOT EXISTS dedup_key text;
ALTER TABLE outbox ADD COLUMN IF NOT EXISTS correlation_id uuid;
ALTER TABLE outbox ADD COLUMN IF NOT EXISTS attempts int NOT NULL DEFAULT 0 CHECK (attempts BETWEEN 0 AND 20);
ALTER TABLE outbox ADD COLUMN IF NOT EXISTS next_attempt_at timestamptz NOT NULL DEFAULT now();
ALTER TABLE outbox ADD CONSTRAINT outbox_dedup_uq UNIQUE (tenant_id, dedup_key);
-- inbox: dedupe per provider ACCOUNT (Part 3.3 UQ-IDEM-01) and reject unsigned rows
ALTER TABLE inbox ADD COLUMN IF NOT EXISTS provider_account text NOT NULL DEFAULT 'unknown';
ALTER TABLE inbox DROP CONSTRAINT inbox_pkey;
ALTER TABLE inbox ADD CONSTRAINT inbox_pkey PRIMARY KEY (provider, provider_account, provider_event_id);
ALTER TABLE inbox ADD CONSTRAINT inbox_signature_required CHECK (signature_ok);
ALTER TABLE inbox ADD COLUMN IF NOT EXISTS payload_ref text;
ALTER TABLE inbox ADD COLUMN IF NOT EXISTS processed_at timestamptz;

-- C3-04 Enumerations and value rules missing from Appendix C/C2 (CHECK constraints)
ALTER TABLE tenant ADD CONSTRAINT tenant_customer_type_ck CHECK (customer_type IN ('owned','client'));
ALTER TABLE tenant ADD CONSTRAINT tenant_contract_status_ck CHECK (contract_status IN ('pending','trial','active','suspended','offboarding','closed'));
ALTER TABLE company ADD CONSTRAINT company_status_ck CHECK (status IN ('draft','active','suspended','archived'));
ALTER TABLE company ADD CONSTRAINT company_country_ck CHECK (registration_country IS NULL OR registration_country ~ '^[A-Z]{2}$');
ALTER TABLE offering ADD CONSTRAINT offering_type_ck CHECK (offering_type IN ('product','service','programme','solution'));
ALTER TABLE offering ADD CONSTRAINT offering_status_ck CHECK (status IN ('draft','pending_approval','approved','published','retired'));
ALTER TABLE offering ADD CONSTRAINT offering_price_ck CHECK (price_amount IS NULL OR (price_amount >= 0 AND currency IS NOT NULL));
ALTER TABLE offering ADD CONSTRAINT offering_version_ck CHECK (version >= 1);
ALTER TABLE market ADD CONSTRAINT market_country_ck CHECK (country ~ '^[A-Z]{2}$');
ALTER TABLE market ADD CONSTRAINT market_currency_ck CHECK (currency ~ '^[A-Z]{3}$');
ALTER TABLE market ADD CONSTRAINT market_timezone_ck CHECK (timezone ~ '^[A-Za-z]+(/[A-Za-z0-9_+-]+)+$' OR timezone = 'UTC');
ALTER TABLE channel_account ADD CONSTRAINT channel_account_channel_ck CHECK (channel IN ('email','whatsapp','sms','rcs','voice','linkedin','social','web_chat'));
ALTER TABLE channel_account ADD CONSTRAINT channel_account_status_ck CHECK (status IN ('pending_verification','active','paused','suspended','retired'));
ALTER TABLE channel_account ADD CONSTRAINT channel_account_credential_ref_ck CHECK (credential_ref ~ '^(vault|sm|kms|aws-sm)://');
ALTER TABLE workflow_step_run ADD CONSTRAINT workflow_step_run_status_ck CHECK (status IN ('Pending','Running','Succeeded','Failed','Skipped','Held','Compensated'));
ALTER TABLE workflow_step_run ADD CONSTRAINT workflow_step_run_ai_trace_ck CHECK (step_class <> 'ai_inference' OR (model_id IS NOT NULL AND prompt_version IS NOT NULL));
ALTER TABLE workflow_step_run ADD CONSTRAINT workflow_step_run_attempt_ck CHECK (attempt BETWEEN 1 AND 3);
ALTER TABLE workflow_run ADD CONSTRAINT workflow_run_wf_ck CHECK (wf_id ~ '^SM-SVC-\d{2}-WF0?[1-4]$' AND wf_version >= 1 AND reserved_units >= 0);
ALTER TABLE workflow_run ADD CONSTRAINT workflow_run_wf_matches_sku_ck CHECK (left(wf_id, 9) = sku_id);
ALTER TABLE consent_record ADD CONSTRAINT consent_record_channel_ck CHECK (channel IN ('email','whatsapp','sms','rcs','voice','linkedin','social','web_chat','any'));
ALTER TABLE consent_record ADD CONSTRAINT consent_record_basis_ck CHECK (basis IN ('consent','legitimate_use','contract','legal_obligation','legitimate_interest'));
ALTER TABLE consent_record ADD CONSTRAINT consent_record_market_ck CHECK (market ~ '^[A-Z]{2}$');
ALTER TABLE consent_record ADD CONSTRAINT consent_record_hash_ck CHECK (octet_length(evidence_hash) = 32);
ALTER TABLE suppression ADD CONSTRAINT suppression_reason_ck CHECK (reason IN ('opt_out','complaint','bounce','erasure','legal','minor','manual'));
ALTER TABLE dsar_request ADD CONSTRAINT dsar_type_ck CHECK (request_type IN ('access','correction','erasure','portability','grievance','nomination','withdraw_consent','objection'));
ALTER TABLE dsar_request ADD CONSTRAINT dsar_status_ck CHECK (status IN ('Received','Identity pending','In progress','On hold (legal)','Completed','Rejected'));
ALTER TABLE dsar_request ADD CONSTRAINT dsar_due_ck CHECK (due_at > received_at);
ALTER TABLE dsar_request ADD CONSTRAINT dsar_identity_before_completion_ck CHECK (status <> 'Completed' OR (identity_verified_at IS NOT NULL AND evidence_ref IS NOT NULL));
ALTER TABLE dsar_request ADD CONSTRAINT dsar_hold_ck CHECK (status <> 'On hold (legal)' OR legal_hold);
ALTER TABLE incident ADD CONSTRAINT incident_severity_ck CHECK (severity IN ('SEV1','SEV2','SEV3','SEV4'));
ALTER TABLE incident ADD CONSTRAINT incident_time_ck CHECK (aware_at >= detected_at);
ALTER TABLE incident_notification ADD CONSTRAINT incident_notification_authority_ck CHECK (authority IN ('CERT-In','DPB-India','EU-SA','UK-ICO','Data-principals','Customer-controller','Other'));
ALTER TABLE ai_model ADD CONSTRAINT ai_model_tier_ck CHECK (tier IN ('T0','T1a','T1b','T2','T3'));
ALTER TABLE ai_model ADD CONSTRAINT ai_model_t2_data_ck CHECK (tier <> 'T2' OR data_classes <@ ARRAY['Public','Internal-non-personal']::text[]);
ALTER TABLE ai_usage_event ADD CONSTRAINT ai_usage_tokens_ck CHECK (input_tokens >= 0 AND output_tokens >= 0 AND cached_tokens >= 0 AND (latency_ms IS NULL OR latency_ms >= 0));
ALTER TABLE ai_usage_event ADD CONSTRAINT ai_usage_outcome_ck CHECK (outcome IS NULL OR outcome IN ('ok','schema_invalid','refused','timeout','error','cached','degraded'));
ALTER TABLE prompt_version ADD CONSTRAINT prompt_version_status_ck CHECK (status IN ('Draft','In evaluation','Approved','Suspended','Retired'));
ALTER TABLE prompt_version ADD CONSTRAINT prompt_version_hash_ck CHECK (octet_length(template_hash) = 32);
ALTER TABLE eval_suite ADD CONSTRAINT eval_suite_count_ck CHECK (case_count > 0);
ALTER TABLE eval_run ADD CONSTRAINT eval_run_denominator_ck CHECK (denominator > 0);
ALTER TABLE connector_installation ADD CONSTRAINT connector_status_ck CHECK (status IN ('Requested','In review','Active','Suspended','Removed'));
ALTER TABLE config_promotion ADD CONSTRAINT config_promotion_status_ck CHECK (status IN ('Requested','Approved','Rejected','Applied','Rolled back'));
ALTER TABLE config_promotion ADD CONSTRAINT config_promotion_approved_ck CHECK (status NOT IN ('Approved','Applied') OR approved_by IS NOT NULL);
ALTER TABLE export_job ADD CONSTRAINT export_job_ready_ck CHECK (status <> 'Ready' OR (approved_by IS NOT NULL AND manifest_hash IS NOT NULL AND expires_at IS NOT NULL));
ALTER TABLE export_job ADD COLUMN IF NOT EXISTS approved_at timestamptz;
ALTER TABLE export_job ADD CONSTRAINT export_job_link_7d_ck CHECK (expires_at IS NULL OR (approved_at IS NOT NULL AND expires_at <= approved_at + interval '7 days'));
ALTER TABLE invoice ADD CONSTRAINT invoice_status_ck CHECK (status IN ('Draft','Issued','Paid','Partially paid','Void','Credited'));
ALTER TABLE invoice ADD CONSTRAINT invoice_currency_ck CHECK (currency ~ '^[A-Z]{3}$');
ALTER TABLE fx_rate ALTER COLUMN base_currency SET NOT NULL, ALTER COLUMN quote_currency SET NOT NULL;
ALTER TABLE fx_rate ADD CONSTRAINT fx_rate_ccy_ck CHECK (base_currency ~ '^[A-Z]{3}$' AND quote_currency ~ '^[A-Z]{3}$' AND base_currency <> quote_currency);
ALTER TABLE fx_rate ADD CONSTRAINT fx_rate_version_uq UNIQUE (base_currency, quote_currency, effective_at, approved_version);
ALTER TABLE api_key ADD CONSTRAINT api_key_prefix_uq UNIQUE (prefix);
ALTER TABLE api_key ADD CONSTRAINT api_key_hash_uq UNIQUE (key_hash);
ALTER TABLE api_key ADD CONSTRAINT api_key_hash_len_ck CHECK (octet_length(key_hash) = 32);
ALTER TABLE api_key ADD COLUMN IF NOT EXISTS created_at timestamptz NOT NULL DEFAULT now();
ALTER TABLE api_key ADD CONSTRAINT api_key_max_life_ck CHECK (expires_at <= created_at + interval '397 days');
ALTER TABLE scim_token ADD CONSTRAINT scim_token_hash_uq UNIQUE (token_hash);
ALTER TABLE scim_token ADD COLUMN IF NOT EXISTS expires_at timestamptz NOT NULL DEFAULT (now() + interval '365 days');
ALTER TABLE scim_token ADD CONSTRAINT scim_token_life_ck CHECK (expires_at <= created_at + interval '397 days');
ALTER TABLE webhook_endpoint ADD COLUMN IF NOT EXISTS verified_at timestamptz;
ALTER TABLE webhook_endpoint ADD CONSTRAINT webhook_active_verified_ck CHECK (NOT active OR verified_at IS NOT NULL);
ALTER TABLE webhook_delivery ADD COLUMN IF NOT EXISTS event_id uuid NOT NULL DEFAULT gen_random_uuid();
ALTER TABLE webhook_delivery ADD CONSTRAINT webhook_delivery_attempt_uq UNIQUE (tenant_id, endpoint_id, event_id, attempt);
ALTER TABLE tenant_key_config ADD COLUMN IF NOT EXISTS provider text;
ALTER TABLE tenant_key_config ADD CONSTRAINT tenant_key_provider_ck CHECK ((mode = 'platform' AND provider IS NULL) OR (mode = 'customer' AND provider IN ('aws-kms','azure-key-vault','gcp-kms')));
ALTER TABLE tenant_key_config ADD COLUMN IF NOT EXISTS key_state text NOT NULL DEFAULT 'active' CHECK (key_state IN ('pending_validation','active','rotating','revoked','failed'));
ALTER TABLE tenant_key_config ADD COLUMN IF NOT EXISTS revoked_at timestamptz;
ALTER TABLE sandbox_environment ADD COLUMN IF NOT EXISTS created_at timestamptz NOT NULL DEFAULT now();
ALTER TABLE jurisdiction_pack ADD CONSTRAINT jurisdiction_pack_approval_ck CHECK (status <> 'Approved' OR (approved_by IS NOT NULL AND approved_at IS NOT NULL AND effective_from IS NOT NULL));
ALTER TABLE jurisdiction_pack ADD CONSTRAINT jurisdiction_pack_window_ck CHECK (effective_to IS NULL OR effective_to >= effective_from);
ALTER TABLE jurisdiction_rule ADD CONSTRAINT jurisdiction_rule_interp_ck CHECK (interpretation_status IN ('Draft','Counsel reviewed','Approved','Superseded'));
ALTER TABLE ai_budget ADD CONSTRAINT ai_budget_period_ck CHECK (period ~ '^\d{4}-(0[1-9]|1[0-2])$');
ALTER TABLE ai_budget ADD CONSTRAINT ai_budget_hard_ck CHECK (hard_cap_tokens > 0);
ALTER TABLE security_finding ADD CONSTRAINT security_finding_close_ck CHECK (closed_at IS NULL OR closed_at >= found_at);
ALTER TABLE locale_bundle ADD CONSTRAINT locale_bundle_cov_ck CHECK (coverage_percent BETWEEN 0 AND 100);
ALTER TABLE locale_bundle ADD CONSTRAINT locale_bundle_tag_ck CHECK (locale ~ '^[a-z]{2,3}(-[A-Z][a-z]{3})?(-[A-Z]{2})?$');

-- C3-05 Data residency (ENT-DAT-03, CJ-R09). Each regional database pins its region; tenant region is immutable.
CREATE OR REPLACE FUNCTION fn_tenant_region_guard() RETURNS trigger LANGUAGE plpgsql AS $$
DECLARE r text := current_setting('app.deployment_region', true);
BEGIN
  IF r IS NULL OR r = '' THEN RAISE EXCEPTION 'deployment region not configured' USING ERRCODE = '42501'; END IF;
  IF TG_OP = 'UPDATE' AND NEW.data_region IS DISTINCT FROM OLD.data_region THEN
    RAISE EXCEPTION 'data_region is fixed at onboarding (CJ-R09)' USING ERRCODE = '23514'; END IF;
  IF NEW.data_region <> r THEN
    RAISE EXCEPTION 'cross-region write rejected: tenant region % in % database', NEW.data_region, r USING ERRCODE = '23514'; END IF;
  RETURN NEW;
END $$;
DROP TRIGGER IF EXISTS trg_tenant_region_guard ON tenant;
CREATE TRIGGER trg_tenant_region_guard BEFORE INSERT OR UPDATE ON tenant FOR EACH ROW EXECUTE FUNCTION fn_tenant_region_guard();

-- C3-06 Separation of duties: also on UPDATE, and across all roles held by one user (ENT-ACC-02).
CREATE TABLE IF NOT EXISTS user_role_assignment (
  tenant_id uuid NOT NULL REFERENCES tenant(tenant_id), user_id uuid NOT NULL, role_id uuid NOT NULL,
  granted_by uuid NOT NULL, granted_at timestamptz NOT NULL DEFAULT now(), expires_at timestamptz, revoked_at timestamptz,
  PRIMARY KEY (tenant_id, user_id, role_id), FOREIGN KEY (tenant_id, role_id) REFERENCES custom_role(tenant_id, role_id),
  CHECK (granted_by <> user_id));
CREATE OR REPLACE FUNCTION enforce_sod() RETURNS trigger LANGUAGE plpgsql AS $$
BEGIN
  IF EXISTS (SELECT 1 FROM role_permission rp JOIN sod_conflict c
             ON (c.permission_a = NEW.permission AND c.permission_b = rp.permission) OR (c.permission_b = NEW.permission AND c.permission_a = rp.permission)
             WHERE rp.role_id = NEW.role_id AND rp.tenant_id = NEW.tenant_id AND rp.permission <> COALESCE(CASE WHEN TG_OP='UPDATE' THEN OLD.permission END,'')) THEN
    RAISE EXCEPTION 'separation of duties violation: % conflicts within role', NEW.permission USING ERRCODE = '23514';
  END IF;
  IF EXISTS (SELECT 1 FROM user_role_assignment ura JOIN user_role_assignment other
               ON other.tenant_id = ura.tenant_id AND other.user_id = ura.user_id AND other.role_id <> ura.role_id AND other.revoked_at IS NULL
             JOIN role_permission rp ON rp.tenant_id = other.tenant_id AND rp.role_id = other.role_id
             JOIN sod_conflict c ON (c.permission_a = NEW.permission AND c.permission_b = rp.permission) OR (c.permission_b = NEW.permission AND c.permission_a = rp.permission)
             WHERE ura.tenant_id = NEW.tenant_id AND ura.role_id = NEW.role_id AND ura.revoked_at IS NULL) THEN
    RAISE EXCEPTION 'separation of duties violation: % conflicts with another role held by the same user', NEW.permission USING ERRCODE = '23514';
  END IF;
  RETURN NEW;
END $$;
DROP TRIGGER IF EXISTS role_permission_sod ON role_permission;
CREATE TRIGGER role_permission_sod BEFORE INSERT OR UPDATE ON role_permission FOR EACH ROW EXECUTE FUNCTION enforce_sod();
CREATE OR REPLACE FUNCTION enforce_sod_assignment() RETURNS trigger LANGUAGE plpgsql AS $$
BEGIN
  IF NEW.revoked_at IS NULL AND EXISTS (
     SELECT 1 FROM role_permission a JOIN user_role_assignment o ON o.tenant_id = NEW.tenant_id AND o.user_id = NEW.user_id AND o.role_id <> NEW.role_id AND o.revoked_at IS NULL
       JOIN role_permission b ON b.tenant_id = o.tenant_id AND b.role_id = o.role_id
       JOIN sod_conflict c ON (c.permission_a = a.permission AND c.permission_b = b.permission) OR (c.permission_b = a.permission AND c.permission_a = b.permission)
     WHERE a.tenant_id = NEW.tenant_id AND a.role_id = NEW.role_id) THEN
    RAISE EXCEPTION 'separation of duties violation: role assignment combines conflicting permissions' USING ERRCODE = '23514';
  END IF;
  RETURN NEW;
END $$;
DROP TRIGGER IF EXISTS trg_user_role_assignment_sod ON user_role_assignment;
CREATE TRIGGER trg_user_role_assignment_sod BEFORE INSERT OR UPDATE ON user_role_assignment FOR EACH ROW EXECUTE FUNCTION enforce_sod_assignment();

-- C3-07 Append-only and tamper evidence (SEC-06, NFR-018)
CREATE OR REPLACE FUNCTION fn_forbid_mutation() RETURNS trigger LANGUAGE plpgsql AS $$
BEGIN
  IF current_user = 'ge_retention' AND current_setting('app.retention_run_id', true) IS NOT NULL
     AND current_setting('app.retention_run_id', true) <> '' AND TG_OP = 'DELETE' THEN RETURN OLD; END IF;
  RAISE EXCEPTION 'IMMUTABLE_RECORD: % on % is not allowed', TG_OP, TG_TABLE_NAME USING ERRCODE = 'P0001';
END $$;
ALTER TABLE audit_event ADD COLUMN IF NOT EXISTS company_id uuid;
ALTER TABLE audit_event ADD COLUMN IF NOT EXISTS correlation_id uuid;
ALTER TABLE audit_event ADD COLUMN IF NOT EXISTS object_type text;
ALTER TABLE audit_event ADD COLUMN IF NOT EXISTS payload_redacted jsonb NOT NULL DEFAULT '{}'::jsonb;
ALTER TABLE audit_event ADD COLUMN IF NOT EXISTS schema_version int NOT NULL DEFAULT 1;
ALTER TABLE audit_event ADD COLUMN IF NOT EXISTS prev_hash bytea;
ALTER TABLE audit_event ADD COLUMN IF NOT EXISTS row_hash bytea;
CREATE OR REPLACE FUNCTION fn_append_audit(p_company uuid, p_actor uuid, p_action text, p_ref text, p_object_type text,
  p_policy_version text, p_correlation uuid, p_payload jsonb) RETURNS bigint LANGUAGE plpgsql SECURITY DEFINER SET search_path = public, pg_temp AS $$
DECLARE t uuid := app_tenant(); prev bytea; h bytea; new_id bigint; ts timestamptz := clock_timestamp();
BEGIN
  PERFORM pg_advisory_xact_lock(hashtextextended(t::text, 42));
  SELECT row_hash INTO prev FROM audit_event WHERE tenant_id = t ORDER BY audit_id DESC LIMIT 1;
  h := digest(coalesce(prev, '\x'::bytea) || convert_to(jsonb_build_object('t',t,'c',p_company,'a',p_actor,'act',p_action,'ref',p_ref,
        'ot',p_object_type,'pv',p_policy_version,'corr',p_correlation,'p',p_payload,'ts',ts)::text, 'UTF8'), 'sha256');
  INSERT INTO audit_event(tenant_id, company_id, actor, action, ref, object_type, policy_version, correlation_id, payload_redacted, occurred_at, prev_hash, row_hash)
  VALUES (t, p_company, p_actor, p_action, p_ref, p_object_type, p_policy_version, p_correlation, p_payload, ts, prev, h) RETURNING audit_id INTO new_id;
  RETURN new_id;
END $$;
REVOKE ALL ON FUNCTION fn_append_audit(uuid,uuid,text,text,text,text,uuid,jsonb) FROM PUBLIC;
GRANT EXECUTE ON FUNCTION fn_append_audit(uuid,uuid,text,text,text,text,uuid,jsonb) TO ge_app, ge_worker;
CREATE OR REPLACE FUNCTION fn_verify_audit_chain(p_tenant uuid) RETURNS TABLE(audit_id bigint, ok boolean) LANGUAGE sql STABLE AS $$
  SELECT a.audit_id, a.row_hash = digest(coalesce(a.prev_hash,'\x'::bytea) || convert_to(jsonb_build_object('t',a.tenant_id,'c',a.company_id,'a',a.actor,'act',a.action,'ref',a.ref,
         'ot',a.object_type,'pv',a.policy_version,'corr',a.correlation_id,'p',a.payload_redacted,'ts',a.occurred_at)::text,'UTF8'),'sha256')
         AND a.prev_hash IS NOT DISTINCT FROM lag(a.row_hash) OVER (ORDER BY a.audit_id)
  FROM audit_event a WHERE a.tenant_id = p_tenant ORDER BY a.audit_id $$;
DO $$ DECLARE t text; BEGIN
  FOREACH t IN ARRAY ARRAY['audit_event','consent_record','ai_usage_event','eval_run','webhook_delivery','incident_notification'] LOOP
    EXECUTE format('DROP TRIGGER IF EXISTS trg_%1$s_immutable ON %1$I', t);
    IF t IN ('webhook_delivery','incident_notification') THEN
      EXECUTE format('CREATE TRIGGER trg_%1$s_immutable BEFORE DELETE ON %1$I FOR EACH ROW EXECUTE FUNCTION fn_forbid_mutation()', t);
    ELSE
      EXECUTE format('CREATE TRIGGER trg_%1$s_immutable BEFORE UPDATE OR DELETE ON %1$I FOR EACH ROW EXECUTE FUNCTION fn_forbid_mutation()', t);
    END IF;
  END LOOP; END $$;
-- Effects move forward only (Intended -> Dispatched -> Reconciling -> Confirmed | Failed -> Compensated)
CREATE OR REPLACE FUNCTION fn_effect_transition() RETURNS trigger LANGUAGE plpgsql AS $$
BEGIN
  IF NEW.idempotency_key <> OLD.idempotency_key OR NEW.preflight_verdict <> OLD.preflight_verdict OR NEW.run_id <> OLD.run_id THEN
    RAISE EXCEPTION 'IMMUTABLE_RECORD: effect identity columns are frozen' USING ERRCODE = 'P0001'; END IF;
  IF NOT ((OLD.status, NEW.status) IN (('Intended','Dispatched'),('Intended','Failed'),('Dispatched','Reconciling'),('Dispatched','Confirmed'),
      ('Dispatched','Failed'),('Reconciling','Confirmed'),('Reconciling','Failed'),('Failed','Compensated'),('Confirmed','Compensated'))
      OR OLD.status = NEW.status) THEN
    RAISE EXCEPTION 'invalid effect transition % -> %', OLD.status, NEW.status USING ERRCODE = '23514'; END IF;
  RETURN NEW;
END $$;
DROP TRIGGER IF EXISTS trg_effect_transition ON effect;
CREATE TRIGGER trg_effect_transition BEFORE UPDATE ON effect FOR EACH ROW EXECUTE FUNCTION fn_effect_transition();
CREATE TRIGGER trg_effect_nodelete BEFORE DELETE ON effect FOR EACH ROW EXECUTE FUNCTION fn_forbid_mutation();

-- C3-08 Breach clocks (V8 regulatory obligations; CERT-In 6 hours)
CREATE OR REPLACE FUNCTION fn_incident_deadline() RETURNS trigger LANGUAGE plpgsql AS $$
DECLARE aware timestamptz;
BEGIN
  SELECT aware_at INTO aware FROM incident WHERE incident_id = NEW.incident_id;
  IF NEW.authority = 'CERT-In' AND NEW.deadline_at > aware + interval '6 hours' THEN
    RAISE EXCEPTION 'CERT-In deadline must be within 6 hours of awareness' USING ERRCODE = '23514'; END IF;
  IF NEW.authority IN ('EU-SA','UK-ICO') AND NEW.deadline_at > aware + interval '72 hours' THEN
    RAISE EXCEPTION 'GDPR supervisory deadline must be within 72 hours of awareness' USING ERRCODE = '23514'; END IF;
  IF NEW.authority = 'DPB-India' AND NEW.deadline_at > aware + interval '72 hours' THEN
    RAISE EXCEPTION 'DPDP Board detailed report deadline must be within 72 hours (verify DPDP Rules 2025)' USING ERRCODE = '23514'; END IF;
  RETURN NEW;
END $$;
DROP TRIGGER IF EXISTS trg_incident_deadline ON incident_notification;
CREATE TRIGGER trg_incident_deadline BEFORE INSERT OR UPDATE ON incident_notification FOR EACH ROW EXECUTE FUNCTION fn_incident_deadline();

-- C3-09 Crypto-shredding support (ENT-DAT-02). Per-tenant data keys wrapped by the platform or customer KMS key.
CREATE TABLE IF NOT EXISTS tenant_data_key (
  tenant_id uuid NOT NULL REFERENCES tenant(tenant_id), dek_id uuid NOT NULL DEFAULT gen_random_uuid(),
  wrapped_dek bytea, kek_ref text NOT NULL, kek_provider text NOT NULL CHECK (kek_provider IN ('platform-aws-kms','aws-kms','azure-key-vault','gcp-kms')),
  created_at timestamptz NOT NULL DEFAULT now(), rotated_from uuid, destroyed_at timestamptz, destroy_reason text,
  PRIMARY KEY (tenant_id, dek_id),
  CHECK ((destroyed_at IS NULL AND wrapped_dek IS NOT NULL) OR (destroyed_at IS NOT NULL AND wrapped_dek IS NULL AND destroy_reason IS NOT NULL)));
CREATE OR REPLACE FUNCTION fn_tenant_key_revoked() RETURNS trigger LANGUAGE plpgsql AS $$
BEGIN
  IF NEW.key_state = 'revoked' AND OLD.key_state <> 'revoked' THEN
    NEW.revoked_at := coalesce(NEW.revoked_at, now());
    UPDATE tenant_data_key SET wrapped_dek = NULL, destroyed_at = now(), destroy_reason = 'customer key revoked (crypto-shred)'
     WHERE tenant_id = NEW.tenant_id AND destroyed_at IS NULL;
  END IF;
  RETURN NEW;
END $$;
DROP TRIGGER IF EXISTS trg_tenant_key_revoked ON tenant_key_config;
CREATE TRIGGER trg_tenant_key_revoked BEFORE UPDATE ON tenant_key_config FOR EACH ROW EXECUTE FUNCTION fn_tenant_key_revoked();

-- C3-10 Domain schema registry: the 89 generic domain tables validate schema_ref, status and required payload keys (Appendix B).
CREATE TABLE IF NOT EXISTS domain_schema_registry (
  schema_ref text NOT NULL, version int NOT NULL CHECK (version >= 1), table_name text NOT NULL, allowed_statuses text[] NOT NULL CHECK (cardinality(allowed_statuses) > 0),
  required_keys text[] NOT NULL DEFAULT '{}', json_schema jsonb NOT NULL, data_class text NOT NULL CHECK (data_class IN ('Public','Internal','Confidential','Restricted')),
  retention_class text NOT NULL, max_payload_bytes int NOT NULL DEFAULT 262144 CHECK (max_payload_bytes BETWEEN 1024 AND 1048576),
  status text NOT NULL CHECK (status IN ('Draft','Approved','Retired')), approved_by uuid, approved_at timestamptz,
  PRIMARY KEY (schema_ref, version), CHECK (status <> 'Approved' OR (approved_by IS NOT NULL AND approved_at IS NOT NULL)));
CREATE OR REPLACE FUNCTION fn_validate_domain_row() RETURNS trigger LANGUAGE plpgsql AS $$
DECLARE r domain_schema_registry%ROWTYPE;
BEGIN
  SELECT * INTO r FROM domain_schema_registry d WHERE d.schema_ref = NEW.schema_ref AND d.table_name = TG_TABLE_NAME AND d.status = 'Approved'
   ORDER BY d.version DESC LIMIT 1;
  IF NOT FOUND THEN RAISE EXCEPTION 'unknown or unapproved schema_ref % for %', NEW.schema_ref, TG_TABLE_NAME USING ERRCODE = '23514'; END IF;
  IF NOT (NEW.status = ANY (r.allowed_statuses)) THEN RAISE EXCEPTION 'status % not allowed for %', NEW.status, NEW.schema_ref USING ERRCODE = '23514'; END IF;
  IF NOT (NEW.payload ?& r.required_keys) THEN RAISE EXCEPTION 'payload missing required keys for %', NEW.schema_ref USING ERRCODE = '23514'; END IF;
  IF pg_column_size(NEW.payload) > r.max_payload_bytes THEN RAISE EXCEPTION 'payload exceeds % bytes', r.max_payload_bytes USING ERRCODE = '54000'; END IF;
  IF TG_OP = 'UPDATE' THEN
    IF NEW.created_by <> OLD.created_by OR NEW.created_at <> OLD.created_at OR NEW.id <> OLD.id THEN
      RAISE EXCEPTION 'IMMUTABLE_RECORD: identity columns frozen' USING ERRCODE = 'P0001'; END IF;
    IF NEW.version <> OLD.version + 1 THEN RAISE EXCEPTION 'STALE_REVISION: expected version %', OLD.version + 1 USING ERRCODE = '40001'; END IF;
    NEW.updated_at := now();
  END IF;
  RETURN NEW;
END $$;
-- C3-11 V6 logical entities absent from Appendix C (MT-09/10/11/18/27/33; ch26 V6 entity table)
CREATE TABLE IF NOT EXISTS company_operating_country (
  tenant_id uuid NOT NULL, company_id uuid NOT NULL, country_code char(2) NOT NULL CHECK (country_code ~ '^[A-Z]{2}$'),
  status text NOT NULL DEFAULT 'active' CHECK (status IN ('active','paused','exited')), created_at timestamptz NOT NULL DEFAULT now(),
  PRIMARY KEY (tenant_id, company_id, country_code), FOREIGN KEY (tenant_id, company_id) REFERENCES company(tenant_id, company_id));
ALTER TABLE division ADD COLUMN IF NOT EXISTS name_norm text GENERATED ALWAYS AS (lower(btrim(name))) STORED;
ALTER TABLE division ADD CONSTRAINT division_company_uq UNIQUE (tenant_id, company_id, division_id);
ALTER TABLE division ADD CONSTRAINT division_name_uq UNIQUE (tenant_id, company_id, name_norm);
ALTER TABLE brand ADD COLUMN IF NOT EXISTS status text NOT NULL DEFAULT 'active' CHECK (status IN ('active','retired'));
ALTER TABLE brand ADD COLUMN IF NOT EXISTS valid_from timestamptz NOT NULL DEFAULT now();
ALTER TABLE brand ADD COLUMN IF NOT EXISTS valid_to timestamptz;
ALTER TABLE brand ADD CONSTRAINT brand_company_uq UNIQUE (tenant_id, company_id, brand_id);
ALTER TABLE brand ADD CONSTRAINT brand_division_company_fk FOREIGN KEY (tenant_id, company_id, division_id) REFERENCES division(tenant_id, company_id, division_id);
ALTER TABLE offering ADD CONSTRAINT offering_company_uq UNIQUE (tenant_id, company_id, offering_id);
ALTER TABLE offering ADD CONSTRAINT offering_brand_company_fk FOREIGN KEY (tenant_id, company_id, brand_id) REFERENCES brand(tenant_id, company_id, brand_id);
ALTER TABLE market ADD CONSTRAINT market_company_uq UNIQUE (tenant_id, company_id, market_id);
ALTER TABLE channel_account ADD CONSTRAINT channel_account_company_uq UNIQUE (tenant_id, company_id, account_id);
CREATE TABLE IF NOT EXISTS offering_market (
  tenant_id uuid NOT NULL, company_id uuid NOT NULL, offering_id uuid NOT NULL, market_id uuid NOT NULL,
  eligibility_status text NOT NULL DEFAULT 'pending' CHECK (eligibility_status IN ('pending','eligible','held','ineligible')), policy_ref uuid,
  created_at timestamptz NOT NULL DEFAULT now(), PRIMARY KEY (tenant_id, company_id, offering_id, market_id),
  FOREIGN KEY (tenant_id, company_id, offering_id) REFERENCES offering(tenant_id, company_id, offering_id),
  FOREIGN KEY (tenant_id, company_id, market_id) REFERENCES market(tenant_id, company_id, market_id));
CREATE TABLE IF NOT EXISTS channel_account_market (
  tenant_id uuid NOT NULL, company_id uuid NOT NULL, account_id uuid NOT NULL, market_id uuid NOT NULL, created_at timestamptz NOT NULL DEFAULT now(),
  PRIMARY KEY (tenant_id, company_id, account_id, market_id),
  FOREIGN KEY (tenant_id, company_id, account_id) REFERENCES channel_account(tenant_id, company_id, account_id),
  FOREIGN KEY (tenant_id, company_id, market_id) REFERENCES market(tenant_id, company_id, market_id));
CREATE TABLE IF NOT EXISTS configuration_revision (
  tenant_id uuid NOT NULL, company_id uuid NOT NULL, config_revision_id uuid NOT NULL DEFAULT gen_random_uuid(), scope text NOT NULL,
  base_version int NOT NULL CHECK (base_version >= 0), revision int NOT NULL CHECK (revision >= 1), requester_id uuid NOT NULL, reviewer_id uuid,
  snapshot_ref text NOT NULL, snapshot_hash bytea NOT NULL CHECK (octet_length(snapshot_hash) = 32),
  status text NOT NULL CHECK (status IN ('Draft','Pending review','Approved','Rejected','Superseded')), created_at timestamptz NOT NULL DEFAULT now(),
  PRIMARY KEY (tenant_id, config_revision_id), UNIQUE (tenant_id, company_id, scope, revision),
  FOREIGN KEY (tenant_id, company_id) REFERENCES company(tenant_id, company_id),
  CHECK (reviewer_id IS NULL OR reviewer_id <> requester_id), CHECK (status NOT IN ('Approved') OR reviewer_id IS NOT NULL),
  CHECK (revision = base_version + 1));
CREATE TABLE IF NOT EXISTS workflow_configuration (
  tenant_id uuid NOT NULL, company_id uuid NOT NULL, config_id uuid NOT NULL DEFAULT gen_random_uuid(),
  offering_id uuid NOT NULL, market_id uuid NOT NULL, account_id uuid, sku_id text NOT NULL CHECK (sku_id ~ '^SM-SVC-\d{2}$'),
  wf_id text NOT NULL, wf_version int NOT NULL CHECK (wf_version >= 1), budget_minor bigint NOT NULL CHECK (budget_minor >= 0),
  currency char(3) NOT NULL CHECK (currency ~ '^[A-Z]{3}$'), authority text NOT NULL CHECK (authority IN ('L0','L1','L2','L3')),
  schedule text, status text NOT NULL CHECK (status IN ('Draft','Active','Paused','Retired')), config_revision_id uuid NOT NULL,
  version int NOT NULL DEFAULT 1 CHECK (version >= 1), created_at timestamptz NOT NULL DEFAULT now(),
  PRIMARY KEY (tenant_id, config_id),
  FOREIGN KEY (tenant_id, company_id, offering_id) REFERENCES offering(tenant_id, company_id, offering_id),
  FOREIGN KEY (tenant_id, company_id, market_id) REFERENCES market(tenant_id, company_id, market_id),
  FOREIGN KEY (tenant_id, company_id, account_id) REFERENCES channel_account(tenant_id, company_id, account_id),
  FOREIGN KEY (tenant_id, config_revision_id) REFERENCES configuration_revision(tenant_id, config_revision_id),
  CHECK (left(wf_id, 9) = sku_id));
CREATE UNIQUE INDEX IF NOT EXISTS ux_workflow_configuration_active ON workflow_configuration (tenant_id, company_id, offering_id, market_id, wf_id) WHERE status = 'Active';
-- BusinessEvent: the attribution fact (MT-27, MT-31; ch29 V6 event attribution). Unknown attribution stays NULL.
CREATE TABLE IF NOT EXISTS business_event (
  tenant_id uuid NOT NULL, company_id uuid NOT NULL, event_id uuid NOT NULL DEFAULT gen_random_uuid(), idempotency_key text NOT NULL,
  event_type text NOT NULL CHECK (event_type IN ('lead_created','opportunity_qualified','meeting_held','proposal_sent','deal_won','deal_lost','order_confirmed',
     'invoice_issued','payment_verified','renewal_won','churned','refund_verified')),
  offering_id uuid, market_id uuid, account_id uuid, campaign_id uuid, sku_id text CHECK (sku_id IS NULL OR sku_id ~ '^SM-SVC-\d{2}$'), wf_id text,
  run_id uuid, wf_version int, config_revision_id uuid, correlation_id uuid,
  amount_minor bigint CHECK (amount_minor IS NULL OR amount_minor >= 0), currency char(3) CHECK (currency IS NULL OR currency ~ '^[A-Z]{3}$'),
  evidence_ref text, verified boolean NOT NULL DEFAULT false, is_simulated boolean NOT NULL DEFAULT false, source_kind text NOT NULL DEFAULT 'live'
     CHECK (source_kind IN ('live','import','demo_fixture')),
  occurred_at timestamptz NOT NULL, recorded_at timestamptz NOT NULL DEFAULT now(), metric_version int NOT NULL DEFAULT 1,
  PRIMARY KEY (tenant_id, event_id), UNIQUE (tenant_id, company_id, idempotency_key),
  FOREIGN KEY (tenant_id, company_id) REFERENCES company(tenant_id, company_id),
  FOREIGN KEY (tenant_id, company_id, offering_id) REFERENCES offering(tenant_id, company_id, offering_id),
  FOREIGN KEY (tenant_id, company_id, market_id) REFERENCES market(tenant_id, company_id, market_id),
  FOREIGN KEY (tenant_id, company_id, account_id) REFERENCES channel_account(tenant_id, company_id, account_id),
  FOREIGN KEY (tenant_id, company_id, run_id) REFERENCES workflow_run(tenant_id, company_id, run_id),
  CHECK ((amount_minor IS NULL) = (currency IS NULL)),
  CHECK (wf_id IS NULL OR (sku_id IS NOT NULL AND left(wf_id, 9) = sku_id)),
  CHECK (NOT verified OR evidence_ref IS NOT NULL),
  CHECK (source_kind <> 'demo_fixture' OR is_simulated));
CREATE OR REPLACE FUNCTION fn_business_event_attribution() RETURNS trigger LANGUAGE plpgsql AS $$
BEGIN  -- run-attributed events inherit only evidenced dimensions from the run; never invent offering/market
  IF NEW.run_id IS NOT NULL THEN
    SELECT r.sku_id, r.wf_id, r.wf_version INTO NEW.sku_id, NEW.wf_id, NEW.wf_version FROM workflow_run r
     WHERE r.tenant_id = NEW.tenant_id AND r.company_id = NEW.company_id AND r.run_id = NEW.run_id;
  END IF;
  RETURN NEW;
END $$;
CREATE TRIGGER trg_business_event_attr BEFORE INSERT ON business_event FOR EACH ROW EXECUTE FUNCTION fn_business_event_attribution();
CREATE TRIGGER trg_business_event_immutable BEFORE UPDATE OR DELETE ON business_event FOR EACH ROW EXECUTE FUNCTION fn_forbid_mutation();

-- C3-12 Analytics: metric contract (ch29 V5 "Metric contract"), versioned aggregates, experiments, feedback, SLI, customer value
CREATE TABLE IF NOT EXISTS metric_definition (
  metric_id text NOT NULL CHECK (metric_id ~ '^[A-Z][A-Z0-9]*(-[A-Z0-9]+)*-\d{2,3}$'), metric_version int NOT NULL CHECK (metric_version >= 1),
  name text NOT NULL, formula text NOT NULL, numerator_sql_ref text NOT NULL, denominator_sql_ref text, unit text NOT NULL CHECK (unit IN ('count','ratio','fraction','ms','seconds','score','minor_currency','percent')),
  source_event_types text[] NOT NULL, currency_rule text NOT NULL CHECK (currency_rule IN ('native_only','no_currency','approved_fx_display')),
  timezone text NOT NULL DEFAULT 'Asia/Kolkata', period_grain text NOT NULL CHECK (period_grain IN ('hour','day','week','month','quarter','rolling_30d')),
  filters jsonb NOT NULL DEFAULT '{}', attribution_rule text CHECK (attribution_rule IN ('none','first_touch','last_non_direct','linear','position_40_20_40')),
  observation_window_days int CHECK (observation_window_days BETWEEN 1 AND 365), owner text NOT NULL, baseline numeric, threshold numeric,
  threshold_direction text CHECK (threshold_direction IN ('<=','>=','=')), audience text NOT NULL CHECK (audience IN ('tenant','operator')),
  status text NOT NULL CHECK (status IN ('Draft','Approved','Retired')), approved_by uuid, approved_at timestamptz,
  PRIMARY KEY (metric_id, metric_version), CHECK (status <> 'Approved' OR approved_by IS NOT NULL));
CREATE TABLE IF NOT EXISTS metric_aggregate (
  tenant_id uuid NOT NULL, company_id uuid NOT NULL, metric_id text NOT NULL, metric_version int NOT NULL, period_start timestamptz NOT NULL,
  dimension_hash bytea NOT NULL, dimensions jsonb NOT NULL DEFAULT '{}', aggregate_version int NOT NULL DEFAULT 1 CHECK (aggregate_version >= 1),
  numerator numeric NOT NULL, denominator numeric CHECK (denominator IS NULL OR denominator >= 0), unknown_count bigint NOT NULL DEFAULT 0 CHECK (unknown_count >= 0),
  value numeric GENERATED ALWAYS AS (CASE WHEN denominator IS NULL THEN numerator WHEN denominator = 0 THEN NULL ELSE numerator / denominator END) STORED,
  currency char(3) CHECK (currency IS NULL OR currency ~ '^[A-Z]{3}$'), source_event_count bigint NOT NULL CHECK (source_event_count >= 0),
  computed_at timestamptz NOT NULL DEFAULT now(), superseded_at timestamptz, late_event_reason text,
  PRIMARY KEY (tenant_id, company_id, metric_id, metric_version, period_start, dimension_hash, aggregate_version),
  FOREIGN KEY (metric_id, metric_version) REFERENCES metric_definition(metric_id, metric_version),
  FOREIGN KEY (tenant_id, company_id) REFERENCES company(tenant_id, company_id),
  CHECK (aggregate_version = 1 OR late_event_reason IS NOT NULL));
CREATE UNIQUE INDEX IF NOT EXISTS ux_metric_aggregate_current ON metric_aggregate (tenant_id, company_id, metric_id, metric_version, period_start, dimension_hash) WHERE superseded_at IS NULL;
CREATE TABLE IF NOT EXISTS experiment (
  tenant_id uuid NOT NULL, company_id uuid NOT NULL, experiment_id uuid NOT NULL DEFAULT gen_random_uuid(), name text NOT NULL,
  hypothesis text NOT NULL, primary_metric_id text NOT NULL, primary_metric_version int NOT NULL, guardrail_metric_ids text[] NOT NULL DEFAULT '{}',
  allocation jsonb NOT NULL, consent_class text NOT NULL CHECK (consent_class IN ('necessary','analytics','marketing')),
  min_sample_per_arm int NOT NULL CHECK (min_sample_per_arm >= 100), stopping_rule text NOT NULL, max_duration_days int NOT NULL CHECK (max_duration_days BETWEEN 7 AND 90),
  status text NOT NULL CHECK (status IN ('Draft','Approved','Running','Stopped','Concluded')), winner_arm text, decided_by uuid, decided_at timestamptz,
  created_by uuid NOT NULL, PRIMARY KEY (tenant_id, experiment_id), FOREIGN KEY (tenant_id, company_id) REFERENCES company(tenant_id, company_id),
  FOREIGN KEY (primary_metric_id, primary_metric_version) REFERENCES metric_definition(metric_id, metric_version),
  CHECK (winner_arm IS NULL OR (decided_by IS NOT NULL AND decided_by <> created_by AND status = 'Concluded')));   -- CV-14: no automatic winner
CREATE TABLE IF NOT EXISTS feedback_case (   -- ch26 V5 opt_feedback_case; ch29 CS-12 (CSAT, CES, NPS)
  tenant_id uuid NOT NULL, company_id uuid NOT NULL, case_id uuid NOT NULL DEFAULT gen_random_uuid(), revision int NOT NULL DEFAULT 1,
  milestone text NOT NULL CHECK (milestone IN ('onboarding_complete','first_value','support_resolved','renewal','quarterly')),
  output_ref text, topic text, csat smallint CHECK (csat BETWEEN 1 AND 5), ces smallint CHECK (ces BETWEEN 1 AND 7), nps smallint CHECK (nps BETWEEN 0 AND 10),
  responded boolean NOT NULL, consent_class text NOT NULL CHECK (consent_class IN ('necessary','analytics','marketing')), owner_id uuid,
  state text NOT NULL CHECK (state IN ('Invited','Responded','Expired','In follow-up','Resolved')), resolution_ref text, invited_at timestamptz NOT NULL, responded_at timestamptz,
  PRIMARY KEY (tenant_id, case_id, revision), FOREIGN KEY (tenant_id, company_id) REFERENCES company(tenant_id, company_id),
  CHECK (responded = (responded_at IS NOT NULL)), CHECK (responded OR (csat IS NULL AND ces IS NULL AND nps IS NULL)),
  CHECK (state <> 'Resolved' OR resolution_ref IS NOT NULL));
CREATE TABLE IF NOT EXISTS sli_sample (   -- ch26 V5 opt_sli_sample; ch29 KPI-05/06/26–31
  component text NOT NULL, tenant_scope uuid NOT NULL DEFAULT '00000000-0000-0000-0000-000000000000', metric_id text NOT NULL, metric_version int NOT NULL, window_start timestamptz NOT NULL, window_end timestamptz NOT NULL,
  numerator bigint NOT NULL CHECK (numerator >= 0), denominator bigint NOT NULL CHECK (denominator >= 0), status text NOT NULL CHECK (status IN ('ok','missing_data','excluded_approved')),
  exclusion_ref text, PRIMARY KEY (component, metric_id, metric_version, window_start, tenant_scope),
  CHECK (window_end > window_start), CHECK (numerator <= denominator OR metric_id ~ '^KPI-(05|26|27|28|29|30|31)$'), CHECK (status <> 'excluded_approved' OR exclusion_ref IS NOT NULL));
CREATE TABLE IF NOT EXISTS customer_value (   -- ch26 V5 opt_customer_value: no guaranteed value
  tenant_id uuid NOT NULL, sku_id text NOT NULL CHECK (sku_id ~ '^SM-SVC-\d{2}$'), period text NOT NULL CHECK (period ~ '^\d{4}-(0[1-9]|1[0-2])$'),
  accepted_count int NOT NULL CHECK (accepted_count >= 0), allowance int NOT NULL CHECK (allowance >= 0), outcome_evidence_refs text[] NOT NULL DEFAULT '{}',
  assumption_version int NOT NULL, label text NOT NULL DEFAULT 'Estimate - not a guarantee' CHECK (label LIKE 'Estimate%'),
  PRIMARY KEY (tenant_id, sku_id, period));
CREATE TABLE IF NOT EXISTS journey_event (   -- ch26 V5 opt_journey_event; ch29 AT-14 consent-aware acquisition analytics
  event_id uuid NOT NULL, audience text NOT NULL CHECK (audience IN ('operator','subscriber')), tenant_id uuid, cohort text, acquisition_source text NOT NULL DEFAULT 'unknown',
  consent_class text NOT NULL CHECK (consent_class IN ('necessary','analytics','marketing')), pseudonymous_ref bytea, stage text NOT NULL, sku_id text,
  occurred_at timestamptz NOT NULL, correlation_id uuid, PRIMARY KEY (event_id),
  CHECK (consent_class <> 'necessary' OR pseudonymous_ref IS NULL), CHECK (pseudonymous_ref IS NULL OR octet_length(pseudonymous_ref) = 32),
  CHECK (audience <> 'subscriber' OR tenant_id IS NOT NULL));
CREATE TABLE IF NOT EXISTS domain_record_version (   -- ch26 "Proposed V4 persistence additions"
  tenant_id uuid NOT NULL, company_id uuid NOT NULL, table_name text NOT NULL, record_id uuid NOT NULL, revision int NOT NULL CHECK (revision >= 1),
  payload jsonb NOT NULL, reason text NOT NULL, actor_id uuid NOT NULL, review_state text NOT NULL CHECK (review_state IN ('none','pending','approved','rejected')),
  created_at timestamptz NOT NULL DEFAULT now(), PRIMARY KEY (tenant_id, table_name, record_id, revision),
  FOREIGN KEY (tenant_id, company_id) REFERENCES company(tenant_id, company_id));
CREATE TRIGGER trg_domain_record_version_immutable BEFORE UPDATE OR DELETE ON domain_record_version FOR EACH ROW EXECUTE FUNCTION fn_forbid_mutation();
CREATE TABLE IF NOT EXISTS usage_reservation (   -- ch26 V4 usage_reservation; DB-V2-USAGE
  tenant_id uuid NOT NULL, company_id uuid NOT NULL, reservation_id uuid NOT NULL DEFAULT gen_random_uuid(), sku_id text NOT NULL, period text NOT NULL,
  run_id uuid NOT NULL, units int NOT NULL CHECK (units > 0), amount_minor bigint NOT NULL CHECK (amount_minor >= 0), currency char(3) NOT NULL CHECK (currency ~ '^[A-Z]{3}$'),
  state text NOT NULL CHECK (state IN ('Reserved','Committed','Released','Reconciled')), idempotency_key text NOT NULL, created_at timestamptz NOT NULL DEFAULT now(),
  PRIMARY KEY (tenant_id, reservation_id), UNIQUE (tenant_id, run_id, period), UNIQUE (tenant_id, idempotency_key),
  FOREIGN KEY (tenant_id, company_id, run_id) REFERENCES workflow_run(tenant_id, company_id, run_id));
-- C3-13 (generated by gen_c3.py) Grants, RLS policies, indexes and domain-registry triggers
ALTER TABLE inbox ALTER COLUMN tenant_id SET NOT NULL;
GRANT SELECT, INSERT, UPDATE ON tenant TO ge_app, ge_worker;
GRANT SELECT ON tenant TO ge_readonly;
GRANT SELECT, INSERT, UPDATE ON organization TO ge_app, ge_worker;
GRANT SELECT ON organization TO ge_readonly;
GRANT SELECT, INSERT, UPDATE ON company TO ge_app, ge_worker;
GRANT SELECT ON company TO ge_readonly;
GRANT SELECT, INSERT, UPDATE ON division TO ge_app, ge_worker;
GRANT SELECT ON division TO ge_readonly;
GRANT SELECT, INSERT, UPDATE ON brand TO ge_app, ge_worker;
GRANT SELECT ON brand TO ge_readonly;
GRANT SELECT, INSERT, UPDATE ON offering TO ge_app, ge_worker;
GRANT SELECT ON offering TO ge_readonly;
GRANT SELECT, INSERT, UPDATE ON market TO ge_app, ge_worker;
GRANT SELECT ON market TO ge_readonly;
GRANT SELECT, INSERT, UPDATE ON channel_account TO ge_app, ge_worker;
GRANT SELECT ON channel_account TO ge_readonly;
GRANT SELECT, INSERT, UPDATE ON workflow_run TO ge_app, ge_worker;
GRANT SELECT ON workflow_run TO ge_readonly;
GRANT SELECT, INSERT, UPDATE ON workflow_step_run TO ge_app, ge_worker;
GRANT SELECT ON workflow_step_run TO ge_readonly;
GRANT SELECT, INSERT, UPDATE ON effect TO ge_app, ge_worker;
GRANT SELECT ON effect TO ge_readonly;
GRANT SELECT, INSERT, UPDATE ON outbox TO ge_app, ge_worker;
GRANT SELECT ON outbox TO ge_readonly;
GRANT SELECT, INSERT, UPDATE ON inbox TO ge_app, ge_worker;
GRANT SELECT ON inbox TO ge_readonly;
GRANT SELECT ON audit_event TO ge_app, ge_worker, ge_readonly;  -- INSERT only through fn_append_audit()
GRANT SELECT, INSERT, UPDATE ON portfolio_grant TO ge_app, ge_worker;
GRANT SELECT ON portfolio_grant TO ge_readonly;
GRANT SELECT ON fx_rate TO ge_app, ge_worker, ge_readonly;
GRANT SELECT ON jurisdiction_pack TO ge_app, ge_worker, ge_readonly;
GRANT SELECT ON jurisdiction_rule TO ge_app, ge_worker, ge_readonly;
GRANT SELECT, INSERT ON consent_record TO ge_app, ge_worker;
GRANT SELECT ON consent_record TO ge_readonly;
GRANT SELECT, INSERT, UPDATE ON suppression TO ge_app, ge_worker;
GRANT SELECT ON suppression TO ge_readonly;
GRANT SELECT, INSERT, UPDATE ON dsar_request TO ge_app, ge_worker;
GRANT SELECT ON dsar_request TO ge_readonly;
GRANT SELECT, INSERT, UPDATE ON incident TO ge_app, ge_worker;
GRANT SELECT ON incident TO ge_readonly;
GRANT SELECT ON incident_notification TO ge_app, ge_worker, ge_readonly;
GRANT SELECT, INSERT, UPDATE ON incident_notification TO ge_platform_sec;
GRANT SELECT ON ai_model TO ge_app, ge_worker, ge_readonly;
GRANT SELECT ON prompt_version TO ge_app, ge_worker, ge_readonly;
GRANT SELECT ON eval_suite TO ge_app, ge_worker, ge_readonly;
GRANT SELECT ON eval_run TO ge_app, ge_worker, ge_readonly;
GRANT SELECT, INSERT ON ai_usage_event TO ge_app, ge_worker;
GRANT SELECT ON ai_usage_event TO ge_readonly;
GRANT SELECT, INSERT, UPDATE ON ai_budget TO ge_app, ge_worker;
GRANT SELECT ON ai_budget TO ge_readonly;
GRANT SELECT, INSERT, UPDATE ON growth_source TO ge_app, ge_worker;
GRANT SELECT ON growth_source TO ge_readonly;
GRANT SELECT, INSERT, UPDATE ON growth_source_policy TO ge_app, ge_worker;
GRANT SELECT ON growth_source_policy TO ge_readonly;
GRANT SELECT, INSERT, UPDATE ON growth_source_record TO ge_app, ge_worker;
GRANT SELECT ON growth_source_record TO ge_readonly;
GRANT SELECT, INSERT, UPDATE ON growth_evidence TO ge_app, ge_worker;
GRANT SELECT ON growth_evidence TO ge_readonly;
GRANT SELECT, INSERT, UPDATE ON growth_competitor TO ge_app, ge_worker;
GRANT SELECT ON growth_competitor TO ge_readonly;
GRANT SELECT, INSERT, UPDATE ON growth_market_event TO ge_app, ge_worker;
GRANT SELECT ON growth_market_event TO ge_readonly;
GRANT SELECT, INSERT, UPDATE ON growth_search_plan TO ge_app, ge_worker;
GRANT SELECT ON growth_search_plan TO ge_readonly;
GRANT SELECT, INSERT, UPDATE ON growth_organization TO ge_app, ge_worker;
GRANT SELECT ON growth_organization TO ge_readonly;
GRANT SELECT, INSERT, UPDATE ON growth_signal TO ge_app, ge_worker;
GRANT SELECT ON growth_signal TO ge_readonly;
GRANT SELECT, INSERT, UPDATE ON growth_signal_type TO ge_app, ge_worker;
GRANT SELECT ON growth_signal_type TO ge_readonly;
GRANT SELECT, INSERT, UPDATE ON growth_need_evidence TO ge_app, ge_worker;
GRANT SELECT ON growth_need_evidence TO ge_readonly;
GRANT SELECT, INSERT, UPDATE ON growth_referral TO ge_app, ge_worker;
GRANT SELECT ON growth_referral TO ge_readonly;
GRANT SELECT, INSERT, UPDATE ON growth_contact TO ge_app, ge_worker;
GRANT SELECT ON growth_contact TO ge_readonly;
GRANT SELECT, INSERT, UPDATE ON growth_contact_source TO ge_app, ge_worker;
GRANT SELECT ON growth_contact_source TO ge_readonly;
GRANT SELECT, INSERT, UPDATE ON growth_contact_verification TO ge_app, ge_worker;
GRANT SELECT ON growth_contact_verification TO ge_readonly;
GRANT SELECT, INSERT, UPDATE ON growth_consent TO ge_app, ge_worker;
GRANT SELECT ON growth_consent TO ge_readonly;
GRANT SELECT, INSERT, UPDATE ON growth_suppression TO ge_app, ge_worker;
GRANT SELECT ON growth_suppression TO ge_readonly;
GRANT SELECT, INSERT, UPDATE ON growth_need TO ge_app, ge_worker;
GRANT SELECT ON growth_need TO ge_readonly;
GRANT SELECT, INSERT, UPDATE ON growth_product TO ge_app, ge_worker;
GRANT SELECT ON growth_product TO ge_readonly;
GRANT SELECT, INSERT, UPDATE ON growth_opportunity TO ge_app, ge_worker;
GRANT SELECT ON growth_opportunity TO ge_readonly;
GRANT SELECT, INSERT, UPDATE ON growth_score_version TO ge_app, ge_worker;
GRANT SELECT ON growth_score_version TO ge_readonly;
GRANT SELECT, INSERT, UPDATE ON growth_activity TO ge_app, ge_worker;
GRANT SELECT ON growth_activity TO ge_readonly;
GRANT SELECT, INSERT, UPDATE ON growth_deal TO ge_app, ge_worker;
GRANT SELECT ON growth_deal TO ge_readonly;
GRANT SELECT, INSERT, UPDATE ON growth_stage TO ge_app, ge_worker;
GRANT SELECT ON growth_stage TO ge_readonly;
GRANT SELECT, INSERT, UPDATE ON growth_task TO ge_app, ge_worker;
GRANT SELECT ON growth_task TO ge_readonly;
GRANT SELECT, INSERT, UPDATE ON growth_budget TO ge_app, ge_worker;
GRANT SELECT ON growth_budget TO ge_readonly;
GRANT SELECT, INSERT, UPDATE ON growth_message TO ge_app, ge_worker;
GRANT SELECT ON growth_message TO ge_readonly;
GRANT SELECT, INSERT, UPDATE ON growth_message_draft TO ge_app, ge_worker;
GRANT SELECT ON growth_message_draft TO ge_readonly;
GRANT SELECT, INSERT, UPDATE ON growth_message_template TO ge_app, ge_worker;
GRANT SELECT ON growth_message_template TO ge_readonly;
GRANT SELECT, INSERT, UPDATE ON growth_outbox TO ge_app, ge_worker;
GRANT SELECT ON growth_outbox TO ge_readonly;
GRANT SELECT, INSERT, UPDATE ON growth_delivery_event TO ge_app, ge_worker;
GRANT SELECT ON growth_delivery_event TO ge_readonly;
GRANT SELECT, INSERT, UPDATE ON growth_thread TO ge_app, ge_worker;
GRANT SELECT ON growth_thread TO ge_readonly;
GRANT SELECT, INSERT, UPDATE ON growth_channel_account TO ge_app, ge_worker;
GRANT SELECT ON growth_channel_account TO ge_readonly;
GRANT SELECT, INSERT, UPDATE ON growth_inbound_event TO ge_app, ge_worker;
GRANT SELECT ON growth_inbound_event TO ge_readonly;
GRANT SELECT, INSERT, UPDATE ON growth_enrollment TO ge_app, ge_worker;
GRANT SELECT ON growth_enrollment TO ge_readonly;
GRANT SELECT, INSERT, UPDATE ON growth_sequence TO ge_app, ge_worker;
GRANT SELECT ON growth_sequence TO ge_readonly;
GRANT SELECT, INSERT, UPDATE ON growth_sequence_step TO ge_app, ge_worker;
GRANT SELECT ON growth_sequence_step TO ge_readonly;
GRANT SELECT, INSERT, UPDATE ON growth_routing_rule TO ge_app, ge_worker;
GRANT SELECT ON growth_routing_rule TO ge_readonly;
GRANT SELECT, INSERT, UPDATE ON growth_workflow_execution TO ge_app, ge_worker;
GRANT SELECT ON growth_workflow_execution TO ge_readonly;
GRANT SELECT, INSERT, UPDATE ON growth_identity_link TO ge_app, ge_worker;
GRANT SELECT ON growth_identity_link TO ge_readonly;
GRANT SELECT, INSERT, UPDATE ON growth_objection TO ge_app, ge_worker;
GRANT SELECT ON growth_objection TO ge_readonly;
GRANT SELECT, INSERT, UPDATE ON growth_calendar_link TO ge_app, ge_worker;
GRANT SELECT ON growth_calendar_link TO ge_readonly;
GRANT SELECT, INSERT, UPDATE ON growth_meeting TO ge_app, ge_worker;
GRANT SELECT ON growth_meeting TO ge_readonly;
GRANT SELECT, INSERT, UPDATE ON growth_business_event TO ge_app, ge_worker;
GRANT SELECT ON growth_business_event TO ge_readonly;
GRANT SELECT, INSERT, UPDATE ON growth_event_attendance TO ge_app, ge_worker;
GRANT SELECT ON growth_event_attendance TO ge_readonly;
GRANT SELECT, INSERT, UPDATE ON growth_event_registration TO ge_app, ge_worker;
GRANT SELECT ON growth_event_registration TO ge_readonly;
GRANT SELECT, INSERT, UPDATE ON growth_claim TO ge_app, ge_worker;
GRANT SELECT ON growth_claim TO ge_readonly;
GRANT SELECT, INSERT, UPDATE ON growth_content_asset TO ge_app, ge_worker;
GRANT SELECT ON growth_content_asset TO ge_readonly;
GRANT SELECT, INSERT, UPDATE ON growth_content_version TO ge_app, ge_worker;
GRANT SELECT ON growth_content_version TO ge_readonly;
GRANT SELECT, INSERT, UPDATE ON growth_approval TO ge_app, ge_worker;
GRANT SELECT ON growth_approval TO ge_readonly;
GRANT SELECT, INSERT, UPDATE ON growth_social_post TO ge_app, ge_worker;
GRANT SELECT ON growth_social_post TO ge_readonly;
GRANT SELECT, INSERT, UPDATE ON growth_social_publication TO ge_app, ge_worker;
GRANT SELECT ON growth_social_publication TO ge_readonly;
GRANT SELECT, INSERT, UPDATE ON growth_keyword TO ge_app, ge_worker;
GRANT SELECT ON growth_keyword TO ge_readonly;
GRANT SELECT, INSERT, UPDATE ON growth_page_metric TO ge_app, ge_worker;
GRANT SELECT ON growth_page_metric TO ge_readonly;
GRANT SELECT, INSERT, UPDATE ON growth_seo_issue TO ge_app, ge_worker;
GRANT SELECT ON growth_seo_issue TO ge_readonly;
GRANT SELECT, INSERT, UPDATE ON growth_landing_page TO ge_app, ge_worker;
GRANT SELECT ON growth_landing_page TO ge_readonly;
GRANT SELECT, INSERT, UPDATE ON growth_audience TO ge_app, ge_worker;
GRANT SELECT ON growth_audience TO ge_readonly;
GRANT SELECT, INSERT, UPDATE ON growth_campaign TO ge_app, ge_worker;
GRANT SELECT ON growth_campaign TO ge_readonly;
GRANT SELECT, INSERT, UPDATE ON growth_campaign_version TO ge_app, ge_worker;
GRANT SELECT ON growth_campaign_version TO ge_readonly;
GRANT SELECT, INSERT, UPDATE ON growth_ad_campaign TO ge_app, ge_worker;
GRANT SELECT ON growth_ad_campaign TO ge_readonly;
GRANT SELECT, INSERT, UPDATE ON growth_ad_spend_event TO ge_app, ge_worker;
GRANT SELECT ON growth_ad_spend_event TO ge_readonly;
GRANT SELECT, INSERT, UPDATE ON growth_attribution_event TO ge_app, ge_worker;
GRANT SELECT ON growth_attribution_event TO ge_readonly;
GRANT SELECT, INSERT, UPDATE ON growth_form TO ge_app, ge_worker;
GRANT SELECT ON growth_form TO ge_readonly;
GRANT SELECT, INSERT, UPDATE ON growth_lead TO ge_app, ge_worker;
GRANT SELECT ON growth_lead TO ge_readonly;
GRANT SELECT, INSERT, UPDATE ON growth_proposal TO ge_app, ge_worker;
GRANT SELECT ON growth_proposal TO ge_readonly;
GRANT SELECT, INSERT, UPDATE ON growth_proposal_version TO ge_app, ge_worker;
GRANT SELECT ON growth_proposal_version TO ge_readonly;
GRANT SELECT, INSERT, UPDATE ON growth_quote TO ge_app, ge_worker;
GRANT SELECT ON growth_quote TO ge_readonly;
GRANT SELECT, INSERT, UPDATE ON growth_quote_line TO ge_app, ge_worker;
GRANT SELECT ON growth_quote_line TO ge_readonly;
GRANT SELECT, INSERT, UPDATE ON growth_negotiation TO ge_app, ge_worker;
GRANT SELECT ON growth_negotiation TO ge_readonly;
GRANT SELECT, INSERT, UPDATE ON growth_contract TO ge_app, ge_worker;
GRANT SELECT ON growth_contract TO ge_readonly;
GRANT SELECT, INSERT, UPDATE ON growth_integration_deal TO ge_app, ge_worker;
GRANT SELECT ON growth_integration_deal TO ge_readonly;
GRANT SELECT, INSERT, UPDATE ON sales_bid TO ge_app, ge_worker;
GRANT SELECT ON sales_bid TO ge_readonly;
GRANT SELECT, INSERT, UPDATE ON growth_invoice TO ge_app, ge_worker;
GRANT SELECT ON growth_invoice TO ge_readonly;
GRANT SELECT, INSERT, UPDATE ON growth_payment TO ge_app, ge_worker;
GRANT SELECT ON growth_payment TO ge_readonly;
GRANT SELECT, INSERT, UPDATE ON sales_fulfillment TO ge_app, ge_worker;
GRANT SELECT ON sales_fulfillment TO ge_readonly;
GRANT SELECT, INSERT, UPDATE ON sales_order TO ge_app, ge_worker;
GRANT SELECT ON sales_order TO ge_readonly;
GRANT SELECT, INSERT, UPDATE ON sales_order_line TO ge_app, ge_worker;
GRANT SELECT ON sales_order_line TO ge_readonly;
GRANT SELECT, INSERT, UPDATE ON growth_onboarding TO ge_app, ge_worker;
GRANT SELECT ON growth_onboarding TO ge_readonly;
GRANT SELECT, INSERT, UPDATE ON growth_deployment TO ge_app, ge_worker;
GRANT SELECT ON growth_deployment TO ge_readonly;
GRANT SELECT, INSERT, UPDATE ON growth_partner TO ge_app, ge_worker;
GRANT SELECT ON growth_partner TO ge_readonly;
GRANT SELECT, INSERT, UPDATE ON growth_pilot TO ge_app, ge_worker;
GRANT SELECT ON growth_pilot TO ge_readonly;
GRANT SELECT, INSERT, UPDATE ON growth_renewal TO ge_app, ge_worker;
GRANT SELECT ON growth_renewal TO ge_readonly;
GRANT SELECT, INSERT, UPDATE ON growth_feedback TO ge_app, ge_worker;
GRANT SELECT ON growth_feedback TO ge_readonly;
GRANT SELECT, INSERT, UPDATE ON growth_metric_snapshot TO ge_app, ge_worker;
GRANT SELECT ON growth_metric_snapshot TO ge_readonly;
GRANT SELECT, INSERT, UPDATE ON growth_forecast TO ge_app, ge_worker;
GRANT SELECT ON growth_forecast TO ge_readonly;
GRANT SELECT, INSERT, UPDATE ON growth_stage_metric TO ge_app, ge_worker;
GRANT SELECT ON growth_stage_metric TO ge_readonly;
GRANT SELECT, INSERT, UPDATE ON growth_document TO ge_app, ge_worker;
GRANT SELECT ON growth_document TO ge_readonly;
GRANT SELECT, INSERT, UPDATE ON growth_document_chunk TO ge_app, ge_worker;
GRANT SELECT ON growth_document_chunk TO ge_readonly;
GRANT SELECT, INSERT, UPDATE ON growth_embedding TO ge_app, ge_worker;
GRANT SELECT ON growth_embedding TO ge_readonly;
GRANT SELECT, INSERT, UPDATE ON identity_provider TO ge_app, ge_worker;
GRANT SELECT, INSERT, UPDATE ON scim_token TO ge_app, ge_worker;
GRANT SELECT, INSERT, UPDATE ON custom_role TO ge_app, ge_worker;
GRANT SELECT ON custom_role TO ge_readonly;
GRANT SELECT, INSERT, UPDATE ON role_permission TO ge_app, ge_worker;
GRANT SELECT ON role_permission TO ge_readonly;
GRANT SELECT ON sod_conflict TO ge_app, ge_worker, ge_readonly;
GRANT SELECT, INSERT, UPDATE ON api_key TO ge_app, ge_worker;
GRANT SELECT, INSERT, UPDATE ON webhook_endpoint TO ge_app, ge_worker;
GRANT SELECT ON webhook_endpoint TO ge_readonly;
GRANT SELECT, INSERT, UPDATE ON webhook_delivery TO ge_app, ge_worker;
GRANT SELECT ON webhook_delivery TO ge_readonly;
GRANT SELECT, INSERT, UPDATE ON audit_sink TO ge_app, ge_worker;
GRANT SELECT ON audit_sink TO ge_readonly;
GRANT SELECT, INSERT, UPDATE ON export_job TO ge_app, ge_worker;
GRANT SELECT ON export_job TO ge_readonly;
GRANT SELECT, INSERT, UPDATE ON tenant_key_config TO ge_app, ge_worker;
GRANT SELECT, INSERT, UPDATE ON sandbox_environment TO ge_app, ge_worker;
GRANT SELECT ON sandbox_environment TO ge_readonly;
GRANT SELECT, INSERT, UPDATE ON config_promotion TO ge_app, ge_worker;
GRANT SELECT ON config_promotion TO ge_readonly;
GRANT SELECT, INSERT, UPDATE ON connector_installation TO ge_app, ge_worker;
GRANT SELECT ON connector_installation TO ge_readonly;
GRANT SELECT ON security_finding TO ge_platform_sec;
GRANT SELECT, INSERT, UPDATE ON security_finding TO ge_platform_sec;
GRANT SELECT ON ops_incident TO ge_app, ge_worker, ge_readonly;
GRANT SELECT, INSERT, UPDATE ON ops_incident TO ge_platform_sec;
GRANT SELECT ON tax_rule TO ge_app, ge_worker, ge_readonly;
GRANT SELECT, INSERT, UPDATE ON invoice TO ge_app, ge_worker;
GRANT SELECT ON invoice TO ge_readonly;
GRANT SELECT ON locale_bundle TO ge_app, ge_worker, ge_readonly;
GRANT SELECT, INSERT, UPDATE ON user_role_assignment TO ge_app, ge_worker;
GRANT SELECT ON user_role_assignment TO ge_readonly;
GRANT SELECT, INSERT, UPDATE ON tenant_data_key TO ge_app, ge_worker;
GRANT SELECT ON domain_schema_registry TO ge_app, ge_worker, ge_readonly;
GRANT SELECT, INSERT, UPDATE ON company_operating_country TO ge_app, ge_worker;
GRANT SELECT ON company_operating_country TO ge_readonly;
GRANT SELECT, INSERT, UPDATE ON offering_market TO ge_app, ge_worker;
GRANT SELECT ON offering_market TO ge_readonly;
GRANT SELECT, INSERT, UPDATE ON channel_account_market TO ge_app, ge_worker;
GRANT SELECT ON channel_account_market TO ge_readonly;
GRANT SELECT, INSERT, UPDATE ON configuration_revision TO ge_app, ge_worker;
GRANT SELECT ON configuration_revision TO ge_readonly;
GRANT SELECT, INSERT, UPDATE ON workflow_configuration TO ge_app, ge_worker;
GRANT SELECT ON workflow_configuration TO ge_readonly;
GRANT SELECT, INSERT ON business_event TO ge_app, ge_worker;
GRANT SELECT ON business_event TO ge_readonly;
GRANT SELECT ON metric_definition TO ge_app, ge_worker, ge_readonly;
GRANT SELECT, INSERT, UPDATE ON metric_aggregate TO ge_app, ge_worker;
GRANT SELECT ON metric_aggregate TO ge_readonly;
GRANT SELECT, INSERT, UPDATE ON experiment TO ge_app, ge_worker;
GRANT SELECT ON experiment TO ge_readonly;
GRANT SELECT, INSERT, UPDATE ON feedback_case TO ge_app, ge_worker;
GRANT SELECT ON feedback_case TO ge_readonly;
GRANT SELECT ON sli_sample TO ge_app, ge_worker, ge_readonly;
GRANT SELECT, INSERT, UPDATE ON customer_value TO ge_app, ge_worker;
GRANT SELECT ON customer_value TO ge_readonly;
GRANT SELECT, INSERT, UPDATE ON journey_event TO ge_app, ge_worker;
GRANT SELECT ON journey_event TO ge_readonly;
GRANT SELECT, INSERT ON domain_record_version TO ge_app, ge_worker;
GRANT SELECT ON domain_record_version TO ge_readonly;
GRANT SELECT, INSERT, UPDATE ON usage_reservation TO ge_app, ge_worker;
GRANT SELECT ON usage_reservation TO ge_readonly;
GRANT USAGE ON ALL SEQUENCES IN SCHEMA public TO ge_app, ge_worker;
DROP POLICY IF EXISTS organization_tenant ON organization;
DROP POLICY IF EXISTS company_tenant ON company;
DROP POLICY IF EXISTS division_tenant ON division;
DROP POLICY IF EXISTS brand_tenant ON brand;
DROP POLICY IF EXISTS offering_tenant ON offering;
DROP POLICY IF EXISTS market_tenant ON market;
DROP POLICY IF EXISTS channel_account_tenant ON channel_account;
DROP POLICY IF EXISTS workflow_run_tenant ON workflow_run;
DROP POLICY IF EXISTS workflow_step_run_tenant ON workflow_step_run;
DROP POLICY IF EXISTS effect_tenant ON effect;
DROP POLICY IF EXISTS outbox_tenant ON outbox;
DROP POLICY IF EXISTS audit_event_tenant ON audit_event;
DROP POLICY IF EXISTS consent_record_tenant ON consent_record;
DROP POLICY IF EXISTS suppression_tenant ON suppression;
DROP POLICY IF EXISTS dsar_request_tenant ON dsar_request;
DROP POLICY IF EXISTS ai_usage_event_tenant ON ai_usage_event;
DROP POLICY IF EXISTS ai_budget_tenant ON ai_budget;
DROP POLICY IF EXISTS growth_source_tenant ON growth_source;
DROP POLICY IF EXISTS growth_source_policy_tenant ON growth_source_policy;
DROP POLICY IF EXISTS growth_source_record_tenant ON growth_source_record;
DROP POLICY IF EXISTS growth_evidence_tenant ON growth_evidence;
DROP POLICY IF EXISTS growth_competitor_tenant ON growth_competitor;
DROP POLICY IF EXISTS growth_market_event_tenant ON growth_market_event;
DROP POLICY IF EXISTS growth_search_plan_tenant ON growth_search_plan;
DROP POLICY IF EXISTS growth_organization_tenant ON growth_organization;
DROP POLICY IF EXISTS growth_signal_tenant ON growth_signal;
DROP POLICY IF EXISTS growth_signal_type_tenant ON growth_signal_type;
DROP POLICY IF EXISTS growth_need_evidence_tenant ON growth_need_evidence;
DROP POLICY IF EXISTS growth_referral_tenant ON growth_referral;
DROP POLICY IF EXISTS growth_contact_tenant ON growth_contact;
DROP POLICY IF EXISTS growth_contact_source_tenant ON growth_contact_source;
DROP POLICY IF EXISTS growth_contact_verification_tenant ON growth_contact_verification;
DROP POLICY IF EXISTS growth_consent_tenant ON growth_consent;
DROP POLICY IF EXISTS growth_suppression_tenant ON growth_suppression;
DROP POLICY IF EXISTS growth_need_tenant ON growth_need;
DROP POLICY IF EXISTS growth_product_tenant ON growth_product;
DROP POLICY IF EXISTS growth_opportunity_tenant ON growth_opportunity;
DROP POLICY IF EXISTS growth_score_version_tenant ON growth_score_version;
DROP POLICY IF EXISTS growth_activity_tenant ON growth_activity;
DROP POLICY IF EXISTS growth_deal_tenant ON growth_deal;
DROP POLICY IF EXISTS growth_stage_tenant ON growth_stage;
DROP POLICY IF EXISTS growth_task_tenant ON growth_task;
DROP POLICY IF EXISTS growth_budget_tenant ON growth_budget;
DROP POLICY IF EXISTS growth_message_tenant ON growth_message;
DROP POLICY IF EXISTS growth_message_draft_tenant ON growth_message_draft;
DROP POLICY IF EXISTS growth_message_template_tenant ON growth_message_template;
DROP POLICY IF EXISTS growth_outbox_tenant ON growth_outbox;
DROP POLICY IF EXISTS growth_delivery_event_tenant ON growth_delivery_event;
DROP POLICY IF EXISTS growth_thread_tenant ON growth_thread;
DROP POLICY IF EXISTS growth_channel_account_tenant ON growth_channel_account;
DROP POLICY IF EXISTS growth_inbound_event_tenant ON growth_inbound_event;
DROP POLICY IF EXISTS growth_enrollment_tenant ON growth_enrollment;
DROP POLICY IF EXISTS growth_sequence_tenant ON growth_sequence;
DROP POLICY IF EXISTS growth_sequence_step_tenant ON growth_sequence_step;
DROP POLICY IF EXISTS growth_routing_rule_tenant ON growth_routing_rule;
DROP POLICY IF EXISTS growth_workflow_execution_tenant ON growth_workflow_execution;
DROP POLICY IF EXISTS growth_identity_link_tenant ON growth_identity_link;
DROP POLICY IF EXISTS growth_objection_tenant ON growth_objection;
DROP POLICY IF EXISTS growth_calendar_link_tenant ON growth_calendar_link;
DROP POLICY IF EXISTS growth_meeting_tenant ON growth_meeting;
DROP POLICY IF EXISTS growth_business_event_tenant ON growth_business_event;
DROP POLICY IF EXISTS growth_event_attendance_tenant ON growth_event_attendance;
DROP POLICY IF EXISTS growth_event_registration_tenant ON growth_event_registration;
DROP POLICY IF EXISTS growth_claim_tenant ON growth_claim;
DROP POLICY IF EXISTS growth_content_asset_tenant ON growth_content_asset;
DROP POLICY IF EXISTS growth_content_version_tenant ON growth_content_version;
DROP POLICY IF EXISTS growth_approval_tenant ON growth_approval;
DROP POLICY IF EXISTS growth_social_post_tenant ON growth_social_post;
DROP POLICY IF EXISTS growth_social_publication_tenant ON growth_social_publication;
DROP POLICY IF EXISTS growth_keyword_tenant ON growth_keyword;
DROP POLICY IF EXISTS growth_page_metric_tenant ON growth_page_metric;
DROP POLICY IF EXISTS growth_seo_issue_tenant ON growth_seo_issue;
DROP POLICY IF EXISTS growth_landing_page_tenant ON growth_landing_page;
DROP POLICY IF EXISTS growth_audience_tenant ON growth_audience;
DROP POLICY IF EXISTS growth_campaign_tenant ON growth_campaign;
DROP POLICY IF EXISTS growth_campaign_version_tenant ON growth_campaign_version;
DROP POLICY IF EXISTS growth_ad_campaign_tenant ON growth_ad_campaign;
DROP POLICY IF EXISTS growth_ad_spend_event_tenant ON growth_ad_spend_event;
DROP POLICY IF EXISTS growth_attribution_event_tenant ON growth_attribution_event;
DROP POLICY IF EXISTS growth_form_tenant ON growth_form;
DROP POLICY IF EXISTS growth_lead_tenant ON growth_lead;
DROP POLICY IF EXISTS growth_proposal_tenant ON growth_proposal;
DROP POLICY IF EXISTS growth_proposal_version_tenant ON growth_proposal_version;
DROP POLICY IF EXISTS growth_quote_tenant ON growth_quote;
DROP POLICY IF EXISTS growth_quote_line_tenant ON growth_quote_line;
DROP POLICY IF EXISTS growth_negotiation_tenant ON growth_negotiation;
DROP POLICY IF EXISTS growth_contract_tenant ON growth_contract;
DROP POLICY IF EXISTS growth_integration_deal_tenant ON growth_integration_deal;
DROP POLICY IF EXISTS sales_bid_tenant ON sales_bid;
DROP POLICY IF EXISTS growth_invoice_tenant ON growth_invoice;
DROP POLICY IF EXISTS growth_payment_tenant ON growth_payment;
DROP POLICY IF EXISTS sales_fulfillment_tenant ON sales_fulfillment;
DROP POLICY IF EXISTS sales_order_tenant ON sales_order;
DROP POLICY IF EXISTS sales_order_line_tenant ON sales_order_line;
DROP POLICY IF EXISTS growth_onboarding_tenant ON growth_onboarding;
DROP POLICY IF EXISTS growth_deployment_tenant ON growth_deployment;
DROP POLICY IF EXISTS growth_partner_tenant ON growth_partner;
DROP POLICY IF EXISTS growth_pilot_tenant ON growth_pilot;
DROP POLICY IF EXISTS growth_renewal_tenant ON growth_renewal;
DROP POLICY IF EXISTS growth_feedback_tenant ON growth_feedback;
DROP POLICY IF EXISTS growth_metric_snapshot_tenant ON growth_metric_snapshot;
DROP POLICY IF EXISTS growth_forecast_tenant ON growth_forecast;
DROP POLICY IF EXISTS growth_stage_metric_tenant ON growth_stage_metric;
DROP POLICY IF EXISTS growth_document_tenant ON growth_document;
DROP POLICY IF EXISTS growth_document_chunk_tenant ON growth_document_chunk;
DROP POLICY IF EXISTS growth_embedding_tenant ON growth_embedding;
DROP POLICY IF EXISTS identity_provider_tenant ON identity_provider;
DROP POLICY IF EXISTS scim_token_tenant ON scim_token;
DROP POLICY IF EXISTS custom_role_tenant ON custom_role;
DROP POLICY IF EXISTS role_permission_tenant ON role_permission;
DROP POLICY IF EXISTS api_key_tenant ON api_key;
DROP POLICY IF EXISTS webhook_endpoint_tenant ON webhook_endpoint;
DROP POLICY IF EXISTS webhook_delivery_tenant ON webhook_delivery;
DROP POLICY IF EXISTS audit_sink_tenant ON audit_sink;
DROP POLICY IF EXISTS export_job_tenant ON export_job;
DROP POLICY IF EXISTS tenant_key_config_tenant ON tenant_key_config;
DROP POLICY IF EXISTS sandbox_environment_tenant ON sandbox_environment;
DROP POLICY IF EXISTS config_promotion_tenant ON config_promotion;
DROP POLICY IF EXISTS connector_installation_tenant ON connector_installation;
DROP POLICY IF EXISTS invoice_tenant ON invoice;
ALTER TABLE tenant ENABLE ROW LEVEL SECURITY; ALTER TABLE tenant FORCE ROW LEVEL SECURITY;
CREATE POLICY rls_tenant__select ON tenant FOR SELECT USING (tenant_id = (SELECT app_tenant()));
ALTER TABLE organization ENABLE ROW LEVEL SECURITY; ALTER TABLE organization FORCE ROW LEVEL SECURITY;
CREATE POLICY rls_organization__select ON organization FOR SELECT USING (tenant_id = (SELECT app_tenant()));
CREATE POLICY rls_organization__insert ON organization FOR INSERT WITH CHECK (tenant_id = (SELECT app_tenant()));
CREATE POLICY rls_organization__update ON organization FOR UPDATE USING (tenant_id = (SELECT app_tenant())) WITH CHECK (tenant_id = (SELECT app_tenant()));
ALTER TABLE company ENABLE ROW LEVEL SECURITY; ALTER TABLE company FORCE ROW LEVEL SECURITY;
CREATE POLICY rls_company__select ON company FOR SELECT USING (tenant_id = (SELECT app_tenant()) AND company_id = ANY ((SELECT app_company_ids())::uuid[]));
CREATE POLICY rls_company__insert ON company FOR INSERT WITH CHECK (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company()));
CREATE POLICY rls_company__update ON company FOR UPDATE USING (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company())) WITH CHECK (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company()));
ALTER TABLE division ENABLE ROW LEVEL SECURITY; ALTER TABLE division FORCE ROW LEVEL SECURITY;
CREATE POLICY rls_division__select ON division FOR SELECT USING (tenant_id = (SELECT app_tenant()) AND (company_id = ANY ((SELECT app_company_ids())::uuid[]) OR company_id IS NULL));
CREATE POLICY rls_division__insert ON division FOR INSERT WITH CHECK (tenant_id = (SELECT app_tenant()) AND (company_id = (SELECT app_write_company()) OR (company_id IS NULL AND (SELECT app_actor_kind()) = 'service')));
CREATE POLICY rls_division__update ON division FOR UPDATE USING (tenant_id = (SELECT app_tenant()) AND (company_id = (SELECT app_write_company()) OR (company_id IS NULL AND (SELECT app_actor_kind()) = 'service'))) WITH CHECK (tenant_id = (SELECT app_tenant()) AND (company_id = (SELECT app_write_company()) OR (company_id IS NULL AND (SELECT app_actor_kind()) = 'service')));
ALTER TABLE brand ENABLE ROW LEVEL SECURITY; ALTER TABLE brand FORCE ROW LEVEL SECURITY;
CREATE POLICY rls_brand__select ON brand FOR SELECT USING (tenant_id = (SELECT app_tenant()) AND (company_id = ANY ((SELECT app_company_ids())::uuid[]) OR company_id IS NULL));
CREATE POLICY rls_brand__insert ON brand FOR INSERT WITH CHECK (tenant_id = (SELECT app_tenant()) AND (company_id = (SELECT app_write_company()) OR (company_id IS NULL AND (SELECT app_actor_kind()) = 'service')));
CREATE POLICY rls_brand__update ON brand FOR UPDATE USING (tenant_id = (SELECT app_tenant()) AND (company_id = (SELECT app_write_company()) OR (company_id IS NULL AND (SELECT app_actor_kind()) = 'service'))) WITH CHECK (tenant_id = (SELECT app_tenant()) AND (company_id = (SELECT app_write_company()) OR (company_id IS NULL AND (SELECT app_actor_kind()) = 'service')));
ALTER TABLE offering ENABLE ROW LEVEL SECURITY; ALTER TABLE offering FORCE ROW LEVEL SECURITY;
CREATE POLICY rls_offering__select ON offering FOR SELECT USING (tenant_id = (SELECT app_tenant()) AND (company_id = ANY ((SELECT app_company_ids())::uuid[]) OR company_id IS NULL));
CREATE POLICY rls_offering__insert ON offering FOR INSERT WITH CHECK (tenant_id = (SELECT app_tenant()) AND (company_id = (SELECT app_write_company()) OR (company_id IS NULL AND (SELECT app_actor_kind()) = 'service')));
CREATE POLICY rls_offering__update ON offering FOR UPDATE USING (tenant_id = (SELECT app_tenant()) AND (company_id = (SELECT app_write_company()) OR (company_id IS NULL AND (SELECT app_actor_kind()) = 'service'))) WITH CHECK (tenant_id = (SELECT app_tenant()) AND (company_id = (SELECT app_write_company()) OR (company_id IS NULL AND (SELECT app_actor_kind()) = 'service')));
ALTER TABLE market ENABLE ROW LEVEL SECURITY; ALTER TABLE market FORCE ROW LEVEL SECURITY;
CREATE POLICY rls_market__select ON market FOR SELECT USING (tenant_id = (SELECT app_tenant()) AND (company_id = ANY ((SELECT app_company_ids())::uuid[]) OR company_id IS NULL));
CREATE POLICY rls_market__insert ON market FOR INSERT WITH CHECK (tenant_id = (SELECT app_tenant()) AND (company_id = (SELECT app_write_company()) OR (company_id IS NULL AND (SELECT app_actor_kind()) = 'service')));
CREATE POLICY rls_market__update ON market FOR UPDATE USING (tenant_id = (SELECT app_tenant()) AND (company_id = (SELECT app_write_company()) OR (company_id IS NULL AND (SELECT app_actor_kind()) = 'service'))) WITH CHECK (tenant_id = (SELECT app_tenant()) AND (company_id = (SELECT app_write_company()) OR (company_id IS NULL AND (SELECT app_actor_kind()) = 'service')));
ALTER TABLE channel_account ENABLE ROW LEVEL SECURITY; ALTER TABLE channel_account FORCE ROW LEVEL SECURITY;
CREATE POLICY rls_channel_account__select ON channel_account FOR SELECT USING (tenant_id = (SELECT app_tenant()) AND (company_id = ANY ((SELECT app_company_ids())::uuid[]) OR company_id IS NULL));
CREATE POLICY rls_channel_account__insert ON channel_account FOR INSERT WITH CHECK (tenant_id = (SELECT app_tenant()) AND (company_id = (SELECT app_write_company()) OR (company_id IS NULL AND (SELECT app_actor_kind()) = 'service')));
CREATE POLICY rls_channel_account__update ON channel_account FOR UPDATE USING (tenant_id = (SELECT app_tenant()) AND (company_id = (SELECT app_write_company()) OR (company_id IS NULL AND (SELECT app_actor_kind()) = 'service'))) WITH CHECK (tenant_id = (SELECT app_tenant()) AND (company_id = (SELECT app_write_company()) OR (company_id IS NULL AND (SELECT app_actor_kind()) = 'service')));
ALTER TABLE workflow_run ENABLE ROW LEVEL SECURITY; ALTER TABLE workflow_run FORCE ROW LEVEL SECURITY;
CREATE POLICY rls_workflow_run__select ON workflow_run FOR SELECT USING (tenant_id = (SELECT app_tenant()) AND (company_id = ANY ((SELECT app_company_ids())::uuid[]) OR company_id IS NULL));
CREATE POLICY rls_workflow_run__insert ON workflow_run FOR INSERT WITH CHECK (tenant_id = (SELECT app_tenant()) AND (company_id = (SELECT app_write_company()) OR (company_id IS NULL AND (SELECT app_actor_kind()) = 'service')));
CREATE POLICY rls_workflow_run__update ON workflow_run FOR UPDATE USING (tenant_id = (SELECT app_tenant()) AND (company_id = (SELECT app_write_company()) OR (company_id IS NULL AND (SELECT app_actor_kind()) = 'service'))) WITH CHECK (tenant_id = (SELECT app_tenant()) AND (company_id = (SELECT app_write_company()) OR (company_id IS NULL AND (SELECT app_actor_kind()) = 'service')));
ALTER TABLE workflow_step_run ENABLE ROW LEVEL SECURITY; ALTER TABLE workflow_step_run FORCE ROW LEVEL SECURITY;
CREATE POLICY rls_workflow_step_run__select ON workflow_step_run FOR SELECT USING (tenant_id = (SELECT app_tenant()) AND company_id = ANY ((SELECT app_company_ids())::uuid[]));
CREATE POLICY rls_workflow_step_run__insert ON workflow_step_run FOR INSERT WITH CHECK (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company()));
CREATE POLICY rls_workflow_step_run__update ON workflow_step_run FOR UPDATE USING (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company())) WITH CHECK (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company()));
ALTER TABLE effect ENABLE ROW LEVEL SECURITY; ALTER TABLE effect FORCE ROW LEVEL SECURITY;
CREATE POLICY rls_effect__select ON effect FOR SELECT USING (tenant_id = (SELECT app_tenant()) AND company_id = ANY ((SELECT app_company_ids())::uuid[]));
CREATE POLICY rls_effect__insert ON effect FOR INSERT WITH CHECK (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company()));
CREATE POLICY rls_effect__update ON effect FOR UPDATE USING (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company())) WITH CHECK (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company()));
ALTER TABLE outbox ENABLE ROW LEVEL SECURITY; ALTER TABLE outbox FORCE ROW LEVEL SECURITY;
CREATE POLICY rls_outbox__select ON outbox FOR SELECT USING (tenant_id = (SELECT app_tenant()) AND (company_id = ANY ((SELECT app_company_ids())::uuid[]) OR company_id IS NULL));
CREATE POLICY rls_outbox__insert ON outbox FOR INSERT WITH CHECK (tenant_id = (SELECT app_tenant()) AND (company_id = (SELECT app_write_company()) OR (company_id IS NULL AND (SELECT app_actor_kind()) = 'service')));
CREATE POLICY rls_outbox__update ON outbox FOR UPDATE USING (tenant_id = (SELECT app_tenant()) AND (company_id = (SELECT app_write_company()) OR (company_id IS NULL AND (SELECT app_actor_kind()) = 'service'))) WITH CHECK (tenant_id = (SELECT app_tenant()) AND (company_id = (SELECT app_write_company()) OR (company_id IS NULL AND (SELECT app_actor_kind()) = 'service')));
ALTER TABLE inbox ENABLE ROW LEVEL SECURITY; ALTER TABLE inbox FORCE ROW LEVEL SECURITY;
CREATE POLICY rls_inbox__select ON inbox FOR SELECT USING (tenant_id = (SELECT app_tenant()));
CREATE POLICY rls_inbox__insert ON inbox FOR INSERT WITH CHECK (tenant_id = (SELECT app_tenant()) AND (SELECT app_actor_kind()) = 'service');
CREATE POLICY rls_inbox__update ON inbox FOR UPDATE USING (tenant_id = (SELECT app_tenant())) WITH CHECK (tenant_id = (SELECT app_tenant()));
ALTER TABLE audit_event ENABLE ROW LEVEL SECURITY; ALTER TABLE audit_event FORCE ROW LEVEL SECURITY;
CREATE POLICY rls_audit_event__select ON audit_event FOR SELECT USING (tenant_id = (SELECT app_tenant()) AND (company_id = ANY ((SELECT app_company_ids())::uuid[]) OR company_id IS NULL));
ALTER TABLE portfolio_grant ENABLE ROW LEVEL SECURITY; ALTER TABLE portfolio_grant FORCE ROW LEVEL SECURITY;
CREATE POLICY rls_portfolio_grant__select ON portfolio_grant FOR SELECT USING (tenant_id = (SELECT app_tenant()) AND (company_id = ANY ((SELECT app_company_ids())::uuid[]) OR portfolio_id = (SELECT app_portfolio_id())) AND revoked_at IS NULL AND expires_at > now());
CREATE POLICY rls_portfolio_grant__insert ON portfolio_grant FOR INSERT WITH CHECK (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company()) AND (SELECT app_actor_kind()) = 'internal');
CREATE POLICY rls_portfolio_grant__update ON portfolio_grant FOR UPDATE USING (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company())) WITH CHECK (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company()));
ALTER TABLE consent_record ENABLE ROW LEVEL SECURITY; ALTER TABLE consent_record FORCE ROW LEVEL SECURITY;
CREATE POLICY rls_consent_record__select ON consent_record FOR SELECT USING (tenant_id = (SELECT app_tenant()) AND company_id = ANY ((SELECT app_company_ids())::uuid[]));
CREATE POLICY rls_consent_record__insert ON consent_record FOR INSERT WITH CHECK (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company()));
ALTER TABLE suppression ENABLE ROW LEVEL SECURITY; ALTER TABLE suppression FORCE ROW LEVEL SECURITY;
CREATE POLICY rls_suppression__select ON suppression FOR SELECT USING (tenant_id = (SELECT app_tenant()) AND company_id = ANY ((SELECT app_company_ids())::uuid[]));
CREATE POLICY rls_suppression__insert ON suppression FOR INSERT WITH CHECK (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company()));
CREATE POLICY rls_suppression__update ON suppression FOR UPDATE USING (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company())) WITH CHECK (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company()));
ALTER TABLE dsar_request ENABLE ROW LEVEL SECURITY; ALTER TABLE dsar_request FORCE ROW LEVEL SECURITY;
CREATE POLICY rls_dsar_request__select ON dsar_request FOR SELECT USING (tenant_id = (SELECT app_tenant()));
CREATE POLICY rls_dsar_request__insert ON dsar_request FOR INSERT WITH CHECK (tenant_id = (SELECT app_tenant()));
CREATE POLICY rls_dsar_request__update ON dsar_request FOR UPDATE USING (tenant_id = (SELECT app_tenant())) WITH CHECK (tenant_id = (SELECT app_tenant()));
ALTER TABLE incident ENABLE ROW LEVEL SECURITY; ALTER TABLE incident FORCE ROW LEVEL SECURITY;
CREATE POLICY rls_incident__select ON incident FOR SELECT TO ge_app, ge_worker, ge_readonly USING (tenant_id = (SELECT app_tenant()));
CREATE POLICY rls_incident__insert ON incident FOR INSERT TO ge_app, ge_worker WITH CHECK (tenant_id = (SELECT app_tenant()));
CREATE POLICY rls_incident__platform ON incident FOR ALL TO ge_platform_sec USING (true) WITH CHECK (true);
GRANT SELECT, INSERT, UPDATE ON incident TO ge_platform_sec;
ALTER TABLE ai_usage_event ENABLE ROW LEVEL SECURITY; ALTER TABLE ai_usage_event FORCE ROW LEVEL SECURITY;
CREATE POLICY rls_ai_usage_event__select ON ai_usage_event FOR SELECT USING (tenant_id = (SELECT app_tenant()) AND (company_id = ANY ((SELECT app_company_ids())::uuid[]) OR company_id IS NULL));
CREATE POLICY rls_ai_usage_event__insert ON ai_usage_event FOR INSERT WITH CHECK (tenant_id = (SELECT app_tenant()) AND (company_id = (SELECT app_write_company()) OR (company_id IS NULL AND (SELECT app_actor_kind()) = 'service')));
ALTER TABLE ai_budget ENABLE ROW LEVEL SECURITY; ALTER TABLE ai_budget FORCE ROW LEVEL SECURITY;
CREATE POLICY rls_ai_budget__select ON ai_budget FOR SELECT USING (tenant_id = (SELECT app_tenant()));
CREATE POLICY rls_ai_budget__insert ON ai_budget FOR INSERT WITH CHECK (tenant_id = (SELECT app_tenant()));
CREATE POLICY rls_ai_budget__update ON ai_budget FOR UPDATE USING (tenant_id = (SELECT app_tenant())) WITH CHECK (tenant_id = (SELECT app_tenant()));
ALTER TABLE growth_source ENABLE ROW LEVEL SECURITY; ALTER TABLE growth_source FORCE ROW LEVEL SECURITY;
CREATE POLICY rls_growth_source__select ON growth_source FOR SELECT USING (tenant_id = (SELECT app_tenant()) AND company_id = ANY ((SELECT app_company_ids())::uuid[]));
CREATE POLICY rls_growth_source__insert ON growth_source FOR INSERT WITH CHECK (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company()));
CREATE POLICY rls_growth_source__update ON growth_source FOR UPDATE USING (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company())) WITH CHECK (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company()));
ALTER TABLE growth_source_policy ENABLE ROW LEVEL SECURITY; ALTER TABLE growth_source_policy FORCE ROW LEVEL SECURITY;
CREATE POLICY rls_growth_source_policy__select ON growth_source_policy FOR SELECT USING (tenant_id = (SELECT app_tenant()) AND company_id = ANY ((SELECT app_company_ids())::uuid[]));
CREATE POLICY rls_growth_source_policy__insert ON growth_source_policy FOR INSERT WITH CHECK (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company()));
CREATE POLICY rls_growth_source_policy__update ON growth_source_policy FOR UPDATE USING (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company())) WITH CHECK (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company()));
ALTER TABLE growth_source_record ENABLE ROW LEVEL SECURITY; ALTER TABLE growth_source_record FORCE ROW LEVEL SECURITY;
CREATE POLICY rls_growth_source_record__select ON growth_source_record FOR SELECT USING (tenant_id = (SELECT app_tenant()) AND company_id = ANY ((SELECT app_company_ids())::uuid[]));
CREATE POLICY rls_growth_source_record__insert ON growth_source_record FOR INSERT WITH CHECK (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company()));
CREATE POLICY rls_growth_source_record__update ON growth_source_record FOR UPDATE USING (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company())) WITH CHECK (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company()));
ALTER TABLE growth_evidence ENABLE ROW LEVEL SECURITY; ALTER TABLE growth_evidence FORCE ROW LEVEL SECURITY;
CREATE POLICY rls_growth_evidence__select ON growth_evidence FOR SELECT USING (tenant_id = (SELECT app_tenant()) AND company_id = ANY ((SELECT app_company_ids())::uuid[]));
CREATE POLICY rls_growth_evidence__insert ON growth_evidence FOR INSERT WITH CHECK (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company()));
CREATE POLICY rls_growth_evidence__update ON growth_evidence FOR UPDATE USING (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company())) WITH CHECK (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company()));
ALTER TABLE growth_competitor ENABLE ROW LEVEL SECURITY; ALTER TABLE growth_competitor FORCE ROW LEVEL SECURITY;
CREATE POLICY rls_growth_competitor__select ON growth_competitor FOR SELECT USING (tenant_id = (SELECT app_tenant()) AND company_id = ANY ((SELECT app_company_ids())::uuid[]));
CREATE POLICY rls_growth_competitor__insert ON growth_competitor FOR INSERT WITH CHECK (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company()));
CREATE POLICY rls_growth_competitor__update ON growth_competitor FOR UPDATE USING (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company())) WITH CHECK (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company()));
ALTER TABLE growth_market_event ENABLE ROW LEVEL SECURITY; ALTER TABLE growth_market_event FORCE ROW LEVEL SECURITY;
CREATE POLICY rls_growth_market_event__select ON growth_market_event FOR SELECT USING (tenant_id = (SELECT app_tenant()) AND company_id = ANY ((SELECT app_company_ids())::uuid[]));
CREATE POLICY rls_growth_market_event__insert ON growth_market_event FOR INSERT WITH CHECK (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company()));
CREATE POLICY rls_growth_market_event__update ON growth_market_event FOR UPDATE USING (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company())) WITH CHECK (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company()));
ALTER TABLE growth_search_plan ENABLE ROW LEVEL SECURITY; ALTER TABLE growth_search_plan FORCE ROW LEVEL SECURITY;
CREATE POLICY rls_growth_search_plan__select ON growth_search_plan FOR SELECT USING (tenant_id = (SELECT app_tenant()) AND company_id = ANY ((SELECT app_company_ids())::uuid[]));
CREATE POLICY rls_growth_search_plan__insert ON growth_search_plan FOR INSERT WITH CHECK (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company()));
CREATE POLICY rls_growth_search_plan__update ON growth_search_plan FOR UPDATE USING (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company())) WITH CHECK (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company()));
ALTER TABLE growth_organization ENABLE ROW LEVEL SECURITY; ALTER TABLE growth_organization FORCE ROW LEVEL SECURITY;
CREATE POLICY rls_growth_organization__select ON growth_organization FOR SELECT USING (tenant_id = (SELECT app_tenant()) AND company_id = ANY ((SELECT app_company_ids())::uuid[]));
CREATE POLICY rls_growth_organization__insert ON growth_organization FOR INSERT WITH CHECK (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company()));
CREATE POLICY rls_growth_organization__update ON growth_organization FOR UPDATE USING (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company())) WITH CHECK (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company()));
ALTER TABLE growth_signal ENABLE ROW LEVEL SECURITY; ALTER TABLE growth_signal FORCE ROW LEVEL SECURITY;
CREATE POLICY rls_growth_signal__select ON growth_signal FOR SELECT USING (tenant_id = (SELECT app_tenant()) AND company_id = ANY ((SELECT app_company_ids())::uuid[]));
CREATE POLICY rls_growth_signal__insert ON growth_signal FOR INSERT WITH CHECK (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company()));
CREATE POLICY rls_growth_signal__update ON growth_signal FOR UPDATE USING (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company())) WITH CHECK (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company()));
ALTER TABLE growth_signal_type ENABLE ROW LEVEL SECURITY; ALTER TABLE growth_signal_type FORCE ROW LEVEL SECURITY;
CREATE POLICY rls_growth_signal_type__select ON growth_signal_type FOR SELECT USING (tenant_id = (SELECT app_tenant()) AND company_id = ANY ((SELECT app_company_ids())::uuid[]));
CREATE POLICY rls_growth_signal_type__insert ON growth_signal_type FOR INSERT WITH CHECK (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company()));
CREATE POLICY rls_growth_signal_type__update ON growth_signal_type FOR UPDATE USING (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company())) WITH CHECK (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company()));
ALTER TABLE growth_need_evidence ENABLE ROW LEVEL SECURITY; ALTER TABLE growth_need_evidence FORCE ROW LEVEL SECURITY;
CREATE POLICY rls_growth_need_evidence__select ON growth_need_evidence FOR SELECT USING (tenant_id = (SELECT app_tenant()) AND company_id = ANY ((SELECT app_company_ids())::uuid[]));
CREATE POLICY rls_growth_need_evidence__insert ON growth_need_evidence FOR INSERT WITH CHECK (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company()));
CREATE POLICY rls_growth_need_evidence__update ON growth_need_evidence FOR UPDATE USING (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company())) WITH CHECK (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company()));
ALTER TABLE growth_referral ENABLE ROW LEVEL SECURITY; ALTER TABLE growth_referral FORCE ROW LEVEL SECURITY;
CREATE POLICY rls_growth_referral__select ON growth_referral FOR SELECT USING (tenant_id = (SELECT app_tenant()) AND company_id = ANY ((SELECT app_company_ids())::uuid[]));
CREATE POLICY rls_growth_referral__insert ON growth_referral FOR INSERT WITH CHECK (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company()));
CREATE POLICY rls_growth_referral__update ON growth_referral FOR UPDATE USING (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company())) WITH CHECK (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company()));
ALTER TABLE growth_contact ENABLE ROW LEVEL SECURITY; ALTER TABLE growth_contact FORCE ROW LEVEL SECURITY;
CREATE POLICY rls_growth_contact__select ON growth_contact FOR SELECT USING (tenant_id = (SELECT app_tenant()) AND company_id = ANY ((SELECT app_company_ids())::uuid[]));
CREATE POLICY rls_growth_contact__insert ON growth_contact FOR INSERT WITH CHECK (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company()));
CREATE POLICY rls_growth_contact__update ON growth_contact FOR UPDATE USING (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company())) WITH CHECK (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company()));
ALTER TABLE growth_contact_source ENABLE ROW LEVEL SECURITY; ALTER TABLE growth_contact_source FORCE ROW LEVEL SECURITY;
CREATE POLICY rls_growth_contact_source__select ON growth_contact_source FOR SELECT USING (tenant_id = (SELECT app_tenant()) AND company_id = ANY ((SELECT app_company_ids())::uuid[]));
CREATE POLICY rls_growth_contact_source__insert ON growth_contact_source FOR INSERT WITH CHECK (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company()));
CREATE POLICY rls_growth_contact_source__update ON growth_contact_source FOR UPDATE USING (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company())) WITH CHECK (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company()));
ALTER TABLE growth_contact_verification ENABLE ROW LEVEL SECURITY; ALTER TABLE growth_contact_verification FORCE ROW LEVEL SECURITY;
CREATE POLICY rls_growth_contact_verification__select ON growth_contact_verification FOR SELECT USING (tenant_id = (SELECT app_tenant()) AND company_id = ANY ((SELECT app_company_ids())::uuid[]));
CREATE POLICY rls_growth_contact_verification__insert ON growth_contact_verification FOR INSERT WITH CHECK (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company()));
CREATE POLICY rls_growth_contact_verification__update ON growth_contact_verification FOR UPDATE USING (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company())) WITH CHECK (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company()));
ALTER TABLE growth_consent ENABLE ROW LEVEL SECURITY; ALTER TABLE growth_consent FORCE ROW LEVEL SECURITY;
CREATE POLICY rls_growth_consent__select ON growth_consent FOR SELECT USING (tenant_id = (SELECT app_tenant()) AND company_id = ANY ((SELECT app_company_ids())::uuid[]));
CREATE POLICY rls_growth_consent__insert ON growth_consent FOR INSERT WITH CHECK (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company()));
CREATE POLICY rls_growth_consent__update ON growth_consent FOR UPDATE USING (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company())) WITH CHECK (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company()));
ALTER TABLE growth_suppression ENABLE ROW LEVEL SECURITY; ALTER TABLE growth_suppression FORCE ROW LEVEL SECURITY;
CREATE POLICY rls_growth_suppression__select ON growth_suppression FOR SELECT USING (tenant_id = (SELECT app_tenant()) AND company_id = ANY ((SELECT app_company_ids())::uuid[]));
CREATE POLICY rls_growth_suppression__insert ON growth_suppression FOR INSERT WITH CHECK (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company()));
CREATE POLICY rls_growth_suppression__update ON growth_suppression FOR UPDATE USING (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company())) WITH CHECK (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company()));
ALTER TABLE growth_need ENABLE ROW LEVEL SECURITY; ALTER TABLE growth_need FORCE ROW LEVEL SECURITY;
CREATE POLICY rls_growth_need__select ON growth_need FOR SELECT USING (tenant_id = (SELECT app_tenant()) AND company_id = ANY ((SELECT app_company_ids())::uuid[]));
CREATE POLICY rls_growth_need__insert ON growth_need FOR INSERT WITH CHECK (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company()));
CREATE POLICY rls_growth_need__update ON growth_need FOR UPDATE USING (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company())) WITH CHECK (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company()));
ALTER TABLE growth_product ENABLE ROW LEVEL SECURITY; ALTER TABLE growth_product FORCE ROW LEVEL SECURITY;
CREATE POLICY rls_growth_product__select ON growth_product FOR SELECT USING (tenant_id = (SELECT app_tenant()) AND company_id = ANY ((SELECT app_company_ids())::uuid[]));
CREATE POLICY rls_growth_product__insert ON growth_product FOR INSERT WITH CHECK (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company()));
CREATE POLICY rls_growth_product__update ON growth_product FOR UPDATE USING (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company())) WITH CHECK (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company()));
ALTER TABLE growth_opportunity ENABLE ROW LEVEL SECURITY; ALTER TABLE growth_opportunity FORCE ROW LEVEL SECURITY;
CREATE POLICY rls_growth_opportunity__select ON growth_opportunity FOR SELECT USING (tenant_id = (SELECT app_tenant()) AND company_id = ANY ((SELECT app_company_ids())::uuid[]));
CREATE POLICY rls_growth_opportunity__insert ON growth_opportunity FOR INSERT WITH CHECK (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company()));
CREATE POLICY rls_growth_opportunity__update ON growth_opportunity FOR UPDATE USING (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company())) WITH CHECK (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company()));
ALTER TABLE growth_score_version ENABLE ROW LEVEL SECURITY; ALTER TABLE growth_score_version FORCE ROW LEVEL SECURITY;
CREATE POLICY rls_growth_score_version__select ON growth_score_version FOR SELECT USING (tenant_id = (SELECT app_tenant()) AND company_id = ANY ((SELECT app_company_ids())::uuid[]));
CREATE POLICY rls_growth_score_version__insert ON growth_score_version FOR INSERT WITH CHECK (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company()));
CREATE POLICY rls_growth_score_version__update ON growth_score_version FOR UPDATE USING (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company())) WITH CHECK (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company()));
ALTER TABLE growth_activity ENABLE ROW LEVEL SECURITY; ALTER TABLE growth_activity FORCE ROW LEVEL SECURITY;
CREATE POLICY rls_growth_activity__select ON growth_activity FOR SELECT USING (tenant_id = (SELECT app_tenant()) AND company_id = ANY ((SELECT app_company_ids())::uuid[]));
CREATE POLICY rls_growth_activity__insert ON growth_activity FOR INSERT WITH CHECK (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company()));
CREATE POLICY rls_growth_activity__update ON growth_activity FOR UPDATE USING (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company())) WITH CHECK (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company()));
ALTER TABLE growth_deal ENABLE ROW LEVEL SECURITY; ALTER TABLE growth_deal FORCE ROW LEVEL SECURITY;
CREATE POLICY rls_growth_deal__select ON growth_deal FOR SELECT USING (tenant_id = (SELECT app_tenant()) AND company_id = ANY ((SELECT app_company_ids())::uuid[]));
CREATE POLICY rls_growth_deal__insert ON growth_deal FOR INSERT WITH CHECK (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company()));
CREATE POLICY rls_growth_deal__update ON growth_deal FOR UPDATE USING (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company())) WITH CHECK (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company()));
ALTER TABLE growth_stage ENABLE ROW LEVEL SECURITY; ALTER TABLE growth_stage FORCE ROW LEVEL SECURITY;
CREATE POLICY rls_growth_stage__select ON growth_stage FOR SELECT USING (tenant_id = (SELECT app_tenant()) AND company_id = ANY ((SELECT app_company_ids())::uuid[]));
CREATE POLICY rls_growth_stage__insert ON growth_stage FOR INSERT WITH CHECK (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company()));
CREATE POLICY rls_growth_stage__update ON growth_stage FOR UPDATE USING (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company())) WITH CHECK (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company()));
ALTER TABLE growth_task ENABLE ROW LEVEL SECURITY; ALTER TABLE growth_task FORCE ROW LEVEL SECURITY;
CREATE POLICY rls_growth_task__select ON growth_task FOR SELECT USING (tenant_id = (SELECT app_tenant()) AND company_id = ANY ((SELECT app_company_ids())::uuid[]));
CREATE POLICY rls_growth_task__insert ON growth_task FOR INSERT WITH CHECK (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company()));
CREATE POLICY rls_growth_task__update ON growth_task FOR UPDATE USING (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company())) WITH CHECK (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company()));
ALTER TABLE growth_budget ENABLE ROW LEVEL SECURITY; ALTER TABLE growth_budget FORCE ROW LEVEL SECURITY;
CREATE POLICY rls_growth_budget__select ON growth_budget FOR SELECT USING (tenant_id = (SELECT app_tenant()) AND company_id = ANY ((SELECT app_company_ids())::uuid[]));
CREATE POLICY rls_growth_budget__insert ON growth_budget FOR INSERT WITH CHECK (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company()));
CREATE POLICY rls_growth_budget__update ON growth_budget FOR UPDATE USING (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company())) WITH CHECK (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company()));
ALTER TABLE growth_message ENABLE ROW LEVEL SECURITY; ALTER TABLE growth_message FORCE ROW LEVEL SECURITY;
CREATE POLICY rls_growth_message__select ON growth_message FOR SELECT USING (tenant_id = (SELECT app_tenant()) AND company_id = ANY ((SELECT app_company_ids())::uuid[]));
CREATE POLICY rls_growth_message__insert ON growth_message FOR INSERT WITH CHECK (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company()));
CREATE POLICY rls_growth_message__update ON growth_message FOR UPDATE USING (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company())) WITH CHECK (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company()));
ALTER TABLE growth_message_draft ENABLE ROW LEVEL SECURITY; ALTER TABLE growth_message_draft FORCE ROW LEVEL SECURITY;
CREATE POLICY rls_growth_message_draft__select ON growth_message_draft FOR SELECT USING (tenant_id = (SELECT app_tenant()) AND company_id = ANY ((SELECT app_company_ids())::uuid[]));
CREATE POLICY rls_growth_message_draft__insert ON growth_message_draft FOR INSERT WITH CHECK (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company()));
CREATE POLICY rls_growth_message_draft__update ON growth_message_draft FOR UPDATE USING (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company())) WITH CHECK (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company()));
ALTER TABLE growth_message_template ENABLE ROW LEVEL SECURITY; ALTER TABLE growth_message_template FORCE ROW LEVEL SECURITY;
CREATE POLICY rls_growth_message_template__select ON growth_message_template FOR SELECT USING (tenant_id = (SELECT app_tenant()) AND company_id = ANY ((SELECT app_company_ids())::uuid[]));
CREATE POLICY rls_growth_message_template__insert ON growth_message_template FOR INSERT WITH CHECK (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company()));
CREATE POLICY rls_growth_message_template__update ON growth_message_template FOR UPDATE USING (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company())) WITH CHECK (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company()));
ALTER TABLE growth_outbox ENABLE ROW LEVEL SECURITY; ALTER TABLE growth_outbox FORCE ROW LEVEL SECURITY;
CREATE POLICY rls_growth_outbox__select ON growth_outbox FOR SELECT USING (tenant_id = (SELECT app_tenant()) AND company_id = ANY ((SELECT app_company_ids())::uuid[]));
CREATE POLICY rls_growth_outbox__insert ON growth_outbox FOR INSERT WITH CHECK (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company()));
CREATE POLICY rls_growth_outbox__update ON growth_outbox FOR UPDATE USING (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company())) WITH CHECK (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company()));
ALTER TABLE growth_delivery_event ENABLE ROW LEVEL SECURITY; ALTER TABLE growth_delivery_event FORCE ROW LEVEL SECURITY;
CREATE POLICY rls_growth_delivery_event__select ON growth_delivery_event FOR SELECT USING (tenant_id = (SELECT app_tenant()) AND company_id = ANY ((SELECT app_company_ids())::uuid[]));
CREATE POLICY rls_growth_delivery_event__insert ON growth_delivery_event FOR INSERT WITH CHECK (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company()));
CREATE POLICY rls_growth_delivery_event__update ON growth_delivery_event FOR UPDATE USING (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company())) WITH CHECK (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company()));
ALTER TABLE growth_thread ENABLE ROW LEVEL SECURITY; ALTER TABLE growth_thread FORCE ROW LEVEL SECURITY;
CREATE POLICY rls_growth_thread__select ON growth_thread FOR SELECT USING (tenant_id = (SELECT app_tenant()) AND company_id = ANY ((SELECT app_company_ids())::uuid[]));
CREATE POLICY rls_growth_thread__insert ON growth_thread FOR INSERT WITH CHECK (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company()));
CREATE POLICY rls_growth_thread__update ON growth_thread FOR UPDATE USING (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company())) WITH CHECK (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company()));
ALTER TABLE growth_channel_account ENABLE ROW LEVEL SECURITY; ALTER TABLE growth_channel_account FORCE ROW LEVEL SECURITY;
CREATE POLICY rls_growth_channel_account__select ON growth_channel_account FOR SELECT USING (tenant_id = (SELECT app_tenant()) AND company_id = ANY ((SELECT app_company_ids())::uuid[]));
CREATE POLICY rls_growth_channel_account__insert ON growth_channel_account FOR INSERT WITH CHECK (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company()));
CREATE POLICY rls_growth_channel_account__update ON growth_channel_account FOR UPDATE USING (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company())) WITH CHECK (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company()));
ALTER TABLE growth_inbound_event ENABLE ROW LEVEL SECURITY; ALTER TABLE growth_inbound_event FORCE ROW LEVEL SECURITY;
CREATE POLICY rls_growth_inbound_event__select ON growth_inbound_event FOR SELECT USING (tenant_id = (SELECT app_tenant()) AND company_id = ANY ((SELECT app_company_ids())::uuid[]));
CREATE POLICY rls_growth_inbound_event__insert ON growth_inbound_event FOR INSERT WITH CHECK (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company()));
CREATE POLICY rls_growth_inbound_event__update ON growth_inbound_event FOR UPDATE USING (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company())) WITH CHECK (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company()));
ALTER TABLE growth_enrollment ENABLE ROW LEVEL SECURITY; ALTER TABLE growth_enrollment FORCE ROW LEVEL SECURITY;
CREATE POLICY rls_growth_enrollment__select ON growth_enrollment FOR SELECT USING (tenant_id = (SELECT app_tenant()) AND company_id = ANY ((SELECT app_company_ids())::uuid[]));
CREATE POLICY rls_growth_enrollment__insert ON growth_enrollment FOR INSERT WITH CHECK (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company()));
CREATE POLICY rls_growth_enrollment__update ON growth_enrollment FOR UPDATE USING (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company())) WITH CHECK (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company()));
ALTER TABLE growth_sequence ENABLE ROW LEVEL SECURITY; ALTER TABLE growth_sequence FORCE ROW LEVEL SECURITY;
CREATE POLICY rls_growth_sequence__select ON growth_sequence FOR SELECT USING (tenant_id = (SELECT app_tenant()) AND company_id = ANY ((SELECT app_company_ids())::uuid[]));
CREATE POLICY rls_growth_sequence__insert ON growth_sequence FOR INSERT WITH CHECK (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company()));
CREATE POLICY rls_growth_sequence__update ON growth_sequence FOR UPDATE USING (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company())) WITH CHECK (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company()));
ALTER TABLE growth_sequence_step ENABLE ROW LEVEL SECURITY; ALTER TABLE growth_sequence_step FORCE ROW LEVEL SECURITY;
CREATE POLICY rls_growth_sequence_step__select ON growth_sequence_step FOR SELECT USING (tenant_id = (SELECT app_tenant()) AND company_id = ANY ((SELECT app_company_ids())::uuid[]));
CREATE POLICY rls_growth_sequence_step__insert ON growth_sequence_step FOR INSERT WITH CHECK (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company()));
CREATE POLICY rls_growth_sequence_step__update ON growth_sequence_step FOR UPDATE USING (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company())) WITH CHECK (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company()));
ALTER TABLE growth_routing_rule ENABLE ROW LEVEL SECURITY; ALTER TABLE growth_routing_rule FORCE ROW LEVEL SECURITY;
CREATE POLICY rls_growth_routing_rule__select ON growth_routing_rule FOR SELECT USING (tenant_id = (SELECT app_tenant()) AND company_id = ANY ((SELECT app_company_ids())::uuid[]));
CREATE POLICY rls_growth_routing_rule__insert ON growth_routing_rule FOR INSERT WITH CHECK (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company()));
CREATE POLICY rls_growth_routing_rule__update ON growth_routing_rule FOR UPDATE USING (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company())) WITH CHECK (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company()));
ALTER TABLE growth_workflow_execution ENABLE ROW LEVEL SECURITY; ALTER TABLE growth_workflow_execution FORCE ROW LEVEL SECURITY;
CREATE POLICY rls_growth_workflow_execution__select ON growth_workflow_execution FOR SELECT USING (tenant_id = (SELECT app_tenant()) AND company_id = ANY ((SELECT app_company_ids())::uuid[]));
CREATE POLICY rls_growth_workflow_execution__insert ON growth_workflow_execution FOR INSERT WITH CHECK (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company()));
CREATE POLICY rls_growth_workflow_execution__update ON growth_workflow_execution FOR UPDATE USING (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company())) WITH CHECK (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company()));
ALTER TABLE growth_identity_link ENABLE ROW LEVEL SECURITY; ALTER TABLE growth_identity_link FORCE ROW LEVEL SECURITY;
CREATE POLICY rls_growth_identity_link__select ON growth_identity_link FOR SELECT USING (tenant_id = (SELECT app_tenant()) AND company_id = ANY ((SELECT app_company_ids())::uuid[]));
CREATE POLICY rls_growth_identity_link__insert ON growth_identity_link FOR INSERT WITH CHECK (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company()));
CREATE POLICY rls_growth_identity_link__update ON growth_identity_link FOR UPDATE USING (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company())) WITH CHECK (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company()));
ALTER TABLE growth_objection ENABLE ROW LEVEL SECURITY; ALTER TABLE growth_objection FORCE ROW LEVEL SECURITY;
CREATE POLICY rls_growth_objection__select ON growth_objection FOR SELECT USING (tenant_id = (SELECT app_tenant()) AND company_id = ANY ((SELECT app_company_ids())::uuid[]));
CREATE POLICY rls_growth_objection__insert ON growth_objection FOR INSERT WITH CHECK (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company()));
CREATE POLICY rls_growth_objection__update ON growth_objection FOR UPDATE USING (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company())) WITH CHECK (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company()));
ALTER TABLE growth_calendar_link ENABLE ROW LEVEL SECURITY; ALTER TABLE growth_calendar_link FORCE ROW LEVEL SECURITY;
CREATE POLICY rls_growth_calendar_link__select ON growth_calendar_link FOR SELECT USING (tenant_id = (SELECT app_tenant()) AND company_id = ANY ((SELECT app_company_ids())::uuid[]));
CREATE POLICY rls_growth_calendar_link__insert ON growth_calendar_link FOR INSERT WITH CHECK (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company()));
CREATE POLICY rls_growth_calendar_link__update ON growth_calendar_link FOR UPDATE USING (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company())) WITH CHECK (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company()));
ALTER TABLE growth_meeting ENABLE ROW LEVEL SECURITY; ALTER TABLE growth_meeting FORCE ROW LEVEL SECURITY;
CREATE POLICY rls_growth_meeting__select ON growth_meeting FOR SELECT USING (tenant_id = (SELECT app_tenant()) AND company_id = ANY ((SELECT app_company_ids())::uuid[]));
CREATE POLICY rls_growth_meeting__insert ON growth_meeting FOR INSERT WITH CHECK (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company()));
CREATE POLICY rls_growth_meeting__update ON growth_meeting FOR UPDATE USING (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company())) WITH CHECK (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company()));
ALTER TABLE growth_business_event ENABLE ROW LEVEL SECURITY; ALTER TABLE growth_business_event FORCE ROW LEVEL SECURITY;
CREATE POLICY rls_growth_business_event__select ON growth_business_event FOR SELECT USING (tenant_id = (SELECT app_tenant()) AND company_id = ANY ((SELECT app_company_ids())::uuid[]));
CREATE POLICY rls_growth_business_event__insert ON growth_business_event FOR INSERT WITH CHECK (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company()));
CREATE POLICY rls_growth_business_event__update ON growth_business_event FOR UPDATE USING (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company())) WITH CHECK (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company()));
ALTER TABLE growth_event_attendance ENABLE ROW LEVEL SECURITY; ALTER TABLE growth_event_attendance FORCE ROW LEVEL SECURITY;
CREATE POLICY rls_growth_event_attendance__select ON growth_event_attendance FOR SELECT USING (tenant_id = (SELECT app_tenant()) AND company_id = ANY ((SELECT app_company_ids())::uuid[]));
CREATE POLICY rls_growth_event_attendance__insert ON growth_event_attendance FOR INSERT WITH CHECK (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company()));
CREATE POLICY rls_growth_event_attendance__update ON growth_event_attendance FOR UPDATE USING (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company())) WITH CHECK (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company()));
ALTER TABLE growth_event_registration ENABLE ROW LEVEL SECURITY; ALTER TABLE growth_event_registration FORCE ROW LEVEL SECURITY;
CREATE POLICY rls_growth_event_registration__select ON growth_event_registration FOR SELECT USING (tenant_id = (SELECT app_tenant()) AND company_id = ANY ((SELECT app_company_ids())::uuid[]));
CREATE POLICY rls_growth_event_registration__insert ON growth_event_registration FOR INSERT WITH CHECK (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company()));
CREATE POLICY rls_growth_event_registration__update ON growth_event_registration FOR UPDATE USING (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company())) WITH CHECK (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company()));
ALTER TABLE growth_claim ENABLE ROW LEVEL SECURITY; ALTER TABLE growth_claim FORCE ROW LEVEL SECURITY;
CREATE POLICY rls_growth_claim__select ON growth_claim FOR SELECT USING (tenant_id = (SELECT app_tenant()) AND company_id = ANY ((SELECT app_company_ids())::uuid[]));
CREATE POLICY rls_growth_claim__insert ON growth_claim FOR INSERT WITH CHECK (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company()));
CREATE POLICY rls_growth_claim__update ON growth_claim FOR UPDATE USING (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company())) WITH CHECK (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company()));
ALTER TABLE growth_content_asset ENABLE ROW LEVEL SECURITY; ALTER TABLE growth_content_asset FORCE ROW LEVEL SECURITY;
CREATE POLICY rls_growth_content_asset__select ON growth_content_asset FOR SELECT USING (tenant_id = (SELECT app_tenant()) AND company_id = ANY ((SELECT app_company_ids())::uuid[]));
CREATE POLICY rls_growth_content_asset__insert ON growth_content_asset FOR INSERT WITH CHECK (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company()));
CREATE POLICY rls_growth_content_asset__update ON growth_content_asset FOR UPDATE USING (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company())) WITH CHECK (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company()));
ALTER TABLE growth_content_version ENABLE ROW LEVEL SECURITY; ALTER TABLE growth_content_version FORCE ROW LEVEL SECURITY;
CREATE POLICY rls_growth_content_version__select ON growth_content_version FOR SELECT USING (tenant_id = (SELECT app_tenant()) AND company_id = ANY ((SELECT app_company_ids())::uuid[]));
CREATE POLICY rls_growth_content_version__insert ON growth_content_version FOR INSERT WITH CHECK (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company()));
CREATE POLICY rls_growth_content_version__update ON growth_content_version FOR UPDATE USING (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company())) WITH CHECK (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company()));
ALTER TABLE growth_approval ENABLE ROW LEVEL SECURITY; ALTER TABLE growth_approval FORCE ROW LEVEL SECURITY;
CREATE POLICY rls_growth_approval__select ON growth_approval FOR SELECT USING (tenant_id = (SELECT app_tenant()) AND company_id = ANY ((SELECT app_company_ids())::uuid[]));
CREATE POLICY rls_growth_approval__insert ON growth_approval FOR INSERT WITH CHECK (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company()));
CREATE POLICY rls_growth_approval__update ON growth_approval FOR UPDATE USING (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company())) WITH CHECK (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company()));
ALTER TABLE growth_social_post ENABLE ROW LEVEL SECURITY; ALTER TABLE growth_social_post FORCE ROW LEVEL SECURITY;
CREATE POLICY rls_growth_social_post__select ON growth_social_post FOR SELECT USING (tenant_id = (SELECT app_tenant()) AND company_id = ANY ((SELECT app_company_ids())::uuid[]));
CREATE POLICY rls_growth_social_post__insert ON growth_social_post FOR INSERT WITH CHECK (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company()));
CREATE POLICY rls_growth_social_post__update ON growth_social_post FOR UPDATE USING (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company())) WITH CHECK (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company()));
ALTER TABLE growth_social_publication ENABLE ROW LEVEL SECURITY; ALTER TABLE growth_social_publication FORCE ROW LEVEL SECURITY;
CREATE POLICY rls_growth_social_publication__select ON growth_social_publication FOR SELECT USING (tenant_id = (SELECT app_tenant()) AND company_id = ANY ((SELECT app_company_ids())::uuid[]));
CREATE POLICY rls_growth_social_publication__insert ON growth_social_publication FOR INSERT WITH CHECK (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company()));
CREATE POLICY rls_growth_social_publication__update ON growth_social_publication FOR UPDATE USING (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company())) WITH CHECK (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company()));
ALTER TABLE growth_keyword ENABLE ROW LEVEL SECURITY; ALTER TABLE growth_keyword FORCE ROW LEVEL SECURITY;
CREATE POLICY rls_growth_keyword__select ON growth_keyword FOR SELECT USING (tenant_id = (SELECT app_tenant()) AND company_id = ANY ((SELECT app_company_ids())::uuid[]));
CREATE POLICY rls_growth_keyword__insert ON growth_keyword FOR INSERT WITH CHECK (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company()));
CREATE POLICY rls_growth_keyword__update ON growth_keyword FOR UPDATE USING (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company())) WITH CHECK (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company()));
ALTER TABLE growth_page_metric ENABLE ROW LEVEL SECURITY; ALTER TABLE growth_page_metric FORCE ROW LEVEL SECURITY;
CREATE POLICY rls_growth_page_metric__select ON growth_page_metric FOR SELECT USING (tenant_id = (SELECT app_tenant()) AND company_id = ANY ((SELECT app_company_ids())::uuid[]));
CREATE POLICY rls_growth_page_metric__insert ON growth_page_metric FOR INSERT WITH CHECK (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company()));
CREATE POLICY rls_growth_page_metric__update ON growth_page_metric FOR UPDATE USING (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company())) WITH CHECK (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company()));
ALTER TABLE growth_seo_issue ENABLE ROW LEVEL SECURITY; ALTER TABLE growth_seo_issue FORCE ROW LEVEL SECURITY;
CREATE POLICY rls_growth_seo_issue__select ON growth_seo_issue FOR SELECT USING (tenant_id = (SELECT app_tenant()) AND company_id = ANY ((SELECT app_company_ids())::uuid[]));
CREATE POLICY rls_growth_seo_issue__insert ON growth_seo_issue FOR INSERT WITH CHECK (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company()));
CREATE POLICY rls_growth_seo_issue__update ON growth_seo_issue FOR UPDATE USING (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company())) WITH CHECK (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company()));
ALTER TABLE growth_landing_page ENABLE ROW LEVEL SECURITY; ALTER TABLE growth_landing_page FORCE ROW LEVEL SECURITY;
CREATE POLICY rls_growth_landing_page__select ON growth_landing_page FOR SELECT USING (tenant_id = (SELECT app_tenant()) AND company_id = ANY ((SELECT app_company_ids())::uuid[]));
CREATE POLICY rls_growth_landing_page__insert ON growth_landing_page FOR INSERT WITH CHECK (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company()));
CREATE POLICY rls_growth_landing_page__update ON growth_landing_page FOR UPDATE USING (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company())) WITH CHECK (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company()));
ALTER TABLE growth_audience ENABLE ROW LEVEL SECURITY; ALTER TABLE growth_audience FORCE ROW LEVEL SECURITY;
CREATE POLICY rls_growth_audience__select ON growth_audience FOR SELECT USING (tenant_id = (SELECT app_tenant()) AND company_id = ANY ((SELECT app_company_ids())::uuid[]));
CREATE POLICY rls_growth_audience__insert ON growth_audience FOR INSERT WITH CHECK (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company()));
CREATE POLICY rls_growth_audience__update ON growth_audience FOR UPDATE USING (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company())) WITH CHECK (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company()));
ALTER TABLE growth_campaign ENABLE ROW LEVEL SECURITY; ALTER TABLE growth_campaign FORCE ROW LEVEL SECURITY;
CREATE POLICY rls_growth_campaign__select ON growth_campaign FOR SELECT USING (tenant_id = (SELECT app_tenant()) AND company_id = ANY ((SELECT app_company_ids())::uuid[]));
CREATE POLICY rls_growth_campaign__insert ON growth_campaign FOR INSERT WITH CHECK (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company()));
CREATE POLICY rls_growth_campaign__update ON growth_campaign FOR UPDATE USING (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company())) WITH CHECK (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company()));
ALTER TABLE growth_campaign_version ENABLE ROW LEVEL SECURITY; ALTER TABLE growth_campaign_version FORCE ROW LEVEL SECURITY;
CREATE POLICY rls_growth_campaign_version__select ON growth_campaign_version FOR SELECT USING (tenant_id = (SELECT app_tenant()) AND company_id = ANY ((SELECT app_company_ids())::uuid[]));
CREATE POLICY rls_growth_campaign_version__insert ON growth_campaign_version FOR INSERT WITH CHECK (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company()));
CREATE POLICY rls_growth_campaign_version__update ON growth_campaign_version FOR UPDATE USING (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company())) WITH CHECK (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company()));
ALTER TABLE growth_ad_campaign ENABLE ROW LEVEL SECURITY; ALTER TABLE growth_ad_campaign FORCE ROW LEVEL SECURITY;
CREATE POLICY rls_growth_ad_campaign__select ON growth_ad_campaign FOR SELECT USING (tenant_id = (SELECT app_tenant()) AND company_id = ANY ((SELECT app_company_ids())::uuid[]));
CREATE POLICY rls_growth_ad_campaign__insert ON growth_ad_campaign FOR INSERT WITH CHECK (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company()));
CREATE POLICY rls_growth_ad_campaign__update ON growth_ad_campaign FOR UPDATE USING (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company())) WITH CHECK (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company()));
ALTER TABLE growth_ad_spend_event ENABLE ROW LEVEL SECURITY; ALTER TABLE growth_ad_spend_event FORCE ROW LEVEL SECURITY;
CREATE POLICY rls_growth_ad_spend_event__select ON growth_ad_spend_event FOR SELECT USING (tenant_id = (SELECT app_tenant()) AND company_id = ANY ((SELECT app_company_ids())::uuid[]));
CREATE POLICY rls_growth_ad_spend_event__insert ON growth_ad_spend_event FOR INSERT WITH CHECK (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company()));
CREATE POLICY rls_growth_ad_spend_event__update ON growth_ad_spend_event FOR UPDATE USING (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company())) WITH CHECK (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company()));
ALTER TABLE growth_attribution_event ENABLE ROW LEVEL SECURITY; ALTER TABLE growth_attribution_event FORCE ROW LEVEL SECURITY;
CREATE POLICY rls_growth_attribution_event__select ON growth_attribution_event FOR SELECT USING (tenant_id = (SELECT app_tenant()) AND company_id = ANY ((SELECT app_company_ids())::uuid[]));
CREATE POLICY rls_growth_attribution_event__insert ON growth_attribution_event FOR INSERT WITH CHECK (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company()));
CREATE POLICY rls_growth_attribution_event__update ON growth_attribution_event FOR UPDATE USING (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company())) WITH CHECK (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company()));
ALTER TABLE growth_form ENABLE ROW LEVEL SECURITY; ALTER TABLE growth_form FORCE ROW LEVEL SECURITY;
CREATE POLICY rls_growth_form__select ON growth_form FOR SELECT USING (tenant_id = (SELECT app_tenant()) AND company_id = ANY ((SELECT app_company_ids())::uuid[]));
CREATE POLICY rls_growth_form__insert ON growth_form FOR INSERT WITH CHECK (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company()));
CREATE POLICY rls_growth_form__update ON growth_form FOR UPDATE USING (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company())) WITH CHECK (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company()));
ALTER TABLE growth_lead ENABLE ROW LEVEL SECURITY; ALTER TABLE growth_lead FORCE ROW LEVEL SECURITY;
CREATE POLICY rls_growth_lead__select ON growth_lead FOR SELECT USING (tenant_id = (SELECT app_tenant()) AND company_id = ANY ((SELECT app_company_ids())::uuid[]));
CREATE POLICY rls_growth_lead__insert ON growth_lead FOR INSERT WITH CHECK (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company()));
CREATE POLICY rls_growth_lead__update ON growth_lead FOR UPDATE USING (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company())) WITH CHECK (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company()));
ALTER TABLE growth_proposal ENABLE ROW LEVEL SECURITY; ALTER TABLE growth_proposal FORCE ROW LEVEL SECURITY;
CREATE POLICY rls_growth_proposal__select ON growth_proposal FOR SELECT USING (tenant_id = (SELECT app_tenant()) AND company_id = ANY ((SELECT app_company_ids())::uuid[]));
CREATE POLICY rls_growth_proposal__insert ON growth_proposal FOR INSERT WITH CHECK (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company()));
CREATE POLICY rls_growth_proposal__update ON growth_proposal FOR UPDATE USING (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company())) WITH CHECK (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company()));
ALTER TABLE growth_proposal_version ENABLE ROW LEVEL SECURITY; ALTER TABLE growth_proposal_version FORCE ROW LEVEL SECURITY;
CREATE POLICY rls_growth_proposal_version__select ON growth_proposal_version FOR SELECT USING (tenant_id = (SELECT app_tenant()) AND company_id = ANY ((SELECT app_company_ids())::uuid[]));
CREATE POLICY rls_growth_proposal_version__insert ON growth_proposal_version FOR INSERT WITH CHECK (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company()));
CREATE POLICY rls_growth_proposal_version__update ON growth_proposal_version FOR UPDATE USING (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company())) WITH CHECK (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company()));
ALTER TABLE growth_quote ENABLE ROW LEVEL SECURITY; ALTER TABLE growth_quote FORCE ROW LEVEL SECURITY;
CREATE POLICY rls_growth_quote__select ON growth_quote FOR SELECT USING (tenant_id = (SELECT app_tenant()) AND company_id = ANY ((SELECT app_company_ids())::uuid[]));
CREATE POLICY rls_growth_quote__insert ON growth_quote FOR INSERT WITH CHECK (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company()));
CREATE POLICY rls_growth_quote__update ON growth_quote FOR UPDATE USING (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company())) WITH CHECK (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company()));
ALTER TABLE growth_quote_line ENABLE ROW LEVEL SECURITY; ALTER TABLE growth_quote_line FORCE ROW LEVEL SECURITY;
CREATE POLICY rls_growth_quote_line__select ON growth_quote_line FOR SELECT USING (tenant_id = (SELECT app_tenant()) AND company_id = ANY ((SELECT app_company_ids())::uuid[]));
CREATE POLICY rls_growth_quote_line__insert ON growth_quote_line FOR INSERT WITH CHECK (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company()));
CREATE POLICY rls_growth_quote_line__update ON growth_quote_line FOR UPDATE USING (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company())) WITH CHECK (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company()));
ALTER TABLE growth_negotiation ENABLE ROW LEVEL SECURITY; ALTER TABLE growth_negotiation FORCE ROW LEVEL SECURITY;
CREATE POLICY rls_growth_negotiation__select ON growth_negotiation FOR SELECT USING (tenant_id = (SELECT app_tenant()) AND company_id = ANY ((SELECT app_company_ids())::uuid[]));
CREATE POLICY rls_growth_negotiation__insert ON growth_negotiation FOR INSERT WITH CHECK (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company()));
CREATE POLICY rls_growth_negotiation__update ON growth_negotiation FOR UPDATE USING (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company())) WITH CHECK (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company()));
ALTER TABLE growth_contract ENABLE ROW LEVEL SECURITY; ALTER TABLE growth_contract FORCE ROW LEVEL SECURITY;
CREATE POLICY rls_growth_contract__select ON growth_contract FOR SELECT USING (tenant_id = (SELECT app_tenant()) AND company_id = ANY ((SELECT app_company_ids())::uuid[]));
CREATE POLICY rls_growth_contract__insert ON growth_contract FOR INSERT WITH CHECK (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company()));
CREATE POLICY rls_growth_contract__update ON growth_contract FOR UPDATE USING (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company())) WITH CHECK (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company()));
ALTER TABLE growth_integration_deal ENABLE ROW LEVEL SECURITY; ALTER TABLE growth_integration_deal FORCE ROW LEVEL SECURITY;
CREATE POLICY rls_growth_integration_deal__select ON growth_integration_deal FOR SELECT USING (tenant_id = (SELECT app_tenant()) AND company_id = ANY ((SELECT app_company_ids())::uuid[]));
CREATE POLICY rls_growth_integration_deal__insert ON growth_integration_deal FOR INSERT WITH CHECK (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company()));
CREATE POLICY rls_growth_integration_deal__update ON growth_integration_deal FOR UPDATE USING (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company())) WITH CHECK (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company()));
ALTER TABLE sales_bid ENABLE ROW LEVEL SECURITY; ALTER TABLE sales_bid FORCE ROW LEVEL SECURITY;
CREATE POLICY rls_sales_bid__select ON sales_bid FOR SELECT USING (tenant_id = (SELECT app_tenant()) AND company_id = ANY ((SELECT app_company_ids())::uuid[]));
CREATE POLICY rls_sales_bid__insert ON sales_bid FOR INSERT WITH CHECK (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company()));
CREATE POLICY rls_sales_bid__update ON sales_bid FOR UPDATE USING (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company())) WITH CHECK (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company()));
ALTER TABLE growth_invoice ENABLE ROW LEVEL SECURITY; ALTER TABLE growth_invoice FORCE ROW LEVEL SECURITY;
CREATE POLICY rls_growth_invoice__select ON growth_invoice FOR SELECT USING (tenant_id = (SELECT app_tenant()) AND company_id = ANY ((SELECT app_company_ids())::uuid[]));
CREATE POLICY rls_growth_invoice__insert ON growth_invoice FOR INSERT WITH CHECK (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company()));
CREATE POLICY rls_growth_invoice__update ON growth_invoice FOR UPDATE USING (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company())) WITH CHECK (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company()));
ALTER TABLE growth_payment ENABLE ROW LEVEL SECURITY; ALTER TABLE growth_payment FORCE ROW LEVEL SECURITY;
CREATE POLICY rls_growth_payment__select ON growth_payment FOR SELECT USING (tenant_id = (SELECT app_tenant()) AND company_id = ANY ((SELECT app_company_ids())::uuid[]));
CREATE POLICY rls_growth_payment__insert ON growth_payment FOR INSERT WITH CHECK (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company()));
CREATE POLICY rls_growth_payment__update ON growth_payment FOR UPDATE USING (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company())) WITH CHECK (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company()));
ALTER TABLE sales_fulfillment ENABLE ROW LEVEL SECURITY; ALTER TABLE sales_fulfillment FORCE ROW LEVEL SECURITY;
CREATE POLICY rls_sales_fulfillment__select ON sales_fulfillment FOR SELECT USING (tenant_id = (SELECT app_tenant()) AND company_id = ANY ((SELECT app_company_ids())::uuid[]));
CREATE POLICY rls_sales_fulfillment__insert ON sales_fulfillment FOR INSERT WITH CHECK (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company()));
CREATE POLICY rls_sales_fulfillment__update ON sales_fulfillment FOR UPDATE USING (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company())) WITH CHECK (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company()));
ALTER TABLE sales_order ENABLE ROW LEVEL SECURITY; ALTER TABLE sales_order FORCE ROW LEVEL SECURITY;
CREATE POLICY rls_sales_order__select ON sales_order FOR SELECT USING (tenant_id = (SELECT app_tenant()) AND company_id = ANY ((SELECT app_company_ids())::uuid[]));
CREATE POLICY rls_sales_order__insert ON sales_order FOR INSERT WITH CHECK (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company()));
CREATE POLICY rls_sales_order__update ON sales_order FOR UPDATE USING (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company())) WITH CHECK (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company()));
ALTER TABLE sales_order_line ENABLE ROW LEVEL SECURITY; ALTER TABLE sales_order_line FORCE ROW LEVEL SECURITY;
CREATE POLICY rls_sales_order_line__select ON sales_order_line FOR SELECT USING (tenant_id = (SELECT app_tenant()) AND company_id = ANY ((SELECT app_company_ids())::uuid[]));
CREATE POLICY rls_sales_order_line__insert ON sales_order_line FOR INSERT WITH CHECK (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company()));
CREATE POLICY rls_sales_order_line__update ON sales_order_line FOR UPDATE USING (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company())) WITH CHECK (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company()));
ALTER TABLE growth_onboarding ENABLE ROW LEVEL SECURITY; ALTER TABLE growth_onboarding FORCE ROW LEVEL SECURITY;
CREATE POLICY rls_growth_onboarding__select ON growth_onboarding FOR SELECT USING (tenant_id = (SELECT app_tenant()) AND company_id = ANY ((SELECT app_company_ids())::uuid[]));
CREATE POLICY rls_growth_onboarding__insert ON growth_onboarding FOR INSERT WITH CHECK (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company()));
CREATE POLICY rls_growth_onboarding__update ON growth_onboarding FOR UPDATE USING (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company())) WITH CHECK (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company()));
ALTER TABLE growth_deployment ENABLE ROW LEVEL SECURITY; ALTER TABLE growth_deployment FORCE ROW LEVEL SECURITY;
CREATE POLICY rls_growth_deployment__select ON growth_deployment FOR SELECT USING (tenant_id = (SELECT app_tenant()) AND company_id = ANY ((SELECT app_company_ids())::uuid[]));
CREATE POLICY rls_growth_deployment__insert ON growth_deployment FOR INSERT WITH CHECK (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company()));
CREATE POLICY rls_growth_deployment__update ON growth_deployment FOR UPDATE USING (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company())) WITH CHECK (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company()));
ALTER TABLE growth_partner ENABLE ROW LEVEL SECURITY; ALTER TABLE growth_partner FORCE ROW LEVEL SECURITY;
CREATE POLICY rls_growth_partner__select ON growth_partner FOR SELECT USING (tenant_id = (SELECT app_tenant()) AND company_id = ANY ((SELECT app_company_ids())::uuid[]));
CREATE POLICY rls_growth_partner__insert ON growth_partner FOR INSERT WITH CHECK (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company()));
CREATE POLICY rls_growth_partner__update ON growth_partner FOR UPDATE USING (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company())) WITH CHECK (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company()));
ALTER TABLE growth_pilot ENABLE ROW LEVEL SECURITY; ALTER TABLE growth_pilot FORCE ROW LEVEL SECURITY;
CREATE POLICY rls_growth_pilot__select ON growth_pilot FOR SELECT USING (tenant_id = (SELECT app_tenant()) AND company_id = ANY ((SELECT app_company_ids())::uuid[]));
CREATE POLICY rls_growth_pilot__insert ON growth_pilot FOR INSERT WITH CHECK (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company()));
CREATE POLICY rls_growth_pilot__update ON growth_pilot FOR UPDATE USING (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company())) WITH CHECK (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company()));
ALTER TABLE growth_renewal ENABLE ROW LEVEL SECURITY; ALTER TABLE growth_renewal FORCE ROW LEVEL SECURITY;
CREATE POLICY rls_growth_renewal__select ON growth_renewal FOR SELECT USING (tenant_id = (SELECT app_tenant()) AND company_id = ANY ((SELECT app_company_ids())::uuid[]));
CREATE POLICY rls_growth_renewal__insert ON growth_renewal FOR INSERT WITH CHECK (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company()));
CREATE POLICY rls_growth_renewal__update ON growth_renewal FOR UPDATE USING (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company())) WITH CHECK (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company()));
ALTER TABLE growth_feedback ENABLE ROW LEVEL SECURITY; ALTER TABLE growth_feedback FORCE ROW LEVEL SECURITY;
CREATE POLICY rls_growth_feedback__select ON growth_feedback FOR SELECT USING (tenant_id = (SELECT app_tenant()) AND company_id = ANY ((SELECT app_company_ids())::uuid[]));
CREATE POLICY rls_growth_feedback__insert ON growth_feedback FOR INSERT WITH CHECK (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company()));
CREATE POLICY rls_growth_feedback__update ON growth_feedback FOR UPDATE USING (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company())) WITH CHECK (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company()));
ALTER TABLE growth_metric_snapshot ENABLE ROW LEVEL SECURITY; ALTER TABLE growth_metric_snapshot FORCE ROW LEVEL SECURITY;
CREATE POLICY rls_growth_metric_snapshot__select ON growth_metric_snapshot FOR SELECT USING (tenant_id = (SELECT app_tenant()) AND company_id = ANY ((SELECT app_company_ids())::uuid[]));
CREATE POLICY rls_growth_metric_snapshot__insert ON growth_metric_snapshot FOR INSERT WITH CHECK (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company()));
CREATE POLICY rls_growth_metric_snapshot__update ON growth_metric_snapshot FOR UPDATE USING (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company())) WITH CHECK (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company()));
ALTER TABLE growth_forecast ENABLE ROW LEVEL SECURITY; ALTER TABLE growth_forecast FORCE ROW LEVEL SECURITY;
CREATE POLICY rls_growth_forecast__select ON growth_forecast FOR SELECT USING (tenant_id = (SELECT app_tenant()) AND company_id = ANY ((SELECT app_company_ids())::uuid[]));
CREATE POLICY rls_growth_forecast__insert ON growth_forecast FOR INSERT WITH CHECK (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company()));
CREATE POLICY rls_growth_forecast__update ON growth_forecast FOR UPDATE USING (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company())) WITH CHECK (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company()));
ALTER TABLE growth_stage_metric ENABLE ROW LEVEL SECURITY; ALTER TABLE growth_stage_metric FORCE ROW LEVEL SECURITY;
CREATE POLICY rls_growth_stage_metric__select ON growth_stage_metric FOR SELECT USING (tenant_id = (SELECT app_tenant()) AND company_id = ANY ((SELECT app_company_ids())::uuid[]));
CREATE POLICY rls_growth_stage_metric__insert ON growth_stage_metric FOR INSERT WITH CHECK (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company()));
CREATE POLICY rls_growth_stage_metric__update ON growth_stage_metric FOR UPDATE USING (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company())) WITH CHECK (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company()));
ALTER TABLE growth_document ENABLE ROW LEVEL SECURITY; ALTER TABLE growth_document FORCE ROW LEVEL SECURITY;
CREATE POLICY rls_growth_document__select ON growth_document FOR SELECT USING (tenant_id = (SELECT app_tenant()) AND company_id = ANY ((SELECT app_company_ids())::uuid[]));
CREATE POLICY rls_growth_document__insert ON growth_document FOR INSERT WITH CHECK (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company()));
CREATE POLICY rls_growth_document__update ON growth_document FOR UPDATE USING (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company())) WITH CHECK (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company()));
ALTER TABLE growth_document_chunk ENABLE ROW LEVEL SECURITY; ALTER TABLE growth_document_chunk FORCE ROW LEVEL SECURITY;
CREATE POLICY rls_growth_document_chunk__select ON growth_document_chunk FOR SELECT USING (tenant_id = (SELECT app_tenant()) AND company_id = ANY ((SELECT app_company_ids())::uuid[]));
CREATE POLICY rls_growth_document_chunk__insert ON growth_document_chunk FOR INSERT WITH CHECK (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company()));
CREATE POLICY rls_growth_document_chunk__update ON growth_document_chunk FOR UPDATE USING (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company())) WITH CHECK (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company()));
ALTER TABLE growth_embedding ENABLE ROW LEVEL SECURITY; ALTER TABLE growth_embedding FORCE ROW LEVEL SECURITY;
CREATE POLICY rls_growth_embedding__select ON growth_embedding FOR SELECT USING (tenant_id = (SELECT app_tenant()) AND company_id = ANY ((SELECT app_company_ids())::uuid[]));
CREATE POLICY rls_growth_embedding__insert ON growth_embedding FOR INSERT WITH CHECK (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company()));
CREATE POLICY rls_growth_embedding__update ON growth_embedding FOR UPDATE USING (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company())) WITH CHECK (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company()));
ALTER TABLE identity_provider ENABLE ROW LEVEL SECURITY; ALTER TABLE identity_provider FORCE ROW LEVEL SECURITY;
CREATE POLICY rls_identity_provider__select ON identity_provider FOR SELECT USING (tenant_id = (SELECT app_tenant()));
CREATE POLICY rls_identity_provider__insert ON identity_provider FOR INSERT WITH CHECK (tenant_id = (SELECT app_tenant()));
CREATE POLICY rls_identity_provider__update ON identity_provider FOR UPDATE USING (tenant_id = (SELECT app_tenant())) WITH CHECK (tenant_id = (SELECT app_tenant()));
ALTER TABLE scim_token ENABLE ROW LEVEL SECURITY; ALTER TABLE scim_token FORCE ROW LEVEL SECURITY;
CREATE POLICY rls_scim_token__select ON scim_token FOR SELECT USING (tenant_id = (SELECT app_tenant()));
CREATE POLICY rls_scim_token__insert ON scim_token FOR INSERT WITH CHECK (tenant_id = (SELECT app_tenant()));
CREATE POLICY rls_scim_token__update ON scim_token FOR UPDATE USING (tenant_id = (SELECT app_tenant())) WITH CHECK (tenant_id = (SELECT app_tenant()));
ALTER TABLE custom_role ENABLE ROW LEVEL SECURITY; ALTER TABLE custom_role FORCE ROW LEVEL SECURITY;
CREATE POLICY rls_custom_role__select ON custom_role FOR SELECT USING (tenant_id = (SELECT app_tenant()));
CREATE POLICY rls_custom_role__insert ON custom_role FOR INSERT WITH CHECK (tenant_id = (SELECT app_tenant()));
CREATE POLICY rls_custom_role__update ON custom_role FOR UPDATE USING (tenant_id = (SELECT app_tenant())) WITH CHECK (tenant_id = (SELECT app_tenant()));
ALTER TABLE role_permission ENABLE ROW LEVEL SECURITY; ALTER TABLE role_permission FORCE ROW LEVEL SECURITY;
CREATE POLICY rls_role_permission__select ON role_permission FOR SELECT USING (tenant_id = (SELECT app_tenant()));
CREATE POLICY rls_role_permission__insert ON role_permission FOR INSERT WITH CHECK (tenant_id = (SELECT app_tenant()));
CREATE POLICY rls_role_permission__update ON role_permission FOR UPDATE USING (tenant_id = (SELECT app_tenant())) WITH CHECK (tenant_id = (SELECT app_tenant()));
ALTER TABLE api_key ENABLE ROW LEVEL SECURITY; ALTER TABLE api_key FORCE ROW LEVEL SECURITY;
CREATE POLICY rls_api_key__select ON api_key FOR SELECT USING (tenant_id = (SELECT app_tenant()));
CREATE POLICY rls_api_key__insert ON api_key FOR INSERT WITH CHECK (tenant_id = (SELECT app_tenant()));
CREATE POLICY rls_api_key__update ON api_key FOR UPDATE USING (tenant_id = (SELECT app_tenant())) WITH CHECK (tenant_id = (SELECT app_tenant()));
ALTER TABLE webhook_endpoint ENABLE ROW LEVEL SECURITY; ALTER TABLE webhook_endpoint FORCE ROW LEVEL SECURITY;
CREATE POLICY rls_webhook_endpoint__select ON webhook_endpoint FOR SELECT USING (tenant_id = (SELECT app_tenant()));
CREATE POLICY rls_webhook_endpoint__insert ON webhook_endpoint FOR INSERT WITH CHECK (tenant_id = (SELECT app_tenant()));
CREATE POLICY rls_webhook_endpoint__update ON webhook_endpoint FOR UPDATE USING (tenant_id = (SELECT app_tenant())) WITH CHECK (tenant_id = (SELECT app_tenant()));
ALTER TABLE webhook_delivery ENABLE ROW LEVEL SECURITY; ALTER TABLE webhook_delivery FORCE ROW LEVEL SECURITY;
CREATE POLICY rls_webhook_delivery__select ON webhook_delivery FOR SELECT USING (tenant_id = (SELECT app_tenant()));
CREATE POLICY rls_webhook_delivery__insert ON webhook_delivery FOR INSERT WITH CHECK (tenant_id = (SELECT app_tenant()));
CREATE POLICY rls_webhook_delivery__update ON webhook_delivery FOR UPDATE USING (tenant_id = (SELECT app_tenant())) WITH CHECK (tenant_id = (SELECT app_tenant()));
ALTER TABLE audit_sink ENABLE ROW LEVEL SECURITY; ALTER TABLE audit_sink FORCE ROW LEVEL SECURITY;
CREATE POLICY rls_audit_sink__select ON audit_sink FOR SELECT USING (tenant_id = (SELECT app_tenant()));
CREATE POLICY rls_audit_sink__insert ON audit_sink FOR INSERT WITH CHECK (tenant_id = (SELECT app_tenant()));
CREATE POLICY rls_audit_sink__update ON audit_sink FOR UPDATE USING (tenant_id = (SELECT app_tenant())) WITH CHECK (tenant_id = (SELECT app_tenant()));
ALTER TABLE export_job ENABLE ROW LEVEL SECURITY; ALTER TABLE export_job FORCE ROW LEVEL SECURITY;
CREATE POLICY rls_export_job__select ON export_job FOR SELECT USING (tenant_id = (SELECT app_tenant()));
CREATE POLICY rls_export_job__insert ON export_job FOR INSERT WITH CHECK (tenant_id = (SELECT app_tenant()));
CREATE POLICY rls_export_job__update ON export_job FOR UPDATE USING (tenant_id = (SELECT app_tenant())) WITH CHECK (tenant_id = (SELECT app_tenant()));
ALTER TABLE tenant_key_config ENABLE ROW LEVEL SECURITY; ALTER TABLE tenant_key_config FORCE ROW LEVEL SECURITY;
CREATE POLICY rls_tenant_key_config__select ON tenant_key_config FOR SELECT USING (tenant_id = (SELECT app_tenant()));
CREATE POLICY rls_tenant_key_config__insert ON tenant_key_config FOR INSERT WITH CHECK (tenant_id = (SELECT app_tenant()));
CREATE POLICY rls_tenant_key_config__update ON tenant_key_config FOR UPDATE USING (tenant_id = (SELECT app_tenant())) WITH CHECK (tenant_id = (SELECT app_tenant()));
ALTER TABLE sandbox_environment ENABLE ROW LEVEL SECURITY; ALTER TABLE sandbox_environment FORCE ROW LEVEL SECURITY;
CREATE POLICY rls_sandbox_environment__select ON sandbox_environment FOR SELECT USING (tenant_id = (SELECT app_tenant()));
CREATE POLICY rls_sandbox_environment__insert ON sandbox_environment FOR INSERT WITH CHECK (tenant_id = (SELECT app_tenant()));
CREATE POLICY rls_sandbox_environment__update ON sandbox_environment FOR UPDATE USING (tenant_id = (SELECT app_tenant())) WITH CHECK (tenant_id = (SELECT app_tenant()));
ALTER TABLE config_promotion ENABLE ROW LEVEL SECURITY; ALTER TABLE config_promotion FORCE ROW LEVEL SECURITY;
CREATE POLICY rls_config_promotion__select ON config_promotion FOR SELECT USING (tenant_id = (SELECT app_tenant()));
CREATE POLICY rls_config_promotion__insert ON config_promotion FOR INSERT WITH CHECK (tenant_id = (SELECT app_tenant()));
CREATE POLICY rls_config_promotion__update ON config_promotion FOR UPDATE USING (tenant_id = (SELECT app_tenant())) WITH CHECK (tenant_id = (SELECT app_tenant()));
ALTER TABLE connector_installation ENABLE ROW LEVEL SECURITY; ALTER TABLE connector_installation FORCE ROW LEVEL SECURITY;
CREATE POLICY rls_connector_installation__select ON connector_installation FOR SELECT USING (tenant_id = (SELECT app_tenant()));
CREATE POLICY rls_connector_installation__insert ON connector_installation FOR INSERT WITH CHECK (tenant_id = (SELECT app_tenant()));
CREATE POLICY rls_connector_installation__update ON connector_installation FOR UPDATE USING (tenant_id = (SELECT app_tenant())) WITH CHECK (tenant_id = (SELECT app_tenant()));
ALTER TABLE invoice ENABLE ROW LEVEL SECURITY; ALTER TABLE invoice FORCE ROW LEVEL SECURITY;
CREATE POLICY rls_invoice__select ON invoice FOR SELECT USING (tenant_id = (SELECT app_tenant()));
CREATE POLICY rls_invoice__insert ON invoice FOR INSERT WITH CHECK (tenant_id = (SELECT app_tenant()));
CREATE POLICY rls_invoice__update ON invoice FOR UPDATE USING (tenant_id = (SELECT app_tenant())) WITH CHECK (tenant_id = (SELECT app_tenant()));
ALTER TABLE user_role_assignment ENABLE ROW LEVEL SECURITY; ALTER TABLE user_role_assignment FORCE ROW LEVEL SECURITY;
CREATE POLICY rls_user_role_assignment__select ON user_role_assignment FOR SELECT USING (tenant_id = (SELECT app_tenant()));
CREATE POLICY rls_user_role_assignment__insert ON user_role_assignment FOR INSERT WITH CHECK (tenant_id = (SELECT app_tenant()));
CREATE POLICY rls_user_role_assignment__update ON user_role_assignment FOR UPDATE USING (tenant_id = (SELECT app_tenant())) WITH CHECK (tenant_id = (SELECT app_tenant()));
ALTER TABLE tenant_data_key ENABLE ROW LEVEL SECURITY; ALTER TABLE tenant_data_key FORCE ROW LEVEL SECURITY;
CREATE POLICY rls_tenant_data_key__select ON tenant_data_key FOR SELECT USING (tenant_id = (SELECT app_tenant()));
CREATE POLICY rls_tenant_data_key__insert ON tenant_data_key FOR INSERT WITH CHECK (tenant_id = (SELECT app_tenant()));
CREATE POLICY rls_tenant_data_key__update ON tenant_data_key FOR UPDATE USING (tenant_id = (SELECT app_tenant())) WITH CHECK (tenant_id = (SELECT app_tenant()));
ALTER TABLE company_operating_country ENABLE ROW LEVEL SECURITY; ALTER TABLE company_operating_country FORCE ROW LEVEL SECURITY;
CREATE POLICY rls_company_operating_country__select ON company_operating_country FOR SELECT USING (tenant_id = (SELECT app_tenant()) AND company_id = ANY ((SELECT app_company_ids())::uuid[]));
CREATE POLICY rls_company_operating_country__insert ON company_operating_country FOR INSERT WITH CHECK (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company()));
CREATE POLICY rls_company_operating_country__update ON company_operating_country FOR UPDATE USING (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company())) WITH CHECK (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company()));
ALTER TABLE offering_market ENABLE ROW LEVEL SECURITY; ALTER TABLE offering_market FORCE ROW LEVEL SECURITY;
CREATE POLICY rls_offering_market__select ON offering_market FOR SELECT USING (tenant_id = (SELECT app_tenant()) AND company_id = ANY ((SELECT app_company_ids())::uuid[]));
CREATE POLICY rls_offering_market__insert ON offering_market FOR INSERT WITH CHECK (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company()));
CREATE POLICY rls_offering_market__update ON offering_market FOR UPDATE USING (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company())) WITH CHECK (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company()));
ALTER TABLE channel_account_market ENABLE ROW LEVEL SECURITY; ALTER TABLE channel_account_market FORCE ROW LEVEL SECURITY;
CREATE POLICY rls_channel_account_market__select ON channel_account_market FOR SELECT USING (tenant_id = (SELECT app_tenant()) AND company_id = ANY ((SELECT app_company_ids())::uuid[]));
CREATE POLICY rls_channel_account_market__insert ON channel_account_market FOR INSERT WITH CHECK (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company()));
CREATE POLICY rls_channel_account_market__update ON channel_account_market FOR UPDATE USING (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company())) WITH CHECK (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company()));
ALTER TABLE configuration_revision ENABLE ROW LEVEL SECURITY; ALTER TABLE configuration_revision FORCE ROW LEVEL SECURITY;
CREATE POLICY rls_configuration_revision__select ON configuration_revision FOR SELECT USING (tenant_id = (SELECT app_tenant()) AND company_id = ANY ((SELECT app_company_ids())::uuid[]));
CREATE POLICY rls_configuration_revision__insert ON configuration_revision FOR INSERT WITH CHECK (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company()));
CREATE POLICY rls_configuration_revision__update ON configuration_revision FOR UPDATE USING (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company())) WITH CHECK (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company()));
ALTER TABLE workflow_configuration ENABLE ROW LEVEL SECURITY; ALTER TABLE workflow_configuration FORCE ROW LEVEL SECURITY;
CREATE POLICY rls_workflow_configuration__select ON workflow_configuration FOR SELECT USING (tenant_id = (SELECT app_tenant()) AND company_id = ANY ((SELECT app_company_ids())::uuid[]));
CREATE POLICY rls_workflow_configuration__insert ON workflow_configuration FOR INSERT WITH CHECK (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company()));
CREATE POLICY rls_workflow_configuration__update ON workflow_configuration FOR UPDATE USING (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company())) WITH CHECK (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company()));
ALTER TABLE business_event ENABLE ROW LEVEL SECURITY; ALTER TABLE business_event FORCE ROW LEVEL SECURITY;
CREATE POLICY rls_business_event__select ON business_event FOR SELECT USING (tenant_id = (SELECT app_tenant()) AND company_id = ANY ((SELECT app_company_ids())::uuid[]));
CREATE POLICY rls_business_event__insert ON business_event FOR INSERT WITH CHECK (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company()));
ALTER TABLE metric_aggregate ENABLE ROW LEVEL SECURITY; ALTER TABLE metric_aggregate FORCE ROW LEVEL SECURITY;
CREATE POLICY rls_metric_aggregate__select ON metric_aggregate FOR SELECT USING (tenant_id = (SELECT app_tenant()) AND company_id = ANY ((SELECT app_company_ids())::uuid[]));
CREATE POLICY rls_metric_aggregate__insert ON metric_aggregate FOR INSERT WITH CHECK (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company()));
CREATE POLICY rls_metric_aggregate__update ON metric_aggregate FOR UPDATE USING (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company())) WITH CHECK (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company()));
ALTER TABLE experiment ENABLE ROW LEVEL SECURITY; ALTER TABLE experiment FORCE ROW LEVEL SECURITY;
CREATE POLICY rls_experiment__select ON experiment FOR SELECT USING (tenant_id = (SELECT app_tenant()) AND company_id = ANY ((SELECT app_company_ids())::uuid[]));
CREATE POLICY rls_experiment__insert ON experiment FOR INSERT WITH CHECK (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company()));
CREATE POLICY rls_experiment__update ON experiment FOR UPDATE USING (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company())) WITH CHECK (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company()));
ALTER TABLE feedback_case ENABLE ROW LEVEL SECURITY; ALTER TABLE feedback_case FORCE ROW LEVEL SECURITY;
CREATE POLICY rls_feedback_case__select ON feedback_case FOR SELECT USING (tenant_id = (SELECT app_tenant()) AND company_id = ANY ((SELECT app_company_ids())::uuid[]));
CREATE POLICY rls_feedback_case__insert ON feedback_case FOR INSERT WITH CHECK (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company()));
CREATE POLICY rls_feedback_case__update ON feedback_case FOR UPDATE USING (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company())) WITH CHECK (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company()));
ALTER TABLE customer_value ENABLE ROW LEVEL SECURITY; ALTER TABLE customer_value FORCE ROW LEVEL SECURITY;
CREATE POLICY rls_customer_value__select ON customer_value FOR SELECT USING (tenant_id = (SELECT app_tenant()));
CREATE POLICY rls_customer_value__insert ON customer_value FOR INSERT WITH CHECK (tenant_id = (SELECT app_tenant()));
CREATE POLICY rls_customer_value__update ON customer_value FOR UPDATE USING (tenant_id = (SELECT app_tenant())) WITH CHECK (tenant_id = (SELECT app_tenant()));
ALTER TABLE journey_event ENABLE ROW LEVEL SECURITY; ALTER TABLE journey_event FORCE ROW LEVEL SECURITY;
CREATE POLICY rls_journey_event__subscriber ON journey_event FOR SELECT TO ge_app, ge_worker USING (audience = 'subscriber' AND tenant_id = (SELECT app_tenant()));
CREATE POLICY rls_journey_event__insert ON journey_event FOR INSERT TO ge_app, ge_worker WITH CHECK ((audience = 'subscriber' AND tenant_id = (SELECT app_tenant())) OR (audience = 'operator' AND tenant_id IS NULL AND (SELECT app_actor_kind()) = 'service'));
CREATE POLICY rls_journey_event__operator ON journey_event FOR SELECT TO ge_readonly USING (audience = 'operator');
ALTER TABLE domain_record_version ENABLE ROW LEVEL SECURITY; ALTER TABLE domain_record_version FORCE ROW LEVEL SECURITY;
CREATE POLICY rls_domain_record_version__select ON domain_record_version FOR SELECT USING (tenant_id = (SELECT app_tenant()) AND company_id = ANY ((SELECT app_company_ids())::uuid[]));
CREATE POLICY rls_domain_record_version__insert ON domain_record_version FOR INSERT WITH CHECK (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company()));
ALTER TABLE usage_reservation ENABLE ROW LEVEL SECURITY; ALTER TABLE usage_reservation FORCE ROW LEVEL SECURITY;
CREATE POLICY rls_usage_reservation__select ON usage_reservation FOR SELECT USING (tenant_id = (SELECT app_tenant()) AND company_id = ANY ((SELECT app_company_ids())::uuid[]));
CREATE POLICY rls_usage_reservation__insert ON usage_reservation FOR INSERT WITH CHECK (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company()));
CREATE POLICY rls_usage_reservation__update ON usage_reservation FOR UPDATE USING (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company())) WITH CHECK (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company()));
CREATE POLICY rls_audit_event__insert_definer ON audit_event FOR INSERT TO CURRENT_USER WITH CHECK (tenant_id = (SELECT app_tenant()));
CREATE INDEX IF NOT EXISTS ix_ai_model__rollback_to ON ai_model (rollback_to);  -- FK support (IX-R1)
CREATE INDEX IF NOT EXISTS ix_api_key__tenant_id ON api_key (tenant_id);  -- FK support (IX-R1)
CREATE INDEX IF NOT EXISTS ix_audit_sink__tenant_id ON audit_sink (tenant_id);  -- FK support (IX-R1)
CREATE INDEX IF NOT EXISTS ix_brand__tenant_id_company_id_division_id ON brand (tenant_id,company_id,division_id);  -- FK support (IX-R1)
CREATE INDEX IF NOT EXISTS ix_brand__tenant_id_division_id ON brand (tenant_id,division_id);  -- FK support (IX-R1)
CREATE INDEX IF NOT EXISTS ix_business_event__tenant_id_company_id_account_id ON business_event (tenant_id,company_id,account_id);  -- FK support (IX-R1)
CREATE INDEX IF NOT EXISTS ix_business_event__tenant_id_company_id_market_id ON business_event (tenant_id,company_id,market_id);  -- FK support (IX-R1)
CREATE INDEX IF NOT EXISTS ix_business_event__tenant_id_company_id_offering_id ON business_event (tenant_id,company_id,offering_id);  -- FK support (IX-R1)
CREATE INDEX IF NOT EXISTS ix_business_event__tenant_id_company_id_run_id ON business_event (tenant_id,company_id,run_id);  -- FK support (IX-R1)
CREATE INDEX IF NOT EXISTS ix_channel_account_market__tenant_id_company_id_market_id ON channel_account_market (tenant_id,company_id,market_id);  -- FK support (IX-R1)
CREATE INDEX IF NOT EXISTS ix_company__tenant_id_organization_id ON company (tenant_id,organization_id);  -- FK support (IX-R1)
CREATE INDEX IF NOT EXISTS ix_config_promotion__tenant_id_sandbox_id ON config_promotion (tenant_id,sandbox_id);  -- FK support (IX-R1)
CREATE INDEX IF NOT EXISTS ix_connector_installation__tenant_id ON connector_installation (tenant_id);  -- FK support (IX-R1)
CREATE INDEX IF NOT EXISTS ix_consent_record__tenant_id_contact_id ON consent_record (tenant_id,contact_id);  -- FK support (IX-R1)
CREATE INDEX IF NOT EXISTS ix_consent_record__tenant_id_company_id ON consent_record (tenant_id,company_id);  -- FK support (IX-R1)
CREATE INDEX IF NOT EXISTS ix_domain_record_version__tenant_id_company_id ON domain_record_version (tenant_id,company_id);  -- FK support (IX-R1)
CREATE INDEX IF NOT EXISTS ix_effect__tenant_id_company_id_run_id ON effect (tenant_id,company_id,run_id);  -- FK support (IX-R1)
CREATE INDEX IF NOT EXISTS ix_eval_run__suite_id ON eval_run (suite_id);  -- FK support (IX-R1)
CREATE INDEX IF NOT EXISTS ix_experiment__primary_metric_id_primary_metric_version ON experiment (primary_metric_id,primary_metric_version);  -- FK support (IX-R1)
CREATE INDEX IF NOT EXISTS ix_experiment__tenant_id_company_id ON experiment (tenant_id,company_id);  -- FK support (IX-R1)
CREATE INDEX IF NOT EXISTS ix_export_job__tenant_id ON export_job (tenant_id);  -- FK support (IX-R1)
CREATE INDEX IF NOT EXISTS ix_feedback_case__tenant_id_company_id ON feedback_case (tenant_id,company_id);  -- FK support (IX-R1)
CREATE INDEX IF NOT EXISTS ix_growth_activity__tenant_id_company_id ON growth_activity (tenant_id,company_id);  -- FK support (IX-R1)
CREATE INDEX IF NOT EXISTS ix_growth_ad_campaign__tenant_id_company_id ON growth_ad_campaign (tenant_id,company_id);  -- FK support (IX-R1)
CREATE INDEX IF NOT EXISTS ix_growth_ad_spend_event__tenant_id_company_id ON growth_ad_spend_event (tenant_id,company_id);  -- FK support (IX-R1)
CREATE INDEX IF NOT EXISTS ix_growth_approval__tenant_id_company_id ON growth_approval (tenant_id,company_id);  -- FK support (IX-R1)
CREATE INDEX IF NOT EXISTS ix_growth_attribution_event__tenant_id_company_id ON growth_attribution_event (tenant_id,company_id);  -- FK support (IX-R1)
CREATE INDEX IF NOT EXISTS ix_growth_audience__tenant_id_company_id ON growth_audience (tenant_id,company_id);  -- FK support (IX-R1)
CREATE INDEX IF NOT EXISTS ix_growth_budget__tenant_id_company_id ON growth_budget (tenant_id,company_id);  -- FK support (IX-R1)
CREATE INDEX IF NOT EXISTS ix_growth_business_event__tenant_id_company_id ON growth_business_event (tenant_id,company_id);  -- FK support (IX-R1)
CREATE INDEX IF NOT EXISTS ix_growth_calendar_link__tenant_id_company_id ON growth_calendar_link (tenant_id,company_id);  -- FK support (IX-R1)
CREATE INDEX IF NOT EXISTS ix_growth_campaign__tenant_id_company_id ON growth_campaign (tenant_id,company_id);  -- FK support (IX-R1)
CREATE INDEX IF NOT EXISTS ix_growth_campaign_version__tenant_id_company_id ON growth_campaign_version (tenant_id,company_id);  -- FK support (IX-R1)
CREATE INDEX IF NOT EXISTS ix_growth_channel_account__tenant_id_company_id ON growth_channel_account (tenant_id,company_id);  -- FK support (IX-R1)
CREATE INDEX IF NOT EXISTS ix_growth_claim__tenant_id_company_id ON growth_claim (tenant_id,company_id);  -- FK support (IX-R1)
CREATE INDEX IF NOT EXISTS ix_growth_competitor__tenant_id_company_id ON growth_competitor (tenant_id,company_id);  -- FK support (IX-R1)
CREATE INDEX IF NOT EXISTS ix_growth_consent__tenant_id_company_id ON growth_consent (tenant_id,company_id);  -- FK support (IX-R1)
CREATE INDEX IF NOT EXISTS ix_growth_contact_source__tenant_id_company_id ON growth_contact_source (tenant_id,company_id);  -- FK support (IX-R1)
CREATE INDEX IF NOT EXISTS ix_growth_contact__tenant_id_company_id ON growth_contact (tenant_id,company_id);  -- FK support (IX-R1)
CREATE INDEX IF NOT EXISTS ix_growth_contact_verification__tenant_id_company_id ON growth_contact_verification (tenant_id,company_id);  -- FK support (IX-R1)
CREATE INDEX IF NOT EXISTS ix_growth_content_asset__tenant_id_company_id ON growth_content_asset (tenant_id,company_id);  -- FK support (IX-R1)
CREATE INDEX IF NOT EXISTS ix_growth_content_version__tenant_id_company_id ON growth_content_version (tenant_id,company_id);  -- FK support (IX-R1)
CREATE INDEX IF NOT EXISTS ix_growth_contract__tenant_id_company_id ON growth_contract (tenant_id,company_id);  -- FK support (IX-R1)
CREATE INDEX IF NOT EXISTS ix_growth_deal__tenant_id_company_id ON growth_deal (tenant_id,company_id);  -- FK support (IX-R1)
CREATE INDEX IF NOT EXISTS ix_growth_delivery_event__tenant_id_company_id ON growth_delivery_event (tenant_id,company_id);  -- FK support (IX-R1)
CREATE INDEX IF NOT EXISTS ix_growth_deployment__tenant_id_company_id ON growth_deployment (tenant_id,company_id);  -- FK support (IX-R1)
CREATE INDEX IF NOT EXISTS ix_growth_document_chunk__tenant_id_company_id ON growth_document_chunk (tenant_id,company_id);  -- FK support (IX-R1)
CREATE INDEX IF NOT EXISTS ix_growth_document__tenant_id_company_id ON growth_document (tenant_id,company_id);  -- FK support (IX-R1)
CREATE INDEX IF NOT EXISTS ix_growth_embedding__tenant_id_company_id ON growth_embedding (tenant_id,company_id);  -- FK support (IX-R1)
CREATE INDEX IF NOT EXISTS ix_growth_enrollment__tenant_id_company_id ON growth_enrollment (tenant_id,company_id);  -- FK support (IX-R1)
CREATE INDEX IF NOT EXISTS ix_growth_event_attendance__tenant_id_company_id ON growth_event_attendance (tenant_id,company_id);  -- FK support (IX-R1)
CREATE INDEX IF NOT EXISTS ix_growth_event_registration__tenant_id_company_id ON growth_event_registration (tenant_id,company_id);  -- FK support (IX-R1)
CREATE INDEX IF NOT EXISTS ix_growth_evidence__tenant_id_company_id ON growth_evidence (tenant_id,company_id);  -- FK support (IX-R1)
CREATE INDEX IF NOT EXISTS ix_growth_feedback__tenant_id_company_id ON growth_feedback (tenant_id,company_id);  -- FK support (IX-R1)
CREATE INDEX IF NOT EXISTS ix_growth_forecast__tenant_id_company_id ON growth_forecast (tenant_id,company_id);  -- FK support (IX-R1)
CREATE INDEX IF NOT EXISTS ix_growth_form__tenant_id_company_id ON growth_form (tenant_id,company_id);  -- FK support (IX-R1)
CREATE INDEX IF NOT EXISTS ix_growth_identity_link__tenant_id_company_id ON growth_identity_link (tenant_id,company_id);  -- FK support (IX-R1)
CREATE INDEX IF NOT EXISTS ix_growth_inbound_event__tenant_id_company_id ON growth_inbound_event (tenant_id,company_id);  -- FK support (IX-R1)
CREATE INDEX IF NOT EXISTS ix_growth_integration_deal__tenant_id_company_id ON growth_integration_deal (tenant_id,company_id);  -- FK support (IX-R1)
CREATE INDEX IF NOT EXISTS ix_growth_invoice__tenant_id_company_id ON growth_invoice (tenant_id,company_id);  -- FK support (IX-R1)
CREATE INDEX IF NOT EXISTS ix_growth_keyword__tenant_id_company_id ON growth_keyword (tenant_id,company_id);  -- FK support (IX-R1)
CREATE INDEX IF NOT EXISTS ix_growth_landing_page__tenant_id_company_id ON growth_landing_page (tenant_id,company_id);  -- FK support (IX-R1)
CREATE INDEX IF NOT EXISTS ix_growth_lead__tenant_id_company_id ON growth_lead (tenant_id,company_id);  -- FK support (IX-R1)
CREATE INDEX IF NOT EXISTS ix_growth_market_event__tenant_id_company_id ON growth_market_event (tenant_id,company_id);  -- FK support (IX-R1)
CREATE INDEX IF NOT EXISTS ix_growth_meeting__tenant_id_company_id ON growth_meeting (tenant_id,company_id);  -- FK support (IX-R1)
CREATE INDEX IF NOT EXISTS ix_growth_message_draft__tenant_id_company_id ON growth_message_draft (tenant_id,company_id);  -- FK support (IX-R1)
CREATE INDEX IF NOT EXISTS ix_growth_message_template__tenant_id_company_id ON growth_message_template (tenant_id,company_id);  -- FK support (IX-R1)
CREATE INDEX IF NOT EXISTS ix_growth_message__tenant_id_company_id ON growth_message (tenant_id,company_id);  -- FK support (IX-R1)
CREATE INDEX IF NOT EXISTS ix_growth_metric_snapshot__tenant_id_company_id ON growth_metric_snapshot (tenant_id,company_id);  -- FK support (IX-R1)
CREATE INDEX IF NOT EXISTS ix_growth_need_evidence__tenant_id_company_id ON growth_need_evidence (tenant_id,company_id);  -- FK support (IX-R1)
CREATE INDEX IF NOT EXISTS ix_growth_need__tenant_id_company_id ON growth_need (tenant_id,company_id);  -- FK support (IX-R1)
CREATE INDEX IF NOT EXISTS ix_growth_negotiation__tenant_id_company_id ON growth_negotiation (tenant_id,company_id);  -- FK support (IX-R1)
CREATE INDEX IF NOT EXISTS ix_growth_objection__tenant_id_company_id ON growth_objection (tenant_id,company_id);  -- FK support (IX-R1)
CREATE INDEX IF NOT EXISTS ix_growth_onboarding__tenant_id_company_id ON growth_onboarding (tenant_id,company_id);  -- FK support (IX-R1)
CREATE INDEX IF NOT EXISTS ix_growth_opportunity__tenant_id_company_id ON growth_opportunity (tenant_id,company_id);  -- FK support (IX-R1)
CREATE INDEX IF NOT EXISTS ix_growth_organization__tenant_id_company_id ON growth_organization (tenant_id,company_id);  -- FK support (IX-R1)
CREATE INDEX IF NOT EXISTS ix_growth_outbox__tenant_id_company_id ON growth_outbox (tenant_id,company_id);  -- FK support (IX-R1)
CREATE INDEX IF NOT EXISTS ix_growth_page_metric__tenant_id_company_id ON growth_page_metric (tenant_id,company_id);  -- FK support (IX-R1)
CREATE INDEX IF NOT EXISTS ix_growth_partner__tenant_id_company_id ON growth_partner (tenant_id,company_id);  -- FK support (IX-R1)
CREATE INDEX IF NOT EXISTS ix_growth_payment__tenant_id_company_id ON growth_payment (tenant_id,company_id);  -- FK support (IX-R1)
CREATE INDEX IF NOT EXISTS ix_growth_pilot__tenant_id_company_id ON growth_pilot (tenant_id,company_id);  -- FK support (IX-R1)
CREATE INDEX IF NOT EXISTS ix_growth_product__tenant_id_company_id ON growth_product (tenant_id,company_id);  -- FK support (IX-R1)
CREATE INDEX IF NOT EXISTS ix_growth_proposal__tenant_id_company_id ON growth_proposal (tenant_id,company_id);  -- FK support (IX-R1)
CREATE INDEX IF NOT EXISTS ix_growth_proposal_version__tenant_id_company_id ON growth_proposal_version (tenant_id,company_id);  -- FK support (IX-R1)
CREATE INDEX IF NOT EXISTS ix_growth_quote_line__tenant_id_company_id ON growth_quote_line (tenant_id,company_id);  -- FK support (IX-R1)
CREATE INDEX IF NOT EXISTS ix_growth_quote__tenant_id_company_id ON growth_quote (tenant_id,company_id);  -- FK support (IX-R1)
CREATE INDEX IF NOT EXISTS ix_growth_referral__tenant_id_company_id ON growth_referral (tenant_id,company_id);  -- FK support (IX-R1)
CREATE INDEX IF NOT EXISTS ix_growth_renewal__tenant_id_company_id ON growth_renewal (tenant_id,company_id);  -- FK support (IX-R1)
CREATE INDEX IF NOT EXISTS ix_growth_routing_rule__tenant_id_company_id ON growth_routing_rule (tenant_id,company_id);  -- FK support (IX-R1)
CREATE INDEX IF NOT EXISTS ix_growth_score_version__tenant_id_company_id ON growth_score_version (tenant_id,company_id);  -- FK support (IX-R1)
CREATE INDEX IF NOT EXISTS ix_growth_search_plan__tenant_id_company_id ON growth_search_plan (tenant_id,company_id);  -- FK support (IX-R1)
CREATE INDEX IF NOT EXISTS ix_growth_seo_issue__tenant_id_company_id ON growth_seo_issue (tenant_id,company_id);  -- FK support (IX-R1)
CREATE INDEX IF NOT EXISTS ix_growth_sequence_step__tenant_id_company_id ON growth_sequence_step (tenant_id,company_id);  -- FK support (IX-R1)
CREATE INDEX IF NOT EXISTS ix_growth_sequence__tenant_id_company_id ON growth_sequence (tenant_id,company_id);  -- FK support (IX-R1)
CREATE INDEX IF NOT EXISTS ix_growth_signal__tenant_id_company_id ON growth_signal (tenant_id,company_id);  -- FK support (IX-R1)
CREATE INDEX IF NOT EXISTS ix_growth_signal_type__tenant_id_company_id ON growth_signal_type (tenant_id,company_id);  -- FK support (IX-R1)
CREATE INDEX IF NOT EXISTS ix_growth_social_post__tenant_id_company_id ON growth_social_post (tenant_id,company_id);  -- FK support (IX-R1)
CREATE INDEX IF NOT EXISTS ix_growth_social_publication__tenant_id_company_id ON growth_social_publication (tenant_id,company_id);  -- FK support (IX-R1)
CREATE INDEX IF NOT EXISTS ix_growth_source_policy__tenant_id_company_id ON growth_source_policy (tenant_id,company_id);  -- FK support (IX-R1)
CREATE INDEX IF NOT EXISTS ix_growth_source_record__tenant_id_company_id ON growth_source_record (tenant_id,company_id);  -- FK support (IX-R1)
CREATE INDEX IF NOT EXISTS ix_growth_source__tenant_id_company_id ON growth_source (tenant_id,company_id);  -- FK support (IX-R1)
CREATE INDEX IF NOT EXISTS ix_growth_stage_metric__tenant_id_company_id ON growth_stage_metric (tenant_id,company_id);  -- FK support (IX-R1)
CREATE INDEX IF NOT EXISTS ix_growth_stage__tenant_id_company_id ON growth_stage (tenant_id,company_id);  -- FK support (IX-R1)
CREATE INDEX IF NOT EXISTS ix_growth_suppression__tenant_id_company_id ON growth_suppression (tenant_id,company_id);  -- FK support (IX-R1)
CREATE INDEX IF NOT EXISTS ix_growth_task__tenant_id_company_id ON growth_task (tenant_id,company_id);  -- FK support (IX-R1)
CREATE INDEX IF NOT EXISTS ix_growth_thread__tenant_id_company_id ON growth_thread (tenant_id,company_id);  -- FK support (IX-R1)
CREATE INDEX IF NOT EXISTS ix_growth_workflow_execution__tenant_id_company_id ON growth_workflow_execution (tenant_id,company_id);  -- FK support (IX-R1)
CREATE INDEX IF NOT EXISTS ix_invoice__tax_rule_id ON invoice (tax_rule_id);  -- FK support (IX-R1)
CREATE INDEX IF NOT EXISTS ix_invoice__tenant_id ON invoice (tenant_id);  -- FK support (IX-R1)
CREATE INDEX IF NOT EXISTS ix_metric_aggregate__metric_id_metric_version ON metric_aggregate (metric_id,metric_version);  -- FK support (IX-R1)
CREATE INDEX IF NOT EXISTS ix_offering__tenant_id_company_id_brand_id ON offering (tenant_id,company_id,brand_id);  -- FK support (IX-R1)
CREATE INDEX IF NOT EXISTS ix_offering_market__tenant_id_company_id_market_id ON offering_market (tenant_id,company_id,market_id);  -- FK support (IX-R1)
CREATE INDEX IF NOT EXISTS ix_offering__tenant_id_brand_id ON offering (tenant_id,brand_id);  -- FK support (IX-R1)
CREATE INDEX IF NOT EXISTS ix_portfolio_grant__tenant_id_company_id ON portfolio_grant (tenant_id,company_id);  -- FK support (IX-R1)
CREATE INDEX IF NOT EXISTS ix_sales_bid__tenant_id_company_id ON sales_bid (tenant_id,company_id);  -- FK support (IX-R1)
CREATE INDEX IF NOT EXISTS ix_sales_fulfillment__tenant_id_company_id ON sales_fulfillment (tenant_id,company_id);  -- FK support (IX-R1)
CREATE INDEX IF NOT EXISTS ix_sales_order_line__tenant_id_company_id ON sales_order_line (tenant_id,company_id);  -- FK support (IX-R1)
CREATE INDEX IF NOT EXISTS ix_sales_order__tenant_id_company_id ON sales_order (tenant_id,company_id);  -- FK support (IX-R1)
CREATE INDEX IF NOT EXISTS ix_scim_token__tenant_id ON scim_token (tenant_id);  -- FK support (IX-R1)
CREATE INDEX IF NOT EXISTS ix_usage_reservation__tenant_id_company_id_run_id ON usage_reservation (tenant_id,company_id,run_id);  -- FK support (IX-R1)
CREATE INDEX IF NOT EXISTS ix_user_role_assignment__tenant_id_role_id ON user_role_assignment (tenant_id,role_id);  -- FK support (IX-R1)
CREATE INDEX IF NOT EXISTS ix_workflow_configuration__tenant_id_company_id_account_id ON workflow_configuration (tenant_id,company_id,account_id);  -- FK support (IX-R1)
CREATE INDEX IF NOT EXISTS ix_workflow_configuration__tenant_id_company_id_market_id ON workflow_configuration (tenant_id,company_id,market_id);  -- FK support (IX-R1)
CREATE INDEX IF NOT EXISTS ix_workflow_configuration__tenant_id_config_revision_id ON workflow_configuration (tenant_id,config_revision_id);  -- FK support (IX-R1)
CREATE INDEX IF NOT EXISTS ix_workflow_step_run__tenant_id_company_id_run_id ON workflow_step_run (tenant_id,company_id,run_id);  -- FK support (IX-R1)
CREATE INDEX IF NOT EXISTS ix_growth_source__scope_status_upd ON growth_source (tenant_id, company_id, status, updated_at DESC);  -- V5 common physical design
CREATE INDEX IF NOT EXISTS ix_growth_source__schema_ref ON growth_source (tenant_id, company_id, schema_ref);  -- registry lookup
CREATE INDEX IF NOT EXISTS ix_growth_source_policy__scope_status_upd ON growth_source_policy (tenant_id, company_id, status, updated_at DESC);  -- V5 common physical design
CREATE INDEX IF NOT EXISTS ix_growth_source_policy__schema_ref ON growth_source_policy (tenant_id, company_id, schema_ref);  -- registry lookup
CREATE INDEX IF NOT EXISTS ix_growth_source_record__scope_status_upd ON growth_source_record (tenant_id, company_id, status, updated_at DESC);  -- V5 common physical design
CREATE INDEX IF NOT EXISTS ix_growth_source_record__schema_ref ON growth_source_record (tenant_id, company_id, schema_ref);  -- registry lookup
CREATE INDEX IF NOT EXISTS ix_growth_evidence__scope_status_upd ON growth_evidence (tenant_id, company_id, status, updated_at DESC);  -- V5 common physical design
CREATE INDEX IF NOT EXISTS ix_growth_evidence__schema_ref ON growth_evidence (tenant_id, company_id, schema_ref);  -- registry lookup
CREATE INDEX IF NOT EXISTS ix_growth_competitor__scope_status_upd ON growth_competitor (tenant_id, company_id, status, updated_at DESC);  -- V5 common physical design
CREATE INDEX IF NOT EXISTS ix_growth_competitor__schema_ref ON growth_competitor (tenant_id, company_id, schema_ref);  -- registry lookup
CREATE INDEX IF NOT EXISTS ix_growth_market_event__scope_status_upd ON growth_market_event (tenant_id, company_id, status, updated_at DESC);  -- V5 common physical design
CREATE INDEX IF NOT EXISTS ix_growth_market_event__schema_ref ON growth_market_event (tenant_id, company_id, schema_ref);  -- registry lookup
CREATE INDEX IF NOT EXISTS ix_growth_search_plan__scope_status_upd ON growth_search_plan (tenant_id, company_id, status, updated_at DESC);  -- V5 common physical design
CREATE INDEX IF NOT EXISTS ix_growth_search_plan__schema_ref ON growth_search_plan (tenant_id, company_id, schema_ref);  -- registry lookup
CREATE INDEX IF NOT EXISTS ix_growth_organization__scope_status_upd ON growth_organization (tenant_id, company_id, status, updated_at DESC);  -- V5 common physical design
CREATE INDEX IF NOT EXISTS ix_growth_organization__schema_ref ON growth_organization (tenant_id, company_id, schema_ref);  -- registry lookup
CREATE INDEX IF NOT EXISTS ix_growth_signal__scope_status_upd ON growth_signal (tenant_id, company_id, status, updated_at DESC);  -- V5 common physical design
CREATE INDEX IF NOT EXISTS ix_growth_signal__schema_ref ON growth_signal (tenant_id, company_id, schema_ref);  -- registry lookup
CREATE INDEX IF NOT EXISTS ix_growth_signal_type__scope_status_upd ON growth_signal_type (tenant_id, company_id, status, updated_at DESC);  -- V5 common physical design
CREATE INDEX IF NOT EXISTS ix_growth_signal_type__schema_ref ON growth_signal_type (tenant_id, company_id, schema_ref);  -- registry lookup
CREATE INDEX IF NOT EXISTS ix_growth_need_evidence__scope_status_upd ON growth_need_evidence (tenant_id, company_id, status, updated_at DESC);  -- V5 common physical design
CREATE INDEX IF NOT EXISTS ix_growth_need_evidence__schema_ref ON growth_need_evidence (tenant_id, company_id, schema_ref);  -- registry lookup
CREATE INDEX IF NOT EXISTS ix_growth_referral__scope_status_upd ON growth_referral (tenant_id, company_id, status, updated_at DESC);  -- V5 common physical design
CREATE INDEX IF NOT EXISTS ix_growth_referral__schema_ref ON growth_referral (tenant_id, company_id, schema_ref);  -- registry lookup
CREATE INDEX IF NOT EXISTS ix_growth_contact__scope_status_upd ON growth_contact (tenant_id, company_id, status, updated_at DESC);  -- V5 common physical design
CREATE INDEX IF NOT EXISTS ix_growth_contact__schema_ref ON growth_contact (tenant_id, company_id, schema_ref);  -- registry lookup
CREATE INDEX IF NOT EXISTS ix_growth_contact_source__scope_status_upd ON growth_contact_source (tenant_id, company_id, status, updated_at DESC);  -- V5 common physical design
CREATE INDEX IF NOT EXISTS ix_growth_contact_source__schema_ref ON growth_contact_source (tenant_id, company_id, schema_ref);  -- registry lookup
CREATE INDEX IF NOT EXISTS ix_growth_contact_verification__scope_status_upd ON growth_contact_verification (tenant_id, company_id, status, updated_at DESC);  -- V5 common physical design
CREATE INDEX IF NOT EXISTS ix_growth_contact_verification__schema_ref ON growth_contact_verification (tenant_id, company_id, schema_ref);  -- registry lookup
CREATE INDEX IF NOT EXISTS ix_growth_consent__scope_status_upd ON growth_consent (tenant_id, company_id, status, updated_at DESC);  -- V5 common physical design
CREATE INDEX IF NOT EXISTS ix_growth_consent__schema_ref ON growth_consent (tenant_id, company_id, schema_ref);  -- registry lookup
CREATE INDEX IF NOT EXISTS ix_growth_suppression__scope_status_upd ON growth_suppression (tenant_id, company_id, status, updated_at DESC);  -- V5 common physical design
CREATE INDEX IF NOT EXISTS ix_growth_suppression__schema_ref ON growth_suppression (tenant_id, company_id, schema_ref);  -- registry lookup
CREATE INDEX IF NOT EXISTS ix_growth_need__scope_status_upd ON growth_need (tenant_id, company_id, status, updated_at DESC);  -- V5 common physical design
CREATE INDEX IF NOT EXISTS ix_growth_need__schema_ref ON growth_need (tenant_id, company_id, schema_ref);  -- registry lookup
CREATE INDEX IF NOT EXISTS ix_growth_product__scope_status_upd ON growth_product (tenant_id, company_id, status, updated_at DESC);  -- V5 common physical design
CREATE INDEX IF NOT EXISTS ix_growth_product__schema_ref ON growth_product (tenant_id, company_id, schema_ref);  -- registry lookup
CREATE INDEX IF NOT EXISTS ix_growth_opportunity__scope_status_upd ON growth_opportunity (tenant_id, company_id, status, updated_at DESC);  -- V5 common physical design
CREATE INDEX IF NOT EXISTS ix_growth_opportunity__schema_ref ON growth_opportunity (tenant_id, company_id, schema_ref);  -- registry lookup
CREATE INDEX IF NOT EXISTS ix_growth_score_version__scope_status_upd ON growth_score_version (tenant_id, company_id, status, updated_at DESC);  -- V5 common physical design
CREATE INDEX IF NOT EXISTS ix_growth_score_version__schema_ref ON growth_score_version (tenant_id, company_id, schema_ref);  -- registry lookup
CREATE INDEX IF NOT EXISTS ix_growth_activity__scope_status_upd ON growth_activity (tenant_id, company_id, status, updated_at DESC);  -- V5 common physical design
CREATE INDEX IF NOT EXISTS ix_growth_activity__schema_ref ON growth_activity (tenant_id, company_id, schema_ref);  -- registry lookup
CREATE INDEX IF NOT EXISTS ix_growth_deal__scope_status_upd ON growth_deal (tenant_id, company_id, status, updated_at DESC);  -- V5 common physical design
CREATE INDEX IF NOT EXISTS ix_growth_deal__schema_ref ON growth_deal (tenant_id, company_id, schema_ref);  -- registry lookup
CREATE INDEX IF NOT EXISTS ix_growth_stage__scope_status_upd ON growth_stage (tenant_id, company_id, status, updated_at DESC);  -- V5 common physical design
CREATE INDEX IF NOT EXISTS ix_growth_stage__schema_ref ON growth_stage (tenant_id, company_id, schema_ref);  -- registry lookup
CREATE INDEX IF NOT EXISTS ix_growth_task__scope_status_upd ON growth_task (tenant_id, company_id, status, updated_at DESC);  -- V5 common physical design
CREATE INDEX IF NOT EXISTS ix_growth_task__schema_ref ON growth_task (tenant_id, company_id, schema_ref);  -- registry lookup
CREATE INDEX IF NOT EXISTS ix_growth_budget__scope_status_upd ON growth_budget (tenant_id, company_id, status, updated_at DESC);  -- V5 common physical design
CREATE INDEX IF NOT EXISTS ix_growth_budget__schema_ref ON growth_budget (tenant_id, company_id, schema_ref);  -- registry lookup
CREATE INDEX IF NOT EXISTS ix_growth_message__scope_status_upd ON growth_message (tenant_id, company_id, status, updated_at DESC);  -- V5 common physical design
CREATE INDEX IF NOT EXISTS ix_growth_message__schema_ref ON growth_message (tenant_id, company_id, schema_ref);  -- registry lookup
CREATE INDEX IF NOT EXISTS ix_growth_message_draft__scope_status_upd ON growth_message_draft (tenant_id, company_id, status, updated_at DESC);  -- V5 common physical design
CREATE INDEX IF NOT EXISTS ix_growth_message_draft__schema_ref ON growth_message_draft (tenant_id, company_id, schema_ref);  -- registry lookup
CREATE INDEX IF NOT EXISTS ix_growth_message_template__scope_status_upd ON growth_message_template (tenant_id, company_id, status, updated_at DESC);  -- V5 common physical design
CREATE INDEX IF NOT EXISTS ix_growth_message_template__schema_ref ON growth_message_template (tenant_id, company_id, schema_ref);  -- registry lookup
CREATE INDEX IF NOT EXISTS ix_growth_outbox__scope_status_upd ON growth_outbox (tenant_id, company_id, status, updated_at DESC);  -- V5 common physical design
CREATE INDEX IF NOT EXISTS ix_growth_outbox__schema_ref ON growth_outbox (tenant_id, company_id, schema_ref);  -- registry lookup
CREATE INDEX IF NOT EXISTS ix_growth_delivery_event__scope_status_upd ON growth_delivery_event (tenant_id, company_id, status, updated_at DESC);  -- V5 common physical design
CREATE INDEX IF NOT EXISTS ix_growth_delivery_event__schema_ref ON growth_delivery_event (tenant_id, company_id, schema_ref);  -- registry lookup
CREATE INDEX IF NOT EXISTS ix_growth_thread__scope_status_upd ON growth_thread (tenant_id, company_id, status, updated_at DESC);  -- V5 common physical design
CREATE INDEX IF NOT EXISTS ix_growth_thread__schema_ref ON growth_thread (tenant_id, company_id, schema_ref);  -- registry lookup
CREATE INDEX IF NOT EXISTS ix_growth_channel_account__scope_status_upd ON growth_channel_account (tenant_id, company_id, status, updated_at DESC);  -- V5 common physical design
CREATE INDEX IF NOT EXISTS ix_growth_channel_account__schema_ref ON growth_channel_account (tenant_id, company_id, schema_ref);  -- registry lookup
CREATE INDEX IF NOT EXISTS ix_growth_inbound_event__scope_status_upd ON growth_inbound_event (tenant_id, company_id, status, updated_at DESC);  -- V5 common physical design
CREATE INDEX IF NOT EXISTS ix_growth_inbound_event__schema_ref ON growth_inbound_event (tenant_id, company_id, schema_ref);  -- registry lookup
CREATE INDEX IF NOT EXISTS ix_growth_enrollment__scope_status_upd ON growth_enrollment (tenant_id, company_id, status, updated_at DESC);  -- V5 common physical design
CREATE INDEX IF NOT EXISTS ix_growth_enrollment__schema_ref ON growth_enrollment (tenant_id, company_id, schema_ref);  -- registry lookup
CREATE INDEX IF NOT EXISTS ix_growth_sequence__scope_status_upd ON growth_sequence (tenant_id, company_id, status, updated_at DESC);  -- V5 common physical design
CREATE INDEX IF NOT EXISTS ix_growth_sequence__schema_ref ON growth_sequence (tenant_id, company_id, schema_ref);  -- registry lookup
CREATE INDEX IF NOT EXISTS ix_growth_sequence_step__scope_status_upd ON growth_sequence_step (tenant_id, company_id, status, updated_at DESC);  -- V5 common physical design
CREATE INDEX IF NOT EXISTS ix_growth_sequence_step__schema_ref ON growth_sequence_step (tenant_id, company_id, schema_ref);  -- registry lookup
CREATE INDEX IF NOT EXISTS ix_growth_routing_rule__scope_status_upd ON growth_routing_rule (tenant_id, company_id, status, updated_at DESC);  -- V5 common physical design
CREATE INDEX IF NOT EXISTS ix_growth_routing_rule__schema_ref ON growth_routing_rule (tenant_id, company_id, schema_ref);  -- registry lookup
CREATE INDEX IF NOT EXISTS ix_growth_workflow_execution__scope_status_upd ON growth_workflow_execution (tenant_id, company_id, status, updated_at DESC);  -- V5 common physical design
CREATE INDEX IF NOT EXISTS ix_growth_workflow_execution__schema_ref ON growth_workflow_execution (tenant_id, company_id, schema_ref);  -- registry lookup
CREATE INDEX IF NOT EXISTS ix_growth_identity_link__scope_status_upd ON growth_identity_link (tenant_id, company_id, status, updated_at DESC);  -- V5 common physical design
CREATE INDEX IF NOT EXISTS ix_growth_identity_link__schema_ref ON growth_identity_link (tenant_id, company_id, schema_ref);  -- registry lookup
CREATE INDEX IF NOT EXISTS ix_growth_objection__scope_status_upd ON growth_objection (tenant_id, company_id, status, updated_at DESC);  -- V5 common physical design
CREATE INDEX IF NOT EXISTS ix_growth_objection__schema_ref ON growth_objection (tenant_id, company_id, schema_ref);  -- registry lookup
CREATE INDEX IF NOT EXISTS ix_growth_calendar_link__scope_status_upd ON growth_calendar_link (tenant_id, company_id, status, updated_at DESC);  -- V5 common physical design
CREATE INDEX IF NOT EXISTS ix_growth_calendar_link__schema_ref ON growth_calendar_link (tenant_id, company_id, schema_ref);  -- registry lookup
CREATE INDEX IF NOT EXISTS ix_growth_meeting__scope_status_upd ON growth_meeting (tenant_id, company_id, status, updated_at DESC);  -- V5 common physical design
CREATE INDEX IF NOT EXISTS ix_growth_meeting__schema_ref ON growth_meeting (tenant_id, company_id, schema_ref);  -- registry lookup
CREATE INDEX IF NOT EXISTS ix_growth_business_event__scope_status_upd ON growth_business_event (tenant_id, company_id, status, updated_at DESC);  -- V5 common physical design
CREATE INDEX IF NOT EXISTS ix_growth_business_event__schema_ref ON growth_business_event (tenant_id, company_id, schema_ref);  -- registry lookup
CREATE INDEX IF NOT EXISTS ix_growth_event_attendance__scope_status_upd ON growth_event_attendance (tenant_id, company_id, status, updated_at DESC);  -- V5 common physical design
CREATE INDEX IF NOT EXISTS ix_growth_event_attendance__schema_ref ON growth_event_attendance (tenant_id, company_id, schema_ref);  -- registry lookup
CREATE INDEX IF NOT EXISTS ix_growth_event_registration__scope_status_upd ON growth_event_registration (tenant_id, company_id, status, updated_at DESC);  -- V5 common physical design
CREATE INDEX IF NOT EXISTS ix_growth_event_registration__schema_ref ON growth_event_registration (tenant_id, company_id, schema_ref);  -- registry lookup
CREATE INDEX IF NOT EXISTS ix_growth_claim__scope_status_upd ON growth_claim (tenant_id, company_id, status, updated_at DESC);  -- V5 common physical design
CREATE INDEX IF NOT EXISTS ix_growth_claim__schema_ref ON growth_claim (tenant_id, company_id, schema_ref);  -- registry lookup
CREATE INDEX IF NOT EXISTS ix_growth_content_asset__scope_status_upd ON growth_content_asset (tenant_id, company_id, status, updated_at DESC);  -- V5 common physical design
CREATE INDEX IF NOT EXISTS ix_growth_content_asset__schema_ref ON growth_content_asset (tenant_id, company_id, schema_ref);  -- registry lookup
CREATE INDEX IF NOT EXISTS ix_growth_content_version__scope_status_upd ON growth_content_version (tenant_id, company_id, status, updated_at DESC);  -- V5 common physical design
CREATE INDEX IF NOT EXISTS ix_growth_content_version__schema_ref ON growth_content_version (tenant_id, company_id, schema_ref);  -- registry lookup
CREATE INDEX IF NOT EXISTS ix_growth_approval__scope_status_upd ON growth_approval (tenant_id, company_id, status, updated_at DESC);  -- V5 common physical design
CREATE INDEX IF NOT EXISTS ix_growth_approval__schema_ref ON growth_approval (tenant_id, company_id, schema_ref);  -- registry lookup
CREATE INDEX IF NOT EXISTS ix_growth_social_post__scope_status_upd ON growth_social_post (tenant_id, company_id, status, updated_at DESC);  -- V5 common physical design
CREATE INDEX IF NOT EXISTS ix_growth_social_post__schema_ref ON growth_social_post (tenant_id, company_id, schema_ref);  -- registry lookup
CREATE INDEX IF NOT EXISTS ix_growth_social_publication__scope_status_upd ON growth_social_publication (tenant_id, company_id, status, updated_at DESC);  -- V5 common physical design
CREATE INDEX IF NOT EXISTS ix_growth_social_publication__schema_ref ON growth_social_publication (tenant_id, company_id, schema_ref);  -- registry lookup
CREATE INDEX IF NOT EXISTS ix_growth_keyword__scope_status_upd ON growth_keyword (tenant_id, company_id, status, updated_at DESC);  -- V5 common physical design
CREATE INDEX IF NOT EXISTS ix_growth_keyword__schema_ref ON growth_keyword (tenant_id, company_id, schema_ref);  -- registry lookup
CREATE INDEX IF NOT EXISTS ix_growth_page_metric__scope_status_upd ON growth_page_metric (tenant_id, company_id, status, updated_at DESC);  -- V5 common physical design
CREATE INDEX IF NOT EXISTS ix_growth_page_metric__schema_ref ON growth_page_metric (tenant_id, company_id, schema_ref);  -- registry lookup
CREATE INDEX IF NOT EXISTS ix_growth_seo_issue__scope_status_upd ON growth_seo_issue (tenant_id, company_id, status, updated_at DESC);  -- V5 common physical design
CREATE INDEX IF NOT EXISTS ix_growth_seo_issue__schema_ref ON growth_seo_issue (tenant_id, company_id, schema_ref);  -- registry lookup
CREATE INDEX IF NOT EXISTS ix_growth_landing_page__scope_status_upd ON growth_landing_page (tenant_id, company_id, status, updated_at DESC);  -- V5 common physical design
CREATE INDEX IF NOT EXISTS ix_growth_landing_page__schema_ref ON growth_landing_page (tenant_id, company_id, schema_ref);  -- registry lookup
CREATE INDEX IF NOT EXISTS ix_growth_audience__scope_status_upd ON growth_audience (tenant_id, company_id, status, updated_at DESC);  -- V5 common physical design
CREATE INDEX IF NOT EXISTS ix_growth_audience__schema_ref ON growth_audience (tenant_id, company_id, schema_ref);  -- registry lookup
CREATE INDEX IF NOT EXISTS ix_growth_campaign__scope_status_upd ON growth_campaign (tenant_id, company_id, status, updated_at DESC);  -- V5 common physical design
CREATE INDEX IF NOT EXISTS ix_growth_campaign__schema_ref ON growth_campaign (tenant_id, company_id, schema_ref);  -- registry lookup
CREATE INDEX IF NOT EXISTS ix_growth_campaign_version__scope_status_upd ON growth_campaign_version (tenant_id, company_id, status, updated_at DESC);  -- V5 common physical design
CREATE INDEX IF NOT EXISTS ix_growth_campaign_version__schema_ref ON growth_campaign_version (tenant_id, company_id, schema_ref);  -- registry lookup
CREATE INDEX IF NOT EXISTS ix_growth_ad_campaign__scope_status_upd ON growth_ad_campaign (tenant_id, company_id, status, updated_at DESC);  -- V5 common physical design
CREATE INDEX IF NOT EXISTS ix_growth_ad_campaign__schema_ref ON growth_ad_campaign (tenant_id, company_id, schema_ref);  -- registry lookup
CREATE INDEX IF NOT EXISTS ix_growth_ad_spend_event__scope_status_upd ON growth_ad_spend_event (tenant_id, company_id, status, updated_at DESC);  -- V5 common physical design
CREATE INDEX IF NOT EXISTS ix_growth_ad_spend_event__schema_ref ON growth_ad_spend_event (tenant_id, company_id, schema_ref);  -- registry lookup
CREATE INDEX IF NOT EXISTS ix_growth_attribution_event__scope_status_upd ON growth_attribution_event (tenant_id, company_id, status, updated_at DESC);  -- V5 common physical design
CREATE INDEX IF NOT EXISTS ix_growth_attribution_event__schema_ref ON growth_attribution_event (tenant_id, company_id, schema_ref);  -- registry lookup
CREATE INDEX IF NOT EXISTS ix_growth_form__scope_status_upd ON growth_form (tenant_id, company_id, status, updated_at DESC);  -- V5 common physical design
CREATE INDEX IF NOT EXISTS ix_growth_form__schema_ref ON growth_form (tenant_id, company_id, schema_ref);  -- registry lookup
CREATE INDEX IF NOT EXISTS ix_growth_lead__scope_status_upd ON growth_lead (tenant_id, company_id, status, updated_at DESC);  -- V5 common physical design
CREATE INDEX IF NOT EXISTS ix_growth_lead__schema_ref ON growth_lead (tenant_id, company_id, schema_ref);  -- registry lookup
CREATE INDEX IF NOT EXISTS ix_growth_proposal__scope_status_upd ON growth_proposal (tenant_id, company_id, status, updated_at DESC);  -- V5 common physical design
CREATE INDEX IF NOT EXISTS ix_growth_proposal__schema_ref ON growth_proposal (tenant_id, company_id, schema_ref);  -- registry lookup
CREATE INDEX IF NOT EXISTS ix_growth_proposal_version__scope_status_upd ON growth_proposal_version (tenant_id, company_id, status, updated_at DESC);  -- V5 common physical design
CREATE INDEX IF NOT EXISTS ix_growth_proposal_version__schema_ref ON growth_proposal_version (tenant_id, company_id, schema_ref);  -- registry lookup
CREATE INDEX IF NOT EXISTS ix_growth_quote__scope_status_upd ON growth_quote (tenant_id, company_id, status, updated_at DESC);  -- V5 common physical design
CREATE INDEX IF NOT EXISTS ix_growth_quote__schema_ref ON growth_quote (tenant_id, company_id, schema_ref);  -- registry lookup
CREATE INDEX IF NOT EXISTS ix_growth_quote_line__scope_status_upd ON growth_quote_line (tenant_id, company_id, status, updated_at DESC);  -- V5 common physical design
CREATE INDEX IF NOT EXISTS ix_growth_quote_line__schema_ref ON growth_quote_line (tenant_id, company_id, schema_ref);  -- registry lookup
CREATE INDEX IF NOT EXISTS ix_growth_negotiation__scope_status_upd ON growth_negotiation (tenant_id, company_id, status, updated_at DESC);  -- V5 common physical design
CREATE INDEX IF NOT EXISTS ix_growth_negotiation__schema_ref ON growth_negotiation (tenant_id, company_id, schema_ref);  -- registry lookup
CREATE INDEX IF NOT EXISTS ix_growth_contract__scope_status_upd ON growth_contract (tenant_id, company_id, status, updated_at DESC);  -- V5 common physical design
CREATE INDEX IF NOT EXISTS ix_growth_contract__schema_ref ON growth_contract (tenant_id, company_id, schema_ref);  -- registry lookup
CREATE INDEX IF NOT EXISTS ix_growth_integration_deal__scope_status_upd ON growth_integration_deal (tenant_id, company_id, status, updated_at DESC);  -- V5 common physical design
CREATE INDEX IF NOT EXISTS ix_growth_integration_deal__schema_ref ON growth_integration_deal (tenant_id, company_id, schema_ref);  -- registry lookup
CREATE INDEX IF NOT EXISTS ix_sales_bid__scope_status_upd ON sales_bid (tenant_id, company_id, status, updated_at DESC);  -- V5 common physical design
CREATE INDEX IF NOT EXISTS ix_sales_bid__schema_ref ON sales_bid (tenant_id, company_id, schema_ref);  -- registry lookup
CREATE INDEX IF NOT EXISTS ix_growth_invoice__scope_status_upd ON growth_invoice (tenant_id, company_id, status, updated_at DESC);  -- V5 common physical design
CREATE INDEX IF NOT EXISTS ix_growth_invoice__schema_ref ON growth_invoice (tenant_id, company_id, schema_ref);  -- registry lookup
CREATE INDEX IF NOT EXISTS ix_growth_payment__scope_status_upd ON growth_payment (tenant_id, company_id, status, updated_at DESC);  -- V5 common physical design
CREATE INDEX IF NOT EXISTS ix_growth_payment__schema_ref ON growth_payment (tenant_id, company_id, schema_ref);  -- registry lookup
CREATE INDEX IF NOT EXISTS ix_sales_fulfillment__scope_status_upd ON sales_fulfillment (tenant_id, company_id, status, updated_at DESC);  -- V5 common physical design
CREATE INDEX IF NOT EXISTS ix_sales_fulfillment__schema_ref ON sales_fulfillment (tenant_id, company_id, schema_ref);  -- registry lookup
CREATE INDEX IF NOT EXISTS ix_sales_order__scope_status_upd ON sales_order (tenant_id, company_id, status, updated_at DESC);  -- V5 common physical design
CREATE INDEX IF NOT EXISTS ix_sales_order__schema_ref ON sales_order (tenant_id, company_id, schema_ref);  -- registry lookup
CREATE INDEX IF NOT EXISTS ix_sales_order_line__scope_status_upd ON sales_order_line (tenant_id, company_id, status, updated_at DESC);  -- V5 common physical design
CREATE INDEX IF NOT EXISTS ix_sales_order_line__schema_ref ON sales_order_line (tenant_id, company_id, schema_ref);  -- registry lookup
CREATE INDEX IF NOT EXISTS ix_growth_onboarding__scope_status_upd ON growth_onboarding (tenant_id, company_id, status, updated_at DESC);  -- V5 common physical design
CREATE INDEX IF NOT EXISTS ix_growth_onboarding__schema_ref ON growth_onboarding (tenant_id, company_id, schema_ref);  -- registry lookup
CREATE INDEX IF NOT EXISTS ix_growth_deployment__scope_status_upd ON growth_deployment (tenant_id, company_id, status, updated_at DESC);  -- V5 common physical design
CREATE INDEX IF NOT EXISTS ix_growth_deployment__schema_ref ON growth_deployment (tenant_id, company_id, schema_ref);  -- registry lookup
CREATE INDEX IF NOT EXISTS ix_growth_partner__scope_status_upd ON growth_partner (tenant_id, company_id, status, updated_at DESC);  -- V5 common physical design
CREATE INDEX IF NOT EXISTS ix_growth_partner__schema_ref ON growth_partner (tenant_id, company_id, schema_ref);  -- registry lookup
CREATE INDEX IF NOT EXISTS ix_growth_pilot__scope_status_upd ON growth_pilot (tenant_id, company_id, status, updated_at DESC);  -- V5 common physical design
CREATE INDEX IF NOT EXISTS ix_growth_pilot__schema_ref ON growth_pilot (tenant_id, company_id, schema_ref);  -- registry lookup
CREATE INDEX IF NOT EXISTS ix_growth_renewal__scope_status_upd ON growth_renewal (tenant_id, company_id, status, updated_at DESC);  -- V5 common physical design
CREATE INDEX IF NOT EXISTS ix_growth_renewal__schema_ref ON growth_renewal (tenant_id, company_id, schema_ref);  -- registry lookup
CREATE INDEX IF NOT EXISTS ix_growth_feedback__scope_status_upd ON growth_feedback (tenant_id, company_id, status, updated_at DESC);  -- V5 common physical design
CREATE INDEX IF NOT EXISTS ix_growth_feedback__schema_ref ON growth_feedback (tenant_id, company_id, schema_ref);  -- registry lookup
CREATE INDEX IF NOT EXISTS ix_growth_metric_snapshot__scope_status_upd ON growth_metric_snapshot (tenant_id, company_id, status, updated_at DESC);  -- V5 common physical design
CREATE INDEX IF NOT EXISTS ix_growth_metric_snapshot__schema_ref ON growth_metric_snapshot (tenant_id, company_id, schema_ref);  -- registry lookup
CREATE INDEX IF NOT EXISTS ix_growth_forecast__scope_status_upd ON growth_forecast (tenant_id, company_id, status, updated_at DESC);  -- V5 common physical design
CREATE INDEX IF NOT EXISTS ix_growth_forecast__schema_ref ON growth_forecast (tenant_id, company_id, schema_ref);  -- registry lookup
CREATE INDEX IF NOT EXISTS ix_growth_stage_metric__scope_status_upd ON growth_stage_metric (tenant_id, company_id, status, updated_at DESC);  -- V5 common physical design
CREATE INDEX IF NOT EXISTS ix_growth_stage_metric__schema_ref ON growth_stage_metric (tenant_id, company_id, schema_ref);  -- registry lookup
CREATE INDEX IF NOT EXISTS ix_growth_document__scope_status_upd ON growth_document (tenant_id, company_id, status, updated_at DESC);  -- V5 common physical design
CREATE INDEX IF NOT EXISTS ix_growth_document__schema_ref ON growth_document (tenant_id, company_id, schema_ref);  -- registry lookup
CREATE INDEX IF NOT EXISTS ix_growth_document_chunk__scope_status_upd ON growth_document_chunk (tenant_id, company_id, status, updated_at DESC);  -- V5 common physical design
CREATE INDEX IF NOT EXISTS ix_growth_document_chunk__schema_ref ON growth_document_chunk (tenant_id, company_id, schema_ref);  -- registry lookup
CREATE INDEX IF NOT EXISTS ix_growth_embedding__scope_status_upd ON growth_embedding (tenant_id, company_id, status, updated_at DESC);  -- V5 common physical design
CREATE INDEX IF NOT EXISTS ix_growth_embedding__schema_ref ON growth_embedding (tenant_id, company_id, schema_ref);  -- registry lookup
CREATE INDEX IF NOT EXISTS ixg_growth_signal__evidence_refs ON growth_signal USING gin (evidence_refs);  -- evidence lookup
CREATE INDEX IF NOT EXISTS ixg_growth_need__evidence_refs ON growth_need USING gin (evidence_refs);  -- evidence lookup
CREATE INDEX IF NOT EXISTS ixg_growth_opportunity__evidence_refs ON growth_opportunity USING gin (evidence_refs);  -- evidence lookup
CREATE INDEX IF NOT EXISTS ixg_growth_need_evidence__evidence_refs ON growth_need_evidence USING gin (evidence_refs);  -- evidence lookup
CREATE INDEX IF NOT EXISTS ixg_growth_claim__evidence_refs ON growth_claim USING gin (evidence_refs);  -- evidence lookup
CREATE INDEX IF NOT EXISTS ixg_growth_evidence__evidence_refs ON growth_evidence USING gin (evidence_refs);  -- evidence lookup
CREATE INDEX IF NOT EXISTS ixg_growth_market_event__evidence_refs ON growth_market_event USING gin (evidence_refs);  -- evidence lookup
CREATE INDEX IF NOT EXISTS ixg_growth_score_version__evidence_refs ON growth_score_version USING gin (evidence_refs);  -- evidence lookup
CREATE INDEX IF NOT EXISTS ixp_outbox__pending ON outbox (next_attempt_at, event_id) WHERE (published_at IS NULL);  -- dispatcher claim FOR UPDATE SKIP LOCKED
CREATE INDEX IF NOT EXISTS ix_workflow_run__scope_status ON workflow_run (tenant_id, company_id, status, created_at DESC);  -- live monitor
CREATE INDEX IF NOT EXISTS ixp_workflow_run__active ON workflow_run (tenant_id, company_id, created_at) WHERE (status IN ('Queued','Running','Awaiting approval','Held','Reconciling'));  -- queue
CREATE INDEX IF NOT EXISTS ixp_effect__open ON effect (tenant_id, company_id, status) WHERE (status IN ('Intended','Dispatched','Reconciling'));  -- reconciliation
CREATE INDEX IF NOT EXISTS ix_consent_record__current ON consent_record (tenant_id, company_id, contact_id, channel, purpose, captured_at DESC);  -- PDP consent lookup
CREATE INDEX IF NOT EXISTS ixp_dsar_request__open ON dsar_request (tenant_id, due_at) WHERE (status NOT IN ('Completed','Rejected'));  -- DSAR clock
CREATE INDEX IF NOT EXISTS ixb_audit_event__time ON audit_event USING brin (occurred_at);  -- time-range audit search
CREATE INDEX IF NOT EXISTS ix_audit_event__object ON audit_event (tenant_id, object_type, ref, occurred_at DESC);  -- object history
CREATE INDEX IF NOT EXISTS ixb_ai_usage_event__time ON ai_usage_event USING brin (occurred_at);  -- usage scans
CREATE INDEX IF NOT EXISTS ix_ai_usage_event__scope_time ON ai_usage_event (tenant_id, company_id, occurred_at);  -- cost per company per day
CREATE INDEX IF NOT EXISTS ixp_webhook_delivery__pending ON webhook_delivery (tenant_id, endpoint_id, signed_at) WHERE (delivered_at IS NULL);  -- retry worker
CREATE INDEX IF NOT EXISTS ixp_api_key__live ON api_key (tenant_id) WHERE (revoked_at IS NULL);  -- key listing
CREATE INDEX IF NOT EXISTS ixp_security_finding__open ON security_finding (severity, due_at) WHERE (closed_at IS NULL);  -- release gate KPI-03
CREATE INDEX IF NOT EXISTS ix_export_job__status ON export_job (tenant_id, status);  -- export queue
CREATE INDEX IF NOT EXISTS ix_business_event__time ON business_event (tenant_id, company_id, occurred_at);  -- KPI period scans
CREATE INDEX IF NOT EXISTS ixp_business_event__campaign ON business_event (tenant_id, company_id, campaign_id, occurred_at) WHERE (campaign_id IS NOT NULL);  -- attribution
CREATE INDEX IF NOT EXISTS ix_business_event__wf ON business_event (tenant_id, company_id, sku_id, wf_id, occurred_at);  -- service/workflow filter MT-27
CREATE INDEX IF NOT EXISTS ixp_incident_notification__due ON incident_notification (deadline_at) WHERE (notified_at IS NULL);  -- breach clock A121
CREATE INDEX IF NOT EXISTS ixp_inbox__unprocessed ON inbox (tenant_id, received_at) WHERE (processed_at IS NULL);  -- inbound processing
CREATE INDEX IF NOT EXISTS ixp_portfolio_grant__live ON portfolio_grant (tenant_id, portfolio_id) WHERE (revoked_at IS NULL);  -- portfolio scope
CREATE INDEX IF NOT EXISTS ix_jurisdiction_pack__status ON jurisdiction_pack (jurisdiction, status);  -- PDP pack lookup
CREATE INDEX IF NOT EXISTS ix_metric_aggregate__lookup ON metric_aggregate (tenant_id, company_id, metric_id, period_start);  -- dashboard
CREATE TRIGGER trg_growth_source_validate BEFORE INSERT OR UPDATE ON growth_source FOR EACH ROW EXECUTE FUNCTION fn_validate_domain_row();
CREATE TRIGGER trg_growth_source_policy_validate BEFORE INSERT OR UPDATE ON growth_source_policy FOR EACH ROW EXECUTE FUNCTION fn_validate_domain_row();
CREATE TRIGGER trg_growth_source_record_validate BEFORE INSERT OR UPDATE ON growth_source_record FOR EACH ROW EXECUTE FUNCTION fn_validate_domain_row();
CREATE TRIGGER trg_growth_evidence_validate BEFORE INSERT OR UPDATE ON growth_evidence FOR EACH ROW EXECUTE FUNCTION fn_validate_domain_row();
CREATE TRIGGER trg_growth_competitor_validate BEFORE INSERT OR UPDATE ON growth_competitor FOR EACH ROW EXECUTE FUNCTION fn_validate_domain_row();
CREATE TRIGGER trg_growth_market_event_validate BEFORE INSERT OR UPDATE ON growth_market_event FOR EACH ROW EXECUTE FUNCTION fn_validate_domain_row();
CREATE TRIGGER trg_growth_search_plan_validate BEFORE INSERT OR UPDATE ON growth_search_plan FOR EACH ROW EXECUTE FUNCTION fn_validate_domain_row();
CREATE TRIGGER trg_growth_organization_validate BEFORE INSERT OR UPDATE ON growth_organization FOR EACH ROW EXECUTE FUNCTION fn_validate_domain_row();
CREATE TRIGGER trg_growth_signal_validate BEFORE INSERT OR UPDATE ON growth_signal FOR EACH ROW EXECUTE FUNCTION fn_validate_domain_row();
CREATE TRIGGER trg_growth_signal_type_validate BEFORE INSERT OR UPDATE ON growth_signal_type FOR EACH ROW EXECUTE FUNCTION fn_validate_domain_row();
CREATE TRIGGER trg_growth_need_evidence_validate BEFORE INSERT OR UPDATE ON growth_need_evidence FOR EACH ROW EXECUTE FUNCTION fn_validate_domain_row();
CREATE TRIGGER trg_growth_referral_validate BEFORE INSERT OR UPDATE ON growth_referral FOR EACH ROW EXECUTE FUNCTION fn_validate_domain_row();
CREATE TRIGGER trg_growth_contact_validate BEFORE INSERT OR UPDATE ON growth_contact FOR EACH ROW EXECUTE FUNCTION fn_validate_domain_row();
CREATE TRIGGER trg_growth_contact_source_validate BEFORE INSERT OR UPDATE ON growth_contact_source FOR EACH ROW EXECUTE FUNCTION fn_validate_domain_row();
CREATE TRIGGER trg_growth_contact_verification_validate BEFORE INSERT OR UPDATE ON growth_contact_verification FOR EACH ROW EXECUTE FUNCTION fn_validate_domain_row();
CREATE TRIGGER trg_growth_consent_validate BEFORE INSERT OR UPDATE ON growth_consent FOR EACH ROW EXECUTE FUNCTION fn_validate_domain_row();
CREATE TRIGGER trg_growth_suppression_validate BEFORE INSERT OR UPDATE ON growth_suppression FOR EACH ROW EXECUTE FUNCTION fn_validate_domain_row();
CREATE TRIGGER trg_growth_need_validate BEFORE INSERT OR UPDATE ON growth_need FOR EACH ROW EXECUTE FUNCTION fn_validate_domain_row();
CREATE TRIGGER trg_growth_product_validate BEFORE INSERT OR UPDATE ON growth_product FOR EACH ROW EXECUTE FUNCTION fn_validate_domain_row();
CREATE TRIGGER trg_growth_opportunity_validate BEFORE INSERT OR UPDATE ON growth_opportunity FOR EACH ROW EXECUTE FUNCTION fn_validate_domain_row();
CREATE TRIGGER trg_growth_score_version_validate BEFORE INSERT OR UPDATE ON growth_score_version FOR EACH ROW EXECUTE FUNCTION fn_validate_domain_row();
CREATE TRIGGER trg_growth_activity_validate BEFORE INSERT OR UPDATE ON growth_activity FOR EACH ROW EXECUTE FUNCTION fn_validate_domain_row();
CREATE TRIGGER trg_growth_deal_validate BEFORE INSERT OR UPDATE ON growth_deal FOR EACH ROW EXECUTE FUNCTION fn_validate_domain_row();
CREATE TRIGGER trg_growth_stage_validate BEFORE INSERT OR UPDATE ON growth_stage FOR EACH ROW EXECUTE FUNCTION fn_validate_domain_row();
CREATE TRIGGER trg_growth_task_validate BEFORE INSERT OR UPDATE ON growth_task FOR EACH ROW EXECUTE FUNCTION fn_validate_domain_row();
CREATE TRIGGER trg_growth_budget_validate BEFORE INSERT OR UPDATE ON growth_budget FOR EACH ROW EXECUTE FUNCTION fn_validate_domain_row();
CREATE TRIGGER trg_growth_message_validate BEFORE INSERT OR UPDATE ON growth_message FOR EACH ROW EXECUTE FUNCTION fn_validate_domain_row();
CREATE TRIGGER trg_growth_message_draft_validate BEFORE INSERT OR UPDATE ON growth_message_draft FOR EACH ROW EXECUTE FUNCTION fn_validate_domain_row();
CREATE TRIGGER trg_growth_message_template_validate BEFORE INSERT OR UPDATE ON growth_message_template FOR EACH ROW EXECUTE FUNCTION fn_validate_domain_row();
CREATE TRIGGER trg_growth_outbox_validate BEFORE INSERT OR UPDATE ON growth_outbox FOR EACH ROW EXECUTE FUNCTION fn_validate_domain_row();
CREATE TRIGGER trg_growth_delivery_event_validate BEFORE INSERT OR UPDATE ON growth_delivery_event FOR EACH ROW EXECUTE FUNCTION fn_validate_domain_row();
CREATE TRIGGER trg_growth_thread_validate BEFORE INSERT OR UPDATE ON growth_thread FOR EACH ROW EXECUTE FUNCTION fn_validate_domain_row();
CREATE TRIGGER trg_growth_channel_account_validate BEFORE INSERT OR UPDATE ON growth_channel_account FOR EACH ROW EXECUTE FUNCTION fn_validate_domain_row();
CREATE TRIGGER trg_growth_inbound_event_validate BEFORE INSERT OR UPDATE ON growth_inbound_event FOR EACH ROW EXECUTE FUNCTION fn_validate_domain_row();
CREATE TRIGGER trg_growth_enrollment_validate BEFORE INSERT OR UPDATE ON growth_enrollment FOR EACH ROW EXECUTE FUNCTION fn_validate_domain_row();
CREATE TRIGGER trg_growth_sequence_validate BEFORE INSERT OR UPDATE ON growth_sequence FOR EACH ROW EXECUTE FUNCTION fn_validate_domain_row();
CREATE TRIGGER trg_growth_sequence_step_validate BEFORE INSERT OR UPDATE ON growth_sequence_step FOR EACH ROW EXECUTE FUNCTION fn_validate_domain_row();
CREATE TRIGGER trg_growth_routing_rule_validate BEFORE INSERT OR UPDATE ON growth_routing_rule FOR EACH ROW EXECUTE FUNCTION fn_validate_domain_row();
CREATE TRIGGER trg_growth_workflow_execution_validate BEFORE INSERT OR UPDATE ON growth_workflow_execution FOR EACH ROW EXECUTE FUNCTION fn_validate_domain_row();
CREATE TRIGGER trg_growth_identity_link_validate BEFORE INSERT OR UPDATE ON growth_identity_link FOR EACH ROW EXECUTE FUNCTION fn_validate_domain_row();
CREATE TRIGGER trg_growth_objection_validate BEFORE INSERT OR UPDATE ON growth_objection FOR EACH ROW EXECUTE FUNCTION fn_validate_domain_row();
CREATE TRIGGER trg_growth_calendar_link_validate BEFORE INSERT OR UPDATE ON growth_calendar_link FOR EACH ROW EXECUTE FUNCTION fn_validate_domain_row();
CREATE TRIGGER trg_growth_meeting_validate BEFORE INSERT OR UPDATE ON growth_meeting FOR EACH ROW EXECUTE FUNCTION fn_validate_domain_row();
CREATE TRIGGER trg_growth_business_event_validate BEFORE INSERT OR UPDATE ON growth_business_event FOR EACH ROW EXECUTE FUNCTION fn_validate_domain_row();
CREATE TRIGGER trg_growth_event_attendance_validate BEFORE INSERT OR UPDATE ON growth_event_attendance FOR EACH ROW EXECUTE FUNCTION fn_validate_domain_row();
CREATE TRIGGER trg_growth_event_registration_validate BEFORE INSERT OR UPDATE ON growth_event_registration FOR EACH ROW EXECUTE FUNCTION fn_validate_domain_row();
CREATE TRIGGER trg_growth_claim_validate BEFORE INSERT OR UPDATE ON growth_claim FOR EACH ROW EXECUTE FUNCTION fn_validate_domain_row();
CREATE TRIGGER trg_growth_content_asset_validate BEFORE INSERT OR UPDATE ON growth_content_asset FOR EACH ROW EXECUTE FUNCTION fn_validate_domain_row();
CREATE TRIGGER trg_growth_content_version_validate BEFORE INSERT OR UPDATE ON growth_content_version FOR EACH ROW EXECUTE FUNCTION fn_validate_domain_row();
CREATE TRIGGER trg_growth_approval_validate BEFORE INSERT OR UPDATE ON growth_approval FOR EACH ROW EXECUTE FUNCTION fn_validate_domain_row();
CREATE TRIGGER trg_growth_social_post_validate BEFORE INSERT OR UPDATE ON growth_social_post FOR EACH ROW EXECUTE FUNCTION fn_validate_domain_row();
CREATE TRIGGER trg_growth_social_publication_validate BEFORE INSERT OR UPDATE ON growth_social_publication FOR EACH ROW EXECUTE FUNCTION fn_validate_domain_row();
CREATE TRIGGER trg_growth_keyword_validate BEFORE INSERT OR UPDATE ON growth_keyword FOR EACH ROW EXECUTE FUNCTION fn_validate_domain_row();
CREATE TRIGGER trg_growth_page_metric_validate BEFORE INSERT OR UPDATE ON growth_page_metric FOR EACH ROW EXECUTE FUNCTION fn_validate_domain_row();
CREATE TRIGGER trg_growth_seo_issue_validate BEFORE INSERT OR UPDATE ON growth_seo_issue FOR EACH ROW EXECUTE FUNCTION fn_validate_domain_row();
CREATE TRIGGER trg_growth_landing_page_validate BEFORE INSERT OR UPDATE ON growth_landing_page FOR EACH ROW EXECUTE FUNCTION fn_validate_domain_row();
CREATE TRIGGER trg_growth_audience_validate BEFORE INSERT OR UPDATE ON growth_audience FOR EACH ROW EXECUTE FUNCTION fn_validate_domain_row();
CREATE TRIGGER trg_growth_campaign_validate BEFORE INSERT OR UPDATE ON growth_campaign FOR EACH ROW EXECUTE FUNCTION fn_validate_domain_row();
CREATE TRIGGER trg_growth_campaign_version_validate BEFORE INSERT OR UPDATE ON growth_campaign_version FOR EACH ROW EXECUTE FUNCTION fn_validate_domain_row();
CREATE TRIGGER trg_growth_ad_campaign_validate BEFORE INSERT OR UPDATE ON growth_ad_campaign FOR EACH ROW EXECUTE FUNCTION fn_validate_domain_row();
CREATE TRIGGER trg_growth_ad_spend_event_validate BEFORE INSERT OR UPDATE ON growth_ad_spend_event FOR EACH ROW EXECUTE FUNCTION fn_validate_domain_row();
CREATE TRIGGER trg_growth_attribution_event_validate BEFORE INSERT OR UPDATE ON growth_attribution_event FOR EACH ROW EXECUTE FUNCTION fn_validate_domain_row();
CREATE TRIGGER trg_growth_form_validate BEFORE INSERT OR UPDATE ON growth_form FOR EACH ROW EXECUTE FUNCTION fn_validate_domain_row();
CREATE TRIGGER trg_growth_lead_validate BEFORE INSERT OR UPDATE ON growth_lead FOR EACH ROW EXECUTE FUNCTION fn_validate_domain_row();
CREATE TRIGGER trg_growth_proposal_validate BEFORE INSERT OR UPDATE ON growth_proposal FOR EACH ROW EXECUTE FUNCTION fn_validate_domain_row();
CREATE TRIGGER trg_growth_proposal_version_validate BEFORE INSERT OR UPDATE ON growth_proposal_version FOR EACH ROW EXECUTE FUNCTION fn_validate_domain_row();
CREATE TRIGGER trg_growth_quote_validate BEFORE INSERT OR UPDATE ON growth_quote FOR EACH ROW EXECUTE FUNCTION fn_validate_domain_row();
CREATE TRIGGER trg_growth_quote_line_validate BEFORE INSERT OR UPDATE ON growth_quote_line FOR EACH ROW EXECUTE FUNCTION fn_validate_domain_row();
CREATE TRIGGER trg_growth_negotiation_validate BEFORE INSERT OR UPDATE ON growth_negotiation FOR EACH ROW EXECUTE FUNCTION fn_validate_domain_row();
CREATE TRIGGER trg_growth_contract_validate BEFORE INSERT OR UPDATE ON growth_contract FOR EACH ROW EXECUTE FUNCTION fn_validate_domain_row();
CREATE TRIGGER trg_growth_integration_deal_validate BEFORE INSERT OR UPDATE ON growth_integration_deal FOR EACH ROW EXECUTE FUNCTION fn_validate_domain_row();
CREATE TRIGGER trg_sales_bid_validate BEFORE INSERT OR UPDATE ON sales_bid FOR EACH ROW EXECUTE FUNCTION fn_validate_domain_row();
CREATE TRIGGER trg_growth_invoice_validate BEFORE INSERT OR UPDATE ON growth_invoice FOR EACH ROW EXECUTE FUNCTION fn_validate_domain_row();
CREATE TRIGGER trg_growth_payment_validate BEFORE INSERT OR UPDATE ON growth_payment FOR EACH ROW EXECUTE FUNCTION fn_validate_domain_row();
CREATE TRIGGER trg_sales_fulfillment_validate BEFORE INSERT OR UPDATE ON sales_fulfillment FOR EACH ROW EXECUTE FUNCTION fn_validate_domain_row();
CREATE TRIGGER trg_sales_order_validate BEFORE INSERT OR UPDATE ON sales_order FOR EACH ROW EXECUTE FUNCTION fn_validate_domain_row();
CREATE TRIGGER trg_sales_order_line_validate BEFORE INSERT OR UPDATE ON sales_order_line FOR EACH ROW EXECUTE FUNCTION fn_validate_domain_row();
CREATE TRIGGER trg_growth_onboarding_validate BEFORE INSERT OR UPDATE ON growth_onboarding FOR EACH ROW EXECUTE FUNCTION fn_validate_domain_row();
CREATE TRIGGER trg_growth_deployment_validate BEFORE INSERT OR UPDATE ON growth_deployment FOR EACH ROW EXECUTE FUNCTION fn_validate_domain_row();
CREATE TRIGGER trg_growth_partner_validate BEFORE INSERT OR UPDATE ON growth_partner FOR EACH ROW EXECUTE FUNCTION fn_validate_domain_row();
CREATE TRIGGER trg_growth_pilot_validate BEFORE INSERT OR UPDATE ON growth_pilot FOR EACH ROW EXECUTE FUNCTION fn_validate_domain_row();
CREATE TRIGGER trg_growth_renewal_validate BEFORE INSERT OR UPDATE ON growth_renewal FOR EACH ROW EXECUTE FUNCTION fn_validate_domain_row();
CREATE TRIGGER trg_growth_feedback_validate BEFORE INSERT OR UPDATE ON growth_feedback FOR EACH ROW EXECUTE FUNCTION fn_validate_domain_row();
CREATE TRIGGER trg_growth_metric_snapshot_validate BEFORE INSERT OR UPDATE ON growth_metric_snapshot FOR EACH ROW EXECUTE FUNCTION fn_validate_domain_row();
CREATE TRIGGER trg_growth_forecast_validate BEFORE INSERT OR UPDATE ON growth_forecast FOR EACH ROW EXECUTE FUNCTION fn_validate_domain_row();
CREATE TRIGGER trg_growth_stage_metric_validate BEFORE INSERT OR UPDATE ON growth_stage_metric FOR EACH ROW EXECUTE FUNCTION fn_validate_domain_row();
CREATE TRIGGER trg_growth_document_validate BEFORE INSERT OR UPDATE ON growth_document FOR EACH ROW EXECUTE FUNCTION fn_validate_domain_row();
CREATE TRIGGER trg_growth_document_chunk_validate BEFORE INSERT OR UPDATE ON growth_document_chunk FOR EACH ROW EXECUTE FUNCTION fn_validate_domain_row();
CREATE TRIGGER trg_growth_embedding_validate BEFORE INSERT OR UPDATE ON growth_embedding FOR EACH ROW EXECUTE FUNCTION fn_validate_domain_row();
