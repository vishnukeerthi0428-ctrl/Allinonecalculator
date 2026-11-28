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
