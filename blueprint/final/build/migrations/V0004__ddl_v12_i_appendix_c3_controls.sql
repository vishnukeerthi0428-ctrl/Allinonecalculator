-- V0004__ddl_v12_i_appendix_c3_controls
SET search_path = ge, extensions, public;

SELECT set_config('app.zone', coalesce(nullif(current_setting('app.deployment_region', true), ''), 'IN'), false);

SELECT set_config('app.deployment_region', coalesce(nullif(current_setting('app.deployment_region', true), ''), 'IN'), false);

DO $$ BEGIN
  IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname='anon') THEN CREATE ROLE anon NOLOGIN; END IF;
  IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname='authenticated') THEN CREATE ROLE authenticated NOLOGIN; END IF;
  IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname='app_owner') THEN CREATE ROLE app_owner NOLOGIN NOBYPASSRLS; END IF;
  IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname='app_rw') THEN CREATE ROLE app_rw NOLOGIN NOBYPASSRLS; END IF;          -- LOGIN in production via Supavisor
  IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname='app_worker') THEN CREATE ROLE app_worker NOLOGIN NOBYPASSRLS; END IF;
  IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname='app_readonly') THEN CREATE ROLE app_readonly NOLOGIN NOBYPASSRLS; END IF;
  IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname='app_retention') THEN CREATE ROLE app_retention NOLOGIN NOBYPASSRLS; END IF;
  IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname='app_audit_writer') THEN CREATE ROLE app_audit_writer NOLOGIN NOBYPASSRLS; END IF;
  IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname='app_platform_sec') THEN CREATE ROLE app_platform_sec NOLOGIN NOBYPASSRLS; END IF;
END $$;

REVOKE ALL ON ALL TABLES IN SCHEMA ge FROM PUBLIC, anon, authenticated;

REVOKE ALL ON ALL SEQUENCES IN SCHEMA ge FROM PUBLIC, anon, authenticated;

REVOKE ALL ON ALL FUNCTIONS IN SCHEMA ge FROM PUBLIC, anon, authenticated;

ALTER DEFAULT PRIVILEGES IN SCHEMA ge REVOKE ALL ON TABLES FROM PUBLIC, anon, authenticated;

ALTER DEFAULT PRIVILEGES IN SCHEMA ge REVOKE EXECUTE ON FUNCTIONS FROM PUBLIC, anon, authenticated;

GRANT USAGE ON SCHEMA ge TO app_rw, app_worker, app_readonly, app_retention, app_audit_writer, app_platform_sec;

GRANT EXECUTE ON FUNCTION digest(bytea, text), digest(text, text), hmac(bytea, bytea, text), gen_random_bytes(int) TO app_rw, app_worker;

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
  TO app_rw, app_worker, app_readonly, app_retention, app_audit_writer;

ALTER TABLE outbox ALTER COLUMN tenant_id SET NOT NULL;

ALTER TABLE portfolio_grant ALTER COLUMN tenant_id SET NOT NULL, ALTER COLUMN company_id SET NOT NULL, ALTER COLUMN portfolio_id SET NOT NULL;

ALTER TABLE portfolio_grant ADD CONSTRAINT portfolio_grant_company_fk FOREIGN KEY (tenant_id, company_id) REFERENCES company(tenant_id, company_id);

ALTER TABLE portfolio_grant ADD CONSTRAINT portfolio_grant_no_wildcard CHECK (cardinality(dimensions) > 0 AND NOT ('*' = ANY (dimensions)));

ALTER TABLE portfolio_grant ADD CONSTRAINT portfolio_grant_expiry_required CHECK (expires_at IS NOT NULL);

ALTER TABLE custom_role ADD CONSTRAINT custom_role_tenant_role_uq UNIQUE (tenant_id, role_id);

ALTER TABLE role_permission DROP CONSTRAINT role_permission_role_id_fkey;

ALTER TABLE role_permission DROP CONSTRAINT role_permission_pkey;

ALTER TABLE role_permission ADD CONSTRAINT role_permission_pkey PRIMARY KEY (tenant_id, role_id, permission);

ALTER TABLE role_permission ADD CONSTRAINT role_permission_role_fk FOREIGN KEY (tenant_id, role_id) REFERENCES custom_role(tenant_id, role_id);

ALTER TABLE role_permission ADD CONSTRAINT role_permission_format CHECK (permission ~ '^[A-Z][A-Za-z]+:[a-z]+$');

ALTER TABLE webhook_endpoint ADD CONSTRAINT webhook_endpoint_tenant_uq UNIQUE (tenant_id, endpoint_id);

ALTER TABLE webhook_delivery DROP CONSTRAINT webhook_delivery_endpoint_id_fkey;

ALTER TABLE webhook_delivery ADD CONSTRAINT webhook_delivery_endpoint_fk FOREIGN KEY (tenant_id, endpoint_id) REFERENCES webhook_endpoint(tenant_id, endpoint_id);

ALTER TABLE sandbox_environment ADD CONSTRAINT sandbox_environment_tenant_uq UNIQUE (tenant_id, sandbox_id);

ALTER TABLE config_promotion DROP CONSTRAINT config_promotion_sandbox_id_fkey;

ALTER TABLE config_promotion ADD CONSTRAINT config_promotion_sandbox_fk FOREIGN KEY (tenant_id, sandbox_id) REFERENCES sandbox_environment(tenant_id, sandbox_id);

ALTER TABLE workflow_run ADD CONSTRAINT workflow_run_company_run_uq UNIQUE (tenant_id, company_id, run_id);

ALTER TABLE workflow_step_run ADD COLUMN IF NOT EXISTS company_id uuid;

ALTER TABLE effect ADD COLUMN IF NOT EXISTS company_id uuid;

ALTER TABLE effect ADD CONSTRAINT effect_run_fk FOREIGN KEY (tenant_id, company_id, run_id) REFERENCES workflow_run(tenant_id, company_id, run_id);

ALTER TABLE workflow_step_run ADD CONSTRAINT workflow_step_run_company_fk FOREIGN KEY (tenant_id, company_id, run_id) REFERENCES workflow_run(tenant_id, company_id, run_id);

ALTER TABLE workflow_step_run ALTER COLUMN company_id SET NOT NULL;

ALTER TABLE effect ALTER COLUMN company_id SET NOT NULL;

ALTER TABLE consent_record ALTER COLUMN company_id SET NOT NULL;

ALTER TABLE outbox ADD COLUMN IF NOT EXISTS company_id uuid;

ALTER TABLE outbox ADD COLUMN IF NOT EXISTS dedup_key text;

ALTER TABLE outbox ADD COLUMN IF NOT EXISTS correlation_id uuid;

ALTER TABLE outbox ADD COLUMN IF NOT EXISTS attempts int NOT NULL DEFAULT 0 CHECK (attempts BETWEEN 0 AND 20);

ALTER TABLE outbox ADD COLUMN IF NOT EXISTS next_attempt_at timestamptz NOT NULL DEFAULT now();

ALTER TABLE outbox ADD CONSTRAINT outbox_dedup_uq UNIQUE (tenant_id, dedup_key);

ALTER TABLE inbox ADD COLUMN IF NOT EXISTS provider_account text NOT NULL DEFAULT 'unknown';

ALTER TABLE inbox DROP CONSTRAINT inbox_pkey;

ALTER TABLE inbox ADD CONSTRAINT inbox_pkey PRIMARY KEY (provider, provider_account, provider_event_id);

ALTER TABLE inbox ADD CONSTRAINT inbox_signature_required CHECK (signature_ok);

ALTER TABLE inbox ADD COLUMN IF NOT EXISTS payload_ref text;

ALTER TABLE inbox ADD COLUMN IF NOT EXISTS processed_at timestamptz;

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

CREATE OR REPLACE FUNCTION fn_forbid_mutation() RETURNS trigger LANGUAGE plpgsql AS $$
BEGIN
  IF current_user = 'app_retention' AND current_setting('app.retention_run_id', true) IS NOT NULL
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
  p_policy_version text, p_correlation uuid, p_payload jsonb) RETURNS bigint LANGUAGE plpgsql SECURITY DEFINER SET search_path = ge, extensions, public, pg_temp AS $$
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

GRANT EXECUTE ON FUNCTION fn_append_audit(uuid,uuid,text,text,text,text,uuid,jsonb) TO app_rw, app_worker;

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
  CHECK (winner_arm IS NULL OR (decided_by IS NOT NULL AND decided_by <> created_by AND status = 'Concluded')));

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

ALTER TABLE inbox ALTER COLUMN tenant_id SET NOT NULL;

GRANT SELECT, INSERT, UPDATE ON tenant TO app_rw, app_worker;

GRANT SELECT ON tenant TO app_readonly;

GRANT SELECT, INSERT, UPDATE ON organization TO app_rw, app_worker;

GRANT SELECT ON organization TO app_readonly;

GRANT SELECT, INSERT, UPDATE ON company TO app_rw, app_worker;

GRANT SELECT ON company TO app_readonly;

GRANT SELECT, INSERT, UPDATE ON division TO app_rw, app_worker;

GRANT SELECT ON division TO app_readonly;

GRANT SELECT, INSERT, UPDATE ON brand TO app_rw, app_worker;

GRANT SELECT ON brand TO app_readonly;

GRANT SELECT, INSERT, UPDATE ON offering TO app_rw, app_worker;

GRANT SELECT ON offering TO app_readonly;

GRANT SELECT, INSERT, UPDATE ON market TO app_rw, app_worker;

GRANT SELECT ON market TO app_readonly;

GRANT SELECT, INSERT, UPDATE ON channel_account TO app_rw, app_worker;

GRANT SELECT ON channel_account TO app_readonly;

GRANT SELECT, INSERT, UPDATE ON workflow_run TO app_rw, app_worker;

GRANT SELECT ON workflow_run TO app_readonly;

GRANT SELECT, INSERT, UPDATE ON workflow_step_run TO app_rw, app_worker;

GRANT SELECT ON workflow_step_run TO app_readonly;

GRANT SELECT, INSERT, UPDATE ON effect TO app_rw, app_worker;

GRANT SELECT ON effect TO app_readonly;

GRANT SELECT, INSERT, UPDATE ON outbox TO app_rw, app_worker;

GRANT SELECT ON outbox TO app_readonly;

GRANT SELECT, INSERT, UPDATE ON inbox TO app_rw, app_worker;

GRANT SELECT ON inbox TO app_readonly;

GRANT SELECT ON audit_event TO app_rw, app_worker, app_readonly;

GRANT SELECT, INSERT, UPDATE ON portfolio_grant TO app_rw, app_worker;

GRANT SELECT ON portfolio_grant TO app_readonly;

GRANT SELECT ON fx_rate TO app_rw, app_worker, app_readonly;

GRANT SELECT ON jurisdiction_pack TO app_rw, app_worker, app_readonly;

GRANT SELECT ON jurisdiction_rule TO app_rw, app_worker, app_readonly;

GRANT SELECT, INSERT ON consent_record TO app_rw, app_worker;

GRANT SELECT ON consent_record TO app_readonly;

GRANT SELECT, INSERT, UPDATE ON suppression TO app_rw, app_worker;

GRANT SELECT ON suppression TO app_readonly;

GRANT SELECT, INSERT, UPDATE ON dsar_request TO app_rw, app_worker;

GRANT SELECT ON dsar_request TO app_readonly;

GRANT SELECT, INSERT, UPDATE ON incident TO app_rw, app_worker;

GRANT SELECT ON incident TO app_readonly;

GRANT SELECT ON incident_notification TO app_rw, app_worker, app_readonly;

GRANT SELECT, INSERT, UPDATE ON incident_notification TO app_platform_sec;

GRANT SELECT ON ai_model TO app_rw, app_worker, app_readonly;

GRANT SELECT ON prompt_version TO app_rw, app_worker, app_readonly;

GRANT SELECT ON eval_suite TO app_rw, app_worker, app_readonly;

GRANT SELECT ON eval_run TO app_rw, app_worker, app_readonly;

GRANT SELECT, INSERT ON ai_usage_event TO app_rw, app_worker;

GRANT SELECT ON ai_usage_event TO app_readonly;

GRANT SELECT, INSERT, UPDATE ON ai_budget TO app_rw, app_worker;

GRANT SELECT ON ai_budget TO app_readonly;

GRANT SELECT, INSERT, UPDATE ON identity_provider TO app_rw, app_worker;

GRANT SELECT, INSERT, UPDATE ON scim_token TO app_rw, app_worker;

GRANT SELECT, INSERT, UPDATE ON custom_role TO app_rw, app_worker;

GRANT SELECT ON custom_role TO app_readonly;

GRANT SELECT, INSERT, UPDATE ON role_permission TO app_rw, app_worker;

GRANT SELECT ON role_permission TO app_readonly;

GRANT SELECT ON sod_conflict TO app_rw, app_worker, app_readonly;

GRANT SELECT, INSERT, UPDATE ON api_key TO app_rw, app_worker;

GRANT SELECT, INSERT, UPDATE ON webhook_endpoint TO app_rw, app_worker;

GRANT SELECT ON webhook_endpoint TO app_readonly;

GRANT SELECT, INSERT, UPDATE ON webhook_delivery TO app_rw, app_worker;

GRANT SELECT ON webhook_delivery TO app_readonly;

GRANT SELECT, INSERT, UPDATE ON audit_sink TO app_rw, app_worker;

GRANT SELECT ON audit_sink TO app_readonly;

GRANT SELECT, INSERT, UPDATE ON export_job TO app_rw, app_worker;

GRANT SELECT ON export_job TO app_readonly;

GRANT SELECT, INSERT, UPDATE ON tenant_key_config TO app_rw, app_worker;

GRANT SELECT, INSERT, UPDATE ON sandbox_environment TO app_rw, app_worker;

GRANT SELECT ON sandbox_environment TO app_readonly;

GRANT SELECT, INSERT, UPDATE ON config_promotion TO app_rw, app_worker;

GRANT SELECT ON config_promotion TO app_readonly;

GRANT SELECT, INSERT, UPDATE ON connector_installation TO app_rw, app_worker;

GRANT SELECT ON connector_installation TO app_readonly;

GRANT SELECT ON security_finding TO app_platform_sec;

GRANT SELECT, INSERT, UPDATE ON security_finding TO app_platform_sec;

GRANT SELECT ON ops_incident TO app_rw, app_worker, app_readonly;

GRANT SELECT, INSERT, UPDATE ON ops_incident TO app_platform_sec;

GRANT SELECT ON tax_rule TO app_rw, app_worker, app_readonly;

GRANT SELECT, INSERT, UPDATE ON invoice TO app_rw, app_worker;

GRANT SELECT ON invoice TO app_readonly;

GRANT SELECT ON locale_bundle TO app_rw, app_worker, app_readonly;

GRANT SELECT, INSERT, UPDATE ON user_role_assignment TO app_rw, app_worker;

GRANT SELECT ON user_role_assignment TO app_readonly;

GRANT SELECT, INSERT, UPDATE ON tenant_data_key TO app_rw, app_worker;

GRANT SELECT ON domain_schema_registry TO app_rw, app_worker, app_readonly;

GRANT SELECT, INSERT, UPDATE ON company_operating_country TO app_rw, app_worker;

GRANT SELECT ON company_operating_country TO app_readonly;

GRANT SELECT, INSERT, UPDATE ON offering_market TO app_rw, app_worker;

GRANT SELECT ON offering_market TO app_readonly;

GRANT SELECT, INSERT, UPDATE ON channel_account_market TO app_rw, app_worker;

GRANT SELECT ON channel_account_market TO app_readonly;

GRANT SELECT, INSERT, UPDATE ON configuration_revision TO app_rw, app_worker;

GRANT SELECT ON configuration_revision TO app_readonly;

GRANT SELECT, INSERT, UPDATE ON workflow_configuration TO app_rw, app_worker;

GRANT SELECT ON workflow_configuration TO app_readonly;

GRANT SELECT, INSERT ON business_event TO app_rw, app_worker;

GRANT SELECT ON business_event TO app_readonly;

GRANT SELECT ON metric_definition TO app_rw, app_worker, app_readonly;

GRANT SELECT, INSERT, UPDATE ON metric_aggregate TO app_rw, app_worker;

GRANT SELECT ON metric_aggregate TO app_readonly;

GRANT SELECT, INSERT, UPDATE ON experiment TO app_rw, app_worker;

GRANT SELECT ON experiment TO app_readonly;

GRANT SELECT, INSERT, UPDATE ON feedback_case TO app_rw, app_worker;

GRANT SELECT ON feedback_case TO app_readonly;

GRANT SELECT ON sli_sample TO app_rw, app_worker, app_readonly;

GRANT SELECT, INSERT, UPDATE ON customer_value TO app_rw, app_worker;

GRANT SELECT ON customer_value TO app_readonly;

GRANT SELECT, INSERT, UPDATE ON journey_event TO app_rw, app_worker;

GRANT SELECT ON journey_event TO app_readonly;

GRANT SELECT, INSERT ON domain_record_version TO app_rw, app_worker;

GRANT SELECT ON domain_record_version TO app_readonly;

GRANT SELECT, INSERT, UPDATE ON usage_reservation TO app_rw, app_worker;

GRANT SELECT ON usage_reservation TO app_readonly;

GRANT USAGE ON ALL SEQUENCES IN SCHEMA ge TO app_rw, app_worker;

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

ALTER TABLE tenant ENABLE ROW LEVEL SECURITY;

ALTER TABLE tenant FORCE ROW LEVEL SECURITY;

CREATE POLICY rls_tenant__select ON tenant FOR SELECT USING (tenant_id = (SELECT app_tenant()));

ALTER TABLE organization ENABLE ROW LEVEL SECURITY;

ALTER TABLE organization FORCE ROW LEVEL SECURITY;

CREATE POLICY rls_organization__select ON organization FOR SELECT USING (tenant_id = (SELECT app_tenant()));

CREATE POLICY rls_organization__insert ON organization FOR INSERT WITH CHECK (tenant_id = (SELECT app_tenant()));

CREATE POLICY rls_organization__update ON organization FOR UPDATE USING (tenant_id = (SELECT app_tenant())) WITH CHECK (tenant_id = (SELECT app_tenant()));

ALTER TABLE company ENABLE ROW LEVEL SECURITY;

ALTER TABLE company FORCE ROW LEVEL SECURITY;

CREATE POLICY rls_company__select ON company FOR SELECT USING (tenant_id = (SELECT app_tenant()) AND company_id = ANY ((SELECT app_company_ids())::uuid[]));

CREATE POLICY rls_company__insert ON company FOR INSERT WITH CHECK (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company()));

CREATE POLICY rls_company__update ON company FOR UPDATE USING (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company())) WITH CHECK (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company()));

ALTER TABLE division ENABLE ROW LEVEL SECURITY;

ALTER TABLE division FORCE ROW LEVEL SECURITY;

CREATE POLICY rls_division__select ON division FOR SELECT USING (tenant_id = (SELECT app_tenant()) AND (company_id = ANY ((SELECT app_company_ids())::uuid[]) OR company_id IS NULL));

CREATE POLICY rls_division__insert ON division FOR INSERT WITH CHECK (tenant_id = (SELECT app_tenant()) AND (company_id = (SELECT app_write_company()) OR (company_id IS NULL AND (SELECT app_actor_kind()) = 'service')));

CREATE POLICY rls_division__update ON division FOR UPDATE USING (tenant_id = (SELECT app_tenant()) AND (company_id = (SELECT app_write_company()) OR (company_id IS NULL AND (SELECT app_actor_kind()) = 'service'))) WITH CHECK (tenant_id = (SELECT app_tenant()) AND (company_id = (SELECT app_write_company()) OR (company_id IS NULL AND (SELECT app_actor_kind()) = 'service')));

ALTER TABLE brand ENABLE ROW LEVEL SECURITY;

ALTER TABLE brand FORCE ROW LEVEL SECURITY;

CREATE POLICY rls_brand__select ON brand FOR SELECT USING (tenant_id = (SELECT app_tenant()) AND (company_id = ANY ((SELECT app_company_ids())::uuid[]) OR company_id IS NULL));

CREATE POLICY rls_brand__insert ON brand FOR INSERT WITH CHECK (tenant_id = (SELECT app_tenant()) AND (company_id = (SELECT app_write_company()) OR (company_id IS NULL AND (SELECT app_actor_kind()) = 'service')));

CREATE POLICY rls_brand__update ON brand FOR UPDATE USING (tenant_id = (SELECT app_tenant()) AND (company_id = (SELECT app_write_company()) OR (company_id IS NULL AND (SELECT app_actor_kind()) = 'service'))) WITH CHECK (tenant_id = (SELECT app_tenant()) AND (company_id = (SELECT app_write_company()) OR (company_id IS NULL AND (SELECT app_actor_kind()) = 'service')));

ALTER TABLE offering ENABLE ROW LEVEL SECURITY;

ALTER TABLE offering FORCE ROW LEVEL SECURITY;

CREATE POLICY rls_offering__select ON offering FOR SELECT USING (tenant_id = (SELECT app_tenant()) AND (company_id = ANY ((SELECT app_company_ids())::uuid[]) OR company_id IS NULL));

CREATE POLICY rls_offering__insert ON offering FOR INSERT WITH CHECK (tenant_id = (SELECT app_tenant()) AND (company_id = (SELECT app_write_company()) OR (company_id IS NULL AND (SELECT app_actor_kind()) = 'service')));

CREATE POLICY rls_offering__update ON offering FOR UPDATE USING (tenant_id = (SELECT app_tenant()) AND (company_id = (SELECT app_write_company()) OR (company_id IS NULL AND (SELECT app_actor_kind()) = 'service'))) WITH CHECK (tenant_id = (SELECT app_tenant()) AND (company_id = (SELECT app_write_company()) OR (company_id IS NULL AND (SELECT app_actor_kind()) = 'service')));

ALTER TABLE market ENABLE ROW LEVEL SECURITY;

ALTER TABLE market FORCE ROW LEVEL SECURITY;

CREATE POLICY rls_market__select ON market FOR SELECT USING (tenant_id = (SELECT app_tenant()) AND (company_id = ANY ((SELECT app_company_ids())::uuid[]) OR company_id IS NULL));

CREATE POLICY rls_market__insert ON market FOR INSERT WITH CHECK (tenant_id = (SELECT app_tenant()) AND (company_id = (SELECT app_write_company()) OR (company_id IS NULL AND (SELECT app_actor_kind()) = 'service')));

CREATE POLICY rls_market__update ON market FOR UPDATE USING (tenant_id = (SELECT app_tenant()) AND (company_id = (SELECT app_write_company()) OR (company_id IS NULL AND (SELECT app_actor_kind()) = 'service'))) WITH CHECK (tenant_id = (SELECT app_tenant()) AND (company_id = (SELECT app_write_company()) OR (company_id IS NULL AND (SELECT app_actor_kind()) = 'service')));

ALTER TABLE channel_account ENABLE ROW LEVEL SECURITY;

ALTER TABLE channel_account FORCE ROW LEVEL SECURITY;

CREATE POLICY rls_channel_account__select ON channel_account FOR SELECT USING (tenant_id = (SELECT app_tenant()) AND (company_id = ANY ((SELECT app_company_ids())::uuid[]) OR company_id IS NULL));

CREATE POLICY rls_channel_account__insert ON channel_account FOR INSERT WITH CHECK (tenant_id = (SELECT app_tenant()) AND (company_id = (SELECT app_write_company()) OR (company_id IS NULL AND (SELECT app_actor_kind()) = 'service')));

CREATE POLICY rls_channel_account__update ON channel_account FOR UPDATE USING (tenant_id = (SELECT app_tenant()) AND (company_id = (SELECT app_write_company()) OR (company_id IS NULL AND (SELECT app_actor_kind()) = 'service'))) WITH CHECK (tenant_id = (SELECT app_tenant()) AND (company_id = (SELECT app_write_company()) OR (company_id IS NULL AND (SELECT app_actor_kind()) = 'service')));

ALTER TABLE workflow_run ENABLE ROW LEVEL SECURITY;

ALTER TABLE workflow_run FORCE ROW LEVEL SECURITY;

CREATE POLICY rls_workflow_run__select ON workflow_run FOR SELECT USING (tenant_id = (SELECT app_tenant()) AND (company_id = ANY ((SELECT app_company_ids())::uuid[]) OR company_id IS NULL));

CREATE POLICY rls_workflow_run__insert ON workflow_run FOR INSERT WITH CHECK (tenant_id = (SELECT app_tenant()) AND (company_id = (SELECT app_write_company()) OR (company_id IS NULL AND (SELECT app_actor_kind()) = 'service')));

CREATE POLICY rls_workflow_run__update ON workflow_run FOR UPDATE USING (tenant_id = (SELECT app_tenant()) AND (company_id = (SELECT app_write_company()) OR (company_id IS NULL AND (SELECT app_actor_kind()) = 'service'))) WITH CHECK (tenant_id = (SELECT app_tenant()) AND (company_id = (SELECT app_write_company()) OR (company_id IS NULL AND (SELECT app_actor_kind()) = 'service')));

ALTER TABLE workflow_step_run ENABLE ROW LEVEL SECURITY;

ALTER TABLE workflow_step_run FORCE ROW LEVEL SECURITY;

CREATE POLICY rls_workflow_step_run__select ON workflow_step_run FOR SELECT USING (tenant_id = (SELECT app_tenant()) AND company_id = ANY ((SELECT app_company_ids())::uuid[]));

CREATE POLICY rls_workflow_step_run__insert ON workflow_step_run FOR INSERT WITH CHECK (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company()));

CREATE POLICY rls_workflow_step_run__update ON workflow_step_run FOR UPDATE USING (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company())) WITH CHECK (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company()));

ALTER TABLE effect ENABLE ROW LEVEL SECURITY;

ALTER TABLE effect FORCE ROW LEVEL SECURITY;

CREATE POLICY rls_effect__select ON effect FOR SELECT USING (tenant_id = (SELECT app_tenant()) AND company_id = ANY ((SELECT app_company_ids())::uuid[]));

CREATE POLICY rls_effect__insert ON effect FOR INSERT WITH CHECK (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company()));

CREATE POLICY rls_effect__update ON effect FOR UPDATE USING (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company())) WITH CHECK (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company()));

ALTER TABLE outbox ENABLE ROW LEVEL SECURITY;

ALTER TABLE outbox FORCE ROW LEVEL SECURITY;

CREATE POLICY rls_outbox__select ON outbox FOR SELECT USING (tenant_id = (SELECT app_tenant()) AND (company_id = ANY ((SELECT app_company_ids())::uuid[]) OR company_id IS NULL));

CREATE POLICY rls_outbox__insert ON outbox FOR INSERT WITH CHECK (tenant_id = (SELECT app_tenant()) AND (company_id = (SELECT app_write_company()) OR (company_id IS NULL AND (SELECT app_actor_kind()) = 'service')));

CREATE POLICY rls_outbox__update ON outbox FOR UPDATE USING (tenant_id = (SELECT app_tenant()) AND (company_id = (SELECT app_write_company()) OR (company_id IS NULL AND (SELECT app_actor_kind()) = 'service'))) WITH CHECK (tenant_id = (SELECT app_tenant()) AND (company_id = (SELECT app_write_company()) OR (company_id IS NULL AND (SELECT app_actor_kind()) = 'service')));

ALTER TABLE inbox ENABLE ROW LEVEL SECURITY;

ALTER TABLE inbox FORCE ROW LEVEL SECURITY;

CREATE POLICY rls_inbox__select ON inbox FOR SELECT USING (tenant_id = (SELECT app_tenant()));

CREATE POLICY rls_inbox__insert ON inbox FOR INSERT WITH CHECK (tenant_id = (SELECT app_tenant()) AND (SELECT app_actor_kind()) = 'service');

CREATE POLICY rls_inbox__update ON inbox FOR UPDATE USING (tenant_id = (SELECT app_tenant())) WITH CHECK (tenant_id = (SELECT app_tenant()));

ALTER TABLE audit_event ENABLE ROW LEVEL SECURITY;

ALTER TABLE audit_event FORCE ROW LEVEL SECURITY;

CREATE POLICY rls_audit_event__select ON audit_event FOR SELECT USING (tenant_id = (SELECT app_tenant()) AND (company_id = ANY ((SELECT app_company_ids())::uuid[]) OR company_id IS NULL));

ALTER TABLE portfolio_grant ENABLE ROW LEVEL SECURITY;

ALTER TABLE portfolio_grant FORCE ROW LEVEL SECURITY;

CREATE POLICY rls_portfolio_grant__select ON portfolio_grant FOR SELECT USING (tenant_id = (SELECT app_tenant()) AND (company_id = ANY ((SELECT app_company_ids())::uuid[]) OR portfolio_id = (SELECT app_portfolio_id())) AND revoked_at IS NULL AND expires_at > now());

CREATE POLICY rls_portfolio_grant__insert ON portfolio_grant FOR INSERT WITH CHECK (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company()) AND (SELECT app_actor_kind()) = 'internal');

CREATE POLICY rls_portfolio_grant__update ON portfolio_grant FOR UPDATE USING (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company())) WITH CHECK (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company()));

ALTER TABLE consent_record ENABLE ROW LEVEL SECURITY;

ALTER TABLE consent_record FORCE ROW LEVEL SECURITY;

CREATE POLICY rls_consent_record__select ON consent_record FOR SELECT USING (tenant_id = (SELECT app_tenant()) AND company_id = ANY ((SELECT app_company_ids())::uuid[]));

CREATE POLICY rls_consent_record__insert ON consent_record FOR INSERT WITH CHECK (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company()));

ALTER TABLE suppression ENABLE ROW LEVEL SECURITY;

ALTER TABLE suppression FORCE ROW LEVEL SECURITY;

CREATE POLICY rls_suppression__select ON suppression FOR SELECT USING (tenant_id = (SELECT app_tenant()) AND company_id = ANY ((SELECT app_company_ids())::uuid[]));

CREATE POLICY rls_suppression__insert ON suppression FOR INSERT WITH CHECK (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company()));

CREATE POLICY rls_suppression__update ON suppression FOR UPDATE USING (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company())) WITH CHECK (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company()));

ALTER TABLE dsar_request ENABLE ROW LEVEL SECURITY;

ALTER TABLE dsar_request FORCE ROW LEVEL SECURITY;

CREATE POLICY rls_dsar_request__select ON dsar_request FOR SELECT USING (tenant_id = (SELECT app_tenant()));

CREATE POLICY rls_dsar_request__insert ON dsar_request FOR INSERT WITH CHECK (tenant_id = (SELECT app_tenant()));

CREATE POLICY rls_dsar_request__update ON dsar_request FOR UPDATE USING (tenant_id = (SELECT app_tenant())) WITH CHECK (tenant_id = (SELECT app_tenant()));

ALTER TABLE incident ENABLE ROW LEVEL SECURITY;

ALTER TABLE incident FORCE ROW LEVEL SECURITY;

CREATE POLICY rls_incident__select ON incident FOR SELECT TO app_rw, app_worker, app_readonly USING (tenant_id = (SELECT app_tenant()));

CREATE POLICY rls_incident__insert ON incident FOR INSERT TO app_rw, app_worker WITH CHECK (tenant_id = (SELECT app_tenant()));

CREATE POLICY rls_incident__platform ON incident FOR ALL TO app_platform_sec USING (true) WITH CHECK (true);

GRANT SELECT, INSERT, UPDATE ON incident TO app_platform_sec;

ALTER TABLE ai_usage_event ENABLE ROW LEVEL SECURITY;

ALTER TABLE ai_usage_event FORCE ROW LEVEL SECURITY;

CREATE POLICY rls_ai_usage_event__select ON ai_usage_event FOR SELECT USING (tenant_id = (SELECT app_tenant()) AND (company_id = ANY ((SELECT app_company_ids())::uuid[]) OR company_id IS NULL));

CREATE POLICY rls_ai_usage_event__insert ON ai_usage_event FOR INSERT WITH CHECK (tenant_id = (SELECT app_tenant()) AND (company_id = (SELECT app_write_company()) OR (company_id IS NULL AND (SELECT app_actor_kind()) = 'service')));

ALTER TABLE ai_budget ENABLE ROW LEVEL SECURITY;

ALTER TABLE ai_budget FORCE ROW LEVEL SECURITY;

CREATE POLICY rls_ai_budget__select ON ai_budget FOR SELECT USING (tenant_id = (SELECT app_tenant()));

CREATE POLICY rls_ai_budget__insert ON ai_budget FOR INSERT WITH CHECK (tenant_id = (SELECT app_tenant()));

CREATE POLICY rls_ai_budget__update ON ai_budget FOR UPDATE USING (tenant_id = (SELECT app_tenant())) WITH CHECK (tenant_id = (SELECT app_tenant()));

ALTER TABLE identity_provider ENABLE ROW LEVEL SECURITY;

ALTER TABLE identity_provider FORCE ROW LEVEL SECURITY;

CREATE POLICY rls_identity_provider__select ON identity_provider FOR SELECT USING (tenant_id = (SELECT app_tenant()));

CREATE POLICY rls_identity_provider__insert ON identity_provider FOR INSERT WITH CHECK (tenant_id = (SELECT app_tenant()));

CREATE POLICY rls_identity_provider__update ON identity_provider FOR UPDATE USING (tenant_id = (SELECT app_tenant())) WITH CHECK (tenant_id = (SELECT app_tenant()));

ALTER TABLE scim_token ENABLE ROW LEVEL SECURITY;

ALTER TABLE scim_token FORCE ROW LEVEL SECURITY;

CREATE POLICY rls_scim_token__select ON scim_token FOR SELECT USING (tenant_id = (SELECT app_tenant()));

CREATE POLICY rls_scim_token__insert ON scim_token FOR INSERT WITH CHECK (tenant_id = (SELECT app_tenant()));

CREATE POLICY rls_scim_token__update ON scim_token FOR UPDATE USING (tenant_id = (SELECT app_tenant())) WITH CHECK (tenant_id = (SELECT app_tenant()));

ALTER TABLE custom_role ENABLE ROW LEVEL SECURITY;

ALTER TABLE custom_role FORCE ROW LEVEL SECURITY;

CREATE POLICY rls_custom_role__select ON custom_role FOR SELECT USING (tenant_id = (SELECT app_tenant()));

CREATE POLICY rls_custom_role__insert ON custom_role FOR INSERT WITH CHECK (tenant_id = (SELECT app_tenant()));

CREATE POLICY rls_custom_role__update ON custom_role FOR UPDATE USING (tenant_id = (SELECT app_tenant())) WITH CHECK (tenant_id = (SELECT app_tenant()));

ALTER TABLE role_permission ENABLE ROW LEVEL SECURITY;

ALTER TABLE role_permission FORCE ROW LEVEL SECURITY;

CREATE POLICY rls_role_permission__select ON role_permission FOR SELECT USING (tenant_id = (SELECT app_tenant()));

CREATE POLICY rls_role_permission__insert ON role_permission FOR INSERT WITH CHECK (tenant_id = (SELECT app_tenant()));

CREATE POLICY rls_role_permission__update ON role_permission FOR UPDATE USING (tenant_id = (SELECT app_tenant())) WITH CHECK (tenant_id = (SELECT app_tenant()));

ALTER TABLE api_key ENABLE ROW LEVEL SECURITY;

ALTER TABLE api_key FORCE ROW LEVEL SECURITY;

CREATE POLICY rls_api_key__select ON api_key FOR SELECT USING (tenant_id = (SELECT app_tenant()));

CREATE POLICY rls_api_key__insert ON api_key FOR INSERT WITH CHECK (tenant_id = (SELECT app_tenant()));

CREATE POLICY rls_api_key__update ON api_key FOR UPDATE USING (tenant_id = (SELECT app_tenant())) WITH CHECK (tenant_id = (SELECT app_tenant()));

ALTER TABLE webhook_endpoint ENABLE ROW LEVEL SECURITY;

ALTER TABLE webhook_endpoint FORCE ROW LEVEL SECURITY;

CREATE POLICY rls_webhook_endpoint__select ON webhook_endpoint FOR SELECT USING (tenant_id = (SELECT app_tenant()));

CREATE POLICY rls_webhook_endpoint__insert ON webhook_endpoint FOR INSERT WITH CHECK (tenant_id = (SELECT app_tenant()));

CREATE POLICY rls_webhook_endpoint__update ON webhook_endpoint FOR UPDATE USING (tenant_id = (SELECT app_tenant())) WITH CHECK (tenant_id = (SELECT app_tenant()));

ALTER TABLE webhook_delivery ENABLE ROW LEVEL SECURITY;

ALTER TABLE webhook_delivery FORCE ROW LEVEL SECURITY;

CREATE POLICY rls_webhook_delivery__select ON webhook_delivery FOR SELECT USING (tenant_id = (SELECT app_tenant()));

CREATE POLICY rls_webhook_delivery__insert ON webhook_delivery FOR INSERT WITH CHECK (tenant_id = (SELECT app_tenant()));

CREATE POLICY rls_webhook_delivery__update ON webhook_delivery FOR UPDATE USING (tenant_id = (SELECT app_tenant())) WITH CHECK (tenant_id = (SELECT app_tenant()));

ALTER TABLE audit_sink ENABLE ROW LEVEL SECURITY;

ALTER TABLE audit_sink FORCE ROW LEVEL SECURITY;

CREATE POLICY rls_audit_sink__select ON audit_sink FOR SELECT USING (tenant_id = (SELECT app_tenant()));

CREATE POLICY rls_audit_sink__insert ON audit_sink FOR INSERT WITH CHECK (tenant_id = (SELECT app_tenant()));

CREATE POLICY rls_audit_sink__update ON audit_sink FOR UPDATE USING (tenant_id = (SELECT app_tenant())) WITH CHECK (tenant_id = (SELECT app_tenant()));

ALTER TABLE export_job ENABLE ROW LEVEL SECURITY;

ALTER TABLE export_job FORCE ROW LEVEL SECURITY;

CREATE POLICY rls_export_job__select ON export_job FOR SELECT USING (tenant_id = (SELECT app_tenant()));

CREATE POLICY rls_export_job__insert ON export_job FOR INSERT WITH CHECK (tenant_id = (SELECT app_tenant()));

CREATE POLICY rls_export_job__update ON export_job FOR UPDATE USING (tenant_id = (SELECT app_tenant())) WITH CHECK (tenant_id = (SELECT app_tenant()));

ALTER TABLE tenant_key_config ENABLE ROW LEVEL SECURITY;

ALTER TABLE tenant_key_config FORCE ROW LEVEL SECURITY;

CREATE POLICY rls_tenant_key_config__select ON tenant_key_config FOR SELECT USING (tenant_id = (SELECT app_tenant()));

CREATE POLICY rls_tenant_key_config__insert ON tenant_key_config FOR INSERT WITH CHECK (tenant_id = (SELECT app_tenant()));

CREATE POLICY rls_tenant_key_config__update ON tenant_key_config FOR UPDATE USING (tenant_id = (SELECT app_tenant())) WITH CHECK (tenant_id = (SELECT app_tenant()));

ALTER TABLE sandbox_environment ENABLE ROW LEVEL SECURITY;

ALTER TABLE sandbox_environment FORCE ROW LEVEL SECURITY;

CREATE POLICY rls_sandbox_environment__select ON sandbox_environment FOR SELECT USING (tenant_id = (SELECT app_tenant()));

CREATE POLICY rls_sandbox_environment__insert ON sandbox_environment FOR INSERT WITH CHECK (tenant_id = (SELECT app_tenant()));

CREATE POLICY rls_sandbox_environment__update ON sandbox_environment FOR UPDATE USING (tenant_id = (SELECT app_tenant())) WITH CHECK (tenant_id = (SELECT app_tenant()));

ALTER TABLE config_promotion ENABLE ROW LEVEL SECURITY;

ALTER TABLE config_promotion FORCE ROW LEVEL SECURITY;

CREATE POLICY rls_config_promotion__select ON config_promotion FOR SELECT USING (tenant_id = (SELECT app_tenant()));

CREATE POLICY rls_config_promotion__insert ON config_promotion FOR INSERT WITH CHECK (tenant_id = (SELECT app_tenant()));

CREATE POLICY rls_config_promotion__update ON config_promotion FOR UPDATE USING (tenant_id = (SELECT app_tenant())) WITH CHECK (tenant_id = (SELECT app_tenant()));

ALTER TABLE connector_installation ENABLE ROW LEVEL SECURITY;

ALTER TABLE connector_installation FORCE ROW LEVEL SECURITY;

CREATE POLICY rls_connector_installation__select ON connector_installation FOR SELECT USING (tenant_id = (SELECT app_tenant()));

CREATE POLICY rls_connector_installation__insert ON connector_installation FOR INSERT WITH CHECK (tenant_id = (SELECT app_tenant()));

CREATE POLICY rls_connector_installation__update ON connector_installation FOR UPDATE USING (tenant_id = (SELECT app_tenant())) WITH CHECK (tenant_id = (SELECT app_tenant()));

ALTER TABLE invoice ENABLE ROW LEVEL SECURITY;

ALTER TABLE invoice FORCE ROW LEVEL SECURITY;

CREATE POLICY rls_invoice__select ON invoice FOR SELECT USING (tenant_id = (SELECT app_tenant()));

CREATE POLICY rls_invoice__insert ON invoice FOR INSERT WITH CHECK (tenant_id = (SELECT app_tenant()));

CREATE POLICY rls_invoice__update ON invoice FOR UPDATE USING (tenant_id = (SELECT app_tenant())) WITH CHECK (tenant_id = (SELECT app_tenant()));

ALTER TABLE user_role_assignment ENABLE ROW LEVEL SECURITY;

ALTER TABLE user_role_assignment FORCE ROW LEVEL SECURITY;

CREATE POLICY rls_user_role_assignment__select ON user_role_assignment FOR SELECT USING (tenant_id = (SELECT app_tenant()));

CREATE POLICY rls_user_role_assignment__insert ON user_role_assignment FOR INSERT WITH CHECK (tenant_id = (SELECT app_tenant()));

CREATE POLICY rls_user_role_assignment__update ON user_role_assignment FOR UPDATE USING (tenant_id = (SELECT app_tenant())) WITH CHECK (tenant_id = (SELECT app_tenant()));

ALTER TABLE tenant_data_key ENABLE ROW LEVEL SECURITY;

ALTER TABLE tenant_data_key FORCE ROW LEVEL SECURITY;

CREATE POLICY rls_tenant_data_key__select ON tenant_data_key FOR SELECT USING (tenant_id = (SELECT app_tenant()));

CREATE POLICY rls_tenant_data_key__insert ON tenant_data_key FOR INSERT WITH CHECK (tenant_id = (SELECT app_tenant()));

CREATE POLICY rls_tenant_data_key__update ON tenant_data_key FOR UPDATE USING (tenant_id = (SELECT app_tenant())) WITH CHECK (tenant_id = (SELECT app_tenant()));

ALTER TABLE company_operating_country ENABLE ROW LEVEL SECURITY;

ALTER TABLE company_operating_country FORCE ROW LEVEL SECURITY;

CREATE POLICY rls_company_operating_country__select ON company_operating_country FOR SELECT USING (tenant_id = (SELECT app_tenant()) AND company_id = ANY ((SELECT app_company_ids())::uuid[]));

CREATE POLICY rls_company_operating_country__insert ON company_operating_country FOR INSERT WITH CHECK (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company()));

CREATE POLICY rls_company_operating_country__update ON company_operating_country FOR UPDATE USING (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company())) WITH CHECK (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company()));

ALTER TABLE offering_market ENABLE ROW LEVEL SECURITY;

ALTER TABLE offering_market FORCE ROW LEVEL SECURITY;

CREATE POLICY rls_offering_market__select ON offering_market FOR SELECT USING (tenant_id = (SELECT app_tenant()) AND company_id = ANY ((SELECT app_company_ids())::uuid[]));

CREATE POLICY rls_offering_market__insert ON offering_market FOR INSERT WITH CHECK (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company()));

CREATE POLICY rls_offering_market__update ON offering_market FOR UPDATE USING (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company())) WITH CHECK (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company()));

ALTER TABLE channel_account_market ENABLE ROW LEVEL SECURITY;

ALTER TABLE channel_account_market FORCE ROW LEVEL SECURITY;

CREATE POLICY rls_channel_account_market__select ON channel_account_market FOR SELECT USING (tenant_id = (SELECT app_tenant()) AND company_id = ANY ((SELECT app_company_ids())::uuid[]));

CREATE POLICY rls_channel_account_market__insert ON channel_account_market FOR INSERT WITH CHECK (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company()));

CREATE POLICY rls_channel_account_market__update ON channel_account_market FOR UPDATE USING (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company())) WITH CHECK (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company()));

ALTER TABLE configuration_revision ENABLE ROW LEVEL SECURITY;

ALTER TABLE configuration_revision FORCE ROW LEVEL SECURITY;

CREATE POLICY rls_configuration_revision__select ON configuration_revision FOR SELECT USING (tenant_id = (SELECT app_tenant()) AND company_id = ANY ((SELECT app_company_ids())::uuid[]));

CREATE POLICY rls_configuration_revision__insert ON configuration_revision FOR INSERT WITH CHECK (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company()));

CREATE POLICY rls_configuration_revision__update ON configuration_revision FOR UPDATE USING (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company())) WITH CHECK (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company()));

ALTER TABLE workflow_configuration ENABLE ROW LEVEL SECURITY;

ALTER TABLE workflow_configuration FORCE ROW LEVEL SECURITY;

CREATE POLICY rls_workflow_configuration__select ON workflow_configuration FOR SELECT USING (tenant_id = (SELECT app_tenant()) AND company_id = ANY ((SELECT app_company_ids())::uuid[]));

CREATE POLICY rls_workflow_configuration__insert ON workflow_configuration FOR INSERT WITH CHECK (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company()));

CREATE POLICY rls_workflow_configuration__update ON workflow_configuration FOR UPDATE USING (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company())) WITH CHECK (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company()));

ALTER TABLE business_event ENABLE ROW LEVEL SECURITY;

ALTER TABLE business_event FORCE ROW LEVEL SECURITY;

CREATE POLICY rls_business_event__select ON business_event FOR SELECT USING (tenant_id = (SELECT app_tenant()) AND company_id = ANY ((SELECT app_company_ids())::uuid[]));

CREATE POLICY rls_business_event__insert ON business_event FOR INSERT WITH CHECK (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company()));

ALTER TABLE metric_aggregate ENABLE ROW LEVEL SECURITY;

ALTER TABLE metric_aggregate FORCE ROW LEVEL SECURITY;

CREATE POLICY rls_metric_aggregate__select ON metric_aggregate FOR SELECT USING (tenant_id = (SELECT app_tenant()) AND company_id = ANY ((SELECT app_company_ids())::uuid[]));

CREATE POLICY rls_metric_aggregate__insert ON metric_aggregate FOR INSERT WITH CHECK (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company()));

CREATE POLICY rls_metric_aggregate__update ON metric_aggregate FOR UPDATE USING (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company())) WITH CHECK (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company()));

ALTER TABLE experiment ENABLE ROW LEVEL SECURITY;

ALTER TABLE experiment FORCE ROW LEVEL SECURITY;

CREATE POLICY rls_experiment__select ON experiment FOR SELECT USING (tenant_id = (SELECT app_tenant()) AND company_id = ANY ((SELECT app_company_ids())::uuid[]));

CREATE POLICY rls_experiment__insert ON experiment FOR INSERT WITH CHECK (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company()));

CREATE POLICY rls_experiment__update ON experiment FOR UPDATE USING (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company())) WITH CHECK (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company()));

ALTER TABLE feedback_case ENABLE ROW LEVEL SECURITY;

ALTER TABLE feedback_case FORCE ROW LEVEL SECURITY;

CREATE POLICY rls_feedback_case__select ON feedback_case FOR SELECT USING (tenant_id = (SELECT app_tenant()) AND company_id = ANY ((SELECT app_company_ids())::uuid[]));

CREATE POLICY rls_feedback_case__insert ON feedback_case FOR INSERT WITH CHECK (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company()));

CREATE POLICY rls_feedback_case__update ON feedback_case FOR UPDATE USING (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company())) WITH CHECK (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company()));

ALTER TABLE customer_value ENABLE ROW LEVEL SECURITY;

ALTER TABLE customer_value FORCE ROW LEVEL SECURITY;

CREATE POLICY rls_customer_value__select ON customer_value FOR SELECT USING (tenant_id = (SELECT app_tenant()));

CREATE POLICY rls_customer_value__insert ON customer_value FOR INSERT WITH CHECK (tenant_id = (SELECT app_tenant()));

CREATE POLICY rls_customer_value__update ON customer_value FOR UPDATE USING (tenant_id = (SELECT app_tenant())) WITH CHECK (tenant_id = (SELECT app_tenant()));

ALTER TABLE journey_event ENABLE ROW LEVEL SECURITY;

ALTER TABLE journey_event FORCE ROW LEVEL SECURITY;

CREATE POLICY rls_journey_event__subscriber ON journey_event FOR SELECT TO app_rw, app_worker USING (audience = 'subscriber' AND tenant_id = (SELECT app_tenant()));

CREATE POLICY rls_journey_event__insert ON journey_event FOR INSERT TO app_rw, app_worker WITH CHECK ((audience = 'subscriber' AND tenant_id = (SELECT app_tenant())) OR (audience = 'operator' AND tenant_id IS NULL AND (SELECT app_actor_kind()) = 'service'));

CREATE POLICY rls_journey_event__operator ON journey_event FOR SELECT TO app_readonly USING (audience = 'operator');

ALTER TABLE domain_record_version ENABLE ROW LEVEL SECURITY;

ALTER TABLE domain_record_version FORCE ROW LEVEL SECURITY;

CREATE POLICY rls_domain_record_version__select ON domain_record_version FOR SELECT USING (tenant_id = (SELECT app_tenant()) AND company_id = ANY ((SELECT app_company_ids())::uuid[]));

CREATE POLICY rls_domain_record_version__insert ON domain_record_version FOR INSERT WITH CHECK (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company()));

ALTER TABLE usage_reservation ENABLE ROW LEVEL SECURITY;

ALTER TABLE usage_reservation FORCE ROW LEVEL SECURITY;

CREATE POLICY rls_usage_reservation__select ON usage_reservation FOR SELECT USING (tenant_id = (SELECT app_tenant()) AND company_id = ANY ((SELECT app_company_ids())::uuid[]));

CREATE POLICY rls_usage_reservation__insert ON usage_reservation FOR INSERT WITH CHECK (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company()));

CREATE POLICY rls_usage_reservation__update ON usage_reservation FOR UPDATE USING (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company())) WITH CHECK (tenant_id = (SELECT app_tenant()) AND company_id = (SELECT app_write_company()));

CREATE POLICY rls_audit_event__insert_definer ON audit_event FOR INSERT TO CURRENT_USER WITH CHECK (tenant_id = (SELECT app_tenant()));

CREATE INDEX IF NOT EXISTS ix_ai_model__rollback_to ON ai_model (rollback_to);

CREATE INDEX IF NOT EXISTS ix_api_key__tenant_id ON api_key (tenant_id);

CREATE INDEX IF NOT EXISTS ix_audit_sink__tenant_id ON audit_sink (tenant_id);

CREATE INDEX IF NOT EXISTS ix_brand__tenant_id_company_id_division_id ON brand (tenant_id,company_id,division_id);

CREATE INDEX IF NOT EXISTS ix_brand__tenant_id_division_id ON brand (tenant_id,division_id);

CREATE INDEX IF NOT EXISTS ix_business_event__tenant_id_company_id_account_id ON business_event (tenant_id,company_id,account_id);

CREATE INDEX IF NOT EXISTS ix_business_event__tenant_id_company_id_market_id ON business_event (tenant_id,company_id,market_id);

CREATE INDEX IF NOT EXISTS ix_business_event__tenant_id_company_id_offering_id ON business_event (tenant_id,company_id,offering_id);

CREATE INDEX IF NOT EXISTS ix_business_event__tenant_id_company_id_run_id ON business_event (tenant_id,company_id,run_id);

CREATE INDEX IF NOT EXISTS ix_channel_account_market__tenant_id_company_id_market_id ON channel_account_market (tenant_id,company_id,market_id);

CREATE INDEX IF NOT EXISTS ix_company__tenant_id_organization_id ON company (tenant_id,organization_id);

CREATE INDEX IF NOT EXISTS ix_config_promotion__tenant_id_sandbox_id ON config_promotion (tenant_id,sandbox_id);

CREATE INDEX IF NOT EXISTS ix_connector_installation__tenant_id ON connector_installation (tenant_id);

CREATE INDEX IF NOT EXISTS ix_consent_record__tenant_id_contact_id ON consent_record (tenant_id,contact_id);

CREATE INDEX IF NOT EXISTS ix_consent_record__tenant_id_company_id ON consent_record (tenant_id,company_id);

CREATE INDEX IF NOT EXISTS ix_domain_record_version__tenant_id_company_id ON domain_record_version (tenant_id,company_id);

CREATE INDEX IF NOT EXISTS ix_effect__tenant_id_company_id_run_id ON effect (tenant_id,company_id,run_id);

CREATE INDEX IF NOT EXISTS ix_eval_run__suite_id ON eval_run (suite_id);

CREATE INDEX IF NOT EXISTS ix_experiment__primary_metric_id_primary_metric_version ON experiment (primary_metric_id,primary_metric_version);

CREATE INDEX IF NOT EXISTS ix_experiment__tenant_id_company_id ON experiment (tenant_id,company_id);

CREATE INDEX IF NOT EXISTS ix_export_job__tenant_id ON export_job (tenant_id);

CREATE INDEX IF NOT EXISTS ix_feedback_case__tenant_id_company_id ON feedback_case (tenant_id,company_id);

CREATE INDEX IF NOT EXISTS ix_invoice__tax_rule_id ON invoice (tax_rule_id);

CREATE INDEX IF NOT EXISTS ix_invoice__tenant_id ON invoice (tenant_id);

CREATE INDEX IF NOT EXISTS ix_metric_aggregate__metric_id_metric_version ON metric_aggregate (metric_id,metric_version);

CREATE INDEX IF NOT EXISTS ix_offering__tenant_id_company_id_brand_id ON offering (tenant_id,company_id,brand_id);

CREATE INDEX IF NOT EXISTS ix_offering_market__tenant_id_company_id_market_id ON offering_market (tenant_id,company_id,market_id);

CREATE INDEX IF NOT EXISTS ix_offering__tenant_id_brand_id ON offering (tenant_id,brand_id);

CREATE INDEX IF NOT EXISTS ix_portfolio_grant__tenant_id_company_id ON portfolio_grant (tenant_id,company_id);

CREATE INDEX IF NOT EXISTS ix_scim_token__tenant_id ON scim_token (tenant_id);

CREATE INDEX IF NOT EXISTS ix_usage_reservation__tenant_id_company_id_run_id ON usage_reservation (tenant_id,company_id,run_id);

CREATE INDEX IF NOT EXISTS ix_user_role_assignment__tenant_id_role_id ON user_role_assignment (tenant_id,role_id);

CREATE INDEX IF NOT EXISTS ix_workflow_configuration__tenant_id_company_id_account_id ON workflow_configuration (tenant_id,company_id,account_id);

CREATE INDEX IF NOT EXISTS ix_workflow_configuration__tenant_id_company_id_market_id ON workflow_configuration (tenant_id,company_id,market_id);

CREATE INDEX IF NOT EXISTS ix_workflow_configuration__tenant_id_config_revision_id ON workflow_configuration (tenant_id,config_revision_id);

CREATE INDEX IF NOT EXISTS ix_workflow_step_run__tenant_id_company_id_run_id ON workflow_step_run (tenant_id,company_id,run_id);

CREATE INDEX IF NOT EXISTS ixp_outbox__pending ON outbox (next_attempt_at, event_id) WHERE (published_at IS NULL);

CREATE INDEX IF NOT EXISTS ix_workflow_run__scope_status ON workflow_run (tenant_id, company_id, status, created_at DESC);

CREATE INDEX IF NOT EXISTS ixp_workflow_run__active ON workflow_run (tenant_id, company_id, created_at) WHERE (status IN ('Queued','Running','Awaiting approval','Held','Reconciling'));

CREATE INDEX IF NOT EXISTS ixp_effect__open ON effect (tenant_id, company_id, status) WHERE (status IN ('Intended','Dispatched','Reconciling'));

CREATE INDEX IF NOT EXISTS ix_consent_record__current ON consent_record (tenant_id, company_id, contact_id, channel, purpose, captured_at DESC);

CREATE INDEX IF NOT EXISTS ixp_dsar_request__open ON dsar_request (tenant_id, due_at) WHERE (status NOT IN ('Completed','Rejected'));

CREATE INDEX IF NOT EXISTS ixb_audit_event__time ON audit_event USING brin (occurred_at);

CREATE INDEX IF NOT EXISTS ix_audit_event__object ON audit_event (tenant_id, object_type, ref, occurred_at DESC);

CREATE INDEX IF NOT EXISTS ixb_ai_usage_event__time ON ai_usage_event USING brin (occurred_at);

CREATE INDEX IF NOT EXISTS ix_ai_usage_event__scope_time ON ai_usage_event (tenant_id, company_id, occurred_at);

CREATE INDEX IF NOT EXISTS ixp_webhook_delivery__pending ON webhook_delivery (tenant_id, endpoint_id, signed_at) WHERE (delivered_at IS NULL);

CREATE INDEX IF NOT EXISTS ixp_api_key__live ON api_key (tenant_id) WHERE (revoked_at IS NULL);

CREATE INDEX IF NOT EXISTS ixp_security_finding__open ON security_finding (severity, due_at) WHERE (closed_at IS NULL);

CREATE INDEX IF NOT EXISTS ix_export_job__status ON export_job (tenant_id, status);

CREATE INDEX IF NOT EXISTS ix_business_event__time ON business_event (tenant_id, company_id, occurred_at);

CREATE INDEX IF NOT EXISTS ixp_business_event__campaign ON business_event (tenant_id, company_id, campaign_id, occurred_at) WHERE (campaign_id IS NOT NULL);

CREATE INDEX IF NOT EXISTS ix_business_event__wf ON business_event (tenant_id, company_id, sku_id, wf_id, occurred_at);

CREATE INDEX IF NOT EXISTS ixp_incident_notification__due ON incident_notification (deadline_at) WHERE (notified_at IS NULL);

CREATE INDEX IF NOT EXISTS ixp_inbox__unprocessed ON inbox (tenant_id, received_at) WHERE (processed_at IS NULL);

CREATE INDEX IF NOT EXISTS ixp_portfolio_grant__live ON portfolio_grant (tenant_id, portfolio_id) WHERE (revoked_at IS NULL);

CREATE INDEX IF NOT EXISTS ix_jurisdiction_pack__status ON jurisdiction_pack (jurisdiction, status);

CREATE INDEX IF NOT EXISTS ix_metric_aggregate__lookup ON metric_aggregate (tenant_id, company_id, metric_id, period_start);
