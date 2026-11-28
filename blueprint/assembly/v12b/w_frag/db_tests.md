| Test | Check | Result |
|---|---|---|
| TC-W-DB-01 | schema.sql applies in one transaction with ON_ERROR_STOP on a clean IN database | PASS |
| TC-W-DB-02 | schema.sql applies in one transaction with ON_ERROR_STOP on a clean EU database | PASS |
| TC-W-DB-03 | No application role has BYPASSRLS or SUPERUSER (DEC-778) | PASS |
| TC-W-DB-04 | Every tenant table has ENABLE + FORCE row-level security | PASS |
| TC-W-DB-05 | Every tenant table has a SELECT policy | PASS |
| TC-W-DB-06 | Data API roles (anon, authenticated) and service_role hold no grant on schema ge (SA-01, SA-02) | PASS |
| TC-W-DB-07 | No FOR ALL policy applies to PUBLIC (command-split policies only; Part 11.9b F2) | PASS |
| TC-W-DB-08 | Every foreign key has a supporting index (Part 11.9b F4) | PASS |
| TC-W-DB-09 | app_rw and app_worker hold no DELETE or TRUNCATE grant (archive, never delete; SA-08) | PASS |
| TC-W-DB-10 | Missing tenant context fails closed (42501) on a company-scoped table | PASS |
| TC-W-DB-11 | app_rw inserts and reads its own company row through set_ctx (P-CO) | PASS |
| TC-W-DB-12 | Company isolation inside one tenant: company A2 session sees 0 rows of A1 (Part 11.9b F1, MT-09) | PASS |
| TC-W-DB-13 | Tenant isolation: tenant B session sees 0 rows of tenant A | PASS |
| TC-W-DB-14 | Write into a company outside the write scope is rejected by WITH CHECK | PASS |
| TC-W-DB-15 | Write into another tenant is rejected by WITH CHECK | PASS |
| TC-W-DB-16 | set_ctx rejects a write company outside the session company list | PASS |
| TC-W-DB-17 | app_rw cannot DELETE business rows (no grant) | PASS |
| TC-W-DB-18 | Portfolio read (two companies, no write company) sees the union and cannot write | PASS |
| TC-W-DB-19 | Portfolio session (no write company) cannot insert | PASS |
| TC-W-DB-20 | V12 compatibility view growth_deal is security_invoker (RLS of crm_deal applies) | PASS |
| TC-W-DB-21 | IN database rejects an EU tenant (CJ-TC-09 IN→EU direction) | PASS |
| TC-W-DB-22 | Tenant data_region is immutable after onboarding (CJ-R09) | PASS |
| TC-W-DB-23 | set_ctx rejects a request routed to the wrong zone (RESIDENCY_ZONE_MISMATCH) | PASS |
| TC-W-DB-24 | Row-level residency guard rejects region EU on agent_credential in the IN database | PASS |
| TC-W-DB-25 | EU database rejects an IN tenant (CJ-TC-09 EU→IN direction) | PASS |
| TC-W-DB-26 | EU database accepts an EU tenant | PASS |
| TC-W-DB-27 | Append-only table cat_launch_approval rejects UPDATE (IMMUTABLE_RECORD, NFR-018) | PASS |
| TC-W-DB-28 | UPDATE without revision + 1 is rejected (STALE_REVISION, NFR-025) | PASS |
| TC-W-DB-29 | UPDATE with revision + 1 succeeds and bumps updated_at | PASS |
| TC-W-DB-30 | Audit events are appended only through fn_append_audit and the per-tenant hash chain verifies | PASS |
| TC-W-DB-31 | Direct INSERT into audit_event by app_rw is refused | PASS |
| TC-W-DB-32 | Typed domain table intel_signal_type rejects a payload without schema_ref (DEC-661) | PASS |
| TC-W-DB-33 | SSO cannot be enforced without a verified domain and a break-glass account (Part 11.19a) | PASS |
| TC-W-DB-34 | app_rw cannot read benchmark_contribution (only app_bench; DEC-789) | PASS |
| TC-W-DB-35 | Supabase anon role cannot read business tables (Data API closed, SA-01) | PASS |
| TC-W-DB-36 | Approved version of cat_offering_capability is frozen (fn_freeze_versioned, BRL-APR-02) | PASS |
| TC-W-DB-37 | Portal object-grant policy present on the eight portal-visible tables (CA-PORTAL, ABAC-09) | PASS |
| TC-W-DB-38 | Context does not leak across transactions on a pooled connection (SB-03) | PASS |
| TC-W-DB-39 | Capability cannot be activated while a required rule pack is in draft (ACTIVATION_PACK_NOT_APPROVED) | PASS |
| TC-W-DB-40 | Capability without any rule pack for the jurisdiction is not activatable (ACTIVATION_NO_RULE_PACK) | PASS |
| TC-W-DB-41 | Activation needs two different approvers, neither the requester (two-person rule) | PASS |
| TC-W-DB-42 | Activation succeeds once every required pack is approved with counsel sign-off and two approvers | PASS |
