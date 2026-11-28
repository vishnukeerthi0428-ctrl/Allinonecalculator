-- V0015__ci_assertions
SET search_path = ge, extensions, public;

SELECT set_config('app.zone', coalesce(nullif(current_setting('app.deployment_region', true), ''), 'IN'), false);

SELECT set_config('app.deployment_region', coalesce(nullif(current_setting('app.deployment_region', true), ''), 'IN'), false);

DO $$ BEGIN
  IF EXISTS (SELECT 1 FROM pg_roles WHERE rolname IN ('app_rw','app_worker','app_readonly','app_retention','app_bench','app_registry','app_migrator','app_platform_sec') AND (rolbypassrls OR rolsuper)) THEN
    RAISE EXCEPTION 'APP_ROLE_CAN_BYPASS_RLS'; END IF;
  IF EXISTS (SELECT 1 FROM pg_class c JOIN pg_namespace n ON n.oid = c.relnamespace
             WHERE n.nspname = 'ge' AND c.relkind IN ('r','p') AND c.relname NOT IN (SELECT table_name FROM ge.platform_table_allowlist)
               AND NOT (c.relrowsecurity AND c.relforcerowsecurity)) THEN
    RAISE EXCEPTION 'TENANT_TABLE_WITHOUT_FORCED_RLS'; END IF;
  IF EXISTS (SELECT 1 FROM pg_class c JOIN pg_namespace n ON n.oid = c.relnamespace
             WHERE n.nspname = 'ge' AND c.relkind IN ('r','p') AND c.relname NOT IN (SELECT table_name FROM ge.platform_table_allowlist)
               AND NOT EXISTS (SELECT 1 FROM pg_policies p WHERE p.schemaname = 'ge' AND p.tablename = c.relname AND p.cmd IN ('SELECT','ALL'))) THEN
    RAISE EXCEPTION 'TENANT_TABLE_WITHOUT_SELECT_POLICY'; END IF;
  IF EXISTS (SELECT 1 FROM information_schema.role_table_grants WHERE table_schema = 'ge' AND grantee IN ('anon','authenticated','PUBLIC')) THEN
    RAISE EXCEPTION 'DATA_API_ROLE_HAS_GRANT'; END IF;
END $$;
