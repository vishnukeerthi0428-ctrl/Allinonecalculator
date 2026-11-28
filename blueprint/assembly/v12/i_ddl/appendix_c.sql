-- Proposed PostgreSQL 16 DDL (V7). Not applied. Requires data-architecture approval (MT-36).
-- Convention: every tenant-scoped table has tenant_id; company-scoped tables add company_id with composite FK.
-- The application connects as role app_user (NOT the owner) and sets: SET LOCAL app.tenant_id = '<uuid>'; SET LOCAL app.company_ids = '{...}';
CREATE EXTENSION IF NOT EXISTS pgcrypto;
-- skipped vector   -- pgvector, only when approved

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
  CHECK (step_class = 'ai_inference' OR model_id IS NULL));   -- AIX-01
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

-- ---------- V7 compliance (CJ-R01…R20)
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

-- ---------- V7 AI governance (AIX-01…20)
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

-- ---------- Row-level security (SEC-02, MT-01)
ALTER TABLE organization ENABLE ROW LEVEL SECURITY; ALTER TABLE organization FORCE ROW LEVEL SECURITY;
CREATE POLICY organization_tenant ON organization USING (tenant_id = current_setting('app.tenant_id')::uuid) WITH CHECK (tenant_id = current_setting('app.tenant_id')::uuid);
ALTER TABLE company ENABLE ROW LEVEL SECURITY; ALTER TABLE company FORCE ROW LEVEL SECURITY;
CREATE POLICY company_tenant ON company USING (tenant_id = current_setting('app.tenant_id')::uuid) WITH CHECK (tenant_id = current_setting('app.tenant_id')::uuid);
ALTER TABLE division ENABLE ROW LEVEL SECURITY; ALTER TABLE division FORCE ROW LEVEL SECURITY;
CREATE POLICY division_tenant ON division USING (tenant_id = current_setting('app.tenant_id')::uuid) WITH CHECK (tenant_id = current_setting('app.tenant_id')::uuid);
ALTER TABLE brand ENABLE ROW LEVEL SECURITY; ALTER TABLE brand FORCE ROW LEVEL SECURITY;
CREATE POLICY brand_tenant ON brand USING (tenant_id = current_setting('app.tenant_id')::uuid) WITH CHECK (tenant_id = current_setting('app.tenant_id')::uuid);
ALTER TABLE offering ENABLE ROW LEVEL SECURITY; ALTER TABLE offering FORCE ROW LEVEL SECURITY;
CREATE POLICY offering_tenant ON offering USING (tenant_id = current_setting('app.tenant_id')::uuid) WITH CHECK (tenant_id = current_setting('app.tenant_id')::uuid);
ALTER TABLE market ENABLE ROW LEVEL SECURITY; ALTER TABLE market FORCE ROW LEVEL SECURITY;
CREATE POLICY market_tenant ON market USING (tenant_id = current_setting('app.tenant_id')::uuid) WITH CHECK (tenant_id = current_setting('app.tenant_id')::uuid);
ALTER TABLE channel_account ENABLE ROW LEVEL SECURITY; ALTER TABLE channel_account FORCE ROW LEVEL SECURITY;
CREATE POLICY channel_account_tenant ON channel_account USING (tenant_id = current_setting('app.tenant_id')::uuid) WITH CHECK (tenant_id = current_setting('app.tenant_id')::uuid);
ALTER TABLE workflow_run ENABLE ROW LEVEL SECURITY; ALTER TABLE workflow_run FORCE ROW LEVEL SECURITY;
CREATE POLICY workflow_run_tenant ON workflow_run USING (tenant_id = current_setting('app.tenant_id')::uuid) WITH CHECK (tenant_id = current_setting('app.tenant_id')::uuid);
ALTER TABLE workflow_step_run ENABLE ROW LEVEL SECURITY; ALTER TABLE workflow_step_run FORCE ROW LEVEL SECURITY;
CREATE POLICY workflow_step_run_tenant ON workflow_step_run USING (tenant_id = current_setting('app.tenant_id')::uuid) WITH CHECK (tenant_id = current_setting('app.tenant_id')::uuid);
ALTER TABLE effect ENABLE ROW LEVEL SECURITY; ALTER TABLE effect FORCE ROW LEVEL SECURITY;
CREATE POLICY effect_tenant ON effect USING (tenant_id = current_setting('app.tenant_id')::uuid) WITH CHECK (tenant_id = current_setting('app.tenant_id')::uuid);
ALTER TABLE outbox ENABLE ROW LEVEL SECURITY; ALTER TABLE outbox FORCE ROW LEVEL SECURITY;
CREATE POLICY outbox_tenant ON outbox USING (tenant_id = current_setting('app.tenant_id')::uuid) WITH CHECK (tenant_id = current_setting('app.tenant_id')::uuid);
ALTER TABLE audit_event ENABLE ROW LEVEL SECURITY; ALTER TABLE audit_event FORCE ROW LEVEL SECURITY;
CREATE POLICY audit_event_tenant ON audit_event USING (tenant_id = current_setting('app.tenant_id')::uuid) WITH CHECK (tenant_id = current_setting('app.tenant_id')::uuid);
ALTER TABLE consent_record ENABLE ROW LEVEL SECURITY; ALTER TABLE consent_record FORCE ROW LEVEL SECURITY;
CREATE POLICY consent_record_tenant ON consent_record USING (tenant_id = current_setting('app.tenant_id')::uuid) WITH CHECK (tenant_id = current_setting('app.tenant_id')::uuid);
ALTER TABLE suppression ENABLE ROW LEVEL SECURITY; ALTER TABLE suppression FORCE ROW LEVEL SECURITY;
CREATE POLICY suppression_tenant ON suppression USING (tenant_id = current_setting('app.tenant_id')::uuid) WITH CHECK (tenant_id = current_setting('app.tenant_id')::uuid);
ALTER TABLE dsar_request ENABLE ROW LEVEL SECURITY; ALTER TABLE dsar_request FORCE ROW LEVEL SECURITY;
CREATE POLICY dsar_request_tenant ON dsar_request USING (tenant_id = current_setting('app.tenant_id')::uuid) WITH CHECK (tenant_id = current_setting('app.tenant_id')::uuid);
ALTER TABLE ai_usage_event ENABLE ROW LEVEL SECURITY; ALTER TABLE ai_usage_event FORCE ROW LEVEL SECURITY;
CREATE POLICY ai_usage_event_tenant ON ai_usage_event USING (tenant_id = current_setting('app.tenant_id')::uuid) WITH CHECK (tenant_id = current_setting('app.tenant_id')::uuid);
ALTER TABLE ai_budget ENABLE ROW LEVEL SECURITY; ALTER TABLE ai_budget FORCE ROW LEVEL SECURITY;
CREATE POLICY ai_budget_tenant ON ai_budget USING (tenant_id = current_setting('app.tenant_id')::uuid) WITH CHECK (tenant_id = current_setting('app.tenant_id')::uuid);
-- Missing context fails closed: current_setting raises when app.tenant_id is unset.

-- ---------- Domain tables referenced by the 156 workflows: common scoped shape; payload validated by Appendix B schemas.
CREATE TABLE growth_source (tenant_id uuid NOT NULL, company_id uuid NOT NULL, id uuid NOT NULL DEFAULT gen_random_uuid(),
  schema_ref text NOT NULL, version int NOT NULL DEFAULT 1, status text NOT NULL, payload jsonb NOT NULL,
  evidence_refs uuid[] NOT NULL DEFAULT '{}', created_by uuid NOT NULL, created_at timestamptz NOT NULL DEFAULT now(), updated_at timestamptz,
  PRIMARY KEY (tenant_id, id), FOREIGN KEY (tenant_id, company_id) REFERENCES company(tenant_id, company_id));  -- SM-SVC-01-WF01, SM-SVC-01-WF02, SM-SVC-01-WF03, SM-SVC-01-WF04, SM-SVC-02-WF01, SM-SVC-02-WF02, SM-SVC-02-WF03, SM-SVC-02-WF04, SM-SVC-12-WF01, SM-SVC-12-WF02, 
ALTER TABLE growth_source ENABLE ROW LEVEL SECURITY; ALTER TABLE growth_source FORCE ROW LEVEL SECURITY;
CREATE POLICY growth_source_tenant ON growth_source USING (tenant_id = current_setting('app.tenant_id')::uuid) WITH CHECK (tenant_id = current_setting('app.tenant_id')::uuid);
CREATE TABLE growth_source_policy (tenant_id uuid NOT NULL, company_id uuid NOT NULL, id uuid NOT NULL DEFAULT gen_random_uuid(),
  schema_ref text NOT NULL, version int NOT NULL DEFAULT 1, status text NOT NULL, payload jsonb NOT NULL,
  evidence_refs uuid[] NOT NULL DEFAULT '{}', created_by uuid NOT NULL, created_at timestamptz NOT NULL DEFAULT now(), updated_at timestamptz,
  PRIMARY KEY (tenant_id, id), FOREIGN KEY (tenant_id, company_id) REFERENCES company(tenant_id, company_id));  -- SM-SVC-01-WF01, SM-SVC-01-WF02, SM-SVC-01-WF03, SM-SVC-01-WF04, SM-SVC-02-WF01, SM-SVC-02-WF02, SM-SVC-02-WF03, SM-SVC-02-WF04, SM-SVC-12-WF01, SM-SVC-12-WF02, 
ALTER TABLE growth_source_policy ENABLE ROW LEVEL SECURITY; ALTER TABLE growth_source_policy FORCE ROW LEVEL SECURITY;
CREATE POLICY growth_source_policy_tenant ON growth_source_policy USING (tenant_id = current_setting('app.tenant_id')::uuid) WITH CHECK (tenant_id = current_setting('app.tenant_id')::uuid);
CREATE TABLE growth_source_record (tenant_id uuid NOT NULL, company_id uuid NOT NULL, id uuid NOT NULL DEFAULT gen_random_uuid(),
  schema_ref text NOT NULL, version int NOT NULL DEFAULT 1, status text NOT NULL, payload jsonb NOT NULL,
  evidence_refs uuid[] NOT NULL DEFAULT '{}', created_by uuid NOT NULL, created_at timestamptz NOT NULL DEFAULT now(), updated_at timestamptz,
  PRIMARY KEY (tenant_id, id), FOREIGN KEY (tenant_id, company_id) REFERENCES company(tenant_id, company_id));  -- SM-SVC-01-WF01, SM-SVC-01-WF02, SM-SVC-01-WF03, SM-SVC-01-WF04, SM-SVC-02-WF01, SM-SVC-02-WF02, SM-SVC-02-WF03, SM-SVC-02-WF04, SM-SVC-12-WF01, SM-SVC-12-WF02, 
ALTER TABLE growth_source_record ENABLE ROW LEVEL SECURITY; ALTER TABLE growth_source_record FORCE ROW LEVEL SECURITY;
CREATE POLICY growth_source_record_tenant ON growth_source_record USING (tenant_id = current_setting('app.tenant_id')::uuid) WITH CHECK (tenant_id = current_setting('app.tenant_id')::uuid);
CREATE TABLE growth_evidence (tenant_id uuid NOT NULL, company_id uuid NOT NULL, id uuid NOT NULL DEFAULT gen_random_uuid(),
  schema_ref text NOT NULL, version int NOT NULL DEFAULT 1, status text NOT NULL, payload jsonb NOT NULL,
  evidence_refs uuid[] NOT NULL DEFAULT '{}', created_by uuid NOT NULL, created_at timestamptz NOT NULL DEFAULT now(), updated_at timestamptz,
  PRIMARY KEY (tenant_id, id), FOREIGN KEY (tenant_id, company_id) REFERENCES company(tenant_id, company_id));  -- SM-SVC-01-WF01, SM-SVC-01-WF02, SM-SVC-01-WF03, SM-SVC-01-WF04, SM-SVC-02-WF01, SM-SVC-02-WF02, SM-SVC-02-WF03, SM-SVC-02-WF04, SM-SVC-19-WF01, SM-SVC-19-WF02, 
ALTER TABLE growth_evidence ENABLE ROW LEVEL SECURITY; ALTER TABLE growth_evidence FORCE ROW LEVEL SECURITY;
CREATE POLICY growth_evidence_tenant ON growth_evidence USING (tenant_id = current_setting('app.tenant_id')::uuid) WITH CHECK (tenant_id = current_setting('app.tenant_id')::uuid);
CREATE TABLE growth_competitor (tenant_id uuid NOT NULL, company_id uuid NOT NULL, id uuid NOT NULL DEFAULT gen_random_uuid(),
  schema_ref text NOT NULL, version int NOT NULL DEFAULT 1, status text NOT NULL, payload jsonb NOT NULL,
  evidence_refs uuid[] NOT NULL DEFAULT '{}', created_by uuid NOT NULL, created_at timestamptz NOT NULL DEFAULT now(), updated_at timestamptz,
  PRIMARY KEY (tenant_id, id), FOREIGN KEY (tenant_id, company_id) REFERENCES company(tenant_id, company_id));  -- SM-SVC-01-WF01, SM-SVC-01-WF02, SM-SVC-01-WF03, SM-SVC-01-WF04
ALTER TABLE growth_competitor ENABLE ROW LEVEL SECURITY; ALTER TABLE growth_competitor FORCE ROW LEVEL SECURITY;
CREATE POLICY growth_competitor_tenant ON growth_competitor USING (tenant_id = current_setting('app.tenant_id')::uuid) WITH CHECK (tenant_id = current_setting('app.tenant_id')::uuid);
CREATE TABLE growth_market_event (tenant_id uuid NOT NULL, company_id uuid NOT NULL, id uuid NOT NULL DEFAULT gen_random_uuid(),
  schema_ref text NOT NULL, version int NOT NULL DEFAULT 1, status text NOT NULL, payload jsonb NOT NULL,
  evidence_refs uuid[] NOT NULL DEFAULT '{}', created_by uuid NOT NULL, created_at timestamptz NOT NULL DEFAULT now(), updated_at timestamptz,
  PRIMARY KEY (tenant_id, id), FOREIGN KEY (tenant_id, company_id) REFERENCES company(tenant_id, company_id));  -- SM-SVC-01-WF01, SM-SVC-01-WF02, SM-SVC-01-WF03, SM-SVC-01-WF04
ALTER TABLE growth_market_event ENABLE ROW LEVEL SECURITY; ALTER TABLE growth_market_event FORCE ROW LEVEL SECURITY;
CREATE POLICY growth_market_event_tenant ON growth_market_event USING (tenant_id = current_setting('app.tenant_id')::uuid) WITH CHECK (tenant_id = current_setting('app.tenant_id')::uuid);
CREATE TABLE growth_search_plan (tenant_id uuid NOT NULL, company_id uuid NOT NULL, id uuid NOT NULL DEFAULT gen_random_uuid(),
  schema_ref text NOT NULL, version int NOT NULL DEFAULT 1, status text NOT NULL, payload jsonb NOT NULL,
  evidence_refs uuid[] NOT NULL DEFAULT '{}', created_by uuid NOT NULL, created_at timestamptz NOT NULL DEFAULT now(), updated_at timestamptz,
  PRIMARY KEY (tenant_id, id), FOREIGN KEY (tenant_id, company_id) REFERENCES company(tenant_id, company_id));  -- SM-SVC-02-WF01, SM-SVC-02-WF02, SM-SVC-02-WF03, SM-SVC-02-WF04
ALTER TABLE growth_search_plan ENABLE ROW LEVEL SECURITY; ALTER TABLE growth_search_plan FORCE ROW LEVEL SECURITY;
CREATE POLICY growth_search_plan_tenant ON growth_search_plan USING (tenant_id = current_setting('app.tenant_id')::uuid) WITH CHECK (tenant_id = current_setting('app.tenant_id')::uuid);
CREATE TABLE growth_organization (tenant_id uuid NOT NULL, company_id uuid NOT NULL, id uuid NOT NULL DEFAULT gen_random_uuid(),
  schema_ref text NOT NULL, version int NOT NULL DEFAULT 1, status text NOT NULL, payload jsonb NOT NULL,
  evidence_refs uuid[] NOT NULL DEFAULT '{}', created_by uuid NOT NULL, created_at timestamptz NOT NULL DEFAULT now(), updated_at timestamptz,
  PRIMARY KEY (tenant_id, id), FOREIGN KEY (tenant_id, company_id) REFERENCES company(tenant_id, company_id));  -- SM-SVC-02-WF01, SM-SVC-02-WF02, SM-SVC-02-WF03, SM-SVC-02-WF04, SM-SVC-03-WF01, SM-SVC-03-WF02, SM-SVC-03-WF03, SM-SVC-03-WF04
ALTER TABLE growth_organization ENABLE ROW LEVEL SECURITY; ALTER TABLE growth_organization FORCE ROW LEVEL SECURITY;
CREATE POLICY growth_organization_tenant ON growth_organization USING (tenant_id = current_setting('app.tenant_id')::uuid) WITH CHECK (tenant_id = current_setting('app.tenant_id')::uuid);
CREATE TABLE growth_signal (tenant_id uuid NOT NULL, company_id uuid NOT NULL, id uuid NOT NULL DEFAULT gen_random_uuid(),
  schema_ref text NOT NULL, version int NOT NULL DEFAULT 1, status text NOT NULL, payload jsonb NOT NULL,
  evidence_refs uuid[] NOT NULL DEFAULT '{}', created_by uuid NOT NULL, created_at timestamptz NOT NULL DEFAULT now(), updated_at timestamptz,
  PRIMARY KEY (tenant_id, id), FOREIGN KEY (tenant_id, company_id) REFERENCES company(tenant_id, company_id));  -- SM-SVC-02-WF01, SM-SVC-02-WF02, SM-SVC-02-WF03, SM-SVC-02-WF04, SM-SVC-12-WF01, SM-SVC-12-WF02, SM-SVC-12-WF03, SM-SVC-12-WF04
ALTER TABLE growth_signal ENABLE ROW LEVEL SECURITY; ALTER TABLE growth_signal FORCE ROW LEVEL SECURITY;
CREATE POLICY growth_signal_tenant ON growth_signal USING (tenant_id = current_setting('app.tenant_id')::uuid) WITH CHECK (tenant_id = current_setting('app.tenant_id')::uuid);
CREATE TABLE growth_signal_type (tenant_id uuid NOT NULL, company_id uuid NOT NULL, id uuid NOT NULL DEFAULT gen_random_uuid(),
  schema_ref text NOT NULL, version int NOT NULL DEFAULT 1, status text NOT NULL, payload jsonb NOT NULL,
  evidence_refs uuid[] NOT NULL DEFAULT '{}', created_by uuid NOT NULL, created_at timestamptz NOT NULL DEFAULT now(), updated_at timestamptz,
  PRIMARY KEY (tenant_id, id), FOREIGN KEY (tenant_id, company_id) REFERENCES company(tenant_id, company_id));  -- SM-SVC-02-WF01, SM-SVC-02-WF02, SM-SVC-02-WF03, SM-SVC-02-WF04
ALTER TABLE growth_signal_type ENABLE ROW LEVEL SECURITY; ALTER TABLE growth_signal_type FORCE ROW LEVEL SECURITY;
CREATE POLICY growth_signal_type_tenant ON growth_signal_type USING (tenant_id = current_setting('app.tenant_id')::uuid) WITH CHECK (tenant_id = current_setting('app.tenant_id')::uuid);
CREATE TABLE growth_need_evidence (tenant_id uuid NOT NULL, company_id uuid NOT NULL, id uuid NOT NULL DEFAULT gen_random_uuid(),
  schema_ref text NOT NULL, version int NOT NULL DEFAULT 1, status text NOT NULL, payload jsonb NOT NULL,
  evidence_refs uuid[] NOT NULL DEFAULT '{}', created_by uuid NOT NULL, created_at timestamptz NOT NULL DEFAULT now(), updated_at timestamptz,
  PRIMARY KEY (tenant_id, id), FOREIGN KEY (tenant_id, company_id) REFERENCES company(tenant_id, company_id));  -- SM-SVC-02-WF01, SM-SVC-02-WF02, SM-SVC-02-WF03, SM-SVC-02-WF04, SM-SVC-04-WF01, SM-SVC-04-WF02, SM-SVC-04-WF03, SM-SVC-04-WF04
ALTER TABLE growth_need_evidence ENABLE ROW LEVEL SECURITY; ALTER TABLE growth_need_evidence FORCE ROW LEVEL SECURITY;
CREATE POLICY growth_need_evidence_tenant ON growth_need_evidence USING (tenant_id = current_setting('app.tenant_id')::uuid) WITH CHECK (tenant_id = current_setting('app.tenant_id')::uuid);
CREATE TABLE growth_referral (tenant_id uuid NOT NULL, company_id uuid NOT NULL, id uuid NOT NULL DEFAULT gen_random_uuid(),
  schema_ref text NOT NULL, version int NOT NULL DEFAULT 1, status text NOT NULL, payload jsonb NOT NULL,
  evidence_refs uuid[] NOT NULL DEFAULT '{}', created_by uuid NOT NULL, created_at timestamptz NOT NULL DEFAULT now(), updated_at timestamptz,
  PRIMARY KEY (tenant_id, id), FOREIGN KEY (tenant_id, company_id) REFERENCES company(tenant_id, company_id));  -- SM-SVC-02-WF01, SM-SVC-02-WF02, SM-SVC-02-WF03, SM-SVC-02-WF04, SM-SVC-16-WF01, SM-SVC-16-WF02, SM-SVC-16-WF03, SM-SVC-16-WF04, SM-SVC-32-WF01, SM-SVC-32-WF02, 
ALTER TABLE growth_referral ENABLE ROW LEVEL SECURITY; ALTER TABLE growth_referral FORCE ROW LEVEL SECURITY;
CREATE POLICY growth_referral_tenant ON growth_referral USING (tenant_id = current_setting('app.tenant_id')::uuid) WITH CHECK (tenant_id = current_setting('app.tenant_id')::uuid);
CREATE TABLE growth_contact (tenant_id uuid NOT NULL, company_id uuid NOT NULL, id uuid NOT NULL DEFAULT gen_random_uuid(),
  schema_ref text NOT NULL, version int NOT NULL DEFAULT 1, status text NOT NULL, payload jsonb NOT NULL,
  evidence_refs uuid[] NOT NULL DEFAULT '{}', created_by uuid NOT NULL, created_at timestamptz NOT NULL DEFAULT now(), updated_at timestamptz,
  PRIMARY KEY (tenant_id, id), FOREIGN KEY (tenant_id, company_id) REFERENCES company(tenant_id, company_id));  -- SM-SVC-03-WF01, SM-SVC-03-WF02, SM-SVC-03-WF03, SM-SVC-03-WF04, SM-SVC-29-WF01, SM-SVC-29-WF02, SM-SVC-29-WF03, SM-SVC-29-WF04
ALTER TABLE growth_contact ENABLE ROW LEVEL SECURITY; ALTER TABLE growth_contact FORCE ROW LEVEL SECURITY;
CREATE POLICY growth_contact_tenant ON growth_contact USING (tenant_id = current_setting('app.tenant_id')::uuid) WITH CHECK (tenant_id = current_setting('app.tenant_id')::uuid);
CREATE TABLE growth_contact_source (tenant_id uuid NOT NULL, company_id uuid NOT NULL, id uuid NOT NULL DEFAULT gen_random_uuid(),
  schema_ref text NOT NULL, version int NOT NULL DEFAULT 1, status text NOT NULL, payload jsonb NOT NULL,
  evidence_refs uuid[] NOT NULL DEFAULT '{}', created_by uuid NOT NULL, created_at timestamptz NOT NULL DEFAULT now(), updated_at timestamptz,
  PRIMARY KEY (tenant_id, id), FOREIGN KEY (tenant_id, company_id) REFERENCES company(tenant_id, company_id));  -- SM-SVC-03-WF01, SM-SVC-03-WF02, SM-SVC-03-WF03, SM-SVC-03-WF04, SM-SVC-29-WF01, SM-SVC-29-WF02, SM-SVC-29-WF03, SM-SVC-29-WF04
ALTER TABLE growth_contact_source ENABLE ROW LEVEL SECURITY; ALTER TABLE growth_contact_source FORCE ROW LEVEL SECURITY;
CREATE POLICY growth_contact_source_tenant ON growth_contact_source USING (tenant_id = current_setting('app.tenant_id')::uuid) WITH CHECK (tenant_id = current_setting('app.tenant_id')::uuid);
CREATE TABLE growth_contact_verification (tenant_id uuid NOT NULL, company_id uuid NOT NULL, id uuid NOT NULL DEFAULT gen_random_uuid(),
  schema_ref text NOT NULL, version int NOT NULL DEFAULT 1, status text NOT NULL, payload jsonb NOT NULL,
  evidence_refs uuid[] NOT NULL DEFAULT '{}', created_by uuid NOT NULL, created_at timestamptz NOT NULL DEFAULT now(), updated_at timestamptz,
  PRIMARY KEY (tenant_id, id), FOREIGN KEY (tenant_id, company_id) REFERENCES company(tenant_id, company_id));  -- SM-SVC-03-WF01, SM-SVC-03-WF02, SM-SVC-03-WF03, SM-SVC-03-WF04, SM-SVC-29-WF01, SM-SVC-29-WF02, SM-SVC-29-WF03, SM-SVC-29-WF04
ALTER TABLE growth_contact_verification ENABLE ROW LEVEL SECURITY; ALTER TABLE growth_contact_verification FORCE ROW LEVEL SECURITY;
CREATE POLICY growth_contact_verification_tenant ON growth_contact_verification USING (tenant_id = current_setting('app.tenant_id')::uuid) WITH CHECK (tenant_id = current_setting('app.tenant_id')::uuid);
CREATE TABLE growth_consent (tenant_id uuid NOT NULL, company_id uuid NOT NULL, id uuid NOT NULL DEFAULT gen_random_uuid(),
  schema_ref text NOT NULL, version int NOT NULL DEFAULT 1, status text NOT NULL, payload jsonb NOT NULL,
  evidence_refs uuid[] NOT NULL DEFAULT '{}', created_by uuid NOT NULL, created_at timestamptz NOT NULL DEFAULT now(), updated_at timestamptz,
  PRIMARY KEY (tenant_id, id), FOREIGN KEY (tenant_id, company_id) REFERENCES company(tenant_id, company_id));  -- SM-SVC-03-WF01, SM-SVC-03-WF02, SM-SVC-03-WF03, SM-SVC-03-WF04, SM-SVC-06-WF01, SM-SVC-06-WF02, SM-SVC-06-WF03, SM-SVC-06-WF04, SM-SVC-07-WF01, SM-SVC-07-WF02, 
ALTER TABLE growth_consent ENABLE ROW LEVEL SECURITY; ALTER TABLE growth_consent FORCE ROW LEVEL SECURITY;
CREATE POLICY growth_consent_tenant ON growth_consent USING (tenant_id = current_setting('app.tenant_id')::uuid) WITH CHECK (tenant_id = current_setting('app.tenant_id')::uuid);
CREATE TABLE growth_suppression (tenant_id uuid NOT NULL, company_id uuid NOT NULL, id uuid NOT NULL DEFAULT gen_random_uuid(),
  schema_ref text NOT NULL, version int NOT NULL DEFAULT 1, status text NOT NULL, payload jsonb NOT NULL,
  evidence_refs uuid[] NOT NULL DEFAULT '{}', created_by uuid NOT NULL, created_at timestamptz NOT NULL DEFAULT now(), updated_at timestamptz,
  PRIMARY KEY (tenant_id, id), FOREIGN KEY (tenant_id, company_id) REFERENCES company(tenant_id, company_id));  -- SM-SVC-03-WF01, SM-SVC-03-WF02, SM-SVC-03-WF03, SM-SVC-03-WF04, SM-SVC-06-WF01, SM-SVC-06-WF02, SM-SVC-06-WF03, SM-SVC-06-WF04, SM-SVC-07-WF01, SM-SVC-07-WF02, 
ALTER TABLE growth_suppression ENABLE ROW LEVEL SECURITY; ALTER TABLE growth_suppression FORCE ROW LEVEL SECURITY;
CREATE POLICY growth_suppression_tenant ON growth_suppression USING (tenant_id = current_setting('app.tenant_id')::uuid) WITH CHECK (tenant_id = current_setting('app.tenant_id')::uuid);
CREATE TABLE growth_need (tenant_id uuid NOT NULL, company_id uuid NOT NULL, id uuid NOT NULL DEFAULT gen_random_uuid(),
  schema_ref text NOT NULL, version int NOT NULL DEFAULT 1, status text NOT NULL, payload jsonb NOT NULL,
  evidence_refs uuid[] NOT NULL DEFAULT '{}', created_by uuid NOT NULL, created_at timestamptz NOT NULL DEFAULT now(), updated_at timestamptz,
  PRIMARY KEY (tenant_id, id), FOREIGN KEY (tenant_id, company_id) REFERENCES company(tenant_id, company_id));  -- SM-SVC-04-WF01, SM-SVC-04-WF02, SM-SVC-04-WF03, SM-SVC-04-WF04
ALTER TABLE growth_need ENABLE ROW LEVEL SECURITY; ALTER TABLE growth_need FORCE ROW LEVEL SECURITY;
CREATE POLICY growth_need_tenant ON growth_need USING (tenant_id = current_setting('app.tenant_id')::uuid) WITH CHECK (tenant_id = current_setting('app.tenant_id')::uuid);
CREATE TABLE growth_product (tenant_id uuid NOT NULL, company_id uuid NOT NULL, id uuid NOT NULL DEFAULT gen_random_uuid(),
  schema_ref text NOT NULL, version int NOT NULL DEFAULT 1, status text NOT NULL, payload jsonb NOT NULL,
  evidence_refs uuid[] NOT NULL DEFAULT '{}', created_by uuid NOT NULL, created_at timestamptz NOT NULL DEFAULT now(), updated_at timestamptz,
  PRIMARY KEY (tenant_id, id), FOREIGN KEY (tenant_id, company_id) REFERENCES company(tenant_id, company_id));  -- SM-SVC-04-WF01, SM-SVC-04-WF02, SM-SVC-04-WF03, SM-SVC-04-WF04, SM-SVC-25-WF01, SM-SVC-25-WF02, SM-SVC-25-WF03, SM-SVC-25-WF04, SM-SVC-28-WF01, SM-SVC-28-WF02, 
ALTER TABLE growth_product ENABLE ROW LEVEL SECURITY; ALTER TABLE growth_product FORCE ROW LEVEL SECURITY;
CREATE POLICY growth_product_tenant ON growth_product USING (tenant_id = current_setting('app.tenant_id')::uuid) WITH CHECK (tenant_id = current_setting('app.tenant_id')::uuid);
CREATE TABLE growth_opportunity (tenant_id uuid NOT NULL, company_id uuid NOT NULL, id uuid NOT NULL DEFAULT gen_random_uuid(),
  schema_ref text NOT NULL, version int NOT NULL DEFAULT 1, status text NOT NULL, payload jsonb NOT NULL,
  evidence_refs uuid[] NOT NULL DEFAULT '{}', created_by uuid NOT NULL, created_at timestamptz NOT NULL DEFAULT now(), updated_at timestamptz,
  PRIMARY KEY (tenant_id, id), FOREIGN KEY (tenant_id, company_id) REFERENCES company(tenant_id, company_id));  -- SM-SVC-04-WF01, SM-SVC-04-WF02, SM-SVC-04-WF03, SM-SVC-04-WF04, SM-SVC-05-WF01, SM-SVC-05-WF02, SM-SVC-05-WF03, SM-SVC-05-WF04, SM-SVC-19-WF01, SM-SVC-19-WF02, 
ALTER TABLE growth_opportunity ENABLE ROW LEVEL SECURITY; ALTER TABLE growth_opportunity FORCE ROW LEVEL SECURITY;
CREATE POLICY growth_opportunity_tenant ON growth_opportunity USING (tenant_id = current_setting('app.tenant_id')::uuid) WITH CHECK (tenant_id = current_setting('app.tenant_id')::uuid);
CREATE TABLE growth_score_version (tenant_id uuid NOT NULL, company_id uuid NOT NULL, id uuid NOT NULL DEFAULT gen_random_uuid(),
  schema_ref text NOT NULL, version int NOT NULL DEFAULT 1, status text NOT NULL, payload jsonb NOT NULL,
  evidence_refs uuid[] NOT NULL DEFAULT '{}', created_by uuid NOT NULL, created_at timestamptz NOT NULL DEFAULT now(), updated_at timestamptz,
  PRIMARY KEY (tenant_id, id), FOREIGN KEY (tenant_id, company_id) REFERENCES company(tenant_id, company_id));  -- SM-SVC-04-WF01, SM-SVC-04-WF02, SM-SVC-04-WF03, SM-SVC-04-WF04
ALTER TABLE growth_score_version ENABLE ROW LEVEL SECURITY; ALTER TABLE growth_score_version FORCE ROW LEVEL SECURITY;
CREATE POLICY growth_score_version_tenant ON growth_score_version USING (tenant_id = current_setting('app.tenant_id')::uuid) WITH CHECK (tenant_id = current_setting('app.tenant_id')::uuid);
CREATE TABLE growth_activity (tenant_id uuid NOT NULL, company_id uuid NOT NULL, id uuid NOT NULL DEFAULT gen_random_uuid(),
  schema_ref text NOT NULL, version int NOT NULL DEFAULT 1, status text NOT NULL, payload jsonb NOT NULL,
  evidence_refs uuid[] NOT NULL DEFAULT '{}', created_by uuid NOT NULL, created_at timestamptz NOT NULL DEFAULT now(), updated_at timestamptz,
  PRIMARY KEY (tenant_id, id), FOREIGN KEY (tenant_id, company_id) REFERENCES company(tenant_id, company_id));  -- SM-SVC-05-WF01, SM-SVC-05-WF02, SM-SVC-05-WF03, SM-SVC-05-WF04, SM-SVC-09-WF01, SM-SVC-09-WF02, SM-SVC-09-WF03, SM-SVC-09-WF04, SM-SVC-26-WF01, SM-SVC-26-WF02, 
ALTER TABLE growth_activity ENABLE ROW LEVEL SECURITY; ALTER TABLE growth_activity FORCE ROW LEVEL SECURITY;
CREATE POLICY growth_activity_tenant ON growth_activity USING (tenant_id = current_setting('app.tenant_id')::uuid) WITH CHECK (tenant_id = current_setting('app.tenant_id')::uuid);
CREATE TABLE growth_deal (tenant_id uuid NOT NULL, company_id uuid NOT NULL, id uuid NOT NULL DEFAULT gen_random_uuid(),
  schema_ref text NOT NULL, version int NOT NULL DEFAULT 1, status text NOT NULL, payload jsonb NOT NULL,
  evidence_refs uuid[] NOT NULL DEFAULT '{}', created_by uuid NOT NULL, created_at timestamptz NOT NULL DEFAULT now(), updated_at timestamptz,
  PRIMARY KEY (tenant_id, id), FOREIGN KEY (tenant_id, company_id) REFERENCES company(tenant_id, company_id));  -- SM-SVC-05-WF01, SM-SVC-05-WF02, SM-SVC-05-WF03, SM-SVC-05-WF04, SM-SVC-18-WF01, SM-SVC-18-WF02, SM-SVC-18-WF03, SM-SVC-18-WF04, SM-SVC-20-WF01, SM-SVC-20-WF02, 
ALTER TABLE growth_deal ENABLE ROW LEVEL SECURITY; ALTER TABLE growth_deal FORCE ROW LEVEL SECURITY;
CREATE POLICY growth_deal_tenant ON growth_deal USING (tenant_id = current_setting('app.tenant_id')::uuid) WITH CHECK (tenant_id = current_setting('app.tenant_id')::uuid);
CREATE TABLE growth_stage (tenant_id uuid NOT NULL, company_id uuid NOT NULL, id uuid NOT NULL DEFAULT gen_random_uuid(),
  schema_ref text NOT NULL, version int NOT NULL DEFAULT 1, status text NOT NULL, payload jsonb NOT NULL,
  evidence_refs uuid[] NOT NULL DEFAULT '{}', created_by uuid NOT NULL, created_at timestamptz NOT NULL DEFAULT now(), updated_at timestamptz,
  PRIMARY KEY (tenant_id, id), FOREIGN KEY (tenant_id, company_id) REFERENCES company(tenant_id, company_id));  -- SM-SVC-05-WF01, SM-SVC-05-WF02, SM-SVC-05-WF03, SM-SVC-05-WF04, SM-SVC-29-WF01, SM-SVC-29-WF02, SM-SVC-29-WF03, SM-SVC-29-WF04
ALTER TABLE growth_stage ENABLE ROW LEVEL SECURITY; ALTER TABLE growth_stage FORCE ROW LEVEL SECURITY;
CREATE POLICY growth_stage_tenant ON growth_stage USING (tenant_id = current_setting('app.tenant_id')::uuid) WITH CHECK (tenant_id = current_setting('app.tenant_id')::uuid);
CREATE TABLE growth_task (tenant_id uuid NOT NULL, company_id uuid NOT NULL, id uuid NOT NULL DEFAULT gen_random_uuid(),
  schema_ref text NOT NULL, version int NOT NULL DEFAULT 1, status text NOT NULL, payload jsonb NOT NULL,
  evidence_refs uuid[] NOT NULL DEFAULT '{}', created_by uuid NOT NULL, created_at timestamptz NOT NULL DEFAULT now(), updated_at timestamptz,
  PRIMARY KEY (tenant_id, id), FOREIGN KEY (tenant_id, company_id) REFERENCES company(tenant_id, company_id));  -- SM-SVC-05-WF01, SM-SVC-05-WF02, SM-SVC-05-WF03, SM-SVC-05-WF04, SM-SVC-08-WF01, SM-SVC-08-WF02, SM-SVC-08-WF03, SM-SVC-08-WF04, SM-SVC-19-WF01, SM-SVC-19-WF02, 
ALTER TABLE growth_task ENABLE ROW LEVEL SECURITY; ALTER TABLE growth_task FORCE ROW LEVEL SECURITY;
CREATE POLICY growth_task_tenant ON growth_task USING (tenant_id = current_setting('app.tenant_id')::uuid) WITH CHECK (tenant_id = current_setting('app.tenant_id')::uuid);
CREATE TABLE growth_budget (tenant_id uuid NOT NULL, company_id uuid NOT NULL, id uuid NOT NULL DEFAULT gen_random_uuid(),
  schema_ref text NOT NULL, version int NOT NULL DEFAULT 1, status text NOT NULL, payload jsonb NOT NULL,
  evidence_refs uuid[] NOT NULL DEFAULT '{}', created_by uuid NOT NULL, created_at timestamptz NOT NULL DEFAULT now(), updated_at timestamptz,
  PRIMARY KEY (tenant_id, id), FOREIGN KEY (tenant_id, company_id) REFERENCES company(tenant_id, company_id));  -- SM-SVC-06-WF01, SM-SVC-06-WF02, SM-SVC-06-WF03, SM-SVC-06-WF04, SM-SVC-14-WF01, SM-SVC-14-WF02, SM-SVC-14-WF03, SM-SVC-14-WF04, SM-SVC-30-WF01, SM-SVC-30-WF02, 
ALTER TABLE growth_budget ENABLE ROW LEVEL SECURITY; ALTER TABLE growth_budget FORCE ROW LEVEL SECURITY;
CREATE POLICY growth_budget_tenant ON growth_budget USING (tenant_id = current_setting('app.tenant_id')::uuid) WITH CHECK (tenant_id = current_setting('app.tenant_id')::uuid);
CREATE TABLE growth_message (tenant_id uuid NOT NULL, company_id uuid NOT NULL, id uuid NOT NULL DEFAULT gen_random_uuid(),
  schema_ref text NOT NULL, version int NOT NULL DEFAULT 1, status text NOT NULL, payload jsonb NOT NULL,
  evidence_refs uuid[] NOT NULL DEFAULT '{}', created_by uuid NOT NULL, created_at timestamptz NOT NULL DEFAULT now(), updated_at timestamptz,
  PRIMARY KEY (tenant_id, id), FOREIGN KEY (tenant_id, company_id) REFERENCES company(tenant_id, company_id));  -- SM-SVC-06-WF01, SM-SVC-06-WF02, SM-SVC-06-WF03, SM-SVC-06-WF04, SM-SVC-07-WF01, SM-SVC-07-WF02, SM-SVC-07-WF03, SM-SVC-07-WF04, SM-SVC-09-WF01, SM-SVC-09-WF02, 
ALTER TABLE growth_message ENABLE ROW LEVEL SECURITY; ALTER TABLE growth_message FORCE ROW LEVEL SECURITY;
CREATE POLICY growth_message_tenant ON growth_message USING (tenant_id = current_setting('app.tenant_id')::uuid) WITH CHECK (tenant_id = current_setting('app.tenant_id')::uuid);
CREATE TABLE growth_message_draft (tenant_id uuid NOT NULL, company_id uuid NOT NULL, id uuid NOT NULL DEFAULT gen_random_uuid(),
  schema_ref text NOT NULL, version int NOT NULL DEFAULT 1, status text NOT NULL, payload jsonb NOT NULL,
  evidence_refs uuid[] NOT NULL DEFAULT '{}', created_by uuid NOT NULL, created_at timestamptz NOT NULL DEFAULT now(), updated_at timestamptz,
  PRIMARY KEY (tenant_id, id), FOREIGN KEY (tenant_id, company_id) REFERENCES company(tenant_id, company_id));  -- SM-SVC-06-WF01, SM-SVC-06-WF02, SM-SVC-06-WF03, SM-SVC-06-WF04, SM-SVC-07-WF01, SM-SVC-07-WF02, SM-SVC-07-WF03, SM-SVC-07-WF04, SM-SVC-09-WF01, SM-SVC-09-WF02, 
ALTER TABLE growth_message_draft ENABLE ROW LEVEL SECURITY; ALTER TABLE growth_message_draft FORCE ROW LEVEL SECURITY;
CREATE POLICY growth_message_draft_tenant ON growth_message_draft USING (tenant_id = current_setting('app.tenant_id')::uuid) WITH CHECK (tenant_id = current_setting('app.tenant_id')::uuid);
CREATE TABLE growth_message_template (tenant_id uuid NOT NULL, company_id uuid NOT NULL, id uuid NOT NULL DEFAULT gen_random_uuid(),
  schema_ref text NOT NULL, version int NOT NULL DEFAULT 1, status text NOT NULL, payload jsonb NOT NULL,
  evidence_refs uuid[] NOT NULL DEFAULT '{}', created_by uuid NOT NULL, created_at timestamptz NOT NULL DEFAULT now(), updated_at timestamptz,
  PRIMARY KEY (tenant_id, id), FOREIGN KEY (tenant_id, company_id) REFERENCES company(tenant_id, company_id));  -- SM-SVC-06-WF01, SM-SVC-06-WF02, SM-SVC-06-WF03, SM-SVC-06-WF04, SM-SVC-07-WF01, SM-SVC-07-WF02, SM-SVC-07-WF03, SM-SVC-07-WF04, SM-SVC-09-WF01, SM-SVC-09-WF02, 
ALTER TABLE growth_message_template ENABLE ROW LEVEL SECURITY; ALTER TABLE growth_message_template FORCE ROW LEVEL SECURITY;
CREATE POLICY growth_message_template_tenant ON growth_message_template USING (tenant_id = current_setting('app.tenant_id')::uuid) WITH CHECK (tenant_id = current_setting('app.tenant_id')::uuid);
CREATE TABLE growth_outbox (tenant_id uuid NOT NULL, company_id uuid NOT NULL, id uuid NOT NULL DEFAULT gen_random_uuid(),
  schema_ref text NOT NULL, version int NOT NULL DEFAULT 1, status text NOT NULL, payload jsonb NOT NULL,
  evidence_refs uuid[] NOT NULL DEFAULT '{}', created_by uuid NOT NULL, created_at timestamptz NOT NULL DEFAULT now(), updated_at timestamptz,
  PRIMARY KEY (tenant_id, id), FOREIGN KEY (tenant_id, company_id) REFERENCES company(tenant_id, company_id));  -- SM-SVC-06-WF01, SM-SVC-06-WF02, SM-SVC-06-WF03, SM-SVC-06-WF04
ALTER TABLE growth_outbox ENABLE ROW LEVEL SECURITY; ALTER TABLE growth_outbox FORCE ROW LEVEL SECURITY;
CREATE POLICY growth_outbox_tenant ON growth_outbox USING (tenant_id = current_setting('app.tenant_id')::uuid) WITH CHECK (tenant_id = current_setting('app.tenant_id')::uuid);
CREATE TABLE growth_delivery_event (tenant_id uuid NOT NULL, company_id uuid NOT NULL, id uuid NOT NULL DEFAULT gen_random_uuid(),
  schema_ref text NOT NULL, version int NOT NULL DEFAULT 1, status text NOT NULL, payload jsonb NOT NULL,
  evidence_refs uuid[] NOT NULL DEFAULT '{}', created_by uuid NOT NULL, created_at timestamptz NOT NULL DEFAULT now(), updated_at timestamptz,
  PRIMARY KEY (tenant_id, id), FOREIGN KEY (tenant_id, company_id) REFERENCES company(tenant_id, company_id));  -- SM-SVC-06-WF01, SM-SVC-06-WF02, SM-SVC-06-WF03, SM-SVC-06-WF04, SM-SVC-07-WF01, SM-SVC-07-WF02, SM-SVC-07-WF03, SM-SVC-07-WF04
ALTER TABLE growth_delivery_event ENABLE ROW LEVEL SECURITY; ALTER TABLE growth_delivery_event FORCE ROW LEVEL SECURITY;
CREATE POLICY growth_delivery_event_tenant ON growth_delivery_event USING (tenant_id = current_setting('app.tenant_id')::uuid) WITH CHECK (tenant_id = current_setting('app.tenant_id')::uuid);
CREATE TABLE growth_thread (tenant_id uuid NOT NULL, company_id uuid NOT NULL, id uuid NOT NULL DEFAULT gen_random_uuid(),
  schema_ref text NOT NULL, version int NOT NULL DEFAULT 1, status text NOT NULL, payload jsonb NOT NULL,
  evidence_refs uuid[] NOT NULL DEFAULT '{}', created_by uuid NOT NULL, created_at timestamptz NOT NULL DEFAULT now(), updated_at timestamptz,
  PRIMARY KEY (tenant_id, id), FOREIGN KEY (tenant_id, company_id) REFERENCES company(tenant_id, company_id));  -- SM-SVC-07-WF01, SM-SVC-07-WF02, SM-SVC-07-WF03, SM-SVC-07-WF04, SM-SVC-08-WF01, SM-SVC-08-WF02, SM-SVC-08-WF03, SM-SVC-08-WF04, SM-SVC-09-WF01, SM-SVC-09-WF02, 
ALTER TABLE growth_thread ENABLE ROW LEVEL SECURITY; ALTER TABLE growth_thread FORCE ROW LEVEL SECURITY;
CREATE POLICY growth_thread_tenant ON growth_thread USING (tenant_id = current_setting('app.tenant_id')::uuid) WITH CHECK (tenant_id = current_setting('app.tenant_id')::uuid);
CREATE TABLE growth_channel_account (tenant_id uuid NOT NULL, company_id uuid NOT NULL, id uuid NOT NULL DEFAULT gen_random_uuid(),
  schema_ref text NOT NULL, version int NOT NULL DEFAULT 1, status text NOT NULL, payload jsonb NOT NULL,
  evidence_refs uuid[] NOT NULL DEFAULT '{}', created_by uuid NOT NULL, created_at timestamptz NOT NULL DEFAULT now(), updated_at timestamptz,
  PRIMARY KEY (tenant_id, id), FOREIGN KEY (tenant_id, company_id) REFERENCES company(tenant_id, company_id));  -- SM-SVC-07-WF01, SM-SVC-07-WF02, SM-SVC-07-WF03, SM-SVC-07-WF04, SM-SVC-12-WF01, SM-SVC-12-WF02, SM-SVC-12-WF03, SM-SVC-12-WF04, SM-SVC-27-WF01, SM-SVC-27-WF02, 
ALTER TABLE growth_channel_account ENABLE ROW LEVEL SECURITY; ALTER TABLE growth_channel_account FORCE ROW LEVEL SECURITY;
CREATE POLICY growth_channel_account_tenant ON growth_channel_account USING (tenant_id = current_setting('app.tenant_id')::uuid) WITH CHECK (tenant_id = current_setting('app.tenant_id')::uuid);
CREATE TABLE growth_inbound_event (tenant_id uuid NOT NULL, company_id uuid NOT NULL, id uuid NOT NULL DEFAULT gen_random_uuid(),
  schema_ref text NOT NULL, version int NOT NULL DEFAULT 1, status text NOT NULL, payload jsonb NOT NULL,
  evidence_refs uuid[] NOT NULL DEFAULT '{}', created_by uuid NOT NULL, created_at timestamptz NOT NULL DEFAULT now(), updated_at timestamptz,
  PRIMARY KEY (tenant_id, id), FOREIGN KEY (tenant_id, company_id) REFERENCES company(tenant_id, company_id));  -- SM-SVC-07-WF01, SM-SVC-07-WF02, SM-SVC-07-WF03, SM-SVC-07-WF04, SM-SVC-10-WF01, SM-SVC-10-WF02, SM-SVC-10-WF03, SM-SVC-10-WF04, SM-SVC-16-WF01, SM-SVC-16-WF02, 
ALTER TABLE growth_inbound_event ENABLE ROW LEVEL SECURITY; ALTER TABLE growth_inbound_event FORCE ROW LEVEL SECURITY;
CREATE POLICY growth_inbound_event_tenant ON growth_inbound_event USING (tenant_id = current_setting('app.tenant_id')::uuid) WITH CHECK (tenant_id = current_setting('app.tenant_id')::uuid);
CREATE TABLE growth_enrollment (tenant_id uuid NOT NULL, company_id uuid NOT NULL, id uuid NOT NULL DEFAULT gen_random_uuid(),
  schema_ref text NOT NULL, version int NOT NULL DEFAULT 1, status text NOT NULL, payload jsonb NOT NULL,
  evidence_refs uuid[] NOT NULL DEFAULT '{}', created_by uuid NOT NULL, created_at timestamptz NOT NULL DEFAULT now(), updated_at timestamptz,
  PRIMARY KEY (tenant_id, id), FOREIGN KEY (tenant_id, company_id) REFERENCES company(tenant_id, company_id));  -- SM-SVC-08-WF01, SM-SVC-08-WF02, SM-SVC-08-WF03, SM-SVC-08-WF04, SM-SVC-29-WF01, SM-SVC-29-WF02, SM-SVC-29-WF03, SM-SVC-29-WF04
ALTER TABLE growth_enrollment ENABLE ROW LEVEL SECURITY; ALTER TABLE growth_enrollment FORCE ROW LEVEL SECURITY;
CREATE POLICY growth_enrollment_tenant ON growth_enrollment USING (tenant_id = current_setting('app.tenant_id')::uuid) WITH CHECK (tenant_id = current_setting('app.tenant_id')::uuid);
CREATE TABLE growth_sequence (tenant_id uuid NOT NULL, company_id uuid NOT NULL, id uuid NOT NULL DEFAULT gen_random_uuid(),
  schema_ref text NOT NULL, version int NOT NULL DEFAULT 1, status text NOT NULL, payload jsonb NOT NULL,
  evidence_refs uuid[] NOT NULL DEFAULT '{}', created_by uuid NOT NULL, created_at timestamptz NOT NULL DEFAULT now(), updated_at timestamptz,
  PRIMARY KEY (tenant_id, id), FOREIGN KEY (tenant_id, company_id) REFERENCES company(tenant_id, company_id));  -- SM-SVC-08-WF01, SM-SVC-08-WF02, SM-SVC-08-WF03, SM-SVC-08-WF04, SM-SVC-29-WF01, SM-SVC-29-WF02, SM-SVC-29-WF03, SM-SVC-29-WF04
ALTER TABLE growth_sequence ENABLE ROW LEVEL SECURITY; ALTER TABLE growth_sequence FORCE ROW LEVEL SECURITY;
CREATE POLICY growth_sequence_tenant ON growth_sequence USING (tenant_id = current_setting('app.tenant_id')::uuid) WITH CHECK (tenant_id = current_setting('app.tenant_id')::uuid);
CREATE TABLE growth_sequence_step (tenant_id uuid NOT NULL, company_id uuid NOT NULL, id uuid NOT NULL DEFAULT gen_random_uuid(),
  schema_ref text NOT NULL, version int NOT NULL DEFAULT 1, status text NOT NULL, payload jsonb NOT NULL,
  evidence_refs uuid[] NOT NULL DEFAULT '{}', created_by uuid NOT NULL, created_at timestamptz NOT NULL DEFAULT now(), updated_at timestamptz,
  PRIMARY KEY (tenant_id, id), FOREIGN KEY (tenant_id, company_id) REFERENCES company(tenant_id, company_id));  -- SM-SVC-08-WF01, SM-SVC-08-WF02, SM-SVC-08-WF03, SM-SVC-08-WF04, SM-SVC-29-WF01, SM-SVC-29-WF02, SM-SVC-29-WF03, SM-SVC-29-WF04
ALTER TABLE growth_sequence_step ENABLE ROW LEVEL SECURITY; ALTER TABLE growth_sequence_step FORCE ROW LEVEL SECURITY;
CREATE POLICY growth_sequence_step_tenant ON growth_sequence_step USING (tenant_id = current_setting('app.tenant_id')::uuid) WITH CHECK (tenant_id = current_setting('app.tenant_id')::uuid);
CREATE TABLE growth_routing_rule (tenant_id uuid NOT NULL, company_id uuid NOT NULL, id uuid NOT NULL DEFAULT gen_random_uuid(),
  schema_ref text NOT NULL, version int NOT NULL DEFAULT 1, status text NOT NULL, payload jsonb NOT NULL,
  evidence_refs uuid[] NOT NULL DEFAULT '{}', created_by uuid NOT NULL, created_at timestamptz NOT NULL DEFAULT now(), updated_at timestamptz,
  PRIMARY KEY (tenant_id, id), FOREIGN KEY (tenant_id, company_id) REFERENCES company(tenant_id, company_id));  -- SM-SVC-08-WF01, SM-SVC-08-WF02, SM-SVC-08-WF03, SM-SVC-08-WF04, SM-SVC-09-WF01, SM-SVC-09-WF02, SM-SVC-09-WF03, SM-SVC-09-WF04, SM-SVC-26-WF01, SM-SVC-26-WF02, 
ALTER TABLE growth_routing_rule ENABLE ROW LEVEL SECURITY; ALTER TABLE growth_routing_rule FORCE ROW LEVEL SECURITY;
CREATE POLICY growth_routing_rule_tenant ON growth_routing_rule USING (tenant_id = current_setting('app.tenant_id')::uuid) WITH CHECK (tenant_id = current_setting('app.tenant_id')::uuid);
CREATE TABLE growth_workflow_execution (tenant_id uuid NOT NULL, company_id uuid NOT NULL, id uuid NOT NULL DEFAULT gen_random_uuid(),
  schema_ref text NOT NULL, version int NOT NULL DEFAULT 1, status text NOT NULL, payload jsonb NOT NULL,
  evidence_refs uuid[] NOT NULL DEFAULT '{}', created_by uuid NOT NULL, created_at timestamptz NOT NULL DEFAULT now(), updated_at timestamptz,
  PRIMARY KEY (tenant_id, id), FOREIGN KEY (tenant_id, company_id) REFERENCES company(tenant_id, company_id));  -- SM-SVC-08-WF01, SM-SVC-08-WF02, SM-SVC-08-WF03, SM-SVC-08-WF04
ALTER TABLE growth_workflow_execution ENABLE ROW LEVEL SECURITY; ALTER TABLE growth_workflow_execution FORCE ROW LEVEL SECURITY;
CREATE POLICY growth_workflow_execution_tenant ON growth_workflow_execution USING (tenant_id = current_setting('app.tenant_id')::uuid) WITH CHECK (tenant_id = current_setting('app.tenant_id')::uuid);
CREATE TABLE growth_identity_link (tenant_id uuid NOT NULL, company_id uuid NOT NULL, id uuid NOT NULL DEFAULT gen_random_uuid(),
  schema_ref text NOT NULL, version int NOT NULL DEFAULT 1, status text NOT NULL, payload jsonb NOT NULL,
  evidence_refs uuid[] NOT NULL DEFAULT '{}', created_by uuid NOT NULL, created_at timestamptz NOT NULL DEFAULT now(), updated_at timestamptz,
  PRIMARY KEY (tenant_id, id), FOREIGN KEY (tenant_id, company_id) REFERENCES company(tenant_id, company_id));  -- SM-SVC-09-WF01, SM-SVC-09-WF02, SM-SVC-09-WF03, SM-SVC-09-WF04, SM-SVC-38-WF01, SM-SVC-38-WF02, SM-SVC-38-WF03, SM-SVC-38-WF04
ALTER TABLE growth_identity_link ENABLE ROW LEVEL SECURITY; ALTER TABLE growth_identity_link FORCE ROW LEVEL SECURITY;
CREATE POLICY growth_identity_link_tenant ON growth_identity_link USING (tenant_id = current_setting('app.tenant_id')::uuid) WITH CHECK (tenant_id = current_setting('app.tenant_id')::uuid);
CREATE TABLE growth_objection (tenant_id uuid NOT NULL, company_id uuid NOT NULL, id uuid NOT NULL DEFAULT gen_random_uuid(),
  schema_ref text NOT NULL, version int NOT NULL DEFAULT 1, status text NOT NULL, payload jsonb NOT NULL,
  evidence_refs uuid[] NOT NULL DEFAULT '{}', created_by uuid NOT NULL, created_at timestamptz NOT NULL DEFAULT now(), updated_at timestamptz,
  PRIMARY KEY (tenant_id, id), FOREIGN KEY (tenant_id, company_id) REFERENCES company(tenant_id, company_id));  -- SM-SVC-09-WF01, SM-SVC-09-WF02, SM-SVC-09-WF03, SM-SVC-09-WF04, SM-SVC-18-WF01, SM-SVC-18-WF02, SM-SVC-18-WF03, SM-SVC-18-WF04, SM-SVC-36-WF01, SM-SVC-36-WF02, 
ALTER TABLE growth_objection ENABLE ROW LEVEL SECURITY; ALTER TABLE growth_objection FORCE ROW LEVEL SECURITY;
CREATE POLICY growth_objection_tenant ON growth_objection USING (tenant_id = current_setting('app.tenant_id')::uuid) WITH CHECK (tenant_id = current_setting('app.tenant_id')::uuid);
CREATE TABLE growth_calendar_link (tenant_id uuid NOT NULL, company_id uuid NOT NULL, id uuid NOT NULL DEFAULT gen_random_uuid(),
  schema_ref text NOT NULL, version int NOT NULL DEFAULT 1, status text NOT NULL, payload jsonb NOT NULL,
  evidence_refs uuid[] NOT NULL DEFAULT '{}', created_by uuid NOT NULL, created_at timestamptz NOT NULL DEFAULT now(), updated_at timestamptz,
  PRIMARY KEY (tenant_id, id), FOREIGN KEY (tenant_id, company_id) REFERENCES company(tenant_id, company_id));  -- SM-SVC-10-WF01, SM-SVC-10-WF02, SM-SVC-10-WF03, SM-SVC-10-WF04, SM-SVC-26-WF01, SM-SVC-26-WF02, SM-SVC-26-WF03, SM-SVC-26-WF04, SM-SVC-36-WF01, SM-SVC-36-WF02, 
ALTER TABLE growth_calendar_link ENABLE ROW LEVEL SECURITY; ALTER TABLE growth_calendar_link FORCE ROW LEVEL SECURITY;
CREATE POLICY growth_calendar_link_tenant ON growth_calendar_link USING (tenant_id = current_setting('app.tenant_id')::uuid) WITH CHECK (tenant_id = current_setting('app.tenant_id')::uuid);
CREATE TABLE growth_meeting (tenant_id uuid NOT NULL, company_id uuid NOT NULL, id uuid NOT NULL DEFAULT gen_random_uuid(),
  schema_ref text NOT NULL, version int NOT NULL DEFAULT 1, status text NOT NULL, payload jsonb NOT NULL,
  evidence_refs uuid[] NOT NULL DEFAULT '{}', created_by uuid NOT NULL, created_at timestamptz NOT NULL DEFAULT now(), updated_at timestamptz,
  PRIMARY KEY (tenant_id, id), FOREIGN KEY (tenant_id, company_id) REFERENCES company(tenant_id, company_id));  -- SM-SVC-10-WF01, SM-SVC-10-WF02, SM-SVC-10-WF03, SM-SVC-10-WF04, SM-SVC-26-WF01, SM-SVC-26-WF02, SM-SVC-26-WF03, SM-SVC-26-WF04, SM-SVC-36-WF01, SM-SVC-36-WF02, 
ALTER TABLE growth_meeting ENABLE ROW LEVEL SECURITY; ALTER TABLE growth_meeting FORCE ROW LEVEL SECURITY;
CREATE POLICY growth_meeting_tenant ON growth_meeting USING (tenant_id = current_setting('app.tenant_id')::uuid) WITH CHECK (tenant_id = current_setting('app.tenant_id')::uuid);
CREATE TABLE growth_business_event (tenant_id uuid NOT NULL, company_id uuid NOT NULL, id uuid NOT NULL DEFAULT gen_random_uuid(),
  schema_ref text NOT NULL, version int NOT NULL DEFAULT 1, status text NOT NULL, payload jsonb NOT NULL,
  evidence_refs uuid[] NOT NULL DEFAULT '{}', created_by uuid NOT NULL, created_at timestamptz NOT NULL DEFAULT now(), updated_at timestamptz,
  PRIMARY KEY (tenant_id, id), FOREIGN KEY (tenant_id, company_id) REFERENCES company(tenant_id, company_id));  -- SM-SVC-10-WF01, SM-SVC-10-WF02, SM-SVC-10-WF03, SM-SVC-10-WF04, SM-SVC-16-WF01, SM-SVC-16-WF02, SM-SVC-16-WF03, SM-SVC-16-WF04
ALTER TABLE growth_business_event ENABLE ROW LEVEL SECURITY; ALTER TABLE growth_business_event FORCE ROW LEVEL SECURITY;
CREATE POLICY growth_business_event_tenant ON growth_business_event USING (tenant_id = current_setting('app.tenant_id')::uuid) WITH CHECK (tenant_id = current_setting('app.tenant_id')::uuid);
CREATE TABLE growth_event_attendance (tenant_id uuid NOT NULL, company_id uuid NOT NULL, id uuid NOT NULL DEFAULT gen_random_uuid(),
  schema_ref text NOT NULL, version int NOT NULL DEFAULT 1, status text NOT NULL, payload jsonb NOT NULL,
  evidence_refs uuid[] NOT NULL DEFAULT '{}', created_by uuid NOT NULL, created_at timestamptz NOT NULL DEFAULT now(), updated_at timestamptz,
  PRIMARY KEY (tenant_id, id), FOREIGN KEY (tenant_id, company_id) REFERENCES company(tenant_id, company_id));  -- SM-SVC-10-WF01, SM-SVC-10-WF02, SM-SVC-10-WF03, SM-SVC-10-WF04, SM-SVC-16-WF01, SM-SVC-16-WF02, SM-SVC-16-WF03, SM-SVC-16-WF04
ALTER TABLE growth_event_attendance ENABLE ROW LEVEL SECURITY; ALTER TABLE growth_event_attendance FORCE ROW LEVEL SECURITY;
CREATE POLICY growth_event_attendance_tenant ON growth_event_attendance USING (tenant_id = current_setting('app.tenant_id')::uuid) WITH CHECK (tenant_id = current_setting('app.tenant_id')::uuid);
CREATE TABLE growth_event_registration (tenant_id uuid NOT NULL, company_id uuid NOT NULL, id uuid NOT NULL DEFAULT gen_random_uuid(),
  schema_ref text NOT NULL, version int NOT NULL DEFAULT 1, status text NOT NULL, payload jsonb NOT NULL,
  evidence_refs uuid[] NOT NULL DEFAULT '{}', created_by uuid NOT NULL, created_at timestamptz NOT NULL DEFAULT now(), updated_at timestamptz,
  PRIMARY KEY (tenant_id, id), FOREIGN KEY (tenant_id, company_id) REFERENCES company(tenant_id, company_id));  -- SM-SVC-10-WF01, SM-SVC-10-WF02, SM-SVC-10-WF03, SM-SVC-10-WF04, SM-SVC-16-WF01, SM-SVC-16-WF02, SM-SVC-16-WF03, SM-SVC-16-WF04
ALTER TABLE growth_event_registration ENABLE ROW LEVEL SECURITY; ALTER TABLE growth_event_registration FORCE ROW LEVEL SECURITY;
CREATE POLICY growth_event_registration_tenant ON growth_event_registration USING (tenant_id = current_setting('app.tenant_id')::uuid) WITH CHECK (tenant_id = current_setting('app.tenant_id')::uuid);
CREATE TABLE growth_claim (tenant_id uuid NOT NULL, company_id uuid NOT NULL, id uuid NOT NULL DEFAULT gen_random_uuid(),
  schema_ref text NOT NULL, version int NOT NULL DEFAULT 1, status text NOT NULL, payload jsonb NOT NULL,
  evidence_refs uuid[] NOT NULL DEFAULT '{}', created_by uuid NOT NULL, created_at timestamptz NOT NULL DEFAULT now(), updated_at timestamptz,
  PRIMARY KEY (tenant_id, id), FOREIGN KEY (tenant_id, company_id) REFERENCES company(tenant_id, company_id));  -- SM-SVC-11-WF01, SM-SVC-11-WF02, SM-SVC-11-WF03, SM-SVC-11-WF04, SM-SVC-25-WF01, SM-SVC-25-WF02, SM-SVC-25-WF03, SM-SVC-25-WF04, SM-SVC-28-WF01, SM-SVC-28-WF02, 
ALTER TABLE growth_claim ENABLE ROW LEVEL SECURITY; ALTER TABLE growth_claim FORCE ROW LEVEL SECURITY;
CREATE POLICY growth_claim_tenant ON growth_claim USING (tenant_id = current_setting('app.tenant_id')::uuid) WITH CHECK (tenant_id = current_setting('app.tenant_id')::uuid);
CREATE TABLE growth_content_asset (tenant_id uuid NOT NULL, company_id uuid NOT NULL, id uuid NOT NULL DEFAULT gen_random_uuid(),
  schema_ref text NOT NULL, version int NOT NULL DEFAULT 1, status text NOT NULL, payload jsonb NOT NULL,
  evidence_refs uuid[] NOT NULL DEFAULT '{}', created_by uuid NOT NULL, created_at timestamptz NOT NULL DEFAULT now(), updated_at timestamptz,
  PRIMARY KEY (tenant_id, id), FOREIGN KEY (tenant_id, company_id) REFERENCES company(tenant_id, company_id));  -- SM-SVC-11-WF01, SM-SVC-11-WF02, SM-SVC-11-WF03, SM-SVC-11-WF04, SM-SVC-12-WF01, SM-SVC-12-WF02, SM-SVC-12-WF03, SM-SVC-12-WF04, SM-SVC-27-WF01, SM-SVC-27-WF02, 
ALTER TABLE growth_content_asset ENABLE ROW LEVEL SECURITY; ALTER TABLE growth_content_asset FORCE ROW LEVEL SECURITY;
CREATE POLICY growth_content_asset_tenant ON growth_content_asset USING (tenant_id = current_setting('app.tenant_id')::uuid) WITH CHECK (tenant_id = current_setting('app.tenant_id')::uuid);
CREATE TABLE growth_content_version (tenant_id uuid NOT NULL, company_id uuid NOT NULL, id uuid NOT NULL DEFAULT gen_random_uuid(),
  schema_ref text NOT NULL, version int NOT NULL DEFAULT 1, status text NOT NULL, payload jsonb NOT NULL,
  evidence_refs uuid[] NOT NULL DEFAULT '{}', created_by uuid NOT NULL, created_at timestamptz NOT NULL DEFAULT now(), updated_at timestamptz,
  PRIMARY KEY (tenant_id, id), FOREIGN KEY (tenant_id, company_id) REFERENCES company(tenant_id, company_id));  -- SM-SVC-11-WF01, SM-SVC-11-WF02, SM-SVC-11-WF03, SM-SVC-11-WF04, SM-SVC-12-WF01, SM-SVC-12-WF02, SM-SVC-12-WF03, SM-SVC-12-WF04, SM-SVC-13-WF01, SM-SVC-13-WF02, 
ALTER TABLE growth_content_version ENABLE ROW LEVEL SECURITY; ALTER TABLE growth_content_version FORCE ROW LEVEL SECURITY;
CREATE POLICY growth_content_version_tenant ON growth_content_version USING (tenant_id = current_setting('app.tenant_id')::uuid) WITH CHECK (tenant_id = current_setting('app.tenant_id')::uuid);
CREATE TABLE growth_approval (tenant_id uuid NOT NULL, company_id uuid NOT NULL, id uuid NOT NULL DEFAULT gen_random_uuid(),
  schema_ref text NOT NULL, version int NOT NULL DEFAULT 1, status text NOT NULL, payload jsonb NOT NULL,
  evidence_refs uuid[] NOT NULL DEFAULT '{}', created_by uuid NOT NULL, created_at timestamptz NOT NULL DEFAULT now(), updated_at timestamptz,
  PRIMARY KEY (tenant_id, id), FOREIGN KEY (tenant_id, company_id) REFERENCES company(tenant_id, company_id));  -- SM-SVC-11-WF01, SM-SVC-11-WF02, SM-SVC-11-WF03, SM-SVC-11-WF04, SM-SVC-13-WF01, SM-SVC-13-WF02, SM-SVC-13-WF03, SM-SVC-13-WF04, SM-SVC-14-WF01, SM-SVC-14-WF02, 
ALTER TABLE growth_approval ENABLE ROW LEVEL SECURITY; ALTER TABLE growth_approval FORCE ROW LEVEL SECURITY;
CREATE POLICY growth_approval_tenant ON growth_approval USING (tenant_id = current_setting('app.tenant_id')::uuid) WITH CHECK (tenant_id = current_setting('app.tenant_id')::uuid);
CREATE TABLE growth_social_post (tenant_id uuid NOT NULL, company_id uuid NOT NULL, id uuid NOT NULL DEFAULT gen_random_uuid(),
  schema_ref text NOT NULL, version int NOT NULL DEFAULT 1, status text NOT NULL, payload jsonb NOT NULL,
  evidence_refs uuid[] NOT NULL DEFAULT '{}', created_by uuid NOT NULL, created_at timestamptz NOT NULL DEFAULT now(), updated_at timestamptz,
  PRIMARY KEY (tenant_id, id), FOREIGN KEY (tenant_id, company_id) REFERENCES company(tenant_id, company_id));  -- SM-SVC-12-WF01, SM-SVC-12-WF02, SM-SVC-12-WF03, SM-SVC-12-WF04, SM-SVC-35-WF01, SM-SVC-35-WF02, SM-SVC-35-WF03, SM-SVC-35-WF04
ALTER TABLE growth_social_post ENABLE ROW LEVEL SECURITY; ALTER TABLE growth_social_post FORCE ROW LEVEL SECURITY;
CREATE POLICY growth_social_post_tenant ON growth_social_post USING (tenant_id = current_setting('app.tenant_id')::uuid) WITH CHECK (tenant_id = current_setting('app.tenant_id')::uuid);
CREATE TABLE growth_social_publication (tenant_id uuid NOT NULL, company_id uuid NOT NULL, id uuid NOT NULL DEFAULT gen_random_uuid(),
  schema_ref text NOT NULL, version int NOT NULL DEFAULT 1, status text NOT NULL, payload jsonb NOT NULL,
  evidence_refs uuid[] NOT NULL DEFAULT '{}', created_by uuid NOT NULL, created_at timestamptz NOT NULL DEFAULT now(), updated_at timestamptz,
  PRIMARY KEY (tenant_id, id), FOREIGN KEY (tenant_id, company_id) REFERENCES company(tenant_id, company_id));  -- SM-SVC-12-WF01, SM-SVC-12-WF02, SM-SVC-12-WF03, SM-SVC-12-WF04, SM-SVC-27-WF01, SM-SVC-27-WF02, SM-SVC-27-WF03, SM-SVC-27-WF04
ALTER TABLE growth_social_publication ENABLE ROW LEVEL SECURITY; ALTER TABLE growth_social_publication FORCE ROW LEVEL SECURITY;
CREATE POLICY growth_social_publication_tenant ON growth_social_publication USING (tenant_id = current_setting('app.tenant_id')::uuid) WITH CHECK (tenant_id = current_setting('app.tenant_id')::uuid);
CREATE TABLE growth_keyword (tenant_id uuid NOT NULL, company_id uuid NOT NULL, id uuid NOT NULL DEFAULT gen_random_uuid(),
  schema_ref text NOT NULL, version int NOT NULL DEFAULT 1, status text NOT NULL, payload jsonb NOT NULL,
  evidence_refs uuid[] NOT NULL DEFAULT '{}', created_by uuid NOT NULL, created_at timestamptz NOT NULL DEFAULT now(), updated_at timestamptz,
  PRIMARY KEY (tenant_id, id), FOREIGN KEY (tenant_id, company_id) REFERENCES company(tenant_id, company_id));  -- SM-SVC-13-WF01, SM-SVC-13-WF02, SM-SVC-13-WF03, SM-SVC-13-WF04
ALTER TABLE growth_keyword ENABLE ROW LEVEL SECURITY; ALTER TABLE growth_keyword FORCE ROW LEVEL SECURITY;
CREATE POLICY growth_keyword_tenant ON growth_keyword USING (tenant_id = current_setting('app.tenant_id')::uuid) WITH CHECK (tenant_id = current_setting('app.tenant_id')::uuid);
CREATE TABLE growth_page_metric (tenant_id uuid NOT NULL, company_id uuid NOT NULL, id uuid NOT NULL DEFAULT gen_random_uuid(),
  schema_ref text NOT NULL, version int NOT NULL DEFAULT 1, status text NOT NULL, payload jsonb NOT NULL,
  evidence_refs uuid[] NOT NULL DEFAULT '{}', created_by uuid NOT NULL, created_at timestamptz NOT NULL DEFAULT now(), updated_at timestamptz,
  PRIMARY KEY (tenant_id, id), FOREIGN KEY (tenant_id, company_id) REFERENCES company(tenant_id, company_id));  -- SM-SVC-13-WF01, SM-SVC-13-WF02, SM-SVC-13-WF03, SM-SVC-13-WF04
ALTER TABLE growth_page_metric ENABLE ROW LEVEL SECURITY; ALTER TABLE growth_page_metric FORCE ROW LEVEL SECURITY;
CREATE POLICY growth_page_metric_tenant ON growth_page_metric USING (tenant_id = current_setting('app.tenant_id')::uuid) WITH CHECK (tenant_id = current_setting('app.tenant_id')::uuid);
CREATE TABLE growth_seo_issue (tenant_id uuid NOT NULL, company_id uuid NOT NULL, id uuid NOT NULL DEFAULT gen_random_uuid(),
  schema_ref text NOT NULL, version int NOT NULL DEFAULT 1, status text NOT NULL, payload jsonb NOT NULL,
  evidence_refs uuid[] NOT NULL DEFAULT '{}', created_by uuid NOT NULL, created_at timestamptz NOT NULL DEFAULT now(), updated_at timestamptz,
  PRIMARY KEY (tenant_id, id), FOREIGN KEY (tenant_id, company_id) REFERENCES company(tenant_id, company_id));  -- SM-SVC-13-WF01, SM-SVC-13-WF02, SM-SVC-13-WF03, SM-SVC-13-WF04
ALTER TABLE growth_seo_issue ENABLE ROW LEVEL SECURITY; ALTER TABLE growth_seo_issue FORCE ROW LEVEL SECURITY;
CREATE POLICY growth_seo_issue_tenant ON growth_seo_issue USING (tenant_id = current_setting('app.tenant_id')::uuid) WITH CHECK (tenant_id = current_setting('app.tenant_id')::uuid);
CREATE TABLE growth_landing_page (tenant_id uuid NOT NULL, company_id uuid NOT NULL, id uuid NOT NULL DEFAULT gen_random_uuid(),
  schema_ref text NOT NULL, version int NOT NULL DEFAULT 1, status text NOT NULL, payload jsonb NOT NULL,
  evidence_refs uuid[] NOT NULL DEFAULT '{}', created_by uuid NOT NULL, created_at timestamptz NOT NULL DEFAULT now(), updated_at timestamptz,
  PRIMARY KEY (tenant_id, id), FOREIGN KEY (tenant_id, company_id) REFERENCES company(tenant_id, company_id));  -- SM-SVC-13-WF01, SM-SVC-13-WF02, SM-SVC-13-WF03, SM-SVC-13-WF04
ALTER TABLE growth_landing_page ENABLE ROW LEVEL SECURITY; ALTER TABLE growth_landing_page FORCE ROW LEVEL SECURITY;
CREATE POLICY growth_landing_page_tenant ON growth_landing_page USING (tenant_id = current_setting('app.tenant_id')::uuid) WITH CHECK (tenant_id = current_setting('app.tenant_id')::uuid);
CREATE TABLE growth_audience (tenant_id uuid NOT NULL, company_id uuid NOT NULL, id uuid NOT NULL DEFAULT gen_random_uuid(),
  schema_ref text NOT NULL, version int NOT NULL DEFAULT 1, status text NOT NULL, payload jsonb NOT NULL,
  evidence_refs uuid[] NOT NULL DEFAULT '{}', created_by uuid NOT NULL, created_at timestamptz NOT NULL DEFAULT now(), updated_at timestamptz,
  PRIMARY KEY (tenant_id, id), FOREIGN KEY (tenant_id, company_id) REFERENCES company(tenant_id, company_id));  -- SM-SVC-14-WF01, SM-SVC-14-WF02, SM-SVC-14-WF03, SM-SVC-14-WF04, SM-SVC-30-WF01, SM-SVC-30-WF02, SM-SVC-30-WF03, SM-SVC-30-WF04
ALTER TABLE growth_audience ENABLE ROW LEVEL SECURITY; ALTER TABLE growth_audience FORCE ROW LEVEL SECURITY;
CREATE POLICY growth_audience_tenant ON growth_audience USING (tenant_id = current_setting('app.tenant_id')::uuid) WITH CHECK (tenant_id = current_setting('app.tenant_id')::uuid);
CREATE TABLE growth_campaign (tenant_id uuid NOT NULL, company_id uuid NOT NULL, id uuid NOT NULL DEFAULT gen_random_uuid(),
  schema_ref text NOT NULL, version int NOT NULL DEFAULT 1, status text NOT NULL, payload jsonb NOT NULL,
  evidence_refs uuid[] NOT NULL DEFAULT '{}', created_by uuid NOT NULL, created_at timestamptz NOT NULL DEFAULT now(), updated_at timestamptz,
  PRIMARY KEY (tenant_id, id), FOREIGN KEY (tenant_id, company_id) REFERENCES company(tenant_id, company_id));  -- SM-SVC-14-WF01, SM-SVC-14-WF02, SM-SVC-14-WF03, SM-SVC-14-WF04, SM-SVC-30-WF01, SM-SVC-30-WF02, SM-SVC-30-WF03, SM-SVC-30-WF04
ALTER TABLE growth_campaign ENABLE ROW LEVEL SECURITY; ALTER TABLE growth_campaign FORCE ROW LEVEL SECURITY;
CREATE POLICY growth_campaign_tenant ON growth_campaign USING (tenant_id = current_setting('app.tenant_id')::uuid) WITH CHECK (tenant_id = current_setting('app.tenant_id')::uuid);
CREATE TABLE growth_campaign_version (tenant_id uuid NOT NULL, company_id uuid NOT NULL, id uuid NOT NULL DEFAULT gen_random_uuid(),
  schema_ref text NOT NULL, version int NOT NULL DEFAULT 1, status text NOT NULL, payload jsonb NOT NULL,
  evidence_refs uuid[] NOT NULL DEFAULT '{}', created_by uuid NOT NULL, created_at timestamptz NOT NULL DEFAULT now(), updated_at timestamptz,
  PRIMARY KEY (tenant_id, id), FOREIGN KEY (tenant_id, company_id) REFERENCES company(tenant_id, company_id));  -- SM-SVC-14-WF01, SM-SVC-14-WF02, SM-SVC-14-WF03, SM-SVC-14-WF04, SM-SVC-30-WF01, SM-SVC-30-WF02, SM-SVC-30-WF03, SM-SVC-30-WF04
ALTER TABLE growth_campaign_version ENABLE ROW LEVEL SECURITY; ALTER TABLE growth_campaign_version FORCE ROW LEVEL SECURITY;
CREATE POLICY growth_campaign_version_tenant ON growth_campaign_version USING (tenant_id = current_setting('app.tenant_id')::uuid) WITH CHECK (tenant_id = current_setting('app.tenant_id')::uuid);
CREATE TABLE growth_ad_campaign (tenant_id uuid NOT NULL, company_id uuid NOT NULL, id uuid NOT NULL DEFAULT gen_random_uuid(),
  schema_ref text NOT NULL, version int NOT NULL DEFAULT 1, status text NOT NULL, payload jsonb NOT NULL,
  evidence_refs uuid[] NOT NULL DEFAULT '{}', created_by uuid NOT NULL, created_at timestamptz NOT NULL DEFAULT now(), updated_at timestamptz,
  PRIMARY KEY (tenant_id, id), FOREIGN KEY (tenant_id, company_id) REFERENCES company(tenant_id, company_id));  -- SM-SVC-14-WF01, SM-SVC-14-WF02, SM-SVC-14-WF03, SM-SVC-14-WF04
ALTER TABLE growth_ad_campaign ENABLE ROW LEVEL SECURITY; ALTER TABLE growth_ad_campaign FORCE ROW LEVEL SECURITY;
CREATE POLICY growth_ad_campaign_tenant ON growth_ad_campaign USING (tenant_id = current_setting('app.tenant_id')::uuid) WITH CHECK (tenant_id = current_setting('app.tenant_id')::uuid);
CREATE TABLE growth_ad_spend_event (tenant_id uuid NOT NULL, company_id uuid NOT NULL, id uuid NOT NULL DEFAULT gen_random_uuid(),
  schema_ref text NOT NULL, version int NOT NULL DEFAULT 1, status text NOT NULL, payload jsonb NOT NULL,
  evidence_refs uuid[] NOT NULL DEFAULT '{}', created_by uuid NOT NULL, created_at timestamptz NOT NULL DEFAULT now(), updated_at timestamptz,
  PRIMARY KEY (tenant_id, id), FOREIGN KEY (tenant_id, company_id) REFERENCES company(tenant_id, company_id));  -- SM-SVC-14-WF01, SM-SVC-14-WF02, SM-SVC-14-WF03, SM-SVC-14-WF04
ALTER TABLE growth_ad_spend_event ENABLE ROW LEVEL SECURITY; ALTER TABLE growth_ad_spend_event FORCE ROW LEVEL SECURITY;
CREATE POLICY growth_ad_spend_event_tenant ON growth_ad_spend_event USING (tenant_id = current_setting('app.tenant_id')::uuid) WITH CHECK (tenant_id = current_setting('app.tenant_id')::uuid);
CREATE TABLE growth_attribution_event (tenant_id uuid NOT NULL, company_id uuid NOT NULL, id uuid NOT NULL DEFAULT gen_random_uuid(),
  schema_ref text NOT NULL, version int NOT NULL DEFAULT 1, status text NOT NULL, payload jsonb NOT NULL,
  evidence_refs uuid[] NOT NULL DEFAULT '{}', created_by uuid NOT NULL, created_at timestamptz NOT NULL DEFAULT now(), updated_at timestamptz,
  PRIMARY KEY (tenant_id, id), FOREIGN KEY (tenant_id, company_id) REFERENCES company(tenant_id, company_id));  -- SM-SVC-14-WF01, SM-SVC-14-WF02, SM-SVC-14-WF03, SM-SVC-14-WF04, SM-SVC-24-WF01, SM-SVC-24-WF02, SM-SVC-24-WF03, SM-SVC-24-WF04, SM-SVC-30-WF01, SM-SVC-30-WF02, 
ALTER TABLE growth_attribution_event ENABLE ROW LEVEL SECURITY; ALTER TABLE growth_attribution_event FORCE ROW LEVEL SECURITY;
CREATE POLICY growth_attribution_event_tenant ON growth_attribution_event USING (tenant_id = current_setting('app.tenant_id')::uuid) WITH CHECK (tenant_id = current_setting('app.tenant_id')::uuid);
CREATE TABLE growth_form (tenant_id uuid NOT NULL, company_id uuid NOT NULL, id uuid NOT NULL DEFAULT gen_random_uuid(),
  schema_ref text NOT NULL, version int NOT NULL DEFAULT 1, status text NOT NULL, payload jsonb NOT NULL,
  evidence_refs uuid[] NOT NULL DEFAULT '{}', created_by uuid NOT NULL, created_at timestamptz NOT NULL DEFAULT now(), updated_at timestamptz,
  PRIMARY KEY (tenant_id, id), FOREIGN KEY (tenant_id, company_id) REFERENCES company(tenant_id, company_id));  -- SM-SVC-15-WF01, SM-SVC-15-WF02, SM-SVC-15-WF03, SM-SVC-15-WF04
ALTER TABLE growth_form ENABLE ROW LEVEL SECURITY; ALTER TABLE growth_form FORCE ROW LEVEL SECURITY;
CREATE POLICY growth_form_tenant ON growth_form USING (tenant_id = current_setting('app.tenant_id')::uuid) WITH CHECK (tenant_id = current_setting('app.tenant_id')::uuid);
CREATE TABLE growth_lead (tenant_id uuid NOT NULL, company_id uuid NOT NULL, id uuid NOT NULL DEFAULT gen_random_uuid(),
  schema_ref text NOT NULL, version int NOT NULL DEFAULT 1, status text NOT NULL, payload jsonb NOT NULL,
  evidence_refs uuid[] NOT NULL DEFAULT '{}', created_by uuid NOT NULL, created_at timestamptz NOT NULL DEFAULT now(), updated_at timestamptz,
  PRIMARY KEY (tenant_id, id), FOREIGN KEY (tenant_id, company_id) REFERENCES company(tenant_id, company_id));  -- SM-SVC-16-WF01, SM-SVC-16-WF02, SM-SVC-16-WF03, SM-SVC-16-WF04
ALTER TABLE growth_lead ENABLE ROW LEVEL SECURITY; ALTER TABLE growth_lead FORCE ROW LEVEL SECURITY;
CREATE POLICY growth_lead_tenant ON growth_lead USING (tenant_id = current_setting('app.tenant_id')::uuid) WITH CHECK (tenant_id = current_setting('app.tenant_id')::uuid);
CREATE TABLE growth_proposal (tenant_id uuid NOT NULL, company_id uuid NOT NULL, id uuid NOT NULL DEFAULT gen_random_uuid(),
  schema_ref text NOT NULL, version int NOT NULL DEFAULT 1, status text NOT NULL, payload jsonb NOT NULL,
  evidence_refs uuid[] NOT NULL DEFAULT '{}', created_by uuid NOT NULL, created_at timestamptz NOT NULL DEFAULT now(), updated_at timestamptz,
  PRIMARY KEY (tenant_id, id), FOREIGN KEY (tenant_id, company_id) REFERENCES company(tenant_id, company_id));  -- SM-SVC-17-WF01, SM-SVC-17-WF02, SM-SVC-17-WF03, SM-SVC-17-WF04, SM-SVC-19-WF01, SM-SVC-19-WF02, SM-SVC-19-WF03, SM-SVC-19-WF04
ALTER TABLE growth_proposal ENABLE ROW LEVEL SECURITY; ALTER TABLE growth_proposal FORCE ROW LEVEL SECURITY;
CREATE POLICY growth_proposal_tenant ON growth_proposal USING (tenant_id = current_setting('app.tenant_id')::uuid) WITH CHECK (tenant_id = current_setting('app.tenant_id')::uuid);
CREATE TABLE growth_proposal_version (tenant_id uuid NOT NULL, company_id uuid NOT NULL, id uuid NOT NULL DEFAULT gen_random_uuid(),
  schema_ref text NOT NULL, version int NOT NULL DEFAULT 1, status text NOT NULL, payload jsonb NOT NULL,
  evidence_refs uuid[] NOT NULL DEFAULT '{}', created_by uuid NOT NULL, created_at timestamptz NOT NULL DEFAULT now(), updated_at timestamptz,
  PRIMARY KEY (tenant_id, id), FOREIGN KEY (tenant_id, company_id) REFERENCES company(tenant_id, company_id));  -- SM-SVC-17-WF01, SM-SVC-17-WF02, SM-SVC-17-WF03, SM-SVC-17-WF04, SM-SVC-19-WF01, SM-SVC-19-WF02, SM-SVC-19-WF03, SM-SVC-19-WF04
ALTER TABLE growth_proposal_version ENABLE ROW LEVEL SECURITY; ALTER TABLE growth_proposal_version FORCE ROW LEVEL SECURITY;
CREATE POLICY growth_proposal_version_tenant ON growth_proposal_version USING (tenant_id = current_setting('app.tenant_id')::uuid) WITH CHECK (tenant_id = current_setting('app.tenant_id')::uuid);
CREATE TABLE growth_quote (tenant_id uuid NOT NULL, company_id uuid NOT NULL, id uuid NOT NULL DEFAULT gen_random_uuid(),
  schema_ref text NOT NULL, version int NOT NULL DEFAULT 1, status text NOT NULL, payload jsonb NOT NULL,
  evidence_refs uuid[] NOT NULL DEFAULT '{}', created_by uuid NOT NULL, created_at timestamptz NOT NULL DEFAULT now(), updated_at timestamptz,
  PRIMARY KEY (tenant_id, id), FOREIGN KEY (tenant_id, company_id) REFERENCES company(tenant_id, company_id));  -- SM-SVC-17-WF01, SM-SVC-17-WF02, SM-SVC-17-WF03, SM-SVC-17-WF04, SM-SVC-20-WF01, SM-SVC-20-WF02, SM-SVC-20-WF03, SM-SVC-20-WF04, SM-SVC-28-WF01, SM-SVC-28-WF02, 
ALTER TABLE growth_quote ENABLE ROW LEVEL SECURITY; ALTER TABLE growth_quote FORCE ROW LEVEL SECURITY;
CREATE POLICY growth_quote_tenant ON growth_quote USING (tenant_id = current_setting('app.tenant_id')::uuid) WITH CHECK (tenant_id = current_setting('app.tenant_id')::uuid);
CREATE TABLE growth_quote_line (tenant_id uuid NOT NULL, company_id uuid NOT NULL, id uuid NOT NULL DEFAULT gen_random_uuid(),
  schema_ref text NOT NULL, version int NOT NULL DEFAULT 1, status text NOT NULL, payload jsonb NOT NULL,
  evidence_refs uuid[] NOT NULL DEFAULT '{}', created_by uuid NOT NULL, created_at timestamptz NOT NULL DEFAULT now(), updated_at timestamptz,
  PRIMARY KEY (tenant_id, id), FOREIGN KEY (tenant_id, company_id) REFERENCES company(tenant_id, company_id));  -- SM-SVC-17-WF01, SM-SVC-17-WF02, SM-SVC-17-WF03, SM-SVC-17-WF04, SM-SVC-20-WF01, SM-SVC-20-WF02, SM-SVC-20-WF03, SM-SVC-20-WF04, SM-SVC-28-WF01, SM-SVC-28-WF02, 
ALTER TABLE growth_quote_line ENABLE ROW LEVEL SECURITY; ALTER TABLE growth_quote_line FORCE ROW LEVEL SECURITY;
CREATE POLICY growth_quote_line_tenant ON growth_quote_line USING (tenant_id = current_setting('app.tenant_id')::uuid) WITH CHECK (tenant_id = current_setting('app.tenant_id')::uuid);
CREATE TABLE growth_negotiation (tenant_id uuid NOT NULL, company_id uuid NOT NULL, id uuid NOT NULL DEFAULT gen_random_uuid(),
  schema_ref text NOT NULL, version int NOT NULL DEFAULT 1, status text NOT NULL, payload jsonb NOT NULL,
  evidence_refs uuid[] NOT NULL DEFAULT '{}', created_by uuid NOT NULL, created_at timestamptz NOT NULL DEFAULT now(), updated_at timestamptz,
  PRIMARY KEY (tenant_id, id), FOREIGN KEY (tenant_id, company_id) REFERENCES company(tenant_id, company_id));  -- SM-SVC-18-WF01, SM-SVC-18-WF02, SM-SVC-18-WF03, SM-SVC-18-WF04, SM-SVC-36-WF01, SM-SVC-36-WF02, SM-SVC-36-WF03, SM-SVC-36-WF04
ALTER TABLE growth_negotiation ENABLE ROW LEVEL SECURITY; ALTER TABLE growth_negotiation FORCE ROW LEVEL SECURITY;
CREATE POLICY growth_negotiation_tenant ON growth_negotiation USING (tenant_id = current_setting('app.tenant_id')::uuid) WITH CHECK (tenant_id = current_setting('app.tenant_id')::uuid);
CREATE TABLE growth_contract (tenant_id uuid NOT NULL, company_id uuid NOT NULL, id uuid NOT NULL DEFAULT gen_random_uuid(),
  schema_ref text NOT NULL, version int NOT NULL DEFAULT 1, status text NOT NULL, payload jsonb NOT NULL,
  evidence_refs uuid[] NOT NULL DEFAULT '{}', created_by uuid NOT NULL, created_at timestamptz NOT NULL DEFAULT now(), updated_at timestamptz,
  PRIMARY KEY (tenant_id, id), FOREIGN KEY (tenant_id, company_id) REFERENCES company(tenant_id, company_id));  -- SM-SVC-18-WF01, SM-SVC-18-WF02, SM-SVC-18-WF03, SM-SVC-18-WF04
ALTER TABLE growth_contract ENABLE ROW LEVEL SECURITY; ALTER TABLE growth_contract FORCE ROW LEVEL SECURITY;
CREATE POLICY growth_contract_tenant ON growth_contract USING (tenant_id = current_setting('app.tenant_id')::uuid) WITH CHECK (tenant_id = current_setting('app.tenant_id')::uuid);
CREATE TABLE growth_integration_deal (tenant_id uuid NOT NULL, company_id uuid NOT NULL, id uuid NOT NULL DEFAULT gen_random_uuid(),
  schema_ref text NOT NULL, version int NOT NULL DEFAULT 1, status text NOT NULL, payload jsonb NOT NULL,
  evidence_refs uuid[] NOT NULL DEFAULT '{}', created_by uuid NOT NULL, created_at timestamptz NOT NULL DEFAULT now(), updated_at timestamptz,
  PRIMARY KEY (tenant_id, id), FOREIGN KEY (tenant_id, company_id) REFERENCES company(tenant_id, company_id));  -- SM-SVC-18-WF01, SM-SVC-18-WF02, SM-SVC-18-WF03, SM-SVC-18-WF04
ALTER TABLE growth_integration_deal ENABLE ROW LEVEL SECURITY; ALTER TABLE growth_integration_deal FORCE ROW LEVEL SECURITY;
CREATE POLICY growth_integration_deal_tenant ON growth_integration_deal USING (tenant_id = current_setting('app.tenant_id')::uuid) WITH CHECK (tenant_id = current_setting('app.tenant_id')::uuid);
CREATE TABLE sales_bid (tenant_id uuid NOT NULL, company_id uuid NOT NULL, id uuid NOT NULL DEFAULT gen_random_uuid(),
  schema_ref text NOT NULL, version int NOT NULL DEFAULT 1, status text NOT NULL, payload jsonb NOT NULL,
  evidence_refs uuid[] NOT NULL DEFAULT '{}', created_by uuid NOT NULL, created_at timestamptz NOT NULL DEFAULT now(), updated_at timestamptz,
  PRIMARY KEY (tenant_id, id), FOREIGN KEY (tenant_id, company_id) REFERENCES company(tenant_id, company_id));  -- SM-SVC-19-WF01, SM-SVC-19-WF02, SM-SVC-19-WF03, SM-SVC-19-WF04
ALTER TABLE sales_bid ENABLE ROW LEVEL SECURITY; ALTER TABLE sales_bid FORCE ROW LEVEL SECURITY;
CREATE POLICY sales_bid_tenant ON sales_bid USING (tenant_id = current_setting('app.tenant_id')::uuid) WITH CHECK (tenant_id = current_setting('app.tenant_id')::uuid);
CREATE TABLE growth_invoice (tenant_id uuid NOT NULL, company_id uuid NOT NULL, id uuid NOT NULL DEFAULT gen_random_uuid(),
  schema_ref text NOT NULL, version int NOT NULL DEFAULT 1, status text NOT NULL, payload jsonb NOT NULL,
  evidence_refs uuid[] NOT NULL DEFAULT '{}', created_by uuid NOT NULL, created_at timestamptz NOT NULL DEFAULT now(), updated_at timestamptz,
  PRIMARY KEY (tenant_id, id), FOREIGN KEY (tenant_id, company_id) REFERENCES company(tenant_id, company_id));  -- SM-SVC-20-WF01, SM-SVC-20-WF02, SM-SVC-20-WF03, SM-SVC-20-WF04, SM-SVC-21-WF01, SM-SVC-21-WF02, SM-SVC-21-WF03, SM-SVC-21-WF04, SM-SVC-28-WF01, SM-SVC-28-WF02, 
ALTER TABLE growth_invoice ENABLE ROW LEVEL SECURITY; ALTER TABLE growth_invoice FORCE ROW LEVEL SECURITY;
CREATE POLICY growth_invoice_tenant ON growth_invoice USING (tenant_id = current_setting('app.tenant_id')::uuid) WITH CHECK (tenant_id = current_setting('app.tenant_id')::uuid);
CREATE TABLE growth_payment (tenant_id uuid NOT NULL, company_id uuid NOT NULL, id uuid NOT NULL DEFAULT gen_random_uuid(),
  schema_ref text NOT NULL, version int NOT NULL DEFAULT 1, status text NOT NULL, payload jsonb NOT NULL,
  evidence_refs uuid[] NOT NULL DEFAULT '{}', created_by uuid NOT NULL, created_at timestamptz NOT NULL DEFAULT now(), updated_at timestamptz,
  PRIMARY KEY (tenant_id, id), FOREIGN KEY (tenant_id, company_id) REFERENCES company(tenant_id, company_id));  -- SM-SVC-20-WF01, SM-SVC-20-WF02, SM-SVC-20-WF03, SM-SVC-20-WF04, SM-SVC-21-WF01, SM-SVC-21-WF02, SM-SVC-21-WF03, SM-SVC-21-WF04, SM-SVC-24-WF01, SM-SVC-24-WF02, 
ALTER TABLE growth_payment ENABLE ROW LEVEL SECURITY; ALTER TABLE growth_payment FORCE ROW LEVEL SECURITY;
CREATE POLICY growth_payment_tenant ON growth_payment USING (tenant_id = current_setting('app.tenant_id')::uuid) WITH CHECK (tenant_id = current_setting('app.tenant_id')::uuid);
CREATE TABLE sales_fulfillment (tenant_id uuid NOT NULL, company_id uuid NOT NULL, id uuid NOT NULL DEFAULT gen_random_uuid(),
  schema_ref text NOT NULL, version int NOT NULL DEFAULT 1, status text NOT NULL, payload jsonb NOT NULL,
  evidence_refs uuid[] NOT NULL DEFAULT '{}', created_by uuid NOT NULL, created_at timestamptz NOT NULL DEFAULT now(), updated_at timestamptz,
  PRIMARY KEY (tenant_id, id), FOREIGN KEY (tenant_id, company_id) REFERENCES company(tenant_id, company_id));  -- SM-SVC-20-WF01, SM-SVC-20-WF02, SM-SVC-20-WF03, SM-SVC-20-WF04, SM-SVC-28-WF01, SM-SVC-28-WF02, SM-SVC-28-WF03, SM-SVC-28-WF04, SM-SVC-31-WF01, SM-SVC-31-WF02, 
ALTER TABLE sales_fulfillment ENABLE ROW LEVEL SECURITY; ALTER TABLE sales_fulfillment FORCE ROW LEVEL SECURITY;
CREATE POLICY sales_fulfillment_tenant ON sales_fulfillment USING (tenant_id = current_setting('app.tenant_id')::uuid) WITH CHECK (tenant_id = current_setting('app.tenant_id')::uuid);
CREATE TABLE sales_order (tenant_id uuid NOT NULL, company_id uuid NOT NULL, id uuid NOT NULL DEFAULT gen_random_uuid(),
  schema_ref text NOT NULL, version int NOT NULL DEFAULT 1, status text NOT NULL, payload jsonb NOT NULL,
  evidence_refs uuid[] NOT NULL DEFAULT '{}', created_by uuid NOT NULL, created_at timestamptz NOT NULL DEFAULT now(), updated_at timestamptz,
  PRIMARY KEY (tenant_id, id), FOREIGN KEY (tenant_id, company_id) REFERENCES company(tenant_id, company_id));  -- SM-SVC-20-WF01, SM-SVC-20-WF02, SM-SVC-20-WF03, SM-SVC-20-WF04, SM-SVC-28-WF01, SM-SVC-28-WF02, SM-SVC-28-WF03, SM-SVC-28-WF04, SM-SVC-31-WF01, SM-SVC-31-WF02, 
ALTER TABLE sales_order ENABLE ROW LEVEL SECURITY; ALTER TABLE sales_order FORCE ROW LEVEL SECURITY;
CREATE POLICY sales_order_tenant ON sales_order USING (tenant_id = current_setting('app.tenant_id')::uuid) WITH CHECK (tenant_id = current_setting('app.tenant_id')::uuid);
CREATE TABLE sales_order_line (tenant_id uuid NOT NULL, company_id uuid NOT NULL, id uuid NOT NULL DEFAULT gen_random_uuid(),
  schema_ref text NOT NULL, version int NOT NULL DEFAULT 1, status text NOT NULL, payload jsonb NOT NULL,
  evidence_refs uuid[] NOT NULL DEFAULT '{}', created_by uuid NOT NULL, created_at timestamptz NOT NULL DEFAULT now(), updated_at timestamptz,
  PRIMARY KEY (tenant_id, id), FOREIGN KEY (tenant_id, company_id) REFERENCES company(tenant_id, company_id));  -- SM-SVC-20-WF01, SM-SVC-20-WF02, SM-SVC-20-WF03, SM-SVC-20-WF04, SM-SVC-28-WF01, SM-SVC-28-WF02, SM-SVC-28-WF03, SM-SVC-28-WF04, SM-SVC-31-WF01, SM-SVC-31-WF02, 
ALTER TABLE sales_order_line ENABLE ROW LEVEL SECURITY; ALTER TABLE sales_order_line FORCE ROW LEVEL SECURITY;
CREATE POLICY sales_order_line_tenant ON sales_order_line USING (tenant_id = current_setting('app.tenant_id')::uuid) WITH CHECK (tenant_id = current_setting('app.tenant_id')::uuid);
CREATE TABLE growth_onboarding (tenant_id uuid NOT NULL, company_id uuid NOT NULL, id uuid NOT NULL DEFAULT gen_random_uuid(),
  schema_ref text NOT NULL, version int NOT NULL DEFAULT 1, status text NOT NULL, payload jsonb NOT NULL,
  evidence_refs uuid[] NOT NULL DEFAULT '{}', created_by uuid NOT NULL, created_at timestamptz NOT NULL DEFAULT now(), updated_at timestamptz,
  PRIMARY KEY (tenant_id, id), FOREIGN KEY (tenant_id, company_id) REFERENCES company(tenant_id, company_id));  -- SM-SVC-22-WF01, SM-SVC-22-WF02, SM-SVC-22-WF03, SM-SVC-22-WF04, SM-SVC-33-WF01, SM-SVC-33-WF02, SM-SVC-33-WF03, SM-SVC-33-WF04
ALTER TABLE growth_onboarding ENABLE ROW LEVEL SECURITY; ALTER TABLE growth_onboarding FORCE ROW LEVEL SECURITY;
CREATE POLICY growth_onboarding_tenant ON growth_onboarding USING (tenant_id = current_setting('app.tenant_id')::uuid) WITH CHECK (tenant_id = current_setting('app.tenant_id')::uuid);
CREATE TABLE growth_deployment (tenant_id uuid NOT NULL, company_id uuid NOT NULL, id uuid NOT NULL DEFAULT gen_random_uuid(),
  schema_ref text NOT NULL, version int NOT NULL DEFAULT 1, status text NOT NULL, payload jsonb NOT NULL,
  evidence_refs uuid[] NOT NULL DEFAULT '{}', created_by uuid NOT NULL, created_at timestamptz NOT NULL DEFAULT now(), updated_at timestamptz,
  PRIMARY KEY (tenant_id, id), FOREIGN KEY (tenant_id, company_id) REFERENCES company(tenant_id, company_id));  -- SM-SVC-22-WF01, SM-SVC-22-WF02, SM-SVC-22-WF03, SM-SVC-22-WF04, SM-SVC-32-WF01, SM-SVC-32-WF02, SM-SVC-32-WF03, SM-SVC-32-WF04
ALTER TABLE growth_deployment ENABLE ROW LEVEL SECURITY; ALTER TABLE growth_deployment FORCE ROW LEVEL SECURITY;
CREATE POLICY growth_deployment_tenant ON growth_deployment USING (tenant_id = current_setting('app.tenant_id')::uuid) WITH CHECK (tenant_id = current_setting('app.tenant_id')::uuid);
CREATE TABLE growth_partner (tenant_id uuid NOT NULL, company_id uuid NOT NULL, id uuid NOT NULL DEFAULT gen_random_uuid(),
  schema_ref text NOT NULL, version int NOT NULL DEFAULT 1, status text NOT NULL, payload jsonb NOT NULL,
  evidence_refs uuid[] NOT NULL DEFAULT '{}', created_by uuid NOT NULL, created_at timestamptz NOT NULL DEFAULT now(), updated_at timestamptz,
  PRIMARY KEY (tenant_id, id), FOREIGN KEY (tenant_id, company_id) REFERENCES company(tenant_id, company_id));  -- SM-SVC-22-WF01, SM-SVC-22-WF02, SM-SVC-22-WF03, SM-SVC-22-WF04, SM-SVC-32-WF01, SM-SVC-32-WF02, SM-SVC-32-WF03, SM-SVC-32-WF04
ALTER TABLE growth_partner ENABLE ROW LEVEL SECURITY; ALTER TABLE growth_partner FORCE ROW LEVEL SECURITY;
CREATE POLICY growth_partner_tenant ON growth_partner USING (tenant_id = current_setting('app.tenant_id')::uuid) WITH CHECK (tenant_id = current_setting('app.tenant_id')::uuid);
CREATE TABLE growth_pilot (tenant_id uuid NOT NULL, company_id uuid NOT NULL, id uuid NOT NULL DEFAULT gen_random_uuid(),
  schema_ref text NOT NULL, version int NOT NULL DEFAULT 1, status text NOT NULL, payload jsonb NOT NULL,
  evidence_refs uuid[] NOT NULL DEFAULT '{}', created_by uuid NOT NULL, created_at timestamptz NOT NULL DEFAULT now(), updated_at timestamptz,
  PRIMARY KEY (tenant_id, id), FOREIGN KEY (tenant_id, company_id) REFERENCES company(tenant_id, company_id));  -- SM-SVC-22-WF01, SM-SVC-22-WF02, SM-SVC-22-WF03, SM-SVC-22-WF04, SM-SVC-32-WF01, SM-SVC-32-WF02, SM-SVC-32-WF03, SM-SVC-32-WF04
ALTER TABLE growth_pilot ENABLE ROW LEVEL SECURITY; ALTER TABLE growth_pilot FORCE ROW LEVEL SECURITY;
CREATE POLICY growth_pilot_tenant ON growth_pilot USING (tenant_id = current_setting('app.tenant_id')::uuid) WITH CHECK (tenant_id = current_setting('app.tenant_id')::uuid);
CREATE TABLE growth_renewal (tenant_id uuid NOT NULL, company_id uuid NOT NULL, id uuid NOT NULL DEFAULT gen_random_uuid(),
  schema_ref text NOT NULL, version int NOT NULL DEFAULT 1, status text NOT NULL, payload jsonb NOT NULL,
  evidence_refs uuid[] NOT NULL DEFAULT '{}', created_by uuid NOT NULL, created_at timestamptz NOT NULL DEFAULT now(), updated_at timestamptz,
  PRIMARY KEY (tenant_id, id), FOREIGN KEY (tenant_id, company_id) REFERENCES company(tenant_id, company_id));  -- SM-SVC-23-WF01, SM-SVC-23-WF02, SM-SVC-23-WF03, SM-SVC-23-WF04, SM-SVC-34-WF01, SM-SVC-34-WF02, SM-SVC-34-WF03, SM-SVC-34-WF04
ALTER TABLE growth_renewal ENABLE ROW LEVEL SECURITY; ALTER TABLE growth_renewal FORCE ROW LEVEL SECURITY;
CREATE POLICY growth_renewal_tenant ON growth_renewal USING (tenant_id = current_setting('app.tenant_id')::uuid) WITH CHECK (tenant_id = current_setting('app.tenant_id')::uuid);
CREATE TABLE growth_feedback (tenant_id uuid NOT NULL, company_id uuid NOT NULL, id uuid NOT NULL DEFAULT gen_random_uuid(),
  schema_ref text NOT NULL, version int NOT NULL DEFAULT 1, status text NOT NULL, payload jsonb NOT NULL,
  evidence_refs uuid[] NOT NULL DEFAULT '{}', created_by uuid NOT NULL, created_at timestamptz NOT NULL DEFAULT now(), updated_at timestamptz,
  PRIMARY KEY (tenant_id, id), FOREIGN KEY (tenant_id, company_id) REFERENCES company(tenant_id, company_id));  -- SM-SVC-23-WF01, SM-SVC-23-WF02, SM-SVC-23-WF03, SM-SVC-23-WF04, SM-SVC-35-WF01, SM-SVC-35-WF02, SM-SVC-35-WF03, SM-SVC-35-WF04
ALTER TABLE growth_feedback ENABLE ROW LEVEL SECURITY; ALTER TABLE growth_feedback FORCE ROW LEVEL SECURITY;
CREATE POLICY growth_feedback_tenant ON growth_feedback USING (tenant_id = current_setting('app.tenant_id')::uuid) WITH CHECK (tenant_id = current_setting('app.tenant_id')::uuid);
CREATE TABLE growth_metric_snapshot (tenant_id uuid NOT NULL, company_id uuid NOT NULL, id uuid NOT NULL DEFAULT gen_random_uuid(),
  schema_ref text NOT NULL, version int NOT NULL DEFAULT 1, status text NOT NULL, payload jsonb NOT NULL,
  evidence_refs uuid[] NOT NULL DEFAULT '{}', created_by uuid NOT NULL, created_at timestamptz NOT NULL DEFAULT now(), updated_at timestamptz,
  PRIMARY KEY (tenant_id, id), FOREIGN KEY (tenant_id, company_id) REFERENCES company(tenant_id, company_id));  -- SM-SVC-24-WF01, SM-SVC-24-WF02, SM-SVC-24-WF03, SM-SVC-24-WF04, SM-SVC-30-WF01, SM-SVC-30-WF02, SM-SVC-30-WF03, SM-SVC-30-WF04, SM-SVC-32-WF01, SM-SVC-32-WF02, 
ALTER TABLE growth_metric_snapshot ENABLE ROW LEVEL SECURITY; ALTER TABLE growth_metric_snapshot FORCE ROW LEVEL SECURITY;
CREATE POLICY growth_metric_snapshot_tenant ON growth_metric_snapshot USING (tenant_id = current_setting('app.tenant_id')::uuid) WITH CHECK (tenant_id = current_setting('app.tenant_id')::uuid);
CREATE TABLE growth_forecast (tenant_id uuid NOT NULL, company_id uuid NOT NULL, id uuid NOT NULL DEFAULT gen_random_uuid(),
  schema_ref text NOT NULL, version int NOT NULL DEFAULT 1, status text NOT NULL, payload jsonb NOT NULL,
  evidence_refs uuid[] NOT NULL DEFAULT '{}', created_by uuid NOT NULL, created_at timestamptz NOT NULL DEFAULT now(), updated_at timestamptz,
  PRIMARY KEY (tenant_id, id), FOREIGN KEY (tenant_id, company_id) REFERENCES company(tenant_id, company_id));  -- SM-SVC-24-WF01, SM-SVC-24-WF02, SM-SVC-24-WF03, SM-SVC-24-WF04, SM-SVC-37-WF01, SM-SVC-37-WF02, SM-SVC-37-WF03, SM-SVC-37-WF04
ALTER TABLE growth_forecast ENABLE ROW LEVEL SECURITY; ALTER TABLE growth_forecast FORCE ROW LEVEL SECURITY;
CREATE POLICY growth_forecast_tenant ON growth_forecast USING (tenant_id = current_setting('app.tenant_id')::uuid) WITH CHECK (tenant_id = current_setting('app.tenant_id')::uuid);
CREATE TABLE growth_stage_metric (tenant_id uuid NOT NULL, company_id uuid NOT NULL, id uuid NOT NULL DEFAULT gen_random_uuid(),
  schema_ref text NOT NULL, version int NOT NULL DEFAULT 1, status text NOT NULL, payload jsonb NOT NULL,
  evidence_refs uuid[] NOT NULL DEFAULT '{}', created_by uuid NOT NULL, created_at timestamptz NOT NULL DEFAULT now(), updated_at timestamptz,
  PRIMARY KEY (tenant_id, id), FOREIGN KEY (tenant_id, company_id) REFERENCES company(tenant_id, company_id));  -- SM-SVC-24-WF01, SM-SVC-24-WF02, SM-SVC-24-WF03, SM-SVC-24-WF04, SM-SVC-37-WF01, SM-SVC-37-WF02, SM-SVC-37-WF03, SM-SVC-37-WF04
ALTER TABLE growth_stage_metric ENABLE ROW LEVEL SECURITY; ALTER TABLE growth_stage_metric FORCE ROW LEVEL SECURITY;
CREATE POLICY growth_stage_metric_tenant ON growth_stage_metric USING (tenant_id = current_setting('app.tenant_id')::uuid) WITH CHECK (tenant_id = current_setting('app.tenant_id')::uuid);
CREATE TABLE growth_document (tenant_id uuid NOT NULL, company_id uuid NOT NULL, id uuid NOT NULL DEFAULT gen_random_uuid(),
  schema_ref text NOT NULL, version int NOT NULL DEFAULT 1, status text NOT NULL, payload jsonb NOT NULL,
  evidence_refs uuid[] NOT NULL DEFAULT '{}', created_by uuid NOT NULL, created_at timestamptz NOT NULL DEFAULT now(), updated_at timestamptz,
  PRIMARY KEY (tenant_id, id), FOREIGN KEY (tenant_id, company_id) REFERENCES company(tenant_id, company_id));  -- SM-SVC-25-WF01, SM-SVC-25-WF02, SM-SVC-25-WF03, SM-SVC-25-WF04
ALTER TABLE growth_document ENABLE ROW LEVEL SECURITY; ALTER TABLE growth_document FORCE ROW LEVEL SECURITY;
CREATE POLICY growth_document_tenant ON growth_document USING (tenant_id = current_setting('app.tenant_id')::uuid) WITH CHECK (tenant_id = current_setting('app.tenant_id')::uuid);
CREATE TABLE growth_document_chunk (tenant_id uuid NOT NULL, company_id uuid NOT NULL, id uuid NOT NULL DEFAULT gen_random_uuid(),
  schema_ref text NOT NULL, version int NOT NULL DEFAULT 1, status text NOT NULL, payload jsonb NOT NULL,
  evidence_refs uuid[] NOT NULL DEFAULT '{}', created_by uuid NOT NULL, created_at timestamptz NOT NULL DEFAULT now(), updated_at timestamptz,
  PRIMARY KEY (tenant_id, id), FOREIGN KEY (tenant_id, company_id) REFERENCES company(tenant_id, company_id));  -- SM-SVC-25-WF01, SM-SVC-25-WF02, SM-SVC-25-WF03, SM-SVC-25-WF04
ALTER TABLE growth_document_chunk ENABLE ROW LEVEL SECURITY; ALTER TABLE growth_document_chunk FORCE ROW LEVEL SECURITY;
CREATE POLICY growth_document_chunk_tenant ON growth_document_chunk USING (tenant_id = current_setting('app.tenant_id')::uuid) WITH CHECK (tenant_id = current_setting('app.tenant_id')::uuid);
CREATE TABLE growth_embedding (tenant_id uuid NOT NULL, company_id uuid NOT NULL, id uuid NOT NULL DEFAULT gen_random_uuid(),
  schema_ref text NOT NULL, version int NOT NULL DEFAULT 1, status text NOT NULL, payload jsonb NOT NULL,
  evidence_refs uuid[] NOT NULL DEFAULT '{}', created_by uuid NOT NULL, created_at timestamptz NOT NULL DEFAULT now(), updated_at timestamptz,
  PRIMARY KEY (tenant_id, id), FOREIGN KEY (tenant_id, company_id) REFERENCES company(tenant_id, company_id));  -- SM-SVC-25-WF01, SM-SVC-25-WF02, SM-SVC-25-WF03, SM-SVC-25-WF04
ALTER TABLE growth_embedding ENABLE ROW LEVEL SECURITY; ALTER TABLE growth_embedding FORCE ROW LEVEL SECURITY;
CREATE POLICY growth_embedding_tenant ON growth_embedding USING (tenant_id = current_setting('app.tenant_id')::uuid) WITH CHECK (tenant_id = current_setting('app.tenant_id')::uuid);