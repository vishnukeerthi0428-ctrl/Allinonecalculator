-- V0009__constraints_and_foreign_keys
SET search_path = ge, extensions, public;

SELECT set_config('app.zone', coalesce(nullif(current_setting('app.deployment_region', true), ''), 'IN'), false);

SELECT set_config('app.deployment_region', coalesce(nullif(current_setting('app.deployment_region', true), ''), 'IN'), false);

ALTER TABLE ge.ten_capability_profile ADD CONSTRAINT ck_ten_capability_profile__revision CHECK (revision >= 1);

ALTER TABLE ge.ten_capability_profile ADD CONSTRAINT ck_ten_capability_profile__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.ten_capability_profile ADD CONSTRAINT ck_ten_capability_profile__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.ten_capability_profile ADD CONSTRAINT ck_ten_capability_profile__version_no CHECK (version_no >= 1);

ALTER TABLE ge.ten_capability_profile ADD CONSTRAINT ck_ten_capability_profile__content_hash CHECK (content_hash ~ '^[0-9a-f]{64}$');

ALTER TABLE ge.ten_domain ADD CONSTRAINT ck_ten_domain__revision CHECK (revision >= 1);

ALTER TABLE ge.ten_domain ADD CONSTRAINT ck_ten_domain__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.ten_domain ADD CONSTRAINT ck_ten_domain__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.ten_user ADD CONSTRAINT ck_ten_user__revision CHECK (revision >= 1);

ALTER TABLE ge.ten_membership ADD CONSTRAINT ck_ten_membership__revision CHECK (revision >= 1);

ALTER TABLE ge.ten_membership ADD CONSTRAINT ck_ten_membership__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.ten_membership ADD CONSTRAINT ck_ten_membership__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.ten_membership ADD CONSTRAINT ck_ten_membership__status CHECK (status IN ('invited', 'active', 'suspended', 'expired', 'revoked'));

ALTER TABLE ge.ten_portal_grant ADD CONSTRAINT ck_ten_portal_grant__revision CHECK (revision >= 1);

ALTER TABLE ge.ten_portal_grant ADD CONSTRAINT ck_ten_portal_grant__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.ten_portal_grant ADD CONSTRAINT ck_ten_portal_grant__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.ten_saved_view ADD CONSTRAINT ck_ten_saved_view__revision CHECK (revision >= 1);

ALTER TABLE ge.ten_saved_view ADD CONSTRAINT ck_ten_saved_view__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.ten_saved_view ADD CONSTRAINT ck_ten_saved_view__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.ref_dataset ADD CONSTRAINT ck_ref_dataset__revision CHECK (revision >= 1);

ALTER TABLE ge.ref_dataset ADD CONSTRAINT ck_ref_dataset__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.ref_dataset ADD CONSTRAINT ck_ref_dataset__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.ref_dataset ADD CONSTRAINT ck_ref_dataset__version_no CHECK (version_no >= 1);

ALTER TABLE ge.ref_dataset ADD CONSTRAINT ck_ref_dataset__content_hash CHECK (content_hash ~ '^[0-9a-f]{64}$');

ALTER TABLE ge.ref_value ADD CONSTRAINT ck_ref_value__revision CHECK (revision >= 1);

ALTER TABLE ge.ref_value ADD CONSTRAINT ck_ref_value__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.ref_value ADD CONSTRAINT ck_ref_value__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.ref_value ADD CONSTRAINT ck_ref_value__version_no CHECK (version_no >= 1);

ALTER TABLE ge.ref_value ADD CONSTRAINT ck_ref_value__content_hash CHECK (content_hash ~ '^[0-9a-f]{64}$');

ALTER TABLE ge.ref_currency ADD CONSTRAINT ck_ref_currency__revision CHECK (revision >= 1);

ALTER TABLE ge.ref_country ADD CONSTRAINT ck_ref_country__revision CHECK (revision >= 1);

ALTER TABLE ge.ref_unit ADD CONSTRAINT ck_ref_unit__revision CHECK (revision >= 1);

ALTER TABLE ge.ref_unit ADD CONSTRAINT ck_ref_unit__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.ref_unit ADD CONSTRAINT ck_ref_unit__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.cat_offering_version ADD CONSTRAINT ck_cat_offering_version__revision CHECK (revision >= 1);

ALTER TABLE ge.cat_offering_version ADD CONSTRAINT ck_cat_offering_version__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.cat_offering_version ADD CONSTRAINT ck_cat_offering_version__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.cat_offering_version ADD CONSTRAINT ck_cat_offering_version__version_no CHECK (version_no >= 1);

ALTER TABLE ge.cat_offering_version ADD CONSTRAINT ck_cat_offering_version__content_hash CHECK (content_hash ~ '^[0-9a-f]{64}$');

ALTER TABLE ge.cat_offering_version ADD CONSTRAINT ck_cat_offering_version__min_order_qty CHECK (min_order_qty >= 0);

ALTER TABLE ge.cat_offering_version ADD CONSTRAINT ck_cat_offering_version__max_order_qty CHECK (max_order_qty >= 0);

ALTER TABLE ge.cat_capability ADD CONSTRAINT ck_cat_capability__revision CHECK (revision >= 1);

ALTER TABLE ge.cat_capability ADD CONSTRAINT ck_cat_capability__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.cat_capability ADD CONSTRAINT ck_cat_capability__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.cat_offering_capability ADD CONSTRAINT ck_cat_offering_capability__revision CHECK (revision >= 1);

ALTER TABLE ge.cat_offering_capability ADD CONSTRAINT ck_cat_offering_capability__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.cat_offering_capability ADD CONSTRAINT ck_cat_offering_capability__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.cat_offering_capability ADD CONSTRAINT ck_cat_offering_capability__version_no CHECK (version_no >= 1);

ALTER TABLE ge.cat_offering_capability ADD CONSTRAINT ck_cat_offering_capability__content_hash CHECK (content_hash ~ '^[0-9a-f]{64}$');

ALTER TABLE ge.cat_claim ADD CONSTRAINT ck_cat_claim__revision CHECK (revision >= 1);

ALTER TABLE ge.cat_claim ADD CONSTRAINT ck_cat_claim__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.cat_claim ADD CONSTRAINT ck_cat_claim__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.cat_claim ADD CONSTRAINT ck_cat_claim__version_no CHECK (version_no >= 1);

ALTER TABLE ge.cat_claim ADD CONSTRAINT ck_cat_claim__content_hash CHECK (content_hash ~ '^[0-9a-f]{64}$');

ALTER TABLE ge.cat_claim ADD CONSTRAINT ck_cat_claim__claim_type CHECK (claim_type IN ('capability', 'traction', 'certification', 'outcome', 'comparative', 'testimonial'));

ALTER TABLE ge.cat_claim ADD CONSTRAINT ck_cat_claim__evidence_count CHECK (evidence_count > 0);

ALTER TABLE ge.cat_price_version ADD CONSTRAINT ck_cat_price_version__revision CHECK (revision >= 1);

ALTER TABLE ge.cat_price_version ADD CONSTRAINT ck_cat_price_version__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.cat_price_version ADD CONSTRAINT ck_cat_price_version__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.cat_price_version ADD CONSTRAINT ck_cat_price_version__version_no CHECK (version_no >= 1);

ALTER TABLE ge.cat_price_version ADD CONSTRAINT ck_cat_price_version__content_hash CHECK (content_hash ~ '^[0-9a-f]{64}$');

ALTER TABLE ge.cat_price_version ADD CONSTRAINT ck_cat_price_version__currency CHECK (currency ~ '^[A-Z]{3}$');

ALTER TABLE ge.cat_price_version ADD CONSTRAINT ck_cat_price_version__unit_price CHECK (unit_price >= 0);

ALTER TABLE ge.cat_price_version ADD CONSTRAINT ck_cat_price_version__unit_cost CHECK (unit_cost >= 0);

ALTER TABLE ge.cat_price_version ADD CONSTRAINT ck_cat_price_version__tax_rate_pct CHECK (tax_rate_pct BETWEEN 0 AND 100);

ALTER TABLE ge.cat_launch_approval ADD CONSTRAINT ck_cat_launch_approval__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.cat_document ADD CONSTRAINT ck_cat_document__revision CHECK (revision >= 1);

ALTER TABLE ge.cat_document ADD CONSTRAINT ck_cat_document__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.cat_document ADD CONSTRAINT ck_cat_document__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.cat_document ADD CONSTRAINT ck_cat_document__version_no CHECK (version_no >= 1);

ALTER TABLE ge.cat_document ADD CONSTRAINT ck_cat_document__content_hash CHECK (content_hash ~ '^[0-9a-f]{64}$');

ALTER TABLE ge.cat_document ADD CONSTRAINT ck_cat_document__doc_kind CHECK (doc_kind IN ('product_sheet', 'faq', 'policy', 'case_study', 'price_list', 'contract_template', 'other'));

ALTER TABLE ge.cat_document ADD CONSTRAINT ck_cat_document__classification CHECK (classification IN ('public', 'internal', 'confidential', 'restricted'));

ALTER TABLE ge.cat_document ADD CONSTRAINT ck_cat_document__scan_result CHECK (scan_result IN ('pending', 'clean', 'infected', 'error'));

ALTER TABLE ge.cat_document ADD CONSTRAINT ck_cat_document__chunk_count CHECK (chunk_count >= 0);

ALTER TABLE ge.cat_chunk ADD CONSTRAINT ck_cat_chunk__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.cat_chunk ADD CONSTRAINT ck_cat_chunk__ordinal CHECK (ordinal >= 0);

ALTER TABLE ge.cat_chunk ADD CONSTRAINT ck_cat_chunk__token_count CHECK (token_count > 0);

ALTER TABLE ge.cat_embedding ADD CONSTRAINT ck_cat_embedding__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.gov_policy_version ADD CONSTRAINT ck_gov_policy_version__revision CHECK (revision >= 1);

ALTER TABLE ge.gov_policy_version ADD CONSTRAINT ck_gov_policy_version__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.gov_policy_version ADD CONSTRAINT ck_gov_policy_version__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.gov_policy_version ADD CONSTRAINT ck_gov_policy_version__version_no CHECK (version_no >= 1);

ALTER TABLE ge.gov_policy_version ADD CONSTRAINT ck_gov_policy_version__content_hash CHECK (content_hash ~ '^[0-9a-f]{64}$');

ALTER TABLE ge.gov_policy_version ADD CONSTRAINT ck_gov_policy_version__policy_type CHECK (policy_type IN ('privacy_notice', 'consent_text', 'quiet_hours', 'frequency_cap', 'eligibility', 'retention_override', 'closure', 'lost_deal'));

ALTER TABLE ge.gov_eligibility_decision ADD CONSTRAINT ck_gov_eligibility_decision__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.gov_eligibility_decision ADD CONSTRAINT ck_gov_eligibility_decision__action_type CHECK (action_type IN ('send_email', 'send_whatsapp', 'enrol', 'publish_ad_audience', 'book_meeting', 'call', 'campaign_dispatch'));

ALTER TABLE ge.gov_eligibility_decision ADD CONSTRAINT ck_gov_eligibility_decision__evaluation_point CHECK (evaluation_point IN ('plan', 'approval', 'dispatch'));

ALTER TABLE ge.gov_eligibility_decision ADD CONSTRAINT ck_gov_eligibility_decision__result CHECK (result IN ('eligible', 'ineligible', 'unknown'));

ALTER TABLE ge.gov_policy_decision ADD CONSTRAINT ck_gov_policy_decision__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.gov_approval_policy ADD CONSTRAINT ck_gov_approval_policy__revision CHECK (revision >= 1);

ALTER TABLE ge.gov_approval_policy ADD CONSTRAINT ck_gov_approval_policy__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.gov_approval_policy ADD CONSTRAINT ck_gov_approval_policy__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.gov_approval_policy ADD CONSTRAINT ck_gov_approval_policy__version_no CHECK (version_no >= 1);

ALTER TABLE ge.gov_approval_policy ADD CONSTRAINT ck_gov_approval_policy__content_hash CHECK (content_hash ~ '^[0-9a-f]{64}$');

ALTER TABLE ge.gov_approval ADD CONSTRAINT ck_gov_approval__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.gov_approval ADD CONSTRAINT ck_gov_approval__object_type CHECK (object_type IN ('offering_version', 'claim', 'price_version', 'document', 'content_version', 'publication', 'campaign_version', 'ad_budget', 'message_draft', 'template', 'proposal_version', 'quote', 'contract', 'bid_decision', 'bid_submission', 'order', 'invoice', 'payment_verification_maker', 'payment_verification_checker', 'config_revision', 'workflow_revision', 'autonomy_plan', 'export_job', 'support_access_grant', 'plan_version', 'launch'));

ALTER TABLE ge.gov_approval ADD CONSTRAINT ck_gov_approval__decision CHECK (decision IN ('approved', 'rejected', 'revoked', 'expired'));

ALTER TABLE ge.gov_approval_delegation ADD CONSTRAINT ck_gov_approval_delegation__revision CHECK (revision >= 1);

ALTER TABLE ge.gov_approval_delegation ADD CONSTRAINT ck_gov_approval_delegation__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.gov_approval_delegation ADD CONSTRAINT ck_gov_approval_delegation__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.gov_retention_policy ADD CONSTRAINT ck_gov_retention_policy__revision CHECK (revision >= 1);

ALTER TABLE ge.gov_retention_policy ADD CONSTRAINT ck_gov_retention_policy__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.gov_retention_policy ADD CONSTRAINT ck_gov_retention_policy__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.gov_retention_policy ADD CONSTRAINT ck_gov_retention_policy__version_no CHECK (version_no >= 1);

ALTER TABLE ge.gov_retention_policy ADD CONSTRAINT ck_gov_retention_policy__content_hash CHECK (content_hash ~ '^[0-9a-f]{64}$');

ALTER TABLE ge.gov_legal_hold ADD CONSTRAINT ck_gov_legal_hold__revision CHECK (revision >= 1);

ALTER TABLE ge.gov_legal_hold ADD CONSTRAINT ck_gov_legal_hold__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.gov_legal_hold ADD CONSTRAINT ck_gov_legal_hold__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.int_credential_ref ADD CONSTRAINT ck_int_credential_ref__revision CHECK (revision >= 1);

ALTER TABLE ge.int_credential_ref ADD CONSTRAINT ck_int_credential_ref__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.int_credential_ref ADD CONSTRAINT ck_int_credential_ref__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.int_quota ADD CONSTRAINT ck_int_quota__revision CHECK (revision >= 1);

ALTER TABLE ge.int_quota ADD CONSTRAINT ck_int_quota__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.int_quota ADD CONSTRAINT ck_int_quota__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.int_provider_event ADD CONSTRAINT ck_int_provider_event__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.ai_agent_definition ADD CONSTRAINT ck_ai_agent_definition__revision CHECK (revision >= 1);

ALTER TABLE ge.ai_agent_definition ADD CONSTRAINT ck_ai_agent_definition__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.ai_agent_definition ADD CONSTRAINT ck_ai_agent_definition__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.ai_agent_definition ADD CONSTRAINT ck_ai_agent_definition__version_no CHECK (version_no >= 1);

ALTER TABLE ge.ai_agent_definition ADD CONSTRAINT ck_ai_agent_definition__content_hash CHECK (content_hash ~ '^[0-9a-f]{64}$');

ALTER TABLE ge.ai_model_run ADD CONSTRAINT ck_ai_model_run__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.ai_model_run ADD CONSTRAINT ck_ai_model_run__purpose CHECK (purpose IN ('classify', 'extract', 'draft', 'match', 'summarize', 'answer', 'copilot', 'translate', 'eval'));

ALTER TABLE ge.ai_model_run ADD CONSTRAINT ck_ai_model_run__tier CHECK (tier IN ('t0_rule', 't0_cache', 't1a', 't1b', 't2_free', 't3_degrade'));

ALTER TABLE ge.ai_model_run ADD CONSTRAINT ck_ai_model_run__data_classification_max CHECK (data_classification_max IN ('public', 'internal', 'confidential', 'restricted'));

ALTER TABLE ge.ai_model_run ADD CONSTRAINT ck_ai_model_run__input_tokens CHECK (input_tokens >= 0);

ALTER TABLE ge.ai_model_run ADD CONSTRAINT ck_ai_model_run__output_tokens CHECK (output_tokens >= 0);

ALTER TABLE ge.ai_model_run ADD CONSTRAINT ck_ai_model_run__cached_tokens CHECK (cached_tokens >= 0);

ALTER TABLE ge.ai_model_run ADD CONSTRAINT ck_ai_model_run__outcome CHECK (outcome IN ('accepted', 'abstained', 'rejected_schema', 'rejected_claim', 'degraded', 'budget_denied', 'error'));

ALTER TABLE ge.ai_model_run ADD CONSTRAINT ck_ai_model_run__cost_reserved CHECK (cost_reserved >= 0);

ALTER TABLE ge.ai_model_run ADD CONSTRAINT ck_ai_model_run__cost_actual CHECK (cost_actual >= 0);

ALTER TABLE ge.ai_eval_case ADD CONSTRAINT ck_ai_eval_case__revision CHECK (revision >= 1);

ALTER TABLE ge.ai_eval_case ADD CONSTRAINT ck_ai_eval_case__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.ai_eval_case ADD CONSTRAINT ck_ai_eval_case__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.ai_eval_case ADD CONSTRAINT ck_ai_eval_case__version_no CHECK (version_no >= 1);

ALTER TABLE ge.ai_eval_case ADD CONSTRAINT ck_ai_eval_case__content_hash CHECK (content_hash ~ '^[0-9a-f]{64}$');

ALTER TABLE ge.ai_feedback ADD CONSTRAINT ck_ai_feedback__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.ai_cost_ledger ADD CONSTRAINT ck_ai_cost_ledger__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.ai_cost_ledger ADD CONSTRAINT ck_ai_cost_ledger__entry_type CHECK (entry_type IN ('reserve', 'settle', 'release', 'adjustment', 'top_up'));

ALTER TABLE ge.intel_source ADD CONSTRAINT ck_intel_source__revision CHECK (revision >= 1);

ALTER TABLE ge.intel_source ADD CONSTRAINT ck_intel_source__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.intel_source ADD CONSTRAINT ck_intel_source__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.intel_source ADD CONSTRAINT ck_intel_source__source_kind CHECK (source_kind IN ('website', 'tender_portal', 'registry', 'news', 'social_api', 'licensed_api', 'directory', 'search_api'));

ALTER TABLE ge.intel_source ADD CONSTRAINT ck_intel_source__state CHECK (state IN ('proposed', 'pending_approval', 'active', 'expired', 'revoked'));

ALTER TABLE ge.intel_source ADD CONSTRAINT ck_intel_source__freshness_sla_days CHECK (freshness_sla_days BETWEEN 1 AND 365);

ALTER TABLE ge.intel_source_policy ADD CONSTRAINT ck_intel_source_policy__revision CHECK (revision >= 1);

ALTER TABLE ge.intel_source_policy ADD CONSTRAINT ck_intel_source_policy__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.intel_source_policy ADD CONSTRAINT ck_intel_source_policy__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.intel_source_policy ADD CONSTRAINT ck_intel_source_policy__version_no CHECK (version_no >= 1);

ALTER TABLE ge.intel_source_policy ADD CONSTRAINT ck_intel_source_policy__content_hash CHECK (content_hash ~ '^[0-9a-f]{64}$');

ALTER TABLE ge.intel_search_plan ADD CONSTRAINT ck_intel_search_plan__revision CHECK (revision >= 1);

ALTER TABLE ge.intel_search_plan ADD CONSTRAINT ck_intel_search_plan__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.intel_search_plan ADD CONSTRAINT ck_intel_search_plan__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.intel_search_plan ADD CONSTRAINT ck_intel_search_plan__version_no CHECK (version_no >= 1);

ALTER TABLE ge.intel_search_plan ADD CONSTRAINT ck_intel_search_plan__content_hash CHECK (content_hash ~ '^[0-9a-f]{64}$');

ALTER TABLE ge.intel_query_run ADD CONSTRAINT ck_intel_query_run__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.intel_source_record ADD CONSTRAINT ck_intel_source_record__revision CHECK (revision >= 1);

ALTER TABLE ge.intel_source_record ADD CONSTRAINT ck_intel_source_record__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.intel_source_record ADD CONSTRAINT ck_intel_source_record__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.intel_fetch_log ADD CONSTRAINT ck_intel_fetch_log__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.intel_evidence ADD CONSTRAINT ck_intel_evidence__revision CHECK (revision >= 1);

ALTER TABLE ge.intel_evidence ADD CONSTRAINT ck_intel_evidence__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.intel_evidence ADD CONSTRAINT ck_intel_evidence__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.intel_evidence ADD CONSTRAINT ck_intel_evidence__confidence CHECK (confidence BETWEEN 0 AND 1);

ALTER TABLE ge.intel_evidence ADD CONSTRAINT ck_intel_evidence__freshness_state CHECK (freshness_state IN ('fresh', 'stale', 'source_expired', 'purged'));

ALTER TABLE ge.intel_evidence ADD CONSTRAINT ck_intel_evidence__rights_state CHECK (rights_state IN ('permitted', 'quarantined'));

ALTER TABLE ge.intel_social_post ADD CONSTRAINT ck_intel_social_post__revision CHECK (revision >= 1);

ALTER TABLE ge.intel_social_post ADD CONSTRAINT ck_intel_social_post__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.intel_social_post ADD CONSTRAINT ck_intel_social_post__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.intel_competitor ADD CONSTRAINT ck_intel_competitor__revision CHECK (revision >= 1);

ALTER TABLE ge.intel_competitor ADD CONSTRAINT ck_intel_competitor__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.intel_competitor ADD CONSTRAINT ck_intel_competitor__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.intel_market_event ADD CONSTRAINT ck_intel_market_event__revision CHECK (revision >= 1);

ALTER TABLE ge.intel_market_event ADD CONSTRAINT ck_intel_market_event__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.intel_market_event ADD CONSTRAINT ck_intel_market_event__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.intel_organization ADD CONSTRAINT ck_intel_organization__revision CHECK (revision >= 1);

ALTER TABLE ge.intel_organization ADD CONSTRAINT ck_intel_organization__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.intel_organization ADD CONSTRAINT ck_intel_organization__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.intel_organization ADD CONSTRAINT ck_intel_organization__relationship CHECK (relationship IN ('prospect', 'customer', 'supplier', 'partner', 'competitor', 'institution'));

ALTER TABLE ge.intel_location ADD CONSTRAINT ck_intel_location__revision CHECK (revision >= 1);

ALTER TABLE ge.intel_location ADD CONSTRAINT ck_intel_location__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.intel_location ADD CONSTRAINT ck_intel_location__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.intel_alias ADD CONSTRAINT ck_intel_alias__revision CHECK (revision >= 1);

ALTER TABLE ge.intel_alias ADD CONSTRAINT ck_intel_alias__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.intel_alias ADD CONSTRAINT ck_intel_alias__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.intel_signal_type ADD CONSTRAINT ck_intel_signal_type__revision CHECK (revision >= 1);

ALTER TABLE ge.intel_signal_type ADD CONSTRAINT ck_intel_signal_type__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.intel_signal_type ADD CONSTRAINT ck_intel_signal_type__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.intel_signal ADD CONSTRAINT ck_intel_signal__revision CHECK (revision >= 1);

ALTER TABLE ge.intel_signal ADD CONSTRAINT ck_intel_signal__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.intel_signal ADD CONSTRAINT ck_intel_signal__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.intel_signal ADD CONSTRAINT ck_intel_signal__derivation CHECK (derivation IN ('explicit', 'inferred'));

ALTER TABLE ge.intel_signal ADD CONSTRAINT ck_intel_signal__state CHECK (state IN ('proposed', 'in_review', 'confirmed', 'rejected', 'expired'));

ALTER TABLE ge.intel_signal ADD CONSTRAINT ck_intel_signal__confidence CHECK (confidence BETWEEN 0 AND 1);

ALTER TABLE ge.intel_signal ADD CONSTRAINT ck_intel_signal__review_verdict CHECK (review_verdict IN ('correct', 'incorrect', 'unsure'));

ALTER TABLE ge.intel_need ADD CONSTRAINT ck_intel_need__revision CHECK (revision >= 1);

ALTER TABLE ge.intel_need ADD CONSTRAINT ck_intel_need__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.intel_need ADD CONSTRAINT ck_intel_need__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.intel_need ADD CONSTRAINT ck_intel_need__derivation CHECK (derivation IN ('explicit', 'inferred'));

ALTER TABLE ge.intel_need ADD CONSTRAINT ck_intel_need__state CHECK (state IN ('proposed', 'in_review', 'confirmed', 'rejected', 'expired'));

ALTER TABLE ge.intel_need_evidence ADD CONSTRAINT ck_intel_need_evidence__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.intel_match ADD CONSTRAINT ck_intel_match__revision CHECK (revision >= 1);

ALTER TABLE ge.intel_match ADD CONSTRAINT ck_intel_match__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.intel_match ADD CONSTRAINT ck_intel_match__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.intel_scoring_model ADD CONSTRAINT ck_intel_scoring_model__revision CHECK (revision >= 1);

ALTER TABLE ge.intel_scoring_model ADD CONSTRAINT ck_intel_scoring_model__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.intel_scoring_model ADD CONSTRAINT ck_intel_scoring_model__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.intel_scoring_model ADD CONSTRAINT ck_intel_scoring_model__version_no CHECK (version_no >= 1);

ALTER TABLE ge.intel_scoring_model ADD CONSTRAINT ck_intel_scoring_model__content_hash CHECK (content_hash ~ '^[0-9a-f]{64}$');

ALTER TABLE ge.intel_opportunity ADD CONSTRAINT ck_intel_opportunity__revision CHECK (revision >= 1);

ALTER TABLE ge.intel_opportunity ADD CONSTRAINT ck_intel_opportunity__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.intel_opportunity ADD CONSTRAINT ck_intel_opportunity__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.intel_opportunity ADD CONSTRAINT ck_intel_opportunity__opportunity_type CHECK (opportunity_type IN ('project_bid', 'healthcare_pilot', 'education_enrolment', 'product_purchase', 'product_sale', 'service', 'training', 'licensing'));

ALTER TABLE ge.intel_opportunity ADD CONSTRAINT ck_intel_opportunity__state CHECK (state IN ('discovered', 'scored', 'unknown', 'priority_review', 'nurture', 'archived', 'qualified', 'rejected', 'deal_created', 'stale'));

ALTER TABLE ge.intel_opportunity ADD CONSTRAINT ck_intel_opportunity__current_score CHECK (current_score BETWEEN 0 AND 100);

ALTER TABLE ge.intel_opportunity ADD CONSTRAINT ck_intel_opportunity__band CHECK (band IN ('priority', 'research_nurture', 'archive_review', 'unknown'));

ALTER TABLE ge.intel_score_version ADD CONSTRAINT ck_intel_score_version__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.intel_score_version ADD CONSTRAINT ck_intel_score_version__known_weight CHECK (known_weight BETWEEN 0 AND 1);

ALTER TABLE ge.intel_score_version ADD CONSTRAINT ck_intel_score_version__score CHECK (score BETWEEN 0 AND 100);

ALTER TABLE ge.intel_score_version ADD CONSTRAINT ck_intel_score_version__trigger_reason CHECK (trigger_reason IN ('new_evidence', 'evidence_expiry', 'offering_change', 'model_change', 'manual'));

ALTER TABLE ge.intel_contact ADD CONSTRAINT ck_intel_contact__revision CHECK (revision >= 1);

ALTER TABLE ge.intel_contact ADD CONSTRAINT ck_intel_contact__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.intel_contact ADD CONSTRAINT ck_intel_contact__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.intel_contact ADD CONSTRAINT ck_intel_contact__person_type CHECK (person_type IN ('professional', 'guardian', 'learner', 'individual_customer', 'supplier_rep'));

ALTER TABLE ge.intel_contact ADD CONSTRAINT ck_intel_contact__age_band CHECK (age_band IN ('adult_assumed', 'adult_verified', 'under_18', 'unknown'));

ALTER TABLE ge.intel_contact ADD CONSTRAINT ck_intel_contact__verification_state CHECK (verification_state IN ('unverified', 'verifying', 'verified', 'stale', 'failed'));

ALTER TABLE ge.intel_contact ADD CONSTRAINT ck_intel_contact__eligibility_basis CHECK (eligibility_basis IN ('none', 'import_unverified', 'consent', 'legitimate_interest', 'contract', 'guardian_consent'));

ALTER TABLE ge.intel_role_hypothesis ADD CONSTRAINT ck_intel_role_hypothesis__revision CHECK (revision >= 1);

ALTER TABLE ge.intel_role_hypothesis ADD CONSTRAINT ck_intel_role_hypothesis__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.intel_role_hypothesis ADD CONSTRAINT ck_intel_role_hypothesis__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.intel_contact_source ADD CONSTRAINT ck_intel_contact_source__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.intel_contact_verification ADD CONSTRAINT ck_intel_contact_verification__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.intel_review ADD CONSTRAINT ck_intel_review__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.crm_lead ADD CONSTRAINT ck_crm_lead__revision CHECK (revision >= 1);

ALTER TABLE ge.crm_lead ADD CONSTRAINT ck_crm_lead__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.crm_lead ADD CONSTRAINT ck_crm_lead__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.crm_lead ADD CONSTRAINT ck_crm_lead__source_channel CHECK (source_channel IN ('web_form', 'portal', 'chat', 'referral', 'event', 'import', 'inbound_email', 'inbound_whatsapp'));

ALTER TABLE ge.crm_lead ADD CONSTRAINT ck_crm_lead__state CHECK (state IN ('received', 'duplicate', 'screening', 'disqualified', 'routed', 'accepted', 'rejected', 'converted_to_opportunity', 'nurture'));

ALTER TABLE ge.crm_form ADD CONSTRAINT ck_crm_form__revision CHECK (revision >= 1);

ALTER TABLE ge.crm_form ADD CONSTRAINT ck_crm_form__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.crm_form ADD CONSTRAINT ck_crm_form__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.crm_form_version ADD CONSTRAINT ck_crm_form_version__revision CHECK (revision >= 1);

ALTER TABLE ge.crm_form_version ADD CONSTRAINT ck_crm_form_version__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.crm_form_version ADD CONSTRAINT ck_crm_form_version__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.crm_form_version ADD CONSTRAINT ck_crm_form_version__version_no CHECK (version_no >= 1);

ALTER TABLE ge.crm_form_version ADD CONSTRAINT ck_crm_form_version__content_hash CHECK (content_hash ~ '^[0-9a-f]{64}$');

ALTER TABLE ge.crm_submission ADD CONSTRAINT ck_crm_submission__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.crm_pipeline ADD CONSTRAINT ck_crm_pipeline__revision CHECK (revision >= 1);

ALTER TABLE ge.crm_pipeline ADD CONSTRAINT ck_crm_pipeline__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.crm_pipeline ADD CONSTRAINT ck_crm_pipeline__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.crm_pipeline ADD CONSTRAINT ck_crm_pipeline__version_no CHECK (version_no >= 1);

ALTER TABLE ge.crm_pipeline ADD CONSTRAINT ck_crm_pipeline__content_hash CHECK (content_hash ~ '^[0-9a-f]{64}$');

ALTER TABLE ge.crm_stage ADD CONSTRAINT ck_crm_stage__revision CHECK (revision >= 1);

ALTER TABLE ge.crm_stage ADD CONSTRAINT ck_crm_stage__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.crm_stage ADD CONSTRAINT ck_crm_stage__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.crm_stage ADD CONSTRAINT ck_crm_stage__version_no CHECK (version_no >= 1);

ALTER TABLE ge.crm_stage ADD CONSTRAINT ck_crm_stage__content_hash CHECK (content_hash ~ '^[0-9a-f]{64}$');

ALTER TABLE ge.crm_closure_policy ADD CONSTRAINT ck_crm_closure_policy__revision CHECK (revision >= 1);

ALTER TABLE ge.crm_closure_policy ADD CONSTRAINT ck_crm_closure_policy__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.crm_closure_policy ADD CONSTRAINT ck_crm_closure_policy__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.crm_closure_policy ADD CONSTRAINT ck_crm_closure_policy__version_no CHECK (version_no >= 1);

ALTER TABLE ge.crm_closure_policy ADD CONSTRAINT ck_crm_closure_policy__content_hash CHECK (content_hash ~ '^[0-9a-f]{64}$');

ALTER TABLE ge.crm_deal ADD CONSTRAINT ck_crm_deal__revision CHECK (revision >= 1);

ALTER TABLE ge.crm_deal ADD CONSTRAINT ck_crm_deal__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.crm_deal ADD CONSTRAINT ck_crm_deal__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.crm_deal ADD CONSTRAINT ck_crm_deal__expected_value CHECK (expected_value >= 0);

ALTER TABLE ge.crm_deal ADD CONSTRAINT ck_crm_deal__closure_status CHECK (closure_status IN ('open', 'won_contracted', 'paid', 'lost', 'on_hold'));

ALTER TABLE ge.crm_stage_transition ADD CONSTRAINT ck_crm_stage_transition__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.crm_activity ADD CONSTRAINT ck_crm_activity__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.crm_activity ADD CONSTRAINT ck_crm_activity__activity_type CHECK (activity_type IN ('note', 'call', 'email_out', 'email_in', 'whatsapp_out', 'whatsapp_in', 'meeting', 'task', 'stage_change', 'document', 'payment', 'system'));

ALTER TABLE ge.crm_activity ADD CONSTRAINT ck_crm_activity__visibility CHECK (visibility IN ('owner', 'team', 'startup'));

ALTER TABLE ge.eng_message_template ADD CONSTRAINT ck_eng_message_template__revision CHECK (revision >= 1);

ALTER TABLE ge.eng_message_template ADD CONSTRAINT ck_eng_message_template__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.eng_message_template ADD CONSTRAINT ck_eng_message_template__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.eng_message_template ADD CONSTRAINT ck_eng_message_template__version_no CHECK (version_no >= 1);

ALTER TABLE ge.eng_message_template ADD CONSTRAINT ck_eng_message_template__content_hash CHECK (content_hash ~ '^[0-9a-f]{64}$');

ALTER TABLE ge.eng_message_draft ADD CONSTRAINT ck_eng_message_draft__revision CHECK (revision >= 1);

ALTER TABLE ge.eng_message_draft ADD CONSTRAINT ck_eng_message_draft__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.eng_message_draft ADD CONSTRAINT ck_eng_message_draft__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.eng_thread ADD CONSTRAINT ck_eng_thread__revision CHECK (revision >= 1);

ALTER TABLE ge.eng_thread ADD CONSTRAINT ck_eng_thread__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.eng_thread ADD CONSTRAINT ck_eng_thread__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.eng_thread ADD CONSTRAINT ck_eng_thread__primary_channel CHECK (primary_channel IN ('email', 'whatsapp', 'web_chat', 'portal'));

ALTER TABLE ge.eng_thread ADD CONSTRAINT ck_eng_thread__state CHECK (state IN ('open', 'awaiting_reply', 'handed_off', 'closed'));

ALTER TABLE ge.eng_message ADD CONSTRAINT ck_eng_message__revision CHECK (revision >= 1);

ALTER TABLE ge.eng_message ADD CONSTRAINT ck_eng_message__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.eng_message ADD CONSTRAINT ck_eng_message__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.eng_message ADD CONSTRAINT ck_eng_message__direction CHECK (direction IN ('outbound', 'inbound'));

ALTER TABLE ge.eng_message ADD CONSTRAINT ck_eng_message__state CHECK (state IN ('drafted', 'policy_checked', 'blocked', 'awaiting_approval', 'queued', 'rejected', 'cancelled', 'simulated', 'sending', 'sent', 'uncertain', 'failed', 'delivered', 'bounced', 'read', 'complained'));

ALTER TABLE ge.eng_message ADD CONSTRAINT ck_eng_message__outcome_certainty CHECK (outcome_certainty IN ('confirmed', 'uncertain', 'failed', 'reconciled_confirmed', 'reconciled_failed'));

ALTER TABLE ge.eng_delivery_event ADD CONSTRAINT ck_eng_delivery_event__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.eng_delivery_event ADD CONSTRAINT ck_eng_delivery_event__event_type CHECK (event_type IN ('accepted', 'delivered', 'opened', 'read', 'clicked', 'bounced_hard', 'bounced_soft', 'complained', 'failed', 'unsubscribed'));

ALTER TABLE ge.eng_inbound_event ADD CONSTRAINT ck_eng_inbound_event__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.eng_intent ADD CONSTRAINT ck_eng_intent__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.eng_identity_link ADD CONSTRAINT ck_eng_identity_link__revision CHECK (revision >= 1);

ALTER TABLE ge.eng_identity_link ADD CONSTRAINT ck_eng_identity_link__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.eng_identity_link ADD CONSTRAINT ck_eng_identity_link__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.eng_routing_rule ADD CONSTRAINT ck_eng_routing_rule__revision CHECK (revision >= 1);

ALTER TABLE ge.eng_routing_rule ADD CONSTRAINT ck_eng_routing_rule__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.eng_routing_rule ADD CONSTRAINT ck_eng_routing_rule__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.eng_routing_rule ADD CONSTRAINT ck_eng_routing_rule__version_no CHECK (version_no >= 1);

ALTER TABLE ge.eng_routing_rule ADD CONSTRAINT ck_eng_routing_rule__content_hash CHECK (content_hash ~ '^[0-9a-f]{64}$');

ALTER TABLE ge.eng_chat_session ADD CONSTRAINT ck_eng_chat_session__revision CHECK (revision >= 1);

ALTER TABLE ge.eng_chat_session ADD CONSTRAINT ck_eng_chat_session__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.eng_chat_session ADD CONSTRAINT ck_eng_chat_session__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.eng_sequence ADD CONSTRAINT ck_eng_sequence__revision CHECK (revision >= 1);

ALTER TABLE ge.eng_sequence ADD CONSTRAINT ck_eng_sequence__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.eng_sequence ADD CONSTRAINT ck_eng_sequence__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.eng_sequence ADD CONSTRAINT ck_eng_sequence__version_no CHECK (version_no >= 1);

ALTER TABLE ge.eng_sequence ADD CONSTRAINT ck_eng_sequence__content_hash CHECK (content_hash ~ '^[0-9a-f]{64}$');

ALTER TABLE ge.eng_sequence ADD CONSTRAINT ck_eng_sequence__purpose CHECK (purpose IN ('generic_outreach', 'follow_up', 'onboarding', 'renewal', 'event_reminder'));

ALTER TABLE ge.eng_sequence ADD CONSTRAINT ck_eng_sequence__max_attempts CHECK (max_attempts BETWEEN 1 AND 10);

ALTER TABLE ge.eng_sequence ADD CONSTRAINT ck_eng_sequence__min_interval_business_days CHECK (min_interval_business_days >= 2);

ALTER TABLE ge.eng_sequence_step ADD CONSTRAINT ck_eng_sequence_step__revision CHECK (revision >= 1);

ALTER TABLE ge.eng_sequence_step ADD CONSTRAINT ck_eng_sequence_step__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.eng_sequence_step ADD CONSTRAINT ck_eng_sequence_step__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.eng_sequence_step ADD CONSTRAINT ck_eng_sequence_step__version_no CHECK (version_no >= 1);

ALTER TABLE ge.eng_sequence_step ADD CONSTRAINT ck_eng_sequence_step__content_hash CHECK (content_hash ~ '^[0-9a-f]{64}$');

ALTER TABLE ge.eng_enrollment ADD CONSTRAINT ck_eng_enrollment__revision CHECK (revision >= 1);

ALTER TABLE ge.eng_enrollment ADD CONSTRAINT ck_eng_enrollment__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.eng_enrollment ADD CONSTRAINT ck_eng_enrollment__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.eng_enrollment ADD CONSTRAINT ck_eng_enrollment__state CHECK (state IN ('enrolled', 'active', 'waiting', 'paused', 'stopped', 'completed'));

ALTER TABLE ge.eng_meeting ADD CONSTRAINT ck_eng_meeting__revision CHECK (revision >= 1);

ALTER TABLE ge.eng_meeting ADD CONSTRAINT ck_eng_meeting__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.eng_meeting ADD CONSTRAINT ck_eng_meeting__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.eng_meeting ADD CONSTRAINT ck_eng_meeting__state CHECK (state IN ('slots_offered', 'held', 'confirmed', 'expired', 'rescheduled', 'cancelled', 'completed', 'no_show'));

ALTER TABLE ge.eng_meeting ADD CONSTRAINT ck_eng_meeting__attendance_evidence CHECK (attendance_evidence IN ('owner_confirmed', 'provider_attendance'));

ALTER TABLE ge.eng_calendar_link ADD CONSTRAINT ck_eng_calendar_link__revision CHECK (revision >= 1);

ALTER TABLE ge.eng_calendar_link ADD CONSTRAINT ck_eng_calendar_link__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.eng_calendar_link ADD CONSTRAINT ck_eng_calendar_link__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.mkt_content_asset ADD CONSTRAINT ck_mkt_content_asset__revision CHECK (revision >= 1);

ALTER TABLE ge.mkt_content_asset ADD CONSTRAINT ck_mkt_content_asset__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.mkt_content_asset ADD CONSTRAINT ck_mkt_content_asset__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.mkt_content_version ADD CONSTRAINT ck_mkt_content_version__revision CHECK (revision >= 1);

ALTER TABLE ge.mkt_content_version ADD CONSTRAINT ck_mkt_content_version__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.mkt_content_version ADD CONSTRAINT ck_mkt_content_version__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.mkt_content_version ADD CONSTRAINT ck_mkt_content_version__version_no CHECK (version_no >= 1);

ALTER TABLE ge.mkt_content_version ADD CONSTRAINT ck_mkt_content_version__content_hash CHECK (content_hash ~ '^[0-9a-f]{64}$');

ALTER TABLE ge.mkt_content_version ADD CONSTRAINT ck_mkt_content_version__accessibility_result CHECK (accessibility_result IN ('pass', 'fail', 'waived'));

ALTER TABLE ge.mkt_social_publication ADD CONSTRAINT ck_mkt_social_publication__revision CHECK (revision >= 1);

ALTER TABLE ge.mkt_social_publication ADD CONSTRAINT ck_mkt_social_publication__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.mkt_social_publication ADD CONSTRAINT ck_mkt_social_publication__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.mkt_keyword ADD CONSTRAINT ck_mkt_keyword__revision CHECK (revision >= 1);

ALTER TABLE ge.mkt_keyword ADD CONSTRAINT ck_mkt_keyword__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.mkt_keyword ADD CONSTRAINT ck_mkt_keyword__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.mkt_seo_issue ADD CONSTRAINT ck_mkt_seo_issue__revision CHECK (revision >= 1);

ALTER TABLE ge.mkt_seo_issue ADD CONSTRAINT ck_mkt_seo_issue__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.mkt_seo_issue ADD CONSTRAINT ck_mkt_seo_issue__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.mkt_page_metric ADD CONSTRAINT ck_mkt_page_metric__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.mkt_landing_page ADD CONSTRAINT ck_mkt_landing_page__revision CHECK (revision >= 1);

ALTER TABLE ge.mkt_landing_page ADD CONSTRAINT ck_mkt_landing_page__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.mkt_landing_page ADD CONSTRAINT ck_mkt_landing_page__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.mkt_publication ADD CONSTRAINT ck_mkt_publication__revision CHECK (revision >= 1);

ALTER TABLE ge.mkt_publication ADD CONSTRAINT ck_mkt_publication__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.mkt_publication ADD CONSTRAINT ck_mkt_publication__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.mkt_publication ADD CONSTRAINT ck_mkt_publication__target_kind CHECK (target_kind IN ('site_page', 'landing_page', 'faq_set', 'public_asset'));

ALTER TABLE ge.mkt_publication ADD CONSTRAINT ck_mkt_publication__path CHECK (path ~ '^/[a-z0-9/_-]*$');

ALTER TABLE ge.mkt_publication ADD CONSTRAINT ck_mkt_publication__state CHECK (state IN ('draft', 'published', 'rolled_back', 'retired'));

ALTER TABLE ge.mkt_publication_snapshot ADD CONSTRAINT ck_mkt_publication_snapshot__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.mkt_preview_grant ADD CONSTRAINT ck_mkt_preview_grant__revision CHECK (revision >= 1);

ALTER TABLE ge.mkt_preview_grant ADD CONSTRAINT ck_mkt_preview_grant__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.mkt_preview_grant ADD CONSTRAINT ck_mkt_preview_grant__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.mkt_campaign ADD CONSTRAINT ck_mkt_campaign__revision CHECK (revision >= 1);

ALTER TABLE ge.mkt_campaign ADD CONSTRAINT ck_mkt_campaign__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.mkt_campaign ADD CONSTRAINT ck_mkt_campaign__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.mkt_campaign ADD CONSTRAINT ck_mkt_campaign__state CHECK (state IN ('draft', 'simulated', 'pending_approval', 'approved', 'running', 'paused', 'completed', 'cancelled'));

ALTER TABLE ge.mkt_campaign ADD CONSTRAINT ck_mkt_campaign__attribution_window_days CHECK (attribution_window_days BETWEEN 1 AND 365);

ALTER TABLE ge.mkt_campaign_version ADD CONSTRAINT ck_mkt_campaign_version__revision CHECK (revision >= 1);

ALTER TABLE ge.mkt_campaign_version ADD CONSTRAINT ck_mkt_campaign_version__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.mkt_campaign_version ADD CONSTRAINT ck_mkt_campaign_version__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.mkt_campaign_version ADD CONSTRAINT ck_mkt_campaign_version__version_no CHECK (version_no >= 1);

ALTER TABLE ge.mkt_campaign_version ADD CONSTRAINT ck_mkt_campaign_version__content_hash CHECK (content_hash ~ '^[0-9a-f]{64}$');

ALTER TABLE ge.mkt_audience ADD CONSTRAINT ck_mkt_audience__revision CHECK (revision >= 1);

ALTER TABLE ge.mkt_audience ADD CONSTRAINT ck_mkt_audience__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.mkt_audience ADD CONSTRAINT ck_mkt_audience__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.mkt_audience ADD CONSTRAINT ck_mkt_audience__version_no CHECK (version_no >= 1);

ALTER TABLE ge.mkt_audience ADD CONSTRAINT ck_mkt_audience__content_hash CHECK (content_hash ~ '^[0-9a-f]{64}$');

ALTER TABLE ge.mkt_ad_campaign ADD CONSTRAINT ck_mkt_ad_campaign__revision CHECK (revision >= 1);

ALTER TABLE ge.mkt_ad_campaign ADD CONSTRAINT ck_mkt_ad_campaign__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.mkt_ad_campaign ADD CONSTRAINT ck_mkt_ad_campaign__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.mkt_spend_event ADD CONSTRAINT ck_mkt_spend_event__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.mkt_event ADD CONSTRAINT ck_mkt_event__revision CHECK (revision >= 1);

ALTER TABLE ge.mkt_event ADD CONSTRAINT ck_mkt_event__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.mkt_event ADD CONSTRAINT ck_mkt_event__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.mkt_registration ADD CONSTRAINT ck_mkt_registration__revision CHECK (revision >= 1);

ALTER TABLE ge.mkt_registration ADD CONSTRAINT ck_mkt_registration__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.mkt_registration ADD CONSTRAINT ck_mkt_registration__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.mkt_attendance ADD CONSTRAINT ck_mkt_attendance__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.mkt_referral ADD CONSTRAINT ck_mkt_referral__revision CHECK (revision >= 1);

ALTER TABLE ge.mkt_referral ADD CONSTRAINT ck_mkt_referral__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.mkt_referral ADD CONSTRAINT ck_mkt_referral__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.mkt_attribution_event ADD CONSTRAINT ck_mkt_attribution_event__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.com_proposal ADD CONSTRAINT ck_com_proposal__revision CHECK (revision >= 1);

ALTER TABLE ge.com_proposal ADD CONSTRAINT ck_com_proposal__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.com_proposal ADD CONSTRAINT ck_com_proposal__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.com_proposal ADD CONSTRAINT ck_com_proposal__state CHECK (state IN ('draft', 'validating', 'pending_approval', 'approved', 'sent', 'viewed', 'accepted', 'change_requested', 'expired', 'superseded', 'withdrawn'));

ALTER TABLE ge.com_proposal_version ADD CONSTRAINT ck_com_proposal_version__revision CHECK (revision >= 1);

ALTER TABLE ge.com_proposal_version ADD CONSTRAINT ck_com_proposal_version__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.com_proposal_version ADD CONSTRAINT ck_com_proposal_version__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.com_proposal_version ADD CONSTRAINT ck_com_proposal_version__version_no CHECK (version_no >= 1);

ALTER TABLE ge.com_proposal_version ADD CONSTRAINT ck_com_proposal_version__content_hash CHECK (content_hash ~ '^[0-9a-f]{64}$');

ALTER TABLE ge.com_quote ADD CONSTRAINT ck_com_quote__revision CHECK (revision >= 1);

ALTER TABLE ge.com_quote ADD CONSTRAINT ck_com_quote__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.com_quote ADD CONSTRAINT ck_com_quote__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.com_quote ADD CONSTRAINT ck_com_quote__discount_amount CHECK (discount_amount >= 0);

ALTER TABLE ge.com_quote ADD CONSTRAINT ck_com_quote__tax_regime CHECK (tax_regime IN ('intra_state', 'inter_state', 'export_lut', 'not_applicable'));

ALTER TABLE ge.com_quote ADD CONSTRAINT ck_com_quote__state CHECK (state IN ('draft', 'validating', 'pending_approval', 'approved', 'sent', 'viewed', 'accepted', 'change_requested', 'expired', 'superseded', 'withdrawn'));

ALTER TABLE ge.com_quote_line ADD CONSTRAINT ck_com_quote_line__revision CHECK (revision >= 1);

ALTER TABLE ge.com_quote_line ADD CONSTRAINT ck_com_quote_line__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.com_quote_line ADD CONSTRAINT ck_com_quote_line__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.com_quote_line ADD CONSTRAINT ck_com_quote_line__line_no CHECK (line_no >= 1);

ALTER TABLE ge.com_quote_line ADD CONSTRAINT ck_com_quote_line__quantity CHECK (quantity > 0);

ALTER TABLE ge.com_quote_line ADD CONSTRAINT ck_com_quote_line__tax_rate_pct CHECK (tax_rate_pct BETWEEN 0 AND 100);

ALTER TABLE ge.com_objection ADD CONSTRAINT ck_com_objection__revision CHECK (revision >= 1);

ALTER TABLE ge.com_objection ADD CONSTRAINT ck_com_objection__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.com_objection ADD CONSTRAINT ck_com_objection__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.com_negotiation ADD CONSTRAINT ck_com_negotiation__revision CHECK (revision >= 1);

ALTER TABLE ge.com_negotiation ADD CONSTRAINT ck_com_negotiation__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.com_negotiation ADD CONSTRAINT ck_com_negotiation__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.com_contract ADD CONSTRAINT ck_com_contract__revision CHECK (revision >= 1);

ALTER TABLE ge.com_contract ADD CONSTRAINT ck_com_contract__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.com_contract ADD CONSTRAINT ck_com_contract__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.com_contract ADD CONSTRAINT ck_com_contract__contract_kind CHECK (contract_kind IN ('msa', 'sow', 'mou', 'licence', 'pilot_agreement', 'purchase_agreement', 'nda'));

ALTER TABLE ge.com_contract ADD CONSTRAINT ck_com_contract__contract_value CHECK (contract_value >= 0);

ALTER TABLE ge.com_contract ADD CONSTRAINT ck_com_contract__state CHECK (state IN ('drafting', 'legal_review', 'legally_approved', 'out_for_signature', 'partially_signed', 'executed', 'declined', 'expired', 'active', 'renewal_due', 'renewed', 'terminated'));

ALTER TABLE ge.com_contract ADD CONSTRAINT ck_com_contract__esign_provider CHECK (esign_provider IN ('signed_pdf_upload', 'leegality', 'digio', 'zoho_sign', 'docusign'));

ALTER TABLE ge.com_signature_event ADD CONSTRAINT ck_com_signature_event__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.com_signature_event ADD CONSTRAINT ck_com_signature_event__party_side CHECK (party_side IN ('startup', 'counterparty'));

ALTER TABLE ge.com_signature_event ADD CONSTRAINT ck_com_signature_event__method CHECK (method IN ('signed_pdf_upload', 'aadhaar_esign', 'dsc', 'provider_esign'));

ALTER TABLE ge.com_bid ADD CONSTRAINT ck_com_bid__revision CHECK (revision >= 1);

ALTER TABLE ge.com_bid ADD CONSTRAINT ck_com_bid__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.com_bid ADD CONSTRAINT ck_com_bid__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.com_bid ADD CONSTRAINT ck_com_bid__submission_buffer_hours CHECK (submission_buffer_hours >= 2);

ALTER TABLE ge.com_bid ADD CONSTRAINT ck_com_bid__delivery_model CHECK (delivery_model IN ('remote', 'onsite', 'hybrid'));

ALTER TABLE ge.com_bid ADD CONSTRAINT ck_com_bid__budget_amount CHECK (budget_amount >= 0);

ALTER TABLE ge.com_bid ADD CONSTRAINT ck_com_bid__eligibility_result CHECK (eligibility_result IN ('not_evaluated', 'eligible', 'ineligible', 'waived'));

ALTER TABLE ge.com_bid ADD CONSTRAINT ck_com_bid__state CHECK (state IN ('identified', 'eligibility_check', 'no_bid', 'bid_decision', 'preparing', 'ready_to_submit', 'expired', 'submitted', 'clarification', 'awarded', 'not_awarded', 'withdrawn'));

ALTER TABLE ge.com_bid_checklist_item ADD CONSTRAINT ck_com_bid_checklist_item__revision CHECK (revision >= 1);

ALTER TABLE ge.com_bid_checklist_item ADD CONSTRAINT ck_com_bid_checklist_item__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.com_bid_checklist_item ADD CONSTRAINT ck_com_bid_checklist_item__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.com_order ADD CONSTRAINT ck_com_order__revision CHECK (revision >= 1);

ALTER TABLE ge.com_order ADD CONSTRAINT ck_com_order__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.com_order ADD CONSTRAINT ck_com_order__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.com_order ADD CONSTRAINT ck_com_order__direction CHECK (direction IN ('sell', 'buy'));

ALTER TABLE ge.com_order ADD CONSTRAINT ck_com_order__state CHECK (state IN ('draft', 'pending_approval', 'approved', 'issued', 'acknowledged', 'partially_fulfilled', 'fulfilled', 'accepted', 'disputed', 'partially_accepted', 'ledger_posted', 'closed', 'cancelled'));

ALTER TABLE ge.com_order ADD CONSTRAINT ck_com_order__over_delivery_tolerance_pct CHECK (over_delivery_tolerance_pct BETWEEN 0 AND 2);

ALTER TABLE ge.com_order_line ADD CONSTRAINT ck_com_order_line__revision CHECK (revision >= 1);

ALTER TABLE ge.com_order_line ADD CONSTRAINT ck_com_order_line__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.com_order_line ADD CONSTRAINT ck_com_order_line__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.com_order_line ADD CONSTRAINT ck_com_order_line__quantity CHECK (quantity > 0);

ALTER TABLE ge.com_order_line ADD CONSTRAINT ck_com_order_line__unit_price CHECK (unit_price >= 0);

ALTER TABLE ge.com_fulfillment_event ADD CONSTRAINT ck_com_fulfillment_event__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.com_fulfillment_event ADD CONSTRAINT ck_com_fulfillment_event__event_type CHECK (event_type IN ('dispatched', 'delivered', 'accepted', 'rejected', 'returned', 'service_rendered', 'reversal'));

ALTER TABLE ge.com_fulfillment_event ADD CONSTRAINT ck_com_fulfillment_event__quantity CHECK (quantity > 0);

ALTER TABLE ge.com_sku_availability ADD CONSTRAINT ck_com_sku_availability__revision CHECK (revision >= 1);

ALTER TABLE ge.com_sku_availability ADD CONSTRAINT ck_com_sku_availability__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.com_sku_availability ADD CONSTRAINT ck_com_sku_availability__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.com_inventory_reservation ADD CONSTRAINT ck_com_inventory_reservation__revision CHECK (revision >= 1);

ALTER TABLE ge.com_inventory_reservation ADD CONSTRAINT ck_com_inventory_reservation__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.com_inventory_reservation ADD CONSTRAINT ck_com_inventory_reservation__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.com_invoice ADD CONSTRAINT ck_com_invoice__revision CHECK (revision >= 1);

ALTER TABLE ge.com_invoice ADD CONSTRAINT ck_com_invoice__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.com_invoice ADD CONSTRAINT ck_com_invoice__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.com_invoice ADD CONSTRAINT ck_com_invoice__invoice_kind CHECK (invoice_kind IN ('proforma', 'commercial', 'credit_note'));

ALTER TABLE ge.com_invoice ADD CONSTRAINT ck_com_invoice__state CHECK (state IN ('invoice_draft', 'invoice_approved', 'issued', 'awaiting_payment', 'partially_paid', 'paid', 'cancelled', 'refunded'));

ALTER TABLE ge.com_invoice_line ADD CONSTRAINT ck_com_invoice_line__revision CHECK (revision >= 1);

ALTER TABLE ge.com_invoice_line ADD CONSTRAINT ck_com_invoice_line__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.com_invoice_line ADD CONSTRAINT ck_com_invoice_line__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.com_payment ADD CONSTRAINT ck_com_payment__revision CHECK (revision >= 1);

ALTER TABLE ge.com_payment ADD CONSTRAINT ck_com_payment__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.com_payment ADD CONSTRAINT ck_com_payment__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.com_payment ADD CONSTRAINT ck_com_payment__direction CHECK (direction IN ('inbound', 'outbound_record'));

ALTER TABLE ge.com_payment ADD CONSTRAINT ck_com_payment__method CHECK (method IN ('bank_transfer', 'upi', 'gateway_link', 'cheque', 'other'));

ALTER TABLE ge.com_payment ADD CONSTRAINT ck_com_payment__amount CHECK (amount > 0);

ALTER TABLE ge.com_payment ADD CONSTRAINT ck_com_payment__state CHECK (state IN ('evidence_received', 'duplicate', 'maker_verified', 'discrepancy', 'rejected', 'checker_verified', 'refunded'));

ALTER TABLE ge.com_payment_allocation ADD CONSTRAINT ck_com_payment_allocation__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.com_discrepancy_case ADD CONSTRAINT ck_com_discrepancy_case__revision CHECK (revision >= 1);

ALTER TABLE ge.com_discrepancy_case ADD CONSTRAINT ck_com_discrepancy_case__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.com_discrepancy_case ADD CONSTRAINT ck_com_discrepancy_case__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.com_receivable_entry ADD CONSTRAINT ck_com_receivable_entry__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.com_receivable_entry ADD CONSTRAINT ck_com_receivable_entry__entry_type CHECK (entry_type IN ('invoice_posted', 'payment_applied', 'credit_note', 'write_off', 'reversal'));

ALTER TABLE ge.com_payable_entry ADD CONSTRAINT ck_com_payable_entry__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.com_payable_entry ADD CONSTRAINT ck_com_payable_entry__entry_type CHECK (entry_type IN ('invoice_posted', 'payment_applied', 'credit_note', 'write_off', 'reversal'));

ALTER TABLE ge.lcy_onboarding ADD CONSTRAINT ck_lcy_onboarding__revision CHECK (revision >= 1);

ALTER TABLE ge.lcy_onboarding ADD CONSTRAINT ck_lcy_onboarding__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.lcy_onboarding ADD CONSTRAINT ck_lcy_onboarding__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.lcy_task ADD CONSTRAINT ck_lcy_task__revision CHECK (revision >= 1);

ALTER TABLE ge.lcy_task ADD CONSTRAINT ck_lcy_task__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.lcy_task ADD CONSTRAINT ck_lcy_task__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.lcy_handoff ADD CONSTRAINT ck_lcy_handoff__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.lcy_renewal ADD CONSTRAINT ck_lcy_renewal__revision CHECK (revision >= 1);

ALTER TABLE ge.lcy_renewal ADD CONSTRAINT ck_lcy_renewal__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.lcy_renewal ADD CONSTRAINT ck_lcy_renewal__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.lcy_customer_subscription ADD CONSTRAINT ck_lcy_customer_subscription__revision CHECK (revision >= 1);

ALTER TABLE ge.lcy_customer_subscription ADD CONSTRAINT ck_lcy_customer_subscription__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.lcy_customer_subscription ADD CONSTRAINT ck_lcy_customer_subscription__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.lcy_account_metric ADD CONSTRAINT ck_lcy_account_metric__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.lcy_partner ADD CONSTRAINT ck_lcy_partner__revision CHECK (revision >= 1);

ALTER TABLE ge.lcy_partner ADD CONSTRAINT ck_lcy_partner__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.lcy_partner ADD CONSTRAINT ck_lcy_partner__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.lcy_pilot ADD CONSTRAINT ck_lcy_pilot__revision CHECK (revision >= 1);

ALTER TABLE ge.lcy_pilot ADD CONSTRAINT ck_lcy_pilot__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.lcy_pilot ADD CONSTRAINT ck_lcy_pilot__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.lcy_deployment ADD CONSTRAINT ck_lcy_deployment__revision CHECK (revision >= 1);

ALTER TABLE ge.lcy_deployment ADD CONSTRAINT ck_lcy_deployment__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.lcy_deployment ADD CONSTRAINT ck_lcy_deployment__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.lcy_integration_deal ADD CONSTRAINT ck_lcy_integration_deal__revision CHECK (revision >= 1);

ALTER TABLE ge.lcy_integration_deal ADD CONSTRAINT ck_lcy_integration_deal__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.lcy_integration_deal ADD CONSTRAINT ck_lcy_integration_deal__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.lcy_feedback ADD CONSTRAINT ck_lcy_feedback__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.lcy_outcome ADD CONSTRAINT ck_lcy_outcome__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.aut_workflow ADD CONSTRAINT ck_aut_workflow__revision CHECK (revision >= 1);

ALTER TABLE ge.aut_workflow ADD CONSTRAINT ck_aut_workflow__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.aut_workflow ADD CONSTRAINT ck_aut_workflow__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.aut_workflow ADD CONSTRAINT ck_aut_workflow__autonomy_mode CHECK (autonomy_mode IN ('L0', 'L1', 'L2', 'L3'));

ALTER TABLE ge.aut_workflow ADD CONSTRAINT ck_aut_workflow__max_concurrent_runs CHECK (max_concurrent_runs BETWEEN 1 AND 20);

ALTER TABLE ge.aut_workflow_revision ADD CONSTRAINT ck_aut_workflow_revision__revision CHECK (revision >= 1);

ALTER TABLE ge.aut_workflow_revision ADD CONSTRAINT ck_aut_workflow_revision__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.aut_workflow_revision ADD CONSTRAINT ck_aut_workflow_revision__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.aut_workflow_revision ADD CONSTRAINT ck_aut_workflow_revision__version_no CHECK (version_no >= 1);

ALTER TABLE ge.aut_workflow_revision ADD CONSTRAINT ck_aut_workflow_revision__content_hash CHECK (content_hash ~ '^[0-9a-f]{64}$');

ALTER TABLE ge.aut_trigger ADD CONSTRAINT ck_aut_trigger__revision CHECK (revision >= 1);

ALTER TABLE ge.aut_trigger ADD CONSTRAINT ck_aut_trigger__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.aut_trigger ADD CONSTRAINT ck_aut_trigger__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.aut_trigger ADD CONSTRAINT ck_aut_trigger__trigger_kind CHECK (trigger_kind IN ('domain_event', 'schedule', 'webhook', 'manual'));

ALTER TABLE ge.aut_trigger ADD CONSTRAINT ck_aut_trigger__dedup_window_s CHECK (dedup_window_s BETWEEN 0 AND 86400);

ALTER TABLE ge.aut_trigger ADD CONSTRAINT ck_aut_trigger__state CHECK (state IN ('draft', 'tested', 'enabled', 'paused', 'retired'));

ALTER TABLE ge.aut_autonomy_plan ADD CONSTRAINT ck_aut_autonomy_plan__revision CHECK (revision >= 1);

ALTER TABLE ge.aut_autonomy_plan ADD CONSTRAINT ck_aut_autonomy_plan__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.aut_autonomy_plan ADD CONSTRAINT ck_aut_autonomy_plan__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.aut_conflict_case ADD CONSTRAINT ck_aut_conflict_case__revision CHECK (revision >= 1);

ALTER TABLE ge.aut_conflict_case ADD CONSTRAINT ck_aut_conflict_case__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.aut_conflict_case ADD CONSTRAINT ck_aut_conflict_case__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.aut_node_template ADD CONSTRAINT ck_aut_node_template__revision CHECK (revision >= 1);

ALTER TABLE ge.aut_node_template ADD CONSTRAINT ck_aut_node_template__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.aut_node_template ADD CONSTRAINT ck_aut_node_template__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.aut_node_template ADD CONSTRAINT ck_aut_node_template__version_no CHECK (version_no >= 1);

ALTER TABLE ge.aut_node_template ADD CONSTRAINT ck_aut_node_template__content_hash CHECK (content_hash ~ '^[0-9a-f]{64}$');

ALTER TABLE ge.aut_workflow_template ADD CONSTRAINT ck_aut_workflow_template__revision CHECK (revision >= 1);

ALTER TABLE ge.aut_workflow_template ADD CONSTRAINT ck_aut_workflow_template__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.aut_workflow_template ADD CONSTRAINT ck_aut_workflow_template__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.aut_workflow_template ADD CONSTRAINT ck_aut_workflow_template__version_no CHECK (version_no >= 1);

ALTER TABLE ge.aut_workflow_template ADD CONSTRAINT ck_aut_workflow_template__content_hash CHECK (content_hash ~ '^[0-9a-f]{64}$');

ALTER TABLE ge.aut_config_revision ADD CONSTRAINT ck_aut_config_revision__revision CHECK (revision >= 1);

ALTER TABLE ge.aut_config_revision ADD CONSTRAINT ck_aut_config_revision__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.aut_config_revision ADD CONSTRAINT ck_aut_config_revision__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.aut_config_revision ADD CONSTRAINT ck_aut_config_revision__version_no CHECK (version_no >= 1);

ALTER TABLE ge.aut_config_revision ADD CONSTRAINT ck_aut_config_revision__content_hash CHECK (content_hash ~ '^[0-9a-f]{64}$');

ALTER TABLE ge.aut_config_revision ADD CONSTRAINT ck_aut_config_revision__config_key CHECK (config_key ~ '^CFG-[0-9]{2}(\.[a-z0-9_]+)*$');

ALTER TABLE ge.ops_domain_event ADD CONSTRAINT ck_ops_domain_event__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.ops_idempotency_key ADD CONSTRAINT ck_ops_idempotency_key__revision CHECK (revision >= 1);

ALTER TABLE ge.ops_idempotency_key ADD CONSTRAINT ck_ops_idempotency_key__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.ops_idempotency_key ADD CONSTRAINT ck_ops_idempotency_key__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.ops_job_run ADD CONSTRAINT ck_ops_job_run__revision CHECK (revision >= 1);

ALTER TABLE ge.ops_job_run ADD CONSTRAINT ck_ops_job_run__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.ops_job_run ADD CONSTRAINT ck_ops_job_run__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.ops_notification ADD CONSTRAINT ck_ops_notification__revision CHECK (revision >= 1);

ALTER TABLE ge.ops_notification ADD CONSTRAINT ck_ops_notification__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.ops_notification ADD CONSTRAINT ck_ops_notification__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.ops_notification_preference ADD CONSTRAINT ck_ops_notification_preference__revision CHECK (revision >= 1);

ALTER TABLE ge.ops_notification_preference ADD CONSTRAINT ck_ops_notification_preference__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.ops_notification_preference ADD CONSTRAINT ck_ops_notification_preference__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.ops_release ADD CONSTRAINT ck_ops_release__revision CHECK (revision >= 1);

ALTER TABLE ge.ops_test_run ADD CONSTRAINT ck_ops_test_run__revision CHECK (revision >= 1);

ALTER TABLE ge.saas_plan ADD CONSTRAINT ck_saas_plan__revision CHECK (revision >= 1);

ALTER TABLE ge.saas_plan ADD CONSTRAINT ck_saas_plan__archetype CHECK (archetype IN ('starter', 'growth', 'scale'));

ALTER TABLE ge.saas_plan ADD CONSTRAINT ck_saas_plan__state CHECK (state IN ('draft', 'approved', 'published', 'retired'));

ALTER TABLE ge.saas_plan_version ADD CONSTRAINT ck_saas_plan_version__revision CHECK (revision >= 1);

ALTER TABLE ge.saas_plan_version ADD CONSTRAINT ck_saas_plan_version__version_no CHECK (version_no >= 1);

ALTER TABLE ge.saas_plan_version ADD CONSTRAINT ck_saas_plan_version__content_hash CHECK (content_hash ~ '^[0-9a-f]{64}$');

ALTER TABLE ge.saas_entitlement ADD CONSTRAINT ck_saas_entitlement__revision CHECK (revision >= 1);

ALTER TABLE ge.saas_entitlement ADD CONSTRAINT ck_saas_entitlement__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.saas_entitlement ADD CONSTRAINT ck_saas_entitlement__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.saas_entitlement ADD CONSTRAINT ck_saas_entitlement__version_no CHECK (version_no >= 1);

ALTER TABLE ge.saas_entitlement ADD CONSTRAINT ck_saas_entitlement__content_hash CHECK (content_hash ~ '^[0-9a-f]{64}$');

ALTER TABLE ge.saas_entitlement ADD CONSTRAINT ck_saas_entitlement__meter_code CHECK (meter_code IN ('workspaces', 'users', 'ai_tasks', 'outbound_messages', 'research_fetches', 'storage_gb', 'channel_whatsapp', 'channel_website'));

ALTER TABLE ge.saas_entitlement ADD CONSTRAINT ck_saas_entitlement__included_qty CHECK (included_qty >= 0);

ALTER TABLE ge.saas_entitlement ADD CONSTRAINT ck_saas_entitlement__overage_mode CHECK (overage_mode IN ('block', 'approved_overage'));

ALTER TABLE ge.saas_subscription ADD CONSTRAINT ck_saas_subscription__revision CHECK (revision >= 1);

ALTER TABLE ge.saas_subscription ADD CONSTRAINT ck_saas_subscription__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.saas_subscription ADD CONSTRAINT ck_saas_subscription__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.saas_subscription ADD CONSTRAINT ck_saas_subscription__state CHECK (state IN ('trial', 'active', 'past_due', 'suspended', 'cancelled'));

ALTER TABLE ge.saas_usage_meter_reading ADD CONSTRAINT ck_saas_usage_meter_reading__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.saas_usage_meter_reading ADD CONSTRAINT ck_saas_usage_meter_reading__quantity CHECK (quantity >= 0);

ALTER TABLE ge.saas_service_invoice_line ADD CONSTRAINT ck_saas_service_invoice_line__revision CHECK (revision >= 1);

ALTER TABLE ge.saas_service_invoice_line ADD CONSTRAINT ck_saas_service_invoice_line__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.saas_service_invoice_line ADD CONSTRAINT ck_saas_service_invoice_line__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.saas_credit ADD CONSTRAINT ck_saas_credit__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.saas_application_draft ADD CONSTRAINT ck_saas_application_draft__revision CHECK (revision >= 1);

ALTER TABLE ge.saas_application_draft ADD CONSTRAINT ck_saas_application_draft__state CHECK (state IN ('started', 'submitted', 'verified', 'approved', 'rejected', 'provisioned', 'expired'));

ALTER TABLE ge.saas_support_access_grant ADD CONSTRAINT ck_saas_support_access_grant__revision CHECK (revision >= 1);

ALTER TABLE ge.saas_support_access_grant ADD CONSTRAINT ck_saas_support_access_grant__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.saas_support_access_grant ADD CONSTRAINT ck_saas_support_access_grant__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.saas_support_access_grant ADD CONSTRAINT ck_saas_support_access_grant__access_mode CHECK (access_mode IN ('read_only', 'read_write'));

ALTER TABLE ge.saas_support_access_grant ADD CONSTRAINT ck_saas_support_access_grant__state CHECK (state IN ('requested', 'approved', 'active', 'expired', 'revoked'));

ALTER TABLE ge.saas_import_job ADD CONSTRAINT ck_saas_import_job__revision CHECK (revision >= 1);

ALTER TABLE ge.saas_import_job ADD CONSTRAINT ck_saas_import_job__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.saas_import_job ADD CONSTRAINT ck_saas_import_job__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.ana_metric_definition ADD CONSTRAINT ck_ana_metric_definition__revision CHECK (revision >= 1);

ALTER TABLE ge.ana_metric_definition ADD CONSTRAINT ck_ana_metric_definition__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.ana_metric_definition ADD CONSTRAINT ck_ana_metric_definition__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.ana_metric_definition ADD CONSTRAINT ck_ana_metric_definition__version_no CHECK (version_no >= 1);

ALTER TABLE ge.ana_metric_definition ADD CONSTRAINT ck_ana_metric_definition__content_hash CHECK (content_hash ~ '^[0-9a-f]{64}$');

ALTER TABLE ge.ana_metric_snapshot ADD CONSTRAINT ck_ana_metric_snapshot__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.ana_account_projection ADD CONSTRAINT ck_ana_account_projection__revision CHECK (revision >= 1);

ALTER TABLE ge.ana_account_projection ADD CONSTRAINT ck_ana_account_projection__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.ana_account_projection ADD CONSTRAINT ck_ana_account_projection__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.ana_admin_projection ADD CONSTRAINT ck_ana_admin_projection__revision CHECK (revision >= 1);

ALTER TABLE ge.ana_admin_projection ADD CONSTRAINT ck_ana_admin_projection__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.ana_admin_projection ADD CONSTRAINT ck_ana_admin_projection__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.ana_pipeline_projection ADD CONSTRAINT ck_ana_pipeline_projection__revision CHECK (revision >= 1);

ALTER TABLE ge.ana_pipeline_projection ADD CONSTRAINT ck_ana_pipeline_projection__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.ana_pipeline_projection ADD CONSTRAINT ck_ana_pipeline_projection__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.ana_forecast ADD CONSTRAINT ck_ana_forecast__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.ana_stage_metric ADD CONSTRAINT ck_ana_stage_metric__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.ana_report_subscription ADD CONSTRAINT ck_ana_report_subscription__revision CHECK (revision >= 1);

ALTER TABLE ge.ana_report_subscription ADD CONSTRAINT ck_ana_report_subscription__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.ana_report_subscription ADD CONSTRAINT ck_ana_report_subscription__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.ten_membership_grant ADD CONSTRAINT ck_ten_membership_grant__revision CHECK (revision >= 1);

ALTER TABLE ge.ten_membership_grant ADD CONSTRAINT ck_ten_membership_grant__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.ten_membership_grant ADD CONSTRAINT ck_ten_membership_grant__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.cat_document_offering ADD CONSTRAINT ck_cat_document_offering__revision CHECK (revision >= 1);

ALTER TABLE ge.cat_document_offering ADD CONSTRAINT ck_cat_document_offering__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.cat_document_offering ADD CONSTRAINT ck_cat_document_offering__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.cat_claim_evidence ADD CONSTRAINT ck_cat_claim_evidence__revision CHECK (revision >= 1);

ALTER TABLE ge.cat_claim_evidence ADD CONSTRAINT ck_cat_claim_evidence__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.cat_claim_evidence ADD CONSTRAINT ck_cat_claim_evidence__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.intel_signal_evidence ADD CONSTRAINT ck_intel_signal_evidence__revision CHECK (revision >= 1);

ALTER TABLE ge.intel_signal_evidence ADD CONSTRAINT ck_intel_signal_evidence__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.intel_signal_evidence ADD CONSTRAINT ck_intel_signal_evidence__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.intel_opportunity_contact ADD CONSTRAINT ck_intel_opportunity_contact__revision CHECK (revision >= 1);

ALTER TABLE ge.intel_opportunity_contact ADD CONSTRAINT ck_intel_opportunity_contact__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.intel_opportunity_contact ADD CONSTRAINT ck_intel_opportunity_contact__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.crm_deal_contact ADD CONSTRAINT ck_crm_deal_contact__revision CHECK (revision >= 1);

ALTER TABLE ge.crm_deal_contact ADD CONSTRAINT ck_crm_deal_contact__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.crm_deal_contact ADD CONSTRAINT ck_crm_deal_contact__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.eng_message_claim ADD CONSTRAINT ck_eng_message_claim__revision CHECK (revision >= 1);

ALTER TABLE ge.eng_message_claim ADD CONSTRAINT ck_eng_message_claim__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.eng_message_claim ADD CONSTRAINT ck_eng_message_claim__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.mkt_content_claim ADD CONSTRAINT ck_mkt_content_claim__revision CHECK (revision >= 1);

ALTER TABLE ge.mkt_content_claim ADD CONSTRAINT ck_mkt_content_claim__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.mkt_content_claim ADD CONSTRAINT ck_mkt_content_claim__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.mkt_audience_member ADD CONSTRAINT ck_mkt_audience_member__revision CHECK (revision >= 1);

ALTER TABLE ge.mkt_audience_member ADD CONSTRAINT ck_mkt_audience_member__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.mkt_audience_member ADD CONSTRAINT ck_mkt_audience_member__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.com_contract_party ADD CONSTRAINT ck_com_contract_party__revision CHECK (revision >= 1);

ALTER TABLE ge.com_contract_party ADD CONSTRAINT ck_com_contract_party__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.com_contract_party ADD CONSTRAINT ck_com_contract_party__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.aut_run_conflict ADD CONSTRAINT ck_aut_run_conflict__revision CHECK (revision >= 1);

ALTER TABLE ge.aut_run_conflict ADD CONSTRAINT ck_aut_run_conflict__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.aut_run_conflict ADD CONSTRAINT ck_aut_run_conflict__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.saas_plan_entitlement ADD CONSTRAINT ck_saas_plan_entitlement__revision CHECK (revision >= 1);

ALTER TABLE ge.saas_plan_entitlement ADD CONSTRAINT ck_saas_plan_entitlement__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.saas_plan_entitlement ADD CONSTRAINT ck_saas_plan_entitlement__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.lcy_onboarding_task ADD CONSTRAINT ck_lcy_onboarding_task__revision CHECK (revision >= 1);

ALTER TABLE ge.lcy_onboarding_task ADD CONSTRAINT ck_lcy_onboarding_task__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.lcy_onboarding_task ADD CONSTRAINT ck_lcy_onboarding_task__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.ten_business_template ADD CONSTRAINT ck_ten_business_template__revision CHECK (revision >= 1);

ALTER TABLE ge.ten_business_template ADD CONSTRAINT ck_ten_business_template__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.ten_business_template ADD CONSTRAINT ck_ten_business_template__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.ten_business_template ADD CONSTRAINT ck_ten_business_template__version_no CHECK (version_no >= 1);

ALTER TABLE ge.ten_business_template ADD CONSTRAINT ck_ten_business_template__content_hash CHECK (content_hash ~ '^[0-9a-f]{64}$');

ALTER TABLE ge.ten_business_template ADD CONSTRAINT ck_ten_business_template__template_key CHECK (template_key ~ '^[a-z0-9_]{3,60}$');

ALTER TABLE ge.saas_service_request ADD CONSTRAINT ck_saas_service_request__revision CHECK (revision >= 1);

ALTER TABLE ge.saas_service_request ADD CONSTRAINT ck_saas_service_request__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.saas_service_request ADD CONSTRAINT ck_saas_service_request__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.saas_service_request ADD CONSTRAINT ck_saas_service_request__kind CHECK (kind IN ('billing_question', 'access_request', 'data_export', 'configuration_change', 'incident', 'other'));

ALTER TABLE ge.saas_service_request ADD CONSTRAINT ck_saas_service_request__priority CHECK (priority IN ('low', 'normal', 'high', 'critical'));

ALTER TABLE ge.saas_service_request ADD CONSTRAINT ck_saas_service_request__status CHECK (status IN ('open', 'acknowledged', 'waiting_client', 'resolved', 'closed', 'cancelled'));

ALTER TABLE ge.com_fulfillment_milestone ADD CONSTRAINT ck_com_fulfillment_milestone__revision CHECK (revision >= 1);

ALTER TABLE ge.com_fulfillment_milestone ADD CONSTRAINT ck_com_fulfillment_milestone__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.com_fulfillment_milestone ADD CONSTRAINT ck_com_fulfillment_milestone__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.com_fulfillment_milestone ADD CONSTRAINT ck_com_fulfillment_milestone__milestone_type CHECK (milestone_type IN ('dispatch', 'delivery', 'service_delivery', 'training_session', 'project_deliverable', 'acceptance', 'return'));

ALTER TABLE ge.com_fulfillment_milestone ADD CONSTRAINT ck_com_fulfillment_milestone__planned_quantity CHECK (planned_quantity > 0);

ALTER TABLE ge.com_fulfillment_milestone ADD CONSTRAINT ck_com_fulfillment_milestone__state CHECK (state IN ('planned', 'in_progress', 'delivered', 'accepted', 'rejected', 'returned', 'cancelled'));

ALTER TABLE ge.ai_eval_case_result ADD CONSTRAINT ck_ai_eval_case_result__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.ai_eval_case_result ADD CONSTRAINT ck_ai_eval_case_result__score CHECK (score BETWEEN 0 AND 1);

ALTER TABLE ge.inv_source ADD CONSTRAINT ck_inv_source__revision CHECK (revision >= 1);

ALTER TABLE ge.inv_source ADD CONSTRAINT ck_inv_source__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.inv_source ADD CONSTRAINT ck_inv_source__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.inv_source ADD CONSTRAINT ck_inv_source__region CHECK (region IN ('IN','EU'));

ALTER TABLE ge.inv_source_policy ADD CONSTRAINT ck_inv_source_policy__revision CHECK (revision >= 1);

ALTER TABLE ge.inv_source_policy ADD CONSTRAINT ck_inv_source_policy__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.inv_source_policy ADD CONSTRAINT ck_inv_source_policy__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.inv_source_policy ADD CONSTRAINT ck_inv_source_policy__region CHECK (region IN ('IN','EU'));

ALTER TABLE ge.inv_search_plan ADD CONSTRAINT ck_inv_search_plan__revision CHECK (revision >= 1);

ALTER TABLE ge.inv_search_plan ADD CONSTRAINT ck_inv_search_plan__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.inv_search_plan ADD CONSTRAINT ck_inv_search_plan__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.inv_search_plan ADD CONSTRAINT ck_inv_search_plan__region CHECK (region IN ('IN','EU'));

ALTER TABLE ge.inv_search_run ADD CONSTRAINT ck_inv_search_run__revision CHECK (revision >= 1);

ALTER TABLE ge.inv_search_run ADD CONSTRAINT ck_inv_search_run__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.inv_search_run ADD CONSTRAINT ck_inv_search_run__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.inv_search_run ADD CONSTRAINT ck_inv_search_run__region CHECK (region IN ('IN','EU'));

ALTER TABLE ge.inv_funding_route ADD CONSTRAINT ck_inv_funding_route__revision CHECK (revision >= 1);

ALTER TABLE ge.inv_funding_route ADD CONSTRAINT ck_inv_funding_route__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.inv_funding_route ADD CONSTRAINT ck_inv_funding_route__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.inv_funding_route ADD CONSTRAINT ck_inv_funding_route__region CHECK (region IN ('IN','EU'));

ALTER TABLE ge.inv_opportunity ADD CONSTRAINT ck_inv_opportunity__revision CHECK (revision >= 1);

ALTER TABLE ge.inv_opportunity ADD CONSTRAINT ck_inv_opportunity__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.inv_opportunity ADD CONSTRAINT ck_inv_opportunity__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.inv_opportunity ADD CONSTRAINT ck_inv_opportunity__region CHECK (region IN ('IN','EU'));

ALTER TABLE ge.inv_evidence ADD CONSTRAINT ck_inv_evidence__revision CHECK (revision >= 1);

ALTER TABLE ge.inv_evidence ADD CONSTRAINT ck_inv_evidence__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.inv_evidence ADD CONSTRAINT ck_inv_evidence__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.inv_evidence ADD CONSTRAINT ck_inv_evidence__region CHECK (region IN ('IN','EU'));

ALTER TABLE ge.inv_investor ADD CONSTRAINT ck_inv_investor__revision CHECK (revision >= 1);

ALTER TABLE ge.inv_investor ADD CONSTRAINT ck_inv_investor__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.inv_investor ADD CONSTRAINT ck_inv_investor__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.inv_investor ADD CONSTRAINT ck_inv_investor__region CHECK (region IN ('IN','EU'));

ALTER TABLE ge.inv_investor_alias ADD CONSTRAINT ck_inv_investor_alias__revision CHECK (revision >= 1);

ALTER TABLE ge.inv_investor_alias ADD CONSTRAINT ck_inv_investor_alias__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.inv_investor_alias ADD CONSTRAINT ck_inv_investor_alias__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.inv_investor_alias ADD CONSTRAINT ck_inv_investor_alias__region CHECK (region IN ('IN','EU'));

ALTER TABLE ge.inv_mandate ADD CONSTRAINT ck_inv_mandate__revision CHECK (revision >= 1);

ALTER TABLE ge.inv_mandate ADD CONSTRAINT ck_inv_mandate__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.inv_mandate ADD CONSTRAINT ck_inv_mandate__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.inv_mandate ADD CONSTRAINT ck_inv_mandate__region CHECK (region IN ('IN','EU'));

ALTER TABLE ge.inv_round ADD CONSTRAINT ck_inv_round__revision CHECK (revision >= 1);

ALTER TABLE ge.inv_round ADD CONSTRAINT ck_inv_round__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.inv_round ADD CONSTRAINT ck_inv_round__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.inv_round ADD CONSTRAINT ck_inv_round__region CHECK (region IN ('IN','EU'));

ALTER TABLE ge.inv_fit_score ADD CONSTRAINT ck_inv_fit_score__revision CHECK (revision >= 1);

ALTER TABLE ge.inv_fit_score ADD CONSTRAINT ck_inv_fit_score__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.inv_fit_score ADD CONSTRAINT ck_inv_fit_score__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.inv_fit_score ADD CONSTRAINT ck_inv_fit_score__region CHECK (region IN ('IN','EU'));

ALTER TABLE ge.inv_match_candidate ADD CONSTRAINT ck_inv_match_candidate__revision CHECK (revision >= 1);

ALTER TABLE ge.inv_match_candidate ADD CONSTRAINT ck_inv_match_candidate__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.inv_match_candidate ADD CONSTRAINT ck_inv_match_candidate__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.inv_match_candidate ADD CONSTRAINT ck_inv_match_candidate__region CHECK (region IN ('IN','EU'));

ALTER TABLE ge.inv_jurisdiction_policy ADD CONSTRAINT ck_inv_jurisdiction_policy__revision CHECK (revision >= 1);

ALTER TABLE ge.inv_jurisdiction_policy ADD CONSTRAINT ck_inv_jurisdiction_policy__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.inv_jurisdiction_policy ADD CONSTRAINT ck_inv_jurisdiction_policy__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.inv_jurisdiction_policy ADD CONSTRAINT ck_inv_jurisdiction_policy__region CHECK (region IN ('IN','EU'));

ALTER TABLE ge.inv_crossborder_case ADD CONSTRAINT ck_inv_crossborder_case__revision CHECK (revision >= 1);

ALTER TABLE ge.inv_crossborder_case ADD CONSTRAINT ck_inv_crossborder_case__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.inv_crossborder_case ADD CONSTRAINT ck_inv_crossborder_case__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.inv_crossborder_case ADD CONSTRAINT ck_inv_crossborder_case__region CHECK (region IN ('IN','EU'));

ALTER TABLE ge.inv_contact ADD CONSTRAINT ck_inv_contact__revision CHECK (revision >= 1);

ALTER TABLE ge.inv_contact ADD CONSTRAINT ck_inv_contact__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.inv_contact ADD CONSTRAINT ck_inv_contact__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.inv_contact ADD CONSTRAINT ck_inv_contact__region CHECK (region IN ('IN','EU'));

ALTER TABLE ge.inv_contact_evidence ADD CONSTRAINT ck_inv_contact_evidence__revision CHECK (revision >= 1);

ALTER TABLE ge.inv_contact_evidence ADD CONSTRAINT ck_inv_contact_evidence__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.inv_contact_evidence ADD CONSTRAINT ck_inv_contact_evidence__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.inv_contact_evidence ADD CONSTRAINT ck_inv_contact_evidence__region CHECK (region IN ('IN','EU'));

ALTER TABLE ge.inv_permission ADD CONSTRAINT ck_inv_permission__revision CHECK (revision >= 1);

ALTER TABLE ge.inv_permission ADD CONSTRAINT ck_inv_permission__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.inv_permission ADD CONSTRAINT ck_inv_permission__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.inv_permission ADD CONSTRAINT ck_inv_permission__region CHECK (region IN ('IN','EU'));

ALTER TABLE ge.inv_suppression ADD CONSTRAINT ck_inv_suppression__revision CHECK (revision >= 1);

ALTER TABLE ge.inv_suppression ADD CONSTRAINT ck_inv_suppression__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.inv_suppression ADD CONSTRAINT ck_inv_suppression__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.inv_suppression ADD CONSTRAINT ck_inv_suppression__region CHECK (region IN ('IN','EU'));

ALTER TABLE ge.inv_locale_template ADD CONSTRAINT ck_inv_locale_template__revision CHECK (revision >= 1);

ALTER TABLE ge.inv_locale_template ADD CONSTRAINT ck_inv_locale_template__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.inv_locale_template ADD CONSTRAINT ck_inv_locale_template__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.inv_locale_template ADD CONSTRAINT ck_inv_locale_template__region CHECK (region IN ('IN','EU'));

ALTER TABLE ge.inv_message ADD CONSTRAINT ck_inv_message__revision CHECK (revision >= 1);

ALTER TABLE ge.inv_message ADD CONSTRAINT ck_inv_message__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.inv_message ADD CONSTRAINT ck_inv_message__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.inv_message ADD CONSTRAINT ck_inv_message__region CHECK (region IN ('IN','EU'));

ALTER TABLE ge.inv_outbox ADD CONSTRAINT ck_inv_outbox__revision CHECK (revision >= 1);

ALTER TABLE ge.inv_outbox ADD CONSTRAINT ck_inv_outbox__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.inv_outbox ADD CONSTRAINT ck_inv_outbox__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.inv_outbox ADD CONSTRAINT ck_inv_outbox__region CHECK (region IN ('IN','EU'));

ALTER TABLE ge.inv_outreach_reservation ADD CONSTRAINT ck_inv_outreach_reservation__revision CHECK (revision >= 1);

ALTER TABLE ge.inv_outreach_reservation ADD CONSTRAINT ck_inv_outreach_reservation__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.inv_outreach_reservation ADD CONSTRAINT ck_inv_outreach_reservation__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.inv_outreach_reservation ADD CONSTRAINT ck_inv_outreach_reservation__region CHECK (region IN ('IN','EU'));

ALTER TABLE ge.inv_delivery_event ADD CONSTRAINT ck_inv_delivery_event__revision CHECK (revision >= 1);

ALTER TABLE ge.inv_delivery_event ADD CONSTRAINT ck_inv_delivery_event__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.inv_delivery_event ADD CONSTRAINT ck_inv_delivery_event__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.inv_delivery_event ADD CONSTRAINT ck_inv_delivery_event__region CHECK (region IN ('IN','EU'));

ALTER TABLE ge.inv_channel ADD CONSTRAINT ck_inv_channel__revision CHECK (revision >= 1);

ALTER TABLE ge.inv_channel ADD CONSTRAINT ck_inv_channel__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.inv_channel ADD CONSTRAINT ck_inv_channel__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.inv_channel ADD CONSTRAINT ck_inv_channel__region CHECK (region IN ('IN','EU'));

ALTER TABLE ge.inv_integration_connection ADD CONSTRAINT ck_inv_integration_connection__revision CHECK (revision >= 1);

ALTER TABLE ge.inv_integration_connection ADD CONSTRAINT ck_inv_integration_connection__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.inv_integration_connection ADD CONSTRAINT ck_inv_integration_connection__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.inv_integration_connection ADD CONSTRAINT ck_inv_integration_connection__region CHECK (region IN ('IN','EU'));

ALTER TABLE ge.inv_inbound_event ADD CONSTRAINT ck_inv_inbound_event__revision CHECK (revision >= 1);

ALTER TABLE ge.inv_inbound_event ADD CONSTRAINT ck_inv_inbound_event__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.inv_inbound_event ADD CONSTRAINT ck_inv_inbound_event__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.inv_inbound_event ADD CONSTRAINT ck_inv_inbound_event__region CHECK (region IN ('IN','EU'));

ALTER TABLE ge.inv_thread ADD CONSTRAINT ck_inv_thread__revision CHECK (revision >= 1);

ALTER TABLE ge.inv_thread ADD CONSTRAINT ck_inv_thread__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.inv_thread ADD CONSTRAINT ck_inv_thread__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.inv_thread ADD CONSTRAINT ck_inv_thread__region CHECK (region IN ('IN','EU'));

ALTER TABLE ge.inv_sequence ADD CONSTRAINT ck_inv_sequence__revision CHECK (revision >= 1);

ALTER TABLE ge.inv_sequence ADD CONSTRAINT ck_inv_sequence__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.inv_sequence ADD CONSTRAINT ck_inv_sequence__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.inv_sequence ADD CONSTRAINT ck_inv_sequence__region CHECK (region IN ('IN','EU'));

ALTER TABLE ge.inv_enrollment ADD CONSTRAINT ck_inv_enrollment__revision CHECK (revision >= 1);

ALTER TABLE ge.inv_enrollment ADD CONSTRAINT ck_inv_enrollment__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.inv_enrollment ADD CONSTRAINT ck_inv_enrollment__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.inv_enrollment ADD CONSTRAINT ck_inv_enrollment__region CHECK (region IN ('IN','EU'));

ALTER TABLE ge.inv_task ADD CONSTRAINT ck_inv_task__revision CHECK (revision >= 1);

ALTER TABLE ge.inv_task ADD CONSTRAINT ck_inv_task__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.inv_task ADD CONSTRAINT ck_inv_task__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.inv_task ADD CONSTRAINT ck_inv_task__region CHECK (region IN ('IN','EU'));

ALTER TABLE ge.inv_stage_event ADD CONSTRAINT ck_inv_stage_event__revision CHECK (revision >= 1);

ALTER TABLE ge.inv_stage_event ADD CONSTRAINT ck_inv_stage_event__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.inv_stage_event ADD CONSTRAINT ck_inv_stage_event__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.inv_stage_event ADD CONSTRAINT ck_inv_stage_event__region CHECK (region IN ('IN','EU'));

ALTER TABLE ge.inv_relationship ADD CONSTRAINT ck_inv_relationship__revision CHECK (revision >= 1);

ALTER TABLE ge.inv_relationship ADD CONSTRAINT ck_inv_relationship__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.inv_relationship ADD CONSTRAINT ck_inv_relationship__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.inv_relationship ADD CONSTRAINT ck_inv_relationship__region CHECK (region IN ('IN','EU'));

ALTER TABLE ge.inv_workflow_run ADD CONSTRAINT ck_inv_workflow_run__revision CHECK (revision >= 1);

ALTER TABLE ge.inv_workflow_run ADD CONSTRAINT ck_inv_workflow_run__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.inv_workflow_run ADD CONSTRAINT ck_inv_workflow_run__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.inv_workflow_run ADD CONSTRAINT ck_inv_workflow_run__region CHECK (region IN ('IN','EU'));

ALTER TABLE ge.inv_objection ADD CONSTRAINT ck_inv_objection__revision CHECK (revision >= 1);

ALTER TABLE ge.inv_objection ADD CONSTRAINT ck_inv_objection__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.inv_objection ADD CONSTRAINT ck_inv_objection__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.inv_objection ADD CONSTRAINT ck_inv_objection__region CHECK (region IN ('IN','EU'));

ALTER TABLE ge.inv_objection_rule ADD CONSTRAINT ck_inv_objection_rule__revision CHECK (revision >= 1);

ALTER TABLE ge.inv_objection_rule ADD CONSTRAINT ck_inv_objection_rule__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.inv_objection_rule ADD CONSTRAINT ck_inv_objection_rule__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.inv_objection_rule ADD CONSTRAINT ck_inv_objection_rule__region CHECK (region IN ('IN','EU'));

ALTER TABLE ge.inv_copilot_action ADD CONSTRAINT ck_inv_copilot_action__revision CHECK (revision >= 1);

ALTER TABLE ge.inv_copilot_action ADD CONSTRAINT ck_inv_copilot_action__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.inv_copilot_action ADD CONSTRAINT ck_inv_copilot_action__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.inv_copilot_action ADD CONSTRAINT ck_inv_copilot_action__region CHECK (region IN ('IN','EU'));

ALTER TABLE ge.inv_meeting ADD CONSTRAINT ck_inv_meeting__revision CHECK (revision >= 1);

ALTER TABLE ge.inv_meeting ADD CONSTRAINT ck_inv_meeting__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.inv_meeting ADD CONSTRAINT ck_inv_meeting__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.inv_meeting ADD CONSTRAINT ck_inv_meeting__region CHECK (region IN ('IN','EU'));

ALTER TABLE ge.inv_event ADD CONSTRAINT ck_inv_event__revision CHECK (revision >= 1);

ALTER TABLE ge.inv_event ADD CONSTRAINT ck_inv_event__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.inv_event ADD CONSTRAINT ck_inv_event__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.inv_event ADD CONSTRAINT ck_inv_event__region CHECK (region IN ('IN','EU'));

ALTER TABLE ge.inv_referral ADD CONSTRAINT ck_inv_referral__revision CHECK (revision >= 1);

ALTER TABLE ge.inv_referral ADD CONSTRAINT ck_inv_referral__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.inv_referral ADD CONSTRAINT ck_inv_referral__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.inv_referral ADD CONSTRAINT ck_inv_referral__region CHECK (region IN ('IN','EU'));

ALTER TABLE ge.inv_adviser_referral ADD CONSTRAINT ck_inv_adviser_referral__revision CHECK (revision >= 1);

ALTER TABLE ge.inv_adviser_referral ADD CONSTRAINT ck_inv_adviser_referral__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.inv_adviser_referral ADD CONSTRAINT ck_inv_adviser_referral__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.inv_adviser_referral ADD CONSTRAINT ck_inv_adviser_referral__region CHECK (region IN ('IN','EU'));

ALTER TABLE ge.inv_scenario ADD CONSTRAINT ck_inv_scenario__revision CHECK (revision >= 1);

ALTER TABLE ge.inv_scenario ADD CONSTRAINT ck_inv_scenario__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.inv_scenario ADD CONSTRAINT ck_inv_scenario__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.inv_scenario ADD CONSTRAINT ck_inv_scenario__region CHECK (region IN ('IN','EU'));

ALTER TABLE ge.inv_claim ADD CONSTRAINT ck_inv_claim__revision CHECK (revision >= 1);

ALTER TABLE ge.inv_claim ADD CONSTRAINT ck_inv_claim__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.inv_claim ADD CONSTRAINT ck_inv_claim__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.inv_claim ADD CONSTRAINT ck_inv_claim__region CHECK (region IN ('IN','EU'));

ALTER TABLE ge.inv_disclosure ADD CONSTRAINT ck_inv_disclosure__revision CHECK (revision >= 1);

ALTER TABLE ge.inv_disclosure ADD CONSTRAINT ck_inv_disclosure__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.inv_disclosure ADD CONSTRAINT ck_inv_disclosure__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.inv_disclosure ADD CONSTRAINT ck_inv_disclosure__region CHECK (region IN ('IN','EU'));

ALTER TABLE ge.inv_guarantee_evidence ADD CONSTRAINT ck_inv_guarantee_evidence__revision CHECK (revision >= 1);

ALTER TABLE ge.inv_guarantee_evidence ADD CONSTRAINT ck_inv_guarantee_evidence__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.inv_guarantee_evidence ADD CONSTRAINT ck_inv_guarantee_evidence__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.inv_guarantee_evidence ADD CONSTRAINT ck_inv_guarantee_evidence__region CHECK (region IN ('IN','EU'));

ALTER TABLE ge.inv_document ADD CONSTRAINT ck_inv_document__revision CHECK (revision >= 1);

ALTER TABLE ge.inv_document ADD CONSTRAINT ck_inv_document__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.inv_document ADD CONSTRAINT ck_inv_document__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.inv_document ADD CONSTRAINT ck_inv_document__region CHECK (region IN ('IN','EU'));

ALTER TABLE ge.inv_room ADD CONSTRAINT ck_inv_room__revision CHECK (revision >= 1);

ALTER TABLE ge.inv_room ADD CONSTRAINT ck_inv_room__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.inv_room ADD CONSTRAINT ck_inv_room__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.inv_room ADD CONSTRAINT ck_inv_room__region CHECK (region IN ('IN','EU'));

ALTER TABLE ge.inv_room_item ADD CONSTRAINT ck_inv_room_item__revision CHECK (revision >= 1);

ALTER TABLE ge.inv_room_item ADD CONSTRAINT ck_inv_room_item__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.inv_room_item ADD CONSTRAINT ck_inv_room_item__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.inv_room_item ADD CONSTRAINT ck_inv_room_item__region CHECK (region IN ('IN','EU'));

ALTER TABLE ge.inv_access_grant ADD CONSTRAINT ck_inv_access_grant__revision CHECK (revision >= 1);

ALTER TABLE ge.inv_access_grant ADD CONSTRAINT ck_inv_access_grant__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.inv_access_grant ADD CONSTRAINT ck_inv_access_grant__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.inv_access_grant ADD CONSTRAINT ck_inv_access_grant__region CHECK (region IN ('IN','EU'));

ALTER TABLE ge.inv_nda ADD CONSTRAINT ck_inv_nda__revision CHECK (revision >= 1);

ALTER TABLE ge.inv_nda ADD CONSTRAINT ck_inv_nda__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.inv_nda ADD CONSTRAINT ck_inv_nda__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.inv_nda ADD CONSTRAINT ck_inv_nda__region CHECK (region IN ('IN','EU'));

ALTER TABLE ge.inv_diligence_request ADD CONSTRAINT ck_inv_diligence_request__revision CHECK (revision >= 1);

ALTER TABLE ge.inv_diligence_request ADD CONSTRAINT ck_inv_diligence_request__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.inv_diligence_request ADD CONSTRAINT ck_inv_diligence_request__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.inv_diligence_request ADD CONSTRAINT ck_inv_diligence_request__region CHECK (region IN ('IN','EU'));

ALTER TABLE ge.inv_term_version ADD CONSTRAINT ck_inv_term_version__revision CHECK (revision >= 1);

ALTER TABLE ge.inv_term_version ADD CONSTRAINT ck_inv_term_version__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.inv_term_version ADD CONSTRAINT ck_inv_term_version__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.inv_term_version ADD CONSTRAINT ck_inv_term_version__region CHECK (region IN ('IN','EU'));

ALTER TABLE ge.inv_agreement ADD CONSTRAINT ck_inv_agreement__revision CHECK (revision >= 1);

ALTER TABLE ge.inv_agreement ADD CONSTRAINT ck_inv_agreement__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.inv_agreement ADD CONSTRAINT ck_inv_agreement__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.inv_agreement ADD CONSTRAINT ck_inv_agreement__region CHECK (region IN ('IN','EU'));

ALTER TABLE ge.inv_approval ADD CONSTRAINT ck_inv_approval__revision CHECK (revision >= 1);

ALTER TABLE ge.inv_approval ADD CONSTRAINT ck_inv_approval__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.inv_approval ADD CONSTRAINT ck_inv_approval__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.inv_approval ADD CONSTRAINT ck_inv_approval__region CHECK (region IN ('IN','EU'));

ALTER TABLE ge.inv_offer ADD CONSTRAINT ck_inv_offer__revision CHECK (revision >= 1);

ALTER TABLE ge.inv_offer ADD CONSTRAINT ck_inv_offer__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.inv_offer ADD CONSTRAINT ck_inv_offer__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.inv_offer ADD CONSTRAINT ck_inv_offer__region CHECK (region IN ('IN','EU'));

ALTER TABLE ge.inv_offer_batch ADD CONSTRAINT ck_inv_offer_batch__revision CHECK (revision >= 1);

ALTER TABLE ge.inv_offer_batch ADD CONSTRAINT ck_inv_offer_batch__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.inv_offer_batch ADD CONSTRAINT ck_inv_offer_batch__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.inv_offer_batch ADD CONSTRAINT ck_inv_offer_batch__region CHECK (region IN ('IN','EU'));

ALTER TABLE ge.inv_offer_recipient ADD CONSTRAINT ck_inv_offer_recipient__revision CHECK (revision >= 1);

ALTER TABLE ge.inv_offer_recipient ADD CONSTRAINT ck_inv_offer_recipient__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.inv_offer_recipient ADD CONSTRAINT ck_inv_offer_recipient__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.inv_offer_recipient ADD CONSTRAINT ck_inv_offer_recipient__region CHECK (region IN ('IN','EU'));

ALTER TABLE ge.inv_verification_case ADD CONSTRAINT ck_inv_verification_case__revision CHECK (revision >= 1);

ALTER TABLE ge.inv_verification_case ADD CONSTRAINT ck_inv_verification_case__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.inv_verification_case ADD CONSTRAINT ck_inv_verification_case__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.inv_verification_case ADD CONSTRAINT ck_inv_verification_case__region CHECK (region IN ('IN','EU'));

ALTER TABLE ge.inv_bank_account ADD CONSTRAINT ck_inv_bank_account__revision CHECK (revision >= 1);

ALTER TABLE ge.inv_bank_account ADD CONSTRAINT ck_inv_bank_account__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.inv_bank_account ADD CONSTRAINT ck_inv_bank_account__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.inv_bank_account ADD CONSTRAINT ck_inv_bank_account__region CHECK (region IN ('IN','EU'));

ALTER TABLE ge.inv_payment_instruction ADD CONSTRAINT ck_inv_payment_instruction__revision CHECK (revision >= 1);

ALTER TABLE ge.inv_payment_instruction ADD CONSTRAINT ck_inv_payment_instruction__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.inv_payment_instruction ADD CONSTRAINT ck_inv_payment_instruction__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.inv_payment_instruction ADD CONSTRAINT ck_inv_payment_instruction__region CHECK (region IN ('IN','EU'));

ALTER TABLE ge.inv_commitment ADD CONSTRAINT ck_inv_commitment__revision CHECK (revision >= 1);

ALTER TABLE ge.inv_commitment ADD CONSTRAINT ck_inv_commitment__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.inv_commitment ADD CONSTRAINT ck_inv_commitment__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.inv_commitment ADD CONSTRAINT ck_inv_commitment__region CHECK (region IN ('IN','EU'));

ALTER TABLE ge.inv_receipt ADD CONSTRAINT ck_inv_receipt__revision CHECK (revision >= 1);

ALTER TABLE ge.inv_receipt ADD CONSTRAINT ck_inv_receipt__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.inv_receipt ADD CONSTRAINT ck_inv_receipt__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.inv_receipt ADD CONSTRAINT ck_inv_receipt__region CHECK (region IN ('IN','EU'));

ALTER TABLE ge.inv_receipt_allocation ADD CONSTRAINT ck_inv_receipt_allocation__revision CHECK (revision >= 1);

ALTER TABLE ge.inv_receipt_allocation ADD CONSTRAINT ck_inv_receipt_allocation__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.inv_receipt_allocation ADD CONSTRAINT ck_inv_receipt_allocation__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.inv_receipt_allocation ADD CONSTRAINT ck_inv_receipt_allocation__region CHECK (region IN ('IN','EU'));

ALTER TABLE ge.inv_refund ADD CONSTRAINT ck_inv_refund__revision CHECK (revision >= 1);

ALTER TABLE ge.inv_refund ADD CONSTRAINT ck_inv_refund__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.inv_refund ADD CONSTRAINT ck_inv_refund__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.inv_refund ADD CONSTRAINT ck_inv_refund__region CHECK (region IN ('IN','EU'));

ALTER TABLE ge.inv_fx_rate ADD CONSTRAINT ck_inv_fx_rate__revision CHECK (revision >= 1);

ALTER TABLE ge.inv_fx_rate ADD CONSTRAINT ck_inv_fx_rate__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.inv_fx_rate ADD CONSTRAINT ck_inv_fx_rate__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.inv_fx_rate ADD CONSTRAINT ck_inv_fx_rate__region CHECK (region IN ('IN','EU'));

ALTER TABLE ge.inv_offering ADD CONSTRAINT ck_inv_offering__revision CHECK (revision >= 1);

ALTER TABLE ge.inv_offering ADD CONSTRAINT ck_inv_offering__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.inv_offering ADD CONSTRAINT ck_inv_offering__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.inv_offering ADD CONSTRAINT ck_inv_offering__region CHECK (region IN ('IN','EU'));

ALTER TABLE ge.inv_counsel_signoff ADD CONSTRAINT ck_inv_counsel_signoff__revision CHECK (revision >= 1);

ALTER TABLE ge.inv_counsel_signoff ADD CONSTRAINT ck_inv_counsel_signoff__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.inv_counsel_signoff ADD CONSTRAINT ck_inv_counsel_signoff__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.inv_counsel_signoff ADD CONSTRAINT ck_inv_counsel_signoff__region CHECK (region IN ('IN','EU'));

ALTER TABLE ge.inv_eligibility_check ADD CONSTRAINT ck_inv_eligibility_check__revision CHECK (revision >= 1);

ALTER TABLE ge.inv_eligibility_check ADD CONSTRAINT ck_inv_eligibility_check__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.inv_eligibility_check ADD CONSTRAINT ck_inv_eligibility_check__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.inv_eligibility_check ADD CONSTRAINT ck_inv_eligibility_check__region CHECK (region IN ('IN','EU'));

ALTER TABLE ge.inv_relationship_provenance ADD CONSTRAINT ck_inv_relationship_provenance__revision CHECK (revision >= 1);

ALTER TABLE ge.inv_relationship_provenance ADD CONSTRAINT ck_inv_relationship_provenance__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.inv_relationship_provenance ADD CONSTRAINT ck_inv_relationship_provenance__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.inv_relationship_provenance ADD CONSTRAINT ck_inv_relationship_provenance__region CHECK (region IN ('IN','EU'));

ALTER TABLE ge.inv_offer_counter ADD CONSTRAINT ck_inv_offer_counter__revision CHECK (revision >= 1);

ALTER TABLE ge.inv_offer_counter ADD CONSTRAINT ck_inv_offer_counter__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.inv_offer_counter ADD CONSTRAINT ck_inv_offer_counter__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.inv_offer_counter ADD CONSTRAINT ck_inv_offer_counter__region CHECK (region IN ('IN','EU'));

ALTER TABLE ge.inv_guard_finding ADD CONSTRAINT ck_inv_guard_finding__revision CHECK (revision >= 1);

ALTER TABLE ge.inv_guard_finding ADD CONSTRAINT ck_inv_guard_finding__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.inv_guard_finding ADD CONSTRAINT ck_inv_guard_finding__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.inv_guard_finding ADD CONSTRAINT ck_inv_guard_finding__region CHECK (region IN ('IN','EU'));

ALTER TABLE ge.inv_offer_ledger ADD CONSTRAINT ck_inv_offer_ledger__revision CHECK (revision >= 1);

ALTER TABLE ge.inv_offer_ledger ADD CONSTRAINT ck_inv_offer_ledger__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.inv_offer_ledger ADD CONSTRAINT ck_inv_offer_ledger__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.inv_offer_ledger ADD CONSTRAINT ck_inv_offer_ledger__region CHECK (region IN ('IN','EU'));

ALTER TABLE ge.inv_offeree ADD CONSTRAINT ck_inv_offeree__revision CHECK (revision >= 1);

ALTER TABLE ge.inv_offeree ADD CONSTRAINT ck_inv_offeree__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.inv_offeree ADD CONSTRAINT ck_inv_offeree__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.inv_offeree ADD CONSTRAINT ck_inv_offeree__region CHECK (region IN ('IN','EU'));

ALTER TABLE ge.inv_investor_classification ADD CONSTRAINT ck_inv_investor_classification__revision CHECK (revision >= 1);

ALTER TABLE ge.inv_investor_classification ADD CONSTRAINT ck_inv_investor_classification__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.inv_investor_classification ADD CONSTRAINT ck_inv_investor_classification__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.inv_investor_classification ADD CONSTRAINT ck_inv_investor_classification__region CHECK (region IN ('IN','EU'));

ALTER TABLE ge.inv_accreditation_verification ADD CONSTRAINT ck_inv_accreditation_verification__revision CHECK (revision >= 1);

ALTER TABLE ge.inv_accreditation_verification ADD CONSTRAINT ck_inv_accreditation_verification__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.inv_accreditation_verification ADD CONSTRAINT ck_inv_accreditation_verification__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.inv_accreditation_verification ADD CONSTRAINT ck_inv_accreditation_verification__region CHECK (region IN ('IN','EU'));

ALTER TABLE ge.inv_promotion_review ADD CONSTRAINT ck_inv_promotion_review__revision CHECK (revision >= 1);

ALTER TABLE ge.inv_promotion_review ADD CONSTRAINT ck_inv_promotion_review__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.inv_promotion_review ADD CONSTRAINT ck_inv_promotion_review__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.inv_promotion_review ADD CONSTRAINT ck_inv_promotion_review__region CHECK (region IN ('IN','EU'));

ALTER TABLE ge.inv_application_money_account ADD CONSTRAINT ck_inv_application_money_account__revision CHECK (revision >= 1);

ALTER TABLE ge.inv_application_money_account ADD CONSTRAINT ck_inv_application_money_account__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.inv_application_money_account ADD CONSTRAINT ck_inv_application_money_account__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.inv_application_money_account ADD CONSTRAINT ck_inv_application_money_account__region CHECK (region IN ('IN','EU'));

ALTER TABLE ge.inv_allotment_clock ADD CONSTRAINT ck_inv_allotment_clock__revision CHECK (revision >= 1);

ALTER TABLE ge.inv_allotment_clock ADD CONSTRAINT ck_inv_allotment_clock__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.inv_allotment_clock ADD CONSTRAINT ck_inv_allotment_clock__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.inv_allotment_clock ADD CONSTRAINT ck_inv_allotment_clock__region CHECK (region IN ('IN','EU'));

ALTER TABLE ge.inv_closing ADD CONSTRAINT ck_inv_closing__revision CHECK (revision >= 1);

ALTER TABLE ge.inv_closing ADD CONSTRAINT ck_inv_closing__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.inv_closing ADD CONSTRAINT ck_inv_closing__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.inv_closing ADD CONSTRAINT ck_inv_closing__region CHECK (region IN ('IN','EU'));

ALTER TABLE ge.inv_closing_requirement ADD CONSTRAINT ck_inv_closing_requirement__revision CHECK (revision >= 1);

ALTER TABLE ge.inv_closing_requirement ADD CONSTRAINT ck_inv_closing_requirement__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.inv_closing_requirement ADD CONSTRAINT ck_inv_closing_requirement__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.inv_closing_requirement ADD CONSTRAINT ck_inv_closing_requirement__region CHECK (region IN ('IN','EU'));

ALTER TABLE ge.inv_allotment ADD CONSTRAINT ck_inv_allotment__revision CHECK (revision >= 1);

ALTER TABLE ge.inv_allotment ADD CONSTRAINT ck_inv_allotment__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.inv_allotment ADD CONSTRAINT ck_inv_allotment__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.inv_allotment ADD CONSTRAINT ck_inv_allotment__region CHECK (region IN ('IN','EU'));

ALTER TABLE ge.inv_filing_task ADD CONSTRAINT ck_inv_filing_task__revision CHECK (revision >= 1);

ALTER TABLE ge.inv_filing_task ADD CONSTRAINT ck_inv_filing_task__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.inv_filing_task ADD CONSTRAINT ck_inv_filing_task__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.inv_filing_task ADD CONSTRAINT ck_inv_filing_task__region CHECK (region IN ('IN','EU'));

ALTER TABLE ge.inv_legal_check ADD CONSTRAINT ck_inv_legal_check__revision CHECK (revision >= 1);

ALTER TABLE ge.inv_legal_check ADD CONSTRAINT ck_inv_legal_check__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.inv_legal_check ADD CONSTRAINT ck_inv_legal_check__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.inv_legal_check ADD CONSTRAINT ck_inv_legal_check__region CHECK (region IN ('IN','EU'));

ALTER TABLE ge.inv_obligation ADD CONSTRAINT ck_inv_obligation__revision CHECK (revision >= 1);

ALTER TABLE ge.inv_obligation ADD CONSTRAINT ck_inv_obligation__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.inv_obligation ADD CONSTRAINT ck_inv_obligation__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.inv_obligation ADD CONSTRAINT ck_inv_obligation__region CHECK (region IN ('IN','EU'));

ALTER TABLE ge.inv_update ADD CONSTRAINT ck_inv_update__revision CHECK (revision >= 1);

ALTER TABLE ge.inv_update ADD CONSTRAINT ck_inv_update__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.inv_update ADD CONSTRAINT ck_inv_update__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.inv_update ADD CONSTRAINT ck_inv_update__region CHECK (region IN ('IN','EU'));

ALTER TABLE ge.inv_feedback ADD CONSTRAINT ck_inv_feedback__revision CHECK (revision >= 1);

ALTER TABLE ge.inv_feedback ADD CONSTRAINT ck_inv_feedback__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.inv_feedback ADD CONSTRAINT ck_inv_feedback__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.inv_feedback ADD CONSTRAINT ck_inv_feedback__region CHECK (region IN ('IN','EU'));

ALTER TABLE ge.inv_deployment_milestone ADD CONSTRAINT ck_inv_deployment_milestone__revision CHECK (revision >= 1);

ALTER TABLE ge.inv_deployment_milestone ADD CONSTRAINT ck_inv_deployment_milestone__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.inv_deployment_milestone ADD CONSTRAINT ck_inv_deployment_milestone__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.inv_deployment_milestone ADD CONSTRAINT ck_inv_deployment_milestone__region CHECK (region IN ('IN','EU'));

ALTER TABLE ge.inv_capital_allocation ADD CONSTRAINT ck_inv_capital_allocation__revision CHECK (revision >= 1);

ALTER TABLE ge.inv_capital_allocation ADD CONSTRAINT ck_inv_capital_allocation__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.inv_capital_allocation ADD CONSTRAINT ck_inv_capital_allocation__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.inv_capital_allocation ADD CONSTRAINT ck_inv_capital_allocation__region CHECK (region IN ('IN','EU'));

ALTER TABLE ge.inv_dashboard_projection ADD CONSTRAINT ck_inv_dashboard_projection__revision CHECK (revision >= 1);

ALTER TABLE ge.inv_dashboard_projection ADD CONSTRAINT ck_inv_dashboard_projection__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.inv_dashboard_projection ADD CONSTRAINT ck_inv_dashboard_projection__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.inv_dashboard_projection ADD CONSTRAINT ck_inv_dashboard_projection__region CHECK (region IN ('IN','EU'));

ALTER TABLE ge.inv_webhook_endpoint ADD CONSTRAINT ck_inv_webhook_endpoint__revision CHECK (revision >= 1);

ALTER TABLE ge.inv_webhook_endpoint ADD CONSTRAINT ck_inv_webhook_endpoint__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.inv_webhook_endpoint ADD CONSTRAINT ck_inv_webhook_endpoint__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.inv_webhook_endpoint ADD CONSTRAINT ck_inv_webhook_endpoint__region CHECK (region IN ('IN','EU'));

ALTER TABLE ge.inv_external_agent_mandate ADD CONSTRAINT ck_inv_external_agent_mandate__revision CHECK (revision >= 1);

ALTER TABLE ge.inv_external_agent_mandate ADD CONSTRAINT ck_inv_external_agent_mandate__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.inv_external_agent_mandate ADD CONSTRAINT ck_inv_external_agent_mandate__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.inv_external_agent_mandate ADD CONSTRAINT ck_inv_external_agent_mandate__region CHECK (region IN ('IN','EU'));

ALTER TABLE ge.inv_grant_case ADD CONSTRAINT ck_inv_grant_case__revision CHECK (revision >= 1);

ALTER TABLE ge.inv_grant_case ADD CONSTRAINT ck_inv_grant_case__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.inv_grant_case ADD CONSTRAINT ck_inv_grant_case__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.inv_grant_case ADD CONSTRAINT ck_inv_grant_case__region CHECK (region IN ('IN','EU'));

ALTER TABLE ge.inv_grant_criterion ADD CONSTRAINT ck_inv_grant_criterion__revision CHECK (revision >= 1);

ALTER TABLE ge.inv_grant_criterion ADD CONSTRAINT ck_inv_grant_criterion__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.inv_grant_criterion ADD CONSTRAINT ck_inv_grant_criterion__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.inv_grant_criterion ADD CONSTRAINT ck_inv_grant_criterion__region CHECK (region IN ('IN','EU'));

ALTER TABLE ge.inv_grant_budget_line ADD CONSTRAINT ck_inv_grant_budget_line__revision CHECK (revision >= 1);

ALTER TABLE ge.inv_grant_budget_line ADD CONSTRAINT ck_inv_grant_budget_line__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.inv_grant_budget_line ADD CONSTRAINT ck_inv_grant_budget_line__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.inv_grant_budget_line ADD CONSTRAINT ck_inv_grant_budget_line__region CHECK (region IN ('IN','EU'));

ALTER TABLE ge.inv_grant_award ADD CONSTRAINT ck_inv_grant_award__revision CHECK (revision >= 1);

ALTER TABLE ge.inv_grant_award ADD CONSTRAINT ck_inv_grant_award__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.inv_grant_award ADD CONSTRAINT ck_inv_grant_award__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.inv_grant_award ADD CONSTRAINT ck_inv_grant_award__region CHECK (region IN ('IN','EU'));

ALTER TABLE ge.inv_debt_case ADD CONSTRAINT ck_inv_debt_case__revision CHECK (revision >= 1);

ALTER TABLE ge.inv_debt_case ADD CONSTRAINT ck_inv_debt_case__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.inv_debt_case ADD CONSTRAINT ck_inv_debt_case__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.inv_debt_case ADD CONSTRAINT ck_inv_debt_case__region CHECK (region IN ('IN','EU'));

ALTER TABLE ge.inv_debt_term ADD CONSTRAINT ck_inv_debt_term__revision CHECK (revision >= 1);

ALTER TABLE ge.inv_debt_term ADD CONSTRAINT ck_inv_debt_term__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.inv_debt_term ADD CONSTRAINT ck_inv_debt_term__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.inv_debt_term ADD CONSTRAINT ck_inv_debt_term__region CHECK (region IN ('IN','EU'));

ALTER TABLE ge.inv_covenant ADD CONSTRAINT ck_inv_covenant__revision CHECK (revision >= 1);

ALTER TABLE ge.inv_covenant ADD CONSTRAINT ck_inv_covenant__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.inv_covenant ADD CONSTRAINT ck_inv_covenant__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.inv_covenant ADD CONSTRAINT ck_inv_covenant__region CHECK (region IN ('IN','EU'));

ALTER TABLE ge.inv_repayment_schedule ADD CONSTRAINT ck_inv_repayment_schedule__revision CHECK (revision >= 1);

ALTER TABLE ge.inv_repayment_schedule ADD CONSTRAINT ck_inv_repayment_schedule__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.inv_repayment_schedule ADD CONSTRAINT ck_inv_repayment_schedule__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.inv_repayment_schedule ADD CONSTRAINT ck_inv_repayment_schedule__region CHECK (region IN ('IN','EU'));

ALTER TABLE ge.inv_readiness_snapshot ADD CONSTRAINT ck_inv_readiness_snapshot__revision CHECK (revision >= 1);

ALTER TABLE ge.inv_readiness_snapshot ADD CONSTRAINT ck_inv_readiness_snapshot__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.inv_readiness_snapshot ADD CONSTRAINT ck_inv_readiness_snapshot__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.inv_readiness_snapshot ADD CONSTRAINT ck_inv_readiness_snapshot__region CHECK (region IN ('IN','EU'));

ALTER TABLE ge.inv_runway_scenario ADD CONSTRAINT ck_inv_runway_scenario__revision CHECK (revision >= 1);

ALTER TABLE ge.inv_runway_scenario ADD CONSTRAINT ck_inv_runway_scenario__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.inv_runway_scenario ADD CONSTRAINT ck_inv_runway_scenario__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.inv_runway_scenario ADD CONSTRAINT ck_inv_runway_scenario__region CHECK (region IN ('IN','EU'));

ALTER TABLE ge.inv_readiness_score ADD CONSTRAINT ck_inv_readiness_score__revision CHECK (revision >= 1);

ALTER TABLE ge.inv_readiness_score ADD CONSTRAINT ck_inv_readiness_score__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.inv_readiness_score ADD CONSTRAINT ck_inv_readiness_score__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.inv_readiness_score ADD CONSTRAINT ck_inv_readiness_score__region CHECK (region IN ('IN','EU'));

ALTER TABLE ge.inv_shareholder ADD CONSTRAINT ck_inv_shareholder__revision CHECK (revision >= 1);

ALTER TABLE ge.inv_shareholder ADD CONSTRAINT ck_inv_shareholder__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.inv_shareholder ADD CONSTRAINT ck_inv_shareholder__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.inv_shareholder ADD CONSTRAINT ck_inv_shareholder__region CHECK (region IN ('IN','EU'));

ALTER TABLE ge.inv_holding ADD CONSTRAINT ck_inv_holding__revision CHECK (revision >= 1);

ALTER TABLE ge.inv_holding ADD CONSTRAINT ck_inv_holding__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.inv_holding ADD CONSTRAINT ck_inv_holding__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.inv_holding ADD CONSTRAINT ck_inv_holding__region CHECK (region IN ('IN','EU'));

ALTER TABLE ge.inv_instrument ADD CONSTRAINT ck_inv_instrument__revision CHECK (revision >= 1);

ALTER TABLE ge.inv_instrument ADD CONSTRAINT ck_inv_instrument__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.inv_instrument ADD CONSTRAINT ck_inv_instrument__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.inv_instrument ADD CONSTRAINT ck_inv_instrument__region CHECK (region IN ('IN','EU'));

ALTER TABLE ge.inv_instrument_term ADD CONSTRAINT ck_inv_instrument_term__revision CHECK (revision >= 1);

ALTER TABLE ge.inv_instrument_term ADD CONSTRAINT ck_inv_instrument_term__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.inv_instrument_term ADD CONSTRAINT ck_inv_instrument_term__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.inv_instrument_term ADD CONSTRAINT ck_inv_instrument_term__region CHECK (region IN ('IN','EU'));

ALTER TABLE ge.inv_option_grant ADD CONSTRAINT ck_inv_option_grant__revision CHECK (revision >= 1);

ALTER TABLE ge.inv_option_grant ADD CONSTRAINT ck_inv_option_grant__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.inv_option_grant ADD CONSTRAINT ck_inv_option_grant__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.inv_option_grant ADD CONSTRAINT ck_inv_option_grant__region CHECK (region IN ('IN','EU'));

ALTER TABLE ge.inv_cap_table_revision ADD CONSTRAINT ck_inv_cap_table_revision__revision CHECK (revision >= 1);

ALTER TABLE ge.inv_cap_table_revision ADD CONSTRAINT ck_inv_cap_table_revision__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.inv_cap_table_revision ADD CONSTRAINT ck_inv_cap_table_revision__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.inv_cap_table_revision ADD CONSTRAINT ck_inv_cap_table_revision__region CHECK (region IN ('IN','EU'));

ALTER TABLE ge.inv_esg_indicator ADD CONSTRAINT ck_inv_esg_indicator__revision CHECK (revision >= 1);

ALTER TABLE ge.inv_esg_indicator ADD CONSTRAINT ck_inv_esg_indicator__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.inv_esg_indicator ADD CONSTRAINT ck_inv_esg_indicator__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.inv_esg_indicator ADD CONSTRAINT ck_inv_esg_indicator__region CHECK (region IN ('IN','EU'));

ALTER TABLE ge.inv_esg_observation ADD CONSTRAINT ck_inv_esg_observation__revision CHECK (revision >= 1);

ALTER TABLE ge.inv_esg_observation ADD CONSTRAINT ck_inv_esg_observation__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.inv_esg_observation ADD CONSTRAINT ck_inv_esg_observation__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.inv_esg_observation ADD CONSTRAINT ck_inv_esg_observation__region CHECK (region IN ('IN','EU'));

ALTER TABLE ge.inv_esg_disclosure ADD CONSTRAINT ck_inv_esg_disclosure__revision CHECK (revision >= 1);

ALTER TABLE ge.inv_esg_disclosure ADD CONSTRAINT ck_inv_esg_disclosure__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.inv_esg_disclosure ADD CONSTRAINT ck_inv_esg_disclosure__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.inv_esg_disclosure ADD CONSTRAINT ck_inv_esg_disclosure__region CHECK (region IN ('IN','EU'));

ALTER TABLE ge.inv_esg_commitment ADD CONSTRAINT ck_inv_esg_commitment__revision CHECK (revision >= 1);

ALTER TABLE ge.inv_esg_commitment ADD CONSTRAINT ck_inv_esg_commitment__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.inv_esg_commitment ADD CONSTRAINT ck_inv_esg_commitment__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.inv_esg_commitment ADD CONSTRAINT ck_inv_esg_commitment__region CHECK (region IN ('IN','EU'));

ALTER TABLE ge.inv_crossborder_requirement ADD CONSTRAINT ck_inv_crossborder_requirement__revision CHECK (revision >= 1);

ALTER TABLE ge.inv_crossborder_requirement ADD CONSTRAINT ck_inv_crossborder_requirement__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.inv_crossborder_requirement ADD CONSTRAINT ck_inv_crossborder_requirement__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.inv_crossborder_requirement ADD CONSTRAINT ck_inv_crossborder_requirement__region CHECK (region IN ('IN','EU'));

ALTER TABLE ge.inv_regulatory_deadline ADD CONSTRAINT ck_inv_regulatory_deadline__revision CHECK (revision >= 1);

ALTER TABLE ge.inv_regulatory_deadline ADD CONSTRAINT ck_inv_regulatory_deadline__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.inv_regulatory_deadline ADD CONSTRAINT ck_inv_regulatory_deadline__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.inv_regulatory_deadline ADD CONSTRAINT ck_inv_regulatory_deadline__region CHECK (region IN ('IN','EU'));

ALTER TABLE ge.inv_resolution ADD CONSTRAINT ck_inv_resolution__revision CHECK (revision >= 1);

ALTER TABLE ge.inv_resolution ADD CONSTRAINT ck_inv_resolution__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.inv_resolution ADD CONSTRAINT ck_inv_resolution__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.inv_resolution ADD CONSTRAINT ck_inv_resolution__region CHECK (region IN ('IN','EU'));

ALTER TABLE ge.inv_vote ADD CONSTRAINT ck_inv_vote__revision CHECK (revision >= 1);

ALTER TABLE ge.inv_vote ADD CONSTRAINT ck_inv_vote__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.inv_vote ADD CONSTRAINT ck_inv_vote__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.inv_vote ADD CONSTRAINT ck_inv_vote__region CHECK (region IN ('IN','EU'));

ALTER TABLE ge.inv_decision_action ADD CONSTRAINT ck_inv_decision_action__revision CHECK (revision >= 1);

ALTER TABLE ge.inv_decision_action ADD CONSTRAINT ck_inv_decision_action__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.inv_decision_action ADD CONSTRAINT ck_inv_decision_action__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.inv_decision_action ADD CONSTRAINT ck_inv_decision_action__region CHECK (region IN ('IN','EU'));

ALTER TABLE ge.inv_kyc_case ADD CONSTRAINT ck_inv_kyc_case__revision CHECK (revision >= 1);

ALTER TABLE ge.inv_kyc_case ADD CONSTRAINT ck_inv_kyc_case__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.inv_kyc_case ADD CONSTRAINT ck_inv_kyc_case__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.inv_kyc_case ADD CONSTRAINT ck_inv_kyc_case__region CHECK (region IN ('IN','EU'));

ALTER TABLE ge.inv_kyc_provider_result ADD CONSTRAINT ck_inv_kyc_provider_result__revision CHECK (revision >= 1);

ALTER TABLE ge.inv_kyc_provider_result ADD CONSTRAINT ck_inv_kyc_provider_result__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.inv_kyc_provider_result ADD CONSTRAINT ck_inv_kyc_provider_result__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.inv_kyc_provider_result ADD CONSTRAINT ck_inv_kyc_provider_result__region CHECK (region IN ('IN','EU'));

ALTER TABLE ge.inv_screening_hit ADD CONSTRAINT ck_inv_screening_hit__revision CHECK (revision >= 1);

ALTER TABLE ge.inv_screening_hit ADD CONSTRAINT ck_inv_screening_hit__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.inv_screening_hit ADD CONSTRAINT ck_inv_screening_hit__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.inv_screening_hit ADD CONSTRAINT ck_inv_screening_hit__region CHECK (region IN ('IN','EU'));

ALTER TABLE ge.inv_advice_boundary_event ADD CONSTRAINT ck_inv_advice_boundary_event__revision CHECK (revision >= 1);

ALTER TABLE ge.inv_advice_boundary_event ADD CONSTRAINT ck_inv_advice_boundary_event__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.inv_advice_boundary_event ADD CONSTRAINT ck_inv_advice_boundary_event__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.inv_advice_boundary_event ADD CONSTRAINT ck_inv_advice_boundary_event__region CHECK (region IN ('IN','EU'));

ALTER TABLE ge.inv_rulepack_activation ADD CONSTRAINT ck_inv_rulepack_activation__revision CHECK (revision >= 1);

ALTER TABLE ge.inv_rulepack_activation ADD CONSTRAINT ck_inv_rulepack_activation__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.inv_rulepack_activation ADD CONSTRAINT ck_inv_rulepack_activation__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.inv_rulepack_activation ADD CONSTRAINT ck_inv_rulepack_activation__region CHECK (region IN ('IN','EU'));

ALTER TABLE ge.mandate ADD CONSTRAINT ck_mandate__revision CHECK (revision >= 1);

ALTER TABLE ge.mandate ADD CONSTRAINT ck_mandate__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.mandate ADD CONSTRAINT ck_mandate__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.mandate ADD CONSTRAINT ck_mandate__region CHECK (region IN ('IN','EU'));

ALTER TABLE ge.mandate_version ADD CONSTRAINT ck_mandate_version__revision CHECK (revision >= 1);

ALTER TABLE ge.mandate_version ADD CONSTRAINT ck_mandate_version__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.mandate_version ADD CONSTRAINT ck_mandate_version__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.mandate_version ADD CONSTRAINT ck_mandate_version__region CHECK (region IN ('IN','EU'));

ALTER TABLE ge.mandate_approval ADD CONSTRAINT ck_mandate_approval__revision CHECK (revision >= 1);

ALTER TABLE ge.mandate_approval ADD CONSTRAINT ck_mandate_approval__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.mandate_approval ADD CONSTRAINT ck_mandate_approval__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.mandate_approval ADD CONSTRAINT ck_mandate_approval__region CHECK (region IN ('IN','EU'));

ALTER TABLE ge.mandate_scope_item ADD CONSTRAINT ck_mandate_scope_item__revision CHECK (revision >= 1);

ALTER TABLE ge.mandate_scope_item ADD CONSTRAINT ck_mandate_scope_item__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.mandate_scope_item ADD CONSTRAINT ck_mandate_scope_item__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.mandate_scope_item ADD CONSTRAINT ck_mandate_scope_item__region CHECK (region IN ('IN','EU'));

ALTER TABLE ge.mandate_limit ADD CONSTRAINT ck_mandate_limit__revision CHECK (revision >= 1);

ALTER TABLE ge.mandate_limit ADD CONSTRAINT ck_mandate_limit__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.mandate_limit ADD CONSTRAINT ck_mandate_limit__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.mandate_limit ADD CONSTRAINT ck_mandate_limit__region CHECK (region IN ('IN','EU'));

ALTER TABLE ge.mandate_window ADD CONSTRAINT ck_mandate_window__revision CHECK (revision >= 1);

ALTER TABLE ge.mandate_window ADD CONSTRAINT ck_mandate_window__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.mandate_window ADD CONSTRAINT ck_mandate_window__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.mandate_window ADD CONSTRAINT ck_mandate_window__region CHECK (region IN ('IN','EU'));

ALTER TABLE ge.mandate_restriction ADD CONSTRAINT ck_mandate_restriction__revision CHECK (revision >= 1);

ALTER TABLE ge.mandate_restriction ADD CONSTRAINT ck_mandate_restriction__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.mandate_restriction ADD CONSTRAINT ck_mandate_restriction__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.mandate_restriction ADD CONSTRAINT ck_mandate_restriction__region CHECK (region IN ('IN','EU'));

ALTER TABLE ge.mandate_counter ADD CONSTRAINT ck_mandate_counter__revision CHECK (revision >= 1);

ALTER TABLE ge.mandate_counter ADD CONSTRAINT ck_mandate_counter__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.mandate_counter ADD CONSTRAINT ck_mandate_counter__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.mandate_counter ADD CONSTRAINT ck_mandate_counter__region CHECK (region IN ('IN','EU'));

ALTER TABLE ge.mandate_consumption ADD CONSTRAINT ck_mandate_consumption__revision CHECK (revision >= 1);

ALTER TABLE ge.mandate_consumption ADD CONSTRAINT ck_mandate_consumption__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.mandate_consumption ADD CONSTRAINT ck_mandate_consumption__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.mandate_consumption ADD CONSTRAINT ck_mandate_consumption__region CHECK (region IN ('IN','EU'));

ALTER TABLE ge.mandate_decision ADD CONSTRAINT ck_mandate_decision__revision CHECK (revision >= 1);

ALTER TABLE ge.mandate_decision ADD CONSTRAINT ck_mandate_decision__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.mandate_decision ADD CONSTRAINT ck_mandate_decision__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.mandate_decision ADD CONSTRAINT ck_mandate_decision__region CHECK (region IN ('IN','EU'));

ALTER TABLE ge.kill_switch ADD CONSTRAINT ck_kill_switch__revision CHECK (revision >= 1);

ALTER TABLE ge.kill_switch ADD CONSTRAINT ck_kill_switch__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.kill_switch ADD CONSTRAINT ck_kill_switch__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.kill_switch ADD CONSTRAINT ck_kill_switch__region CHECK (region IN ('IN','EU'));

ALTER TABLE ge.kill_switch_event ADD CONSTRAINT ck_kill_switch_event__revision CHECK (revision >= 1);

ALTER TABLE ge.kill_switch_event ADD CONSTRAINT ck_kill_switch_event__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.kill_switch_event ADD CONSTRAINT ck_kill_switch_event__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.kill_switch_event ADD CONSTRAINT ck_kill_switch_event__region CHECK (region IN ('IN','EU'));

ALTER TABLE ge.effect_receipt ADD CONSTRAINT ck_effect_receipt__revision CHECK (revision >= 1);

ALTER TABLE ge.effect_receipt ADD CONSTRAINT ck_effect_receipt__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.effect_receipt ADD CONSTRAINT ck_effect_receipt__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.effect_receipt ADD CONSTRAINT ck_effect_receipt__region CHECK (region IN ('IN','EU'));

ALTER TABLE ge.counterparty_agent ADD CONSTRAINT ck_counterparty_agent__revision CHECK (revision >= 1);

ALTER TABLE ge.counterparty_agent ADD CONSTRAINT ck_counterparty_agent__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.counterparty_agent ADD CONSTRAINT ck_counterparty_agent__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.counterparty_agent ADD CONSTRAINT ck_counterparty_agent__region CHECK (region IN ('IN','EU'));

ALTER TABLE ge.agent_credential ADD CONSTRAINT ck_agent_credential__revision CHECK (revision >= 1);

ALTER TABLE ge.agent_credential ADD CONSTRAINT ck_agent_credential__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.agent_credential ADD CONSTRAINT ck_agent_credential__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.agent_credential ADD CONSTRAINT ck_agent_credential__region CHECK (region IN ('IN','EU'));

ALTER TABLE ge.agent_message ADD CONSTRAINT ck_agent_message__revision CHECK (revision >= 1);

ALTER TABLE ge.agent_message ADD CONSTRAINT ck_agent_message__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.agent_message ADD CONSTRAINT ck_agent_message__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.agent_message ADD CONSTRAINT ck_agent_message__region CHECK (region IN ('IN','EU'));

ALTER TABLE ge.negotiation_session ADD CONSTRAINT ck_negotiation_session__revision CHECK (revision >= 1);

ALTER TABLE ge.negotiation_session ADD CONSTRAINT ck_negotiation_session__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.negotiation_session ADD CONSTRAINT ck_negotiation_session__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.negotiation_session ADD CONSTRAINT ck_negotiation_session__region CHECK (region IN ('IN','EU'));

ALTER TABLE ge.negotiation_step ADD CONSTRAINT ck_negotiation_step__revision CHECK (revision >= 1);

ALTER TABLE ge.negotiation_step ADD CONSTRAINT ck_negotiation_step__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.negotiation_step ADD CONSTRAINT ck_negotiation_step__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.negotiation_step ADD CONSTRAINT ck_negotiation_step__region CHECK (region IN ('IN','EU'));

ALTER TABLE ge.commerce_order ADD CONSTRAINT ck_commerce_order__revision CHECK (revision >= 1);

ALTER TABLE ge.commerce_order ADD CONSTRAINT ck_commerce_order__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.commerce_order ADD CONSTRAINT ck_commerce_order__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.commerce_order ADD CONSTRAINT ck_commerce_order__region CHECK (region IN ('IN','EU'));

ALTER TABLE ge.payment_mandate ADD CONSTRAINT ck_payment_mandate__revision CHECK (revision >= 1);

ALTER TABLE ge.payment_mandate ADD CONSTRAINT ck_payment_mandate__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.payment_mandate ADD CONSTRAINT ck_payment_mandate__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.payment_mandate ADD CONSTRAINT ck_payment_mandate__region CHECK (region IN ('IN','EU'));

ALTER TABLE ge.payment_txn ADD CONSTRAINT ck_payment_txn__revision CHECK (revision >= 1);

ALTER TABLE ge.payment_txn ADD CONSTRAINT ck_payment_txn__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.payment_txn ADD CONSTRAINT ck_payment_txn__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.payment_txn ADD CONSTRAINT ck_payment_txn__region CHECK (region IN ('IN','EU'));

ALTER TABLE ge.refund ADD CONSTRAINT ck_refund__revision CHECK (revision >= 1);

ALTER TABLE ge.refund ADD CONSTRAINT ck_refund__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.refund ADD CONSTRAINT ck_refund__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.refund ADD CONSTRAINT ck_refund__region CHECK (region IN ('IN','EU'));

ALTER TABLE ge.dispute_case ADD CONSTRAINT ck_dispute_case__revision CHECK (revision >= 1);

ALTER TABLE ge.dispute_case ADD CONSTRAINT ck_dispute_case__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.dispute_case ADD CONSTRAINT ck_dispute_case__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.dispute_case ADD CONSTRAINT ck_dispute_case__region CHECK (region IN ('IN','EU'));

ALTER TABLE ge.settlement_batch ADD CONSTRAINT ck_settlement_batch__revision CHECK (revision >= 1);

ALTER TABLE ge.settlement_batch ADD CONSTRAINT ck_settlement_batch__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.settlement_batch ADD CONSTRAINT ck_settlement_batch__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.settlement_batch ADD CONSTRAINT ck_settlement_batch__region CHECK (region IN ('IN','EU'));

ALTER TABLE ge.bid_package ADD CONSTRAINT ck_bid_package__revision CHECK (revision >= 1);

ALTER TABLE ge.bid_package ADD CONSTRAINT ck_bid_package__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.bid_package ADD CONSTRAINT ck_bid_package__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.bid_package ADD CONSTRAINT ck_bid_package__region CHECK (region IN ('IN','EU'));

ALTER TABLE ge.bid_file ADD CONSTRAINT ck_bid_file__revision CHECK (revision >= 1);

ALTER TABLE ge.bid_file ADD CONSTRAINT ck_bid_file__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.bid_file ADD CONSTRAINT ck_bid_file__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.bid_file ADD CONSTRAINT ck_bid_file__region CHECK (region IN ('IN','EU'));

ALTER TABLE ge.bid_submission ADD CONSTRAINT ck_bid_submission__revision CHECK (revision >= 1);

ALTER TABLE ge.bid_submission ADD CONSTRAINT ck_bid_submission__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.bid_submission ADD CONSTRAINT ck_bid_submission__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.bid_submission ADD CONSTRAINT ck_bid_submission__region CHECK (region IN ('IN','EU'));

ALTER TABLE ge.portal_profile ADD CONSTRAINT ck_portal_profile__revision CHECK (revision >= 1);

ALTER TABLE ge.portal_profile ADD CONSTRAINT ck_portal_profile__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.portal_profile ADD CONSTRAINT ck_portal_profile__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.portal_profile ADD CONSTRAINT ck_portal_profile__region CHECK (region IN ('IN','EU'));

ALTER TABLE ge.recon_run ADD CONSTRAINT ck_recon_run__revision CHECK (revision >= 1);

ALTER TABLE ge.recon_run ADD CONSTRAINT ck_recon_run__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.recon_run ADD CONSTRAINT ck_recon_run__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.recon_run ADD CONSTRAINT ck_recon_run__region CHECK (region IN ('IN','EU'));

ALTER TABLE ge.recon_break ADD CONSTRAINT ck_recon_break__revision CHECK (revision >= 1);

ALTER TABLE ge.recon_break ADD CONSTRAINT ck_recon_break__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.recon_break ADD CONSTRAINT ck_recon_break__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.recon_break ADD CONSTRAINT ck_recon_break__region CHECK (region IN ('IN','EU'));

ALTER TABLE ge.ledger_entry ADD CONSTRAINT ck_ledger_entry__revision CHECK (revision >= 1);

ALTER TABLE ge.ledger_entry ADD CONSTRAINT ck_ledger_entry__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.ledger_entry ADD CONSTRAINT ck_ledger_entry__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.ledger_entry ADD CONSTRAINT ck_ledger_entry__region CHECK (region IN ('IN','EU'));

ALTER TABLE ge.voice_session ADD CONSTRAINT ck_voice_session__revision CHECK (revision >= 1);

ALTER TABLE ge.voice_session ADD CONSTRAINT ck_voice_session__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.voice_session ADD CONSTRAINT ck_voice_session__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.voice_session ADD CONSTRAINT ck_voice_session__region CHECK (region IN ('IN','EU'));

ALTER TABLE ge.voice_leg ADD CONSTRAINT ck_voice_leg__revision CHECK (revision >= 1);

ALTER TABLE ge.voice_leg ADD CONSTRAINT ck_voice_leg__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.voice_leg ADD CONSTRAINT ck_voice_leg__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.voice_leg ADD CONSTRAINT ck_voice_leg__region CHECK (region IN ('IN','EU'));

ALTER TABLE ge.voice_campaign ADD CONSTRAINT ck_voice_campaign__revision CHECK (revision >= 1);

ALTER TABLE ge.voice_campaign ADD CONSTRAINT ck_voice_campaign__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.voice_campaign ADD CONSTRAINT ck_voice_campaign__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.voice_campaign ADD CONSTRAINT ck_voice_campaign__region CHECK (region IN ('IN','EU'));

ALTER TABLE ge.voice_campaign_contact ADD CONSTRAINT ck_voice_campaign_contact__revision CHECK (revision >= 1);

ALTER TABLE ge.voice_campaign_contact ADD CONSTRAINT ck_voice_campaign_contact__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.voice_campaign_contact ADD CONSTRAINT ck_voice_campaign_contact__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.voice_campaign_contact ADD CONSTRAINT ck_voice_campaign_contact__region CHECK (region IN ('IN','EU'));

ALTER TABLE ge.voice_script ADD CONSTRAINT ck_voice_script__revision CHECK (revision >= 1);

ALTER TABLE ge.voice_script ADD CONSTRAINT ck_voice_script__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.voice_script ADD CONSTRAINT ck_voice_script__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.voice_script ADD CONSTRAINT ck_voice_script__region CHECK (region IN ('IN','EU'));

ALTER TABLE ge.voice_script_version ADD CONSTRAINT ck_voice_script_version__revision CHECK (revision >= 1);

ALTER TABLE ge.voice_script_version ADD CONSTRAINT ck_voice_script_version__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.voice_script_version ADD CONSTRAINT ck_voice_script_version__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.voice_script_version ADD CONSTRAINT ck_voice_script_version__region CHECK (region IN ('IN','EU'));

ALTER TABLE ge.voice_number ADD CONSTRAINT ck_voice_number__revision CHECK (revision >= 1);

ALTER TABLE ge.voice_number ADD CONSTRAINT ck_voice_number__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.voice_number ADD CONSTRAINT ck_voice_number__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.voice_number ADD CONSTRAINT ck_voice_number__region CHECK (region IN ('IN','EU'));

ALTER TABLE ge.voice_number_pool ADD CONSTRAINT ck_voice_number_pool__revision CHECK (revision >= 1);

ALTER TABLE ge.voice_number_pool ADD CONSTRAINT ck_voice_number_pool__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.voice_number_pool ADD CONSTRAINT ck_voice_number_pool__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.voice_number_pool ADD CONSTRAINT ck_voice_number_pool__region CHECK (region IN ('IN','EU'));

ALTER TABLE ge.voice_scrub_result ADD CONSTRAINT ck_voice_scrub_result__revision CHECK (revision >= 1);

ALTER TABLE ge.voice_scrub_result ADD CONSTRAINT ck_voice_scrub_result__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.voice_scrub_result ADD CONSTRAINT ck_voice_scrub_result__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.voice_scrub_result ADD CONSTRAINT ck_voice_scrub_result__region CHECK (region IN ('IN','EU'));

ALTER TABLE ge.voice_consent_evidence ADD CONSTRAINT ck_voice_consent_evidence__revision CHECK (revision >= 1);

ALTER TABLE ge.voice_consent_evidence ADD CONSTRAINT ck_voice_consent_evidence__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.voice_consent_evidence ADD CONSTRAINT ck_voice_consent_evidence__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.voice_consent_evidence ADD CONSTRAINT ck_voice_consent_evidence__region CHECK (region IN ('IN','EU'));

ALTER TABLE ge.voice_recording ADD CONSTRAINT ck_voice_recording__revision CHECK (revision >= 1);

ALTER TABLE ge.voice_recording ADD CONSTRAINT ck_voice_recording__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.voice_recording ADD CONSTRAINT ck_voice_recording__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.voice_recording ADD CONSTRAINT ck_voice_recording__region CHECK (region IN ('IN','EU'));

ALTER TABLE ge.voice_transcript ADD CONSTRAINT ck_voice_transcript__revision CHECK (revision >= 1);

ALTER TABLE ge.voice_transcript ADD CONSTRAINT ck_voice_transcript__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.voice_transcript ADD CONSTRAINT ck_voice_transcript__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.voice_transcript ADD CONSTRAINT ck_voice_transcript__region CHECK (region IN ('IN','EU'));

ALTER TABLE ge.voice_transcript_segment ADD CONSTRAINT ck_voice_transcript_segment__revision CHECK (revision >= 1);

ALTER TABLE ge.voice_transcript_segment ADD CONSTRAINT ck_voice_transcript_segment__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.voice_transcript_segment ADD CONSTRAINT ck_voice_transcript_segment__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.voice_transcript_segment ADD CONSTRAINT ck_voice_transcript_segment__region CHECK (region IN ('IN','EU'));

ALTER TABLE ge.voice_summary ADD CONSTRAINT ck_voice_summary__revision CHECK (revision >= 1);

ALTER TABLE ge.voice_summary ADD CONSTRAINT ck_voice_summary__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.voice_summary ADD CONSTRAINT ck_voice_summary__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.voice_summary ADD CONSTRAINT ck_voice_summary__region CHECK (region IN ('IN','EU'));

ALTER TABLE ge.voice_handoff ADD CONSTRAINT ck_voice_handoff__revision CHECK (revision >= 1);

ALTER TABLE ge.voice_handoff ADD CONSTRAINT ck_voice_handoff__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.voice_handoff ADD CONSTRAINT ck_voice_handoff__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.voice_handoff ADD CONSTRAINT ck_voice_handoff__region CHECK (region IN ('IN','EU'));

ALTER TABLE ge.voice_voicemail ADD CONSTRAINT ck_voice_voicemail__revision CHECK (revision >= 1);

ALTER TABLE ge.voice_voicemail ADD CONSTRAINT ck_voice_voicemail__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.voice_voicemail ADD CONSTRAINT ck_voice_voicemail__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.voice_voicemail ADD CONSTRAINT ck_voice_voicemail__region CHECK (region IN ('IN','EU'));

ALTER TABLE ge.voice_meter_event ADD CONSTRAINT ck_voice_meter_event__revision CHECK (revision >= 1);

ALTER TABLE ge.voice_meter_event ADD CONSTRAINT ck_voice_meter_event__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.voice_meter_event ADD CONSTRAINT ck_voice_meter_event__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.voice_meter_event ADD CONSTRAINT ck_voice_meter_event__region CHECK (region IN ('IN','EU'));

ALTER TABLE ge.voice_access_log ADD CONSTRAINT ck_voice_access_log__revision CHECK (revision >= 1);

ALTER TABLE ge.voice_access_log ADD CONSTRAINT ck_voice_access_log__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.voice_access_log ADD CONSTRAINT ck_voice_access_log__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.voice_access_log ADD CONSTRAINT ck_voice_access_log__region CHECK (region IN ('IN','EU'));

ALTER TABLE ge.voice_legal_hold ADD CONSTRAINT ck_voice_legal_hold__revision CHECK (revision >= 1);

ALTER TABLE ge.voice_legal_hold ADD CONSTRAINT ck_voice_legal_hold__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.voice_legal_hold ADD CONSTRAINT ck_voice_legal_hold__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.voice_legal_hold ADD CONSTRAINT ck_voice_legal_hold__region CHECK (region IN ('IN','EU'));

ALTER TABLE ge.coaching_rubric ADD CONSTRAINT ck_coaching_rubric__revision CHECK (revision >= 1);

ALTER TABLE ge.coaching_rubric ADD CONSTRAINT ck_coaching_rubric__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.coaching_rubric ADD CONSTRAINT ck_coaching_rubric__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.coaching_rubric ADD CONSTRAINT ck_coaching_rubric__region CHECK (region IN ('IN','EU'));

ALTER TABLE ge.coaching_feedback ADD CONSTRAINT ck_coaching_feedback__revision CHECK (revision >= 1);

ALTER TABLE ge.coaching_feedback ADD CONSTRAINT ck_coaching_feedback__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.coaching_feedback ADD CONSTRAINT ck_coaching_feedback__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.coaching_feedback ADD CONSTRAINT ck_coaching_feedback__region CHECK (region IN ('IN','EU'));

ALTER TABLE ge.coaching_share ADD CONSTRAINT ck_coaching_share__revision CHECK (revision >= 1);

ALTER TABLE ge.coaching_share ADD CONSTRAINT ck_coaching_share__created_by_type CHECK (created_by_type IN ('user','service','ai_agent','provider','anonymous'));

ALTER TABLE ge.coaching_share ADD CONSTRAINT ck_coaching_share__archive_reason CHECK (length(archive_reason) <= 500);

ALTER TABLE ge.coaching_share ADD CONSTRAINT ck_coaching_share__region CHECK (region IN ('IN','EU'));

ALTER TABLE ge.ten_capability_profile ADD CONSTRAINT uq_ten_capability_profile__startup_id_version_no UNIQUE (startup_id, version_no);

ALTER TABLE ge.ten_domain ADD CONSTRAINT uq_ten_domain__hostname UNIQUE (hostname);

ALTER TABLE ge.ten_user ADD CONSTRAINT uq_ten_user__idp_subject UNIQUE (idp_subject);

ALTER TABLE ge.ten_user ADD CONSTRAINT uq_ten_user__email_hmac UNIQUE (email_hmac);

CREATE UNIQUE INDEX IF NOT EXISTS uq_ten_membership__tenant_id_user_id ON ge.ten_membership (tenant_id, user_id) WHERE archived_at IS NULL;

ALTER TABLE ge.ten_membership ADD CONSTRAINT uq_ten_membership__invite_token_hash UNIQUE (invite_token_hash);

CREATE UNIQUE INDEX IF NOT EXISTS uq_ten_portal_grant__subject_user_id_object_type_object_id ON ge.ten_portal_grant (subject_user_id, object_type, object_id) WHERE revoked_at IS NULL;

ALTER TABLE ge.ten_saved_view ADD CONSTRAINT uq_ten_saved_view__user_id_screen_code_name UNIQUE (user_id, screen_code, name);

CREATE UNIQUE INDEX IF NOT EXISTS uq_ref_dataset__tenant_id_code_version_no ON ge.ref_dataset (COALESCE(tenant_id, '00000000-0000-0000-0000-000000000000'::uuid), code, version_no);

ALTER TABLE ge.ref_value ADD CONSTRAINT uq_ref_value__dataset_id_code UNIQUE (dataset_id, code);

ALTER TABLE ge.cat_offering_version ADD CONSTRAINT uq_cat_offering_version__offering_id_version_no UNIQUE (offering_id, version_no);

ALTER TABLE ge.cat_capability ADD CONSTRAINT uq_cat_capability__tenant_id_startup_id_code UNIQUE (tenant_id, startup_id, code);

ALTER TABLE ge.cat_offering_capability ADD CONSTRAINT uq_cat_offering_capability__offering_version_id_capability_id UNIQUE (offering_version_id, capability_id);

ALTER TABLE ge.cat_price_version ADD CONSTRAINT uq_cat_price_version__offering_version_id_price_list_code_curr UNIQUE (offering_version_id, price_list_code, currency, unit_code, version_no);

ALTER TABLE ge.cat_document ADD CONSTRAINT uq_cat_document__storage_key UNIQUE (storage_key);

ALTER TABLE ge.cat_document ADD CONSTRAINT uq_cat_document__tenant_id_startup_id_sha256_version_no UNIQUE (tenant_id, startup_id, sha256, version_no);

ALTER TABLE ge.cat_chunk ADD CONSTRAINT uq_cat_chunk__document_id_ordinal UNIQUE (document_id, ordinal);

ALTER TABLE ge.cat_embedding ADD CONSTRAINT uq_cat_embedding__chunk_id_model_id UNIQUE (chunk_id, model_id);

CREATE UNIQUE INDEX IF NOT EXISTS uq_gov_policy_version__tenant_id_startup_id_policy_code_version ON ge.gov_policy_version (COALESCE(tenant_id, '00000000-0000-0000-0000-000000000000'::uuid), COALESCE(startup_id, '00000000-0000-0000-0000-000000000000'::uuid), policy_code, version_no);

CREATE UNIQUE INDEX IF NOT EXISTS uq_gov_approval_policy__tenant_id_startup_id_policy_kind_versio ON ge.gov_approval_policy (tenant_id, COALESCE(startup_id, '00000000-0000-0000-0000-000000000000'::uuid), policy_kind, version_no);

CREATE UNIQUE INDEX IF NOT EXISTS uq_gov_retention_policy__tenant_id_data_class_version_no ON ge.gov_retention_policy (COALESCE(tenant_id, '00000000-0000-0000-0000-000000000000'::uuid), data_class, version_no);

ALTER TABLE ge.int_credential_ref ADD CONSTRAINT uq_int_credential_ref__integration_id UNIQUE (integration_id);

CREATE UNIQUE INDEX IF NOT EXISTS uq_ai_agent_definition__tenant_id_agent_code_version_no ON ge.ai_agent_definition (COALESCE(tenant_id, '00000000-0000-0000-0000-000000000000'::uuid), agent_code, version_no);

ALTER TABLE ge.intel_source ADD CONSTRAINT uq_intel_source__tenant_id_startup_id_host_path_prefix UNIQUE (tenant_id, startup_id, host, path_prefix);

ALTER TABLE ge.intel_source_policy ADD CONSTRAINT uq_intel_source_policy__source_id_version_no UNIQUE (source_id, version_no);

ALTER TABLE ge.intel_source_record ADD CONSTRAINT uq_intel_source_record__tenant_id_startup_id_url_hash UNIQUE (tenant_id, startup_id, url_hash);

ALTER TABLE ge.intel_evidence ADD CONSTRAINT uq_intel_evidence__tenant_id_startup_id_content_hash_organi UNIQUE (tenant_id, startup_id, content_hash, organization_id);

ALTER TABLE ge.intel_social_post ADD CONSTRAINT uq_intel_social_post__tenant_id_startup_id_platform_post_ref UNIQUE (tenant_id, startup_id, platform, post_ref);

CREATE UNIQUE INDEX IF NOT EXISTS uq_intel_organization__tenant_id_startup_id_primary_domain ON ge.intel_organization (tenant_id, startup_id, primary_domain) WHERE merged_into_id IS NULL AND archived_at IS NULL;

CREATE UNIQUE INDEX IF NOT EXISTS uq_intel_alias__organization_id_loweralias_name ON ge.intel_alias (organization_id, lower(alias_name));

CREATE UNIQUE INDEX IF NOT EXISTS uq_intel_signal_type__tenant_id_code ON ge.intel_signal_type (COALESCE(tenant_id, '00000000-0000-0000-0000-000000000000'::uuid), code);

ALTER TABLE ge.intel_need_evidence ADD CONSTRAINT uq_intel_need_evidence__need_id_evidence_id UNIQUE (need_id, evidence_id);

ALTER TABLE ge.intel_match ADD CONSTRAINT uq_intel_match__need_id_offering_version_id UNIQUE (need_id, offering_version_id);

CREATE UNIQUE INDEX IF NOT EXISTS uq_intel_contact__tenant_id_startup_id_email_hmac ON ge.intel_contact (tenant_id, startup_id, email_hmac) WHERE archived_at IS NULL;

ALTER TABLE ge.crm_form ADD CONSTRAINT uq_crm_form__tenant_id_startup_id_form_code UNIQUE (tenant_id, startup_id, form_code);

ALTER TABLE ge.crm_form_version ADD CONSTRAINT uq_crm_form_version__form_id_version_no UNIQUE (form_id, version_no);

ALTER TABLE ge.crm_submission ADD CONSTRAINT uq_crm_submission__tenant_id_startup_id_form_version_id_ide UNIQUE (tenant_id, startup_id, form_version_id, idempotency_key);

ALTER TABLE ge.crm_pipeline ADD CONSTRAINT uq_crm_pipeline__tenant_id_startup_id_opportunity_type_ve UNIQUE (tenant_id, startup_id, opportunity_type, version_no);

ALTER TABLE ge.crm_stage ADD CONSTRAINT uq_crm_stage__pipeline_id_code UNIQUE (pipeline_id, code);

ALTER TABLE ge.crm_stage ADD CONSTRAINT uq_crm_stage__pipeline_id_ordinal UNIQUE (pipeline_id, ordinal);

ALTER TABLE ge.crm_deal ADD CONSTRAINT uq_crm_deal__tenant_id_startup_id_deal_no UNIQUE (tenant_id, startup_id, deal_no);

ALTER TABLE ge.eng_delivery_event ADD CONSTRAINT uq_eng_delivery_event__channel_account_id_provider_event_id_occ UNIQUE (channel_account_id, provider_event_id, occurred_at);

ALTER TABLE ge.eng_inbound_event ADD CONSTRAINT uq_eng_inbound_event__channel_account_id_provider_message_id UNIQUE (channel_account_id, provider_message_id);

ALTER TABLE ge.eng_identity_link ADD CONSTRAINT uq_eng_identity_link__tenant_id_startup_id_channel_address_hma UNIQUE (tenant_id, startup_id, channel, address_hmac);

ALTER TABLE ge.eng_routing_rule ADD CONSTRAINT uq_eng_routing_rule__startup_id_priority_version_no UNIQUE (startup_id, priority, version_no);

ALTER TABLE ge.eng_sequence ADD CONSTRAINT uq_eng_sequence__tenant_id_startup_id_code_version_no UNIQUE (tenant_id, startup_id, code, version_no);

ALTER TABLE ge.eng_sequence_step ADD CONSTRAINT uq_eng_sequence_step__sequence_id_ordinal UNIQUE (sequence_id, ordinal);

ALTER TABLE ge.eng_meeting ADD CONSTRAINT uq_eng_meeting__calendar_link_id_provider_event_ref UNIQUE (calendar_link_id, provider_event_ref);

ALTER TABLE ge.eng_calendar_link ADD CONSTRAINT uq_eng_calendar_link__user_id_provider UNIQUE (user_id, provider);

ALTER TABLE ge.mkt_social_publication ADD CONSTRAINT uq_mkt_social_publication__channel_account_id_idempotency_key UNIQUE (channel_account_id, idempotency_key);

ALTER TABLE ge.mkt_social_publication ADD CONSTRAINT uq_mkt_social_publication__channel_account_id_provider_post_id UNIQUE (channel_account_id, provider_post_id);

CREATE UNIQUE INDEX IF NOT EXISTS uq_mkt_keyword__startup_id_lowerphrase_locale ON ge.mkt_keyword (startup_id, lower(phrase), locale);

CREATE UNIQUE INDEX IF NOT EXISTS uq_mkt_page_metric__page_id_keyword_id_metric_date_source ON ge.mkt_page_metric (page_id, COALESCE(keyword_id, '00000000-0000-0000-0000-000000000000'::uuid), metric_date, source);

ALTER TABLE ge.mkt_landing_page ADD CONSTRAINT uq_mkt_landing_page__tenant_id_startup_id_slug_locale UNIQUE (tenant_id, startup_id, slug, locale);

ALTER TABLE ge.mkt_publication ADD CONSTRAINT uq_mkt_publication__domain_id_path_locale UNIQUE (domain_id, path, locale);

ALTER TABLE ge.mkt_publication_snapshot ADD CONSTRAINT uq_mkt_publication_snapshot__publication_id_snapshot_hash UNIQUE (publication_id, snapshot_hash);

ALTER TABLE ge.mkt_preview_grant ADD CONSTRAINT uq_mkt_preview_grant__token_hash UNIQUE (token_hash);

ALTER TABLE ge.mkt_campaign_version ADD CONSTRAINT uq_mkt_campaign_version__campaign_id_version_no UNIQUE (campaign_id, version_no);

ALTER TABLE ge.mkt_ad_campaign ADD CONSTRAINT uq_mkt_ad_campaign__platform_provider_campaign_id UNIQUE (platform, provider_campaign_id);

ALTER TABLE ge.mkt_spend_event ADD CONSTRAINT uq_mkt_spend_event__ad_campaign_id_spend_date_provider_repor UNIQUE (ad_campaign_id, spend_date, provider_report_id);

ALTER TABLE ge.mkt_registration ADD CONSTRAINT uq_mkt_registration__event_id_contact_id UNIQUE (event_id, contact_id);

ALTER TABLE ge.mkt_attendance ADD CONSTRAINT uq_mkt_attendance__registration_id_source UNIQUE (registration_id, source);

ALTER TABLE ge.mkt_referral ADD CONSTRAINT uq_mkt_referral__tenant_id_referral_code UNIQUE (tenant_id, referral_code);

ALTER TABLE ge.com_proposal ADD CONSTRAINT uq_com_proposal__tenant_id_startup_id_proposal_no UNIQUE (tenant_id, startup_id, proposal_no);

ALTER TABLE ge.com_proposal_version ADD CONSTRAINT uq_com_proposal_version__proposal_id_version_no UNIQUE (proposal_id, version_no);

ALTER TABLE ge.com_quote ADD CONSTRAINT uq_com_quote__tenant_id_startup_id_quote_no_quote_revi UNIQUE (tenant_id, startup_id, quote_no, quote_revision);

ALTER TABLE ge.com_quote_line ADD CONSTRAINT uq_com_quote_line__quote_id_line_no UNIQUE (quote_id, line_no);

ALTER TABLE ge.com_negotiation ADD CONSTRAINT uq_com_negotiation__deal_id UNIQUE (deal_id);

ALTER TABLE ge.com_contract ADD CONSTRAINT uq_com_contract__tenant_id_startup_id_contract_no UNIQUE (tenant_id, startup_id, contract_no);

ALTER TABLE ge.com_signature_event ADD CONSTRAINT uq_com_signature_event__provider_account_provider_event_id UNIQUE (provider_account, provider_event_id);

ALTER TABLE ge.com_bid ADD CONSTRAINT uq_com_bid__tenant_id_startup_id_portal_code_tender_ UNIQUE (tenant_id, startup_id, portal_code, tender_ref);

ALTER TABLE ge.com_bid_checklist_item ADD CONSTRAINT uq_com_bid_checklist_item__bid_id_criterion_code UNIQUE (bid_id, criterion_code);

ALTER TABLE ge.com_order ADD CONSTRAINT uq_com_order__tenant_id_startup_id_order_no UNIQUE (tenant_id, startup_id, order_no);

ALTER TABLE ge.com_order_line ADD CONSTRAINT uq_com_order_line__order_id_line_no UNIQUE (order_id, line_no);

ALTER TABLE ge.com_fulfillment_event ADD CONSTRAINT uq_com_fulfillment_event__tenant_id_startup_id_order_line_id_event UNIQUE (tenant_id, startup_id, order_line_id, event_key);

ALTER TABLE ge.com_sku_availability ADD CONSTRAINT uq_com_sku_availability__tenant_id_startup_id_sku_code UNIQUE (tenant_id, startup_id, sku_code);

CREATE UNIQUE INDEX IF NOT EXISTS uq_com_inventory_reservation__order_line_id ON ge.com_inventory_reservation (order_line_id) WHERE state = 'held';

ALTER TABLE ge.com_invoice ADD CONSTRAINT uq_com_invoice__tenant_id_startup_id_invoice_no UNIQUE (tenant_id, startup_id, invoice_no);

ALTER TABLE ge.com_invoice_line ADD CONSTRAINT uq_com_invoice_line__invoice_id_line_no UNIQUE (invoice_id, line_no);

ALTER TABLE ge.com_payment ADD CONSTRAINT uq_com_payment__tenant_id_provider_account_provider_paym UNIQUE (tenant_id, provider_account, provider_payment_id);

ALTER TABLE ge.com_receivable_entry ADD CONSTRAINT uq_com_receivable_entry__tenant_id_startup_id_entry_seq UNIQUE (tenant_id, startup_id, entry_seq);

ALTER TABLE ge.com_payable_entry ADD CONSTRAINT uq_com_payable_entry__tenant_id_startup_id_entry_seq UNIQUE (tenant_id, startup_id, entry_seq);

ALTER TABLE ge.lcy_renewal ADD CONSTRAINT uq_lcy_renewal__customer_subscription_id_due_date UNIQUE (customer_subscription_id, due_date);

ALTER TABLE ge.lcy_account_metric ADD CONSTRAINT uq_lcy_account_metric__organization_id_metric_code_as_of_date UNIQUE (organization_id, metric_code, as_of_date);

ALTER TABLE ge.lcy_partner ADD CONSTRAINT uq_lcy_partner__tenant_id_startup_id_organization_id_par UNIQUE (tenant_id, startup_id, organization_id, partner_type);

ALTER TABLE ge.lcy_outcome ADD CONSTRAINT uq_lcy_outcome__subject_type_subject_id_outcome_code UNIQUE (subject_type, subject_id, outcome_code);

ALTER TABLE ge.aut_workflow ADD CONSTRAINT uq_aut_workflow__tenant_id_startup_id_workflow_code UNIQUE (tenant_id, startup_id, workflow_code);

ALTER TABLE ge.aut_workflow_revision ADD CONSTRAINT uq_aut_workflow_revision__workflow_id_version_no UNIQUE (workflow_id, version_no);

ALTER TABLE ge.aut_conflict_case ADD CONSTRAINT uq_aut_conflict_case__tenant_id_startup_id_duplicate_key UNIQUE (tenant_id, startup_id, duplicate_key);

CREATE UNIQUE INDEX IF NOT EXISTS uq_aut_node_template__tenant_id_node_type_version_no ON ge.aut_node_template (COALESCE(tenant_id, '00000000-0000-0000-0000-000000000000'::uuid), node_type, version_no);

CREATE UNIQUE INDEX IF NOT EXISTS uq_aut_workflow_template__tenant_id_template_code_version_no ON ge.aut_workflow_template (COALESCE(tenant_id, '00000000-0000-0000-0000-000000000000'::uuid), template_code, version_no);

ALTER TABLE ge.ops_idempotency_key ADD CONSTRAINT uq_ops_idempotency_key__tenant_id_startup_id_scope_key_key_value UNIQUE (tenant_id, startup_id, scope_key, key_value);

ALTER TABLE ge.ops_notification ADD CONSTRAINT uq_ops_notification__recipient_id_dedup_key UNIQUE (recipient_id, dedup_key);

ALTER TABLE ge.ops_notification_preference ADD CONSTRAINT uq_ops_notification_preference__user_id_category_channel UNIQUE (user_id, category, channel);

ALTER TABLE ge.ops_release ADD CONSTRAINT uq_ops_release__version_tag UNIQUE (version_tag);

ALTER TABLE ge.saas_plan ADD CONSTRAINT uq_saas_plan__code UNIQUE (code);

ALTER TABLE ge.saas_plan_version ADD CONSTRAINT uq_saas_plan_version__plan_id_version_no UNIQUE (plan_id, version_no);

ALTER TABLE ge.saas_service_invoice_line ADD CONSTRAINT uq_saas_service_invoice_line__service_invoice_id_line_kind_meter_code UNIQUE (service_invoice_id, line_kind, meter_code);

ALTER TABLE ge.saas_application_draft ADD CONSTRAINT uq_saas_application_draft__provisioned_tenant_id UNIQUE (provisioned_tenant_id);

ALTER TABLE ge.saas_import_job ADD CONSTRAINT uq_saas_import_job__tenant_id_startup_id_source_sha256_templ UNIQUE (tenant_id, startup_id, source_sha256, template_code);

CREATE UNIQUE INDEX IF NOT EXISTS uq_ana_metric_definition__tenant_id_metric_code_version_no ON ge.ana_metric_definition (COALESCE(tenant_id, '00000000-0000-0000-0000-000000000000'::uuid), metric_code, version_no);

ALTER TABLE ge.ana_metric_snapshot ADD CONSTRAINT uq_ana_metric_snapshot__metric_definition_id_startup_id_period_s UNIQUE (metric_definition_id, startup_id, period_start, period_end, as_of);

ALTER TABLE ge.ana_account_projection ADD CONSTRAINT uq_ana_account_projection__startup_id_organization_id UNIQUE (startup_id, organization_id);

ALTER TABLE ge.ana_pipeline_projection ADD CONSTRAINT uq_ana_pipeline_projection__deal_id UNIQUE (deal_id);

ALTER TABLE ge.ten_membership_grant ADD CONSTRAINT uq_ten_membership_grant__membership_id_role_id_startup_id UNIQUE (membership_id, role_id, startup_id);

ALTER TABLE ge.cat_document_offering ADD CONSTRAINT uq_cat_document_offering__document_id_offering_version_id UNIQUE (document_id, offering_version_id);

ALTER TABLE ge.cat_claim_evidence ADD CONSTRAINT uq_cat_claim_evidence__claim_id_evidence_ref UNIQUE (claim_id, evidence_ref);

ALTER TABLE ge.intel_signal_evidence ADD CONSTRAINT uq_intel_signal_evidence__signal_id_evidence_id UNIQUE (signal_id, evidence_id);

ALTER TABLE ge.intel_opportunity_contact ADD CONSTRAINT uq_intel_opportunity_contact__opportunity_id_contact_id UNIQUE (opportunity_id, contact_id);

ALTER TABLE ge.crm_deal_contact ADD CONSTRAINT uq_crm_deal_contact__deal_id_contact_id_role_code UNIQUE (deal_id, contact_id, role_code);

ALTER TABLE ge.eng_message_claim ADD CONSTRAINT uq_eng_message_claim__message_id_claim_id UNIQUE (message_id, claim_id);

ALTER TABLE ge.mkt_content_claim ADD CONSTRAINT uq_mkt_content_claim__content_version_id_claim_id UNIQUE (content_version_id, claim_id);

ALTER TABLE ge.mkt_audience_member ADD CONSTRAINT uq_mkt_audience_member__audience_id_contact_id UNIQUE (audience_id, contact_id);

ALTER TABLE ge.com_contract_party ADD CONSTRAINT uq_com_contract_party__contract_id_party_ref_party_role UNIQUE (contract_id, party_ref, party_role);

ALTER TABLE ge.aut_run_conflict ADD CONSTRAINT uq_aut_run_conflict__run_id_conflict_case_id UNIQUE (run_id, conflict_case_id);

ALTER TABLE ge.saas_plan_entitlement ADD CONSTRAINT uq_saas_plan_entitlement__plan_version_id_entitlement_id UNIQUE (plan_version_id, entitlement_id);

ALTER TABLE ge.lcy_onboarding_task ADD CONSTRAINT uq_lcy_onboarding_task__onboarding_id_task_id UNIQUE (onboarding_id, task_id);

ALTER TABLE ge.saas_service_request ADD CONSTRAINT uq_saas_service_request__tenant_id_request_no UNIQUE (tenant_id, request_no);

ALTER TABLE ge.com_fulfillment_milestone ADD CONSTRAINT uq_com_fulfillment_milestone__tenant_id_startup_id_order_id_milestone_ UNIQUE (tenant_id, startup_id, order_id, milestone_key);

ALTER TABLE ge.ai_eval_case_result ADD CONSTRAINT uq_ai_eval_case_result__eval_run_id_eval_case_id UNIQUE (eval_run_id, eval_case_id);

ALTER TABLE ge.ten_portal_grant ADD CONSTRAINT uq_ten_portal_grant__invite_token_hash UNIQUE (invite_token_hash);

ALTER TABLE ge.eng_chat_session ADD CONSTRAINT uq_eng_chat_session__session_token_hash UNIQUE (session_token_hash);

ALTER TABLE ge.saas_application_draft ADD CONSTRAINT uq_saas_application_draft__application_ref UNIQUE (application_ref);

ALTER TABLE ge.ten_capability_profile ADD CONSTRAINT fk_ten_capability_profile__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.ten_domain ADD CONSTRAINT fk_ten_domain__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.ten_membership ADD CONSTRAINT fk_ten_membership__user_id FOREIGN KEY (user_id) REFERENCES ge.ten_user (id) ON DELETE RESTRICT;

ALTER TABLE ge.ten_membership ADD CONSTRAINT fk_ten_membership__invited_by FOREIGN KEY (invited_by) REFERENCES ge.ten_user (id) ON DELETE RESTRICT;

ALTER TABLE ge.ten_membership ADD CONSTRAINT fk_ten_membership__tenant_id FOREIGN KEY (tenant_id) REFERENCES ge.tenant (tenant_id) ON DELETE RESTRICT;

ALTER TABLE ge.ten_membership ADD CONSTRAINT fk_ten_membership__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.ten_portal_grant ADD CONSTRAINT fk_ten_portal_grant__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.ten_saved_view ADD CONSTRAINT fk_ten_saved_view__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.ref_dataset ADD CONSTRAINT fk_ref_dataset__tenant_id FOREIGN KEY (tenant_id) REFERENCES ge.tenant (tenant_id) ON DELETE RESTRICT;

ALTER TABLE ge.ref_dataset ADD CONSTRAINT fk_ref_dataset__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.ref_value ADD CONSTRAINT fk_ref_value__tenant_id FOREIGN KEY (tenant_id) REFERENCES ge.tenant (tenant_id) ON DELETE RESTRICT;

ALTER TABLE ge.ref_value ADD CONSTRAINT fk_ref_value__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.ref_unit ADD CONSTRAINT fk_ref_unit__tenant_id FOREIGN KEY (tenant_id) REFERENCES ge.tenant (tenant_id) ON DELETE RESTRICT;

ALTER TABLE ge.ref_unit ADD CONSTRAINT fk_ref_unit__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.offering ADD CONSTRAINT uq_offering__offering_id UNIQUE (offering_id);

ALTER TABLE ge.cat_offering_version ADD CONSTRAINT fk_cat_offering_version__offering_id FOREIGN KEY (offering_id) REFERENCES ge.offering (offering_id) ON DELETE RESTRICT;

ALTER TABLE ge.cat_offering_version ADD CONSTRAINT fk_cat_offering_version__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.cat_capability ADD CONSTRAINT fk_cat_capability__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.cat_offering_capability ADD CONSTRAINT fk_cat_offering_capability__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.cat_claim ADD CONSTRAINT fk_cat_claim__offering_version_id FOREIGN KEY (offering_version_id) REFERENCES ge.cat_offering_version (id) ON DELETE RESTRICT;

ALTER TABLE ge.consent_record ADD CONSTRAINT uq_consent_record__consent_id UNIQUE (consent_id);

ALTER TABLE ge.cat_claim ADD CONSTRAINT fk_cat_claim__subject_consent_ref FOREIGN KEY (subject_consent_ref) REFERENCES ge.consent_record (consent_id) ON DELETE RESTRICT;

ALTER TABLE ge.cat_claim ADD CONSTRAINT fk_cat_claim__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.cat_price_version ADD CONSTRAINT fk_cat_price_version__offering_version_id FOREIGN KEY (offering_version_id) REFERENCES ge.cat_offering_version (id) ON DELETE RESTRICT;

ALTER TABLE ge.ref_currency ADD CONSTRAINT uq_ref_currency__code UNIQUE (code);

ALTER TABLE ge.cat_price_version ADD CONSTRAINT fk_cat_price_version__currency FOREIGN KEY (currency) REFERENCES ge.ref_currency (code) ON DELETE RESTRICT;

ALTER TABLE ge.ref_unit ADD CONSTRAINT uq_ref_unit__code UNIQUE (code);

ALTER TABLE ge.cat_price_version ADD CONSTRAINT fk_cat_price_version__unit_code FOREIGN KEY (unit_code) REFERENCES ge.ref_unit (code) ON DELETE RESTRICT;

ALTER TABLE ge.cat_price_version ADD CONSTRAINT fk_cat_price_version__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.cat_launch_approval ADD CONSTRAINT fk_cat_launch_approval__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.cat_document ADD CONSTRAINT fk_cat_document__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.cat_chunk ADD CONSTRAINT fk_cat_chunk__document_id FOREIGN KEY (document_id) REFERENCES ge.cat_document (id) ON DELETE RESTRICT;

ALTER TABLE ge.cat_chunk ADD CONSTRAINT fk_cat_chunk__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.cat_embedding ADD CONSTRAINT fk_cat_embedding__chunk_id FOREIGN KEY (chunk_id) REFERENCES ge.cat_chunk (id) ON DELETE RESTRICT;

ALTER TABLE ge.cat_embedding ADD CONSTRAINT fk_cat_embedding__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.gov_policy_version ADD CONSTRAINT fk_gov_policy_version__simulation_report_ref FOREIGN KEY (simulation_report_ref) REFERENCES ge.aut_config_revision (id) ON DELETE RESTRICT;

ALTER TABLE ge.gov_policy_version ADD CONSTRAINT fk_gov_policy_version__tenant_id FOREIGN KEY (tenant_id) REFERENCES ge.tenant (tenant_id) ON DELETE RESTRICT;

ALTER TABLE ge.gov_policy_version ADD CONSTRAINT fk_gov_policy_version__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.gov_eligibility_decision ADD CONSTRAINT fk_gov_eligibility_decision__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.gov_policy_decision ADD CONSTRAINT fk_gov_policy_decision__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.gov_approval_policy ADD CONSTRAINT fk_gov_approval_policy__tenant_id FOREIGN KEY (tenant_id) REFERENCES ge.tenant (tenant_id) ON DELETE RESTRICT;

ALTER TABLE ge.gov_approval_policy ADD CONSTRAINT fk_gov_approval_policy__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.gov_approval ADD CONSTRAINT fk_gov_approval__approver_id FOREIGN KEY (approver_id) REFERENCES ge.ten_user (id) ON DELETE RESTRICT;

ALTER TABLE ge.gov_approval ADD CONSTRAINT fk_gov_approval__delegation_id FOREIGN KEY (delegation_id) REFERENCES ge.gov_approval_delegation (id) ON DELETE RESTRICT;

ALTER TABLE ge.gov_approval ADD CONSTRAINT fk_gov_approval__revokes_id FOREIGN KEY (revokes_id) REFERENCES ge.gov_approval (id) ON DELETE RESTRICT;

ALTER TABLE ge.gov_approval ADD CONSTRAINT fk_gov_approval__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.gov_approval_delegation ADD CONSTRAINT fk_gov_approval_delegation__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.gov_retention_policy ADD CONSTRAINT fk_gov_retention_policy__tenant_id FOREIGN KEY (tenant_id) REFERENCES ge.tenant (tenant_id) ON DELETE RESTRICT;

ALTER TABLE ge.gov_retention_policy ADD CONSTRAINT fk_gov_retention_policy__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.gov_legal_hold ADD CONSTRAINT fk_gov_legal_hold__tenant_id FOREIGN KEY (tenant_id) REFERENCES ge.tenant (tenant_id) ON DELETE RESTRICT;

ALTER TABLE ge.gov_legal_hold ADD CONSTRAINT fk_gov_legal_hold__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.int_credential_ref ADD CONSTRAINT fk_int_credential_ref__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.int_quota ADD CONSTRAINT fk_int_quota__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.int_provider_event ADD CONSTRAINT fk_int_provider_event__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.ai_agent_definition ADD CONSTRAINT fk_ai_agent_definition__tenant_id FOREIGN KEY (tenant_id) REFERENCES ge.tenant (tenant_id) ON DELETE RESTRICT;

ALTER TABLE ge.ai_agent_definition ADD CONSTRAINT fk_ai_agent_definition__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.ai_model_run ADD CONSTRAINT fk_ai_model_run__agent_id FOREIGN KEY (agent_id) REFERENCES ge.ai_agent_definition (id) ON DELETE RESTRICT;

ALTER TABLE ge.ai_model_run ADD CONSTRAINT fk_ai_model_run__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.ai_eval_case ADD CONSTRAINT fk_ai_eval_case__tenant_id FOREIGN KEY (tenant_id) REFERENCES ge.tenant (tenant_id) ON DELETE RESTRICT;

ALTER TABLE ge.ai_eval_case ADD CONSTRAINT fk_ai_eval_case__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.ai_feedback ADD CONSTRAINT fk_ai_feedback__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.ai_cost_ledger ADD CONSTRAINT fk_ai_cost_ledger__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.intel_source ADD CONSTRAINT fk_intel_source__active_policy_id FOREIGN KEY (active_policy_id) REFERENCES ge.intel_source_policy (id) ON DELETE RESTRICT;

ALTER TABLE ge.intel_source ADD CONSTRAINT fk_intel_source__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.intel_source_policy ADD CONSTRAINT fk_intel_source_policy__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.intel_search_plan ADD CONSTRAINT fk_intel_search_plan__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.intel_query_run ADD CONSTRAINT fk_intel_query_run__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.intel_source_record ADD CONSTRAINT fk_intel_source_record__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.intel_fetch_log ADD CONSTRAINT fk_intel_fetch_log__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.intel_evidence ADD CONSTRAINT fk_intel_evidence__source_record_id FOREIGN KEY (source_record_id) REFERENCES ge.intel_source_record (id) ON DELETE RESTRICT;

ALTER TABLE ge.intel_evidence ADD CONSTRAINT fk_intel_evidence__social_post_id FOREIGN KEY (social_post_id) REFERENCES ge.intel_social_post (id) ON DELETE RESTRICT;

ALTER TABLE ge.intel_evidence ADD CONSTRAINT fk_intel_evidence__organization_id FOREIGN KEY (organization_id) REFERENCES ge.intel_organization (id) ON DELETE RESTRICT;

ALTER TABLE ge.intel_evidence ADD CONSTRAINT fk_intel_evidence__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.intel_social_post ADD CONSTRAINT fk_intel_social_post__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.intel_competitor ADD CONSTRAINT fk_intel_competitor__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.intel_market_event ADD CONSTRAINT fk_intel_market_event__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.ref_country ADD CONSTRAINT uq_ref_country__code UNIQUE (code);

ALTER TABLE ge.intel_organization ADD CONSTRAINT fk_intel_organization__country_code FOREIGN KEY (country_code) REFERENCES ge.ref_country (code) ON DELETE RESTRICT;

ALTER TABLE ge.intel_organization ADD CONSTRAINT fk_intel_organization__owner_id FOREIGN KEY (owner_id) REFERENCES ge.ten_user (id) ON DELETE RESTRICT;

ALTER TABLE ge.intel_organization ADD CONSTRAINT fk_intel_organization__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.intel_location ADD CONSTRAINT fk_intel_location__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.intel_alias ADD CONSTRAINT fk_intel_alias__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.intel_signal_type ADD CONSTRAINT fk_intel_signal_type__tenant_id FOREIGN KEY (tenant_id) REFERENCES ge.tenant (tenant_id) ON DELETE RESTRICT;

ALTER TABLE ge.intel_signal_type ADD CONSTRAINT fk_intel_signal_type__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.intel_signal ADD CONSTRAINT fk_intel_signal__signal_type_id FOREIGN KEY (signal_type_id) REFERENCES ge.intel_signal_type (id) ON DELETE RESTRICT;

ALTER TABLE ge.intel_signal ADD CONSTRAINT fk_intel_signal__organization_id FOREIGN KEY (organization_id) REFERENCES ge.intel_organization (id) ON DELETE RESTRICT;

ALTER TABLE ge.intel_signal ADD CONSTRAINT fk_intel_signal__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.intel_need ADD CONSTRAINT fk_intel_need__organization_id FOREIGN KEY (organization_id) REFERENCES ge.intel_organization (id) ON DELETE RESTRICT;

ALTER TABLE ge.intel_need ADD CONSTRAINT fk_intel_need__source_signal_id FOREIGN KEY (source_signal_id) REFERENCES ge.intel_signal (id) ON DELETE RESTRICT;

ALTER TABLE ge.intel_need ADD CONSTRAINT fk_intel_need__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.intel_need_evidence ADD CONSTRAINT fk_intel_need_evidence__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.intel_match ADD CONSTRAINT fk_intel_match__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.intel_scoring_model ADD CONSTRAINT fk_intel_scoring_model__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.intel_opportunity ADD CONSTRAINT fk_intel_opportunity__organization_id FOREIGN KEY (organization_id) REFERENCES ge.intel_organization (id) ON DELETE RESTRICT;

ALTER TABLE ge.intel_opportunity ADD CONSTRAINT fk_intel_opportunity__offering_id FOREIGN KEY (offering_id) REFERENCES ge.offering (offering_id) ON DELETE RESTRICT;

ALTER TABLE ge.intel_opportunity ADD CONSTRAINT fk_intel_opportunity__match_id FOREIGN KEY (match_id) REFERENCES ge.intel_match (id) ON DELETE RESTRICT;

ALTER TABLE ge.intel_opportunity ADD CONSTRAINT fk_intel_opportunity__need_id FOREIGN KEY (need_id) REFERENCES ge.intel_need (id) ON DELETE RESTRICT;

ALTER TABLE ge.intel_opportunity ADD CONSTRAINT fk_intel_opportunity__current_score_version_id FOREIGN KEY (current_score_version_id) REFERENCES ge.intel_score_version (id) ON DELETE RESTRICT;

ALTER TABLE ge.intel_opportunity ADD CONSTRAINT fk_intel_opportunity__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.intel_score_version ADD CONSTRAINT fk_intel_score_version__opportunity_id FOREIGN KEY (opportunity_id) REFERENCES ge.intel_opportunity (id) ON DELETE RESTRICT;

ALTER TABLE ge.intel_score_version ADD CONSTRAINT fk_intel_score_version__scoring_model_id FOREIGN KEY (scoring_model_id) REFERENCES ge.intel_scoring_model (id) ON DELETE RESTRICT;

ALTER TABLE ge.intel_score_version ADD CONSTRAINT fk_intel_score_version__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.intel_contact ADD CONSTRAINT fk_intel_contact__organization_id FOREIGN KEY (organization_id) REFERENCES ge.intel_organization (id) ON DELETE RESTRICT;

ALTER TABLE ge.intel_contact ADD CONSTRAINT fk_intel_contact__country_code FOREIGN KEY (country_code) REFERENCES ge.ref_country (code) ON DELETE RESTRICT;

ALTER TABLE ge.intel_contact ADD CONSTRAINT fk_intel_contact__import_job_id FOREIGN KEY (import_job_id) REFERENCES ge.saas_import_job (id) ON DELETE RESTRICT;

ALTER TABLE ge.intel_contact ADD CONSTRAINT fk_intel_contact__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.intel_role_hypothesis ADD CONSTRAINT fk_intel_role_hypothesis__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.intel_contact_source ADD CONSTRAINT fk_intel_contact_source__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.intel_contact_verification ADD CONSTRAINT fk_intel_contact_verification__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.intel_review ADD CONSTRAINT fk_intel_review__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.crm_lead ADD CONSTRAINT fk_crm_lead__submission_id FOREIGN KEY (submission_id) REFERENCES ge.crm_submission (id) ON DELETE RESTRICT;

ALTER TABLE ge.crm_lead ADD CONSTRAINT fk_crm_lead__contact_id FOREIGN KEY (contact_id) REFERENCES ge.intel_contact (id) ON DELETE RESTRICT;

ALTER TABLE ge.crm_lead ADD CONSTRAINT fk_crm_lead__organization_id FOREIGN KEY (organization_id) REFERENCES ge.intel_organization (id) ON DELETE RESTRICT;

ALTER TABLE ge.crm_lead ADD CONSTRAINT fk_crm_lead__consent_id FOREIGN KEY (consent_id) REFERENCES ge.consent_record (consent_id) ON DELETE RESTRICT;

ALTER TABLE ge.crm_lead ADD CONSTRAINT fk_crm_lead__opportunity_id FOREIGN KEY (opportunity_id) REFERENCES ge.intel_opportunity (id) ON DELETE RESTRICT;

ALTER TABLE ge.crm_lead ADD CONSTRAINT fk_crm_lead__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.crm_form ADD CONSTRAINT fk_crm_form__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.crm_form_version ADD CONSTRAINT fk_crm_form_version__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.crm_submission ADD CONSTRAINT fk_crm_submission__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.crm_pipeline ADD CONSTRAINT fk_crm_pipeline__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.crm_stage ADD CONSTRAINT fk_crm_stage__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.crm_closure_policy ADD CONSTRAINT fk_crm_closure_policy__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.crm_deal ADD CONSTRAINT fk_crm_deal__opportunity_id FOREIGN KEY (opportunity_id) REFERENCES ge.intel_opportunity (id) ON DELETE RESTRICT;

ALTER TABLE ge.crm_deal ADD CONSTRAINT fk_crm_deal__organization_id FOREIGN KEY (organization_id) REFERENCES ge.intel_organization (id) ON DELETE RESTRICT;

ALTER TABLE ge.crm_deal ADD CONSTRAINT fk_crm_deal__offering_id FOREIGN KEY (offering_id) REFERENCES ge.offering (offering_id) ON DELETE RESTRICT;

ALTER TABLE ge.crm_deal ADD CONSTRAINT fk_crm_deal__pipeline_id FOREIGN KEY (pipeline_id) REFERENCES ge.crm_pipeline (id) ON DELETE RESTRICT;

ALTER TABLE ge.crm_deal ADD CONSTRAINT fk_crm_deal__stage_id FOREIGN KEY (stage_id) REFERENCES ge.crm_stage (id) ON DELETE RESTRICT;

ALTER TABLE ge.crm_deal ADD CONSTRAINT fk_crm_deal__owner_id FOREIGN KEY (owner_id) REFERENCES ge.ten_user (id) ON DELETE RESTRICT;

ALTER TABLE ge.crm_deal ADD CONSTRAINT fk_crm_deal__currency FOREIGN KEY (currency) REFERENCES ge.ref_currency (code) ON DELETE RESTRICT;

ALTER TABLE ge.crm_deal ADD CONSTRAINT fk_crm_deal__accepted_quote_id FOREIGN KEY (accepted_quote_id) REFERENCES ge.com_quote (id) ON DELETE RESTRICT DEFERRABLE INITIALLY DEFERRED;

ALTER TABLE ge.crm_deal ADD CONSTRAINT fk_crm_deal__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.crm_stage_transition ADD CONSTRAINT fk_crm_stage_transition__deal_id FOREIGN KEY (deal_id) REFERENCES ge.crm_deal (id) ON DELETE RESTRICT;

ALTER TABLE ge.crm_stage_transition ADD CONSTRAINT fk_crm_stage_transition__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.crm_activity ADD CONSTRAINT fk_crm_activity__organization_id FOREIGN KEY (organization_id) REFERENCES ge.intel_organization (id) ON DELETE RESTRICT;

ALTER TABLE ge.crm_activity ADD CONSTRAINT fk_crm_activity__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.eng_message_template ADD CONSTRAINT fk_eng_message_template__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.eng_message_draft ADD CONSTRAINT fk_eng_message_draft__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.eng_thread ADD CONSTRAINT fk_eng_thread__contact_id FOREIGN KEY (contact_id) REFERENCES ge.intel_contact (id) ON DELETE RESTRICT;

ALTER TABLE ge.channel_account ADD CONSTRAINT uq_channel_account__account_id UNIQUE (account_id);

ALTER TABLE ge.eng_thread ADD CONSTRAINT fk_eng_thread__channel_account_id FOREIGN KEY (channel_account_id) REFERENCES ge.channel_account (account_id) ON DELETE RESTRICT;

ALTER TABLE ge.eng_thread ADD CONSTRAINT fk_eng_thread__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.eng_message ADD CONSTRAINT fk_eng_message__thread_id FOREIGN KEY (thread_id) REFERENCES ge.eng_thread (id) ON DELETE RESTRICT;

ALTER TABLE ge.eng_message ADD CONSTRAINT fk_eng_message__draft_id FOREIGN KEY (draft_id) REFERENCES ge.eng_message_draft (id) ON DELETE RESTRICT;

ALTER TABLE ge.eng_message ADD CONSTRAINT fk_eng_message__enrollment_id FOREIGN KEY (enrollment_id) REFERENCES ge.eng_enrollment (id) ON DELETE RESTRICT;

ALTER TABLE ge.eng_message ADD CONSTRAINT fk_eng_message__approval_id FOREIGN KEY (approval_id) REFERENCES ge.gov_approval (id) ON DELETE RESTRICT;

ALTER TABLE ge.eng_message ADD CONSTRAINT fk_eng_message__cost_reservation_id FOREIGN KEY (cost_reservation_id) REFERENCES ge.ai_cost_ledger (id) ON DELETE RESTRICT;

ALTER TABLE ge.eng_message ADD CONSTRAINT fk_eng_message__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.eng_delivery_event ADD CONSTRAINT fk_eng_delivery_event__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.eng_inbound_event ADD CONSTRAINT fk_eng_inbound_event__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.eng_intent ADD CONSTRAINT fk_eng_intent__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.eng_identity_link ADD CONSTRAINT fk_eng_identity_link__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.eng_routing_rule ADD CONSTRAINT fk_eng_routing_rule__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.eng_chat_session ADD CONSTRAINT fk_eng_chat_session__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.eng_sequence ADD CONSTRAINT fk_eng_sequence__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.eng_sequence_step ADD CONSTRAINT fk_eng_sequence_step__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.eng_enrollment ADD CONSTRAINT fk_eng_enrollment__sequence_id FOREIGN KEY (sequence_id) REFERENCES ge.eng_sequence (id) ON DELETE RESTRICT;

ALTER TABLE ge.eng_enrollment ADD CONSTRAINT fk_eng_enrollment__contact_id FOREIGN KEY (contact_id) REFERENCES ge.intel_contact (id) ON DELETE RESTRICT;

ALTER TABLE ge.eng_enrollment ADD CONSTRAINT fk_eng_enrollment__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.eng_meeting ADD CONSTRAINT fk_eng_meeting__organizer_id FOREIGN KEY (organizer_id) REFERENCES ge.ten_user (id) ON DELETE RESTRICT;

ALTER TABLE ge.eng_meeting ADD CONSTRAINT fk_eng_meeting__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.eng_calendar_link ADD CONSTRAINT fk_eng_calendar_link__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.mkt_content_asset ADD CONSTRAINT fk_mkt_content_asset__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.mkt_content_version ADD CONSTRAINT fk_mkt_content_version__asset_id FOREIGN KEY (asset_id) REFERENCES ge.mkt_content_asset (id) ON DELETE RESTRICT;

ALTER TABLE ge.mkt_content_version ADD CONSTRAINT fk_mkt_content_version__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.mkt_social_publication ADD CONSTRAINT fk_mkt_social_publication__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.mkt_keyword ADD CONSTRAINT fk_mkt_keyword__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.mkt_seo_issue ADD CONSTRAINT fk_mkt_seo_issue__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.mkt_page_metric ADD CONSTRAINT fk_mkt_page_metric__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.mkt_landing_page ADD CONSTRAINT fk_mkt_landing_page__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.mkt_publication ADD CONSTRAINT fk_mkt_publication__domain_id FOREIGN KEY (domain_id) REFERENCES ge.ten_domain (id) ON DELETE RESTRICT;

ALTER TABLE ge.mkt_publication ADD CONSTRAINT fk_mkt_publication__current_snapshot_id FOREIGN KEY (current_snapshot_id) REFERENCES ge.mkt_publication_snapshot (id) ON DELETE RESTRICT DEFERRABLE INITIALLY DEFERRED;

ALTER TABLE ge.mkt_publication ADD CONSTRAINT fk_mkt_publication__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.mkt_publication_snapshot ADD CONSTRAINT fk_mkt_publication_snapshot__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.mkt_preview_grant ADD CONSTRAINT fk_mkt_preview_grant__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.mkt_campaign ADD CONSTRAINT fk_mkt_campaign__current_version_id FOREIGN KEY (current_version_id) REFERENCES ge.mkt_campaign_version (id) ON DELETE RESTRICT DEFERRABLE INITIALLY DEFERRED;

ALTER TABLE ge.mkt_campaign ADD CONSTRAINT fk_mkt_campaign__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.mkt_campaign_version ADD CONSTRAINT fk_mkt_campaign_version__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.mkt_audience ADD CONSTRAINT fk_mkt_audience__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.mkt_ad_campaign ADD CONSTRAINT fk_mkt_ad_campaign__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.mkt_spend_event ADD CONSTRAINT fk_mkt_spend_event__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.mkt_event ADD CONSTRAINT fk_mkt_event__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.mkt_registration ADD CONSTRAINT fk_mkt_registration__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.mkt_attendance ADD CONSTRAINT fk_mkt_attendance__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.mkt_referral ADD CONSTRAINT fk_mkt_referral__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.mkt_attribution_event ADD CONSTRAINT fk_mkt_attribution_event__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.com_proposal ADD CONSTRAINT fk_com_proposal__deal_id FOREIGN KEY (deal_id) REFERENCES ge.crm_deal (id) ON DELETE RESTRICT;

ALTER TABLE ge.com_proposal ADD CONSTRAINT fk_com_proposal__current_version_id FOREIGN KEY (current_version_id) REFERENCES ge.com_proposal_version (id) ON DELETE RESTRICT DEFERRABLE INITIALLY DEFERRED;

ALTER TABLE ge.com_proposal ADD CONSTRAINT fk_com_proposal__portal_grant_id FOREIGN KEY (portal_grant_id) REFERENCES ge.ten_portal_grant (id) ON DELETE RESTRICT;

ALTER TABLE ge.com_proposal ADD CONSTRAINT fk_com_proposal__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.com_proposal_version ADD CONSTRAINT fk_com_proposal_version__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.com_quote ADD CONSTRAINT fk_com_quote__deal_id FOREIGN KEY (deal_id) REFERENCES ge.crm_deal (id) ON DELETE RESTRICT;

ALTER TABLE ge.com_quote ADD CONSTRAINT fk_com_quote__proposal_version_id FOREIGN KEY (proposal_version_id) REFERENCES ge.com_proposal_version (id) ON DELETE RESTRICT;

ALTER TABLE ge.com_quote ADD CONSTRAINT fk_com_quote__currency FOREIGN KEY (currency) REFERENCES ge.ref_currency (code) ON DELETE RESTRICT;

ALTER TABLE ge.com_quote ADD CONSTRAINT fk_com_quote__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.com_quote_line ADD CONSTRAINT fk_com_quote_line__quote_id FOREIGN KEY (quote_id) REFERENCES ge.com_quote (id) ON DELETE RESTRICT;

ALTER TABLE ge.com_quote_line ADD CONSTRAINT fk_com_quote_line__offering_version_id FOREIGN KEY (offering_version_id) REFERENCES ge.cat_offering_version (id) ON DELETE RESTRICT;

ALTER TABLE ge.com_quote_line ADD CONSTRAINT fk_com_quote_line__price_version_id FOREIGN KEY (price_version_id) REFERENCES ge.cat_price_version (id) ON DELETE RESTRICT;

ALTER TABLE ge.com_quote_line ADD CONSTRAINT fk_com_quote_line__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.com_objection ADD CONSTRAINT fk_com_objection__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.com_negotiation ADD CONSTRAINT fk_com_negotiation__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.com_contract ADD CONSTRAINT fk_com_contract__deal_id FOREIGN KEY (deal_id) REFERENCES ge.crm_deal (id) ON DELETE RESTRICT;

ALTER TABLE ge.com_contract ADD CONSTRAINT fk_com_contract__quote_id FOREIGN KEY (quote_id) REFERENCES ge.com_quote (id) ON DELETE RESTRICT;

ALTER TABLE ge.com_contract ADD CONSTRAINT fk_com_contract__currency FOREIGN KEY (currency) REFERENCES ge.ref_currency (code) ON DELETE RESTRICT;

ALTER TABLE ge.com_contract ADD CONSTRAINT fk_com_contract__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.com_signature_event ADD CONSTRAINT fk_com_signature_event__contract_id FOREIGN KEY (contract_id) REFERENCES ge.com_contract (id) ON DELETE RESTRICT;

ALTER TABLE ge.com_signature_event ADD CONSTRAINT fk_com_signature_event__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.com_bid ADD CONSTRAINT fk_com_bid__deal_id FOREIGN KEY (deal_id) REFERENCES ge.crm_deal (id) ON DELETE RESTRICT;

ALTER TABLE ge.com_bid ADD CONSTRAINT fk_com_bid__organization_id FOREIGN KEY (organization_id) REFERENCES ge.intel_organization (id) ON DELETE RESTRICT;

ALTER TABLE ge.com_bid ADD CONSTRAINT fk_com_bid__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.com_bid_checklist_item ADD CONSTRAINT fk_com_bid_checklist_item__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.com_order ADD CONSTRAINT fk_com_order__deal_id FOREIGN KEY (deal_id) REFERENCES ge.crm_deal (id) ON DELETE RESTRICT;

ALTER TABLE ge.com_order ADD CONSTRAINT fk_com_order__counterparty_org_id FOREIGN KEY (counterparty_org_id) REFERENCES ge.intel_organization (id) ON DELETE RESTRICT;

ALTER TABLE ge.com_order ADD CONSTRAINT fk_com_order__currency FOREIGN KEY (currency) REFERENCES ge.ref_currency (code) ON DELETE RESTRICT;

ALTER TABLE ge.com_order ADD CONSTRAINT fk_com_order__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.com_order_line ADD CONSTRAINT fk_com_order_line__order_id FOREIGN KEY (order_id) REFERENCES ge.com_order (id) ON DELETE RESTRICT;

ALTER TABLE ge.com_order_line ADD CONSTRAINT fk_com_order_line__unit_code FOREIGN KEY (unit_code) REFERENCES ge.ref_unit (code) ON DELETE RESTRICT;

ALTER TABLE ge.com_order_line ADD CONSTRAINT fk_com_order_line__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.com_fulfillment_event ADD CONSTRAINT fk_com_fulfillment_event__order_line_id FOREIGN KEY (order_line_id) REFERENCES ge.com_order_line (id) ON DELETE RESTRICT;

ALTER TABLE ge.com_fulfillment_event ADD CONSTRAINT fk_com_fulfillment_event__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.com_sku_availability ADD CONSTRAINT fk_com_sku_availability__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.com_inventory_reservation ADD CONSTRAINT fk_com_inventory_reservation__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.com_invoice ADD CONSTRAINT fk_com_invoice__bill_to_org_id FOREIGN KEY (bill_to_org_id) REFERENCES ge.intel_organization (id) ON DELETE RESTRICT;

ALTER TABLE ge.com_invoice ADD CONSTRAINT fk_com_invoice__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.com_invoice_line ADD CONSTRAINT fk_com_invoice_line__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.com_payment ADD CONSTRAINT fk_com_payment__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.com_payment_allocation ADD CONSTRAINT fk_com_payment_allocation__payment_id FOREIGN KEY (payment_id) REFERENCES ge.com_payment (id) ON DELETE RESTRICT;

ALTER TABLE ge.com_payment_allocation ADD CONSTRAINT fk_com_payment_allocation__invoice_id FOREIGN KEY (invoice_id) REFERENCES ge.com_invoice (id) ON DELETE RESTRICT;

ALTER TABLE ge.com_payment_allocation ADD CONSTRAINT fk_com_payment_allocation__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.com_discrepancy_case ADD CONSTRAINT fk_com_discrepancy_case__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.com_receivable_entry ADD CONSTRAINT fk_com_receivable_entry__counterparty_org_id FOREIGN KEY (counterparty_org_id) REFERENCES ge.intel_organization (id) ON DELETE RESTRICT;

ALTER TABLE ge.com_receivable_entry ADD CONSTRAINT fk_com_receivable_entry__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.com_payable_entry ADD CONSTRAINT fk_com_payable_entry__counterparty_org_id FOREIGN KEY (counterparty_org_id) REFERENCES ge.intel_organization (id) ON DELETE RESTRICT;

ALTER TABLE ge.com_payable_entry ADD CONSTRAINT fk_com_payable_entry__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.lcy_onboarding ADD CONSTRAINT fk_lcy_onboarding__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.lcy_task ADD CONSTRAINT fk_lcy_task__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.lcy_handoff ADD CONSTRAINT fk_lcy_handoff__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.lcy_renewal ADD CONSTRAINT fk_lcy_renewal__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.lcy_customer_subscription ADD CONSTRAINT fk_lcy_customer_subscription__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.lcy_account_metric ADD CONSTRAINT fk_lcy_account_metric__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.lcy_partner ADD CONSTRAINT fk_lcy_partner__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.lcy_pilot ADD CONSTRAINT fk_lcy_pilot__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.lcy_deployment ADD CONSTRAINT fk_lcy_deployment__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.lcy_integration_deal ADD CONSTRAINT fk_lcy_integration_deal__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.lcy_feedback ADD CONSTRAINT fk_lcy_feedback__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.lcy_outcome ADD CONSTRAINT fk_lcy_outcome__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.aut_workflow ADD CONSTRAINT fk_aut_workflow__active_revision_id FOREIGN KEY (active_revision_id) REFERENCES ge.aut_workflow_revision (id) ON DELETE RESTRICT DEFERRABLE INITIALLY DEFERRED;

ALTER TABLE ge.aut_workflow ADD CONSTRAINT fk_aut_workflow__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.aut_workflow_revision ADD CONSTRAINT fk_aut_workflow_revision__workflow_id FOREIGN KEY (workflow_id) REFERENCES ge.aut_workflow (id) ON DELETE RESTRICT;

ALTER TABLE ge.aut_workflow_revision ADD CONSTRAINT fk_aut_workflow_revision__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.aut_trigger ADD CONSTRAINT fk_aut_trigger__workflow_revision_id FOREIGN KEY (workflow_revision_id) REFERENCES ge.aut_workflow_revision (id) ON DELETE RESTRICT;

ALTER TABLE ge.aut_trigger ADD CONSTRAINT fk_aut_trigger__credential_ref_id FOREIGN KEY (credential_ref_id) REFERENCES ge.int_credential_ref (id) ON DELETE RESTRICT;

ALTER TABLE ge.aut_trigger ADD CONSTRAINT fk_aut_trigger__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.aut_autonomy_plan ADD CONSTRAINT fk_aut_autonomy_plan__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.aut_conflict_case ADD CONSTRAINT fk_aut_conflict_case__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.aut_node_template ADD CONSTRAINT fk_aut_node_template__tenant_id FOREIGN KEY (tenant_id) REFERENCES ge.tenant (tenant_id) ON DELETE RESTRICT;

ALTER TABLE ge.aut_node_template ADD CONSTRAINT fk_aut_node_template__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.aut_workflow_template ADD CONSTRAINT fk_aut_workflow_template__tenant_id FOREIGN KEY (tenant_id) REFERENCES ge.tenant (tenant_id) ON DELETE RESTRICT;

ALTER TABLE ge.aut_workflow_template ADD CONSTRAINT fk_aut_workflow_template__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.aut_config_revision ADD CONSTRAINT fk_aut_config_revision__tenant_id FOREIGN KEY (tenant_id) REFERENCES ge.tenant (tenant_id) ON DELETE RESTRICT;

ALTER TABLE ge.aut_config_revision ADD CONSTRAINT fk_aut_config_revision__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.ops_domain_event ADD CONSTRAINT fk_ops_domain_event__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.ops_idempotency_key ADD CONSTRAINT fk_ops_idempotency_key__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.ops_job_run ADD CONSTRAINT fk_ops_job_run__tenant_id FOREIGN KEY (tenant_id) REFERENCES ge.tenant (tenant_id) ON DELETE RESTRICT;

ALTER TABLE ge.ops_job_run ADD CONSTRAINT fk_ops_job_run__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.ops_notification ADD CONSTRAINT fk_ops_notification__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.ops_notification_preference ADD CONSTRAINT fk_ops_notification_preference__tenant_id FOREIGN KEY (tenant_id) REFERENCES ge.tenant (tenant_id) ON DELETE RESTRICT;

ALTER TABLE ge.ops_notification_preference ADD CONSTRAINT fk_ops_notification_preference__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.saas_plan ADD CONSTRAINT fk_saas_plan__current_version_id FOREIGN KEY (current_version_id) REFERENCES ge.saas_plan_version (id) ON DELETE RESTRICT DEFERRABLE INITIALLY DEFERRED;

ALTER TABLE ge.saas_entitlement ADD CONSTRAINT fk_saas_entitlement__tenant_id FOREIGN KEY (tenant_id) REFERENCES ge.tenant (tenant_id) ON DELETE RESTRICT;

ALTER TABLE ge.saas_entitlement ADD CONSTRAINT fk_saas_entitlement__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.saas_subscription ADD CONSTRAINT fk_saas_subscription__plan_version_id FOREIGN KEY (plan_version_id) REFERENCES ge.saas_plan_version (id) ON DELETE RESTRICT;

ALTER TABLE ge.saas_subscription ADD CONSTRAINT fk_saas_subscription__tenant_id FOREIGN KEY (tenant_id) REFERENCES ge.tenant (tenant_id) ON DELETE RESTRICT;

ALTER TABLE ge.saas_subscription ADD CONSTRAINT fk_saas_subscription__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.saas_usage_meter_reading ADD CONSTRAINT fk_saas_usage_meter_reading__tenant_id FOREIGN KEY (tenant_id) REFERENCES ge.tenant (tenant_id) ON DELETE RESTRICT;

ALTER TABLE ge.saas_usage_meter_reading ADD CONSTRAINT fk_saas_usage_meter_reading__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.saas_service_invoice_line ADD CONSTRAINT fk_saas_service_invoice_line__tenant_id FOREIGN KEY (tenant_id) REFERENCES ge.tenant (tenant_id) ON DELETE RESTRICT;

ALTER TABLE ge.saas_service_invoice_line ADD CONSTRAINT fk_saas_service_invoice_line__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.saas_credit ADD CONSTRAINT fk_saas_credit__tenant_id FOREIGN KEY (tenant_id) REFERENCES ge.tenant (tenant_id) ON DELETE RESTRICT;

ALTER TABLE ge.saas_credit ADD CONSTRAINT fk_saas_credit__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.saas_application_draft ADD CONSTRAINT fk_saas_application_draft__applicant_user_id FOREIGN KEY (applicant_user_id) REFERENCES ge.ten_user (id) ON DELETE RESTRICT;

ALTER TABLE ge.saas_application_draft ADD CONSTRAINT fk_saas_application_draft__provisioned_tenant_id FOREIGN KEY (provisioned_tenant_id) REFERENCES ge.tenant (tenant_id) ON DELETE RESTRICT DEFERRABLE INITIALLY DEFERRED;

ALTER TABLE ge.saas_support_access_grant ADD CONSTRAINT fk_saas_support_access_grant__tenant_id FOREIGN KEY (tenant_id) REFERENCES ge.tenant (tenant_id) ON DELETE RESTRICT;

ALTER TABLE ge.saas_support_access_grant ADD CONSTRAINT fk_saas_support_access_grant__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.saas_import_job ADD CONSTRAINT fk_saas_import_job__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.ana_metric_definition ADD CONSTRAINT fk_ana_metric_definition__tenant_id FOREIGN KEY (tenant_id) REFERENCES ge.tenant (tenant_id) ON DELETE RESTRICT;

ALTER TABLE ge.ana_metric_definition ADD CONSTRAINT fk_ana_metric_definition__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.ana_metric_snapshot ADD CONSTRAINT fk_ana_metric_snapshot__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.ana_account_projection ADD CONSTRAINT fk_ana_account_projection__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.ana_admin_projection ADD CONSTRAINT fk_ana_admin_projection__tenant_id FOREIGN KEY (tenant_id) REFERENCES ge.tenant (tenant_id) ON DELETE RESTRICT;

ALTER TABLE ge.ana_admin_projection ADD CONSTRAINT fk_ana_admin_projection__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.ana_pipeline_projection ADD CONSTRAINT fk_ana_pipeline_projection__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.ana_forecast ADD CONSTRAINT fk_ana_forecast__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.ana_stage_metric ADD CONSTRAINT fk_ana_stage_metric__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.ana_report_subscription ADD CONSTRAINT fk_ana_report_subscription__tenant_id FOREIGN KEY (tenant_id) REFERENCES ge.tenant (tenant_id) ON DELETE RESTRICT;

ALTER TABLE ge.ana_report_subscription ADD CONSTRAINT fk_ana_report_subscription__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.ten_membership_grant ADD CONSTRAINT fk_ten_membership_grant__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.cat_document_offering ADD CONSTRAINT fk_cat_document_offering__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.cat_claim_evidence ADD CONSTRAINT fk_cat_claim_evidence__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.intel_signal_evidence ADD CONSTRAINT fk_intel_signal_evidence__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.intel_opportunity_contact ADD CONSTRAINT fk_intel_opportunity_contact__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.crm_deal_contact ADD CONSTRAINT fk_crm_deal_contact__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.eng_message_claim ADD CONSTRAINT fk_eng_message_claim__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.mkt_content_claim ADD CONSTRAINT fk_mkt_content_claim__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.mkt_audience_member ADD CONSTRAINT fk_mkt_audience_member__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.com_contract_party ADD CONSTRAINT fk_com_contract_party__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.aut_run_conflict ADD CONSTRAINT fk_aut_run_conflict__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.saas_plan_entitlement ADD CONSTRAINT fk_saas_plan_entitlement__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.lcy_onboarding_task ADD CONSTRAINT fk_lcy_onboarding_task__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.ten_business_template ADD CONSTRAINT fk_ten_business_template__tenant_id FOREIGN KEY (tenant_id) REFERENCES ge.tenant (tenant_id) ON DELETE RESTRICT;

ALTER TABLE ge.ten_business_template ADD CONSTRAINT fk_ten_business_template__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.saas_service_request ADD CONSTRAINT fk_saas_service_request__requester_user_id FOREIGN KEY (requester_user_id) REFERENCES ge.ten_user (id) ON DELETE RESTRICT;

ALTER TABLE ge.saas_service_request ADD CONSTRAINT fk_saas_service_request__assignee_user_id FOREIGN KEY (assignee_user_id) REFERENCES ge.ten_user (id) ON DELETE RESTRICT;

ALTER TABLE ge.saas_service_request ADD CONSTRAINT fk_saas_service_request__support_grant_id FOREIGN KEY (support_grant_id) REFERENCES ge.saas_support_access_grant (id) ON DELETE RESTRICT;

ALTER TABLE ge.saas_service_request ADD CONSTRAINT fk_saas_service_request__tenant_id FOREIGN KEY (tenant_id) REFERENCES ge.tenant (tenant_id) ON DELETE RESTRICT;

ALTER TABLE ge.saas_service_request ADD CONSTRAINT fk_saas_service_request__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.com_fulfillment_milestone ADD CONSTRAINT fk_com_fulfillment_milestone__order_id FOREIGN KEY (order_id) REFERENCES ge.com_order (id) ON DELETE RESTRICT;

ALTER TABLE ge.com_fulfillment_milestone ADD CONSTRAINT fk_com_fulfillment_milestone__order_line_id FOREIGN KEY (order_line_id) REFERENCES ge.com_order_line (id) ON DELETE RESTRICT;

ALTER TABLE ge.com_fulfillment_milestone ADD CONSTRAINT fk_com_fulfillment_milestone__unit_code FOREIGN KEY (unit_code) REFERENCES ge.ref_unit (code) ON DELETE RESTRICT;

ALTER TABLE ge.com_fulfillment_milestone ADD CONSTRAINT fk_com_fulfillment_milestone__last_event_id FOREIGN KEY (last_event_id) REFERENCES ge.com_fulfillment_event (id) ON DELETE RESTRICT;

ALTER TABLE ge.com_fulfillment_milestone ADD CONSTRAINT fk_com_fulfillment_milestone__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.ai_eval_case_result ADD CONSTRAINT fk_ai_eval_case_result__eval_run_id FOREIGN KEY (eval_run_id) REFERENCES ge.eval_run (eval_run_id) ON DELETE RESTRICT;

ALTER TABLE ge.ai_eval_case_result ADD CONSTRAINT fk_ai_eval_case_result__eval_case_id FOREIGN KEY (eval_case_id) REFERENCES ge.ai_eval_case (id) ON DELETE RESTRICT;

ALTER TABLE ge.ai_eval_case_result ADD CONSTRAINT fk_ai_eval_case_result__model_run_id FOREIGN KEY (model_run_id) REFERENCES ge.ai_model_run (id) ON DELETE RESTRICT;

ALTER TABLE ge.ai_eval_case_result ADD CONSTRAINT fk_ai_eval_case_result__tenant_id FOREIGN KEY (tenant_id) REFERENCES ge.tenant (tenant_id) ON DELETE RESTRICT;

ALTER TABLE ge.ai_eval_case_result ADD CONSTRAINT fk_ai_eval_case_result__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.inv_source ADD CONSTRAINT fk_inv_source__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.inv_source_policy ADD CONSTRAINT fk_inv_source_policy__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.inv_search_plan ADD CONSTRAINT fk_inv_search_plan__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.inv_search_run ADD CONSTRAINT fk_inv_search_run__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.inv_funding_route ADD CONSTRAINT fk_inv_funding_route__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.inv_opportunity ADD CONSTRAINT fk_inv_opportunity__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.inv_evidence ADD CONSTRAINT fk_inv_evidence__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.inv_investor ADD CONSTRAINT fk_inv_investor__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.inv_investor_alias ADD CONSTRAINT fk_inv_investor_alias__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.inv_mandate ADD CONSTRAINT fk_inv_mandate__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.inv_round ADD CONSTRAINT fk_inv_round__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.inv_fit_score ADD CONSTRAINT fk_inv_fit_score__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.inv_match_candidate ADD CONSTRAINT fk_inv_match_candidate__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.inv_jurisdiction_policy ADD CONSTRAINT fk_inv_jurisdiction_policy__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.inv_crossborder_case ADD CONSTRAINT fk_inv_crossborder_case__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.inv_contact ADD CONSTRAINT fk_inv_contact__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.inv_contact_evidence ADD CONSTRAINT fk_inv_contact_evidence__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.inv_permission ADD CONSTRAINT fk_inv_permission__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.inv_suppression ADD CONSTRAINT fk_inv_suppression__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.inv_locale_template ADD CONSTRAINT fk_inv_locale_template__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.inv_message ADD CONSTRAINT fk_inv_message__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.inv_outbox ADD CONSTRAINT fk_inv_outbox__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.inv_outreach_reservation ADD CONSTRAINT fk_inv_outreach_reservation__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.inv_delivery_event ADD CONSTRAINT fk_inv_delivery_event__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.inv_channel ADD CONSTRAINT fk_inv_channel__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.inv_integration_connection ADD CONSTRAINT fk_inv_integration_connection__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.inv_inbound_event ADD CONSTRAINT fk_inv_inbound_event__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.inv_thread ADD CONSTRAINT fk_inv_thread__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.inv_sequence ADD CONSTRAINT fk_inv_sequence__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.inv_enrollment ADD CONSTRAINT fk_inv_enrollment__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.inv_task ADD CONSTRAINT fk_inv_task__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.inv_stage_event ADD CONSTRAINT fk_inv_stage_event__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.inv_relationship ADD CONSTRAINT fk_inv_relationship__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.inv_workflow_run ADD CONSTRAINT fk_inv_workflow_run__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.inv_objection ADD CONSTRAINT fk_inv_objection__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.inv_objection_rule ADD CONSTRAINT fk_inv_objection_rule__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.inv_copilot_action ADD CONSTRAINT fk_inv_copilot_action__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.inv_meeting ADD CONSTRAINT fk_inv_meeting__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.inv_event ADD CONSTRAINT fk_inv_event__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.inv_referral ADD CONSTRAINT fk_inv_referral__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.inv_adviser_referral ADD CONSTRAINT fk_inv_adviser_referral__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.inv_scenario ADD CONSTRAINT fk_inv_scenario__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.inv_claim ADD CONSTRAINT fk_inv_claim__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.inv_disclosure ADD CONSTRAINT fk_inv_disclosure__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.inv_guarantee_evidence ADD CONSTRAINT fk_inv_guarantee_evidence__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.inv_document ADD CONSTRAINT fk_inv_document__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.inv_room ADD CONSTRAINT fk_inv_room__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.inv_room_item ADD CONSTRAINT fk_inv_room_item__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.inv_access_grant ADD CONSTRAINT fk_inv_access_grant__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.inv_nda ADD CONSTRAINT fk_inv_nda__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.inv_diligence_request ADD CONSTRAINT fk_inv_diligence_request__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.inv_term_version ADD CONSTRAINT fk_inv_term_version__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.inv_agreement ADD CONSTRAINT fk_inv_agreement__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.inv_approval ADD CONSTRAINT fk_inv_approval__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.inv_offer ADD CONSTRAINT fk_inv_offer__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.inv_offer_batch ADD CONSTRAINT fk_inv_offer_batch__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.inv_offer_recipient ADD CONSTRAINT fk_inv_offer_recipient__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.inv_verification_case ADD CONSTRAINT fk_inv_verification_case__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.inv_bank_account ADD CONSTRAINT fk_inv_bank_account__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.inv_payment_instruction ADD CONSTRAINT fk_inv_payment_instruction__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.inv_commitment ADD CONSTRAINT fk_inv_commitment__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.inv_receipt ADD CONSTRAINT fk_inv_receipt__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.inv_receipt_allocation ADD CONSTRAINT fk_inv_receipt_allocation__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.inv_refund ADD CONSTRAINT fk_inv_refund__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.inv_fx_rate ADD CONSTRAINT fk_inv_fx_rate__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.inv_offering ADD CONSTRAINT fk_inv_offering__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.inv_counsel_signoff ADD CONSTRAINT fk_inv_counsel_signoff__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.inv_eligibility_check ADD CONSTRAINT fk_inv_eligibility_check__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.inv_relationship_provenance ADD CONSTRAINT fk_inv_relationship_provenance__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.inv_offer_counter ADD CONSTRAINT fk_inv_offer_counter__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.inv_guard_finding ADD CONSTRAINT fk_inv_guard_finding__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.inv_offer_ledger ADD CONSTRAINT fk_inv_offer_ledger__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.inv_offeree ADD CONSTRAINT fk_inv_offeree__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.inv_investor_classification ADD CONSTRAINT fk_inv_investor_classification__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.inv_accreditation_verification ADD CONSTRAINT fk_inv_accreditation_verification__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.inv_promotion_review ADD CONSTRAINT fk_inv_promotion_review__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.inv_application_money_account ADD CONSTRAINT fk_inv_application_money_account__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.inv_allotment_clock ADD CONSTRAINT fk_inv_allotment_clock__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.inv_closing ADD CONSTRAINT fk_inv_closing__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.inv_closing_requirement ADD CONSTRAINT fk_inv_closing_requirement__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.inv_allotment ADD CONSTRAINT fk_inv_allotment__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.inv_filing_task ADD CONSTRAINT fk_inv_filing_task__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.inv_legal_check ADD CONSTRAINT fk_inv_legal_check__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.inv_obligation ADD CONSTRAINT fk_inv_obligation__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.inv_update ADD CONSTRAINT fk_inv_update__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.inv_feedback ADD CONSTRAINT fk_inv_feedback__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.inv_deployment_milestone ADD CONSTRAINT fk_inv_deployment_milestone__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.inv_capital_allocation ADD CONSTRAINT fk_inv_capital_allocation__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.inv_dashboard_projection ADD CONSTRAINT fk_inv_dashboard_projection__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.inv_webhook_endpoint ADD CONSTRAINT fk_inv_webhook_endpoint__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.inv_external_agent_mandate ADD CONSTRAINT fk_inv_external_agent_mandate__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.inv_grant_case ADD CONSTRAINT fk_inv_grant_case__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.inv_grant_criterion ADD CONSTRAINT fk_inv_grant_criterion__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.inv_grant_budget_line ADD CONSTRAINT fk_inv_grant_budget_line__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.inv_grant_award ADD CONSTRAINT fk_inv_grant_award__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.inv_debt_case ADD CONSTRAINT fk_inv_debt_case__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.inv_debt_term ADD CONSTRAINT fk_inv_debt_term__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.inv_covenant ADD CONSTRAINT fk_inv_covenant__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.inv_repayment_schedule ADD CONSTRAINT fk_inv_repayment_schedule__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.inv_readiness_snapshot ADD CONSTRAINT fk_inv_readiness_snapshot__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.inv_runway_scenario ADD CONSTRAINT fk_inv_runway_scenario__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.inv_readiness_score ADD CONSTRAINT fk_inv_readiness_score__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.inv_shareholder ADD CONSTRAINT fk_inv_shareholder__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.inv_holding ADD CONSTRAINT fk_inv_holding__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.inv_instrument ADD CONSTRAINT fk_inv_instrument__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.inv_instrument_term ADD CONSTRAINT fk_inv_instrument_term__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.inv_option_grant ADD CONSTRAINT fk_inv_option_grant__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.inv_cap_table_revision ADD CONSTRAINT fk_inv_cap_table_revision__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.inv_esg_indicator ADD CONSTRAINT fk_inv_esg_indicator__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.inv_esg_observation ADD CONSTRAINT fk_inv_esg_observation__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.inv_esg_disclosure ADD CONSTRAINT fk_inv_esg_disclosure__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.inv_esg_commitment ADD CONSTRAINT fk_inv_esg_commitment__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.inv_crossborder_requirement ADD CONSTRAINT fk_inv_crossborder_requirement__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.inv_regulatory_deadline ADD CONSTRAINT fk_inv_regulatory_deadline__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.inv_resolution ADD CONSTRAINT fk_inv_resolution__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.inv_vote ADD CONSTRAINT fk_inv_vote__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.inv_decision_action ADD CONSTRAINT fk_inv_decision_action__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.inv_kyc_case ADD CONSTRAINT fk_inv_kyc_case__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.inv_kyc_provider_result ADD CONSTRAINT fk_inv_kyc_provider_result__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.inv_screening_hit ADD CONSTRAINT fk_inv_screening_hit__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.inv_advice_boundary_event ADD CONSTRAINT fk_inv_advice_boundary_event__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.inv_rulepack_activation ADD CONSTRAINT fk_inv_rulepack_activation__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.mandate ADD CONSTRAINT fk_mandate__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.mandate_version ADD CONSTRAINT fk_mandate_version__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.mandate_approval ADD CONSTRAINT fk_mandate_approval__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.mandate_scope_item ADD CONSTRAINT fk_mandate_scope_item__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.mandate_limit ADD CONSTRAINT fk_mandate_limit__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.mandate_window ADD CONSTRAINT fk_mandate_window__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.mandate_restriction ADD CONSTRAINT fk_mandate_restriction__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.mandate_counter ADD CONSTRAINT fk_mandate_counter__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.mandate_consumption ADD CONSTRAINT fk_mandate_consumption__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.mandate_decision ADD CONSTRAINT fk_mandate_decision__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.kill_switch ADD CONSTRAINT fk_kill_switch__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.kill_switch_event ADD CONSTRAINT fk_kill_switch_event__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.effect_receipt ADD CONSTRAINT fk_effect_receipt__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.counterparty_agent ADD CONSTRAINT fk_counterparty_agent__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.agent_credential ADD CONSTRAINT fk_agent_credential__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.agent_message ADD CONSTRAINT fk_agent_message__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.negotiation_session ADD CONSTRAINT fk_negotiation_session__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.negotiation_step ADD CONSTRAINT fk_negotiation_step__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.commerce_order ADD CONSTRAINT fk_commerce_order__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.payment_mandate ADD CONSTRAINT fk_payment_mandate__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.payment_txn ADD CONSTRAINT fk_payment_txn__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.refund ADD CONSTRAINT fk_refund__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.dispute_case ADD CONSTRAINT fk_dispute_case__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.settlement_batch ADD CONSTRAINT fk_settlement_batch__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.bid_package ADD CONSTRAINT fk_bid_package__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.bid_file ADD CONSTRAINT fk_bid_file__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.bid_submission ADD CONSTRAINT fk_bid_submission__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.portal_profile ADD CONSTRAINT fk_portal_profile__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.recon_run ADD CONSTRAINT fk_recon_run__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.recon_break ADD CONSTRAINT fk_recon_break__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.ledger_entry ADD CONSTRAINT fk_ledger_entry__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.voice_session ADD CONSTRAINT fk_voice_session__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.voice_leg ADD CONSTRAINT fk_voice_leg__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.voice_campaign ADD CONSTRAINT fk_voice_campaign__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.voice_campaign_contact ADD CONSTRAINT fk_voice_campaign_contact__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.voice_script ADD CONSTRAINT fk_voice_script__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.voice_script_version ADD CONSTRAINT fk_voice_script_version__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.voice_number_pool ADD CONSTRAINT fk_voice_number_pool__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.voice_scrub_result ADD CONSTRAINT fk_voice_scrub_result__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.voice_consent_evidence ADD CONSTRAINT fk_voice_consent_evidence__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.voice_recording ADD CONSTRAINT fk_voice_recording__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.voice_transcript ADD CONSTRAINT fk_voice_transcript__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.voice_transcript_segment ADD CONSTRAINT fk_voice_transcript_segment__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.voice_summary ADD CONSTRAINT fk_voice_summary__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.voice_handoff ADD CONSTRAINT fk_voice_handoff__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.voice_voicemail ADD CONSTRAINT fk_voice_voicemail__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.voice_meter_event ADD CONSTRAINT fk_voice_meter_event__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.voice_access_log ADD CONSTRAINT fk_voice_access_log__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.voice_legal_hold ADD CONSTRAINT fk_voice_legal_hold__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.coaching_rubric ADD CONSTRAINT fk_coaching_rubric__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.coaching_feedback ADD CONSTRAINT fk_coaching_feedback__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.coaching_share ADD CONSTRAINT fk_coaching_share__tenant_id_startup_id FOREIGN KEY (tenant_id, startup_id) REFERENCES ge.company (tenant_id, company_id) ON DELETE RESTRICT;

ALTER TABLE ge.tenant ADD CONSTRAINT fk_tenant__source_application_id FOREIGN KEY (source_application_id) REFERENCES ge.saas_application_draft (id) ON DELETE RESTRICT DEFERRABLE INITIALLY DEFERRED;

ALTER TABLE ge.company ADD CONSTRAINT fk_company__country_code FOREIGN KEY (country_code) REFERENCES ge.ref_country (code) ON DELETE RESTRICT;

ALTER TABLE ge.company ADD CONSTRAINT fk_company__base_currency FOREIGN KEY (base_currency) REFERENCES ge.ref_currency (code) ON DELETE RESTRICT;

ALTER TABLE ge.company ADD CONSTRAINT fk_company__template_ref FOREIGN KEY (template_ref) REFERENCES ge.aut_workflow_template (id) ON DELETE RESTRICT;

ALTER TABLE ge.division ADD CONSTRAINT uq_division__division_id UNIQUE (division_id);

ALTER TABLE ge.offering ADD CONSTRAINT fk_offering__business_line_id FOREIGN KEY (business_line_id) REFERENCES ge.division (division_id) ON DELETE RESTRICT;

ALTER TABLE ge.offering ADD CONSTRAINT fk_offering__current_version_id FOREIGN KEY (current_version_id) REFERENCES ge.cat_offering_version (id) ON DELETE RESTRICT DEFERRABLE INITIALLY DEFERRED;

ALTER TABLE ge.offering ADD CONSTRAINT fk_offering__owner_id FOREIGN KEY (owner_id) REFERENCES ge.ten_user (id) ON DELETE RESTRICT;

ALTER TABLE ge.workflow_run ADD CONSTRAINT fk_workflow_run__workflow_revision_id FOREIGN KEY (workflow_revision_id) REFERENCES ge.aut_workflow_revision (id) ON DELETE RESTRICT;

ALTER TABLE ge.consent_record ADD CONSTRAINT fk_consent_record__lia_ref FOREIGN KEY (lia_ref) REFERENCES ge.cat_document (id) ON DELETE RESTRICT;

ALTER TABLE ge.consent_record ADD CONSTRAINT fk_consent_record__policy_version_id FOREIGN KEY (policy_version_id) REFERENCES ge.gov_policy_version (id) ON DELETE RESTRICT;

ALTER TABLE ge.consent_record ADD CONSTRAINT fk_consent_record__guardian_contact_id FOREIGN KEY (guardian_contact_id) REFERENCES ge.intel_contact (id) ON DELETE RESTRICT;

ALTER TABLE ge.consent_record ADD CONSTRAINT fk_consent_record__jurisdiction_code FOREIGN KEY (jurisdiction_code) REFERENCES ge.ref_country (code) ON DELETE RESTRICT;

ALTER TABLE ge.ten_portal_grant ADD CONSTRAINT fk_ten_portal_grant__contact_id FOREIGN KEY (contact_id) REFERENCES ge.intel_contact (id) ON DELETE RESTRICT;

ALTER TABLE ge.gov_policy_decision ADD CONSTRAINT fk_gov_policy_decision__policy_version_id FOREIGN KEY (policy_version_id) REFERENCES ge.gov_policy_version (id) ON DELETE RESTRICT;

ALTER TABLE ge.incident ADD CONSTRAINT fk_incident__policy_decision_id FOREIGN KEY (policy_decision_id) REFERENCES ge.gov_policy_decision (id) ON DELETE RESTRICT;

ALTER TABLE ge.incident ADD CONSTRAINT fk_incident__message_id FOREIGN KEY (message_id) REFERENCES ge.eng_message (id) ON DELETE RESTRICT;

ALTER TABLE ge.ai_usage_event ADD CONSTRAINT fk_ai_usage_event__integration_id FOREIGN KEY (integration_id) REFERENCES ge.connector_installation (installation_id) ON DELETE RESTRICT;

ALTER TABLE ge.intel_search_plan ADD CONSTRAINT fk_intel_search_plan__offering_id FOREIGN KEY (offering_id) REFERENCES ge.offering (offering_id) ON DELETE RESTRICT;

ALTER TABLE ge.intel_source_record ADD CONSTRAINT fk_intel_source_record__query_run_id FOREIGN KEY (query_run_id) REFERENCES ge.intel_query_run (id) ON DELETE RESTRICT;

ALTER TABLE ge.intel_fetch_log ADD CONSTRAINT fk_intel_fetch_log__source_id FOREIGN KEY (source_id) REFERENCES ge.intel_source (id) ON DELETE RESTRICT;

ALTER TABLE ge.intel_fetch_log ADD CONSTRAINT fk_intel_fetch_log__query_run_id FOREIGN KEY (query_run_id) REFERENCES ge.intel_query_run (id) ON DELETE RESTRICT;

ALTER TABLE ge.intel_alias ADD CONSTRAINT fk_intel_alias__source_record_id FOREIGN KEY (source_record_id) REFERENCES ge.intel_source_record (id) ON DELETE RESTRICT;

ALTER TABLE ge.intel_match ADD CONSTRAINT fk_intel_match__capability_id FOREIGN KEY (capability_id) REFERENCES ge.cat_capability (id) ON DELETE RESTRICT;

ALTER TABLE ge.intel_role_hypothesis ADD CONSTRAINT fk_intel_role_hypothesis__opportunity_id FOREIGN KEY (opportunity_id) REFERENCES ge.intel_opportunity (id) ON DELETE RESTRICT;

ALTER TABLE ge.intel_contact_source ADD CONSTRAINT fk_intel_contact_source__source_record_id FOREIGN KEY (source_record_id) REFERENCES ge.intel_source_record (id) ON DELETE RESTRICT;

ALTER TABLE ge.intel_contact_verification ADD CONSTRAINT fk_intel_contact_verification__contact_source_id FOREIGN KEY (contact_source_id) REFERENCES ge.intel_contact_source (id) ON DELETE RESTRICT;

ALTER TABLE ge.intel_social_post ADD CONSTRAINT fk_intel_social_post__source_record_id FOREIGN KEY (source_record_id) REFERENCES ge.intel_source_record (id) ON DELETE RESTRICT;

ALTER TABLE ge.crm_submission ADD CONSTRAINT fk_crm_submission__consent_id FOREIGN KEY (consent_id) REFERENCES ge.consent_record (consent_id) ON DELETE RESTRICT;

ALTER TABLE ge.eng_message_draft ADD CONSTRAINT fk_eng_message_draft__eligibility_decision_id FOREIGN KEY (eligibility_decision_id) REFERENCES ge.gov_eligibility_decision (id) ON DELETE RESTRICT;

ALTER TABLE ge.eng_chat_session ADD CONSTRAINT fk_eng_chat_session__thread_id FOREIGN KEY (thread_id) REFERENCES ge.eng_thread (id) ON DELETE RESTRICT;

ALTER TABLE ge.eng_identity_link ADD CONSTRAINT fk_eng_identity_link__channel_account_id FOREIGN KEY (channel_account_id) REFERENCES ge.channel_account (account_id) ON DELETE RESTRICT;

ALTER TABLE ge.mkt_content_asset ADD CONSTRAINT fk_mkt_content_asset__offering_id FOREIGN KEY (offering_id) REFERENCES ge.offering (offering_id) ON DELETE RESTRICT;

ALTER TABLE ge.mkt_seo_issue ADD CONSTRAINT fk_mkt_seo_issue__keyword_id FOREIGN KEY (keyword_id) REFERENCES ge.mkt_keyword (id) ON DELETE RESTRICT;

ALTER TABLE ge.mkt_attribution_event ADD CONSTRAINT fk_mkt_attribution_event__landing_page_id FOREIGN KEY (landing_page_id) REFERENCES ge.mkt_landing_page (id) ON DELETE RESTRICT;

ALTER TABLE ge.mkt_ad_campaign ADD CONSTRAINT fk_mkt_ad_campaign__channel_account_id FOREIGN KEY (channel_account_id) REFERENCES ge.channel_account (account_id) ON DELETE RESTRICT;

ALTER TABLE ge.mkt_event ADD CONSTRAINT fk_mkt_event__offering_id FOREIGN KEY (offering_id) REFERENCES ge.offering (offering_id) ON DELETE RESTRICT;

ALTER TABLE ge.mkt_registration ADD CONSTRAINT fk_mkt_registration__lead_id FOREIGN KEY (lead_id) REFERENCES ge.crm_lead (id) ON DELETE RESTRICT;

ALTER TABLE ge.mkt_referral ADD CONSTRAINT fk_mkt_referral__lead_id FOREIGN KEY (lead_id) REFERENCES ge.crm_lead (id) ON DELETE RESTRICT;

ALTER TABLE ge.com_objection ADD CONSTRAINT fk_com_objection__thread_id FOREIGN KEY (thread_id) REFERENCES ge.eng_thread (id) ON DELETE RESTRICT;

ALTER TABLE ge.com_negotiation ADD CONSTRAINT fk_com_negotiation__quote_id FOREIGN KEY (quote_id) REFERENCES ge.com_quote (id) ON DELETE RESTRICT;

ALTER TABLE ge.com_bid ADD CONSTRAINT fk_com_bid__opportunity_id FOREIGN KEY (opportunity_id) REFERENCES ge.intel_opportunity (id) ON DELETE RESTRICT;

ALTER TABLE ge.com_bid ADD CONSTRAINT fk_com_bid__proposal_id FOREIGN KEY (proposal_id) REFERENCES ge.com_proposal (id) ON DELETE RESTRICT;

ALTER TABLE ge.com_order ADD CONSTRAINT fk_com_order__quote_id FOREIGN KEY (quote_id) REFERENCES ge.com_quote (id) ON DELETE RESTRICT;

ALTER TABLE ge.lcy_onboarding ADD CONSTRAINT fk_lcy_onboarding__owner_id FOREIGN KEY (owner_id) REFERENCES ge.ten_user (id) ON DELETE RESTRICT;

ALTER TABLE ge.lcy_handoff ADD CONSTRAINT fk_lcy_handoff__task_id FOREIGN KEY (task_id) REFERENCES ge.lcy_task (id) ON DELETE RESTRICT;

ALTER TABLE ge.lcy_pilot ADD CONSTRAINT fk_lcy_pilot__deal_id FOREIGN KEY (deal_id) REFERENCES ge.crm_deal (id) ON DELETE RESTRICT;

ALTER TABLE ge.lcy_integration_deal ADD CONSTRAINT fk_lcy_integration_deal__deal_id FOREIGN KEY (deal_id) REFERENCES ge.crm_deal (id) ON DELETE RESTRICT;

ALTER TABLE ge.ops_incident ADD CONSTRAINT fk_ops_incident__job_run_id FOREIGN KEY (job_run_id) REFERENCES ge.ops_job_run (id) ON DELETE RESTRICT;

ALTER TABLE ge.eng_intent ADD CONSTRAINT fk_eng_intent__superseded_by FOREIGN KEY (superseded_by) REFERENCES ge.eng_intent (id) ON DELETE RESTRICT;

ALTER TABLE ge.consent_record ADD CONSTRAINT consent_record_contact_fk FOREIGN KEY (tenant_id, contact_id) REFERENCES ge.intel_contact (tenant_id, id);
