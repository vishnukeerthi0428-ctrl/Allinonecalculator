-- V0013__compatibility_views
SET search_path = ge, extensions, public;

SELECT set_config('app.zone', coalesce(nullif(current_setting('app.deployment_region', true), ''), 'IN'), false);

SELECT set_config('app.deployment_region', coalesce(nullif(current_setting('app.deployment_region', true), ''), 'IN'), false);

CREATE VIEW ge.growth_source WITH (security_invoker = true) AS
  SELECT tenant_id, startup_id AS company_id, id AS id, schema_ref AS schema_ref, revision AS version, state AS status,
         payload AS payload, evidence_refs AS evidence_refs, created_by AS created_by,
         created_at AS created_at, updated_at AS updated_at FROM ge.intel_source;

GRANT SELECT ON ge.growth_source TO app_rw, app_worker, app_readonly;

CREATE VIEW ge.growth_source_policy WITH (security_invoker = true) AS
  SELECT tenant_id, startup_id AS company_id, id AS id, schema_ref AS schema_ref, revision AS version, status AS status,
         payload AS payload, evidence_refs AS evidence_refs, created_by AS created_by,
         created_at AS created_at, updated_at AS updated_at FROM ge.intel_source_policy;

GRANT SELECT ON ge.growth_source_policy TO app_rw, app_worker, app_readonly;

CREATE VIEW ge.growth_source_record WITH (security_invoker = true) AS
  SELECT tenant_id, startup_id AS company_id, id AS id, schema_ref AS schema_ref, revision AS version, NULL::text AS status,
         payload AS payload, evidence_refs AS evidence_refs, created_by AS created_by,
         created_at AS created_at, updated_at AS updated_at FROM ge.intel_source_record;

GRANT SELECT ON ge.growth_source_record TO app_rw, app_worker, app_readonly;

CREATE VIEW ge.growth_evidence WITH (security_invoker = true) AS
  SELECT tenant_id, startup_id AS company_id, id AS id, schema_ref AS schema_ref, revision AS version, NULL::text AS status,
         payload AS payload, evidence_refs AS evidence_refs, created_by AS created_by,
         created_at AS created_at, updated_at AS updated_at FROM ge.intel_evidence;

GRANT SELECT ON ge.growth_evidence TO app_rw, app_worker, app_readonly;

CREATE VIEW ge.growth_competitor WITH (security_invoker = true) AS
  SELECT tenant_id, startup_id AS company_id, id AS id, schema_ref AS schema_ref, revision AS version, NULL::text AS status,
         payload AS payload, evidence_refs AS evidence_refs, created_by AS created_by,
         created_at AS created_at, updated_at AS updated_at FROM ge.intel_competitor;

GRANT SELECT ON ge.growth_competitor TO app_rw, app_worker, app_readonly;

CREATE VIEW ge.growth_market_event WITH (security_invoker = true) AS
  SELECT tenant_id, startup_id AS company_id, id AS id, schema_ref AS schema_ref, revision AS version, NULL::text AS status,
         payload AS payload, evidence_refs AS evidence_refs, created_by AS created_by,
         created_at AS created_at, updated_at AS updated_at FROM ge.intel_market_event;

GRANT SELECT ON ge.growth_market_event TO app_rw, app_worker, app_readonly;

CREATE VIEW ge.growth_search_plan WITH (security_invoker = true) AS
  SELECT tenant_id, startup_id AS company_id, id AS id, schema_ref AS schema_ref, revision AS version, status AS status,
         payload AS payload, evidence_refs AS evidence_refs, created_by AS created_by,
         created_at AS created_at, updated_at AS updated_at FROM ge.intel_search_plan;

GRANT SELECT ON ge.growth_search_plan TO app_rw, app_worker, app_readonly;

CREATE VIEW ge.growth_organization WITH (security_invoker = true) AS
  SELECT tenant_id, startup_id AS company_id, id AS id, schema_ref AS schema_ref, revision AS version, NULL::text AS status,
         payload AS payload, evidence_refs AS evidence_refs, created_by AS created_by,
         created_at AS created_at, updated_at AS updated_at FROM ge.intel_organization;

GRANT SELECT ON ge.growth_organization TO app_rw, app_worker, app_readonly;

CREATE VIEW ge.growth_signal WITH (security_invoker = true) AS
  SELECT tenant_id, startup_id AS company_id, id AS id, schema_ref AS schema_ref, revision AS version, state AS status,
         payload AS payload, evidence_refs AS evidence_refs, created_by AS created_by,
         created_at AS created_at, updated_at AS updated_at FROM ge.intel_signal;

GRANT SELECT ON ge.growth_signal TO app_rw, app_worker, app_readonly;

CREATE VIEW ge.growth_signal_type WITH (security_invoker = true) AS
  SELECT tenant_id, startup_id AS company_id, id AS id, schema_ref AS schema_ref, revision AS version, NULL::text AS status,
         payload AS payload, evidence_refs AS evidence_refs, created_by AS created_by,
         created_at AS created_at, updated_at AS updated_at FROM ge.intel_signal_type;

GRANT SELECT ON ge.growth_signal_type TO app_rw, app_worker, app_readonly;

CREATE VIEW ge.growth_need_evidence WITH (security_invoker = true) AS
  SELECT tenant_id, startup_id AS company_id, id AS id, schema_ref AS schema_ref, 1 AS version, NULL::text AS status,
         payload AS payload, evidence_refs AS evidence_refs, created_by AS created_by,
         created_at AS created_at, created_at AS updated_at FROM ge.intel_need_evidence;

GRANT SELECT ON ge.growth_need_evidence TO app_rw, app_worker, app_readonly;

CREATE VIEW ge.growth_referral WITH (security_invoker = true) AS
  SELECT tenant_id, startup_id AS company_id, id AS id, schema_ref AS schema_ref, revision AS version, state AS status,
         payload AS payload, evidence_refs AS evidence_refs, created_by AS created_by,
         created_at AS created_at, updated_at AS updated_at FROM ge.mkt_referral;

GRANT SELECT ON ge.growth_referral TO app_rw, app_worker, app_readonly;

CREATE VIEW ge.growth_contact WITH (security_invoker = true) AS
  SELECT tenant_id, startup_id AS company_id, id AS id, schema_ref AS schema_ref, revision AS version, NULL::text AS status,
         payload AS payload, evidence_refs AS evidence_refs, created_by AS created_by,
         created_at AS created_at, updated_at AS updated_at FROM ge.intel_contact;

GRANT SELECT ON ge.growth_contact TO app_rw, app_worker, app_readonly;

CREATE VIEW ge.growth_contact_source WITH (security_invoker = true) AS
  SELECT tenant_id, startup_id AS company_id, id AS id, schema_ref AS schema_ref, 1 AS version, NULL::text AS status,
         payload AS payload, evidence_refs AS evidence_refs, created_by AS created_by,
         created_at AS created_at, created_at AS updated_at FROM ge.intel_contact_source;

GRANT SELECT ON ge.growth_contact_source TO app_rw, app_worker, app_readonly;

CREATE VIEW ge.growth_contact_verification WITH (security_invoker = true) AS
  SELECT tenant_id, startup_id AS company_id, id AS id, schema_ref AS schema_ref, 1 AS version, NULL::text AS status,
         payload AS payload, evidence_refs AS evidence_refs, created_by AS created_by,
         created_at AS created_at, created_at AS updated_at FROM ge.intel_contact_verification;

GRANT SELECT ON ge.growth_contact_verification TO app_rw, app_worker, app_readonly;

CREATE VIEW ge.growth_need WITH (security_invoker = true) AS
  SELECT tenant_id, startup_id AS company_id, id AS id, schema_ref AS schema_ref, revision AS version, state AS status,
         payload AS payload, evidence_refs AS evidence_refs, created_by AS created_by,
         created_at AS created_at, updated_at AS updated_at FROM ge.intel_need;

GRANT SELECT ON ge.growth_need TO app_rw, app_worker, app_readonly;

CREATE VIEW ge.growth_opportunity WITH (security_invoker = true) AS
  SELECT tenant_id, startup_id AS company_id, id AS id, schema_ref AS schema_ref, revision AS version, state AS status,
         payload AS payload, evidence_refs AS evidence_refs, created_by AS created_by,
         created_at AS created_at, updated_at AS updated_at FROM ge.intel_opportunity;

GRANT SELECT ON ge.growth_opportunity TO app_rw, app_worker, app_readonly;

CREATE VIEW ge.growth_score_version WITH (security_invoker = true) AS
  SELECT tenant_id, startup_id AS company_id, id AS id, schema_ref AS schema_ref, 1 AS version, NULL::text AS status,
         payload AS payload, evidence_refs AS evidence_refs, created_by AS created_by,
         created_at AS created_at, created_at AS updated_at FROM ge.intel_score_version;

GRANT SELECT ON ge.growth_score_version TO app_rw, app_worker, app_readonly;

CREATE VIEW ge.growth_activity WITH (security_invoker = true) AS
  SELECT tenant_id, startup_id AS company_id, id AS id, schema_ref AS schema_ref, 1 AS version, NULL::text AS status,
         payload AS payload, evidence_refs AS evidence_refs, created_by AS created_by,
         created_at AS created_at, created_at AS updated_at FROM ge.crm_activity;

GRANT SELECT ON ge.growth_activity TO app_rw, app_worker, app_readonly;

CREATE VIEW ge.growth_deal WITH (security_invoker = true) AS
  SELECT tenant_id, startup_id AS company_id, id AS id, schema_ref AS schema_ref, revision AS version, NULL::text AS status,
         payload AS payload, evidence_refs AS evidence_refs, created_by AS created_by,
         created_at AS created_at, updated_at AS updated_at FROM ge.crm_deal;

GRANT SELECT ON ge.growth_deal TO app_rw, app_worker, app_readonly;

CREATE VIEW ge.growth_stage WITH (security_invoker = true) AS
  SELECT tenant_id, startup_id AS company_id, id AS id, schema_ref AS schema_ref, revision AS version, status AS status,
         payload AS payload, evidence_refs AS evidence_refs, created_by AS created_by,
         created_at AS created_at, updated_at AS updated_at FROM ge.crm_stage;

GRANT SELECT ON ge.growth_stage TO app_rw, app_worker, app_readonly;

CREATE VIEW ge.growth_task WITH (security_invoker = true) AS
  SELECT tenant_id, startup_id AS company_id, id AS id, schema_ref AS schema_ref, revision AS version, state AS status,
         payload AS payload, evidence_refs AS evidence_refs, created_by AS created_by,
         created_at AS created_at, updated_at AS updated_at FROM ge.lcy_task;

GRANT SELECT ON ge.growth_task TO app_rw, app_worker, app_readonly;

CREATE VIEW ge.growth_budget WITH (security_invoker = true) AS
  SELECT tenant_id, NULL::uuid AS company_id, period AS id, NULL::text AS schema_ref, 1 AS version, NULL::text AS status,
         '{}'::jsonb AS payload, '{}'::uuid[] AS evidence_refs, NULL::uuid AS created_by,
         NULL::timestamptz AS created_at, NULL::timestamptz AS updated_at FROM ge.ai_budget;

GRANT SELECT ON ge.growth_budget TO app_rw, app_worker, app_readonly;

CREATE VIEW ge.growth_message WITH (security_invoker = true) AS
  SELECT tenant_id, startup_id AS company_id, id AS id, schema_ref AS schema_ref, revision AS version, state AS status,
         payload AS payload, evidence_refs AS evidence_refs, created_by AS created_by,
         created_at AS created_at, updated_at AS updated_at FROM ge.eng_message;

GRANT SELECT ON ge.growth_message TO app_rw, app_worker, app_readonly;

CREATE VIEW ge.growth_message_draft WITH (security_invoker = true) AS
  SELECT tenant_id, startup_id AS company_id, id AS id, schema_ref AS schema_ref, revision AS version, state AS status,
         payload AS payload, evidence_refs AS evidence_refs, created_by AS created_by,
         created_at AS created_at, updated_at AS updated_at FROM ge.eng_message_draft;

GRANT SELECT ON ge.growth_message_draft TO app_rw, app_worker, app_readonly;

CREATE VIEW ge.growth_message_template WITH (security_invoker = true) AS
  SELECT tenant_id, startup_id AS company_id, id AS id, schema_ref AS schema_ref, revision AS version, status AS status,
         payload AS payload, evidence_refs AS evidence_refs, created_by AS created_by,
         created_at AS created_at, updated_at AS updated_at FROM ge.eng_message_template;

GRANT SELECT ON ge.growth_message_template TO app_rw, app_worker, app_readonly;

CREATE VIEW ge.growth_delivery_event WITH (security_invoker = true) AS
  SELECT tenant_id, startup_id AS company_id, id AS id, schema_ref AS schema_ref, 1 AS version, NULL::text AS status,
         payload AS payload, evidence_refs AS evidence_refs, created_by AS created_by,
         created_at AS created_at, created_at AS updated_at FROM ge.eng_delivery_event;

GRANT SELECT ON ge.growth_delivery_event TO app_rw, app_worker, app_readonly;

CREATE VIEW ge.growth_thread WITH (security_invoker = true) AS
  SELECT tenant_id, startup_id AS company_id, id AS id, schema_ref AS schema_ref, revision AS version, state AS status,
         payload AS payload, evidence_refs AS evidence_refs, created_by AS created_by,
         created_at AS created_at, updated_at AS updated_at FROM ge.eng_thread;

GRANT SELECT ON ge.growth_thread TO app_rw, app_worker, app_readonly;

CREATE VIEW ge.growth_inbound_event WITH (security_invoker = true) AS
  SELECT tenant_id, startup_id AS company_id, id AS id, schema_ref AS schema_ref, 1 AS version, NULL::text AS status,
         payload AS payload, evidence_refs AS evidence_refs, created_by AS created_by,
         created_at AS created_at, created_at AS updated_at FROM ge.eng_inbound_event;

GRANT SELECT ON ge.growth_inbound_event TO app_rw, app_worker, app_readonly;

CREATE VIEW ge.growth_enrollment WITH (security_invoker = true) AS
  SELECT tenant_id, startup_id AS company_id, id AS id, schema_ref AS schema_ref, revision AS version, state AS status,
         payload AS payload, evidence_refs AS evidence_refs, created_by AS created_by,
         created_at AS created_at, updated_at AS updated_at FROM ge.eng_enrollment;

GRANT SELECT ON ge.growth_enrollment TO app_rw, app_worker, app_readonly;

CREATE VIEW ge.growth_sequence WITH (security_invoker = true) AS
  SELECT tenant_id, startup_id AS company_id, id AS id, schema_ref AS schema_ref, revision AS version, status AS status,
         payload AS payload, evidence_refs AS evidence_refs, created_by AS created_by,
         created_at AS created_at, updated_at AS updated_at FROM ge.eng_sequence;

GRANT SELECT ON ge.growth_sequence TO app_rw, app_worker, app_readonly;

CREATE VIEW ge.growth_sequence_step WITH (security_invoker = true) AS
  SELECT tenant_id, startup_id AS company_id, id AS id, schema_ref AS schema_ref, revision AS version, status AS status,
         payload AS payload, evidence_refs AS evidence_refs, created_by AS created_by,
         created_at AS created_at, updated_at AS updated_at FROM ge.eng_sequence_step;

GRANT SELECT ON ge.growth_sequence_step TO app_rw, app_worker, app_readonly;

CREATE VIEW ge.growth_routing_rule WITH (security_invoker = true) AS
  SELECT tenant_id, startup_id AS company_id, id AS id, schema_ref AS schema_ref, revision AS version, status AS status,
         payload AS payload, evidence_refs AS evidence_refs, created_by AS created_by,
         created_at AS created_at, updated_at AS updated_at FROM ge.eng_routing_rule;

GRANT SELECT ON ge.growth_routing_rule TO app_rw, app_worker, app_readonly;

CREATE VIEW ge.growth_identity_link WITH (security_invoker = true) AS
  SELECT tenant_id, startup_id AS company_id, id AS id, schema_ref AS schema_ref, revision AS version, NULL::text AS status,
         payload AS payload, evidence_refs AS evidence_refs, created_by AS created_by,
         created_at AS created_at, updated_at AS updated_at FROM ge.eng_identity_link;

GRANT SELECT ON ge.growth_identity_link TO app_rw, app_worker, app_readonly;

CREATE VIEW ge.growth_objection WITH (security_invoker = true) AS
  SELECT tenant_id, startup_id AS company_id, id AS id, schema_ref AS schema_ref, revision AS version, state AS status,
         payload AS payload, evidence_refs AS evidence_refs, created_by AS created_by,
         created_at AS created_at, updated_at AS updated_at FROM ge.com_objection;

GRANT SELECT ON ge.growth_objection TO app_rw, app_worker, app_readonly;

CREATE VIEW ge.growth_calendar_link WITH (security_invoker = true) AS
  SELECT tenant_id, startup_id AS company_id, id AS id, schema_ref AS schema_ref, revision AS version, NULL::text AS status,
         payload AS payload, evidence_refs AS evidence_refs, created_by AS created_by,
         created_at AS created_at, updated_at AS updated_at FROM ge.eng_calendar_link;

GRANT SELECT ON ge.growth_calendar_link TO app_rw, app_worker, app_readonly;

CREATE VIEW ge.growth_meeting WITH (security_invoker = true) AS
  SELECT tenant_id, startup_id AS company_id, id AS id, schema_ref AS schema_ref, revision AS version, state AS status,
         payload AS payload, evidence_refs AS evidence_refs, created_by AS created_by,
         created_at AS created_at, updated_at AS updated_at FROM ge.eng_meeting;

GRANT SELECT ON ge.growth_meeting TO app_rw, app_worker, app_readonly;

CREATE VIEW ge.growth_business_event WITH (security_invoker = true) AS
  SELECT tenant_id, startup_id AS company_id, id AS id, schema_ref AS schema_ref, revision AS version, state AS status,
         payload AS payload, evidence_refs AS evidence_refs, created_by AS created_by,
         created_at AS created_at, updated_at AS updated_at FROM ge.mkt_event;

GRANT SELECT ON ge.growth_business_event TO app_rw, app_worker, app_readonly;

CREATE VIEW ge.growth_event_attendance WITH (security_invoker = true) AS
  SELECT tenant_id, startup_id AS company_id, id AS id, schema_ref AS schema_ref, 1 AS version, NULL::text AS status,
         payload AS payload, evidence_refs AS evidence_refs, created_by AS created_by,
         created_at AS created_at, created_at AS updated_at FROM ge.mkt_attendance;

GRANT SELECT ON ge.growth_event_attendance TO app_rw, app_worker, app_readonly;

CREATE VIEW ge.growth_event_registration WITH (security_invoker = true) AS
  SELECT tenant_id, startup_id AS company_id, id AS id, schema_ref AS schema_ref, revision AS version, state AS status,
         payload AS payload, evidence_refs AS evidence_refs, created_by AS created_by,
         created_at AS created_at, updated_at AS updated_at FROM ge.mkt_registration;

GRANT SELECT ON ge.growth_event_registration TO app_rw, app_worker, app_readonly;

CREATE VIEW ge.growth_claim WITH (security_invoker = true) AS
  SELECT tenant_id, startup_id AS company_id, id AS id, schema_ref AS schema_ref, revision AS version, status AS status,
         payload AS payload, evidence_refs AS evidence_refs, created_by AS created_by,
         created_at AS created_at, updated_at AS updated_at FROM ge.cat_claim;

GRANT SELECT ON ge.growth_claim TO app_rw, app_worker, app_readonly;

CREATE VIEW ge.growth_content_asset WITH (security_invoker = true) AS
  SELECT tenant_id, startup_id AS company_id, id AS id, schema_ref AS schema_ref, revision AS version, state AS status,
         payload AS payload, evidence_refs AS evidence_refs, created_by AS created_by,
         created_at AS created_at, updated_at AS updated_at FROM ge.mkt_content_asset;

GRANT SELECT ON ge.growth_content_asset TO app_rw, app_worker, app_readonly;

CREATE VIEW ge.growth_content_version WITH (security_invoker = true) AS
  SELECT tenant_id, startup_id AS company_id, id AS id, schema_ref AS schema_ref, revision AS version, status AS status,
         payload AS payload, evidence_refs AS evidence_refs, created_by AS created_by,
         created_at AS created_at, updated_at AS updated_at FROM ge.mkt_content_version;

GRANT SELECT ON ge.growth_content_version TO app_rw, app_worker, app_readonly;

CREATE VIEW ge.growth_approval WITH (security_invoker = true) AS
  SELECT tenant_id, startup_id AS company_id, id AS id, schema_ref AS schema_ref, 1 AS version, NULL::text AS status,
         payload AS payload, evidence_refs AS evidence_refs, created_by AS created_by,
         created_at AS created_at, created_at AS updated_at FROM ge.gov_approval;

GRANT SELECT ON ge.growth_approval TO app_rw, app_worker, app_readonly;

CREATE VIEW ge.growth_social_post WITH (security_invoker = true) AS
  SELECT tenant_id, startup_id AS company_id, id AS id, schema_ref AS schema_ref, revision AS version, NULL::text AS status,
         payload AS payload, evidence_refs AS evidence_refs, created_by AS created_by,
         created_at AS created_at, updated_at AS updated_at FROM ge.intel_social_post;

GRANT SELECT ON ge.growth_social_post TO app_rw, app_worker, app_readonly;

CREATE VIEW ge.growth_social_publication WITH (security_invoker = true) AS
  SELECT tenant_id, startup_id AS company_id, id AS id, schema_ref AS schema_ref, revision AS version, state AS status,
         payload AS payload, evidence_refs AS evidence_refs, created_by AS created_by,
         created_at AS created_at, updated_at AS updated_at FROM ge.mkt_social_publication;

GRANT SELECT ON ge.growth_social_publication TO app_rw, app_worker, app_readonly;

CREATE VIEW ge.growth_keyword WITH (security_invoker = true) AS
  SELECT tenant_id, startup_id AS company_id, id AS id, schema_ref AS schema_ref, revision AS version, NULL::text AS status,
         payload AS payload, evidence_refs AS evidence_refs, created_by AS created_by,
         created_at AS created_at, updated_at AS updated_at FROM ge.mkt_keyword;

GRANT SELECT ON ge.growth_keyword TO app_rw, app_worker, app_readonly;

CREATE VIEW ge.growth_page_metric WITH (security_invoker = true) AS
  SELECT tenant_id, startup_id AS company_id, id AS id, schema_ref AS schema_ref, 1 AS version, NULL::text AS status,
         payload AS payload, evidence_refs AS evidence_refs, created_by AS created_by,
         created_at AS created_at, created_at AS updated_at FROM ge.mkt_page_metric;

GRANT SELECT ON ge.growth_page_metric TO app_rw, app_worker, app_readonly;

CREATE VIEW ge.growth_seo_issue WITH (security_invoker = true) AS
  SELECT tenant_id, startup_id AS company_id, id AS id, schema_ref AS schema_ref, revision AS version, state AS status,
         payload AS payload, evidence_refs AS evidence_refs, created_by AS created_by,
         created_at AS created_at, updated_at AS updated_at FROM ge.mkt_seo_issue;

GRANT SELECT ON ge.growth_seo_issue TO app_rw, app_worker, app_readonly;

CREATE VIEW ge.growth_landing_page WITH (security_invoker = true) AS
  SELECT tenant_id, startup_id AS company_id, id AS id, schema_ref AS schema_ref, revision AS version, NULL::text AS status,
         payload AS payload, evidence_refs AS evidence_refs, created_by AS created_by,
         created_at AS created_at, updated_at AS updated_at FROM ge.mkt_landing_page;

GRANT SELECT ON ge.growth_landing_page TO app_rw, app_worker, app_readonly;

CREATE VIEW ge.growth_audience WITH (security_invoker = true) AS
  SELECT tenant_id, startup_id AS company_id, id AS id, schema_ref AS schema_ref, revision AS version, status AS status,
         payload AS payload, evidence_refs AS evidence_refs, created_by AS created_by,
         created_at AS created_at, updated_at AS updated_at FROM ge.mkt_audience;

GRANT SELECT ON ge.growth_audience TO app_rw, app_worker, app_readonly;

CREATE VIEW ge.growth_campaign WITH (security_invoker = true) AS
  SELECT tenant_id, startup_id AS company_id, id AS id, schema_ref AS schema_ref, revision AS version, state AS status,
         payload AS payload, evidence_refs AS evidence_refs, created_by AS created_by,
         created_at AS created_at, updated_at AS updated_at FROM ge.mkt_campaign;

GRANT SELECT ON ge.growth_campaign TO app_rw, app_worker, app_readonly;

CREATE VIEW ge.growth_campaign_version WITH (security_invoker = true) AS
  SELECT tenant_id, startup_id AS company_id, id AS id, schema_ref AS schema_ref, revision AS version, status AS status,
         payload AS payload, evidence_refs AS evidence_refs, created_by AS created_by,
         created_at AS created_at, updated_at AS updated_at FROM ge.mkt_campaign_version;

GRANT SELECT ON ge.growth_campaign_version TO app_rw, app_worker, app_readonly;

CREATE VIEW ge.growth_ad_campaign WITH (security_invoker = true) AS
  SELECT tenant_id, startup_id AS company_id, id AS id, schema_ref AS schema_ref, revision AS version, state AS status,
         payload AS payload, evidence_refs AS evidence_refs, created_by AS created_by,
         created_at AS created_at, updated_at AS updated_at FROM ge.mkt_ad_campaign;

GRANT SELECT ON ge.growth_ad_campaign TO app_rw, app_worker, app_readonly;

CREATE VIEW ge.growth_ad_spend_event WITH (security_invoker = true) AS
  SELECT tenant_id, startup_id AS company_id, id AS id, schema_ref AS schema_ref, 1 AS version, NULL::text AS status,
         payload AS payload, evidence_refs AS evidence_refs, created_by AS created_by,
         created_at AS created_at, created_at AS updated_at FROM ge.mkt_spend_event;

GRANT SELECT ON ge.growth_ad_spend_event TO app_rw, app_worker, app_readonly;

CREATE VIEW ge.growth_attribution_event WITH (security_invoker = true) AS
  SELECT tenant_id, startup_id AS company_id, id AS id, schema_ref AS schema_ref, 1 AS version, NULL::text AS status,
         payload AS payload, evidence_refs AS evidence_refs, created_by AS created_by,
         created_at AS created_at, created_at AS updated_at FROM ge.mkt_attribution_event;

GRANT SELECT ON ge.growth_attribution_event TO app_rw, app_worker, app_readonly;

CREATE VIEW ge.growth_form WITH (security_invoker = true) AS
  SELECT tenant_id, startup_id AS company_id, id AS id, schema_ref AS schema_ref, revision AS version, NULL::text AS status,
         payload AS payload, evidence_refs AS evidence_refs, created_by AS created_by,
         created_at AS created_at, updated_at AS updated_at FROM ge.crm_form;

GRANT SELECT ON ge.growth_form TO app_rw, app_worker, app_readonly;

CREATE VIEW ge.growth_lead WITH (security_invoker = true) AS
  SELECT tenant_id, startup_id AS company_id, id AS id, schema_ref AS schema_ref, revision AS version, state AS status,
         payload AS payload, evidence_refs AS evidence_refs, created_by AS created_by,
         created_at AS created_at, updated_at AS updated_at FROM ge.crm_lead;

GRANT SELECT ON ge.growth_lead TO app_rw, app_worker, app_readonly;

CREATE VIEW ge.growth_proposal WITH (security_invoker = true) AS
  SELECT tenant_id, startup_id AS company_id, id AS id, schema_ref AS schema_ref, revision AS version, state AS status,
         payload AS payload, evidence_refs AS evidence_refs, created_by AS created_by,
         created_at AS created_at, updated_at AS updated_at FROM ge.com_proposal;

GRANT SELECT ON ge.growth_proposal TO app_rw, app_worker, app_readonly;

CREATE VIEW ge.growth_proposal_version WITH (security_invoker = true) AS
  SELECT tenant_id, startup_id AS company_id, id AS id, schema_ref AS schema_ref, revision AS version, status AS status,
         payload AS payload, evidence_refs AS evidence_refs, created_by AS created_by,
         created_at AS created_at, updated_at AS updated_at FROM ge.com_proposal_version;

GRANT SELECT ON ge.growth_proposal_version TO app_rw, app_worker, app_readonly;

CREATE VIEW ge.growth_quote WITH (security_invoker = true) AS
  SELECT tenant_id, startup_id AS company_id, id AS id, schema_ref AS schema_ref, revision AS version, state AS status,
         payload AS payload, evidence_refs AS evidence_refs, created_by AS created_by,
         created_at AS created_at, updated_at AS updated_at FROM ge.com_quote;

GRANT SELECT ON ge.growth_quote TO app_rw, app_worker, app_readonly;

CREATE VIEW ge.growth_quote_line WITH (security_invoker = true) AS
  SELECT tenant_id, startup_id AS company_id, id AS id, schema_ref AS schema_ref, revision AS version, NULL::text AS status,
         payload AS payload, evidence_refs AS evidence_refs, created_by AS created_by,
         created_at AS created_at, updated_at AS updated_at FROM ge.com_quote_line;

GRANT SELECT ON ge.growth_quote_line TO app_rw, app_worker, app_readonly;

CREATE VIEW ge.growth_negotiation WITH (security_invoker = true) AS
  SELECT tenant_id, startup_id AS company_id, id AS id, schema_ref AS schema_ref, revision AS version, state AS status,
         payload AS payload, evidence_refs AS evidence_refs, created_by AS created_by,
         created_at AS created_at, updated_at AS updated_at FROM ge.com_negotiation;

GRANT SELECT ON ge.growth_negotiation TO app_rw, app_worker, app_readonly;

CREATE VIEW ge.growth_contract WITH (security_invoker = true) AS
  SELECT tenant_id, startup_id AS company_id, id AS id, schema_ref AS schema_ref, revision AS version, state AS status,
         payload AS payload, evidence_refs AS evidence_refs, created_by AS created_by,
         created_at AS created_at, updated_at AS updated_at FROM ge.com_contract;

GRANT SELECT ON ge.growth_contract TO app_rw, app_worker, app_readonly;

CREATE VIEW ge.growth_integration_deal WITH (security_invoker = true) AS
  SELECT tenant_id, startup_id AS company_id, id AS id, schema_ref AS schema_ref, revision AS version, state AS status,
         payload AS payload, evidence_refs AS evidence_refs, created_by AS created_by,
         created_at AS created_at, updated_at AS updated_at FROM ge.lcy_integration_deal;

GRANT SELECT ON ge.growth_integration_deal TO app_rw, app_worker, app_readonly;

CREATE VIEW ge.sales_bid WITH (security_invoker = true) AS
  SELECT tenant_id, startup_id AS company_id, id AS id, schema_ref AS schema_ref, revision AS version, state AS status,
         payload AS payload, evidence_refs AS evidence_refs, created_by AS created_by,
         created_at AS created_at, updated_at AS updated_at FROM ge.com_bid;

GRANT SELECT ON ge.sales_bid TO app_rw, app_worker, app_readonly;

CREATE VIEW ge.growth_invoice WITH (security_invoker = true) AS
  SELECT tenant_id, startup_id AS company_id, id AS id, schema_ref AS schema_ref, revision AS version, state AS status,
         payload AS payload, evidence_refs AS evidence_refs, created_by AS created_by,
         created_at AS created_at, updated_at AS updated_at FROM ge.com_invoice;

GRANT SELECT ON ge.growth_invoice TO app_rw, app_worker, app_readonly;

CREATE VIEW ge.growth_payment WITH (security_invoker = true) AS
  SELECT tenant_id, startup_id AS company_id, id AS id, schema_ref AS schema_ref, revision AS version, state AS status,
         payload AS payload, evidence_refs AS evidence_refs, created_by AS created_by,
         created_at AS created_at, updated_at AS updated_at FROM ge.com_payment;

GRANT SELECT ON ge.growth_payment TO app_rw, app_worker, app_readonly;

CREATE VIEW ge.sales_fulfillment WITH (security_invoker = true) AS
  SELECT tenant_id, startup_id AS company_id, id AS id, schema_ref AS schema_ref, 1 AS version, NULL::text AS status,
         payload AS payload, evidence_refs AS evidence_refs, created_by AS created_by,
         created_at AS created_at, created_at AS updated_at FROM ge.com_fulfillment_event;

GRANT SELECT ON ge.sales_fulfillment TO app_rw, app_worker, app_readonly;

CREATE VIEW ge.sales_order WITH (security_invoker = true) AS
  SELECT tenant_id, startup_id AS company_id, id AS id, schema_ref AS schema_ref, revision AS version, state AS status,
         payload AS payload, evidence_refs AS evidence_refs, created_by AS created_by,
         created_at AS created_at, updated_at AS updated_at FROM ge.com_order;

GRANT SELECT ON ge.sales_order TO app_rw, app_worker, app_readonly;

CREATE VIEW ge.sales_order_line WITH (security_invoker = true) AS
  SELECT tenant_id, startup_id AS company_id, id AS id, schema_ref AS schema_ref, revision AS version, NULL::text AS status,
         payload AS payload, evidence_refs AS evidence_refs, created_by AS created_by,
         created_at AS created_at, updated_at AS updated_at FROM ge.com_order_line;

GRANT SELECT ON ge.sales_order_line TO app_rw, app_worker, app_readonly;

CREATE VIEW ge.growth_onboarding WITH (security_invoker = true) AS
  SELECT tenant_id, startup_id AS company_id, id AS id, schema_ref AS schema_ref, revision AS version, state AS status,
         payload AS payload, evidence_refs AS evidence_refs, created_by AS created_by,
         created_at AS created_at, updated_at AS updated_at FROM ge.lcy_onboarding;

GRANT SELECT ON ge.growth_onboarding TO app_rw, app_worker, app_readonly;

CREATE VIEW ge.growth_deployment WITH (security_invoker = true) AS
  SELECT tenant_id, startup_id AS company_id, id AS id, schema_ref AS schema_ref, revision AS version, state AS status,
         payload AS payload, evidence_refs AS evidence_refs, created_by AS created_by,
         created_at AS created_at, updated_at AS updated_at FROM ge.lcy_deployment;

GRANT SELECT ON ge.growth_deployment TO app_rw, app_worker, app_readonly;

CREATE VIEW ge.growth_partner WITH (security_invoker = true) AS
  SELECT tenant_id, startup_id AS company_id, id AS id, schema_ref AS schema_ref, revision AS version, NULL::text AS status,
         payload AS payload, evidence_refs AS evidence_refs, created_by AS created_by,
         created_at AS created_at, updated_at AS updated_at FROM ge.lcy_partner;

GRANT SELECT ON ge.growth_partner TO app_rw, app_worker, app_readonly;

CREATE VIEW ge.growth_pilot WITH (security_invoker = true) AS
  SELECT tenant_id, startup_id AS company_id, id AS id, schema_ref AS schema_ref, revision AS version, state AS status,
         payload AS payload, evidence_refs AS evidence_refs, created_by AS created_by,
         created_at AS created_at, updated_at AS updated_at FROM ge.lcy_pilot;

GRANT SELECT ON ge.growth_pilot TO app_rw, app_worker, app_readonly;

CREATE VIEW ge.growth_renewal WITH (security_invoker = true) AS
  SELECT tenant_id, startup_id AS company_id, id AS id, schema_ref AS schema_ref, revision AS version, state AS status,
         payload AS payload, evidence_refs AS evidence_refs, created_by AS created_by,
         created_at AS created_at, updated_at AS updated_at FROM ge.lcy_renewal;

GRANT SELECT ON ge.growth_renewal TO app_rw, app_worker, app_readonly;

CREATE VIEW ge.growth_feedback WITH (security_invoker = true) AS
  SELECT tenant_id, startup_id AS company_id, id AS id, schema_ref AS schema_ref, 1 AS version, NULL::text AS status,
         payload AS payload, evidence_refs AS evidence_refs, created_by AS created_by,
         created_at AS created_at, created_at AS updated_at FROM ge.ai_feedback;

GRANT SELECT ON ge.growth_feedback TO app_rw, app_worker, app_readonly;

CREATE VIEW ge.growth_metric_snapshot WITH (security_invoker = true) AS
  SELECT tenant_id, startup_id AS company_id, id AS id, schema_ref AS schema_ref, 1 AS version, NULL::text AS status,
         payload AS payload, evidence_refs AS evidence_refs, created_by AS created_by,
         created_at AS created_at, created_at AS updated_at FROM ge.ana_metric_snapshot;

GRANT SELECT ON ge.growth_metric_snapshot TO app_rw, app_worker, app_readonly;

CREATE VIEW ge.growth_forecast WITH (security_invoker = true) AS
  SELECT tenant_id, startup_id AS company_id, id AS id, schema_ref AS schema_ref, 1 AS version, NULL::text AS status,
         payload AS payload, evidence_refs AS evidence_refs, created_by AS created_by,
         created_at AS created_at, created_at AS updated_at FROM ge.ana_forecast;

GRANT SELECT ON ge.growth_forecast TO app_rw, app_worker, app_readonly;

CREATE VIEW ge.growth_stage_metric WITH (security_invoker = true) AS
  SELECT tenant_id, startup_id AS company_id, id AS id, schema_ref AS schema_ref, 1 AS version, NULL::text AS status,
         payload AS payload, evidence_refs AS evidence_refs, created_by AS created_by,
         created_at AS created_at, created_at AS updated_at FROM ge.ana_stage_metric;

GRANT SELECT ON ge.growth_stage_metric TO app_rw, app_worker, app_readonly;

CREATE VIEW ge.growth_document WITH (security_invoker = true) AS
  SELECT tenant_id, startup_id AS company_id, id AS id, schema_ref AS schema_ref, revision AS version, status AS status,
         payload AS payload, evidence_refs AS evidence_refs, created_by AS created_by,
         created_at AS created_at, updated_at AS updated_at FROM ge.cat_document;

GRANT SELECT ON ge.growth_document TO app_rw, app_worker, app_readonly;

CREATE VIEW ge.growth_document_chunk WITH (security_invoker = true) AS
  SELECT tenant_id, startup_id AS company_id, id AS id, schema_ref AS schema_ref, 1 AS version, NULL::text AS status,
         payload AS payload, evidence_refs AS evidence_refs, created_by AS created_by,
         created_at AS created_at, created_at AS updated_at FROM ge.cat_chunk;

GRANT SELECT ON ge.growth_document_chunk TO app_rw, app_worker, app_readonly;

CREATE VIEW ge.growth_embedding WITH (security_invoker = true) AS
  SELECT tenant_id, startup_id AS company_id, id AS id, schema_ref AS schema_ref, 1 AS version, NULL::text AS status,
         payload AS payload, evidence_refs AS evidence_refs, created_by AS created_by,
         created_at AS created_at, created_at AS updated_at FROM ge.cat_embedding;

GRANT SELECT ON ge.growth_embedding TO app_rw, app_worker, app_readonly;

CREATE VIEW ge.ten_tenant WITH (security_invoker = true) AS SELECT tenant.*, tenant_id AS id FROM ge.tenant;

GRANT SELECT ON ge.ten_tenant TO app_rw, app_worker, app_readonly;

CREATE VIEW ge.ten_organization WITH (security_invoker = true) AS SELECT organization.*, organization_id AS id FROM ge.organization;

GRANT SELECT ON ge.ten_organization TO app_rw, app_worker, app_readonly;

CREATE VIEW ge.ten_startup WITH (security_invoker = true) AS SELECT company.*, company_id AS id, company_id AS startup_id FROM ge.company;

GRANT SELECT ON ge.ten_startup TO app_rw, app_worker, app_readonly;

CREATE VIEW ge.ten_business_line WITH (security_invoker = true) AS SELECT division.*, division_id AS id, company_id AS startup_id FROM ge.division;

GRANT SELECT ON ge.ten_business_line TO app_rw, app_worker, app_readonly;

CREATE VIEW ge.ten_brand WITH (security_invoker = true) AS SELECT brand.*, brand_id AS id, company_id AS startup_id FROM ge.brand;

GRANT SELECT ON ge.ten_brand TO app_rw, app_worker, app_readonly;

CREATE VIEW ge.cat_offering WITH (security_invoker = true) AS SELECT offering.*, offering_id AS id, company_id AS startup_id FROM ge.offering;

GRANT SELECT ON ge.cat_offering TO app_rw, app_worker, app_readonly;

CREATE VIEW ge.ten_market WITH (security_invoker = true) AS SELECT market.*, market_id AS id, company_id AS startup_id FROM ge.market;

GRANT SELECT ON ge.ten_market TO app_rw, app_worker, app_readonly;

CREATE VIEW ge.eng_channel_account WITH (security_invoker = true) AS SELECT channel_account.*, account_id AS id, company_id AS startup_id FROM ge.channel_account;

GRANT SELECT ON ge.eng_channel_account TO app_rw, app_worker, app_readonly;

CREATE VIEW ge.aut_run WITH (security_invoker = true) AS SELECT workflow_run.*, run_id AS id, company_id AS startup_id FROM ge.workflow_run;

GRANT SELECT ON ge.aut_run TO app_rw, app_worker, app_readonly;

CREATE VIEW ge.aut_step_run WITH (security_invoker = true) AS SELECT workflow_step_run.*, attempt AS id, company_id AS startup_id FROM ge.workflow_step_run;

GRANT SELECT ON ge.aut_step_run TO app_rw, app_worker, app_readonly;

CREATE VIEW ge.aut_effect WITH (security_invoker = true) AS SELECT effect.*, effect_id AS id, company_id AS startup_id FROM ge.effect;

GRANT SELECT ON ge.aut_effect TO app_rw, app_worker, app_readonly;

CREATE VIEW ge.ops_outbox WITH (security_invoker = true) AS SELECT outbox.*, event_id AS id, company_id AS startup_id FROM ge.outbox;

GRANT SELECT ON ge.ops_outbox TO app_rw, app_worker, app_readonly;

CREATE VIEW ge.int_provider_event_key WITH (security_invoker = true) AS SELECT inbox.*, provider_event_id AS id FROM ge.inbox;

GRANT SELECT ON ge.int_provider_event_key TO app_rw, app_worker, app_readonly;

CREATE VIEW ge.ops_audit_event WITH (security_invoker = true) AS SELECT audit_event.*, audit_id AS id, company_id AS startup_id FROM ge.audit_event;

GRANT SELECT ON ge.ops_audit_event TO app_rw, app_worker, app_readonly;

CREATE VIEW ge.ten_portfolio_grant WITH (security_invoker = true) AS SELECT portfolio_grant.*, grant_id AS id, company_id AS startup_id FROM ge.portfolio_grant;

GRANT SELECT ON ge.ten_portfolio_grant TO app_rw, app_worker, app_readonly;

CREATE VIEW ge.ana_fx_snapshot WITH (security_invoker = true) AS SELECT fx_rate.*, rate_id AS id FROM ge.fx_rate;

GRANT SELECT ON ge.ana_fx_snapshot TO app_rw, app_worker, app_readonly;

CREATE VIEW ge.gov_jurisdiction_pack WITH (security_invoker = true) AS SELECT jurisdiction_pack.*, pack_id AS id FROM ge.jurisdiction_pack;

GRANT SELECT ON ge.gov_jurisdiction_pack TO app_rw, app_worker, app_readonly;

CREATE VIEW ge.gov_jurisdiction_rule WITH (security_invoker = true) AS SELECT jurisdiction_rule.*, rule_id AS id FROM ge.jurisdiction_rule;

GRANT SELECT ON ge.gov_jurisdiction_rule TO app_rw, app_worker, app_readonly;

CREATE VIEW ge.gov_consent WITH (security_invoker = true) AS SELECT consent_record.*, consent_id AS id, company_id AS startup_id FROM ge.consent_record;

GRANT SELECT ON ge.gov_consent TO app_rw, app_worker, app_readonly;

CREATE VIEW ge.gov_suppression WITH (security_invoker = true) AS SELECT suppression.*, purpose AS id, company_id AS startup_id FROM ge.suppression;

GRANT SELECT ON ge.gov_suppression TO app_rw, app_worker, app_readonly;

CREATE VIEW ge.gov_privacy_request WITH (security_invoker = true) AS SELECT dsar_request.*, dsar_id AS id FROM ge.dsar_request;

GRANT SELECT ON ge.gov_privacy_request TO app_rw, app_worker, app_readonly;

CREATE VIEW ge.gov_compliance_incident WITH (security_invoker = true) AS SELECT incident.*, incident_id AS id FROM ge.incident;

GRANT SELECT ON ge.gov_compliance_incident TO app_rw, app_worker, app_readonly;

CREATE VIEW ge.gov_incident_notification WITH (security_invoker = true) AS SELECT incident_notification.*, authority AS id FROM ge.incident_notification;

GRANT SELECT ON ge.gov_incident_notification TO app_rw, app_worker, app_readonly;

CREATE VIEW ge.ai_prompt_version WITH (security_invoker = true) AS SELECT prompt_version.*, version AS id FROM ge.prompt_version;

GRANT SELECT ON ge.ai_prompt_version TO app_rw, app_worker, app_readonly;

CREATE VIEW ge.ai_eval_suite WITH (security_invoker = true) AS SELECT eval_suite.*, suite_id AS id FROM ge.eval_suite;

GRANT SELECT ON ge.ai_eval_suite TO app_rw, app_worker, app_readonly;

CREATE VIEW ge.ai_eval_run WITH (security_invoker = true) AS SELECT eval_run.*, eval_run_id AS id FROM ge.eval_run;

GRANT SELECT ON ge.ai_eval_run TO app_rw, app_worker, app_readonly;

CREATE VIEW ge.ai_usage WITH (security_invoker = true) AS SELECT ai_usage_event.*, usage_id AS id, company_id AS startup_id FROM ge.ai_usage_event;

GRANT SELECT ON ge.ai_usage TO app_rw, app_worker, app_readonly;

CREATE VIEW ge.sec_scim_token WITH (security_invoker = true) AS SELECT scim_token.*, token_id AS id FROM ge.scim_token;

GRANT SELECT ON ge.sec_scim_token TO app_rw, app_worker, app_readonly;

CREATE VIEW ge.ten_role WITH (security_invoker = true) AS SELECT custom_role.*, role_id AS id FROM ge.custom_role;

GRANT SELECT ON ge.ten_role TO app_rw, app_worker, app_readonly;

CREATE VIEW ge.ten_role_permission WITH (security_invoker = true) AS SELECT role_permission.*, permission AS id FROM ge.role_permission;

GRANT SELECT ON ge.ten_role_permission TO app_rw, app_worker, app_readonly;

CREATE VIEW ge.ref_sod_conflict WITH (security_invoker = true) AS SELECT sod_conflict.*, permission_b AS id FROM ge.sod_conflict;

GRANT SELECT ON ge.ref_sod_conflict TO app_rw, app_worker, app_readonly;

CREATE VIEW ge.saas_api_credential WITH (security_invoker = true) AS SELECT api_key.*, key_id AS id FROM ge.api_key;

GRANT SELECT ON ge.saas_api_credential TO app_rw, app_worker, app_readonly;

CREATE VIEW ge.saas_webhook_subscription WITH (security_invoker = true) AS SELECT webhook_endpoint.*, endpoint_id AS id FROM ge.webhook_endpoint;

GRANT SELECT ON ge.saas_webhook_subscription TO app_rw, app_worker, app_readonly;

CREATE VIEW ge.saas_webhook_delivery WITH (security_invoker = true) AS SELECT webhook_delivery.*, delivery_id AS id FROM ge.webhook_delivery;

GRANT SELECT ON ge.saas_webhook_delivery TO app_rw, app_worker, app_readonly;

CREATE VIEW ge.ops_audit_sink WITH (security_invoker = true) AS SELECT audit_sink.*, sink_id AS id FROM ge.audit_sink;

GRANT SELECT ON ge.ops_audit_sink TO app_rw, app_worker, app_readonly;

CREATE VIEW ge.saas_export_job WITH (security_invoker = true) AS SELECT export_job.*, export_id AS id FROM ge.export_job;

GRANT SELECT ON ge.saas_export_job TO app_rw, app_worker, app_readonly;

CREATE VIEW ge.ten_tenant_key WITH (security_invoker = true) AS SELECT tenant_key_config.*, tenant_id AS id FROM ge.tenant_key_config;

GRANT SELECT ON ge.ten_tenant_key TO app_rw, app_worker, app_readonly;

CREATE VIEW ge.saas_sandbox_environment WITH (security_invoker = true) AS SELECT sandbox_environment.*, sandbox_id AS id FROM ge.sandbox_environment;

GRANT SELECT ON ge.saas_sandbox_environment TO app_rw, app_worker, app_readonly;

CREATE VIEW ge.aut_config_promotion WITH (security_invoker = true) AS SELECT config_promotion.*, promotion_id AS id FROM ge.config_promotion;

GRANT SELECT ON ge.aut_config_promotion TO app_rw, app_worker, app_readonly;

CREATE VIEW ge.int_integration WITH (security_invoker = true) AS SELECT connector_installation.*, installation_id AS id FROM ge.connector_installation;

GRANT SELECT ON ge.int_integration TO app_rw, app_worker, app_readonly;

CREATE VIEW ge.sec_security_finding WITH (security_invoker = true) AS SELECT security_finding.*, finding_id AS id FROM ge.security_finding;

GRANT SELECT ON ge.sec_security_finding TO app_rw, app_worker, app_readonly;

CREATE VIEW ge.cat_tax_profile WITH (security_invoker = true) AS SELECT tax_rule.*, rule_id AS id FROM ge.tax_rule;

GRANT SELECT ON ge.cat_tax_profile TO app_rw, app_worker, app_readonly;

CREATE VIEW ge.saas_service_invoice WITH (security_invoker = true) AS SELECT invoice.*, invoice_id AS id FROM ge.invoice;

GRANT SELECT ON ge.saas_service_invoice TO app_rw, app_worker, app_readonly;

CREATE VIEW ge.ref_locale_bundle WITH (security_invoker = true) AS SELECT locale_bundle.*, locale AS id FROM ge.locale_bundle;

GRANT SELECT ON ge.ref_locale_bundle TO app_rw, app_worker, app_readonly;
