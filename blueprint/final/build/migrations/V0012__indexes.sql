-- V0012__indexes
SET search_path = ge, extensions, public;

SELECT set_config('app.zone', coalesce(nullif(current_setting('app.deployment_region', true), ''), 'IN'), false);

SELECT set_config('app.deployment_region', coalesce(nullif(current_setting('app.deployment_region', true), ''), 'IN'), false);

CREATE INDEX IF NOT EXISTS ix_verified_domain__tenant_id_connection_id ON ge.verified_domain (tenant_id, connection_id);

CREATE INDEX IF NOT EXISTS ix_dlt_template__tenant_id_channel_account_id_header ON ge.dlt_template (tenant_id, channel_account_id, header);

CREATE INDEX IF NOT EXISTS ix_edge_conformance_check__project ON ge.edge_conformance_check (project);

CREATE INDEX IF NOT EXISTS ix_ai_model_pin__model_id ON ge.ai_model_pin (model_id);

CREATE INDEX IF NOT EXISTS ix_ai_model_pin__rollback_to ON ge.ai_model_pin (rollback_to);

CREATE INDEX IF NOT EXISTS ix_ten_membership__user_id ON ge.ten_membership (user_id);

CREATE INDEX IF NOT EXISTS ix_ten_membership__invited_by ON ge.ten_membership (invited_by);

CREATE INDEX IF NOT EXISTS ix_cat_claim__offering_version_id ON ge.cat_claim (offering_version_id);

CREATE INDEX IF NOT EXISTS ix_cat_claim__subject_consent_ref ON ge.cat_claim (subject_consent_ref);

CREATE INDEX IF NOT EXISTS ix_cat_price_version__currency ON ge.cat_price_version (currency);

CREATE INDEX IF NOT EXISTS ix_cat_price_version__unit_code ON ge.cat_price_version (unit_code);

CREATE INDEX IF NOT EXISTS ix_gov_policy_version__simulation_report_ref ON ge.gov_policy_version (simulation_report_ref);

CREATE INDEX IF NOT EXISTS ix_gov_approval__approver_id ON ge.gov_approval (approver_id);

CREATE INDEX IF NOT EXISTS ix_gov_approval__delegation_id ON ge.gov_approval (delegation_id);

CREATE INDEX IF NOT EXISTS ix_gov_approval__revokes_id ON ge.gov_approval (revokes_id);

CREATE INDEX IF NOT EXISTS ix_ai_model_run__agent_id ON ge.ai_model_run (agent_id);

CREATE INDEX IF NOT EXISTS ix_intel_source__active_policy_id ON ge.intel_source (active_policy_id);

CREATE INDEX IF NOT EXISTS ix_intel_evidence__source_record_id ON ge.intel_evidence (source_record_id);

CREATE INDEX IF NOT EXISTS ix_intel_evidence__social_post_id ON ge.intel_evidence (social_post_id);

CREATE INDEX IF NOT EXISTS ix_intel_evidence__organization_id ON ge.intel_evidence (organization_id);

CREATE INDEX IF NOT EXISTS ix_intel_organization__country_code ON ge.intel_organization (country_code);

CREATE INDEX IF NOT EXISTS ix_intel_organization__owner_id ON ge.intel_organization (owner_id);

CREATE INDEX IF NOT EXISTS ix_intel_signal__signal_type_id ON ge.intel_signal (signal_type_id);

CREATE INDEX IF NOT EXISTS ix_intel_signal__organization_id ON ge.intel_signal (organization_id);

CREATE INDEX IF NOT EXISTS ix_intel_need__organization_id ON ge.intel_need (organization_id);

CREATE INDEX IF NOT EXISTS ix_intel_need__source_signal_id ON ge.intel_need (source_signal_id);

CREATE INDEX IF NOT EXISTS ix_intel_opportunity__organization_id ON ge.intel_opportunity (organization_id);

CREATE INDEX IF NOT EXISTS ix_intel_opportunity__offering_id ON ge.intel_opportunity (offering_id);

CREATE INDEX IF NOT EXISTS ix_intel_opportunity__match_id ON ge.intel_opportunity (match_id);

CREATE INDEX IF NOT EXISTS ix_intel_opportunity__need_id ON ge.intel_opportunity (need_id);

CREATE INDEX IF NOT EXISTS ix_intel_opportunity__current_score_version_id ON ge.intel_opportunity (current_score_version_id);

CREATE INDEX IF NOT EXISTS ix_intel_score_version__opportunity_id ON ge.intel_score_version (opportunity_id);

CREATE INDEX IF NOT EXISTS ix_intel_score_version__scoring_model_id ON ge.intel_score_version (scoring_model_id);

CREATE INDEX IF NOT EXISTS ix_intel_contact__organization_id ON ge.intel_contact (organization_id);

CREATE INDEX IF NOT EXISTS ix_intel_contact__country_code ON ge.intel_contact (country_code);

CREATE INDEX IF NOT EXISTS ix_intel_contact__import_job_id ON ge.intel_contact (import_job_id);

CREATE INDEX IF NOT EXISTS ix_crm_lead__submission_id ON ge.crm_lead (submission_id);

CREATE INDEX IF NOT EXISTS ix_crm_lead__contact_id ON ge.crm_lead (contact_id);

CREATE INDEX IF NOT EXISTS ix_crm_lead__organization_id ON ge.crm_lead (organization_id);

CREATE INDEX IF NOT EXISTS ix_crm_lead__consent_id ON ge.crm_lead (consent_id);

CREATE INDEX IF NOT EXISTS ix_crm_lead__opportunity_id ON ge.crm_lead (opportunity_id);

CREATE INDEX IF NOT EXISTS ix_crm_deal__opportunity_id ON ge.crm_deal (opportunity_id);

CREATE INDEX IF NOT EXISTS ix_crm_deal__organization_id ON ge.crm_deal (organization_id);

CREATE INDEX IF NOT EXISTS ix_crm_deal__offering_id ON ge.crm_deal (offering_id);

CREATE INDEX IF NOT EXISTS ix_crm_deal__pipeline_id ON ge.crm_deal (pipeline_id);

CREATE INDEX IF NOT EXISTS ix_crm_deal__stage_id ON ge.crm_deal (stage_id);

CREATE INDEX IF NOT EXISTS ix_crm_deal__owner_id ON ge.crm_deal (owner_id);

CREATE INDEX IF NOT EXISTS ix_crm_deal__currency ON ge.crm_deal (currency);

CREATE INDEX IF NOT EXISTS ix_crm_deal__accepted_quote_id ON ge.crm_deal (accepted_quote_id);

CREATE INDEX IF NOT EXISTS ix_crm_stage_transition__deal_id ON ge.crm_stage_transition (deal_id);

CREATE INDEX IF NOT EXISTS ix_crm_activity__organization_id ON ge.crm_activity (organization_id);

CREATE INDEX IF NOT EXISTS ix_eng_thread__contact_id ON ge.eng_thread (contact_id);

CREATE INDEX IF NOT EXISTS ix_eng_thread__channel_account_id ON ge.eng_thread (channel_account_id);

CREATE INDEX IF NOT EXISTS ix_eng_message__thread_id ON ge.eng_message (thread_id);

CREATE INDEX IF NOT EXISTS ix_eng_message__draft_id ON ge.eng_message (draft_id);

CREATE INDEX IF NOT EXISTS ix_eng_message__enrollment_id ON ge.eng_message (enrollment_id);

CREATE INDEX IF NOT EXISTS ix_eng_message__approval_id ON ge.eng_message (approval_id);

CREATE INDEX IF NOT EXISTS ix_eng_message__cost_reservation_id ON ge.eng_message (cost_reservation_id);

CREATE INDEX IF NOT EXISTS ix_eng_enrollment__sequence_id ON ge.eng_enrollment (sequence_id);

CREATE INDEX IF NOT EXISTS ix_eng_enrollment__contact_id ON ge.eng_enrollment (contact_id);

CREATE INDEX IF NOT EXISTS ix_eng_meeting__organizer_id ON ge.eng_meeting (organizer_id);

CREATE INDEX IF NOT EXISTS ix_mkt_content_version__asset_id ON ge.mkt_content_version (asset_id);

CREATE INDEX IF NOT EXISTS ix_mkt_publication__current_snapshot_id ON ge.mkt_publication (current_snapshot_id);

CREATE INDEX IF NOT EXISTS ix_mkt_campaign__current_version_id ON ge.mkt_campaign (current_version_id);

CREATE INDEX IF NOT EXISTS ix_com_proposal__deal_id ON ge.com_proposal (deal_id);

CREATE INDEX IF NOT EXISTS ix_com_proposal__current_version_id ON ge.com_proposal (current_version_id);

CREATE INDEX IF NOT EXISTS ix_com_proposal__portal_grant_id ON ge.com_proposal (portal_grant_id);

CREATE INDEX IF NOT EXISTS ix_com_quote__deal_id ON ge.com_quote (deal_id);

CREATE INDEX IF NOT EXISTS ix_com_quote__proposal_version_id ON ge.com_quote (proposal_version_id);

CREATE INDEX IF NOT EXISTS ix_com_quote__currency ON ge.com_quote (currency);

CREATE INDEX IF NOT EXISTS ix_com_quote_line__offering_version_id ON ge.com_quote_line (offering_version_id);

CREATE INDEX IF NOT EXISTS ix_com_quote_line__price_version_id ON ge.com_quote_line (price_version_id);

CREATE INDEX IF NOT EXISTS ix_com_contract__deal_id ON ge.com_contract (deal_id);

CREATE INDEX IF NOT EXISTS ix_com_contract__quote_id ON ge.com_contract (quote_id);

CREATE INDEX IF NOT EXISTS ix_com_contract__currency ON ge.com_contract (currency);

CREATE INDEX IF NOT EXISTS ix_com_signature_event__contract_id ON ge.com_signature_event (contract_id);

CREATE INDEX IF NOT EXISTS ix_com_bid__deal_id ON ge.com_bid (deal_id);

CREATE INDEX IF NOT EXISTS ix_com_bid__organization_id ON ge.com_bid (organization_id);

CREATE INDEX IF NOT EXISTS ix_com_order__deal_id ON ge.com_order (deal_id);

CREATE INDEX IF NOT EXISTS ix_com_order__counterparty_org_id ON ge.com_order (counterparty_org_id);

CREATE INDEX IF NOT EXISTS ix_com_order__currency ON ge.com_order (currency);

CREATE INDEX IF NOT EXISTS ix_com_order_line__unit_code ON ge.com_order_line (unit_code);

CREATE INDEX IF NOT EXISTS ix_com_fulfillment_event__order_line_id ON ge.com_fulfillment_event (order_line_id);

CREATE INDEX IF NOT EXISTS ix_com_invoice__bill_to_org_id ON ge.com_invoice (bill_to_org_id);

CREATE INDEX IF NOT EXISTS ix_com_payment_allocation__payment_id ON ge.com_payment_allocation (payment_id);

CREATE INDEX IF NOT EXISTS ix_com_payment_allocation__invoice_id ON ge.com_payment_allocation (invoice_id);

CREATE INDEX IF NOT EXISTS ix_com_receivable_entry__counterparty_org_id ON ge.com_receivable_entry (counterparty_org_id);

CREATE INDEX IF NOT EXISTS ix_com_payable_entry__counterparty_org_id ON ge.com_payable_entry (counterparty_org_id);

CREATE INDEX IF NOT EXISTS ix_aut_workflow__active_revision_id ON ge.aut_workflow (active_revision_id);

CREATE INDEX IF NOT EXISTS ix_aut_trigger__workflow_revision_id ON ge.aut_trigger (workflow_revision_id);

CREATE INDEX IF NOT EXISTS ix_aut_trigger__credential_ref_id ON ge.aut_trigger (credential_ref_id);

CREATE INDEX IF NOT EXISTS ix_saas_plan__current_version_id ON ge.saas_plan (current_version_id);

CREATE INDEX IF NOT EXISTS ix_saas_subscription__plan_version_id ON ge.saas_subscription (plan_version_id);

CREATE INDEX IF NOT EXISTS ix_saas_application_draft__applicant_user_id ON ge.saas_application_draft (applicant_user_id);

CREATE INDEX IF NOT EXISTS ix_saas_service_request__requester_user_id ON ge.saas_service_request (requester_user_id);

CREATE INDEX IF NOT EXISTS ix_saas_service_request__assignee_user_id ON ge.saas_service_request (assignee_user_id);

CREATE INDEX IF NOT EXISTS ix_saas_service_request__support_grant_id ON ge.saas_service_request (support_grant_id);

CREATE INDEX IF NOT EXISTS ix_com_fulfillment_milestone__order_id ON ge.com_fulfillment_milestone (order_id);

CREATE INDEX IF NOT EXISTS ix_com_fulfillment_milestone__order_line_id ON ge.com_fulfillment_milestone (order_line_id);

CREATE INDEX IF NOT EXISTS ix_com_fulfillment_milestone__unit_code ON ge.com_fulfillment_milestone (unit_code);

CREATE INDEX IF NOT EXISTS ix_com_fulfillment_milestone__last_event_id ON ge.com_fulfillment_milestone (last_event_id);

CREATE INDEX IF NOT EXISTS ix_ai_eval_case_result__eval_case_id ON ge.ai_eval_case_result (eval_case_id);

CREATE INDEX IF NOT EXISTS ix_ai_eval_case_result__model_run_id ON ge.ai_eval_case_result (model_run_id);

CREATE INDEX IF NOT EXISTS ix_tenant__source_application_id ON ge.tenant (source_application_id);

CREATE INDEX IF NOT EXISTS ix_company__country_code ON ge.company (country_code);

CREATE INDEX IF NOT EXISTS ix_company__base_currency ON ge.company (base_currency);

CREATE INDEX IF NOT EXISTS ix_company__template_ref ON ge.company (template_ref);

CREATE INDEX IF NOT EXISTS ix_offering__business_line_id ON ge.offering (business_line_id);

CREATE INDEX IF NOT EXISTS ix_offering__current_version_id ON ge.offering (current_version_id);

CREATE INDEX IF NOT EXISTS ix_offering__owner_id ON ge.offering (owner_id);

CREATE INDEX IF NOT EXISTS ix_workflow_run__workflow_revision_id ON ge.workflow_run (workflow_revision_id);

CREATE INDEX IF NOT EXISTS ix_consent_record__lia_ref ON ge.consent_record (lia_ref);

CREATE INDEX IF NOT EXISTS ix_consent_record__policy_version_id ON ge.consent_record (policy_version_id);

CREATE INDEX IF NOT EXISTS ix_consent_record__guardian_contact_id ON ge.consent_record (guardian_contact_id);

CREATE INDEX IF NOT EXISTS ix_consent_record__jurisdiction_code ON ge.consent_record (jurisdiction_code);

CREATE INDEX IF NOT EXISTS ix_ten_portal_grant__contact_id ON ge.ten_portal_grant (contact_id);

CREATE INDEX IF NOT EXISTS ix_gov_policy_decision__policy_version_id ON ge.gov_policy_decision (policy_version_id);

CREATE INDEX IF NOT EXISTS ix_incident__policy_decision_id ON ge.incident (policy_decision_id);

CREATE INDEX IF NOT EXISTS ix_incident__message_id ON ge.incident (message_id);

CREATE INDEX IF NOT EXISTS ix_ai_usage_event__integration_id ON ge.ai_usage_event (integration_id);

CREATE INDEX IF NOT EXISTS ix_intel_search_plan__offering_id ON ge.intel_search_plan (offering_id);

CREATE INDEX IF NOT EXISTS ix_intel_source_record__query_run_id ON ge.intel_source_record (query_run_id);

CREATE INDEX IF NOT EXISTS ix_intel_fetch_log__source_id ON ge.intel_fetch_log (source_id);

CREATE INDEX IF NOT EXISTS ix_intel_fetch_log__query_run_id ON ge.intel_fetch_log (query_run_id);

CREATE INDEX IF NOT EXISTS ix_intel_alias__source_record_id ON ge.intel_alias (source_record_id);

CREATE INDEX IF NOT EXISTS ix_intel_match__capability_id ON ge.intel_match (capability_id);

CREATE INDEX IF NOT EXISTS ix_intel_role_hypothesis__opportunity_id ON ge.intel_role_hypothesis (opportunity_id);

CREATE INDEX IF NOT EXISTS ix_intel_contact_source__source_record_id ON ge.intel_contact_source (source_record_id);

CREATE INDEX IF NOT EXISTS ix_intel_contact_verification__contact_source_id ON ge.intel_contact_verification (contact_source_id);

CREATE INDEX IF NOT EXISTS ix_intel_social_post__source_record_id ON ge.intel_social_post (source_record_id);

CREATE INDEX IF NOT EXISTS ix_crm_submission__consent_id ON ge.crm_submission (consent_id);

CREATE INDEX IF NOT EXISTS ix_eng_message_draft__eligibility_decision_id ON ge.eng_message_draft (eligibility_decision_id);

CREATE INDEX IF NOT EXISTS ix_eng_chat_session__thread_id ON ge.eng_chat_session (thread_id);

CREATE INDEX IF NOT EXISTS ix_eng_identity_link__channel_account_id ON ge.eng_identity_link (channel_account_id);

CREATE INDEX IF NOT EXISTS ix_mkt_content_asset__offering_id ON ge.mkt_content_asset (offering_id);

CREATE INDEX IF NOT EXISTS ix_mkt_seo_issue__keyword_id ON ge.mkt_seo_issue (keyword_id);

CREATE INDEX IF NOT EXISTS ix_mkt_attribution_event__landing_page_id ON ge.mkt_attribution_event (landing_page_id);

CREATE INDEX IF NOT EXISTS ix_mkt_ad_campaign__channel_account_id ON ge.mkt_ad_campaign (channel_account_id);

CREATE INDEX IF NOT EXISTS ix_mkt_event__offering_id ON ge.mkt_event (offering_id);

CREATE INDEX IF NOT EXISTS ix_mkt_registration__lead_id ON ge.mkt_registration (lead_id);

CREATE INDEX IF NOT EXISTS ix_mkt_referral__lead_id ON ge.mkt_referral (lead_id);

CREATE INDEX IF NOT EXISTS ix_com_objection__thread_id ON ge.com_objection (thread_id);

CREATE INDEX IF NOT EXISTS ix_com_negotiation__quote_id ON ge.com_negotiation (quote_id);

CREATE INDEX IF NOT EXISTS ix_com_bid__opportunity_id ON ge.com_bid (opportunity_id);

CREATE INDEX IF NOT EXISTS ix_com_bid__proposal_id ON ge.com_bid (proposal_id);

CREATE INDEX IF NOT EXISTS ix_com_order__quote_id ON ge.com_order (quote_id);

CREATE INDEX IF NOT EXISTS ix_lcy_onboarding__owner_id ON ge.lcy_onboarding (owner_id);

CREATE INDEX IF NOT EXISTS ix_lcy_handoff__task_id ON ge.lcy_handoff (task_id);

CREATE INDEX IF NOT EXISTS ix_lcy_pilot__deal_id ON ge.lcy_pilot (deal_id);

CREATE INDEX IF NOT EXISTS ix_lcy_integration_deal__deal_id ON ge.lcy_integration_deal (deal_id);

CREATE INDEX IF NOT EXISTS ix_ops_incident__job_run_id ON ge.ops_incident (job_run_id);

CREATE INDEX IF NOT EXISTS ix_eng_intent__superseded_by ON ge.eng_intent (superseded_by);

CREATE INDEX IF NOT EXISTS ixp_ops_outbox__pending ON ge.outbox (available_at, event_id) WHERE status IN ('pending','failed');

CREATE INDEX IF NOT EXISTS ixp_eng_message__dispatchable ON ge.eng_message (tenant_id, startup_id, scheduled_for) WHERE state IN ('queued','policy_checked') AND is_simulated = false;

CREATE INDEX IF NOT EXISTS ixp_eng_message__uncertain ON ge.eng_message (tenant_id, startup_id, sent_at) WHERE outcome_certainty = 'uncertain';

CREATE INDEX IF NOT EXISTS ixp_eng_enrollment__due ON ge.eng_enrollment (next_due_at) WHERE state IN ('active','waiting');

CREATE INDEX IF NOT EXISTS ixp_gov_suppression__active ON ge.suppression (tenant_id, identifier_hmac, channel, purpose) WHERE lifted_by_id IS NULL;

CREATE INDEX IF NOT EXISTS ix_gov_consent__current ON ge.consent_record (tenant_id, company_id, subject_hmac, channel, purpose, effective_at DESC);

CREATE INDEX IF NOT EXISTS ixp_intel_opportunity__review ON ge.intel_opportunity (tenant_id, startup_id, current_score DESC) WHERE state IN ('priority_review','scored') AND archived_at IS NULL;

CREATE INDEX IF NOT EXISTS ixp_crm_deal__open ON ge.crm_deal (tenant_id, startup_id, stage_code, owner_id) WHERE closure_status = 'open' AND archived_at IS NULL;

CREATE INDEX IF NOT EXISTS ixp_lcy_task__open ON ge.lcy_task (tenant_id, startup_id, assignee_id, due_at) WHERE state IN ('open','in_progress');

CREATE INDEX IF NOT EXISTS ixp_ops_notification__unread ON ge.ops_notification (recipient_id, created_at DESC) WHERE state = 'new';

CREATE INDEX IF NOT EXISTS ixp_aut_run__active ON ge.workflow_run (tenant_id, company_id, state, due_at) WHERE state IN ('pending','running','waiting','held','paused','reconciling');

CREATE INDEX IF NOT EXISTS ixp_com_invoice__receivable ON ge.com_invoice (tenant_id, startup_id, due_date) WHERE state IN ('issued','awaiting_payment','partially_paid');

CREATE INDEX IF NOT EXISTS ixp_intel_contact__retention ON ge.intel_contact (tenant_id, last_eligible_interaction_at) WHERE erased_at IS NULL;

CREATE INDEX IF NOT EXISTS ix_crm_activity__timeline ON ge.crm_activity (tenant_id, startup_id, organization_id, occurred_at DESC, id DESC);

CREATE INDEX IF NOT EXISTS ixb_ops_audit_event__time ON ge.audit_event USING brin (occurred_at);

CREATE INDEX IF NOT EXISTS ix_ops_audit_event__object ON ge.audit_event (tenant_id, object_type, object_id, occurred_at DESC);

CREATE INDEX IF NOT EXISTS ix_ai_model_run__agent_day ON ge.ai_model_run (tenant_id, agent_id, created_at);

CREATE UNIQUE INDEX IF NOT EXISTS uq_cat_capability__code ON ge.cat_capability (tenant_id, startup_id, code) WHERE archived_at IS NULL;

CREATE UNIQUE INDEX IF NOT EXISTS uq_int_quota__period ON ge.int_quota (tenant_id, startup_id, integration_id, unit, period);

CREATE UNIQUE INDEX IF NOT EXISTS uq_ops_job_run__job_key ON ge.ops_job_run (COALESCE(tenant_id, '00000000-0000-0000-0000-000000000000'::uuid), job_key);

CREATE INDEX IF NOT EXISTS ixp_ops_job_run__retry ON ge.ops_job_run (next_retry_at) WHERE state IN ('failed','retry_scheduled');

CREATE UNIQUE INDEX IF NOT EXISTS uq_ai_eval_case__code ON ge.ai_eval_case (COALESCE(tenant_id, '00000000-0000-0000-0000-000000000000'::uuid), suite_code, case_code, version_no);

CREATE UNIQUE INDEX IF NOT EXISTS uq_ai_cost_ledger__entry_key ON ge.ai_cost_ledger (tenant_id, entry_key);

CREATE INDEX IF NOT EXISTS ixp_gov_privacy_request__due ON ge.dsar_request (tenant_id, due_at) WHERE state NOT IN ('completed','rejected','withdrawn');

CREATE UNIQUE INDEX IF NOT EXISTS uq_ops_release__tag_env ON ge.ops_release (version_tag, environment);

CREATE INDEX IF NOT EXISTS ixp_ops_incident__open ON ge.ops_incident (severity, opened_at DESC) WHERE state <> 'closed';

CREATE UNIQUE INDEX IF NOT EXISTS uq_intel_query_run__correlation ON ge.intel_query_run (tenant_id, startup_id, correlation_id) WHERE correlation_id IS NOT NULL;

CREATE UNIQUE INDEX IF NOT EXISTS uq_intel_source_record__version ON ge.intel_source_record (tenant_id, startup_id, source_id, url_hash, content_hash);

CREATE INDEX IF NOT EXISTS ix_intel_fetch_log__source_time ON ge.intel_fetch_log (tenant_id, startup_id, source_id, created_at DESC);

CREATE INDEX IF NOT EXISTS ix_intel_location__org_geo ON ge.intel_location (tenant_id, startup_id, organization_id, country_code, subdivision_code);

CREATE UNIQUE INDEX IF NOT EXISTS uq_intel_signal__dedupe ON ge.intel_signal (tenant_id, startup_id, dedupe_key) WHERE state <> 'rejected';

CREATE UNIQUE INDEX IF NOT EXISTS uq_intel_match__need_target ON ge.intel_match (tenant_id, startup_id, need_id, offering_version_id, COALESCE(capability_id, '00000000-0000-0000-0000-000000000000'::uuid));

CREATE UNIQUE INDEX IF NOT EXISTS uq_intel_score_version__seq ON ge.intel_score_version (opportunity_id, version_no);

CREATE UNIQUE INDEX IF NOT EXISTS uq_intel_role_hypothesis__opp_role ON ge.intel_role_hypothesis (tenant_id, startup_id, opportunity_id, role_code) WHERE opportunity_id IS NOT NULL;

CREATE INDEX IF NOT EXISTS ix_intel_contact_verification__expiry ON ge.intel_contact_verification (tenant_id, startup_id, contact_id, channel, expires_at DESC);

CREATE UNIQUE INDEX IF NOT EXISTS uq_crm_form__code ON ge.crm_form (tenant_id, startup_id, form_code) WHERE archived_at IS NULL;

CREATE INDEX IF NOT EXISTS ixp_crm_lead__queue ON ge.crm_lead (tenant_id, startup_id, state, owner_id) WHERE archived_at IS NULL;

CREATE UNIQUE INDEX IF NOT EXISTS uq_aut_workflow__code ON ge.aut_workflow (tenant_id, startup_id, workflow_code);

CREATE UNIQUE INDEX IF NOT EXISTS uq_eng_message_template__code ON ge.eng_message_template (tenant_id, startup_id, template_code, channel, locale, version_no);

CREATE UNIQUE INDEX IF NOT EXISTS uq_eng_thread__external ON ge.eng_thread (channel_account_id, external_thread_ref) WHERE external_thread_ref IS NOT NULL;

CREATE UNIQUE INDEX IF NOT EXISTS uq_eng_intent__inbound ON ge.eng_intent (inbound_event_id) WHERE superseded_by IS NULL;

CREATE UNIQUE INDEX IF NOT EXISTS uq_eng_calendar_link__external ON ge.eng_calendar_link (integration_id, external_calendar_id);

CREATE INDEX IF NOT EXISTS ix_gov_approval__object ON ge.gov_approval (tenant_id, startup_id, object_type, object_id, created_at DESC);

CREATE UNIQUE INDEX IF NOT EXISTS uq_eng_identity_link__address ON ge.eng_identity_link (tenant_id, startup_id, channel_account_id, address_hmac);

CREATE UNIQUE INDEX IF NOT EXISTS uq_eng_routing_rule__priority ON ge.eng_routing_rule (tenant_id, startup_id, COALESCE(channel,'*'), priority) WHERE status = 'active';

CREATE INDEX IF NOT EXISTS ix_gov_policy_decision__action ON ge.gov_policy_decision (tenant_id, startup_id, action, created_at DESC);

CREATE INDEX IF NOT EXISTS ixp_gov_compliance_incident__open ON ge.incident (tenant_id, severity, opened_at DESC) WHERE state <> 'closed';

CREATE UNIQUE INDEX IF NOT EXISTS uq_intel_social_post__ref ON ge.intel_social_post (tenant_id, startup_id, platform, post_ref);

CREATE INDEX IF NOT EXISTS ix_mkt_content_asset__offering_state ON ge.mkt_content_asset (tenant_id, startup_id, offering_id, state);

CREATE INDEX IF NOT EXISTS ixp_mkt_seo_issue__open ON ge.mkt_seo_issue (tenant_id, startup_id, page_id, severity) WHERE state <> 'resolved';

CREATE UNIQUE INDEX IF NOT EXISTS uq_mkt_page_metric__day ON ge.mkt_page_metric (tenant_id, startup_id, page_id, COALESCE(keyword_id, '00000000-0000-0000-0000-000000000000'::uuid), metric_date, source);

CREATE UNIQUE INDEX IF NOT EXISTS uq_mkt_attribution_event__key ON ge.mkt_attribution_event (tenant_id, startup_id, event_key);

CREATE INDEX IF NOT EXISTS ix_mkt_campaign__state ON ge.mkt_campaign (tenant_id, startup_id, state, starts_at);

CREATE UNIQUE INDEX IF NOT EXISTS uq_mkt_spend_event__key ON ge.mkt_spend_event (ad_campaign_id, event_key);

CREATE INDEX IF NOT EXISTS ix_mkt_event__starts ON ge.mkt_event (tenant_id, startup_id, starts_at, state);

CREATE UNIQUE INDEX IF NOT EXISTS uq_mkt_registration__event_contact ON ge.mkt_registration (event_id, contact_id);

CREATE UNIQUE INDEX IF NOT EXISTS uq_mkt_attendance__provider ON ge.mkt_attendance (registration_id, provider_ref) WHERE provider_ref IS NOT NULL;

CREATE INDEX IF NOT EXISTS ix_com_proposal__deal_state ON ge.com_proposal (tenant_id, startup_id, deal_id, state);

CREATE INDEX IF NOT EXISTS ix_com_quote__deal_state ON ge.com_quote (tenant_id, startup_id, deal_id, state);

CREATE INDEX IF NOT EXISTS ix_com_objection__deal_state ON ge.com_objection (tenant_id, startup_id, deal_id, state);

CREATE UNIQUE INDEX IF NOT EXISTS uq_lcy_onboarding__deal ON ge.lcy_onboarding (tenant_id, startup_id, deal_id) WHERE archived_at IS NULL;

CREATE UNIQUE INDEX IF NOT EXISTS uq_lcy_handoff__task ON ge.lcy_handoff (onboarding_id, task_id) WHERE task_id IS NOT NULL;

CREATE INDEX IF NOT EXISTS ix_ai_eval_run__prompt_gate ON ge.eval_run (prompt_version_id, gate_result, run_at DESC);

CREATE UNIQUE INDEX IF NOT EXISTS uq_intel_competitor__website ON ge.intel_competitor (tenant_id, startup_id, lower(website)) WHERE website IS NOT NULL;

CREATE UNIQUE INDEX IF NOT EXISTS uq_intel_market_event__dedupe ON ge.intel_market_event (tenant_id, startup_id, competitor_id, evidence_id, event_type);

CREATE UNIQUE INDEX IF NOT EXISTS uq_ana_stage_metric__period ON ge.ana_stage_metric (tenant_id, startup_id, pipeline_id, stage_code, period);

CREATE UNIQUE INDEX IF NOT EXISTS uq_ana_forecast__period ON ge.ana_forecast (tenant_id, startup_id, period, scenario, model_version);

CREATE INDEX IF NOT EXISTS ix_ops_test_run__release ON ge.ops_test_run (release_id, result, executed_at DESC);

CREATE UNIQUE INDEX IF NOT EXISTS uq_lcy_integration_deal__deal ON ge.lcy_integration_deal (tenant_id, startup_id, deal_id) WHERE deal_id IS NOT NULL;

CREATE INDEX IF NOT EXISTS ix_agent_credential__list ON ge.agent_credential (tenant_id, startup_id, state, updated_at DESC);

CREATE INDEX IF NOT EXISTS ix_agent_message__list ON ge.agent_message (tenant_id, startup_id, state, updated_at DESC);

CREATE INDEX IF NOT EXISTS ix_ai_agent_definition__list ON ge.ai_agent_definition (tenant_id, startup_id, status, updated_at DESC);

CREATE INDEX IF NOT EXISTS ix_ai_eval_case__list ON ge.ai_eval_case (tenant_id, startup_id, status, updated_at DESC);

CREATE INDEX IF NOT EXISTS ix_ana_metric_definition__list ON ge.ana_metric_definition (tenant_id, startup_id, status, updated_at DESC);

CREATE INDEX IF NOT EXISTS ix_aut_autonomy_plan__list ON ge.aut_autonomy_plan (tenant_id, startup_id, state, updated_at DESC);

CREATE INDEX IF NOT EXISTS ix_aut_config_revision__list ON ge.aut_config_revision (tenant_id, startup_id, status, updated_at DESC);

CREATE INDEX IF NOT EXISTS ix_aut_conflict_case__list ON ge.aut_conflict_case (tenant_id, startup_id, state, updated_at DESC);

CREATE INDEX IF NOT EXISTS ix_aut_node_template__list ON ge.aut_node_template (tenant_id, startup_id, status, updated_at DESC);

CREATE INDEX IF NOT EXISTS ix_aut_trigger__list ON ge.aut_trigger (tenant_id, startup_id, state, updated_at DESC);

CREATE INDEX IF NOT EXISTS ix_aut_workflow_revision__list ON ge.aut_workflow_revision (tenant_id, startup_id, status, updated_at DESC);

CREATE INDEX IF NOT EXISTS ix_aut_workflow_template__list ON ge.aut_workflow_template (tenant_id, startup_id, status, updated_at DESC);

CREATE INDEX IF NOT EXISTS ix_bid_file__list ON ge.bid_file (tenant_id, startup_id, state, updated_at DESC);

CREATE INDEX IF NOT EXISTS ix_bid_package__list ON ge.bid_package (tenant_id, startup_id, state, updated_at DESC);

CREATE INDEX IF NOT EXISTS ix_bid_submission__list ON ge.bid_submission (tenant_id, startup_id, state, updated_at DESC);

CREATE INDEX IF NOT EXISTS ix_cat_claim__list ON ge.cat_claim (tenant_id, startup_id, status, updated_at DESC);

CREATE INDEX IF NOT EXISTS ix_cat_document__list ON ge.cat_document (tenant_id, startup_id, status, updated_at DESC);

CREATE INDEX IF NOT EXISTS ix_cat_offering_capability__list ON ge.cat_offering_capability (tenant_id, startup_id, status, updated_at DESC);

CREATE INDEX IF NOT EXISTS ix_cat_offering_version__list ON ge.cat_offering_version (tenant_id, startup_id, status, updated_at DESC);

CREATE INDEX IF NOT EXISTS ix_cat_price_version__list ON ge.cat_price_version (tenant_id, startup_id, status, updated_at DESC);

CREATE INDEX IF NOT EXISTS ix_coaching_feedback__list ON ge.coaching_feedback (tenant_id, startup_id, state, updated_at DESC);

CREATE INDEX IF NOT EXISTS ix_coaching_rubric__list ON ge.coaching_rubric (tenant_id, startup_id, state, updated_at DESC);

CREATE INDEX IF NOT EXISTS ix_coaching_share__list ON ge.coaching_share (tenant_id, startup_id, state, updated_at DESC);

CREATE INDEX IF NOT EXISTS ix_com_bid__list ON ge.com_bid (tenant_id, startup_id, state, updated_at DESC);

CREATE INDEX IF NOT EXISTS ix_com_contract__list ON ge.com_contract (tenant_id, startup_id, state, updated_at DESC);

CREATE INDEX IF NOT EXISTS ix_com_discrepancy_case__list ON ge.com_discrepancy_case (tenant_id, startup_id, state, updated_at DESC);

CREATE INDEX IF NOT EXISTS ix_com_fulfillment_milestone__list ON ge.com_fulfillment_milestone (tenant_id, startup_id, state, updated_at DESC);

CREATE INDEX IF NOT EXISTS ix_com_inventory_reservation__list ON ge.com_inventory_reservation (tenant_id, startup_id, state, updated_at DESC);

CREATE INDEX IF NOT EXISTS ix_com_invoice__list ON ge.com_invoice (tenant_id, startup_id, state, updated_at DESC);

CREATE INDEX IF NOT EXISTS ix_com_negotiation__list ON ge.com_negotiation (tenant_id, startup_id, state, updated_at DESC);

CREATE INDEX IF NOT EXISTS ix_com_objection__list ON ge.com_objection (tenant_id, startup_id, state, updated_at DESC);

CREATE INDEX IF NOT EXISTS ix_com_order__list ON ge.com_order (tenant_id, startup_id, state, updated_at DESC);

CREATE INDEX IF NOT EXISTS ix_com_payment__list ON ge.com_payment (tenant_id, startup_id, state, updated_at DESC);

CREATE INDEX IF NOT EXISTS ix_com_proposal__list ON ge.com_proposal (tenant_id, startup_id, state, updated_at DESC);

CREATE INDEX IF NOT EXISTS ix_com_proposal_version__list ON ge.com_proposal_version (tenant_id, startup_id, status, updated_at DESC);

CREATE INDEX IF NOT EXISTS ix_com_quote__list ON ge.com_quote (tenant_id, startup_id, state, updated_at DESC);

CREATE INDEX IF NOT EXISTS ix_commerce_order__list ON ge.commerce_order (tenant_id, startup_id, state, updated_at DESC);

CREATE INDEX IF NOT EXISTS ix_counterparty_agent__list ON ge.counterparty_agent (tenant_id, startup_id, state, updated_at DESC);

CREATE INDEX IF NOT EXISTS ix_crm_closure_policy__list ON ge.crm_closure_policy (tenant_id, startup_id, status, updated_at DESC);

CREATE INDEX IF NOT EXISTS ix_crm_form_version__list ON ge.crm_form_version (tenant_id, startup_id, status, updated_at DESC);

CREATE INDEX IF NOT EXISTS ix_crm_lead__list ON ge.crm_lead (tenant_id, startup_id, state, updated_at DESC);

CREATE INDEX IF NOT EXISTS ix_crm_pipeline__list ON ge.crm_pipeline (tenant_id, startup_id, status, updated_at DESC);

CREATE INDEX IF NOT EXISTS ix_crm_stage__list ON ge.crm_stage (tenant_id, startup_id, status, updated_at DESC);

CREATE INDEX IF NOT EXISTS ix_dispute_case__list ON ge.dispute_case (tenant_id, startup_id, state, updated_at DESC);

CREATE INDEX IF NOT EXISTS ix_effect_receipt__list ON ge.effect_receipt (tenant_id, startup_id, state, updated_at DESC);

CREATE INDEX IF NOT EXISTS ix_eng_chat_session__list ON ge.eng_chat_session (tenant_id, startup_id, state, updated_at DESC);

CREATE INDEX IF NOT EXISTS ix_eng_enrollment__list ON ge.eng_enrollment (tenant_id, startup_id, state, updated_at DESC);

CREATE INDEX IF NOT EXISTS ix_eng_meeting__list ON ge.eng_meeting (tenant_id, startup_id, state, updated_at DESC);

CREATE INDEX IF NOT EXISTS ix_eng_message__list ON ge.eng_message (tenant_id, startup_id, state, updated_at DESC);

CREATE INDEX IF NOT EXISTS ix_eng_message_draft__list ON ge.eng_message_draft (tenant_id, startup_id, state, updated_at DESC);

CREATE INDEX IF NOT EXISTS ix_eng_message_template__list ON ge.eng_message_template (tenant_id, startup_id, status, updated_at DESC);

CREATE INDEX IF NOT EXISTS ix_eng_routing_rule__list ON ge.eng_routing_rule (tenant_id, startup_id, status, updated_at DESC);

CREATE INDEX IF NOT EXISTS ix_eng_sequence__list ON ge.eng_sequence (tenant_id, startup_id, status, updated_at DESC);

CREATE INDEX IF NOT EXISTS ix_eng_sequence_step__list ON ge.eng_sequence_step (tenant_id, startup_id, status, updated_at DESC);

CREATE INDEX IF NOT EXISTS ix_eng_thread__list ON ge.eng_thread (tenant_id, startup_id, state, updated_at DESC);

CREATE INDEX IF NOT EXISTS ix_gov_approval_policy__list ON ge.gov_approval_policy (tenant_id, startup_id, status, updated_at DESC);

CREATE INDEX IF NOT EXISTS ix_gov_legal_hold__list ON ge.gov_legal_hold (tenant_id, startup_id, state, updated_at DESC);

CREATE INDEX IF NOT EXISTS ix_gov_policy_version__list ON ge.gov_policy_version (tenant_id, startup_id, status, updated_at DESC);

CREATE INDEX IF NOT EXISTS ix_gov_retention_policy__list ON ge.gov_retention_policy (tenant_id, startup_id, status, updated_at DESC);

CREATE INDEX IF NOT EXISTS ix_intel_match__list ON ge.intel_match (tenant_id, startup_id, state, updated_at DESC);

CREATE INDEX IF NOT EXISTS ix_intel_need__list ON ge.intel_need (tenant_id, startup_id, state, updated_at DESC);

CREATE INDEX IF NOT EXISTS ix_intel_opportunity__list ON ge.intel_opportunity (tenant_id, startup_id, state, updated_at DESC);

CREATE INDEX IF NOT EXISTS ix_intel_scoring_model__list ON ge.intel_scoring_model (tenant_id, startup_id, status, updated_at DESC);

CREATE INDEX IF NOT EXISTS ix_intel_search_plan__list ON ge.intel_search_plan (tenant_id, startup_id, status, updated_at DESC);

CREATE INDEX IF NOT EXISTS ix_intel_signal__list ON ge.intel_signal (tenant_id, startup_id, state, updated_at DESC);

CREATE INDEX IF NOT EXISTS ix_intel_source__list ON ge.intel_source (tenant_id, startup_id, state, updated_at DESC);

CREATE INDEX IF NOT EXISTS ix_intel_source_policy__list ON ge.intel_source_policy (tenant_id, startup_id, status, updated_at DESC);

CREATE INDEX IF NOT EXISTS ix_inv_access_grant__list ON ge.inv_access_grant (tenant_id, startup_id, state, updated_at DESC);

CREATE INDEX IF NOT EXISTS ix_inv_accreditation_verification__list ON ge.inv_accreditation_verification (tenant_id, startup_id, state, updated_at DESC);

CREATE INDEX IF NOT EXISTS ix_inv_advice_boundary_event__list ON ge.inv_advice_boundary_event (tenant_id, startup_id, state, updated_at DESC);

CREATE INDEX IF NOT EXISTS ix_inv_adviser_referral__list ON ge.inv_adviser_referral (tenant_id, startup_id, state, updated_at DESC);

CREATE INDEX IF NOT EXISTS ix_inv_agreement__list ON ge.inv_agreement (tenant_id, startup_id, state, updated_at DESC);

CREATE INDEX IF NOT EXISTS ix_inv_allotment__list ON ge.inv_allotment (tenant_id, startup_id, state, updated_at DESC);

CREATE INDEX IF NOT EXISTS ix_inv_allotment_clock__list ON ge.inv_allotment_clock (tenant_id, startup_id, state, updated_at DESC);

CREATE INDEX IF NOT EXISTS ix_inv_application_money_account__list ON ge.inv_application_money_account (tenant_id, startup_id, state, updated_at DESC);

CREATE INDEX IF NOT EXISTS ix_inv_approval__list ON ge.inv_approval (tenant_id, startup_id, state, updated_at DESC);

CREATE INDEX IF NOT EXISTS ix_inv_bank_account__list ON ge.inv_bank_account (tenant_id, startup_id, state, updated_at DESC);

CREATE INDEX IF NOT EXISTS ix_inv_cap_table_revision__list ON ge.inv_cap_table_revision (tenant_id, startup_id, state, updated_at DESC);

CREATE INDEX IF NOT EXISTS ix_inv_capital_allocation__list ON ge.inv_capital_allocation (tenant_id, startup_id, state, updated_at DESC);

CREATE INDEX IF NOT EXISTS ix_inv_channel__list ON ge.inv_channel (tenant_id, startup_id, state, updated_at DESC);

CREATE INDEX IF NOT EXISTS ix_inv_claim__list ON ge.inv_claim (tenant_id, startup_id, state, updated_at DESC);

CREATE INDEX IF NOT EXISTS ix_inv_closing__list ON ge.inv_closing (tenant_id, startup_id, state, updated_at DESC);

CREATE INDEX IF NOT EXISTS ix_inv_closing_requirement__list ON ge.inv_closing_requirement (tenant_id, startup_id, state, updated_at DESC);

CREATE INDEX IF NOT EXISTS ix_inv_commitment__list ON ge.inv_commitment (tenant_id, startup_id, state, updated_at DESC);

CREATE INDEX IF NOT EXISTS ix_inv_contact__list ON ge.inv_contact (tenant_id, startup_id, state, updated_at DESC);

CREATE INDEX IF NOT EXISTS ix_inv_contact_evidence__list ON ge.inv_contact_evidence (tenant_id, startup_id, state, updated_at DESC);

CREATE INDEX IF NOT EXISTS ix_inv_copilot_action__list ON ge.inv_copilot_action (tenant_id, startup_id, state, updated_at DESC);

CREATE INDEX IF NOT EXISTS ix_inv_counsel_signoff__list ON ge.inv_counsel_signoff (tenant_id, startup_id, state, updated_at DESC);

CREATE INDEX IF NOT EXISTS ix_inv_covenant__list ON ge.inv_covenant (tenant_id, startup_id, state, updated_at DESC);

CREATE INDEX IF NOT EXISTS ix_inv_crossborder_case__list ON ge.inv_crossborder_case (tenant_id, startup_id, state, updated_at DESC);

CREATE INDEX IF NOT EXISTS ix_inv_crossborder_requirement__list ON ge.inv_crossborder_requirement (tenant_id, startup_id, state, updated_at DESC);

CREATE INDEX IF NOT EXISTS ix_inv_dashboard_projection__list ON ge.inv_dashboard_projection (tenant_id, startup_id, state, updated_at DESC);

CREATE INDEX IF NOT EXISTS ix_inv_debt_case__list ON ge.inv_debt_case (tenant_id, startup_id, state, updated_at DESC);

CREATE INDEX IF NOT EXISTS ix_inv_debt_term__list ON ge.inv_debt_term (tenant_id, startup_id, state, updated_at DESC);

CREATE INDEX IF NOT EXISTS ix_inv_decision_action__list ON ge.inv_decision_action (tenant_id, startup_id, state, updated_at DESC);

CREATE INDEX IF NOT EXISTS ix_inv_delivery_event__list ON ge.inv_delivery_event (tenant_id, startup_id, state, updated_at DESC);

CREATE INDEX IF NOT EXISTS ix_inv_deployment_milestone__list ON ge.inv_deployment_milestone (tenant_id, startup_id, state, updated_at DESC);

CREATE INDEX IF NOT EXISTS ix_inv_diligence_request__list ON ge.inv_diligence_request (tenant_id, startup_id, state, updated_at DESC);

CREATE INDEX IF NOT EXISTS ix_inv_disclosure__list ON ge.inv_disclosure (tenant_id, startup_id, state, updated_at DESC);

CREATE INDEX IF NOT EXISTS ix_inv_document__list ON ge.inv_document (tenant_id, startup_id, state, updated_at DESC);

CREATE INDEX IF NOT EXISTS ix_inv_eligibility_check__list ON ge.inv_eligibility_check (tenant_id, startup_id, state, updated_at DESC);

CREATE INDEX IF NOT EXISTS ix_inv_enrollment__list ON ge.inv_enrollment (tenant_id, startup_id, state, updated_at DESC);

CREATE INDEX IF NOT EXISTS ix_inv_esg_commitment__list ON ge.inv_esg_commitment (tenant_id, startup_id, state, updated_at DESC);

CREATE INDEX IF NOT EXISTS ix_inv_esg_disclosure__list ON ge.inv_esg_disclosure (tenant_id, startup_id, state, updated_at DESC);

CREATE INDEX IF NOT EXISTS ix_inv_esg_indicator__list ON ge.inv_esg_indicator (tenant_id, startup_id, state, updated_at DESC);

CREATE INDEX IF NOT EXISTS ix_inv_esg_observation__list ON ge.inv_esg_observation (tenant_id, startup_id, state, updated_at DESC);

CREATE INDEX IF NOT EXISTS ix_inv_event__list ON ge.inv_event (tenant_id, startup_id, state, updated_at DESC);

CREATE INDEX IF NOT EXISTS ix_inv_evidence__list ON ge.inv_evidence (tenant_id, startup_id, state, updated_at DESC);

CREATE INDEX IF NOT EXISTS ix_inv_external_agent_mandate__list ON ge.inv_external_agent_mandate (tenant_id, startup_id, state, updated_at DESC);

CREATE INDEX IF NOT EXISTS ix_inv_feedback__list ON ge.inv_feedback (tenant_id, startup_id, state, updated_at DESC);

CREATE INDEX IF NOT EXISTS ix_inv_filing_task__list ON ge.inv_filing_task (tenant_id, startup_id, state, updated_at DESC);

CREATE INDEX IF NOT EXISTS ix_inv_fit_score__list ON ge.inv_fit_score (tenant_id, startup_id, state, updated_at DESC);

CREATE INDEX IF NOT EXISTS ix_inv_funding_route__list ON ge.inv_funding_route (tenant_id, startup_id, state, updated_at DESC);

CREATE INDEX IF NOT EXISTS ix_inv_fx_rate__list ON ge.inv_fx_rate (tenant_id, startup_id, state, updated_at DESC);

CREATE INDEX IF NOT EXISTS ix_inv_grant_award__list ON ge.inv_grant_award (tenant_id, startup_id, state, updated_at DESC);

CREATE INDEX IF NOT EXISTS ix_inv_grant_budget_line__list ON ge.inv_grant_budget_line (tenant_id, startup_id, state, updated_at DESC);

CREATE INDEX IF NOT EXISTS ix_inv_grant_case__list ON ge.inv_grant_case (tenant_id, startup_id, state, updated_at DESC);

CREATE INDEX IF NOT EXISTS ix_inv_grant_criterion__list ON ge.inv_grant_criterion (tenant_id, startup_id, state, updated_at DESC);

CREATE INDEX IF NOT EXISTS ix_inv_guarantee_evidence__list ON ge.inv_guarantee_evidence (tenant_id, startup_id, state, updated_at DESC);

CREATE INDEX IF NOT EXISTS ix_inv_guard_finding__list ON ge.inv_guard_finding (tenant_id, startup_id, state, updated_at DESC);

CREATE INDEX IF NOT EXISTS ix_inv_holding__list ON ge.inv_holding (tenant_id, startup_id, state, updated_at DESC);

CREATE INDEX IF NOT EXISTS ix_inv_inbound_event__list ON ge.inv_inbound_event (tenant_id, startup_id, state, updated_at DESC);

CREATE INDEX IF NOT EXISTS ix_inv_instrument__list ON ge.inv_instrument (tenant_id, startup_id, state, updated_at DESC);

CREATE INDEX IF NOT EXISTS ix_inv_instrument_term__list ON ge.inv_instrument_term (tenant_id, startup_id, state, updated_at DESC);

CREATE INDEX IF NOT EXISTS ix_inv_integration_connection__list ON ge.inv_integration_connection (tenant_id, startup_id, state, updated_at DESC);

CREATE INDEX IF NOT EXISTS ix_inv_investor__list ON ge.inv_investor (tenant_id, startup_id, state, updated_at DESC);

CREATE INDEX IF NOT EXISTS ix_inv_investor_alias__list ON ge.inv_investor_alias (tenant_id, startup_id, state, updated_at DESC);

CREATE INDEX IF NOT EXISTS ix_inv_investor_classification__list ON ge.inv_investor_classification (tenant_id, startup_id, state, updated_at DESC);

CREATE INDEX IF NOT EXISTS ix_inv_jurisdiction_policy__list ON ge.inv_jurisdiction_policy (tenant_id, startup_id, state, updated_at DESC);

CREATE INDEX IF NOT EXISTS ix_inv_kyc_case__list ON ge.inv_kyc_case (tenant_id, startup_id, state, updated_at DESC);

CREATE INDEX IF NOT EXISTS ix_inv_kyc_provider_result__list ON ge.inv_kyc_provider_result (tenant_id, startup_id, state, updated_at DESC);

CREATE INDEX IF NOT EXISTS ix_inv_legal_check__list ON ge.inv_legal_check (tenant_id, startup_id, state, updated_at DESC);

CREATE INDEX IF NOT EXISTS ix_inv_locale_template__list ON ge.inv_locale_template (tenant_id, startup_id, state, updated_at DESC);

CREATE INDEX IF NOT EXISTS ix_inv_mandate__list ON ge.inv_mandate (tenant_id, startup_id, state, updated_at DESC);

CREATE INDEX IF NOT EXISTS ix_inv_match_candidate__list ON ge.inv_match_candidate (tenant_id, startup_id, state, updated_at DESC);

CREATE INDEX IF NOT EXISTS ix_inv_meeting__list ON ge.inv_meeting (tenant_id, startup_id, state, updated_at DESC);

CREATE INDEX IF NOT EXISTS ix_inv_message__list ON ge.inv_message (tenant_id, startup_id, state, updated_at DESC);

CREATE INDEX IF NOT EXISTS ix_inv_nda__list ON ge.inv_nda (tenant_id, startup_id, state, updated_at DESC);

CREATE INDEX IF NOT EXISTS ix_inv_objection__list ON ge.inv_objection (tenant_id, startup_id, state, updated_at DESC);

CREATE INDEX IF NOT EXISTS ix_inv_objection_rule__list ON ge.inv_objection_rule (tenant_id, startup_id, state, updated_at DESC);

CREATE INDEX IF NOT EXISTS ix_inv_obligation__list ON ge.inv_obligation (tenant_id, startup_id, state, updated_at DESC);

CREATE INDEX IF NOT EXISTS ix_inv_offer__list ON ge.inv_offer (tenant_id, startup_id, state, updated_at DESC);

CREATE INDEX IF NOT EXISTS ix_inv_offer_batch__list ON ge.inv_offer_batch (tenant_id, startup_id, state, updated_at DESC);

CREATE INDEX IF NOT EXISTS ix_inv_offer_counter__list ON ge.inv_offer_counter (tenant_id, startup_id, state, updated_at DESC);

CREATE INDEX IF NOT EXISTS ix_inv_offer_ledger__list ON ge.inv_offer_ledger (tenant_id, startup_id, state, updated_at DESC);

CREATE INDEX IF NOT EXISTS ix_inv_offer_recipient__list ON ge.inv_offer_recipient (tenant_id, startup_id, state, updated_at DESC);

CREATE INDEX IF NOT EXISTS ix_inv_offeree__list ON ge.inv_offeree (tenant_id, startup_id, state, updated_at DESC);

CREATE INDEX IF NOT EXISTS ix_inv_offering__list ON ge.inv_offering (tenant_id, startup_id, state, updated_at DESC);

CREATE INDEX IF NOT EXISTS ix_inv_opportunity__list ON ge.inv_opportunity (tenant_id, startup_id, state, updated_at DESC);

CREATE INDEX IF NOT EXISTS ix_inv_option_grant__list ON ge.inv_option_grant (tenant_id, startup_id, state, updated_at DESC);

CREATE INDEX IF NOT EXISTS ix_inv_outbox__list ON ge.inv_outbox (tenant_id, startup_id, state, updated_at DESC);

CREATE INDEX IF NOT EXISTS ix_inv_outreach_reservation__list ON ge.inv_outreach_reservation (tenant_id, startup_id, state, updated_at DESC);

CREATE INDEX IF NOT EXISTS ix_inv_payment_instruction__list ON ge.inv_payment_instruction (tenant_id, startup_id, state, updated_at DESC);

CREATE INDEX IF NOT EXISTS ix_inv_permission__list ON ge.inv_permission (tenant_id, startup_id, state, updated_at DESC);

CREATE INDEX IF NOT EXISTS ix_inv_promotion_review__list ON ge.inv_promotion_review (tenant_id, startup_id, state, updated_at DESC);

CREATE INDEX IF NOT EXISTS ix_inv_readiness_score__list ON ge.inv_readiness_score (tenant_id, startup_id, state, updated_at DESC);

CREATE INDEX IF NOT EXISTS ix_inv_readiness_snapshot__list ON ge.inv_readiness_snapshot (tenant_id, startup_id, state, updated_at DESC);

CREATE INDEX IF NOT EXISTS ix_inv_receipt__list ON ge.inv_receipt (tenant_id, startup_id, state, updated_at DESC);

CREATE INDEX IF NOT EXISTS ix_inv_receipt_allocation__list ON ge.inv_receipt_allocation (tenant_id, startup_id, state, updated_at DESC);

CREATE INDEX IF NOT EXISTS ix_inv_referral__list ON ge.inv_referral (tenant_id, startup_id, state, updated_at DESC);

CREATE INDEX IF NOT EXISTS ix_inv_refund__list ON ge.inv_refund (tenant_id, startup_id, state, updated_at DESC);

CREATE INDEX IF NOT EXISTS ix_inv_regulatory_deadline__list ON ge.inv_regulatory_deadline (tenant_id, startup_id, state, updated_at DESC);

CREATE INDEX IF NOT EXISTS ix_inv_relationship__list ON ge.inv_relationship (tenant_id, startup_id, state, updated_at DESC);

CREATE INDEX IF NOT EXISTS ix_inv_relationship_provenance__list ON ge.inv_relationship_provenance (tenant_id, startup_id, state, updated_at DESC);

CREATE INDEX IF NOT EXISTS ix_inv_repayment_schedule__list ON ge.inv_repayment_schedule (tenant_id, startup_id, state, updated_at DESC);

CREATE INDEX IF NOT EXISTS ix_inv_resolution__list ON ge.inv_resolution (tenant_id, startup_id, state, updated_at DESC);

CREATE INDEX IF NOT EXISTS ix_inv_room__list ON ge.inv_room (tenant_id, startup_id, state, updated_at DESC);

CREATE INDEX IF NOT EXISTS ix_inv_room_item__list ON ge.inv_room_item (tenant_id, startup_id, state, updated_at DESC);

CREATE INDEX IF NOT EXISTS ix_inv_round__list ON ge.inv_round (tenant_id, startup_id, state, updated_at DESC);

CREATE INDEX IF NOT EXISTS ix_inv_rulepack_activation__list ON ge.inv_rulepack_activation (tenant_id, startup_id, state, updated_at DESC);

CREATE INDEX IF NOT EXISTS ix_inv_runway_scenario__list ON ge.inv_runway_scenario (tenant_id, startup_id, state, updated_at DESC);

CREATE INDEX IF NOT EXISTS ix_inv_scenario__list ON ge.inv_scenario (tenant_id, startup_id, state, updated_at DESC);

CREATE INDEX IF NOT EXISTS ix_inv_screening_hit__list ON ge.inv_screening_hit (tenant_id, startup_id, state, updated_at DESC);

CREATE INDEX IF NOT EXISTS ix_inv_search_plan__list ON ge.inv_search_plan (tenant_id, startup_id, state, updated_at DESC);

CREATE INDEX IF NOT EXISTS ix_inv_search_run__list ON ge.inv_search_run (tenant_id, startup_id, state, updated_at DESC);

CREATE INDEX IF NOT EXISTS ix_inv_sequence__list ON ge.inv_sequence (tenant_id, startup_id, state, updated_at DESC);

CREATE INDEX IF NOT EXISTS ix_inv_shareholder__list ON ge.inv_shareholder (tenant_id, startup_id, state, updated_at DESC);

CREATE INDEX IF NOT EXISTS ix_inv_source__list ON ge.inv_source (tenant_id, startup_id, state, updated_at DESC);

CREATE INDEX IF NOT EXISTS ix_inv_source_policy__list ON ge.inv_source_policy (tenant_id, startup_id, state, updated_at DESC);

CREATE INDEX IF NOT EXISTS ix_inv_stage_event__list ON ge.inv_stage_event (tenant_id, startup_id, state, updated_at DESC);

CREATE INDEX IF NOT EXISTS ix_inv_suppression__list ON ge.inv_suppression (tenant_id, startup_id, state, updated_at DESC);

CREATE INDEX IF NOT EXISTS ix_inv_task__list ON ge.inv_task (tenant_id, startup_id, state, updated_at DESC);

CREATE INDEX IF NOT EXISTS ix_inv_term_version__list ON ge.inv_term_version (tenant_id, startup_id, state, updated_at DESC);

CREATE INDEX IF NOT EXISTS ix_inv_thread__list ON ge.inv_thread (tenant_id, startup_id, state, updated_at DESC);

CREATE INDEX IF NOT EXISTS ix_inv_update__list ON ge.inv_update (tenant_id, startup_id, state, updated_at DESC);

CREATE INDEX IF NOT EXISTS ix_inv_verification_case__list ON ge.inv_verification_case (tenant_id, startup_id, state, updated_at DESC);

CREATE INDEX IF NOT EXISTS ix_inv_vote__list ON ge.inv_vote (tenant_id, startup_id, state, updated_at DESC);

CREATE INDEX IF NOT EXISTS ix_inv_webhook_endpoint__list ON ge.inv_webhook_endpoint (tenant_id, startup_id, state, updated_at DESC);

CREATE INDEX IF NOT EXISTS ix_inv_workflow_run__list ON ge.inv_workflow_run (tenant_id, startup_id, state, updated_at DESC);

CREATE INDEX IF NOT EXISTS ix_kill_switch__list ON ge.kill_switch (tenant_id, startup_id, state, updated_at DESC);

CREATE INDEX IF NOT EXISTS ix_kill_switch_event__list ON ge.kill_switch_event (tenant_id, startup_id, state, updated_at DESC);

CREATE INDEX IF NOT EXISTS ix_lcy_customer_subscription__list ON ge.lcy_customer_subscription (tenant_id, startup_id, state, updated_at DESC);

CREATE INDEX IF NOT EXISTS ix_lcy_deployment__list ON ge.lcy_deployment (tenant_id, startup_id, state, updated_at DESC);

CREATE INDEX IF NOT EXISTS ix_lcy_integration_deal__list ON ge.lcy_integration_deal (tenant_id, startup_id, state, updated_at DESC);

CREATE INDEX IF NOT EXISTS ix_lcy_onboarding__list ON ge.lcy_onboarding (tenant_id, startup_id, state, updated_at DESC);

CREATE INDEX IF NOT EXISTS ix_lcy_pilot__list ON ge.lcy_pilot (tenant_id, startup_id, state, updated_at DESC);

CREATE INDEX IF NOT EXISTS ix_lcy_renewal__list ON ge.lcy_renewal (tenant_id, startup_id, state, updated_at DESC);

CREATE INDEX IF NOT EXISTS ix_lcy_task__list ON ge.lcy_task (tenant_id, startup_id, state, updated_at DESC);

CREATE INDEX IF NOT EXISTS ix_ledger_entry__list ON ge.ledger_entry (tenant_id, startup_id, state, updated_at DESC);

CREATE INDEX IF NOT EXISTS ix_mandate__list ON ge.mandate (tenant_id, startup_id, state, updated_at DESC);

CREATE INDEX IF NOT EXISTS ix_mandate_approval__list ON ge.mandate_approval (tenant_id, startup_id, state, updated_at DESC);

CREATE INDEX IF NOT EXISTS ix_mandate_consumption__list ON ge.mandate_consumption (tenant_id, startup_id, state, updated_at DESC);

CREATE INDEX IF NOT EXISTS ix_mandate_counter__list ON ge.mandate_counter (tenant_id, startup_id, state, updated_at DESC);

CREATE INDEX IF NOT EXISTS ix_mandate_decision__list ON ge.mandate_decision (tenant_id, startup_id, state, updated_at DESC);

CREATE INDEX IF NOT EXISTS ix_mandate_limit__list ON ge.mandate_limit (tenant_id, startup_id, state, updated_at DESC);

CREATE INDEX IF NOT EXISTS ix_mandate_restriction__list ON ge.mandate_restriction (tenant_id, startup_id, state, updated_at DESC);

CREATE INDEX IF NOT EXISTS ix_mandate_scope_item__list ON ge.mandate_scope_item (tenant_id, startup_id, state, updated_at DESC);

CREATE INDEX IF NOT EXISTS ix_mandate_version__list ON ge.mandate_version (tenant_id, startup_id, state, updated_at DESC);

CREATE INDEX IF NOT EXISTS ix_mandate_window__list ON ge.mandate_window (tenant_id, startup_id, state, updated_at DESC);

CREATE INDEX IF NOT EXISTS ix_mkt_ad_campaign__list ON ge.mkt_ad_campaign (tenant_id, startup_id, state, updated_at DESC);

CREATE INDEX IF NOT EXISTS ix_mkt_audience__list ON ge.mkt_audience (tenant_id, startup_id, status, updated_at DESC);

CREATE INDEX IF NOT EXISTS ix_mkt_campaign__list ON ge.mkt_campaign (tenant_id, startup_id, state, updated_at DESC);

CREATE INDEX IF NOT EXISTS ix_mkt_campaign_version__list ON ge.mkt_campaign_version (tenant_id, startup_id, status, updated_at DESC);

CREATE INDEX IF NOT EXISTS ix_mkt_content_asset__list ON ge.mkt_content_asset (tenant_id, startup_id, state, updated_at DESC);

CREATE INDEX IF NOT EXISTS ix_mkt_content_version__list ON ge.mkt_content_version (tenant_id, startup_id, status, updated_at DESC);

CREATE INDEX IF NOT EXISTS ix_mkt_event__list ON ge.mkt_event (tenant_id, startup_id, state, updated_at DESC);

CREATE INDEX IF NOT EXISTS ix_mkt_publication__list ON ge.mkt_publication (tenant_id, startup_id, state, updated_at DESC);

CREATE INDEX IF NOT EXISTS ix_mkt_referral__list ON ge.mkt_referral (tenant_id, startup_id, state, updated_at DESC);

CREATE INDEX IF NOT EXISTS ix_mkt_registration__list ON ge.mkt_registration (tenant_id, startup_id, state, updated_at DESC);

CREATE INDEX IF NOT EXISTS ix_mkt_seo_issue__list ON ge.mkt_seo_issue (tenant_id, startup_id, state, updated_at DESC);

CREATE INDEX IF NOT EXISTS ix_mkt_social_publication__list ON ge.mkt_social_publication (tenant_id, startup_id, state, updated_at DESC);

CREATE INDEX IF NOT EXISTS ix_negotiation_session__list ON ge.negotiation_session (tenant_id, startup_id, state, updated_at DESC);

CREATE INDEX IF NOT EXISTS ix_negotiation_step__list ON ge.negotiation_step (tenant_id, startup_id, state, updated_at DESC);

CREATE INDEX IF NOT EXISTS ix_ops_job_run__list ON ge.ops_job_run (tenant_id, startup_id, state, updated_at DESC);

CREATE INDEX IF NOT EXISTS ix_ops_notification__list ON ge.ops_notification (tenant_id, startup_id, state, updated_at DESC);

CREATE INDEX IF NOT EXISTS ix_payment_mandate__list ON ge.payment_mandate (tenant_id, startup_id, state, updated_at DESC);

CREATE INDEX IF NOT EXISTS ix_payment_txn__list ON ge.payment_txn (tenant_id, startup_id, state, updated_at DESC);

CREATE INDEX IF NOT EXISTS ix_portal_profile__list ON ge.portal_profile (tenant_id, startup_id, state, updated_at DESC);

CREATE INDEX IF NOT EXISTS ix_recon_break__list ON ge.recon_break (tenant_id, startup_id, state, updated_at DESC);

CREATE INDEX IF NOT EXISTS ix_recon_run__list ON ge.recon_run (tenant_id, startup_id, state, updated_at DESC);

CREATE INDEX IF NOT EXISTS ix_ref_dataset__list ON ge.ref_dataset (tenant_id, startup_id, status, updated_at DESC);

CREATE INDEX IF NOT EXISTS ix_ref_value__list ON ge.ref_value (tenant_id, startup_id, status, updated_at DESC);

CREATE INDEX IF NOT EXISTS ix_refund__list ON ge.refund (tenant_id, startup_id, state, updated_at DESC);

CREATE INDEX IF NOT EXISTS ix_saas_entitlement__list ON ge.saas_entitlement (tenant_id, startup_id, status, updated_at DESC);

CREATE INDEX IF NOT EXISTS ix_saas_import_job__list ON ge.saas_import_job (tenant_id, startup_id, state, updated_at DESC);

CREATE INDEX IF NOT EXISTS ix_saas_service_request__list ON ge.saas_service_request (tenant_id, startup_id, status, updated_at DESC);

CREATE INDEX IF NOT EXISTS ix_saas_subscription__list ON ge.saas_subscription (tenant_id, startup_id, state, updated_at DESC);

CREATE INDEX IF NOT EXISTS ix_saas_support_access_grant__list ON ge.saas_support_access_grant (tenant_id, startup_id, state, updated_at DESC);

CREATE INDEX IF NOT EXISTS ix_settlement_batch__list ON ge.settlement_batch (tenant_id, startup_id, state, updated_at DESC);

CREATE INDEX IF NOT EXISTS ix_ten_business_template__list ON ge.ten_business_template (tenant_id, startup_id, status, updated_at DESC);

CREATE INDEX IF NOT EXISTS ix_ten_capability_profile__list ON ge.ten_capability_profile (tenant_id, startup_id, status, updated_at DESC);

CREATE INDEX IF NOT EXISTS ix_ten_membership__list ON ge.ten_membership (tenant_id, startup_id, status, updated_at DESC);

CREATE INDEX IF NOT EXISTS ix_ten_portal_grant__list ON ge.ten_portal_grant (tenant_id, startup_id, state, updated_at DESC);

CREATE INDEX IF NOT EXISTS ix_voice_access_log__list ON ge.voice_access_log (tenant_id, startup_id, state, updated_at DESC);

CREATE INDEX IF NOT EXISTS ix_voice_campaign__list ON ge.voice_campaign (tenant_id, startup_id, state, updated_at DESC);

CREATE INDEX IF NOT EXISTS ix_voice_campaign_contact__list ON ge.voice_campaign_contact (tenant_id, startup_id, state, updated_at DESC);

CREATE INDEX IF NOT EXISTS ix_voice_consent_evidence__list ON ge.voice_consent_evidence (tenant_id, startup_id, state, updated_at DESC);

CREATE INDEX IF NOT EXISTS ix_voice_handoff__list ON ge.voice_handoff (tenant_id, startup_id, state, updated_at DESC);

CREATE INDEX IF NOT EXISTS ix_voice_leg__list ON ge.voice_leg (tenant_id, startup_id, state, updated_at DESC);

CREATE INDEX IF NOT EXISTS ix_voice_legal_hold__list ON ge.voice_legal_hold (tenant_id, startup_id, state, updated_at DESC);

CREATE INDEX IF NOT EXISTS ix_voice_meter_event__list ON ge.voice_meter_event (tenant_id, startup_id, state, updated_at DESC);

CREATE INDEX IF NOT EXISTS ix_voice_number__list ON ge.voice_number (tenant_id, startup_id, state, updated_at DESC);

CREATE INDEX IF NOT EXISTS ix_voice_number_pool__list ON ge.voice_number_pool (tenant_id, startup_id, state, updated_at DESC);

CREATE INDEX IF NOT EXISTS ix_voice_recording__list ON ge.voice_recording (tenant_id, startup_id, state, updated_at DESC);

CREATE INDEX IF NOT EXISTS ix_voice_script__list ON ge.voice_script (tenant_id, startup_id, state, updated_at DESC);

CREATE INDEX IF NOT EXISTS ix_voice_script_version__list ON ge.voice_script_version (tenant_id, startup_id, state, updated_at DESC);

CREATE INDEX IF NOT EXISTS ix_voice_scrub_result__list ON ge.voice_scrub_result (tenant_id, startup_id, state, updated_at DESC);

CREATE INDEX IF NOT EXISTS ix_voice_session__list ON ge.voice_session (tenant_id, startup_id, state, updated_at DESC);

CREATE INDEX IF NOT EXISTS ix_voice_summary__list ON ge.voice_summary (tenant_id, startup_id, state, updated_at DESC);

CREATE INDEX IF NOT EXISTS ix_voice_transcript__list ON ge.voice_transcript (tenant_id, startup_id, state, updated_at DESC);

CREATE INDEX IF NOT EXISTS ix_voice_transcript_segment__list ON ge.voice_transcript_segment (tenant_id, startup_id, state, updated_at DESC);

CREATE INDEX IF NOT EXISTS ix_voice_voicemail__list ON ge.voice_voicemail (tenant_id, startup_id, state, updated_at DESC);
