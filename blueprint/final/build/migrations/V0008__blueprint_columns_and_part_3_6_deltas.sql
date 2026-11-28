-- V0008__blueprint_columns_and_part_3_6_deltas
SET search_path = ge, extensions, public;

SELECT set_config('app.zone', coalesce(nullif(current_setting('app.deployment_region', true), ''), 'IN'), false);

SELECT set_config('app.deployment_region', coalesce(nullif(current_setting('app.deployment_region', true), ''), 'IN'), false);

ALTER TABLE ge.tenant ADD COLUMN IF NOT EXISTS slug text;

ALTER TABLE ge.tenant ADD COLUMN IF NOT EXISTS display_name text;

ALTER TABLE ge.tenant ADD COLUMN IF NOT EXISTS legal_name text;

ALTER TABLE ge.tenant ADD COLUMN IF NOT EXISTS legal_id text;

ALTER TABLE ge.tenant ADD COLUMN IF NOT EXISTS ownership_type text;

ALTER TABLE ge.tenant ADD COLUMN IF NOT EXISTS service_model text;

ALTER TABLE ge.tenant ADD COLUMN IF NOT EXISTS lifecycle_state text;

ALTER TABLE ge.tenant ADD COLUMN IF NOT EXISTS home_region text;

ALTER TABLE ge.tenant ADD COLUMN IF NOT EXISTS kms_key_arn text;

ALTER TABLE ge.tenant ADD COLUMN IF NOT EXISTS storage_prefix text;

ALTER TABLE ge.tenant ADD COLUMN IF NOT EXISTS source_application_id uuid;

ALTER TABLE ge.tenant ADD COLUMN IF NOT EXISTS audit_genesis_hash char(64);

ALTER TABLE ge.tenant ADD COLUMN IF NOT EXISTS suspended_reason text;

ALTER TABLE ge.company ADD COLUMN IF NOT EXISTS slug text;

ALTER TABLE ge.company ADD COLUMN IF NOT EXISTS display_name text;

ALTER TABLE ge.company ADD COLUMN IF NOT EXISTS country_code char(2);

ALTER TABLE ge.company ADD COLUMN IF NOT EXISTS base_currency char(3);

ALTER TABLE ge.company ADD COLUMN IF NOT EXISTS business_timezone text;

ALTER TABLE ge.company ADD COLUMN IF NOT EXISTS default_locale text;

ALTER TABLE ge.company ADD COLUMN IF NOT EXISTS lifecycle_state text;

ALTER TABLE ge.company ADD COLUMN IF NOT EXISTS template_ref uuid;

ALTER TABLE ge.company ADD COLUMN IF NOT EXISTS margin_floor_pct numeric(7,4);

ALTER TABLE ge.company ADD COLUMN IF NOT EXISTS tax_profile_id uuid;

ALTER TABLE ge.company ADD COLUMN IF NOT EXISTS emergency_stop boolean;

ALTER TABLE ge.division ADD COLUMN IF NOT EXISTS code text;

ALTER TABLE ge.division ADD COLUMN IF NOT EXISTS description text;

ALTER TABLE ge.division ADD COLUMN IF NOT EXISTS owner_id uuid;

ALTER TABLE ge.offering ADD COLUMN IF NOT EXISTS business_line_id uuid;

ALTER TABLE ge.offering ADD COLUMN IF NOT EXISTS code text;

ALTER TABLE ge.offering ADD COLUMN IF NOT EXISTS name text;

ALTER TABLE ge.offering ADD COLUMN IF NOT EXISTS offering_kind text;

ALTER TABLE ge.offering ADD COLUMN IF NOT EXISTS readiness_state text;

ALTER TABLE ge.offering ADD COLUMN IF NOT EXISTS current_version_id uuid;

ALTER TABLE ge.offering ADD COLUMN IF NOT EXISTS is_promotable boolean;

ALTER TABLE ge.offering ADD COLUMN IF NOT EXISTS owner_id uuid;

ALTER TABLE ge.channel_account ADD COLUMN IF NOT EXISTS integration_id uuid;

ALTER TABLE ge.channel_account ADD COLUMN IF NOT EXISTS sender_identity text;

ALTER TABLE ge.channel_account ADD COLUMN IF NOT EXISTS ses_configuration_set text;

ALTER TABLE ge.channel_account ADD COLUMN IF NOT EXISTS reputation_state text;

ALTER TABLE ge.workflow_run ADD COLUMN IF NOT EXISTS workflow_revision_id uuid;

ALTER TABLE ge.workflow_run ADD COLUMN IF NOT EXISTS trigger_id uuid;

ALTER TABLE ge.workflow_run ADD COLUMN IF NOT EXISTS trigger_event_id text;

ALTER TABLE ge.workflow_run ADD COLUMN IF NOT EXISTS autonomy_plan_id uuid;

ALTER TABLE ge.workflow_run ADD COLUMN IF NOT EXISTS mode text;

ALTER TABLE ge.workflow_run ADD COLUMN IF NOT EXISTS state text;

ALTER TABLE ge.workflow_run ADD COLUMN IF NOT EXISTS current_node_key text;

ALTER TABLE ge.workflow_run ADD COLUMN IF NOT EXISTS wait_reason text;

ALTER TABLE ge.workflow_run ADD COLUMN IF NOT EXISTS due_at timestamptz;

ALTER TABLE ge.workflow_run ADD COLUMN IF NOT EXISTS started_at timestamptz;

ALTER TABLE ge.workflow_run ADD COLUMN IF NOT EXISTS finished_at timestamptz;

ALTER TABLE ge.workflow_run ADD COLUMN IF NOT EXISTS cost_reserved numeric(18,4);

ALTER TABLE ge.workflow_run ADD COLUMN IF NOT EXISTS cost_actual numeric(18,4);

ALTER TABLE ge.workflow_run ADD COLUMN IF NOT EXISTS outcome_certainty text;

ALTER TABLE ge.workflow_run ADD COLUMN IF NOT EXISTS step_count smallint;

ALTER TABLE ge.workflow_run ADD COLUMN IF NOT EXISTS owner_id uuid;

ALTER TABLE ge.workflow_step_run ADD COLUMN IF NOT EXISTS node_key text;

ALTER TABLE ge.workflow_step_run ADD COLUMN IF NOT EXISTS node_type text;

ALTER TABLE ge.workflow_step_run ADD COLUMN IF NOT EXISTS state text;

ALTER TABLE ge.workflow_step_run ADD COLUMN IF NOT EXISTS side_effect_class text;

ALTER TABLE ge.workflow_step_run ADD COLUMN IF NOT EXISTS idempotency_key text;

ALTER TABLE ge.workflow_step_run ADD COLUMN IF NOT EXISTS policy_decision_id uuid;

ALTER TABLE ge.workflow_step_run ADD COLUMN IF NOT EXISTS outcome_certainty text;

ALTER TABLE ge.workflow_step_run ADD COLUMN IF NOT EXISTS error_class text;

ALTER TABLE ge.workflow_step_run ADD COLUMN IF NOT EXISTS output_digest char(64);

ALTER TABLE ge.outbox ADD COLUMN IF NOT EXISTS aggregate_type text;

ALTER TABLE ge.outbox ADD COLUMN IF NOT EXISTS aggregate_id text;

ALTER TABLE ge.outbox ADD COLUMN IF NOT EXISTS aggregate_revision integer;

ALTER TABLE ge.outbox ADD COLUMN IF NOT EXISTS status text;

ALTER TABLE ge.outbox ADD COLUMN IF NOT EXISTS available_at timestamptz;

ALTER TABLE ge.outbox ADD COLUMN IF NOT EXISTS last_error text;

ALTER TABLE ge.outbox ADD COLUMN IF NOT EXISTS dispatched_at timestamptz;

ALTER TABLE ge.audit_event ADD COLUMN IF NOT EXISTS event_id uuid;

ALTER TABLE ge.audit_event ADD COLUMN IF NOT EXISTS scope_type text;

ALTER TABLE ge.audit_event ADD COLUMN IF NOT EXISTS actor_type text;

ALTER TABLE ge.audit_event ADD COLUMN IF NOT EXISTS actor_id text;

ALTER TABLE ge.audit_event ADD COLUMN IF NOT EXISTS actor_role text;

ALTER TABLE ge.audit_event ADD COLUMN IF NOT EXISTS session_id text;

ALTER TABLE ge.audit_event ADD COLUMN IF NOT EXISTS mfa_at timestamptz;

ALTER TABLE ge.audit_event ADD COLUMN IF NOT EXISTS on_behalf_of uuid;

ALTER TABLE ge.audit_event ADD COLUMN IF NOT EXISTS object_id text;

ALTER TABLE ge.audit_event ADD COLUMN IF NOT EXISTS object_revision text;

ALTER TABLE ge.audit_event ADD COLUMN IF NOT EXISTS outcome text;

ALTER TABLE ge.audit_event ADD COLUMN IF NOT EXISTS reason_codes text[];

ALTER TABLE ge.audit_event ADD COLUMN IF NOT EXISTS before_digest char(64);

ALTER TABLE ge.audit_event ADD COLUMN IF NOT EXISTS after_digest char(64);

ALTER TABLE ge.audit_event ADD COLUMN IF NOT EXISTS field_diff jsonb;

ALTER TABLE ge.audit_event ADD COLUMN IF NOT EXISTS run_id uuid;

ALTER TABLE ge.audit_event ADD COLUMN IF NOT EXISTS request_id uuid;

ALTER TABLE ge.audit_event ADD COLUMN IF NOT EXISTS ip inet;

ALTER TABLE ge.audit_event ADD COLUMN IF NOT EXISTS ip_hmac char(64);

ALTER TABLE ge.audit_event ADD COLUMN IF NOT EXISTS user_agent_hmac char(64);

ALTER TABLE ge.audit_event ADD COLUMN IF NOT EXISTS retention_class text;

ALTER TABLE ge.audit_event ADD COLUMN IF NOT EXISTS seq bigint;

ALTER TABLE ge.audit_event ADD COLUMN IF NOT EXISTS hash char(64);

ALTER TABLE ge.fx_rate ADD COLUMN IF NOT EXISTS rate_source text;

ALTER TABLE ge.fx_rate ADD COLUMN IF NOT EXISTS rate_date date;

ALTER TABLE ge.jurisdiction_rule ADD COLUMN IF NOT EXISTS country_code text;

ALTER TABLE ge.jurisdiction_rule ADD COLUMN IF NOT EXISTS pack_code text;

ALTER TABLE ge.jurisdiction_rule ADD COLUMN IF NOT EXISTS outbound_mode text;

ALTER TABLE ge.jurisdiction_rule ADD COLUMN IF NOT EXISTS requires_lia text;

ALTER TABLE ge.jurisdiction_rule ADD COLUMN IF NOT EXISTS opt_out_sla_days integer;

ALTER TABLE ge.jurisdiction_rule ADD COLUMN IF NOT EXISTS quiet_hours jsonb;

ALTER TABLE ge.consent_record ADD COLUMN IF NOT EXISTS subject_hmac char(64);

ALTER TABLE ge.consent_record ADD COLUMN IF NOT EXISTS action text;

ALTER TABLE ge.consent_record ADD COLUMN IF NOT EXISTS lawful_basis text;

ALTER TABLE ge.consent_record ADD COLUMN IF NOT EXISTS lia_ref uuid;

ALTER TABLE ge.consent_record ADD COLUMN IF NOT EXISTS policy_version_id uuid;

ALTER TABLE ge.consent_record ADD COLUMN IF NOT EXISTS capture_method text;

ALTER TABLE ge.consent_record ADD COLUMN IF NOT EXISTS evidence_ref text;

ALTER TABLE ge.consent_record ADD COLUMN IF NOT EXISTS guardian_contact_id uuid;

ALTER TABLE ge.consent_record ADD COLUMN IF NOT EXISTS jurisdiction_code char(2);

ALTER TABLE ge.consent_record ADD COLUMN IF NOT EXISTS effective_at timestamptz;

ALTER TABLE ge.consent_record ADD COLUMN IF NOT EXISTS expires_at timestamptz;

ALTER TABLE ge.suppression ADD COLUMN IF NOT EXISTS identifier_hmac char(64);

ALTER TABLE ge.suppression ADD COLUMN IF NOT EXISTS identifier_kind text;

ALTER TABLE ge.suppression ADD COLUMN IF NOT EXISTS scope_level text;

ALTER TABLE ge.suppression ADD COLUMN IF NOT EXISTS expires_at timestamptz;

ALTER TABLE ge.suppression ADD COLUMN IF NOT EXISTS lifted_by_id uuid;

ALTER TABLE ge.dsar_request ADD COLUMN IF NOT EXISTS subject_hmac char(64);

ALTER TABLE ge.dsar_request ADD COLUMN IF NOT EXISTS contact_ids uuid;

ALTER TABLE ge.dsar_request ADD COLUMN IF NOT EXISTS identity_verification text;

ALTER TABLE ge.dsar_request ADD COLUMN IF NOT EXISTS state text;

ALTER TABLE ge.dsar_request ADD COLUMN IF NOT EXISTS escalate_at timestamptz;

ALTER TABLE ge.dsar_request ADD COLUMN IF NOT EXISTS legal_hold_id uuid;

ALTER TABLE ge.dsar_request ADD COLUMN IF NOT EXISTS fulfilment_report_key text;

ALTER TABLE ge.incident ADD COLUMN IF NOT EXISTS incident_type text;

ALTER TABLE ge.incident ADD COLUMN IF NOT EXISTS state text;

ALTER TABLE ge.incident ADD COLUMN IF NOT EXISTS containment_action text;

ALTER TABLE ge.incident ADD COLUMN IF NOT EXISTS affected_scope text;

ALTER TABLE ge.incident ADD COLUMN IF NOT EXISTS opened_at timestamptz;

ALTER TABLE ge.incident ADD COLUMN IF NOT EXISTS resolved_at timestamptz;

ALTER TABLE ge.incident ADD COLUMN IF NOT EXISTS dpb_notified_at timestamptz;

ALTER TABLE ge.prompt_version ADD COLUMN IF NOT EXISTS prompt_code text;

ALTER TABLE ge.prompt_version ADD COLUMN IF NOT EXISTS output_schema jsonb;

ALTER TABLE ge.prompt_version ADD COLUMN IF NOT EXISTS eval_run_id uuid;

ALTER TABLE ge.prompt_version ADD COLUMN IF NOT EXISTS model_routing jsonb;

ALTER TABLE ge.eval_run ADD COLUMN IF NOT EXISTS suite_code text;

ALTER TABLE ge.eval_run ADD COLUMN IF NOT EXISTS prompt_version_id uuid;

ALTER TABLE ge.eval_run ADD COLUMN IF NOT EXISTS precision_score numeric(9,4);

ALTER TABLE ge.eval_run ADD COLUMN IF NOT EXISTS recall_score numeric(9,4);

ALTER TABLE ge.eval_run ADD COLUMN IF NOT EXISTS abstention_rate numeric(7,4);

ALTER TABLE ge.eval_run ADD COLUMN IF NOT EXISTS cost_total numeric(18,2);

ALTER TABLE ge.eval_run ADD COLUMN IF NOT EXISTS gate_result text;

ALTER TABLE ge.ai_usage_event ADD COLUMN IF NOT EXISTS model_run_id uuid;

ALTER TABLE ge.ai_usage_event ADD COLUMN IF NOT EXISTS provider_call_ref text;

ALTER TABLE ge.ai_usage_event ADD COLUMN IF NOT EXISTS unit text;

ALTER TABLE ge.ai_usage_event ADD COLUMN IF NOT EXISTS quantity numeric(18,4);

ALTER TABLE ge.ai_usage_event ADD COLUMN IF NOT EXISTS unit_cost numeric(18,2);

ALTER TABLE ge.ai_budget ADD COLUMN IF NOT EXISTS budget_code text;

ALTER TABLE ge.ai_budget ADD COLUMN IF NOT EXISTS scope_level text;

ALTER TABLE ge.ai_budget ADD COLUMN IF NOT EXISTS cap_amount numeric(18,2);

ALTER TABLE ge.ai_budget ADD COLUMN IF NOT EXISTS currency char(3);

ALTER TABLE ge.ai_budget ADD COLUMN IF NOT EXISTS alert_pct numeric(7,4);

ALTER TABLE ge.ai_budget ADD COLUMN IF NOT EXISTS hard_stop boolean;

ALTER TABLE ge.ai_budget ADD COLUMN IF NOT EXISTS ceiling_tier text;

ALTER TABLE ge.ai_budget ADD COLUMN IF NOT EXISTS balance_reserved numeric(18,4);

ALTER TABLE ge.ai_budget ADD COLUMN IF NOT EXISTS balance_settled numeric(18,4);

ALTER TABLE ge.custom_role ADD COLUMN IF NOT EXISTS code text;

ALTER TABLE ge.custom_role ADD COLUMN IF NOT EXISTS is_system boolean;

ALTER TABLE ge.custom_role ADD COLUMN IF NOT EXISTS surface text;

ALTER TABLE ge.custom_role ADD COLUMN IF NOT EXISTS permissions jsonb;

ALTER TABLE ge.custom_role ADD COLUMN IF NOT EXISTS is_privileged boolean;

ALTER TABLE ge.custom_role ADD COLUMN IF NOT EXISTS can_approve boolean;

ALTER TABLE ge.export_job ADD COLUMN IF NOT EXISTS request_type text;

ALTER TABLE ge.export_job ADD COLUMN IF NOT EXISTS entity_selection jsonb;

ALTER TABLE ge.export_job ADD COLUMN IF NOT EXISTS format_version text;

ALTER TABLE ge.export_job ADD COLUMN IF NOT EXISTS classification_max text;

ALTER TABLE ge.export_job ADD COLUMN IF NOT EXISTS redaction_profile text;

ALTER TABLE ge.export_job ADD COLUMN IF NOT EXISTS approval_id uuid;

ALTER TABLE ge.export_job ADD COLUMN IF NOT EXISTS legal_hold_checked text;

ALTER TABLE ge.export_job ADD COLUMN IF NOT EXISTS file_storage_key text;

ALTER TABLE ge.export_job ADD COLUMN IF NOT EXISTS link_token_hash char(64);

ALTER TABLE ge.export_job ADD COLUMN IF NOT EXISTS link_expires_at timestamptz;

ALTER TABLE ge.export_job ADD COLUMN IF NOT EXISTS state text;

ALTER TABLE ge.connector_installation ADD COLUMN IF NOT EXISTS provider_code text;

ALTER TABLE ge.connector_installation ADD COLUMN IF NOT EXISTS adapter_kind text;

ALTER TABLE ge.connector_installation ADD COLUMN IF NOT EXISTS state text;

ALTER TABLE ge.connector_installation ADD COLUMN IF NOT EXISTS scopes text;

ALTER TABLE ge.connector_installation ADD COLUMN IF NOT EXISTS health_checked_at timestamptz;

ALTER TABLE ge.connector_installation ADD COLUMN IF NOT EXISTS is_paid boolean;

ALTER TABLE ge.ops_incident ADD COLUMN IF NOT EXISTS state text;

ALTER TABLE ge.ops_incident ADD COLUMN IF NOT EXISTS opened_at timestamptz;

ALTER TABLE ge.ops_incident ADD COLUMN IF NOT EXISTS resolved_at timestamptz;

ALTER TABLE ge.ops_incident ADD COLUMN IF NOT EXISTS postmortem_ref text;

ALTER TABLE ge.ops_incident ADD COLUMN IF NOT EXISTS affected_tenants_count integer;

ALTER TABLE ge.tax_rule ADD COLUMN IF NOT EXISTS gstin text;

ALTER TABLE ge.tax_rule ADD COLUMN IF NOT EXISTS legal_name text;

ALTER TABLE ge.tax_rule ADD COLUMN IF NOT EXISTS state_code text;

ALTER TABLE ge.tax_rule ADD COLUMN IF NOT EXISTS lut_number text;

ALTER TABLE ge.tax_rule ADD COLUMN IF NOT EXISTS lut_valid_until date;

ALTER TABLE ge.tax_rule ADD COLUMN IF NOT EXISTS einvoice_applicable boolean;

ALTER TABLE ge.tax_rule ADD COLUMN IF NOT EXISTS registered_address text;

ALTER TABLE ge.invoice ADD COLUMN IF NOT EXISTS invoice_no integer;

ALTER TABLE ge.invoice ADD COLUMN IF NOT EXISTS subscription_id uuid;

ALTER TABLE ge.invoice ADD COLUMN IF NOT EXISTS period_start date;

ALTER TABLE ge.invoice ADD COLUMN IF NOT EXISTS period_end date;

ALTER TABLE ge.invoice ADD COLUMN IF NOT EXISTS subtotal numeric(18,2);

ALTER TABLE ge.invoice ADD COLUMN IF NOT EXISTS tax text;

ALTER TABLE ge.invoice ADD COLUMN IF NOT EXISTS total_amount numeric(18,2);

ALTER TABLE ge.invoice ADD COLUMN IF NOT EXISTS state text;

ALTER TABLE ge.invoice ADD COLUMN IF NOT EXISTS maker_approval_id uuid;

ALTER TABLE ge.invoice ADD COLUMN IF NOT EXISTS checker_approval_id uuid;

ALTER TABLE ge.tenant ADD COLUMN IF NOT EXISTS policy jsonb NOT NULL DEFAULT '{}'::jsonb;

ALTER TABLE ge.company ADD COLUMN IF NOT EXISTS industry_code text NULL;

ALTER TABLE ge.company ADD COLUMN IF NOT EXISTS profile jsonb NOT NULL DEFAULT '{}'::jsonb;

ALTER TABLE ge.company ADD COLUMN IF NOT EXISTS autonomy_caps jsonb NOT NULL DEFAULT '{}'::jsonb;

ALTER TABLE ge.company ADD COLUMN IF NOT EXISTS approved_config_hash char(64) NULL;

ALTER TABLE ge.ten_domain ADD COLUMN IF NOT EXISTS brand jsonb NULL;

ALTER TABLE ge.ten_portal_grant ADD COLUMN IF NOT EXISTS contact_id uuid NULL;

ALTER TABLE ge.ten_portal_grant ADD COLUMN IF NOT EXISTS invite_token_hash char(64) NULL;

ALTER TABLE ge.ten_portal_grant ADD COLUMN IF NOT EXISTS redeemed_at timestamptz NULL;

ALTER TABLE ge.ten_portal_grant ADD COLUMN IF NOT EXISTS state text NOT NULL DEFAULT 'invited' CHECK (state IN ('invited', 'active', 'expired', 'revoked'));

ALTER TABLE ge.cat_capability ADD COLUMN IF NOT EXISTS limitations text NULL;

ALTER TABLE ge.cat_chunk ADD COLUMN IF NOT EXISTS source_locator text NULL;

ALTER TABLE ge.gov_eligibility_decision ADD COLUMN IF NOT EXISTS valid_until timestamptz NULL;

ALTER TABLE ge.gov_policy_decision ADD COLUMN IF NOT EXISTS policy_version_id uuid NOT NULL;

ALTER TABLE ge.incident ADD COLUMN IF NOT EXISTS policy_decision_id uuid NULL;

ALTER TABLE ge.incident ADD COLUMN IF NOT EXISTS message_id uuid NULL;

ALTER TABLE ge.prompt_version ADD COLUMN IF NOT EXISTS template_body text NOT NULL;

ALTER TABLE ge.ai_eval_case ADD COLUMN IF NOT EXISTS case_code text NOT NULL;

ALTER TABLE ge.ai_usage_event ADD COLUMN IF NOT EXISTS integration_id uuid NULL;

ALTER TABLE ge.ai_cost_ledger ADD COLUMN IF NOT EXISTS usage_id uuid NULL;

ALTER TABLE ge.ai_cost_ledger ADD COLUMN IF NOT EXISTS entry_key text NOT NULL;

ALTER TABLE ge.ai_feedback ADD COLUMN IF NOT EXISTS correction jsonb NULL;

ALTER TABLE ge.intel_source ADD COLUMN IF NOT EXISTS name text NOT NULL;

ALTER TABLE ge.intel_search_plan ADD COLUMN IF NOT EXISTS offering_id uuid NULL;

ALTER TABLE ge.intel_source_record ADD COLUMN IF NOT EXISTS query_run_id uuid NULL;

ALTER TABLE ge.intel_source_record ADD COLUMN IF NOT EXISTS content_hash char(64) NULL;

ALTER TABLE ge.intel_source_record ADD COLUMN IF NOT EXISTS last_fetched_at timestamptz NULL;

ALTER TABLE ge.intel_fetch_log ADD COLUMN IF NOT EXISTS source_id uuid NOT NULL;

ALTER TABLE ge.intel_fetch_log ADD COLUMN IF NOT EXISTS query_run_id uuid NULL;

ALTER TABLE ge.intel_evidence ADD COLUMN IF NOT EXISTS locator text NULL;

ALTER TABLE ge.intel_evidence ADD COLUMN IF NOT EXISTS verified_at timestamptz NULL;

ALTER TABLE ge.intel_evidence ADD COLUMN IF NOT EXISTS verified_by uuid NULL;

ALTER TABLE ge.intel_alias ADD COLUMN IF NOT EXISTS source_record_id uuid NULL;

ALTER TABLE ge.intel_signal_type ADD COLUMN IF NOT EXISTS detection_rules jsonb NULL;

ALTER TABLE ge.intel_need ADD COLUMN IF NOT EXISTS confidence numeric(5,4) NULL CHECK (confidence BETWEEN 0 AND 1);

ALTER TABLE ge.intel_match ADD COLUMN IF NOT EXISTS capability_id uuid NULL;

ALTER TABLE ge.intel_match ADD COLUMN IF NOT EXISTS rationale text NULL;

ALTER TABLE ge.intel_match ADD COLUMN IF NOT EXISTS state text NOT NULL DEFAULT 'proposed' CHECK (state IN ('proposed', 'accepted', 'rejected', 'superseded'));

ALTER TABLE ge.intel_opportunity ADD COLUMN IF NOT EXISTS expires_at timestamptz NULL;

ALTER TABLE ge.intel_role_hypothesis ADD COLUMN IF NOT EXISTS opportunity_id uuid NULL;

ALTER TABLE ge.intel_contact_source ADD COLUMN IF NOT EXISTS source_record_id uuid NULL;

ALTER TABLE ge.intel_contact_source ADD COLUMN IF NOT EXISTS provider_ref text NULL;

ALTER TABLE ge.intel_contact_verification ADD COLUMN IF NOT EXISTS contact_source_id uuid NULL;

ALTER TABLE ge.intel_social_post ADD COLUMN IF NOT EXISTS source_record_id uuid NULL;

ALTER TABLE ge.intel_social_post ADD COLUMN IF NOT EXISTS permalink text NULL;

ALTER TABLE ge.crm_deal ADD COLUMN IF NOT EXISTS closure_evidence_ref text NULL;

ALTER TABLE ge.crm_submission ADD COLUMN IF NOT EXISTS subject_hmac char(64) NULL;

ALTER TABLE ge.crm_submission ADD COLUMN IF NOT EXISTS consent_id uuid NULL;

ALTER TABLE ge.eng_message_template ADD COLUMN IF NOT EXISTS template_code text NOT NULL;

ALTER TABLE ge.eng_message_draft ADD COLUMN IF NOT EXISTS eligibility_decision_id uuid NULL;

ALTER TABLE ge.eng_thread ADD COLUMN IF NOT EXISTS external_thread_ref text NULL;

ALTER TABLE ge.eng_inbound_event ADD COLUMN IF NOT EXISTS processing_state text NOT NULL DEFAULT 'received' CHECK (processing_state IN ('received', 'classified', 'routed', 'quarantined', 'failed'));

ALTER TABLE ge.eng_intent ADD COLUMN IF NOT EXISTS action_taken text NULL CHECK (action_taken IN ('none', 'task', 'stop', 'route', 'escalate'));

ALTER TABLE ge.eng_calendar_link ADD COLUMN IF NOT EXISTS external_calendar_id text NULL;

ALTER TABLE ge.channel_account ADD COLUMN IF NOT EXISTS state text NOT NULL DEFAULT 'pending' CHECK (state IN ('pending', 'verified', 'active', 'paused', 'revoked'));

ALTER TABLE ge.eng_chat_session ADD COLUMN IF NOT EXISTS thread_id uuid NULL;

ALTER TABLE ge.eng_chat_session ADD COLUMN IF NOT EXISTS session_token_hash char(64) NOT NULL;

ALTER TABLE ge.eng_identity_link ADD COLUMN IF NOT EXISTS channel_account_id uuid NULL;

ALTER TABLE ge.eng_routing_rule ADD COLUMN IF NOT EXISTS channel text NULL;

ALTER TABLE ge.mkt_content_asset ADD COLUMN IF NOT EXISTS offering_id uuid NULL;

ALTER TABLE ge.mkt_content_asset ADD COLUMN IF NOT EXISTS state text NOT NULL DEFAULT 'draft' CHECK (state IN ('draft', 'in_review', 'approved', 'retired'));

ALTER TABLE ge.mkt_seo_issue ADD COLUMN IF NOT EXISTS keyword_id uuid NULL;

ALTER TABLE ge.mkt_attribution_event ADD COLUMN IF NOT EXISTS landing_page_id uuid NULL;

ALTER TABLE ge.mkt_attribution_event ADD COLUMN IF NOT EXISTS event_key text NOT NULL;

ALTER TABLE ge.mkt_audience ADD COLUMN IF NOT EXISTS name text NOT NULL;

ALTER TABLE ge.mkt_ad_campaign ADD COLUMN IF NOT EXISTS channel_account_id uuid NULL;

ALTER TABLE ge.mkt_spend_event ADD COLUMN IF NOT EXISTS event_key text NOT NULL;

ALTER TABLE ge.mkt_event ADD COLUMN IF NOT EXISTS offering_id uuid NULL;

ALTER TABLE ge.mkt_registration ADD COLUMN IF NOT EXISTS lead_id uuid NULL;

ALTER TABLE ge.mkt_attendance ADD COLUMN IF NOT EXISTS provider_ref text NULL;

ALTER TABLE ge.mkt_referral ADD COLUMN IF NOT EXISTS lead_id uuid NULL;

ALTER TABLE ge.mkt_publication_snapshot ADD COLUMN IF NOT EXISTS approved_asset_refs jsonb NOT NULL DEFAULT '[]'::jsonb;

ALTER TABLE ge.com_objection ADD COLUMN IF NOT EXISTS thread_id uuid NULL;

ALTER TABLE ge.com_negotiation ADD COLUMN IF NOT EXISTS quote_id uuid NULL;

ALTER TABLE ge.com_negotiation ADD COLUMN IF NOT EXISTS proposed_terms jsonb NULL;

ALTER TABLE ge.com_bid ADD COLUMN IF NOT EXISTS opportunity_id uuid NULL;

ALTER TABLE ge.com_bid ADD COLUMN IF NOT EXISTS proposal_id uuid NULL;

ALTER TABLE ge.com_order ADD COLUMN IF NOT EXISTS quote_id uuid NULL;

ALTER TABLE ge.com_order ADD COLUMN IF NOT EXISTS external_ref text NULL;

ALTER TABLE ge.com_order_line ADD COLUMN IF NOT EXISTS description text NULL;

ALTER TABLE ge.com_order_line ADD COLUMN IF NOT EXISTS tax_amount numeric(18,2) NOT NULL DEFAULT 0;

ALTER TABLE ge.lcy_onboarding ADD COLUMN IF NOT EXISTS owner_id uuid NOT NULL;

ALTER TABLE ge.lcy_handoff ADD COLUMN IF NOT EXISTS task_id uuid NULL;

ALTER TABLE ge.lcy_handoff ADD COLUMN IF NOT EXISTS to_team text NULL;

ALTER TABLE ge.lcy_pilot ADD COLUMN IF NOT EXISTS deal_id uuid NULL;

ALTER TABLE ge.lcy_pilot ADD COLUMN IF NOT EXISTS scope jsonb NULL;

ALTER TABLE ge.lcy_integration_deal ADD COLUMN IF NOT EXISTS deal_id uuid NULL;

ALTER TABLE ge.aut_autonomy_plan ADD COLUMN IF NOT EXISTS input_hash char(64) NOT NULL;

ALTER TABLE ge.aut_autonomy_plan ADD COLUMN IF NOT EXISTS policy_hash char(64) NOT NULL;

ALTER TABLE ge.aut_autonomy_plan ADD COLUMN IF NOT EXISTS planned_actions jsonb NOT NULL;

ALTER TABLE ge.aut_autonomy_plan ADD COLUMN IF NOT EXISTS simulation_result jsonb NULL;

ALTER TABLE ge.aut_config_revision ADD COLUMN IF NOT EXISTS schema_revision integer NOT NULL;

ALTER TABLE ge.aut_trigger ADD COLUMN IF NOT EXISTS concurrency_limit integer NOT NULL DEFAULT 1 CHECK (concurrency_limit BETWEEN 1 AND 20);

ALTER TABLE ge.aut_conflict_case ADD COLUMN IF NOT EXISTS decision_reason text NULL;

ALTER TABLE ge.aut_conflict_case ADD COLUMN IF NOT EXISTS resolved_at timestamptz NULL;

ALTER TABLE ge.ops_job_run ADD COLUMN IF NOT EXISTS job_key text NOT NULL;

ALTER TABLE ge.ops_job_run ADD COLUMN IF NOT EXISTS next_retry_at timestamptz NULL;

ALTER TABLE ge.ops_release ADD COLUMN IF NOT EXISTS environment text NOT NULL CHECK (environment IN ('dev', 'staging', 'prod'));

ALTER TABLE ge.ops_incident ADD COLUMN IF NOT EXISTS job_run_id uuid NULL;

ALTER TABLE ge.ops_incident ADD COLUMN IF NOT EXISTS summary text NULL;

ALTER TABLE ge.invoice ADD COLUMN IF NOT EXISTS payment_ref text NULL;

ALTER TABLE ge.saas_service_invoice_line ADD COLUMN IF NOT EXISTS cost_amount numeric(18,4) NULL;

ALTER TABLE ge.saas_service_invoice_line ADD COLUMN IF NOT EXISTS rate_snapshot jsonb NOT NULL;

ALTER TABLE ge.export_job ADD COLUMN IF NOT EXISTS file_sha256 char(64) NULL;

ALTER TABLE ge.export_job ADD COLUMN IF NOT EXISTS manifest jsonb NULL;

ALTER TABLE ge.saas_application_draft ADD COLUMN IF NOT EXISTS application_ref uuid NOT NULL;

ALTER TABLE ge.saas_application_draft ADD COLUMN IF NOT EXISTS country_code char(2) NULL;

ALTER TABLE ge.saas_application_draft ADD COLUMN IF NOT EXISTS industry_code text NULL;

ALTER TABLE ge.saas_application_draft ADD COLUMN IF NOT EXISTS website text NULL;

ALTER TABLE ge.saas_application_draft ADD COLUMN IF NOT EXISTS service_model text NULL CHECK (service_model IN ('owned', 'saas'));

ALTER TABLE ge.saas_application_draft ADD COLUMN IF NOT EXISTS terms_revision text NOT NULL;

ALTER TABLE ge.ana_forecast ADD COLUMN IF NOT EXISTS model_version text NULL;

ALTER TABLE ge.com_order ADD COLUMN IF NOT EXISTS order_kind text NOT NULL DEFAULT 'goods' CHECK (order_kind IN ('goods','service','training','project'));

ALTER TABLE ge.intel_score_version ADD COLUMN IF NOT EXISTS version_no integer;

ALTER TABLE ge.intel_signal ADD COLUMN IF NOT EXISTS dedupe_key char(64);

ALTER TABLE ge.eng_intent ADD COLUMN IF NOT EXISTS superseded_by uuid;

ALTER TABLE ge.gov_policy_decision ADD COLUMN IF NOT EXISTS reason_codes text[] NOT NULL DEFAULT '{}';

ALTER TABLE ge.mkt_publication_snapshot ADD COLUMN IF NOT EXISTS page_type text;

DO $$ BEGIN IF EXISTS (SELECT 1 FROM pg_extension WHERE extname = 'vector') THEN EXECUTE 'ALTER TABLE ge.cat_embedding ADD COLUMN IF NOT EXISTS embedding extensions.halfvec(1024)'; END IF; END $$;
