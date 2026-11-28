-- V0003__v12_core_and_enterprise_spine
SET search_path = ge, extensions, public;

SELECT set_config('app.zone', coalesce(nullif(current_setting('app.deployment_region', true), ''), 'IN'), false);

SELECT set_config('app.deployment_region', coalesce(nullif(current_setting('app.deployment_region', true), ''), 'IN'), false);

CREATE TABLE tenant (
  tenant_id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  customer_type text NOT NULL,
  data_region text NOT NULL CHECK (data_region IN ('IN','EU')),      -- CJ-R09, fixed at onboarding
  contract_status text NOT NULL DEFAULT 'pending',
  created_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE organization (
  tenant_id uuid NOT NULL REFERENCES tenant(tenant_id),
  organization_id uuid NOT NULL DEFAULT gen_random_uuid(),
  name text NOT NULL, name_norm text GENERATED ALWAYS AS (lower(btrim(name))) STORED,
  PRIMARY KEY (tenant_id, organization_id), UNIQUE (tenant_id, name_norm)
);

CREATE TABLE company (
  tenant_id uuid NOT NULL, company_id uuid NOT NULL DEFAULT gen_random_uuid(), organization_id uuid NOT NULL,
  legal_name text NOT NULL, registration_country char(2), status text NOT NULL DEFAULT 'active',
  PRIMARY KEY (tenant_id, company_id),
  FOREIGN KEY (tenant_id, organization_id) REFERENCES organization(tenant_id, organization_id)
);

CREATE TABLE division (tenant_id uuid, company_id uuid, division_id uuid DEFAULT gen_random_uuid(), name text NOT NULL,
  PRIMARY KEY (tenant_id, division_id), FOREIGN KEY (tenant_id, company_id) REFERENCES company(tenant_id, company_id));

CREATE TABLE brand (tenant_id uuid, company_id uuid, division_id uuid, brand_id uuid DEFAULT gen_random_uuid(), name text NOT NULL,
  PRIMARY KEY (tenant_id, brand_id), FOREIGN KEY (tenant_id, division_id) REFERENCES division(tenant_id, division_id));

CREATE TABLE offering (tenant_id uuid, company_id uuid, brand_id uuid, offering_id uuid DEFAULT gen_random_uuid(),
  offering_type text NOT NULL, version int NOT NULL DEFAULT 1, status text NOT NULL, claims_ref uuid,
  price_amount numeric(18,4), currency char(3) CHECK (currency ~ '^[A-Z]{3}$'),
  PRIMARY KEY (tenant_id, offering_id), FOREIGN KEY (tenant_id, brand_id) REFERENCES brand(tenant_id, brand_id));

CREATE TABLE market (tenant_id uuid, company_id uuid, market_id uuid DEFAULT gen_random_uuid(), country char(2) NOT NULL,
  region text, timezone text NOT NULL, language text NOT NULL, currency char(3) NOT NULL, jurisdiction_pack_id uuid,
  PRIMARY KEY (tenant_id, market_id), FOREIGN KEY (tenant_id, company_id) REFERENCES company(tenant_id, company_id));

CREATE TABLE channel_account (tenant_id uuid, company_id uuid, account_id uuid DEFAULT gen_random_uuid(), channel text NOT NULL,
  sender_alias text, credential_ref text NOT NULL,          -- secret-manager reference, never the secret
  dlt_entity_id text, dlt_header text, number_series text,  -- CJ-R06 (IN)
  daily_cap int CHECK (daily_cap >= 0), status text NOT NULL,
  PRIMARY KEY (tenant_id, account_id), FOREIGN KEY (tenant_id, company_id) REFERENCES company(tenant_id, company_id));

CREATE TABLE workflow_run (tenant_id uuid, company_id uuid, run_id uuid DEFAULT gen_random_uuid(),
  sku_id text NOT NULL CHECK (sku_id ~ '^SM-SVC-\d{2}$'), wf_id text NOT NULL, wf_version int NOT NULL,
  business_context jsonb NOT NULL, input jsonb NOT NULL, status text NOT NULL
    CHECK (status IN ('Queued','Running','Awaiting approval','Held','Reconciling','Completed','Failed','Canceled')),
  requested_by uuid NOT NULL, reviewed_by uuid, CHECK (reviewed_by IS NULL OR reviewed_by <> requested_by),   -- D10
  idempotency_key text NOT NULL, reserved_units int NOT NULL DEFAULT 0, created_at timestamptz NOT NULL DEFAULT now(),
  PRIMARY KEY (tenant_id, run_id), UNIQUE (tenant_id, idempotency_key),
  FOREIGN KEY (tenant_id, company_id) REFERENCES company(tenant_id, company_id));

CREATE TABLE workflow_step_run (tenant_id uuid, run_id uuid, step_id text, attempt int NOT NULL DEFAULT 1,
  step_class text NOT NULL CHECK (step_class IN ('ai_inference','deterministic','policy_gate','evidence','effect')),
  status text NOT NULL, model_id text, prompt_version text, output jsonb, reason_code text,
  PRIMARY KEY (tenant_id, run_id, step_id, attempt), FOREIGN KEY (tenant_id, run_id) REFERENCES workflow_run(tenant_id, run_id),
  CHECK (step_class = 'ai_inference' OR model_id IS NULL));

CREATE TABLE effect (tenant_id uuid, effect_id uuid DEFAULT gen_random_uuid(), run_id uuid NOT NULL, step_id text NOT NULL,
  idempotency_key text NOT NULL, preflight_verdict text NOT NULL CHECK (preflight_verdict = 'ALLOW'),
  status text NOT NULL CHECK (status IN ('Intended','Dispatched','Reconciling','Confirmed','Failed','Compensated')),
  provider_receipt jsonb, PRIMARY KEY (tenant_id, effect_id), UNIQUE (tenant_id, idempotency_key));

CREATE TABLE outbox (tenant_id uuid, event_id uuid PRIMARY KEY DEFAULT gen_random_uuid(), topic text NOT NULL, payload jsonb NOT NULL,
  created_at timestamptz NOT NULL DEFAULT now(), published_at timestamptz);

CREATE TABLE inbox (provider text, provider_event_id text, tenant_id uuid, received_at timestamptz NOT NULL DEFAULT now(), signature_ok boolean NOT NULL,
  PRIMARY KEY (provider, provider_event_id));

CREATE TABLE audit_event (tenant_id uuid, audit_id bigserial, actor uuid, action text NOT NULL, ref text, policy_version text,
  occurred_at timestamptz NOT NULL DEFAULT now(), PRIMARY KEY (tenant_id, audit_id));

CREATE TABLE portfolio_grant (portfolio_id uuid, tenant_id uuid, company_id uuid, grant_id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  dimensions text[] NOT NULL, expires_at timestamptz, revoked_at timestamptz);

CREATE TABLE fx_rate (rate_id uuid PRIMARY KEY DEFAULT gen_random_uuid(), base_currency char(3), quote_currency char(3),
  effective_at timestamptz NOT NULL, source text NOT NULL, rate numeric(20,10) NOT NULL CHECK (rate > 0), approved_version int NOT NULL);

CREATE TABLE jurisdiction_pack (pack_id uuid PRIMARY KEY DEFAULT gen_random_uuid(), jurisdiction text NOT NULL, version int NOT NULL,
  status text NOT NULL CHECK (status IN ('Draft','Pending legal review','Approved','Retired')), approved_by uuid, approved_at timestamptz,
  effective_from date, effective_to date, UNIQUE (jurisdiction, version));

CREATE TABLE jurisdiction_rule (pack_id uuid REFERENCES jurisdiction_pack(pack_id), rule_id text, channel text, purpose text,
  condition jsonb NOT NULL, effect text NOT NULL CHECK (effect IN ('ALLOW','HOLD','REVIEW','INFO')), legal_source text NOT NULL,
  interpretation_status text NOT NULL, PRIMARY KEY (pack_id, rule_id));

CREATE TABLE consent_record (tenant_id uuid, company_id uuid, consent_id uuid DEFAULT gen_random_uuid(), contact_id uuid NOT NULL,
  market char(2) NOT NULL, channel text NOT NULL, purpose text NOT NULL, basis text NOT NULL, notice_version text NOT NULL,
  captured_at timestamptz NOT NULL, capture_source text NOT NULL, evidence_hash bytea NOT NULL,
  status text NOT NULL CHECK (status IN ('Granted','Withdrawn','Expired')), supersedes uuid,
  PRIMARY KEY (tenant_id, consent_id), FOREIGN KEY (tenant_id, company_id) REFERENCES company(tenant_id, company_id));

CREATE TABLE suppression (tenant_id uuid, company_id uuid, contact_id uuid, channel text, purpose text, reason text NOT NULL,
  created_at timestamptz NOT NULL DEFAULT now(), PRIMARY KEY (tenant_id, company_id, contact_id, channel, purpose));

CREATE TABLE dsar_request (tenant_id uuid, dsar_id uuid DEFAULT gen_random_uuid(), jurisdiction char(2) NOT NULL, request_type text NOT NULL,
  received_at timestamptz NOT NULL, due_at timestamptz NOT NULL, identity_verified_at timestamptz, legal_hold boolean NOT NULL DEFAULT false,
  status text NOT NULL, evidence_ref text, PRIMARY KEY (tenant_id, dsar_id));

CREATE TABLE incident (incident_id uuid PRIMARY KEY DEFAULT gen_random_uuid(), tenant_id uuid, severity text NOT NULL,
  detected_at timestamptz NOT NULL, aware_at timestamptz NOT NULL, personal_data boolean NOT NULL, summary text NOT NULL);

CREATE TABLE incident_notification (incident_id uuid REFERENCES incident(incident_id), authority text, deadline_at timestamptz NOT NULL,
  notified_at timestamptz, evidence_ref text, PRIMARY KEY (incident_id, authority));

CREATE TABLE ai_model (model_id text PRIMARY KEY, tier text NOT NULL, provider text, version text NOT NULL, regions text[] NOT NULL,
  data_classes text[] NOT NULL, context_limit int, dpa_ref text, status text NOT NULL CHECK (status IN ('Candidate','Approved','Suspended','Retired')),
  rollback_to text REFERENCES ai_model(model_id));

CREATE TABLE prompt_version (prompt_id text, version int, agent_id text NOT NULL, task text NOT NULL, template_hash bytea NOT NULL,
  output_schema_ref text NOT NULL, status text NOT NULL, approved_by uuid, PRIMARY KEY (prompt_id, version));

CREATE TABLE eval_suite (suite_id text PRIMARY KEY, wf_id text NOT NULL, languages text[] NOT NULL, case_count int NOT NULL, thresholds jsonb NOT NULL);

CREATE TABLE eval_run (eval_run_id uuid PRIMARY KEY DEFAULT gen_random_uuid(), suite_id text REFERENCES eval_suite(suite_id), model_id text, prompt_id text,
  prompt_version int, metrics jsonb NOT NULL, denominator int NOT NULL, passed boolean NOT NULL, run_at timestamptz NOT NULL DEFAULT now());

CREATE TABLE ai_usage_event (tenant_id uuid, usage_id bigserial, company_id uuid, run_id uuid, step_id text, model_id text NOT NULL,
  prompt_version text, input_tokens int NOT NULL, output_tokens int NOT NULL, cached_tokens int NOT NULL DEFAULT 0,
  latency_ms int, outcome text, occurred_at timestamptz NOT NULL DEFAULT now(), PRIMARY KEY (tenant_id, usage_id));

CREATE TABLE ai_budget (tenant_id uuid, scope_ref text, period text NOT NULL, soft_cap_tokens bigint, hard_cap_tokens bigint NOT NULL,
  PRIMARY KEY (tenant_id, scope_ref, period), CHECK (soft_cap_tokens IS NULL OR soft_cap_tokens <= hard_cap_tokens));

ALTER TABLE organization ENABLE ROW LEVEL SECURITY;

ALTER TABLE organization FORCE ROW LEVEL SECURITY;

ALTER TABLE company ENABLE ROW LEVEL SECURITY;

ALTER TABLE company FORCE ROW LEVEL SECURITY;

ALTER TABLE division ENABLE ROW LEVEL SECURITY;

ALTER TABLE division FORCE ROW LEVEL SECURITY;

ALTER TABLE brand ENABLE ROW LEVEL SECURITY;

ALTER TABLE brand FORCE ROW LEVEL SECURITY;

ALTER TABLE offering ENABLE ROW LEVEL SECURITY;

ALTER TABLE offering FORCE ROW LEVEL SECURITY;

ALTER TABLE market ENABLE ROW LEVEL SECURITY;

ALTER TABLE market FORCE ROW LEVEL SECURITY;

ALTER TABLE channel_account ENABLE ROW LEVEL SECURITY;

ALTER TABLE channel_account FORCE ROW LEVEL SECURITY;

ALTER TABLE workflow_run ENABLE ROW LEVEL SECURITY;

ALTER TABLE workflow_run FORCE ROW LEVEL SECURITY;

ALTER TABLE workflow_step_run ENABLE ROW LEVEL SECURITY;

ALTER TABLE workflow_step_run FORCE ROW LEVEL SECURITY;

ALTER TABLE effect ENABLE ROW LEVEL SECURITY;

ALTER TABLE effect FORCE ROW LEVEL SECURITY;

ALTER TABLE outbox ENABLE ROW LEVEL SECURITY;

ALTER TABLE outbox FORCE ROW LEVEL SECURITY;

ALTER TABLE audit_event ENABLE ROW LEVEL SECURITY;

ALTER TABLE audit_event FORCE ROW LEVEL SECURITY;

ALTER TABLE consent_record ENABLE ROW LEVEL SECURITY;

ALTER TABLE consent_record FORCE ROW LEVEL SECURITY;

ALTER TABLE suppression ENABLE ROW LEVEL SECURITY;

ALTER TABLE suppression FORCE ROW LEVEL SECURITY;

ALTER TABLE dsar_request ENABLE ROW LEVEL SECURITY;

ALTER TABLE dsar_request FORCE ROW LEVEL SECURITY;

ALTER TABLE ai_usage_event ENABLE ROW LEVEL SECURITY;

ALTER TABLE ai_usage_event FORCE ROW LEVEL SECURITY;

ALTER TABLE ai_budget ENABLE ROW LEVEL SECURITY;

ALTER TABLE ai_budget FORCE ROW LEVEL SECURITY;

CREATE TABLE identity_provider (tenant_id uuid PRIMARY KEY REFERENCES tenant(tenant_id), protocol text NOT NULL CHECK (protocol IN ('SAML 2.0','OpenID Connect')),
  sso_url text NOT NULL CHECK (sso_url ~ '^https://'), issuer text NOT NULL, domain text NOT NULL, domain_verified boolean NOT NULL DEFAULT false,
  breakglass_email text, enforced boolean NOT NULL DEFAULT false, mfa_policy text NOT NULL, max_session_hours int NOT NULL CHECK (max_session_hours BETWEEN 1 AND 24),
  idle_minutes int NOT NULL CHECK (idle_minutes BETWEEN 5 AND 120),
  CHECK (NOT enforced OR (domain_verified AND breakglass_email IS NOT NULL)));

CREATE TABLE scim_token (tenant_id uuid NOT NULL REFERENCES tenant(tenant_id), token_id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  token_hash bytea NOT NULL, prefix text NOT NULL, created_at timestamptz NOT NULL DEFAULT now(), revoked_at timestamptz);

CREATE TABLE custom_role (tenant_id uuid NOT NULL REFERENCES tenant(tenant_id), role_id uuid PRIMARY KEY DEFAULT gen_random_uuid(), name text NOT NULL, UNIQUE (tenant_id, name));

CREATE TABLE role_permission (tenant_id uuid NOT NULL, role_id uuid NOT NULL REFERENCES custom_role(role_id), permission text NOT NULL, PRIMARY KEY (role_id, permission));

CREATE TABLE sod_conflict (permission_a text, permission_b text, PRIMARY KEY (permission_a, permission_b));

INSERT INTO sod_conflict VALUES ('Runs:create','Runs:approve'),('Configuration:edit','Configuration:approve'),('Billing:view','Billing:approve'),('Runs:approve','Runs:dispatch');

CREATE FUNCTION enforce_sod() RETURNS trigger LANGUAGE plpgsql AS $$
BEGIN
  IF EXISTS (SELECT 1 FROM role_permission rp JOIN sod_conflict c
             ON (c.permission_a = NEW.permission AND c.permission_b = rp.permission) OR (c.permission_b = NEW.permission AND c.permission_a = rp.permission)
             WHERE rp.role_id = NEW.role_id) THEN
    RAISE EXCEPTION 'separation of duties violation: % conflicts within role', NEW.permission;
  END IF;
  RETURN NEW;
END $$;

CREATE TRIGGER role_permission_sod BEFORE INSERT ON role_permission FOR EACH ROW EXECUTE FUNCTION enforce_sod();

CREATE TABLE api_key (tenant_id uuid NOT NULL REFERENCES tenant(tenant_id), key_id uuid PRIMARY KEY DEFAULT gen_random_uuid(), name text NOT NULL,
  prefix text NOT NULL, last4 char(4) NOT NULL, key_hash bytea NOT NULL,                  -- ENT-API-01: hash only, never plaintext
  scopes text[] NOT NULL CHECK (cardinality(scopes) > 0), ip_allowlist cidr[], expires_at timestamptz NOT NULL, revoked_at timestamptz);

CREATE TABLE webhook_endpoint (tenant_id uuid NOT NULL REFERENCES tenant(tenant_id), endpoint_id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  url text NOT NULL CHECK (url ~ '^https://'), events text[] NOT NULL CHECK (cardinality(events) > 0), secret_ref text NOT NULL, active boolean NOT NULL DEFAULT true);

CREATE TABLE webhook_delivery (tenant_id uuid NOT NULL, delivery_id bigserial PRIMARY KEY, endpoint_id uuid NOT NULL REFERENCES webhook_endpoint(endpoint_id),
  event text NOT NULL, attempt int NOT NULL CHECK (attempt BETWEEN 1 AND 6), status_code int, signed_at timestamptz NOT NULL, delivered_at timestamptz);

CREATE TABLE audit_sink (tenant_id uuid NOT NULL REFERENCES tenant(tenant_id), sink_id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  kind text NOT NULL CHECK (kind IN ('https','syslog-tls','object-storage')), endpoint text NOT NULL CHECK (endpoint ~ '^(https://|syslog-tls://|s3://|gs://|azure://)'),
  format text NOT NULL CHECK (format IN ('JSON','CEF')), retention_years int NOT NULL CHECK (retention_years IN (1,3,7)));

CREATE TABLE export_job (tenant_id uuid NOT NULL REFERENCES tenant(tenant_id), export_id uuid PRIMARY KEY DEFAULT gen_random_uuid(), scope text NOT NULL,
  format text NOT NULL CHECK (format IN ('jsonl','csv','parquet')), requested_by uuid NOT NULL, approved_by uuid,
  status text NOT NULL CHECK (status IN ('Awaiting approval','Running','Ready','Expired')), manifest_hash bytea, expires_at timestamptz,
  CHECK (approved_by IS NULL OR approved_by <> requested_by));

CREATE TABLE tenant_key_config (tenant_id uuid PRIMARY KEY REFERENCES tenant(tenant_id), mode text NOT NULL CHECK (mode IN ('platform','customer')),
  kms_key_ref text, rotation_days int NOT NULL CHECK (rotation_days IN (90,180,365)), CHECK (mode = 'platform' OR kms_key_ref IS NOT NULL));

CREATE TABLE sandbox_environment (tenant_id uuid NOT NULL REFERENCES tenant(tenant_id), sandbox_id uuid PRIMARY KEY DEFAULT gen_random_uuid(), name text NOT NULL,
  copies_configuration boolean NOT NULL, contains_personal_data boolean NOT NULL DEFAULT false CHECK (contains_personal_data = false));

CREATE TABLE config_promotion (tenant_id uuid NOT NULL, promotion_id uuid PRIMARY KEY DEFAULT gen_random_uuid(), sandbox_id uuid NOT NULL REFERENCES sandbox_environment(sandbox_id),
  requested_by uuid NOT NULL, approved_by uuid, status text NOT NULL, CHECK (approved_by IS NULL OR approved_by <> requested_by));

CREATE TABLE connector_installation (tenant_id uuid NOT NULL REFERENCES tenant(tenant_id), installation_id uuid PRIMARY KEY DEFAULT gen_random_uuid(), connector_id text NOT NULL,
  environment text NOT NULL CHECK (environment IN ('sandbox','production')), credential_ref text NOT NULL, legal_review_ref text, security_review_ref text, status text NOT NULL,
  CHECK (environment = 'sandbox' OR (legal_review_ref IS NOT NULL AND security_review_ref IS NOT NULL)));

CREATE TABLE security_finding (finding_id uuid PRIMARY KEY DEFAULT gen_random_uuid(), title text NOT NULL, severity text NOT NULL CHECK (severity IN ('Critical','High','Medium','Low')),
  found_at date NOT NULL, due_at date NOT NULL, closed_at date, evidence_ref text,
  CHECK (due_at <= found_at + CASE severity WHEN 'Critical' THEN 7 WHEN 'High' THEN 30 WHEN 'Medium' THEN 90 ELSE 180 END),
  CHECK (closed_at IS NULL OR evidence_ref IS NOT NULL));

CREATE TABLE ops_incident (incident_id uuid PRIMARY KEY DEFAULT gen_random_uuid(), severity text NOT NULL CHECK (severity IN ('SEV1','SEV2','SEV3','SEV4')),
  title text NOT NULL, declared_at timestamptz NOT NULL, status text NOT NULL CHECK (status IN ('Investigating','Identified','Monitoring','Resolved')), status_message text);

CREATE TABLE tax_rule (rule_id text PRIMARY KEY, jurisdiction text NOT NULL, description text NOT NULL, rate_percent numeric(5,2) CHECK (rate_percent BETWEEN 0 AND 30),
  needs_rate_input boolean NOT NULL DEFAULT false, approved_by text, approved_at date);

CREATE TABLE invoice (tenant_id uuid NOT NULL REFERENCES tenant(tenant_id), invoice_id uuid PRIMARY KEY DEFAULT gen_random_uuid(), number text NOT NULL UNIQUE,
  currency char(3) NOT NULL, net_minor bigint NOT NULL CHECK (net_minor >= 0), tax_minor bigint NOT NULL CHECK (tax_minor >= 0), total_minor bigint NOT NULL,
  tax_rule_id text REFERENCES tax_rule(rule_id), status text NOT NULL, CHECK (total_minor = net_minor + tax_minor));

CREATE TABLE locale_bundle (locale text PRIMARY KEY, direction text NOT NULL CHECK (direction IN ('ltr','rtl')), coverage_percent numeric(5,2) NOT NULL, reviewed_by text);

ALTER TABLE identity_provider ENABLE ROW LEVEL SECURITY;

ALTER TABLE identity_provider FORCE ROW LEVEL SECURITY;

ALTER TABLE scim_token ENABLE ROW LEVEL SECURITY;

ALTER TABLE scim_token FORCE ROW LEVEL SECURITY;

ALTER TABLE custom_role ENABLE ROW LEVEL SECURITY;

ALTER TABLE custom_role FORCE ROW LEVEL SECURITY;

ALTER TABLE role_permission ENABLE ROW LEVEL SECURITY;

ALTER TABLE role_permission FORCE ROW LEVEL SECURITY;

ALTER TABLE api_key ENABLE ROW LEVEL SECURITY;

ALTER TABLE api_key FORCE ROW LEVEL SECURITY;

ALTER TABLE webhook_endpoint ENABLE ROW LEVEL SECURITY;

ALTER TABLE webhook_endpoint FORCE ROW LEVEL SECURITY;

ALTER TABLE webhook_delivery ENABLE ROW LEVEL SECURITY;

ALTER TABLE webhook_delivery FORCE ROW LEVEL SECURITY;

ALTER TABLE audit_sink ENABLE ROW LEVEL SECURITY;

ALTER TABLE audit_sink FORCE ROW LEVEL SECURITY;

ALTER TABLE export_job ENABLE ROW LEVEL SECURITY;

ALTER TABLE export_job FORCE ROW LEVEL SECURITY;

ALTER TABLE tenant_key_config ENABLE ROW LEVEL SECURITY;

ALTER TABLE tenant_key_config FORCE ROW LEVEL SECURITY;

ALTER TABLE sandbox_environment ENABLE ROW LEVEL SECURITY;

ALTER TABLE sandbox_environment FORCE ROW LEVEL SECURITY;

ALTER TABLE config_promotion ENABLE ROW LEVEL SECURITY;

ALTER TABLE config_promotion FORCE ROW LEVEL SECURITY;

ALTER TABLE connector_installation ENABLE ROW LEVEL SECURITY;

ALTER TABLE connector_installation FORCE ROW LEVEL SECURITY;

ALTER TABLE invoice ENABLE ROW LEVEL SECURITY;

ALTER TABLE invoice FORCE ROW LEVEL SECURITY;
