-- V0001__extensions_schema_roles
SET search_path = ge, extensions, public;

SELECT set_config('app.zone', coalesce(nullif(current_setting('app.deployment_region', true), ''), 'IN'), false);

SELECT set_config('app.deployment_region', coalesce(nullif(current_setting('app.deployment_region', true), ''), 'IN'), false);

CREATE SCHEMA IF NOT EXISTS extensions;

CREATE SCHEMA IF NOT EXISTS ge;

CREATE EXTENSION IF NOT EXISTS pgcrypto WITH SCHEMA extensions;

CREATE EXTENSION IF NOT EXISTS pg_trgm WITH SCHEMA extensions;

CREATE EXTENSION IF NOT EXISTS btree_gin WITH SCHEMA extensions;

CREATE EXTENSION IF NOT EXISTS citext WITH SCHEMA extensions;

DO $$ BEGIN IF EXISTS (SELECT 1 FROM pg_available_extensions WHERE name = 'vector') THEN EXECUTE 'CREATE EXTENSION IF NOT EXISTS vector WITH SCHEMA extensions'; ELSE RAISE NOTICE 'pgvector not available: halfvec columns are added by V0008 only where the extension exists (Supabase provides it; verify)'; END IF; END $$;

DO $$ BEGIN IF EXISTS (SELECT 1 FROM pg_available_extensions WHERE name = 'pg_stat_statements') THEN EXECUTE 'CREATE EXTENSION IF NOT EXISTS pg_stat_statements WITH SCHEMA extensions'; END IF; END $$;

DO $$ BEGIN IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'anon') THEN CREATE ROLE anon NOLOGIN; END IF; END $$;

DO $$ BEGIN IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'authenticated') THEN CREATE ROLE authenticated NOLOGIN; END IF; END $$;

DO $$ BEGIN IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'service_role') THEN CREATE ROLE service_role NOLOGIN; END IF; END $$;

DO $$ BEGIN IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'app_owner') THEN CREATE ROLE app_owner NOLOGIN NOBYPASSRLS NOSUPERUSER NOCREATEDB NOCREATEROLE; END IF; END $$;

DO $$ BEGIN IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'app_migrator') THEN CREATE ROLE app_migrator LOGIN NOBYPASSRLS NOSUPERUSER NOCREATEDB NOCREATEROLE; END IF; END $$;

DO $$ BEGIN IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'app_rw') THEN CREATE ROLE app_rw LOGIN NOBYPASSRLS NOSUPERUSER NOCREATEDB NOCREATEROLE; END IF; END $$;

DO $$ BEGIN IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'app_worker') THEN CREATE ROLE app_worker LOGIN NOBYPASSRLS NOSUPERUSER NOCREATEDB NOCREATEROLE; END IF; END $$;

DO $$ BEGIN IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'app_readonly') THEN CREATE ROLE app_readonly LOGIN NOBYPASSRLS NOSUPERUSER NOCREATEDB NOCREATEROLE; END IF; END $$;

DO $$ BEGIN IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'app_retention') THEN CREATE ROLE app_retention LOGIN NOBYPASSRLS NOSUPERUSER NOCREATEDB NOCREATEROLE; END IF; END $$;

DO $$ BEGIN IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'app_audit_writer') THEN CREATE ROLE app_audit_writer NOLOGIN NOBYPASSRLS NOSUPERUSER NOCREATEDB NOCREATEROLE; END IF; END $$;

DO $$ BEGIN IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'app_platform_sec') THEN CREATE ROLE app_platform_sec LOGIN NOBYPASSRLS NOSUPERUSER NOCREATEDB NOCREATEROLE; END IF; END $$;

DO $$ BEGIN IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'app_bench') THEN CREATE ROLE app_bench LOGIN NOBYPASSRLS NOSUPERUSER NOCREATEDB NOCREATEROLE; END IF; END $$;

DO $$ BEGIN IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'app_registry') THEN CREATE ROLE app_registry LOGIN NOBYPASSRLS NOSUPERUSER NOCREATEDB NOCREATEROLE; END IF; END $$;

GRANT app_owner TO app_migrator;

ALTER SCHEMA ge OWNER TO app_owner;

REVOKE ALL ON SCHEMA ge FROM PUBLIC;

DO $$ BEGIN EXECUTE 'REVOKE ALL ON SCHEMA ge FROM anon, authenticated'; END $$;

GRANT USAGE ON SCHEMA ge TO app_rw, app_worker, app_readonly, app_retention, app_audit_writer, app_platform_sec, app_bench, app_registry;

GRANT USAGE ON SCHEMA extensions TO app_owner, app_rw, app_worker, app_readonly, app_retention, app_audit_writer, app_platform_sec, app_bench, app_registry;

ALTER DEFAULT PRIVILEGES IN SCHEMA ge REVOKE ALL ON TABLES FROM PUBLIC;

ALTER DEFAULT PRIVILEGES IN SCHEMA ge REVOKE EXECUTE ON FUNCTIONS FROM PUBLIC;

DO $$ BEGIN EXECUTE format('ALTER DATABASE %I SET search_path = ge, extensions, public', current_database()); END $$;

ALTER ROLE app_bench SET search_path = ge, extensions, public;

ALTER ROLE app_migrator SET search_path = ge, extensions, public;

ALTER ROLE app_owner SET search_path = ge, extensions, public;

ALTER ROLE app_platform_sec SET search_path = ge, extensions, public;

ALTER ROLE app_readonly SET search_path = ge, extensions, public;

ALTER ROLE app_registry SET search_path = ge, extensions, public;

ALTER ROLE app_retention SET search_path = ge, extensions, public;

ALTER ROLE app_rw SET search_path = ge, extensions, public;

ALTER ROLE app_worker SET search_path = ge, extensions, public;
