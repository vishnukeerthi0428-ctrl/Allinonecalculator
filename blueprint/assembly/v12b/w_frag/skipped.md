| # | Migration | Reason | Statement / reference (truncated) |
|---|---|---|---|
| 1 | V0006 | role rename not needed: roles are created with canonical names in V0001 (DEC-778, DEC-894) | DO $$ BEGIN   IF EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'ge_app') AND NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'app_rw') T |
| 2 | V0006 | assertion moved to V0015 (runs after all tables and policies exist) | DO $$ BEGIN   IF EXISTS (SELECT 1 FROM pg_roles WHERE rolname IN ('app_rw','app_worker','app_readonly','app_retention','app_bench','app_regi |
| 3 | V0009 | unique key names a column the dictionary does not define (received_month) | UNIQUE int_provider_event (provider_account, provider_event_id, received_month)  |
| 4 | V0009 | unique key names a column the dictionary does not define (case_key) | UNIQUE ai_eval_case (suite_code, case_key, version_no)  |
| 5 | V0009 | unique key names a column the dictionary does not define (code) | UNIQUE eng_message_template (tenant_id, startup_id, code, locale, version_no)  |
| 6 | V0009 | unique key names a column the dictionary does not define (channel_account_id) | UNIQUE eng_message (channel_account_id, idempotency_key)  |
| 7 | V0009 | unique key names a column the dictionary does not define (channel_account_id) | UNIQUE eng_message (channel_account_id, provider_message_id)  |
| 8 | V0009 | unique key names a column the dictionary does not define (outbox_id) | UNIQUE ops_domain_event (outbox_id)  |
| 9 | V0009 | unique key names a column the dictionary does not define (startup_scope_hash) | UNIQUE ana_admin_projection (tenant_id, panel_code, startup_scope_hash)  |
| 10 | V0009 | unique key names a column the dictionary does not define () | UNIQUE ten_business_template (COALESCE(tenant_id, zero-uuid), template_key, version_no)  |
| 11 | V0009 | ref_value is keyed by (dataset_id, code): code columns are validated by fn/app against the dataset (Part 3.3 ENT-012) | FK cat_offering_version(hsn_sac_code) -> ref_value |
| 12 | V0009 | type mismatch ['uuid'] -> ai_budget['text']: reference kept as a soft reference (validated in the service layer) | FK ai_cost_ledger(budget_id) -> ai_budget(period) |
| 13 | V0009 | ref_value is keyed by (dataset_id, code): code columns are validated by fn/app against the dataset (Part 3.3 ENT-012) | FK intel_organization(org_type) -> ref_value |
| 14 | V0009 | ref_value is keyed by (dataset_id, code): code columns are validated by fn/app against the dataset (Part 3.3 ENT-012) | FK intel_organization(industry_code) -> ref_value |
| 15 | V0009 | ref_value is keyed by (dataset_id, code): code columns are validated by fn/app against the dataset (Part 3.3 ENT-012) | FK intel_need(need_category) -> ref_value |
| 16 | V0009 | ref_value is keyed by (dataset_id, code): code columns are validated by fn/app against the dataset (Part 3.3 ENT-012) | FK intel_contact(role_code) -> ref_value |
| 17 | V0009 | ref_value is keyed by (dataset_id, code): code columns are validated by fn/app against the dataset (Part 3.3 ENT-012) | FK crm_deal(lost_reason_code) -> ref_value |
| 18 | V0009 | type mismatch ['uuid'] -> ai_budget['text']: reference kept as a soft reference (validated in the service layer) | FK mkt_campaign(budget_id) -> ai_budget(period) |
| 19 | V0009 | type mismatch ['text'] -> com_sku_availability['uuid']: reference kept as a soft reference (validated in the service layer) | FK com_order_line(sku_code) -> com_sku_availability(id) |
| 20 | V0009 | type mismatch ['text'] -> aut_workflow_template['uuid']: reference kept as a soft reference (validated in the service layer) | FK aut_workflow_revision(template_id) -> aut_workflow_template(id) |
| 21 | V0009 | type mismatch ['text'] -> aut_workflow_template['uuid']: reference kept as a soft reference (validated in the service layer) | FK aut_workflow_revision(template_version) -> aut_workflow_template(id) |
| 22 | V0009 | ref_value is keyed by (dataset_id, code): code columns are validated by fn/app against the dataset (Part 3.3 ENT-012) | FK ten_business_template(industry_code) -> ref_value |
| 23 | V0009 | type mismatch ['uuid[]'] -> aut_workflow_template['uuid']: reference kept as a soft reference (validated in the service layer) | FK ten_business_template(workflow_template_ids) -> aut_workflow_template(id) |
| 24 | V0009 | type mismatch ['uuid'] -> tax_rule['text']: reference kept as a soft reference (validated in the service layer) | FK company(tax_profile_id) -> tax_rule(rule_id) |
| 25 | V0009 | type mismatch ['uuid'] -> suppression['text']: reference kept as a soft reference (validated in the service layer) | FK suppression(lifted_by_id) -> suppression(purpose) |
| 26 | V0009 | type mismatch ['uuid'] -> ai_usage_event['bigint']: reference kept as a soft reference (validated in the service layer) | FK ai_cost_ledger(usage_id) -> ai_usage_event(usage_id) |
| 27 | V0012 | index names columns not defined on ai_budget: status | CREATE UNIQUE INDEX uq_ai_budget__scope_period ON ai_budget (COALESCE(tenant_id, '00000000-0000-0000-0000-000000000000'::uuid), scope_level, |
