-- V0010__triggers
SET search_path = ge, extensions, public;

SELECT set_config('app.zone', coalesce(nullif(current_setting('app.deployment_region', true), ''), 'IN'), false);

SELECT set_config('app.deployment_region', coalesce(nullif(current_setting('app.deployment_region', true), ''), 'IN'), false);

CREATE OR REPLACE FUNCTION ge.fn_touch_revision() RETURNS trigger LANGUAGE plpgsql AS $$
BEGIN
  IF NEW.revision IS DISTINCT FROM OLD.revision + 1 THEN
    RAISE EXCEPTION 'STALE_REVISION: expected revision %', OLD.revision + 1 USING ERRCODE = '40001'; END IF;
  NEW.updated_at := now();
  IF NEW.created_at IS DISTINCT FROM OLD.created_at OR NEW.id IS DISTINCT FROM OLD.id THEN
    RAISE EXCEPTION 'IMMUTABLE_RECORD: identity columns are frozen' USING ERRCODE = 'P0001'; END IF;
  RETURN NEW;
END $$;

CREATE OR REPLACE FUNCTION ge.fn_freeze_versioned() RETURNS trigger LANGUAGE plpgsql AS $$
DECLARE o jsonb := to_jsonb(OLD); n jsonb := to_jsonb(NEW);
BEGIN
  IF (o->>'status') IN ('approved','published','active','superseded') THEN
    IF (n - ARRAY['status','superseded_by_id','effective_to','revision','updated_at','updated_by']) IS DISTINCT FROM
       (o - ARRAY['status','superseded_by_id','effective_to','revision','updated_at','updated_by'])
       OR (n->>'status') NOT IN ('superseded','expired','retired', o->>'status') THEN
      RAISE EXCEPTION 'IMMUTABLE_RECORD: % version is frozen', o->>'status' USING ERRCODE = 'P0001'; END IF;
  END IF;
  RETURN NEW;
END $$;

CREATE OR REPLACE FUNCTION ge.fn_row_region_guard() RETURNS trigger LANGUAGE plpgsql AS $$
DECLARE r text := ge.app_zone(); v text := coalesce(to_jsonb(NEW)->>'region', to_jsonb(NEW)->>'zone', to_jsonb(NEW)->>'data_region');
BEGIN
  IF v IS NOT NULL AND v NOT IN ('GLOBAL') AND v <> r THEN
    RAISE EXCEPTION 'RESIDENCY_VIOLATION: row for zone % written to % database (DEC-772, CJ-TC-09)', v, r USING ERRCODE = '23514'; END IF;
  RETURN NEW;
END $$;

CREATE OR REPLACE FUNCTION ge.fn_validate_typed_domain_row() RETURNS trigger LANGUAGE plpgsql AS $$
DECLARE r ge.domain_schema_registry%ROWTYPE; st text := coalesce(to_jsonb(NEW)->>'status', to_jsonb(NEW)->>'state');
BEGIN
  IF NEW.schema_ref IS NULL THEN
    IF NEW.payload IS DISTINCT FROM '{}'::jsonb THEN RAISE EXCEPTION 'SCHEMA_REF_REQUIRED: payload needs schema_ref (DEC-661)' USING ERRCODE = '23514'; END IF;
    RETURN NEW; END IF;
  SELECT * INTO r FROM ge.domain_schema_registry d WHERE d.schema_ref = NEW.schema_ref AND d.table_name = TG_TABLE_NAME AND d.status = 'Approved'
   ORDER BY d.version DESC LIMIT 1;
  IF NOT FOUND THEN RAISE EXCEPTION 'unknown or unapproved schema_ref % for %', NEW.schema_ref, TG_TABLE_NAME USING ERRCODE = '23514'; END IF;
  IF st IS NOT NULL AND NOT (st = ANY (r.allowed_statuses)) THEN RAISE EXCEPTION 'status % not allowed for %', st, NEW.schema_ref USING ERRCODE = '23514'; END IF;
  IF NOT (NEW.payload ?& r.required_keys) THEN RAISE EXCEPTION 'payload missing required keys for %', NEW.schema_ref USING ERRCODE = '23514'; END IF;
  IF pg_column_size(NEW.payload) > r.max_payload_bytes THEN RAISE EXCEPTION 'payload exceeds % bytes', r.max_payload_bytes USING ERRCODE = '54000'; END IF;
  RETURN NEW;
END $$;

CREATE TRIGGER trg_agent_credential__revision BEFORE UPDATE ON ge.agent_credential FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_agent_credential__residency BEFORE INSERT OR UPDATE ON ge.agent_credential FOR EACH ROW EXECUTE FUNCTION ge.fn_row_region_guard();

CREATE TRIGGER trg_agent_message__revision BEFORE UPDATE ON ge.agent_message FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_agent_message__residency BEFORE INSERT OR UPDATE ON ge.agent_message FOR EACH ROW EXECUTE FUNCTION ge.fn_row_region_guard();

CREATE TRIGGER trg_ai_agent_definition__revision BEFORE UPDATE ON ge.ai_agent_definition FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_ai_agent_definition__freeze BEFORE UPDATE ON ge.ai_agent_definition FOR EACH ROW EXECUTE FUNCTION ge.fn_freeze_versioned();

CREATE TRIGGER trg_ai_cost_ledger__immutable BEFORE UPDATE OR DELETE ON ge.ai_cost_ledger FOR EACH ROW EXECUTE FUNCTION ge.fn_forbid_mutation();

CREATE TRIGGER trg_ai_eval_case__revision BEFORE UPDATE ON ge.ai_eval_case FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_ai_eval_case__freeze BEFORE UPDATE ON ge.ai_eval_case FOR EACH ROW EXECUTE FUNCTION ge.fn_freeze_versioned();

CREATE TRIGGER trg_ai_eval_case_result__immutable BEFORE UPDATE OR DELETE ON ge.ai_eval_case_result FOR EACH ROW EXECUTE FUNCTION ge.fn_forbid_mutation();

CREATE TRIGGER trg_ai_feedback__immutable BEFORE UPDATE OR DELETE ON ge.ai_feedback FOR EACH ROW EXECUTE FUNCTION ge.fn_forbid_mutation();

CREATE TRIGGER trg_ai_feedback__domain_registry BEFORE INSERT OR UPDATE ON ge.ai_feedback FOR EACH ROW EXECUTE FUNCTION ge.fn_validate_typed_domain_row();

CREATE TRIGGER trg_ai_model_run__immutable BEFORE UPDATE OR DELETE ON ge.ai_model_run FOR EACH ROW EXECUTE FUNCTION ge.fn_forbid_mutation();

CREATE TRIGGER trg_ana_account_projection__revision BEFORE UPDATE ON ge.ana_account_projection FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_ana_admin_projection__revision BEFORE UPDATE ON ge.ana_admin_projection FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_ana_forecast__immutable BEFORE UPDATE OR DELETE ON ge.ana_forecast FOR EACH ROW EXECUTE FUNCTION ge.fn_forbid_mutation();

CREATE TRIGGER trg_ana_forecast__domain_registry BEFORE INSERT OR UPDATE ON ge.ana_forecast FOR EACH ROW EXECUTE FUNCTION ge.fn_validate_typed_domain_row();

CREATE TRIGGER trg_ana_metric_definition__revision BEFORE UPDATE ON ge.ana_metric_definition FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_ana_metric_definition__freeze BEFORE UPDATE ON ge.ana_metric_definition FOR EACH ROW EXECUTE FUNCTION ge.fn_freeze_versioned();

CREATE TRIGGER trg_ana_metric_snapshot__immutable BEFORE UPDATE OR DELETE ON ge.ana_metric_snapshot FOR EACH ROW EXECUTE FUNCTION ge.fn_forbid_mutation();

CREATE TRIGGER trg_ana_metric_snapshot__domain_registry BEFORE INSERT OR UPDATE ON ge.ana_metric_snapshot FOR EACH ROW EXECUTE FUNCTION ge.fn_validate_typed_domain_row();

CREATE TRIGGER trg_ana_pipeline_projection__revision BEFORE UPDATE ON ge.ana_pipeline_projection FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_ana_report_subscription__revision BEFORE UPDATE ON ge.ana_report_subscription FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_ana_stage_metric__immutable BEFORE UPDATE OR DELETE ON ge.ana_stage_metric FOR EACH ROW EXECUTE FUNCTION ge.fn_forbid_mutation();

CREATE TRIGGER trg_ana_stage_metric__domain_registry BEFORE INSERT OR UPDATE ON ge.ana_stage_metric FOR EACH ROW EXECUTE FUNCTION ge.fn_validate_typed_domain_row();

CREATE TRIGGER trg_api_key__residency BEFORE INSERT OR UPDATE ON ge.api_key FOR EACH ROW EXECUTE FUNCTION ge.fn_row_region_guard();

CREATE TRIGGER trg_aut_autonomy_plan__revision BEFORE UPDATE ON ge.aut_autonomy_plan FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_aut_config_revision__revision BEFORE UPDATE ON ge.aut_config_revision FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_aut_config_revision__freeze BEFORE UPDATE ON ge.aut_config_revision FOR EACH ROW EXECUTE FUNCTION ge.fn_freeze_versioned();

CREATE TRIGGER trg_aut_conflict_case__revision BEFORE UPDATE ON ge.aut_conflict_case FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_aut_node_template__revision BEFORE UPDATE ON ge.aut_node_template FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_aut_node_template__freeze BEFORE UPDATE ON ge.aut_node_template FOR EACH ROW EXECUTE FUNCTION ge.fn_freeze_versioned();

CREATE TRIGGER trg_aut_run_conflict__revision BEFORE UPDATE ON ge.aut_run_conflict FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_aut_trigger__revision BEFORE UPDATE ON ge.aut_trigger FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_aut_workflow__revision BEFORE UPDATE ON ge.aut_workflow FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_aut_workflow_revision__revision BEFORE UPDATE ON ge.aut_workflow_revision FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_aut_workflow_revision__freeze BEFORE UPDATE ON ge.aut_workflow_revision FOR EACH ROW EXECUTE FUNCTION ge.fn_freeze_versioned();

CREATE TRIGGER trg_aut_workflow_template__revision BEFORE UPDATE ON ge.aut_workflow_template FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_aut_workflow_template__freeze BEFORE UPDATE ON ge.aut_workflow_template FOR EACH ROW EXECUTE FUNCTION ge.fn_freeze_versioned();

CREATE TRIGGER trg_bid_file__revision BEFORE UPDATE ON ge.bid_file FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_bid_file__residency BEFORE INSERT OR UPDATE ON ge.bid_file FOR EACH ROW EXECUTE FUNCTION ge.fn_row_region_guard();

CREATE TRIGGER trg_bid_package__revision BEFORE UPDATE ON ge.bid_package FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_bid_package__residency BEFORE INSERT OR UPDATE ON ge.bid_package FOR EACH ROW EXECUTE FUNCTION ge.fn_row_region_guard();

CREATE TRIGGER trg_bid_submission__revision BEFORE UPDATE ON ge.bid_submission FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_bid_submission__residency BEFORE INSERT OR UPDATE ON ge.bid_submission FOR EACH ROW EXECUTE FUNCTION ge.fn_row_region_guard();

CREATE TRIGGER trg_cat_capability__revision BEFORE UPDATE ON ge.cat_capability FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_cat_chunk__immutable BEFORE UPDATE OR DELETE ON ge.cat_chunk FOR EACH ROW EXECUTE FUNCTION ge.fn_forbid_mutation();

CREATE TRIGGER trg_cat_chunk__domain_registry BEFORE INSERT OR UPDATE ON ge.cat_chunk FOR EACH ROW EXECUTE FUNCTION ge.fn_validate_typed_domain_row();

CREATE TRIGGER trg_cat_claim__revision BEFORE UPDATE ON ge.cat_claim FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_cat_claim__freeze BEFORE UPDATE ON ge.cat_claim FOR EACH ROW EXECUTE FUNCTION ge.fn_freeze_versioned();

CREATE TRIGGER trg_cat_claim__domain_registry BEFORE INSERT OR UPDATE ON ge.cat_claim FOR EACH ROW EXECUTE FUNCTION ge.fn_validate_typed_domain_row();

CREATE TRIGGER trg_cat_claim_evidence__revision BEFORE UPDATE ON ge.cat_claim_evidence FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_cat_document__revision BEFORE UPDATE ON ge.cat_document FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_cat_document__freeze BEFORE UPDATE ON ge.cat_document FOR EACH ROW EXECUTE FUNCTION ge.fn_freeze_versioned();

CREATE TRIGGER trg_cat_document__domain_registry BEFORE INSERT OR UPDATE ON ge.cat_document FOR EACH ROW EXECUTE FUNCTION ge.fn_validate_typed_domain_row();

CREATE TRIGGER trg_cat_document_offering__revision BEFORE UPDATE ON ge.cat_document_offering FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_cat_embedding__immutable BEFORE UPDATE OR DELETE ON ge.cat_embedding FOR EACH ROW EXECUTE FUNCTION ge.fn_forbid_mutation();

CREATE TRIGGER trg_cat_embedding__domain_registry BEFORE INSERT OR UPDATE ON ge.cat_embedding FOR EACH ROW EXECUTE FUNCTION ge.fn_validate_typed_domain_row();

CREATE TRIGGER trg_cat_launch_approval__immutable BEFORE UPDATE OR DELETE ON ge.cat_launch_approval FOR EACH ROW EXECUTE FUNCTION ge.fn_forbid_mutation();

CREATE TRIGGER trg_cat_offering_capability__revision BEFORE UPDATE ON ge.cat_offering_capability FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_cat_offering_capability__freeze BEFORE UPDATE ON ge.cat_offering_capability FOR EACH ROW EXECUTE FUNCTION ge.fn_freeze_versioned();

CREATE TRIGGER trg_cat_offering_version__revision BEFORE UPDATE ON ge.cat_offering_version FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_cat_offering_version__freeze BEFORE UPDATE ON ge.cat_offering_version FOR EACH ROW EXECUTE FUNCTION ge.fn_freeze_versioned();

CREATE TRIGGER trg_cat_price_version__revision BEFORE UPDATE ON ge.cat_price_version FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_cat_price_version__freeze BEFORE UPDATE ON ge.cat_price_version FOR EACH ROW EXECUTE FUNCTION ge.fn_freeze_versioned();

CREATE TRIGGER trg_coaching_feedback__revision BEFORE UPDATE ON ge.coaching_feedback FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_coaching_feedback__residency BEFORE INSERT OR UPDATE ON ge.coaching_feedback FOR EACH ROW EXECUTE FUNCTION ge.fn_row_region_guard();

CREATE TRIGGER trg_coaching_rubric__revision BEFORE UPDATE ON ge.coaching_rubric FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_coaching_rubric__residency BEFORE INSERT OR UPDATE ON ge.coaching_rubric FOR EACH ROW EXECUTE FUNCTION ge.fn_row_region_guard();

CREATE TRIGGER trg_coaching_share__revision BEFORE UPDATE ON ge.coaching_share FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_coaching_share__residency BEFORE INSERT OR UPDATE ON ge.coaching_share FOR EACH ROW EXECUTE FUNCTION ge.fn_row_region_guard();

CREATE TRIGGER trg_com_bid__revision BEFORE UPDATE ON ge.com_bid FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_com_bid__domain_registry BEFORE INSERT OR UPDATE ON ge.com_bid FOR EACH ROW EXECUTE FUNCTION ge.fn_validate_typed_domain_row();

CREATE TRIGGER trg_com_bid_checklist_item__revision BEFORE UPDATE ON ge.com_bid_checklist_item FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_com_contract__revision BEFORE UPDATE ON ge.com_contract FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_com_contract__domain_registry BEFORE INSERT OR UPDATE ON ge.com_contract FOR EACH ROW EXECUTE FUNCTION ge.fn_validate_typed_domain_row();

CREATE TRIGGER trg_com_contract_party__revision BEFORE UPDATE ON ge.com_contract_party FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_com_discrepancy_case__revision BEFORE UPDATE ON ge.com_discrepancy_case FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_com_fulfillment_event__immutable BEFORE UPDATE OR DELETE ON ge.com_fulfillment_event FOR EACH ROW EXECUTE FUNCTION ge.fn_forbid_mutation();

CREATE TRIGGER trg_com_fulfillment_event__domain_registry BEFORE INSERT OR UPDATE ON ge.com_fulfillment_event FOR EACH ROW EXECUTE FUNCTION ge.fn_validate_typed_domain_row();

CREATE TRIGGER trg_com_fulfillment_milestone__revision BEFORE UPDATE ON ge.com_fulfillment_milestone FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_com_inventory_reservation__revision BEFORE UPDATE ON ge.com_inventory_reservation FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_com_invoice__revision BEFORE UPDATE ON ge.com_invoice FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_com_invoice__domain_registry BEFORE INSERT OR UPDATE ON ge.com_invoice FOR EACH ROW EXECUTE FUNCTION ge.fn_validate_typed_domain_row();

CREATE TRIGGER trg_com_invoice_line__revision BEFORE UPDATE ON ge.com_invoice_line FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_com_negotiation__revision BEFORE UPDATE ON ge.com_negotiation FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_com_negotiation__domain_registry BEFORE INSERT OR UPDATE ON ge.com_negotiation FOR EACH ROW EXECUTE FUNCTION ge.fn_validate_typed_domain_row();

CREATE TRIGGER trg_com_objection__revision BEFORE UPDATE ON ge.com_objection FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_com_objection__domain_registry BEFORE INSERT OR UPDATE ON ge.com_objection FOR EACH ROW EXECUTE FUNCTION ge.fn_validate_typed_domain_row();

CREATE TRIGGER trg_com_order__revision BEFORE UPDATE ON ge.com_order FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_com_order__domain_registry BEFORE INSERT OR UPDATE ON ge.com_order FOR EACH ROW EXECUTE FUNCTION ge.fn_validate_typed_domain_row();

CREATE TRIGGER trg_com_order_line__revision BEFORE UPDATE ON ge.com_order_line FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_com_order_line__domain_registry BEFORE INSERT OR UPDATE ON ge.com_order_line FOR EACH ROW EXECUTE FUNCTION ge.fn_validate_typed_domain_row();

CREATE TRIGGER trg_com_payable_entry__immutable BEFORE UPDATE OR DELETE ON ge.com_payable_entry FOR EACH ROW EXECUTE FUNCTION ge.fn_forbid_mutation();

CREATE TRIGGER trg_com_payment__revision BEFORE UPDATE ON ge.com_payment FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_com_payment__domain_registry BEFORE INSERT OR UPDATE ON ge.com_payment FOR EACH ROW EXECUTE FUNCTION ge.fn_validate_typed_domain_row();

CREATE TRIGGER trg_com_payment_allocation__immutable BEFORE UPDATE OR DELETE ON ge.com_payment_allocation FOR EACH ROW EXECUTE FUNCTION ge.fn_forbid_mutation();

CREATE TRIGGER trg_com_proposal__revision BEFORE UPDATE ON ge.com_proposal FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_com_proposal__domain_registry BEFORE INSERT OR UPDATE ON ge.com_proposal FOR EACH ROW EXECUTE FUNCTION ge.fn_validate_typed_domain_row();

CREATE TRIGGER trg_com_proposal_version__revision BEFORE UPDATE ON ge.com_proposal_version FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_com_proposal_version__freeze BEFORE UPDATE ON ge.com_proposal_version FOR EACH ROW EXECUTE FUNCTION ge.fn_freeze_versioned();

CREATE TRIGGER trg_com_proposal_version__domain_registry BEFORE INSERT OR UPDATE ON ge.com_proposal_version FOR EACH ROW EXECUTE FUNCTION ge.fn_validate_typed_domain_row();

CREATE TRIGGER trg_com_quote__revision BEFORE UPDATE ON ge.com_quote FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_com_quote__domain_registry BEFORE INSERT OR UPDATE ON ge.com_quote FOR EACH ROW EXECUTE FUNCTION ge.fn_validate_typed_domain_row();

CREATE TRIGGER trg_com_quote_line__revision BEFORE UPDATE ON ge.com_quote_line FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_com_quote_line__domain_registry BEFORE INSERT OR UPDATE ON ge.com_quote_line FOR EACH ROW EXECUTE FUNCTION ge.fn_validate_typed_domain_row();

CREATE TRIGGER trg_com_receivable_entry__immutable BEFORE UPDATE OR DELETE ON ge.com_receivable_entry FOR EACH ROW EXECUTE FUNCTION ge.fn_forbid_mutation();

CREATE TRIGGER trg_com_signature_event__immutable BEFORE UPDATE OR DELETE ON ge.com_signature_event FOR EACH ROW EXECUTE FUNCTION ge.fn_forbid_mutation();

CREATE TRIGGER trg_com_sku_availability__revision BEFORE UPDATE ON ge.com_sku_availability FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_commerce_order__immutable BEFORE UPDATE OR DELETE ON ge.commerce_order FOR EACH ROW EXECUTE FUNCTION ge.fn_forbid_mutation();

CREATE TRIGGER trg_commerce_order__residency BEFORE INSERT OR UPDATE ON ge.commerce_order FOR EACH ROW EXECUTE FUNCTION ge.fn_row_region_guard();

CREATE TRIGGER trg_counterparty_agent__revision BEFORE UPDATE ON ge.counterparty_agent FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_counterparty_agent__residency BEFORE INSERT OR UPDATE ON ge.counterparty_agent FOR EACH ROW EXECUTE FUNCTION ge.fn_row_region_guard();

CREATE TRIGGER trg_crm_activity__immutable BEFORE UPDATE OR DELETE ON ge.crm_activity FOR EACH ROW EXECUTE FUNCTION ge.fn_forbid_mutation();

CREATE TRIGGER trg_crm_activity__domain_registry BEFORE INSERT OR UPDATE ON ge.crm_activity FOR EACH ROW EXECUTE FUNCTION ge.fn_validate_typed_domain_row();

CREATE TRIGGER trg_crm_closure_policy__revision BEFORE UPDATE ON ge.crm_closure_policy FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_crm_closure_policy__freeze BEFORE UPDATE ON ge.crm_closure_policy FOR EACH ROW EXECUTE FUNCTION ge.fn_freeze_versioned();

CREATE TRIGGER trg_crm_deal__revision BEFORE UPDATE ON ge.crm_deal FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_crm_deal__domain_registry BEFORE INSERT OR UPDATE ON ge.crm_deal FOR EACH ROW EXECUTE FUNCTION ge.fn_validate_typed_domain_row();

CREATE TRIGGER trg_crm_deal_contact__revision BEFORE UPDATE ON ge.crm_deal_contact FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_crm_form__revision BEFORE UPDATE ON ge.crm_form FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_crm_form__domain_registry BEFORE INSERT OR UPDATE ON ge.crm_form FOR EACH ROW EXECUTE FUNCTION ge.fn_validate_typed_domain_row();

CREATE TRIGGER trg_crm_form_version__revision BEFORE UPDATE ON ge.crm_form_version FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_crm_form_version__freeze BEFORE UPDATE ON ge.crm_form_version FOR EACH ROW EXECUTE FUNCTION ge.fn_freeze_versioned();

CREATE TRIGGER trg_crm_lead__revision BEFORE UPDATE ON ge.crm_lead FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_crm_lead__domain_registry BEFORE INSERT OR UPDATE ON ge.crm_lead FOR EACH ROW EXECUTE FUNCTION ge.fn_validate_typed_domain_row();

CREATE TRIGGER trg_crm_pipeline__revision BEFORE UPDATE ON ge.crm_pipeline FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_crm_pipeline__freeze BEFORE UPDATE ON ge.crm_pipeline FOR EACH ROW EXECUTE FUNCTION ge.fn_freeze_versioned();

CREATE TRIGGER trg_crm_stage__revision BEFORE UPDATE ON ge.crm_stage FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_crm_stage__freeze BEFORE UPDATE ON ge.crm_stage FOR EACH ROW EXECUTE FUNCTION ge.fn_freeze_versioned();

CREATE TRIGGER trg_crm_stage__domain_registry BEFORE INSERT OR UPDATE ON ge.crm_stage FOR EACH ROW EXECUTE FUNCTION ge.fn_validate_typed_domain_row();

CREATE TRIGGER trg_crm_stage_transition__immutable BEFORE UPDATE OR DELETE ON ge.crm_stage_transition FOR EACH ROW EXECUTE FUNCTION ge.fn_forbid_mutation();

CREATE TRIGGER trg_crm_submission__immutable BEFORE UPDATE OR DELETE ON ge.crm_submission FOR EACH ROW EXECUTE FUNCTION ge.fn_forbid_mutation();

CREATE TRIGGER trg_dispute_case__revision BEFORE UPDATE ON ge.dispute_case FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_dispute_case__residency BEFORE INSERT OR UPDATE ON ge.dispute_case FOR EACH ROW EXECUTE FUNCTION ge.fn_row_region_guard();

CREATE TRIGGER trg_effect_receipt__revision BEFORE UPDATE ON ge.effect_receipt FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_effect_receipt__residency BEFORE INSERT OR UPDATE ON ge.effect_receipt FOR EACH ROW EXECUTE FUNCTION ge.fn_row_region_guard();

CREATE TRIGGER trg_eng_calendar_link__revision BEFORE UPDATE ON ge.eng_calendar_link FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_eng_calendar_link__domain_registry BEFORE INSERT OR UPDATE ON ge.eng_calendar_link FOR EACH ROW EXECUTE FUNCTION ge.fn_validate_typed_domain_row();

CREATE TRIGGER trg_eng_chat_session__revision BEFORE UPDATE ON ge.eng_chat_session FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_eng_delivery_event__immutable BEFORE UPDATE OR DELETE ON ge.eng_delivery_event FOR EACH ROW EXECUTE FUNCTION ge.fn_forbid_mutation();

CREATE TRIGGER trg_eng_delivery_event__domain_registry BEFORE INSERT OR UPDATE ON ge.eng_delivery_event FOR EACH ROW EXECUTE FUNCTION ge.fn_validate_typed_domain_row();

CREATE TRIGGER trg_eng_enrollment__revision BEFORE UPDATE ON ge.eng_enrollment FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_eng_enrollment__domain_registry BEFORE INSERT OR UPDATE ON ge.eng_enrollment FOR EACH ROW EXECUTE FUNCTION ge.fn_validate_typed_domain_row();

CREATE TRIGGER trg_eng_identity_link__revision BEFORE UPDATE ON ge.eng_identity_link FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_eng_identity_link__domain_registry BEFORE INSERT OR UPDATE ON ge.eng_identity_link FOR EACH ROW EXECUTE FUNCTION ge.fn_validate_typed_domain_row();

CREATE TRIGGER trg_eng_inbound_event__immutable BEFORE UPDATE OR DELETE ON ge.eng_inbound_event FOR EACH ROW EXECUTE FUNCTION ge.fn_forbid_mutation();

CREATE TRIGGER trg_eng_inbound_event__domain_registry BEFORE INSERT OR UPDATE ON ge.eng_inbound_event FOR EACH ROW EXECUTE FUNCTION ge.fn_validate_typed_domain_row();

CREATE TRIGGER trg_eng_intent__immutable BEFORE UPDATE OR DELETE ON ge.eng_intent FOR EACH ROW EXECUTE FUNCTION ge.fn_forbid_mutation();

CREATE TRIGGER trg_eng_meeting__revision BEFORE UPDATE ON ge.eng_meeting FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_eng_meeting__domain_registry BEFORE INSERT OR UPDATE ON ge.eng_meeting FOR EACH ROW EXECUTE FUNCTION ge.fn_validate_typed_domain_row();

CREATE TRIGGER trg_eng_message__revision BEFORE UPDATE ON ge.eng_message FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_eng_message__domain_registry BEFORE INSERT OR UPDATE ON ge.eng_message FOR EACH ROW EXECUTE FUNCTION ge.fn_validate_typed_domain_row();

CREATE TRIGGER trg_eng_message_claim__revision BEFORE UPDATE ON ge.eng_message_claim FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_eng_message_draft__revision BEFORE UPDATE ON ge.eng_message_draft FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_eng_message_draft__domain_registry BEFORE INSERT OR UPDATE ON ge.eng_message_draft FOR EACH ROW EXECUTE FUNCTION ge.fn_validate_typed_domain_row();

CREATE TRIGGER trg_eng_message_template__revision BEFORE UPDATE ON ge.eng_message_template FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_eng_message_template__freeze BEFORE UPDATE ON ge.eng_message_template FOR EACH ROW EXECUTE FUNCTION ge.fn_freeze_versioned();

CREATE TRIGGER trg_eng_message_template__domain_registry BEFORE INSERT OR UPDATE ON ge.eng_message_template FOR EACH ROW EXECUTE FUNCTION ge.fn_validate_typed_domain_row();

CREATE TRIGGER trg_eng_routing_rule__revision BEFORE UPDATE ON ge.eng_routing_rule FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_eng_routing_rule__freeze BEFORE UPDATE ON ge.eng_routing_rule FOR EACH ROW EXECUTE FUNCTION ge.fn_freeze_versioned();

CREATE TRIGGER trg_eng_routing_rule__domain_registry BEFORE INSERT OR UPDATE ON ge.eng_routing_rule FOR EACH ROW EXECUTE FUNCTION ge.fn_validate_typed_domain_row();

CREATE TRIGGER trg_eng_sequence__revision BEFORE UPDATE ON ge.eng_sequence FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_eng_sequence__freeze BEFORE UPDATE ON ge.eng_sequence FOR EACH ROW EXECUTE FUNCTION ge.fn_freeze_versioned();

CREATE TRIGGER trg_eng_sequence__domain_registry BEFORE INSERT OR UPDATE ON ge.eng_sequence FOR EACH ROW EXECUTE FUNCTION ge.fn_validate_typed_domain_row();

CREATE TRIGGER trg_eng_sequence_step__revision BEFORE UPDATE ON ge.eng_sequence_step FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_eng_sequence_step__freeze BEFORE UPDATE ON ge.eng_sequence_step FOR EACH ROW EXECUTE FUNCTION ge.fn_freeze_versioned();

CREATE TRIGGER trg_eng_sequence_step__domain_registry BEFORE INSERT OR UPDATE ON ge.eng_sequence_step FOR EACH ROW EXECUTE FUNCTION ge.fn_validate_typed_domain_row();

CREATE TRIGGER trg_eng_thread__revision BEFORE UPDATE ON ge.eng_thread FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_eng_thread__domain_registry BEFORE INSERT OR UPDATE ON ge.eng_thread FOR EACH ROW EXECUTE FUNCTION ge.fn_validate_typed_domain_row();

CREATE TRIGGER trg_gov_approval__immutable BEFORE UPDATE OR DELETE ON ge.gov_approval FOR EACH ROW EXECUTE FUNCTION ge.fn_forbid_mutation();

CREATE TRIGGER trg_gov_approval__domain_registry BEFORE INSERT OR UPDATE ON ge.gov_approval FOR EACH ROW EXECUTE FUNCTION ge.fn_validate_typed_domain_row();

CREATE TRIGGER trg_gov_approval_delegation__revision BEFORE UPDATE ON ge.gov_approval_delegation FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_gov_approval_policy__revision BEFORE UPDATE ON ge.gov_approval_policy FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_gov_approval_policy__freeze BEFORE UPDATE ON ge.gov_approval_policy FOR EACH ROW EXECUTE FUNCTION ge.fn_freeze_versioned();

CREATE TRIGGER trg_gov_eligibility_decision__immutable BEFORE UPDATE OR DELETE ON ge.gov_eligibility_decision FOR EACH ROW EXECUTE FUNCTION ge.fn_forbid_mutation();

CREATE TRIGGER trg_gov_legal_hold__revision BEFORE UPDATE ON ge.gov_legal_hold FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_gov_policy_decision__immutable BEFORE UPDATE OR DELETE ON ge.gov_policy_decision FOR EACH ROW EXECUTE FUNCTION ge.fn_forbid_mutation();

CREATE TRIGGER trg_gov_policy_version__revision BEFORE UPDATE ON ge.gov_policy_version FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_gov_policy_version__freeze BEFORE UPDATE ON ge.gov_policy_version FOR EACH ROW EXECUTE FUNCTION ge.fn_freeze_versioned();

CREATE TRIGGER trg_gov_retention_policy__revision BEFORE UPDATE ON ge.gov_retention_policy FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_gov_retention_policy__freeze BEFORE UPDATE ON ge.gov_retention_policy FOR EACH ROW EXECUTE FUNCTION ge.fn_freeze_versioned();

CREATE TRIGGER trg_int_credential_ref__revision BEFORE UPDATE ON ge.int_credential_ref FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_int_provider_event__immutable BEFORE UPDATE OR DELETE ON ge.int_provider_event FOR EACH ROW EXECUTE FUNCTION ge.fn_forbid_mutation();

CREATE TRIGGER trg_int_quota__revision BEFORE UPDATE ON ge.int_quota FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_intel_alias__revision BEFORE UPDATE ON ge.intel_alias FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_intel_competitor__revision BEFORE UPDATE ON ge.intel_competitor FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_intel_competitor__domain_registry BEFORE INSERT OR UPDATE ON ge.intel_competitor FOR EACH ROW EXECUTE FUNCTION ge.fn_validate_typed_domain_row();

CREATE TRIGGER trg_intel_contact__revision BEFORE UPDATE ON ge.intel_contact FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_intel_contact__domain_registry BEFORE INSERT OR UPDATE ON ge.intel_contact FOR EACH ROW EXECUTE FUNCTION ge.fn_validate_typed_domain_row();

CREATE TRIGGER trg_intel_contact_source__immutable BEFORE UPDATE OR DELETE ON ge.intel_contact_source FOR EACH ROW EXECUTE FUNCTION ge.fn_forbid_mutation();

CREATE TRIGGER trg_intel_contact_source__domain_registry BEFORE INSERT OR UPDATE ON ge.intel_contact_source FOR EACH ROW EXECUTE FUNCTION ge.fn_validate_typed_domain_row();

CREATE TRIGGER trg_intel_contact_verification__immutable BEFORE UPDATE OR DELETE ON ge.intel_contact_verification FOR EACH ROW EXECUTE FUNCTION ge.fn_forbid_mutation();

CREATE TRIGGER trg_intel_contact_verification__domain_registry BEFORE INSERT OR UPDATE ON ge.intel_contact_verification FOR EACH ROW EXECUTE FUNCTION ge.fn_validate_typed_domain_row();

CREATE TRIGGER trg_intel_evidence__revision BEFORE UPDATE ON ge.intel_evidence FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_intel_evidence__domain_registry BEFORE INSERT OR UPDATE ON ge.intel_evidence FOR EACH ROW EXECUTE FUNCTION ge.fn_validate_typed_domain_row();

CREATE TRIGGER trg_intel_fetch_log__immutable BEFORE UPDATE OR DELETE ON ge.intel_fetch_log FOR EACH ROW EXECUTE FUNCTION ge.fn_forbid_mutation();

CREATE TRIGGER trg_intel_location__revision BEFORE UPDATE ON ge.intel_location FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_intel_market_event__revision BEFORE UPDATE ON ge.intel_market_event FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_intel_market_event__domain_registry BEFORE INSERT OR UPDATE ON ge.intel_market_event FOR EACH ROW EXECUTE FUNCTION ge.fn_validate_typed_domain_row();

CREATE TRIGGER trg_intel_match__revision BEFORE UPDATE ON ge.intel_match FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_intel_need__revision BEFORE UPDATE ON ge.intel_need FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_intel_need__domain_registry BEFORE INSERT OR UPDATE ON ge.intel_need FOR EACH ROW EXECUTE FUNCTION ge.fn_validate_typed_domain_row();

CREATE TRIGGER trg_intel_need_evidence__immutable BEFORE UPDATE OR DELETE ON ge.intel_need_evidence FOR EACH ROW EXECUTE FUNCTION ge.fn_forbid_mutation();

CREATE TRIGGER trg_intel_need_evidence__domain_registry BEFORE INSERT OR UPDATE ON ge.intel_need_evidence FOR EACH ROW EXECUTE FUNCTION ge.fn_validate_typed_domain_row();

CREATE TRIGGER trg_intel_opportunity__revision BEFORE UPDATE ON ge.intel_opportunity FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_intel_opportunity__domain_registry BEFORE INSERT OR UPDATE ON ge.intel_opportunity FOR EACH ROW EXECUTE FUNCTION ge.fn_validate_typed_domain_row();

CREATE TRIGGER trg_intel_opportunity_contact__revision BEFORE UPDATE ON ge.intel_opportunity_contact FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_intel_organization__revision BEFORE UPDATE ON ge.intel_organization FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_intel_organization__domain_registry BEFORE INSERT OR UPDATE ON ge.intel_organization FOR EACH ROW EXECUTE FUNCTION ge.fn_validate_typed_domain_row();

CREATE TRIGGER trg_intel_query_run__immutable BEFORE UPDATE OR DELETE ON ge.intel_query_run FOR EACH ROW EXECUTE FUNCTION ge.fn_forbid_mutation();

CREATE TRIGGER trg_intel_review__immutable BEFORE UPDATE OR DELETE ON ge.intel_review FOR EACH ROW EXECUTE FUNCTION ge.fn_forbid_mutation();

CREATE TRIGGER trg_intel_role_hypothesis__revision BEFORE UPDATE ON ge.intel_role_hypothesis FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_intel_score_version__immutable BEFORE UPDATE OR DELETE ON ge.intel_score_version FOR EACH ROW EXECUTE FUNCTION ge.fn_forbid_mutation();

CREATE TRIGGER trg_intel_score_version__domain_registry BEFORE INSERT OR UPDATE ON ge.intel_score_version FOR EACH ROW EXECUTE FUNCTION ge.fn_validate_typed_domain_row();

CREATE TRIGGER trg_intel_scoring_model__revision BEFORE UPDATE ON ge.intel_scoring_model FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_intel_scoring_model__freeze BEFORE UPDATE ON ge.intel_scoring_model FOR EACH ROW EXECUTE FUNCTION ge.fn_freeze_versioned();

CREATE TRIGGER trg_intel_search_plan__revision BEFORE UPDATE ON ge.intel_search_plan FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_intel_search_plan__freeze BEFORE UPDATE ON ge.intel_search_plan FOR EACH ROW EXECUTE FUNCTION ge.fn_freeze_versioned();

CREATE TRIGGER trg_intel_search_plan__domain_registry BEFORE INSERT OR UPDATE ON ge.intel_search_plan FOR EACH ROW EXECUTE FUNCTION ge.fn_validate_typed_domain_row();

CREATE TRIGGER trg_intel_signal__revision BEFORE UPDATE ON ge.intel_signal FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_intel_signal__domain_registry BEFORE INSERT OR UPDATE ON ge.intel_signal FOR EACH ROW EXECUTE FUNCTION ge.fn_validate_typed_domain_row();

CREATE TRIGGER trg_intel_signal_evidence__revision BEFORE UPDATE ON ge.intel_signal_evidence FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_intel_signal_type__revision BEFORE UPDATE ON ge.intel_signal_type FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_intel_signal_type__domain_registry BEFORE INSERT OR UPDATE ON ge.intel_signal_type FOR EACH ROW EXECUTE FUNCTION ge.fn_validate_typed_domain_row();

CREATE TRIGGER trg_intel_social_post__revision BEFORE UPDATE ON ge.intel_social_post FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_intel_social_post__domain_registry BEFORE INSERT OR UPDATE ON ge.intel_social_post FOR EACH ROW EXECUTE FUNCTION ge.fn_validate_typed_domain_row();

CREATE TRIGGER trg_intel_source__revision BEFORE UPDATE ON ge.intel_source FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_intel_source__domain_registry BEFORE INSERT OR UPDATE ON ge.intel_source FOR EACH ROW EXECUTE FUNCTION ge.fn_validate_typed_domain_row();

CREATE TRIGGER trg_intel_source_policy__revision BEFORE UPDATE ON ge.intel_source_policy FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_intel_source_policy__freeze BEFORE UPDATE ON ge.intel_source_policy FOR EACH ROW EXECUTE FUNCTION ge.fn_freeze_versioned();

CREATE TRIGGER trg_intel_source_policy__domain_registry BEFORE INSERT OR UPDATE ON ge.intel_source_policy FOR EACH ROW EXECUTE FUNCTION ge.fn_validate_typed_domain_row();

CREATE TRIGGER trg_intel_source_record__revision BEFORE UPDATE ON ge.intel_source_record FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_intel_source_record__domain_registry BEFORE INSERT OR UPDATE ON ge.intel_source_record FOR EACH ROW EXECUTE FUNCTION ge.fn_validate_typed_domain_row();

CREATE TRIGGER trg_inv_access_grant__revision BEFORE UPDATE ON ge.inv_access_grant FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_inv_access_grant__residency BEFORE INSERT OR UPDATE ON ge.inv_access_grant FOR EACH ROW EXECUTE FUNCTION ge.fn_row_region_guard();

CREATE TRIGGER trg_inv_accreditation_verification__revision BEFORE UPDATE ON ge.inv_accreditation_verification FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_inv_accreditation_verification__residency BEFORE INSERT OR UPDATE ON ge.inv_accreditation_verification FOR EACH ROW EXECUTE FUNCTION ge.fn_row_region_guard();

CREATE TRIGGER trg_inv_advice_boundary_event__immutable BEFORE UPDATE OR DELETE ON ge.inv_advice_boundary_event FOR EACH ROW EXECUTE FUNCTION ge.fn_forbid_mutation();

CREATE TRIGGER trg_inv_advice_boundary_event__residency BEFORE INSERT OR UPDATE ON ge.inv_advice_boundary_event FOR EACH ROW EXECUTE FUNCTION ge.fn_row_region_guard();

CREATE TRIGGER trg_inv_adviser_referral__revision BEFORE UPDATE ON ge.inv_adviser_referral FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_inv_adviser_referral__residency BEFORE INSERT OR UPDATE ON ge.inv_adviser_referral FOR EACH ROW EXECUTE FUNCTION ge.fn_row_region_guard();

CREATE TRIGGER trg_inv_agreement__revision BEFORE UPDATE ON ge.inv_agreement FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_inv_agreement__residency BEFORE INSERT OR UPDATE ON ge.inv_agreement FOR EACH ROW EXECUTE FUNCTION ge.fn_row_region_guard();

CREATE TRIGGER trg_inv_allotment__revision BEFORE UPDATE ON ge.inv_allotment FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_inv_allotment__residency BEFORE INSERT OR UPDATE ON ge.inv_allotment FOR EACH ROW EXECUTE FUNCTION ge.fn_row_region_guard();

CREATE TRIGGER trg_inv_allotment_clock__revision BEFORE UPDATE ON ge.inv_allotment_clock FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_inv_allotment_clock__residency BEFORE INSERT OR UPDATE ON ge.inv_allotment_clock FOR EACH ROW EXECUTE FUNCTION ge.fn_row_region_guard();

CREATE TRIGGER trg_inv_application_money_account__revision BEFORE UPDATE ON ge.inv_application_money_account FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_inv_application_money_account__residency BEFORE INSERT OR UPDATE ON ge.inv_application_money_account FOR EACH ROW EXECUTE FUNCTION ge.fn_row_region_guard();

CREATE TRIGGER trg_inv_approval__revision BEFORE UPDATE ON ge.inv_approval FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_inv_approval__residency BEFORE INSERT OR UPDATE ON ge.inv_approval FOR EACH ROW EXECUTE FUNCTION ge.fn_row_region_guard();

CREATE TRIGGER trg_inv_bank_account__revision BEFORE UPDATE ON ge.inv_bank_account FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_inv_bank_account__residency BEFORE INSERT OR UPDATE ON ge.inv_bank_account FOR EACH ROW EXECUTE FUNCTION ge.fn_row_region_guard();

CREATE TRIGGER trg_inv_cap_table_revision__immutable BEFORE UPDATE OR DELETE ON ge.inv_cap_table_revision FOR EACH ROW EXECUTE FUNCTION ge.fn_forbid_mutation();

CREATE TRIGGER trg_inv_cap_table_revision__residency BEFORE INSERT OR UPDATE ON ge.inv_cap_table_revision FOR EACH ROW EXECUTE FUNCTION ge.fn_row_region_guard();

CREATE TRIGGER trg_inv_capital_allocation__revision BEFORE UPDATE ON ge.inv_capital_allocation FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_inv_capital_allocation__residency BEFORE INSERT OR UPDATE ON ge.inv_capital_allocation FOR EACH ROW EXECUTE FUNCTION ge.fn_row_region_guard();

CREATE TRIGGER trg_inv_channel__revision BEFORE UPDATE ON ge.inv_channel FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_inv_channel__residency BEFORE INSERT OR UPDATE ON ge.inv_channel FOR EACH ROW EXECUTE FUNCTION ge.fn_row_region_guard();

CREATE TRIGGER trg_inv_claim__revision BEFORE UPDATE ON ge.inv_claim FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_inv_claim__residency BEFORE INSERT OR UPDATE ON ge.inv_claim FOR EACH ROW EXECUTE FUNCTION ge.fn_row_region_guard();

CREATE TRIGGER trg_inv_closing__revision BEFORE UPDATE ON ge.inv_closing FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_inv_closing__residency BEFORE INSERT OR UPDATE ON ge.inv_closing FOR EACH ROW EXECUTE FUNCTION ge.fn_row_region_guard();

CREATE TRIGGER trg_inv_closing_requirement__revision BEFORE UPDATE ON ge.inv_closing_requirement FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_inv_closing_requirement__residency BEFORE INSERT OR UPDATE ON ge.inv_closing_requirement FOR EACH ROW EXECUTE FUNCTION ge.fn_row_region_guard();

CREATE TRIGGER trg_inv_commitment__immutable BEFORE UPDATE OR DELETE ON ge.inv_commitment FOR EACH ROW EXECUTE FUNCTION ge.fn_forbid_mutation();

CREATE TRIGGER trg_inv_commitment__residency BEFORE INSERT OR UPDATE ON ge.inv_commitment FOR EACH ROW EXECUTE FUNCTION ge.fn_row_region_guard();

CREATE TRIGGER trg_inv_contact__revision BEFORE UPDATE ON ge.inv_contact FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_inv_contact__residency BEFORE INSERT OR UPDATE ON ge.inv_contact FOR EACH ROW EXECUTE FUNCTION ge.fn_row_region_guard();

CREATE TRIGGER trg_inv_contact_evidence__revision BEFORE UPDATE ON ge.inv_contact_evidence FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_inv_contact_evidence__residency BEFORE INSERT OR UPDATE ON ge.inv_contact_evidence FOR EACH ROW EXECUTE FUNCTION ge.fn_row_region_guard();

CREATE TRIGGER trg_inv_copilot_action__revision BEFORE UPDATE ON ge.inv_copilot_action FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_inv_copilot_action__residency BEFORE INSERT OR UPDATE ON ge.inv_copilot_action FOR EACH ROW EXECUTE FUNCTION ge.fn_row_region_guard();

CREATE TRIGGER trg_inv_counsel_signoff__revision BEFORE UPDATE ON ge.inv_counsel_signoff FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_inv_counsel_signoff__residency BEFORE INSERT OR UPDATE ON ge.inv_counsel_signoff FOR EACH ROW EXECUTE FUNCTION ge.fn_row_region_guard();

CREATE TRIGGER trg_inv_covenant__revision BEFORE UPDATE ON ge.inv_covenant FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_inv_covenant__residency BEFORE INSERT OR UPDATE ON ge.inv_covenant FOR EACH ROW EXECUTE FUNCTION ge.fn_row_region_guard();

CREATE TRIGGER trg_inv_crossborder_case__revision BEFORE UPDATE ON ge.inv_crossborder_case FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_inv_crossborder_case__residency BEFORE INSERT OR UPDATE ON ge.inv_crossborder_case FOR EACH ROW EXECUTE FUNCTION ge.fn_row_region_guard();

CREATE TRIGGER trg_inv_crossborder_requirement__revision BEFORE UPDATE ON ge.inv_crossborder_requirement FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_inv_crossborder_requirement__residency BEFORE INSERT OR UPDATE ON ge.inv_crossborder_requirement FOR EACH ROW EXECUTE FUNCTION ge.fn_row_region_guard();

CREATE TRIGGER trg_inv_dashboard_projection__revision BEFORE UPDATE ON ge.inv_dashboard_projection FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_inv_dashboard_projection__residency BEFORE INSERT OR UPDATE ON ge.inv_dashboard_projection FOR EACH ROW EXECUTE FUNCTION ge.fn_row_region_guard();

CREATE TRIGGER trg_inv_debt_case__revision BEFORE UPDATE ON ge.inv_debt_case FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_inv_debt_case__residency BEFORE INSERT OR UPDATE ON ge.inv_debt_case FOR EACH ROW EXECUTE FUNCTION ge.fn_row_region_guard();

CREATE TRIGGER trg_inv_debt_term__revision BEFORE UPDATE ON ge.inv_debt_term FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_inv_debt_term__residency BEFORE INSERT OR UPDATE ON ge.inv_debt_term FOR EACH ROW EXECUTE FUNCTION ge.fn_row_region_guard();

CREATE TRIGGER trg_inv_decision_action__revision BEFORE UPDATE ON ge.inv_decision_action FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_inv_decision_action__residency BEFORE INSERT OR UPDATE ON ge.inv_decision_action FOR EACH ROW EXECUTE FUNCTION ge.fn_row_region_guard();

CREATE TRIGGER trg_inv_delivery_event__revision BEFORE UPDATE ON ge.inv_delivery_event FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_inv_delivery_event__residency BEFORE INSERT OR UPDATE ON ge.inv_delivery_event FOR EACH ROW EXECUTE FUNCTION ge.fn_row_region_guard();

CREATE TRIGGER trg_inv_deployment_milestone__revision BEFORE UPDATE ON ge.inv_deployment_milestone FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_inv_deployment_milestone__residency BEFORE INSERT OR UPDATE ON ge.inv_deployment_milestone FOR EACH ROW EXECUTE FUNCTION ge.fn_row_region_guard();

CREATE TRIGGER trg_inv_diligence_request__revision BEFORE UPDATE ON ge.inv_diligence_request FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_inv_diligence_request__residency BEFORE INSERT OR UPDATE ON ge.inv_diligence_request FOR EACH ROW EXECUTE FUNCTION ge.fn_row_region_guard();

CREATE TRIGGER trg_inv_disclosure__revision BEFORE UPDATE ON ge.inv_disclosure FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_inv_disclosure__residency BEFORE INSERT OR UPDATE ON ge.inv_disclosure FOR EACH ROW EXECUTE FUNCTION ge.fn_row_region_guard();

CREATE TRIGGER trg_inv_document__revision BEFORE UPDATE ON ge.inv_document FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_inv_document__residency BEFORE INSERT OR UPDATE ON ge.inv_document FOR EACH ROW EXECUTE FUNCTION ge.fn_row_region_guard();

CREATE TRIGGER trg_inv_eligibility_check__revision BEFORE UPDATE ON ge.inv_eligibility_check FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_inv_eligibility_check__residency BEFORE INSERT OR UPDATE ON ge.inv_eligibility_check FOR EACH ROW EXECUTE FUNCTION ge.fn_row_region_guard();

CREATE TRIGGER trg_inv_enrollment__revision BEFORE UPDATE ON ge.inv_enrollment FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_inv_enrollment__residency BEFORE INSERT OR UPDATE ON ge.inv_enrollment FOR EACH ROW EXECUTE FUNCTION ge.fn_row_region_guard();

CREATE TRIGGER trg_inv_esg_commitment__revision BEFORE UPDATE ON ge.inv_esg_commitment FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_inv_esg_commitment__residency BEFORE INSERT OR UPDATE ON ge.inv_esg_commitment FOR EACH ROW EXECUTE FUNCTION ge.fn_row_region_guard();

CREATE TRIGGER trg_inv_esg_disclosure__revision BEFORE UPDATE ON ge.inv_esg_disclosure FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_inv_esg_disclosure__residency BEFORE INSERT OR UPDATE ON ge.inv_esg_disclosure FOR EACH ROW EXECUTE FUNCTION ge.fn_row_region_guard();

CREATE TRIGGER trg_inv_esg_indicator__revision BEFORE UPDATE ON ge.inv_esg_indicator FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_inv_esg_indicator__residency BEFORE INSERT OR UPDATE ON ge.inv_esg_indicator FOR EACH ROW EXECUTE FUNCTION ge.fn_row_region_guard();

CREATE TRIGGER trg_inv_esg_observation__revision BEFORE UPDATE ON ge.inv_esg_observation FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_inv_esg_observation__residency BEFORE INSERT OR UPDATE ON ge.inv_esg_observation FOR EACH ROW EXECUTE FUNCTION ge.fn_row_region_guard();

CREATE TRIGGER trg_inv_event__revision BEFORE UPDATE ON ge.inv_event FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_inv_event__residency BEFORE INSERT OR UPDATE ON ge.inv_event FOR EACH ROW EXECUTE FUNCTION ge.fn_row_region_guard();

CREATE TRIGGER trg_inv_evidence__revision BEFORE UPDATE ON ge.inv_evidence FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_inv_evidence__residency BEFORE INSERT OR UPDATE ON ge.inv_evidence FOR EACH ROW EXECUTE FUNCTION ge.fn_row_region_guard();

CREATE TRIGGER trg_inv_external_agent_mandate__revision BEFORE UPDATE ON ge.inv_external_agent_mandate FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_inv_external_agent_mandate__residency BEFORE INSERT OR UPDATE ON ge.inv_external_agent_mandate FOR EACH ROW EXECUTE FUNCTION ge.fn_row_region_guard();

CREATE TRIGGER trg_inv_feedback__revision BEFORE UPDATE ON ge.inv_feedback FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_inv_feedback__residency BEFORE INSERT OR UPDATE ON ge.inv_feedback FOR EACH ROW EXECUTE FUNCTION ge.fn_row_region_guard();

CREATE TRIGGER trg_inv_filing_task__revision BEFORE UPDATE ON ge.inv_filing_task FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_inv_filing_task__residency BEFORE INSERT OR UPDATE ON ge.inv_filing_task FOR EACH ROW EXECUTE FUNCTION ge.fn_row_region_guard();

CREATE TRIGGER trg_inv_fit_score__revision BEFORE UPDATE ON ge.inv_fit_score FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_inv_fit_score__residency BEFORE INSERT OR UPDATE ON ge.inv_fit_score FOR EACH ROW EXECUTE FUNCTION ge.fn_row_region_guard();

CREATE TRIGGER trg_inv_funding_route__revision BEFORE UPDATE ON ge.inv_funding_route FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_inv_funding_route__residency BEFORE INSERT OR UPDATE ON ge.inv_funding_route FOR EACH ROW EXECUTE FUNCTION ge.fn_row_region_guard();

CREATE TRIGGER trg_inv_fx_rate__immutable BEFORE UPDATE OR DELETE ON ge.inv_fx_rate FOR EACH ROW EXECUTE FUNCTION ge.fn_forbid_mutation();

CREATE TRIGGER trg_inv_fx_rate__residency BEFORE INSERT OR UPDATE ON ge.inv_fx_rate FOR EACH ROW EXECUTE FUNCTION ge.fn_row_region_guard();

CREATE TRIGGER trg_inv_grant_award__revision BEFORE UPDATE ON ge.inv_grant_award FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_inv_grant_award__residency BEFORE INSERT OR UPDATE ON ge.inv_grant_award FOR EACH ROW EXECUTE FUNCTION ge.fn_row_region_guard();

CREATE TRIGGER trg_inv_grant_budget_line__revision BEFORE UPDATE ON ge.inv_grant_budget_line FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_inv_grant_budget_line__residency BEFORE INSERT OR UPDATE ON ge.inv_grant_budget_line FOR EACH ROW EXECUTE FUNCTION ge.fn_row_region_guard();

CREATE TRIGGER trg_inv_grant_case__revision BEFORE UPDATE ON ge.inv_grant_case FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_inv_grant_case__residency BEFORE INSERT OR UPDATE ON ge.inv_grant_case FOR EACH ROW EXECUTE FUNCTION ge.fn_row_region_guard();

CREATE TRIGGER trg_inv_grant_criterion__revision BEFORE UPDATE ON ge.inv_grant_criterion FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_inv_grant_criterion__residency BEFORE INSERT OR UPDATE ON ge.inv_grant_criterion FOR EACH ROW EXECUTE FUNCTION ge.fn_row_region_guard();

CREATE TRIGGER trg_inv_guarantee_evidence__revision BEFORE UPDATE ON ge.inv_guarantee_evidence FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_inv_guarantee_evidence__residency BEFORE INSERT OR UPDATE ON ge.inv_guarantee_evidence FOR EACH ROW EXECUTE FUNCTION ge.fn_row_region_guard();

CREATE TRIGGER trg_inv_guard_finding__revision BEFORE UPDATE ON ge.inv_guard_finding FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_inv_guard_finding__residency BEFORE INSERT OR UPDATE ON ge.inv_guard_finding FOR EACH ROW EXECUTE FUNCTION ge.fn_row_region_guard();

CREATE TRIGGER trg_inv_holding__immutable BEFORE UPDATE OR DELETE ON ge.inv_holding FOR EACH ROW EXECUTE FUNCTION ge.fn_forbid_mutation();

CREATE TRIGGER trg_inv_holding__residency BEFORE INSERT OR UPDATE ON ge.inv_holding FOR EACH ROW EXECUTE FUNCTION ge.fn_row_region_guard();

CREATE TRIGGER trg_inv_inbound_event__revision BEFORE UPDATE ON ge.inv_inbound_event FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_inv_inbound_event__residency BEFORE INSERT OR UPDATE ON ge.inv_inbound_event FOR EACH ROW EXECUTE FUNCTION ge.fn_row_region_guard();

CREATE TRIGGER trg_inv_instrument__immutable BEFORE UPDATE OR DELETE ON ge.inv_instrument FOR EACH ROW EXECUTE FUNCTION ge.fn_forbid_mutation();

CREATE TRIGGER trg_inv_instrument__residency BEFORE INSERT OR UPDATE ON ge.inv_instrument FOR EACH ROW EXECUTE FUNCTION ge.fn_row_region_guard();

CREATE TRIGGER trg_inv_instrument_term__immutable BEFORE UPDATE OR DELETE ON ge.inv_instrument_term FOR EACH ROW EXECUTE FUNCTION ge.fn_forbid_mutation();

CREATE TRIGGER trg_inv_instrument_term__residency BEFORE INSERT OR UPDATE ON ge.inv_instrument_term FOR EACH ROW EXECUTE FUNCTION ge.fn_row_region_guard();

CREATE TRIGGER trg_inv_integration_connection__revision BEFORE UPDATE ON ge.inv_integration_connection FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_inv_integration_connection__residency BEFORE INSERT OR UPDATE ON ge.inv_integration_connection FOR EACH ROW EXECUTE FUNCTION ge.fn_row_region_guard();

CREATE TRIGGER trg_inv_investor__revision BEFORE UPDATE ON ge.inv_investor FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_inv_investor__residency BEFORE INSERT OR UPDATE ON ge.inv_investor FOR EACH ROW EXECUTE FUNCTION ge.fn_row_region_guard();

CREATE TRIGGER trg_inv_investor_alias__revision BEFORE UPDATE ON ge.inv_investor_alias FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_inv_investor_alias__residency BEFORE INSERT OR UPDATE ON ge.inv_investor_alias FOR EACH ROW EXECUTE FUNCTION ge.fn_row_region_guard();

CREATE TRIGGER trg_inv_investor_classification__revision BEFORE UPDATE ON ge.inv_investor_classification FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_inv_investor_classification__residency BEFORE INSERT OR UPDATE ON ge.inv_investor_classification FOR EACH ROW EXECUTE FUNCTION ge.fn_row_region_guard();

CREATE TRIGGER trg_inv_jurisdiction_policy__revision BEFORE UPDATE ON ge.inv_jurisdiction_policy FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_inv_jurisdiction_policy__residency BEFORE INSERT OR UPDATE ON ge.inv_jurisdiction_policy FOR EACH ROW EXECUTE FUNCTION ge.fn_row_region_guard();

CREATE TRIGGER trg_inv_kyc_case__revision BEFORE UPDATE ON ge.inv_kyc_case FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_inv_kyc_case__residency BEFORE INSERT OR UPDATE ON ge.inv_kyc_case FOR EACH ROW EXECUTE FUNCTION ge.fn_row_region_guard();

CREATE TRIGGER trg_inv_kyc_provider_result__immutable BEFORE UPDATE OR DELETE ON ge.inv_kyc_provider_result FOR EACH ROW EXECUTE FUNCTION ge.fn_forbid_mutation();

CREATE TRIGGER trg_inv_kyc_provider_result__residency BEFORE INSERT OR UPDATE ON ge.inv_kyc_provider_result FOR EACH ROW EXECUTE FUNCTION ge.fn_row_region_guard();

CREATE TRIGGER trg_inv_legal_check__revision BEFORE UPDATE ON ge.inv_legal_check FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_inv_legal_check__residency BEFORE INSERT OR UPDATE ON ge.inv_legal_check FOR EACH ROW EXECUTE FUNCTION ge.fn_row_region_guard();

CREATE TRIGGER trg_inv_locale_template__revision BEFORE UPDATE ON ge.inv_locale_template FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_inv_locale_template__residency BEFORE INSERT OR UPDATE ON ge.inv_locale_template FOR EACH ROW EXECUTE FUNCTION ge.fn_row_region_guard();

CREATE TRIGGER trg_inv_mandate__revision BEFORE UPDATE ON ge.inv_mandate FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_inv_mandate__residency BEFORE INSERT OR UPDATE ON ge.inv_mandate FOR EACH ROW EXECUTE FUNCTION ge.fn_row_region_guard();

CREATE TRIGGER trg_inv_match_candidate__revision BEFORE UPDATE ON ge.inv_match_candidate FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_inv_match_candidate__residency BEFORE INSERT OR UPDATE ON ge.inv_match_candidate FOR EACH ROW EXECUTE FUNCTION ge.fn_row_region_guard();

CREATE TRIGGER trg_inv_meeting__revision BEFORE UPDATE ON ge.inv_meeting FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_inv_meeting__residency BEFORE INSERT OR UPDATE ON ge.inv_meeting FOR EACH ROW EXECUTE FUNCTION ge.fn_row_region_guard();

CREATE TRIGGER trg_inv_message__revision BEFORE UPDATE ON ge.inv_message FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_inv_message__residency BEFORE INSERT OR UPDATE ON ge.inv_message FOR EACH ROW EXECUTE FUNCTION ge.fn_row_region_guard();

CREATE TRIGGER trg_inv_nda__revision BEFORE UPDATE ON ge.inv_nda FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_inv_nda__residency BEFORE INSERT OR UPDATE ON ge.inv_nda FOR EACH ROW EXECUTE FUNCTION ge.fn_row_region_guard();

CREATE TRIGGER trg_inv_objection__revision BEFORE UPDATE ON ge.inv_objection FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_inv_objection__residency BEFORE INSERT OR UPDATE ON ge.inv_objection FOR EACH ROW EXECUTE FUNCTION ge.fn_row_region_guard();

CREATE TRIGGER trg_inv_objection_rule__revision BEFORE UPDATE ON ge.inv_objection_rule FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_inv_objection_rule__residency BEFORE INSERT OR UPDATE ON ge.inv_objection_rule FOR EACH ROW EXECUTE FUNCTION ge.fn_row_region_guard();

CREATE TRIGGER trg_inv_obligation__revision BEFORE UPDATE ON ge.inv_obligation FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_inv_obligation__residency BEFORE INSERT OR UPDATE ON ge.inv_obligation FOR EACH ROW EXECUTE FUNCTION ge.fn_row_region_guard();

CREATE TRIGGER trg_inv_offer__revision BEFORE UPDATE ON ge.inv_offer FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_inv_offer__residency BEFORE INSERT OR UPDATE ON ge.inv_offer FOR EACH ROW EXECUTE FUNCTION ge.fn_row_region_guard();

CREATE TRIGGER trg_inv_offer_batch__revision BEFORE UPDATE ON ge.inv_offer_batch FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_inv_offer_batch__residency BEFORE INSERT OR UPDATE ON ge.inv_offer_batch FOR EACH ROW EXECUTE FUNCTION ge.fn_row_region_guard();

CREATE TRIGGER trg_inv_offer_counter__revision BEFORE UPDATE ON ge.inv_offer_counter FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_inv_offer_counter__residency BEFORE INSERT OR UPDATE ON ge.inv_offer_counter FOR EACH ROW EXECUTE FUNCTION ge.fn_row_region_guard();

CREATE TRIGGER trg_inv_offer_ledger__immutable BEFORE UPDATE OR DELETE ON ge.inv_offer_ledger FOR EACH ROW EXECUTE FUNCTION ge.fn_forbid_mutation();

CREATE TRIGGER trg_inv_offer_ledger__residency BEFORE INSERT OR UPDATE ON ge.inv_offer_ledger FOR EACH ROW EXECUTE FUNCTION ge.fn_row_region_guard();

CREATE TRIGGER trg_inv_offer_recipient__revision BEFORE UPDATE ON ge.inv_offer_recipient FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_inv_offer_recipient__residency BEFORE INSERT OR UPDATE ON ge.inv_offer_recipient FOR EACH ROW EXECUTE FUNCTION ge.fn_row_region_guard();

CREATE TRIGGER trg_inv_offeree__revision BEFORE UPDATE ON ge.inv_offeree FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_inv_offeree__residency BEFORE INSERT OR UPDATE ON ge.inv_offeree FOR EACH ROW EXECUTE FUNCTION ge.fn_row_region_guard();

CREATE TRIGGER trg_inv_offering__revision BEFORE UPDATE ON ge.inv_offering FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_inv_offering__residency BEFORE INSERT OR UPDATE ON ge.inv_offering FOR EACH ROW EXECUTE FUNCTION ge.fn_row_region_guard();

CREATE TRIGGER trg_inv_opportunity__revision BEFORE UPDATE ON ge.inv_opportunity FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_inv_opportunity__residency BEFORE INSERT OR UPDATE ON ge.inv_opportunity FOR EACH ROW EXECUTE FUNCTION ge.fn_row_region_guard();

CREATE TRIGGER trg_inv_option_grant__immutable BEFORE UPDATE OR DELETE ON ge.inv_option_grant FOR EACH ROW EXECUTE FUNCTION ge.fn_forbid_mutation();

CREATE TRIGGER trg_inv_option_grant__residency BEFORE INSERT OR UPDATE ON ge.inv_option_grant FOR EACH ROW EXECUTE FUNCTION ge.fn_row_region_guard();

CREATE TRIGGER trg_inv_outbox__revision BEFORE UPDATE ON ge.inv_outbox FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_inv_outbox__residency BEFORE INSERT OR UPDATE ON ge.inv_outbox FOR EACH ROW EXECUTE FUNCTION ge.fn_row_region_guard();

CREATE TRIGGER trg_inv_outreach_reservation__revision BEFORE UPDATE ON ge.inv_outreach_reservation FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_inv_outreach_reservation__residency BEFORE INSERT OR UPDATE ON ge.inv_outreach_reservation FOR EACH ROW EXECUTE FUNCTION ge.fn_row_region_guard();

CREATE TRIGGER trg_inv_payment_instruction__revision BEFORE UPDATE ON ge.inv_payment_instruction FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_inv_payment_instruction__residency BEFORE INSERT OR UPDATE ON ge.inv_payment_instruction FOR EACH ROW EXECUTE FUNCTION ge.fn_row_region_guard();

CREATE TRIGGER trg_inv_permission__revision BEFORE UPDATE ON ge.inv_permission FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_inv_permission__residency BEFORE INSERT OR UPDATE ON ge.inv_permission FOR EACH ROW EXECUTE FUNCTION ge.fn_row_region_guard();

CREATE TRIGGER trg_inv_promotion_review__revision BEFORE UPDATE ON ge.inv_promotion_review FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_inv_promotion_review__residency BEFORE INSERT OR UPDATE ON ge.inv_promotion_review FOR EACH ROW EXECUTE FUNCTION ge.fn_row_region_guard();

CREATE TRIGGER trg_inv_readiness_score__revision BEFORE UPDATE ON ge.inv_readiness_score FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_inv_readiness_score__residency BEFORE INSERT OR UPDATE ON ge.inv_readiness_score FOR EACH ROW EXECUTE FUNCTION ge.fn_row_region_guard();

CREATE TRIGGER trg_inv_readiness_snapshot__revision BEFORE UPDATE ON ge.inv_readiness_snapshot FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_inv_readiness_snapshot__residency BEFORE INSERT OR UPDATE ON ge.inv_readiness_snapshot FOR EACH ROW EXECUTE FUNCTION ge.fn_row_region_guard();

CREATE TRIGGER trg_inv_receipt__immutable BEFORE UPDATE OR DELETE ON ge.inv_receipt FOR EACH ROW EXECUTE FUNCTION ge.fn_forbid_mutation();

CREATE TRIGGER trg_inv_receipt__residency BEFORE INSERT OR UPDATE ON ge.inv_receipt FOR EACH ROW EXECUTE FUNCTION ge.fn_row_region_guard();

CREATE TRIGGER trg_inv_receipt_allocation__immutable BEFORE UPDATE OR DELETE ON ge.inv_receipt_allocation FOR EACH ROW EXECUTE FUNCTION ge.fn_forbid_mutation();

CREATE TRIGGER trg_inv_receipt_allocation__residency BEFORE INSERT OR UPDATE ON ge.inv_receipt_allocation FOR EACH ROW EXECUTE FUNCTION ge.fn_row_region_guard();

CREATE TRIGGER trg_inv_referral__revision BEFORE UPDATE ON ge.inv_referral FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_inv_referral__residency BEFORE INSERT OR UPDATE ON ge.inv_referral FOR EACH ROW EXECUTE FUNCTION ge.fn_row_region_guard();

CREATE TRIGGER trg_inv_refund__immutable BEFORE UPDATE OR DELETE ON ge.inv_refund FOR EACH ROW EXECUTE FUNCTION ge.fn_forbid_mutation();

CREATE TRIGGER trg_inv_refund__residency BEFORE INSERT OR UPDATE ON ge.inv_refund FOR EACH ROW EXECUTE FUNCTION ge.fn_row_region_guard();

CREATE TRIGGER trg_inv_regulatory_deadline__revision BEFORE UPDATE ON ge.inv_regulatory_deadline FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_inv_regulatory_deadline__residency BEFORE INSERT OR UPDATE ON ge.inv_regulatory_deadline FOR EACH ROW EXECUTE FUNCTION ge.fn_row_region_guard();

CREATE TRIGGER trg_inv_relationship__revision BEFORE UPDATE ON ge.inv_relationship FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_inv_relationship__residency BEFORE INSERT OR UPDATE ON ge.inv_relationship FOR EACH ROW EXECUTE FUNCTION ge.fn_row_region_guard();

CREATE TRIGGER trg_inv_relationship_provenance__revision BEFORE UPDATE ON ge.inv_relationship_provenance FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_inv_relationship_provenance__residency BEFORE INSERT OR UPDATE ON ge.inv_relationship_provenance FOR EACH ROW EXECUTE FUNCTION ge.fn_row_region_guard();

CREATE TRIGGER trg_inv_repayment_schedule__revision BEFORE UPDATE ON ge.inv_repayment_schedule FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_inv_repayment_schedule__residency BEFORE INSERT OR UPDATE ON ge.inv_repayment_schedule FOR EACH ROW EXECUTE FUNCTION ge.fn_row_region_guard();

CREATE TRIGGER trg_inv_resolution__revision BEFORE UPDATE ON ge.inv_resolution FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_inv_resolution__residency BEFORE INSERT OR UPDATE ON ge.inv_resolution FOR EACH ROW EXECUTE FUNCTION ge.fn_row_region_guard();

CREATE TRIGGER trg_inv_room__revision BEFORE UPDATE ON ge.inv_room FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_inv_room__residency BEFORE INSERT OR UPDATE ON ge.inv_room FOR EACH ROW EXECUTE FUNCTION ge.fn_row_region_guard();

CREATE TRIGGER trg_inv_room_item__revision BEFORE UPDATE ON ge.inv_room_item FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_inv_room_item__residency BEFORE INSERT OR UPDATE ON ge.inv_room_item FOR EACH ROW EXECUTE FUNCTION ge.fn_row_region_guard();

CREATE TRIGGER trg_inv_round__revision BEFORE UPDATE ON ge.inv_round FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_inv_round__residency BEFORE INSERT OR UPDATE ON ge.inv_round FOR EACH ROW EXECUTE FUNCTION ge.fn_row_region_guard();

CREATE TRIGGER trg_inv_rulepack_activation__revision BEFORE UPDATE ON ge.inv_rulepack_activation FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_inv_rulepack_activation__residency BEFORE INSERT OR UPDATE ON ge.inv_rulepack_activation FOR EACH ROW EXECUTE FUNCTION ge.fn_row_region_guard();

CREATE TRIGGER trg_inv_runway_scenario__revision BEFORE UPDATE ON ge.inv_runway_scenario FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_inv_runway_scenario__residency BEFORE INSERT OR UPDATE ON ge.inv_runway_scenario FOR EACH ROW EXECUTE FUNCTION ge.fn_row_region_guard();

CREATE TRIGGER trg_inv_scenario__revision BEFORE UPDATE ON ge.inv_scenario FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_inv_scenario__residency BEFORE INSERT OR UPDATE ON ge.inv_scenario FOR EACH ROW EXECUTE FUNCTION ge.fn_row_region_guard();

CREATE TRIGGER trg_inv_screening_hit__revision BEFORE UPDATE ON ge.inv_screening_hit FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_inv_screening_hit__residency BEFORE INSERT OR UPDATE ON ge.inv_screening_hit FOR EACH ROW EXECUTE FUNCTION ge.fn_row_region_guard();

CREATE TRIGGER trg_inv_search_plan__revision BEFORE UPDATE ON ge.inv_search_plan FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_inv_search_plan__residency BEFORE INSERT OR UPDATE ON ge.inv_search_plan FOR EACH ROW EXECUTE FUNCTION ge.fn_row_region_guard();

CREATE TRIGGER trg_inv_search_run__revision BEFORE UPDATE ON ge.inv_search_run FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_inv_search_run__residency BEFORE INSERT OR UPDATE ON ge.inv_search_run FOR EACH ROW EXECUTE FUNCTION ge.fn_row_region_guard();

CREATE TRIGGER trg_inv_sequence__revision BEFORE UPDATE ON ge.inv_sequence FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_inv_sequence__residency BEFORE INSERT OR UPDATE ON ge.inv_sequence FOR EACH ROW EXECUTE FUNCTION ge.fn_row_region_guard();

CREATE TRIGGER trg_inv_shareholder__immutable BEFORE UPDATE OR DELETE ON ge.inv_shareholder FOR EACH ROW EXECUTE FUNCTION ge.fn_forbid_mutation();

CREATE TRIGGER trg_inv_shareholder__residency BEFORE INSERT OR UPDATE ON ge.inv_shareholder FOR EACH ROW EXECUTE FUNCTION ge.fn_row_region_guard();

CREATE TRIGGER trg_inv_source__revision BEFORE UPDATE ON ge.inv_source FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_inv_source__residency BEFORE INSERT OR UPDATE ON ge.inv_source FOR EACH ROW EXECUTE FUNCTION ge.fn_row_region_guard();

CREATE TRIGGER trg_inv_source_policy__revision BEFORE UPDATE ON ge.inv_source_policy FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_inv_source_policy__residency BEFORE INSERT OR UPDATE ON ge.inv_source_policy FOR EACH ROW EXECUTE FUNCTION ge.fn_row_region_guard();

CREATE TRIGGER trg_inv_stage_event__revision BEFORE UPDATE ON ge.inv_stage_event FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_inv_stage_event__residency BEFORE INSERT OR UPDATE ON ge.inv_stage_event FOR EACH ROW EXECUTE FUNCTION ge.fn_row_region_guard();

CREATE TRIGGER trg_inv_suppression__revision BEFORE UPDATE ON ge.inv_suppression FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_inv_suppression__residency BEFORE INSERT OR UPDATE ON ge.inv_suppression FOR EACH ROW EXECUTE FUNCTION ge.fn_row_region_guard();

CREATE TRIGGER trg_inv_task__revision BEFORE UPDATE ON ge.inv_task FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_inv_task__residency BEFORE INSERT OR UPDATE ON ge.inv_task FOR EACH ROW EXECUTE FUNCTION ge.fn_row_region_guard();

CREATE TRIGGER trg_inv_term_version__revision BEFORE UPDATE ON ge.inv_term_version FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_inv_term_version__residency BEFORE INSERT OR UPDATE ON ge.inv_term_version FOR EACH ROW EXECUTE FUNCTION ge.fn_row_region_guard();

CREATE TRIGGER trg_inv_thread__revision BEFORE UPDATE ON ge.inv_thread FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_inv_thread__residency BEFORE INSERT OR UPDATE ON ge.inv_thread FOR EACH ROW EXECUTE FUNCTION ge.fn_row_region_guard();

CREATE TRIGGER trg_inv_update__revision BEFORE UPDATE ON ge.inv_update FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_inv_update__residency BEFORE INSERT OR UPDATE ON ge.inv_update FOR EACH ROW EXECUTE FUNCTION ge.fn_row_region_guard();

CREATE TRIGGER trg_inv_verification_case__revision BEFORE UPDATE ON ge.inv_verification_case FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_inv_verification_case__residency BEFORE INSERT OR UPDATE ON ge.inv_verification_case FOR EACH ROW EXECUTE FUNCTION ge.fn_row_region_guard();

CREATE TRIGGER trg_inv_vote__immutable BEFORE UPDATE OR DELETE ON ge.inv_vote FOR EACH ROW EXECUTE FUNCTION ge.fn_forbid_mutation();

CREATE TRIGGER trg_inv_vote__residency BEFORE INSERT OR UPDATE ON ge.inv_vote FOR EACH ROW EXECUTE FUNCTION ge.fn_row_region_guard();

CREATE TRIGGER trg_inv_webhook_endpoint__revision BEFORE UPDATE ON ge.inv_webhook_endpoint FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_inv_webhook_endpoint__residency BEFORE INSERT OR UPDATE ON ge.inv_webhook_endpoint FOR EACH ROW EXECUTE FUNCTION ge.fn_row_region_guard();

CREATE TRIGGER trg_inv_workflow_run__revision BEFORE UPDATE ON ge.inv_workflow_run FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_inv_workflow_run__residency BEFORE INSERT OR UPDATE ON ge.inv_workflow_run FOR EACH ROW EXECUTE FUNCTION ge.fn_row_region_guard();

CREATE TRIGGER trg_kill_switch__revision BEFORE UPDATE ON ge.kill_switch FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_kill_switch__residency BEFORE INSERT OR UPDATE ON ge.kill_switch FOR EACH ROW EXECUTE FUNCTION ge.fn_row_region_guard();

CREATE TRIGGER trg_kill_switch_event__revision BEFORE UPDATE ON ge.kill_switch_event FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_kill_switch_event__residency BEFORE INSERT OR UPDATE ON ge.kill_switch_event FOR EACH ROW EXECUTE FUNCTION ge.fn_row_region_guard();

CREATE TRIGGER trg_lcy_account_metric__immutable BEFORE UPDATE OR DELETE ON ge.lcy_account_metric FOR EACH ROW EXECUTE FUNCTION ge.fn_forbid_mutation();

CREATE TRIGGER trg_lcy_customer_subscription__revision BEFORE UPDATE ON ge.lcy_customer_subscription FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_lcy_deployment__revision BEFORE UPDATE ON ge.lcy_deployment FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_lcy_deployment__domain_registry BEFORE INSERT OR UPDATE ON ge.lcy_deployment FOR EACH ROW EXECUTE FUNCTION ge.fn_validate_typed_domain_row();

CREATE TRIGGER trg_lcy_feedback__immutable BEFORE UPDATE OR DELETE ON ge.lcy_feedback FOR EACH ROW EXECUTE FUNCTION ge.fn_forbid_mutation();

CREATE TRIGGER trg_lcy_handoff__immutable BEFORE UPDATE OR DELETE ON ge.lcy_handoff FOR EACH ROW EXECUTE FUNCTION ge.fn_forbid_mutation();

CREATE TRIGGER trg_lcy_integration_deal__revision BEFORE UPDATE ON ge.lcy_integration_deal FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_lcy_integration_deal__domain_registry BEFORE INSERT OR UPDATE ON ge.lcy_integration_deal FOR EACH ROW EXECUTE FUNCTION ge.fn_validate_typed_domain_row();

CREATE TRIGGER trg_lcy_onboarding__revision BEFORE UPDATE ON ge.lcy_onboarding FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_lcy_onboarding__domain_registry BEFORE INSERT OR UPDATE ON ge.lcy_onboarding FOR EACH ROW EXECUTE FUNCTION ge.fn_validate_typed_domain_row();

CREATE TRIGGER trg_lcy_onboarding_task__revision BEFORE UPDATE ON ge.lcy_onboarding_task FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_lcy_outcome__immutable BEFORE UPDATE OR DELETE ON ge.lcy_outcome FOR EACH ROW EXECUTE FUNCTION ge.fn_forbid_mutation();

CREATE TRIGGER trg_lcy_partner__revision BEFORE UPDATE ON ge.lcy_partner FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_lcy_partner__domain_registry BEFORE INSERT OR UPDATE ON ge.lcy_partner FOR EACH ROW EXECUTE FUNCTION ge.fn_validate_typed_domain_row();

CREATE TRIGGER trg_lcy_pilot__revision BEFORE UPDATE ON ge.lcy_pilot FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_lcy_pilot__domain_registry BEFORE INSERT OR UPDATE ON ge.lcy_pilot FOR EACH ROW EXECUTE FUNCTION ge.fn_validate_typed_domain_row();

CREATE TRIGGER trg_lcy_renewal__revision BEFORE UPDATE ON ge.lcy_renewal FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_lcy_renewal__domain_registry BEFORE INSERT OR UPDATE ON ge.lcy_renewal FOR EACH ROW EXECUTE FUNCTION ge.fn_validate_typed_domain_row();

CREATE TRIGGER trg_lcy_task__revision BEFORE UPDATE ON ge.lcy_task FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_lcy_task__domain_registry BEFORE INSERT OR UPDATE ON ge.lcy_task FOR EACH ROW EXECUTE FUNCTION ge.fn_validate_typed_domain_row();

CREATE TRIGGER trg_ledger_entry__revision BEFORE UPDATE ON ge.ledger_entry FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_ledger_entry__residency BEFORE INSERT OR UPDATE ON ge.ledger_entry FOR EACH ROW EXECUTE FUNCTION ge.fn_row_region_guard();

CREATE TRIGGER trg_mandate__revision BEFORE UPDATE ON ge.mandate FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_mandate__residency BEFORE INSERT OR UPDATE ON ge.mandate FOR EACH ROW EXECUTE FUNCTION ge.fn_row_region_guard();

CREATE TRIGGER trg_mandate_approval__revision BEFORE UPDATE ON ge.mandate_approval FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_mandate_approval__residency BEFORE INSERT OR UPDATE ON ge.mandate_approval FOR EACH ROW EXECUTE FUNCTION ge.fn_row_region_guard();

CREATE TRIGGER trg_mandate_consumption__revision BEFORE UPDATE ON ge.mandate_consumption FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_mandate_consumption__residency BEFORE INSERT OR UPDATE ON ge.mandate_consumption FOR EACH ROW EXECUTE FUNCTION ge.fn_row_region_guard();

CREATE TRIGGER trg_mandate_counter__revision BEFORE UPDATE ON ge.mandate_counter FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_mandate_counter__residency BEFORE INSERT OR UPDATE ON ge.mandate_counter FOR EACH ROW EXECUTE FUNCTION ge.fn_row_region_guard();

CREATE TRIGGER trg_mandate_decision__revision BEFORE UPDATE ON ge.mandate_decision FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_mandate_decision__residency BEFORE INSERT OR UPDATE ON ge.mandate_decision FOR EACH ROW EXECUTE FUNCTION ge.fn_row_region_guard();

CREATE TRIGGER trg_mandate_limit__revision BEFORE UPDATE ON ge.mandate_limit FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_mandate_limit__residency BEFORE INSERT OR UPDATE ON ge.mandate_limit FOR EACH ROW EXECUTE FUNCTION ge.fn_row_region_guard();

CREATE TRIGGER trg_mandate_restriction__revision BEFORE UPDATE ON ge.mandate_restriction FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_mandate_restriction__residency BEFORE INSERT OR UPDATE ON ge.mandate_restriction FOR EACH ROW EXECUTE FUNCTION ge.fn_row_region_guard();

CREATE TRIGGER trg_mandate_scope_item__revision BEFORE UPDATE ON ge.mandate_scope_item FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_mandate_scope_item__residency BEFORE INSERT OR UPDATE ON ge.mandate_scope_item FOR EACH ROW EXECUTE FUNCTION ge.fn_row_region_guard();

CREATE TRIGGER trg_mandate_version__revision BEFORE UPDATE ON ge.mandate_version FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_mandate_version__residency BEFORE INSERT OR UPDATE ON ge.mandate_version FOR EACH ROW EXECUTE FUNCTION ge.fn_row_region_guard();

CREATE TRIGGER trg_mandate_window__revision BEFORE UPDATE ON ge.mandate_window FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_mandate_window__residency BEFORE INSERT OR UPDATE ON ge.mandate_window FOR EACH ROW EXECUTE FUNCTION ge.fn_row_region_guard();

CREATE TRIGGER trg_market__residency BEFORE INSERT OR UPDATE ON ge.market FOR EACH ROW EXECUTE FUNCTION ge.fn_row_region_guard();

CREATE TRIGGER trg_mkt_ad_campaign__revision BEFORE UPDATE ON ge.mkt_ad_campaign FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_mkt_ad_campaign__domain_registry BEFORE INSERT OR UPDATE ON ge.mkt_ad_campaign FOR EACH ROW EXECUTE FUNCTION ge.fn_validate_typed_domain_row();

CREATE TRIGGER trg_mkt_attendance__immutable BEFORE UPDATE OR DELETE ON ge.mkt_attendance FOR EACH ROW EXECUTE FUNCTION ge.fn_forbid_mutation();

CREATE TRIGGER trg_mkt_attendance__domain_registry BEFORE INSERT OR UPDATE ON ge.mkt_attendance FOR EACH ROW EXECUTE FUNCTION ge.fn_validate_typed_domain_row();

CREATE TRIGGER trg_mkt_attribution_event__immutable BEFORE UPDATE OR DELETE ON ge.mkt_attribution_event FOR EACH ROW EXECUTE FUNCTION ge.fn_forbid_mutation();

CREATE TRIGGER trg_mkt_attribution_event__domain_registry BEFORE INSERT OR UPDATE ON ge.mkt_attribution_event FOR EACH ROW EXECUTE FUNCTION ge.fn_validate_typed_domain_row();

CREATE TRIGGER trg_mkt_audience__revision BEFORE UPDATE ON ge.mkt_audience FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_mkt_audience__freeze BEFORE UPDATE ON ge.mkt_audience FOR EACH ROW EXECUTE FUNCTION ge.fn_freeze_versioned();

CREATE TRIGGER trg_mkt_audience__domain_registry BEFORE INSERT OR UPDATE ON ge.mkt_audience FOR EACH ROW EXECUTE FUNCTION ge.fn_validate_typed_domain_row();

CREATE TRIGGER trg_mkt_audience_member__revision BEFORE UPDATE ON ge.mkt_audience_member FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_mkt_campaign__revision BEFORE UPDATE ON ge.mkt_campaign FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_mkt_campaign__domain_registry BEFORE INSERT OR UPDATE ON ge.mkt_campaign FOR EACH ROW EXECUTE FUNCTION ge.fn_validate_typed_domain_row();

CREATE TRIGGER trg_mkt_campaign_version__revision BEFORE UPDATE ON ge.mkt_campaign_version FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_mkt_campaign_version__freeze BEFORE UPDATE ON ge.mkt_campaign_version FOR EACH ROW EXECUTE FUNCTION ge.fn_freeze_versioned();

CREATE TRIGGER trg_mkt_campaign_version__domain_registry BEFORE INSERT OR UPDATE ON ge.mkt_campaign_version FOR EACH ROW EXECUTE FUNCTION ge.fn_validate_typed_domain_row();

CREATE TRIGGER trg_mkt_content_asset__revision BEFORE UPDATE ON ge.mkt_content_asset FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_mkt_content_asset__domain_registry BEFORE INSERT OR UPDATE ON ge.mkt_content_asset FOR EACH ROW EXECUTE FUNCTION ge.fn_validate_typed_domain_row();

CREATE TRIGGER trg_mkt_content_claim__revision BEFORE UPDATE ON ge.mkt_content_claim FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_mkt_content_version__revision BEFORE UPDATE ON ge.mkt_content_version FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_mkt_content_version__freeze BEFORE UPDATE ON ge.mkt_content_version FOR EACH ROW EXECUTE FUNCTION ge.fn_freeze_versioned();

CREATE TRIGGER trg_mkt_content_version__domain_registry BEFORE INSERT OR UPDATE ON ge.mkt_content_version FOR EACH ROW EXECUTE FUNCTION ge.fn_validate_typed_domain_row();

CREATE TRIGGER trg_mkt_event__revision BEFORE UPDATE ON ge.mkt_event FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_mkt_event__domain_registry BEFORE INSERT OR UPDATE ON ge.mkt_event FOR EACH ROW EXECUTE FUNCTION ge.fn_validate_typed_domain_row();

CREATE TRIGGER trg_mkt_keyword__revision BEFORE UPDATE ON ge.mkt_keyword FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_mkt_keyword__domain_registry BEFORE INSERT OR UPDATE ON ge.mkt_keyword FOR EACH ROW EXECUTE FUNCTION ge.fn_validate_typed_domain_row();

CREATE TRIGGER trg_mkt_landing_page__revision BEFORE UPDATE ON ge.mkt_landing_page FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_mkt_landing_page__domain_registry BEFORE INSERT OR UPDATE ON ge.mkt_landing_page FOR EACH ROW EXECUTE FUNCTION ge.fn_validate_typed_domain_row();

CREATE TRIGGER trg_mkt_page_metric__immutable BEFORE UPDATE OR DELETE ON ge.mkt_page_metric FOR EACH ROW EXECUTE FUNCTION ge.fn_forbid_mutation();

CREATE TRIGGER trg_mkt_page_metric__domain_registry BEFORE INSERT OR UPDATE ON ge.mkt_page_metric FOR EACH ROW EXECUTE FUNCTION ge.fn_validate_typed_domain_row();

CREATE TRIGGER trg_mkt_preview_grant__revision BEFORE UPDATE ON ge.mkt_preview_grant FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_mkt_publication__revision BEFORE UPDATE ON ge.mkt_publication FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_mkt_publication_snapshot__immutable BEFORE UPDATE OR DELETE ON ge.mkt_publication_snapshot FOR EACH ROW EXECUTE FUNCTION ge.fn_forbid_mutation();

CREATE TRIGGER trg_mkt_referral__revision BEFORE UPDATE ON ge.mkt_referral FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_mkt_referral__domain_registry BEFORE INSERT OR UPDATE ON ge.mkt_referral FOR EACH ROW EXECUTE FUNCTION ge.fn_validate_typed_domain_row();

CREATE TRIGGER trg_mkt_registration__revision BEFORE UPDATE ON ge.mkt_registration FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_mkt_registration__domain_registry BEFORE INSERT OR UPDATE ON ge.mkt_registration FOR EACH ROW EXECUTE FUNCTION ge.fn_validate_typed_domain_row();

CREATE TRIGGER trg_mkt_seo_issue__revision BEFORE UPDATE ON ge.mkt_seo_issue FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_mkt_seo_issue__domain_registry BEFORE INSERT OR UPDATE ON ge.mkt_seo_issue FOR EACH ROW EXECUTE FUNCTION ge.fn_validate_typed_domain_row();

CREATE TRIGGER trg_mkt_social_publication__revision BEFORE UPDATE ON ge.mkt_social_publication FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_mkt_social_publication__domain_registry BEFORE INSERT OR UPDATE ON ge.mkt_social_publication FOR EACH ROW EXECUTE FUNCTION ge.fn_validate_typed_domain_row();

CREATE TRIGGER trg_mkt_spend_event__immutable BEFORE UPDATE OR DELETE ON ge.mkt_spend_event FOR EACH ROW EXECUTE FUNCTION ge.fn_forbid_mutation();

CREATE TRIGGER trg_mkt_spend_event__domain_registry BEFORE INSERT OR UPDATE ON ge.mkt_spend_event FOR EACH ROW EXECUTE FUNCTION ge.fn_validate_typed_domain_row();

CREATE TRIGGER trg_negotiation_session__revision BEFORE UPDATE ON ge.negotiation_session FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_negotiation_session__residency BEFORE INSERT OR UPDATE ON ge.negotiation_session FOR EACH ROW EXECUTE FUNCTION ge.fn_row_region_guard();

CREATE TRIGGER trg_negotiation_step__revision BEFORE UPDATE ON ge.negotiation_step FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_negotiation_step__residency BEFORE INSERT OR UPDATE ON ge.negotiation_step FOR EACH ROW EXECUTE FUNCTION ge.fn_row_region_guard();

CREATE TRIGGER trg_oauth_client__residency BEFORE INSERT OR UPDATE ON ge.oauth_client FOR EACH ROW EXECUTE FUNCTION ge.fn_row_region_guard();

CREATE TRIGGER trg_ops_domain_event__immutable BEFORE UPDATE OR DELETE ON ge.ops_domain_event FOR EACH ROW EXECUTE FUNCTION ge.fn_forbid_mutation();

CREATE TRIGGER trg_ops_idempotency_key__revision BEFORE UPDATE ON ge.ops_idempotency_key FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_ops_job_run__revision BEFORE UPDATE ON ge.ops_job_run FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_ops_notification__revision BEFORE UPDATE ON ge.ops_notification FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_ops_notification_preference__revision BEFORE UPDATE ON ge.ops_notification_preference FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_ops_release__revision BEFORE UPDATE ON ge.ops_release FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_ops_test_run__immutable BEFORE UPDATE OR DELETE ON ge.ops_test_run FOR EACH ROW EXECUTE FUNCTION ge.fn_forbid_mutation();

CREATE TRIGGER trg_payment_mandate__revision BEFORE UPDATE ON ge.payment_mandate FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_payment_mandate__residency BEFORE INSERT OR UPDATE ON ge.payment_mandate FOR EACH ROW EXECUTE FUNCTION ge.fn_row_region_guard();

CREATE TRIGGER trg_payment_txn__revision BEFORE UPDATE ON ge.payment_txn FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_payment_txn__residency BEFORE INSERT OR UPDATE ON ge.payment_txn FOR EACH ROW EXECUTE FUNCTION ge.fn_row_region_guard();

CREATE TRIGGER trg_portal_profile__revision BEFORE UPDATE ON ge.portal_profile FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_portal_profile__residency BEFORE INSERT OR UPDATE ON ge.portal_profile FOR EACH ROW EXECUTE FUNCTION ge.fn_row_region_guard();

CREATE TRIGGER trg_recon_break__revision BEFORE UPDATE ON ge.recon_break FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_recon_break__residency BEFORE INSERT OR UPDATE ON ge.recon_break FOR EACH ROW EXECUTE FUNCTION ge.fn_row_region_guard();

CREATE TRIGGER trg_recon_run__revision BEFORE UPDATE ON ge.recon_run FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_recon_run__residency BEFORE INSERT OR UPDATE ON ge.recon_run FOR EACH ROW EXECUTE FUNCTION ge.fn_row_region_guard();

CREATE TRIGGER trg_ref_country__revision BEFORE UPDATE ON ge.ref_country FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_ref_currency__revision BEFORE UPDATE ON ge.ref_currency FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_ref_dataset__revision BEFORE UPDATE ON ge.ref_dataset FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_ref_dataset__freeze BEFORE UPDATE ON ge.ref_dataset FOR EACH ROW EXECUTE FUNCTION ge.fn_freeze_versioned();

CREATE TRIGGER trg_ref_unit__revision BEFORE UPDATE ON ge.ref_unit FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_ref_value__revision BEFORE UPDATE ON ge.ref_value FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_ref_value__freeze BEFORE UPDATE ON ge.ref_value FOR EACH ROW EXECUTE FUNCTION ge.fn_freeze_versioned();

CREATE TRIGGER trg_refund__revision BEFORE UPDATE ON ge.refund FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_refund__residency BEFORE INSERT OR UPDATE ON ge.refund FOR EACH ROW EXECUTE FUNCTION ge.fn_row_region_guard();

CREATE TRIGGER trg_saas_application_draft__revision BEFORE UPDATE ON ge.saas_application_draft FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_saas_credit__immutable BEFORE UPDATE OR DELETE ON ge.saas_credit FOR EACH ROW EXECUTE FUNCTION ge.fn_forbid_mutation();

CREATE TRIGGER trg_saas_entitlement__revision BEFORE UPDATE ON ge.saas_entitlement FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_saas_entitlement__freeze BEFORE UPDATE ON ge.saas_entitlement FOR EACH ROW EXECUTE FUNCTION ge.fn_freeze_versioned();

CREATE TRIGGER trg_saas_import_job__revision BEFORE UPDATE ON ge.saas_import_job FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_saas_plan__revision BEFORE UPDATE ON ge.saas_plan FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_saas_plan_entitlement__revision BEFORE UPDATE ON ge.saas_plan_entitlement FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_saas_plan_version__revision BEFORE UPDATE ON ge.saas_plan_version FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_saas_plan_version__freeze BEFORE UPDATE ON ge.saas_plan_version FOR EACH ROW EXECUTE FUNCTION ge.fn_freeze_versioned();

CREATE TRIGGER trg_saas_service_invoice_line__revision BEFORE UPDATE ON ge.saas_service_invoice_line FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_saas_service_request__revision BEFORE UPDATE ON ge.saas_service_request FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_saas_subscription__revision BEFORE UPDATE ON ge.saas_subscription FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_saas_support_access_grant__revision BEFORE UPDATE ON ge.saas_support_access_grant FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_saas_usage_meter_reading__immutable BEFORE UPDATE OR DELETE ON ge.saas_usage_meter_reading FOR EACH ROW EXECUTE FUNCTION ge.fn_forbid_mutation();

CREATE TRIGGER trg_scim_token__residency BEFORE INSERT OR UPDATE ON ge.scim_token FOR EACH ROW EXECUTE FUNCTION ge.fn_row_region_guard();

CREATE TRIGGER trg_settlement_batch__revision BEFORE UPDATE ON ge.settlement_batch FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_settlement_batch__residency BEFORE INSERT OR UPDATE ON ge.settlement_batch FOR EACH ROW EXECUTE FUNCTION ge.fn_row_region_guard();

CREATE TRIGGER trg_ten_business_template__revision BEFORE UPDATE ON ge.ten_business_template FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_ten_business_template__freeze BEFORE UPDATE ON ge.ten_business_template FOR EACH ROW EXECUTE FUNCTION ge.fn_freeze_versioned();

CREATE TRIGGER trg_ten_capability_profile__revision BEFORE UPDATE ON ge.ten_capability_profile FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_ten_capability_profile__freeze BEFORE UPDATE ON ge.ten_capability_profile FOR EACH ROW EXECUTE FUNCTION ge.fn_freeze_versioned();

CREATE TRIGGER trg_ten_domain__revision BEFORE UPDATE ON ge.ten_domain FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_ten_membership__revision BEFORE UPDATE ON ge.ten_membership FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_ten_membership_grant__revision BEFORE UPDATE ON ge.ten_membership_grant FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_ten_portal_grant__revision BEFORE UPDATE ON ge.ten_portal_grant FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_ten_saved_view__revision BEFORE UPDATE ON ge.ten_saved_view FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_ten_user__revision BEFORE UPDATE ON ge.ten_user FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_voice_access_log__revision BEFORE UPDATE ON ge.voice_access_log FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_voice_access_log__residency BEFORE INSERT OR UPDATE ON ge.voice_access_log FOR EACH ROW EXECUTE FUNCTION ge.fn_row_region_guard();

CREATE TRIGGER trg_voice_campaign__revision BEFORE UPDATE ON ge.voice_campaign FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_voice_campaign__residency BEFORE INSERT OR UPDATE ON ge.voice_campaign FOR EACH ROW EXECUTE FUNCTION ge.fn_row_region_guard();

CREATE TRIGGER trg_voice_campaign_contact__revision BEFORE UPDATE ON ge.voice_campaign_contact FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_voice_campaign_contact__residency BEFORE INSERT OR UPDATE ON ge.voice_campaign_contact FOR EACH ROW EXECUTE FUNCTION ge.fn_row_region_guard();

CREATE TRIGGER trg_voice_consent_evidence__revision BEFORE UPDATE ON ge.voice_consent_evidence FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_voice_consent_evidence__residency BEFORE INSERT OR UPDATE ON ge.voice_consent_evidence FOR EACH ROW EXECUTE FUNCTION ge.fn_row_region_guard();

CREATE TRIGGER trg_voice_handoff__revision BEFORE UPDATE ON ge.voice_handoff FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_voice_handoff__residency BEFORE INSERT OR UPDATE ON ge.voice_handoff FOR EACH ROW EXECUTE FUNCTION ge.fn_row_region_guard();

CREATE TRIGGER trg_voice_leg__revision BEFORE UPDATE ON ge.voice_leg FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_voice_leg__residency BEFORE INSERT OR UPDATE ON ge.voice_leg FOR EACH ROW EXECUTE FUNCTION ge.fn_row_region_guard();

CREATE TRIGGER trg_voice_legal_hold__revision BEFORE UPDATE ON ge.voice_legal_hold FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_voice_legal_hold__residency BEFORE INSERT OR UPDATE ON ge.voice_legal_hold FOR EACH ROW EXECUTE FUNCTION ge.fn_row_region_guard();

CREATE TRIGGER trg_voice_meter_event__revision BEFORE UPDATE ON ge.voice_meter_event FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_voice_meter_event__residency BEFORE INSERT OR UPDATE ON ge.voice_meter_event FOR EACH ROW EXECUTE FUNCTION ge.fn_row_region_guard();

CREATE TRIGGER trg_voice_number__residency BEFORE INSERT OR UPDATE ON ge.voice_number FOR EACH ROW EXECUTE FUNCTION ge.fn_row_region_guard();

CREATE TRIGGER trg_voice_number_pool__revision BEFORE UPDATE ON ge.voice_number_pool FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_voice_number_pool__residency BEFORE INSERT OR UPDATE ON ge.voice_number_pool FOR EACH ROW EXECUTE FUNCTION ge.fn_row_region_guard();

CREATE TRIGGER trg_voice_recording__revision BEFORE UPDATE ON ge.voice_recording FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_voice_recording__residency BEFORE INSERT OR UPDATE ON ge.voice_recording FOR EACH ROW EXECUTE FUNCTION ge.fn_row_region_guard();

CREATE TRIGGER trg_voice_script__revision BEFORE UPDATE ON ge.voice_script FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_voice_script__residency BEFORE INSERT OR UPDATE ON ge.voice_script FOR EACH ROW EXECUTE FUNCTION ge.fn_row_region_guard();

CREATE TRIGGER trg_voice_script_version__revision BEFORE UPDATE ON ge.voice_script_version FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_voice_script_version__residency BEFORE INSERT OR UPDATE ON ge.voice_script_version FOR EACH ROW EXECUTE FUNCTION ge.fn_row_region_guard();

CREATE TRIGGER trg_voice_scrub_result__revision BEFORE UPDATE ON ge.voice_scrub_result FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_voice_scrub_result__residency BEFORE INSERT OR UPDATE ON ge.voice_scrub_result FOR EACH ROW EXECUTE FUNCTION ge.fn_row_region_guard();

CREATE TRIGGER trg_voice_session__revision BEFORE UPDATE ON ge.voice_session FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_voice_session__residency BEFORE INSERT OR UPDATE ON ge.voice_session FOR EACH ROW EXECUTE FUNCTION ge.fn_row_region_guard();

CREATE TRIGGER trg_voice_summary__revision BEFORE UPDATE ON ge.voice_summary FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_voice_summary__residency BEFORE INSERT OR UPDATE ON ge.voice_summary FOR EACH ROW EXECUTE FUNCTION ge.fn_row_region_guard();

CREATE TRIGGER trg_voice_transcript__revision BEFORE UPDATE ON ge.voice_transcript FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_voice_transcript__residency BEFORE INSERT OR UPDATE ON ge.voice_transcript FOR EACH ROW EXECUTE FUNCTION ge.fn_row_region_guard();

CREATE TRIGGER trg_voice_transcript_segment__revision BEFORE UPDATE ON ge.voice_transcript_segment FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_voice_transcript_segment__residency BEFORE INSERT OR UPDATE ON ge.voice_transcript_segment FOR EACH ROW EXECUTE FUNCTION ge.fn_row_region_guard();

CREATE TRIGGER trg_voice_voicemail__revision BEFORE UPDATE ON ge.voice_voicemail FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();

CREATE TRIGGER trg_voice_voicemail__residency BEFORE INSERT OR UPDATE ON ge.voice_voicemail FOR EACH ROW EXECUTE FUNCTION ge.fn_row_region_guard();
