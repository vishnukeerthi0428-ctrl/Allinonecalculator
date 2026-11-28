| # | Migration file (final/build/migrations/) | Content | Statements | CREATE TABLE |
|---|---|---|---|---|
| 1 | `V0001__extensions_schema_roles.sql` | Extensions (schema extensions), schema ge, ten canonical roles, Data API closure, default privileges | 42 | 0 |
| 2 | `V0002__context_functions.sql` | Context functions: app_tenant(), app_company_ids(), app_write_company(), app_actor_*(), app_zone(), set_ctx(), require_ctx(), ctx_* aliases | 15 | 0 |
| 3 | `V0003__v12_core_and_enterprise_spine.sql` | FSD V12 Appendix C core (29) + C2 enterprise (19) tables; customer FOR ALL policies dropped; 89 generic growth_* tables not created (DEC-661) | 116 | 48 |
| 4 | `V0004__ddl_v12_i_appendix_c3_controls.sql` | Appendix C3 (Part 11.9b): roles grants, scope integrity, 80 CHECKs, residency guard, SoD, audit hash chain, breach clocks, crypto-shredding, registry, 18 tables, verified policies and indexes | 648 | 18 |
| 5 | `V0005__reconcile_v12_lineage_for_ddl_v12_r.sql` | Reconciliation patch: columns DDL-V12-R expects (tenant.kind, jurisdiction_pack.market/pack_code/counsel_signoff_ref, ai_model evidence columns), app_user | 15 | 1 |
| 6 | `V0006__ddl_v12_r_platform_decisions.sql` | DDL-V12-R parts 1–6 (Part 11.19a/b): identity, SCIM, roles, API keys, OAuth clients, webhooks, sandbox, connectors, CRM sync, DLT, Vercel conformance, recovery, registry, benchmarks | 110 | 37 |
| 7 | `V0007__typed_tables_blueprint_and_v12b.sql` | Typed tables: Part 3.3 (199 entities + 13 association tables), Part 3.6 ENT-ENH-E-01…04, V12-B tables of Parts 11.16a/c, 11.17b, 11.18b | 758 | 365 |
| 8 | `V0008__blueprint_columns_and_part_3_6_deltas.sql` | Part 3.3 columns on the V12-realised entities; Part 3.6b ALTER deltas; DEC-661 common columns (schema_ref, evidence_refs, payload) | 324 | 0 |
| 9 | `V0008a__activation_gates_and_rule_pack_requirements.sql` | Rule-pack requirements (capability × jurisdiction × pack), tenant_activation with two-person check and DB activation gate; 32 packs seeded as Draft | 120 | 2 |
| 10 | `V0009__constraints_and_foreign_keys.sql` | CHECK and UNIQUE constraints from the dictionaries; foreign keys (dictionary arrows, composite scope keys, Part 3.6b) | 2053 | 0 |
| 11 | `V0010__triggers.sql` | Triggers: revision/updated_at, append-only, versioned freeze, domain registry (typed), row residency guard | 669 | 0 |
| 12 | `V0011__rls_policies_and_grants.sql` | RLS ENABLE + FORCE, command-split policies (P-CO, P-CO-NULLABLE, P-TEN, P-X, portal object grants), grants per role, platform allowlist | 3724 | 1 |
| 13 | `V0012__indexes.sql` | Indexes: FK support, Part 3.3 §3.3.8.2 key indexes, Part 3.6b IX-ENH-E, list indexes (tenant, company, state, updated_at) | 486 | 0 |
| 14 | `V0013__compatibility_views.sql` | Compatibility views (security_invoker): 89 V12 logical names over typed tables; Part 3.3 names over V12 spine tables | 257 | 0 |
| 15 | `V0014__seed_reference_data.sql` | Seed: currencies, recovery paths per zone (P1/P2/P3), Vercel edge projects (bom1/fra1) | 20 | 0 |
| 16 | `V0015__ci_assertions.sql` | CI assertions: no RLS bypass, forced RLS, SELECT policy on every tenant table, no Data API grants | 4 | 0 |
|  | **Total** |  | **9361** | **472** |
