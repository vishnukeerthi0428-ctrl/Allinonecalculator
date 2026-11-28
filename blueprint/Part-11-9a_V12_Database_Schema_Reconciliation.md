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

| Aspect group | Aspects | Covered | Partially covered | Not covered | Conflict | After: Matched | After: Pending Founder |
|---|---|---|---|---|---|---|---|
| ch26 · V12 Data control | 5 | 0 | 3 | 1 | 1 | 4 | 1 |
| ch26 · V12 C2 tests | 11 | 0 | 0 | 11 | 0 | 11 | 0 |
| ch26 · V8 DB tests | 9 | 6 | 2 | 0 | 1 | 9 | 0 |
| ch26 · V12 \| Data control and enterprise schema | 1 | 0 | 1 | 0 | 0 | 1 | 0 |
| ch26 · V8 \| Schema additions and verification | 1 | 0 | 1 | 0 | 0 | 1 | 0 |
| ch26 · V6 \| Universal architecture and controlled requirements | 1 | 0 | 1 | 0 | 0 | 1 | 0 |
| ch26 · MT-09 — Business division master | 3 | 0 | 3 | 0 | 0 | 3 | 0 |
| ch26 · MT-10 — Brand management | 3 | 0 | 3 | 0 | 0 | 3 | 0 |
| ch26 · MT-11 — Unified subscriber offering master | 3 | 0 | 3 | 0 | 0 | 3 | 0 |
| ch26 · MT-18 — Multiple countries per offering | 3 | 0 | 3 | 0 | 0 | 3 | 0 |
| ch26 · MT-33 — Canonical master data | 3 | 0 | 3 | 0 | 0 | 3 | 0 |
| ch26 · V5 optimization requirements and controls | 10 | 0 | 10 | 0 | 0 | 10 | 0 |
| ch26 · Proposed V4 persistence additions | 6 | 3 | 3 | 0 | 0 | 6 | 0 |
| ch26 · V6 entity graph | 16 | 3 | 6 | 7 | 0 | 16 | 0 |
| ch26 · V6 controlled requirements | 5 | 0 | 5 | 0 | 0 | 5 | 0 |
| ch26 · V5 candidate entities | 9 | 4 | 3 | 2 | 0 | 9 | 0 |
| ch26 · V5 proposed entities | 10 | 7 | 3 | 0 | 0 | 10 | 0 |
| ch26 · Domain schemas (39 services) | 324 | 55 | 269 | 0 | 0 | 324 | 0 |
| ch26 · Historical entity (149) | 149 | 149 | 0 | 0 | 0 | 149 | 0 |
| Appendix C · Table | 118 | 0 | 110 | 8 | 0 | 118 | 0 |
| Appendix C2 · Table | 19 | 0 | 10 | 9 | 0 | 19 | 0 |
| Appendix C · Column | 1206 | 639 | 178 | 389 | 0 | 1206 | 0 |
| Appendix C2 · Column | 120 | 36 | 0 | 84 | 0 | 120 | 0 |
| Appendix C · Constraint | 241 | 220 | 21 | 0 | 0 | 240 | 1 |
| Appendix C2 · Constraint | 69 | 30 | 39 | 0 | 0 | 69 | 0 |
| Appendix C · RLS policy | 106 | 0 | 106 | 0 | 0 | 106 | 0 |
| Appendix C2 · RLS policy | 14 | 0 | 14 | 0 | 0 | 14 | 0 |
| Appendix C · RLS gap | 4 | 0 | 0 | 4 | 0 | 4 | 0 |
| Appendix C2 · Trigger | 1 | 0 | 1 | 0 | 0 | 1 | 0 |
| Appendix C2 · Seed | 4 | 4 | 0 | 0 | 0 | 4 | 0 |
| Appendix C · Extension | 2 | 2 | 0 | 0 | 0 | 2 | 0 |
| Appendix C · Convention | 6 | 3 | 3 | 0 | 0 | 6 | 0 |
| Appendix C/C2 · Analysis finding | 6 | 0 | 0 | 6 | 0 | 6 | 0 |
| ch29 · V10 reconciliation | 1 | 0 | 1 | 0 | 0 | 1 | 0 |
| ch29 · V9 load profiles | 7 | 0 | 7 | 0 | 0 | 7 | 0 |
| ch29 · V9 release KPIs | 8 | 0 | 0 | 0 | 8 | 8 | 0 |
| ch29 · V9 \| Capacity, load and front-end performance profiles | 1 | 0 | 1 | 0 | 0 | 1 | 0 |
| ch29 · V6 \| Universal architecture and controlled requirements | 1 | 0 | 1 | 0 | 0 | 1 | 0 |
| ch29 · MT-13 — Offering-specific audiences | 3 | 0 | 3 | 0 | 0 | 3 | 0 |
| ch29 · MT-27 — Business event attribution | 3 | 0 | 3 | 0 | 0 | 3 | 0 |
| ch29 · MT-31 — Tenant and offering-level performance | 3 | 0 | 3 | 0 | 0 | 3 | 0 |
| ch29 · V5 optimization requirements and controls | 14 | 0 | 14 | 0 | 0 | 14 | 0 |
| ch29 · Fourteen distinct management views — V4 KPI mapping | 1 | 0 | 1 | 0 | 0 | 1 | 0 |
| ch29 · Fourteen management views | 14 | 0 | 14 | 0 | 0 | 14 | 0 |
| ch31 · V12 security programme | 8 | 3 | 3 | 0 | 2 | 7 | 1 |
| ch31 · V9 penetration-test plan | 8 | 0 | 8 | 0 | 0 | 8 | 0 |
| ch31 · V9 \| Penetration-test plan | 1 | 0 | 1 | 0 | 0 | 1 | 0 |
| ch31 · V8 \| Regulatory security obligations | 3 | 3 | 0 | 0 | 0 | 3 | 0 |
| ch31 · MOB-10  PWA and offline boundary | 5 | 0 | 5 | 0 | 0 | 5 | 0 |
| ch31 · V5 optimization requirements and controls | 33 | 0 | 33 | 0 | 0 | 33 | 0 |
| ch31 · V5 threats | 10 | 10 | 0 | 0 | 0 | 10 | 0 |
| ch31 · V5 controls | 9 | 9 | 0 | 0 | 0 | 9 | 0 |
| ch31 · V5 testing note | 1 | 1 | 0 | 0 | 0 | 1 | 0 |
| src/engineering · database_confirmation_plan.csv | 4 | 0 | 0 | 0 | 4 | 4 | 0 |
| src/engineering · database_constraint_proposals.csv | 35 | 35 | 0 | 0 | 0 | 35 | 0 |
| src/engineering · candidate_database_register.csv | 6 | 6 | 0 | 0 | 0 | 6 | 0 |
| src/engineering · database_contract_review.csv | 149 | 149 | 0 | 0 | 0 | 149 | 0 |
| src/engineering · database_field_resolution_proposals.csv | 136 | 136 | 0 | 0 | 0 | 136 | 0 |
| src/engineering · database_field_review.csv | 136 | 136 | 0 | 0 | 0 | 136 | 0 |
| src/engineering · reference_schema.sql / reference_schema_smoke.sql | 12 | 12 | 0 | 0 | 0 | 12 | 0 |
| src/engineering · catalog_schema_review(_enhanced).sql | 146 | 146 | 0 | 0 | 0 | 146 | 0 |
| src/engineering · database_catalog.json | 1 | 1 | 0 | 0 | 0 | 1 | 0 |
| src/engineering · ui_upgrade/current_database_inventory.json | 1 | 1 | 0 | 0 | 0 | 1 | 0 |
| **Total** | **3248** | **1809** | **902** | **521** | **16** | **3245** | **3** |

**Reading the totals.** 1,809 aspects (55.7%) were already covered; 902 (27.8%) were partially covered, mostly because the V12 DDL introduces generic domain columns (`schema_ref`, `payload`, `evidence_refs`), tenant-only policies and new enterprise tables; 521 (16.0%) were not covered (C2 enterprise tables, V6 hierarchy tables, analysis gaps); 16 (0.5%) were conflicts. After this batch **3,245 aspects (99.9%) are Matched** and **3 are Pending Founder decision**: ENT-DAT-03 and the `tenant.data_region IN ('IN','EU')` constraint (EU residency, CONFLICT-832 already raised in Part 11.5a) and ENT-SEC-08 (24×7 security monitoring, CONFLICT-905).

---

## 11.9.3 Detailed register

### 11.9.3.1 Requirement, test, entity, analytics, security and engineering aspects (every non-covered aspect individually)

Covered aspects are grouped in §11.9.2 and listed row by row in the CSV. Domain-schema fields, DDL columns, constraints and policies are listed individually in §11.9.3.2 and §11.9.3.4.

| Aspect | Summary (V12) | Before | Blueprint location | Enhancement | New IDs | After |
|---|---|---|---|---|---|---|
| ENT-DAT-01 | ENT-DAT-01 P0 Full tenant export (JSON Lines, CSV, Parquet) with hashed manifest; second approver required; 7-day link. \| Acceptance: Requester cannot approve (DB check C | Partially covered | Part 3.3 ENT-189 saas_export_job; Part 9.9 CAP-X3-07 | export_job adopted: second approver CHECK (C2-T2), jsonl/csv/parquet, manifest hash, 7-day link CHECK (C3-04) | DEC-673, FR-V12-I-020, TC-V12-I-020 | Matched |
| ENT-DAT-02 | ENT-DAT-02 P1 Customer-managed keys (AWS KMS, Azure Key Vault, GCP KMS) with rotation; key revocation crypto-shreds data. \| Acceptance: Invalid key reference rejected; re | Partially covered | Part 9.9 CAP-X3-15 ten_tenant_key (AWS KMS, ap-south-1 only, ASSUMPTION-704) | Multi-cloud KEK adapters (AWS KMS, Azure Key Vault, GCP KMS), per-tenant DEKs, revocation crypto-shred trigger (C3-09) | DEC-671, ADR-213, CONFLICT-910, FR-V12-I-021, TC-V12-I-015 | Matched |
| ENT-DAT-03 | ENT-DAT-03 P0 Data residency by region chosen at onboarding: India and EU now; US, UK, Middle East and APAC planned. \| Acceptance: Cross-region write test fails (CJ-R09). | Conflict | DEC-421 Supabase Mumbai only; Part 11.5a CONFLICT-832 | tenant.data_region fixed at onboarding + per-region database guard (C3-05); EU activation held | CONFLICT-832 (Part 11.5a), DEC-667, TC-V12-I-011/012 | Pending Founder decision |
| ENT-DAT-04 | ENT-DAT-04 P1 Sandbox environments with synthetic data only; personal data is never copied. \| Acceptance: Sandbox clone contains no personal fields; promotion needs revie | Not covered | DEC-420 agent sandboxes synthetic only (build tooling, not tenant sandboxes) | sandbox_environment adopted with contains_personal_data=false CHECK; synthetic seed generator; reviewer promotion | DEC-674, FR-V12-I-022 | Matched |
| ENT-DAT-05 | ENT-DAT-05 P1 Configuration promotion sandbox → production as a reviewed configuration revision. \| Acceptance: Self-approval rejected; promoted revision is immutable. \| C | Partially covered | Part 3.3 ENT-168 aut_config_revision (immutable approved revision) | config_promotion + configuration_revision (C3-11) with requester<>reviewer and immutability | DEC-674, FR-V12-I-022 | Matched |
| C2-T1 | C2-T1: Role with Runs:create + Runs:approve -> Rejected by SoD trigger | Not covered | No equivalent DB test in Part 3.3/6.x | Reproduced on PostgreSQL 16.15 (assembly/v12/i_ddl/v12_tests.out) and re-run on the C3 build (TC-V12-I-032) | TC-V12-I-032 | Matched |
| C2-T2 | C2-T2: Export approved by its requester -> Rejected (check) | Not covered | No equivalent DB test in Part 3.3/6.x | Reproduced on PostgreSQL 16.15 (assembly/v12/i_ddl/v12_tests.out) and re-run on the C3 build (TC-V12-I-032) | TC-V12-I-032 | Matched |
| C2-T3 | C2-T3: Sandbox promotion approved by its requester -> Rejected (check) | Not covered | No equivalent DB test in Part 3.3/6.x | Reproduced on PostgreSQL 16.15 (assembly/v12/i_ddl/v12_tests.out) and re-run on the C3 build (TC-V12-I-032) | TC-V12-I-032 | Matched |
| C2-T4 | C2-T4: SSO enforced without verified domain / break-glass -> Rejected (check) | Not covered | No equivalent DB test in Part 3.3/6.x | Reproduced on PostgreSQL 16.15 (assembly/v12/i_ddl/v12_tests.out) and re-run on the C3 build (TC-V12-I-032) | TC-V12-I-032 | Matched |
| C2-T5 | C2-T5: Sandbox flagged as containing personal data -> Rejected (check) | Not covered | No equivalent DB test in Part 3.3/6.x | Reproduced on PostgreSQL 16.15 (assembly/v12/i_ddl/v12_tests.out) and re-run on the C3 build (TC-V12-I-032) | TC-V12-I-032 | Matched |
| C2-T6 | C2-T6: Production connector without legal and security review -> Rejected (check) | Not covered | No equivalent DB test in Part 3.3/6.x | Reproduced on PostgreSQL 16.15 (assembly/v12/i_ddl/v12_tests.out) and re-run on the C3 build (TC-V12-I-032) | TC-V12-I-032 | Matched |
| C2-T7 | C2-T7: Critical finding due later than 7 days -> Rejected (check) | Not covered | No equivalent DB test in Part 3.3/6.x | Reproduced on PostgreSQL 16.15 (assembly/v12/i_ddl/v12_tests.out) and re-run on the C3 build (TC-V12-I-032) | TC-V12-I-032 | Matched |
| C2-T8 | C2-T8: Invoice total ≠ net + tax -> Rejected (check) | Not covered | No equivalent DB test in Part 3.3/6.x | Reproduced on PostgreSQL 16.15 (assembly/v12/i_ddl/v12_tests.out) and re-run on the C3 build (TC-V12-I-032) | TC-V12-I-032 | Matched |
| C2-T9 | C2-T9: api_key table has a plaintext key column -> 0 such columns | Not covered | No equivalent DB test in Part 3.3/6.x | Reproduced on PostgreSQL 16.15 (assembly/v12/i_ddl/v12_tests.out) and re-run on the C3 build (TC-V12-I-032) | TC-V12-I-032 | Matched |
| C2-T10 | C2-T10: Tenant B reads tenant A API keys; query without context -> 0 rows; fails closed | Not covered | No equivalent DB test in Part 3.3/6.x | Reproduced on PostgreSQL 16.15 (assembly/v12/i_ddl/v12_tests.out) and re-run on the C3 build (TC-V12-I-032) | TC-V12-I-032 | Matched |
| C2-T11 | C2-T11: Valid permission and invoice rows -> Accepted | Not covered | No equivalent DB test in Part 3.3/6.x | Reproduced on PostgreSQL 16.15 (assembly/v12/i_ddl/v12_tests.out) and re-run on the C3 build (TC-V12-I-032) | TC-V12-I-032 | Matched |
| DB-T2 | DB-T2: Query without app.tenant_id -> Fails closed (error) | Conflict | Part 3.3 §3.3.9.6 unset-variable test (zero rows) | Reproduced (v12_tests.out); re-run on C3 build (c3_v12_regression.out); missing context now raises an error (DEC-662) | TC-V12-I-032, CONFLICT-909, DEC-662 | Matched |
| DB-T6 | DB-T6: Effect with preflight HOLD -> Rejected (check constraint) | Partially covered | Part 3.1 PDP recheck at dispatch | Reproduced (v12_tests.out); re-run on C3 build (c3_v12_regression.out) | TC-V12-I-032 | Matched |
| DB-T7 | DB-T7: Model ID on deterministic step -> Rejected (check constraint) | Partially covered | Part 3.3 CK-16 (tier rows) | Reproduced (v12_tests.out); re-run on C3 build (c3_v12_regression.out) | TC-V12-I-032 | Matched |
| I-26-P-001 | Appendix C2 adds 19 tables with 14 row-level security policies, applied on top of Appendix C in PostgreSQL 16 (137 tables, 120 policies). Tests: | Partially covered | Part 3.3 §3.3.5, §3.3.9; Part 3.6a | Adopted in Part 11.9 §11.9.5 (DDL-V12-I conventions) | DEC-661, DEC-662 | Matched |
| I-26-P-002 | Appendix C contains the full proposed DDL. It was applied to PostgreSQL 16.15 (pgvector line skipped because the extension was not installed in the test environment) and  | Partially covered | Part 3.3 §3.3.5, §3.3.9; Part 3.6a | Adopted in Part 11.9 §11.9.5 (DDL-V12-I conventions) | DEC-661, DEC-662 | Matched |
| I-26-P-003 | Canonical physical schema direction: The graph below defines candidate logical data relationships and constraints; approved PostgreSQL DDL and migration required. Version | Partially covered | Part 3.3 §3.3.5, §3.3.9; Part 3.6a | Adopted in Part 11.9 §11.9.5 (DDL-V12-I conventions) | DEC-661, DEC-662 | Matched |
| I-26-P-004 | Requirement: Division stable ID and scoped company FK; lifecycle independent of name; all relevant records use reference. | Partially covered | Part 3.3 §3.3.5, §3.3.9; Part 3.6a | Adopted in Part 11.9 §11.9.5 (DDL-V12-I conventions) | DEC-661, DEC-662 | Matched |
| I-26-P-005 | Acceptance: MT-TC-MT-09 — Create and rename division; linked offering remains valid; cross-company edit denied. | Partially covered | Part 3.3 §3.3.5, §3.3.9; Part 3.6a | Adopted in Part 11.9 §11.9.5 (DDL-V12-I conventions) | DEC-661, DEC-662 | Matched |
| I-26-P-006 | P0 \| Owner: Data architecture \| BRD chapter 07 \| Production acceptance pending. | Partially covered | Part 3.3 §3.3.5, §3.3.9; Part 3.6a | Adopted in Part 11.9 §11.9.5 (DDL-V12-I conventions) | DEC-661, DEC-662 | Matched |
| I-26-P-007 | Requirement: Brand owned by division; scoped brand configuration and approved claims; reusable in offering records. | Partially covered | Part 3.3 §3.3.5, §3.3.9; Part 3.6a | Adopted in Part 11.9 §11.9.5 (DDL-V12-I conventions) | DEC-661, DEC-662 | Matched |
| I-26-P-008 | Acceptance: MT-TC-MT-10 — Two brands with same name in different divisions; no leakage across scope. | Partially covered | Part 3.3 §3.3.5, §3.3.9; Part 3.6a | Adopted in Part 11.9 §11.9.5 (DDL-V12-I conventions) | DEC-661, DEC-662 | Matched |
| I-26-P-009 | P1 \| Owner: Business configuration \| BRD chapter 07 \| Production acceptance pending. | Partially covered | Part 3.3 §3.3.5, §3.3.9; Part 3.6a | Adopted in Part 11.9 §11.9.5 (DDL-V12-I conventions) | DEC-661, DEC-662 | Matched |
| I-26-P-010 | Requirement: Product, service, programme, solution separate from platform SKU; versioned brand FK, status, currency and claims. | Partially covered | Part 3.3 §3.3.5, §3.3.9; Part 3.6a | Adopted in Part 11.9 §11.9.5 (DDL-V12-I conventions) | DEC-661, DEC-662 | Matched |
| I-26-P-011 | Acceptance: MT-TC-MT-11 — One tenant selects one automation SKU for two offerings; no duplicated definition or auto-charge. | Partially covered | Part 3.3 §3.3.5, §3.3.9; Part 3.6a | Adopted in Part 11.9 §11.9.5 (DDL-V12-I conventions) | DEC-661, DEC-662 | Matched |
| I-26-P-012 | P0 \| Owner: Product / data architecture \| BRD chapter 07 \| Production acceptance pending. | Partially covered | Part 3.3 §3.3.5, §3.3.9; Part 3.6a | Adopted in Part 11.9 §11.9.5 (DDL-V12-I conventions) | DEC-661, DEC-662 | Matched |
| I-26-P-013 | Requirement: Market profiles reused through offering-market associations; each market independently eligible. | Partially covered | Part 3.3 §3.3.5, §3.3.9; Part 3.6a | Adopted in Part 11.9 §11.9.5 (DDL-V12-I conventions) | DEC-661, DEC-662 | Matched |
| I-26-P-014 | Acceptance: MT-TC-MT-18 — One offering mapped to two markets; cross-company market link denied. | Partially covered | Part 3.3 §3.3.5, §3.3.9; Part 3.6a | Adopted in Part 11.9 §11.9.5 (DDL-V12-I conventions) | DEC-661, DEC-662 | Matched |
| I-26-P-015 | P0 \| Owner: Data architecture \| BRD chapter 07 \| Production acceptance pending. | Partially covered | Part 3.3 §3.3.5, §3.3.9; Part 3.6a | Adopted in Part 11.9 §11.9.5 (DDL-V12-I conventions) | DEC-661, DEC-662 | Matched |
| I-26-P-016 | Requirement: Normalized IDs, scoped FK, aliases and dedup; no separate copies per service. Retain historical snapshots where required. | Partially covered | Part 3.3 §3.3.5, §3.3.9; Part 3.6a | Adopted in Part 11.9 §11.9.5 (DDL-V12-I conventions) | DEC-661, DEC-662 | Matched |
| I-26-P-017 | Acceptance: MT-TC-MT-33 — Rename master; dependent lookup reflects name; duplicate scoped natural key rejected. | Partially covered | Part 3.3 §3.3.5, §3.3.9; Part 3.6a | Adopted in Part 11.9 §11.9.5 (DDL-V12-I conventions) | DEC-661, DEC-662 | Matched |
| I-26-P-018 | P0 \| Owner: Data architecture \| BRD chapter 06 \| Production acceptance pending. | Partially covered | Part 3.3 §3.3.5, §3.3.9; Part 3.6a | Adopted in Part 11.9 §11.9.5 (DDL-V12-I conventions) | DEC-661, DEC-662 | Matched |
| I-26-P-019 | Proposed physical schema additions: Do not execute these design proposals as DDL. Reconcile with existing 149 historical entities and actual schema. Use scoped UUID/FKs,  | Partially covered | Part 3.3 §3.3.5, §3.3.9; Part 3.6a | Adopted in Part 11.9 §11.9.5 (DDL-V12-I conventions) | DEC-661, DEC-662 | Matched |
| I-26-P-020 | GC-05 · P0 · Database performance and pooling | Partially covered | Part 3.3 §3.3.5, §3.3.9; Part 3.6a | Adopted in Part 11.9 §11.9.5 (DDL-V12-I conventions) | DEC-661, DEC-662 | Matched |
| I-26-P-021 | Requirement: Profile slow queries, use scoped indexes and connection pooling; test transaction-local context reset. | Partially covered | Part 3.3 §3.3.5, §3.3.9; Part 3.6a | Adopted in Part 11.9 §11.9.5 (DDL-V12-I conventions) | DEC-661, DEC-662 | Matched |
| I-26-P-022 | Acceptance OPT-TC-GC-05: Explain plans improve target query; pool reuse cannot expose another tenant. | Partially covered | Part 3.3 §3.3.5, §3.3.9; Part 3.6a | Adopted in Part 11.9 §11.9.5 (DDL-V12-I conventions) | DEC-661, DEC-662 | Matched |
| I-26-P-023 | Owner: FinOps / platform engineering \| BRD chapter 11 \| Website: No new website interaction; production requirement where applicable \| Admin: A089 requirement register; o | Partially covered | Part 3.3 §3.3.5, §3.3.9; Part 3.6a | Adopted in Part 11.9 §11.9.5 (DDL-V12-I conventions) | DEC-661, DEC-662 | Matched |
| I-26-P-024 | ST-12 · P0 · Backward-compatible schema migration | Partially covered | Part 3.3 §3.3.5, §3.3.9; Part 3.6a | Adopted in Part 11.9 §11.9.5 (DDL-V12-I conventions) | DEC-661, DEC-662 | Matched |
| I-26-P-025 | Requirement: Use expand/migrate/contract and versioned events; test old/new workers together. | Partially covered | Part 3.3 §3.3.5, §3.3.9; Part 3.6a | Adopted in Part 11.9 §11.9.5 (DDL-V12-I conventions) | DEC-661, DEC-662 | Matched |
| I-26-P-026 | Acceptance OPT-TC-ST-12: Mixed-version fixture handles supported events without lost data. | Partially covered | Part 3.3 §3.3.5, §3.3.9; Part 3.6a | Adopted in Part 11.9 §11.9.5 (DDL-V12-I conventions) | DEC-661, DEC-662 | Matched |
| I-26-P-027 | Owner: Reliability / SRE \| BRD chapter 21 \| Website: No new website interaction; production requirement where applicable \| Admin: A089 requirement register; operational i | Partially covered | Part 3.3 §3.3.5, §3.3.9; Part 3.6a | Adopted in Part 11.9 §11.9.5 (DDL-V12-I conventions) | DEC-661, DEC-662 | Matched |
| I-26-P-028 | Proposed common physical design (review before migrations): uuid IDs, scoped FK, UTC timestamps, optimistic version, immutable posted audit/ledger, no secrets in payload. | Partially covered | Part 3.3 §3.3.5, §3.3.9; Part 3.6a | Adopted in Part 11.9 §11.9.5 (DDL-V12-I conventions) | DEC-661, DEC-662 | Matched |
| I-26-P-029 | Extend the existing schema after migration review; do not execute draft DDL. All private keys include tenant/company scope and appropriate RLS, indexes, retention and aud | Partially covered | Part 3.3 §3.3.5, §3.3.9; Part 3.6a | Adopted in Part 11.9 §11.9.5 (DDL-V12-I conventions) | DEC-661, DEC-662 | Matched |
| I-26-V6-Organization | Organization: tenant_id, organization_id, name \| Composite FK tenant; scoped unique normalized name | Not covered | new (DEC-581 Part 11.5a; ten_organization) | Full DDL in Appendix C or C3-11; mapping §11.9.4.2 | DEC-660, FR-V12-I-010 | Matched |
| I-26-V6-CompanyOperatingCountry | CompanyOperatingCountry: tenant_id, company_id, country_code \| Unique company/country; distinct target markets | Not covered | new company_operating_country (C3-11) | Full DDL in Appendix C or C3-11; mapping §11.9.4.2 | DEC-660, FR-V12-I-010 | Matched |
| I-26-V6-Division | Division: tenant_id, company_id, division_id, name \| Composite FK company; scoped unique normalized name | Partially covered | ENT-003 ten_business_line | Full DDL in Appendix C or C3-11; mapping §11.9.4.2 | DEC-660, FR-V12-I-010 | Matched |
| I-26-V6-Brand | Brand: tenant_id, company_id, division_id, brand_id \| Composite FK division; retain history | Not covered | new ten_brand | Full DDL in Appendix C or C3-11; mapping §11.9.4.2 | DEC-660, FR-V12-I-010 | Matched |
| I-26-V6-Offering | Offering: tenant_id, company_id, brand_id, offering_id, type, version, status, claims_ref, price, currency \| Scoped FK brand; status and currency checks; versioned price/ | Partially covered | ENT-016 cat_offering (+brand_id) | Full DDL in Appendix C or C3-11; mapping §11.9.4.2 | DEC-660, FR-V12-I-010 | Matched |
| I-26-V6-Market | Market: tenant_id, company_id, market_id, country, region, timezone, language, currency, policy_ref \| Scoped company FK; validate IANA zone and approved policy | Not covered | new ten_market | Full DDL in Appendix C or C3-11; mapping §11.9.4.2 | DEC-660, FR-V12-I-010 | Matched |
| I-26-V6-OfferingMarket | OfferingMarket: tenant_id, company_id, offering_id, market_id \| Both FKs same company; unique pair | Not covered | new offering_market (C3-11) | Full DDL in Appendix C or C3-11; mapping §11.9.4.2 | DEC-660, FR-V12-I-010 | Matched |
| I-26-V6-ChannelAccountMarket | ChannelAccountMarket: tenant_id, company_id, account_id, market_id \| Both FKs same company; unique pair | Not covered | new channel_account_market (C3-11) | Full DDL in Appendix C or C3-11; mapping §11.9.4.2 | DEC-660, FR-V12-I-010 | Matched |
| I-26-V6-WorkflowConfiguration | WorkflowConfiguration: tenant_id, company_id, config_id, offering_id, market_id, account_id, sku_id, wf_id, wf_version, budget, currency, authority, schedule, status \| Co | Not covered | new workflow_configuration (C3-11) | Full DDL in Appendix C or C3-11; mapping §11.9.4.2 | DEC-660, FR-V12-I-010 | Matched |
| I-26-V6-ConfigurationRevision | ConfigurationRevision: tenant_id, config_revision_id, scope, base_version, requester_id, reviewer_id, snapshot_ref, status \| Immutable history; compare-and-swap; separate | Partially covered | ENT-168 aut_config_revision (+C3-11 configuration_revision) | Full DDL in Appendix C or C3-11; mapping §11.9.4.2 | DEC-660, FR-V12-I-010 | Matched |
| I-26-V6-PortfolioGrant | PortfolioGrant: portfolio_id, tenant_id, company_id, grant_id, dimensions, expiry, revoked_at \| Explicit scope; no global wildcard; audit | Partially covered | ten_membership_grant (Owner Portfolio) | Full DDL in Appendix C or C3-11; mapping §11.9.4.2 | DEC-660, FR-V12-I-010 | Matched |
| I-26-V6-BusinessEvent | BusinessEvent: tenant_id, company_id, event_id, offering_id, market_id, account_id, campaign_id, sku_id, wf_id, amount_minor, currency, occurred_at \| Idempotency, nullabl | Partially covered | ENT-124 mkt_attribution_event + ops_domain_event | Full DDL in Appendix C or C3-11; mapping §11.9.4.2 | DEC-660, FR-V12-I-010 | Matched |
| I-26-V6-FXRate | FXRate: rate_id, base_currency, quote_currency, effective_at, source, rate_decimal, approved_version \| Positive rate; timestamp/source/direction; immutable approved versi | Partially covered | ENT-198 ana_fx_snapshot | Full DDL in Appendix C or C3-11; mapping §11.9.4.2 | DEC-660, FR-V12-I-010 | Matched |
| MT-09 | MT-09 (requirement, acceptance MT-TC-MT-09, P0/P1, Data architecture) | Partially covered | Part 3.3 §3.3.4.1; Part 11.5a DEC-581 | Hierarchy DDL with composite company-pinned FKs (C3-11) and scoped unique normalized names | DEC-660, FR-V12-I-010, TC-V12-I-030 | Matched |
| MT-10 | MT-10 (requirement, acceptance MT-TC-MT-10, P0/P1, Data architecture) | Partially covered | Part 3.3 §3.3.4.1; Part 11.5a DEC-581 | Hierarchy DDL with composite company-pinned FKs (C3-11) and scoped unique normalized names | DEC-660, FR-V12-I-010, TC-V12-I-030 | Matched |
| MT-11 | MT-11 (requirement, acceptance MT-TC-MT-11, P0/P1, Data architecture) | Partially covered | Part 3.3 §3.3.4.1; Part 11.5a DEC-581 | Hierarchy DDL with composite company-pinned FKs (C3-11) and scoped unique normalized names | DEC-660, FR-V12-I-010, TC-V12-I-030 | Matched |
| MT-18 | MT-18 (requirement, acceptance MT-TC-MT-18, P0/P1, Data architecture) | Partially covered | Part 3.3 §3.3.4.1; Part 11.5a DEC-581 | Hierarchy DDL with composite company-pinned FKs (C3-11) and scoped unique normalized names | DEC-660, FR-V12-I-010, TC-V12-I-030 | Matched |
| MT-33 | MT-33 (requirement, acceptance MT-TC-MT-33, P0/P1, Data architecture) | Partially covered | Part 3.3 §3.3.4.1; Part 11.5a DEC-581 | Hierarchy DDL with composite company-pinned FKs (C3-11) and scoped unique normalized names | DEC-660, FR-V12-I-010, TC-V12-I-030 | Matched |
| I-26-V5-opt_step_checkpoint | opt_step_checkpoint: run_id; step_id; step_version; state; artifact_ref; effect_ref; attempts; lease; recorded_at \| Unique run/step/attempt; conditional state transitions | Partially covered | ENT-163 aut_step_run | Mapped or created in C3-12 | FR-V12-I-030 | Matched |
| I-26-V5-opt_sli_sample | opt_sli_sample: component; tenant_scope; metric_version; time; numerator; denominator; status \| Aggregate by period; missing data explicit | Not covered | new sli_sample (C3-12) | Mapped or created in C3-12 | FR-V12-I-030 | Matched |
| I-26-V5-opt_customer_value | opt_customer_value: tenant/sku/period; accepted_count; allowance; outcome_evidence; assumption_version \| Scoped unique tenant/SKU/period; no guaranteed value | Not covered | new customer_value (C3-12) | Mapped or created in C3-12 | FR-V12-I-030 | Matched |
| I-26-V5-opt_feedback_case | opt_feedback_case: tenant; case_id; revision; output_ref; topic; rating; CES; NPS; owner; state; resolution_ref \| Scoped version; retention/consent; no automatic closure | Partially covered | crm_survey_response; new feedback_case (C3-12) | Mapped or created in C3-12 | FR-V12-I-030 | Matched |
| I-26-V5-opt_journey_event | opt_journey_event: event_id; cohort; acquisition_source; consent; stage; sku; occurred_at; correlation \| Dedup; anonymous minimized; separate operator/subscriber events | Partially covered | ENT-124 mkt_attribution_event; new journey_event (C3-12) | Mapped or created in C3-12 | FR-V12-I-030 | Matched |
| DB-V2-ARTIFACT | DB-V2-ARTIFACT: id uuid; tenant/company; domain; schema_version; payload jsonb validated against registry; source_ref; hash; revision; retention_class | Partially covered | generic domain shape + domain_schema_registry (C3-10) | Mapped (§11.9.4.3) | DEC-661 | Matched |
| DB-V2-EFFECT | DB-V2-EFFECT: id; scoped run/step; action_digest; approval_ref; provider_ref; status; idempotency_key unique scoped; reconciliation_at | Partially covered | effect (Appendix C) -> aut_effect | Mapped (§11.9.4.3) | DEC-661 | Matched |
| DB-V2-USAGE | DB-V2-USAGE: id; scope; service_id; period; reservation/ref; delta integer; currency; charge_minor; unique event; append only | Partially covered | ENT-183 + usage_reservation (C3-12) | Mapped (§11.9.4.3) | DEC-661 | Matched |
| I-26-V4-domain_record_version | domain_record_version: tenant_id/company_id; record_id UUID; revision int; payload JSONB; reason text; actor_id; review_state; created_at \| Unique scoped record/revision; | Partially covered | new domain_record_version (C3-12) | Mapped or created (C3-12) | FR-V12-I-031 | Matched |
| I-26-V4-usage_reservation | usage_reservation: tenant/company/SKU/period/run; integer units; currency; minor-unit amount; reservation state; idempotency key \| Atomic balance reservation, unique run/ | Partially covered | new usage_reservation (C3-12); ai_cost_ledger reserve | Mapped or created (C3-12) | FR-V12-I-031 | Matched |
| I-DDL-NORLS-tenant | tenant carries tenant_id but has no RLS in Appendix C | Not covered | Part 3.3 §3.3.9.6 CI guard | RLS + FORCE + policies added (C3-13); CI guard TC-V12-I-027 | GAP-913 | Matched |
| I-DDL-NORLS-inbox | inbox carries tenant_id but has no RLS in Appendix C | Not covered | Part 3.3 §3.3.9.6 CI guard | RLS + FORCE + policies added (C3-13); CI guard TC-V12-I-027 | GAP-913 | Matched |
| I-DDL-NORLS-incident | incident carries tenant_id but has no RLS in Appendix C | Not covered | Part 3.3 §3.3.9.6 CI guard | RLS + FORCE + policies added (C3-13); CI guard TC-V12-I-027 | GAP-913 | Matched |
| I-DDL-NORLS-portfolio_grant | portfolio_grant carries tenant_id but has no RLS in Appendix C | Not covered | Part 3.3 §3.3.9.6 CI guard | RLS + FORCE + policies added (C3-13); CI guard TC-V12-I-027 | GAP-913 | Matched |
| I-DDL-TRG-role_permission_sod | enforce_sod() BEFORE INSERT on role_permission (ENT-ACC-02) | Partially covered | Part 2.3 SoD rules (application layer) | Extended to UPDATE and to user-level SoD (C3-06) | GAP-915, DEC-669, TC-V12-I-005/006 | Matched |
| I-DDL-CONV-01 | App connects as non-owner app_user and sets SET LOCAL app.tenant_id / app.company_ids | Partially covered | Part 3.3 §3.3.5, §3.3.9 | Adopted with C3 (company predicate actually enforced; ge_app = app_user = app_rw) | DEC-662, DEC-663 | Matched |
| I-DDL-CONV-03 | Domain tables referenced by the 156 workflows use a common scoped shape; payload validated by Appendix B | Partially covered | Part 3.3 §3.3.5, §3.3.9 | Adopted with C3 (company predicate actually enforced; ge_app = app_user = app_rw) | DEC-662, DEC-663 | Matched |
| I-DDL-CONV-04 | Missing context fails closed: current_setting raises when app.tenant_id is unset | Partially covered | Part 3.3 §3.3.5, §3.3.9 | Adopted with C3 (company predicate actually enforced; ge_app = app_user = app_rw) | DEC-662, DEC-663 | Matched |
| I-DDL-GAP-INDEX | 110 foreign keys without supporting index; 0 secondary indexes in Appendix C/C2 | Not covered | assembly/v12/i_ddl/analyze_catalog.out | Fixed in DDL-V12-I (C3) and verified by TC-V12-I tests | GAP-914 | Matched |
| I-DDL-GAP-GRANTS | No roles, grants or REVOKE in Appendix C/C2; audit and consent tables mutable | Not covered | assembly/v12/i_ddl/analyze_catalog.out | Fixed in DDL-V12-I (C3) and verified by TC-V12-I tests | GAP-915 | Matched |
| I-DDL-GAP-ENUM | 109 status/state/type columns without CHECK vocabulary | Not covered | assembly/v12/i_ddl/analyze_catalog.out | Fixed in DDL-V12-I (C3) and verified by TC-V12-I tests | GAP-915 | Matched |
| I-DDL-GAP-NULLSCOPE | Nullable tenant_id on outbox, inbox, portfolio_grant, incident | Not covered | assembly/v12/i_ddl/analyze_catalog.out | Fixed in DDL-V12-I (C3) and verified by TC-V12-I tests | GAP-913 | Matched |
| I-DDL-GAP-VECTOR | growth_embedding has no vector column although pgvector is enabled | Not covered | assembly/v12/i_ddl/analyze_catalog.out | Fixed in DDL-V12-I (C3) and verified by TC-V12-I tests | GAP-916 | Matched |
| I-DDL-GAP-SUPABASE | Supabase Data API roles (anon/authenticated) and service_role BYPASSRLS not addressed | Not covered | assembly/v12/i_ddl/analyze_catalog.out | Fixed in DDL-V12-I (C3) and verified by TC-V12-I tests | CONFLICT-906 | Matched |
| REC-15 | REC-15 · P1 / Analytics lead / Source D06,17 Timestamped scoped drill-down, record count, unknown indicators, original currency; stable cursor and bulk authority contract | Partially covered | Part 2.4 §2.31 (RPT-R rules); NFR-015 cursor | Drill-down contract: as-of timestamp, record count, unknown indicator, native currency; totals reconcile; bulk re-check (§11.9.5.11) | FR-V12-I-040, TC-V12-I-040 | Matched |
| PERF-01 | PERF-01 Initial: 25 owned startups +10 external tenants; 50 staff; 100k opportunities; 50 concurrent jobs; 10k scheduled actions/day. -> Dashboard p95 <=2s, async ACK p95 | Partially covered | Part 4.2 NFR-001..038 load tests LT-xx; DEC-031 design points | Adopted as binding performance acceptance profile (§11.9.5.12) | DEC-676, FR-V12-I-041 | Matched |
| PERF-02 | PERF-02 Growth: 50+ owned +100 external tenants; 250 staff; 1m opportunities; 250 concurrent jobs; 100k actions/day. -> Dashboard p95 <=2.5s, async ACK p95 <=2s. | Partially covered | Part 4.2 NFR-001..038 load tests LT-xx; DEC-031 design points | Adopted as binding performance acceptance profile (§11.9.5.12) | DEC-676, FR-V12-I-041 | Matched |
| PERF-03 | PERF-03 Burst: Proposed 2x approved short burst; test queue and tenant caps. -> No data corruption; bounded 429/queue response; recover to baseline. | Partially covered | Part 4.2 NFR-001..038 load tests LT-xx; DEC-031 design points | Adopted as binding performance acceptance profile (§11.9.5.12) | DEC-676, FR-V12-I-041 | Matched |
| PERF-04 | PERF-04 Endurance: Proposed 8h synthetic load at approved representative rate. -> No growing leak/queue backlog; budgets and outcomes reconcile. | Partially covered | Part 4.2 NFR-001..038 load tests LT-xx; DEC-031 design points | Adopted as binding performance acceptance profile (§11.9.5.12) | DEC-676, FR-V12-I-041 | Matched |
| PERF-05 | PERF-05 Projection: Track event committed to dashboard visible timestamp. -> Refresh <=60 seconds in approved workload. | Partially covered | Part 4.2 NFR-001..038 load tests LT-xx; DEC-031 design points | Adopted as binding performance acceptance profile (§11.9.5.12) | DEC-676, FR-V12-I-041 | Matched |
| PERF-06 | PERF-06 Recovery: Stop worker/provider, restart, replay synthetic event. -> No duplicate side effect; backlog drains within agreed recovery window. | Partially covered | Part 4.2 NFR-001..038 load tests LT-xx; DEC-031 design points | Adopted as binding performance acceptance profile (§11.9.5.12) | DEC-676, FR-V12-I-041 | Matched |
| PERF-07 | PERF-07 Noisy neighbor: One tenant at quota alongside another normal tenant. -> Quotas isolate service, no cross-tenant access. | Partially covered | Part 4.2 NFR-001..038 load tests LT-xx; DEC-031 design points | Adopted as binding performance acceptance profile (§11.9.5.12) | DEC-676, FR-V12-I-041 | Matched |
| V12 KPI-05 | V12 KPI-05 Initial dashboard p95 ≤ 2000 ms (50 staff; 100k scoped opportunities) | Conflict | Blueprint KPI-05 has a different meaning (Part 1 KPI register) | Namespaced as "V12 KPI-nn" (DEC-665); target adopted; sli_sample + metric_definition rows (C3-12) | CONFLICT-907, DEC-665, MET-V12-I | Matched |
| V12 KPI-06 | V12 KPI-06 Critical service availability ≥ 0.999 ratio (Rolling 30 days, defined service window; approved exclusions only) | Conflict | Blueprint KPI-06 has a different meaning (Part 1 KPI register) | Namespaced as "V12 KPI-nn" (DEC-665); target adopted; sli_sample + metric_definition rows (C3-12) | CONFLICT-907, DEC-665, MET-V12-I | Matched |
| V12 KPI-26 | V12 KPI-26 Growth dashboard p95 ≤ 2500 ms (250 staff; 1m scoped opportunities) | Conflict | Blueprint KPI-26 has a different meaning (Part 1 KPI register) | Namespaced as "V12 KPI-nn" (DEC-665); target adopted; sli_sample + metric_definition rows (C3-12) | CONFLICT-907, DEC-665, MET-V12-I | Matched |
| V12 KPI-27 | V12 KPI-27 Async acknowledgement p95 ≤ 2000 ms (Durable accept, verified webhooks, not external completion) | Conflict | Blueprint KPI-27 has a different meaning (Part 1 KPI register) | Namespaced as "V12 KPI-nn" (DEC-665); target adopted; sli_sample + metric_definition rows (C3-12) | CONFLICT-907, DEC-665, MET-V12-I | Matched |
| V12 KPI-28 | V12 KPI-28 Projection refresh ≤ 60 seconds (Committed event to scoped projection) | Conflict | Blueprint KPI-28 has a different meaning (Part 1 KPI register) | Namespaced as "V12 KPI-nn" (DEC-665); target adopted; sli_sample + metric_definition rows (C3-12) | CONFLICT-907, DEC-665, MET-V12-I | Matched |
| V12 KPI-29 | V12 KPI-29 LCP p75 ≤ 2500 ms (Representative website visits) | Conflict | Blueprint KPI-29 has a different meaning (Part 1 KPI register) | Namespaced as "V12 KPI-nn" (DEC-665); target adopted; sli_sample + metric_definition rows (C3-12) | CONFLICT-907, DEC-665, MET-V12-I | Matched |
| V12 KPI-30 | V12 KPI-30 INP p75 ≤ 200 ms (Representative website visits) | Conflict | Blueprint KPI-30 has a different meaning (Part 1 KPI register) | Namespaced as "V12 KPI-nn" (DEC-665); target adopted; sli_sample + metric_definition rows (C3-12) | CONFLICT-907, DEC-665, MET-V12-I | Matched |
| V12 KPI-31 | V12 KPI-31 CLS p75 ≤ 0.1 score (Representative website visits) | Conflict | Blueprint KPI-31 has a different meaning (Part 1 KPI register) | Namespaced as "V12 KPI-nn" (DEC-665); target adopted; sli_sample + metric_definition rows (C3-12) | CONFLICT-907, DEC-665, MET-V12-I | Matched |
| I-29-P-001 | Binding load profiles for performance acceptance (previously only in the historical annex). Targets are the release KPIs in chapter 34. | Partially covered | Part 2.4 §2.31; Part 3.3 ENT-124, ENT-191..199; Part 9.9 CAP-X3-04 | Specified in §11.9.5.11 (BusinessEvent fact, metric contract, attribution, consent-aware analytics) | DEC-672, ADR-214, FR-V12-I-042 | Matched |
| I-29-P-002 | Event attribution: Business event references trusted tenant/company, optional offering, market, account, campaign, SKU and workflow ID if evidenced, amount/currency and e | Partially covered | Part 2.4 §2.31; Part 3.3 ENT-124, ENT-191..199; Part 9.9 CAP-X3-04 | Specified in §11.9.5.11 (BusinessEvent fact, metric contract, attribution, consent-aware analytics) | DEC-672, ADR-214, FR-V12-I-042 | Matched |
| I-29-P-003 | Requirement: Separate ICP, segment, market eligibility and source rights by offering; no cross-product prospect assumptions. | Partially covered | Part 2.4 §2.31; Part 3.3 ENT-124, ENT-191..199; Part 9.9 CAP-X3-04 | Specified in §11.9.5.11 (BusinessEvent fact, metric contract, attribution, consent-aware analytics) | DEC-672, ADR-214, FR-V12-I-042 | Matched |
| I-29-P-004 | Acceptance: MT-TC-MT-13 — Configure two audiences; results use selected offering and evidence. | Partially covered | Part 2.4 §2.31; Part 3.3 ENT-124, ENT-191..199; Part 9.9 CAP-X3-04 | Specified in §11.9.5.11 (BusinessEvent fact, metric contract, attribution, consent-aware analytics) | DEC-672, ADR-214, FR-V12-I-042 | Matched |
| I-29-P-005 | P1 \| Owner: Marketing / analytics \| BRD chapter 13 \| Production acceptance pending. | Partially covered | Part 2.4 §2.31; Part 3.3 ENT-124, ENT-191..199; Part 9.9 CAP-X3-04 | Specified in §11.9.5.11 (BusinessEvent fact, metric contract, attribution, consent-aware analytics) | DEC-672, ADR-214, FR-V12-I-042 | Matched |
| I-29-P-006 | Requirement: Event scope references tenant/company/offering/market/account/campaign and workflow where known. No false attribution; missing values explicit. | Partially covered | Part 2.4 §2.31; Part 3.3 ENT-124, ENT-191..199; Part 9.9 CAP-X3-04 | Specified in §11.9.5.11 (BusinessEvent fact, metric contract, attribution, consent-aware analytics) | DEC-672, ADR-214, FR-V12-I-042 | Matched |
| I-29-P-007 | Acceptance: MT-TC-MT-27 — Service/workflow filter applies to attributed events; unknowns excluded and labeled. | Partially covered | Part 2.4 §2.31; Part 3.3 ENT-124, ENT-191..199; Part 9.9 CAP-X3-04 | Specified in §11.9.5.11 (BusinessEvent fact, metric contract, attribution, consent-aware analytics) | DEC-672, ADR-214, FR-V12-I-042 | Matched |
| I-29-P-008 | P0 \| Owner: Analytics \| BRD chapter 22 \| Production acceptance pending. | Partially covered | Part 2.4 §2.31; Part 3.3 ENT-124, ENT-191..199; Part 9.9 CAP-X3-04 | Specified in §11.9.5.11 (BusinessEvent fact, metric contract, attribution, consent-aware analytics) | DEC-672, ADR-214, FR-V12-I-042 | Matched |
| I-29-P-009 | Requirement: Separate business outcomes from workflow runs; use authorized scope and event dimensions; unmeasured metric shown unavailable. | Partially covered | Part 2.4 §2.31; Part 3.3 ENT-124, ENT-191..199; Part 9.9 CAP-X3-04 | Specified in §11.9.5.11 (BusinessEvent fact, metric contract, attribution, consent-aware analytics) | DEC-672, ADR-214, FR-V12-I-042 | Matched |
| I-29-P-010 | Acceptance: MT-TC-MT-31 — Compare two offering ledgers, count only matching events. | Partially covered | Part 2.4 §2.31; Part 3.3 ENT-124, ENT-191..199; Part 9.9 CAP-X3-04 | Specified in §11.9.5.11 (BusinessEvent fact, metric contract, attribution, consent-aware analytics) | DEC-672, ADR-214, FR-V12-I-042 | Matched |
| I-29-P-011 | P1 \| Owner: Analytics \| BRD chapter 22 \| Production acceptance pending. | Partially covered | Part 2.4 §2.31; Part 3.3 ENT-124, ENT-191..199; Part 9.9 CAP-X3-04 | Specified in §11.9.5.11 (BusinessEvent fact, metric contract, attribution, consent-aware analytics) | DEC-672, ADR-214, FR-V12-I-042 | Matched |
| I-29-P-012 | Analytics and outcome instrumentation: Use consent-aware events for public acquisition, private activation, accepted outputs, renewal, support and billing. Store event_id | Partially covered | Part 2.4 §2.31; Part 3.3 ENT-124, ENT-191..199; Part 9.9 CAP-X3-04 | Specified in §11.9.5.11 (BusinessEvent fact, metric contract, attribution, consent-aware analytics) | DEC-672, ADR-214, FR-V12-I-042 | Matched |
| I-29-P-013 | AT-14 · P1 · Consent-aware acquisition analytics | Partially covered | Part 2.4 §2.31; Part 3.3 ENT-124, ENT-191..199; Part 9.9 CAP-X3-04 | Specified in §11.9.5.11 (BusinessEvent fact, metric contract, attribution, consent-aware analytics) | DEC-672, ADR-214, FR-V12-I-042 | Matched |
| I-29-P-014 | Requirement: Use first-party event schema, consent and attribution windows; minimize identifiers. | Partially covered | Part 2.4 §2.31; Part 3.3 ENT-124, ENT-191..199; Part 9.9 CAP-X3-04 | Specified in §11.9.5.11 (BusinessEvent fact, metric contract, attribution, consent-aware analytics) | DEC-672, ADR-214, FR-V12-I-042 | Matched |
| I-29-P-015 | Acceptance OPT-TC-AT-14: Opt-out blocks optional analytics; denominators distinguish unknown source. | Partially covered | Part 2.4 §2.31; Part 3.3 ENT-124, ENT-191..199; Part 9.9 CAP-X3-04 | Specified in §11.9.5.11 (BusinessEvent fact, metric contract, attribution, consent-aware analytics) | DEC-672, ADR-214, FR-V12-I-042 | Matched |
| I-29-P-016 | Owner: Growth / marketing \| BRD chapter 12 \| Website: No new website interaction; production requirement where applicable \| Admin: A089 fictional channel metrics; no anal | Partially covered | Part 2.4 §2.31; Part 3.3 ENT-124, ENT-191..199; Part 9.9 CAP-X3-04 | Specified in §11.9.5.11 (BusinessEvent fact, metric contract, attribution, consent-aware analytics) | DEC-672, ADR-214, FR-V12-I-042 | Matched |
| I-29-P-017 | CV-14 · P1 · Controlled conversion experiments | Partially covered | Part 2.4 §2.31; Part 3.3 ENT-124, ENT-191..199; Part 9.9 CAP-X3-04 | Specified in §11.9.5.11 (BusinessEvent fact, metric contract, attribution, consent-aware analytics) | DEC-672, ADR-214, FR-V12-I-042 | Matched |
| I-29-P-018 | Requirement: Use consent-aware allocation, metric, stopping rule and guardrails; avoid deceptive patterns. | Partially covered | Part 2.4 §2.31; Part 3.3 ENT-124, ENT-191..199; Part 9.9 CAP-X3-04 | Specified in §11.9.5.11 (BusinessEvent fact, metric contract, attribution, consent-aware analytics) | DEC-672, ADR-214, FR-V12-I-042 | Matched |
| I-29-P-019 | Acceptance OPT-TC-CV-14: Variant fixture reports denominator and uncertainty; no auto winner without review. | Partially covered | Part 2.4 §2.31; Part 3.3 ENT-124, ENT-191..199; Part 9.9 CAP-X3-04 | Specified in §11.9.5.11 (BusinessEvent fact, metric contract, attribution, consent-aware analytics) | DEC-672, ADR-214, FR-V12-I-042 | Matched |
| I-29-P-020 | Owner: Commercial / growth \| BRD chapter 12 \| Website: No new website interaction; production requirement where applicable \| Admin: A089 A/B arithmetic; no allocation or  | Partially covered | Part 2.4 §2.31; Part 3.3 ENT-124, ENT-191..199; Part 9.9 CAP-X3-04 | Specified in §11.9.5.11 (BusinessEvent fact, metric contract, attribution, consent-aware analytics) | DEC-672, ADR-214, FR-V12-I-042 | Matched |
| I-29-P-021 | CS-12 · P1 · CSAT, CES and NPS measurement | Partially covered | Part 2.4 §2.31; Part 3.3 ENT-124, ENT-191..199; Part 9.9 CAP-X3-04 | Specified in §11.9.5.11 (BusinessEvent fact, metric contract, attribution, consent-aware analytics) | DEC-672, ADR-214, FR-V12-I-042 | Matched |
| I-29-P-022 | Requirement: Collect optional feedback at defined milestones; report denominator and period. | Partially covered | Part 2.4 §2.31; Part 3.3 ENT-124, ENT-191..199; Part 9.9 CAP-X3-04 | Specified in §11.9.5.11 (BusinessEvent fact, metric contract, attribution, consent-aware analytics) | DEC-672, ADR-214, FR-V12-I-042 | Matched |
| I-29-P-023 | Acceptance OPT-TC-CS-12: Survey aggregates compute correctly; missing response not treated as satisfaction. | Partially covered | Part 2.4 §2.31; Part 3.3 ENT-124, ENT-191..199; Part 9.9 CAP-X3-04 | Specified in §11.9.5.11 (BusinessEvent fact, metric contract, attribution, consent-aware analytics) | DEC-672, ADR-214, FR-V12-I-042 | Matched |
| I-29-P-024 | Owner: Customer experience / support \| BRD chapter 22 \| Website: W28 local feedback fixture \| Admin: A089 CSAT/CES/NPS arithmetic \| Production status: not run. | Partially covered | Part 2.4 §2.31; Part 3.3 ENT-124, ENT-191..199; Part 9.9 CAP-X3-04 | Specified in §11.9.5.11 (BusinessEvent fact, metric contract, attribution, consent-aware analytics) | DEC-672, ADR-214, FR-V12-I-042 | Matched |
| I-29-P-025 | Metric contract: metric_id/version, formula, numerator/denominator, source event IDs, currency/timezone, period, filters, owner, baseline and threshold. Use verified outc | Partially covered | Part 2.4 §2.31; Part 3.3 ENT-124, ENT-191..199; Part 9.9 CAP-X3-04 | Specified in §11.9.5.11 (BusinessEvent fact, metric contract, attribution, consent-aware analytics) | DEC-672, ADR-214, FR-V12-I-042 | Matched |
| I-29-P-026 | Each KPI is a labeled synthetic local aggregate. Do not substitute run counts for actual business outcomes. Production calculations require metric definitions, denominato | Partially covered | Part 2.4 §2.31; Part 3.3 ENT-124, ENT-191..199; Part 9.9 CAP-X3-04 | Specified in §11.9.5.11 (BusinessEvent fact, metric contract, attribution, consent-aware analytics) | DEC-672, ADR-214, FR-V12-I-042 | Matched |
| I-29-VIEW-01 | View 1 Executive performance: Opportunity records; Open pipeline; Won deals; Sample receipts (Scoped synthetic business ledger and/or filtered run states; unavailable pro | Partially covered | Part 2.4 RP-01..30; Part 2.5 dashboards A087-A089 | Each label mapped to a production metric with formula (§11.9.5.11 table) and "synthetic" labelling rule | FR-V12-I-043, MET-V12-I-01..56 | Matched |
| I-29-VIEW-02 | View 2 Market intelligence: Market research runs; Evidence reviews; Held signals; Completed research (Scoped synthetic business ledger and/or filtered run states; unavail | Partially covered | Part 2.4 RP-01..30; Part 2.5 dashboards A087-A089 | Each label mapped to a production metric with formula (§11.9.5.11 table) and "synthetic" labelling rule | FR-V12-I-043, MET-V12-I-01..56 | Matched |
| I-29-VIEW-03 | View 3 Lead & contact intelligence: Discovered prospects; Qualified prospects; Contact & lead runs; Pending reviews (Scoped synthetic business ledger and/or filtered run  | Partially covered | Part 2.4 RP-01..30; Part 2.5 dashboards A087-A089 | Each label mapped to a production metric with formula (§11.9.5.11 table) and "synthetic" labelling rule | FR-V12-I-043, MET-V12-I-01..56 | Matched |
| I-29-VIEW-04 | View 4 Digital marketing: Marketing runs; Completed campaigns; Held campaign actions; Sample marketing receipts (Scoped synthetic business ledger and/or filtered run stat | Partially covered | Part 2.4 RP-01..30; Part 2.5 dashboards A087-A089 | Each label mapped to a production metric with formula (§11.9.5.11 table) and "synthetic" labelling rule | FR-V12-I-043, MET-V12-I-01..56 | Matched |
| I-29-VIEW-05 | View 5 Omnichannel engagement: Engagement runs; Completed messages / tasks; Held outreach; Channel records (Scoped synthetic business ledger and/or filtered run states; u | Partially covered | Part 2.4 RP-01..30; Part 2.5 dashboards A087-A089 | Each label mapped to a production metric with formula (§11.9.5.11 table) and "synthetic" labelling rule | FR-V12-I-043, MET-V12-I-01..56 | Matched |
| I-29-VIEW-06 | View 6 Follow-up & meetings: Follow-up runs; Meeting-stage records; Pending approvals; Held tasks (Scoped synthetic business ledger and/or filtered run states; unavailabl | Partially covered | Part 2.4 RP-01..30; Part 2.5 dashboards A087-A089 | Each label mapped to a production metric with formula (§11.9.5.11 table) and "synthetic" labelling rule | FR-V12-I-043, MET-V12-I-01..56 | Matched |
| I-29-VIEW-07 | View 7 Objection & negotiation: Negotiation runs; Proposal-stage records; Awaiting review; Held negotiations (Scoped synthetic business ledger and/or filtered run states; | Partially covered | Part 2.4 RP-01..30; Part 2.5 dashboards A087-A089 | Each label mapped to a production metric with formula (§11.9.5.11 table) and "synthetic" labelling rule | FR-V12-I-043, MET-V12-I-01..56 | Matched |
| I-29-VIEW-08 | View 8 Sales pipeline & closure: Open opportunities; Proposal-stage records; Won deals; Open pipeline (Scoped synthetic business ledger and/or filtered run states; unavai | Partially covered | Part 2.4 RP-01..30; Part 2.5 dashboards A087-A089 | Each label mapped to a production metric with formula (§11.9.5.11 table) and "synthetic" labelling rule | FR-V12-I-043, MET-V12-I-01..56 | Matched |
| I-29-VIEW-09 | View 9 Revenue & financial intelligence: Sample receipts; Open pipeline; Won deals; Financial runs (Scoped synthetic business ledger and/or filtered run states; unavailab | Partially covered | Part 2.4 RP-01..30; Part 2.5 dashboards A087-A089 | Each label mapped to a production metric with formula (§11.9.5.11 table) and "synthetic" labelling rule | FR-V12-I-043, MET-V12-I-01..56 | Matched |
| I-29-VIEW-10 | View 10 Customer success: Lifecycle runs; Completed lifecycle runs; Open reviews; Held lifecycle actions (Scoped synthetic business ledger and/or filtered run states; una | Partially covered | Part 2.4 RP-01..30; Part 2.5 dashboards A087-A089 | Each label mapped to a production metric with formula (§11.9.5.11 table) and "synthetic" labelling rule | FR-V12-I-043, MET-V12-I-01..56 | Matched |
| I-29-VIEW-11 | View 11 Partner & procurement: Partner / procurement runs; Completed runs; Pending reviews; Held purchasing actions (Scoped synthetic business ledger and/or filtered run  | Partially covered | Part 2.4 RP-01..30; Part 2.5 dashboards A087-A089 | Each label mapped to a production metric with formula (§11.9.5.11 table) and "synthetic" labelling rule | FR-V12-I-043, MET-V12-I-01..56 | Matched |
| I-29-VIEW-12 | View 12 AI & automation control: Total runs; Completed runs; Reserved units; Held / failed runs (Scoped synthetic business ledger and/or filtered run states; unavailable  | Partially covered | Part 2.4 RP-01..30; Part 2.5 dashboards A087-A089 | Each label mapped to a production metric with formula (§11.9.5.11 table) and "synthetic" labelling rule | FR-V12-I-043, MET-V12-I-01..56 | Matched |
| I-29-VIEW-13 | View 13 Governance & risk: Awaiting approval; Held runs; Failed runs; Uncertain outcomes (Scoped synthetic business ledger and/or filtered run states; unavailable product | Partially covered | Part 2.4 RP-01..30; Part 2.5 dashboards A087-A089 | Each label mapped to a production metric with formula (§11.9.5.11 table) and "synthetic" labelling rule | FR-V12-I-043, MET-V12-I-01..56 | Matched |
| I-29-VIEW-14 | View 14 Optimization intelligence: Optimization runs; Completed runs; Pending review; Held experiments (Scoped synthetic business ledger and/or filtered run states; unava | Partially covered | Part 2.4 RP-01..30; Part 2.5 dashboards A087-A089 | Each label mapped to a production metric with formula (§11.9.5.11 table) and "synthetic" labelling rule | FR-V12-I-043, MET-V12-I-01..56 | Matched |
| ENT-SEC-02 | ENT-SEC-02 P0 SBOM (CycloneDX or SPDX) for every release, stored with the release record. \| SBOM generated and signed for each artefact. \| DevOps lead R0 A129 | Partially covered | Part 4.1 SBOM (CycloneDX); Part 9.9 CAP-X3-19 (signing) | Specified in §11.9.5.13 | DEC-675 | Matched |
| ENT-SEC-03 | ENT-SEC-03 P0 Vulnerability remediation SLAs: Critical 7 days, High 30, Medium 90, Low 180 (proposed). \| Overdue critical blocks release (KPI-03). \| Security lead R1 A129 | Conflict | Part 4.1 §4.16.3 (Low = next maintenance) | Specified in §11.9.5.13 | CONFLICT-911, DEC-666 | Matched |
| ENT-SEC-04 | ENT-SEC-04 P0 Independent penetration test before each major release and at least annually (PEN-01…08). \| Report with no open critical/high before go-live. \| Security lea | Partially covered | Part 8.4 A7 two pen tests (R1, R2) | Specified in §11.9.5.13 | DEC-675 | Matched |
| ENT-SEC-05 | ENT-SEC-05 P2 Public bug-bounty programme after R3. \| Programme live with triage SLA. \| Security lead R3 W38 | Partially covered | Part 4.1 RECOMMENDATION-048 (bug bounty considered at W6) | Specified in §11.9.5.13 | DEC-675 | Matched |
| ENT-SEC-08 | ENT-SEC-08 P0 24×7 security monitoring and an incident-response plan linked to breach clocks (A121). \| Tabletop exercise each quarter. \| Security lead R2 A130 | Conflict | Part 4.3 out-of-hours paging Sev1 only (CONFLICT-113, DEC-044) | Specified in §11.9.5.13 | CONFLICT-905 | Pending Founder decision |
| PEN-01 | PEN-01 Admin identity: Try external token, revoked membership and wrong product audience against protected test endpoints. \| blocking: Any private read/write permitted. | Partially covered | Part 4.1 §4.16.2 pen-test scope | PEN-01..08 adopted as mandatory scope of every pen test; mapped to THR and TC (§11.9.5.13) | DEC-675, TC-V12-I-050..057 | Matched |
| PEN-02 | PEN-02 Tenant/issuer data: Seed separate tenants with same-looking identifiers; test API, worker, export, cache, storage and RAG. \| blocking: Cross-scope leak or mutation | Partially covered | Part 4.1 §4.16.2 pen-test scope | PEN-01..08 adopted as mandatory scope of every pen test; mapped to THR and TC (§11.9.5.13) | DEC-675, TC-V12-I-050..057 | Matched |
| PEN-03 | PEN-03 Website publication: Access unknown host, draft revision, private URL and mismatched domain. \| blocking: Draft or private content exposed. | Partially covered | Part 4.1 §4.16.2 pen-test scope | PEN-01..08 adopted as mandatory scope of every pen test; mapped to THR and TC (§11.9.5.13) | DEC-675, TC-V12-I-050..057 | Matched |
| PEN-04 | PEN-04 Portal invitations: Test expired/replayed token, foreign resource, revocation and signed URL. \| blocking: Unauthorized object access. | Partially covered | Part 4.1 §4.16.2 pen-test scope | PEN-01..08 adopted as mandatory scope of every pen test; mapped to THR and TC (§11.9.5.13) | DEC-675, TC-V12-I-050..057 | Matched |
| PEN-05 | PEN-05 Workflow/financial: Replay callback, stale approval, concurrent budget and receipt attempts in sandbox. \| blocking: Duplicate payment/message or bypass. | Partially covered | Part 4.1 §4.16.2 pen-test scope | PEN-01..08 adopted as mandatory scope of every pen test; mapped to THR and TC (§11.9.5.13) | DEC-675, TC-V12-I-050..057 | Matched |
| PEN-06 | PEN-06 AI: Untrusted source instructs model to expose private info or execute action; use synthetic evidence. \| blocking: Unauthorized retrieval/tool execution. | Partially covered | Part 4.1 §4.16.2 pen-test scope | PEN-01..08 adopted as mandatory scope of every pen test; mapped to THR and TC (§11.9.5.13) | DEC-675, TC-V12-I-050..057 | Matched |
| PEN-07 | PEN-07 Supply chain: Review SBOM/dependency and secret scan, artifact digest, least privilege and network boundaries. \| blocking: Unaccepted exploitable high/critical iss | Partially covered | Part 4.1 §4.16.2 pen-test scope | PEN-01..08 adopted as mandatory scope of every pen test; mapped to THR and TC (§11.9.5.13) | DEC-675, TC-V12-I-050..057 | Matched |
| PEN-08 | PEN-08 Incident readiness: Exercise containment, revoke access, stop dispatch, preserve logs and recover. \| blocking: No safe containment or recovery. | Partially covered | Part 4.1 §4.16.2 pen-test scope | PEN-01..08 adopted as mandatory scope of every pen test; mapped to THR and TC (§11.9.5.13) | DEC-675, TC-V12-I-050..057 | Matched |
| I-31-P-001 | Authorised testing only, against isolated environments with synthetic data; any production-blocking condition below stops release (KPI-03). | Partially covered | Part 4.1 §4.10–4.12, §4.16; Part 9.9 CAP-X3-26 PWA | Specified in §11.9.5.13–11.9.5.15 | DEC-675, FR-V12-I-051 | Matched |
| I-31-P-005 | Owner — Security + frontend | Partially covered | Part 4.1 §4.10–4.12, §4.16; Part 9.9 CAP-X3-26 PWA | Specified in §11.9.5.13–11.9.5.15 | DEC-675, FR-V12-I-051 | Matched |
| I-31-P-006 | Business requirement — An installable web experience may be offered after security review. Offline must not expose confidential customer data or dispatch external effects | Partially covered | Part 4.1 §4.10–4.12, §4.16; Part 9.9 CAP-X3-26 PWA | Specified in §11.9.5.13–11.9.5.15 | DEC-675, FR-V12-I-051 | Matched |
| I-31-P-007 | Functional contract — Production manifest/service worker may cache public assets only by default; authenticated API data no-store; clear private caches at logout; no back | Partially covered | Part 4.1 §4.10–4.12, §4.16; Part 9.9 CAP-X3-26 PWA | Specified in §11.9.5.13–11.9.5.15 | DEC-675, FR-V12-I-051 | Matched |
| I-31-P-008 | Scope / UI mapping — Website and Admin shell; cache policy | Partially covered | Part 4.1 §4.10–4.12, §4.16; Part 9.9 CAP-X3-26 PWA | Specified in §11.9.5.13–11.9.5.15 | DEC-675, FR-V12-I-051 | Matched |
| I-31-P-009 | Acceptance MOB-10-AT01 — Proposed: inspect service-worker cache and airplane-mode behavior; no private response persistence or external action. Not run. | Partially covered | Part 4.1 §4.10–4.12, §4.16; Part 9.9 CAP-X3-26 PWA | Specified in §11.9.5.13–11.9.5.15 | DEC-675, FR-V12-I-051 | Matched |
| I-31-P-010 | Security release rule: SEC-01–15 refine inherited BR-C05/06/09/11/13. Server-side authorization, non-owner RLS, secret vault, approved outbound gateway, malicious file qu | Partially covered | Part 4.1 §4.10–4.12, §4.16; Part 9.9 CAP-X3-26 PWA | Specified in §11.9.5.13–11.9.5.15 | DEC-675, FR-V12-I-051 | Matched |
| I-31-P-011 | SEC-06 · P0 · Tamper-evident audit records | Partially covered | Part 4.1 §4.10–4.12, §4.16; Part 9.9 CAP-X3-26 PWA | Specified in §11.9.5.13–11.9.5.15 | DEC-675, FR-V12-I-051 | Matched |
| I-31-P-012 | Requirement: Append versioned audit events with actor, scope, correlation and integrity chain; redact sensitive values. | Partially covered | Part 4.1 §4.10–4.12, §4.16; Part 9.9 CAP-X3-26 PWA | Specified in §11.9.5.13–11.9.5.15 | DEC-675, FR-V12-I-051 | Matched |
| I-31-P-013 | Acceptance OPT-TC-SEC-06: Modification detectable; unauthorized audit deletion rejected. | Partially covered | Part 4.1 §4.10–4.12, §4.16; Part 9.9 CAP-X3-26 PWA | Specified in §11.9.5.13–11.9.5.15 | DEC-675, FR-V12-I-051 | Matched |
| I-31-P-014 | Owner: Security / privacy engineering \| BRD chapter 20 \| Website: No new website interaction; production requirement where applicable \| Admin: A089 requirement register;  | Partially covered | Part 4.1 §4.10–4.12, §4.16; Part 9.9 CAP-X3-26 PWA | Specified in §11.9.5.13–11.9.5.15 | DEC-675, FR-V12-I-051 | Matched |
| I-31-P-015 | SEC-08 · P0 · Prompt-injection defenses | Partially covered | Part 4.1 §4.10–4.12, §4.16; Part 9.9 CAP-X3-26 PWA | Specified in §11.9.5.13–11.9.5.15 | DEC-675, FR-V12-I-051 | Matched |
| I-31-P-016 | Requirement: Treat external text as untrusted evidence; separate instructions, schemas and tools; validate output and egress. | Partially covered | Part 4.1 §4.10–4.12, §4.16; Part 9.9 CAP-X3-26 PWA | Specified in §11.9.5.13–11.9.5.15 | DEC-675, FR-V12-I-051 | Matched |
| I-31-P-017 | Acceptance OPT-TC-SEC-08: Adversarial document cannot override tool, approval or disclosure policy. | Partially covered | Part 4.1 §4.10–4.12, §4.16; Part 9.9 CAP-X3-26 PWA | Specified in §11.9.5.13–11.9.5.15 | DEC-675, FR-V12-I-051 | Matched |
| I-31-P-018 | Owner: Security / privacy engineering \| BRD chapter 20 \| Website: No new website interaction; production requirement where applicable \| Admin: A089 injection gate fixture | Partially covered | Part 4.1 §4.10–4.12, §4.16; Part 9.9 CAP-X3-26 PWA | Specified in §11.9.5.13–11.9.5.15 | DEC-675, FR-V12-I-051 | Matched |
| I-31-P-019 | SEC-09 · P0 · Data-loss prevention | Partially covered | Part 4.1 §4.10–4.12, §4.16; Part 9.9 CAP-X3-26 PWA | Specified in §11.9.5.13–11.9.5.15 | DEC-675, FR-V12-I-051 | Matched |
| I-31-P-020 | Requirement: Classify and redact/minimize data before model/provider transmission; hold prohibited fields. | Partially covered | Part 4.1 §4.10–4.12, §4.16; Part 9.9 CAP-X3-26 PWA | Specified in §11.9.5.13–11.9.5.15 | DEC-675, FR-V12-I-051 | Matched |
| I-31-P-021 | Acceptance OPT-TC-SEC-09: Seeded sensitive fixture blocked or redacted; approved fields preserved. | Partially covered | Part 4.1 §4.10–4.12, §4.16; Part 9.9 CAP-X3-26 PWA | Specified in §11.9.5.13–11.9.5.15 | DEC-675, FR-V12-I-051 | Matched |
| I-31-P-022 | Owner: Security / privacy engineering \| BRD chapter 20 \| Website: No new website interaction; production requirement where applicable \| Admin: A089 DLP gate fixture (not  | Partially covered | Part 4.1 §4.10–4.12, §4.16; Part 9.9 CAP-X3-26 PWA | Specified in §11.9.5.13–11.9.5.15 | DEC-675, FR-V12-I-051 | Matched |
| I-31-P-023 | SEC-10 · P0 · Safe private file ingestion | Partially covered | Part 4.1 §4.10–4.12, §4.16; Part 9.9 CAP-X3-26 PWA | Specified in §11.9.5.13–11.9.5.15 | DEC-675, FR-V12-I-051 | Matched |
| I-31-P-024 | Requirement: Quarantine, scan, validate MIME and size, isolate parsers and restrict retrieval until approved. | Partially covered | Part 4.1 §4.10–4.12, §4.16; Part 9.9 CAP-X3-26 PWA | Specified in §11.9.5.13–11.9.5.15 | DEC-675, FR-V12-I-051 | Matched |
| I-31-P-025 | Acceptance OPT-TC-SEC-10: Malicious or mismatched file quarantined; no agent access before clearance. | Partially covered | Part 4.1 §4.10–4.12, §4.16; Part 9.9 CAP-X3-26 PWA | Specified in §11.9.5.13–11.9.5.15 | DEC-675, FR-V12-I-051 | Matched |
| I-31-P-026 | Owner: Security / privacy engineering \| BRD chapter 20 \| Website: No new website interaction; production requirement where applicable \| Admin: A089 requirement register;  | Partially covered | Part 4.1 §4.10–4.12, §4.16; Part 9.9 CAP-X3-26 PWA | Specified in §11.9.5.13–11.9.5.15 | DEC-675, FR-V12-I-051 | Matched |
| I-31-P-027 | SEC-11 · P0 · Browser security controls | Partially covered | Part 4.1 §4.10–4.12, §4.16; Part 9.9 CAP-X3-26 PWA | Specified in §11.9.5.13–11.9.5.15 | DEC-675, FR-V12-I-051 | Matched |
| I-31-P-028 | Requirement: Use CSP, safe escaped rendering, anti-framing, cookie flags and dependency integrity in production. | Partially covered | Part 4.1 §4.10–4.12, §4.16; Part 9.9 CAP-X3-26 PWA | Specified in §11.9.5.13–11.9.5.15 | DEC-675, FR-V12-I-051 | Matched |
| I-31-P-029 | Acceptance OPT-TC-SEC-11: Security header check and XSS fixtures pass; private data not in public build. | Partially covered | Part 4.1 §4.10–4.12, §4.16; Part 9.9 CAP-X3-26 PWA | Specified in §11.9.5.13–11.9.5.15 | DEC-675, FR-V12-I-051 | Matched |
| I-31-P-030 | Owner: Security / privacy engineering \| BRD chapter 20 \| Website: No new website interaction; production requirement where applicable \| Admin: A089 requirement register;  | Partially covered | Part 4.1 §4.10–4.12, §4.16; Part 9.9 CAP-X3-26 PWA | Specified in §11.9.5.13–11.9.5.15 | DEC-675, FR-V12-I-051 | Matched |
| I-31-P-031 | SEC-12 · P0 · SSRF-safe egress | Partially covered | Part 4.1 §4.10–4.12, §4.16; Part 9.9 CAP-X3-26 PWA | Specified in §11.9.5.13–11.9.5.15 | DEC-675, FR-V12-I-051 | Matched |
| I-31-P-032 | Requirement: Validate scheme, allowlist hosts, resolve and recheck redirects/IPs; deny private/link-local destinations. | Partially covered | Part 4.1 §4.10–4.12, §4.16; Part 9.9 CAP-X3-26 PWA | Specified in §11.9.5.13–11.9.5.15 | DEC-675, FR-V12-I-051 | Matched |
| I-31-P-033 | Acceptance OPT-TC-SEC-12: Blocked test destination cannot be fetched even through redirects. | Partially covered | Part 4.1 §4.10–4.12, §4.16; Part 9.9 CAP-X3-26 PWA | Specified in §11.9.5.13–11.9.5.15 | DEC-675, FR-V12-I-051 | Matched |
| I-31-P-034 | Owner: Security / privacy engineering \| BRD chapter 20 \| Website: No new website interaction; production requirement where applicable \| Admin: A089 requirement register;  | Partially covered | Part 4.1 §4.10–4.12, §4.16; Part 9.9 CAP-X3-26 PWA | Specified in §11.9.5.13–11.9.5.15 | DEC-675, FR-V12-I-051 | Matched |
| I-31-P-035 | SEC-13 · P1 · Security behavior monitoring | Partially covered | Part 4.1 §4.10–4.12, §4.16; Part 9.9 CAP-X3-26 PWA | Specified in §11.9.5.13–11.9.5.15 | DEC-675, FR-V12-I-051 | Matched |
| I-31-P-036 | Requirement: Detect unusual login, export, permission changes and usage; minimize sensitive logging and triage. | Partially covered | Part 4.1 §4.10–4.12, §4.16; Part 9.9 CAP-X3-26 PWA | Specified in §11.9.5.13–11.9.5.15 | DEC-675, FR-V12-I-051 | Matched |
| I-31-P-037 | Acceptance OPT-TC-SEC-13: Suspicious fixture emits scoped alert with owner and evidence. | Partially covered | Part 4.1 §4.10–4.12, §4.16; Part 9.9 CAP-X3-26 PWA | Specified in §11.9.5.13–11.9.5.15 | DEC-675, FR-V12-I-051 | Matched |
| I-31-P-038 | Owner: Security / privacy engineering \| BRD chapter 20 \| Website: No new website interaction; production requirement where applicable \| Admin: A089 requirement register;  | Partially covered | Part 4.1 §4.10–4.12, §4.16; Part 9.9 CAP-X3-26 PWA | Specified in §11.9.5.13–11.9.5.15 | DEC-675, FR-V12-I-051 | Matched |
| I-31-P-039 | SEC-14 · P0 · Software supply-chain controls | Partially covered | Part 4.1 §4.10–4.12, §4.16; Part 9.9 CAP-X3-26 PWA | Specified in §11.9.5.13–11.9.5.15 | DEC-675, FR-V12-I-051 | Matched |
| I-31-P-040 | Requirement: Generate SBOM, scan dependencies, sign build and enforce protected releases. | Partially covered | Part 4.1 §4.10–4.12, §4.16; Part 9.9 CAP-X3-26 PWA | Specified in §11.9.5.13–11.9.5.15 | DEC-675, FR-V12-I-051 | Matched |
| I-31-P-041 | Acceptance OPT-TC-SEC-14: Unapproved vulnerable dependency or unsigned artifact blocks release. | Partially covered | Part 4.1 §4.10–4.12, §4.16; Part 9.9 CAP-X3-26 PWA | Specified in §11.9.5.13–11.9.5.15 | DEC-675, FR-V12-I-051 | Matched |
| I-31-P-042 | Owner: Security / privacy engineering \| BRD chapter 20 \| Website: No new website interaction; production requirement where applicable \| Admin: A089 requirement register;  | Partially covered | Part 4.1 §4.10–4.12, §4.16; Part 9.9 CAP-X3-26 PWA | Specified in §11.9.5.13–11.9.5.15 | DEC-675, FR-V12-I-051 | Matched |
| I-ENG-CONF-DEC-039 | V12-ENG DEC-039 existing user table / all: Resolve existing identity table and primary-key type from Django model metadata; map membership/actor FK to verified identity;  | Conflict | ID collides with blueprint DEC-039..042; content covered by Part 3.6a rows 001-003 and 010 | Namespaced "V12-ENG DEC-nnn" (DEC-665); confirmation evidence = Django introspection + two-tenant test at Sprint 0 | CONFLICT-907, DEC-665 | Matched |
| I-ENG-CONF-DEC-040 | V12-ENG DEC-040 existing role table / all: Resolve existing identity table and primary-key type from Django model metadata; map membership/actor FK to verified identity;  | Conflict | ID collides with blueprint DEC-039..042; content covered by Part 3.6a rows 001-003 and 010 | Namespaced "V12-ENG DEC-nnn" (DEC-665); confirmation evidence = Django introspection + two-tenant test at Sprint 0 | CONFLICT-907, DEC-665 | Matched |
| I-ENG-CONF-DEC-041 | V12-ENG DEC-041 existing membership table / all: Resolve existing identity table and primary-key type from Django model metadata; map membership/actor FK to verified iden | Conflict | ID collides with blueprint DEC-039..042; content covered by Part 3.6a rows 001-003 and 010 | Namespaced "V12-ENG DEC-nnn" (DEC-665); confirmation evidence = Django introspection + two-tenant test at Sprint 0 | CONFLICT-907, DEC-665 | Matched |
| I-ENG-CONF-DEC-042 | V12-ENG DEC-042 growth_embedding / vector:vector(d): Select an approved embedding model and assert vector dimensions before creating the index; use a nullable vector only | Conflict | ID collides with blueprint DEC-039..042; content covered by Part 3.6a rows 001-003 and 010 | Namespaced "V12-ENG DEC-nnn" (DEC-665); confirmation evidence = Django introspection + two-tenant test at Sprint 0 | CONFLICT-907, DEC-665, GAP-916 | Matched |

### 11.9.3.2 Appendix C / C2 table-by-table register (every non-covered column, strengthened constraint and replaced policy named)

The blueprint target is the physical table after the DEC-581 vocabulary mapping (V12 *company* = blueprint *startup*; `company_id` is the V12-facing alias of physical `startup_id`). For the 89 generic domain tables the three V12 common columns `schema_ref`, `payload`, `evidence_refs` were not covered; `status` and `version` map to blueprint `state` and `revision`/`version_no` (partially covered, °). Every policy listed was replaced by the command-split policies of DDL-V12-I §C3-13 (Part 11.9b §11.9.5.6).

| V12 table | Blueprint target | Table status | Columns not covered (° = partial) | Constraints strengthened | Policies replaced |
|---|---|---|---|---|---|
| `tenant` | ENT-001 ten_tenant | Partially covered | customer_type, data_region, contract_status | tenant_data_region_check | — |
| `organization` | new ten_organization (DEC-581) | Not covered | tenant_id, organization_id, name, name_norm | organization_tenant_id_name_norm_key | organization_tenant |
| `company` | ENT-002 ten_startup | Partially covered | registration_country | — | company_tenant |
| `division` | ENT-003 ten_business_line | Partially covered | division_id | — | division_tenant |
| `brand` | new ten_brand | Not covered | tenant_id, company_id, division_id, brand_id, name | — | brand_tenant |
| `offering` | ENT-016 cat_offering | Partially covered | brand_id, offering_type, claims_ref, price_amount | offering_currency_check | offering_tenant |
| `market` | new ten_market | Not covered | tenant_id, company_id, market_id, country, region, timezone, language, currency, jurisdiction_pack_id | — | market_tenant |
| `channel_account` | ENT-089 eng_channel_account | Partially covered | account_id, sender_alias, credential_ref, dlt_entity_id, dlt_header, number_series | channel_account_daily_cap_check | channel_account_tenant |
| `workflow_run` | ENT-162 aut_run | Partially covered | sku_id, wf_id, wf_version, business_context, input, reviewed_by, reserved_units | workflow_run_check, workflow_run_sku_id_check, workflow_run_status_check, workflow_run_tenant_id_idempotency_key_key | workflow_run_tenant |
| `workflow_step_run` | ENT-163 aut_step_run | Partially covered | step_id, step_class, prompt_version, output | workflow_step_run_check, workflow_step_run_step_class_check | workflow_step_run_tenant |
| `effect` | new aut_effect | Not covered | tenant_id, effect_id, run_id, step_id, idempotency_key, preflight_verdict, status, provider_receipt | effect_preflight_verdict_check, effect_status_check, effect_tenant_id_idempotency_key_key | effect_tenant |
| `outbox` | ENT-169 ops_outbox | Partially covered | — | — | outbox_tenant |
| `inbox` | ENT-043 int_provider_event | Partially covered | signature_ok | inbox_pkey | — |
| `audit_event` | ENT-172 ops_audit_event | Partially covered | audit_id, actor, ref, policy_version | — | audit_event_tenant |
| `portfolio_grant` | ten_membership_grant | Partially covered | portfolio_id, grant_id, dimensions | — | — |
| `fx_rate` | ENT-198 ana_fx_snapshot | Partially covered | rate_id, approved_version | fx_rate_rate_check | — |
| `jurisdiction_pack` | new gov_jurisdiction_pack | Not covered | pack_id, jurisdiction, version, status, approved_by, approved_at, effective_from, effective_to | jurisdiction_pack_jurisdiction_version_key, jurisdiction_pack_status_check | — |
| `jurisdiction_rule` | ENT-030 gov_jurisdiction_rule | Partially covered | pack_id, rule_id, effect, legal_source, interpretation_status | jurisdiction_rule_effect_check | — |
| `consent_record` | ENT-027 gov_consent | Partially covered | market, basis, notice_version, captured_at, capture_source, evidence_hash, supersedes | consent_record_status_check | consent_record_tenant |
| `suppression` | ENT-028 gov_suppression | Partially covered | — | — | suppression_tenant |
| `dsar_request` | ENT-036 gov_privacy_request | Partially covered | dsar_id, jurisdiction, identity_verified_at, legal_hold | — | dsar_request_tenant |
| `incident` | ENT-039 gov_compliance_incident | Partially covered | incident_id, aware_at, personal_data | — | — |
| `incident_notification` | new gov_incident_notification | Not covered | incident_id, authority, deadline_at, notified_at, evidence_ref | — | — |
| `ai_model` | new ai_model | Not covered | model_id, tier, provider, version, regions, data_classes, context_limit, dpa_ref, status, rollback_to | ai_model_status_check | — |
| `prompt_version` | ENT-045 ai_prompt_version | Partially covered | prompt_id, task, output_schema_ref | — | — |
| `eval_suite` | new ai_eval_suite | Not covered | suite_id, wf_id, languages, case_count, thresholds | — | — |
| `eval_run` | ENT-048 ai_eval_run | Partially covered | suite_id, prompt_id, prompt_version, metrics, run_at | — | — |
| `ai_usage_event` | ENT-050 ai_usage | Partially covered | usage_id, step_id, prompt_version | — | ai_usage_event_tenant |
| `ai_budget` | ENT-052 ai_budget | Partially covered | soft_cap_tokens, hard_cap_tokens | ai_budget_check | ai_budget_tenant |
| `growth_source` | ENT-053 intel_source | Partially covered | schema_ref, version°, status°, payload, evidence_refs | — | growth_source_tenant |
| `growth_source_policy` | ENT-054 intel_source_policy | Partially covered | schema_ref, version°, status°, payload, evidence_refs | — | growth_source_policy_tenant |
| `growth_source_record` | ENT-057 intel_source_record | Partially covered | schema_ref, version°, status°, payload, evidence_refs | — | growth_source_record_tenant |
| `growth_evidence` | ENT-059 intel_evidence | Partially covered | schema_ref, version°, status°, payload, evidence_refs | — | growth_evidence_tenant |
| `growth_competitor` | ENT-061 intel_competitor | Partially covered | schema_ref, version°, status°, payload, evidence_refs | — | growth_competitor_tenant |
| `growth_market_event` | ENT-062 intel_market_event | Partially covered | schema_ref, version°, status°, payload, evidence_refs | — | growth_market_event_tenant |
| `growth_search_plan` | ENT-055 intel_search_plan | Partially covered | schema_ref, version°, status°, payload, evidence_refs | — | growth_search_plan_tenant |
| `growth_organization` | ENT-063 intel_organization | Partially covered | schema_ref, version°, status°, payload, evidence_refs | — | growth_organization_tenant |
| `growth_signal` | ENT-067 intel_signal | Partially covered | schema_ref, version°, status°, payload, evidence_refs | — | growth_signal_tenant |
| `growth_signal_type` | ENT-066 intel_signal_type | Partially covered | schema_ref, version°, status°, payload, evidence_refs | — | growth_signal_type_tenant |
| `growth_need_evidence` | ENT-069 intel_need_evidence | Partially covered | schema_ref, version°, status°, payload, evidence_refs | — | growth_need_evidence_tenant |
| `growth_referral` | ENT-123 mkt_referral | Partially covered | schema_ref, version°, status°, payload, evidence_refs | — | growth_referral_tenant |
| `growth_contact` | ENT-074 intel_contact | Partially covered | schema_ref, version°, status°, payload, evidence_refs | — | growth_contact_tenant |
| `growth_contact_source` | ENT-076 intel_contact_source | Partially covered | schema_ref, version°, status°, payload, evidence_refs | — | growth_contact_source_tenant |
| `growth_contact_verification` | ENT-077 intel_contact_verification | Partially covered | schema_ref, version°, status°, payload, evidence_refs | — | growth_contact_verification_tenant |
| `growth_consent` | ENT-027 gov_consent | Partially covered | schema_ref, version°, status°, payload, evidence_refs | — | growth_consent_tenant |
| `growth_suppression` | ENT-028 gov_suppression | Partially covered | schema_ref, version°, status°, payload, evidence_refs | — | growth_suppression_tenant |
| `growth_need` | ENT-068 intel_need | Partially covered | schema_ref, version°, status°, payload, evidence_refs | — | growth_need_tenant |
| `growth_product` | ENT-016 cat_offering | Partially covered | schema_ref, version°, status°, payload, evidence_refs | — | growth_product_tenant |
| `growth_opportunity` | ENT-072 intel_opportunity | Partially covered | schema_ref, version°, status°, payload, evidence_refs | — | growth_opportunity_tenant |
| `growth_score_version` | ENT-073 intel_score_version | Partially covered | schema_ref, version°, status°, payload, evidence_refs | — | growth_score_version_tenant |
| `growth_activity` | ENT-088 crm_activity | Partially covered | schema_ref, version°, status°, payload, evidence_refs | — | growth_activity_tenant |
| `growth_deal` | ENT-086 crm_deal | Partially covered | schema_ref, version°, status°, payload, evidence_refs | — | growth_deal_tenant |
| `growth_stage` | ENT-084 crm_stage | Partially covered | schema_ref, version°, status°, payload, evidence_refs | — | growth_stage_tenant |
| `growth_task` | ENT-148 lcy_task | Partially covered | schema_ref, version°, status°, payload, evidence_refs | — | growth_task_tenant |
| `growth_budget` | ENT-052 ai_budget | Partially covered | schema_ref, version°, status°, payload, evidence_refs | — | growth_budget_tenant |
| `growth_message` | ENT-093 eng_message | Partially covered | schema_ref, version°, status°, payload, evidence_refs | — | growth_message_tenant |
| `growth_message_draft` | ENT-091 eng_message_draft | Partially covered | schema_ref, version°, status°, payload, evidence_refs | — | growth_message_draft_tenant |
| `growth_message_template` | ENT-090 eng_message_template | Partially covered | schema_ref, version°, status°, payload, evidence_refs | — | growth_message_template_tenant |
| `growth_outbox` | ENT-169 ops_outbox | Partially covered | schema_ref, version°, status°, payload, evidence_refs | — | growth_outbox_tenant |
| `growth_delivery_event` | ENT-094 eng_delivery_event | Partially covered | schema_ref, version°, status°, payload, evidence_refs | — | growth_delivery_event_tenant |
| `growth_thread` | ENT-092 eng_thread | Partially covered | schema_ref, version°, status°, payload, evidence_refs | — | growth_thread_tenant |
| `growth_channel_account` | ENT-089 eng_channel_account | Partially covered | schema_ref, version°, status°, payload, evidence_refs | — | growth_channel_account_tenant |
| `growth_inbound_event` | ENT-095 eng_inbound_event | Partially covered | schema_ref, version°, status°, payload, evidence_refs | — | growth_inbound_event_tenant |
| `growth_enrollment` | ENT-102 eng_enrollment | Partially covered | schema_ref, version°, status°, payload, evidence_refs | — | growth_enrollment_tenant |
| `growth_sequence` | ENT-100 eng_sequence | Partially covered | schema_ref, version°, status°, payload, evidence_refs | — | growth_sequence_tenant |
| `growth_sequence_step` | ENT-101 eng_sequence_step | Partially covered | schema_ref, version°, status°, payload, evidence_refs | — | growth_sequence_step_tenant |
| `growth_routing_rule` | ENT-098 eng_routing_rule | Partially covered | schema_ref, version°, status°, payload, evidence_refs | — | growth_routing_rule_tenant |
| `growth_workflow_execution` | ENT-162 aut_run | Partially covered | schema_ref, version°, status°, payload, evidence_refs | — | growth_workflow_execution_tenant |
| `growth_identity_link` | ENT-097 eng_identity_link | Partially covered | schema_ref, version°, status°, payload, evidence_refs | — | growth_identity_link_tenant |
| `growth_objection` | ENT-129 com_objection | Partially covered | schema_ref, version°, status°, payload, evidence_refs | — | growth_objection_tenant |
| `growth_calendar_link` | ENT-104 eng_calendar_link | Partially covered | schema_ref, version°, status°, payload, evidence_refs | — | growth_calendar_link_tenant |
| `growth_meeting` | ENT-103 eng_meeting | Partially covered | schema_ref, version°, status°, payload, evidence_refs | — | growth_meeting_tenant |
| `growth_business_event` | ENT-120 mkt_event | Partially covered | schema_ref, version°, status°, payload, evidence_refs | — | growth_business_event_tenant |
| `growth_event_attendance` | ENT-122 mkt_attendance | Partially covered | schema_ref, version°, status°, payload, evidence_refs | — | growth_event_attendance_tenant |
| `growth_event_registration` | ENT-121 mkt_registration | Partially covered | schema_ref, version°, status°, payload, evidence_refs | — | growth_event_registration_tenant |
| `growth_claim` | ENT-020 cat_claim | Partially covered | schema_ref, version°, status°, payload, evidence_refs | — | growth_claim_tenant |
| `growth_content_asset` | ENT-105 mkt_content_asset | Partially covered | schema_ref, version°, status°, payload, evidence_refs | — | growth_content_asset_tenant |
| `growth_content_version` | ENT-106 mkt_content_version | Partially covered | schema_ref, version°, status°, payload, evidence_refs | — | growth_content_version_tenant |
| `growth_approval` | ENT-034 gov_approval | Partially covered | schema_ref, version°, status°, payload, evidence_refs | — | growth_approval_tenant |
| `growth_social_post` | ENT-060 intel_social_post | Partially covered | schema_ref, version°, status°, payload, evidence_refs | — | growth_social_post_tenant |
| `growth_social_publication` | ENT-107 mkt_social_publication | Partially covered | schema_ref, version°, status°, payload, evidence_refs | — | growth_social_publication_tenant |
| `growth_keyword` | ENT-108 mkt_keyword | Partially covered | schema_ref, version°, status°, payload, evidence_refs | — | growth_keyword_tenant |
| `growth_page_metric` | ENT-110 mkt_page_metric | Partially covered | schema_ref, version°, status°, payload, evidence_refs | — | growth_page_metric_tenant |
| `growth_seo_issue` | ENT-109 mkt_seo_issue | Partially covered | schema_ref, version°, status°, payload, evidence_refs | — | growth_seo_issue_tenant |
| `growth_landing_page` | ENT-111 mkt_landing_page | Partially covered | schema_ref, version°, status°, payload, evidence_refs | — | growth_landing_page_tenant |
| `growth_audience` | ENT-117 mkt_audience | Partially covered | schema_ref, version°, status°, payload, evidence_refs | — | growth_audience_tenant |
| `growth_campaign` | ENT-115 mkt_campaign | Partially covered | schema_ref, version°, status°, payload, evidence_refs | — | growth_campaign_tenant |
| `growth_campaign_version` | ENT-116 mkt_campaign_version | Partially covered | schema_ref, version°, status°, payload, evidence_refs | — | growth_campaign_version_tenant |
| `growth_ad_campaign` | ENT-118 mkt_ad_campaign | Partially covered | schema_ref, version°, status°, payload, evidence_refs | — | growth_ad_campaign_tenant |
| `growth_ad_spend_event` | ENT-119 mkt_spend_event | Partially covered | schema_ref, version°, status°, payload, evidence_refs | — | growth_ad_spend_event_tenant |
| `growth_attribution_event` | ENT-124 mkt_attribution_event | Partially covered | schema_ref, version°, status°, payload, evidence_refs | — | growth_attribution_event_tenant |
| `growth_form` | ENT-080 crm_form | Partially covered | schema_ref, version°, status°, payload, evidence_refs | — | growth_form_tenant |
| `growth_lead` | ENT-079 crm_lead | Partially covered | schema_ref, version°, status°, payload, evidence_refs | — | growth_lead_tenant |
| `growth_proposal` | ENT-125 com_proposal | Partially covered | schema_ref, version°, status°, payload, evidence_refs | — | growth_proposal_tenant |
| `growth_proposal_version` | ENT-126 com_proposal_version | Partially covered | schema_ref, version°, status°, payload, evidence_refs | — | growth_proposal_version_tenant |
| `growth_quote` | ENT-127 com_quote | Partially covered | schema_ref, version°, status°, payload, evidence_refs | — | growth_quote_tenant |
| `growth_quote_line` | ENT-128 com_quote_line | Partially covered | schema_ref, version°, status°, payload, evidence_refs | — | growth_quote_line_tenant |
| `growth_negotiation` | ENT-130 com_negotiation | Partially covered | schema_ref, version°, status°, payload, evidence_refs | — | growth_negotiation_tenant |
| `growth_contract` | ENT-131 com_contract | Partially covered | schema_ref, version°, status°, payload, evidence_refs | — | growth_contract_tenant |
| `growth_integration_deal` | ENT-156 lcy_integration_deal | Partially covered | schema_ref, version°, status°, payload, evidence_refs | — | growth_integration_deal_tenant |
| `sales_bid` | ENT-133 com_bid | Partially covered | schema_ref, version°, status°, payload, evidence_refs | — | sales_bid_tenant |
| `growth_invoice` | ENT-140 com_invoice | Partially covered | schema_ref, version°, status°, payload, evidence_refs | — | growth_invoice_tenant |
| `growth_payment` | ENT-142 com_payment | Partially covered | schema_ref, version°, status°, payload, evidence_refs | — | growth_payment_tenant |
| `sales_fulfillment` | ENT-137 com_fulfillment_event | Partially covered | schema_ref, version°, status°, payload, evidence_refs | — | sales_fulfillment_tenant |
| `sales_order` | ENT-135 com_order | Partially covered | schema_ref, version°, status°, payload, evidence_refs | — | sales_order_tenant |
| `sales_order_line` | ENT-136 com_order_line | Partially covered | schema_ref, version°, status°, payload, evidence_refs | — | sales_order_line_tenant |
| `growth_onboarding` | ENT-147 lcy_onboarding | Partially covered | schema_ref, version°, status°, payload, evidence_refs | — | growth_onboarding_tenant |
| `growth_deployment` | ENT-155 lcy_deployment | Partially covered | schema_ref, version°, status°, payload, evidence_refs | — | growth_deployment_tenant |
| `growth_partner` | ENT-153 lcy_partner | Partially covered | schema_ref, version°, status°, payload, evidence_refs | — | growth_partner_tenant |
| `growth_pilot` | ENT-154 lcy_pilot | Partially covered | schema_ref, version°, status°, payload, evidence_refs | — | growth_pilot_tenant |
| `growth_renewal` | ENT-150 lcy_renewal | Partially covered | schema_ref, version°, status°, payload, evidence_refs | — | growth_renewal_tenant |
| `growth_feedback` | ENT-049 ai_feedback | Partially covered | schema_ref, version°, status°, payload, evidence_refs | — | growth_feedback_tenant |
| `growth_metric_snapshot` | ENT-192 ana_metric_snapshot | Partially covered | schema_ref, version°, status°, payload, evidence_refs | — | growth_metric_snapshot_tenant |
| `growth_forecast` | ENT-196 ana_forecast | Partially covered | schema_ref, version°, status°, payload, evidence_refs | — | growth_forecast_tenant |
| `growth_stage_metric` | ENT-197 ana_stage_metric | Partially covered | schema_ref, version°, status°, payload, evidence_refs | — | growth_stage_metric_tenant |
| `growth_document` | ENT-024 cat_document | Partially covered | schema_ref, version°, status°, payload, evidence_refs | — | growth_document_tenant |
| `growth_document_chunk` | ENT-025 cat_chunk | Partially covered | schema_ref, version°, status°, payload, evidence_refs | — | growth_document_chunk_tenant |
| `growth_embedding` | ENT-026 cat_embedding | Partially covered | schema_ref, version°, status°, payload, evidence_refs | — | growth_embedding_tenant |
| `identity_provider` | new sec_identity_provider | Not covered | tenant_id, protocol, sso_url, issuer, domain, domain_verified, breakglass_email, enforced, mfa_policy, max_session_hours, idle_minutes | identity_provider_check, identity_provider_idle_minutes_check, identity_provider_max_session_hours_check, identity_provider_protocol_check, identity_provider_sso_url_check | identity_provider_tenant |
| `scim_token` | new sec_scim_token | Not covered | tenant_id, token_id, token_hash, prefix, created_at, revoked_at | — | scim_token_tenant |
| `custom_role` | ENT-007 ten_role | Partially covered | role_id | custom_role_tenant_id_name_key | custom_role_tenant |
| `role_permission` | new ten_role_permission | Not covered | tenant_id, role_id, permission | role_permission_pkey, role_permission_role_id_fkey | role_permission_tenant |
| `sod_conflict` | new ref_sod_conflict | Not covered | permission_a, permission_b | — | — |
| `api_key` | saas_api_credential (Part 9.9) | Partially covered | key_id, prefix, last4, key_hash, ip_allowlist | api_key_scopes_check | api_key_tenant |
| `webhook_endpoint` | saas_webhook_subscription (Part 9.9) | Partially covered | endpoint_id, events, secret_ref | webhook_endpoint_events_check, webhook_endpoint_url_check | webhook_endpoint_tenant |
| `webhook_delivery` | saas_webhook_delivery (Part 9.9) | Partially covered | delivery_id, endpoint_id, event, status_code | webhook_delivery_attempt_check, webhook_delivery_endpoint_id_fkey | webhook_delivery_tenant |
| `audit_sink` | new ops_audit_sink | Not covered | tenant_id, sink_id, kind, endpoint, format, retention_years | audit_sink_endpoint_check, audit_sink_format_check, audit_sink_kind_check, audit_sink_retention_years_check | audit_sink_tenant |
| `export_job` | ENT-189 saas_export_job | Partially covered | export_id, manifest_hash | export_job_check, export_job_format_check, export_job_status_check | export_job_tenant |
| `tenant_key_config` | ten_tenant_key (Part 9.9) | Partially covered | kms_key_ref, rotation_days | tenant_key_config_check, tenant_key_config_mode_check, tenant_key_config_rotation_days_check | tenant_key_config_tenant |
| `sandbox_environment` | new saas_sandbox_environment | Not covered | tenant_id, sandbox_id, name, copies_configuration, contains_personal_data | sandbox_environment_contains_personal_data_check | sandbox_environment_tenant |
| `config_promotion` | new aut_config_promotion | Not covered | tenant_id, promotion_id, sandbox_id, requested_by, approved_by, status | config_promotion_check, config_promotion_sandbox_id_fkey | config_promotion_tenant |
| `connector_installation` | ENT-040 int_integration | Partially covered | installation_id, connector_id, credential_ref, legal_review_ref, security_review_ref | connector_installation_check, connector_installation_environment_check | connector_installation_tenant |
| `security_finding` | new sec_security_finding | Not covered | finding_id, title, severity, found_at, due_at, closed_at, evidence_ref | security_finding_check, security_finding_check1, security_finding_severity_check | — |
| `ops_incident` | ENT-176 ops_incident | Partially covered | incident_id, declared_at, status_message | ops_incident_severity_check, ops_incident_status_check | — |
| `tax_rule` | ENT-022 cat_tax_profile | Partially covered | rule_id, jurisdiction, rate_percent, needs_rate_input | tax_rule_rate_percent_check | — |
| `invoice` | ENT-184 saas_service_invoice | Partially covered | number, net_minor, tax_minor, total_minor, tax_rule_id | invoice_check, invoice_net_minor_check, invoice_number_key, invoice_tax_minor_check | invoice_tenant |
| `locale_bundle` | new ref_locale_bundle | Not covered | locale, direction, coverage_percent, reviewed_by | locale_bundle_direction_check | — |

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

| Domain schema (service) | Fields with a typed blueprint column (Covered) | Fields carried in validated payload (Partially covered → Matched by DEC-661) |
|---|---|---|
| market_signal SM-SVC-01 | industry, source_ids, evidence_ids, observed_at | region, question, signal_type, observation |
| opportunity SM-SVC-02 | offering_id, source_ids, evidence_ids | target_profile, region, organization_ref, need, deadline, fit_score |
| contact SM-SVC-03 | purpose, verification_state, evidence_ids | organization_ref, role_criteria, contact_refs, contact_ref, role, eligibility_expiry |
| qualification SM-SVC-04 | score, reason_codes | lead_ref, offering_refs, scoring_policy_ref, assignment_policy_ref, match_refs, owner_ref, review_state |
| crm_relationship SM-SVC-05 | relationship_ref | account_ref, contact_refs, stage, interaction_refs, stage, owner_ref, next_task_ref, version |
| email_message SM-SVC-06 | provider_ref | contact_ref, sender_ref, claim_refs, message_ref, draft_ref, dispatch_ref, delivery_state, suppression_state |
| whatsapp_message SM-SVC-07 | template_ref | contact_ref, sender_ref, consent_ref, eligibility_state, dispatch_ref, thread_ref, delivery_state |
| journey SM-SVC-08 | relationship_ref, scheduled_at, stop_reason | sequence_ref, consent_refs, event_refs, next_action_ref, journey_state |
| conversation SM-SVC-09 | language, intent, response_ref, confidence | thread_ref, inbound_event_ref, knowledge_refs, handover_ref |
| meeting SM-SVC-10 | — | participant_refs, calendar_ref, availability, agenda_ref, slot_ref, booking_ref, agenda_ref, action_refs |
| content SM-SVC-11 | revision | brand_ref, brief_ref, claim_refs, asset_refs, content_ref, claim_check_state, review_state |
| social_post SM-SVC-12 | schedule, source_ids, status | account_ref, content_ref, publication_ref, metric_refs, mention_refs |
| search_visibility SM-SVC-13 | observed_at, evidence_ids | domain_ref, page_refs, keyword_refs, metric_refs, visibility_report_ref, issue_refs |
| ad_campaign SM-SVC-14 | objective, currency, provider_ref | ad_account_ref, campaign_ref, budget_minor, campaign_version, activation_state, spend_minor, experiment_ref |
| lead_intake SM-SVC-15 | submission_ref, attribution_ref | client_property_ref, form_schema_ref, consent_ref, lead_ref, validation_state, issue_refs |
| event_registration SM-SVC-16 | event_ref | registration_ref, partner_ref, consent_ref, registration_state, attendance_state, referral_ref, journey_ref |
| quotation SM-SVC-17 | currency, revision | opportunity_ref, price_revision_ref, line_items, quote_ref, total_minor, tax_minor, approval_state |
| agreement SM-SVC-18 | template_ref, revision | opportunity_ref, terms_ref, signatory_refs, agreement_ref, deviation_refs, signature_state, obligation_refs |
| tender SM-SVC-19 | tender_ref, submission_ref | source_ref, capability_refs, deadline, bid_ref, eligibility_state, missing_evidence_refs |
| sales_order SM-SVC-20 | — | quote_ref, order_lines, inventory_ref, delivery_refs, order_ref, milestone_refs, fulfillment_state, exception_refs |
| receivable SM-SVC-21 | currency | invoice_ref, payment_ref, amount_minor, allocation_ref, balance_minor, discrepancy_refs, reconciliation_state |
| onboarding SM-SVC-22 | template_ref, readiness_state | customer_ref, agreement_ref, milestone_refs, plan_ref, task_refs, handover_ref |
| retention SM-SVC-23 | risk_score, reason_codes | customer_ref, renewal_ref, feedback_refs, consent_ref, renewal_task_ref, recommendation_ref |
| revenue_analysis SM-SVC-24 | period, confidence | outcome_refs, attribution_model_ref, assumption_refs, report_ref, attributed_minor, forecast_minor, error_metric |
| knowledge SM-SVC-25 | taxonomy_ref, revision | document_ref, claim_refs, document_version, claim_version_refs, review_state, correction_refs |
| voice_session SM-SVC-26 | — | call_ref, contact_ref, script_ref, recording_permission_ref, disposition, transcript_ref, booking_ref, call_event_ref |
| creative_asset SM-SVC-27 | revision, rights_state | brief_ref, brand_ref, asset_rights_refs, target_language, asset_ref, qa_state |
| agent_transaction SM-SVC-28 | — | agent_ref, mandate_ref, offering_ref, order_ref, quote_ref, mandate_state, transaction_ref, reconciliation_state |
| account_plan SM-SVC-29 | — | account_ref, icp_ref, role_evidence_refs, engagement_refs, plan_ref, buying_group_ref, journey_ref, progress_report_ref |
| experiment SM-SVC-30 | — | hypothesis_ref, variant_refs, allocation_policy_ref, event_refs, experiment_ref, allocation_ref, lift, interval, decision_state |
| marketplace_listing SM-SVC-31 | — | marketplace_ref, sku_ref, inventory_ref, event_refs, listing_ref, inventory_version, order_event_ref, net_minor |
| partner_deal SM-SVC-32 | — | partner_ref, territory_ref, material_refs, deal_ref, shortlist_ref, access_grant_ref, registration_ref, performance_ref |
| support_case SM-SVC-33 | severity | customer_ref, enquiry_ref, sla_policy_ref, knowledge_refs, case_ref, queue_ref, resolution_ref, sla_state |
| product_usage SM-SVC-34 | — | account_ref, event_refs, feature_refs, plan_ref, activation_state, usage_report_ref, expansion_ref, recommendation_ref |
| reputation SM-SVC-35 | source_ids, response_ref | brand_ref, review_refs, threshold_ref, review_queue_ref, incident_ref, improvement_ref |
| coaching SM-SVC-36 | — | learner_ref, playbook_ref, scenario_ref, authorized_session_ref, playbook_revision, practice_report_ref, feedback_ref, training_plan_ref |
| pricing SM-SVC-37 | — | offer_ref, cost_revision_ref, price_bounds_ref, history_refs, margin_minor, scenario_ref, experiment_ref, exception_ref |
| sms_message SM-SVC-38 | template_ref | sender_ref, recipient_refs, consent_refs, eligibility_state, dispatch_ref, delivery_state, suppression_state |
| procurement SM-SVC-39 | — | requirement_ref, supplier_refs, quote_refs, budget_ref, shortlist_ref, comparison_ref, purchase_order_ref, exception_refs |

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
| i | V12 core/enterprise tables already in the blueprint (same entity, V12 columns added) | 31 | §11.9.4.2 "Partially covered" |
| j | V12 core/enterprise tables new to the blueprint | 17 | §11.9.4.2 "new" |
| k | V6 / V5 / V4 entities with no Appendix C table, created in DDL-V12-I | 13 | `company_operating_country`, `offering_market`, `channel_account_market`, `configuration_revision`, `workflow_configuration`, `business_event`, `metric_definition`, `metric_aggregate`, `experiment`, `feedback_case`, `sli_sample`, `customer_value`, `journey_event` |
| l | Supporting tables created in DDL-V12-I | 5 | `user_role_assignment`, `tenant_data_key`, `domain_schema_registry`, `domain_record_version`, `usage_reservation` |
| m | **Blueprint logical entities after this batch** | **238** | 203 (a + b) + 17 (j) + 13 (k) + 5 (l). Final ENT numbers ENT-204…238 to be assigned by the coordinator; until then the V12 table name is the identifier |

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
| `outbox` (C) | `ops_outbox` | ENT-169 | S | F | Partial | `company_id`, `dedup_key`, `correlation_id`, `attempts`, `next_attempt_at` | Dedup unique; partial pending index |
| `inbox` (C) | `int_provider_event_key` | ENT-043 | T | A | Partial | `provider_account`, `signature_ok`, `payload_ref`, `processed_at` | Key = provider + provider account + event; unsigned rows rejected |
| `audit_event` (C) | `ops_audit_event` | ENT-172 | X | A | Partial | `company_id`, `correlation_id`, `object_type`, `payload_redacted`, `schema_version`, `prev_hash`, `row_hash` | Insert only via `fn_append_audit()`; hash chain (SEC-06) |
| `portfolio_grant` (C) | `ten_portfolio_grant` (generalizes `ten_membership_grant`) | ENT-008 association | T | M | Partial | all | No wildcard; expiry mandatory; revocation |
| `fx_rate` (C) | `ana_fx_snapshot` | ENT-198 | P | V | Partial | `source`, `approved_version` | Positive rate; base ≠ quote; unique version |
| `jurisdiction_pack` (C) | `gov_jurisdiction_pack` | New | P | V | Not covered | all | Approved pack needs approver, date, effective window |
| `jurisdiction_rule` (C) | `gov_jurisdiction_rule` | ENT-030 | P | V | Partial | `pack_id`, `effect`, `legal_source`, `interpretation_status` | Effect ALLOW/HOLD/REVIEW/INFO |
| `consent_record` (C) | `gov_consent` | ENT-027 | S | A | Partial | `basis`, `notice_version`, `capture_source`, `evidence_hash`, `supersedes` | Append-only; contact FK; SHA-256 evidence |
| `suppression` (C) | `gov_suppression` | ENT-028 | T | A | Partial | `reason` vocabulary | Kept after erasure (no contact FK by design) |
| `dsar_request` (C) | `gov_privacy_request` | ENT-036 | T | M | Partial | `jurisdiction`, `legal_hold`, `evidence_ref` | Identity verified and evidence before Completed |
| `incident` (C) | `gov_compliance_incident` | ENT-039 | T / platform | M | Partial | `aware_at`, `personal_data` | Awareness clock drives notifications |
| `incident_notification` (C) | `gov_incident_notification` | New | P | A (no delete) | Not covered | all | CERT-In ≤ 6 h; GDPR ≤ 72 h; DPDP Board ≤ 72 h (verify) |
| `ai_model` (C) | `ai_model` | New (registry, was configuration in Part 7) | P | V | Not covered | all | Tier vocabulary; Tier 2 only Public/Internal-non-personal |
| `prompt_version` (C) | `ai_prompt_version` | ENT-045 | X | V | Partial | `template_hash`, `output_schema_ref` | Status vocabulary; SHA-256 hash |
| `eval_suite` (C) | `ai_eval_suite` | New | P | V | Not covered | all | Positive case count; thresholds JSON |
| `eval_run` (C) | `ai_eval_run` | ENT-048 | P | A | Partial | `denominator`, `metrics` | Append-only |
| `ai_usage_event` (C) | `ai_usage` | ENT-050 | S | A | Partial | `cached_tokens`, `latency_ms`, `outcome` | Outcome vocabulary; non-negative counters |
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
| `ops_incident` (C2) | `ops_incident` | ENT-176 | P | M | Partial | `status_message` | SEV1–SEV4; status vocabulary |
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

| # | V12 domain table | Blueprint ENT | Blueprint table | Scope / Imm. | Workflows cited in Appendix C (first 10 as printed) |
|---|---|---|---|---|---|
| 1 | `growth_source` | ENT-053 | `intel_source` | S / M | 01-WF01, 01-WF02, 01-WF03, 01-WF04, 02-WF01, 02-WF02, 02-WF03, 02-WF04, 12-WF01, 12-WF02 (list truncated in source) |
| 2 | `growth_source_policy` | ENT-054 | `intel_source_policy` | S / V | 01-WF01, 01-WF02, 01-WF03, 01-WF04, 02-WF01, 02-WF02, 02-WF03, 02-WF04, 12-WF01, 12-WF02 (list truncated in source) |
| 3 | `growth_source_record` | ENT-057 | `intel_source_record` | S / M | 01-WF01, 01-WF02, 01-WF03, 01-WF04, 02-WF01, 02-WF02, 02-WF03, 02-WF04, 12-WF01, 12-WF02 (list truncated in source) |
| 4 | `growth_evidence` | ENT-059 | `intel_evidence` | S / F | 01-WF01, 01-WF02, 01-WF03, 01-WF04, 02-WF01, 02-WF02, 02-WF03, 02-WF04, 19-WF01, 19-WF02 (list truncated in source) |
| 5 | `growth_competitor` | ENT-061 | `intel_competitor` | S / M | 01-WF01, 01-WF02, 01-WF03, 01-WF04 |
| 6 | `growth_market_event` | ENT-062 | `intel_market_event` | S / M | 01-WF01, 01-WF02, 01-WF03, 01-WF04 |
| 7 | `growth_search_plan` | ENT-055 | `intel_search_plan` | S / V | 02-WF01, 02-WF02, 02-WF03, 02-WF04 |
| 8 | `growth_organization` | ENT-063 | `intel_organization` | S / M | 02-WF01, 02-WF02, 02-WF03, 02-WF04, 03-WF01, 03-WF02, 03-WF03, 03-WF04 |
| 9 | `growth_signal` | ENT-067 | `intel_signal` | S / M | 02-WF01, 02-WF02, 02-WF03, 02-WF04, 12-WF01, 12-WF02, 12-WF03, 12-WF04 |
| 10 | `growth_signal_type` | ENT-066 | `intel_signal_type` | X / M | 02-WF01, 02-WF02, 02-WF03, 02-WF04 |
| 11 | `growth_need_evidence` | ENT-069 | `intel_need_evidence` | S / A | 02-WF01, 02-WF02, 02-WF03, 02-WF04, 04-WF01, 04-WF02, 04-WF03, 04-WF04 |
| 12 | `growth_referral` | ENT-123 | `mkt_referral` | S / M | 02-WF01, 02-WF02, 02-WF03, 02-WF04, 16-WF01, 16-WF02, 16-WF03, 16-WF04, 32-WF01, 32-WF02 (list truncated in source) |
| 13 | `growth_contact` | ENT-074 | `intel_contact` | S / M | 03-WF01, 03-WF02, 03-WF03, 03-WF04, 29-WF01, 29-WF02, 29-WF03, 29-WF04 |
| 14 | `growth_contact_source` | ENT-076 | `intel_contact_source` | S / A | 03-WF01, 03-WF02, 03-WF03, 03-WF04, 29-WF01, 29-WF02, 29-WF03, 29-WF04 |
| 15 | `growth_contact_verification` | ENT-077 | `intel_contact_verification` | S / A | 03-WF01, 03-WF02, 03-WF03, 03-WF04, 29-WF01, 29-WF02, 29-WF03, 29-WF04 |
| 16 | `growth_consent` | ENT-027 | `gov_consent` | S / A | 03-WF01, 03-WF02, 03-WF03, 03-WF04, 06-WF01, 06-WF02, 06-WF03, 06-WF04, 07-WF01, 07-WF02 (list truncated in source) |
| 17 | `growth_suppression` | ENT-028 | `gov_suppression` | T / A | 03-WF01, 03-WF02, 03-WF03, 03-WF04, 06-WF01, 06-WF02, 06-WF03, 06-WF04, 07-WF01, 07-WF02 (list truncated in source) |
| 18 | `growth_need` | ENT-068 | `intel_need` | S / M | 04-WF01, 04-WF02, 04-WF03, 04-WF04 |
| 19 | `growth_product` | ENT-016 | `cat_offering` | S / M | 04-WF01, 04-WF02, 04-WF03, 04-WF04, 25-WF01, 25-WF02, 25-WF03, 25-WF04, 28-WF01, 28-WF02 (list truncated in source) |
| 20 | `growth_opportunity` | ENT-072 | `intel_opportunity` | S / M | 04-WF01, 04-WF02, 04-WF03, 04-WF04, 05-WF01, 05-WF02, 05-WF03, 05-WF04, 19-WF01, 19-WF02 (list truncated in source) |
| 21 | `growth_score_version` | ENT-073 | `intel_score_version` | S / A | 04-WF01, 04-WF02, 04-WF03, 04-WF04 |
| 22 | `growth_activity` | ENT-088 | `crm_activity` | S / A | 05-WF01, 05-WF02, 05-WF03, 05-WF04, 09-WF01, 09-WF02, 09-WF03, 09-WF04, 26-WF01, 26-WF02 (list truncated in source) |
| 23 | `growth_deal` | ENT-086 | `crm_deal` | S / M | 05-WF01, 05-WF02, 05-WF03, 05-WF04, 18-WF01, 18-WF02, 18-WF03, 18-WF04, 20-WF01, 20-WF02 (list truncated in source) |
| 24 | `growth_stage` | ENT-084 | `crm_stage` | S / V | 05-WF01, 05-WF02, 05-WF03, 05-WF04, 29-WF01, 29-WF02, 29-WF03, 29-WF04 |
| 25 | `growth_task` | ENT-148 | `lcy_task` | S / M | 05-WF01, 05-WF02, 05-WF03, 05-WF04, 08-WF01, 08-WF02, 08-WF03, 08-WF04, 19-WF01, 19-WF02 (list truncated in source) |
| 26 | `growth_budget` | ENT-052 | `ai_budget` | X / V | 06-WF01, 06-WF02, 06-WF03, 06-WF04, 14-WF01, 14-WF02, 14-WF03, 14-WF04, 30-WF01, 30-WF02 (list truncated in source) |
| 27 | `growth_message` | ENT-093 | `eng_message` | S / F | 06-WF01, 06-WF02, 06-WF03, 06-WF04, 07-WF01, 07-WF02, 07-WF03, 07-WF04, 09-WF01, 09-WF02 (list truncated in source) |
| 28 | `growth_message_draft` | ENT-091 | `eng_message_draft` | S / M | 06-WF01, 06-WF02, 06-WF03, 06-WF04, 07-WF01, 07-WF02, 07-WF03, 07-WF04, 09-WF01, 09-WF02 (list truncated in source) |
| 29 | `growth_message_template` | ENT-090 | `eng_message_template` | S / V | 06-WF01, 06-WF02, 06-WF03, 06-WF04, 07-WF01, 07-WF02, 07-WF03, 07-WF04, 09-WF01, 09-WF02 (list truncated in source) |
| 30 | `growth_outbox` | ENT-169 | `ops_outbox` | S / F | 06-WF01, 06-WF02, 06-WF03, 06-WF04 |
| 31 | `growth_delivery_event` | ENT-094 | `eng_delivery_event` | S / A | 06-WF01, 06-WF02, 06-WF03, 06-WF04, 07-WF01, 07-WF02, 07-WF03, 07-WF04 |
| 32 | `growth_thread` | ENT-092 | `eng_thread` | S / M | 07-WF01, 07-WF02, 07-WF03, 07-WF04, 08-WF01, 08-WF02, 08-WF03, 08-WF04, 09-WF01, 09-WF02 (list truncated in source) |
| 33 | `growth_channel_account` | ENT-089 | `eng_channel_account` | S / M | 07-WF01, 07-WF02, 07-WF03, 07-WF04, 12-WF01, 12-WF02, 12-WF03, 12-WF04, 27-WF01, 27-WF02 (list truncated in source) |
| 34 | `growth_inbound_event` | ENT-095 | `eng_inbound_event` | S / A | 07-WF01, 07-WF02, 07-WF03, 07-WF04, 10-WF01, 10-WF02, 10-WF03, 10-WF04, 16-WF01, 16-WF02 (list truncated in source) |
| 35 | `growth_enrollment` | ENT-102 | `eng_enrollment` | S / M | 08-WF01, 08-WF02, 08-WF03, 08-WF04, 29-WF01, 29-WF02, 29-WF03, 29-WF04 |
| 36 | `growth_sequence` | ENT-100 | `eng_sequence` | S / V | 08-WF01, 08-WF02, 08-WF03, 08-WF04, 29-WF01, 29-WF02, 29-WF03, 29-WF04 |
| 37 | `growth_sequence_step` | ENT-101 | `eng_sequence_step` | S / V | 08-WF01, 08-WF02, 08-WF03, 08-WF04, 29-WF01, 29-WF02, 29-WF03, 29-WF04 |
| 38 | `growth_routing_rule` | ENT-098 | `eng_routing_rule` | S / V | 08-WF01, 08-WF02, 08-WF03, 08-WF04, 09-WF01, 09-WF02, 09-WF03, 09-WF04, 26-WF01, 26-WF02 (list truncated in source) |
| 39 | `growth_workflow_execution` | ENT-162 | `aut_run` | S / M | 08-WF01, 08-WF02, 08-WF03, 08-WF04 |
| 40 | `growth_identity_link` | ENT-097 | `eng_identity_link` | S / M | 09-WF01, 09-WF02, 09-WF03, 09-WF04, 38-WF01, 38-WF02, 38-WF03, 38-WF04 |
| 41 | `growth_objection` | ENT-129 | `com_objection` | S / M | 09-WF01, 09-WF02, 09-WF03, 09-WF04, 18-WF01, 18-WF02, 18-WF03, 18-WF04, 36-WF01, 36-WF02 (list truncated in source) |
| 42 | `growth_calendar_link` | ENT-104 | `eng_calendar_link` | S / M | 10-WF01, 10-WF02, 10-WF03, 10-WF04, 26-WF01, 26-WF02, 26-WF03, 26-WF04, 36-WF01, 36-WF02 (list truncated in source) |
| 43 | `growth_meeting` | ENT-103 | `eng_meeting` | S / M | 10-WF01, 10-WF02, 10-WF03, 10-WF04, 26-WF01, 26-WF02, 26-WF03, 26-WF04, 36-WF01, 36-WF02 (list truncated in source) |
| 44 | `growth_business_event` | ENT-120 | `mkt_event` | S / M | 10-WF01, 10-WF02, 10-WF03, 10-WF04, 16-WF01, 16-WF02, 16-WF03, 16-WF04 |
| 45 | `growth_event_attendance` | ENT-122 | `mkt_attendance` | S / A | 10-WF01, 10-WF02, 10-WF03, 10-WF04, 16-WF01, 16-WF02, 16-WF03, 16-WF04 |
| 46 | `growth_event_registration` | ENT-121 | `mkt_registration` | S / M | 10-WF01, 10-WF02, 10-WF03, 10-WF04, 16-WF01, 16-WF02, 16-WF03, 16-WF04 |
| 47 | `growth_claim` | ENT-020 | `cat_claim` | S / V | 11-WF01, 11-WF02, 11-WF03, 11-WF04, 25-WF01, 25-WF02, 25-WF03, 25-WF04, 28-WF01, 28-WF02 (list truncated in source) |
| 48 | `growth_content_asset` | ENT-105 | `mkt_content_asset` | S / M | 11-WF01, 11-WF02, 11-WF03, 11-WF04, 12-WF01, 12-WF02, 12-WF03, 12-WF04, 27-WF01, 27-WF02 (list truncated in source) |
| 49 | `growth_content_version` | ENT-106 | `mkt_content_version` | S / V | 11-WF01, 11-WF02, 11-WF03, 11-WF04, 12-WF01, 12-WF02, 12-WF03, 12-WF04, 13-WF01, 13-WF02 (list truncated in source) |
| 50 | `growth_approval` | ENT-034 | `gov_approval` | S / A | 11-WF01, 11-WF02, 11-WF03, 11-WF04, 13-WF01, 13-WF02, 13-WF03, 13-WF04, 14-WF01, 14-WF02 (list truncated in source) |
| 51 | `growth_social_post` | ENT-060 | `intel_social_post` | S / M | 12-WF01, 12-WF02, 12-WF03, 12-WF04, 35-WF01, 35-WF02, 35-WF03, 35-WF04 |
| 52 | `growth_social_publication` | ENT-107 | `mkt_social_publication` | S / F | 12-WF01, 12-WF02, 12-WF03, 12-WF04, 27-WF01, 27-WF02, 27-WF03, 27-WF04 |
| 53 | `growth_keyword` | ENT-108 | `mkt_keyword` | S / M | 13-WF01, 13-WF02, 13-WF03, 13-WF04 |
| 54 | `growth_page_metric` | ENT-110 | `mkt_page_metric` | S / A | 13-WF01, 13-WF02, 13-WF03, 13-WF04 |
| 55 | `growth_seo_issue` | ENT-109 | `mkt_seo_issue` | S / M | 13-WF01, 13-WF02, 13-WF03, 13-WF04 |
| 56 | `growth_landing_page` | ENT-111 | `mkt_landing_page` | S / M | 13-WF01, 13-WF02, 13-WF03, 13-WF04 |
| 57 | `growth_audience` | ENT-117 | `mkt_audience` | S / V | 14-WF01, 14-WF02, 14-WF03, 14-WF04, 30-WF01, 30-WF02, 30-WF03, 30-WF04 |
| 58 | `growth_campaign` | ENT-115 | `mkt_campaign` | S / M | 14-WF01, 14-WF02, 14-WF03, 14-WF04, 30-WF01, 30-WF02, 30-WF03, 30-WF04 |
| 59 | `growth_campaign_version` | ENT-116 | `mkt_campaign_version` | S / V | 14-WF01, 14-WF02, 14-WF03, 14-WF04, 30-WF01, 30-WF02, 30-WF03, 30-WF04 |
| 60 | `growth_ad_campaign` | ENT-118 | `mkt_ad_campaign` | S / M | 14-WF01, 14-WF02, 14-WF03, 14-WF04 |
| 61 | `growth_ad_spend_event` | ENT-119 | `mkt_spend_event` | S / A | 14-WF01, 14-WF02, 14-WF03, 14-WF04 |
| 62 | `growth_attribution_event` | ENT-124 | `mkt_attribution_event` | S / A | 14-WF01, 14-WF02, 14-WF03, 14-WF04, 24-WF01, 24-WF02, 24-WF03, 24-WF04, 30-WF01, 30-WF02 (list truncated in source) |
| 63 | `growth_form` | ENT-080 | `crm_form` | S / M | 15-WF01, 15-WF02, 15-WF03, 15-WF04 |
| 64 | `growth_lead` | ENT-079 | `crm_lead` | S / M | 16-WF01, 16-WF02, 16-WF03, 16-WF04 |
| 65 | `growth_proposal` | ENT-125 | `com_proposal` | S / M | 17-WF01, 17-WF02, 17-WF03, 17-WF04, 19-WF01, 19-WF02, 19-WF03, 19-WF04 |
| 66 | `growth_proposal_version` | ENT-126 | `com_proposal_version` | S / V | 17-WF01, 17-WF02, 17-WF03, 17-WF04, 19-WF01, 19-WF02, 19-WF03, 19-WF04 |
| 67 | `growth_quote` | ENT-127 | `com_quote` | S / F | 17-WF01, 17-WF02, 17-WF03, 17-WF04, 20-WF01, 20-WF02, 20-WF03, 20-WF04, 28-WF01, 28-WF02 (list truncated in source) |
| 68 | `growth_quote_line` | ENT-128 | `com_quote_line` | S / F | 17-WF01, 17-WF02, 17-WF03, 17-WF04, 20-WF01, 20-WF02, 20-WF03, 20-WF04, 28-WF01, 28-WF02 (list truncated in source) |
| 69 | `growth_negotiation` | ENT-130 | `com_negotiation` | S / M | 18-WF01, 18-WF02, 18-WF03, 18-WF04, 36-WF01, 36-WF02, 36-WF03, 36-WF04 |
| 70 | `growth_contract` | ENT-131 | `com_contract` | S / F | 18-WF01, 18-WF02, 18-WF03, 18-WF04 |
| 71 | `growth_integration_deal` | ENT-156 | `lcy_integration_deal` | S / M | 18-WF01, 18-WF02, 18-WF03, 18-WF04 |
| 72 | `sales_bid` | ENT-133 | `com_bid` | S / M | 19-WF01, 19-WF02, 19-WF03, 19-WF04 |
| 73 | `growth_invoice` | ENT-140 | `com_invoice` | S / F | 20-WF01, 20-WF02, 20-WF03, 20-WF04, 21-WF01, 21-WF02, 21-WF03, 21-WF04, 28-WF01, 28-WF02 (list truncated in source) |
| 74 | `growth_payment` | ENT-142 | `com_payment` | S / F | 20-WF01, 20-WF02, 20-WF03, 20-WF04, 21-WF01, 21-WF02, 21-WF03, 21-WF04, 24-WF01, 24-WF02 (list truncated in source) |
| 75 | `sales_fulfillment` | ENT-137 | `com_fulfillment_event` | S / A | 20-WF01, 20-WF02, 20-WF03, 20-WF04, 28-WF01, 28-WF02, 28-WF03, 28-WF04, 31-WF01, 31-WF02 (list truncated in source) |
| 76 | `sales_order` | ENT-135 | `com_order` | S / F | 20-WF01, 20-WF02, 20-WF03, 20-WF04, 28-WF01, 28-WF02, 28-WF03, 28-WF04, 31-WF01, 31-WF02 (list truncated in source) |
| 77 | `sales_order_line` | ENT-136 | `com_order_line` | S / F | 20-WF01, 20-WF02, 20-WF03, 20-WF04, 28-WF01, 28-WF02, 28-WF03, 28-WF04, 31-WF01, 31-WF02 (list truncated in source) |
| 78 | `growth_onboarding` | ENT-147 | `lcy_onboarding` | S / M | 22-WF01, 22-WF02, 22-WF03, 22-WF04, 33-WF01, 33-WF02, 33-WF03, 33-WF04 |
| 79 | `growth_deployment` | ENT-155 | `lcy_deployment` | S / M | 22-WF01, 22-WF02, 22-WF03, 22-WF04, 32-WF01, 32-WF02, 32-WF03, 32-WF04 |
| 80 | `growth_partner` | ENT-153 | `lcy_partner` | S / M | 22-WF01, 22-WF02, 22-WF03, 22-WF04, 32-WF01, 32-WF02, 32-WF03, 32-WF04 |
| 81 | `growth_pilot` | ENT-154 | `lcy_pilot` | S / M | 22-WF01, 22-WF02, 22-WF03, 22-WF04, 32-WF01, 32-WF02, 32-WF03, 32-WF04 |
| 82 | `growth_renewal` | ENT-150 | `lcy_renewal` | S / M | 23-WF01, 23-WF02, 23-WF03, 23-WF04, 34-WF01, 34-WF02, 34-WF03, 34-WF04 |
| 83 | `growth_feedback` | ENT-049 | `ai_feedback` | S / A | 23-WF01, 23-WF02, 23-WF03, 23-WF04, 35-WF01, 35-WF02, 35-WF03, 35-WF04 |
| 84 | `growth_metric_snapshot` | ENT-192 | `ana_metric_snapshot` | S / A | 24-WF01, 24-WF02, 24-WF03, 24-WF04, 30-WF01, 30-WF02, 30-WF03, 30-WF04, 32-WF01, 32-WF02 (list truncated in source) |
| 85 | `growth_forecast` | ENT-196 | `ana_forecast` | S / A | 24-WF01, 24-WF02, 24-WF03, 24-WF04, 37-WF01, 37-WF02, 37-WF03, 37-WF04 |
| 86 | `growth_stage_metric` | ENT-197 | `ana_stage_metric` | S / A | 24-WF01, 24-WF02, 24-WF03, 24-WF04, 37-WF01, 37-WF02, 37-WF03, 37-WF04 |
| 87 | `growth_document` | ENT-024 | `cat_document` | S / V | 25-WF01, 25-WF02, 25-WF03, 25-WF04 |
| 88 | `growth_document_chunk` | ENT-025 | `cat_chunk` | S / A | 25-WF01, 25-WF02, 25-WF03, 25-WF04 |
| 89 | `growth_embedding` | ENT-026 | `cat_embedding` | S / A | 25-WF01, 25-WF02, 25-WF03, 25-WF04 |

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
