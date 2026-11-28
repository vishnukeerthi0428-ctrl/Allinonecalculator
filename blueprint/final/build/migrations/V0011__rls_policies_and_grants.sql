-- V0011__rls_policies_and_grants
SET search_path = ge, extensions, public;

SELECT set_config('app.zone', coalesce(nullif(current_setting('app.deployment_region', true), ''), 'IN'), false);

SELECT set_config('app.deployment_region', coalesce(nullif(current_setting('app.deployment_region', true), ''), 'IN'), false);

ALTER TABLE ge.access_recert_campaign ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.access_recert_campaign FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.access_recert_campaign TO app_rw, app_worker;

GRANT SELECT ON ge.access_recert_campaign TO app_readonly;

GRANT SELECT, DELETE ON ge.access_recert_campaign TO app_retention;

CREATE POLICY rls_access_recert_campaign__select ON ge.access_recert_campaign FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()));

CREATE POLICY rls_access_recert_campaign__insert ON ge.access_recert_campaign FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()));

CREATE POLICY rls_access_recert_campaign__update ON ge.access_recert_campaign FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()));

CREATE POLICY rls_access_recert_campaign__retention_delete ON ge.access_recert_campaign FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.access_recert_item ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.access_recert_item FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.access_recert_item TO app_rw, app_worker;

GRANT SELECT ON ge.access_recert_item TO app_readonly;

GRANT SELECT, DELETE ON ge.access_recert_item TO app_retention;

CREATE POLICY rls_access_recert_item__select ON ge.access_recert_item FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()));

CREATE POLICY rls_access_recert_item__insert ON ge.access_recert_item FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()));

CREATE POLICY rls_access_recert_item__update ON ge.access_recert_item FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()));

CREATE POLICY rls_access_recert_item__retention_delete ON ge.access_recert_item FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.agent_credential ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.agent_credential FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.agent_credential TO app_rw, app_worker;

GRANT SELECT ON ge.agent_credential TO app_readonly;

GRANT SELECT, DELETE ON ge.agent_credential TO app_retention;

CREATE POLICY rls_agent_credential__select ON ge.agent_credential FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_agent_credential__insert ON ge.agent_credential FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_agent_credential__update ON ge.agent_credential FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_agent_credential__retention_delete ON ge.agent_credential FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.agent_message ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.agent_message FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.agent_message TO app_rw, app_worker;

GRANT SELECT ON ge.agent_message TO app_readonly;

GRANT SELECT, DELETE ON ge.agent_message TO app_retention;

CREATE POLICY rls_agent_message__select ON ge.agent_message FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_agent_message__insert ON ge.agent_message FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_agent_message__update ON ge.agent_message FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_agent_message__retention_delete ON ge.agent_message FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.ai_agent_definition ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.ai_agent_definition FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.ai_agent_definition TO app_rw, app_worker;

GRANT SELECT ON ge.ai_agent_definition TO app_readonly;

GRANT SELECT, DELETE ON ge.ai_agent_definition TO app_retention;

CREATE POLICY rls_ai_agent_definition__select ON ge.ai_agent_definition FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND (startup_id IS NULL OR startup_id = ANY ((SELECT ge.app_company_ids())::uuid[])));

CREATE POLICY rls_ai_agent_definition__insert ON ge.ai_agent_definition FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND (startup_id = (SELECT ge.app_write_company()) OR (startup_id IS NULL AND (SELECT ge.app_actor_kind()) IN ('internal','service'))));

CREATE POLICY rls_ai_agent_definition__update ON ge.ai_agent_definition FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND (startup_id = (SELECT ge.app_write_company()) OR (startup_id IS NULL AND (SELECT ge.app_actor_kind()) IN ('internal','service')))) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND (startup_id = (SELECT ge.app_write_company()) OR (startup_id IS NULL AND (SELECT ge.app_actor_kind()) IN ('internal','service'))));

CREATE POLICY rls_ai_agent_definition__retention_delete ON ge.ai_agent_definition FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.ai_budget ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.ai_budget FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.ai_budget TO app_rw, app_worker;

GRANT SELECT ON ge.ai_budget TO app_readonly;

GRANT SELECT, DELETE ON ge.ai_budget TO app_retention;

ALTER TABLE ge.ai_cost_ledger ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.ai_cost_ledger FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT ON ge.ai_cost_ledger TO app_rw, app_worker;

GRANT SELECT ON ge.ai_cost_ledger TO app_readonly;

GRANT SELECT, DELETE ON ge.ai_cost_ledger TO app_retention;

CREATE POLICY rls_ai_cost_ledger__select ON ge.ai_cost_ledger FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_ai_cost_ledger__insert ON ge.ai_cost_ledger FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_ai_cost_ledger__retention_delete ON ge.ai_cost_ledger FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.ai_eval_case ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.ai_eval_case FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.ai_eval_case TO app_rw, app_worker;

GRANT SELECT ON ge.ai_eval_case TO app_readonly;

GRANT SELECT, DELETE ON ge.ai_eval_case TO app_retention;

CREATE POLICY rls_ai_eval_case__select ON ge.ai_eval_case FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND (startup_id IS NULL OR startup_id = ANY ((SELECT ge.app_company_ids())::uuid[])));

CREATE POLICY rls_ai_eval_case__insert ON ge.ai_eval_case FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND (startup_id = (SELECT ge.app_write_company()) OR (startup_id IS NULL AND (SELECT ge.app_actor_kind()) IN ('internal','service'))));

CREATE POLICY rls_ai_eval_case__update ON ge.ai_eval_case FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND (startup_id = (SELECT ge.app_write_company()) OR (startup_id IS NULL AND (SELECT ge.app_actor_kind()) IN ('internal','service')))) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND (startup_id = (SELECT ge.app_write_company()) OR (startup_id IS NULL AND (SELECT ge.app_actor_kind()) IN ('internal','service'))));

CREATE POLICY rls_ai_eval_case__retention_delete ON ge.ai_eval_case FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.ai_eval_case_result ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.ai_eval_case_result FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT ON ge.ai_eval_case_result TO app_rw, app_worker;

GRANT SELECT ON ge.ai_eval_case_result TO app_readonly;

GRANT SELECT, DELETE ON ge.ai_eval_case_result TO app_retention;

CREATE POLICY rls_ai_eval_case_result__select ON ge.ai_eval_case_result FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND (startup_id IS NULL OR startup_id = ANY ((SELECT ge.app_company_ids())::uuid[])));

CREATE POLICY rls_ai_eval_case_result__insert ON ge.ai_eval_case_result FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND (startup_id = (SELECT ge.app_write_company()) OR (startup_id IS NULL AND (SELECT ge.app_actor_kind()) IN ('internal','service'))));

CREATE POLICY rls_ai_eval_case_result__retention_delete ON ge.ai_eval_case_result FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.ai_feedback ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.ai_feedback FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT ON ge.ai_feedback TO app_rw, app_worker;

GRANT SELECT ON ge.ai_feedback TO app_readonly;

GRANT SELECT, DELETE ON ge.ai_feedback TO app_retention;

CREATE POLICY rls_ai_feedback__select ON ge.ai_feedback FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_ai_feedback__insert ON ge.ai_feedback FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_ai_feedback__retention_delete ON ge.ai_feedback FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

GRANT SELECT ON ge.ai_model TO app_rw, app_worker, app_readonly;

GRANT SELECT, INSERT, UPDATE ON ge.ai_model TO app_registry;

GRANT SELECT ON ge.ai_model_approval TO app_rw, app_worker, app_readonly;

GRANT SELECT, INSERT, UPDATE ON ge.ai_model_approval TO app_registry;

GRANT SELECT ON ge.ai_model_pin TO app_rw, app_worker, app_readonly;

GRANT SELECT, INSERT, UPDATE ON ge.ai_model_pin TO app_registry;

GRANT SELECT ON ge.ai_model_region TO app_rw, app_worker, app_readonly;

GRANT SELECT, INSERT, UPDATE ON ge.ai_model_region TO app_registry;

ALTER TABLE ge.ai_model_run ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.ai_model_run FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT ON ge.ai_model_run TO app_rw, app_worker;

GRANT SELECT ON ge.ai_model_run TO app_readonly;

GRANT SELECT, DELETE ON ge.ai_model_run TO app_retention;

CREATE POLICY rls_ai_model_run__select ON ge.ai_model_run FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_ai_model_run__insert ON ge.ai_model_run FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_ai_model_run__retention_delete ON ge.ai_model_run FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.ai_usage_event ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.ai_usage_event FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT ON ge.ai_usage_event TO app_rw, app_worker;

GRANT SELECT ON ge.ai_usage_event TO app_readonly;

GRANT SELECT, DELETE ON ge.ai_usage_event TO app_retention;

ALTER TABLE ge.ana_account_projection ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.ana_account_projection FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.ana_account_projection TO app_rw, app_worker;

GRANT SELECT ON ge.ana_account_projection TO app_readonly;

GRANT SELECT, DELETE ON ge.ana_account_projection TO app_retention;

CREATE POLICY rls_ana_account_projection__select ON ge.ana_account_projection FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_ana_account_projection__insert ON ge.ana_account_projection FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_ana_account_projection__update ON ge.ana_account_projection FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_ana_account_projection__retention_delete ON ge.ana_account_projection FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.ana_admin_projection ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.ana_admin_projection FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.ana_admin_projection TO app_rw, app_worker;

GRANT SELECT ON ge.ana_admin_projection TO app_readonly;

GRANT SELECT, DELETE ON ge.ana_admin_projection TO app_retention;

CREATE POLICY rls_ana_admin_projection__select ON ge.ana_admin_projection FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND (startup_id IS NULL OR startup_id = ANY ((SELECT ge.app_company_ids())::uuid[])));

CREATE POLICY rls_ana_admin_projection__insert ON ge.ana_admin_projection FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND (startup_id = (SELECT ge.app_write_company()) OR (startup_id IS NULL AND (SELECT ge.app_actor_kind()) IN ('internal','service'))));

CREATE POLICY rls_ana_admin_projection__update ON ge.ana_admin_projection FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND (startup_id = (SELECT ge.app_write_company()) OR (startup_id IS NULL AND (SELECT ge.app_actor_kind()) IN ('internal','service')))) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND (startup_id = (SELECT ge.app_write_company()) OR (startup_id IS NULL AND (SELECT ge.app_actor_kind()) IN ('internal','service'))));

CREATE POLICY rls_ana_admin_projection__retention_delete ON ge.ana_admin_projection FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.ana_forecast ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.ana_forecast FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT ON ge.ana_forecast TO app_rw, app_worker;

GRANT SELECT ON ge.ana_forecast TO app_readonly;

GRANT SELECT, DELETE ON ge.ana_forecast TO app_retention;

CREATE POLICY rls_ana_forecast__select ON ge.ana_forecast FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_ana_forecast__insert ON ge.ana_forecast FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_ana_forecast__retention_delete ON ge.ana_forecast FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.ana_metric_definition ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.ana_metric_definition FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.ana_metric_definition TO app_rw, app_worker;

GRANT SELECT ON ge.ana_metric_definition TO app_readonly;

GRANT SELECT, DELETE ON ge.ana_metric_definition TO app_retention;

CREATE POLICY rls_ana_metric_definition__select ON ge.ana_metric_definition FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND (startup_id IS NULL OR startup_id = ANY ((SELECT ge.app_company_ids())::uuid[])));

CREATE POLICY rls_ana_metric_definition__insert ON ge.ana_metric_definition FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND (startup_id = (SELECT ge.app_write_company()) OR (startup_id IS NULL AND (SELECT ge.app_actor_kind()) IN ('internal','service'))));

CREATE POLICY rls_ana_metric_definition__update ON ge.ana_metric_definition FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND (startup_id = (SELECT ge.app_write_company()) OR (startup_id IS NULL AND (SELECT ge.app_actor_kind()) IN ('internal','service')))) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND (startup_id = (SELECT ge.app_write_company()) OR (startup_id IS NULL AND (SELECT ge.app_actor_kind()) IN ('internal','service'))));

CREATE POLICY rls_ana_metric_definition__retention_delete ON ge.ana_metric_definition FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.ana_metric_snapshot ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.ana_metric_snapshot FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT ON ge.ana_metric_snapshot TO app_rw, app_worker;

GRANT SELECT ON ge.ana_metric_snapshot TO app_readonly;

GRANT SELECT, DELETE ON ge.ana_metric_snapshot TO app_retention;

CREATE POLICY rls_ana_metric_snapshot__select ON ge.ana_metric_snapshot FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_ana_metric_snapshot__insert ON ge.ana_metric_snapshot FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_ana_metric_snapshot__retention_delete ON ge.ana_metric_snapshot FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.ana_pipeline_projection ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.ana_pipeline_projection FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.ana_pipeline_projection TO app_rw, app_worker;

GRANT SELECT ON ge.ana_pipeline_projection TO app_readonly;

GRANT SELECT, DELETE ON ge.ana_pipeline_projection TO app_retention;

CREATE POLICY rls_ana_pipeline_projection__select ON ge.ana_pipeline_projection FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_ana_pipeline_projection__insert ON ge.ana_pipeline_projection FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_ana_pipeline_projection__update ON ge.ana_pipeline_projection FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_ana_pipeline_projection__retention_delete ON ge.ana_pipeline_projection FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.ana_report_subscription ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.ana_report_subscription FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.ana_report_subscription TO app_rw, app_worker;

GRANT SELECT ON ge.ana_report_subscription TO app_readonly;

GRANT SELECT, DELETE ON ge.ana_report_subscription TO app_retention;

CREATE POLICY rls_ana_report_subscription__select ON ge.ana_report_subscription FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND (startup_id IS NULL OR startup_id = ANY ((SELECT ge.app_company_ids())::uuid[])));

CREATE POLICY rls_ana_report_subscription__insert ON ge.ana_report_subscription FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND (startup_id = (SELECT ge.app_write_company()) OR (startup_id IS NULL AND (SELECT ge.app_actor_kind()) IN ('internal','service'))));

CREATE POLICY rls_ana_report_subscription__update ON ge.ana_report_subscription FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND (startup_id = (SELECT ge.app_write_company()) OR (startup_id IS NULL AND (SELECT ge.app_actor_kind()) IN ('internal','service')))) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND (startup_id = (SELECT ge.app_write_company()) OR (startup_id IS NULL AND (SELECT ge.app_actor_kind()) IN ('internal','service'))));

CREATE POLICY rls_ana_report_subscription__retention_delete ON ge.ana_report_subscription FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.ana_stage_metric ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.ana_stage_metric FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT ON ge.ana_stage_metric TO app_rw, app_worker;

GRANT SELECT ON ge.ana_stage_metric TO app_readonly;

GRANT SELECT, DELETE ON ge.ana_stage_metric TO app_retention;

CREATE POLICY rls_ana_stage_metric__select ON ge.ana_stage_metric FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_ana_stage_metric__insert ON ge.ana_stage_metric FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_ana_stage_metric__retention_delete ON ge.ana_stage_metric FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.api_key ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.api_key FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.api_key TO app_rw, app_worker;

GRANT SELECT ON ge.api_key TO app_readonly;

GRANT SELECT, DELETE ON ge.api_key TO app_retention;

GRANT SELECT ON ge.app_user TO app_rw, app_worker, app_readonly;

ALTER TABLE ge.audit_event ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.audit_event FORCE ROW LEVEL SECURITY;

GRANT SELECT ON ge.audit_event TO app_readonly;

GRANT SELECT, DELETE ON ge.audit_event TO app_retention;

ALTER TABLE ge.audit_sink ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.audit_sink FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.audit_sink TO app_rw, app_worker;

GRANT SELECT ON ge.audit_sink TO app_readonly;

GRANT SELECT, DELETE ON ge.audit_sink TO app_retention;

ALTER TABLE ge.aut_autonomy_plan ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.aut_autonomy_plan FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.aut_autonomy_plan TO app_rw, app_worker;

GRANT SELECT ON ge.aut_autonomy_plan TO app_readonly;

GRANT SELECT, DELETE ON ge.aut_autonomy_plan TO app_retention;

CREATE POLICY rls_aut_autonomy_plan__select ON ge.aut_autonomy_plan FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_aut_autonomy_plan__insert ON ge.aut_autonomy_plan FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_aut_autonomy_plan__update ON ge.aut_autonomy_plan FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_aut_autonomy_plan__retention_delete ON ge.aut_autonomy_plan FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.aut_config_revision ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.aut_config_revision FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.aut_config_revision TO app_rw, app_worker;

GRANT SELECT ON ge.aut_config_revision TO app_readonly;

GRANT SELECT, DELETE ON ge.aut_config_revision TO app_retention;

CREATE POLICY rls_aut_config_revision__select ON ge.aut_config_revision FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND (startup_id IS NULL OR startup_id = ANY ((SELECT ge.app_company_ids())::uuid[])));

CREATE POLICY rls_aut_config_revision__insert ON ge.aut_config_revision FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND (startup_id = (SELECT ge.app_write_company()) OR (startup_id IS NULL AND (SELECT ge.app_actor_kind()) IN ('internal','service'))));

CREATE POLICY rls_aut_config_revision__update ON ge.aut_config_revision FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND (startup_id = (SELECT ge.app_write_company()) OR (startup_id IS NULL AND (SELECT ge.app_actor_kind()) IN ('internal','service')))) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND (startup_id = (SELECT ge.app_write_company()) OR (startup_id IS NULL AND (SELECT ge.app_actor_kind()) IN ('internal','service'))));

CREATE POLICY rls_aut_config_revision__retention_delete ON ge.aut_config_revision FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.aut_conflict_case ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.aut_conflict_case FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.aut_conflict_case TO app_rw, app_worker;

GRANT SELECT ON ge.aut_conflict_case TO app_readonly;

GRANT SELECT, DELETE ON ge.aut_conflict_case TO app_retention;

CREATE POLICY rls_aut_conflict_case__select ON ge.aut_conflict_case FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_aut_conflict_case__insert ON ge.aut_conflict_case FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_aut_conflict_case__update ON ge.aut_conflict_case FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_aut_conflict_case__retention_delete ON ge.aut_conflict_case FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.aut_node_template ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.aut_node_template FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.aut_node_template TO app_rw, app_worker;

GRANT SELECT ON ge.aut_node_template TO app_readonly;

GRANT SELECT, DELETE ON ge.aut_node_template TO app_retention;

CREATE POLICY rls_aut_node_template__select ON ge.aut_node_template FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND (startup_id IS NULL OR startup_id = ANY ((SELECT ge.app_company_ids())::uuid[])));

CREATE POLICY rls_aut_node_template__insert ON ge.aut_node_template FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND (startup_id = (SELECT ge.app_write_company()) OR (startup_id IS NULL AND (SELECT ge.app_actor_kind()) IN ('internal','service'))));

CREATE POLICY rls_aut_node_template__update ON ge.aut_node_template FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND (startup_id = (SELECT ge.app_write_company()) OR (startup_id IS NULL AND (SELECT ge.app_actor_kind()) IN ('internal','service')))) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND (startup_id = (SELECT ge.app_write_company()) OR (startup_id IS NULL AND (SELECT ge.app_actor_kind()) IN ('internal','service'))));

CREATE POLICY rls_aut_node_template__retention_delete ON ge.aut_node_template FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.aut_run_conflict ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.aut_run_conflict FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.aut_run_conflict TO app_rw, app_worker;

GRANT SELECT ON ge.aut_run_conflict TO app_readonly;

GRANT SELECT, DELETE ON ge.aut_run_conflict TO app_retention;

CREATE POLICY rls_aut_run_conflict__select ON ge.aut_run_conflict FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_aut_run_conflict__insert ON ge.aut_run_conflict FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_aut_run_conflict__update ON ge.aut_run_conflict FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_aut_run_conflict__retention_delete ON ge.aut_run_conflict FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.aut_trigger ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.aut_trigger FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.aut_trigger TO app_rw, app_worker;

GRANT SELECT ON ge.aut_trigger TO app_readonly;

GRANT SELECT, DELETE ON ge.aut_trigger TO app_retention;

CREATE POLICY rls_aut_trigger__select ON ge.aut_trigger FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_aut_trigger__insert ON ge.aut_trigger FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_aut_trigger__update ON ge.aut_trigger FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_aut_trigger__retention_delete ON ge.aut_trigger FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.aut_workflow ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.aut_workflow FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.aut_workflow TO app_rw, app_worker;

GRANT SELECT ON ge.aut_workflow TO app_readonly;

GRANT SELECT, DELETE ON ge.aut_workflow TO app_retention;

CREATE POLICY rls_aut_workflow__select ON ge.aut_workflow FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_aut_workflow__insert ON ge.aut_workflow FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_aut_workflow__update ON ge.aut_workflow FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_aut_workflow__retention_delete ON ge.aut_workflow FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.aut_workflow_revision ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.aut_workflow_revision FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.aut_workflow_revision TO app_rw, app_worker;

GRANT SELECT ON ge.aut_workflow_revision TO app_readonly;

GRANT SELECT, DELETE ON ge.aut_workflow_revision TO app_retention;

CREATE POLICY rls_aut_workflow_revision__select ON ge.aut_workflow_revision FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_aut_workflow_revision__insert ON ge.aut_workflow_revision FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_aut_workflow_revision__update ON ge.aut_workflow_revision FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_aut_workflow_revision__retention_delete ON ge.aut_workflow_revision FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.aut_workflow_template ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.aut_workflow_template FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.aut_workflow_template TO app_rw, app_worker;

GRANT SELECT ON ge.aut_workflow_template TO app_readonly;

GRANT SELECT, DELETE ON ge.aut_workflow_template TO app_retention;

CREATE POLICY rls_aut_workflow_template__select ON ge.aut_workflow_template FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND (startup_id IS NULL OR startup_id = ANY ((SELECT ge.app_company_ids())::uuid[])));

CREATE POLICY rls_aut_workflow_template__insert ON ge.aut_workflow_template FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND (startup_id = (SELECT ge.app_write_company()) OR (startup_id IS NULL AND (SELECT ge.app_actor_kind()) IN ('internal','service'))));

CREATE POLICY rls_aut_workflow_template__update ON ge.aut_workflow_template FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND (startup_id = (SELECT ge.app_write_company()) OR (startup_id IS NULL AND (SELECT ge.app_actor_kind()) IN ('internal','service')))) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND (startup_id = (SELECT ge.app_write_company()) OR (startup_id IS NULL AND (SELECT ge.app_actor_kind()) IN ('internal','service'))));

CREATE POLICY rls_aut_workflow_template__retention_delete ON ge.aut_workflow_template FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

GRANT SELECT, INSERT, UPDATE ON ge.benchmark_cell TO app_bench;

ALTER TABLE ge.benchmark_cell ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.benchmark_cell FORCE ROW LEVEL SECURITY;

GRANT SELECT ON ge.benchmark_cell TO app_rw, app_readonly;

CREATE POLICY rls_benchmark_cell__published ON ge.benchmark_cell FOR SELECT TO app_rw, app_readonly USING (state = 'published');

CREATE POLICY rls_benchmark_cell__bench ON ge.benchmark_cell FOR ALL TO app_bench USING (true) WITH CHECK (true);

GRANT SELECT, INSERT, UPDATE ON ge.benchmark_contribution TO app_bench;

ALTER TABLE ge.benchmark_enrolment ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.benchmark_enrolment FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.benchmark_enrolment TO app_rw, app_worker;

GRANT SELECT ON ge.benchmark_enrolment TO app_readonly;

GRANT SELECT, DELETE ON ge.benchmark_enrolment TO app_retention;

CREATE POLICY rls_benchmark_enrolment__select ON ge.benchmark_enrolment FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND (company_id IS NULL OR company_id = ANY ((SELECT ge.app_company_ids())::uuid[])));

CREATE POLICY rls_benchmark_enrolment__insert ON ge.benchmark_enrolment FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND (company_id = (SELECT ge.app_write_company()) OR (company_id IS NULL AND (SELECT ge.app_actor_kind()) IN ('internal','service'))));

CREATE POLICY rls_benchmark_enrolment__update ON ge.benchmark_enrolment FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND (company_id = (SELECT ge.app_write_company()) OR (company_id IS NULL AND (SELECT ge.app_actor_kind()) IN ('internal','service')))) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND (company_id = (SELECT ge.app_write_company()) OR (company_id IS NULL AND (SELECT ge.app_actor_kind()) IN ('internal','service'))));

CREATE POLICY rls_benchmark_enrolment__retention_delete ON ge.benchmark_enrolment FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

GRANT SELECT, INSERT, UPDATE ON ge.benchmark_privacy_ledger TO app_bench;

ALTER TABLE ge.bid_file ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.bid_file FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.bid_file TO app_rw, app_worker;

GRANT SELECT ON ge.bid_file TO app_readonly;

GRANT SELECT, DELETE ON ge.bid_file TO app_retention;

CREATE POLICY rls_bid_file__select ON ge.bid_file FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_bid_file__insert ON ge.bid_file FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_bid_file__update ON ge.bid_file FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_bid_file__retention_delete ON ge.bid_file FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.bid_package ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.bid_package FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.bid_package TO app_rw, app_worker;

GRANT SELECT ON ge.bid_package TO app_readonly;

GRANT SELECT, DELETE ON ge.bid_package TO app_retention;

CREATE POLICY rls_bid_package__select ON ge.bid_package FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_bid_package__insert ON ge.bid_package FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_bid_package__update ON ge.bid_package FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_bid_package__retention_delete ON ge.bid_package FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.bid_submission ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.bid_submission FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.bid_submission TO app_rw, app_worker;

GRANT SELECT ON ge.bid_submission TO app_readonly;

GRANT SELECT, DELETE ON ge.bid_submission TO app_retention;

CREATE POLICY rls_bid_submission__select ON ge.bid_submission FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_bid_submission__insert ON ge.bid_submission FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_bid_submission__update ON ge.bid_submission FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_bid_submission__retention_delete ON ge.bid_submission FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.brand ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.brand FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.brand TO app_rw, app_worker;

GRANT SELECT ON ge.brand TO app_readonly;

GRANT SELECT, DELETE ON ge.brand TO app_retention;

ALTER TABLE ge.breakglass_account ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.breakglass_account FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.breakglass_account TO app_rw, app_worker;

GRANT SELECT ON ge.breakglass_account TO app_readonly;

GRANT SELECT, DELETE ON ge.breakglass_account TO app_retention;

CREATE POLICY rls_breakglass_account__select ON ge.breakglass_account FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()));

CREATE POLICY rls_breakglass_account__insert ON ge.breakglass_account FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()));

CREATE POLICY rls_breakglass_account__update ON ge.breakglass_account FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()));

CREATE POLICY rls_breakglass_account__retention_delete ON ge.breakglass_account FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.business_event ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.business_event FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.business_event TO app_rw, app_worker;

GRANT SELECT ON ge.business_event TO app_readonly;

GRANT SELECT, DELETE ON ge.business_event TO app_retention;

ALTER TABLE ge.cat_capability ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.cat_capability FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.cat_capability TO app_rw, app_worker;

GRANT SELECT ON ge.cat_capability TO app_readonly;

GRANT SELECT, DELETE ON ge.cat_capability TO app_retention;

CREATE POLICY rls_cat_capability__select ON ge.cat_capability FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_cat_capability__insert ON ge.cat_capability FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_cat_capability__update ON ge.cat_capability FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_cat_capability__retention_delete ON ge.cat_capability FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.cat_chunk ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.cat_chunk FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT ON ge.cat_chunk TO app_rw, app_worker;

GRANT SELECT ON ge.cat_chunk TO app_readonly;

GRANT SELECT, DELETE ON ge.cat_chunk TO app_retention;

CREATE POLICY rls_cat_chunk__select ON ge.cat_chunk FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_cat_chunk__insert ON ge.cat_chunk FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_cat_chunk__retention_delete ON ge.cat_chunk FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.cat_claim ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.cat_claim FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.cat_claim TO app_rw, app_worker;

GRANT SELECT ON ge.cat_claim TO app_readonly;

GRANT SELECT, DELETE ON ge.cat_claim TO app_retention;

CREATE POLICY rls_cat_claim__select ON ge.cat_claim FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_cat_claim__insert ON ge.cat_claim FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_cat_claim__update ON ge.cat_claim FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_cat_claim__retention_delete ON ge.cat_claim FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.cat_claim_evidence ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.cat_claim_evidence FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.cat_claim_evidence TO app_rw, app_worker;

GRANT SELECT ON ge.cat_claim_evidence TO app_readonly;

GRANT SELECT, DELETE ON ge.cat_claim_evidence TO app_retention;

CREATE POLICY rls_cat_claim_evidence__select ON ge.cat_claim_evidence FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_cat_claim_evidence__insert ON ge.cat_claim_evidence FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_cat_claim_evidence__update ON ge.cat_claim_evidence FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_cat_claim_evidence__retention_delete ON ge.cat_claim_evidence FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.cat_document ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.cat_document FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.cat_document TO app_rw, app_worker;

GRANT SELECT ON ge.cat_document TO app_readonly;

GRANT SELECT, DELETE ON ge.cat_document TO app_retention;

CREATE POLICY rls_cat_document__select ON ge.cat_document FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_cat_document__insert ON ge.cat_document FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_cat_document__update ON ge.cat_document FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_cat_document__retention_delete ON ge.cat_document FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.cat_document_offering ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.cat_document_offering FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.cat_document_offering TO app_rw, app_worker;

GRANT SELECT ON ge.cat_document_offering TO app_readonly;

GRANT SELECT, DELETE ON ge.cat_document_offering TO app_retention;

CREATE POLICY rls_cat_document_offering__select ON ge.cat_document_offering FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_cat_document_offering__insert ON ge.cat_document_offering FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_cat_document_offering__update ON ge.cat_document_offering FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_cat_document_offering__retention_delete ON ge.cat_document_offering FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.cat_embedding ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.cat_embedding FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT ON ge.cat_embedding TO app_rw, app_worker;

GRANT SELECT ON ge.cat_embedding TO app_readonly;

GRANT SELECT, DELETE ON ge.cat_embedding TO app_retention;

CREATE POLICY rls_cat_embedding__select ON ge.cat_embedding FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_cat_embedding__insert ON ge.cat_embedding FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_cat_embedding__retention_delete ON ge.cat_embedding FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.cat_launch_approval ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.cat_launch_approval FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT ON ge.cat_launch_approval TO app_rw, app_worker;

GRANT SELECT ON ge.cat_launch_approval TO app_readonly;

GRANT SELECT, DELETE ON ge.cat_launch_approval TO app_retention;

CREATE POLICY rls_cat_launch_approval__select ON ge.cat_launch_approval FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_cat_launch_approval__insert ON ge.cat_launch_approval FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_cat_launch_approval__retention_delete ON ge.cat_launch_approval FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.cat_offering_capability ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.cat_offering_capability FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.cat_offering_capability TO app_rw, app_worker;

GRANT SELECT ON ge.cat_offering_capability TO app_readonly;

GRANT SELECT, DELETE ON ge.cat_offering_capability TO app_retention;

CREATE POLICY rls_cat_offering_capability__select ON ge.cat_offering_capability FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_cat_offering_capability__insert ON ge.cat_offering_capability FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_cat_offering_capability__update ON ge.cat_offering_capability FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_cat_offering_capability__retention_delete ON ge.cat_offering_capability FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.cat_offering_version ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.cat_offering_version FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.cat_offering_version TO app_rw, app_worker;

GRANT SELECT ON ge.cat_offering_version TO app_readonly;

GRANT SELECT, DELETE ON ge.cat_offering_version TO app_retention;

CREATE POLICY rls_cat_offering_version__select ON ge.cat_offering_version FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_cat_offering_version__insert ON ge.cat_offering_version FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_cat_offering_version__update ON ge.cat_offering_version FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_cat_offering_version__retention_delete ON ge.cat_offering_version FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.cat_price_version ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.cat_price_version FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.cat_price_version TO app_rw, app_worker;

GRANT SELECT ON ge.cat_price_version TO app_readonly;

GRANT SELECT, DELETE ON ge.cat_price_version TO app_retention;

CREATE POLICY rls_cat_price_version__select ON ge.cat_price_version FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_cat_price_version__insert ON ge.cat_price_version FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_cat_price_version__update ON ge.cat_price_version FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_cat_price_version__retention_delete ON ge.cat_price_version FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.channel_account ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.channel_account FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.channel_account TO app_rw, app_worker;

GRANT SELECT ON ge.channel_account TO app_readonly;

GRANT SELECT, DELETE ON ge.channel_account TO app_retention;

ALTER TABLE ge.channel_account_market ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.channel_account_market FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.channel_account_market TO app_rw, app_worker;

GRANT SELECT ON ge.channel_account_market TO app_readonly;

GRANT SELECT, DELETE ON ge.channel_account_market TO app_retention;

ALTER TABLE ge.coaching_feedback ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.coaching_feedback FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.coaching_feedback TO app_rw, app_worker;

GRANT SELECT ON ge.coaching_feedback TO app_readonly;

GRANT SELECT, DELETE ON ge.coaching_feedback TO app_retention;

CREATE POLICY rls_coaching_feedback__select ON ge.coaching_feedback FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_coaching_feedback__insert ON ge.coaching_feedback FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_coaching_feedback__update ON ge.coaching_feedback FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_coaching_feedback__retention_delete ON ge.coaching_feedback FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.coaching_rubric ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.coaching_rubric FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.coaching_rubric TO app_rw, app_worker;

GRANT SELECT ON ge.coaching_rubric TO app_readonly;

GRANT SELECT, DELETE ON ge.coaching_rubric TO app_retention;

CREATE POLICY rls_coaching_rubric__select ON ge.coaching_rubric FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_coaching_rubric__insert ON ge.coaching_rubric FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_coaching_rubric__update ON ge.coaching_rubric FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_coaching_rubric__retention_delete ON ge.coaching_rubric FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.coaching_share ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.coaching_share FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.coaching_share TO app_rw, app_worker;

GRANT SELECT ON ge.coaching_share TO app_readonly;

GRANT SELECT, DELETE ON ge.coaching_share TO app_retention;

CREATE POLICY rls_coaching_share__select ON ge.coaching_share FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_coaching_share__insert ON ge.coaching_share FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_coaching_share__update ON ge.coaching_share FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_coaching_share__retention_delete ON ge.coaching_share FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.com_bid ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.com_bid FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.com_bid TO app_rw, app_worker;

GRANT SELECT ON ge.com_bid TO app_readonly;

GRANT SELECT, DELETE ON ge.com_bid TO app_retention;

CREATE POLICY rls_com_bid__select ON ge.com_bid FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_com_bid__insert ON ge.com_bid FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_com_bid__update ON ge.com_bid FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_com_bid__retention_delete ON ge.com_bid FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.com_bid_checklist_item ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.com_bid_checklist_item FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.com_bid_checklist_item TO app_rw, app_worker;

GRANT SELECT ON ge.com_bid_checklist_item TO app_readonly;

GRANT SELECT, DELETE ON ge.com_bid_checklist_item TO app_retention;

CREATE POLICY rls_com_bid_checklist_item__select ON ge.com_bid_checklist_item FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_com_bid_checklist_item__insert ON ge.com_bid_checklist_item FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_com_bid_checklist_item__update ON ge.com_bid_checklist_item FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_com_bid_checklist_item__retention_delete ON ge.com_bid_checklist_item FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.com_contract ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.com_contract FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.com_contract TO app_rw, app_worker;

GRANT SELECT ON ge.com_contract TO app_readonly;

GRANT SELECT, DELETE ON ge.com_contract TO app_retention;

CREATE POLICY rls_com_contract__select ON ge.com_contract FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_com_contract__insert ON ge.com_contract FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_com_contract__update ON ge.com_contract FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_com_contract__retention_delete ON ge.com_contract FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

CREATE POLICY rls_com_contract__portal_select ON ge.com_contract FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND (SELECT ge.app_actor_kind()) = 'portal' AND EXISTS (
  SELECT 1 FROM ge.ten_portal_grant g WHERE g.tenant_id = com_contract.tenant_id AND g.object_type = 'contract' AND g.object_id = com_contract.id
  AND g.subject_user_id = (SELECT ge.app_actor_id()) AND g.revoked_at IS NULL AND (g.expires_at IS NULL OR g.expires_at > now())));

ALTER TABLE ge.com_contract_party ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.com_contract_party FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.com_contract_party TO app_rw, app_worker;

GRANT SELECT ON ge.com_contract_party TO app_readonly;

GRANT SELECT, DELETE ON ge.com_contract_party TO app_retention;

CREATE POLICY rls_com_contract_party__select ON ge.com_contract_party FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_com_contract_party__insert ON ge.com_contract_party FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_com_contract_party__update ON ge.com_contract_party FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_com_contract_party__retention_delete ON ge.com_contract_party FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.com_discrepancy_case ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.com_discrepancy_case FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.com_discrepancy_case TO app_rw, app_worker;

GRANT SELECT ON ge.com_discrepancy_case TO app_readonly;

GRANT SELECT, DELETE ON ge.com_discrepancy_case TO app_retention;

CREATE POLICY rls_com_discrepancy_case__select ON ge.com_discrepancy_case FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_com_discrepancy_case__insert ON ge.com_discrepancy_case FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_com_discrepancy_case__update ON ge.com_discrepancy_case FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_com_discrepancy_case__retention_delete ON ge.com_discrepancy_case FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.com_fulfillment_event ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.com_fulfillment_event FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT ON ge.com_fulfillment_event TO app_rw, app_worker;

GRANT SELECT ON ge.com_fulfillment_event TO app_readonly;

GRANT SELECT, DELETE ON ge.com_fulfillment_event TO app_retention;

CREATE POLICY rls_com_fulfillment_event__select ON ge.com_fulfillment_event FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_com_fulfillment_event__insert ON ge.com_fulfillment_event FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_com_fulfillment_event__retention_delete ON ge.com_fulfillment_event FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.com_fulfillment_milestone ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.com_fulfillment_milestone FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.com_fulfillment_milestone TO app_rw, app_worker;

GRANT SELECT ON ge.com_fulfillment_milestone TO app_readonly;

GRANT SELECT, DELETE ON ge.com_fulfillment_milestone TO app_retention;

CREATE POLICY rls_com_fulfillment_milestone__select ON ge.com_fulfillment_milestone FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_com_fulfillment_milestone__insert ON ge.com_fulfillment_milestone FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_com_fulfillment_milestone__update ON ge.com_fulfillment_milestone FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_com_fulfillment_milestone__retention_delete ON ge.com_fulfillment_milestone FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.com_inventory_reservation ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.com_inventory_reservation FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.com_inventory_reservation TO app_rw, app_worker;

GRANT SELECT ON ge.com_inventory_reservation TO app_readonly;

GRANT SELECT, DELETE ON ge.com_inventory_reservation TO app_retention;

CREATE POLICY rls_com_inventory_reservation__select ON ge.com_inventory_reservation FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_com_inventory_reservation__insert ON ge.com_inventory_reservation FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_com_inventory_reservation__update ON ge.com_inventory_reservation FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_com_inventory_reservation__retention_delete ON ge.com_inventory_reservation FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.com_invoice ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.com_invoice FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.com_invoice TO app_rw, app_worker;

GRANT SELECT ON ge.com_invoice TO app_readonly;

GRANT SELECT, DELETE ON ge.com_invoice TO app_retention;

CREATE POLICY rls_com_invoice__select ON ge.com_invoice FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_com_invoice__insert ON ge.com_invoice FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_com_invoice__update ON ge.com_invoice FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_com_invoice__retention_delete ON ge.com_invoice FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

CREATE POLICY rls_com_invoice__portal_select ON ge.com_invoice FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND (SELECT ge.app_actor_kind()) = 'portal' AND EXISTS (
  SELECT 1 FROM ge.ten_portal_grant g WHERE g.tenant_id = com_invoice.tenant_id AND g.object_type = 'invoice' AND g.object_id = com_invoice.id
  AND g.subject_user_id = (SELECT ge.app_actor_id()) AND g.revoked_at IS NULL AND (g.expires_at IS NULL OR g.expires_at > now())));

ALTER TABLE ge.com_invoice_line ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.com_invoice_line FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.com_invoice_line TO app_rw, app_worker;

GRANT SELECT ON ge.com_invoice_line TO app_readonly;

GRANT SELECT, DELETE ON ge.com_invoice_line TO app_retention;

CREATE POLICY rls_com_invoice_line__select ON ge.com_invoice_line FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_com_invoice_line__insert ON ge.com_invoice_line FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_com_invoice_line__update ON ge.com_invoice_line FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_com_invoice_line__retention_delete ON ge.com_invoice_line FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.com_negotiation ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.com_negotiation FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.com_negotiation TO app_rw, app_worker;

GRANT SELECT ON ge.com_negotiation TO app_readonly;

GRANT SELECT, DELETE ON ge.com_negotiation TO app_retention;

CREATE POLICY rls_com_negotiation__select ON ge.com_negotiation FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_com_negotiation__insert ON ge.com_negotiation FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_com_negotiation__update ON ge.com_negotiation FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_com_negotiation__retention_delete ON ge.com_negotiation FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.com_objection ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.com_objection FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.com_objection TO app_rw, app_worker;

GRANT SELECT ON ge.com_objection TO app_readonly;

GRANT SELECT, DELETE ON ge.com_objection TO app_retention;

CREATE POLICY rls_com_objection__select ON ge.com_objection FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_com_objection__insert ON ge.com_objection FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_com_objection__update ON ge.com_objection FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_com_objection__retention_delete ON ge.com_objection FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.com_order ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.com_order FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.com_order TO app_rw, app_worker;

GRANT SELECT ON ge.com_order TO app_readonly;

GRANT SELECT, DELETE ON ge.com_order TO app_retention;

CREATE POLICY rls_com_order__select ON ge.com_order FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_com_order__insert ON ge.com_order FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_com_order__update ON ge.com_order FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_com_order__retention_delete ON ge.com_order FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

CREATE POLICY rls_com_order__portal_select ON ge.com_order FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND (SELECT ge.app_actor_kind()) = 'portal' AND EXISTS (
  SELECT 1 FROM ge.ten_portal_grant g WHERE g.tenant_id = com_order.tenant_id AND g.object_type = 'order' AND g.object_id = com_order.id
  AND g.subject_user_id = (SELECT ge.app_actor_id()) AND g.revoked_at IS NULL AND (g.expires_at IS NULL OR g.expires_at > now())));

ALTER TABLE ge.com_order_line ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.com_order_line FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.com_order_line TO app_rw, app_worker;

GRANT SELECT ON ge.com_order_line TO app_readonly;

GRANT SELECT, DELETE ON ge.com_order_line TO app_retention;

CREATE POLICY rls_com_order_line__select ON ge.com_order_line FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_com_order_line__insert ON ge.com_order_line FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_com_order_line__update ON ge.com_order_line FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_com_order_line__retention_delete ON ge.com_order_line FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.com_payable_entry ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.com_payable_entry FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT ON ge.com_payable_entry TO app_rw, app_worker;

GRANT SELECT ON ge.com_payable_entry TO app_readonly;

GRANT SELECT, DELETE ON ge.com_payable_entry TO app_retention;

CREATE POLICY rls_com_payable_entry__select ON ge.com_payable_entry FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_com_payable_entry__insert ON ge.com_payable_entry FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_com_payable_entry__retention_delete ON ge.com_payable_entry FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.com_payment ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.com_payment FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.com_payment TO app_rw, app_worker;

GRANT SELECT ON ge.com_payment TO app_readonly;

GRANT SELECT, DELETE ON ge.com_payment TO app_retention;

CREATE POLICY rls_com_payment__select ON ge.com_payment FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_com_payment__insert ON ge.com_payment FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_com_payment__update ON ge.com_payment FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_com_payment__retention_delete ON ge.com_payment FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.com_payment_allocation ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.com_payment_allocation FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT ON ge.com_payment_allocation TO app_rw, app_worker;

GRANT SELECT ON ge.com_payment_allocation TO app_readonly;

GRANT SELECT, DELETE ON ge.com_payment_allocation TO app_retention;

CREATE POLICY rls_com_payment_allocation__select ON ge.com_payment_allocation FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_com_payment_allocation__insert ON ge.com_payment_allocation FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_com_payment_allocation__retention_delete ON ge.com_payment_allocation FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.com_proposal ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.com_proposal FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.com_proposal TO app_rw, app_worker;

GRANT SELECT ON ge.com_proposal TO app_readonly;

GRANT SELECT, DELETE ON ge.com_proposal TO app_retention;

CREATE POLICY rls_com_proposal__select ON ge.com_proposal FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_com_proposal__insert ON ge.com_proposal FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_com_proposal__update ON ge.com_proposal FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_com_proposal__retention_delete ON ge.com_proposal FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

CREATE POLICY rls_com_proposal__portal_select ON ge.com_proposal FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND (SELECT ge.app_actor_kind()) = 'portal' AND EXISTS (
  SELECT 1 FROM ge.ten_portal_grant g WHERE g.tenant_id = com_proposal.tenant_id AND g.object_type = 'proposal' AND g.object_id = com_proposal.id
  AND g.subject_user_id = (SELECT ge.app_actor_id()) AND g.revoked_at IS NULL AND (g.expires_at IS NULL OR g.expires_at > now())));

ALTER TABLE ge.com_proposal_version ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.com_proposal_version FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.com_proposal_version TO app_rw, app_worker;

GRANT SELECT ON ge.com_proposal_version TO app_readonly;

GRANT SELECT, DELETE ON ge.com_proposal_version TO app_retention;

CREATE POLICY rls_com_proposal_version__select ON ge.com_proposal_version FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_com_proposal_version__insert ON ge.com_proposal_version FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_com_proposal_version__update ON ge.com_proposal_version FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_com_proposal_version__retention_delete ON ge.com_proposal_version FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.com_quote ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.com_quote FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.com_quote TO app_rw, app_worker;

GRANT SELECT ON ge.com_quote TO app_readonly;

GRANT SELECT, DELETE ON ge.com_quote TO app_retention;

CREATE POLICY rls_com_quote__select ON ge.com_quote FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_com_quote__insert ON ge.com_quote FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_com_quote__update ON ge.com_quote FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_com_quote__retention_delete ON ge.com_quote FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

CREATE POLICY rls_com_quote__portal_select ON ge.com_quote FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND (SELECT ge.app_actor_kind()) = 'portal' AND EXISTS (
  SELECT 1 FROM ge.ten_portal_grant g WHERE g.tenant_id = com_quote.tenant_id AND g.object_type = 'quote' AND g.object_id = com_quote.id
  AND g.subject_user_id = (SELECT ge.app_actor_id()) AND g.revoked_at IS NULL AND (g.expires_at IS NULL OR g.expires_at > now())));

ALTER TABLE ge.com_quote_line ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.com_quote_line FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.com_quote_line TO app_rw, app_worker;

GRANT SELECT ON ge.com_quote_line TO app_readonly;

GRANT SELECT, DELETE ON ge.com_quote_line TO app_retention;

CREATE POLICY rls_com_quote_line__select ON ge.com_quote_line FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_com_quote_line__insert ON ge.com_quote_line FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_com_quote_line__update ON ge.com_quote_line FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_com_quote_line__retention_delete ON ge.com_quote_line FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.com_receivable_entry ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.com_receivable_entry FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT ON ge.com_receivable_entry TO app_rw, app_worker;

GRANT SELECT ON ge.com_receivable_entry TO app_readonly;

GRANT SELECT, DELETE ON ge.com_receivable_entry TO app_retention;

CREATE POLICY rls_com_receivable_entry__select ON ge.com_receivable_entry FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_com_receivable_entry__insert ON ge.com_receivable_entry FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_com_receivable_entry__retention_delete ON ge.com_receivable_entry FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.com_signature_event ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.com_signature_event FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT ON ge.com_signature_event TO app_rw, app_worker;

GRANT SELECT ON ge.com_signature_event TO app_readonly;

GRANT SELECT, DELETE ON ge.com_signature_event TO app_retention;

CREATE POLICY rls_com_signature_event__select ON ge.com_signature_event FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_com_signature_event__insert ON ge.com_signature_event FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_com_signature_event__retention_delete ON ge.com_signature_event FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.com_sku_availability ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.com_sku_availability FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.com_sku_availability TO app_rw, app_worker;

GRANT SELECT ON ge.com_sku_availability TO app_readonly;

GRANT SELECT, DELETE ON ge.com_sku_availability TO app_retention;

CREATE POLICY rls_com_sku_availability__select ON ge.com_sku_availability FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_com_sku_availability__insert ON ge.com_sku_availability FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_com_sku_availability__update ON ge.com_sku_availability FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_com_sku_availability__retention_delete ON ge.com_sku_availability FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.commerce_order ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.commerce_order FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT ON ge.commerce_order TO app_rw, app_worker;

GRANT SELECT ON ge.commerce_order TO app_readonly;

GRANT SELECT, DELETE ON ge.commerce_order TO app_retention;

CREATE POLICY rls_commerce_order__select ON ge.commerce_order FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_commerce_order__insert ON ge.commerce_order FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_commerce_order__retention_delete ON ge.commerce_order FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.company ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.company FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.company TO app_rw, app_worker;

GRANT SELECT ON ge.company TO app_readonly;

GRANT SELECT, DELETE ON ge.company TO app_retention;

ALTER TABLE ge.company_operating_country ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.company_operating_country FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.company_operating_country TO app_rw, app_worker;

GRANT SELECT ON ge.company_operating_country TO app_readonly;

GRANT SELECT, DELETE ON ge.company_operating_country TO app_retention;

ALTER TABLE ge.config_promotion ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.config_promotion FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.config_promotion TO app_rw, app_worker;

GRANT SELECT ON ge.config_promotion TO app_readonly;

GRANT SELECT, DELETE ON ge.config_promotion TO app_retention;

ALTER TABLE ge.configuration_revision ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.configuration_revision FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.configuration_revision TO app_rw, app_worker;

GRANT SELECT ON ge.configuration_revision TO app_readonly;

GRANT SELECT, DELETE ON ge.configuration_revision TO app_retention;

ALTER TABLE ge.connector_installation ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.connector_installation FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.connector_installation TO app_rw, app_worker;

GRANT SELECT ON ge.connector_installation TO app_readonly;

GRANT SELECT, DELETE ON ge.connector_installation TO app_retention;

ALTER TABLE ge.consent_record ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.consent_record FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT ON ge.consent_record TO app_rw, app_worker;

GRANT SELECT ON ge.consent_record TO app_readonly;

GRANT SELECT, DELETE ON ge.consent_record TO app_retention;

ALTER TABLE ge.counterparty_agent ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.counterparty_agent FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.counterparty_agent TO app_rw, app_worker;

GRANT SELECT ON ge.counterparty_agent TO app_readonly;

GRANT SELECT, DELETE ON ge.counterparty_agent TO app_retention;

CREATE POLICY rls_counterparty_agent__select ON ge.counterparty_agent FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_counterparty_agent__insert ON ge.counterparty_agent FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_counterparty_agent__update ON ge.counterparty_agent FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_counterparty_agent__retention_delete ON ge.counterparty_agent FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.crm_activity ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.crm_activity FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT ON ge.crm_activity TO app_rw, app_worker;

GRANT SELECT ON ge.crm_activity TO app_readonly;

GRANT SELECT, DELETE ON ge.crm_activity TO app_retention;

CREATE POLICY rls_crm_activity__select ON ge.crm_activity FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_crm_activity__insert ON ge.crm_activity FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_crm_activity__retention_delete ON ge.crm_activity FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.crm_closure_policy ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.crm_closure_policy FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.crm_closure_policy TO app_rw, app_worker;

GRANT SELECT ON ge.crm_closure_policy TO app_readonly;

GRANT SELECT, DELETE ON ge.crm_closure_policy TO app_retention;

CREATE POLICY rls_crm_closure_policy__select ON ge.crm_closure_policy FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_crm_closure_policy__insert ON ge.crm_closure_policy FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_crm_closure_policy__update ON ge.crm_closure_policy FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_crm_closure_policy__retention_delete ON ge.crm_closure_policy FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.crm_deal ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.crm_deal FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.crm_deal TO app_rw, app_worker;

GRANT SELECT ON ge.crm_deal TO app_readonly;

GRANT SELECT, DELETE ON ge.crm_deal TO app_retention;

CREATE POLICY rls_crm_deal__select ON ge.crm_deal FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_crm_deal__insert ON ge.crm_deal FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_crm_deal__update ON ge.crm_deal FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_crm_deal__retention_delete ON ge.crm_deal FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.crm_deal_contact ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.crm_deal_contact FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.crm_deal_contact TO app_rw, app_worker;

GRANT SELECT ON ge.crm_deal_contact TO app_readonly;

GRANT SELECT, DELETE ON ge.crm_deal_contact TO app_retention;

CREATE POLICY rls_crm_deal_contact__select ON ge.crm_deal_contact FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_crm_deal_contact__insert ON ge.crm_deal_contact FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_crm_deal_contact__update ON ge.crm_deal_contact FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_crm_deal_contact__retention_delete ON ge.crm_deal_contact FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.crm_field_mapping ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.crm_field_mapping FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.crm_field_mapping TO app_rw, app_worker;

GRANT SELECT ON ge.crm_field_mapping TO app_readonly;

GRANT SELECT, DELETE ON ge.crm_field_mapping TO app_retention;

CREATE POLICY rls_crm_field_mapping__select ON ge.crm_field_mapping FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()));

CREATE POLICY rls_crm_field_mapping__insert ON ge.crm_field_mapping FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()));

CREATE POLICY rls_crm_field_mapping__update ON ge.crm_field_mapping FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()));

CREATE POLICY rls_crm_field_mapping__retention_delete ON ge.crm_field_mapping FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.crm_form ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.crm_form FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.crm_form TO app_rw, app_worker;

GRANT SELECT ON ge.crm_form TO app_readonly;

GRANT SELECT, DELETE ON ge.crm_form TO app_retention;

CREATE POLICY rls_crm_form__select ON ge.crm_form FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_crm_form__insert ON ge.crm_form FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_crm_form__update ON ge.crm_form FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_crm_form__retention_delete ON ge.crm_form FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.crm_form_version ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.crm_form_version FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.crm_form_version TO app_rw, app_worker;

GRANT SELECT ON ge.crm_form_version TO app_readonly;

GRANT SELECT, DELETE ON ge.crm_form_version TO app_retention;

CREATE POLICY rls_crm_form_version__select ON ge.crm_form_version FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_crm_form_version__insert ON ge.crm_form_version FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_crm_form_version__update ON ge.crm_form_version FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_crm_form_version__retention_delete ON ge.crm_form_version FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.crm_lead ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.crm_lead FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.crm_lead TO app_rw, app_worker;

GRANT SELECT ON ge.crm_lead TO app_readonly;

GRANT SELECT, DELETE ON ge.crm_lead TO app_retention;

CREATE POLICY rls_crm_lead__select ON ge.crm_lead FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_crm_lead__insert ON ge.crm_lead FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_crm_lead__update ON ge.crm_lead FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_crm_lead__retention_delete ON ge.crm_lead FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.crm_link ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.crm_link FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.crm_link TO app_rw, app_worker;

GRANT SELECT ON ge.crm_link TO app_readonly;

GRANT SELECT, DELETE ON ge.crm_link TO app_retention;

CREATE POLICY rls_crm_link__select ON ge.crm_link FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()));

CREATE POLICY rls_crm_link__insert ON ge.crm_link FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()));

CREATE POLICY rls_crm_link__update ON ge.crm_link FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()));

CREATE POLICY rls_crm_link__retention_delete ON ge.crm_link FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.crm_pipeline ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.crm_pipeline FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.crm_pipeline TO app_rw, app_worker;

GRANT SELECT ON ge.crm_pipeline TO app_readonly;

GRANT SELECT, DELETE ON ge.crm_pipeline TO app_retention;

CREATE POLICY rls_crm_pipeline__select ON ge.crm_pipeline FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_crm_pipeline__insert ON ge.crm_pipeline FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_crm_pipeline__update ON ge.crm_pipeline FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_crm_pipeline__retention_delete ON ge.crm_pipeline FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.crm_stage ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.crm_stage FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.crm_stage TO app_rw, app_worker;

GRANT SELECT ON ge.crm_stage TO app_readonly;

GRANT SELECT, DELETE ON ge.crm_stage TO app_retention;

CREATE POLICY rls_crm_stage__select ON ge.crm_stage FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_crm_stage__insert ON ge.crm_stage FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_crm_stage__update ON ge.crm_stage FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_crm_stage__retention_delete ON ge.crm_stage FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.crm_stage_transition ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.crm_stage_transition FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT ON ge.crm_stage_transition TO app_rw, app_worker;

GRANT SELECT ON ge.crm_stage_transition TO app_readonly;

GRANT SELECT, DELETE ON ge.crm_stage_transition TO app_retention;

CREATE POLICY rls_crm_stage_transition__select ON ge.crm_stage_transition FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_crm_stage_transition__insert ON ge.crm_stage_transition FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_crm_stage_transition__retention_delete ON ge.crm_stage_transition FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.crm_submission ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.crm_submission FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT ON ge.crm_submission TO app_rw, app_worker;

GRANT SELECT ON ge.crm_submission TO app_readonly;

GRANT SELECT, DELETE ON ge.crm_submission TO app_retention;

CREATE POLICY rls_crm_submission__select ON ge.crm_submission FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_crm_submission__insert ON ge.crm_submission FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_crm_submission__retention_delete ON ge.crm_submission FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.custom_role ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.custom_role FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.custom_role TO app_rw, app_worker;

GRANT SELECT ON ge.custom_role TO app_readonly;

GRANT SELECT, DELETE ON ge.custom_role TO app_retention;

ALTER TABLE ge.customer_value ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.customer_value FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.customer_value TO app_rw, app_worker;

GRANT SELECT ON ge.customer_value TO app_readonly;

GRANT SELECT, DELETE ON ge.customer_value TO app_retention;

ALTER TABLE ge.dispute_case ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.dispute_case FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.dispute_case TO app_rw, app_worker;

GRANT SELECT ON ge.dispute_case TO app_readonly;

GRANT SELECT, DELETE ON ge.dispute_case TO app_retention;

CREATE POLICY rls_dispute_case__select ON ge.dispute_case FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_dispute_case__insert ON ge.dispute_case FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_dispute_case__update ON ge.dispute_case FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_dispute_case__retention_delete ON ge.dispute_case FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.division ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.division FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.division TO app_rw, app_worker;

GRANT SELECT ON ge.division TO app_readonly;

GRANT SELECT, DELETE ON ge.division TO app_retention;

ALTER TABLE ge.dlt_registration ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.dlt_registration FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.dlt_registration TO app_rw, app_worker;

GRANT SELECT ON ge.dlt_registration TO app_readonly;

GRANT SELECT, DELETE ON ge.dlt_registration TO app_retention;

CREATE POLICY rls_dlt_registration__select ON ge.dlt_registration FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND company_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_dlt_registration__insert ON ge.dlt_registration FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND company_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_dlt_registration__update ON ge.dlt_registration FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND company_id = (SELECT ge.app_write_company())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND company_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_dlt_registration__retention_delete ON ge.dlt_registration FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.dlt_template ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.dlt_template FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.dlt_template TO app_rw, app_worker;

GRANT SELECT ON ge.dlt_template TO app_readonly;

GRANT SELECT, DELETE ON ge.dlt_template TO app_retention;

CREATE POLICY rls_dlt_template__select ON ge.dlt_template FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()));

CREATE POLICY rls_dlt_template__insert ON ge.dlt_template FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()));

CREATE POLICY rls_dlt_template__update ON ge.dlt_template FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()));

CREATE POLICY rls_dlt_template__retention_delete ON ge.dlt_template FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.domain_record_version ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.domain_record_version FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.domain_record_version TO app_rw, app_worker;

GRANT SELECT ON ge.domain_record_version TO app_readonly;

GRANT SELECT, DELETE ON ge.domain_record_version TO app_retention;

GRANT SELECT ON ge.domain_schema_registry TO app_rw, app_worker, app_readonly;

ALTER TABLE ge.dsar_request ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.dsar_request FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.dsar_request TO app_rw, app_worker;

GRANT SELECT ON ge.dsar_request TO app_readonly;

GRANT SELECT, DELETE ON ge.dsar_request TO app_retention;

GRANT SELECT ON ge.edge_conformance_check TO app_rw, app_worker, app_readonly;

GRANT INSERT ON ge.edge_conformance_check TO app_worker;

GRANT SELECT ON ge.edge_project TO app_rw, app_worker, app_readonly;

ALTER TABLE ge.effect ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.effect FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.effect TO app_rw, app_worker;

GRANT SELECT ON ge.effect TO app_readonly;

GRANT SELECT, DELETE ON ge.effect TO app_retention;

ALTER TABLE ge.effect_receipt ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.effect_receipt FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.effect_receipt TO app_rw, app_worker;

GRANT SELECT ON ge.effect_receipt TO app_readonly;

GRANT SELECT, DELETE ON ge.effect_receipt TO app_retention;

CREATE POLICY rls_effect_receipt__select ON ge.effect_receipt FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_effect_receipt__insert ON ge.effect_receipt FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_effect_receipt__update ON ge.effect_receipt FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_effect_receipt__retention_delete ON ge.effect_receipt FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.eng_calendar_link ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.eng_calendar_link FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.eng_calendar_link TO app_rw, app_worker;

GRANT SELECT ON ge.eng_calendar_link TO app_readonly;

GRANT SELECT, DELETE ON ge.eng_calendar_link TO app_retention;

CREATE POLICY rls_eng_calendar_link__select ON ge.eng_calendar_link FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_eng_calendar_link__insert ON ge.eng_calendar_link FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_eng_calendar_link__update ON ge.eng_calendar_link FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_eng_calendar_link__retention_delete ON ge.eng_calendar_link FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.eng_chat_session ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.eng_chat_session FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.eng_chat_session TO app_rw, app_worker;

GRANT SELECT ON ge.eng_chat_session TO app_readonly;

GRANT SELECT, DELETE ON ge.eng_chat_session TO app_retention;

CREATE POLICY rls_eng_chat_session__select ON ge.eng_chat_session FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_eng_chat_session__insert ON ge.eng_chat_session FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_eng_chat_session__update ON ge.eng_chat_session FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_eng_chat_session__retention_delete ON ge.eng_chat_session FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.eng_delivery_event ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.eng_delivery_event FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT ON ge.eng_delivery_event TO app_rw, app_worker;

GRANT SELECT ON ge.eng_delivery_event TO app_readonly;

GRANT SELECT, DELETE ON ge.eng_delivery_event TO app_retention;

CREATE POLICY rls_eng_delivery_event__select ON ge.eng_delivery_event FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_eng_delivery_event__insert ON ge.eng_delivery_event FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_eng_delivery_event__retention_delete ON ge.eng_delivery_event FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.eng_enrollment ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.eng_enrollment FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.eng_enrollment TO app_rw, app_worker;

GRANT SELECT ON ge.eng_enrollment TO app_readonly;

GRANT SELECT, DELETE ON ge.eng_enrollment TO app_retention;

CREATE POLICY rls_eng_enrollment__select ON ge.eng_enrollment FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_eng_enrollment__insert ON ge.eng_enrollment FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_eng_enrollment__update ON ge.eng_enrollment FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_eng_enrollment__retention_delete ON ge.eng_enrollment FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.eng_identity_link ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.eng_identity_link FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.eng_identity_link TO app_rw, app_worker;

GRANT SELECT ON ge.eng_identity_link TO app_readonly;

GRANT SELECT, DELETE ON ge.eng_identity_link TO app_retention;

CREATE POLICY rls_eng_identity_link__select ON ge.eng_identity_link FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_eng_identity_link__insert ON ge.eng_identity_link FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_eng_identity_link__update ON ge.eng_identity_link FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_eng_identity_link__retention_delete ON ge.eng_identity_link FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.eng_inbound_event ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.eng_inbound_event FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT ON ge.eng_inbound_event TO app_rw, app_worker;

GRANT SELECT ON ge.eng_inbound_event TO app_readonly;

GRANT SELECT, DELETE ON ge.eng_inbound_event TO app_retention;

CREATE POLICY rls_eng_inbound_event__select ON ge.eng_inbound_event FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_eng_inbound_event__insert ON ge.eng_inbound_event FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_eng_inbound_event__retention_delete ON ge.eng_inbound_event FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.eng_intent ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.eng_intent FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT ON ge.eng_intent TO app_rw, app_worker;

GRANT SELECT ON ge.eng_intent TO app_readonly;

GRANT SELECT, DELETE ON ge.eng_intent TO app_retention;

CREATE POLICY rls_eng_intent__select ON ge.eng_intent FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_eng_intent__insert ON ge.eng_intent FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_eng_intent__retention_delete ON ge.eng_intent FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.eng_meeting ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.eng_meeting FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.eng_meeting TO app_rw, app_worker;

GRANT SELECT ON ge.eng_meeting TO app_readonly;

GRANT SELECT, DELETE ON ge.eng_meeting TO app_retention;

CREATE POLICY rls_eng_meeting__select ON ge.eng_meeting FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_eng_meeting__insert ON ge.eng_meeting FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_eng_meeting__update ON ge.eng_meeting FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_eng_meeting__retention_delete ON ge.eng_meeting FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.eng_message ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.eng_message FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.eng_message TO app_rw, app_worker;

GRANT SELECT ON ge.eng_message TO app_readonly;

GRANT SELECT, DELETE ON ge.eng_message TO app_retention;

CREATE POLICY rls_eng_message__select ON ge.eng_message FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_eng_message__insert ON ge.eng_message FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_eng_message__update ON ge.eng_message FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_eng_message__retention_delete ON ge.eng_message FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.eng_message_claim ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.eng_message_claim FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.eng_message_claim TO app_rw, app_worker;

GRANT SELECT ON ge.eng_message_claim TO app_readonly;

GRANT SELECT, DELETE ON ge.eng_message_claim TO app_retention;

CREATE POLICY rls_eng_message_claim__select ON ge.eng_message_claim FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_eng_message_claim__insert ON ge.eng_message_claim FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_eng_message_claim__update ON ge.eng_message_claim FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_eng_message_claim__retention_delete ON ge.eng_message_claim FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.eng_message_draft ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.eng_message_draft FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.eng_message_draft TO app_rw, app_worker;

GRANT SELECT ON ge.eng_message_draft TO app_readonly;

GRANT SELECT, DELETE ON ge.eng_message_draft TO app_retention;

CREATE POLICY rls_eng_message_draft__select ON ge.eng_message_draft FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_eng_message_draft__insert ON ge.eng_message_draft FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_eng_message_draft__update ON ge.eng_message_draft FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_eng_message_draft__retention_delete ON ge.eng_message_draft FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.eng_message_template ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.eng_message_template FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.eng_message_template TO app_rw, app_worker;

GRANT SELECT ON ge.eng_message_template TO app_readonly;

GRANT SELECT, DELETE ON ge.eng_message_template TO app_retention;

CREATE POLICY rls_eng_message_template__select ON ge.eng_message_template FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_eng_message_template__insert ON ge.eng_message_template FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_eng_message_template__update ON ge.eng_message_template FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_eng_message_template__retention_delete ON ge.eng_message_template FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.eng_routing_rule ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.eng_routing_rule FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.eng_routing_rule TO app_rw, app_worker;

GRANT SELECT ON ge.eng_routing_rule TO app_readonly;

GRANT SELECT, DELETE ON ge.eng_routing_rule TO app_retention;

CREATE POLICY rls_eng_routing_rule__select ON ge.eng_routing_rule FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_eng_routing_rule__insert ON ge.eng_routing_rule FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_eng_routing_rule__update ON ge.eng_routing_rule FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_eng_routing_rule__retention_delete ON ge.eng_routing_rule FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.eng_sequence ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.eng_sequence FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.eng_sequence TO app_rw, app_worker;

GRANT SELECT ON ge.eng_sequence TO app_readonly;

GRANT SELECT, DELETE ON ge.eng_sequence TO app_retention;

CREATE POLICY rls_eng_sequence__select ON ge.eng_sequence FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_eng_sequence__insert ON ge.eng_sequence FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_eng_sequence__update ON ge.eng_sequence FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_eng_sequence__retention_delete ON ge.eng_sequence FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.eng_sequence_step ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.eng_sequence_step FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.eng_sequence_step TO app_rw, app_worker;

GRANT SELECT ON ge.eng_sequence_step TO app_readonly;

GRANT SELECT, DELETE ON ge.eng_sequence_step TO app_retention;

CREATE POLICY rls_eng_sequence_step__select ON ge.eng_sequence_step FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_eng_sequence_step__insert ON ge.eng_sequence_step FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_eng_sequence_step__update ON ge.eng_sequence_step FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_eng_sequence_step__retention_delete ON ge.eng_sequence_step FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.eng_thread ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.eng_thread FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.eng_thread TO app_rw, app_worker;

GRANT SELECT ON ge.eng_thread TO app_readonly;

GRANT SELECT, DELETE ON ge.eng_thread TO app_retention;

CREATE POLICY rls_eng_thread__select ON ge.eng_thread FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_eng_thread__insert ON ge.eng_thread FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_eng_thread__update ON ge.eng_thread FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_eng_thread__retention_delete ON ge.eng_thread FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

GRANT SELECT ON ge.eval_run TO app_rw, app_worker, app_readonly;

GRANT SELECT, INSERT, UPDATE ON ge.eval_run TO app_registry;

GRANT SELECT ON ge.eval_suite TO app_rw, app_worker, app_readonly;

GRANT SELECT, INSERT, UPDATE ON ge.eval_suite TO app_registry;

ALTER TABLE ge.experiment ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.experiment FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.experiment TO app_rw, app_worker;

GRANT SELECT ON ge.experiment TO app_readonly;

GRANT SELECT, DELETE ON ge.experiment TO app_retention;

ALTER TABLE ge.export_job ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.export_job FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.export_job TO app_rw, app_worker;

GRANT SELECT ON ge.export_job TO app_readonly;

GRANT SELECT, DELETE ON ge.export_job TO app_retention;

ALTER TABLE ge.feedback_case ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.feedback_case FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.feedback_case TO app_rw, app_worker;

GRANT SELECT ON ge.feedback_case TO app_readonly;

GRANT SELECT, DELETE ON ge.feedback_case TO app_retention;

GRANT SELECT ON ge.fx_rate TO app_rw, app_worker, app_readonly;

ALTER TABLE ge.gov_approval ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.gov_approval FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT ON ge.gov_approval TO app_rw, app_worker;

GRANT SELECT ON ge.gov_approval TO app_readonly;

GRANT SELECT, DELETE ON ge.gov_approval TO app_retention;

CREATE POLICY rls_gov_approval__select ON ge.gov_approval FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_gov_approval__insert ON ge.gov_approval FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_gov_approval__retention_delete ON ge.gov_approval FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.gov_approval_delegation ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.gov_approval_delegation FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.gov_approval_delegation TO app_rw, app_worker;

GRANT SELECT ON ge.gov_approval_delegation TO app_readonly;

GRANT SELECT, DELETE ON ge.gov_approval_delegation TO app_retention;

CREATE POLICY rls_gov_approval_delegation__select ON ge.gov_approval_delegation FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_gov_approval_delegation__insert ON ge.gov_approval_delegation FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_gov_approval_delegation__update ON ge.gov_approval_delegation FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_gov_approval_delegation__retention_delete ON ge.gov_approval_delegation FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.gov_approval_policy ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.gov_approval_policy FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.gov_approval_policy TO app_rw, app_worker;

GRANT SELECT ON ge.gov_approval_policy TO app_readonly;

GRANT SELECT, DELETE ON ge.gov_approval_policy TO app_retention;

CREATE POLICY rls_gov_approval_policy__select ON ge.gov_approval_policy FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND (startup_id IS NULL OR startup_id = ANY ((SELECT ge.app_company_ids())::uuid[])));

CREATE POLICY rls_gov_approval_policy__insert ON ge.gov_approval_policy FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND (startup_id = (SELECT ge.app_write_company()) OR (startup_id IS NULL AND (SELECT ge.app_actor_kind()) IN ('internal','service'))));

CREATE POLICY rls_gov_approval_policy__update ON ge.gov_approval_policy FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND (startup_id = (SELECT ge.app_write_company()) OR (startup_id IS NULL AND (SELECT ge.app_actor_kind()) IN ('internal','service')))) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND (startup_id = (SELECT ge.app_write_company()) OR (startup_id IS NULL AND (SELECT ge.app_actor_kind()) IN ('internal','service'))));

CREATE POLICY rls_gov_approval_policy__retention_delete ON ge.gov_approval_policy FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.gov_eligibility_decision ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.gov_eligibility_decision FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT ON ge.gov_eligibility_decision TO app_rw, app_worker;

GRANT SELECT ON ge.gov_eligibility_decision TO app_readonly;

GRANT SELECT, DELETE ON ge.gov_eligibility_decision TO app_retention;

CREATE POLICY rls_gov_eligibility_decision__select ON ge.gov_eligibility_decision FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_gov_eligibility_decision__insert ON ge.gov_eligibility_decision FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_gov_eligibility_decision__retention_delete ON ge.gov_eligibility_decision FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.gov_legal_hold ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.gov_legal_hold FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.gov_legal_hold TO app_rw, app_worker;

GRANT SELECT ON ge.gov_legal_hold TO app_readonly;

GRANT SELECT, DELETE ON ge.gov_legal_hold TO app_retention;

CREATE POLICY rls_gov_legal_hold__select ON ge.gov_legal_hold FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND (startup_id IS NULL OR startup_id = ANY ((SELECT ge.app_company_ids())::uuid[])));

CREATE POLICY rls_gov_legal_hold__insert ON ge.gov_legal_hold FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND (startup_id = (SELECT ge.app_write_company()) OR (startup_id IS NULL AND (SELECT ge.app_actor_kind()) IN ('internal','service'))));

CREATE POLICY rls_gov_legal_hold__update ON ge.gov_legal_hold FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND (startup_id = (SELECT ge.app_write_company()) OR (startup_id IS NULL AND (SELECT ge.app_actor_kind()) IN ('internal','service')))) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND (startup_id = (SELECT ge.app_write_company()) OR (startup_id IS NULL AND (SELECT ge.app_actor_kind()) IN ('internal','service'))));

CREATE POLICY rls_gov_legal_hold__retention_delete ON ge.gov_legal_hold FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.gov_policy_decision ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.gov_policy_decision FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT ON ge.gov_policy_decision TO app_rw, app_worker;

GRANT SELECT ON ge.gov_policy_decision TO app_readonly;

GRANT SELECT, DELETE ON ge.gov_policy_decision TO app_retention;

CREATE POLICY rls_gov_policy_decision__select ON ge.gov_policy_decision FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_gov_policy_decision__insert ON ge.gov_policy_decision FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_gov_policy_decision__retention_delete ON ge.gov_policy_decision FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.gov_policy_version ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.gov_policy_version FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.gov_policy_version TO app_rw, app_worker;

GRANT SELECT ON ge.gov_policy_version TO app_readonly;

GRANT SELECT, DELETE ON ge.gov_policy_version TO app_retention;

CREATE POLICY rls_gov_policy_version__select ON ge.gov_policy_version FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND (startup_id IS NULL OR startup_id = ANY ((SELECT ge.app_company_ids())::uuid[])));

CREATE POLICY rls_gov_policy_version__insert ON ge.gov_policy_version FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND (startup_id = (SELECT ge.app_write_company()) OR (startup_id IS NULL AND (SELECT ge.app_actor_kind()) IN ('internal','service'))));

CREATE POLICY rls_gov_policy_version__update ON ge.gov_policy_version FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND (startup_id = (SELECT ge.app_write_company()) OR (startup_id IS NULL AND (SELECT ge.app_actor_kind()) IN ('internal','service')))) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND (startup_id = (SELECT ge.app_write_company()) OR (startup_id IS NULL AND (SELECT ge.app_actor_kind()) IN ('internal','service'))));

CREATE POLICY rls_gov_policy_version__retention_delete ON ge.gov_policy_version FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.gov_retention_policy ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.gov_retention_policy FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.gov_retention_policy TO app_rw, app_worker;

GRANT SELECT ON ge.gov_retention_policy TO app_readonly;

GRANT SELECT, DELETE ON ge.gov_retention_policy TO app_retention;

CREATE POLICY rls_gov_retention_policy__select ON ge.gov_retention_policy FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND (startup_id IS NULL OR startup_id = ANY ((SELECT ge.app_company_ids())::uuid[])));

CREATE POLICY rls_gov_retention_policy__insert ON ge.gov_retention_policy FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND (startup_id = (SELECT ge.app_write_company()) OR (startup_id IS NULL AND (SELECT ge.app_actor_kind()) IN ('internal','service'))));

CREATE POLICY rls_gov_retention_policy__update ON ge.gov_retention_policy FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND (startup_id = (SELECT ge.app_write_company()) OR (startup_id IS NULL AND (SELECT ge.app_actor_kind()) IN ('internal','service')))) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND (startup_id = (SELECT ge.app_write_company()) OR (startup_id IS NULL AND (SELECT ge.app_actor_kind()) IN ('internal','service'))));

CREATE POLICY rls_gov_retention_policy__retention_delete ON ge.gov_retention_policy FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.idp_certificate ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.idp_certificate FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.idp_certificate TO app_rw, app_worker;

GRANT SELECT ON ge.idp_certificate TO app_readonly;

GRANT SELECT, DELETE ON ge.idp_certificate TO app_retention;

CREATE POLICY rls_idp_certificate__select ON ge.idp_certificate FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()));

CREATE POLICY rls_idp_certificate__insert ON ge.idp_certificate FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()));

CREATE POLICY rls_idp_certificate__update ON ge.idp_certificate FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()));

CREATE POLICY rls_idp_certificate__retention_delete ON ge.idp_certificate FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.idp_connection ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.idp_connection FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.idp_connection TO app_rw, app_worker;

GRANT SELECT ON ge.idp_connection TO app_readonly;

GRANT SELECT, DELETE ON ge.idp_connection TO app_retention;

CREATE POLICY rls_idp_connection__select ON ge.idp_connection FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()));

CREATE POLICY rls_idp_connection__insert ON ge.idp_connection FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()));

CREATE POLICY rls_idp_connection__update ON ge.idp_connection FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()));

CREATE POLICY rls_idp_connection__retention_delete ON ge.idp_connection FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.inbox ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.inbox FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.inbox TO app_rw, app_worker;

GRANT SELECT ON ge.inbox TO app_readonly;

GRANT SELECT, DELETE ON ge.inbox TO app_retention;

ALTER TABLE ge.incident ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.incident FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.incident TO app_rw, app_worker;

GRANT SELECT ON ge.incident TO app_readonly;

GRANT SELECT, DELETE ON ge.incident TO app_retention;

GRANT SELECT ON ge.incident_notification TO app_rw, app_worker, app_readonly;

GRANT SELECT, INSERT, UPDATE ON ge.incident_notification TO app_platform_sec;

ALTER TABLE ge.int_credential_ref ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.int_credential_ref FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.int_credential_ref TO app_rw, app_worker;

GRANT SELECT ON ge.int_credential_ref TO app_readonly;

GRANT SELECT, DELETE ON ge.int_credential_ref TO app_retention;

CREATE POLICY rls_int_credential_ref__select ON ge.int_credential_ref FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_int_credential_ref__insert ON ge.int_credential_ref FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_int_credential_ref__update ON ge.int_credential_ref FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_int_credential_ref__retention_delete ON ge.int_credential_ref FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.int_provider_event ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.int_provider_event FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT ON ge.int_provider_event TO app_rw, app_worker;

GRANT SELECT ON ge.int_provider_event TO app_readonly;

GRANT SELECT, DELETE ON ge.int_provider_event TO app_retention;

CREATE POLICY rls_int_provider_event__select ON ge.int_provider_event FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_int_provider_event__insert ON ge.int_provider_event FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_int_provider_event__retention_delete ON ge.int_provider_event FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.int_quota ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.int_quota FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.int_quota TO app_rw, app_worker;

GRANT SELECT ON ge.int_quota TO app_readonly;

GRANT SELECT, DELETE ON ge.int_quota TO app_retention;

CREATE POLICY rls_int_quota__select ON ge.int_quota FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_int_quota__insert ON ge.int_quota FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_int_quota__update ON ge.int_quota FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_int_quota__retention_delete ON ge.int_quota FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.intel_alias ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.intel_alias FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.intel_alias TO app_rw, app_worker;

GRANT SELECT ON ge.intel_alias TO app_readonly;

GRANT SELECT, DELETE ON ge.intel_alias TO app_retention;

CREATE POLICY rls_intel_alias__select ON ge.intel_alias FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_intel_alias__insert ON ge.intel_alias FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_intel_alias__update ON ge.intel_alias FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_intel_alias__retention_delete ON ge.intel_alias FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.intel_competitor ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.intel_competitor FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.intel_competitor TO app_rw, app_worker;

GRANT SELECT ON ge.intel_competitor TO app_readonly;

GRANT SELECT, DELETE ON ge.intel_competitor TO app_retention;

CREATE POLICY rls_intel_competitor__select ON ge.intel_competitor FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_intel_competitor__insert ON ge.intel_competitor FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_intel_competitor__update ON ge.intel_competitor FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_intel_competitor__retention_delete ON ge.intel_competitor FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.intel_contact ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.intel_contact FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.intel_contact TO app_rw, app_worker;

GRANT SELECT ON ge.intel_contact TO app_readonly;

GRANT SELECT, DELETE ON ge.intel_contact TO app_retention;

CREATE POLICY rls_intel_contact__select ON ge.intel_contact FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_intel_contact__insert ON ge.intel_contact FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_intel_contact__update ON ge.intel_contact FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_intel_contact__retention_delete ON ge.intel_contact FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.intel_contact_source ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.intel_contact_source FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT ON ge.intel_contact_source TO app_rw, app_worker;

GRANT SELECT ON ge.intel_contact_source TO app_readonly;

GRANT SELECT, DELETE ON ge.intel_contact_source TO app_retention;

CREATE POLICY rls_intel_contact_source__select ON ge.intel_contact_source FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_intel_contact_source__insert ON ge.intel_contact_source FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_intel_contact_source__retention_delete ON ge.intel_contact_source FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.intel_contact_verification ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.intel_contact_verification FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT ON ge.intel_contact_verification TO app_rw, app_worker;

GRANT SELECT ON ge.intel_contact_verification TO app_readonly;

GRANT SELECT, DELETE ON ge.intel_contact_verification TO app_retention;

CREATE POLICY rls_intel_contact_verification__select ON ge.intel_contact_verification FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_intel_contact_verification__insert ON ge.intel_contact_verification FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_intel_contact_verification__retention_delete ON ge.intel_contact_verification FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.intel_evidence ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.intel_evidence FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.intel_evidence TO app_rw, app_worker;

GRANT SELECT ON ge.intel_evidence TO app_readonly;

GRANT SELECT, DELETE ON ge.intel_evidence TO app_retention;

CREATE POLICY rls_intel_evidence__select ON ge.intel_evidence FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_intel_evidence__insert ON ge.intel_evidence FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_intel_evidence__update ON ge.intel_evidence FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_intel_evidence__retention_delete ON ge.intel_evidence FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.intel_fetch_log ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.intel_fetch_log FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT ON ge.intel_fetch_log TO app_rw, app_worker;

GRANT SELECT ON ge.intel_fetch_log TO app_readonly;

GRANT SELECT, DELETE ON ge.intel_fetch_log TO app_retention;

CREATE POLICY rls_intel_fetch_log__select ON ge.intel_fetch_log FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_intel_fetch_log__insert ON ge.intel_fetch_log FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_intel_fetch_log__retention_delete ON ge.intel_fetch_log FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.intel_location ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.intel_location FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.intel_location TO app_rw, app_worker;

GRANT SELECT ON ge.intel_location TO app_readonly;

GRANT SELECT, DELETE ON ge.intel_location TO app_retention;

CREATE POLICY rls_intel_location__select ON ge.intel_location FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_intel_location__insert ON ge.intel_location FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_intel_location__update ON ge.intel_location FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_intel_location__retention_delete ON ge.intel_location FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.intel_market_event ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.intel_market_event FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.intel_market_event TO app_rw, app_worker;

GRANT SELECT ON ge.intel_market_event TO app_readonly;

GRANT SELECT, DELETE ON ge.intel_market_event TO app_retention;

CREATE POLICY rls_intel_market_event__select ON ge.intel_market_event FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_intel_market_event__insert ON ge.intel_market_event FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_intel_market_event__update ON ge.intel_market_event FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_intel_market_event__retention_delete ON ge.intel_market_event FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.intel_match ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.intel_match FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.intel_match TO app_rw, app_worker;

GRANT SELECT ON ge.intel_match TO app_readonly;

GRANT SELECT, DELETE ON ge.intel_match TO app_retention;

CREATE POLICY rls_intel_match__select ON ge.intel_match FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_intel_match__insert ON ge.intel_match FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_intel_match__update ON ge.intel_match FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_intel_match__retention_delete ON ge.intel_match FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.intel_need ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.intel_need FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.intel_need TO app_rw, app_worker;

GRANT SELECT ON ge.intel_need TO app_readonly;

GRANT SELECT, DELETE ON ge.intel_need TO app_retention;

CREATE POLICY rls_intel_need__select ON ge.intel_need FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_intel_need__insert ON ge.intel_need FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_intel_need__update ON ge.intel_need FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_intel_need__retention_delete ON ge.intel_need FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.intel_need_evidence ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.intel_need_evidence FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT ON ge.intel_need_evidence TO app_rw, app_worker;

GRANT SELECT ON ge.intel_need_evidence TO app_readonly;

GRANT SELECT, DELETE ON ge.intel_need_evidence TO app_retention;

CREATE POLICY rls_intel_need_evidence__select ON ge.intel_need_evidence FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_intel_need_evidence__insert ON ge.intel_need_evidence FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_intel_need_evidence__retention_delete ON ge.intel_need_evidence FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.intel_opportunity ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.intel_opportunity FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.intel_opportunity TO app_rw, app_worker;

GRANT SELECT ON ge.intel_opportunity TO app_readonly;

GRANT SELECT, DELETE ON ge.intel_opportunity TO app_retention;

CREATE POLICY rls_intel_opportunity__select ON ge.intel_opportunity FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_intel_opportunity__insert ON ge.intel_opportunity FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_intel_opportunity__update ON ge.intel_opportunity FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_intel_opportunity__retention_delete ON ge.intel_opportunity FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.intel_opportunity_contact ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.intel_opportunity_contact FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.intel_opportunity_contact TO app_rw, app_worker;

GRANT SELECT ON ge.intel_opportunity_contact TO app_readonly;

GRANT SELECT, DELETE ON ge.intel_opportunity_contact TO app_retention;

CREATE POLICY rls_intel_opportunity_contact__select ON ge.intel_opportunity_contact FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_intel_opportunity_contact__insert ON ge.intel_opportunity_contact FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_intel_opportunity_contact__update ON ge.intel_opportunity_contact FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_intel_opportunity_contact__retention_delete ON ge.intel_opportunity_contact FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.intel_organization ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.intel_organization FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.intel_organization TO app_rw, app_worker;

GRANT SELECT ON ge.intel_organization TO app_readonly;

GRANT SELECT, DELETE ON ge.intel_organization TO app_retention;

CREATE POLICY rls_intel_organization__select ON ge.intel_organization FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_intel_organization__insert ON ge.intel_organization FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_intel_organization__update ON ge.intel_organization FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_intel_organization__retention_delete ON ge.intel_organization FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.intel_query_run ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.intel_query_run FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT ON ge.intel_query_run TO app_rw, app_worker;

GRANT SELECT ON ge.intel_query_run TO app_readonly;

GRANT SELECT, DELETE ON ge.intel_query_run TO app_retention;

CREATE POLICY rls_intel_query_run__select ON ge.intel_query_run FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_intel_query_run__insert ON ge.intel_query_run FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_intel_query_run__retention_delete ON ge.intel_query_run FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.intel_review ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.intel_review FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT ON ge.intel_review TO app_rw, app_worker;

GRANT SELECT ON ge.intel_review TO app_readonly;

GRANT SELECT, DELETE ON ge.intel_review TO app_retention;

CREATE POLICY rls_intel_review__select ON ge.intel_review FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_intel_review__insert ON ge.intel_review FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_intel_review__retention_delete ON ge.intel_review FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.intel_role_hypothesis ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.intel_role_hypothesis FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.intel_role_hypothesis TO app_rw, app_worker;

GRANT SELECT ON ge.intel_role_hypothesis TO app_readonly;

GRANT SELECT, DELETE ON ge.intel_role_hypothesis TO app_retention;

CREATE POLICY rls_intel_role_hypothesis__select ON ge.intel_role_hypothesis FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_intel_role_hypothesis__insert ON ge.intel_role_hypothesis FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_intel_role_hypothesis__update ON ge.intel_role_hypothesis FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_intel_role_hypothesis__retention_delete ON ge.intel_role_hypothesis FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.intel_score_version ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.intel_score_version FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT ON ge.intel_score_version TO app_rw, app_worker;

GRANT SELECT ON ge.intel_score_version TO app_readonly;

GRANT SELECT, DELETE ON ge.intel_score_version TO app_retention;

CREATE POLICY rls_intel_score_version__select ON ge.intel_score_version FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_intel_score_version__insert ON ge.intel_score_version FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_intel_score_version__retention_delete ON ge.intel_score_version FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.intel_scoring_model ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.intel_scoring_model FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.intel_scoring_model TO app_rw, app_worker;

GRANT SELECT ON ge.intel_scoring_model TO app_readonly;

GRANT SELECT, DELETE ON ge.intel_scoring_model TO app_retention;

CREATE POLICY rls_intel_scoring_model__select ON ge.intel_scoring_model FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_intel_scoring_model__insert ON ge.intel_scoring_model FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_intel_scoring_model__update ON ge.intel_scoring_model FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_intel_scoring_model__retention_delete ON ge.intel_scoring_model FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.intel_search_plan ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.intel_search_plan FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.intel_search_plan TO app_rw, app_worker;

GRANT SELECT ON ge.intel_search_plan TO app_readonly;

GRANT SELECT, DELETE ON ge.intel_search_plan TO app_retention;

CREATE POLICY rls_intel_search_plan__select ON ge.intel_search_plan FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_intel_search_plan__insert ON ge.intel_search_plan FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_intel_search_plan__update ON ge.intel_search_plan FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_intel_search_plan__retention_delete ON ge.intel_search_plan FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.intel_signal ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.intel_signal FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.intel_signal TO app_rw, app_worker;

GRANT SELECT ON ge.intel_signal TO app_readonly;

GRANT SELECT, DELETE ON ge.intel_signal TO app_retention;

CREATE POLICY rls_intel_signal__select ON ge.intel_signal FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_intel_signal__insert ON ge.intel_signal FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_intel_signal__update ON ge.intel_signal FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_intel_signal__retention_delete ON ge.intel_signal FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.intel_signal_evidence ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.intel_signal_evidence FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.intel_signal_evidence TO app_rw, app_worker;

GRANT SELECT ON ge.intel_signal_evidence TO app_readonly;

GRANT SELECT, DELETE ON ge.intel_signal_evidence TO app_retention;

CREATE POLICY rls_intel_signal_evidence__select ON ge.intel_signal_evidence FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_intel_signal_evidence__insert ON ge.intel_signal_evidence FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_intel_signal_evidence__update ON ge.intel_signal_evidence FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_intel_signal_evidence__retention_delete ON ge.intel_signal_evidence FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.intel_signal_type ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.intel_signal_type FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.intel_signal_type TO app_rw, app_worker;

GRANT SELECT ON ge.intel_signal_type TO app_readonly;

GRANT SELECT, DELETE ON ge.intel_signal_type TO app_retention;

CREATE POLICY rls_intel_signal_type__select ON ge.intel_signal_type FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND (startup_id IS NULL OR startup_id = ANY ((SELECT ge.app_company_ids())::uuid[])));

CREATE POLICY rls_intel_signal_type__insert ON ge.intel_signal_type FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND (startup_id = (SELECT ge.app_write_company()) OR (startup_id IS NULL AND (SELECT ge.app_actor_kind()) IN ('internal','service'))));

CREATE POLICY rls_intel_signal_type__update ON ge.intel_signal_type FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND (startup_id = (SELECT ge.app_write_company()) OR (startup_id IS NULL AND (SELECT ge.app_actor_kind()) IN ('internal','service')))) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND (startup_id = (SELECT ge.app_write_company()) OR (startup_id IS NULL AND (SELECT ge.app_actor_kind()) IN ('internal','service'))));

CREATE POLICY rls_intel_signal_type__retention_delete ON ge.intel_signal_type FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.intel_social_post ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.intel_social_post FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.intel_social_post TO app_rw, app_worker;

GRANT SELECT ON ge.intel_social_post TO app_readonly;

GRANT SELECT, DELETE ON ge.intel_social_post TO app_retention;

CREATE POLICY rls_intel_social_post__select ON ge.intel_social_post FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_intel_social_post__insert ON ge.intel_social_post FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_intel_social_post__update ON ge.intel_social_post FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_intel_social_post__retention_delete ON ge.intel_social_post FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.intel_source ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.intel_source FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.intel_source TO app_rw, app_worker;

GRANT SELECT ON ge.intel_source TO app_readonly;

GRANT SELECT, DELETE ON ge.intel_source TO app_retention;

CREATE POLICY rls_intel_source__select ON ge.intel_source FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_intel_source__insert ON ge.intel_source FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_intel_source__update ON ge.intel_source FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_intel_source__retention_delete ON ge.intel_source FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.intel_source_policy ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.intel_source_policy FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.intel_source_policy TO app_rw, app_worker;

GRANT SELECT ON ge.intel_source_policy TO app_readonly;

GRANT SELECT, DELETE ON ge.intel_source_policy TO app_retention;

CREATE POLICY rls_intel_source_policy__select ON ge.intel_source_policy FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_intel_source_policy__insert ON ge.intel_source_policy FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_intel_source_policy__update ON ge.intel_source_policy FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_intel_source_policy__retention_delete ON ge.intel_source_policy FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.intel_source_record ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.intel_source_record FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.intel_source_record TO app_rw, app_worker;

GRANT SELECT ON ge.intel_source_record TO app_readonly;

GRANT SELECT, DELETE ON ge.intel_source_record TO app_retention;

CREATE POLICY rls_intel_source_record__select ON ge.intel_source_record FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_intel_source_record__insert ON ge.intel_source_record FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_intel_source_record__update ON ge.intel_source_record FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_intel_source_record__retention_delete ON ge.intel_source_record FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.inv_access_grant ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.inv_access_grant FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.inv_access_grant TO app_rw, app_worker;

GRANT SELECT ON ge.inv_access_grant TO app_readonly;

GRANT SELECT, DELETE ON ge.inv_access_grant TO app_retention;

CREATE POLICY rls_inv_access_grant__select ON ge.inv_access_grant FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_inv_access_grant__insert ON ge.inv_access_grant FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_inv_access_grant__update ON ge.inv_access_grant FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_inv_access_grant__retention_delete ON ge.inv_access_grant FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.inv_accreditation_verification ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.inv_accreditation_verification FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.inv_accreditation_verification TO app_rw, app_worker;

GRANT SELECT ON ge.inv_accreditation_verification TO app_readonly;

GRANT SELECT, DELETE ON ge.inv_accreditation_verification TO app_retention;

CREATE POLICY rls_inv_accreditation_verification__select ON ge.inv_accreditation_verification FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_inv_accreditation_verification__insert ON ge.inv_accreditation_verification FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_inv_accreditation_verification__update ON ge.inv_accreditation_verification FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_inv_accreditation_verification__retention_delete ON ge.inv_accreditation_verification FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.inv_advice_boundary_event ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.inv_advice_boundary_event FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT ON ge.inv_advice_boundary_event TO app_rw, app_worker;

GRANT SELECT ON ge.inv_advice_boundary_event TO app_readonly;

GRANT SELECT, DELETE ON ge.inv_advice_boundary_event TO app_retention;

CREATE POLICY rls_inv_advice_boundary_event__select ON ge.inv_advice_boundary_event FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_inv_advice_boundary_event__insert ON ge.inv_advice_boundary_event FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_inv_advice_boundary_event__retention_delete ON ge.inv_advice_boundary_event FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.inv_adviser_referral ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.inv_adviser_referral FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.inv_adviser_referral TO app_rw, app_worker;

GRANT SELECT ON ge.inv_adviser_referral TO app_readonly;

GRANT SELECT, DELETE ON ge.inv_adviser_referral TO app_retention;

CREATE POLICY rls_inv_adviser_referral__select ON ge.inv_adviser_referral FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_inv_adviser_referral__insert ON ge.inv_adviser_referral FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_inv_adviser_referral__update ON ge.inv_adviser_referral FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_inv_adviser_referral__retention_delete ON ge.inv_adviser_referral FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.inv_agreement ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.inv_agreement FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.inv_agreement TO app_rw, app_worker;

GRANT SELECT ON ge.inv_agreement TO app_readonly;

GRANT SELECT, DELETE ON ge.inv_agreement TO app_retention;

CREATE POLICY rls_inv_agreement__select ON ge.inv_agreement FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_inv_agreement__insert ON ge.inv_agreement FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_inv_agreement__update ON ge.inv_agreement FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_inv_agreement__retention_delete ON ge.inv_agreement FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.inv_allotment ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.inv_allotment FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.inv_allotment TO app_rw, app_worker;

GRANT SELECT ON ge.inv_allotment TO app_readonly;

GRANT SELECT, DELETE ON ge.inv_allotment TO app_retention;

CREATE POLICY rls_inv_allotment__select ON ge.inv_allotment FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_inv_allotment__insert ON ge.inv_allotment FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_inv_allotment__update ON ge.inv_allotment FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_inv_allotment__retention_delete ON ge.inv_allotment FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.inv_allotment_clock ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.inv_allotment_clock FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.inv_allotment_clock TO app_rw, app_worker;

GRANT SELECT ON ge.inv_allotment_clock TO app_readonly;

GRANT SELECT, DELETE ON ge.inv_allotment_clock TO app_retention;

CREATE POLICY rls_inv_allotment_clock__select ON ge.inv_allotment_clock FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_inv_allotment_clock__insert ON ge.inv_allotment_clock FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_inv_allotment_clock__update ON ge.inv_allotment_clock FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_inv_allotment_clock__retention_delete ON ge.inv_allotment_clock FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.inv_application_money_account ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.inv_application_money_account FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.inv_application_money_account TO app_rw, app_worker;

GRANT SELECT ON ge.inv_application_money_account TO app_readonly;

GRANT SELECT, DELETE ON ge.inv_application_money_account TO app_retention;

CREATE POLICY rls_inv_application_money_account__select ON ge.inv_application_money_account FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_inv_application_money_account__insert ON ge.inv_application_money_account FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_inv_application_money_account__update ON ge.inv_application_money_account FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_inv_application_money_account__retention_delete ON ge.inv_application_money_account FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.inv_approval ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.inv_approval FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.inv_approval TO app_rw, app_worker;

GRANT SELECT ON ge.inv_approval TO app_readonly;

GRANT SELECT, DELETE ON ge.inv_approval TO app_retention;

CREATE POLICY rls_inv_approval__select ON ge.inv_approval FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_inv_approval__insert ON ge.inv_approval FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_inv_approval__update ON ge.inv_approval FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_inv_approval__retention_delete ON ge.inv_approval FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.inv_bank_account ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.inv_bank_account FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.inv_bank_account TO app_rw, app_worker;

GRANT SELECT ON ge.inv_bank_account TO app_readonly;

GRANT SELECT, DELETE ON ge.inv_bank_account TO app_retention;

CREATE POLICY rls_inv_bank_account__select ON ge.inv_bank_account FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_inv_bank_account__insert ON ge.inv_bank_account FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_inv_bank_account__update ON ge.inv_bank_account FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_inv_bank_account__retention_delete ON ge.inv_bank_account FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.inv_cap_table_revision ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.inv_cap_table_revision FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT ON ge.inv_cap_table_revision TO app_rw, app_worker;

GRANT SELECT ON ge.inv_cap_table_revision TO app_readonly;

GRANT SELECT, DELETE ON ge.inv_cap_table_revision TO app_retention;

CREATE POLICY rls_inv_cap_table_revision__select ON ge.inv_cap_table_revision FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_inv_cap_table_revision__insert ON ge.inv_cap_table_revision FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_inv_cap_table_revision__retention_delete ON ge.inv_cap_table_revision FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.inv_capital_allocation ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.inv_capital_allocation FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.inv_capital_allocation TO app_rw, app_worker;

GRANT SELECT ON ge.inv_capital_allocation TO app_readonly;

GRANT SELECT, DELETE ON ge.inv_capital_allocation TO app_retention;

CREATE POLICY rls_inv_capital_allocation__select ON ge.inv_capital_allocation FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_inv_capital_allocation__insert ON ge.inv_capital_allocation FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_inv_capital_allocation__update ON ge.inv_capital_allocation FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_inv_capital_allocation__retention_delete ON ge.inv_capital_allocation FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.inv_channel ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.inv_channel FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.inv_channel TO app_rw, app_worker;

GRANT SELECT ON ge.inv_channel TO app_readonly;

GRANT SELECT, DELETE ON ge.inv_channel TO app_retention;

CREATE POLICY rls_inv_channel__select ON ge.inv_channel FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_inv_channel__insert ON ge.inv_channel FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_inv_channel__update ON ge.inv_channel FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_inv_channel__retention_delete ON ge.inv_channel FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.inv_claim ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.inv_claim FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.inv_claim TO app_rw, app_worker;

GRANT SELECT ON ge.inv_claim TO app_readonly;

GRANT SELECT, DELETE ON ge.inv_claim TO app_retention;

CREATE POLICY rls_inv_claim__select ON ge.inv_claim FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_inv_claim__insert ON ge.inv_claim FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_inv_claim__update ON ge.inv_claim FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_inv_claim__retention_delete ON ge.inv_claim FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.inv_closing ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.inv_closing FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.inv_closing TO app_rw, app_worker;

GRANT SELECT ON ge.inv_closing TO app_readonly;

GRANT SELECT, DELETE ON ge.inv_closing TO app_retention;

CREATE POLICY rls_inv_closing__select ON ge.inv_closing FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_inv_closing__insert ON ge.inv_closing FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_inv_closing__update ON ge.inv_closing FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_inv_closing__retention_delete ON ge.inv_closing FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.inv_closing_requirement ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.inv_closing_requirement FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.inv_closing_requirement TO app_rw, app_worker;

GRANT SELECT ON ge.inv_closing_requirement TO app_readonly;

GRANT SELECT, DELETE ON ge.inv_closing_requirement TO app_retention;

CREATE POLICY rls_inv_closing_requirement__select ON ge.inv_closing_requirement FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_inv_closing_requirement__insert ON ge.inv_closing_requirement FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_inv_closing_requirement__update ON ge.inv_closing_requirement FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_inv_closing_requirement__retention_delete ON ge.inv_closing_requirement FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.inv_commitment ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.inv_commitment FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT ON ge.inv_commitment TO app_rw, app_worker;

GRANT SELECT ON ge.inv_commitment TO app_readonly;

GRANT SELECT, DELETE ON ge.inv_commitment TO app_retention;

CREATE POLICY rls_inv_commitment__select ON ge.inv_commitment FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_inv_commitment__insert ON ge.inv_commitment FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_inv_commitment__retention_delete ON ge.inv_commitment FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.inv_contact ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.inv_contact FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.inv_contact TO app_rw, app_worker;

GRANT SELECT ON ge.inv_contact TO app_readonly;

GRANT SELECT, DELETE ON ge.inv_contact TO app_retention;

CREATE POLICY rls_inv_contact__select ON ge.inv_contact FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_inv_contact__insert ON ge.inv_contact FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_inv_contact__update ON ge.inv_contact FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_inv_contact__retention_delete ON ge.inv_contact FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.inv_contact_evidence ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.inv_contact_evidence FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.inv_contact_evidence TO app_rw, app_worker;

GRANT SELECT ON ge.inv_contact_evidence TO app_readonly;

GRANT SELECT, DELETE ON ge.inv_contact_evidence TO app_retention;

CREATE POLICY rls_inv_contact_evidence__select ON ge.inv_contact_evidence FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_inv_contact_evidence__insert ON ge.inv_contact_evidence FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_inv_contact_evidence__update ON ge.inv_contact_evidence FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_inv_contact_evidence__retention_delete ON ge.inv_contact_evidence FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.inv_copilot_action ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.inv_copilot_action FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.inv_copilot_action TO app_rw, app_worker;

GRANT SELECT ON ge.inv_copilot_action TO app_readonly;

GRANT SELECT, DELETE ON ge.inv_copilot_action TO app_retention;

CREATE POLICY rls_inv_copilot_action__select ON ge.inv_copilot_action FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_inv_copilot_action__insert ON ge.inv_copilot_action FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_inv_copilot_action__update ON ge.inv_copilot_action FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_inv_copilot_action__retention_delete ON ge.inv_copilot_action FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.inv_counsel_signoff ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.inv_counsel_signoff FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.inv_counsel_signoff TO app_rw, app_worker;

GRANT SELECT ON ge.inv_counsel_signoff TO app_readonly;

GRANT SELECT, DELETE ON ge.inv_counsel_signoff TO app_retention;

CREATE POLICY rls_inv_counsel_signoff__select ON ge.inv_counsel_signoff FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_inv_counsel_signoff__insert ON ge.inv_counsel_signoff FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_inv_counsel_signoff__update ON ge.inv_counsel_signoff FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_inv_counsel_signoff__retention_delete ON ge.inv_counsel_signoff FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.inv_covenant ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.inv_covenant FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.inv_covenant TO app_rw, app_worker;

GRANT SELECT ON ge.inv_covenant TO app_readonly;

GRANT SELECT, DELETE ON ge.inv_covenant TO app_retention;

CREATE POLICY rls_inv_covenant__select ON ge.inv_covenant FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_inv_covenant__insert ON ge.inv_covenant FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_inv_covenant__update ON ge.inv_covenant FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_inv_covenant__retention_delete ON ge.inv_covenant FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.inv_crossborder_case ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.inv_crossborder_case FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.inv_crossborder_case TO app_rw, app_worker;

GRANT SELECT ON ge.inv_crossborder_case TO app_readonly;

GRANT SELECT, DELETE ON ge.inv_crossborder_case TO app_retention;

CREATE POLICY rls_inv_crossborder_case__select ON ge.inv_crossborder_case FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_inv_crossborder_case__insert ON ge.inv_crossborder_case FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_inv_crossborder_case__update ON ge.inv_crossborder_case FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_inv_crossborder_case__retention_delete ON ge.inv_crossborder_case FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.inv_crossborder_requirement ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.inv_crossborder_requirement FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.inv_crossborder_requirement TO app_rw, app_worker;

GRANT SELECT ON ge.inv_crossborder_requirement TO app_readonly;

GRANT SELECT, DELETE ON ge.inv_crossborder_requirement TO app_retention;

CREATE POLICY rls_inv_crossborder_requirement__select ON ge.inv_crossborder_requirement FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_inv_crossborder_requirement__insert ON ge.inv_crossborder_requirement FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_inv_crossborder_requirement__update ON ge.inv_crossborder_requirement FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_inv_crossborder_requirement__retention_delete ON ge.inv_crossborder_requirement FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.inv_dashboard_projection ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.inv_dashboard_projection FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.inv_dashboard_projection TO app_rw, app_worker;

GRANT SELECT ON ge.inv_dashboard_projection TO app_readonly;

GRANT SELECT, DELETE ON ge.inv_dashboard_projection TO app_retention;

CREATE POLICY rls_inv_dashboard_projection__select ON ge.inv_dashboard_projection FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_inv_dashboard_projection__insert ON ge.inv_dashboard_projection FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_inv_dashboard_projection__update ON ge.inv_dashboard_projection FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_inv_dashboard_projection__retention_delete ON ge.inv_dashboard_projection FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.inv_debt_case ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.inv_debt_case FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.inv_debt_case TO app_rw, app_worker;

GRANT SELECT ON ge.inv_debt_case TO app_readonly;

GRANT SELECT, DELETE ON ge.inv_debt_case TO app_retention;

CREATE POLICY rls_inv_debt_case__select ON ge.inv_debt_case FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_inv_debt_case__insert ON ge.inv_debt_case FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_inv_debt_case__update ON ge.inv_debt_case FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_inv_debt_case__retention_delete ON ge.inv_debt_case FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.inv_debt_term ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.inv_debt_term FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.inv_debt_term TO app_rw, app_worker;

GRANT SELECT ON ge.inv_debt_term TO app_readonly;

GRANT SELECT, DELETE ON ge.inv_debt_term TO app_retention;

CREATE POLICY rls_inv_debt_term__select ON ge.inv_debt_term FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_inv_debt_term__insert ON ge.inv_debt_term FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_inv_debt_term__update ON ge.inv_debt_term FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_inv_debt_term__retention_delete ON ge.inv_debt_term FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.inv_decision_action ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.inv_decision_action FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.inv_decision_action TO app_rw, app_worker;

GRANT SELECT ON ge.inv_decision_action TO app_readonly;

GRANT SELECT, DELETE ON ge.inv_decision_action TO app_retention;

CREATE POLICY rls_inv_decision_action__select ON ge.inv_decision_action FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_inv_decision_action__insert ON ge.inv_decision_action FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_inv_decision_action__update ON ge.inv_decision_action FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_inv_decision_action__retention_delete ON ge.inv_decision_action FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.inv_delivery_event ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.inv_delivery_event FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.inv_delivery_event TO app_rw, app_worker;

GRANT SELECT ON ge.inv_delivery_event TO app_readonly;

GRANT SELECT, DELETE ON ge.inv_delivery_event TO app_retention;

CREATE POLICY rls_inv_delivery_event__select ON ge.inv_delivery_event FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_inv_delivery_event__insert ON ge.inv_delivery_event FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_inv_delivery_event__update ON ge.inv_delivery_event FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_inv_delivery_event__retention_delete ON ge.inv_delivery_event FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.inv_deployment_milestone ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.inv_deployment_milestone FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.inv_deployment_milestone TO app_rw, app_worker;

GRANT SELECT ON ge.inv_deployment_milestone TO app_readonly;

GRANT SELECT, DELETE ON ge.inv_deployment_milestone TO app_retention;

CREATE POLICY rls_inv_deployment_milestone__select ON ge.inv_deployment_milestone FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_inv_deployment_milestone__insert ON ge.inv_deployment_milestone FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_inv_deployment_milestone__update ON ge.inv_deployment_milestone FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_inv_deployment_milestone__retention_delete ON ge.inv_deployment_milestone FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.inv_diligence_request ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.inv_diligence_request FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.inv_diligence_request TO app_rw, app_worker;

GRANT SELECT ON ge.inv_diligence_request TO app_readonly;

GRANT SELECT, DELETE ON ge.inv_diligence_request TO app_retention;

CREATE POLICY rls_inv_diligence_request__select ON ge.inv_diligence_request FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_inv_diligence_request__insert ON ge.inv_diligence_request FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_inv_diligence_request__update ON ge.inv_diligence_request FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_inv_diligence_request__retention_delete ON ge.inv_diligence_request FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.inv_disclosure ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.inv_disclosure FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.inv_disclosure TO app_rw, app_worker;

GRANT SELECT ON ge.inv_disclosure TO app_readonly;

GRANT SELECT, DELETE ON ge.inv_disclosure TO app_retention;

CREATE POLICY rls_inv_disclosure__select ON ge.inv_disclosure FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_inv_disclosure__insert ON ge.inv_disclosure FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_inv_disclosure__update ON ge.inv_disclosure FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_inv_disclosure__retention_delete ON ge.inv_disclosure FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.inv_document ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.inv_document FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.inv_document TO app_rw, app_worker;

GRANT SELECT ON ge.inv_document TO app_readonly;

GRANT SELECT, DELETE ON ge.inv_document TO app_retention;

CREATE POLICY rls_inv_document__select ON ge.inv_document FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_inv_document__insert ON ge.inv_document FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_inv_document__update ON ge.inv_document FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_inv_document__retention_delete ON ge.inv_document FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.inv_eligibility_check ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.inv_eligibility_check FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.inv_eligibility_check TO app_rw, app_worker;

GRANT SELECT ON ge.inv_eligibility_check TO app_readonly;

GRANT SELECT, DELETE ON ge.inv_eligibility_check TO app_retention;

CREATE POLICY rls_inv_eligibility_check__select ON ge.inv_eligibility_check FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_inv_eligibility_check__insert ON ge.inv_eligibility_check FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_inv_eligibility_check__update ON ge.inv_eligibility_check FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_inv_eligibility_check__retention_delete ON ge.inv_eligibility_check FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.inv_enrollment ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.inv_enrollment FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.inv_enrollment TO app_rw, app_worker;

GRANT SELECT ON ge.inv_enrollment TO app_readonly;

GRANT SELECT, DELETE ON ge.inv_enrollment TO app_retention;

CREATE POLICY rls_inv_enrollment__select ON ge.inv_enrollment FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_inv_enrollment__insert ON ge.inv_enrollment FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_inv_enrollment__update ON ge.inv_enrollment FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_inv_enrollment__retention_delete ON ge.inv_enrollment FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.inv_esg_commitment ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.inv_esg_commitment FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.inv_esg_commitment TO app_rw, app_worker;

GRANT SELECT ON ge.inv_esg_commitment TO app_readonly;

GRANT SELECT, DELETE ON ge.inv_esg_commitment TO app_retention;

CREATE POLICY rls_inv_esg_commitment__select ON ge.inv_esg_commitment FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_inv_esg_commitment__insert ON ge.inv_esg_commitment FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_inv_esg_commitment__update ON ge.inv_esg_commitment FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_inv_esg_commitment__retention_delete ON ge.inv_esg_commitment FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.inv_esg_disclosure ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.inv_esg_disclosure FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.inv_esg_disclosure TO app_rw, app_worker;

GRANT SELECT ON ge.inv_esg_disclosure TO app_readonly;

GRANT SELECT, DELETE ON ge.inv_esg_disclosure TO app_retention;

CREATE POLICY rls_inv_esg_disclosure__select ON ge.inv_esg_disclosure FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_inv_esg_disclosure__insert ON ge.inv_esg_disclosure FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_inv_esg_disclosure__update ON ge.inv_esg_disclosure FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_inv_esg_disclosure__retention_delete ON ge.inv_esg_disclosure FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.inv_esg_indicator ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.inv_esg_indicator FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.inv_esg_indicator TO app_rw, app_worker;

GRANT SELECT ON ge.inv_esg_indicator TO app_readonly;

GRANT SELECT, DELETE ON ge.inv_esg_indicator TO app_retention;

CREATE POLICY rls_inv_esg_indicator__select ON ge.inv_esg_indicator FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_inv_esg_indicator__insert ON ge.inv_esg_indicator FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_inv_esg_indicator__update ON ge.inv_esg_indicator FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_inv_esg_indicator__retention_delete ON ge.inv_esg_indicator FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.inv_esg_observation ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.inv_esg_observation FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.inv_esg_observation TO app_rw, app_worker;

GRANT SELECT ON ge.inv_esg_observation TO app_readonly;

GRANT SELECT, DELETE ON ge.inv_esg_observation TO app_retention;

CREATE POLICY rls_inv_esg_observation__select ON ge.inv_esg_observation FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_inv_esg_observation__insert ON ge.inv_esg_observation FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_inv_esg_observation__update ON ge.inv_esg_observation FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_inv_esg_observation__retention_delete ON ge.inv_esg_observation FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.inv_event ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.inv_event FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.inv_event TO app_rw, app_worker;

GRANT SELECT ON ge.inv_event TO app_readonly;

GRANT SELECT, DELETE ON ge.inv_event TO app_retention;

CREATE POLICY rls_inv_event__select ON ge.inv_event FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_inv_event__insert ON ge.inv_event FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_inv_event__update ON ge.inv_event FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_inv_event__retention_delete ON ge.inv_event FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.inv_evidence ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.inv_evidence FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.inv_evidence TO app_rw, app_worker;

GRANT SELECT ON ge.inv_evidence TO app_readonly;

GRANT SELECT, DELETE ON ge.inv_evidence TO app_retention;

CREATE POLICY rls_inv_evidence__select ON ge.inv_evidence FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_inv_evidence__insert ON ge.inv_evidence FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_inv_evidence__update ON ge.inv_evidence FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_inv_evidence__retention_delete ON ge.inv_evidence FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.inv_external_agent_mandate ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.inv_external_agent_mandate FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.inv_external_agent_mandate TO app_rw, app_worker;

GRANT SELECT ON ge.inv_external_agent_mandate TO app_readonly;

GRANT SELECT, DELETE ON ge.inv_external_agent_mandate TO app_retention;

CREATE POLICY rls_inv_external_agent_mandate__select ON ge.inv_external_agent_mandate FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_inv_external_agent_mandate__insert ON ge.inv_external_agent_mandate FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_inv_external_agent_mandate__update ON ge.inv_external_agent_mandate FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_inv_external_agent_mandate__retention_delete ON ge.inv_external_agent_mandate FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.inv_feedback ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.inv_feedback FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.inv_feedback TO app_rw, app_worker;

GRANT SELECT ON ge.inv_feedback TO app_readonly;

GRANT SELECT, DELETE ON ge.inv_feedback TO app_retention;

CREATE POLICY rls_inv_feedback__select ON ge.inv_feedback FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_inv_feedback__insert ON ge.inv_feedback FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_inv_feedback__update ON ge.inv_feedback FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_inv_feedback__retention_delete ON ge.inv_feedback FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.inv_filing_task ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.inv_filing_task FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.inv_filing_task TO app_rw, app_worker;

GRANT SELECT ON ge.inv_filing_task TO app_readonly;

GRANT SELECT, DELETE ON ge.inv_filing_task TO app_retention;

CREATE POLICY rls_inv_filing_task__select ON ge.inv_filing_task FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_inv_filing_task__insert ON ge.inv_filing_task FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_inv_filing_task__update ON ge.inv_filing_task FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_inv_filing_task__retention_delete ON ge.inv_filing_task FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.inv_fit_score ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.inv_fit_score FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.inv_fit_score TO app_rw, app_worker;

GRANT SELECT ON ge.inv_fit_score TO app_readonly;

GRANT SELECT, DELETE ON ge.inv_fit_score TO app_retention;

CREATE POLICY rls_inv_fit_score__select ON ge.inv_fit_score FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_inv_fit_score__insert ON ge.inv_fit_score FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_inv_fit_score__update ON ge.inv_fit_score FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_inv_fit_score__retention_delete ON ge.inv_fit_score FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.inv_funding_route ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.inv_funding_route FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.inv_funding_route TO app_rw, app_worker;

GRANT SELECT ON ge.inv_funding_route TO app_readonly;

GRANT SELECT, DELETE ON ge.inv_funding_route TO app_retention;

CREATE POLICY rls_inv_funding_route__select ON ge.inv_funding_route FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_inv_funding_route__insert ON ge.inv_funding_route FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_inv_funding_route__update ON ge.inv_funding_route FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_inv_funding_route__retention_delete ON ge.inv_funding_route FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.inv_fx_rate ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.inv_fx_rate FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT ON ge.inv_fx_rate TO app_rw, app_worker;

GRANT SELECT ON ge.inv_fx_rate TO app_readonly;

GRANT SELECT, DELETE ON ge.inv_fx_rate TO app_retention;

CREATE POLICY rls_inv_fx_rate__select ON ge.inv_fx_rate FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_inv_fx_rate__insert ON ge.inv_fx_rate FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_inv_fx_rate__retention_delete ON ge.inv_fx_rate FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.inv_grant_award ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.inv_grant_award FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.inv_grant_award TO app_rw, app_worker;

GRANT SELECT ON ge.inv_grant_award TO app_readonly;

GRANT SELECT, DELETE ON ge.inv_grant_award TO app_retention;

CREATE POLICY rls_inv_grant_award__select ON ge.inv_grant_award FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_inv_grant_award__insert ON ge.inv_grant_award FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_inv_grant_award__update ON ge.inv_grant_award FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_inv_grant_award__retention_delete ON ge.inv_grant_award FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.inv_grant_budget_line ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.inv_grant_budget_line FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.inv_grant_budget_line TO app_rw, app_worker;

GRANT SELECT ON ge.inv_grant_budget_line TO app_readonly;

GRANT SELECT, DELETE ON ge.inv_grant_budget_line TO app_retention;

CREATE POLICY rls_inv_grant_budget_line__select ON ge.inv_grant_budget_line FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_inv_grant_budget_line__insert ON ge.inv_grant_budget_line FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_inv_grant_budget_line__update ON ge.inv_grant_budget_line FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_inv_grant_budget_line__retention_delete ON ge.inv_grant_budget_line FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.inv_grant_case ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.inv_grant_case FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.inv_grant_case TO app_rw, app_worker;

GRANT SELECT ON ge.inv_grant_case TO app_readonly;

GRANT SELECT, DELETE ON ge.inv_grant_case TO app_retention;

CREATE POLICY rls_inv_grant_case__select ON ge.inv_grant_case FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_inv_grant_case__insert ON ge.inv_grant_case FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_inv_grant_case__update ON ge.inv_grant_case FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_inv_grant_case__retention_delete ON ge.inv_grant_case FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.inv_grant_criterion ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.inv_grant_criterion FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.inv_grant_criterion TO app_rw, app_worker;

GRANT SELECT ON ge.inv_grant_criterion TO app_readonly;

GRANT SELECT, DELETE ON ge.inv_grant_criterion TO app_retention;

CREATE POLICY rls_inv_grant_criterion__select ON ge.inv_grant_criterion FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_inv_grant_criterion__insert ON ge.inv_grant_criterion FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_inv_grant_criterion__update ON ge.inv_grant_criterion FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_inv_grant_criterion__retention_delete ON ge.inv_grant_criterion FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.inv_guarantee_evidence ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.inv_guarantee_evidence FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.inv_guarantee_evidence TO app_rw, app_worker;

GRANT SELECT ON ge.inv_guarantee_evidence TO app_readonly;

GRANT SELECT, DELETE ON ge.inv_guarantee_evidence TO app_retention;

CREATE POLICY rls_inv_guarantee_evidence__select ON ge.inv_guarantee_evidence FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_inv_guarantee_evidence__insert ON ge.inv_guarantee_evidence FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_inv_guarantee_evidence__update ON ge.inv_guarantee_evidence FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_inv_guarantee_evidence__retention_delete ON ge.inv_guarantee_evidence FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.inv_guard_finding ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.inv_guard_finding FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.inv_guard_finding TO app_rw, app_worker;

GRANT SELECT ON ge.inv_guard_finding TO app_readonly;

GRANT SELECT, DELETE ON ge.inv_guard_finding TO app_retention;

CREATE POLICY rls_inv_guard_finding__select ON ge.inv_guard_finding FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_inv_guard_finding__insert ON ge.inv_guard_finding FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_inv_guard_finding__update ON ge.inv_guard_finding FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_inv_guard_finding__retention_delete ON ge.inv_guard_finding FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.inv_holding ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.inv_holding FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT ON ge.inv_holding TO app_rw, app_worker;

GRANT SELECT ON ge.inv_holding TO app_readonly;

GRANT SELECT, DELETE ON ge.inv_holding TO app_retention;

CREATE POLICY rls_inv_holding__select ON ge.inv_holding FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_inv_holding__insert ON ge.inv_holding FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_inv_holding__retention_delete ON ge.inv_holding FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.inv_inbound_event ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.inv_inbound_event FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.inv_inbound_event TO app_rw, app_worker;

GRANT SELECT ON ge.inv_inbound_event TO app_readonly;

GRANT SELECT, DELETE ON ge.inv_inbound_event TO app_retention;

CREATE POLICY rls_inv_inbound_event__select ON ge.inv_inbound_event FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_inv_inbound_event__insert ON ge.inv_inbound_event FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_inv_inbound_event__update ON ge.inv_inbound_event FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_inv_inbound_event__retention_delete ON ge.inv_inbound_event FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.inv_instrument ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.inv_instrument FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT ON ge.inv_instrument TO app_rw, app_worker;

GRANT SELECT ON ge.inv_instrument TO app_readonly;

GRANT SELECT, DELETE ON ge.inv_instrument TO app_retention;

CREATE POLICY rls_inv_instrument__select ON ge.inv_instrument FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_inv_instrument__insert ON ge.inv_instrument FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_inv_instrument__retention_delete ON ge.inv_instrument FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.inv_instrument_term ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.inv_instrument_term FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT ON ge.inv_instrument_term TO app_rw, app_worker;

GRANT SELECT ON ge.inv_instrument_term TO app_readonly;

GRANT SELECT, DELETE ON ge.inv_instrument_term TO app_retention;

CREATE POLICY rls_inv_instrument_term__select ON ge.inv_instrument_term FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_inv_instrument_term__insert ON ge.inv_instrument_term FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_inv_instrument_term__retention_delete ON ge.inv_instrument_term FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.inv_integration_connection ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.inv_integration_connection FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.inv_integration_connection TO app_rw, app_worker;

GRANT SELECT ON ge.inv_integration_connection TO app_readonly;

GRANT SELECT, DELETE ON ge.inv_integration_connection TO app_retention;

CREATE POLICY rls_inv_integration_connection__select ON ge.inv_integration_connection FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_inv_integration_connection__insert ON ge.inv_integration_connection FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_inv_integration_connection__update ON ge.inv_integration_connection FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_inv_integration_connection__retention_delete ON ge.inv_integration_connection FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.inv_investor ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.inv_investor FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.inv_investor TO app_rw, app_worker;

GRANT SELECT ON ge.inv_investor TO app_readonly;

GRANT SELECT, DELETE ON ge.inv_investor TO app_retention;

CREATE POLICY rls_inv_investor__select ON ge.inv_investor FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_inv_investor__insert ON ge.inv_investor FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_inv_investor__update ON ge.inv_investor FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_inv_investor__retention_delete ON ge.inv_investor FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.inv_investor_alias ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.inv_investor_alias FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.inv_investor_alias TO app_rw, app_worker;

GRANT SELECT ON ge.inv_investor_alias TO app_readonly;

GRANT SELECT, DELETE ON ge.inv_investor_alias TO app_retention;

CREATE POLICY rls_inv_investor_alias__select ON ge.inv_investor_alias FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_inv_investor_alias__insert ON ge.inv_investor_alias FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_inv_investor_alias__update ON ge.inv_investor_alias FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_inv_investor_alias__retention_delete ON ge.inv_investor_alias FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.inv_investor_classification ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.inv_investor_classification FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.inv_investor_classification TO app_rw, app_worker;

GRANT SELECT ON ge.inv_investor_classification TO app_readonly;

GRANT SELECT, DELETE ON ge.inv_investor_classification TO app_retention;

CREATE POLICY rls_inv_investor_classification__select ON ge.inv_investor_classification FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_inv_investor_classification__insert ON ge.inv_investor_classification FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_inv_investor_classification__update ON ge.inv_investor_classification FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_inv_investor_classification__retention_delete ON ge.inv_investor_classification FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.inv_jurisdiction_policy ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.inv_jurisdiction_policy FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.inv_jurisdiction_policy TO app_rw, app_worker;

GRANT SELECT ON ge.inv_jurisdiction_policy TO app_readonly;

GRANT SELECT, DELETE ON ge.inv_jurisdiction_policy TO app_retention;

CREATE POLICY rls_inv_jurisdiction_policy__select ON ge.inv_jurisdiction_policy FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_inv_jurisdiction_policy__insert ON ge.inv_jurisdiction_policy FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_inv_jurisdiction_policy__update ON ge.inv_jurisdiction_policy FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_inv_jurisdiction_policy__retention_delete ON ge.inv_jurisdiction_policy FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.inv_kyc_case ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.inv_kyc_case FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.inv_kyc_case TO app_rw, app_worker;

GRANT SELECT ON ge.inv_kyc_case TO app_readonly;

GRANT SELECT, DELETE ON ge.inv_kyc_case TO app_retention;

CREATE POLICY rls_inv_kyc_case__select ON ge.inv_kyc_case FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_inv_kyc_case__insert ON ge.inv_kyc_case FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_inv_kyc_case__update ON ge.inv_kyc_case FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_inv_kyc_case__retention_delete ON ge.inv_kyc_case FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.inv_kyc_provider_result ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.inv_kyc_provider_result FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT ON ge.inv_kyc_provider_result TO app_rw, app_worker;

GRANT SELECT ON ge.inv_kyc_provider_result TO app_readonly;

GRANT SELECT, DELETE ON ge.inv_kyc_provider_result TO app_retention;

CREATE POLICY rls_inv_kyc_provider_result__select ON ge.inv_kyc_provider_result FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_inv_kyc_provider_result__insert ON ge.inv_kyc_provider_result FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_inv_kyc_provider_result__retention_delete ON ge.inv_kyc_provider_result FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.inv_legal_check ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.inv_legal_check FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.inv_legal_check TO app_rw, app_worker;

GRANT SELECT ON ge.inv_legal_check TO app_readonly;

GRANT SELECT, DELETE ON ge.inv_legal_check TO app_retention;

CREATE POLICY rls_inv_legal_check__select ON ge.inv_legal_check FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_inv_legal_check__insert ON ge.inv_legal_check FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_inv_legal_check__update ON ge.inv_legal_check FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_inv_legal_check__retention_delete ON ge.inv_legal_check FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.inv_locale_template ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.inv_locale_template FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.inv_locale_template TO app_rw, app_worker;

GRANT SELECT ON ge.inv_locale_template TO app_readonly;

GRANT SELECT, DELETE ON ge.inv_locale_template TO app_retention;

CREATE POLICY rls_inv_locale_template__select ON ge.inv_locale_template FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_inv_locale_template__insert ON ge.inv_locale_template FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_inv_locale_template__update ON ge.inv_locale_template FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_inv_locale_template__retention_delete ON ge.inv_locale_template FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.inv_mandate ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.inv_mandate FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.inv_mandate TO app_rw, app_worker;

GRANT SELECT ON ge.inv_mandate TO app_readonly;

GRANT SELECT, DELETE ON ge.inv_mandate TO app_retention;

CREATE POLICY rls_inv_mandate__select ON ge.inv_mandate FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_inv_mandate__insert ON ge.inv_mandate FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_inv_mandate__update ON ge.inv_mandate FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_inv_mandate__retention_delete ON ge.inv_mandate FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.inv_match_candidate ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.inv_match_candidate FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.inv_match_candidate TO app_rw, app_worker;

GRANT SELECT ON ge.inv_match_candidate TO app_readonly;

GRANT SELECT, DELETE ON ge.inv_match_candidate TO app_retention;

CREATE POLICY rls_inv_match_candidate__select ON ge.inv_match_candidate FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_inv_match_candidate__insert ON ge.inv_match_candidate FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_inv_match_candidate__update ON ge.inv_match_candidate FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_inv_match_candidate__retention_delete ON ge.inv_match_candidate FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.inv_meeting ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.inv_meeting FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.inv_meeting TO app_rw, app_worker;

GRANT SELECT ON ge.inv_meeting TO app_readonly;

GRANT SELECT, DELETE ON ge.inv_meeting TO app_retention;

CREATE POLICY rls_inv_meeting__select ON ge.inv_meeting FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_inv_meeting__insert ON ge.inv_meeting FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_inv_meeting__update ON ge.inv_meeting FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_inv_meeting__retention_delete ON ge.inv_meeting FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.inv_message ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.inv_message FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.inv_message TO app_rw, app_worker;

GRANT SELECT ON ge.inv_message TO app_readonly;

GRANT SELECT, DELETE ON ge.inv_message TO app_retention;

CREATE POLICY rls_inv_message__select ON ge.inv_message FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_inv_message__insert ON ge.inv_message FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_inv_message__update ON ge.inv_message FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_inv_message__retention_delete ON ge.inv_message FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.inv_nda ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.inv_nda FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.inv_nda TO app_rw, app_worker;

GRANT SELECT ON ge.inv_nda TO app_readonly;

GRANT SELECT, DELETE ON ge.inv_nda TO app_retention;

CREATE POLICY rls_inv_nda__select ON ge.inv_nda FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_inv_nda__insert ON ge.inv_nda FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_inv_nda__update ON ge.inv_nda FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_inv_nda__retention_delete ON ge.inv_nda FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.inv_objection ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.inv_objection FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.inv_objection TO app_rw, app_worker;

GRANT SELECT ON ge.inv_objection TO app_readonly;

GRANT SELECT, DELETE ON ge.inv_objection TO app_retention;

CREATE POLICY rls_inv_objection__select ON ge.inv_objection FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_inv_objection__insert ON ge.inv_objection FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_inv_objection__update ON ge.inv_objection FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_inv_objection__retention_delete ON ge.inv_objection FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.inv_objection_rule ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.inv_objection_rule FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.inv_objection_rule TO app_rw, app_worker;

GRANT SELECT ON ge.inv_objection_rule TO app_readonly;

GRANT SELECT, DELETE ON ge.inv_objection_rule TO app_retention;

CREATE POLICY rls_inv_objection_rule__select ON ge.inv_objection_rule FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_inv_objection_rule__insert ON ge.inv_objection_rule FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_inv_objection_rule__update ON ge.inv_objection_rule FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_inv_objection_rule__retention_delete ON ge.inv_objection_rule FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.inv_obligation ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.inv_obligation FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.inv_obligation TO app_rw, app_worker;

GRANT SELECT ON ge.inv_obligation TO app_readonly;

GRANT SELECT, DELETE ON ge.inv_obligation TO app_retention;

CREATE POLICY rls_inv_obligation__select ON ge.inv_obligation FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_inv_obligation__insert ON ge.inv_obligation FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_inv_obligation__update ON ge.inv_obligation FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_inv_obligation__retention_delete ON ge.inv_obligation FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.inv_offer ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.inv_offer FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.inv_offer TO app_rw, app_worker;

GRANT SELECT ON ge.inv_offer TO app_readonly;

GRANT SELECT, DELETE ON ge.inv_offer TO app_retention;

CREATE POLICY rls_inv_offer__select ON ge.inv_offer FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_inv_offer__insert ON ge.inv_offer FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_inv_offer__update ON ge.inv_offer FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_inv_offer__retention_delete ON ge.inv_offer FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.inv_offer_batch ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.inv_offer_batch FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.inv_offer_batch TO app_rw, app_worker;

GRANT SELECT ON ge.inv_offer_batch TO app_readonly;

GRANT SELECT, DELETE ON ge.inv_offer_batch TO app_retention;

CREATE POLICY rls_inv_offer_batch__select ON ge.inv_offer_batch FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_inv_offer_batch__insert ON ge.inv_offer_batch FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_inv_offer_batch__update ON ge.inv_offer_batch FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_inv_offer_batch__retention_delete ON ge.inv_offer_batch FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.inv_offer_counter ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.inv_offer_counter FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.inv_offer_counter TO app_rw, app_worker;

GRANT SELECT ON ge.inv_offer_counter TO app_readonly;

GRANT SELECT, DELETE ON ge.inv_offer_counter TO app_retention;

CREATE POLICY rls_inv_offer_counter__select ON ge.inv_offer_counter FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_inv_offer_counter__insert ON ge.inv_offer_counter FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_inv_offer_counter__update ON ge.inv_offer_counter FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_inv_offer_counter__retention_delete ON ge.inv_offer_counter FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.inv_offer_ledger ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.inv_offer_ledger FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT ON ge.inv_offer_ledger TO app_rw, app_worker;

GRANT SELECT ON ge.inv_offer_ledger TO app_readonly;

GRANT SELECT, DELETE ON ge.inv_offer_ledger TO app_retention;

CREATE POLICY rls_inv_offer_ledger__select ON ge.inv_offer_ledger FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_inv_offer_ledger__insert ON ge.inv_offer_ledger FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_inv_offer_ledger__retention_delete ON ge.inv_offer_ledger FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.inv_offer_recipient ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.inv_offer_recipient FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.inv_offer_recipient TO app_rw, app_worker;

GRANT SELECT ON ge.inv_offer_recipient TO app_readonly;

GRANT SELECT, DELETE ON ge.inv_offer_recipient TO app_retention;

CREATE POLICY rls_inv_offer_recipient__select ON ge.inv_offer_recipient FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_inv_offer_recipient__insert ON ge.inv_offer_recipient FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_inv_offer_recipient__update ON ge.inv_offer_recipient FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_inv_offer_recipient__retention_delete ON ge.inv_offer_recipient FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.inv_offeree ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.inv_offeree FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.inv_offeree TO app_rw, app_worker;

GRANT SELECT ON ge.inv_offeree TO app_readonly;

GRANT SELECT, DELETE ON ge.inv_offeree TO app_retention;

CREATE POLICY rls_inv_offeree__select ON ge.inv_offeree FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_inv_offeree__insert ON ge.inv_offeree FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_inv_offeree__update ON ge.inv_offeree FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_inv_offeree__retention_delete ON ge.inv_offeree FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.inv_offering ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.inv_offering FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.inv_offering TO app_rw, app_worker;

GRANT SELECT ON ge.inv_offering TO app_readonly;

GRANT SELECT, DELETE ON ge.inv_offering TO app_retention;

CREATE POLICY rls_inv_offering__select ON ge.inv_offering FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_inv_offering__insert ON ge.inv_offering FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_inv_offering__update ON ge.inv_offering FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_inv_offering__retention_delete ON ge.inv_offering FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.inv_opportunity ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.inv_opportunity FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.inv_opportunity TO app_rw, app_worker;

GRANT SELECT ON ge.inv_opportunity TO app_readonly;

GRANT SELECT, DELETE ON ge.inv_opportunity TO app_retention;

CREATE POLICY rls_inv_opportunity__select ON ge.inv_opportunity FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_inv_opportunity__insert ON ge.inv_opportunity FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_inv_opportunity__update ON ge.inv_opportunity FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_inv_opportunity__retention_delete ON ge.inv_opportunity FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.inv_option_grant ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.inv_option_grant FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT ON ge.inv_option_grant TO app_rw, app_worker;

GRANT SELECT ON ge.inv_option_grant TO app_readonly;

GRANT SELECT, DELETE ON ge.inv_option_grant TO app_retention;

CREATE POLICY rls_inv_option_grant__select ON ge.inv_option_grant FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_inv_option_grant__insert ON ge.inv_option_grant FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_inv_option_grant__retention_delete ON ge.inv_option_grant FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.inv_outbox ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.inv_outbox FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.inv_outbox TO app_rw, app_worker;

GRANT SELECT ON ge.inv_outbox TO app_readonly;

GRANT SELECT, DELETE ON ge.inv_outbox TO app_retention;

CREATE POLICY rls_inv_outbox__select ON ge.inv_outbox FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_inv_outbox__insert ON ge.inv_outbox FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_inv_outbox__update ON ge.inv_outbox FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_inv_outbox__retention_delete ON ge.inv_outbox FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.inv_outreach_reservation ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.inv_outreach_reservation FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.inv_outreach_reservation TO app_rw, app_worker;

GRANT SELECT ON ge.inv_outreach_reservation TO app_readonly;

GRANT SELECT, DELETE ON ge.inv_outreach_reservation TO app_retention;

CREATE POLICY rls_inv_outreach_reservation__select ON ge.inv_outreach_reservation FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_inv_outreach_reservation__insert ON ge.inv_outreach_reservation FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_inv_outreach_reservation__update ON ge.inv_outreach_reservation FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_inv_outreach_reservation__retention_delete ON ge.inv_outreach_reservation FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.inv_payment_instruction ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.inv_payment_instruction FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.inv_payment_instruction TO app_rw, app_worker;

GRANT SELECT ON ge.inv_payment_instruction TO app_readonly;

GRANT SELECT, DELETE ON ge.inv_payment_instruction TO app_retention;

CREATE POLICY rls_inv_payment_instruction__select ON ge.inv_payment_instruction FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_inv_payment_instruction__insert ON ge.inv_payment_instruction FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_inv_payment_instruction__update ON ge.inv_payment_instruction FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_inv_payment_instruction__retention_delete ON ge.inv_payment_instruction FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.inv_permission ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.inv_permission FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.inv_permission TO app_rw, app_worker;

GRANT SELECT ON ge.inv_permission TO app_readonly;

GRANT SELECT, DELETE ON ge.inv_permission TO app_retention;

CREATE POLICY rls_inv_permission__select ON ge.inv_permission FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_inv_permission__insert ON ge.inv_permission FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_inv_permission__update ON ge.inv_permission FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_inv_permission__retention_delete ON ge.inv_permission FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.inv_promotion_review ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.inv_promotion_review FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.inv_promotion_review TO app_rw, app_worker;

GRANT SELECT ON ge.inv_promotion_review TO app_readonly;

GRANT SELECT, DELETE ON ge.inv_promotion_review TO app_retention;

CREATE POLICY rls_inv_promotion_review__select ON ge.inv_promotion_review FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_inv_promotion_review__insert ON ge.inv_promotion_review FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_inv_promotion_review__update ON ge.inv_promotion_review FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_inv_promotion_review__retention_delete ON ge.inv_promotion_review FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.inv_readiness_score ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.inv_readiness_score FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.inv_readiness_score TO app_rw, app_worker;

GRANT SELECT ON ge.inv_readiness_score TO app_readonly;

GRANT SELECT, DELETE ON ge.inv_readiness_score TO app_retention;

CREATE POLICY rls_inv_readiness_score__select ON ge.inv_readiness_score FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_inv_readiness_score__insert ON ge.inv_readiness_score FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_inv_readiness_score__update ON ge.inv_readiness_score FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_inv_readiness_score__retention_delete ON ge.inv_readiness_score FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.inv_readiness_snapshot ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.inv_readiness_snapshot FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.inv_readiness_snapshot TO app_rw, app_worker;

GRANT SELECT ON ge.inv_readiness_snapshot TO app_readonly;

GRANT SELECT, DELETE ON ge.inv_readiness_snapshot TO app_retention;

CREATE POLICY rls_inv_readiness_snapshot__select ON ge.inv_readiness_snapshot FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_inv_readiness_snapshot__insert ON ge.inv_readiness_snapshot FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_inv_readiness_snapshot__update ON ge.inv_readiness_snapshot FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_inv_readiness_snapshot__retention_delete ON ge.inv_readiness_snapshot FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.inv_receipt ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.inv_receipt FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT ON ge.inv_receipt TO app_rw, app_worker;

GRANT SELECT ON ge.inv_receipt TO app_readonly;

GRANT SELECT, DELETE ON ge.inv_receipt TO app_retention;

CREATE POLICY rls_inv_receipt__select ON ge.inv_receipt FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_inv_receipt__insert ON ge.inv_receipt FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_inv_receipt__retention_delete ON ge.inv_receipt FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.inv_receipt_allocation ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.inv_receipt_allocation FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT ON ge.inv_receipt_allocation TO app_rw, app_worker;

GRANT SELECT ON ge.inv_receipt_allocation TO app_readonly;

GRANT SELECT, DELETE ON ge.inv_receipt_allocation TO app_retention;

CREATE POLICY rls_inv_receipt_allocation__select ON ge.inv_receipt_allocation FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_inv_receipt_allocation__insert ON ge.inv_receipt_allocation FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_inv_receipt_allocation__retention_delete ON ge.inv_receipt_allocation FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.inv_referral ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.inv_referral FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.inv_referral TO app_rw, app_worker;

GRANT SELECT ON ge.inv_referral TO app_readonly;

GRANT SELECT, DELETE ON ge.inv_referral TO app_retention;

CREATE POLICY rls_inv_referral__select ON ge.inv_referral FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_inv_referral__insert ON ge.inv_referral FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_inv_referral__update ON ge.inv_referral FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_inv_referral__retention_delete ON ge.inv_referral FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.inv_refund ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.inv_refund FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT ON ge.inv_refund TO app_rw, app_worker;

GRANT SELECT ON ge.inv_refund TO app_readonly;

GRANT SELECT, DELETE ON ge.inv_refund TO app_retention;

CREATE POLICY rls_inv_refund__select ON ge.inv_refund FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_inv_refund__insert ON ge.inv_refund FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_inv_refund__retention_delete ON ge.inv_refund FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.inv_regulatory_deadline ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.inv_regulatory_deadline FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.inv_regulatory_deadline TO app_rw, app_worker;

GRANT SELECT ON ge.inv_regulatory_deadline TO app_readonly;

GRANT SELECT, DELETE ON ge.inv_regulatory_deadline TO app_retention;

CREATE POLICY rls_inv_regulatory_deadline__select ON ge.inv_regulatory_deadline FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_inv_regulatory_deadline__insert ON ge.inv_regulatory_deadline FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_inv_regulatory_deadline__update ON ge.inv_regulatory_deadline FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_inv_regulatory_deadline__retention_delete ON ge.inv_regulatory_deadline FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.inv_relationship ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.inv_relationship FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.inv_relationship TO app_rw, app_worker;

GRANT SELECT ON ge.inv_relationship TO app_readonly;

GRANT SELECT, DELETE ON ge.inv_relationship TO app_retention;

CREATE POLICY rls_inv_relationship__select ON ge.inv_relationship FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_inv_relationship__insert ON ge.inv_relationship FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_inv_relationship__update ON ge.inv_relationship FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_inv_relationship__retention_delete ON ge.inv_relationship FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.inv_relationship_provenance ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.inv_relationship_provenance FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.inv_relationship_provenance TO app_rw, app_worker;

GRANT SELECT ON ge.inv_relationship_provenance TO app_readonly;

GRANT SELECT, DELETE ON ge.inv_relationship_provenance TO app_retention;

CREATE POLICY rls_inv_relationship_provenance__select ON ge.inv_relationship_provenance FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_inv_relationship_provenance__insert ON ge.inv_relationship_provenance FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_inv_relationship_provenance__update ON ge.inv_relationship_provenance FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_inv_relationship_provenance__retention_delete ON ge.inv_relationship_provenance FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.inv_repayment_schedule ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.inv_repayment_schedule FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.inv_repayment_schedule TO app_rw, app_worker;

GRANT SELECT ON ge.inv_repayment_schedule TO app_readonly;

GRANT SELECT, DELETE ON ge.inv_repayment_schedule TO app_retention;

CREATE POLICY rls_inv_repayment_schedule__select ON ge.inv_repayment_schedule FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_inv_repayment_schedule__insert ON ge.inv_repayment_schedule FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_inv_repayment_schedule__update ON ge.inv_repayment_schedule FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_inv_repayment_schedule__retention_delete ON ge.inv_repayment_schedule FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.inv_resolution ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.inv_resolution FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.inv_resolution TO app_rw, app_worker;

GRANT SELECT ON ge.inv_resolution TO app_readonly;

GRANT SELECT, DELETE ON ge.inv_resolution TO app_retention;

CREATE POLICY rls_inv_resolution__select ON ge.inv_resolution FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_inv_resolution__insert ON ge.inv_resolution FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_inv_resolution__update ON ge.inv_resolution FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_inv_resolution__retention_delete ON ge.inv_resolution FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.inv_room ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.inv_room FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.inv_room TO app_rw, app_worker;

GRANT SELECT ON ge.inv_room TO app_readonly;

GRANT SELECT, DELETE ON ge.inv_room TO app_retention;

CREATE POLICY rls_inv_room__select ON ge.inv_room FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_inv_room__insert ON ge.inv_room FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_inv_room__update ON ge.inv_room FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_inv_room__retention_delete ON ge.inv_room FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.inv_room_item ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.inv_room_item FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.inv_room_item TO app_rw, app_worker;

GRANT SELECT ON ge.inv_room_item TO app_readonly;

GRANT SELECT, DELETE ON ge.inv_room_item TO app_retention;

CREATE POLICY rls_inv_room_item__select ON ge.inv_room_item FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_inv_room_item__insert ON ge.inv_room_item FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_inv_room_item__update ON ge.inv_room_item FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_inv_room_item__retention_delete ON ge.inv_room_item FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.inv_round ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.inv_round FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.inv_round TO app_rw, app_worker;

GRANT SELECT ON ge.inv_round TO app_readonly;

GRANT SELECT, DELETE ON ge.inv_round TO app_retention;

CREATE POLICY rls_inv_round__select ON ge.inv_round FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_inv_round__insert ON ge.inv_round FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_inv_round__update ON ge.inv_round FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_inv_round__retention_delete ON ge.inv_round FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.inv_rulepack_activation ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.inv_rulepack_activation FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.inv_rulepack_activation TO app_rw, app_worker;

GRANT SELECT ON ge.inv_rulepack_activation TO app_readonly;

GRANT SELECT, DELETE ON ge.inv_rulepack_activation TO app_retention;

CREATE POLICY rls_inv_rulepack_activation__select ON ge.inv_rulepack_activation FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_inv_rulepack_activation__insert ON ge.inv_rulepack_activation FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_inv_rulepack_activation__update ON ge.inv_rulepack_activation FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_inv_rulepack_activation__retention_delete ON ge.inv_rulepack_activation FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.inv_runway_scenario ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.inv_runway_scenario FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.inv_runway_scenario TO app_rw, app_worker;

GRANT SELECT ON ge.inv_runway_scenario TO app_readonly;

GRANT SELECT, DELETE ON ge.inv_runway_scenario TO app_retention;

CREATE POLICY rls_inv_runway_scenario__select ON ge.inv_runway_scenario FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_inv_runway_scenario__insert ON ge.inv_runway_scenario FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_inv_runway_scenario__update ON ge.inv_runway_scenario FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_inv_runway_scenario__retention_delete ON ge.inv_runway_scenario FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.inv_scenario ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.inv_scenario FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.inv_scenario TO app_rw, app_worker;

GRANT SELECT ON ge.inv_scenario TO app_readonly;

GRANT SELECT, DELETE ON ge.inv_scenario TO app_retention;

CREATE POLICY rls_inv_scenario__select ON ge.inv_scenario FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_inv_scenario__insert ON ge.inv_scenario FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_inv_scenario__update ON ge.inv_scenario FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_inv_scenario__retention_delete ON ge.inv_scenario FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.inv_screening_hit ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.inv_screening_hit FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.inv_screening_hit TO app_rw, app_worker;

GRANT SELECT ON ge.inv_screening_hit TO app_readonly;

GRANT SELECT, DELETE ON ge.inv_screening_hit TO app_retention;

CREATE POLICY rls_inv_screening_hit__select ON ge.inv_screening_hit FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_inv_screening_hit__insert ON ge.inv_screening_hit FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_inv_screening_hit__update ON ge.inv_screening_hit FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_inv_screening_hit__retention_delete ON ge.inv_screening_hit FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.inv_search_plan ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.inv_search_plan FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.inv_search_plan TO app_rw, app_worker;

GRANT SELECT ON ge.inv_search_plan TO app_readonly;

GRANT SELECT, DELETE ON ge.inv_search_plan TO app_retention;

CREATE POLICY rls_inv_search_plan__select ON ge.inv_search_plan FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_inv_search_plan__insert ON ge.inv_search_plan FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_inv_search_plan__update ON ge.inv_search_plan FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_inv_search_plan__retention_delete ON ge.inv_search_plan FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.inv_search_run ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.inv_search_run FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.inv_search_run TO app_rw, app_worker;

GRANT SELECT ON ge.inv_search_run TO app_readonly;

GRANT SELECT, DELETE ON ge.inv_search_run TO app_retention;

CREATE POLICY rls_inv_search_run__select ON ge.inv_search_run FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_inv_search_run__insert ON ge.inv_search_run FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_inv_search_run__update ON ge.inv_search_run FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_inv_search_run__retention_delete ON ge.inv_search_run FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.inv_sequence ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.inv_sequence FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.inv_sequence TO app_rw, app_worker;

GRANT SELECT ON ge.inv_sequence TO app_readonly;

GRANT SELECT, DELETE ON ge.inv_sequence TO app_retention;

CREATE POLICY rls_inv_sequence__select ON ge.inv_sequence FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_inv_sequence__insert ON ge.inv_sequence FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_inv_sequence__update ON ge.inv_sequence FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_inv_sequence__retention_delete ON ge.inv_sequence FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.inv_shareholder ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.inv_shareholder FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT ON ge.inv_shareholder TO app_rw, app_worker;

GRANT SELECT ON ge.inv_shareholder TO app_readonly;

GRANT SELECT, DELETE ON ge.inv_shareholder TO app_retention;

CREATE POLICY rls_inv_shareholder__select ON ge.inv_shareholder FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_inv_shareholder__insert ON ge.inv_shareholder FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_inv_shareholder__retention_delete ON ge.inv_shareholder FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.inv_source ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.inv_source FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.inv_source TO app_rw, app_worker;

GRANT SELECT ON ge.inv_source TO app_readonly;

GRANT SELECT, DELETE ON ge.inv_source TO app_retention;

CREATE POLICY rls_inv_source__select ON ge.inv_source FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_inv_source__insert ON ge.inv_source FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_inv_source__update ON ge.inv_source FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_inv_source__retention_delete ON ge.inv_source FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.inv_source_policy ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.inv_source_policy FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.inv_source_policy TO app_rw, app_worker;

GRANT SELECT ON ge.inv_source_policy TO app_readonly;

GRANT SELECT, DELETE ON ge.inv_source_policy TO app_retention;

CREATE POLICY rls_inv_source_policy__select ON ge.inv_source_policy FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_inv_source_policy__insert ON ge.inv_source_policy FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_inv_source_policy__update ON ge.inv_source_policy FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_inv_source_policy__retention_delete ON ge.inv_source_policy FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.inv_stage_event ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.inv_stage_event FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.inv_stage_event TO app_rw, app_worker;

GRANT SELECT ON ge.inv_stage_event TO app_readonly;

GRANT SELECT, DELETE ON ge.inv_stage_event TO app_retention;

CREATE POLICY rls_inv_stage_event__select ON ge.inv_stage_event FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_inv_stage_event__insert ON ge.inv_stage_event FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_inv_stage_event__update ON ge.inv_stage_event FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_inv_stage_event__retention_delete ON ge.inv_stage_event FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.inv_suppression ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.inv_suppression FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.inv_suppression TO app_rw, app_worker;

GRANT SELECT ON ge.inv_suppression TO app_readonly;

GRANT SELECT, DELETE ON ge.inv_suppression TO app_retention;

CREATE POLICY rls_inv_suppression__select ON ge.inv_suppression FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_inv_suppression__insert ON ge.inv_suppression FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_inv_suppression__update ON ge.inv_suppression FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_inv_suppression__retention_delete ON ge.inv_suppression FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.inv_task ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.inv_task FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.inv_task TO app_rw, app_worker;

GRANT SELECT ON ge.inv_task TO app_readonly;

GRANT SELECT, DELETE ON ge.inv_task TO app_retention;

CREATE POLICY rls_inv_task__select ON ge.inv_task FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_inv_task__insert ON ge.inv_task FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_inv_task__update ON ge.inv_task FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_inv_task__retention_delete ON ge.inv_task FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.inv_term_version ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.inv_term_version FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.inv_term_version TO app_rw, app_worker;

GRANT SELECT ON ge.inv_term_version TO app_readonly;

GRANT SELECT, DELETE ON ge.inv_term_version TO app_retention;

CREATE POLICY rls_inv_term_version__select ON ge.inv_term_version FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_inv_term_version__insert ON ge.inv_term_version FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_inv_term_version__update ON ge.inv_term_version FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_inv_term_version__retention_delete ON ge.inv_term_version FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.inv_thread ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.inv_thread FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.inv_thread TO app_rw, app_worker;

GRANT SELECT ON ge.inv_thread TO app_readonly;

GRANT SELECT, DELETE ON ge.inv_thread TO app_retention;

CREATE POLICY rls_inv_thread__select ON ge.inv_thread FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_inv_thread__insert ON ge.inv_thread FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_inv_thread__update ON ge.inv_thread FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_inv_thread__retention_delete ON ge.inv_thread FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.inv_update ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.inv_update FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.inv_update TO app_rw, app_worker;

GRANT SELECT ON ge.inv_update TO app_readonly;

GRANT SELECT, DELETE ON ge.inv_update TO app_retention;

CREATE POLICY rls_inv_update__select ON ge.inv_update FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_inv_update__insert ON ge.inv_update FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_inv_update__update ON ge.inv_update FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_inv_update__retention_delete ON ge.inv_update FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.inv_verification_case ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.inv_verification_case FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.inv_verification_case TO app_rw, app_worker;

GRANT SELECT ON ge.inv_verification_case TO app_readonly;

GRANT SELECT, DELETE ON ge.inv_verification_case TO app_retention;

CREATE POLICY rls_inv_verification_case__select ON ge.inv_verification_case FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_inv_verification_case__insert ON ge.inv_verification_case FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_inv_verification_case__update ON ge.inv_verification_case FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_inv_verification_case__retention_delete ON ge.inv_verification_case FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.inv_vote ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.inv_vote FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT ON ge.inv_vote TO app_rw, app_worker;

GRANT SELECT ON ge.inv_vote TO app_readonly;

GRANT SELECT, DELETE ON ge.inv_vote TO app_retention;

CREATE POLICY rls_inv_vote__select ON ge.inv_vote FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_inv_vote__insert ON ge.inv_vote FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_inv_vote__retention_delete ON ge.inv_vote FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.inv_webhook_endpoint ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.inv_webhook_endpoint FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.inv_webhook_endpoint TO app_rw, app_worker;

GRANT SELECT ON ge.inv_webhook_endpoint TO app_readonly;

GRANT SELECT, DELETE ON ge.inv_webhook_endpoint TO app_retention;

CREATE POLICY rls_inv_webhook_endpoint__select ON ge.inv_webhook_endpoint FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_inv_webhook_endpoint__insert ON ge.inv_webhook_endpoint FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_inv_webhook_endpoint__update ON ge.inv_webhook_endpoint FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_inv_webhook_endpoint__retention_delete ON ge.inv_webhook_endpoint FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.inv_workflow_run ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.inv_workflow_run FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.inv_workflow_run TO app_rw, app_worker;

GRANT SELECT ON ge.inv_workflow_run TO app_readonly;

GRANT SELECT, DELETE ON ge.inv_workflow_run TO app_retention;

CREATE POLICY rls_inv_workflow_run__select ON ge.inv_workflow_run FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_inv_workflow_run__insert ON ge.inv_workflow_run FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_inv_workflow_run__update ON ge.inv_workflow_run FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_inv_workflow_run__retention_delete ON ge.inv_workflow_run FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.invoice ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.invoice FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.invoice TO app_rw, app_worker;

GRANT SELECT ON ge.invoice TO app_readonly;

GRANT SELECT, DELETE ON ge.invoice TO app_retention;

ALTER TABLE ge.journey_event ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.journey_event FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.journey_event TO app_rw, app_worker;

GRANT SELECT ON ge.journey_event TO app_readonly;

GRANT SELECT, DELETE ON ge.journey_event TO app_retention;

GRANT SELECT ON ge.jurisdiction_pack TO app_rw, app_worker, app_readonly;

GRANT SELECT, INSERT, UPDATE ON ge.jurisdiction_pack TO app_platform_sec;

GRANT SELECT ON ge.jurisdiction_rule TO app_rw, app_worker, app_readonly;

GRANT SELECT, INSERT, UPDATE ON ge.jurisdiction_rule TO app_platform_sec;

ALTER TABLE ge.kill_switch ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.kill_switch FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.kill_switch TO app_rw, app_worker;

GRANT SELECT ON ge.kill_switch TO app_readonly;

GRANT SELECT, DELETE ON ge.kill_switch TO app_retention;

CREATE POLICY rls_kill_switch__select ON ge.kill_switch FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_kill_switch__insert ON ge.kill_switch FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_kill_switch__update ON ge.kill_switch FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_kill_switch__retention_delete ON ge.kill_switch FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.kill_switch_event ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.kill_switch_event FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.kill_switch_event TO app_rw, app_worker;

GRANT SELECT ON ge.kill_switch_event TO app_readonly;

GRANT SELECT, DELETE ON ge.kill_switch_event TO app_retention;

CREATE POLICY rls_kill_switch_event__select ON ge.kill_switch_event FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_kill_switch_event__insert ON ge.kill_switch_event FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_kill_switch_event__update ON ge.kill_switch_event FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_kill_switch_event__retention_delete ON ge.kill_switch_event FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.lcy_account_metric ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.lcy_account_metric FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT ON ge.lcy_account_metric TO app_rw, app_worker;

GRANT SELECT ON ge.lcy_account_metric TO app_readonly;

GRANT SELECT, DELETE ON ge.lcy_account_metric TO app_retention;

CREATE POLICY rls_lcy_account_metric__select ON ge.lcy_account_metric FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_lcy_account_metric__insert ON ge.lcy_account_metric FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_lcy_account_metric__retention_delete ON ge.lcy_account_metric FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.lcy_customer_subscription ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.lcy_customer_subscription FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.lcy_customer_subscription TO app_rw, app_worker;

GRANT SELECT ON ge.lcy_customer_subscription TO app_readonly;

GRANT SELECT, DELETE ON ge.lcy_customer_subscription TO app_retention;

CREATE POLICY rls_lcy_customer_subscription__select ON ge.lcy_customer_subscription FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_lcy_customer_subscription__insert ON ge.lcy_customer_subscription FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_lcy_customer_subscription__update ON ge.lcy_customer_subscription FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_lcy_customer_subscription__retention_delete ON ge.lcy_customer_subscription FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.lcy_deployment ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.lcy_deployment FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.lcy_deployment TO app_rw, app_worker;

GRANT SELECT ON ge.lcy_deployment TO app_readonly;

GRANT SELECT, DELETE ON ge.lcy_deployment TO app_retention;

CREATE POLICY rls_lcy_deployment__select ON ge.lcy_deployment FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_lcy_deployment__insert ON ge.lcy_deployment FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_lcy_deployment__update ON ge.lcy_deployment FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_lcy_deployment__retention_delete ON ge.lcy_deployment FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.lcy_feedback ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.lcy_feedback FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT ON ge.lcy_feedback TO app_rw, app_worker;

GRANT SELECT ON ge.lcy_feedback TO app_readonly;

GRANT SELECT, DELETE ON ge.lcy_feedback TO app_retention;

CREATE POLICY rls_lcy_feedback__select ON ge.lcy_feedback FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_lcy_feedback__insert ON ge.lcy_feedback FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_lcy_feedback__retention_delete ON ge.lcy_feedback FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.lcy_handoff ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.lcy_handoff FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT ON ge.lcy_handoff TO app_rw, app_worker;

GRANT SELECT ON ge.lcy_handoff TO app_readonly;

GRANT SELECT, DELETE ON ge.lcy_handoff TO app_retention;

CREATE POLICY rls_lcy_handoff__select ON ge.lcy_handoff FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_lcy_handoff__insert ON ge.lcy_handoff FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_lcy_handoff__retention_delete ON ge.lcy_handoff FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.lcy_integration_deal ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.lcy_integration_deal FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.lcy_integration_deal TO app_rw, app_worker;

GRANT SELECT ON ge.lcy_integration_deal TO app_readonly;

GRANT SELECT, DELETE ON ge.lcy_integration_deal TO app_retention;

CREATE POLICY rls_lcy_integration_deal__select ON ge.lcy_integration_deal FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_lcy_integration_deal__insert ON ge.lcy_integration_deal FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_lcy_integration_deal__update ON ge.lcy_integration_deal FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_lcy_integration_deal__retention_delete ON ge.lcy_integration_deal FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.lcy_onboarding ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.lcy_onboarding FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.lcy_onboarding TO app_rw, app_worker;

GRANT SELECT ON ge.lcy_onboarding TO app_readonly;

GRANT SELECT, DELETE ON ge.lcy_onboarding TO app_retention;

CREATE POLICY rls_lcy_onboarding__select ON ge.lcy_onboarding FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_lcy_onboarding__insert ON ge.lcy_onboarding FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_lcy_onboarding__update ON ge.lcy_onboarding FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_lcy_onboarding__retention_delete ON ge.lcy_onboarding FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

CREATE POLICY rls_lcy_onboarding__portal_select ON ge.lcy_onboarding FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND (SELECT ge.app_actor_kind()) = 'portal' AND EXISTS (
  SELECT 1 FROM ge.ten_portal_grant g WHERE g.tenant_id = lcy_onboarding.tenant_id AND g.object_type = 'onboarding' AND g.object_id = lcy_onboarding.id
  AND g.subject_user_id = (SELECT ge.app_actor_id()) AND g.revoked_at IS NULL AND (g.expires_at IS NULL OR g.expires_at > now())));

ALTER TABLE ge.lcy_onboarding_task ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.lcy_onboarding_task FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.lcy_onboarding_task TO app_rw, app_worker;

GRANT SELECT ON ge.lcy_onboarding_task TO app_readonly;

GRANT SELECT, DELETE ON ge.lcy_onboarding_task TO app_retention;

CREATE POLICY rls_lcy_onboarding_task__select ON ge.lcy_onboarding_task FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_lcy_onboarding_task__insert ON ge.lcy_onboarding_task FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_lcy_onboarding_task__update ON ge.lcy_onboarding_task FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_lcy_onboarding_task__retention_delete ON ge.lcy_onboarding_task FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.lcy_outcome ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.lcy_outcome FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT ON ge.lcy_outcome TO app_rw, app_worker;

GRANT SELECT ON ge.lcy_outcome TO app_readonly;

GRANT SELECT, DELETE ON ge.lcy_outcome TO app_retention;

CREATE POLICY rls_lcy_outcome__select ON ge.lcy_outcome FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_lcy_outcome__insert ON ge.lcy_outcome FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_lcy_outcome__retention_delete ON ge.lcy_outcome FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.lcy_partner ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.lcy_partner FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.lcy_partner TO app_rw, app_worker;

GRANT SELECT ON ge.lcy_partner TO app_readonly;

GRANT SELECT, DELETE ON ge.lcy_partner TO app_retention;

CREATE POLICY rls_lcy_partner__select ON ge.lcy_partner FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_lcy_partner__insert ON ge.lcy_partner FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_lcy_partner__update ON ge.lcy_partner FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_lcy_partner__retention_delete ON ge.lcy_partner FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.lcy_pilot ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.lcy_pilot FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.lcy_pilot TO app_rw, app_worker;

GRANT SELECT ON ge.lcy_pilot TO app_readonly;

GRANT SELECT, DELETE ON ge.lcy_pilot TO app_retention;

CREATE POLICY rls_lcy_pilot__select ON ge.lcy_pilot FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_lcy_pilot__insert ON ge.lcy_pilot FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_lcy_pilot__update ON ge.lcy_pilot FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_lcy_pilot__retention_delete ON ge.lcy_pilot FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.lcy_renewal ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.lcy_renewal FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.lcy_renewal TO app_rw, app_worker;

GRANT SELECT ON ge.lcy_renewal TO app_readonly;

GRANT SELECT, DELETE ON ge.lcy_renewal TO app_retention;

CREATE POLICY rls_lcy_renewal__select ON ge.lcy_renewal FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_lcy_renewal__insert ON ge.lcy_renewal FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_lcy_renewal__update ON ge.lcy_renewal FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_lcy_renewal__retention_delete ON ge.lcy_renewal FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

CREATE POLICY rls_lcy_renewal__portal_select ON ge.lcy_renewal FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND (SELECT ge.app_actor_kind()) = 'portal' AND EXISTS (
  SELECT 1 FROM ge.ten_portal_grant g WHERE g.tenant_id = lcy_renewal.tenant_id AND g.object_type = 'renewal' AND g.object_id = lcy_renewal.id
  AND g.subject_user_id = (SELECT ge.app_actor_id()) AND g.revoked_at IS NULL AND (g.expires_at IS NULL OR g.expires_at > now())));

ALTER TABLE ge.lcy_task ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.lcy_task FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.lcy_task TO app_rw, app_worker;

GRANT SELECT ON ge.lcy_task TO app_readonly;

GRANT SELECT, DELETE ON ge.lcy_task TO app_retention;

CREATE POLICY rls_lcy_task__select ON ge.lcy_task FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_lcy_task__insert ON ge.lcy_task FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_lcy_task__update ON ge.lcy_task FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_lcy_task__retention_delete ON ge.lcy_task FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.ledger_entry ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.ledger_entry FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.ledger_entry TO app_rw, app_worker;

GRANT SELECT ON ge.ledger_entry TO app_readonly;

GRANT SELECT, DELETE ON ge.ledger_entry TO app_retention;

CREATE POLICY rls_ledger_entry__select ON ge.ledger_entry FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_ledger_entry__insert ON ge.ledger_entry FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_ledger_entry__update ON ge.ledger_entry FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_ledger_entry__retention_delete ON ge.ledger_entry FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

GRANT SELECT ON ge.locale_bundle TO app_rw, app_worker, app_readonly;

ALTER TABLE ge.mandate ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.mandate FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.mandate TO app_rw, app_worker;

GRANT SELECT ON ge.mandate TO app_readonly;

GRANT SELECT, DELETE ON ge.mandate TO app_retention;

CREATE POLICY rls_mandate__select ON ge.mandate FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_mandate__insert ON ge.mandate FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_mandate__update ON ge.mandate FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_mandate__retention_delete ON ge.mandate FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.mandate_approval ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.mandate_approval FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.mandate_approval TO app_rw, app_worker;

GRANT SELECT ON ge.mandate_approval TO app_readonly;

GRANT SELECT, DELETE ON ge.mandate_approval TO app_retention;

CREATE POLICY rls_mandate_approval__select ON ge.mandate_approval FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_mandate_approval__insert ON ge.mandate_approval FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_mandate_approval__update ON ge.mandate_approval FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_mandate_approval__retention_delete ON ge.mandate_approval FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.mandate_consumption ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.mandate_consumption FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.mandate_consumption TO app_rw, app_worker;

GRANT SELECT ON ge.mandate_consumption TO app_readonly;

GRANT SELECT, DELETE ON ge.mandate_consumption TO app_retention;

CREATE POLICY rls_mandate_consumption__select ON ge.mandate_consumption FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_mandate_consumption__insert ON ge.mandate_consumption FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_mandate_consumption__update ON ge.mandate_consumption FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_mandate_consumption__retention_delete ON ge.mandate_consumption FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.mandate_counter ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.mandate_counter FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.mandate_counter TO app_rw, app_worker;

GRANT SELECT ON ge.mandate_counter TO app_readonly;

GRANT SELECT, DELETE ON ge.mandate_counter TO app_retention;

CREATE POLICY rls_mandate_counter__select ON ge.mandate_counter FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_mandate_counter__insert ON ge.mandate_counter FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_mandate_counter__update ON ge.mandate_counter FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_mandate_counter__retention_delete ON ge.mandate_counter FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.mandate_decision ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.mandate_decision FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.mandate_decision TO app_rw, app_worker;

GRANT SELECT ON ge.mandate_decision TO app_readonly;

GRANT SELECT, DELETE ON ge.mandate_decision TO app_retention;

CREATE POLICY rls_mandate_decision__select ON ge.mandate_decision FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_mandate_decision__insert ON ge.mandate_decision FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_mandate_decision__update ON ge.mandate_decision FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_mandate_decision__retention_delete ON ge.mandate_decision FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.mandate_limit ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.mandate_limit FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.mandate_limit TO app_rw, app_worker;

GRANT SELECT ON ge.mandate_limit TO app_readonly;

GRANT SELECT, DELETE ON ge.mandate_limit TO app_retention;

CREATE POLICY rls_mandate_limit__select ON ge.mandate_limit FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_mandate_limit__insert ON ge.mandate_limit FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_mandate_limit__update ON ge.mandate_limit FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_mandate_limit__retention_delete ON ge.mandate_limit FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.mandate_restriction ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.mandate_restriction FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.mandate_restriction TO app_rw, app_worker;

GRANT SELECT ON ge.mandate_restriction TO app_readonly;

GRANT SELECT, DELETE ON ge.mandate_restriction TO app_retention;

CREATE POLICY rls_mandate_restriction__select ON ge.mandate_restriction FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_mandate_restriction__insert ON ge.mandate_restriction FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_mandate_restriction__update ON ge.mandate_restriction FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_mandate_restriction__retention_delete ON ge.mandate_restriction FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.mandate_scope_item ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.mandate_scope_item FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.mandate_scope_item TO app_rw, app_worker;

GRANT SELECT ON ge.mandate_scope_item TO app_readonly;

GRANT SELECT, DELETE ON ge.mandate_scope_item TO app_retention;

CREATE POLICY rls_mandate_scope_item__select ON ge.mandate_scope_item FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_mandate_scope_item__insert ON ge.mandate_scope_item FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_mandate_scope_item__update ON ge.mandate_scope_item FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_mandate_scope_item__retention_delete ON ge.mandate_scope_item FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.mandate_version ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.mandate_version FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.mandate_version TO app_rw, app_worker;

GRANT SELECT ON ge.mandate_version TO app_readonly;

GRANT SELECT, DELETE ON ge.mandate_version TO app_retention;

CREATE POLICY rls_mandate_version__select ON ge.mandate_version FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_mandate_version__insert ON ge.mandate_version FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_mandate_version__update ON ge.mandate_version FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_mandate_version__retention_delete ON ge.mandate_version FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.mandate_window ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.mandate_window FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.mandate_window TO app_rw, app_worker;

GRANT SELECT ON ge.mandate_window TO app_readonly;

GRANT SELECT, DELETE ON ge.mandate_window TO app_retention;

CREATE POLICY rls_mandate_window__select ON ge.mandate_window FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_mandate_window__insert ON ge.mandate_window FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_mandate_window__update ON ge.mandate_window FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_mandate_window__retention_delete ON ge.mandate_window FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.market ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.market FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.market TO app_rw, app_worker;

GRANT SELECT ON ge.market TO app_readonly;

GRANT SELECT, DELETE ON ge.market TO app_retention;

ALTER TABLE ge.metric_aggregate ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.metric_aggregate FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.metric_aggregate TO app_rw, app_worker;

GRANT SELECT ON ge.metric_aggregate TO app_readonly;

GRANT SELECT, DELETE ON ge.metric_aggregate TO app_retention;

GRANT SELECT ON ge.metric_definition TO app_rw, app_worker, app_readonly;

ALTER TABLE ge.mkt_ad_campaign ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.mkt_ad_campaign FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.mkt_ad_campaign TO app_rw, app_worker;

GRANT SELECT ON ge.mkt_ad_campaign TO app_readonly;

GRANT SELECT, DELETE ON ge.mkt_ad_campaign TO app_retention;

CREATE POLICY rls_mkt_ad_campaign__select ON ge.mkt_ad_campaign FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_mkt_ad_campaign__insert ON ge.mkt_ad_campaign FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_mkt_ad_campaign__update ON ge.mkt_ad_campaign FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_mkt_ad_campaign__retention_delete ON ge.mkt_ad_campaign FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.mkt_attendance ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.mkt_attendance FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT ON ge.mkt_attendance TO app_rw, app_worker;

GRANT SELECT ON ge.mkt_attendance TO app_readonly;

GRANT SELECT, DELETE ON ge.mkt_attendance TO app_retention;

CREATE POLICY rls_mkt_attendance__select ON ge.mkt_attendance FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_mkt_attendance__insert ON ge.mkt_attendance FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_mkt_attendance__retention_delete ON ge.mkt_attendance FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.mkt_attribution_event ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.mkt_attribution_event FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT ON ge.mkt_attribution_event TO app_rw, app_worker;

GRANT SELECT ON ge.mkt_attribution_event TO app_readonly;

GRANT SELECT, DELETE ON ge.mkt_attribution_event TO app_retention;

CREATE POLICY rls_mkt_attribution_event__select ON ge.mkt_attribution_event FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_mkt_attribution_event__insert ON ge.mkt_attribution_event FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_mkt_attribution_event__retention_delete ON ge.mkt_attribution_event FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.mkt_audience ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.mkt_audience FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.mkt_audience TO app_rw, app_worker;

GRANT SELECT ON ge.mkt_audience TO app_readonly;

GRANT SELECT, DELETE ON ge.mkt_audience TO app_retention;

CREATE POLICY rls_mkt_audience__select ON ge.mkt_audience FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_mkt_audience__insert ON ge.mkt_audience FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_mkt_audience__update ON ge.mkt_audience FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_mkt_audience__retention_delete ON ge.mkt_audience FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.mkt_audience_member ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.mkt_audience_member FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.mkt_audience_member TO app_rw, app_worker;

GRANT SELECT ON ge.mkt_audience_member TO app_readonly;

GRANT SELECT, DELETE ON ge.mkt_audience_member TO app_retention;

CREATE POLICY rls_mkt_audience_member__select ON ge.mkt_audience_member FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_mkt_audience_member__insert ON ge.mkt_audience_member FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_mkt_audience_member__update ON ge.mkt_audience_member FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_mkt_audience_member__retention_delete ON ge.mkt_audience_member FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.mkt_campaign ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.mkt_campaign FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.mkt_campaign TO app_rw, app_worker;

GRANT SELECT ON ge.mkt_campaign TO app_readonly;

GRANT SELECT, DELETE ON ge.mkt_campaign TO app_retention;

CREATE POLICY rls_mkt_campaign__select ON ge.mkt_campaign FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_mkt_campaign__insert ON ge.mkt_campaign FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_mkt_campaign__update ON ge.mkt_campaign FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_mkt_campaign__retention_delete ON ge.mkt_campaign FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.mkt_campaign_version ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.mkt_campaign_version FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.mkt_campaign_version TO app_rw, app_worker;

GRANT SELECT ON ge.mkt_campaign_version TO app_readonly;

GRANT SELECT, DELETE ON ge.mkt_campaign_version TO app_retention;

CREATE POLICY rls_mkt_campaign_version__select ON ge.mkt_campaign_version FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_mkt_campaign_version__insert ON ge.mkt_campaign_version FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_mkt_campaign_version__update ON ge.mkt_campaign_version FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_mkt_campaign_version__retention_delete ON ge.mkt_campaign_version FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.mkt_content_asset ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.mkt_content_asset FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.mkt_content_asset TO app_rw, app_worker;

GRANT SELECT ON ge.mkt_content_asset TO app_readonly;

GRANT SELECT, DELETE ON ge.mkt_content_asset TO app_retention;

CREATE POLICY rls_mkt_content_asset__select ON ge.mkt_content_asset FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_mkt_content_asset__insert ON ge.mkt_content_asset FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_mkt_content_asset__update ON ge.mkt_content_asset FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_mkt_content_asset__retention_delete ON ge.mkt_content_asset FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.mkt_content_claim ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.mkt_content_claim FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.mkt_content_claim TO app_rw, app_worker;

GRANT SELECT ON ge.mkt_content_claim TO app_readonly;

GRANT SELECT, DELETE ON ge.mkt_content_claim TO app_retention;

CREATE POLICY rls_mkt_content_claim__select ON ge.mkt_content_claim FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_mkt_content_claim__insert ON ge.mkt_content_claim FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_mkt_content_claim__update ON ge.mkt_content_claim FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_mkt_content_claim__retention_delete ON ge.mkt_content_claim FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.mkt_content_version ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.mkt_content_version FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.mkt_content_version TO app_rw, app_worker;

GRANT SELECT ON ge.mkt_content_version TO app_readonly;

GRANT SELECT, DELETE ON ge.mkt_content_version TO app_retention;

CREATE POLICY rls_mkt_content_version__select ON ge.mkt_content_version FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_mkt_content_version__insert ON ge.mkt_content_version FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_mkt_content_version__update ON ge.mkt_content_version FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_mkt_content_version__retention_delete ON ge.mkt_content_version FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.mkt_event ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.mkt_event FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.mkt_event TO app_rw, app_worker;

GRANT SELECT ON ge.mkt_event TO app_readonly;

GRANT SELECT, DELETE ON ge.mkt_event TO app_retention;

CREATE POLICY rls_mkt_event__select ON ge.mkt_event FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_mkt_event__insert ON ge.mkt_event FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_mkt_event__update ON ge.mkt_event FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_mkt_event__retention_delete ON ge.mkt_event FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.mkt_keyword ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.mkt_keyword FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.mkt_keyword TO app_rw, app_worker;

GRANT SELECT ON ge.mkt_keyword TO app_readonly;

GRANT SELECT, DELETE ON ge.mkt_keyword TO app_retention;

CREATE POLICY rls_mkt_keyword__select ON ge.mkt_keyword FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_mkt_keyword__insert ON ge.mkt_keyword FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_mkt_keyword__update ON ge.mkt_keyword FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_mkt_keyword__retention_delete ON ge.mkt_keyword FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.mkt_landing_page ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.mkt_landing_page FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.mkt_landing_page TO app_rw, app_worker;

GRANT SELECT ON ge.mkt_landing_page TO app_readonly;

GRANT SELECT, DELETE ON ge.mkt_landing_page TO app_retention;

CREATE POLICY rls_mkt_landing_page__select ON ge.mkt_landing_page FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_mkt_landing_page__insert ON ge.mkt_landing_page FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_mkt_landing_page__update ON ge.mkt_landing_page FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_mkt_landing_page__retention_delete ON ge.mkt_landing_page FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.mkt_page_metric ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.mkt_page_metric FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT ON ge.mkt_page_metric TO app_rw, app_worker;

GRANT SELECT ON ge.mkt_page_metric TO app_readonly;

GRANT SELECT, DELETE ON ge.mkt_page_metric TO app_retention;

CREATE POLICY rls_mkt_page_metric__select ON ge.mkt_page_metric FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_mkt_page_metric__insert ON ge.mkt_page_metric FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_mkt_page_metric__retention_delete ON ge.mkt_page_metric FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.mkt_preview_grant ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.mkt_preview_grant FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.mkt_preview_grant TO app_rw, app_worker;

GRANT SELECT ON ge.mkt_preview_grant TO app_readonly;

GRANT SELECT, DELETE ON ge.mkt_preview_grant TO app_retention;

CREATE POLICY rls_mkt_preview_grant__select ON ge.mkt_preview_grant FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_mkt_preview_grant__insert ON ge.mkt_preview_grant FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_mkt_preview_grant__update ON ge.mkt_preview_grant FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_mkt_preview_grant__retention_delete ON ge.mkt_preview_grant FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.mkt_publication ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.mkt_publication FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.mkt_publication TO app_rw, app_worker;

GRANT SELECT ON ge.mkt_publication TO app_readonly;

GRANT SELECT, DELETE ON ge.mkt_publication TO app_retention;

CREATE POLICY rls_mkt_publication__select ON ge.mkt_publication FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_mkt_publication__insert ON ge.mkt_publication FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_mkt_publication__update ON ge.mkt_publication FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_mkt_publication__retention_delete ON ge.mkt_publication FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.mkt_publication_snapshot ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.mkt_publication_snapshot FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT ON ge.mkt_publication_snapshot TO app_rw, app_worker;

GRANT SELECT ON ge.mkt_publication_snapshot TO app_readonly;

GRANT SELECT, DELETE ON ge.mkt_publication_snapshot TO app_retention;

CREATE POLICY rls_mkt_publication_snapshot__select ON ge.mkt_publication_snapshot FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_mkt_publication_snapshot__insert ON ge.mkt_publication_snapshot FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_mkt_publication_snapshot__retention_delete ON ge.mkt_publication_snapshot FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.mkt_referral ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.mkt_referral FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.mkt_referral TO app_rw, app_worker;

GRANT SELECT ON ge.mkt_referral TO app_readonly;

GRANT SELECT, DELETE ON ge.mkt_referral TO app_retention;

CREATE POLICY rls_mkt_referral__select ON ge.mkt_referral FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_mkt_referral__insert ON ge.mkt_referral FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_mkt_referral__update ON ge.mkt_referral FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_mkt_referral__retention_delete ON ge.mkt_referral FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.mkt_registration ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.mkt_registration FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.mkt_registration TO app_rw, app_worker;

GRANT SELECT ON ge.mkt_registration TO app_readonly;

GRANT SELECT, DELETE ON ge.mkt_registration TO app_retention;

CREATE POLICY rls_mkt_registration__select ON ge.mkt_registration FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_mkt_registration__insert ON ge.mkt_registration FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_mkt_registration__update ON ge.mkt_registration FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_mkt_registration__retention_delete ON ge.mkt_registration FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.mkt_seo_issue ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.mkt_seo_issue FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.mkt_seo_issue TO app_rw, app_worker;

GRANT SELECT ON ge.mkt_seo_issue TO app_readonly;

GRANT SELECT, DELETE ON ge.mkt_seo_issue TO app_retention;

CREATE POLICY rls_mkt_seo_issue__select ON ge.mkt_seo_issue FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_mkt_seo_issue__insert ON ge.mkt_seo_issue FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_mkt_seo_issue__update ON ge.mkt_seo_issue FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_mkt_seo_issue__retention_delete ON ge.mkt_seo_issue FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.mkt_social_publication ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.mkt_social_publication FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.mkt_social_publication TO app_rw, app_worker;

GRANT SELECT ON ge.mkt_social_publication TO app_readonly;

GRANT SELECT, DELETE ON ge.mkt_social_publication TO app_retention;

CREATE POLICY rls_mkt_social_publication__select ON ge.mkt_social_publication FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_mkt_social_publication__insert ON ge.mkt_social_publication FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_mkt_social_publication__update ON ge.mkt_social_publication FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_mkt_social_publication__retention_delete ON ge.mkt_social_publication FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.mkt_spend_event ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.mkt_spend_event FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT ON ge.mkt_spend_event TO app_rw, app_worker;

GRANT SELECT ON ge.mkt_spend_event TO app_readonly;

GRANT SELECT, DELETE ON ge.mkt_spend_event TO app_retention;

CREATE POLICY rls_mkt_spend_event__select ON ge.mkt_spend_event FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_mkt_spend_event__insert ON ge.mkt_spend_event FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_mkt_spend_event__retention_delete ON ge.mkt_spend_event FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.negotiation_session ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.negotiation_session FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.negotiation_session TO app_rw, app_worker;

GRANT SELECT ON ge.negotiation_session TO app_readonly;

GRANT SELECT, DELETE ON ge.negotiation_session TO app_retention;

CREATE POLICY rls_negotiation_session__select ON ge.negotiation_session FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_negotiation_session__insert ON ge.negotiation_session FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_negotiation_session__update ON ge.negotiation_session FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_negotiation_session__retention_delete ON ge.negotiation_session FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.negotiation_step ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.negotiation_step FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.negotiation_step TO app_rw, app_worker;

GRANT SELECT ON ge.negotiation_step TO app_readonly;

GRANT SELECT, DELETE ON ge.negotiation_step TO app_retention;

CREATE POLICY rls_negotiation_step__select ON ge.negotiation_step FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_negotiation_step__insert ON ge.negotiation_step FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_negotiation_step__update ON ge.negotiation_step FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_negotiation_step__retention_delete ON ge.negotiation_step FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.oauth_client ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.oauth_client FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.oauth_client TO app_rw, app_worker;

GRANT SELECT ON ge.oauth_client TO app_readonly;

GRANT SELECT, DELETE ON ge.oauth_client TO app_retention;

CREATE POLICY rls_oauth_client__select ON ge.oauth_client FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()));

CREATE POLICY rls_oauth_client__insert ON ge.oauth_client FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()));

CREATE POLICY rls_oauth_client__update ON ge.oauth_client FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()));

CREATE POLICY rls_oauth_client__retention_delete ON ge.oauth_client FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

GRANT SELECT ON ge.oauth_jti_seen TO app_rw, app_worker, app_readonly;

GRANT INSERT ON ge.oauth_jti_seen TO app_worker;

ALTER TABLE ge.offering ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.offering FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.offering TO app_rw, app_worker;

GRANT SELECT ON ge.offering TO app_readonly;

GRANT SELECT, DELETE ON ge.offering TO app_retention;

ALTER TABLE ge.offering_market ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.offering_market FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.offering_market TO app_rw, app_worker;

GRANT SELECT ON ge.offering_market TO app_readonly;

GRANT SELECT, DELETE ON ge.offering_market TO app_retention;

ALTER TABLE ge.ops_domain_event ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.ops_domain_event FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT ON ge.ops_domain_event TO app_rw, app_worker;

GRANT SELECT ON ge.ops_domain_event TO app_readonly;

GRANT SELECT, DELETE ON ge.ops_domain_event TO app_retention;

CREATE POLICY rls_ops_domain_event__select ON ge.ops_domain_event FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_ops_domain_event__insert ON ge.ops_domain_event FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_ops_domain_event__retention_delete ON ge.ops_domain_event FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.ops_idempotency_key ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.ops_idempotency_key FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.ops_idempotency_key TO app_rw, app_worker;

GRANT SELECT ON ge.ops_idempotency_key TO app_readonly;

GRANT SELECT, DELETE ON ge.ops_idempotency_key TO app_retention;

CREATE POLICY rls_ops_idempotency_key__select ON ge.ops_idempotency_key FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_ops_idempotency_key__insert ON ge.ops_idempotency_key FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_ops_idempotency_key__update ON ge.ops_idempotency_key FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_ops_idempotency_key__retention_delete ON ge.ops_idempotency_key FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

GRANT SELECT ON ge.ops_incident TO app_rw, app_worker, app_readonly;

GRANT SELECT, INSERT, UPDATE ON ge.ops_incident TO app_platform_sec;

ALTER TABLE ge.ops_job_run ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.ops_job_run FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.ops_job_run TO app_rw, app_worker;

GRANT SELECT ON ge.ops_job_run TO app_readonly;

GRANT SELECT, DELETE ON ge.ops_job_run TO app_retention;

CREATE POLICY rls_ops_job_run__select ON ge.ops_job_run FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND (startup_id IS NULL OR startup_id = ANY ((SELECT ge.app_company_ids())::uuid[])));

CREATE POLICY rls_ops_job_run__insert ON ge.ops_job_run FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND (startup_id = (SELECT ge.app_write_company()) OR (startup_id IS NULL AND (SELECT ge.app_actor_kind()) IN ('internal','service'))));

CREATE POLICY rls_ops_job_run__update ON ge.ops_job_run FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND (startup_id = (SELECT ge.app_write_company()) OR (startup_id IS NULL AND (SELECT ge.app_actor_kind()) IN ('internal','service')))) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND (startup_id = (SELECT ge.app_write_company()) OR (startup_id IS NULL AND (SELECT ge.app_actor_kind()) IN ('internal','service'))));

CREATE POLICY rls_ops_job_run__retention_delete ON ge.ops_job_run FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.ops_notification ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.ops_notification FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.ops_notification TO app_rw, app_worker;

GRANT SELECT ON ge.ops_notification TO app_readonly;

GRANT SELECT, DELETE ON ge.ops_notification TO app_retention;

CREATE POLICY rls_ops_notification__select ON ge.ops_notification FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_ops_notification__insert ON ge.ops_notification FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_ops_notification__update ON ge.ops_notification FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_ops_notification__retention_delete ON ge.ops_notification FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.ops_notification_preference ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.ops_notification_preference FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.ops_notification_preference TO app_rw, app_worker;

GRANT SELECT ON ge.ops_notification_preference TO app_readonly;

GRANT SELECT, DELETE ON ge.ops_notification_preference TO app_retention;

CREATE POLICY rls_ops_notification_preference__select ON ge.ops_notification_preference FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND (startup_id IS NULL OR startup_id = ANY ((SELECT ge.app_company_ids())::uuid[])));

CREATE POLICY rls_ops_notification_preference__insert ON ge.ops_notification_preference FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND (startup_id = (SELECT ge.app_write_company()) OR (startup_id IS NULL AND (SELECT ge.app_actor_kind()) IN ('internal','service'))));

CREATE POLICY rls_ops_notification_preference__update ON ge.ops_notification_preference FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND (startup_id = (SELECT ge.app_write_company()) OR (startup_id IS NULL AND (SELECT ge.app_actor_kind()) IN ('internal','service')))) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND (startup_id = (SELECT ge.app_write_company()) OR (startup_id IS NULL AND (SELECT ge.app_actor_kind()) IN ('internal','service'))));

CREATE POLICY rls_ops_notification_preference__retention_delete ON ge.ops_notification_preference FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

GRANT SELECT ON ge.ops_release TO app_rw, app_worker, app_readonly;

GRANT SELECT ON ge.ops_test_run TO app_rw, app_worker, app_readonly;

ALTER TABLE ge.organization ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.organization FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.organization TO app_rw, app_worker;

GRANT SELECT ON ge.organization TO app_readonly;

GRANT SELECT, DELETE ON ge.organization TO app_retention;

ALTER TABLE ge.outbox ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.outbox FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.outbox TO app_rw, app_worker;

GRANT SELECT ON ge.outbox TO app_readonly;

GRANT SELECT, DELETE ON ge.outbox TO app_retention;

ALTER TABLE ge.payment_mandate ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.payment_mandate FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.payment_mandate TO app_rw, app_worker;

GRANT SELECT ON ge.payment_mandate TO app_readonly;

GRANT SELECT, DELETE ON ge.payment_mandate TO app_retention;

CREATE POLICY rls_payment_mandate__select ON ge.payment_mandate FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_payment_mandate__insert ON ge.payment_mandate FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_payment_mandate__update ON ge.payment_mandate FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_payment_mandate__retention_delete ON ge.payment_mandate FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.payment_txn ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.payment_txn FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.payment_txn TO app_rw, app_worker;

GRANT SELECT ON ge.payment_txn TO app_readonly;

GRANT SELECT, DELETE ON ge.payment_txn TO app_retention;

CREATE POLICY rls_payment_txn__select ON ge.payment_txn FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_payment_txn__insert ON ge.payment_txn FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_payment_txn__update ON ge.payment_txn FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_payment_txn__retention_delete ON ge.payment_txn FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

GRANT SELECT ON ge.permission_catalogue TO app_rw, app_worker, app_readonly;

GRANT SELECT, INSERT, UPDATE ON ge.permission_catalogue TO app_registry;

GRANT SELECT ON ge.platform_table_allowlist TO app_rw, app_worker, app_readonly;

ALTER TABLE ge.portal_profile ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.portal_profile FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.portal_profile TO app_rw, app_worker;

GRANT SELECT ON ge.portal_profile TO app_readonly;

GRANT SELECT, DELETE ON ge.portal_profile TO app_retention;

CREATE POLICY rls_portal_profile__select ON ge.portal_profile FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_portal_profile__insert ON ge.portal_profile FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_portal_profile__update ON ge.portal_profile FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_portal_profile__retention_delete ON ge.portal_profile FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.portfolio_grant ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.portfolio_grant FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.portfolio_grant TO app_rw, app_worker;

GRANT SELECT ON ge.portfolio_grant TO app_readonly;

GRANT SELECT, DELETE ON ge.portfolio_grant TO app_retention;

GRANT SELECT ON ge.prompt_version TO app_rw, app_worker, app_readonly;

GRANT SELECT, INSERT, UPDATE ON ge.prompt_version TO app_registry;

ALTER TABLE ge.recon_break ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.recon_break FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.recon_break TO app_rw, app_worker;

GRANT SELECT ON ge.recon_break TO app_readonly;

GRANT SELECT, DELETE ON ge.recon_break TO app_retention;

CREATE POLICY rls_recon_break__select ON ge.recon_break FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_recon_break__insert ON ge.recon_break FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_recon_break__update ON ge.recon_break FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_recon_break__retention_delete ON ge.recon_break FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.recon_run ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.recon_run FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.recon_run TO app_rw, app_worker;

GRANT SELECT ON ge.recon_run TO app_readonly;

GRANT SELECT, DELETE ON ge.recon_run TO app_retention;

CREATE POLICY rls_recon_run__select ON ge.recon_run FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_recon_run__insert ON ge.recon_run FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_recon_run__update ON ge.recon_run FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_recon_run__retention_delete ON ge.recon_run FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

GRANT SELECT ON ge.recovery_path TO app_rw, app_worker, app_readonly;

GRANT SELECT ON ge.ref_country TO app_rw, app_worker, app_readonly;

GRANT SELECT ON ge.ref_currency TO app_rw, app_worker, app_readonly;

ALTER TABLE ge.ref_dataset ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.ref_dataset FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.ref_dataset TO app_rw, app_worker;

GRANT SELECT ON ge.ref_dataset TO app_readonly;

GRANT SELECT, DELETE ON ge.ref_dataset TO app_retention;

CREATE POLICY rls_ref_dataset__select ON ge.ref_dataset FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND (startup_id IS NULL OR startup_id = ANY ((SELECT ge.app_company_ids())::uuid[])));

CREATE POLICY rls_ref_dataset__insert ON ge.ref_dataset FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND (startup_id = (SELECT ge.app_write_company()) OR (startup_id IS NULL AND (SELECT ge.app_actor_kind()) IN ('internal','service'))));

CREATE POLICY rls_ref_dataset__update ON ge.ref_dataset FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND (startup_id = (SELECT ge.app_write_company()) OR (startup_id IS NULL AND (SELECT ge.app_actor_kind()) IN ('internal','service')))) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND (startup_id = (SELECT ge.app_write_company()) OR (startup_id IS NULL AND (SELECT ge.app_actor_kind()) IN ('internal','service'))));

CREATE POLICY rls_ref_dataset__retention_delete ON ge.ref_dataset FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.ref_unit ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.ref_unit FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.ref_unit TO app_rw, app_worker;

GRANT SELECT ON ge.ref_unit TO app_readonly;

GRANT SELECT, DELETE ON ge.ref_unit TO app_retention;

CREATE POLICY rls_ref_unit__select ON ge.ref_unit FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND (startup_id IS NULL OR startup_id = ANY ((SELECT ge.app_company_ids())::uuid[])));

CREATE POLICY rls_ref_unit__insert ON ge.ref_unit FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND (startup_id = (SELECT ge.app_write_company()) OR (startup_id IS NULL AND (SELECT ge.app_actor_kind()) IN ('internal','service'))));

CREATE POLICY rls_ref_unit__update ON ge.ref_unit FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND (startup_id = (SELECT ge.app_write_company()) OR (startup_id IS NULL AND (SELECT ge.app_actor_kind()) IN ('internal','service')))) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND (startup_id = (SELECT ge.app_write_company()) OR (startup_id IS NULL AND (SELECT ge.app_actor_kind()) IN ('internal','service'))));

CREATE POLICY rls_ref_unit__retention_delete ON ge.ref_unit FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.ref_value ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.ref_value FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.ref_value TO app_rw, app_worker;

GRANT SELECT ON ge.ref_value TO app_readonly;

GRANT SELECT, DELETE ON ge.ref_value TO app_retention;

CREATE POLICY rls_ref_value__select ON ge.ref_value FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND (startup_id IS NULL OR startup_id = ANY ((SELECT ge.app_company_ids())::uuid[])));

CREATE POLICY rls_ref_value__insert ON ge.ref_value FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND (startup_id = (SELECT ge.app_write_company()) OR (startup_id IS NULL AND (SELECT ge.app_actor_kind()) IN ('internal','service'))));

CREATE POLICY rls_ref_value__update ON ge.ref_value FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND (startup_id = (SELECT ge.app_write_company()) OR (startup_id IS NULL AND (SELECT ge.app_actor_kind()) IN ('internal','service')))) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND (startup_id = (SELECT ge.app_write_company()) OR (startup_id IS NULL AND (SELECT ge.app_actor_kind()) IN ('internal','service'))));

CREATE POLICY rls_ref_value__retention_delete ON ge.ref_value FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.refund ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.refund FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.refund TO app_rw, app_worker;

GRANT SELECT ON ge.refund TO app_readonly;

GRANT SELECT, DELETE ON ge.refund TO app_retention;

CREATE POLICY rls_refund__select ON ge.refund FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_refund__insert ON ge.refund FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_refund__update ON ge.refund FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_refund__retention_delete ON ge.refund FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

GRANT SELECT ON ge.restore_drill TO app_rw, app_worker, app_readonly;

GRANT INSERT ON ge.restore_drill TO app_worker;

ALTER TABLE ge.role_permission ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.role_permission FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.role_permission TO app_rw, app_worker;

GRANT SELECT ON ge.role_permission TO app_readonly;

GRANT SELECT, DELETE ON ge.role_permission TO app_retention;

GRANT SELECT ON ge.rpo_sample TO app_rw, app_worker, app_readonly;

GRANT INSERT ON ge.rpo_sample TO app_worker;

GRANT SELECT ON ge.rulepack_requirement TO app_rw, app_worker, app_readonly;

GRANT SELECT ON ge.saas_application_draft TO app_rw, app_worker, app_readonly;

ALTER TABLE ge.saas_credit ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.saas_credit FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT ON ge.saas_credit TO app_rw, app_worker;

GRANT SELECT ON ge.saas_credit TO app_readonly;

GRANT SELECT, DELETE ON ge.saas_credit TO app_retention;

CREATE POLICY rls_saas_credit__select ON ge.saas_credit FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND (startup_id IS NULL OR startup_id = ANY ((SELECT ge.app_company_ids())::uuid[])));

CREATE POLICY rls_saas_credit__insert ON ge.saas_credit FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND (startup_id = (SELECT ge.app_write_company()) OR (startup_id IS NULL AND (SELECT ge.app_actor_kind()) IN ('internal','service'))));

CREATE POLICY rls_saas_credit__retention_delete ON ge.saas_credit FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.saas_entitlement ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.saas_entitlement FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.saas_entitlement TO app_rw, app_worker;

GRANT SELECT ON ge.saas_entitlement TO app_readonly;

GRANT SELECT, DELETE ON ge.saas_entitlement TO app_retention;

CREATE POLICY rls_saas_entitlement__select ON ge.saas_entitlement FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND (startup_id IS NULL OR startup_id = ANY ((SELECT ge.app_company_ids())::uuid[])));

CREATE POLICY rls_saas_entitlement__insert ON ge.saas_entitlement FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND (startup_id = (SELECT ge.app_write_company()) OR (startup_id IS NULL AND (SELECT ge.app_actor_kind()) IN ('internal','service'))));

CREATE POLICY rls_saas_entitlement__update ON ge.saas_entitlement FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND (startup_id = (SELECT ge.app_write_company()) OR (startup_id IS NULL AND (SELECT ge.app_actor_kind()) IN ('internal','service')))) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND (startup_id = (SELECT ge.app_write_company()) OR (startup_id IS NULL AND (SELECT ge.app_actor_kind()) IN ('internal','service'))));

CREATE POLICY rls_saas_entitlement__retention_delete ON ge.saas_entitlement FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.saas_import_job ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.saas_import_job FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.saas_import_job TO app_rw, app_worker;

GRANT SELECT ON ge.saas_import_job TO app_readonly;

GRANT SELECT, DELETE ON ge.saas_import_job TO app_retention;

CREATE POLICY rls_saas_import_job__select ON ge.saas_import_job FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_saas_import_job__insert ON ge.saas_import_job FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_saas_import_job__update ON ge.saas_import_job FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_saas_import_job__retention_delete ON ge.saas_import_job FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

GRANT SELECT ON ge.saas_plan TO app_rw, app_worker, app_readonly;

ALTER TABLE ge.saas_plan_entitlement ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.saas_plan_entitlement FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.saas_plan_entitlement TO app_rw, app_worker;

GRANT SELECT ON ge.saas_plan_entitlement TO app_readonly;

GRANT SELECT, DELETE ON ge.saas_plan_entitlement TO app_retention;

CREATE POLICY rls_saas_plan_entitlement__select ON ge.saas_plan_entitlement FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_saas_plan_entitlement__insert ON ge.saas_plan_entitlement FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_saas_plan_entitlement__update ON ge.saas_plan_entitlement FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_saas_plan_entitlement__retention_delete ON ge.saas_plan_entitlement FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

GRANT SELECT ON ge.saas_plan_version TO app_rw, app_worker, app_readonly;

ALTER TABLE ge.saas_service_invoice_line ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.saas_service_invoice_line FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.saas_service_invoice_line TO app_rw, app_worker;

GRANT SELECT ON ge.saas_service_invoice_line TO app_readonly;

GRANT SELECT, DELETE ON ge.saas_service_invoice_line TO app_retention;

CREATE POLICY rls_saas_service_invoice_line__select ON ge.saas_service_invoice_line FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND (startup_id IS NULL OR startup_id = ANY ((SELECT ge.app_company_ids())::uuid[])));

CREATE POLICY rls_saas_service_invoice_line__insert ON ge.saas_service_invoice_line FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND (startup_id = (SELECT ge.app_write_company()) OR (startup_id IS NULL AND (SELECT ge.app_actor_kind()) IN ('internal','service'))));

CREATE POLICY rls_saas_service_invoice_line__update ON ge.saas_service_invoice_line FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND (startup_id = (SELECT ge.app_write_company()) OR (startup_id IS NULL AND (SELECT ge.app_actor_kind()) IN ('internal','service')))) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND (startup_id = (SELECT ge.app_write_company()) OR (startup_id IS NULL AND (SELECT ge.app_actor_kind()) IN ('internal','service'))));

CREATE POLICY rls_saas_service_invoice_line__retention_delete ON ge.saas_service_invoice_line FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.saas_service_request ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.saas_service_request FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.saas_service_request TO app_rw, app_worker;

GRANT SELECT ON ge.saas_service_request TO app_readonly;

GRANT SELECT, DELETE ON ge.saas_service_request TO app_retention;

CREATE POLICY rls_saas_service_request__select ON ge.saas_service_request FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND (startup_id IS NULL OR startup_id = ANY ((SELECT ge.app_company_ids())::uuid[])));

CREATE POLICY rls_saas_service_request__insert ON ge.saas_service_request FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND (startup_id = (SELECT ge.app_write_company()) OR (startup_id IS NULL AND (SELECT ge.app_actor_kind()) IN ('internal','service'))));

CREATE POLICY rls_saas_service_request__update ON ge.saas_service_request FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND (startup_id = (SELECT ge.app_write_company()) OR (startup_id IS NULL AND (SELECT ge.app_actor_kind()) IN ('internal','service')))) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND (startup_id = (SELECT ge.app_write_company()) OR (startup_id IS NULL AND (SELECT ge.app_actor_kind()) IN ('internal','service'))));

CREATE POLICY rls_saas_service_request__retention_delete ON ge.saas_service_request FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

CREATE POLICY rls_saas_service_request__portal_select ON ge.saas_service_request FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND (SELECT ge.app_actor_kind()) = 'portal' AND EXISTS (
  SELECT 1 FROM ge.ten_portal_grant g WHERE g.tenant_id = saas_service_request.tenant_id AND g.object_type = 'ticket' AND g.object_id = saas_service_request.id
  AND g.subject_user_id = (SELECT ge.app_actor_id()) AND g.revoked_at IS NULL AND (g.expires_at IS NULL OR g.expires_at > now())));

ALTER TABLE ge.saas_subscription ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.saas_subscription FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.saas_subscription TO app_rw, app_worker;

GRANT SELECT ON ge.saas_subscription TO app_readonly;

GRANT SELECT, DELETE ON ge.saas_subscription TO app_retention;

CREATE POLICY rls_saas_subscription__select ON ge.saas_subscription FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND (startup_id IS NULL OR startup_id = ANY ((SELECT ge.app_company_ids())::uuid[])));

CREATE POLICY rls_saas_subscription__insert ON ge.saas_subscription FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND (startup_id = (SELECT ge.app_write_company()) OR (startup_id IS NULL AND (SELECT ge.app_actor_kind()) IN ('internal','service'))));

CREATE POLICY rls_saas_subscription__update ON ge.saas_subscription FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND (startup_id = (SELECT ge.app_write_company()) OR (startup_id IS NULL AND (SELECT ge.app_actor_kind()) IN ('internal','service')))) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND (startup_id = (SELECT ge.app_write_company()) OR (startup_id IS NULL AND (SELECT ge.app_actor_kind()) IN ('internal','service'))));

CREATE POLICY rls_saas_subscription__retention_delete ON ge.saas_subscription FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.saas_support_access_grant ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.saas_support_access_grant FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.saas_support_access_grant TO app_rw, app_worker;

GRANT SELECT ON ge.saas_support_access_grant TO app_readonly;

GRANT SELECT, DELETE ON ge.saas_support_access_grant TO app_retention;

CREATE POLICY rls_saas_support_access_grant__select ON ge.saas_support_access_grant FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND (startup_id IS NULL OR startup_id = ANY ((SELECT ge.app_company_ids())::uuid[])));

CREATE POLICY rls_saas_support_access_grant__insert ON ge.saas_support_access_grant FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND (startup_id = (SELECT ge.app_write_company()) OR (startup_id IS NULL AND (SELECT ge.app_actor_kind()) IN ('internal','service'))));

CREATE POLICY rls_saas_support_access_grant__update ON ge.saas_support_access_grant FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND (startup_id = (SELECT ge.app_write_company()) OR (startup_id IS NULL AND (SELECT ge.app_actor_kind()) IN ('internal','service')))) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND (startup_id = (SELECT ge.app_write_company()) OR (startup_id IS NULL AND (SELECT ge.app_actor_kind()) IN ('internal','service'))));

CREATE POLICY rls_saas_support_access_grant__retention_delete ON ge.saas_support_access_grant FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.saas_usage_meter_reading ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.saas_usage_meter_reading FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT ON ge.saas_usage_meter_reading TO app_rw, app_worker;

GRANT SELECT ON ge.saas_usage_meter_reading TO app_readonly;

GRANT SELECT, DELETE ON ge.saas_usage_meter_reading TO app_retention;

CREATE POLICY rls_saas_usage_meter_reading__select ON ge.saas_usage_meter_reading FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND (startup_id IS NULL OR startup_id = ANY ((SELECT ge.app_company_ids())::uuid[])));

CREATE POLICY rls_saas_usage_meter_reading__insert ON ge.saas_usage_meter_reading FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND (startup_id = (SELECT ge.app_write_company()) OR (startup_id IS NULL AND (SELECT ge.app_actor_kind()) IN ('internal','service'))));

CREATE POLICY rls_saas_usage_meter_reading__retention_delete ON ge.saas_usage_meter_reading FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.sandbox_environment ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.sandbox_environment FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.sandbox_environment TO app_rw, app_worker;

GRANT SELECT ON ge.sandbox_environment TO app_readonly;

GRANT SELECT, DELETE ON ge.sandbox_environment TO app_retention;

ALTER TABLE ge.scim_deprovision_sla ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.scim_deprovision_sla FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.scim_deprovision_sla TO app_rw, app_worker;

GRANT SELECT ON ge.scim_deprovision_sla TO app_readonly;

GRANT SELECT, DELETE ON ge.scim_deprovision_sla TO app_retention;

CREATE POLICY rls_scim_deprovision_sla__select ON ge.scim_deprovision_sla FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()));

CREATE POLICY rls_scim_deprovision_sla__insert ON ge.scim_deprovision_sla FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()));

CREATE POLICY rls_scim_deprovision_sla__update ON ge.scim_deprovision_sla FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()));

CREATE POLICY rls_scim_deprovision_sla__retention_delete ON ge.scim_deprovision_sla FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.scim_group ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.scim_group FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.scim_group TO app_rw, app_worker;

GRANT SELECT ON ge.scim_group TO app_readonly;

GRANT SELECT, DELETE ON ge.scim_group TO app_retention;

CREATE POLICY rls_scim_group__select ON ge.scim_group FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()));

CREATE POLICY rls_scim_group__insert ON ge.scim_group FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()));

CREATE POLICY rls_scim_group__update ON ge.scim_group FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()));

CREATE POLICY rls_scim_group__retention_delete ON ge.scim_group FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.scim_group_member ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.scim_group_member FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.scim_group_member TO app_rw, app_worker;

GRANT SELECT ON ge.scim_group_member TO app_readonly;

GRANT SELECT, DELETE ON ge.scim_group_member TO app_retention;

CREATE POLICY rls_scim_group_member__select ON ge.scim_group_member FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()));

CREATE POLICY rls_scim_group_member__insert ON ge.scim_group_member FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()));

CREATE POLICY rls_scim_group_member__update ON ge.scim_group_member FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()));

CREATE POLICY rls_scim_group_member__retention_delete ON ge.scim_group_member FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.scim_group_role_map ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.scim_group_role_map FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.scim_group_role_map TO app_rw, app_worker;

GRANT SELECT ON ge.scim_group_role_map TO app_readonly;

GRANT SELECT, DELETE ON ge.scim_group_role_map TO app_retention;

CREATE POLICY rls_scim_group_role_map__select ON ge.scim_group_role_map FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND (company_id IS NULL OR company_id = ANY ((SELECT ge.app_company_ids())::uuid[])));

CREATE POLICY rls_scim_group_role_map__insert ON ge.scim_group_role_map FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND (company_id = (SELECT ge.app_write_company()) OR (company_id IS NULL AND (SELECT ge.app_actor_kind()) IN ('internal','service'))));

CREATE POLICY rls_scim_group_role_map__update ON ge.scim_group_role_map FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND (company_id = (SELECT ge.app_write_company()) OR (company_id IS NULL AND (SELECT ge.app_actor_kind()) IN ('internal','service')))) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND (company_id = (SELECT ge.app_write_company()) OR (company_id IS NULL AND (SELECT ge.app_actor_kind()) IN ('internal','service'))));

CREATE POLICY rls_scim_group_role_map__retention_delete ON ge.scim_group_role_map FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.scim_identity ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.scim_identity FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.scim_identity TO app_rw, app_worker;

GRANT SELECT ON ge.scim_identity TO app_readonly;

GRANT SELECT, DELETE ON ge.scim_identity TO app_retention;

CREATE POLICY rls_scim_identity__select ON ge.scim_identity FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()));

CREATE POLICY rls_scim_identity__insert ON ge.scim_identity FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()));

CREATE POLICY rls_scim_identity__update ON ge.scim_identity FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()));

CREATE POLICY rls_scim_identity__retention_delete ON ge.scim_identity FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.scim_token ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.scim_token FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.scim_token TO app_rw, app_worker;

GRANT SELECT ON ge.scim_token TO app_readonly;

GRANT SELECT, DELETE ON ge.scim_token TO app_retention;

GRANT SELECT ON ge.security_finding TO app_rw, app_worker, app_readonly;

GRANT SELECT, INSERT, UPDATE ON ge.security_finding TO app_platform_sec;

ALTER TABLE ge.settlement_batch ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.settlement_batch FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.settlement_batch TO app_rw, app_worker;

GRANT SELECT ON ge.settlement_batch TO app_readonly;

GRANT SELECT, DELETE ON ge.settlement_batch TO app_retention;

CREATE POLICY rls_settlement_batch__select ON ge.settlement_batch FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_settlement_batch__insert ON ge.settlement_batch FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_settlement_batch__update ON ge.settlement_batch FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_settlement_batch__retention_delete ON ge.settlement_batch FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

GRANT SELECT ON ge.sli_sample TO app_rw, app_worker, app_readonly;

GRANT SELECT ON ge.sod_conflict TO app_rw, app_worker, app_readonly;

GRANT SELECT, INSERT, UPDATE ON ge.sod_conflict TO app_platform_sec;

GRANT SELECT ON ge.subprocessor TO app_rw, app_worker, app_readonly;

GRANT SELECT, INSERT, UPDATE ON ge.subprocessor TO app_registry;

ALTER TABLE ge.suppression ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.suppression FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.suppression TO app_rw, app_worker;

GRANT SELECT ON ge.suppression TO app_readonly;

GRANT SELECT, DELETE ON ge.suppression TO app_retention;

ALTER TABLE ge.sync_conflict ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.sync_conflict FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.sync_conflict TO app_rw, app_worker;

GRANT SELECT ON ge.sync_conflict TO app_readonly;

GRANT SELECT, DELETE ON ge.sync_conflict TO app_retention;

CREATE POLICY rls_sync_conflict__select ON ge.sync_conflict FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()));

CREATE POLICY rls_sync_conflict__insert ON ge.sync_conflict FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()));

CREATE POLICY rls_sync_conflict__update ON ge.sync_conflict FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()));

CREATE POLICY rls_sync_conflict__retention_delete ON ge.sync_conflict FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.sync_cursor ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.sync_cursor FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.sync_cursor TO app_rw, app_worker;

GRANT SELECT ON ge.sync_cursor TO app_readonly;

GRANT SELECT, DELETE ON ge.sync_cursor TO app_retention;

CREATE POLICY rls_sync_cursor__select ON ge.sync_cursor FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()));

CREATE POLICY rls_sync_cursor__insert ON ge.sync_cursor FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()));

CREATE POLICY rls_sync_cursor__update ON ge.sync_cursor FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()));

CREATE POLICY rls_sync_cursor__retention_delete ON ge.sync_cursor FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

GRANT SELECT ON ge.tax_rule TO app_rw, app_worker, app_readonly;

GRANT SELECT, INSERT, UPDATE ON ge.tax_rule TO app_platform_sec;

ALTER TABLE ge.ten_business_template ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.ten_business_template FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.ten_business_template TO app_rw, app_worker;

GRANT SELECT ON ge.ten_business_template TO app_readonly;

GRANT SELECT, DELETE ON ge.ten_business_template TO app_retention;

CREATE POLICY rls_ten_business_template__select ON ge.ten_business_template FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND (startup_id IS NULL OR startup_id = ANY ((SELECT ge.app_company_ids())::uuid[])));

CREATE POLICY rls_ten_business_template__insert ON ge.ten_business_template FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND (startup_id = (SELECT ge.app_write_company()) OR (startup_id IS NULL AND (SELECT ge.app_actor_kind()) IN ('internal','service'))));

CREATE POLICY rls_ten_business_template__update ON ge.ten_business_template FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND (startup_id = (SELECT ge.app_write_company()) OR (startup_id IS NULL AND (SELECT ge.app_actor_kind()) IN ('internal','service')))) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND (startup_id = (SELECT ge.app_write_company()) OR (startup_id IS NULL AND (SELECT ge.app_actor_kind()) IN ('internal','service'))));

CREATE POLICY rls_ten_business_template__retention_delete ON ge.ten_business_template FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.ten_capability_profile ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.ten_capability_profile FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.ten_capability_profile TO app_rw, app_worker;

GRANT SELECT ON ge.ten_capability_profile TO app_readonly;

GRANT SELECT, DELETE ON ge.ten_capability_profile TO app_retention;

CREATE POLICY rls_ten_capability_profile__select ON ge.ten_capability_profile FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_ten_capability_profile__insert ON ge.ten_capability_profile FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_ten_capability_profile__update ON ge.ten_capability_profile FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_ten_capability_profile__retention_delete ON ge.ten_capability_profile FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.ten_domain ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.ten_domain FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.ten_domain TO app_rw, app_worker;

GRANT SELECT ON ge.ten_domain TO app_readonly;

GRANT SELECT, DELETE ON ge.ten_domain TO app_retention;

CREATE POLICY rls_ten_domain__select ON ge.ten_domain FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_ten_domain__insert ON ge.ten_domain FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_ten_domain__update ON ge.ten_domain FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_ten_domain__retention_delete ON ge.ten_domain FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.ten_membership ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.ten_membership FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.ten_membership TO app_rw, app_worker;

GRANT SELECT ON ge.ten_membership TO app_readonly;

GRANT SELECT, DELETE ON ge.ten_membership TO app_retention;

CREATE POLICY rls_ten_membership__select ON ge.ten_membership FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND (startup_id IS NULL OR startup_id = ANY ((SELECT ge.app_company_ids())::uuid[])));

CREATE POLICY rls_ten_membership__insert ON ge.ten_membership FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND (startup_id = (SELECT ge.app_write_company()) OR (startup_id IS NULL AND (SELECT ge.app_actor_kind()) IN ('internal','service'))));

CREATE POLICY rls_ten_membership__update ON ge.ten_membership FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND (startup_id = (SELECT ge.app_write_company()) OR (startup_id IS NULL AND (SELECT ge.app_actor_kind()) IN ('internal','service')))) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND (startup_id = (SELECT ge.app_write_company()) OR (startup_id IS NULL AND (SELECT ge.app_actor_kind()) IN ('internal','service'))));

CREATE POLICY rls_ten_membership__retention_delete ON ge.ten_membership FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.ten_membership_grant ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.ten_membership_grant FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.ten_membership_grant TO app_rw, app_worker;

GRANT SELECT ON ge.ten_membership_grant TO app_readonly;

GRANT SELECT, DELETE ON ge.ten_membership_grant TO app_retention;

CREATE POLICY rls_ten_membership_grant__select ON ge.ten_membership_grant FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_ten_membership_grant__insert ON ge.ten_membership_grant FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_ten_membership_grant__update ON ge.ten_membership_grant FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_ten_membership_grant__retention_delete ON ge.ten_membership_grant FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.ten_portal_grant ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.ten_portal_grant FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.ten_portal_grant TO app_rw, app_worker;

GRANT SELECT ON ge.ten_portal_grant TO app_readonly;

GRANT SELECT, DELETE ON ge.ten_portal_grant TO app_retention;

CREATE POLICY rls_ten_portal_grant__select ON ge.ten_portal_grant FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_ten_portal_grant__insert ON ge.ten_portal_grant FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_ten_portal_grant__update ON ge.ten_portal_grant FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_ten_portal_grant__retention_delete ON ge.ten_portal_grant FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.ten_saved_view ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.ten_saved_view FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.ten_saved_view TO app_rw, app_worker;

GRANT SELECT ON ge.ten_saved_view TO app_readonly;

GRANT SELECT, DELETE ON ge.ten_saved_view TO app_retention;

CREATE POLICY rls_ten_saved_view__select ON ge.ten_saved_view FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_ten_saved_view__insert ON ge.ten_saved_view FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_ten_saved_view__update ON ge.ten_saved_view FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_ten_saved_view__retention_delete ON ge.ten_saved_view FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

GRANT SELECT ON ge.ten_user TO app_rw, app_worker, app_readonly;

ALTER TABLE ge.tenant ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.tenant FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.tenant TO app_rw, app_worker;

GRANT SELECT ON ge.tenant TO app_readonly;

GRANT SELECT, DELETE ON ge.tenant TO app_retention;

ALTER TABLE ge.tenant_activation ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.tenant_activation FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.tenant_activation TO app_rw, app_worker;

GRANT SELECT ON ge.tenant_activation TO app_readonly;

GRANT SELECT, DELETE ON ge.tenant_activation TO app_retention;

CREATE POLICY rls_tenant_activation__select ON ge.tenant_activation FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()));

CREATE POLICY rls_tenant_activation__insert ON ge.tenant_activation FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()));

CREATE POLICY rls_tenant_activation__update ON ge.tenant_activation FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()));

CREATE POLICY rls_tenant_activation__retention_delete ON ge.tenant_activation FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.tenant_data_key ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.tenant_data_key FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.tenant_data_key TO app_rw, app_worker;

GRANT SELECT ON ge.tenant_data_key TO app_readonly;

GRANT SELECT, DELETE ON ge.tenant_data_key TO app_retention;

ALTER TABLE ge.tenant_key_config ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.tenant_key_config FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.tenant_key_config TO app_rw, app_worker;

GRANT SELECT ON ge.tenant_key_config TO app_readonly;

GRANT SELECT, DELETE ON ge.tenant_key_config TO app_retention;

ALTER TABLE ge.tenant_security_policy ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.tenant_security_policy FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.tenant_security_policy TO app_rw, app_worker;

GRANT SELECT ON ge.tenant_security_policy TO app_readonly;

GRANT SELECT, DELETE ON ge.tenant_security_policy TO app_retention;

CREATE POLICY rls_tenant_security_policy__select ON ge.tenant_security_policy FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()));

CREATE POLICY rls_tenant_security_policy__insert ON ge.tenant_security_policy FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()));

CREATE POLICY rls_tenant_security_policy__update ON ge.tenant_security_policy FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()));

CREATE POLICY rls_tenant_security_policy__retention_delete ON ge.tenant_security_policy FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.usage_reservation ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.usage_reservation FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.usage_reservation TO app_rw, app_worker;

GRANT SELECT ON ge.usage_reservation TO app_readonly;

GRANT SELECT, DELETE ON ge.usage_reservation TO app_retention;

ALTER TABLE ge.user_role_assignment ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.user_role_assignment FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.user_role_assignment TO app_rw, app_worker;

GRANT SELECT ON ge.user_role_assignment TO app_readonly;

GRANT SELECT, DELETE ON ge.user_role_assignment TO app_retention;

ALTER TABLE ge.user_session ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.user_session FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.user_session TO app_rw, app_worker;

GRANT SELECT ON ge.user_session TO app_readonly;

GRANT SELECT, DELETE ON ge.user_session TO app_retention;

CREATE POLICY rls_user_session__select ON ge.user_session FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()));

CREATE POLICY rls_user_session__insert ON ge.user_session FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()));

CREATE POLICY rls_user_session__update ON ge.user_session FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()));

CREATE POLICY rls_user_session__retention_delete ON ge.user_session FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.verified_domain ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.verified_domain FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.verified_domain TO app_rw, app_worker;

GRANT SELECT ON ge.verified_domain TO app_readonly;

GRANT SELECT, DELETE ON ge.verified_domain TO app_retention;

CREATE POLICY rls_verified_domain__select ON ge.verified_domain FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()));

CREATE POLICY rls_verified_domain__insert ON ge.verified_domain FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()));

CREATE POLICY rls_verified_domain__update ON ge.verified_domain FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()));

CREATE POLICY rls_verified_domain__retention_delete ON ge.verified_domain FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.voice_access_log ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.voice_access_log FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.voice_access_log TO app_rw, app_worker;

GRANT SELECT ON ge.voice_access_log TO app_readonly;

GRANT SELECT, DELETE ON ge.voice_access_log TO app_retention;

CREATE POLICY rls_voice_access_log__select ON ge.voice_access_log FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_voice_access_log__insert ON ge.voice_access_log FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_voice_access_log__update ON ge.voice_access_log FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_voice_access_log__retention_delete ON ge.voice_access_log FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.voice_campaign ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.voice_campaign FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.voice_campaign TO app_rw, app_worker;

GRANT SELECT ON ge.voice_campaign TO app_readonly;

GRANT SELECT, DELETE ON ge.voice_campaign TO app_retention;

CREATE POLICY rls_voice_campaign__select ON ge.voice_campaign FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_voice_campaign__insert ON ge.voice_campaign FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_voice_campaign__update ON ge.voice_campaign FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_voice_campaign__retention_delete ON ge.voice_campaign FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.voice_campaign_contact ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.voice_campaign_contact FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.voice_campaign_contact TO app_rw, app_worker;

GRANT SELECT ON ge.voice_campaign_contact TO app_readonly;

GRANT SELECT, DELETE ON ge.voice_campaign_contact TO app_retention;

CREATE POLICY rls_voice_campaign_contact__select ON ge.voice_campaign_contact FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_voice_campaign_contact__insert ON ge.voice_campaign_contact FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_voice_campaign_contact__update ON ge.voice_campaign_contact FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_voice_campaign_contact__retention_delete ON ge.voice_campaign_contact FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.voice_consent_evidence ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.voice_consent_evidence FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.voice_consent_evidence TO app_rw, app_worker;

GRANT SELECT ON ge.voice_consent_evidence TO app_readonly;

GRANT SELECT, DELETE ON ge.voice_consent_evidence TO app_retention;

CREATE POLICY rls_voice_consent_evidence__select ON ge.voice_consent_evidence FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_voice_consent_evidence__insert ON ge.voice_consent_evidence FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_voice_consent_evidence__update ON ge.voice_consent_evidence FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_voice_consent_evidence__retention_delete ON ge.voice_consent_evidence FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.voice_handoff ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.voice_handoff FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.voice_handoff TO app_rw, app_worker;

GRANT SELECT ON ge.voice_handoff TO app_readonly;

GRANT SELECT, DELETE ON ge.voice_handoff TO app_retention;

CREATE POLICY rls_voice_handoff__select ON ge.voice_handoff FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_voice_handoff__insert ON ge.voice_handoff FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_voice_handoff__update ON ge.voice_handoff FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_voice_handoff__retention_delete ON ge.voice_handoff FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.voice_leg ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.voice_leg FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.voice_leg TO app_rw, app_worker;

GRANT SELECT ON ge.voice_leg TO app_readonly;

GRANT SELECT, DELETE ON ge.voice_leg TO app_retention;

CREATE POLICY rls_voice_leg__select ON ge.voice_leg FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_voice_leg__insert ON ge.voice_leg FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_voice_leg__update ON ge.voice_leg FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_voice_leg__retention_delete ON ge.voice_leg FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.voice_legal_hold ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.voice_legal_hold FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.voice_legal_hold TO app_rw, app_worker;

GRANT SELECT ON ge.voice_legal_hold TO app_readonly;

GRANT SELECT, DELETE ON ge.voice_legal_hold TO app_retention;

CREATE POLICY rls_voice_legal_hold__select ON ge.voice_legal_hold FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_voice_legal_hold__insert ON ge.voice_legal_hold FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_voice_legal_hold__update ON ge.voice_legal_hold FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_voice_legal_hold__retention_delete ON ge.voice_legal_hold FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.voice_meter_event ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.voice_meter_event FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.voice_meter_event TO app_rw, app_worker;

GRANT SELECT ON ge.voice_meter_event TO app_readonly;

GRANT SELECT, DELETE ON ge.voice_meter_event TO app_retention;

CREATE POLICY rls_voice_meter_event__select ON ge.voice_meter_event FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_voice_meter_event__insert ON ge.voice_meter_event FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_voice_meter_event__update ON ge.voice_meter_event FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_voice_meter_event__retention_delete ON ge.voice_meter_event FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.voice_number ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.voice_number FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.voice_number TO app_rw, app_worker;

GRANT SELECT ON ge.voice_number TO app_readonly;

GRANT SELECT, DELETE ON ge.voice_number TO app_retention;

CREATE POLICY rls_voice_number__select ON ge.voice_number FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND (startup_id IS NULL OR startup_id = ANY ((SELECT ge.app_company_ids())::uuid[])));

CREATE POLICY rls_voice_number__insert ON ge.voice_number FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND (startup_id = (SELECT ge.app_write_company()) OR (startup_id IS NULL AND (SELECT ge.app_actor_kind()) IN ('internal','service'))));

CREATE POLICY rls_voice_number__update ON ge.voice_number FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND (startup_id = (SELECT ge.app_write_company()) OR (startup_id IS NULL AND (SELECT ge.app_actor_kind()) IN ('internal','service')))) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND (startup_id = (SELECT ge.app_write_company()) OR (startup_id IS NULL AND (SELECT ge.app_actor_kind()) IN ('internal','service'))));

CREATE POLICY rls_voice_number__retention_delete ON ge.voice_number FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.voice_number_pool ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.voice_number_pool FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.voice_number_pool TO app_rw, app_worker;

GRANT SELECT ON ge.voice_number_pool TO app_readonly;

GRANT SELECT, DELETE ON ge.voice_number_pool TO app_retention;

CREATE POLICY rls_voice_number_pool__select ON ge.voice_number_pool FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_voice_number_pool__insert ON ge.voice_number_pool FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_voice_number_pool__update ON ge.voice_number_pool FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_voice_number_pool__retention_delete ON ge.voice_number_pool FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.voice_recording ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.voice_recording FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.voice_recording TO app_rw, app_worker;

GRANT SELECT ON ge.voice_recording TO app_readonly;

GRANT SELECT, DELETE ON ge.voice_recording TO app_retention;

CREATE POLICY rls_voice_recording__select ON ge.voice_recording FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_voice_recording__insert ON ge.voice_recording FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_voice_recording__update ON ge.voice_recording FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_voice_recording__retention_delete ON ge.voice_recording FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.voice_script ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.voice_script FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.voice_script TO app_rw, app_worker;

GRANT SELECT ON ge.voice_script TO app_readonly;

GRANT SELECT, DELETE ON ge.voice_script TO app_retention;

CREATE POLICY rls_voice_script__select ON ge.voice_script FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_voice_script__insert ON ge.voice_script FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_voice_script__update ON ge.voice_script FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_voice_script__retention_delete ON ge.voice_script FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.voice_script_version ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.voice_script_version FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.voice_script_version TO app_rw, app_worker;

GRANT SELECT ON ge.voice_script_version TO app_readonly;

GRANT SELECT, DELETE ON ge.voice_script_version TO app_retention;

CREATE POLICY rls_voice_script_version__select ON ge.voice_script_version FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_voice_script_version__insert ON ge.voice_script_version FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_voice_script_version__update ON ge.voice_script_version FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_voice_script_version__retention_delete ON ge.voice_script_version FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.voice_scrub_result ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.voice_scrub_result FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.voice_scrub_result TO app_rw, app_worker;

GRANT SELECT ON ge.voice_scrub_result TO app_readonly;

GRANT SELECT, DELETE ON ge.voice_scrub_result TO app_retention;

CREATE POLICY rls_voice_scrub_result__select ON ge.voice_scrub_result FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_voice_scrub_result__insert ON ge.voice_scrub_result FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_voice_scrub_result__update ON ge.voice_scrub_result FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_voice_scrub_result__retention_delete ON ge.voice_scrub_result FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.voice_session ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.voice_session FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.voice_session TO app_rw, app_worker;

GRANT SELECT ON ge.voice_session TO app_readonly;

GRANT SELECT, DELETE ON ge.voice_session TO app_retention;

CREATE POLICY rls_voice_session__select ON ge.voice_session FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_voice_session__insert ON ge.voice_session FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_voice_session__update ON ge.voice_session FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_voice_session__retention_delete ON ge.voice_session FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.voice_summary ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.voice_summary FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.voice_summary TO app_rw, app_worker;

GRANT SELECT ON ge.voice_summary TO app_readonly;

GRANT SELECT, DELETE ON ge.voice_summary TO app_retention;

CREATE POLICY rls_voice_summary__select ON ge.voice_summary FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_voice_summary__insert ON ge.voice_summary FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_voice_summary__update ON ge.voice_summary FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_voice_summary__retention_delete ON ge.voice_summary FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.voice_transcript ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.voice_transcript FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.voice_transcript TO app_rw, app_worker;

GRANT SELECT ON ge.voice_transcript TO app_readonly;

GRANT SELECT, DELETE ON ge.voice_transcript TO app_retention;

CREATE POLICY rls_voice_transcript__select ON ge.voice_transcript FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_voice_transcript__insert ON ge.voice_transcript FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_voice_transcript__update ON ge.voice_transcript FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_voice_transcript__retention_delete ON ge.voice_transcript FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.voice_transcript_segment ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.voice_transcript_segment FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.voice_transcript_segment TO app_rw, app_worker;

GRANT SELECT ON ge.voice_transcript_segment TO app_readonly;

GRANT SELECT, DELETE ON ge.voice_transcript_segment TO app_retention;

CREATE POLICY rls_voice_transcript_segment__select ON ge.voice_transcript_segment FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_voice_transcript_segment__insert ON ge.voice_transcript_segment FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_voice_transcript_segment__update ON ge.voice_transcript_segment FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_voice_transcript_segment__retention_delete ON ge.voice_transcript_segment FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.voice_voicemail ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.voice_voicemail FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.voice_voicemail TO app_rw, app_worker;

GRANT SELECT ON ge.voice_voicemail TO app_readonly;

GRANT SELECT, DELETE ON ge.voice_voicemail TO app_retention;

CREATE POLICY rls_voice_voicemail__select ON ge.voice_voicemail FOR SELECT USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = ANY ((SELECT ge.app_company_ids())::uuid[]));

CREATE POLICY rls_voice_voicemail__insert ON ge.voice_voicemail FOR INSERT WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_voice_voicemail__update ON ge.voice_voicemail FOR UPDATE USING (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company())) WITH CHECK (tenant_id = (SELECT ge.app_tenant()) AND startup_id = (SELECT ge.app_write_company()));

CREATE POLICY rls_voice_voicemail__retention_delete ON ge.voice_voicemail FOR DELETE TO app_retention USING (tenant_id = (SELECT ge.app_tenant()) AND current_setting('app.retention_run_id', true) <> '');

ALTER TABLE ge.webhook_delivery ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.webhook_delivery FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT ON ge.webhook_delivery TO app_rw, app_worker;

GRANT SELECT ON ge.webhook_delivery TO app_readonly;

GRANT SELECT, DELETE ON ge.webhook_delivery TO app_retention;

ALTER TABLE ge.webhook_endpoint ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.webhook_endpoint FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.webhook_endpoint TO app_rw, app_worker;

GRANT SELECT ON ge.webhook_endpoint TO app_readonly;

GRANT SELECT, DELETE ON ge.webhook_endpoint TO app_retention;

ALTER TABLE ge.workflow_configuration ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.workflow_configuration FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.workflow_configuration TO app_rw, app_worker;

GRANT SELECT ON ge.workflow_configuration TO app_readonly;

GRANT SELECT, DELETE ON ge.workflow_configuration TO app_retention;

ALTER TABLE ge.workflow_run ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.workflow_run FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.workflow_run TO app_rw, app_worker;

GRANT SELECT ON ge.workflow_run TO app_readonly;

GRANT SELECT, DELETE ON ge.workflow_run TO app_retention;

ALTER TABLE ge.workflow_step_run ENABLE ROW LEVEL SECURITY;

ALTER TABLE ge.workflow_step_run FORCE ROW LEVEL SECURITY;

GRANT SELECT, INSERT, UPDATE ON ge.workflow_step_run TO app_rw, app_worker;

GRANT SELECT ON ge.workflow_step_run TO app_readonly;

GRANT SELECT, DELETE ON ge.workflow_step_run TO app_retention;

CREATE TABLE IF NOT EXISTS ge.platform_table_allowlist (table_name text PRIMARY KEY, reason text NOT NULL);

INSERT INTO ge.platform_table_allowlist VALUES ('ai_model', 'no tenant column: platform metadata, reference data or zone evidence; writes only by app_owner migrations or a named service role') ON CONFLICT DO NOTHING;

INSERT INTO ge.platform_table_allowlist VALUES ('ai_model_approval', 'no tenant column: platform metadata, reference data or zone evidence; writes only by app_owner migrations or a named service role') ON CONFLICT DO NOTHING;

INSERT INTO ge.platform_table_allowlist VALUES ('ai_model_pin', 'no tenant column: platform metadata, reference data or zone evidence; writes only by app_owner migrations or a named service role') ON CONFLICT DO NOTHING;

INSERT INTO ge.platform_table_allowlist VALUES ('ai_model_region', 'no tenant column: platform metadata, reference data or zone evidence; writes only by app_owner migrations or a named service role') ON CONFLICT DO NOTHING;

INSERT INTO ge.platform_table_allowlist VALUES ('app_user', 'no tenant column: platform metadata, reference data or zone evidence; writes only by app_owner migrations or a named service role') ON CONFLICT DO NOTHING;

INSERT INTO ge.platform_table_allowlist VALUES ('benchmark_contribution', 'no tenant column: platform metadata, reference data or zone evidence; writes only by app_owner migrations or a named service role') ON CONFLICT DO NOTHING;

INSERT INTO ge.platform_table_allowlist VALUES ('benchmark_privacy_ledger', 'no tenant column: platform metadata, reference data or zone evidence; writes only by app_owner migrations or a named service role') ON CONFLICT DO NOTHING;

INSERT INTO ge.platform_table_allowlist VALUES ('domain_schema_registry', 'no tenant column: platform metadata, reference data or zone evidence; writes only by app_owner migrations or a named service role') ON CONFLICT DO NOTHING;

INSERT INTO ge.platform_table_allowlist VALUES ('edge_conformance_check', 'no tenant column: platform metadata, reference data or zone evidence; writes only by app_owner migrations or a named service role') ON CONFLICT DO NOTHING;

INSERT INTO ge.platform_table_allowlist VALUES ('edge_project', 'no tenant column: platform metadata, reference data or zone evidence; writes only by app_owner migrations or a named service role') ON CONFLICT DO NOTHING;

INSERT INTO ge.platform_table_allowlist VALUES ('eval_run', 'no tenant column: platform metadata, reference data or zone evidence; writes only by app_owner migrations or a named service role') ON CONFLICT DO NOTHING;

INSERT INTO ge.platform_table_allowlist VALUES ('eval_suite', 'no tenant column: platform metadata, reference data or zone evidence; writes only by app_owner migrations or a named service role') ON CONFLICT DO NOTHING;

INSERT INTO ge.platform_table_allowlist VALUES ('fx_rate', 'no tenant column: platform metadata, reference data or zone evidence; writes only by app_owner migrations or a named service role') ON CONFLICT DO NOTHING;

INSERT INTO ge.platform_table_allowlist VALUES ('incident_notification', 'no tenant column: platform metadata, reference data or zone evidence; writes only by app_owner migrations or a named service role') ON CONFLICT DO NOTHING;

INSERT INTO ge.platform_table_allowlist VALUES ('jurisdiction_pack', 'no tenant column: platform metadata, reference data or zone evidence; writes only by app_owner migrations or a named service role') ON CONFLICT DO NOTHING;

INSERT INTO ge.platform_table_allowlist VALUES ('jurisdiction_rule', 'no tenant column: platform metadata, reference data or zone evidence; writes only by app_owner migrations or a named service role') ON CONFLICT DO NOTHING;

INSERT INTO ge.platform_table_allowlist VALUES ('locale_bundle', 'no tenant column: platform metadata, reference data or zone evidence; writes only by app_owner migrations or a named service role') ON CONFLICT DO NOTHING;

INSERT INTO ge.platform_table_allowlist VALUES ('metric_definition', 'no tenant column: platform metadata, reference data or zone evidence; writes only by app_owner migrations or a named service role') ON CONFLICT DO NOTHING;

INSERT INTO ge.platform_table_allowlist VALUES ('oauth_jti_seen', 'no tenant column: platform metadata, reference data or zone evidence; writes only by app_owner migrations or a named service role') ON CONFLICT DO NOTHING;

INSERT INTO ge.platform_table_allowlist VALUES ('ops_incident', 'no tenant column: platform metadata, reference data or zone evidence; writes only by app_owner migrations or a named service role') ON CONFLICT DO NOTHING;

INSERT INTO ge.platform_table_allowlist VALUES ('ops_release', 'no tenant column: platform metadata, reference data or zone evidence; writes only by app_owner migrations or a named service role') ON CONFLICT DO NOTHING;

INSERT INTO ge.platform_table_allowlist VALUES ('ops_test_run', 'no tenant column: platform metadata, reference data or zone evidence; writes only by app_owner migrations or a named service role') ON CONFLICT DO NOTHING;

INSERT INTO ge.platform_table_allowlist VALUES ('permission_catalogue', 'no tenant column: platform metadata, reference data or zone evidence; writes only by app_owner migrations or a named service role') ON CONFLICT DO NOTHING;

INSERT INTO ge.platform_table_allowlist VALUES ('platform_table_allowlist', 'no tenant column: platform metadata, reference data or zone evidence; writes only by app_owner migrations or a named service role') ON CONFLICT DO NOTHING;

INSERT INTO ge.platform_table_allowlist VALUES ('prompt_version', 'no tenant column: platform metadata, reference data or zone evidence; writes only by app_owner migrations or a named service role') ON CONFLICT DO NOTHING;

INSERT INTO ge.platform_table_allowlist VALUES ('recovery_path', 'no tenant column: platform metadata, reference data or zone evidence; writes only by app_owner migrations or a named service role') ON CONFLICT DO NOTHING;

INSERT INTO ge.platform_table_allowlist VALUES ('ref_country', 'no tenant column: platform metadata, reference data or zone evidence; writes only by app_owner migrations or a named service role') ON CONFLICT DO NOTHING;

INSERT INTO ge.platform_table_allowlist VALUES ('ref_currency', 'no tenant column: platform metadata, reference data or zone evidence; writes only by app_owner migrations or a named service role') ON CONFLICT DO NOTHING;

INSERT INTO ge.platform_table_allowlist VALUES ('restore_drill', 'no tenant column: platform metadata, reference data or zone evidence; writes only by app_owner migrations or a named service role') ON CONFLICT DO NOTHING;

INSERT INTO ge.platform_table_allowlist VALUES ('rpo_sample', 'no tenant column: platform metadata, reference data or zone evidence; writes only by app_owner migrations or a named service role') ON CONFLICT DO NOTHING;

INSERT INTO ge.platform_table_allowlist VALUES ('rulepack_requirement', 'no tenant column: platform metadata, reference data or zone evidence; writes only by app_owner migrations or a named service role') ON CONFLICT DO NOTHING;

INSERT INTO ge.platform_table_allowlist VALUES ('saas_application_draft', 'no tenant column: platform metadata, reference data or zone evidence; writes only by app_owner migrations or a named service role') ON CONFLICT DO NOTHING;

INSERT INTO ge.platform_table_allowlist VALUES ('saas_plan', 'no tenant column: platform metadata, reference data or zone evidence; writes only by app_owner migrations or a named service role') ON CONFLICT DO NOTHING;

INSERT INTO ge.platform_table_allowlist VALUES ('saas_plan_version', 'no tenant column: platform metadata, reference data or zone evidence; writes only by app_owner migrations or a named service role') ON CONFLICT DO NOTHING;

INSERT INTO ge.platform_table_allowlist VALUES ('security_finding', 'no tenant column: platform metadata, reference data or zone evidence; writes only by app_owner migrations or a named service role') ON CONFLICT DO NOTHING;

INSERT INTO ge.platform_table_allowlist VALUES ('sli_sample', 'no tenant column: platform metadata, reference data or zone evidence; writes only by app_owner migrations or a named service role') ON CONFLICT DO NOTHING;

INSERT INTO ge.platform_table_allowlist VALUES ('sod_conflict', 'no tenant column: platform metadata, reference data or zone evidence; writes only by app_owner migrations or a named service role') ON CONFLICT DO NOTHING;

INSERT INTO ge.platform_table_allowlist VALUES ('subprocessor', 'no tenant column: platform metadata, reference data or zone evidence; writes only by app_owner migrations or a named service role') ON CONFLICT DO NOTHING;

INSERT INTO ge.platform_table_allowlist VALUES ('tax_rule', 'no tenant column: platform metadata, reference data or zone evidence; writes only by app_owner migrations or a named service role') ON CONFLICT DO NOTHING;

INSERT INTO ge.platform_table_allowlist VALUES ('ten_user', 'no tenant column: platform metadata, reference data or zone evidence; writes only by app_owner migrations or a named service role') ON CONFLICT DO NOTHING;

GRANT SELECT ON ge.platform_table_allowlist TO app_readonly;

GRANT EXECUTE ON FUNCTION ge.fn_append_audit(uuid,uuid,text,text,text,text,uuid,jsonb) TO app_rw, app_worker;
