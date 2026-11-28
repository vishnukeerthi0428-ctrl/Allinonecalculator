| # | V12 operationId | Method | V12 path | V12 tag / summary | Source | Blueprint operation(s) | Relation | Before | Enhancement |
|---|---|---|---|---|---|---|---|---|---|
| 1 | get_admin_ai_eval_cases | GET | `/api/v1/admin/ai/eval-cases` | Screens: Screen A011 | SM-OP-036 | API-ENH-D-002 | New (Part 3.5b) | Covered | — |
| 2 | post_admin_ai_prompts | POST | `/api/v1/admin/ai/prompts` | SM-SVC-25: Used by SM-SVC-25-WF01 | SM-OP-035 | API-142 | Alias | Covered | — |
| 3 | get_admin_ai_runs | GET | `/api/v1/admin/ai/runs` | SM-SVC-25: Used by SM-SVC-25-WF01 | SM-OP-034 | API-135 | Exact | Covered | — |
| 4 | get_admin_approvals | GET | `/api/v1/admin/approvals` | SM-SVC-11: Used by SM-SVC-11-WF01 | SM-OP-107 | API-540 | Alias | Covered | — |
| 5 | post_admin_approvals_id_decide | POST | `/api/v1/admin/approvals/{id}/decide` | Screens: Screen A089 | SM-OP-232 | API-539 | Exact | Covered | — |
| 6 | post_admin_budgets | POST | `/api/v1/admin/budgets` | Screens: Screen A012 | SM-OP-039 | API-137 | Exact | Covered | — |
| 7 | post_admin_budgets_id_pause | POST | `/api/v1/admin/budgets/{id}/pause` | Screens: Screen A012 | SM-OP-040 | API-144 | Alias | Covered | — |
| 8 | post_admin_calendar_links | POST | `/api/v1/admin/calendar-links` | SM-SVC-10: Used by SM-SVC-10-WF01 | SM-OP-125 | API-110 | Alias | Covered | — |
| 9 | post_admin_chat_settings | POST | `/api/v1/admin/chat/settings` | SM-SVC-08: Used by SM-SVC-08-WF01 | SM-OP-138 | API-280; API-ENH-D-009 | Partial | Covered | — |
| 10 | post_admin_claims_approve | POST | `/api/v1/admin/claims/approve` | SM-SVC-28: Used by SM-SVC-28-WF01 | SM-OP-010 | API-049 | Exact | Covered | — |
| 11 | post_admin_competitor_sources | POST | `/api/v1/admin/competitor-sources` | SM-SVC-01: Used by SM-SVC-01-WF01 | SM-OP-228 | API-208 | Alias | Covered | — |
| 12 | get_admin_compliance | GET | `/api/v1/admin/compliance` | Screens: Screen A047 | SM-OP-142 | API-070 | Exact | Covered | — |
| 13 | post_admin_compliance_id_resolve | POST | `/api/v1/admin/compliance/{id}/resolve` | Screens: Screen A047 | SM-OP-143 | API-094 | Alias | Covered | — |
| 14 | get_admin_costs | GET | `/api/v1/admin/costs` | Screens: Screen A012 | SM-OP-038 | API-136 | Exact | Covered | — |
| 15 | get_admin_dashboard | GET | `/api/v1/admin/dashboard` | Screens: Screen A089 | SM-OP-231 | API-538 | Exact | Covered | — |
| 16 | get_admin_evals_results | GET | `/api/v1/admin/evals/results` | Screens: Screen A084 | SM-OP-226 | API-147;API-148 | Split | Covered | — |
| 17 | post_admin_evals_run | POST | `/api/v1/admin/evals/run` | Screens: Screen A084 | SM-OP-225 | API-138 | Exact | Covered | — |
| 18 | post_admin_events_id_settings | POST | `/api/v1/admin/events/{id}/settings` | SM-SVC-10: Used by SM-SVC-10-WF01 | SM-OP-180 | API-325 | Alias | Covered | — |
| 19 | post_admin_forecast_settings | POST | `/api/v1/admin/forecast-settings` | SM-SVC-24: Used by SM-SVC-24-WF01 | SM-OP-230 | API-407; API-ENH-D-010 | Partial | Covered | — |
| 20 | get_admin_forms | GET | `/api/v1/admin/forms` | SM-SVC-15: Used by SM-SVC-15-WF01 | SM-OP-094 | API-221 | Alias | Covered | — |
| 21 | post_admin_forms | POST | `/api/v1/admin/forms` | SM-SVC-15: Used by SM-SVC-15-WF01 | SM-OP-095 | API-222;API-223 | Split | Covered | — |
| 22 | get_admin_health | GET | `/api/v1/admin/health` | Screens: Screen A014 | SM-OP-047 | API-119 | Exact | Covered | — |
| 23 | post_admin_incidents_id_resolve | POST | `/api/v1/admin/incidents/{id}/resolve` | Screens: Screen A014 | SM-OP-048 | API-129;API-130 | Split | Covered | — |
| 24 | post_admin_integrations | POST | `/api/v1/admin/integrations` | SM-SVC-06: Used by SM-SVC-06-WF01 | SM-OP-024 | API-097 | Alias | Covered | — |
| 25 | post_admin_integrations_test | POST | `/api/v1/admin/integrations/test` | Screens: Screen A008 | SM-OP-025 | API-096 | Exact | Covered | — |
| 26 | post_admin_integrations_id_disable | POST | `/api/v1/admin/integrations/{id}/disable` | Screens: Screen A008 | SM-OP-026 | API-099 | Alias | Covered | — |
| 27 | get_admin_jobs | GET | `/api/v1/admin/jobs` | Screens: Screen A009 | SM-OP-028 | API-124 | Alias | Covered | — |
| 28 | post_admin_jobs_id_retry | POST | `/api/v1/admin/jobs/{id}/retry` | Screens: Screen A009 | SM-OP-029 | API-116 | Exact | Covered | — |
| 29 | post_admin_kpi_definitions | POST | `/api/v1/admin/kpi-definitions` | SM-SVC-21: Used by SM-SVC-21-WF01 | SM-OP-224 | API-405 | Alias | Covered | — |
| 30 | get_admin_message_templates | GET | `/api/v1/admin/message-templates` | SM-SVC-06: Used by SM-SVC-06-WF01 | SM-OP-104 | API-255 | Alias | Covered | — |
| 31 | post_admin_message_templates | POST | `/api/v1/admin/message-templates` | SM-SVC-06: Used by SM-SVC-06-WF01 | SM-OP-105 | API-256 | Alias | Covered | — |
| 32 | get_admin_pipeline_stages | GET | `/api/v1/admin/pipeline-stages` | SM-SVC-05: Used by SM-SVC-05-WF01 | SM-OP-089 | API-218 | Alias | Covered | — |
| 33 | post_admin_pipeline_stages | POST | `/api/v1/admin/pipeline-stages` | SM-SVC-05: Used by SM-SVC-05-WF01 | SM-OP-090 | API-219;API-220 | Split | Covered | — |
| 34 | get_admin_policies | GET | `/api/v1/admin/policies` | SM-SVC-06: Used by SM-SVC-06-WF01 | SM-OP-020 | API-071 | Alias | Covered | — |
| 35 | post_admin_policies | POST | `/api/v1/admin/policies` | SM-SVC-06: Used by SM-SVC-06-WF01 | SM-OP-021 | API-072;API-073 | Split | Covered | — |
| 36 | get_admin_privacy_requests | GET | `/api/v1/admin/privacy/requests` | Screens: Screen A013 | SM-OP-042 | API-084 | Alias | Covered | — |
| 37 | post_admin_privacy_requests_id_resolve | POST | `/api/v1/admin/privacy/requests/{id}/resolve` | Screens: Screen A013 | SM-OP-043 | API-085;API-086;API-087 | Split | Covered | — |
| 38 | post_admin_products | POST | `/api/v1/admin/products` | SM-SVC-25: Used by SM-SVC-25-WF01 | SM-OP-008 | API-053 | Alias | Covered | — |
| 39 | get_admin_products_planned | GET | `/api/v1/admin/products/planned` | Screens: Screen A097 | SM-OP-245 | API-064 | Alias | Covered | — |
| 40 | patch_admin_products_id | PATCH | `/api/v1/admin/products/{id}` | SM-SVC-28: Used by SM-SVC-28-WF01 | SM-OP-009 | API-055;API-056 | Split | Covered | — |
| 41 | post_admin_products_id_launch | POST | `/api/v1/admin/products/{id}/launch` | Screens: Screen A098 | SM-OP-246 | API-050 | Exact | Covered | — |
| 42 | post_admin_products_id_prices | POST | `/api/v1/admin/products/{id}/prices` | SM-SVC-28: Used by SM-SVC-28-WF01 | SM-OP-011 | API-057 | Alias | Covered | — |
| 43 | get_admin_referrals | GET | `/api/v1/admin/referrals` | SM-SVC-16: Used by SM-SVC-16-WF01 | SM-OP-183 | API-327 | Alias | Covered | — |
| 44 | post_admin_referrals_id_review | POST | `/api/v1/admin/referrals/{id}/review` | SM-SVC-16: Used by SM-SVC-16-WF01 | SM-OP-184 | API-541;API-539 | Approval | Covered | — |
| 45 | get_admin_releases | GET | `/api/v1/admin/releases` | Screens: Screen A090 | SM-OP-233 | API-120 | Exact | Covered | — |
| 46 | post_admin_releases_id_approve | POST | `/api/v1/admin/releases/{id}/approve` | Screens: Screen A090 | SM-OP-234 | API-132 | Alias | Covered | — |
| 47 | post_admin_renewal_policies | POST | `/api/v1/admin/renewal-policies` | SM-SVC-23: Used by SM-SVC-23-WF01 | SM-OP-219 | API-429 | Alias | Covered | — |
| 48 | post_admin_research_review_rules | POST | `/api/v1/admin/research-review-rules` | SM-SVC-19: Used by SM-SVC-19-WF01 | SM-OP-083 | API-202 | Alias | Covered | — |
| 49 | post_admin_retention_policies | POST | `/api/v1/admin/retention-policies` | Screens: Screen A013 | SM-OP-044 | API-091 | Alias | Covered | — |
| 50 | post_admin_role_mappings | POST | `/api/v1/admin/role-mappings` | SM-SVC-03: Used by SM-SVC-03-WF01 | SM-OP-075 | API-199; API-ENH-D-004 | Partial | Covered | — |
| 51 | post_admin_routing_rules | POST | `/api/v1/admin/routing-rules` | SM-SVC-26: Used by SM-SVC-26-WF01 | SM-OP-141 | API-283 | Alias | Covered | — |
| 52 | post_admin_scoring_rules | POST | `/api/v1/admin/scoring-rules` | Screens: Screen A023 | SM-OP-072 | API-194;API-195 | Split | Covered | — |
| 53 | post_admin_sequences | POST | `/api/v1/admin/sequences` | SM-SVC-08: Used by SM-SVC-08-WF01 | SM-OP-117 | API-262 | Alias | Covered | — |
| 54 | post_admin_signal_types | POST | `/api/v1/admin/signal-types` | Screens: Screen A023 | SM-OP-065 | API-047; API-ENH-D-003 | Partial | Covered | — |
| 55 | post_admin_social_accounts | POST | `/api/v1/admin/social/accounts` | Screens: Screen A053 | SM-OP-154 | API-113 | Alias | Covered | — |
| 56 | post_admin_social_sources | POST | `/api/v1/admin/social/sources` | SM-SVC-12: Used by SM-SVC-12-WF01 | SM-OP-145 | API-206 | Alias | Covered | — |
| 57 | post_admin_sources | POST | `/api/v1/admin/sources` | Screens: Screen A010 | SM-OP-031 | API-159 | Exact | Covered | — |
| 58 | patch_admin_sources_id | PATCH | `/api/v1/admin/sources/{id}` | Screens: Screen A010 | SM-OP-032 | API-179; API-ENH-D-001 | Partial | Covered | — |
| 59 | get_admin_suppressions | GET | `/api/v1/admin/suppressions` | SM-SVC-38: Used by SM-SVC-38-WF01 | SM-OP-022 | API-074;API-076 | Split | Covered | — |
| 60 | get_admin_users | GET | `/api/v1/admin/users` | Screens: Screen A002 | SM-OP-003 | API-019 | Alias (prefix) | Covered | — |
| 61 | post_admin_users_id_roles | POST | `/api/v1/admin/users/{id}/roles` | Screens: Screen A002 | SM-OP-004 | API-021;API-020 | Alias (prefix) | Covered | — |
| 62 | get_admin_whatsapp_accounts | GET | `/api/v1/admin/whatsapp/accounts` | SM-SVC-07: Used by SM-SVC-07-WF01 | SM-OP-130 | API-109;API-102; API-ENH-D-008 | Partial | Covered | — |
| 63 | post_admin_whatsapp_accounts | POST | `/api/v1/admin/whatsapp/accounts` | SM-SVC-07: Used by SM-SVC-07-WF01 | SM-OP-131 | API-107 | Alias | Covered | — |
| 64 | post_admin_whatsapp_templates | POST | `/api/v1/admin/whatsapp/templates` | SM-SVC-07: Used by SM-SVC-07-WF01 | SM-OP-132 | API-108 | Alias | Covered | — |
| 65 | post_admin_workflows | POST | `/api/v1/admin/workflows` | Screens: Screen A033 | SM-OP-099 | API-446;API-448 | Split | Covered | — |
| 66 | post_admin_workflows_pause | POST | `/api/v1/admin/workflows/pause` | Screens: Screen A033 | SM-OP-100 | API-445 | Exact | Covered | — |
| 67 | post_admin_workflows_id_resume | POST | `/api/v1/admin/workflows/{id}/resume` | Screens: Screen A033 | SM-OP-101 | API-469;API-450; API-ENH-D-006 | Partial | Covered | — |
| 68 | post_ads_drafts | POST | `/api/v1/ads/drafts` | SM-SVC-14: Used by SM-SVC-14-WF01 | SM-OP-170 | API-294 | Exact | Covered | — |
| 69 | get_ads_metrics | GET | `/api/v1/ads/metrics` | SM-SVC-14: Used by SM-SVC-14-WF01 | SM-OP-171 | API-295 | Exact | Covered | — |
| 70 | post_ads_id_launch | POST | `/api/v1/ads/{id}/launch` | SM-SVC-14: Used by SM-SVC-14-WF01 | SM-OP-172 | API-318 | Alias | Covered | — |
| 71 | post_ads_id_pause | POST | `/api/v1/ads/{id}/pause` | SM-SVC-14: Used by SM-SVC-14-WF01 | SM-OP-173 | API-319 | Alias | Covered | — |
| 72 | put_ai_budgets_id | PUT | `/api/v1/ai/budgets/{id}` | AI: Set soft/hard AI budget for scope (AIX-13) | V8 | API-137; API-146 | Alias | Covered | — |
| 73 | post_ai_content_screen | POST | `/api/v1/ai/content-screen` | AI: Screen untrusted content; returns flags only | V8 | — | New | Not covered | API-V12-H-054 |
| 74 | get_ai_eval_runs_id | GET | `/api/v1/ai/eval-runs/{id}` | AI: Evaluation run result with denominator | V8 | API-148 | Alias | Covered | — |
| 75 | get_ai_eval_suites | GET | `/api/v1/ai/eval-suites` | AI: List evaluation suites (AIX-05) | V8 | API-ENH-D-002; API-147 | Partial | Partially covered | API-V12-H-052 |
| 76 | post_ai_eval_suites_id_runs | POST | `/api/v1/ai/eval-suites/{id}/runs` | AI: Replay suite against candidate (AIX-06) | V8 | API-138 | Alias | Covered | — |
| 77 | post_ai_kill_switch | POST | `/api/v1/ai/kill-switch` | AI: Stop model/prompt/workflow (AIX-20) | V8 | API-451; API-144 | Partial | Partially covered | API-V12-H-056 |
| 78 | get_ai_models | GET | `/api/v1/ai/models` | AI: List model registry entries (AIX-02) | V8 | API-140; API-ADV-X1-12 | Partial | Partially covered | API-V12-H-049 |
| 79 | post_ai_models_id_promotion_requests | POST | `/api/v1/ai/models/{id}/promotion-requests` | AI: Request promotion; requires passing suites (AIX-05) | V8 | API-141 | Partial | Partially covered | API-V12-H-050 |
| 80 | get_ai_prompts | GET | `/api/v1/ai/prompts` | AI: List prompt versions (AIX-04) | V8 | API-142 | Partial | Partially covered | API-V12-H-051 |
| 81 | get_ai_red_team_results | GET | `/api/v1/ai/red-team/results` | AI: AI-INJ suite results (AIX-08) | V8 | API-ADV-X1-38 | Partial | Partially covered | API-V12-H-053 |
| 82 | get_ai_usage | GET | `/api/v1/ai/usage` | AI: Token usage and cost per accepted result (AIX-12, AIX-14) | V8 | API-135; API-136 | Partial | Partially covered | API-V12-H-055 |
| 83 | get_alerts | GET | `/api/v1/alerts` | SM-SVC-19: Used by SM-SVC-19-WF01 | SM-OP-082 | API-176 | Exact | Covered | — |
| 84 | post_alerts_id_read | POST | `/api/v1/alerts/{id}/read` | Screens: Screen A027 | SM-OP-084 | API-ENH-D-005 | New (Part 3.5b) | Covered | — |
| 85 | post_auth_login | POST | `/api/v1/auth/login` | Screens: Screen A001 | SM-OP-001 | API-001 | Alias (prefix) | Covered | — |
| 86 | post_auth_logout | POST | `/api/v1/auth/logout` | Screens: Screen A001 | SM-OP-005 | API-007;API-012 | Alias (prefix) | Covered | — |
| 87 | get_campaigns | GET | `/api/v1/campaigns` | SM-SVC-14: Used by SM-SVC-14-WF01 | SM-OP-166 | API-311 | Alias | Covered | — |
| 88 | post_campaigns | POST | `/api/v1/campaigns` | SM-SVC-14: Used by SM-SVC-14-WF01 | SM-OP-167 | API-292 | Exact | Covered | — |
| 89 | post_campaigns_id_approve | POST | `/api/v1/campaigns/{id}/approve` | SM-SVC-14: Used by SM-SVC-14-WF01 | SM-OP-168 | API-293 | Exact | Covered | — |
| 90 | post_campaigns_id_pause | POST | `/api/v1/campaigns/{id}/pause` | SM-SVC-30: Used by SM-SVC-30-WF01 | SM-OP-169 | API-316 | Alias | Covered | — |
| 91 | post_commercial_admin_external_grants | POST | `/api/v1/commercial/admin/external-grants` | SM-SVC-34: Used by SM-SVC-34-WF01 | SM-OP-293 | API-227 | Alias | Covered | — |
| 92 | post_commercial_admin_external_grants_id_control | POST | `/api/v1/commercial/admin/external-grants/{id}/control` | SM-SVC-34: Used by SM-SVC-34-WF01 | SM-OP-294 | API-ENH-D-017 | New (Part 3.5b) | Covered | — |
| 93 | get_commercial_workspace_admin_conflicts | GET | `/api/v1/commercial/workspace/admin/conflicts` | SM-SVC-08: Used by SM-SVC-08-WF01 | SM-UX-API-12 | API-473 | Alias | Covered | — |
| 94 | post_commercial_workspace_admin_conflicts_id_resolve | POST | `/api/v1/commercial/workspace/admin/conflicts/{id}/resolve` | SM-SVC-08: Used by SM-SVC-08-WF01 | SM-UX-API-13 | API-475;API-476 | Split | Covered | — |
| 95 | get_compliance_packs | GET | `/api/v1/compliance/packs` | Compliance: List jurisdiction packs (CJ-R01) | V8 | API-077 | Alias | Covered | — |
| 96 | get_compliance_packs_id_rules | GET | `/api/v1/compliance/packs/{id}/rules` | Compliance: Rules with legal source and status | V8 | API-077 | Partial | Partially covered | API-V12-H-057 |
| 97 | post_compliance_preflight | POST | `/api/v1/compliance/preflight` | Compliance: Send preflight decision (CJ-R02) | V8 | API-068 | Alias | Covered | — |
| 98 | get_consents | GET | `/api/v1/consents` | Compliance: Search consent ledger (CJ-R04) | V8 | API-076 | Partial | Partially covered | API-V12-H-058 |
| 99 | post_consents | POST | `/api/v1/consents` | SM-SVC-03: Used by SM-SVC-03-WF01 | V8 | API-066 | Exact | Covered | — |
| 100 | post_consents_id_withdraw | POST | `/api/v1/consents/{id}/withdraw` | Compliance: Withdraw consent and suppress (CJ-R05) | V8 | API-067; API-082 | Partial | Partially covered | API-V12-H-059 |
| 101 | get_contacts_verification_queue | GET | `/api/v1/contacts/verification-queue` | SM-SVC-03: Used by SM-SVC-03-WF01 | SM-OP-077 | API-200 | Alias | Covered | — |
| 102 | patch_contacts_id | PATCH | `/api/v1/contacts/{id}` | SM-SVC-03: Used by SM-SVC-03-WF01 | SM-OP-079 | API-197 | Alias | Covered | — |
| 103 | post_contacts_id_verify | POST | `/api/v1/contacts/{id}/verify` | SM-SVC-03: Used by SM-SVC-03-WF01 | SM-OP-078 | API-174 | Exact | Covered | — |
| 104 | get_content | GET | `/api/v1/content` | SM-SVC-11: Used by SM-SVC-11-WF01 | SM-OP-147 | API-299 | Alias | Covered | — |
| 105 | post_content_draft | POST | `/api/v1/content/draft` | SM-SVC-11: Used by SM-SVC-11-WF01 | SM-OP-148 | API-284 | Exact | Covered | — |
| 106 | patch_content_id | PATCH | `/api/v1/content/{id}` | SM-SVC-11: Used by SM-SVC-11-WF01 | SM-OP-149 | API-301 | Alias | Covered | — |
| 107 | post_content_id_approve | POST | `/api/v1/content/{id}/approve` | SM-SVC-11: Used by SM-SVC-11-WF01 | SM-OP-150 | API-285 | Exact | Covered | — |
| 108 | get_contracts | GET | `/api/v1/contracts` | SM-SVC-18: Used by SM-SVC-18-WF01 | SM-OP-194 | API-348 | Alias | Covered | — |
| 109 | post_contracts | POST | `/api/v1/contracts` | SM-SVC-18: Used by SM-SVC-18-WF01 | SM-OP-195 | API-332 | Exact | Covered | — |
| 110 | post_contracts_id_approve | POST | `/api/v1/contracts/{id}/approve` | SM-SVC-18: Used by SM-SVC-18-WF01 | SM-OP-198 | API-541;API-539 | Approval | Covered | — |
| 111 | get_deals | GET | `/api/v1/deals` | SM-SVC-05: Used by SM-SVC-05-WF01 | SM-OP-085 | API-209 | Exact | Covered | — |
| 112 | post_deals | POST | `/api/v1/deals` | SM-SVC-05: Used by SM-SVC-05-WF01 | SM-OP-086 | API-210 | Exact | Covered | — |
| 113 | get_deals_id | GET | `/api/v1/deals/{id}` | SM-SVC-05: Used by SM-SVC-05-WF01 | SM-OP-087 | API-214;API-217 | Split | Covered | — |
| 114 | post_deals_id_assign | POST | `/api/v1/deals/{id}/assign` | SM-SVC-05: Used by SM-SVC-05-WF01 | SM-OP-091 | API-216 | Alias | Covered | — |
| 115 | post_deals_id_close | POST | `/api/v1/deals/{id}/close` | SM-SVC-21: Used by SM-SVC-21-WF01 | SM-OP-205 | API-386 | Exact | Covered | — |
| 116 | post_deals_id_invoices | POST | `/api/v1/deals/{id}/invoices` | SM-SVC-21: Used by SM-SVC-21-WF01 | SM-OP-202 | API-390 | Alias | Covered | — |
| 117 | post_deals_id_lost | POST | `/api/v1/deals/{id}/lost` | SM-SVC-23: Used by SM-SVC-23-WF01 | SM-OP-220 | API-387 | Exact | Covered | — |
| 118 | get_deals_id_objections | GET | `/api/v1/deals/{id}/objections` | SM-SVC-18: Used by SM-SVC-18-WF01 | SM-OP-191 | API-343 | Alias | Covered | — |
| 119 | post_deals_id_objections | POST | `/api/v1/deals/{id}/objections` | SM-SVC-18: Used by SM-SVC-18-WF01 | SM-OP-192 | API-331 | Exact | Covered | — |
| 120 | get_deals_id_payments | GET | `/api/v1/deals/{id}/payments` | SM-SVC-21: Used by SM-SVC-21-WF01 | SM-OP-201 | API-393 | Alias | Covered | — |
| 121 | get_deals_id_proposals | GET | `/api/v1/deals/{id}/proposals` | SM-SVC-17: Used by SM-SVC-17-WF01 | SM-OP-185 | API-334;API-335 | Split | Covered | — |
| 122 | post_deals_id_proposals | POST | `/api/v1/deals/{id}/proposals` | SM-SVC-17: Used by SM-SVC-17-WF01 | SM-OP-186 | API-328 | Exact | Covered | — |
| 123 | post_deals_id_transition | POST | `/api/v1/deals/{id}/transition` | SM-SVC-29: Used by SM-SVC-29-WF01 | SM-OP-088 | API-211 | Exact | Covered | — |
| 124 | get_deployments | GET | `/api/v1/deployments` | Screens: Screen A095 | SM-OP-242 | API-421 | Exact | Covered | — |
| 125 | patch_deployments_id | PATCH | `/api/v1/deployments/{id}` | Screens: Screen A095 | SM-OP-244 | API-435 | Alias | Covered | — |
| 126 | post_deployments_id_approve | POST | `/api/v1/deployments/{id}/approve` | Screens: Screen A096 | SM-OP-243 | API-541;API-539 | Approval | Covered | — |
| 127 | get_dsar | GET | `/api/v1/dsar` | Compliance: Tenant DSAR queue | V8 | API-084 | Alias | Covered | — |
| 128 | post_dsar_id_complete | POST | `/api/v1/dsar/{id}/complete` | Compliance: Complete with evidence; legal-hold check | V8 | API-086 | Alias | Covered | — |
| 129 | post_dsar_id_verify | POST | `/api/v1/dsar/{id}/verify` | Compliance: Record identity verification | V8 | API-085 | Alias | Covered | — |
| 130 | post_engagement_check | POST | `/api/v1/engagement/check` | SM-SVC-05: Used by SM-SVC-05-WF01 | SM-OP-097 | API-068 | Exact | Covered | — |
| 131 | get_enrollments | GET | `/api/v1/enrollments` | Screens: Screen A038 | SM-OP-120 | API-263 | Alias | Covered | — |
| 132 | post_enrollments_id_stop | POST | `/api/v1/enrollments/{id}/stop` | SM-SVC-08: Used by SM-SVC-08-WF01 | SM-OP-119 | API-264 | Alias | Covered | — |
| 133 | get_events | GET | `/api/v1/events` | Screens: Screen A009 | SM-OP-027 | API-115 | Exact | Covered | — |
| 134 | get_events_business | GET | `/api/v1/events/business` | SM-SVC-10: Used by SM-SVC-10-WF01 | SM-OP-175 | API-322 | Alias | Covered | — |
| 135 | post_events_business | POST | `/api/v1/events/business` | SM-SVC-16: Used by SM-SVC-16-WF01 | SM-OP-176 | API-323 | Alias | Covered | — |
| 136 | get_evidence | GET | `/api/v1/evidence` | Screens: Screen A017 | SM-OP-057 | API-186 | Alias | Covered | — |
| 137 | get_evidence_id | GET | `/api/v1/evidence/{id}` | Screens: Screen A017 | SM-OP-056 | API-163 | Exact | Covered | — |
| 138 | get_feedback | GET | `/api/v1/feedback` | SM-SVC-23: Used by SM-SVC-23-WF01 | SM-OP-222 | API-431 | Alias | Covered | — |
| 139 | post_feedback | POST | `/api/v1/feedback` | SM-SVC-23: Used by SM-SVC-23-WF01 | SM-OP-221 | API-418 | Exact | Covered | — |
| 140 | get_inbox | GET | `/api/v1/inbox` | SM-SVC-08: Used by SM-SVC-08-WF01 | SM-OP-139 | API-247 | Exact | Covered | — |
| 141 | get_incidents | GET | `/api/v1/incidents` | Compliance: Incident register (CJ-R08) | V8 | API-070; API-092 | Alias | Covered | — |
| 142 | post_incidents | POST | `/api/v1/incidents` | Compliance: Open incident; clocks start | V8 | — | New | Not covered | API-V12-H-060 |
| 143 | post_incidents_id_notifications | POST | `/api/v1/incidents/{id}/notifications` | Compliance: Record authority/principal notification | V8 | — | New | Not covered | API-V12-H-061 |
| 144 | get_insurance_pilots | GET | `/api/v1/insurance/pilots` | SM-SVC-22: Used by SM-SVC-22-WF01 | SM-OP-236 | API-ENH-D-011 | New (Part 3.5b) | Covered | — |
| 145 | post_insurance_pilots_id_approve | POST | `/api/v1/insurance/pilots/{id}/approve` | SM-SVC-22: Used by SM-SVC-22-WF01 | SM-OP-238 | API-541;API-539 | Approval | Covered | — |
| 146 | get_integration_enquiries | GET | `/api/v1/integration-enquiries` | SM-SVC-18: Used by SM-SVC-18-WF01 | SM-OP-239 | API-433 | Alias | Covered | — |
| 147 | post_integration_enquiries | POST | `/api/v1/integration-enquiries` | Screens: Screen A093 | SM-OP-240 | API-420 | Exact | Covered | — |
| 148 | post_integration_enquiries_id_approve | POST | `/api/v1/integration-enquiries/{id}/approve` | Screens: Screen A094 | SM-OP-241 | API-541;API-539 | Approval | Covered | — |
| 149 | get_integrations | GET | `/api/v1/integrations` | Screens: Screen A008 | SM-OP-023 | API-095 | Exact | Covered | — |
| 150 | post_invoices_id_payment_link | POST | `/api/v1/invoices/{id}/payment-link` | Screens: Screen A073 | SM-OP-207 | API-398 | Alias | Covered | — |
| 151 | get_knowledge_documents | GET | `/api/v1/knowledge/documents` | SM-SVC-25: Used by SM-SVC-25-WF01 | SM-OP-013 | API-061 | Alias | Covered | — |
| 152 | post_knowledge_documents_id_review | POST | `/api/v1/knowledge/documents/{id}/review` | SM-SVC-25: Used by SM-SVC-25-WF01 | SM-OP-014 | API-541;API-539 | Approval | Covered | — |
| 153 | get_knowledge_search | GET | `/api/v1/knowledge/search` | SM-SVC-25: Used by SM-SVC-25-WF01 | SM-OP-015 | API-052 | Exact | Covered | — |
| 154 | post_knowledge_uploads | POST | `/api/v1/knowledge/uploads` | SM-SVC-25: Used by SM-SVC-25-WF01 | SM-OP-012 | API-051 | Exact | Covered | — |
| 155 | get_landing_pages | GET | `/api/v1/landing-pages` | SM-SVC-13: Used by SM-SVC-13-WF01 | SM-OP-161 | API-308 | Alias | Covered | — |
| 156 | post_landing_pages | POST | `/api/v1/landing-pages` | SM-SVC-13: Used by SM-SVC-13-WF01 | SM-OP-162 | API-309 | Alias | Covered | — |
| 157 | post_landing_pages_id_publish | POST | `/api/v1/landing-pages/{id}/publish` | SM-SVC-13: Used by SM-SVC-13-WF01 | SM-OP-163 | API-492 | Alias | Covered | — |
| 158 | get_market_competitors | GET | `/api/v1/market/competitors` | SM-SVC-01: Used by SM-SVC-01-WF01 | SM-OP-227 | API-178 | Exact | Covered | — |
| 159 | get_matches | GET | `/api/v1/matches` | SM-SVC-04: Used by SM-SVC-04-WF01 | SM-OP-068 | API-192 | Alias | Covered | — |
| 160 | post_matches_recompute | POST | `/api/v1/matches/recompute` | SM-SVC-04: Used by SM-SVC-04-WF01 | SM-OP-069 | API-170 | Exact | Covered | — |
| 161 | get_me | GET | `/api/v1/me` | Screens: Screen A001 | SM-OP-002 | API-002 | Alias (prefix) | Covered | — |
| 162 | get_meetings | GET | `/api/v1/meetings` | SM-SVC-10: Used by SM-SVC-10-WF01 | SM-OP-121 | API-268 | Alias | Covered | — |
| 163 | post_meetings_book | POST | `/api/v1/meetings/book` | SM-SVC-10: Used by SM-SVC-10-WF01 | SM-OP-123 | API-243 | Exact | Covered | — |
| 164 | post_messages_draft | POST | `/api/v1/messages/draft` | SM-SVC-06: Used by SM-SVC-06-WF01 | SM-OP-103 | API-237 | Exact | Covered | — |
| 165 | post_messages_drafts_id_review | POST | `/api/v1/messages/drafts/{id}/review` | SM-SVC-06: Used by SM-SVC-06-WF01 | SM-OP-106 | API-541;API-539 | Approval | Covered | — |
| 166 | post_messages_send | POST | `/api/v1/messages/send` | SM-SVC-09: Used by SM-SVC-09-WF01 | SM-OP-108 | API-238 | Exact | Covered | — |
| 167 | get_messages_id | GET | `/api/v1/messages/{id}` | SM-SVC-09: Used by SM-SVC-09-WF01 | SM-OP-110 | API-252;API-257; API-ENH-D-007 | Partial | Covered | — |
| 168 | get_metrics_forecast | GET | `/api/v1/metrics/forecast` | SM-SVC-24: Used by SM-SVC-24-WF01 | SM-OP-229 | API-389 | Exact | Covered | — |
| 169 | get_metrics_funnel | GET | `/api/v1/metrics/funnel` | SM-SVC-05: Used by SM-SVC-05-WF01 | SM-OP-127 | API-537 | Exact | Covered | — |
| 170 | get_metrics_revenue | GET | `/api/v1/metrics/revenue` | SM-SVC-21: Used by SM-SVC-21-WF01 | SM-OP-223 | API-388 | Exact | Covered | — |
| 171 | get_needs | GET | `/api/v1/needs` | SM-SVC-04: Used by SM-SVC-04-WF01 | SM-OP-066 | API-168 | Exact | Covered | — |
| 172 | post_needs_id_verify | POST | `/api/v1/needs/{id}/verify` | SM-SVC-04: Used by SM-SVC-04-WF01 | SM-OP-067 | API-169 | Exact | Covered | — |
| 173 | post_negotiations_id_review | POST | `/api/v1/negotiations/{id}/review` | SM-SVC-18: Used by SM-SVC-18-WF01 | SM-OP-193 | API-347 | Alias | Covered | — |
| 174 | get_onboarding | GET | `/api/v1/onboarding` | SM-SVC-20: Used by SM-SVC-20-WF01 | SM-OP-209 | API-412 | Exact | Covered | — |
| 175 | post_onboarding_id_assign | POST | `/api/v1/onboarding/{id}/assign` | SM-SVC-22: Used by SM-SVC-22-WF01 | SM-OP-212 | API-425 | Alias | Covered | — |
| 176 | post_onboarding_id_complete | POST | `/api/v1/onboarding/{id}/complete` | SM-SVC-20: Used by SM-SVC-20-WF01 | SM-OP-211 | API-413 | Exact | Covered | — |
| 177 | get_opportunities | GET | `/api/v1/opportunities` | SM-SVC-04: Used by SM-SVC-04-WF01 | SM-OP-070 | API-171 | Exact | Covered | — |
| 178 | post_opportunities_id_review | POST | `/api/v1/opportunities/{id}/review` | Screens: Screen A027 | SM-OP-081 | API-175 | Exact | Covered | — |
| 179 | post_opportunities_id_score | POST | `/api/v1/opportunities/{id}/score` | SM-SVC-04: Used by SM-SVC-04-WF01 | SM-OP-071 | API-172 | Exact | Covered | — |
| 180 | get_organizations | GET | `/api/v1/organizations` | SM-SVC-02: Used by SM-SVC-02-WF01 | SM-OP-059 | API-164 | Exact | Covered | — |
| 181 | post_organizations | POST | `/api/v1/organizations` | SM-SVC-02: Used by SM-SVC-02-WF01 | SM-OP-060 | API-165 | Exact | Covered | — |
| 182 | get_organizations_id | GET | `/api/v1/organizations/{id}` | SM-SVC-02: Used by SM-SVC-02-WF01 | SM-OP-061 | API-189 | Alias | Covered | — |
| 183 | get_organizations_id_360 | GET | `/api/v1/organizations/{id}/360` | SM-SVC-05: Used by SM-SVC-05-WF01 | SM-OP-096 | API-213 | Exact | Covered | — |
| 184 | get_organizations_id_contacts | GET | `/api/v1/organizations/{id}/contacts` | SM-SVC-03: Used by SM-SVC-03-WF01 | SM-OP-073 | API-173 | Exact | Covered | — |
| 185 | post_organizations_id_contacts_discover | POST | `/api/v1/organizations/{id}/contacts/discover` | SM-SVC-03: Used by SM-SVC-03-WF01 | SM-OP-074 | API-196 | Alias | Covered | — |
| 186 | post_organizations_id_merge | POST | `/api/v1/organizations/{id}/merge` | SM-SVC-03: Used by SM-SVC-03-WF01 | SM-OP-062 | API-190;API-191 | Split | Covered | — |
| 187 | post_partner_pilots | POST | `/api/v1/partner-pilots` | SM-SVC-32: Used by SM-SVC-32-WF01 | SM-OP-216 | API-419 | Alias | Covered | — |
| 188 | get_partners | GET | `/api/v1/partners` | SM-SVC-20: Used by SM-SVC-20-WF01 | SM-OP-213 | API-427 | Alias | Covered | — |
| 189 | post_partners | POST | `/api/v1/partners` | SM-SVC-20: Used by SM-SVC-20-WF01 | SM-OP-214 | API-414 | Exact | Covered | — |
| 190 | post_payments_id_reconcile | POST | `/api/v1/payments/{id}/reconcile` | SM-SVC-39: Used by SM-SVC-39-WF01 | SM-OP-206 | API-394;API-395;API-396 | Split | Covered | — |
| 191 | post_pilots | POST | `/api/v1/pilots` | SM-SVC-22: Used by SM-SVC-22-WF01 | SM-OP-237 | API-419 | Exact | Covered | — |
| 192 | post_pilots_id_status | POST | `/api/v1/pilots/{id}/status` | SM-SVC-22: Used by SM-SVC-22-WF01 | SM-OP-215 | API-415 | Exact | Covered | — |
| 193 | post_privacy_requests | POST | `/api/v1/privacy/requests` | Screens: Screen A013 | SM-OP-041 | API-069 | Exact | Covered | — |
| 194 | get_products | GET | `/api/v1/products` | SM-SVC-11: Used by SM-SVC-11-WF01 | SM-OP-006 | API-048 | Exact | Covered | — |
| 195 | get_products_id | GET | `/api/v1/products/{id}` | SM-SVC-25: Used by SM-SVC-25-WF01 | SM-OP-007 | API-054 | Alias | Covered | — |
| 196 | post_proposals_id_review | POST | `/api/v1/proposals/{id}/review` | SM-SVC-17: Used by SM-SVC-17-WF01 | SM-OP-187 | API-541;API-539 | Approval | Covered | — |
| 197 | post_public_cookie_consent | POST | `/api/v1/public/cookie-consent` | Compliance: Record cookie choice with notice version (CJ-R12) | V8 | — | New | Not covered | API-V12-H-062 |
| 198 | post_public_data_rights_requests | POST | `/api/v1/public/data-rights-requests` | Compliance: Public DSAR intake, rate-limited (CJ-R07) | V8 | API-069 | Alias | Covered | — |
| 199 | get_quotes | GET | `/api/v1/quotes` | SM-SVC-17: Used by SM-SVC-17-WF01 | SM-OP-188 | API-338 | Alias | Covered | — |
| 200 | post_quotes | POST | `/api/v1/quotes` | SM-SVC-17: Used by SM-SVC-17-WF01 | SM-OP-189 | API-329 | Exact | Covered | — |
| 201 | post_quotes_id_approve | POST | `/api/v1/quotes/{id}/approve` | SM-SVC-17: Used by SM-SVC-17-WF01 | SM-OP-190 | API-330 | Exact | Covered | — |
| 202 | get_renewals | GET | `/api/v1/renewals` | SM-SVC-23: Used by SM-SVC-23-WF01 | SM-OP-217 | API-416 | Exact | Covered | — |
| 203 | post_renewals_id_review | POST | `/api/v1/renewals/{id}/review` | SM-SVC-23: Used by SM-SVC-23-WF01 | SM-OP-218 | API-417 | Exact | Covered | — |
| 204 | get_research_plans | GET | `/api/v1/research/plans` | SM-SVC-01: Used by SM-SVC-01-WF01 | SM-OP-049 | API-180 | Alias | Covered | — |
| 205 | post_research_plans | POST | `/api/v1/research/plans` | SM-SVC-01: Used by SM-SVC-01-WF01 | SM-OP-050 | API-160 | Exact | Covered | — |
| 206 | patch_research_plans_id | PATCH | `/api/v1/research/plans/{id}` | Screens: Screen A015 | SM-OP-052 | API-181 | Alias | Covered | — |
| 207 | get_research_results | GET | `/api/v1/research/results` | SM-SVC-01: Used by SM-SVC-01-WF01 | SM-OP-053 | API-162 | Exact | Covered | — |
| 208 | post_research_run | POST | `/api/v1/research/run` | Screens: Screen A015 | SM-OP-051 | API-161 | Exact | Covered | — |
| 209 | get_research_runs_id | GET | `/api/v1/research/runs/{id}` | SM-SVC-01: Used by SM-SVC-01-WF01 | SM-OP-054 | API-183 | Alias | Covered | — |
| 210 | get_sales_action_plans | GET | `/api/v1/sales/action-plans` | Screens: Screen A102 | SM-OP-269 | API-453 | Alias | Covered | — |
| 211 | post_sales_action_plans | POST | `/api/v1/sales/action-plans` | Screens: Screen A102 | SM-OP-270 | API-454;API-455 | Split | Covered | — |
| 212 | post_sales_action_plans_id_control | POST | `/api/v1/sales/action-plans/{id}/control` | Screens: Screen A102 | SM-OP-271 | API-456;API-457;API-458;API-541;API-539 | Split | Covered | — |
| 213 | get_sales_bids | GET | `/api/v1/sales/bids` | SM-SVC-19: Used by SM-SVC-19-WF01 | SM-OP-277 | API-362 | Alias | Covered | — |
| 214 | post_sales_bids | POST | `/api/v1/sales/bids` | SM-SVC-19: Used by SM-SVC-19-WF01 | SM-OP-278 | API-363 | Alias | Covered | — |
| 215 | patch_sales_bids_id | PATCH | `/api/v1/sales/bids/{id}` | SM-SVC-19: Used by SM-SVC-19-WF01 | SM-OP-279 | API-365 | Alias | Covered | — |
| 216 | post_sales_bids_id_control | POST | `/api/v1/sales/bids/{id}/control` | Screens: Screen A104 | SM-OP-280 | API-366;API-367;API-368;API-369;API-541;API-539 | Split | Covered | — |
| 217 | get_sales_data_transfers | GET | `/api/v1/sales/data-transfers` | Screens: Screen A103 | SM-OP-272 | API-530 | Alias | Covered | — |
| 218 | post_sales_data_transfers | POST | `/api/v1/sales/data-transfers` | Screens: Screen A103 | SM-OP-273 | API-531;API-534 | Split | Covered | — |
| 219 | post_sales_data_transfers_id_complete | POST | `/api/v1/sales/data-transfers/{id}/complete` | Screens: Screen A103 | SM-OP-274 | API-532 | Alias | Covered | — |
| 220 | post_sales_data_transfers_id_control | POST | `/api/v1/sales/data-transfers/{id}/control` | Screens: Screen A103 | SM-OP-275 | API-536;API-541;API-539 | Split | Covered | — |
| 221 | get_sales_data_transfers_id_download | GET | `/api/v1/sales/data-transfers/{id}/download` | Screens: Screen A103 | SM-OP-276 | API-535 | Alias | Covered | — |
| 222 | get_sales_domains | GET | `/api/v1/sales/domains` | Screens: Screen A100 | SM-OP-258 | API-044 | Alias | Covered | — |
| 223 | post_sales_domains | POST | `/api/v1/sales/domains` | Screens: Screen A100 | SM-OP-259 | API-045 | Alias | Covered | — |
| 224 | post_sales_domains_id_control | POST | `/api/v1/sales/domains/{id}/control` | Screens: Screen A100 | SM-OP-260 | API-046; API-ENH-D-012 | Partial | Covered | — |
| 225 | post_sales_memberships | POST | `/api/v1/sales/memberships` | Screens: Screen A099 | SM-OP-253 | API-020;API-022 | Split | Covered | — |
| 226 | post_sales_milestones_id_accept | POST | `/api/v1/sales/milestones/{id}/accept` | SM-SVC-31: Used by SM-SVC-31-WF01 | SM-OP-286 | API-383;API-384; API-ENH-D-016 | Partial | Covered | — |
| 227 | get_sales_notifications | GET | `/api/v1/sales/notifications` | Screens: Screen A106 | SM-OP-287 | API-549 | Alias | Covered | — |
| 228 | patch_sales_notifications_id | PATCH | `/api/v1/sales/notifications/{id}` | Screens: Screen A106 | SM-OP-288 | API-550;API-552 | Split | Covered | — |
| 229 | get_sales_orders | GET | `/api/v1/sales/orders` | SM-SVC-20: Used by SM-SVC-20-WF01 | SM-OP-281 | API-370 | Alias | Covered | — |
| 230 | post_sales_orders | POST | `/api/v1/sales/orders` | SM-SVC-20: Used by SM-SVC-20-WF01 | SM-OP-282 | API-371 | Alias | Covered | — |
| 231 | patch_sales_orders_id | PATCH | `/api/v1/sales/orders/{id}` | SM-SVC-20: Used by SM-SVC-20-WF01 | SM-OP-283 | API-373 | Alias | Covered | — |
| 232 | post_sales_orders_id_control | POST | `/api/v1/sales/orders/{id}/control` | SM-SVC-28: Used by SM-SVC-28-WF01 | SM-OP-284 | API-374;API-375;API-376;API-378 | Split | Covered | — |
| 233 | post_sales_orders_id_milestones | POST | `/api/v1/sales/orders/{id}/milestones` | SM-SVC-31: Used by SM-SVC-31-WF01 | SM-OP-285 | API-377 | Alias | Covered | — |
| 234 | get_sales_service_invoices | GET | `/api/v1/sales/service-invoices` | Screens: Screen A101 | SM-OP-265 | API-526 | Alias | Covered | — |
| 235 | post_sales_service_invoices_id_reconcile | POST | `/api/v1/sales/service-invoices/{id}/reconcile` | Screens: Screen A101 | SM-OP-266 | API-ENH-D-013 | New (Part 3.5b) | Covered | — |
| 236 | get_sales_service_plans | GET | `/api/v1/sales/service-plans` | Screens: Screen A101 | SM-OP-261 | API-519 | Alias | Covered | — |
| 237 | post_sales_service_plans | POST | `/api/v1/sales/service-plans` | Screens: Screen A101 | SM-OP-262 | API-520;API-541;API-539 | Split | Covered | — |
| 238 | get_sales_service_subscriptions | GET | `/api/v1/sales/service-subscriptions` | Screens: Screen A101 | SM-OP-263 | API-521 | Alias | Covered | — |
| 239 | post_sales_service_subscriptions_id_control | POST | `/api/v1/sales/service-subscriptions/{id}/control` | Screens: Screen A101 | SM-OP-264 | API-522;API-523;API-524;API-525 | Split | Covered | — |
| 240 | get_sales_startups | GET | `/api/v1/sales/startups` | Screens: Screen A099 | SM-OP-250 | API-029 | Alias | Covered | — |
| 241 | post_sales_startups | POST | `/api/v1/sales/startups` | Screens: Screen A099 | SM-OP-251 | API-030 | Alias | Covered | — |
| 242 | patch_sales_startups_id | PATCH | `/api/v1/sales/startups/{id}` | Screens: Screen A099 | SM-OP-252 | API-031;API-039 | Split | Covered | — |
| 243 | post_sales_support_grants | POST | `/api/v1/sales/support-grants` | Screens: Screen A099 | SM-OP-254 | API-024;API-025 | Split | Covered | — |
| 244 | get_sales_templates | GET | `/api/v1/sales/templates` | Screens: Screen A100 | SM-OP-255 | API-033 | Alias | Covered | — |
| 245 | post_sales_templates | POST | `/api/v1/sales/templates` | Screens: Screen A100 | SM-OP-256 | API-034 | Alias | Covered | — |
| 246 | post_sales_templates_id_control | POST | `/api/v1/sales/templates/{id}/control` | Screens: Screen A100 | SM-OP-257 | API-035;API-036;API-037;API-541;API-539 | Split | Covered | — |
| 247 | get_sales_tenants | GET | `/api/v1/sales/tenants` | Screens: Screen A099 | SM-OP-247 | API-026 | Alias | Covered | — |
| 248 | post_sales_tenants | POST | `/api/v1/sales/tenants` | Screens: Screen A099 | SM-OP-248 | API-027 | Alias | Covered | — |
| 249 | post_sales_tenants_id_control | POST | `/api/v1/sales/tenants/{id}/control` | Screens: Screen A099 | SM-OP-249 | API-028 | Alias | Covered | — |
| 250 | get_sales_usage_charges | GET | `/api/v1/sales/usage-charges` | Screens: Screen A101 | SM-OP-267 | API-528; API-ENH-D-014 | Partial | Covered | — |
| 251 | post_sales_usage_charges_id_adjust | POST | `/api/v1/sales/usage-charges/{id}/adjust` | Screens: Screen A101 | SM-OP-268 | API-ENH-D-015 | New (Part 3.5b) | Covered | — |
| 252 | get_seo_audit | GET | `/api/v1/seo/audit` | SM-SVC-13: Used by SM-SVC-13-WF01 | SM-OP-157 | API-288 | Exact | Covered | — |
| 253 | post_seo_audit_run | POST | `/api/v1/seo/audit/run` | SM-SVC-13: Used by SM-SVC-13-WF01 | SM-OP-159 | API-289 | Alias | Covered | — |
| 254 | post_seo_tasks | POST | `/api/v1/seo/tasks` | SM-SVC-13: Used by SM-SVC-13-WF01 | SM-OP-158 | API-289 | Exact | Covered | — |
| 255 | get_sequences | GET | `/api/v1/sequences` | SM-SVC-08: Used by SM-SVC-08-WF01 | SM-OP-116 | API-261 | Alias | Covered | — |
| 256 | post_sequences_id_enroll | POST | `/api/v1/sequences/{id}/enroll` | SM-SVC-08: Used by SM-SVC-08-WF01 | SM-OP-118 | API-242 | Exact | Covered | — |
| 257 | get_signals | GET | `/api/v1/signals` | Screens: Screen A019 | SM-OP-063 | API-166 | Exact | Covered | — |
| 258 | post_signals_id_review | POST | `/api/v1/signals/{id}/review` | Screens: Screen A019 | SM-OP-064 | API-167 | Exact | Covered | — |
| 259 | get_social_posts | GET | `/api/v1/social/posts` | SM-SVC-11: Used by SM-SVC-11-WF01 | SM-OP-151 | API-302 | Alias | Covered | — |
| 260 | post_social_posts | POST | `/api/v1/social/posts` | SM-SVC-11: Used by SM-SVC-11-WF01 | SM-OP-152 | API-286 | Exact | Covered | — |
| 261 | post_social_posts_id_cancel | POST | `/api/v1/social/posts/{id}/cancel` | SM-SVC-27: Used by SM-SVC-27-WF01 | SM-OP-155 | API-303 | Alias | Covered | — |
| 262 | get_social_signals | GET | `/api/v1/social/signals` | SM-SVC-12: Used by SM-SVC-12-WF01 | SM-OP-144 | API-177 | Exact | Covered | — |
| 263 | get_social_status | GET | `/api/v1/social/status` | SM-SVC-11: Used by SM-SVC-11-WF01 | SM-OP-153 | API-287 | Exact | Covered | — |
| 264 | get_sources | GET | `/api/v1/sources` | SM-SVC-01: Used by SM-SVC-01-WF01 | SM-OP-030 | API-158 | Exact | Covered | — |
| 265 | get_suppressions | GET | `/api/v1/suppressions` | Compliance: List suppressions | V8 | API-074 | Alias | Covered | — |
| 266 | get_tasks | GET | `/api/v1/tasks` | SM-SVC-24: Used by SM-SVC-24-WF01 | SM-OP-128 | API-265 | Alias | Covered | — |
| 267 | patch_tasks_id | PATCH | `/api/v1/tasks/{id}` | SM-SVC-24: Used by SM-SVC-24-WF01 | SM-OP-129 | API-266 | Alias | Covered | — |
| 268 | get_threads | GET | `/api/v1/threads` | SM-SVC-26: Used by SM-SVC-26-WF01 | SM-OP-113 | API-241 | Exact | Covered | — |
| 269 | post_threads_id_assign | POST | `/api/v1/threads/{id}/assign` | SM-SVC-08: Used by SM-SVC-08-WF01 | SM-OP-140 | API-248 | Exact | Covered | — |
| 270 | post_threads_id_handoff | POST | `/api/v1/threads/{id}/handoff` | SM-SVC-26: Used by SM-SVC-26-WF01 | SM-OP-115 | API-259 | Alias | Covered | — |
| 271 | get_threads_id_messages | GET | `/api/v1/threads/{id}/messages` | SM-SVC-26: Used by SM-SVC-26-WF01 | SM-OP-114 | API-257 | Alias | Covered | — |
| 272 | post_webhooks_calendar | POST | `/api/v1/webhooks/calendar` | SM-SVC-10: Used by SM-SVC-10-WF01 | SM-OP-124 | API-244 | Exact | Covered | — |
| 273 | post_webhooks_email | POST | `/api/v1/webhooks/email` | SM-SVC-09: Used by SM-SVC-09-WF01 | SM-OP-109 | API-239 | Exact | Covered | — |
| 274 | post_webhooks_esign | POST | `/api/v1/webhooks/esign` | SM-SVC-18: Used by SM-SVC-18-WF01 | SM-OP-199 | API-333 | Exact | Covered | — |
| 275 | post_webhooks_events | POST | `/api/v1/webhooks/events` | SM-SVC-16: Used by SM-SVC-16-WF01 | SM-OP-179 | API-297 | Exact | Covered | — |
| 276 | post_webhooks_inbound | POST | `/api/v1/webhooks/inbound` | SM-SVC-26: Used by SM-SVC-26-WF01 | SM-OP-112 | API-240 | Exact | Covered | — |
| 277 | post_webhooks_payment | POST | `/api/v1/webhooks/payment` | SM-SVC-21: Used by SM-SVC-21-WF01 | SM-OP-204 | API-385 | Exact | Covered | — |
| 278 | get_webhooks_whatsapp | GET | `/api/v1/webhooks/whatsapp` | SM-SVC-09: Used by SM-SVC-09-WF01 | SM-OP-133 | API-249 | Exact | Covered | — |
| 279 | post_webhooks_whatsapp | POST | `/api/v1/webhooks/whatsapp` | SM-SVC-09: Used by SM-SVC-09-WF01 | SM-OP-134 | API-245 | Exact | Covered | — |
| 280 | get_whatsapp_conversations | GET | `/api/v1/whatsapp/conversations` | Screens: Screen A045 | SM-OP-135 | API-241 | Alias | Covered | — |
| 281 | get_workflows | GET | `/api/v1/workflows` | Screens: Screen A033 | SM-OP-098 | API-444 | Exact | Covered | — |
| 282 | get_workflows_id_executions | GET | `/api/v1/workflows/{id}/executions` | Screens: Screen A033 | SM-OP-102 | API-466 | Alias | Covered | — |
