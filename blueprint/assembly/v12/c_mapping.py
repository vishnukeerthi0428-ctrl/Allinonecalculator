# -*- coding: utf-8 -*-
"""Hand-authored blueprint mapping for V12 SM-SVC-01..20 workflows (Group R3a, letter C).
Status codes: C = capability covered in blueprint, P = partially covered, N = not covered."""

SVC = {
 '01': dict(epic='05', bpwf='WF-02', actors='R04 Research Analyst (requester), R02 Startup Head (source/claim approver), R10 Legal (source rights), R19 service identity, R20 AI agent identity',
   ag='AG-003 Research Query Planner, AG-004 Evidence Extractor, AG-005 Buying Signal Classifier, AG-027 Market & Competitor Watch Summarizer, AG-041 Signal and Intent Fusion Analyst',
   au='AU-007 source permission, AU-014 URL/blocked-host filter, AU-005 untrusted-content sanitizer, AU-019 research review assignment, AU-001 gateway router, AU-002 budget reservation',
   brl='BRL-SRC-01…07, BRL-SRC-09, BRL-SRC-10, BRL-AI-03/04', dclass='Public / Internal (Tier 2 eligible only for public-source, non-personal text with opt-in, DEC-020 flag OFF by default)',
   tables='growth_source→intel_source; growth_source_policy→intel_source_policy; growth_source_record→intel_source_record; growth_evidence→intel_evidence; growth_competitor→intel_competitor; growth_market_event→intel_market_event'),
 '02': dict(epic='05', bpwf='WF-02 (+ WF-30 partner discovery for WF02)', actors='R04 Research Analyst, R02 Startup Head, R03 Growth Manager (opportunity owner), R19, R20',
   ag='AG-003, AG-004, AG-005 Buying Signal Classifier, AG-006 Need Discovery Agent, AG-032 Partner Due-Diligence Brief, AG-062 Signal Fusion "Why-Now" Brief Writer',
   au='AU-007, AU-014, AU-015 organization safe merge, AU-017 opportunity scoring, AU-019, AU-052 tender amendment/evidence refresh, AU-084 signal fusion and intent decay',
   brl='BRL-SRC-01…09, BRL-SCR-01…05, BRL-TEN-12 (no fundraising capability)', dclass='Public / Internal; organization records Confidential (Tier 2 ineligible once linked to a tenant opportunity)',
   tables='growth_search_plan→intel_search_plan; growth_organization→intel_organization; growth_signal→intel_signal; growth_signal_type→intel_signal_type; growth_need→intel_need; growth_need_evidence→intel_need_evidence; growth_opportunity→intel_opportunity; growth_referral→mkt_referral'),
 '03': dict(epic='06', bpwf='WF-03', actors='R04 Research Analyst, R10 Legal/DPO (eligibility rules), R03 Growth Manager, R19, R20',
   ag='AG-008 Decision-Maker Role Extractor, AG-060 Data-Quality and Dedupe Steward',
   au='AU-018 contact verification and freshness expiry, AU-015 safe merge, AU-074 data-quality rules and dedupe blocking, AU-100 identity resolution matcher, AU-009 PDP dispatch guard',
   brl='BRL-SRC-04/05, BRL-ELG-01…06, BRL-ELG-13/14, BRL-PRV-06', dclass='Confidential / personal (business contact data) — Tier 2 never',
   tables='growth_contact→intel_contact; growth_contact_source→intel_contact_source; growth_contact_verification→intel_contact_verification; growth_consent→gov_consent; growth_suppression→gov_suppression'),
 '04': dict(epic='06', bpwf='WF-02 (match → qualify) and WF-26 (route and SLA); WF-16 for WF04', actors='R04 Research Analyst, R03 Growth Manager, R03L Sales Lead (routing), R02 Startup Head (rubric approval), R19, R20',
   ag='AG-007 Solution Match Explainer, AG-009 Qualification Brief Assistant, AG-042 Predictive Score Explainer',
   au='AU-016 readiness-gated match ranking, AU-017 opportunity scoring (DEC-011), AU-080 lead-to-account matcher, AU-081 owner routing and speed-to-lead SLA, AU-056 propensity model (advisory), AU-057 drift monitor',
   brl='BRL-SCR-01…09, BRL-ELG-04 (score ≠ permission), BRL-ELG-15', dclass='Confidential — Tier 2 never',
   tables='growth_product→cat_offering; growth_opportunity→intel_opportunity; growth_score_version→intel_score_version; growth_need→intel_need'),
 '05': dict(epic='07', bpwf='WF-11 closure rules, WF-17 deal risk, WF-29 pipeline inspection; Customer 360 (M21–M23)', actors='R03 Growth Manager (owner), R03L Sales Lead, R02 Startup Head, R12 Tenant Administrator (imports), R19, R20',
   ag='AG-010 Import Mapping Assistant, AG-043 Next-Best-Action and Offer Advisor, AG-044 Deal-Risk Early-Warning Analyst, AG-060 Data-Quality and Dedupe Steward',
   au='AU-015, AU-021 Customer 360 projection, AU-100 identity resolution, AU-060 action catalogue eligibility filter, AU-058 deal-risk rule pack, AU-088 pipeline hygiene flags, AU-030 conflict resolution',
   brl='BRL-FIN-01 (closure evidence), BRL-AUT-09, BRL-TEN-01…04, NFR-025 stale revision', dclass='Confidential — Tier 2 never',
   tables='growth_deal→crm_deal; growth_stage→crm_stage; growth_activity→crm_activity; growth_task→lcy_task; growth_organization→intel_organization; growth_identity_link→eng_identity_link'),
 '06': dict(epic='08', bpwf='WF-06 (+ WF-27 cadence)', actors='R03 Growth Manager (author), R05 Marketing Specialist, R02 Startup Head (campaign/content approver), R10 Legal (claims), R19, R20',
   ag='AG-011 Outreach & Follow-up Message Drafter, AG-012 Claims & Policy Guard, AG-049 Personalization-at-Scale Variant Generator, AG-050 Indic Localization Agent',
   au='AU-009 PDP dispatch guard, AU-022 sequence scheduler with stop-on-reply, AU-024 bounce/complaint suppression, AU-008 STOP/opt-out handler, AU-031 compliance auto-pause, AU-002 budget reservation, AU-076 translation memory',
   brl='BRL-ELG-01…12, BRL-ELG-18, BRL-MKT-01/02, BRL-APR-02, BRL-AUT-01', dclass='Confidential / personal — Tier 2 never',
   tables='growth_message→eng_message; growth_message_draft→eng_message_draft; growth_message_template→eng_message_template; growth_outbox→ops_outbox; growth_delivery_event→eng_delivery_event; growth_channel_account→eng_channel_account; growth_suppression→gov_suppression'),
 '07': dict(epic='10', bpwf='WF-06 and WF-23 (WhatsApp concierge)', actors='R03 Growth Manager, R05 Marketing Specialist, R02 Startup Head (template/campaign approver), R16 customer (inbound), R19, R20',
   ag='AG-058 WhatsApp Concierge with Human Handoff, AG-011, AG-012, AG-013 Inbound Intent Classifier & Router',
   au='AU-073 WhatsApp service-window and handoff router, AU-009, AU-008, AU-024, AU-002',
   brl='BRL-ELG-07 (opt-in and 24 h window), BRL-ELG-02, BRL-ELG-13, BRL-AUT-08, BRL-MKT-01', dclass='Confidential / personal — Tier 2 never',
   tables='growth_thread→eng_thread; growth_channel_account→eng_channel_account; growth_message_template→eng_message_template; growth_consent→gov_consent; growth_inbound_event→eng_inbound_event'),
 '08': dict(epic='08', bpwf='WF-07 and WF-27 (multichannel cadence under consent)', actors='R03 Growth Manager, R03L Sales Lead, R11 Automation Lead (sequence config), R19, R20',
   ag='AG-063 Multichannel Cadence Composer, AG-011, AG-013',
   au='AU-022, AU-086 multichannel cadence orchestrator, AU-077 send-time window optimizer, AU-030 conflict resolution, AU-008, AU-025 emergency stop',
   brl='BRL-SEQ-01…05, BRL-ELG-08/09/10, BRL-AUT-09', dclass='Confidential — Tier 2 never',
   tables='growth_sequence→eng_sequence; growth_sequence_step→eng_sequence_step; growth_enrollment→eng_enrollment; growth_workflow_execution→aut_run'),
 '09': dict(epic='08', bpwf='WF-04 inbound and WF-06 reply classification; WF-23 handoff', actors='R03 Growth Manager (inbox owner), R16 customer, R10 Legal (sensitive claims), R19, R20',
   ag='AG-013 Inbound Intent Classifier & Router, AG-014 Reply Assistant, AG-017 Website Assistant, AG-021 Objection & Negotiation Assistant, AG-046 Objection-Handling Coach, AG-050 Indic Localization Agent',
   au='AU-073 handoff router, AU-030 conflict resolution, AU-100 identity resolution, AU-001 gateway (Tier 0 FAQ cache), AU-005 sanitizer',
   brl='BRL-AI-03/04/11, BRL-ELG-10, BRL-ELG-14, BRL-AUT-01 (L3 only for approved FAQ replies)', dclass='Confidential / personal — Tier 2 never',
   tables='growth_inbound_event→eng_inbound_event; growth_thread→eng_thread; growth_identity_link→eng_identity_link; growth_routing_rule→eng_routing_rule; growth_objection→com_objection'),
 '10': dict(epic='09', bpwf='WF-07 (meetings)', actors='R03 Growth Manager (host), R16 external participant, R02 Startup Head, R19, R20',
   ag='AG-059 Meeting-Prep Brief Agent, AG-037 Meeting Notes & Action Summarizer, AG-045 Conversation Intelligence Analyst',
   au='AU-023 slot offer and booking conflict check, AU-075 meeting-prep scheduler, AU-009, AU-027 notification digest',
   brl='BRL-MTG-01…06, BRL-ELG-08, FR-ENH-B-015 (notes-only meeting summaries)', dclass='Confidential / personal — Tier 2 never',
   tables='growth_meeting→eng_meeting; growth_calendar_link→eng_calendar_link; growth_task→lcy_task'),
 '11': dict(epic='11', bpwf='WF-05 (content and campaign)', actors='R05 Marketing Specialist (author), R02 Startup Head (publication approver), R10 Legal (claims/copyright), R19, R20',
   ag='AG-018 Content & Campaign Studio Drafter, AG-012 Claims & Policy Guard, AG-055 Knowledge Curator and RAG Freshness Agent, AG-050',
   au='AU-029 publication pipeline and expiry monitor, AU-069 RAG freshness and coverage monitor, AU-036 document assembly/hash/diff, AU-003 schema validation',
   brl='BRL-MKT-01…03, BRL-MKT-09, BRL-PUB-01, BRL-APR-01/02', dclass='Internal / Confidential (Tier 2 eligible only for approved public claims, opt-in)',
   tables='growth_claim→cat_claim; growth_content_asset→mkt_content_asset; growth_content_version→mkt_content_version; growth_approval→gov_approval'),
 '12': dict(epic='11', bpwf='WF-05 (social publishing)', actors='R05 Marketing Specialist, R02 Startup Head (publication approver), R10 Legal, R19, R20',
   ag='AG-018, AG-027 Market & Competitor Watch Summarizer, AG-012',
   au='AU-029 publication pipeline, AU-010 provider health/circuit breakers, AU-026 uncertain-outcome reconciliation, AU-007 source permission',
   brl='BRL-MKT-07 (no automated DMs; owned accounts only), BRL-PUB-01, BRL-SRC-01/04, BRL-AUT-08', dclass='Public (published) / Internal — Tier 2 eligible only for public-post classification, opt-in',
   tables='growth_social_post→intel_social_post; growth_social_publication→mkt_social_publication; growth_page_metric→mkt_page_metric'),
 '13': dict(epic='11', bpwf='WF-05 (SEO)', actors='R05 Marketing Specialist, R02 Startup Head (site change approver), R19, R20',
   ag='AG-018, AG-027',
   au='AU-033 SEO technical audit, AU-029, AU-014',
   brl='BRL-MKT-08 (authorized metrics only), BRL-PUB-01…06', dclass='Public / Internal — Tier 2 eligible (public page text only, opt-in)',
   tables='growth_keyword→mkt_keyword; growth_page_metric→mkt_page_metric; growth_seo_issue→mkt_seo_issue; growth_landing_page→mkt_landing_page'),
 '14': dict(epic='12', bpwf='WF-05 (paid ads) and WF-20 (experiments)', actors='R05 Marketing Specialist (author), R02 Startup Head (campaign/spend approver), R08/R09 Finance (budget line), R19, R20',
   ag='AG-051 Campaign Planner and Pacing Advisor, AG-052 Experiment Designer and Analyst, AG-053 Attribution and Marketing-Mix Analyst, AG-018',
   au='AU-032 ad spend cap and anomaly pause, AU-064 budget pacing, AU-065 experiment allocator/statistics, AU-098 experiment assignment and stop monitor, AU-097 campaign ROI, AU-002, AU-026',
   brl='BRL-MKT-04/05/06/10, BRL-AUT-01, BRL-APR-02/06, NFR-014', dclass='Confidential (spend, audiences) — Tier 2 never',
   tables='growth_audience→mkt_audience; growth_campaign→mkt_campaign; growth_campaign_version→mkt_campaign_version; growth_budget→ai_budget (budget line); growth_ad_campaign→mkt_ad_campaign; growth_ad_spend_event→mkt_spend_event; growth_attribution_event→mkt_attribution_event'),
 '15': dict(epic='12', bpwf='WF-04 (inbound acquisition) and §2.22.3 website publication', actors='R05 Marketing Specialist, R02 Startup Head, R10 Legal/DPO (consent text), R18 visitor, R19, R20',
   ag='AG-018, AG-017 Website Assistant, AG-012, AG-076 Accessibility Co-pilot',
   au='AU-020 lead dedupe, consent capture and form routing, AU-029, AU-080, AU-081',
   brl='BRL-PUB-01…06, BRL-PRV-06, BRL-ELG-13 (minors), BRL-ELG-14 (health data)', dclass='Personal (form submissions) — Tier 2 never; page copy Public',
   tables='growth_form→crm_form; growth_landing_page→mkt_landing_page; growth_lead→crm_lead; growth_consent→gov_consent; growth_attribution_event→mkt_attribution_event'),
 '16': dict(epic='09', bpwf='WF-04 (event/referral intake), WF-30 (partner referral)', actors='R05 Marketing Specialist, R03 Growth Manager, R16 partner/attendee, R02 Startup Head, R19, R20',
   ag='AG-013, AG-069 Partner Match and Co-sell Brief Assistant, AG-011',
   au='AU-051 event registration capacity, dedupe and reminders, AU-091 partner registration and channel-conflict checker, AU-020, AU-022',
   brl='BRL-ELG-17 (referral third parties), BRL-ELG-13, BRL-MTG-06, BRL-SEQ-02', dclass='Personal — Tier 2 never',
   tables='growth_business_event→mkt_event; growth_event_registration→mkt_registration; growth_event_attendance→mkt_attendance; growth_referral→mkt_referral'),
 '17': dict(epic='13', bpwf='WF-09 (proposal, quote, negotiation) and WF-28 (guarded quote)', actors='R03 Growth Manager (author), R02 Startup Head (discount approver per DEC-038), R08 Finance Maker / R09 Checker (tax), R16 customer (portal review), R19, R20',
   ag='AG-020 Proposal & Bid Response Drafter, AG-048 Price-Book Guidance Assistant, AG-066 CPQ Bundle Advisor and Guardrail Explainer',
   au='AU-035 quote calculator and approval routing, AU-089 CPQ guardrail evaluator, AU-036 document assembly/hash/diff',
   brl='BRL-QTE-01…07, BRL-APR-01…06, BRL-AUT-01 (≤ L1), DEC-027', dclass='Confidential — Tier 2 never; AI receives no price values (DEC-395)',
   tables='growth_proposal→com_proposal; growth_proposal_version→com_proposal_version; growth_quote→com_quote; growth_quote_line→com_quote_line'),
 '18': dict(epic='13', bpwf='WF-09 (negotiation) and WF-11 (commercial closure)', actors='R03 Growth Manager, R10 Legal (terms/deviation approver), R02 Startup Head (commercial approver), R16 counter-party signatory, R19, R20',
   ag='AG-021 Objection & Negotiation Assistant, AG-022 Contract Clause Reviewer, AG-046 Objection-Handling Coach',
   au='AU-036 document assembly, hashing and diff, AU-026 reconciliation',
   brl='BRL-CTR-01…05, BRL-APR-05, BRL-AUT-01, DEC-023 (e-sign adapter), DEC-054', dclass='Confidential / legal — Tier 2 never',
   tables='growth_negotiation→com_negotiation; growth_contract→com_contract; growth_objection→com_objection; growth_integration_deal→lcy_integration_deal'),
 '19': dict(epic='14', bpwf='WF-08 (project bid, AppNAI route) and WF-18 (RFP co-pilot)', actors='R06 Bid Manager, R02 Startup Head (bid/no-bid and submission approver), R10 Legal, R04 Research Analyst, R19, R20',
   ag='AG-019 Bid / RFP Analyzer, AG-020 Proposal & Bid Response Drafter, AG-047 RFP Response Co-pilot',
   au='AU-034 bid deadline and mandatory-checklist tracker, AU-052 tender amendment detector, AU-063 RFP answer library freshness, AU-007',
   brl='BRL-BID-01…06, DEC-053 (submission never automated), BRL-AUT-01', dclass='Confidential — Tier 2 never (public tender notice text Tier 2 eligible, opt-in)',
   tables='sales_bid→com_bid; growth_source→intel_source; growth_opportunity→intel_opportunity'),
 '20': dict(epic='14', bpwf='WF-10 (order and fulfilment, OrganicSpec route) and WF-11', actors='R07 Order Coordinator, R02 Startup Head (commitment approver), R08/R09 Finance, R16 customer, R19, R20',
   ag='AG-023 Order Document Extractor, AG-025 Onboarding Handoff Summarizer',
   au='AU-038 fulfilment ledger and over-delivery guard, AU-035, AU-026',
   brl='BRL-ORD-01…06, BRL-FIN-01, BRL-LCY-01', dclass='Confidential — Tier 2 never',
   tables='sales_order→com_order; sales_order_line→com_order_line; sales_fulfillment→com_fulfillment_event; growth_invoice→com_invoice; growth_payment→com_payment'),
}

# AGT (V12) -> blueprint agents
AGT = {
 'AGT-01': 'AG-027 (primary), AG-003, AG-004, AG-041', 'AGT-02': 'AG-003 (primary), AG-006, AG-062, AG-032',
 'AGT-03': 'AG-008 (primary), AG-060', 'AGT-04': 'AG-009 (primary), AG-007, AG-042; AG-013 and AG-069 for SM-SVC-16',
 'AGT-05': 'AG-043 (primary), AG-044, AG-010', 'AGT-06': 'AG-011 (primary), AG-012, AG-058 (WhatsApp), AG-049, AG-050',
 'AGT-07': 'AG-063 (primary), AG-011', 'AGT-08': 'AG-014 (primary), AG-013, AG-017, AG-021',
 'AGT-09': 'AG-059 (primary), AG-037, AG-045', 'AGT-10': 'AG-018 (primary), AG-012, AG-017 (SM-SVC-15)',
 'AGT-11': 'AG-018 (social/SEO drafting), AG-027 (listening, visibility)', 'AGT-12': 'AG-051 (primary), AG-052, AG-053',
 'AGT-13': 'AG-020 (SM-SVC-17), AG-048, AG-066; AG-023 (SM-SVC-20)', 'AGT-14': 'AG-021 (primary), AG-022, AG-046',
 'AGT-15': 'AG-019 (primary), AG-020, AG-047',
}

# executor -> blueprint component
EXEC = {
 'Evidence/ingestion engine': 'Research ingestion (M10–M12) via AU-007 source permission, AU-014 URL filter, AU-005 sanitizer; writes intel_source_record / intel_evidence',
 'Domain agent / task router': 'Model gateway AU-001 (Tier 0 → 1a → 1b; Tier 3 degrade), AU-003 schema validation, AU-006 eval gate; agent = AGT mapping below; output is a draft only (BRL-AI-07)',
 'Rules/analytics engine': 'Deterministic calculator in the domain module (zero model calls); Decimal arithmetic (DEC-027); BRL-AI-04 abstain on missing inputs',
 'Domain service': 'Domain module service: revision check (NFR-025), single transaction with audit and outbox (E-2)',
 'Policy/validation engine': 'Policy Decision Point AU-009 (plan-time and dispatch-time, E-3) with gov_policy_decision record; approval routing API-541',
 'Identity/reconciliation engine': 'AU-100 identity resolution / AU-015 safe merge / AU-030 conflict case / AU-026 uncertain-outcome reconciliation',
 'Effect adapter': 'Outbox relay + provider adapter (adapter port v2, Part 3.4 §3.4.5.2 A) with provider idempotency key; AU-009 recheck; AU-026 on timeout',
}
# failure code -> blueprint state (Part 2.3 §2.27.14 + this part's step states)
FAIL = {
 'SOURCE_DENIED': ('Held', 'Step Held with reason SOURCE_DENIED; transient read errors retried ≤ 3 with jitter (BRL-AUT-06, NFR-016)'),
 'REVIEW_REQUIRED': ('Waiting (AWAITING_APPROVAL)', 'Run Waiting on review/approval (gov_approval or intel_review); approval hash-bound (BRL-APR-02)'),
 'INVALID_METRIC': ('Held', 'Step Held with reason INVALID_METRIC; never impute missing values (BRL-AI-04)'),
 'INVALID_STATE': ('Held', 'Step Held with reason INVALID_STATE; stale revision → 409 (NFR-025)'),
 'POLICY_DENIED': ('Blocked', 'Step Blocked (new terminal step state, DEC-541); PDP Deny recorded; zero external effect'),
 'CONFLICT': ('Held / Reconciling', 'Held with aut_conflict_case (AU-030); uncertain provider outcome → Reconciling (AU-026)'),
 'EFFECT_UNKNOWN': ('Reconciling', 'Run Reconciling (DEC-050 uncertain); no retry before reconciliation (E-5); missing grant → Blocked'),
}
CLASS_TEST = {  # V12 step-test class -> test level/technique in blueprint test strategy
 'Evidence retrieval': 'IT (adapter stub) + SEC', 'AI inference': 'AIE (eval suite) + CT schema', 'Deterministic calculation': 'UT golden fixture',
 'Deterministic domain logic': 'UT golden fixture', 'Policy gate / human review': 'UT decision table + IT PDP', 'Deterministic identity / reconciliation': 'UT + IT replay',
 'External effect': 'IT sandbox adapter + CHAOS timeout',
}

# DTO field -> blueprint entity/column (logical)
FIELD = {
 'industry':'ref_value (industry taxonomy)', 'region':'ref_country / region code', 'source_ids':'intel_source.id[]', 'question':'intel_search_plan.objective',
 'signal_type':'intel_signal_type.code', 'observation':'intel_signal.summary', 'evidence_ids':'intel_evidence.id[]', 'observed_at':'intel_evidence.observed_at',
 'offering_id':'cat_offering.id', 'target_profile':'intel_search_plan.target_profile', 'organization_ref':'intel_organization.id', 'need':'intel_need.statement',
 'deadline':'intel_opportunity.deadline_utc', 'fit_score':'intel_score_version.score (Decimal)', 'role_criteria':'intel_role_hypothesis.criteria', 'contact_refs':'intel_contact.id[]',
 'purpose':'gov_consent.purpose', 'contact_ref':'intel_contact.id', 'role':'intel_role_hypothesis.role_code', 'verification_state':'intel_contact_verification.state',
 'eligibility_expiry':'gov_eligibility_decision.expires_at', 'lead_ref':'crm_lead.id', 'offering_refs':'cat_offering_version.id[]', 'scoring_policy_ref':'intel_scoring_model.id',
 'assignment_policy_ref':'eng_routing_rule.id', 'match_refs':'intel_match.id[]', 'score':'intel_score_version.score', 'reason_codes':'intel_score_version.reason_codes[]',
 'owner_ref':'ten_membership.id (owner)', 'review_state':'intel_review.state', 'account_ref':'intel_organization.id (account)', 'stage':'crm_stage.code',
 'interaction_refs':'crm_activity.id[]', 'relationship_ref':'crm_deal.id / relationship projection', 'next_task_ref':'lcy_task.id', 'version':'row revision (NFR-025)',
 'sender_ref':'eng_channel_account.id (verified sender)', 'claim_refs':'cat_claim.id[]', 'message_ref':'eng_message_template.id / eng_message.id', 'draft_ref':'eng_message_draft.id',
 'dispatch_ref':'ops_outbox.id / eng_message.id', 'delivery_state':'eng_delivery_event.state', 'suppression_state':'gov_suppression.state', 'provider_ref':'int_provider_event.provider_ref',
 'template_ref':'eng_message_template.id', 'consent_ref':'gov_consent.id', 'eligibility_state':'gov_eligibility_decision.outcome', 'thread_ref':'eng_thread.id',
 'sequence_ref':'eng_sequence.id', 'consent_refs':'gov_consent.id[]', 'event_refs':'ops_domain_event.id[]', 'next_action_ref':'eng_sequence_step.id / lcy_task.id',
 'scheduled_at':'eng_enrollment.next_due_at', 'stop_reason':'eng_enrollment.stop_reason', 'journey_state':'eng_enrollment.state', 'inbound_event_ref':'eng_inbound_event.id',
 'knowledge_refs':'cat_chunk.id[]', 'language':'ref_value (locale)', 'intent':'eng_intent.code', 'response_ref':'eng_message_draft.id', 'handover_ref':'eng_thread.assignee / handoff record',
 'confidence':'ai_model_run.confidence (Decimal)', 'participant_refs':'eng_meeting.participants[]', 'calendar_ref':'eng_calendar_link.id', 'availability':'free/busy window set',
 'agenda_ref':'eng_meeting.agenda_document_id', 'slot_ref':'eng_meeting.slot_hold_id', 'booking_ref':'eng_meeting.id', 'action_refs':'lcy_task.id[]',
 'brand_ref':'ten_business_line.brand_profile', 'brief_ref':'mkt_campaign.brief / mkt_content_asset.brief', 'asset_refs':'mkt_content_asset.id[]', 'content_ref':'mkt_content_asset.id',
 'revision':'mkt_content_version.revision / com_*_version.revision', 'claim_check_state':'mkt_content_version.claim_check_state', 'schedule':'mkt_social_publication.schedule (RFC 5545 RRULE + IANA tz)',
 'publication_ref':'mkt_social_publication.id', 'status':'mkt_social_publication.state', 'metric_refs':'mkt_page_metric.id[]', 'mention_refs':'intel_social_post.id[]',
 'domain_ref':'ten_domain.id', 'page_refs':'mkt_landing_page.id[]', 'keyword_refs':'mkt_keyword.id[]', 'visibility_report_ref':'ana_metric_snapshot.id (visibility report)',
 'issue_refs':'mkt_seo_issue.id[]', 'ad_account_ref':'eng_channel_account.id (ad account)', 'campaign_ref':'mkt_campaign.id / mkt_ad_campaign.id', 'objective':'mkt_campaign.objective',
 'budget_minor':'ai_budget line amount (Decimal ↔ minor units, DEC-543)', 'currency':'ref_currency.code', 'campaign_version':'mkt_campaign_version.revision', 'activation_state':'mkt_ad_campaign.state',
 'spend_minor':'mkt_spend_event.amount (Decimal ↔ minor units)', 'experiment_ref':'experiment record (WF-20, AU-065)', 'client_property_ref':'ten_domain.id (client-controlled property)',
 'form_schema_ref':'crm_form_version.id', 'submission_ref':'crm_submission.id', 'attribution_ref':'mkt_attribution_event.id', 'validation_state':'crm_submission.validation_state',
 'event_ref':'mkt_event.id', 'registration_ref':'mkt_registration.id', 'partner_ref':'lcy_partner.id', 'registration_state':'mkt_registration.state', 'attendance_state':'mkt_attendance.state',
 'referral_ref':'mkt_referral.id', 'journey_ref':'eng_enrollment.id / attribution journey', 'opportunity_ref':'intel_opportunity.id / crm_deal.id', 'price_revision_ref':'cat_price_version.id',
 'line_items':'com_quote_line[] (sku, unit, qty, price version)', 'quote_ref':'com_quote.id', 'total_minor':'com_quote.total (Decimal ↔ minor units)', 'tax_minor':'com_quote.tax_total (Decimal ↔ minor units)',
 'approval_state':'gov_approval.state', 'terms_ref':'cat_document.id (approved terms)', 'signatory_refs':'com_signature_event.signer[]', 'agreement_ref':'com_contract.id',
 'deviation_refs':'com_contract.deviation_flags[]', 'signature_state':'com_signature_event.state', 'obligation_refs':'contract obligation register (FR-V12-C, see SM-SVC-18-WF04)',
 'source_ref':'intel_source.id', 'tender_ref':'com_bid.tender_reference', 'capability_refs':'cat_capability.id[]', 'bid_ref':'com_bid.id', 'missing_evidence_refs':'com_bid_checklist_item.id[]',
 'submission_ref':'com_bid.submission_evidence (human submission, DEC-053)', 'order_lines':'com_order_line[]', 'inventory_ref':'com_sku_availability.id / com_inventory_reservation.id',
 'delivery_refs':'com_fulfillment_event.id[]', 'order_ref':'com_order.id', 'milestone_refs':'com_fulfillment_event.id[] (milestones)', 'fulfillment_state':'com_order.fulfilment_state',
 'exception_refs':'com_discrepancy_case.id[] / lcy_task.id[]',
}

# Per-workflow mapping: st, bp (blueprint coverage), gap, rules[], sla, kpis (formula text), flow
W = {}
def w(id, st, bp, gap, rules, sla, kpis, flow=False):
    W[id] = dict(st=st, bp=bp, gap=gap, rules=rules, sla=sla, kpis=kpis, flow=flow)

T = 'Run start ≤ 15 min (transactional) / ≤ 24 h (batch) per NFR-009, DEC-032'
w('SM-SVC-01-WF01','C','WF-02 steps 1–3 (source plan → evidence → signals), A015/A016/A085/A086, AU-007, AG-005','Typed DTO, step IDs, acceptance IDs and per-invocation cost not in blueprint',
  ['Only sources with an active intel_source_policy for the purpose are read (BRL-SRC-01/02)','Each signal carries ≥ 1 evidence_id with hash, rights and observed_at (BRL-SRC-03)','Freshness = now − observed_at compared with the source class freshness window; stale → flag, not delete (BRL-SRC-06)','Material claims in alerts require R02 approval before external reuse (BRL-SRC-10)'],
  'Batch: completes ≤ 24 h of schedule; alert to owner ≤ 15 min after signal accepted', 'source-linked signal rate = signals with ≥ 1 valid evidence_id ÷ signals emitted; signal freshness = median(now − observed_at) per source class; service KPI evidence-linked findings ≥ 95%, stale-source flags 100%')
w('SM-SVC-01-WF02','C','WF-02 (competitor watch A085/A086), AG-027','Regional analysis artefact and V12 contract not specified',
  ['Comparison only on approved public evidence; comparative claims need evidence pair (BRL-SRC-10)','A change is “verified” only when two dated observations differ and both cite evidence','Regional analysis states coverage gaps explicitly; no imputed market size'],
  T, 'competitor comparison completeness = attributes with evidence ÷ attributes in approved comparison template; verified change rate = changes confirmed by reviewer ÷ changes flagged')
w('SM-SVC-01-WF03','P','WF-02 evidence refresh; AG-027 summaries; AU-069 freshness (knowledge only)','Trend report artefact that separates facts from estimates is not specified',
  ['Report sections labelled Fact (cited) or Estimate (assumptions listed) (BRL-SCR-05 labelling)','Aggregation windows and denominators are versioned (metric_version)','Report is a draft until R02 approves; approved report hash stored'],
  'Batch ≤ 24 h; report draft available ≤ 2 h after run start [ASSUMPTION-796]', 'report claim evidence rate = cited factual statements ÷ factual statements; stale flag recall = stale sources flagged ÷ stale sources in fixture set')
w('SM-SVC-01-WF04','P','AG-041 signal fusion and AU-084 decay give change detection; no scenario brief','Scenario comparison with explicit assumptions, and alerting on material change, are new (V12 WF04)',
  ['Material change = signal delta above approved threshold per signal_type (threshold set in pilot, KPI baseline)','Scenarios are deterministic comparisons of approved assumption sets; AI drafts narrative only','Unverified evidence (POLICY_DENIED at verify) blocks the alert; owner notified via NT digest'],
  T, 'change alert precision = alerts confirmed material by reviewer ÷ alerts; scenario assumption coverage = scenarios with every assumption sourced or labelled ÷ scenarios', flow=True)
w('SM-SVC-02-WF01','C','WF-02 (need discovery → match), AG-006, AU-015, AU-017','Contract-level items only',
  ['Search only allowed sources within BRL-SRC-09 budget bounds','Entities normalized through AU-015 safe merge; ambiguous merges Held','fit_score is Decimal string; DEC-011 formula; score ≠ permission (BRL-ELG-04)','No investor or fundraising targets (BRL-TEN-12, DEC-002)'],
  T, 'qualified account precision = accounts accepted by R04 ÷ accounts proposed; duplicate rate = candidate accounts merged as duplicates ÷ candidates')
w('SM-SVC-02-WF02','P','WF-02 + WF-30 partner onboarding; AG-032 due-diligence brief','Supplier/distributor discovery for procurement purposes not explicit; procurement is SM-SVC-39 (group D)',
  ['Role classes: customer, supplier, distributor, partner (versioned enum); one organization may hold several roles','Conflicts = existing partner/channel conflict per AU-091 or same organization under another startup (portfolio isolation, BRL-TEN-06)','Supplier candidates never create payables or POs (procurement separate, SM-SVC-39)'],
  T, 'partner role accuracy = roles confirmed ÷ roles proposed; conflict recall = conflicts flagged ÷ conflicts in labelled fixture')
w('SM-SVC-02-WF03','C','AU-019 research alerts, AU-052 amendment detector, AU-034 deadline tracker','Contract-level items only',
  ['Deadline stored UTC with source timezone (BRL-BID-01 pattern); verified deadline required','Alert only to assigned owner; digest rules NT apply','Refresh respects source expiry (BRL-SRC-02)'],
  'Deadline alert ≤ 15 min after change detected; daily refresh', 'deadline accuracy = deadlines matching source of record ÷ deadlines stored; alert latency = p95(alert sent − change observed)')
w('SM-SVC-02-WF04','P','AU-084 signal fusion and intent decay; AG-062 why-now brief','Opportunity update with dedupe across continuous signals is partially specified',
  ['New signal deduplicated by (organization, signal_type, evidence hash) within the dedup window','Opportunity update is a revisioned write; owner reviews material changes','Decay per AU-084; alerts suppressed for closed or rejected opportunities (BRL-ELG-15)'],
  T, 'new signal precision = signals accepted ÷ new signals; duplicate alert rate = duplicate alerts ÷ alerts', flow=False)
w('SM-SVC-03-WF01','C','WF-03 step 1–2, AG-008, AU-018','Contract-level items only',
  ['Only permitted professional records; no private scraping and no guessed emails (BRL-SRC-04/05)','Role is a hypothesis with confidence until verified (intel_role_hypothesis)','Provenance (source, observed_at, rights) saved for every field'],
  T, 'role match precision = roles confirmed ÷ roles proposed; provenance rate = contact fields with provenance ÷ contact fields stored')
w('SM-SVC-03-WF02','C','WF-03 verification and dedupe; AU-018, AU-015, AU-074, AG-060','Contract-level items only',
  ['Format checks deterministic; deliverability check only where permitted','Merge proposal above match threshold; ambiguous → R04 review; no cross-startup merge','Verified ≠ consent (BRL-ELG-03)'],
  T, 'verified contact precision = verified contacts later confirmed valid ÷ verified contacts; merge error rate = merges reversed ÷ merges')
w('SM-SVC-03-WF03','C','WF-03 eligibility; PDP AU-009; gov_eligibility_decision','Contract-level items only',
  ['Eligibility per channel and purpose from consent, jurisdiction pack, suppression, minors and health exclusions (BRL-ELG-01…14)','eligibility_expiry set from the shortest-lived input','Expired consent → not eligible; fail closed'],
  'Synchronous decision p95 ≤ 500 ms (NFR-039)', 'eligibility accuracy = decisions matching decision-table oracle ÷ decisions; expired consent rejection = expired-consent cases rejected ÷ expired-consent cases (target 100%)')
w('SM-SVC-03-WF04','P','AU-018 freshness expiry; AG-060 steward','Active monitoring of organization and role changes with link invalidation not specified',
  ['Compare only permitted source updates; stale links invalidated (not deleted) with reason','Invalidated contact leaves active sequences at next dispatch recheck (BRL-ELG-18)','Verification task routed to R04 with SLA'],
  'Verification task SLA 2 business days [ASSUMPTION-796]', 'stale relationship recall = stale links detected ÷ stale links in fixture; verification turnaround = median(task closed − task created)')
w('SM-SVC-04-WF01','C','WF-02 match; AU-016, AG-007','Contract-level items only',
  ['Requirement classification drafts only; mandatory gaps listed explicitly','Match only to Launched offerings with readiness gate (BRL-SCR-04, BRL-MKT-02)','Gaps and evidence recorded; no inferred capability'],
  T, 'match precision = matches accepted ÷ matches proposed; mandatory gap recall = mandatory gaps found ÷ mandatory gaps in labelled set')
w('SM-SVC-04-WF02','C','AU-017 opportunity scoring (DEC-011), BRL-SCR-01…09','Contract-level items only',
  ['Score = DEC-011 formula; < 0.60 known weight → Unknown – review required (BRL-SCR-02)','Reason codes from registry ^[A-Z][A-Z0-9_]{2,63}$; freshness attached','Uncertain result flagged to review; score never grants permission (BRL-ELG-04)'],
  'Synchronous p95 ≤ 500 ms', 'score agreement = scores within ±5 of reviewer re-score ÷ scored leads [ASSUMPTION-797]; evidence freshness = scored leads whose evidence is within freshness window ÷ scored leads')
w('SM-SVC-04-WF03','C','WF-26 routing (AU-080, AU-081)','Contract-level items only',
  ['Ownership, capacity and territory validated before assignment; ineligible owners skipped','Duplicate leads merged before assignment (one owner per relationship)','Task creation idempotent per (lead, policy revision)'],
  'Assignment ≤ 5 min after qualification; speed-to-lead SLA per WF-26', 'assignment correctness = assignments matching policy oracle ÷ assignments; duplicate task rate = duplicate tasks ÷ tasks')
w('SM-SVC-04-WF04','P','WF-16 predictive model lifecycle, AU-056 (advisory), AG-042, AU-057 drift','Dynamic propensity scoring must stay advisory and never replace DEC-011 (DEC-383)',
  ['Model output is advisory only; DEC-011 score remains the decision of record (DEC-383)','Calibration on labelled outcomes per tenant scope; minimum sample before use (NFR-011)','Drift above threshold → route to R04 review and pause advisory display'],
  'Nightly batch ≤ 24 h', 'calibration error = expected calibration error (10 bins) on hold-out; drift detection recall = injected drift detected ÷ injected drift', flow=True)
w('SM-SVC-05-WF01','C','M21–M23 import (AG-010), AU-015, AU-021, AU-100','Contract-level items only',
  ['Import maps to scoped records only (tenant, startup from membership, BRL-TEN-01)','Identity resolution proposals above threshold auto-link; below → review','Interaction history linked with evidence; no cross-startup merge'],
  'Import of ≤ 10,000 rows completes ≤ 30 min [ASSUMPTION-796]', 'identity match accuracy = links confirmed ÷ links made; import rejection rate = rows rejected ÷ rows submitted')
w('SM-SVC-05-WF02','C','Stage transitions (crm_stage_transition), WF-11 closure evidence, BRL-FIN-01','Contract-level items only',
  ['Only permitted stage transitions per pipeline definition','Closure only with route-specific verified evidence (DEC-054)','Next task created idempotently per stage event'],
  'Synchronous p95 ≤ 500 ms', 'valid stage transition rate = accepted transitions ÷ attempted transitions; unsupported closure rejection = unsupported closures rejected ÷ unsupported closures attempted (target 100%)')
w('SM-SVC-05-WF03','C','AG-043 NBA, AU-060 action eligibility, AU-030 conflicts','Contract-level items only',
  ['Recommendations limited to the action catalogue after eligibility filter (AU-060)','Conflicting tasks resolved by priority compliance > transactional > sales > marketing (BRL-AUT-09)','Owner assignment reviewed when ambiguous'],
  T, 'next-action acceptance = recommendations accepted ÷ shown; conflict suppression rate = conflicting actions suppressed ÷ conflicts detected')
w('SM-SVC-05-WF04','C','WF-17 deal-risk early warning (AU-058, AG-044), AU-088','Contract-level items only',
  ['Stalled = no stage progress beyond stage SLA (configurable per pipeline)','Eligibility checked before any recommended outreach','Assign or hold; no automatic external action (R0)'],
  'Nightly ≤ 24 h', 'stalled deal recall = stalled deals flagged ÷ stalled deals; overdue task age = median age of overdue tasks')
w('SM-SVC-06-WF01','C','WF-06 draft (AG-011, AG-012), A034/A035','Contract-level items only',
  ['Facts retrieved only from approved, unexpired claims (BRL-MKT-01)','Localization via glossary/TM (AU-076); claims revalidated after translation','Draft staged for approval; author ≠ approver (BRL-APR-01)'],
  'Draft ≤ 60 s p95 (interactive)', 'claim accuracy = drafts with zero unsupported claims ÷ drafts; approved draft rate = drafts approved without edit ÷ drafts')
w('SM-SVC-06-WF02','C','WF-06 dispatch with PDP recheck, outbox, AU-024','V12 R2 L3-mandate path vs DEC-064 (CONFLICT-799)',
  ['Plan-time and dispatch-time recheck of consent, scope, caps and budget (E-3, BRL-ELG-18)','Idempotent send key = tenant/company/run/version/step/target digest','Timeout after submission → Reconciling; never resend before reconcile (E-5)','First-touch sends need approved template hash (L1); L3 only for DEC-064 L3 categories'],
  'Dispatch ≤ 15 min of approval (transactional)', 'duplicate send rate = duplicate provider sends ÷ sends (target 0); accepted delivery reconciliation = sends with reconciled provider status ÷ sends', flow=True)
w('SM-SVC-06-WF03','C','WF-06 callbacks; AU-024 bounce suppression; AU-008 STOP; BRL-AUT-08','Contract-level items only',
  ['Mailbox events verified (signature or authorized mailbox) and deduplicated','Hard bounce/complaint → suppression immediately (BRL-ELG-11/12)','Reply pauses generic follow-up (BRL-ELG-10)'],
  'Stop propagation ≤ 60 s (E-7)', 'bounce classification accuracy = bounces classified correctly ÷ bounces; stop propagation latency = p95(follow-up paused − event received)')
w('SM-SVC-06-WF04','P','AU-031 complaint auto-pause, AU-024; Part 2.2 deliverability check','Sender authentication (SPF/DKIM/DMARC) validation and remediation proposals not specified',
  ['Sender settings validated (SPF, DKIM, DMARC alignment) before sender is eligible','Complaint or bounce rate above threshold pauses the sender (deterministic, L3 safety control)','Remediation is a proposal for R11 review; no automatic DNS change'],
  'Risky sender paused ≤ 15 min after threshold breach', 'complaint rate = complaints ÷ delivered per sender per 7 days; risky sender pause latency = p95(pause − threshold breach)')
w('SM-SVC-07-WF01','C','WF-06/WF-23 eligibility; BRL-ELG-07; template approval','Contract-level items only',
  ['Opt-in record specific to WhatsApp and purpose; template approved by provider and R02','Service window and template category rules applied (verify provider rules at implementation, as of 27 Nov 2026)','Failures held with reason; no send'],
  'Synchronous p95 ≤ 500 ms', 'template eligibility accuracy = decisions matching oracle ÷ decisions; opt-out rejection = opted-out contacts rejected ÷ opted-out contacts (target 100%)')
w('SM-SVC-07-WF02','C','WF-06 WhatsApp dispatch; AU-073; AU-009','V12 R2 L3 mandate vs DEC-064 (CONFLICT-799)',
  ['Rendered template content and budget validated; approval hash bound','Idempotent send; uncertain outcome reconciled','Outside service window only approved templates'],
  'Dispatch ≤ 15 min of approval', 'authorized dispatch rate = dispatches with valid approval and eligibility ÷ dispatches (target 100%); duplicate send rate (target 0)')
w('SM-SVC-07-WF03','C','WF-23 inbound; BRL-AUT-08 signature and dedupe; AU-008','Contract-level items only',
  ['Signature and event ID verified; replay has one effect (E-4)','Inbound linked to the shared thread (eng_thread) with identity link','STOP keywords update suppression ≤ 60 s'],
  'Webhook ack ≤ 2 s; processing ≤ 60 s', 'webhook dedup rate = duplicate events ignored ÷ duplicate events; reply sync latency = p95(thread updated − provider event time)')
w('SM-SVC-07-WF04','P','WF-23 concierge (AG-058) + WF-10 orders','Interactive commerce offers inside chat (catalogue offers, order hand-off) are new; prices never set by AI',
  ['Buying intent classified; offer prepared only from approved offering and price version','Messaging window checked before any reply; outside window → approved template or human','Transaction routed to WF-10 order flow / human; AI never confirms price or order (BRL-AI-07)'],
  'First response ≤ 60 s inside window (L3 FAQ) or human handoff ≤ 15 min business hours', 'intent accuracy = intents confirmed ÷ classified; commerce handoff completeness = handoffs with offer, contact and thread context ÷ handoffs', flow=True)
w('SM-SVC-08-WF01','C','WF-07/WF-27 sequence scheduling; AU-022, AU-086, AU-077','Contract-level items only',
  ['Due step created only for eligible enrolment (BRL-SEQ-01)','Quiet hours and frequency caps applied in recipient timezone (BRL-ELG-08/09)','Next action reserved with budget reservation'],
  'Due steps start ≤ 15 min after due time (NFR-009)', 'quiet-hour violation rate = sends inside quiet hours ÷ sends (target 0); due-time accuracy = steps started within 15 min of due ÷ steps')
w('SM-SVC-08-WF02','C','AG-063 cadence composer; AU-060; AU-030','Contract-level items only',
  ['Response classified (intent taxonomy FR-ENH-B-014)','Only eligible actions from catalogue; draft or hold','Conflicts prevented across workflows (BRL-AUT-09)'],
  T, 'eligible action rate = proposed actions passing PDP ÷ proposed actions; conflict prevention = conflicting actions prevented ÷ conflicts detected')
w('SM-SVC-08-WF03','C','§2.22.1 opt-out flow; AU-008; AU-025','Contract-level items only',
  ['Event deduplicated; suppression applied before any pending send','All runs for the relationship paused within 60 s (E-7)','Owner notified with reason'],
  'Stop ≤ 60 s', 'stop propagation latency = p95(all queued sends cancelled − stop event); suppressed-send count = sends after suppression (target 0)')
w('SM-SVC-08-WF04','P','AU-086 orchestrator; AU-077; WF-27','Real-time cross-channel rescheduling with one frequency budget partly specified',
  ['One frequency budget across channels per relationship (WF-27)','Duplicate actions across channels removed before dispatch','Stop rules applied before reschedule'],
  'Re-plan ≤ 5 min after triggering event', 'cross-channel duplicate rate = duplicate touches across channels ÷ touches; reschedule accuracy = rescheduled steps within allowed window ÷ rescheduled steps')
w('SM-SVC-09-WF01','C','WF-04 inbound capture; AG-013; AU-100','Contract-level items only',
  ['Scope and signature verified; event deduplicated','Identity linked via AU-100; ambiguous → review','Intent and priority classified; untrusted content sanitized (AU-005)'],
  'Capture ≤ 60 s', 'identity link accuracy = links confirmed ÷ links; event dedup rate = duplicates suppressed ÷ duplicates')
w('SM-SVC-09-WF02','C','AG-014 reply assistant; Tier 0 FAQ (AU-001); BRL-AI-03 grounding','V12 R2 L3 mandate vs DEC-064 (approved FAQ only)',
  ['Answer only from approved FAQ/knowledge with citations; abstain otherwise (BRL-AI-03/04)','Claims validated (AG-012); sensitive topics → human','L3 permitted only for approved-FAQ replies (DEC-064); all else L1'],
  'L3 FAQ reply ≤ 60 s; human review queue ≤ 4 business hours', 'grounded answer rate = answers fully cited ÷ answers; escalation recall = escalations made ÷ cases that required escalation', flow=True)
w('SM-SVC-09-WF03','C','WF-23 handoff; AU-073','Contract-level items only',
  ['Automation paused on handover; resumes only under policy recheck','Agent assignment per routing rule','Resolution tracked; unauthorized resume blocked'],
  'Handover SLA 15 min business hours [ASSUMPTION-796]', 'handover SLA = handovers acknowledged within SLA ÷ handovers; unauthorized resume count (target 0)')
w('SM-SVC-09-WF04','P','AG-050 Indic localization; WF-23','Audio/image enquiry extraction is not in the blueprint; multimodal data class rules needed',
  ['Audio/image only from authorized channels; consent for recording where required (verify)','Extraction via gateway Tier 1b; no Tier 2 for any personal media','Uncertain language or intent → human; grounded response only'],
  'Text ≤ 60 s; media ≤ 5 min', 'multilingual intent accuracy = correct intents ÷ enquiries per language; grounding coverage = responses with citations ÷ responses', flow=True)
w('SM-SVC-10-WF01','C','WF-07 booking; AU-023; BRL-MTG-01…04','V12 R2 L3 mandate vs DEC-064 (bookings are eligible follow-ups ⇒ L3 allowed within caps)',
  ['Only verified free slots (BRL-MTG-01); hold 15 min (BRL-MTG-02)','Confirmation creates one invitation (idempotent); conflict → re-offer','Timeout on calendar provider → Reconciling'],
  'Slot offer ≤ 5 s; invitation ≤ 60 s', 'booking conflict rate = double-booked confirmations ÷ confirmations (target 0); confirmation evidence = bookings with provider event ID ÷ bookings')
w('SM-SVC-10-WF02','C','AU-075 meeting-prep scheduler; AG-059; BRL-MTG-06','Contract-level items only',
  ['Brief summarizes approved CRM facts only','Reminders 24 h and 1 h on eligible channels; stop on cancellation (BRL-MTG-06)','Agenda requires owner review'],
  'Brief ready ≥ 24 h before meeting', 'agenda requirement coverage = agenda items mapped to stated needs ÷ needs; reminder timing = reminders sent within ±5 min of schedule ÷ reminders')
w('SM-SVC-10-WF03','C','AG-037 notes summarizer; FR-ENH-B-015 notes-only','Contract-level items only',
  ['Only approved notes or transcripts with recording consent','Material items reviewed by owner before tasks','Tasks created idempotently'],
  'Actions ≤ 30 min after notes approved', 'owner extraction accuracy = actions with correct owner ÷ actions; action review rate = material actions reviewed ÷ material actions')
w('SM-SVC-10-WF04','P','AG-059 prep brief; AG-045 conversation intelligence','Demo plan tailored to requirements and gap identification is new',
  ['Demo agenda uses approved product details only (BRL-MKT-02)','Gaps vs prospect requirements listed, never hidden','Actions extracted only from authorized notes'],
  'Demo plan ≥ 24 h before demo', 'demo requirement coverage = requirements addressed in plan ÷ requirements; action extraction accuracy = correct actions ÷ extracted', flow=False)
w('SM-SVC-11-WF01','C','WF-05 content plan; AG-018','Contract-level items only',
  ['Themes suggested from approved offerings and claims only','Missing evidence flagged before calendar approval','Calendar approved by R02'],
  T, 'calendar coverage = planned slots filled ÷ slots; unsupported theme rate = themes without approved claim ÷ themes')
w('SM-SVC-11-WF02','C','WF-05 drafting; AG-018; AG-012','Contract-level items only',
  ['Evidence retrieved from approved claims and knowledge','Variants generated; unsupported claims blocked (BRL-MKT-01)','Copyrighted material reviewed'],
  'Draft ≤ 2 min p95', 'claim accuracy = drafts with zero unsupported claims ÷ drafts; draft acceptance = drafts approved ÷ drafts')
w('SM-SVC-11-WF03','C','WF-05 review; AU-036 diff','Contract-level items only',
  ['Revision diff computed against last approved hash','Claims and style reviewed; changes create new revision (BRL-QTE-06 pattern)','Approval routed to R02'],
  T, 'revision traceability = revisions with diff and approver ÷ revisions; material claim error rate = published items with claim error ÷ published')
w('SM-SVC-11-WF04','P','AU-069 RAG freshness (knowledge base only); AU-029 expiry monitor','Content-inventory gap and freshness backlog is new',
  ['Coverage gaps computed against approved topic map','Claims re-verified; expired claim → content flagged for withdrawal','Backlog prioritized by traffic × staleness (deterministic)'],
  'Weekly batch', 'stale content recall = stale items flagged ÷ stale items; backlog precision = backlog items accepted ÷ backlog items')
w('SM-SVC-12-WF01','C','WF-05 social scheduling; AU-029; BRL-MKT-07','V12 R2 L3 mandate vs DEC-064 (publishing L1 approval then L2 dispatch)',
  ['Channel capability, asset format and schedule validated','Publication key reserved (idempotent)','Only approved posts queued; owned accounts only'],
  'Publish within ±5 min of schedule', 'schedule accuracy = posts published within ±5 min ÷ posts; duplicate publication count (target 0)')
w('SM-SVC-12-WF02','C','AU-029; AU-026 reconciliation; BRL-AUT-08','Contract-level items only',
  ['Callbacks verified; polling fallback where no webhook','Status reconciled; uncertain → Reconciling','Aggregate metrics only (no personal data)'],
  'Status reconciled ≤ 15 min', 'publication reconciliation = publications with confirmed status ÷ publications; metric completeness = metrics collected ÷ expected')
w('SM-SVC-12-WF03','P','AG-027 watch summaries; intel_social_post; BRL-SRC-01','Permitted social listening topics, collection and escalation partly specified',
  ['Collect only via authorized listening APIs or owned-account data (BRL-SRC-04)','Themes and intent classified; no individual profiling','Relevant mentions escalated to owner'],
  'Daily batch', 'mention relevance precision = relevant mentions ÷ mentions surfaced; source compliance = mentions from permitted sources ÷ mentions (target 100%)')
w('SM-SVC-12-WF04','N','—','Community response queue and social trend coordination are not in the blueprint',
  ['Responses drafted from approved response playbook only; L1 approval each (no automated DMs, BRL-MKT-07)','Duplicates collapsed before drafting','Sensitive issues (complaints, legal, health) escalated to human'],
  'Response draft ≤ 30 min business hours', 'trend precision = trends confirmed ÷ trends flagged; approved-response queue accuracy = queued responses approved without edit ÷ queued', flow=True)
w('SM-SVC-13-WF01','C','WF-05 SEO; mkt_keyword; mkt_page_metric; BRL-MKT-08','Contract-level items only',
  ['Metrics only from authorized sources (Search Console or analytics)','Opportunities ranked deterministically; AI labels relevance','Evidence saved with observed_at'],
  'Weekly batch', 'metric completeness = metrics present ÷ expected; keyword relevance = relevant keywords ÷ classified keywords')
w('SM-SVC-13-WF02','C','AU-033 SEO technical audit; mkt_seo_issue','Contract-level items only',
  ['Crawl within permitted budget and robots rules','Issues prioritized by severity × traffic','Affected pages listed'],
  'Audit ≤ 2 h for ≤ 500 pages [ASSUMPTION-796]', 'issue detection precision = confirmed issues ÷ issues; affected-page recall = affected pages found ÷ affected pages')
w('SM-SVC-13-WF03','C','WF-05 SEO tasks; site approval (BRL-PUB-01)','Contract-level items only',
  ['Change drafts never published without site approval','Post-change comparison uses same metric version and window','Limitations recorded'],
  T, 'validated change coverage = changes with post-change comparison ÷ changes; post-change comparison quality = comparisons with matching window and metric version ÷ comparisons')
w('SM-SVC-13-WF04','N','—','AI search / answer-engine visibility monitoring is not in the blueprint (only AU-033 and doc 21 AI search in replacement register)',
  ['Query samples approved and versioned; observations from permitted interfaces only (verify provider terms, as of 27 Nov 2026)','Indexability and structured-data evidence checked','Recommendations are drafts; no deceptive optimization'],
  'Weekly batch', 'query observation coverage = sampled queries observed ÷ sampled queries; citation accuracy = observed citations correctly attributed ÷ citations', flow=True)
w('SM-SVC-14-WF01','C','WF-05 campaign draft; AG-051; BRL-MKT-04/06','Contract-level items only',
  ['Audience eligible; no minors, health or sensitive targeting (BRL-MKT-06, DEC-030)','Claims validated','Approval routed with budget line'],
  T, 'targeting compliance = drafts passing targeting rules ÷ drafts; draft readiness = drafts approved first pass ÷ drafts')
w('SM-SVC-14-WF02','C','WF-05 activation (AU-032 caps, AU-009 recheck, AU-026)','R3 + V12 L3-mandate path vs DEC-064/safety invariant (CONFLICT-798)',
  ['Grant and budget rechecked at dispatch (E-3, NFR-014)','Spend reserved before activation; cap enforced by provider and platform','Approval digest must equal activation payload digest','Provider timeout → Reconciling; never re-launch blindly'],
  'Activation ≤ 15 min of approval; pause ≤ 60 s', 'unauthorized spend count (target 0); reconciliation rate = activations with reconciled provider state ÷ activations', flow=True)
w('SM-SVC-14-WF03','C','AU-064 pacing; AU-097 ROI; AG-051','Contract-level items only',
  ['Attribution normalized per AU-096 model in use','Overspend alerts at 80/100%; anomaly > 150% pauses (BRL-MKT-05)','Changes drafted for approval only'],
  'Daily', 'spend variance = |actual − planned| ÷ planned; recommendation accuracy = recommendations accepted and improving KPI ÷ accepted')
w('SM-SVC-14-WF04','P','WF-20 experiment lifecycle; AU-065; AU-098; AG-052','Incrementality measurement with spend cap per variant partially specified',
  ['Variants assigned per pre-registered design','Spend cap per variant enforced (R3 spend control)','Incrementality via holdout; inconclusive flagged (no claim)'],
  'Daily monitoring; readout at pre-registered end', 'incrementality confidence = posterior/CI coverage of lift per pre-registration; cap violation count (target 0)', flow=False)
w('SM-SVC-15-WF01','C','WF-04/§2.22.3 landing pages; A107/A108; BRL-PUB','Contract-level items only',
  ['Page and form drafted from approved claims; consent text approved by R10','Preview only on separate client property with expiring grant (BRL-PUB-03)','Age band first for EduVerse (DEC-030)'],
  T, 'form schema coverage = required fields present ÷ required fields; privacy preview pass = previews passing privacy checks ÷ previews')
w('SM-SVC-15-WF02','C','AU-020 lead dedupe, consent and routing; W12–W17','Contract-level items only',
  ['Schema and scope validated; free text scanned (BRL-PRV-06)','Deduplicated; consent and attribution captured','Lead routed (AU-081)'],
  'Lead created ≤ 60 s of submission', 'valid lead capture rate = valid submissions converted to leads ÷ valid submissions; duplicate lead count (target 0)')
w('SM-SVC-15-WF03','P','KPI funnel (RP-), AU-020','Intake health (failures, retries, denominators) not specified',
  ['Failures and missing fields detected from submission logs','Retries reconciled so one submission counts once','Conversion = leads ÷ unique form views (same window)'],
  'Hourly', 'failure detection recall = failures detected ÷ injected failures; conversion denominator accuracy = conversions using deduped denominator ÷ conversions')
w('SM-SVC-15-WF04','N','—','Machine-readable offering (structured data) and intake readiness validation not in the blueprint',
  ['Structured offering schema validated against approved offering and price visibility rules','Access and privacy checked: no personal data in public payloads','Test intake with synthetic submission in simulation'],
  'On change', 'schema validation pass = pages passing validation ÷ pages; data leak count (target 0)', flow=False)
w('SM-SVC-16-WF01','C','AU-051 event registration; A062/A063','Contract-level items only',
  ['Form and schedule approved','Consent validated; minors path per DEC-030','Registration deduplicated'],
  'Registration confirmed ≤ 60 s', 'registration accuracy = registrations with valid data ÷ registrations; duplicate signup count (target 0)')
w('SM-SVC-16-WF02','C','AU-051 reminders; BRL-MTG-06; AU-022','Contract-level items only',
  ['Reminders only to eligible registrants','Attendance reconciled from provider evidence','Follow-up assigned by interest'],
  'Reminders 24 h and 1 h before', 'eligible reminder rate = reminders to eligible ÷ reminders; attendance match rate = attendance matched to registration ÷ attendance')
w('SM-SVC-16-WF03','C','WF-30 partner referral; AU-091; BRL-ELG-17','Contract-level items only',
  ['Referral source and permission validated (third-party consent, BRL-ELG-17)','Relationship deduplicated; channel conflict checked','Qualified and assigned'],
  T, 'referral attribution accuracy = referrals attributed correctly ÷ referrals; duplicate opportunity count (target 0)')
w('SM-SVC-16-WF04','P','AU-096 attribution; WF-20','Event conversion journey report partly specified',
  ['Segments use eligible attendees only','Journey progression measured with fixed window','Opt-outs suppressed before any follow-up'],
  'Weekly', 'event funnel coverage = funnel stages measured ÷ stages; opt-out compliance = follow-ups to opted-out (target 0)')
w('SM-SVC-17-WF01','C','WF-09 proposal draft; AG-020','Contract-level items only',
  ['Deliverables matched to approved catalogue','Scope, assumptions and exclusions explicit','Review routed'],
  T, 'scope coverage = requirements covered ÷ requirements; unsupported deliverable count (target 0)')
w('SM-SVC-17-WF02','C','AU-035 quote calculator; BRL-QTE-01…07; DEC-027','R3; V12 int64 minor-unit DTO vs Decimal (DEC-543); L3 mandate (CONFLICT-798)',
  ['Price revision validated (approved snapshot)','Line total = ROUND_HALF_UP(qty × price × (1 − d), 2); totals Σ rounded lines + tax (BRL-QTE-02)','Unapproved discount held for approver per DEC-038'],
  'Synchronous p95 ≤ 500 ms', 'calculation accuracy = quotes matching golden calculator ÷ quotes (target 100%); discount violation count (target 0)', flow=True)
w('SM-SVC-17-WF03','C','WF-09 approval; BRL-QTE-06; BRL-APR-02','R3 L3 mandate (CONFLICT-798)',
  ['Version compared; calculations revalidated','Approved revision frozen (hash)','Validity tracked; expired quote cannot be accepted (BRL-QTE-05)'],
  T, 'version integrity = approved quotes whose hash matches sent ÷ approved; approval traceability = quotes with complete approval chain ÷ quotes')
w('SM-SVC-17-WF04','P','WF-28 guarded quote; AU-089 CPQ; AG-066','Configurable bundle quotation with versioned configuration partly specified',
  ['Configuration validated against approved bundle rules','Totals deterministic; permitted discounts only','Exceptions routed to approver'],
  T, 'configuration coverage = configurations supported ÷ requested; deterministic total accuracy (target 100%)')
w('SM-SVC-18-WF01','C','WF-09 objections; AG-021; AG-046','Contract-level items only',
  ['Issue classified; playbook approved','Suggestions within approved limits only','Exceptions escalated'],
  T, 'playbook alignment = suggestions within playbook ÷ suggestions; exception escalation recall = exceptions escalated ÷ exceptions')
w('SM-SVC-18-WF02','C','WF-09/WF-11 contract draft; BRL-CTR-01; AG-022','Contract-level items only',
  ['Draft only from approved templates','Deviations flagged for Legal','Approved version frozen with SHA-256 hash (BRL-CTR-02)'],
  T, 'clause coverage = required clauses present ÷ required; legal deviation recall = deviations flagged ÷ deviations')
w('SM-SVC-18-WF03','C','WF-11; DEC-023 e-sign adapter; BRL-CTR-03/04','R3; AI never signs; L3 mandate path (CONFLICT-798)',
  ['Signatory authority validated for both parties (BRL-CTR-03)','Signature task initiated only after legal approval of exact hash (BRL-CTR-04)','Signed hash must equal approved hash (BRL-CTR-02)'],
  'Signature request ≤ 15 min of approval', 'signatory authorization pass = requests with verified authority ÷ requests (target 100%); receipt reconciliation = signature events reconciled ÷ events', flow=True)
w('SM-SVC-18-WF04','N','—','Obligation register and negotiation scenario analysis are not in the blueprint',
  ['Obligations extracted from authorized drafts with clause citation','Scenarios compared inside approved negotiation bounds','Deviations flagged; review by R10'],
  T, 'obligation extraction precision = obligations confirmed ÷ extracted; deviation recall = deviations flagged ÷ deviations', flow=False)
w('SM-SVC-19-WF01','C','WF-08 discovery; AU-034; AU-052','Contract-level items only',
  ['Only allowed tender sources','Requirements and deadlines extracted with evidence','Deduplicated; bid candidates created'],
  'Daily', 'deadline accuracy = deadlines matching notice ÷ deadlines; duplicate tender count (target 0)')
w('SM-SVC-19-WF02','C','WF-08 bid/no-bid; BRL-BID-02/03','Contract-level items only',
  ['Mandatory criteria checked','Gaps and cost flagged','Recommendation for R02 decision'],
  T, 'mandatory criteria recall = criteria evaluated ÷ criteria; cost assumption coverage = cost lines with assumptions ÷ cost lines')
w('SM-SVC-19-WF03','C','WF-08 package + human submission (DEC-053); WF-18','R3; V12 “coordinate authorized submission” and L3 mandate vs DEC-053 (CONFLICT-800)',
  ['Response drafted; attachments validated','Submission approval by R02','Human submits outside the system; evidence recorded (BRL-BID-04)','Submission blocked at deadline − buffer (BRL-BID-01)'],
  'Package ready ≥ buffer before deadline', 'attachment completeness = required attachments present ÷ required; verified receipt rate = submissions with verified receipt ÷ submissions', flow=True)
w('SM-SVC-19-WF04','P','AU-034 checklist; AU-063','Continuous compliance matrix partly specified',
  ['Each requirement mapped to evidence','Completeness validated','Missing items flagged; submission approval still required'],
  'Daily until deadline', 'requirement evidence coverage = requirements with evidence ÷ requirements; missing-item recall = missing items flagged ÷ missing items')
w('SM-SVC-20-WF01','C','WF-10 order draft; BRL-ORD-01; AU-038','Contract-level items only',
  ['Approved quote, price, tax and quantity validated','Inventory and selling capability checked','Draft for approval; procurement separate'],
  T, 'quote consistency = orders matching approved quote ÷ orders (target 100%); inventory check coverage = lines checked ÷ lines')
w('SM-SVC-20-WF02','C','WF-10 fulfilment; BRL-ORD-02…04','R3 L3 mandate (CONFLICT-798)',
  ['Milestones created; owner assigned','Status transitions validated','Delays flagged'],
  T, 'milestone assignment completeness = milestones with owner ÷ milestones; delay detection = delays flagged ÷ delays')
w('SM-SVC-20-WF03','C','WF-10 acceptance; BRL-ORD-05; AU-038','R3 L3 mandate (CONFLICT-798)',
  ['Milestone matched to acceptance evidence','Inconsistent state held','Reviewer routed; handoff updated'],
  T, 'acceptance evidence match = acceptances with evidence ÷ acceptances; invalid transition rejection (target 100%)', flow=False)
w('SM-SVC-20-WF04','N','—','Fulfilment delay prediction and exception monitoring are not in the blueprint',
  ['Delay risk estimated from promised dates, capacity and history (deterministic baseline first)','Actual vs milestone compared','Owner alerted; exceptions escalated'],
  'Daily', 'delay forecast error = MAE(predicted − actual delay days); exception recall = exceptions flagged ÷ exceptions', flow=True)
