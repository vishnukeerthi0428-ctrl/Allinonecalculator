-- V0006__ddl_v12_r_platform_decisions
SET search_path = ge, extensions, public;

SELECT set_config('app.zone', coalesce(nullif(current_setting('app.deployment_region', true), ''), 'IN'), false);

SELECT set_config('app.deployment_region', coalesce(nullif(current_setting('app.deployment_region', true), ''), 'IN'), false);

CREATE TABLE ge.idp_connection (
  tenant_id        uuid NOT NULL REFERENCES ge.tenant(tenant_id),
  connection_id    uuid NOT NULL DEFAULT gen_random_uuid(),
  display_name     text NOT NULL,
  vendor           text NOT NULL CHECK (vendor IN ('okta','entra_id','google_workspace','generic_saml','generic_oidc')),
  protocol         text NOT NULL CHECK (protocol IN ('SAML 2.0','OpenID Connect')),
  issuer           text NOT NULL,                      -- SAML entityID or OIDC iss
  metadata_url     text CHECK (metadata_url ~ '^https://'),
  sso_url          text NOT NULL CHECK (sso_url ~ '^https://'),
  audience         text NOT NULL,                      -- our SP entityID / client_id, per zone
  attribute_map    jsonb NOT NULL DEFAULT '{"email":"email","given_name":"given_name","family_name":"family_name","groups":"groups"}',
  broker_ref       text,                               -- connection id inside the reused IdP broker
  state            text NOT NULL DEFAULT 'draft' CHECK (state IN ('draft','testing','active','disabled')),
  enforced         boolean NOT NULL DEFAULT false,
  last_test_ok_at  timestamptz,
  created_by       uuid NOT NULL, created_at timestamptz NOT NULL DEFAULT now(),
  version          int NOT NULL DEFAULT 1,
  PRIMARY KEY (tenant_id, connection_id),
  CHECK (NOT (vendor = 'generic_saml' AND protocol <> 'SAML 2.0')),
  CHECK (NOT (vendor = 'generic_oidc' AND protocol <> 'OpenID Connect')),
  CHECK (state = 'active' OR NOT enforced),
  CHECK (state <> 'active' OR last_test_ok_at IS NOT NULL)          -- test login before activation
);

CREATE TABLE ge.idp_certificate (
  tenant_id uuid NOT NULL, connection_id uuid NOT NULL, cert_id uuid NOT NULL DEFAULT gen_random_uuid(),
  use text NOT NULL CHECK (use IN ('signing','encryption')), pem_sha256 bytea NOT NULL, not_after timestamptz NOT NULL,
  active boolean NOT NULL DEFAULT true, PRIMARY KEY (tenant_id, cert_id),
  FOREIGN KEY (tenant_id, connection_id) REFERENCES ge.idp_connection(tenant_id, connection_id));

CREATE UNIQUE INDEX ux_idp_cert_two_active ON ge.idp_certificate (tenant_id, connection_id, use, cert_id) WHERE active;

CREATE TABLE ge.verified_domain (
  tenant_id uuid NOT NULL, domain_id uuid NOT NULL DEFAULT gen_random_uuid(),
  domain citext NOT NULL CHECK (domain ~ '^[a-z0-9.-]+\.[a-z]{2,}$'),
  txt_token text NOT NULL, state text NOT NULL DEFAULT 'pending' CHECK (state IN ('pending','verified','verification_lost','released')),
  connection_id uuid, consecutive_misses int NOT NULL DEFAULT 0, last_checked_at timestamptz, verified_at timestamptz,
  PRIMARY KEY (tenant_id, domain_id),
  FOREIGN KEY (tenant_id, connection_id) REFERENCES ge.idp_connection(tenant_id, connection_id));

CREATE UNIQUE INDEX ux_verified_domain_global ON ge.verified_domain (domain) WHERE state IN ('verified','verification_lost');

CREATE TABLE ge.breakglass_account (
  tenant_id uuid NOT NULL, user_id uuid NOT NULL, hardware_key_registered boolean NOT NULL,
  last_test_at timestamptz, PRIMARY KEY (tenant_id, user_id), CHECK (hardware_key_registered));

CREATE OR REPLACE FUNCTION ge.enforce_sso_guard() RETURNS trigger LANGUAGE plpgsql AS $$
BEGIN
  IF NEW.enforced AND NOT EXISTS (SELECT 1 FROM ge.verified_domain d WHERE d.tenant_id = NEW.tenant_id
        AND d.connection_id = NEW.connection_id AND d.state IN ('verified','verification_lost')) THEN
    RAISE EXCEPTION 'SSO_ENFORCEMENT_REQUIRES_VERIFIED_DOMAIN' USING ERRCODE = 'check_violation'; END IF;
  IF NEW.enforced AND NOT EXISTS (SELECT 1 FROM ge.breakglass_account b WHERE b.tenant_id = NEW.tenant_id) THEN
    RAISE EXCEPTION 'SSO_ENFORCEMENT_REQUIRES_BREAKGLASS' USING ERRCODE = 'check_violation'; END IF;
  RETURN NEW; END $$;

CREATE TRIGGER idp_connection_enforce_guard BEFORE INSERT OR UPDATE OF enforced ON ge.idp_connection
  FOR EACH ROW EXECUTE FUNCTION ge.enforce_sso_guard();

DROP TABLE IF EXISTS ge.identity_provider CASCADE;

CREATE TABLE ge.tenant_security_policy (
  tenant_id uuid PRIMARY KEY REFERENCES ge.tenant(tenant_id),
  mfa_mode text NOT NULL DEFAULT 'required_privileged' CHECK (mfa_mode IN ('required_privileged','required_all')),
  privileged_factor text NOT NULL DEFAULT 'phishing_resistant' CHECK (privileged_factor = 'phishing_resistant'),  -- floor DEC-077
  max_session_hours int NOT NULL DEFAULT 12 CHECK (max_session_hours BETWEEN 1 AND 24),
  idle_minutes int NOT NULL DEFAULT 30 CHECK (idle_minutes BETWEEN 5 AND 120),
  version int NOT NULL DEFAULT 1, updated_by uuid, updated_at timestamptz NOT NULL DEFAULT now());

CREATE TABLE ge.user_session (
  tenant_id uuid NOT NULL, session_id uuid NOT NULL DEFAULT gen_random_uuid(), user_id uuid NOT NULL,
  connection_id uuid, amr text[] NOT NULL DEFAULT '{}', acr text, privileged boolean NOT NULL,
  created_at timestamptz NOT NULL DEFAULT now(), last_seen_at timestamptz NOT NULL DEFAULT now(),
  expires_at timestamptz NOT NULL, revoked_at timestamptz, revoke_reason text,
  PRIMARY KEY (tenant_id, session_id));

CREATE INDEX ix_user_session_live ON ge.user_session (tenant_id, user_id) WHERE revoked_at IS NULL;

ALTER TABLE ge.scim_token ADD COLUMN IF NOT EXISTS zone text NOT NULL DEFAULT current_setting('app.zone') CHECK (zone IN ('IN','EU'));

ALTER TABLE ge.scim_token ADD COLUMN IF NOT EXISTS last_used_at timestamptz;

CREATE TABLE ge.scim_identity (
  tenant_id uuid NOT NULL, user_id uuid NOT NULL, external_id text NOT NULL, user_name citext NOT NULL,
  active boolean NOT NULL DEFAULT true, meta_version int NOT NULL DEFAULT 1, idp_last_modified timestamptz,
  deprovisioned_at timestamptz, PRIMARY KEY (tenant_id, user_id), UNIQUE (tenant_id, external_id), UNIQUE (tenant_id, user_name));

CREATE TABLE ge.scim_group (
  tenant_id uuid NOT NULL, group_id uuid NOT NULL DEFAULT gen_random_uuid(), external_id text, display_name text NOT NULL,
  PRIMARY KEY (tenant_id, group_id), UNIQUE (tenant_id, display_name));

CREATE TABLE ge.scim_group_member (tenant_id uuid NOT NULL, group_id uuid NOT NULL, user_id uuid NOT NULL,
  PRIMARY KEY (tenant_id, group_id, user_id), FOREIGN KEY (tenant_id, group_id) REFERENCES ge.scim_group(tenant_id, group_id));

CREATE TABLE ge.scim_group_role_map (
  tenant_id uuid NOT NULL, group_id uuid NOT NULL, role_id uuid NOT NULL, company_id uuid,
  state text NOT NULL DEFAULT 'requested' CHECK (state IN ('requested','approved','blocked','retired')),
  requested_by uuid NOT NULL, approved_by uuid, CHECK (approved_by IS NULL OR approved_by <> requested_by),
  PRIMARY KEY (tenant_id, group_id, role_id));

CREATE TABLE ge.scim_deprovision_sla (
  tenant_id uuid NOT NULL, user_id uuid NOT NULL, idp_changed_at timestamptz, received_at timestamptz NOT NULL,
  revoked_at timestamptz, product_ms int GENERATED ALWAYS AS ((extract(epoch FROM revoked_at - received_at) * 1000)::int) STORED,
  end_to_end_s int GENERATED ALWAYS AS ((extract(epoch FROM revoked_at - coalesce(idp_changed_at, received_at)))::int) STORED,
  PRIMARY KEY (tenant_id, user_id, received_at));

ALTER TABLE ge.custom_role ADD COLUMN IF NOT EXISTS scope text NOT NULL DEFAULT 'tenant' CHECK (scope IN ('tenant','company'));

ALTER TABLE ge.custom_role ADD COLUMN IF NOT EXISTS privileged boolean NOT NULL DEFAULT false;

ALTER TABLE ge.custom_role ADD COLUMN IF NOT EXISTS permissions_hash bytea;

ALTER TABLE ge.custom_role ADD COLUMN IF NOT EXISTS state text NOT NULL DEFAULT 'active' CHECK (state IN ('active','retired'));

CREATE TABLE ge.permission_catalogue (
  permission text PRIMARY KEY CHECK (permission ~ '^[A-Z][A-Za-z]+:[a-z_]+$'), resource text NOT NULL, action text NOT NULL,
  privileged boolean NOT NULL, consequential boolean NOT NULL, catalogue_version int NOT NULL);

ALTER TABLE ge.sod_conflict ADD COLUMN IF NOT EXISTS source text NOT NULL DEFAULT 'V12-C2';

INSERT INTO ge.sod_conflict (permission_a, permission_b, source) VALUES
  ('Finance:verify_first','Finance:verify_second','DEC-898'), ('Billing:purchase','Billing:approve_refund','DEC-898'),
  ('Roles:edit','Roles:approve_assignment','DEC-898'), ('Mandates:request','Mandates:approve','DEC-898 + Part 11.17'),
  ('Connectors:request_activation','Connectors:approve_activation','DEC-898'), ('Models:propose','Models:approve','DEC-898 + DEC-890'),
  ('Benchmarks:enrol','Benchmarks:approve_release','DEC-898 + DEC-893'), ('ApiKeys:create_unmasked_scope','ApiKeys:approve_unmasked_scope','DEC-898')
ON CONFLICT DO NOTHING;

CREATE TABLE ge.access_recert_campaign (
  tenant_id uuid NOT NULL, campaign_id uuid NOT NULL DEFAULT gen_random_uuid(), opened_at timestamptz NOT NULL, due_at timestamptz NOT NULL,
  state text NOT NULL CHECK (state IN ('open','closed','escalated')), PRIMARY KEY (tenant_id, campaign_id));

CREATE TABLE ge.access_recert_item (
  tenant_id uuid NOT NULL, campaign_id uuid NOT NULL, user_id uuid NOT NULL, role_id uuid NOT NULL,
  decision text CHECK (decision IN ('keep','remove')), decided_by uuid, decided_at timestamptz,
  CHECK (decided_by IS NULL OR decided_by <> user_id),                -- nobody recertifies themself
  PRIMARY KEY (tenant_id, campaign_id, user_id, role_id));

ALTER TABLE ge.api_key ADD COLUMN IF NOT EXISTS zone text NOT NULL DEFAULT current_setting('app.zone') CHECK (zone IN ('IN','EU'));

ALTER TABLE ge.api_key ADD COLUMN IF NOT EXISTS environment text NOT NULL DEFAULT 'live' CHECK (environment IN ('live','test'));

ALTER TABLE ge.api_key ADD COLUMN IF NOT EXISTS created_by uuid NOT NULL;

ALTER TABLE ge.api_key ADD COLUMN IF NOT EXISTS last_used_at timestamptz;

ALTER TABLE ge.api_key ADD COLUMN IF NOT EXISTS revoke_reason text CHECK (revoke_reason IN ('owner','expired','deprovisioned','leak_report','idle','admin'));

ALTER TABLE ge.api_key ADD CONSTRAINT api_key_no_consequential_scope_ck
  CHECK (NOT scopes && ARRAY['approve','send','publish','pay','sign','bids:submit','prices:set','roles:write','policies:write']::text[]);

CREATE TABLE ge.oauth_client (
  tenant_id uuid NOT NULL REFERENCES ge.tenant(tenant_id), client_id text NOT NULL CHECK (client_id ~ '^gec_[a-z0-9]{20}$'),
  zone text NOT NULL CHECK (zone IN ('IN','EU')), name text NOT NULL,
  auth_method text NOT NULL CHECK (auth_method IN ('private_key_jwt','client_secret_basic')),
  jwks_url text CHECK (jwks_url ~ '^https://'), jwks_inline jsonb, secret_hash bytea, secret_expires_at timestamptz,
  scopes text[] NOT NULL CHECK (cardinality(scopes) > 0), ip_allowlist cidr[], state text NOT NULL DEFAULT 'active' CHECK (state IN ('active','suspended','revoked')),
  created_by uuid NOT NULL, created_at timestamptz NOT NULL DEFAULT now(), last_token_at timestamptz,
  PRIMARY KEY (tenant_id, client_id), UNIQUE (client_id),
  CHECK (auth_method <> 'private_key_jwt' OR jwks_url IS NOT NULL OR jwks_inline IS NOT NULL),
  CHECK (auth_method <> 'client_secret_basic' OR (secret_hash IS NOT NULL AND secret_expires_at IS NOT NULL)),
  CHECK (NOT scopes && ARRAY['approve','send','publish','pay','sign','bids:submit','prices:set','roles:write','policies:write']::text[]));

CREATE TABLE ge.oauth_jti_seen (client_id text NOT NULL, jti text NOT NULL, exp timestamptz NOT NULL, PRIMARY KEY (client_id, jti));

ALTER TABLE ge.webhook_endpoint ADD COLUMN IF NOT EXISTS secret_version int NOT NULL DEFAULT 1;

ALTER TABLE ge.webhook_endpoint ADD COLUMN IF NOT EXISTS previous_secret_ref text;

ALTER TABLE ge.webhook_endpoint ADD COLUMN IF NOT EXISTS previous_secret_until timestamptz;

ALTER TABLE ge.webhook_endpoint ADD COLUMN IF NOT EXISTS disabled_reason text CHECK (disabled_reason IN ('owner','gone_410','exhausted_threshold','verification_failed'));

ALTER TABLE ge.webhook_endpoint ADD COLUMN IF NOT EXISTS consecutive_exhausted int NOT NULL DEFAULT 0;

ALTER TABLE ge.webhook_delivery ADD COLUMN IF NOT EXISTS event_id uuid NOT NULL;

ALTER TABLE ge.webhook_delivery ADD COLUMN IF NOT EXISTS next_attempt_at timestamptz;

ALTER TABLE ge.webhook_delivery ADD COLUMN IF NOT EXISTS outcome text NOT NULL DEFAULT 'pending' CHECK (outcome IN ('pending','succeeded','failed','exhausted','disabled','replayed'));

ALTER TABLE ge.webhook_delivery ADD COLUMN IF NOT EXISTS latency_ms int;

ALTER TABLE ge.webhook_delivery DROP CONSTRAINT IF EXISTS webhook_delivery_attempt_uq;

ALTER TABLE ge.webhook_delivery ADD CONSTRAINT webhook_delivery_attempt_uq UNIQUE (tenant_id, endpoint_id, event_id, attempt);

ALTER TABLE ge.sandbox_environment ADD COLUMN IF NOT EXISTS sandbox_tenant_id uuid NOT NULL;

ALTER TABLE ge.sandbox_environment ADD COLUMN IF NOT EXISTS dataset_version text NOT NULL DEFAULT 'gse_syn 1.4.0';

ALTER TABLE ge.config_promotion ADD COLUMN IF NOT EXISTS config_revision_id uuid NOT NULL;

ALTER TABLE ge.config_promotion ADD COLUMN IF NOT EXISTS diff_hash bytea NOT NULL;

ALTER TABLE ge.config_promotion DROP CONSTRAINT IF EXISTS config_promotion_status_ck;

ALTER TABLE ge.config_promotion ADD CONSTRAINT config_promotion_status_ck CHECK (status IN ('Requested','Approved','Rejected','Applied','RolledBack'));

ALTER TABLE ge.tenant DROP CONSTRAINT IF EXISTS tenant_kind_ck;

ALTER TABLE ge.tenant ADD CONSTRAINT tenant_kind_ck CHECK (kind IN ('owned','client','sandbox'));

ALTER TABLE ge.connector_installation ADD COLUMN IF NOT EXISTS provider text NOT NULL
  CHECK (provider IN ('salesforce','hubspot','zoho_crm','sms_dlt_aggregator','voice_cpaas','ses','whatsapp_bsp','google_calendar','m365_calendar','payments','warehouse','siem','idp'));

ALTER TABLE ge.connector_installation ADD COLUMN IF NOT EXISTS ownership text NOT NULL DEFAULT 'tenant_byo' CHECK (ownership IN ('tenant_byo','platform'));

ALTER TABLE ge.connector_installation ADD COLUMN IF NOT EXISTS dpa_ref text;

ALTER TABLE ge.connector_installation ADD COLUMN IF NOT EXISTS transfer_entry_ref text;

ALTER TABLE ge.connector_installation ADD COLUMN IF NOT EXISTS registration_ref text;

ALTER TABLE ge.connector_installation ADD COLUMN IF NOT EXISTS markets text[] NOT NULL DEFAULT '{}';

ALTER TABLE ge.connector_installation ADD COLUMN IF NOT EXISTS requested_by uuid, ADD COLUMN IF NOT EXISTS approved_by uuid;

ALTER TABLE ge.connector_installation DROP CONSTRAINT IF EXISTS connector_gate_ck;

ALTER TABLE ge.connector_installation ADD CONSTRAINT connector_gate_ck CHECK (
  environment = 'sandbox' OR status NOT IN ('Active') OR (
    legal_review_ref IS NOT NULL AND security_review_ref IS NOT NULL AND dpa_ref IS NOT NULL AND transfer_entry_ref IS NOT NULL
    AND approved_by IS NOT NULL AND approved_by <> requested_by
    AND (provider NOT IN ('sms_dlt_aggregator','voice_cpaas','whatsapp_bsp') OR registration_ref IS NOT NULL)));

CREATE OR REPLACE FUNCTION ge.connector_pack_guard() RETURNS trigger LANGUAGE plpgsql AS $$
BEGIN
  -- v1.2 (Part 11.25, CONFLICT-1215 resolved by DEC-1000): Appendix C names. Packs are keyed by
  -- jurisdiction_pack.jurisdiction / pack_code, status vocabulary 'Approved'; the required packs per
  -- capability come from ge.rulepack_requirement, the same join as ge.fn_activation_gate().
  IF NEW.environment = 'production' AND NEW.status = 'Active' AND EXISTS (
       SELECT 1 FROM unnest(NEW.markets) m WHERE
         NOT EXISTS (SELECT 1 FROM ge.jurisdiction_pack p WHERE p.jurisdiction = m AND p.status = 'Approved'
                       AND p.counsel_signoff_ref IS NOT NULL AND p.effective_from <= current_date
                       AND (p.effective_to IS NULL OR p.effective_to >= current_date))
         OR EXISTS (SELECT 1 FROM ge.rulepack_requirement r
                     WHERE r.jurisdiction = m
                       AND r.capability = CASE NEW.provider WHEN 'sms_dlt_aggregator' THEN 'outreach.sms'
                                            WHEN 'whatsapp_bsp' THEN 'outreach.whatsapp' WHEN 'ses' THEN 'outreach.email'
                                            WHEN 'voice_cpaas' THEN 'voice.ai_calls' WHEN 'payments' THEN 'payments.mandated' END
                       AND NOT EXISTS (SELECT 1 FROM ge.jurisdiction_pack p WHERE p.pack_code = r.pack_code AND p.status = 'Approved'
                                         AND p.counsel_signoff_ref IS NOT NULL AND p.effective_from <= current_date
                                         AND (p.effective_to IS NULL OR p.effective_to >= current_date)))) THEN
    RAISE EXCEPTION 'CONNECTOR_MARKET_PACK_NOT_APPROVED' USING ERRCODE = 'check_violation'; END IF;
  RETURN NEW; END $$;

CREATE TRIGGER connector_installation_pack_guard BEFORE INSERT OR UPDATE ON ge.connector_installation
  FOR EACH ROW EXECUTE FUNCTION ge.connector_pack_guard();

CREATE TABLE ge.crm_field_mapping (
  tenant_id uuid NOT NULL, installation_id uuid NOT NULL, mapping_version int NOT NULL, object text NOT NULL CHECK (object IN ('contact','organization','deal','activity')),
  platform_field text NOT NULL, crm_field text NOT NULL, policy text NOT NULL CHECK (policy IN ('platform_wins','crm_wins','newest_wins','platform_wins_stricter')),
  PRIMARY KEY (tenant_id, installation_id, mapping_version, object, platform_field),
  CHECK (platform_field NOT IN ('consent_state','suppression','approval_state','mandate_id') OR policy = 'platform_wins_stricter'));

CREATE TABLE ge.crm_link (
  tenant_id uuid NOT NULL, installation_id uuid NOT NULL, object text NOT NULL, platform_id uuid NOT NULL, crm_id text NOT NULL,
  last_platform_version int, last_crm_version text, last_synced_at timestamptz,
  PRIMARY KEY (tenant_id, installation_id, object, platform_id), UNIQUE (tenant_id, installation_id, object, crm_id));

CREATE TABLE ge.sync_cursor (tenant_id uuid NOT NULL, installation_id uuid NOT NULL, object text NOT NULL, cursor text, cursor_at timestamptz, gap_detected boolean NOT NULL DEFAULT false,
  PRIMARY KEY (tenant_id, installation_id, object));

CREATE TABLE ge.sync_conflict (tenant_id uuid NOT NULL, conflict_id uuid NOT NULL DEFAULT gen_random_uuid(), installation_id uuid NOT NULL, object text NOT NULL,
  platform_id uuid NOT NULL, field text NOT NULL, platform_value_hash bytea, crm_value_hash bytea, state text NOT NULL DEFAULT 'open' CHECK (state IN ('open','resolved_platform','resolved_crm','ignored')),
  resolved_by uuid, PRIMARY KEY (tenant_id, conflict_id));

CREATE TABLE ge.dlt_registration (
  tenant_id uuid NOT NULL, company_id uuid NOT NULL, channel_account_id uuid NOT NULL, entity_id text NOT NULL CHECK (entity_id ~ '^[0-9]{19}$'),
  header text NOT NULL CHECK (header ~ '^[A-Z0-9]{3,11}$'), header_type text NOT NULL CHECK (header_type IN ('promotional','service_implicit','service_explicit','transactional')),
  valid_from date NOT NULL, valid_to date, PRIMARY KEY (tenant_id, channel_account_id, header));

CREATE TABLE ge.dlt_template (
  tenant_id uuid NOT NULL, channel_account_id uuid NOT NULL, template_id text NOT NULL, header text NOT NULL, category text NOT NULL,
  body_pattern text NOT NULL, variables int NOT NULL CHECK (variables BETWEEN 0 AND 10), approved_at date NOT NULL, state text NOT NULL CHECK (state IN ('active','suspended','expired')),
  PRIMARY KEY (tenant_id, channel_account_id, template_id),
  FOREIGN KEY (tenant_id, channel_account_id, header) REFERENCES ge.dlt_registration(tenant_id, channel_account_id, header));

CREATE TABLE ge.voice_number (
  tenant_id uuid NOT NULL, channel_account_id uuid NOT NULL, e164 text NOT NULL CHECK (e164 ~ '^\+[1-9][0-9]{7,14}$'),
  series text CHECK (series IN ('140','160','other')), purpose text NOT NULL CHECK (purpose IN ('promotional','service','transactional')),
  CHECK (series IS NULL OR (series = '140') = (purpose = 'promotional')),
  PRIMARY KEY (tenant_id, e164));

CREATE TABLE ge.edge_project (
  project text PRIMARY KEY CHECK (project ~ '^(web|admin|developers)(-(in|eu))?$'), zone text CHECK (zone IN ('IN','EU')),
  function_regions text[] NOT NULL, carries_personal_data boolean NOT NULL,
  CHECK (NOT carries_personal_data OR zone IS NOT NULL),
  CHECK (zone IS NULL OR function_regions = CASE zone WHEN 'IN' THEN ARRAY['bom1'] ELSE ARRAY['fra1'] END));

CREATE TABLE ge.edge_conformance_check (
  check_id bigserial PRIMARY KEY, project text NOT NULL REFERENCES ge.edge_project(project), rule_id text NOT NULL CHECK (rule_id ~ '^VD-[0-9]{2}$'),
  checked_at timestamptz NOT NULL DEFAULT now(), passed boolean NOT NULL, evidence_ref text NOT NULL, finding_id uuid);

CREATE TABLE ge.subprocessor (
  name text PRIMARY KEY, purpose text NOT NULL, zones text[] NOT NULL, dpa_ref text NOT NULL, transfer_mechanism text,
  listed_at date NOT NULL, notice_sent_at date, CHECK (notice_sent_at IS NULL OR listed_at >= notice_sent_at + 30));

CREATE TABLE ge.recovery_path (
  zone text NOT NULL CHECK (zone IN ('IN','EU')), path text NOT NULL CHECK (path IN ('P1_supabase_pitr','P2_walg_standby','P3_logical_dump')),
  retention_days int NOT NULL, location text NOT NULL, secondary_location text, enabled boolean NOT NULL,
  PRIMARY KEY (zone, path), CHECK (path <> 'P2_walg_standby' OR retention_days >= 35));

CREATE TABLE ge.rpo_sample (
  zone text NOT NULL, sampled_at timestamptz NOT NULL, replication_lag_s int, wal_archive_age_s int, last_base_backup_at timestamptz,
  pitr_status text, PRIMARY KEY (zone, sampled_at));

CREATE TABLE ge.restore_drill (
  drill_id uuid PRIMARY KEY DEFAULT gen_random_uuid(), zone text NOT NULL, path text NOT NULL, trigger text NOT NULL CHECK (trigger IN ('release_gate','quarterly','incident')),
  release_ref text, started_at timestamptz NOT NULL, target_time timestamptz NOT NULL, restored_to timestamptz,
  service_restored_at timestamptz, achieved_rpo_s int GENERATED ALWAYS AS ((extract(epoch FROM target_time - restored_to))::int) STORED,
  achieved_rto_min int GENERATED ALWAYS AS ((extract(epoch FROM service_restored_at - started_at)/60)::int) STORED,
  prv_results jsonb NOT NULL DEFAULT '{}', passed boolean, evidence_ref text,
  CHECK (passed IS NULL OR evidence_ref IS NOT NULL));

ALTER TABLE ge.ai_model ADD COLUMN IF NOT EXISTS reg_id text UNIQUE CHECK (reg_id ~ '^REG-[0-9]{3}$');

ALTER TABLE ge.ai_model ADD COLUMN IF NOT EXISTS hosting text NOT NULL DEFAULT 'provider_hosted'
  CHECK (hosting IN ('provider_hosted','cloud_marketplace','self_hosted_in_zone','free_third_party'));

ALTER TABLE ge.ai_model ADD COLUMN IF NOT EXISTS modality text NOT NULL DEFAULT 'text' CHECK (modality IN ('text','embedding','classifier','image','video','voice'));

ALTER TABLE ge.ai_model ADD COLUMN IF NOT EXISTS task_classes text[] NOT NULL DEFAULT '{}';

ALTER TABLE ge.ai_model ADD COLUMN IF NOT EXISTS licence_ref text;

ALTER TABLE ge.ai_model ADD COLUMN IF NOT EXISTS redteam_ref text, ADD COLUMN IF NOT EXISTS recert_due date;

ALTER TABLE ge.ai_model DROP CONSTRAINT IF EXISTS ai_model_t2_data_ck;

ALTER TABLE ge.ai_model ADD CONSTRAINT ai_model_free_tier_data_ck
  CHECK (hosting <> 'free_third_party' OR data_classes <@ ARRAY['Public','Internal-non-personal']::text[]);

ALTER TABLE ge.ai_model ADD CONSTRAINT ai_model_open_weight_data_ck
  CHECK (hosting <> 'self_hosted_in_zone' OR NOT (data_classes && ARRAY['Personal','Restricted']::text[]));

ALTER TABLE ge.ai_model ADD CONSTRAINT ai_model_approved_evidence_ck
  CHECK (status <> 'approved' OR (dpa_ref IS NOT NULL AND no_training AND eval_status = 'passed' AND redteam_ref IS NOT NULL
         AND security_review_ref IS NOT NULL AND cpar_inr IS NOT NULL AND latency_p95_ms IS NOT NULL AND recert_due IS NOT NULL
         AND (hosting <> 'self_hosted_in_zone' OR licence_ref IS NOT NULL)));

CREATE TABLE ge.ai_model_region (
  model_id text NOT NULL REFERENCES ge.ai_model(model_id), zone text NOT NULL CHECK (zone IN ('IN','EU')),
  processing_location text NOT NULL, endpoint_ref text NOT NULL, transfer_basis_ref text,
  PRIMARY KEY (model_id, zone));

CREATE TABLE ge.ai_model_approval (
  model_id text NOT NULL REFERENCES ge.ai_model(model_id), approval_no int NOT NULL, task_class text NOT NULL,
  proposed_by uuid NOT NULL, approver_1 uuid, approver_1_role text CHECK (approver_1_role = 'R10'),
  approver_2 uuid, approver_2_role text CHECK (approver_2_role IN ('R01','R01-delegate')),
  decided_at timestamptz, decision text CHECK (decision IN ('approved','rejected','suspended','retired')), evidence_hash bytea NOT NULL,
  CHECK (approver_1 IS NULL OR approver_1 <> proposed_by), CHECK (approver_2 IS NULL OR (approver_2 <> approver_1 AND approver_2 <> proposed_by)),
  PRIMARY KEY (model_id, approval_no, task_class));

CREATE TABLE ge.ai_model_pin (                  -- per workflow (and optional tenant override within approved rows)
  workflow_id text NOT NULL, task_class text NOT NULL, locale text NOT NULL, zone text NOT NULL,
  model_id text NOT NULL REFERENCES ge.ai_model(model_id), prompt_version text NOT NULL, rollback_to text REFERENCES ge.ai_model(model_id),
  kill_switch boolean NOT NULL DEFAULT false, PRIMARY KEY (workflow_id, task_class, locale, zone));

CREATE TABLE ge.benchmark_enrolment (
  tenant_id uuid NOT NULL REFERENCES ge.tenant(tenant_id), company_id uuid, contract_clause_ref text NOT NULL,
  opted_in_at timestamptz NOT NULL, opted_in_by uuid NOT NULL, withdrawn_at timestamptz, owner_portfolio boolean NOT NULL DEFAULT false,
  r01_opt_in_ref text, PRIMARY KEY (tenant_id, opted_in_at),
  CHECK (NOT owner_portfolio OR r01_opt_in_ref IS NOT NULL));

CREATE TABLE ge.benchmark_contribution (                                    -- written by app_bench via a SECURITY DEFINER function; no tenant_id column
  period date NOT NULL, zone text NOT NULL, cohort text NOT NULL, metric text NOT NULL,
  contributor_hash bytea NOT NULL,                                          -- HMAC(zone pepper, tenant_id || period); not reversible without the pepper
  clipped_value numeric NOT NULL, event_share numeric NOT NULL CHECK (event_share BETWEEN 0 AND 1),
  PRIMARY KEY (period, zone, cohort, metric, contributor_hash));

CREATE TABLE ge.benchmark_cell (
  period date NOT NULL, zone text NOT NULL CHECK (zone IN ('IN','EU','GLOBAL')), cohort text NOT NULL, metric text NOT NULL,
  value_noised numeric, k_band text CHECK (k_band IN ('10-24','25+')), state text NOT NULL CHECK (state IN ('published','suppressed_k','suppressed_dominance','budget_exhausted')),
  epsilon numeric, published_at timestamptz, PRIMARY KEY (period, zone, cohort, metric),
  CHECK (state <> 'published' OR (value_noised IS NOT NULL AND k_band IS NOT NULL AND epsilon IS NOT NULL)));

CREATE TABLE ge.benchmark_privacy_ledger (
  zone text NOT NULL, cohort text NOT NULL, metric text NOT NULL, year int NOT NULL, epsilon_spent numeric NOT NULL DEFAULT 0 CHECK (epsilon_spent <= 6),
  PRIMARY KEY (zone, cohort, metric, year));

CREATE OR REPLACE FUNCTION ge.bench_contribute(p_period date, p_metric text) RETURNS void
  LANGUAGE plpgsql SECURITY DEFINER SET search_path = ge, extensions, public, pg_temp AS $$
BEGIN
  PERFORM ge.require_ctx();
  IF NOT EXISTS (SELECT 1 FROM ge.benchmark_enrolment e WHERE e.tenant_id = ge.ctx_tenant() AND e.withdrawn_at IS NULL) THEN RETURN; END IF;
  INSERT INTO ge.benchmark_contribution (period, zone, cohort, metric, contributor_hash, clipped_value, event_share)
  SELECT p_period, current_setting('app.zone'), ge.bench_cohort(ge.ctx_tenant()), p_metric,
         hmac(ge.ctx_tenant()::text || p_period::text, current_setting('app.bench_pepper'), 'sha256'),
         ge.bench_clip(p_metric, ge.bench_metric(ge.ctx_tenant(), p_metric, p_period)), ge.bench_event_share(ge.ctx_tenant(), p_metric, p_period)
  ON CONFLICT DO NOTHING;
END $$;

REVOKE ALL ON FUNCTION ge.bench_contribute(date, text) FROM PUBLIC;

GRANT EXECUTE ON FUNCTION ge.bench_contribute(date, text) TO app_bench;

DO $$ BEGIN
  IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'app_migrator') THEN CREATE ROLE app_migrator LOGIN NOBYPASSRLS; END IF;
  IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'app_bench') THEN CREATE ROLE app_bench LOGIN NOBYPASSRLS; END IF;
  IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'app_registry') THEN CREATE ROLE app_registry LOGIN NOBYPASSRLS; END IF;
END $$;

GRANT app_owner TO app_migrator;

ALTER ROLE app_rw NOBYPASSRLS;

ALTER ROLE app_worker NOBYPASSRLS;

REVOKE ALL ON SCHEMA ge FROM PUBLIC, anon, authenticated;

ALTER DEFAULT PRIVILEGES FOR ROLE app_owner IN SCHEMA ge REVOKE ALL ON TABLES FROM PUBLIC, anon, authenticated;

CREATE TABLE IF NOT EXISTS ge.platform_table_allowlist (table_name text PRIMARY KEY, reason text NOT NULL);

CREATE VIEW ge.identity_provider AS
  SELECT DISTINCT ON (c.tenant_id) c.tenant_id, c.protocol, c.sso_url, c.issuer, d.domain::text AS domain,
         (d.state = 'verified') AS domain_verified, (SELECT u.email FROM ge.app_user u JOIN ge.breakglass_account b USING (user_id)
          WHERE b.tenant_id = c.tenant_id LIMIT 1) AS breakglass_email, c.enforced,
         p.mfa_mode AS mfa_policy, p.max_session_hours, p.idle_minutes
  FROM ge.idp_connection c LEFT JOIN ge.verified_domain d ON d.tenant_id = c.tenant_id AND d.connection_id = c.connection_id
  JOIN ge.tenant_security_policy p ON p.tenant_id = c.tenant_id
  WHERE c.state = 'active' ORDER BY c.tenant_id, c.enforced DESC, c.created_at DESC;
