-- V0007__typed_tables_blueprint_and_v12b
SET search_path = ge, extensions, public;

SELECT set_config('app.zone', coalesce(nullif(current_setting('app.deployment_region', true), ''), 'IN'), false);

SELECT set_config('app.deployment_region', coalesce(nullif(current_setting('app.deployment_region', true), ''), 'IN'), false);

CREATE TABLE ge.ten_capability_profile (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  version_no integer NOT NULL DEFAULT 1,
  status text NOT NULL DEFAULT 'draft',
  content_hash char(64),
  approval_id uuid,
  approved_at timestamptz,
  effective_from timestamptz,
  effective_to timestamptz,
  supersedes_id uuid,
  capabilities jsonb,
  granted_by_approval_id uuid,
  CONSTRAINT pk_ten_capability_profile PRIMARY KEY (id),
  CONSTRAINT uq_ten_capability_profile__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_ten_capability_profile__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.ten_capability_profile IS 'ENT-004 CapabilityProfile · scope S · Imm. V · Part 3.3 §3.3.3.2 + §3.3.7';

CREATE TABLE ge.ten_domain (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  hostname text,
  is_platform_subdomain boolean,
  verification_state text,
  verification_token_hash char(64),
  verified_at timestamptz,
  tls_state text,
  CONSTRAINT pk_ten_domain PRIMARY KEY (id),
  CONSTRAINT uq_ten_domain__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_ten_domain__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.ten_domain IS 'ENT-005 Domain (verified web domain) · scope S · Imm. M · Part 3.3 §3.3.3.2 + §3.3.7';

CREATE TABLE ge.ten_user (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  updated_at timestamptz NOT NULL DEFAULT now(),
  idp_subject text,
  user_kind text,
  display_name text,
  email_enc bytea,
  email_hmac char(64),
  locale text,
  timezone text,
  status text,
  last_seen_at timestamptz,
  CONSTRAINT pk_ten_user PRIMARY KEY (id)
);

COMMENT ON TABLE ge.ten_user IS 'ENT-006 User (product-local identity mirror) · scope P · Imm. M · Part 3.3 §3.3.3.2 + §3.3.7';

CREATE TABLE ge.ten_membership (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  user_id uuid NOT NULL,
  status text NOT NULL DEFAULT 'invited',
  invited_by uuid,
  invite_token_hash char(64),
  activated_at timestamptz,
  expires_at timestamptz,
  mfa_required boolean NOT NULL,
  last_access_review_at timestamptz,
  approval_limits jsonb NOT NULL DEFAULT '{}'::jsonb,
  CONSTRAINT pk_ten_membership PRIMARY KEY (id),
  CONSTRAINT uq_ten_membership__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_ten_membership__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.ten_membership IS 'ENT-008 Membership · scope T · Imm. M · Part 3.3 §3.3.3.2';

CREATE TABLE ge.ten_portal_grant (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  subject_user_id uuid,
  object_type text,
  object_id uuid,
  actions text,
  expires_at timestamptz,
  revoked_at timestamptz,
  granted_by text,
  CONSTRAINT pk_ten_portal_grant PRIMARY KEY (id),
  CONSTRAINT uq_ten_portal_grant__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_ten_portal_grant__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.ten_portal_grant IS 'ENT-009 PortalGrant (object grant for external users) · scope S · Imm. M · Part 3.3 §3.3.3.2 + §3.3.7';

CREATE TABLE ge.ten_saved_view (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  user_id uuid,
  screen_code text,
  name text,
  filter_spec jsonb,
  is_shared_team boolean,
  CONSTRAINT pk_ten_saved_view PRIMARY KEY (id),
  CONSTRAINT uq_ten_saved_view__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_ten_saved_view__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.ten_saved_view IS 'ENT-010 SavedView · scope S · Imm. M · Part 3.3 §3.3.3.2 + §3.3.7';

CREATE TABLE ge.ref_dataset (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid,
  startup_id uuid,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  version_no integer NOT NULL DEFAULT 1,
  status text NOT NULL DEFAULT 'draft',
  content_hash char(64),
  approval_id uuid,
  approved_at timestamptz,
  effective_from timestamptz,
  effective_to timestamptz,
  supersedes_id uuid,
  code text,
  owner_role text,
  is_extensible_by_tenant boolean,
  CONSTRAINT pk_ref_dataset PRIMARY KEY (id),
  CONSTRAINT uq_ref_dataset__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_ref_dataset__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.ref_dataset IS 'ENT-011 ReferenceDataset · scope X · Imm. V · Part 3.3 §3.3.3.2 + §3.3.7';

CREATE TABLE ge.ref_value (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid,
  startup_id uuid,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  version_no integer NOT NULL DEFAULT 1,
  status text NOT NULL DEFAULT 'draft',
  content_hash char(64),
  approval_id uuid,
  approved_at timestamptz,
  effective_from timestamptz,
  effective_to timestamptz,
  supersedes_id uuid,
  dataset_id uuid,
  code text,
  label text,
  parent_id uuid,
  attributes jsonb,
  valid_from timestamptz,
  valid_to timestamptz,
  sort_order integer,
  CONSTRAINT pk_ref_value PRIMARY KEY (id),
  CONSTRAINT uq_ref_value__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_ref_value__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.ref_value IS 'ENT-012 ReferenceValue · scope X · Imm. V · Part 3.3 §3.3.3.2 + §3.3.7';

CREATE TABLE ge.ref_currency (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  updated_at timestamptz NOT NULL DEFAULT now(),
  code text,
  name text,
  minor_units smallint,
  is_active boolean,
  CONSTRAINT pk_ref_currency PRIMARY KEY (id)
);

COMMENT ON TABLE ge.ref_currency IS 'ENT-013 Currency · scope P · Imm. M · Part 3.3 §3.3.3.2 + §3.3.7';

CREATE TABLE ge.ref_country (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  updated_at timestamptz NOT NULL DEFAULT now(),
  code text,
  name text,
  iso3 text,
  jurisdiction_pack text,
  subdivisions text,
  CONSTRAINT pk_ref_country PRIMARY KEY (id)
);

COMMENT ON TABLE ge.ref_country IS 'ENT-014 Country (with subdivisions) · scope P · Imm. M · Part 3.3 §3.3.3.2 + §3.3.7';

CREATE TABLE ge.ref_unit (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid,
  startup_id uuid,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  code text,
  dimension text,
  base_code text,
  to_base_factor text,
  CONSTRAINT pk_ref_unit PRIMARY KEY (id),
  CONSTRAINT uq_ref_unit__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_ref_unit__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.ref_unit IS 'ENT-015 UnitOfMeasure · scope X · Imm. M · Part 3.3 §3.3.3.2 + §3.3.7';

CREATE TABLE ge.cat_offering_version (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  version_no integer NOT NULL DEFAULT 1,
  status text NOT NULL DEFAULT 'draft',
  content_hash char(64),
  approval_id uuid,
  approved_at timestamptz,
  effective_from timestamptz,
  effective_to timestamptz,
  supersedes_id uuid,
  offering_id uuid NOT NULL,
  summary text NOT NULL,
  specification jsonb NOT NULL DEFAULT '{}'::jsonb,
  hsn_sac_code text,
  allowed_units text[] NOT NULL DEFAULT '{}',
  min_order_qty numeric(18,4),
  max_order_qty numeric(18,4),
  delivery_geographies text[] NOT NULL DEFAULT '{}',
  excluded_data_classes text[] NOT NULL DEFAULT '{}',
  CONSTRAINT pk_cat_offering_version PRIMARY KEY (id),
  CONSTRAINT uq_cat_offering_version__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_cat_offering_version__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.cat_offering_version IS 'ENT-017 OfferingVersion · scope S · Imm. V · Part 3.3 §3.3.3.2';

CREATE TABLE ge.cat_capability (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  code text,
  name text,
  taxonomy_ref text,
  description text,
  CONSTRAINT pk_cat_capability PRIMARY KEY (id),
  CONSTRAINT uq_cat_capability__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_cat_capability__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.cat_capability IS 'ENT-018 Capability · scope S · Imm. M · Part 3.3 §3.3.3.2 + §3.3.7';

CREATE TABLE ge.cat_offering_capability (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  version_no integer NOT NULL DEFAULT 1,
  status text NOT NULL DEFAULT 'draft',
  content_hash char(64),
  approval_id uuid,
  approved_at timestamptz,
  effective_from timestamptz,
  effective_to timestamptz,
  supersedes_id uuid,
  offering_version_id uuid,
  capability_id uuid,
  fit_level text,
  evidence_document_id uuid,
  CONSTRAINT pk_cat_offering_capability PRIMARY KEY (id),
  CONSTRAINT uq_cat_offering_capability__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_cat_offering_capability__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.cat_offering_capability IS 'ENT-019 ProductCapability (offering version × capability) · scope S · Imm. V · Part 3.3 §3.3.3.2 + §3.3.7';

CREATE TABLE ge.cat_claim (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  version_no integer NOT NULL DEFAULT 1,
  status text NOT NULL DEFAULT 'draft',
  content_hash char(64),
  approval_id uuid,
  approved_at timestamptz,
  effective_from timestamptz,
  effective_to timestamptz,
  supersedes_id uuid,
  offering_version_id uuid,
  claim_text text NOT NULL,
  claim_type text NOT NULL,
  is_management_claim boolean NOT NULL DEFAULT false,
  evidence_count integer NOT NULL DEFAULT 0,
  subject_consent_ref uuid,
  expires_at timestamptz NOT NULL,
  author_id uuid NOT NULL,
  schema_ref text,
  evidence_refs uuid[] NOT NULL DEFAULT '{}',
  payload jsonb NOT NULL,
  CONSTRAINT pk_cat_claim PRIMARY KEY (id),
  CONSTRAINT uq_cat_claim__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_cat_claim__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.cat_claim IS 'ENT-020 Claim · scope S · Imm. V · Part 3.3 §3.3.3.2';

CREATE TABLE ge.cat_price_version (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  version_no integer NOT NULL DEFAULT 1,
  status text NOT NULL DEFAULT 'draft',
  content_hash char(64),
  approval_id uuid,
  approved_at timestamptz,
  effective_from timestamptz,
  effective_to timestamptz,
  supersedes_id uuid,
  offering_version_id uuid NOT NULL,
  price_list_code text NOT NULL DEFAULT 'standard',
  currency char(3) NOT NULL,
  unit_code text NOT NULL,
  unit_price numeric(18,4) NOT NULL,
  unit_cost numeric(18,4),
  tax_rate_pct numeric(7,4) NOT NULL DEFAULT 0,
  tax_inclusive boolean NOT NULL DEFAULT false,
  valid_from date NOT NULL,
  valid_to date NOT NULL,
  CONSTRAINT pk_cat_price_version PRIMARY KEY (id),
  CONSTRAINT uq_cat_price_version__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_cat_price_version__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.cat_price_version IS 'ENT-021 PriceVersion · scope S · Imm. V · Part 3.3 §3.3.3.2';

CREATE TABLE ge.cat_launch_approval (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  correlation_id uuid,
  offering_id uuid,
  from_readiness text,
  to_readiness text,
  approval_id uuid,
  checklist_results jsonb,
  CONSTRAINT pk_cat_launch_approval PRIMARY KEY (id),
  CONSTRAINT uq_cat_launch_approval__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_cat_launch_approval__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.cat_launch_approval IS 'ENT-023 LaunchApproval · scope S · Imm. A · Part 3.3 §3.3.3.2 + §3.3.7';

CREATE TABLE ge.cat_document (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  version_no integer NOT NULL DEFAULT 1,
  status text NOT NULL DEFAULT 'draft',
  content_hash char(64),
  approval_id uuid,
  approved_at timestamptz,
  effective_from timestamptz,
  effective_to timestamptz,
  supersedes_id uuid,
  title text NOT NULL,
  doc_kind text NOT NULL,
  classification text NOT NULL DEFAULT 'internal',
  storage_key text NOT NULL,
  mime_type text NOT NULL,
  size_bytes bigint NOT NULL,
  sha256 char(64) NOT NULL,
  scan_result text NOT NULL DEFAULT 'pending',
  language text NOT NULL DEFAULT 'en',
  chunk_count integer NOT NULL DEFAULT 0,
  embedding_model_id text,
  schema_ref text,
  evidence_refs uuid[] NOT NULL DEFAULT '{}',
  payload jsonb NOT NULL,
  CONSTRAINT pk_cat_document PRIMARY KEY (id),
  CONSTRAINT uq_cat_document__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_cat_document__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.cat_document IS 'ENT-024 Document · scope S · Imm. V · Part 3.3 §3.3.3.2';

CREATE TABLE ge.cat_chunk (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  correlation_id uuid,
  document_id uuid NOT NULL,
  ordinal integer NOT NULL,
  body text NOT NULL,
  token_count integer NOT NULL,
  heading_path text,
  classification text NOT NULL,
  tsv tsvector NOT NULL,
  is_searchable boolean NOT NULL DEFAULT false,
  schema_ref text,
  evidence_refs uuid[] NOT NULL DEFAULT '{}',
  payload jsonb NOT NULL,
  CONSTRAINT pk_cat_chunk PRIMARY KEY (id),
  CONSTRAINT uq_cat_chunk__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_cat_chunk__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.cat_chunk IS 'ENT-025 Chunk · scope S · Imm. A · Part 3.3 §3.3.3.2';

CREATE TABLE ge.cat_embedding (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  correlation_id uuid,
  chunk_id uuid NOT NULL,
  model_id text NOT NULL,
  classification text NOT NULL,
  offering_version_ids uuid[] NOT NULL DEFAULT '{}',
  schema_ref text,
  evidence_refs uuid[] NOT NULL DEFAULT '{}',
  payload jsonb NOT NULL,
  CONSTRAINT pk_cat_embedding PRIMARY KEY (id),
  CONSTRAINT uq_cat_embedding__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_cat_embedding__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.cat_embedding IS 'ENT-026 Embedding · scope S · Imm. A · Part 3.3 §3.3.3.2';

CREATE TABLE ge.gov_policy_version (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid,
  startup_id uuid,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  version_no integer NOT NULL DEFAULT 1,
  status text NOT NULL DEFAULT 'draft',
  content_hash char(64),
  approval_id uuid,
  approved_at timestamptz,
  effective_from timestamptz,
  effective_to timestamptz,
  supersedes_id uuid,
  policy_type text NOT NULL,
  policy_code text NOT NULL,
  body jsonb NOT NULL,
  tightens_only boolean NOT NULL,
  simulation_report_ref uuid,
  CONSTRAINT pk_gov_policy_version PRIMARY KEY (id),
  CONSTRAINT uq_gov_policy_version__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_gov_policy_version__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.gov_policy_version IS 'ENT-029 PolicyVersion · scope X · Imm. V · Part 3.3 §3.3.3.2';

CREATE TABLE ge.gov_eligibility_decision (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  correlation_id uuid,
  is_simulated boolean NOT NULL DEFAULT false,
  run_id uuid,
  contact_id uuid,
  organization_id uuid,
  action_type text NOT NULL,
  evaluation_point text NOT NULL,
  result text NOT NULL,
  reason_codes text[] NOT NULL DEFAULT '{}',
  policy_version_ids uuid[] NOT NULL,
  jurisdiction_rule_id uuid,
  inputs_digest char(64) NOT NULL,
  object_type text NOT NULL,
  object_id text NOT NULL,
  CONSTRAINT pk_gov_eligibility_decision PRIMARY KEY (id),
  CONSTRAINT uq_gov_eligibility_decision__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_gov_eligibility_decision__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.gov_eligibility_decision IS 'ENT-031 EligibilityDecision · scope S · Imm. A · Part 3.3 §3.3.3.2';

CREATE TABLE ge.gov_policy_decision (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  correlation_id uuid,
  is_simulated boolean NOT NULL DEFAULT false,
  run_id uuid,
  object_type text,
  object_id uuid,
  action text,
  decision text,
  rule_ids text,
  inputs_digest text,
  approval_hash_checked text,
  budget_reservation_id uuid,
  CONSTRAINT pk_gov_policy_decision PRIMARY KEY (id),
  CONSTRAINT uq_gov_policy_decision__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_gov_policy_decision__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.gov_policy_decision IS 'ENT-032 PolicyDecision · scope S · Imm. A · Part 3.3 §3.3.3.2 + §3.3.7';

CREATE TABLE ge.gov_approval_policy (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  version_no integer NOT NULL DEFAULT 1,
  status text NOT NULL DEFAULT 'draft',
  content_hash char(64),
  approval_id uuid,
  approved_at timestamptz,
  effective_from timestamptz,
  effective_to timestamptz,
  supersedes_id uuid,
  policy_kind text,
  thresholds jsonb,
  approver_roles text,
  CONSTRAINT pk_gov_approval_policy PRIMARY KEY (id),
  CONSTRAINT uq_gov_approval_policy__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_gov_approval_policy__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.gov_approval_policy IS 'ENT-033 ApprovalPolicy · scope T · Imm. V · Part 3.3 §3.3.3.2 + §3.3.7';

CREATE TABLE ge.gov_approval (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  correlation_id uuid,
  object_type text NOT NULL,
  object_id uuid NOT NULL,
  object_revision integer NOT NULL,
  approved_hash char(64) NOT NULL,
  decision text NOT NULL,
  approver_id uuid NOT NULL,
  approver_role text NOT NULL,
  delegation_id uuid,
  policy_rule_ref text NOT NULL,
  mfa_at timestamptz NOT NULL,
  reason_code text,
  reason_text text,
  expires_at timestamptz,
  revokes_id uuid,
  schema_ref text,
  evidence_refs uuid[] NOT NULL DEFAULT '{}',
  payload jsonb NOT NULL,
  CONSTRAINT pk_gov_approval PRIMARY KEY (id),
  CONSTRAINT uq_gov_approval__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_gov_approval__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.gov_approval IS 'ENT-034 Approval · scope S · Imm. A · Part 3.3 §3.3.3.2';

CREATE TABLE ge.gov_approval_delegation (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  is_simulated boolean NOT NULL DEFAULT false,
  run_id uuid,
  correlation_id uuid,
  delegator_id uuid,
  delegate_id uuid,
  role_code text,
  valid_from timestamptz,
  valid_to timestamptz,
  revoked_at timestamptz,
  CONSTRAINT pk_gov_approval_delegation PRIMARY KEY (id),
  CONSTRAINT uq_gov_approval_delegation__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_gov_approval_delegation__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.gov_approval_delegation IS 'ENT-035 ApprovalDelegation · scope S · Imm. F · Part 3.3 §3.3.3.2 + §3.3.7';

CREATE TABLE ge.gov_retention_policy (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid,
  startup_id uuid,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  version_no integer NOT NULL DEFAULT 1,
  status text NOT NULL DEFAULT 'draft',
  content_hash char(64),
  approval_id uuid,
  approved_at timestamptz,
  effective_from timestamptz,
  effective_to timestamptz,
  supersedes_id uuid,
  data_class text,
  retention_period text,
  clock_start text,
  action text,
  CONSTRAINT pk_gov_retention_policy PRIMARY KEY (id),
  CONSTRAINT uq_gov_retention_policy__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_gov_retention_policy__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.gov_retention_policy IS 'ENT-037 RetentionPolicy · scope X · Imm. V · Part 3.3 §3.3.3.2 + §3.3.7';

CREATE TABLE ge.gov_legal_hold (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  hold_scope text,
  target_ref text,
  matter_ref text,
  placed_by text,
  released_by text,
  state text,
  reason text,
  CONSTRAINT pk_gov_legal_hold PRIMARY KEY (id),
  CONSTRAINT uq_gov_legal_hold__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_gov_legal_hold__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.gov_legal_hold IS 'ENT-038 LegalHold · scope T · Imm. F · Part 3.3 §3.3.3.2 + §3.3.7';

CREATE TABLE ge.int_credential_ref (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  integration_id uuid,
  secret_arn text,
  rotates_at timestamptz,
  last_rotated_at timestamptz,
  CONSTRAINT pk_int_credential_ref PRIMARY KEY (id),
  CONSTRAINT uq_int_credential_ref__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_int_credential_ref__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.int_credential_ref IS 'ENT-041 CredentialRef · scope S · Imm. M · Part 3.3 §3.3.3.2 + §3.3.7';

CREATE TABLE ge.int_quota (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  integration_id uuid,
  unit text,
  limit_value text,
  period text,
  consumed text,
  resets_at timestamptz,
  CONSTRAINT pk_int_quota PRIMARY KEY (id),
  CONSTRAINT uq_int_quota__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_int_quota__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.int_quota IS 'ENT-042 Quota · scope S · Imm. M · Part 3.3 §3.3.3.2 + §3.3.7';

CREATE TABLE ge.int_provider_event (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  correlation_id uuid,
  integration_id uuid,
  provider_account text,
  provider_event_id uuid,
  event_type text,
  signature_valid boolean,
  payload_min jsonb,
  processing_state text,
  received_at timestamptz,
  CONSTRAINT pk_int_provider_event PRIMARY KEY (id),
  CONSTRAINT uq_int_provider_event__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_int_provider_event__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.int_provider_event IS 'ENT-043 ProviderEvent (verified webhook receipt) · scope S · Imm. A · Part 3.3 §3.3.3.2 + §3.3.7';

CREATE TABLE ge.ai_agent_definition (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid,
  startup_id uuid,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  version_no integer NOT NULL DEFAULT 1,
  status text NOT NULL DEFAULT 'draft',
  content_hash char(64),
  approval_id uuid,
  approved_at timestamptz,
  effective_from timestamptz,
  effective_to timestamptz,
  supersedes_id uuid,
  agent_code text,
  max_autonomy text,
  tool_scopes jsonb,
  allowed_tiers text,
  budget_id uuid,
  kpi_refs text,
  CONSTRAINT pk_ai_agent_definition PRIMARY KEY (id),
  CONSTRAINT uq_ai_agent_definition__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_ai_agent_definition__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.ai_agent_definition IS 'ENT-044 AgentDefinition (tool registry entry) · scope X · Imm. V · Part 3.3 §3.3.3.2 + §3.3.7';

CREATE TABLE ge.ai_model_run (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  correlation_id uuid,
  is_simulated boolean NOT NULL DEFAULT false,
  run_id uuid,
  agent_id uuid NOT NULL,
  purpose text NOT NULL,
  prompt_version_id uuid,
  tier text NOT NULL,
  provider text,
  model_id text,
  data_classification_max text NOT NULL,
  contains_personal_data boolean NOT NULL,
  input_digest char(64) NOT NULL,
  output_digest char(64) NOT NULL,
  payload_storage_key text,
  input_tokens integer NOT NULL DEFAULT 0,
  output_tokens integer NOT NULL DEFAULT 0,
  cached_tokens integer NOT NULL DEFAULT 0,
  latency_ms integer,
  schema_valid boolean,
  repair_attempts smallint NOT NULL DEFAULT 0,
  citations uuid[] NOT NULL DEFAULT '{}',
  guardrail_results jsonb NOT NULL DEFAULT '{}'::jsonb,
  outcome text NOT NULL,
  cost_reserved numeric(18,4) NOT NULL DEFAULT 0,
  cost_actual numeric(18,4) NOT NULL DEFAULT 0,
  currency char(3) NOT NULL DEFAULT 'INR',
  budget_id uuid NOT NULL,
  CONSTRAINT pk_ai_model_run PRIMARY KEY (id),
  CONSTRAINT uq_ai_model_run__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_ai_model_run__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.ai_model_run IS 'ENT-046 ModelRun · scope S · Imm. A · Part 3.3 §3.3.3.2';

CREATE TABLE ge.ai_eval_case (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid,
  startup_id uuid,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  version_no integer NOT NULL DEFAULT 1,
  status text NOT NULL DEFAULT 'draft',
  content_hash char(64),
  approval_id uuid,
  approved_at timestamptz,
  effective_from timestamptz,
  effective_to timestamptz,
  supersedes_id uuid,
  suite_code text,
  vertical text,
  input_fixture jsonb,
  expected jsonb,
  label_source text,
  is_benchmark boolean,
  CONSTRAINT pk_ai_eval_case PRIMARY KEY (id),
  CONSTRAINT uq_ai_eval_case__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_ai_eval_case__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.ai_eval_case IS 'ENT-047 EvalCase · scope X · Imm. V · Part 3.3 §3.3.3.2 + §3.3.7';

CREATE TABLE ge.ai_feedback (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  correlation_id uuid,
  model_run_id uuid,
  reviewer_id uuid,
  verdict text,
  reason_code text,
  edit_distance text,
  schema_ref text,
  evidence_refs uuid[] NOT NULL DEFAULT '{}',
  payload jsonb NOT NULL,
  CONSTRAINT pk_ai_feedback PRIMARY KEY (id),
  CONSTRAINT uq_ai_feedback__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_ai_feedback__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.ai_feedback IS 'ENT-049 AiFeedback (human feedback on AI output) · scope S · Imm. A · Part 3.3 §3.3.3.2 + §3.3.7';

CREATE TABLE ge.ai_cost_ledger (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  correlation_id uuid,
  budget_id uuid NOT NULL,
  entry_type text NOT NULL,
  amount numeric(18,4) NOT NULL,
  currency char(3) NOT NULL,
  source_type text NOT NULL,
  source_id text NOT NULL,
  reservation_id uuid,
  budget_period date NOT NULL,
  reason text,
  CONSTRAINT pk_ai_cost_ledger PRIMARY KEY (id),
  CONSTRAINT uq_ai_cost_ledger__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_ai_cost_ledger__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.ai_cost_ledger IS 'ENT-051 CostLedger · scope S · Imm. A · Part 3.3 §3.3.3.2';

CREATE TABLE ge.intel_source (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  is_simulated boolean NOT NULL DEFAULT false,
  run_id uuid,
  correlation_id uuid,
  host text NOT NULL,
  path_prefix text NOT NULL DEFAULT '/',
  source_kind text NOT NULL,
  purpose text NOT NULL,
  state text NOT NULL DEFAULT 'proposed',
  active_policy_id uuid,
  country_codes char(2)[] NOT NULL DEFAULT '{}',
  freshness_sla_days integer NOT NULL DEFAULT 90,
  robots_respected boolean NOT NULL DEFAULT true,
  schema_ref text,
  evidence_refs uuid[] NOT NULL DEFAULT '{}',
  payload jsonb NOT NULL,
  CONSTRAINT pk_intel_source PRIMARY KEY (id),
  CONSTRAINT uq_intel_source__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_intel_source__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.intel_source IS 'ENT-053 Source · scope S · Imm. M · Part 3.3 §3.3.3.2';

CREATE TABLE ge.intel_source_policy (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  version_no integer NOT NULL DEFAULT 1,
  status text NOT NULL DEFAULT 'draft',
  content_hash char(64),
  approval_id uuid,
  approved_at timestamptz,
  effective_from timestamptz,
  effective_to timestamptz,
  supersedes_id uuid,
  is_simulated boolean NOT NULL DEFAULT false,
  run_id uuid,
  correlation_id uuid,
  source_id uuid,
  licence_ref text,
  terms_reviewed_by text,
  purpose text,
  allowed_fields text,
  rate_limit text,
  expires_at timestamptz,
  schema_ref text,
  evidence_refs uuid[] NOT NULL DEFAULT '{}',
  payload jsonb NOT NULL,
  CONSTRAINT pk_intel_source_policy PRIMARY KEY (id),
  CONSTRAINT uq_intel_source_policy__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_intel_source_policy__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.intel_source_policy IS 'ENT-054 SourcePolicy · scope S · Imm. V · Part 3.3 §3.3.3.2 + §3.3.7';

CREATE TABLE ge.intel_search_plan (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  version_no integer NOT NULL DEFAULT 1,
  status text NOT NULL DEFAULT 'draft',
  content_hash char(64),
  approval_id uuid,
  approved_at timestamptz,
  effective_from timestamptz,
  effective_to timestamptz,
  supersedes_id uuid,
  is_simulated boolean NOT NULL DEFAULT false,
  run_id uuid,
  correlation_id uuid,
  objective text,
  query_spec jsonb,
  source_ids uuid,
  schedule_cron text,
  budget_cap numeric(18,2),
  schema_ref text,
  evidence_refs uuid[] NOT NULL DEFAULT '{}',
  payload jsonb NOT NULL,
  CONSTRAINT pk_intel_search_plan PRIMARY KEY (id),
  CONSTRAINT uq_intel_search_plan__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_intel_search_plan__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.intel_search_plan IS 'ENT-055 SearchPlan · scope S · Imm. V · Part 3.3 §3.3.3.2 + §3.3.7';

CREATE TABLE ge.intel_query_run (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  correlation_id uuid,
  is_simulated boolean NOT NULL DEFAULT false,
  run_id uuid,
  search_plan_id uuid,
  status text,
  results_count integer,
  cost_reserved numeric(18,2),
  cost_actual numeric(18,2),
  stopped_reason text,
  CONSTRAINT pk_intel_query_run PRIMARY KEY (id),
  CONSTRAINT uq_intel_query_run__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_intel_query_run__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.intel_query_run IS 'ENT-056 QueryRun · scope S · Imm. A · Part 3.3 §3.3.3.2 + §3.3.7';

CREATE TABLE ge.intel_source_record (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  is_simulated boolean NOT NULL DEFAULT false,
  run_id uuid,
  correlation_id uuid,
  source_id uuid,
  canonical_url text,
  url_hash char(64),
  title text,
  published_at timestamptz,
  metadata jsonb,
  blocked_reason text,
  schema_ref text,
  evidence_refs uuid[] NOT NULL DEFAULT '{}',
  payload jsonb NOT NULL,
  CONSTRAINT pk_intel_source_record PRIMARY KEY (id),
  CONSTRAINT uq_intel_source_record__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_intel_source_record__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.intel_source_record IS 'ENT-057 SourceRecord · scope S · Imm. M · Part 3.3 §3.3.3.2 + §3.3.7';

CREATE TABLE ge.intel_fetch_log (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  correlation_id uuid,
  source_record_id uuid,
  http_status text,
  bytes text,
  robots_allowed text,
  outcome text,
  duration_ms integer,
  CONSTRAINT pk_intel_fetch_log PRIMARY KEY (id),
  CONSTRAINT uq_intel_fetch_log__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_intel_fetch_log__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.intel_fetch_log IS 'ENT-058 FetchLog · scope S · Imm. A · Part 3.3 §3.3.3.2 + §3.3.7';

CREATE TABLE ge.intel_evidence (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  is_simulated boolean NOT NULL DEFAULT false,
  run_id uuid,
  correlation_id uuid,
  source_record_id uuid,
  social_post_id uuid,
  organization_id uuid,
  source_policy_version integer NOT NULL,
  url text NOT NULL,
  retrieved_at timestamptz NOT NULL,
  published_at timestamptz,
  content_hash char(64) NOT NULL,
  extracted jsonb NOT NULL,
  content_text text,
  content_storage_key text,
  confidence numeric(5,4) NOT NULL,
  freshness_state text NOT NULL DEFAULT 'fresh',
  injection_flag boolean NOT NULL DEFAULT false,
  rights_state text NOT NULL DEFAULT 'permitted',
  model_run_id uuid,
  schema_ref text,
  evidence_refs uuid[] NOT NULL DEFAULT '{}',
  payload jsonb NOT NULL,
  CONSTRAINT pk_intel_evidence PRIMARY KEY (id),
  CONSTRAINT uq_intel_evidence__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_intel_evidence__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.intel_evidence IS 'ENT-059 Evidence · scope S · Imm. F · Part 3.3 §3.3.3.2';

CREATE TABLE ge.intel_social_post (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  is_simulated boolean NOT NULL DEFAULT false,
  run_id uuid,
  correlation_id uuid,
  platform text,
  post_ref text,
  author_org_id uuid,
  posted_at timestamptz,
  text_excerpt text,
  licence_basis text,
  schema_ref text,
  evidence_refs uuid[] NOT NULL DEFAULT '{}',
  payload jsonb NOT NULL,
  CONSTRAINT pk_intel_social_post PRIMARY KEY (id),
  CONSTRAINT uq_intel_social_post__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_intel_social_post__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.intel_social_post IS 'ENT-060 SocialPost · scope S · Imm. M · Part 3.3 §3.3.3.2 + §3.3.7';

CREATE TABLE ge.intel_competitor (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  is_simulated boolean NOT NULL DEFAULT false,
  run_id uuid,
  correlation_id uuid,
  name text,
  website text,
  segments text,
  internal_only boolean,
  schema_ref text,
  evidence_refs uuid[] NOT NULL DEFAULT '{}',
  payload jsonb NOT NULL,
  CONSTRAINT pk_intel_competitor PRIMARY KEY (id),
  CONSTRAINT uq_intel_competitor__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_intel_competitor__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.intel_competitor IS 'ENT-061 Competitor · scope S · Imm. M · Part 3.3 §3.3.3.2 + §3.3.7';

CREATE TABLE ge.intel_market_event (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  is_simulated boolean NOT NULL DEFAULT false,
  run_id uuid,
  correlation_id uuid,
  competitor_id uuid,
  event_type text,
  event_date date,
  summary text,
  evidence_id uuid,
  schema_ref text,
  evidence_refs uuid[] NOT NULL DEFAULT '{}',
  payload jsonb NOT NULL,
  CONSTRAINT pk_intel_market_event PRIMARY KEY (id),
  CONSTRAINT uq_intel_market_event__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_intel_market_event__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.intel_market_event IS 'ENT-062 MarketEvent · scope S · Imm. M · Part 3.3 §3.3.3.2 + §3.3.7';

CREATE TABLE ge.intel_organization (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  is_simulated boolean NOT NULL DEFAULT false,
  run_id uuid,
  correlation_id uuid,
  name text NOT NULL,
  normalized_name text NOT NULL,
  primary_domain text,
  legal_id text,
  org_type text NOT NULL DEFAULT 'unknown',
  industry_code text,
  country_code char(2),
  size_band text,
  relationship text NOT NULL DEFAULT 'prospect',
  merged_into_id uuid,
  merge_reversible_until timestamptz,
  owner_id uuid,
  tsv tsvector NOT NULL,
  schema_ref text,
  evidence_refs uuid[] NOT NULL DEFAULT '{}',
  payload jsonb NOT NULL,
  CONSTRAINT pk_intel_organization PRIMARY KEY (id),
  CONSTRAINT uq_intel_organization__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_intel_organization__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.intel_organization IS 'ENT-063 Organization · scope S · Imm. M · Part 3.3 §3.3.3.2';

CREATE TABLE ge.intel_location (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  is_simulated boolean NOT NULL DEFAULT false,
  run_id uuid,
  correlation_id uuid,
  organization_id uuid,
  country_code text,
  subdivision_code text,
  city text,
  address text,
  geo text,
  CONSTRAINT pk_intel_location PRIMARY KEY (id),
  CONSTRAINT uq_intel_location__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_intel_location__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.intel_location IS 'ENT-064 Location · scope S · Imm. M · Part 3.3 §3.3.3.2 + §3.3.7';

CREATE TABLE ge.intel_alias (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  is_simulated boolean NOT NULL DEFAULT false,
  run_id uuid,
  correlation_id uuid,
  organization_id uuid,
  alias_name text,
  alias_kind text,
  CONSTRAINT pk_intel_alias PRIMARY KEY (id),
  CONSTRAINT uq_intel_alias__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_intel_alias__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.intel_alias IS 'ENT-065 Alias · scope S · Imm. M · Part 3.3 §3.3.3.2 + §3.3.7';

CREATE TABLE ge.intel_signal_type (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid,
  startup_id uuid,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  code text,
  label text,
  examples jsonb,
  default_ttl_days integer,
  schema_ref text,
  evidence_refs uuid[] NOT NULL DEFAULT '{}',
  payload jsonb NOT NULL,
  CONSTRAINT pk_intel_signal_type PRIMARY KEY (id),
  CONSTRAINT uq_intel_signal_type__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_intel_signal_type__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.intel_signal_type IS 'ENT-066 SignalType · scope X · Imm. M · Part 3.3 §3.3.3.2 + §3.3.7';

CREATE TABLE ge.intel_signal (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  is_simulated boolean NOT NULL DEFAULT false,
  run_id uuid,
  correlation_id uuid,
  signal_type_id uuid NOT NULL,
  organization_id uuid NOT NULL,
  derivation text NOT NULL,
  state text NOT NULL DEFAULT 'proposed',
  confidence numeric(5,4) NOT NULL,
  evidence_count integer NOT NULL DEFAULT 0,
  observed_at timestamptz NOT NULL,
  expires_at timestamptz,
  classifier_run_id uuid,
  reviewer_id text,
  reviewed_at text,
  review_verdict text,
  schema_ref text,
  evidence_refs uuid[] NOT NULL DEFAULT '{}',
  payload jsonb NOT NULL,
  CONSTRAINT pk_intel_signal PRIMARY KEY (id),
  CONSTRAINT uq_intel_signal__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_intel_signal__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.intel_signal IS 'ENT-067 Signal · scope S · Imm. M · Part 3.3 §3.3.3.2';

CREATE TABLE ge.intel_need (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  is_simulated boolean NOT NULL DEFAULT false,
  run_id uuid,
  correlation_id uuid,
  organization_id uuid NOT NULL,
  need_category text NOT NULL,
  statement text NOT NULL,
  derivation text NOT NULL,
  state text NOT NULL DEFAULT 'proposed',
  source_signal_id uuid,
  health_data_flag boolean NOT NULL DEFAULT false,
  schema_ref text,
  evidence_refs uuid[] NOT NULL DEFAULT '{}',
  payload jsonb NOT NULL,
  CONSTRAINT pk_intel_need PRIMARY KEY (id),
  CONSTRAINT uq_intel_need__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_intel_need__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.intel_need IS 'ENT-068 Need · scope S · Imm. M · Part 3.3 §3.3.3.2';

CREATE TABLE ge.intel_need_evidence (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  correlation_id uuid,
  need_id uuid,
  evidence_id uuid,
  relevance text,
  schema_ref text,
  evidence_refs uuid[] NOT NULL DEFAULT '{}',
  payload jsonb NOT NULL,
  CONSTRAINT pk_intel_need_evidence PRIMARY KEY (id),
  CONSTRAINT uq_intel_need_evidence__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_intel_need_evidence__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.intel_need_evidence IS 'ENT-069 NeedEvidence · scope S · Imm. A · Part 3.3 §3.3.3.2 + §3.3.7';

CREATE TABLE ge.intel_match (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  is_simulated boolean NOT NULL DEFAULT false,
  run_id uuid,
  correlation_id uuid,
  need_id uuid,
  offering_version_id uuid,
  match_score numeric(9,4),
  rank integer,
  exclusion_reason text,
  readiness_ok boolean,
  CONSTRAINT pk_intel_match PRIMARY KEY (id),
  CONSTRAINT uq_intel_match__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_intel_match__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.intel_match IS 'ENT-070 Match · scope S · Imm. M · Part 3.3 §3.3.3.2 + §3.3.7';

CREATE TABLE ge.intel_scoring_model (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  version_no integer NOT NULL DEFAULT 1,
  status text NOT NULL DEFAULT 'draft',
  content_hash char(64),
  approval_id uuid,
  approved_at timestamptz,
  effective_from timestamptz,
  effective_to timestamptz,
  supersedes_id uuid,
  is_simulated boolean NOT NULL DEFAULT false,
  run_id uuid,
  correlation_id uuid,
  w_fit text,
  w_evidence text,
  w_intent text,
  w_readiness text,
  w_timing text,
  min_known_weight text,
  band_priority text,
  band_nurture text,
  CONSTRAINT pk_intel_scoring_model PRIMARY KEY (id),
  CONSTRAINT uq_intel_scoring_model__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_intel_scoring_model__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.intel_scoring_model IS 'ENT-071 ScoringModel (weights version) · scope S · Imm. V · Part 3.3 §3.3.3.2 + §3.3.7';

CREATE TABLE ge.intel_opportunity (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  is_simulated boolean NOT NULL DEFAULT false,
  run_id uuid,
  correlation_id uuid,
  organization_id uuid NOT NULL,
  offering_id uuid NOT NULL,
  match_id uuid,
  need_id uuid,
  opportunity_type text NOT NULL,
  state text NOT NULL DEFAULT 'discovered',
  current_score smallint,
  band text,
  current_score_version_id uuid,
  owner_id uuid,
  qualified_at timestamptz,
  priority_override text,
  rejection_reason text,
  schema_ref text,
  evidence_refs uuid[] NOT NULL DEFAULT '{}',
  payload jsonb NOT NULL,
  CONSTRAINT pk_intel_opportunity PRIMARY KEY (id),
  CONSTRAINT uq_intel_opportunity__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_intel_opportunity__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.intel_opportunity IS 'ENT-072 Opportunity · scope S · Imm. M · Part 3.3 §3.3.3.2';

CREATE TABLE ge.intel_score_version (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  correlation_id uuid,
  is_simulated boolean NOT NULL DEFAULT false,
  run_id uuid,
  opportunity_id uuid NOT NULL,
  scoring_model_id uuid NOT NULL,
  components jsonb NOT NULL,
  known_weight numeric(5,4) NOT NULL,
  score smallint,
  band text NOT NULL,
  trigger_reason text NOT NULL,
  evidence_ids uuid[] NOT NULL DEFAULT '{}',
  schema_ref text,
  evidence_refs uuid[] NOT NULL DEFAULT '{}',
  payload jsonb NOT NULL,
  CONSTRAINT pk_intel_score_version PRIMARY KEY (id),
  CONSTRAINT uq_intel_score_version__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_intel_score_version__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.intel_score_version IS 'ENT-073 ScoreVersion (computed score record) · scope S · Imm. A · Part 3.3 §3.3.3.2';

CREATE TABLE ge.intel_contact (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  is_simulated boolean NOT NULL DEFAULT false,
  run_id uuid,
  correlation_id uuid,
  organization_id uuid,
  person_type text NOT NULL DEFAULT 'professional',
  full_name text NOT NULL,
  name_search text NOT NULL,
  job_title text,
  role_code text,
  email_enc bytea,
  email_hmac char(64),
  email_domain text,
  is_role_based_address boolean NOT NULL DEFAULT false,
  phone_enc bytea,
  phone_hmac char(64),
  country_code char(2),
  timezone text,
  preferred_locale text,
  age_band text NOT NULL DEFAULT 'adult_assumed',
  guardian_contact_id uuid,
  grade_band text,
  verification_state text NOT NULL DEFAULT 'unverified',
  verified_until timestamptz,
  eligibility_basis text NOT NULL DEFAULT 'none',
  last_eligible_interaction_at timestamptz,
  erased_at timestamptz,
  import_job_id uuid,
  schema_ref text,
  evidence_refs uuid[] NOT NULL DEFAULT '{}',
  payload jsonb NOT NULL,
  CONSTRAINT pk_intel_contact PRIMARY KEY (id),
  CONSTRAINT uq_intel_contact__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_intel_contact__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.intel_contact IS 'ENT-074 Contact · scope S · Imm. M · Part 3.3 §3.3.3.2';

CREATE TABLE ge.intel_role_hypothesis (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  is_simulated boolean NOT NULL DEFAULT false,
  run_id uuid,
  correlation_id uuid,
  organization_id uuid,
  role_code text,
  confidence numeric(7,4),
  source_evidence_id uuid,
  resolved_contact_id uuid,
  CONSTRAINT pk_intel_role_hypothesis PRIMARY KEY (id),
  CONSTRAINT uq_intel_role_hypothesis__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_intel_role_hypothesis__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.intel_role_hypothesis IS 'ENT-075 RoleHypothesis · scope S · Imm. M · Part 3.3 §3.3.3.2 + §3.3.7';

CREATE TABLE ge.intel_contact_source (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  correlation_id uuid,
  contact_id uuid,
  source_url text,
  observed_at timestamptz,
  field_names text,
  licence_basis text,
  schema_ref text,
  evidence_refs uuid[] NOT NULL DEFAULT '{}',
  payload jsonb NOT NULL,
  CONSTRAINT pk_intel_contact_source PRIMARY KEY (id),
  CONSTRAINT uq_intel_contact_source__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_intel_contact_source__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.intel_contact_source IS 'ENT-076 ContactSource · scope S · Imm. A · Part 3.3 §3.3.3.2 + §3.3.7';

CREATE TABLE ge.intel_contact_verification (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  correlation_id uuid,
  is_simulated boolean NOT NULL DEFAULT false,
  run_id uuid,
  contact_id uuid,
  channel text,
  method text,
  result text,
  expires_at timestamptz,
  provider_ref text,
  schema_ref text,
  evidence_refs uuid[] NOT NULL DEFAULT '{}',
  payload jsonb NOT NULL,
  CONSTRAINT pk_intel_contact_verification PRIMARY KEY (id),
  CONSTRAINT uq_intel_contact_verification__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_intel_contact_verification__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.intel_contact_verification IS 'ENT-077 ContactVerification · scope S · Imm. A · Part 3.3 §3.3.3.2 + §3.3.7';

CREATE TABLE ge.intel_review (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  correlation_id uuid,
  opportunity_id uuid,
  signal_id uuid,
  need_id uuid,
  decision text,
  reason_code text,
  reviewer_id uuid,
  qualification_checks jsonb,
  CONSTRAINT pk_intel_review PRIMARY KEY (id),
  CONSTRAINT uq_intel_review__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_intel_review__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.intel_review IS 'ENT-078 Review · scope S · Imm. A · Part 3.3 §3.3.3.2 + §3.3.7';

CREATE TABLE ge.crm_lead (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  is_simulated boolean NOT NULL DEFAULT false,
  run_id uuid,
  correlation_id uuid,
  source_channel text NOT NULL,
  submission_id uuid,
  contact_id uuid,
  organization_id uuid,
  intent_summary text,
  state text NOT NULL DEFAULT 'received',
  duplicate_of_id uuid,
  dedupe_key char(64) NOT NULL,
  owner_id uuid,
  routing_rule_id uuid,
  consent_id uuid,
  attribution_ref text,
  opportunity_id uuid,
  rejected_at timestamptz,
  schema_ref text,
  evidence_refs uuid[] NOT NULL DEFAULT '{}',
  payload jsonb NOT NULL,
  CONSTRAINT pk_crm_lead PRIMARY KEY (id),
  CONSTRAINT uq_crm_lead__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_crm_lead__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.crm_lead IS 'ENT-079 Lead · scope S · Imm. M · Part 3.3 §3.3.3.2';

CREATE TABLE ge.crm_form (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  is_simulated boolean NOT NULL DEFAULT false,
  run_id uuid,
  correlation_id uuid,
  form_code text,
  purpose text,
  active_version_id uuid,
  schema_ref text,
  evidence_refs uuid[] NOT NULL DEFAULT '{}',
  payload jsonb NOT NULL,
  CONSTRAINT pk_crm_form PRIMARY KEY (id),
  CONSTRAINT uq_crm_form__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_crm_form__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.crm_form IS 'ENT-080 Form · scope S · Imm. M · Part 3.3 §3.3.3.2 + §3.3.7';

CREATE TABLE ge.crm_form_version (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  version_no integer NOT NULL DEFAULT 1,
  status text NOT NULL DEFAULT 'draft',
  content_hash char(64),
  approval_id uuid,
  approved_at timestamptz,
  effective_from timestamptz,
  effective_to timestamptz,
  supersedes_id uuid,
  is_simulated boolean NOT NULL DEFAULT false,
  run_id uuid,
  correlation_id uuid,
  form_id uuid,
  field_schema jsonb,
  consent_text_policy_id uuid,
  minor_handling text,
  CONSTRAINT pk_crm_form_version PRIMARY KEY (id),
  CONSTRAINT uq_crm_form_version__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_crm_form_version__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.crm_form_version IS 'ENT-081 FormVersion · scope S · Imm. V · Part 3.3 §3.3.3.2 + §3.3.7';

CREATE TABLE ge.crm_submission (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  correlation_id uuid,
  is_simulated boolean NOT NULL DEFAULT false,
  run_id uuid,
  form_version_id uuid,
  idempotency_key text,
  body_hash char(64),
  payload_min jsonb,
  ip_hmac char(64),
  screening_result text,
  CONSTRAINT pk_crm_submission PRIMARY KEY (id),
  CONSTRAINT uq_crm_submission__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_crm_submission__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.crm_submission IS 'ENT-082 Submission · scope S · Imm. A · Part 3.3 §3.3.3.2 + §3.3.7';

CREATE TABLE ge.crm_pipeline (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  version_no integer NOT NULL DEFAULT 1,
  status text NOT NULL DEFAULT 'draft',
  content_hash char(64),
  approval_id uuid,
  approved_at timestamptz,
  effective_from timestamptz,
  effective_to timestamptz,
  supersedes_id uuid,
  is_simulated boolean NOT NULL DEFAULT false,
  run_id uuid,
  correlation_id uuid,
  opportunity_type text,
  closure_policy_id uuid,
  name text,
  CONSTRAINT pk_crm_pipeline PRIMARY KEY (id),
  CONSTRAINT uq_crm_pipeline__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_crm_pipeline__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.crm_pipeline IS 'ENT-083 Pipeline · scope S · Imm. V · Part 3.3 §3.3.3.2 + §3.3.7';

CREATE TABLE ge.crm_stage (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  version_no integer NOT NULL DEFAULT 1,
  status text NOT NULL DEFAULT 'draft',
  content_hash char(64),
  approval_id uuid,
  approved_at timestamptz,
  effective_from timestamptz,
  effective_to timestamptz,
  supersedes_id uuid,
  is_simulated boolean NOT NULL DEFAULT false,
  run_id uuid,
  correlation_id uuid,
  pipeline_id uuid,
  code text,
  ordinal text,
  default_weight text,
  is_terminal boolean,
  entry_rules jsonb,
  exit_rules jsonb,
  allowed_next text,
  schema_ref text,
  evidence_refs uuid[] NOT NULL DEFAULT '{}',
  payload jsonb NOT NULL,
  CONSTRAINT pk_crm_stage PRIMARY KEY (id),
  CONSTRAINT uq_crm_stage__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_crm_stage__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.crm_stage IS 'ENT-084 Stage · scope S · Imm. V · Part 3.3 §3.3.3.2 + §3.3.7';

CREATE TABLE ge.crm_closure_policy (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  version_no integer NOT NULL DEFAULT 1,
  status text NOT NULL DEFAULT 'draft',
  content_hash char(64),
  approval_id uuid,
  approved_at timestamptz,
  effective_from timestamptz,
  effective_to timestamptz,
  supersedes_id uuid,
  is_simulated boolean NOT NULL DEFAULT false,
  run_id uuid,
  correlation_id uuid,
  opportunity_type text,
  close_on text,
  evidence_required jsonb,
  CONSTRAINT pk_crm_closure_policy PRIMARY KEY (id),
  CONSTRAINT uq_crm_closure_policy__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_crm_closure_policy__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.crm_closure_policy IS 'ENT-085 ClosurePolicy · scope S · Imm. V · Part 3.3 §3.3.3.2 + §3.3.7';

CREATE TABLE ge.crm_deal (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  is_simulated boolean NOT NULL DEFAULT false,
  run_id uuid,
  correlation_id uuid,
  deal_no text NOT NULL,
  title text NOT NULL,
  opportunity_id uuid,
  organization_id uuid NOT NULL,
  offering_id uuid NOT NULL,
  pipeline_id uuid NOT NULL,
  stage_id uuid NOT NULL,
  stage_code text NOT NULL,
  owner_id uuid NOT NULL,
  expected_value numeric(18,2),
  currency char(3),
  expected_close_date date,
  accepted_quote_id uuid,
  closure_status text NOT NULL DEFAULT 'open',
  awarded_at timestamptz,
  signed_at timestamptz,
  delivered_at timestamptz,
  paid_at timestamptz,
  lost_reason_code text,
  recontact_not_before date,
  schema_ref text,
  evidence_refs uuid[] NOT NULL DEFAULT '{}',
  payload jsonb NOT NULL,
  CONSTRAINT pk_crm_deal PRIMARY KEY (id),
  CONSTRAINT uq_crm_deal__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_crm_deal__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.crm_deal IS 'ENT-086 Deal · scope S · Imm. M · Part 3.3 §3.3.3.2';

CREATE TABLE ge.crm_stage_transition (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  correlation_id uuid,
  is_simulated boolean NOT NULL DEFAULT false,
  run_id uuid,
  deal_id uuid NOT NULL,
  from_stage_id uuid,
  to_stage_id uuid NOT NULL,
  guard_results jsonb NOT NULL DEFAULT '{}'::jsonb,
  evidence_refs jsonb NOT NULL DEFAULT '[]'::jsonb,
  reason_code text,
  deal_revision integer NOT NULL,
  occurred_at timestamptz NOT NULL DEFAULT now(),
  CONSTRAINT pk_crm_stage_transition PRIMARY KEY (id),
  CONSTRAINT uq_crm_stage_transition__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_crm_stage_transition__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.crm_stage_transition IS 'ENT-087 DealStageTransition · scope S · Imm. A · Part 3.3 §3.3.3.2';

CREATE TABLE ge.crm_activity (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  correlation_id uuid,
  is_simulated boolean NOT NULL DEFAULT false,
  run_id uuid,
  activity_type text NOT NULL,
  subject_type text NOT NULL,
  subject_id text NOT NULL,
  organization_id uuid,
  summary text NOT NULL,
  body_ref text,
  occurred_at timestamptz NOT NULL,
  visibility text NOT NULL DEFAULT 'team',
  schema_ref text,
  evidence_refs uuid[] NOT NULL DEFAULT '{}',
  payload jsonb NOT NULL,
  CONSTRAINT pk_crm_activity PRIMARY KEY (id),
  CONSTRAINT uq_crm_activity__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_crm_activity__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.crm_activity IS 'ENT-088 Activity · scope S · Imm. A · Part 3.3 §3.3.3.2';

CREATE TABLE ge.eng_message_template (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  version_no integer NOT NULL DEFAULT 1,
  status text NOT NULL DEFAULT 'draft',
  content_hash char(64),
  approval_id uuid,
  approved_at timestamptz,
  effective_from timestamptz,
  effective_to timestamptz,
  supersedes_id uuid,
  is_simulated boolean NOT NULL DEFAULT false,
  run_id uuid,
  correlation_id uuid,
  channel text,
  locale text,
  purpose text,
  body jsonb,
  provider_template_ref text,
  claim_ids uuid[],
  schema_ref text,
  evidence_refs uuid[] NOT NULL DEFAULT '{}',
  payload jsonb NOT NULL,
  CONSTRAINT pk_eng_message_template PRIMARY KEY (id),
  CONSTRAINT uq_eng_message_template__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_eng_message_template__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.eng_message_template IS 'ENT-090 MessageTemplate (FRD "Template") · scope S · Imm. V · Part 3.3 §3.3.3.2 + §3.3.7';

CREATE TABLE ge.eng_message_draft (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  is_simulated boolean NOT NULL DEFAULT false,
  run_id uuid,
  correlation_id uuid,
  template_id uuid,
  opportunity_id uuid,
  contact_id uuid,
  body text,
  content_hash char(64),
  citations uuid,
  model_run_id uuid,
  state text,
  schema_ref text,
  evidence_refs uuid[] NOT NULL DEFAULT '{}',
  payload jsonb NOT NULL,
  CONSTRAINT pk_eng_message_draft PRIMARY KEY (id),
  CONSTRAINT uq_eng_message_draft__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_eng_message_draft__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.eng_message_draft IS 'ENT-091 MessageDraft · scope S · Imm. M · Part 3.3 §3.3.3.2 + §3.3.7';

CREATE TABLE ge.eng_thread (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  is_simulated boolean NOT NULL DEFAULT false,
  run_id uuid,
  correlation_id uuid,
  contact_id uuid,
  organization_id uuid,
  primary_channel text NOT NULL,
  channel_account_id uuid NOT NULL,
  owner_id uuid,
  state text NOT NULL DEFAULT 'open',
  last_message_id uuid,
  last_activity_at timestamptz NOT NULL DEFAULT now(),
  service_window_expires_at timestamptz,
  deal_id uuid,
  schema_ref text,
  evidence_refs uuid[] NOT NULL DEFAULT '{}',
  payload jsonb NOT NULL,
  CONSTRAINT pk_eng_thread PRIMARY KEY (id),
  CONSTRAINT uq_eng_thread__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_eng_thread__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.eng_thread IS 'ENT-092 Thread · scope S · Imm. M · Part 3.3 §3.3.3.2';

CREATE TABLE ge.eng_message (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  is_simulated boolean NOT NULL DEFAULT false,
  run_id uuid,
  correlation_id uuid,
  thread_id uuid NOT NULL,
  direction text NOT NULL,
  channel text NOT NULL,
  draft_id uuid,
  template_id text,
  template_version text,
  enrollment_id uuid,
  campaign_version_id uuid,
  recipient_hmac char(64) NOT NULL,
  recipient_enc bytea NOT NULL,
  subject text,
  body_storage_key text,
  content_hash char(64) NOT NULL,
  approval_id uuid,
  state text NOT NULL DEFAULT 'drafted',
  outcome_certainty text,
  idempotency_key text NOT NULL,
  provider_message_id text,
  eligibility_decision_id uuid,
  scheduled_for timestamptz,
  sent_at timestamptz,
  cost_reservation_id uuid,
  schema_ref text,
  evidence_refs uuid[] NOT NULL DEFAULT '{}',
  payload jsonb NOT NULL,
  CONSTRAINT pk_eng_message PRIMARY KEY (id),
  CONSTRAINT uq_eng_message__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_eng_message__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.eng_message IS 'ENT-093 Message · scope S · Imm. F · Part 3.3 §3.3.3.2';

CREATE TABLE ge.eng_delivery_event (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  correlation_id uuid,
  message_id uuid NOT NULL,
  channel_account_id uuid NOT NULL,
  event_type text NOT NULL,
  provider_event_id text NOT NULL,
  occurred_at timestamptz NOT NULL,
  received_at timestamptz NOT NULL DEFAULT now(),
  diagnostic jsonb,
  ip_hmac char(64),
  schema_ref text,
  evidence_refs uuid[] NOT NULL DEFAULT '{}',
  payload jsonb NOT NULL,
  CONSTRAINT pk_eng_delivery_event PRIMARY KEY (id),
  CONSTRAINT uq_eng_delivery_event__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_eng_delivery_event__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.eng_delivery_event IS 'ENT-094 DeliveryEvent · scope S · Imm. A · Part 3.3 §3.3.3.2';

CREATE TABLE ge.eng_inbound_event (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  correlation_id uuid,
  thread_id uuid,
  channel_account_id uuid,
  provider_message_id uuid,
  sender_hmac char(64),
  body_storage_key text,
  is_stop_keyword boolean,
  received_at timestamptz,
  schema_ref text,
  evidence_refs uuid[] NOT NULL DEFAULT '{}',
  payload jsonb NOT NULL,
  CONSTRAINT pk_eng_inbound_event PRIMARY KEY (id),
  CONSTRAINT uq_eng_inbound_event__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_eng_inbound_event__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.eng_inbound_event IS 'ENT-095 InboundEvent · scope S · Imm. A · Part 3.3 §3.3.3.2 + §3.3.7';

CREATE TABLE ge.eng_intent (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  correlation_id uuid,
  inbound_event_id uuid,
  intent_code text,
  confidence numeric(7,4),
  model_run_id uuid,
  rule_hit text,
  CONSTRAINT pk_eng_intent PRIMARY KEY (id),
  CONSTRAINT uq_eng_intent__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_eng_intent__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.eng_intent IS 'ENT-096 Intent · scope S · Imm. A · Part 3.3 §3.3.3.2 + §3.3.7';

CREATE TABLE ge.eng_identity_link (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  is_simulated boolean NOT NULL DEFAULT false,
  run_id uuid,
  correlation_id uuid,
  contact_id uuid,
  channel text,
  address_hmac char(64),
  verified text,
  schema_ref text,
  evidence_refs uuid[] NOT NULL DEFAULT '{}',
  payload jsonb NOT NULL,
  CONSTRAINT pk_eng_identity_link PRIMARY KEY (id),
  CONSTRAINT uq_eng_identity_link__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_eng_identity_link__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.eng_identity_link IS 'ENT-097 IdentityLink · scope S · Imm. M · Part 3.3 §3.3.3.2 + §3.3.7';

CREATE TABLE ge.eng_routing_rule (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  version_no integer NOT NULL DEFAULT 1,
  status text NOT NULL DEFAULT 'draft',
  content_hash char(64),
  approval_id uuid,
  approved_at timestamptz,
  effective_from timestamptz,
  effective_to timestamptz,
  supersedes_id uuid,
  is_simulated boolean NOT NULL DEFAULT false,
  run_id uuid,
  correlation_id uuid,
  priority integer,
  condition jsonb,
  assign_to text,
  handover_sla_minutes integer,
  schema_ref text,
  evidence_refs uuid[] NOT NULL DEFAULT '{}',
  payload jsonb NOT NULL,
  CONSTRAINT pk_eng_routing_rule PRIMARY KEY (id),
  CONSTRAINT uq_eng_routing_rule__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_eng_routing_rule__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.eng_routing_rule IS 'ENT-098 RoutingRule · scope S · Imm. V · Part 3.3 §3.3.3.2 + §3.3.7';

CREATE TABLE ge.eng_chat_session (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  is_simulated boolean NOT NULL DEFAULT false,
  run_id uuid,
  correlation_id uuid,
  visitor_ref text,
  locale text,
  state text,
  transcript_storage_key text,
  lead_id uuid,
  expires_at timestamptz,
  CONSTRAINT pk_eng_chat_session PRIMARY KEY (id),
  CONSTRAINT uq_eng_chat_session__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_eng_chat_session__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.eng_chat_session IS 'ENT-099 ChatSession · scope S · Imm. M · Part 3.3 §3.3.3.2 + §3.3.7';

CREATE TABLE ge.eng_sequence (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  version_no integer NOT NULL DEFAULT 1,
  status text NOT NULL DEFAULT 'draft',
  content_hash char(64),
  approval_id uuid,
  approved_at timestamptz,
  effective_from timestamptz,
  effective_to timestamptz,
  supersedes_id uuid,
  is_simulated boolean NOT NULL DEFAULT false,
  run_id uuid,
  correlation_id uuid,
  code text NOT NULL,
  purpose text NOT NULL,
  max_attempts smallint NOT NULL DEFAULT 3,
  min_interval_business_days smallint NOT NULL DEFAULT 2,
  stop_conditions text[] NOT NULL,
  schema_ref text,
  evidence_refs uuid[] NOT NULL DEFAULT '{}',
  payload jsonb NOT NULL,
  CONSTRAINT pk_eng_sequence PRIMARY KEY (id),
  CONSTRAINT uq_eng_sequence__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_eng_sequence__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.eng_sequence IS 'ENT-100 Sequence · scope S · Imm. V · Part 3.3 §3.3.3.2';

CREATE TABLE ge.eng_sequence_step (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  version_no integer NOT NULL DEFAULT 1,
  status text NOT NULL DEFAULT 'draft',
  content_hash char(64),
  approval_id uuid,
  approved_at timestamptz,
  effective_from timestamptz,
  effective_to timestamptz,
  supersedes_id uuid,
  is_simulated boolean NOT NULL DEFAULT false,
  run_id uuid,
  correlation_id uuid,
  sequence_id uuid,
  ordinal text,
  channel text,
  template_id uuid,
  wait_business_days integer,
  condition jsonb,
  schema_ref text,
  evidence_refs uuid[] NOT NULL DEFAULT '{}',
  payload jsonb NOT NULL,
  CONSTRAINT pk_eng_sequence_step PRIMARY KEY (id),
  CONSTRAINT uq_eng_sequence_step__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_eng_sequence_step__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.eng_sequence_step IS 'ENT-101 SequenceStep (FRD "Step") · scope S · Imm. V · Part 3.3 §3.3.3.2 + §3.3.7';

CREATE TABLE ge.eng_enrollment (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  is_simulated boolean NOT NULL DEFAULT false,
  run_id uuid,
  correlation_id uuid,
  sequence_id uuid NOT NULL,
  contact_id uuid NOT NULL,
  relationship_key char(64) NOT NULL,
  state text NOT NULL DEFAULT 'enrolled',
  current_step_ordinal smallint NOT NULL DEFAULT 0,
  next_due_at timestamptz,
  stop_reason text,
  schema_ref text,
  evidence_refs uuid[] NOT NULL DEFAULT '{}',
  payload jsonb NOT NULL,
  CONSTRAINT pk_eng_enrollment PRIMARY KEY (id),
  CONSTRAINT uq_eng_enrollment__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_eng_enrollment__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.eng_enrollment IS 'ENT-102 Enrollment · scope S · Imm. M · Part 3.3 §3.3.3.2';

CREATE TABLE ge.eng_meeting (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  is_simulated boolean NOT NULL DEFAULT false,
  run_id uuid,
  correlation_id uuid,
  thread_id uuid,
  deal_id uuid,
  organizer_id uuid NOT NULL,
  contact_id uuid,
  starts_at timestamptz NOT NULL,
  ends_at timestamptz NOT NULL,
  organizer_timezone text NOT NULL,
  attendee_timezone text NOT NULL,
  state text NOT NULL DEFAULT 'slots_offered',
  hold_expires_at timestamptz,
  provider_event_ref text,
  calendar_link_id uuid,
  attendance_evidence text,
  meeting_url_enc bytea,
  schema_ref text,
  evidence_refs uuid[] NOT NULL DEFAULT '{}',
  payload jsonb NOT NULL,
  CONSTRAINT pk_eng_meeting PRIMARY KEY (id),
  CONSTRAINT uq_eng_meeting__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_eng_meeting__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.eng_meeting IS 'ENT-103 Meeting · scope S · Imm. M · Part 3.3 §3.3.3.2';

CREATE TABLE ge.eng_calendar_link (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  is_simulated boolean NOT NULL DEFAULT false,
  run_id uuid,
  correlation_id uuid,
  user_id uuid,
  provider text,
  integration_id uuid,
  work_hours jsonb,
  buffer_minutes integer,
  schema_ref text,
  evidence_refs uuid[] NOT NULL DEFAULT '{}',
  payload jsonb NOT NULL,
  CONSTRAINT pk_eng_calendar_link PRIMARY KEY (id),
  CONSTRAINT uq_eng_calendar_link__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_eng_calendar_link__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.eng_calendar_link IS 'ENT-104 CalendarLink · scope S · Imm. M · Part 3.3 §3.3.3.2 + §3.3.7';

CREATE TABLE ge.mkt_content_asset (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  is_simulated boolean NOT NULL DEFAULT false,
  run_id uuid,
  correlation_id uuid,
  asset_type text,
  title text,
  owner_id uuid,
  brief text,
  schema_ref text,
  evidence_refs uuid[] NOT NULL DEFAULT '{}',
  payload jsonb NOT NULL,
  CONSTRAINT pk_mkt_content_asset PRIMARY KEY (id),
  CONSTRAINT uq_mkt_content_asset__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_mkt_content_asset__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.mkt_content_asset IS 'ENT-105 ContentAsset · scope S · Imm. M · Part 3.3 §3.3.3.2 + §3.3.7';

CREATE TABLE ge.mkt_content_version (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  version_no integer NOT NULL DEFAULT 1,
  status text NOT NULL DEFAULT 'draft',
  content_hash char(64),
  approval_id uuid,
  approved_at timestamptz,
  effective_from timestamptz,
  effective_to timestamptz,
  supersedes_id uuid,
  is_simulated boolean NOT NULL DEFAULT false,
  run_id uuid,
  correlation_id uuid,
  asset_id uuid NOT NULL,
  locale text NOT NULL DEFAULT 'en-IN',
  body jsonb NOT NULL,
  claim_ids uuid[] NOT NULL DEFAULT '{}',
  author_id uuid NOT NULL,
  ai_generated boolean NOT NULL DEFAULT false,
  model_run_id uuid,
  accessibility_result text,
  is_machine_translation boolean NOT NULL DEFAULT false,
  schema_ref text,
  evidence_refs uuid[] NOT NULL DEFAULT '{}',
  payload jsonb NOT NULL,
  CONSTRAINT pk_mkt_content_version PRIMARY KEY (id),
  CONSTRAINT uq_mkt_content_version__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_mkt_content_version__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.mkt_content_version IS 'ENT-106 ContentVersion · scope S · Imm. V · Part 3.3 §3.3.3.2';

CREATE TABLE ge.mkt_social_publication (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  is_simulated boolean NOT NULL DEFAULT false,
  run_id uuid,
  correlation_id uuid,
  content_version_id uuid,
  channel_account_id uuid,
  scheduled_at timestamptz,
  idempotency_key text,
  provider_post_id uuid,
  state text,
  outcome_certainty text,
  schema_ref text,
  evidence_refs uuid[] NOT NULL DEFAULT '{}',
  payload jsonb NOT NULL,
  CONSTRAINT pk_mkt_social_publication PRIMARY KEY (id),
  CONSTRAINT uq_mkt_social_publication__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_mkt_social_publication__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.mkt_social_publication IS 'ENT-107 SocialPublication · scope S · Imm. F · Part 3.3 §3.3.3.2 + §3.3.7';

CREATE TABLE ge.mkt_keyword (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  is_simulated boolean NOT NULL DEFAULT false,
  run_id uuid,
  correlation_id uuid,
  phrase text,
  locale text,
  intent text,
  target_page_id uuid,
  schema_ref text,
  evidence_refs uuid[] NOT NULL DEFAULT '{}',
  payload jsonb NOT NULL,
  CONSTRAINT pk_mkt_keyword PRIMARY KEY (id),
  CONSTRAINT uq_mkt_keyword__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_mkt_keyword__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.mkt_keyword IS 'ENT-108 Keyword · scope S · Imm. M · Part 3.3 §3.3.3.2 + §3.3.7';

CREATE TABLE ge.mkt_seo_issue (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  is_simulated boolean NOT NULL DEFAULT false,
  run_id uuid,
  correlation_id uuid,
  page_id uuid,
  issue_code text,
  severity text,
  state text,
  detected_at timestamptz,
  source text,
  schema_ref text,
  evidence_refs uuid[] NOT NULL DEFAULT '{}',
  payload jsonb NOT NULL,
  CONSTRAINT pk_mkt_seo_issue PRIMARY KEY (id),
  CONSTRAINT uq_mkt_seo_issue__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_mkt_seo_issue__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.mkt_seo_issue IS 'ENT-109 SEOIssue · scope S · Imm. M · Part 3.3 §3.3.3.2 + §3.3.7';

CREATE TABLE ge.mkt_page_metric (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  correlation_id uuid,
  page_id uuid,
  keyword_id uuid,
  metric_date date,
  impressions text,
  clicks text,
  avg_position text,
  enquiries text,
  source text,
  schema_ref text,
  evidence_refs uuid[] NOT NULL DEFAULT '{}',
  payload jsonb NOT NULL,
  CONSTRAINT pk_mkt_page_metric PRIMARY KEY (id),
  CONSTRAINT uq_mkt_page_metric__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_mkt_page_metric__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.mkt_page_metric IS 'ENT-110 PageMetric · scope S · Imm. A · Part 3.3 §3.3.3.2 + §3.3.7';

CREATE TABLE ge.mkt_landing_page (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  is_simulated boolean NOT NULL DEFAULT false,
  run_id uuid,
  correlation_id uuid,
  page_kind text,
  slug text,
  locale text,
  template_code text,
  blocks_version_id uuid,
  form_id uuid,
  is_health_related boolean,
  schema_ref text,
  evidence_refs uuid[] NOT NULL DEFAULT '{}',
  payload jsonb NOT NULL,
  CONSTRAINT pk_mkt_landing_page PRIMARY KEY (id),
  CONSTRAINT uq_mkt_landing_page__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_mkt_landing_page__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.mkt_landing_page IS 'ENT-111 LandingPage (site or landing page) · scope S · Imm. M · Part 3.3 §3.3.3.2 + §3.3.7';

CREATE TABLE ge.mkt_publication (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  is_simulated boolean NOT NULL DEFAULT false,
  run_id uuid,
  correlation_id uuid,
  target_kind text NOT NULL,
  target_id uuid NOT NULL,
  domain_id uuid NOT NULL,
  locale text NOT NULL,
  path text NOT NULL,
  current_snapshot_id uuid,
  previous_snapshot_id uuid,
  state text NOT NULL DEFAULT 'draft',
  cache_tag text NOT NULL,
  CONSTRAINT pk_mkt_publication PRIMARY KEY (id),
  CONSTRAINT uq_mkt_publication__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_mkt_publication__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.mkt_publication IS 'ENT-112 Publication · scope S · Imm. M · Part 3.3 §3.3.3.2';

CREATE TABLE ge.mkt_publication_snapshot (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  correlation_id uuid,
  publication_id uuid,
  content_version_id uuid,
  snapshot_hash char(64),
  storage_key text,
  approval_id uuid,
  published_at timestamptz,
  published_by text,
  CONSTRAINT pk_mkt_publication_snapshot PRIMARY KEY (id),
  CONSTRAINT uq_mkt_publication_snapshot__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_mkt_publication_snapshot__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.mkt_publication_snapshot IS 'ENT-113 PublicationSnapshot · scope S · Imm. A · Part 3.3 §3.3.3.2 + §3.3.7';

CREATE TABLE ge.mkt_preview_grant (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  is_simulated boolean NOT NULL DEFAULT false,
  run_id uuid,
  correlation_id uuid,
  publication_id uuid,
  token_hash char(64),
  expires_at timestamptz,
  created_for text,
  CONSTRAINT pk_mkt_preview_grant PRIMARY KEY (id),
  CONSTRAINT uq_mkt_preview_grant__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_mkt_preview_grant__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.mkt_preview_grant IS 'ENT-114 PreviewGrant · scope S · Imm. M · Part 3.3 §3.3.3.2 + §3.3.7';

CREATE TABLE ge.mkt_campaign (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  is_simulated boolean NOT NULL DEFAULT false,
  run_id uuid,
  correlation_id uuid,
  name text NOT NULL,
  objective text NOT NULL,
  channels text[] NOT NULL,
  state text NOT NULL DEFAULT 'draft',
  current_version_id uuid,
  starts_at timestamptz,
  ends_at timestamptz,
  budget_id uuid,
  complaint_threshold_pct numeric(7,4) NOT NULL DEFAULT 0.1000,
  attribution_window_days smallint NOT NULL DEFAULT 90,
  schema_ref text,
  evidence_refs uuid[] NOT NULL DEFAULT '{}',
  payload jsonb NOT NULL,
  CONSTRAINT pk_mkt_campaign PRIMARY KEY (id),
  CONSTRAINT uq_mkt_campaign__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_mkt_campaign__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.mkt_campaign IS 'ENT-115 Campaign · scope S · Imm. M · Part 3.3 §3.3.3.2';

CREATE TABLE ge.mkt_campaign_version (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  version_no integer NOT NULL DEFAULT 1,
  status text NOT NULL DEFAULT 'draft',
  content_hash char(64),
  approval_id uuid,
  approved_at timestamptz,
  effective_from timestamptz,
  effective_to timestamptz,
  supersedes_id uuid,
  is_simulated boolean NOT NULL DEFAULT false,
  run_id uuid,
  correlation_id uuid,
  campaign_id uuid,
  audience_id uuid,
  content_version_ids uuid[],
  budget_cap numeric(18,2),
  currency char(3),
  schedule jsonb,
  simulation_result jsonb,
  schema_ref text,
  evidence_refs uuid[] NOT NULL DEFAULT '{}',
  payload jsonb NOT NULL,
  CONSTRAINT pk_mkt_campaign_version PRIMARY KEY (id),
  CONSTRAINT uq_mkt_campaign_version__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_mkt_campaign_version__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.mkt_campaign_version IS 'ENT-116 CampaignVersion · scope S · Imm. V · Part 3.3 §3.3.3.2 + §3.3.7';

CREATE TABLE ge.mkt_audience (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  version_no integer NOT NULL DEFAULT 1,
  status text NOT NULL DEFAULT 'draft',
  content_hash char(64),
  approval_id uuid,
  approved_at timestamptz,
  effective_from timestamptz,
  effective_to timestamptz,
  supersedes_id uuid,
  is_simulated boolean NOT NULL DEFAULT false,
  run_id uuid,
  correlation_id uuid,
  criteria jsonb,
  member_count integer,
  frozen_at timestamptz,
  excluded_counts jsonb,
  schema_ref text,
  evidence_refs uuid[] NOT NULL DEFAULT '{}',
  payload jsonb NOT NULL,
  CONSTRAINT pk_mkt_audience PRIMARY KEY (id),
  CONSTRAINT uq_mkt_audience__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_mkt_audience__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.mkt_audience IS 'ENT-117 Audience · scope S · Imm. V · Part 3.3 §3.3.3.2 + §3.3.7';

CREATE TABLE ge.mkt_ad_campaign (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  is_simulated boolean NOT NULL DEFAULT false,
  run_id uuid,
  correlation_id uuid,
  campaign_id uuid,
  platform text,
  provider_campaign_id uuid,
  daily_cap text,
  monthly_cap text,
  currency char(3),
  state text,
  budget_id uuid,
  schema_ref text,
  evidence_refs uuid[] NOT NULL DEFAULT '{}',
  payload jsonb NOT NULL,
  CONSTRAINT pk_mkt_ad_campaign PRIMARY KEY (id),
  CONSTRAINT uq_mkt_ad_campaign__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_mkt_ad_campaign__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.mkt_ad_campaign IS 'ENT-118 AdCampaign · scope S · Imm. M · Part 3.3 §3.3.3.2 + §3.3.7';

CREATE TABLE ge.mkt_spend_event (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  correlation_id uuid,
  ad_campaign_id uuid,
  spend_date date,
  amount numeric(18,2),
  currency char(3),
  provider_report_id uuid,
  schema_ref text,
  evidence_refs uuid[] NOT NULL DEFAULT '{}',
  payload jsonb NOT NULL,
  CONSTRAINT pk_mkt_spend_event PRIMARY KEY (id),
  CONSTRAINT uq_mkt_spend_event__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_mkt_spend_event__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.mkt_spend_event IS 'ENT-119 SpendEvent · scope S · Imm. A · Part 3.3 §3.3.3.2 + §3.3.7';

CREATE TABLE ge.mkt_event (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  is_simulated boolean NOT NULL DEFAULT false,
  run_id uuid,
  correlation_id uuid,
  event_kind text,
  title text,
  starts_at timestamptz,
  ends_at timestamptz,
  capacity text,
  provider_event_ref text,
  state text,
  schema_ref text,
  evidence_refs uuid[] NOT NULL DEFAULT '{}',
  payload jsonb NOT NULL,
  CONSTRAINT pk_mkt_event PRIMARY KEY (id),
  CONSTRAINT uq_mkt_event__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_mkt_event__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.mkt_event IS 'ENT-120 MarketingEvent (FRD "Event": webinar/demo) · scope S · Imm. M · Part 3.3 §3.3.3.2 + §3.3.7';

CREATE TABLE ge.mkt_registration (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  is_simulated boolean NOT NULL DEFAULT false,
  run_id uuid,
  correlation_id uuid,
  event_id uuid,
  contact_id uuid,
  consent_id uuid,
  state text,
  schema_ref text,
  evidence_refs uuid[] NOT NULL DEFAULT '{}',
  payload jsonb NOT NULL,
  CONSTRAINT pk_mkt_registration PRIMARY KEY (id),
  CONSTRAINT uq_mkt_registration__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_mkt_registration__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.mkt_registration IS 'ENT-121 Registration · scope S · Imm. M · Part 3.3 §3.3.3.2 + §3.3.7';

CREATE TABLE ge.mkt_attendance (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  correlation_id uuid,
  registration_id uuid,
  joined_at timestamptz,
  left_at timestamptz,
  minutes_attended text,
  source text,
  schema_ref text,
  evidence_refs uuid[] NOT NULL DEFAULT '{}',
  payload jsonb NOT NULL,
  CONSTRAINT pk_mkt_attendance PRIMARY KEY (id),
  CONSTRAINT uq_mkt_attendance__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_mkt_attendance__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.mkt_attendance IS 'ENT-122 Attendance · scope S · Imm. A · Part 3.3 §3.3.3.2 + §3.3.7';

CREATE TABLE ge.mkt_referral (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  is_simulated boolean NOT NULL DEFAULT false,
  run_id uuid,
  correlation_id uuid,
  partner_id uuid,
  referral_code text,
  referred_contact_id uuid,
  consent_id uuid,
  proposed_commission_pct numeric(7,4),
  approval_id uuid,
  state text,
  schema_ref text,
  evidence_refs uuid[] NOT NULL DEFAULT '{}',
  payload jsonb NOT NULL,
  CONSTRAINT pk_mkt_referral PRIMARY KEY (id),
  CONSTRAINT uq_mkt_referral__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_mkt_referral__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.mkt_referral IS 'ENT-123 Referral · scope S · Imm. M · Part 3.3 §3.3.3.2 + §3.3.7';

CREATE TABLE ge.mkt_attribution_event (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  correlation_id uuid,
  touch_type text,
  anonymous_ref text,
  lead_id uuid,
  campaign_id uuid,
  referral_id uuid,
  utm jsonb,
  occurred_at timestamptz,
  schema_ref text,
  evidence_refs uuid[] NOT NULL DEFAULT '{}',
  payload jsonb NOT NULL,
  CONSTRAINT pk_mkt_attribution_event PRIMARY KEY (id),
  CONSTRAINT uq_mkt_attribution_event__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_mkt_attribution_event__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.mkt_attribution_event IS 'ENT-124 AttributionEvent · scope S · Imm. A · Part 3.3 §3.3.3.2 + §3.3.7';

CREATE TABLE ge.com_proposal (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  is_simulated boolean NOT NULL DEFAULT false,
  run_id uuid,
  correlation_id uuid,
  deal_id uuid NOT NULL,
  proposal_no text NOT NULL,
  template_ref uuid NOT NULL,
  state text NOT NULL DEFAULT 'draft',
  current_version_id uuid,
  portal_grant_id uuid,
  schema_ref text,
  evidence_refs uuid[] NOT NULL DEFAULT '{}',
  payload jsonb NOT NULL,
  CONSTRAINT pk_com_proposal PRIMARY KEY (id),
  CONSTRAINT uq_com_proposal__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_com_proposal__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.com_proposal IS 'ENT-125 Proposal · scope S · Imm. M · Part 3.3 §3.3.3.2';

CREATE TABLE ge.com_proposal_version (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  version_no integer NOT NULL DEFAULT 1,
  status text NOT NULL DEFAULT 'draft',
  content_hash char(64),
  approval_id uuid,
  approved_at timestamptz,
  effective_from timestamptz,
  effective_to timestamptz,
  supersedes_id uuid,
  is_simulated boolean NOT NULL DEFAULT false,
  run_id uuid,
  correlation_id uuid,
  proposal_id uuid,
  body_storage_key text,
  price_snapshot jsonb,
  author_id uuid,
  schema_ref text,
  evidence_refs uuid[] NOT NULL DEFAULT '{}',
  payload jsonb NOT NULL,
  CONSTRAINT pk_com_proposal_version PRIMARY KEY (id),
  CONSTRAINT uq_com_proposal_version__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_com_proposal_version__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.com_proposal_version IS 'ENT-126 ProposalVersion · scope S · Imm. V · Part 3.3 §3.3.3.2 + §3.3.7';

CREATE TABLE ge.com_quote (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  is_simulated boolean NOT NULL DEFAULT false,
  run_id uuid,
  correlation_id uuid,
  deal_id uuid NOT NULL,
  proposal_version_id uuid,
  quote_no text NOT NULL,
  quote_revision integer NOT NULL DEFAULT 1,
  currency char(3) NOT NULL,
  subtotal_amount numeric(18,2) NOT NULL DEFAULT 0,
  discount_amount numeric(18,2) NOT NULL DEFAULT 0,
  tax_amount numeric(18,2) NOT NULL DEFAULT 0,
  total_amount numeric(18,2) NOT NULL DEFAULT 0,
  max_discount_pct numeric(7,4) NOT NULL DEFAULT 0,
  margin_pct numeric(7,4),
  tax_regime text NOT NULL,
  place_of_supply text,
  valid_until date NOT NULL,
  content_hash char(64),
  state text NOT NULL DEFAULT 'draft',
  accepted_at text,
  accepted_by_ref text,
  schema_ref text,
  evidence_refs uuid[] NOT NULL DEFAULT '{}',
  payload jsonb NOT NULL,
  CONSTRAINT pk_com_quote PRIMARY KEY (id),
  CONSTRAINT uq_com_quote__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_com_quote__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.com_quote IS 'ENT-127 Quote · scope S · Imm. F · Part 3.3 §3.3.3.2';

CREATE TABLE ge.com_quote_line (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  is_simulated boolean NOT NULL DEFAULT false,
  run_id uuid,
  correlation_id uuid,
  quote_id uuid NOT NULL,
  line_no smallint NOT NULL,
  offering_version_id uuid NOT NULL,
  price_version_id uuid NOT NULL,
  description text NOT NULL,
  quantity numeric(18,4) NOT NULL,
  unit_code text NOT NULL,
  unit_price numeric(18,4) NOT NULL,
  discount_pct numeric(7,4) NOT NULL DEFAULT 0,
  line_total numeric(18,2) NOT NULL,
  hsn_sac_code text,
  tax_rate_pct numeric(7,4) NOT NULL DEFAULT 0,
  tax_amount numeric(18,2) NOT NULL DEFAULT 0,
  schema_ref text,
  evidence_refs uuid[] NOT NULL DEFAULT '{}',
  payload jsonb NOT NULL,
  CONSTRAINT pk_com_quote_line PRIMARY KEY (id),
  CONSTRAINT uq_com_quote_line__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_com_quote_line__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.com_quote_line IS 'ENT-128 QuoteLine · scope S · Imm. F · Part 3.3 §3.3.3.2';

CREATE TABLE ge.com_objection (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  is_simulated boolean NOT NULL DEFAULT false,
  run_id uuid,
  correlation_id uuid,
  deal_id uuid,
  negotiation_id uuid,
  category_code text,
  raised_text text,
  approved_answer_ref text,
  state text,
  resolved_at timestamptz,
  schema_ref text,
  evidence_refs uuid[] NOT NULL DEFAULT '{}',
  payload jsonb NOT NULL,
  CONSTRAINT pk_com_objection PRIMARY KEY (id),
  CONSTRAINT uq_com_objection__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_com_objection__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.com_objection IS 'ENT-129 Objection · scope S · Imm. M · Part 3.3 §3.3.3.2 + §3.3.7';

CREATE TABLE ge.com_negotiation (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  is_simulated boolean NOT NULL DEFAULT false,
  run_id uuid,
  correlation_id uuid,
  deal_id uuid,
  concession_limit_pct numeric(7,4),
  exception_requested text,
  exception_approval_id uuid,
  state text,
  schema_ref text,
  evidence_refs uuid[] NOT NULL DEFAULT '{}',
  payload jsonb NOT NULL,
  CONSTRAINT pk_com_negotiation PRIMARY KEY (id),
  CONSTRAINT uq_com_negotiation__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_com_negotiation__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.com_negotiation IS 'ENT-130 Negotiation · scope S · Imm. M · Part 3.3 §3.3.3.2 + §3.3.7';

CREATE TABLE ge.com_contract (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  is_simulated boolean NOT NULL DEFAULT false,
  run_id uuid,
  correlation_id uuid,
  deal_id uuid NOT NULL,
  quote_id uuid,
  contract_no text NOT NULL,
  contract_kind text NOT NULL,
  template_ref uuid NOT NULL,
  has_deviation boolean NOT NULL DEFAULT false,
  contract_value numeric(18,2),
  currency char(3),
  is_cross_border boolean NOT NULL DEFAULT false,
  document_storage_key text NOT NULL,
  approved_hash char(64),
  signed_hash char(64),
  state text NOT NULL DEFAULT 'drafting',
  term_start date,
  term_end date,
  renewal_notice_days smallint NOT NULL DEFAULT 60,
  esign_provider text,
  schema_ref text,
  evidence_refs uuid[] NOT NULL DEFAULT '{}',
  payload jsonb NOT NULL,
  CONSTRAINT pk_com_contract PRIMARY KEY (id),
  CONSTRAINT uq_com_contract__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_com_contract__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.com_contract IS 'ENT-131 Contract · scope S · Imm. F · Part 3.3 §3.3.3.2';

CREATE TABLE ge.com_signature_event (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  correlation_id uuid,
  contract_id uuid NOT NULL,
  party_side text NOT NULL,
  signer_name text NOT NULL,
  signer_authority_ref text NOT NULL,
  method text NOT NULL,
  document_hash char(64) NOT NULL,
  provider_account text,
  provider_event_id text,
  signed_at timestamptz NOT NULL,
  evidence_storage_key text,
  CONSTRAINT pk_com_signature_event PRIMARY KEY (id),
  CONSTRAINT uq_com_signature_event__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_com_signature_event__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.com_signature_event IS 'ENT-132 SignatureEvent · scope S · Imm. A · Part 3.3 §3.3.3.2';

CREATE TABLE ge.com_bid (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  is_simulated boolean NOT NULL DEFAULT false,
  run_id uuid,
  correlation_id uuid,
  deal_id uuid NOT NULL,
  tender_ref text NOT NULL,
  portal_code text NOT NULL,
  organization_id uuid NOT NULL,
  technology_codes text[] NOT NULL DEFAULT '{}',
  deadline_utc timestamptz NOT NULL,
  portal_timezone text NOT NULL,
  submission_buffer_hours smallint NOT NULL DEFAULT 24,
  delivery_model text,
  budget_amount numeric(18,2),
  currency char(3),
  eligibility_result text NOT NULL DEFAULT 'not_evaluated',
  state text NOT NULL DEFAULT 'identified',
  submitted_by uuid,
  submission_ref text,
  submitted_at text,
  receipt_hash text,
  award_evidence_ref text,
  schema_ref text,
  evidence_refs uuid[] NOT NULL DEFAULT '{}',
  payload jsonb NOT NULL,
  CONSTRAINT pk_com_bid PRIMARY KEY (id),
  CONSTRAINT uq_com_bid__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_com_bid__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.com_bid IS 'ENT-133 Bid · scope S · Imm. M · Part 3.3 §3.3.3.2';

CREATE TABLE ge.com_bid_checklist_item (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  is_simulated boolean NOT NULL DEFAULT false,
  run_id uuid,
  correlation_id uuid,
  bid_id uuid,
  criterion_code text,
  result text,
  evidence_ref text,
  waiver_approval_id uuid,
  CONSTRAINT pk_com_bid_checklist_item PRIMARY KEY (id),
  CONSTRAINT uq_com_bid_checklist_item__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_com_bid_checklist_item__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.com_bid_checklist_item IS 'ENT-134 BidChecklistItem · scope S · Imm. M · Part 3.3 §3.3.3.2 + §3.3.7';

CREATE TABLE ge.com_order (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  is_simulated boolean NOT NULL DEFAULT false,
  run_id uuid,
  correlation_id uuid,
  order_no text NOT NULL,
  direction text NOT NULL,
  deal_id uuid,
  counterparty_org_id uuid NOT NULL,
  currency char(3) NOT NULL,
  total_amount numeric(18,2) NOT NULL DEFAULT 0,
  tax_amount numeric(18,2) NOT NULL DEFAULT 0,
  state text NOT NULL DEFAULT 'draft',
  acceptance_deadline date,
  delivery_region text,
  over_delivery_tolerance_pct numeric(7,4) NOT NULL DEFAULT 0,
  schema_ref text,
  evidence_refs uuid[] NOT NULL DEFAULT '{}',
  payload jsonb NOT NULL,
  CONSTRAINT pk_com_order PRIMARY KEY (id),
  CONSTRAINT uq_com_order__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_com_order__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.com_order IS 'ENT-135 Order · scope S · Imm. F · Part 3.3 §3.3.3.2';

CREATE TABLE ge.com_order_line (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  is_simulated boolean NOT NULL DEFAULT false,
  run_id uuid,
  correlation_id uuid,
  order_id uuid NOT NULL,
  line_no smallint NOT NULL,
  sku_code text NOT NULL,
  offering_version_id uuid,
  price_version_id uuid,
  quantity numeric(18,4) NOT NULL,
  unit_code text NOT NULL,
  unit_price numeric(18,4) NOT NULL,
  line_total numeric(18,2) NOT NULL,
  fulfilled_qty numeric(18,4) NOT NULL DEFAULT 0,
  accepted_qty numeric(18,4) NOT NULL DEFAULT 0,
  certification_ref text,
  schema_ref text,
  evidence_refs uuid[] NOT NULL DEFAULT '{}',
  payload jsonb NOT NULL,
  CONSTRAINT pk_com_order_line PRIMARY KEY (id),
  CONSTRAINT uq_com_order_line__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_com_order_line__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.com_order_line IS 'ENT-136 OrderLine · scope S · Imm. F · Part 3.3 §3.3.3.2';

CREATE TABLE ge.com_fulfillment_event (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  correlation_id uuid,
  order_line_id uuid NOT NULL,
  event_key text NOT NULL,
  event_type text NOT NULL,
  quantity numeric(18,4) NOT NULL,
  unit_code text NOT NULL,
  occurred_at timestamptz NOT NULL,
  evidence_ref text,
  reverses_id uuid,
  schema_ref text,
  evidence_refs uuid[] NOT NULL DEFAULT '{}',
  payload jsonb NOT NULL,
  CONSTRAINT pk_com_fulfillment_event PRIMARY KEY (id),
  CONSTRAINT uq_com_fulfillment_event__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_com_fulfillment_event__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.com_fulfillment_event IS 'ENT-137 FulfillmentEvent · scope S · Imm. A · Part 3.3 §3.3.3.2';

CREATE TABLE ge.com_sku_availability (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  is_simulated boolean NOT NULL DEFAULT false,
  run_id uuid,
  correlation_id uuid,
  sku_code text,
  offering_version_id uuid,
  availability_status text,
  available_qty numeric(18,4),
  reserved_qty numeric(18,4),
  unit_code text,
  CONSTRAINT pk_com_sku_availability PRIMARY KEY (id),
  CONSTRAINT uq_com_sku_availability__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_com_sku_availability__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.com_sku_availability IS 'ENT-138 SkuAvailability · scope S · Imm. M · Part 3.3 §3.3.3.2 + §3.3.7';

CREATE TABLE ge.com_inventory_reservation (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  is_simulated boolean NOT NULL DEFAULT false,
  run_id uuid,
  correlation_id uuid,
  sku_availability_id uuid,
  order_line_id uuid,
  quantity numeric(18,4),
  state text,
  expires_at timestamptz,
  CONSTRAINT pk_com_inventory_reservation PRIMARY KEY (id),
  CONSTRAINT uq_com_inventory_reservation__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_com_inventory_reservation__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.com_inventory_reservation IS 'ENT-139 InventoryReservation · scope S · Imm. M · Part 3.3 §3.3.3.2 + §3.3.7';

CREATE TABLE ge.com_invoice (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  is_simulated boolean NOT NULL DEFAULT false,
  run_id uuid,
  correlation_id uuid,
  invoice_no text NOT NULL,
  invoice_kind text NOT NULL,
  deal_id uuid,
  order_id uuid,
  contract_id uuid,
  bill_to_org_id uuid NOT NULL,
  currency char(3) NOT NULL,
  subtotal_amount numeric(18,2) NOT NULL DEFAULT 0,
  tax_amount numeric(18,2) NOT NULL DEFAULT 0,
  total_amount numeric(18,2) NOT NULL DEFAULT 0,
  issue_date date,
  due_date date,
  irn_external text,
  state text NOT NULL DEFAULT 'invoice_draft',
  maker_approval_id uuid,
  checker_approval_id uuid,
  amount_allocated numeric(18,2) NOT NULL DEFAULT 0,
  credits_invoice_id uuid,
  schema_ref text,
  evidence_refs uuid[] NOT NULL DEFAULT '{}',
  payload jsonb NOT NULL,
  CONSTRAINT pk_com_invoice PRIMARY KEY (id),
  CONSTRAINT uq_com_invoice__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_com_invoice__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.com_invoice IS 'ENT-140 Invoice · scope S · Imm. F · Part 3.3 §3.3.3.2';

CREATE TABLE ge.com_invoice_line (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  is_simulated boolean NOT NULL DEFAULT false,
  run_id uuid,
  correlation_id uuid,
  invoice_id uuid,
  line_no integer,
  source_type text,
  source_id uuid,
  description text,
  quantity numeric(18,4),
  unit_price numeric(18,2),
  discount_pct numeric(7,4),
  line_total numeric(18,2),
  hsn_sac_code text,
  tax_rate_pct numeric(7,4),
  tax_amount numeric(18,2),
  tax_split jsonb,
  CONSTRAINT pk_com_invoice_line PRIMARY KEY (id),
  CONSTRAINT uq_com_invoice_line__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_com_invoice_line__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.com_invoice_line IS 'ENT-141 InvoiceLine · scope S · Imm. F · Part 3.3 §3.3.3.2 + §3.3.7';

CREATE TABLE ge.com_payment (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  is_simulated boolean NOT NULL DEFAULT false,
  run_id uuid,
  correlation_id uuid,
  direction text NOT NULL DEFAULT 'inbound',
  method text NOT NULL,
  provider_account text NOT NULL,
  provider_payment_id text NOT NULL,
  amount numeric(18,2) NOT NULL,
  currency char(3) NOT NULL,
  payer_legal_name text,
  payer_org_id uuid,
  reference_text text,
  received_at timestamptz NOT NULL,
  evidence_storage_key text,
  state text NOT NULL DEFAULT 'evidence_received',
  maker_id uuid,
  checker_id uuid,
  outcome_certainty text,
  is_saas_fee boolean NOT NULL DEFAULT false,
  schema_ref text,
  evidence_refs uuid[] NOT NULL DEFAULT '{}',
  payload jsonb NOT NULL,
  CONSTRAINT pk_com_payment PRIMARY KEY (id),
  CONSTRAINT uq_com_payment__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_com_payment__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.com_payment IS 'ENT-142 Payment · scope S · Imm. F · Part 3.3 §3.3.3.2';

CREATE TABLE ge.com_payment_allocation (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  correlation_id uuid,
  payment_id uuid NOT NULL,
  invoice_id uuid NOT NULL,
  amount numeric(18,2) NOT NULL,
  reverses_id uuid,
  CONSTRAINT pk_com_payment_allocation PRIMARY KEY (id),
  CONSTRAINT uq_com_payment_allocation__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_com_payment_allocation__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.com_payment_allocation IS 'ENT-143 PaymentAllocation · scope S · Imm. A · Part 3.3 §3.3.3.2';

CREATE TABLE ge.com_discrepancy_case (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  is_simulated boolean NOT NULL DEFAULT false,
  run_id uuid,
  correlation_id uuid,
  payment_id uuid,
  invoice_id uuid,
  discrepancy_type text,
  expected jsonb,
  observed jsonb,
  state text,
  resolution text,
  CONSTRAINT pk_com_discrepancy_case PRIMARY KEY (id),
  CONSTRAINT uq_com_discrepancy_case__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_com_discrepancy_case__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.com_discrepancy_case IS 'ENT-144 DiscrepancyCase · scope S · Imm. M · Part 3.3 §3.3.3.2 + §3.3.7';

CREATE TABLE ge.com_receivable_entry (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  correlation_id uuid,
  counterparty_org_id uuid NOT NULL,
  entry_type text NOT NULL,
  amount numeric(18,2) NOT NULL,
  currency char(3) NOT NULL,
  source_type text NOT NULL,
  source_id text NOT NULL,
  posting_date date NOT NULL,
  due_date date,
  reverses_id uuid,
  reason text,
  entry_seq bigint NOT NULL,
  CONSTRAINT pk_com_receivable_entry PRIMARY KEY (id),
  CONSTRAINT uq_com_receivable_entry__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_com_receivable_entry__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.com_receivable_entry IS 'ENT-145 ReceivableEntry · scope S · Imm. A · Part 3.3 §3.3.3.2';

CREATE TABLE ge.com_payable_entry (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  correlation_id uuid,
  counterparty_org_id uuid NOT NULL,
  entry_type text NOT NULL,
  amount numeric(18,2) NOT NULL,
  currency char(3) NOT NULL,
  source_type text NOT NULL,
  source_id text NOT NULL,
  posting_date date NOT NULL,
  due_date date,
  reverses_id uuid,
  reason text,
  entry_seq bigint NOT NULL,
  CONSTRAINT pk_com_payable_entry PRIMARY KEY (id),
  CONSTRAINT uq_com_payable_entry__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_com_payable_entry__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.com_payable_entry IS 'ENT-146 PayableEntry · scope S · Imm. A · Part 3.3 §3.3.3.2';

CREATE TABLE ge.lcy_onboarding (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  is_simulated boolean NOT NULL DEFAULT false,
  run_id uuid,
  correlation_id uuid,
  deal_id uuid,
  offering_id uuid,
  template_ref text,
  state text,
  sla_due_at timestamptz,
  mandatory_open_count integer,
  schema_ref text,
  evidence_refs uuid[] NOT NULL DEFAULT '{}',
  payload jsonb NOT NULL,
  CONSTRAINT pk_lcy_onboarding PRIMARY KEY (id),
  CONSTRAINT uq_lcy_onboarding__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_lcy_onboarding__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.lcy_onboarding IS 'ENT-147 Onboarding · scope S · Imm. M · Part 3.3 §3.3.3.2 + §3.3.7';

CREATE TABLE ge.lcy_task (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  is_simulated boolean NOT NULL DEFAULT false,
  run_id uuid,
  correlation_id uuid,
  subject_type text,
  subject_id uuid,
  title text,
  assignee_id uuid,
  due_at timestamptz,
  priority integer,
  state text,
  is_mandatory boolean,
  source text,
  schema_ref text,
  evidence_refs uuid[] NOT NULL DEFAULT '{}',
  payload jsonb NOT NULL,
  CONSTRAINT pk_lcy_task PRIMARY KEY (id),
  CONSTRAINT uq_lcy_task__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_lcy_task__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.lcy_task IS 'ENT-148 Task · scope S · Imm. M · Part 3.3 §3.3.3.2 + §3.3.7';

CREATE TABLE ge.lcy_handoff (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  correlation_id uuid,
  onboarding_id uuid,
  from_owner_id uuid,
  to_owner_id uuid,
  checklist jsonb,
  handed_off_at timestamptz,
  CONSTRAINT pk_lcy_handoff PRIMARY KEY (id),
  CONSTRAINT uq_lcy_handoff__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_lcy_handoff__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.lcy_handoff IS 'ENT-149 Handoff · scope S · Imm. A · Part 3.3 §3.3.3.2 + §3.3.7';

CREATE TABLE ge.lcy_renewal (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  is_simulated boolean NOT NULL DEFAULT false,
  run_id uuid,
  correlation_id uuid,
  customer_subscription_id uuid,
  contract_id uuid,
  due_date date,
  state text,
  risk_score numeric(9,4),
  outcome_id uuid,
  schema_ref text,
  evidence_refs uuid[] NOT NULL DEFAULT '{}',
  payload jsonb NOT NULL,
  CONSTRAINT pk_lcy_renewal PRIMARY KEY (id),
  CONSTRAINT uq_lcy_renewal__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_lcy_renewal__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.lcy_renewal IS 'ENT-150 Renewal · scope S · Imm. M · Part 3.3 §3.3.3.2 + §3.3.7';

CREATE TABLE ge.lcy_customer_subscription (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  is_simulated boolean NOT NULL DEFAULT false,
  run_id uuid,
  correlation_id uuid,
  contract_id uuid,
  organization_id uuid,
  offering_id uuid,
  start_date date,
  end_date date,
  billing_terms jsonb,
  state text,
  CONSTRAINT pk_lcy_customer_subscription PRIMARY KEY (id),
  CONSTRAINT uq_lcy_customer_subscription__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_lcy_customer_subscription__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.lcy_customer_subscription IS 'ENT-151 CustomerSubscription (FRD "Subscription", M50) · scope S · Imm. M · Part 3.3 §3.3.3.2 + §3.3.7';

CREATE TABLE ge.lcy_account_metric (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  correlation_id uuid,
  organization_id uuid,
  metric_code text,
  value text,
  as_of_date date,
  source text,
  CONSTRAINT pk_lcy_account_metric PRIMARY KEY (id),
  CONSTRAINT uq_lcy_account_metric__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_lcy_account_metric__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.lcy_account_metric IS 'ENT-152 AccountMetric · scope S · Imm. A · Part 3.3 §3.3.3.2 + §3.3.7';

CREATE TABLE ge.lcy_partner (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  is_simulated boolean NOT NULL DEFAULT false,
  run_id uuid,
  correlation_id uuid,
  organization_id uuid,
  partner_type text,
  due_diligence_state text,
  agreement_contract_id uuid,
  schema_ref text,
  evidence_refs uuid[] NOT NULL DEFAULT '{}',
  payload jsonb NOT NULL,
  CONSTRAINT pk_lcy_partner PRIMARY KEY (id),
  CONSTRAINT uq_lcy_partner__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_lcy_partner__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.lcy_partner IS 'ENT-153 Partner · scope S · Imm. M · Part 3.3 §3.3.3.2 + §3.3.7';

CREATE TABLE ge.lcy_pilot (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  is_simulated boolean NOT NULL DEFAULT false,
  run_id uuid,
  correlation_id uuid,
  partner_id uuid,
  pilot_type text,
  state text,
  readiness_approval_id uuid,
  data_restrictions jsonb,
  schema_ref text,
  evidence_refs uuid[] NOT NULL DEFAULT '{}',
  payload jsonb NOT NULL,
  CONSTRAINT pk_lcy_pilot PRIMARY KEY (id),
  CONSTRAINT uq_lcy_pilot__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_lcy_pilot__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.lcy_pilot IS 'ENT-154 Pilot · scope S · Imm. M · Part 3.3 §3.3.3.2 + §3.3.7';

CREATE TABLE ge.lcy_deployment (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  is_simulated boolean NOT NULL DEFAULT false,
  run_id uuid,
  correlation_id uuid,
  pilot_id uuid,
  partner_id uuid,
  location_ref text,
  readiness_checklist jsonb,
  state text,
  go_live_date date,
  schema_ref text,
  evidence_refs uuid[] NOT NULL DEFAULT '{}',
  payload jsonb NOT NULL,
  CONSTRAINT pk_lcy_deployment PRIMARY KEY (id),
  CONSTRAINT uq_lcy_deployment__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_lcy_deployment__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.lcy_deployment IS 'ENT-155 Deployment · scope S · Imm. M · Part 3.3 §3.3.3.2 + §3.3.7';

CREATE TABLE ge.lcy_integration_deal (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  is_simulated boolean NOT NULL DEFAULT false,
  run_id uuid,
  correlation_id uuid,
  partner_id uuid,
  api_capabilities jsonb,
  technical_review_state text,
  legal_review_state text,
  contract_id uuid,
  state text,
  schema_ref text,
  evidence_refs uuid[] NOT NULL DEFAULT '{}',
  payload jsonb NOT NULL,
  CONSTRAINT pk_lcy_integration_deal PRIMARY KEY (id),
  CONSTRAINT uq_lcy_integration_deal__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_lcy_integration_deal__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.lcy_integration_deal IS 'ENT-156 IntegrationDeal (licensing enquiry) · scope S · Imm. M · Part 3.3 §3.3.3.2 + §3.3.7';

CREATE TABLE ge.lcy_feedback (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  correlation_id uuid,
  feedback_kind text,
  subject_type text,
  subject_id uuid,
  category_code text,
  body_redacted text,
  contact_id uuid,
  CONSTRAINT pk_lcy_feedback PRIMARY KEY (id),
  CONSTRAINT uq_lcy_feedback__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_lcy_feedback__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.lcy_feedback IS 'ENT-157 Feedback (customer / loss feedback) · scope S · Imm. A · Part 3.3 §3.3.3.2 + §3.3.7';

CREATE TABLE ge.lcy_outcome (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  correlation_id uuid,
  subject_type text,
  subject_id uuid,
  outcome_code text,
  loss_reason_code text,
  learning_actions jsonb,
  recorded_at timestamptz,
  CONSTRAINT pk_lcy_outcome PRIMARY KEY (id),
  CONSTRAINT uq_lcy_outcome__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_lcy_outcome__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.lcy_outcome IS 'ENT-158 Outcome · scope S · Imm. A · Part 3.3 §3.3.3.2 + §3.3.7';

CREATE TABLE ge.aut_workflow (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  workflow_code text NOT NULL,
  name text NOT NULL,
  objective_code text,
  autonomy_mode text NOT NULL DEFAULT 'L1',
  active_revision_id uuid,
  is_paused boolean NOT NULL DEFAULT false,
  max_concurrent_runs smallint NOT NULL DEFAULT 20,
  CONSTRAINT pk_aut_workflow PRIMARY KEY (id),
  CONSTRAINT uq_aut_workflow__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_aut_workflow__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.aut_workflow IS 'ENT-159 Workflow · scope S · Imm. M · Part 3.3 §3.3.3.2';

CREATE TABLE ge.aut_workflow_revision (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  version_no integer NOT NULL DEFAULT 1,
  status text NOT NULL DEFAULT 'draft',
  content_hash char(64),
  approval_id uuid,
  approved_at timestamptz,
  effective_from timestamptz,
  effective_to timestamptz,
  supersedes_id uuid,
  workflow_id uuid NOT NULL,
  template_id text,
  template_version text,
  dag_spec jsonb NOT NULL,
  spec_hash char(64) NOT NULL,
  contains_secret boolean NOT NULL DEFAULT false,
  max_steps smallint NOT NULL DEFAULT 50,
  simulation_run_id uuid,
  CONSTRAINT pk_aut_workflow_revision PRIMARY KEY (id),
  CONSTRAINT uq_aut_workflow_revision__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_aut_workflow_revision__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.aut_workflow_revision IS 'ENT-160 WorkflowRevision · scope S · Imm. V · Part 3.3 §3.3.3.2';

CREATE TABLE ge.aut_trigger (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  trigger_kind text NOT NULL,
  event_type text,
  event_schema_version smallint,
  schedule_cron text,
  timezone text NOT NULL,
  condition jsonb,
  workflow_revision_id uuid NOT NULL,
  dedup_window_s integer NOT NULL DEFAULT 300,
  credential_ref_id uuid,
  state text NOT NULL DEFAULT 'draft',
  last_fired_at timestamptz,
  next_fire_at timestamptz,
  CONSTRAINT pk_aut_trigger PRIMARY KEY (id),
  CONSTRAINT uq_aut_trigger__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_aut_trigger__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.aut_trigger IS 'ENT-161 Trigger · scope S · Imm. M · Part 3.3 §3.3.3.2';

CREATE TABLE ge.aut_autonomy_plan (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  is_simulated boolean NOT NULL DEFAULT false,
  run_id uuid,
  correlation_id uuid,
  objective_code text,
  mode text,
  plan_revision text,
  template_ids uuid[],
  concurrency_limit text,
  budget_cap numeric(18,2),
  simulation_cost numeric(18,2),
  stop_policy jsonb,
  approval_id uuid,
  state text,
  expires_at timestamptz,
  CONSTRAINT pk_aut_autonomy_plan PRIMARY KEY (id),
  CONSTRAINT uq_aut_autonomy_plan__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_aut_autonomy_plan__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.aut_autonomy_plan IS 'ENT-164 AutonomyPlan (autonomous commercial plan) · scope S · Imm. M · Part 3.3 §3.3.3.2 + §3.3.7';

CREATE TABLE ge.aut_conflict_case (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  relationship_ref text,
  action_type text,
  duplicate_key text,
  priority_rule text,
  frequency_count integer,
  budget_reservation_id uuid,
  resolution text,
  reviewer_id uuid,
  state text,
  CONSTRAINT pk_aut_conflict_case PRIMARY KEY (id),
  CONSTRAINT uq_aut_conflict_case__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_aut_conflict_case__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.aut_conflict_case IS 'ENT-165 ConflictCase · scope S · Imm. M · Part 3.3 §3.3.3.2 + §3.3.7';

CREATE TABLE ge.aut_node_template (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid,
  startup_id uuid,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  version_no integer NOT NULL DEFAULT 1,
  status text NOT NULL DEFAULT 'draft',
  content_hash char(64),
  approval_id uuid,
  approved_at timestamptz,
  effective_from timestamptz,
  effective_to timestamptz,
  supersedes_id uuid,
  node_type text,
  input_schema jsonb,
  output_schema jsonb,
  side_effect_class text,
  required_permissions text,
  risk_class text,
  allowed_channels text,
  cost_estimate numeric(18,2),
  CONSTRAINT pk_aut_node_template PRIMARY KEY (id),
  CONSTRAINT uq_aut_node_template__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_aut_node_template__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.aut_node_template IS 'ENT-166 NodeTemplate · scope X · Imm. V · Part 3.3 §3.3.3.2 + §3.3.7';

CREATE TABLE ge.aut_workflow_template (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid,
  startup_id uuid,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  version_no integer NOT NULL DEFAULT 1,
  status text NOT NULL DEFAULT 'draft',
  content_hash char(64),
  approval_id uuid,
  approved_at timestamptz,
  effective_from timestamptz,
  effective_to timestamptz,
  supersedes_id uuid,
  template_code text,
  business_capability text,
  objective text,
  node_types text,
  test_fixtures jsonb,
  deprecation_status text,
  CONSTRAINT pk_aut_workflow_template PRIMARY KEY (id),
  CONSTRAINT uq_aut_workflow_template__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_aut_workflow_template__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.aut_workflow_template IS 'ENT-167 WorkflowTemplate · scope X · Imm. V · Part 3.3 §3.3.3.2 + §3.3.7';

CREATE TABLE ge.aut_config_revision (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid,
  startup_id uuid,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  version_no integer NOT NULL DEFAULT 1,
  status text NOT NULL DEFAULT 'draft',
  content_hash char(64),
  approval_id uuid,
  approved_at timestamptz,
  effective_from timestamptz,
  effective_to timestamptz,
  supersedes_id uuid,
  config_key text NOT NULL,
  target_type text,
  target_id text,
  active_snapshot jsonb,
  candidate jsonb NOT NULL,
  diff jsonb NOT NULL,
  is_loosening boolean NOT NULL,
  impact_report jsonb,
  simulation_report jsonb,
  effective_at timestamptz,
  rollback_of_id uuid,
  CONSTRAINT pk_aut_config_revision PRIMARY KEY (id),
  CONSTRAINT uq_aut_config_revision__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_aut_config_revision__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.aut_config_revision IS 'ENT-168 ConfigRevision · scope X · Imm. V · Part 3.3 §3.3.3.2';

CREATE TABLE ge.ops_domain_event (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  correlation_id uuid,
  event_type text,
  schema_version text,
  aggregate_type text,
  aggregate_id uuid,
  aggregate_revision text,
  payload jsonb,
  occurred_at timestamptz,
  global_seq bigint,
  CONSTRAINT pk_ops_domain_event PRIMARY KEY (id),
  CONSTRAINT uq_ops_domain_event__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_ops_domain_event__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.ops_domain_event IS 'ENT-170 DomainEvent · scope S · Imm. A · Part 3.3 §3.3.3.2 + §3.3.7';

CREATE TABLE ge.ops_idempotency_key (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  scope_key text,
  key_value text,
  body_hash char(64),
  response_status text,
  response_ref text,
  expires_at timestamptz,
  CONSTRAINT pk_ops_idempotency_key PRIMARY KEY (id),
  CONSTRAINT uq_ops_idempotency_key__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_ops_idempotency_key__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.ops_idempotency_key IS 'ENT-171 IdempotencyKey · scope S · Imm. F · Part 3.3 §3.3.3.2 + §3.3.7';

CREATE TABLE ge.ops_job_run (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid,
  startup_id uuid,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  job_name text,
  queue text,
  state text,
  attempt integer,
  scope jsonb,
  error_class text,
  started_at timestamptz,
  finished_at timestamptz,
  CONSTRAINT pk_ops_job_run PRIMARY KEY (id),
  CONSTRAINT uq_ops_job_run__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_ops_job_run__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.ops_job_run IS 'ENT-173 JobRun · scope X · Imm. M · Part 3.3 §3.3.3.2 + §3.3.7';

CREATE TABLE ge.ops_notification (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  recipient_id uuid,
  severity text,
  category text,
  title text,
  action_link text,
  event_ref text,
  run_id uuid,
  dedup_key text,
  due_at timestamptz,
  acknowledged_at timestamptz,
  state text,
  CONSTRAINT pk_ops_notification PRIMARY KEY (id),
  CONSTRAINT uq_ops_notification__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_ops_notification__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.ops_notification IS 'ENT-174 Notification · scope S · Imm. M · Part 3.3 §3.3.3.2 + §3.3.7';

CREATE TABLE ge.ops_notification_preference (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  user_id uuid,
  category text,
  digest_mode text,
  channel text,
  CONSTRAINT pk_ops_notification_preference PRIMARY KEY (id),
  CONSTRAINT uq_ops_notification_preference__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_ops_notification_preference__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.ops_notification_preference IS 'ENT-175 NotificationPreference · scope T · Imm. M · Part 3.3 §3.3.3.2 + §3.3.7';

CREATE TABLE ge.ops_release (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  updated_at timestamptz NOT NULL DEFAULT now(),
  version_tag text,
  state text,
  gate_results jsonb,
  evidence_refs text,
  approved_by text,
  deployed_at timestamptz,
  rollback_of text,
  CONSTRAINT pk_ops_release PRIMARY KEY (id)
);

COMMENT ON TABLE ge.ops_release IS 'ENT-177 Release · scope P · Imm. M · Part 3.3 §3.3.3.2 + §3.3.7';

CREATE TABLE ge.ops_test_run (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  updated_at timestamptz NOT NULL DEFAULT now(),
  release_id uuid,
  suite text,
  result jsonb,
  report_key text,
  executed_at timestamptz,
  CONSTRAINT pk_ops_test_run PRIMARY KEY (id)
);

COMMENT ON TABLE ge.ops_test_run IS 'ENT-178 TestRun · scope P · Imm. A · Part 3.3 §3.3.3.2 + §3.3.7';

CREATE TABLE ge.saas_plan (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  updated_at timestamptz NOT NULL DEFAULT now(),
  archetype text NOT NULL,
  code text NOT NULL,
  state text NOT NULL DEFAULT 'draft',
  current_version_id uuid,
  CONSTRAINT pk_saas_plan PRIMARY KEY (id)
);

COMMENT ON TABLE ge.saas_plan IS 'ENT-179 ServicePlan (DEC-016 "Plan") · scope P · Imm. M · Part 3.3 §3.3.3.2';

CREATE TABLE ge.saas_plan_version (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  updated_at timestamptz NOT NULL DEFAULT now(),
  version_no integer NOT NULL DEFAULT 1,
  status text NOT NULL DEFAULT 'draft',
  content_hash char(64),
  approval_id uuid,
  approved_at timestamptz,
  effective_from timestamptz,
  effective_to timestamptz,
  supersedes_id uuid,
  plan_id uuid,
  base_fee numeric(18,2),
  currency char(3),
  billing_cycle text,
  trial_days integer,
  published_price boolean,
  CONSTRAINT pk_saas_plan_version PRIMARY KEY (id)
);

COMMENT ON TABLE ge.saas_plan_version IS 'ENT-180 PlanVersion · scope P · Imm. V · Part 3.3 §3.3.3.2 + §3.3.7';

CREATE TABLE ge.saas_entitlement (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid,
  startup_id uuid,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  version_no integer NOT NULL DEFAULT 1,
  status text NOT NULL DEFAULT 'draft',
  content_hash char(64),
  approval_id uuid,
  approved_at timestamptz,
  effective_from timestamptz,
  effective_to timestamptz,
  supersedes_id uuid,
  meter_code text NOT NULL,
  included_qty numeric(18,4) NOT NULL,
  period text NOT NULL DEFAULT 'month',
  overage_mode text NOT NULL DEFAULT 'block',
  overage_unit_price numeric(18,4),
  trial_qty numeric(18,4),
  CONSTRAINT pk_saas_entitlement PRIMARY KEY (id),
  CONSTRAINT uq_saas_entitlement__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_saas_entitlement__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.saas_entitlement IS 'ENT-181 Entitlement · scope X · Imm. V · Part 3.3 §3.3.3.2';

CREATE TABLE ge.saas_subscription (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  plan_version_id uuid NOT NULL,
  state text NOT NULL DEFAULT 'trial',
  trial_ends_at timestamptz,
  billing_cycle text NOT NULL DEFAULT 'monthly',
  current_period_start date NOT NULL,
  current_period_end date NOT NULL,
  currency char(3) NOT NULL DEFAULT 'INR',
  budget_limit numeric(18,2),
  suspension_reason text,
  CONSTRAINT pk_saas_subscription PRIMARY KEY (id),
  CONSTRAINT uq_saas_subscription__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_saas_subscription__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.saas_subscription IS 'ENT-182 ServiceSubscription · scope T · Imm. M · Part 3.3 §3.3.3.2';

CREATE TABLE ge.saas_usage_meter_reading (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  correlation_id uuid,
  subscription_id uuid NOT NULL,
  meter_code text NOT NULL,
  period_start timestamptz NOT NULL,
  period_end timestamptz NOT NULL,
  quantity numeric(18,4) NOT NULL,
  source_watermark text NOT NULL,
  source_count_digest char(64) NOT NULL,
  invoice_line_id uuid,
  correction_of_id uuid,
  CONSTRAINT pk_saas_usage_meter_reading PRIMARY KEY (id),
  CONSTRAINT uq_saas_usage_meter_reading__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_saas_usage_meter_reading__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.saas_usage_meter_reading IS 'ENT-183 UsageMeterReading · scope T · Imm. A · Part 3.3 §3.3.3.2';

CREATE TABLE ge.saas_service_invoice_line (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  service_invoice_id uuid,
  line_kind text,
  meter_code text,
  quantity numeric(18,4),
  unit_price numeric(18,2),
  amount numeric(18,2),
  reading_count integer,
  readings_digest text,
  CONSTRAINT pk_saas_service_invoice_line PRIMARY KEY (id),
  CONSTRAINT uq_saas_service_invoice_line__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_saas_service_invoice_line__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.saas_service_invoice_line IS 'ENT-185 ServiceInvoiceLine · scope T · Imm. F · Part 3.3 §3.3.3.2 + §3.3.7';

CREATE TABLE ge.saas_credit (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  correlation_id uuid,
  subscription_id uuid,
  amount numeric(18,2),
  currency char(3),
  reason_code text,
  approval_id uuid,
  applied_invoice_id uuid,
  reverses_id uuid,
  CONSTRAINT pk_saas_credit PRIMARY KEY (id),
  CONSTRAINT uq_saas_credit__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_saas_credit__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.saas_credit IS 'ENT-186 Credit (credit/adjustment) · scope T · Imm. A · Part 3.3 §3.3.3.2 + §3.3.7';

CREATE TABLE ge.saas_application_draft (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  updated_at timestamptz NOT NULL DEFAULT now(),
  applicant_user_id uuid NOT NULL,
  applicant_email_enc text NOT NULL,
  applicant_email_hmac text NOT NULL,
  organization_legal_name text NOT NULL,
  legal_id text,
  authority_evidence_key text,
  requested_plan_code text,
  onboarding_answers jsonb NOT NULL DEFAULT '{}'::jsonb,
  ai_draft_config jsonb,
  state text NOT NULL DEFAULT 'started',
  expires_at timestamptz NOT NULL,
  provisioned_tenant_id uuid,
  CONSTRAINT pk_saas_application_draft PRIMARY KEY (id)
);

COMMENT ON TABLE ge.saas_application_draft IS 'ENT-187 ApplicationDraft · scope P · Imm. M · Part 3.3 §3.3.3.2';

CREATE TABLE ge.saas_support_access_grant (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  requested_by uuid NOT NULL,
  approved_by uuid,
  module_scope text[] NOT NULL,
  startup_ids uuid[] NOT NULL DEFAULT '{}',
  access_mode text NOT NULL DEFAULT 'read_only',
  reason text NOT NULL,
  starts_at timestamptz NOT NULL,
  expires_at timestamptz NOT NULL,
  state text NOT NULL DEFAULT 'requested',
  access_count integer NOT NULL DEFAULT 0,
  CONSTRAINT pk_saas_support_access_grant PRIMARY KEY (id),
  CONSTRAINT uq_saas_support_access_grant__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_saas_support_access_grant__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.saas_support_access_grant IS 'ENT-188 SupportAccessGrant · scope T · Imm. F · Part 3.3 §3.3.3.2';

CREATE TABLE ge.saas_import_job (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  template_code text,
  template_version text,
  source_file_key text,
  source_sha256 text,
  dry_run boolean,
  validation_report_key text,
  rows_total numeric(18,2),
  rows_accepted text,
  rows_rejected text,
  rows_merged text,
  approval_id uuid,
  state text,
  rollback_state text,
  CONSTRAINT pk_saas_import_job PRIMARY KEY (id),
  CONSTRAINT uq_saas_import_job__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_saas_import_job__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.saas_import_job IS 'ENT-190 ImportJob · scope S · Imm. M · Part 3.3 §3.3.3.2 + §3.3.7';

CREATE TABLE ge.ana_metric_definition (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid,
  startup_id uuid,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  version_no integer NOT NULL DEFAULT 1,
  status text NOT NULL DEFAULT 'draft',
  content_hash char(64),
  approval_id uuid,
  approved_at timestamptz,
  effective_from timestamptz,
  effective_to timestamptz,
  supersedes_id uuid,
  metric_code text,
  formula_text text,
  numerator_ref text,
  denominator_ref text,
  filters jsonb,
  currency_basis text,
  owner_role text,
  CONSTRAINT pk_ana_metric_definition PRIMARY KEY (id),
  CONSTRAINT uq_ana_metric_definition__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_ana_metric_definition__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.ana_metric_definition IS 'ENT-191 MetricDefinition · scope X · Imm. V · Part 3.3 §3.3.3.2 + §3.3.7';

CREATE TABLE ge.ana_metric_snapshot (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  correlation_id uuid,
  metric_definition_id uuid,
  metric_version text,
  scope jsonb,
  period_start date,
  period_end date,
  as_of text,
  numerator text,
  denominator text,
  value text,
  unknown_count integer,
  currency char(3),
  schema_ref text,
  evidence_refs uuid[] NOT NULL DEFAULT '{}',
  payload jsonb NOT NULL,
  CONSTRAINT pk_ana_metric_snapshot PRIMARY KEY (id),
  CONSTRAINT uq_ana_metric_snapshot__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_ana_metric_snapshot__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.ana_metric_snapshot IS 'ENT-192 MetricSnapshot · scope S · Imm. A · Part 3.3 §3.3.3.2 + §3.3.7';

CREATE TABLE ge.ana_account_projection (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  organization_id uuid,
  summary jsonb,
  open_deals text,
  last_touch_at timestamptz,
  receivable_balance numeric(18,2),
  last_event_seq text,
  CONSTRAINT pk_ana_account_projection PRIMARY KEY (id),
  CONSTRAINT uq_ana_account_projection__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_ana_account_projection__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.ana_account_projection IS 'ENT-193 AccountProjection · scope S · Imm. M · Part 3.3 §3.3.3.2 + §3.3.7';

CREATE TABLE ge.ana_admin_projection (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  panel_code text,
  startup_ids uuid[],
  payload jsonb,
  refreshed_at timestamptz,
  last_event_seq text,
  CONSTRAINT pk_ana_admin_projection PRIMARY KEY (id),
  CONSTRAINT uq_ana_admin_projection__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_ana_admin_projection__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.ana_admin_projection IS 'ENT-194 AdminProjection · scope T · Imm. M · Part 3.3 §3.3.3.2 + §3.3.7';

CREATE TABLE ge.ana_pipeline_projection (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  deal_id uuid,
  stage_code text,
  owner_id uuid,
  expected_value text,
  currency char(3),
  weighted_value text,
  age_days integer,
  is_simulated boolean,
  CONSTRAINT pk_ana_pipeline_projection PRIMARY KEY (id),
  CONSTRAINT uq_ana_pipeline_projection__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_ana_pipeline_projection__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.ana_pipeline_projection IS 'ENT-195 PipelineProjection · scope S · Imm. M · Part 3.3 §3.3.3.2 + §3.3.7';

CREATE TABLE ge.ana_forecast (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  correlation_id uuid,
  period text,
  scenario text,
  method text,
  weighted_value text,
  ci_low text,
  ci_high text,
  currency char(3),
  assumptions jsonb,
  is_estimate boolean,
  schema_ref text,
  evidence_refs uuid[] NOT NULL DEFAULT '{}',
  payload jsonb NOT NULL,
  CONSTRAINT pk_ana_forecast PRIMARY KEY (id),
  CONSTRAINT uq_ana_forecast__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_ana_forecast__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.ana_forecast IS 'ENT-196 Forecast · scope S · Imm. A · Part 3.3 §3.3.3.2 + §3.3.7';

CREATE TABLE ge.ana_stage_metric (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  correlation_id uuid,
  pipeline_id uuid,
  stage_code text,
  period text,
  conversion_rate numeric(7,4),
  sample_size text,
  median_days integer,
  schema_ref text,
  evidence_refs uuid[] NOT NULL DEFAULT '{}',
  payload jsonb NOT NULL,
  CONSTRAINT pk_ana_stage_metric PRIMARY KEY (id),
  CONSTRAINT uq_ana_stage_metric__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_ana_stage_metric__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.ana_stage_metric IS 'ENT-197 StageMetric · scope S · Imm. A · Part 3.3 §3.3.3.2 + §3.3.7';

CREATE TABLE ge.ana_report_subscription (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  user_id uuid,
  report_code text,
  scope jsonb,
  frequency text,
  format text,
  last_sent_at timestamptz,
  CONSTRAINT pk_ana_report_subscription PRIMARY KEY (id),
  CONSTRAINT uq_ana_report_subscription__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_ana_report_subscription__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.ana_report_subscription IS 'ENT-199 ReportSubscription · scope T · Imm. M · Part 3.3 §3.3.3.2 + §3.3.7';

CREATE TABLE ge.ten_membership_grant (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  membership_id uuid NOT NULL,
  role_id uuid NOT NULL,
  CONSTRAINT pk_ten_membership_grant PRIMARY KEY (id),
  CONSTRAINT uq_ten_membership_grant__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_ten_membership_grant__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.ten_membership_grant IS 'ASSOC Membership × Role × Startup (nullable = tenant-wide) · scope S · Imm. M · Part 3.3 §3.3.3.3';

CREATE TABLE ge.cat_document_offering (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  document_id uuid NOT NULL,
  offering_version_id uuid NOT NULL,
  CONSTRAINT pk_cat_document_offering PRIMARY KEY (id),
  CONSTRAINT uq_cat_document_offering__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_cat_document_offering__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.cat_document_offering IS 'ASSOC Document × OfferingVersion · scope S · Imm. M · Part 3.3 §3.3.3.3';

CREATE TABLE ge.cat_claim_evidence (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  claim_id uuid NOT NULL,
  evidence_ref text NOT NULL,
  CONSTRAINT pk_cat_claim_evidence PRIMARY KEY (id),
  CONSTRAINT uq_cat_claim_evidence__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_cat_claim_evidence__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.cat_claim_evidence IS 'ASSOC Claim × Document/Evidence · scope S · Imm. M · Part 3.3 §3.3.3.3';

CREATE TABLE ge.intel_signal_evidence (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  is_simulated boolean NOT NULL DEFAULT false,
  run_id uuid,
  correlation_id uuid,
  signal_id uuid NOT NULL,
  evidence_id uuid NOT NULL,
  CONSTRAINT pk_intel_signal_evidence PRIMARY KEY (id),
  CONSTRAINT uq_intel_signal_evidence__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_intel_signal_evidence__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.intel_signal_evidence IS 'ASSOC Signal × Evidence · scope S · Imm. M · Part 3.3 §3.3.3.3';

CREATE TABLE ge.intel_opportunity_contact (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  is_simulated boolean NOT NULL DEFAULT false,
  run_id uuid,
  correlation_id uuid,
  opportunity_id uuid NOT NULL,
  contact_id uuid NOT NULL,
  CONSTRAINT pk_intel_opportunity_contact PRIMARY KEY (id),
  CONSTRAINT uq_intel_opportunity_contact__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_intel_opportunity_contact__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.intel_opportunity_contact IS 'ASSOC Opportunity × Contact · scope S · Imm. M · Part 3.3 §3.3.3.3';

CREATE TABLE ge.crm_deal_contact (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  is_simulated boolean NOT NULL DEFAULT false,
  run_id uuid,
  correlation_id uuid,
  deal_id uuid NOT NULL,
  contact_id uuid NOT NULL,
  role_code text NOT NULL,
  CONSTRAINT pk_crm_deal_contact PRIMARY KEY (id),
  CONSTRAINT uq_crm_deal_contact__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_crm_deal_contact__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.crm_deal_contact IS 'ASSOC Deal × Contact (role) · scope S · Imm. M · Part 3.3 §3.3.3.3';

CREATE TABLE ge.eng_message_claim (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  is_simulated boolean NOT NULL DEFAULT false,
  run_id uuid,
  correlation_id uuid,
  message_id uuid NOT NULL,
  claim_id uuid NOT NULL,
  CONSTRAINT pk_eng_message_claim PRIMARY KEY (id),
  CONSTRAINT uq_eng_message_claim__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_eng_message_claim__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.eng_message_claim IS 'ASSOC MessageDraft/Message × Claim · scope S · Imm. M · Part 3.3 §3.3.3.3';

CREATE TABLE ge.mkt_content_claim (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  is_simulated boolean NOT NULL DEFAULT false,
  run_id uuid,
  correlation_id uuid,
  content_version_id uuid NOT NULL,
  claim_id uuid NOT NULL,
  CONSTRAINT pk_mkt_content_claim PRIMARY KEY (id),
  CONSTRAINT uq_mkt_content_claim__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_mkt_content_claim__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.mkt_content_claim IS 'ASSOC ContentVersion × Claim · scope S · Imm. M · Part 3.3 §3.3.3.3';

CREATE TABLE ge.mkt_audience_member (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  is_simulated boolean NOT NULL DEFAULT false,
  run_id uuid,
  correlation_id uuid,
  audience_id uuid NOT NULL,
  contact_id uuid NOT NULL,
  CONSTRAINT pk_mkt_audience_member PRIMARY KEY (id),
  CONSTRAINT uq_mkt_audience_member__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_mkt_audience_member__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.mkt_audience_member IS 'ASSOC Audience (version) × Contact · scope S · Imm. M · Part 3.3 §3.3.3.3';

CREATE TABLE ge.com_contract_party (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  is_simulated boolean NOT NULL DEFAULT false,
  run_id uuid,
  correlation_id uuid,
  contract_id uuid NOT NULL,
  party_ref text NOT NULL,
  party_role text NOT NULL,
  CONSTRAINT pk_com_contract_party PRIMARY KEY (id),
  CONSTRAINT uq_com_contract_party__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_com_contract_party__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.com_contract_party IS 'ASSOC Contract × Organization/Contact · scope S · Imm. M · Part 3.3 §3.3.3.3';

CREATE TABLE ge.aut_run_conflict (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  run_id uuid NOT NULL,
  conflict_case_id uuid NOT NULL,
  CONSTRAINT pk_aut_run_conflict PRIMARY KEY (id),
  CONSTRAINT uq_aut_run_conflict__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_aut_run_conflict__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.aut_run_conflict IS 'ASSOC WorkflowRun × ConflictCase · scope S · Imm. M · Part 3.3 §3.3.3.3';

CREATE TABLE ge.saas_plan_entitlement (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  plan_version_id uuid NOT NULL,
  entitlement_id uuid NOT NULL,
  CONSTRAINT pk_saas_plan_entitlement PRIMARY KEY (id),
  CONSTRAINT uq_saas_plan_entitlement__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_saas_plan_entitlement__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.saas_plan_entitlement IS 'ASSOC PlanVersion × Entitlement · scope S · Imm. M · Part 3.3 §3.3.3.3';

CREATE TABLE ge.lcy_onboarding_task (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  is_simulated boolean NOT NULL DEFAULT false,
  run_id uuid,
  correlation_id uuid,
  onboarding_id uuid NOT NULL,
  task_id uuid NOT NULL,
  CONSTRAINT pk_lcy_onboarding_task PRIMARY KEY (id),
  CONSTRAINT uq_lcy_onboarding_task__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_lcy_onboarding_task__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.lcy_onboarding_task IS 'ASSOC Onboarding × Task · scope S · Imm. M · Part 3.3 §3.3.3.3';

CREATE TABLE ge.ten_business_template (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid,
  startup_id uuid,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  version_no integer NOT NULL DEFAULT 1,
  status text NOT NULL DEFAULT 'draft',
  content_hash char(64),
  approval_id uuid,
  approved_at timestamptz,
  effective_from timestamptz,
  effective_to timestamptz,
  supersedes_id uuid,
  template_key text NOT NULL,
  name text NOT NULL,
  industry_code text,
  schema jsonb NOT NULL,
  defaults jsonb NOT NULL DEFAULT '{}'::jsonb,
  capability_defaults jsonb NOT NULL DEFAULT '{}'::jsonb,
  workflow_template_ids uuid[] NOT NULL DEFAULT '{}',
  is_public_library boolean NOT NULL DEFAULT false,
  CONSTRAINT pk_ten_business_template PRIMARY KEY (id),
  CONSTRAINT uq_ten_business_template__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_ten_business_template__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.ten_business_template IS 'ENT-ENH-E-01 BusinessTemplate · scope X · Imm. V · Part 3.6b §3.6.5';

CREATE TABLE ge.saas_service_request (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  is_simulated boolean NOT NULL DEFAULT false,
  run_id uuid,
  correlation_id uuid,
  request_no text NOT NULL,
  requester_user_id uuid NOT NULL,
  kind text NOT NULL,
  subject text NOT NULL,
  description text NOT NULL,
  priority text NOT NULL DEFAULT 'normal',
  status text NOT NULL DEFAULT 'open',
  assignee_user_id uuid,
  linked_object_type text,
  linked_object_id text,
  first_response_at timestamptz,
  resolved_at timestamptz,
  closed_at timestamptz,
  support_grant_id uuid,
  CONSTRAINT pk_saas_service_request PRIMARY KEY (id),
  CONSTRAINT uq_saas_service_request__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_saas_service_request__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.saas_service_request IS 'ENT-ENH-E-02 ServiceRequest · scope T · Imm. M · Part 3.6b §3.6.5';

CREATE TABLE ge.com_fulfillment_milestone (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  is_simulated boolean NOT NULL DEFAULT false,
  run_id uuid,
  correlation_id uuid,
  order_id uuid NOT NULL,
  order_line_id uuid,
  milestone_key text NOT NULL,
  milestone_type text NOT NULL,
  planned_quantity numeric(18,4),
  unit_code text,
  due_at timestamptz NOT NULL,
  state text NOT NULL DEFAULT 'planned',
  evidence_ref text,
  accepted_at text,
  accepted_by_ref text,
  last_event_id uuid,
  CONSTRAINT pk_com_fulfillment_milestone PRIMARY KEY (id),
  CONSTRAINT uq_com_fulfillment_milestone__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_com_fulfillment_milestone__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.com_fulfillment_milestone IS 'ENT-ENH-E-03 FulfillmentMilestone · scope S · Imm. F · Part 3.6b §3.6.5';

CREATE TABLE ge.ai_eval_case_result (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid,
  startup_id uuid,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  correlation_id uuid,
  eval_run_id uuid NOT NULL,
  eval_case_id uuid NOT NULL,
  passed boolean NOT NULL,
  score numeric(7,4),
  result jsonb NOT NULL,
  model_run_id uuid,
  CONSTRAINT pk_ai_eval_case_result PRIMARY KEY (id),
  CONSTRAINT uq_ai_eval_case_result__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_ai_eval_case_result__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.ai_eval_case_result IS 'ENT-ENH-E-04 EvalCaseResult · scope X · Imm. A · Part 3.6b §3.6.5';

CREATE TABLE ge.inv_source (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  is_simulated boolean NOT NULL DEFAULT false,
  run_id uuid,
  correlation_id uuid,
  kind text,
  host text,
  licence_ref text,
  policy_id uuid,
  state text NOT NULL DEFAULT 'draft',
  payload jsonb NOT NULL DEFAULT '{}'::jsonb,
  region text NOT NULL DEFAULT ge.app_zone(),
  CONSTRAINT pk_inv_source PRIMARY KEY (id),
  CONSTRAINT uq_inv_source__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_inv_source__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.inv_source IS 'NEW inv_source · scope S · Imm. M · Part 11.16a §11.16.5.10';

CREATE TABLE ge.inv_source_policy (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  is_simulated boolean NOT NULL DEFAULT false,
  run_id uuid,
  correlation_id uuid,
  source_id uuid,
  purpose text,
  permitted_use text,
  freshness_days integer,
  expires_at timestamptz,
  state text NOT NULL DEFAULT 'draft',
  payload jsonb NOT NULL DEFAULT '{}'::jsonb,
  region text NOT NULL DEFAULT ge.app_zone(),
  CONSTRAINT pk_inv_source_policy PRIMARY KEY (id),
  CONSTRAINT uq_inv_source_policy__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_inv_source_policy__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.inv_source_policy IS 'NEW inv_source_policy · scope S · Imm. M · Part 11.16a §11.16.5.10';

CREATE TABLE ge.inv_search_plan (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  is_simulated boolean NOT NULL DEFAULT false,
  run_id uuid,
  correlation_id uuid,
  round_id uuid,
  thesis text,
  routes text[],
  regions text[],
  status text,
  state text NOT NULL DEFAULT 'draft',
  payload jsonb NOT NULL DEFAULT '{}'::jsonb,
  region text NOT NULL DEFAULT ge.app_zone(),
  CONSTRAINT pk_inv_search_plan PRIMARY KEY (id),
  CONSTRAINT uq_inv_search_plan__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_inv_search_plan__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.inv_search_plan IS 'NEW inv_search_plan · scope S · Imm. M · Part 11.16a §11.16.5.10';

CREATE TABLE ge.inv_search_run (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  is_simulated boolean NOT NULL DEFAULT false,
  run_id uuid,
  correlation_id uuid,
  plan_id uuid,
  started_at timestamptz,
  finished_at timestamptz,
  counts text,
  cost_minor numeric(18,2),
  state text NOT NULL DEFAULT 'draft',
  payload jsonb NOT NULL DEFAULT '{}'::jsonb,
  region text NOT NULL DEFAULT ge.app_zone(),
  CONSTRAINT pk_inv_search_run PRIMARY KEY (id),
  CONSTRAINT uq_inv_search_run__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_inv_search_run__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.inv_search_run IS 'NEW inv_search_run · scope S · Imm. M · Part 11.16a §11.16.5.10';

CREATE TABLE ge.inv_funding_route (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  is_simulated boolean NOT NULL DEFAULT false,
  run_id uuid,
  correlation_id uuid,
  type text,
  criteria text,
  status text,
  approved_by text,
  approved_at timestamptz,
  state text NOT NULL DEFAULT 'draft',
  payload jsonb NOT NULL DEFAULT '{}'::jsonb,
  region text NOT NULL DEFAULT ge.app_zone(),
  CONSTRAINT pk_inv_funding_route PRIMARY KEY (id),
  CONSTRAINT uq_inv_funding_route__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_inv_funding_route__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.inv_funding_route IS 'NEW inv_funding_route · scope S · Imm. M · Part 11.16a §11.16.5.10';

CREATE TABLE ge.inv_opportunity (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  is_simulated boolean NOT NULL DEFAULT false,
  run_id uuid,
  correlation_id uuid,
  route_id uuid,
  investor_id uuid,
  deadline_at timestamptz,
  confidence numeric(7,4),
  state text,
  payload jsonb NOT NULL DEFAULT '{}'::jsonb,
  region text NOT NULL DEFAULT ge.app_zone(),
  CONSTRAINT pk_inv_opportunity PRIMARY KEY (id),
  CONSTRAINT uq_inv_opportunity__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_inv_opportunity__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.inv_opportunity IS 'NEW inv_opportunity · scope S · Imm. M · Part 11.16a §11.16.5.10';

CREATE TABLE ge.inv_evidence (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  is_simulated boolean NOT NULL DEFAULT false,
  run_id uuid,
  correlation_id uuid,
  source_id uuid,
  observed_at timestamptz,
  hash text,
  permitted_use text,
  freshness_state text,
  state text NOT NULL DEFAULT 'draft',
  payload jsonb NOT NULL DEFAULT '{}'::jsonb,
  region text NOT NULL DEFAULT ge.app_zone(),
  CONSTRAINT pk_inv_evidence PRIMARY KEY (id),
  CONSTRAINT uq_inv_evidence__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_inv_evidence__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.inv_evidence IS 'NEW inv_evidence · scope S · Imm. M · Part 11.16a §11.16.5.10';

CREATE TABLE ge.inv_investor (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  is_simulated boolean NOT NULL DEFAULT false,
  run_id uuid,
  correlation_id uuid,
  kind text,
  name text,
  investor_class text,
  jurisdiction text,
  eligibility_status text,
  state text NOT NULL DEFAULT 'draft',
  payload jsonb NOT NULL DEFAULT '{}'::jsonb,
  region text NOT NULL DEFAULT ge.app_zone(),
  CONSTRAINT pk_inv_investor PRIMARY KEY (id),
  CONSTRAINT uq_inv_investor__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_inv_investor__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.inv_investor IS 'NEW inv_investor · scope S · Imm. M · Part 11.16a §11.16.5.10';

CREATE TABLE ge.inv_investor_alias (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  is_simulated boolean NOT NULL DEFAULT false,
  run_id uuid,
  correlation_id uuid,
  investor_id uuid,
  alias text,
  source_id uuid,
  state text NOT NULL DEFAULT 'draft',
  payload jsonb NOT NULL DEFAULT '{}'::jsonb,
  region text NOT NULL DEFAULT ge.app_zone(),
  CONSTRAINT pk_inv_investor_alias PRIMARY KEY (id),
  CONSTRAINT uq_inv_investor_alias__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_inv_investor_alias__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.inv_investor_alias IS 'NEW inv_investor_alias · scope S · Imm. M · Part 11.16a §11.16.5.10';

CREATE TABLE ge.inv_mandate (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  is_simulated boolean NOT NULL DEFAULT false,
  run_id uuid,
  correlation_id uuid,
  investor_id uuid,
  sectors text[],
  stages text[],
  ticket_min text,
  ticket_max text,
  currency char(3),
  regions text[],
  state text NOT NULL DEFAULT 'draft',
  payload jsonb NOT NULL DEFAULT '{}'::jsonb,
  region text NOT NULL DEFAULT ge.app_zone(),
  CONSTRAINT pk_inv_mandate PRIMARY KEY (id),
  CONSTRAINT uq_inv_mandate__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_inv_mandate__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.inv_mandate IS 'NEW inv_mandate · scope S · Imm. M · Part 11.16a §11.16.5.10';

CREATE TABLE ge.inv_round (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  is_simulated boolean NOT NULL DEFAULT false,
  run_id uuid,
  correlation_id uuid,
  instrument text,
  target_minor text,
  currency char(3),
  state text,
  payload jsonb NOT NULL DEFAULT '{}'::jsonb,
  region text NOT NULL DEFAULT ge.app_zone(),
  CONSTRAINT pk_inv_round PRIMARY KEY (id),
  CONSTRAINT uq_inv_round__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_inv_round__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.inv_round IS 'NEW inv_round · scope S · Imm. M · Part 11.16a §11.16.5.10';

CREATE TABLE ge.inv_fit_score (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  is_simulated boolean NOT NULL DEFAULT false,
  run_id uuid,
  correlation_id uuid,
  mandate_id uuid,
  round_id uuid,
  score numeric(9,4),
  reasons text[],
  rubric_version text,
  state text NOT NULL DEFAULT 'draft',
  payload jsonb NOT NULL DEFAULT '{}'::jsonb,
  region text NOT NULL DEFAULT ge.app_zone(),
  CONSTRAINT pk_inv_fit_score PRIMARY KEY (id),
  CONSTRAINT uq_inv_fit_score__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_inv_fit_score__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.inv_fit_score IS 'NEW inv_fit_score · scope S · Imm. M · Part 11.16a §11.16.5.10';

CREATE TABLE ge.inv_match_candidate (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  is_simulated boolean NOT NULL DEFAULT false,
  run_id uuid,
  correlation_id uuid,
  round_id uuid,
  investor_id uuid,
  status text,
  state text NOT NULL DEFAULT 'draft',
  payload jsonb NOT NULL DEFAULT '{}'::jsonb,
  region text NOT NULL DEFAULT ge.app_zone(),
  CONSTRAINT pk_inv_match_candidate PRIMARY KEY (id),
  CONSTRAINT uq_inv_match_candidate__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_inv_match_candidate__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.inv_match_candidate IS 'NEW inv_match_candidate · scope S · Imm. M · Part 11.16a §11.16.5.10';

CREATE TABLE ge.inv_jurisdiction_policy (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  is_simulated boolean NOT NULL DEFAULT false,
  run_id uuid,
  correlation_id uuid,
  jurisdiction text,
  pack_ids uuid[],
  state text,
  payload jsonb NOT NULL DEFAULT '{}'::jsonb,
  region text NOT NULL DEFAULT ge.app_zone(),
  CONSTRAINT pk_inv_jurisdiction_policy PRIMARY KEY (id),
  CONSTRAINT uq_inv_jurisdiction_policy__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_inv_jurisdiction_policy__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.inv_jurisdiction_policy IS 'NEW inv_jurisdiction_policy · scope S · Imm. M · Part 11.16a §11.16.5.10';

CREATE TABLE ge.inv_crossborder_case (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  is_simulated boolean NOT NULL DEFAULT false,
  run_id uuid,
  correlation_id uuid,
  investor_id uuid,
  round_id uuid,
  jurisdictions text[],
  state text,
  payload jsonb NOT NULL DEFAULT '{}'::jsonb,
  region text NOT NULL DEFAULT ge.app_zone(),
  CONSTRAINT pk_inv_crossborder_case PRIMARY KEY (id),
  CONSTRAINT uq_inv_crossborder_case__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_inv_crossborder_case__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.inv_crossborder_case IS 'NEW inv_crossborder_case · scope S · Imm. M · Part 11.16a §11.16.5.10';

CREATE TABLE ge.inv_contact (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  is_simulated boolean NOT NULL DEFAULT false,
  run_id uuid,
  correlation_id uuid,
  investor_id uuid,
  name text,
  role text,
  email text,
  phone text,
  verification_state text,
  state text NOT NULL DEFAULT 'draft',
  payload jsonb NOT NULL DEFAULT '{}'::jsonb,
  region text NOT NULL DEFAULT ge.app_zone(),
  CONSTRAINT pk_inv_contact PRIMARY KEY (id),
  CONSTRAINT uq_inv_contact__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_inv_contact__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.inv_contact IS 'NEW inv_contact · scope S · Imm. M · Part 11.16a §11.16.5.10';

CREATE TABLE ge.inv_contact_evidence (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  is_simulated boolean NOT NULL DEFAULT false,
  run_id uuid,
  correlation_id uuid,
  contact_id uuid,
  source_id uuid,
  observed_at timestamptz,
  permitted_use text,
  state text NOT NULL DEFAULT 'draft',
  payload jsonb NOT NULL DEFAULT '{}'::jsonb,
  region text NOT NULL DEFAULT ge.app_zone(),
  CONSTRAINT pk_inv_contact_evidence PRIMARY KEY (id),
  CONSTRAINT uq_inv_contact_evidence__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_inv_contact_evidence__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.inv_contact_evidence IS 'NEW inv_contact_evidence · scope S · Imm. M · Part 11.16a §11.16.5.10';

CREATE TABLE ge.inv_permission (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  is_simulated boolean NOT NULL DEFAULT false,
  run_id uuid,
  correlation_id uuid,
  contact_id uuid,
  purpose text,
  channel text,
  basis text,
  granted_at timestamptz,
  withdrawn_at timestamptz,
  state text NOT NULL DEFAULT 'draft',
  payload jsonb NOT NULL DEFAULT '{}'::jsonb,
  region text NOT NULL DEFAULT ge.app_zone(),
  CONSTRAINT pk_inv_permission PRIMARY KEY (id),
  CONSTRAINT uq_inv_permission__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_inv_permission__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.inv_permission IS 'NEW inv_permission · scope S · Imm. M · Part 11.16a §11.16.5.10';

CREATE TABLE ge.inv_suppression (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  is_simulated boolean NOT NULL DEFAULT false,
  run_id uuid,
  correlation_id uuid,
  channel text,
  address_hash char(64),
  reason text,
  state text NOT NULL DEFAULT 'draft',
  payload jsonb NOT NULL DEFAULT '{}'::jsonb,
  region text NOT NULL DEFAULT ge.app_zone(),
  CONSTRAINT pk_inv_suppression PRIMARY KEY (id),
  CONSTRAINT uq_inv_suppression__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_inv_suppression__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.inv_suppression IS 'NEW inv_suppression · scope S · Imm. M · Part 11.16a §11.16.5.10';

CREATE TABLE ge.inv_locale_template (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  is_simulated boolean NOT NULL DEFAULT false,
  run_id uuid,
  correlation_id uuid,
  channel text,
  locale text,
  body text,
  approval_hash char(64),
  offering_tag text,
  state text NOT NULL DEFAULT 'draft',
  payload jsonb NOT NULL DEFAULT '{}'::jsonb,
  region text NOT NULL DEFAULT ge.app_zone(),
  CONSTRAINT pk_inv_locale_template PRIMARY KEY (id),
  CONSTRAINT uq_inv_locale_template__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_inv_locale_template__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.inv_locale_template IS 'NEW inv_locale_template · scope S · Imm. M · Part 11.16a §11.16.5.10';

CREATE TABLE ge.inv_message (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  is_simulated boolean NOT NULL DEFAULT false,
  run_id uuid,
  correlation_id uuid,
  thread_id uuid,
  channel text,
  body_ref text,
  approval_hash char(64),
  state text,
  offering_tag text,
  payload jsonb NOT NULL DEFAULT '{}'::jsonb,
  region text NOT NULL DEFAULT ge.app_zone(),
  CONSTRAINT pk_inv_message PRIMARY KEY (id),
  CONSTRAINT uq_inv_message__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_inv_message__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.inv_message IS 'NEW inv_message · scope S · Imm. M · Part 11.16a §11.16.5.10';

CREATE TABLE ge.inv_outbox (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  is_simulated boolean NOT NULL DEFAULT false,
  run_id uuid,
  correlation_id uuid,
  aggregate text,
  event_type text,
  payload_ref text,
  dispatched_at timestamptz,
  state text NOT NULL DEFAULT 'draft',
  payload jsonb NOT NULL DEFAULT '{}'::jsonb,
  region text NOT NULL DEFAULT ge.app_zone(),
  CONSTRAINT pk_inv_outbox PRIMARY KEY (id),
  CONSTRAINT uq_inv_outbox__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_inv_outbox__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.inv_outbox IS 'NEW inv_outbox · scope S · Imm. M · Part 11.16a §11.16.5.10';

CREATE TABLE ge.inv_outreach_reservation (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  is_simulated boolean NOT NULL DEFAULT false,
  run_id uuid,
  correlation_id uuid,
  message_id uuid,
  cost_minor numeric(18,2),
  state text,
  payload jsonb NOT NULL DEFAULT '{}'::jsonb,
  region text NOT NULL DEFAULT ge.app_zone(),
  CONSTRAINT pk_inv_outreach_reservation PRIMARY KEY (id),
  CONSTRAINT uq_inv_outreach_reservation__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_inv_outreach_reservation__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.inv_outreach_reservation IS 'NEW inv_outreach_reservation · scope S · Imm. M · Part 11.16a §11.16.5.10';

CREATE TABLE ge.inv_delivery_event (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  is_simulated boolean NOT NULL DEFAULT false,
  run_id uuid,
  correlation_id uuid,
  message_id uuid,
  provider_event_id uuid,
  state text,
  at text,
  payload jsonb NOT NULL DEFAULT '{}'::jsonb,
  region text NOT NULL DEFAULT ge.app_zone(),
  CONSTRAINT pk_inv_delivery_event PRIMARY KEY (id),
  CONSTRAINT uq_inv_delivery_event__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_inv_delivery_event__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.inv_delivery_event IS 'NEW inv_delivery_event · scope S · Imm. M · Part 11.16a §11.16.5.10';

CREATE TABLE ge.inv_channel (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  is_simulated boolean NOT NULL DEFAULT false,
  run_id uuid,
  correlation_id uuid,
  kind text,
  secret_ref text,
  state text,
  payload jsonb NOT NULL DEFAULT '{}'::jsonb,
  region text NOT NULL DEFAULT ge.app_zone(),
  CONSTRAINT pk_inv_channel PRIMARY KEY (id),
  CONSTRAINT uq_inv_channel__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_inv_channel__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.inv_channel IS 'NEW inv_channel · scope S · Imm. M · Part 11.16a §11.16.5.10';

CREATE TABLE ge.inv_integration_connection (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  is_simulated boolean NOT NULL DEFAULT false,
  run_id uuid,
  correlation_id uuid,
  kind text,
  secret_ref text,
  state text,
  payload jsonb NOT NULL DEFAULT '{}'::jsonb,
  region text NOT NULL DEFAULT ge.app_zone(),
  CONSTRAINT pk_inv_integration_connection PRIMARY KEY (id),
  CONSTRAINT uq_inv_integration_connection__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_inv_integration_connection__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.inv_integration_connection IS 'NEW inv_integration_connection · scope S · Imm. M · Part 11.16a §11.16.5.10';

CREATE TABLE ge.inv_inbound_event (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  is_simulated boolean NOT NULL DEFAULT false,
  run_id uuid,
  correlation_id uuid,
  thread_id uuid,
  channel text,
  received_at timestamptz,
  signature_ok text,
  state text NOT NULL DEFAULT 'draft',
  payload jsonb NOT NULL DEFAULT '{}'::jsonb,
  region text NOT NULL DEFAULT ge.app_zone(),
  CONSTRAINT pk_inv_inbound_event PRIMARY KEY (id),
  CONSTRAINT uq_inv_inbound_event__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_inv_inbound_event__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.inv_inbound_event IS 'NEW inv_inbound_event · scope S · Imm. M · Part 11.16a §11.16.5.10';

CREATE TABLE ge.inv_thread (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  is_simulated boolean NOT NULL DEFAULT false,
  run_id uuid,
  correlation_id uuid,
  thread_id uuid,
  channel text,
  received_at timestamptz,
  signature_ok text,
  state text NOT NULL DEFAULT 'draft',
  payload jsonb NOT NULL DEFAULT '{}'::jsonb,
  region text NOT NULL DEFAULT ge.app_zone(),
  CONSTRAINT pk_inv_thread PRIMARY KEY (id),
  CONSTRAINT uq_inv_thread__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_inv_thread__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.inv_thread IS 'NEW inv_thread · scope S · Imm. M · Part 11.16a §11.16.5.10';

CREATE TABLE ge.inv_sequence (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  is_simulated boolean NOT NULL DEFAULT false,
  run_id uuid,
  correlation_id uuid,
  relationship_id uuid,
  sequence_id uuid,
  step text,
  due_at timestamptz,
  state text,
  payload jsonb NOT NULL DEFAULT '{}'::jsonb,
  region text NOT NULL DEFAULT ge.app_zone(),
  CONSTRAINT pk_inv_sequence PRIMARY KEY (id),
  CONSTRAINT uq_inv_sequence__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_inv_sequence__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.inv_sequence IS 'NEW inv_sequence · scope S · Imm. M · Part 11.16a §11.16.5.10';

CREATE TABLE ge.inv_enrollment (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  is_simulated boolean NOT NULL DEFAULT false,
  run_id uuid,
  correlation_id uuid,
  relationship_id uuid,
  sequence_id uuid,
  step text,
  due_at timestamptz,
  state text,
  payload jsonb NOT NULL DEFAULT '{}'::jsonb,
  region text NOT NULL DEFAULT ge.app_zone(),
  CONSTRAINT pk_inv_enrollment PRIMARY KEY (id),
  CONSTRAINT uq_inv_enrollment__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_inv_enrollment__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.inv_enrollment IS 'NEW inv_enrollment · scope S · Imm. M · Part 11.16a §11.16.5.10';

CREATE TABLE ge.inv_task (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  is_simulated boolean NOT NULL DEFAULT false,
  run_id uuid,
  correlation_id uuid,
  relationship_id uuid,
  sequence_id uuid,
  step text,
  due_at timestamptz,
  state text,
  payload jsonb NOT NULL DEFAULT '{}'::jsonb,
  region text NOT NULL DEFAULT ge.app_zone(),
  CONSTRAINT pk_inv_task PRIMARY KEY (id),
  CONSTRAINT uq_inv_task__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_inv_task__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.inv_task IS 'NEW inv_task · scope S · Imm. M · Part 11.16a §11.16.5.10';

CREATE TABLE ge.inv_stage_event (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  is_simulated boolean NOT NULL DEFAULT false,
  run_id uuid,
  correlation_id uuid,
  relationship_id uuid,
  sequence_id uuid,
  step text,
  due_at timestamptz,
  state text,
  payload jsonb NOT NULL DEFAULT '{}'::jsonb,
  region text NOT NULL DEFAULT ge.app_zone(),
  CONSTRAINT pk_inv_stage_event PRIMARY KEY (id),
  CONSTRAINT uq_inv_stage_event__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_inv_stage_event__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.inv_stage_event IS 'NEW inv_stage_event · scope S · Imm. M · Part 11.16a §11.16.5.10';

CREATE TABLE ge.inv_relationship (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  is_simulated boolean NOT NULL DEFAULT false,
  run_id uuid,
  correlation_id uuid,
  relationship_id uuid,
  sequence_id uuid,
  step text,
  due_at timestamptz,
  state text,
  payload jsonb NOT NULL DEFAULT '{}'::jsonb,
  region text NOT NULL DEFAULT ge.app_zone(),
  CONSTRAINT pk_inv_relationship PRIMARY KEY (id),
  CONSTRAINT uq_inv_relationship__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_inv_relationship__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.inv_relationship IS 'NEW inv_relationship · scope S · Imm. M · Part 11.16a §11.16.5.10';

CREATE TABLE ge.inv_workflow_run (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  is_simulated boolean NOT NULL DEFAULT false,
  run_id uuid,
  correlation_id uuid,
  service_id uuid,
  workflow_id uuid,
  state text,
  payload jsonb NOT NULL DEFAULT '{}'::jsonb,
  region text NOT NULL DEFAULT ge.app_zone(),
  CONSTRAINT pk_inv_workflow_run PRIMARY KEY (id),
  CONSTRAINT uq_inv_workflow_run__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_inv_workflow_run__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.inv_workflow_run IS 'NEW inv_workflow_run · scope S · Imm. M · Part 11.16a §11.16.5.10';

CREATE TABLE ge.inv_objection (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  is_simulated boolean NOT NULL DEFAULT false,
  run_id uuid,
  correlation_id uuid,
  thread_id uuid,
  type text,
  rule_id uuid,
  state text,
  payload jsonb NOT NULL DEFAULT '{}'::jsonb,
  region text NOT NULL DEFAULT ge.app_zone(),
  CONSTRAINT pk_inv_objection PRIMARY KEY (id),
  CONSTRAINT uq_inv_objection__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_inv_objection__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.inv_objection IS 'NEW inv_objection · scope S · Imm. M · Part 11.16a §11.16.5.10';

CREATE TABLE ge.inv_objection_rule (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  is_simulated boolean NOT NULL DEFAULT false,
  run_id uuid,
  correlation_id uuid,
  thread_id uuid,
  type text,
  rule_id uuid,
  state text,
  payload jsonb NOT NULL DEFAULT '{}'::jsonb,
  region text NOT NULL DEFAULT ge.app_zone(),
  CONSTRAINT pk_inv_objection_rule PRIMARY KEY (id),
  CONSTRAINT uq_inv_objection_rule__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_inv_objection_rule__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.inv_objection_rule IS 'NEW inv_objection_rule · scope S · Imm. M · Part 11.16a §11.16.5.10';

CREATE TABLE ge.inv_copilot_action (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  is_simulated boolean NOT NULL DEFAULT false,
  run_id uuid,
  correlation_id uuid,
  thread_id uuid,
  type text,
  rule_id uuid,
  state text,
  payload jsonb NOT NULL DEFAULT '{}'::jsonb,
  region text NOT NULL DEFAULT ge.app_zone(),
  CONSTRAINT pk_inv_copilot_action PRIMARY KEY (id),
  CONSTRAINT uq_inv_copilot_action__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_inv_copilot_action__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.inv_copilot_action IS 'NEW inv_copilot_action · scope S · Imm. M · Part 11.16a §11.16.5.10';

CREATE TABLE ge.inv_meeting (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  is_simulated boolean NOT NULL DEFAULT false,
  run_id uuid,
  correlation_id uuid,
  participants text[],
  starts_at timestamptz,
  consent_id uuid,
  state text,
  payload jsonb NOT NULL DEFAULT '{}'::jsonb,
  region text NOT NULL DEFAULT ge.app_zone(),
  CONSTRAINT pk_inv_meeting PRIMARY KEY (id),
  CONSTRAINT uq_inv_meeting__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_inv_meeting__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.inv_meeting IS 'NEW inv_meeting · scope S · Imm. M · Part 11.16a §11.16.5.10';

CREATE TABLE ge.inv_event (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  is_simulated boolean NOT NULL DEFAULT false,
  run_id uuid,
  correlation_id uuid,
  participants text[],
  starts_at timestamptz,
  consent_id uuid,
  state text,
  payload jsonb NOT NULL DEFAULT '{}'::jsonb,
  region text NOT NULL DEFAULT ge.app_zone(),
  CONSTRAINT pk_inv_event PRIMARY KEY (id),
  CONSTRAINT uq_inv_event__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_inv_event__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.inv_event IS 'NEW inv_event · scope S · Imm. M · Part 11.16a §11.16.5.10';

CREATE TABLE ge.inv_referral (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  is_simulated boolean NOT NULL DEFAULT false,
  run_id uuid,
  correlation_id uuid,
  participants text[],
  starts_at timestamptz,
  consent_id uuid,
  state text,
  payload jsonb NOT NULL DEFAULT '{}'::jsonb,
  region text NOT NULL DEFAULT ge.app_zone(),
  CONSTRAINT pk_inv_referral PRIMARY KEY (id),
  CONSTRAINT uq_inv_referral__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_inv_referral__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.inv_referral IS 'NEW inv_referral · scope S · Imm. M · Part 11.16a §11.16.5.10';

CREATE TABLE ge.inv_adviser_referral (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  is_simulated boolean NOT NULL DEFAULT false,
  run_id uuid,
  correlation_id uuid,
  participants text[],
  starts_at timestamptz,
  consent_id uuid,
  state text,
  payload jsonb NOT NULL DEFAULT '{}'::jsonb,
  region text NOT NULL DEFAULT ge.app_zone(),
  CONSTRAINT pk_inv_adviser_referral PRIMARY KEY (id),
  CONSTRAINT uq_inv_adviser_referral__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_inv_adviser_referral__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.inv_adviser_referral IS 'NEW inv_adviser_referral · scope S · Imm. M · Part 11.16a §11.16.5.10';

CREATE TABLE ge.inv_scenario (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  is_simulated boolean NOT NULL DEFAULT false,
  run_id uuid,
  correlation_id uuid,
  round_id uuid,
  inputs_json jsonb,
  outputs_json jsonb,
  assumptions text[],
  hash text,
  state text NOT NULL DEFAULT 'draft',
  payload jsonb NOT NULL DEFAULT '{}'::jsonb,
  region text NOT NULL DEFAULT ge.app_zone(),
  CONSTRAINT pk_inv_scenario PRIMARY KEY (id),
  CONSTRAINT uq_inv_scenario__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_inv_scenario__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.inv_scenario IS 'NEW inv_scenario · scope S · Imm. M · Part 11.16a §11.16.5.10';

CREATE TABLE ge.inv_claim (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  is_simulated boolean NOT NULL DEFAULT false,
  run_id uuid,
  correlation_id uuid,
  text text,
  evidence_ids uuid[],
  approved_by text,
  expires_at timestamptz,
  state text NOT NULL DEFAULT 'draft',
  payload jsonb NOT NULL DEFAULT '{}'::jsonb,
  region text NOT NULL DEFAULT ge.app_zone(),
  CONSTRAINT pk_inv_claim PRIMARY KEY (id),
  CONSTRAINT uq_inv_claim__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_inv_claim__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.inv_claim IS 'NEW inv_claim · scope S · Imm. M · Part 11.16a §11.16.5.10';

CREATE TABLE ge.inv_disclosure (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  is_simulated boolean NOT NULL DEFAULT false,
  run_id uuid,
  correlation_id uuid,
  text text,
  evidence_ids uuid[],
  approved_by text,
  expires_at timestamptz,
  state text NOT NULL DEFAULT 'draft',
  payload jsonb NOT NULL DEFAULT '{}'::jsonb,
  region text NOT NULL DEFAULT ge.app_zone(),
  CONSTRAINT pk_inv_disclosure PRIMARY KEY (id),
  CONSTRAINT uq_inv_disclosure__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_inv_disclosure__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.inv_disclosure IS 'NEW inv_disclosure · scope S · Imm. M · Part 11.16a §11.16.5.10';

CREATE TABLE ge.inv_guarantee_evidence (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  is_simulated boolean NOT NULL DEFAULT false,
  run_id uuid,
  correlation_id uuid,
  text text,
  evidence_ids uuid[],
  approved_by text,
  expires_at timestamptz,
  state text NOT NULL DEFAULT 'draft',
  payload jsonb NOT NULL DEFAULT '{}'::jsonb,
  region text NOT NULL DEFAULT ge.app_zone(),
  CONSTRAINT pk_inv_guarantee_evidence PRIMARY KEY (id),
  CONSTRAINT uq_inv_guarantee_evidence__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_inv_guarantee_evidence__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.inv_guarantee_evidence IS 'NEW inv_guarantee_evidence · scope S · Imm. M · Part 11.16a §11.16.5.10';

CREATE TABLE ge.inv_document (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  is_simulated boolean NOT NULL DEFAULT false,
  run_id uuid,
  correlation_id uuid,
  room_id uuid,
  doc_class text,
  sensitivity text,
  hash text,
  retention_until date,
  state text NOT NULL DEFAULT 'draft',
  payload jsonb NOT NULL DEFAULT '{}'::jsonb,
  region text NOT NULL DEFAULT ge.app_zone(),
  CONSTRAINT pk_inv_document PRIMARY KEY (id),
  CONSTRAINT uq_inv_document__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_inv_document__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.inv_document IS 'NEW inv_document · scope S · Imm. M · Part 11.16a §11.16.5.10';

CREATE TABLE ge.inv_room (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  is_simulated boolean NOT NULL DEFAULT false,
  run_id uuid,
  correlation_id uuid,
  room_id uuid,
  doc_class text,
  sensitivity text,
  hash text,
  retention_until date,
  state text NOT NULL DEFAULT 'draft',
  payload jsonb NOT NULL DEFAULT '{}'::jsonb,
  region text NOT NULL DEFAULT ge.app_zone(),
  CONSTRAINT pk_inv_room PRIMARY KEY (id),
  CONSTRAINT uq_inv_room__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_inv_room__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.inv_room IS 'NEW inv_room · scope S · Imm. M · Part 11.16a §11.16.5.10';

CREATE TABLE ge.inv_room_item (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  is_simulated boolean NOT NULL DEFAULT false,
  run_id uuid,
  correlation_id uuid,
  room_id uuid,
  doc_class text,
  sensitivity text,
  hash text,
  retention_until date,
  state text NOT NULL DEFAULT 'draft',
  payload jsonb NOT NULL DEFAULT '{}'::jsonb,
  region text NOT NULL DEFAULT ge.app_zone(),
  CONSTRAINT pk_inv_room_item PRIMARY KEY (id),
  CONSTRAINT uq_inv_room_item__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_inv_room_item__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.inv_room_item IS 'NEW inv_room_item · scope S · Imm. M · Part 11.16a §11.16.5.10';

CREATE TABLE ge.inv_access_grant (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  is_simulated boolean NOT NULL DEFAULT false,
  run_id uuid,
  correlation_id uuid,
  investor_id uuid,
  room_id uuid,
  scope jsonb,
  expires_at timestamptz,
  nda_id uuid,
  revoked_at timestamptz,
  state text NOT NULL DEFAULT 'draft',
  payload jsonb NOT NULL DEFAULT '{}'::jsonb,
  region text NOT NULL DEFAULT ge.app_zone(),
  CONSTRAINT pk_inv_access_grant PRIMARY KEY (id),
  CONSTRAINT uq_inv_access_grant__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_inv_access_grant__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.inv_access_grant IS 'NEW inv_access_grant · scope S · Imm. M · Part 11.16a §11.16.5.10';

CREATE TABLE ge.inv_nda (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  is_simulated boolean NOT NULL DEFAULT false,
  run_id uuid,
  correlation_id uuid,
  investor_id uuid,
  room_id uuid,
  scope jsonb,
  expires_at timestamptz,
  nda_id uuid,
  revoked_at timestamptz,
  state text NOT NULL DEFAULT 'draft',
  payload jsonb NOT NULL DEFAULT '{}'::jsonb,
  region text NOT NULL DEFAULT ge.app_zone(),
  CONSTRAINT pk_inv_nda PRIMARY KEY (id),
  CONSTRAINT uq_inv_nda__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_inv_nda__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.inv_nda IS 'NEW inv_nda · scope S · Imm. M · Part 11.16a §11.16.5.10';

CREATE TABLE ge.inv_diligence_request (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  is_simulated boolean NOT NULL DEFAULT false,
  run_id uuid,
  correlation_id uuid,
  room_id uuid,
  investor_id uuid,
  question text,
  answer_ref text,
  state text,
  payload jsonb NOT NULL DEFAULT '{}'::jsonb,
  region text NOT NULL DEFAULT ge.app_zone(),
  CONSTRAINT pk_inv_diligence_request PRIMARY KEY (id),
  CONSTRAINT uq_inv_diligence_request__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_inv_diligence_request__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.inv_diligence_request IS 'NEW inv_diligence_request · scope S · Imm. M · Part 11.16a §11.16.5.10';

CREATE TABLE ge.inv_term_version (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  is_simulated boolean NOT NULL DEFAULT false,
  run_id uuid,
  correlation_id uuid,
  hash text,
  approvers text[],
  state text,
  payload jsonb NOT NULL DEFAULT '{}'::jsonb,
  region text NOT NULL DEFAULT ge.app_zone(),
  CONSTRAINT pk_inv_term_version PRIMARY KEY (id),
  CONSTRAINT uq_inv_term_version__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_inv_term_version__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.inv_term_version IS 'NEW inv_term_version · scope S · Imm. M · Part 11.16a §11.16.5.10';

CREATE TABLE ge.inv_agreement (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  is_simulated boolean NOT NULL DEFAULT false,
  run_id uuid,
  correlation_id uuid,
  hash text,
  approvers text[],
  state text,
  payload jsonb NOT NULL DEFAULT '{}'::jsonb,
  region text NOT NULL DEFAULT ge.app_zone(),
  CONSTRAINT pk_inv_agreement PRIMARY KEY (id),
  CONSTRAINT uq_inv_agreement__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_inv_agreement__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.inv_agreement IS 'NEW inv_agreement · scope S · Imm. M · Part 11.16a §11.16.5.10';

CREATE TABLE ge.inv_approval (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  is_simulated boolean NOT NULL DEFAULT false,
  run_id uuid,
  correlation_id uuid,
  hash text,
  approvers text[],
  state text,
  payload jsonb NOT NULL DEFAULT '{}'::jsonb,
  region text NOT NULL DEFAULT ge.app_zone(),
  CONSTRAINT pk_inv_approval PRIMARY KEY (id),
  CONSTRAINT uq_inv_approval__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_inv_approval__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.inv_approval IS 'NEW inv_approval · scope S · Imm. M · Part 11.16a §11.16.5.10';

CREATE TABLE ge.inv_offer (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  is_simulated boolean NOT NULL DEFAULT false,
  run_id uuid,
  correlation_id uuid,
  offering_id uuid,
  recipient_id uuid,
  serial_no text,
  issued_at timestamptz,
  expires_at timestamptz,
  state text,
  investor_id uuid,
  route text,
  solicitation_mode text,
  financial_year text,
  payload jsonb NOT NULL DEFAULT '{}'::jsonb,
  region text NOT NULL DEFAULT ge.app_zone(),
  CONSTRAINT pk_inv_offer PRIMARY KEY (id),
  CONSTRAINT uq_inv_offer__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_inv_offer__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.inv_offer IS 'NEW inv_offer · scope S · Imm. M · Part 11.16a §11.16.5.10';

CREATE TABLE ge.inv_offer_batch (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  is_simulated boolean NOT NULL DEFAULT false,
  run_id uuid,
  correlation_id uuid,
  offering_id uuid,
  recipient_id uuid,
  serial_no integer,
  issued_at timestamptz,
  expires_at timestamptz,
  state text,
  payload jsonb NOT NULL DEFAULT '{}'::jsonb,
  region text NOT NULL DEFAULT ge.app_zone(),
  CONSTRAINT pk_inv_offer_batch PRIMARY KEY (id),
  CONSTRAINT uq_inv_offer_batch__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_inv_offer_batch__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.inv_offer_batch IS 'NEW inv_offer_batch · scope S · Imm. M · Part 11.16a §11.16.5.10';

CREATE TABLE ge.inv_offer_recipient (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  is_simulated boolean NOT NULL DEFAULT false,
  run_id uuid,
  correlation_id uuid,
  offering_id uuid,
  recipient_id uuid,
  serial_no integer,
  issued_at timestamptz,
  expires_at timestamptz,
  state text,
  payload jsonb NOT NULL DEFAULT '{}'::jsonb,
  region text NOT NULL DEFAULT ge.app_zone(),
  CONSTRAINT pk_inv_offer_recipient PRIMARY KEY (id),
  CONSTRAINT uq_inv_offer_recipient__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_inv_offer_recipient__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.inv_offer_recipient IS 'NEW inv_offer_recipient · scope S · Imm. M · Part 11.16a §11.16.5.10';

CREATE TABLE ge.inv_verification_case (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  is_simulated boolean NOT NULL DEFAULT false,
  run_id uuid,
  correlation_id uuid,
  investor_id uuid,
  provider text,
  result jsonb,
  expires_at timestamptz,
  state text NOT NULL DEFAULT 'draft',
  payload jsonb NOT NULL DEFAULT '{}'::jsonb,
  region text NOT NULL DEFAULT ge.app_zone(),
  CONSTRAINT pk_inv_verification_case PRIMARY KEY (id),
  CONSTRAINT uq_inv_verification_case__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_inv_verification_case__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.inv_verification_case IS 'NEW inv_verification_case · scope S · Imm. M · Part 11.16a §11.16.5.10';

CREATE TABLE ge.inv_bank_account (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  is_simulated boolean NOT NULL DEFAULT false,
  run_id uuid,
  correlation_id uuid,
  masked_no integer,
  verified_at timestamptz,
  state text NOT NULL DEFAULT 'draft',
  payload jsonb NOT NULL DEFAULT '{}'::jsonb,
  region text NOT NULL DEFAULT ge.app_zone(),
  CONSTRAINT pk_inv_bank_account PRIMARY KEY (id),
  CONSTRAINT uq_inv_bank_account__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_inv_bank_account__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.inv_bank_account IS 'NEW inv_bank_account · scope S · Imm. M · Part 11.16a §11.16.5.10';

CREATE TABLE ge.inv_payment_instruction (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  is_simulated boolean NOT NULL DEFAULT false,
  run_id uuid,
  correlation_id uuid,
  masked_no integer,
  verified_at timestamptz,
  state text NOT NULL DEFAULT 'draft',
  payload jsonb NOT NULL DEFAULT '{}'::jsonb,
  region text NOT NULL DEFAULT ge.app_zone(),
  CONSTRAINT pk_inv_payment_instruction PRIMARY KEY (id),
  CONSTRAINT uq_inv_payment_instruction__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_inv_payment_instruction__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.inv_payment_instruction IS 'NEW inv_payment_instruction · scope S · Imm. M · Part 11.16a §11.16.5.10';

CREATE TABLE ge.inv_commitment (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  commitment_id uuid,
  amount_minor numeric(18,2),
  currency char(3),
  payer_ref_hash char(64),
  state text,
  payload jsonb NOT NULL DEFAULT '{}'::jsonb,
  region text NOT NULL DEFAULT ge.app_zone(),
  CONSTRAINT pk_inv_commitment PRIMARY KEY (id),
  CONSTRAINT uq_inv_commitment__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_inv_commitment__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.inv_commitment IS 'NEW inv_commitment · scope S · Imm. A · Part 11.16a §11.16.5.10';

CREATE TABLE ge.inv_receipt (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  commitment_id uuid,
  amount_minor numeric(18,2),
  currency char(3),
  payer_ref_hash char(64),
  state text,
  payload jsonb NOT NULL DEFAULT '{}'::jsonb,
  region text NOT NULL DEFAULT ge.app_zone(),
  CONSTRAINT pk_inv_receipt PRIMARY KEY (id),
  CONSTRAINT uq_inv_receipt__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_inv_receipt__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.inv_receipt IS 'NEW inv_receipt · scope S · Imm. A · Part 11.16a §11.16.5.10';

CREATE TABLE ge.inv_receipt_allocation (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  commitment_id uuid,
  amount_minor numeric(18,2),
  currency char(3),
  payer_ref_hash char(64),
  state text,
  payload jsonb NOT NULL DEFAULT '{}'::jsonb,
  region text NOT NULL DEFAULT ge.app_zone(),
  CONSTRAINT pk_inv_receipt_allocation PRIMARY KEY (id),
  CONSTRAINT uq_inv_receipt_allocation__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_inv_receipt_allocation__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.inv_receipt_allocation IS 'NEW inv_receipt_allocation · scope S · Imm. A · Part 11.16a §11.16.5.10';

CREATE TABLE ge.inv_refund (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  commitment_id uuid,
  amount_minor numeric(18,2),
  currency char(3),
  payer_ref_hash char(64),
  state text,
  payload jsonb NOT NULL DEFAULT '{}'::jsonb,
  region text NOT NULL DEFAULT ge.app_zone(),
  CONSTRAINT pk_inv_refund PRIMARY KEY (id),
  CONSTRAINT uq_inv_refund__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_inv_refund__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.inv_refund IS 'NEW inv_refund · scope S · Imm. A · Part 11.16a §11.16.5.10';

CREATE TABLE ge.inv_fx_rate (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  commitment_id uuid,
  amount_minor numeric(18,2),
  currency char(3),
  payer_ref_hash char(64),
  state text,
  payload jsonb NOT NULL DEFAULT '{}'::jsonb,
  region text NOT NULL DEFAULT ge.app_zone(),
  CONSTRAINT pk_inv_fx_rate PRIMARY KEY (id),
  CONSTRAINT uq_inv_fx_rate__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_inv_fx_rate__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.inv_fx_rate IS 'NEW inv_fx_rate · scope S · Imm. A · Part 11.16a §11.16.5.10';

CREATE TABLE ge.inv_offering (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  is_simulated boolean NOT NULL DEFAULT false,
  run_id uuid,
  correlation_id uuid,
  round_id uuid,
  route text,
  jurisdictions text[],
  solicitation_mode text,
  caps_json jsonb,
  doc_set_hash text,
  state text,
  payload jsonb NOT NULL DEFAULT '{}'::jsonb,
  region text NOT NULL DEFAULT ge.app_zone(),
  CONSTRAINT pk_inv_offering PRIMARY KEY (id),
  CONSTRAINT uq_inv_offering__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_inv_offering__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.inv_offering IS 'NEW inv_offering · scope S · Imm. M · Part 11.16a §11.16.5.10';

CREATE TABLE ge.inv_counsel_signoff (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  is_simulated boolean NOT NULL DEFAULT false,
  run_id uuid,
  correlation_id uuid,
  offering_id uuid,
  jurisdiction text,
  counsel_name text,
  firm text,
  admission text,
  doc_set_hash text,
  signed_at timestamptz,
  expires_at text,
  r10_approved_by text,
  state text NOT NULL DEFAULT 'draft',
  payload jsonb NOT NULL DEFAULT '{}'::jsonb,
  region text NOT NULL DEFAULT ge.app_zone(),
  CONSTRAINT pk_inv_counsel_signoff PRIMARY KEY (id),
  CONSTRAINT uq_inv_counsel_signoff__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_inv_counsel_signoff__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.inv_counsel_signoff IS 'NEW inv_counsel_signoff · scope S · Imm. M · Part 11.16a §11.16.5.10';

CREATE TABLE ge.inv_eligibility_check (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  is_simulated boolean NOT NULL DEFAULT false,
  run_id uuid,
  correlation_id uuid,
  investor_id uuid,
  route text,
  investor_class text,
  evidence_ids uuid[],
  kyc_case_id uuid,
  status text,
  expires_at text,
  decided_by text,
  state text NOT NULL DEFAULT 'draft',
  payload jsonb NOT NULL DEFAULT '{}'::jsonb,
  region text NOT NULL DEFAULT ge.app_zone(),
  CONSTRAINT pk_inv_eligibility_check PRIMARY KEY (id),
  CONSTRAINT uq_inv_eligibility_check__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_inv_eligibility_check__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.inv_eligibility_check IS 'NEW inv_eligibility_check · scope S · Imm. M · Part 11.16a §11.16.5.10';

CREATE TABLE ge.inv_relationship_provenance (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  is_simulated boolean NOT NULL DEFAULT false,
  run_id uuid,
  correlation_id uuid,
  investor_id uuid,
  issuer_id uuid,
  kind text,
  first_contact_at timestamptz,
  evidence_ref text,
  recorded_by text,
  state text NOT NULL DEFAULT 'draft',
  payload jsonb NOT NULL DEFAULT '{}'::jsonb,
  region text NOT NULL DEFAULT ge.app_zone(),
  CONSTRAINT pk_inv_relationship_provenance PRIMARY KEY (id),
  CONSTRAINT uq_inv_relationship_provenance__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_inv_relationship_provenance__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.inv_relationship_provenance IS 'NEW inv_relationship_provenance · scope S · Imm. M · Part 11.16a §11.16.5.10';

CREATE TABLE ge.inv_offer_counter (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  is_simulated boolean NOT NULL DEFAULT false,
  run_id uuid,
  correlation_id uuid,
  offering_id uuid,
  route text,
  period text,
  scope jsonb,
  used text,
  cap text,
  state text NOT NULL DEFAULT 'draft',
  payload jsonb NOT NULL DEFAULT '{}'::jsonb,
  region text NOT NULL DEFAULT ge.app_zone(),
  CONSTRAINT pk_inv_offer_counter PRIMARY KEY (id),
  CONSTRAINT uq_inv_offer_counter__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_inv_offer_counter__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.inv_offer_counter IS 'NEW inv_offer_counter · scope S · Imm. M · Part 11.16a §11.16.5.10';

CREATE TABLE ge.inv_guard_finding (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  is_simulated boolean NOT NULL DEFAULT false,
  run_id uuid,
  correlation_id uuid,
  draft_ref text,
  label text,
  rule_id uuid,
  pack_version text,
  verdict text,
  overridden_by text,
  state text NOT NULL DEFAULT 'draft',
  payload jsonb NOT NULL DEFAULT '{}'::jsonb,
  region text NOT NULL DEFAULT ge.app_zone(),
  CONSTRAINT pk_inv_guard_finding PRIMARY KEY (id),
  CONSTRAINT uq_inv_guard_finding__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_inv_guard_finding__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.inv_guard_finding IS 'NEW inv_guard_finding · scope S · Imm. M · Part 11.16a §11.16.5.10';

CREATE TABLE ge.inv_offer_ledger (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  counted boolean,
  offer_id uuid,
  jurisdiction text,
  person_id uuid,
  exclusion_reason text,
  state text NOT NULL DEFAULT 'draft',
  payload jsonb NOT NULL DEFAULT '{}'::jsonb,
  region text NOT NULL DEFAULT ge.app_zone(),
  CONSTRAINT pk_inv_offer_ledger PRIMARY KEY (id),
  CONSTRAINT uq_inv_offer_ledger__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_inv_offer_ledger__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.inv_offer_ledger IS 'NEW inv_offer_ledger · scope S · Imm. A · Part 11.16c §11.16.15.18';

CREATE TABLE ge.inv_offeree (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  is_simulated boolean NOT NULL DEFAULT false,
  run_id uuid,
  correlation_id uuid,
  state text NOT NULL DEFAULT 'draft',
  payload jsonb NOT NULL DEFAULT '{}'::jsonb,
  region text NOT NULL DEFAULT ge.app_zone(),
  CONSTRAINT pk_inv_offeree PRIMARY KEY (id),
  CONSTRAINT uq_inv_offeree__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_inv_offeree__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.inv_offeree IS 'NEW inv_offeree · scope S · Imm. M · Part 11.16c §11.16.15.18';

CREATE TABLE ge.inv_investor_classification (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  is_simulated boolean NOT NULL DEFAULT false,
  run_id uuid,
  correlation_id uuid,
  basis text,
  statement text,
  signed_at timestamptz,
  expires_at timestamptz,
  state text NOT NULL DEFAULT 'draft',
  payload jsonb NOT NULL DEFAULT '{}'::jsonb,
  region text NOT NULL DEFAULT ge.app_zone(),
  CONSTRAINT pk_inv_investor_classification PRIMARY KEY (id),
  CONSTRAINT uq_inv_investor_classification__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_inv_investor_classification__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.inv_investor_classification IS 'NEW inv_investor_classification · scope S · Imm. M · Part 11.16c §11.16.15.18';

CREATE TABLE ge.inv_accreditation_verification (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  is_simulated boolean NOT NULL DEFAULT false,
  run_id uuid,
  correlation_id uuid,
  verifier text,
  evidence text,
  verified_at timestamptz,
  expires_at timestamptz,
  state text NOT NULL DEFAULT 'draft',
  payload jsonb NOT NULL DEFAULT '{}'::jsonb,
  region text NOT NULL DEFAULT ge.app_zone(),
  CONSTRAINT pk_inv_accreditation_verification PRIMARY KEY (id),
  CONSTRAINT uq_inv_accreditation_verification__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_inv_accreditation_verification__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.inv_accreditation_verification IS 'NEW inv_accreditation_verification · scope S · Imm. M · Part 11.16c §11.16.15.18';

CREATE TABLE ge.inv_promotion_review (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  is_simulated boolean NOT NULL DEFAULT false,
  run_id uuid,
  correlation_id uuid,
  findings text,
  legends text,
  verdict text,
  approver text,
  state text NOT NULL DEFAULT 'draft',
  payload jsonb NOT NULL DEFAULT '{}'::jsonb,
  region text NOT NULL DEFAULT ge.app_zone(),
  CONSTRAINT pk_inv_promotion_review PRIMARY KEY (id),
  CONSTRAINT uq_inv_promotion_review__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_inv_promotion_review__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.inv_promotion_review IS 'NEW inv_promotion_review · scope S · Imm. M · Part 11.16c §11.16.15.18';

CREATE TABLE ge.inv_application_money_account (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  is_simulated boolean NOT NULL DEFAULT false,
  run_id uuid,
  correlation_id uuid,
  receipts text,
  state text NOT NULL DEFAULT 'draft',
  payload jsonb NOT NULL DEFAULT '{}'::jsonb,
  region text NOT NULL DEFAULT ge.app_zone(),
  CONSTRAINT pk_inv_application_money_account PRIMARY KEY (id),
  CONSTRAINT uq_inv_application_money_account__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_inv_application_money_account__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.inv_application_money_account IS 'NEW inv_application_money_account · scope S · Imm. M · Part 11.16c §11.16.15.18';

CREATE TABLE ge.inv_allotment_clock (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  is_simulated boolean NOT NULL DEFAULT false,
  run_id uuid,
  correlation_id uuid,
  allot_by date,
  refund_by date,
  interest_from text,
  state text,
  receipt_date date,
  payload jsonb NOT NULL DEFAULT '{}'::jsonb,
  region text NOT NULL DEFAULT ge.app_zone(),
  CONSTRAINT pk_inv_allotment_clock PRIMARY KEY (id),
  CONSTRAINT uq_inv_allotment_clock__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_inv_allotment_clock__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.inv_allotment_clock IS 'NEW inv_allotment_clock · scope S · Imm. M · Part 11.16c §11.16.15.18';

CREATE TABLE ge.inv_closing (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  is_simulated boolean NOT NULL DEFAULT false,
  run_id uuid,
  correlation_id uuid,
  offer_id uuid,
  state text,
  checklist_hash text,
  payload jsonb NOT NULL DEFAULT '{}'::jsonb,
  region text NOT NULL DEFAULT ge.app_zone(),
  CONSTRAINT pk_inv_closing PRIMARY KEY (id),
  CONSTRAINT uq_inv_closing__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_inv_closing__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.inv_closing IS 'NEW inv_closing · scope S · Imm. M · Part 11.16c §11.16.15.18';

CREATE TABLE ge.inv_closing_requirement (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  is_simulated boolean NOT NULL DEFAULT false,
  run_id uuid,
  correlation_id uuid,
  state text NOT NULL DEFAULT 'draft',
  payload jsonb NOT NULL DEFAULT '{}'::jsonb,
  region text NOT NULL DEFAULT ge.app_zone(),
  CONSTRAINT pk_inv_closing_requirement PRIMARY KEY (id),
  CONSTRAINT uq_inv_closing_requirement__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_inv_closing_requirement__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.inv_closing_requirement IS 'NEW inv_closing_requirement · scope S · Imm. M · Part 11.16c §11.16.15.18';

CREATE TABLE ge.inv_allotment (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  is_simulated boolean NOT NULL DEFAULT false,
  run_id uuid,
  correlation_id uuid,
  filing_task text,
  due_rule text,
  ack_ref text,
  state text NOT NULL DEFAULT 'draft',
  payload jsonb NOT NULL DEFAULT '{}'::jsonb,
  region text NOT NULL DEFAULT ge.app_zone(),
  CONSTRAINT pk_inv_allotment PRIMARY KEY (id),
  CONSTRAINT uq_inv_allotment__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_inv_allotment__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.inv_allotment IS 'NEW inv_allotment · scope S · Imm. M · Part 11.16c §11.16.15.18';

CREATE TABLE ge.inv_filing_task (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  is_simulated boolean NOT NULL DEFAULT false,
  run_id uuid,
  correlation_id uuid,
  filing_task text,
  due_rule text,
  ack_ref text,
  state text NOT NULL DEFAULT 'draft',
  payload jsonb NOT NULL DEFAULT '{}'::jsonb,
  region text NOT NULL DEFAULT ge.app_zone(),
  CONSTRAINT pk_inv_filing_task PRIMARY KEY (id),
  CONSTRAINT uq_inv_filing_task__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_inv_filing_task__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.inv_filing_task IS 'NEW inv_filing_task · scope S · Imm. M · Part 11.16c §11.16.15.18';

CREATE TABLE ge.inv_legal_check (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  is_simulated boolean NOT NULL DEFAULT false,
  run_id uuid,
  correlation_id uuid,
  filing_task text,
  due_rule text,
  ack_ref text,
  state text NOT NULL DEFAULT 'draft',
  payload jsonb NOT NULL DEFAULT '{}'::jsonb,
  region text NOT NULL DEFAULT ge.app_zone(),
  CONSTRAINT pk_inv_legal_check PRIMARY KEY (id),
  CONSTRAINT uq_inv_legal_check__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_inv_legal_check__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.inv_legal_check IS 'NEW inv_legal_check · scope S · Imm. M · Part 11.16c §11.16.15.18';

CREATE TABLE ge.inv_obligation (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  is_simulated boolean NOT NULL DEFAULT false,
  run_id uuid,
  correlation_id uuid,
  filing_task text,
  due_rule text,
  ack_ref text,
  state text NOT NULL DEFAULT 'draft',
  payload jsonb NOT NULL DEFAULT '{}'::jsonb,
  region text NOT NULL DEFAULT ge.app_zone(),
  CONSTRAINT pk_inv_obligation PRIMARY KEY (id),
  CONSTRAINT uq_inv_obligation__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_inv_obligation__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.inv_obligation IS 'NEW inv_obligation · scope S · Imm. M · Part 11.16c §11.16.15.18';

CREATE TABLE ge.inv_update (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  is_simulated boolean NOT NULL DEFAULT false,
  run_id uuid,
  correlation_id uuid,
  update text,
  state text NOT NULL DEFAULT 'draft',
  payload jsonb NOT NULL DEFAULT '{}'::jsonb,
  region text NOT NULL DEFAULT ge.app_zone(),
  CONSTRAINT pk_inv_update PRIMARY KEY (id),
  CONSTRAINT uq_inv_update__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_inv_update__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.inv_update IS 'NEW inv_update · scope S · Imm. M · Part 11.16c §11.16.15.18';

CREATE TABLE ge.inv_feedback (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  is_simulated boolean NOT NULL DEFAULT false,
  run_id uuid,
  correlation_id uuid,
  update text,
  state text NOT NULL DEFAULT 'draft',
  payload jsonb NOT NULL DEFAULT '{}'::jsonb,
  region text NOT NULL DEFAULT ge.app_zone(),
  CONSTRAINT pk_inv_feedback PRIMARY KEY (id),
  CONSTRAINT uq_inv_feedback__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_inv_feedback__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.inv_feedback IS 'NEW inv_feedback · scope S · Imm. M · Part 11.16c §11.16.15.18';

CREATE TABLE ge.inv_deployment_milestone (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  is_simulated boolean NOT NULL DEFAULT false,
  run_id uuid,
  correlation_id uuid,
  update text,
  state text NOT NULL DEFAULT 'draft',
  payload jsonb NOT NULL DEFAULT '{}'::jsonb,
  region text NOT NULL DEFAULT ge.app_zone(),
  CONSTRAINT pk_inv_deployment_milestone PRIMARY KEY (id),
  CONSTRAINT uq_inv_deployment_milestone__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_inv_deployment_milestone__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.inv_deployment_milestone IS 'NEW inv_deployment_milestone · scope S · Imm. M · Part 11.16c §11.16.15.18';

CREATE TABLE ge.inv_capital_allocation (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  is_simulated boolean NOT NULL DEFAULT false,
  run_id uuid,
  correlation_id uuid,
  update text,
  state text NOT NULL DEFAULT 'draft',
  payload jsonb NOT NULL DEFAULT '{}'::jsonb,
  region text NOT NULL DEFAULT ge.app_zone(),
  CONSTRAINT pk_inv_capital_allocation PRIMARY KEY (id),
  CONSTRAINT uq_inv_capital_allocation__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_inv_capital_allocation__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.inv_capital_allocation IS 'NEW inv_capital_allocation · scope S · Imm. M · Part 11.16c §11.16.15.18';

CREATE TABLE ge.inv_dashboard_projection (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  is_simulated boolean NOT NULL DEFAULT false,
  run_id uuid,
  correlation_id uuid,
  state text NOT NULL DEFAULT 'draft',
  payload jsonb NOT NULL DEFAULT '{}'::jsonb,
  region text NOT NULL DEFAULT ge.app_zone(),
  CONSTRAINT pk_inv_dashboard_projection PRIMARY KEY (id),
  CONSTRAINT uq_inv_dashboard_projection__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_inv_dashboard_projection__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.inv_dashboard_projection IS 'NEW inv_dashboard_projection · scope S · Imm. M · Part 11.16c §11.16.15.18';

CREATE TABLE ge.inv_webhook_endpoint (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  is_simulated boolean NOT NULL DEFAULT false,
  run_id uuid,
  correlation_id uuid,
  endpoint text,
  rotation text,
  schema text,
  state text NOT NULL DEFAULT 'draft',
  payload jsonb NOT NULL DEFAULT '{}'::jsonb,
  region text NOT NULL DEFAULT ge.app_zone(),
  CONSTRAINT pk_inv_webhook_endpoint PRIMARY KEY (id),
  CONSTRAINT uq_inv_webhook_endpoint__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_inv_webhook_endpoint__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.inv_webhook_endpoint IS 'NEW inv_webhook_endpoint · scope S · Imm. M · Part 11.16c §11.16.15.18';

CREATE TABLE ge.inv_external_agent_mandate (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  is_simulated boolean NOT NULL DEFAULT false,
  run_id uuid,
  correlation_id uuid,
  scope jsonb,
  issuer text,
  caps text,
  validity text,
  state text NOT NULL DEFAULT 'draft',
  payload jsonb NOT NULL DEFAULT '{}'::jsonb,
  region text NOT NULL DEFAULT ge.app_zone(),
  CONSTRAINT pk_inv_external_agent_mandate PRIMARY KEY (id),
  CONSTRAINT uq_inv_external_agent_mandate__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_inv_external_agent_mandate__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.inv_external_agent_mandate IS 'NEW inv_external_agent_mandate · scope S · Imm. M · Part 11.16c §11.16.15.18';

CREATE TABLE ge.inv_grant_case (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  is_simulated boolean NOT NULL DEFAULT false,
  run_id uuid,
  correlation_id uuid,
  state text NOT NULL DEFAULT 'draft',
  payload jsonb NOT NULL DEFAULT '{}'::jsonb,
  region text NOT NULL DEFAULT ge.app_zone(),
  CONSTRAINT pk_inv_grant_case PRIMARY KEY (id),
  CONSTRAINT uq_inv_grant_case__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_inv_grant_case__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.inv_grant_case IS 'NEW inv_grant_case · scope S · Imm. M · Part 11.16c §11.16.15.18';

CREATE TABLE ge.inv_grant_criterion (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  is_simulated boolean NOT NULL DEFAULT false,
  run_id uuid,
  correlation_id uuid,
  state text NOT NULL DEFAULT 'draft',
  payload jsonb NOT NULL DEFAULT '{}'::jsonb,
  region text NOT NULL DEFAULT ge.app_zone(),
  CONSTRAINT pk_inv_grant_criterion PRIMARY KEY (id),
  CONSTRAINT uq_inv_grant_criterion__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_inv_grant_criterion__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.inv_grant_criterion IS 'NEW inv_grant_criterion · scope S · Imm. M · Part 11.16c §11.16.15.18';

CREATE TABLE ge.inv_grant_budget_line (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  is_simulated boolean NOT NULL DEFAULT false,
  run_id uuid,
  correlation_id uuid,
  state text NOT NULL DEFAULT 'draft',
  payload jsonb NOT NULL DEFAULT '{}'::jsonb,
  region text NOT NULL DEFAULT ge.app_zone(),
  CONSTRAINT pk_inv_grant_budget_line PRIMARY KEY (id),
  CONSTRAINT uq_inv_grant_budget_line__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_inv_grant_budget_line__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.inv_grant_budget_line IS 'NEW inv_grant_budget_line · scope S · Imm. M · Part 11.16c §11.16.15.18';

CREATE TABLE ge.inv_grant_award (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  is_simulated boolean NOT NULL DEFAULT false,
  run_id uuid,
  correlation_id uuid,
  state text NOT NULL DEFAULT 'draft',
  payload jsonb NOT NULL DEFAULT '{}'::jsonb,
  region text NOT NULL DEFAULT ge.app_zone(),
  CONSTRAINT pk_inv_grant_award PRIMARY KEY (id),
  CONSTRAINT uq_inv_grant_award__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_inv_grant_award__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.inv_grant_award IS 'NEW inv_grant_award · scope S · Imm. M · Part 11.16c §11.16.15.18';

CREATE TABLE ge.inv_debt_case (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  is_simulated boolean NOT NULL DEFAULT false,
  run_id uuid,
  correlation_id uuid,
  state text NOT NULL DEFAULT 'draft',
  payload jsonb NOT NULL DEFAULT '{}'::jsonb,
  region text NOT NULL DEFAULT ge.app_zone(),
  CONSTRAINT pk_inv_debt_case PRIMARY KEY (id),
  CONSTRAINT uq_inv_debt_case__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_inv_debt_case__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.inv_debt_case IS 'NEW inv_debt_case · scope S · Imm. M · Part 11.16c §11.16.15.18';

CREATE TABLE ge.inv_debt_term (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  is_simulated boolean NOT NULL DEFAULT false,
  run_id uuid,
  correlation_id uuid,
  state text NOT NULL DEFAULT 'draft',
  payload jsonb NOT NULL DEFAULT '{}'::jsonb,
  region text NOT NULL DEFAULT ge.app_zone(),
  CONSTRAINT pk_inv_debt_term PRIMARY KEY (id),
  CONSTRAINT uq_inv_debt_term__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_inv_debt_term__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.inv_debt_term IS 'NEW inv_debt_term · scope S · Imm. M · Part 11.16c §11.16.15.18';

CREATE TABLE ge.inv_covenant (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  is_simulated boolean NOT NULL DEFAULT false,
  run_id uuid,
  correlation_id uuid,
  state text NOT NULL DEFAULT 'draft',
  payload jsonb NOT NULL DEFAULT '{}'::jsonb,
  region text NOT NULL DEFAULT ge.app_zone(),
  CONSTRAINT pk_inv_covenant PRIMARY KEY (id),
  CONSTRAINT uq_inv_covenant__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_inv_covenant__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.inv_covenant IS 'NEW inv_covenant · scope S · Imm. M · Part 11.16c §11.16.15.18';

CREATE TABLE ge.inv_repayment_schedule (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  is_simulated boolean NOT NULL DEFAULT false,
  run_id uuid,
  correlation_id uuid,
  state text NOT NULL DEFAULT 'draft',
  payload jsonb NOT NULL DEFAULT '{}'::jsonb,
  region text NOT NULL DEFAULT ge.app_zone(),
  CONSTRAINT pk_inv_repayment_schedule PRIMARY KEY (id),
  CONSTRAINT uq_inv_repayment_schedule__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_inv_repayment_schedule__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.inv_repayment_schedule IS 'NEW inv_repayment_schedule · scope S · Imm. M · Part 11.16c §11.16.15.18';

CREATE TABLE ge.inv_readiness_snapshot (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  is_simulated boolean NOT NULL DEFAULT false,
  run_id uuid,
  correlation_id uuid,
  state text NOT NULL DEFAULT 'draft',
  payload jsonb NOT NULL DEFAULT '{}'::jsonb,
  region text NOT NULL DEFAULT ge.app_zone(),
  CONSTRAINT pk_inv_readiness_snapshot PRIMARY KEY (id),
  CONSTRAINT uq_inv_readiness_snapshot__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_inv_readiness_snapshot__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.inv_readiness_snapshot IS 'NEW inv_readiness_snapshot · scope S · Imm. M · Part 11.16c §11.16.15.18';

CREATE TABLE ge.inv_runway_scenario (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  is_simulated boolean NOT NULL DEFAULT false,
  run_id uuid,
  correlation_id uuid,
  state text NOT NULL DEFAULT 'draft',
  payload jsonb NOT NULL DEFAULT '{}'::jsonb,
  region text NOT NULL DEFAULT ge.app_zone(),
  CONSTRAINT pk_inv_runway_scenario PRIMARY KEY (id),
  CONSTRAINT uq_inv_runway_scenario__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_inv_runway_scenario__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.inv_runway_scenario IS 'NEW inv_runway_scenario · scope S · Imm. M · Part 11.16c §11.16.15.18';

CREATE TABLE ge.inv_readiness_score (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  is_simulated boolean NOT NULL DEFAULT false,
  run_id uuid,
  correlation_id uuid,
  state text NOT NULL DEFAULT 'draft',
  payload jsonb NOT NULL DEFAULT '{}'::jsonb,
  region text NOT NULL DEFAULT ge.app_zone(),
  CONSTRAINT pk_inv_readiness_score PRIMARY KEY (id),
  CONSTRAINT uq_inv_readiness_score__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_inv_readiness_score__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.inv_readiness_score IS 'NEW inv_readiness_score · scope S · Imm. M · Part 11.16c §11.16.15.18';

CREATE TABLE ge.inv_shareholder (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  state text NOT NULL DEFAULT 'draft',
  payload jsonb NOT NULL DEFAULT '{}'::jsonb,
  region text NOT NULL DEFAULT ge.app_zone(),
  CONSTRAINT pk_inv_shareholder PRIMARY KEY (id),
  CONSTRAINT uq_inv_shareholder__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_inv_shareholder__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.inv_shareholder IS 'NEW inv_shareholder · scope S · Imm. A · Part 11.16c §11.16.15.18';

CREATE TABLE ge.inv_holding (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  revision_id uuid,
  shareholder_id uuid,
  quantity numeric(20,4),
  state text NOT NULL DEFAULT 'draft',
  payload jsonb NOT NULL DEFAULT '{}'::jsonb,
  region text NOT NULL DEFAULT ge.app_zone(),
  CONSTRAINT pk_inv_holding PRIMARY KEY (id),
  CONSTRAINT uq_inv_holding__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_inv_holding__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.inv_holding IS 'NEW inv_holding · scope S · Imm. A · Part 11.16c §11.16.15.18';

CREATE TABLE ge.inv_instrument (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  state text NOT NULL DEFAULT 'draft',
  payload jsonb NOT NULL DEFAULT '{}'::jsonb,
  region text NOT NULL DEFAULT ge.app_zone(),
  CONSTRAINT pk_inv_instrument PRIMARY KEY (id),
  CONSTRAINT uq_inv_instrument__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_inv_instrument__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.inv_instrument IS 'NEW inv_instrument · scope S · Imm. A · Part 11.16c §11.16.15.18';

CREATE TABLE ge.inv_instrument_term (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  state text NOT NULL DEFAULT 'draft',
  payload jsonb NOT NULL DEFAULT '{}'::jsonb,
  region text NOT NULL DEFAULT ge.app_zone(),
  CONSTRAINT pk_inv_instrument_term PRIMARY KEY (id),
  CONSTRAINT uq_inv_instrument_term__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_inv_instrument_term__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.inv_instrument_term IS 'NEW inv_instrument_term · scope S · Imm. A · Part 11.16c §11.16.15.18';

CREATE TABLE ge.inv_option_grant (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  state text NOT NULL DEFAULT 'draft',
  payload jsonb NOT NULL DEFAULT '{}'::jsonb,
  region text NOT NULL DEFAULT ge.app_zone(),
  CONSTRAINT pk_inv_option_grant PRIMARY KEY (id),
  CONSTRAINT uq_inv_option_grant__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_inv_option_grant__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.inv_option_grant IS 'NEW inv_option_grant · scope S · Imm. A · Part 11.16c §11.16.15.18';

CREATE TABLE ge.inv_cap_table_revision (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  revision_no integer,
  authority_resolution_id uuid,
  state text,
  payload jsonb NOT NULL DEFAULT '{}'::jsonb,
  region text NOT NULL DEFAULT ge.app_zone(),
  CONSTRAINT pk_inv_cap_table_revision PRIMARY KEY (id),
  CONSTRAINT uq_inv_cap_table_revision__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_inv_cap_table_revision__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.inv_cap_table_revision IS 'NEW inv_cap_table_revision · scope S · Imm. A · Part 11.16c §11.16.15.18';

CREATE TABLE ge.inv_esg_indicator (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  is_simulated boolean NOT NULL DEFAULT false,
  run_id uuid,
  correlation_id uuid,
  state text NOT NULL DEFAULT 'draft',
  payload jsonb NOT NULL DEFAULT '{}'::jsonb,
  region text NOT NULL DEFAULT ge.app_zone(),
  CONSTRAINT pk_inv_esg_indicator PRIMARY KEY (id),
  CONSTRAINT uq_inv_esg_indicator__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_inv_esg_indicator__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.inv_esg_indicator IS 'NEW inv_esg_indicator · scope S · Imm. M · Part 11.16c §11.16.15.18';

CREATE TABLE ge.inv_esg_observation (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  is_simulated boolean NOT NULL DEFAULT false,
  run_id uuid,
  correlation_id uuid,
  state text NOT NULL DEFAULT 'draft',
  payload jsonb NOT NULL DEFAULT '{}'::jsonb,
  region text NOT NULL DEFAULT ge.app_zone(),
  CONSTRAINT pk_inv_esg_observation PRIMARY KEY (id),
  CONSTRAINT uq_inv_esg_observation__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_inv_esg_observation__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.inv_esg_observation IS 'NEW inv_esg_observation · scope S · Imm. M · Part 11.16c §11.16.15.18';

CREATE TABLE ge.inv_esg_disclosure (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  is_simulated boolean NOT NULL DEFAULT false,
  run_id uuid,
  correlation_id uuid,
  state text NOT NULL DEFAULT 'draft',
  payload jsonb NOT NULL DEFAULT '{}'::jsonb,
  region text NOT NULL DEFAULT ge.app_zone(),
  CONSTRAINT pk_inv_esg_disclosure PRIMARY KEY (id),
  CONSTRAINT uq_inv_esg_disclosure__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_inv_esg_disclosure__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.inv_esg_disclosure IS 'NEW inv_esg_disclosure · scope S · Imm. M · Part 11.16c §11.16.15.18';

CREATE TABLE ge.inv_esg_commitment (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  is_simulated boolean NOT NULL DEFAULT false,
  run_id uuid,
  correlation_id uuid,
  state text NOT NULL DEFAULT 'draft',
  payload jsonb NOT NULL DEFAULT '{}'::jsonb,
  region text NOT NULL DEFAULT ge.app_zone(),
  CONSTRAINT pk_inv_esg_commitment PRIMARY KEY (id),
  CONSTRAINT uq_inv_esg_commitment__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_inv_esg_commitment__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.inv_esg_commitment IS 'NEW inv_esg_commitment · scope S · Imm. M · Part 11.16c §11.16.15.18';

CREATE TABLE ge.inv_crossborder_requirement (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  is_simulated boolean NOT NULL DEFAULT false,
  run_id uuid,
  correlation_id uuid,
  state text NOT NULL DEFAULT 'draft',
  payload jsonb NOT NULL DEFAULT '{}'::jsonb,
  region text NOT NULL DEFAULT ge.app_zone(),
  CONSTRAINT pk_inv_crossborder_requirement PRIMARY KEY (id),
  CONSTRAINT uq_inv_crossborder_requirement__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_inv_crossborder_requirement__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.inv_crossborder_requirement IS 'NEW inv_crossborder_requirement · scope S · Imm. M · Part 11.16c §11.16.15.18';

CREATE TABLE ge.inv_regulatory_deadline (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  is_simulated boolean NOT NULL DEFAULT false,
  run_id uuid,
  correlation_id uuid,
  state text NOT NULL DEFAULT 'draft',
  payload jsonb NOT NULL DEFAULT '{}'::jsonb,
  region text NOT NULL DEFAULT ge.app_zone(),
  CONSTRAINT pk_inv_regulatory_deadline PRIMARY KEY (id),
  CONSTRAINT uq_inv_regulatory_deadline__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_inv_regulatory_deadline__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.inv_regulatory_deadline IS 'NEW inv_regulatory_deadline · scope S · Imm. M · Part 11.16c §11.16.15.18';

CREATE TABLE ge.inv_resolution (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  is_simulated boolean NOT NULL DEFAULT false,
  run_id uuid,
  correlation_id uuid,
  state text NOT NULL DEFAULT 'draft',
  payload jsonb NOT NULL DEFAULT '{}'::jsonb,
  region text NOT NULL DEFAULT ge.app_zone(),
  CONSTRAINT pk_inv_resolution PRIMARY KEY (id),
  CONSTRAINT uq_inv_resolution__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_inv_resolution__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.inv_resolution IS 'NEW inv_resolution · scope S · Imm. M · Part 11.16c §11.16.15.18';

CREATE TABLE ge.inv_vote (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  resolution_id uuid,
  shareholder_id uuid,
  votes numeric(20,4),
  choice text,
  state text NOT NULL DEFAULT 'draft',
  payload jsonb NOT NULL DEFAULT '{}'::jsonb,
  region text NOT NULL DEFAULT ge.app_zone(),
  CONSTRAINT pk_inv_vote PRIMARY KEY (id),
  CONSTRAINT uq_inv_vote__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_inv_vote__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.inv_vote IS 'NEW inv_vote · scope S · Imm. A · Part 11.16c §11.16.15.18';

CREATE TABLE ge.inv_decision_action (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  is_simulated boolean NOT NULL DEFAULT false,
  run_id uuid,
  correlation_id uuid,
  state text NOT NULL DEFAULT 'draft',
  payload jsonb NOT NULL DEFAULT '{}'::jsonb,
  region text NOT NULL DEFAULT ge.app_zone(),
  CONSTRAINT pk_inv_decision_action PRIMARY KEY (id),
  CONSTRAINT uq_inv_decision_action__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_inv_decision_action__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.inv_decision_action IS 'NEW inv_decision_action · scope S · Imm. M · Part 11.16c §11.16.15.18';

CREATE TABLE ge.inv_kyc_case (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  is_simulated boolean NOT NULL DEFAULT false,
  run_id uuid,
  correlation_id uuid,
  investor_id uuid,
  region text DEFAULT ge.app_zone(),
  state text,
  expires_at date,
  payload jsonb NOT NULL DEFAULT '{}'::jsonb,
  CONSTRAINT pk_inv_kyc_case PRIMARY KEY (id),
  CONSTRAINT uq_inv_kyc_case__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_inv_kyc_case__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.inv_kyc_case IS 'NEW inv_kyc_case · scope S · Imm. M · Part 11.16c §11.16.15.18';

CREATE TABLE ge.inv_kyc_provider_result (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  state text NOT NULL DEFAULT 'draft',
  payload jsonb NOT NULL DEFAULT '{}'::jsonb,
  region text NOT NULL DEFAULT ge.app_zone(),
  CONSTRAINT pk_inv_kyc_provider_result PRIMARY KEY (id),
  CONSTRAINT uq_inv_kyc_provider_result__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_inv_kyc_provider_result__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.inv_kyc_provider_result IS 'NEW inv_kyc_provider_result · scope S · Imm. A · Part 11.16c §11.16.15.18';

CREATE TABLE ge.inv_screening_hit (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  is_simulated boolean NOT NULL DEFAULT false,
  run_id uuid,
  correlation_id uuid,
  state text NOT NULL DEFAULT 'draft',
  payload jsonb NOT NULL DEFAULT '{}'::jsonb,
  region text NOT NULL DEFAULT ge.app_zone(),
  CONSTRAINT pk_inv_screening_hit PRIMARY KEY (id),
  CONSTRAINT uq_inv_screening_hit__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_inv_screening_hit__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.inv_screening_hit IS 'NEW inv_screening_hit · scope S · Imm. M · Part 11.16c §11.16.15.18';

CREATE TABLE ge.inv_advice_boundary_event (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  state text NOT NULL DEFAULT 'draft',
  payload jsonb NOT NULL DEFAULT '{}'::jsonb,
  region text NOT NULL DEFAULT ge.app_zone(),
  CONSTRAINT pk_inv_advice_boundary_event PRIMARY KEY (id),
  CONSTRAINT uq_inv_advice_boundary_event__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_inv_advice_boundary_event__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.inv_advice_boundary_event IS 'NEW inv_advice_boundary_event · scope S · Imm. A · Part 11.16c §11.16.15.18';

CREATE TABLE ge.inv_rulepack_activation (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  is_simulated boolean NOT NULL DEFAULT false,
  run_id uuid,
  correlation_id uuid,
  state text NOT NULL DEFAULT 'draft',
  payload jsonb NOT NULL DEFAULT '{}'::jsonb,
  region text NOT NULL DEFAULT ge.app_zone(),
  CONSTRAINT pk_inv_rulepack_activation PRIMARY KEY (id),
  CONSTRAINT uq_inv_rulepack_activation__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_inv_rulepack_activation__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.inv_rulepack_activation IS 'NEW inv_rulepack_activation · scope S · Imm. M · Part 11.16c §11.16.15.18';

CREATE TABLE ge.mandate (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  is_simulated boolean NOT NULL DEFAULT false,
  run_id uuid,
  correlation_id uuid,
  region text DEFAULT ge.app_zone(),
  mandate_type text,
  effect_class text,
  autonomy_level text,
  current_version integer,
  state text,
  shadow_until timestamptz,
  owner_id uuid,
  payload jsonb NOT NULL DEFAULT '{}'::jsonb,
  CONSTRAINT pk_mandate PRIMARY KEY (id),
  CONSTRAINT uq_mandate__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_mandate__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.mandate IS 'NEW mandate · scope S · Imm. M · Part 11.17b §11.17.9.2';

CREATE TABLE ge.mandate_version (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  is_simulated boolean NOT NULL DEFAULT false,
  run_id uuid,
  correlation_id uuid,
  mandate_id uuid,
  body jsonb,
  digest text,
  jws text,
  policy_version text,
  rule_pack_versions jsonb,
  version integer,
  state text NOT NULL DEFAULT 'draft',
  payload jsonb NOT NULL DEFAULT '{}'::jsonb,
  region text NOT NULL DEFAULT ge.app_zone(),
  CONSTRAINT pk_mandate_version PRIMARY KEY (id),
  CONSTRAINT uq_mandate_version__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_mandate_version__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.mandate_version IS 'NEW mandate_version · scope S · Imm. M · Part 11.17b §11.17.9.2';

CREATE TABLE ge.mandate_approval (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  is_simulated boolean NOT NULL DEFAULT false,
  run_id uuid,
  correlation_id uuid,
  version_id uuid,
  approver_id uuid,
  role text,
  decision text,
  reason_code text,
  mfa_at timestamptz,
  signed_at timestamptz,
  state text NOT NULL DEFAULT 'draft',
  payload jsonb NOT NULL DEFAULT '{}'::jsonb,
  region text NOT NULL DEFAULT ge.app_zone(),
  CONSTRAINT pk_mandate_approval PRIMARY KEY (id),
  CONSTRAINT uq_mandate_approval__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_mandate_approval__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.mandate_approval IS 'NEW mandate_approval · scope S · Imm. M · Part 11.17b §11.17.9.2';

CREATE TABLE ge.mandate_scope_item (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  is_simulated boolean NOT NULL DEFAULT false,
  run_id uuid,
  correlation_id uuid,
  state text NOT NULL DEFAULT 'draft',
  payload jsonb NOT NULL DEFAULT '{}'::jsonb,
  region text NOT NULL DEFAULT ge.app_zone(),
  CONSTRAINT pk_mandate_scope_item PRIMARY KEY (id),
  CONSTRAINT uq_mandate_scope_item__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_mandate_scope_item__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.mandate_scope_item IS 'NEW mandate_scope_item · scope S · Imm. M · Part 11.17b §11.17.9.2';

CREATE TABLE ge.mandate_limit (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  is_simulated boolean NOT NULL DEFAULT false,
  run_id uuid,
  correlation_id uuid,
  state text NOT NULL DEFAULT 'draft',
  payload jsonb NOT NULL DEFAULT '{}'::jsonb,
  region text NOT NULL DEFAULT ge.app_zone(),
  CONSTRAINT pk_mandate_limit PRIMARY KEY (id),
  CONSTRAINT uq_mandate_limit__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_mandate_limit__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.mandate_limit IS 'NEW mandate_limit · scope S · Imm. M · Part 11.17b §11.17.9.2';

CREATE TABLE ge.mandate_window (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  is_simulated boolean NOT NULL DEFAULT false,
  run_id uuid,
  correlation_id uuid,
  state text NOT NULL DEFAULT 'draft',
  payload jsonb NOT NULL DEFAULT '{}'::jsonb,
  region text NOT NULL DEFAULT ge.app_zone(),
  CONSTRAINT pk_mandate_window PRIMARY KEY (id),
  CONSTRAINT uq_mandate_window__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_mandate_window__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.mandate_window IS 'NEW mandate_window · scope S · Imm. M · Part 11.17b §11.17.9.2';

CREATE TABLE ge.mandate_restriction (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  is_simulated boolean NOT NULL DEFAULT false,
  run_id uuid,
  correlation_id uuid,
  mandate_id uuid,
  kind text,
  value jsonb,
  effective_at timestamptz,
  state text NOT NULL DEFAULT 'draft',
  payload jsonb NOT NULL DEFAULT '{}'::jsonb,
  region text NOT NULL DEFAULT ge.app_zone(),
  CONSTRAINT pk_mandate_restriction PRIMARY KEY (id),
  CONSTRAINT uq_mandate_restriction__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_mandate_restriction__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.mandate_restriction IS 'NEW mandate_restriction · scope S · Imm. M · Part 11.17b §11.17.9.2';

CREATE TABLE ge.mandate_counter (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  is_simulated boolean NOT NULL DEFAULT false,
  run_id uuid,
  correlation_id uuid,
  mandate_id uuid,
  period_key text,
  committed_amount numeric(18,2),
  reserved_amount numeric(18,2),
  committed_count integer,
  reserved_count integer,
  state text NOT NULL DEFAULT 'draft',
  payload jsonb NOT NULL DEFAULT '{}'::jsonb,
  region text NOT NULL DEFAULT ge.app_zone(),
  CONSTRAINT pk_mandate_counter PRIMARY KEY (id),
  CONSTRAINT uq_mandate_counter__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_mandate_counter__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.mandate_counter IS 'NEW mandate_counter · scope S · Imm. M · Part 11.17b §11.17.9.2';

CREATE TABLE ge.mandate_consumption (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  is_simulated boolean NOT NULL DEFAULT false,
  run_id uuid,
  correlation_id uuid,
  mandate_id uuid,
  idem_key text,
  amount numeric(20,4),
  currency text,
  state text,
  reserved_at timestamptz,
  committed_at timestamptz,
  receipt_id uuid,
  fence_token text,
  payload jsonb NOT NULL DEFAULT '{}'::jsonb,
  region text NOT NULL DEFAULT ge.app_zone(),
  CONSTRAINT pk_mandate_consumption PRIMARY KEY (id),
  CONSTRAINT uq_mandate_consumption__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_mandate_consumption__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.mandate_consumption IS 'NEW mandate_consumption · scope S · Imm. M · Part 11.17b §11.17.9.2';

CREATE TABLE ge.mandate_decision (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  is_simulated boolean NOT NULL DEFAULT false,
  run_id uuid,
  correlation_id uuid,
  mandate_id uuid,
  step_id uuid,
  level text,
  verdict text,
  reason_code text,
  rule_no integer,
  inputs_hash char(64),
  fence_token bigint,
  state text NOT NULL DEFAULT 'draft',
  payload jsonb NOT NULL DEFAULT '{}'::jsonb,
  region text NOT NULL DEFAULT ge.app_zone(),
  CONSTRAINT pk_mandate_decision PRIMARY KEY (id),
  CONSTRAINT uq_mandate_decision__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_mandate_decision__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.mandate_decision IS 'NEW mandate_decision · scope S · Imm. M · Part 11.17b §11.17.9.2';

CREATE TABLE ge.kill_switch (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  is_simulated boolean NOT NULL DEFAULT false,
  run_id uuid,
  correlation_id uuid,
  scope_type text,
  scope_id uuid,
  engaged text,
  engaged_by text,
  released_by text,
  reason text,
  state text NOT NULL DEFAULT 'draft',
  payload jsonb NOT NULL DEFAULT '{}'::jsonb,
  region text NOT NULL DEFAULT ge.app_zone(),
  CONSTRAINT pk_kill_switch PRIMARY KEY (id),
  CONSTRAINT uq_kill_switch__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_kill_switch__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.kill_switch IS 'NEW kill_switch · scope S · Imm. M · Part 11.17b §11.17.9.2';

CREATE TABLE ge.kill_switch_event (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  is_simulated boolean NOT NULL DEFAULT false,
  run_id uuid,
  correlation_id uuid,
  scope_type text,
  scope_id uuid,
  engaged text,
  engaged_by text,
  released_by text,
  reason text,
  state text NOT NULL DEFAULT 'draft',
  payload jsonb NOT NULL DEFAULT '{}'::jsonb,
  region text NOT NULL DEFAULT ge.app_zone(),
  CONSTRAINT pk_kill_switch_event PRIMARY KEY (id),
  CONSTRAINT uq_kill_switch_event__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_kill_switch_event__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.kill_switch_event IS 'NEW kill_switch_event · scope S · Imm. M · Part 11.17b §11.17.9.2';

CREATE TABLE ge.effect_receipt (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  is_simulated boolean NOT NULL DEFAULT false,
  run_id uuid,
  correlation_id uuid,
  adapter text,
  provider_ref text,
  status text,
  observed_at timestamptz,
  payload_hash char(64),
  s3_key text,
  state text NOT NULL DEFAULT 'draft',
  payload jsonb NOT NULL DEFAULT '{}'::jsonb,
  region text NOT NULL DEFAULT ge.app_zone(),
  CONSTRAINT pk_effect_receipt PRIMARY KEY (id),
  CONSTRAINT uq_effect_receipt__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_effect_receipt__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.effect_receipt IS 'NEW effect_receipt · scope S · Imm. M · Part 11.17b §11.17.9.2';

CREATE TABLE ge.counterparty_agent (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  is_simulated boolean NOT NULL DEFAULT false,
  run_id uuid,
  correlation_id uuid,
  did text,
  tier text,
  kyb_status text,
  registration_ids uuid[],
  instrument_hint text,
  screening_at timestamptz,
  credential text,
  type text,
  status_list_ref text,
  expires_at timestamptz,
  vc_hash char(64),
  state text NOT NULL DEFAULT 'draft',
  payload jsonb NOT NULL DEFAULT '{}'::jsonb,
  region text NOT NULL DEFAULT ge.app_zone(),
  CONSTRAINT pk_counterparty_agent PRIMARY KEY (id),
  CONSTRAINT uq_counterparty_agent__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_counterparty_agent__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.counterparty_agent IS 'NEW counterparty_agent · scope S · Imm. M · Part 11.17b §11.17.9.2';

CREATE TABLE ge.agent_credential (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  is_simulated boolean NOT NULL DEFAULT false,
  run_id uuid,
  correlation_id uuid,
  did text,
  tier text,
  kyb_status text,
  registration_ids uuid[],
  instrument_hint text,
  screening_at timestamptz,
  credential text,
  type text,
  status_list_ref text,
  expires_at timestamptz,
  vc_hash char(64),
  state text NOT NULL DEFAULT 'draft',
  payload jsonb NOT NULL DEFAULT '{}'::jsonb,
  region text NOT NULL DEFAULT ge.app_zone(),
  CONSTRAINT pk_agent_credential PRIMARY KEY (id),
  CONSTRAINT uq_agent_credential__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_agent_credential__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.agent_credential IS 'NEW agent_credential · scope S · Imm. M · Part 11.17b §11.17.9.2';

CREATE TABLE ge.agent_message (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  is_simulated boolean NOT NULL DEFAULT false,
  run_id uuid,
  correlation_id uuid,
  session_id uuid,
  envelope_id uuid,
  direction text,
  type text,
  body_hash char(64),
  s3_key text,
  verified text,
  injection_flag boolean,
  state text NOT NULL DEFAULT 'draft',
  payload jsonb NOT NULL DEFAULT '{}'::jsonb,
  region text NOT NULL DEFAULT ge.app_zone(),
  CONSTRAINT pk_agent_message PRIMARY KEY (id),
  CONSTRAINT uq_agent_message__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_agent_message__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.agent_message IS 'NEW agent_message · scope S · Imm. M · Part 11.17b §11.17.9.2';

CREATE TABLE ge.negotiation_session (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  is_simulated boolean NOT NULL DEFAULT false,
  run_id uuid,
  correlation_id uuid,
  counterparty_id uuid,
  mandate_id uuid,
  state text,
  round text,
  engine_inputs jsonb,
  engine_outputs jsonb,
  payload jsonb NOT NULL DEFAULT '{}'::jsonb,
  region text NOT NULL DEFAULT ge.app_zone(),
  CONSTRAINT pk_negotiation_session PRIMARY KEY (id),
  CONSTRAINT uq_negotiation_session__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_negotiation_session__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.negotiation_session IS 'NEW negotiation_session · scope S · Imm. M · Part 11.17b §11.17.9.2';

CREATE TABLE ge.negotiation_step (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  is_simulated boolean NOT NULL DEFAULT false,
  run_id uuid,
  correlation_id uuid,
  counterparty_id uuid,
  mandate_id uuid,
  state text,
  round text,
  engine_inputs jsonb,
  engine_outputs jsonb,
  payload jsonb NOT NULL DEFAULT '{}'::jsonb,
  region text NOT NULL DEFAULT ge.app_zone(),
  CONSTRAINT pk_negotiation_step PRIMARY KEY (id),
  CONSTRAINT uq_negotiation_step__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_negotiation_step__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.negotiation_step IS 'NEW negotiation_step · scope S · Imm. M · Part 11.17b §11.17.9.2';

CREATE TABLE ge.commerce_order (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  session_id uuid,
  order_ref text,
  lines jsonb,
  total numeric(18,2),
  currency char(3),
  state text,
  signed_confirmation_hash char(64),
  payload jsonb NOT NULL DEFAULT '{}'::jsonb,
  region text NOT NULL DEFAULT ge.app_zone(),
  CONSTRAINT pk_commerce_order PRIMARY KEY (id),
  CONSTRAINT uq_commerce_order__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_commerce_order__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.commerce_order IS 'NEW commerce_order · scope S · Imm. A · Part 11.17b §11.17.9.2';

CREATE TABLE ge.payment_mandate (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  is_simulated boolean NOT NULL DEFAULT false,
  run_id uuid,
  correlation_id uuid,
  mandate_id uuid,
  psp text,
  scheme text,
  psp_ref text,
  max_amount numeric(18,2),
  frequency text,
  status text,
  state text NOT NULL DEFAULT 'draft',
  payload jsonb NOT NULL DEFAULT '{}'::jsonb,
  region text NOT NULL DEFAULT ge.app_zone(),
  CONSTRAINT pk_payment_mandate PRIMARY KEY (id),
  CONSTRAINT uq_payment_mandate__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_payment_mandate__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.payment_mandate IS 'NEW payment_mandate · scope S · Imm. M · Part 11.17b §11.17.9.2';

CREATE TABLE ge.payment_txn (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  is_simulated boolean NOT NULL DEFAULT false,
  run_id uuid,
  correlation_id uuid,
  psp_payment_id text,
  amount numeric(20,4),
  fee numeric(18,2),
  tax text,
  state text,
  deadlines text,
  mandate_id uuid,
  payload jsonb NOT NULL DEFAULT '{}'::jsonb,
  region text NOT NULL DEFAULT ge.app_zone(),
  CONSTRAINT pk_payment_txn PRIMARY KEY (id),
  CONSTRAINT uq_payment_txn__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_payment_txn__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.payment_txn IS 'NEW payment_txn · scope S · Imm. M · Part 11.17b §11.17.9.2';

CREATE TABLE ge.refund (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  is_simulated boolean NOT NULL DEFAULT false,
  run_id uuid,
  correlation_id uuid,
  psp_payment_id uuid,
  amount numeric(18,2),
  fee numeric(18,2),
  tax text,
  state text,
  deadlines text,
  payload jsonb NOT NULL DEFAULT '{}'::jsonb,
  region text NOT NULL DEFAULT ge.app_zone(),
  CONSTRAINT pk_refund PRIMARY KEY (id),
  CONSTRAINT uq_refund__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_refund__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.refund IS 'NEW refund · scope S · Imm. M · Part 11.17b §11.17.9.2';

CREATE TABLE ge.dispute_case (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  is_simulated boolean NOT NULL DEFAULT false,
  run_id uuid,
  correlation_id uuid,
  psp_payment_id uuid,
  amount numeric(18,2),
  fee numeric(18,2),
  tax text,
  state text,
  deadlines text,
  payload jsonb NOT NULL DEFAULT '{}'::jsonb,
  region text NOT NULL DEFAULT ge.app_zone(),
  CONSTRAINT pk_dispute_case PRIMARY KEY (id),
  CONSTRAINT uq_dispute_case__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_dispute_case__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.dispute_case IS 'NEW dispute_case · scope S · Imm. M · Part 11.17b §11.17.9.2';

CREATE TABLE ge.settlement_batch (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  is_simulated boolean NOT NULL DEFAULT false,
  run_id uuid,
  correlation_id uuid,
  psp_payment_id uuid,
  amount numeric(18,2),
  fee numeric(18,2),
  tax text,
  state text,
  deadlines text,
  payload jsonb NOT NULL DEFAULT '{}'::jsonb,
  region text NOT NULL DEFAULT ge.app_zone(),
  CONSTRAINT pk_settlement_batch PRIMARY KEY (id),
  CONSTRAINT uq_settlement_batch__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_settlement_batch__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.settlement_batch IS 'NEW settlement_batch · scope S · Imm. M · Part 11.17b §11.17.9.2';

CREATE TABLE ge.bid_package (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  is_simulated boolean NOT NULL DEFAULT false,
  run_id uuid,
  correlation_id uuid,
  tender_id uuid,
  manifest jsonb,
  package_hash text,
  file text,
  s3_key text,
  state text,
  payload jsonb NOT NULL DEFAULT '{}'::jsonb,
  region text NOT NULL DEFAULT ge.app_zone(),
  CONSTRAINT pk_bid_package PRIMARY KEY (id),
  CONSTRAINT uq_bid_package__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_bid_package__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.bid_package IS 'NEW bid_package · scope S · Imm. M · Part 11.17b §11.17.9.2';

CREATE TABLE ge.bid_file (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  is_simulated boolean NOT NULL DEFAULT false,
  run_id uuid,
  correlation_id uuid,
  tender_id uuid,
  manifest jsonb,
  package_hash char(64),
  file text,
  s3_key text,
  state text NOT NULL DEFAULT 'draft',
  payload jsonb NOT NULL DEFAULT '{}'::jsonb,
  region text NOT NULL DEFAULT ge.app_zone(),
  CONSTRAINT pk_bid_file PRIMARY KEY (id),
  CONSTRAINT uq_bid_file__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_bid_file__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.bid_file IS 'NEW bid_file · scope S · Imm. M · Part 11.17b §11.17.9.2';

CREATE TABLE ge.bid_submission (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  is_simulated boolean NOT NULL DEFAULT false,
  run_id uuid,
  correlation_id uuid,
  package_id uuid,
  mandate_id uuid,
  portal_profile_id uuid,
  mode text,
  idem_key text,
  state text,
  portal_bid_ref text,
  verified text,
  payload jsonb NOT NULL DEFAULT '{}'::jsonb,
  region text NOT NULL DEFAULT ge.app_zone(),
  CONSTRAINT pk_bid_submission PRIMARY KEY (id),
  CONSTRAINT uq_bid_submission__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_bid_submission__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.bid_submission IS 'NEW bid_submission · scope S · Imm. M · Part 11.17b §11.17.9.2';

CREATE TABLE ge.portal_profile (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  is_simulated boolean NOT NULL DEFAULT false,
  run_id uuid,
  correlation_id uuid,
  portal_family text,
  jurisdiction text,
  capability text,
  review_by text,
  review_expires_at timestamptz,
  adapter_version text,
  signing_rule text,
  state text NOT NULL DEFAULT 'draft',
  payload jsonb NOT NULL DEFAULT '{}'::jsonb,
  region text NOT NULL DEFAULT ge.app_zone(),
  CONSTRAINT pk_portal_profile PRIMARY KEY (id),
  CONSTRAINT uq_portal_profile__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_portal_profile__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.portal_profile IS 'NEW portal_profile · scope S · Imm. M · Part 11.17b §11.17.9.2';

CREATE TABLE ge.recon_run (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  is_simulated boolean NOT NULL DEFAULT false,
  run_id uuid,
  correlation_id uuid,
  rule_id uuid,
  mandate_id uuid,
  refs jsonb,
  disposition text,
  state text NOT NULL DEFAULT 'draft',
  payload jsonb NOT NULL DEFAULT '{}'::jsonb,
  region text NOT NULL DEFAULT ge.app_zone(),
  CONSTRAINT pk_recon_run PRIMARY KEY (id),
  CONSTRAINT uq_recon_run__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_recon_run__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.recon_run IS 'NEW recon_run · scope S · Imm. M · Part 11.17b §11.17.9.2';

CREATE TABLE ge.recon_break (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  is_simulated boolean NOT NULL DEFAULT false,
  run_id uuid,
  correlation_id uuid,
  rule_id uuid,
  mandate_id uuid,
  refs jsonb,
  disposition text,
  state text NOT NULL DEFAULT 'draft',
  payload jsonb NOT NULL DEFAULT '{}'::jsonb,
  region text NOT NULL DEFAULT ge.app_zone(),
  CONSTRAINT pk_recon_break PRIMARY KEY (id),
  CONSTRAINT uq_recon_break__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_recon_break__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.recon_break IS 'NEW recon_break · scope S · Imm. M · Part 11.17b §11.17.9.2';

CREATE TABLE ge.ledger_entry (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  is_simulated boolean NOT NULL DEFAULT false,
  run_id uuid,
  correlation_id uuid,
  journal_id uuid,
  account text,
  debit numeric(20,4),
  credit numeric(20,4),
  state text NOT NULL DEFAULT 'draft',
  payload jsonb NOT NULL DEFAULT '{}'::jsonb,
  region text NOT NULL DEFAULT ge.app_zone(),
  CONSTRAINT pk_ledger_entry PRIMARY KEY (id),
  CONSTRAINT uq_ledger_entry__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_ledger_entry__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.ledger_entry IS 'NEW ledger_entry · scope S · Imm. M · Part 11.17b §11.17.9.2 (ER)';

CREATE TABLE ge.voice_session (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  is_simulated boolean NOT NULL DEFAULT false,
  run_id uuid,
  correlation_id uuid,
  call_ref text,
  direction text,
  state text,
  campaign_id uuid,
  contact_id uuid,
  number_id uuid,
  remote_number_hash char(64),
  jurisdiction_set text,
  language text,
  language_tier text,
  script_version_id uuid,
  disclosure_played_at timestamptz,
  disclosure_template_hash char(64),
  recording_state text,
  recording_permission_ref text,
  verified_caller text,
  risk_band text,
  disposition text,
  booking_ref text,
  transcript_ref text,
  call_event_ref text,
  answered_at timestamptz,
  ended_at timestamptz,
  connected_seconds integer,
  degradation_level text,
  preflight_verdict_id uuid,
  payload jsonb NOT NULL DEFAULT '{}'::jsonb,
  region text NOT NULL DEFAULT ge.app_zone(),
  CONSTRAINT pk_voice_session PRIMARY KEY (id),
  CONSTRAINT uq_voice_session__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_voice_session__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.voice_session IS 'NEW voice_session · scope S · Imm. M · Part 11.18b §11.18.5.24';

CREATE TABLE ge.voice_leg (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  is_simulated boolean NOT NULL DEFAULT false,
  run_id uuid,
  correlation_id uuid,
  session_id uuid,
  party_type text,
  party_ref text,
  joined_at timestamptz,
  left_at timestamptz,
  consent_state text,
  channel_index text,
  state text NOT NULL DEFAULT 'draft',
  payload jsonb NOT NULL DEFAULT '{}'::jsonb,
  region text NOT NULL DEFAULT ge.app_zone(),
  CONSTRAINT pk_voice_leg PRIMARY KEY (id),
  CONSTRAINT uq_voice_leg__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_voice_leg__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.voice_leg IS 'NEW voice_leg · scope S · Imm. M · Part 11.18b §11.18.5.24';

CREATE TABLE ge.voice_campaign (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  is_simulated boolean NOT NULL DEFAULT false,
  run_id uuid,
  correlation_id uuid,
  purpose_code text,
  digest_sha256 text,
  list_snapshot_hash char(64),
  languages text[],
  voice_id uuid,
  window_policy text,
  caps jsonb,
  voicemail_policy text,
  recording_mode text,
  budget_minor numeric(18,2),
  expires_at timestamptz,
  approval_id uuid,
  mandate_id uuid,
  state text,
  payload jsonb NOT NULL DEFAULT '{}'::jsonb,
  region text NOT NULL DEFAULT ge.app_zone(),
  CONSTRAINT pk_voice_campaign PRIMARY KEY (id),
  CONSTRAINT uq_voice_campaign__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_voice_campaign__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.voice_campaign IS 'NEW voice_campaign · scope S · Imm. M · Part 11.18b §11.18.5.24';

CREATE TABLE ge.voice_campaign_contact (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  is_simulated boolean NOT NULL DEFAULT false,
  run_id uuid,
  correlation_id uuid,
  campaign_id uuid,
  contact_id uuid,
  variant_id uuid,
  slot_values text,
  attempts integer,
  next_eligible_at timestamptz,
  last_verdict text,
  last_reasons text[],
  state text NOT NULL DEFAULT 'draft',
  payload jsonb NOT NULL DEFAULT '{}'::jsonb,
  region text NOT NULL DEFAULT ge.app_zone(),
  CONSTRAINT pk_voice_campaign_contact PRIMARY KEY (id),
  CONSTRAINT uq_voice_campaign_contact__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_voice_campaign_contact__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.voice_campaign_contact IS 'NEW voice_campaign_contact · scope S · Imm. M · Part 11.18b §11.18.5.24';

CREATE TABLE ge.voice_script (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  is_simulated boolean NOT NULL DEFAULT false,
  run_id uuid,
  correlation_id uuid,
  kind text,
  language text,
  text text,
  sha256 text,
  state text,
  approved_by text,
  approved_at timestamptz,
  pack_check_id uuid,
  payload jsonb NOT NULL DEFAULT '{}'::jsonb,
  region text NOT NULL DEFAULT ge.app_zone(),
  CONSTRAINT pk_voice_script PRIMARY KEY (id),
  CONSTRAINT uq_voice_script__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_voice_script__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.voice_script IS 'NEW voice_script · scope S · Imm. M · Part 11.18b §11.18.5.24';

CREATE TABLE ge.voice_script_version (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  is_simulated boolean NOT NULL DEFAULT false,
  run_id uuid,
  correlation_id uuid,
  kind text,
  language text,
  text text,
  sha256 text,
  state text,
  approved_by text,
  approved_at timestamptz,
  pack_check_id uuid,
  payload jsonb NOT NULL DEFAULT '{}'::jsonb,
  region text NOT NULL DEFAULT ge.app_zone(),
  CONSTRAINT pk_voice_script_version PRIMARY KEY (id),
  CONSTRAINT uq_voice_script_version__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_voice_script_version__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.voice_script_version IS 'NEW voice_script_version · scope S · Imm. M · Part 11.18b §11.18.5.24';

ALTER TABLE ge.voice_number ADD COLUMN IF NOT EXISTS id uuid DEFAULT gen_random_uuid();

ALTER TABLE ge.voice_number ADD COLUMN IF NOT EXISTS startup_id uuid;

ALTER TABLE ge.voice_number ADD COLUMN IF NOT EXISTS revision integer DEFAULT 1;

ALTER TABLE ge.voice_number ADD COLUMN IF NOT EXISTS created_at timestamptz DEFAULT now();

ALTER TABLE ge.voice_number ADD COLUMN IF NOT EXISTS created_by uuid;

ALTER TABLE ge.voice_number ADD COLUMN IF NOT EXISTS created_by_type text DEFAULT 'user';

ALTER TABLE ge.voice_number ADD COLUMN IF NOT EXISTS updated_at timestamptz DEFAULT now();

ALTER TABLE ge.voice_number ADD COLUMN IF NOT EXISTS updated_by uuid;

ALTER TABLE ge.voice_number ADD COLUMN IF NOT EXISTS archived_at timestamptz;

ALTER TABLE ge.voice_number ADD COLUMN IF NOT EXISTS archived_by uuid;

ALTER TABLE ge.voice_number ADD COLUMN IF NOT EXISTS archive_reason text;

ALTER TABLE ge.voice_number ADD COLUMN IF NOT EXISTS is_simulated boolean DEFAULT false;

ALTER TABLE ge.voice_number ADD COLUMN IF NOT EXISTS run_id uuid;

ALTER TABLE ge.voice_number ADD COLUMN IF NOT EXISTS correlation_id uuid;

ALTER TABLE ge.voice_number ADD COLUMN IF NOT EXISTS country text;

ALTER TABLE ge.voice_number ADD COLUMN IF NOT EXISTS type text;

ALTER TABLE ge.voice_number ADD COLUMN IF NOT EXISTS purpose_pool text;

ALTER TABLE ge.voice_number ADD COLUMN IF NOT EXISTS provider text;

ALTER TABLE ge.voice_number ADD COLUMN IF NOT EXISTS registration jsonb;

ALTER TABLE ge.voice_number ADD COLUMN IF NOT EXISTS reputation_state text;

ALTER TABLE ge.voice_number ADD COLUMN IF NOT EXISTS state text;

ALTER TABLE ge.voice_number ADD COLUMN IF NOT EXISTS assigned_company_id uuid;

ALTER TABLE ge.voice_number ADD COLUMN IF NOT EXISTS routing_config jsonb;

ALTER TABLE ge.voice_number ADD COLUMN IF NOT EXISTS payload jsonb DEFAULT '{}'::jsonb;

ALTER TABLE ge.voice_number ADD COLUMN IF NOT EXISTS region text DEFAULT ge.app_zone();

CREATE TABLE ge.voice_number_pool (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  is_simulated boolean NOT NULL DEFAULT false,
  run_id uuid,
  correlation_id uuid,
  e164 text,
  country text,
  type text,
  purpose_pool text,
  provider text,
  registration jsonb,
  reputation_state text,
  state text,
  assigned_company_id uuid,
  routing_config jsonb,
  payload jsonb NOT NULL DEFAULT '{}'::jsonb,
  region text NOT NULL DEFAULT ge.app_zone(),
  CONSTRAINT pk_voice_number_pool PRIMARY KEY (id),
  CONSTRAINT uq_voice_number_pool__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_voice_number_pool__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.voice_number_pool IS 'NEW voice_number_pool · scope S · Imm. M · Part 11.18b §11.18.5.24';

CREATE TABLE ge.voice_scrub_result (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  is_simulated boolean NOT NULL DEFAULT false,
  run_id uuid,
  correlation_id uuid,
  registry text,
  list_version text,
  queried_at timestamptz,
  result jsonb,
  override_consent_id uuid,
  state text NOT NULL DEFAULT 'draft',
  payload jsonb NOT NULL DEFAULT '{}'::jsonb,
  region text NOT NULL DEFAULT ge.app_zone(),
  CONSTRAINT pk_voice_scrub_result PRIMARY KEY (id),
  CONSTRAINT uq_voice_scrub_result__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_voice_scrub_result__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.voice_scrub_result IS 'NEW voice_scrub_result · scope S · Imm. M · Part 11.18b §11.18.5.24';

CREATE TABLE ge.voice_consent_evidence (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  is_simulated boolean NOT NULL DEFAULT false,
  run_id uuid,
  correlation_id uuid,
  consent_id uuid,
  purpose text,
  method text,
  prompt_hash text,
  asr_confidence text,
  dtmf_digit text,
  evidence_ref text,
  captured_at timestamptz,
  session_id uuid,
  state text NOT NULL DEFAULT 'draft',
  payload jsonb NOT NULL DEFAULT '{}'::jsonb,
  region text NOT NULL DEFAULT ge.app_zone(),
  CONSTRAINT pk_voice_consent_evidence PRIMARY KEY (id),
  CONSTRAINT uq_voice_consent_evidence__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_voice_consent_evidence__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.voice_consent_evidence IS 'NEW voice_consent_evidence · scope S · Imm. M · Part 11.18b §11.18.5.24';

CREATE TABLE ge.voice_recording (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  is_simulated boolean NOT NULL DEFAULT false,
  run_id uuid,
  correlation_id uuid,
  s3_key text,
  sha256 text,
  codec text,
  channels text[],
  duration_ms integer,
  kms_key_version text,
  redaction_state text,
  delete_after timestamptz,
  deleted_at timestamptz,
  deletion_receipt text,
  session_id uuid,
  state text NOT NULL DEFAULT 'draft',
  payload jsonb NOT NULL DEFAULT '{}'::jsonb,
  region text NOT NULL DEFAULT ge.app_zone(),
  CONSTRAINT pk_voice_recording PRIMARY KEY (id),
  CONSTRAINT uq_voice_recording__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_voice_recording__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.voice_recording IS 'NEW voice_recording · scope S · Imm. M · Part 11.18b §11.18.5.24';

CREATE TABLE ge.voice_transcript (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  is_simulated boolean NOT NULL DEFAULT false,
  run_id uuid,
  correlation_id uuid,
  segment text,
  start_ms integer,
  end_ms integer,
  text_redacted text,
  language text,
  confidence numeric(7,4),
  transcript text,
  model_id uuid,
  redaction_versions text,
  state text NOT NULL DEFAULT 'draft',
  payload jsonb NOT NULL DEFAULT '{}'::jsonb,
  region text NOT NULL DEFAULT ge.app_zone(),
  CONSTRAINT pk_voice_transcript PRIMARY KEY (id),
  CONSTRAINT uq_voice_transcript__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_voice_transcript__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.voice_transcript IS 'NEW voice_transcript · scope S · Imm. M · Part 11.18b §11.18.5.24';

CREATE TABLE ge.voice_transcript_segment (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  is_simulated boolean NOT NULL DEFAULT false,
  run_id uuid,
  correlation_id uuid,
  segment text,
  start_ms integer,
  end_ms integer,
  text_redacted text,
  language text,
  confidence numeric(7,4),
  transcript text,
  model_id uuid,
  redaction_versions text,
  state text NOT NULL DEFAULT 'draft',
  payload jsonb NOT NULL DEFAULT '{}'::jsonb,
  region text NOT NULL DEFAULT ge.app_zone(),
  CONSTRAINT pk_voice_transcript_segment PRIMARY KEY (id),
  CONSTRAINT uq_voice_transcript_segment__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_voice_transcript_segment__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.voice_transcript_segment IS 'NEW voice_transcript_segment · scope S · Imm. M · Part 11.18b §11.18.5.24';

CREATE TABLE ge.voice_summary (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  is_simulated boolean NOT NULL DEFAULT false,
  run_id uuid,
  correlation_id uuid,
  approved_by text,
  synced_at timestamptz,
  state text NOT NULL DEFAULT 'draft',
  payload jsonb NOT NULL DEFAULT '{}'::jsonb,
  region text NOT NULL DEFAULT ge.app_zone(),
  CONSTRAINT pk_voice_summary PRIMARY KEY (id),
  CONSTRAINT uq_voice_summary__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_voice_summary__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.voice_summary IS 'NEW voice_summary · scope S · Imm. M · Part 11.18b §11.18.5.24';

CREATE TABLE ge.voice_handoff (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  is_simulated boolean NOT NULL DEFAULT false,
  run_id uuid,
  correlation_id uuid,
  trigger text,
  brief text,
  queued_at timestamptz,
  answered_at timestamptz,
  agent_id uuid,
  outcome text,
  callback_due_at timestamptz,
  state text NOT NULL DEFAULT 'draft',
  payload jsonb NOT NULL DEFAULT '{}'::jsonb,
  region text NOT NULL DEFAULT ge.app_zone(),
  CONSTRAINT pk_voice_handoff PRIMARY KEY (id),
  CONSTRAINT uq_voice_handoff__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_voice_handoff__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.voice_handoff IS 'NEW voice_handoff · scope S · Imm. M · Part 11.18b §11.18.5.24';

CREATE TABLE ge.voice_voicemail (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  is_simulated boolean NOT NULL DEFAULT false,
  run_id uuid,
  correlation_id uuid,
  template_hash char(64),
  left_at timestamptz,
  amd_result text,
  state text NOT NULL DEFAULT 'draft',
  payload jsonb NOT NULL DEFAULT '{}'::jsonb,
  region text NOT NULL DEFAULT ge.app_zone(),
  CONSTRAINT pk_voice_voicemail PRIMARY KEY (id),
  CONSTRAINT uq_voice_voicemail__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_voice_voicemail__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.voice_voicemail IS 'NEW voice_voicemail · scope S · Imm. M · Part 11.18b §11.18.5.24';

CREATE TABLE ge.voice_meter_event (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  is_simulated boolean NOT NULL DEFAULT false,
  run_id uuid,
  correlation_id uuid,
  leg_id uuid,
  billable_minutes integer,
  provider_cost_minor numeric(18,2),
  currency char(3),
  event_key text,
  reservation_id uuid,
  state text NOT NULL DEFAULT 'draft',
  payload jsonb NOT NULL DEFAULT '{}'::jsonb,
  region text NOT NULL DEFAULT ge.app_zone(),
  CONSTRAINT pk_voice_meter_event PRIMARY KEY (id),
  CONSTRAINT uq_voice_meter_event__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_voice_meter_event__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.voice_meter_event IS 'NEW voice_meter_event · scope S · Imm. M · Part 11.18b §11.18.5.24';

CREATE TABLE ge.voice_access_log (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  is_simulated boolean NOT NULL DEFAULT false,
  run_id uuid,
  correlation_id uuid,
  actor_id uuid,
  purpose_code text,
  action text,
  ip text,
  outcome text,
  at text,
  state text NOT NULL DEFAULT 'draft',
  payload jsonb NOT NULL DEFAULT '{}'::jsonb,
  region text NOT NULL DEFAULT ge.app_zone(),
  CONSTRAINT pk_voice_access_log PRIMARY KEY (id),
  CONSTRAINT uq_voice_access_log__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_voice_access_log__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.voice_access_log IS 'NEW voice_access_log · scope S · Imm. M · Part 11.18b §11.18.5.24';

CREATE TABLE ge.voice_legal_hold (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  is_simulated boolean NOT NULL DEFAULT false,
  run_id uuid,
  correlation_id uuid,
  scope jsonb,
  reason text,
  set_by text,
  released_by text,
  state text NOT NULL DEFAULT 'draft',
  payload jsonb NOT NULL DEFAULT '{}'::jsonb,
  region text NOT NULL DEFAULT ge.app_zone(),
  CONSTRAINT pk_voice_legal_hold PRIMARY KEY (id),
  CONSTRAINT uq_voice_legal_hold__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_voice_legal_hold__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.voice_legal_hold IS 'NEW voice_legal_hold · scope S · Imm. M · Part 11.18b §11.18.5.24';

CREATE TABLE ge.coaching_rubric (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  is_simulated boolean NOT NULL DEFAULT false,
  run_id uuid,
  correlation_id uuid,
  rubric text,
  feedback numeric(18,2),
  source_session_id uuid,
  observations text,
  rubric_version text,
  share text,
  revoked_at timestamptz,
  state text NOT NULL DEFAULT 'draft',
  payload jsonb NOT NULL DEFAULT '{}'::jsonb,
  region text NOT NULL DEFAULT ge.app_zone(),
  CONSTRAINT pk_coaching_rubric PRIMARY KEY (id),
  CONSTRAINT uq_coaching_rubric__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_coaching_rubric__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.coaching_rubric IS 'NEW coaching_rubric · scope S · Imm. M · Part 11.18b §11.18.5.24';

CREATE TABLE ge.coaching_feedback (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  is_simulated boolean NOT NULL DEFAULT false,
  run_id uuid,
  correlation_id uuid,
  rubric text,
  feedback numeric(18,2),
  source_session_id uuid,
  observations text,
  rubric_version text,
  share text,
  revoked_at timestamptz,
  state text NOT NULL DEFAULT 'draft',
  payload jsonb NOT NULL DEFAULT '{}'::jsonb,
  region text NOT NULL DEFAULT ge.app_zone(),
  CONSTRAINT pk_coaching_feedback PRIMARY KEY (id),
  CONSTRAINT uq_coaching_feedback__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_coaching_feedback__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.coaching_feedback IS 'NEW coaching_feedback · scope S · Imm. M · Part 11.18b §11.18.5.24';

CREATE TABLE ge.coaching_share (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL,
  startup_id uuid NOT NULL,
  revision integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by uuid,
  created_by_type text NOT NULL DEFAULT 'user',
  updated_at timestamptz NOT NULL DEFAULT now(),
  updated_by uuid,
  archived_at timestamptz,
  archived_by uuid,
  archive_reason text,
  is_simulated boolean NOT NULL DEFAULT false,
  run_id uuid,
  correlation_id uuid,
  rubric text,
  feedback numeric(18,2),
  source_session_id uuid,
  observations text,
  rubric_version text,
  share text,
  revoked_at timestamptz,
  state text NOT NULL DEFAULT 'draft',
  payload jsonb NOT NULL DEFAULT '{}'::jsonb,
  region text NOT NULL DEFAULT ge.app_zone(),
  CONSTRAINT pk_coaching_share PRIMARY KEY (id),
  CONSTRAINT uq_coaching_share__tenant_id_id UNIQUE (tenant_id, id),
  CONSTRAINT uq_coaching_share__scope_id UNIQUE (tenant_id, startup_id, id)
);

COMMENT ON TABLE ge.coaching_share IS 'NEW coaching_share · scope S · Imm. M · Part 11.18b §11.18.5.24';
