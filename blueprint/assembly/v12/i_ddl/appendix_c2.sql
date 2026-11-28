-- Appendix C2 — enterprise tables (proposed). Applied after Appendix C; tested on PostgreSQL 16.
CREATE TABLE identity_provider (tenant_id uuid PRIMARY KEY REFERENCES tenant(tenant_id), protocol text NOT NULL CHECK (protocol IN ('SAML 2.0','OpenID Connect')),
  sso_url text NOT NULL CHECK (sso_url ~ '^https://'), issuer text NOT NULL, domain text NOT NULL, domain_verified boolean NOT NULL DEFAULT false,
  breakglass_email text, enforced boolean NOT NULL DEFAULT false, mfa_policy text NOT NULL, max_session_hours int NOT NULL CHECK (max_session_hours BETWEEN 1 AND 24),
  idle_minutes int NOT NULL CHECK (idle_minutes BETWEEN 5 AND 120),
  CHECK (NOT enforced OR (domain_verified AND breakglass_email IS NOT NULL)));            -- ENT-IDN-02/06
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
CREATE TRIGGER role_permission_sod BEFORE INSERT ON role_permission FOR EACH ROW EXECUTE FUNCTION enforce_sod();   -- ENT-ACC-02
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
  CHECK (approved_by IS NULL OR approved_by <> requested_by));                          -- ENT-DAT-01
CREATE TABLE tenant_key_config (tenant_id uuid PRIMARY KEY REFERENCES tenant(tenant_id), mode text NOT NULL CHECK (mode IN ('platform','customer')),
  kms_key_ref text, rotation_days int NOT NULL CHECK (rotation_days IN (90,180,365)), CHECK (mode = 'platform' OR kms_key_ref IS NOT NULL));
CREATE TABLE sandbox_environment (tenant_id uuid NOT NULL REFERENCES tenant(tenant_id), sandbox_id uuid PRIMARY KEY DEFAULT gen_random_uuid(), name text NOT NULL,
  copies_configuration boolean NOT NULL, contains_personal_data boolean NOT NULL DEFAULT false CHECK (contains_personal_data = false));   -- ENT-DAT-04
CREATE TABLE config_promotion (tenant_id uuid NOT NULL, promotion_id uuid PRIMARY KEY DEFAULT gen_random_uuid(), sandbox_id uuid NOT NULL REFERENCES sandbox_environment(sandbox_id),
  requested_by uuid NOT NULL, approved_by uuid, status text NOT NULL, CHECK (approved_by IS NULL OR approved_by <> requested_by));   -- ENT-DAT-05
CREATE TABLE connector_installation (tenant_id uuid NOT NULL REFERENCES tenant(tenant_id), installation_id uuid PRIMARY KEY DEFAULT gen_random_uuid(), connector_id text NOT NULL,
  environment text NOT NULL CHECK (environment IN ('sandbox','production')), credential_ref text NOT NULL, legal_review_ref text, security_review_ref text, status text NOT NULL,
  CHECK (environment = 'sandbox' OR (legal_review_ref IS NOT NULL AND security_review_ref IS NOT NULL)));   -- ENT-INT-05
CREATE TABLE security_finding (finding_id uuid PRIMARY KEY DEFAULT gen_random_uuid(), title text NOT NULL, severity text NOT NULL CHECK (severity IN ('Critical','High','Medium','Low')),
  found_at date NOT NULL, due_at date NOT NULL, closed_at date, evidence_ref text,
  CHECK (due_at <= found_at + CASE severity WHEN 'Critical' THEN 7 WHEN 'High' THEN 30 WHEN 'Medium' THEN 90 ELSE 180 END),
  CHECK (closed_at IS NULL OR evidence_ref IS NOT NULL));                               -- ENT-SEC-03
CREATE TABLE ops_incident (incident_id uuid PRIMARY KEY DEFAULT gen_random_uuid(), severity text NOT NULL CHECK (severity IN ('SEV1','SEV2','SEV3','SEV4')),
  title text NOT NULL, declared_at timestamptz NOT NULL, status text NOT NULL CHECK (status IN ('Investigating','Identified','Monitoring','Resolved')), status_message text);
CREATE TABLE tax_rule (rule_id text PRIMARY KEY, jurisdiction text NOT NULL, description text NOT NULL, rate_percent numeric(5,2) CHECK (rate_percent BETWEEN 0 AND 30),
  needs_rate_input boolean NOT NULL DEFAULT false, approved_by text, approved_at date);
CREATE TABLE invoice (tenant_id uuid NOT NULL REFERENCES tenant(tenant_id), invoice_id uuid PRIMARY KEY DEFAULT gen_random_uuid(), number text NOT NULL UNIQUE,
  currency char(3) NOT NULL, net_minor bigint NOT NULL CHECK (net_minor >= 0), tax_minor bigint NOT NULL CHECK (tax_minor >= 0), total_minor bigint NOT NULL,
  tax_rule_id text REFERENCES tax_rule(rule_id), status text NOT NULL, CHECK (total_minor = net_minor + tax_minor));
CREATE TABLE locale_bundle (locale text PRIMARY KEY, direction text NOT NULL CHECK (direction IN ('ltr','rtl')), coverage_percent numeric(5,2) NOT NULL, reviewed_by text);

-- Row-level security
ALTER TABLE identity_provider ENABLE ROW LEVEL SECURITY; ALTER TABLE identity_provider FORCE ROW LEVEL SECURITY;
CREATE POLICY identity_provider_tenant ON identity_provider USING (tenant_id = current_setting('app.tenant_id')::uuid) WITH CHECK (tenant_id = current_setting('app.tenant_id')::uuid);
ALTER TABLE scim_token ENABLE ROW LEVEL SECURITY; ALTER TABLE scim_token FORCE ROW LEVEL SECURITY;
CREATE POLICY scim_token_tenant ON scim_token USING (tenant_id = current_setting('app.tenant_id')::uuid) WITH CHECK (tenant_id = current_setting('app.tenant_id')::uuid);
ALTER TABLE custom_role ENABLE ROW LEVEL SECURITY; ALTER TABLE custom_role FORCE ROW LEVEL SECURITY;
CREATE POLICY custom_role_tenant ON custom_role USING (tenant_id = current_setting('app.tenant_id')::uuid) WITH CHECK (tenant_id = current_setting('app.tenant_id')::uuid);
ALTER TABLE role_permission ENABLE ROW LEVEL SECURITY; ALTER TABLE role_permission FORCE ROW LEVEL SECURITY;
CREATE POLICY role_permission_tenant ON role_permission USING (tenant_id = current_setting('app.tenant_id')::uuid) WITH CHECK (tenant_id = current_setting('app.tenant_id')::uuid);
ALTER TABLE api_key ENABLE ROW LEVEL SECURITY; ALTER TABLE api_key FORCE ROW LEVEL SECURITY;
CREATE POLICY api_key_tenant ON api_key USING (tenant_id = current_setting('app.tenant_id')::uuid) WITH CHECK (tenant_id = current_setting('app.tenant_id')::uuid);
ALTER TABLE webhook_endpoint ENABLE ROW LEVEL SECURITY; ALTER TABLE webhook_endpoint FORCE ROW LEVEL SECURITY;
CREATE POLICY webhook_endpoint_tenant ON webhook_endpoint USING (tenant_id = current_setting('app.tenant_id')::uuid) WITH CHECK (tenant_id = current_setting('app.tenant_id')::uuid);
ALTER TABLE webhook_delivery ENABLE ROW LEVEL SECURITY; ALTER TABLE webhook_delivery FORCE ROW LEVEL SECURITY;
CREATE POLICY webhook_delivery_tenant ON webhook_delivery USING (tenant_id = current_setting('app.tenant_id')::uuid) WITH CHECK (tenant_id = current_setting('app.tenant_id')::uuid);
ALTER TABLE audit_sink ENABLE ROW LEVEL SECURITY; ALTER TABLE audit_sink FORCE ROW LEVEL SECURITY;
CREATE POLICY audit_sink_tenant ON audit_sink USING (tenant_id = current_setting('app.tenant_id')::uuid) WITH CHECK (tenant_id = current_setting('app.tenant_id')::uuid);
ALTER TABLE export_job ENABLE ROW LEVEL SECURITY; ALTER TABLE export_job FORCE ROW LEVEL SECURITY;
CREATE POLICY export_job_tenant ON export_job USING (tenant_id = current_setting('app.tenant_id')::uuid) WITH CHECK (tenant_id = current_setting('app.tenant_id')::uuid);
ALTER TABLE tenant_key_config ENABLE ROW LEVEL SECURITY; ALTER TABLE tenant_key_config FORCE ROW LEVEL SECURITY;
CREATE POLICY tenant_key_config_tenant ON tenant_key_config USING (tenant_id = current_setting('app.tenant_id')::uuid) WITH CHECK (tenant_id = current_setting('app.tenant_id')::uuid);
ALTER TABLE sandbox_environment ENABLE ROW LEVEL SECURITY; ALTER TABLE sandbox_environment FORCE ROW LEVEL SECURITY;
CREATE POLICY sandbox_environment_tenant ON sandbox_environment USING (tenant_id = current_setting('app.tenant_id')::uuid) WITH CHECK (tenant_id = current_setting('app.tenant_id')::uuid);
ALTER TABLE config_promotion ENABLE ROW LEVEL SECURITY; ALTER TABLE config_promotion FORCE ROW LEVEL SECURITY;
CREATE POLICY config_promotion_tenant ON config_promotion USING (tenant_id = current_setting('app.tenant_id')::uuid) WITH CHECK (tenant_id = current_setting('app.tenant_id')::uuid);
ALTER TABLE connector_installation ENABLE ROW LEVEL SECURITY; ALTER TABLE connector_installation FORCE ROW LEVEL SECURITY;
CREATE POLICY connector_installation_tenant ON connector_installation USING (tenant_id = current_setting('app.tenant_id')::uuid) WITH CHECK (tenant_id = current_setting('app.tenant_id')::uuid);
ALTER TABLE invoice ENABLE ROW LEVEL SECURITY; ALTER TABLE invoice FORCE ROW LEVEL SECURITY;
CREATE POLICY invoice_tenant ON invoice USING (tenant_id = current_setting('app.tenant_id')::uuid) WITH CHECK (tenant_id = current_setting('app.tenant_id')::uuid);