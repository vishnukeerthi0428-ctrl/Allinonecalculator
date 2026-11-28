# AI Growth Engine: Employee Sales & Marketing Automation
## Application Blueprint: PART 11 (Batch 11.9a), V12 Database Schema, DDL with RLS: Material, Coverage and Catalogue Reconciliation

| Field | Value |
|---|---|
| Document | Part 11, Batch 11.9a · Customer revision V12 (28 Nov 2026), Group R8 letter I: FSD V12 chapter 26 (PostgreSQL Database Schema Master), Appendix C (PostgreSQL DDL with row-level security), Appendix C2 (Enterprise schema additions), chapter 29 (Analytics, Attribution and KPI Engineering), chapter 31 (Cybersecurity, Privacy and Threat Management) and the database files of the FSD source archive `src/engineering/` |
| Version | 1.0 · 28 Nov 2026 |
| Baseline | Parts 0–9.10 and 0B; DEC-001…422; Part 3.3 (199 entities), Part 3.6a/b (155 source tables), Part 4.1, Part 9.9; hosting **DEC-421 (Vercel + Supabase PostgreSQL, Mumbai)**; running budget DEC-422; sibling V12 batches Part 11.5a (DEC-581 tenancy vocabulary, CONFLICT-832 regions) |
| Companion files | **Part 11.9b** (DDL-V12-I "Appendix C3": full DDL, RLS, indexes, Supabase privilege model, tests) · **Part 11.9c** (security controls, STRIDE, DPDP privacy, analytics, attribution, KPI formulas, conflicts, decisions, persona review, tags, quality gate) |
| Machine-readable outputs | `final/coverage_v12/I_coverage.csv` (3,248 aspect rows) · scripts and evidence in `assembly/v12/` (`I_build_coverage.py`, `I_fragments.py`, `i_ddl/parse_tables.py`, `i_ddl/analyze_catalog.sql`, `i_ddl/gen_c3.py`, `i_ddl/run_all.sh`, test outputs `*.out`) |
| Roles applied | Principal Data Architect / PostgreSQL DBA (lead: RLS, partitioning, indexing), CISO (zero trust, DPDP/GDPR, SOC 2), Chief Data Officer (analytics, attribution, KPI engineering), Threat-modelling lead; supported by QA Lead and FinOps Lead |
| ID ranges used | DEC-660…679 · ADR-210…214 · ASSUMPTION/GAP/CONFLICT/RECOMMENDATION-904…921 · FR-V12-I-### · US-<EP>-YI<nn> · TC-V12-I-### · namespaced registers THR-V12-I-##, SC-V12-I-##, MET-V12-I-## (new prefixes, no collision with THR-001…082, SC-01…50, KPI-01…31) |

**Acronyms used in this part.** BRIN block-range index · CMK customer-managed key · DEK data-encryption key · DLP data-loss prevention · DPDP Digital Personal Data Protection (Act 2023, Rules 2025) · DSAR data-subject (data-principal) access request · FK foreign key · GIN generalized inverted index · HNSW hierarchical navigable small world (vector index) · KEK key-encryption key · PDP Policy Decision Point · PK primary key · RLS row-level security · SBOM software bill of materials · SCIM System for Cross-domain Identity Management · SIEM security information and event management · SoD separation of duties · SSO single sign-on · STRIDE Spoofing, Tampering, Repudiation, Information disclosure, Denial of service, Elevation of privilege · Supavisor the Supabase connection pooler.

**How this part treats the customer text.** All V12 document content was handled as data. Per the V12 brief, active V12 sections are authoritative, and earlier version sections (V4…V11) stay normative unless superseded. V12 identifiers are adopted literally and mapped to blueprint identifiers. Where V12 clashes with a Founder decision (DEC-421 hosting, DEC-422 budget, DEC-228 staffing) a conflict is raised and the item is marked **Pending Founder decision**. No safety invariant is weakened. Every proposal of the customer DDL was **executed** on PostgreSQL 16.15, not only read.

---

## 11.9.1 Material reviewed

### 11.9.1.1 Files, sizes and purpose

| # | File (V12 pack) | Size | Sections / rows | Purpose | Pattern | Aspects |
|---|---|---|---|---|---|---|
| 1 | `FSD/26_PostgreSQL_Database_Schema_Master.txt` | 91,065 B · 2,201 lines | 8 version sections (V12, V8, V6, V5, V4) · 47 tables · 68 prose lines | Data control requirements ENT-DAT-01…05; C2-T1…T11 and DB-T1…T9 database tests; V6 canonical entity graph (16 entities) and MT-09/10/11/18/33; V5 GC-05, ST-12, 9 `opt_*` and 10 `DB-V2-*` candidate entities; 39 per-service domain schemas (324 fields); 149 historical entities; 5 V4 persistence additions | Requirement tables + entity tables + field tables | 572 |
| 2 | `FSD/AP_Appendix_C_PostgreSQL_DDL_with_row_level.txt` | 96,436 B · 679 lines | 118 tables · 1,206 columns · 241 constraints · 106 RLS policies · 2 extensions | Proposed PostgreSQL 16 DDL (V7), tested by the customer on 16.15; 29 core tables + 89 generic domain tables referenced by the 156 workflows | SQL | 1,683 (incl. analysis findings) |
| 3 | `FSD/AP_Appendix_C2_Enterprise_schema_additions.txt` | 11,461 B · 88 lines | 19 tables · 120 columns · 69 constraints · 14 policies · 1 trigger function · 4 seed rows | Enterprise identity (SSO, SCIM), custom roles and SoD, API keys, webhooks, audit sink, export, tenant keys, sandbox, promotion, connectors, security findings, status incidents, tax, invoices, locales | SQL | 227 |
| 4 | `FSD/29_Analytics_Attribution_KPI_Engineering.txt` | 9,908 B | 4 tables · 21 prose lines | REC-15; PERF-01…07; 8 release KPIs (KPI-05, 06, 26–31); event attribution; MT-13/27/31; instrumentation rule; AT-14, CV-14, CS-12; metric contract; 14 management views | Requirement tables + prose | 56 |
| 5 | `FSD/31_Cybersecurity_Privacy_Threat_Management.txt` | 9,077 B | 2 tables · 40 prose lines | ENT-SEC-01…08; PEN-01…08; CERT-In/GDPR/DPDP obligations; MOB-10; SEC release rule; SEC-06, 08…14; 10 threats and 9 control families | Requirement tables + prose | 78 |
| 6 | `src/engineering/engineering/closure/database_confirmation_plan.csv` | 2,179 B | 4 rows | Database confirmation items "DEC-039…042" (identity reuse, embedding dimension) | CSV | 4 |
| 7 | `src/engineering/engineering/database_constraint_proposals.csv` | 4,248 B | 35 rows | Candidate CHECK/FK/UNIQUE proposals for `sales_*` and `growth_*` tables | CSV | 35 |
| 8 | `src/engineering/engineering/database_contract_review.csv` | 55,548 B | 149 rows | Exposure, fields, constraints, dependencies per historical entity | CSV | 149 |
| 9 | `src/engineering/engineering/database_field_resolution_proposals.csv` and `starter/database_field_review.csv` | 55,854 B + 33,189 B | 136 + 136 rows | Field type proposals (identical keys in both files) | CSV | 272 |
| 10 | `src/engineering/engineering/ui_upgrade/candidate_database_register.csv` | 2,770 B | 6 rows | `sales_ui_*` candidate entities | CSV | 6 |
| 11 | `src/engineering/engineering/starter/reference_schema.sql`, `reference_schema_smoke.sql` | 2,829 B + 2,094 B | 5 tables, 1 function, 1 index, 4 smoke assertions | Sandbox reference schema for budget reservation, idempotent outbox and receipt de-duplication | SQL | 12 |
| 12 | `src/engineering/engineering/starter/catalog_schema_review.sql`, `catalog_schema_review_enhanced.sql` | 43,304 B + 39,466 B | 146 tables each (identical table set, verified) | Disposable review DDL for the historical entities | SQL | 146 |
| 13 | `src/engineering/engineering/database_catalog.json`, `ui_upgrade/current_database_inventory.json` | 401,113 B + 413,034 B | 149 and 149 + 6 entries | Machine copies of the same entity catalogue | JSON | 2 |
| | **Total** | | | | | **3,248** |

### 11.9.1.2 Method (programmatic, reproducible)

1. **Parse.** `assembly/v12/i_ddl/parse_tables.py` reads the V12 text format (`<HeadingN>`, `[TABLE]`, `---row`, one cell per line) and returns every table row and prose line with its heading path. All 47 tables of chapter 26, 4 of chapter 29 and 2 of chapter 31 were parsed; no row was skipped.
2. **Execute the customer DDL.** Appendix C (with the `CREATE EXTENSION vector` line skipped, exactly as the customer did) and Appendix C2 were applied to a scratch **PostgreSQL 16.15** cluster. Result: **137 tables, 1,326 columns, 310 constraints (137 PK, 118 FK, 49 CHECK, 6 UNIQUE), 120 RLS policies, 143 indexes, 1 trigger, 1 trigger function, 4 seed rows** — matching the V12 claim "137 tables, 120 policies".
3. **Reproduce the customer tests.** DB-T1…T9 and C2-T1…T11 were re-run as a non-owner role: **20 of 20 reproduce** (`i_ddl/v12_tests.out`).
4. **Analyse the catalogue.** `i_ddl/analyze_catalog.sql` queried `pg_catalog` for RLS coverage, policy predicates, nullable scope keys, FK index support, non-composite cross-table keys, missing enumerations, roles and grants (`i_ddl/analyze_catalog.out`). Findings are in §11.9.3.3.
5. **Reconcile.** Every table, column, constraint and policy was compared with the blueprint catalogue: Part 3.3 (199 entities), Part 3.6a/b (155 source tables, `final/coverage/E_table_mapping.csv`, 1,641 doc-08 aspects in `final/coverage/E_coverage.csv`), Part 9.9 (developer platform, BYOK) and Part 11.5a (DEC-581).
6. **Enhance and prove.** The gaps were closed in **DDL-V12-I ("Appendix C3")**, generated and applied on top of C + C2, then verified by **50 passing assertions (TC-V12-I-001…031)** and a regression run of all 20 customer tests on the hardened schema (TC-V12-I-032). See Part 11.9b.

### 11.9.1.3 Sizes after enhancement (C + C2 + C3, same PostgreSQL 16.15 run)

| Object | Appendix C + C2 (customer) | After DDL-V12-I (C3) | Change |
|---|---|---|---|
| Tables | 137 | **155** | +18 (6 V6 entities, 7 analytics/usage tables, `user_role_assignment`, `tenant_data_key`, `domain_schema_registry`, `domain_record_version`, `usage_reservation`) |
| Columns | 1,326 | **1,579** | +253 |
| Constraints | 310 | **536** | +226 (CHECK vocabularies, composite tenant-pinned FKs, uniqueness) |
| RLS-enabled and forced tables | 120 | **139** | +19 (every table carrying `tenant_id`) |
| RLS policies | 120 (all `FOR ALL`, tenant only) | **410** (140 SELECT, 138 INSERT, 131 UPDATE, 1 platform `ALL`) | Command-split, tenant **and company** |
| Indexes | 143 (PK/UNIQUE only, 0 secondary) | **516** | +373 (110 FK-support, 178 domain scope/registry, 8 evidence GIN, 22 query-specific, plus new-table keys) |
| Triggers | 1 | **105** | Domain validation (89), immutability, SoD, residency, breach clocks, crypto-shred, effect transitions |
| Database roles | 0 | 8 (`ge_owner`, `ge_app`, `ge_worker`, `ge_readonly`, `ge_retention`, `ge_audit_writer`, `ge_platform_sec`; Supabase `anon`/`authenticated` revoked) | Non-owner, no `BYPASSRLS` |

---

## 11.9.2 Coverage summary

Status before is the blueprint position (Parts 0–9.10, 11.5a) before this batch; status after is the position once Parts 11.9a/b/c are applied. "Covered" items were checked, not assumed: columns were matched by name against the Part 3.3/3.6b/9.9/4.1 dictionaries and historical entities through the 155-row mapping of Part 3.6a.

{{summary}}

**Reading the totals.** 1,809 aspects (55.7%) were already covered; 902 (27.8%) were partially covered, mostly because the V12 DDL introduces generic domain columns (`schema_ref`, `payload`, `evidence_refs`), tenant-only policies and new enterprise tables; 521 (16.0%) were not covered (C2 enterprise tables, V6 hierarchy tables, analysis gaps); 16 (0.5%) were conflicts. After this batch **3,245 aspects (99.9%) are Matched** and **3 are Pending Founder decision**: ENT-DAT-03 and the `tenant.data_region IN ('IN','EU')` constraint (EU residency, CONFLICT-832 already raised in Part 11.5a) and ENT-SEC-08 (24×7 security monitoring, CONFLICT-905).

---

## 11.9.3 Detailed register

### 11.9.3.1 Requirement, test, entity, analytics, security and engineering aspects (every non-covered aspect individually)

Covered aspects are grouped in §11.9.2 and listed row by row in the CSV. Domain-schema fields, DDL columns, constraints and policies are listed individually in §11.9.3.2 and §11.9.3.4.

{{register_req}}

### 11.9.3.2 Appendix C / C2 table-by-table register (every non-covered column, strengthened constraint and replaced policy named)

The blueprint target is the physical table after the DEC-581 vocabulary mapping (V12 *company* = blueprint *startup*; `company_id` is the V12-facing alias of physical `startup_id`). For the 89 generic domain tables the three V12 common columns `schema_ref`, `payload`, `evidence_refs` were not covered; `status` and `version` map to blueprint `state` and `revision`/`version_no` (partially covered, °). Every policy listed was replaced by the command-split policies of DDL-V12-I §C3-13 (Part 11.9b §11.9.5.6).

{{register_ddl}}

### 11.9.3.3 Catalogue analysis findings on the customer DDL (executed, not inferred)

| Finding | Evidence (query in `analyze_catalog.sql`) | Risk | Fix (DDL-V12-I) | Tag / decision |
|---|---|---|---|---|
| F1 RLS policies check `tenant_id` only. `app.company_ids` is set by the application (Appendix C header) but **no policy uses it**: any user of tenant A reads every company of tenant A | A3: 100 company-scoped tables, 0 policies referencing `company` | Cross-company leakage inside a tenant (Owner Portfolio: 25+ startups; DEC-065; MT-09 "cross-company edit denied") | Command-split policies with `company_id = ANY(app_company_ids())` for reads and `company_id = app_write_company()` for writes (C3-13); TC-V12-I-001/002 | GAP-912, DEC-662, ADR-210 |
| F2 All 120 policies are `FOR ALL` | A4 | Portfolio (multi-company) sessions can write; DELETE allowed wherever the role has the grant | Separate SELECT/INSERT/UPDATE policies; no DELETE policy on business tables; TC-V12-I-002b, 026 | GAP-912 |
| F3 Four tables carry `tenant_id` without RLS: `tenant`, `inbox`, `incident`, `portfolio_grant`; four have nullable `tenant_id` (`outbox`, `inbox`, `incident`, `portfolio_grant`) | A1, A5 | Cross-tenant read of inbound provider events, incidents (with `personal_data` flags) and portfolio grants | RLS + FORCE + policies; NOT NULL scope keys; TC-V12-I-008/009/027 | GAP-913 |
| F4 Zero secondary indexes; 110 foreign keys without a supporting index | A6, A9 | RLS predicates and joins scan whole tables; FK checks lock-escalate on parent deletes; misses KPI-05/26 p95 targets | 110 FK-support indexes, V5 common `(tenant_id, company_id, status, updated_at)` index on 89 domain tables, 22 query-specific partial/BRIN/GIN indexes; CI guard TC-V12-I-028 | GAP-914, DEC-677 |
| F5 Three tenant-scoped children reference tenant-scoped parents by a single column (`role_permission.role_id`, `webhook_delivery.endpoint_id`, `config_promotion.sandbox_id`); `role_permission` PK `(role_id, permission)` lacks `tenant_id` | A7 | Tenant B can attach rows to tenant A's parent; FK and PK errors become an existence oracle across tenants | Composite `(tenant_id, …)` keys and PK `(tenant_id, role_id, permission)`; TC-V12-I-004 | GAP-915 |
| F6 No roles, grants or REVOKE statements | A12 | On Supabase, tables in `public` are reachable through the Data API roles `anon`/`authenticated` unless revoked; the `service_role` key bypasses RLS | Roles and grants (C3-01), Data API closed, `ge_app` NOBYPASSRLS through Supavisor; TC-V12-I-025 | CONFLICT-906, DEC-663, ADR-212 |
| F7 Audit, consent and usage tables are mutable; the SoD trigger fires on INSERT only and checks one role at a time | A13 | Tamper with audit trail (SEC-06); SoD bypass by UPDATE or by holding two roles | Append-only triggers, hash-chained `fn_append_audit()`, SoD on INSERT/UPDATE and per user; TC-V12-I-005/006/007 | GAP-915, DEC-668, DEC-669 |
| F8 109 status/state/type columns have no allowed-value CHECK (20 core, 89 domain) | A8 | Free-text states break state machines and KPI filters | CHECK vocabularies for core tables (C3-04); `domain_schema_registry.allowed_statuses` enforced by trigger for domain tables (C3-10); TC-V12-I-016 | GAP-915, DEC-661 |
| F9 `growth_embedding` has no vector column although `vector` is enabled | Appendix C text | Retrieval (SVC-25) cannot be built from the DDL | `embedding halfvec(1024)` + HNSW per Part 3.3 §3.3.8.4, gated by the embedding-model decision (V12-ENG DEC-042) | GAP-916 |
| F10 Mixed money representations: `offering.price_amount numeric(18,4)`, `invoice.*_minor bigint`; blueprint `numeric(18,2)` | A10 | Rounding drift between ledgers and invoices | Amounts in integer minor units + currency; unit prices, quantities, rates in exact numeric | CONFLICT-908, DEC-664 |
| F11 Workflow-ID format: comments cite `SM-SVC-01-WF01` while chapters 11–13 use `SM-SVC-01-WF1`; 49 comment lists are cut at 10 IDs with a trailing comma | Appendix C comments | Traceability tooling mismatch | CHECK accepts both (`WF0?[1-4]`); canonical form `SM-SVC-##-WF#` per V12 brief; the full table→workflow map is the DTO registry (Part 11.4) | DEC-661 |

### 11.9.3.4 Domain-schema fields (chapter 26 V5, 39 services, 324 fields)

{{register_ds}}

All 324 fields end **Matched**: each is a required or optional key of the service's Appendix B JSON Schema, registered in `domain_schema_registry` (schema reference, version, allowed statuses, required keys, data class, retention class) and enforced at write time by `fn_validate_domain_row()` (Part 11.9b §11.9.5.5). A field becomes a typed column only when a list, filter, index or RLS predicate needs it (ADR-211).

---

## 11.9.4 Catalogue reconciliation

### 11.9.4.1 Entity-count reconciliation (199 entities, 155 source tables, 137 + 18 V12 tables)

| Line | Item | Count | Basis |
|---|---|---|---|
| a | Blueprint logical entities (Part 3.3) | 199 | §3.3.3.2 |
| b | Blueprint entities added by Part 3.6 (ENT-ENH-E-01…04) | 4 | Part 3.6a line j |
| c | Historical source tables (V12 ch26 "149 historical entities" = document 08 tables 001–149) | 149 | All 149 names equal `E_table_mapping.csv` rows 001–149 (verified) |
| d | V12 `sales_ui_*` candidates (`candidate_database_register.csv`) | 6 | = Part 3.6a rows 150–155 |
| e | V12 Appendix C domain tables (generic shape) | 89 | All 89 are historical names (subset of c); 60 historical entities are not in Appendix C because no V12 workflow persists them directly (they stay as typed blueprint tables) |
| f | V12 Appendix C core tables | 29 | Mapped in §11.9.4.2 |
| g | V12 Appendix C2 enterprise tables | 19 | Mapped in §11.9.4.2 |
| h | Check: e + f + g | 137 | = customer total |
| i | V12 core/enterprise tables already in the blueprint (same entity, partial columns) | 26 | §11.9.4.2 "Partially covered" |
| j | V12 core/enterprise tables new to the blueprint | 22 | §11.9.4.2 "new" |
| k | V6 / V5 / V4 entities with no Appendix C table, created in DDL-V12-I | 13 | `company_operating_country`, `offering_market`, `channel_account_market`, `configuration_revision`, `workflow_configuration`, `business_event`, `metric_definition`, `metric_aggregate`, `experiment`, `feedback_case`, `sli_sample`, `customer_value`, `journey_event` |
| l | Supporting tables created in DDL-V12-I | 5 | `user_role_assignment`, `tenant_data_key`, `domain_schema_registry`, `domain_record_version`, `usage_reservation` |
| m | **Blueprint logical entities after this batch** | **243** | 203 (a + b) + 22 (j) + 13 (k) + 5 (l). Final ENT numbers ENT-204…246 to be assigned by the coordinator; until then the V12 table name is the identifier |

### 11.9.4.2 Core and enterprise tables (48) → blueprint physical model

Naming rule (DEC-660): the V12 table name is the canonical **logical** name and is used in V12 tests and contracts; the **physical** table keeps the blueprint prefix convention of Part 3.3 §3.3.5.8. Scope class and immutability profile follow Part 3.3 (S startup/company-scoped, T tenant-scoped, X platform-or-tenant, P platform; M mutable, V versioned-frozen, A append-only, F frozen-after-state).

| V12 table (source) | Physical table | ENT / origin | Scope | Imm. | Before | Columns added to the blueprint table (V12 names) | Key V12 rules adopted |
|---|---|---|---|---|---|---|---|
| `tenant` (C) | `ten_tenant` | ENT-001 | P (root) | M | Partial | `customer_type`, `data_region`, `contract_status` | Region fixed at onboarding (CJ-R09); residency guard trigger |
| `organization` (C) | `ten_organization` | New (DEC-581) | T | M | Not covered | all | Unique normalized name per tenant |
| `company` (C) | `ten_startup` (alias company) | ENT-002 | T | M | Partial | `organization_id`, `registration_country` | Composite FK to organization |
| `division` (C) | `ten_business_line` (alias division) | ENT-003 | S | M | Partial | `division_id` alias, `name_norm` | Unique name per company (C3-11) |
| `brand` (C) | `ten_brand` | New | S | M (history retained: `valid_from`/`valid_to`) | Not covered | all | Company-pinned FK to division |
| `offering` (C) | `cat_offering` | ENT-016 | S | M (+V versions) | Partial | `brand_id`, `offering_type`, `claims_ref`, `price_amount`, `currency` | Type and status vocabularies; brand in same company |
| `market` (C) | `ten_market` | New | S | M | Not covered | all | IANA zone, ISO country/currency, jurisdiction pack |
| `channel_account` (C) | `eng_channel_account` | ENT-089 | S | M | Partial | `sender_alias`, `credential_ref`, `dlt_entity_id`, `dlt_header`, `number_series`, `daily_cap` | Secret reference only (`vault://`, `sm://`, `kms://`) |
| `workflow_run` (C) | `aut_run` | ENT-162 | S | M (state machine) | Partial | `sku_id`, `wf_id`, `wf_version`, `business_context`, `input`, `reviewed_by`, `reserved_units` | Reviewer ≠ requester (D10); idempotency unique; WF belongs to SKU |
| `workflow_step_run` (C) | `aut_step_run` | ENT-163 | S | M | Partial | `step_class`, `model_id`, `prompt_version`, `reason_code`, `company_id` | Model only on `ai_inference` (AIX-01) and then model + prompt mandatory |
| `effect` (C) | `aut_effect` | New (DB-V2-EFFECT) | S | F (forward-only) | Not covered | all + `company_id` | Preflight must be ALLOW; forward transitions only |
| `outbox` (C) | `ops_outbox` | ENT-169 | S | F | Covered | `company_id`, `dedup_key`, `correlation_id`, `attempts`, `next_attempt_at` | Dedup unique; partial pending index |
| `inbox` (C) | `int_provider_event_key` | ENT-043 | T | A | Covered | `provider_account`, `signature_ok`, `payload_ref`, `processed_at` | Key = provider + provider account + event; unsigned rows rejected |
| `audit_event` (C) | `ops_audit_event` | ENT-172 | X | A | Covered | `company_id`, `correlation_id`, `object_type`, `payload_redacted`, `schema_version`, `prev_hash`, `row_hash` | Insert only via `fn_append_audit()`; hash chain (SEC-06) |
| `portfolio_grant` (C) | `ten_portfolio_grant` (generalizes `ten_membership_grant`) | ENT-008 association | T | M | Partial | all | No wildcard; expiry mandatory; revocation |
| `fx_rate` (C) | `ana_fx_snapshot` | ENT-198 | P | V | Partial | `source`, `approved_version` | Positive rate; base ≠ quote; unique version |
| `jurisdiction_pack` (C) | `gov_jurisdiction_pack` | New | P | V | Not covered | all | Approved pack needs approver, date, effective window |
| `jurisdiction_rule` (C) | `gov_jurisdiction_rule` | ENT-030 | P | V | Partial | `pack_id`, `effect`, `legal_source`, `interpretation_status` | Effect ALLOW/HOLD/REVIEW/INFO |
| `consent_record` (C) | `gov_consent` | ENT-027 | S | A | Covered | `basis`, `notice_version`, `capture_source`, `evidence_hash`, `supersedes` | Append-only; contact FK; SHA-256 evidence |
| `suppression` (C) | `gov_suppression` | ENT-028 | T | A | Covered | `reason` vocabulary | Kept after erasure (no contact FK by design) |
| `dsar_request` (C) | `gov_privacy_request` | ENT-036 | T | M | Covered | `jurisdiction`, `legal_hold`, `evidence_ref` | Identity verified and evidence before Completed |
| `incident` (C) | `gov_compliance_incident` | ENT-039 | T / platform | M | Partial | `aware_at`, `personal_data` | Awareness clock drives notifications |
| `incident_notification` (C) | `gov_incident_notification` | New | P | A (no delete) | Not covered | all | CERT-In ≤ 6 h; GDPR ≤ 72 h; DPDP Board ≤ 72 h (verify) |
| `ai_model` (C) | `ai_model` | New (registry, was configuration in Part 7) | P | V | Not covered | all | Tier vocabulary; Tier 2 only Public/Internal-non-personal |
| `prompt_version` (C) | `ai_prompt_version` | ENT-045 | X | V | Covered | `template_hash`, `output_schema_ref` | Status vocabulary; SHA-256 hash |
| `eval_suite` (C) | `ai_eval_suite` | New | P | V | Not covered | all | Positive case count; thresholds JSON |
| `eval_run` (C) | `ai_eval_run` | ENT-048 | P | A | Covered | `denominator`, `metrics` | Append-only |
| `ai_usage_event` (C) | `ai_usage` | ENT-050 | S | A | Covered | `cached_tokens`, `latency_ms`, `outcome` | Outcome vocabulary; non-negative counters |
| `ai_budget` (C) | `ai_budget` | ENT-052 | T | M | Partial | `soft_cap_tokens`, `hard_cap_tokens` (in addition to INR caps, DEC-008) | soft ≤ hard; period `YYYY-MM` |
| `identity_provider` (C2) | `sec_identity_provider` | New (Part 11.5a FR-V12-E-010…015) | T | M | Not covered | all | Enforcement needs verified domain + break-glass (C2-T4) |
| `scim_token` (C2) | `sec_scim_token` | New | T | M | Not covered | all + `expires_at` | Hash only; unique hash; ≤ 397 days |
| `custom_role` (C2) | `ten_role` (tenant rows) | ENT-007 | X | M | Partial | `name` per tenant | Unique (tenant, role) |
| `role_permission` (C2) | `ten_role_permission` | New | T | M | Not covered | all | `Resource:action` format; SoD trigger |
| `sod_conflict` (C2) | `ref_sod_conflict` | New | P | M | Not covered | all | Seeds + RECOMMENDATION-920 pairs |
| `api_key` (C2) | `saas_api_credential` | Part 9.9 CAP-X3-23 | T | M | Partial | `prefix`, `last4`, `key_hash`, `scopes`, `ip_allowlist` | Hash only (C2-T9); unique prefix and hash; ≤ 397 days |
| `webhook_endpoint` (C2) | `saas_webhook_subscription` | Part 9.9 | T | M | Partial | `events`, `secret_ref`, `verified_at` | HTTPS only; active requires verification |
| `webhook_delivery` (C2) | `saas_webhook_delivery` | Part 9.9 | T | A (no delete) | Partial | `attempt` 1–6, `signed_at`, `event_id` | Unique (endpoint, event, attempt) |
| `audit_sink` (C2) | `ops_audit_sink` | New | T | M | Not covered | all | https / syslog-tls / object storage; JSON or CEF; 1/3/7 years |
| `export_job` (C2) | `saas_export_job` | ENT-189 | T | F | Partial | `format`, `approved_by`, `manifest_hash`, `expires_at`, `approved_at` | Requester ≠ approver (C2-T2); link ≤ 7 days |
| `tenant_key_config` (C2) | `ten_tenant_key` | Part 9.9 CAP-X3-15 | T | M | Partial | `mode`, `rotation_days`, `provider`, `key_state`, `revoked_at` | 90/180/365-day rotation; revocation crypto-shreds |
| `sandbox_environment` (C2) | `saas_sandbox_environment` | New | T | M | Not covered | all | No personal data (C2-T5) |
| `config_promotion` (C2) | `aut_config_promotion` | New | T | F | Not covered | all | Requester ≠ approver (C2-T3) |
| `connector_installation` (C2) | `int_integration` | ENT-040 | T | M | Partial | `environment`, `legal_review_ref`, `security_review_ref` | Production needs both reviews (C2-T6) |
| `security_finding` (C2) | `sec_security_finding` | New | P | M | Not covered | all | Due date by severity 7/30/90/180 days (C2-T7) |
| `ops_incident` (C2) | `ops_incident` | ENT-176 | P | M | Covered | `status_message` | SEV1–SEV4; status vocabulary |
| `tax_rule` (C2) | `cat_tax_profile` | ENT-022 | P | V | Partial | `needs_rate_input`, `approved_by`, `approved_at` | Rate 0–30% |
| `invoice` (C2) | `saas_service_invoice` | ENT-184 | T | F | Partial | `net_minor`, `tax_minor`, `total_minor`, `tax_rule_id` | Total = net + tax (C2-T8) |
| `locale_bundle` (C2) | `ref_locale_bundle` | New | P | M | Not covered | all | LTR/RTL; coverage 0–100% |

### 11.9.4.3 V5 and V4 candidate entities → blueprint

| V12 entity | Blueprint / DDL-V12-I target | Note |
|---|---|---|
| `opt_usage_event` | ENT-050 `ai_usage` + ENT-183 `saas_usage_meter_reading` | Append-only; reconciled to ledger (NFR-014) |
| `opt_model_evaluation` | ENT-048 `ai_eval_run` + `ai_eval_suite` | Promotion gate |
| `opt_scoped_cache` | `ai_semantic_cache` (Part 7) | Key = scope + purpose + input hash + model + prompt + policy + evidence version; revocation invalidates |
| `opt_step_checkpoint` | ENT-163 `aut_step_run` (unique run/step/attempt; lease columns) | Conditional transitions |
| `opt_control_event` | ENT-172 `ops_audit_event`, ENT-032 `gov_policy_decision` | Redacted payload |
| `opt_sli_sample` | **`sli_sample`** (new) | Missing data explicit (`status = missing_data`) |
| `opt_customer_value` | **`customer_value`** (new) | Labelled "Estimate – not a guarantee" |
| `opt_feedback_case` | **`feedback_case`** (new) + `crm_survey_response` | Missing response never counted as satisfied |
| `opt_journey_event` | **`journey_event`** (new) + ENT-124 | Operator and subscriber events separated |
| DB-V2-RUN / STEP / EVIDENCE / APPROVAL / INBOX-OUTBOX / SUBSCRIPTION / CONFIG | ENT-162 / 163 / 059 / 034 / 043+169 / 182 / 168 | Covered |
| DB-V2-ARTIFACT | Generic domain shape + `domain_schema_registry` | ADR-211 |
| DB-V2-EFFECT | `effect` → `aut_effect` | Forward-only |
| DB-V2-USAGE, V4 `usage_reservation` | **`usage_reservation`** (new) + `ai_cost_ledger` | Unique run/period; idempotency key |
| V4 `application` | ENT-187 `saas_application_draft` | Covered |
| V4 `domain_record_version` | **`domain_record_version`** (new) | Immutable snapshots |
| V4 `approval_decision` | ENT-034 `gov_approval` | No self-approval |
| V4 `workflow_step_event` | ENT-163 + ENT-170 `ops_domain_event` | Ordered sequence |

### 11.9.4.4 The 89 generic domain tables → blueprint typed tables

The physical implementation keeps the typed blueprint table and **adds** the three V12 common columns (`schema_ref text NOT NULL`, `evidence_refs uuid[] NOT NULL DEFAULT '{}'`, `payload jsonb NOT NULL DEFAULT '{}'`) plus the registry trigger (DEC-661). `status`/`version` map to `state`/`revision`.

{{map_domain}}

### 11.9.4.5 Engineering-file reconciliation

| File | Rows | Result |
|---|---|---|
| `database_contract_review.csv` | 149 | Same 149 entities as chapter 26; exposure classes equal Part 3.6a §3.6.4.9; status "Not started" for all rows becomes the Sprint 0 migration-approval task (MT-36) |
| `database_field_resolution_proposals.csv` / `starter/database_field_review.csv` | 136 / 136 | Identical keys; each row linked to its `08-SDR` aspect in Part 3.6 (schema decision register). The one `numeric(18,2)` proposal follows DEC-664 (minor units) |
| `database_constraint_proposals.csv` | 35 | All covered by Part 3.3 composite `(tenant_id, startup_id)` FKs and Part 3.6a §3.6.4.7 checks |
| `candidate_database_register.csv` | 6 | = Part 3.6a rows 150–155 |
| `closure/database_confirmation_plan.csv` | 4 | IDs "DEC-039…042" collide with blueprint DEC-039…042 (migration, hosting, monitoring, model names). Namespaced as **V12-ENG DEC-039…042** (DEC-665). Content: reuse the existing Django identity tables (Part 3.6a rows 001–003) and choose the embedding model/dimension before the vector index (GAP-916) |
| `starter/reference_schema.sql` + smoke | 12 objects | Equivalent blueprint objects exist (ai_budget reservation, outbox idempotency, payment de-duplication); smoke assertions adopted as TC-V12-I-033 |
| `starter/catalog_schema_review*.sql` | 146 + 146 | Same table set in both files; superseded by Part 3.3/3.6 typed DDL plus DDL-V12-I |
| `database_catalog.json`, `current_database_inventory.json` | 149; 149 + 6 | Counts verified |

---

### Quality gate: Batch 11.9a

| # | Item | Result | Notes |
|---|---|---|---|
| 1 | Every requirement traced to a source | Pass | Every register row cites the V12 file, chapter, section and aspect ID; blueprint locations cite part/section/ENT |
| 2 | Assumptions, gaps, conflicts tagged and logged | Pass | Tags 904…921 in Part 11.9c §11.9.9 |
| 3 | IDs unique and consistent | Pass | 3,248 unique aspect IDs (script check: 0 duplicates); V12 KPI/DEC collisions namespaced (DEC-665) |
| 4 | No story lacks AC; no requirement lacks a test | Pass | Stories and tests in Part 11.9b/c |
| 5 | Negative, edge, security, accessibility cases | Pass | 50 negative/positive DB assertions; accessibility N/A for DDL (KPI-23 handled by Group G) |
| 6 | Agents have guardrail, fallback, KPI, cost | N/A | No agent added |
| 7 | Time-sensitive facts flagged | Pass | Supabase features and DPDP Rules timings flagged "verify (as of 27 Nov 2026)" in 11.9b/c |
| 8 | No restricted data to free tiers | Pass | `ai_model_t2_data_ck` enforces it in the database |
| 9 | Consistent with earlier parts | Pass | DEC-581 vocabulary kept (physical `startup_id`); inconsistencies reported in 11.9c §11.9.8.2 |

**Status: Part 11 Batch 11.9a complete. 3,248 V12 data, security and analytics aspects inventoried programmatically; before 1,809 covered / 902 partial / 521 not covered / 16 conflict; after 3,245 Matched and 3 Pending Founder decision. Continue with Part 11.9b.**
